"""F1 target exit (frozen mean-reference) computation and predicate.

Per Phase 3b §4:

    Mean reference frozen at signal-time bar B's close:
        sma_8_close(B) = (1/8) * sum_{i=0..7} close(B - i)

    Target exit:
        Long: first completed bar t > B with close(t) >= frozen_target
        Short: first completed bar t > B with close(t) <= frozen_target
        Fill at open(t+1).

The intrabar high/low is intentionally NOT used; only the bar's
close decides whether the target is hit.
"""

from __future__ import annotations

from collections.abc import Sequence

from ..types import Direction
from .features import sma_8_close

# Locked spec constant (Phase 3b §4).
MEAN_REFERENCE_WINDOW_BARS: int = 8


def compute_target(closes: Sequence[float], b_index: int) -> float:
    """Return the frozen F1 target = SMA(8) of closes at signal bar B.

    This is just :func:`prometheus.strategy.mean_reversion_overextension.
    features.sma_8_close` re-exposed under the target-exit name for
    readability at call sites.
    """
    return sma_8_close(closes, b_index)


def target_hit(direction: Direction, completed_close: float, frozen_target: float) -> bool:
    """Evaluate the F1 target predicate for a single completed bar.

    Long target hit iff ``completed_close >= frozen_target``.
    Short target hit iff ``completed_close <= frozen_target``.

    The frozen target is the SMA(8) computed once at signal-time bar B's
    close (Phase 3b §4); this function only checks whether a later
    completed bar's close has crossed it. The actual fill (open of
    t+1) is the caller's responsibility.
    """
    if direction == Direction.LONG:
        return completed_close >= frozen_target
    return completed_close <= frozen_target
