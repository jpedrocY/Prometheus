"""R2 (pullback-retest entry) lifecycle unit tests.

Per Phase 2v §3.1.7 (Gate 2 amended):

    - H0 baseline preservation under default entry_kind.
    - R2 registration / warmup rejection.
    - R2 touch+confirmation (LONG + SHORT).
    - R2 STRUCTURAL_INVALIDATION (Phase 2v Gate 2 amendment).
    - R2 cancellation precedence (5-step ordering).
    - R2 fill-time stop-distance band rejection.
    - R2 expiry at validity-window close.
    - R2 pending uniqueness.
    - R2 R3 time-stop-counted-from-fill-bar.
    - R2 frozen protective-stop-level invariant.

The tests here are predicate-level (``evaluate_pending_candidate``,
``evaluate_fill_at_next_bar_open``, ``PendingCandidate`` state) and
StrategySession lifecycle hooks. Full engine-integration baseline
preservation is verified by the H0/R3 R/V control runs in 2w-A
(see the 2w-A checkpoint report); the unit tests here lock in the
predicate behavior that those control runs depend on.
"""

from __future__ import annotations

import math

import pytest

from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol
from prometheus.strategy.types import (
    BreakoutSignal,
    Direction,
    SetupWindow,
    TrendBias,
)
from prometheus.strategy.v1_breakout import (
    R2_VALIDITY_WINDOW_BARS,
    CancellationReason,
    EntryKind,
    ExitKind,
    PendingCandidate,
    PendingEvaluation,
    StrategySession,
    V1BreakoutConfig,
    evaluate_fill_at_next_bar_open,
    evaluate_pending_candidate,
)
from prometheus.strategy.v1_breakout.stop import (
    FILTER_MAX_ATR_MULT,
    FILTER_MIN_ATR_MULT,
)

from ..conftest import ANCHOR_MS, kline

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def _make_setup() -> SetupWindow:
    d = interval_duration_ms(Interval.I_15M)
    return SetupWindow(
        symbol=Symbol.BTCUSDT,
        first_bar_open_time=ANCHOR_MS,
        last_bar_open_time=ANCHOR_MS + 7 * d,
        setup_high=100.0,
        setup_low=98.0,
        setup_range_width=2.0,
        net_drift_abs=0.5,
        atr_20_15m=1.5,
    )


def _make_signal(direction: Direction, *, setup: SetupWindow | None = None) -> BreakoutSignal:
    if setup is None:
        setup = _make_setup()
    d = interval_duration_ms(Interval.I_15M)
    breakout_open_time = setup.last_bar_open_time + d
    return BreakoutSignal(
        symbol=Symbol.BTCUSDT,
        direction=direction,
        signal_bar_open_time=breakout_open_time,
        signal_bar_close_time=breakout_open_time + d - 1,
        signal_bar_close=101.0 if direction == Direction.LONG else 97.0,
        signal_bar_high=101.5 if direction == Direction.LONG else 99.0,
        signal_bar_low=99.0 if direction == Direction.LONG else 96.5,
        setup=setup,
        atr_20_15m=1.5,
        atr_20_1h=10.0,
        latest_1h_close=1000.0,
        normalized_atr_1h=0.01,
        trend_bias=TrendBias.LONG if direction == Direction.LONG else TrendBias.SHORT,
    )


def _make_candidate(
    direction: Direction = Direction.LONG,
    *,
    registration_bar_index: int = 100,
    pullback_level: float = 100.0,  # = setup.setup_high for LONG
    structural_stop_level: float = 96.0,  # below setup_low - 0.10*ATR for LONG
    atr_at_signal: float = 1.5,
    next_bar_open_at_signal: float = 101.5,
) -> PendingCandidate:
    setup = _make_setup()
    sig = _make_signal(direction, setup=setup)
    return PendingCandidate(
        direction=direction,
        registration_bar_index=registration_bar_index,
        registration_bar_open_time=ANCHOR_MS + registration_bar_index * 900_000,
        pullback_level=pullback_level,
        structural_stop_level=structural_stop_level,
        atr_at_signal=atr_at_signal,
        validity_expires_at_index=registration_bar_index + R2_VALIDITY_WINDOW_BARS,
        signal_bar_open_time_ms=sig.signal_bar_open_time,
        signal_bar_close_time_ms=sig.signal_bar_close_time,
        next_bar_open_at_signal=next_bar_open_at_signal,
        signal=sig,
    )


def _bar_at(idx: int, *, low: float, high: float, close: float) -> NormalizedKline:
    """Build a kline with consistent OHLC fields.

    The NormalizedKline validator requires ``low <= min(open, close)``
    and ``high >= max(open, close)``. We pick ``open = low`` (always
    satisfies the low-side invariant when ``close >= low``) and clamp
    ``high`` upward if needed to satisfy the high-side invariant.

    Callers must pass ``low <= close`` (the OHLC invariant); a bar
    where the close is below the low is not a real bar and cannot be
    constructed via NormalizedKline. For tests where we want to verify
    that ``close <= structural_stop_level`` triggers
    STRUCTURAL_INVALIDATION, the close is the lowest point so we set
    low equal to (or below) close.
    """
    assert low <= close, f"OHLC violation: low {low} must be <= close {close}"
    open_ = low
    high_val = max(high, close, open_)
    return kline(
        open_time=ANCHOR_MS + idx * 900_000,
        open=open_,
        high=high_val,
        low=low,
        close=close,
    )


# --------------------------------------------------------------------------
# H0 baseline preservation under default entry_kind
# --------------------------------------------------------------------------


def test_default_entry_kind_is_market_next_bar_open() -> None:
    """V1BreakoutConfig() produces EntryKind.MARKET_NEXT_BAR_OPEN."""
    cfg = V1BreakoutConfig()
    assert cfg.entry_kind == EntryKind.MARKET_NEXT_BAR_OPEN


def test_explicit_entry_kind_pullback_retest() -> None:
    """R2 opt-in via explicit kwarg works under pydantic strict mode."""
    cfg = V1BreakoutConfig(entry_kind=EntryKind.PULLBACK_RETEST)
    assert cfg.entry_kind == EntryKind.PULLBACK_RETEST


def test_default_session_has_no_pending_candidate() -> None:
    """Fresh StrategySession has no pending candidate (H0 default)."""
    session = StrategySession(symbol=Symbol.BTCUSDT)
    assert session.has_pending_candidate is False
    assert session.pending_candidate is None


def test_default_session_with_r3_config_has_no_pending_candidate() -> None:
    """R3-config session also has no pending candidate (R3 doesn't touch entry-lifecycle)."""
    session = StrategySession(
        symbol=Symbol.BTCUSDT,
        config=V1BreakoutConfig(
            exit_kind=ExitKind.FIXED_R_TIME_STOP,
            exit_r_target=2.0,
            exit_time_stop_bars=8,
        ),
    )
    assert session.has_pending_candidate is False


# --------------------------------------------------------------------------
# PendingCandidate state methods
# --------------------------------------------------------------------------


def test_pending_candidate_is_within_validity_at_b_plus_one_through_b_plus_eight() -> None:
    c = _make_candidate(registration_bar_index=100)
    # B+0 (registration bar itself) is NOT eligible per spec.
    assert c.is_within_validity(100) is False
    # B+1..B+8 inclusive.
    for k in range(1, 9):
        assert c.is_within_validity(100 + k) is True
    # B+9 onwards is past the validity window.
    assert c.is_within_validity(109) is False
    assert c.is_within_validity(200) is False


def test_pending_candidate_is_expired_strictly_past_b_plus_eight() -> None:
    c = _make_candidate(registration_bar_index=100)
    # During validity window: not expired.
    assert c.is_expired(108) is False
    # Strictly past: expired.
    assert c.is_expired(109) is True
    assert c.is_expired(110) is True


def test_pending_candidate_validity_expires_at_index_is_registration_plus_eight() -> None:
    c = _make_candidate(registration_bar_index=42)
    assert c.validity_expires_at_index == 42 + R2_VALIDITY_WINDOW_BARS
    assert R2_VALIDITY_WINDOW_BARS == 8


# --------------------------------------------------------------------------
# StrategySession pending-candidate hooks
# --------------------------------------------------------------------------


def test_session_register_pending_candidate_then_clear() -> None:
    session = StrategySession(symbol=Symbol.BTCUSDT)
    c = _make_candidate()
    session.register_pending_candidate(c)
    assert session.has_pending_candidate is True
    assert session.pending_candidate is c
    session.clear_pending_candidate()
    assert session.has_pending_candidate is False
    assert session.pending_candidate is None


def test_session_register_pending_candidate_rejects_double_registration() -> None:
    """Per Phase 2u §E.5 pending uniqueness: at most one candidate at a time.

    Registering when one already exists is a programming error (the
    engine is responsible for handling same-direction drop and
    opposite-direction cancel-then-register per §E.5).
    """
    session = StrategySession(symbol=Symbol.BTCUSDT)
    c = _make_candidate()
    session.register_pending_candidate(c)
    with pytest.raises(ValueError, match="already active"):
        session.register_pending_candidate(_make_candidate(direction=Direction.SHORT))


def test_session_clear_pending_candidate_when_no_pending_is_idempotent() -> None:
    """Clearing when no candidate is registered is a no-op (used by the
    engine after FILL/EXPIRE/CANCEL paths converge).
    """
    session = StrategySession(symbol=Symbol.BTCUSDT)
    session.clear_pending_candidate()
    assert session.has_pending_candidate is False


# --------------------------------------------------------------------------
# evaluate_pending_candidate — TOUCH + CONFIRMATION (LONG)
# --------------------------------------------------------------------------


def test_R2_long_touch_and_confirm_produces_ready_to_fill() -> None:
    """LONG: low <= setup_high AND close > structural_stop → READY_TO_FILL."""
    c = _make_candidate(direction=Direction.LONG)
    bar = _bar_at(101, low=99.5, high=100.5, close=99.8)  # touch (low <= 100), confirm (close > 96)
    assert evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False) == (
        PendingEvaluation.READY_TO_FILL
    )


def test_R2_long_no_touch_continues_pending() -> None:
    """LONG: low > pullback_level AND close > structural_stop → CONTINUE."""
    c = _make_candidate(direction=Direction.LONG)
    bar = _bar_at(101, low=100.5, high=101.5, close=101.0)  # no touch (low > 100), close OK
    assert evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False) == (
        PendingEvaluation.CONTINUE
    )


def test_R2_long_close_violates_stop_triggers_structural_invalidation() -> None:
    """LONG with bar that touches AND closes below structural_stop → CANCEL_STRUCTURAL_INVALIDATION.

    Replaces the pre-amendment ``test_R2_long_touch_without_confirm_continues_pending``
    case. Under the Phase 2v Gate 2 amended precedence, step 3
    STRUCTURAL_INVALIDATION fires before step 4 TOUCH+CONFIRMATION
    can be reached. In valid OHLC data, a close-violates-stop bar
    always has low <= close <= stop (the close is the lowest meaningful
    point), so touch is implicit. We use low=95.0, close=95.5 — a bar
    that fell to 95.0 then closed at 95.5, well below the structural
    stop at 96.0.
    """
    c = _make_candidate(direction=Direction.LONG, structural_stop_level=96.0)
    bar = _bar_at(101, low=95.0, high=100.5, close=95.5)
    assert evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False) == (
        PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION
    )


def test_R2_long_confirm_without_touch_continues_pending() -> None:
    """LONG: close > stop AND low > pullback (no touch) → CONTINUE.

    Behavior unchanged from pre-amendment per Phase 2u §E.6.
    """
    c = _make_candidate(direction=Direction.LONG)
    bar = _bar_at(101, low=100.5, high=102.0, close=101.0)
    assert evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False) == (
        PendingEvaluation.CONTINUE
    )


# --------------------------------------------------------------------------
# evaluate_pending_candidate — TOUCH + CONFIRMATION (SHORT mirrored)
# --------------------------------------------------------------------------


def _short_candidate() -> PendingCandidate:
    return _make_candidate(
        direction=Direction.SHORT,
        pullback_level=98.0,  # setup_low for short
        structural_stop_level=102.0,  # above setup_high + 0.10*ATR
        next_bar_open_at_signal=97.5,
    )


def test_R2_short_touch_and_confirm_produces_ready_to_fill() -> None:
    """SHORT: high >= setup_low AND close < structural_stop → READY_TO_FILL."""
    c = _short_candidate()
    # SHORT touch requires high >= pullback (98). Use low=98.0, close=98.2,
    # high=98.5 — all consistent (low <= close <= high).
    bar = _bar_at(101, low=98.0, high=98.5, close=98.2)
    assert evaluate_pending_candidate(c, bar, TrendBias.SHORT, opposite_signal_fires=False) == (
        PendingEvaluation.READY_TO_FILL
    )


def test_R2_short_close_violates_stop_triggers_structural_invalidation() -> None:
    """SHORT: close >= structural_stop_level → CANCEL_STRUCTURAL_INVALIDATION.

    For SHORT, structural_stop is ABOVE the price. A bar that closes
    above the stop has its close being the highest point: low <= open
    <= close. Pick low=98.0, close=102.5, high=103.0.
    """
    c = _short_candidate()
    bar = _bar_at(101, low=98.0, high=103.0, close=102.5)
    assert evaluate_pending_candidate(c, bar, TrendBias.SHORT, opposite_signal_fires=False) == (
        PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION
    )


def test_R2_short_confirm_without_touch_continues_pending() -> None:
    """SHORT: close < stop AND high < pullback → CONTINUE."""
    c = _short_candidate()
    bar = _bar_at(101, low=96.5, high=97.5, close=97.0)
    assert evaluate_pending_candidate(c, bar, TrendBias.SHORT, opposite_signal_fires=False) == (
        PendingEvaluation.CONTINUE
    )


# --------------------------------------------------------------------------
# Cancellation precedence (5-step ordering per Phase 2v Gate 2 amendment)
# --------------------------------------------------------------------------


def test_R2_bias_flip_cancels_candidate() -> None:
    """LONG candidate + SHORT bias at bar t → CANCEL_BIAS_FLIP."""
    c = _make_candidate(direction=Direction.LONG)
    bar = _bar_at(101, low=99.5, high=100.5, close=99.8)  # would touch+confirm
    assert (
        evaluate_pending_candidate(c, bar, TrendBias.SHORT, opposite_signal_fires=False)
        == PendingEvaluation.CANCEL_BIAS_FLIP
    )


def test_R2_bias_neutral_at_bar_t_cancels_via_bias_flip() -> None:
    """NEUTRAL bias at bar t while LONG-pending → CANCEL_BIAS_FLIP."""
    c = _make_candidate(direction=Direction.LONG)
    bar = _bar_at(101, low=99.5, high=100.5, close=99.8)
    assert (
        evaluate_pending_candidate(c, bar, TrendBias.NEUTRAL, opposite_signal_fires=False)
        == PendingEvaluation.CANCEL_BIAS_FLIP
    )


def test_R2_opposite_signal_cancels_candidate() -> None:
    """LONG candidate + opposite_signal_fires=True → CANCEL_OPPOSITE_SIGNAL."""
    c = _make_candidate(direction=Direction.LONG)
    bar = _bar_at(101, low=99.5, high=100.5, close=99.8)  # would touch+confirm
    assert (
        evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=True)
        == PendingEvaluation.CANCEL_OPPOSITE_SIGNAL
    )


def _construct_synthetic_bar(*, low: float, high: float, close: float) -> NormalizedKline:
    """Bypass NormalizedKline OHLC validation for predicate-isolation tests.

    Used only by tests that exercise impossible-in-real-OHLC scenarios
    (e.g., non-touch + close-violates-stop for LONG, where in real
    markets close <= stop implies low <= close <= stop < pullback so
    touch is forced). The predicate must produce the right outcome
    regardless of OHLC consistency; this helper lets us assert on
    that.
    """
    from prometheus.core.intervals import Interval
    from prometheus.core.time import close_time_for

    open_time = ANCHOR_MS + 101 * 900_000
    return NormalizedKline.model_construct(
        symbol=Symbol.BTCUSDT,
        interval=Interval.I_15M,
        open_time=open_time,
        close_time=close_time_for(open_time, Interval.I_15M),
        open=close,  # placeholder; predicate doesn't read open
        high=high,
        low=low,
        close=close,
        volume=1.0,
        quote_asset_volume=close,
        trade_count=1,
        taker_buy_base_volume=0.5,
        taker_buy_quote_volume=close * 0.5,
        source="synthetic-predicate-test",
    )


def test_R2_structural_invalidation_long_no_touch() -> None:
    """LONG: close <= structural_stop, no touch → CANCEL_STRUCTURAL_INVALIDATION.

    Phase 2v Gate 2 amendment: STRUCTURAL_INVALIDATION fires regardless
    of touch state. The (low > pullback) AND (close <= stop) input is
    impossible in valid OHLC (close <= stop < pullback < low → close
    < low contradicts low <= close), but the predicate's logic must
    still produce the right outcome. Constructed via
    ``NormalizedKline.model_construct`` to bypass OHLC validation.
    """
    c = _make_candidate(direction=Direction.LONG, structural_stop_level=96.0)
    # low=100.5 > pullback=100 (no touch); close=95.5 <= stop=96 (violation)
    bar = _construct_synthetic_bar(low=100.5, high=102.0, close=95.5)
    assert evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False) == (
        PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION
    )


def test_R2_structural_invalidation_short_no_touch() -> None:
    """SHORT: close >= structural_stop, no touch → CANCEL_STRUCTURAL_INVALIDATION.

    Mirror of the LONG no-touch test; impossible in valid OHLC, tested
    via predicate isolation.
    """
    c = _short_candidate()  # pullback=98, stop=102
    # high=97.5 < pullback=98 (no touch); close=102.5 >= stop=102 (violation)
    bar = _construct_synthetic_bar(low=96.0, high=97.5, close=102.5)
    assert evaluate_pending_candidate(c, bar, TrendBias.SHORT, opposite_signal_fires=False) == (
        PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION
    )


def test_R2_structural_invalidation_precedence_after_opposite_signal() -> None:
    """Bar where OPPOSITE_SIGNAL AND structural-violation both fire →
    OPPOSITE_SIGNAL wins (precedence position 2 < 3).
    """
    c = _make_candidate(direction=Direction.LONG, structural_stop_level=96.0)
    # Touch + close-violates-stop (OHLC-valid: low <= close).
    bar = _bar_at(101, low=95.0, high=100.5, close=95.5)
    # opposite signal True overrides structural-invalidation per precedence.
    assert (
        evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=True)
        == PendingEvaluation.CANCEL_OPPOSITE_SIGNAL
    )


def test_R2_structural_invalidation_precedence_before_touch_confirmation() -> None:
    """Touch bar with close <= structural_stop → STRUCTURAL_INVALIDATION wins.

    Per Phase 2v Gate 2 amendment: step 3 fires before step 4
    touch+confirmation can be reached. Pre-amendment this case was
    misclassified as "touch without confirmation" continue-pending.
    """
    c = _make_candidate(direction=Direction.LONG, structural_stop_level=96.0)
    # Touch + close-violates-stop (OHLC-valid).
    bar = _bar_at(101, low=95.0, high=100.5, close=95.5)
    assert (
        evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False)
        == PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION
    )


def test_R2_cancellation_precedence_full_5_step_ordering() -> None:
    """All four cancellation predicates true simultaneously → BIAS_FLIP wins.

    Bar with bias-flip AND opposite-signal AND structural-violation AND
    touch+confirmation all true → CANCEL_BIAS_FLIP (precedence 1 < 2 < 3 < 4).
    """
    c = _make_candidate(direction=Direction.LONG, structural_stop_level=96.0)
    # Touch + close-violates-stop (OHLC-valid).
    bar = _bar_at(101, low=95.0, high=100.5, close=95.5)
    # Bias-flip (SHORT bias) + opposite-signal True + close-violates-stop + touch:
    assert (
        evaluate_pending_candidate(c, bar, TrendBias.SHORT, opposite_signal_fires=True)
        == PendingEvaluation.CANCEL_BIAS_FLIP
    )


# --------------------------------------------------------------------------
# Boundary cases per Phase 2u §E.6
# --------------------------------------------------------------------------


def test_R2_long_close_exactly_at_structural_stop_triggers_invalidation() -> None:
    """LONG with close == structural_stop_level → CANCEL_STRUCTURAL_INVALIDATION.

    The ``<=`` predicate at step 3 admits equality (treats stop level
    itself as invalidation per H0 protective-stop convention).
    """
    c = _make_candidate(direction=Direction.LONG, structural_stop_level=96.0)
    bar = _bar_at(101, low=95.5, high=100.5, close=96.0)
    assert evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False) == (
        PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION
    )


def test_R2_long_close_just_above_structural_stop_admits_touch_confirmation() -> None:
    """LONG with close strictly > structural_stop AND touch → READY_TO_FILL."""
    c = _make_candidate(direction=Direction.LONG, structural_stop_level=96.0)
    bar = _bar_at(101, low=96.0, high=100.5, close=96.5)
    assert evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False) == (
        PendingEvaluation.READY_TO_FILL
    )


def test_R2_long_low_exactly_at_pullback_level_is_a_touch() -> None:
    """LONG: low == pullback_level satisfies the touch predicate (``<=``).

    Pick close = pullback_level (= low) so OHLC stays valid; close
    100.0 > stop 96.0 (confirm).
    """
    c = _make_candidate(direction=Direction.LONG)  # pullback=100
    bar = _bar_at(101, low=100.0, high=100.5, close=100.0)
    assert evaluate_pending_candidate(c, bar, TrendBias.LONG, opposite_signal_fires=False) == (
        PendingEvaluation.READY_TO_FILL
    )


# --------------------------------------------------------------------------
# evaluate_fill_at_next_bar_open — fill-time stop-distance band
# --------------------------------------------------------------------------


def test_R2_fill_admitted_within_band() -> None:
    """Fill price producing stop_distance within [0.60, 1.80]*ATR → fill=True."""
    c = _make_candidate(structural_stop_level=96.0, atr_at_signal=1.5)
    # stop_distance = abs(98 - 96) = 2.0 = 1.33 * 1.5 → in [0.90, 2.70]
    fill = evaluate_fill_at_next_bar_open(
        c,
        fill_bar_open_price=98.0,
        filter_min_atr_mult=FILTER_MIN_ATR_MULT,
        filter_max_atr_mult=FILTER_MAX_ATR_MULT,
    )
    assert fill.fill is True
    assert fill.fill_price == 98.0
    assert fill.fill_stop_distance is not None
    assert math.isclose(fill.fill_stop_distance, 2.0)
    assert fill.cancellation_reason is None


def test_R2_fill_rejected_if_stop_distance_below_floor() -> None:
    """Fill price too close to stop (below 0.60*ATR) → CANCEL_STOP_DISTANCE_AT_FILL."""
    c = _make_candidate(structural_stop_level=96.0, atr_at_signal=1.5)
    # stop_distance = abs(96.5 - 96) = 0.5 < 0.60*1.5 = 0.90 → below floor.
    fill = evaluate_fill_at_next_bar_open(
        c,
        fill_bar_open_price=96.5,
        filter_min_atr_mult=FILTER_MIN_ATR_MULT,
        filter_max_atr_mult=FILTER_MAX_ATR_MULT,
    )
    assert fill.fill is False
    assert fill.fill_price is None
    assert fill.cancellation_reason == CancellationReason.STOP_DISTANCE_AT_FILL


def test_R2_fill_rejected_if_stop_distance_above_ceiling() -> None:
    """Fill price too far from stop (above 1.80*ATR) → CANCEL_STOP_DISTANCE_AT_FILL."""
    c = _make_candidate(structural_stop_level=96.0, atr_at_signal=1.5)
    # stop_distance = abs(99.5 - 96) = 3.5 > 1.80*1.5 = 2.70 → above ceiling.
    fill = evaluate_fill_at_next_bar_open(
        c,
        fill_bar_open_price=99.5,
        filter_min_atr_mult=FILTER_MIN_ATR_MULT,
        filter_max_atr_mult=FILTER_MAX_ATR_MULT,
    )
    assert fill.fill is False
    assert fill.cancellation_reason == CancellationReason.STOP_DISTANCE_AT_FILL


def test_R2_fill_rejected_if_atr_at_signal_zero() -> None:
    """Defense-in-depth: atr_at_signal <= 0 always rejects fill."""
    c = _make_candidate(atr_at_signal=0.0)
    fill = evaluate_fill_at_next_bar_open(
        c,
        fill_bar_open_price=98.0,
        filter_min_atr_mult=FILTER_MIN_ATR_MULT,
        filter_max_atr_mult=FILTER_MAX_ATR_MULT,
    )
    assert fill.fill is False
    assert fill.cancellation_reason == CancellationReason.STOP_DISTANCE_AT_FILL


# --------------------------------------------------------------------------
# Frozen-protective-stop invariant
# --------------------------------------------------------------------------


def test_R2_pending_candidate_structural_stop_is_frozen() -> None:
    """PendingCandidate is a frozen dataclass; structural_stop_level cannot be reassigned."""
    c = _make_candidate(structural_stop_level=96.0)
    with pytest.raises(Exception):  # noqa: B017 — FrozenInstanceError or similar
        c.structural_stop_level = 95.0  # type: ignore[misc]


def test_R2_pending_candidate_pullback_level_is_frozen() -> None:
    """PendingCandidate.pullback_level is frozen at registration."""
    c = _make_candidate(pullback_level=100.0)
    with pytest.raises(Exception):  # noqa: B017
        c.pullback_level = 99.0  # type: ignore[misc]


def test_R2_pending_candidate_atr_at_signal_is_frozen() -> None:
    """PendingCandidate.atr_at_signal is frozen at registration (preserves
    H0's GAP-20260419-015 no-look-ahead convention).
    """
    c = _make_candidate(atr_at_signal=1.5)
    with pytest.raises(Exception):  # noqa: B017
        c.atr_at_signal = 2.0  # type: ignore[misc]


# --------------------------------------------------------------------------
# Engine-side accounting identity
# --------------------------------------------------------------------------


def test_R2_lifecycle_counters_default_to_zero() -> None:
    """Fresh R2LifecycleCounters has all counters at zero (control-path baseline)."""
    from prometheus.research.backtest.engine import R2LifecycleCounters

    counters = R2LifecycleCounters()
    assert counters.registered == 0
    assert counters.filled == 0
    assert counters.cancelled_bias_flip == 0
    assert counters.cancelled_opposite_signal == 0
    assert counters.cancelled_structural_invalidation == 0
    assert counters.cancelled_stop_distance_at_fill == 0
    assert counters.expired_no_pullback == 0
    assert counters.accounting_identity_holds is True


def test_R2_lifecycle_counters_accounting_identity_holds_after_each_outcome() -> None:
    """The identity registered = sum(terminal outcomes) holds after every increment."""
    from prometheus.research.backtest.engine import R2LifecycleCounters

    counters = R2LifecycleCounters()
    counters.registered += 1
    counters.filled += 1
    assert counters.accounting_identity_holds

    counters.registered += 1
    counters.cancelled_bias_flip += 1
    assert counters.accounting_identity_holds

    counters.registered += 1
    counters.cancelled_opposite_signal += 1
    assert counters.accounting_identity_holds

    counters.registered += 1
    counters.cancelled_structural_invalidation += 1
    assert counters.accounting_identity_holds

    counters.registered += 1
    counters.cancelled_stop_distance_at_fill += 1
    assert counters.accounting_identity_holds

    counters.registered += 1
    counters.expired_no_pullback += 1
    assert counters.accounting_identity_holds


def test_R2_lifecycle_counters_identity_breaks_when_unattributed() -> None:
    """Sanity: registering without a terminal outcome breaks the identity."""
    from prometheus.research.backtest.engine import R2LifecycleCounters

    counters = R2LifecycleCounters()
    counters.registered += 1
    assert counters.accounting_identity_holds is False


def test_signal_funnel_counts_r2_accounting_identity_holds_default() -> None:
    """SignalFunnelCounts default state has the R2 identity holding (0=0)."""
    from prometheus.research.backtest.diagnostics import SignalFunnelCounts

    counts = SignalFunnelCounts(symbol=Symbol.BTCUSDT)
    assert counts.r2_accounting_identity_holds is True
    assert counts.registered_candidates == 0
    assert counts.trades_filled_R2 == 0


# --------------------------------------------------------------------------
# Validity-window expiry
# --------------------------------------------------------------------------


def test_R2_candidate_at_b_plus_eight_is_within_validity() -> None:
    """B+8 is the LAST eligible bar (inclusive); not yet expired."""
    c = _make_candidate(registration_bar_index=100)
    assert c.is_within_validity(108) is True
    assert c.is_expired(108) is False


def test_R2_candidate_at_b_plus_nine_is_expired() -> None:
    """B+9 is strictly past the validity window → expired."""
    c = _make_candidate(registration_bar_index=100)
    assert c.is_within_validity(109) is False
    assert c.is_expired(109) is True


# --------------------------------------------------------------------------
# Pending uniqueness (engine-state-level)
# --------------------------------------------------------------------------


def test_R2_session_register_after_clear_admits_new_candidate() -> None:
    """After clear, the slot is free; a new registration is admitted."""
    session = StrategySession(symbol=Symbol.BTCUSDT)
    c1 = _make_candidate(direction=Direction.LONG)
    session.register_pending_candidate(c1)
    session.clear_pending_candidate()
    c2 = _make_candidate(direction=Direction.SHORT)
    session.register_pending_candidate(c2)
    assert session.pending_candidate is c2


def test_R2_session_register_during_trade_is_rejected() -> None:
    """Cannot register a candidate while an active trade is open
    (one-position-max invariant).
    """
    session = StrategySession(symbol=Symbol.BTCUSDT)
    sig = _make_signal(Direction.LONG)
    fill_bar = kline(
        open_time=ANCHOR_MS + 100 * 900_000,
        open=101.5,
        high=102.0,
        low=101.0,
        close=101.5,
    )
    session.on_entry_filled(
        signal=sig,
        fill_price=101.5,
        fill_time_ms=fill_bar.open_time,
        fill_bar=fill_bar,
        initial_stop=96.0,
    )
    with pytest.raises(ValueError, match="already in_trade"):
        session.register_pending_candidate(_make_candidate())
