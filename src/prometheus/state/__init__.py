"""Runtime state model for the Phase 4a local safe runtime foundation.

This package owns the in-process runtime state machine, the
``RuntimeMode`` enum, and the ``RuntimeControlState`` record. It is
strategy-agnostic and exchange-write-free per Phase 3x §5 / §6.

The state model is consumed by:

- ``prometheus.persistence`` — durable persistence of restart-critical
  runtime control state.
- ``prometheus.events`` — runtime mode-change events.
- ``prometheus.execution.fake_adapter`` — fake-exchange decisions
  gated on runtime mode.
- ``prometheus.operator.state_view`` — read-only operator surface.

Per Phase 3x §5 / §6, this package must NOT import from any module
that talks to a real exchange, places orders, or implements a strategy.
"""

from __future__ import annotations

from .errors import (
    EntriesBlockedError,
    KillSwitchActiveError,
    RuntimeStateError,
    UnknownStateError,
)
from .mode import RuntimeMode
from .control import RuntimeControlState, fresh_control_state
from .transitions import (
    activate_kill_switch,
    clear_kill_switch,
    enter_blocked,
    enter_emergency,
    enter_recovery_required,
    enter_running,
    enter_safe_mode,
)

__all__ = [
    "EntriesBlockedError",
    "KillSwitchActiveError",
    "RuntimeControlState",
    "RuntimeMode",
    "RuntimeStateError",
    "UnknownStateError",
    "activate_kill_switch",
    "clear_kill_switch",
    "enter_blocked",
    "enter_emergency",
    "enter_recovery_required",
    "enter_running",
    "enter_safe_mode",
    "fresh_control_state",
]
