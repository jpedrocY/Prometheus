"""Phase 3s — 5m Diagnostics Execution.

Runs the predeclared Phase 3o / Phase 3p Q1-Q7 diagnostic question set
on the v002-locked retained-evidence trade populations, using the
Phase 3q v001-of-5m supplemental datasets and applying the Phase 3r
§8 Q6 invalid-window exclusion rule.

Strict scope:
- Reads only existing trade_log.parquet artefacts and Phase 3q 5m
  parquet partitions. Does NOT regenerate any v002 trade population.
  Does NOT modify any v002 dataset or manifest. Does NOT modify any
  Phase 3q manifest. Does NOT run any backtest. Does NOT acquire,
  download, or patch data. Does NOT use forward-fill / interpolation
  / imputation / replacement / synthetic data.
- Q6 obeys Phase 3r §8 in full.
- All outputs are diagnostic only. No verdict revision, parameter
  change, threshold revision, strategy rescue, or live-readiness
  implication is produced or implied.

Outputs JSON tables under docs/00-meta/implementation-reports/phase-3s/.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

REPO = Path(r"C:\Prometheus")
BACKTESTS = REPO / "data" / "derived" / "backtests"
NORM_KLINES = REPO / "data" / "normalized" / "klines"
NORM_MARKPRICE = REPO / "data" / "normalized" / "mark_price_klines"
MANIFESTS = REPO / "data" / "manifests"
OUT = REPO / "docs" / "00-meta" / "implementation-reports" / "phase-3s"

INTERVAL_5M_MS = 5 * 60 * 1000
INTERVAL_15M_MS = 15 * 60 * 1000

# ---------------------------------------------------------------------------
# Canonical retained-evidence populations (R-window, MEDIUM slip; v002-locked)
# ---------------------------------------------------------------------------

# All entries are (candidate_label, run_dir_relative_to_BACKTESTS, run_id_subdir)
POPULATIONS: list[tuple[str, str, str]] = [
    ("R3", "phase-2l-r3-r", "2026-04-29T03-11-42Z"),
    ("R2", "phase-2w-r2-r2_r3-r", "2026-04-27T11-25-07Z"),
    ("F1", "phase-3d-f1-window=r-slip=medium", "2026-04-29T03-12-14Z"),
    ("D1A", "phase-3j-d1a-window=r-slip=medium", "2026-04-29T03-22-26Z"),
]

SYMBOLS = ("BTCUSDT", "ETHUSDT")


# ---------------------------------------------------------------------------
# 5m dataset loader (in-memory cache; one symbol/family at a time)
# ---------------------------------------------------------------------------

_kline_cache: dict[tuple[str, str], dict[int, dict[str, float]]] = {}


def load_5m_klines(symbol: str, family: str) -> dict[int, dict[str, float]]:
    """Load and index a (symbol, family) 5m dataset by `open_time` -> row dict.

    family ∈ {"trade", "mark"}.

    Returns dict[open_time_ms] -> {"open": ..., "high": ..., "low": ..., "close": ...,
        "volume": ..., "quote_asset_volume": ...} (volume fields only for trade).
    """
    key = (symbol, family)
    if key in _kline_cache:
        return _kline_cache[key]
    root = NORM_KLINES if family == "trade" else NORM_MARKPRICE
    base = root / f"symbol={symbol}" / "interval=5m"
    paths = sorted(base.glob("year=*/month=*/part-0000.parquet"))
    if not paths:
        raise FileNotFoundError(f"no 5m {family} parquet under {base}")
    tables = [pq.ParquetFile(str(p)).read() for p in paths]
    combined = pa.concat_tables(tables)
    open_time = combined.column("open_time").to_pylist()
    o = combined.column("open").to_pylist()
    h = combined.column("high").to_pylist()
    lo = combined.column("low").to_pylist()
    c = combined.column("close").to_pylist()
    if family == "trade":
        v = combined.column("volume").to_pylist()
        qv = combined.column("quote_asset_volume").to_pylist()
    else:
        v = qv = [None] * len(open_time)
    idx: dict[int, dict[str, float]] = {}
    for i in range(len(open_time)):
        idx[int(open_time[i])] = {
            "open": float(o[i]),
            "high": float(h[i]),
            "low": float(lo[i]),
            "close": float(c[i]),
            "volume": v[i] if family == "trade" else None,
            "quote_asset_volume": qv[i] if family == "trade" else None,
        }
    _kline_cache[key] = idx
    return idx


# ---------------------------------------------------------------------------
# 5m mark-price invalid windows (from Phase 3q manifests)
# ---------------------------------------------------------------------------

def load_invalid_windows(symbol: str) -> list[tuple[int, int]]:
    """Return list of (start_open_time_ms, end_open_time_ms) inclusive ranges
    of mark-price gap windows for `symbol`. Both endpoints are bar `open_time`
    values that are MISSING from the dataset."""
    p = MANIFESTS / f"binance_usdm_{symbol.lower()}_markprice_5m__v001.manifest.json"
    m = json.loads(p.read_text())
    out = []
    for w in m.get("invalid_windows", []):
        out.append((int(w["start_open_time_ms"]), int(w["end_open_time_ms"])))
    return out


def intersects_invalid(window_start_ms: int, window_end_ms: int,
                       invalid_windows: list[tuple[int, int]]) -> str | None:
    """Return the invalid-window key (formatted) if [window_start_ms, window_end_ms]
    intersects any invalid window, else None."""
    for s, e in invalid_windows:
        if not (window_end_ms < s or window_start_ms > e):
            return f"{s}-{e}"
    return None


# ---------------------------------------------------------------------------
# Bar lookup helpers
# ---------------------------------------------------------------------------

def bar_open_time_for(ts_ms: int) -> int:
    """Return the 5m `open_time` of the bar that contains `ts_ms`."""
    return (ts_ms // INTERVAL_5M_MS) * INTERVAL_5M_MS


def iter_5m_bars(klines: dict[int, dict], start_ot: int, end_ot: int):
    """Yield (open_time, bar) pairs for bars in [start_ot, end_ot] inclusive
    (in 5m steps). Skip missing bars silently."""
    t = start_ot
    while t <= end_ot:
        b = klines.get(t)
        if b is not None:
            yield t, b
        t += INTERVAL_5M_MS


# ---------------------------------------------------------------------------
# Q1 — IAE / IFE in first 1, 2, 3 5m bars after entry
# ---------------------------------------------------------------------------

def q1_per_trade(trade: dict, klines: dict[int, dict]) -> dict[str, Any]:
    direction = trade["direction"]
    entry_price = trade["entry_fill_price"]
    R = trade["stop_distance"]
    entry_ot = bar_open_time_for(trade["entry_fill_time_ms"])

    out: dict[str, Any] = {}
    cur_low = float("inf")
    cur_high = float("-inf")
    for n in (1, 2, 3):
        t = entry_ot + (n - 1) * INTERVAL_5M_MS
        b = klines.get(t)
        if b is None:
            out[f"iae_{n}"] = None
            out[f"ife_{n}"] = None
            continue
        cur_low = min(cur_low, b["low"])
        cur_high = max(cur_high, b["high"])
        if direction == "LONG":
            iae = (entry_price - cur_low) / R
            ife = (cur_high - entry_price) / R
        else:
            iae = (cur_high - entry_price) / R
            ife = (entry_price - cur_low) / R
        out[f"iae_{n}"] = iae
        out[f"ife_{n}"] = ife
    return out


# ---------------------------------------------------------------------------
# Q2 — wick-stop vs sustained-stop classification (STOP-exited only)
# ---------------------------------------------------------------------------

def q2_per_trade(trade: dict, klines: dict[int, dict]) -> str | None:
    if trade["exit_reason"] != "STOP":
        return None
    direction = trade["direction"]
    stop_level = trade["initial_stop"]
    exit_ot = bar_open_time_for(trade["exit_fill_time_ms"])
    bar = klines.get(exit_ot)
    if bar is None:
        return None
    if direction == "LONG":
        # stop violated by wick-low; close back above stop?
        wick_violation = bar["low"] <= stop_level
        close_back = bar["close"] > stop_level
    else:
        wick_violation = bar["high"] >= stop_level
        close_back = bar["close"] < stop_level
    if not wick_violation:
        return None  # not a wick event at this bar — defensive
    if close_back:
        return "wick_stop"
    # check sustained: this bar AND next 2 bars all close on adverse side
    sustained = True
    for n in range(3):
        b = klines.get(exit_ot + n * INTERVAL_5M_MS)
        if b is None:
            sustained = False
            break
        if direction == "LONG":
            if b["close"] > stop_level:
                sustained = False
                break
        else:
            if b["close"] < stop_level:
                sustained = False
                break
    return "sustained_stop" if sustained else "indeterminate"


# ---------------------------------------------------------------------------
# Q3 — intrabar +1R / +2R target touches before adverse exit
# ---------------------------------------------------------------------------

def q3_per_trade(trade: dict, klines: dict[int, dict]) -> dict[str, Any]:
    direction = trade["direction"]
    entry_price = trade["entry_fill_price"]
    R = trade["stop_distance"]
    entry_ot = bar_open_time_for(trade["entry_fill_time_ms"])
    exit_ot = bar_open_time_for(trade["exit_fill_time_ms"])

    if direction == "LONG":
        t1 = entry_price + 1.0 * R
        t2 = entry_price + 2.0 * R
    else:
        t1 = entry_price - 1.0 * R
        t2 = entry_price - 2.0 * R

    intrabar_1 = False
    intrabar_2 = False
    confirmed_1 = False
    confirmed_2 = False
    for _ot, b in iter_5m_bars(klines, entry_ot, exit_ot):
        if direction == "LONG":
            if b["high"] >= t1:
                intrabar_1 = True
            if b["high"] >= t2:
                intrabar_2 = True
            if b["close"] >= t1:
                confirmed_1 = True
            if b["close"] >= t2:
                confirmed_2 = True
        else:
            if b["low"] <= t1:
                intrabar_1 = True
            if b["low"] <= t2:
                intrabar_2 = True
            if b["close"] <= t1:
                confirmed_1 = True
            if b["close"] <= t2:
                confirmed_2 = True
    return {
        "intrabar_target_1r": intrabar_1,
        "intrabar_target_2r": intrabar_2,
        "confirmed_target_1r": confirmed_1,
        "confirmed_target_2r": confirmed_2,
        # Adverse-exit context: trade was STOP / TIME_STOP, not TARGET
        "adverse_exit": trade["exit_reason"] != "TARGET",
    }


# ---------------------------------------------------------------------------
# Q4 — D1-A funding-extreme decay over 5/10/15/30/60 minutes
# ---------------------------------------------------------------------------

def q4_per_trade(trade: dict, klines: dict[int, dict]) -> dict[str, float | None]:
    """For a D1-A trade, sample cumulative price displacement at +5/+10/+15/+30/+60 min
    from entry, signed in the trade's direction (positive = favorable contrarian
    realization). Each value in R-units."""
    direction = trade["direction"]
    entry_price = trade["entry_fill_price"]
    R = trade["stop_distance"]
    entry_ot = bar_open_time_for(trade["entry_fill_time_ms"])
    out: dict[str, float | None] = {}
    for minutes in (5, 10, 15, 30, 60):
        t = entry_ot + minutes * 60 * 1000
        # Snap to nearest 5m boundary
        t_ot = (t // INTERVAL_5M_MS) * INTERVAL_5M_MS
        b = klines.get(t_ot)
        if b is None:
            out[f"decay_{minutes}m_R"] = None
            continue
        if direction == "LONG":
            disp = (b["close"] - entry_price) / R
        else:
            disp = (entry_price - b["close"]) / R
        out[f"decay_{minutes}m_R"] = disp
    return out


# ---------------------------------------------------------------------------
# Q5 — fill-assumption realism (15m next-open vs first 5m sub-bar mid)
# ---------------------------------------------------------------------------

def q5_per_trade(trade: dict, klines: dict[int, dict]) -> dict[str, float | None]:
    """Compare 15m next-open fill (= entry_fill_price) to a probability-weighted
    5m fill simulation across the first 5m sub-bar of the 15m signal-confirmation
    bar's next bar.

    Predeclared probability weight: simple mid-price = (high + low) / 2 of the
    first 5m sub-bar containing entry.

    Reported in trade-direction-signed basis points (positive = 15m fill better
    than 5m mid, i.e. the 15m assumption is favorable; negative = 15m fill worse,
    i.e. the 15m assumption is unfavorable)."""
    direction = trade["direction"]
    entry_price = trade["entry_fill_price"]
    entry_ot = bar_open_time_for(trade["entry_fill_time_ms"])
    b = klines.get(entry_ot)
    if b is None:
        return {"fill_realism_signed_bps": None, "fill_realism_unsigned_bps": None}
    mid_5m = (b["high"] + b["low"]) / 2
    diff = entry_price - mid_5m
    # Sign by direction: for LONG, lower fill is better → 15m fill is "better"
    # if entry_price < mid_5m → diff < 0 → favorable for LONG.
    # We want: positive = 15m assumption is favorable to the trade.
    if direction == "LONG":
        signed_bps = -diff / entry_price * 1e4
    else:
        signed_bps = diff / entry_price * 1e4
    unsigned_bps = abs(diff) / entry_price * 1e4
    return {
        "fill_realism_signed_bps": signed_bps,
        "fill_realism_unsigned_bps": unsigned_bps,
    }


# ---------------------------------------------------------------------------
# Q6 — mark-vs-trade stop-trigger sensitivity (Phase 3r §8 exclusion rule)
# ---------------------------------------------------------------------------

def q6_per_trade(
    trade: dict,
    trade_klines: dict[int, dict],
    mark_klines: dict[int, dict],
    invalid_windows: list[tuple[int, int]],
) -> dict[str, Any]:
    """Compute mark-vs-trade stop-trigger 5m-bar timing difference for STOP-exited
    trades, applying Phase 3r §8 invalid-window exclusion.

    Q6 analysis window predeclaration (Phase 3r §8 / Phase 3p §6.1): the entire
    trade lifetime [entry_ot, exit_ot] is the Q6 analysis window. If any 5m
    `open_time` in that window equals an `invalid_window` boundary or any 5m
    bar within the window is missing from the mark-price 5m dataset, the trade
    is excluded from Q6.
    """
    out: dict[str, Any] = {
        "applicable": trade["exit_reason"] == "STOP",
        "excluded": False,
        "exclusion_reason": None,
        "mark_minus_trade_5m_bars": None,
    }
    if not out["applicable"]:
        return out
    direction = trade["direction"]
    stop_level = trade["initial_stop"]
    entry_ot = bar_open_time_for(trade["entry_fill_time_ms"])
    exit_ot = bar_open_time_for(trade["exit_fill_time_ms"])
    # Phase 3r §8 exclusion test
    invalid_match = intersects_invalid(entry_ot, exit_ot, invalid_windows)
    if invalid_match is not None:
        out["excluded"] = True
        out["exclusion_reason"] = f"q6_window_intersects_invalid_window:{invalid_match}"
        return out
    # Also exclude if any 5m mark-bar in the window is missing
    t = entry_ot
    while t <= exit_ot:
        if t not in mark_klines:
            out["excluded"] = True
            out["exclusion_reason"] = f"missing_mark_5m_bar_at:{t}"
            return out
        t += INTERVAL_5M_MS
    # Find first 5m bar where trade-price stop would trigger
    trade_trigger_ot = None
    mark_trigger_ot = None
    t = entry_ot
    while t <= exit_ot:
        tb = trade_klines.get(t)
        mb = mark_klines.get(t)
        if tb is not None and trade_trigger_ot is None:
            if direction == "LONG":
                if tb["low"] <= stop_level:
                    trade_trigger_ot = t
            else:
                if tb["high"] >= stop_level:
                    trade_trigger_ot = t
        if mb is not None and mark_trigger_ot is None:
            if direction == "LONG":
                if mb["low"] <= stop_level:
                    mark_trigger_ot = t
            else:
                if mb["high"] >= stop_level:
                    mark_trigger_ot = t
        if trade_trigger_ot is not None and mark_trigger_ot is not None:
            break
        t += INTERVAL_5M_MS
    if trade_trigger_ot is None or mark_trigger_ot is None:
        # Stop level not actually breached at 5m granularity (rare; could be
        # gap-fill rounding). Mark as inconclusive but keep counted.
        out["mark_minus_trade_5m_bars"] = None
        out["exclusion_reason"] = "no_5m_trigger_detected"
        return out
    out["mark_minus_trade_5m_bars"] = (mark_trigger_ot - trade_trigger_ot) // INTERVAL_5M_MS
    return out


# ---------------------------------------------------------------------------
# Population loader
# ---------------------------------------------------------------------------

def load_population(label: str, run_dir: str, run_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sym in SYMBOLS:
        p = BACKTESTS / run_dir / run_id / sym / "trade_log.parquet"
        if not p.exists():
            continue
        t = pq.read_table(str(p))
        for i in range(t.num_rows):
            r = {c: t.column(c).to_pylist()[i] for c in t.column_names}
            r["_candidate"] = label
            r["_population_path"] = str(p)
            rows.append(r)
    return rows


# ---------------------------------------------------------------------------
# Aggregations
# ---------------------------------------------------------------------------

def safe_mean(xs):
    xs = [x for x in xs if x is not None]
    return None if not xs else sum(xs) / len(xs)


def safe_median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 == 1 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def safe_pct(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    k = (len(xs) - 1) * p / 100
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    if f == c:
        return xs[f]
    return xs[f] + (xs[c] - xs[f]) * (k - f)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    # Eagerly load all 5m datasets and invalid-windows.
    klines_trade: dict[str, dict[int, dict]] = {}
    klines_mark: dict[str, dict[int, dict]] = {}
    invalid: dict[str, list[tuple[int, int]]] = {}
    for sym in SYMBOLS:
        klines_trade[sym] = load_5m_klines(sym, "trade")
        klines_mark[sym] = load_5m_klines(sym, "mark")
        invalid[sym] = load_invalid_windows(sym)
        print(
            f"loaded {sym}: trade={len(klines_trade[sym])} "
            f"mark={len(klines_mark[sym])} invalid={len(invalid[sym])}"
        )
        sys.stdout.flush()

    # Per-candidate results
    all_results: dict[str, dict[str, Any]] = {}
    q6_excl_table: list[dict[str, Any]] = []
    q1_per_candidate_q1: dict[str, list] = defaultdict(list)

    for label, run_dir, run_id in POPULATIONS:
        print(f"=== {label} ===")
        sys.stdout.flush()
        trades = load_population(label, run_dir, run_id)
        if not trades:
            all_results[label] = {"error": "no_trades_loaded", "run": f"{run_dir}/{run_id}"}
            continue
        # Per-trade augmentation
        q1_long = defaultdict(list)
        q2_counts = defaultdict(int)
        q3_counts = defaultdict(int)
        q3_total_stop_or_time = defaultdict(int)
        q4_curves = defaultdict(list)
        q5_signed = defaultdict(list)
        q5_unsigned = defaultdict(list)
        q6_results = []
        excl_keys = defaultdict(int)
        for tr in trades:
            sym = tr["symbol"]
            tk = klines_trade[sym]
            mk = klines_mark[sym]
            iw = invalid[sym]
            # Q1
            q1 = q1_per_trade(tr, tk)
            for k in ("iae_1", "iae_2", "iae_3", "ife_1", "ife_2", "ife_3"):
                q1_long[(sym, k)].append(q1[k])
            # Q1 IAE_1 list global per-candidate
            q1_per_candidate_q1[(label, sym)].append(q1["iae_1"])
            # Q2
            q2c = q2_per_trade(tr, tk)
            if q2c is not None:
                q2_counts[(sym, q2c)] += 1
            # Q3 (only on adverse-exit trades for the central question)
            q3 = q3_per_trade(tr, tk)
            if q3["adverse_exit"]:
                q3_total_stop_or_time[sym] += 1
                if q3["intrabar_target_1r"]:
                    q3_counts[(sym, "intrabar_1r")] += 1
                if q3["intrabar_target_2r"]:
                    q3_counts[(sym, "intrabar_2r")] += 1
                if q3["confirmed_target_1r"]:
                    q3_counts[(sym, "confirmed_1r")] += 1
                if q3["confirmed_target_2r"]:
                    q3_counts[(sym, "confirmed_2r")] += 1
            # Q4 (only D1A)
            if label == "D1A":
                q4 = q4_per_trade(tr, tk)
                for k, v in q4.items():
                    q4_curves[(sym, k)].append(v)
            # Q5
            q5 = q5_per_trade(tr, tk)
            q5_signed[sym].append(q5["fill_realism_signed_bps"])
            q5_unsigned[sym].append(q5["fill_realism_unsigned_bps"])
            # Q6
            q6 = q6_per_trade(tr, tk, mk, iw)
            q6_results.append(
                {
                    "sym": sym,
                    "direction": tr["direction"],
                    "exit_reason": tr["exit_reason"],
                    **q6,
                }
            )
            if q6["excluded"]:
                key = (label, sym, tr["direction"], tr["exit_reason"], q6["exclusion_reason"])
                excl_keys[key] += 1

        # Aggregations
        results: dict[str, Any] = {
            "candidate": label,
            "run": f"{run_dir}/{run_id}",
            "n_trades": len(trades),
            "n_trades_by_symbol": {
                sym: sum(1 for tr in trades if tr["symbol"] == sym) for sym in SYMBOLS
            },
            "q1": {},
            "q2": {},
            "q3": {},
            "q4": {},
            "q5": {},
            "q6": {},
        }
        for sym in SYMBOLS:
            results["q1"][sym] = {}
            for k in ("iae_1", "iae_2", "iae_3", "ife_1", "ife_2", "ife_3"):
                xs = q1_long[(sym, k)]
                results["q1"][sym][k] = {
                    "mean": safe_mean(xs),
                    "median": safe_median(xs),
                    "p25": safe_pct(xs, 25),
                    "p75": safe_pct(xs, 75),
                    "p90": safe_pct(xs, 90),
                    "n": sum(1 for x in xs if x is not None),
                }
            wick = q2_counts.get((sym, "wick_stop"), 0)
            sus = q2_counts.get((sym, "sustained_stop"), 0)
            ind = q2_counts.get((sym, "indeterminate"), 0)
            tot = wick + sus + ind
            results["q2"][sym] = {
                "wick_stop": wick,
                "sustained_stop": sus,
                "indeterminate": ind,
                "total_stop_classified": tot,
                "wick_fraction": (wick / tot) if tot > 0 else None,
            }
            adverse_n = q3_total_stop_or_time.get(sym, 0)
            results["q3"][sym] = {
                "n_adverse_exits": adverse_n,
                "intrabar_1r_count": q3_counts.get((sym, "intrabar_1r"), 0),
                "intrabar_2r_count": q3_counts.get((sym, "intrabar_2r"), 0),
                "confirmed_1r_count": q3_counts.get((sym, "confirmed_1r"), 0),
                "confirmed_2r_count": q3_counts.get((sym, "confirmed_2r"), 0),
                "intrabar_1r_fraction": (
                    (q3_counts.get((sym, "intrabar_1r"), 0) / adverse_n)
                    if adverse_n
                    else None
                ),
                "intrabar_2r_fraction": (
                    (q3_counts.get((sym, "intrabar_2r"), 0) / adverse_n)
                    if adverse_n
                    else None
                ),
            }
            if label == "D1A":
                results["q4"][sym] = {}
                for minutes in (5, 10, 15, 30, 60):
                    xs = q4_curves[(sym, f"decay_{minutes}m_R")]
                    n_valid = sum(1 for x in xs if x is not None)
                    mean = safe_mean(xs)
                    if n_valid >= 2:
                        valid = [x for x in xs if x is not None]
                        var = sum((x - mean) ** 2 for x in valid) / (n_valid - 1)
                        std = var ** 0.5
                        sem = std / (n_valid ** 0.5)
                    else:
                        sem = None
                    results["q4"][sym][f"decay_{minutes}m_R"] = {
                        "mean_R": mean,
                        "sem_R": sem,
                        "n_valid": n_valid,
                    }
            results["q5"][sym] = {
                "signed_bps_mean": safe_mean(q5_signed[sym]),
                "signed_bps_median": safe_median(q5_signed[sym]),
                "unsigned_bps_mean": safe_mean(q5_unsigned[sym]),
                "unsigned_bps_median": safe_median(q5_unsigned[sym]),
                "n": sum(1 for x in q5_signed[sym] if x is not None),
            }
            applicable = [r for r in q6_results if r["sym"] == sym and r["applicable"]]
            excluded = [r for r in applicable if r["excluded"]]
            included = [
                r
                for r in applicable
                if not r["excluded"] and r["mark_minus_trade_5m_bars"] is not None
            ]
            diffs = [r["mark_minus_trade_5m_bars"] for r in included]
            results["q6"][sym] = {
                "n_applicable": len(applicable),
                "n_excluded": len(excluded),
                "n_included": len(included),
                "n_inconclusive_5m_trigger": (
                    len(applicable) - len(excluded) - len(included)
                ),
                "mean_mark_minus_trade_5m_bars": safe_mean(diffs),
                "median_mark_minus_trade_5m_bars": safe_median(diffs),
                "fraction_simultaneous_trigger": (
                    (sum(1 for d in diffs if d == 0) / len(diffs)) if diffs else None
                ),
                "fraction_mark_lags_trade": (
                    (sum(1 for d in diffs if d > 0) / len(diffs)) if diffs else None
                ),
                "fraction_mark_leads_trade": (
                    (sum(1 for d in diffs if d < 0) / len(diffs)) if diffs else None
                ),
            }
        # Q6 exclusion-counts table
        for key, cnt in excl_keys.items():
            label2, sym, direction, exit_reason, reason = key
            q6_excl_table.append({
                "candidate": label2,
                "symbol": sym,
                "direction": direction,
                "exit_type": exit_reason,
                "exclusion_reason": reason,
                "count": cnt,
            })
        all_results[label] = results

    # Write outputs
    (OUT / "q1_q5_results.json").write_text(
        json.dumps(all_results, indent=2, default=str), encoding="utf-8"
    )
    (OUT / "q6_exclusion_counts.json").write_text(
        json.dumps(q6_excl_table, indent=2), encoding="utf-8"
    )

    # Summary print
    print()
    print("=== SUMMARY ===")
    for label, res in all_results.items():
        print(f"{label}: n_trades={res['n_trades']}")
    print()
    print(f"Q6 exclusion table rows: {len(q6_excl_table)}")
    print(f"Outputs in: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
