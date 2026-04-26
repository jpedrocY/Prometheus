"""Phase 2l R3 internal analysis (R-window + V-window + sensitivity).

One-shot analysis script (not a committed deliverable). Reads the
Phase 2l run directories under data/derived/backtests/phase-2l-* and
prints the headline table, deltas-vs-H0, per-fold consistency,
mandatory diagnostics (per-regime expR, MFE distribution, long/short
asymmetry, TP R-multiple distribution, time-stop bias diagnostic),
Phase 2f s10.3 / s10.4 classification, V-window comparison, and
slippage / stop-trigger sensitivity.

Outputs are stdout only; nothing committed. Gitignored under data/
behavior applies only to its inputs, not to this script itself.
"""

from __future__ import annotations

import bisect
import json
import statistics
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.storage import read_klines
from prometheus.strategy.indicators import wilder_atr

ROOT = Path("data/derived/backtests")
DATA_ROOT = Path("data")
VARIANTS = ["H0", "R3"]

# Bar duration in ms for time-stop bias diagnostic.
BAR_15M_MS = 900_000

# Realized 1h volatility-regime classification convention.
# Trailing 1000 1h bars (~6 weeks) with tercile cutoffs.
ATR_REGIME_LOOKBACK = 1000
ATR_REGIME_LOW_PCT = 1.0 / 3.0
ATR_REGIME_HIGH_PCT = 2.0 / 3.0


def latest_run_dir(experiment_name: str) -> Path:
    dir_ = ROOT / experiment_name
    runs = sorted(d for d in dir_.iterdir() if d.is_dir())
    return runs[-1]


def load_run(experiment: str) -> dict:
    run = latest_run_dir(experiment)
    out: dict = {"experiment": experiment, "run_dir": str(run), "symbols": {}}
    for sym in ("BTCUSDT", "ETHUSDT"):
        sm = json.loads((run / sym / "summary_metrics.json").read_text())
        fn = json.loads((run / sym / "funnel_total.json").read_text())
        tl = json.loads((run / sym / "trade_log.json").read_text())["trades"]
        out["symbols"][sym] = {"summary": sm, "funnel": fn, "trades": tl}
    return out


def pf(trades: list) -> float:
    wins = [t["net_pnl"] for t in trades if t["net_pnl"] > 0]
    losses = [-t["net_pnl"] for t in trades if t["net_pnl"] <= 0]
    sw = sum(wins) if wins else 0.0
    sl = sum(losses) if losses else 0.0
    return sw / sl if sl > 0 else float("inf")


def row(run: dict, sym: str) -> dict:
    s = run["symbols"][sym]
    sm = s["summary"]
    tl = s["trades"]
    n = len(tl)
    exp = statistics.mean([t["net_r_multiple"] for t in tl]) if tl else 0.0
    pf_v = pf(tl)
    net = sm.get("realized_pnl", sum(t["net_pnl"] for t in tl))
    maxdd_pct = sm.get("max_drawdown_fraction", 0.0) * 100.0
    wr = sm.get("win_rate", 0.0)
    longs = sum(1 for t in tl if t["direction"] == "LONG")
    exits: defaultdict = defaultdict(int)
    for t in tl:
        exits[t["exit_reason"]] += 1
    return dict(
        n=n,
        expR=exp,
        PF=pf_v,
        net=net,
        maxdd_pct=maxdd_pct,
        wr=wr,
        longs=longs,
        shorts=n - longs,
        exits=dict(exits),
    )


def fold_stats(trades: list, start_ms: int, end_ms: int) -> dict:
    in_fold = [t for t in trades if start_ms <= t["entry_fill_time_ms"] < end_ms]
    n = len(in_fold)
    if n == 0:
        return dict(n=0, expR=0.0, PF=0.0, net=0.0, maxdd=0.0)
    exp = statistics.mean([t["net_r_multiple"] for t in in_fold])
    wins = sum(t["net_pnl"] for t in in_fold if t["net_pnl"] > 0)
    losses = -sum(t["net_pnl"] for t in in_fold if t["net_pnl"] <= 0)
    pf_v = wins / losses if losses > 0 else float("inf")
    net = sum(t["net_pnl"] for t in in_fold)
    # Per-fold maxDD via running cumulative net pnl.
    sorted_in = sorted(in_fold, key=lambda t: t["exit_fill_time_ms"])
    running, peak, dd = 0.0, 0.0, 0.0
    for t in sorted_in:
        running += t["net_pnl"]
        peak = max(peak, running)
        dd = min(dd, running - peak)
    return dict(n=n, expR=exp, PF=pf_v, net=net, maxdd=dd)


def classify_R3(h0: dict, r3: dict) -> tuple[str, list[str]]:
    """Apply Phase 2f s10.3 promotion + s10.3 disqualification + s10.4."""

    def _row(run: dict, sym: str) -> dict:
        return row(run, sym)

    def disqualify(r: dict, h0r: dict, sym: str) -> list[str]:
        reasons: list[str] = []
        if r["expR"] < h0r["expR"]:
            reasons.append(f"{sym}: expR worsens ({r['expR']:+.3f} vs {h0r['expR']:+.3f})")
        if r["PF"] < h0r["PF"] and h0r["PF"] != float("inf"):
            reasons.append(f"{sym}: PF worsens ({r['PF']:.3f} vs {h0r['PF']:.3f})")
        abs_h0 = abs(h0r["maxdd_pct"])
        abs_r = abs(r["maxdd_pct"])
        if abs_h0 > 0 and abs_r > 1.5 * abs_h0:
            reasons.append(
                f"{sym}: |maxDD|>1.5x baseline "
                f"({abs_r:.2f}% vs {abs_h0:.2f}% -> ratio {abs_r / abs_h0:.3f}x)"
            )
        return reasons

    def hard_reject(r: dict, h0r: dict, sym: str) -> list[str]:
        if r["n"] <= h0r["n"]:
            return []
        reasons: list[str] = []
        if r["expR"] < -0.50:
            reasons.append(f"{sym}: expR<-0.50 ({r['expR']:+.3f}) with rising trade count")
        if r["PF"] != float("inf") and r["PF"] < 0.30:
            reasons.append(f"{sym}: PF<0.30 ({r['PF']:.3f}) with rising trade count")
        return reasons

    def promote(r: dict, h0r: dict) -> list[str]:
        dexp = r["expR"] - h0r["expR"]
        dpf = (
            (r["PF"] - h0r["PF"])
            if (h0r["PF"] != float("inf") and r["PF"] != float("inf"))
            else 0.0
        )
        dn_pct = (r["n"] - h0r["n"]) / max(h0r["n"], 1)
        abs_h0 = abs(h0r["maxdd_pct"])
        abs_r = abs(r["maxdd_pct"])
        d_abs_dd = abs_r - abs_h0
        reasons: list[str] = []
        if dexp >= 0.10 and dpf >= 0.05:
            reasons.append(f"s10.3.a (d_exp={dexp:+.3f}, d_PF={dpf:+.3f})")
        if dexp >= 0 and dn_pct >= 0.50 and d_abs_dd <= 1.0:
            reasons.append(
                f"s10.3.b (d_exp={dexp:+.3f}, d_n={dn_pct * 100:+.1f}%, d_|dd|={d_abs_dd:+.3f}pp)"
            )
        # s10.3.c strict-dominance for exit-philosophy-only changes.
        if dexp > 0 and dpf > 0 and d_abs_dd <= 0:
            reasons.append(
                f"s10.3.c strict-dominance (d_exp={dexp:+.3f}, d_PF={dpf:+.3f}, "
                f"d_|dd|={d_abs_dd:+.3f}pp)"
            )
        return reasons

    r3_btc = _row(r3, "BTCUSDT")
    r3_eth = _row(r3, "ETHUSDT")
    h0_btc = _row(h0, "BTCUSDT")
    h0_eth = _row(h0, "ETHUSDT")

    dq_btc = disqualify(r3_btc, h0_btc, "BTC")
    dq_eth = disqualify(r3_eth, h0_eth, "ETH")
    hr_btc = hard_reject(r3_btc, h0_btc, "BTC")
    hr_eth = hard_reject(r3_eth, h0_eth, "ETH")

    if dq_btc or hr_btc:
        return ("DISQUALIFY", dq_btc + hr_btc)
    if hr_eth:
        return ("REJECT-ETH-CATASTROPHIC", hr_eth)

    btc_prom = promote(r3_btc, h0_btc)
    eth_prom = promote(r3_eth, h0_eth)
    msgs: list[str] = []
    if btc_prom and not dq_eth:
        msgs.append("BTC clears: " + ", ".join(btc_prom))
        if eth_prom:
            msgs.append("ETH also clears: " + ", ".join(eth_prom))
        else:
            msgs.append("ETH clears s10.3 / s10.4 floors (no catastrophic failure)")
        return ("PROMOTE", msgs)
    if btc_prom and dq_eth:
        return (
            "PROMOTE-WITH-ETH-CAVEAT",
            [f"BTC clears: {btc_prom}", f"ETH disqualified: {dq_eth}"],
        )
    if eth_prom and not btc_prom:
        return (
            "ETH-ONLY-NOTE",
            [f"ETH clears: {eth_prom}", "BTC does not clear s10.3 (s11.4 ETH-only N/A)"],
        )
    return ("HOLD", ["No s10.3 path met; baseline-equivalent or worse on BTC"])


def _load_1h_atr(symbol_str: str) -> tuple[list, list]:
    """Load 1h klines (close_time, atr_20) for the given symbol.

    Uses the same bars_1h_root the runner reads from. Returns parallel
    lists of close_time_ms and Wilder ATR(20) values. Output ATR list
    has NaN at indices 0..20 (warmup) and numeric values from 21+.
    """
    bars_1h_root = DATA_ROOT / "derived" / "bars_1h" / "standard"
    klines = read_klines(bars_1h_root, symbol=Symbol(symbol_str), interval=Interval.I_1H)
    close_times = [b.close_time for b in klines]
    highs = [b.high for b in klines]
    lows = [b.low for b in klines]
    closes = [b.close for b in klines]
    atrs = wilder_atr(highs, lows, closes, period=20)
    return close_times, atrs


def regime_label_for_entry(
    close_times: list,
    atrs: list,
    entry_fill_time_ms: int,
    lookback: int = ATR_REGIME_LOOKBACK,
) -> str | None:
    """Classify a trade entry by realized 1h volatility regime.

    Looks up the most recent COMPLETED 1h bar at entry time, takes its
    Wilder ATR(20) value, and computes the percentile rank of that
    value within the trailing ``lookback`` 1h ATR(20) values (inclusive
    of the current bar). Returns:

        "low_vol"  if percentile <= 1/3
        "med_vol"  if 1/3 <  percentile <= 2/3
        "high_vol" if percentile >  2/3

    Returns None if there are not enough non-NaN ATR values in the
    trailing window to classify (warmup region).
    """
    # Most recent 1h bar with close_time < entry_fill_time_ms.
    idx = bisect.bisect_left(close_times, entry_fill_time_ms) - 1
    if idx < 0:
        return None
    cur = atrs[idx]
    if cur is None or cur != cur:  # NaN check
        return None
    start = max(0, idx - lookback + 1)
    window = [a for a in atrs[start : idx + 1] if a is not None and a == a]
    if len(window) < lookback // 4:  # require at least 25% of lookback in non-NaN
        return None
    sorted_w = sorted(window)
    # Mid-rank percentile: count strictly-less + 0.5 * count-equal.
    less = sum(1 for h in sorted_w if h < cur)
    equal = sum(1 for h in sorted_w if h == cur)
    pct = (less + 0.5 * equal) / len(sorted_w)
    if pct <= ATR_REGIME_LOW_PCT:
        return "low_vol"
    if pct <= ATR_REGIME_HIGH_PCT:
        return "med_vol"
    return "high_vol"


def regime_decompose_realized_vol(trades: list, symbol_str: str) -> dict[str, dict]:
    """Per-regime aggregation of expR / PF / WR / trade count.

    Regime classification uses realized 1h volatility (Wilder ATR(20)
    at entry, trailing-percentile vs. last 1000 1h bars, terciles
    33/67) per the operator-required diagnostic spec.
    """
    close_times, atrs = _load_1h_atr(symbol_str)
    buckets: dict[str, list] = {"low_vol": [], "med_vol": [], "high_vol": [], "unclassified": []}
    for t in trades:
        label = regime_label_for_entry(close_times, atrs, t["entry_fill_time_ms"])
        buckets[label or "unclassified"].append(t)
    out: dict[str, dict] = {}
    for label, ts in buckets.items():
        if not ts:
            out[label] = {"n": 0, "expR": 0.0, "PF": 0.0, "wr": 0.0}
        else:
            wins = [x for x in ts if x["net_pnl"] > 0]
            out[label] = {
                "n": len(ts),
                "expR": statistics.mean(t["net_r_multiple"] for t in ts),
                "PF": pf(ts),
                "wr": len(wins) / len(ts),
            }
    return out


def duration_bucket_decompose(trades: list) -> dict[str, dict]:
    """AUXILIARY (proxy) diagnostic: per-trade-duration-bucket expR.

    NOT the required per-regime expR diagnostic — that one is in
    ``regime_decompose_realized_vol``. This bucket-by-trade-duration
    breakdown is retained as a supplemental view because it surfaces
    R3's structural mechanism (R3 specifically reshapes short-duration
    trade outcomes via the time-stop), but it should not be conflated
    with realized-volatility-regime classification.

    Buckets are by completed-bar count from entry-fill to exit-fill:

        short_duration   : <= 4 bars  (~1 hour)
        medium_duration  : 5..8 bars  (~1.25..2 hours)
        long_duration    : > 8 bars   (> 2 hours)
    """
    by_bucket: dict[str, list] = {
        "short_duration": [],
        "medium_duration": [],
        "long_duration": [],
    }
    for t in trades:
        dur_bars = (t["exit_fill_time_ms"] - t["entry_fill_time_ms"]) // BAR_15M_MS
        if dur_bars <= 4:
            label = "short_duration"
        elif dur_bars <= 8:
            label = "medium_duration"
        else:
            label = "long_duration"
        by_bucket[label].append(t)
    out: dict[str, dict] = {}
    for label, ts in by_bucket.items():
        if not ts:
            out[label] = {"n": 0, "expR": 0.0}
        else:
            out[label] = {
                "n": len(ts),
                "expR": statistics.mean(t["net_r_multiple"] for t in ts),
                "PF": pf(ts),
            }
    return out


def mfe_distribution(trades: list) -> dict:
    if not trades:
        return {"n": 0}
    mfes = [t.get("mfe_r", 0.0) for t in trades]
    return {
        "n": len(mfes),
        "mean": statistics.mean(mfes),
        "median": statistics.median(mfes),
        "p25": statistics.quantiles(mfes, n=4)[0] if len(mfes) >= 4 else mfes[0],
        "p75": statistics.quantiles(mfes, n=4)[2] if len(mfes) >= 4 else mfes[-1],
        "max": max(mfes),
    }


def long_short_asymmetry(trades: list) -> dict:
    longs = [t for t in trades if t["direction"] == "LONG"]
    shorts = [t for t in trades if t["direction"] == "SHORT"]
    return {
        "long_n": len(longs),
        "long_expR": statistics.mean(t["net_r_multiple"] for t in longs) if longs else 0.0,
        "long_PF": pf(longs),
        "short_n": len(shorts),
        "short_expR": statistics.mean(t["net_r_multiple"] for t in shorts) if shorts else 0.0,
        "short_PF": pf(shorts),
    }


def tp_r_distribution(trades: list) -> dict:
    """R-multiple distribution for TAKE_PROFIT exits.

    For R3 with R-target = 2.0, TAKE_PROFIT exits should cluster near
    +2 R minus fees + slippage; significant deviation indicates the
    next-bar-open fill mechanism is over- or under-shooting.
    """
    tps = [t for t in trades if t["exit_reason"] == "TAKE_PROFIT"]
    if not tps:
        return {"n": 0}
    rs = [t["net_r_multiple"] for t in tps]
    return {
        "n": len(tps),
        "mean_r": statistics.mean(rs),
        "min_r": min(rs),
        "max_r": max(rs),
        "stdev_r": statistics.stdev(rs) if len(rs) > 1 else 0.0,
    }


def time_stop_bias_diagnostic(trades: list) -> dict:
    """Time-stop bias: compare TIME_STOP exits' net R distribution against
    the overall non-TP / non-STOP distribution. If TIME_STOP trades have
    materially worse R than other exits (e.g., consistent slow-bleed
    losers), R3 is biting structurally rather than randomly.
    """
    tss = [t for t in trades if t["exit_reason"] == "TIME_STOP"]
    if not tss:
        return {"n": 0}
    rs = [t["net_r_multiple"] for t in tss]
    return {
        "n": len(tss),
        "mean_r": statistics.mean(rs),
        "median_r": statistics.median(rs),
        "min_r": min(rs),
        "max_r": max(rs),
        "stdev_r": statistics.stdev(rs) if len(rs) > 1 else 0.0,
        "frac_negative": sum(1 for r in rs if r < 0) / len(rs),
    }


def main() -> int:
    runs: dict[str, dict] = {}
    runs["H0_R"] = load_run("phase-2l-h0-r")
    runs["R3_R"] = load_run("phase-2l-r3-r")
    runs["H0_V"] = load_run("phase-2l-h0-v")
    runs["R3_V"] = load_run("phase-2l-r3-v")
    runs["R3_R_LOW"] = load_run("phase-2l-r3-r-slip=LOW")
    runs["R3_R_HIGH"] = load_run("phase-2l-r3-r-slip=HIGH")
    runs["R3_R_TP"] = load_run("phase-2l-r3-r-stop=TRADE_PRICE")

    # ---- R-WINDOW HEADLINE ----
    print("=" * 80)
    print("R-WINDOW HEADLINE (2022-01-01 -> 2025-01-01, 36 months)")
    print("=" * 80)
    print(
        f"{'var':5} {'sym':9} {'trades':>6} {'WR%':>6} {'expR':>7} {'PF':>6} "
        f"{'netPct':>7} {'maxDD%':>7} {'L/S':>7} {'exits':<35}"
    )
    print("-" * 110)
    for v_id, run_key in [("H0", "H0_R"), ("R3", "R3_R")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs[run_key], sym)
            exit_str = ", ".join(f"{k}={v}" for k, v in sorted(r["exits"].items()))
            print(
                f"{v_id:5} {sym:9} {r['n']:>6} {r['wr'] * 100:>5.2f}% "
                f"{r['expR']:>+7.3f} {r['PF']:>6.3f} {r['net'] / 10000 * 100:>+6.2f}% "
                f"{r['maxdd_pct']:>6.2f}% {r['longs']}/{r['shorts']}  {exit_str}"
            )
        print()

    # ---- DELTAS ----
    print("=" * 80)
    print("Deltas vs H0 (R window)")
    print("=" * 80)
    for sym in ("BTCUSDT", "ETHUSDT"):
        h0r = row(runs["H0_R"], sym)
        r3r = row(runs["R3_R"], sym)
        dexp = r3r["expR"] - h0r["expR"]
        dpf = (
            (r3r["PF"] - h0r["PF"])
            if (h0r["PF"] != float("inf") and r3r["PF"] != float("inf"))
            else 0.0
        )
        dn_pct = (r3r["n"] - h0r["n"]) / max(h0r["n"], 1) * 100
        ddd = r3r["maxdd_pct"] - h0r["maxdd_pct"]
        dd_ratio = abs(r3r["maxdd_pct"]) / abs(h0r["maxdd_pct"]) if h0r["maxdd_pct"] != 0 else 0.0
        print(
            f"\n  {sym} H0: n={h0r['n']}  expR={h0r['expR']:+.3f}  "
            f"PF={h0r['PF']:.3f}  netPct={h0r['net'] / 10000 * 100:+.2f}%  "
            f"maxDD={h0r['maxdd_pct']:.2f}%"
        )
        print(
            f"  {sym} R3: n={r3r['n']:>3} (d={dn_pct:+5.1f}%)  "
            f"expR={r3r['expR']:+.3f} (d={dexp:+.3f})  "
            f"PF={r3r['PF']:.3f} (d={dpf:+.3f})  "
            f"maxDD={r3r['maxdd_pct']:.2f}% (d={ddd:+.2f}pp, |ratio|={dd_ratio:.3f}x)"
        )

    # ---- s10.3 / s10.4 CLASSIFICATION ----
    print("\n" + "=" * 80)
    print("s10.3 promote / s10.4 reject classification (pre-declared thresholds)")
    print("=" * 80)
    status, reasons = classify_R3(runs["H0_R"], runs["R3_R"])
    print(f"  R3 -> {status}")
    for r_msg in reasons:
        print(f"      {r_msg}")

    # ---- PER-FOLD 5-ROLLING (GAP-036) ----
    print("\n" + "=" * 80)
    print("Per-fold R analysis -- Phase 2f s11.2 + GAP-036 (5 rolling, fold-1 partial)")
    print("=" * 80)
    rolling_folds: list[tuple[str, str, int, int]] = []
    for test_lbl, train_lbl, (sy, sm), (ey, em) in [
        ("F1 2022H2", "train 2022-01..2022-06 (6m partial)", (2022, 7), (2023, 1)),
        ("F2 2023H1", "train 2022-01..2022-12 (12m)", (2023, 1), (2023, 7)),
        ("F3 2023H2", "train 2022-07..2023-06 (12m)", (2023, 7), (2024, 1)),
        ("F4 2024H1", "train 2023-01..2023-12 (12m)", (2024, 1), (2024, 7)),
        ("F5 2024H2", "train 2023-07..2024-06 (12m)", (2024, 7), (2025, 1)),
    ]:
        s_dt = datetime(sy, sm, 1, tzinfo=UTC)
        e_dt = datetime(ey, em, 1, tzinfo=UTC)
        rolling_folds.append(
            (test_lbl, train_lbl, int(s_dt.timestamp() * 1000), int(e_dt.timestamp() * 1000))
        )
    print()
    print(
        f"{'var':5} {'sym':9} "
        + " ".join(f"{lbl.split()[0]:>6}" for lbl, _, _, _ in rolling_folds)
        + "  metric"
    )
    for v_id, run_key in [("H0", "H0_R"), ("R3", "R3_R")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[run_key]["symbols"][sym]["trades"]
            n_vals = [fold_stats(tl, s, e)["n"] for _, _, s, e in rolling_folds]
            exp_vals = [fold_stats(tl, s, e)["expR"] for _, _, s, e in rolling_folds]
            pf_vals = [fold_stats(tl, s, e)["PF"] for _, _, s, e in rolling_folds]
            print(f"{v_id:5} {sym:9} " + " ".join(f"{x:>6d}" for x in n_vals) + "  n_trades")
            print(f"{v_id:5} {sym:9} " + " ".join(f"{x:>+6.2f}" for x in exp_vals) + "  expR")
            pf_strs = [f"{x:>6.2f}" if x != float("inf") else "  inf " for x in pf_vals]
            print(f"{v_id:5} {sym:9} " + " ".join(pf_strs) + "  PF")
        print()

    # Per-fold consistency comparison: how many R3 folds beat H0?
    print("Per-fold expR comparison R3 - H0 (positive = R3 better):")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl_h0 = runs["H0_R"]["symbols"][sym]["trades"]
        tl_r3 = runs["R3_R"]["symbols"][sym]["trades"]
        n_better = 0
        n_total = 0
        for lbl, _, s, e in rolling_folds:
            h0_e = fold_stats(tl_h0, s, e)["expR"]
            r3_e = fold_stats(tl_r3, s, e)["expR"]
            d = r3_e - h0_e
            if d > 0:
                n_better += 1
            n_total += 1
            print(f"    {sym} {lbl}: H0={h0_e:+.3f} R3={r3_e:+.3f}  delta={d:+.3f}")
        print(f"    {sym}: R3 beats H0 in {n_better}/{n_total} folds")
        print()

    # ---- MANDATORY DIAGNOSTICS ----
    print("=" * 80)
    print("MANDATORY DIAGNOSTICS (per Phase 2k Gate 1 + Phase 2l brief)")
    print("=" * 80)

    print(
        "\n-- Per-regime expR (REQUIRED diagnostic: realized 1h volatility regime) --\n"
        f"   Convention: trailing {ATR_REGIME_LOOKBACK} 1h-bar window of Wilder ATR(20),\n"
        f"   tercile cutoffs at {ATR_REGIME_LOW_PCT * 100:.0f}% / {ATR_REGIME_HIGH_PCT * 100:.0f}%."
    )
    for v_id, run_key in [("H0", "H0_R"), ("R3", "R3_R")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[run_key]["symbols"][sym]["trades"]
            r = regime_decompose_realized_vol(tl, sym)
            print(f"  {v_id} {sym}:")
            for label in ("low_vol", "med_vol", "high_vol", "unclassified"):
                stats = r[label]
                if stats["n"] == 0:
                    print(f"    {label:13s}: n=0")
                else:
                    print(
                        f"    {label:13s}: n={stats['n']:3d}  "
                        f"expR={stats['expR']:+.3f}  PF={stats['PF']:.3f}  "
                        f"WR={stats['wr'] * 100:.2f}%"
                    )

    print(
        "\n-- AUXILIARY (proxy) diagnostic: trade-duration-bucket expR --\n"
        "   Retained as supplemental — surfaces R3's mechanism but is NOT\n"
        "   the realized-volatility-regime classification above."
    )
    for v_id, run_key in [("H0", "H0_R"), ("R3", "R3_R")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[run_key]["symbols"][sym]["trades"]
            r = duration_bucket_decompose(tl)
            print(f"  {v_id} {sym}:")
            for label, stats in r.items():
                if stats["n"] == 0:
                    print(f"    {label:18s}: n=0")
                else:
                    print(
                        f"    {label:18s}: n={stats['n']:3d}  "
                        f"expR={stats['expR']:+.3f}  PF={stats.get('PF', 0.0):.3f}"
                    )

    print("\n-- MFE distribution in R units --")
    for v_id, run_key in [("H0", "H0_R"), ("R3", "R3_R")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[run_key]["symbols"][sym]["trades"]
            m = mfe_distribution(tl)
            if m["n"] == 0:
                print(f"  {v_id} {sym}: n=0")
                continue
            print(
                f"  {v_id} {sym}: n={m['n']:3d}  mean={m['mean']:+.3f}  "
                f"median={m['median']:+.3f}  p25={m['p25']:+.3f}  "
                f"p75={m['p75']:+.3f}  max={m['max']:+.3f}"
            )

    print("\n-- Long/short asymmetry --")
    for v_id, run_key in [("H0", "H0_R"), ("R3", "R3_R")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[run_key]["symbols"][sym]["trades"]
            a = long_short_asymmetry(tl)
            print(
                f"  {v_id} {sym}: "
                f"LONG  n={a['long_n']:3d} expR={a['long_expR']:+.3f} PF={a['long_PF']:.3f}  | "
                f"SHORT n={a['short_n']:3d} expR={a['short_expR']:+.3f} PF={a['short_PF']:.3f}"
            )

    print("\n-- TAKE_PROFIT R-multiple distribution (R3 only) --")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl = runs["R3_R"]["symbols"][sym]["trades"]
        d = tp_r_distribution(tl)
        if d["n"] == 0:
            print(f"  R3 {sym}: 0 take-profit exits")
        else:
            print(
                f"  R3 {sym}: n={d['n']:2d}  mean_r={d['mean_r']:+.3f}  "
                f"min={d['min_r']:+.3f}  max={d['max_r']:+.3f}  stdev={d['stdev_r']:.3f}"
            )
            print("           (R-target=2.0; expected mean_r near +2 R minus fees+slippage)")

    print("\n-- TIME_STOP bias diagnostic (R3 only) --")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl = runs["R3_R"]["symbols"][sym]["trades"]
        d = time_stop_bias_diagnostic(tl)
        if d["n"] == 0:
            print(f"  R3 {sym}: 0 time-stop exits")
        else:
            print(
                f"  R3 {sym}: n={d['n']:2d}  mean_r={d['mean_r']:+.3f}  "
                f"median_r={d['median_r']:+.3f}  "
                f"frac_negative={d['frac_negative']:.2%}  stdev={d['stdev_r']:.3f}"
            )
            print(
                "           (mean_r near 0 = symmetric; mean_r << 0 = systematic slow-bleed loss)"
            )

    # ---- IMPLEMENTATION-BUG CHECK ----
    print("\n-- IMPLEMENTATION-BUG CHECK (TRAILING_BREACH or STAGNATION in R3) --")
    bugs_found: list[str] = []
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl = runs["R3_R"]["symbols"][sym]["trades"]
        bad = sum(1 for t in tl if t["exit_reason"] in ("TRAILING_BREACH", "STAGNATION"))
        print(f"  R3 {sym}: TRAILING_BREACH+STAGNATION exits = {bad} (must be 0)")
        if bad > 0:
            bugs_found.append(f"{sym} has {bad} forbidden exits")
    if bugs_found:
        print(f"  *** IMPLEMENTATION BUG: {bugs_found} ***")
    else:
        print("  All R3 exits use only {STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA}: clean.")

    # ---- V-WINDOW ----
    print("\n" + "=" * 80)
    print("V-WINDOW (2025-01-01 -> 2026-04-01, 15 months) — promotion-only run")
    print("=" * 80)
    print(
        f"{'var':5} {'sym':9} {'trades':>6} {'WR%':>6} {'expR':>7} {'PF':>6} "
        f"{'netPct':>7} {'maxDD%':>7} {'exits':<40}"
    )
    print("-" * 110)
    for v_id, run_key in [("H0", "H0_V"), ("R3", "R3_V")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs[run_key], sym)
            exit_str = ", ".join(f"{k}={v}" for k, v in sorted(r["exits"].items()))
            print(
                f"{v_id:5} {sym:9} {r['n']:>6} {r['wr'] * 100:>5.2f}% "
                f"{r['expR']:>+7.3f} {r['PF']:>6.3f} {r['net'] / 10000 * 100:>+6.2f}% "
                f"{r['maxdd_pct']:>6.2f}% {exit_str}"
            )
        print()

    # ---- SLIPPAGE SENSITIVITY ----
    print("=" * 80)
    print("SLIPPAGE SENSITIVITY (R3 on R window)")
    print("=" * 80)
    print(f"{'slip':6} {'sym':9} {'trades':>6} {'expR':>7} {'PF':>6} {'netPct':>7} {'maxDD%':>7}")
    for slip_id, run_key in [("LOW", "R3_R_LOW"), ("MED", "R3_R"), ("HIGH", "R3_R_HIGH")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs[run_key], sym)
            print(
                f"{slip_id:6} {sym:9} {r['n']:>6} {r['expR']:>+7.3f} {r['PF']:>6.3f} "
                f"{r['net'] / 10000 * 100:>+6.2f}% {r['maxdd_pct']:>6.2f}%"
            )
        print()

    # ---- TRADE_PRICE SENSITIVITY (GAP-032) ----
    print("=" * 80)
    print("STOP-TRIGGER-SOURCE SENSITIVITY (GAP-032; R3 on R window)")
    print("=" * 80)
    print(
        f"{'trig':12} {'sym':9} {'trades':>6} {'expR':>7} {'PF':>6} "
        f"{'netPct':>7} {'maxDD%':>7} {'gap_thr':>7}"
    )
    for trig_id, run_key in [("MARK_PRICE", "R3_R"), ("TRADE_PRICE", "R3_R_TP")]:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs[run_key], sym)
            sm = runs[run_key]["symbols"][sym]["summary"]
            gap = sm.get("gap_through_stops", 0)
            print(
                f"{trig_id:12} {sym:9} {r['n']:>6} {r['expR']:>+7.3f} {r['PF']:>6.3f} "
                f"{r['net'] / 10000 * 100:>+6.2f}% {r['maxdd_pct']:>6.2f}% {gap:>7d}"
            )
        print()

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
