from __future__ import annotations

import pytest
from pydantic import ValidationError

from prometheus.core.symbols import Symbol
from prometheus.strategy.types import (
    BreakoutSignal,
    Direction,
    EntryIntent,
    ExitIntent,
    ExitReason,
    SetupWindow,
    StopMoveStage,
    StopUpdateIntent,
    TrendBias,
)


def _valid_setup() -> SetupWindow:
    return SetupWindow(
        symbol=Symbol.BTCUSDT,
        first_bar_open_time=1_000_000,
        last_bar_open_time=1_000_000 + 7 * 15 * 60 * 1000,
        setup_high=102.0,
        setup_low=98.0,
        setup_range_width=4.0,
        net_drift_abs=0.5,
        atr_20_15m=3.0,
    )


def _valid_signal(direction: Direction = Direction.LONG) -> BreakoutSignal:
    setup = _valid_setup()
    return BreakoutSignal(
        symbol=Symbol.BTCUSDT,
        direction=direction,
        signal_bar_open_time=1_000_000 + 8 * 15 * 60 * 1000,
        signal_bar_close_time=1_000_000 + 9 * 15 * 60 * 1000 - 1,
        signal_bar_close=103.0,
        signal_bar_high=104.0,
        signal_bar_low=101.0,
        setup=setup,
        atr_20_15m=3.0,
        atr_20_1h=20.0,
        latest_1h_close=100.0,
        normalized_atr_1h=0.005,
        trend_bias=TrendBias.LONG if direction == Direction.LONG else TrendBias.SHORT,
    )


class TestSetupWindow:
    def test_rejects_first_after_last(self) -> None:
        with pytest.raises(ValidationError):
            SetupWindow(
                symbol=Symbol.BTCUSDT,
                first_bar_open_time=100,
                last_bar_open_time=100,
                setup_high=10.0,
                setup_low=9.0,
                setup_range_width=1.0,
                net_drift_abs=0.0,
                atr_20_15m=1.0,
            )

    def test_rejects_high_below_low(self) -> None:
        with pytest.raises(ValidationError):
            SetupWindow(
                symbol=Symbol.BTCUSDT,
                first_bar_open_time=100,
                last_bar_open_time=200,
                setup_high=5.0,
                setup_low=10.0,
                setup_range_width=5.0,
                net_drift_abs=0.0,
                atr_20_15m=1.0,
            )


class TestEntryIntent:
    def test_long_stop_must_be_below_reference(self) -> None:
        sig = _valid_signal(Direction.LONG)
        with pytest.raises(ValidationError):
            EntryIntent(
                symbol=Symbol.BTCUSDT,
                direction=Direction.LONG,
                signal=sig,
                reference_price=100.0,
                initial_stop=105.0,  # above entry: invalid for long
                stop_distance=5.0,
            )

    def test_short_stop_must_be_above_reference(self) -> None:
        sig = _valid_signal(Direction.SHORT)
        with pytest.raises(ValidationError):
            EntryIntent(
                symbol=Symbol.BTCUSDT,
                direction=Direction.SHORT,
                signal=sig,
                reference_price=100.0,
                initial_stop=95.0,  # below entry: invalid for short
                stop_distance=5.0,
            )

    def test_happy_long(self) -> None:
        sig = _valid_signal(Direction.LONG)
        ei = EntryIntent(
            symbol=Symbol.BTCUSDT,
            direction=Direction.LONG,
            signal=sig,
            reference_price=103.0,
            initial_stop=98.0,
            stop_distance=5.0,
        )
        assert ei.stop_distance == pytest.approx(5.0)


class TestStopUpdateIntent:
    def test_frozen(self) -> None:
        upd = StopUpdateIntent(
            symbol=Symbol.BTCUSDT,
            direction=Direction.LONG,
            new_stop=99.0,
            reason=StopMoveStage.STAGE_4_BREAK_EVEN,
            triggered_at_close_time=1_000_000,
        )
        with pytest.raises(ValidationError):
            upd.new_stop = 100.0  # type: ignore[misc]


class TestExitIntent:
    def test_valid(self) -> None:
        ex = ExitIntent(
            symbol=Symbol.BTCUSDT,
            direction=Direction.SHORT,
            reason=ExitReason.STAGNATION,
            triggering_bar_close_time=1_000_000,
        )
        assert ex.reason == ExitReason.STAGNATION
