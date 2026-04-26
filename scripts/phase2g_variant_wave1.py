"""Phase 2g wave-1 variant runner.

Runs the four operator-approved variants plus the H0 baseline control
against the existing Phase 2e v002 datasets:

    H0    — baseline (V1BreakoutConfig defaults)
    H-A1  — setup window 8 -> 10
    H-C1  — HTF EMA pair 50/200 -> 20/100
    H-B2  — breakout expansion threshold 1.0 -> 0.75 × ATR20
    H-D3  — break-even threshold +1.5 R -> +2.0 R

Per Phase 2f/2g Gate 1:

  - Research-only. No live trading, no exchange adapter, no keys.
  - Same v002 datasets as Phase 2e. No data downloads.
  - Same baseline cost/funding/slippage assumptions unless a sensitivity
    override is explicitly supplied.
  - One variant per invocation (positional), emitting a distinct
    per-variant run directory under data/derived/backtests/phase-2g-wave1/.
  - Baseline artifacts from Phase 2e remain untouched and serve as the
    permanent control.

Usage::

    uv run python scripts/phase2g_variant_wave1.py --variant H-A1 --window R
    uv run python scripts/phase2g_variant_wave1.py --variant H0   --window V
    uv run python scripts/phase2g_variant_wave1.py --variant H-D3 --window R \\
        --slippage HIGH
    uv run python scripts/phase2g_variant_wave1.py --variant H-D3 --window R \\
        --stop-trigger TRADE_PRICE

Output directory::

    data/derived/backtests/phase-2g-wave1/<variant>/<window>/<experiment>/<run_id>/
        <SYMBOL>/
            trade_log.{parquet,json}
            summary_metrics.json
            funnel_total.json
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
from prometheus.research.backtest.report import DatasetCitation, write_report
from prometheus.research.backtest.trade_log import TradeRecord
from prometheus.research.data.storage import (
    read_funding_rate_events,
    read_klines,
    read_mark_price_klines,
)
from prometheus.strategy.v1_breakout import V1BreakoutConfig

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"

SYMBOLS = (Symbol.BTCUSDT, Symbol.ETHUSDT)

# Window boundaries per Phase 2f Gate 1 §11.1
# R: 2022-01-01 .. 2025-01-01 (exclusive) = 36 months
# V: 2025-01-01 .. 2026-04-01 (exclusive) = 15 months
# FULL: 2022-01-01 .. 2026-04-01 (exclusive) = 51 months (matches Phase 2e)
WINDOWS: dict[str, tuple[int, int]] = {
    "R": (1_640_995_200_000, 1_735_689_600_000),  # 2022-01-01 -> 2025-01-01
    "V": (1_735_689_600_000, 1_775_001_600_000),  # 2025-01-01 -> 2026-04-01
    "FULL": (1_640_995_200_000, 1_775_001_600_000),
}

# Four wave-1 variants + the H0 control. Single-axis changes only.
VARIANTS: dict[str, V1BreakoutConfig] = {
    "H0": V1BreakoutConfig(),
    "H-A1": V1BreakoutConfig(setup_size=10),
    "H-B2": V1BreakoutConfig(expansion_atr_mult=0.75),
    "H-C1": V1BreakoutConfig(ema_fast=20, ema_slow=100),
    "H-D3": V1BreakoutConfig(break_even_r=2.0),
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
    """Mirror the Phase 2e runner's minimal funnel dict exactly."""
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


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 2g wave-1 variant runner")
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
    return p.parse_args()


def main() -> int:
    args = _parse_args()

    variant_id: str = args.variant
    window_id: str = args.window
    slippage_bucket = SlippageBucket(args.slippage)
    stop_trigger = StopTriggerSource(args.stop_trigger)

    variant_cfg = VARIANTS[variant_id]
    window_start_ms, window_end_ms = WINDOWS[window_id]

    # Compact experiment-name segment encoding non-default knobs so the
    # directory tree stays readable. Baseline knobs are omitted.
    experiment_parts: list[str] = []
    if slippage_bucket != SlippageBucket.MEDIUM:
        experiment_parts.append(f"slip={slippage_bucket.value}")
    if stop_trigger != StopTriggerSource.MARK_PRICE:
        experiment_parts.append(f"stop={stop_trigger.value}")
    experiment_suffix = "_".join(experiment_parts) if experiment_parts else "baseline"

    experiment_name = f"phase-2g-wave1-{variant_id.lower()}-{window_id.lower()}"
    if experiment_parts:
        experiment_name = f"{experiment_name}-{experiment_suffix}"
    run_id = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H-%M-%SZ")

    reports_root = DATA_ROOT / "derived" / "backtests"
    run_dir = reports_root / experiment_name / run_id

    _banner(
        f"Phase 2g wave-1 | variant={variant_id} window={window_id}\n"
        f"  slippage={slippage_bucket.value} stop_trigger={stop_trigger.value}\n"
        f"  experiment={experiment_name}\n"
        f"  strategy_variant={variant_cfg.model_dump_json()}"
    )

    # Load inputs via Hive-partitioned storage helpers (shared across variants).
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
    engine = BacktestEngine(cfg)
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
        f"Phase 2g wave-1 variant={variant_id} window={window_id} "
        f"slippage={slippage_bucket.value} stop_trigger={stop_trigger.value}.",
        "Strategy variant applied per Phase 2f Gate 1 plan wave-1 selection. "
        "Single-axis change from H0. All other thresholds inherit the locked Phase 3 defaults.",
        "GAP-20260424-031 (EMA slope definition): memo adopts discrete comparison "
        "EMA[now] > EMA[now-3 completed 1h bars], consistent with current implementation.",
        "GAP-20260424-032 (mark-price stop-trigger sensitivity): Phase 2g adds "
        "an explicit TRADE_PRICE switch; runs emit stop_trigger_source in the manifest.",
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
        print(funnel.summary())
        print("")

    _banner(f"Phase 2g wave-1 run complete. run_id={run_id}")
    print(f"Output: {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
