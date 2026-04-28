"""F1 stop computation + admissibility tests (Phase 3b §4)."""

from __future__ import annotations

import pytest

from prometheus.strategy.mean_reversion_overextension.stop import (
    STOP_BUFFER_ATR_MULTIPLE,
    STOP_DISTANCE_MAX_ATR,
    STOP_DISTANCE_MIN_ATR,
    compute_initial_stop,
    passes_stop_distance_filter,
)
from prometheus.strategy.types import Direction

# ---------------------------------------------------------------------------
# compute_initial_stop — long
# ---------------------------------------------------------------------------


def test_long_stop_uses_lowest_low_minus_buffer() -> None:
    # 8-bar window B-7..B has lows ascending; lowest_low = lows[B-7].
    lows = [90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0]
    highs = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0]
    atr = 2.0
    stop = compute_initial_stop(
        direction=Direction.LONG,
        lows=lows,
        highs=highs,
        atr20_at_b=atr,
        b_index=7,
        stop_buffer_atr_multiple=STOP_BUFFER_ATR_MULTIPLE,
    )
    expected = 90.0 - 0.10 * 2.0  # 89.80
    assert stop == pytest.approx(expected)


def test_long_stop_uses_min_in_window_only() -> None:
    # Lower low BEFORE the window must NOT influence the stop.
    lows = [10.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0]
    highs = [100.0] * 9
    atr = 1.0
    stop = compute_initial_stop(
        direction=Direction.LONG,
        lows=lows,
        highs=highs,
        atr20_at_b=atr,
        b_index=8,
        stop_buffer_atr_multiple=STOP_BUFFER_ATR_MULTIPLE,
    )
    # Window is indices 1..8 -> lowest = 91.0
    expected = 91.0 - 0.10 * 1.0
    assert stop == pytest.approx(expected)


# ---------------------------------------------------------------------------
# compute_initial_stop — short
# ---------------------------------------------------------------------------


def test_short_stop_uses_highest_high_plus_buffer() -> None:
    lows = [90.0] * 8
    highs = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0]
    atr = 2.0
    stop = compute_initial_stop(
        direction=Direction.SHORT,
        lows=lows,
        highs=highs,
        atr20_at_b=atr,
        b_index=7,
        stop_buffer_atr_multiple=STOP_BUFFER_ATR_MULTIPLE,
    )
    expected = 107.0 + 0.10 * 2.0  # 107.20
    assert stop == pytest.approx(expected)


def test_short_stop_uses_max_in_window_only() -> None:
    lows = [90.0] * 9
    # Higher high BEFORE the window must NOT influence the stop.
    highs = [200.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0]
    atr = 1.0
    stop = compute_initial_stop(
        direction=Direction.SHORT,
        lows=lows,
        highs=highs,
        atr20_at_b=atr,
        b_index=8,
        stop_buffer_atr_multiple=STOP_BUFFER_ATR_MULTIPLE,
    )
    # Window is indices 1..8 -> highest = 108.0
    expected = 108.0 + 0.10 * 1.0
    assert stop == pytest.approx(expected)


def test_compute_initial_stop_warmup_raises() -> None:
    lows = [90.0] * 6
    highs = [100.0] * 6
    with pytest.raises(IndexError):
        compute_initial_stop(
            direction=Direction.LONG,
            lows=lows,
            highs=highs,
            atr20_at_b=1.0,
            b_index=5,
            stop_buffer_atr_multiple=STOP_BUFFER_ATR_MULTIPLE,
        )


def test_compute_initial_stop_non_positive_atr_raises() -> None:
    lows = [90.0] * 8
    highs = [100.0] * 8
    with pytest.raises(ValueError):
        compute_initial_stop(
            direction=Direction.LONG,
            lows=lows,
            highs=highs,
            atr20_at_b=0.0,
            b_index=7,
            stop_buffer_atr_multiple=STOP_BUFFER_ATR_MULTIPLE,
        )


# ---------------------------------------------------------------------------
# passes_stop_distance_filter
# ---------------------------------------------------------------------------


def test_passes_stop_distance_in_band() -> None:
    atr = 10.0
    # Band: [6.0, 18.0]
    assert passes_stop_distance_filter(
        stop_distance=6.0,
        atr20_at_b=atr,
        min_atr_multiple=STOP_DISTANCE_MIN_ATR,
        max_atr_multiple=STOP_DISTANCE_MAX_ATR,
    )
    assert passes_stop_distance_filter(
        stop_distance=12.0,
        atr20_at_b=atr,
        min_atr_multiple=STOP_DISTANCE_MIN_ATR,
        max_atr_multiple=STOP_DISTANCE_MAX_ATR,
    )
    assert passes_stop_distance_filter(
        stop_distance=18.0,
        atr20_at_b=atr,
        min_atr_multiple=STOP_DISTANCE_MIN_ATR,
        max_atr_multiple=STOP_DISTANCE_MAX_ATR,
    )


def test_rejects_below_band() -> None:
    atr = 10.0
    assert not passes_stop_distance_filter(
        stop_distance=5.99,
        atr20_at_b=atr,
        min_atr_multiple=STOP_DISTANCE_MIN_ATR,
        max_atr_multiple=STOP_DISTANCE_MAX_ATR,
    )


def test_rejects_above_band() -> None:
    atr = 10.0
    assert not passes_stop_distance_filter(
        stop_distance=18.01,
        atr20_at_b=atr,
        min_atr_multiple=STOP_DISTANCE_MIN_ATR,
        max_atr_multiple=STOP_DISTANCE_MAX_ATR,
    )


def test_rejects_non_positive_stop_distance() -> None:
    atr = 10.0
    assert not passes_stop_distance_filter(
        stop_distance=0.0,
        atr20_at_b=atr,
        min_atr_multiple=STOP_DISTANCE_MIN_ATR,
        max_atr_multiple=STOP_DISTANCE_MAX_ATR,
    )


def test_rejects_non_positive_atr() -> None:
    assert not passes_stop_distance_filter(
        stop_distance=10.0,
        atr20_at_b=0.0,
        min_atr_multiple=STOP_DISTANCE_MIN_ATR,
        max_atr_multiple=STOP_DISTANCE_MAX_ATR,
    )
