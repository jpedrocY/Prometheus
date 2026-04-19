from __future__ import annotations

import pytest

from prometheus.research.backtest.stops import StopHit, evaluate_stop_hit
from tests.unit.strategy.conftest import ANCHOR_MS, mark


def _mark(open_: float, high: float, low: float, close: float) -> object:
    return mark(open_time=ANCHOR_MS, open=open_, high=high, low=low, close=close)


class TestLongStopHit:
    def test_no_hit_when_low_above_stop(self) -> None:
        bar = _mark(100.0, 101.0, 99.5, 100.5)
        assert (
            evaluate_stop_hit(
                direction_long=True, current_stop=99.0, mark_bar=bar, slippage_bps=0.0
            )
            is None
        )

    def test_intrabar_hit_fills_at_stop_level(self) -> None:
        bar = _mark(100.0, 100.5, 98.8, 99.2)
        hit = evaluate_stop_hit(
            direction_long=True, current_stop=99.0, mark_bar=bar, slippage_bps=0.0
        )
        assert isinstance(hit, StopHit)
        assert hit.fill_price == pytest.approx(99.0)
        assert hit.was_gap_through is False

    def test_gap_through_fills_at_bar_open(self) -> None:
        # Bar opens below stop -> adverse gap; fill at open.
        bar = _mark(98.5, 99.5, 98.0, 98.8)
        hit = evaluate_stop_hit(
            direction_long=True, current_stop=99.0, mark_bar=bar, slippage_bps=0.0
        )
        assert hit is not None
        assert hit.was_gap_through is True
        assert hit.fill_price == pytest.approx(98.5)

    def test_slippage_applied_adversely(self) -> None:
        bar = _mark(100.0, 100.5, 98.8, 99.2)
        hit = evaluate_stop_hit(
            direction_long=True, current_stop=99.0, mark_bar=bar, slippage_bps=10.0
        )
        assert hit is not None
        # Exit long: slippage reduces fill.
        assert hit.fill_price == pytest.approx(99.0 * 0.999)


class TestShortStopHit:
    def test_no_hit_when_high_below_stop(self) -> None:
        bar = _mark(100.0, 100.4, 99.5, 99.8)
        assert (
            evaluate_stop_hit(
                direction_long=False, current_stop=101.0, mark_bar=bar, slippage_bps=0.0
            )
            is None
        )

    def test_intrabar_hit_fills_at_stop_level(self) -> None:
        bar = _mark(100.0, 101.2, 99.8, 101.0)
        hit = evaluate_stop_hit(
            direction_long=False, current_stop=101.0, mark_bar=bar, slippage_bps=0.0
        )
        assert hit is not None
        assert hit.was_gap_through is False
        assert hit.fill_price == pytest.approx(101.0)

    def test_gap_through_up_fills_at_bar_open(self) -> None:
        bar = _mark(101.5, 102.5, 101.0, 102.0)
        hit = evaluate_stop_hit(
            direction_long=False, current_stop=101.0, mark_bar=bar, slippage_bps=0.0
        )
        assert hit is not None
        assert hit.was_gap_through is True
        assert hit.fill_price == pytest.approx(101.5)


def test_invalid_stop() -> None:
    bar = _mark(100.0, 101.0, 99.0, 100.5)
    with pytest.raises(ValueError):
        evaluate_stop_hit(direction_long=True, current_stop=0.0, mark_bar=bar, slippage_bps=0.0)


def test_negative_slippage() -> None:
    bar = _mark(100.0, 101.0, 99.0, 100.5)
    with pytest.raises(ValueError):
        evaluate_stop_hit(direction_long=True, current_stop=99.0, mark_bar=bar, slippage_bps=-1.0)
