"""Funding-event join for open positions.

Per Phase 3 Gate 1 §10.6 and GAP-20260419-019 (A6, operator-approved
inclusive both ends):

    funding_time in [T_entry, T_exit]  -> apply to open position

Direction sign:

    positive rate means longs pay shorts (long's funding_pnl is negative)
    negative rate means shorts pay longs (long's funding_pnl is positive)

    funding_pnl = position_notional * funding_rate * (-direction_sign)
    where direction_sign = +1 for long, -1 for short

This matches Binance USD-M perpetual funding convention.
"""

from __future__ import annotations

from collections.abc import Sequence

from prometheus.core.events import FundingRateEvent


def apply_funding_accrual(
    *,
    direction_long: bool,
    entry_fill_time_ms: int,
    exit_fill_time_ms: int,
    position_notional_usdt: float,
    funding_events: Sequence[FundingRateEvent],
) -> tuple[float, list[FundingRateEvent]]:
    """Sum signed funding PnL across events in the holding window.

    Returns ``(total_funding_pnl, matched_events)``. The matched
    events are included in the returned list for audit / trade-log
    enrichment.

    Uses operator-approved INCLUSIVE-BOTH-ENDS window convention
    (GAP-20260419-019).
    """
    if exit_fill_time_ms < entry_fill_time_ms:
        raise ValueError("exit_fill_time_ms must be >= entry_fill_time_ms")
    if position_notional_usdt <= 0:
        raise ValueError("position_notional_usdt must be positive")

    direction_sign = 1.0 if direction_long else -1.0
    matched: list[FundingRateEvent] = []
    total = 0.0
    for event in funding_events:
        if entry_fill_time_ms <= event.funding_time <= exit_fill_time_ms:
            # Long pays when rate > 0: funding_pnl is NEGATIVE for long.
            pnl_for_direction = position_notional_usdt * event.funding_rate * (-direction_sign)
            total += pnl_for_direction
            matched.append(event)
    return total, matched
