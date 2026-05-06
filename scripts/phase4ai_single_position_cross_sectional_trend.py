"""Phase 4ai - Single-Position Cross-Sectional Trend Feasibility Analysis.

Authority: Phase 4ah (single-position cross-sectional trend / relative-
strength feasibility memo; merged 5384589). Phase 4ag (research-program
pivot and mechanism-source triage memo; merged fa72870). Phase 4af (alt-
symbol regime-continuity / directional-persistence analysis; merged
25959dd). Phase 4ae (alt-symbol substrate-feasibility analysis; merged
c57afa4). Phase 4ad (gap-governance / scope-revision; Rule B1 common
post-gap start at 2022-04-03 00:00 UTC; merged 10f122e). Phase 4ac (alt-
symbol public data acquisition; merged 3478d05). Phase 4ab / 4aa (alt-
symbol data-requirements / market-selection memos).

Brief: analysis-and-docs only. Reads existing local normalized Parquet
only. No network I/O. No Binance API. No `data.binance.vision`. No
authenticated REST. No private endpoints. No public-endpoint code calls.
No user stream / WebSocket / listenKey. No credentials. No `.env`. No
MCP / Graphify / `.mcp.json`. No data acquisition. No data modification.
No manifest creation or modification. No backtest. No diagnostic / Q1-Q7
rerun. No strategy candidate. No strategy PnL. No equity curve. No
hypothesis-spec / strategy-spec / backtest-plan. No `src/prometheus/`
modification. No test modification. No existing-script modification. No
retained verdict revised. No project lock changed.

Default scope (Phase 4ai brief):
    Symbols   : BTCUSDT  ETHUSDT  SOLUSDT  XRPUSDT  ADAUSDT
    Intervals : 15m  30m  1h  4h
    Start     : 2022-04-03 00:00 UTC  (Phase 4ad Rule B1 common post-gap)
    End       : 2026-04-30 23:59:59 UTC
    Cost lock : 8 bps HIGH per side; round-trip = 16 bps; §11.6 preserved
    Output    : data/research/phase4ai/  (gitignored; not committed)

Predeclared descriptive parameters (NOT optimized):
    RANK_LOOKBACK_HOURS                                = (4, 12, 24, 72, 168)
    VOL_ADJ_LOOKBACK_HOURS                             = (24, 72, 168)
    FORWARD_HORIZON_HOURS                              = (4, 12, 24, 72)
    ATR_WINDOW                                         = 20
    REALIZED_VOL_WINDOW_BARS                           = 96
    RANK_QUALITY_MIN_SCORE                             = 0.60
    RANK_QUALITY_MIN_TOP_MINUS_SECOND                  = 0.05
    RANK_QUALITY_REQUIRE_POSITIVE_24H_AND_72H          = True
    PRIMARY_COMPOSITE_WEIGHT_RELATIVE_RETURN           = 0.70
    PRIMARY_COMPOSITE_WEIGHT_VOL_ADJ                   = 0.30
    HIGH_COST_ONE_WAY_BPS                              = 8
    HIGH_COST_ROUND_TRIP_BPS                           = 16

All metrics in this script are descriptive cross-sectional feasibility
metrics ONLY. They are NOT strategy signals, NOT backtests, NOT entry/
exit rules, NOT regime filters, NOT threshold-optimization candidates,
NOT a strategy PnL, NOT an equity curve, and NOT a fresh-hypothesis spec.
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
DEFAULT_OUT = REPO_ROOT / "data" / "research" / "phase4ai"
MANIFESTS_ROOT = REPO_ROOT / "data" / "manifests"

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT")
DEFAULT_INTERVALS = ("15m", "30m", "1h", "4h")

INTERVAL_MS = {
    "15m": 15 * 60 * 1000,
    "30m": 30 * 60 * 1000,
    "1h": 60 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
}

# Cost lock from §11.6 (preserved verbatim by Phase 4ai).
HIGH_COST_BPS_PER_SIDE = 8.0
ROUND_TRIP_COST_BPS = 16.0

# Predeclared parameters (Phase 4ai brief). Fixed before analysis.
RANK_LOOKBACK_HOURS = (4, 12, 24, 72, 168)
VOL_ADJ_LOOKBACK_HOURS = (24, 72, 168)
FORWARD_HORIZON_HOURS = (4, 12, 24, 72)
REALIZED_VOL_WINDOW_BARS = 96
RANK_QUALITY_MIN_SCORE = 0.60
RANK_QUALITY_MIN_TOP_MINUS_SECOND = 0.05
PRIMARY_W_RR = 0.70
PRIMARY_W_VA = 0.30

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


def hours_to_bars(hours: int, interval: str) -> int:
    interval_hours = INTERVAL_MS[interval] / (60 * 60 * 1000)
    bars = int(round(hours / interval_hours))
    return max(1, bars)


def manifest_eligibility(symbol: str, interval: str) -> tuple[bool, str | None]:
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


def load_klines(
    symbol: str, interval: str, start_ms: int, end_ms: int
) -> dict | None:
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
        "close": combined.column("close").to_numpy()[final],
    }
    return out


# ---------------------------------------------------------------------------
# Cross-sectional alignment
# ---------------------------------------------------------------------------


def align_symbols(
    symbol_data: dict[str, dict], interval: str, start_ms: int, end_ms: int
) -> dict[str, Any]:
    """Build aligned matrix of close prices indexed by common open_time.

    Uses an exact equally-spaced grid from start_ms..end_ms for the interval.
    For each grid timestamp, gather close per symbol; if any symbol is
    missing at a grid point, that timestamp is dropped from the aligned
    dataset.
    """
    step = INTERVAL_MS[interval]
    # Build canonical grid aligned to 0 mod step starting at the first valid
    # bar across all symbols (>= start_ms).
    earliest = max(int(d["open_time"][0]) for d in symbol_data.values())
    latest = min(int(d["open_time"][-1]) for d in symbol_data.values())
    grid_start = max(start_ms, earliest)
    grid_end = min(end_ms, latest)
    # Snap grid_start to nearest step boundary
    grid_start = (grid_start // step) * step
    n_grid = (grid_end - grid_start) // step + 1
    if n_grid <= 0:
        return {
            "open_time": np.empty(0, dtype=np.int64),
            "close": np.empty((0, len(symbol_data)), dtype=np.float64),
            "symbols": list(symbol_data.keys()),
            "n_dropped_missing": 0,
        }
    grid = grid_start + np.arange(n_grid, dtype=np.int64) * step

    symbols = list(symbol_data.keys())
    closes = np.full((n_grid, len(symbols)), np.nan, dtype=np.float64)
    for j, s in enumerate(symbols):
        d = symbol_data[s]
        ot = d["open_time"].astype(np.int64)
        cl = d["close"].astype(np.float64)
        # Index map: position within grid
        pos = (ot - grid_start) // step
        valid = (pos >= 0) & (pos < n_grid)
        closes[pos[valid], j] = cl[valid]

    # Drop any timestamp where any symbol is missing.
    have_all = np.all(np.isfinite(closes), axis=1)
    n_dropped_missing = int((~have_all).sum())
    keep_idx = np.where(have_all)[0]
    return {
        "open_time": grid[keep_idx],
        "close": closes[keep_idx, :],
        "symbols": symbols,
        "n_dropped_missing": n_dropped_missing,
        "n_grid": int(n_grid),
        "grid_start_ms": int(grid_start),
        "grid_end_ms": int(grid_end),
    }


# ---------------------------------------------------------------------------
# Vectorized metric primitives
# ---------------------------------------------------------------------------


def log_returns(closes: np.ndarray, lookback_bars: int) -> np.ndarray:
    """Per-symbol cumulative log return over the prior `lookback_bars`.

    `closes` shape: (T, S). Returns shape (T, S) with NaN for warmup rows.
    """
    out = np.full_like(closes, np.nan)
    if lookback_bars >= closes.shape[0]:
        return out
    out[lookback_bars:, :] = np.log(closes[lookback_bars:, :] / closes[:-lookback_bars, :])
    return out


def realized_volatility(closes: np.ndarray, window_bars: int) -> np.ndarray:
    """Per-symbol realized volatility via rolling stdev of one-bar log returns.

    Window covers the prior `window_bars` one-bar log returns. Returns shape
    (T, S) with NaN for warmup rows.
    """
    T, S = closes.shape
    out = np.full((T, S), np.nan, dtype=np.float64)
    if window_bars + 2 > T:
        return out
    one_bar = np.full((T, S), np.nan, dtype=np.float64)
    one_bar[1:, :] = np.log(closes[1:, :] / closes[:-1, :])
    # Rolling stdev: use cumulative sums of x and x^2
    # Pad zero row at top for cumulative-sum convenience.
    x = np.where(np.isfinite(one_bar), one_bar, 0.0)
    valid = np.isfinite(one_bar).astype(np.float64)
    cs_x = np.zeros((T + 1, S), dtype=np.float64)
    cs_x2 = np.zeros((T + 1, S), dtype=np.float64)
    cs_n = np.zeros((T + 1, S), dtype=np.float64)
    cs_x[1:, :] = np.cumsum(x, axis=0)
    cs_x2[1:, :] = np.cumsum(x * x, axis=0)
    cs_n[1:, :] = np.cumsum(valid, axis=0)
    # Window covers indices [t-window_bars, t-1] (one-bar returns), i.e. for
    # bar t the rolling window ends at bar t-1's return. Equivalent to a
    # window of `window_bars` ending immediately before bar t.
    for t in range(window_bars + 1, T):
        n = cs_n[t, :] - cs_n[t - window_bars, :]
        sx = cs_x[t, :] - cs_x[t - window_bars, :]
        sx2 = cs_x2[t, :] - cs_x2[t - window_bars, :]
        # Sample variance with n-1 if n>=2, else NaN
        with np.errstate(divide="ignore", invalid="ignore"):
            mean = np.where(n > 0, sx / n, np.nan)
            var = np.where(
                n > 1, (sx2 - n * mean * mean) / np.maximum(n - 1.0, 1.0), np.nan
            )
            out[t, :] = np.sqrt(np.maximum(var, 0.0))
    return out


def percentile_rank_rows(values: np.ndarray) -> np.ndarray:
    """Cross-sectional percentile rank per row.

    `values` shape (T, S). For each row, rank symbols by value (higher value
    = higher rank), and return percentile rank in [0, 1] (0 for lowest, 1
    for highest). Rows with any NaN return all-NaN for that row.
    """
    T, S = values.shape
    out = np.full((T, S), np.nan, dtype=np.float64)
    valid_rows = np.all(np.isfinite(values), axis=1)
    if S < 2:
        return out
    # argsort along axis=1 (ascending), then convert to ranks 0..S-1
    rows = values[valid_rows]
    order = np.argsort(rows, axis=1, kind="stable")
    ranks = np.empty_like(order, dtype=np.float64)
    cols = np.broadcast_to(np.arange(S), order.shape)
    np.put_along_axis(ranks, order, cols.astype(np.float64), axis=1)
    pct = ranks / max(S - 1, 1)
    out[valid_rows] = pct
    return out


# ---------------------------------------------------------------------------
# Per-interval analysis
# ---------------------------------------------------------------------------


def analyze_interval(
    interval: str,
    symbol_data: dict[str, dict],
    start_ms: int,
    end_ms: int,
) -> dict[str, Any]:
    aligned = align_symbols(symbol_data, interval, start_ms, end_ms)
    closes = aligned["close"]
    symbols = aligned["symbols"]
    T, S = closes.shape

    if T == 0:
        return {
            "interval": interval,
            "symbols": symbols,
            "n_aligned": 0,
            "n_dropped_missing": aligned["n_dropped_missing"],
            "n_warmup_dropped": 0,
            "n_horizon_dropped": 0,
            "n_ranking_timestamps": 0,
            "tables": {},
        }

    # Translate hours to bars
    rr_lookbacks = {h: hours_to_bars(h, interval) for h in RANK_LOOKBACK_HOURS}
    va_lookbacks = {h: hours_to_bars(h, interval) for h in VOL_ADJ_LOOKBACK_HOURS}
    fwd_horizons = {h: hours_to_bars(h, interval) for h in FORWARD_HORIZON_HOURS}

    # ---------- Per-symbol log returns at all rr / va lookbacks ----------
    rr_returns = {h: log_returns(closes, b) for h, b in rr_lookbacks.items()}
    va_returns = {h: log_returns(closes, b) for h, b in va_lookbacks.items()}

    # ---------- Realized volatility ----------
    rvol = realized_volatility(closes, REALIZED_VOL_WINDOW_BARS)

    # ---------- Cross-sectional percentile ranks ----------
    rr_pct = {h: percentile_rank_rows(rr_returns[h]) for h in RANK_LOOKBACK_HOURS}
    va_score_inputs = {}
    for h in VOL_ADJ_LOOKBACK_HOURS:
        va = va_returns[h] / np.where(rvol > EPSILON, rvol, np.nan)
        va_score_inputs[h] = va
    va_pct = {h: percentile_rank_rows(va_score_inputs[h]) for h in VOL_ADJ_LOOKBACK_HOURS}

    # ---------- Composite scores ----------
    rr_arr = np.stack([rr_pct[h] for h in RANK_LOOKBACK_HOURS], axis=2)  # (T,S,5)
    va_arr = np.stack([va_pct[h] for h in VOL_ADJ_LOOKBACK_HOURS], axis=2)  # (T,S,3)
    relative_return_score = np.nanmean(rr_arr, axis=2)
    vol_adj_score = np.nanmean(va_arr, axis=2)
    primary = (
        PRIMARY_W_RR * relative_return_score + PRIMARY_W_VA * vol_adj_score
    )

    # ---------- Mask: drop rows where any score is non-finite ----------
    score_valid = np.all(np.isfinite(primary), axis=1)
    max_lookback_bars = max(
        max(rr_lookbacks.values()),
        max(va_lookbacks.values()) + REALIZED_VOL_WINDOW_BARS + 1,
    )
    warmup_mask = np.arange(T) < max_lookback_bars
    n_warmup_dropped = int(warmup_mask.sum() & (~score_valid).sum() != 0)  # noqa: E501
    # Actual count of rows dropped due to warmup is the count where both
    # warmup_mask is True and score_valid is False.
    n_warmup_dropped = int((warmup_mask & ~score_valid).sum())

    # ---------- Forward-return horizon mask ----------
    max_fwd = max(fwd_horizons.values())
    horizon_mask = np.arange(T) >= T - max_fwd
    n_horizon_dropped = int((~warmup_mask & horizon_mask).sum())

    rank_mask = score_valid & (~warmup_mask) & (~horizon_mask)
    rank_idx = np.where(rank_mask)[0]
    n_rank_ts = int(len(rank_idx))

    if n_rank_ts == 0:
        return {
            "interval": interval,
            "symbols": symbols,
            "n_aligned": int(T),
            "n_dropped_missing": aligned["n_dropped_missing"],
            "n_warmup_dropped": n_warmup_dropped,
            "n_horizon_dropped": n_horizon_dropped,
            "n_ranking_timestamps": 0,
            "tables": {},
        }

    # ---------- Top-ranked / selected / median / bottom per row ----------
    pri = primary[rank_idx, :]
    order = np.argsort(pri, axis=1, kind="stable")  # ascending
    bottom_idx = order[:, 0]
    median_idx = order[:, S // 2]  # for S=5 -> index 2 (middle)
    top_idx = order[:, -1]
    second_idx = order[:, -2]

    top_score = pri[np.arange(n_rank_ts), top_idx]
    second_score = pri[np.arange(n_rank_ts), second_idx]

    # Rank-quality filter
    raw_24 = rr_returns[24]
    raw_72 = rr_returns[72]
    sym_24 = raw_24[rank_idx, :][np.arange(n_rank_ts), top_idx]
    sym_72 = raw_72[rank_idx, :][np.arange(n_rank_ts), top_idx]
    quality_pass = (
        (top_score >= RANK_QUALITY_MIN_SCORE)
        & ((top_score - second_score) >= RANK_QUALITY_MIN_TOP_MINUS_SECOND)
        & (np.isfinite(sym_24) & (sym_24 > 0))
        & (np.isfinite(sym_72) & (sym_72 > 0))
    )
    selected_idx = np.where(quality_pass, top_idx, -1)  # -1 = no symbol

    # ---------- Forward returns at each horizon ----------
    fwd_returns = {}
    for h, b in fwd_horizons.items():
        fr = np.full((T, S), np.nan, dtype=np.float64)
        if b < T:
            fr[: T - b, :] = np.log(closes[b:, :] / closes[: T - b, :])
        fwd_returns[h] = fr

    # ---------- Tables ----------
    tables: dict[str, list[dict]] = {}

    # 1. Coverage / alignment summary (per-symbol)
    cov_rows = []
    for s in symbols:
        d = symbol_data[s]
        ot = d["open_time"]
        elig, manifest = manifest_eligibility(s, interval)
        cov_rows.append(
            {
                "symbol": s,
                "interval": interval,
                "manifest": manifest or "MISSING",
                "research_eligible": "true" if elig else "false_or_governed",
                "first_bar_iso": ms_to_iso(int(ot[0])) if len(ot) else "",
                "last_bar_iso": ms_to_iso(int(ot[-1])) if len(ot) else "",
                "bar_count": int(len(ot)),
                "phase4ad_rule_b1_governed": (
                    "true" if s in ("SOLUSDT", "XRPUSDT") else "false"
                ),
            }
        )
    tables["coverage.csv"] = cov_rows

    # 2. Alignment summary
    tables["alignment.csv"] = [
        {
            "interval": interval,
            "n_grid": int(aligned["n_grid"]),
            "n_dropped_missing": int(aligned["n_dropped_missing"]),
            "n_aligned": int(T),
            "n_warmup_dropped": int(n_warmup_dropped),
            "n_horizon_dropped": int(n_horizon_dropped),
            "n_ranking_timestamps": int(n_rank_ts),
            "max_lookback_bars": int(max_lookback_bars),
            "max_forward_bars": int(max_fwd),
        }
    ]

    # 3. Rank distribution
    top_counts = {s: int((top_idx == j).sum()) for j, s in enumerate(symbols)}
    selected_counts = {
        s: int((selected_idx == j).sum()) for j, s in enumerate(symbols)
    }
    no_symbol_count = int((selected_idx == -1).sum())
    rank_dist_rows = []
    for j, s in enumerate(symbols):
        rank_dist_rows.append(
            {
                "symbol": s,
                "interval": interval,
                "top_ranked_count": top_counts[s],
                "selected_count": selected_counts[s],
                "top_ranked_share": round(top_counts[s] / n_rank_ts, 6),
                "selected_share": round(selected_counts[s] / n_rank_ts, 6),
                "mean_primary_score": round(float(np.nanmean(pri[:, j])), 6),
                "median_primary_score": round(
                    float(np.nanmedian(pri[:, j])), 6
                ),
            }
        )
    rank_dist_rows.append(
        {
            "symbol": "NO_SYMBOL",
            "interval": interval,
            "top_ranked_count": 0,
            "selected_count": no_symbol_count,
            "top_ranked_share": 0.0,
            "selected_share": round(no_symbol_count / n_rank_ts, 6),
            "mean_primary_score": float("nan"),
            "median_primary_score": float("nan"),
        }
    )
    tables["rank_distribution.csv"] = rank_dist_rows

    # Concentration metrics
    top_share_max = max(top_counts.values()) / n_rank_ts
    selected_denom = max(n_rank_ts - no_symbol_count, 1)
    selected_share_max = (
        max(selected_counts.values()) / selected_denom if selected_denom > 0 else 0.0
    )
    hhi_top = sum((c / n_rank_ts) ** 2 for c in top_counts.values())
    hhi_selected = (
        sum((c / selected_denom) ** 2 for c in selected_counts.values())
        if selected_denom > 0
        else 0.0
    )
    tables["concentration.csv"] = [
        {
            "interval": interval,
            "n_rank_ts": n_rank_ts,
            "no_symbol_count": no_symbol_count,
            "no_symbol_fraction": round(no_symbol_count / n_rank_ts, 6),
            "top_share_max": round(float(top_share_max), 6),
            "selected_share_max": round(float(selected_share_max), 6),
            "hhi_top": round(float(hhi_top), 6),
            "hhi_selected": round(float(hhi_selected), 6),
        }
    ]

    # 4. Persistence / turnover
    top_persist = float(np.mean(top_idx[1:] == top_idx[:-1])) if n_rank_ts > 1 else float("nan")
    sel_mask = selected_idx >= 0
    if n_rank_ts > 1:
        consec_sel = sel_mask[1:] & sel_mask[:-1]
        if consec_sel.any():
            sel_persist = float(
                np.mean(selected_idx[1:][consec_sel] == selected_idx[:-1][consec_sel])
            )
        else:
            sel_persist = float("nan")
    else:
        sel_persist = float("nan")
    top_switches = int((top_idx[1:] != top_idx[:-1]).sum()) if n_rank_ts > 1 else 0
    sel_switches_total = int((selected_idx[1:] != selected_idx[:-1]).sum()) if n_rank_ts > 1 else 0
    # Switch into / out of NO_SYMBOL
    if n_rank_ts > 1:
        into_no = int(((selected_idx[1:] == -1) & (selected_idx[:-1] != -1)).sum())
        out_of_no = int(((selected_idx[1:] != -1) & (selected_idx[:-1] == -1)).sum())
    else:
        into_no = 0
        out_of_no = 0
    sel_to_sel_switch = sel_switches_total - into_no - out_of_no
    tables["persistence_turnover.csv"] = [
        {
            "interval": interval,
            "top_persistence": round(float(top_persist), 6),
            "selected_persistence_excl_no_symbol": round(float(sel_persist), 6),
            "top_switches_per_1000": (
                round(top_switches / max(n_rank_ts - 1, 1) * 1000.0, 3)
            ),
            "selected_switches_per_1000": (
                round(sel_switches_total / max(n_rank_ts - 1, 1) * 1000.0, 3)
            ),
            "into_no_symbol_count": into_no,
            "out_of_no_symbol_count": out_of_no,
            "selected_to_selected_switch_count": sel_to_sel_switch,
            "implied_round_trip_cost_pressure_bps_total": (
                round(sel_switches_total * ROUND_TRIP_COST_BPS, 3)
            ),
        }
    ]

    # 5. Forward behavior by horizon
    fwd_rows = []
    for h, b in fwd_horizons.items():
        fr = fwd_returns[h][rank_idx, :]
        # bps conversion: log_return * 1e4
        fr_bps = fr * 1e4
        if not np.any(np.isfinite(fr_bps)):
            continue
        top_fwd = fr_bps[np.arange(n_rank_ts), top_idx]
        bot_fwd = fr_bps[np.arange(n_rank_ts), bottom_idx]
        med_fwd = fr_bps[np.arange(n_rank_ts), median_idx]
        # Selected: only rows where quality_pass
        sel_rows = sel_mask
        if sel_rows.any():
            sel_fwd = fr_bps[sel_rows, :][np.arange(int(sel_rows.sum())), selected_idx[sel_rows]]
            med_fwd_at_sel = med_fwd[sel_rows]
        else:
            sel_fwd = np.array([], dtype=np.float64)
            med_fwd_at_sel = np.array([], dtype=np.float64)
        valid_top = np.isfinite(top_fwd) & np.isfinite(med_fwd) & np.isfinite(bot_fwd)
        valid_sel = (
            np.isfinite(sel_fwd) & np.isfinite(med_fwd_at_sel)
            if sel_fwd.size
            else np.array([], dtype=bool)
        )
        n_valid_top = int(valid_top.sum())
        n_valid_sel = int(valid_sel.sum())

        def stat(arr: np.ndarray, mask: np.ndarray | None = None) -> dict[str, float]:
            a = arr[mask] if mask is not None else arr
            a = a[np.isfinite(a)]
            if a.size == 0:
                return {"median": float("nan"), "p5": float("nan"), "p95": float("nan")}
            return {
                "median": float(np.median(a)),
                "p5": float(np.percentile(a, 5)),
                "p95": float(np.percentile(a, 95)),
            }

        top_stats = stat(top_fwd, valid_top)
        bot_stats = stat(bot_fwd, valid_top)
        med_stats = stat(med_fwd, valid_top)
        nan_stats = {
            "median": float("nan"),
            "p5": float("nan"),
            "p95": float("nan"),
        }
        sel_stats = stat(sel_fwd, valid_sel) if n_valid_sel > 0 else nan_stats

        spread_top_med_med = (
            float(np.median((top_fwd - med_fwd)[valid_top])) if n_valid_top > 0 else float("nan")
        )
        if n_valid_sel > 0:
            spread_sel_med_med = float(
                np.median((sel_fwd - med_fwd_at_sel)[valid_sel])
            )
        else:
            spread_sel_med_med = float("nan")

        frac_top_gt_med = (
            float(np.mean(top_fwd[valid_top] > med_fwd[valid_top]))
            if n_valid_top > 0
            else float("nan")
        )
        frac_sel_gt_med = (
            float(np.mean(sel_fwd[valid_sel] > med_fwd_at_sel[valid_sel]))
            if n_valid_sel > 0
            else float("nan")
        )
        frac_top_gt_bot = (
            float(np.mean(top_fwd[valid_top] > bot_fwd[valid_top]))
            if n_valid_top > 0
            else float("nan")
        )
        sel_gt_bot = float("nan")
        if n_valid_sel > 0:
            bot_at_sel = bot_fwd[sel_rows][valid_sel]
            sel_gt_bot = float(np.mean(sel_fwd[valid_sel] > bot_at_sel))

        frac_top_med_above_16 = (
            float(np.mean((top_fwd[valid_top] - med_fwd[valid_top]) > 16.0))
            if n_valid_top > 0
            else float("nan")
        )
        frac_sel_med_above_16 = (
            float(np.mean((sel_fwd[valid_sel] - med_fwd_at_sel[valid_sel]) > 16.0))
            if n_valid_sel > 0
            else float("nan")
        )
        frac_top_med_below_neg16 = (
            float(np.mean((top_fwd[valid_top] - med_fwd[valid_top]) < -16.0))
            if n_valid_top > 0
            else float("nan")
        )
        frac_sel_med_below_neg16 = (
            float(np.mean((sel_fwd[valid_sel] - med_fwd_at_sel[valid_sel]) < -16.0))
            if n_valid_sel > 0
            else float("nan")
        )

        fwd_rows.append(
            {
                "interval": interval,
                "forward_horizon_h": int(h),
                "forward_horizon_bars": int(b),
                "n_valid_top": n_valid_top,
                "n_valid_sel": n_valid_sel,
                "top_median_bps": round(top_stats["median"], 3),
                "selected_median_bps": round(sel_stats["median"], 3),
                "median_median_bps": round(med_stats["median"], 3),
                "bottom_median_bps": round(bot_stats["median"], 3),
                "top_p5_bps": round(top_stats["p5"], 3),
                "top_p95_bps": round(top_stats["p95"], 3),
                "selected_p5_bps": round(sel_stats["p5"], 3),
                "selected_p95_bps": round(sel_stats["p95"], 3),
                "spread_top_minus_median_median_bps": round(spread_top_med_med, 3),
                "spread_selected_minus_median_median_bps": round(
                    spread_sel_med_med, 3
                ),
                "frac_top_gt_median": round(frac_top_gt_med, 6),
                "frac_selected_gt_median": round(frac_sel_gt_med, 6),
                "frac_top_gt_bottom": round(frac_top_gt_bot, 6),
                "frac_selected_gt_bottom": round(sel_gt_bot, 6),
                "frac_top_med_spread_above_plus16bps": round(frac_top_med_above_16, 6),
                "frac_selected_med_spread_above_plus16bps": round(
                    frac_sel_med_above_16, 6
                ),
                "frac_top_med_spread_below_minus16bps": round(
                    frac_top_med_below_neg16, 6
                ),
                "frac_selected_med_spread_below_minus16bps": round(
                    frac_sel_med_below_neg16, 6
                ),
            }
        )
    tables["forward_behavior.csv"] = fwd_rows

    # 6. Spearman IC by interval / horizon
    ic_rows = []
    for h, _b in fwd_horizons.items():
        fr = fwd_returns[h][rank_idx, :]
        # Per-row Spearman: rank scores cross-sectionally and rank forwards
        score_rows = pri  # already finite by score_valid mask
        valid_rows = np.all(np.isfinite(fr), axis=1)
        if not valid_rows.any():
            ic_rows.append(
                {
                    "interval": interval,
                    "forward_horizon_h": int(h),
                    "n_valid_rows": 0,
                    "spearman_ic_median": float("nan"),
                    "spearman_ic_mean": float("nan"),
                    "frac_directional_alignment": float("nan"),
                }
            )
            continue
        sr = score_rows[valid_rows]
        fwd_v = fr[valid_rows]
        # Cross-sectional ranks
        score_ranks = np.argsort(
            np.argsort(sr, axis=1, kind="stable"), axis=1, kind="stable"
        ).astype(float)
        fwd_ranks = np.argsort(
            np.argsort(fwd_v, axis=1, kind="stable"), axis=1, kind="stable"
        ).astype(float)
        # Pearson on ranks = Spearman
        sr_c = score_ranks - score_ranks.mean(axis=1, keepdims=True)
        fr_c = fwd_ranks - fwd_ranks.mean(axis=1, keepdims=True)
        num = np.sum(sr_c * fr_c, axis=1)
        denom = np.sqrt(np.sum(sr_c * sr_c, axis=1) * np.sum(fr_c * fr_c, axis=1))
        ic = np.where(denom > EPSILON, num / denom, np.nan)
        ic_clean = ic[np.isfinite(ic)]
        # Directional alignment: top-ranked symbol is also top forward symbol
        score_top = np.argmax(sr, axis=1)
        fwd_top = np.argmax(fwd_v, axis=1)
        align = float(np.mean(score_top == fwd_top)) if score_top.size else float("nan")
        ic_med = (
            round(float(np.median(ic_clean)), 6) if ic_clean.size else float("nan")
        )
        ic_mn = (
            round(float(np.mean(ic_clean)), 6) if ic_clean.size else float("nan")
        )
        ic_rows.append(
            {
                "interval": interval,
                "forward_horizon_h": int(h),
                "n_valid_rows": int(ic_clean.size),
                "spearman_ic_median": ic_med,
                "spearman_ic_mean": ic_mn,
                "frac_directional_alignment": round(align, 6),
            }
        )
    tables["rank_ic.csv"] = ic_rows

    # 7. Cost-adjusted forward absolute movement
    cost_rows = []
    thresholds_bps = (16.0, 24.0, 32.0)
    for h in FORWARD_HORIZON_HOURS:
        fr = fwd_returns[h][rank_idx, :]
        fr_bps = fr * 1e4
        for thr in thresholds_bps:
            top_fr = fr_bps[np.arange(n_rank_ts), top_idx]
            med_fr = fr_bps[np.arange(n_rank_ts), median_idx]
            bot_fr = fr_bps[np.arange(n_rank_ts), bottom_idx]
            sel_rows = sel_mask
            sel_fr = (
                fr_bps[sel_rows, :][np.arange(int(sel_rows.sum())), selected_idx[sel_rows]]
                if sel_rows.any()
                else np.array([], dtype=np.float64)
            )
            def fr_above_abs(arr: np.ndarray, thr: float) -> float:
                a = arr[np.isfinite(arr)]
                if a.size == 0:
                    return float("nan")
                return float(np.mean(np.abs(a) > thr))

            cost_rows.append(
                {
                    "interval": interval,
                    "forward_horizon_h": int(h),
                    "threshold_bps": int(thr),
                    "frac_top_abs_above_thr": round(fr_above_abs(top_fr, thr), 6),
                    "frac_selected_abs_above_thr": round(
                        fr_above_abs(sel_fr, thr), 6
                    ),
                    "frac_median_abs_above_thr": round(fr_above_abs(med_fr, thr), 6),
                    "frac_bottom_abs_above_thr": round(fr_above_abs(bot_fr, thr), 6),
                }
            )
    tables["cost_adjusted_movement.csv"] = cost_rows

    # 8. Crash / adverse-tail exposure
    crash_rows = []
    for h in FORWARD_HORIZON_HOURS:
        fr = fwd_returns[h][rank_idx, :]
        fr_bps = fr * 1e4
        top_fr = fr_bps[np.arange(n_rank_ts), top_idx]
        sel_rows = sel_mask
        sel_fr = (
            fr_bps[sel_rows, :][np.arange(int(sel_rows.sum())), selected_idx[sel_rows]]
            if sel_rows.any()
            else np.array([], dtype=np.float64)
        )
        def tail(arr: np.ndarray, q: float) -> float:
            a = arr[np.isfinite(arr)]
            if a.size == 0:
                return float("nan")
            return float(np.percentile(a, q))

        def frac_below(arr: np.ndarray, thr: float) -> float:
            a = arr[np.isfinite(arr)]
            if a.size == 0:
                return float("nan")
            return float(np.mean(a < thr))

        crash_rows.append(
            {
                "interval": interval,
                "forward_horizon_h": int(h),
                "top_p1_bps": round(tail(top_fr, 1.0), 3),
                "top_p5_bps": round(tail(top_fr, 5.0), 3),
                "top_p25_bps": round(tail(top_fr, 25.0), 3),
                "top_median_bps": round(tail(top_fr, 50.0), 3),
                "top_p75_bps": round(tail(top_fr, 75.0), 3),
                "top_p95_bps": round(tail(top_fr, 95.0), 3),
                "selected_p1_bps": (
                    round(tail(sel_fr, 1.0), 3) if sel_fr.size else float("nan")
                ),
                "selected_p5_bps": (
                    round(tail(sel_fr, 5.0), 3) if sel_fr.size else float("nan")
                ),
                "selected_median_bps": (
                    round(tail(sel_fr, 50.0), 3) if sel_fr.size else float("nan")
                ),
                "selected_p95_bps": (
                    round(tail(sel_fr, 95.0), 3) if sel_fr.size else float("nan")
                ),
                "frac_top_below_minus16bps": round(frac_below(top_fr, -16.0), 6),
                "frac_top_below_minus32bps": round(frac_below(top_fr, -32.0), 6),
                "frac_top_below_minus64bps": round(frac_below(top_fr, -64.0), 6),
                "frac_selected_below_minus16bps": (
                    round(frac_below(sel_fr, -16.0), 6) if sel_fr.size else float("nan")
                ),
                "frac_selected_below_minus32bps": (
                    round(frac_below(sel_fr, -32.0), 6) if sel_fr.size else float("nan")
                ),
                "frac_selected_below_minus64bps": (
                    round(frac_below(sel_fr, -64.0), 6) if sel_fr.size else float("nan")
                ),
            }
        )
    tables["crash_exposure.csv"] = crash_rows

    return {
        "interval": interval,
        "symbols": symbols,
        "n_aligned": int(T),
        "n_dropped_missing": aligned["n_dropped_missing"],
        "n_warmup_dropped": int(n_warmup_dropped),
        "n_horizon_dropped": int(n_horizon_dropped),
        "n_ranking_timestamps": n_rank_ts,
        "no_symbol_fraction": round(no_symbol_count / n_rank_ts, 6),
        "tables": tables,
    }


# ---------------------------------------------------------------------------
# Falsification verdict
# ---------------------------------------------------------------------------


def derive_verdict(per_interval: dict[str, dict]) -> dict[str, Any]:
    """Apply Phase 4ai §9 falsification criteria across primary cells.

    Primary cells: (interval, forward_horizon_h) in {1h, 4h} × {24h, 72h}.
    """
    primary_intervals = ("1h", "4h")
    primary_horizons = (24, 72)

    cell_summaries: list[dict[str, Any]] = []
    for itv in primary_intervals:
        if itv not in per_interval:
            continue
        fwd_rows = per_interval[itv]["tables"].get("forward_behavior.csv", [])
        ic_rows = per_interval[itv]["tables"].get("rank_ic.csv", [])
        for h in primary_horizons:
            fwd = next(
                (r for r in fwd_rows if r["forward_horizon_h"] == h), None
            )
            ic = next(
                (r for r in ic_rows if r["forward_horizon_h"] == h), None
            )
            if fwd is None or ic is None:
                continue
            cell_summaries.append(
                {
                    "interval": itv,
                    "horizon_h": h,
                    "frac_selected_gt_median": fwd.get("frac_selected_gt_median"),
                    "spread_selected_minus_median_median_bps": fwd.get(
                        "spread_selected_minus_median_median_bps"
                    ),
                    "spearman_ic_median": ic.get("spearman_ic_median"),
                    "n_valid_sel": fwd.get("n_valid_sel", 0),
                }
            )

    def fnum(v: Any) -> float:
        try:
            x = float(v)
            return x if np.isfinite(x) else float("nan")
        except Exception:  # noqa: BLE001
            return float("nan")

    if not cell_summaries:
        verdict = "NOT_SUPPORTED"
        notes = ["no primary cells could be computed"]
        return {
            "verdict": verdict,
            "notes": notes,
            "cell_summaries": cell_summaries,
        }

    # Falsification criteria 1, 2, 3:
    fail_1 = all(
        fnum(c["frac_selected_gt_median"]) <= 0.52
        or not np.isfinite(fnum(c["frac_selected_gt_median"]))
        for c in cell_summaries
    )
    fail_2 = all(
        fnum(c["spread_selected_minus_median_median_bps"]) <= 0.0
        or not np.isfinite(fnum(c["spread_selected_minus_median_median_bps"]))
        for c in cell_summaries
    )
    fail_3 = all(
        fnum(c["spearman_ic_median"]) <= 0.0
        or not np.isfinite(fnum(c["spearman_ic_median"]))
        for c in cell_summaries
    )

    # Conditional-supported criteria (relaxed from full falsification):
    cond_outperf = sum(
        1 for c in cell_summaries if fnum(c["frac_selected_gt_median"]) > 0.55
    )
    cond_spread = sum(
        1
        for c in cell_summaries
        if fnum(c["spread_selected_minus_median_median_bps"]) > 16.0
    )
    cond_ic = sum(
        1 for c in cell_summaries if fnum(c["spearman_ic_median"]) > 0.0
    )

    notes = []
    notes.append(f"primary_cells_evaluated={len(cell_summaries)}")
    notes.append(f"fail_criterion_1_outperf_le_52pct_in_all_cells={fail_1}")
    notes.append(f"fail_criterion_2_spread_le_0_in_all_cells={fail_2}")
    notes.append(f"fail_criterion_3_ic_le_0_in_all_cells={fail_3}")
    notes.append(f"cond_cells_outperf_gt_55pct={cond_outperf}")
    notes.append(f"cond_cells_spread_gt_plus16bps={cond_spread}")
    notes.append(f"cond_cells_ic_gt_0={cond_ic}")

    if fail_1 and fail_2 and fail_3:
        verdict = "NOT_SUPPORTED"
    elif cond_outperf >= 2 and cond_spread >= 2 and cond_ic >= 2:
        verdict = "SUPPORTED_FOR_FUTURE_DISCUSSION"
    else:
        verdict = "CONDITIONAL_MIXED"

    return {
        "verdict": verdict,
        "notes": notes,
        "cell_summaries": cell_summaries,
    }


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(
        description="Phase 4ai single-position cross-sectional trend feasibility analysis."
    )
    p.add_argument(
        "--symbols",
        nargs="+",
        default=list(DEFAULT_SYMBOLS),
        help="Core symbols (default: BTCUSDT ETHUSDT SOLUSDT XRPUSDT ADAUSDT).",
    )
    p.add_argument(
        "--intervals",
        nargs="+",
        default=list(DEFAULT_INTERVALS),
        help="Intervals (default: 15m 30m 1h 4h).",
    )
    p.add_argument(
        "--start", default="2022-04-03", help="Start date (YYYY-MM-DD UTC)."
    )
    p.add_argument(
        "--end", default="2026-04-30", help="End date (YYYY-MM-DD UTC)."
    )
    p.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT),
        help="Output directory (default: data/research/phase4ai).",
    )
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tables_dir = out_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    start_ms = parse_ymd_to_ms_utc(args.start, end_of_day=False)
    end_ms = parse_ymd_to_ms_utc(args.end, end_of_day=True)

    print(
        f"Phase 4ai analysis "
        f"start={args.start}T00:00:00Z "
        f"end={args.end}T23:59:59Z "
        f"symbols={','.join(args.symbols)} "
        f"intervals={','.join(args.intervals)}"
    )

    # Load all symbol data per interval.
    per_interval_results: dict[str, dict] = {}
    omitted_datasets: list[dict[str, str]] = []
    for itv in args.intervals:
        symbol_data: dict[str, dict] = {}
        for sym in args.symbols:
            d = load_klines(sym, itv, start_ms, end_ms)
            if d is None:
                omitted_datasets.append(
                    {
                        "symbol": sym,
                        "interval": itv,
                        "reason": "missing_or_no_data_in_window",
                    }
                )
                continue
            symbol_data[sym] = d
        if len(symbol_data) < 2:
            print(
                f"  interval={itv} insufficient symbols loaded; skipping",
                file=sys.stderr,
            )
            continue
        if len(symbol_data) < len(args.symbols):
            missing = [s for s in args.symbols if s not in symbol_data]
            print(
                f"  WARNING interval={itv} missing symbols={missing}",
                file=sys.stderr,
            )
        result = analyze_interval(itv, symbol_data, start_ms, end_ms)
        per_interval_results[itv] = result

    if not per_interval_results:
        print("No interval analysis succeeded; STOP.", file=sys.stderr)
        return 1

    # Write per-interval tables.
    for itv, result in per_interval_results.items():
        for fname, rows in result.get("tables", {}).items():
            target = tables_dir / f"{itv}__{fname}"
            write_csv(target, rows)

    # Write omitted-datasets table.
    write_csv(tables_dir / "omitted_datasets.csv", omitted_datasets)

    # Write run metadata.
    run_meta = {
        "phase": "4ai",
        "title": "single-position cross-sectional trend feasibility analysis",
        "analysis_window_start_utc": ms_to_iso(start_ms),
        "analysis_window_end_utc": ms_to_iso(end_ms),
        "phase4ad_rule_b1": True,
        "phase4ad_rule_b1_common_post_gap_start_utc": "2022-04-03T00:00:00+00:00",
        "symbols": args.symbols,
        "intervals": args.intervals,
        "uses_mark_price": False,
        "uses_funding": False,
        "uses_metrics_or_oi": False,
        "uses_aggtrades_or_orderbook": False,
        "uses_only_local_normalized_data": True,
        "manifest_modifications": 0,
        "data_acquisitions": 0,
        "network_io_calls": 0,
        "rank_lookback_hours": list(RANK_LOOKBACK_HOURS),
        "vol_adj_lookback_hours": list(VOL_ADJ_LOOKBACK_HOURS),
        "forward_horizon_hours": list(FORWARD_HORIZON_HOURS),
        "realized_vol_window_bars": REALIZED_VOL_WINDOW_BARS,
        "rank_quality_min_score": RANK_QUALITY_MIN_SCORE,
        "rank_quality_min_top_minus_second": RANK_QUALITY_MIN_TOP_MINUS_SECOND,
        "primary_w_relative_return": PRIMARY_W_RR,
        "primary_w_vol_adjusted": PRIMARY_W_VA,
        "high_cost_one_way_bps": HIGH_COST_BPS_PER_SIDE,
        "high_cost_round_trip_bps": ROUND_TRIP_COST_BPS,
        "per_interval_summary": {
            itv: {
                "n_aligned": r["n_aligned"],
                "n_dropped_missing": r["n_dropped_missing"],
                "n_warmup_dropped": r["n_warmup_dropped"],
                "n_horizon_dropped": r["n_horizon_dropped"],
                "n_ranking_timestamps": r["n_ranking_timestamps"],
                "no_symbol_fraction": r.get("no_symbol_fraction", float("nan")),
            }
            for itv, r in per_interval_results.items()
        },
        "omitted_datasets_count": len(omitted_datasets),
    }
    (out_dir / "run_metadata.json").write_text(
        json.dumps(run_meta, indent=2, sort_keys=True), encoding="utf-8"
    )

    # Falsification verdict.
    verdict = derive_verdict(per_interval_results)
    write_csv(
        tables_dir / "verdict_summary.csv",
        [
            {
                "interval": c["interval"],
                "horizon_h": c["horizon_h"],
                "frac_selected_gt_median": c["frac_selected_gt_median"],
                "spread_selected_minus_median_median_bps": (
                    c["spread_selected_minus_median_median_bps"]
                ),
                "spearman_ic_median": c["spearman_ic_median"],
                "n_valid_sel": c["n_valid_sel"],
            }
            for c in verdict["cell_summaries"]
        ],
    )
    (out_dir / "verdict.json").write_text(
        json.dumps(verdict, indent=2, sort_keys=True), encoding="utf-8"
    )

    print(f"Phase 4ai verdict: {verdict['verdict']}")
    for n in verdict["notes"]:
        print(f"  {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
