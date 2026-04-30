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
from .governance import (
    BreakEvenRule,
    EmaSlopeMethod,
    GovernanceLabel,
    GovernanceLabelError,
    StagnationWindowRole,
    StopTriggerDomain,
    is_fail_closed,
    parse_break_even_rule,
    parse_ema_slope_method,
    parse_stagnation_window_role,
    parse_stop_trigger_domain,
    require_valid,
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
    "BreakEvenRule",
    "ClockFn",
    "DataIntegrityError",
    "EmaSlopeMethod",
    "ExchangeInfoSnapshot",
    "FundingRateEvent",
    "GovernanceLabel",
    "GovernanceLabelError",
    "Interval",
    "LotSizeFilter",
    "ManifestError",
    "MarkPriceKline",
    "MarketLotSizeFilter",
    "MinNotionalFilter",
    "NormalizedKline",
    "PriceFilter",
    "PrometheusError",
    "StagnationWindowRole",
    "StopTriggerDomain",
    "Symbol",
    "SymbolInfo",
    "close_time_for",
    "floor_to_interval",
    "interval_duration_ms",
    "is_aligned_open_time",
    "is_fail_closed",
    "parse_break_even_rule",
    "parse_ema_slope_method",
    "parse_stagnation_window_role",
    "parse_stop_trigger_domain",
    "require_valid",
    "utc_now_ms",
]
