from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol
from prometheus.research.backtest.funding_join import apply_funding_accrual
from tests.unit.strategy.conftest import funding

ANCHOR = 1_772_582_400_000
EIGHT_HOURS_MS = 8 * 60 * 60 * 1000


def _events(rates: list[float], symbol: Symbol = Symbol.BTCUSDT) -> list:
    return [
        funding(symbol=symbol, funding_time=ANCHOR + i * EIGHT_HOURS_MS, funding_rate=r)
        for i, r in enumerate(rates)
    ]


def test_no_events_in_window() -> None:
    events = _events([0.0001, 0.0002, -0.0001])
    total, matched = apply_funding_accrual(
        direction_long=True,
        entry_fill_time_ms=ANCHOR + 100 * EIGHT_HOURS_MS,
        exit_fill_time_ms=ANCHOR + 101 * EIGHT_HOURS_MS,
        position_notional_usdt=1_000.0,
        funding_events=events,
    )
    assert total == 0.0
    assert matched == []


def test_long_pays_positive_rate() -> None:
    events = _events([0.0001])  # rate > 0, long pays
    total, matched = apply_funding_accrual(
        direction_long=True,
        entry_fill_time_ms=ANCHOR - 1,
        exit_fill_time_ms=ANCHOR + 1,
        position_notional_usdt=1_000.0,
        funding_events=events,
    )
    assert len(matched) == 1
    # Long's funding_pnl = notional * rate * (-direction_sign) = 1000 * 0.0001 * -1 = -0.1
    assert total == pytest.approx(-0.1)


def test_short_receives_positive_rate() -> None:
    events = _events([0.0001])
    total, _ = apply_funding_accrual(
        direction_long=False,
        entry_fill_time_ms=ANCHOR - 1,
        exit_fill_time_ms=ANCHOR + 1,
        position_notional_usdt=1_000.0,
        funding_events=events,
    )
    # Short's funding_pnl = 1000 * 0.0001 * +1 = +0.1
    assert total == pytest.approx(0.1)


def test_inclusive_both_ends() -> None:
    """Per GAP-20260419-019 operator decision: window is inclusive both ends."""
    events = _events([0.0001])
    # Event exactly AT entry time -> included.
    total_at_entry, matched_entry = apply_funding_accrual(
        direction_long=True,
        entry_fill_time_ms=ANCHOR,
        exit_fill_time_ms=ANCHOR + 1_000,
        position_notional_usdt=1_000.0,
        funding_events=events,
    )
    assert len(matched_entry) == 1
    # Event exactly AT exit time -> included.
    total_at_exit, matched_exit = apply_funding_accrual(
        direction_long=True,
        entry_fill_time_ms=ANCHOR - 1_000,
        exit_fill_time_ms=ANCHOR,
        position_notional_usdt=1_000.0,
        funding_events=events,
    )
    assert len(matched_exit) == 1


def test_multiple_events_summed() -> None:
    events = _events([0.0001, 0.0002, 0.0003])
    total, matched = apply_funding_accrual(
        direction_long=True,
        entry_fill_time_ms=ANCHOR - 1,
        exit_fill_time_ms=ANCHOR + 3 * EIGHT_HOURS_MS,
        position_notional_usdt=1_000.0,
        funding_events=events,
    )
    assert len(matched) == 3
    assert total == pytest.approx(-(0.0001 + 0.0002 + 0.0003) * 1_000.0)


def test_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        apply_funding_accrual(
            direction_long=True,
            entry_fill_time_ms=100,
            exit_fill_time_ms=50,
            position_notional_usdt=1_000.0,
            funding_events=[],
        )
    with pytest.raises(ValueError):
        apply_funding_accrual(
            direction_long=True,
            entry_fill_time_ms=100,
            exit_fill_time_ms=200,
            position_notional_usdt=0.0,
            funding_events=[],
        )


# Per GAP-20260420-029: Binance fundingRate returns markPrice="" for
# pre-2024 funding events. FundingRateEvent.mark_price is Optional.
# apply_funding_accrual uses only funding_rate and the position
# notional; None mark_price must NOT affect funding math.


def test_funding_accrual_works_with_none_mark_price() -> None:
    """An event with mark_price=None still accrues via funding_rate."""
    from prometheus.core.events import FundingRateEvent

    events = [
        FundingRateEvent(
            symbol=Symbol.BTCUSDT,
            funding_time=ANCHOR,
            funding_rate=0.0001,
            mark_price=None,  # pre-2024 upstream behavior
            source="test",
        )
    ]
    total, matched = apply_funding_accrual(
        direction_long=True,
        entry_fill_time_ms=ANCHOR - 1,
        exit_fill_time_ms=ANCHOR + 1,
        position_notional_usdt=1_000.0,
        funding_events=events,
    )
    # Expected: 1000 * 0.0001 * -1 = -0.1 (long pays positive-rate funding).
    assert len(matched) == 1
    assert total == pytest.approx(-0.1)


def test_funding_accrual_mixes_none_and_populated_mark_prices() -> None:
    """Pre-2024 (None) and 2024+ (populated) events coexist without special-casing."""
    from prometheus.core.events import FundingRateEvent

    events = [
        FundingRateEvent(
            symbol=Symbol.BTCUSDT,
            funding_time=ANCHOR,
            funding_rate=0.0001,
            mark_price=None,
            source="test",
        ),
        FundingRateEvent(
            symbol=Symbol.BTCUSDT,
            funding_time=ANCHOR + EIGHT_HOURS_MS,
            funding_rate=0.0002,
            mark_price=50_000.0,
            source="test",
        ),
    ]
    total, matched = apply_funding_accrual(
        direction_long=True,
        entry_fill_time_ms=ANCHOR - 1,
        exit_fill_time_ms=ANCHOR + EIGHT_HOURS_MS + 1,
        position_notional_usdt=1_000.0,
        funding_events=events,
    )
    assert len(matched) == 2
    # Sum: 1000 * (0.0001 + 0.0002) * -1 = -0.3
    assert total == pytest.approx(-0.3)
