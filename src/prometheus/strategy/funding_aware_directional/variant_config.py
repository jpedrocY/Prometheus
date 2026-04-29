"""D1-A funding-aware directional / carry-aware variant configuration.

Per the binding Phase 3g spec §6 (with §5.6 RR/target sanity Option A
revising the target to +2.0R), D1-A has a single locked rule per axis
with NO TUNING, NO ALTERNATIVES, and NO SWEEPS. This config mirrors
that lock: every field has a single locked value and any attempt to
override it raises :class:`ValueError` from ``model_post_init``.

Locked fields (Phase 3g §6, §5.6.5):

    funding_z_score_threshold        = 2.0   (|Z_F| >= 2.0 contrarian)
    funding_z_score_lookback_days    = 90
    funding_z_score_lookback_events  = 270   (90d * 3 events/day)
    stop_distance_atr_multiplier     = 1.0   (stop = 1.0 * ATR(20))
    target_r_multiple                = 2.0   (R3 non-fitting convention)
    time_stop_bars                   = 32    (= 8h = one funding cycle)
    cooldown_rule                    = "per_funding_event"
    stop_distance_min_atr            = 0.60  (admissibility band)
    stop_distance_max_atr            = 1.80  (admissibility band)
    direction_logic                  = "contrarian"
    regime_filter                    = None  (no regime conditioning)

These are the spec-locked values. Any future research that wishes to
vary them must do so through a separate variant config registered
under a different family/phase, not by mutating this model.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# Locked spec values (Phase 3g §6 + §5.6.5). These constants are the
# single source of truth for the D1-A family.
FUNDING_Z_SCORE_THRESHOLD: float = 2.0
FUNDING_Z_SCORE_LOOKBACK_DAYS: int = 90
FUNDING_Z_SCORE_LOOKBACK_EVENTS: int = 270  # 90 days × 3 events/day on Binance USDⓈ-M
STOP_DISTANCE_ATR_MULTIPLIER: float = 1.0
TARGET_R_MULTIPLE: float = 2.0
TIME_STOP_BARS: int = 32  # 8 hours / 15 minutes per bar
STOP_DISTANCE_MIN_ATR: float = 0.60
STOP_DISTANCE_MAX_ATR: float = 1.80
COOLDOWN_RULE: Literal["per_funding_event"] = "per_funding_event"
DIRECTION_LOGIC: Literal["contrarian"] = "contrarian"


class FundingAwareConfig(BaseModel):
    """Locked D1-A config — single-rule-per-axis, no tuning.

    Frozen pydantic model so it nests cleanly into
    ``prometheus.research.backtest.BacktestConfig`` and serializes
    into the run's ``config_snapshot.json``. Per Phase 3g §6 every
    field is locked at a single spec value; ``model_post_init``
    rejects any attempt to override.

    The ``regime_filter`` field is intentionally absent (no regime
    conditioning per Phase 3g §6.13). ``model_config`` has
    ``extra="forbid"`` so any client attempting to pass a regime
    filter or any other unrecognized field will be rejected at
    construction time.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    # Phase 3g §6.1 — funding Z-score extreme threshold (|Z_F| >= 2.0).
    funding_z_score_threshold: float = Field(
        default=FUNDING_Z_SCORE_THRESHOLD,
        ge=FUNDING_Z_SCORE_THRESHOLD,
        le=FUNDING_Z_SCORE_THRESHOLD,
    )

    # Phase 3g §6.2 — trailing 90-day rolling Z-score lookback.
    funding_z_score_lookback_days: int = Field(
        default=FUNDING_Z_SCORE_LOOKBACK_DAYS,
        ge=FUNDING_Z_SCORE_LOOKBACK_DAYS,
        le=FUNDING_Z_SCORE_LOOKBACK_DAYS,
    )
    funding_z_score_lookback_events: int = Field(
        default=FUNDING_Z_SCORE_LOOKBACK_EVENTS,
        ge=FUNDING_Z_SCORE_LOOKBACK_EVENTS,
        le=FUNDING_Z_SCORE_LOOKBACK_EVENTS,
    )

    # Phase 3g §6.7 — protective stop distance = 1.0 × ATR(20) at fill.
    stop_distance_atr_multiplier: float = Field(
        default=STOP_DISTANCE_ATR_MULTIPLIER,
        ge=STOP_DISTANCE_ATR_MULTIPLIER,
        le=STOP_DISTANCE_ATR_MULTIPLIER,
    )

    # Phase 3g §6.8 + §5.6.5 — TARGET = +2.0R (revised from +1.0R via
    # RR/target sanity Option A using R3's non-fitting convention).
    target_r_multiple: float = Field(
        default=TARGET_R_MULTIPLE,
        ge=TARGET_R_MULTIPLE,
        le=TARGET_R_MULTIPLE,
    )

    # Phase 3g §6.9 — unconditional time-stop = 32 × 15m bars (= 8h =
    # one funding cycle).
    time_stop_bars: int = Field(default=TIME_STOP_BARS, ge=TIME_STOP_BARS, le=TIME_STOP_BARS)

    # Phase 3g §6.10 — per-funding-event cooldown (consume on entry,
    # require fresh event for same-direction re-entry).
    cooldown_rule: Literal["per_funding_event"] = Field(default=COOLDOWN_RULE)

    # Phase 3g §6.11 — stop-distance admissibility band [0.60, 1.80] × ATR.
    stop_distance_min_atr: float = Field(
        default=STOP_DISTANCE_MIN_ATR,
        ge=STOP_DISTANCE_MIN_ATR,
        le=STOP_DISTANCE_MIN_ATR,
    )
    stop_distance_max_atr: float = Field(
        default=STOP_DISTANCE_MAX_ATR,
        ge=STOP_DISTANCE_MAX_ATR,
        le=STOP_DISTANCE_MAX_ATR,
    )

    # Phase 3g §6.3 — contrarian direction (Z >= +2 -> SHORT; Z <= -2 -> LONG).
    direction_logic: Literal["contrarian"] = Field(default=DIRECTION_LOGIC)

    def model_post_init(self, __context: object) -> None:
        # Belt-and-suspenders: reject any non-spec value even if Field
        # constraints were ever relaxed. Raising ValueError here keeps
        # the lock visible at the model level.
        if self.funding_z_score_threshold != FUNDING_Z_SCORE_THRESHOLD:
            raise ValueError(
                f"funding_z_score_threshold locked at "
                f"{FUNDING_Z_SCORE_THRESHOLD}; got {self.funding_z_score_threshold}"
            )
        if self.funding_z_score_lookback_days != FUNDING_Z_SCORE_LOOKBACK_DAYS:
            raise ValueError(
                f"funding_z_score_lookback_days locked at "
                f"{FUNDING_Z_SCORE_LOOKBACK_DAYS}; got {self.funding_z_score_lookback_days}"
            )
        if self.funding_z_score_lookback_events != FUNDING_Z_SCORE_LOOKBACK_EVENTS:
            raise ValueError(
                f"funding_z_score_lookback_events locked at "
                f"{FUNDING_Z_SCORE_LOOKBACK_EVENTS}; got {self.funding_z_score_lookback_events}"
            )
        if self.stop_distance_atr_multiplier != STOP_DISTANCE_ATR_MULTIPLIER:
            raise ValueError(
                f"stop_distance_atr_multiplier locked at "
                f"{STOP_DISTANCE_ATR_MULTIPLIER}; got {self.stop_distance_atr_multiplier}"
            )
        if self.target_r_multiple != TARGET_R_MULTIPLE:
            raise ValueError(
                f"target_r_multiple locked at {TARGET_R_MULTIPLE} "
                f"(Phase 3g §5.6.5 Option A; R3 non-fitting convention); "
                f"got {self.target_r_multiple}"
            )
        if self.time_stop_bars != TIME_STOP_BARS:
            raise ValueError(
                f"time_stop_bars locked at {TIME_STOP_BARS} "
                f"(Phase 3g §6.9; one funding cycle); got {self.time_stop_bars}"
            )
        if self.cooldown_rule != COOLDOWN_RULE:
            raise ValueError(
                f"cooldown_rule locked at '{COOLDOWN_RULE}'; got '{self.cooldown_rule}'"
            )
        if self.stop_distance_min_atr != STOP_DISTANCE_MIN_ATR:
            raise ValueError(
                f"stop_distance_min_atr locked at "
                f"{STOP_DISTANCE_MIN_ATR}; got {self.stop_distance_min_atr}"
            )
        if self.stop_distance_max_atr != STOP_DISTANCE_MAX_ATR:
            raise ValueError(
                f"stop_distance_max_atr locked at "
                f"{STOP_DISTANCE_MAX_ATR}; got {self.stop_distance_max_atr}"
            )
        if self.direction_logic != DIRECTION_LOGIC:
            raise ValueError(
                f"direction_logic locked at '{DIRECTION_LOGIC}'; got '{self.direction_logic}'"
            )

    @classmethod
    def baseline(cls) -> FundingAwareConfig:
        """Return the locked baseline config; explicit alternative to ``cls()``."""
        return cls()
