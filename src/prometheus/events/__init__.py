"""Internal event/message contracts for the Phase 4a runtime.

Per `docs/08-architecture/internal-event-contracts.md`, runtime
internal communication must distinguish:

- **Commands** — requests asking a component to do something (intent).
- **Events** — facts that something has happened (observed reality).
- **Queries** — read-only requests for current state.

Phase 4a implements a strategy-agnostic subset of these contracts:

- Runtime mode-change events.
- Kill-switch activation / clearance events.
- Fake-exchange lifecycle events (clearly marked fake/local).
- Governance-label-bearing event payloads with fail-closed validation.

Phase 4a explicitly does NOT implement:

- Real exchange-write events.
- Authenticated-exchange events.
- User-stream events.
- Strategy-signal events for any specific strategy.
"""

from __future__ import annotations

from .envelope import MessageClass, MessageEnvelope, new_message_id
from .runtime_events import (
    FakeExchangeLifecycleEvent,
    GovernanceLabelEvent,
    KillSwitchEvent,
    RuntimeModeChangedEvent,
)

__all__ = [
    "FakeExchangeLifecycleEvent",
    "GovernanceLabelEvent",
    "KillSwitchEvent",
    "MessageClass",
    "MessageEnvelope",
    "RuntimeModeChangedEvent",
    "new_message_id",
]
