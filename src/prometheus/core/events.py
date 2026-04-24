"""Event-type domain models.

Funding-rate events are keyed by ``(symbol, funding_time)`` and are
not bar-aligned; they fire at the exchange's funding cadence
(typically 8-hour intervals on USD-M perpetuals, but not strictly
guaranteed).

Per docs/04-data/timestamp-policy.md: funding must be joined using
funding timestamps, not assumed to belong automatically to any candle.

Note on ``mark_price``: per GAP-20260420-029, Binance's public
``/fapi/v1/fundingRate`` endpoint returns an empty string for
``markPrice`` on funding events before approximately 2024-01-01
(verified 2026-04-20: 2022 and 2023 sample windows return
``markPrice: ""``; 2024-01-01 onward returns a populated decimal
string). The funding event is still valid and usable for backtest
funding accrual (``funding_rate`` + ``funding_time`` are always
populated), so ``mark_price`` is modeled as ``float | None``. A
``None`` value means "upstream did not populate it"; a non-None
value must be strictly positive. The v1 backtester's
``apply_funding_accrual`` computes funding PnL from
``funding_rate`` and the position notional, not from mark_price,
so a None mark_price does not affect funding math.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .symbols import Symbol


class FundingRateEvent(BaseModel):
    """A single funding-rate event for a perpetual futures symbol.

    Fields mirror Binance's ``/fapi/v1/fundingRate`` response
    (lowercased), with ``fundingRate`` parsed from the upstream
    string-decimal into ``float``. ``mark_price`` is optional
    (``float | None``) because Binance returns an empty string
    for pre-2024 events.
    """

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
    )

    symbol: Symbol
    funding_time: int  # UTC milliseconds
    funding_rate: float
    mark_price: float | None
    source: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate(self) -> FundingRateEvent:
        if self.funding_time <= 0:
            raise ValueError("funding_time must be positive")
        # Historically Binance USD-M funding rates stay well under 1%.
        # A rate of magnitude >= 1.0 (100%) indicates malformed data;
        # we reject it outright to fail closed on corruption.
        if abs(self.funding_rate) >= 1.0:
            raise ValueError(
                f"funding_rate {self.funding_rate} has magnitude >= 1.0 (suspected malformed data)"
            )
        # mark_price is optional per GAP-20260420-029: if provided, it
        # must be strictly positive; None means upstream did not populate.
        if self.mark_price is not None and self.mark_price <= 0:
            raise ValueError("mark_price, when provided, must be strictly positive")
        return self
