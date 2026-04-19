"""ExchangeInfo REST snapshot source.

## TD-006 verification evidence (2026-04-19)

Verified via WebFetch of the official Binance developer docs page
``https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information``:

1. Method + path: ``GET /fapi/v1/exchangeInfo`` at ``https://fapi.binance.com``.
2. Public endpoint: no authentication, no parameters.
3. Request weight: 1.
4. Top-level response fields (verbatim from docs):
     ``timezone``, ``serverTime``, ``rateLimits``, ``exchangeFilters``,
     ``assets``, ``symbols``.
5. Per-symbol fields (24 documented; only a subset modelled here):
     ``symbol``, ``pair``, ``contractType``, ``deliveryDate``,
     ``onboardDate``, ``status``, ``maintMarginPercent``,
     ``requiredMarginPercent``, ``baseAsset``, ``quoteAsset``,
     ``marginAsset``, ``pricePrecision``, ``quantityPrecision``,
     ``baseAssetPrecision``, ``quotePrecision``, ``underlyingType``,
     ``underlyingSubType``, ``settlePlan``, ``triggerProtect``,
     ``filters``, ``orderTypes``, ``timeInForce``,
     ``liquidationFee``, ``marketTakeBound``.
6. Filter types documented:
     ``PRICE_FILTER`` (minPrice, maxPrice, tickSize),
     ``LOT_SIZE`` (minQty, maxQty, stepSize),
     ``MARKET_LOT_SIZE`` (minQty, maxQty, stepSize),
     ``MAX_NUM_ORDERS`` (limit),
     ``MIN_NOTIONAL`` (notional),
     ``PERCENT_PRICE`` (multiplierUp, multiplierDown, multiplierDecimal).

This module extracts only the symbols named in the caller's
``interested_symbols`` set and materializes a
:class:`ExchangeInfoSnapshot` with typed filters. The raw JSON body is
persisted verbatim alongside the derived snapshot (see
:func:`fetch_exchange_info_snapshot`).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from prometheus.core.errors import DataIntegrityError
from prometheus.core.exchange_info import (
    ExchangeInfoSnapshot,
    LotSizeFilter,
    MarketLotSizeFilter,
    MinNotionalFilter,
    PriceFilter,
    SymbolInfo,
)
from prometheus.core.symbols import Symbol
from prometheus.core.time import utc_now_ms

from .binance_rest import BinanceRestClient

_ENDPOINT = "/fapi/v1/exchangeInfo"


def _build_symbol_info(raw: dict[str, Any]) -> SymbolInfo:
    filters_raw = raw.get("filters") or []
    price_filter: PriceFilter | None = None
    lot_size_filter: LotSizeFilter | None = None
    market_lot_size_filter: MarketLotSizeFilter | None = None
    min_notional_filter: MinNotionalFilter | None = None

    for filt in filters_raw:
        filter_type = filt.get("filterType")
        if filter_type == "PRICE_FILTER":
            price_filter = PriceFilter.model_validate(filt)
        elif filter_type == "LOT_SIZE":
            lot_size_filter = LotSizeFilter.model_validate(filt)
        elif filter_type == "MARKET_LOT_SIZE":
            market_lot_size_filter = MarketLotSizeFilter.model_validate(filt)
        elif filter_type == "MIN_NOTIONAL":
            min_notional_filter = MinNotionalFilter.model_validate(filt)

    try:
        return SymbolInfo.model_validate(
            {
                "symbol": raw["symbol"],
                "pair": raw.get("pair", raw["symbol"]),
                "contractType": raw["contractType"],
                "status": raw["status"],
                "baseAsset": raw["baseAsset"],
                "quoteAsset": raw["quoteAsset"],
                "pricePrecision": raw["pricePrecision"],
                "quantityPrecision": raw["quantityPrecision"],
                "price_filter": price_filter,
                "lot_size_filter": lot_size_filter,
                "market_lot_size_filter": market_lot_size_filter,
                "min_notional_filter": min_notional_filter,
            }
        )
    except ValidationError as exc:
        raise DataIntegrityError(
            f"exchangeInfo symbol {raw.get('symbol', '<?>')} validation failed: {exc.errors()}"
        ) from exc


def parse_exchange_info(
    raw_body: dict[str, Any],
    *,
    source_url: str,
    response_sha256: str,
    interested_symbols: frozenset[Symbol],
    now_ms: int | None = None,
) -> ExchangeInfoSnapshot:
    """Parse a raw ``/fapi/v1/exchangeInfo`` response into a snapshot.

    Filters the ``symbols`` list to only the ``interested_symbols``.
    Raises :class:`DataIntegrityError` if any required interested symbol
    is missing from the response, or if top-level fields are malformed.
    """
    for required in ("timezone", "serverTime", "symbols"):
        if required not in raw_body:
            raise DataIntegrityError(f"exchangeInfo response missing required field {required!r}")

    server_time_ms = raw_body["serverTime"]
    if not isinstance(server_time_ms, int):
        raise DataIntegrityError(
            f"exchangeInfo serverTime must be int, got {type(server_time_ms).__name__}"
        )

    interested_str = {s.value for s in interested_symbols}
    matched: list[SymbolInfo] = []
    for raw_symbol in raw_body["symbols"]:
        if not isinstance(raw_symbol, dict):
            raise DataIntegrityError(
                f"exchangeInfo symbols entry not dict: {type(raw_symbol).__name__}"
            )
        if raw_symbol.get("symbol") in interested_str:
            matched.append(_build_symbol_info(raw_symbol))

    found_names = {s.symbol for s in matched}
    missing = interested_str - found_names
    if missing:
        raise DataIntegrityError(
            f"exchangeInfo response missing required symbols {sorted(missing)}"
        )

    return ExchangeInfoSnapshot(
        canonical_timezone="UTC",
        canonical_timestamp_format="unix_milliseconds",
        server_time_ms=server_time_ms,
        server_timezone=raw_body["timezone"],
        snapshot_fetched_at_utc_ms=now_ms if now_ms is not None else utc_now_ms(),
        source_url=source_url,
        response_sha256=response_sha256,
        symbols=tuple(matched),
    )


def fetch_exchange_info_snapshot(
    rest: BinanceRestClient,
    *,
    interested_symbols: frozenset[Symbol],
    raw_root: Path,
) -> tuple[ExchangeInfoSnapshot, Path, Path]:
    """Fetch the live exchangeInfo, persist raw + parsed, return summary.

    Writes the raw JSON bytes verbatim to
    ``<raw_root>/binance_usdm/exchange_info/<ISO-timestamp>.json`` and
    a derived summary JSON to
    ``<raw_root>/../derived/exchange_info/<ISO-timestamp>.json`` (via
    path calculation). Returns the parsed snapshot plus both file paths.
    """
    import datetime as dt

    source_url = f"{rest.base_url}{_ENDPOINT}"
    # Raw persistence path (timestamped for idempotency across runs).
    now_utc = dt.datetime.now(tz=dt.UTC).replace(microsecond=0)
    iso_tag = now_utc.strftime("%Y-%m-%dT%H-%M-%SZ")
    raw_dir = raw_root / "binance_usdm" / "exchange_info"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"{iso_tag}.json"

    parsed, sha = rest.save_raw_response(_ENDPOINT, params=None, dest_path=raw_path)
    if not isinstance(parsed, dict):
        raise DataIntegrityError(
            f"expected JSON object from {_ENDPOINT}, got {type(parsed).__name__}"
        )

    snapshot = parse_exchange_info(
        parsed,
        source_url=source_url,
        response_sha256=sha,
        interested_symbols=interested_symbols,
    )

    # Derived summary beside raw data, so operators can locate the
    # trimmed view without crawling the full JSON.
    derived_dir = raw_root.parent / "derived" / "exchange_info"
    derived_dir.mkdir(parents=True, exist_ok=True)
    derived_path = derived_dir / f"{iso_tag}.json"
    derived_path.write_text(
        json.dumps(snapshot.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return snapshot, raw_path, derived_path
