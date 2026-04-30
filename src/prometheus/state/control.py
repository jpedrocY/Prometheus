"""Runtime control state record.

Per `docs/08-architecture/runtime-persistence-spec.md` §Entity 1, the
runtime control record represents current top-level runtime posture.
Phase 4a implements the strategy-agnostic subset.

Fields:

- ``runtime_mode``: top-level runtime mode (`RuntimeMode`).
- ``kill_switch_active``: whether the kill switch is asserted; persists
  across restart and never auto-clears (per `docs/07-risk/kill-switches.md`).
- ``paused_by_operator``: explicit operator pause.
- ``operator_review_required``: blocked-awaiting-operator flag.
- ``entries_blocked``: derived gate; if any blocking flag is true or
  the runtime mode is not RUNNING, entries are blocked.
- ``incident_active``: an incident is currently open and not yet
  resolved.
- ``updated_at_utc_ms``: last-update timestamp in canonical UTC ms.

The record is immutable (frozen dataclass-equivalent); state changes
produce new records via the helpers in
``prometheus.state.transitions``.

Phase 4a does NOT model active-trade or protection records — those
belong to the trade-lifecycle scope which requires a strategy and is
out of scope per Phase 3x §10.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .mode import RuntimeMode


class RuntimeControlState(BaseModel):
    """Restart-critical runtime control state.

    Use ``RuntimeControlState.with_changes(...)`` (or the helpers in
    ``prometheus.state.transitions``) to produce a new record; do not
    mutate fields in place.
    """

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
    )

    runtime_mode: RuntimeMode
    kill_switch_active: bool
    paused_by_operator: bool
    operator_review_required: bool
    entries_blocked: bool
    incident_active: bool
    updated_at_utc_ms: int

    def with_changes(self, **changes: object) -> RuntimeControlState:
        """Return a new ``RuntimeControlState`` with the given changes applied."""
        # ``model_copy`` preserves field validation.
        return self.model_copy(update=changes)


def fresh_control_state(now_utc_ms: int) -> RuntimeControlState:
    """Return the canonical fresh-startup runtime control state.

    On every process start the runtime enters ``SAFE_MODE`` with all
    blocking flags cleared and ``entries_blocked = True``. This is the
    canonical "no exposure, no commitments, supervised" baseline.
    """
    return RuntimeControlState(
        runtime_mode=RuntimeMode.SAFE_MODE,
        kill_switch_active=False,
        paused_by_operator=False,
        operator_review_required=False,
        entries_blocked=True,
        incident_active=False,
        updated_at_utc_ms=now_utc_ms,
    )
