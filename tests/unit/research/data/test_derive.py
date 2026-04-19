from __future__ import annotations

from typing import Any

import pytest

from prometheus.core.errors import DataIntegrityError
from prometheus.core.intervals import Interval
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol
from prometheus.research.data.derive import derive_1h_from_15m

ANCHOR_MS = 1_774_224_000_000  # 2026-04-01T00:00:00Z, 1h-aligned
FIFTEEN_MIN_MS = 15 * 60 * 1000
ONE_HOUR_MS = 60 * 60 * 1000


def _kline_15m(
    bucket_start_ms: int,
    index_in_bucket: int,
    **overrides: Any,
) -> NormalizedKline:
    open_time = bucket_start_ms + index_in_bucket * FIFTEEN_MIN_MS
    close_time = open_time + FIFTEEN_MIN_MS - 1
    base: dict[str, Any] = {
        "symbol": Symbol.BTCUSDT,
        "interval": Interval.I_15M,
        "open_time": open_time,
        "close_time": close_time,
        "open": 65000.0 + index_in_bucket,
        "high": 65100.0 + index_in_bucket,
        "low": 64900.0 + index_in_bucket,
        "close": 65050.0 + index_in_bucket,
        "volume": 10.0,
        "quote_asset_volume": 650_000.0,
        "trade_count": 100,
        "taker_buy_base_volume": 5.0,
        "taker_buy_quote_volume": 325_000.0,
        "source": "test",
    }
    base.update(overrides)
    return NormalizedKline(**base)


def _happy_bucket(bucket_start_ms: int) -> list[NormalizedKline]:
    return [_kline_15m(bucket_start_ms, i) for i in range(4)]


def test_empty_input_returns_empty() -> None:
    derived, invalid = derive_1h_from_15m([])
    assert derived == []
    assert invalid == []


def test_single_complete_bucket() -> None:
    klines = _happy_bucket(ANCHOR_MS)
    derived, invalid = derive_1h_from_15m(klines)
    assert invalid == []
    assert len(derived) == 1

    hour = derived[0]
    assert hour.interval is Interval.I_1H
    assert hour.open_time == ANCHOR_MS
    assert hour.close_time == ANCHOR_MS + ONE_HOUR_MS - 1
    assert hour.open == 65000.0  # first 15m open
    assert hour.close == 65053.0  # last 15m close (65050 + 3)
    assert hour.high == max(65100.0 + i for i in range(4))
    assert hour.low == min(64900.0 + i for i in range(4))
    assert hour.volume == 40.0  # 4 * 10
    assert hour.trade_count == 400
    assert hour.source == "derived:15m->1h"


def test_two_complete_buckets() -> None:
    klines = _happy_bucket(ANCHOR_MS) + _happy_bucket(ANCHOR_MS + ONE_HOUR_MS)
    derived, invalid = derive_1h_from_15m(klines)
    assert invalid == []
    assert len(derived) == 2
    assert derived[0].open_time == ANCHOR_MS
    assert derived[1].open_time == ANCHOR_MS + ONE_HOUR_MS


def test_partial_bucket_is_invalid_and_not_emitted() -> None:
    klines = _happy_bucket(ANCHOR_MS)[:3]
    derived, invalid = derive_1h_from_15m(klines)
    assert derived == []
    assert len(invalid) == 1
    assert invalid[0].start_open_time_ms == ANCHOR_MS
    assert invalid[0].reason == "partial_1h_bucket:3_of_4"


def test_complete_and_partial_mixed() -> None:
    klines = _happy_bucket(ANCHOR_MS) + _happy_bucket(ANCHOR_MS + ONE_HOUR_MS)[:2]
    derived, invalid = derive_1h_from_15m(klines)
    assert len(derived) == 1
    assert derived[0].open_time == ANCHOR_MS
    assert len(invalid) == 1
    assert invalid[0].start_open_time_ms == ANCHOR_MS + ONE_HOUR_MS


def test_rejects_non_15m_input() -> None:
    kline = NormalizedKline(
        symbol=Symbol.BTCUSDT,
        interval=Interval.I_1H,
        open_time=ANCHOR_MS,
        close_time=ANCHOR_MS + ONE_HOUR_MS - 1,
        open=1.0,
        high=1.0,
        low=1.0,
        close=1.0,
        volume=0.0,
        quote_asset_volume=0.0,
        trade_count=0,
        taker_buy_base_volume=0.0,
        taker_buy_quote_volume=0.0,
        source="test",
    )
    with pytest.raises(DataIntegrityError):
        derive_1h_from_15m([kline])


def test_rejects_mixed_symbols() -> None:
    btc = _kline_15m(ANCHOR_MS, 0)
    eth = _kline_15m(ANCHOR_MS, 1, symbol=Symbol.ETHUSDT)
    with pytest.raises(DataIntegrityError):
        derive_1h_from_15m([btc, eth])


def test_derived_1h_bar_close_time_is_strictly_before_next_hour() -> None:
    klines = _happy_bucket(ANCHOR_MS)
    derived, _ = derive_1h_from_15m(klines)
    assert derived[0].close_time < ANCHOR_MS + ONE_HOUR_MS


def test_no_forward_leakage_past_decision_time() -> None:
    # Decision time is the end of the first 1h bucket (close of last 15m bar).
    # The 1h bar for this bucket is fully completed BEFORE the decision
    # time for any signal evaluated on the NEXT 15m bar.
    klines = _happy_bucket(ANCHOR_MS) + _happy_bucket(ANCHOR_MS + ONE_HOUR_MS)
    derived, _ = derive_1h_from_15m(klines)
    first_bucket_close = ANCHOR_MS + ONE_HOUR_MS - 1
    # The 1h bar for the first bucket has close_time strictly <=
    # any 15m decision time >= first_bucket_close + 1.
    decision_time_after_first_bucket = first_bucket_close + 1
    bar_visible = derived[0]
    assert bar_visible.close_time < decision_time_after_first_bucket
