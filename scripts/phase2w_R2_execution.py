"""Phase 2w R2 (pullback-retest entry) execution runner.

Runs the Phase 2u/2v Gate-2-amended R2 candidate (entry_kind=
PULLBACK_RETEST on top of the locked R3 exit baseline) on the locked
Phase 2e v002 datasets. Includes the H0 control and the R3-only locked
control on the same engine version for the §10.3 H0-anchor comparison.

Variants:
    H0      — V1BreakoutConfig() defaults (locked Phase 2e baseline).
    R3      — V1BreakoutConfig(exit_kind=FIXED_R_TIME_STOP, R-target=2.0,
              time-stop=8). Locked exit baseline (Phase 2j memo §D).
    R2+R3   — R3 + entry_kind=PULLBACK_RETEST. The Phase 2u R2
              candidate per the Gate-2-amended spec memo §F.

Per the Phase 2w-B operator-approved brief + Phase 2u spec memo +
Phase 2v Gate 1 execution plan + Phase 2v Gate 2 review:

  - Research-only. No live trading, no exchange adapter, no keys.
  - Same v002 datasets as Phase 2e/2g/2l/2m/2s. No data downloads.
  - One variant per invocation.
  - H0 + R3 controls re-run on the same engine version.
  - R2 sub-parameters committed singularly per Phase 2u §F (pullback
    level=setup_high/setup_low; confirmation=close-not-violating-stop;
    validity window=8 bars; committed fill model=next-bar-open after
    confirmation). Hard-coded; no V1BreakoutConfig fill-model field.
  - Mark-price stop-trigger semantics preserved as default; TRADE_PRICE
    is a sensitivity diagnostic per GAP-20260424-032.
  - The diagnostic-only ``--fill-model limit-at-pullback`` flag enables
    Phase 2u §P.6 / Phase 2v run #10 fill-model sensitivity. It is
    intentionally NOT a V1BreakoutConfig field (Phase 2v Gate 2
    clarification): only this runner script can opt in, and only
    run #3's committed next-bar-open path is eligible for §10.3
    governing evaluation.

Usage::

    uv run python scripts/phase2w_R2_execution.py --variant H0      --window R
    uv run python scripts/phase2w_R2_execution.py --variant R3      --window R
    uv run python scripts/phase2w_R2_execution.py --variant R2+R3   --window R
    uv run python scripts/phase2w_R2_execution.py --variant R2+R3   --window V
    uv run python scripts/phase2w_R2_execution.py --variant R2+R3   --window R \\
        --slippage HIGH
    uv run python scripts/phase2w_R2_execution.py --variant R2+R3   --window R \\
        --stop-trigger TRADE_PRICE
    uv run python scripts/phase2w_R2_execution.py --variant R2+R3   --window R \\
        --fill-model limit-at-pullback

Output directory::

    data/derived/backtests/phase-2w-r2-<variant>-<window>[-<suffixes>]/<run_id>/
        <SYMBOL>/
            trade_log.{parquet,json}
            summary_metrics.json
            funnel_total.json
            r2_lifecycle_total.json    (R2 path only)
            equity_curve.parquet
            drawdown.parquet
            r_multiple_hist.parquet
            monthly_breakdown.parquet
            yearly_breakdown.parquet
        backtest_report.manifest.json
        config_snapshot.json

Artifacts under data/ are git-ignored.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from prometheus.core.exchange_info import ExchangeInfoSnapshot
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.backtest import (
    BacktestConfig,
    BacktestEngine,
    SignalFunnelCounts,
    SlippageBucket,
    StopTriggerSource,
    run_signal_funnel,
)
from prometheus.research.backtest.config import DEFAULT_SLIPPAGE_BPS
from prometheus.research.backtest.engine import R2LifecycleCounters
from prometheus.research.backtest.report import DatasetCitation, write_report
from prometheus.research.backtest.trade_log import TradeRecord
from prometheus.research.data.storage import (
    read_funding_rate_events,
    read_klines,
    read_mark_price_klines,
)
from prometheus.strategy.v1_breakout import EntryKind, ExitKind, V1BreakoutConfig

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"

SYMBOLS = (Symbol.BTCUSDT, Symbol.ETHUSDT)

WINDOWS: dict[str, tuple[int, int]] = {
    "R": (1_640_995_200_000, 1_735_689_600_000),
    "V": (1_735_689_600_000, 1_775_001_600_000),
    "FULL": (1_640_995_200_000, 1_775_001_600_000),
}

# Phase 2w carry-forward: H0 control, R3 locked control, R2+R3 candidate.
# All four R2 sub-parameters are hard-coded in entry_lifecycle.py and
# the engine; only the EntryKind axis is exposed via V1BreakoutConfig.
VARIANTS: dict[str, V1BreakoutConfig] = {
    "H0": V1BreakoutConfig(),
    "R3": V1BreakoutConfig(
        exit_kind=ExitKind.FIXED_R_TIME_STOP,
        exit_r_target=2.0,
        exit_time_stop_bars=8,
    ),
    "R2+R3": V1BreakoutConfig(
        exit_kind=ExitKind.FIXED_R_TIME_STOP,
        exit_r_target=2.0,
        exit_time_stop_bars=8,
        entry_kind=EntryKind.PULLBACK_RETEST,
    ),
}

# Diagnostic-only fill-model sensitivity (Phase 2u §P.6 / Phase 2v
# run #10). Per Phase 2v Gate 2 clarification, this exists ONLY as a
# runner-script flag and never as a V1BreakoutConfig field. The
# committed model (Phase 2u §F.4) is "next-bar-open" — the only path
# eligible for §10.3 governing evaluation.
FILL_MODELS = {
    "next-bar-open": "next-bar-open-after-confirmation",
    "limit-at-pullback": "limit-at-pullback-intrabar",
}


def _banner(title: str) -> None:
    bar = "=" * 72
    print(f"\n{bar}\n{title}\n{bar}")


def _exchange_info_path() -> Path:
    candidates = sorted((DATA_ROOT / "derived" / "exchange_info").glob("*.json"))
    if not candidates:
        raise RuntimeError("No exchangeInfo snapshot under data/derived/exchange_info/")
    return candidates[-1]


def _load_symbol_info(ei_path: Path, symbol: Symbol):  # type: ignore[no-untyped-def]
    snap = ExchangeInfoSnapshot.model_validate(json.loads(ei_path.read_text()))
    for si in snap.symbols:
        if si.symbol == symbol.value:
            return si
    raise RuntimeError(f"{symbol.value} not in exchangeInfo snapshot {ei_path}")


def _ym_for_ms(ms: int) -> tuple[int, int]:
    dt = datetime.fromtimestamp(ms / 1000.0, tz=UTC)
    return dt.year, dt.month


def _aggregate_trades_by_month(trades: list[TradeRecord]) -> pa.Table:
    by_ym: dict[tuple[int, int], dict[str, float | int]] = defaultdict(
        lambda: {
            "trade_count": 0,
            "win_count": 0,
            "loss_count": 0,
            "long_count": 0,
            "short_count": 0,
            "stop_exits": 0,
            "trailing_exits": 0,
            "stagnation_exits": 0,
            "take_profit_exits": 0,
            "time_stop_exits": 0,
            "end_of_data_exits": 0,
            "gross_pnl": 0.0,
            "net_pnl": 0.0,
            "fees": 0.0,
            "funding": 0.0,
            "sum_r": 0.0,
        }
    )
    for t in trades:
        ym = _ym_for_ms(t.exit_fill_time_ms)
        row = by_ym[ym]
        row["trade_count"] = int(row["trade_count"]) + 1
        if t.net_pnl > 0:
            row["win_count"] = int(row["win_count"]) + 1
        else:
            row["loss_count"] = int(row["loss_count"]) + 1
        if t.direction == "LONG":
            row["long_count"] = int(row["long_count"]) + 1
        else:
            row["short_count"] = int(row["short_count"]) + 1
        if t.exit_reason == "STOP":
            row["stop_exits"] = int(row["stop_exits"]) + 1
        elif t.exit_reason == "TRAILING_BREACH":
            row["trailing_exits"] = int(row["trailing_exits"]) + 1
        elif t.exit_reason == "STAGNATION":
            row["stagnation_exits"] = int(row["stagnation_exits"]) + 1
        elif t.exit_reason == "TAKE_PROFIT":
            row["take_profit_exits"] = int(row["take_profit_exits"]) + 1
        elif t.exit_reason == "TIME_STOP":
            row["time_stop_exits"] = int(row["time_stop_exits"]) + 1
        elif t.exit_reason == "END_OF_DATA":
            row["end_of_data_exits"] = int(row["end_of_data_exits"]) + 1
        row["gross_pnl"] = float(row["gross_pnl"]) + float(t.gross_pnl)
        row["net_pnl"] = float(row["net_pnl"]) + float(t.net_pnl)
        row["fees"] = float(row["fees"]) + float(t.entry_fee + t.exit_fee)
        row["funding"] = float(row["funding"]) + float(t.funding_pnl)
        row["sum_r"] = float(row["sum_r"]) + float(t.net_r_multiple)
    years: list[int] = []
    months: list[int] = []
    cols: dict[str, list[int | float]] = defaultdict(list)
    for y, m in sorted(by_ym):
        years.append(y)
        months.append(m)
        for k, v in by_ym[(y, m)].items():
            cols[k].append(v)
    return pa.table({"year": years, "month": months, **cols})


def _aggregate_trades_by_year(trades: list[TradeRecord]) -> pa.Table:
    by_y: dict[int, dict[str, float | int]] = defaultdict(
        lambda: {
            "trade_count": 0,
            "win_count": 0,
            "loss_count": 0,
            "stop_exits": 0,
            "trailing_exits": 0,
            "stagnation_exits": 0,
            "take_profit_exits": 0,
            "time_stop_exits": 0,
            "end_of_data_exits": 0,
            "gross_pnl": 0.0,
            "net_pnl": 0.0,
            "fees": 0.0,
            "funding": 0.0,
            "sum_r": 0.0,
        }
    )
    for t in trades:
        y, _ = _ym_for_ms(t.exit_fill_time_ms)
        row = by_y[y]
        row["trade_count"] = int(row["trade_count"]) + 1
        if t.net_pnl > 0:
            row["win_count"] = int(row["win_count"]) + 1
        else:
            row["loss_count"] = int(row["loss_count"]) + 1
        if t.exit_reason == "STOP":
            row["stop_exits"] = int(row["stop_exits"]) + 1
        elif t.exit_reason == "TRAILING_BREACH":
            row["trailing_exits"] = int(row["trailing_exits"]) + 1
        elif t.exit_reason == "STAGNATION":
            row["stagnation_exits"] = int(row["stagnation_exits"]) + 1
        elif t.exit_reason == "TAKE_PROFIT":
            row["take_profit_exits"] = int(row["take_profit_exits"]) + 1
        elif t.exit_reason == "TIME_STOP":
            row["time_stop_exits"] = int(row["time_stop_exits"]) + 1
        elif t.exit_reason == "END_OF_DATA":
            row["end_of_data_exits"] = int(row["end_of_data_exits"]) + 1
        row["gross_pnl"] = float(row["gross_pnl"]) + float(t.gross_pnl)
        row["net_pnl"] = float(row["net_pnl"]) + float(t.net_pnl)
        row["fees"] = float(row["fees"]) + float(t.entry_fee + t.exit_fee)
        row["funding"] = float(row["funding"]) + float(t.funding_pnl)
        row["sum_r"] = float(row["sum_r"]) + float(t.net_r_multiple)
    years_sorted = sorted(by_y)
    cols: dict[str, list[int | float]] = defaultdict(list)
    for y in years_sorted:
        for k, v in by_y[y].items():
            cols[k].append(v)
    return pa.table({"year": years_sorted, **cols})


def _funnel_summary_dict(f: SignalFunnelCounts) -> dict[str, object]:
    return {
        "symbol": f.symbol.value,
        "total_15m_bars_loaded": f.total_15m_bars_loaded,
        "total_1h_bars_loaded": f.total_1h_bars_loaded,
        "warmup_15m_bars_excluded": f.warmup_15m_bars_excluded,
        "warmup_1h_bars_excluded": f.warmup_1h_bars_excluded,
        "decision_bars_evaluated": f.decision_bars_evaluated,
        "bias_long_count": f.bias_long_count,
        "bias_short_count": f.bias_short_count,
        "bias_neutral_count": f.bias_neutral_count,
        "valid_setup_windows_detected": f.valid_setup_windows_detected,
        "long_breakout_candidates": f.long_breakout_candidates,
        "short_breakout_candidates": f.short_breakout_candidates,
        "rejected_neutral_bias": f.rejected_neutral_bias,
        "rejected_no_valid_setup": f.rejected_no_valid_setup,
        "rejected_close_did_not_break_level": f.rejected_close_did_not_break_level,
        "rejected_true_range_too_small": f.rejected_true_range_too_small,
        "rejected_close_location_failed": f.rejected_close_location_failed,
        "rejected_normalized_atr_regime_failed": f.rejected_normalized_atr_regime_failed,
        "rejected_stop_distance_filter_failed": f.rejected_stop_distance_filter_failed,
        "rejected_sizing_failed": f.rejected_sizing_failed,
        "sizing_below_minqty": f.sizing_below_minqty,
        "sizing_below_min_notional": f.sizing_below_min_notional,
        "sizing_missing_filters": f.sizing_missing_filters,
        "end_of_data_no_fill": f.end_of_data_no_fill,
        "entry_intents_produced": f.entry_intents_produced,
        "trades_filled": f.trades_filled,
        "trades_closed": f.trades_closed,
    }


def _r2_lifecycle_dict(c: R2LifecycleCounters, symbol: Symbol) -> dict[str, object]:
    """Serialize the per-symbol R2 lifecycle counters for sidecar output.

    The accounting identity per Phase 2u §J.4 (Gate 2 amended):

        registered = no_pullback + bias_flip + opposite_signal
                   + structural_invalidation + stop_distance_at_fill
                   + filled

    is enforced via ``c.accounting_identity_holds`` and reported here.
    """
    return {
        "symbol": symbol.value,
        "registered_candidates": c.registered,
        "expired_candidates_no_pullback": c.expired_no_pullback,
        "expired_candidates_bias_flip": c.cancelled_bias_flip,
        "expired_candidates_opposite_signal": c.cancelled_opposite_signal,
        "expired_candidates_structural_invalidation": c.cancelled_structural_invalidation,
        "expired_candidates_stop_distance_at_fill": c.cancelled_stop_distance_at_fill,
        "trades_filled_R2": c.filled,
        "fill_rate": (c.filled / c.registered) if c.registered > 0 else 0.0,
        "accounting_identity_holds": c.accounting_identity_holds,
    }


def _experiment_label(variant_id: str) -> str:
    return variant_id.lower().replace("+", "_").replace("-", "_")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 2w R2 execution runner")
    p.add_argument("--variant", required=True, choices=sorted(VARIANTS.keys()))
    p.add_argument("--window", required=True, choices=sorted(WINDOWS.keys()))
    p.add_argument(
        "--slippage",
        default="MEDIUM",
        choices=[b.value for b in SlippageBucket],
        help="Slippage bucket (default MEDIUM matches baseline).",
    )
    p.add_argument(
        "--stop-trigger",
        default="MARK_PRICE",
        choices=[s.value for s in StopTriggerSource],
        help="Stop-trigger source (default MARK_PRICE matches live protective stops).",
    )
    p.add_argument(
        "--fill-model",
        default="next-bar-open",
        choices=sorted(FILL_MODELS.keys()),
        help=(
            "R2 fill model (default next-bar-open). 'limit-at-pullback' is "
            "DIAGNOSTIC-ONLY per Phase 2v Gate 2 clarification — only valid "
            "for variant=R2+R3 and only used for the §P.6 / run #10 sensitivity. "
            "The committed §F.4 fill model is next-bar-open after confirmation."
        ),
    )
    return p.parse_args()


def main() -> int:
    args = _parse_args()

    variant_id: str = args.variant
    window_id: str = args.window
    slippage_bucket = SlippageBucket(args.slippage)
    stop_trigger = StopTriggerSource(args.stop_trigger)
    fill_model_label: str = args.fill_model
    fill_model_engine = FILL_MODELS[fill_model_label]

    if fill_model_label == "limit-at-pullback" and variant_id != "R2+R3":
        raise RuntimeError(
            "--fill-model limit-at-pullback is only valid for variant=R2+R3 "
            "(diagnostic-only per Phase 2v §P.6 / Gate 2 clarification)."
        )

    variant_cfg = VARIANTS[variant_id]
    window_start_ms, window_end_ms = WINDOWS[window_id]

    experiment_parts: list[str] = []
    if slippage_bucket != SlippageBucket.MEDIUM:
        experiment_parts.append(f"slip={slippage_bucket.value}")
    if stop_trigger != StopTriggerSource.MARK_PRICE:
        experiment_parts.append(f"stop={stop_trigger.value}")
    if fill_model_label != "next-bar-open":
        experiment_parts.append(f"fill={fill_model_label}")
    experiment_suffix = "_".join(experiment_parts) if experiment_parts else "baseline"

    experiment_name = f"phase-2w-r2-{_experiment_label(variant_id)}-{window_id.lower()}"
    if experiment_parts:
        experiment_name = f"{experiment_name}-{experiment_suffix}"
    run_id = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H-%M-%SZ")

    reports_root = DATA_ROOT / "derived" / "backtests"
    run_dir = reports_root / experiment_name / run_id

    _banner(
        f"Phase 2w R2 | variant={variant_id} window={window_id}\n"
        f"  slippage={slippage_bucket.value} stop_trigger={stop_trigger.value}\n"
        f"  fill_model={fill_model_label} (engine={fill_model_engine})\n"
        f"  experiment={experiment_name}\n"
        f"  strategy_variant={variant_cfg.model_dump_json()}"
    )

    klines_root = DATA_ROOT / "normalized" / "klines"
    bars_1h_root = DATA_ROOT / "derived" / "bars_1h" / "standard"
    mark_root = DATA_ROOT / "normalized" / "mark_price_klines"
    funding_root = DATA_ROOT / "normalized" / "funding_rate"
    ei_path = _exchange_info_path()

    k15: dict = {}
    k1h: dict = {}
    m15: dict = {}
    fund: dict = {}
    si_map: dict = {}

    for s in SYMBOLS:
        print(f"\nLoading {s.value}...")
        k15[s] = read_klines(klines_root, symbol=s, interval=Interval.I_15M)
        k1h[s] = read_klines(bars_1h_root, symbol=s, interval=Interval.I_1H)
        m15[s] = read_mark_price_klines(mark_root, symbol=s, interval=Interval.I_15M)
        fund[s] = read_funding_rate_events(funding_root, symbol=s)
        si_map[s] = _load_symbol_info(ei_path, s)
        print(
            f"  15m={len(k15[s]):,}  1h={len(k1h[s]):,}  mark={len(m15[s]):,}  "
            f"funding={len(fund[s]):,}"
        )

    cfg = BacktestConfig(
        experiment_name=experiment_name,
        run_id=run_id,
        symbols=SYMBOLS,
        window_start_ms=window_start_ms,
        window_end_ms=window_end_ms,
        sizing_equity_usdt=10_000.0,
        risk_fraction=0.0025,
        risk_usage_fraction=0.90,
        max_effective_leverage=2.0,
        max_notional_internal_usdt=100_000.0,
        taker_fee_rate=0.0005,
        slippage_bucket=slippage_bucket,
        slippage_bps_map=dict(DEFAULT_SLIPPAGE_BPS),
        klines_root=klines_root,
        bars_1h_root=bars_1h_root,
        mark_price_root=mark_root,
        funding_root=funding_root,
        exchange_info_path=ei_path,
        reports_root=reports_root,
        strategy_variant=variant_cfg,
        stop_trigger_source=stop_trigger,
    )

    _banner("Running engine")
    engine = BacktestEngine(cfg, r2_fill_model=fill_model_engine)
    result = engine.run(
        klines_15m_per_symbol=k15,
        klines_1h_per_symbol=k1h,
        mark_15m_per_symbol=m15,
        funding_per_symbol=fund,
        symbol_info_per_symbol=si_map,
    )
    if result.warnings:
        print(f"Engine warnings: {result.warnings}")

    print(f"\nTotal trades (all symbols): {result.total_trades}")
    for s in SYMBOLS:
        acc = result.accounting_per_symbol.get(s)
        trades = result.per_symbol_trades.get(s, [])
        if acc is None:
            continue
        print(
            f"  {s.value}: {len(trades)} trades | equity {acc.equity:.2f} | "
            f"realized PnL {acc.realized_pnl:+.2f} USDT "
            f"({acc.return_fraction * 100:+.2f}%)"
        )
        # Per-symbol R2 lifecycle counters (zero for non-R2 paths).
        r2c = result.r2_counters_per_symbol.get(s)
        if r2c is not None and r2c.registered > 0:
            print(
                f"    R2 lifecycle: registered={r2c.registered} "
                f"filled={r2c.filled} (rate={r2c.filled / r2c.registered:.2%}); "
                f"cancellations: bias={r2c.cancelled_bias_flip} "
                f"opp={r2c.cancelled_opposite_signal} "
                f"struct={r2c.cancelled_structural_invalidation} "
                f"stop_dist_at_fill={r2c.cancelled_stop_distance_at_fill} "
                f"no_pullback={r2c.expired_no_pullback}; "
                f"identity_holds={r2c.accounting_identity_holds}"
            )

    citations: list[DatasetCitation] = []
    for s in SYMBOLS:
        for dataset, ds_cat in [
            ("15m", "15m"),
            ("1h_derived", "1h derived"),
            ("markprice_15m", "mark-price 15m"),
            ("funding", "funding-rate events"),
        ]:
            ds_name = f"binance_usdm_{s.value.lower()}_{dataset}"
            citations.append(
                DatasetCitation(
                    dataset_name=ds_name,
                    dataset_version=f"{ds_name}__v002",
                    manifest_path=str(DATA_ROOT / "manifests" / f"{ds_name}__v002.manifest.json"),
                    notes=f"{ds_cat} dataset for {s.value}",
                )
            )
    citations.append(
        DatasetCitation(
            dataset_name="exchange_info_snapshot",
            raw_file_path=str(ei_path),
            notes="GAP-20260419-020: 2026-04-19 snapshot proxy for entire range.",
        )
    )

    accepted_limits = [
        f"Phase 2w R2 execution variant={variant_id} window={window_id} "
        f"slippage={slippage_bucket.value} stop_trigger={stop_trigger.value} "
        f"fill_model={fill_model_label}.",
        "R2 spec is single-axis structural redesign per Phase 2u spec memo §B "
        "(Gate 2 amended): conditional-pending pullback-retest entry topology "
        "with sub-parameters committed singularly per §F (pullback level = "
        "setup_high/setup_low; confirmation = close not violating structural "
        "stop; validity window = 8 bars; committed fill model = "
        "next-bar-open after confirmation). Cancellation precedence: "
        "BIAS_FLIP > OPPOSITE_SIGNAL > STRUCTURAL_INVALIDATION > "
        "TOUCH+CONFIRMATION > CONTINUE.",
        "R3 exit baseline locked per Phase 2j memo §D (exit_kind=FIXED_R_TIME_STOP; "
        "R-target=2.0; time-stop=8). Unchanged from Phase 2l/2m/2s.",
        "H0 (control) and R3 (locked control) re-run on the same engine version for "
        "§10.3 promotion comparison; H0 is the sole comparison anchor per Phase 2i §1.7.3.",
        "GAP-20260424-031 (EMA slope definition): R2 does not touch the bias-validity "
        "rule; carried unchanged from Phase 2s.",
        "GAP-20260424-032 (mark-price stop-trigger sensitivity): runs emit "
        "stop_trigger_source in the manifest; promotion includes a TRADE_PRICE pass.",
        "GAP-20260424-033 (R3 unconditional time-stop): inherited from R3.",
        "GAP-20260424-036 (5-rolling-fold consistency): R2 may operate at sample-size "
        "lower bound; per-fold caveats applied descriptively.",
        "GAP-20260419-015 (stop-distance reference price): R2 uses close_B at "
        "registration and actual fill_price at fill-time, both with frozen "
        "atr_at_signal.",
        "Phase 2v Gate 2 amendment: STRUCTURAL_INVALIDATION cancellation reason "
        "added at precedence position 3; limit-at-pullback intrabar fill model "
        "is diagnostic-only and exposed only via this runner-script flag, never "
        "as a V1BreakoutConfig field.",
        "Phase 2g wave-1 REJECT ALL preserved as historical evidence; no comparison-baseline "
        "shifting. Phase 2l R3 PROMOTE preserved. Phase 2m R1a+R3 mixed PROMOTE preserved as "
        "non-leading research evidence. Phase 2s R1b-narrow PROMOTE / PASS preserved.",
        "Run is descriptive comparison evidence; NOT a live-readiness or promotion claim.",
    ]

    written_dir = write_report(
        config=cfg,
        trades_by_symbol=result.per_symbol_trades,
        accounting_by_symbol=result.accounting_per_symbol,
        dataset_citations=citations,
        accepted_limitations=accepted_limits,
        dest_root=reports_root,
    )
    assert written_dir == run_dir, f"expected {run_dir}, got {written_dir}"
    print(f"\nReport written to: {run_dir}")

    _banner("Signal-funnel and per-symbol breakdowns")
    for s in SYMBOLS:
        trades = result.per_symbol_trades.get(s, [])
        sym_dir = run_dir / s.value
        sym_dir.mkdir(parents=True, exist_ok=True)

        monthly = _aggregate_trades_by_month(trades)
        yearly = _aggregate_trades_by_year(trades)
        pq.write_table(monthly, sym_dir / "monthly_breakdown.parquet")
        pq.write_table(yearly, sym_dir / "yearly_breakdown.parquet")
        print(
            f"  {s.value}: monthly_breakdown.parquet rows={monthly.num_rows}, "
            f"yearly_breakdown.parquet rows={yearly.num_rows}"
        )

        funnel = run_signal_funnel(
            symbol=s,
            klines_15m=k15[s],
            klines_1h=k1h[s],
            symbol_info=si_map[s],
            config=cfg,
            strategy_config=variant_cfg,
        )
        (sym_dir / "funnel_total.json").write_text(
            json.dumps(_funnel_summary_dict(funnel), indent=2, sort_keys=True)
        )

        # R2 lifecycle counters sidecar (for the §P.1 fill-rate diagnostic).
        # Always emitted; counts are 0 for non-R2 paths.
        r2c = result.r2_counters_per_symbol.get(s)
        if r2c is not None:
            (sym_dir / "r2_lifecycle_total.json").write_text(
                json.dumps(_r2_lifecycle_dict(r2c, s), indent=2, sort_keys=True)
            )

        print(funnel.summary())
        print("")

    _banner(f"Phase 2w R2 run complete. run_id={run_id}")
    print(f"Output: {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
