"""1h higher-timeframe trend-bias evaluation.

Per docs/03-strategy-research/v1-breakout-strategy-spec.md §"Higher-Timeframe Trend Bias".

Long bias requires ALL:
    1h EMA(50) > 1h EMA(200)
    latest completed 1h close > 1h EMA(50)
    1h EMA(50) is RISING vs 3 completed 1h candles earlier

Short bias is the symmetric mirror. Otherwise bias is NEUTRAL.

Phase 2s (R1b-narrow — Bias-strength redesign; Phase 2r spec memo §C)
adds ``evaluate_1h_bias_with_slope_strength``, a sibling predicate
that replaces the binary direction-sign slope-3 check with a magnitude
threshold. The 1h EMA(50)/EMA(200) computations and the EMA-position
component of the predicate are preserved unchanged. The original
``evaluate_1h_bias`` is preserved unchanged for bit-for-bit H0
compatibility.
"""

from __future__ import annotations

from collections.abc import Sequence
from math import isnan

from prometheus.core.klines import NormalizedKline

from ..indicators import ema
from ..types import TrendBias

EMA_FAST = 50
EMA_SLOW = 200
SLOPE_LOOKBACK = 3


def evaluate_1h_bias(completed_1h_bars: Sequence[NormalizedKline]) -> TrendBias:
    """Return the trend bias implied by a window of completed 1h bars.

    The caller must supply only COMPLETED 1h bars (``close_time <
    decision_time_ms``). The function evaluates the bias at the most
    recent bar in the input. If there are fewer than
    ``EMA_SLOW + SLOPE_LOOKBACK`` bars available, bias is NEUTRAL
    (insufficient warmup).
    """
    n = len(completed_1h_bars)
    if n < EMA_SLOW + SLOPE_LOOKBACK:
        return TrendBias.NEUTRAL
    closes = [b.close for b in completed_1h_bars]
    ema_fast = ema(closes, EMA_FAST)
    ema_slow = ema(closes, EMA_SLOW)
    last = n - 1
    slope_ref = last - SLOPE_LOOKBACK
    fast_now = ema_fast[last]
    slow_now = ema_slow[last]
    fast_then = ema_fast[slope_ref]
    close_now = closes[last]
    if isnan(fast_now) or isnan(slow_now) or isnan(fast_then):
        return TrendBias.NEUTRAL
    long_ok = (fast_now > slow_now) and (close_now > fast_now) and (fast_now > fast_then)
    short_ok = (fast_now < slow_now) and (close_now < fast_now) and (fast_now < fast_then)
    if long_ok and not short_ok:
        return TrendBias.LONG
    if short_ok and not long_ok:
        return TrendBias.SHORT
    return TrendBias.NEUTRAL


def evaluate_1h_bias_with_slope_strength(
    completed_1h_bars: Sequence[NormalizedKline],
    slope_strength_threshold: float,
) -> TrendBias:
    """R1b-narrow bias-validity predicate per Phase 2r spec memo §B / §E.

    Identical to ``evaluate_1h_bias`` except the slope-3 direction-sign
    check is replaced with a magnitude check. Let

        slope_strength_3 = (EMA(50)[now] - EMA(50)[now - 3]) / EMA(50)[now]

    Then:

        LONG  iff EMA(50)[now] > EMA(200)[now]
              AND close[now] > EMA(50)[now]
              AND slope_strength_3 >= +threshold
        SHORT iff EMA(50)[now] < EMA(200)[now]
              AND close[now] < EMA(50)[now]
              AND slope_strength_3 <= -threshold
        NEUTRAL otherwise

    The committed R1b-narrow value of ``slope_strength_threshold`` is
    0.0020 (= 0.20%) per Phase 2r spec memo §F. The threshold must be
    non-negative; ``threshold == 0.0`` would degenerate the magnitude
    check to ``slope_strength_3 >= 0`` (LONG) and ``<= 0`` (SHORT),
    which differs from H0's strict ``>`` / ``<`` only at the exact
    zero-slope boundary; for bit-for-bit H0 preservation the strategy
    facade dispatches to the original ``evaluate_1h_bias`` when the
    config field equals 0.0.

    Boundary cases:
    - Insufficient warmup (< EMA_SLOW + SLOPE_LOOKBACK bars) -> NEUTRAL.
    - Any of fast_now / slow_now / fast_then is NaN -> NEUTRAL.
    - fast_now <= 0 (degenerate; impossible after warmup with positive
      prices but defended for floating-point edge cases) -> NEUTRAL.
    - Slope at exactly +threshold admits LONG (non-strict ``>=``).
    - Slope at exactly -threshold admits SHORT (non-strict ``<=``).
    """
    if slope_strength_threshold < 0.0:
        raise ValueError(
            f"slope_strength_threshold must be non-negative, got {slope_strength_threshold}"
        )
    n = len(completed_1h_bars)
    if n < EMA_SLOW + SLOPE_LOOKBACK:
        return TrendBias.NEUTRAL
    closes = [b.close for b in completed_1h_bars]
    ema_fast = ema(closes, EMA_FAST)
    ema_slow = ema(closes, EMA_SLOW)
    last = n - 1
    slope_ref = last - SLOPE_LOOKBACK
    fast_now = ema_fast[last]
    slow_now = ema_slow[last]
    fast_then = ema_fast[slope_ref]
    close_now = closes[last]
    if isnan(fast_now) or isnan(slow_now) or isnan(fast_then):
        return TrendBias.NEUTRAL
    if fast_now <= 0.0:
        return TrendBias.NEUTRAL
    slope_strength_3 = (fast_now - fast_then) / fast_now
    long_ok = (
        (fast_now > slow_now)
        and (close_now > fast_now)
        and (slope_strength_3 >= slope_strength_threshold)
    )
    short_ok = (
        (fast_now < slow_now)
        and (close_now < fast_now)
        and (slope_strength_3 <= -slope_strength_threshold)
    )
    if long_ok and not short_ok:
        return TrendBias.LONG
    if short_ok and not long_ok:
        return TrendBias.SHORT
    return TrendBias.NEUTRAL
