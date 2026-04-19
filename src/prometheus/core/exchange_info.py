"""ExchangeInfo snapshot models.

Represents a point-in-time snapshot of Binance USD-M futures exchange
metadata, filtered down to the fields Prometheus consumes for order
rounding, minimum-notional checks, and price-precision validation.

The raw Binance JSON contains many fields we do not use (per-symbol
``maintMarginPercent``, ``onboardDate``, ``deliveryDate``, etc.). We
parse only the fields we need and set ``extra="ignore"`` so future
additions on Binance's side don't break parsing. The raw JSON is also
persisted verbatim alongside the derived snapshot so nothing is lost.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


def _as_tuple(value: object) -> object:
    if isinstance(value, list):
        return tuple(value)
    return value


class PriceFilter(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="ignore")

    filterType: Literal["PRICE_FILTER"]
    minPrice: str
    maxPrice: str
    tickSize: str


class LotSizeFilter(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="ignore")

    filterType: Literal["LOT_SIZE"]
    minQty: str
    maxQty: str
    stepSize: str


class MarketLotSizeFilter(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="ignore")

    filterType: Literal["MARKET_LOT_SIZE"]
    minQty: str
    maxQty: str
    stepSize: str


class MinNotionalFilter(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="ignore")

    filterType: Literal["MIN_NOTIONAL"]
    notional: str


class SymbolInfo(BaseModel):
    """Per-symbol metadata extracted from /fapi/v1/exchangeInfo.

    Only the fields Prometheus consumes downstream are modelled. The
    raw upstream response carries ~24 fields per symbol; ``extra="ignore"``
    keeps parsing resilient to Binance adding new fields. The filters
    list retains order from the upstream response.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="ignore")

    symbol: str = Field(min_length=1)
    pair: str = Field(min_length=1)
    contractType: str
    status: str
    baseAsset: str
    quoteAsset: str
    pricePrecision: int
    quantityPrecision: int

    price_filter: PriceFilter | None = None
    lot_size_filter: LotSizeFilter | None = None
    market_lot_size_filter: MarketLotSizeFilter | None = None
    min_notional_filter: MinNotionalFilter | None = None


class ExchangeInfoSnapshot(BaseModel):
    """Full snapshot of /fapi/v1/exchangeInfo for a subset of symbols.

    The top-level ``server_time_ms`` is the exchange's authoritative
    clock; ``snapshot_fetched_at_utc_ms`` is the operator's local fetch
    timestamp.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    canonical_timezone: Literal["UTC"]
    canonical_timestamp_format: Literal["unix_milliseconds"]
    server_time_ms: int
    server_timezone: str
    snapshot_fetched_at_utc_ms: int
    source_url: str = Field(min_length=1)
    response_sha256: str = Field(min_length=64, max_length=64)
    symbols: Annotated[tuple[SymbolInfo, ...], BeforeValidator(_as_tuple)]
