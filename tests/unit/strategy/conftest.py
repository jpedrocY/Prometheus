"""Shared helpers for strategy unit tests.

Offers small factory functions that produce valid NormalizedKline /
MarkPriceKline / FundingRateEvent objects with minimal boilerplate,
so individual tests can focus on the scenario they want to exercise
rather than on keyword-argument plumbing.
"""

from __future__ import annotations

from collections.abc import Iterable

from prometheus.core.events import FundingRateEvent
from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline
from prometheus.core.mark_price_klines import MarkPriceKline
from prometheus.core.symbols import Symbol
from prometheus.core.time import close_time_for

# A small, obviously-synthetic anchor in UTC ms (2026-03-01 00:00:00 UTC).
ANCHOR_MS = 1_772_582_400_000


def kline(
    *,
    symbol: Symbol = Symbol.BTCUSDT,
    interval: Interval = Interval.I_15M,
    open_time: int,
    open: float,
    high: float | None = None,
    low: float | None = None,
    close: float,
    volume: float = 1.0,
    quote_asset_volume: float | None = None,
    trade_count: int = 1,
    taker_buy_base_volume: float = 0.5,
    taker_buy_quote_volume: float | None = None,
    source: str = "synthetic-test",
) -> NormalizedKline:
    hi = high if high is not None else max(open, close)
    lo = low if low is not None else min(open, close)
    qav = quote_asset_volume if quote_asset_volume is not None else volume * close
    tbqv = (
        taker_buy_quote_volume
        if taker_buy_quote_volume is not None
        else taker_buy_base_volume * close
    )
    return NormalizedKline(
        symbol=symbol,
        interval=interval,
        open_time=open_time,
        close_time=close_time_for(open_time, interval),
        open=open,
        high=hi,
        low=lo,
        close=close,
        volume=volume,
        quote_asset_volume=qav,
        trade_count=trade_count,
        taker_buy_base_volume=taker_buy_base_volume,
        taker_buy_quote_volume=tbqv,
        source=source,
    )


def mark(
    *,
    symbol: Symbol = Symbol.BTCUSDT,
    interval: Interval = Interval.I_15M,
    open_time: int,
    open: float,
    high: float | None = None,
    low: float | None = None,
    close: float,
    source: str = "synthetic-test",
) -> MarkPriceKline:
    hi = high if high is not None else max(open, close)
    lo = low if low is not None else min(open, close)
    return MarkPriceKline(
        symbol=symbol,
        interval=interval,
        open_time=open_time,
        close_time=close_time_for(open_time, interval),
        open=open,
        high=hi,
        low=lo,
        close=close,
        source=source,
    )


def funding(
    *,
    symbol: Symbol = Symbol.BTCUSDT,
    funding_time: int,
    funding_rate: float,
    mark_price: float = 50_000.0,
    source: str = "synthetic-test",
) -> FundingRateEvent:
    return FundingRateEvent(
        symbol=symbol,
        funding_time=funding_time,
        funding_rate=funding_rate,
        mark_price=mark_price,
        source=source,
    )


def linear_15m_series(
    *,
    n: int,
    start_price: float,
    step: float,
    start_open_time: int = ANCHOR_MS,
    symbol: Symbol = Symbol.BTCUSDT,
) -> list[NormalizedKline]:
    """A deterministic linear ramp of 15m bars for indicator-correctness tests."""
    bars: list[NormalizedKline] = []
    t = start_open_time
    d = interval_duration_ms(Interval.I_15M)
    price = start_price
    for _ in range(n):
        nxt = price + step
        bars.append(
            kline(
                symbol=symbol,
                interval=Interval.I_15M,
                open_time=t,
                open=price,
                high=max(price, nxt),
                low=min(price, nxt),
                close=nxt,
            )
        )
        t += d
        price = nxt
    return bars


def hours_of_flat_1h(
    *,
    n: int,
    price: float,
    start_open_time: int = ANCHOR_MS,
    symbol: Symbol = Symbol.BTCUSDT,
) -> list[NormalizedKline]:
    bars: list[NormalizedKline] = []
    t = start_open_time
    d = interval_duration_ms(Interval.I_1H)
    for _ in range(n):
        bars.append(
            kline(
                symbol=symbol,
                interval=Interval.I_1H,
                open_time=t,
                open=price,
                high=price * 1.001,
                low=price * 0.999,
                close=price,
            )
        )
        t += d
    return bars


def ramping_1h_series(
    *,
    n: int,
    start_price: float,
    per_hour_return: float,
    start_open_time: int = ANCHOR_MS,
    symbol: Symbol = Symbol.BTCUSDT,
) -> list[NormalizedKline]:
    """A 1h series with geometric per-hour return. Rising if return > 0."""
    bars: list[NormalizedKline] = []
    t = start_open_time
    d = interval_duration_ms(Interval.I_1H)
    price = start_price
    for _ in range(n):
        nxt = price * (1.0 + per_hour_return)
        bars.append(
            kline(
                symbol=symbol,
                interval=Interval.I_1H,
                open_time=t,
                open=price,
                high=max(price, nxt) * 1.0005,
                low=min(price, nxt) * 0.9995,
                close=nxt,
            )
        )
        t += d
        price = nxt
    return bars


def collect(series: Iterable[NormalizedKline]) -> list[NormalizedKline]:
    return list(series)
