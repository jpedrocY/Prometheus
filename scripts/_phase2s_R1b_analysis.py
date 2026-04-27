"""Phase 2s R1b-narrow internal analysis (R-window + V-window + sensitivity).

Reads Phase 2s run directories under data/derived/backtests/phase-2s-r1b-*
and prints the headline tables, deltas-vs-H0 (governing), supplemental
deltas-vs-R3 (descriptive), per-fold (GAP-036), per-regime (realized
1h-vol), MFE distribution, long/short asymmetry, exit-reason histogram,
implementation-bug check, R1b-narrow-specific diagnostics (slope-strength
distribution at filled entries, funnel NEUTRAL-bias rejection comparison,
slope-strength bucket analysis, direction-asymmetry check), V-window
comparison, slippage and stop-trigger sensitivity.

Outputs are stdout only; nothing committed.
"""

from __future__ import annotations

import bisect
import contextlib
import json
import statistics
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.storage import read_klines
from prometheus.strategy.indicators import ema, wilder_atr

ROOT = Path("data/derived/backtests")
DATA_ROOT = Path("data")
VARIANTS = ["H0", "R3", "R1b-narrow"]
EXPERIMENT_LABEL = {"H0": "h0", "R3": "r3", "R1b-narrow": "r1b_narrow"}

BAR_15M_MS = 900_000
BAR_1H_MS = 3_600_000

ATR_REGIME_LOOKBACK = 1000  # 1h-bar trailing window for regime classification
ATR_REGIME_LOW_PCT = 1.0 / 3.0
ATR_REGIME_HIGH_PCT = 2.0 / 3.0

# R1b-narrow committed sub-parameter S = 0.0020
R1B_THRESHOLD = 0.0020

EMA_FAST_PERIOD = 50
EMA_SLOW_PERIOD = 200
SLOPE_LOOKBACK = 3


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
        return dict(n=0, expR=0.0, PF=0.0, net=0.0)
    exp = statistics.mean([t["net_r_multiple"] for t in in_fold])
    wins = sum(t["net_pnl"] for t in in_fold if t["net_pnl"] > 0)
    losses = -sum(t["net_pnl"] for t in in_fold if t["net_pnl"] <= 0)
    pf_v = wins / losses if losses > 0 else float("inf")
    net = sum(t["net_pnl"] for t in in_fold)
    return dict(n=n, expR=exp, PF=pf_v, net=net)


def classify_h0_anchor(h0: dict, candidate: dict) -> tuple[str, list[str]]:
    """Phase 2f §10.3 promotion + disqualification + §10.4 with H0 anchor."""

    def disqualify(r: dict, h0r: dict, sym: str) -> list[str]:
        reasons: list[str] = []
        if r["expR"] < h0r["expR"]:
            reasons.append(f"{sym}: expR worsens ({r['expR']:+.3f} vs {h0r['expR']:+.3f})")
        if r["PF"] < h0r["PF"] and h0r["PF"] != float("inf"):
            reasons.append(f"{sym}: PF worsens ({r['PF']:.3f} vs {h0r['PF']:.3f})")
        abs_h0 = abs(h0r["maxdd_pct"])
        abs_r = abs(r["maxdd_pct"])
        if abs_h0 > 0 and abs_r > 1.5 * abs_h0:
            reasons.append(f"{sym}: |maxDD|>1.5x baseline ({abs_r:.2f}% vs {abs_h0:.2f}%)")
        return reasons

    def hard_reject(r: dict, h0r: dict, sym: str) -> list[str]:
        if r["n"] <= h0r["n"]:
            return []
        reasons: list[str] = []
        if r["expR"] < -0.50:
            reasons.append(f"{sym}: expR<-0.50 with rising trade count")
        if r["PF"] != float("inf") and r["PF"] < 0.30:
            reasons.append(f"{sym}: PF<0.30 with rising trade count")
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
            reasons.append(f"s10.3.a (dexp={dexp:+.3f}, dPF={dpf:+.3f})")
        if dexp >= 0 and dn_pct >= 0.50 and d_abs_dd <= 1.0:
            reasons.append(f"s10.3.b (dexp={dexp:+.3f}, dn={dn_pct * 100:+.1f}%)")
        if dexp > 0 and dpf > 0 and d_abs_dd <= 0:
            reasons.append(
                f"s10.3.c strict-dominance (dexp={dexp:+.3f}, dPF={dpf:+.3f}, "
                f"d|dd|={d_abs_dd:+.3f}pp)"
            )
        return reasons

    btc = row(candidate, "BTCUSDT")
    eth = row(candidate, "ETHUSDT")
    h0_btc = row(h0, "BTCUSDT")
    h0_eth = row(h0, "ETHUSDT")

    dq_btc = disqualify(btc, h0_btc, "BTC")
    dq_eth = disqualify(eth, h0_eth, "ETH")
    hr_btc = hard_reject(btc, h0_btc, "BTC")
    hr_eth = hard_reject(eth, h0_eth, "ETH")

    if dq_btc or hr_btc:
        return ("DISQUALIFY", dq_btc + hr_btc)
    if hr_eth:
        return ("REJECT-ETH-CATASTROPHIC", hr_eth)

    btc_prom = promote(btc, h0_btc)
    eth_prom = promote(eth, h0_eth)
    msgs: list[str] = []
    if btc_prom and not dq_eth:
        msgs.append("BTC clears: " + ", ".join(btc_prom))
        if eth_prom:
            msgs.append("ETH also clears: " + ", ".join(eth_prom))
        else:
            msgs.append("ETH clears s10.3 / s10.4 floors")
        return ("PROMOTE", msgs)
    if btc_prom and dq_eth:
        return ("PROMOTE-WITH-ETH-CAVEAT", [f"BTC: {btc_prom}", f"ETH dq: {dq_eth}"])
    if eth_prom and not btc_prom:
        return ("ETH-ONLY-NOTE", [f"ETH: {eth_prom}", "BTC does not clear s10.3"])
    return ("HOLD", ["No s10.3 path met on BTC"])


# ----- 1h regime classification (realized vol) -----


def _load_1h_atr(symbol_str: str) -> tuple[list, list]:
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
    idx = bisect.bisect_left(close_times, entry_fill_time_ms) - 1
    if idx < 0:
        return None
    cur = atrs[idx]
    if cur is None or cur != cur:
        return None
    start = max(0, idx - lookback + 1)
    window = [a for a in atrs[start : idx + 1] if a is not None and a == a]
    if len(window) < lookback // 4:
        return None
    sorted_w = sorted(window)
    less = sum(1 for h in sorted_w if h < cur)
    equal = sum(1 for h in sorted_w if h == cur)
    pct = (less + 0.5 * equal) / len(sorted_w)
    if pct <= ATR_REGIME_LOW_PCT:
        return "low_vol"
    if pct <= ATR_REGIME_HIGH_PCT:
        return "med_vol"
    return "high_vol"


def regime_decompose(trades: list, symbol_str: str) -> dict[str, dict]:
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


# ----- R1b-narrow-specific diagnostics -----


def _load_1h_ema_fast(symbol_str: str) -> tuple[list, list]:
    """Return parallel (close_time_ms, ema_fast) per 1h bar.

    Matches the reference ``ema`` function's seeding convention.
    """
    bars_1h_root = DATA_ROOT / "derived" / "bars_1h" / "standard"
    klines = read_klines(bars_1h_root, symbol=Symbol(symbol_str), interval=Interval.I_1H)
    close_times = [b.close_time for b in klines]
    closes = [b.close for b in klines]
    emas = ema(closes, EMA_FAST_PERIOD)
    return close_times, emas


def slope_strength_at_entry(
    close_times: list,
    emas: list,
    entry_fill_time_ms: int,
) -> float | None:
    """Compute slope_strength_3 = (EMA[B-1] - EMA[B-1-3]) / EMA[B-1] at the
    1h bar B-1 just before the 15m entry fill.

    Returns None if insufficient EMA history.
    """
    # The 15m entry fills on bar B+1 open; the bias was evaluated at the
    # close of the 1h bar that completed before the 15m signal bar. We
    # approximate by finding the most recent 1h bar with close_time <
    # entry_fill_time_ms - BAR_15M_MS (the signal bar's open time).
    target_ms = entry_fill_time_ms - BAR_15M_MS
    idx = bisect.bisect_left(close_times, target_ms) - 1
    if idx < SLOPE_LOOKBACK:
        return None
    f_now = emas[idx]
    f_then = emas[idx - SLOPE_LOOKBACK]
    if f_now is None or f_now != f_now or f_then is None or f_then != f_then:
        return None
    if f_now <= 0:
        return None
    return (f_now - f_then) / f_now


def slope_strength_distribution(trades: list, symbol_str: str) -> dict:
    """For each filled R1b-narrow entry, compute slope_strength_3 at the
    bias-evaluation time (1h bar before signal). Per Phase 2r spec memo
    §P.1.
    """
    if not trades:
        return {"n": 0}
    close_times, emas = _load_1h_ema_fast(symbol_str)
    values: list[float] = []
    signed_values: list[float] = []  # preserves sign for direction analysis
    for t in trades:
        slope = slope_strength_at_entry(close_times, emas, t["entry_fill_time_ms"])
        if slope is None:
            continue
        values.append(abs(slope))
        signed_values.append(slope)
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "mean_abs": statistics.mean(values),
        "median_abs": statistics.median(values),
        "min_abs": min(values),
        "max_abs": max(values),
        "p25_abs": statistics.quantiles(values, n=4)[0] if len(values) >= 4 else values[0],
        "p75_abs": statistics.quantiles(values, n=4)[2] if len(values) >= 4 else values[-1],
        "min_signed": min(signed_values),
        "max_signed": max(signed_values),
        "frac_at_threshold": sum(1 for v in values if v < R1B_THRESHOLD * 1.05) / len(values),
        "signed": signed_values,
    }


def slope_strength_bucket_analysis(
    trades: list,
    symbol_str: str,
) -> dict[str, dict]:
    """Phase 2r §P.3: per-direction expR by |slope_strength_3| bucket.

    Buckets:
      Bucket 1: [+0.0020, +0.0050)  marginal-strength
      Bucket 2: [+0.0050, +0.0100)  moderate-strength
      Bucket 3: [+0.0100, +inf)     strong-strength
    """
    if not trades:
        return {}
    close_times, emas = _load_1h_ema_fast(symbol_str)
    buckets: dict[str, list] = {"marginal": [], "moderate": [], "strong": [], "unclassified": []}
    for t in trades:
        slope = slope_strength_at_entry(close_times, emas, t["entry_fill_time_ms"])
        if slope is None:
            buckets["unclassified"].append(t)
            continue
        absslope = abs(slope)
        if absslope < 0.0050:
            buckets["marginal"].append(t)
        elif absslope < 0.0100:
            buckets["moderate"].append(t)
        else:
            buckets["strong"].append(t)
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


def main() -> int:
    runs: dict[str, dict] = {}
    for v in VARIANTS:
        runs[f"{v}_R"] = load_run(f"phase-2s-r1b-{EXPERIMENT_LABEL[v]}-r")
    for v in VARIANTS:
        with contextlib.suppress(FileNotFoundError):
            runs[f"{v}_V"] = load_run(f"phase-2s-r1b-{EXPERIMENT_LABEL[v]}-v")
    with contextlib.suppress(FileNotFoundError):
        runs["R1b_LOW"] = load_run("phase-2s-r1b-r1b_narrow-r-slip=LOW")
    with contextlib.suppress(FileNotFoundError):
        runs["R1b_HIGH"] = load_run("phase-2s-r1b-r1b_narrow-r-slip=HIGH")
    with contextlib.suppress(FileNotFoundError):
        runs["R1b_TP"] = load_run("phase-2s-r1b-r1b_narrow-r-stop=TRADE_PRICE")

    # ---- Headline R-window ----
    print("=" * 80)
    print("R-WINDOW HEADLINE (2022-01-01 -> 2025-01-01, 36 months)")
    print("=" * 80)
    print(
        f"{'var':12} {'sym':9} {'trades':>6} {'WR%':>6} {'expR':>7} {'PF':>6} "
        f"{'netPct':>7} {'maxDD%':>7} {'L/S':>7} {'exits':<35}"
    )
    print("-" * 110)
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs[f"{v}_R"], sym)
            exit_str = ", ".join(f"{k}={v_}" for k, v_ in sorted(r["exits"].items()))
            print(
                f"{v:12} {sym:9} {r['n']:>6} {r['wr'] * 100:>5.2f}% "
                f"{r['expR']:>+7.3f} {r['PF']:>6.3f} {r['net'] / 10000 * 100:>+6.2f}% "
                f"{r['maxdd_pct']:>6.2f}% {r['longs']}/{r['shorts']}  {exit_str}"
            )
        print()

    # ---- Deltas vs H0 (governing) ----
    print("=" * 80)
    print("OFFICIAL -- Deltas vs H0 (governing s10.3 / s10.4 anchor)")
    print("=" * 80)
    for sym in ("BTCUSDT", "ETHUSDT"):
        h0r = row(runs["H0_R"], sym)
        cand = row(runs["R1b-narrow_R"], sym)
        dexp = cand["expR"] - h0r["expR"]
        dpf = cand["PF"] - h0r["PF"]
        dn_pct = (cand["n"] - h0r["n"]) / max(h0r["n"], 1) * 100
        ddd = cand["maxdd_pct"] - h0r["maxdd_pct"]
        dd_ratio = abs(cand["maxdd_pct"]) / abs(h0r["maxdd_pct"]) if h0r["maxdd_pct"] != 0 else 0.0
        print(
            f"\n  {sym} H0:         n={h0r['n']:>3}  expR={h0r['expR']:+.3f}  "
            f"PF={h0r['PF']:.3f}  netPct={h0r['net'] / 10000 * 100:+.2f}%  "
            f"maxDD={h0r['maxdd_pct']:.2f}%"
        )
        print(
            f"  {sym} R1b-narrow: n={cand['n']:>3} (d={dn_pct:+5.1f}%)  "
            f"expR={cand['expR']:+.3f} (d={dexp:+.3f})  "
            f"PF={cand['PF']:.3f} (d={dpf:+.3f})  "
            f"maxDD={cand['maxdd_pct']:.2f}% (d={ddd:+.2f}pp, ratio={dd_ratio:.3f}x)"
        )

    print("\n" + "=" * 80)
    print("OFFICIAL -- s10.3 / s10.4 verdict (H0 anchor)")
    print("=" * 80)
    status, reasons = classify_h0_anchor(runs["H0_R"], runs["R1b-narrow_R"])
    print(f"  R1b-narrow -> {status}")
    for r_msg in reasons:
        print(f"      {r_msg}")

    # ---- Supplemental deltas vs R3 ----
    print("\n" + "=" * 80)
    print("SUPPLEMENTAL -- Deltas vs R3 (descriptive only)")
    print("=" * 80)
    for sym in ("BTCUSDT", "ETHUSDT"):
        r3r = row(runs["R3_R"], sym)
        cand = row(runs["R1b-narrow_R"], sym)
        dexp = cand["expR"] - r3r["expR"]
        dpf = cand["PF"] - r3r["PF"]
        dn_pct = (cand["n"] - r3r["n"]) / max(r3r["n"], 1) * 100
        ddd = cand["maxdd_pct"] - r3r["maxdd_pct"]
        print(
            f"\n  {sym} R3:         n={r3r['n']}  expR={r3r['expR']:+.3f}  "
            f"PF={r3r['PF']:.3f}  maxDD={r3r['maxdd_pct']:.2f}%"
        )
        print(
            f"  {sym} R1b-narrow: n={cand['n']:>3} (d={dn_pct:+5.1f}%)  "
            f"expR={cand['expR']:+.3f} (d={dexp:+.3f})  "
            f"PF={cand['PF']:.3f} (d={dpf:+.3f})  "
            f"maxDD={cand['maxdd_pct']:.2f}% (d={ddd:+.2f}pp)"
        )

    # ---- Per-fold ----
    print("\n" + "=" * 80)
    print("Per-fold R analysis -- Phase 2f s11.2 + GAP-036 (5 rolling)")
    print("=" * 80)
    rolling_folds: list[tuple[str, int, int]] = []
    for test_lbl, (sy, sm), (ey, em) in [
        ("F1 2022H2", (2022, 7), (2023, 1)),
        ("F2 2023H1", (2023, 1), (2023, 7)),
        ("F3 2023H2", (2023, 7), (2024, 1)),
        ("F4 2024H1", (2024, 1), (2024, 7)),
        ("F5 2024H2", (2024, 7), (2025, 1)),
    ]:
        s_dt = datetime(sy, sm, 1, tzinfo=UTC)
        e_dt = datetime(ey, em, 1, tzinfo=UTC)
        rolling_folds.append((test_lbl, int(s_dt.timestamp() * 1000), int(e_dt.timestamp() * 1000)))
    print(
        f"\n{'var':12} {'sym':9} "
        + " ".join(f"{lbl.split()[0]:>6}" for lbl, _, _ in rolling_folds)
        + "  metric"
    )
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            n_vals = [fold_stats(tl, s, e)["n"] for _, s, e in rolling_folds]
            exp_vals = [fold_stats(tl, s, e)["expR"] for _, s, e in rolling_folds]
            print(f"{v:12} {sym:9} " + " ".join(f"{x:>6d}" for x in n_vals) + "  n_trades")
            print(f"{v:12} {sym:9} " + " ".join(f"{x:>+6.2f}" for x in exp_vals) + "  expR")
        print()

    # ---- Per-fold delta vs H0 ----
    print("Per-fold expR R1b-narrow - H0:")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl_h0 = runs["H0_R"]["symbols"][sym]["trades"]
        tl_cand = runs["R1b-narrow_R"]["symbols"][sym]["trades"]
        n_better = 0
        for lbl, s, e in rolling_folds:
            h0_e = fold_stats(tl_h0, s, e)["expR"]
            c_e = fold_stats(tl_cand, s, e)["expR"]
            d = c_e - h0_e
            if d > 0:
                n_better += 1
            print(f"    {sym} {lbl}: H0={h0_e:+.3f} R1b={c_e:+.3f}  d={d:+.3f}")
        print(f"    {sym}: R1b-narrow beats H0 in {n_better}/5 folds\n")

    print("Per-fold expR R1b-narrow - R3 (descriptive):")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl_r3 = runs["R3_R"]["symbols"][sym]["trades"]
        tl_cand = runs["R1b-narrow_R"]["symbols"][sym]["trades"]
        n_better = 0
        for lbl, s, e in rolling_folds:
            r3_e = fold_stats(tl_r3, s, e)["expR"]
            c_e = fold_stats(tl_cand, s, e)["expR"]
            d = c_e - r3_e
            if d > 0:
                n_better += 1
            print(f"    {sym} {lbl}: R3={r3_e:+.3f} R1b={c_e:+.3f}  d={d:+.3f}")
        print(f"    {sym}: R1b-narrow beats R3 in {n_better}/5 folds\n")

    # ---- Common diagnostics ----
    print("=" * 80)
    print("COMMON DIAGNOSTICS")
    print("=" * 80)

    print(
        "\n-- Per-regime expR (realized 1h volatility regime) --\n"
        f"   Convention: trailing {ATR_REGIME_LOOKBACK} 1h-bar window of Wilder ATR(20),\n"
        f"   tercile cutoffs 33% / 67%."
    )
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            r = regime_decompose(tl, sym)
            print(f"  {v} {sym}:")
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

    print("\n-- MFE distribution in R units --")
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            m = mfe_distribution(tl)
            if m["n"] == 0:
                print(f"  {v} {sym}: n=0")
                continue
            print(
                f"  {v:12} {sym}: n={m['n']:3d}  mean={m['mean']:+.3f}  "
                f"median={m['median']:+.3f}  p25={m['p25']:+.3f}  "
                f"p75={m['p75']:+.3f}  max={m['max']:+.3f}"
            )

    print("\n-- Long/short asymmetry --")
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            a = long_short_asymmetry(tl)
            print(
                f"  {v:12} {sym}: "
                f"L n={a['long_n']:3d} expR={a['long_expR']:+.3f} PF={a['long_PF']:.3f}  | "
                f"S n={a['short_n']:3d} expR={a['short_expR']:+.3f} PF={a['short_PF']:.3f}"
            )

    print("\n-- IMPLEMENTATION-BUG CHECK --")
    bugs: list[str] = []
    for v in VARIANTS:
        if v == "H0":
            continue
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            bad = sum(1 for t in tl if t["exit_reason"] in ("TRAILING_BREACH", "STAGNATION"))
            print(f"  {v} {sym}: TRAILING_BREACH+STAGNATION = {bad} (must be 0)")
            if bad > 0:
                bugs.append(f"{v} {sym} has {bad}")
    if bugs:
        print(f"  *** IMPLEMENTATION BUG: {bugs} ***")
    else:
        print("  All R3-or-R1b-narrow exits use only {STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA}.")

    # ---- R1b-narrow-specific diagnostics ----
    print("\n" + "=" * 80)
    print("R1b-NARROW-SPECIFIC DIAGNOSTICS (Phase 2r spec memo §P)")
    print("=" * 80)

    print("\n-- §P.1 Slope-strength distribution at filled R1b-narrow entries --")
    print("   (Expected: |slope_strength_3| >= 0.0020 for all entries.)")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl = runs["R1b-narrow_R"]["symbols"][sym]["trades"]
        d = slope_strength_distribution(tl, sym)
        if d["n"] == 0:
            print(f"  R1b-narrow {sym}: 0 entries with computable slope")
            continue
        print(
            f"  R1b-narrow {sym}: n={d['n']:3d}  "
            f"|mean|={d['mean_abs']:.4f} ({d['mean_abs'] * 100:.2f}%)  "
            f"|median|={d['median_abs']:.4f}  |min|={d['min_abs']:.4f}  "
            f"|max|={d['max_abs']:.4f}  "
            f"|p25|={d['p25_abs']:.4f}  |p75|={d['p75_abs']:.4f}"
        )
        print(
            f"    signed range: [{d['min_signed']:+.4f}, {d['max_signed']:+.4f}]  "
            f"frac_near_threshold(<1.05*S): {d['frac_at_threshold'] * 100:.2f}%"
        )
        if d["min_abs"] < R1B_THRESHOLD * 0.999:
            print("    *** WARNING: |slope| < S detected — potential implementation issue ***")

    print("\n-- §P.2 Funnel attribution: rejected_neutral_bias comparison --")
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            f = runs[f"{v}_R"]["symbols"][sym]["funnel"]
            print(
                f"  {v:12} {sym}: rejected_neutral_bias={f['rejected_neutral_bias']:7d}  "
                f"bias_long={f['bias_long_count']:6d}  bias_short={f['bias_short_count']:6d}  "
                f"bias_neutral={f['bias_neutral_count']:6d}"
            )
        print()

    print("-- §P.3 Per-direction expR by slope-strength bucket --")
    print(
        "   Bucket 1 [0.0020, 0.0050) marginal | "
        "2 [0.0050, 0.0100) moderate | 3 [0.0100,+inf) strong"
    )
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl = runs["R1b-narrow_R"]["symbols"][sym]["trades"]
        b = slope_strength_bucket_analysis(tl, sym)
        print(f"  R1b-narrow {sym}:")
        for label in ("marginal", "moderate", "strong", "unclassified"):
            stats = b.get(label, {"n": 0})
            if stats["n"] == 0:
                print(f"    {label:14s}: n=0")
            else:
                print(
                    f"    {label:14s}: n={stats['n']:3d}  "
                    f"expR={stats['expR']:+.3f}  PF={stats['PF']:.3f}  "
                    f"WR={stats['wr'] * 100:.2f}%"
                )

    print("\n-- §P.4 Direction-asymmetry check (R1b-narrow vs R3 vs H0) --")
    for sym in ("BTCUSDT", "ETHUSDT"):
        for v in VARIANTS:
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            a = long_short_asymmetry(tl)
            print(
                f"  {sym} {v:12}: L n={a['long_n']:3d} expR={a['long_expR']:+.3f} "
                f"PF={a['long_PF']:.3f}  | S n={a['short_n']:3d} expR={a['short_expR']:+.3f} "
                f"PF={a['short_PF']:.3f}"
            )
        print()

    # ---- Trade-frequency sanity check ----
    print("-- Trade-frequency sanity check --")
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs[f"{v}_R"], sym)
            f = runs[f"{v}_R"]["symbols"][sym]["funnel"]
            print(
                f"  {v:12} {sym}: {r['n']:3d} closed   |   "
                f"funnel: entry_intents={f['entry_intents_produced']:3d} "
                f"trades_filled={f['trades_filled']:3d}"
            )
        print()

    # ---- V-window ----
    if "R1b-narrow_V" in runs:
        print("=" * 80)
        print("V-WINDOW (2025-01-01 -> 2026-04-01, 15 months)")
        print("=" * 80)
        print(
            f"{'var':12} {'sym':9} {'trades':>6} {'WR%':>6} {'expR':>7} {'PF':>6} "
            f"{'netPct':>7} {'maxDD%':>7}"
        )
        print("-" * 90)
        for v in VARIANTS:
            key = f"{v}_V"
            if key not in runs:
                continue
            for sym in ("BTCUSDT", "ETHUSDT"):
                r = row(runs[key], sym)
                exit_str = ", ".join(f"{k}={v_}" for k, v_ in sorted(r["exits"].items()))
                print(
                    f"{v:12} {sym:9} {r['n']:>6} {r['wr'] * 100:>5.2f}% "
                    f"{r['expR']:>+7.3f} {r['PF']:>6.3f} {r['net'] / 10000 * 100:>+6.2f}% "
                    f"{r['maxdd_pct']:>6.2f}%  {exit_str}"
                )
            print()

    # ---- Slippage sensitivity ----
    if "R1b_LOW" in runs and "R1b_HIGH" in runs:
        print("=" * 80)
        print("SLIPPAGE SENSITIVITY (R1b-narrow on R window)")
        print("=" * 80)
        print(
            f"{'slip':6} {'sym':9} {'trades':>6} {'expR':>7} {'PF':>6} {'netPct':>7} {'maxDD%':>7}"
        )
        for slip_id, run_key in [("LOW", "R1b_LOW"), ("MED", "R1b-narrow_R"), ("HIGH", "R1b_HIGH")]:
            for sym in ("BTCUSDT", "ETHUSDT"):
                r = row(runs[run_key], sym)
                print(
                    f"{slip_id:6} {sym:9} {r['n']:>6} {r['expR']:>+7.3f} {r['PF']:>6.3f} "
                    f"{r['net'] / 10000 * 100:>+6.2f}% {r['maxdd_pct']:>6.2f}%"
                )
            print()

    # ---- Stop-trigger sensitivity ----
    if "R1b_TP" in runs:
        print("=" * 80)
        print("STOP-TRIGGER SENSITIVITY (GAP-032)")
        print("=" * 80)
        print(
            f"{'trig':12} {'sym':9} {'trades':>6} {'expR':>7} {'PF':>6} "
            f"{'netPct':>7} {'maxDD%':>7} {'gap_thr':>7}"
        )
        for trig_id, run_key in [("MARK_PRICE", "R1b-narrow_R"), ("TRADE_PRICE", "R1b_TP")]:
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
