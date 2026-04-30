"""Read-only operator state surface for the Phase 4a runtime.

Phase 4a's operator surface is intentionally minimal: a function that
formats the current runtime control state, fake-position state, fake
protective-stop state, and governance label values into a plain-text
report. There are NO control buttons, NO exchange actions, and NO
production alerting (Telegram / n8n alerts are pre-tiny-live per
TD-019).

The read-only surface is exposed both as a Python function and as a
small CLI command (``python -m prometheus.cli`` — see
``prometheus.cli``).
"""

from __future__ import annotations

from .state_view import format_state_view

__all__ = ["format_state_view"]
