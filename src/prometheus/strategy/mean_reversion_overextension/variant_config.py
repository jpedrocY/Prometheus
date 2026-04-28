"""F1 mean-reversion-after-overextension variant configuration.

Per the binding Phase 3b spec §4, F1 has a single locked rule per
axis with NO TUNING, NO ALTERNATIVES, and NO SWEEPS. This config
mirrors that lock: every field has a single locked value and any
attempt to override it raises :class:`ValueError` from
``model_post_init``.

Locked fields (Phase 3b §4):

    overextension_window_bars         = 8
    overextension_threshold_atr_multiple = 1.75
    mean_reference_window_bars        = 8
    stop_buffer_atr_multiple          = 0.10
    time_stop_bars                    = 8
    stop_distance_min_atr             = 0.60
    stop_distance_max_atr             = 1.80

These are the spec-locked values. Any future research that wishes
to vary them must do so through a separate variant config registered
under a different family/phase, not by mutating this model.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# Locked spec values (Phase 3b §4). These constants are the single
# source of truth for the F1 family.
OVEREXTENSION_WINDOW_BARS: int = 8
OVEREXTENSION_THRESHOLD_ATR_MULTIPLE: float = 1.75
MEAN_REFERENCE_WINDOW_BARS: int = 8
STOP_BUFFER_ATR_MULTIPLE: float = 0.10
TIME_STOP_BARS: int = 8
STOP_DISTANCE_MIN_ATR: float = 0.60
STOP_DISTANCE_MAX_ATR: float = 1.80


class MeanReversionConfig(BaseModel):
    """Locked F1 config — single-rule-per-axis, no tuning.

    Frozen pydantic model so it nests cleanly into
    ``prometheus.research.backtest.BacktestConfig`` and serializes
    into the run's ``config_snapshot.json``. Per Phase 3b §4 every
    field is locked at a single spec value; ``model_post_init``
    rejects any attempt to override.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    # Phase 3b §4 — overextension definition.
    # cumulative_displacement_<N>bar(B) = close(B) - close(B - N).
    # F1 fires iff abs(...) > threshold_atr_multiple * ATR(20)(B).
    overextension_window_bars: int = Field(
        default=OVEREXTENSION_WINDOW_BARS,
        ge=OVEREXTENSION_WINDOW_BARS,
        le=OVEREXTENSION_WINDOW_BARS,
    )
    overextension_threshold_atr_multiple: float = Field(
        default=OVEREXTENSION_THRESHOLD_ATR_MULTIPLE,
        ge=OVEREXTENSION_THRESHOLD_ATR_MULTIPLE,
        le=OVEREXTENSION_THRESHOLD_ATR_MULTIPLE,
    )

    # Phase 3b §4 — mean reference (frozen SMA on signal bar B).
    mean_reference_window_bars: int = Field(
        default=MEAN_REFERENCE_WINDOW_BARS,
        ge=MEAN_REFERENCE_WINDOW_BARS,
        le=MEAN_REFERENCE_WINDOW_BARS,
    )

    # Phase 3b §4 — protective stop buffer (multiplier on ATR(20) at B).
    stop_buffer_atr_multiple: float = Field(
        default=STOP_BUFFER_ATR_MULTIPLE,
        ge=STOP_BUFFER_ATR_MULTIPLE,
        le=STOP_BUFFER_ATR_MULTIPLE,
    )

    # Phase 3b §4 — unconditional time-stop horizon (15m bars from entry).
    time_stop_bars: int = Field(default=TIME_STOP_BARS, ge=TIME_STOP_BARS, le=TIME_STOP_BARS)

    # Phase 3b §4 — stop-distance admissibility band, in ATR(20) multiples.
    # Evaluated on the raw (de-slipped) open(B+1).
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

    def model_post_init(self, __context: object) -> None:
        # Belt-and-suspenders: reject any non-spec value even if the
        # Field constraints were ever relaxed in a refactor. Raising
        # ValueError here keeps the lock visible at the model level.
        if self.overextension_window_bars != OVEREXTENSION_WINDOW_BARS:
            raise ValueError(
                f"overextension_window_bars locked at "
                f"{OVEREXTENSION_WINDOW_BARS}; got {self.overextension_window_bars}"
            )
        if self.overextension_threshold_atr_multiple != OVEREXTENSION_THRESHOLD_ATR_MULTIPLE:
            raise ValueError(
                f"overextension_threshold_atr_multiple locked at "
                f"{OVEREXTENSION_THRESHOLD_ATR_MULTIPLE}; "
                f"got {self.overextension_threshold_atr_multiple}"
            )
        if self.mean_reference_window_bars != MEAN_REFERENCE_WINDOW_BARS:
            raise ValueError(
                f"mean_reference_window_bars locked at "
                f"{MEAN_REFERENCE_WINDOW_BARS}; got {self.mean_reference_window_bars}"
            )
        if self.stop_buffer_atr_multiple != STOP_BUFFER_ATR_MULTIPLE:
            raise ValueError(
                f"stop_buffer_atr_multiple locked at "
                f"{STOP_BUFFER_ATR_MULTIPLE}; got {self.stop_buffer_atr_multiple}"
            )
        if self.time_stop_bars != TIME_STOP_BARS:
            raise ValueError(
                f"time_stop_bars locked at {TIME_STOP_BARS}; got {self.time_stop_bars}"
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

    @classmethod
    def baseline(cls) -> MeanReversionConfig:
        """Return the locked baseline config; explicit alternative to ``cls()``."""
        return cls()
