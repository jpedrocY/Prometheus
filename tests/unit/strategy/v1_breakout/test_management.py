from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol
from prometheus.strategy.types import (
    Direction,
    ExitIntent,
    ExitReason,
    StopMoveStage,
    StopUpdateIntent,
    TradeStage,
)
from prometheus.strategy.v1_breakout.management import (
    STAGNATION_BARS,
    TRAIL_ATR_MULT,
    TradeManagement,
)

from ..conftest import ANCHOR_MS, kline


def _make_long_tm(entry: float = 100.0, stop: float = 99.0) -> TradeManagement:
    return TradeManagement.start(
        symbol=Symbol.BTCUSDT,
        direction=Direction.LONG,
        entry_price=entry,
        initial_stop=stop,
        entry_bar_high=100.2,
        entry_bar_low=99.8,
    )


def _bar(close: float, high: float, low: float, offset_bars: int = 1) -> object:
    return kline(
        open_time=ANCHOR_MS + offset_bars * 15 * 60 * 1000,
        open=close,
        high=high,
        low=low,
        close=close,
    )


class TestStart:
    def test_rejects_stop_on_wrong_side_long(self) -> None:
        with pytest.raises(ValueError):
            TradeManagement.start(
                symbol=Symbol.BTCUSDT,
                direction=Direction.LONG,
                entry_price=100.0,
                initial_stop=101.0,
                entry_bar_high=100.2,
                entry_bar_low=99.8,
            )

    def test_rejects_stop_on_wrong_side_short(self) -> None:
        with pytest.raises(ValueError):
            TradeManagement.start(
                symbol=Symbol.BTCUSDT,
                direction=Direction.SHORT,
                entry_price=100.0,
                initial_stop=99.0,
                entry_bar_high=100.2,
                entry_bar_low=99.8,
            )

    def test_happy_long(self) -> None:
        tm = _make_long_tm()
        assert tm.r_magnitude == pytest.approx(1.0)
        assert tm.current_stop == pytest.approx(99.0)
        assert tm.stage == TradeStage.STAGE_2_INITIAL


class TestStageTransitions:
    def test_stage_2_holds_below_1R(self) -> None:
        tm = _make_long_tm()
        bar = _bar(close=100.5, high=100.8, low=100.3)
        intent, diag = tm.on_completed_bar(bar, atr_20_15m=1.0)
        # MFE = 0.8 -> 0.8R < 1.0R
        assert intent is None
        assert diag.stage == TradeStage.STAGE_2_INITIAL
        assert tm.current_stop == pytest.approx(99.0)

    def test_stage_3_transition_at_1R(self) -> None:
        tm = _make_long_tm()
        bar = _bar(close=101.1, high=101.2, low=100.9)  # MFE = 1.2R
        intent, diag = tm.on_completed_bar(bar, atr_20_15m=1.0)
        # Stop should move from 99.0 to entry - 0.25R = 99.75.
        assert isinstance(intent, StopUpdateIntent)
        assert intent.reason == StopMoveStage.STAGE_3_RISK_REDUCTION
        assert intent.new_stop == pytest.approx(99.75)
        assert tm.stage == TradeStage.STAGE_3_RISK_REDUCED

    def test_stage_4_break_even_at_1_5R(self) -> None:
        tm = _make_long_tm()
        # Push through stages: set MFE to 1.6R in one bar.
        bar = _bar(close=101.5, high=101.6, low=100.0)
        intent, diag = tm.on_completed_bar(bar, atr_20_15m=1.0)
        # Cascade: stage 3 then stage 4. The stop ends at break-even = entry = 100.0.
        assert isinstance(intent, StopUpdateIntent)
        assert intent.reason == StopMoveStage.STAGE_4_BREAK_EVEN
        assert intent.new_stop == pytest.approx(100.0)
        assert tm.stage == TradeStage.STAGE_4_BREAK_EVEN

    def test_stage_5_trail_activates_at_2R(self) -> None:
        tm = _make_long_tm()
        bar = _bar(close=102.1, high=102.2, low=100.0)  # MFE = 2.2R
        intent, diag = tm.on_completed_bar(bar, atr_20_15m=1.0)
        # Stage cascade through 3 -> 4 -> 5. Stage reaches STAGE_5_TRAILING.
        # But trail level (high - 2.5*ATR = 99.7) is WORSE than break-even
        # (100.0), so the risk-reducing-only guard keeps current_stop at
        # break-even and the emitted intent is the stage-4 break-even update.
        assert tm.stage == TradeStage.STAGE_5_TRAILING
        assert isinstance(intent, StopUpdateIntent)
        assert intent.new_stop == pytest.approx(100.0)
        assert intent.reason == StopMoveStage.STAGE_4_BREAK_EVEN

    def test_stage_5_trail_does_raise_stop_when_favorable(self) -> None:
        tm = _make_long_tm()
        # Bar 1: push MFE to 3.5R with a big body; trail level = 103.5 - 2.5 = 101.0 > 100.0 BE.
        bar = _bar(close=103.4, high=103.5, low=100.0)
        intent, _ = tm.on_completed_bar(bar, atr_20_15m=1.0)
        assert tm.stage == TradeStage.STAGE_5_TRAILING
        assert isinstance(intent, StopUpdateIntent)
        assert intent.reason == StopMoveStage.STAGE_5_TRAIL
        assert intent.new_stop == pytest.approx(103.5 - TRAIL_ATR_MULT * 1.0)


class TestStagnationExit:
    def test_stagnation_fires_at_8_bars_without_1R(self) -> None:
        tm = _make_long_tm()
        # 8 bars with MFE never reaching 1R.
        last_intent = None
        for i in range(STAGNATION_BARS):
            b = _bar(close=100.3, high=100.5, low=99.9, offset_bars=i + 1)
            last_intent, diag = tm.on_completed_bar(b, atr_20_15m=1.0)
        assert isinstance(last_intent, ExitIntent)
        assert last_intent.reason == ExitReason.STAGNATION

    def test_no_stagnation_if_1R_reached(self) -> None:
        tm = _make_long_tm()
        # Bar 1 reaches +1R.
        first, _ = tm.on_completed_bar(
            _bar(close=101.1, high=101.2, low=100.9, offset_bars=1), atr_20_15m=1.0
        )
        assert isinstance(first, StopUpdateIntent)
        # 7 more quiet bars; stagnation should NOT fire because MFE was reached.
        for i in range(2, STAGNATION_BARS + 2):
            result, _ = tm.on_completed_bar(
                _bar(close=100.5, high=100.8, low=100.3, offset_bars=i),
                atr_20_15m=1.0,
            )
            assert not isinstance(result, ExitIntent)


class TestTrailingExit:
    def test_trailing_breach_fires_after_stage_5(self) -> None:
        tm = _make_long_tm()
        # Bar 1: MFE hits 2.2R
        tm.on_completed_bar(_bar(close=102.1, high=102.2, low=100.0, offset_bars=1), atr_20_15m=1.0)
        # At this point stage=5, current_stop remains at break-even 100 (trail 99.7 < 100 rejected)
        # Bar 2: high=102.3 -> trail = 102.3-2.5=99.8 still < 100.
        tm.on_completed_bar(_bar(close=102.1, high=102.3, low=101.5, offset_bars=2), atr_20_15m=1.0)
        # Bar 3: close < current_stop=100 triggers trailing breach.
        intent, _ = tm.on_completed_bar(
            _bar(close=99.5, high=102.0, low=99.5, offset_bars=3), atr_20_15m=1.0
        )
        assert isinstance(intent, ExitIntent)
        assert intent.reason == ExitReason.TRAILING_BREACH


class TestRiskReducingOnlyInvariant:
    def test_stop_never_moves_adversely_on_long(self) -> None:
        tm = _make_long_tm()
        # Force stage 3 first (stop -> 99.75).
        tm.on_completed_bar(_bar(close=101.1, high=101.2, low=100.9, offset_bars=1), atr_20_15m=1.0)
        assert tm.current_stop == pytest.approx(99.75)
        # A subsequent small bar with MFE <1.5R should not emit an update
        # and should not move the stop adversely.
        intent, _ = tm.on_completed_bar(
            _bar(close=101.0, high=101.1, low=100.0, offset_bars=2), atr_20_15m=1.0
        )
        assert intent is None
        assert tm.current_stop == pytest.approx(99.75)
