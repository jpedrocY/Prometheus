"""F1 protective stop computation and stop-distance admissibility.

Per Phase 3b §4:

    Long protective stop  = lowest_low([B-7..B]) - stop_buffer * ATR(20)(B)
    Short protective stop = highest_high([B-7..B]) + stop_buffer * ATR(20)(B)
    stop_buffer (locked) = 0.10

Stop-distance admissibility band (Phase 3b §4):

    reject if stop_distance < stop_distance_min_atr * ATR(20)(B)
    reject if stop_distance > stop_distance_max_atr * ATR(20)(B)

The stop_distance reference price is the **raw (de-slipped) open(B+1)**.
This module's :func:`passes_stop_distance_filter` takes the
already-computed ``stop_distance`` magnitude; the engine
integration (Phase 3d-B) is responsible for passing the de-slipped
price.
"""

from __future__ import annotations

from collections.abc import Sequence

from ..types import Direction

# Locked spec constants (Phase 3b §4).
STOP_BUFFER_ATR_MULTIPLE: float = 0.10
STOP_DISTANCE_MIN_ATR: float = 0.60
STOP_DISTANCE_MAX_ATR: float = 1.80
STOP_WINDOW_BARS: int = 8


def compute_initial_stop(
    direction: Direction,
    lows: Sequence[float],
    highs: Sequence[float],
    atr20_at_b: float,
    b_index: int,
    stop_buffer_atr_multiple: float = STOP_BUFFER_ATR_MULTIPLE,
) -> float:
    """Compute the F1 initial protective stop for the given direction.

    Long  -> ``min(lows[B-7..B]) - stop_buffer * ATR(20)(B)``.
    Short -> ``max(highs[B-7..B]) + stop_buffer * ATR(20)(B)``.

    The window length is hard-coded to the locked Phase 3b spec value
    (``STOP_WINDOW_BARS = 8``); ``stop_buffer_atr_multiple`` defaults
    to the locked 0.10 and is only parameterized for testability — the
    engine integration (Phase 3d-B) will pass ``MeanReversionConfig.
    stop_buffer_atr_multiple`` which is also locked at 0.10.

    Parameters
    ----------
    direction:
        Trade direction.
    lows, highs:
        Sequences of completed-bar lows / highs aligned by index.
    atr20_at_b:
        ATR(20) at the close of bar B. Must be strictly positive.
    b_index:
        Index of bar B. Must satisfy
        ``b_index >= STOP_WINDOW_BARS - 1``.

    Raises
    ------
    IndexError
        If ``b_index`` is below warmup or out of range.
    ValueError
        If ``atr20_at_b`` is non-positive.
    """
    if atr20_at_b <= 0.0:
        raise ValueError(f"atr20_at_b must be positive, got {atr20_at_b}")
    if b_index < STOP_WINDOW_BARS - 1:
        raise IndexError(
            f"b_index={b_index} below warmup; need at least {STOP_WINDOW_BARS - 1} prior bars"
        )
    if b_index >= len(lows) or b_index >= len(highs):
        raise IndexError(
            f"b_index={b_index} out of range len(lows)={len(lows)} len(highs)={len(highs)}"
        )

    buffer_amount = stop_buffer_atr_multiple * atr20_at_b
    window_start = b_index - STOP_WINDOW_BARS + 1
    if direction == Direction.LONG:
        lowest_low = min(float(x) for x in lows[window_start : b_index + 1])
        return lowest_low - buffer_amount
    highest_high = max(float(x) for x in highs[window_start : b_index + 1])
    return highest_high + buffer_amount


def passes_stop_distance_filter(
    stop_distance: float,
    atr20_at_b: float,
    min_atr_multiple: float = STOP_DISTANCE_MIN_ATR,
    max_atr_multiple: float = STOP_DISTANCE_MAX_ATR,
) -> bool:
    """Return True iff ``stop_distance`` is in the locked admissibility band.

    Band (Phase 3b §4): ``[min_atr_multiple, max_atr_multiple] * ATR(20)(B)``.
    The locked spec values are 0.60 and 1.80 respectively.

    The caller computes ``stop_distance = abs(reference_price - initial_stop)``
    where ``reference_price`` is the **raw de-slipped open(B+1)** per
    Phase 3b §4. The min/max multiples are parameterized only for
    testability; in production they come from
    ``MeanReversionConfig.stop_distance_min_atr`` /
    ``MeanReversionConfig.stop_distance_max_atr`` which are locked.

    Inclusive both ends, matching the v1_breakout convention.
    """
    if stop_distance <= 0.0:
        return False
    if atr20_at_b <= 0.0:
        return False
    return min_atr_multiple * atr20_at_b <= stop_distance <= max_atr_multiple * atr20_at_b
