"""Point-in-time simulation clock predicates.

Per Phase 3 Gate 1 §10.1 and GAP-20260419-017 canonical form:
a bar is "visible" to the strategy when at least one full interval
duration has elapsed since its open_time. This is equivalent to
``t_now_ms > bar.close_time`` but is expressed against
``open_time + duration`` for clarity and for symmetry with how the
1h bias bar is selected.
"""

from __future__ import annotations

from collections.abc import Sequence

from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline


def bar_visible_at(t_now_ms: int, bar: NormalizedKline) -> bool:
    """Return True iff ``bar`` is completed relative to ``t_now_ms``."""
    duration = interval_duration_ms(bar.interval)
    return t_now_ms >= bar.open_time + duration


def select_latest_completed_1h(
    bars_1h: Sequence[NormalizedKline], decision_time_ms: int
) -> NormalizedKline | None:
    """Return the most recent 1h bar eligible for bias evaluation.

    Per GAP-20260419-017: a 1h bar is eligible when
    ``bar.open_time + 3_600_000 <= decision_time_ms``.
    """
    eligible = [b for b in bars_1h if bar_visible_at(decision_time_ms, b)]
    if not eligible:
        return None
    # Bars are assumed to arrive in ascending open_time but we pick
    # the max defensively.
    return max(eligible, key=lambda b: b.open_time)


def next_15m_open_time(bar: NormalizedKline) -> int:
    """Return the open_time of the 15m bar immediately after ``bar``.

    Caller is responsible for ensuring ``bar`` is a 15m bar.
    """
    if bar.interval != Interval.I_15M:
        raise ValueError("expected a 15m bar")
    return bar.open_time + interval_duration_ms(Interval.I_15M)
