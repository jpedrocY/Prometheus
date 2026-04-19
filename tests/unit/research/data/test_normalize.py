from __future__ import annotations

from typing import Any

import pytest

from prometheus.core.errors import DataIntegrityError
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.normalize import normalize_rows

ANCHOR_MS = 1_774_224_000_000


def _row(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
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
    }
    base.update(overrides)
    return base


def test_normalize_single_valid_row() -> None:
    klines = normalize_rows(
        [_row()],
        symbol=Symbol.BTCUSDT,
        interval=Interval.I_15M,
        source="test",
    )
    assert len(klines) == 1
    assert klines[0].symbol is Symbol.BTCUSDT
    assert klines[0].source == "test"


def test_normalize_rejects_unaligned_row() -> None:
    with pytest.raises(DataIntegrityError) as exc_info:
        normalize_rows(
            [_row(open_time=ANCHOR_MS + 1, close_time=ANCHOR_MS + 15 * 60 * 1000)],
            symbol=Symbol.BTCUSDT,
            interval=Interval.I_15M,
            source="test",
        )
    assert "row 0" in str(exc_info.value)


def test_normalize_reports_row_index_on_failure() -> None:
    second_open = ANCHOR_MS + 15 * 60 * 1000
    second_close = ANCHOR_MS + 2 * 15 * 60 * 1000 - 1
    rows = [
        _row(),
        _row(open_time=second_open, close_time=second_close, high=1.0, low=2.0),
    ]
    with pytest.raises(DataIntegrityError) as exc_info:
        normalize_rows(rows, symbol=Symbol.BTCUSDT, interval=Interval.I_15M, source="test")
    assert "row 1" in str(exc_info.value)


def test_normalize_many_rows() -> None:
    rows = [
        _row(
            open_time=ANCHOR_MS + i * 15 * 60 * 1000,
            close_time=ANCHOR_MS + (i + 1) * 15 * 60 * 1000 - 1,
        )
        for i in range(8)
    ]
    klines = normalize_rows(rows, symbol=Symbol.BTCUSDT, interval=Interval.I_15M, source="test")
    assert len(klines) == 8
    assert [k.open_time for k in klines] == [ANCHOR_MS + i * 15 * 60 * 1000 for i in range(8)]
