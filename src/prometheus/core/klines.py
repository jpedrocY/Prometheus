"""Normalized kline (candle) model.

Schema and field order match docs/04-data/historical-data-spec.md. The
model is frozen, strict (no implicit coercion), and rejects unknown
fields. Construction enforces bar-identity and OHLC invariants.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .intervals import Interval
from .symbols import Symbol
from .time import close_time_for, is_aligned_open_time


class NormalizedKline(BaseModel):
    """A single completed, validated bar.

    Primary key: (symbol, interval, open_time). All volumes are
    non-negative. close_time is always open_time + interval_ms - 1.
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
    volume: float
    quote_asset_volume: float
    trade_count: int
    taker_buy_base_volume: float
    taker_buy_quote_volume: float
    source: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_invariants(self) -> NormalizedKline:
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
        if self.volume < 0:
            raise ValueError("volume must be non-negative")
        if self.quote_asset_volume < 0:
            raise ValueError("quote_asset_volume must be non-negative")
        if self.trade_count < 0:
            raise ValueError("trade_count must be non-negative")
        if self.taker_buy_base_volume < 0:
            raise ValueError("taker_buy_base_volume must be non-negative")
        if self.taker_buy_quote_volume < 0:
            raise ValueError("taker_buy_quote_volume must be non-negative")
        return self
