from __future__ import annotations

import math

import pytest

from prometheus.strategy.indicators import ema, true_range, wilder_atr


class TestEMA:
    def test_empty_returns_empty(self) -> None:
        assert ema([], 5) == []

    def test_period_larger_than_input_returns_all_nan(self) -> None:
        out = ema([1.0, 2.0, 3.0], 5)
        assert len(out) == 3
        assert all(math.isnan(x) for x in out)

    def test_warmup_positions_are_nan(self) -> None:
        out = ema([1.0, 2.0, 3.0, 4.0, 5.0], 3)
        assert math.isnan(out[0])
        assert math.isnan(out[1])
        assert not math.isnan(out[2])

    def test_seed_is_sma(self) -> None:
        values = [1.0, 2.0, 3.0, 10.0, 20.0]
        out = ema(values, 3)
        assert out[2] == pytest.approx(2.0)  # (1 + 2 + 3) / 3

    def test_recursion_against_hand_computed(self) -> None:
        # period=3 alpha=0.5
        values = [10.0, 20.0, 30.0, 40.0]
        out = ema(values, 3)
        # seed at idx 2 = 20.0
        # idx 3 = 0.5*40 + 0.5*20 = 30.0
        assert out[2] == pytest.approx(20.0)
        assert out[3] == pytest.approx(30.0)

    def test_invalid_period(self) -> None:
        with pytest.raises(ValueError):
            ema([1.0, 2.0], 0)
        with pytest.raises(ValueError):
            ema([1.0, 2.0], -1)

    def test_monotonic_ema_tracks_rising_series(self) -> None:
        values = list(range(1, 51))  # 1..50
        out = ema([float(v) for v in values], 10)
        finite = [x for x in out if not math.isnan(x)]
        # EMA of a monotonically increasing series is monotonically increasing.
        assert all(finite[i] <= finite[i + 1] for i in range(len(finite) - 1))


class TestTrueRange:
    def test_first_bar_no_prev_close(self) -> None:
        assert true_range(10.0, 5.0, None) == pytest.approx(5.0)

    def test_uses_max_of_three_ranges(self) -> None:
        # high=10, low=5, prev_close=8 -> max(5, |10-8|=2, |5-8|=3) = 5
        assert true_range(10.0, 5.0, 8.0) == pytest.approx(5.0)

    def test_prev_close_above_range(self) -> None:
        # gap-down scenario: high=10, low=8, prev_close=15
        # hl=2, |10-15|=5, |8-15|=7 -> 7
        assert true_range(10.0, 8.0, 15.0) == pytest.approx(7.0)

    def test_prev_close_below_range(self) -> None:
        # gap-up scenario: high=20, low=15, prev_close=10
        # hl=5, |20-10|=10, |15-10|=5 -> 10
        assert true_range(20.0, 15.0, 10.0) == pytest.approx(10.0)

    def test_low_above_high_raises(self) -> None:
        with pytest.raises(ValueError):
            true_range(5.0, 10.0, None)


class TestWilderATR:
    def test_empty(self) -> None:
        assert wilder_atr([], [], [], 5) == []

    def test_warmup_positions_are_nan(self) -> None:
        highs = [10.0, 11.0, 12.0]
        lows = [9.0, 10.0, 11.0]
        closes = [9.5, 10.5, 11.5]
        out = wilder_atr(highs, lows, closes, 5)
        assert all(math.isnan(x) for x in out)

    def test_seed_is_mean_of_first_period_trs(self) -> None:
        # Constant OHLC with H-L=1 each bar, prev_close = mid: TR = 1 for all.
        n = 25
        highs = [10.5] * n
        lows = [9.5] * n
        closes = [10.0] * n
        out = wilder_atr(highs, lows, closes, 5)
        # Seed at index 5. bar 0 TR=1; bars 1..4 TR=max(1, |10.5-10|=0.5, |9.5-10|=0.5)=1
        assert out[5] == pytest.approx(1.0)

    def test_lengths_must_match(self) -> None:
        with pytest.raises(ValueError):
            wilder_atr([1.0], [1.0, 2.0], [1.0], 3)

    def test_atr_on_constant_series_is_zero_after_first_bar(self) -> None:
        # perfectly flat series: each bar's high == low == close.
        n = 30
        out = wilder_atr([5.0] * n, [5.0] * n, [5.0] * n, 10)
        # seed includes the first bar (TR=0 since high==low) so seed==0.
        # Subsequent wilder step keeps it at 0.
        assert out[10] == pytest.approx(0.0)
        assert out[-1] == pytest.approx(0.0)

    def test_invalid_period(self) -> None:
        with pytest.raises(ValueError):
            wilder_atr([1.0], [1.0], [1.0], 0)
