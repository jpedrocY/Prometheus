"""Funding-rate history REST source.

## TD-006 verification evidence (2026-04-19)

Verified via WebFetch of the official Binance developer docs page
``https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History``:

1. Method + path: ``GET /fapi/v1/fundingRate`` at ``https://fapi.binance.com``.
2. Public endpoint: no authentication, no X-MBX-APIKEY, no signed request.
3. Parameters (case-sensitive):
     * ``symbol`` (STRING, optional)
     * ``startTime`` (LONG, optional) — "Timestamp in ms to get funding rate from INCLUSIVE."
     * ``endTime`` (LONG, optional) — "Timestamp in ms to get funding rate until INCLUSIVE."
     * ``limit`` (INT, default 100, max 1000)
4. Response: array of objects each having EXACT fields:
     * ``symbol`` (STRING)
     * ``fundingRate`` (STRING, decimal format)
     * ``fundingTime`` (LONG, millisecond timestamp)
     * ``markPrice`` (STRING, decimal format)
5. Rate limit (verbatim quote):
     "share 500/5min/IP rate limit with GET /fapi/v1/fundingInfo"
6. Pagination (verbatim quote):
     "If ``startTime`` and ``endTime`` are not sent, the most recent 200
      records are returned. If the number of data between ``startTime``
      and ``endTime`` is larger than ``limit``, return as
      ``startTime + limit``. In ascending order."

Pacing chosen for the BinanceRestClient used here: 1000 ms between
requests (500/5min = 100/min = 1.67/s peak; 1000 ms leaves a 40% margin).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pydantic import ValidationError

from prometheus.core.errors import DataIntegrityError
from prometheus.core.events import FundingRateEvent
from prometheus.core.symbols import Symbol

from .binance_rest import BinanceRestClient

_ENDPOINT = "/fapi/v1/fundingRate"
_MAX_LIMIT = 1000
_SAFETY_PAGE_CAP = 100  # circuit breaker; real months have ~93 events per symbol


def fetch_funding_events_raw(
    rest: BinanceRestClient,
    *,
    symbol: Symbol,
    start_time_ms: int,
    end_time_ms: int,
) -> list[dict[str, Any]]:
    """Fetch raw funding-rate events from /fapi/v1/fundingRate with pagination.

    Returns the raw Binance response objects (not yet normalized to
    :class:`FundingRateEvent`) spanning ``[start_time_ms, end_time_ms]``
    inclusive for ``symbol``. Pagination advances ``startTime`` past the
    last returned ``fundingTime``; terminates on empty or short pages.
    A hard safety cap (``_SAFETY_PAGE_CAP``) prevents runaway loops.
    """
    if end_time_ms < start_time_ms:
        raise ValueError("end_time_ms must be >= start_time_ms")

    collected: list[dict[str, Any]] = []
    cursor_start_ms = start_time_ms
    for _ in range(_SAFETY_PAGE_CAP):
        page = rest.get_json(
            _ENDPOINT,
            params={
                "symbol": symbol.value,
                "startTime": cursor_start_ms,
                "endTime": end_time_ms,
                "limit": _MAX_LIMIT,
            },
        )
        if not isinstance(page, list):
            raise DataIntegrityError(
                f"expected JSON array from {_ENDPOINT}, got {type(page).__name__}"
            )
        if not page:
            break

        collected.extend(page)

        if len(page) < _MAX_LIMIT:
            break

        last_event = page[-1]
        if "fundingTime" not in last_event:
            raise DataIntegrityError(
                f"event missing fundingTime field: keys={list(last_event.keys())}"
            )
        next_cursor = int(last_event["fundingTime"]) + 1
        if next_cursor <= cursor_start_ms:
            raise DataIntegrityError(
                "pagination cursor did not advance; aborting to prevent infinite loop"
            )
        cursor_start_ms = next_cursor
    else:
        raise DataIntegrityError(
            f"pagination exceeded safety cap of {_SAFETY_PAGE_CAP} pages for "
            f"{symbol.value} in [{start_time_ms}, {end_time_ms}]"
        )

    return collected


def normalize_funding_events(
    raw_events: Sequence[dict[str, Any]],
    *,
    expected_symbol: Symbol,
    source: str,
) -> list[FundingRateEvent]:
    """Convert raw Binance funding-rate JSON objects into typed events.

    Binance returns ``fundingRate`` as a string-decimal; this function
    parses it as ``float``. A mismatched ``symbol`` raises
    :class:`DataIntegrityError`.

    ``markPrice`` handling per GAP-20260420-029:
      - Empty string ``""`` -> ``mark_price = None`` (Binance does not
        populate markPrice for pre-2024 funding events).
      - Missing key (``None``) -> ``mark_price = None``.
      - Numeric-looking string -> parsed as float; must be strictly
        positive (the model enforces this on construction).
      - Malformed non-empty markPrice -> ``DataIntegrityError``.
    """
    result: list[FundingRateEvent] = []
    for index, raw in enumerate(raw_events):
        # Per GAP-20260420-029: markPrice may be present but empty.
        # It is still a required KEY in the upstream schema, so a
        # missing key is treated as malformed. Empty string is valid.
        missing = {"symbol", "fundingTime", "fundingRate", "markPrice"} - raw.keys()
        if missing:
            raise DataIntegrityError(f"funding event {index} missing fields {sorted(missing)}")
        if raw["symbol"] != expected_symbol.value:
            raise DataIntegrityError(
                f"funding event {index} symbol {raw['symbol']!r} != "
                f"expected {expected_symbol.value!r}"
            )
        try:
            funding_rate = float(raw["fundingRate"])
            funding_time = int(raw["fundingTime"])
        except (TypeError, ValueError) as exc:
            raise DataIntegrityError(f"funding event {index} numeric cast failed: {exc}") from exc

        raw_mark_price = raw["markPrice"]
        mark_price: float | None
        if raw_mark_price is None or raw_mark_price == "":
            # Upstream absence. Do not coerce to 0.0; do not derive.
            mark_price = None
        else:
            try:
                mark_price = float(raw_mark_price)
            except (TypeError, ValueError) as exc:
                raise DataIntegrityError(
                    f"funding event {index} markPrice cast failed: {exc}"
                ) from exc

        try:
            event = FundingRateEvent(
                symbol=expected_symbol,
                funding_time=funding_time,
                funding_rate=funding_rate,
                mark_price=mark_price,
                source=source,
            )
        except ValidationError as exc:
            raise DataIntegrityError(
                f"funding event {index} model validation failed: {exc.errors()}"
            ) from exc
        result.append(event)
    return result
