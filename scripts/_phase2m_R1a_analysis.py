"""Phase 2m R1a-on-R3 internal analysis (R-window + V-window + sensitivity).

One-shot analysis script (not a committed deliverable). Reads the
Phase 2m run directories under data/derived/backtests/phase-2m-r1a-*
and prints:

  - headline tables for H0, R3, R1a+R3 on R and (optionally) V
  - official deltas vs H0 (the H0 anchor governs the s10.3 / s10.4
    promotion verdict)
  - supplemental deltas vs R3 (descriptive only -- does R1a add value
    on top of R3?)
  - per-fold (5 rolling, GAP-036) consistency comparison
  - mandatory diagnostics: realized 1h volatility regime expR, MFE
    distribution, long/short asymmetry, exit-reason histogram,
    implementation-bug check (zero TRAILING_BREACH/STAGNATION in any
    R3-or-later variant)
  - R1a-specific diagnostics: setup-validity rate per fold (computed
    from the engine signal-funnel using both predicates) and the
    ATR-percentile distribution at filled R1a entries
  - V-window comparison (if PROMOTED on R)
  - slippage and stop-trigger sensitivity (if PROMOTED on R)

Outputs are stdout only; nothing committed. Mirrors the Phase 2l
analysis script's pattern.
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
from prometheus.strategy.indicators import wilder_atr

ROOT = Path("data/derived/backtests")
DATA_ROOT = Path("data")
VARIANTS = ["H0", "R3", "R1a+R3"]
EXPERIMENT_LABEL = {"H0": "h0", "R3": "r3", "R1a+R3": "r1a_plus_r3"}

BAR_15M_MS = 900_000
BAR_1H_MS = 3_600_000

ATR_REGIME_LOOKBACK = 1000  # trailing 1h-bar window for regime classification
ATR_REGIME_LOW_PCT = 1.0 / 3.0
ATR_REGIME_HIGH_PCT = 2.0 / 3.0

# R1a sub-parameters per Phase 2j memo sC.6 (committed singularly).
R1A_LOOKBACK = 200
R1A_PERCENTILE_THRESHOLD = 25
ATR_PERIOD_15M = 20


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
    sorted_in = sorted(in_fold, key=lambda t: t["exit_fill_time_ms"])
    running, peak, dd = 0.0, 0.0, 0.0
    for t in sorted_in:
        running += t["net_pnl"]
        peak = max(peak, running)
        dd = min(dd, running - peak)
    return dict(n=n, expR=exp, PF=pf_v, net=net, maxdd=dd)


def classify_h0_anchor(h0: dict, candidate: dict) -> tuple[str, list[str]]:
    """Apply Phase 2f s10.3 promotion + s10.3 disqualification + s10.4 with H0 as anchor."""

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
            reasons.append(f"s10.3.a (dexp={dexp:+.3f}, dPF={dpf:+.3f})")
        if dexp >= 0 and dn_pct >= 0.50 and d_abs_dd <= 1.0:
            reasons.append(
                f"s10.3.b (dexp={dexp:+.3f}, dn={dn_pct * 100:+.1f}%, d|dd|={d_abs_dd:+.3f}pp)"
            )
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


# --------------------------------------------------------------------------
# R1a-specific diagnostics (Phase 2j memo sC.16)
# --------------------------------------------------------------------------


def _load_15m_atr_series(symbol_str: str) -> tuple[list, list]:
    """Load 15m klines and compute Wilder ATR(20) per bar.

    Returns parallel lists (close_time_ms, atr_value); the ATR list has
    NaN for indices 0..20 and numeric values from 21+ matching the
    standalone `wilder_atr` reference convention.
    """
    klines_root = DATA_ROOT / "normalized" / "klines"
    klines = read_klines(klines_root, symbol=Symbol(symbol_str), interval=Interval.I_15M)
    close_times = [b.close_time for b in klines]
    highs = [b.high for b in klines]
    lows = [b.low for b in klines]
    closes = [b.close for b in klines]
    atrs = wilder_atr(highs, lows, closes, period=ATR_PERIOD_15M)
    return close_times, atrs


def atr_percentile_at_entries(trades: list, symbol_str: str) -> dict:
    """For each filled R1a entry, compute the realized percentile rank
    of A_prior within the trailing N-bar 15m ATR(20) distribution.

    Per Phase 2j memo sC.16 R1a-specific diagnostic. If R1a is admitting
    non-compression bars (the sC.12 failure mode), this distribution
    will not concentrate near the bottom of the rank.
    """
    if not trades:
        return {"n": 0}
    close_times, atrs = _load_15m_atr_series(symbol_str)
    pcts: list[float] = []
    for t in trades:
        # entry-fill happens at the next 15m bar's open after the breakout
        # bar's close. The percentile is computed against the 15m ATR(20)
        # at close of bar B-1, where B is the breakout bar (one before
        # the fill bar).
        fill_idx = bisect.bisect_left(close_times, t["entry_fill_time_ms"])
        if fill_idx <= 1:
            continue
        # B-1 = fill_idx - 2 (the bar before the breakout bar)
        prior_idx = fill_idx - 2
        if prior_idx < 0:
            continue
        a_prior = atrs[prior_idx]
        if a_prior is None or a_prior != a_prior:
            continue
        start = max(0, prior_idx - R1A_LOOKBACK + 1)
        window = [v for v in atrs[start : prior_idx + 1] if v is not None and v == v]
        if len(window) < R1A_LOOKBACK:
            continue
        sorted_w = sorted(window)
        less = sum(1 for v in sorted_w if v < a_prior)
        equal = sum(1 for v in sorted_w if v == a_prior)
        rank = less + (equal + 1) // 2  # 1-indexed mid-rank
        pct = rank / len(sorted_w) * 100.0
        pcts.append(pct)
    if not pcts:
        return {"n": 0}
    return {
        "n": len(pcts),
        "mean_pct": statistics.mean(pcts),
        "median_pct": statistics.median(pcts),
        "min_pct": min(pcts),
        "max_pct": max(pcts),
        "p25_pct": statistics.quantiles(pcts, n=4)[0] if len(pcts) >= 4 else pcts[0],
        "p75_pct": statistics.quantiles(pcts, n=4)[2] if len(pcts) >= 4 else pcts[-1],
        "frac_in_bottom_25pct": sum(1 for p in pcts if p <= 25.0) / len(pcts),
    }


def main() -> int:
    runs: dict[str, dict] = {}
    for v in VARIANTS:
        label = EXPERIMENT_LABEL[v]
        runs[f"{v}_R"] = load_run(f"phase-2m-r1a-{label}-r")
    for v in VARIANTS:
        label = EXPERIMENT_LABEL[v]
        with contextlib.suppress(FileNotFoundError):
            runs[f"{v}_V"] = load_run(f"phase-2m-r1a-{label}-v")
    with contextlib.suppress(FileNotFoundError):
        runs["R1a+R3_R_LOW"] = load_run("phase-2m-r1a-r1a_plus_r3-r-slip=LOW")
    with contextlib.suppress(FileNotFoundError):
        runs["R1a+R3_R_HIGH"] = load_run("phase-2m-r1a-r1a_plus_r3-r-slip=HIGH")
    with contextlib.suppress(FileNotFoundError):
        runs["R1a+R3_R_TP"] = load_run("phase-2m-r1a-r1a_plus_r3-r-stop=TRADE_PRICE")

    # ---- HEADLINE TABLE (R window) ----
    print("=" * 80)
    print("R-WINDOW HEADLINE (2022-01-01 -> 2025-01-01, 36 months)")
    print("=" * 80)
    print(
        f"{'var':8} {'sym':9} {'trades':>6} {'WR%':>6} {'expR':>7} {'PF':>6} "
        f"{'netPct':>7} {'maxDD%':>7} {'L/S':>7} {'exits':<35}"
    )
    print("-" * 110)
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs[f"{v}_R"], sym)
            exit_str = ", ".join(f"{k}={v_}" for k, v_ in sorted(r["exits"].items()))
            print(
                f"{v:8} {sym:9} {r['n']:>6} {r['wr'] * 100:>5.2f}% "
                f"{r['expR']:>+7.3f} {r['PF']:>6.3f} {r['net'] / 10000 * 100:>+6.2f}% "
                f"{r['maxdd_pct']:>6.2f}% {r['longs']}/{r['shorts']}  {exit_str}"
            )
        print()

    # ---- OFFICIAL: deltas vs H0 ----
    print("=" * 80)
    print("OFFICIAL -- Deltas vs H0 (governing s10.3 / s10.4 anchor)")
    print("=" * 80)
    for sym in ("BTCUSDT", "ETHUSDT"):
        h0r = row(runs["H0_R"], sym)
        cand = row(runs["R1a+R3_R"], sym)
        dexp = cand["expR"] - h0r["expR"]
        dpf = (
            (cand["PF"] - h0r["PF"])
            if (h0r["PF"] != float("inf") and cand["PF"] != float("inf"))
            else 0.0
        )
        dn_pct = (cand["n"] - h0r["n"]) / max(h0r["n"], 1) * 100
        ddd = cand["maxdd_pct"] - h0r["maxdd_pct"]
        dd_ratio = abs(cand["maxdd_pct"]) / abs(h0r["maxdd_pct"]) if h0r["maxdd_pct"] != 0 else 0.0
        print(
            f"\n  {sym} H0:     n={h0r['n']}  expR={h0r['expR']:+.3f}  "
            f"PF={h0r['PF']:.3f}  netPct={h0r['net'] / 10000 * 100:+.2f}%  "
            f"maxDD={h0r['maxdd_pct']:.2f}%"
        )
        print(
            f"  {sym} R1a+R3: n={cand['n']:>3} (d={dn_pct:+5.1f}%)  "
            f"expR={cand['expR']:+.3f} (d={dexp:+.3f})  "
            f"PF={cand['PF']:.3f} (d={dpf:+.3f})  "
            f"maxDD={cand['maxdd_pct']:.2f}% (d={ddd:+.2f}pp, |ratio|={dd_ratio:.3f}x)"
        )

    print("\n" + "=" * 80)
    print("OFFICIAL -- s10.3 / s10.4 verdict (H0 anchor; pre-declared thresholds)")
    print("=" * 80)
    status, reasons = classify_h0_anchor(runs["H0_R"], runs["R1a+R3_R"])
    print(f"  R1a+R3 -> {status}")
    for r_msg in reasons:
        print(f"      {r_msg}")

    # ---- SUPPLEMENTAL: deltas vs R3 (descriptive only) ----
    print("\n" + "=" * 80)
    print("SUPPLEMENTAL -- Deltas vs R3 (DESCRIPTIVE ONLY; not the governing anchor)")
    print("=" * 80)
    for sym in ("BTCUSDT", "ETHUSDT"):
        r3r = row(runs["R3_R"], sym)
        cand = row(runs["R1a+R3_R"], sym)
        dexp = cand["expR"] - r3r["expR"]
        dpf = (
            (cand["PF"] - r3r["PF"])
            if (r3r["PF"] != float("inf") and cand["PF"] != float("inf"))
            else 0.0
        )
        dn_pct = (cand["n"] - r3r["n"]) / max(r3r["n"], 1) * 100
        ddd = cand["maxdd_pct"] - r3r["maxdd_pct"]
        print(
            f"\n  {sym} R3:     n={r3r['n']}  expR={r3r['expR']:+.3f}  "
            f"PF={r3r['PF']:.3f}  maxDD={r3r['maxdd_pct']:.2f}%"
        )
        print(
            f"  {sym} R1a+R3: n={cand['n']:>3} (d={dn_pct:+5.1f}%)  "
            f"expR={cand['expR']:+.3f} (d={dexp:+.3f})  "
            f"PF={cand['PF']:.3f} (d={dpf:+.3f})  "
            f"maxDD={cand['maxdd_pct']:.2f}% (d={ddd:+.2f}pp)"
        )

    # ---- PER-FOLD (GAP-036) ----
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
    print(
        f"\n{'var':8} {'sym':9} "
        + " ".join(f"{lbl.split()[0]:>6}" for lbl, _, _, _ in rolling_folds)
        + "  metric"
    )
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            n_vals = [fold_stats(tl, s, e)["n"] for _, _, s, e in rolling_folds]
            exp_vals = [fold_stats(tl, s, e)["expR"] for _, _, s, e in rolling_folds]
            pf_vals = [fold_stats(tl, s, e)["PF"] for _, _, s, e in rolling_folds]
            print(f"{v:8} {sym:9} " + " ".join(f"{x:>6d}" for x in n_vals) + "  n_trades")
            print(f"{v:8} {sym:9} " + " ".join(f"{x:>+6.2f}" for x in exp_vals) + "  expR")
            pf_strs = [f"{x:>6.2f}" if x != float("inf") else "  inf " for x in pf_vals]
            print(f"{v:8} {sym:9} " + " ".join(pf_strs) + "  PF")
        print()

    print("Per-fold expR comparison R1a+R3 - H0 (positive = R1a+R3 better):")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl_h0 = runs["H0_R"]["symbols"][sym]["trades"]
        tl_cand = runs["R1a+R3_R"]["symbols"][sym]["trades"]
        n_better = 0
        n_total = 0
        for lbl, _, s, e in rolling_folds:
            h0_e = fold_stats(tl_h0, s, e)["expR"]
            c_e = fold_stats(tl_cand, s, e)["expR"]
            d = c_e - h0_e
            if d > 0:
                n_better += 1
            n_total += 1
            print(f"    {sym} {lbl}: H0={h0_e:+.3f} R1a+R3={c_e:+.3f}  d={d:+.3f}")
        print(f"    {sym}: R1a+R3 beats H0 in {n_better}/{n_total} folds")
        print()

    print("Per-fold expR comparison R1a+R3 - R3 (descriptive only):")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl_r3 = runs["R3_R"]["symbols"][sym]["trades"]
        tl_cand = runs["R1a+R3_R"]["symbols"][sym]["trades"]
        n_better = 0
        n_total = 0
        for lbl, _, s, e in rolling_folds:
            r3_e = fold_stats(tl_r3, s, e)["expR"]
            c_e = fold_stats(tl_cand, s, e)["expR"]
            d = c_e - r3_e
            if d > 0:
                n_better += 1
            n_total += 1
            print(f"    {sym} {lbl}: R3={r3_e:+.3f} R1a+R3={c_e:+.3f}  d={d:+.3f}")
        print(f"    {sym}: R1a+R3 beats R3 in {n_better}/{n_total} folds")
        print()

    # ---- Common diagnostics ----
    print("=" * 80)
    print("COMMON DIAGNOSTICS")
    print("=" * 80)

    print(
        "\n-- Per-regime expR (REQUIRED diagnostic: realized 1h volatility regime) --\n"
        f"   Convention: trailing {ATR_REGIME_LOOKBACK} 1h-bar window of Wilder ATR(20),\n"
        f"   tercile cutoffs at {ATR_REGIME_LOW_PCT * 100:.0f}% / {ATR_REGIME_HIGH_PCT * 100:.0f}%."
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
                f"  {v} {sym}: n={m['n']:3d}  mean={m['mean']:+.3f}  "
                f"median={m['median']:+.3f}  p25={m['p25']:+.3f}  "
                f"p75={m['p75']:+.3f}  max={m['max']:+.3f}"
            )

    print("\n-- Long/short asymmetry --")
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            a = long_short_asymmetry(tl)
            print(
                f"  {v} {sym}: "
                f"LONG  n={a['long_n']:3d} expR={a['long_expR']:+.3f} PF={a['long_PF']:.3f}  | "
                f"SHORT n={a['short_n']:3d} expR={a['short_expR']:+.3f} PF={a['short_PF']:.3f}"
            )

    # ---- Implementation-bug check ----
    print("\n-- IMPLEMENTATION-BUG CHECK --")
    bugs: list[str] = []
    for v in VARIANTS:
        if v == "H0":
            continue  # H0 keeps STAGED_TRAILING; STAGNATION is expected
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[f"{v}_R"]["symbols"][sym]["trades"]
            bad = sum(1 for t in tl if t["exit_reason"] in ("TRAILING_BREACH", "STAGNATION"))
            print(f"  {v} {sym}: TRAILING_BREACH+STAGNATION exits = {bad} (must be 0)")
            if bad > 0:
                bugs.append(f"{v} {sym} has {bad} forbidden exits")
    if bugs:
        print(f"  *** IMPLEMENTATION BUG: {bugs} ***")
    else:
        print("  All R3 / R1a+R3 exits use only {STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA}.")

    # ---- R1a-specific diagnostic: ATR-percentile distribution at entries ----
    print("\n-- R1a-SPECIFIC: ATR-percentile distribution at filled R1a entries --")
    print("   (Phase 2j sC.16; expected to concentrate near 0% if R1a is gating compression.)")
    for sym in ("BTCUSDT", "ETHUSDT"):
        tl = runs["R1a+R3_R"]["symbols"][sym]["trades"]
        d = atr_percentile_at_entries(tl, sym)
        if d["n"] == 0:
            print(f"  R1a+R3 {sym}: 0 entries with computable percentile")
        else:
            print(
                f"  R1a+R3 {sym}: n={d['n']:3d}  mean_pct={d['mean_pct']:.2f}%  "
                f"median_pct={d['median_pct']:.2f}%  min={d['min_pct']:.2f}%  "
                f"max={d['max_pct']:.2f}%  p25={d['p25_pct']:.2f}%  p75={d['p75_pct']:.2f}%  "
                f"frac<=25%={d['frac_in_bottom_25pct'] * 100:.2f}%"
            )

    # ---- R1a-specific diagnostic: setup-validity attribution comparison ----
    print("\n-- R1a-SPECIFIC: funnel rejected_no_valid_setup comparison (per symbol) --")
    print("   The R1a candidate's 'no valid setup' rejection count differs from H0's")
    print("   because the predicate's gating shape is different. Lower = predicate")
    print("   admitting more setups; higher = predicate admitting fewer.")
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            f = runs[f"{v}_R"]["symbols"][sym]["funnel"]
            print(
                f"  {v} {sym}: rejected_no_valid_setup={f['rejected_no_valid_setup']:6d}  "
                f"valid_setup_windows_detected={f['valid_setup_windows_detected']:5d}  "
                f"warmup_15m_excluded={f['warmup_15m_bars_excluded']:6d}"
            )
        print()

    # Trade-frequency sanity check
    print("-- Trade-frequency sanity check --")
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs[f"{v}_R"], sym)
            f = runs[f"{v}_R"]["symbols"][sym]["funnel"]
            print(
                f"  {v} {sym}: {r['n']:3d} closed trades   |   "
                f"funnel: entry_intents={f['entry_intents_produced']:3d}, "
                f"trades_filled={f['trades_filled']:3d}, "
                f"trades_closed={f['trades_closed']:3d}"
            )
        print()

    # ---- V-window ----
    if "R1a+R3_V" in runs:
        print("=" * 80)
        print("V-WINDOW (2025-01-01 -> 2026-04-01, 15 months) -- promotion-only run")
        print("=" * 80)
        print(
            f"{'var':8} {'sym':9} {'trades':>6} {'WR%':>6} {'expR':>7} {'PF':>6} "
            f"{'netPct':>7} {'maxDD%':>7} {'exits':<40}"
        )
        print("-" * 110)
        for v in VARIANTS:
            key = f"{v}_V"
            if key not in runs:
                continue
            for sym in ("BTCUSDT", "ETHUSDT"):
                r = row(runs[key], sym)
                exit_str = ", ".join(f"{k}={v_}" for k, v_ in sorted(r["exits"].items()))
                print(
                    f"{v:8} {sym:9} {r['n']:>6} {r['wr'] * 100:>5.2f}% "
                    f"{r['expR']:>+7.3f} {r['PF']:>6.3f} {r['net'] / 10000 * 100:>+6.2f}% "
                    f"{r['maxdd_pct']:>6.2f}% {exit_str}"
                )
            print()

    # ---- Slippage sensitivity ----
    if "R1a+R3_R_LOW" in runs and "R1a+R3_R_HIGH" in runs:
        print("=" * 80)
        print("SLIPPAGE SENSITIVITY (R1a+R3 on R window)")
        print("=" * 80)
        print(
            f"{'slip':6} {'sym':9} {'trades':>6} {'expR':>7} {'PF':>6} {'netPct':>7} {'maxDD%':>7}"
        )
        for slip_id, run_key in [
            ("LOW", "R1a+R3_R_LOW"),
            ("MED", "R1a+R3_R"),
            ("HIGH", "R1a+R3_R_HIGH"),
        ]:
            for sym in ("BTCUSDT", "ETHUSDT"):
                r = row(runs[run_key], sym)
                print(
                    f"{slip_id:6} {sym:9} {r['n']:>6} {r['expR']:>+7.3f} {r['PF']:>6.3f} "
                    f"{r['net'] / 10000 * 100:>+6.2f}% {r['maxdd_pct']:>6.2f}%"
                )
            print()

    # ---- Stop-trigger sensitivity ----
    if "R1a+R3_R_TP" in runs:
        print("=" * 80)
        print("STOP-TRIGGER-SOURCE SENSITIVITY (GAP-032; R1a+R3 on R window)")
        print("=" * 80)
        print(
            f"{'trig':12} {'sym':9} {'trades':>6} {'expR':>7} {'PF':>6} "
            f"{'netPct':>7} {'maxDD%':>7} {'gap_thr':>7}"
        )
        for trig_id, run_key in [("MARK_PRICE", "R1a+R3_R"), ("TRADE_PRICE", "R1a+R3_R_TP")]:
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
