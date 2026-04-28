"""Phase 3d F1 (mean-reversion-after-overextension) execution runner — SCAFFOLD.

Phase 3d-B1 scope is engine wiring + tests + quality gates + H0/R3
control reproduction ONLY. F1 candidate execution is reserved for
Phase 3d-B2. This script is a deliberate scaffold that imports the
new F1 engine surface and exposes the CLI argument shape Phase 3d-B2
will consume, but it intentionally REFUSES to run F1 backtests until
Phase 3d-B2 is authorized.

Per Phase 3c §6 the eventual run inventory is::

    1. F1   R MED MARK     (governing first F1 run)
    2. F1   R LOW MARK      (§11.6 cost-sensitivity LOW)
    3. F1   R HIGH MARK     (§11.6 HIGH cost-sensitivity gate)
    4. F1   R MED TRADE_PRICE  (stop-trigger sensitivity)
    5. F1   V MED MARK      (conditional on §7.2 PROMOTE)

Phase 3d-B1 validates that the engine's F1 dispatch surface compiles,
quality-gates green, and reproduces H0/R3 baselines bit-for-bit. NO
F1 candidate backtest is executed by this scaffold — invoking the
``f1`` action without ``--phase-3d-b2-authorized`` exits with a hard
guard message.

Usage during Phase 3d-B1::

    uv run python scripts/phase3d_F1_execution.py --check-imports

The ``--check-imports`` action verifies the F1 engine surface imports
cleanly and prints a one-line summary; it executes no backtest.
"""

from __future__ import annotations

import argparse
import sys

from prometheus.research.backtest import BacktestEngine
from prometheus.research.backtest.config import StrategyFamily
from prometheus.research.backtest.engine import F1LifecycleCounters
from prometheus.strategy.mean_reversion_overextension import (
    MeanReversionConfig,
    MeanReversionStrategy,
)

PHASE_3D_B2_AUTHORIZATION_FLAG = "--phase-3d-b2-authorized"


def _check_imports() -> int:
    """Verify the F1 engine surface imports cleanly. No backtest run."""
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


def _f1_run_guard(args: argparse.Namespace) -> int:
    """Hard guard: F1 candidate backtests are reserved for Phase 3d-B2."""
    if not getattr(args, "phase_3d_b2_authorized", False):
        print(
            "Phase 3d-B1 forbids F1 candidate backtest execution.\n"
            "F1 R/V runs are Phase 3d-B2 work.\n"
            f"Pass {PHASE_3D_B2_AUTHORIZATION_FLAG} only after operator\n"
            "approval of Phase 3d-B2.",
            file=sys.stderr,
        )
        return 2
    print(
        "Phase 3d-B2 authorization received but the runner is a scaffold;\n"
        "the actual run-loop / dataset wiring / report writer is part of\n"
        "Phase 3d-B2 implementation.",
        file=sys.stderr,
    )
    return 2


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="phase3d_F1_execution",
        description=("Phase 3d F1 execution runner — Phase 3d-B1 scaffold (no run-loop)."),
    )
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("check-imports", help="Verify F1 engine surface imports cleanly.")
    f1_parser = sub.add_parser(
        "f1",
        help="Execute an F1 candidate backtest (Phase 3d-B2; guarded).",
    )
    f1_parser.add_argument(
        "--variant",
        choices=("F1",),
        default="F1",
        help="Strategy variant (only F1 supported).",
    )
    f1_parser.add_argument(
        "--window",
        choices=("R", "V"),
        required=False,
        help="R-window or V-window (V conditional on PROMOTE per §11.3).",
    )
    f1_parser.add_argument(
        "--slippage",
        choices=("LOW", "MED", "HIGH"),
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
        help="Required to attempt any F1 backtest invocation.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_argparser()
    args = parser.parse_args(argv)
    if args.action == "check-imports":
        return _check_imports()
    if args.action == "f1":
        return _f1_run_guard(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
