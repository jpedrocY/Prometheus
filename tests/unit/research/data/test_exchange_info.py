from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Any

import httpx
import pytest

from prometheus.core.errors import DataIntegrityError
from prometheus.core.symbols import Symbol
from prometheus.research.data.binance_rest import BinanceRestClient
from prometheus.research.data.exchange_info import (
    fetch_exchange_info_snapshot,
    parse_exchange_info,
)


def _raw_symbol(symbol: str) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "pair": symbol,
        "contractType": "PERPETUAL",
        "status": "TRADING",
        "baseAsset": symbol.replace("USDT", ""),
        "quoteAsset": "USDT",
        "pricePrecision": 2,
        "quantityPrecision": 3,
        # Extra fields Binance returns that we don't model:
        "deliveryDate": 4_102_444_800_000,
        "onboardDate": 1_569_398_400_000,
        "filters": [
            {
                "filterType": "PRICE_FILTER",
                "minPrice": "0.10",
                "maxPrice": "1000000.00",
                "tickSize": "0.10",
            },
            {
                "filterType": "LOT_SIZE",
                "minQty": "0.001",
                "maxQty": "1000.000",
                "stepSize": "0.001",
            },
            {
                "filterType": "MIN_NOTIONAL",
                "notional": "5",
            },
        ],
    }


def _raw_body(symbols: list[str] | None = None) -> dict[str, Any]:
    if symbols is None:
        symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
    return {
        "timezone": "UTC",
        "serverTime": 1_774_224_000_000,
        "rateLimits": [],
        "exchangeFilters": [],
        "assets": [],
        "symbols": [_raw_symbol(s) for s in symbols],
    }


# ---------------------------------------------------------------------------
# parse_exchange_info
# ---------------------------------------------------------------------------


def test_parse_happy_filters_to_interested() -> None:
    body = _raw_body()
    snap = parse_exchange_info(
        body,
        source_url="https://fapi.binance.com/fapi/v1/exchangeInfo",
        response_sha256="a" * 64,
        interested_symbols=frozenset({Symbol.BTCUSDT, Symbol.ETHUSDT}),
        now_ms=1_774_224_000_100,
    )
    assert len(snap.symbols) == 2
    names = {s.symbol for s in snap.symbols}
    assert names == {"BTCUSDT", "ETHUSDT"}
    assert snap.server_time_ms == 1_774_224_000_000


def test_parse_extracts_filters() -> None:
    body = _raw_body(["BTCUSDT"])
    snap = parse_exchange_info(
        body,
        source_url="https://fapi.binance.com/fapi/v1/exchangeInfo",
        response_sha256="b" * 64,
        interested_symbols=frozenset({Symbol.BTCUSDT}),
        now_ms=1,
    )
    btc = snap.symbols[0]
    assert btc.price_filter is not None
    assert btc.price_filter.tickSize == "0.10"
    assert btc.lot_size_filter is not None
    assert btc.lot_size_filter.stepSize == "0.001"
    assert btc.min_notional_filter is not None
    assert btc.min_notional_filter.notional == "5"


def test_parse_missing_required_symbol_raises() -> None:
    body = _raw_body(["BTCUSDT"])
    with pytest.raises(DataIntegrityError) as exc_info:
        parse_exchange_info(
            body,
            source_url="https://fapi.binance.com/fapi/v1/exchangeInfo",
            response_sha256="c" * 64,
            interested_symbols=frozenset({Symbol.BTCUSDT, Symbol.ETHUSDT}),
            now_ms=1,
        )
    assert "ETHUSDT" in str(exc_info.value)


def test_parse_missing_top_level_field_raises() -> None:
    body = _raw_body()
    body.pop("serverTime")
    with pytest.raises(DataIntegrityError):
        parse_exchange_info(
            body,
            source_url="https://fapi.binance.com/fapi/v1/exchangeInfo",
            response_sha256="d" * 64,
            interested_symbols=frozenset({Symbol.BTCUSDT}),
            now_ms=1,
        )


def test_parse_server_time_wrong_type_raises() -> None:
    body = _raw_body()
    body["serverTime"] = "not-a-number"
    with pytest.raises(DataIntegrityError):
        parse_exchange_info(
            body,
            source_url="https://fapi.binance.com/fapi/v1/exchangeInfo",
            response_sha256="e" * 64,
            interested_symbols=frozenset({Symbol.BTCUSDT}),
            now_ms=1,
        )


def test_parse_ignores_unmodeled_per_symbol_fields() -> None:
    body = _raw_body(["BTCUSDT"])
    # deliveryDate, onboardDate are in the raw but not in SymbolInfo's model.
    snap = parse_exchange_info(
        body,
        source_url="https://fapi.binance.com/fapi/v1/exchangeInfo",
        response_sha256="f" * 64,
        interested_symbols=frozenset({Symbol.BTCUSDT}),
        now_ms=1,
    )
    assert snap.symbols[0].symbol == "BTCUSDT"


# ---------------------------------------------------------------------------
# fetch_exchange_info_snapshot (writes raw + derived + returns parsed)
# ---------------------------------------------------------------------------


def test_fetch_writes_raw_and_derived(tmp_path: Path) -> None:
    body = _raw_body(["BTCUSDT", "ETHUSDT"])
    body_bytes = json.dumps(body).encode("utf-8")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=body_bytes,
            headers={"Content-Type": "application/json"},
        )

    rest = BinanceRestClient(
        httpx.Client(transport=httpx.MockTransport(handler)),
        pace_ms=0,
        sleep=lambda _: None,
        rng=random.Random(0),
    )
    raw_root = tmp_path / "data" / "raw"

    snap, raw_path, derived_path = fetch_exchange_info_snapshot(
        rest,
        interested_symbols=frozenset({Symbol.BTCUSDT, Symbol.ETHUSDT}),
        raw_root=raw_root,
    )
    assert len(snap.symbols) == 2
    assert raw_path.is_file()
    assert derived_path.is_file()
    # Raw body matches the byte-for-byte response.
    assert raw_path.read_bytes() == body_bytes
    # SHA256 recorded in the snapshot equals the on-disk bytes' SHA256.
    assert snap.response_sha256 == hashlib.sha256(body_bytes).hexdigest()
    # Derived JSON is human-readable (pretty printed).
    derived_text = derived_path.read_text(encoding="utf-8")
    assert derived_text.endswith("\n")
    assert "symbols" in derived_text
