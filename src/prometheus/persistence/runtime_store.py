"""SQLite-backed store for the runtime control state.

The store persists the single current runtime control record plus an
append-only history of mode-change events for audit. It does NOT
persist secrets, credentials, or any sensitive material.

On startup the store provides ``load_persisted()`` which returns the
last-known persisted record (if any) for inspection — but the runtime
must NOT resume RUNNING from this record. Per
`docs/08-architecture/state-model.md` §Startup rule and Phase 3x §9.2,
the runtime constructs a fresh SAFE_MODE record via
``prometheus.state.fresh_control_state(now_utc_ms)`` and persists that
as the new current state. Persisted ``kill_switch_active`` is
preserved across restart; persisted ``operator_review_required`` and
``incident_active`` are preserved. The runtime mode itself is reset
to SAFE_MODE.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from prometheus.core.errors import PrometheusError
from prometheus.core.governance import (
    BreakEvenRule,
    EmaSlopeMethod,
    StagnationWindowRole,
    StopTriggerDomain,
    require_valid,
)
from prometheus.state.control import RuntimeControlState
from prometheus.state.mode import RuntimeMode

_SCHEMA_DDL = (
    """
    CREATE TABLE IF NOT EXISTS runtime_control (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        runtime_mode TEXT NOT NULL,
        kill_switch_active INTEGER NOT NULL CHECK (kill_switch_active IN (0, 1)),
        paused_by_operator INTEGER NOT NULL CHECK (paused_by_operator IN (0, 1)),
        operator_review_required INTEGER NOT NULL CHECK (operator_review_required IN (0, 1)),
        entries_blocked INTEGER NOT NULL CHECK (entries_blocked IN (0, 1)),
        incident_active INTEGER NOT NULL CHECK (incident_active IN (0, 1)),
        updated_at_utc_ms INTEGER NOT NULL CHECK (updated_at_utc_ms > 0)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS runtime_mode_event (
        rowid_pk INTEGER PRIMARY KEY AUTOINCREMENT,
        previous_mode TEXT NOT NULL,
        new_mode TEXT NOT NULL,
        reason TEXT NOT NULL,
        kill_switch_active INTEGER NOT NULL CHECK (kill_switch_active IN (0, 1)),
        operator_review_required INTEGER NOT NULL CHECK (operator_review_required IN (0, 1)),
        incident_active INTEGER NOT NULL CHECK (incident_active IN (0, 1)),
        occurred_at_utc_ms INTEGER NOT NULL CHECK (occurred_at_utc_ms > 0)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS governance_label_audit (
        rowid_pk INTEGER PRIMARY KEY AUTOINCREMENT,
        scheme TEXT NOT NULL CHECK (scheme IN (
            'stop_trigger_domain',
            'break_even_rule',
            'ema_slope_method',
            'stagnation_window_role'
        )),
        value TEXT NOT NULL,
        context TEXT NOT NULL,
        recorded_at_utc_ms INTEGER NOT NULL CHECK (recorded_at_utc_ms > 0)
    );
    """,
)

_PRAGMAS = (
    "PRAGMA journal_mode = WAL;",
    "PRAGMA foreign_keys = ON;",
    "PRAGMA synchronous = FULL;",
    "PRAGMA busy_timeout = 5000;",
)


class RuntimeStoreError(PrometheusError):
    """Raised when the persistence layer rejects a write or read."""


class RuntimeStore:
    """SQLite-backed store for the runtime control record.

    Lifecycle:

    1. Construct with a database path (file or ``":memory:"``).
    2. Call ``initialize()`` once per process to apply schema + pragmas.
    3. Call ``load_persisted()`` to retrieve the last persisted record
       for inspection (do NOT auto-resume from it).
    4. Call ``save(record)`` to persist a new current state.
    5. Call ``record_mode_event(...)`` to append to the audit log.

    The store deliberately does not own a long-lived connection; it
    opens a connection per operation and closes it cleanly. This
    matches the Phase 4a "no background services / no daemon"
    constraint.
    """

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self._db_path)
        try:
            for pragma in _PRAGMAS:
                connection.execute(pragma)
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        """Apply schema and pragmas. Idempotent."""
        with self._connect() as connection:
            for ddl in _SCHEMA_DDL:
                connection.execute(ddl)

    def load_persisted(self) -> RuntimeControlState | None:
        """Return the last-persisted control state, or None if none exists.

        The runtime must NOT use this record as the resumed runtime
        state. Per Phase 3x §9.2 / `state-model.md` §Startup rule, the
        runtime always begins in SAFE_MODE on every process start. The
        persisted record is used only to *carry forward* fields that
        must survive restart: ``kill_switch_active``,
        ``operator_review_required``, ``incident_active``,
        ``paused_by_operator``.
        """
        with self._connect() as connection:
            cursor = connection.execute(
                "SELECT runtime_mode, kill_switch_active, paused_by_operator, "
                "operator_review_required, entries_blocked, incident_active, "
                "updated_at_utc_ms FROM runtime_control WHERE id = 1"
            )
            row = cursor.fetchone()
        if row is None:
            return None
        runtime_mode_value, kill, paused, review, blocked, incident, updated_ms = row
        try:
            runtime_mode = RuntimeMode(runtime_mode_value)
        except ValueError as exc:
            raise RuntimeStoreError(
                f"persisted runtime_mode {runtime_mode_value!r} is not a valid RuntimeMode"
            ) from exc
        return RuntimeControlState(
            runtime_mode=runtime_mode,
            kill_switch_active=bool(kill),
            paused_by_operator=bool(paused),
            operator_review_required=bool(review),
            entries_blocked=bool(blocked),
            incident_active=bool(incident),
            updated_at_utc_ms=int(updated_ms),
        )

    def save(self, state: RuntimeControlState) -> None:
        """Persist the current control state (single-row table).

        Idempotent on the (id = 1) row; later writes overwrite earlier
        writes via UPSERT.
        """
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO runtime_control (id, runtime_mode, kill_switch_active, "
                "paused_by_operator, operator_review_required, entries_blocked, "
                "incident_active, updated_at_utc_ms) "
                "VALUES (1, ?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET "
                "runtime_mode = excluded.runtime_mode, "
                "kill_switch_active = excluded.kill_switch_active, "
                "paused_by_operator = excluded.paused_by_operator, "
                "operator_review_required = excluded.operator_review_required, "
                "entries_blocked = excluded.entries_blocked, "
                "incident_active = excluded.incident_active, "
                "updated_at_utc_ms = excluded.updated_at_utc_ms",
                (
                    state.runtime_mode.value,
                    int(state.kill_switch_active),
                    int(state.paused_by_operator),
                    int(state.operator_review_required),
                    int(state.entries_blocked),
                    int(state.incident_active),
                    state.updated_at_utc_ms,
                ),
            )

    def record_mode_event(
        self,
        *,
        previous: RuntimeControlState,
        new: RuntimeControlState,
        reason: str,
    ) -> None:
        """Append an audit row for a runtime-mode change."""
        if not reason:
            raise RuntimeStoreError("mode-event reason must be a non-empty string")
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO runtime_mode_event (previous_mode, new_mode, reason, "
                "kill_switch_active, operator_review_required, incident_active, "
                "occurred_at_utc_ms) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    previous.runtime_mode.value,
                    new.runtime_mode.value,
                    reason,
                    int(new.kill_switch_active),
                    int(new.operator_review_required),
                    int(new.incident_active),
                    new.updated_at_utc_ms,
                ),
            )

    def record_governance_label(
        self,
        *,
        label: StopTriggerDomain | BreakEvenRule | EmaSlopeMethod | StagnationWindowRole,
        context: str,
        recorded_at_utc_ms: int,
    ) -> None:
        """Persist a governance label observation to the audit table.

        Fails closed (raises ``GovernanceLabelError``) if the label
        value is ``mixed_or_unknown``. This enforces the Phase 3v §8.4
        / Phase 3w §6.3 / §7.3 / §8.3 fail-closed rule at the
        persistence boundary.
        """
        require_valid(label)
        scheme = _scheme_for_label(label)
        if not context:
            raise RuntimeStoreError("governance-label context must be non-empty")
        if recorded_at_utc_ms <= 0:
            raise RuntimeStoreError("recorded_at_utc_ms must be positive")
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO governance_label_audit (scheme, value, context, "
                "recorded_at_utc_ms) VALUES (?, ?, ?, ?)",
                (scheme, label.value, context, recorded_at_utc_ms),
            )


def _scheme_for_label(
    label: StopTriggerDomain | BreakEvenRule | EmaSlopeMethod | StagnationWindowRole,
) -> str:
    if isinstance(label, StopTriggerDomain):
        return "stop_trigger_domain"
    if isinstance(label, BreakEvenRule):
        return "break_even_rule"
    if isinstance(label, EmaSlopeMethod):
        return "ema_slope_method"
    if isinstance(label, StagnationWindowRole):
        return "stagnation_window_role"
    raise RuntimeStoreError(
        f"unknown governance label type: {type(label).__name__}"
    )
