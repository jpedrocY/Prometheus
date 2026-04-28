"""F1 mean-reversion feature functions (Phase 3b §4).

Pure, completed-bars-only, no-lookahead feature helpers:

    - cumulative_displacement_8bar: close(B) - close(B - 8)
    - sma_8_close: (1/8) * sum_{i=0..7} close(B - i)  (frozen at B)
    - overextension_event: (fires, direction) given the threshold

All inputs are sequences indexed by bar position. The caller is
responsible for ensuring inputs come from completed bars only.
"""

from __future__ import annotations

from collections.abc import Sequence

# Locked spec constants (Phase 3b §4); duplicated as integers/floats
# for the pure-function module so it has no dependency on the
# ``MeanReversionConfig`` model.
DISPLACEMENT_WINDOW_BARS: int = 8
SMA_WINDOW_BARS: int = 8


def cumulative_displacement_8bar(closes: Sequence[float], b_index: int) -> float:
    """Return ``close(B) - close(B - 8)``.

    Per Phase 3b §4 (overextension definition). Positive value means
    upward displacement (short candidate); negative means downward
    (long candidate).

    Parameters
    ----------
    closes:
        Sequence of completed-bar closes (index 0 is oldest).
    b_index:
        Index of bar B in ``closes``. Must satisfy
        ``b_index >= DISPLACEMENT_WINDOW_BARS``.

    Raises
    ------
    IndexError
        If ``b_index < DISPLACEMENT_WINDOW_BARS`` (warmup not available)
        or ``b_index >= len(closes)``.
    """
    if b_index < DISPLACEMENT_WINDOW_BARS:
        raise IndexError(
            f"b_index={b_index} below warmup; need at least {DISPLACEMENT_WINDOW_BARS} prior bars"
        )
    if b_index >= len(closes):
        raise IndexError(f"b_index={b_index} out of range len={len(closes)}")
    return float(closes[b_index]) - float(closes[b_index - DISPLACEMENT_WINDOW_BARS])


def sma_8_close(closes: Sequence[float], b_index: int) -> float:
    """Return SMA(8) of close ending at bar B.

    Per Phase 3b §4: ``sma_8_close(B) = (1/8) * sum_{i=0..7} close(B - i)``.
    This is the F1 mean-reference value, frozen at signal-time bar B.

    Parameters
    ----------
    closes:
        Sequence of completed-bar closes (index 0 is oldest).
    b_index:
        Index of bar B in ``closes``. Must satisfy
        ``b_index >= SMA_WINDOW_BARS - 1``.

    Raises
    ------
    IndexError
        If ``b_index < SMA_WINDOW_BARS - 1`` (warmup not available)
        or ``b_index >= len(closes)``.
    """
    if b_index < SMA_WINDOW_BARS - 1:
        raise IndexError(
            f"b_index={b_index} below warmup; need at least {SMA_WINDOW_BARS - 1} prior bars"
        )
    if b_index >= len(closes):
        raise IndexError(f"b_index={b_index} out of range len={len(closes)}")
    window = closes[b_index - SMA_WINDOW_BARS + 1 : b_index + 1]
    if len(window) != SMA_WINDOW_BARS:  # pragma: no cover — defensive
        raise IndexError(f"window length {len(window)} != {SMA_WINDOW_BARS}")
    return sum(float(c) for c in window) / float(SMA_WINDOW_BARS)


def overextension_event(
    closes: Sequence[float],
    atr20: Sequence[float],
    b_index: int,
    threshold_atr_multiple: float,
) -> tuple[bool, int]:
    """Evaluate the F1 overextension predicate at bar B.

    Per Phase 3b §4: F1 fires iff
    ``abs(cumulative_displacement_8bar(B)) > threshold * ATR(20)(B)``.
    Direction:

        positive cumulative displacement -> SHORT candidate (+1)
        negative cumulative displacement -> LONG candidate (-1)
        no fire                          -> 0

    The comparison is strict ``>``; equality at the boundary does NOT
    fire (matches the literal Phase 3b §4 wording).

    Parameters
    ----------
    closes:
        Sequence of completed-bar closes.
    atr20:
        Sequence of ATR(20) values aligned with ``closes`` by bar index.
    b_index:
        Index of bar B.
    threshold_atr_multiple:
        Multiplier on ``ATR(20)(B)``; locked spec value 1.75.

    Returns
    -------
    tuple[bool, int]
        ``(fires, direction)`` where direction is +1 / -1 / 0 as above.

    Raises
    ------
    IndexError
        If ``b_index`` lacks the displacement warmup (raised by
        :func:`cumulative_displacement_8bar`).
    ValueError
        If ``atr20[b_index]`` is non-positive.
    """
    if b_index >= len(atr20):
        raise IndexError(f"b_index={b_index} out of range len(atr20)={len(atr20)}")
    atr_b = float(atr20[b_index])
    if atr_b <= 0.0:
        raise ValueError(f"atr20[{b_index}] must be positive, got {atr_b}")
    disp = cumulative_displacement_8bar(closes, b_index)
    threshold = threshold_atr_multiple * atr_b
    if abs(disp) > threshold:
        direction = 1 if disp > 0 else -1
        return True, direction
    return False, 0
