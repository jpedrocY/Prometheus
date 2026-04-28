"""F1 feature function tests (Phase 3b §4).

Covers:

    - cumulative_displacement_8bar: window correctness, warmup, OOR.
    - sma_8_close: SMA correctness, warmup, OOR.
    - overextension_event:
        * below threshold -> no event (False, 0)
        * at-threshold boundary (strict >) -> no event
        * above threshold positive -> SHORT candidate (+1)
        * above threshold negative -> LONG candidate (-1)
        * non-positive ATR rejected
"""

from __future__ import annotations

import pytest

from prometheus.strategy.mean_reversion_overextension.features import (
    cumulative_displacement_8bar,
    overextension_event,
    sma_8_close,
)

# ---------------------------------------------------------------------------
# cumulative_displacement_8bar
# ---------------------------------------------------------------------------


def test_displacement_basic_positive() -> None:
    closes = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 110.0]
    # B = 8, B - 8 = 0  -> 110 - 100 = +10
    assert cumulative_displacement_8bar(closes, 8) == 10.0


def test_displacement_basic_negative() -> None:
    closes = [110.0, 109.0, 108.0, 107.0, 106.0, 105.0, 104.0, 103.0, 95.0]
    # B = 8, B - 8 = 0 -> 95 - 110 = -15
    assert cumulative_displacement_8bar(closes, 8) == -15.0


def test_displacement_warmup_below_8_raises() -> None:
    closes = [100.0] * 7
    with pytest.raises(IndexError):
        cumulative_displacement_8bar(closes, 7)


def test_displacement_index_out_of_range() -> None:
    closes = [100.0] * 9
    with pytest.raises(IndexError):
        cumulative_displacement_8bar(closes, 9)


# ---------------------------------------------------------------------------
# sma_8_close
# ---------------------------------------------------------------------------


def test_sma_8_close_constant_series() -> None:
    closes = [50.0] * 10
    assert sma_8_close(closes, 7) == pytest.approx(50.0)
    assert sma_8_close(closes, 9) == pytest.approx(50.0)


def test_sma_8_close_arithmetic_progression() -> None:
    # closes[0..7] = 1..8 -> SMA = 4.5
    closes = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 99.0]
    assert sma_8_close(closes, 7) == pytest.approx(4.5)
    # closes[1..8] = 2..8, 99 -> sum = 134, mean = 16.75
    assert sma_8_close(closes, 8) == pytest.approx(16.75)


def test_sma_8_close_warmup_raises() -> None:
    closes = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]  # only 7 bars
    with pytest.raises(IndexError):
        sma_8_close(closes, 6)


def test_sma_8_close_oor_raises() -> None:
    closes = [1.0] * 8
    with pytest.raises(IndexError):
        sma_8_close(closes, 8)


# ---------------------------------------------------------------------------
# overextension_event
# ---------------------------------------------------------------------------


def _make_atr(n: int, value: float = 1.0) -> list[float]:
    return [value] * n


def test_overextension_below_threshold_no_event() -> None:
    closes = [100.0] * 9
    closes[8] = 100.0 + 1.74  # displacement 1.74, threshold 1.75 -> not strict >
    atr = _make_atr(9, 1.0)
    fires, direction = overextension_event(
        closes=closes, atr20=atr, b_index=8, threshold_atr_multiple=1.75
    )
    assert fires is False
    assert direction == 0


def test_overextension_at_threshold_strictly_not_firing() -> None:
    # Strict ">" boundary: equality at threshold does NOT fire.
    closes = [100.0] * 9
    closes[8] = 100.0 + 1.75
    atr = _make_atr(9, 1.0)
    fires, direction = overextension_event(
        closes=closes, atr20=atr, b_index=8, threshold_atr_multiple=1.75
    )
    assert fires is False
    assert direction == 0


def test_overextension_above_threshold_positive_short_candidate() -> None:
    closes = [100.0] * 9
    closes[8] = 100.0 + 2.00  # +2 vs threshold 1.75
    atr = _make_atr(9, 1.0)
    fires, direction = overextension_event(
        closes=closes, atr20=atr, b_index=8, threshold_atr_multiple=1.75
    )
    assert fires is True
    assert direction == +1  # short candidate


def test_overextension_above_threshold_negative_long_candidate() -> None:
    closes = [100.0] * 9
    closes[8] = 100.0 - 2.00  # -2 vs threshold 1.75
    atr = _make_atr(9, 1.0)
    fires, direction = overextension_event(
        closes=closes, atr20=atr, b_index=8, threshold_atr_multiple=1.75
    )
    assert fires is True
    assert direction == -1  # long candidate


def test_overextension_threshold_scales_with_atr() -> None:
    closes = [100.0] * 9
    closes[8] = 100.0 + 4.0  # +4
    atr_low = _make_atr(9, 1.0)  # threshold 1.75 -> fires
    atr_high = _make_atr(9, 4.0)  # threshold 7.0 -> does NOT fire
    fires_low, _ = overextension_event(
        closes=closes, atr20=atr_low, b_index=8, threshold_atr_multiple=1.75
    )
    fires_high, _ = overextension_event(
        closes=closes, atr20=atr_high, b_index=8, threshold_atr_multiple=1.75
    )
    assert fires_low is True
    assert fires_high is False


def test_overextension_rejects_non_positive_atr() -> None:
    closes = [100.0] * 9
    atr = _make_atr(9, 0.0)
    with pytest.raises(ValueError):
        overextension_event(closes=closes, atr20=atr, b_index=8, threshold_atr_multiple=1.75)


def test_overextension_warmup_propagates_index_error() -> None:
    closes = [100.0] * 7
    atr = _make_atr(7, 1.0)
    with pytest.raises(IndexError):
        overextension_event(closes=closes, atr20=atr, b_index=6, threshold_atr_multiple=1.75)
