"""Deterministic local fake-exchange adapter.

The adapter is a Phase 4a strategy-agnostic test harness. It maintains
in-memory state for one fake position and one fake protective stop
(matching v1's one-symbol / one-position / one-stop scope).

Determinism: the adapter accepts an injectable ``ClockFn`` (per
``prometheus.core.time``); all timestamps come from the clock; no
``time.time()`` calls inside the adapter. There is no randomness, no
network I/O, no threading.

State machine:

```
NO_POSITION
  -> entry_submitted (pending)
  -> fake_fill_confirmed (called by the test/runtime)
  -> POSITION_HELD (no protection)
  -> protective_stop_submitted
  -> fake_stop_confirmed (called by the test/runtime)
  -> POSITION_PROTECTED
  -> fake_stop_triggered or test-driven exit
  -> NO_POSITION
```

Failure-injection paths the test harness can trigger:

- ``mark_entry_unknown_outcome()`` — entry result is unknown (timeout
  or ambiguous response). The adapter surfaces ``FakeOrderOutcome.UNKNOWN``
  and the runtime must fail closed.
- ``mark_stop_submission_failed()`` — stop submission failed; if a
  position exists, the runtime must enter EMERGENCY.

Phase 4a's adapter does NOT, ever:

- import from any module that talks to a real exchange,
- read environment variables that might contain credentials,
- open files,
- open sockets,
- call Binance,
- emit events without ``is_fake = True``.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from prometheus.core.errors import PrometheusError
from prometheus.core.governance import StopTriggerDomain, require_valid
from prometheus.core.symbols import Symbol
from prometheus.core.time import ClockFn, utc_now_ms
from prometheus.events.runtime_events import (
    FakeExchangeLifecycleEvent,
    FakeExchangeLifecycleKind,
)
from prometheus.risk.exposure import PositionSide


class FakeExchangeError(PrometheusError):
    """Raised when the fake adapter cannot satisfy a request."""


class FakeOrderOutcome(StrEnum):
    """Outcome of a fake order submission."""

    PENDING = "pending"
    FILLED = "filled"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class FakePositionState(BaseModel):
    """Frozen snapshot of fake position state."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    has_position: bool
    side: PositionSide | None = None
    quantity: float = 0.0
    entry_price: float | None = None


class FakeStopState(BaseModel):
    """Frozen snapshot of fake protective-stop state."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    has_stop: bool
    stop_price: float | None = None
    confirmed: bool = False
    submission_failed: bool = False


class _SubmittedEntry(BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, extra="forbid")

    correlation_id: str = Field(min_length=1)
    side: PositionSide
    requested_quantity: float = Field(gt=0)
    requested_price: float = Field(gt=0)
    outcome: FakeOrderOutcome = FakeOrderOutcome.PENDING


class FakeExchangeAdapter:
    """Deterministic local fake exchange.

    Construct one per test; do NOT share instances across tests.
    """

    def __init__(self, *, symbol: Symbol = Symbol.BTCUSDT, clock: ClockFn | None = None) -> None:
        self._symbol = symbol
        self._clock = clock
        self._position = FakePositionState(symbol=symbol, has_position=False)
        self._stop = FakeStopState(has_stop=False)
        self._pending_entry: _SubmittedEntry | None = None
        self._events: list[FakeExchangeLifecycleEvent] = []

    # -- Read accessors -------------------------------------------------

    @property
    def position_state(self) -> FakePositionState:
        return self._position

    @property
    def stop_state(self) -> FakeStopState:
        return self._stop

    @property
    def is_entry_in_flight(self) -> bool:
        return self._pending_entry is not None and self._pending_entry.outcome in {
            FakeOrderOutcome.PENDING,
            FakeOrderOutcome.UNKNOWN,
        }

    @property
    def emitted_events(self) -> tuple[FakeExchangeLifecycleEvent, ...]:
        return tuple(self._events)

    # -- Mutation methods (public API) ---------------------------------

    def submit_entry_order(
        self, *, correlation_id: str, side: PositionSide, quantity: float, price: float
    ) -> FakeExchangeLifecycleEvent:
        """Submit a fake entry order.

        Fails closed if an entry is already in flight or a position
        already exists; the runtime is expected to gate this via the
        exposure layer before calling.
        """
        if quantity <= 0:
            raise FakeExchangeError("quantity must be positive")
        if price <= 0:
            raise FakeExchangeError("price must be positive")
        if self._pending_entry is not None:
            raise FakeExchangeError("entry already in flight")
        if self._position.has_position:
            raise FakeExchangeError(
                "fake position already exists; exposure gate should have blocked"
            )
        self._pending_entry = _SubmittedEntry(
            correlation_id=correlation_id,
            side=side,
            requested_quantity=quantity,
            requested_price=price,
        )
        event = self._emit(
            FakeExchangeLifecycleKind.FAKE_ENTRY_SUBMITTED, correlation_id=correlation_id
        )
        return event

    def confirm_fake_fill(self, *, correlation_id: str) -> FakeExchangeLifecycleEvent:
        """Mark a pending entry as fully filled."""
        pending = self._require_pending_entry(correlation_id)
        pending.outcome = FakeOrderOutcome.FILLED
        self._position = FakePositionState(
            symbol=self._symbol,
            has_position=True,
            side=pending.side,
            quantity=pending.requested_quantity,
            entry_price=pending.requested_price,
        )
        self._emit(
            FakeExchangeLifecycleKind.FAKE_FILL_CONFIRMED, correlation_id=correlation_id
        )
        event = self._emit(
            FakeExchangeLifecycleKind.FAKE_POSITION_CONFIRMED,
            correlation_id=correlation_id,
        )
        self._pending_entry = None
        return event

    def mark_entry_unknown_outcome(
        self, *, correlation_id: str
    ) -> FakeExchangeLifecycleEvent:
        """Surface an unknown / timeout entry result.

        The runtime must fail closed on this event: block new entries,
        require reconciliation, do not assume position state.
        """
        pending = self._require_pending_entry(correlation_id)
        pending.outcome = FakeOrderOutcome.UNKNOWN
        return self._emit(
            FakeExchangeLifecycleKind.FAKE_UNKNOWN_OUTCOME, correlation_id=correlation_id
        )

    def submit_protective_stop(
        self,
        *,
        correlation_id: str,
        stop_price: float,
        stop_trigger_domain: StopTriggerDomain,
    ) -> FakeExchangeLifecycleEvent:
        """Submit a fake protective stop.

        Enforces:
        - The Phase 3v `stop_trigger_domain` governance label is valid
          (fail closed on `mixed_or_unknown`).
        - For Phase 4a's runtime context, callers should pass
          ``stop_trigger_domain = mark_price_runtime`` (per Phase 3v
          §8.3 and `docs/07-risk/stop-loss-policy.md` §1.7.3 lock).
        - A position must exist before a protective stop is submitted
          (per `docs/07-risk/stop-loss-policy.md` §Protective Stop Timing).
        """
        require_valid(stop_trigger_domain)
        if stop_price <= 0:
            raise FakeExchangeError("stop_price must be positive")
        if not self._position.has_position:
            raise FakeExchangeError(
                "cannot submit protective stop without an existing fake position"
            )
        self._stop = FakeStopState(
            has_stop=True, stop_price=stop_price, confirmed=False, submission_failed=False
        )
        return self._emit(
            FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_SUBMITTED,
            correlation_id=correlation_id,
            stop_trigger_domain=stop_trigger_domain,
        )

    def confirm_fake_protective_stop(
        self,
        *,
        correlation_id: str,
        stop_trigger_domain: StopTriggerDomain,
    ) -> FakeExchangeLifecycleEvent:
        """Confirm the previously submitted fake protective stop."""
        require_valid(stop_trigger_domain)
        if not self._stop.has_stop:
            raise FakeExchangeError("no fake protective stop has been submitted")
        if self._stop.submission_failed:
            raise FakeExchangeError(
                "fake protective stop submission was marked as failed"
            )
        self._stop = self._stop.model_copy(update={"confirmed": True})
        return self._emit(
            FakeExchangeLifecycleKind.FAKE_PROTECTIVE_STOP_CONFIRMED,
            correlation_id=correlation_id,
            stop_trigger_domain=stop_trigger_domain,
        )

    def mark_stop_submission_failed(
        self,
        *,
        correlation_id: str,
        stop_trigger_domain: StopTriggerDomain,
    ) -> FakeExchangeLifecycleEvent:
        """Surface a fake stop submission failure.

        If a fake position exists, the runtime must enter EMERGENCY
        per `docs/07-risk/stop-loss-policy.md` §Emergency Unprotected
        Policy.
        """
        require_valid(stop_trigger_domain)
        self._stop = FakeStopState(
            has_stop=False, stop_price=None, confirmed=False, submission_failed=True
        )
        return self._emit(
            FakeExchangeLifecycleKind.FAKE_SUBMISSION_TIMEOUT,
            correlation_id=correlation_id,
            stop_trigger_domain=stop_trigger_domain,
        )

    def trigger_fake_stop(
        self,
        *,
        correlation_id: str,
        stop_trigger_domain: StopTriggerDomain,
    ) -> FakeExchangeLifecycleEvent:
        """Simulate the fake protective stop firing."""
        require_valid(stop_trigger_domain)
        if not self._stop.has_stop or not self._stop.confirmed:
            raise FakeExchangeError(
                "cannot trigger fake stop without confirmed fake protective stop"
            )
        if not self._position.has_position:
            raise FakeExchangeError(
                "cannot trigger fake stop without existing fake position"
            )
        self._position = FakePositionState(symbol=self._symbol, has_position=False)
        self._stop = FakeStopState(has_stop=False)
        return self._emit(
            FakeExchangeLifecycleKind.FAKE_STOP_TRIGGERED,
            correlation_id=correlation_id,
            stop_trigger_domain=stop_trigger_domain,
        )

    # -- Internals -----------------------------------------------------

    def _require_pending_entry(self, correlation_id: str) -> _SubmittedEntry:
        if self._pending_entry is None:
            raise FakeExchangeError("no pending entry to act on")
        if self._pending_entry.correlation_id != correlation_id:
            raise FakeExchangeError(
                f"pending entry correlation_id mismatch: "
                f"{self._pending_entry.correlation_id} vs {correlation_id}"
            )
        return self._pending_entry

    def _emit(
        self,
        kind: FakeExchangeLifecycleKind,
        *,
        correlation_id: str,
        stop_trigger_domain: StopTriggerDomain | None = None,
    ) -> FakeExchangeLifecycleEvent:
        event = FakeExchangeLifecycleEvent(
            kind=kind,
            is_fake=True,
            correlation_id=correlation_id,
            stop_trigger_domain=stop_trigger_domain,
            occurred_at_utc_ms=utc_now_ms(self._clock),
        )
        self._events.append(event)
        return event
