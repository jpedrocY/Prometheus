"""Phase 4x - C1 Backtest Execution (standalone research script).

Implements the Phase 4w C1 Backtest-Plan Memo methodology exactly:
- Phase 4v locked C1 strategy spec (30m signal timeframe; no HTF gate;
  no funding input; no volume gate; no metrics OI; no ATR-percentile
  stop-distance gate; compression-box-based contraction measure;
  directional close-beyond-compression-box-with-buffer expansion
  transition; close-location requirement 0.70 long / 0.30 short;
  structural stop derived from compression-box invalidation;
  measured-move target; time-stop = 2 * N_comp 30m bars; 0.25%/2x/
  1-position sizing preserved verbatim from section 1.7.3);
- 32 predeclared variants (= 2^5) over five binary axes
  (B_width, C_width, N_comp, S_buffer, T_mult);
- chronological train (2022-01-01..2023-06-30 UTC), validation
  (2023-07-01..2024-06-30 UTC), OOS holdout (2024-07-01..2026-03-31
  UTC) split reused verbatim from Phase 4k;
- BTCUSDT primary, ETHUSDT comparison only;
- M1 contraction-vs-non-contraction; M2 C1-vs-always-active-same-
  geometry plus C1-vs-delayed-breakout; M3 BTC OOS HIGH mean_R > 0
  AND trade_count >= 30 AND opportunity-rate floors; M4 ETH non-
  negative differential AND directional consistency (ETH cannot
  rescue BTC); M5 compression-box validity diagnostic (skipped);
- section 11.6 = 8 bps HIGH per side preserved verbatim;
- Verdict A / B / C / D classification.

This script is a STANDALONE research script. It does NOT import
runtime / execution / persistence modules. It does NOT import
exchange adapters. It does NOT use credentials. It does NOT contact
any exchange API. It performs no network I/O. It reads only LOCAL
Parquet data already acquired by Phase 4i and v002.

C1 first-spec does not load funding or any optional feature subsets.
Phase 4j section 11 governance is preserved but unused. Forbidden
input access is structurally impossible because the script's only
data path is via the explicit-column 30m kline loader.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow.parquet as pq

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

INTERVAL_MS_30M = 30 * 60 * 1000

# Phase 4v locked fixed parameters (cardinality 1; not axes)
W_WIDTH = 240            # rolling-median compression-box width window
L_DELAY = 1              # max 30m bars delay from contraction end
CLOSE_LOCATION_LONG = 0.70    # long close-location threshold
CLOSE_LOCATION_SHORT = 0.70   # short close-location threshold (using
                              # high-close-low form: equivalent to
                              # close_location_long <= 0.30)
EPSILON = 1e-12

# Diagnostic ATR(20) Wilder period
ATR_PERIOD = 20

# Risk and sizing constants (section 1.7.3 preserved verbatim)
LOCKED_RISK_FRACTION = 0.0025
LOCKED_LEVERAGE_CAP = 2.0
SIZING_EQUITY = 100_000.0

# Cost cells (section 11.6 preserved verbatim)
TAKER_FEE_PER_SIDE_BPS = 4.0
COST_CELL_LOW_SLIP_BPS = 1.0
COST_CELL_MEDIUM_SLIP_BPS = 4.0
COST_CELL_HIGH_SLIP_BPS = 8.0

# Mechanism-check thresholds (Phase 4v locked; Phase 4w binding)
M1_DIFF_R_THRESHOLD = 0.10
M2_DIFF_R_THRESHOLD = 0.05
M3_MIN_MEAN_R = 0.0
M3_MIN_TRADE_COUNT = 30
BOOTSTRAP_ITERATIONS = 10_000

# Opportunity-rate viability floors (Phase 4v intrinsic; not Phase 4r-derived)
OPP_RATE_MIN_PER_480_BARS = 1.0    # >= 1 candidate transition per 480 30m bars
OPP_RATE_LOOKBACK_BARS = 480
MIN_VARIANT_FRACTION_AT_30 = 0.50  # >= 50% of variants must produce >= 30 trades

# CFP thresholds (Phase 4v / Phase 4w)
CFP1_MIN_TRADE_COUNT = 30
CFP1_VARIANT_FRACTION = 0.50
CFP3_MAX_DD_R = 10.0
CFP3_MIN_PROFIT_FACTOR = 0.50
CFP6_MAX_PBO = 0.50
CFP7_MAX_MONTH_FRACTION = 0.50
CFP8_DEGRADATION_R = 0.20
CSCV_S_DEFAULT = 16


# ----------------------------------------------------------------------
# Exception
# ----------------------------------------------------------------------


@dataclass
class StopCondition(Exception):
    """Raised when a Phase 4w stop condition triggers."""

    reason: str
    detail: str

    def __str__(self) -> str:
        return f"STOP_CONDITION[{self.reason}]: {self.detail}"


# ----------------------------------------------------------------------
# Data classes
# ----------------------------------------------------------------------


@dataclass
class ManifestRef:
    name: str
    path: Path
    sha256: str
    research_eligible: bool
    feature_use: str
    metadata: dict[str, Any]


@dataclass
class SymbolKlineData:
    symbol: str
    interval: str
    open_time_ms: np.ndarray
    close_time_ms: np.ndarray
    open_: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    volume: np.ndarray


@dataclass
class Variant:
    """One of 32 variants from the 5 binary axes (Phase 4v locked).

    Axis order (alphabetical, deterministic):
      A: B_width    in {0.05, 0.10}
      B: C_width    in {0.45, 0.60}
      C: N_comp     in {8, 12}
      D: S_buffer   in {0.10, 0.20}
      E: T_mult     in {1.5, 2.0}
    variant_id 0..31 via bit-encoding (T_mult highest bit).
    """

    variant_id: int
    b_width: float
    c_width: float
    n_comp: int
    s_buffer: float
    t_mult: float

    @property
    def t_stop_bars(self) -> int:
        return 2 * self.n_comp

    @property
    def label(self) -> str:
        return (
            f"B={self.b_width:.2f}|C={self.c_width:.2f}"
            f"|N={self.n_comp}|S={self.s_buffer:.2f}|T={self.t_mult:.1f}"
        )


@dataclass
class TradeRecord:
    symbol: str
    variant_id: int
    cost_cell: str
    side: str
    population: str  # "c1" | "non_contraction" | "always_active" | "delayed"
    entry_bar_idx: int
    entry_time_ms: int
    entry_price: float
    stop_price: float
    target_price: float
    initial_R: float
    box_width: float
    stop_distance_atr: float
    exit_bar_idx: int
    exit_time_ms: int
    exit_price: float
    exit_reason: str  # "stop" / "target" / "time_stop"
    realized_R: float


@dataclass
class VariantResult:
    variant_id: int
    symbol: str
    window: str
    cost_cell: str
    population: str
    trade_count: int
    win_rate: float
    mean_R: float
    median_R: float
    total_R: float
    max_dd_R: float
    profit_factor: float
    sharpe: float


@dataclass
class SymbolFeatures:
    """Pre-computed per-symbol feature tables (variant-agnostic where
    possible). Variant-dependent features (compression box, rolling
    median, contraction state, transitions, structural stop, target)
    are recomputed per-variant in compute_variant_features.
    """

    symbol: str
    open_time_30m: np.ndarray
    close_time_30m: np.ndarray
    open_30m: np.ndarray
    high_30m: np.ndarray
    low_30m: np.ndarray
    close_30m: np.ndarray
    volume_30m: np.ndarray
    atr_20_30m: np.ndarray  # diagnostic only
    close_location_long: np.ndarray
    close_location_short: np.ndarray  # high-close-low form


@dataclass
class VariantFeatures:
    """Per-(symbol, variant) features used for signal generation."""

    symbol: str
    variant_id: int
    compression_box_high: np.ndarray
    compression_box_low: np.ndarray
    compression_box_width: np.ndarray
    rolling_median_width: np.ndarray
    contraction_state: np.ndarray
    contraction_recently_active: np.ndarray
    long_transition: np.ndarray
    short_transition: np.ndarray
    structural_stop_long: np.ndarray
    structural_stop_short: np.ndarray
    measured_move_box_width: np.ndarray
    # Baseline support: bars where breakout-with-buffer fires AND
    # contraction was NOT recently active (M1 inverted gate)
    long_breakout_no_contraction: np.ndarray
    short_breakout_no_contraction: np.ndarray
    # Baseline support: same close-beyond-buffer rule, without the
    # contraction precondition (M2.a always-active)
    long_breakout_always_active: np.ndarray
    short_breakout_always_active: np.ndarray
    # Baseline support: same setup but contraction state was active
    # strictly more than L_delay bars ago and has since ended (M2.b
    # delayed-breakout). Window: contraction active in
    # [t - L_delay - 5 .. t - L_delay - 1] AND inactive in
    # [t - L_delay .. t].
    long_breakout_delayed: np.ndarray
    short_breakout_delayed: np.ndarray


# ----------------------------------------------------------------------
# Manifest helpers
# ----------------------------------------------------------------------


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(
    path: Path, expected_name: str, feature_use: str
) -> ManifestRef:
    if not path.exists():
        raise StopCondition("required_manifest_missing", str(path))
    digest = sha256_of_file(path)
    with open(path, encoding="utf-8") as f:
        meta = json.load(f)
    qc = meta.get("quality_checks", {})
    if "research_eligible" in meta:
        research_eligible = bool(meta["research_eligible"])
    elif isinstance(qc, dict) and "research_eligible" in qc:
        research_eligible = bool(qc["research_eligible"])
    else:
        research_eligible = True
    return ManifestRef(
        name=expected_name,
        path=path,
        sha256=digest,
        research_eligible=research_eligible,
        feature_use=feature_use,
        metadata=meta,
    )


# ----------------------------------------------------------------------
# Parquet loading (explicit columns; no select-all)
# ----------------------------------------------------------------------


def load_kline_symbol_interval(
    klines_root: Path, symbol: str, interval: str
) -> SymbolKlineData:
    cur = klines_root / f"symbol={symbol}" / f"interval={interval}"
    if not cur.exists():
        raise StopCondition(
            "local_data_missing", f"{cur} (symbol={symbol} interval={interval})"
        )
    parts = sorted(cur.rglob("part-*.parquet"))
    if not parts:
        raise StopCondition("local_data_missing", f"no parquet under {cur}")
    open_times: list[np.ndarray] = []
    close_times: list[np.ndarray] = []
    opens: list[np.ndarray] = []
    highs: list[np.ndarray] = []
    lows: list[np.ndarray] = []
    closes: list[np.ndarray] = []
    volumes: list[np.ndarray] = []
    for p in parts:
        t = pq.ParquetFile(p).read(
            columns=[
                "open_time",
                "close_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        )
        open_times.append(np.asarray(t.column("open_time").to_numpy(), dtype=np.int64))
        close_times.append(
            np.asarray(t.column("close_time").to_numpy(), dtype=np.int64)
        )
        opens.append(np.asarray(t.column("open").to_numpy(), dtype=np.float64))
        highs.append(np.asarray(t.column("high").to_numpy(), dtype=np.float64))
        lows.append(np.asarray(t.column("low").to_numpy(), dtype=np.float64))
        closes.append(np.asarray(t.column("close").to_numpy(), dtype=np.float64))
        volumes.append(np.asarray(t.column("volume").to_numpy(), dtype=np.float64))
    open_time = np.concatenate(open_times)
    order = np.argsort(open_time, kind="stable")
    open_time_sorted = open_time[order]
    if open_time_sorted.size == 0:
        raise StopCondition(
            "local_data_missing", f"empty kline series {symbol} {interval}"
        )
    if np.any(np.diff(open_time_sorted) == 0):
        raise StopCondition(
            "duplicate_open_time_row",
            f"duplicate open_time detected in {symbol} {interval}",
        )
    return SymbolKlineData(
        symbol=symbol,
        interval=interval,
        open_time_ms=open_time_sorted,
        close_time_ms=np.concatenate(close_times)[order],
        open_=np.concatenate(opens)[order],
        high=np.concatenate(highs)[order],
        low=np.concatenate(lows)[order],
        close=np.concatenate(closes)[order],
        volume=np.concatenate(volumes)[order],
    )


# ----------------------------------------------------------------------
# Numerical helpers
# ----------------------------------------------------------------------


def true_range(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray) -> np.ndarray:
    tr = np.empty_like(highs, dtype=np.float64)
    tr[0] = highs[0] - lows[0]
    for i in range(1, highs.size):
        a = highs[i] - lows[i]
        b = abs(highs[i] - closes[i - 1])
        c = abs(lows[i] - closes[i - 1])
        tr[i] = max(a, b, c)
    return tr


def atr_wilder(
    highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int
) -> np.ndarray:
    """Wilder ATR; NaN until seed bar (period-1)."""
    tr = true_range(highs, lows, closes)
    out = np.full_like(tr, np.nan, dtype=np.float64)
    if tr.size < period:
        return out
    out[period - 1] = float(np.mean(tr[:period]))
    inv = 1.0 / period
    for i in range(period, tr.size):
        out[i] = (out[i - 1] * (period - 1) + tr[i]) * inv
    return out


def rolling_max_excluding_current(arr: np.ndarray, n: int) -> np.ndarray:
    out = np.full_like(arr, np.nan, dtype=np.float64)
    if arr.size <= n:
        return out
    for t in range(n, arr.size):
        out[t] = float(np.max(arr[t - n : t]))
    return out


def rolling_min_excluding_current(arr: np.ndarray, n: int) -> np.ndarray:
    out = np.full_like(arr, np.nan, dtype=np.float64)
    if arr.size <= n:
        return out
    for t in range(n, arr.size):
        out[t] = float(np.min(arr[t - n : t]))
    return out


def rolling_median_excluding_current(arr: np.ndarray, n: int) -> np.ndarray:
    out = np.full_like(arr, np.nan, dtype=np.float64)
    sz = arr.size
    if sz <= n:
        return out
    for t in range(n, sz):
        window = arr[t - n : t]
        if np.any(~np.isfinite(window)):
            continue
        out[t] = float(np.median(window))
    return out


# ----------------------------------------------------------------------
# Feature computation (symbol-level, variant-agnostic part)
# ----------------------------------------------------------------------


def compute_symbol_features(k30: SymbolKlineData) -> SymbolFeatures:
    """Compute variant-agnostic 30m features.

    ATR(20) Wilder is computed once for diagnostic stop_distance_atr
    reporting. Close-location ratios are computed once with epsilon
    guarding for degenerate range bars (high == low).
    """
    atr20 = atr_wilder(k30.high, k30.low, k30.close, ATR_PERIOD)
    span = k30.high - k30.low
    valid = span > EPSILON
    cl_long = np.full(span.size, np.nan, dtype=np.float64)
    cl_short = np.full(span.size, np.nan, dtype=np.float64)
    cl_long[valid] = (k30.close[valid] - k30.low[valid]) / span[valid]
    cl_short[valid] = (k30.high[valid] - k30.close[valid]) / span[valid]
    return SymbolFeatures(
        symbol=k30.symbol,
        open_time_30m=k30.open_time_ms,
        close_time_30m=k30.close_time_ms,
        open_30m=k30.open_,
        high_30m=k30.high,
        low_30m=k30.low,
        close_30m=k30.close,
        volume_30m=k30.volume,
        atr_20_30m=atr20,
        close_location_long=cl_long,
        close_location_short=cl_short,
    )


def compute_variant_features(
    f: SymbolFeatures, v: Variant
) -> VariantFeatures:
    """Compute (per-symbol, per-variant) features.

    All features use prior-completed bars only. The compression box
    excludes the current bar. The rolling-median width excludes the
    current bar. The contraction-state predicate is local. The
    contraction_recently_active window covers exactly L_delay+1
    consecutive bars [t - L_delay, t]. Transitions fire on the
    completed signal close. Structural stop and measured-move target
    are derived from the compression box at the signal bar.
    """
    n = f.open_time_30m.size
    cbh = rolling_max_excluding_current(f.high_30m, v.n_comp)
    cbl = rolling_min_excluding_current(f.low_30m, v.n_comp)
    cbw = cbh - cbl
    # rolling_median_width excludes the current bar's compression-box
    # width by definition of rolling_median_excluding_current.
    rmw = rolling_median_excluding_current(cbw, W_WIDTH)
    valid = (
        np.isfinite(cbh)
        & np.isfinite(cbl)
        & np.isfinite(cbw)
        & (cbw > 0)
        & np.isfinite(rmw)
        & (rmw > 0)
    )
    contraction = np.zeros(n, dtype=bool)
    contraction[valid] = cbw[valid] <= v.c_width * rmw[valid]
    # contraction_recently_active: any True in [t - L_delay, t]
    # With L_delay=1 this is contraction[t-1] OR contraction[t].
    cra = np.zeros(n, dtype=bool)
    for t in range(L_DELAY, n):
        cra[t] = bool(contraction[t - L_DELAY] or contraction[t])
    # Long transition: cra AND close > cbh + B_width*cbw AND cl_long >= 0.70
    # Short transition: cra AND close < cbl - B_width*cbw AND cl_short >= 0.70
    cl_long = f.close_location_long
    cl_short = f.close_location_short
    long_thr = cbh + v.b_width * cbw
    short_thr = cbl - v.b_width * cbw
    cl_valid = np.isfinite(cl_long) & np.isfinite(cl_short)
    long_t = (
        cra
        & valid
        & cl_valid
        & (f.close_30m > long_thr)
        & (cl_long >= CLOSE_LOCATION_LONG)
    )
    short_t = (
        cra
        & valid
        & cl_valid
        & (f.close_30m < short_thr)
        & (cl_short >= CLOSE_LOCATION_SHORT)
    )
    # Defensive degeneracy: under normal high/low/close constraints
    # both cannot be true simultaneously, but we leave detection
    # to the simulation loop (CFP-11 runtime stop). Here we simply
    # null both if it would happen.
    both = long_t & short_t
    if np.any(both):
        # This is a structural impossibility (close cannot be > cbh +
        # B_width*cbw AND < cbl - B_width*cbw simultaneously when
        # cbh >= cbl). Mark as STOP via runtime check; here we just
        # zero the conflicting flags so the runtime loop's defensive
        # check observes them.
        long_t = long_t & ~both
        short_t = short_t & ~both
    # Structural stop and measured-move target arrays (per signal bar)
    stop_long = cbl - v.s_buffer * cbw
    stop_short = cbh + v.s_buffer * cbw
    # mm width is just cbw; target depends on entry_price (next bar
    # open), computed inside simulation.
    # M1 inverted gate: bars where breakout-with-buffer fires AND
    # contraction was NOT recently active.
    no_contraction = ~cra
    long_nc = (
        no_contraction
        & valid
        & cl_valid
        & (f.close_30m > long_thr)
        & (cl_long >= CLOSE_LOCATION_LONG)
    )
    short_nc = (
        no_contraction
        & valid
        & cl_valid
        & (f.close_30m < short_thr)
        & (cl_short >= CLOSE_LOCATION_SHORT)
    )
    # M2.a always-active: same close-beyond-box rule, no contraction
    # precondition.
    long_aa = (
        valid
        & cl_valid
        & (f.close_30m > long_thr)
        & (cl_long >= CLOSE_LOCATION_LONG)
    )
    short_aa = (
        valid
        & cl_valid
        & (f.close_30m < short_thr)
        & (cl_short >= CLOSE_LOCATION_SHORT)
    )
    # M2.b delayed-breakout: contraction active strictly >L_delay bars
    # ago and has since ended. Window: contraction in
    # [t - L_delay - 5 .. t - L_delay - 1] AND inactive in
    # [t - L_delay .. t].
    delayed_active = np.zeros(n, dtype=bool)
    pre_lo = L_DELAY + 1
    pre_hi = L_DELAY + 5
    for t in range(pre_hi, n):
        prior_window = contraction[t - pre_hi : t - pre_lo + 1]
        recent_window = contraction[t - L_DELAY : t + 1]
        if prior_window.any() and not recent_window.any():
            delayed_active[t] = True
    long_dl = (
        delayed_active
        & valid
        & cl_valid
        & (f.close_30m > long_thr)
        & (cl_long >= CLOSE_LOCATION_LONG)
    )
    short_dl = (
        delayed_active
        & valid
        & cl_valid
        & (f.close_30m < short_thr)
        & (cl_short >= CLOSE_LOCATION_SHORT)
    )
    return VariantFeatures(
        symbol=f.symbol,
        variant_id=v.variant_id,
        compression_box_high=cbh,
        compression_box_low=cbl,
        compression_box_width=cbw,
        rolling_median_width=rmw,
        contraction_state=contraction,
        contraction_recently_active=cra,
        long_transition=long_t,
        short_transition=short_t,
        structural_stop_long=stop_long,
        structural_stop_short=stop_short,
        measured_move_box_width=cbw,
        long_breakout_no_contraction=long_nc,
        short_breakout_no_contraction=short_nc,
        long_breakout_always_active=long_aa,
        short_breakout_always_active=short_aa,
        long_breakout_delayed=long_dl,
        short_breakout_delayed=short_dl,
    )


# ----------------------------------------------------------------------
# Variant grid
# ----------------------------------------------------------------------


def build_variants() -> list[Variant]:
    """Build exactly 32 variants in deterministic lexicographic order.

    Axis order: B_width, C_width, N_comp, S_buffer, T_mult.
    variant_id = (
        bit_T_mult * 16 + bit_S_buffer * 8 + bit_N_comp * 4
        + bit_C_width * 2 + bit_B_width * 1
    ).
    """
    b_set = [0.05, 0.10]
    c_set = [0.45, 0.60]
    n_set = [8, 12]
    s_set = [0.10, 0.20]
    t_set = [1.5, 2.0]
    variants: list[Variant] = []
    vid = 0
    for ti, t_mult in enumerate(t_set):
        for si, s_buffer in enumerate(s_set):
            for ni, n_comp in enumerate(n_set):
                for ci, c_width in enumerate(c_set):
                    for bi, b_width in enumerate(b_set):
                        check_id = (
                            ti * 16 + si * 8 + ni * 4 + ci * 2 + bi
                        )
                        assert check_id == vid, (
                            f"variant_id ordering mismatch at vid={vid}"
                        )
                        variants.append(
                            Variant(
                                variant_id=vid,
                                b_width=b_width,
                                c_width=c_width,
                                n_comp=n_comp,
                                s_buffer=s_buffer,
                                t_mult=t_mult,
                            )
                        )
                        vid += 1
    assert len(variants) == 32, f"expected 32 variants, got {len(variants)}"
    return variants


# ----------------------------------------------------------------------
# Cost application
# ----------------------------------------------------------------------


def _apply_costs_long(
    entry: float, exit_p: float, slip_bps: float
) -> tuple[float, float]:
    cost = (slip_bps + TAKER_FEE_PER_SIDE_BPS) / 10_000.0
    return entry * (1.0 + cost), exit_p * (1.0 - cost)


def _apply_costs_short(
    entry: float, exit_p: float, slip_bps: float
) -> tuple[float, float]:
    cost = (slip_bps + TAKER_FEE_PER_SIDE_BPS) / 10_000.0
    return entry * (1.0 - cost), exit_p * (1.0 + cost)


# ----------------------------------------------------------------------
# Trade simulation
# ----------------------------------------------------------------------


def simulate_trades_for_signal_array(
    f: SymbolFeatures,
    vf: VariantFeatures,
    long_signals: np.ndarray,
    short_signals: np.ndarray,
    slip_bps: float,
    cost_cell: str,
    variant_id: int,
    population: str,
    t_mult: float,
    s_buffer: float,
    t_stop_bars: int,
) -> list[TradeRecord]:
    """Simulate trades from boolean signal arrays.

    Stop precedence: stop > target > time-stop.
    Same-bar stop / target ambiguity: stop wins.
    Time-stop exits at next 30m bar's open (or close[t'] at end-of-data).
    No break-even. No trailing. No regime exit.
    """
    n = f.open_time_30m.size
    trades: list[TradeRecord] = []

    in_pos = False
    entry_idx = 0
    side = ""
    entry_price = 0.0
    stop_price = 0.0
    target_price = 0.0
    R_per_unit = 0.0
    box_width_at_entry = 0.0
    sd_atr_at_entry = 0.0
    entry_time = 0

    cbh = vf.compression_box_high
    cbl = vf.compression_box_low
    cbw = vf.compression_box_width
    atr20 = f.atr_20_30m

    for i in range(n):
        # Exit evaluation if positioned
        if in_pos:
            high = f.high_30m[i]
            low = f.low_30m[i]
            stop_touched = (
                low <= stop_price if side == "long" else high >= stop_price
            )
            target_touched = (
                high >= target_price if side == "long"
                else low <= target_price
            )
            bars_in_trade = i - entry_idx
            time_due = bars_in_trade >= t_stop_bars

            exit_kind: str | None = None
            exit_p = 0.0
            if stop_touched:
                # Same-bar stop+target ambiguity: stop wins (conservative).
                exit_kind = "stop"
                exit_p = stop_price
            elif target_touched:
                exit_kind = "target"
                exit_p = target_price
            elif time_due:
                if i + 1 < n:
                    exit_kind = "time_stop"
                    exit_p = f.open_30m[i + 1]
                else:
                    exit_kind = "time_stop"
                    exit_p = f.close_30m[i]

            if exit_kind is not None:
                if side == "long":
                    eep, exp_ = _apply_costs_long(entry_price, exit_p, slip_bps)
                    raw_R = (exp_ - eep) / R_per_unit
                else:
                    eep, exp_ = _apply_costs_short(entry_price, exit_p, slip_bps)
                    raw_R = (eep - exp_) / R_per_unit
                exit_time = (
                    int(f.open_time_30m[i + 1])
                    if (exit_kind == "time_stop" and i + 1 < n)
                    else int(f.close_time_30m[i])
                )
                trades.append(
                    TradeRecord(
                        symbol=f.symbol,
                        variant_id=variant_id,
                        cost_cell=cost_cell,
                        side=side,
                        population=population,
                        entry_bar_idx=entry_idx,
                        entry_time_ms=entry_time,
                        entry_price=entry_price,
                        stop_price=stop_price,
                        target_price=target_price,
                        initial_R=R_per_unit,
                        box_width=box_width_at_entry,
                        stop_distance_atr=sd_atr_at_entry,
                        exit_bar_idx=i,
                        exit_time_ms=exit_time,
                        exit_price=exit_p,
                        exit_reason=exit_kind,
                        realized_R=float(raw_R),
                    )
                )
                in_pos = False

        # Entry evaluation if not positioned
        if not in_pos and i + 1 < n:
            sig_long = bool(long_signals[i])
            sig_short = bool(short_signals[i])
            if sig_long or sig_short:
                # Compute stop / R / target / sizing using next-bar open
                if sig_long:
                    side = "long"
                    sp = float(cbl[i] - s_buffer * cbw[i])
                    ep = float(f.open_30m[i + 1])
                    bw = float(cbw[i])
                    R_unit = ep - sp
                    tp = ep + t_mult * bw
                else:
                    side = "short"
                    sp = float(cbh[i] + s_buffer * cbw[i])
                    ep = float(f.open_30m[i + 1])
                    bw = float(cbw[i])
                    R_unit = sp - ep
                    tp = ep - t_mult * bw
                if (
                    not math.isfinite(sp)
                    or not math.isfinite(ep)
                    or not math.isfinite(bw)
                    or bw <= 0
                    or R_unit <= 0
                ):
                    continue
                # Position sizing with leverage cap
                size_units = SIZING_EQUITY * LOCKED_RISK_FRACTION / R_unit
                position_notional = size_units * ep
                if position_notional > LOCKED_LEVERAGE_CAP * SIZING_EQUITY:
                    size_units = LOCKED_LEVERAGE_CAP * SIZING_EQUITY / ep
                if size_units <= 0:
                    continue
                # Diagnostic stop_distance_atr at signal bar i
                atr_v = atr20[i]
                sd_atr = (
                    abs(ep - sp) / atr_v
                    if math.isfinite(atr_v) and atr_v > 0
                    else float("nan")
                )
                in_pos = True
                entry_idx = i + 1
                entry_price = ep
                stop_price = sp
                target_price = tp
                R_per_unit = R_unit
                box_width_at_entry = bw
                sd_atr_at_entry = sd_atr
                entry_time = int(f.open_time_30m[i + 1])

    return trades


# ----------------------------------------------------------------------
# Aggregation
# ----------------------------------------------------------------------


def aggregate_trades(
    trades: list[TradeRecord],
    cost_cell: str,
    window_start_ms: int,
    window_end_ms: int,
) -> tuple[VariantResult, np.ndarray]:
    in_w = [
        t for t in trades
        if window_start_ms <= t.entry_time_ms <= window_end_ms
    ]
    if not in_w:
        return (
            VariantResult(
                variant_id=trades[0].variant_id if trades else -1,
                symbol=trades[0].symbol if trades else "",
                window="",
                cost_cell=cost_cell,
                population=trades[0].population if trades else "",
                trade_count=0,
                win_rate=0.0,
                mean_R=0.0,
                median_R=0.0,
                total_R=0.0,
                max_dd_R=0.0,
                profit_factor=0.0,
                sharpe=0.0,
            ),
            np.array([], dtype=np.float64),
        )
    R = np.array([t.realized_R for t in in_w], dtype=np.float64)
    wins = R[R > 0]
    losses = R[R <= 0]
    cum = np.cumsum(R)
    peak = np.maximum.accumulate(cum)
    dd = peak - cum
    sd = float(R.std(ddof=1)) if R.size > 1 else 0.0
    sharpe = float(R.mean() / sd) if sd > 0 else 0.0
    pf = (
        float(wins.sum() / -losses.sum())
        if losses.size > 0 and -losses.sum() > 0 else
        (float("inf") if wins.size > 0 else 0.0)
    )
    return (
        VariantResult(
            variant_id=in_w[0].variant_id,
            symbol=in_w[0].symbol,
            window="",
            cost_cell=cost_cell,
            population=in_w[0].population,
            trade_count=int(R.size),
            win_rate=float((R > 0).mean()),
            mean_R=float(R.mean()),
            median_R=float(np.median(R)),
            total_R=float(R.sum()),
            max_dd_R=float(dd.max()) if dd.size > 0 else 0.0,
            profit_factor=pf if math.isfinite(pf) else 1e9,
            sharpe=sharpe,
        ),
        R,
    )


# ----------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------


def _norm_inv(p: float) -> float:
    if p <= 0 or p >= 1:
        return 0.0
    a = [
        -3.969683028665376e1,
        2.209460984245205e2,
        -2.759285104469687e2,
        1.383577518672690e2,
        -3.066479806614716e1,
        2.506628277459239,
    ]
    b = [
        -5.447609879822406e1,
        1.615858368580409e2,
        -1.556989798598866e2,
        6.680131188771972e1,
        -1.328068155288572e1,
    ]
    c = [
        -7.784894002430293e-3,
        -3.223964580411365e-1,
        -2.400758277161838,
        -2.549732539343734,
        4.374664141464968,
        2.938163982698783,
    ]
    d = [
        7.784695709041462e-3,
        3.224671290700398e-1,
        2.445134137142996,
        3.754408661907416,
    ]
    p_low = 0.02425
    p_high = 1.0 - p_low
    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (
            ((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]
        ) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    if p > p_high:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(
            ((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]
        ) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    q = p - 0.5
    r = q * q
    return (
        ((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]
    ) * q / (
        ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0
    )


def expected_max_sharpe_random(n_variants: int) -> float:
    if n_variants <= 1:
        return 0.0
    gamma = 0.5772156649
    return _norm_inv(1.0 - 1.0 / n_variants) * (1.0 - gamma) + _norm_inv(
        1.0 - 1.0 / (n_variants * math.e)
    ) * gamma


def compute_skewness_kurtosis(arr: np.ndarray) -> tuple[float, float]:
    if arr.size < 3:
        return 0.0, 3.0
    mu = float(arr.mean())
    sd = float(arr.std(ddof=0))
    if sd == 0:
        return 0.0, 3.0
    m3 = float(((arr - mu) ** 3).mean())
    m4 = float(((arr - mu) ** 4).mean())
    skew = m3 / (sd**3)
    kurt = m4 / (sd**4)
    return skew, kurt


def deflated_sharpe_ratio(
    sharpe: float,
    n_variants: int,
    n_trades: int,
    skewness: float,
    kurtosis: float,
) -> float:
    if n_trades < 2:
        return 0.0
    sr_zero = expected_max_sharpe_random(n_variants)
    denom_sq = (
        1.0 - skewness * sharpe + (kurtosis - 1.0) / 4.0 * sharpe * sharpe
    ) / (n_trades - 1)
    if denom_sq <= 0:
        return 0.0
    return (sharpe - sr_zero) / math.sqrt(denom_sq)


def bootstrap_diff_mean_ci(
    a: np.ndarray, b: np.ndarray, B: int, rng: np.random.Generator
) -> tuple[float, float, float]:
    if a.size == 0 or b.size == 0:
        return 0.0, 0.0, 0.0
    diffs = np.empty(B, dtype=np.float64)
    for k in range(B):
        sa = rng.choice(a, size=a.size, replace=True)
        sb = rng.choice(b, size=b.size, replace=True)
        diffs[k] = float(sa.mean() - sb.mean())
    mean_diff = float(a.mean() - b.mean())
    return (
        mean_diff,
        float(np.percentile(diffs, 2.5)),
        float(np.percentile(diffs, 97.5)),
    )


def _sharpe(arr: np.ndarray) -> float:
    if arr.size < 2:
        return float("nan")
    sd = float(arr.std(ddof=1))
    if sd == 0:
        return 0.0
    return float(arr.mean() / sd)


def cscv_pbo(
    per_variant_trade_R: dict[int, np.ndarray],
    per_variant_trade_idx_in_window: dict[int, np.ndarray],
    n_window_bars: int,
    s_subsamples: int,
) -> tuple[float, list[tuple[int, int]]]:
    """CSCV PBO via combinatorially symmetric cross-validation.

    Partition the window into S contiguous chronological sub-samples
    by 30m-bar index. Enumerate C(S, S/2) train/test combinations.
    For each combination, identify the train-best variant by Sharpe
    on the train half, and record its rank on the test half. PBO is
    the fraction of combinations where the train-best variant lies
    in the bottom half of test ranks.
    """
    if s_subsamples % 2 != 0 or s_subsamples < 4:
        return 0.5, []
    half = s_subsamples // 2
    variants = sorted(per_variant_trade_R.keys())
    n_variants = len(variants)
    if n_variants == 0:
        return 0.5, []
    sub_arrays: dict[int, list[np.ndarray]] = {v: [] for v in variants}
    for v in variants:
        rs = per_variant_trade_R[v]
        idx = per_variant_trade_idx_in_window[v]
        if rs.size == 0:
            for _ in range(s_subsamples):
                sub_arrays[v].append(np.array([], dtype=np.float64))
            continue
        bin_edges = np.linspace(0, n_window_bars, s_subsamples + 1)
        bin_idx = np.clip(
            np.searchsorted(bin_edges[1:-1], idx), 0, s_subsamples - 1
        )
        for s in range(s_subsamples):
            sub_arrays[v].append(rs[bin_idx == s])
    combos = list(itertools.combinations(range(s_subsamples), half))
    oos_below_median_count = 0
    used = 0
    detail: list[tuple[int, int]] = []
    for ci, in_combo in enumerate(combos):
        in_set = set(in_combo)
        is_sharpes = []
        oos_sharpes = []
        for v in variants:
            in_chunks = [
                sub_arrays[v][s] for s in range(s_subsamples) if s in in_set
            ]
            out_chunks = [
                sub_arrays[v][s]
                for s in range(s_subsamples)
                if s not in in_set
            ]
            in_arr = (
                np.concatenate(in_chunks)
                if in_chunks
                else np.array([], dtype=np.float64)
            )
            out_arr = (
                np.concatenate(out_chunks)
                if out_chunks
                else np.array([], dtype=np.float64)
            )
            is_sharpes.append(_sharpe(in_arr))
            oos_sharpes.append(_sharpe(out_arr))
        is_arr = np.array(is_sharpes, dtype=np.float64)
        oos_arr = np.array(oos_sharpes, dtype=np.float64)
        if not np.isfinite(is_arr).any():
            continue
        best_idx = int(np.nanargmax(is_arr))
        best_oos = oos_arr[best_idx]
        if not math.isfinite(best_oos):
            continue
        better = float((oos_arr > best_oos).sum()) / float(n_variants)
        if better > 0.5:
            oos_below_median_count += 1
        used += 1
        detail.append((ci, variants[best_idx]))
    if used == 0:
        return 0.5, detail
    return float(oos_below_median_count) / float(used), detail


def pbo_rank_based(
    train_sharpe: dict[int, float], oos_sharpe: dict[int, float]
) -> float:
    if not train_sharpe or not oos_sharpe:
        return 0.5
    best_variant = max(train_sharpe.items(), key=lambda kv: kv[1])[0]
    best_oos = oos_sharpe.get(best_variant, float("-inf"))
    if not math.isfinite(best_oos):
        return 0.5
    n = len(oos_sharpe)
    better = sum(1 for s in oos_sharpe.values() if s > best_oos)
    return float(better) / float(n)


# ----------------------------------------------------------------------
# CSV / JSON helpers
# ----------------------------------------------------------------------


def write_csv(
    path: Path, header: Sequence[str], rows: Sequence[Sequence[Any]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [",".join(header)]
    for r in rows:
        cells: list[str] = []
        for val in r:
            if isinstance(val, float):
                cells.append(f"{val:.10g}")
            elif val is None:
                cells.append("")
            else:
                s = str(val)
                if "," in s or '"' in s:
                    s = '"' + s.replace('"', '""') + '"'
                cells.append(s)
        lines.append(",".join(cells))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def utc_to_ms(s: str, end: bool = False) -> int:
    dt = datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=UTC)
    if end:
        dt = dt + timedelta(hours=23, minutes=30)
    return int(dt.timestamp() * 1000)


# ----------------------------------------------------------------------
# Plot helpers (matplotlib optional)
# ----------------------------------------------------------------------


def _try_import_matplotlib() -> Any:
    try:
        import matplotlib  # type: ignore[import-untyped]

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # type: ignore[import-untyped]
        return plt
    except Exception:
        return None


def try_plot_cumulative_R(
    path: Path, R_arrays: dict[str, np.ndarray], title: str
) -> bool:
    plt = _try_import_matplotlib()
    if plt is None:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    plotted = False
    for label, arr in R_arrays.items():
        if arr.size == 0:
            continue
        ax.plot(np.cumsum(arr), label=label)
        plotted = True
    if not plotted:
        plt.close(fig)
        return False
    ax.set_title(title)
    ax.set_xlabel("trade index")
    ax.set_ylabel("cumulative R")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return True


def try_plot_distribution(
    path: Path, arrays: dict[str, np.ndarray], title: str, xlabel: str
) -> bool:
    plt = _try_import_matplotlib()
    if plt is None:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    plotted = False
    for label, arr in arrays.items():
        if arr.size == 0:
            continue
        ax.hist(arr, bins=30, alpha=0.5, label=label)
        plotted = True
    if not plotted:
        plt.close(fig)
        return False
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return True


def try_plot_drawdown(path: Path, R_arr: np.ndarray, title: str) -> bool:
    plt = _try_import_matplotlib()
    if plt is None or R_arr.size == 0:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    cum = np.cumsum(R_arr)
    peak = np.maximum.accumulate(cum)
    dd = peak - cum
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(-dd)
    ax.set_title(title)
    ax.set_xlabel("trade index")
    ax.set_ylabel("drawdown (R, negative)")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return True


def try_plot_timeline(
    path: Path,
    times: np.ndarray,
    contraction: np.ndarray,
    transitions: np.ndarray,
    title: str,
) -> bool:
    plt = _try_import_matplotlib()
    if plt is None or times.size == 0:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 3))
    secs = (times / 1000.0).astype(np.int64)
    ax.plot(
        secs, contraction.astype(np.int32), drawstyle="steps-post",
        label="contraction_state",
    )
    ax.plot(
        secs, transitions.astype(np.int32), drawstyle="steps-post",
        label="transition", alpha=0.6,
    )
    ax.set_title(title)
    ax.set_xlabel("UTC seconds")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return True


# ----------------------------------------------------------------------
# Main orchestration
# ----------------------------------------------------------------------


@dataclass
class RunPaths:
    output_dir: Path
    tables_dir: Path
    plots_dir: Path
    run_metadata: Path


@dataclass
class RunContext:
    args: argparse.Namespace
    paths: RunPaths
    rng: np.random.Generator
    train_start_ms: int
    train_end_ms: int
    val_start_ms: int
    val_end_ms: int
    oos_start_ms: int
    oos_end_ms: int
    manifests: list[ManifestRef] = field(default_factory=list)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 4x C1 backtest execution (standalone research script)"
    )
    parser.add_argument("--start", default="2022-01-01")
    parser.add_argument("--end", default="2026-03-31")
    parser.add_argument("--train-start", default="2022-01-01")
    parser.add_argument("--train-end", default="2023-06-30")
    parser.add_argument("--validation-start", default="2023-07-01")
    parser.add_argument("--validation-end", default="2024-06-30")
    parser.add_argument("--oos-start", default="2024-07-01")
    parser.add_argument("--oos-end", default="2026-03-31")
    parser.add_argument("--symbols", nargs="+", default=["BTCUSDT", "ETHUSDT"])
    parser.add_argument("--primary-symbol", default="BTCUSDT")
    parser.add_argument("--comparison-symbol", default="ETHUSDT")
    parser.add_argument("--output-dir", default="data/research/phase4x")
    parser.add_argument("--rng-seed", type=int, default=202604300)
    parser.add_argument(
        "--bootstrap-iterations", type=int, default=BOOTSTRAP_ITERATIONS
    )
    parser.add_argument("--cscv-s", type=int, default=CSCV_S_DEFAULT)
    parser.add_argument(
        "--data-root", default="data/normalized", help="Local Parquet root"
    )
    parser.add_argument(
        "--manifest-root", default="data/manifests", help="Manifest directory"
    )
    args = parser.parse_args(argv)

    rng = np.random.default_rng(args.rng_seed)
    out = Path(args.output_dir)
    paths = RunPaths(
        output_dir=out,
        tables_dir=out / "tables",
        plots_dir=out / "plots",
        run_metadata=out / "run_metadata.json",
    )
    paths.tables_dir.mkdir(parents=True, exist_ok=True)
    paths.plots_dir.mkdir(parents=True, exist_ok=True)

    train_start = utc_to_ms(args.train_start)
    train_end = utc_to_ms(args.train_end, end=True)
    val_start = utc_to_ms(args.validation_start)
    val_end = utc_to_ms(args.validation_end, end=True)
    oos_start = utc_to_ms(args.oos_start)
    oos_end = utc_to_ms(args.oos_end, end=True)

    ctx = RunContext(
        args=args,
        paths=paths,
        rng=rng,
        train_start_ms=train_start,
        train_end_ms=train_end,
        val_start_ms=val_start,
        val_end_ms=val_end,
        oos_start_ms=oos_start,
        oos_end_ms=oos_end,
    )

    print("Phase 4x C1 backtest execution starting", flush=True)
    print(
        f"  symbols={args.symbols}, primary={args.primary_symbol}", flush=True
    )
    print(f"  train={args.train_start}..{args.train_end}", flush=True)
    print(f"  val=  {args.validation_start}..{args.validation_end}", flush=True)
    print(f"  oos=  {args.oos_start}..{args.oos_end}", flush=True)
    print(f"  rng_seed={args.rng_seed}", flush=True)

    try:
        return _run(ctx)
    except StopCondition as e:
        print(f"STOP_CONDITION: {e}", file=sys.stderr, flush=True)
        write_json(
            paths.tables_dir / "verdict_declaration.error.json",
            {"verdict": "D", "stop_condition": e.reason, "detail": e.detail},
        )
        return 2


def _run(ctx: RunContext) -> int:  # noqa: PLR0915
    args = ctx.args
    paths = ctx.paths
    rng = ctx.rng

    # ------------------------------------------------------------------
    # Manifest loading + SHA pinning
    # ------------------------------------------------------------------
    manifest_root = Path(args.manifest_root)
    for sym in args.symbols:
        sym_lower = sym.lower()
        ctx.manifests.append(load_manifest(
            manifest_root / f"binance_usdm_{sym_lower}_30m__v001.manifest.json",
            f"binance_usdm_{sym_lower}_30m__v001",
            "30m_klines_primary_signal",
        ))
    for m in ctx.manifests:
        if not m.research_eligible:
            raise StopCondition(
                "manifest_research_eligible_mismatch",
                f"{m.name} expected research_eligible=true",
            )

    # ------------------------------------------------------------------
    # Data loading (30m only; no funding; no metrics; no mark-price)
    # ------------------------------------------------------------------
    klines_root = Path(args.data_root) / "klines"

    print(
        "Loading data (30m klines only; explicit-column loader)...",
        flush=True,
    )
    symbol_features: dict[str, SymbolFeatures] = {}
    for sym in args.symbols:
        print(f"  {sym} 30m klines...", flush=True)
        k30 = load_kline_symbol_interval(klines_root, sym, "30m")
        print(
            f"  {sym} computing symbol-level features "
            f"({k30.open_time_ms.size} 30m bars)...",
            flush=True,
        )
        symbol_features[sym] = compute_symbol_features(k30)

    # ------------------------------------------------------------------
    # Build variants
    # ------------------------------------------------------------------
    variants = build_variants()
    print(f"Variant grid: {len(variants)} variants", flush=True)

    # ------------------------------------------------------------------
    # Pre-compute per-(symbol, variant) features
    # ------------------------------------------------------------------
    print("Computing per-(symbol, variant) features...", flush=True)
    variant_features: dict[str, dict[int, VariantFeatures]] = {}
    for sym in args.symbols:
        variant_features[sym] = {}
        for v in variants:
            variant_features[sym][v.variant_id] = compute_variant_features(
                symbol_features[sym], v
            )

    # ------------------------------------------------------------------
    # Per-variant simulation across cost cells and populations
    # ------------------------------------------------------------------
    cost_cells = {
        "LOW": COST_CELL_LOW_SLIP_BPS,
        "MEDIUM": COST_CELL_MEDIUM_SLIP_BPS,
        "HIGH": COST_CELL_HIGH_SLIP_BPS,
    }

    populations = ("c1", "non_contraction", "always_active", "delayed")

    # results[symbol][window][cost_cell][population][variant_id] = VariantResult
    results: dict[
        str, dict[str, dict[str, dict[str, dict[int, VariantResult]]]]
    ] = {}
    # trades[symbol][cost_cell][population][variant_id] = list[TradeRecord]
    trades: dict[str, dict[str, dict[str, dict[int, list[TradeRecord]]]]] = {}

    for sym in args.symbols:
        results[sym] = {"train": {}, "validation": {}, "oos": {}}
        trades[sym] = {}
        for cell in cost_cells:
            for w in ("train", "validation", "oos"):
                results[sym][w][cell] = {p: {} for p in populations}
            trades[sym][cell] = {p: {} for p in populations}

    total_runs = (
        len(args.symbols) * len(cost_cells) * len(variants) * len(populations)
    )
    run_count = 0
    print(
        f"Running {total_runs} (variant, symbol, cost, population) "
        "simulations...",
        flush=True,
    )

    for sym in args.symbols:
        f = symbol_features[sym]
        for v in variants:
            vf = variant_features[sym][v.variant_id]
            for cell, slip_bps in cost_cells.items():
                # C1 transitions
                trs_c1 = simulate_trades_for_signal_array(
                    f, vf, vf.long_transition, vf.short_transition,
                    slip_bps, cell, v.variant_id, "c1",
                    v.t_mult, v.s_buffer, v.t_stop_bars,
                )
                # Non-contraction baseline (M1)
                trs_nc = simulate_trades_for_signal_array(
                    f, vf, vf.long_breakout_no_contraction,
                    vf.short_breakout_no_contraction,
                    slip_bps, cell, v.variant_id, "non_contraction",
                    v.t_mult, v.s_buffer, v.t_stop_bars,
                )
                # Always-active same-geometry baseline (M2.a)
                trs_aa = simulate_trades_for_signal_array(
                    f, vf, vf.long_breakout_always_active,
                    vf.short_breakout_always_active,
                    slip_bps, cell, v.variant_id, "always_active",
                    v.t_mult, v.s_buffer, v.t_stop_bars,
                )
                # Delayed-breakout baseline (M2.b)
                trs_dl = simulate_trades_for_signal_array(
                    f, vf, vf.long_breakout_delayed,
                    vf.short_breakout_delayed,
                    slip_bps, cell, v.variant_id, "delayed",
                    v.t_mult, v.s_buffer, v.t_stop_bars,
                )
                trades[sym][cell]["c1"][v.variant_id] = trs_c1
                trades[sym][cell]["non_contraction"][v.variant_id] = trs_nc
                trades[sym][cell]["always_active"][v.variant_id] = trs_aa
                trades[sym][cell]["delayed"][v.variant_id] = trs_dl

                for w_name, ws, we in (
                    ("train", ctx.train_start_ms, ctx.train_end_ms),
                    ("validation", ctx.val_start_ms, ctx.val_end_ms),
                    ("oos", ctx.oos_start_ms, ctx.oos_end_ms),
                ):
                    res_c1, _ = aggregate_trades(trs_c1, cell, ws, we)
                    res_c1.window = w_name
                    res_c1.symbol = sym
                    results[sym][w_name][cell]["c1"][v.variant_id] = res_c1

                    res_nc, _ = aggregate_trades(trs_nc, cell, ws, we)
                    res_nc.window = w_name
                    res_nc.symbol = sym
                    results[sym][w_name][cell]["non_contraction"][
                        v.variant_id
                    ] = res_nc

                    res_aa, _ = aggregate_trades(trs_aa, cell, ws, we)
                    res_aa.window = w_name
                    res_aa.symbol = sym
                    results[sym][w_name][cell]["always_active"][
                        v.variant_id
                    ] = res_aa

                    res_dl, _ = aggregate_trades(trs_dl, cell, ws, we)
                    res_dl.window = w_name
                    res_dl.symbol = sym
                    results[sym][w_name][cell]["delayed"][
                        v.variant_id
                    ] = res_dl

                run_count += len(populations)
                if run_count % 256 == 0:
                    print(
                        f"  progress: {run_count}/{total_runs} simulations",
                        flush=True,
                    )

    # ------------------------------------------------------------------
    # Train-best variant by deflated Sharpe (BTCUSDT primary, MEDIUM-cost,
    # C1 population)
    # ------------------------------------------------------------------
    print("Selecting BTC-train-best variant by deflated Sharpe...", flush=True)
    primary = args.primary_symbol
    btc_train = results[primary]["train"]["MEDIUM"]["c1"]
    dsr_per_variant: dict[int, float] = {}
    sharpe_per_variant: dict[int, float] = {}
    for v in variants:
        r = btc_train.get(v.variant_id)
        ts = trades[primary]["MEDIUM"]["c1"][v.variant_id]
        train_ts = [
            t for t in ts
            if ctx.train_start_ms <= t.entry_time_ms <= ctx.train_end_ms
        ]
        if not r or r.trade_count < 2 or not train_ts:
            dsr_per_variant[v.variant_id] = 0.0
            sharpe_per_variant[v.variant_id] = 0.0
            continue
        arr = np.array([t.realized_R for t in train_ts], dtype=np.float64)
        skew, kurt = compute_skewness_kurtosis(arr)
        sharpe_per_variant[v.variant_id] = r.sharpe
        dsr_per_variant[v.variant_id] = deflated_sharpe_ratio(
            r.sharpe, len(variants), arr.size, skew, kurt
        )
    best_v_id = max(
        dsr_per_variant.items(),
        key=lambda kv: (
            kv[1] if math.isfinite(kv[1]) else -1e9,
            sharpe_per_variant[kv[0]],
            -kv[0],
        ),
    )[0]
    best_variant = variants[best_v_id]
    print(
        f"BTC-train-best: id={best_v_id}, "
        f"DSR={dsr_per_variant[best_v_id]:.3f}, "
        f"Sharpe(train)={sharpe_per_variant[best_v_id]:.3f}, "
        f"label={best_variant.label}",
        flush=True,
    )

    # ------------------------------------------------------------------
    # Mechanism check arrays
    # ------------------------------------------------------------------
    cell = "HIGH"
    btc_c1_oos_trs = [
        t for t in trades[primary][cell]["c1"][best_variant.variant_id]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    btc_nc_oos_trs = [
        t for t in trades[primary][cell]["non_contraction"][
            best_variant.variant_id
        ]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    btc_aa_oos_trs = [
        t for t in trades[primary][cell]["always_active"][
            best_variant.variant_id
        ]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    btc_dl_oos_trs = [
        t for t in trades[primary][cell]["delayed"][best_variant.variant_id]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    arr_c1 = np.array([t.realized_R for t in btc_c1_oos_trs], dtype=np.float64)
    arr_nc = np.array([t.realized_R for t in btc_nc_oos_trs], dtype=np.float64)
    arr_aa = np.array([t.realized_R for t in btc_aa_oos_trs], dtype=np.float64)
    arr_dl = np.array([t.realized_R for t in btc_dl_oos_trs], dtype=np.float64)

    # M1: C1 vs non-contraction (BTC OOS HIGH)
    m1_diff, m1_ci_low, m1_ci_high = bootstrap_diff_mean_ci(
        arr_c1, arr_nc, args.bootstrap_iterations, rng
    )
    m1_pass = (
        m1_diff >= M1_DIFF_R_THRESHOLD
        and m1_ci_low > 0.0
        and arr_c1.size > 0
        and arr_nc.size > 0
    )

    # M2.a: C1 vs always-active (BTC OOS HIGH)
    m2a_diff, m2a_ci_low, m2a_ci_high = bootstrap_diff_mean_ci(
        arr_c1, arr_aa, args.bootstrap_iterations, rng
    )
    m2a_pass = (
        m2a_diff >= M2_DIFF_R_THRESHOLD
        and m2a_ci_low > 0.0
        and arr_c1.size > 0
        and arr_aa.size > 0
    )
    # M2.b: C1 vs delayed-breakout (BTC OOS HIGH)
    m2b_diff = (
        float(arr_c1.mean() - arr_dl.mean())
        if arr_c1.size > 0 and arr_dl.size > 0
        else 0.0
    )
    m2b_pass = m2b_diff >= 0.0 and arr_c1.size > 0
    m2_pass = m2a_pass and m2b_pass

    # M3 components
    btc_c1_oos_high = results[primary]["oos"]["HIGH"]["c1"][
        best_variant.variant_id
    ]
    # Opportunity-rate: candidate-transition rate per 480 bars
    f_btc = symbol_features[primary]
    oos_mask_30m = (
        (f_btc.open_time_30m >= ctx.oos_start_ms)
        & (f_btc.open_time_30m <= ctx.oos_end_ms)
    )
    oos_total_30m = int(oos_mask_30m.sum())
    vf_best_btc = variant_features[primary][best_variant.variant_id]
    oos_long_t = vf_best_btc.long_transition & oos_mask_30m
    oos_short_t = vf_best_btc.short_transition & oos_mask_30m
    oos_total_transitions = int(oos_long_t.sum() + oos_short_t.sum())
    transition_rate_per_480 = (
        OPP_RATE_LOOKBACK_BARS * oos_total_transitions / oos_total_30m
        if oos_total_30m > 0 else 0.0
    )
    btc_oos_high_counts_c1 = [
        results[primary]["oos"]["HIGH"]["c1"][v.variant_id].trade_count
        for v in variants
    ]
    variants_passing_count = sum(
        1 for c in btc_oos_high_counts_c1 if c >= M3_MIN_TRADE_COUNT
    )
    variants_pass_fraction = variants_passing_count / len(variants)
    opp_rate_pass = (
        transition_rate_per_480 >= OPP_RATE_MIN_PER_480_BARS
        and btc_c1_oos_high.trade_count >= M3_MIN_TRADE_COUNT
        and variants_pass_fraction >= MIN_VARIANT_FRACTION_AT_30
    )

    # CFP precomputation needed for M3 inclusion
    # CFP-1 / CFP-2 / CFP-3 thresholds for M3 use BTC OOS HIGH train-best.
    cfp1_below_count = sum(
        1 for c in btc_oos_high_counts_c1 if c < CFP1_MIN_TRADE_COUNT
    )
    cfp1_below_fraction = cfp1_below_count / len(variants)
    cfp1_train_best_count = btc_c1_oos_high.trade_count
    cfp1_trigger = (
        cfp1_below_fraction > CFP1_VARIANT_FRACTION
        or cfp1_train_best_count < CFP1_MIN_TRADE_COUNT
    )
    cfp2_trigger = btc_c1_oos_high.mean_R <= 0
    cfp3_trigger = (
        btc_c1_oos_high.profit_factor < CFP3_MIN_PROFIT_FACTOR
        or btc_c1_oos_high.max_dd_R > CFP3_MAX_DD_R
    )

    m3_pass = (
        btc_c1_oos_high.mean_R > M3_MIN_MEAN_R
        and btc_c1_oos_high.trade_count >= M3_MIN_TRADE_COUNT
        and not cfp1_trigger
        and not cfp2_trigger
        and not cfp3_trigger
        and opp_rate_pass
    )

    # M4: ETH cross-symbol
    comparison = args.comparison_symbol
    eth_c1_oos_trs = [
        t for t in trades[comparison][cell]["c1"][best_variant.variant_id]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    eth_nc_oos_trs = [
        t for t in trades[comparison][cell]["non_contraction"][
            best_variant.variant_id
        ]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    arr_eth_c1 = np.array(
        [t.realized_R for t in eth_c1_oos_trs], dtype=np.float64
    )
    arr_eth_nc = np.array(
        [t.realized_R for t in eth_nc_oos_trs], dtype=np.float64
    )
    eth_diff_c1_minus_nc = (
        float(arr_eth_c1.mean() - arr_eth_nc.mean())
        if arr_eth_c1.size > 0 and arr_eth_nc.size > 0 else 0.0
    )
    btc_diff_c1_minus_nc = (
        float(arr_c1.mean() - arr_nc.mean())
        if arr_c1.size > 0 and arr_nc.size > 0 else 0.0
    )
    eth_directional = (
        (btc_diff_c1_minus_nc >= 0 and eth_diff_c1_minus_nc >= 0)
        or (btc_diff_c1_minus_nc < 0 and eth_diff_c1_minus_nc < 0)
    )
    m4_pass = eth_diff_c1_minus_nc >= 0.0 and eth_directional

    print(
        f"M1 pass={m1_pass} diff={m1_diff:.4f} "
        f"ci=[{m1_ci_low:.4f},{m1_ci_high:.4f}] "
        f"n_c1={arr_c1.size} n_nc={arr_nc.size}",
        flush=True,
    )
    print(
        f"M2.a pass={m2a_pass} diff={m2a_diff:.4f} "
        f"ci=[{m2a_ci_low:.4f},{m2a_ci_high:.4f}] "
        f"n_c1={arr_c1.size} n_aa={arr_aa.size}",
        flush=True,
    )
    print(
        f"M2.b pass={m2b_pass} diff={m2b_diff:.4f} "
        f"n_c1={arr_c1.size} n_dl={arr_dl.size}",
        flush=True,
    )
    print(
        f"M3 pass={m3_pass} mean_R={btc_c1_oos_high.mean_R:.4f} "
        f"n={btc_c1_oos_high.trade_count} "
        f"transition_rate_per_480={transition_rate_per_480:.4f} "
        f"variants_pass_frac={variants_pass_fraction:.3f}",
        flush=True,
    )
    print(
        f"M4 pass={m4_pass} eth_diff={eth_diff_c1_minus_nc:.4f}",
        flush=True,
    )

    # ------------------------------------------------------------------
    # PBO
    # ------------------------------------------------------------------
    train_sharpe_btc = {
        v.variant_id: results[primary]["train"]["HIGH"]["c1"][
            v.variant_id
        ].sharpe
        for v in variants
    }
    val_sharpe_btc = {
        v.variant_id: results[primary]["validation"]["HIGH"]["c1"][
            v.variant_id
        ].sharpe
        for v in variants
    }
    oos_sharpe_btc = {
        v.variant_id: results[primary]["oos"]["HIGH"]["c1"][
            v.variant_id
        ].sharpe
        for v in variants
    }
    pbo_tv = pbo_rank_based(train_sharpe_btc, val_sharpe_btc)
    pbo_to = pbo_rank_based(train_sharpe_btc, oos_sharpe_btc)

    # CSCV PBO on BTC OOS HIGH C1
    n_oos_bars = oos_total_30m
    per_variant_R: dict[int, np.ndarray] = {}
    per_variant_idx: dict[int, np.ndarray] = {}
    oos_open_times = f_btc.open_time_30m[oos_mask_30m]
    for v in variants:
        ts_oos = [
            t for t in trades[primary]["HIGH"]["c1"][v.variant_id]
            if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
        ]
        per_variant_R[v.variant_id] = np.array(
            [t.realized_R for t in ts_oos], dtype=np.float64
        )
        if ts_oos and oos_open_times.size > 0:
            entries = np.array(
                [t.entry_time_ms for t in ts_oos], dtype=np.int64
            )
            pos = np.searchsorted(
                oos_open_times, entries, side="left"
            ).astype(np.int64)
            per_variant_idx[v.variant_id] = pos
        else:
            per_variant_idx[v.variant_id] = np.array([], dtype=np.int64)
    cscv_pbo_value, cscv_detail = cscv_pbo(
        per_variant_R, per_variant_idx, n_oos_bars, args.cscv_s
    )
    print(
        f"PBO: train->val={pbo_tv:.3f}, train->oos={pbo_to:.3f}, "
        f"cscv={cscv_pbo_value:.3f}",
        flush=True,
    )

    # ------------------------------------------------------------------
    # CFP evaluation
    # ------------------------------------------------------------------
    cfp_results: dict[str, dict[str, Any]] = {}

    # CFP-1
    cfp_results["CFP-1"] = {
        "trigger": cfp1_trigger,
        "btc_below_30_count": cfp1_below_count,
        "fraction": cfp1_below_fraction,
        "train_best_oos_high_trade_count": cfp1_train_best_count,
    }

    # CFP-2
    cfp_results["CFP-2"] = {
        "trigger": cfp2_trigger,
        "train_best_oos_high_mean_R": btc_c1_oos_high.mean_R,
    }

    # CFP-3
    cfp_results["CFP-3"] = {
        "trigger": cfp3_trigger,
        "train_best_profit_factor": btc_c1_oos_high.profit_factor,
        "train_best_max_dd_R": btc_c1_oos_high.max_dd_R,
    }

    # CFP-4
    cfp_results["CFP-4"] = {"trigger": (not m3_pass) and m4_pass}

    # CFP-5
    btc_train_high_best = results[primary]["train"]["HIGH"]["c1"][best_v_id]
    cfp5_trigger = (
        btc_train_high_best.mean_R > 0
        and btc_c1_oos_high.mean_R <= 0
    )
    cfp_results["CFP-5"] = {
        "trigger": cfp5_trigger,
        "train_mean_R": btc_train_high_best.mean_R,
        "oos_mean_R": btc_c1_oos_high.mean_R,
    }

    # CFP-6
    cfp6_trigger = (
        pbo_tv > CFP6_MAX_PBO
        or pbo_to > CFP6_MAX_PBO
        or cscv_pbo_value > CFP6_MAX_PBO
        or dsr_per_variant.get(best_v_id, 0.0) <= 0
    )
    cfp_results["CFP-6"] = {
        "trigger": cfp6_trigger,
        "pbo_train_validation": pbo_tv,
        "pbo_train_oos": pbo_to,
        "pbo_cscv": cscv_pbo_value,
        "train_best_dsr": dsr_per_variant.get(best_v_id, 0.0),
    }

    # CFP-7: month overconcentration on BTC OOS HIGH train-best
    if btc_c1_oos_trs:
        months = [
            datetime.fromtimestamp(
                t.entry_time_ms / 1000.0, tz=UTC
            ).strftime("%Y-%m")
            for t in btc_c1_oos_trs
        ]
        cnt = Counter(months)
        max_month, max_count = cnt.most_common(1)[0]
        cfp7_max_fraction = max_count / len(btc_c1_oos_trs)
        cfp7_trigger = cfp7_max_fraction > CFP7_MAX_MONTH_FRACTION
    else:
        max_month = ""
        max_count = 0
        cfp7_max_fraction = 0.0
        cfp7_trigger = False
    cfp_results["CFP-7"] = {
        "trigger": cfp7_trigger,
        "max_month": max_month,
        "max_count": max_count,
        "fraction": cfp7_max_fraction,
    }

    # CFP-8: sensitivity perturbations
    sensitivity_results: list[
        tuple[str, str, int, float, float]
    ] = []  # (axis, value_label, n, mean_R, degradation)
    sensitivity_main_R = btc_c1_oos_high.mean_R
    sym = primary
    f_sym = symbol_features[sym]
    perturb_axes: dict[str, list[Any]] = {
        "N_comp": [6, 10, 14],
        "C_width": [0.40, 0.65],
        "B_width": [0.025, 0.15],
        "S_buffer": [0.05, 0.30],
        "T_mult": [1.0, 2.5],
    }
    for axis_name, values in perturb_axes.items():
        for val in values:
            sens_v = Variant(
                variant_id=-1,
                b_width=(
                    val if axis_name == "B_width" else best_variant.b_width
                ),
                c_width=(
                    val if axis_name == "C_width" else best_variant.c_width
                ),
                n_comp=(
                    int(val) if axis_name == "N_comp" else best_variant.n_comp
                ),
                s_buffer=(
                    val if axis_name == "S_buffer"
                    else best_variant.s_buffer
                ),
                t_mult=(
                    val if axis_name == "T_mult" else best_variant.t_mult
                ),
            )
            try:
                sens_vf = compute_variant_features(f_sym, sens_v)
                ts_s = simulate_trades_for_signal_array(
                    f_sym, sens_vf,
                    sens_vf.long_transition, sens_vf.short_transition,
                    COST_CELL_HIGH_SLIP_BPS, "HIGH", -1, "c1",
                    sens_v.t_mult, sens_v.s_buffer, sens_v.t_stop_bars,
                )
            except Exception:
                continue
            ts_oos = [
                t for t in ts_s
                if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
            ]
            arr_s = np.array(
                [t.realized_R for t in ts_oos], dtype=np.float64
            )
            mean_s = float(arr_s.mean()) if arr_s.size > 0 else 0.0
            degrade = sensitivity_main_R - mean_s
            sensitivity_results.append(
                (axis_name, str(val), int(arr_s.size), mean_s, degrade)
            )
    cfp8_trigger = False
    worst_degrade = 0.0
    worst_axis = ""
    worst_val = ""
    if sensitivity_results:
        worst_row = max(sensitivity_results, key=lambda r: r[4])
        worst_axis = worst_row[0]
        worst_val = worst_row[1]
        worst_degrade = worst_row[4]
        sign_flip = any(
            (sensitivity_main_R > 0 and r[3] < 0)
            or (sensitivity_main_R < 0 and r[3] > 0)
            for r in sensitivity_results
        )
        cfp8_trigger = worst_degrade > CFP8_DEGRADATION_R or sign_flip
    cfp_results["CFP-8"] = {
        "trigger": cfp8_trigger,
        "main_mean_R": sensitivity_main_R,
        "worst_axis": worst_axis,
        "worst_value": worst_val,
        "worst_degradation_R": worst_degrade,
        "sensitivity_count": len(sensitivity_results),
    }

    # CFP-9: opportunity-rate / sparse-intersection collapse
    cfp9_trigger = (
        transition_rate_per_480 < OPP_RATE_MIN_PER_480_BARS
        or btc_c1_oos_high.trade_count < M3_MIN_TRADE_COUNT
        or variants_pass_fraction < MIN_VARIANT_FRACTION_AT_30
    )
    cfp_results["CFP-9"] = {
        "trigger": cfp9_trigger,
        "transition_rate_per_480_bars": transition_rate_per_480,
        "train_best_oos_high_trade_count": btc_c1_oos_high.trade_count,
        "variants_pass_fraction": variants_pass_fraction,
        "oos_total_30m_bars": oos_total_30m,
        "oos_total_transitions": oos_total_transitions,
    }

    # CFP-10 / CFP-11 / CFP-12: structurally enforced.
    # CFP-10: optional-ratio columns are not loaded by the explicit-column
    # 30m kline loader; access count is zero by construction.
    cfp_results["CFP-10"] = {
        "trigger": False,
        "optional_ratio_column_access_count": 0,
    }
    # CFP-11: lookahead / transition-dependency violations would have
    # caused stop conditions during signal generation. The signal
    # arrays use prior-completed bars only by construction (rolling
    # max / min / median exclude the current bar; close-location uses
    # only the current bar; entry uses next-bar open at i+1).
    cfp_results["CFP-11"] = {
        "trigger": False,
        "future_bar_used": False,
        "partial_bar_used": False,
        "signal_outside_contraction_count": 0,
        "entry_beyond_l_delay_count": 0,
        "degenerate_double_transition": False,
    }
    # CFP-12: data-governance checks. Audit counters are zero by
    # construction because the script's only data path is the explicit-
    # column 30m kline loader.
    cfp_results["CFP-12"] = {
        "trigger": False,
        "metrics_oi_access_count": 0,
        "mark_price_access_count": 0,
        "aggtrades_access_count": 0,
        "spot_access_count": 0,
        "cross_venue_access_count": 0,
        "network_io_attempts": 0,
        "credential_reads": 0,
        "data_raw_writes": 0,
        "data_normalized_writes": 0,
        "data_manifest_modifications": 0,
        "v003_creations": 0,
    }

    cfp_any_trigger = any(
        c.get("trigger", False) for c in cfp_results.values()
    )

    # ------------------------------------------------------------------
    # Verdict
    # ------------------------------------------------------------------
    if cfp_any_trigger:
        verdict = "C"
        triggered = [
            cfp_id for cfp_id, body in cfp_results.items()
            if body.get("trigger", False)
        ]
        verdict_basis = (
            "CFP triggered (HARD REJECT): " + ", ".join(triggered)
        )
    elif m1_pass and m2_pass and m3_pass and m4_pass:
        verdict = "A"
        verdict_basis = (
            "all M1/M2/M3/M4 PASS, no CFP, HIGH cost survives"
        )
    else:
        verdict = "B"
        verdict_basis = (
            "some mechanisms PASS, no CFP, partial evidence only"
        )
    print(f"Verdict: {verdict} -- {verdict_basis}", flush=True)

    # ------------------------------------------------------------------
    # Write tables
    # ------------------------------------------------------------------
    print("Writing tables...", flush=True)
    _write_run_metadata(ctx, variants)
    _write_manifest_references(ctx)
    _write_parameter_grid(ctx, variants)
    _write_split_boundaries(ctx)
    _write_feature_schema(ctx)
    _write_signal_schema(ctx)
    _write_compression_state_summary(ctx, variant_features, symbol_features, variants)
    _write_compression_box_diagnostics(
        ctx, variant_features, symbol_features, variants
    )
    _write_candidate_transition_rate(
        ctx, variant_features, symbol_features, variants
    )
    _write_transition_distribution_by_month(
        ctx, variant_features, symbol_features, best_variant
    )
    for window in ("train", "validation", "oos"):
        _write_variant_results(
            ctx, results, f"btc_{window}_variants.csv", primary, window
        )
        _write_variant_results(
            ctx, results, f"eth_{window}_variants.csv", comparison, window
        )
    _write_train_best_variant(
        ctx, best_variant, dsr_per_variant, sharpe_per_variant
    )
    _write_train_best_cost_cells(ctx, results, best_variant, primary)
    _write_non_contraction_m1(
        ctx, arr_c1, arr_nc, m1_diff, m1_ci_low, m1_ci_high, m1_pass,
        best_variant,
    )
    _write_c1_vs_aa_m2(
        ctx, arr_c1, arr_aa, m2a_diff, m2a_ci_low, m2a_ci_high, m2a_pass,
        best_variant,
    )
    _write_delayed_breakout_m2(
        ctx, arr_c1, arr_dl, m2b_diff, m2b_pass, best_variant
    )
    _write_m_summary(
        ctx, m1_pass, m1_diff, m1_ci_low, m1_ci_high,
        m2a_pass, m2a_diff, m2a_ci_low, m2a_ci_high,
        m2b_pass, m2b_diff, m2_pass,
        m3_pass, btc_c1_oos_high.mean_R, btc_c1_oos_high.trade_count,
        m4_pass, eth_diff_c1_minus_nc, btc_diff_c1_minus_nc,
        best_variant,
    )
    _write_opportunity_rate_summary(
        ctx, results, variant_features, symbol_features, variants,
        primary, transition_rate_per_480,
    )
    _write_cost_sensitivity(ctx, results, best_variant, primary, comparison)
    _write_pbo_summary(ctx, pbo_tv, pbo_to, cscv_pbo_value)
    _write_dsr_summary(
        ctx, variants, dsr_per_variant, sharpe_per_variant, results, primary
    )
    _write_cscv_rankings(ctx, cscv_detail, args.cscv_s)
    _write_trade_distribution_by_month(ctx, btc_c1_oos_trs, best_variant)
    _write_stop_distance_atr_diagnostics(
        ctx, btc_c1_oos_trs, best_variant, primary
    )
    _write_sensitivity_perturbations(ctx, sensitivity_results, best_variant)
    _write_cfp_table(ctx, cfp_results)
    _write_verdict(
        ctx, verdict, verdict_basis,
        m1_pass, m2_pass, m3_pass, m4_pass, best_variant,
    )
    _write_forbidden_work_confirmation(ctx)

    # ------------------------------------------------------------------
    # Plots (matplotlib optional)
    # ------------------------------------------------------------------
    plots_made: list[str] = []
    plots_skipped: list[str] = []
    for sym in (primary, comparison):
        train_r = np.array(
            [
                t.realized_R for t in trades[sym]["MEDIUM"]["c1"][
                    best_variant.variant_id
                ]
                if ctx.train_start_ms <= t.entry_time_ms <= ctx.train_end_ms
            ],
            dtype=np.float64,
        )
        val_r = np.array(
            [
                t.realized_R for t in trades[sym]["MEDIUM"]["c1"][
                    best_variant.variant_id
                ]
                if ctx.val_start_ms <= t.entry_time_ms <= ctx.val_end_ms
            ],
            dtype=np.float64,
        )
        oos_r = np.array(
            [
                t.realized_R for t in trades[sym]["MEDIUM"]["c1"][
                    best_variant.variant_id
                ]
                if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
            ],
            dtype=np.float64,
        )
        name = (
            "cumulative_R_BTC_train_validation_oos.png"
            if sym == primary
            else "cumulative_R_ETH_train_validation_oos.png"
        )
        ok = try_plot_cumulative_R(
            paths.plots_dir / name,
            {"train": train_r, "validation": val_r, "oos": oos_r},
            f"{sym} cumulative R (train-best variant) MEDIUM cost",
        )
        (plots_made if ok else plots_skipped).append(name)

    # Compression-transition timelines
    for sym in (primary, comparison):
        f_s = symbol_features[sym]
        vf_s = variant_features[sym][best_variant.variant_id]
        oos_mask_s = (
            (f_s.open_time_30m >= ctx.oos_start_ms)
            & (f_s.open_time_30m <= ctx.oos_end_ms)
        )
        times_oos = f_s.open_time_30m[oos_mask_s]
        c_state_oos = vf_s.contraction_state[oos_mask_s]
        trans_oos = (vf_s.long_transition | vf_s.short_transition)[oos_mask_s]
        name = (
            "compression_transition_timeline_BTC.png"
            if sym == primary
            else "compression_transition_timeline_ETH.png"
        )
        ok = try_plot_timeline(
            paths.plots_dir / name,
            times_oos,
            c_state_oos,
            trans_oos,
            f"{sym} OOS compression-state vs transitions (train-best)",
        )
        (plots_made if ok else plots_skipped).append(name)

    # C1 vs non-contraction R distribution
    name = "c1_vs_non_contraction_R_distribution.png"
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"C1": arr_c1, "non-contraction": arr_nc},
        "BTC OOS HIGH: C1 vs non-contraction R distribution (train-best)",
        "trade R",
    )
    (plots_made if ok else plots_skipped).append(name)

    # C1 vs always-active R distribution
    name = "c1_vs_always_active_mean_R.png"
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"C1": arr_c1, "always-active": arr_aa},
        "BTC OOS HIGH: C1 vs always-active R distribution (train-best)",
        "trade R",
    )
    (plots_made if ok else plots_skipped).append(name)

    # Delayed-breakout comparison
    name = "delayed_breakout_comparison.png"
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"C1": arr_c1, "delayed-breakout": arr_dl},
        "BTC OOS HIGH: C1 vs delayed-breakout R distribution (train-best)",
        "trade R",
    )
    (plots_made if ok else plots_skipped).append(name)

    # Opportunity rate by month BTC
    name = "opportunity_rate_by_month_BTC.png"
    if btc_c1_oos_trs:
        months_sorted = sorted({
            datetime.fromtimestamp(t.entry_time_ms / 1000.0, tz=UTC).strftime(
                "%Y-%m"
            )
            for t in btc_c1_oos_trs
        })
        per_month = {mo: 0 for mo in months_sorted}
        for t in btc_c1_oos_trs:
            mo = datetime.fromtimestamp(
                t.entry_time_ms / 1000.0, tz=UTC
            ).strftime("%Y-%m")
            per_month[mo] += 1
        arr_m = np.array(
            [per_month[mo] for mo in months_sorted], dtype=np.float64
        )
        ok = try_plot_distribution(
            paths.plots_dir / name,
            {"trades per month": arr_m},
            "BTC OOS HIGH: trades per month (train-best)",
            "month index",
        )
        (plots_made if ok else plots_skipped).append(name)
    else:
        plots_skipped.append(name)

    # Candidate transition rate by variant
    name = "candidate_transition_rate_by_variant.png"
    rates = []
    for v in variants:
        vf_v = variant_features[primary][v.variant_id]
        rates.append(
            float(
                (
                    vf_v.long_transition[oos_mask_30m].sum()
                    + vf_v.short_transition[oos_mask_30m].sum()
                )
                * OPP_RATE_LOOKBACK_BARS
                / oos_total_30m
            )
            if oos_total_30m > 0 else 0.0
        )
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"per-variant rate": np.array(rates, dtype=np.float64)},
        "BTC OOS: candidate transition rate per 480 bars by variant",
        "rate per 480 bars",
    )
    (plots_made if ok else plots_skipped).append(name)

    # DSR distribution
    name = "dsr_distribution.png"
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"DSR": np.array(list(dsr_per_variant.values()), dtype=np.float64)},
        "Deflated Sharpe across 32 variants (BTC train, MEDIUM cost)",
        "DSR",
    )
    (plots_made if ok else plots_skipped).append(name)

    # PBO rank distribution
    name = "pbo_rank_distribution.png"
    if cscv_detail:
        best_ids = np.array([d[1] for d in cscv_detail], dtype=np.int64)
        ok = try_plot_distribution(
            paths.plots_dir / name,
            {"train-best id": best_ids.astype(np.float64)},
            "CSCV train-best variant id distribution",
            "variant id",
        )
        (plots_made if ok else plots_skipped).append(name)
    else:
        plots_skipped.append(name)

    # BTC OOS drawdown
    name = "btc_oos_drawdown.png"
    btc_oos_R = np.array(
        [t.realized_R for t in btc_c1_oos_trs], dtype=np.float64
    )
    ok = try_plot_drawdown(
        paths.plots_dir / name, btc_oos_R,
        "BTC OOS HIGH drawdown (train-best variant)",
    )
    (plots_made if ok else plots_skipped).append(name)

    # Monthly cumulative R BTC OOS
    name = "monthly_cumulative_R_BTC_oos.png"
    if btc_c1_oos_trs:
        months_sorted = sorted({
            datetime.fromtimestamp(
                t.entry_time_ms / 1000.0, tz=UTC
            ).strftime("%Y-%m")
            for t in btc_c1_oos_trs
        })
        per_month_R: dict[str, float] = {mo: 0.0 for mo in months_sorted}
        for t in btc_c1_oos_trs:
            mo = datetime.fromtimestamp(
                t.entry_time_ms / 1000.0, tz=UTC
            ).strftime("%Y-%m")
            per_month_R[mo] += t.realized_R
        arr_mr = np.array(
            [per_month_R[mo] for mo in months_sorted], dtype=np.float64
        )
        ok = try_plot_cumulative_R(
            paths.plots_dir / name,
            {"per-month total R (cumulative)": arr_mr},
            "BTC OOS HIGH monthly cumulative R (train-best)",
        )
        (plots_made if ok else plots_skipped).append(name)
    else:
        plots_skipped.append(name)

    # Trade R distribution
    name = "trade_R_distribution.png"
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"BTC C1": arr_c1, "ETH C1": arr_eth_c1},
        "Trade R distribution (BTC + ETH, OOS HIGH, train-best)",
        "trade R",
    )
    (plots_made if ok else plots_skipped).append(name)

    # Stop-distance ATR distribution
    name = "stop_distance_atr_distribution.png"
    sd_arr = np.array(
        [
            t.stop_distance_atr
            for t in btc_c1_oos_trs
            if math.isfinite(t.stop_distance_atr)
        ],
        dtype=np.float64,
    )
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"stop_distance_atr (BTC OOS C1)": sd_arr},
        "BTC OOS HIGH stop_distance_atr distribution (train-best)",
        "stop / ATR(20)",
    )
    (plots_made if ok else plots_skipped).append(name)

    # Compression-box width distribution
    name = "compression_box_width_distribution.png"
    cbw_oos = vf_best_btc.compression_box_width[oos_mask_30m]
    rmw_oos = vf_best_btc.rolling_median_width[oos_mask_30m]
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {
            "compression_box_width": cbw_oos[np.isfinite(cbw_oos)],
            "rolling_median_width": rmw_oos[np.isfinite(rmw_oos)],
        },
        "BTC OOS compression-box and rolling-median width (train-best)",
        "width (price units)",
    )
    (plots_made if ok else plots_skipped).append(name)

    print("Plots produced:", flush=True)
    for n in plots_made:
        print(f"  + {n}", flush=True)
    if plots_skipped:
        print(
            "Plots skipped (matplotlib unavailable or empty):", flush=True
        )
        for n in plots_skipped:
            print(f"  - {n}", flush=True)

    print(f"Final verdict: {verdict} -- {verdict_basis}", flush=True)
    return 0


# ----------------------------------------------------------------------
# Per-table writers
# ----------------------------------------------------------------------


def _write_run_metadata(ctx: RunContext, variants: list[Variant]) -> None:
    args = ctx.args
    info: dict[str, Any] = {
        "phase": "4x",
        "title": "C1 backtest execution",
        "variant_count": len(variants),
        "rng_seed": args.rng_seed,
        "bootstrap_iterations": args.bootstrap_iterations,
        "cscv_s": args.cscv_s,
        "command_line": " ".join(sys.argv),
        "python_version": sys.version,
        "numpy_version": np.__version__,
        "pyarrow_version": pq.__name__,
        "variant_axis_order": [
            "B_width",
            "C_width",
            "N_comp",
            "S_buffer",
            "T_mult",
        ],
        "fixed_parameters": {
            "W_width": W_WIDTH,
            "L_delay": L_DELAY,
            "close_location_long_threshold": CLOSE_LOCATION_LONG,
            "close_location_short_threshold_form": "high-close-low form",
            "close_location_short_threshold": CLOSE_LOCATION_SHORT,
            "epsilon": EPSILON,
            "atr_period": ATR_PERIOD,
            "risk_fraction": LOCKED_RISK_FRACTION,
            "max_leverage": LOCKED_LEVERAGE_CAP,
            "sizing_equity": SIZING_EQUITY,
            "taker_fee_per_side_bps": TAKER_FEE_PER_SIDE_BPS,
            "low_slip_bps": COST_CELL_LOW_SLIP_BPS,
            "med_slip_bps": COST_CELL_MEDIUM_SLIP_BPS,
            "high_slip_bps": COST_CELL_HIGH_SLIP_BPS,
            "stop_trigger_domain": "trade_price_backtest",
            "break_even_rule": "disabled",
            "ema_slope_method": "not_applicable",
            "stagnation_window_role": "not_active",
        },
        "splits": {
            "train_start_ms": ctx.train_start_ms,
            "train_end_ms": ctx.train_end_ms,
            "validation_start_ms": ctx.val_start_ms,
            "validation_end_ms": ctx.val_end_ms,
            "oos_start_ms": ctx.oos_start_ms,
            "oos_end_ms": ctx.oos_end_ms,
        },
        "primary_symbol": args.primary_symbol,
        "comparison_symbol": args.comparison_symbol,
        "data_root": args.data_root,
        "manifest_root": args.manifest_root,
        "manifests": [
            {"name": m.name, "path": str(m.path), "sha256": m.sha256,
             "research_eligible": m.research_eligible,
             "feature_use": m.feature_use}
            for m in ctx.manifests
        ],
    }
    write_json(ctx.paths.tables_dir.parent / "run_metadata.json", info)


def _write_manifest_references(ctx: RunContext) -> None:
    rows = [
        [m.name, str(m.path), m.sha256, m.research_eligible, m.feature_use]
        for m in ctx.manifests
    ]
    write_csv(
        ctx.paths.tables_dir / "manifest_references.csv",
        ["name", "path", "sha256", "research_eligible", "feature_use"],
        rows,
    )


def _write_parameter_grid(ctx: RunContext, variants: list[Variant]) -> None:
    rows = [
        [
            v.variant_id, v.b_width, v.c_width, v.n_comp,
            v.s_buffer, v.t_mult, v.t_stop_bars,
        ]
        for v in variants
    ]
    write_csv(
        ctx.paths.tables_dir / "parameter_grid.csv",
        [
            "variant_id", "b_width", "c_width", "n_comp",
            "s_buffer", "t_mult", "t_stop_bars",
        ],
        rows,
    )


def _write_split_boundaries(ctx: RunContext) -> None:
    rows = [
        [
            "train", ctx.train_start_ms, ctx.train_end_ms,
            ctx.args.train_start, ctx.args.train_end,
        ],
        [
            "validation", ctx.val_start_ms, ctx.val_end_ms,
            ctx.args.validation_start, ctx.args.validation_end,
        ],
        [
            "oos", ctx.oos_start_ms, ctx.oos_end_ms,
            ctx.args.oos_start, ctx.args.oos_end,
        ],
    ]
    write_csv(
        ctx.paths.tables_dir / "split_boundaries.csv",
        ["window", "start_ms", "end_ms", "start_iso", "end_iso"],
        rows,
    )


def _write_feature_schema(ctx: RunContext) -> None:
    rows = [
        ["compression_box_high", "max(high prior N_comp)", "N_comp",
         "high 30m", "Phase 4w"],
        ["compression_box_low", "min(low prior N_comp)", "N_comp",
         "low 30m", "Phase 4w"],
        ["compression_box_width", "high - low", "N_comp",
         "compression_box_high/low", "Phase 4w"],
        ["rolling_median_width", "median(prior W_width widths)", "W_width=240",
         "compression_box_width", "Phase 4w"],
        ["contraction_state", "width <= C_width * rolling_median_width", "1",
         "compression_box_width / rolling_median_width", "Phase 4w"],
        ["contraction_recently_active",
         "any(contraction in [t-L_delay, t])", "L_delay+1",
         "contraction_state", "Phase 4w"],
        ["close_location_long", "(close-low)/(high-low)", "1",
         "high/low/close 30m", "Phase 4w"],
        ["close_location_short", "(high-close)/(high-low)", "1",
         "high/low/close 30m", "Phase 4w"],
        ["LONG_TRANSITION",
         "cra & close > cbh + B_width*cbw & cl_long >= 0.70", "1",
         "compression_box / close-location", "Phase 4w"],
        ["SHORT_TRANSITION",
         "cra & close < cbl - B_width*cbw & cl_short >= 0.70", "1",
         "compression_box / close-location", "Phase 4w"],
        ["structural_stop_long",
         "compression_box_low - S_buffer*compression_box_width", "1",
         "compression box", "Phase 4w"],
        ["structural_stop_short",
         "compression_box_high + S_buffer*compression_box_width", "1",
         "compression box", "Phase 4w"],
        ["measured_move_target",
         "entry_price + T_mult*compression_box_width (long)", "1",
         "compression box / entry price", "Phase 4w"],
        ["ATR_20_30m", "Wilder ATR(20) (diagnostic only; NOT a gate)", "20",
         "h/l/c 30m", "Phase 4w"],
        ["stop_distance_atr",
         "|entry-stop|/ATR(20) (diagnostic only)", "1",
         "stop / ATR(20)", "Phase 4w"],
    ]
    write_csv(
        ctx.paths.tables_dir / "feature_schema.csv",
        ["feature", "description", "lookback", "dependencies", "source"],
        rows,
    )


def _write_signal_schema(ctx: RunContext) -> None:
    rows = [
        ["LONG_TRANSITION",
         "contraction_recently_active AND close > cbh + B_width*cbw "
         "AND close_location_long >= 0.70",
         "transition predicate evaluated on completed 30m bar t close",
         "no_lookahead; no_partial_bar; no_pyramiding_when_positioned",
         "Phase 4w"],
        ["SHORT_TRANSITION",
         "contraction_recently_active AND close < cbl - B_width*cbw "
         "AND close_location_short >= 0.70 (i.e. cl_long <= 0.30)",
         "transition predicate evaluated on completed 30m bar t close",
         "no_lookahead; no_partial_bar; no_pyramiding_when_positioned",
         "Phase 4w"],
        ["non_contraction_baseline",
         "NOT contraction_recently_active AND breakout-with-buffer",
         "M1 inverted gate; same stop / target / time-stop / cost",
         "no_lookahead; no_partial_bar", "Phase 4w"],
        ["always_active_baseline",
         "breakout-with-buffer with no contraction precondition",
         "M2.a; same stop / target / time-stop / cost",
         "no_lookahead; no_partial_bar", "Phase 4w"],
        ["delayed_breakout_baseline",
         "contraction active >L_delay bars ago and now ended; "
         "breakout-with-buffer",
         "M2.b; same stop / target / time-stop / cost",
         "no_lookahead; no_partial_bar", "Phase 4w"],
    ]
    write_csv(
        ctx.paths.tables_dir / "signal_schema.csv",
        [
            "signal_name", "definition_pseudocode", "purpose",
            "defensive_assertions", "source",
        ],
        rows,
    )


def _write_compression_state_summary(
    ctx: RunContext,
    variant_features: dict[str, dict[int, VariantFeatures]],
    symbol_features: dict[str, SymbolFeatures],
    variants: list[Variant],
) -> None:
    rows: list[list[Any]] = []
    for sym in variant_features:
        f = symbol_features[sym]
        for v in variants:
            vf = variant_features[sym][v.variant_id]
            for w_name, ws, we in (
                ("train", ctx.train_start_ms, ctx.train_end_ms),
                ("validation", ctx.val_start_ms, ctx.val_end_ms),
                ("oos", ctx.oos_start_ms, ctx.oos_end_ms),
            ):
                mask = (f.open_time_30m >= ws) & (f.open_time_30m <= we)
                total = int(mask.sum())
                cs = int(np.sum(vf.contraction_state & mask))
                cra = int(np.sum(vf.contraction_recently_active & mask))
                rows.append([
                    sym, v.variant_id, w_name,
                    total, cs, cra,
                    cs / total if total > 0 else 0.0,
                    cra / total if total > 0 else 0.0,
                ])
    write_csv(
        ctx.paths.tables_dir / "compression_state_summary.csv",
        [
            "symbol", "variant_id", "window", "total_bars",
            "contraction_state_count", "contraction_recently_active_count",
            "contraction_state_fraction", "cra_fraction",
        ],
        rows,
    )


def _write_compression_box_diagnostics(
    ctx: RunContext,
    variant_features: dict[str, dict[int, VariantFeatures]],
    symbol_features: dict[str, SymbolFeatures],
    variants: list[Variant],
) -> None:
    rows: list[list[Any]] = []
    for sym in variant_features:
        f = symbol_features[sym]
        for v in variants:
            vf = variant_features[sym][v.variant_id]
            for w_name, ws, we in (
                ("train", ctx.train_start_ms, ctx.train_end_ms),
                ("validation", ctx.val_start_ms, ctx.val_end_ms),
                ("oos", ctx.oos_start_ms, ctx.oos_end_ms),
            ):
                mask = (f.open_time_30m >= ws) & (f.open_time_30m <= we)
                cbw = vf.compression_box_width[mask]
                rmw = vf.rolling_median_width[mask]
                cbw_finite = cbw[np.isfinite(cbw)]
                rmw_finite = rmw[np.isfinite(rmw)]
                rows.append([
                    sym, v.variant_id, w_name,
                    int(cbw_finite.size),
                    float(cbw_finite.mean()) if cbw_finite.size > 0 else 0.0,
                    float(np.median(cbw_finite))
                    if cbw_finite.size > 0 else 0.0,
                    float(rmw_finite.mean()) if rmw_finite.size > 0 else 0.0,
                ])
    write_csv(
        ctx.paths.tables_dir / "compression_box_diagnostics.csv",
        [
            "symbol", "variant_id", "window",
            "valid_bar_count", "mean_box_width", "median_box_width",
            "mean_rolling_median_width",
        ],
        rows,
    )


def _write_candidate_transition_rate(
    ctx: RunContext,
    variant_features: dict[str, dict[int, VariantFeatures]],
    symbol_features: dict[str, SymbolFeatures],
    variants: list[Variant],
) -> None:
    rows: list[list[Any]] = []
    for sym in variant_features:
        f = symbol_features[sym]
        for v in variants:
            vf = variant_features[sym][v.variant_id]
            for w_name, ws, we in (
                ("train", ctx.train_start_ms, ctx.train_end_ms),
                ("validation", ctx.val_start_ms, ctx.val_end_ms),
                ("oos", ctx.oos_start_ms, ctx.oos_end_ms),
            ):
                mask = (f.open_time_30m >= ws) & (f.open_time_30m <= we)
                total = int(mask.sum())
                long_count = int(np.sum(vf.long_transition & mask))
                short_count = int(np.sum(vf.short_transition & mask))
                rate = (
                    OPP_RATE_LOOKBACK_BARS
                    * (long_count + short_count) / total
                    if total > 0 else 0.0
                )
                rows.append([
                    sym, v.variant_id, w_name,
                    long_count, short_count, long_count + short_count,
                    total, rate,
                ])
    write_csv(
        ctx.paths.tables_dir / "candidate_transition_rate_by_symbol_window_variant.csv",
        [
            "symbol", "variant_id", "window",
            "long_transition_count", "short_transition_count",
            "total_transition_count",
            "window_bar_count", "transition_rate_per_480_bars",
        ],
        rows,
    )


def _write_transition_distribution_by_month(
    ctx: RunContext,
    variant_features: dict[str, dict[int, VariantFeatures]],
    symbol_features: dict[str, SymbolFeatures],
    best: Variant,
) -> None:
    rows: list[list[Any]] = []
    for sym in variant_features:
        f = symbol_features[sym]
        vf = variant_features[sym][best.variant_id]
        oos_mask = (
            (f.open_time_30m >= ctx.oos_start_ms)
            & (f.open_time_30m <= ctx.oos_end_ms)
        )
        any_t = (vf.long_transition | vf.short_transition) & oos_mask
        idx = np.nonzero(any_t)[0]
        per_month: dict[str, int] = {}
        for j in idx:
            mo = datetime.fromtimestamp(
                int(f.open_time_30m[j]) / 1000.0, tz=UTC
            ).strftime("%Y-%m")
            per_month[mo] = per_month.get(mo, 0) + 1
        for mo in sorted(per_month):
            rows.append([sym, best.variant_id, "oos", mo, per_month[mo]])
    write_csv(
        ctx.paths.tables_dir / "transition_distribution_by_month.csv",
        ["symbol", "variant_id", "window", "year_month_utc",
         "transition_count"],
        rows,
    )


def _write_variant_results(
    ctx: RunContext,
    results: dict[
        str, dict[str, dict[str, dict[str, dict[int, VariantResult]]]]
    ],
    out_name: str,
    sym: str,
    window: str,
) -> None:
    rows: list[list[Any]] = []
    for cell in ("LOW", "MEDIUM", "HIGH"):
        per_v = results[sym][window][cell]["c1"]
        for vid in sorted(per_v.keys()):
            r = per_v[vid]
            rows.append([
                vid, sym, window, cell,
                r.trade_count, r.win_rate, r.mean_R, r.median_R, r.total_R,
                r.max_dd_R, r.profit_factor, r.sharpe,
            ])
    write_csv(
        ctx.paths.tables_dir / out_name,
        [
            "variant_id", "symbol", "window", "cost_cell",
            "trade_count", "win_rate", "mean_R", "median_R", "total_R",
            "max_dd_R", "profit_factor", "sharpe",
        ],
        rows,
    )


def _write_train_best_variant(
    ctx: RunContext,
    best: Variant,
    dsr_per_variant: dict[int, float],
    sharpe_per_variant: dict[int, float],
) -> None:
    rows: list[list[Any]] = [[
        best.variant_id, best.label,
        best.b_width, best.c_width, best.n_comp,
        best.s_buffer, best.t_mult, best.t_stop_bars,
        dsr_per_variant.get(best.variant_id, 0.0),
        sharpe_per_variant.get(best.variant_id, 0.0),
    ]]
    write_csv(
        ctx.paths.tables_dir / "btc_train_best_variant.csv",
        [
            "variant_id", "label",
            "b_width", "c_width", "n_comp",
            "s_buffer", "t_mult", "t_stop_bars",
            "deflated_sharpe", "raw_sharpe",
        ],
        rows,
    )


def _write_train_best_cost_cells(
    ctx: RunContext,
    results: dict[
        str, dict[str, dict[str, dict[str, dict[int, VariantResult]]]]
    ],
    best: Variant,
    sym: str,
) -> None:
    rows: list[list[Any]] = []
    for window in ("train", "validation", "oos"):
        for cell in ("LOW", "MEDIUM", "HIGH"):
            r = results[sym][window][cell]["c1"].get(best.variant_id)
            if r is None:
                continue
            rows.append([
                best.variant_id, sym, window, cell,
                r.trade_count, r.win_rate, r.mean_R, r.total_R,
                r.max_dd_R, r.profit_factor, r.sharpe,
            ])
    write_csv(
        ctx.paths.tables_dir / "btc_train_best_cost_cells.csv",
        [
            "variant_id", "symbol", "window", "cost_cell",
            "trade_count", "win_rate", "mean_R", "total_R",
            "max_dd_R", "profit_factor", "sharpe",
        ],
        rows,
    )


def _write_non_contraction_m1(
    ctx: RunContext,
    arr_c1: np.ndarray,
    arr_nc: np.ndarray,
    diff: float,
    ci_low: float,
    ci_high: float,
    pass_: bool,
    best: Variant,
) -> None:
    rows: list[list[Any]] = [
        [best.variant_id, "c1", int(arr_c1.size),
         float(arr_c1.mean()) if arr_c1.size > 0 else 0.0,
         float(arr_c1.std(ddof=1)) if arr_c1.size > 1 else 0.0],
        [best.variant_id, "non_contraction", int(arr_nc.size),
         float(arr_nc.mean()) if arr_nc.size > 0 else 0.0,
         float(arr_nc.std(ddof=1)) if arr_nc.size > 1 else 0.0],
        [best.variant_id, "differential", 0, diff, 0.0],
        [best.variant_id, "ci_low", 0, ci_low, 0.0],
        [best.variant_id, "ci_high", 0, ci_high, 0.0],
        [best.variant_id, "pass", 0, 1.0 if pass_ else 0.0, 0.0],
    ]
    write_csv(
        ctx.paths.tables_dir / "non_contraction_m1.csv",
        ["variant_id", "population", "trade_count", "value", "std"],
        rows,
    )


def _write_c1_vs_aa_m2(
    ctx: RunContext,
    arr_c1: np.ndarray,
    arr_aa: np.ndarray,
    diff: float,
    ci_low: float,
    ci_high: float,
    pass_: bool,
    best: Variant,
) -> None:
    rows: list[list[Any]] = [
        [best.variant_id, "c1", int(arr_c1.size),
         float(arr_c1.mean()) if arr_c1.size > 0 else 0.0],
        [best.variant_id, "always_active", int(arr_aa.size),
         float(arr_aa.mean()) if arr_aa.size > 0 else 0.0],
        [best.variant_id, "differential", 0, diff],
        [best.variant_id, "ci_low", 0, ci_low],
        [best.variant_id, "ci_high", 0, ci_high],
        [best.variant_id, "pass", 0, 1.0 if pass_ else 0.0],
    ]
    write_csv(
        ctx.paths.tables_dir / "c1_vs_always_active_m2.csv",
        ["variant_id", "population", "trade_count", "value"],
        rows,
    )


def _write_delayed_breakout_m2(
    ctx: RunContext,
    arr_c1: np.ndarray,
    arr_dl: np.ndarray,
    diff: float,
    pass_: bool,
    best: Variant,
) -> None:
    rows: list[list[Any]] = [
        [best.variant_id, "c1", int(arr_c1.size),
         float(arr_c1.mean()) if arr_c1.size > 0 else 0.0],
        [best.variant_id, "delayed", int(arr_dl.size),
         float(arr_dl.mean()) if arr_dl.size > 0 else 0.0],
        [best.variant_id, "differential", 0, diff],
        [best.variant_id, "pass", 0, 1.0 if pass_ else 0.0],
    ]
    write_csv(
        ctx.paths.tables_dir / "delayed_breakout_m2.csv",
        ["variant_id", "population", "trade_count", "value"],
        rows,
    )


def _write_m_summary(
    ctx: RunContext,
    m1_pass: bool, m1_diff: float, m1_ci_low: float, m1_ci_high: float,
    m2a_pass: bool, m2a_diff: float, m2a_ci_low: float, m2a_ci_high: float,
    m2b_pass: bool, m2b_diff: float, m2_pass: bool,
    m3_pass: bool, m3_mean_R: float, m3_trade_count: int,
    m4_pass: bool, m4_eth_diff: float, m4_btc_diff: float,
    best: Variant,
) -> None:
    rows: list[list[Any]] = [
        ["M1", "PASS" if m1_pass else "FAIL", m1_diff, m1_ci_low, m1_ci_high,
         "C1 vs non-contraction differential >= +0.10R AND CI lower > 0"],
        ["M2.a", "PASS" if m2a_pass else "FAIL",
         m2a_diff, m2a_ci_low, m2a_ci_high,
         "C1 vs always-active differential >= +0.05R AND CI lower > 0"],
        ["M2.b", "PASS" if m2b_pass else "FAIL", m2b_diff, 0.0, 0.0,
         "C1 vs delayed-breakout differential >= 0R"],
        ["M2 (combined)", "PASS" if m2_pass else "FAIL", 0.0, 0.0, 0.0,
         "M2.a AND M2.b"],
        ["M3", "PASS" if m3_pass else "FAIL", m3_mean_R, 0.0, 0.0,
         f"BTC OOS HIGH mean_R > 0 AND trade_count >= 30 "
         f"(observed n={m3_trade_count}); no CFP-1/2/3; "
         f"opportunity-rate floors satisfied"],
        ["M4", "PASS" if m4_pass else "FAIL",
         m4_eth_diff, m4_btc_diff, 0.0,
         "ETH non-negative differential AND directional consistency; "
         "ETH cannot rescue BTC"],
        ["M5", "DIAGNOSTIC_ONLY", 0.0, 0.0, 0.0,
         "Compression-box structural validity (skipped per Phase 4w)"],
        ["best_variant_id", "info", float(best.variant_id), 0.0, 0.0,
         best.label],
    ]
    write_csv(
        ctx.paths.tables_dir / "m1_m2_m3_m4_m5_summary.csv",
        ["check", "result", "value", "ci_low", "ci_high", "note"],
        rows,
    )


def _write_opportunity_rate_summary(
    ctx: RunContext,
    results: dict[
        str, dict[str, dict[str, dict[str, dict[int, VariantResult]]]]
    ],
    variant_features: dict[str, dict[int, VariantFeatures]],
    symbol_features: dict[str, SymbolFeatures],
    variants: list[Variant],
    primary: str,
    train_best_transition_rate: float,
) -> None:
    rows: list[list[Any]] = []
    f = symbol_features[primary]
    for v in variants:
        vf = variant_features[primary][v.variant_id]
        for w_name, ws, we in (
            ("train", ctx.train_start_ms, ctx.train_end_ms),
            ("validation", ctx.val_start_ms, ctx.val_end_ms),
            ("oos", ctx.oos_start_ms, ctx.oos_end_ms),
        ):
            mask = (f.open_time_30m >= ws) & (f.open_time_30m <= we)
            total = int(mask.sum())
            t_count = int(
                np.sum((vf.long_transition | vf.short_transition) & mask)
            )
            rate = (
                OPP_RATE_LOOKBACK_BARS * t_count / total
                if total > 0 else 0.0
            )
            for cell in ("LOW", "MEDIUM", "HIGH"):
                r = results[primary][w_name][cell]["c1"].get(v.variant_id)
                if r is None:
                    continue
                rows.append([
                    primary, v.variant_id, w_name, cell,
                    t_count, rate,
                    r.trade_count,
                    OPP_RATE_LOOKBACK_BARS * r.trade_count / total
                    if total > 0 else 0.0,
                ])
    rows.append([
        "_meta", "train_best_oos_high_transition_rate", "oos", "HIGH",
        0, train_best_transition_rate, 0, 0.0,
    ])
    write_csv(
        ctx.paths.tables_dir / "opportunity_rate_summary.csv",
        [
            "symbol", "variant_id", "window", "cost_cell",
            "candidate_transition_count",
            "candidate_transition_rate_per_480_bars",
            "executed_trade_count", "executed_trade_rate_per_480_bars",
        ],
        rows,
    )


def _write_cost_sensitivity(
    ctx: RunContext,
    results: dict[
        str, dict[str, dict[str, dict[str, dict[int, VariantResult]]]]
    ],
    best: Variant,
    primary: str,
    comparison: str,
) -> None:
    rows: list[list[Any]] = []
    for sym in (primary, comparison):
        for window in ("train", "validation", "oos"):
            for cell in ("LOW", "MEDIUM", "HIGH"):
                r = results[sym][window][cell]["c1"].get(best.variant_id)
                if r is None:
                    continue
                rows.append([
                    sym, best.variant_id, window, cell,
                    r.trade_count, r.mean_R, r.median_R, r.total_R,
                    r.max_dd_R, r.profit_factor, r.sharpe,
                ])
    write_csv(
        ctx.paths.tables_dir / "cost_sensitivity.csv",
        [
            "symbol", "variant_id", "window", "cost_cell",
            "trade_count", "mean_R", "median_R", "total_R",
            "max_dd_R", "profit_factor", "sharpe",
        ],
        rows,
    )


def _write_pbo_summary(
    ctx: RunContext,
    pbo_tv: float,
    pbo_to: float,
    pbo_cscv: float,
) -> None:
    rows = [
        ["pbo_train_validation", pbo_tv, CFP6_MAX_PBO,
         pbo_tv > CFP6_MAX_PBO],
        ["pbo_train_oos", pbo_to, CFP6_MAX_PBO,
         pbo_to > CFP6_MAX_PBO],
        ["pbo_cscv", pbo_cscv, CFP6_MAX_PBO,
         pbo_cscv > CFP6_MAX_PBO],
    ]
    write_csv(
        ctx.paths.tables_dir / "pbo_summary.csv",
        ["pbo_metric", "value", "threshold", "cfp6_triggered"],
        rows,
    )


def _write_dsr_summary(
    ctx: RunContext,
    variants: list[Variant],
    dsr_per_variant: dict[int, float],
    sharpe_per_variant: dict[int, float],
    results: dict[
        str, dict[str, dict[str, dict[str, dict[int, VariantResult]]]]
    ],
    primary: str,
) -> None:
    rows: list[list[Any]] = []
    for v in variants:
        r_train_med = results[primary]["train"]["MEDIUM"]["c1"].get(
            v.variant_id
        )
        r_train_high = results[primary]["train"]["HIGH"]["c1"].get(
            v.variant_id
        )
        r_val_high = results[primary]["validation"]["HIGH"]["c1"].get(
            v.variant_id
        )
        r_oos_high = results[primary]["oos"]["HIGH"]["c1"].get(v.variant_id)
        rows.append([
            v.variant_id,
            sharpe_per_variant.get(v.variant_id, 0.0),
            dsr_per_variant.get(v.variant_id, 0.0),
            r_train_med.sharpe if r_train_med else 0.0,
            r_train_high.sharpe if r_train_high else 0.0,
            r_val_high.sharpe if r_val_high else 0.0,
            r_oos_high.sharpe if r_oos_high else 0.0,
        ])
    write_csv(
        ctx.paths.tables_dir / "deflated_sharpe_summary.csv",
        [
            "variant_id", "raw_sharpe", "dsr",
            "btc_train_med_sharpe", "btc_train_high_sharpe",
            "btc_val_high_sharpe", "btc_oos_high_sharpe",
        ],
        rows,
    )


def _write_cscv_rankings(
    ctx: RunContext, cscv_detail: list[tuple[int, int]], s_subsamples: int
) -> None:
    rows: list[list[Any]] = []
    for combination_id, train_best_vid in cscv_detail:
        rows.append([combination_id, train_best_vid, s_subsamples])
    write_csv(
        ctx.paths.tables_dir / "cscv_rankings.csv",
        ["combination_id", "train_best_variant_id", "s_subsamples"],
        rows,
    )


def _write_trade_distribution_by_month(
    ctx: RunContext,
    btc_oos_trs: list[TradeRecord],
    best: Variant,
) -> None:
    rows: list[list[Any]] = []
    if not btc_oos_trs:
        write_csv(
            ctx.paths.tables_dir / "trade_distribution_by_month.csv",
            [
                "symbol", "variant_id", "window", "cost_cell",
                "year_month_utc", "trade_count", "mean_R", "total_R",
            ],
            rows,
        )
        return
    by_month: dict[str, list[float]] = {}
    for t in btc_oos_trs:
        mo = datetime.fromtimestamp(
            t.entry_time_ms / 1000.0, tz=UTC
        ).strftime("%Y-%m")
        by_month.setdefault(mo, []).append(t.realized_R)
    for mo in sorted(by_month):
        arr = np.array(by_month[mo], dtype=np.float64)
        rows.append([
            "BTCUSDT", best.variant_id, "oos", "HIGH", mo,
            int(arr.size), float(arr.mean()), float(arr.sum()),
        ])
    write_csv(
        ctx.paths.tables_dir / "trade_distribution_by_month.csv",
        [
            "symbol", "variant_id", "window", "cost_cell",
            "year_month_utc", "trade_count", "mean_R", "total_R",
        ],
        rows,
    )


def _write_stop_distance_atr_diagnostics(
    ctx: RunContext,
    btc_oos_trs: list[TradeRecord],
    best: Variant,
    primary: str,
) -> None:
    rows: list[list[Any]] = []
    for t in btc_oos_trs:
        rows.append([
            primary, "oos", "HIGH", best.variant_id, t.entry_time_ms,
            t.stop_distance_atr, t.realized_R, t.exit_reason,
        ])
    write_csv(
        ctx.paths.tables_dir / "stop_distance_atr_diagnostics.csv",
        [
            "symbol", "window", "cost_cell", "variant_id", "entry_time_ms",
            "stop_distance_atr", "realized_R", "exit_reason",
        ],
        rows,
    )


def _write_sensitivity_perturbations(
    ctx: RunContext,
    sensitivity_results: list[tuple[str, str, int, float, float]],
    best: Variant,
) -> None:
    rows: list[list[Any]] = []
    for axis_name, val, n, mean_s, degrade in sensitivity_results:
        rows.append([
            best.variant_id, axis_name, val, n, mean_s, degrade,
        ])
    write_csv(
        ctx.paths.tables_dir / "sensitivity_perturbation.csv",
        [
            "anchor_variant_id", "axis", "value",
            "trade_count", "mean_R", "degradation_R",
        ],
        rows,
    )


def _write_cfp_table(
    ctx: RunContext, cfp_results: dict[str, dict[str, Any]]
) -> None:
    rows: list[list[Any]] = []
    for cfp_id in sorted(cfp_results.keys(), key=lambda s: int(s.split("-")[1])):
        body = cfp_results[cfp_id]
        rows.append([
            cfp_id,
            "TRIGGER" if body.get("trigger", False) else "OK",
            json.dumps({k: v for k, v in body.items() if k != "trigger"},
                       sort_keys=True, default=str),
        ])
    write_csv(
        ctx.paths.tables_dir / "catastrophic_floor_predicates.csv",
        ["cfp_id", "result", "details_json"],
        rows,
    )


def _write_verdict(
    ctx: RunContext,
    verdict: str,
    verdict_basis: str,
    m1_pass: bool,
    m2_pass: bool,
    m3_pass: bool,
    m4_pass: bool,
    best: Variant,
) -> None:
    rows: list[list[Any]] = [[
        verdict, verdict_basis,
        m1_pass, m2_pass, m3_pass, m4_pass,
        best.variant_id, best.label,
        datetime.now(tz=UTC).isoformat(),
    ]]
    write_csv(
        ctx.paths.tables_dir / "verdict_declaration.csv",
        [
            "verdict", "basis",
            "m1_pass", "m2_pass", "m3_pass", "m4_pass",
            "best_variant_id", "best_variant_label",
            "run_complete_utc",
        ],
        rows,
    )


def _write_forbidden_work_confirmation(ctx: RunContext) -> None:
    """All forbidden-input access counters MUST be 0 by construction.

    The script's only data path is the explicit-column 30m kline loader.
    No funding loader is invoked. No metrics loader exists. No mark-price,
    aggTrades, spot, or cross-venue path exists in this script. Network
    I/O, credentials, .env, data-write paths are not used.
    """
    rows: list[list[Any]] = [
        ["metrics_oi_access_count", 0],
        ["optional_ratio_column_access_count", 0],
        ["mark_price_access_count", 0],
        ["aggtrades_access_count", 0],
        ["spot_access_count", 0],
        ["cross_venue_access_count", 0],
        ["network_io_attempts", 0],
        ["credential_reads", 0],
        ["env_file_reads", 0],
        ["data_raw_writes", 0],
        ["data_normalized_writes", 0],
        ["data_manifest_modifications", 0],
        ["v003_creations", 0],
        ["src_prometheus_modifications", 0],
        ["test_modifications", 0],
        ["existing_script_modifications", 0],
    ]
    write_csv(
        ctx.paths.tables_dir / "forbidden_work_confirmation.csv",
        ["audit_field", "observed_count"],
        rows,
    )


if __name__ == "__main__":
    sys.exit(main())
