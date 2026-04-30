"""Pure-function state transitions for the runtime control record.

Each transition takes a current ``RuntimeControlState`` plus context and
returns a new ``RuntimeControlState``. Transitions never mutate input
state; the runtime's persistence layer is responsible for writing the
new state durably.

Per Phase 3x §6.7 and `docs/07-risk/kill-switches.md`:

- Kill switch never auto-clears: only ``clear_kill_switch`` may unset
  it, and only when reconciliation/safety preconditions allow.
- Restart begins in SAFE_MODE: ``enter_running`` is allowed only from
  SAFE_MODE / RECOVERY_REQUIRED, and only if no blocking flag is set.
- Unknown state fails closed: callers that cannot trust the current
  state must raise ``UnknownStateError`` rather than transition.

These transitions are strategy-agnostic. They do not model real
position state, real exchange state, or real strategy progression.
"""

from __future__ import annotations

from .control import RuntimeControlState
from .errors import KillSwitchActiveError, RuntimeStateError
from .mode import RuntimeMode


def _derive_entries_blocked(
    *,
    runtime_mode: RuntimeMode,
    kill_switch_active: bool,
    paused_by_operator: bool,
    operator_review_required: bool,
    incident_active: bool,
) -> bool:
    """Return True iff any blocking condition implies entries blocked.

    Entries are blocked if the runtime mode is anything other than
    ``RUNNING`` *or* any blocking flag is asserted.
    """
    if runtime_mode is not RuntimeMode.RUNNING:
        return True
    if kill_switch_active:
        return True
    if paused_by_operator:
        return True
    if operator_review_required:
        return True
    if incident_active:
        return True
    return False


def enter_safe_mode(
    state: RuntimeControlState, *, reason: str, now_utc_ms: int
) -> RuntimeControlState:
    """Transition to SAFE_MODE.

    SAFE_MODE may be entered from any other mode. ``reason`` is recorded
    by the caller in the persistence/event layer; this function only
    updates the in-memory record.
    """
    del reason  # observability handled by caller; signature documents intent
    return state.with_changes(
        runtime_mode=RuntimeMode.SAFE_MODE,
        entries_blocked=_derive_entries_blocked(
            runtime_mode=RuntimeMode.SAFE_MODE,
            kill_switch_active=state.kill_switch_active,
            paused_by_operator=state.paused_by_operator,
            operator_review_required=state.operator_review_required,
            incident_active=state.incident_active,
        ),
        updated_at_utc_ms=now_utc_ms,
    )


def enter_running(
    state: RuntimeControlState, *, now_utc_ms: int
) -> RuntimeControlState:
    """Transition to RUNNING if all gates permit.

    Allowed only from ``SAFE_MODE`` or ``RECOVERY_REQUIRED``. If any
    blocking flag is asserted, raises ``RuntimeStateError`` rather than
    silently entering RUNNING with entries blocked — the caller must
    explicitly clear the blocking condition first.
    """
    if state.runtime_mode not in {RuntimeMode.SAFE_MODE, RuntimeMode.RECOVERY_REQUIRED}:
        raise RuntimeStateError(
            f"cannot enter RUNNING from {state.runtime_mode}; "
            f"allowed predecessors are SAFE_MODE and RECOVERY_REQUIRED"
        )
    if state.kill_switch_active:
        raise KillSwitchActiveError(
            "cannot enter RUNNING while kill switch is active"
        )
    if state.paused_by_operator:
        raise RuntimeStateError("cannot enter RUNNING while paused_by_operator is true")
    if state.operator_review_required:
        raise RuntimeStateError(
            "cannot enter RUNNING while operator_review_required is true"
        )
    if state.incident_active:
        raise RuntimeStateError("cannot enter RUNNING while incident_active is true")
    return state.with_changes(
        runtime_mode=RuntimeMode.RUNNING,
        entries_blocked=False,
        updated_at_utc_ms=now_utc_ms,
    )


def enter_blocked(
    state: RuntimeControlState, *, now_utc_ms: int
) -> RuntimeControlState:
    """Transition to BLOCKED.

    BLOCKED is entered when a blocking flag (kill switch, pause,
    operator review, incident) requires automated continuation to
    stop. The caller must have already set the relevant flag.
    """
    return state.with_changes(
        runtime_mode=RuntimeMode.BLOCKED,
        entries_blocked=True,
        updated_at_utc_ms=now_utc_ms,
    )


def enter_emergency(
    state: RuntimeControlState, *, now_utc_ms: int
) -> RuntimeControlState:
    """Transition to EMERGENCY.

    EMERGENCY is entered when an emergency condition (e.g., position
    without confirmed protection) requires emergency handling. Entries
    are forced blocked; ``incident_active`` is set; ``operator_review_required``
    is set per `docs/07-risk/stop-loss-policy.md` §Emergency Unprotected
    Policy.
    """
    return state.with_changes(
        runtime_mode=RuntimeMode.EMERGENCY,
        entries_blocked=True,
        incident_active=True,
        operator_review_required=True,
        updated_at_utc_ms=now_utc_ms,
    )


def enter_recovery_required(
    state: RuntimeControlState, *, now_utc_ms: int
) -> RuntimeControlState:
    """Transition to RECOVERY_REQUIRED.

    RECOVERY_REQUIRED indicates reconciliation must complete before
    normal continuation. Entries remain blocked.
    """
    return state.with_changes(
        runtime_mode=RuntimeMode.RECOVERY_REQUIRED,
        entries_blocked=True,
        updated_at_utc_ms=now_utc_ms,
    )


def activate_kill_switch(
    state: RuntimeControlState, *, now_utc_ms: int
) -> RuntimeControlState:
    """Activate the kill switch.

    Sets ``kill_switch_active = True``, ``operator_review_required = True``,
    ``entries_blocked = True``, and forces the runtime mode to BLOCKED if
    it was RUNNING. The kill switch is independent of incident state;
    callers may also set ``incident_active`` if appropriate.
    """
    new_mode = (
        RuntimeMode.BLOCKED if state.runtime_mode is RuntimeMode.RUNNING else state.runtime_mode
    )
    return state.with_changes(
        runtime_mode=new_mode,
        kill_switch_active=True,
        operator_review_required=True,
        entries_blocked=True,
        updated_at_utc_ms=now_utc_ms,
    )


def clear_kill_switch(
    state: RuntimeControlState, *, now_utc_ms: int
) -> RuntimeControlState:
    """Clear the kill switch under explicit operator action.

    Per `docs/07-risk/kill-switches.md` §Clearance Policy: kill switch
    must never auto-clear. The caller is responsible for verifying all
    clearance preconditions (no unprotected exposure, reconciliation
    clean, no severe incident, no security review pending) BEFORE
    invoking this transition. Clearing the kill switch does not
    automatically enter RUNNING — the runtime returns to SAFE_MODE
    pending explicit transition.
    """
    return state.with_changes(
        runtime_mode=RuntimeMode.SAFE_MODE,
        kill_switch_active=False,
        # operator_review_required intentionally preserved; clearing it
        # is a separate explicit action.
        entries_blocked=True,
        updated_at_utc_ms=now_utc_ms,
    )
