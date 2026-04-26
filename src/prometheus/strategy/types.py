"""Strategy-layer typed intents and shared enums.

Intents are pure, frozen, validated Pydantic models. A strategy
function returns an intent; the consumer decides how to act.

Per docs/03-strategy-research/v1-breakout-strategy-spec.md and
docs/08-architecture/codebase-structure.md §"Strategy boundary rule".
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from prometheus.core.symbols import Symbol


class Direction(StrEnum):
    """Position direction."""

    LONG = "LONG"
    SHORT = "SHORT"


class TrendBias(StrEnum):
    """Higher-timeframe bias state.

    Per v1-breakout-strategy-spec.md §"Higher-Timeframe Trend Bias".
    """

    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"


class StopMoveStage(StrEnum):
    """Which management stage is issuing a stop update.

    Per v1-breakout-strategy-spec.md §"Exit Logic".
    """

    STAGE_3_RISK_REDUCTION = "STAGE_3_RISK_REDUCTION"
    STAGE_4_BREAK_EVEN = "STAGE_4_BREAK_EVEN"
    STAGE_5_TRAIL = "STAGE_5_TRAIL"


class ExitReason(StrEnum):
    """Why a strategy-managed exit fires.

    STOP, TRAILING_BREACH, STAGNATION are per the H0 staged-trailing
    exit philosophy (v1-breakout-strategy-spec.md §"Stage 5" and
    §"Stage 7"). TAKE_PROFIT and TIME_STOP are per the R3 fixed-R
    exit philosophy (Phase 2j memo §D, exit_kind=FIXED_R_TIME_STOP).
    END_OF_DATA is a backtest-only terminator for trades still open
    at the end of the simulation window.
    """

    STOP = "STOP"
    TRAILING_BREACH = "TRAILING_BREACH"
    STAGNATION = "STAGNATION"
    TAKE_PROFIT = "TAKE_PROFIT"
    TIME_STOP = "TIME_STOP"
    END_OF_DATA = "END_OF_DATA"


class TradeStage(StrEnum):
    """Trade management stage per v1-breakout-strategy-spec.md §"Exit Logic"."""

    STAGE_2_INITIAL = "STAGE_2_INITIAL"
    STAGE_3_RISK_REDUCED = "STAGE_3_RISK_REDUCED"
    STAGE_4_BREAK_EVEN = "STAGE_4_BREAK_EVEN"
    STAGE_5_TRAILING = "STAGE_5_TRAILING"


class SetupWindow(BaseModel):
    """Detected 8-bar consolidation window.

    Per v1-breakout-strategy-spec.md §"Setup / Consolidation Rules".
    Identified by the open_time of the FIRST bar in the window
    (oldest of the 8).
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    first_bar_open_time: int
    last_bar_open_time: int
    setup_high: float
    setup_low: float
    setup_range_width: float
    net_drift_abs: float  # abs(close[-1] - open[-8])
    atr_20_15m: float  # 15m ATR(20) evaluated at last_bar's close

    @model_validator(mode="after")
    def _check(self) -> SetupWindow:
        if self.first_bar_open_time >= self.last_bar_open_time:
            raise ValueError("first_bar_open_time must be strictly before last_bar_open_time")
        if self.setup_high < self.setup_low:
            raise ValueError("setup_high must be >= setup_low")
        if self.setup_range_width < 0:
            raise ValueError("setup_range_width must be non-negative")
        if self.atr_20_15m <= 0:
            raise ValueError("atr_20_15m must be strictly positive")
        return self


class BreakoutSignal(BaseModel):
    """A validated breakout signal (long or short), produced at the
    close of the breakout 15m bar.

    Per v1-breakout-strategy-spec.md §"Entry Trigger Rules". The
    signal captures both the decision and the input conditions that
    justify it, for audit and evidence.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    direction: Direction
    signal_bar_open_time: int  # breakout bar's open_time (UTC ms)
    signal_bar_close_time: int  # breakout bar's close_time (UTC ms)
    signal_bar_close: float
    signal_bar_high: float
    signal_bar_low: float
    setup: SetupWindow
    atr_20_15m: float
    atr_20_1h: float
    latest_1h_close: float
    normalized_atr_1h: float  # ATR(20)_1h / latest_1h_close
    trend_bias: TrendBias


class EntryIntent(BaseModel):
    """Strategy says: I'd like to enter a position with these parameters.

    The consumer (backtest engine or live execution layer) applies
    sizing, rounding, fill model, and actually "makes it happen."
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    direction: Direction
    signal: BreakoutSignal
    # Reference price for pre-fill sizing/filter decisions: the
    # signal-bar close, per operator-approved ambiguity A2
    # (GAP-20260419-015).
    reference_price: float
    initial_stop: float
    stop_distance: float = Field(gt=0)  # abs(reference_price - initial_stop)

    @model_validator(mode="after")
    def _check(self) -> EntryIntent:
        if self.reference_price <= 0:
            raise ValueError("reference_price must be strictly positive")
        if self.initial_stop <= 0:
            raise ValueError("initial_stop must be strictly positive")
        if self.direction == Direction.LONG:
            if self.initial_stop >= self.reference_price:
                raise ValueError("long initial_stop must be below reference_price")
        else:
            if self.initial_stop <= self.reference_price:
                raise ValueError("short initial_stop must be above reference_price")
        return self


class StopUpdateIntent(BaseModel):
    """Strategy says: move the protective stop to this new level.

    Stop widening is forbidden (docs/07-risk/stop-loss-policy.md).
    The consumer must enforce the risk-reducing-only invariant when
    applying the update.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    direction: Direction
    new_stop: float = Field(gt=0)
    reason: StopMoveStage
    triggered_at_close_time: int  # close_time of the 15m bar that triggered the stage change


class ExitIntent(BaseModel):
    """Strategy says: close the position at the next available price.

    The consumer decides the exact fill (next-bar-open per approved
    ambiguity A3, GAP-20260419-016).
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    direction: Direction
    reason: ExitReason
    triggering_bar_close_time: int
