"""Phase 4af - Alt-Symbol Regime-Continuity and Directional-Persistence Analysis.

Authority: Phase 4ae (alt-symbol substrate-feasibility analysis memo; merged
c57afa4). Phase 4ad (alt-symbol gap-governance and scope-revision memo; Rule
A mark-price invalid-window exclusion; Rule B SOL/XRP early-2022 kline gap
scope policy with B1 / B2 / B3; Rule C PASS-only subset; merged 10f122e).
Phase 4ac (alt-symbol public data acquisition; merged 3478d05). Phase 4ab
(alt-symbol data-requirements / feasibility memo). Phase 4aa (alt-symbol
market-selection / admissibility memo).

Brief: analysis-and-docs only. Reads existing local normalized Parquet only.
No network I/O. No Binance API. No `data.binance.vision`. No authenticated
REST. No private endpoints. No public-endpoint code calls. No user stream
/ WebSocket / listenKey. No credentials. No `.env`. No MCP / Graphify /
`.mcp.json`. No data acquisition. No data modification. No manifest
creation or modification. No backtest. No diagnostic / Q1-Q7 rerun. No
strategy candidate. No hypothesis-spec / strategy-spec / backtest-plan.
No `src/prometheus/` modification. No test modification. No existing-script
modification. No retained verdict revised. No project lock changed.

Default scope (Phase 4af brief):
    Symbols   : BTCUSDT  ETHUSDT  SOLUSDT  XRPUSDT  ADAUSDT
    Intervals : 15m  30m  1h  4h
    Start     : 2022-04-03 00:00 UTC  (Phase 4ad Rule B1 common post-gap)
    End       : 2026-04-30 23:59:59 UTC (cell ends at last available bar)
    Cost lock : 8 bps HIGH per side; round-trip = 16 bps; §11.6 preserved
    Output    : data/research/phase4af/  (gitignored; not committed)

Predeclared descriptive metric parameters (NOT optimized):
    EMA_FAST                          = 50
    EMA_SLOW                          = 200
    EMA_SLOPE_LAG                     = 3 bars
    ATR_WINDOW                        = 20
    ROLLING_WINDOW                    = 96 bars
    FORWARD_WINDOWS                   = (1, 2, 4, 8) bars
    PERSISTENCE_MOVE_THRESHOLDS_BPS   = (16, 24, 32)
    EXPANSION_THRESHOLD_MULTIPLIERS   = (1.5,)
    VOL_REGIME_QUANTILE               = 0.75

All metrics in this script are descriptive substrate-feasibility metrics
ONLY. They are NOT strategy signals, NOT backtests, NOT entry/exit rules,
NOT regime filters, NOT threshold-optimization candidates, NOT Q1-Q7
stop-pathology diagnostics, and NOT a fresh-hypothesis spec.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

REPO_ROOT = Path(r"C:\Prometheus")
NORM_KLINES_ROOT = REPO_ROOT / "data" / "normalized" / "klines"
DEFAULT_OUT = REPO_ROOT / "data" / "research" / "phase4af"
MANIFESTS_ROOT = REPO_ROOT / "data" / "manifests"

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT")
DEFAULT_INTERVALS = ("15m", "30m", "1h", "4h")

INTERVAL_MS = {
    "15m": 15 * 60 * 1000,
    "30m": 30 * 60 * 1000,
    "1h": 60 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
}

# Cost lock from §11.6 (preserved verbatim by Phase 4af).
HIGH_COST_BPS_PER_SIDE = 8.0
ROUND_TRIP_COST_BPS = 16.0

# Predeclared descriptive parameters. Fixed before analysis. Not optimized.
EMA_FAST = 50
EMA_SLOW = 200
EMA_SLOPE_LAG = 3
ATR_WINDOW = 20
ROLLING_WINDOW = 96
FORWARD_WINDOWS = (1, 2, 4, 8)
PERSISTENCE_MOVE_THRESHOLDS_BPS = (16.0, 24.0, 32.0)
EXPANSION_THRESHOLD_MULTIPLIERS = (1.5,)
VOL_REGIME_QUANTILE = 0.75

EPSILON = 1e-12


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_ymd_to_ms_utc(s: str, end_of_day: bool = False) -> int:
    y, m, d = (int(p) for p in s.split("-"))
    if end_of_day:
        dt = datetime(y, m, d, 23, 59, 59, tzinfo=UTC)
    else:
        dt = datetime(y, m, d, 0, 0, 0, tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def ms_to_iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, UTC).isoformat()


def manifest_eligibility(symbol: str, interval: str) -> tuple[bool, str | None]:
    """Read research_eligible flag from the relevant kline manifest.

    Prefer __v002 then __v001. Returns (eligible, manifest_name).
    """
    sym_lower = symbol.lower()
    candidates = [
        f"binance_usdm_{sym_lower}_{interval}__v002.manifest.json",
        f"binance_usdm_{sym_lower}_{interval}__v001.manifest.json",
    ]
    for name in candidates:
        p = MANIFESTS_ROOT / name
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                return bool(data.get("research_eligible", False)), name
            except Exception:  # noqa: BLE001
                continue
    return False, None


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def load_klines(symbol: str, interval: str, start_ms: int, end_ms: int) -> dict | None:
    """Read all monthly partitions for (symbol, interval), filter to the
    [start_ms, end_ms] inclusive analysis window, and return numpy arrays.

    Schema-tolerant: reads only OHLCV-compatible columns that exist in BOTH
    the Phase 2 schema (`trade_count`, `taker_buy_base_volume`, ...) and the
    Phase 4i / 4ac schema (`count`, `taker_buy_volume`, ..., `ignore`). The
    common column set is: open_time, close_time, open, high, low, close,
    volume.
    """
    base = NORM_KLINES_ROOT / f"symbol={symbol}" / f"interval={interval}"
    if not base.exists():
        return None
    parts = sorted(base.rglob("part-0000.parquet"))
    if not parts:
        return None
    cols = ["open_time", "close_time", "open", "high", "low", "close", "volume"]
    tables = []
    for p in parts:
        try:
            pf = pq.ParquetFile(str(p))
            t = pf.read(columns=cols)
        except Exception as exc:  # noqa: BLE001
            print(f"  ERROR reading {p}: {exc}", file=sys.stderr)
            continue
        tables.append(t)
    if not tables:
        return None
    combined = pa.concat_tables(tables, promote_options="default")
    open_time = combined.column("open_time").to_numpy()
    mask = (open_time >= start_ms) & (open_time <= end_ms)
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return None
    sort_idx = np.argsort(open_time[idx], kind="stable")
    final = idx[sort_idx]
    out = {
        "open_time": open_time[final],
        "close_time": combined.column("close_time").to_numpy()[final],
        "open": combined.column("open").to_numpy()[final],
        "high": combined.column("high").to_numpy()[final],
        "low": combined.column("low").to_numpy()[final],
        "close": combined.column("close").to_numpy()[final],
        "volume": combined.column("volume").to_numpy()[final],
    }
    return out


# ---------------------------------------------------------------------------
# Metric primitives
# ---------------------------------------------------------------------------


def rolling_median(values: np.ndarray, window: int) -> np.ndarray:
    """Rolling median over `window` previous values (excluding current);
    NaN until enough history.
    """
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    if n < window + 1:
        return out
    for i in range(window, n):
        out[i] = np.median(values[i - window : i])
    return out


def rolling_quantile(values: np.ndarray, window: int, q: float) -> np.ndarray:
    """Rolling quantile over `window` previous values (excluding current);
    NaN until enough history.
    """
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    if n < window + 1:
        return out
    for i in range(window, n):
        seg = values[i - window : i]
        seg = seg[np.isfinite(seg)]
        if seg.size == 0:
            continue
        out[i] = float(np.quantile(seg, q))
    return out


def compute_atr_wilder(
    h: np.ndarray, lo: np.ndarray, c: np.ndarray, window: int
) -> np.ndarray:
    n = len(c)
    tr = np.empty(n, dtype=np.float64)
    tr[0] = h[0] - lo[0]
    for i in range(1, n):
        a = h[i] - lo[i]
        b = abs(h[i] - c[i - 1])
        d = abs(lo[i] - c[i - 1])
        tr[i] = max(a, b, d)
    atr = np.full(n, np.nan, dtype=np.float64)
    if n < window:
        return atr
    atr[window - 1] = float(np.mean(tr[:window]))
    for i in range(window, n):
        atr[i] = (atr[i - 1] * (window - 1) + tr[i]) / window
    return atr


def compute_ema(values: np.ndarray, span: int) -> np.ndarray:
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    if n < span:
        return out
    alpha = 2.0 / (span + 1.0)
    seed = float(np.mean(values[:span]))
    out[span - 1] = seed
    for i in range(span, n):
        out[i] = alpha * values[i] + (1 - alpha) * out[i - 1]
    return out


def median_safe(arr: np.ndarray) -> float:
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    return float(np.median(arr))


def percentile_safe(arr: np.ndarray, q: float) -> float:
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    return float(np.percentile(arr, q))


# ---------------------------------------------------------------------------
# Run-length / persistence helpers
# ---------------------------------------------------------------------------


def run_lengths(states: np.ndarray, target: int) -> np.ndarray:
    """Return contiguous run lengths where states == target.

    `states` is a 1D integer array; transitions are contiguous segments of
    equal value. Returns a numpy array of run lengths (in bars) for runs
    matching `target`. Empty array if no such runs.
    """
    n = len(states)
    if n == 0:
        return np.empty(0, dtype=np.int64)
    out: list[int] = []
    i = 0
    while i < n:
        if states[i] == target:
            j = i
            while j < n and states[j] == target:
                j += 1
            out.append(j - i)
            i = j
        else:
            i += 1
    if not out:
        return np.empty(0, dtype=np.int64)
    return np.asarray(out, dtype=np.int64)


def transition_counts(states: np.ndarray, valid_mask: np.ndarray) -> dict[str, int]:
    """Count consecutive (state[t], state[t+1]) transitions among bars where
    BOTH t and t+1 satisfy valid_mask. Keys are encoded as 'A->B'.
    """
    counts: dict[str, int] = {}
    n = len(states)
    if n < 2:
        return counts
    for i in range(n - 1):
        if not (valid_mask[i] and valid_mask[i + 1]):
            continue
        a = int(states[i])
        b = int(states[i + 1])
        key = f"{a}->{b}"
        counts[key] = counts.get(key, 0) + 1
    return counts


def self_transition_probability(
    states: np.ndarray, valid_mask: np.ndarray, target: int
) -> float:
    """P(state[t+1] == target | state[t] == target) over valid pair indices."""
    n = len(states)
    if n < 2:
        return float("nan")
    base = 0
    same = 0
    for i in range(n - 1):
        if not (valid_mask[i] and valid_mask[i + 1]):
            continue
        if int(states[i]) == target:
            base += 1
            if int(states[i + 1]) == target:
                same += 1
    if base == 0:
        return float("nan")
    return same / base


# ---------------------------------------------------------------------------
# Main metric computation
# ---------------------------------------------------------------------------

# State encoding for trend states.
STATE_UNKNOWN = -1
STATE_UP = 1
STATE_DOWN = 2
STATE_MIXED = 0

STATE_NAME = {
    STATE_UNKNOWN: "UNKNOWN",
    STATE_UP: "UP",
    STATE_DOWN: "DOWN",
    STATE_MIXED: "MIXED",
}

# Slope state encoding.
SLOPE_FLAT = 0
SLOPE_POS = 1
SLOPE_NEG = 2

SLOPE_NAME = {
    SLOPE_FLAT: "FLAT",
    SLOPE_POS: "POS",
    SLOPE_NEG: "NEG",
}


def compute_trend_states(
    c: np.ndarray, ema50: np.ndarray, ema200: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Compute UP/DOWN/MIXED/UNKNOWN integer states and validity mask.

    UP      = close > EMA50 AND EMA50 > EMA200
    DOWN    = close < EMA50 AND EMA50 < EMA200
    MIXED   = otherwise (when both EMAs valid)
    UNKNOWN = either EMA invalid

    Returns (states, valid_mask). valid_mask is True where state is one of
    UP/DOWN/MIXED (i.e., both EMAs finite).
    """
    n = len(c)
    states = np.full(n, STATE_UNKNOWN, dtype=np.int8)
    valid_both = np.isfinite(ema50) & np.isfinite(ema200)
    up_mask = valid_both & (c > ema50) & (ema50 > ema200)
    down_mask = valid_both & (c < ema50) & (ema50 < ema200)
    mixed_mask = valid_both & ~up_mask & ~down_mask
    states[up_mask] = STATE_UP
    states[down_mask] = STATE_DOWN
    states[mixed_mask] = STATE_MIXED
    return states, valid_both


def compute_slope_states(ema50: np.ndarray, lag: int) -> tuple[np.ndarray, np.ndarray]:
    """EMA(50) discrete slope sign over `lag` bars: POS / NEG / FLAT.

    POS  = ema50[t] > ema50[t - lag]
    NEG  = ema50[t] < ema50[t - lag]
    FLAT = otherwise (equal)

    Returns (states, valid_mask) where valid_mask is True where both ema50[t]
    and ema50[t - lag] are finite.
    """
    n = len(ema50)
    states = np.full(n, SLOPE_FLAT, dtype=np.int8)
    valid = np.zeros(n, dtype=bool)
    if n <= lag:
        return states, valid
    prev = np.full(n, np.nan, dtype=np.float64)
    prev[lag:] = ema50[:-lag]
    valid = np.isfinite(prev) & np.isfinite(ema50)
    pos_mask = valid & (ema50 > prev)
    neg_mask = valid & (ema50 < prev)
    states[pos_mask] = SLOPE_POS
    states[neg_mask] = SLOPE_NEG
    return states, valid


def compute_kline_metrics(
    symbol: str, interval: str, df: dict
) -> tuple[
    dict[str, Any],            # coverage_row
    dict[str, Any],            # trend_state_row
    list[dict[str, Any]],      # trend_transition_rows (one per (from, to))
    dict[str, Any],            # slope_persistence_row
    list[dict[str, Any]],      # post_expansion_rows (per N)
    dict[str, Any],            # sign_persistence_row
    dict[str, Any],            # vol_regime_row
    list[dict[str, Any]],      # cost_continuation_rows (per N x threshold)
]:
    """Compute Phase 4af metrics for one (symbol, interval)."""
    h = df["high"]
    lo = df["low"]
    c = df["close"]
    o = df["open"]
    n = len(c)

    interval_ms = INTERVAL_MS[interval]
    expected_in_span = (
        ((int(df["open_time"][-1]) - int(df["open_time"][0])) // interval_ms) + 1
    )
    missing_in_span = int(max(0, expected_in_span - n))
    eligible, manifest_name = manifest_eligibility(symbol, interval)

    coverage_row: dict[str, Any] = {
        "symbol": symbol,
        "interval": interval,
        "manifest_name": manifest_name or "",
        "manifest_research_eligible": bool(eligible),
        "governance_scope": (
            "PASS"
            if eligible
            else (
                "Phase4ad_RuleB1_common_post_gap"
                if symbol in ("SOLUSDT", "XRPUSDT")
                else "PASS_or_legacy_phase2_eligible_via_v002"
            )
        ),
        "first_open_time_iso": ms_to_iso(int(df["open_time"][0])),
        "last_open_time_iso": ms_to_iso(int(df["open_time"][-1])),
        "first_open_time_ms": int(df["open_time"][0]),
        "last_open_time_ms": int(df["open_time"][-1]),
        "bar_count": int(n),
        "expected_bars_in_observed_span": int(expected_in_span),
        "missing_bars_in_observed_span": missing_in_span,
    }

    # ---- Trend states ------------------------------------------------
    ema50 = compute_ema(c, EMA_FAST)
    ema200 = compute_ema(c, EMA_SLOW)
    states, valid_both = compute_trend_states(c, ema50, ema200)

    n_unknown = int(np.sum(states == STATE_UNKNOWN))
    n_up = int(np.sum(states == STATE_UP))
    n_down = int(np.sum(states == STATE_DOWN))
    n_mixed = int(np.sum(states == STATE_MIXED))
    n_total = n
    n_valid_both = int(np.sum(valid_both))

    up_runs = run_lengths(states, STATE_UP)
    down_runs = run_lengths(states, STATE_DOWN)
    mixed_runs = run_lengths(states, STATE_MIXED)

    trend_state_row: dict[str, Any] = {
        "symbol": symbol,
        "interval": interval,
        "n_bars": n_total,
        "n_valid_both_emas": n_valid_both,
        "frac_up": float(n_up / max(n_total, 1)),
        "frac_down": float(n_down / max(n_total, 1)),
        "frac_mixed": float(n_mixed / max(n_total, 1)),
        "frac_unknown": float(n_unknown / max(n_total, 1)),
        "up_run_count": int(up_runs.size),
        "down_run_count": int(down_runs.size),
        "mixed_run_count": int(mixed_runs.size),
        "up_run_median_bars": (
            float(np.median(up_runs)) if up_runs.size else float("nan")
        ),
        "up_run_mean_bars": (
            float(np.mean(up_runs)) if up_runs.size else float("nan")
        ),
        "up_run_p75_bars": (
            float(np.percentile(up_runs, 75)) if up_runs.size else float("nan")
        ),
        "up_run_max_bars": int(np.max(up_runs)) if up_runs.size else 0,
        "down_run_median_bars": (
            float(np.median(down_runs)) if down_runs.size else float("nan")
        ),
        "down_run_mean_bars": (
            float(np.mean(down_runs)) if down_runs.size else float("nan")
        ),
        "down_run_p75_bars": (
            float(np.percentile(down_runs, 75)) if down_runs.size else float("nan")
        ),
        "down_run_max_bars": int(np.max(down_runs)) if down_runs.size else 0,
        "mixed_run_median_bars": (
            float(np.median(mixed_runs)) if mixed_runs.size else float("nan")
        ),
        "mixed_run_mean_bars": (
            float(np.mean(mixed_runs)) if mixed_runs.size else float("nan")
        ),
        "p_up_self_transition": self_transition_probability(states, valid_both, STATE_UP),
        "p_down_self_transition": self_transition_probability(states, valid_both, STATE_DOWN),
        "p_mixed_self_transition": self_transition_probability(states, valid_both, STATE_MIXED),
    }

    # ---- Trend-state transition rows ---------------------------------
    tcounts = transition_counts(states, valid_both)
    trend_transition_rows: list[dict[str, Any]] = []
    for a_state, a_name in STATE_NAME.items():
        if a_state == STATE_UNKNOWN:
            continue
        for b_state, b_name in STATE_NAME.items():
            if b_state == STATE_UNKNOWN:
                continue
            key = f"{a_state}->{b_state}"
            trend_transition_rows.append(
                {
                    "symbol": symbol,
                    "interval": interval,
                    "from_state": a_name,
                    "to_state": b_name,
                    "count": int(tcounts.get(key, 0)),
                }
            )

    # ---- Slope persistence -------------------------------------------
    slope_states, slope_valid = compute_slope_states(ema50, EMA_SLOPE_LAG)
    n_slope_valid = int(np.sum(slope_valid))
    n_slope_pos = int(np.sum(slope_valid & (slope_states == SLOPE_POS)))
    n_slope_neg = int(np.sum(slope_valid & (slope_states == SLOPE_NEG)))
    n_slope_flat = int(np.sum(slope_valid & (slope_states == SLOPE_FLAT)))
    pos_runs = run_lengths(np.where(slope_valid, slope_states, -99), SLOPE_POS)
    neg_runs = run_lengths(np.where(slope_valid, slope_states, -99), SLOPE_NEG)
    slope_persistence_row: dict[str, Any] = {
        "symbol": symbol,
        "interval": interval,
        "n_slope_valid": n_slope_valid,
        "frac_slope_pos": float(n_slope_pos / max(n_slope_valid, 1)),
        "frac_slope_neg": float(n_slope_neg / max(n_slope_valid, 1)),
        "frac_slope_flat": float(n_slope_flat / max(n_slope_valid, 1)),
        "slope_pos_run_count": int(pos_runs.size),
        "slope_neg_run_count": int(neg_runs.size),
        "slope_pos_run_median_bars": float(np.median(pos_runs)) if pos_runs.size else float("nan"),
        "slope_neg_run_median_bars": float(np.median(neg_runs)) if neg_runs.size else float("nan"),
        "p_slope_pos_self_transition": self_transition_probability(
            slope_states, slope_valid, SLOPE_POS
        ),
        "p_slope_neg_self_transition": self_transition_probability(
            slope_states, slope_valid, SLOPE_NEG
        ),
    }

    # ---- Post-expansion follow-through -------------------------------
    range_bps = (h - lo) / np.maximum(c, EPSILON) * 1e4
    range_med = rolling_median(range_bps, ROLLING_WINDOW)
    valid_med = np.isfinite(range_med)

    # Forward log returns in bps for each forward window N (using close
    # of the bar t+N relative to close of bar t; thus only valid when
    # t + N < n).
    log_close = np.log(np.maximum(c, EPSILON))
    forward_returns_bps: dict[int, np.ndarray] = {}
    forward_valid: dict[int, np.ndarray] = {}
    for N in FORWARD_WINDOWS:
        fr = np.full(n, np.nan, dtype=np.float64)
        if n > N:
            fr[: n - N] = (log_close[N:] - log_close[: n - N]) * 1e4
        forward_returns_bps[N] = fr
        forward_valid[N] = np.isfinite(fr)

    # Expansion event mask (using only the highest predeclared multiplier).
    expansion_thresh_mult = EXPANSION_THRESHOLD_MULTIPLIERS[0]
    expansion_mask_full = valid_med & (range_bps > expansion_thresh_mult * range_med)

    # Expansion direction: bar close >= open is "up", else "down".
    bar_dir_up = c >= o

    post_expansion_rows: list[dict[str, Any]] = []
    for N in FORWARD_WINDOWS:
        valid_event = expansion_mask_full & forward_valid[N]
        n_events = int(np.sum(valid_event))
        if n_events == 0:
            row = {
                "symbol": symbol,
                "interval": interval,
                "forward_window_bars": N,
                "expansion_threshold_mult": expansion_thresh_mult,
                "expansion_event_count": 0,
                "median_forward_return_bps": float("nan"),
                "median_abs_forward_return_bps": float("nan"),
                "frac_same_direction_followthrough": float("nan"),
                "frac_opposite_direction_reversal": float("nan"),
            }
            for thresh in PERSISTENCE_MOVE_THRESHOLDS_BPS:
                row[f"frac_same_direction_gt_{int(thresh)}bps"] = float("nan")
            row["unconditional_frac_abs_gt_16bps"] = float("nan")
            post_expansion_rows.append(row)
            continue
        fr = forward_returns_bps[N]
        # Same-direction: if bar up then forward > 0, if bar down then forward < 0.
        # Equal forward = 0 counts as neither.
        same_dir = np.zeros(n, dtype=bool)
        opp_dir = np.zeros(n, dtype=bool)
        up_event = valid_event & bar_dir_up
        down_event = valid_event & ~bar_dir_up
        same_dir |= up_event & (fr > 0)
        same_dir |= down_event & (fr < 0)
        opp_dir |= up_event & (fr < 0)
        opp_dir |= down_event & (fr > 0)
        n_same = int(np.sum(same_dir))
        n_opp = int(np.sum(opp_dir))
        median_fr = float(np.median(fr[valid_event]))
        median_abs_fr = float(np.median(np.abs(fr[valid_event])))

        row = {
            "symbol": symbol,
            "interval": interval,
            "forward_window_bars": N,
            "expansion_threshold_mult": expansion_thresh_mult,
            "expansion_event_count": n_events,
            "median_forward_return_bps": median_fr,
            "median_abs_forward_return_bps": median_abs_fr,
            "frac_same_direction_followthrough": float(n_same / n_events),
            "frac_opposite_direction_reversal": float(n_opp / n_events),
        }
        # Same-direction-with-magnitude thresholds.
        for thresh in PERSISTENCE_MOVE_THRESHOLDS_BPS:
            same_thresh = np.zeros(n, dtype=bool)
            same_thresh |= up_event & (fr > thresh)
            same_thresh |= down_event & (fr < -thresh)
            row[f"frac_same_direction_gt_{int(thresh)}bps"] = float(
                int(np.sum(same_thresh)) / n_events
            )
        # Unconditional reference frequency: fraction of bars where |forward| > 16 bps.
        valid_uncond = forward_valid[N]
        n_valid_uncond = int(np.sum(valid_uncond))
        if n_valid_uncond > 0:
            row["unconditional_frac_abs_gt_16bps"] = float(
                int(np.sum(valid_uncond & (np.abs(fr) > 16.0))) / n_valid_uncond
            )
        else:
            row["unconditional_frac_abs_gt_16bps"] = float("nan")
        post_expansion_rows.append(row)

    # ---- Directional autocorrelation / sign persistence --------------
    # Close-to-close log return.
    ret = np.zeros(n, dtype=np.float64)
    if n > 1:
        ret[1:] = log_close[1:] - log_close[:-1]
    sign = np.sign(ret).astype(np.int8)  # -1 / 0 / +1

    # frac of bars where sign repeats next bar (excluding zero-sign bars).
    def _frac_sign_repeats_next(s: np.ndarray, k: int) -> float:
        """Fraction of indices i in [1, n-k) where s[i] != 0 and
        s[i+1] == s[i] AND ... AND s[i+k] == s[i]."""
        if n < k + 2:
            return float("nan")
        base = 0
        same = 0
        for i in range(1, n - k):
            si = s[i]
            if si == 0:
                continue
            base += 1
            ok = True
            for j in range(1, k + 1):
                if s[i + j] != si:
                    ok = False
                    break
            if ok:
                same += 1
        if base == 0:
            return float("nan")
        return same / base

    frac_repeat_1 = _frac_sign_repeats_next(sign, 1)
    frac_repeat_2 = _frac_sign_repeats_next(sign, 2)
    frac_repeat_4 = _frac_sign_repeats_next(sign, 4)

    def _autocorr(r: np.ndarray, lag: int) -> float:
        if n <= lag + 1:
            return float("nan")
        a = r[lag:]
        b = r[: n - lag]
        if a.size == 0 or b.size == 0:
            return float("nan")
        a_mean = float(np.mean(a))
        b_mean = float(np.mean(b))
        a_dev = a - a_mean
        b_dev = b - b_mean
        denom = float(np.sqrt(np.sum(a_dev * a_dev) * np.sum(b_dev * b_dev)))
        if denom < EPSILON:
            return float("nan")
        return float(np.sum(a_dev * b_dev) / denom)

    sign_persistence_row: dict[str, Any] = {
        "symbol": symbol,
        "interval": interval,
        "n_bars": n,
        "frac_sign_repeats_next_1": frac_repeat_1,
        "frac_sign_repeats_next_2": frac_repeat_2,
        "frac_sign_repeats_next_4": frac_repeat_4,
        "lag1_return_autocorr": _autocorr(ret, 1),
        "lag2_return_autocorr": _autocorr(ret, 2),
        "lag4_return_autocorr": _autocorr(ret, 4),
    }

    # ---- Volatility-regime persistence -------------------------------
    atr = compute_atr_wilder(h, lo, c, ATR_WINDOW)
    atr_bps = atr / np.maximum(c, EPSILON) * 1e4
    atr_q = rolling_quantile(atr_bps, ROLLING_WINDOW, VOL_REGIME_QUANTILE)
    vol_valid = np.isfinite(atr_bps) & np.isfinite(atr_q)
    high_vol = np.zeros(n, dtype=np.int8)
    high_vol_mask = vol_valid & (atr_bps > atr_q)
    high_vol[high_vol_mask] = 1
    n_vol_valid = int(np.sum(vol_valid))
    n_high = int(np.sum(high_vol_mask))
    high_runs = run_lengths(np.where(vol_valid, high_vol, -99).astype(np.int8), 1)

    # Overlap of high-vol with trend states.
    overlap_up = int(np.sum(high_vol_mask & (states == STATE_UP)))
    overlap_down = int(np.sum(high_vol_mask & (states == STATE_DOWN)))
    overlap_mixed = int(np.sum(high_vol_mask & (states == STATE_MIXED)))

    vol_regime_row: dict[str, Any] = {
        "symbol": symbol,
        "interval": interval,
        "n_vol_valid": n_vol_valid,
        "frac_high_vol": float(n_high / max(n_vol_valid, 1)),
        "high_vol_run_count": int(high_runs.size),
        "high_vol_run_median_bars": (
            float(np.median(high_runs)) if high_runs.size else float("nan")
        ),
        "high_vol_run_p75_bars": (
            float(np.percentile(high_runs, 75)) if high_runs.size else float("nan")
        ),
        "p_high_vol_self_transition": self_transition_probability(
            high_vol, vol_valid, 1
        ),
        "high_vol_overlap_up": overlap_up,
        "high_vol_overlap_down": overlap_down,
        "high_vol_overlap_mixed": overlap_mixed,
    }

    # ---- Cost-adjusted continuation sufficiency ----------------------
    cost_continuation_rows: list[dict[str, Any]] = []
    for N in FORWARD_WINDOWS:
        fr = forward_returns_bps[N]
        v_full = forward_valid[N]
        n_v_full = int(np.sum(v_full))
        # Conditional masks.
        v_up = v_full & (states == STATE_UP)
        v_down = v_full & (states == STATE_DOWN)
        n_v_up = int(np.sum(v_up))
        n_v_down = int(np.sum(v_down))
        v_post_event = expansion_mask_full & v_full
        n_v_post = int(np.sum(v_post_event))

        for thresh in PERSISTENCE_MOVE_THRESHOLDS_BPS:
            row: dict[str, Any] = {
                "symbol": symbol,
                "interval": interval,
                "forward_window_bars": N,
                "threshold_bps": thresh,
            }
            if n_v_full > 0:
                row["unconditional_frac_abs_gt_thresh"] = float(
                    int(np.sum(v_full & (np.abs(fr) > thresh))) / n_v_full
                )
            else:
                row["unconditional_frac_abs_gt_thresh"] = float("nan")
            if n_v_up > 0:
                row["up_state_frac_abs_gt_thresh"] = float(
                    int(np.sum(v_up & (np.abs(fr) > thresh))) / n_v_up
                )
            else:
                row["up_state_frac_abs_gt_thresh"] = float("nan")
            if n_v_down > 0:
                row["down_state_frac_abs_gt_thresh"] = float(
                    int(np.sum(v_down & (np.abs(fr) > thresh))) / n_v_down
                )
            else:
                row["down_state_frac_abs_gt_thresh"] = float("nan")
            if n_v_post > 0:
                row["post_expansion_frac_abs_gt_thresh"] = float(
                    int(np.sum(v_post_event & (np.abs(fr) > thresh))) / n_v_post
                )
            else:
                row["post_expansion_frac_abs_gt_thresh"] = float("nan")
            row["n_unconditional"] = n_v_full
            row["n_up_state"] = n_v_up
            row["n_down_state"] = n_v_down
            row["n_post_expansion"] = n_v_post
            cost_continuation_rows.append(row)

    return (
        coverage_row,
        trend_state_row,
        trend_transition_rows,
        slope_persistence_row,
        post_expansion_rows,
        sign_persistence_row,
        vol_regime_row,
        cost_continuation_rows,
    )


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(rows[0].keys())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_json(obj: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 4af regime persistence analysis")
    p.add_argument("--start", default="2022-04-03", help="YYYY-MM-DD UTC")
    p.add_argument("--end", default="2026-04-30", help="YYYY-MM-DD UTC (inclusive)")
    p.add_argument("--symbols", nargs="+", default=list(DEFAULT_SYMBOLS))
    p.add_argument("--intervals", nargs="+", default=list(DEFAULT_INTERVALS))
    p.add_argument("--out-dir", default=str(DEFAULT_OUT))
    return p.parse_args()


def main() -> int:
    args = parse_args()

    start_ms = parse_ymd_to_ms_utc(args.start, end_of_day=False)
    end_ms = parse_ymd_to_ms_utc(args.end, end_of_day=True)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tables_dir = out_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    print("Phase 4af regime-continuity / directional-persistence analysis")
    print(f"  start    : {args.start} ({start_ms})")
    print(f"  end      : {args.end} ({end_ms}) inclusive")
    print(f"  symbols  : {args.symbols}")
    print(f"  intervals: {args.intervals}")
    print(f"  out_dir  : {out_dir}")
    print()

    coverage_rows: list[dict[str, Any]] = []
    trend_state_rows: list[dict[str, Any]] = []
    trend_transition_rows: list[dict[str, Any]] = []
    slope_rows: list[dict[str, Any]] = []
    post_expansion_rows: list[dict[str, Any]] = []
    sign_persistence_rows: list[dict[str, Any]] = []
    vol_regime_rows: list[dict[str, Any]] = []
    cost_continuation_rows: list[dict[str, Any]] = []
    omitted: list[dict[str, Any]] = []

    for symbol in args.symbols:
        for interval in args.intervals:
            print(f"  loading {symbol} {interval} ...")
            df = load_klines(symbol, interval, start_ms, end_ms)
            if df is None or len(df["open_time"]) == 0:
                print(f"    NO DATA in window for {symbol} {interval}")
                omitted.append(
                    {
                        "symbol": symbol,
                        "interval": interval,
                        "reason": "no normalized data in analysis window",
                    }
                )
                continue
            (
                cov_row,
                trend_row,
                t_trans_rows,
                slope_row,
                pe_rows,
                sp_row,
                vr_row,
                cc_rows,
            ) = compute_kline_metrics(symbol, interval, df)
            coverage_rows.append(cov_row)
            trend_state_rows.append(trend_row)
            trend_transition_rows.extend(t_trans_rows)
            slope_rows.append(slope_row)
            post_expansion_rows.extend(pe_rows)
            sign_persistence_rows.append(sp_row)
            vol_regime_rows.append(vr_row)
            cost_continuation_rows.extend(cc_rows)
            print(
                f"    bars={cov_row['bar_count']} "
                f"frac_up={trend_row['frac_up']:.3f} "
                f"frac_down={trend_row['frac_down']:.3f} "
                f"p_up_self={trend_row['p_up_self_transition']:.3f}"
            )

    # Cross-symbol rankings.
    rank_rows: list[dict[str, Any]] = []

    def _rank_key(value: Any) -> float:
        try:
            v = float(value)
        except (TypeError, ValueError):
            return float("inf")
        if not np.isfinite(v):
            return float("inf")
        return v

    rank_specs = [
        ("trend_state", trend_state_rows, "up_run_median_bars", "median_up_run_bars"),
        ("trend_state", trend_state_rows, "down_run_median_bars", "median_down_run_bars"),
        ("trend_state", trend_state_rows, "p_up_self_transition", "p_up_self"),
        ("trend_state", trend_state_rows, "p_down_self_transition", "p_down_self"),
        ("trend_state", trend_state_rows, "frac_up", "frac_up"),
        ("trend_state", trend_state_rows, "frac_down", "frac_down"),
        ("vol_regime", vol_regime_rows, "p_high_vol_self_transition", "p_high_vol_self"),
        ("vol_regime", vol_regime_rows, "frac_high_vol", "frac_high_vol"),
        (
            "sign_persistence",
            sign_persistence_rows,
            "frac_sign_repeats_next_1",
            "frac_sign_repeats_1",
        ),
        (
            "sign_persistence",
            sign_persistence_rows,
            "lag1_return_autocorr",
            "lag1_autocorr",
        ),
    ]

    for table_name, source, metric_key, label in rank_specs:
        for interval in args.intervals:
            rows_at_int = [r for r in source if r.get("interval") == interval]
            sorted_rows = sorted(rows_at_int, key=lambda r, mk=metric_key: _rank_key(r.get(mk)))
            for rank, r in enumerate(sorted_rows, start=1):
                rank_rows.append(
                    {
                        "table": table_name,
                        "metric": metric_key,
                        "label": label,
                        "interval": interval,
                        "rank_low_to_high": rank,
                        "symbol": r["symbol"],
                        "value": r.get(metric_key, float("nan")),
                    }
                )

    # Post-expansion ranking at N=4 and N=8 across thresholds and frac fields.
    pe_rank_fields = [
        ("frac_same_direction_followthrough", "same_dir_followthrough"),
        ("frac_same_direction_gt_16bps", "same_dir_gt_16bps"),
        ("frac_same_direction_gt_24bps", "same_dir_gt_24bps"),
        ("frac_same_direction_gt_32bps", "same_dir_gt_32bps"),
    ]
    for N in (4, 8):
        rows_at_N = [r for r in post_expansion_rows if r.get("forward_window_bars") == N]
        for interval in args.intervals:
            rows_at_int = [r for r in rows_at_N if r.get("interval") == interval]
            for metric_key, label in pe_rank_fields:
                sorted_rows = sorted(
                    rows_at_int,
                    key=lambda r, mk=metric_key: _rank_key(r.get(mk)),
                )
                for rank, r in enumerate(sorted_rows, start=1):
                    rank_rows.append(
                        {
                            "table": "post_expansion",
                            "metric": f"{metric_key}__N{N}",
                            "label": f"{label}__N{N}",
                            "interval": interval,
                            "rank_low_to_high": rank,
                            "symbol": r["symbol"],
                            "value": r.get(metric_key, float("nan")),
                        }
                    )

    # Cost-continuation ranking at N=4, threshold=16 bps (cost-adjusted reference).
    cc_rank_subset = [
        r for r in cost_continuation_rows
        if r.get("forward_window_bars") == 4 and r.get("threshold_bps") == 16.0
    ]
    for interval in args.intervals:
        rows_at_int = [r for r in cc_rank_subset if r.get("interval") == interval]
        for metric_key, label in [
            ("unconditional_frac_abs_gt_thresh", "unconditional_abs_gt_16_N4"),
            ("up_state_frac_abs_gt_thresh", "up_state_abs_gt_16_N4"),
            ("post_expansion_frac_abs_gt_thresh", "post_expansion_abs_gt_16_N4"),
        ]:
            sorted_rows = sorted(rows_at_int, key=lambda r, mk=metric_key: _rank_key(r.get(mk)))
            for rank, r in enumerate(sorted_rows, start=1):
                rank_rows.append(
                    {
                        "table": "cost_continuation",
                        "metric": metric_key,
                        "label": label,
                        "interval": interval,
                        "rank_low_to_high": rank,
                        "symbol": r["symbol"],
                        "value": r.get(metric_key, float("nan")),
                    }
                )

    # Write tables.
    write_csv(coverage_rows, tables_dir / "coverage.csv")
    write_csv(trend_state_rows, tables_dir / "trend_state_persistence.csv")
    write_csv(trend_transition_rows, tables_dir / "trend_state_transitions.csv")
    write_csv(slope_rows, tables_dir / "ema_slope_persistence.csv")
    write_csv(post_expansion_rows, tables_dir / "post_expansion_followthrough.csv")
    write_csv(sign_persistence_rows, tables_dir / "sign_persistence.csv")
    write_csv(vol_regime_rows, tables_dir / "vol_regime_persistence.csv")
    write_csv(cost_continuation_rows, tables_dir / "cost_continuation_sufficiency.csv")
    write_csv(rank_rows, tables_dir / "cross_symbol_rankings.csv")
    write_csv(omitted, tables_dir / "omitted_datasets.csv")

    # Run metadata.
    run_meta = {
        "phase": "Phase 4af regime-continuity / directional-persistence",
        "start_utc": args.start,
        "end_utc_inclusive": args.end,
        "start_ms": start_ms,
        "end_ms_inclusive": end_ms,
        "symbols": list(args.symbols),
        "intervals": list(args.intervals),
        "ema_fast": EMA_FAST,
        "ema_slow": EMA_SLOW,
        "ema_slope_lag": EMA_SLOPE_LAG,
        "atr_window": ATR_WINDOW,
        "rolling_window_bars": ROLLING_WINDOW,
        "forward_windows_bars": list(FORWARD_WINDOWS),
        "persistence_move_thresholds_bps": list(PERSISTENCE_MOVE_THRESHOLDS_BPS),
        "expansion_threshold_multipliers": list(EXPANSION_THRESHOLD_MULTIPLIERS),
        "vol_regime_quantile": VOL_REGIME_QUANTILE,
        "high_cost_bps_per_side": HIGH_COST_BPS_PER_SIDE,
        "round_trip_cost_bps": ROUND_TRIP_COST_BPS,
        "phase4ad_rule_b1_applied": True,
        "phase4ad_rule_a_applied": False,
        "mark_price_used": False,
        "metrics_or_oi_used": False,
        "aggtrades_used": False,
        "funding_used": False,
        "command": " ".join(sys.argv),
        "no_credentials_confirmation": True,
        "private_endpoint_used": False,
        "authenticated_api_used": False,
        "websocket_used": False,
        "user_stream_used": False,
        "exchange_write_attempted": False,
    }
    write_json(run_meta, out_dir / "run_metadata.json")

    print()
    print("Phase 4af analysis complete.")
    print(f"  cells              : {len(trend_state_rows)}")
    print(f"  omitted datasets   : {len(omitted)}")
    print(f"  coverage rows      : {len(coverage_rows)}")
    print(f"  trend state rows   : {len(trend_state_rows)}")
    print(f"  trend trans rows   : {len(trend_transition_rows)}")
    print(f"  slope rows         : {len(slope_rows)}")
    print(f"  post-expansion rows: {len(post_expansion_rows)}")
    print(f"  sign rows          : {len(sign_persistence_rows)}")
    print(f"  vol regime rows    : {len(vol_regime_rows)}")
    print(f"  cost-continuation  : {len(cost_continuation_rows)}")
    print(f"  ranking rows       : {len(rank_rows)}")
    print(f"  outputs at         : {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
