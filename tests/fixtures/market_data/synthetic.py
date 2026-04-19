"""Deterministic synthetic 15m kline fixtures for BTCUSDT and ETHUSDT.

Used by Phase 2 integration tests and optionally by operators running
the pipeline end-to-end against repeatable data. Not representative of
real market behavior - exists only to exercise pipeline correctness.
"""

from __future__ import annotations

import random
from collections.abc import Iterable
from typing import Any

from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol

FIFTEEN_MIN_MS = 15 * 60 * 1000

_SYMBOL_CONFIG: dict[Symbol, dict[str, float]] = {
    Symbol.BTCUSDT: {"start_price": 65000.0, "sigma": 80.0},
    Symbol.ETHUSDT: {"start_price": 3500.0, "sigma": 6.0},
}


def _seed_for(symbol: Symbol, version: str) -> int:
    return hash(f"{symbol.value}|{version}") & 0xFFFFFFFF


def synthetic_15m_rows(
    symbol: Symbol,
    interval: Interval,
    start_ms: int,
    end_ms: int,
    *,
    version: str = "v001",
) -> list[dict[str, Any]]:
    """Return a deterministic list of raw 15m kline rows in ``[start_ms, end_ms]``.

    The rows use the same schema as :func:`prometheus.research.data.normalize.normalize_rows`.
    Bounds must be 15m-aligned and ``interval`` must be ``Interval.I_15M``.
    """
    if interval is not Interval.I_15M:
        raise ValueError(f"synthetic_15m_rows only supports 15m, got {interval}")
    if start_ms % FIFTEEN_MIN_MS != 0 or end_ms % FIFTEEN_MIN_MS != 0:
        raise ValueError("start_ms and end_ms must be 15m-aligned")
    if end_ms < start_ms:
        raise ValueError("end_ms must be >= start_ms")

    config = _SYMBOL_CONFIG[symbol]
    rng = random.Random(_seed_for(symbol, version))

    rows: list[dict[str, Any]] = []
    price = config["start_price"]
    sigma = config["sigma"]
    open_time = start_ms
    while open_time <= end_ms:
        open_price = price
        close_price = max(1.0, open_price + rng.gauss(0.0, sigma))
        high_price = max(open_price, close_price) + abs(rng.gauss(0.0, sigma / 3.0))
        low_price = min(open_price, close_price) - abs(rng.gauss(0.0, sigma / 3.0))
        low_price = max(1.0, low_price)

        base_volume = abs(rng.gauss(10.0, 4.0)) + 0.1
        quote_volume = base_volume * ((high_price + low_price) / 2.0)
        trades = max(1, int(abs(rng.gauss(200.0, 60.0))))
        taker_base_fraction = min(1.0, max(0.0, rng.gauss(0.5, 0.1)))
        taker_base = base_volume * taker_base_fraction
        taker_quote = quote_volume * taker_base_fraction

        rows.append(
            {
                "open_time": open_time,
                "close_time": open_time + FIFTEEN_MIN_MS - 1,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": base_volume,
                "quote_asset_volume": quote_volume,
                "trade_count": trades,
                "taker_buy_base_volume": taker_base,
                "taker_buy_quote_volume": taker_quote,
            }
        )
        price = close_price
        open_time += FIFTEEN_MIN_MS
    return rows


def synthetic_15m_spec(
    symbol: Symbol,
    interval: Interval,
    start_ms: int,
    end_ms: int,
) -> Iterable[dict[str, Any]]:
    """Spec callable compatible with :class:`FixtureKlineSource`."""
    return synthetic_15m_rows(symbol, interval, start_ms, end_ms)
