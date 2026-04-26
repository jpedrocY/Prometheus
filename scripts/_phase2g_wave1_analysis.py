"""Phase 2g wave-1 internal analysis (R-window comparison + ranking).

One-shot analysis script (not a committed deliverable). Reads the 5
variant run directories under data/derived/backtests/phase-2g-wave1-*-r/
and prints the headline table, deltas-vs-H0, per-fold breakdown, and
Phase 2f Gate 1 s10.3 / s10.4 classification. Gitignored under data/
behavior applies only to its outputs, not to the script itself.
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("data/derived/backtests")
VARIANTS = ["H0", "H-A1", "H-B2", "H-C1", "H-D3"]


def latest_run_dir(experiment_name: str) -> Path:
    dir_ = ROOT / experiment_name
    runs = sorted(d for d in dir_.iterdir() if d.is_dir())
    return runs[-1]


def load_run(variant: str, window: str = "r") -> dict:
    exp = f"phase-2g-wave1-{variant.lower()}-{window}"
    run = latest_run_dir(exp)
    out: dict = {"variant": variant, "run_dir": str(run), "symbols": {}}
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


def row(runs: dict, v: str, sym: str) -> dict:
    s = runs[v]["symbols"][sym]
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
    fn = s["funnel"]
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
        setups=fn["valid_setup_windows_detected"],
        candidates=fn["long_breakout_candidates"] + fn["short_breakout_candidates"],
        rej_no_setup=fn["rejected_no_valid_setup"],
        rej_neutral_bias=fn["rejected_neutral_bias"],
        rej_no_close=fn["rejected_close_did_not_break_level"],
        rej_tr=fn["rejected_true_range_too_small"],
        entry_intents=fn["entry_intents_produced"],
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


def classify(runs: dict, v: str) -> tuple[str, str]:
    r_btc = row(runs, v, "BTCUSDT")
    r_eth = row(runs, v, "ETHUSDT")
    h0_btc = row(runs, "H0", "BTCUSDT")
    h0_eth = row(runs, "H0", "ETHUSDT")

    def disqualify(r: dict, h0: dict, sym: str) -> list[str]:
        """Phase 2f Gate 1 plan s10.3 disqualification floor.

        Vetoes apply regardless of any promotion path: expectancy
        worsens, PF worsens, |maxDD| > 1.5x |baseline|.
        """
        reasons: list[str] = []
        if r["expR"] < h0["expR"]:
            reasons.append(f"{sym}: expR worsens ({r['expR']:+.3f} vs {h0['expR']:+.3f})")
        if r["PF"] < h0["PF"] and h0["PF"] != float("inf"):
            reasons.append(f"{sym}: PF worsens ({r['PF']:.2f} vs {h0['PF']:.2f})")
        # maxdd_pct is stored as negative (pct of equity); compare absolute values.
        abs_h0 = abs(h0["maxdd_pct"])
        abs_r = abs(r["maxdd_pct"])
        if abs_h0 > 0 and abs_r > 1.5 * abs_h0:
            reasons.append(
                f"{sym}: |maxDD|>1.5x baseline "
                f"({abs_r:.2f}% vs {abs_h0:.2f}% -> ratio {abs_r / abs_h0:.3f}x)"
            )
        return reasons

    def hard_reject(r: dict, h0: dict, sym: str) -> list[str]:
        """Phase 2f Gate 1 plan s10.4 -- only fires when trade count rises."""
        if r["n"] <= h0["n"]:
            return []
        reasons: list[str] = []
        if r["expR"] < -0.50:
            reasons.append(f"{sym}: expR<-0.50 ({r['expR']:+.3f}) with rising trade count")
        if r["PF"] != float("inf") and r["PF"] < 0.30:
            reasons.append(f"{sym}: PF<0.30 ({r['PF']:.2f}) with rising trade count")
        return reasons

    def promote(r: dict, h0: dict) -> list[str]:
        dexp = r["expR"] - h0["expR"]
        dpf = (
            (r["PF"] - h0["PF"]) if (h0["PF"] != float("inf") and r["PF"] != float("inf")) else 0.0
        )
        dn_pct = (r["n"] - h0["n"]) / max(h0["n"], 1)
        # maxdd "not worse by > 1.0 pp" -- compare absolute values.
        abs_h0 = abs(h0["maxdd_pct"])
        abs_r = abs(r["maxdd_pct"])
        d_abs_dd = abs_r - abs_h0
        reasons: list[str] = []
        if dexp >= 0.10 and dpf >= 0.05:
            reasons.append(f"s10.3.a (d_exp={dexp:+.3f}, d_PF={dpf:+.2f})")
        if dexp >= 0 and dn_pct >= 0.50 and d_abs_dd <= 1.0:
            reasons.append(
                f"s10.3.b (d_exp={dexp:+.3f}, d_n={dn_pct * 100:+.1f}%, d_|dd|={d_abs_dd:+.2f}pp)"
            )
        return reasons

    # Stage 1 -- s10.3 disqualification floor + s10.4 hard reject (per-symbol).
    dq_btc = disqualify(r_btc, h0_btc, "BTC")
    dq_eth = disqualify(r_eth, h0_eth, "ETH")
    hr_btc = hard_reject(r_btc, h0_btc, "BTC")
    hr_eth = hard_reject(r_eth, h0_eth, "ETH")

    # Per s11.4 ETH-as-comparison: BTC failures decide; ETH must not catastrophically fail.
    if dq_btc or hr_btc:
        why = "; ".join(dq_btc + hr_btc)
        return ("DISQUALIFY", f"BTC: {why}")
    if hr_eth:
        return (
            "REJECT-ETH-CATASTROPHIC",
            f"ETH catastrophic per s10.4: {'; '.join(hr_eth)}",
        )

    # Stage 2 -- promotion, per s11.4 BTC must clear, ETH must not be disqualified.
    btc_prom = promote(r_btc, h0_btc)
    eth_prom = promote(r_eth, h0_eth)
    if btc_prom and not dq_eth:
        msg = "BTC passes: " + ", ".join(btc_prom)
        if eth_prom:
            msg += "; ETH also passes: " + ", ".join(eth_prom)
        else:
            msg += "; ETH passes s10.3/s10.4 floors (no catastrophic failure)"
        return ("PROMOTE", msg)
    if btc_prom and dq_eth:
        return (
            "PROMOTE-WITH-ETH-CAVEAT",
            (
                f"BTC passes {btc_prom}; ETH disqualified ({'; '.join(dq_eth)}) "
                "-- s11.4 requires ETH not catastrophic. Operator review."
            ),
        )
    if eth_prom and not btc_prom:
        return (
            "ETH-ONLY-NOTE",
            (
                f"ETH passes {eth_prom} but BTC does not clear s10.3 "
                "(s11.4: ETH-only does not qualify on BTC)"
            ),
        )
    return (
        "HOLD",
        "No s10.3 pathway met; no s10.4 trigger; baseline-equivalent or worse on BTC",
    )


def main() -> int:
    runs = {v: load_run(v, "r") for v in VARIANTS}

    print("R-WINDOW HEADLINE (2022-01-01 -> 2025-01-01, 36 months)")
    hdr = (
        f"{'var':6} {'sym':8} {'trades':>6} {'WR%':>6} {'expR':>7} {'PF':>6} "
        f"{'netPct':>7} {'maxDD%':>7} {'L/S':>6}"
    )
    print(hdr)
    print("-" * 80)
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            r = row(runs, v, sym)
            print(
                f"{v:6} {sym:8} {r['n']:>6} {r['wr'] * 100:>5.2f}% "
                f"{r['expR']:>+7.3f} {r['PF']:>6.2f} {r['net'] / 10000 * 100:>+6.2f}% "
                f"{r['maxdd_pct']:>6.2f}% {r['longs']}/{r['shorts']}"
            )
        print()

    print("=" * 80)
    print("Deltas vs H0 (R window)")
    print("=" * 80)
    for sym in ("BTCUSDT", "ETHUSDT"):
        h0 = row(runs, "H0", sym)
        print(
            f"\n  {sym} H0: n={h0['n']}  expR={h0['expR']:+.3f}  "
            f"PF={h0['PF']:.2f}  netPct={h0['net'] / 10000 * 100:+.2f}%  "
            f"maxDD={h0['maxdd_pct']:.2f}%"
        )
        for v in ["H-A1", "H-B2", "H-C1", "H-D3"]:
            r = row(runs, v, sym)
            dexp = r["expR"] - h0["expR"]
            dpf = (
                (r["PF"] - h0["PF"])
                if (h0["PF"] != float("inf") and r["PF"] != float("inf"))
                else 0.0
            )
            dn_pct = (r["n"] - h0["n"]) / max(h0["n"], 1) * 100
            ddd = r["maxdd_pct"] - h0["maxdd_pct"]
            dd_ratio = r["maxdd_pct"] / h0["maxdd_pct"] if h0["maxdd_pct"] > 0 else float("inf")
            print(
                f"    {v:5}: n={r['n']:>3} (d={dn_pct:+6.1f}%)  "
                f"expR={r['expR']:+.3f} (d={dexp:+.3f})  "
                f"PF={r['PF']:.2f} (d={dpf:+.2f})  "
                f"maxDD={r['maxdd_pct']:.2f}% (d={ddd:+.2f}pp, ratio={dd_ratio:.2f}x)"
            )

    print("\n" + "=" * 80)
    print("Per-fold R analysis -- Phase 2f s11.2 approved scheme")
    print("Five rolling folds, 12m train / 6m test, stepping 6m, all tests in R")
    print("=" * 80)

    # Phase 2f s11.2 approved scheme. Test windows step 6m starting at month 6
    # so all 5 fold tests fit inside R (2022-01..2025-01). Fold 1's notional
    # train is the first 6 months of R (a 6m partial-train front edge — the
    # only arrangement that places exactly 5 stepping-6m tests entirely
    # within R). No tuning happens in 2g, so train windows are notional.
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
    for test_lbl, train_lbl, _, _ in rolling_folds:
        print(f"  {test_lbl}  ({train_lbl})")
    print()
    print(
        f"{'var':6} {'sym':8} "
        + " ".join(f"{lbl.split()[0]:>5}" for lbl, _, _, _ in rolling_folds)
        + "  metric"
    )
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[v]["symbols"][sym]["trades"]
            n_vals = [fold_stats(tl, s, e)["n"] for _, _, s, e in rolling_folds]
            exp_vals = [fold_stats(tl, s, e)["expR"] for _, _, s, e in rolling_folds]
            print(f"{v:6} {sym:8} " + " ".join(f"{x:>5d}" for x in n_vals) + "  n_trades")
            print(f"{v:6} {sym:8} " + " ".join(f"{x:>+5.2f}" for x in exp_vals) + "  expR")
        print()

    print("=" * 80)
    print("Supplemental appendix: 6 non-overlapping 6-month half-year folds")
    print("(NOT the approved Phase 2f scheme; descriptive coverage of all 36 R months)")
    print("=" * 80)
    half_year_folds: list[tuple[str, int, int]] = []
    for i, label in enumerate(["2022H1", "2022H2", "2023H1", "2023H2", "2024H1", "2024H2"]):
        start_y = 2022 + i // 2
        start_m = 1 if i % 2 == 0 else 7
        end_y = start_y if (i % 2 == 0) else start_y + 1
        end_m = 7 if (i % 2 == 0) else 1
        start_dt = datetime(start_y, start_m, 1, tzinfo=UTC)
        end_dt = datetime(end_y, end_m, 1, tzinfo=UTC)
        half_year_folds.append(
            (label, int(start_dt.timestamp() * 1000), int(end_dt.timestamp() * 1000))
        )

    print(
        f"\n{'var':6} {'sym':8} "
        + " ".join(f"{lbl:>8}" for lbl, _, _ in half_year_folds)
        + "  metric"
    )
    for v in VARIANTS:
        for sym in ("BTCUSDT", "ETHUSDT"):
            tl = runs[v]["symbols"][sym]["trades"]
            n_vals = [fold_stats(tl, s, e)["n"] for _, s, e in half_year_folds]
            exp_vals = [fold_stats(tl, s, e)["expR"] for _, s, e in half_year_folds]
            print(f"{v:6} {sym:8} " + " ".join(f"{x:>8d}" for x in n_vals) + "  n_trades")
            print(f"{v:6} {sym:8} " + " ".join(f"{x:>+8.3f}" for x in exp_vals) + "  expR")
        print()

    print("=" * 80)
    print("s10.3 promote / s10.4 reject classification (pre-declared thresholds)")
    print("=" * 80)
    for v in ["H-A1", "H-B2", "H-C1", "H-D3"]:
        status, reason = classify(runs, v)
        print(f"  {v:5} -> {status}")
        print(f"         {reason}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
