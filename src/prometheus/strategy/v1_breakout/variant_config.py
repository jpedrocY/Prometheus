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

    def model_post_init(self, __context: object) -> None:
        if self.ema_fast >= self.ema_slow:
            raise ValueError(
                f"ema_fast ({self.ema_fast}) must be strictly less than ema_slow ({self.ema_slow})"
            )

    @classmethod
    def baseline(cls) -> V1BreakoutConfig:
        """Explicit baseline for call sites that want the intent documented."""
        return cls()
