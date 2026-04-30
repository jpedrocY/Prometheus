"""Execution layer for the Phase 4a local safe runtime foundation.

Phase 4a implements only a deterministic local fake-exchange adapter
per Phase 3x §9.8. There is NO real Binance adapter. The architectural
prohibition is structural, not configurational: only the fake adapter
exists in code; there is no configuration switch that turns on a live
adapter. Authorization for any future live adapter would require new
code AND a new phase authorization.

The fake adapter:

- exposes a small interface mirroring the live adapter shape (entry
  submission, protective stop submission, position query) so the
  runtime can be tested end-to-end;
- backs all state with an in-memory deterministic state machine; no
  network I/O; no Binance credentials; no listenKey; no WebSocket;
- emits Phase 4a fake-lifecycle events tagged with ``is_fake = True``
  so downstream code cannot confuse fake events with live truth;
- enforces the Phase 3v ``stop_trigger_domain`` governance label at
  the fake-exchange decision boundary.
"""

from __future__ import annotations

from .fake_adapter import (
    FakeExchangeAdapter,
    FakeExchangeError,
    FakeOrderOutcome,
    FakePositionState,
    FakeStopState,
)

__all__ = [
    "FakeExchangeAdapter",
    "FakeExchangeError",
    "FakeOrderOutcome",
    "FakePositionState",
    "FakeStopState",
]
