"""Phase 3j D1-A execution runner scaffold.

Runs the Phase 3g D1-A funding-aware directional / carry-aware
candidate against the locked Phase 2e v002 datasets.

This is **a scaffolded runner only** in Phase 3i-B1. Per the Phase
3i-B1 brief, no D1-A candidate backtests may be run during Phase
3i-B1; this script is committed as a non-runnable scaffold so a
future Phase 3j (or 3i-B2) can authorize candidate runs explicitly.

Usage (when Phase 3j is operator-authorized)::

    uv run python scripts/phase3j_D1A_execution.py d1a --window R \\
        --slippage MED --stop-trigger MARK_PRICE \\
        --phase-3j-authorized

Without ``--phase-3j-authorized`` the script exits non-zero and
emits the "D1-A candidate execution requires Phase 3j authorization"
message to stderr. The Phase 3i-B1 unit tests verify this guard.

The script intentionally does NOT import-time invoke the engine on
real data; the heavy run path is gated behind the authorization flag
and an operator-driven CLI invocation.

Forbidden in Phase 3i-B1:
- Any D1-A candidate backtest run (R-window or V-window).
- Any first-execution gate evaluation.
- Any M1 / M2 / M3 mechanism check on real data.
- Any derived ``funding_aware_features__v001`` artifact commit.

Forbidden under any phase that lacks operator authorization:
- threshold sweeps;
- target sweeps;
- lookback sweeps;
- time-stop sweeps;
- regime-conditional D1-A-prime;
- D1-B / V1-D1 hybrid / F1-D1 hybrid;
- additional symbols beyond BTCUSDT (primary) and ETHUSDT
  (research/comparison only per §1.7.3).
"""

from __future__ import annotations

import argparse
import sys

PHASE_3J_AUTHORIZATION_FLAG = "--phase-3j-authorized"

# Window definitions per Phase 2e (UTC milliseconds).
WINDOWS: dict[str, tuple[int, int]] = {
    "R": (1_640_995_200_000, 1_735_689_600_000),  # 2022-01-01 → 2025-01-01
    "V": (1_735_689_600_000, 1_775_001_600_000),  # 2025-01-01 → 2026-04-01
}

SLIPPAGE_ALIASES = {
    "LOW": "LOW",
    "MED": "MEDIUM",
    "MEDIUM": "MEDIUM",
    "HIGH": "HIGH",
}


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


def _check_imports() -> int:
    """Verify the D1-A engine surface imports cleanly.

    No-op except as a smoke for the import graph; safe to invoke
    without authorization.
    """
    # Local imports so a missing optional dependency does not break
    # argparse setup or guard messages.
    from prometheus.research.backtest.config import StrategyFamily  # noqa: F401
    from prometheus.research.backtest.engine import (  # noqa: F401
        BacktestEngine,
        FundingAwareLifecycleCounters,
    )
    from prometheus.strategy.funding_aware_directional import (  # noqa: F401
        FundingAwareConfig,
        FundingAwareStrategy,
    )

    print("D1-A engine surface imports OK.", file=sys.stdout)
    return 0


def _run_d1a(args: argparse.Namespace) -> int:
    """Execute a D1-A candidate cell, gated by ``--phase-3j-authorized``.

    Phase 3i-B1 ships this as a guarded scaffold only. Phase 3j (a
    future operator-authorized phase) is expected to lift the gate by
    running with ``--phase-3j-authorized`` after operator approval and
    then implement the full run-loop here.
    """
    if not getattr(args, "phase_3j_authorized", False):
        print(
            "D1-A candidate execution requires Phase 3j authorization.\n"
            f"Pass {PHASE_3J_AUTHORIZATION_FLAG} only after operator approval.",
            file=sys.stderr,
        )
        return 2

    # Phase 3i-B1 ships this scaffold without the live run-loop.
    # When Phase 3j is authorized, the full run-loop (data load,
    # BacktestEngine.run dispatch, summary metrics emission, lifecycle
    # counter aggregation, parquet output) will be implemented here,
    # mirroring scripts/phase3d_F1_execution.py's ``_run_f1`` shape.
    print(
        "D1-A run-loop not yet implemented in Phase 3i-B1 scaffold; "
        "Phase 3j is required to authorize candidate runs.",
        file=sys.stderr,
    )
    return 3


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
