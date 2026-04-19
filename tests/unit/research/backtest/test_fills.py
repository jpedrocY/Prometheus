from __future__ import annotations

import pytest

from prometheus.research.backtest.fills import (
    FillSide,
    compute_fill_price,
    entry_fill_price,
    exit_fill_price,
)
from tests.unit.strategy.conftest import ANCHOR_MS, kline

from .conftest import default_config


def test_compute_fill_price_entry_long_adverse_higher() -> None:
    fp = compute_fill_price(raw_price=100.0, side=FillSide.ENTRY_LONG, slippage_bps=10.0)
    assert fp == pytest.approx(100.0 * 1.001)


def test_compute_fill_price_entry_short_adverse_lower() -> None:
    fp = compute_fill_price(raw_price=100.0, side=FillSide.ENTRY_SHORT, slippage_bps=10.0)
    assert fp == pytest.approx(100.0 * 0.999)


def test_compute_fill_price_exit_long_adverse_lower() -> None:
    # Closing a long = selling; gets the bid (lower).
    fp = compute_fill_price(raw_price=100.0, side=FillSide.EXIT_LONG, slippage_bps=10.0)
    assert fp == pytest.approx(100.0 * 0.999)


def test_compute_fill_price_exit_short_adverse_higher(tmp_path) -> None:
    # Closing a short = buying; pays the ask (higher).
    fp = compute_fill_price(raw_price=100.0, side=FillSide.EXIT_SHORT, slippage_bps=10.0)
    assert fp == pytest.approx(100.0 * 1.001)


def test_entry_fill_price_uses_next_bar_open(tmp_path) -> None:
    cfg = default_config(tmp_path)
    next_bar = kline(open_time=ANCHOR_MS, open=100.5, high=101.0, low=100.0, close=100.8)
    fp_long = entry_fill_price(next_bar=next_bar, direction_long=True, config=cfg)
    fp_short = entry_fill_price(next_bar=next_bar, direction_long=False, config=cfg)
    # MEDIUM bucket = 3 bps
    assert fp_long == pytest.approx(100.5 * 1.0003)
    assert fp_short == pytest.approx(100.5 * 0.9997)


def test_exit_fill_price_uses_next_bar_open(tmp_path) -> None:
    cfg = default_config(tmp_path)
    next_bar = kline(open_time=ANCHOR_MS, open=100.5, high=101.0, low=100.0, close=100.8)
    fp_long = exit_fill_price(next_bar=next_bar, direction_long=True, config=cfg)
    fp_short = exit_fill_price(next_bar=next_bar, direction_long=False, config=cfg)
    assert fp_long == pytest.approx(100.5 * 0.9997)
    assert fp_short == pytest.approx(100.5 * 1.0003)


def test_negative_slippage_rejected() -> None:
    with pytest.raises(ValueError):
        compute_fill_price(raw_price=100.0, side=FillSide.ENTRY_LONG, slippage_bps=-1.0)


def test_zero_slippage_no_change() -> None:
    assert compute_fill_price(raw_price=100.0, side=FillSide.ENTRY_LONG, slippage_bps=0.0) == 100.0
