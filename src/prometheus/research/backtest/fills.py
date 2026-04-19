"""Fill model: next-bar-open baseline with slippage.

Per Phase 3 Gate 1 §10.4 and ambiguity decisions:

    - A3 (GAP-20260419-016): managed exits also fill at next-bar-open.
    - Slippage applied in the adverse direction:
        long entry / short exit -> higher (worse) fill
        short entry / long exit -> lower (worse) fill

The stop-hit fill model is separate (see ``stops.py``).
"""

from __future__ import annotations

from enum import StrEnum

from prometheus.core.klines import NormalizedKline

from ..backtest.config import (
    DEFAULT_SLIPPAGE_BPS,  # noqa: F401
    SlippageBucket,  # noqa: F401  -- re-exported at package level
)
from .config import BacktestConfig


class FillSide(StrEnum):
    ENTRY_LONG = "ENTRY_LONG"
    ENTRY_SHORT = "ENTRY_SHORT"
    EXIT_LONG = "EXIT_LONG"
    EXIT_SHORT = "EXIT_SHORT"


def _bps_to_multiplier(bps: float) -> float:
    return bps / 10_000.0


def compute_fill_price(
    *,
    raw_price: float,
    side: FillSide,
    slippage_bps: float,
) -> float:
    """Apply slippage adversely to a raw bar-open price.

    Entry long and exit short both buy-to-open/close; both pay the
    ask (higher). Entry short and exit long both sell-to-open/close;
    both receive the bid (lower).
    """
    if raw_price <= 0:
        raise ValueError("raw_price must be positive")
    if slippage_bps < 0:
        raise ValueError("slippage_bps must be non-negative")
    mult = _bps_to_multiplier(slippage_bps)
    if side in (FillSide.ENTRY_LONG, FillSide.EXIT_SHORT):
        return raw_price * (1.0 + mult)
    return raw_price * (1.0 - mult)


def entry_fill_price(
    *, next_bar: NormalizedKline, direction_long: bool, config: BacktestConfig
) -> float:
    """Entry fill price at the next 15m bar's open, with slippage."""
    side = FillSide.ENTRY_LONG if direction_long else FillSide.ENTRY_SHORT
    return compute_fill_price(
        raw_price=next_bar.open,
        side=side,
        slippage_bps=config.slippage_bps,
    )


def exit_fill_price(
    *, next_bar: NormalizedKline, direction_long: bool, config: BacktestConfig
) -> float:
    """Managed-exit fill price at the next 15m bar's open, with slippage."""
    side = FillSide.EXIT_LONG if direction_long else FillSide.EXIT_SHORT
    return compute_fill_price(
        raw_price=next_bar.open,
        side=side,
        slippage_bps=config.slippage_bps,
    )
