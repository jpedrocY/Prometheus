"""V1 breakout strategy variant configuration.

Defaults reproduce the locked Phase 2e baseline (H0) bit-for-bit.
Phase 2g wave-1 variants override exactly one field each per the
approved Gate 1 plan:

    H-A1 -> setup_size          (baseline 8  -> 10)
    H-B2 -> expansion_atr_mult  (baseline 1.0 -> 0.75)
    H-C1 -> ema_fast / ema_slow (baseline 50/200 -> 20/100)
    H-D3 -> break_even_r        (baseline 1.5 -> 2.0)

Phase 2l (R3 — Fixed-R exit with time stop) adds three exit-machinery
fields. ``exit_kind`` selects between H0's staged-trailing topology
(default; STAGED_TRAILING) and R3's two-rule terminal exit
(FIXED_R_TIME_STOP). The two R3 sub-parameters are committed singularly
per Phase 2j memo §D.6:

    exit_r_target = 2.0  R-target multiple for take-profit
    exit_time_stop_bars = 8  unconditional time-stop horizon (15m bars)

Phase 2m (R1a — Volatility-percentile setup) adds three setup-validity
fields. ``setup_predicate_kind`` selects between H0's range-based
predicate (default; RANGE_BASED) and R1a's percentile-based predicate
(VOLATILITY_PERCENTILE). The two R1a sub-parameters are committed
singularly per Phase 2j memo §C.6:

    setup_percentile_threshold = 25  bottom-quartile cutoff
    setup_percentile_lookback  = 200 trailing-bars distribution length

Phase 2s (R1b-narrow — Bias-strength redesign) adds one bias-validity
field. ``bias_slope_strength_threshold`` extends H0's binary slope-3
direction-sign check with a magnitude threshold per Phase 2r spec
memo §F. Default 0.0 dispatches to H0's bit-for-bit binary predicate;
non-zero opts in to R1b-narrow's magnitude check. The committed
R1b-narrow value is 0.0020 (= 0.20%), anchored to the project's
existing ``ATR_REGIME_MIN`` constant.

Phase 2w (R2 — Pullback-retest entry) adds one entry-lifecycle field.
``entry_kind`` selects between H0's locked market-on-next-bar-open
fill (default; MARKET_NEXT_BAR_OPEN) and R2's conditional-pending
pullback-retest topology (PULLBACK_RETEST). Per Phase 2u spec memo §F
the four R2 sub-parameters (pullback level, confirmation rule, validity
window, fill model) are committed singularly and hard-coded in the R2
entry-lifecycle module — they are NOT exposed as config fields, to
prevent parameter drift. Default MARKET_NEXT_BAR_OPEN preserves
H0 / R3 / R1a / R1b-narrow behavior bit-for-bit through the strategy
facade and the backtest engine.

Any instance constructed with all defaults produces the baseline H0
behavior exactly; see ``tests/unit/strategy/v1_breakout/test_variant_config.py``.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ExitKind(StrEnum):
    """Selects the trade-management exit philosophy.

    STAGED_TRAILING is H0's locked Phase 2e baseline (Stage 3 risk
    reduction at +1.0 R, Stage 4 break-even at +1.5 R, Stage 5
    trailing at +2.0 R, Stage 7 stagnation at 8 bars + MFE < +1.0 R).
    FIXED_R_TIME_STOP is R3 per Phase 2j memo §D: stop never moved,
    take-profit at +R_TARGET R, unconditional time-stop at TIME_STOP_BARS.
    """

    STAGED_TRAILING = "STAGED_TRAILING"
    FIXED_R_TIME_STOP = "FIXED_R_TIME_STOP"


class SetupPredicateKind(StrEnum):
    """Selects the setup-validity predicate.

    RANGE_BASED is H0's locked Phase 2e baseline (range_width <= 1.75 *
    ATR(20) on 15m AND |close[-1] - open[-8]| <= 0.35 * range_width).
    VOLATILITY_PERCENTILE is R1a per Phase 2j memo §C: setup is valid
    iff the 15m ATR(20) at close of bar B-1 is in the bottom X-th
    percentile of the trailing N-bar ATR distribution.
    """

    RANGE_BASED = "RANGE_BASED"
    VOLATILITY_PERCENTILE = "VOLATILITY_PERCENTILE"


class EntryKind(StrEnum):
    """Selects the entry-lifecycle topology.

    MARKET_NEXT_BAR_OPEN is H0's locked Phase 2e baseline: the engine
    fills a market order at the next 15m bar's open immediately after
    a breakout-bar signal closes. This default preserves H0 / R3 /
    R1a / R1b-narrow behavior bit-for-bit.

    PULLBACK_RETEST is R2 per Phase 2u spec memo §B / §E (Gate 2
    amended): the engine registers a PendingCandidate at signal close
    and waits up to 8 completed 15m bars for a pullback-retest of the
    setup boundary. The fill triggers when the bar's low touches
    setup_high (LONG) or high touches setup_low (SHORT) AND the bar's
    close is on the breakout-side of the structural-stop level. The
    fill is a market order at the NEXT bar's open after confirmation.
    Cancellation precedence: BIAS_FLIP > OPPOSITE_SIGNAL >
    STRUCTURAL_INVALIDATION > TOUCH+CONFIRMATION > CONTINUE.
    """

    MARKET_NEXT_BAR_OPEN = "MARKET_NEXT_BAR_OPEN"
    PULLBACK_RETEST = "PULLBACK_RETEST"


class V1BreakoutConfig(BaseModel):
    """Tunable parameters for the v1 breakout strategy.

    Frozen pydantic model so it nests cleanly into
    ``prometheus.research.backtest.BacktestConfig`` and serializes
    into the run's ``config_snapshot.json``.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    # H-A1 axis. Baseline 8. Window is the N bars strictly BEFORE the breakout bar.
    setup_size: int = Field(default=8, gt=1, le=20)

    # H-B2 axis. Baseline 1.0. Multiplier on 15m ATR(20) for the breakout-bar TR gate.
    expansion_atr_mult: float = Field(default=1.0, gt=0.0, le=5.0)

    # H-C1 axis. Baseline 50/200. Fast must be strictly less than slow.
    ema_fast: int = Field(default=50, gt=0, le=500)
    ema_slow: int = Field(default=200, gt=0, le=500)

    # H-D3 axis. Baseline 1.5 R. Stage-4 break-even MFE trigger; Stage-5 trailing
    # is still gated by the separate +2.0 R threshold in management.py, so setting
    # break_even_r == 2.0 collapses Stage-4 and Stage-5 onto the same bar (clean
    # cascade; no collision).
    break_even_r: float = Field(default=1.5, gt=0.0, le=5.0)

    # R3 exit-philosophy axis. Default = STAGED_TRAILING preserves H0 bit-for-bit.
    # The two sub-parameters apply only when exit_kind == FIXED_R_TIME_STOP and are
    # ignored under STAGED_TRAILING (which uses the management-module constants).
    exit_kind: ExitKind = ExitKind.STAGED_TRAILING
    exit_r_target: float = Field(default=2.0, gt=0.0, le=10.0)
    exit_time_stop_bars: int = Field(default=8, gt=0, le=200)

    # R1a setup-predicate axis. Default = RANGE_BASED preserves H0 bit-for-bit.
    # The two sub-parameters apply only when setup_predicate_kind ==
    # VOLATILITY_PERCENTILE and are ignored under RANGE_BASED (which uses the
    # setup-module constants MAX_RANGE_ATR_MULT and MAX_DRIFT_RATIO).
    setup_predicate_kind: SetupPredicateKind = SetupPredicateKind.RANGE_BASED
    setup_percentile_threshold: int = Field(default=25, gt=0, lt=100)
    setup_percentile_lookback: int = Field(default=200, gt=0, le=2000)

    # R1b-narrow bias-strength axis. Default 0.0 dispatches to H0's strict
    # binary direction-sign slope-3 check (bit-for-bit preservation per
    # Phase 2r spec memo §J sentinel pattern). Non-zero opts in to the
    # magnitude check: LONG iff slope_strength_3 >= +threshold; SHORT iff
    # slope_strength_3 <= -threshold; where slope_strength_3 = (EMA(50)[now]
    # - EMA(50)[now-3]) / EMA(50)[now]. The committed R1b-narrow value is
    # 0.0020 (= 0.20%), anchored to the project's existing ATR_REGIME_MIN
    # constant in trigger.py per Phase 2r spec memo §F. Field constraint
    # le=0.10 is conservative; the spec only commits a single value.
    bias_slope_strength_threshold: float = Field(default=0.0, ge=0.0, le=0.10)

    # R2 entry-lifecycle axis (Phase 2u, Gate 2 amended). Default
    # MARKET_NEXT_BAR_OPEN preserves H0 / R3 / R1a / R1b-narrow
    # behavior bit-for-bit. PULLBACK_RETEST opts in to R2's
    # conditional-pending pullback-retest topology with sub-parameters
    # committed singularly per Phase 2u §F (pullback level =
    # setup_high/setup_low; confirmation = close not violating
    # structural stop; validity window = 8 bars; fill model =
    # next-bar-open after confirmation). The four R2 sub-parameters
    # are intentionally NOT exposed as config fields — they are
    # hard-coded in entry_lifecycle.py and the engine to prevent
    # parameter drift toward sweeps. The diagnostic-only
    # limit-at-pullback intrabar fill model lives behind a runner-
    # script flag in 2w-B (not Phase 2w-A scope), never as a config
    # field.
    entry_kind: EntryKind = EntryKind.MARKET_NEXT_BAR_OPEN

    def model_post_init(self, __context: object) -> None:
        if self.ema_fast >= self.ema_slow:
            raise ValueError(
                f"ema_fast ({self.ema_fast}) must be strictly less than ema_slow ({self.ema_slow})"
            )

    @classmethod
    def baseline(cls) -> V1BreakoutConfig:
        """Explicit baseline for call sites that want the intent documented."""
        return cls()
