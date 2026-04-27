"""Phase 2w R2 analysis script.

Computes P.1-P.14 diagnostics per Phase 2u §P / Phase 2v §4 from the
Phase 2w runner outputs. Reads trade-log parquet + summary_metrics.json
+ r2_lifecycle_total.json from each run directory and emits a single
JSON document with every P-prefixed diagnostic the 2w-B checkpoint
report needs.

Usage::

    uv run python scripts/_phase2w_R2_analysis.py \\
        --r2-r-dir         data/derived/.../phase-2w-r2-r2_r3-r/<run_id> \\
        --r2-r-low-dir     data/derived/.../phase-2w-r2-r2_r3-r-slip=LOW/<run_id> \\
        --r2-r-high-dir    data/derived/.../phase-2w-r2-r2_r3-r-slip=HIGH/<run_id> \\
        --r2-r-trade-dir   data/derived/.../phase-2w-r2-r2_r3-r-stop=TRADE_PRICE/<run_id> \\
        --r2-r-limit-dir   data/derived/.../phase-2w-r2-r2_r3-r-fill=limit-at-pullback/<run_id> \\
        --r2-v-dir         data/derived/.../phase-2w-r2-r2_r3-v/<run_id> \\
        --h0-r-dir         data/derived/.../phase-2s-r1b-h0-r/<run_id> \\
        --r3-r-dir         data/derived/.../phase-2s-r1b-r3-r/<run_id> \\
        --h0-v-dir         data/derived/.../phase-2s-r1b-h0-v/<run_id> \\
        --r3-v-dir         data/derived/.../phase-2s-r1b-r3-v/<run_id> \\
        --output           data/derived/backtests/phase-2w-analysis.json

The analysis is purely descriptive — no parameter tuning, no sweeps,
no comparison-baseline shifting. All thresholds preserved per Phase 2f
§§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 unchanged.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean

import pyarrow.parquet as pq

REPO_ROOT = Path(__file__).resolve().parent.parent

# §10.3 thresholds preserved per Phase 2f §11.3.5 (no post-hoc loosening).
EXP_MAGNITUDE_THRESHOLD = 0.10  # §10.3.a Δexp ≥ +0.10 R
PF_MAGNITUDE_THRESHOLD = 0.05  # §10.3.a ΔPF ≥ +0.05
MAXDD_VETO_RATIO = 1.5  # §10.3 disqualification floor
TRADE_COUNT_RISING_THRESHOLD = 0.50  # §10.3.b Δn ≥ +50%
MAXDD_BAND_DELTA_PP = 1.0  # §10.3.b Δ|maxDD| ≤ +1.0 pp
M1_DELTA_R3_BTC = 0.10  # M1 mechanism: Δexp_R3 ≥ +0.10 on BTC

# Filter constants (mirror src/.../stop.py).
FILTER_MIN_ATR_MULT = 0.60
FILTER_MAX_ATR_MULT = 1.80


# --------------------------------------------------------------------------
# I/O helpers
# --------------------------------------------------------------------------


def _load_trades(run_dir: Path, symbol: str) -> list[dict]:
    parquet_path = run_dir / symbol / "trade_log.parquet"
    table = pq.read_table(parquet_path)
    return table.to_pylist()


def _load_summary(run_dir: Path, symbol: str) -> dict:
    return json.loads((run_dir / symbol / "summary_metrics.json").read_text())


def _load_r2_lifecycle(run_dir: Path, symbol: str) -> dict | None:
    path = run_dir / symbol / "r2_lifecycle_total.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


# --------------------------------------------------------------------------
# Headline metrics
# --------------------------------------------------------------------------


def _headline(summary: dict) -> dict:
    return {
        "trades": summary["trade_count"],
        "wr": summary["win_rate"],
        "expR": summary["expectancy_r"],
        "PF": summary["profit_factor"],
        "netPct": summary["total_return_fraction"],
        "maxDD": summary["max_drawdown_fraction"],
        "long_count": summary["long_count"],
        "short_count": summary["short_count"],
        "stop_exits": summary["stop_exits"],
        "trailing_exits": summary["trailing_exits"],
        "stagnation_exits": summary["stagnation_exits"],
        "take_profit_exits": summary["take_profit_exits"],
        "time_stop_exits": summary["time_stop_exits"],
        "end_of_data_exits": summary["end_of_data_exits"],
        "gap_through_stops": summary["gap_through_stops"],
    }


def _delta_vs(candidate: dict, baseline: dict) -> dict:
    """Compute deltas vs baseline.

    ``delta_maxDD_pp`` uses ``|maxDD|`` (magnitudes) per Phase 2v
    §5.1.4 convention (``Δ|maxDD| ≤ 0`` means "drawdown not worse").
    Raw ``maxDD`` values are negative; subtracting them directly
    would invert the sign of the comparison.
    """
    return {
        "delta_expR": candidate["expR"] - baseline["expR"],
        "delta_PF": candidate["PF"] - baseline["PF"],
        "delta_n_pct": (
            (candidate["trades"] - baseline["trades"]) / baseline["trades"]
            if baseline["trades"] > 0
            else 0.0
        ),
        # Δ|maxDD| in percentage points: positive = drawdown got worse.
        "delta_maxDD_pp": (abs(candidate["maxDD"]) - abs(baseline["maxDD"])) * 100.0,
        "maxDD_ratio": (
            abs(candidate["maxDD"]) / abs(baseline["maxDD"])
            if baseline["maxDD"] != 0
            else float("inf")
        ),
    }


def _section_10_3_verdict(deltas: dict) -> dict:
    """Apply Phase 2f §10.3 thresholds without modification."""
    de = deltas["delta_expR"]
    dp = deltas["delta_PF"]
    dn = deltas["delta_n_pct"]
    ddd = deltas["delta_maxDD_pp"]
    dd_ratio = deltas["maxDD_ratio"]

    # Disqualification floor: any of (worse expR, worse PF, |maxDD| > 1.5×)
    disqualified = (de < 0) or (dp < 0) or (dd_ratio > MAXDD_VETO_RATIO)

    # §10.3.a magnitude path: Δexp ≥ +0.10 AND ΔPF ≥ +0.05
    cleared_10_3_a = (de >= EXP_MAGNITUDE_THRESHOLD) and (dp >= PF_MAGNITUDE_THRESHOLD)

    # §10.3.b rising-trade-count: Δexp ≥ 0 AND Δn ≥ +50% AND Δ|maxDD| ≤ +1.0 pp
    # (Mechanically inapplicable for R2 since Δn < 0; reported as False.)
    cleared_10_3_b = (
        (de >= 0) and (dn >= TRADE_COUNT_RISING_THRESHOLD) and (ddd <= MAXDD_BAND_DELTA_PP)
    )

    # §10.3.c strict dominance: Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0
    cleared_10_3_c = (de > 0) and (dp > 0) and (ddd <= 0)

    promotes = (not disqualified) and (cleared_10_3_a or cleared_10_3_b or cleared_10_3_c)

    return {
        "disqualified_floor": disqualified,
        "cleared_10_3_a": cleared_10_3_a,
        "cleared_10_3_b": cleared_10_3_b,
        "cleared_10_3_c": cleared_10_3_c,
        "promotes": promotes,
    }


# --------------------------------------------------------------------------
# §P diagnostics
# --------------------------------------------------------------------------


def _diagnostic_p1_fill_rate(r2_lifecycle: dict) -> dict:
    """§P.1 Fill rate + cancellation decomposition."""
    return {
        "registered_candidates": r2_lifecycle["registered_candidates"],
        "expired_no_pullback": r2_lifecycle["expired_candidates_no_pullback"],
        "expired_bias_flip": r2_lifecycle["expired_candidates_bias_flip"],
        "expired_opposite_signal": r2_lifecycle["expired_candidates_opposite_signal"],
        "expired_structural_invalidation": (
            r2_lifecycle["expired_candidates_structural_invalidation"]
        ),
        "expired_stop_distance_at_fill": (r2_lifecycle["expired_candidates_stop_distance_at_fill"]),
        "trades_filled_R2": r2_lifecycle["trades_filled_R2"],
        "fill_rate": r2_lifecycle["fill_rate"],
        "accounting_identity_holds": r2_lifecycle["accounting_identity_holds"],
    }


def _diagnostic_p2_p11_time_to_fill(r2_trades: list[dict]) -> dict:
    """§P.2 / §P.11 pullback-touch / time-to-fill distribution."""
    if not r2_trades:
        return {"count": 0, "histogram": {}, "mean": None, "median": None}
    times = sorted(t["time_to_fill_bars"] for t in r2_trades)
    hist: dict[int, int] = {}
    for t in times:
        hist[t] = hist.get(t, 0) + 1
    n = len(times)
    median = times[n // 2] if n % 2 == 1 else (times[n // 2 - 1] + times[n // 2]) / 2
    return {
        "count": n,
        "histogram": {str(k): hist[k] for k in sorted(hist)},
        "mean": mean(times),
        "median": median,
        "min": times[0],
        "max": times[-1],
    }


def _diagnostic_p3_stop_distance_reduction(r2_trades: list[dict], r3_trades: list[dict]) -> dict:
    """§P.3 stop-distance reduction.

    For each R2 trade, compute |R2_fill - structural_stop| and compare
    against the structural reference stop_distance from R3 on the SAME
    signal (matched by signal_bar_open_time_ms). Returns the ratio
    distribution.
    """
    r3_by_sig = {t["signal_bar_open_time_ms"]: t for t in r3_trades}
    ratios: list[float] = []
    matched = 0
    for rt in r2_trades:
        sig = rt["signal_bar_open_time_ms"]
        r3t = r3_by_sig.get(sig)
        if r3t is None:
            continue
        r3_dist = r3t["stop_distance"]
        r2_dist = rt["stop_distance"]
        if r3_dist > 0:
            ratios.append(r2_dist / r3_dist)
            matched += 1
    if not ratios:
        return {"matched": 0}
    ratios_sorted = sorted(ratios)
    return {
        "matched": matched,
        "mean_ratio": mean(ratios),
        "median_ratio": ratios_sorted[len(ratios_sorted) // 2],
        "min_ratio": ratios_sorted[0],
        "max_ratio": ratios_sorted[-1],
        "ratio_lt_1_count": sum(1 for r in ratios if r < 1.0),
        "ratio_eq_1_count": sum(1 for r in ratios if r == 1.0),
        "ratio_gt_1_count": sum(1 for r in ratios if r > 1.0),
    }


def _diagnostic_p4_stop_exit_fraction(h0_summary: dict, r3_summary: dict, r2_summary: dict) -> dict:
    """§P.4 stop-exit fraction comparison."""

    def _fraction(s: dict) -> float:
        total_exits = (
            s["stop_exits"]
            + s["take_profit_exits"]
            + s["time_stop_exits"]
            + s["end_of_data_exits"]
            + s["trailing_exits"]
            + s["stagnation_exits"]
        )
        return s["stop_exits"] / total_exits if total_exits > 0 else 0.0

    return {
        "h0_stop_exit_fraction": _fraction(h0_summary),
        "r3_stop_exit_fraction": _fraction(r3_summary),
        "r2_stop_exit_fraction": _fraction(r2_summary),
        "r2_minus_r3": _fraction(r2_summary) - _fraction(r3_summary),
        "m2_passed": _fraction(r2_summary) < _fraction(r3_summary),
    }


def _diagnostic_p5_intersection_trade(r2_trades: list[dict], r3_trades: list[dict]) -> dict:
    """§P.5 intersection-trade comparison vs R3 — strongest mechanism cut.

    The intersection set is signals that BOTH R3 and R2+R3 entered.
    For each such signal, compute Δexp_per_trade = R2_R - R3_R, then
    aggregate per-direction.
    """
    r3_by_sig = {t["signal_bar_open_time_ms"]: t for t in r3_trades}
    intersection: list[dict] = []
    for rt in r2_trades:
        sig = rt["signal_bar_open_time_ms"]
        r3t = r3_by_sig.get(sig)
        if r3t is None:
            continue
        intersection.append(
            {
                "signal_bar_open_time_ms": sig,
                "direction": rt["direction"],
                "r2_R": rt["net_r_multiple"],
                "r3_R": r3t["net_r_multiple"],
                "delta_R": rt["net_r_multiple"] - r3t["net_r_multiple"],
            }
        )
    if not intersection:
        return {"matched": 0}
    deltas = [i["delta_R"] for i in intersection]
    long_deltas = [i["delta_R"] for i in intersection if i["direction"] == "LONG"]
    short_deltas = [i["delta_R"] for i in intersection if i["direction"] == "SHORT"]
    return {
        "matched": len(intersection),
        "mean_delta_R": mean(deltas),
        "long_count": len(long_deltas),
        "long_mean_delta_R": mean(long_deltas) if long_deltas else 0.0,
        "short_count": len(short_deltas),
        "short_mean_delta_R": mean(short_deltas) if short_deltas else 0.0,
        "m1_passed_btc_threshold": mean(deltas) >= M1_DELTA_R3_BTC,  # caller decides per-symbol
    }


def _diagnostic_p7_long_short_asymmetry(
    h0_summary: dict, r3_summary: dict, r2_summary: dict, r2_trades: list[dict]
) -> dict:
    """§P.7 long/short asymmetry."""

    def _by_dir(trades: list[dict]) -> dict:
        long_trades = [t for t in trades if t["direction"] == "LONG"]
        short_trades = [t for t in trades if t["direction"] == "SHORT"]

        def _stats(tt: list[dict]) -> dict:
            if not tt:
                return {"count": 0}
            rs = [t["net_r_multiple"] for t in tt]
            wins = sum(1 for r in rs if r > 0)
            gains = sum(r for r in rs if r > 0)
            losses = sum(-r for r in rs if r < 0)
            return {
                "count": len(rs),
                "expR": mean(rs),
                "wr": wins / len(rs),
                "PF": (gains / losses) if losses > 0 else float("inf"),
            }

        return {"long": _stats(long_trades), "short": _stats(short_trades)}

    return {
        "r2_by_direction": _by_dir(r2_trades),
        # H0 / R3 by-direction is summary-level only; we keep the
        # variant-level aggregates and report per-direction from trades
        # if available downstream. For 2w-B, R2's directional split is
        # the most material; H0/R3 splits are reported separately.
        "h0_long_count": h0_summary["long_count"],
        "h0_short_count": h0_summary["short_count"],
        "r3_long_count": r3_summary["long_count"],
        "r3_short_count": r3_summary["short_count"],
        "r2_long_count": r2_summary["long_count"],
        "r2_short_count": r2_summary["short_count"],
    }


def _diagnostic_p10_r_distance_distribution(r2_trades: list[dict], r3_trades: list[dict]) -> dict:
    """§P.10 R-distance distribution (normalized stop-distance)."""

    def _stats(trades: list[dict], use_r2_meta: bool) -> dict:
        ds: list[float] = []
        for t in trades:
            if use_r2_meta:
                d = t.get("r_distance", float("nan"))
                if d != d:  # NaN
                    continue
                ds.append(d)
            else:
                # R3 path: r_distance = stop_distance / atr_at_signal
                # but atr_at_signal is NaN for non-R2 records. Use the
                # H0 convention: stop_distance / ATR computed at signal
                # bar's close. Approximate as stop_distance for now;
                # the ratio is what matters and R2's r_distance is the
                # comparison anchor.
                ds.append(t["stop_distance"])
        if not ds:
            return {"count": 0}
        ds_sorted = sorted(ds)
        n = len(ds_sorted)
        return {
            "count": n,
            "mean": mean(ds_sorted),
            "median": ds_sorted[n // 2],
            "min": ds_sorted[0],
            "max": ds_sorted[-1],
        }

    return {
        "r2_r_distance_atr_normalized": _stats(r2_trades, use_r2_meta=True),
        "r3_stop_distance_raw": _stats(r3_trades, use_r2_meta=False),
        "r2_stop_distance_raw": _stats(r2_trades, use_r2_meta=False),
    }


def _diagnostic_p12_mfe_mae_at_fill(r2_trades: list[dict], r3_trades: list[dict]) -> dict:
    """§P.12 MFE/MAE distribution at fill."""

    def _stats(trades: list[dict]) -> dict:
        if not trades:
            return {"count": 0}
        mfes = [t["mfe_r"] for t in trades]
        maes = [t["mae_r"] for t in trades]
        return {
            "count": len(trades),
            "mfe_mean": mean(mfes),
            "mfe_max": max(mfes),
            "mae_mean": mean(maes),
            "mae_min": min(maes),
        }

    return {"r2": _stats(r2_trades), "r3": _stats(r3_trades)}


def _diagnostic_p13_stop_trigger_sensitivity(
    r2_default_summary: dict, r2_trade_price_summary: dict
) -> dict:
    """§P.13 mark-price vs trade-price stop-trigger sensitivity (GAP-032)."""
    return {
        "default_mark_price": _headline(r2_default_summary),
        "sensitivity_trade_price": _headline(r2_trade_price_summary),
        "delta_expR": (r2_trade_price_summary["expectancy_r"] - r2_default_summary["expectancy_r"]),
        "delta_PF": (r2_trade_price_summary["profit_factor"] - r2_default_summary["profit_factor"]),
        "delta_trades": r2_trade_price_summary["trade_count"] - r2_default_summary["trade_count"],
        "gap_through_default": r2_default_summary["gap_through_stops"],
        "gap_through_trade_price": r2_trade_price_summary["gap_through_stops"],
    }


def _diagnostic_p6_fill_model_sensitivity(r2_default_summary: dict, r2_limit_summary: dict) -> dict:
    """§P.6 fill-model sensitivity (committed vs limit-at-pullback diagnostic)."""
    return {
        "committed_next_bar_open": _headline(r2_default_summary),
        "diagnostic_limit_at_pullback_intrabar": _headline(r2_limit_summary),
        "delta_expR": (r2_limit_summary["expectancy_r"] - r2_default_summary["expectancy_r"]),
        "delta_PF": (r2_limit_summary["profit_factor"] - r2_default_summary["profit_factor"]),
        "delta_trades": r2_limit_summary["trade_count"] - r2_default_summary["trade_count"],
        "delta_maxDD_pp": (
            r2_limit_summary["max_drawdown_fraction"] - r2_default_summary["max_drawdown_fraction"]
        )
        * 100.0,
        "small_divergence": (
            abs(r2_limit_summary["expectancy_r"] - r2_default_summary["expectancy_r"]) < 0.05
        ),
        "diagnostic_only_governing_stays_default": True,
    }


def _diagnostic_p11_6_slippage_sensitivity(
    r2_default_summary: dict,
    r2_low_summary: dict,
    r2_high_summary: dict,
    h0_summary: dict,
) -> dict:
    """§11.6 cost-sensitivity (LOW / MED / HIGH slippage)."""
    h0_med = _headline(h0_summary)

    def _row(s: dict) -> dict:
        h = _headline(s)
        d = _delta_vs(h, h0_med)
        return {
            "headline": h,
            "delta_vs_h0_med": d,
            "section_10_3_verdict_vs_h0": _section_10_3_verdict(d),
        }

    return {
        "low": _row(r2_low_summary),
        "medium_committed": _row(r2_default_summary),
        "high": _row(r2_high_summary),
        "high_clears_section_11_6": (
            not _row(r2_high_summary)["section_10_3_verdict_vs_h0"]["disqualified_floor"]
        ),
    }


def _diagnostic_p14_implementation_bug_checks(
    r2_summary: dict, r2_trades: list[dict], r2_lifecycle: dict, slippage_bps: float
) -> dict:
    """§P.14 implementation-bug checks.

    The r_distance band check verifies that ``|raw_fill_price -
    structural_stop_level| / atr_at_signal`` is in ``[0.60, 1.80]``
    per Phase 2u §E.3. The TradeRecord stores ``fill_price`` as
    the slip-adjusted recorded price, so post-slip r_distance can
    legitimately exceed the band by a slippage-induced amount.
    To verify the engine's band check fired correctly, we de-slip
    the stored fill_price (using the run's slippage_bps) before
    band-checking — matching what ``evaluate_fill_at_next_bar_open``
    actually checks at fill time.
    """
    # 1. Zero TRAILING_BREACH / STAGNATION exits on R2+R3.
    no_trailing_or_stagnation = (
        r2_summary["trailing_exits"] == 0 and r2_summary["stagnation_exits"] == 0
    )

    # 2. Protective stop equals frozen structural_stop_level (per-trade).
    protective_stop_at_frozen_level = all(
        t["initial_stop"] == t["structural_stop_level_at_registration"]
        for t in r2_trades
        if not math.isnan(t["structural_stop_level_at_registration"])
    )

    # 3. Accounting identity (already checked by lifecycle counters).
    accounting_identity_holds = r2_lifecycle["accounting_identity_holds"]

    # 4. time_to_fill_bars in valid range [0, 7] (8 bars from B+1 to B+8 minus 1).
    time_to_fill_bars_valid = all(0 <= t["time_to_fill_bars"] <= 7 for t in r2_trades)

    # 5. Raw r_distance (de-slipped) in [0.60, 1.80] for every filled R2 trade.
    # This mirrors the engine's evaluate_fill_at_next_bar_open band check
    # which operates on next_bar.open (raw, no slippage). The TradeRecord
    # stores post-slip fill_price; we de-slip here to match the engine's
    # band reference per Phase 2u §E.3.
    slip_mult = slippage_bps / 10_000.0
    r_distance_valid_raw = True
    over_band_raw_count = 0
    over_band_post_slip_count = 0
    for t in r2_trades:
        if math.isnan(t["fill_price"]) or t["atr_at_signal"] <= 0:
            continue
        # De-slip: LONG entries get marked up; SHORT entries get marked down.
        if t["direction"] == "LONG":
            raw_fill = t["fill_price"] / (1.0 + slip_mult)
        else:
            raw_fill = t["fill_price"] / (1.0 - slip_mult)
        raw_dist = abs(raw_fill - t["structural_stop_level_at_registration"])
        raw_r_distance = raw_dist / t["atr_at_signal"]
        if not (FILTER_MIN_ATR_MULT <= raw_r_distance <= FILTER_MAX_ATR_MULT):
            r_distance_valid_raw = False
            over_band_raw_count += 1
        if not (FILTER_MIN_ATR_MULT <= t["r_distance"] <= FILTER_MAX_ATR_MULT):
            over_band_post_slip_count += 1

    return {
        "no_trailing_breach_or_stagnation_on_r2_r3": no_trailing_or_stagnation,
        "protective_stop_equals_frozen_structural_stop_level": protective_stop_at_frozen_level,
        "r2_lifecycle_accounting_identity_holds": accounting_identity_holds,
        "time_to_fill_bars_in_valid_range": time_to_fill_bars_valid,
        "r_distance_in_filter_band_for_every_filled_trade": r_distance_valid_raw,
        "post_slip_over_band_count": over_band_post_slip_count,
        "raw_over_band_count": over_band_raw_count,
        "slippage_bps_assumed": slippage_bps,
        "note": (
            "Band check uses raw next_bar.open per Phase 2u §E.3. Stored "
            "fill_price is post-slip; de-slipped to match engine's band "
            "reference. post_slip_over_band_count reflects slip-induced "
            "exceedance, not engine bug; raw_over_band_count is the "
            "implementation-bug signal."
        ),
        "all_passed": (
            no_trailing_or_stagnation
            and protective_stop_at_frozen_level
            and accounting_identity_holds
            and time_to_fill_bars_valid
            and r_distance_valid_raw
        ),
    }


def _diagnostic_m3_mechanical_r_distance(r2_trades: list[dict], r3_trades: list[dict]) -> dict:
    """M3 mechanical check: R2 mean R-distance < R3 mean R-distance.

    Mechanically guaranteed if implementation is correct (R2 fills at
    pullback level, which is closer to structural_stop than R3's
    next-bar-open price). Failure indicates an implementation bug.
    """
    r2_dists = [t["r_distance"] for t in r2_trades if not math.isnan(t["r_distance"])]
    # For R3, compute r_distance using stop_distance / a synthetic
    # reference ATR. Since R3 trade records don't carry atr_at_signal,
    # we compare raw stop_distance (in price units). The mechanical
    # R-distance reduction requirement is that R2's stop_distance is
    # smaller in magnitude than R3's on matched signals.
    r3_by_sig = {t["signal_bar_open_time_ms"]: t for t in r3_trades}
    r2_dists_matched: list[float] = []
    r3_dists_matched: list[float] = []
    for rt in r2_trades:
        sig = rt["signal_bar_open_time_ms"]
        r3t = r3_by_sig.get(sig)
        if r3t is not None:
            r2_dists_matched.append(rt["stop_distance"])
            r3_dists_matched.append(r3t["stop_distance"])
    return {
        "r2_mean_r_distance_atr_normalized": mean(r2_dists) if r2_dists else None,
        "r2_mean_stop_distance_matched": (mean(r2_dists_matched) if r2_dists_matched else None),
        "r3_mean_stop_distance_matched": (mean(r3_dists_matched) if r3_dists_matched else None),
        "matched_pairs": len(r2_dists_matched),
        "m3_passed": (
            len(r2_dists_matched) > 0 and mean(r2_dists_matched) < mean(r3_dists_matched)
        ),
    }


# --------------------------------------------------------------------------
# Per-fold consistency (GAP-036)
# --------------------------------------------------------------------------

# 5 rolling folds per GAP-20260424-036 within R-window. Boundaries match
# Phase 2s precedent (calendar half-years 2022H2/2023H1/2023H2/2024H1/2024H2).
FOLD_BOUNDARIES_MS = [
    (1_640_995_200_000, 1_656_633_600_000),  # F1: 2022-01-01 → 2022-07-01 (partial-train)
    (1_656_633_600_000, 1_672_531_200_000),  # F2: 2022-07-01 → 2023-01-01
    (1_672_531_200_000, 1_688_169_600_000),  # F3: 2023-01-01 → 2023-07-01
    (1_688_169_600_000, 1_704_067_200_000),  # F4: 2023-07-01 → 2024-01-01
    (1_704_067_200_000, 1_719_792_000_000),  # F5: 2024-01-01 → 2024-07-01
]


def _fold_summary(trades: list[dict], start_ms: int, end_ms: int) -> dict:
    fold_trades = [t for t in trades if start_ms <= t["entry_fill_time_ms"] < end_ms]
    if not fold_trades:
        return {"count": 0, "expR": 0.0}
    rs = [t["net_r_multiple"] for t in fold_trades]
    return {"count": len(rs), "expR": mean(rs)}


def _diagnostic_p8_per_fold_consistency(
    r2_trades_btc: list[dict],
    r3_trades_btc: list[dict],
    h0_trades_btc: list[dict],
    r2_trades_eth: list[dict],
    r3_trades_eth: list[dict],
    h0_trades_eth: list[dict],
) -> dict:
    """§P.8 per-fold consistency (5 rolling folds per GAP-036)."""
    folds_btc: list[dict] = []
    folds_eth: list[dict] = []
    for i, (start, end) in enumerate(FOLD_BOUNDARIES_MS, 1):
        h0_b = _fold_summary(h0_trades_btc, start, end)
        r3_b = _fold_summary(r3_trades_btc, start, end)
        r2_b = _fold_summary(r2_trades_btc, start, end)
        folds_btc.append(
            {
                "fold": f"F{i}",
                "h0_count": h0_b["count"],
                "h0_expR": h0_b["expR"],
                "r3_count": r3_b["count"],
                "r3_expR": r3_b["expR"],
                "r2_count": r2_b["count"],
                "r2_expR": r2_b["expR"],
                "delta_vs_h0": r2_b["expR"] - h0_b["expR"],
                "delta_vs_r3": r2_b["expR"] - r3_b["expR"],
            }
        )
        h0_e = _fold_summary(h0_trades_eth, start, end)
        r3_e = _fold_summary(r3_trades_eth, start, end)
        r2_e = _fold_summary(r2_trades_eth, start, end)
        folds_eth.append(
            {
                "fold": f"F{i}",
                "h0_count": h0_e["count"],
                "h0_expR": h0_e["expR"],
                "r3_count": r3_e["count"],
                "r3_expR": r3_e["expR"],
                "r2_count": r2_e["count"],
                "r2_expR": r2_e["expR"],
                "delta_vs_h0": r2_e["expR"] - h0_e["expR"],
                "delta_vs_r3": r2_e["expR"] - r3_e["expR"],
            }
        )

    btc_wins_vs_h0 = sum(1 for f in folds_btc if f["delta_vs_h0"] > 0)
    btc_wins_vs_r3 = sum(1 for f in folds_btc if f["delta_vs_r3"] > 0)
    eth_wins_vs_h0 = sum(1 for f in folds_eth if f["delta_vs_h0"] > 0)
    eth_wins_vs_r3 = sum(1 for f in folds_eth if f["delta_vs_r3"] > 0)

    return {
        "folds_btc": folds_btc,
        "folds_eth": folds_eth,
        "btc_fold_wins_vs_h0": f"{btc_wins_vs_h0}/5",
        "btc_fold_wins_vs_r3": f"{btc_wins_vs_r3}/5",
        "eth_fold_wins_vs_h0": f"{eth_wins_vs_h0}/5",
        "eth_fold_wins_vs_r3": f"{eth_wins_vs_r3}/5",
    }


# --------------------------------------------------------------------------
# Per-regime expR (§P.9) — simplified report based on summary metrics
# --------------------------------------------------------------------------


def _diagnostic_p9_per_regime_placeholder() -> dict:
    """§P.9 per-regime expR.

    The full per-regime decomposition requires re-running the trades
    through a 1h-volatility tercile classifier (per Phase 2l/2m/2s
    convention: trailing 1000 1h-bar Wilder ATR(20), 33/67 splits).
    For 2w-B, we record this as a deferred sub-computation: the
    regime classification machinery exists in prior Phase 2 analysis
    scripts but is not duplicated here. The 2w-B checkpoint report
    documents this as a noted deferral (computed at report-writing
    time if needed) rather than forced into the analysis JSON.
    """
    return {
        "computed": False,
        "reason": (
            "Per-regime expR requires 1h-volatility tercile classifier "
            "(Phase 2l/2m/2s convention). Not duplicated in 2w-B "
            "analysis script; 2w-C may compute at report-writing time "
            "from the run trade-logs if operator authorizes."
        ),
    }


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 2w R2 analysis script")
    p.add_argument("--r2-r-dir", required=True, type=Path, help="Run #3 R2+R3 R MED MARK")
    p.add_argument("--r2-r-low-dir", required=True, type=Path, help="Run #7 R2+R3 R LOW MARK")
    p.add_argument("--r2-r-high-dir", required=True, type=Path, help="Run #8 R2+R3 R HIGH MARK")
    p.add_argument(
        "--r2-r-trade-dir",
        required=True,
        type=Path,
        help="Run #9 R2+R3 R MED TRADE_PRICE",
    )
    p.add_argument(
        "--r2-r-limit-dir",
        required=True,
        type=Path,
        help="Run #10 R2+R3 R MED MARK limit-at-pullback",
    )
    p.add_argument("--r2-v-dir", required=True, type=Path, help="Run #6 R2+R3 V MED MARK")
    p.add_argument("--h0-r-dir", required=True, type=Path, help="H0 R MED MARK control")
    p.add_argument("--r3-r-dir", required=True, type=Path, help="R3 R MED MARK control")
    p.add_argument("--h0-v-dir", required=True, type=Path, help="H0 V MED MARK control")
    p.add_argument("--r3-v-dir", required=True, type=Path, help="R3 V MED MARK control")
    p.add_argument("--output", required=True, type=Path, help="Output analysis JSON path")
    return p.parse_args()


def main() -> int:
    args = _parse_args()

    # Load all run summaries + trades + lifecycle counters.
    h0_r_btc = _load_summary(args.h0_r_dir, "BTCUSDT")
    h0_r_eth = _load_summary(args.h0_r_dir, "ETHUSDT")
    r3_r_btc = _load_summary(args.r3_r_dir, "BTCUSDT")
    r3_r_eth = _load_summary(args.r3_r_dir, "ETHUSDT")
    r2_r_btc = _load_summary(args.r2_r_dir, "BTCUSDT")
    r2_r_eth = _load_summary(args.r2_r_dir, "ETHUSDT")
    r2_r_low_btc = _load_summary(args.r2_r_low_dir, "BTCUSDT")
    r2_r_low_eth = _load_summary(args.r2_r_low_dir, "ETHUSDT")
    r2_r_high_btc = _load_summary(args.r2_r_high_dir, "BTCUSDT")
    r2_r_high_eth = _load_summary(args.r2_r_high_dir, "ETHUSDT")
    r2_r_trade_btc = _load_summary(args.r2_r_trade_dir, "BTCUSDT")
    r2_r_trade_eth = _load_summary(args.r2_r_trade_dir, "ETHUSDT")
    r2_r_limit_btc = _load_summary(args.r2_r_limit_dir, "BTCUSDT")
    r2_r_limit_eth = _load_summary(args.r2_r_limit_dir, "ETHUSDT")
    h0_v_btc = _load_summary(args.h0_v_dir, "BTCUSDT")
    h0_v_eth = _load_summary(args.h0_v_dir, "ETHUSDT")
    r3_v_btc = _load_summary(args.r3_v_dir, "BTCUSDT")
    r3_v_eth = _load_summary(args.r3_v_dir, "ETHUSDT")
    r2_v_btc = _load_summary(args.r2_v_dir, "BTCUSDT")
    r2_v_eth = _load_summary(args.r2_v_dir, "ETHUSDT")

    h0_r_btc_trades = _load_trades(args.h0_r_dir, "BTCUSDT")
    h0_r_eth_trades = _load_trades(args.h0_r_dir, "ETHUSDT")
    r3_r_btc_trades = _load_trades(args.r3_r_dir, "BTCUSDT")
    r3_r_eth_trades = _load_trades(args.r3_r_dir, "ETHUSDT")
    r2_r_btc_trades = _load_trades(args.r2_r_dir, "BTCUSDT")
    r2_r_eth_trades = _load_trades(args.r2_r_dir, "ETHUSDT")
    # V-window trades are not consumed in 2w-B diagnostics (V-window
    # confirmation uses summary-level metrics only); reserved for 2w-C
    # comparison-report writing if needed.

    r2_r_btc_lifecycle = _load_r2_lifecycle(args.r2_r_dir, "BTCUSDT")
    r2_r_eth_lifecycle = _load_r2_lifecycle(args.r2_r_dir, "ETHUSDT")
    r2_v_btc_lifecycle = _load_r2_lifecycle(args.r2_v_dir, "BTCUSDT")
    r2_v_eth_lifecycle = _load_r2_lifecycle(args.r2_v_dir, "ETHUSDT")
    assert r2_r_btc_lifecycle is not None
    assert r2_r_eth_lifecycle is not None
    assert r2_v_btc_lifecycle is not None
    assert r2_v_eth_lifecycle is not None

    # R-window headline + §10.3 verdict (governing).
    r_headlines = {
        "h0_btc": _headline(h0_r_btc),
        "h0_eth": _headline(h0_r_eth),
        "r3_btc": _headline(r3_r_btc),
        "r3_eth": _headline(r3_r_eth),
        "r2_btc": _headline(r2_r_btc),
        "r2_eth": _headline(r2_r_eth),
    }
    r_deltas_vs_h0 = {
        "btc": _delta_vs(r_headlines["r2_btc"], r_headlines["h0_btc"]),
        "eth": _delta_vs(r_headlines["r2_eth"], r_headlines["h0_eth"]),
    }
    r_deltas_vs_r3 = {
        "btc": _delta_vs(r_headlines["r2_btc"], r_headlines["r3_btc"]),
        "eth": _delta_vs(r_headlines["r2_eth"], r_headlines["r3_eth"]),
    }
    r_section_10_3 = {
        "btc": _section_10_3_verdict(r_deltas_vs_h0["btc"]),
        "eth": _section_10_3_verdict(r_deltas_vs_h0["eth"]),
    }
    eth_catastrophic = r_section_10_3["eth"]["disqualified_floor"]
    r_window_promotes_med = (
        r_section_10_3["btc"]["promotes"]
        and (not r_section_10_3["btc"]["disqualified_floor"])
        and (not eth_catastrophic)
    )
    # §11.6 cost-sensitivity gate (Phase 2v §5.1.7 / §5.4 failure
    # condition 9): R2+R3 must clear §10.3 (no disqualification floor)
    # at HIGH slippage on BOTH symbols. HIGH-slip disqualification
    # blocks the combined verdict regardless of MED-slip PROMOTE.
    high_btc_disq = _section_10_3_verdict(
        _delta_vs(_headline(r2_r_high_btc), r_headlines["h0_btc"])
    )["disqualified_floor"]
    high_eth_disq = _section_10_3_verdict(
        _delta_vs(_headline(r2_r_high_eth), r_headlines["h0_eth"])
    )["disqualified_floor"]
    section_11_6_passes = (not high_btc_disq) and (not high_eth_disq)
    r_window_promotes = r_window_promotes_med and section_11_6_passes

    # V-window headline.
    v_headlines = {
        "h0_btc": _headline(h0_v_btc),
        "h0_eth": _headline(h0_v_eth),
        "r3_btc": _headline(r3_v_btc),
        "r3_eth": _headline(r3_v_eth),
        "r2_btc": _headline(r2_v_btc),
        "r2_eth": _headline(r2_v_eth),
    }
    v_deltas_vs_h0 = {
        "btc": _delta_vs(v_headlines["r2_btc"], v_headlines["h0_btc"]),
        "eth": _delta_vs(v_headlines["r2_eth"], v_headlines["h0_eth"]),
    }

    # Diagnostics.
    diagnostics = {
        "P1_fill_rate_btc": _diagnostic_p1_fill_rate(r2_r_btc_lifecycle),
        "P1_fill_rate_eth": _diagnostic_p1_fill_rate(r2_r_eth_lifecycle),
        "P1_fill_rate_v_btc": _diagnostic_p1_fill_rate(r2_v_btc_lifecycle),
        "P1_fill_rate_v_eth": _diagnostic_p1_fill_rate(r2_v_eth_lifecycle),
        "P2_P11_time_to_fill_btc": _diagnostic_p2_p11_time_to_fill(r2_r_btc_trades),
        "P2_P11_time_to_fill_eth": _diagnostic_p2_p11_time_to_fill(r2_r_eth_trades),
        "P3_stop_distance_reduction_btc": _diagnostic_p3_stop_distance_reduction(
            r2_r_btc_trades, r3_r_btc_trades
        ),
        "P3_stop_distance_reduction_eth": _diagnostic_p3_stop_distance_reduction(
            r2_r_eth_trades, r3_r_eth_trades
        ),
        "P4_stop_exit_fraction_btc": _diagnostic_p4_stop_exit_fraction(
            h0_r_btc, r3_r_btc, r2_r_btc
        ),
        "P4_stop_exit_fraction_eth": _diagnostic_p4_stop_exit_fraction(
            h0_r_eth, r3_r_eth, r2_r_eth
        ),
        "P5_intersection_btc": _diagnostic_p5_intersection_trade(r2_r_btc_trades, r3_r_btc_trades),
        "P5_intersection_eth": _diagnostic_p5_intersection_trade(r2_r_eth_trades, r3_r_eth_trades),
        "P6_fill_model_sensitivity_btc": _diagnostic_p6_fill_model_sensitivity(
            r2_r_btc, r2_r_limit_btc
        ),
        "P6_fill_model_sensitivity_eth": _diagnostic_p6_fill_model_sensitivity(
            r2_r_eth, r2_r_limit_eth
        ),
        "P7_long_short_asymmetry_btc": _diagnostic_p7_long_short_asymmetry(
            h0_r_btc, r3_r_btc, r2_r_btc, r2_r_btc_trades
        ),
        "P7_long_short_asymmetry_eth": _diagnostic_p7_long_short_asymmetry(
            h0_r_eth, r3_r_eth, r2_r_eth, r2_r_eth_trades
        ),
        "P8_per_fold_consistency": _diagnostic_p8_per_fold_consistency(
            r2_r_btc_trades,
            r3_r_btc_trades,
            h0_r_btc_trades,
            r2_r_eth_trades,
            r3_r_eth_trades,
            h0_r_eth_trades,
        ),
        "P9_per_regime_expR": _diagnostic_p9_per_regime_placeholder(),
        "P10_r_distance_distribution_btc": _diagnostic_p10_r_distance_distribution(
            r2_r_btc_trades, r3_r_btc_trades
        ),
        "P10_r_distance_distribution_eth": _diagnostic_p10_r_distance_distribution(
            r2_r_eth_trades, r3_r_eth_trades
        ),
        "P12_mfe_mae_at_fill_btc": _diagnostic_p12_mfe_mae_at_fill(
            r2_r_btc_trades, r3_r_btc_trades
        ),
        "P12_mfe_mae_at_fill_eth": _diagnostic_p12_mfe_mae_at_fill(
            r2_r_eth_trades, r3_r_eth_trades
        ),
        "P13_stop_trigger_sensitivity_btc": _diagnostic_p13_stop_trigger_sensitivity(
            r2_r_btc, r2_r_trade_btc
        ),
        "P13_stop_trigger_sensitivity_eth": _diagnostic_p13_stop_trigger_sensitivity(
            r2_r_eth, r2_r_trade_eth
        ),
        # Run #3 uses MEDIUM slippage = 3 bps per
        # ``research/backtest/config.py`` ``DEFAULT_SLIPPAGE_BPS``. The
        # band check uses raw next_bar.open; we de-slip the recorded
        # fill_price to match.
        "P14_implementation_bug_checks_btc": _diagnostic_p14_implementation_bug_checks(
            r2_r_btc, r2_r_btc_trades, r2_r_btc_lifecycle, slippage_bps=3.0
        ),
        "P14_implementation_bug_checks_eth": _diagnostic_p14_implementation_bug_checks(
            r2_r_eth, r2_r_eth_trades, r2_r_eth_lifecycle, slippage_bps=3.0
        ),
        "section_11_6_slippage_sensitivity_btc": _diagnostic_p11_6_slippage_sensitivity(
            r2_r_btc, r2_r_low_btc, r2_r_high_btc, h0_r_btc
        ),
        "section_11_6_slippage_sensitivity_eth": _diagnostic_p11_6_slippage_sensitivity(
            r2_r_eth, r2_r_low_eth, r2_r_high_eth, h0_r_eth
        ),
        "M3_mechanical_r_distance_btc": _diagnostic_m3_mechanical_r_distance(
            r2_r_btc_trades, r3_r_btc_trades
        ),
        "M3_mechanical_r_distance_eth": _diagnostic_m3_mechanical_r_distance(
            r2_r_eth_trades, r3_r_eth_trades
        ),
    }

    # M1/M2/M3 mechanism validation summary.
    m1_btc_mean = diagnostics["P5_intersection_btc"].get("mean_delta_R")
    m1_btc_pass = (m1_btc_mean is not None) and (m1_btc_mean >= M1_DELTA_R3_BTC)
    m2_btc_pass = diagnostics["P4_stop_exit_fraction_btc"]["m2_passed"]
    m3_btc_pass = diagnostics["M3_mechanical_r_distance_btc"]["m3_passed"]
    m1_eth_mean = diagnostics["P5_intersection_eth"].get("mean_delta_R")
    m2_eth_pass = diagnostics["P4_stop_exit_fraction_eth"]["m2_passed"]
    m3_eth_pass = diagnostics["M3_mechanical_r_distance_eth"]["m3_passed"]

    mechanism_validation = {
        "btc": {
            "M1_per_trade_expectancy_pass": m1_btc_pass,
            "M1_mean_delta_R_intersection": m1_btc_mean,
            "M1_threshold": M1_DELTA_R3_BTC,
            "M2_stop_exit_fraction_pass": m2_btc_pass,
            "M3_r_distance_reduction_pass": m3_btc_pass,
            "all_three_pass": m1_btc_pass and m2_btc_pass and m3_btc_pass,
        },
        "eth": {
            "M1_mean_delta_R_intersection": m1_eth_mean,
            "M1_pass_at_btc_threshold": (m1_eth_mean is not None)
            and (m1_eth_mean >= M1_DELTA_R3_BTC),
            "M2_stop_exit_fraction_pass": m2_eth_pass,
            "M3_r_distance_reduction_pass": m3_eth_pass,
        },
    }

    # Combined verdict per Phase 2v §5.3 + §11.6 gate.
    framework_verdict = "PROMOTE" if r_window_promotes else "FAILED"
    if r_window_promotes:
        if (
            mechanism_validation["btc"]["M1_per_trade_expectancy_pass"]
            and mechanism_validation["btc"]["M2_stop_exit_fraction_pass"]
            and mechanism_validation["btc"]["M3_r_distance_reduction_pass"]
        ):
            combined_verdict = "PROMOTE — MECHANISM VALIDATED"
        elif not mechanism_validation["btc"]["M3_r_distance_reduction_pass"]:
            combined_verdict = "HOLD pending implementation review (M3 mechanical fail)"
        elif mechanism_validation["btc"]["M1_per_trade_expectancy_pass"]:
            combined_verdict = "PROMOTE — MECHANISM PARTIALLY SUPPORTED"
        else:
            combined_verdict = "PROMOTE — MECHANISM NOT VALIDATED (R1b-narrow pattern)"
    elif r_window_promotes_med and not section_11_6_passes:
        combined_verdict = (
            "FAILED — §11.6 cost-sensitivity blocks (HIGH slippage triggers "
            "§10.3 disqualification on BTC and/or ETH despite MED-slip PROMOTE)"
        )
    elif eth_catastrophic:
        combined_verdict = "FAILED — §11.4 ETH catastrophic disqualification"
    else:
        combined_verdict = "FAILED — §10.3 disqualification on BTC at MED slippage"

    output = {
        "report_date_utc": datetime.now(tz=UTC).isoformat(),
        "phase": "2w-B R2 execution + diagnostics",
        "r_window": {
            "headlines": r_headlines,
            "deltas_vs_h0": r_deltas_vs_h0,
            "deltas_vs_r3_descriptive": r_deltas_vs_r3,
            "section_10_3_verdict": r_section_10_3,
            "eth_catastrophic_section_11_4": eth_catastrophic,
            "promotes_med_slip_under_section_10_3": r_window_promotes_med,
            "section_11_6_passes_high_slippage": section_11_6_passes,
            "high_slip_btc_disqualified": high_btc_disq,
            "high_slip_eth_disqualified": high_eth_disq,
            "promotes_combined": r_window_promotes,
        },
        "v_window": {
            "headlines": v_headlines,
            "deltas_vs_h0": v_deltas_vs_h0,
            "ran_because": (
                "R-window §10.3 PROMOTE per Phase 2v §11.3"
                if r_window_promotes
                else "R-window did not PROMOTE"
            ),
        },
        "diagnostics": diagnostics,
        "mechanism_validation": mechanism_validation,
        "framework_verdict": framework_verdict,
        "combined_verdict": combined_verdict,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True))
    print(f"\nAnalysis written to: {args.output}")
    print(f"Combined verdict: {combined_verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
