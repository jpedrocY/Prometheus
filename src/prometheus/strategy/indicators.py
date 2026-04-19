"""Pure indicator functions: EMA, True Range, Wilder ATR.

All functions are deterministic and take plain float inputs. Callers
are responsible for feeding only completed bars in chronological
order. Indicator outputs at the start of a series (before warmup is
reached) are defined as the arithmetic seed value; the caller should
verify enough bars are present before reading indicator values.

Per v1-breakout-strategy-spec.md §"Core Definitions" and
docs/03-strategy-research/v1-breakout-backtest-plan.md §"Indicator
assumptions".
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def ema(values: Sequence[float], period: int) -> list[float]:
    """Exponential moving average with SMA-seed.

    The first ``period`` samples are seeded with the simple mean of
    the first ``period`` samples (a common and well-documented
    seeding choice). Before the seed is available, the output is
    filled with NaN. After the seed, the recursion uses

        ema[i] = alpha * values[i] + (1 - alpha) * ema[i-1]
        alpha = 2 / (period + 1)

    Parameters
    ----------
    values:
        A sequence of float samples in chronological order.
    period:
        Positive integer. Must be <= len(values) to produce any
        numeric output; otherwise the full output is NaN.

    Returns
    -------
    list[float]
        Same length as ``values``. Positions 0..period-2 are NaN
        (warmup); position period-1 equals the SMA seed; subsequent
        positions use the EMA recursion.
    """
    if period <= 0:
        raise ValueError(f"ema period must be positive, got {period}")
    n = len(values)
    if n == 0:
        return []
    arr = np.asarray(values, dtype=np.float64)
    out = np.full(n, np.nan, dtype=np.float64)
    if n < period:
        return [float(x) for x in out]
    # Seed at index period-1 with SMA of first `period` values.
    seed = float(arr[:period].mean())
    out[period - 1] = seed
    if n == period:
        return [float(x) for x in out]
    alpha = 2.0 / (period + 1.0)
    prev = seed
    for i in range(period, n):
        cur = alpha * float(arr[i]) + (1.0 - alpha) * prev
        out[i] = cur
        prev = cur
    return [float(x) for x in out]


def true_range(high: float, low: float, prev_close: float | None) -> float:
    """Single-bar True Range.

    On the very first bar of a series (no prior close), True Range
    is defined as ``high - low``. For later bars it is the maximum of
    three candidate ranges:

        max(high - low, abs(high - prev_close), abs(low - prev_close))
    """
    if high < low:
        raise ValueError(f"true_range: high {high} < low {low}")
    if prev_close is None:
        return high - low
    return max(high - low, abs(high - prev_close), abs(low - prev_close))


def wilder_atr(
    highs: Sequence[float],
    lows: Sequence[float],
    closes: Sequence[float],
    period: int,
) -> list[float]:
    """Wilder's ATR (the de-facto standard "ATR").

    Seeds with the arithmetic mean of the first ``period`` true-range
    values, then applies Wilder smoothing:

        atr[i] = ((period - 1) * atr[i-1] + TR[i]) / period

    The output has the same length as the input sequences. Positions
    0..period-1 are NaN (warmup), position ``period`` is the seed,
    and positions >= period+1 use the recursion.

    Parameters
    ----------
    highs, lows, closes:
        Parallel float sequences of equal length.
    period:
        Positive integer.

    Raises
    ------
    ValueError
        If the three input sequences have different lengths or if
        period is non-positive.
    """
    if period <= 0:
        raise ValueError(f"wilder_atr period must be positive, got {period}")
    n = len(highs)
    if len(lows) != n or len(closes) != n:
        raise ValueError("highs, lows, closes must have equal length")
    out = np.full(n, np.nan, dtype=np.float64)
    if n == 0:
        return []
    # Compute per-bar true ranges.
    tr = np.full(n, np.nan, dtype=np.float64)
    tr[0] = true_range(float(highs[0]), float(lows[0]), None)
    for i in range(1, n):
        tr[i] = true_range(float(highs[i]), float(lows[i]), float(closes[i - 1]))
    if n <= period:
        return [float(x) for x in out]
    # Seed at index `period` with the simple mean of tr[0..period-1].
    seed = float(tr[:period].mean())
    out[period] = seed
    prev = seed
    for i in range(period + 1, n):
        cur = ((period - 1) * prev + float(tr[i])) / period
        out[i] = cur
        prev = cur
    return [float(x) for x in out]
