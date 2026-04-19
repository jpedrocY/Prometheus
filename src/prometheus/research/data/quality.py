"""Data-integrity checks for normalized kline datasets.

Each check returns a structured result rather than raising. Callers
decide whether a non-empty result is a hard failure (fixture tests) or a
soft flag to be recorded in the dataset manifest's ``invalid_windows``.

``NormalizedKline`` construction already enforces OHLC sanity, volume
non-negativity, interval alignment, and close_time correctness; those
invariants are not re-checked here.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict

from prometheus.core.events import FundingRateEvent
from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline


class DuplicateReport(BaseModel):
    """A bar identity seen more than once in a single input set."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: str
    interval: str
    open_time: int
    count: int


class MissingWindow(BaseModel):
    """A contiguous range of expected-but-absent bars."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    start_open_time_ms: int
    end_open_time_ms: int
    missing_count: int


def check_no_duplicates(klines: Sequence[NormalizedKline]) -> list[DuplicateReport]:
    """Return duplicate bar identities ``(symbol, interval, open_time)``."""
    counts: dict[tuple[str, str, int], int] = defaultdict(int)
    for kline in klines:
        counts[(kline.symbol.value, kline.interval.value, kline.open_time)] += 1
    return [
        DuplicateReport(symbol=sym, interval=itv, open_time=ot, count=n)
        for (sym, itv, ot), n in sorted(counts.items())
        if n > 1
    ]


def check_timestamp_monotonic(klines: Sequence[NormalizedKline]) -> list[tuple[int, int]]:
    """Return pairs of adjacent (previous, current) open_time values that are
    not strictly increasing, per ``(symbol, interval)`` partition.

    An empty list means timestamps are strictly increasing within each
    partition; this does not imply completeness.
    """
    per_partition: dict[tuple[str, str], list[int]] = defaultdict(list)
    for kline in klines:
        per_partition[(kline.symbol.value, kline.interval.value)].append(kline.open_time)

    violations: list[tuple[int, int]] = []
    for open_times in per_partition.values():
        sorted_hint = sorted(open_times)
        if open_times != sorted_hint:
            for previous, current in zip(open_times, open_times[1:], strict=False):
                if current <= previous:
                    violations.append((previous, current))
    return violations


def check_no_missing_bars(
    klines: Sequence[NormalizedKline],
    *,
    expected_start_ms: int,
    expected_end_ms: int,
    interval: Interval,
) -> list[MissingWindow]:
    """Detect gaps in the expected open_time progression.

    ``expected_start_ms`` and ``expected_end_ms`` are both inclusive and
    must be interval-aligned open_times. Returns a list of contiguous
    missing ranges; an empty list means the expected progression is
    fully populated.
    """
    duration = interval_duration_ms(interval)
    if expected_end_ms < expected_start_ms:
        raise ValueError("expected_end_ms must be >= expected_start_ms")
    if expected_start_ms % duration != 0 or expected_end_ms % duration != 0:
        raise ValueError("expected_start_ms and expected_end_ms must be interval-aligned")

    present: set[int] = {
        k.open_time
        for k in klines
        if k.interval is interval and expected_start_ms <= k.open_time <= expected_end_ms
    }
    expected_count = ((expected_end_ms - expected_start_ms) // duration) + 1

    missing: list[MissingWindow] = []
    run_start: int | None = None
    run_count = 0
    for i in range(expected_count):
        ms = expected_start_ms + i * duration
        if ms in present:
            if run_start is not None:
                missing.append(
                    MissingWindow(
                        start_open_time_ms=run_start,
                        end_open_time_ms=run_start + (run_count - 1) * duration,
                        missing_count=run_count,
                    )
                )
                run_start = None
                run_count = 0
        else:
            if run_start is None:
                run_start = ms
            run_count += 1
    if run_start is not None:
        missing.append(
            MissingWindow(
                start_open_time_ms=run_start,
                end_open_time_ms=run_start + (run_count - 1) * duration,
                missing_count=run_count,
            )
        )
    return missing


def check_no_future_bars(
    klines: Sequence[NormalizedKline],
    *,
    now_ms: int,
) -> list[NormalizedKline]:
    """Return bars whose open_time is in the future relative to ``now_ms``."""
    return [k for k in klines if k.open_time > now_ms]


# ---------------------------------------------------------------------------
# Funding-rate checks (Phase 2c)
# ---------------------------------------------------------------------------


class DuplicateFundingReport(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: str
    funding_time: int
    count: int


class ExtremeFundingReport(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: str
    funding_time: int
    funding_rate: float


def check_no_duplicate_funding_events(
    events: Sequence[FundingRateEvent],
) -> list[DuplicateFundingReport]:
    """Return funding-event identities seen more than once."""
    counts: dict[tuple[str, int], int] = defaultdict(int)
    for event in events:
        counts[(event.symbol.value, event.funding_time)] += 1
    return [
        DuplicateFundingReport(symbol=sym, funding_time=ft, count=n)
        for (sym, ft), n in sorted(counts.items())
        if n > 1
    ]


def check_funding_events_within_window(
    events: Sequence[FundingRateEvent],
    *,
    start_ms: int,
    end_ms: int,
) -> list[FundingRateEvent]:
    """Return funding events whose funding_time falls outside the window."""
    if end_ms < start_ms:
        raise ValueError("end_ms must be >= start_ms")
    return [e for e in events if e.funding_time < start_ms or e.funding_time > end_ms]


def check_funding_rate_magnitude(
    events: Sequence[FundingRateEvent],
    *,
    threshold: float = 0.01,
) -> list[ExtremeFundingReport]:
    """Soft-flag funding events whose rate magnitude exceeds ``threshold``.

    Not a hard fail; rates > 1% (the default threshold) are rare for USD-M
    perpetuals and worth an operator eye. The model-level bound at
    ``abs(rate) >= 1.0`` still rejects clearly-malformed inputs.
    """
    return [
        ExtremeFundingReport(
            symbol=e.symbol.value,
            funding_time=e.funding_time,
            funding_rate=e.funding_rate,
        )
        for e in events
        if abs(e.funding_rate) > threshold
    ]
