"""Plain-text read-only operator state view.

The view formats:

- Runtime mode.
- Kill-switch state.
- Pause / operator-review-required / incident-active flags.
- Entries-blocked status.
- Fake-position state (if any).
- Fake-protective-stop state (if any).
- Governance label values where supplied.

Per Phase 3x §6 / §10 and `docs/11-interface/operator-dashboard-requirements.md`:
this surface is read-only. It does NOT expose any control or order
action. It does NOT include production alerting wiring.
"""

from __future__ import annotations

from prometheus.core.governance import (
    BreakEvenRule,
    EmaSlopeMethod,
    StagnationWindowRole,
    StopTriggerDomain,
)
from prometheus.execution.fake_adapter import FakePositionState, FakeStopState
from prometheus.state.control import RuntimeControlState


def format_state_view(
    *,
    control: RuntimeControlState,
    fake_position: FakePositionState | None = None,
    fake_stop: FakeStopState | None = None,
    stop_trigger_domain: StopTriggerDomain | None = None,
    break_even_rule: BreakEvenRule | None = None,
    ema_slope_method: EmaSlopeMethod | None = None,
    stagnation_window_role: StagnationWindowRole | None = None,
) -> str:
    """Return a plain-text rendering of the current runtime state.

    The function is pure: same inputs produce the same output. It does
    not read from any global state or make any I/O calls.
    """
    lines: list[str] = []
    lines.append("Prometheus runtime — read-only state view (Phase 4a, fake/local)")
    lines.append("=" * 64)
    lines.append(f"runtime_mode:               {control.runtime_mode.value}")
    lines.append(f"kill_switch_active:         {control.kill_switch_active}")
    lines.append(f"paused_by_operator:         {control.paused_by_operator}")
    lines.append(f"operator_review_required:   {control.operator_review_required}")
    lines.append(f"incident_active:            {control.incident_active}")
    lines.append(f"entries_blocked:            {control.entries_blocked}")
    lines.append(f"updated_at_utc_ms:          {control.updated_at_utc_ms}")
    lines.append("")
    lines.append("Fake position (local; not exchange truth)")
    lines.append("-" * 64)
    if fake_position is None or not fake_position.has_position:
        lines.append("  has_position: False")
    else:
        lines.append("  has_position: True")
        lines.append(f"  symbol:       {fake_position.symbol}")
        lines.append(f"  side:         {fake_position.side}")
        lines.append(f"  quantity:     {fake_position.quantity}")
        lines.append(f"  entry_price:  {fake_position.entry_price}")
    lines.append("")
    lines.append("Fake protective stop (local; not exchange truth)")
    lines.append("-" * 64)
    if fake_stop is None or not fake_stop.has_stop:
        lines.append("  has_stop: False")
    else:
        lines.append("  has_stop:           True")
        lines.append(f"  stop_price:         {fake_stop.stop_price}")
        lines.append(f"  confirmed:          {fake_stop.confirmed}")
        lines.append(f"  submission_failed:  {fake_stop.submission_failed}")
    lines.append("")
    lines.append("Governance labels (Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3)")
    lines.append("-" * 64)
    lines.append(
        f"  stop_trigger_domain:     "
        f"{_label(stop_trigger_domain)}"
    )
    lines.append(
        f"  break_even_rule:         {_label(break_even_rule)}"
    )
    lines.append(
        f"  ema_slope_method:        {_label(ema_slope_method)}"
    )
    lines.append(
        f"  stagnation_window_role:  {_label(stagnation_window_role)}"
    )
    lines.append("")
    lines.append(
        "Phase 4a is local-only / fake-exchange / dry-run / "
        "exchange-write-free / strategy-agnostic."
    )
    return "\n".join(lines)


def _label(value: object) -> str:
    if value is None:
        return "<unset>"
    return getattr(value, "value", str(value))
