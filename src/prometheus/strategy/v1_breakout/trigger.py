"""Breakout trigger evaluation (long + short) on the completed 15m signal bar.

Per v1-breakout-strategy-spec.md §"Entry Trigger Rules". Six
conditions must ALL be true for a signal to fire:

    1. Higher-timeframe bias active in the candidate direction
    2. Valid setup exists
    3. Breakout bar close > setup_high + 0.10*ATR(20) (long)
       or close < setup_low - 0.10*ATR(20) (short)
    4. Breakout bar true range >= 1.0 * ATR(20)_15m
    5. Breakout bar closes in top 25% (long) or bottom 25% (short) of own range
    6. 1h normalized ATR filter: 0.20% <= ATR(20)_1h / latest_1h_close <= 2.00%

The normalized-ATR filter ambiguity (Gate-1 §11.A.A1) is resolved
per operator approval (GAP-20260419-014): use 1h ATR(20) and latest
completed 1h close.
"""

from __future__ import annotations

from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol

from ..indicators import true_range
from ..types import BreakoutSignal, Direction, SetupWindow, TrendBias

BREAKOUT_BUFFER_ATR_MULT = 0.10
TRUE_RANGE_ATR_MULT = 1.0
CLOSE_LOCATION_RATIO = 0.75  # top-25% for long, bottom-25% for short = <=0.25 from low
ATR_REGIME_MIN = 0.0020  # 0.20%
ATR_REGIME_MAX = 0.0200  # 2.00%


def _passes_atr_regime(atr_20_1h: float, latest_1h_close: float) -> bool:
    if latest_1h_close <= 0:
        return False
    if atr_20_1h <= 0:
        return False
    normalized = atr_20_1h / latest_1h_close
    return ATR_REGIME_MIN <= normalized <= ATR_REGIME_MAX


def _true_range_passes(
    breakout_bar: NormalizedKline,
    prev_close: float,
    atr_20_15m: float,
    *,
    expansion_atr_mult: float = TRUE_RANGE_ATR_MULT,
) -> bool:
    tr = true_range(breakout_bar.high, breakout_bar.low, prev_close)
    return tr >= expansion_atr_mult * atr_20_15m


def _close_in_top_quarter(bar: NormalizedKline) -> bool:
    span = bar.high - bar.low
    if span <= 0:
        return False
    location = (bar.close - bar.low) / span
    return location >= CLOSE_LOCATION_RATIO


def _close_in_bottom_quarter(bar: NormalizedKline) -> bool:
    span = bar.high - bar.low
    if span <= 0:
        return False
    location = (bar.close - bar.low) / span
    return location <= (1.0 - CLOSE_LOCATION_RATIO)


def _build_signal(
    *,
    symbol: Symbol,
    direction: Direction,
    breakout_bar: NormalizedKline,
    setup: SetupWindow,
    atr_20_1h: float,
    latest_1h_close: float,
    trend_bias: TrendBias,
) -> BreakoutSignal:
    return BreakoutSignal(
        symbol=symbol,
        direction=direction,
        signal_bar_open_time=breakout_bar.open_time,
        signal_bar_close_time=breakout_bar.close_time,
        signal_bar_close=breakout_bar.close,
        signal_bar_high=breakout_bar.high,
        signal_bar_low=breakout_bar.low,
        setup=setup,
        atr_20_15m=setup.atr_20_15m,
        atr_20_1h=atr_20_1h,
        latest_1h_close=latest_1h_close,
        normalized_atr_1h=atr_20_1h / latest_1h_close,
        trend_bias=trend_bias,
    )


def evaluate_long_trigger(
    *,
    bias: TrendBias,
    setup: SetupWindow | None,
    breakout_bar: NormalizedKline,
    prev_15m_close: float,
    atr_20_15m: float,
    atr_20_1h: float,
    latest_1h_close: float,
    expansion_atr_mult: float = TRUE_RANGE_ATR_MULT,
) -> BreakoutSignal | None:
    """Long-direction six-condition trigger.

    Returns a ``BreakoutSignal`` if all six conditions pass, else
    ``None``. ``expansion_atr_mult`` controls the breakout-bar TR
    gate and defaults to the locked baseline (1.0 × ATR20). Phase 2g
    H-B2 sets this to 0.75.
    """
    if bias != TrendBias.LONG:
        return None
    if setup is None:
        return None
    if atr_20_15m <= 0:
        return None
    trigger_level = setup.setup_high + BREAKOUT_BUFFER_ATR_MULT * atr_20_15m
    if breakout_bar.close <= trigger_level:
        return None
    if not _true_range_passes(
        breakout_bar, prev_15m_close, atr_20_15m, expansion_atr_mult=expansion_atr_mult
    ):
        return None
    if not _close_in_top_quarter(breakout_bar):
        return None
    if not _passes_atr_regime(atr_20_1h, latest_1h_close):
        return None
    return _build_signal(
        symbol=breakout_bar.symbol,
        direction=Direction.LONG,
        breakout_bar=breakout_bar,
        setup=setup,
        atr_20_1h=atr_20_1h,
        latest_1h_close=latest_1h_close,
        trend_bias=bias,
    )


def evaluate_short_trigger(
    *,
    bias: TrendBias,
    setup: SetupWindow | None,
    breakout_bar: NormalizedKline,
    prev_15m_close: float,
    atr_20_15m: float,
    atr_20_1h: float,
    latest_1h_close: float,
    expansion_atr_mult: float = TRUE_RANGE_ATR_MULT,
) -> BreakoutSignal | None:
    """Short-direction six-condition trigger.

    ``expansion_atr_mult`` defaults to the locked baseline (1.0 × ATR20);
    Phase 2g H-B2 sets this to 0.75.
    """
    if bias != TrendBias.SHORT:
        return None
    if setup is None:
        return None
    if atr_20_15m <= 0:
        return None
    trigger_level = setup.setup_low - BREAKOUT_BUFFER_ATR_MULT * atr_20_15m
    if breakout_bar.close >= trigger_level:
        return None
    if not _true_range_passes(
        breakout_bar, prev_15m_close, atr_20_15m, expansion_atr_mult=expansion_atr_mult
    ):
        return None
    if not _close_in_bottom_quarter(breakout_bar):
        return None
    if not _passes_atr_regime(atr_20_1h, latest_1h_close):
        return None
    return _build_signal(
        symbol=breakout_bar.symbol,
        direction=Direction.SHORT,
        breakout_bar=breakout_bar,
        setup=setup,
        atr_20_1h=atr_20_1h,
        latest_1h_close=latest_1h_close,
        trend_bias=bias,
    )
