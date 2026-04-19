from __future__ import annotations

from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.strategy.v1_breakout.setup import (
    MAX_DRIFT_RATIO,
    MAX_RANGE_ATR_MULT,
    SETUP_SIZE,
    detect_setup,
)

from ..conftest import ANCHOR_MS, kline


def _make_8_bars(
    opens: list[float],
    closes: list[float],
    highs: list[float] | None = None,
    lows: list[float] | None = None,
) -> list:
    assert len(opens) == SETUP_SIZE
    t = ANCHOR_MS
    d = interval_duration_ms(Interval.I_15M)
    bars = []
    for i in range(SETUP_SIZE):
        o = opens[i]
        c = closes[i]
        h = highs[i] if highs else max(o, c) + 0.1
        lo = lows[i] if lows else min(o, c) - 0.1
        bars.append(kline(open_time=t, open=o, high=h, low=lo, close=c))
        t += d
    return bars


def test_wrong_bar_count_returns_none() -> None:
    bars = _make_8_bars([100.0] * SETUP_SIZE, [100.5] * SETUP_SIZE)[:4]
    assert detect_setup(bars, atr_20_15m=1.0) is None


def test_zero_atr_returns_none() -> None:
    bars = _make_8_bars([100.0] * SETUP_SIZE, [100.5] * SETUP_SIZE)
    assert detect_setup(bars, atr_20_15m=0.0) is None


def test_valid_tight_setup() -> None:
    # Range ~ 1.0, ATR = 1.0 -> 1.0 / 1.0 = 1.0 <= 1.75 OK
    # Net drift = |close[-1] - open[0]| = 0.4 -> drift ratio = 0.4 vs 0.35*1.0 = 0.35 NG
    # Adjust: close[-1] = 100.1, open[0] = 100.0 -> drift = 0.1 OK
    opens = [100.0] * SETUP_SIZE
    closes = [100.3, 100.2, 100.4, 100.3, 100.5, 100.4, 100.2, 100.1]
    highs = [100.7, 100.6, 100.7, 100.7, 100.8, 100.7, 100.6, 100.5]
    lows = [99.7, 99.8, 99.9, 99.8, 99.9, 99.7, 99.8, 99.8]
    bars = _make_8_bars(opens, closes, highs, lows)
    setup = detect_setup(bars, atr_20_15m=1.0)
    assert setup is not None
    assert setup.setup_high == 100.8
    assert setup.setup_low == 99.7
    assert setup.setup_range_width == float((100.8) - (99.7))


def test_range_exceeds_1_75_atr_returns_none() -> None:
    opens = [100.0] * SETUP_SIZE
    closes = [100.0] * SETUP_SIZE
    # Range = 2.0; ATR = 1.0; ratio = 2.0 > 1.75 -> reject
    highs = [101.0] * SETUP_SIZE
    lows = [99.0] * SETUP_SIZE
    bars = _make_8_bars(opens, closes, highs, lows)
    assert detect_setup(bars, atr_20_15m=1.0) is None


def test_drift_exceeds_0_35_of_range_returns_none() -> None:
    # Range ~ 1.0 OK; drift = 0.5 > 0.35*1.0 -> reject
    opens = [100.0] + [100.2] * (SETUP_SIZE - 1)
    closes = [100.2] * (SETUP_SIZE - 1) + [100.5]
    highs = [100.7] * SETUP_SIZE
    lows = [99.7] * SETUP_SIZE
    bars = _make_8_bars(opens, closes, highs, lows)
    assert detect_setup(bars, atr_20_15m=1.0) is None


def test_degenerate_zero_width_returns_none() -> None:
    opens = [100.0] * SETUP_SIZE
    closes = [100.0] * SETUP_SIZE
    highs = [100.0] * SETUP_SIZE
    lows = [100.0] * SETUP_SIZE
    bars = _make_8_bars(opens, closes, highs, lows)
    # range_width=0 -> degenerate, reject.
    assert detect_setup(bars, atr_20_15m=1.0) is None


def test_sanity_bounds_captured_in_window() -> None:
    # Range = 1.75 * ATR exactly (boundary accept), drift small.
    opens = [100.0] * SETUP_SIZE
    closes = [100.0] * SETUP_SIZE
    highs = [100.875] * SETUP_SIZE
    lows = [99.125] * SETUP_SIZE
    bars = _make_8_bars(opens, closes, highs, lows)
    # range = 1.75, atr = 1.0 -> boundary 1.75*1.0 = 1.75 OK (<=)
    setup = detect_setup(bars, atr_20_15m=1.0)
    assert setup is not None
    assert setup.setup_range_width == float((100.875) - (99.125))
    assert setup.setup_range_width <= MAX_RANGE_ATR_MULT * 1.0
    assert setup.net_drift_abs <= MAX_DRIFT_RATIO * setup.setup_range_width
