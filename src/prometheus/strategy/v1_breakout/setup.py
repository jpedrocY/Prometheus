"""8-bar consolidation / setup detection on 15m bars.

Per v1-breakout-strategy-spec.md §"Setup / Consolidation Rules":

    Use the previous 8 completed 15m candles.
    A setup is valid only when:
      1. setup_range_width <= 1.75 * ATR(20) on 15m
      2. abs(close[-1] - open[-8]) <= 0.35 * setup_range_width

The setup window is keyed by the first bar's open_time. The
"current" bar (breakout candidate) is NOT part of the window.

Phase 2m (R1a — Volatility-percentile setup; Phase 2j memo §C) adds
``detect_setup_volatility_percentile``, a sibling predicate that
replaces the range_width / drift two-clause rule with a percentile-based
ranking of the 15m ATR(20) at the close of bar B-1 against its trailing
N-bar distribution. The 8-bar setup window itself is preserved (used
for setup_high / setup_low determination by the trigger). R1a does not
touch SETUP_SIZE.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from prometheus.core.klines import NormalizedKline

from ..types import SetupWindow

SETUP_SIZE = 8
MAX_RANGE_ATR_MULT = 1.75
MAX_DRIFT_RATIO = 0.35


def detect_setup(
    prior_bars: Sequence[NormalizedKline],
    atr_20_15m: float,
    *,
    setup_size: int = SETUP_SIZE,
) -> SetupWindow | None:
    """Detect a valid setup from ``prior_bars``.

    ``prior_bars`` must be exactly ``setup_size`` bars in ascending
    open_time order, strictly BEFORE the breakout candidate bar
    (see variant_config.py — the window excludes the current bar).

    ``atr_20_15m`` is the 15m ATR(20) value evaluated at the close of
    the LAST bar in the window (i.e., at position [-1]; NOT the
    breakout bar).

    ``setup_size`` defaults to the locked baseline (8). Phase 2g H-A1
    sets this to 10. Range-width and drift ratios are unchanged.

    Returns a ``SetupWindow`` if both conditions pass, else ``None``.
    """
    if len(prior_bars) != setup_size:
        return None
    if atr_20_15m <= 0:
        return None
    highs = [b.high for b in prior_bars]
    lows = [b.low for b in prior_bars]
    setup_high = max(highs)
    setup_low = min(lows)
    range_width = setup_high - setup_low
    if range_width > MAX_RANGE_ATR_MULT * atr_20_15m:
        return None
    drift_abs = abs(prior_bars[-1].close - prior_bars[0].open)
    if range_width > 0 and drift_abs > MAX_DRIFT_RATIO * range_width:
        return None
    # When range_width == 0 the bars are degenerate (flat). Reject
    # as a degenerate setup to avoid division-by-zero downstream and
    # because a zero-width setup is not a meaningful consolidation.
    if range_width == 0:
        return None
    return SetupWindow(
        symbol=prior_bars[0].symbol,
        first_bar_open_time=prior_bars[0].open_time,
        last_bar_open_time=prior_bars[-1].open_time,
        setup_high=setup_high,
        setup_low=setup_low,
        setup_range_width=range_width,
        net_drift_abs=drift_abs,
        atr_20_15m=atr_20_15m,
    )


def percentile_rank_threshold(percentile_threshold: int, lookback: int) -> int:
    """Rank threshold for the R1a percentile predicate.

    Per Phase 2j memo §C.5: ``rank(A_prior, Q_prior) <= floor(X * N / 100)``.
    Returns the integer rank cutoff (1-indexed). At X=25, N=200 this is 50:
    the setup is valid iff A_prior is among the 50 smallest of the 200
    trailing values, i.e. the bottom 25%.
    """
    return math.floor(percentile_threshold * lookback / 100)


def detect_setup_volatility_percentile(
    prior_bars: Sequence[NormalizedKline],
    atr_prior_15m: float,
    atr_history: Sequence[float],
    *,
    percentile_threshold: int,
    lookback: int,
    setup_size: int = SETUP_SIZE,
) -> SetupWindow | None:
    """R1a setup-validity predicate (Phase 2j memo §C.5).

    The 8-bar setup window is preserved from H0 — ``prior_bars`` is
    still ``setup_size`` completed 15m bars strictly BEFORE the
    breakout candidate, used only to determine ``setup_high`` /
    ``setup_low`` for the downstream trigger. The validity predicate
    is **replaced** by a percentile-based ranking:

    Let ``A_prior = atr_prior_15m`` (15m Wilder ATR(20) at close of
    bar B-1) and ``Q_prior = atr_history`` (trailing N values ending
    at close of bar B-1, inclusive of A_prior). The setup is valid iff

        rank(A_prior, Q_prior) <= floor(X * N / 100)

    where rank is the 1-indexed ascending rank within sorted Q_prior
    (mid-rank tie convention). Equivalently, A_prior is in the bottom
    X-th percentile of the trailing-N distribution.

    Boundary cases per spec:

    - ``len(atr_history) < lookback`` (insufficient history) -> reject.
    - Any NaN in ``atr_history`` -> reject (insufficient ATR seed
      anywhere in the lookback window).
    - ``atr_prior_15m`` NaN or non-positive -> reject.
    - ``range_width == 0`` (degenerate flat setup) -> reject (preserved
      from H0 to keep downstream invariants consistent).

    Returns a ``SetupWindow`` if valid, else ``None``.
    """
    if len(prior_bars) != setup_size:
        return None
    if atr_prior_15m != atr_prior_15m or atr_prior_15m <= 0:
        return None
    if len(atr_history) < lookback:
        return None
    # Take the most recent `lookback` values; reject if any NaN present.
    history = list(atr_history)[-lookback:]
    for v in history:
        if v != v:  # NaN
            return None
    rank_threshold = percentile_rank_threshold(percentile_threshold, lookback)
    # Mid-rank percentile rank: count values strictly less + 0.5 * count equal,
    # rounded up to the nearest integer. The spec says the rank is 1-indexed
    # ascending; we resolve ties by mid-rank for determinism.
    less = sum(1 for v in history if v < atr_prior_15m)
    equal = sum(1 for v in history if v == atr_prior_15m)
    rank = less + (equal + 1) // 2  # 1-indexed mid-rank, ceil-on-tie
    if rank > rank_threshold:
        return None
    highs = [b.high for b in prior_bars]
    lows = [b.low for b in prior_bars]
    setup_high = max(highs)
    setup_low = min(lows)
    range_width = setup_high - setup_low
    if range_width == 0:
        return None
    drift_abs = abs(prior_bars[-1].close - prior_bars[0].open)
    return SetupWindow(
        symbol=prior_bars[0].symbol,
        first_bar_open_time=prior_bars[0].open_time,
        last_bar_open_time=prior_bars[-1].open_time,
        setup_high=setup_high,
        setup_low=setup_low,
        setup_range_width=range_width,
        net_drift_abs=drift_abs,
        atr_20_15m=atr_prior_15m,
    )
