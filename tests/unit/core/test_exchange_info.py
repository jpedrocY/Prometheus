from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from prometheus.core.exchange_info import (
    ExchangeInfoSnapshot,
    LotSizeFilter,
    MinNotionalFilter,
    PriceFilter,
    SymbolInfo,
)


def _price_filter() -> PriceFilter:
    return PriceFilter(
        filterType="PRICE_FILTER", minPrice="0.10", maxPrice="1000000.00", tickSize="0.10"
    )


def _lot_filter() -> LotSizeFilter:
    return LotSizeFilter(filterType="LOT_SIZE", minQty="0.001", maxQty="1000.000", stepSize="0.001")


def _min_notional() -> MinNotionalFilter:
    return MinNotionalFilter(filterType="MIN_NOTIONAL", notional="5")


def _symbol_info(**overrides: Any) -> SymbolInfo:
    base: dict[str, Any] = {
        "symbol": "BTCUSDT",
        "pair": "BTCUSDT",
        "contractType": "PERPETUAL",
        "status": "TRADING",
        "baseAsset": "BTC",
        "quoteAsset": "USDT",
        "pricePrecision": 2,
        "quantityPrecision": 3,
        "price_filter": _price_filter(),
        "lot_size_filter": _lot_filter(),
        "min_notional_filter": _min_notional(),
    }
    base.update(overrides)
    return SymbolInfo(**base)


def _snapshot_kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "canonical_timezone": "UTC",
        "canonical_timestamp_format": "unix_milliseconds",
        "server_time_ms": 1_774_224_000_000,
        "server_timezone": "UTC",
        "snapshot_fetched_at_utc_ms": 1_774_224_000_100,
        "source_url": "https://fapi.binance.com/fapi/v1/exchangeInfo",
        "response_sha256": "a" * 64,
        "symbols": (_symbol_info(),),
    }
    base.update(overrides)
    return base


def test_valid_snapshot_accepts() -> None:
    snap = ExchangeInfoSnapshot(**_snapshot_kwargs())
    assert snap.canonical_timezone == "UTC"
    assert len(snap.symbols) == 1
    assert snap.symbols[0].symbol == "BTCUSDT"


def test_snapshot_frozen() -> None:
    snap = ExchangeInfoSnapshot(**_snapshot_kwargs())
    with pytest.raises(ValidationError):
        snap.server_time_ms = 0  # type: ignore[misc]


def test_snapshot_extra_forbid() -> None:
    with pytest.raises(ValidationError):
        ExchangeInfoSnapshot(**_snapshot_kwargs(), surprise="no")


def test_symbol_info_extra_ignore() -> None:
    # SymbolInfo allows ignoring upstream fields Binance may add.
    info = SymbolInfo(
        symbol="BTCUSDT",
        pair="BTCUSDT",
        contractType="PERPETUAL",
        status="TRADING",
        baseAsset="BTC",
        quoteAsset="USDT",
        pricePrecision=2,
        quantityPrecision=3,
        deliveryDate=9_999_999_999_999,  # upstream field not modelled
    )
    assert info.symbol == "BTCUSDT"


def test_snapshot_list_of_symbols_accepted_via_tuple_coercion() -> None:
    snap = ExchangeInfoSnapshot(**_snapshot_kwargs(symbols=[_symbol_info()]))
    assert isinstance(snap.symbols, tuple)


def test_snapshot_response_sha256_length_validated() -> None:
    with pytest.raises(ValidationError):
        ExchangeInfoSnapshot(**_snapshot_kwargs(response_sha256="short"))


def test_filter_types_strict() -> None:
    with pytest.raises(ValidationError):
        PriceFilter(filterType="WRONG", minPrice="0.1", maxPrice="1.0", tickSize="0.1")


def test_price_filter_frozen() -> None:
    pf = _price_filter()
    with pytest.raises(ValidationError):
        pf.tickSize = "0.01"  # type: ignore[misc]
