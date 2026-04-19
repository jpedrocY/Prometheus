"""Shared domain primitives used across the Prometheus codebase.

Per docs/08-architecture/codebase-structure.md, `core` owns UTC millisecond
time utilities, canonical symbol/interval primitives, the normalized kline
type, and shared error types. It must not depend on exchange, strategy,
execution, persistence, secrets, or operator modules.
"""

from .errors import DataIntegrityError, ManifestError, PrometheusError
from .intervals import Interval, interval_duration_ms
from .klines import NormalizedKline
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
    "Interval",
    "ManifestError",
    "NormalizedKline",
    "PrometheusError",
    "Symbol",
    "close_time_for",
    "floor_to_interval",
    "interval_duration_ms",
    "is_aligned_open_time",
    "utc_now_ms",
]
