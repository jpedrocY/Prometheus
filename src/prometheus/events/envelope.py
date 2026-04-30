"""Shared message envelope for internal events / commands / queries.

Per `docs/08-architecture/internal-event-contracts.md` §Shared Message
Envelope, every important runtime message uses a common envelope with:

- ``message_type`` (specific name, e.g. ``runtime.mode_changed``),
- ``message_class`` (command | event | query),
- ``message_id`` (unique per message instance),
- ``correlation_id`` (groups messages of one workflow),
- ``causation_id`` (references the prior message that caused this one),
- ``occurred_at_utc_ms`` (canonical UTC ms),
- ``source_component`` (the component that emitted the message),
- ``payload`` (message-specific body).

Phase 4a uses a deterministic ``message_id`` generator backed by a
counter so that tests are reproducible without depending on UUIDs or
wall-clock time.
"""

from __future__ import annotations

from enum import StrEnum
from itertools import count
from threading import Lock
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MessageClass(StrEnum):
    """Top-level message classification."""

    COMMAND = "command"
    EVENT = "event"
    QUERY = "query"


class MessageEnvelope(BaseModel):
    """Shared envelope for runtime messages.

    The envelope itself does not carry secret material; payload models
    that include governance labels enforce fail-closed via their own
    validators (see ``runtime_events.py``).
    """

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
    )

    message_type: str = Field(min_length=1)
    message_class: MessageClass
    message_id: str = Field(min_length=1)
    correlation_id: str = Field(min_length=1)
    causation_id: str | None = None
    occurred_at_utc_ms: int = Field(gt=0)
    source_component: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


_ID_LOCK = Lock()
_ID_COUNTER = count(start=1)


def new_message_id(prefix: str = "msg") -> str:
    """Return a deterministic, monotonically-increasing message id.

    Phase 4a's runtime is single-process and synchronous; a counter is
    sufficient. Tests can reset the counter via the helper in the test
    harness (or by importing and incrementing the module-private state
    explicitly).
    """
    if not prefix:
        raise ValueError("prefix must be non-empty")
    with _ID_LOCK:
        n = next(_ID_COUNTER)
    return f"{prefix}-{n:08d}"
