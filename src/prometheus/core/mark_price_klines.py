"""Mark-price kline model.

Mark-price klines share timestamp semantics with standard klines but have
no volume, no trade_count, and no taker-buy fields. Primary key is
``(symbol, interval, open_time)``. Schema matches
``docs/04-data/historical-data-spec.md`` §"Mark-price kline schema".
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .intervals import Interval
from .symbols import Symbol
from .time import close_time_for, is_aligned_open_time


class MarkPriceKline(BaseModel):
    """A single completed mark-price bar.

    Primary key: (symbol, interval, open_time). Interval-aligned
    open_time and ``close_time = open_time + duration - 1`` are
    enforced at construction.
    """

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
    )

    symbol: Symbol
    interval: Interval
    open_time: int
    close_time: int
    open: float
    high: float
    low: float
    close: float
    source: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_invariants(self) -> MarkPriceKline:
        if self.open_time <= 0:
            raise ValueError("open_time must be positive")
        if not is_aligned_open_time(self.open_time, self.interval):
            raise ValueError(
                f"open_time {self.open_time} is not aligned to interval {self.interval.value}"
            )
        expected_close = close_time_for(self.open_time, self.interval)
        if self.close_time != expected_close:
            raise ValueError(
                f"close_time {self.close_time} does not match "
                f"open_time + duration - 1 = {expected_close}"
            )
        if self.high < max(self.open, self.close):
            raise ValueError("high must be >= max(open, close)")
        if self.low > min(self.open, self.close):
            raise ValueError("low must be <= min(open, close)")
        if self.high < self.low:
            raise ValueError("high must be >= low")
        if self.open <= 0 or self.high <= 0 or self.low <= 0 or self.close <= 0:
            raise ValueError("mark prices must be strictly positive")
        return self
