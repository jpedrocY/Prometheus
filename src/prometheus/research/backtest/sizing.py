"""Position sizing pipeline per docs/07-risk/position-sizing-framework.md.

Pipeline steps (Phase 3 Gate 1 §10.7):

    1. risk_amount = sizing_equity * risk_fraction
    2. risk_budget = risk_amount * risk_usage_fraction
    3. raw_qty = risk_budget / stop_distance
    4. leverage_cap_qty = (sizing_equity * max_effective_leverage) / reference_price
    5. notional_cap_qty = max_notional_internal / reference_price
    6. candidate_qty = min(raw_qty, leverage_cap_qty, notional_cap_qty)
    7. Floor candidate_qty to LOT_SIZE.stepSize
    8. If final_qty < LOT_SIZE.minQty -> reject (BELOW_MINQTY)
    9. If final_qty * reference_price < MIN_NOTIONAL.notional -> reject (BELOW_MIN_NOTIONAL)
   10. Emit sizing_limited_by label

Round-down quantity rule is non-negotiable (position-sizing-framework
§"Quantity Rounding Policy"): "Always round DOWN; nearest rounding is
explicitly forbidden."
"""

from __future__ import annotations

import math
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from prometheus.core.exchange_info import SymbolInfo


class SizingLimitedBy(StrEnum):
    """Which constraint bound the sized quantity."""

    STOP_RISK = "STOP_RISK"
    MAX_EFFECTIVE_LEVERAGE = "MAX_EFFECTIVE_LEVERAGE"
    INTERNAL_NOTIONAL_CAP = "INTERNAL_NOTIONAL_CAP"
    STEP_SIZE_FLOOR = "STEP_SIZE_FLOOR"


class RejectionReason(StrEnum):
    BELOW_MINQTY = "BELOW_MINQTY"
    BELOW_MIN_NOTIONAL = "BELOW_MIN_NOTIONAL"
    MISSING_FILTERS = "MISSING_FILTERS"


class SizingDecision(BaseModel):
    """Outcome of the sizing pipeline.

    Either approved with ``quantity > 0`` and a ``limited_by`` label,
    or rejected with a ``rejection_reason`` and ``quantity == 0``.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    approved: bool
    quantity: float = Field(ge=0)
    notional: float = Field(ge=0)
    realized_risk_usdt: float = Field(ge=0)
    raw_qty: float = Field(ge=0)
    leverage_cap_qty: float = Field(ge=0)
    notional_cap_qty: float = Field(ge=0)
    candidate_qty: float = Field(ge=0)
    limited_by: SizingLimitedBy | None = None
    rejection_reason: RejectionReason | None = None


def _floor_to_step(value: float, step: float) -> float:
    """Floor ``value`` to the nearest multiple of ``step`` (strict round-down).

    Uses Decimal for bit-exact arithmetic against the published
    step size. Per position-sizing-framework §"Quantity Rounding
    Policy": round-down only, never nearest.
    """
    if step <= 0:
        raise ValueError(f"step must be positive, got {step}")
    d_val = Decimal(repr(value))
    d_step = Decimal(repr(step))
    steps = (d_val / d_step).to_integral_value(rounding="ROUND_FLOOR")
    floored = steps * d_step
    return float(floored)


def compute_size(
    *,
    sizing_equity_usdt: float,
    risk_fraction: float,
    risk_usage_fraction: float,
    stop_distance: float,
    reference_price: float,
    max_effective_leverage: float,
    max_notional_internal_usdt: float,
    symbol_info: SymbolInfo,
) -> SizingDecision:
    """Run the full sizing pipeline. See module docstring for steps."""
    if sizing_equity_usdt <= 0:
        raise ValueError("sizing_equity_usdt must be positive")
    if stop_distance <= 0:
        raise ValueError("stop_distance must be positive")
    if reference_price <= 0:
        raise ValueError("reference_price must be positive")

    if symbol_info.lot_size_filter is None or symbol_info.min_notional_filter is None:
        return SizingDecision(
            approved=False,
            quantity=0.0,
            notional=0.0,
            realized_risk_usdt=0.0,
            raw_qty=0.0,
            leverage_cap_qty=0.0,
            notional_cap_qty=0.0,
            candidate_qty=0.0,
            rejection_reason=RejectionReason.MISSING_FILTERS,
        )

    step_size = float(symbol_info.lot_size_filter.stepSize)
    min_qty = float(symbol_info.lot_size_filter.minQty)
    min_notional = float(symbol_info.min_notional_filter.notional)

    risk_amount = sizing_equity_usdt * risk_fraction
    risk_budget = risk_amount * risk_usage_fraction
    raw_qty = risk_budget / stop_distance
    leverage_cap_qty = (sizing_equity_usdt * max_effective_leverage) / reference_price
    notional_cap_qty = max_notional_internal_usdt / reference_price

    candidate_qty = min(raw_qty, leverage_cap_qty, notional_cap_qty)
    # Label which constraint bound the candidate before flooring.
    if math.isclose(candidate_qty, raw_qty):
        limited_by: SizingLimitedBy = SizingLimitedBy.STOP_RISK
    elif math.isclose(candidate_qty, leverage_cap_qty):
        limited_by = SizingLimitedBy.MAX_EFFECTIVE_LEVERAGE
    else:
        limited_by = SizingLimitedBy.INTERNAL_NOTIONAL_CAP

    floored_qty = _floor_to_step(candidate_qty, step_size)
    if floored_qty < candidate_qty and math.isclose(floored_qty, candidate_qty, rel_tol=1e-12):
        # Treat tiny float differences from _floor_to_step as equal.
        floored_qty = candidate_qty
    if floored_qty < candidate_qty:
        limited_by = SizingLimitedBy.STEP_SIZE_FLOOR

    if floored_qty < min_qty:
        return SizingDecision(
            approved=False,
            quantity=0.0,
            notional=0.0,
            realized_risk_usdt=0.0,
            raw_qty=raw_qty,
            leverage_cap_qty=leverage_cap_qty,
            notional_cap_qty=notional_cap_qty,
            candidate_qty=candidate_qty,
            rejection_reason=RejectionReason.BELOW_MINQTY,
        )

    notional = floored_qty * reference_price
    if notional < min_notional:
        return SizingDecision(
            approved=False,
            quantity=0.0,
            notional=0.0,
            realized_risk_usdt=0.0,
            raw_qty=raw_qty,
            leverage_cap_qty=leverage_cap_qty,
            notional_cap_qty=notional_cap_qty,
            candidate_qty=candidate_qty,
            rejection_reason=RejectionReason.BELOW_MIN_NOTIONAL,
        )

    realized_risk = floored_qty * stop_distance
    return SizingDecision(
        approved=True,
        quantity=floored_qty,
        notional=notional,
        realized_risk_usdt=realized_risk,
        raw_qty=raw_qty,
        leverage_cap_qty=leverage_cap_qty,
        notional_cap_qty=notional_cap_qty,
        candidate_qty=candidate_qty,
        limited_by=limited_by,
    )
