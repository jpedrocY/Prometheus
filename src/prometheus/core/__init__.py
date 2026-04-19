"""Shared domain primitives used across the Prometheus codebase.

Per docs/08-architecture/codebase-structure.md, `core` owns UTC millisecond
time utilities, canonical symbol/interval primitives, the normalized kline
type, and shared error types. It must not depend on exchange, strategy,
execution, persistence, secrets, or operator modules.
"""

from .errors import DataIntegrityError, ManifestError, PrometheusError
from .events import FundingRateEvent
from .exchange_info import (
    ExchangeInfoSnapshot,
    LotSizeFilter,
    MarketLotSizeFilter,
    MinNotionalFilter,
    PriceFilter,
    SymbolInfo,
)
from .intervals import Interval, interval_duration_ms
from .klines import NormalizedKline
from .mark_price_klines import MarkPriceKline
from .symbols import Symbol
from .time import (
    ClockFn,
    close_time_for,
    floor_to_interval,
    is_aligned_open_time,
    utc_now_ms,
)

__all__ = [
    "ClockFn",
    "DataIntegrityError",
    "ExchangeInfoSnapshot",
    "FundingRateEvent",
    "Interval",
    "LotSizeFilter",
    "ManifestError",
    "MarkPriceKline",
    "MarketLotSizeFilter",
    "MinNotionalFilter",
    "NormalizedKline",
    "PriceFilter",
    "PrometheusError",
    "Symbol",
    "SymbolInfo",
    "close_time_for",
    "floor_to_interval",
    "interval_duration_ms",
    "is_aligned_open_time",
    "utc_now_ms",
]
