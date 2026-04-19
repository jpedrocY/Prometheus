"""1h higher-timeframe trend-bias evaluation.

Per docs/03-strategy-research/v1-breakout-strategy-spec.md §"Higher-Timeframe Trend Bias".

Long bias requires ALL:
    1h EMA(50) > 1h EMA(200)
    latest completed 1h close > 1h EMA(50)
    1h EMA(50) is RISING vs 3 completed 1h candles earlier

Short bias is the symmetric mirror. Otherwise bias is NEUTRAL.
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
