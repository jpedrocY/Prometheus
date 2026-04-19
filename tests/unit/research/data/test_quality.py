from __future__ import annotations

from typing import Any

import pytest

from prometheus.core.intervals import Interval
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol
from prometheus.research.data.quality import (
    check_no_duplicates,
    check_no_future_bars,
    check_no_missing_bars,
    check_timestamp_monotonic,
)

ANCHOR_MS = 1_774_224_000_000
FIFTEEN_MIN_MS = 15 * 60 * 1000


def _kline(i: int, **overrides: Any) -> NormalizedKline:
    base: dict[str, Any] = {
        "symbol": Symbol.BTCUSDT,
        "interval": Interval.I_15M,
        "open_time": ANCHOR_MS + i * FIFTEEN_MIN_MS,
        "close_time": ANCHOR_MS + (i + 1) * FIFTEEN_MIN_MS - 1,
        "open": 65000.0,
        "high": 65100.0,
        "low": 64900.0,
        "close": 65050.0,
        "volume": 1.0,
        "quote_asset_volume": 65_000.0,
        "trade_count": 1,
        "taker_buy_base_volume": 0.5,
        "taker_buy_quote_volume": 32_500.0,
        "source": "test",
    }
    base.update(overrides)
    return NormalizedKline(**base)


def test_no_duplicates_empty() -> None:
    assert check_no_duplicates([]) == []


def test_no_duplicates_clean_sequence() -> None:
    klines = [_kline(i) for i in range(4)]
    assert check_no_duplicates(klines) == []


def test_duplicates_detected() -> None:
    klines = [_kline(0), _kline(1), _kline(1), _kline(2)]
    reports = check_no_duplicates(klines)
    assert len(reports) == 1
    assert reports[0].count == 2
    assert reports[0].open_time == ANCHOR_MS + FIFTEEN_MIN_MS


def test_monotonic_empty() -> None:
    assert check_timestamp_monotonic([]) == []


def test_monotonic_happy() -> None:
    assert check_timestamp_monotonic([_kline(i) for i in range(4)]) == []


def test_monotonic_violation_backward_jump() -> None:
    klines = [_kline(0), _kline(2), _kline(1)]
    violations = check_timestamp_monotonic(klines)
    assert violations
    assert violations[0] == (
        ANCHOR_MS + 2 * FIFTEEN_MIN_MS,
        ANCHOR_MS + FIFTEEN_MIN_MS,
    )


def test_no_missing_happy() -> None:
    klines = [_kline(i) for i in range(4)]
    missing = check_no_missing_bars(
        klines,
        expected_start_ms=ANCHOR_MS,
        expected_end_ms=ANCHOR_MS + 3 * FIFTEEN_MIN_MS,
        interval=Interval.I_15M,
    )
    assert missing == []


def test_missing_detects_single_gap() -> None:
    klines = [_kline(0), _kline(1), _kline(3)]  # index 2 missing
    missing = check_no_missing_bars(
        klines,
        expected_start_ms=ANCHOR_MS,
        expected_end_ms=ANCHOR_MS + 3 * FIFTEEN_MIN_MS,
        interval=Interval.I_15M,
    )
    assert len(missing) == 1
    assert missing[0].start_open_time_ms == ANCHOR_MS + 2 * FIFTEEN_MIN_MS
    assert missing[0].missing_count == 1


def test_missing_detects_run() -> None:
    klines = [_kline(0), _kline(3)]  # 1, 2 missing
    missing = check_no_missing_bars(
        klines,
        expected_start_ms=ANCHOR_MS,
        expected_end_ms=ANCHOR_MS + 3 * FIFTEEN_MIN_MS,
        interval=Interval.I_15M,
    )
    assert len(missing) == 1
    assert missing[0].start_open_time_ms == ANCHOR_MS + FIFTEEN_MIN_MS
    assert missing[0].end_open_time_ms == ANCHOR_MS + 2 * FIFTEEN_MIN_MS
    assert missing[0].missing_count == 2


def test_missing_rejects_unaligned_bounds() -> None:
    with pytest.raises(ValueError):
        check_no_missing_bars(
            [],
            expected_start_ms=ANCHOR_MS + 1,
            expected_end_ms=ANCHOR_MS + FIFTEEN_MIN_MS,
            interval=Interval.I_15M,
        )


def test_no_future_bars_happy() -> None:
    klines = [_kline(i) for i in range(3)]
    assert check_no_future_bars(klines, now_ms=ANCHOR_MS + 10 * FIFTEEN_MIN_MS) == []


def test_no_future_bars_catches_future() -> None:
    klines = [_kline(0), _kline(5)]
    offenders = check_no_future_bars(klines, now_ms=ANCHOR_MS + 2 * FIFTEEN_MIN_MS)
    assert len(offenders) == 1
    assert offenders[0].open_time == ANCHOR_MS + 5 * FIFTEEN_MIN_MS
