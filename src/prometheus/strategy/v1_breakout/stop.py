"""Initial structural stop + stop-distance filter.

Per v1-breakout-strategy-spec.md §"Initial Stop Logic":

    Long: initial_stop = min(setup_low, breakout_bar_low) - 0.10 * ATR(20)_15m
    Short: initial_stop = max(setup_high, breakout_bar_high) + 0.10 * ATR(20)_15m

Per v1-breakout-strategy-spec.md §"Stop-distance filter":

    Reject if stop_distance < 0.60 * ATR(20)
    Reject if stop_distance > 1.80 * ATR(20)

The "stop_distance reference price" ambiguity (Gate-1 §11.A.A2) is
resolved per operator approval (GAP-20260419-015): use the signal
bar's CLOSE as the reference (not the fill price, which is not yet
realized at signal time).
"""

from __future__ import annotations

from prometheus.core.klines import NormalizedKline

from ..types import Direction, SetupWindow

STOP_BUFFER_ATR_MULT = 0.10
FILTER_MIN_ATR_MULT = 0.60
FILTER_MAX_ATR_MULT = 1.80


def compute_initial_stop(
    direction: Direction,
    setup: SetupWindow,
    breakout_bar: NormalizedKline,
    atr_20_15m: float,
) -> float:
    """Compute the structural initial stop per the v1 spec."""
    if atr_20_15m <= 0:
        raise ValueError("atr_20_15m must be positive")
    buffer = STOP_BUFFER_ATR_MULT * atr_20_15m
    if direction == Direction.LONG:
        base = min(setup.setup_low, breakout_bar.low)
        return base - buffer
    base = max(setup.setup_high, breakout_bar.high)
    return base + buffer


def passes_stop_distance_filter(stop_distance: float, atr_20_15m: float) -> bool:
    """Return True iff stop_distance is within [0.60, 1.80] * ATR(20)_15m.

    ``stop_distance`` must already be a positive magnitude (the
    caller should pass ``abs(reference_price - initial_stop)``).
    """
    if stop_distance <= 0:
        return False
    if atr_20_15m <= 0:
        return False
    return FILTER_MIN_ATR_MULT * atr_20_15m <= stop_distance <= FILTER_MAX_ATR_MULT * atr_20_15m
