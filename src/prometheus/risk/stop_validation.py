"""Local stop-validation skeleton.

Implements stop validation per `docs/07-risk/stop-loss-policy.md`
§Initial Stop Validation and §Stop Update Policy, gated by the
Phase 3v `stop_trigger_domain` governance label.

Validation rules (Phase 4a in-scope subset):

- ``stop_trigger_domain`` must be valid; ``mixed_or_unknown`` fails
  closed via ``prometheus.core.governance.require_valid``.
- Long stops must be strictly below entry; short stops strictly above.
- Stop distance must be strictly positive.
- ATR filter ``0.60 * ATR <= stop_distance <= 1.80 * ATR`` if ATR is
  provided.
- Required metadata (tick size, price precision) must be present.
- Stop-update direction must be risk-reducing only (no widening).
- For any future-runtime path (``stop_trigger_domain ==
  mark_price_runtime``), the validation function explicitly records
  this so callers can verify the §1.7.3 mark-price-stop lock is
  honored.

Phase 4a does NOT place stops on a real exchange and does NOT cancel
real stops. The stop-validation skeleton is used by the fake-exchange
adapter and by tests.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from prometheus.core.governance import StopTriggerDomain, require_valid
from prometheus.core.symbols import Symbol
from prometheus.risk.exposure import PositionSide

from .errors import MissingMetadataError, StopValidationError


class StopRequest(BaseModel):
    """An initial-stop validation request."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    side: PositionSide
    proposed_entry_price: float = Field(gt=0)
    initial_stop_price: float = Field(gt=0)
    atr: float | None = None
    tick_size: float | None = None
    price_precision: int | None = None
    stop_trigger_domain: StopTriggerDomain


class StopUpdateRequest(BaseModel):
    """A stop-update validation request (cancel-and-replace).

    The update is allowed only if it is risk-reducing relative to the
    current active stop. Any widening attempt fails closed.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    side: PositionSide
    current_stop_price: float = Field(gt=0)
    proposed_new_stop_price: float = Field(gt=0)
    stop_trigger_domain: StopTriggerDomain

    @model_validator(mode="after")
    def _validate(self) -> StopUpdateRequest:
        require_valid(self.stop_trigger_domain)
        return self


def validate_initial_stop(request: StopRequest) -> None:
    """Validate an initial-stop request; raise on any failure.

    Returns ``None`` on success. The function is a *predicate* — its
    sole purpose is to fail closed; it does not transform the input.
    """
    require_valid(request.stop_trigger_domain)

    # Side-vs-entry check.
    if request.side == PositionSide.LONG:
        if request.initial_stop_price >= request.proposed_entry_price:
            raise StopValidationError(
                "long initial_stop_price must be strictly below entry"
            )
        stop_distance = request.proposed_entry_price - request.initial_stop_price
    else:
        if request.initial_stop_price <= request.proposed_entry_price:
            raise StopValidationError(
                "short initial_stop_price must be strictly above entry"
            )
        stop_distance = request.initial_stop_price - request.proposed_entry_price

    if stop_distance <= 0:
        raise StopValidationError("stop_distance must be strictly positive")

    # ATR filter (if ATR available).
    if request.atr is not None:
        if request.atr <= 0:
            raise MissingMetadataError("ATR must be positive when provided")
        if stop_distance < 0.60 * request.atr:
            raise StopValidationError(
                f"stop_distance {stop_distance} is too tight relative to ATR "
                f"{request.atr} (< 0.60 × ATR)"
            )
        if stop_distance > 1.80 * request.atr:
            raise StopValidationError(
                f"stop_distance {stop_distance} is too wide relative to ATR "
                f"{request.atr} (> 1.80 × ATR)"
            )

    # Metadata-presence checks where caller asserted them required.
    if request.tick_size is not None and request.tick_size <= 0:
        raise MissingMetadataError("tick_size must be positive when provided")
    if request.price_precision is not None and request.price_precision < 0:
        raise MissingMetadataError(
            "price_precision must be non-negative when provided"
        )


def validate_stop_update(request: StopUpdateRequest) -> None:
    """Validate a stop-update request; raise on any widening attempt.

    For longs: proposed new stop must be >= current stop.
    For shorts: proposed new stop must be <= current stop.
    Equality is permitted (defensive idempotent re-submission); strict
    widening is rejected.
    """
    if request.side == PositionSide.LONG:
        if request.proposed_new_stop_price < request.current_stop_price:
            raise StopValidationError(
                "long stop update would widen risk (proposed below current)"
            )
    else:
        if request.proposed_new_stop_price > request.current_stop_price:
            raise StopValidationError(
                "short stop update would widen risk (proposed above current)"
            )
