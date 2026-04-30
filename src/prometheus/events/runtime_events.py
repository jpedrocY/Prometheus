"""Runtime event payloads.

Each payload is a frozen pydantic model with strict validation. Where
a payload carries a governance label, the model's validator rejects
``mixed_or_unknown`` by calling ``prometheus.core.governance.require_valid``,
implementing the fail-closed rule at the event-validation boundary
(per Phase 3v §8.4 / Phase 3w §6.3 / §7.3 / §8.3).
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from prometheus.core.governance import (
    BreakEvenRule,
    EmaSlopeMethod,
    StagnationWindowRole,
    StopTriggerDomain,
    require_valid,
)
from prometheus.state.mode import RuntimeMode


class RuntimeModeChangedEvent(BaseModel):
    """Fact: runtime mode transitioned."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    previous_mode: RuntimeMode
    new_mode: RuntimeMode
    reason: str = Field(min_length=1)
    operator_review_required: bool
    occurred_at_utc_ms: int = Field(gt=0)


class KillSwitchEventKind(StrEnum):
    """Kill-switch event subtypes."""

    ACTIVATED = "activated"
    CLEARANCE_REQUESTED = "clearance_requested"
    CLEARANCE_BLOCKED = "clearance_blocked"
    CLEARED = "cleared"


class KillSwitchEvent(BaseModel):
    """Fact: kill-switch state changed."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    kind: KillSwitchEventKind
    reason: str = Field(min_length=1)
    operator_review_required: bool
    occurred_at_utc_ms: int = Field(gt=0)


class FakeExchangeLifecycleKind(StrEnum):
    """Fake-exchange lifecycle event subtypes (clearly fake/local)."""

    FAKE_ENTRY_SUBMITTED = "fake_entry_submitted"
    FAKE_FILL_CONFIRMED = "fake_fill_confirmed"
    FAKE_POSITION_CONFIRMED = "fake_position_confirmed"
    FAKE_PROTECTIVE_STOP_SUBMITTED = "fake_protective_stop_submitted"
    FAKE_PROTECTIVE_STOP_CONFIRMED = "fake_protective_stop_confirmed"
    FAKE_STOP_TRIGGERED = "fake_stop_triggered"
    FAKE_SUBMISSION_TIMEOUT = "fake_submission_timeout"
    FAKE_UNKNOWN_OUTCOME = "fake_unknown_outcome"


class FakeExchangeLifecycleEvent(BaseModel):
    """Fact: a fake-exchange lifecycle transition occurred.

    All instances of this event carry ``is_fake = True`` to make it
    syntactically impossible for downstream code to confuse fake events
    with live exchange truth.

    Where the event involves stop-trigger semantics, the
    ``stop_trigger_domain`` field is required and validated for
    fail-closed semantics.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    kind: FakeExchangeLifecycleKind
    is_fake: bool = True
    correlation_id: str = Field(min_length=1)
    stop_trigger_domain: StopTriggerDomain | None = None
    occurred_at_utc_ms: int = Field(gt=0)

    @model_validator(mode="after")
    def _validate(self) -> FakeExchangeLifecycleEvent:
        if self.is_fake is not True:
            raise ValueError("FakeExchangeLifecycleEvent.is_fake must always be True")
        if self.stop_trigger_domain is not None:
            require_valid(self.stop_trigger_domain)
        # Stop-bearing event kinds must carry a stop_trigger_domain.
        stop_bearing = {
            FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_SUBMITTED,
            FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_CONFIRMED,
            FakeExchangeLifecycleKind.FAKE_STOP_TRIGGERED,
        }
        if self.kind in stop_bearing and self.stop_trigger_domain is None:
            raise ValueError(
                f"{self.kind} event requires a stop_trigger_domain "
                "(fail-closed per Phase 3v §8.4)"
            )
        return self


class GovernanceLabelEvent(BaseModel):
    """Fact: a governance-label observation was recorded.

    Used to record (in event form) the appearance of a label in a
    runtime decision. Validates fail-closed semantics for whichever
    label is populated. At least one label must be populated.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    stop_trigger_domain: StopTriggerDomain | None = None
    break_even_rule: BreakEvenRule | None = None
    ema_slope_method: EmaSlopeMethod | None = None
    stagnation_window_role: StagnationWindowRole | None = None
    context: str = Field(min_length=1)
    occurred_at_utc_ms: int = Field(gt=0)

    @model_validator(mode="after")
    def _validate(self) -> GovernanceLabelEvent:
        present = [
            self.stop_trigger_domain,
            self.break_even_rule,
            self.ema_slope_method,
            self.stagnation_window_role,
        ]
        if all(x is None for x in present):
            raise ValueError(
                "GovernanceLabelEvent must include at least one label"
            )
        for label in present:
            if label is not None:
                require_valid(label)
        return self
