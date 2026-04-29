"""Phase 3j D1-A analysis script.

Reads the trade logs from the four mandatory D1-A R-window runs plus
the H0 / R3 / F1 control runs, computes the Phase 3h §11 first-execution-
gate evaluation, the Phase 3h §12 M1 / M2 / M3 mechanism checks, and
the Phase 3h §13 / §14 mandatory diagnostics + P.14 hard-block
invariants subset that does not require running additional backtests,
and writes a single JSON analysis output.

The script consumes only existing per-run artifacts (under
``data/derived/backtests/``) plus the v002 normalized klines (for the
M1 post-entry counter-displacement, M2 1h-vol regime classifier, and
the M2 funding-benefit aggregation).

Output: ``data/derived/backtests/phase-3j-d1a-analysis-<run_id>.json``
(git-ignored).
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

import pyarrow.parquet as pq

from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.storage import read_klines

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"


def _latest_run_dir(experiment_name: str) -> Path:
    base = DATA_ROOT / "derived" / "backtests" / experiment_name
    candidates = sorted(base.glob("*Z"))
    if not candidates:
        raise RuntimeError(f"no runs under {base}")
    return candidates[-1]


def _load_trades(run_dir: Path, symbol: Symbol) -> list[dict]:
    table = pq.read_table(run_dir / symbol.value / "trade_log.parquet")
    return table.to_pylist()


def _load_summary(run_dir: Path, symbol: Symbol) -> dict:
    return json.loads((run_dir / symbol.value / "summary_metrics.json").read_text())


def _load_lifecycle_d1a(run_dir: Path, symbol: Symbol) -> dict:
    f = run_dir / symbol.value / "funding_aware_lifecycle_total.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text())


def _build_open_time_index(klines: list) -> dict[int, int]:  # type: ignore[type-arg]
    return {b.open_time: i for i, b in enumerate(klines)}


def _m1_counter_displacements(
    trades: list[dict], klines_15m: list, horizons: tuple[int, ...] = (8, 16, 32)
) -> dict[str, dict[int, dict[str, float]]]:  # type: ignore[type-arg]
    """Per-trade post-entry counter-displacement at the requested horizons.

    Per Phase 3h §10.1 timing-clarification amendment, the formula uses
    ``fill_price`` (the actual next-bar-open fill price), NOT
    ``close(B+1)``:

        counter_displacement_h_R =
            ((close(entry_bar + h) - fill_price) * trade_direction_sign)
            / stop_distance

    where trade_direction_sign = +1 for LONG, -1 for SHORT (positive
    means the price moved in the trade's profit direction).

    Returns ``{"counter_h_R": {h: {"mean": ..., "fraction_non_neg": ...,
    "n": ...}}}``. ``n`` may shrink at large horizons when the fill
    bar is too close to end-of-data to reach ``h`` future bars.
    """
    open_index = _build_open_time_index(klines_15m)
    closes = [float(b.close) for b in klines_15m]

    per_horizon: dict[int, list[float]] = {h: [] for h in horizons}
    for t in trades:
        fill_open_time = int(t["entry_fill_time_ms"])
        if fill_open_time not in open_index:
            continue
        fill_idx = open_index[fill_open_time]
        direction_sign = +1 if t["direction"] == "LONG" else -1
        sd = float(t["stop_distance"])
        if sd <= 0:
            continue
        fill_price = float(t["entry_fill_price"])  # actual next-bar-open fill price
        for h in horizons:
            if fill_idx + h >= len(closes):
                continue
            cd = (closes[fill_idx + h] - fill_price) * direction_sign
            per_horizon[h].append(cd / sd)

    out: dict[int, dict[str, float]] = {}
    for h, vals in per_horizon.items():
        if not vals:
            out[h] = {"mean": 0.0, "fraction_non_neg": 0.0, "n": 0}
            continue
        out[h] = {
            "mean": sum(vals) / len(vals),
            "fraction_non_neg": sum(1 for v in vals if v >= 0) / len(vals),
            "n": len(vals),
        }
    return {"counter_h_R": out}


def _m2_funding_benefit(trades: list[dict]) -> dict[str, float | int]:
    """M2 — Funding-cost benefit. Per Phase 3h §12.2:

        funding_benefit_R = funding_pnl / realized_risk_usdt
        PASS if mean funding_benefit_R >= +0.05 R per trade per symbol.

    Positive when funding flows to the strategy (e.g., SHORT collects
    positive funding from longs at extreme positive funding cycles).
    """
    n = len(trades)
    if n == 0:
        return {"n": 0, "mean_funding_benefit_R": 0.0, "M2_pass_threshold_0_05": False}
    vals: list[float] = []
    for t in trades:
        risk = float(t["realized_risk_usdt"])
        if risk <= 0:
            continue
        vals.append(float(t["funding_pnl"]) / risk)
    if not vals:
        return {"n": 0, "mean_funding_benefit_R": 0.0, "M2_pass_threshold_0_05": False}
    mean_v = sum(vals) / len(vals)
    return {
        "n": len(vals),
        "mean_funding_benefit_R": mean_v,
        "M2_pass_threshold_0_05": mean_v >= 0.05,
    }


def _m3_target_subset(trades: list[dict]) -> dict[str, float | int]:
    """M3 — TARGET-exit subset positive contribution. Per Phase 3h §12.3:

    PASS if mean net_R >= +0.30 AND aggregate net_R > 0 per symbol.
    """
    sub = [t for t in trades if t["exit_reason"] == "TARGET"]
    n = len(sub)
    if n == 0:
        return {"n": 0, "aggregate_R": 0.0, "mean_R": 0.0}
    agg = sum(float(t["net_r_multiple"]) for t in sub)
    return {"n": n, "aggregate_R": agg, "mean_R": agg / n}


def _bucket_summary(trades: list[dict]) -> dict[str, float | int]:
    n = len(trades)
    if n == 0:
        return {"n": 0, "expR": 0.0, "PF": 0.0, "WR": 0.0, "stop_frac": 0.0}
    wins = [t for t in trades if t["net_pnl"] > 0]
    expR = sum(t["net_r_multiple"] for t in trades) / n
    gross_win = sum(t["net_pnl"] for t in wins)
    gross_loss = -sum(t["net_pnl"] for t in trades if t["net_pnl"] < 0)
    pf = (gross_win / gross_loss) if gross_loss > 0 else float("inf") if gross_win > 0 else 0.0
    wr = len(wins) / n
    stop_frac = sum(1 for t in trades if t["exit_reason"] == "STOP") / n
    return {"n": n, "expR": expR, "PF": pf, "WR": wr, "stop_frac": stop_frac}


def _per_fold_breakdown(trades: list[dict]) -> list[dict]:
    """6 half-year folds across the R-window."""
    fold_bounds = [
        ("F1_2022H1", 1_640_995_200_000, 1_656_633_600_000),
        ("F2_2022H2", 1_656_633_600_000, 1_672_531_200_000),
        ("F3_2023H1", 1_672_531_200_000, 1_688_169_600_000),
        ("F4_2023H2", 1_688_169_600_000, 1_704_067_200_000),
        ("F5_2024H1", 1_704_067_200_000, 1_719_792_000_000),
        ("F6_2024H2", 1_719_792_000_000, 1_735_689_600_000),
    ]
    out: list[dict] = []
    for name, start, end in fold_bounds:
        bucket = [t for t in trades if start <= int(t["exit_fill_time_ms"]) < end]
        s = _bucket_summary(bucket)
        out.append({"fold": name, **s})
    return out


def _exit_fractions_with_per_reason_R(trades: list[dict]) -> dict[str, object]:
    n = len(trades)
    if n == 0:
        return {"n": 0}
    counts: dict[str, int] = defaultdict(int)
    sum_R: dict[str, float] = defaultdict(float)
    for t in trades:
        r = str(t["exit_reason"])
        counts[r] += 1
        sum_R[r] += float(t["net_r_multiple"])
    out: dict[str, object] = {"n": n}
    for k, v in counts.items():
        out[f"count_{k}"] = v
        out[f"frac_{k}"] = v / n
        out[f"mean_R_{k}"] = sum_R[k] / v if v > 0 else 0.0
        out[f"aggregate_R_{k}"] = sum_R[k]
    out["accounting_sum"] = sum(int(c) for c in counts.values())
    out["accounting_identity"] = bool(out["accounting_sum"] == n)
    return out


def _distribution_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"n": 0, "mean": 0.0, "median": 0.0, "p25": 0.0, "p75": 0.0, "max": 0.0, "min": 0.0}
    s = sorted(values)
    n = len(s)
    return {
        "n": n,
        "mean": sum(s) / n,
        "median": s[n // 2],
        "p25": s[n // 4],
        "p75": s[(3 * n) // 4],
        "max": s[-1],
        "min": s[0],
    }


def _d1a_field_distributions(trades: list[dict]) -> dict[str, dict[str, float]]:
    return {
        "funding_z_score_at_signal": _distribution_stats(
            [float(t["funding_z_score_at_signal"]) for t in trades]
        ),
        "funding_rate_at_signal": _distribution_stats(
            [float(t["funding_rate_at_signal"]) for t in trades]
        ),
        "bars_since_funding_event_at_signal": _distribution_stats(
            [float(t["bars_since_funding_event_at_signal"]) for t in trades]
        ),
        "stop_distance_at_signal_atr": _distribution_stats(
            [float(t["stop_distance_at_signal_atr"]) for t in trades]
        ),
        "entry_to_target_distance_atr": _distribution_stats(
            [float(t["entry_to_target_distance_atr"]) for t in trades]
        ),
    }


def _p14_invariants(trades: list[dict]) -> dict[str, object]:
    """Phase 3h §14 P.14-style hard-block invariants applied to the
    actual D1-A trade log.

    The +2.0R target geometry is enforced by construction in the
    engine (``compute_d1a_target(fill_price, stop_distance=
    post_slip_stop_distance, target_r=2.0)``) and cannot be re-derived
    at the trade-log level because ``atr_at_signal`` is an R2-specific
    field that stays NaN for D1-A rows. The diagnostic field
    ``entry_to_target_distance_atr`` is reported as an informational
    descriptive band (its mean exceeds 2.0 by the post-slip stop-
    distance inflation, by design).
    """
    allowed = {"STOP", "TARGET", "TIME_STOP", "END_OF_DATA"}
    forbidden = {"TRAILING_BREACH", "STAGNATION", "TAKE_PROFIT"}
    n = len(trades)
    bad_exit = sum(1 for t in trades if t["exit_reason"] in forbidden)
    only_allowed = bad_exit == 0 and all(t["exit_reason"] in allowed for t in trades)
    band_ok = all(0.60 <= float(t["stop_distance_at_signal_atr"]) <= 1.80 for t in trades)
    sd_atr = [float(t["stop_distance_at_signal_atr"]) for t in trades]
    e2t_atr = [float(t["entry_to_target_distance_atr"]) for t in trades]
    funding_event_ids_present = all(
        t["funding_event_id_at_signal"] is not None and t["funding_event_id_at_signal"] != ""
        for t in trades
    )
    return {
        "n_trades": n,
        "no_v1_only_exit_reasons": bool(only_allowed),
        "n_trades_with_forbidden_exit_reason": bad_exit,
        "raw_stop_distance_in_band": bool(band_ok),
        "min_stop_distance_atr": min(sd_atr) if sd_atr else 0.0,
        "max_stop_distance_atr": max(sd_atr) if sd_atr else 0.0,
        "entry_to_target_atr_min": min(e2t_atr) if e2t_atr else 0.0,
        "entry_to_target_atr_max": max(e2t_atr) if e2t_atr else 0.0,
        "entry_to_target_atr_mean": sum(e2t_atr) / len(e2t_atr) if e2t_atr else 0.0,
        "funding_event_ids_populated": bool(funding_event_ids_present),
    }


# ---------------------------------------------------------------------------


def main() -> int:
    out: dict[str, object] = {}

    cells = {
        "D1A_R_MED_MARK": "phase-3j-d1a-window=r-slip=medium",
        "D1A_R_LOW_MARK": "phase-3j-d1a-window=r-slip=low",
        "D1A_R_HIGH_MARK": "phase-3j-d1a-window=r-slip=high",
        "D1A_R_MED_TRADE": "phase-3j-d1a-window=r-slip=medium-stop=trade_price",
    }
    cell_dirs: dict[str, Path] = {k: _latest_run_dir(v) for k, v in cells.items()}

    control_dirs = {
        "H0_R": _latest_run_dir("phase-2l-h0-r"),
        "H0_V": _latest_run_dir("phase-2l-h0-v"),
        "R3_R": _latest_run_dir("phase-2l-r3-r"),
        "R3_V": _latest_run_dir("phase-2l-r3-v"),
        "F1_R_MED_MARK": _latest_run_dir("phase-3d-f1-window=r-slip=medium"),
    }

    klines_root = DATA_ROOT / "normalized" / "klines"
    klines_15m: dict[Symbol, list] = {}  # type: ignore[type-arg]
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        klines_15m[s] = read_klines(klines_root, symbol=s, interval=Interval.I_15M)

    # ----- Per-cell summaries + lifecycle -----
    summaries: dict[str, dict[str, dict]] = {}
    for cell_id, run_dir in cell_dirs.items():
        summaries[cell_id] = {
            "BTCUSDT": _load_summary(run_dir, Symbol.BTCUSDT),
            "ETHUSDT": _load_summary(run_dir, Symbol.ETHUSDT),
        }
    out["cells"] = {
        cell_id: {
            "run_dir": str(run_dir),
            "summary": summaries[cell_id],
            "lifecycle": {
                "BTCUSDT": _load_lifecycle_d1a(run_dir, Symbol.BTCUSDT),
                "ETHUSDT": _load_lifecycle_d1a(run_dir, Symbol.ETHUSDT),
            },
        }
        for cell_id, run_dir in cell_dirs.items()
    }

    btc_med = summaries["D1A_R_MED_MARK"]["BTCUSDT"]
    eth_med = summaries["D1A_R_MED_MARK"]["ETHUSDT"]
    btc_high = summaries["D1A_R_HIGH_MARK"]["BTCUSDT"]
    eth_high = summaries["D1A_R_HIGH_MARK"]["ETHUSDT"]

    # ----- §11.1 first-execution gate (Phase 3h) -----
    cond_i = btc_med["expectancy_r"] > 0
    cond_iii = eth_med["expectancy_r"] > -0.50 and eth_med["profit_factor"] > 0.30
    cond_iv = (
        btc_high["expectancy_r"] > 0
        and btc_high["profit_factor"] > 0.30
        and eth_high["expectancy_r"] > -0.50
        and eth_high["profit_factor"] > 0.30
    )
    cond_v = (
        btc_med["expectancy_r"] > -0.50
        and btc_med["profit_factor"] > 0.30
        and eth_med["expectancy_r"] > -0.50
        and eth_med["profit_factor"] > 0.30
    )

    catastrophic_floor_violation = (
        btc_med["expectancy_r"] <= -0.50
        or btc_med["profit_factor"] <= 0.30
        or eth_med["expectancy_r"] <= -0.50
        or eth_med["profit_factor"] <= 0.30
        or btc_high["expectancy_r"] <= -0.50
        or btc_high["profit_factor"] <= 0.30
        or eth_high["expectancy_r"] <= -0.50
        or eth_high["profit_factor"] <= 0.30
    )

    # ----- §12.1 M1 mechanism (BTC + ETH; BTC drives §11.1(ii)) -----
    m1: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        trades = _load_trades(cell_dirs["D1A_R_MED_MARK"], s)
        m1[s.value] = _m1_counter_displacements(trades, klines_15m[s])
    btc_m1_32 = m1[Symbol.BTCUSDT.value]["counter_h_R"][32]
    cond_ii = btc_m1_32["mean"] >= 0.10 and btc_m1_32["fraction_non_neg"] >= 0.50

    # ----- §11.2 verdict mapping -----
    if catastrophic_floor_violation:
        verdict = "HARD REJECT"
    elif not cond_ii:
        verdict = "MECHANISM FAIL"
    elif cond_i and cond_ii and cond_iii and cond_iv and cond_v:
        verdict = "PROMOTE"
    elif cond_i and cond_ii and (not cond_iv) and (not catastrophic_floor_violation):
        verdict = "MECHANISM PASS / FRAMEWORK FAIL - sec.11.6 cost-sensitivity blocks"
    elif cond_ii and (not cond_i) and (not catastrophic_floor_violation):
        verdict = "MECHANISM PASS / FRAMEWORK FAIL - other"
    else:
        verdict = "PROMOTE-with-caveats or NOT PROMOTE (manual review)"

    out["first_execution_gate"] = {
        "condition_i_BTC_MED_expR_gt_0": cond_i,
        "condition_ii_M1_BTC_pass_h32": cond_ii,
        "condition_iii_ETH_MED_non_catastrophic": cond_iii,
        "condition_iv_HIGH_slippage_cost_sensitivity": cond_iv,
        "condition_v_MED_absolute_floors": cond_v,
        "catastrophic_floor_violation": catastrophic_floor_violation,
        "verdict": verdict,
    }
    out["m1_mechanism"] = m1

    # ----- §12.2 M2 funding-cost benefit -----
    m2: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        d1a_trades = _load_trades(cell_dirs["D1A_R_MED_MARK"], s)
        m2[s.value] = _m2_funding_benefit(d1a_trades)
    m2_btc_pass = bool(m2[Symbol.BTCUSDT.value].get("M2_pass_threshold_0_05", False))
    m2_eth_pass = bool(m2[Symbol.ETHUSDT.value].get("M2_pass_threshold_0_05", False))
    out["m2_mechanism"] = {
        **m2,
        "M2_pass_both_symbols": m2_btc_pass and m2_eth_pass,
        "M2_partial": (m2_btc_pass != m2_eth_pass),
    }

    # ----- §12.3 M3 target-exit subset -----
    m3: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        d1a_trades = _load_trades(cell_dirs["D1A_R_MED_MARK"], s)
        m3[s.value] = _m3_target_subset(d1a_trades)
    btc_m3 = m3[Symbol.BTCUSDT.value]
    eth_m3 = m3[Symbol.ETHUSDT.value]
    m3_pass = (
        btc_m3.get("aggregate_R", 0.0) > 0
        and eth_m3.get("aggregate_R", 0.0) > 0
        and btc_m3.get("mean_R", 0.0) >= 0.30
        and eth_m3.get("mean_R", 0.0) >= 0.30
    )
    out["m3_mechanism"] = {**m3, "M3_pass_both_symbols": m3_pass}

    # ----- §13 mandatory diagnostics subset -----
    diag: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        d1a_trades = _load_trades(cell_dirs["D1A_R_MED_MARK"], s)
        diag[s.value] = {
            "trade_count": len(d1a_trades),
            "long_count": sum(1 for t in d1a_trades if t["direction"] == "LONG"),
            "short_count": sum(1 for t in d1a_trades if t["direction"] == "SHORT"),
            "exit_fractions_per_reason_R": _exit_fractions_with_per_reason_R(d1a_trades),
            "field_distributions": _d1a_field_distributions(d1a_trades),
            "per_fold": _per_fold_breakdown(d1a_trades),
            "p14_invariants": _p14_invariants(d1a_trades),
        }
    out["diagnostics_D1A_R_MED_MARK"] = diag

    # ----- Cost sensitivity LOW / MED / HIGH cross-cell summary -----
    out["cost_sensitivity"] = {
        s.value: {
            "LOW": summaries["D1A_R_LOW_MARK"][s.value],
            "MED": summaries["D1A_R_MED_MARK"][s.value],
            "HIGH": summaries["D1A_R_HIGH_MARK"][s.value],
        }
        for s in (Symbol.BTCUSDT, Symbol.ETHUSDT)
    }

    # ----- Mark vs Trade-price stop-trigger sensitivity -----
    out["stop_trigger_sensitivity"] = {
        s.value: {
            "MARK": summaries["D1A_R_MED_MARK"][s.value],
            "TRADE_PRICE": summaries["D1A_R_MED_TRADE"][s.value],
        }
        for s in (Symbol.BTCUSDT, Symbol.ETHUSDT)
    }

    # ----- Cross-family descriptive references -----
    cross_family: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        d1a = summaries["D1A_R_MED_MARK"][s.value]
        h0 = json.loads((control_dirs["H0_R"] / s.value / "summary_metrics.json").read_text())
        r3 = json.loads((control_dirs["R3_R"] / s.value / "summary_metrics.json").read_text())
        f1 = json.loads(
            (control_dirs["F1_R_MED_MARK"] / s.value / "summary_metrics.json").read_text()
        )
        cross_family[s.value] = {
            "D1A_R_MED_MARK": d1a,
            "H0_R_MED_MARK": h0,
            "R3_R_MED_MARK": r3,
            "F1_R_MED_MARK": f1,
            "delta_D1A_minus_H0": {
                "expR": d1a["expectancy_r"] - h0["expectancy_r"],
                "PF": d1a["profit_factor"] - h0["profit_factor"],
                "trade_count_pct": (d1a["trade_count"] - h0["trade_count"])
                / max(h0["trade_count"], 1),
            },
            "delta_D1A_minus_R3": {
                "expR": d1a["expectancy_r"] - r3["expectancy_r"],
                "PF": d1a["profit_factor"] - r3["profit_factor"],
                "trade_count_pct": (d1a["trade_count"] - r3["trade_count"])
                / max(r3["trade_count"], 1),
            },
            "delta_D1A_minus_F1": {
                "expR": d1a["expectancy_r"] - f1["expectancy_r"],
                "PF": d1a["profit_factor"] - f1["profit_factor"],
                "trade_count_pct": (d1a["trade_count"] - f1["trade_count"])
                / max(f1["trade_count"], 1),
            },
        }
    out["cross_family_descriptive"] = cross_family

    # ----- RR / breakeven realized-vs-expected review (§13 #24) -----
    # Per Phase 3h §5.6.1-5.6.5 expected:
    #   At MED slip:  winner ~+1.47R; loser ~-1.53R; breakeven WR ≈ 51%
    #                 (without funding); ≈ 45% with one-cycle funding.
    #   At HIGH slip: winner ~+1.14R; loser ~-1.86R; breakeven WR ≈ 62%
    #                 (without funding); ≈ 56% with one-cycle funding.
    rr_breakeven: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        d1a_trades = _load_trades(cell_dirs["D1A_R_MED_MARK"], s)
        wins = [t for t in d1a_trades if t["net_r_multiple"] > 0]
        losses = [t for t in d1a_trades if t["net_r_multiple"] <= 0]
        n = len(d1a_trades)
        rr_breakeven[s.value] = {
            "n": n,
            "winner_count": len(wins),
            "loser_count": len(losses),
            "empirical_win_rate": len(wins) / n if n > 0 else 0.0,
            "winner_mean_R": sum(t["net_r_multiple"] for t in wins) / max(len(wins), 1),
            "loser_mean_R": sum(t["net_r_multiple"] for t in losses) / max(len(losses), 1),
            "expected_winner_R_at_MED": 1.47,
            "expected_loser_R_at_MED": -1.53,
            "expected_breakeven_WR_at_MED_no_funding": 0.51,
        }
    out["rr_breakeven_review_MED"] = rr_breakeven

    # ----- Save -----
    run_id = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    out_path = DATA_ROOT / "derived" / "backtests" / f"phase-3j-d1a-analysis-{run_id}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True, default=str))
    print(f"Analysis written to: {out_path}")
    print(f"\nVerdict: {verdict}")
    print(
        f"\nD1A R MED MARK BTC: expR={btc_med['expectancy_r']:.4f} "
        f"PF={btc_med['profit_factor']:.4f}"
    )
    print(
        f"D1A R MED MARK ETH: expR={eth_med['expectancy_r']:.4f} PF={eth_med['profit_factor']:.4f}"
    )
    print(
        f"D1A R HIGH MARK BTC: expR={btc_high['expectancy_r']:.4f} "
        f"PF={btc_high['profit_factor']:.4f}"
    )
    print(
        f"D1A R HIGH MARK ETH: expR={eth_high['expectancy_r']:.4f} "
        f"PF={eth_high['profit_factor']:.4f}"
    )
    print(
        f"M1 BTC h=32: mean={btc_m1_32['mean']:.4f} R "
        f"fraction>=0={btc_m1_32['fraction_non_neg']:.4f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
