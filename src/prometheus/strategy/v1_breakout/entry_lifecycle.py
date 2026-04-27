"""R2 (pullback-retest entry) lifecycle module.

Phase 2u spec memo §B / §E (Gate 2 amended) committed:

    - Pullback level = setup.setup_high (LONG) / setup.setup_low (SHORT).
    - Confirmation rule = close not violating structural-stop level.
    - Validity window = 8 completed 15m bars after registration.
    - Committed fill model = next-bar-open after confirmation.
    - Cancellation precedence (5-step, first-match wins):
        1. BIAS_FLIP
        2. OPPOSITE_SIGNAL
        3. STRUCTURAL_INVALIDATION
        4. TOUCH + CONFIRMATION
        5. CONTINUE

The four R2 sub-parameters above are committed singularly per Phase 2u
§F with non-fitting rationale anchored to existing project conventions:

    - setup_high / setup_low ↔ H0 setup-validity rule's structural reference.
    - structural_stop_level ↔ H0 ``compute_initial_stop()`` output.
    - 8 bars ↔ ``setup_size = 8`` AND ``exit_time_stop_bars = 8``.
    - next-bar-open ↔ H0 market-on-next-bar-open convention.

This module exposes:

    - ``PendingCandidate`` — frozen record of a registered candidate.
    - ``CancellationReason`` — enum for terminal-non-fill outcomes.
    - ``PendingEvaluation`` — enum for per-bar-close outcomes.
    - ``R2_VALIDITY_WINDOW_BARS = 8`` — module-level constant.
    - ``evaluate_pending_candidate`` — pure predicate per §E.2.
    - ``evaluate_fill_at_next_bar_open`` — pure predicate per §E.3.

The committed fill model is hard-coded; no fill-model field is
exposed on ``V1BreakoutConfig``. The diagnostic-only limit-at-pullback
intrabar fill model lives behind a runner-script flag in 2w-B, never
as a config field (Phase 2v Gate 2 clarification).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from prometheus.core.klines import NormalizedKline
from prometheus.strategy.types import BreakoutSignal, Direction, TrendBias

# Validity window committed singularly per Phase 2u §F.3. Anchored to
# both ``SETUP_SIZE = 8`` (H0 setup-window length) AND
# ``exit_time_stop_bars = 8`` (R3 unconditional time-stop horizon) —
# the strongest non-fitting anchor available for the R2 axes.
R2_VALIDITY_WINDOW_BARS = 8


class CancellationReason(StrEnum):
    """Terminal-non-fill outcomes for a PendingCandidate.

    Each cancellation outcome corresponds to one of the per-bar
    cancellation predicates per Phase 2u §E.2 (Gate 2 amended), or
    to the validity-window expiry per §E.4, or to the fill-time
    stop-distance filter per §E.3.
    """

    BIAS_FLIP = "BIAS_FLIP"
    OPPOSITE_SIGNAL = "OPPOSITE_SIGNAL"
    STRUCTURAL_INVALIDATION = "STRUCTURAL_INVALIDATION"
    STOP_DISTANCE_AT_FILL = "STOP_DISTANCE_AT_FILL"
    VALIDITY_WINDOW_ELAPSED = "VALIDITY_WINDOW_ELAPSED"


class PendingEvaluation(StrEnum):
    """Per-bar-close outcome of evaluating a PendingCandidate.

    Returned by ``evaluate_pending_candidate``. The five values map
    1:1 to the 5-step precedence in Phase 2u §E.2 (Gate 2 amended):

        1. CANCEL_BIAS_FLIP        — bias_at_t != candidate.direction
        2. CANCEL_OPPOSITE_SIGNAL  — opposite-direction trigger fires at bar t
        3. CANCEL_STRUCTURAL_INVALIDATION
                                   — close_t crosses structural_stop_level
        4. READY_TO_FILL           — touch + confirmation jointly fire
        5. CONTINUE                — none of the above; remain pending
    """

    CANCEL_BIAS_FLIP = "CANCEL_BIAS_FLIP"
    CANCEL_OPPOSITE_SIGNAL = "CANCEL_OPPOSITE_SIGNAL"
    CANCEL_STRUCTURAL_INVALIDATION = "CANCEL_STRUCTURAL_INVALIDATION"
    READY_TO_FILL = "READY_TO_FILL"
    CONTINUE = "CONTINUE"


@dataclass(frozen=True)
class PendingCandidate:
    """Frozen snapshot of a registered R2 candidate.

    All values are captured at the close of the breakout-bar B (the
    registration bar) and held immutable through evaluation. The
    structural-stop level and ATR-at-signal are explicitly frozen to
    preserve H0's GAP-20260419-015 no-look-ahead convention: stop
    distance at fill time uses the snapshot ATR, not a recomputed
    value at the fill bar.

    Fields:

        direction:                 LONG | SHORT
        registration_bar_index:    integer index of bar B in the per-symbol
                                   15m kline sequence (engine-side reference)
        registration_bar_open_time:UTC ms; bar B's open_time
        pullback_level:            setup.setup_high (LONG) / setup_low (SHORT)
        structural_stop_level:     ``compute_initial_stop()`` output at B
        atr_at_signal:             15m ATR(20) at close of B (frozen)
        validity_expires_at_index: registration_bar_index + R2_VALIDITY_WINDOW_BARS;
                                   the last bar eligible for fill-evaluation is
                                   this index inclusive
        signal_bar_open_time_ms:   bar B's open_time (for trade-record provenance)
        signal_bar_close_time_ms:  bar B's close_time (for trade-record provenance)
        next_bar_open_at_signal:   open price at bar B+1 (for §P.3
                                   stop-distance reduction diagnostic against
                                   the R3 would-have-entered-at price)
    """

    direction: Direction
    registration_bar_index: int
    registration_bar_open_time: int
    pullback_level: float
    structural_stop_level: float
    atr_at_signal: float
    validity_expires_at_index: int
    signal_bar_open_time_ms: int
    signal_bar_close_time_ms: int
    next_bar_open_at_signal: float
    # The original H0 trigger output. Carried so the engine can pass
    # it to ``StrategySession.on_entry_filled`` at fill time without
    # constructing a synthetic placeholder. Kept frozen alongside the
    # other registration-time snapshots.
    signal: BreakoutSignal

    def is_within_validity(self, bar_index: int) -> bool:
        """True if bar_index is in the per-bar evaluation window (B, B+8].

        Bar B itself (registration bar) is not evaluated; bars
        B+1..B+8 are. Bar B+9 and beyond trigger validity-window
        expiry per §E.4.
        """
        return self.registration_bar_index < bar_index <= self.validity_expires_at_index

    def is_expired(self, bar_index: int) -> bool:
        """True if bar_index is strictly past the validity window.

        At bar B+9 (one bar after the last eligible bar), the candidate
        is considered EXPIRED per §E.4 if no FILL or CANCEL has fired.
        """
        return bar_index > self.validity_expires_at_index


@dataclass(frozen=True)
class FillEvaluation:
    """Outcome of ``evaluate_fill_at_next_bar_open`` per Phase 2u §E.3.

    Either FILL with a fill price, or CANCEL_STOP_DISTANCE_AT_FILL
    (no fill; candidate consumed). The fill-time stop-distance filter
    re-applies the same ``[0.60, 1.80] × atr_at_signal`` band that
    H0 applies at signal time; the only difference is the reference
    price (actual fill_price under R2 vs signal-bar close under H0).
    """

    fill: bool
    fill_price: float | None
    fill_stop_distance: float | None
    cancellation_reason: CancellationReason | None


def evaluate_pending_candidate(
    candidate: PendingCandidate,
    bar: NormalizedKline,
    bias_at_bar: TrendBias,
    opposite_signal_fires: bool,
) -> PendingEvaluation:
    """Per-bar-close evaluation of a PendingCandidate per Phase 2u §E.2.

    5-step precedence (first-match wins):

        1. BIAS_FLIP — bias_at_bar != candidate.direction
        2. OPPOSITE_SIGNAL — opposite_signal_fires is True
        3. STRUCTURAL_INVALIDATION — close_t crosses structural_stop_level
              LONG:  close_t <= structural_stop_level
              SHORT: close_t >= structural_stop_level
        4. TOUCH + CONFIRMATION — touch + close-not-violating-stop
              LONG:  low_t <= pullback_level AND close_t > structural_stop_level
              SHORT: high_t >= pullback_level AND close_t < structural_stop_level
        5. CONTINUE — none of the above

    The confirmation predicate at step 4 is mechanically redundant
    given step 3 precedence (any bar reaching step 4 has already been
    verified close-on-the-breakout-side), but it is kept in the rule
    for symmetry per Phase 2u §E.2 amendment rationale.

    The caller is responsible for checking
    ``candidate.is_within_validity(bar_index)`` before calling this
    function. Out-of-window bars should produce a
    VALIDITY_WINDOW_ELAPSED expiry directly, not flow through this
    evaluator.
    """
    # Step 1: BIAS_FLIP
    if bias_at_bar != _bias_for_direction(candidate.direction):
        return PendingEvaluation.CANCEL_BIAS_FLIP

    # Step 2: OPPOSITE_SIGNAL
    if opposite_signal_fires:
        return PendingEvaluation.CANCEL_OPPOSITE_SIGNAL

    # Step 3: STRUCTURAL_INVALIDATION (Phase 2v Gate 2 amendment)
    if candidate.direction == Direction.LONG:
        if bar.close <= candidate.structural_stop_level:
            return PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION
    else:  # SHORT
        if bar.close >= candidate.structural_stop_level:
            return PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION

    # Step 4: TOUCH + CONFIRMATION
    if candidate.direction == Direction.LONG:
        touched = bar.low <= candidate.pullback_level
        confirmed = bar.close > candidate.structural_stop_level
    else:  # SHORT
        touched = bar.high >= candidate.pullback_level
        confirmed = bar.close < candidate.structural_stop_level

    if touched and confirmed:
        return PendingEvaluation.READY_TO_FILL

    # Step 5: CONTINUE
    return PendingEvaluation.CONTINUE


def evaluate_fill_at_next_bar_open(
    candidate: PendingCandidate,
    fill_bar_open_price: float,
    *,
    filter_min_atr_mult: float,
    filter_max_atr_mult: float,
) -> FillEvaluation:
    """Apply the fill-time stop-distance filter per Phase 2u §E.3.

    The fill price is the open of the bar AFTER the touch+confirmation
    bar (committed fill model: next-bar-open after confirmation).
    The fill-time stop-distance is computed against the FROZEN
    structural-stop level and the FROZEN atr_at_signal (no
    recomputation); both are captured at registration to preserve
    H0's GAP-20260419-015 no-look-ahead convention.

    Returns FillEvaluation with ``fill=True`` and a ``fill_price`` if
    the stop-distance band ``[filter_min_atr_mult, filter_max_atr_mult]
    * atr_at_signal`` admits the fill; otherwise ``fill=False`` and
    ``cancellation_reason=STOP_DISTANCE_AT_FILL``.
    """
    if candidate.atr_at_signal <= 0.0:
        # Defense-in-depth: matches H0's passes_stop_distance_filter
        # behavior on non-positive ATR.
        return FillEvaluation(
            fill=False,
            fill_price=None,
            fill_stop_distance=None,
            cancellation_reason=CancellationReason.STOP_DISTANCE_AT_FILL,
        )
    fill_stop_distance = abs(fill_bar_open_price - candidate.structural_stop_level)
    band_min = filter_min_atr_mult * candidate.atr_at_signal
    band_max = filter_max_atr_mult * candidate.atr_at_signal
    if not (band_min <= fill_stop_distance <= band_max):
        return FillEvaluation(
            fill=False,
            fill_price=None,
            fill_stop_distance=fill_stop_distance,
            cancellation_reason=CancellationReason.STOP_DISTANCE_AT_FILL,
        )
    return FillEvaluation(
        fill=True,
        fill_price=fill_bar_open_price,
        fill_stop_distance=fill_stop_distance,
        cancellation_reason=None,
    )


def _bias_for_direction(direction: Direction) -> TrendBias:
    """Map a candidate direction to its corresponding 1h bias state."""
    if direction == Direction.LONG:
        return TrendBias.LONG
    return TrendBias.SHORT


__all__ = [
    "CancellationReason",
    "FillEvaluation",
    "PendingCandidate",
    "PendingEvaluation",
    "R2_VALIDITY_WINDOW_BARS",
    "evaluate_fill_at_next_bar_open",
    "evaluate_pending_candidate",
]
