"""Phase 4a tests for the runtime state model and transitions."""

from __future__ import annotations

import pytest

from prometheus.state.control import RuntimeControlState, fresh_control_state
from prometheus.state.errors import KillSwitchActiveError, RuntimeStateError
from prometheus.state.mode import RuntimeMode
from prometheus.state.transitions import (
    activate_kill_switch,
    clear_kill_switch,
    enter_blocked,
    enter_emergency,
    enter_recovery_required,
    enter_running,
    enter_safe_mode,
)


def _baseline() -> RuntimeControlState:
    return fresh_control_state(now_utc_ms=1)


def test_fresh_control_state_defaults_to_safe_mode() -> None:
    s = _baseline()
    assert s.runtime_mode is RuntimeMode.SAFE_MODE
    assert s.kill_switch_active is False
    assert s.paused_by_operator is False
    assert s.operator_review_required is False
    assert s.entries_blocked is True
    assert s.incident_active is False
    assert s.updated_at_utc_ms == 1


def test_runtime_modes_match_phase_4a_requirements() -> None:
    expected = {"SAFE_MODE", "RUNNING", "BLOCKED", "EMERGENCY", "RECOVERY_REQUIRED"}
    assert {m.value for m in RuntimeMode} == expected


def test_enter_running_from_safe_mode_succeeds_when_no_blockers() -> None:
    s = _baseline()
    new = enter_running(s, now_utc_ms=2)
    assert new.runtime_mode is RuntimeMode.RUNNING
    assert new.entries_blocked is False
    assert new.updated_at_utc_ms == 2


def test_enter_running_blocked_by_kill_switch() -> None:
    s = activate_kill_switch(_baseline(), now_utc_ms=2)
    with pytest.raises(KillSwitchActiveError):
        enter_running(s, now_utc_ms=3)


def test_enter_running_blocked_by_pause() -> None:
    s = _baseline().with_changes(paused_by_operator=True)
    with pytest.raises(RuntimeStateError):
        enter_running(s, now_utc_ms=2)


def test_enter_running_blocked_by_operator_review_required() -> None:
    s = _baseline().with_changes(operator_review_required=True)
    with pytest.raises(RuntimeStateError):
        enter_running(s, now_utc_ms=2)


def test_enter_running_blocked_by_incident_active() -> None:
    s = _baseline().with_changes(incident_active=True)
    with pytest.raises(RuntimeStateError):
        enter_running(s, now_utc_ms=2)


def test_enter_running_only_from_safe_mode_or_recovery_required() -> None:
    # First reach RUNNING legitimately.
    running = enter_running(_baseline(), now_utc_ms=2)
    # Cannot transition RUNNING -> RUNNING via this transition.
    with pytest.raises(RuntimeStateError):
        enter_running(running, now_utc_ms=3)
    # BLOCKED -> RUNNING is also forbidden via this transition.
    blocked = enter_blocked(running, now_utc_ms=3)
    with pytest.raises(RuntimeStateError):
        enter_running(blocked, now_utc_ms=4)


def test_kill_switch_activation_forces_blocked_when_running() -> None:
    running = enter_running(_baseline(), now_utc_ms=2)
    after = activate_kill_switch(running, now_utc_ms=3)
    assert after.kill_switch_active is True
    assert after.runtime_mode is RuntimeMode.BLOCKED
    assert after.operator_review_required is True
    assert after.entries_blocked is True


def test_kill_switch_does_not_change_mode_outside_running() -> None:
    safe = _baseline()
    after = activate_kill_switch(safe, now_utc_ms=2)
    assert after.kill_switch_active is True
    assert after.runtime_mode is RuntimeMode.SAFE_MODE
    assert after.operator_review_required is True
    assert after.entries_blocked is True


def test_clear_kill_switch_returns_to_safe_mode_not_running() -> None:
    activated = activate_kill_switch(_baseline(), now_utc_ms=2)
    cleared = clear_kill_switch(activated, now_utc_ms=3)
    assert cleared.kill_switch_active is False
    assert cleared.runtime_mode is RuntimeMode.SAFE_MODE
    # operator_review_required is preserved; clearing kill switch is
    # not the same as clearing operator review.
    assert cleared.operator_review_required is True
    assert cleared.entries_blocked is True


def test_enter_emergency_sets_incident_and_review() -> None:
    e = enter_emergency(_baseline(), now_utc_ms=5)
    assert e.runtime_mode is RuntimeMode.EMERGENCY
    assert e.entries_blocked is True
    assert e.incident_active is True
    assert e.operator_review_required is True


def test_enter_recovery_required_blocks_entries() -> None:
    r = enter_recovery_required(_baseline(), now_utc_ms=5)
    assert r.runtime_mode is RuntimeMode.RECOVERY_REQUIRED
    assert r.entries_blocked is True


def test_enter_safe_mode_idempotent() -> None:
    s1 = _baseline()
    s2 = enter_safe_mode(s1, reason="test", now_utc_ms=3)
    assert s2.runtime_mode is RuntimeMode.SAFE_MODE
    assert s2.entries_blocked is True


def test_runtime_control_state_is_immutable() -> None:
    s = _baseline()
    # pydantic v2 raises ``ValidationError`` for assignment on a
    # frozen model. We assert against that specific type rather than
    # blind ``Exception``.
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        s.runtime_mode = RuntimeMode.RUNNING  # type: ignore[misc]
