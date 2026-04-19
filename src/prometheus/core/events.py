"""Event-type domain models.

Funding-rate events are keyed by ``(symbol, funding_time)`` and are
not bar-aligned; they fire at the exchange's funding cadence
(typically 8-hour intervals on USD-M perpetuals, but not strictly
guaranteed).

Per docs/04-data/timestamp-policy.md: funding must be joined using
funding timestamps, not assumed to belong automatically to any candle.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .symbols import Symbol


class FundingRateEvent(BaseModel):
    """A single funding-rate event for a perpetual futures symbol.

    Fields mirror Binance's ``/fapi/v1/fundingRate`` response
    (lowercased), with ``fundingRate`` and ``markPrice`` parsed from
    their upstream string-decimal representation into ``float``.
    """

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
    )

    symbol: Symbol
    funding_time: int  # UTC milliseconds
    funding_rate: float
    mark_price: float
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
        if self.mark_price <= 0:
            raise ValueError("mark_price must be strictly positive")
        return self
