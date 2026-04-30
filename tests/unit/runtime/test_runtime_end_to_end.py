"""Phase 4a end-to-end test covering happy + failure + restart paths.

This test wires together the runtime state model, persistence, fake-
exchange adapter, governance label enforcement, and exposure gates to
prove the Phase 4a safe-slice can be exercised without any real
exchange, credentials, or strategy.
"""

from __future__ import annotations

from pathlib import Path

from prometheus.core.governance import StopTriggerDomain
from prometheus.core.symbols import Symbol
from prometheus.execution.fake_adapter import FakeExchangeAdapter
from prometheus.persistence.runtime_store import RuntimeStore
from prometheus.risk.exposure import (
    ExposureSnapshot,
    PositionSide,
    evaluate_entry_candidate,
)
from prometheus.state.control import fresh_control_state
from prometheus.state.errors import KillSwitchActiveError
from prometheus.state.mode import RuntimeMode
from prometheus.state.transitions import (
    activate_kill_switch,
    enter_emergency,
    enter_running,
)


def _seed_store(db_path: Path) -> RuntimeStore:
    store = RuntimeStore(db_path)
    store.initialize()
    return store


def test_phase_4a_full_lifecycle_no_real_exchange(tmp_path: Path) -> None:
    db_path = tmp_path / "runtime.db"
    store = _seed_store(db_path)

    # Process start: enter SAFE_MODE explicitly. Persist baseline.
    control = fresh_control_state(now_utc_ms=1)
    store.save(control)
    assert control.runtime_mode is RuntimeMode.SAFE_MODE
    assert control.entries_blocked is True

    # Operator transitions runtime to RUNNING (no blocking flags).
    control = enter_running(control, now_utc_ms=2)
    store.save(control)
    store.record_mode_event(
        previous=fresh_control_state(now_utc_ms=1),
        new=control,
        reason="operator-test-transition",
    )
    assert control.runtime_mode is RuntimeMode.RUNNING

    # Exposure gate accepts a flat-state long entry.
    flat_snapshot = ExposureSnapshot(
        symbol=Symbol.BTCUSDT,
        has_position=False,
        position_side=None,
        protection_confirmed=False,
        entry_in_flight=False,
        manual_or_non_bot_exposure=False,
    )
    decision = evaluate_entry_candidate(
        candidate_symbol=Symbol.BTCUSDT,
        candidate_side=PositionSide.LONG,
        snapshot=flat_snapshot,
    )
    assert decision.allowed is True

    # Fake-exchange adapter drives the lifecycle end-to-end.
    adapter = FakeExchangeAdapter(symbol=Symbol.BTCUSDT, clock=lambda: 100)
    correlation = "trade-1"
    domain = StopTriggerDomain.MARK_PRICE_RUNTIME

    adapter.submit_entry_order(
        correlation_id=correlation,
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    adapter.confirm_fake_fill(correlation_id=correlation)
    adapter.submit_protective_stop(
        correlation_id=correlation,
        stop_price=49_500.0,
        stop_trigger_domain=domain,
    )
    adapter.confirm_fake_protective_stop(
        correlation_id=correlation, stop_trigger_domain=domain
    )
    assert adapter.position_state.has_position is True
    assert adapter.stop_state.confirmed is True

    # Inject a fake stop submission failure on a hypothetical second
    # cycle to prove EMERGENCY transition. Reset adapter to simulate
    # second trade cycle.
    adapter2 = FakeExchangeAdapter(symbol=Symbol.BTCUSDT, clock=lambda: 200)
    adapter2.submit_entry_order(
        correlation_id="trade-2",
        side=PositionSide.LONG,
        quantity=0.045,
        price=50_000.0,
    )
    adapter2.confirm_fake_fill(correlation_id="trade-2")
    adapter2.mark_stop_submission_failed(
        correlation_id="trade-2", stop_trigger_domain=domain
    )
    assert adapter2.position_state.has_position is True
    assert adapter2.stop_state.has_stop is False

    # Position exists, no protection: runtime must enter EMERGENCY.
    control = enter_emergency(control, now_utc_ms=3)
    store.save(control)
    assert control.runtime_mode is RuntimeMode.EMERGENCY
    assert control.entries_blocked is True
    assert control.incident_active is True
    assert control.operator_review_required is True

    # Activate the kill switch and persist it.
    control = activate_kill_switch(control, now_utc_ms=4)
    store.save(control)
    assert control.kill_switch_active is True

    # --- Simulated process restart -------------------------------------
    # New process: do NOT auto-resume from persisted state. Construct a
    # fresh SAFE_MODE record, then carry forward only restart-critical
    # flags.
    store2 = _seed_store(db_path)
    persisted = store2.load_persisted()
    assert persisted is not None
    assert persisted.kill_switch_active is True

    fresh = fresh_control_state(now_utc_ms=1000)
    carried = fresh.with_changes(
        kill_switch_active=persisted.kill_switch_active,
        operator_review_required=persisted.operator_review_required,
        incident_active=persisted.incident_active,
        paused_by_operator=persisted.paused_by_operator,
    )
    assert carried.runtime_mode is RuntimeMode.SAFE_MODE
    assert carried.kill_switch_active is True
    assert carried.entries_blocked is True

    # Cannot enter RUNNING while kill switch is active.
    raised = False
    try:
        enter_running(carried, now_utc_ms=1001)
    except KillSwitchActiveError:
        raised = True
    assert raised is True
