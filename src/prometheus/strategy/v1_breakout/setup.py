"""8-bar consolidation / setup detection on 15m bars.

Per v1-breakout-strategy-spec.md §"Setup / Consolidation Rules":

    Use the previous 8 completed 15m candles.
    A setup is valid only when:
      1. setup_range_width <= 1.75 * ATR(20) on 15m
      2. abs(close[-1] - open[-8]) <= 0.35 * setup_range_width

The setup window is keyed by the first bar's open_time. The
"current" bar (breakout candidate) is NOT part of the window.
"""

from __future__ import annotations

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
