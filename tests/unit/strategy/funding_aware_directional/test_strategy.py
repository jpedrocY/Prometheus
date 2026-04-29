"""D1-A FundingAwareStrategy facade tests (Phase 3i-A scope).

Stateless per-call evaluation tests: no engine, no time-stop counting,
no per-trade lifecycle. The facade combines the primitive helpers
into a single ``evaluate_entry_signal`` method.
"""

from __future__ import annotations

from prometheus.strategy.funding_aware_directional import (
    FundingAwareConfig,
    FundingAwareStrategy,
    FundingEvent,
)
from prometheus.strategy.types import Direction


def _build_prior_rates(n: int = 270, value: float = 0.0) -> list[float]:
    # Alternating ±1 produces sample mean ≈ 0 and sample std ≈ 1.
    return [1.0 if i % 2 == 0 else -1.0 for i in range(n)]


def test_evaluate_entry_no_eligible_event_returns_none() -> None:
    strat = FundingAwareStrategy()
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=_build_prior_rates(),
        funding_events=[],
        atr20_at_b=2.5,
        reference_price=100.0,
    )
    assert out is None


def test_evaluate_entry_below_threshold_returns_none() -> None:
    """A funding rate of 0.0 produces Z ≈ 0 -> no extreme-event signal."""
    strat = FundingAwareStrategy()
    events = [FundingEvent(event_id="e-1", funding_time=900, funding_rate=0.0)]
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=_build_prior_rates(),
        funding_events=events,
        atr20_at_b=2.5,
        reference_price=100.0,
    )
    assert out is None


def test_evaluate_entry_short_signal_at_positive_extreme() -> None:
    """Z ≈ +3 contrarian SHORT signal."""
    strat = FundingAwareStrategy()
    events = [FundingEvent(event_id="e-1", funding_time=900, funding_rate=3.0)]
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=_build_prior_rates(),
        funding_events=events,
        atr20_at_b=2.5,
        reference_price=100.0,
    )
    assert out is not None
    assert out.direction == Direction.SHORT
    assert out.signal_bar_index == 100
    assert out.funding_event_id == "e-1"
    assert out.reference_price == 100.0
    assert out.atr_at_signal == 2.5
    # SHORT stop above fill_price
    assert out.initial_stop > out.reference_price
    # SHORT target below fill_price (contrarian; favorable direction down)
    assert out.target_price < out.reference_price
    # +2.0R target geometry
    assert abs((out.reference_price - out.target_price) - 2.0 * out.stop_distance) < 1e-9


def test_evaluate_entry_long_signal_at_negative_extreme() -> None:
    strat = FundingAwareStrategy()
    events = [FundingEvent(event_id="e-1", funding_time=900, funding_rate=-3.0)]
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=_build_prior_rates(),
        funding_events=events,
        atr20_at_b=2.5,
        reference_price=100.0,
    )
    assert out is not None
    assert out.direction == Direction.LONG
    # LONG stop below fill, target above
    assert out.initial_stop < out.reference_price
    assert out.target_price > out.reference_price
    # +2.0R target geometry
    assert abs((out.target_price - out.reference_price) - 2.0 * out.stop_distance) < 1e-9


def test_evaluate_entry_blocked_by_cooldown_same_direction_same_event() -> None:
    strat = FundingAwareStrategy()
    events = [FundingEvent(event_id="e-1", funding_time=900, funding_rate=3.0)]
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=_build_prior_rates(),
        funding_events=events,
        atr20_at_b=2.5,
        reference_price=100.0,
        last_consumed_event_id="e-1",
        last_consumed_direction=Direction.SHORT,
        position_open=False,
    )
    assert out is None


def test_evaluate_entry_allows_opposite_direction_same_event() -> None:
    """Opposite-direction never cooldown-blocked at the same event."""
    strat = FundingAwareStrategy()
    # Negative funding extreme would normally produce LONG; ensure we
    # also allow LONG when the prior consumed event was SHORT.
    events = [FundingEvent(event_id="e-1", funding_time=900, funding_rate=-3.0)]
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=_build_prior_rates(),
        funding_events=events,
        atr20_at_b=2.5,
        reference_price=100.0,
        last_consumed_event_id="e-1",
        last_consumed_direction=Direction.SHORT,
        position_open=False,
    )
    assert out is not None
    assert out.direction == Direction.LONG


def test_evaluate_entry_blocked_when_position_open() -> None:
    strat = FundingAwareStrategy()
    events = [FundingEvent(event_id="e-1", funding_time=900, funding_rate=3.0)]
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=_build_prior_rates(),
        funding_events=events,
        atr20_at_b=2.5,
        reference_price=100.0,
        position_open=True,
    )
    assert out is None


def test_evaluate_entry_warmup_returns_none() -> None:
    """Fewer than 270 prior events -> Z is NaN -> no signal."""
    strat = FundingAwareStrategy()
    events = [FundingEvent(event_id="e-1", funding_time=900, funding_rate=3.0)]
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=[0.0001] * 200,  # warmup
        funding_events=events,
        atr20_at_b=2.5,
        reference_price=100.0,
    )
    assert out is None


def test_evaluate_entry_time_stop_trigger_index() -> None:
    """time_stop_trigger_bar_index = (b_index + 1) + 32 per Phase 3g §6.9
    (entry fill bar = B+1; time-stop triggers at close of B+1+32)."""
    strat = FundingAwareStrategy()
    events = [FundingEvent(event_id="e-1", funding_time=900, funding_rate=3.0)]
    out = strat.evaluate_entry_signal(
        b_index=100,
        bar_close_time=1000,
        prior_funding_rates=_build_prior_rates(),
        funding_events=events,
        atr20_at_b=2.5,
        reference_price=100.0,
    )
    assert out is not None
    # b_index = 100 -> entry fill at B+1 = 101 -> trigger bar = 101 + 32 = 133
    assert out.time_stop_trigger_bar_index == 133


def test_strategy_uses_locked_config_by_default() -> None:
    strat = FundingAwareStrategy()
    assert strat.config == FundingAwareConfig()
    assert strat.config.target_r_multiple == 2.0  # Phase 3g §5.6.5 Option A
    assert strat.config.time_stop_bars == 32
    assert strat.config.funding_z_score_threshold == 2.0
