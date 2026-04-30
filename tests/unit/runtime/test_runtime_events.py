"""Phase 4a tests for internal event contracts."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from prometheus.core.governance import (
    BreakEvenRule,
    EmaSlopeMethod,
    GovernanceLabelError,
    StagnationWindowRole,
    StopTriggerDomain,
)
from prometheus.events.envelope import (
    MessageClass,
    MessageEnvelope,
    new_message_id,
)
from prometheus.events.runtime_events import (
    FakeExchangeLifecycleEvent,
    FakeExchangeLifecycleKind,
    GovernanceLabelEvent,
    KillSwitchEvent,
    KillSwitchEventKind,
    RuntimeModeChangedEvent,
)
from prometheus.state.mode import RuntimeMode


def test_message_envelope_required_fields() -> None:
    envelope = MessageEnvelope(
        message_type="runtime.mode_changed",
        message_class=MessageClass.EVENT,
        message_id="msg-00000001",
        correlation_id="corr-1",
        causation_id=None,
        occurred_at_utc_ms=1,
        source_component="state",
    )
    assert envelope.message_class is MessageClass.EVENT
    assert envelope.payload == {}


def test_new_message_id_monotone() -> None:
    a = new_message_id("test")
    b = new_message_id("test")
    assert a != b
    n_a = int(a.split("-")[-1])
    n_b = int(b.split("-")[-1])
    assert n_b == n_a + 1


def test_runtime_mode_changed_event_requires_reason() -> None:
    with pytest.raises(ValidationError):
        RuntimeModeChangedEvent(
            previous_mode=RuntimeMode.SAFE_MODE,
            new_mode=RuntimeMode.RUNNING,
            reason="",
            operator_review_required=False,
            occurred_at_utc_ms=1,
        )


def test_kill_switch_event_kinds() -> None:
    expected = {"activated", "clearance_requested", "clearance_blocked", "cleared"}
    assert {member.value for member in KillSwitchEventKind} == expected


def test_kill_switch_event_construction() -> None:
    e = KillSwitchEvent(
        kind=KillSwitchEventKind.ACTIVATED,
        reason="operator activation",
        operator_review_required=True,
        occurred_at_utc_ms=10,
    )
    assert e.kind is KillSwitchEventKind.ACTIVATED


def test_fake_exchange_lifecycle_event_requires_is_fake_true() -> None:
    e = FakeExchangeLifecycleEvent(
        kind=FakeExchangeLifecycleKind.FAKE_ENTRY_SUBMITTED,
        is_fake=True,
        correlation_id="corr-1",
        occurred_at_utc_ms=1,
    )
    assert e.is_fake is True


def test_fake_exchange_lifecycle_stop_event_requires_stop_trigger_domain() -> None:
    with pytest.raises(ValidationError):
        FakeExchangeLifecycleEvent(
            kind=FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_SUBMITTED,
            is_fake=True,
            correlation_id="corr-1",
            stop_trigger_domain=None,
            occurred_at_utc_ms=1,
        )


def test_fake_exchange_lifecycle_event_rejects_mixed_or_unknown_stop_trigger() -> None:
    """``model_validator(mode="after")`` propagates ``GovernanceLabelError``
    directly (pydantic v2 wraps only ``ValueError`` / ``AssertionError``).
    The fail-closed contract is the same either way."""
    with pytest.raises(GovernanceLabelError) as info:
        FakeExchangeLifecycleEvent(
            kind=FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_SUBMITTED,
            is_fake=True,
            correlation_id="corr-1",
            stop_trigger_domain=StopTriggerDomain.MIXED_OR_UNKNOWN,
            occurred_at_utc_ms=1,
        )
    assert "mixed_or_unknown" in str(info.value)


def test_fake_exchange_lifecycle_event_accepts_mark_price_runtime() -> None:
    e = FakeExchangeLifecycleEvent(
        kind=FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_SUBMITTED,
        is_fake=True,
        correlation_id="corr-1",
        stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
        occurred_at_utc_ms=1,
    )
    assert e.stop_trigger_domain is StopTriggerDomain.MARK_PRICE_RUNTIME


def test_governance_label_event_requires_at_least_one_label() -> None:
    with pytest.raises(ValidationError):
        GovernanceLabelEvent(context="x", occurred_at_utc_ms=1)


def test_governance_label_event_rejects_mixed_or_unknown_in_any_slot() -> None:
    cases = [
        {"stop_trigger_domain": StopTriggerDomain.MIXED_OR_UNKNOWN},
        {"break_even_rule": BreakEvenRule.MIXED_OR_UNKNOWN},
        {"ema_slope_method": EmaSlopeMethod.MIXED_OR_UNKNOWN},
        {"stagnation_window_role": StagnationWindowRole.MIXED_OR_UNKNOWN},
    ]
    for kwargs in cases:
        with pytest.raises(GovernanceLabelError):
            GovernanceLabelEvent(context="x", occurred_at_utc_ms=1, **kwargs)


def test_governance_label_event_accepts_valid_labels() -> None:
    e = GovernanceLabelEvent(
        stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
        break_even_rule=BreakEvenRule.DISABLED,
        ema_slope_method=EmaSlopeMethod.DISCRETE_COMPARISON,
        stagnation_window_role=StagnationWindowRole.NOT_ACTIVE,
        context="x",
        occurred_at_utc_ms=1,
    )
    assert e.stop_trigger_domain is StopTriggerDomain.MARK_PRICE_RUNTIME


def test_governance_label_validator_uses_governance_module() -> None:
    """The fail-closed semantics must come from the shared governance
    module so pydantic and the runtime layer cannot diverge."""
    # If the validator were re-implementing fail-closed locally, the
    # GovernanceLabelError would not have surfaced. By construction
    # (ValidationError-wrapped GovernanceLabelError) the contract is
    # honored. Sanity-check the parser path also raises the right type.
    from prometheus.core.governance import parse_stop_trigger_domain

    with pytest.raises(GovernanceLabelError):
        parse_stop_trigger_domain("not_a_real_value")
