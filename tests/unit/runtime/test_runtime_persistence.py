"""Phase 4a tests for SQLite-backed runtime control persistence."""

from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.core.governance import (
    BreakEvenRule,
    EmaSlopeMethod,
    GovernanceLabelError,
    StagnationWindowRole,
    StopTriggerDomain,
)
from prometheus.persistence.runtime_store import RuntimeStore, RuntimeStoreError
from prometheus.state.control import fresh_control_state
from prometheus.state.mode import RuntimeMode
from prometheus.state.transitions import activate_kill_switch, enter_running


def _new_store(tmp_path: Path) -> RuntimeStore:
    store = RuntimeStore(tmp_path / "runtime.db")
    store.initialize()
    return store


def test_load_persisted_returns_none_when_empty(tmp_path: Path) -> None:
    store = _new_store(tmp_path)
    assert store.load_persisted() is None


def test_save_and_load_round_trip_preserves_fields(tmp_path: Path) -> None:
    store = _new_store(tmp_path)
    s = fresh_control_state(now_utc_ms=42).with_changes(
        kill_switch_active=True,
        operator_review_required=True,
        incident_active=True,
        updated_at_utc_ms=42,
    )
    store.save(s)
    loaded = store.load_persisted()
    assert loaded == s


def test_save_overwrites_existing_record(tmp_path: Path) -> None:
    store = _new_store(tmp_path)
    s1 = fresh_control_state(now_utc_ms=10)
    store.save(s1)
    s2 = enter_running(s1, now_utc_ms=11)
    store.save(s2)
    loaded = store.load_persisted()
    assert loaded is not None
    assert loaded.runtime_mode is RuntimeMode.RUNNING


def test_persisted_running_does_not_auto_resume_running(tmp_path: Path) -> None:
    """Phase 3x §9.2 / state-model.md §Startup rule: every process start
    enters SAFE_MODE regardless of last persisted mode."""
    store = _new_store(tmp_path)
    running = enter_running(fresh_control_state(now_utc_ms=10), now_utc_ms=11)
    store.save(running)

    # Simulated "next process start": do NOT auto-resume from persisted
    # record. Construct fresh SAFE_MODE state instead.
    persisted = store.load_persisted()
    assert persisted is not None
    assert persisted.runtime_mode is RuntimeMode.RUNNING  # still on disk

    fresh = fresh_control_state(now_utc_ms=100)
    assert fresh.runtime_mode is RuntimeMode.SAFE_MODE
    assert fresh.entries_blocked is True

    # The runtime layer carries forward only restart-critical flags,
    # never the mode itself.
    carried = fresh.with_changes(
        kill_switch_active=persisted.kill_switch_active,
        operator_review_required=persisted.operator_review_required,
        incident_active=persisted.incident_active,
        paused_by_operator=persisted.paused_by_operator,
    )
    assert carried.runtime_mode is RuntimeMode.SAFE_MODE


def test_kill_switch_persists_across_restart(tmp_path: Path) -> None:
    store = _new_store(tmp_path)
    s = activate_kill_switch(fresh_control_state(now_utc_ms=10), now_utc_ms=11)
    store.save(s)
    loaded = store.load_persisted()
    assert loaded is not None
    assert loaded.kill_switch_active is True
    assert loaded.operator_review_required is True


def test_record_mode_event_appends_audit_row(tmp_path: Path) -> None:
    store = _new_store(tmp_path)
    s1 = fresh_control_state(now_utc_ms=10)
    s2 = enter_running(s1, now_utc_ms=11)
    store.save(s1)
    store.save(s2)
    store.record_mode_event(previous=s1, new=s2, reason="enter_running")
    # We don't expose query API; verify via raw SQL.
    import sqlite3

    conn = sqlite3.connect(str(tmp_path / "runtime.db"))
    try:
        rows = conn.execute(
            "SELECT previous_mode, new_mode, reason FROM runtime_mode_event"
        ).fetchall()
    finally:
        conn.close()
    assert rows == [("SAFE_MODE", "RUNNING", "enter_running")]


def test_record_mode_event_rejects_empty_reason(tmp_path: Path) -> None:
    store = _new_store(tmp_path)
    s1 = fresh_control_state(now_utc_ms=10)
    with pytest.raises(RuntimeStoreError):
        store.record_mode_event(previous=s1, new=s1, reason="")


def test_persistence_rejects_mixed_or_unknown_stop_trigger_domain(
    tmp_path: Path,
) -> None:
    store = _new_store(tmp_path)
    with pytest.raises(GovernanceLabelError):
        store.record_governance_label(
            label=StopTriggerDomain.MIXED_OR_UNKNOWN,
            context="test",
            recorded_at_utc_ms=1,
        )


def test_persistence_rejects_mixed_or_unknown_break_even_rule(
    tmp_path: Path,
) -> None:
    store = _new_store(tmp_path)
    with pytest.raises(GovernanceLabelError):
        store.record_governance_label(
            label=BreakEvenRule.MIXED_OR_UNKNOWN,
            context="test",
            recorded_at_utc_ms=1,
        )


def test_persistence_rejects_mixed_or_unknown_ema_slope_method(
    tmp_path: Path,
) -> None:
    store = _new_store(tmp_path)
    with pytest.raises(GovernanceLabelError):
        store.record_governance_label(
            label=EmaSlopeMethod.MIXED_OR_UNKNOWN,
            context="test",
            recorded_at_utc_ms=1,
        )


def test_persistence_rejects_mixed_or_unknown_stagnation_window_role(
    tmp_path: Path,
) -> None:
    store = _new_store(tmp_path)
    with pytest.raises(GovernanceLabelError):
        store.record_governance_label(
            label=StagnationWindowRole.MIXED_OR_UNKNOWN,
            context="test",
            recorded_at_utc_ms=1,
        )


def test_persistence_accepts_valid_governance_labels(tmp_path: Path) -> None:
    store = _new_store(tmp_path)
    store.record_governance_label(
        label=StopTriggerDomain.MARK_PRICE_RUNTIME,
        context="runtime-startup",
        recorded_at_utc_ms=1,
    )
    store.record_governance_label(
        label=BreakEvenRule.DISABLED,
        context="config-load",
        recorded_at_utc_ms=2,
    )
    store.record_governance_label(
        label=EmaSlopeMethod.NOT_APPLICABLE,
        context="config-load",
        recorded_at_utc_ms=3,
    )
    store.record_governance_label(
        label=StagnationWindowRole.NOT_ACTIVE,
        context="config-load",
        recorded_at_utc_ms=4,
    )


def test_persistence_rejects_empty_context(tmp_path: Path) -> None:
    store = _new_store(tmp_path)
    with pytest.raises(RuntimeStoreError):
        store.record_governance_label(
            label=StopTriggerDomain.MARK_PRICE_RUNTIME,
            context="",
            recorded_at_utc_ms=1,
        )


def test_persistence_rejects_invalid_persisted_runtime_mode(tmp_path: Path) -> None:
    """If the runtime DB is corrupted with an out-of-scheme mode value,
    ``load_persisted`` must fail closed rather than silently accept it."""
    store = _new_store(tmp_path)
    # Insert an invalid row directly.
    import sqlite3

    conn = sqlite3.connect(str(tmp_path / "runtime.db"))
    try:
        conn.execute(
            "INSERT INTO runtime_control (id, runtime_mode, kill_switch_active, "
            "paused_by_operator, operator_review_required, entries_blocked, "
            "incident_active, updated_at_utc_ms) "
            "VALUES (1, 'NOT_A_MODE', 0, 0, 0, 1, 0, 1)"
        )
        conn.commit()
    finally:
        conn.close()
    with pytest.raises(RuntimeStoreError):
        store.load_persisted()
