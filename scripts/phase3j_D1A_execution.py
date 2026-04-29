"""Phase 3j D1-A (funding-aware directional / carry-aware) execution runner.

Phase 3j scope: execute the Phase 3h §10 precommitted D1-A run inventory
against the locked v002 datasets, write per-run trade logs / summary
metrics / lifecycle counters, and produce the artifacts the Phase 3j
analysis script consumes for the §11 first-execution gate, §12
mechanism checks (M1 / M2 / M3), §13 mandatory diagnostics, and §14
P.14 hard-block invariants.

Run inventory per Phase 3h §10 (precommitted; no expansion):

    1. D1-A   R MED  MARK_PRICE     (governing first D1-A run)
    2. D1-A   R LOW  MARK_PRICE     (LOW cost-sensitivity)
    3. D1-A   R HIGH MARK_PRICE     (§11.6 HIGH cost-sensitivity gate)
    4. D1-A   R MED  TRADE_PRICE    (stop-trigger sensitivity)
    5. D1-A   V MED  MARK_PRICE     (conditional on PROMOTE outcome)

Phase 3i-B1 added the Phase 3j authorization guard. Phase 3j operates
under operator authorization and runs D1-A candidates by passing
``--phase-3j-authorized`` on each invocation.

Usage::

    uv run python scripts/phase3j_D1A_execution.py check-imports
    uv run python scripts/phase3j_D1A_execution.py d1a --window R \\
        --slippage MED --stop-trigger MARK_PRICE \\
        --phase-3j-authorized

Per the Phase 3i-B1 brief and Phase 3h §3, this runner does NOT modify
the D1-A spec axes (Z-threshold |Z_F| ≥ 2.0 / lookback 90 days /
events 270 / stop multiplier 1.0 × ATR / target +2.0R / time-stop 32 /
band [0.60, 1.80] / cooldown per_funding_event / direction contrarian
/ no regime filter). All axes come from the locked
``FundingAwareConfig`` defaults.
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
from prometheus.research.backtest.engine import FundingAwareLifecycleCounters
from prometheus.research.backtest.report import DatasetCitation, write_report
from prometheus.research.backtest.trade_log import TradeRecord
from prometheus.research.data.storage import (
    read_funding_rate_events,
    read_klines,
    read_mark_price_klines,
)
from prometheus.strategy.funding_aware_directional import (
    FundingAwareConfig,
    FundingAwareStrategy,
)

PHASE_3J_AUTHORIZATION_FLAG = "--phase-3j-authorized"

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"

SYMBOLS = (Symbol.BTCUSDT, Symbol.ETHUSDT)

# Window boundaries identical to Phase 2l / Phase 3d (Phase 2f Gate 1 §11.1):
#   R: 2022-01-01 .. 2025-01-01 (exclusive)  =  36 months
#   V: 2025-01-01 .. 2026-04-01 (exclusive)  =  15 months
WINDOWS: dict[str, tuple[int, int]] = {
    "R": (1_640_995_200_000, 1_735_689_600_000),
    "V": (1_735_689_600_000, 1_775_001_600_000),
}

SLIPPAGE_ALIASES: dict[str, SlippageBucket] = {
    "LOW": SlippageBucket.LOW,
    "MED": SlippageBucket.MEDIUM,
    "MEDIUM": SlippageBucket.MEDIUM,
    "HIGH": SlippageBucket.HIGH,
}


# ---------------------------------------------------------------------------
# Sanity action — verify the D1-A engine surface imports cleanly.
# ---------------------------------------------------------------------------


def _check_imports() -> int:
    cfg = FundingAwareConfig()
    strat = FundingAwareStrategy(cfg)
    counters = FundingAwareLifecycleCounters()
    print(
        f"D1-A engine surface imports OK: "
        f"family={StrategyFamily.FUNDING_AWARE_DIRECTIONAL.value} "
        f"variant_locked=z_threshold={cfg.funding_z_score_threshold} "
        f"lookback_events={cfg.funding_z_score_lookback_events} "
        f"target_r={cfg.target_r_multiple} time_stop={cfg.time_stop_bars} "
        f"strategy={strat.__class__.__name__} "
        f"counters_default_identity={counters.accounting_identity_holds} "
        f"engine_class={BacktestEngine.__name__}"
    )
    return 0


# ---------------------------------------------------------------------------
# Helpers (mirrored from scripts/phase3d_F1_execution.py for consistency).
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
    """Monthly per-symbol breakdown for D1-A.

    D1-A emits only STOP / TARGET / TIME_STOP / END_OF_DATA exit
    reasons. V1-only TRAILING_BREACH / STAGNATION / TAKE_PROFIT
    columns are kept as zeros for schema-shape compatibility with the
    Phase 2l reports.
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
        # D1-A must never emit TRAILING_BREACH / STAGNATION / TAKE_PROFIT;
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


def _d1a_lifecycle_dict(c: FundingAwareLifecycleCounters, symbol: Symbol) -> dict[str, object]:
    return {
        "symbol": symbol.value,
        "funding_extreme_events_detected": c.funding_extreme_events_detected,
        "funding_extreme_events_filled": c.funding_extreme_events_filled,
        "funding_extreme_events_rejected_stop_distance": (
            c.funding_extreme_events_rejected_stop_distance
        ),
        "funding_extreme_events_blocked_cooldown": c.funding_extreme_events_blocked_cooldown,
        "accounting_identity_holds": c.accounting_identity_holds,
    }


def _summary_metrics_dict_d1a(
    trades: list[TradeRecord], starting_equity: float
) -> dict[str, object]:
    """Compact per-symbol summary metrics for a D1-A run.

    Mirrors the Phase 3d F1 ``_summary_metrics_dict_f1`` shape: TARGET
    (not TAKE_PROFIT), no TRAILING_BREACH / STAGNATION columns.
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
# D1-A run-loop (Phase 3j).
# ---------------------------------------------------------------------------


def _run_d1a(args: argparse.Namespace) -> int:
    if not getattr(args, "phase_3j_authorized", False):
        print(
            "D1-A candidate execution requires Phase 3j authorization.\n"
            f"Pass {PHASE_3J_AUTHORIZATION_FLAG} only after operator approval.",
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

    experiment_name = "phase-3j-d1a-" + "-".join(experiment_parts)
    run_id = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    reports_root = DATA_ROOT / "derived" / "backtests"
    run_dir = reports_root / experiment_name / run_id

    _banner(
        f"Phase 3j D1-A execution | window={window_id} "
        f"slippage={slippage_bucket.value} stop_trigger={stop_trigger.value}\n"
        f"  experiment={experiment_name}\n"
        f"  variant=FundingAwareConfig() (locked Phase 3g §6 + §5.6.5 Option A)"
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
        strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
        funding_aware_variant=FundingAwareConfig(),
        stop_trigger_source=stop_trigger,
    )

    _banner("Running D1-A engine")
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

    print(f"\nTotal D1-A trades (all symbols): {result.total_trades}")
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
        f"Phase 3j D1-A first-execution variant=D1-A window={window_id} "
        f"slippage={slippage_bucket.value} stop_trigger={stop_trigger.value}.",
        "D1-A spec is locked verbatim per Phase 3g sec.6 + sec.5.6.5 Option A "
        "(|Z_F| >= 2.0 over trailing 90 days / 270 events; current event "
        "excluded from rolling mean/std; 1.0 x ATR(20) stop; +2.0R TARGET; "
        "32-bar time-stop; per-funding-event cooldown; band [0.60, 1.80] x "
        "ATR(20); contrarian direction; no regime filter). No tuning, sweeps, "
        "alternatives, or D1-A-prime variants in Phase 3j.",
        "D1-A family is self-anchored absolute per Phase 3h sec.11. H0/R3/F1 "
        "are descriptive cross-family references only.",
        "BTC HIGH-slip expR > 0 + PF > 0.30 is the Phase 3h sec.11.2 cost-"
        "resilience gate; failure with M1 PASS classifies MECHANISM PASS / "
        "FRAMEWORK FAIL - sec.11.6 cost-sensitivity blocks (Phase 3h "
        "sec.11.2).",
        "Run is research-only descriptive evidence; NOT a live-readiness or "
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

    _banner("D1-A per-symbol breakdowns + lifecycle counters")
    for s in SYMBOLS:
        trades = result.per_symbol_trades.get(s, [])
        sym_dir = run_dir / s.value
        sym_dir.mkdir(parents=True, exist_ok=True)

        # Override the report's auto-written summary_metrics with the
        # D1-A-aware version that uses TARGET (not TAKE_PROFIT) and
        # omits TRAILING_BREACH / STAGNATION columns.
        starting_equity = float(result.accounting_per_symbol[s].starting_equity)
        d1a_summary = _summary_metrics_dict_d1a(trades, starting_equity)
        (sym_dir / "summary_metrics.json").write_text(
            json.dumps(d1a_summary, indent=2, sort_keys=True)
        )

        monthly = _aggregate_trades_by_month(trades)
        pq.write_table(monthly, sym_dir / "monthly_breakdown.parquet")

        d1ac = result.funding_aware_counters_per_symbol.get(s)
        if d1ac is not None:
            (sym_dir / "funding_aware_lifecycle_total.json").write_text(
                json.dumps(_d1a_lifecycle_dict(d1ac, s), indent=2, sort_keys=True)
            )
        print(
            f"  {s.value}: trades={len(trades)} "
            f"target={d1a_summary['target_exits']} "
            f"stop={d1a_summary['stop_exits']} "
            f"time_stop={d1a_summary['time_stop_exits']} "
            f"eod={d1a_summary['end_of_data_exits']} "
            f"expR={d1a_summary['expectancy_r']:.4f} "
            f"PF={d1a_summary['profit_factor']:.4f}"
        )

    _banner(f"Phase 3j D1-A run complete. run_id={run_id}")
    print(f"Output: {run_dir}")
    return 0


# ---------------------------------------------------------------------------
# CLI plumbing.
# ---------------------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Phase 3j D1-A execution runner. Guarded by "
            f"{PHASE_3J_AUTHORIZATION_FLAG}; fails closed without it."
        ),
    )
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser(
        "check-imports",
        help="Verify the D1-A engine surface imports cleanly without running anything.",
    )
    d1a_parser = sub.add_parser(
        "d1a",
        help="Execute a D1-A candidate backtest cell (Phase 3j; guarded).",
    )
    d1a_parser.add_argument(
        "--window",
        choices=("R", "V"),
        required=True,
        help="R = 2022-01-01..2025-01-01; V = 2025-01-01..2026-04-01.",
    )
    d1a_parser.add_argument(
        "--slippage",
        choices=("LOW", "MED", "MEDIUM", "HIGH"),
        default="MED",
        help="Slippage bucket per Phase 2y (LOW=1bps, MED=3bps, HIGH=8bps per side).",
    )
    d1a_parser.add_argument(
        "--stop-trigger",
        choices=("MARK_PRICE", "TRADE_PRICE"),
        default="MARK_PRICE",
        help="Stop-trigger source per §1.7.3 (MARK_PRICE default; TRADE_PRICE diagnostic).",
    )
    d1a_parser.add_argument(
        PHASE_3J_AUTHORIZATION_FLAG,
        dest="phase_3j_authorized",
        action="store_true",
        help="Required: explicit Phase 3j operator authorization flag.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_argparser()
    args = parser.parse_args(argv)
    if args.action == "check-imports":
        return _check_imports()
    if args.action == "d1a":
        return _run_d1a(args)
    parser.error(f"unknown action: {args.action!r}")
    return 64


if __name__ == "__main__":
    raise SystemExit(main())
