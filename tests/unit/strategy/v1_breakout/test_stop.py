from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol
from prometheus.strategy.types import Direction, SetupWindow
from prometheus.strategy.v1_breakout.stop import (
    FILTER_MAX_ATR_MULT,
    FILTER_MIN_ATR_MULT,
    STOP_BUFFER_ATR_MULT,
    compute_initial_stop,
    passes_stop_distance_filter,
)

from ..conftest import ANCHOR_MS, kline


def _setup(high: float = 101.0, low: float = 99.0, atr15: float = 1.0) -> SetupWindow:
    return SetupWindow(
        symbol=Symbol.BTCUSDT,
        first_bar_open_time=ANCHOR_MS,
        last_bar_open_time=ANCHOR_MS + 7 * 15 * 60 * 1000,
        setup_high=high,
        setup_low=low,
        setup_range_width=high - low,
        net_drift_abs=0.2,
        atr_20_15m=atr15,
    )


class TestComputeInitialStop:
    def test_long_uses_min_of_setup_low_and_breakout_low(self) -> None:
        setup = _setup(high=101.0, low=99.0)
        # Breakout bar low above setup_low -> stop = setup_low - 0.10*ATR = 98.9
        bar = kline(
            open_time=ANCHOR_MS + 8 * 15 * 60 * 1000, open=100.0, high=102.0, low=99.5, close=101.5
        )
        stop = compute_initial_stop(Direction.LONG, setup, bar, atr_20_15m=1.0)
        assert stop == pytest.approx(99.0 - STOP_BUFFER_ATR_MULT * 1.0)

    def test_long_uses_breakout_low_when_lower(self) -> None:
        setup = _setup(high=101.0, low=99.0)
        bar = kline(
            open_time=ANCHOR_MS + 8 * 15 * 60 * 1000, open=100.0, high=102.0, low=98.5, close=101.5
        )
        stop = compute_initial_stop(Direction.LONG, setup, bar, atr_20_15m=1.0)
        assert stop == pytest.approx(98.5 - 0.1)

    def test_short_uses_max_of_setup_high_and_breakout_high(self) -> None:
        setup = _setup(high=101.0, low=99.0)
        bar = kline(
            open_time=ANCHOR_MS + 8 * 15 * 60 * 1000, open=100.0, high=101.5, low=98.5, close=98.8
        )
        stop = compute_initial_stop(Direction.SHORT, setup, bar, atr_20_15m=1.0)
        # setup_high=101 vs breakout_high=101.5 -> 101.5 + 0.1 = 101.6
        assert stop == pytest.approx(101.5 + 0.1)

    def test_rejects_zero_atr(self) -> None:
        setup = _setup()
        bar = kline(
            open_time=ANCHOR_MS + 8 * 15 * 60 * 1000, open=100.0, high=101.0, low=99.0, close=100.5
        )
        with pytest.raises(ValueError):
            compute_initial_stop(Direction.LONG, setup, bar, atr_20_15m=0.0)


class TestStopDistanceFilter:
    def test_in_range_accepts(self) -> None:
        assert passes_stop_distance_filter(stop_distance=1.0, atr_20_15m=1.0)

    def test_below_min_rejects(self) -> None:
        # 0.59 * 1.0 < 0.60 lower bound
        assert not passes_stop_distance_filter(stop_distance=0.59, atr_20_15m=1.0)

    def test_above_max_rejects(self) -> None:
        # 1.85 * 1.0 > 1.80 upper bound
        assert not passes_stop_distance_filter(stop_distance=1.85, atr_20_15m=1.0)

    def test_boundary_exactly_min(self) -> None:
        assert passes_stop_distance_filter(stop_distance=FILTER_MIN_ATR_MULT * 1.0, atr_20_15m=1.0)

    def test_boundary_exactly_max(self) -> None:
        assert passes_stop_distance_filter(stop_distance=FILTER_MAX_ATR_MULT * 1.0, atr_20_15m=1.0)

    def test_invalid_inputs(self) -> None:
        assert not passes_stop_distance_filter(stop_distance=0.0, atr_20_15m=1.0)
        assert not passes_stop_distance_filter(stop_distance=-1.0, atr_20_15m=1.0)
        assert not passes_stop_distance_filter(stop_distance=1.0, atr_20_15m=0.0)
