"""Normalize raw kline rows into validated :class:`NormalizedKline` values."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from pydantic import ValidationError

from prometheus.core.errors import DataIntegrityError
from prometheus.core.intervals import Interval
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol


def normalize_rows(
    raw_rows: Iterable[dict[str, Any]],
    *,
    symbol: Symbol,
    interval: Interval,
    source: str,
) -> list[NormalizedKline]:
    """Validate and construct :class:`NormalizedKline` values from raw rows.

    The caller supplies ``symbol``, ``interval``, and ``source`` so the
    raw rows do not need to carry them. Any validation failure — for a
    single row — raises :class:`DataIntegrityError` with the originating
    Pydantic diagnostic and the offending row index.
    """
    result: list[NormalizedKline] = []
    for index, row in enumerate(raw_rows):
        payload = {
            "symbol": symbol,
            "interval": interval,
            "source": source,
            "open_time": row["open_time"],
            "close_time": row["close_time"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row["volume"],
            "quote_asset_volume": row["quote_asset_volume"],
            "trade_count": row["trade_count"],
            "taker_buy_base_volume": row["taker_buy_base_volume"],
            "taker_buy_quote_volume": row["taker_buy_quote_volume"],
        }
        try:
            kline = NormalizedKline.model_validate(payload)
        except ValidationError as exc:
            raise DataIntegrityError(f"row {index} failed validation: {exc.errors()}") from exc
        result.append(kline)
    return result
