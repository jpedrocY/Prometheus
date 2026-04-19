from __future__ import annotations

from prometheus.core.intervals import Interval
from prometheus.core.time import (
    close_time_for,
    floor_to_interval,
    is_aligned_open_time,
    utc_now_ms,
)

# Reference anchor: 2026-04-01T00:00:00Z in UTC milliseconds.
ANCHOR_MS = 1_774_224_000_000


def test_utc_now_ms_accepts_injected_clock() -> None:
    assert utc_now_ms(clock=lambda: 42) == 42


def test_utc_now_ms_default_is_positive_int() -> None:
    value = utc_now_ms()
    assert isinstance(value, int)
    assert value > 0


def test_floor_to_interval_15m_already_aligned() -> None:
    assert floor_to_interval(ANCHOR_MS, Interval.I_15M) == ANCHOR_MS


def test_floor_to_interval_15m_mid_bar() -> None:
    mid = ANCHOR_MS + 7 * 60 * 1000  # 7 minutes past anchor
    assert floor_to_interval(mid, Interval.I_15M) == ANCHOR_MS


def test_floor_to_interval_1h_from_15m_aligned_anchor() -> None:
    fifteen_after = ANCHOR_MS + 15 * 60 * 1000
    assert floor_to_interval(fifteen_after, Interval.I_1H) == ANCHOR_MS


def test_is_aligned_open_time_true_cases() -> None:
    assert is_aligned_open_time(ANCHOR_MS, Interval.I_15M)
    assert is_aligned_open_time(ANCHOR_MS, Interval.I_1H)
    assert is_aligned_open_time(ANCHOR_MS + 15 * 60 * 1000, Interval.I_15M)


def test_is_aligned_open_time_false_cases() -> None:
    assert not is_aligned_open_time(ANCHOR_MS + 1, Interval.I_15M)
    assert not is_aligned_open_time(ANCHOR_MS + 15 * 60 * 1000, Interval.I_1H)


def test_close_time_for_15m() -> None:
    assert close_time_for(ANCHOR_MS, Interval.I_15M) == ANCHOR_MS + 15 * 60 * 1000 - 1


def test_close_time_for_1h() -> None:
    assert close_time_for(ANCHOR_MS, Interval.I_1H) == ANCHOR_MS + 60 * 60 * 1000 - 1
