"""Deterministic 15m → 1h bar derivation.

Emits a 1h bar only when all four constituent 15m bars are present and
aligned. Partial buckets are reported as invalid windows rather than
silently filled.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from prometheus.core.errors import DataIntegrityError
from prometheus.core.intervals import Interval
from prometheus.core.klines import NormalizedKline
from prometheus.core.time import close_time_for, floor_to_interval, is_aligned_open_time

from .manifests import InvalidWindow

_BARS_PER_HOUR = 4
_DERIVED_SOURCE = "derived:15m->1h"


def derive_1h_from_15m(
    klines_15m: Sequence[NormalizedKline],
) -> tuple[list[NormalizedKline], list[InvalidWindow]]:
    """Aggregate 15m bars into completed 1h bars.

    Returns ``(derived_1h_klines, invalid_windows)``. A 1h bar is emitted
    only for buckets where all four 15m bars are present; buckets with
    fewer than four bars are recorded as invalid windows and skipped.

    Raises :class:`DataIntegrityError` if any input bar is not 15m, is
    not interval-aligned, or mixes symbols.
    """
    if not klines_15m:
        return [], []

    symbols = {k.symbol for k in klines_15m}
    if len(symbols) != 1:
        raise DataIntegrityError(
            f"derive_1h_from_15m requires a single symbol, got {sorted(symbols)}"
        )
    symbol = next(iter(symbols))

    for kline in klines_15m:
        if kline.interval is not Interval.I_15M:
            raise DataIntegrityError(
                f"derive_1h_from_15m expects 15m bars, got {kline.interval.value}"
            )
        if not is_aligned_open_time(kline.open_time, Interval.I_15M):
            raise DataIntegrityError(f"open_time {kline.open_time} is not 15m-aligned")

    buckets: dict[int, list[NormalizedKline]] = defaultdict(list)
    for kline in klines_15m:
        bucket_open = floor_to_interval(kline.open_time, Interval.I_1H)
        buckets[bucket_open].append(kline)

    derived: list[NormalizedKline] = []
    invalid: list[InvalidWindow] = []

    for bucket_open in sorted(buckets.keys()):
        group = sorted(buckets[bucket_open], key=lambda k: k.open_time)
        if len(group) != _BARS_PER_HOUR:
            invalid.append(
                InvalidWindow(
                    start_open_time_ms=bucket_open,
                    end_open_time_ms=close_time_for(bucket_open, Interval.I_1H),
                    reason=f"partial_1h_bucket:{len(group)}_of_{_BARS_PER_HOUR}",
                )
            )
            continue

        expected_opens = [bucket_open + i * 15 * 60 * 1000 for i in range(_BARS_PER_HOUR)]
        if [k.open_time for k in group] != expected_opens:
            invalid.append(
                InvalidWindow(
                    start_open_time_ms=bucket_open,
                    end_open_time_ms=close_time_for(bucket_open, Interval.I_1H),
                    reason="misaligned_15m_bars_in_1h_bucket",
                )
            )
            continue

        first = group[0]
        last = group[-1]
        derived.append(
            NormalizedKline(
                symbol=symbol,
                interval=Interval.I_1H,
                open_time=bucket_open,
                close_time=close_time_for(bucket_open, Interval.I_1H),
                open=first.open,
                high=max(k.high for k in group),
                low=min(k.low for k in group),
                close=last.close,
                volume=sum(k.volume for k in group),
                quote_asset_volume=sum(k.quote_asset_volume for k in group),
                trade_count=sum(k.trade_count for k in group),
                taker_buy_base_volume=sum(k.taker_buy_base_volume for k in group),
                taker_buy_quote_volume=sum(k.taker_buy_quote_volume for k in group),
                source=_DERIVED_SOURCE,
            )
        )
    return derived, invalid
