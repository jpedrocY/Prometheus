"""Stop-hit evaluation against mark-price bars.

Per Phase 3 Gate 1 §10.5 and operator-approved GAP-20260419-017
(gap-through rule, Option 2):

    - If the mark-price bar's OPEN is already beyond the stop level
      (adverse gap), the stop fills at the bar's open price.
    - Otherwise, if the bar's range crosses the stop, fill at the
      stop level itself.
    - Exit slippage is applied on top.

Mark-price bars are used because live protective stops use
workingType=MARK_PRICE. Using trade-price bars for evaluation would
produce systematically different fills.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from prometheus.core.mark_price_klines import MarkPriceKline
from prometheus.core.symbols import Symbol

from .fills import FillSide, compute_fill_price


class StopHit(BaseModel):
    """A stop fill produced by ``evaluate_stop_hit``."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    fill_price: float = Field(gt=0)
    fill_time_ms: int = Field(gt=0)  # defined as bar.close_time + 1 (next millisecond)
    mark_bar_open_time: int
    was_gap_through: bool


def evaluate_stop_hit(
    *,
    direction_long: bool,
    current_stop: float,
    mark_bar: MarkPriceKline,
    slippage_bps: float,
) -> StopHit | None:
    """Determine whether ``mark_bar`` triggers the stop. Return the
    filled price if so, else None.

    The caller is responsible for ensuring ``mark_bar`` is ordered
    AFTER any bar on which management already moved the stop.
    """
    if current_stop <= 0:
        raise ValueError("current_stop must be positive")
    if slippage_bps < 0:
        raise ValueError("slippage_bps must be non-negative")

    if direction_long:
        # Long stop hit when mark-price drops to/below the stop.
        if mark_bar.low > current_stop:
            return None
        was_gap = mark_bar.open <= current_stop
        raw_fill = mark_bar.open if was_gap else current_stop
        side = FillSide.EXIT_LONG
    else:
        # Short stop hit when mark-price rises to/above the stop.
        if mark_bar.high < current_stop:
            return None
        was_gap = mark_bar.open >= current_stop
        raw_fill = mark_bar.open if was_gap else current_stop
        side = FillSide.EXIT_SHORT

    fill_price = compute_fill_price(raw_price=raw_fill, side=side, slippage_bps=slippage_bps)
    return StopHit(
        symbol=mark_bar.symbol,
        fill_price=fill_price,
        fill_time_ms=mark_bar.close_time + 1,
        mark_bar_open_time=mark_bar.open_time,
        was_gap_through=was_gap,
    )
