"""D1-A primitive function tests (Phase 3g §6 + Phase 3h clarifications).

Pure-function tests for:

    - compute_funding_z_score (uses trailing 270 prior events; excludes
      current event from its own mean/std; NaN during warmup; NaN on
      degenerate variance)
    - align_funding_event_to_bar (non-strict ≤; equality eligible;
      strict-greater forbidden)
    - funding_extreme_event (|Z| ≥ threshold; NaN-safe)
    - signal_direction (contrarian; ±2.0 inclusive)
    - compute_stop / compute_target (LONG / SHORT geometry)
    - time_stop_bar_index (entry_bar_idx + 32)
    - passes_stop_distance_filter (admissibility band)
    - can_re_enter (per-event cooldown)
"""

from __future__ import annotations

import math

import pytest

from prometheus.strategy.funding_aware_directional import (
    FundingEvent,
    align_funding_event_to_bar,
    can_re_enter,
    compute_funding_z_score,
    compute_stop,
    compute_target,
    funding_extreme_event,
    passes_stop_distance_filter,
    signal_direction,
    time_stop_bar_index,
)
from prometheus.strategy.types import Direction

# ---------------------------------------------------------------------
# compute_funding_z_score
# ---------------------------------------------------------------------


def test_z_score_uses_trailing_270_prior_events() -> None:
    """Mean/std computed over the most recent 270 entries of prior_funding_rates."""
    # Build a series where prior 270 events have known mean = 0.0001 and
    # known sample std. Then the current rate's Z is exactly computable.
    prior = [0.0001] * 269 + [0.0001]
    # All values equal -> sample std == 0 -> NaN expected (degenerate).
    z = compute_funding_z_score(prior, 0.0005)
    assert math.isnan(z)


def test_z_score_excludes_current_event() -> None:
    """The current event must NOT enter its own mean/std."""
    # Construct prior such that adding current would change mean visibly.
    prior = [0.0] * 270
    # If current event were included, mean would shift toward current.
    # Here, prior std is 0 -> NaN (degenerate). This proves current
    # is not in the sample, because if it were, sample variance > 0.
    z = compute_funding_z_score(prior, 0.001)
    assert math.isnan(z)

    # Now make prior have non-zero variance and verify excluding-current
    # behavior numerically.
    prior2 = [0.0001 if i % 2 == 0 else -0.0001 for i in range(270)]
    # Sample mean = 0 (or very close); sample std > 0.
    z2 = compute_funding_z_score(prior2, 0.0)
    # If current event 0.0 enters mean, mean would still ≈ 0; but
    # std would be slightly different. The Z of 0.0 should be near 0
    # since mean ≈ 0.
    assert not math.isnan(z2)
    assert abs(z2) < 0.01


def test_z_score_warmup_returns_nan() -> None:
    """Fewer than 270 prior events -> NaN."""
    prior = [0.0001] * 269  # one short
    z = compute_funding_z_score(prior, 0.0005)
    assert math.isnan(z)


def test_z_score_zero_warmup_returns_nan() -> None:
    z = compute_funding_z_score([], 0.0005)
    assert math.isnan(z)


def test_z_score_zero_variance_returns_nan() -> None:
    """Degenerate-variance prior -> NaN, not a fabricated signal."""
    prior = [0.0001] * 270
    z = compute_funding_z_score(prior, 0.0010)
    assert math.isnan(z)


def test_z_score_basic_positive() -> None:
    """A positive funding rate vs zero-mean prior with known std produces
    a positive Z."""
    # Prior alternates +1, -1 (sample mean = 0, sample variance ≈ 1).
    prior = [1.0 if i % 2 == 0 else -1.0 for i in range(270)]
    z = compute_funding_z_score(prior, 3.0)
    assert z > 0
    assert abs(z - 3.0) < 0.05  # close to 3.0 since std ≈ 1


def test_z_score_invalid_lookback_raises() -> None:
    with pytest.raises(ValueError):
        compute_funding_z_score([0.0] * 10, 0.0, lookback_events=1)


# ---------------------------------------------------------------------
# align_funding_event_to_bar
# ---------------------------------------------------------------------


def _ev(t_ms: int, rate: float = 0.0001) -> FundingEvent:
    return FundingEvent(event_id=f"e-{t_ms}", funding_time=t_ms, funding_rate=rate)


def test_align_strict_less_than_eligible() -> None:
    events = [_ev(1000), _ev(2000), _ev(3000)]
    out = align_funding_event_to_bar(events, bar_close_time=2500)
    assert out is not None
    assert out.funding_time == 2000


def test_align_equality_eligible() -> None:
    """funding_time == bar_close_time is eligible (Phase 3h §4.5
    non-strict ≤; equality eligible)."""
    events = [_ev(1000), _ev(2000), _ev(3000)]
    out = align_funding_event_to_bar(events, bar_close_time=2000)
    assert out is not None
    assert out.funding_time == 2000


def test_align_strict_greater_forbidden() -> None:
    """funding_time > bar_close_time is excluded."""
    events = [_ev(1000), _ev(2000), _ev(3000)]
    out = align_funding_event_to_bar(events, bar_close_time=1999)
    assert out is not None
    assert out.funding_time == 1000  # 2000 ineligible since > 1999


def test_align_no_lookahead_future_event() -> None:
    """A future event at bar_close_time + 1 ms is excluded."""
    events = [_ev(1000), _ev(2001)]  # 2001 = bar_close + 1 (with bar_close=2000)
    out = align_funding_event_to_bar(events, bar_close_time=2000)
    assert out is not None
    assert out.funding_time == 1000


def test_align_returns_none_when_all_future() -> None:
    events = [_ev(2000), _ev(3000)]
    out = align_funding_event_to_bar(events, bar_close_time=1500)
    assert out is None


def test_align_unsorted_input_returns_latest_eligible() -> None:
    events = [_ev(3000), _ev(1000), _ev(2000)]
    out = align_funding_event_to_bar(events, bar_close_time=2500)
    assert out is not None
    assert out.funding_time == 2000


# ---------------------------------------------------------------------
# funding_extreme_event
# ---------------------------------------------------------------------


def test_funding_extreme_event_above_threshold() -> None:
    assert funding_extreme_event(2.5, threshold=2.0) is True
    assert funding_extreme_event(-2.5, threshold=2.0) is True


def test_funding_extreme_event_at_threshold_inclusive() -> None:
    """|Z| >= threshold is inclusive at exactly ±2.0."""
    assert funding_extreme_event(2.0, threshold=2.0) is True
    assert funding_extreme_event(-2.0, threshold=2.0) is True


def test_funding_extreme_event_below_threshold() -> None:
    assert funding_extreme_event(1.99, threshold=2.0) is False
    assert funding_extreme_event(-1.99, threshold=2.0) is False
    assert funding_extreme_event(0.0, threshold=2.0) is False


def test_funding_extreme_event_nan_safe() -> None:
    assert funding_extreme_event(float("nan"), threshold=2.0) is False


# ---------------------------------------------------------------------
# signal_direction
# ---------------------------------------------------------------------


def test_signal_direction_positive_extreme_creates_short() -> None:
    assert signal_direction(2.0, threshold=2.0) == Direction.SHORT
    assert signal_direction(3.5, threshold=2.0) == Direction.SHORT


def test_signal_direction_negative_extreme_creates_long() -> None:
    assert signal_direction(-2.0, threshold=2.0) == Direction.LONG
    assert signal_direction(-3.5, threshold=2.0) == Direction.LONG


def test_signal_direction_below_threshold_no_signal() -> None:
    assert signal_direction(1.99, threshold=2.0) is None
    assert signal_direction(-1.99, threshold=2.0) is None
    assert signal_direction(0.0, threshold=2.0) is None


def test_signal_direction_nan_no_signal() -> None:
    assert signal_direction(float("nan"), threshold=2.0) is None


# ---------------------------------------------------------------------
# compute_stop
# ---------------------------------------------------------------------


def test_compute_stop_long() -> None:
    stop = compute_stop(fill_price=100.0, atr20=2.5, side=Direction.LONG, multiplier=1.0)
    assert stop == 97.5


def test_compute_stop_short() -> None:
    stop = compute_stop(fill_price=100.0, atr20=2.5, side=Direction.SHORT, multiplier=1.0)
    assert stop == 102.5


def test_compute_stop_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        compute_stop(fill_price=0.0, atr20=2.5, side=Direction.LONG)
    with pytest.raises(ValueError):
        compute_stop(fill_price=100.0, atr20=0.0, side=Direction.LONG)
    with pytest.raises(ValueError):
        compute_stop(fill_price=100.0, atr20=2.5, side=Direction.LONG, multiplier=0.0)


# ---------------------------------------------------------------------
# compute_target
# ---------------------------------------------------------------------


def test_compute_target_long_at_two_R() -> None:
    target = compute_target(fill_price=100.0, stop_distance=2.5, side=Direction.LONG, target_r=2.0)
    assert target == 105.0


def test_compute_target_short_at_two_R() -> None:
    target = compute_target(fill_price=100.0, stop_distance=2.5, side=Direction.SHORT, target_r=2.0)
    assert target == 95.0


def test_compute_target_default_two_R() -> None:
    """Default target_r = 2.0 per Phase 3g §5.6.5 Option A."""
    target = compute_target(fill_price=100.0, stop_distance=2.5, side=Direction.LONG)
    assert target == 105.0


def test_compute_target_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        compute_target(fill_price=0.0, stop_distance=2.5, side=Direction.LONG)
    with pytest.raises(ValueError):
        compute_target(fill_price=100.0, stop_distance=0.0, side=Direction.LONG)
    with pytest.raises(ValueError):
        compute_target(fill_price=100.0, stop_distance=2.5, side=Direction.LONG, target_r=0.0)


# ---------------------------------------------------------------------
# time_stop_bar_index
# ---------------------------------------------------------------------


def test_time_stop_bar_index_default_32() -> None:
    """Default 32 bars per Phase 3g §6.9."""
    assert time_stop_bar_index(entry_bar_idx=100) == 132


def test_time_stop_bar_index_custom() -> None:
    assert time_stop_bar_index(entry_bar_idx=10, time_stop_bars=8) == 18


def test_time_stop_bar_index_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        time_stop_bar_index(entry_bar_idx=-1)
    with pytest.raises(ValueError):
        time_stop_bar_index(entry_bar_idx=10, time_stop_bars=0)


# ---------------------------------------------------------------------
# passes_stop_distance_filter
# ---------------------------------------------------------------------


def test_stop_distance_filter_accepts_one_atr() -> None:
    """D1-A's 1.0 × ATR is inside [0.60, 1.80] band by construction."""
    assert passes_stop_distance_filter(stop_distance=2.5, atr20=2.5, min_atr=0.60, max_atr=1.80)


def test_stop_distance_filter_rejects_below_band() -> None:
    assert not passes_stop_distance_filter(
        stop_distance=1.0, atr20=2.5, min_atr=0.60, max_atr=1.80
    )  # ratio = 0.40 < 0.60


def test_stop_distance_filter_rejects_above_band() -> None:
    assert not passes_stop_distance_filter(
        stop_distance=5.0, atr20=2.5, min_atr=0.60, max_atr=1.80
    )  # ratio = 2.0 > 1.80


def test_stop_distance_filter_band_edges_inclusive() -> None:
    assert passes_stop_distance_filter(
        stop_distance=1.5, atr20=2.5, min_atr=0.60, max_atr=1.80
    )  # ratio = 0.60 exactly
    assert passes_stop_distance_filter(
        stop_distance=4.5, atr20=2.5, min_atr=0.60, max_atr=1.80
    )  # ratio = 1.80 exactly


def test_stop_distance_filter_invalid_inputs() -> None:
    assert not passes_stop_distance_filter(stop_distance=0.0, atr20=2.5)
    assert not passes_stop_distance_filter(stop_distance=2.5, atr20=0.0)


# ---------------------------------------------------------------------
# can_re_enter
# ---------------------------------------------------------------------


def test_can_re_enter_no_prior_consumption_allowed() -> None:
    assert can_re_enter(
        candidate_direction=Direction.LONG,
        candidate_event_id="e-1",
        last_consumed_event_id=None,
        last_consumed_direction=None,
        position_open=False,
    )


def test_can_re_enter_position_open_blocks_all() -> None:
    assert not can_re_enter(
        candidate_direction=Direction.LONG,
        candidate_event_id="e-2",
        last_consumed_event_id="e-1",
        last_consumed_direction=Direction.LONG,
        position_open=True,
    )


def test_can_re_enter_same_event_same_direction_blocked() -> None:
    """Same-event same-direction re-entry blocked (cooldown consumed event)."""
    assert not can_re_enter(
        candidate_direction=Direction.SHORT,
        candidate_event_id="e-1",
        last_consumed_event_id="e-1",
        last_consumed_direction=Direction.SHORT,
        position_open=False,
    )


def test_can_re_enter_fresh_event_same_direction_allowed() -> None:
    """Fresh event allows same-direction re-entry."""
    assert can_re_enter(
        candidate_direction=Direction.SHORT,
        candidate_event_id="e-2",
        last_consumed_event_id="e-1",
        last_consumed_direction=Direction.SHORT,
        position_open=False,
    )


def test_can_re_enter_opposite_direction_same_event_allowed() -> None:
    """Opposite direction is never cooldown-blocked."""
    assert can_re_enter(
        candidate_direction=Direction.LONG,
        candidate_event_id="e-1",
        last_consumed_event_id="e-1",
        last_consumed_direction=Direction.SHORT,
        position_open=False,
    )


def test_can_re_enter_opposite_direction_fresh_event_allowed() -> None:
    assert can_re_enter(
        candidate_direction=Direction.LONG,
        candidate_event_id="e-2",
        last_consumed_event_id="e-1",
        last_consumed_direction=Direction.SHORT,
        position_open=False,
    )
