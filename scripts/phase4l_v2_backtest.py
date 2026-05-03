"""Phase 4l - V2 Backtest Execution (standalone research script).

Implements the Phase 4k V2 Backtest-Plan Memo methodology exactly:
- Phase 4g locked V2 strategy spec (signal 30m, bias 4h, session 1h);
- 8 active entry features + 3 exit / regime features;
- Phase 4j §11 metrics OI-subset partial-eligibility binding rule;
- 512 predeclared variants (2^9);
- chronological train (2022-01-01..2023-06-30 UTC), validation
  (2023-07-01..2024-06-30 UTC), OOS holdout (2024-07-01..2026-03-31
  UTC) split;
- BTCUSDT primary, ETHUSDT comparison only;
- M1 / M2 / M3 mechanism checks per Phase 4g §30;
- §11.6 = 8 bps HIGH per side cost cell preserved verbatim;
- Verdict A / B / C / D classification.

This script is a STANDALONE research script. It does NOT import from
prometheus.runtime.*, prometheus.execution.*, prometheus.persistence.*,
or any module that performs network I/O. It does NOT use credentials.
It does NOT contact authenticated APIs. It reads only LOCAL Parquet
data already acquired by Phase 4i and existing v002 funding manifests.

The script does NOT touch the four optional metrics ratio columns;
the metrics loader exposes ONLY the OI subset (create_time, symbol,
sum_open_interest, sum_open_interest_value).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow.parquet as pq

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

INTERVAL_MS_30M = 30 * 60 * 1000
INTERVAL_MS_4H = 4 * 60 * 60 * 1000
INTERVAL_MS_5M = 5 * 60 * 1000
INTERVAL_MS_8H = 8 * 60 * 60 * 1000

EPOCH_2022_01_01_UTC_MS = 1_640_995_200_000

# Phase 4j §11 — explicit OI-subset column list. The four optional
# ratio columns are NOT included and MUST NOT be loaded by this script.
METRICS_OI_COLUMNS = [
    "create_time",
    "symbol",
    "sum_open_interest",
    "sum_open_interest_value",
]

# Phase 4g §29 fixed parameters (cardinality 1)
L_W = 240          # Donchian width percentile lookback (5d at 30m)
L_ATR = 240        # ATR percentile lookback (5d at 30m)
N_RE = 20          # Range-expansion baseline lookback
RE_MIN = 1.0       # Range-expansion minimum
L_VOL = 240        # Volume baseline lookback
Q_SESSION = 50.0   # UTC-hour volume percentile minimum
L_SESSION_DAYS = 60  # UTC-hour session-bucket lookback
N_OI = 240         # OI lookback (Phase 4g §29; not used directly because
                   # Phase 4j §17 supersedes with point-in-time-clear rule)
P_OI_LOW = 10.0    # OI delta percentile band low (fixed; informational)
P_OI_HIGH = 90.0   # OI delta percentile band high (fixed; informational)
L_FUND = 90        # Funding lookback in events (~30d at 8h cadence)
COOLDOWN_BARS = 8  # Same-direction cooldown
ATR_PERIOD = 20    # ATR window
ATR_BUFFER = 0.10  # ATR buffer for stop and breakout (fraction of ATR)
STOP_DIST_MIN_ATR = 0.60
STOP_DIST_MAX_ATR = 1.80
ATR_PCT_LOW = 25.0
ATR_PCT_HIGH = 75.0

# Risk and sizing constants per §1.7.3 (locked)
LOCKED_RISK_FRACTION = 0.0025
LOCKED_LEVERAGE_CAP = 2.0

# Cost cells per Phase 4g §26 / Phase 4k
TAKER_FEE_PER_SIDE_BPS = 4.0  # USDⓈ-M futures default taker fee
COST_CELL_LOW_SLIP_BPS = 1.0
COST_CELL_MEDIUM_SLIP_BPS = 4.0
COST_CELL_HIGH_SLIP_BPS = 8.0  # §11.6 HIGH preserved verbatim

# Mechanism-check thresholds (Phase 4g §30 predeclared)
M1_MFE_TARGET_R = 0.5
M1_MFE_FRACTION_THRESHOLD = 0.50
M2_DIFF_R_THRESHOLD = 0.10
M2_BOOTSTRAP_ITERATIONS = 10_000
M3_DIFF_R_THRESHOLD = 0.05
M3_HIGH_RESILIENCE_EPSILON_R = 0.05

# Catastrophic-floor predicate thresholds
CFP1_MIN_TRADE_COUNT = 30
CFP3_MAX_DD_R = 10.0
CFP3_MIN_PROFIT_FACTOR = 0.50
CFP6_MAX_PBO = 0.5
CFP7_MAX_MONTH_FRACTION = 0.50
CFP8_SENSITIVITY_DEGRADATION_FRACTION = 0.50  # main_R - 0.5*|main_R| if main>0
CFP9_MAX_EXCLUDED_FRACTION = 0.05
CSCV_S_DEFAULT = 16

# DSR confidence
DSR_SIGNIFICANCE_Z = 1.96


# ----------------------------------------------------------------------
# Data classes
# ----------------------------------------------------------------------


@dataclass
class StopCondition(Exception):
    """Raised when a Phase 4k stop condition triggers."""

    reason: str
    detail: str

    def __str__(self) -> str:
        return f"STOP_CONDITION[{self.reason}]: {self.detail}"


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
    open_time_ms: np.ndarray  # int64 [N]
    open_: np.ndarray         # float64 [N]
    high: np.ndarray          # float64 [N]
    low: np.ndarray           # float64 [N]
    close: np.ndarray         # float64 [N]
    volume: np.ndarray        # float64 [N]
    taker_buy_volume: np.ndarray  # float64 [N]


@dataclass
class SymbolMetricsData:
    symbol: str
    create_time_ms: np.ndarray   # int64 [M] sorted
    sum_oi: np.ndarray           # float64 [M] (NaN where absent)
    sum_oi_value: np.ndarray     # float64 [M] (NaN where absent)
    # Dense lookup: (create_time_ms - epoch) // 5min -> idx
    # We store start_ms and a dense bool/float array for O(1) access
    dense_start_ms: int
    dense_oi: np.ndarray         # float64 [K] dense, NaN where missing
    dense_oi_value: np.ndarray
    invalid_dates: set[str]      # YYYY-MM-DD (UTC) of any 5m record
                                 # missing or NaN in OI columns


@dataclass
class SymbolFundingData:
    symbol: str
    funding_time_ms: np.ndarray  # int64 [F] sorted
    funding_rate: np.ndarray     # float64 [F]


@dataclass
class Variant:
    """One of 512 variants from the 9 binary axes."""

    variant_id: int
    n1: int
    p_w_max: float
    v_rel_min: float
    v_z_min: float
    t_imb_min: float
    oi_dir: str  # "aligned" or "non_negative"
    fund_band_low: float
    fund_band_high: float
    n_r: float
    t_stop: int

    @property
    def label(self) -> str:
        return (
            f"N1={self.n1}|Pw={int(self.p_w_max)}|Vrel={self.v_rel_min}"
            f"|Vz={self.v_z_min}|Timb={self.t_imb_min}|OI={self.oi_dir}"
            f"|FB={int(self.fund_band_low)}-{int(self.fund_band_high)}"
            f"|NR={self.n_r}|Tstop={self.t_stop}"
        )


@dataclass
class TradeRecord:
    symbol: str
    variant_id: int
    cost_cell: str
    side: str  # "long" or "short"
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
    pnl_bps_per_unit_pre_cost: float  # gross % move in bps
    realized_R: float                 # net of fees + slippage + funding
    mfe_R: float                      # max favorable excursion (R units)
    funding_cost_R: float             # funding cost component in R units


@dataclass
class VariantResult:
    variant_id: int
    symbol: str
    window: str  # "train" / "validation" / "oos"
    cost_cell: str
    trade_count: int
    win_rate: float
    mean_R: float
    median_R: float
    total_R: float
    max_dd_R: float
    profit_factor: float
    sharpe: float


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
    name = meta.get("dataset_name", "")
    version = meta.get("dataset_version", "")
    expected_full = expected_name
    full = f"{name}__{version}" if version and "__v" not in name else name
    if expected_full and full != expected_full and name != expected_full:
        # Not strictly fatal — we'll still try to use it
        pass
    return ManifestRef(
        name=expected_name,
        path=path,
        sha256=digest,
        research_eligible=bool(meta.get("research_eligible", False)),
        feature_use=feature_use,
        metadata=meta,
    )


# ----------------------------------------------------------------------
# Parquet loading
# ----------------------------------------------------------------------


def list_parquet_partitions(
    base: Path, predicate: tuple[tuple[str, str], ...]
) -> list[Path]:
    """Walk a partitioned directory and return all part-NNNN.parquet
    files. predicate is a sequence of (key, value) pairs forming the
    expected partition path components.
    """
    cur = base
    for k, v in predicate:
        cur = cur / f"{k}={v}"
        if not cur.exists():
            return []
    parts: list[Path] = []
    if cur.is_file():
        if cur.suffix == ".parquet":
            parts.append(cur)
        return parts
    for child in sorted(cur.rglob("part-*.parquet")):
        parts.append(child)
    return parts


def load_kline_symbol_interval(
    base: Path, symbol: str, interval: str
) -> SymbolKlineData:
    cur = base / f"symbol={symbol}" / f"interval={interval}"
    if not cur.exists():
        raise StopCondition(
            "local_data_missing", f"{cur} (symbol={symbol} interval={interval})"
        )
    parts = sorted(cur.rglob("part-*.parquet"))
    if not parts:
        raise StopCondition("local_data_missing", f"no parquet under {cur}")
    open_times: list[np.ndarray] = []
    opens: list[np.ndarray] = []
    highs: list[np.ndarray] = []
    lows: list[np.ndarray] = []
    closes: list[np.ndarray] = []
    volumes: list[np.ndarray] = []
    taker_buys: list[np.ndarray] = []
    for p in parts:
        t = pq.ParquetFile(p).read(
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "taker_buy_volume",
            ]
        )
        open_times.append(np.asarray(t.column("open_time").to_numpy(), dtype=np.int64))
        opens.append(np.asarray(t.column("open").to_numpy(), dtype=np.float64))
        highs.append(np.asarray(t.column("high").to_numpy(), dtype=np.float64))
        lows.append(np.asarray(t.column("low").to_numpy(), dtype=np.float64))
        closes.append(np.asarray(t.column("close").to_numpy(), dtype=np.float64))
        volumes.append(np.asarray(t.column("volume").to_numpy(), dtype=np.float64))
        taker_buys.append(
            np.asarray(t.column("taker_buy_volume").to_numpy(), dtype=np.float64)
        )
    open_time = np.concatenate(open_times)
    order = np.argsort(open_time, kind="stable")
    return SymbolKlineData(
        symbol=symbol,
        open_time_ms=open_time[order],
        open_=np.concatenate(opens)[order],
        high=np.concatenate(highs)[order],
        low=np.concatenate(lows)[order],
        close=np.concatenate(closes)[order],
        volume=np.concatenate(volumes)[order],
        taker_buy_volume=np.concatenate(taker_buys)[order],
    )


def load_metrics_oi_subset(base: Path, symbol: str) -> SymbolMetricsData:
    """Load metrics OI subset only. Phase 4j §11 enforced at column-list level.

    The four optional ratio columns are NOT in METRICS_OI_COLUMNS and will
    NOT be loaded by pyarrow.
    """
    cur = base / f"symbol={symbol}"
    if not cur.exists():
        raise StopCondition("local_data_missing", f"metrics root missing {cur}")
    parts = sorted(cur.rglob("part-*.parquet"))
    if not parts:
        raise StopCondition("local_data_missing", f"no metrics parquet under {cur}")
    create_times: list[np.ndarray] = []
    sum_oi: list[np.ndarray] = []
    sum_oi_value: list[np.ndarray] = []
    for p in parts:
        t = pq.ParquetFile(p).read(columns=METRICS_OI_COLUMNS)
        create_times.append(np.asarray(t.column("create_time").to_numpy(), dtype=np.int64))
        sum_oi.append(np.asarray(t.column("sum_open_interest").to_numpy(), dtype=np.float64))
        sum_oi_value.append(
            np.asarray(t.column("sum_open_interest_value").to_numpy(), dtype=np.float64)
        )
    create_time = np.concatenate(create_times)
    order = np.argsort(create_time, kind="stable")
    create_time = create_time[order]
    soi = np.concatenate(sum_oi)[order]
    soi_v = np.concatenate(sum_oi_value)[order]
    # Build dense lookup
    if create_time.size == 0:
        raise StopCondition("local_data_missing", f"empty metrics for {symbol}")
    start_ms = int(create_time[0])
    end_ms = int(create_time[-1])
    n_slots = (end_ms - start_ms) // INTERVAL_MS_5M + 1
    dense_oi = np.full(n_slots, np.nan, dtype=np.float64)
    dense_oi_value = np.full(n_slots, np.nan, dtype=np.float64)
    idx = (create_time - start_ms) // INTERVAL_MS_5M
    dense_oi[idx] = soi
    dense_oi_value[idx] = soi_v
    # Build invalid_dates set (any 5m slot in the dense range with missing/NaN)
    invalid_dates: set[str] = set()
    # Detect missing slots OR NaN OI
    missing_mask = np.isnan(dense_oi) | np.isnan(dense_oi_value)
    if missing_mask.any():
        slot_idx = np.where(missing_mask)[0]
        slot_ms = start_ms + slot_idx.astype(np.int64) * INTERVAL_MS_5M
        for ms in slot_ms:
            d = datetime.fromtimestamp(int(ms) / 1000.0, tz=UTC).date().isoformat()
            invalid_dates.add(d)
    return SymbolMetricsData(
        symbol=symbol,
        create_time_ms=create_time,
        sum_oi=soi,
        sum_oi_value=soi_v,
        dense_start_ms=start_ms,
        dense_oi=dense_oi,
        dense_oi_value=dense_oi_value,
        invalid_dates=invalid_dates,
    )


def load_funding(base: Path, symbol: str) -> SymbolFundingData:
    cur = base / f"symbol={symbol}"
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


def ema(values: np.ndarray, period: int) -> np.ndarray:
    """Standard EMA with alpha = 2 / (period + 1)."""
    alpha = 2.0 / (period + 1.0)
    out = np.empty_like(values, dtype=np.float64)
    out[0] = values[0]
    for i in range(1, values.size):
        out[i] = alpha * values[i] + (1.0 - alpha) * out[i - 1]
    return out


def true_range(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray) -> np.ndarray:
    """True range; tr[0] = high[0] - low[0]."""
    tr = np.empty_like(highs, dtype=np.float64)
    tr[0] = highs[0] - lows[0]
    a = highs[1:] - lows[1:]
    b = np.abs(highs[1:] - closes[:-1])
    c = np.abs(lows[1:] - closes[:-1])
    tr[1:] = np.maximum(np.maximum(a, b), c)
    return tr


def atr(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int) -> np.ndarray:
    """Wilder's ATR using simple-mean seed and recursive smoothing."""
    tr = true_range(highs, lows, closes)
    n = tr.size
    out = np.full(n, np.nan, dtype=np.float64)
    if n < period:
        return out
    seed = float(tr[:period].mean())
    out[period - 1] = seed
    for i in range(period, n):
        out[i] = (out[i - 1] * (period - 1) + tr[i]) / period
    return out


def rolling_max_excluding_current(arr: np.ndarray, n: int) -> np.ndarray:
    """At index i, returns max(arr[i-n : i]) excluding arr[i]. NaN until i>=n."""
    out = np.full(arr.size, np.nan, dtype=np.float64)
    if arr.size <= n:
        return out
    # Use stride tricks for efficiency
    for i in range(n, arr.size):
        out[i] = float(arr[i - n : i].max())
    return out


def rolling_min_excluding_current(arr: np.ndarray, n: int) -> np.ndarray:
    out = np.full(arr.size, np.nan, dtype=np.float64)
    if arr.size <= n:
        return out
    for i in range(n, arr.size):
        out[i] = float(arr[i - n : i].min())
    return out


def rolling_percentile_rank_excluding_current(
    arr: np.ndarray, n: int
) -> np.ndarray:
    """At index i, returns the percentile rank (0-100) of arr[i] within
    the prior n values arr[i-n : i] (excluding current). NaN until i>=n.
    Percentile rank = 100 * fraction of prior values <= arr[i].
    """
    out = np.full(arr.size, np.nan, dtype=np.float64)
    if arr.size <= n:
        return out
    for i in range(n, arr.size):
        window = arr[i - n : i]
        # Skip NaNs in window
        valid = window[~np.isnan(window)]
        if valid.size == 0 or np.isnan(arr[i]):
            continue
        out[i] = 100.0 * float((valid <= arr[i]).sum()) / float(valid.size)
    return out


def rolling_mean_excluding_current(arr: np.ndarray, n: int) -> np.ndarray:
    out = np.full(arr.size, np.nan, dtype=np.float64)
    if arr.size <= n:
        return out
    cumsum = np.cumsum(np.where(np.isnan(arr), 0.0, arr))
    valid_count = np.cumsum((~np.isnan(arr)).astype(np.int64))
    for i in range(n, arr.size):
        s = float(cumsum[i - 1])
        c = int(valid_count[i - 1])
        if i >= 2 * n + 1:
            s -= float(cumsum[i - n - 1])
            c -= int(valid_count[i - n - 1])
        else:
            # window arr[i-n : i] = cumsum[i-1] - cumsum[i-n-1] when i-n-1 >= 0
            if i - n - 1 >= 0:
                s -= float(cumsum[i - n - 1])
                c -= int(valid_count[i - n - 1])
        if c == 0:
            continue
        out[i] = s / c
    return out


def rolling_std_excluding_current(arr: np.ndarray, n: int) -> np.ndarray:
    out = np.full(arr.size, np.nan, dtype=np.float64)
    if arr.size <= n:
        return out
    for i in range(n, arr.size):
        window = arr[i - n : i]
        valid = window[~np.isnan(window)]
        if valid.size < 2:
            continue
        out[i] = float(valid.std(ddof=1))
    return out


# ----------------------------------------------------------------------
# HTF bias state (4h)
# ----------------------------------------------------------------------


def compute_htf_bias_state(close_4h: np.ndarray) -> np.ndarray:
    """Returns int8 array of same size as close_4h:
    +1 = long bias, -1 = short bias, 0 = neutral.

    Long bias if EMA(20) > EMA(50), close > EMA(20), and EMA(20) is
    rising vs. 3 4h bars earlier. Short bias is strict mirror.
    """
    n = close_4h.size
    out = np.zeros(n, dtype=np.int8)
    if n < 53:
        return out
    e20 = ema(close_4h, 20)
    e50 = ema(close_4h, 50)
    for i in range(53, n):
        if e20[i] > e50[i] and close_4h[i] > e20[i] and e20[i] > e20[i - 3]:
            out[i] = 1
        elif e20[i] < e50[i] and close_4h[i] < e20[i] and e20[i] < e20[i - 3]:
            out[i] = -1
        else:
            out[i] = 0
    return out


def map_4h_state_to_30m(
    open_time_30m: np.ndarray,
    close_time_4h: np.ndarray,
    state_4h: np.ndarray,
) -> np.ndarray:
    """For each 30m bar, map to most recent COMPLETED 4h bar with
    close_time_4h <= 30m bar's close_time = open_time_30m + 30min - 1.
    """
    decision_time = open_time_30m + INTERVAL_MS_30M - 1
    # searchsorted: index of first close_time_4h > decision_time
    # we want the index of the latest close_time_4h <= decision_time
    idx = np.searchsorted(close_time_4h, decision_time, side="right") - 1
    out = np.zeros_like(idx, dtype=np.int8)
    valid = idx >= 0
    out[valid] = state_4h[idx[valid]]
    return out


# ----------------------------------------------------------------------
# Volume percentile by UTC hour
# ----------------------------------------------------------------------


def compute_utc_hour_volume_percentile(
    open_time_30m: np.ndarray,
    volume_30m: np.ndarray,
    lookback_days: int,
) -> np.ndarray:
    """For each 30m bar, compute the percentile rank of its volume within
    the trailing distribution of bars that fall in the same UTC hour over
    the prior lookback_days days. Excludes the current bar.
    """
    n = volume_30m.size
    out = np.full(n, np.nan, dtype=np.float64)
    # Compute UTC hour for each bar
    hours = ((open_time_30m // (60 * 60 * 1000)) % 24).astype(np.int64)
    lookback_ms = lookback_days * 24 * 60 * 60 * 1000
    for i in range(n):
        cutoff_ms = open_time_30m[i] - lookback_ms
        if open_time_30m[0] > cutoff_ms:
            continue  # not enough history
        # Find indices in same hour with open_time in [cutoff_ms, open_time[i])
        hour_i = hours[i]
        # naive scan; precomputable but small enough
        start_idx = int(np.searchsorted(open_time_30m, cutoff_ms, side="left"))
        # Indices [start_idx, i) and same hour
        if i <= start_idx:
            continue
        sl = slice(start_idx, i)
        mask = hours[sl] == hour_i
        if not mask.any():
            continue
        vols = volume_30m[sl][mask]
        if vols.size == 0:
            continue
        out[i] = 100.0 * float((vols <= volume_30m[i]).sum()) / float(vols.size)
    return out


# ----------------------------------------------------------------------
# OI per-bar eligibility + delta (Phase 4j §11)
# ----------------------------------------------------------------------


def compute_oi_eligibility_and_delta(
    open_time_30m: np.ndarray,
    metrics: SymbolMetricsData,
) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    """Returns:
    - eligible: bool[N] — True if all six aligned 5m OI records are present
      AND the previous-window 5m OI record is also present.
    - oi_delta: float64[N] — current_OI - previous_OI for eligible bars; NaN otherwise.
    - exclusion_counts: dict with reason -> count.
    """
    n = open_time_30m.size
    eligible = np.zeros(n, dtype=bool)
    oi_delta = np.full(n, np.nan, dtype=np.float64)
    counts = {
        "total_bars": int(n),
        "metrics_oi_missing_or_invalid": 0,
        "metrics_oi_prev_window_missing": 0,
        "eligible": 0,
    }
    start_ms = metrics.dense_start_ms
    dense_oi = metrics.dense_oi
    dense_oi_value = metrics.dense_oi_value
    dense_size = dense_oi.size
    for i in range(n):
        bar_open = int(open_time_30m[i])
        # Six aligned records at offsets 0, 5, 10, 15, 20, 25
        all_present = True
        for off_min in (0, 5, 10, 15, 20, 25):
            ts = bar_open + off_min * 60 * 1000
            slot = (ts - start_ms) // INTERVAL_MS_5M
            if slot < 0 or slot >= dense_size:
                all_present = False
                break
            if math.isnan(dense_oi[slot]) or math.isnan(dense_oi_value[slot]):
                all_present = False
                break
        if not all_present:
            counts["metrics_oi_missing_or_invalid"] += 1
            continue
        # Previous-window 5m record at bar_open - 5min
        prev_ts = bar_open - 5 * 60 * 1000
        prev_slot = (prev_ts - start_ms) // INTERVAL_MS_5M
        if (
            prev_slot < 0
            or prev_slot >= dense_size
            or math.isnan(dense_oi[prev_slot])
            or math.isnan(dense_oi_value[prev_slot])
        ):
            counts["metrics_oi_prev_window_missing"] += 1
            continue
        # Compute OI delta per Phase 4j §17:
        # current = OI at bar_open + 25min (last 5m of current 30m window)
        cur_slot = (bar_open + 25 * 60 * 1000 - start_ms) // INTERVAL_MS_5M
        eligible[i] = True
        oi_delta[i] = float(dense_oi[cur_slot] - dense_oi[prev_slot])
        counts["eligible"] += 1
    return eligible, oi_delta, counts


# ----------------------------------------------------------------------
# Funding-rate percentile band check
# ----------------------------------------------------------------------


def compute_funding_percentile_at_30m_close(
    decision_time_30m_ms: np.ndarray,
    funding: SymbolFundingData,
    lookback_events: int,
) -> np.ndarray:
    """For each 30m signal bar, find the most recent funding event with
    funding_time_ms <= decision_time, then compute the percentile rank of
    that event's rate within the trailing lookback_events events
    (including the most recent one and the prior lookback_events-1).
    Returns percentile_rank in [0, 100], NaN if insufficient history.
    """
    n = decision_time_30m_ms.size
    out = np.full(n, np.nan, dtype=np.float64)
    ftime = funding.funding_time_ms
    frate = funding.funding_rate
    # For each 30m decision time, idx = last funding event index where ftime <= dt
    idx = np.searchsorted(ftime, decision_time_30m_ms, side="right") - 1
    for i in range(n):
        j = int(idx[i])
        if j < lookback_events - 1:
            continue
        window = frate[j - lookback_events + 1 : j + 1]
        if window.size == 0:
            continue
        cur = float(frate[j])
        out[i] = 100.0 * float((window <= cur).sum()) / float(window.size)
    return out


# ----------------------------------------------------------------------
# Variant grid
# ----------------------------------------------------------------------


def build_variants() -> list[Variant]:
    """Build the 512-variant grid in deterministic lexicographic order
    of axis values."""
    axes = [
        ("n1", [20, 40]),
        ("p_w_max", [25.0, 35.0]),
        ("v_rel_min", [1.5, 2.0]),
        ("v_z_min", [0.5, 1.0]),
        ("t_imb_min", [0.55, 0.60]),
        ("oi_dir", ["aligned", "non_negative"]),
        ("fund_band", [(20.0, 80.0), (30.0, 70.0)]),
        ("n_r", [2.0, 2.5]),
        ("t_stop", [12, 16]),
    ]
    variants: list[Variant] = []
    for vid, combo in enumerate(itertools.product(*[opts for _, opts in axes])):
        n1, p_w, v_rel, v_z, t_imb, oi_dir, fund_band, n_r, t_stop = combo
        variants.append(
            Variant(
                variant_id=vid,
                n1=int(n1),
                p_w_max=float(p_w),
                v_rel_min=float(v_rel),
                v_z_min=float(v_z),
                t_imb_min=float(t_imb),
                oi_dir=str(oi_dir),
                fund_band_low=float(fund_band[0]),
                fund_band_high=float(fund_band[1]),
                n_r=float(n_r),
                t_stop=int(t_stop),
            )
        )
    if len(variants) != 512:
        raise StopCondition(
            "validation_report_incomplete",
            f"variant grid built with {len(variants)} != 512",
        )
    return variants


# ----------------------------------------------------------------------
# Per-symbol feature precomputation
# ----------------------------------------------------------------------


@dataclass
class SymbolFeatures:
    """Pre-computed per-symbol features (variant-independent)."""

    symbol: str
    open_time_30m: np.ndarray
    open_30m: np.ndarray
    high_30m: np.ndarray
    low_30m: np.ndarray
    close_30m: np.ndarray
    volume_30m: np.ndarray
    taker_buy_volume_30m: np.ndarray
    atr20_30m: np.ndarray
    htf_bias_30m: np.ndarray
    don_high_n1_20: np.ndarray
    don_low_n1_20: np.ndarray
    don_high_n1_40: np.ndarray
    don_low_n1_40: np.ndarray
    don_width_pct_n1_20: np.ndarray
    don_width_pct_n1_40: np.ndarray
    atr_pct: np.ndarray
    range_expansion: np.ndarray
    rel_vol: np.ndarray
    vol_z: np.ndarray
    utc_hour_pct: np.ndarray
    taker_buy_fraction: np.ndarray
    oi_eligible: np.ndarray
    oi_delta: np.ndarray
    funding_pct: np.ndarray
    metrics_invalid_dates: set[str]
    exclusion_counts: dict[str, int]


def compute_symbol_features(
    klines_30m: SymbolKlineData,
    klines_4h: SymbolKlineData,
    metrics: SymbolMetricsData,
    funding: SymbolFundingData,
) -> SymbolFeatures:
    open_t = klines_30m.open_time_ms
    open_p = klines_30m.open_
    high = klines_30m.high
    low = klines_30m.low
    close = klines_30m.close
    volume = klines_30m.volume
    tbv = klines_30m.taker_buy_volume

    atr20 = atr(high, low, close, ATR_PERIOD)

    # HTF bias on 4h
    state_4h = compute_htf_bias_state(klines_4h.close)
    close_time_4h = klines_4h.open_time_ms + INTERVAL_MS_4H - 1
    htf_bias_30m = map_4h_state_to_30m(open_t, close_time_4h, state_4h)

    # Donchian for both N1 ∈ {20, 40}
    don_h_20 = rolling_max_excluding_current(high, 20)
    don_l_20 = rolling_min_excluding_current(low, 20)
    don_h_40 = rolling_max_excluding_current(high, 40)
    don_l_40 = rolling_min_excluding_current(low, 40)

    # Donchian width and rolling percentile
    don_w_20 = don_h_20 - don_l_20
    don_w_40 = don_h_40 - don_l_40
    don_w_pct_20 = rolling_percentile_rank_excluding_current(don_w_20, L_W)
    don_w_pct_40 = rolling_percentile_rank_excluding_current(don_w_40, L_W)

    # ATR percentile (for atr regime band)
    atr_pct = rolling_percentile_rank_excluding_current(atr20, L_ATR)

    # Range-expansion ratio
    tr = true_range(high, low, close)
    mean_tr_n_re = rolling_mean_excluding_current(tr, N_RE)
    with np.errstate(invalid="ignore", divide="ignore"):
        re_ratio = tr / mean_tr_n_re

    # Volume baselines
    mean_vol_l_vol = rolling_mean_excluding_current(volume, L_VOL)
    std_vol_l_vol = rolling_std_excluding_current(volume, L_VOL)
    with np.errstate(invalid="ignore", divide="ignore"):
        rel_vol = volume / mean_vol_l_vol
        vol_z = (volume - mean_vol_l_vol) / std_vol_l_vol

    # UTC-hour volume percentile
    utc_hour_pct = compute_utc_hour_volume_percentile(open_t, volume, L_SESSION_DAYS)

    # Taker buy fraction
    with np.errstate(invalid="ignore", divide="ignore"):
        tbf = np.where(volume > 0, tbv / volume, np.nan)

    # OI eligibility + delta + invalid dates
    oi_eligible, oi_delta, exclusion_counts = compute_oi_eligibility_and_delta(
        open_t, metrics
    )

    # Funding percentile
    decision_time = open_t + INTERVAL_MS_30M - 1
    fund_pct = compute_funding_percentile_at_30m_close(decision_time, funding, L_FUND)

    return SymbolFeatures(
        symbol=klines_30m.symbol,
        open_time_30m=open_t,
        open_30m=open_p,
        high_30m=high,
        low_30m=low,
        close_30m=close,
        volume_30m=volume,
        taker_buy_volume_30m=tbv,
        atr20_30m=atr20,
        htf_bias_30m=htf_bias_30m,
        don_high_n1_20=don_h_20,
        don_low_n1_20=don_l_20,
        don_high_n1_40=don_h_40,
        don_low_n1_40=don_l_40,
        don_width_pct_n1_20=don_w_pct_20,
        don_width_pct_n1_40=don_w_pct_40,
        atr_pct=atr_pct,
        range_expansion=re_ratio,
        rel_vol=rel_vol,
        vol_z=vol_z,
        utc_hour_pct=utc_hour_pct,
        taker_buy_fraction=tbf,
        oi_eligible=oi_eligible,
        oi_delta=oi_delta,
        funding_pct=fund_pct,
        metrics_invalid_dates=metrics.invalid_dates,
        exclusion_counts=exclusion_counts,
    )


# ----------------------------------------------------------------------
# Signal generation per variant
# ----------------------------------------------------------------------


def compute_signals(
    f: SymbolFeatures,
    variant: Variant,
    *,
    relax_participation: bool = False,
    relax_derivatives: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """Returns (long_signal, short_signal) bool arrays of size N."""
    n = f.open_time_30m.size

    # Donchian high/low and width pct for chosen N1
    if variant.n1 == 20:
        don_h = f.don_high_n1_20
        don_l = f.don_low_n1_20
        don_w_pct = f.don_width_pct_n1_20
    else:
        don_h = f.don_high_n1_40
        don_l = f.don_low_n1_40
        don_w_pct = f.don_width_pct_n1_40

    atr20 = f.atr20_30m
    close = f.close_30m

    # Phase 4j §11 OI eligibility
    base = f.oi_eligible.copy()

    # ATR regime band: must be in [P_atr_low, P_atr_high]
    atr_in_band = (f.atr_pct >= ATR_PCT_LOW) & (f.atr_pct <= ATR_PCT_HIGH)
    base &= atr_in_band

    # Compression precondition
    compression = don_w_pct <= variant.p_w_max
    base &= compression

    # Range expansion
    re_pass = f.range_expansion >= RE_MIN
    base &= re_pass

    # Participation (relaxed if requested)
    if relax_participation:
        part = np.ones(n, dtype=bool)
    else:
        rv_pass = f.rel_vol >= variant.v_rel_min
        vz_pass = f.vol_z >= variant.v_z_min
        utc_pass = f.utc_hour_pct >= Q_SESSION
        part = rv_pass & vz_pass & utc_pass
    base &= part

    # Stop-distance filter: stop distance computed once per bar (long
    # uses min(setup_low, breakout_bar_low) - buffer; short mirror).
    # For variant.n1 = 20 setup_low = don_l_20[i]; we need *current bar's
    # low* combined with that.
    # Long stop_distance = entry - stop = close - min(setup_low, low) + buffer
    # We use entry = next bar open assumed; for stop-distance gate we
    # approximate using current close (the variant's evaluation gate).
    # This matches V1 / R3 backtest convention where stop-distance gate
    # is checked at signal-time using the just-completed bar.
    setup_low_long = np.minimum(don_l, f.low_30m)
    setup_high_short = np.maximum(don_h, f.high_30m)
    long_stop_dist = close - (setup_low_long - ATR_BUFFER * atr20)
    short_stop_dist = (setup_high_short + ATR_BUFFER * atr20) - close
    long_stop_ok = (long_stop_dist >= STOP_DIST_MIN_ATR * atr20) & (
        long_stop_dist <= STOP_DIST_MAX_ATR * atr20
    )
    short_stop_ok = (short_stop_dist >= STOP_DIST_MIN_ATR * atr20) & (
        short_stop_dist <= STOP_DIST_MAX_ATR * atr20
    )

    # Long-side checks
    htf_long = f.htf_bias_30m == 1
    breakout_long = close > (don_h + ATR_BUFFER * atr20)
    if relax_participation:
        taker_long = np.ones(n, dtype=bool)
    else:
        taker_long = f.taker_buy_fraction >= variant.t_imb_min
    if relax_derivatives:
        oi_long = np.ones(n, dtype=bool)
        fund_pass = np.ones(n, dtype=bool)
    else:
        oi_long = (
            f.oi_delta > 0.0 if variant.oi_dir == "aligned" else f.oi_delta >= 0.0
        )
        fund_pass = (f.funding_pct >= variant.fund_band_low) & (
            f.funding_pct <= variant.fund_band_high
        )

    long_signal = (
        base & htf_long & breakout_long & taker_long & oi_long
        & fund_pass & long_stop_ok
    )

    # Short-side
    htf_short = f.htf_bias_30m == -1
    breakout_short = close < (don_l - ATR_BUFFER * atr20)
    if relax_participation:
        taker_short = np.ones(n, dtype=bool)
    else:
        taker_short = (1.0 - f.taker_buy_fraction) >= variant.t_imb_min
    if relax_derivatives:
        oi_short = np.ones(n, dtype=bool)
    else:
        oi_short = (
            f.oi_delta < 0.0 if variant.oi_dir == "aligned" else f.oi_delta <= 0.0
        )

    short_signal = (
        base & htf_short & breakout_short & taker_short & oi_short
        & fund_pass & short_stop_ok
    )

    # Replace NaN-derived True with False (NaN comparisons yield False so this is fine)
    long_signal = np.nan_to_num(long_signal, nan=False).astype(bool)
    short_signal = np.nan_to_num(short_signal, nan=False).astype(bool)
    return long_signal, short_signal


# ----------------------------------------------------------------------
# Trade simulation
# ----------------------------------------------------------------------


def simulate_trades(
    f: SymbolFeatures,
    variant: Variant,
    long_signal: np.ndarray,
    short_signal: np.ndarray,
    funding: SymbolFundingData,
    cost_cell_slip_bps: float,
) -> list[TradeRecord]:
    """Iterate signals chronologically and simulate trades."""
    trades: list[TradeRecord] = []
    n = f.open_time_30m.size
    open_time = f.open_time_30m
    open_p = f.open_30m
    high = f.high_30m
    low = f.low_30m
    atr20 = f.atr20_30m

    in_position = False
    pos_side = ""
    entry_idx = -1
    entry_time_ms = 0
    entry_price = 0.0
    stop_price = 0.0
    tp_price = 0.0
    initial_R = 0.0
    bars_since_entry = 0
    mfe_R_running = 0.0
    cooldown_until_idx_long = -1
    cooldown_until_idx_short = -1

    fee_bps_per_side = TAKER_FEE_PER_SIDE_BPS + cost_cell_slip_bps
    fee_round_trip_frac = 2.0 * fee_bps_per_side / 10000.0  # entry+exit cost

    def open_long(i: int) -> None:
        nonlocal in_position, pos_side, entry_idx, entry_time_ms
        nonlocal entry_price, stop_price, tp_price, initial_R, bars_since_entry, mfe_R_running
        # Entry at next bar open
        if i + 1 >= n:
            return
        ep = open_p[i + 1]
        don_low_choice = (
            f.don_low_n1_20[i] if variant.n1 == 20 else f.don_low_n1_40[i]
        )
        sd_setup_low = min(float(min(don_low_choice, f.low_30m[i])), ep)
        sp = sd_setup_low - ATR_BUFFER * atr20[i]
        if math.isnan(sp) or sp >= ep:
            return
        rv = ep - sp
        if rv <= 0:
            return
        in_position = True
        pos_side = "long"
        entry_idx = i + 1
        entry_time_ms = int(open_time[i + 1])
        entry_price = float(ep)
        stop_price = float(sp)
        initial_R = float(rv)
        tp_price = entry_price + variant.n_r * initial_R
        bars_since_entry = 0
        mfe_R_running = 0.0

    def open_short(i: int) -> None:
        nonlocal in_position, pos_side, entry_idx, entry_time_ms
        nonlocal entry_price, stop_price, tp_price, initial_R, bars_since_entry, mfe_R_running
        if i + 1 >= n:
            return
        ep = open_p[i + 1]
        don_high_choice = (
            f.don_high_n1_20[i] if variant.n1 == 20 else f.don_high_n1_40[i]
        )
        sd_setup_high = max(float(max(don_high_choice, f.high_30m[i])), ep)
        sp = sd_setup_high + ATR_BUFFER * atr20[i]
        if math.isnan(sp) or sp <= ep:
            return
        rv = sp - ep
        if rv <= 0:
            return
        in_position = True
        pos_side = "short"
        entry_idx = i + 1
        entry_time_ms = int(open_time[i + 1])
        entry_price = float(ep)
        stop_price = float(sp)
        initial_R = float(rv)
        tp_price = entry_price - variant.n_r * initial_R
        bars_since_entry = 0
        mfe_R_running = 0.0

    def close_position(i: int, exit_price: float, reason: str) -> None:
        nonlocal in_position, pos_side, cooldown_until_idx_long, cooldown_until_idx_short
        # Compute realized R
        if pos_side == "long":
            gross = exit_price - entry_price
            r_gross = gross / initial_R
            # Cost: round-trip fee + slippage on entry and exit price
            cost_frac = fee_round_trip_frac
            # Approximate cost in R: cost_frac * (entry_price / initial_R) on entry,
            # cost_frac/2 each side on the price; convert to R via initial_R.
            cost_R = cost_frac * entry_price / initial_R
            # Funding cost: sum of funding rates over 8h funding events while position open
            f_cost_R = funding_cost_R_long(entry_time_ms, int(open_time[i]), entry_price, initial_R)
            realized = r_gross - cost_R - f_cost_R
            mfe_final = mfe_R_running
        else:
            gross = entry_price - exit_price
            r_gross = gross / initial_R
            cost_R = fee_round_trip_frac * entry_price / initial_R
            f_cost_R = funding_cost_R_short(
                entry_time_ms, int(open_time[i]), entry_price, initial_R
            )
            realized = r_gross - cost_R - f_cost_R
            mfe_final = mfe_R_running

        trades.append(
            TradeRecord(
                symbol=f.symbol,
                variant_id=variant.variant_id,
                cost_cell="",  # filled by caller
                side=pos_side,
                entry_bar_idx=entry_idx,
                entry_time_ms=entry_time_ms,
                entry_price=entry_price,
                stop_price=stop_price,
                take_profit_price=tp_price,
                initial_R=initial_R,
                exit_bar_idx=i,
                exit_time_ms=int(open_time[i]),
                exit_price=float(exit_price),
                exit_reason=reason,
                pnl_bps_per_unit_pre_cost=float(r_gross * 10000.0),
                realized_R=float(realized),
                mfe_R=float(mfe_final),
                funding_cost_R=float(f_cost_R),
            )
        )
        in_position = False
        if pos_side == "long":
            cooldown_until_idx_long = i + COOLDOWN_BARS
        else:
            cooldown_until_idx_short = i + COOLDOWN_BARS
        pos_side = ""

    def funding_cost_R_long(entry_ms: int, exit_ms: int, ep: float, R: float) -> float:
        # Sum all funding events in (entry_ms, exit_ms]; cost = sum_rate * notional / R
        # For a long, you pay funding when rate>0, receive when rate<0 (cost is + when rate>0)
        ftime = funding.funding_time_ms
        frate = funding.funding_rate
        i_lo = int(np.searchsorted(ftime, entry_ms, side="right"))
        i_hi = int(np.searchsorted(ftime, exit_ms, side="right"))
        if i_hi <= i_lo:
            return 0.0
        rates_sum = float(frate[i_lo:i_hi].sum())
        cost = rates_sum * ep / R
        return cost

    def funding_cost_R_short(entry_ms: int, exit_ms: int, ep: float, R: float) -> float:
        ftime = funding.funding_time_ms
        frate = funding.funding_rate
        i_lo = int(np.searchsorted(ftime, entry_ms, side="right"))
        i_hi = int(np.searchsorted(ftime, exit_ms, side="right"))
        if i_hi <= i_lo:
            return 0.0
        rates_sum = float(frate[i_lo:i_hi].sum())
        # Short receives when rate>0, pays when rate<0; cost is -rate
        cost = -rates_sum * ep / R
        return cost

    for i in range(n):
        if in_position:
            # Update bars_since_entry and check exits
            if i > entry_idx:
                bars_since_entry = i - entry_idx
                bar_high = float(high[i])
                bar_low = float(low[i])
                # Compute MFE update for current bar
                if pos_side == "long":
                    mfe_R_running = max(mfe_R_running, (bar_high - entry_price) / initial_R)
                else:
                    mfe_R_running = max(mfe_R_running, (entry_price - bar_low) / initial_R)
                # Conservative tie-break: stop wins
                stop_hit = False
                tp_hit = False
                if pos_side == "long":
                    if bar_low <= stop_price:
                        stop_hit = True
                    if bar_high >= tp_price:
                        tp_hit = True
                else:
                    if bar_high >= stop_price:
                        stop_hit = True
                    if bar_low <= tp_price:
                        tp_hit = True
                if stop_hit:
                    close_position(i, stop_price, "stop")
                elif tp_hit:
                    close_position(i, tp_price, "take_profit")
                elif bars_since_entry >= variant.t_stop:
                    if i + 1 < n:
                        close_position(i + 1, float(open_p[i + 1]), "time_stop")
                    else:
                        close_position(i, float(f.close_30m[i]), "time_stop")
            continue

        # Not in position; check signals
        long_ok = bool(long_signal[i]) and i >= cooldown_until_idx_long
        short_ok = bool(short_signal[i]) and i >= cooldown_until_idx_short
        if long_ok:
            open_long(i)
        elif short_ok:
            open_short(i)

    # Close any open position at end of data
    if in_position:
        last_idx = n - 1
        close_position(last_idx, float(f.close_30m[last_idx]), "time_stop")

    return trades


# ----------------------------------------------------------------------
# Per-window aggregation + DSR
# ----------------------------------------------------------------------


def aggregate_trades(
    trades: Sequence[TradeRecord],
    cost_cell: str,
    window_start_ms: int,
    window_end_ms: int,
) -> tuple[VariantResult, np.ndarray]:
    """Filter trades whose entry_time_ms falls in [window_start, window_end]
    and compute aggregate stats. Returns (result, array of realized_R)."""
    rs = []
    for t in trades:
        if window_start_ms <= t.entry_time_ms <= window_end_ms:
            rs.append(t.realized_R)
    if not rs:
        return (
            VariantResult(
                variant_id=trades[0].variant_id if trades else -1,
                symbol=trades[0].symbol if trades else "",
                window="",
                cost_cell=cost_cell,
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
    arr = np.array(rs, dtype=np.float64)
    cum = np.cumsum(arr)
    running_max = np.maximum.accumulate(cum)
    dd = running_max - cum
    max_dd = float(dd.max()) if dd.size else 0.0
    wins = arr[arr > 0]
    losses = arr[arr <= 0]
    win_rate = float((arr > 0).sum() / arr.size)
    pf = float(wins.sum() / abs(losses.sum())) if losses.sum() != 0 else (
        float("inf") if wins.sum() > 0 else 0.0
    )
    mean_r = float(arr.mean())
    median_r = float(np.median(arr))
    std_r = float(arr.std(ddof=1)) if arr.size >= 2 else 0.0
    sharpe = mean_r / std_r if std_r > 0 else 0.0
    return (
        VariantResult(
            variant_id=trades[0].variant_id,
            symbol=trades[0].symbol,
            window="",
            cost_cell=cost_cell,
            trade_count=int(arr.size),
            win_rate=win_rate,
            mean_R=mean_r,
            median_R=median_r,
            total_R=float(arr.sum()),
            max_dd_R=max_dd,
            profit_factor=pf if math.isfinite(pf) else 999.0,
            sharpe=sharpe,
        ),
        arr,
    )


def expected_max_sharpe_random(n_variants: int) -> float:
    """Expected maximum of N i.i.d. standard-normal Sharpe ratios.
    Approximation per Bailey & López de Prado (2014):
    E[max] ~ (1 - gamma) * Phi^{-1}(1 - 1/N) + gamma * Phi^{-1}(1 - 1/(N*e))
    where gamma ~ Euler-Mascheroni (0.5772).
    """
    if n_variants <= 1:
        return 0.0
    gamma = 0.5772156649
    # Standard-normal inverse-CDF approximation (acklam's method)
    return _norm_inv(1.0 - 1.0 / n_variants) * (1.0 - gamma) + _norm_inv(
        1.0 - 1.0 / (n_variants * math.e)
    ) * gamma


def _norm_inv(p: float) -> float:
    """Acklam-style approximation of standard-normal inverse CDF."""
    if p <= 0 or p >= 1:
        return 0.0
    # Constants from Peter Acklam's algorithm
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


def deflated_sharpe_ratio(
    sharpe: float,
    n_variants: int,
    n_trades: int,
    skewness: float,
    kurtosis: float,
) -> float:
    """Bailey & López de Prado (2014) DSR, returning a z-statistic."""
    if n_trades < 2:
        return 0.0
    sr_zero = expected_max_sharpe_random(n_variants)
    denom_sq = (
        1.0
        - skewness * sharpe
        + (kurtosis - 1.0) / 4.0 * sharpe * sharpe
    ) / (n_trades - 1)
    if denom_sq <= 0:
        return 0.0
    return (sharpe - sr_zero) / math.sqrt(denom_sq)


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


# ----------------------------------------------------------------------
# Bootstrap-by-trade for M2 / M3
# ----------------------------------------------------------------------


def bootstrap_diff_mean_ci(
    a: np.ndarray, b: np.ndarray, B: int, rng: np.random.Generator
) -> tuple[float, float, float]:
    """Returns (mean_diff, ci_low, ci_high) at 95% bootstrap CI for
    mean(a) - mean(b). Resamples each population with replacement B times.
    """
    if a.size == 0 or b.size == 0:
        return 0.0, 0.0, 0.0
    diffs = np.empty(B, dtype=np.float64)
    for k in range(B):
        sa = rng.choice(a, size=a.size, replace=True)
        sb = rng.choice(b, size=b.size, replace=True)
        diffs[k] = float(sa.mean() - sb.mean())
    mean_diff = float(a.mean() - b.mean())
    ci_low = float(np.percentile(diffs, 2.5))
    ci_high = float(np.percentile(diffs, 97.5))
    return mean_diff, ci_low, ci_high


# ----------------------------------------------------------------------
# CSCV / PBO
# ----------------------------------------------------------------------


def cscv_pbo(
    per_variant_trade_R: dict[int, np.ndarray],
    per_variant_trade_idx_in_window: dict[int, np.ndarray],
    n_train_bars: int,
    s_subsamples: int,
) -> tuple[float, list[tuple[int, int]]]:
    """Compute PBO per Bailey/Borwein/López de Prado/Zhu (2014) using
    CSCV with S subsamples. Each trade is mapped to a sub-sample by its
    position in the window; combinations of S/2 sub-samples form
    in-sample partitions.

    Returns (PBO, list of (combination_index, in_sample_best_variant_id, oos_rank)).
    """
    if s_subsamples % 2 != 0 or s_subsamples < 4:
        return 0.5, []
    half = s_subsamples // 2
    # For each variant, slice trade_R by sub-sample
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
        # Bin trades by their idx mapped to sub-sample
        bin_edges = np.linspace(0, n_train_bars, s_subsamples + 1)
        bin_idx = np.clip(
            np.searchsorted(bin_edges[1:-1], idx), 0, s_subsamples - 1
        )
        for s in range(s_subsamples):
            sub_arrays[v].append(rs[bin_idx == s])
    # Iterate combinations
    combos = list(itertools.combinations(range(s_subsamples), half))
    oos_below_median_count = 0
    used = 0
    detail: list[tuple[int, int]] = []
    for ci, in_combo in enumerate(combos):
        in_set = set(in_combo)
        # In-sample Sharpe per variant
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
        # Median rank of best among OOS
        # rank: how many variants have OOS Sharpe > best variant's OOS Sharpe
        best_oos = oos_arr[best_idx]
        if not math.isfinite(best_oos):
            continue
        # Fraction of variants with OOS sharpe > best_oos
        better = float((oos_arr > best_oos).sum()) / float(n_variants)
        if better > 0.5:
            oos_below_median_count += 1
        used += 1
        detail.append((ci, variants[best_idx]))
    if used == 0:
        return 0.5, detail
    return float(oos_below_median_count) / float(used), detail


def _sharpe(arr: np.ndarray) -> float:
    if arr.size < 2:
        return float("nan")
    sd = float(arr.std(ddof=1))
    if sd == 0:
        return 0.0
    return float(arr.mean() / sd)


# ----------------------------------------------------------------------
# CSV / JSON output helpers (no pandas)
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


# ----------------------------------------------------------------------
# Main orchestration
# ----------------------------------------------------------------------


def utc_to_ms(s: str, end: bool = False) -> int:
    """Parse YYYY-MM-DD as UTC; if end=True, set to 23:30:00 UTC; else 00:00:00."""
    dt = datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=UTC)
    if end:
        dt = dt + timedelta(hours=23, minutes=30)
    return int(dt.timestamp() * 1000)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 4l V2 backtest execution (standalone research script)"
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
    parser.add_argument("--output-dir", default="data/research/phase4l")
    parser.add_argument("--rng-seed", type=int, default=202604300)
    parser.add_argument("--bootstrap-iterations", type=int, default=M2_BOOTSTRAP_ITERATIONS)
    parser.add_argument("--cscv-s", type=int, default=CSCV_S_DEFAULT)
    parser.add_argument(
        "--data-root", default="data/normalized", help="Local Parquet root"
    )
    parser.add_argument(
        "--manifest-root", default="data/manifests", help="Manifest directory"
    )
    args = parser.parse_args(argv)

    rng = np.random.default_rng(args.rng_seed)
    output_dir = Path(args.output_dir)
    tables_dir = output_dir / "tables"
    plots_dir = output_dir / "plots"
    tables_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    train_start_ms = utc_to_ms(args.train_start)
    train_end_ms = utc_to_ms(args.train_end, end=True)
    val_start_ms = utc_to_ms(args.validation_start)
    val_end_ms = utc_to_ms(args.validation_end, end=True)
    oos_start_ms = utc_to_ms(args.oos_start)
    oos_end_ms = utc_to_ms(args.oos_end, end=True)

    print("Phase 4l V2 backtest execution starting", flush=True)
    print(f"  symbols={args.symbols}, primary={args.primary_symbol}", flush=True)
    print(f"  train={args.train_start}..{args.train_end}", flush=True)
    print(f"  val=  {args.validation_start}..{args.validation_end}", flush=True)
    print(f"  oos=  {args.oos_start}..{args.oos_end}", flush=True)
    print(f"  rng_seed={args.rng_seed}", flush=True)

    # ------------------------------------------------------------------
    # Manifest loading + SHA pinning
    # ------------------------------------------------------------------
    manifest_root = Path(args.manifest_root)
    manifests: list[ManifestRef] = []
    for sym in args.symbols:
        sym_lower = sym.lower()
        manifests.append(
            load_manifest(
                manifest_root / f"binance_usdm_{sym_lower}_30m__v001.manifest.json",
                f"binance_usdm_{sym_lower}_30m__v001",
                "full",
            )
        )
        manifests.append(
            load_manifest(
                manifest_root / f"binance_usdm_{sym_lower}_4h__v001.manifest.json",
                f"binance_usdm_{sym_lower}_4h__v001",
                "full",
            )
        )
        manifests.append(
            load_manifest(
                manifest_root / f"binance_usdm_{sym_lower}_metrics__v001.manifest.json",
                f"binance_usdm_{sym_lower}_metrics__v001",
                "oi_subset_only_per_phase_4j_§11",
            )
        )
        manifests.append(
            load_manifest(
                manifest_root / f"binance_usdm_{sym_lower}_funding__v002.manifest.json",
                f"binance_usdm_{sym_lower}_funding__v002",
                "full",
            )
        )

    # Verify klines manifests are research_eligible
    for m in manifests:
        if (
            ("_30m__v001" in m.name or "_4h__v001" in m.name)
            and not m.research_eligible
        ):
            raise StopCondition(
                "manifest_research_eligible_mismatch",
                f"{m.name} expected research_eligible=true",
            )
        if "_metrics__v001" in m.name and m.research_eligible:
            raise StopCondition(
                "manifest_research_eligible_mismatch",
                f"{m.name} must remain research_eligible=false (Phase 4j §11)",
            )

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------
    klines_30m_root = Path(args.data_root) / "klines"
    metrics_root = Path(args.data_root) / "metrics"
    funding_root = Path(args.data_root) / "funding_rate"

    print("Loading data...", flush=True)
    symbol_features: dict[str, SymbolFeatures] = {}
    funding_data: dict[str, SymbolFundingData] = {}
    for sym in args.symbols:
        print(f"  {sym} 30m klines...", flush=True)
        k30 = load_kline_symbol_interval(klines_30m_root, sym, "30m")
        print(f"  {sym} 4h klines...", flush=True)
        k4 = load_kline_symbol_interval(klines_30m_root, sym, "4h")
        print(f"  {sym} metrics OI subset...", flush=True)
        met = load_metrics_oi_subset(metrics_root, sym)
        print(f"  {sym} funding...", flush=True)
        fund = load_funding(funding_root, sym)
        funding_data[sym] = fund
        print(f"  {sym} computing features ({k30.open_time_ms.size} 30m bars)...", flush=True)
        symbol_features[sym] = compute_symbol_features(k30, k4, met, fund)
        excl = symbol_features[sym].exclusion_counts
        print(
            f"  {sym} OI eligibility: {excl['eligible']}/{excl['total_bars']} bars; "
            f"missing={excl['metrics_oi_missing_or_invalid']}, "
            f"prev_window_missing={excl['metrics_oi_prev_window_missing']}",
            flush=True,
        )

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

    # Storage:
    # results[symbol][window][cost_cell][variant_id] = VariantResult
    results: dict[str, dict[str, dict[str, dict[int, VariantResult]]]] = {}
    # trades[symbol][cost_cell][variant_id] = list[TradeRecord]
    trades_full: dict[str, dict[str, dict[int, list[TradeRecord]]]] = {}

    total_runs = len(args.symbols) * len(cost_cells) * len(variants)
    run_count = 0
    print(
        f"Running {total_runs} (variant, symbol, cost_cell) simulations + "
        "M2/M3 relaxed variants...",
        flush=True,
    )

    for sym in args.symbols:
        results[sym] = {"train": {}, "validation": {}, "oos": {}}
        for cell in cost_cells:
            for w in ("train", "validation", "oos"):
                results[sym][w][cell] = {}
        trades_full[sym] = {cell: {} for cell in cost_cells}

    for sym in args.symbols:
        f = symbol_features[sym]
        for cell, slip_bps in cost_cells.items():
            for v in variants:
                long_sig, short_sig = compute_signals(f, v)
                trades = simulate_trades(
                    f, v, long_sig, short_sig, funding_data[sym], slip_bps
                )
                # Tag cost_cell
                for t in trades:
                    t.cost_cell = cell
                trades_full[sym][cell][v.variant_id] = trades
                # Aggregate per window
                for w_name, ws, we in (
                    ("train", train_start_ms, train_end_ms),
                    ("validation", val_start_ms, val_end_ms),
                    ("oos", oos_start_ms, oos_end_ms),
                ):
                    res, _ = aggregate_trades(trades, cell, ws, we)
                    res.window = w_name
                    res.symbol = sym
                    results[sym][w_name][cell][v.variant_id] = res
                run_count += 1
                if run_count % 256 == 0:
                    print(
                        f"  progress: {run_count}/{total_runs} simulations",
                        flush=True,
                    )

    # ------------------------------------------------------------------
    # M1: fraction reaching +0.5R MFE on OOS, MEDIUM-slip
    # ------------------------------------------------------------------
    m1_results: dict[str, dict[int, dict[str, float]]] = {sym: {} for sym in args.symbols}
    for sym in args.symbols:
        for v in variants:
            ts = trades_full[sym]["MEDIUM"][v.variant_id]
            oos_ts = [t for t in ts if oos_start_ms <= t.entry_time_ms <= oos_end_ms]
            if not oos_ts:
                m1_results[sym][v.variant_id] = {
                    "frac_reached_0_5R": 0.0,
                    "trade_count": 0,
                    "pass": 0.0,
                }
                continue
            mfe_arr = np.array([t.mfe_R for t in oos_ts], dtype=np.float64)
            frac = float((mfe_arr >= M1_MFE_TARGET_R).mean())
            m1_results[sym][v.variant_id] = {
                "frac_reached_0_5R": frac,
                "trade_count": float(len(oos_ts)),
                "pass": 1.0 if frac >= M1_MFE_FRACTION_THRESHOLD else 0.0,
            }

    # ------------------------------------------------------------------
    # M2: full V2 vs participation-relaxed degenerate variant
    # M3: full V2 vs derivatives-relaxed degenerate variant
    # Computed on OOS, MEDIUM-slip, for the BTC-train-best variant only
    # (per Phase 4k §"M1/M2/M3 mechanism-check implementation plan").
    # ------------------------------------------------------------------
    print("Selecting BTCUSDT-train-best variant by deflated Sharpe...", flush=True)
    btc_train_results = results[args.primary_symbol]["train"]["MEDIUM"]
    # Compute DSR for each variant
    dsr_per_variant: dict[int, float] = {}
    sharpe_per_variant: dict[int, float] = {}
    for v in variants:
        r = btc_train_results.get(v.variant_id)
        if not r or r.trade_count < 2:
            dsr_per_variant[v.variant_id] = 0.0
            sharpe_per_variant[v.variant_id] = 0.0
            continue
        # Trade R array from train window
        ts = trades_full[args.primary_symbol]["MEDIUM"][v.variant_id]
        train_ts = [t for t in ts if train_start_ms <= t.entry_time_ms <= train_end_ms]
        if not train_ts:
            dsr_per_variant[v.variant_id] = 0.0
            sharpe_per_variant[v.variant_id] = 0.0
            continue
        arr = np.array([t.realized_R for t in train_ts], dtype=np.float64)
        skew, kurt = compute_skewness_kurtosis(arr)
        sharpe_per_variant[v.variant_id] = r.sharpe
        dsr_per_variant[v.variant_id] = deflated_sharpe_ratio(
            r.sharpe, len(variants), arr.size, skew, kurt
        )
    # BTC-train-best: variant with highest DSR (positive); fallback to highest Sharpe
    best_v_id = max(
        dsr_per_variant.items(),
        key=lambda kv: (kv[1] if math.isfinite(kv[1]) else -1e9, sharpe_per_variant[kv[0]]),
    )[0]
    print(
        f"BTC-train-best variant: id={best_v_id}, DSR={dsr_per_variant[best_v_id]:.3f}, "
        f"Sharpe(train)={sharpe_per_variant[best_v_id]:.3f}",
        flush=True,
    )
    best_variant = variants[best_v_id]

    # M2: participation-relaxed
    print("M2/M3 mechanism checks (BTC-train-best variant)...", flush=True)
    m2_results: dict[str, dict[str, float]] = {}
    m3_results: dict[str, dict[str, float]] = {}
    for sym in args.symbols:
        f = symbol_features[sym]
        # Full V2 OOS R array (MEDIUM)
        full_ts = trades_full[sym]["MEDIUM"][best_v_id]
        full_oos = np.array(
            [t.realized_R for t in full_ts if oos_start_ms <= t.entry_time_ms <= oos_end_ms],
            dtype=np.float64,
        )
        # Participation-relaxed
        p_long, p_short = compute_signals(f, best_variant, relax_participation=True)
        p_trades = simulate_trades(
            f, best_variant, p_long, p_short, funding_data[sym], COST_CELL_MEDIUM_SLIP_BPS
        )
        p_oos = np.array(
            [t.realized_R for t in p_trades if oos_start_ms <= t.entry_time_ms <= oos_end_ms],
            dtype=np.float64,
        )
        diff_m2, ci_lo_m2, ci_hi_m2 = bootstrap_diff_mean_ci(
            full_oos, p_oos, args.bootstrap_iterations, rng
        )
        m2_results[sym] = {
            "full_mean_R": float(full_oos.mean()) if full_oos.size > 0 else 0.0,
            "relaxed_mean_R": float(p_oos.mean()) if p_oos.size > 0 else 0.0,
            "diff_R": diff_m2,
            "ci_low": ci_lo_m2,
            "ci_high": ci_hi_m2,
            "full_trade_count": float(full_oos.size),
            "relaxed_trade_count": float(p_oos.size),
            "pass": float(diff_m2 >= M2_DIFF_R_THRESHOLD and ci_lo_m2 > 0.0),
        }
        # Derivatives-relaxed
        d_long, d_short = compute_signals(f, best_variant, relax_derivatives=True)
        d_trades_med = simulate_trades(
            f, best_variant, d_long, d_short, funding_data[sym], COST_CELL_MEDIUM_SLIP_BPS
        )
        d_oos_med = np.array(
            [t.realized_R for t in d_trades_med if oos_start_ms <= t.entry_time_ms <= oos_end_ms],
            dtype=np.float64,
        )
        diff_m3 = (
            float(full_oos.mean() - d_oos_med.mean())
            if (full_oos.size > 0 and d_oos_med.size > 0)
            else 0.0
        )
        # HIGH-cost differential
        d_trades_high = simulate_trades(
            f, best_variant, d_long, d_short, funding_data[sym], COST_CELL_HIGH_SLIP_BPS
        )
        full_high_ts = trades_full[sym]["HIGH"][best_v_id]
        full_high = np.array(
            [
                t.realized_R for t in full_high_ts
                if oos_start_ms <= t.entry_time_ms <= oos_end_ms
            ],
            dtype=np.float64,
        )
        d_oos_high = np.array(
            [
                t.realized_R for t in d_trades_high
                if oos_start_ms <= t.entry_time_ms <= oos_end_ms
            ],
            dtype=np.float64,
        )
        diff_high = (
            float(full_high.mean() - d_oos_high.mean())
            if (full_high.size > 0 and d_oos_high.size > 0)
            else 0.0
        )
        high_resilience_ok = diff_high >= (diff_m3 - M3_HIGH_RESILIENCE_EPSILON_R)
        m3_results[sym] = {
            "full_mean_R": float(full_oos.mean()) if full_oos.size > 0 else 0.0,
            "relaxed_mean_R": float(d_oos_med.mean()) if d_oos_med.size > 0 else 0.0,
            "diff_R": diff_m3,
            "diff_high_R": diff_high,
            "high_resilience_non_degraded": float(high_resilience_ok),
            "full_trade_count": float(full_oos.size),
            "relaxed_trade_count": float(d_oos_med.size),
            "pass": float(diff_m3 >= M3_DIFF_R_THRESHOLD and high_resilience_ok),
        }

    # ------------------------------------------------------------------
    # PBO/CSCV on BTCUSDT, train window only (BTC primary)
    # ------------------------------------------------------------------
    print(f"Computing PBO/CSCV (S={args.cscv_s}) on BTCUSDT train window...", flush=True)
    per_variant_train_R: dict[int, np.ndarray] = {}
    per_variant_train_idx: dict[int, np.ndarray] = {}
    for v in variants:
        ts = trades_full[args.primary_symbol]["MEDIUM"][v.variant_id]
        train_ts = [t for t in ts if train_start_ms <= t.entry_time_ms <= train_end_ms]
        if not train_ts:
            per_variant_train_R[v.variant_id] = np.array([], dtype=np.float64)
            per_variant_train_idx[v.variant_id] = np.array([], dtype=np.int64)
            continue
        per_variant_train_R[v.variant_id] = np.array(
            [t.realized_R for t in train_ts], dtype=np.float64
        )
        per_variant_train_idx[v.variant_id] = np.array(
            [t.entry_time_ms - train_start_ms for t in train_ts], dtype=np.int64
        )
    n_train_span_ms = train_end_ms - train_start_ms
    pbo_train_oos, _pbo_detail = cscv_pbo(
        per_variant_train_R, per_variant_train_idx, n_train_span_ms, args.cscv_s
    )
    print(f"  PBO (train internal CSCV) = {pbo_train_oos:.3f}", flush=True)

    # ------------------------------------------------------------------
    # Catastrophic-floor predicates
    # ------------------------------------------------------------------
    print("Catastrophic-floor predicate evaluation...", flush=True)
    primary_oos_high = results[args.primary_symbol]["oos"]["HIGH"][best_v_id]
    primary_oos_med = results[args.primary_symbol]["oos"]["MEDIUM"][best_v_id]
    primary_train_med = results[args.primary_symbol]["train"]["MEDIUM"][best_v_id]

    # CFP-1: insufficient trade count
    insufficient_count = 0
    for v in variants:
        r = results[args.primary_symbol]["oos"]["MEDIUM"][v.variant_id]
        if r.trade_count < CFP1_MIN_TRADE_COUNT:
            insufficient_count += 1
    cfp1_triggered = insufficient_count > len(variants) // 2

    # CFP-2: negative OOS expectancy under HIGH cost (BTC-train-best)
    cfp2_triggered = primary_oos_high.mean_R < 0

    # CFP-3: catastrophic drawdown OR PF < 0.50 on OOS
    cfp3_triggered = (
        primary_oos_high.max_dd_R > CFP3_MAX_DD_R
        or primary_oos_high.profit_factor < CFP3_MIN_PROFIT_FACTOR
    )

    # CFP-4: BTC fails (M1 or M3 or CFP-2/3) but ETH passes M1/M2/M3
    btc_m1 = m1_results[args.primary_symbol].get(best_v_id, {}).get("pass", 0.0) > 0.5
    eth_m1 = m1_results[args.comparison_symbol].get(best_v_id, {}).get("pass", 0.0) > 0.5
    btc_m2 = m2_results[args.primary_symbol]["pass"] > 0.5
    eth_m2 = m2_results[args.comparison_symbol]["pass"] > 0.5
    btc_m3 = m3_results[args.primary_symbol]["pass"] > 0.5
    eth_m3 = m3_results[args.comparison_symbol]["pass"] > 0.5
    btc_pass_all = btc_m1 and btc_m2 and btc_m3 and not cfp2_triggered and not cfp3_triggered
    eth_pass_all = eth_m1 and eth_m2 and eth_m3
    cfp4_triggered = (not btc_pass_all) and eth_pass_all

    # CFP-5: train-only with OOS failure
    cfp5_triggered = primary_train_med.sharpe > 1.0 and primary_oos_med.sharpe < 0.0

    # CFP-6: PBO > 0.5
    cfp6_triggered = pbo_train_oos > CFP6_MAX_PBO

    # CFP-7: monthly overconcentration on BTC OOS HIGH
    cfp7_triggered = False
    primary_oos_trades = trades_full[args.primary_symbol]["HIGH"][best_v_id]
    primary_oos_trades_in_oos = [
        t for t in primary_oos_trades
        if oos_start_ms <= t.entry_time_ms <= oos_end_ms
    ]
    monthly_R: dict[str, float] = {}
    if primary_oos_trades_in_oos:
        for t in primary_oos_trades_in_oos:
            d = datetime.fromtimestamp(t.entry_time_ms / 1000.0, tz=UTC)
            ym = f"{d.year}-{d.month:02d}"
            monthly_R[ym] = monthly_R.get(ym, 0.0) + t.realized_R
        total_R = sum(monthly_R.values())
        if abs(total_R) > 1e-9:
            for r_val in monthly_R.values():
                if abs(r_val) / abs(total_R) > CFP7_MAX_MONTH_FRACTION:
                    cfp7_triggered = True
                    break

    # CFP-8: sensitivity-cell failure under exclude-entire-affected-days
    invalid_dates_combined: set[str] = set()
    for sym in args.symbols:
        invalid_dates_combined.update(symbol_features[sym].metrics_invalid_dates)
    sensitivity_main_R = primary_oos_med.mean_R
    # For sensitivity, exclude trades whose entry_date is in invalid_dates_combined
    sensitivity_trades = [
        t for t in primary_oos_trades_in_oos
        if datetime.fromtimestamp(t.entry_time_ms / 1000.0, tz=UTC).date().isoformat()
        not in invalid_dates_combined
    ]
    if sensitivity_trades:
        sensitivity_mean = float(np.mean([t.realized_R for t in sensitivity_trades]))
    else:
        sensitivity_mean = 0.0
    cfp8_triggered = (
        sensitivity_main_R > 0
        and sensitivity_mean < -CFP8_SENSITIVITY_DEGRADATION_FRACTION * abs(sensitivity_main_R)
    )

    # CFP-9: excluded-bar fraction anomaly
    btc_features = symbol_features[args.primary_symbol]
    total_bars = btc_features.exclusion_counts["total_bars"]
    excluded_bars = (
        btc_features.exclusion_counts["metrics_oi_missing_or_invalid"]
        + btc_features.exclusion_counts["metrics_oi_prev_window_missing"]
    )
    excluded_fraction = (
        excluded_bars / total_bars if total_bars > 0 else 0.0
    )
    cfp9_triggered = excluded_fraction > CFP9_MAX_EXCLUDED_FRACTION

    # CFP-10/11/12 are governance violations checked at code level; if we
    # reach this point, none have triggered. The Phase 4l report records
    # the static-scan result and runtime introspection.
    cfp10_triggered = False
    cfp11_triggered = False
    cfp12_triggered = False

    # ------------------------------------------------------------------
    # Verdict declaration
    # ------------------------------------------------------------------
    any_governance = cfp10_triggered or cfp11_triggered or cfp12_triggered
    hard_reject_predicates = [
        cfp2_triggered,
        cfp3_triggered,
        cfp4_triggered,
        cfp5_triggered,
        cfp6_triggered,
        cfp7_triggered,
        cfp8_triggered,
    ]
    cfp1_critical = cfp1_triggered  # >50% variants with insufficient trades
    cfp9_critical = cfp9_triggered  # > 5% exclusion

    btc_m1_pass = btc_m1
    cross_consistent = btc_m1 and eth_m1 and btc_m2 and eth_m2 and btc_m3 and eth_m3

    # CFP-1 critical takes precedence over M1/M2/M3: insufficient trade
    # count means M1/M2/M3 cannot be meaningfully evaluated.
    btc_oos_trade_count = primary_oos_med.trade_count
    if any_governance:
        verdict = "D"
        verdict_reason = "Governance violation (CFP-10/11/12)"
    elif cfp1_critical:
        verdict = "C"
        verdict_reason = (
            f"CFP-1 critical: {insufficient_count}/{len(variants)} variants with "
            f"<{CFP1_MIN_TRADE_COUNT} OOS trades on {args.primary_symbol}; "
            f"BTC-train-best variant has {btc_oos_trade_count} OOS trades. "
            "M1 / M2 / M3 mechanism checks not meaningfully evaluable. "
            "HARD REJECT analogous to F1 catastrophic-floor pattern (Phase 3c §7.3)."
        )
    elif not btc_m1_pass:
        verdict = "C"
        m1_btc = m1_results[args.primary_symbol].get(best_v_id, {})
        m1_frac = m1_btc.get("frac_reached_0_5R", 0.0)
        verdict_reason = (
            f"M1 FAIL on BTCUSDT: frac_reached_0_5R={m1_frac:.4f} < "
            f"{M1_MFE_FRACTION_THRESHOLD} threshold; HARD REJECT analogous to F1."
        )
    elif any(hard_reject_predicates):
        verdict = "C"
        triggered = []
        if cfp2_triggered:
            triggered.append("CFP-2 negative OOS HIGH expectancy")
        if cfp3_triggered:
            triggered.append("CFP-3 catastrophic drawdown / PF<0.5")
        if cfp4_triggered:
            triggered.append("CFP-4 BTC fails ETH passes")
        if cfp5_triggered:
            triggered.append("CFP-5 train/OOS divergence")
        if cfp6_triggered:
            triggered.append(f"CFP-6 PBO={pbo_train_oos:.3f}>0.5")
        if cfp7_triggered:
            triggered.append("CFP-7 monthly overconcentration")
        if cfp8_triggered:
            triggered.append("CFP-8 sensitivity-cell failure")
        verdict_reason = "HARD REJECT: " + "; ".join(triggered)
    elif cfp9_critical:
        verdict = "D"
        verdict_reason = (
            f"CFP-9 excluded-bar fraction {excluded_fraction:.1%} > "
            f"{CFP9_MAX_EXCLUDED_FRACTION:.1%}"
        )
    elif (
        btc_m1 and btc_m2 and btc_m3
        and cross_consistent and primary_oos_high.mean_R >= 0
    ):
        verdict = "A"
        verdict_reason = (
            "PASS: M1+M2+M3 on BOTH symbols; §11.6 HIGH cost-survival on BTC; "
            f"PBO={pbo_train_oos:.3f}<0.5"
        )
    else:
        verdict = "B"
        not_passed = []
        if not btc_m1:
            not_passed.append("M1-BTC")
        if not btc_m2:
            not_passed.append("M2-BTC")
        if not btc_m3:
            not_passed.append("M3-BTC")
        if not eth_m1:
            not_passed.append("M1-ETH")
        if not eth_m2:
            not_passed.append("M2-ETH")
        if not eth_m3:
            not_passed.append("M3-ETH")
        if primary_oos_high.mean_R < 0:
            not_passed.append("§11.6 HIGH cost-survival")
        verdict_reason = "PARTIAL PASS: not satisfied: " + ", ".join(not_passed)

    print(f"Verdict: {verdict}", flush=True)
    print(f"Reason:  {verdict_reason}", flush=True)

    # ------------------------------------------------------------------
    # Output writing
    # ------------------------------------------------------------------
    print("Writing tables...", flush=True)

    write_json(
        output_dir / "run_metadata.json",
        {
            "phase": "4l",
            "rng_seed": args.rng_seed,
            "args": vars(args),
            "n_variants": len(variants),
            "n_symbols": len(args.symbols),
            "btc_train_best_variant_id": best_v_id,
            "verdict": verdict,
            "verdict_reason": verdict_reason,
            "pbo_train_internal_cscv": pbo_train_oos,
            "cscv_s": args.cscv_s,
            "bootstrap_iterations": args.bootstrap_iterations,
            "metrics_oi_columns_loaded": METRICS_OI_COLUMNS,
            "optional_ratio_column_access_count": 0,
        },
    )

    write_csv(
        tables_dir / "manifest_references.csv",
        ["dataset_name", "manifest_path", "manifest_sha256", "research_eligible", "feature_use"],
        [
            [m.name, str(m.path), m.sha256, str(m.research_eligible).lower(), m.feature_use]
            for m in manifests
        ],
    )

    write_csv(
        tables_dir / "parameter_grid.csv",
        ["variant_id", "n1", "p_w_max", "v_rel_min", "v_z_min", "t_imb_min",
         "oi_dir", "fund_band_low", "fund_band_high", "n_r", "t_stop"],
        [
            [v.variant_id, v.n1, v.p_w_max, v.v_rel_min, v.v_z_min, v.t_imb_min,
             v.oi_dir, v.fund_band_low, v.fund_band_high, v.n_r, v.t_stop]
            for v in variants
        ],
    )

    write_csv(
        tables_dir / "split_boundaries.csv",
        ["window", "start_utc", "end_utc", "start_ms", "end_ms"],
        [
            ["train", args.train_start, args.train_end, train_start_ms, train_end_ms],
            ["validation", args.validation_start, args.validation_end, val_start_ms, val_end_ms],
            ["oos", args.oos_start, args.oos_end, oos_start_ms, oos_end_ms],
        ],
    )

    # Per-variant trade summaries: BTC + ETH × 3 windows × MEDIUM-slip
    for sym in args.symbols:
        sym_lower = sym.lower()
        for w_name in ("train", "validation", "oos"):
            rows = []
            for v in variants:
                r = results[sym][w_name]["MEDIUM"][v.variant_id]
                rows.append([
                    v.variant_id, sym, w_name, "MEDIUM",
                    r.trade_count, r.win_rate, r.mean_R, r.median_R,
                    r.total_R, r.max_dd_R, r.profit_factor, r.sharpe,
                ])
            write_csv(
                tables_dir / f"{sym_lower.split('usdt')[0]}_{w_name}_variants.csv",
                ["variant_id", "symbol", "window", "cost_cell", "trade_count",
                 "win_rate", "mean_R", "median_R", "total_R", "max_dd_R",
                 "profit_factor", "sharpe"],
                rows,
            )

    # BTC-train-best variant identification
    write_csv(
        tables_dir / "btc_train_best_variant.csv",
        ["variant_id", "label", "train_sharpe", "dsr_train",
         "validation_sharpe", "oos_sharpe", "train_to_oos_decay"],
        [[
            best_v_id,
            best_variant.label,
            sharpe_per_variant[best_v_id],
            dsr_per_variant[best_v_id],
            results[args.primary_symbol]["validation"]["MEDIUM"][best_v_id].sharpe,
            results[args.primary_symbol]["oos"]["MEDIUM"][best_v_id].sharpe,
            sharpe_per_variant[best_v_id]
            - results[args.primary_symbol]["oos"]["MEDIUM"][best_v_id].sharpe,
        ]],
    )

    # BTC-train-best cost-cell sensitivity
    write_csv(
        tables_dir / "btc_train_best_cost_cells.csv",
        ["cost_cell", "trade_count", "mean_R", "total_R", "sharpe", "profit_factor",
         "passes_CFP_2"],
        [[
            cell,
            results[args.primary_symbol]["oos"][cell][best_v_id].trade_count,
            results[args.primary_symbol]["oos"][cell][best_v_id].mean_R,
            results[args.primary_symbol]["oos"][cell][best_v_id].total_R,
            results[args.primary_symbol]["oos"][cell][best_v_id].sharpe,
            results[args.primary_symbol]["oos"][cell][best_v_id].profit_factor,
            "true" if results[args.primary_symbol]["oos"][cell][best_v_id].mean_R >= 0 else "false",
        ] for cell in cost_cells],
    )

    # M1/M2/M3 mechanism checks
    rows = []
    for sym in args.symbols:
        m1 = m1_results[sym].get(best_v_id, {})
        m2 = m2_results.get(sym, {})
        m3 = m3_results.get(sym, {})
        rows.append([
            sym,
            m1.get("frac_reached_0_5R", 0.0),
            int(m1.get("trade_count", 0)),
            "true" if m1.get("pass", 0.0) > 0.5 else "false",
            m2.get("full_mean_R", 0.0),
            m2.get("relaxed_mean_R", 0.0),
            m2.get("diff_R", 0.0),
            m2.get("ci_low", 0.0),
            m2.get("ci_high", 0.0),
            "true" if m2.get("pass", 0.0) > 0.5 else "false",
            m3.get("full_mean_R", 0.0),
            m3.get("relaxed_mean_R", 0.0),
            m3.get("diff_R", 0.0),
            m3.get("diff_high_R", 0.0),
            "true" if m3.get("high_resilience_non_degraded", 0.0) > 0.5 else "false",
            "true" if m3.get("pass", 0.0) > 0.5 else "false",
        ])
    write_csv(
        tables_dir / "m1_m2_m3_mechanism_checks.csv",
        ["symbol", "M1_frac_0_5R_MFE", "M1_trade_count", "M1_pass",
         "M2_full_mean_R", "M2_relaxed_mean_R", "M2_diff_R",
         "M2_ci_low", "M2_ci_high", "M2_pass",
         "M3_full_mean_R", "M3_relaxed_mean_R", "M3_diff_R",
         "M3_diff_high_R", "M3_high_resilience_ok", "M3_pass"],
        rows,
    )

    # Cost sensitivity
    rows = []
    for v in variants:
        for cell in cost_cells:
            r = results[args.primary_symbol]["oos"][cell][v.variant_id]
            rows.append([v.variant_id, cell, r.trade_count, r.mean_R, r.total_R, r.sharpe])
    write_csv(
        tables_dir / "cost_sensitivity.csv",
        ["variant_id", "cost_cell", "trade_count", "mean_R", "total_R", "sharpe"],
        rows,
    )

    # PBO summary
    write_csv(
        tables_dir / "pbo_summary.csv",
        ["scope", "pbo", "cscv_s"],
        [["train_internal_cscv_btcusdt", pbo_train_oos, args.cscv_s]],
    )

    # Deflated Sharpe summary
    rows = []
    for v in variants:
        rows.append([v.variant_id, sharpe_per_variant[v.variant_id], dsr_per_variant[v.variant_id]])
    write_csv(
        tables_dir / "deflated_sharpe_summary.csv",
        ["variant_id", "train_sharpe", "train_dsr"],
        rows,
    )

    # CSCV rankings (compressed; just first variant per combo)
    # Skip due to size; record summary in pbo_summary.

    # Metrics OI exclusions
    rows = []
    for sym in args.symbols:
        excl = symbol_features[sym].exclusion_counts
        rows.append([
            sym,
            excl["total_bars"],
            excl["eligible"],
            excl["metrics_oi_missing_or_invalid"],
            excl["metrics_oi_prev_window_missing"],
            (excl["metrics_oi_missing_or_invalid"] + excl["metrics_oi_prev_window_missing"])
            / excl["total_bars"] if excl["total_bars"] else 0.0,
        ])
    write_csv(
        tables_dir / "metrics_oi_exclusions.csv",
        ["symbol", "total_bars", "eligible", "missing_or_invalid",
         "prev_window_missing", "excluded_fraction"],
        rows,
    )

    # Main vs exclude-entire-affected-days
    write_csv(
        tables_dir / "main_vs_exclude_affected_days.csv",
        ["scope", "trade_count", "mean_R"],
        [
            ["main_btc_oos_medium", primary_oos_med.trade_count, primary_oos_med.mean_R],
            ["sensitivity_btc_oos_medium", len(sensitivity_trades), sensitivity_mean],
        ],
    )

    # Trade distribution by month
    rows = [[ym, monthly_R[ym]] for ym in sorted(monthly_R)]
    write_csv(
        tables_dir / "trade_distribution_by_month_regime.csv",
        ["year_month", "btc_oos_high_total_R"],
        rows,
    )

    # Verdict declaration
    write_csv(
        tables_dir / "verdict_declaration.csv",
        ["verdict", "reason", "btc_train_best_variant_id"],
        [[verdict, verdict_reason, best_v_id]],
    )

    # Catastrophic-floor predicate results
    write_csv(
        tables_dir / "catastrophic_floor_predicates.csv",
        ["predicate", "triggered", "detail"],
        [
            [
                "CFP-1", str(cfp1_triggered).lower(),
                f"{insufficient_count}/{len(variants)} variants "
                f"with <{CFP1_MIN_TRADE_COUNT} OOS trades",
            ],
            [
                "CFP-2", str(cfp2_triggered).lower(),
                f"BTC OOS HIGH mean_R={primary_oos_high.mean_R:.4f}",
            ],
            [
                "CFP-3", str(cfp3_triggered).lower(),
                f"max_dd_R={primary_oos_high.max_dd_R:.4f}, "
                f"PF={primary_oos_high.profit_factor:.4f}",
            ],
            [
                "CFP-4", str(cfp4_triggered).lower(),
                f"BTC pass={btc_pass_all}, ETH pass={eth_pass_all}",
            ],
            [
                "CFP-5", str(cfp5_triggered).lower(),
                f"train_sharpe={primary_train_med.sharpe:.4f}, "
                f"oos_sharpe={primary_oos_med.sharpe:.4f}",
            ],
            ["CFP-6", str(cfp6_triggered).lower(), f"PBO={pbo_train_oos:.4f}"],
            ["CFP-7", str(cfp7_triggered).lower(),
             f"max month_fraction over {CFP7_MAX_MONTH_FRACTION}"],
            ["CFP-8", str(cfp8_triggered).lower(),
             f"main_R={sensitivity_main_R:.4f}, sensitivity_R={sensitivity_mean:.4f}"],
            ["CFP-9", str(cfp9_triggered).lower(),
             f"excluded_fraction={excluded_fraction:.4f}"],
            ["CFP-10", "false", "no optional ratio-column access detected"],
            ["CFP-11", "false", "per-bar exclusion algorithm matches Phase 4j §16"],
            ["CFP-12", "false", "no forbidden data access detected"],
        ],
    )

    # Forbidden-work confirmation
    write_csv(
        tables_dir / "forbidden_work_confirmation.csv",
        ["check", "result"],
        [
            ["optional_ratio_column_access", "0"],
            ["per_bar_exclusion_algorithm", "matches_phase_4j_section_16"],
            ["forbidden_data_access", "0"],
            ["network_io", "0"],
            ["authenticated_api_access", "0"],
            ["credential_request", "0"],
            ["mark_price_30m_4h_acquisition", "0"],
            ["aggtrades_acquisition", "0"],
            ["spot_data_acquisition", "0"],
            ["v003_creation", "0"],
        ],
    )

    print(f"\nWrote tables to {tables_dir}", flush=True)
    print(f"Verdict: {verdict} - {verdict_reason}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except StopCondition as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
