"""Runtime-state-specific errors."""

from __future__ import annotations

from prometheus.core.errors import PrometheusError


class RuntimeStateError(PrometheusError):
    """Base class for runtime state errors."""


class UnknownStateError(RuntimeStateError):
    """Raised when the runtime cannot trust the current state.

    Per `docs/08-architecture/state-model.md` §State-Model Principles 4
    and `.claude/rules/prometheus-safety.md`: unknown state must fail
    closed. Raising this exception is the canonical fail-closed signal
    for the state-model layer.
    """


class KillSwitchActiveError(RuntimeStateError):
    """Raised when an action is rejected because the kill switch is active.

    Per `docs/07-risk/kill-switches.md`: kill switch blocks new entries
    and normal strategy progression; only controlled safety actions are
    allowed.
    """


class EntriesBlockedError(RuntimeStateError):
    """Raised when an entry attempt is rejected because entries are blocked."""
