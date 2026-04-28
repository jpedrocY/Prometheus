"""F1 target exit tests (Phase 3b §4)."""

from __future__ import annotations

import pytest

from prometheus.strategy.mean_reversion_overextension.target import (
    compute_target,
    target_hit,
)
from prometheus.strategy.types import Direction

# ---------------------------------------------------------------------------
# compute_target
# ---------------------------------------------------------------------------


def test_compute_target_matches_sma_8() -> None:
    closes = [10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 100.0]
    # SMA(8) at B=7 over closes[0..7] = (10+12+14+16+18+20+22+24)/8 = 17.0
    assert compute_target(closes, 7) == pytest.approx(17.0)


def test_compute_target_constant_series() -> None:
    closes = [55.5] * 12
    assert compute_target(closes, 11) == pytest.approx(55.5)


def test_compute_target_warmup_raises() -> None:
    closes = [1.0] * 7
    with pytest.raises(IndexError):
        compute_target(closes, 6)


# ---------------------------------------------------------------------------
# target_hit — long
# ---------------------------------------------------------------------------


def test_long_close_at_or_above_target_is_hit() -> None:
    assert target_hit(Direction.LONG, completed_close=17.0, frozen_target=17.0) is True
    assert target_hit(Direction.LONG, completed_close=17.5, frozen_target=17.0) is True


def test_long_close_below_target_is_not_hit() -> None:
    assert target_hit(Direction.LONG, completed_close=16.99, frozen_target=17.0) is False


# ---------------------------------------------------------------------------
# target_hit — short
# ---------------------------------------------------------------------------


def test_short_close_at_or_below_target_is_hit() -> None:
    assert target_hit(Direction.SHORT, completed_close=17.0, frozen_target=17.0) is True
    assert target_hit(Direction.SHORT, completed_close=16.5, frozen_target=17.0) is True


def test_short_close_above_target_is_not_hit() -> None:
    assert target_hit(Direction.SHORT, completed_close=17.01, frozen_target=17.0) is False


def test_target_hit_uses_close_only_documented() -> None:
    """Per Phase 3b §4 the target predicate is on the bar's close, not the high/low.

    The function signature itself enforces this by only accepting a single
    ``completed_close`` value; we keep this assertion as a regression guard
    that nobody refactors the signature to take a high/low pair.
    """
    # Mirror sanity check: for short, even a high above target shouldn't
    # matter — only the close matters. We can't pass a high here, but we
    # confirm the equality boundary is the close value itself.
    assert target_hit(Direction.SHORT, completed_close=99.99, frozen_target=100.0) is True
    assert target_hit(Direction.SHORT, completed_close=100.01, frozen_target=100.0) is False
