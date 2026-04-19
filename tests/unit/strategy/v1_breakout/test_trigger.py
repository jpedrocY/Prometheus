from __future__ import annotations

from prometheus.core.symbols import Symbol
from prometheus.strategy.types import SetupWindow, TrendBias
from prometheus.strategy.v1_breakout.trigger import (
    evaluate_long_trigger,
    evaluate_short_trigger,
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


def _breakout_bar(
    close: float, high: float | None = None, low: float | None = None, open_: float = 100.0
):
    h = high if high is not None else close + 0.5
    lo = low if low is not None else min(open_, close) - 0.2
    return kline(
        open_time=ANCHOR_MS + 8 * 15 * 60 * 1000,
        open=open_,
        high=h,
        low=lo,
        close=close,
    )


class TestLongTrigger:
    def test_happy_long_signal(self) -> None:
        setup = _setup(high=101.0, low=99.0, atr15=1.0)
        bar = _breakout_bar(close=102.0, high=102.3, low=100.5, open_=100.7)
        sig = evaluate_long_trigger(
            bias=TrendBias.LONG,
            setup=setup,
            breakout_bar=bar,
            prev_15m_close=100.5,
            atr_20_15m=1.0,
            atr_20_1h=1.0,  # normalized ATR = 1/100 = 1% in [0.2%, 2%]
            latest_1h_close=100.0,
        )
        assert sig is not None
        assert sig.atr_20_15m == 1.0
        assert sig.normalized_atr_1h == 0.01

    def test_wrong_bias_rejects(self) -> None:
        bar = _breakout_bar(close=102.0)
        assert (
            evaluate_long_trigger(
                bias=TrendBias.SHORT,
                setup=_setup(),
                breakout_bar=bar,
                prev_15m_close=100.5,
                atr_20_15m=1.0,
                atr_20_1h=1.0,
                latest_1h_close=100.0,
            )
            is None
        )

    def test_no_setup_rejects(self) -> None:
        bar = _breakout_bar(close=102.0)
        assert (
            evaluate_long_trigger(
                bias=TrendBias.LONG,
                setup=None,
                breakout_bar=bar,
                prev_15m_close=100.5,
                atr_20_15m=1.0,
                atr_20_1h=1.0,
                latest_1h_close=100.0,
            )
            is None
        )

    def test_close_below_trigger_level_rejects(self) -> None:
        # trigger_level = 101 + 0.10*1 = 101.1; close = 101.05 -> reject
        bar = _breakout_bar(close=101.05, high=101.3, low=100.0, open_=100.8)
        assert (
            evaluate_long_trigger(
                bias=TrendBias.LONG,
                setup=_setup(),
                breakout_bar=bar,
                prev_15m_close=100.5,
                atr_20_15m=1.0,
                atr_20_1h=1.0,
                latest_1h_close=100.0,
            )
            is None
        )

    def test_true_range_too_small_rejects(self) -> None:
        # TR must be >= 1.0 * ATR. If high-low = 0.3 and prev_close=100.5
        # then TR ~= 0.3 < 1.0 -> reject
        bar = _breakout_bar(close=102.0, high=102.1, low=101.8, open_=101.9)
        assert (
            evaluate_long_trigger(
                bias=TrendBias.LONG,
                setup=_setup(high=101.0, low=99.0, atr15=1.0),
                breakout_bar=bar,
                prev_15m_close=101.9,
                atr_20_15m=1.0,
                atr_20_1h=1.0,
                latest_1h_close=100.0,
            )
            is None
        )

    def test_close_not_in_top_quarter_rejects(self) -> None:
        # range = 102.0 - 100.0 = 2.0; close_loc = (101.2-100.0)/2 = 0.6 < 0.75
        bar = _breakout_bar(close=101.2, high=102.0, low=100.0, open_=100.0)
        assert (
            evaluate_long_trigger(
                bias=TrendBias.LONG,
                setup=_setup(),
                breakout_bar=bar,
                prev_15m_close=100.5,
                atr_20_15m=1.0,
                atr_20_1h=1.0,
                latest_1h_close=100.0,
            )
            is None
        )

    def test_normalized_atr_out_of_range_rejects(self) -> None:
        # ATR_1h / close = 0.001 -> 0.1% < 0.20% lower bound
        bar = _breakout_bar(close=102.0, high=102.3, low=100.5, open_=100.7)
        assert (
            evaluate_long_trigger(
                bias=TrendBias.LONG,
                setup=_setup(),
                breakout_bar=bar,
                prev_15m_close=100.5,
                atr_20_15m=1.0,
                atr_20_1h=0.1,  # normalized = 0.1%
                latest_1h_close=100.0,
            )
            is None
        )


class TestShortTrigger:
    def test_happy_short_signal(self) -> None:
        setup = _setup(high=101.0, low=99.0, atr15=1.0)
        # trigger_level = 99 - 0.1 = 98.9; close = 98.1; high-low = 1.5;
        # location = (98.1 - 98.0) / 1.5 = 0.067 <= 0.25 -> bottom-25% OK.
        bar = _breakout_bar(close=98.1, high=99.5, low=98.0, open_=99.3)
        sig = evaluate_short_trigger(
            bias=TrendBias.SHORT,
            setup=setup,
            breakout_bar=bar,
            prev_15m_close=99.3,
            atr_20_15m=1.0,
            atr_20_1h=1.0,
            latest_1h_close=100.0,
        )
        assert sig is not None

    def test_wrong_bias_rejects(self) -> None:
        bar = _breakout_bar(close=98.5, high=99.5, low=98.0, open_=99.3)
        assert (
            evaluate_short_trigger(
                bias=TrendBias.LONG,
                setup=_setup(),
                breakout_bar=bar,
                prev_15m_close=99.3,
                atr_20_15m=1.0,
                atr_20_1h=1.0,
                latest_1h_close=100.0,
            )
            is None
        )
