"""Phase 3d F1 (mean-reversion-after-overextension) execution runner.

Phase 3d-B2 scope: execute the precommitted F1 run inventory from
Phase 3c §6 against the locked v002 datasets, write per-run trade
logs / summary metrics / lifecycle counters, and produce the
artifacts the Phase 3d-B2 analysis script consumes for the §7.2
first-execution gate, §9 mechanism checks, and §8 mandatory
diagnostics.

Run inventory per Phase 3c §6 (precommitted; no expansion)::

    1. F1   R MED  MARK_PRICE     (governing first F1 run)
    2. F1   R LOW  MARK_PRICE     (§11.6 cost-sensitivity LOW)
    3. F1   R HIGH MARK_PRICE     (§11.6 HIGH cost-sensitivity gate)
    4. F1   R MED  TRADE_PRICE    (stop-trigger sensitivity)
    5. F1   V MED  MARK_PRICE     (conditional on §7.2 PROMOTE)

Phase 3d-B1 added the Phase 3d-B2 authorization guard. Phase 3d-B2
operates under operator authorization and runs F1 candidates by
passing ``--phase-3d-b2-authorized`` on each invocation.

Usage::

    uv run python scripts/phase3d_F1_execution.py check-imports
    uv run python scripts/phase3d_F1_execution.py f1 --window R \
        --slippage MED --stop-trigger MARK_PRICE \
        --phase-3d-b2-authorized

The ``check-imports`` action verifies the F1 engine surface imports
cleanly (legacy Phase 3d-B1 sanity check). The ``f1`` action runs the
selected cell and writes its artifacts under the
``data/derived/backtests/phase-3d-f1-*/`` tree (git-ignored).

Per the Phase 3d-B1 brief and Phase 3c §3, this runner does NOT modify
the F1 spec axes (overextension window 8 / threshold 1.75 / mean-window
8 / stop-buffer 0.10 / time-stop 8 / band [0.60, 1.80]). All seven
axes come from the locked ``MeanReversionConfig`` defaults.
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
    SlippageBucket,
    StopTriggerSource,
)
from prometheus.research.backtest.config import DEFAULT_SLIPPAGE_BPS, StrategyFamily
from prometheus.research.backtest.engine import F1LifecycleCounters
from prometheus.research.backtest.report import DatasetCitation, write_report
from prometheus.research.backtest.trade_log import TradeRecord
from prometheus.research.data.storage import (
    read_funding_rate_events,
    read_klines,
    read_mark_price_klines,
)
from prometheus.strategy.mean_reversion_overextension import (
    MeanReversionConfig,
    MeanReversionStrategy,
)

PHASE_3D_B2_AUTHORIZATION_FLAG = "--phase-3d-b2-authorized"

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"

SYMBOLS = (Symbol.BTCUSDT, Symbol.ETHUSDT)

# Window boundaries identical to Phase 2l (Phase 2f Gate 1 §11.1):
#   R: 2022-01-01 .. 2025-01-01 (exclusive)  =  36 months
#   V: 2025-01-01 .. 2026-04-01 (exclusive)  =  15 months
WINDOWS: dict[str, tuple[int, int]] = {
    "R": (1_640_995_200_000, 1_735_689_600_000),
    "V": (1_735_689_600_000, 1_775_001_600_000),
}

# Friendly slippage label aliases expected by the Phase 3c §6 inventory
# language (LOW / MED / HIGH map to LOW / MEDIUM / HIGH).
SLIPPAGE_ALIASES: dict[str, SlippageBucket] = {
    "LOW": SlippageBucket.LOW,
    "MED": SlippageBucket.MEDIUM,
    "MEDIUM": SlippageBucket.MEDIUM,
    "HIGH": SlippageBucket.HIGH,
}


# ---------------------------------------------------------------------------
# Phase 3d-B1 sanity action — preserved unchanged for backward compatibility.
# ---------------------------------------------------------------------------


def _check_imports() -> int:
    cfg = MeanReversionConfig()
    strat = MeanReversionStrategy(cfg)
    counters = F1LifecycleCounters()
    print(
        f"OK Phase 3d-B1 F1 engine surface: "
        f"family={StrategyFamily.MEAN_REVERSION_OVEREXTENSION.value} "
        f"variant_locked=overext_window={cfg.overextension_window_bars} "
        f"threshold_atr={cfg.overextension_threshold_atr_multiple} "
        f"strategy={strat.__class__.__name__} "
        f"counters_default_identity={counters.accounting_identity_holds} "
        f"engine_class={BacktestEngine.__name__}"
    )
    return 0


# ---------------------------------------------------------------------------
# Helpers shared with Phase 2l-style runners (tabulation, exchange info).
# ---------------------------------------------------------------------------


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
    """Monthly per-symbol breakdown for F1 (STOP / TARGET / TIME_STOP /
    END_OF_DATA exit reasons only; V1-only TRAILING_BREACH /
    STAGNATION / TAKE_PROFIT columns kept as zeros for schema-shape
    compatibility with the Phase 2l reports).
    """
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
            "target_exits": 0,
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
        elif t.exit_reason == "TARGET":
            row["target_exits"] = int(row["target_exits"]) + 1
        elif t.exit_reason == "TIME_STOP":
            row["time_stop_exits"] = int(row["time_stop_exits"]) + 1
        elif t.exit_reason == "END_OF_DATA":
            row["end_of_data_exits"] = int(row["end_of_data_exits"]) + 1
        # F1 must never emit TRAILING_BREACH / STAGNATION / TAKE_PROFIT;
        # the P.14 hard-block check verifies this independently.
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


def _f1_lifecycle_dict(c: F1LifecycleCounters, symbol: Symbol) -> dict[str, object]:
    return {
        "symbol": symbol.value,
        "overextension_events_detected": c.overextension_events_detected,
        "overextension_events_filled": c.overextension_events_filled,
        "overextension_events_rejected_stop_distance": (
            c.overextension_events_rejected_stop_distance
        ),
        "overextension_events_blocked_cooldown": c.overextension_events_blocked_cooldown,
        "accounting_identity_holds": c.accounting_identity_holds,
    }


def _summary_metrics_dict_f1(
    trades: list[TradeRecord], starting_equity: float
) -> dict[str, object]:
    """Compact per-symbol summary metrics for an F1 run.

    Mirrors the Phase 2 ``compute_summary_metrics`` shape but uses the
    F1 exit-reason taxonomy (TARGET instead of TAKE_PROFIT and no
    TRAILING_BREACH / STAGNATION).
    """
    n = len(trades)
    if n == 0:
        return {
            "trade_count": 0,
            "win_count": 0,
            "loss_count": 0,
            "win_rate": 0.0,
            "expectancy_r": 0.0,
            "profit_factor": 0.0,
            "total_net_pnl_usdt": 0.0,
            "total_return_fraction": 0.0,
            "max_drawdown_usdt": 0.0,
            "max_drawdown_fraction": 0.0,
            "long_count": 0,
            "short_count": 0,
            "stop_exits": 0,
            "target_exits": 0,
            "time_stop_exits": 0,
            "end_of_data_exits": 0,
            "total_fees_usdt": 0.0,
            "total_funding_usdt": 0.0,
            "gap_through_stops": 0,
        }
    wins = [t for t in trades if t.net_pnl > 0]
    losses = [t for t in trades if t.net_pnl < 0]
    win_rate = len(wins) / n
    expectancy_r = sum(t.net_r_multiple for t in trades) / n
    gross_win = sum(t.net_pnl for t in wins)
    gross_loss = -sum(t.net_pnl for t in losses)
    profit_factor = (
        (gross_win / gross_loss) if gross_loss > 0 else float("inf") if gross_win > 0 else 0.0
    )
    total_net = sum(t.net_pnl for t in trades)
    total_fees = sum(t.entry_fee + t.exit_fee for t in trades)
    total_funding = sum(t.funding_pnl for t in trades)
    long_count = sum(1 for t in trades if t.direction == "LONG")
    short_count = sum(1 for t in trades if t.direction == "SHORT")
    stop_exits = sum(1 for t in trades if t.exit_reason == "STOP")
    target_exits = sum(1 for t in trades if t.exit_reason == "TARGET")
    time_stop_exits = sum(1 for t in trades if t.exit_reason == "TIME_STOP")
    end_exits = sum(1 for t in trades if t.exit_reason == "END_OF_DATA")
    gap_through = sum(1 for t in trades if t.stop_was_gap_through)

    # Equity / drawdown via Phase 2 helpers for consistency.
    from prometheus.research.backtest.report import (
        compute_drawdown_series,
        compute_equity_curve,
    )

    equity_table = compute_equity_curve(trades, starting_equity)
    dd_table = compute_drawdown_series(equity_table)
    if dd_table.num_rows > 0:
        max_dd = min(dd_table.column("drawdown_usdt").to_pylist())
        max_dd_frac = min(dd_table.column("drawdown_fraction").to_pylist())
    else:
        max_dd = 0.0
        max_dd_frac = 0.0

    return {
        "trade_count": n,
        "win_count": len(wins),
        "loss_count": len(losses),
        "win_rate": win_rate,
        "expectancy_r": expectancy_r,
        "profit_factor": profit_factor,
        "total_net_pnl_usdt": total_net,
        "total_return_fraction": total_net / starting_equity,
        "max_drawdown_usdt": max_dd,
        "max_drawdown_fraction": max_dd_frac,
        "long_count": long_count,
        "short_count": short_count,
        "stop_exits": stop_exits,
        "target_exits": target_exits,
        "time_stop_exits": time_stop_exits,
        "end_of_data_exits": end_exits,
        "total_fees_usdt": total_fees,
        "total_funding_usdt": total_funding,
        "gap_through_stops": gap_through,
    }


# ---------------------------------------------------------------------------
# F1 run-loop (Phase 3d-B2).
# ---------------------------------------------------------------------------


def _run_f1(args: argparse.Namespace) -> int:
    if not getattr(args, "phase_3d_b2_authorized", False):
        print(
            "F1 candidate backtest execution requires Phase 3d-B2 authorization.\n"
            f"Pass {PHASE_3D_B2_AUTHORIZATION_FLAG} only after operator approval.",
            file=sys.stderr,
        )
        return 2

    window_id: str = args.window
    slippage_bucket = SLIPPAGE_ALIASES[args.slippage]
    stop_trigger = StopTriggerSource(args.stop_trigger)
    window_start_ms, window_end_ms = WINDOWS[window_id]

    experiment_parts: list[str] = [f"window={window_id.lower()}"]
    experiment_parts.append(f"slip={slippage_bucket.value.lower()}")
    if stop_trigger != StopTriggerSource.MARK_PRICE:
        experiment_parts.append(f"stop={stop_trigger.value.lower()}")

    experiment_name = "phase-3d-f1-" + "-".join(experiment_parts)
    run_id = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    reports_root = DATA_ROOT / "derived" / "backtests"
    run_dir = reports_root / experiment_name / run_id

    _banner(
        f"Phase 3d-B2 F1 execution | window={window_id} "
        f"slippage={slippage_bucket.value} stop_trigger={stop_trigger.value}\n"
        f"  experiment={experiment_name}\n"
        f"  variant=MeanReversionConfig() (locked Phase 3b §4)"
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
        strategy_family=StrategyFamily.MEAN_REVERSION_OVEREXTENSION,
        mean_reversion_variant=MeanReversionConfig(),
        stop_trigger_source=stop_trigger,
    )

    _banner("Running F1 engine")
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

    print(f"\nTotal F1 trades (all symbols): {result.total_trades}")
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
        f"Phase 3d-B2 F1 first-execution variant=F1 window={window_id} "
        f"slippage={slippage_bucket.value} stop_trigger={stop_trigger.value}.",
        "F1 spec is locked verbatim per Phase 3b sec.4 (overextension window=8; "
        "threshold=1.75 ATR; mean reference SMA(8) frozen at signal close; "
        "stop buffer=0.10 ATR; time-stop=8 bars; band=[0.60, 1.80] ATR). No "
        "tuning, sweeps, alternatives, or F1-prime variants in Phase 3d-B2.",
        "F1 family is self-anchored absolute per Phase 3c sec.7. H0/R3 are "
        "descriptive cross-family references only (Phase 3c sec.7.4 / sec.11.9).",
        "BTC HIGH-slip expR > 0 is the Phase 3c sec.7.2(iv) cost-resilience gate; "
        "BTC HIGH expR <= 0 with M1 PASS classifies MECHANISM PASS / FRAMEWORK "
        "FAIL - sec.11.6 cost-sensitivity blocks (Phase 3c sec.7.3).",
        "Run is descriptive comparison evidence; NOT a live-readiness or "
        "promotion claim. No paper/shadow / Phase 4 / live-readiness / "
        "deployment / production-key / exchange-write authorized.",
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

    _banner("F1 per-symbol breakdowns + lifecycle counters")
    for s in SYMBOLS:
        trades = result.per_symbol_trades.get(s, [])
        sym_dir = run_dir / s.value
        sym_dir.mkdir(parents=True, exist_ok=True)

        # Override the report's auto-written summary_metrics with the
        # F1-aware version that uses TARGET (not TAKE_PROFIT) and omits
        # TRAILING_BREACH / STAGNATION columns.
        starting_equity = float(result.accounting_per_symbol[s].starting_equity)
        f1_summary = _summary_metrics_dict_f1(trades, starting_equity)
        (sym_dir / "summary_metrics.json").write_text(
            json.dumps(f1_summary, indent=2, sort_keys=True)
        )

        monthly = _aggregate_trades_by_month(trades)
        pq.write_table(monthly, sym_dir / "monthly_breakdown.parquet")

        f1c = result.f1_counters_per_symbol.get(s)
        if f1c is not None:
            (sym_dir / "f1_lifecycle_total.json").write_text(
                json.dumps(_f1_lifecycle_dict(f1c, s), indent=2, sort_keys=True)
            )
        print(
            f"  {s.value}: trades={len(trades)} "
            f"target={f1_summary['target_exits']} "
            f"stop={f1_summary['stop_exits']} "
            f"time_stop={f1_summary['time_stop_exits']} "
            f"eod={f1_summary['end_of_data_exits']} "
            f"expR={f1_summary['expectancy_r']:.4f} PF={f1_summary['profit_factor']:.4f}"
        )

    _banner(f"Phase 3d-B2 F1 run complete. run_id={run_id}")
    print(f"Output: {run_dir}")
    return 0


# ---------------------------------------------------------------------------
# CLI plumbing.
# ---------------------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="phase3d_F1_execution",
        description="Phase 3d F1 execution runner.",
    )
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("check-imports", help="Verify F1 engine surface imports cleanly.")
    f1_parser = sub.add_parser(
        "f1",
        help="Execute an F1 candidate backtest cell (Phase 3d-B2; guarded).",
    )
    f1_parser.add_argument(
        "--window",
        choices=("R", "V"),
        required=True,
        help="R-window or V-window (V conditional on PROMOTE per §11.3).",
    )
    f1_parser.add_argument(
        "--slippage",
        choices=("LOW", "MED", "MEDIUM", "HIGH"),
        default="MED",
    )
    f1_parser.add_argument(
        "--stop-trigger",
        choices=("MARK_PRICE", "TRADE_PRICE"),
        default="MARK_PRICE",
    )
    f1_parser.add_argument(
        PHASE_3D_B2_AUTHORIZATION_FLAG,
        dest="phase_3d_b2_authorized",
        action="store_true",
        help="Required to run any F1 backtest cell.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_argparser()
    args = parser.parse_args(argv)
    if args.action == "check-imports":
        return _check_imports()
    if args.action == "f1":
        return _run_f1(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
