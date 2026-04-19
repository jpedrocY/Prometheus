"""Thin CLI for invoking backtest runs from the shell.

Usage::

    uv run python -m prometheus.research.backtest.cli \
        --experiment example --run-id test-2026-03 \
        --symbols BTCUSDT,ETHUSDT \
        --klines-root data/normalized/klines \
        --bars-1h-root data/derived/bars_1h/standard \
        --mark-root data/normalized/mark_price_klines \
        --funding-root data/normalized/funding_rate \
        --exchange-info data/derived/exchange_info/2026-04-19T21-22-59Z.json \
        --reports-root data/derived/backtests

The CLI is deliberately narrow. It exists so operator-run smoke
checks on real data can be invoked in one command; nothing here is
part of any automated default-run pytest path (per Gate 1 condition
A, simulation tests use synthetic fixtures and skip real-data when
the files are absent).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from prometheus.core.symbols import Symbol

from .config import BacktestAdapter, BacktestConfig, SlippageBucket


def _parse_symbols(raw: str) -> tuple[Symbol, ...]:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise argparse.ArgumentTypeError("--symbols must list at least one symbol")
    try:
        return tuple(Symbol(p) for p in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m prometheus.research.backtest.cli",
        description="Run a Prometheus v1 breakout backtest (research-only).",
    )
    p.add_argument("--experiment", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--symbols", required=True, type=_parse_symbols)
    p.add_argument("--window-start-ms", required=True, type=int)
    p.add_argument("--window-end-ms", required=True, type=int)
    p.add_argument("--sizing-equity", type=float, default=10_000.0)
    p.add_argument("--risk-fraction", type=float, default=0.0025)
    p.add_argument("--risk-usage", type=float, default=0.90)
    p.add_argument("--max-leverage", type=float, default=2.0)
    p.add_argument("--notional-cap", type=float, default=100_000.0)
    p.add_argument("--fee-rate", type=float, default=0.0005)
    p.add_argument(
        "--slippage", type=lambda s: SlippageBucket(s.upper()), default=SlippageBucket.MEDIUM
    )
    p.add_argument("--klines-root", required=True, type=Path)
    p.add_argument("--bars-1h-root", required=True, type=Path)
    p.add_argument("--mark-root", required=True, type=Path)
    p.add_argument("--funding-root", required=True, type=Path)
    p.add_argument("--exchange-info", required=True, type=Path)
    p.add_argument("--reports-root", required=True, type=Path)
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config and print it without running the engine.",
    )
    return p


def config_from_args(args: argparse.Namespace) -> BacktestConfig:
    return BacktestConfig(
        experiment_name=args.experiment,
        run_id=args.run_id,
        symbols=args.symbols,
        window_start_ms=args.window_start_ms,
        window_end_ms=args.window_end_ms,
        sizing_equity_usdt=args.sizing_equity,
        risk_fraction=args.risk_fraction,
        risk_usage_fraction=args.risk_usage,
        max_effective_leverage=args.max_leverage,
        max_notional_internal_usdt=args.notional_cap,
        taker_fee_rate=args.fee_rate,
        slippage_bucket=args.slippage,
        klines_root=args.klines_root,
        mark_price_root=args.mark_root,
        funding_root=args.funding_root,
        bars_1h_root=args.bars_1h_root,
        exchange_info_path=args.exchange_info,
        reports_root=args.reports_root,
        adapter=BacktestAdapter.FAKE,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = config_from_args(args)
    # Print the config snapshot for operator review regardless of dry-run.
    print(json.dumps(json.loads(config.model_dump_json()), indent=2, sort_keys=True))
    if args.dry_run:
        return 0
    # Real-data invocation is handled by a small operator-facing
    # runner module kept out of the CLI itself to minimize the CLI's
    # responsibility. See `docs/00-meta/implementation-reports/
    # 2026-04-19_phase-3_gate-2-review.md` for the exact script used
    # during Phase 3 smoke runs.
    raise SystemExit(
        "Non-dry-run execution requires the operator-facing runner "
        "script; the CLI itself only validates config. "
        "Use --dry-run or invoke the runner directly."
    )


if __name__ == "__main__":
    sys.exit(main())
