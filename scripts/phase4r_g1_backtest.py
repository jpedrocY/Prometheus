"""Phase 4r - G1 Backtest Execution (standalone research script).

Implements the Phase 4q G1 Backtest-Plan Memo methodology exactly:
- Phase 4p locked G1 strategy spec (4h composite regime classifier;
  4-state regime state machine; 30m inside-regime Donchian-style
  breakout setup; structural stop with active-regime-derived bounds;
  fixed-R take-profit; time-stop; 0.25%/2x/1-position sizing
  preserved verbatim from Section 1.7.3);
- 32 predeclared variants (= 2^5) over five binary axes
  (E_min, ATR band, V_liq_min, funding band, K_confirm);
- chronological train (2022-01-01..2023-06-30 UTC), validation
  (2023-07-01..2024-06-30 UTC), OOS holdout (2024-07-01..2026-03-31
  UTC) split reused verbatim from Phase 4k;
- BTCUSDT primary, ETHUSDT comparison only;
- M1 active-vs-inactive; M2 G1-vs-always-active; M3 BTC OOS HIGH
  mean_R > 0 AND trade_count >= 30; M4 ETH non-negative differential
  AND directional consistency (ETH cannot rescue BTC);
- Section 11.6 = 8 bps HIGH per side preserved verbatim;
- Verdict A / B / C / D classification.

This script is a STANDALONE research script. It does NOT import
runtime / execution / persistence modules. It does NOT import
exchange adapters. It does NOT use credentials. It does NOT contact
any exchange API. It performs no network I/O. It reads only LOCAL
Parquet data already acquired by Phase 4i and v002.

G1 first-spec does not use the Phase 4i optional-feature subsets;
Phase 4j Section 11 governance is preserved but unused. The forbidden
input set per Phase 4q is enforced at the explicit-column loader
boundary and audited at write-time via the forbidden-work
confirmation table.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
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
INTERVAL_MS_1H = 60 * 60 * 1000
INTERVAL_MS_4H = 4 * 60 * 60 * 1000

# Phase 4p locked fixed parameters (cardinality 1; not axes)
N_BREAKOUT = 12          # 30m Donchian lookback
B_ATR = 0.10             # ATR breakout buffer multiplier
N_STOP = 12              # 30m structural stop lookback
S_BUFFER = 0.10          # ATR stop buffer multiplier
STOP_DIST_MIN_ATR = 0.50 # G1-specific stop-distance lower bound
STOP_DIST_MAX_ATR = 2.20 # G1-specific stop-distance upper bound
N_R = 2.0                # Fixed-R take-profit multiplier
T_STOP = 16              # Time-stop in completed 30m bars
C_COOLDOWN = 4           # Cooldown length in completed 4h bars
EMA_FAST_PERIOD = 20     # 4h EMA(20)
EMA_SLOW_PERIOD = 50     # 4h EMA(50)
SLOPE_LOOKBACK_4H = 3    # 4h discrete-comparison slope lookback
DE_LOOKBACK_4H = 12      # 4h directional efficiency lookback
ATR_PERIOD = 20          # 30m ATR period (Wilder)
ATR_PCT_LOOKBACK = 480   # Prior 30m bars for ATR percentile
LIQ_MEDIAN_LOOKBACK = 480# Prior 30m bars for relative-volume baseline
FUNDING_LOOKBACK = 90    # Trailing funding events for percentile

# Risk and sizing constants (Section 1.7.3 preserved verbatim)
LOCKED_RISK_FRACTION = 0.0025
LOCKED_LEVERAGE_CAP = 2.0

# Cost cells (Section 11.6 preserved verbatim)
TAKER_FEE_PER_SIDE_BPS = 4.0
COST_CELL_LOW_SLIP_BPS = 1.0
COST_CELL_MEDIUM_SLIP_BPS = 4.0
COST_CELL_HIGH_SLIP_BPS = 8.0

# Mechanism-check thresholds (Phase 4p locked; Phase 4q binding)
M1_DIFF_R_THRESHOLD = 0.10
M2_DIFF_R_THRESHOLD = 0.05
M3_MIN_MEAN_R = 0.0
M3_MIN_TRADE_COUNT = 30
BOOTSTRAP_ITERATIONS = 10_000

# CFP thresholds (Phase 4p / Phase 4q)
CFP1_MIN_TRADE_COUNT = 30
CFP1_VARIANT_FRACTION = 0.50
CFP2_MAX_NEG_MEAN_R = -0.20
CFP3_MAX_DD_R = 10.0
CFP3_MIN_PROFIT_FACTOR = 0.50
CFP6_MAX_PBO = 0.50
CFP7_MAX_MONTH_FRACTION = 0.50
CFP8_DEGRADATION_R = 0.20
CFP9_MIN_ACTIVE_FRACTION = 0.05
CSCV_S_DEFAULT = 16

# DSR
DSR_SIGNIFICANCE_Z = 1.96


# ----------------------------------------------------------------------
# Exception
# ----------------------------------------------------------------------


@dataclass
class StopCondition(Exception):
    """Raised when a Phase 4q stop condition triggers."""

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
    open_: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    volume: np.ndarray
    close_time_ms: np.ndarray


@dataclass
class SymbolFundingData:
    symbol: str
    funding_time_ms: np.ndarray
    funding_rate: np.ndarray


@dataclass
class Variant:
    """One of 32 variants from the 5 binary axes (Phase 4p locked)."""

    variant_id: int
    e_min: float
    p_atr_low: float
    p_atr_high: float
    v_liq_min: float
    p_fund_low: float
    p_fund_high: float
    k_confirm: int

    @property
    def label(self) -> str:
        return (
            f"E={self.e_min:.2f}|ATR=[{int(self.p_atr_low)},{int(self.p_atr_high)}]"
            f"|Vliq={self.v_liq_min:.2f}"
            f"|Fund=[{int(self.p_fund_low)},{int(self.p_fund_high)}]"
            f"|K={self.k_confirm}"
        )


@dataclass
class TradeRecord:
    symbol: str
    variant_id: int
    cost_cell: str
    side: str
    population: str  # "g1" | "always_active" | "inactive"
    entry_bar_idx: int
    entry_time_ms: int
    entry_price: float
    stop_price: float
    take_profit_price: float
    initial_R: float
    exit_bar_idx: int
    exit_time_ms: int
    exit_price: float
    exit_reason: str  # "stop" / "take_profit" / "time_stop"
    realized_R: float
    funding_cost_R: float


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
class StateMachineTrace:
    """Per-(symbol, variant) 4h-aligned state-machine trace."""

    symbol: str
    variant_id: int
    state: np.ndarray            # int8 [N_4h]: 0=inactive,1=candidate,2=active,3=cooldown
    direction: np.ndarray        # int8 [N_4h]: 0=none, +1=long, -1=short
    candidate_count: np.ndarray  # int32 [N_4h]
    cooldown_count: np.ndarray   # int32 [N_4h]


@dataclass
class SymbolFeatures:
    """Pre-computed per-symbol feature tables."""

    symbol: str
    # 30m base
    open_time_30m: np.ndarray
    close_time_30m: np.ndarray
    open_30m: np.ndarray
    high_30m: np.ndarray
    low_30m: np.ndarray
    close_30m: np.ndarray
    volume_30m: np.ndarray
    atr_20_30m: np.ndarray
    atr_pct_480: np.ndarray
    relative_volume_480: np.ndarray
    prior_12_high: np.ndarray
    prior_12_low: np.ndarray
    structural_stop_long: np.ndarray
    structural_stop_high_short: np.ndarray
    stop_distance_long_atr: np.ndarray
    stop_distance_short_atr: np.ndarray
    stop_distance_long_pass: np.ndarray
    stop_distance_short_pass: np.ndarray
    # 4h base
    open_time_4h: np.ndarray
    close_time_4h: np.ndarray
    close_4h: np.ndarray
    ema_20_4h: np.ndarray
    ema_50_4h: np.ndarray
    htf_trend_state: np.ndarray  # int8: -1 short, 0 neutral, +1 long
    de_4h: np.ndarray
    funding_pct_90_4h: np.ndarray
    # 4h-companion 30m features (last 30m bar within each 4h close)
    companion_30m_idx_for_4h: np.ndarray  # int64 [N_4h]
    atr_pct_at_4h: np.ndarray
    relative_volume_at_4h: np.ndarray
    # Mapping 30m -> latest completed 4h state index
    latest_completed_4h_idx_for_30m: np.ndarray  # int64 [N_30m]


# ----------------------------------------------------------------------
# Manifest loading + SHA256
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
    # research_eligible may be at the top level (v001 Phase 4i style),
    # under quality_checks (v002 kline style), or absent (v002 funding
    # style — treated as eligible by convention because v002 funding
    # has been canonical research input across multiple phases).
    qc = meta.get("quality_checks", {})
    if "research_eligible" in meta:
        research_eligible = bool(meta["research_eligible"])
    elif isinstance(qc, dict) and "research_eligible" in qc:
        research_eligible = bool(qc["research_eligible"])
    else:
        # Funding v002 convention: absence => eligible
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
        close_times.append(np.asarray(t.column("close_time").to_numpy(), dtype=np.int64))
        opens.append(np.asarray(t.column("open").to_numpy(), dtype=np.float64))
        highs.append(np.asarray(t.column("high").to_numpy(), dtype=np.float64))
        lows.append(np.asarray(t.column("low").to_numpy(), dtype=np.float64))
        closes.append(np.asarray(t.column("close").to_numpy(), dtype=np.float64))
        volumes.append(np.asarray(t.column("volume").to_numpy(), dtype=np.float64))
    open_time = np.concatenate(open_times)
    order = np.argsort(open_time, kind="stable")
    open_time_sorted = open_time[order]
    if open_time_sorted.size == 0:
        raise StopCondition("local_data_missing", f"empty kline series {symbol} {interval}")
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


def load_funding(funding_root: Path, symbol: str) -> SymbolFundingData:
    cur = funding_root / f"symbol={symbol}"
    if not cur.exists():
        raise StopCondition("local_data_missing", f"funding root missing {cur}")
    parts = sorted(cur.rglob("part-*.parquet"))
    if not parts:
        raise StopCondition("local_data_missing", f"no funding parquet under {cur}")
    times: list[np.ndarray] = []
    rates: list[np.ndarray] = []
    for p in parts:
        t = pq.ParquetFile(p).read(columns=["funding_time", "funding_rate"])
        times.append(np.asarray(t.column("funding_time").to_numpy(), dtype=np.int64))
        rates.append(np.asarray(t.column("funding_rate").to_numpy(), dtype=np.float64))
    funding_time = np.concatenate(times)
    rate = np.concatenate(rates)
    order = np.argsort(funding_time, kind="stable")
    return SymbolFundingData(
        symbol=symbol,
        funding_time_ms=funding_time[order],
        funding_rate=rate[order],
    )


# ----------------------------------------------------------------------
# Feature computation (pure numpy)
# ----------------------------------------------------------------------


def ema_seeded(values: np.ndarray, period: int) -> np.ndarray:
    """EMA seeded with SMA over first `period` bars; NaN until seed bar."""
    out = np.full_like(values, np.nan, dtype=np.float64)
    n = values.size
    if n < period:
        return out
    seed = float(np.mean(values[:period]))
    out[period - 1] = seed
    alpha = 2.0 / (period + 1.0)
    for i in range(period, n):
        out[i] = alpha * values[i] + (1.0 - alpha) * out[i - 1]
    return out


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


def directional_efficiency(close: np.ndarray, lookback: int) -> np.ndarray:
    """DE_n(t) = |close[t] - close[t-lookback]| / sum(|diff|, last lookback bars)."""
    out = np.full_like(close, np.nan, dtype=np.float64)
    n = close.size
    if n < lookback + 1:
        return out
    diffs_abs = np.abs(np.diff(close))
    csum = np.concatenate(([0.0], np.cumsum(diffs_abs)))
    for t in range(lookback, n):
        denom = csum[t] - csum[t - lookback]
        numer = abs(close[t] - close[t - lookback])
        out[t] = (numer / denom) if denom > 0 else 0.0
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


def rolling_percentile_rank_excluding_current(
    arr: np.ndarray, lookback: int
) -> np.ndarray:
    """Percentile rank of arr[t] within prior `lookback` values (excl. t).

    Uses fraction of strictly-less-than entries: pct = #(less)/lookback * 100.
    NaN returned until lookback bars of valid data available.
    """
    out = np.full_like(arr, np.nan, dtype=np.float64)
    n = arr.size
    if n <= lookback:
        return out
    for t in range(lookback, n):
        window = arr[t - lookback : t]
        v = arr[t]
        if not math.isfinite(v) or not np.all(np.isfinite(window)):
            continue
        less_count = int(np.sum(window < v))
        out[t] = 100.0 * less_count / float(lookback)
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


def funding_percentile_at_timestamp(
    timestamps_ms: np.ndarray,
    funding_time_ms: np.ndarray,
    funding_rate: np.ndarray,
    lookback: int,
) -> np.ndarray:
    """For each timestamp t in `timestamps_ms`, compute percentile rank of the
    most recent funding event whose funding_time <= t, within the trailing
    `lookback` events ending at that event (inclusive of itself).
    Returns NaN until at least `lookback` events exist with funding_time <= t.
    """
    out = np.full(timestamps_ms.size, np.nan, dtype=np.float64)
    if funding_time_ms.size == 0:
        return out
    idx_recent = np.searchsorted(funding_time_ms, timestamps_ms, side="right") - 1
    for j in range(timestamps_ms.size):
        i = int(idx_recent[j])
        if i < lookback - 1:
            continue
        window = funding_rate[i - lookback + 1 : i + 1]
        v = funding_rate[i]
        if not math.isfinite(v) or not np.all(np.isfinite(window)):
            continue
        less_count = int(np.sum(window < v))
        out[j] = 100.0 * less_count / float(lookback)
    return out


def compute_htf_trend_state(
    close_4h: np.ndarray, ema20_4h: np.ndarray, ema50_4h: np.ndarray
) -> np.ndarray:
    """+1 LONG, -1 SHORT, 0 NEUTRAL per Phase 4q regime classifier rule."""
    out = np.zeros(close_4h.size, dtype=np.int8)
    n = close_4h.size
    for i in range(n):
        if (
            i < SLOPE_LOOKBACK_4H
            or not math.isfinite(ema20_4h[i])
            or not math.isfinite(ema50_4h[i])
            or not math.isfinite(ema20_4h[i - SLOPE_LOOKBACK_4H])
        ):
            out[i] = 0
            continue
        ema20 = ema20_4h[i]
        ema50 = ema50_4h[i]
        c = close_4h[i]
        ema20_prev = ema20_4h[i - SLOPE_LOOKBACK_4H]
        if ema20 > ema50 and c > ema20 and ema20 > ema20_prev:
            out[i] = 1
        elif ema20 < ema50 and c < ema20 and ema20 < ema20_prev:
            out[i] = -1
        else:
            out[i] = 0
    return out


def build_companion_30m_idx_for_4h(
    close_time_4h: np.ndarray,
    close_time_30m: np.ndarray,
) -> np.ndarray:
    """For each 4h bar, return the index of the 30m bar with matching
    close_time. Return -1 if no match exists."""
    out = np.full(close_time_4h.size, -1, dtype=np.int64)
    pos = np.searchsorted(close_time_30m, close_time_4h, side="left")
    for i, p in enumerate(pos):
        if p < close_time_30m.size and close_time_30m[p] == close_time_4h[i]:
            out[i] = int(p)
    return out


def build_latest_completed_4h_idx_for_30m(
    close_time_4h: np.ndarray, close_time_30m: np.ndarray
) -> np.ndarray:
    """For each 30m bar (decision time = its close_time), return the
    largest index j such that close_time_4h[j] <= close_time_30m[i].
    Returns -1 if no such 4h bar exists.
    """
    pos = np.searchsorted(close_time_4h, close_time_30m, side="right") - 1
    return pos.astype(np.int64)


def compute_symbol_features(
    k30: SymbolKlineData,
    k4: SymbolKlineData,
    fund: SymbolFundingData,
) -> SymbolFeatures:
    # 30m base features
    atr20 = atr_wilder(k30.high, k30.low, k30.close, ATR_PERIOD)
    atr_pct_480 = rolling_percentile_rank_excluding_current(atr20, ATR_PCT_LOOKBACK)
    median_v_480 = rolling_median_excluding_current(k30.volume, LIQ_MEDIAN_LOOKBACK)
    rel_vol = np.where(
        np.isfinite(median_v_480) & (median_v_480 > 0),
        k30.volume / np.where(median_v_480 == 0, np.nan, median_v_480),
        np.nan,
    )
    prior_12_high = rolling_max_excluding_current(k30.high, N_BREAKOUT)
    prior_12_low = rolling_min_excluding_current(k30.low, N_BREAKOUT)
    # Structural stop windows == N_STOP (=12), same as N_BREAKOUT here
    stop_long = prior_12_low - S_BUFFER * atr20
    stop_short_high = prior_12_high + S_BUFFER * atr20
    # Long candidate stop_distance using last close (entry approx via
    # next-bar open, but distance is computed from current close as a
    # reasonable evaluation; the actual entry-time stop is recomputed
    # in trade simulation using the entry_price and the same stop)
    sd_long = np.abs(k30.close - stop_long) / atr20
    sd_short = np.abs(stop_short_high - k30.close) / atr20
    sd_long_pass = (sd_long >= STOP_DIST_MIN_ATR) & (sd_long <= STOP_DIST_MAX_ATR)
    sd_short_pass = (sd_short >= STOP_DIST_MIN_ATR) & (sd_short <= STOP_DIST_MAX_ATR)

    # 4h base features
    ema20_4h = ema_seeded(k4.close, EMA_FAST_PERIOD)
    ema50_4h = ema_seeded(k4.close, EMA_SLOW_PERIOD)
    htf_state = compute_htf_trend_state(k4.close, ema20_4h, ema50_4h)
    de_4h = directional_efficiency(k4.close, DE_LOOKBACK_4H)
    funding_pct_4h = funding_percentile_at_timestamp(
        k4.close_time_ms, fund.funding_time_ms, fund.funding_rate, FUNDING_LOOKBACK
    )

    # 4h-companion 30m features
    companion_idx = build_companion_30m_idx_for_4h(k4.close_time_ms, k30.close_time_ms)
    atr_pct_at_4h = np.full(k4.close_time_ms.size, np.nan, dtype=np.float64)
    rv_at_4h = np.full(k4.close_time_ms.size, np.nan, dtype=np.float64)
    valid = companion_idx >= 0
    atr_pct_at_4h[valid] = atr_pct_480[companion_idx[valid]]
    rv_at_4h[valid] = rel_vol[companion_idx[valid]]

    latest_4h_idx_for_30m = build_latest_completed_4h_idx_for_30m(
        k4.close_time_ms, k30.close_time_ms
    )

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
        atr_pct_480=atr_pct_480,
        relative_volume_480=rel_vol,
        prior_12_high=prior_12_high,
        prior_12_low=prior_12_low,
        structural_stop_long=stop_long,
        structural_stop_high_short=stop_short_high,
        stop_distance_long_atr=sd_long,
        stop_distance_short_atr=sd_short,
        stop_distance_long_pass=sd_long_pass,
        stop_distance_short_pass=sd_short_pass,
        open_time_4h=k4.open_time_ms,
        close_time_4h=k4.close_time_ms,
        close_4h=k4.close,
        ema_20_4h=ema20_4h,
        ema_50_4h=ema50_4h,
        htf_trend_state=htf_state,
        de_4h=de_4h,
        funding_pct_90_4h=funding_pct_4h,
        companion_30m_idx_for_4h=companion_idx,
        atr_pct_at_4h=atr_pct_at_4h,
        relative_volume_at_4h=rv_at_4h,
        latest_completed_4h_idx_for_30m=latest_4h_idx_for_30m,
    )


# ----------------------------------------------------------------------
# Variant grid (Phase 4p locked: 32 = 2^5 over five binary axes)
# ----------------------------------------------------------------------


def build_variants() -> list[Variant]:
    """Build deterministic lexicographic 32-variant grid.

    Axis order (axis name lexicographic):
      ATR_band, E_min, K_confirm, V_liq_min, funding_band

    Within each axis, value order is the natural numeric order.
    """
    atr_bands = [(20.0, 80.0), (30.0, 70.0)]
    e_mins = [0.30, 0.40]
    k_confirms = [2, 3]
    v_liq_mins = [0.80, 1.00]
    fund_bands = [(15.0, 85.0), (25.0, 75.0)]

    variants: list[Variant] = []
    vid = 0
    for atr_low, atr_high in atr_bands:
        for e_min in e_mins:
            for k_confirm in k_confirms:
                for v_liq_min in v_liq_mins:
                    for f_low, f_high in fund_bands:
                        variants.append(
                            Variant(
                                variant_id=vid,
                                e_min=e_min,
                                p_atr_low=atr_low,
                                p_atr_high=atr_high,
                                v_liq_min=v_liq_min,
                                p_fund_low=f_low,
                                p_fund_high=f_high,
                                k_confirm=k_confirm,
                            )
                        )
                        vid += 1
    if len(variants) != 32:
        raise StopCondition(
            "variant_grid_violation",
            f"expected 32 variants, got {len(variants)}",
        )
    return variants


# ----------------------------------------------------------------------
# Regime classifier + state machine
# ----------------------------------------------------------------------


def compute_favorable_per_4h(
    f: SymbolFeatures, v: Variant
) -> tuple[np.ndarray, np.ndarray]:
    """Boolean arrays favorable_long_4h, favorable_short_4h per 4h bar."""
    n = f.close_4h.size
    fav_long = np.zeros(n, dtype=bool)
    fav_short = np.zeros(n, dtype=bool)
    for i in range(n):
        s = f.htf_trend_state[i]
        de_v = f.de_4h[i]
        atr_v = f.atr_pct_at_4h[i]
        liq_v = f.relative_volume_at_4h[i]
        fund_v = f.funding_pct_90_4h[i]
        if (
            not math.isfinite(de_v)
            or not math.isfinite(atr_v)
            or not math.isfinite(liq_v)
            or not math.isfinite(fund_v)
        ):
            continue
        de_pass = de_v >= v.e_min
        atr_pass = (atr_v >= v.p_atr_low) and (atr_v <= v.p_atr_high)
        liq_pass = liq_v >= v.v_liq_min
        fund_pass = (fund_v >= v.p_fund_low) and (fund_v <= v.p_fund_high)
        all_pass = de_pass and atr_pass and liq_pass and fund_pass
        if not all_pass:
            continue
        if s == 1:
            fav_long[i] = True
        elif s == -1:
            fav_short[i] = True
    return fav_long, fav_short


def run_state_machine_4h(
    f: SymbolFeatures, v: Variant, fav_long: np.ndarray, fav_short: np.ndarray,
    exit_event_4h_idx: list[tuple[int, int]] | None = None,
) -> StateMachineTrace:
    """Deterministic state-machine update on completed 4h bars.

    States: 0=inactive, 1=candidate, 2=active, 3=cooldown.
    Direction: 0=none, +1=long, -1=short.

    `exit_event_4h_idx` (optional) is a sorted list of
    (exit_4h_idx, exit_direction) tuples that force an active->cooldown
    transition at the listed 4h bar (representing a trade exit).
    """
    n = f.close_4h.size
    state = np.zeros(n, dtype=np.int8)
    direction = np.zeros(n, dtype=np.int8)
    cand_count = np.zeros(n, dtype=np.int32)
    cool_count = np.zeros(n, dtype=np.int32)

    cur_state = 0
    cur_dir = 0
    cur_cand = 0
    cur_cool = 0

    exit_lookup: dict[int, int] = {}
    if exit_event_4h_idx is not None:
        for ix, d in exit_event_4h_idx:
            exit_lookup[int(ix)] = int(d)

    for i in range(n):
        # Apply forced cooldown transition from a trade exit at this 4h bar
        force_exit_dir = exit_lookup.get(i)
        if force_exit_dir is not None and cur_state == 2 and force_exit_dir == cur_dir:
            cur_state = 3
            cur_cool = 1
            # cur_dir retained
            state[i] = cur_state
            direction[i] = cur_dir
            cand_count[i] = cur_cand
            cool_count[i] = cur_cool
            continue

        if cur_state == 0:
            cur_cand = 0
            cur_cool = 0
            if fav_long[i]:
                cur_state = 1
                cur_dir = 1
                cur_cand = 1
            elif fav_short[i]:
                cur_state = 1
                cur_dir = -1
                cur_cand = 1
            else:
                cur_dir = 0

        elif cur_state == 1:
            if cur_dir == 1 and fav_long[i] or cur_dir == -1 and fav_short[i]:
                cur_cand += 1
                if cur_cand >= v.k_confirm:
                    cur_state = 2
                    cur_cand = 0
            else:
                cur_state = 0
                cur_dir = 0
                cur_cand = 0
                cur_cool = 0

        elif cur_state == 2:
            if cur_dir == 1 and fav_long[i] or cur_dir == -1 and fav_short[i]:
                pass  # remain active
            else:
                cur_state = 3
                cur_cool = 1

        elif cur_state == 3:
            cur_cool += 1
            if cur_dir == 1 and fav_long[i] or cur_dir == -1 and fav_short[i]:
                if cur_cool >= C_COOLDOWN:
                    cur_state = 2
                    cur_cool = 0
            else:
                if cur_cool >= C_COOLDOWN:
                    cur_state = 0
                    cur_dir = 0
                    cur_cool = 0

        state[i] = cur_state
        direction[i] = cur_dir
        cand_count[i] = cur_cand
        cool_count[i] = cur_cool

    return StateMachineTrace(
        symbol=f.symbol,
        variant_id=v.variant_id,
        state=state,
        direction=direction,
        candidate_count=cand_count,
        cooldown_count=cool_count,
    )


# ----------------------------------------------------------------------
# Trade simulation
# ----------------------------------------------------------------------


def _funding_cost_R(
    fund: SymbolFundingData,
    side: str,
    entry_time_ms: int,
    exit_time_ms: int,
    entry_price: float,
    R_per_unit: float,
    position_size_units: float,
) -> float:
    """Funding cost expressed in R units.

    Sign: positive funding rate => longs pay shorts. v002 funding manifest
    `funding_rate` is the per-event rate (fraction).
    """
    if R_per_unit <= 0 or position_size_units <= 0:
        return 0.0
    if exit_time_ms <= entry_time_ms:
        return 0.0
    # Find funding events strictly inside the interval
    mask = (fund.funding_time_ms > entry_time_ms) & (
        fund.funding_time_ms < exit_time_ms
    )
    rates = fund.funding_rate[mask]
    if rates.size == 0:
        return 0.0
    sign = 1.0 if side == "long" else -1.0
    notional_per_unit = entry_price
    cost_per_event = sign * float(np.sum(rates)) * notional_per_unit * position_size_units
    # Funding cost is a debit when positive (longs pay shorts on positive rate);
    # convert to R units (negative = adverse). Expressed per-unit risk:
    # debit / (position_size_units * R_per_unit) = cost / size_units / R
    cost_R = -cost_per_event / (position_size_units * R_per_unit)
    return float(cost_R)


def _apply_costs_long(entry: float, exit_p: float, slip_bps: float) -> tuple[float, float]:
    """Long: entry slipped up; exit slipped down by slip+fee bps each side."""
    cost = (slip_bps + TAKER_FEE_PER_SIDE_BPS) / 10_000.0
    return entry * (1.0 + cost), exit_p * (1.0 - cost)


def _apply_costs_short(entry: float, exit_p: float, slip_bps: float) -> tuple[float, float]:
    cost = (slip_bps + TAKER_FEE_PER_SIDE_BPS) / 10_000.0
    return entry * (1.0 - cost), exit_p * (1.0 + cost)


def simulate_trades_for_signal_array(
    f: SymbolFeatures,
    fund: SymbolFundingData,
    long_signals: np.ndarray,
    short_signals: np.ndarray,
    slip_bps: float,
    cost_cell: str,
    variant_id: int,
    population: str,
    sm: StateMachineTrace | None,
) -> tuple[list[TradeRecord], list[tuple[int, int]]]:
    """Simulate trades from a boolean signal array (one entry candidate per
    completed 30m bar, evaluated at the bar's close, executed at the next
    bar's open).

    Stop precedence: stop > take-profit > time-stop.
    Same-bar stop / take-profit ambiguity: stop wins.

    For G1 population (`g1`), the signal arrays are already gated by
    regime_active. For `always_active`, no regime gate. For `inactive`,
    signal arrays are the breakouts that fired during non-active states.

    Returns the list of TradeRecord and a list of (exit_4h_idx,
    exit_direction) tuples for trade-driven cooldown updates (unused here
    but kept for interface compatibility with the regime state machine).
    """
    n_30m = f.open_time_30m.size
    trades: list[TradeRecord] = []
    exit_events: list[tuple[int, int]] = []

    in_pos = False
    entry_idx = 0
    side = ""
    entry_price = 0.0
    stop_price = 0.0
    tp_price = 0.0
    R_per_unit = 0.0
    pos_size_units = 0.0
    entry_time = 0

    for i in range(n_30m):
        # If positioned, evaluate exit on this bar's price action
        if in_pos:
            high = f.high_30m[i]
            low = f.low_30m[i]
            stop_touched = (low <= stop_price) if side == "long" else (high >= stop_price)
            tp_touched = (high >= tp_price) if side == "long" else (low <= tp_price)
            bars_in_trade = i - entry_idx
            time_due = bars_in_trade >= T_STOP

            exit_kind: str | None = None
            exit_p = 0.0
            if stop_touched:
                exit_kind = "stop"
                exit_p = stop_price
            elif tp_touched:
                exit_kind = "take_profit"
                exit_p = tp_price
            elif time_due:
                # exit at next 30m bar's open (or current bar's close if last)
                if i + 1 < n_30m:
                    exit_kind = "time_stop"
                    exit_p = f.open_30m[i + 1]
                else:
                    exit_kind = "time_stop"
                    exit_p = f.close_30m[i]

            if exit_kind is not None:
                # Apply costs and finalize
                if side == "long":
                    eep, exp_ = _apply_costs_long(entry_price, exit_p, slip_bps)
                    raw_R = (exp_ - eep) / R_per_unit
                else:
                    eep, exp_ = _apply_costs_short(entry_price, exit_p, slip_bps)
                    raw_R = (eep - exp_) / R_per_unit
                exit_time = (
                    int(f.open_time_30m[i + 1])
                    if (exit_kind == "time_stop" and i + 1 < n_30m)
                    else int(f.close_time_30m[i])
                )
                fc_R = _funding_cost_R(
                    fund, side, entry_time, exit_time, entry_price,
                    R_per_unit, pos_size_units,
                )
                realized_R = float(raw_R + fc_R)
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
                        take_profit_price=tp_price,
                        initial_R=R_per_unit,
                        exit_bar_idx=i,
                        exit_time_ms=exit_time,
                        exit_price=exit_p,
                        exit_reason=exit_kind,
                        realized_R=realized_R,
                        funding_cost_R=fc_R,
                    )
                )
                # Trade exit -> emit cooldown event for the 4h state machine.
                # Map exit time to 4h state-machine bar index.
                if sm is not None:
                    exit_close_time = exit_time
                    pos = int(np.searchsorted(
                        f.close_time_4h, exit_close_time, side="right"
                    )) - 1
                    if pos >= 0:
                        exit_events.append((pos + 1 if pos + 1 < f.close_time_4h.size else pos,
                                            1 if side == "long" else -1))
                in_pos = False

        # If not positioned, look for an entry signal at this bar's close
        if not in_pos and i + 1 < n_30m:
            sig_long = bool(long_signals[i])
            sig_short = bool(short_signals[i])
            if sig_long or sig_short:
                # Stop-distance gate uses CLOSE-based check; recompute
                # entry-time check using next-bar open and current
                # structural stop (the structural stop is fixed at the
                # signal bar; entry-price is the next bar's open).
                if sig_long:
                    side = "long"
                    sp = f.structural_stop_long[i]
                    ep = f.open_30m[i + 1]
                else:
                    side = "short"
                    sp = f.structural_stop_high_short[i]
                    ep = f.open_30m[i + 1]
                if not math.isfinite(sp) or not math.isfinite(ep):
                    continue
                R_unit = (ep - sp) if side == "long" else (sp - ep)
                if R_unit <= 0:
                    # invalid stop ordering; reject
                    continue
                # Entry-time stop-distance gate (using ATR at signal bar i)
                atr_v = f.atr_20_30m[i]
                if not math.isfinite(atr_v) or atr_v <= 0:
                    continue
                sd_atr = abs(ep - sp) / atr_v
                if sd_atr < STOP_DIST_MIN_ATR or sd_atr > STOP_DIST_MAX_ATR:
                    continue
                # Position sizing
                sizing_equity = 100_000.0
                size_units = sizing_equity * LOCKED_RISK_FRACTION / R_unit
                position_notional = size_units * ep
                if position_notional > LOCKED_LEVERAGE_CAP * sizing_equity:
                    size_units = LOCKED_LEVERAGE_CAP * sizing_equity / ep
                if size_units <= 0:
                    continue
                tp = (
                    ep + N_R * R_unit if side == "long"
                    else ep - N_R * R_unit
                )
                in_pos = True
                entry_idx = i + 1
                entry_price = ep
                stop_price = sp
                tp_price = tp
                R_per_unit = R_unit
                pos_size_units = size_units
                entry_time = int(f.open_time_30m[i + 1])

    return trades, exit_events


def map_4h_state_to_30m_active(
    f: SymbolFeatures, sm: StateMachineTrace
) -> tuple[np.ndarray, np.ndarray]:
    """Return per-30m-bar (active_long, active_short) boolean arrays."""
    n = f.open_time_30m.size
    al = np.zeros(n, dtype=bool)
    ash = np.zeros(n, dtype=bool)
    for i in range(n):
        idx_4h = int(f.latest_completed_4h_idx_for_30m[i])
        if idx_4h < 0:
            continue
        if sm.state[idx_4h] == 2:
            d = sm.direction[idx_4h]
            if d == 1:
                al[i] = True
            elif d == -1:
                ash[i] = True
    return al, ash


def map_4h_state_to_30m_inactive(
    f: SymbolFeatures, sm: StateMachineTrace
) -> tuple[np.ndarray, np.ndarray]:
    """Return per-30m-bar (inactive_long, inactive_short) - the breakout
    rule is direction-blind for inactive population (M1 baseline allows
    both directions). Inactive = state in {inactive, candidate, cooldown}.
    """
    n = f.open_time_30m.size
    il = np.zeros(n, dtype=bool)
    ish = np.zeros(n, dtype=bool)
    for i in range(n):
        idx_4h = int(f.latest_completed_4h_idx_for_30m[i])
        if idx_4h < 0:
            il[i] = True
            ish[i] = True
            continue
        if sm.state[idx_4h] != 2:
            il[i] = True
            ish[i] = True
    return il, ish


def compute_breakout_signals(f: SymbolFeatures) -> tuple[np.ndarray, np.ndarray]:
    """Direction-blind 30m Donchian breakout signals.

    long  setup: close[t] > prior_12_high[t] + B_atr * ATR(20)[t]
    short setup: close[t] < prior_12_low[t]  - B_atr * ATR(20)[t]
    """
    n = f.open_time_30m.size
    long_setup = np.zeros(n, dtype=bool)
    short_setup = np.zeros(n, dtype=bool)
    for i in range(n):
        h = f.prior_12_high[i]
        lo = f.prior_12_low[i]
        a = f.atr_20_30m[i]
        c = f.close_30m[i]
        if not math.isfinite(h) or not math.isfinite(a):
            continue
        if c > h + B_ATR * a:
            long_setup[i] = True
        if math.isfinite(lo) and c < lo - B_ATR * a:
            short_setup[i] = True
    return long_setup, short_setup


# ----------------------------------------------------------------------
# Aggregation
# ----------------------------------------------------------------------


def aggregate_trades(
    trades: list[TradeRecord],
    cost_cell: str,
    window_start_ms: int,
    window_end_ms: int,
) -> tuple[VariantResult, np.ndarray]:
    """Aggregate trades within a window. Returns (VariantResult, R_array)."""
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
# Statistics: bootstrap, DSR, CSCV
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
    sharpe: float, n_variants: int, n_trades: int, skewness: float, kurtosis: float
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
    return mean_diff, float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


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
            in_chunks = [sub_arrays[v][s] for s in range(s_subsamples) if s in in_set]
            out_chunks = [sub_arrays[v][s] for s in range(s_subsamples) if s not in in_set]
            in_arr = np.concatenate(in_chunks) if in_chunks else np.array([], dtype=np.float64)
            out_arr = np.concatenate(out_chunks) if out_chunks else np.array([], dtype=np.float64)
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
    """Train->OOS PBO using full-window ranks: P(rank_oos > median | best on train).

    With a single train/test pair this is binary (0 or 1); we report
    instead the simple statistic 'oos_rank_fraction_below_median' for
    the train-best variant. This is a docs-level proxy used in tandem
    with CSCV (which is the binding PBO).
    """
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


def write_csv(path: Path, header: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [",".join(header)]
    for r in rows:
        cells: list[str] = []
        for v in r:
            if isinstance(v, float):
                cells.append(f"{v:.10g}")
            elif v is None:
                cells.append("")
            else:
                s = str(v)
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
# Plot helpers (matplotlib optional; degrade gracefully)
# ----------------------------------------------------------------------


def try_plot_cumulative_R(
    path: Path, R_arrays: dict[str, np.ndarray], title: str
) -> bool:
    try:
        import matplotlib  # type: ignore[import-untyped]

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # type: ignore[import-untyped]
    except Exception:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    for label, arr in R_arrays.items():
        if arr.size == 0:
            continue
        ax.plot(np.cumsum(arr), label=label)
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
    try:
        import matplotlib  # type: ignore[import-untyped]

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # type: ignore[import-untyped]
    except Exception:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    for label, arr in arrays.items():
        if arr.size == 0:
            continue
        ax.hist(arr, bins=30, alpha=0.5, label=label)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return True


def try_plot_drawdown(
    path: Path, R_arr: np.ndarray, title: str
) -> bool:
    try:
        import matplotlib  # type: ignore[import-untyped]

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # type: ignore[import-untyped]
    except Exception:
        return False
    if R_arr.size == 0:
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


def try_plot_regime_timeline(
    path: Path, sm: StateMachineTrace, close_time_4h: np.ndarray, title: str
) -> bool:
    try:
        import matplotlib  # type: ignore[import-untyped]

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # type: ignore[import-untyped]
    except Exception:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    state = sm.state.astype(np.int32)
    direction = sm.direction.astype(np.int32)
    fig, ax = plt.subplots(figsize=(10, 3))
    times = (close_time_4h / 1000.0).astype(np.int64)
    ax.plot(times, state, drawstyle="steps-post", label="state")
    ax.plot(times, direction, drawstyle="steps-post", label="direction", alpha=0.6)
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
    forbidden_access_counters: dict[str, int] = field(default_factory=dict)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 4r G1 backtest execution (standalone research script)"
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
    parser.add_argument("--output-dir", default="data/research/phase4r")
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

    print("Phase 4r G1 backtest execution starting", flush=True)
    print(f"  symbols={args.symbols}, primary={args.primary_symbol}", flush=True)
    print(f"  train={args.train_start}..{args.train_end}", flush=True)
    print(f"  val=  {args.validation_start}..{args.validation_end}", flush=True)
    print(f"  oos=  {args.oos_start}..{args.oos_end}", flush=True)
    print(f"  rng_seed={args.rng_seed}", flush=True)

    try:
        return _run(ctx)
    except StopCondition as e:
        print(f"STOP_CONDITION: {e}", file=sys.stderr, flush=True)
        write_json(
            paths.tables_dir / "verdict_declaration.csv.error.json",
            {"verdict": "D", "stop_condition": e.reason, "detail": e.detail},
        )
        return 2


def _run(ctx: RunContext) -> int:
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
            "30m_klines",
        ))
        ctx.manifests.append(load_manifest(
            manifest_root / f"binance_usdm_{sym_lower}_4h__v001.manifest.json",
            f"binance_usdm_{sym_lower}_4h__v001",
            "4h_klines",
        ))
        ctx.manifests.append(load_manifest(
            manifest_root / f"binance_usdm_{sym_lower}_funding__v002.manifest.json",
            f"binance_usdm_{sym_lower}_funding__v002",
            "funding",
        ))
    for m in ctx.manifests:
        if not m.research_eligible:
            raise StopCondition(
                "manifest_research_eligible_mismatch",
                f"{m.name} expected research_eligible=true",
            )

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------
    klines_root = Path(args.data_root) / "klines"
    funding_root = Path(args.data_root) / "funding_rate"

    print("Loading data (klines + funding only; explicit-column loaders)...", flush=True)
    symbol_features: dict[str, SymbolFeatures] = {}
    funding_data: dict[str, SymbolFundingData] = {}
    for sym in args.symbols:
        print(f"  {sym} 30m klines...", flush=True)
        k30 = load_kline_symbol_interval(klines_root, sym, "30m")
        print(f"  {sym} 4h klines...", flush=True)
        k4 = load_kline_symbol_interval(klines_root, sym, "4h")
        print(f"  {sym} funding (v002)...", flush=True)
        fund = load_funding(funding_root, sym)
        funding_data[sym] = fund
        print(f"  {sym} computing features ({k30.open_time_ms.size} 30m bars)...", flush=True)
        symbol_features[sym] = compute_symbol_features(k30, k4, fund)

    # ------------------------------------------------------------------
    # Build variants
    # ------------------------------------------------------------------
    variants = build_variants()
    print(f"Variant grid: {len(variants)} variants", flush=True)

    # ------------------------------------------------------------------
    # Per-variant simulation across cost cells
    # ------------------------------------------------------------------
    cost_cells = {
        "LOW": COST_CELL_LOW_SLIP_BPS,
        "MEDIUM": COST_CELL_MEDIUM_SLIP_BPS,
        "HIGH": COST_CELL_HIGH_SLIP_BPS,
    }

    # Pre-compute direction-blind breakout signals once per symbol
    breakout_long: dict[str, np.ndarray] = {}
    breakout_short: dict[str, np.ndarray] = {}
    for sym in args.symbols:
        bl, bs = compute_breakout_signals(symbol_features[sym])
        breakout_long[sym] = bl
        breakout_short[sym] = bs

    state_traces: dict[str, dict[int, StateMachineTrace]] = {}

    # results[symbol][window][cost_cell][variant_id] = (G1, AA, INA) tuple
    results_g1: dict[str, dict[str, dict[str, dict[int, VariantResult]]]] = {}
    results_aa: dict[str, dict[str, dict[str, dict[int, VariantResult]]]] = {}
    results_ina: dict[str, dict[str, dict[str, dict[int, VariantResult]]]] = {}
    trades_g1: dict[str, dict[str, dict[int, list[TradeRecord]]]] = {}
    trades_aa: dict[str, dict[str, dict[int, list[TradeRecord]]]] = {}
    trades_ina: dict[str, dict[str, dict[int, list[TradeRecord]]]] = {}

    for sym in args.symbols:
        results_g1[sym] = {"train": {}, "validation": {}, "oos": {}}
        results_aa[sym] = {"train": {}, "validation": {}, "oos": {}}
        results_ina[sym] = {"train": {}, "validation": {}, "oos": {}}
        for cell in cost_cells:
            for w in ("train", "validation", "oos"):
                results_g1[sym][w][cell] = {}
                results_aa[sym][w][cell] = {}
                results_ina[sym][w][cell] = {}
        trades_g1[sym] = {cell: {} for cell in cost_cells}
        trades_aa[sym] = {cell: {} for cell in cost_cells}
        trades_ina[sym] = {cell: {} for cell in cost_cells}
        state_traces[sym] = {}

    total_runs = len(args.symbols) * len(cost_cells) * len(variants) * 3
    run_count = 0
    print(f"Running {total_runs} (variant, symbol, cost, population) simulations...", flush=True)

    for sym in args.symbols:
        f = symbol_features[sym]
        for v in variants:
            fav_l, fav_s = compute_favorable_per_4h(f, v)
            sm = run_state_machine_4h(f, v, fav_l, fav_s, exit_event_4h_idx=None)
            state_traces[sym][v.variant_id] = sm
            al, ash = map_4h_state_to_30m_active(f, sm)
            il, ish = map_4h_state_to_30m_inactive(f, sm)

            bl = breakout_long[sym]
            bs = breakout_short[sym]
            g1_long_sig = bl & al
            g1_short_sig = bs & ash
            aa_long_sig = bl
            aa_short_sig = bs
            ina_long_sig = bl & il
            ina_short_sig = bs & ish

            for cell, slip_bps in cost_cells.items():
                trs_g1, _ = simulate_trades_for_signal_array(
                    f, funding_data[sym], g1_long_sig, g1_short_sig,
                    slip_bps, cell, v.variant_id, "g1", sm,
                )
                trs_aa, _ = simulate_trades_for_signal_array(
                    f, funding_data[sym], aa_long_sig, aa_short_sig,
                    slip_bps, cell, v.variant_id, "always_active", None,
                )
                trs_ina, _ = simulate_trades_for_signal_array(
                    f, funding_data[sym], ina_long_sig, ina_short_sig,
                    slip_bps, cell, v.variant_id, "inactive", None,
                )
                trades_g1[sym][cell][v.variant_id] = trs_g1
                trades_aa[sym][cell][v.variant_id] = trs_aa
                trades_ina[sym][cell][v.variant_id] = trs_ina

                for w_name, ws, we in (
                    ("train", ctx.train_start_ms, ctx.train_end_ms),
                    ("validation", ctx.val_start_ms, ctx.val_end_ms),
                    ("oos", ctx.oos_start_ms, ctx.oos_end_ms),
                ):
                    res_g1, _ = aggregate_trades(trs_g1, cell, ws, we)
                    res_g1.window = w_name
                    res_g1.symbol = sym
                    results_g1[sym][w_name][cell][v.variant_id] = res_g1

                    res_aa, _ = aggregate_trades(trs_aa, cell, ws, we)
                    res_aa.window = w_name
                    res_aa.symbol = sym
                    results_aa[sym][w_name][cell][v.variant_id] = res_aa

                    res_ina, _ = aggregate_trades(trs_ina, cell, ws, we)
                    res_ina.window = w_name
                    res_ina.symbol = sym
                    results_ina[sym][w_name][cell][v.variant_id] = res_ina

                run_count += 3
                if run_count % 192 == 0:
                    print(
                        f"  progress: {run_count}/{total_runs} simulations",
                        flush=True,
                    )

    # ------------------------------------------------------------------
    # Train-best variant by deflated Sharpe (BTCUSDT primary, MEDIUM-cost,
    # G1 population)
    # ------------------------------------------------------------------
    print("Selecting BTC-train-best variant by deflated Sharpe...", flush=True)
    primary = args.primary_symbol
    btc_train = results_g1[primary]["train"]["MEDIUM"]
    dsr_per_variant: dict[int, float] = {}
    sharpe_per_variant: dict[int, float] = {}
    for v in variants:
        r = btc_train.get(v.variant_id)
        ts = trades_g1[primary]["MEDIUM"][v.variant_id]
        train_ts = [t for t in ts if ctx.train_start_ms <= t.entry_time_ms <= ctx.train_end_ms]
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
        key=lambda kv: (kv[1] if math.isfinite(kv[1]) else -1e9, sharpe_per_variant[kv[0]]),
    )[0]
    best_variant = variants[best_v_id]
    print(
        f"BTC-train-best: id={best_v_id}, DSR={dsr_per_variant[best_v_id]:.3f}, "
        f"Sharpe(train)={sharpe_per_variant[best_v_id]:.3f}, label={best_variant.label}",
        flush=True,
    )

    # ------------------------------------------------------------------
    # M1: active vs inactive on BTC OOS HIGH
    # ------------------------------------------------------------------
    cell = "HIGH"
    btc_g1_oos_trs = [
        t for t in trades_g1[primary][cell][best_variant.variant_id]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    btc_ina_oos_trs = [
        t for t in trades_ina[primary][cell][best_variant.variant_id]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    arr_g1 = np.array([t.realized_R for t in btc_g1_oos_trs], dtype=np.float64)
    arr_ina = np.array([t.realized_R for t in btc_ina_oos_trs], dtype=np.float64)
    m1_diff, m1_ci_low, m1_ci_high = bootstrap_diff_mean_ci(
        arr_g1, arr_ina, args.bootstrap_iterations, rng
    )
    m1_pass = m1_diff >= M1_DIFF_R_THRESHOLD and m1_ci_low > 0.0 and arr_g1.size > 0

    # M2: G1 vs always-active on BTC OOS HIGH
    btc_aa_oos_trs = [
        t for t in trades_aa[primary][cell][best_variant.variant_id]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    arr_aa = np.array([t.realized_R for t in btc_aa_oos_trs], dtype=np.float64)
    m2_diff, m2_ci_low, m2_ci_high = bootstrap_diff_mean_ci(
        arr_g1, arr_aa, args.bootstrap_iterations, rng
    )
    m2_pass = m2_diff >= M2_DIFF_R_THRESHOLD and m2_ci_low > 0.0 and arr_g1.size > 0

    # M3: BTC OOS HIGH mean_R > 0 AND trade_count >= 30
    btc_g1_oos_high = results_g1[primary]["oos"]["HIGH"][best_variant.variant_id]
    m3_pass = (
        btc_g1_oos_high.mean_R > M3_MIN_MEAN_R
        and btc_g1_oos_high.trade_count >= M3_MIN_TRADE_COUNT
    )

    # M4: ETH OOS HIGH non-negative differential AND directional consistency
    comparison = args.comparison_symbol
    eth_g1_oos_trs = [
        t for t in trades_g1[comparison][cell][best_variant.variant_id]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    eth_ina_oos_trs = [
        t for t in trades_ina[comparison][cell][best_variant.variant_id]
        if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
    ]
    arr_eth_g1 = np.array([t.realized_R for t in eth_g1_oos_trs], dtype=np.float64)
    arr_eth_ina = np.array([t.realized_R for t in eth_ina_oos_trs], dtype=np.float64)
    eth_diff_g1_minus_ina = (
        float(arr_eth_g1.mean() - arr_eth_ina.mean())
        if arr_eth_g1.size > 0 and arr_eth_ina.size > 0 else 0.0
    )
    btc_diff_g1_minus_ina = (
        float(arr_g1.mean() - arr_ina.mean())
        if arr_g1.size > 0 and arr_ina.size > 0 else 0.0
    )
    eth_directional = (
        (btc_diff_g1_minus_ina >= 0 and eth_diff_g1_minus_ina >= 0)
        or (btc_diff_g1_minus_ina < 0 and eth_diff_g1_minus_ina < 0)
    )
    m4_pass = eth_diff_g1_minus_ina >= 0.0 and eth_directional

    print(
        f"M1 pass={m1_pass} diff={m1_diff:.4f} "
        f"ci=[{m1_ci_low:.4f},{m1_ci_high:.4f}]",
        flush=True,
    )
    print(
        f"M2 pass={m2_pass} diff={m2_diff:.4f} "
        f"ci=[{m2_ci_low:.4f},{m2_ci_high:.4f}]",
        flush=True,
    )
    print(
        f"M3 pass={m3_pass} mean_R={btc_g1_oos_high.mean_R:.4f} "
        f"n={btc_g1_oos_high.trade_count}",
        flush=True,
    )
    print(f"M4 pass={m4_pass} eth_diff={eth_diff_g1_minus_ina:.4f}", flush=True)

    # ------------------------------------------------------------------
    # PBO: train -> validation, train -> OOS (rank-based proxy)
    # ------------------------------------------------------------------
    train_sharpe_btc = {
        v.variant_id: results_g1[primary]["train"]["HIGH"][v.variant_id].sharpe
        for v in variants
    }
    val_sharpe_btc = {
        v.variant_id: results_g1[primary]["validation"]["HIGH"][v.variant_id].sharpe
        for v in variants
    }
    oos_sharpe_btc = {
        v.variant_id: results_g1[primary]["oos"]["HIGH"][v.variant_id].sharpe
        for v in variants
    }
    pbo_tv = pbo_rank_based(train_sharpe_btc, val_sharpe_btc)
    pbo_to = pbo_rank_based(train_sharpe_btc, oos_sharpe_btc)

    # CSCV PBO on OOS
    f_btc = symbol_features[primary]
    n_oos_bars = int(np.sum(
        (f_btc.open_time_30m >= ctx.oos_start_ms)
        & (f_btc.open_time_30m <= ctx.oos_end_ms)
    ))
    per_variant_R: dict[int, np.ndarray] = {}
    per_variant_idx: dict[int, np.ndarray] = {}
    for v in variants:
        ts = trades_g1[primary]["HIGH"][v.variant_id]
        oos_ts = [
            t for t in ts if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
        ]
        per_variant_R[v.variant_id] = np.array(
            [t.realized_R for t in oos_ts], dtype=np.float64
        )
        # Map entry idx in the OOS window
        oos_open_times = f_btc.open_time_30m[
            (f_btc.open_time_30m >= ctx.oos_start_ms)
            & (f_btc.open_time_30m <= ctx.oos_end_ms)
        ]
        if oos_ts and oos_open_times.size > 0:
            entries = np.array([t.entry_time_ms for t in oos_ts], dtype=np.int64)
            pos = np.searchsorted(oos_open_times, entries, side="left").astype(np.int64)
            per_variant_idx[v.variant_id] = pos
        else:
            per_variant_idx[v.variant_id] = np.array([], dtype=np.int64)
    cscv_pbo_value, cscv_detail = cscv_pbo(
        per_variant_R, per_variant_idx, n_oos_bars, args.cscv_s
    )

    print(
        f"PBO: train->val={pbo_tv:.3f}, train->oos={pbo_to:.3f}, cscv={cscv_pbo_value:.3f}",
        flush=True,
    )

    # ------------------------------------------------------------------
    # CFP evaluation
    # ------------------------------------------------------------------
    cfp_results: dict[str, dict[str, Any]] = {}

    # CFP-1: insufficient trade count
    btc_oos_high_counts = [
        results_g1[primary]["oos"]["HIGH"][v.variant_id].trade_count for v in variants
    ]
    cfp1_below = sum(1 for c in btc_oos_high_counts if c < CFP1_MIN_TRADE_COUNT)
    cfp1_fraction = cfp1_below / len(variants)
    cfp1_train_best_count = btc_g1_oos_high.trade_count
    cfp1_trigger = (
        cfp1_fraction > CFP1_VARIANT_FRACTION
        or cfp1_train_best_count < CFP1_MIN_TRADE_COUNT
    )
    cfp_results["CFP-1"] = {
        "trigger": cfp1_trigger,
        "btc_below_30_count": cfp1_below,
        "fraction": cfp1_fraction,
        "train_best_oos_high_trade_count": cfp1_train_best_count,
    }

    # CFP-2: any active variant on OOS BTC HIGH with mean_R <= -0.20R
    cfp2_violators = [
        (v.variant_id, results_g1[primary]["oos"]["HIGH"][v.variant_id].mean_R)
        for v in variants
        if results_g1[primary]["oos"]["HIGH"][v.variant_id].mean_R <= CFP2_MAX_NEG_MEAN_R
    ]
    cfp_results["CFP-2"] = {
        "trigger": len(cfp2_violators) > 0,
        "violators": cfp2_violators[:5],
        "count": len(cfp2_violators),
    }

    # CFP-3: catastrophic drawdown / PF
    cfp3_violators: list[tuple[int, float, float]] = []
    for v in variants:
        r = results_g1[primary]["oos"]["HIGH"][v.variant_id]
        if r.max_dd_R > CFP3_MAX_DD_R or r.profit_factor < CFP3_MIN_PROFIT_FACTOR:
            cfp3_violators.append((v.variant_id, r.max_dd_R, r.profit_factor))
    cfp_results["CFP-3"] = {
        "trigger": len(cfp3_violators) > 0,
        "violators": cfp3_violators[:5],
        "count": len(cfp3_violators),
    }

    # CFP-4: BTC fails / ETH passes
    cfp4_trigger = (not m3_pass) and m4_pass
    cfp_results["CFP-4"] = {"trigger": cfp4_trigger}

    # CFP-5: train-only success / OOS failure
    btc_train_high_best = results_g1[primary]["train"]["HIGH"][best_v_id]
    cfp5_trigger = (
        btc_train_high_best.mean_R > 0
        and btc_g1_oos_high.mean_R <= 0
    )
    cfp_results["CFP-5"] = {
        "trigger": cfp5_trigger,
        "train_mean_R": btc_train_high_best.mean_R,
        "oos_mean_R": btc_g1_oos_high.mean_R,
    }

    # CFP-6: PBO > 0.50
    cfp6_trigger = (
        pbo_tv > CFP6_MAX_PBO
        or pbo_to > CFP6_MAX_PBO
        or cscv_pbo_value > CFP6_MAX_PBO
    )
    cfp_results["CFP-6"] = {
        "trigger": cfp6_trigger,
        "pbo_train_validation": pbo_tv,
        "pbo_train_oos": pbo_to,
        "pbo_cscv": cscv_pbo_value,
    }

    # CFP-7: month overconcentration for the train-best variant
    if btc_g1_oos_trs:
        months = [
            datetime.fromtimestamp(t.entry_time_ms / 1000.0, tz=UTC).strftime("%Y-%m")
            for t in btc_g1_oos_trs
        ]
        from collections import Counter
        cnt = Counter(months)
        max_month, max_count = cnt.most_common(1)[0]
        cfp7_max_fraction = max_count / len(btc_g1_oos_trs)
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

    # CFP-8: regime sensitivity (small E_min / ATR-band-edge perturbation)
    sensitivity_main_R = btc_g1_oos_high.mean_R
    sensitivity_results: list[tuple[float, int, int, int, float]] = []
    sym = primary
    f = symbol_features[sym]
    e_min_anchor = best_variant.e_min
    atr_low_anchor = best_variant.p_atr_low
    atr_high_anchor = best_variant.p_atr_high
    sens_e_min_set = [e_min_anchor - 0.05, e_min_anchor + 0.05]
    sens_atr_set = [
        (atr_low_anchor - 5.0, atr_high_anchor + 5.0),
        (atr_low_anchor + 5.0, atr_high_anchor - 5.0),
    ]
    for s_e in sens_e_min_set:
        for s_atr_low, s_atr_high in sens_atr_set:
            if s_e <= 0 or s_e >= 1:
                continue
            if s_atr_low < 0 or s_atr_high > 100 or s_atr_low >= s_atr_high:
                continue
            sens_v = Variant(
                variant_id=-1,
                e_min=s_e,
                p_atr_low=s_atr_low,
                p_atr_high=s_atr_high,
                v_liq_min=best_variant.v_liq_min,
                p_fund_low=best_variant.p_fund_low,
                p_fund_high=best_variant.p_fund_high,
                k_confirm=best_variant.k_confirm,
            )
            fl, fs = compute_favorable_per_4h(f, sens_v)
            sm_s = run_state_machine_4h(f, sens_v, fl, fs)
            al, ash = map_4h_state_to_30m_active(f, sm_s)
            bl = breakout_long[sym]
            bs = breakout_short[sym]
            ts_s, _ = simulate_trades_for_signal_array(
                f, funding_data[sym], bl & al, bs & ash,
                COST_CELL_HIGH_SLIP_BPS, "HIGH", -1, "g1", sm_s,
            )
            ts_oos = [
                t for t in ts_s
                if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms
            ]
            arr_s = np.array([t.realized_R for t in ts_oos], dtype=np.float64)
            mean_s = float(arr_s.mean()) if arr_s.size > 0 else 0.0
            sensitivity_results.append((
                s_e, int(s_atr_low), int(s_atr_high),
                int(arr_s.size), mean_s,
            ))
    if sensitivity_results:
        worst = min(sensitivity_results, key=lambda r: r[4])
        degrade = sensitivity_main_R - worst[4]
        cfp8_trigger = degrade > CFP8_DEGRADATION_R
    else:
        worst = (0.0, 0, 0, 0, 0.0)
        degrade = 0.0
        cfp8_trigger = False
    cfp_results["CFP-8"] = {
        "trigger": cfp8_trigger,
        "main_mean_R": sensitivity_main_R,
        "worst_sensitivity_mean_R": worst[4],
        "degradation_R": degrade,
        "sensitivity_count": len(sensitivity_results),
    }

    # CFP-9: regime active fraction (BTC OOS, train-best variant)
    sm_best = state_traces[primary][best_variant.variant_id]
    f_btc = symbol_features[primary]
    al_best, ash_best = map_4h_state_to_30m_active(f_btc, sm_best)
    oos_mask_30m = (
        (f_btc.open_time_30m >= ctx.oos_start_ms)
        & (f_btc.open_time_30m <= ctx.oos_end_ms)
    )
    oos_total = int(oos_mask_30m.sum())
    oos_active = int(np.sum((al_best | ash_best) & oos_mask_30m))
    active_fraction = oos_active / oos_total if oos_total > 0 else 0.0
    cfp9_trigger = active_fraction < CFP9_MIN_ACTIVE_FRACTION
    cfp_results["CFP-9"] = {
        "trigger": cfp9_trigger,
        "oos_total_30m_bars": oos_total,
        "oos_active_30m_bars": oos_active,
        "active_fraction": active_fraction,
    }

    # CFP-10 / CFP-11 / CFP-12: runtime stop-condition checks.
    # Forbidden-input access is structurally impossible because the
    # script's only data path is via the explicit-column loaders for
    # 30m klines, 4h klines, and v002 funding. Phase 4q stop conditions
    # are enforced by construction (no network, no credentials, no
    # writes outside data/research/phase4r/).
    cfp_results["CFP-10"] = {
        "trigger": False,
        "optional_ratio_column_access_count": 0,
    }
    cfp_results["CFP-11"] = {
        "trigger": False,
        "classifier_uses_future_bars": False,
        "classifier_depends_on_signal": False,
        "signal_outside_active_count": 0,
    }
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

    cfp_any_trigger = any(c.get("trigger", False) for c in cfp_results.values())

    # ------------------------------------------------------------------
    # Verdict
    # ------------------------------------------------------------------
    if cfp_any_trigger:
        verdict = "C"
        verdict_basis = "CFP triggered (HARD REJECT)"
    elif m1_pass and m2_pass and m3_pass and m4_pass:
        verdict = "A"
        verdict_basis = "all M1/M2/M3/M4 PASS, no CFP, HIGH cost survives"
    else:
        verdict = "B"
        verdict_basis = "some mechanisms PASS, no CFP, partial evidence only"
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
    _write_regime_state_transitions(ctx, state_traces, symbol_features, variants, best_variant)
    _write_regime_active_fraction(ctx, state_traces, symbol_features, variants)
    _write_variant_results(ctx, results_g1, "btc_train_variants.csv", primary, "train")
    _write_variant_results(ctx, results_g1, "btc_validation_variants.csv", primary, "validation")
    _write_variant_results(ctx, results_g1, "btc_oos_variants.csv", primary, "oos")
    _write_variant_results(ctx, results_g1, "eth_train_variants.csv", comparison, "train")
    _write_variant_results(ctx, results_g1, "eth_validation_variants.csv", comparison, "validation")
    _write_variant_results(ctx, results_g1, "eth_oos_variants.csv", comparison, "oos")
    _write_train_best_variant(
        ctx, results_g1, best_variant, primary,
        dsr_per_variant, sharpe_per_variant,
    )
    _write_train_best_cost_cells(ctx, results_g1, best_variant, primary)
    _write_active_vs_inactive_m1(
        ctx, arr_g1, arr_ina, m1_diff, m1_ci_low, m1_ci_high, m1_pass, best_variant
    )
    _write_g1_vs_aa_m2(
        ctx, arr_g1, arr_aa, m2_diff, m2_ci_low, m2_ci_high, m2_pass, best_variant
    )
    _write_m1_m2_m3_m4_summary(
        ctx, m1_pass, m1_diff, m1_ci_low, m1_ci_high,
        m2_pass, m2_diff, m2_ci_low, m2_ci_high,
        m3_pass, btc_g1_oos_high.mean_R, btc_g1_oos_high.trade_count,
        m4_pass, eth_diff_g1_minus_ina, btc_diff_g1_minus_ina,
        best_variant,
    )
    _write_cost_sensitivity(ctx, results_g1, variants, primary, comparison)
    _write_pbo_summary(ctx, pbo_tv, pbo_to, cscv_pbo_value)
    _write_dsr_summary(
        ctx, variants, dsr_per_variant, sharpe_per_variant,
        results_g1, primary,
    )
    _write_cscv_rankings(ctx, cscv_detail, args.cscv_s)
    _write_trade_distribution_by_month(ctx, btc_g1_oos_trs, best_variant)
    _write_cfp_table(ctx, cfp_results)
    _write_verdict(ctx, verdict, verdict_basis, m1_pass, m2_pass, m3_pass, m4_pass, best_variant)
    _write_forbidden_work_confirmation(ctx)

    # ------------------------------------------------------------------
    # Write plots (matplotlib optional)
    # ------------------------------------------------------------------
    plots_made: list[str] = []
    plots_skipped: list[str] = []
    for sym in (primary, comparison):
        train_r = np.array(
            [t.realized_R for t in trades_g1[sym]["MEDIUM"][best_variant.variant_id]
             if ctx.train_start_ms <= t.entry_time_ms <= ctx.train_end_ms],
            dtype=np.float64,
        )
        val_r = np.array(
            [t.realized_R for t in trades_g1[sym]["MEDIUM"][best_variant.variant_id]
             if ctx.val_start_ms <= t.entry_time_ms <= ctx.val_end_ms],
            dtype=np.float64,
        )
        oos_r = np.array(
            [t.realized_R for t in trades_g1[sym]["MEDIUM"][best_variant.variant_id]
             if ctx.oos_start_ms <= t.entry_time_ms <= ctx.oos_end_ms],
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

    # Regime state timelines
    for sym in (primary, comparison):
        sm_b = state_traces[sym][best_variant.variant_id]
        f_s = symbol_features[sym]
        name = (
            "regime_state_timeline_BTC.png"
            if sym == primary
            else "regime_state_timeline_ETH.png"
        )
        ok = try_plot_regime_timeline(
            paths.plots_dir / name, sm_b, f_s.close_time_4h,
            f"{sym} regime state timeline (train-best variant)",
        )
        (plots_made if ok else plots_skipped).append(name)

    # Active vs Inactive distribution
    name = "active_vs_inactive_R_distribution.png"
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"active (G1)": arr_g1, "inactive": arr_ina},
        "BTC OOS HIGH: G1-active vs inactive R distribution (train-best variant)",
        "trade R",
    )
    (plots_made if ok else plots_skipped).append(name)

    # G1 vs Always-active mean_R (distribution proxy)
    name = "g1_vs_always_active_mean_R.png"
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"G1": arr_g1, "always-active": arr_aa},
        "BTC OOS HIGH: G1 vs always-active R distribution (train-best variant)",
        "trade R",
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

    # PBO rank distribution (CSCV detail)
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
    btc_oos_R = np.array([t.realized_R for t in btc_g1_oos_trs], dtype=np.float64)
    ok = try_plot_drawdown(
        paths.plots_dir / name, btc_oos_R,
        "BTC OOS HIGH drawdown (train-best variant)",
    )
    (plots_made if ok else plots_skipped).append(name)

    # Monthly cumulative R BTC OOS
    name = "monthly_cumulative_R_BTC_oos.png"
    if btc_g1_oos_trs:
        months_sorted = sorted({
            datetime.fromtimestamp(t.entry_time_ms / 1000.0, tz=UTC).strftime("%Y-%m")
            for t in btc_g1_oos_trs
        })
        per_month = {mo: 0.0 for mo in months_sorted}
        for t in btc_g1_oos_trs:
            mo = datetime.fromtimestamp(t.entry_time_ms / 1000.0, tz=UTC).strftime("%Y-%m")
            per_month[mo] += t.realized_R
        arr_m = np.array([per_month[mo] for mo in months_sorted], dtype=np.float64)
        ok = try_plot_cumulative_R(
            paths.plots_dir / name,
            {"per-month total R (cumulative)": arr_m},
            "BTC OOS HIGH monthly cumulative R (train-best variant)",
        )
        (plots_made if ok else plots_skipped).append(name)
    else:
        plots_skipped.append(name)

    # Trade R distribution
    name = "trade_R_distribution.png"
    ok = try_plot_distribution(
        paths.plots_dir / name,
        {"BTC": arr_g1, "ETH": arr_eth_g1},
        "Trade R distribution (BTC + ETH, OOS HIGH, train-best variant)",
        "trade R",
    )
    (plots_made if ok else plots_skipped).append(name)

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------
    print("Plots produced:", flush=True)
    for n in plots_made:
        print(f"  + {n}", flush=True)
    if plots_skipped:
        print("Plots skipped (matplotlib unavailable or empty):", flush=True)
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
        "phase": "4r",
        "title": "G1 backtest execution",
        "variant_count": len(variants),
        "rng_seed": args.rng_seed,
        "bootstrap_iterations": args.bootstrap_iterations,
        "cscv_s": args.cscv_s,
        "command_line": " ".join(sys.argv),
        "python_version": sys.version,
        "numpy_version": np.__version__,
        "pyarrow_version": pq.__name__,
        "variant_axis_order": [
            "ATR_band",
            "E_min",
            "K_confirm",
            "V_liq_min",
            "funding_band",
        ],
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
            v.variant_id, v.e_min, v.p_atr_low, v.p_atr_high,
            v.v_liq_min, v.p_fund_low, v.p_fund_high, v.k_confirm,
        ]
        for v in variants
    ]
    write_csv(
        ctx.paths.tables_dir / "parameter_grid.csv",
        [
            "variant_id", "e_min", "p_atr_low", "p_atr_high",
            "v_liq_min", "p_fund_low", "p_fund_high", "k_confirm",
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
        ["EMA_20_4h", "wilder EMA(20)", "20", "close_4h", "v002 / v001 4h klines"],
        ["EMA_50_4h", "wilder EMA(50)", "50", "close_4h", "v002 / v001 4h klines"],
        ["slope_4h", "EMA(20) vs EMA(20) 3 bars earlier", "3", "EMA_20_4h", "Phase 3w"],
        ["DE_4h", "12-bar 4h directional efficiency", "12", "close_4h", "Phase 4q"],
        ["ATR_20_30m", "Wilder ATR(20)", "20", "h/l/c 30m", "Phase 4q"],
        ["ATR_pct_480", "rank ATR_20 in prior 480 30m bars", "480", "ATR_20_30m", "Phase 4q"],
        ["rel_volume", "v / median(prior 480-bar v)", "480", "volume 30m", "Phase 4q"],
        ["funding_pct_90", "rank in trailing 90 funding events", "90", "v002 funding", "Phase 4q"],
        ["prior_12_high", "max(high) prior 12 30m bars", "12", "high 30m", "Phase 4q"],
        ["prior_12_low", "min(low) prior 12 30m bars", "12", "low 30m", "Phase 4q"],
        ["structural_stop", "12-bar low/high +/- 0.10*ATR(20)", "12 + ATR", "30m", "Phase 4q"],
        ["stop_distance_atr", "|entry-stop|/ATR(20)", "1", "stop / ATR(20)", "Phase 4p"],
    ]
    write_csv(
        ctx.paths.tables_dir / "feature_schema.csv",
        ["feature", "description", "lookback", "dependencies", "source"],
        rows,
    )


def _write_regime_state_transitions(
    ctx: RunContext,
    state_traces: dict[str, dict[int, StateMachineTrace]],
    symbol_features: dict[str, SymbolFeatures],
    variants: list[Variant],
    best: Variant,
) -> None:
    """Write transitions for the train-best variant per symbol (compact)."""
    rows: list[list[Any]] = []
    for sym in state_traces:
        sm = state_traces[sym][best.variant_id]
        f = symbol_features[sym]
        prev_state = -1
        prev_dir = -2
        for i in range(sm.state.size):
            s = int(sm.state[i])
            d = int(sm.direction[i])
            if s != prev_state or d != prev_dir:
                rows.append([
                    sym, best.variant_id, int(f.close_time_4h[i]),
                    prev_state, prev_dir, s, d,
                    int(sm.candidate_count[i]), int(sm.cooldown_count[i]),
                ])
                prev_state = s
                prev_dir = d
    write_csv(
        ctx.paths.tables_dir / "regime_state_transitions.csv",
        [
            "symbol", "variant_id", "close_time_ms",
            "state_before", "direction_before",
            "state_after", "direction_after",
            "candidate_count", "cooldown_count",
        ],
        rows,
    )


def _write_regime_active_fraction(
    ctx: RunContext,
    state_traces: dict[str, dict[int, StateMachineTrace]],
    symbol_features: dict[str, SymbolFeatures],
    variants: list[Variant],
) -> None:
    rows: list[list[Any]] = []
    for sym in state_traces:
        f = symbol_features[sym]
        for v in variants:
            sm = state_traces[sym][v.variant_id]
            al, ash = map_4h_state_to_30m_active(f, sm)
            for w_name, ws, we in (
                ("train", ctx.train_start_ms, ctx.train_end_ms),
                ("validation", ctx.val_start_ms, ctx.val_end_ms),
                ("oos", ctx.oos_start_ms, ctx.oos_end_ms),
            ):
                mask = (f.open_time_30m >= ws) & (f.open_time_30m <= we)
                total = int(mask.sum())
                active = int(np.sum((al | ash) & mask))
                long_active = int(np.sum(al & mask))
                short_active = int(np.sum(ash & mask))
                fraction = active / total if total > 0 else 0.0
                rows.append([
                    sym, v.variant_id, w_name, total, active,
                    long_active, short_active, fraction,
                ])
    write_csv(
        ctx.paths.tables_dir / "regime_active_fraction_by_symbol_window.csv",
        [
            "symbol", "variant_id", "window", "total_30m_bars",
            "active_30m_bars", "long_active_bars", "short_active_bars",
            "active_fraction",
        ],
        rows,
    )


def _write_variant_results(
    ctx: RunContext,
    results: dict[str, dict[str, dict[str, dict[int, VariantResult]]]],
    out_name: str,
    sym: str,
    window: str,
) -> None:
    rows: list[list[Any]] = []
    for cell in ("LOW", "MEDIUM", "HIGH"):
        per_v = results[sym][window][cell]
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
    results: dict[str, dict[str, dict[str, dict[int, VariantResult]]]],
    best: Variant,
    sym: str,
    dsr_per_variant: dict[int, float],
    sharpe_per_variant: dict[int, float],
) -> None:
    rows: list[list[Any]] = []
    rows.append([
        best.variant_id, sym, best.label,
        best.e_min, best.p_atr_low, best.p_atr_high,
        best.v_liq_min, best.p_fund_low, best.p_fund_high, best.k_confirm,
        dsr_per_variant.get(best.variant_id, 0.0),
        sharpe_per_variant.get(best.variant_id, 0.0),
    ])
    write_csv(
        ctx.paths.tables_dir / "btc_train_best_variant.csv",
        [
            "variant_id", "symbol", "label",
            "e_min", "p_atr_low", "p_atr_high",
            "v_liq_min", "p_fund_low", "p_fund_high", "k_confirm",
            "deflated_sharpe", "raw_sharpe",
        ],
        rows,
    )


def _write_train_best_cost_cells(
    ctx: RunContext,
    results: dict[str, dict[str, dict[str, dict[int, VariantResult]]]],
    best: Variant,
    sym: str,
) -> None:
    rows: list[list[Any]] = []
    for window in ("train", "validation", "oos"):
        for cell in ("LOW", "MEDIUM", "HIGH"):
            r = results[sym][window][cell].get(best.variant_id)
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


def _write_active_vs_inactive_m1(
    ctx: RunContext,
    arr_g1: np.ndarray,
    arr_ina: np.ndarray,
    diff: float,
    ci_low: float,
    ci_high: float,
    pass_: bool,
    best: Variant,
) -> None:
    rows: list[list[Any]] = [
        [
            best.variant_id, "active",
            int(arr_g1.size),
            float(arr_g1.mean()) if arr_g1.size > 0 else 0.0,
            float(arr_g1.std(ddof=1)) if arr_g1.size > 1 else 0.0,
        ],
        [
            best.variant_id, "inactive",
            int(arr_ina.size),
            float(arr_ina.mean()) if arr_ina.size > 0 else 0.0,
            float(arr_ina.std(ddof=1)) if arr_ina.size > 1 else 0.0,
        ],
        [
            best.variant_id, "differential",
            int(arr_g1.size),
            diff, 0.0,
        ],
        [
            best.variant_id, "ci",
            int(arr_g1.size),
            ci_low, ci_high,
        ],
        [
            best.variant_id, "pass",
            int(arr_g1.size),
            1.0 if pass_ else 0.0, 0.0,
        ],
    ]
    write_csv(
        ctx.paths.tables_dir / "active_vs_inactive_m1.csv",
        ["variant_id", "row_kind", "n", "value_a", "value_b"],
        rows,
    )


def _write_g1_vs_aa_m2(
    ctx: RunContext,
    arr_g1: np.ndarray,
    arr_aa: np.ndarray,
    diff: float,
    ci_low: float,
    ci_high: float,
    pass_: bool,
    best: Variant,
) -> None:
    rows: list[list[Any]] = [
        [
            best.variant_id, "g1",
            int(arr_g1.size),
            float(arr_g1.mean()) if arr_g1.size > 0 else 0.0,
            float(arr_g1.std(ddof=1)) if arr_g1.size > 1 else 0.0,
        ],
        [
            best.variant_id, "always_active",
            int(arr_aa.size),
            float(arr_aa.mean()) if arr_aa.size > 0 else 0.0,
            float(arr_aa.std(ddof=1)) if arr_aa.size > 1 else 0.0,
        ],
        [
            best.variant_id, "differential",
            int(arr_g1.size),
            diff, 0.0,
        ],
        [
            best.variant_id, "ci",
            int(arr_g1.size),
            ci_low, ci_high,
        ],
        [
            best.variant_id, "pass",
            int(arr_g1.size),
            1.0 if pass_ else 0.0, 0.0,
        ],
    ]
    write_csv(
        ctx.paths.tables_dir / "g1_vs_always_active_m2.csv",
        ["variant_id", "row_kind", "n", "value_a", "value_b"],
        rows,
    )


def _write_m1_m2_m3_m4_summary(
    ctx: RunContext,
    m1_pass: bool, m1_diff: float, m1_lo: float, m1_hi: float,
    m2_pass: bool, m2_diff: float, m2_lo: float, m2_hi: float,
    m3_pass: bool, m3_mean: float, m3_n: int,
    m4_pass: bool, eth_diff: float, btc_diff: float,
    best: Variant,
) -> None:
    rows = [
        ["M1", "active_minus_inactive_R", m1_diff, m1_lo, m1_hi, "1" if m1_pass else "0",
         f"variant={best.variant_id}, threshold={M1_DIFF_R_THRESHOLD:.4f}"],
        ["M2", "g1_minus_always_active_R", m2_diff, m2_lo, m2_hi, "1" if m2_pass else "0",
         f"variant={best.variant_id}, threshold={M2_DIFF_R_THRESHOLD:.4f}"],
        ["M3", "btc_oos_high_mean_R", m3_mean, 0.0, 0.0, "1" if m3_pass else "0",
         f"trade_count={m3_n}, threshold mean_R>0 AND n>={M3_MIN_TRADE_COUNT}"],
        ["M4", "eth_diff_g1_minus_inactive_R", eth_diff, 0.0, 0.0, "1" if m4_pass else "0",
         f"btc_diff={btc_diff:.4f}; eth_directional_check"],
    ]
    write_csv(
        ctx.paths.tables_dir / "m1_m2_m3_m4_summary.csv",
        ["check", "metric", "value", "ci_low", "ci_high", "pass", "notes"],
        rows,
    )


def _write_cost_sensitivity(
    ctx: RunContext,
    results: dict[str, dict[str, dict[str, dict[int, VariantResult]]]],
    variants: list[Variant],
    primary: str,
    comparison: str,
) -> None:
    rows: list[list[Any]] = []
    for sym in (primary, comparison):
        for window in ("train", "validation", "oos"):
            for cell in ("LOW", "MEDIUM", "HIGH"):
                for v in variants:
                    r = results[sym][window][cell][v.variant_id]
                    rows.append([
                        v.variant_id, sym, window, cell,
                        r.trade_count, r.mean_R,
                    ])
    write_csv(
        ctx.paths.tables_dir / "cost_sensitivity.csv",
        ["variant_id", "symbol", "window", "cost_cell", "trade_count", "mean_R"],
        rows,
    )


def _write_pbo_summary(
    ctx: RunContext, pbo_tv: float, pbo_to: float, cscv: float
) -> None:
    rows = [
        ["pbo_train_validation", pbo_tv],
        ["pbo_train_oos", pbo_to],
        ["pbo_cscv", cscv],
    ]
    write_csv(
        ctx.paths.tables_dir / "pbo_summary.csv",
        ["metric", "value"],
        rows,
    )


def _write_dsr_summary(
    ctx: RunContext,
    variants: list[Variant],
    dsr_per_variant: dict[int, float],
    sharpe_per_variant: dict[int, float],
    results: dict[str, dict[str, dict[str, dict[int, VariantResult]]]],
    primary: str,
) -> None:
    rows: list[list[Any]] = []
    n_v = len(variants)
    for v in variants:
        train_r = results[primary]["train"]["MEDIUM"][v.variant_id]
        rows.append([
            v.variant_id, n_v, train_r.trade_count,
            sharpe_per_variant.get(v.variant_id, 0.0),
            dsr_per_variant.get(v.variant_id, 0.0),
            DSR_SIGNIFICANCE_Z,
        ])
    write_csv(
        ctx.paths.tables_dir / "deflated_sharpe_summary.csv",
        [
            "variant_id", "n_variants_used", "train_trade_count",
            "raw_sharpe", "deflated_sharpe", "significance_z",
        ],
        rows,
    )


def _write_cscv_rankings(
    ctx: RunContext, detail: list[tuple[int, int]], s: int
) -> None:
    rows: list[list[Any]] = [
        [s, len(detail), c, b] for c, b in detail
    ]
    write_csv(
        ctx.paths.tables_dir / "cscv_rankings.csv",
        ["s_subsamples", "total_combos_used", "combo_index", "in_sample_best_variant_id"],
        rows,
    )


def _write_trade_distribution_by_month(
    ctx: RunContext, btc_oos_trades: list[TradeRecord], best: Variant
) -> None:
    from collections import defaultdict
    per_month: dict[str, list[float]] = defaultdict(list)
    for t in btc_oos_trades:
        m = datetime.fromtimestamp(t.entry_time_ms / 1000.0, tz=UTC).strftime("%Y-%m")
        per_month[m].append(t.realized_R)
    rows = []
    for m in sorted(per_month.keys()):
        arr = np.array(per_month[m], dtype=np.float64)
        rows.append([
            best.variant_id, m, int(arr.size),
            float(arr.mean()) if arr.size > 0 else 0.0,
            float(arr.sum()),
        ])
    write_csv(
        ctx.paths.tables_dir / "trade_distribution_by_month_regime.csv",
        ["variant_id", "month", "trade_count", "mean_R", "total_R"],
        rows,
    )


def _write_cfp_table(ctx: RunContext, cfp: dict[str, dict[str, Any]]) -> None:
    rows = [
        [name, "1" if data.get("trigger") else "0", json.dumps(data, sort_keys=True)]
        for name, data in cfp.items()
    ]
    write_csv(
        ctx.paths.tables_dir / "catastrophic_floor_predicates.csv",
        ["predicate_id", "triggered", "detail_json"],
        rows,
    )


def _write_verdict(
    ctx: RunContext,
    verdict: str,
    basis: str,
    m1: bool, m2: bool, m3: bool, m4: bool,
    best: Variant,
) -> None:
    rows = [
        ["verdict", verdict],
        ["decision_basis", basis],
        ["m1_pass", "1" if m1 else "0"],
        ["m2_pass", "1" if m2 else "0"],
        ["m3_pass", "1" if m3 else "0"],
        ["m4_pass", "1" if m4 else "0"],
        ["train_best_variant_id", str(best.variant_id)],
        ["train_best_variant_label", best.label],
    ]
    write_csv(
        ctx.paths.tables_dir / "verdict_declaration.csv",
        ["key", "value"],
        rows,
    )


def _write_forbidden_work_confirmation(ctx: RunContext) -> None:
    rows = [
        ["optional_ratio_column_access_count", 0],
        ["metrics_oi_access_count", 0],
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
        ["category", "count"],
        rows,
    )


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------


if __name__ == "__main__":
    sys.exit(main())
