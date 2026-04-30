"""Local risk-sizing skeleton.

Implements the basic stop-distance-based sizing computation per
`docs/07-risk/position-sizing-framework.md` §Definitions:

```
sizing_equity = min(account_equity, strategy_allocated_equity)
risk_amount   = sizing_equity * risk_fraction
budget        = risk_amount * risk_usage_fraction
raw_quantity  = budget / stop_distance
```

The skeleton fails closed on:

- missing or non-positive equity,
- missing or non-positive stop distance,
- missing strategy-allocated equity,
- risk_fraction outside (0, 1],
- risk_usage_fraction outside (0, 1],
- a notional cap violation (if a cap is provided),
- a leverage cap violation (if account-equity reference is provided).

Phase 4a deliberately does NOT fetch live account equity. The caller
provides equity values explicitly via ``SizingInputs`` (test fixtures
only).

Locked v1 constants (per `current-project-state.md` Locked V1
Decisions §Risk and `docs/07-risk/position-sizing-framework.md`):

- ``LOCKED_LIVE_RISK_FRACTION = 0.0025`` (0.25%).
- ``LOCKED_LIVE_LEVERAGE_CAP = 2.0``.

These constants are exposed as module-level read-only references so
callers can opt to validate against them. Phase 4a does NOT enforce
them by default in the sizing function — the caller passes the
relevant values via inputs and the function checks them — because
research-stage callers may legitimately use other values.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from prometheus.core.symbols import Symbol

from .errors import MissingMetadataError, SizingError

LOCKED_LIVE_RISK_FRACTION: float = 0.0025
LOCKED_LIVE_LEVERAGE_CAP: float = 2.0


class SizingInputs(BaseModel):
    """Inputs to the risk-sizing computation.

    All values are explicit; no implicit account-equity lookup.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    account_equity_usdt: float = Field(gt=0)
    strategy_allocated_equity_usdt: float = Field(gt=0)
    risk_fraction: float = Field(gt=0, le=1)
    risk_usage_fraction: float = Field(gt=0, le=1)
    proposed_entry_price: float = Field(gt=0)
    initial_stop_price: float = Field(gt=0)
    side_is_long: bool
    leverage_cap: float = Field(gt=0)
    notional_cap_usdt: float = Field(gt=0)
    quantity_step: float = Field(gt=0)
    min_quantity: float = Field(gt=0)


class SizingResult(BaseModel):
    """Output of the risk-sizing computation."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    sizing_equity_usdt: float
    risk_amount_usdt: float
    effective_stop_risk_budget_usdt: float
    stop_distance: float
    raw_quantity: float
    rounded_quantity: float
    notional_usdt: float
    effective_leverage: float


def _stop_distance(side_is_long: bool, entry: float, stop: float) -> float:
    if side_is_long:
        return entry - stop
    return stop - entry


def _round_down_to_step(value: float, step: float) -> float:
    if step <= 0:
        raise MissingMetadataError("quantity_step must be positive")
    # Conservative rounding: floor to step boundary.
    return (int(value / step)) * step


def compute_sizing(inputs: SizingInputs) -> SizingResult:
    """Compute risk-sized quantity, failing closed on invalid inputs.

    The function returns a ``SizingResult`` if and only if every
    invariant holds. Otherwise it raises a subclass of ``RiskError``:

    - ``MissingMetadataError`` for missing/invalid metadata
      (quantity step, min_quantity).
    - ``SizingError`` for stop-side invalidity, below-minimum
      quantity, or cap violations.

    Phase 4a does NOT optimize the result; it returns the conservative
    floored quantity.
    """
    stop_distance = _stop_distance(
        side_is_long=inputs.side_is_long,
        entry=inputs.proposed_entry_price,
        stop=inputs.initial_stop_price,
    )
    if stop_distance <= 0:
        raise SizingError(
            "stop_distance is non-positive; long stop must be below "
            "entry, short stop must be above entry"
        )

    sizing_equity = min(
        inputs.account_equity_usdt, inputs.strategy_allocated_equity_usdt
    )
    risk_amount = sizing_equity * inputs.risk_fraction
    effective_budget = risk_amount * inputs.risk_usage_fraction
    raw_quantity = effective_budget / stop_distance

    rounded_quantity = _round_down_to_step(raw_quantity, inputs.quantity_step)
    if rounded_quantity < inputs.min_quantity:
        raise SizingError(
            f"rounded_quantity {rounded_quantity} below min_quantity "
            f"{inputs.min_quantity}; reject trade rather than scale up"
        )

    notional = rounded_quantity * inputs.proposed_entry_price
    if notional > inputs.notional_cap_usdt:
        raise SizingError(
            f"notional {notional} exceeds notional_cap_usdt "
            f"{inputs.notional_cap_usdt}"
        )

    effective_leverage = notional / sizing_equity
    if effective_leverage > inputs.leverage_cap:
        raise SizingError(
            f"effective_leverage {effective_leverage} exceeds leverage_cap "
            f"{inputs.leverage_cap}"
        )

    return SizingResult(
        sizing_equity_usdt=sizing_equity,
        risk_amount_usdt=risk_amount,
        effective_stop_risk_budget_usdt=effective_budget,
        stop_distance=stop_distance,
        raw_quantity=raw_quantity,
        rounded_quantity=rounded_quantity,
        notional_usdt=notional,
        effective_leverage=effective_leverage,
    )
