"""Phase 4ae - Alt-Symbol Substrate-Feasibility Analysis (descriptive only).

Authority: Phase 4ad (alt-symbol gap-governance and scope-revision memo;
Rule A mark-price invalid-window exclusion; Rule B SOL/XRP early-2022 kline
gap scope policy with B1 / B2 / B3; Rule C PASS-only subset; merged
10f122e). Phase 4ac (alt-symbol public data acquisition; merged 3478d05).
Phase 4ab (alt-symbol data-requirements / feasibility memo). Phase 4aa
(alt-symbol market-selection / admissibility memo).

Brief: analysis-and-docs only. Reads existing local normalized Parquet only.
No network I/O. No Binance API. No `data.binance.vision`. No authenticated
REST. No private endpoints. No public-endpoint code calls. No user stream
/ WebSocket / listenKey. No credentials. No `.env`. No MCP / Graphify /
`.mcp.json`. No data acquisition. No data modification. No manifest
creation or modification. No backtest. No diagnostic / Q1-Q7 rerun. No
strategy candidate. No hypothesis-spec / strategy-spec / backtest-plan.
No `src/prometheus/` modification. No test modification. No existing-script
modification. No retained verdict revised. No project lock changed.

Default scope (Phase 4ae brief):
    Symbols   : BTCUSDT  ETHUSDT  SOLUSDT  XRPUSDT  ADAUSDT
    Intervals : 15m  30m  1h  4h
    Start     : 2022-04-03 00:00 UTC  (Phase 4ad Rule B1 common post-gap)
    End       : 2026-04-30 23:59:59 UTC (cell ends at last available bar)
    Cost lock : 8 bps HIGH per side; round-trip = 16 bps; §11.6 preserved
    Output    : data/research/phase4ae/  (gitignored; not committed)

Predeclared descriptive thresholds (NOT optimized):
    EXPANSION_RANGE_THRESHOLDS   = (1.0, 1.5)  multiples of rolling median range
    EXPANSION_ABSRET_THRESHOLDS  = (1.0, 1.5)  multiples of rolling median |ret|
    WICK_FRACTION_THRESHOLD      = 0.5
    ROLLING_WINDOW_BARS          = 96
    ATR_WINDOW                   = 20
    EMA_FAST                     = 50
    EMA_SLOW                     = 200

All metrics in this script are descriptive substrate-feasibility metrics
ONLY. They are NOT strategy signals, NOT backtests, NOT entry/exit rules,
NOT threshold-optimization candidates, and NOT Q1-Q7 stop-pathology
diagnostics.
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
NORM_FUNDING_ROOT = REPO_ROOT / "data" / "normalized" / "funding"
LEGACY_FUNDING_ROOT = REPO_ROOT / "data" / "normalized" / "funding_rate"
DEFAULT_OUT = REPO_ROOT / "data" / "research" / "phase4ae"
MANIFESTS_ROOT = REPO_ROOT / "data" / "manifests"

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT")
DEFAULT_INTERVALS = ("15m", "30m", "1h", "4h")

INTERVAL_MS = {
    "15m": 15 * 60 * 1000,
    "30m": 30 * 60 * 1000,
    "1h": 60 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
}

# Cost lock from §11.6 (preserved verbatim by Phase 4ae).
HIGH_COST_BPS_PER_SIDE = 8.0
ROUND_TRIP_COST_BPS = 16.0

# Predeclared descriptive thresholds. Fixed before analysis. Not optimized.
EXPANSION_RANGE_THRESHOLDS = (1.0, 1.5)
EXPANSION_ABSRET_THRESHOLDS = (1.0, 1.5)
WICK_FRACTION_THRESHOLD = 0.5
ROLLING_WINDOW_BARS = 96
ATR_WINDOW = 20
EMA_FAST = 50
EMA_SLOW = 200

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

    Returns (eligible: bool, manifest_name: str | None). If multiple manifests
    exist (e.g., __v001 and __v002), prefer __v002 then __v001.
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


def load_funding(symbol: str, start_ms: int, end_ms: int) -> dict | None:
    """Read funding events for symbol from either the Phase 2 legacy
    `funding_rate/` path (BTC/ETH) or the Phase 4ac `funding/` path (alts).

    Returns dict with `ts_ms` and `rate` numpy arrays (rate in fraction, e.g.
    0.0001 = 1 bp); or None if not found.
    """
    # Try Phase 4ac path first.
    base_4ac = NORM_FUNDING_ROOT / f"symbol={symbol}"
    base_2 = LEGACY_FUNDING_ROOT / f"symbol={symbol}"

    rows_ts: list[np.ndarray] = []
    rows_rate: list[np.ndarray] = []

    if base_4ac.exists():
        for p in sorted(base_4ac.rglob("part-0000.parquet")):
            try:
                pf = pq.ParquetFile(str(p))
                t = pf.read(columns=["calc_time", "last_funding_rate"])
            except Exception as exc:  # noqa: BLE001
                print(f"  ERROR reading {p}: {exc}", file=sys.stderr)
                continue
            rows_ts.append(t.column("calc_time").to_numpy())
            rows_rate.append(t.column("last_funding_rate").to_numpy())
    elif base_2.exists():
        for p in sorted(base_2.rglob("part-0000.parquet")):
            try:
                pf = pq.ParquetFile(str(p))
                t = pf.read(columns=["funding_time", "funding_rate"])
            except Exception as exc:  # noqa: BLE001
                print(f"  ERROR reading {p}: {exc}", file=sys.stderr)
                continue
            rows_ts.append(t.column("funding_time").to_numpy())
            rows_rate.append(t.column("funding_rate").to_numpy())
    else:
        return None

    if not rows_ts:
        return None
    ts = np.concatenate(rows_ts)
    rate = np.concatenate(rows_rate)
    mask = (ts >= start_ms) & (ts <= end_ms)
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return None
    sort_idx = np.argsort(ts[idx], kind="stable")
    final = idx[sort_idx]
    return {"ts_ms": ts[final], "rate": rate[final]}


# ---------------------------------------------------------------------------
# Metric computations
# ---------------------------------------------------------------------------


def rolling_median(values: np.ndarray, window: int) -> np.ndarray:
    """Rolling median over `window` previous values (excluding current);
    NaN until enough history. Uses a simple O(n*window) approach that is
    fine for our dataset sizes.
    """
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    if n < window + 1:
        return out
    for i in range(window, n):
        out[i] = np.median(values[i - window : i])
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


def percentile_safe(arr: np.ndarray, q: float) -> float:
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    return float(np.percentile(arr, q))


def median_safe(arr: np.ndarray) -> float:
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    return float(np.median(arr))


def compute_kline_metrics(symbol: str, interval: str, df: dict) -> dict[str, Any]:
    """Compute all descriptive substrate metrics for one (symbol, interval)."""
    h = df["high"]
    l = df["low"]  # noqa: E741 (matches OHLC convention)
    c = df["close"]
    o = df["open"]
    v = df["volume"]
    n = len(c)

    # Range bps (relative to close).
    range_bps = (h - l) / np.maximum(c, EPSILON) * 1e4
    # True range bps using prev close.
    prev_c = np.empty(n, dtype=np.float64)
    prev_c[0] = c[0]
    prev_c[1:] = c[:-1]
    tr = np.maximum.reduce(
        [h - l, np.abs(h - prev_c), np.abs(l - prev_c)]
    )
    tr_bps = tr / np.maximum(c, EPSILON) * 1e4

    # ATR(20) Wilder, in bps relative to close.
    atr = compute_atr_wilder(h, l, c, ATR_WINDOW)
    atr_bps = atr / np.maximum(c, EPSILON) * 1e4

    # Close-to-close absolute returns in bps.
    abs_ret_bps = np.zeros(n, dtype=np.float64)
    abs_ret_bps[1:] = np.abs(np.log(np.maximum(c[1:], EPSILON) / np.maximum(c[:-1], EPSILON))) * 1e4

    # Wick fractions.
    den = np.maximum(h - l, EPSILON)
    upper_wick = (h - np.maximum(o, c)) / den
    lower_wick = (np.minimum(o, c) - l) / den
    upper_wick = np.clip(upper_wick, 0.0, 1.0)
    lower_wick = np.clip(lower_wick, 0.0, 1.0)

    # EMA regime.
    ema50 = compute_ema(c, EMA_FAST)
    ema200 = compute_ema(c, EMA_SLOW)
    valid_ema50 = np.isfinite(ema50)
    valid_ema200 = np.isfinite(ema200)
    valid_both_emas = valid_ema50 & valid_ema200
    # Discrete EMA(50) slope: today's EMA50 vs 3 bars earlier EMA50.
    ema50_slope_pos = np.zeros(n, dtype=bool)
    if n > 3:
        prev_ema50 = np.full(n, np.nan, dtype=np.float64)
        prev_ema50[3:] = ema50[:-3]
        ema50_slope_pos = (ema50 > prev_ema50) & np.isfinite(prev_ema50) & np.isfinite(ema50)

    # Rolling medians for expansion proxies (excluding current).
    range_med = rolling_median(range_bps, ROLLING_WINDOW_BARS)
    absret_med = rolling_median(abs_ret_bps, ROLLING_WINDOW_BARS)

    # Notional proxy.
    notional = c * v

    # Aggregate metrics.
    metrics: dict[str, Any] = {
        "symbol": symbol,
        "interval": interval,
        "bar_count": n,
        "first_open_time_ms": int(df["open_time"][0]),
        "last_open_time_ms": int(df["open_time"][-1]),
        "first_open_time_iso": ms_to_iso(int(df["open_time"][0])),
        "last_open_time_iso": ms_to_iso(int(df["open_time"][-1])),
        # Range / TR / ATR distributions in bps.
        "range_bps_median": median_safe(range_bps),
        "range_bps_p25": percentile_safe(range_bps, 25),
        "range_bps_p75": percentile_safe(range_bps, 75),
        "tr_bps_median": median_safe(tr_bps),
        "atr_bps_median": median_safe(atr_bps),
        "atr_bps_p25": percentile_safe(atr_bps, 25),
        "atr_bps_p75": percentile_safe(atr_bps, 75),
        # Cost ratios (round-trip = 2 × HIGH per-side).
        "cost_oneway_over_range_median": HIGH_COST_BPS_PER_SIDE
        / max(median_safe(range_bps), EPSILON),
        "cost_roundtrip_over_range_median": ROUND_TRIP_COST_BPS
        / max(median_safe(range_bps), EPSILON),
        "cost_roundtrip_over_atr_median": ROUND_TRIP_COST_BPS
        / max(median_safe(atr_bps), EPSILON),
        # Wick proxies.
        "upper_wick_fraction_median": median_safe(upper_wick),
        "lower_wick_fraction_median": median_safe(lower_wick),
        "frac_bars_upper_wick_gt_thresh": float(
            np.sum(upper_wick > WICK_FRACTION_THRESHOLD) / max(n, 1)
        ),
        "frac_bars_lower_wick_gt_thresh": float(
            np.sum(lower_wick > WICK_FRACTION_THRESHOLD) / max(n, 1)
        ),
        "frac_bars_both_wicks_elevated": float(
            np.sum(
                (upper_wick > WICK_FRACTION_THRESHOLD)
                & (lower_wick > WICK_FRACTION_THRESHOLD)
            )
            / max(n, 1)
        ),
        # Volume / notional proxies (descriptive only).
        "volume_median": median_safe(v),
        "notional_proxy_median": median_safe(notional),
        "notional_proxy_p25": percentile_safe(notional, 25),
        "notional_proxy_p75": percentile_safe(notional, 75),
    }

    # Expansion-event frequencies.
    valid_range_med = np.isfinite(range_med)
    n_valid_range = int(np.sum(valid_range_med))
    for thresh in EXPANSION_RANGE_THRESHOLDS:
        if n_valid_range > 0:
            mask = valid_range_med & (range_bps > thresh * range_med)
            cnt = int(np.sum(mask))
            metrics[f"frac_bars_range_gt_{thresh:.1f}xmed"] = cnt / n_valid_range
            metrics[f"events_per_1000_bars_range_gt_{thresh:.1f}xmed"] = (
                cnt * 1000.0 / n_valid_range
            )
        else:
            metrics[f"frac_bars_range_gt_{thresh:.1f}xmed"] = float("nan")
            metrics[f"events_per_1000_bars_range_gt_{thresh:.1f}xmed"] = float("nan")

    valid_absret_med = np.isfinite(absret_med)
    n_valid_absret = int(np.sum(valid_absret_med))
    for thresh in EXPANSION_ABSRET_THRESHOLDS:
        if n_valid_absret > 0:
            mask = valid_absret_med & (abs_ret_bps > thresh * absret_med)
            cnt = int(np.sum(mask))
            metrics[f"frac_bars_absret_gt_{thresh:.1f}xmed"] = cnt / n_valid_absret
            metrics[f"events_per_1000_bars_absret_gt_{thresh:.1f}xmed"] = (
                cnt * 1000.0 / n_valid_absret
            )
        else:
            metrics[f"frac_bars_absret_gt_{thresh:.1f}xmed"] = float("nan")
            metrics[f"events_per_1000_bars_absret_gt_{thresh:.1f}xmed"] = float("nan")

    # Trend / regime descriptive frequencies.
    n_valid_ema50 = int(np.sum(valid_ema50))
    if n_valid_ema50 > 0:
        metrics["frac_bars_close_above_ema50"] = float(
            np.sum(valid_ema50 & (c > ema50)) / n_valid_ema50
        )
        metrics["frac_bars_ema50_pos_slope"] = float(
            np.sum(ema50_slope_pos) / n_valid_ema50
        )
    else:
        metrics["frac_bars_close_above_ema50"] = float("nan")
        metrics["frac_bars_ema50_pos_slope"] = float("nan")

    n_valid_both = int(np.sum(valid_both_emas))
    if n_valid_both > 0:
        metrics["frac_bars_ema50_above_ema200"] = float(
            np.sum(valid_both_emas & (ema50 > ema200)) / n_valid_both
        )
        # Trend-state transitions: simple two-state (ema50>ema200 vs not),
        # transitions among bars where both EMAs are valid.
        ema_state = (ema50 > ema200).astype(np.int8)
        valid_idx = np.where(valid_both_emas)[0]
        transitions = 0
        if len(valid_idx) > 1:
            prev_state = ema_state[valid_idx[0]]
            for i in valid_idx[1:]:
                if ema_state[i] != prev_state:
                    transitions += 1
                    prev_state = ema_state[i]
        metrics["ema50_above_ema200_transition_count"] = int(transitions)
    else:
        metrics["frac_bars_ema50_above_ema200"] = float("nan")
        metrics["ema50_above_ema200_transition_count"] = 0

    # Coverage / governance attributes.
    eligible, manifest_name = manifest_eligibility(symbol, interval)
    metrics["manifest_research_eligible"] = bool(eligible)
    metrics["manifest_name"] = manifest_name or ""
    metrics["governance_scope"] = (
        "PASS"
        if eligible
        else (
            "Phase4ad_RuleB1_common_post_gap"
            if symbol in ("SOLUSDT", "XRPUSDT")
            else "PASS_or_legacy"
        )
    )
    return metrics


def compute_funding_metrics(symbol: str, fund: dict) -> dict[str, Any]:
    rate = fund["rate"].astype(np.float64)
    n = len(rate)
    rate_bps = rate * 1e4
    out = {
        "symbol": symbol,
        "event_count": int(n),
        "first_event_ms": int(fund["ts_ms"][0]),
        "last_event_ms": int(fund["ts_ms"][-1]),
        "first_event_iso": ms_to_iso(int(fund["ts_ms"][0])),
        "last_event_iso": ms_to_iso(int(fund["ts_ms"][-1])),
        "rate_bps_median": median_safe(rate_bps),
        "rate_bps_p25": percentile_safe(rate_bps, 25),
        "rate_bps_p75": percentile_safe(rate_bps, 75),
        "rate_bps_p05": percentile_safe(rate_bps, 5),
        "rate_bps_p95": percentile_safe(rate_bps, 95),
        "frac_positive_funding": float(np.sum(rate > 0) / max(n, 1)),
        "frac_negative_funding": float(np.sum(rate < 0) / max(n, 1)),
        "abs_rate_bps_median": median_safe(np.abs(rate_bps)),
        "abs_rate_bps_p95": percentile_safe(np.abs(rate_bps), 95),
        "abs_rate_bps_p99": percentile_safe(np.abs(rate_bps), 99),
    }
    return out


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
    p = argparse.ArgumentParser(description="Phase 4ae substrate-feasibility")
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

    print("Phase 4ae substrate-feasibility analysis")
    print(f"  start    : {args.start} ({start_ms})")
    print(f"  end      : {args.end} ({end_ms}) inclusive")
    print(f"  symbols  : {args.symbols}")
    print(f"  intervals: {args.intervals}")
    print(f"  out_dir  : {out_dir}")
    print()

    kline_metrics: list[dict[str, Any]] = []
    coverage_rows: list[dict[str, Any]] = []
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
            n = len(df["open_time"])
            interval_ms = INTERVAL_MS[interval]
            expected = ((df["open_time"][-1] - df["open_time"][0]) // interval_ms) + 1
            missing_in_window = int(max(0, expected - n))
            cov_row = {
                "symbol": symbol,
                "interval": interval,
                "bar_count": int(n),
                "first_open_time_iso": ms_to_iso(int(df["open_time"][0])),
                "last_open_time_iso": ms_to_iso(int(df["open_time"][-1])),
                "expected_bars_in_observed_span": int(expected),
                "missing_bars_in_observed_span": missing_in_window,
            }
            eligible, manifest_name = manifest_eligibility(symbol, interval)
            cov_row["manifest_research_eligible"] = bool(eligible)
            cov_row["manifest_name"] = manifest_name or ""
            cov_row["governance_scope"] = (
                "PASS"
                if eligible
                else (
                    "Phase4ad_RuleB1_common_post_gap"
                    if symbol in ("SOLUSDT", "XRPUSDT")
                    else "PASS_or_legacy_phase2_eligible_via_v002"
                )
            )
            coverage_rows.append(cov_row)
            print(f"    bars={n} expected={expected} missing_in_span={missing_in_window}")
            metrics = compute_kline_metrics(symbol, interval, df)
            kline_metrics.append(metrics)

    funding_metrics: list[dict[str, Any]] = []
    for symbol in args.symbols:
        print(f"  loading funding {symbol} ...")
        fund = load_funding(symbol, start_ms, end_ms)
        if fund is None or len(fund["ts_ms"]) == 0:
            print(f"    NO FUNDING in window for {symbol}")
            continue
        funding_metrics.append(compute_funding_metrics(symbol, fund))

    # Write tables.
    write_csv(coverage_rows, tables_dir / "coverage.csv")
    write_csv(kline_metrics, tables_dir / "kline_metrics.csv")
    write_csv(funding_metrics, tables_dir / "funding_metrics.csv")
    write_csv(omitted, tables_dir / "omitted_datasets.csv")

    # Cross-symbol ranking tables (per interval).
    rank_metrics_keys = [
        "atr_bps_median",
        "range_bps_median",
        "cost_roundtrip_over_atr_median",
        "events_per_1000_bars_range_gt_1.5xmed",
        "frac_bars_upper_wick_gt_thresh",
        "frac_bars_lower_wick_gt_thresh",
        "notional_proxy_median",
    ]
    rank_rows: list[dict[str, Any]] = []
    for interval in args.intervals:
        rows_at_int = [m for m in kline_metrics if m["interval"] == interval]
        for metric_key in rank_metrics_keys:
            def _key(r: dict[str, Any], mk: str = metric_key) -> float:
                v = r.get(mk, float("nan"))
                return float("inf") if not np.isfinite(v) else float(v)
            sorted_rows = sorted(rows_at_int, key=_key)
            for rank, r in enumerate(sorted_rows, start=1):
                rank_rows.append(
                    {
                        "interval": interval,
                        "metric": metric_key,
                        "rank_low_to_high": rank,
                        "symbol": r["symbol"],
                        "value": r.get(metric_key, float("nan")),
                    }
                )
    write_csv(rank_rows, tables_dir / "cross_symbol_rankings.csv")

    # Funding ranking (one table; not per interval).
    funding_rank_rows: list[dict[str, Any]] = []
    for metric_key in [
        "abs_rate_bps_median",
        "abs_rate_bps_p95",
        "rate_bps_p95",
        "rate_bps_p05",
        "frac_positive_funding",
    ]:
        def _fkey(r: dict[str, Any], mk: str = metric_key) -> float:
            v = r.get(mk, float("nan"))
            return float("inf") if not np.isfinite(v) else float(v)
        sorted_f = sorted(funding_metrics, key=_fkey)
        for rank, r in enumerate(sorted_f, start=1):
            funding_rank_rows.append(
                {
                    "metric": metric_key,
                    "rank_low_to_high": rank,
                    "symbol": r["symbol"],
                    "value": r.get(metric_key, float("nan")),
                }
            )
    write_csv(funding_rank_rows, tables_dir / "funding_rankings.csv")

    # Run metadata.
    run_meta = {
        "phase": "Phase 4ae substrate-feasibility analysis",
        "start_utc": args.start,
        "end_utc_inclusive": args.end,
        "start_ms": start_ms,
        "end_ms_inclusive": end_ms,
        "symbols": list(args.symbols),
        "intervals": list(args.intervals),
        "rolling_window_bars": ROLLING_WINDOW_BARS,
        "atr_window": ATR_WINDOW,
        "ema_fast": EMA_FAST,
        "ema_slow": EMA_SLOW,
        "expansion_range_thresholds": list(EXPANSION_RANGE_THRESHOLDS),
        "expansion_absret_thresholds": list(EXPANSION_ABSRET_THRESHOLDS),
        "wick_fraction_threshold": WICK_FRACTION_THRESHOLD,
        "high_cost_bps_per_side": HIGH_COST_BPS_PER_SIDE,
        "round_trip_cost_bps": ROUND_TRIP_COST_BPS,
        "phase4ad_rule_b1_applied": True,
        "phase4ad_rule_a_applied": False,
        "mark_price_used": False,
        "metrics_or_oi_used": False,
        "aggtrades_used": False,
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
    print("Phase 4ae analysis complete.")
    print(f"  kline cells       : {len(kline_metrics)}")
    print(f"  funding cells     : {len(funding_metrics)}")
    print(f"  coverage rows     : {len(coverage_rows)}")
    print(f"  omitted datasets  : {len(omitted)}")
    print(f"  ranking rows      : {len(rank_rows)}")
    print(f"  funding rank rows : {len(funding_rank_rows)}")
    print(f"  outputs at        : {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
