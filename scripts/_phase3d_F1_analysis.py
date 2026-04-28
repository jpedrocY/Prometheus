"""Phase 3d-B2 F1 analysis script.

Reads the trade logs from the four mandatory F1 R-window runs plus the
H0/R3 control runs, computes the §7.2 first-execution-gate evaluation,
the §9 M1 / M2 / M3 mechanism checks, and the §8 mandatory diagnostics
subset that does not require running additional backtests, and writes a
single JSON analysis output.

The script consumes only existing per-run artifacts (under
``data/derived/backtests/``) plus the v002 normalized klines (for the
M1 post-entry counter-displacement and M2 1h-vol regime classifier).

Output: ``data/derived/backtests/phase-3d-f1-analysis-<run_id>.json``
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
from prometheus.strategy.indicators import wilder_atr

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


def _load_lifecycle(run_dir: Path, symbol: Symbol) -> dict:
    f = run_dir / symbol.value / "f1_lifecycle_total.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text())


def _build_open_time_index(klines: list) -> dict[int, int]:  # type: ignore[type-arg]
    return {b.open_time: i for i, b in enumerate(klines)}


def _m1_counter_displacements(
    trades: list[dict], klines_15m: list, horizons: tuple[int, ...] = (1, 2, 4, 8)
) -> dict[str, dict[int, dict[str, float]]]:  # type: ignore[type-arg]
    """Per-trade post-entry counter-displacement at the requested horizons.

    counter_displacement_h = (close(fill_bar + h) - close(fill_bar))
                             * trade_direction_sign
    where trade_direction_sign = +1 for LONG, -1 for SHORT (positive
    means the price moved in the trade's profit direction).

    counter_displacement_h_R = counter_displacement_h / stop_distance.

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
        c_fill = closes[fill_idx]
        for h in horizons:
            if fill_idx + h >= len(closes):
                continue
            cd = (closes[fill_idx + h] - c_fill) * direction_sign
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


def _vol_regime_1h(klines_1h: list) -> tuple[list[float], list[int]]:  # type: ignore[type-arg]
    """Classify each 1h bar into a vol tercile (0=low, 1=med, 2=high)
    using a trailing 1000-bar ATR(20) percentile rank with tercile cuts
    at 33rd / 67th percentiles (Phase 2l §6.1 / Phase 2w §11.9).

    Returns (atr20_1h, regime_label_per_bar). Bars before the lookback
    is filled return regime label -1.
    """
    highs = [float(b.high) for b in klines_1h]
    lows = [float(b.low) for b in klines_1h]
    closes = [float(b.close) for b in klines_1h]
    atr20 = wilder_atr(highs, lows, closes, period=20)

    lookback = 1000
    labels: list[int] = []
    for i, atr in enumerate(atr20):
        if i < lookback:
            labels.append(-1)
            continue
        window = [a for a in atr20[i - lookback : i] if a == a]  # drop NaN
        if len(window) < 200:
            labels.append(-1)
            continue
        sorted_w = sorted(window)
        # percentile rank of atr against window
        rank = sum(1 for v in sorted_w if v < atr)
        pct = rank / len(sorted_w)
        if pct < 1.0 / 3.0:
            labels.append(0)
        elif pct < 2.0 / 3.0:
            labels.append(1)
        else:
            labels.append(2)
    return atr20, labels


def _classify_trade_regime(
    trades: list[dict],
    klines_1h: list,
    regime_labels: list[int],  # type: ignore[type-arg]
) -> dict[int, list[dict]]:
    """Bucket trades by the 1h-vol regime at the most recent completed
    1h bar before the trade's fill time.
    """
    bars_close_time = [b.close_time for b in klines_1h]
    by_regime: dict[int, list[dict]] = defaultdict(list)
    for t in trades:
        fill_ms = int(t["entry_fill_time_ms"])
        # Find latest 1h bar with close_time < fill_ms (completed before fill).
        # Linear scan acceptable; trades are sequential.
        idx = -1
        for i in range(len(bars_close_time) - 1, -1, -1):
            if bars_close_time[i] < fill_ms:
                idx = i
                break
        if idx < 0:
            continue
        label = regime_labels[idx]
        by_regime[label].append(t)
    return by_regime


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
    """5 rolling 6-month folds across the R-window.

    Phase 2f §11.2 / GAP-20260424-036 fold convention: 5 rolling folds;
    6-month test windows stepping 6 months. R-window covers 36 months
    (Jan 2022 → Jan 2025). Folds are F1=2022H1, F2=2022H2, F3=2023H1,
    F4=2023H2, F5=2024H1, F6=2024H2 (6 folds, but Phase 2 uses 5; we
    use the 6 natural half-year cells for descriptive purposes).
    """
    fold_bounds = [
        ("F1_2022H1", 1_640_995_200_000, 1_656_633_600_000),  # 2022-01-01 - 2022-07-01
        ("F2_2022H2", 1_656_633_600_000, 1_672_531_200_000),  # 2022-07-01 - 2023-01-01
        ("F3_2023H1", 1_672_531_200_000, 1_688_169_600_000),  # 2023-01-01 - 2023-07-01
        ("F4_2023H2", 1_688_169_600_000, 1_704_067_200_000),  # 2023-07-01 - 2024-01-01
        ("F5_2024H1", 1_704_067_200_000, 1_719_792_000_000),  # 2024-01-01 - 2024-07-01
        ("F6_2024H2", 1_719_792_000_000, 1_735_689_600_000),  # 2024-07-01 - 2025-01-01
    ]
    out: list[dict] = []
    for name, start, end in fold_bounds:
        bucket = [t for t in trades if start <= int(t["exit_fill_time_ms"]) < end]
        s = _bucket_summary(bucket)
        out.append({"fold": name, **s})
    return out


def _exit_fractions(trades: list[dict]) -> dict[str, int | float]:
    n = len(trades)
    if n == 0:
        return {"n": 0}
    counts = defaultdict(int)
    for t in trades:
        counts[str(t["exit_reason"])] += 1
    out: dict[str, int | float] = {"n": n}
    for k, v in counts.items():
        out[f"count_{k}"] = v
        out[f"frac_{k}"] = v / n
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


def _f1_field_distributions(trades: list[dict]) -> dict[str, dict[str, float]]:
    return {
        "overextension_magnitude_at_signal": _distribution_stats(
            [float(t["overextension_magnitude_at_signal"]) for t in trades]
        ),
        "stop_distance_at_signal_atr": _distribution_stats(
            [float(t["stop_distance_at_signal_atr"]) for t in trades]
        ),
        "entry_to_target_distance_atr": _distribution_stats(
            [float(t["entry_to_target_distance_atr"]) for t in trades]
        ),
    }


def _p14_invariants(trades: list[dict]) -> dict[str, bool | int]:
    allowed = {"STOP", "TARGET", "TIME_STOP", "END_OF_DATA"}
    forbidden = {"TRAILING_BREACH", "STAGNATION", "TAKE_PROFIT"}
    n = len(trades)
    bad_exit = sum(1 for t in trades if t["exit_reason"] in forbidden)
    only_allowed = bad_exit == 0 and all(t["exit_reason"] in allowed for t in trades)
    band_ok = all(0.60 <= float(t["stop_distance_at_signal_atr"]) <= 1.80 for t in trades)
    sd_at_signal = [
        float(t["stop_distance_at_signal_atr"]) for t in trades if t["stop_distance"] > 0
    ]
    return {
        "n_trades": n,
        "no_v1_only_exit_reasons": bool(only_allowed),
        "n_trades_with_forbidden_exit_reason": bad_exit,
        "raw_stop_distance_in_band": bool(band_ok),
        "min_stop_distance_atr": min(sd_at_signal) if sd_at_signal else 0.0,
        "max_stop_distance_atr": max(sd_at_signal) if sd_at_signal else 0.0,
    }


def _m3_target_subset(trades: list[dict]) -> dict[str, float | int]:
    sub = [t for t in trades if t["exit_reason"] == "TARGET"]
    n = len(sub)
    if n == 0:
        return {"n": 0, "aggregate_R": 0.0, "mean_R": 0.0}
    agg = sum(float(t["net_r_multiple"]) for t in sub)
    return {"n": n, "aggregate_R": agg, "mean_R": agg / n}


# ---------------------------------------------------------------------------


def main() -> int:
    out: dict[str, object] = {}

    # Locate the latest run directories for each F1 cell.
    cells = {
        "F1_R_MED_MARK": "phase-3d-f1-window=r-slip=medium",
        "F1_R_LOW_MARK": "phase-3d-f1-window=r-slip=low",
        "F1_R_HIGH_MARK": "phase-3d-f1-window=r-slip=high",
        "F1_R_MED_TRADE": "phase-3d-f1-window=r-slip=medium-stop=trade_price",
    }
    cell_dirs: dict[str, Path] = {k: _latest_run_dir(v) for k, v in cells.items()}

    # Locate the latest H0/R3 control run dirs (for descriptive
    # cross-family deltas + M2 H0 low-vol stop-out fraction).
    control_dirs = {
        "H0_R": _latest_run_dir("phase-2l-h0-r"),
        "H0_V": _latest_run_dir("phase-2l-h0-v"),
        "R3_R": _latest_run_dir("phase-2l-r3-r"),
        "R3_V": _latest_run_dir("phase-2l-r3-v"),
    }

    # Load 15m + 1h klines for M1 + M2.
    klines_root = DATA_ROOT / "normalized" / "klines"
    bars_1h_root = DATA_ROOT / "derived" / "bars_1h" / "standard"
    klines_15m: dict[Symbol, list] = {}  # type: ignore[type-arg]
    klines_1h: dict[Symbol, list] = {}  # type: ignore[type-arg]
    regime_1h: dict[Symbol, list[int]] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        klines_15m[s] = read_klines(klines_root, symbol=s, interval=Interval.I_15M)
        klines_1h[s] = read_klines(bars_1h_root, symbol=s, interval=Interval.I_1H)
        _atr, regime_1h[s] = _vol_regime_1h(klines_1h[s])

    # ----- §7.2 first-execution gate -----
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
                "BTCUSDT": _load_lifecycle(run_dir, Symbol.BTCUSDT),
                "ETHUSDT": _load_lifecycle(run_dir, Symbol.ETHUSDT),
            },
        }
        for cell_id, run_dir in cell_dirs.items()
    }

    btc_med = summaries["F1_R_MED_MARK"]["BTCUSDT"]
    eth_med = summaries["F1_R_MED_MARK"]["ETHUSDT"]
    btc_high = summaries["F1_R_HIGH_MARK"]["BTCUSDT"]
    eth_high = summaries["F1_R_HIGH_MARK"]["ETHUSDT"]

    cond_i = btc_med["expectancy_r"] > 0
    cond_iii = eth_med["expectancy_r"] > -0.50 and eth_med["profit_factor"] > 0.30
    cond_iv = (
        btc_high["expectancy_r"] > 0
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

    # ----- §9 M1 mechanism (BTC + ETH; BTC drives §7.2(ii)) -----
    m1: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        trades = _load_trades(cell_dirs["F1_R_MED_MARK"], s)
        m1[s.value] = _m1_counter_displacements(trades, klines_15m[s])
    btc_m1_8 = m1[Symbol.BTCUSDT.value]["counter_h_R"][8]
    cond_ii = btc_m1_8["mean"] >= 0.10 and btc_m1_8["fraction_non_neg"] >= 0.50

    # ----- Verdict mapping (Phase 3c §7.3) -----
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
        "condition_ii_M1_BTC_pass": cond_ii,
        "condition_iii_ETH_MED_non_catastrophic": cond_iii,
        "condition_iv_HIGH_slippage_cost_sensitivity": cond_iv,
        "condition_v_MED_absolute_floors": cond_v,
        "catastrophic_floor_violation": catastrophic_floor_violation,
        "verdict": verdict,
    }
    out["m1_mechanism"] = m1

    # ----- M2 chop-regime stop-out fraction -----
    m2: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        f1_trades = _load_trades(cell_dirs["F1_R_MED_MARK"], s)
        h0_trades = _load_trades(control_dirs["H0_R"], s)
        f1_by_regime = _classify_trade_regime(f1_trades, klines_1h[s], regime_1h[s])
        h0_by_regime = _classify_trade_regime(h0_trades, klines_1h[s], regime_1h[s])
        f1_low = _bucket_summary(f1_by_regime.get(0, []))
        h0_low = _bucket_summary(h0_by_regime.get(0, []))
        delta = h0_low["stop_frac"] - f1_low["stop_frac"]
        m2[s.value] = {
            "f1_low_vol": f1_low,
            "h0_low_vol": h0_low,
            "delta_M2_h0_minus_f1": delta,
            "M2_pass_descriptive_threshold_0_10": delta >= 0.10,
        }
    out["m2_mechanism"] = m2

    # ----- M3 target-exit subset -----
    m3: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        f1_trades = _load_trades(cell_dirs["F1_R_MED_MARK"], s)
        m3[s.value] = _m3_target_subset(f1_trades)
    btc_m3 = m3[Symbol.BTCUSDT.value]
    eth_m3 = m3[Symbol.ETHUSDT.value]
    m3_pass = (
        btc_m3.get("aggregate_R", 0.0) > 0
        and eth_m3.get("aggregate_R", 0.0) > 0
        and btc_m3.get("mean_R", 0.0) >= 0.30
        and eth_m3.get("mean_R", 0.0) >= 0.30
    )
    out["m3_mechanism"] = {**m3, "M3_pass_both_symbols": m3_pass}

    # ----- §8 mandatory diagnostics subset -----
    diag: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        f1_trades = _load_trades(cell_dirs["F1_R_MED_MARK"], s)
        diag[s.value] = {
            "trade_count": len(f1_trades),
            "long_count": sum(1 for t in f1_trades if t["direction"] == "LONG"),
            "short_count": sum(1 for t in f1_trades if t["direction"] == "SHORT"),
            "exit_fractions": _exit_fractions(f1_trades),
            "field_distributions": _f1_field_distributions(f1_trades),
            "per_fold": _per_fold_breakdown(f1_trades),
            "p14_invariants": _p14_invariants(f1_trades),
        }
    out["diagnostics_F1_R_MED_MARK"] = diag

    # ----- Cost sensitivity LOW / MED / HIGH cross-cell summary -----
    out["cost_sensitivity"] = {
        s.value: {
            "LOW": summaries["F1_R_LOW_MARK"][s.value],
            "MED": summaries["F1_R_MED_MARK"][s.value],
            "HIGH": summaries["F1_R_HIGH_MARK"][s.value],
        }
        for s in (Symbol.BTCUSDT, Symbol.ETHUSDT)
    }

    # ----- Mark vs Trade-price stop-trigger sensitivity -----
    out["stop_trigger_sensitivity"] = {
        s.value: {
            "MARK": summaries["F1_R_MED_MARK"][s.value],
            "TRADE_PRICE": summaries["F1_R_MED_TRADE"][s.value],
        }
        for s in (Symbol.BTCUSDT, Symbol.ETHUSDT)
    }

    # ----- Cross-family descriptive references (H0 R / R3 R) -----
    cross_family: dict[str, dict] = {}
    for s in (Symbol.BTCUSDT, Symbol.ETHUSDT):
        f1 = summaries["F1_R_MED_MARK"][s.value]
        h0 = json.loads((control_dirs["H0_R"] / s.value / "summary_metrics.json").read_text())
        r3 = json.loads((control_dirs["R3_R"] / s.value / "summary_metrics.json").read_text())
        cross_family[s.value] = {
            "F1_R_MED_MARK": f1,
            "H0_R_MED_MARK": h0,
            "R3_R_MED_MARK": r3,
            "delta_F1_minus_H0": {
                "expR": f1["expectancy_r"] - h0["expectancy_r"],
                "PF": f1["profit_factor"] - h0["profit_factor"],
                "trade_count_pct": (f1["trade_count"] - h0["trade_count"])
                / max(h0["trade_count"], 1),
            },
            "delta_F1_minus_R3": {
                "expR": f1["expectancy_r"] - r3["expectancy_r"],
                "PF": f1["profit_factor"] - r3["profit_factor"],
                "trade_count_pct": (f1["trade_count"] - r3["trade_count"])
                / max(r3["trade_count"], 1),
            },
        }
    out["cross_family_descriptive"] = cross_family

    # ----- Save -----
    run_id = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    out_path = DATA_ROOT / "derived" / "backtests" / f"phase-3d-f1-analysis-{run_id}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True, default=str))
    print(f"Analysis written to: {out_path}")
    print(f"\nVerdict: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
