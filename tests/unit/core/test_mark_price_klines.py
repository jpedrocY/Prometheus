from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from prometheus.core.intervals import Interval
from prometheus.core.mark_price_klines import MarkPriceKline
from prometheus.core.symbols import Symbol

ANCHOR_MS = 1_774_224_000_000  # 2026-04-01T00:00:00Z


def _kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "symbol": Symbol.BTCUSDT,
        "interval": Interval.I_15M,
        "open_time": ANCHOR_MS,
        "close_time": ANCHOR_MS + 15 * 60 * 1000 - 1,
        "open": 65000.0,
        "high": 65100.0,
        "low": 64900.0,
        "close": 65050.0,
        "source": "test",
    }
    base.update(overrides)
    return base


def test_valid_mark_price_kline_accepts() -> None:
    kline = MarkPriceKline(**_kwargs())
    assert kline.symbol is Symbol.BTCUSDT
    assert kline.interval is Interval.I_15M
    assert kline.source == "test"


def test_frozen() -> None:
    kline = MarkPriceKline(**_kwargs())
    with pytest.raises(ValidationError):
        kline.open = 1.0  # type: ignore[misc]


def test_extra_field_rejected() -> None:
    # Mark-price klines do NOT carry volume fields; asserting those are
    # rejected by the strict extra="forbid" config.
    with pytest.raises(ValidationError):
        MarkPriceKline(**_kwargs(), volume=0.0)


def test_unaligned_open_time_rejected() -> None:
    with pytest.raises(ValidationError):
        MarkPriceKline(**_kwargs(open_time=ANCHOR_MS + 1, close_time=ANCHOR_MS + 15 * 60 * 1000))


def test_close_time_mismatch_rejected() -> None:
    with pytest.raises(ValidationError):
        MarkPriceKline(**_kwargs(close_time=ANCHOR_MS + 15 * 60 * 1000))


def test_high_below_open_rejected() -> None:
    with pytest.raises(ValidationError):
        MarkPriceKline(**_kwargs(open=65100.0, high=65000.0))


def test_negative_price_rejected() -> None:
    with pytest.raises(ValidationError):
        MarkPriceKline(**_kwargs(open=-1.0, high=65100.0, low=64900.0, close=65050.0))


def test_zero_price_rejected() -> None:
    with pytest.raises(ValidationError):
        MarkPriceKline(**_kwargs(open=0.0, high=65100.0, low=64900.0, close=65050.0))


def test_1h_interval_valid() -> None:
    hour_close = ANCHOR_MS + 60 * 60 * 1000 - 1
    kline = MarkPriceKline(
        **_kwargs(interval=Interval.I_1H, open_time=ANCHOR_MS, close_time=hour_close)
    )
    assert kline.interval is Interval.I_1H
