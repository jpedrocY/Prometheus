"""F1 strategy facade end-to-end tests (Phase 3b §4).

The facade combines features (overextension event), stop, target, and
admissibility band into a single ``evaluate_entry_signal`` call. These
tests exercise the integrated pipeline with synthetic series.
"""

from __future__ import annotations

import pytest

from prometheus.strategy.mean_reversion_overextension import (
    MeanReversionConfig,
    MeanReversionEntrySignal,
    MeanReversionStrategy,
)
from prometheus.strategy.types import Direction


def _build_short_candidate_series() -> tuple[list[float], list[float], list[float], list[float]]:
    """Build a 9-bar synthetic series that fires SHORT at B=8.

    closes: drift up by 5 over 8 bars (displacement = +5; threshold = 1.75 * 1 = 1.75 -> fires)
    highs / lows: tight bands so the structural stop is close to close[8].
    atr: constant 1.0 so threshold = 1.75 and band = [0.60, 1.80].

    With these bars, max(highs[1..8]) = closes[8] + 0.2 = 105.2 and the stop is
    105.2 + 0.10 = 105.30. A reference_price ~104.0..104.6 puts stop_distance
    in the [0.60, 1.80] band.
    """
    closes = [100.0, 100.5, 101.0, 101.5, 102.0, 102.5, 103.0, 103.5, 105.0]
    highs = [c + 0.2 for c in closes]
    lows = [c - 0.2 for c in closes]
    atr = [1.0] * 9
    return closes, highs, lows, atr


def _build_long_candidate_series() -> tuple[list[float], list[float], list[float], list[float]]:
    """Mirror of the SHORT series — drift down by 5 over 8 bars.

    With these bars, min(lows[1..8]) = closes[8] - 0.2 = 99.8 and the stop is
    99.8 - 0.10 = 99.70. A reference_price ~100.4..101.5 puts stop_distance
    in the [0.60, 1.80] band.
    """
    closes = [105.0, 104.5, 104.0, 103.5, 103.0, 102.5, 102.0, 101.5, 100.0]
    highs = [c + 0.2 for c in closes]
    lows = [c - 0.2 for c in closes]
    atr = [1.0] * 9
    return closes, highs, lows, atr


def _build_no_event_series() -> tuple[list[float], list[float], list[float], list[float]]:
    closes = [100.0, 100.1, 100.2, 100.3, 100.4, 100.5, 100.6, 100.7, 100.8]
    highs = [c + 0.2 for c in closes]
    lows = [c - 0.2 for c in closes]
    atr = [1.0] * 9
    return closes, highs, lows, atr


# ---------------------------------------------------------------------------
# Construction + config wiring
# ---------------------------------------------------------------------------


def test_strategy_default_config_is_locked_baseline() -> None:
    s = MeanReversionStrategy()
    assert s.config == MeanReversionConfig()


def test_strategy_explicit_config_round_trips() -> None:
    cfg = MeanReversionConfig()
    s = MeanReversionStrategy(cfg)
    assert s.config is cfg


# ---------------------------------------------------------------------------
# Signal generation
# ---------------------------------------------------------------------------


def test_below_threshold_no_signal() -> None:
    s = MeanReversionStrategy()
    closes, highs, lows, atr = _build_no_event_series()
    sig = s.evaluate_entry_signal(
        b_index=8,
        closes=closes,
        highs=highs,
        lows=lows,
        atr20=atr,
        reference_price=closes[8],
    )
    assert sig is None


def test_short_candidate_signal_generated() -> None:
    s = MeanReversionStrategy()
    closes, highs, lows, atr = _build_short_candidate_series()
    # Stop = max(highs[1..8]) + 0.10 = 105.2 + 0.10 = 105.30.
    # Pick reference_price ~104.4 so stop_distance ~0.90 (within [0.60, 1.80]).
    sig = s.evaluate_entry_signal(
        b_index=8,
        closes=closes,
        highs=highs,
        lows=lows,
        atr20=atr,
        reference_price=104.4,
    )
    assert sig is not None
    assert isinstance(sig, MeanReversionEntrySignal)
    assert sig.direction == Direction.SHORT
    assert sig.signal_bar_index == 8
    assert sig.atr_at_signal == 1.0
    # Stop is above reference price for SHORT.
    assert sig.initial_stop > sig.reference_price
    expected_stop = max(highs[1:9]) + 0.10 * 1.0
    assert sig.initial_stop == pytest.approx(expected_stop)
    assert sig.stop_distance == pytest.approx(abs(104.4 - expected_stop))
    # Frozen target = SMA(8) of closes[1..8] (B=8 -> window [B-7..B] = [1..8]).
    expected_target = sum(closes[1:9]) / 8.0
    assert sig.frozen_target == pytest.approx(expected_target)
    assert sig.displacement_at_signal == pytest.approx(closes[8] - closes[0])


def test_long_candidate_signal_generated() -> None:
    s = MeanReversionStrategy()
    closes, highs, lows, atr = _build_long_candidate_series()
    # Stop = min(lows[1..8]) - 0.10 = 99.8 - 0.10 = 99.70.
    # Pick reference_price ~100.6 so stop_distance ~0.90 (within band).
    sig = s.evaluate_entry_signal(
        b_index=8,
        closes=closes,
        highs=highs,
        lows=lows,
        atr20=atr,
        reference_price=100.6,
    )
    assert sig is not None
    assert sig.direction == Direction.LONG
    # Stop is below reference price for LONG.
    assert sig.initial_stop < sig.reference_price
    expected_stop = min(lows[1:9]) - 0.10 * 1.0
    assert sig.initial_stop == pytest.approx(expected_stop)
    assert sig.stop_distance == pytest.approx(abs(100.6 - expected_stop))
    expected_target = sum(closes[1:9]) / 8.0
    assert sig.frozen_target == pytest.approx(expected_target)
    assert sig.displacement_at_signal == pytest.approx(closes[8] - closes[0])
    assert sig.displacement_at_signal < 0.0


# ---------------------------------------------------------------------------
# Stop-distance admissibility integration
# ---------------------------------------------------------------------------


def test_stop_distance_below_band_rejected() -> None:
    """If reference_price is too close to the stop, the signal is dropped."""
    s = MeanReversionStrategy()
    closes, highs, lows, atr = _build_short_candidate_series()
    # Stop = max(highs[1..8]) + 0.10 = 105.20 + 0.10 = 105.30.
    # Use reference_price=105.0 -> stop_distance = 0.30 < 0.60 * atr -> rejected.
    sig = s.evaluate_entry_signal(
        b_index=8,
        closes=closes,
        highs=highs,
        lows=lows,
        atr20=atr,
        reference_price=105.0,
    )
    assert sig is None


def test_stop_distance_above_band_rejected() -> None:
    """If reference_price is far from the stop, the signal is dropped."""
    s = MeanReversionStrategy()
    closes, highs, lows, atr = _build_short_candidate_series()
    # Stop = 105.30, atr=1.0 -> max admissible stop_distance = 1.80.
    # Use reference_price=103.0 -> stop_distance = 2.30 > 1.80 -> rejected.
    sig = s.evaluate_entry_signal(
        b_index=8,
        closes=closes,
        highs=highs,
        lows=lows,
        atr20=atr,
        reference_price=103.0,
    )
    assert sig is None


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def test_non_positive_reference_price_raises() -> None:
    s = MeanReversionStrategy()
    closes, highs, lows, atr = _build_short_candidate_series()
    with pytest.raises(ValueError):
        s.evaluate_entry_signal(
            b_index=8,
            closes=closes,
            highs=highs,
            lows=lows,
            atr20=atr,
            reference_price=0.0,
        )


def test_b_index_out_of_atr_range_raises() -> None:
    s = MeanReversionStrategy()
    closes, highs, lows, _ = _build_short_candidate_series()
    short_atr = [1.0] * 5  # too short
    with pytest.raises(IndexError):
        s.evaluate_entry_signal(
            b_index=8,
            closes=closes,
            highs=highs,
            lows=lows,
            atr20=short_atr,
            reference_price=105.0,
        )
