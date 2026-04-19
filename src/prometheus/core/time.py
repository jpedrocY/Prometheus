"""UTC millisecond time utilities.

Canonical time format across Prometheus is UTC Unix milliseconds (integer).
Local timezones are never stored as canonical. See docs/04-data/timestamp-policy.md.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from .intervals import Interval, interval_duration_ms

ClockFn = Callable[[], int]


def _default_clock() -> int:
    return int(time.time() * 1000)


def utc_now_ms(clock: ClockFn | None = None) -> int:
    """Return the current time as UTC Unix milliseconds.

    Pass a deterministic ``clock`` callable in tests to avoid wall-clock
    dependence.
    """
    if clock is None:
        return _default_clock()
    return clock()


def floor_to_interval(ms: int, interval: Interval) -> int:
    """Return the interval-aligned open_time at or before ``ms``."""
    duration = interval_duration_ms(interval)
    return ms - (ms % duration)


def is_aligned_open_time(ms: int, interval: Interval) -> bool:
    """Return True iff ``ms`` is an interval-aligned open_time."""
    return ms % interval_duration_ms(interval) == 0


def close_time_for(open_time_ms: int, interval: Interval) -> int:
    """Return the close_time for a bar that opens at ``open_time_ms``.

    Per docs/04-data/historical-data-spec.md::
        close_time == open_time + interval.duration_ms - 1
    """
    return open_time_ms + interval_duration_ms(interval) - 1
