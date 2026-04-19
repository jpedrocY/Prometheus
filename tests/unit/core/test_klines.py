from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from prometheus.core.intervals import Interval
from prometheus.core.klines import NormalizedKline
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
        "volume": 12.5,
        "quote_asset_volume": 812_500.0,
        "trade_count": 42,
        "taker_buy_base_volume": 6.0,
        "taker_buy_quote_volume": 390_000.0,
        "source": "test",
    }
    base.update(overrides)
    return base


def test_valid_kline_accepts() -> None:
    kline = NormalizedKline(**_kwargs())
    assert kline.symbol is Symbol.BTCUSDT
    assert kline.interval is Interval.I_15M
    assert kline.source == "test"


def test_kline_is_frozen() -> None:
    kline = NormalizedKline(**_kwargs())
    with pytest.raises(ValidationError):
        kline.open = 1.0  # type: ignore[misc]


def test_extra_field_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(), unexpected="no")


def test_unaligned_open_time_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(open_time=ANCHOR_MS + 1, close_time=ANCHOR_MS + 15 * 60 * 1000))


def test_close_time_mismatch_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(close_time=ANCHOR_MS + 15 * 60 * 1000))  # off by one


def test_high_below_open_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(open=65100.0, high=65000.0))


def test_low_above_close_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(low=65060.0, close=65050.0))


def test_negative_volume_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(volume=-0.001))


def test_negative_trade_count_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(trade_count=-1))


def test_string_open_time_rejected_in_strict_mode() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(open_time=str(ANCHOR_MS)))


def test_empty_source_rejected() -> None:
    with pytest.raises(ValidationError):
        NormalizedKline(**_kwargs(source=""))


def test_1h_kline_valid() -> None:
    hour_close = ANCHOR_MS + 60 * 60 * 1000 - 1
    kline = NormalizedKline(
        **_kwargs(interval=Interval.I_1H, open_time=ANCHOR_MS, close_time=hour_close)
    )
    assert kline.interval is Interval.I_1H
