"""Historical kline source protocol and fixture-based implementation.

Phase 2 deliberately ships NO network-facing source. ``HistoricalKlineSource``
is a :class:`typing.Protocol` so later phases can add real fetchers (e.g.,
Binance bulk-download or REST) behind the same interface without altering
callers. The only concrete implementation here is :class:`FixtureKlineSource`,
which returns pre-computed rows from an in-memory spec.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, Protocol, TypeAlias, runtime_checkable

from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol

RawKlineRow: TypeAlias = dict[str, Any]


@runtime_checkable
class HistoricalKlineSource(Protocol):
    """Read-only kline source returning rows for later normalization.

    Returned rows must contain, at minimum, the keys consumed by
    :func:`prometheus.research.data.normalize.normalize_rows`::
        open_time, close_time, open, high, low, close, volume,
        quote_asset_volume, trade_count, taker_buy_base_volume,
        taker_buy_quote_volume
    """

    def fetch(
        self,
        *,
        symbol: Symbol,
        interval: Interval,
        start_ms: int,
        end_ms: int,
    ) -> Iterable[RawKlineRow]: ...


FixtureSpecFn = Callable[[Symbol, Interval, int, int], Iterable[RawKlineRow]]


class FixtureKlineSource:
    """In-memory fixture source used by tests and by Phase 2 integration code.

    Wraps a deterministic spec function. No network calls, no file I/O.
    """

    def __init__(self, spec: FixtureSpecFn) -> None:
        self._spec = spec

    def fetch(
        self,
        *,
        symbol: Symbol,
        interval: Interval,
        start_ms: int,
        end_ms: int,
    ) -> Iterable[RawKlineRow]:
        return self._spec(symbol, interval, start_ms, end_ms)
