"""Stage 2-7 trade management per v1-breakout-strategy-spec.md §"Exit Logic".

The management object is stateful per open position. It consumes
each completed 15m bar after entry and emits:

    - a StopUpdateIntent when a stage transition moves the stop
    - an ExitIntent when stagnation or trailing-breach fires
    - or None when no action is needed

Stop-widening is forbidden. The consumer must enforce the
risk-reducing-only invariant when applying updates, but this class
only issues updates that reduce risk in the correct direction.

Reference levels are computed in price terms from the initial R
(the per-trade risk magnitude at entry):

    R_long = entry_price - initial_stop
    R_short = initial_stop - entry_price

MFE = maximum favorable excursion since entry, in price terms.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from prometheus.core.klines import NormalizedKline

from ..types import (
    Direction,
    ExitIntent,
    ExitReason,
    StopMoveStage,
    StopUpdateIntent,
    TradeStage,
)

STAGE_3_MFE_R = 1.0
STAGE_3_NEW_STOP_R = -0.25  # new stop is 0.25R ADVERSE from entry (long: below entry, short: above)
STAGE_4_MFE_R = 1.5
STAGE_5_MFE_R = 2.0
TRAIL_ATR_MULT = 2.5
STAGNATION_BARS = 8
STAGNATION_MFE_THRESHOLD_R = 1.0


@dataclass
class TradeManagement:
    """Per-position management state.

    Usage:

        tm = TradeManagement.start(entry_price, initial_stop, direction, entry_time_ms)
        for bar in completed_bars_after_entry:
            result = tm.on_completed_bar(bar, atr_20_15m)
            ...

    Fields are not user-facing; use the factory and the public
    method ``on_completed_bar``.
    """

    symbol: Symbol  # noqa: F821 -- forward ref
    direction: Direction
    entry_price: float
    initial_stop: float
    r_magnitude: float  # abs(entry_price - initial_stop)
    current_stop: float
    stage: TradeStage = TradeStage.STAGE_2_INITIAL
    bars_in_trade: int = 0
    mfe_abs: float = 0.0  # max favorable excursion (price, positive)
    mae_abs: float = 0.0  # max adverse excursion (price, positive)
    highest_high_since_entry: float = field(default=0.0)
    lowest_low_since_entry: float = field(default=0.0)

    @classmethod
    def start(
        cls,
        *,
        symbol: Symbol,  # noqa: F821
        direction: Direction,
        entry_price: float,
        initial_stop: float,
        entry_bar_high: float,
        entry_bar_low: float,
    ) -> TradeManagement:
        """Construct a fresh management state immediately after entry fill.

        ``entry_bar_high`` and ``entry_bar_low`` are the high/low of
        the bar the trade was FILLED on (the bar after the signal
        bar). They seed the MFE/MAE trackers.
        """
        if direction == Direction.LONG:
            r = entry_price - initial_stop
        else:
            r = initial_stop - entry_price
        if r <= 0:
            raise ValueError(f"initial_stop on wrong side of entry for direction {direction.value}")
        tm = cls(
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            initial_stop=initial_stop,
            r_magnitude=r,
            current_stop=initial_stop,
            highest_high_since_entry=entry_bar_high,
            lowest_low_since_entry=entry_bar_low,
        )
        tm._update_excursions(entry_bar_high, entry_bar_low)
        return tm

    @property
    def mfe_r(self) -> float:
        if self.r_magnitude == 0:
            return 0.0
        return self.mfe_abs / self.r_magnitude

    @property
    def mae_r(self) -> float:
        if self.r_magnitude == 0:
            return 0.0
        return self.mae_abs / self.r_magnitude

    def _update_excursions(self, bar_high: float, bar_low: float) -> None:
        """Update MFE/MAE/trail reference levels with a new bar's high/low."""
        if bar_high > self.highest_high_since_entry:
            self.highest_high_since_entry = bar_high
        if bar_low < self.lowest_low_since_entry or self.lowest_low_since_entry == 0.0:
            # 0.0 is our "unset" sentinel at construction; replace it.
            self.lowest_low_since_entry = bar_low
        if self.direction == Direction.LONG:
            fav = bar_high - self.entry_price
            adv = self.entry_price - bar_low
        else:
            fav = self.entry_price - bar_low
            adv = bar_high - self.entry_price
        if fav > self.mfe_abs:
            self.mfe_abs = fav
        if adv > self.mae_abs:
            self.mae_abs = adv

    def _stage_3_new_stop(self) -> float:
        # New stop is 0.25R adverse from entry (long: entry - 0.25R; short: entry + 0.25R).
        # Wait — spec says "-0.25R" as the stop location. That means the
        # remaining risk from entry is 0.25R (a small loss if hit), not
        # 0.25R profit. For long: new_stop = entry - 0.25R (below entry).
        # For short: new_stop = entry + 0.25R (above entry).
        offset = 0.25 * self.r_magnitude
        if self.direction == Direction.LONG:
            return self.entry_price - offset
        return self.entry_price + offset

    def _trail_level(self, atr_20_15m: float) -> float:
        offset = TRAIL_ATR_MULT * atr_20_15m
        if self.direction == Direction.LONG:
            return self.highest_high_since_entry - offset
        return self.lowest_low_since_entry + offset

    def _update_stop_if_better(
        self, candidate: float, reason: StopMoveStage
    ) -> StopUpdateIntent | None:
        """Move the stop only if the candidate is RISK-REDUCING.

        Long: new stop must be strictly higher than current_stop.
        Short: new stop must be strictly lower than current_stop.
        If the candidate does not reduce risk, return None (no-op).
        """
        if self.direction == Direction.LONG and candidate <= self.current_stop:
            return None
        if self.direction == Direction.SHORT and candidate >= self.current_stop:
            return None
        self.current_stop = candidate
        return StopUpdateIntent(
            symbol=self.symbol,
            direction=self.direction,
            new_stop=candidate,
            reason=reason,
            triggered_at_close_time=0,  # filled by caller to the bar's close_time
        )

    def on_completed_bar(
        self,
        bar: NormalizedKline,
        atr_20_15m: float,
        *,
        break_even_r: float = STAGE_4_MFE_R,
    ) -> tuple[StopUpdateIntent | ExitIntent | None, ManagementBarDiagnostic]:
        """Process one completed 15m bar after the entry fill.

        ``break_even_r`` is the Stage-3 → Stage-4 MFE-R threshold that
        moves the stop to break-even. Defaults to the locked baseline
        (+1.5 R). Phase 2g H-D3 sets this to 2.0. Note that Stage 5
        (trailing activation at +2.0 R) is unchanged; setting
        ``break_even_r == STAGE_5_MFE_R`` collapses Stage 4 and Stage 5
        onto the same bar — a clean cascade, not a collision, because
        the risk-reducing-only guard in ``_update_stop_if_better``
        always picks the tighter candidate.

        Returns a tuple of (intent, diagnostic).
        """
        self.bars_in_trade += 1
        self._update_excursions(bar.high, bar.low)
        intent: StopUpdateIntent | ExitIntent | None = None

        # Stage transitions by MFE thresholds. Check them in order
        # so a single bar can cascade (e.g., a big bar that pushes
        # MFE from 0 to 2.5R promotes through Stage 3 -> 4 -> 5).
        if self.stage == TradeStage.STAGE_2_INITIAL and self.mfe_r >= STAGE_3_MFE_R:
            candidate = self._stage_3_new_stop()
            update = self._update_stop_if_better(candidate, StopMoveStage.STAGE_3_RISK_REDUCTION)
            if update is not None:
                intent = StopUpdateIntent(
                    symbol=update.symbol,
                    direction=update.direction,
                    new_stop=update.new_stop,
                    reason=update.reason,
                    triggered_at_close_time=bar.close_time,
                )
            self.stage = TradeStage.STAGE_3_RISK_REDUCED

        if self.stage == TradeStage.STAGE_3_RISK_REDUCED and self.mfe_r >= break_even_r:
            candidate = self.entry_price
            update = self._update_stop_if_better(candidate, StopMoveStage.STAGE_4_BREAK_EVEN)
            if update is not None:
                # If a stage 3 transition also fired this bar we
                # prefer the later (tighter) update.
                intent = StopUpdateIntent(
                    symbol=update.symbol,
                    direction=update.direction,
                    new_stop=update.new_stop,
                    reason=update.reason,
                    triggered_at_close_time=bar.close_time,
                )
            self.stage = TradeStage.STAGE_4_BREAK_EVEN

        if self.stage == TradeStage.STAGE_4_BREAK_EVEN and self.mfe_r >= STAGE_5_MFE_R:
            self.stage = TradeStage.STAGE_5_TRAILING
            candidate = self._trail_level(atr_20_15m)
            update = self._update_stop_if_better(candidate, StopMoveStage.STAGE_5_TRAIL)
            if update is not None:
                intent = StopUpdateIntent(
                    symbol=update.symbol,
                    direction=update.direction,
                    new_stop=update.new_stop,
                    reason=update.reason,
                    triggered_at_close_time=bar.close_time,
                )

        # Stage 5 trailing: each subsequent bar potentially tightens the trail.
        if self.stage == TradeStage.STAGE_5_TRAILING:
            candidate = self._trail_level(atr_20_15m)
            update = self._update_stop_if_better(candidate, StopMoveStage.STAGE_5_TRAIL)
            if update is not None and intent is None:
                intent = StopUpdateIntent(
                    symbol=update.symbol,
                    direction=update.direction,
                    new_stop=update.new_stop,
                    reason=update.reason,
                    triggered_at_close_time=bar.close_time,
                )
            # Stage 5 exit check: completed close beyond trail level.
            if self.direction == Direction.LONG and bar.close < self.current_stop:
                intent = ExitIntent(
                    symbol=self.symbol,
                    direction=self.direction,
                    reason=ExitReason.TRAILING_BREACH,
                    triggering_bar_close_time=bar.close_time,
                )
            if self.direction == Direction.SHORT and bar.close > self.current_stop:
                intent = ExitIntent(
                    symbol=self.symbol,
                    direction=self.direction,
                    reason=ExitReason.TRAILING_BREACH,
                    triggering_bar_close_time=bar.close_time,
                )

        # Stage 7 stagnation exit: bars_in_trade >= 8 with MFE < +1R.
        if (
            intent is None
            and self.bars_in_trade >= STAGNATION_BARS
            and self.mfe_r < STAGNATION_MFE_THRESHOLD_R
        ):
            intent = ExitIntent(
                symbol=self.symbol,
                direction=self.direction,
                reason=ExitReason.STAGNATION,
                triggering_bar_close_time=bar.close_time,
            )

        diag = ManagementBarDiagnostic(
            bars_in_trade=self.bars_in_trade,
            stage=self.stage,
            current_stop=self.current_stop,
            mfe_r=self.mfe_r,
            mae_r=self.mae_r,
        )
        return intent, diag


@dataclass(frozen=True)
class ManagementBarDiagnostic:
    """Per-bar diagnostic emitted alongside any intent.

    Useful for trade-log enrichment and tests.
    """

    bars_in_trade: int
    stage: TradeStage
    current_stop: float
    mfe_r: float
    mae_r: float


# For forward-ref type hints without circular imports.
from prometheus.core.symbols import Symbol  # noqa: E402, F401
