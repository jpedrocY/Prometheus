"""Phase 4a tests for the read-only operator state view."""

from __future__ import annotations

import pytest

from prometheus.cli import main
from prometheus.core.governance import (
    BreakEvenRule,
    EmaSlopeMethod,
    StagnationWindowRole,
    StopTriggerDomain,
)
from prometheus.core.symbols import Symbol
from prometheus.execution.fake_adapter import FakePositionState, FakeStopState
from prometheus.operator.state_view import format_state_view
from prometheus.persistence.runtime_store import RuntimeStore
from prometheus.risk.exposure import PositionSide
from prometheus.state.control import fresh_control_state
from prometheus.state.transitions import activate_kill_switch


def test_format_state_view_renders_safe_mode_baseline() -> None:
    control = fresh_control_state(now_utc_ms=1)
    out = format_state_view(control=control)
    assert "runtime_mode:               SAFE_MODE" in out
    assert "kill_switch_active:         False" in out
    assert "entries_blocked:            True" in out
    assert "has_position: False" in out
    assert "has_stop: False" in out
    # Local-only disclaimer is part of the output.
    assert "Phase 4a is local-only" in out


def test_format_state_view_renders_kill_switch_and_governance_labels() -> None:
    control = activate_kill_switch(fresh_control_state(now_utc_ms=1), now_utc_ms=2)
    fake_position = FakePositionState(
        symbol=Symbol.BTCUSDT,
        has_position=True,
        side=PositionSide.LONG,
        quantity=0.045,
        entry_price=50_000.0,
    )
    fake_stop = FakeStopState(
        has_stop=True, stop_price=49_500.0, confirmed=True, submission_failed=False
    )
    out = format_state_view(
        control=control,
        fake_position=fake_position,
        fake_stop=fake_stop,
        stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
        break_even_rule=BreakEvenRule.DISABLED,
        ema_slope_method=EmaSlopeMethod.NOT_APPLICABLE,
        stagnation_window_role=StagnationWindowRole.NOT_ACTIVE,
    )
    assert "kill_switch_active:         True" in out
    assert "side:         long" in out
    assert "stop_price:         49500.0" in out
    assert "stop_trigger_domain:     mark_price_runtime" in out
    assert "break_even_rule:         disabled" in out
    assert "ema_slope_method:        not_applicable" in out
    assert "stagnation_window_role:  not_active" in out


def test_state_view_does_not_expose_exchange_actions() -> None:
    """The read-only output must not include any control / order /
    cancel / kill-switch-toggle action language. The disclaimer line
    naming Phase 4a as ``exchange-write-free`` is anti-write language
    and is allowed; only action-shaped phrases are forbidden."""
    control = fresh_control_state(now_utc_ms=1)
    out = format_state_view(control=control)
    forbidden = [
        "place order",
        "submit order",
        "cancel order",
        "modify stop",
        "click to",
        "production key",
        "credentials",
    ]
    lower = out.lower()
    for phrase in forbidden:
        assert phrase not in lower, f"state view leaked phrase: {phrase!r}"


def test_cli_inspect_runtime_with_empty_db_requires_allow_empty(
    tmp_path, capsys: pytest.CaptureFixture[str]
) -> None:
    db_path = tmp_path / "runtime.db"
    rc = main(["inspect-runtime", "--db", str(db_path)])
    captured = capsys.readouterr()
    assert rc == 2
    assert "no persisted runtime control row found" in captured.err


def test_cli_inspect_runtime_allow_empty_prints_safe_mode(
    tmp_path, capsys: pytest.CaptureFixture[str]
) -> None:
    db_path = tmp_path / "runtime.db"
    rc = main(["inspect-runtime", "--db", str(db_path), "--allow-empty"])
    captured = capsys.readouterr()
    assert rc == 0
    assert "runtime_mode:               SAFE_MODE" in captured.out


def test_cli_inspect_runtime_reads_persisted_record(
    tmp_path, capsys: pytest.CaptureFixture[str]
) -> None:
    db_path = tmp_path / "runtime.db"
    store = RuntimeStore(db_path)
    store.initialize()
    state = activate_kill_switch(fresh_control_state(now_utc_ms=1), now_utc_ms=2)
    store.save(state)

    rc = main(["inspect-runtime", "--db", str(db_path)])
    captured = capsys.readouterr()
    assert rc == 0
    assert "kill_switch_active:         True" in captured.out
