"""Phase 4a tests for the deterministic local fake-exchange adapter."""

from __future__ import annotations

import pytest

from prometheus.core.governance import (
    GovernanceLabelError,
    StopTriggerDomain,
)
from prometheus.core.symbols import Symbol
from prometheus.events.runtime_events import FakeExchangeLifecycleKind
from prometheus.execution.fake_adapter import (
    FakeExchangeAdapter,
    FakeExchangeError,
)
from prometheus.risk.exposure import PositionSide


def _adapter(now: int = 100) -> FakeExchangeAdapter:
    return FakeExchangeAdapter(symbol=Symbol.BTCUSDT, clock=lambda: now)


def test_adapter_starts_with_no_position_or_stop() -> None:
    adapter = _adapter()
    assert adapter.position_state.has_position is False
    assert adapter.stop_state.has_stop is False
    assert adapter.is_entry_in_flight is False
    assert adapter.emitted_events == ()


def test_happy_path_signal_to_protected_position() -> None:
    """Phase 4a fake-exchange happy path:
    fake entry submission -> fake fill -> fake position confirmed
    -> fake protective stop submitted -> fake stop confirmed."""
    adapter = _adapter()
    correlation = "trade-1"
    domain = StopTriggerDomain.MARK_PRICE_RUNTIME

    adapter.submit_entry_order(
        correlation_id=correlation,
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    assert adapter.is_entry_in_flight is True

    adapter.confirm_fake_fill(correlation_id=correlation)
    assert adapter.position_state.has_position is True
    assert adapter.position_state.side is PositionSide.LONG
    assert adapter.is_entry_in_flight is False

    adapter.submit_protective_stop(
        correlation_id=correlation,
        stop_price=49_500.0,
        stop_trigger_domain=domain,
    )
    assert adapter.stop_state.has_stop is True
    assert adapter.stop_state.confirmed is False

    adapter.confirm_fake_protective_stop(
        correlation_id=correlation, stop_trigger_domain=domain
    )
    assert adapter.stop_state.confirmed is True

    kinds = [event.kind for event in adapter.emitted_events]
    assert kinds == [
        FakeExchangeLifecycleKind.FAKE_ENTRY_SUBMITTED,
        FakeExchangeLifecycleKind.FAKE_FILL_CONFIRMED,
        FakeExchangeLifecycleKind.FAKE_POSITION_CONFIRMED,
        FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_SUBMITTED,
        FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_CONFIRMED,
    ]
    for event in adapter.emitted_events:
        assert event.is_fake is True


def test_failure_path_unknown_outcome_blocks_progression() -> None:
    """Phase 4a fake-exchange failure path:
    fake submission timeout / unknown outcome -> fail closed."""
    adapter = _adapter()
    adapter.submit_entry_order(
        correlation_id="trade-1",
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    adapter.mark_entry_unknown_outcome(correlation_id="trade-1")
    assert adapter.position_state.has_position is False
    assert adapter.is_entry_in_flight is True
    kinds = [event.kind for event in adapter.emitted_events]
    assert FakeExchangeLifecycleKind.FAKE_UNKNOWN_OUTCOME in kinds


def test_stop_submission_failure_after_fill_signals_emergency() -> None:
    """fake fill confirmed + fake stop submission failed -> protection
    cannot be confirmed -> the runtime is expected to enter EMERGENCY."""
    adapter = _adapter()
    domain = StopTriggerDomain.MARK_PRICE_RUNTIME
    adapter.submit_entry_order(
        correlation_id="trade-1",
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    adapter.confirm_fake_fill(correlation_id="trade-1")
    adapter.mark_stop_submission_failed(
        correlation_id="trade-1", stop_trigger_domain=domain
    )
    assert adapter.position_state.has_position is True
    assert adapter.stop_state.has_stop is False
    assert adapter.stop_state.submission_failed is True


def test_protective_stop_requires_position() -> None:
    adapter = _adapter()
    with pytest.raises(FakeExchangeError):
        adapter.submit_protective_stop(
            correlation_id="trade-1",
            stop_price=49_500.0,
            stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
        )


def test_double_entry_submission_rejected() -> None:
    adapter = _adapter()
    adapter.submit_entry_order(
        correlation_id="trade-1",
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    with pytest.raises(FakeExchangeError):
        adapter.submit_entry_order(
            correlation_id="trade-2",
            side=PositionSide.LONG,
            quantity=0.045,
            price=50_000.0,
        )


def test_mismatched_correlation_id_rejected() -> None:
    adapter = _adapter()
    adapter.submit_entry_order(
        correlation_id="trade-1",
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    with pytest.raises(FakeExchangeError):
        adapter.confirm_fake_fill(correlation_id="other")


def test_protective_stop_rejects_mixed_or_unknown_label() -> None:
    adapter = _adapter()
    adapter.submit_entry_order(
        correlation_id="trade-1",
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    adapter.confirm_fake_fill(correlation_id="trade-1")
    with pytest.raises(GovernanceLabelError):
        adapter.submit_protective_stop(
            correlation_id="trade-1",
            stop_price=49_500.0,
            stop_trigger_domain=StopTriggerDomain.MIXED_OR_UNKNOWN,
        )


def test_stop_trigger_event_clears_position_and_stop() -> None:
    adapter = _adapter()
    domain = StopTriggerDomain.MARK_PRICE_RUNTIME
    adapter.submit_entry_order(
        correlation_id="trade-1",
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    adapter.confirm_fake_fill(correlation_id="trade-1")
    adapter.submit_protective_stop(
        correlation_id="trade-1",
        stop_price=49_500.0,
        stop_trigger_domain=domain,
    )
    adapter.confirm_fake_protective_stop(
        correlation_id="trade-1", stop_trigger_domain=domain
    )
    adapter.trigger_fake_stop(
        correlation_id="trade-1", stop_trigger_domain=domain
    )
    assert adapter.position_state.has_position is False
    assert adapter.stop_state.has_stop is False
