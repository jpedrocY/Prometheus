from __future__ import annotations

from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.research.backtest.simulation_clock import (
    bar_visible_at,
    next_15m_open_time,
    select_latest_completed_1h,
)
from tests.unit.strategy.conftest import ANCHOR_MS, kline


def test_bar_visible_at_boundary() -> None:
    bar = kline(open_time=ANCHOR_MS, open=100.0, high=101.0, low=99.0, close=100.5)
    # Visible when t_now_ms >= open_time + duration
    assert not bar_visible_at(ANCHOR_MS + 15 * 60 * 1000 - 1, bar)
    assert bar_visible_at(ANCHOR_MS + 15 * 60 * 1000, bar)


def test_select_latest_completed_1h_returns_most_recent_eligible() -> None:
    bars_1h = []
    t = ANCHOR_MS
    d = interval_duration_ms(Interval.I_1H)
    for i in range(5):
        bars_1h.append(
            kline(
                interval=Interval.I_1H,
                open_time=t + i * d,
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.5,
            )
        )
    # Decision time: end of bar index 2 (inclusive).
    decision = bars_1h[2].open_time + d
    chosen = select_latest_completed_1h(bars_1h, decision)
    assert chosen is not None
    assert chosen.open_time == bars_1h[2].open_time


def test_select_latest_completed_1h_returns_none_if_none_eligible() -> None:
    bars_1h = [
        kline(
            interval=Interval.I_1H,
            open_time=ANCHOR_MS,
            open=100.0,
            high=101.0,
            low=99.0,
            close=100.5,
        )
    ]
    # Decision time before the bar closes.
    assert select_latest_completed_1h(bars_1h, ANCHOR_MS + 1000) is None


def test_next_15m_open_time() -> None:
    bar = kline(open_time=ANCHOR_MS, open=100.0, high=101.0, low=99.0, close=100.5)
    assert next_15m_open_time(bar) == ANCHOR_MS + 15 * 60 * 1000
