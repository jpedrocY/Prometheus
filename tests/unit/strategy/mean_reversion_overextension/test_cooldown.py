"""F1 cooldown predicate tests (Phase 3b §4)."""

from __future__ import annotations

import pytest

from prometheus.strategy.mean_reversion_overextension.cooldown import (
    can_re_enter,
    cooldown_unwound,
)
from prometheus.strategy.types import Direction

THRESHOLD = 1.75


# ---------------------------------------------------------------------------
# cooldown_unwound
# ---------------------------------------------------------------------------


def test_cooldown_blocks_when_displacement_remains_extended() -> None:
    # All bars after exit show displacement well above threshold.
    displacement = [10.0] * 20  # always extended
    atr = [1.0] * 20  # threshold = 1.75
    assert (
        cooldown_unwound(
            displacement_history=displacement,
            atr20_history=atr,
            threshold_atr_multiple=THRESHOLD,
            since_index=5,
            current_index=15,
        )
        is False
    )


def test_cooldown_unwinds_when_displacement_drops_within_threshold() -> None:
    displacement = [10.0] * 20
    atr = [1.0] * 20
    # Bar 10 normalizes (within threshold).
    displacement[10] = 1.0
    assert (
        cooldown_unwound(
            displacement_history=displacement,
            atr20_history=atr,
            threshold_atr_multiple=THRESHOLD,
            since_index=5,
            current_index=15,
        )
        is True
    )


def test_cooldown_does_not_count_exit_bar_itself() -> None:
    # since_index is exclusive; even if the exit bar is unwound, we
    # must wait for a strictly-later bar.
    displacement = [10.0] * 20
    atr = [1.0] * 20
    displacement[5] = 0.0  # only the exit bar is normalized
    assert (
        cooldown_unwound(
            displacement_history=displacement,
            atr20_history=atr,
            threshold_atr_multiple=THRESHOLD,
            since_index=5,
            current_index=15,
        )
        is False
    )


def test_cooldown_at_threshold_boundary_inclusive() -> None:
    # cooldown_unwound uses <= for the unwind boundary (inclusive).
    displacement = [10.0] * 20
    atr = [1.0] * 20
    displacement[10] = THRESHOLD * 1.0  # exactly at threshold
    assert (
        cooldown_unwound(
            displacement_history=displacement,
            atr20_history=atr,
            threshold_atr_multiple=THRESHOLD,
            since_index=5,
            current_index=15,
        )
        is True
    )


def test_cooldown_skips_zero_atr_warmup_bars() -> None:
    displacement = [0.0] * 20  # would unwind on every bar with positive ATR
    atr = [0.0] * 5 + [1.0] * 15  # first 5 are warmup
    assert (
        cooldown_unwound(
            displacement_history=displacement,
            atr20_history=atr,
            threshold_atr_multiple=THRESHOLD,
            since_index=0,
            current_index=4,
        )
        is False
    )
    assert (
        cooldown_unwound(
            displacement_history=displacement,
            atr20_history=atr,
            threshold_atr_multiple=THRESHOLD,
            since_index=0,
            current_index=10,
        )
        is True
    )


def test_cooldown_current_le_since_returns_false() -> None:
    displacement = [0.0] * 5
    atr = [1.0] * 5
    assert (
        cooldown_unwound(
            displacement_history=displacement,
            atr20_history=atr,
            threshold_atr_multiple=THRESHOLD,
            since_index=4,
            current_index=4,
        )
        is False
    )


def test_cooldown_negative_since_raises() -> None:
    with pytest.raises(ValueError):
        cooldown_unwound(
            displacement_history=[0.0],
            atr20_history=[1.0],
            threshold_atr_multiple=THRESHOLD,
            since_index=-1,
            current_index=0,
        )


# ---------------------------------------------------------------------------
# can_re_enter
# ---------------------------------------------------------------------------


def test_can_re_enter_no_prior_exit_allowed() -> None:
    assert (
        can_re_enter(
            candidate_direction=Direction.LONG,
            last_exit_direction=None,
            last_exit_index=None,
            displacement_history=[10.0] * 5,
            atr20_history=[1.0] * 5,
            current_index=4,
            threshold_atr_multiple=THRESHOLD,
        )
        is True
    )


def test_can_re_enter_opposite_direction_never_blocked() -> None:
    # Same-direction would be blocked (no unwind), but opposite is allowed.
    displacement = [10.0] * 20
    atr = [1.0] * 20
    assert (
        can_re_enter(
            candidate_direction=Direction.SHORT,
            last_exit_direction=Direction.LONG,
            last_exit_index=5,
            displacement_history=displacement,
            atr20_history=atr,
            current_index=15,
            threshold_atr_multiple=THRESHOLD,
        )
        is True
    )


def test_can_re_enter_same_direction_blocked_until_unwind() -> None:
    displacement = [10.0] * 20
    atr = [1.0] * 20
    assert (
        can_re_enter(
            candidate_direction=Direction.LONG,
            last_exit_direction=Direction.LONG,
            last_exit_index=5,
            displacement_history=displacement,
            atr20_history=atr,
            current_index=15,
            threshold_atr_multiple=THRESHOLD,
        )
        is False
    )


def test_can_re_enter_same_direction_allowed_after_unwind() -> None:
    displacement = [10.0] * 20
    atr = [1.0] * 20
    displacement[10] = 0.5  # unwind happens at bar 10
    assert (
        can_re_enter(
            candidate_direction=Direction.LONG,
            last_exit_direction=Direction.LONG,
            last_exit_index=5,
            displacement_history=displacement,
            atr20_history=atr,
            current_index=15,
            threshold_atr_multiple=THRESHOLD,
        )
        is True
    )
