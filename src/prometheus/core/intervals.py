"""Canonical bar intervals and their durations in UTC milliseconds."""

from __future__ import annotations

from enum import StrEnum


class Interval(StrEnum):
    """Supported bar intervals for Prometheus v1.

    The v1 strategy uses 15m for signal decisions and 1h for higher-timeframe
    bias. Additional intervals may be added in later phases.
    """

    I_15M = "15m"
    I_1H = "1h"


_INTERVAL_DURATION_MS: dict[Interval, int] = {
    Interval.I_15M: 15 * 60 * 1000,
    Interval.I_1H: 60 * 60 * 1000,
}


def interval_duration_ms(interval: Interval) -> int:
    """Return the duration of a bar interval in UTC milliseconds."""
    return _INTERVAL_DURATION_MS[interval]
