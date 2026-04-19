from __future__ import annotations

import random
from typing import Any

import httpx
import pytest

from prometheus.core.errors import DataIntegrityError
from prometheus.core.symbols import Symbol
from prometheus.research.data.binance_rest import BinanceRestClient
from prometheus.research.data.funding_rate import (
    fetch_funding_events_raw,
    normalize_funding_events,
)

ANCHOR_MS = 1_774_224_000_000
EIGHT_HOURS_MS = 8 * 60 * 60 * 1000


def _make_event(n: int, *, symbol: str = "BTCUSDT") -> dict[str, Any]:
    return {
        "symbol": symbol,
        "fundingTime": ANCHOR_MS + n * EIGHT_HOURS_MS,
        "fundingRate": "0.0001",
        "markPrice": "65000.0",
    }


def _rest_client(handler: httpx.MockTransport) -> BinanceRestClient:
    return BinanceRestClient(
        httpx.Client(transport=handler),
        pace_ms=0,
        sleep=lambda _: None,
        rng=random.Random(0),
    )


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


def test_fetch_single_page() -> None:
    events = [_make_event(i) for i in range(5)]

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=events)

    rest = _rest_client(httpx.MockTransport(handler))
    out = fetch_funding_events_raw(
        rest,
        symbol=Symbol.BTCUSDT,
        start_time_ms=ANCHOR_MS,
        end_time_ms=ANCHOR_MS + 10 * EIGHT_HOURS_MS,
    )
    assert len(out) == 5


def test_fetch_advances_cursor_on_full_page() -> None:
    # Simulate three pages: 1000, 1000, 10. Cursor must advance past the
    # last fundingTime of each full page.
    full_1 = [_make_event(i) for i in range(1000)]
    full_2 = [_make_event(1000 + i) for i in range(1000)]
    tail = [_make_event(2000 + i) for i in range(10)]
    pages = iter([full_1, full_2, tail])
    observed_cursors: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        params = request.url.params
        observed_cursors.append(int(params["startTime"]))
        return httpx.Response(200, json=next(pages))

    rest = _rest_client(httpx.MockTransport(handler))
    out = fetch_funding_events_raw(
        rest,
        symbol=Symbol.BTCUSDT,
        start_time_ms=ANCHOR_MS,
        end_time_ms=ANCHOR_MS + 5000 * EIGHT_HOURS_MS,
    )
    assert len(out) == 2010
    assert observed_cursors[0] == ANCHOR_MS
    # Cursor after page 1 must be past the last full_1 fundingTime.
    assert observed_cursors[1] == full_1[-1]["fundingTime"] + 1
    assert observed_cursors[2] == full_2[-1]["fundingTime"] + 1


def test_fetch_empty_page_terminates_cleanly() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[])

    rest = _rest_client(httpx.MockTransport(handler))
    out = fetch_funding_events_raw(
        rest,
        symbol=Symbol.BTCUSDT,
        start_time_ms=ANCHOR_MS,
        end_time_ms=ANCHOR_MS + 10 * EIGHT_HOURS_MS,
    )
    assert out == []


def test_fetch_rejects_non_array_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"error": "wat"})

    rest = _rest_client(httpx.MockTransport(handler))
    with pytest.raises(DataIntegrityError):
        fetch_funding_events_raw(
            rest,
            symbol=Symbol.BTCUSDT,
            start_time_ms=ANCHOR_MS,
            end_time_ms=ANCHOR_MS + 10 * EIGHT_HOURS_MS,
        )


def test_fetch_stale_cursor_raises_rather_than_loops() -> None:
    # If Binance ever serves a full page whose last fundingTime does
    # not advance past the cursor, we must raise instead of looping.
    stuck = [
        {"symbol": "BTCUSDT", "fundingTime": ANCHOR_MS, "fundingRate": "0", "markPrice": "1"}
    ] * 1000

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=stuck)

    rest = _rest_client(httpx.MockTransport(handler))
    with pytest.raises(DataIntegrityError):
        fetch_funding_events_raw(
            rest,
            symbol=Symbol.BTCUSDT,
            start_time_ms=ANCHOR_MS,
            end_time_ms=ANCHOR_MS + 10 * EIGHT_HOURS_MS,
        )


def test_fetch_rejects_end_before_start() -> None:
    rest = _rest_client(httpx.MockTransport(lambda r: httpx.Response(200, json=[])))
    with pytest.raises(ValueError):
        fetch_funding_events_raw(rest, symbol=Symbol.BTCUSDT, start_time_ms=100, end_time_ms=50)


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def test_normalize_happy() -> None:
    raw = [_make_event(i) for i in range(3)]
    events = normalize_funding_events(raw, expected_symbol=Symbol.BTCUSDT, source="test")
    assert len(events) == 3
    assert events[0].symbol is Symbol.BTCUSDT
    assert events[0].funding_rate == 0.0001
    assert events[0].mark_price == 65000.0


def test_normalize_rejects_symbol_mismatch() -> None:
    raw = [_make_event(0, symbol="ETHUSDT")]
    with pytest.raises(DataIntegrityError):
        normalize_funding_events(raw, expected_symbol=Symbol.BTCUSDT, source="test")


def test_normalize_rejects_missing_field() -> None:
    raw: list[dict[str, Any]] = [{"symbol": "BTCUSDT", "fundingTime": 1, "fundingRate": "0.0001"}]
    with pytest.raises(DataIntegrityError):
        normalize_funding_events(raw, expected_symbol=Symbol.BTCUSDT, source="test")


def test_normalize_rejects_extreme_rate() -> None:
    raw = [
        {
            "symbol": "BTCUSDT",
            "fundingTime": 1,
            "fundingRate": "1.5",
            "markPrice": "65000.0",
        }
    ]
    with pytest.raises(DataIntegrityError):
        normalize_funding_events(raw, expected_symbol=Symbol.BTCUSDT, source="test")


def test_normalize_rejects_zero_mark_price() -> None:
    raw = [
        {
            "symbol": "BTCUSDT",
            "fundingTime": 1,
            "fundingRate": "0.0001",
            "markPrice": "0",
        }
    ]
    with pytest.raises(DataIntegrityError):
        normalize_funding_events(raw, expected_symbol=Symbol.BTCUSDT, source="test")


def test_normalize_rejects_non_numeric_rate() -> None:
    raw = [
        {
            "symbol": "BTCUSDT",
            "fundingTime": 1,
            "fundingRate": "not-a-number",
            "markPrice": "65000.0",
        }
    ]
    with pytest.raises(DataIntegrityError):
        normalize_funding_events(raw, expected_symbol=Symbol.BTCUSDT, source="test")
