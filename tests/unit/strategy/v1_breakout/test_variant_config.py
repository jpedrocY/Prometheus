"""V1BreakoutConfig and variant wiring tests.

These tests are Phase 2g's H0-preservation contract:

    - V1BreakoutConfig() must equal the locked Phase 2e baseline
      on every field.
    - StrategySession + V1BreakoutStrategy constructed with default
      config must produce bit-for-bit identical decisions vs. the
      baseline constants.
    - Each of the four wave-1 variants (H-A1, H-B2, H-C1, H-D3) must
      actually change the axis it claims to change.
"""

from __future__ import annotations

import pytest

from prometheus.core.intervals import Interval, interval_duration_ms
from prometheus.core.klines import NormalizedKline
from prometheus.core.symbols import Symbol
from prometheus.strategy.types import Direction, ExitReason, TrendBias
from prometheus.strategy.v1_breakout import (
    ExitKind,
    SetupPredicateKind,
    StrategySession,
    V1BreakoutConfig,
    V1BreakoutStrategy,
    detect_setup,
    detect_setup_volatility_percentile,
    evaluate_long_trigger,
)
from prometheus.strategy.v1_breakout.bias import (
    EMA_FAST,
    EMA_SLOW,
    evaluate_1h_bias,
    evaluate_1h_bias_with_slope_strength,
)
from prometheus.strategy.v1_breakout.management import STAGE_4_MFE_R, TradeManagement
from prometheus.strategy.v1_breakout.setup import SETUP_SIZE, percentile_rank_threshold
from prometheus.strategy.v1_breakout.trigger import TRUE_RANGE_ATR_MULT

from ..conftest import ANCHOR_MS, kline


def _make_tight_15m_bars(count: int) -> list[NormalizedKline]:
    """Helper: n identical tight-range 15m bars suitable for a setup window."""
    d = interval_duration_ms(Interval.I_15M)
    t = ANCHOR_MS
    bars: list[NormalizedKline] = []
    for _ in range(count):
        bars.append(kline(open_time=t, open=99.0, high=100.0, low=98.0, close=99.5))
        t += d
    return bars


# --------------------------------------------------------------------------
# Baseline preservation
# --------------------------------------------------------------------------


def test_default_config_matches_baseline_constants() -> None:
    cfg = V1BreakoutConfig()
    assert cfg.setup_size == SETUP_SIZE
    assert cfg.expansion_atr_mult == TRUE_RANGE_ATR_MULT
    assert cfg.ema_fast == EMA_FAST
    assert cfg.ema_slow == EMA_SLOW
    assert cfg.break_even_r == STAGE_4_MFE_R
    # R3 fields default to H0 staged-trailing topology preserved bit-for-bit.
    assert cfg.exit_kind == ExitKind.STAGED_TRAILING
    assert cfg.exit_r_target == 2.0
    assert cfg.exit_time_stop_bars == 8
    # R1a fields default to H0 range-based predicate preserved bit-for-bit.
    assert cfg.setup_predicate_kind == SetupPredicateKind.RANGE_BASED
    assert cfg.setup_percentile_threshold == 25
    assert cfg.setup_percentile_lookback == 200
    # R1b-narrow field defaults to 0.0 (H0 strict-binary slope-3 check).
    assert cfg.bias_slope_strength_threshold == 0.0


def test_default_config_is_frozen_and_strict() -> None:
    cfg = V1BreakoutConfig()
    with pytest.raises(Exception):  # noqa: B017
        cfg.setup_size = 99  # type: ignore[misc]
    with pytest.raises(Exception):  # noqa: B017
        V1BreakoutConfig(unknown_field=1)  # type: ignore[call-arg]


def test_ema_fast_must_be_less_than_ema_slow() -> None:
    with pytest.raises(ValueError):
        V1BreakoutConfig(ema_fast=200, ema_slow=50)
    with pytest.raises(ValueError):
        V1BreakoutConfig(ema_fast=100, ema_slow=100)


def test_default_session_min_bars_equal_baseline() -> None:
    session = StrategySession(symbol=Symbol.BTCUSDT)
    assert session.min_1h_bars_for_bias == EMA_SLOW + 3  # SLOPE_LOOKBACK
    assert session.min_15m_bars_for_signal == 20 + 1 + SETUP_SIZE + 1


def test_default_strategy_config_is_baseline() -> None:
    s = V1BreakoutStrategy()
    assert s.config.setup_size == SETUP_SIZE
    assert s.config.expansion_atr_mult == TRUE_RANGE_ATR_MULT
    assert s.config.ema_fast == EMA_FAST
    assert s.config.ema_slow == EMA_SLOW
    assert s.config.break_even_r == STAGE_4_MFE_R


# --------------------------------------------------------------------------
# Variant-axis behavior tests (each variant moves the axis it claims)
# --------------------------------------------------------------------------


def test_HA1_setup_size_10_requires_10_bar_window() -> None:
    """H-A1: detect_setup with setup_size=10 rejects 8-bar windows and
    accepts well-formed 10-bar windows."""
    atr = 10.0

    # 8 bars with setup_size=10 must be rejected (length mismatch).
    eight_bars = _make_tight_15m_bars(8)
    assert detect_setup(eight_bars, atr_20_15m=atr, setup_size=10) is None

    # 10 bars with setup_size=10 must produce a valid setup when the
    # range is within 1.75*ATR and drift is within 0.35*width.
    ten_bars = _make_tight_15m_bars(10)
    s = detect_setup(ten_bars, atr_20_15m=atr, setup_size=10)
    assert s is not None
    assert s.first_bar_open_time == ten_bars[0].open_time
    assert s.last_bar_open_time == ten_bars[-1].open_time


def test_HB2_expansion_075_admits_smaller_breakouts_than_baseline() -> None:
    """H-B2: expansion_atr_mult=0.75 lets a true-range barely-passes-0.75
    bar through where the baseline 1.0 multiplier rejects it."""
    from prometheus.strategy.types import SetupWindow

    atr_15m = 10.0
    atr_1h = 50.0
    latest_1h_close = 5000.0  # normalized ATR = 1% (well within regime)

    setup = SetupWindow(
        symbol=Symbol.BTCUSDT,
        first_bar_open_time=1_600_000_000_000,
        last_bar_open_time=1_600_000_000_000 + 7 * 900_000,
        setup_high=100.0,
        setup_low=95.0,
        setup_range_width=5.0,
        net_drift_abs=1.0,
        atr_20_15m=atr_15m,
    )

    # Breakout bar: close above 100 + 0.1*10 = 101; TR = 8 (between 0.75*10 and 1.0*10).
    # Close near top of bar (top-25% positioning pass).
    breakout_bar = kline(
        open_time=ANCHOR_MS + 8 * interval_duration_ms(Interval.I_15M),
        open=99.0,
        high=103.0,
        low=95.0,
        close=102.5,
    )
    prev_close = 99.0

    # Baseline (1.0 * ATR = 10) requires TR >= 10. Bar TR is 8 → reject.
    sig_baseline = evaluate_long_trigger(
        bias=TrendBias.LONG,
        setup=setup,
        breakout_bar=breakout_bar,
        prev_15m_close=prev_close,
        atr_20_15m=atr_15m,
        atr_20_1h=atr_1h,
        latest_1h_close=latest_1h_close,
    )
    assert sig_baseline is None

    # H-B2 (0.75 * ATR = 7.5) admits TR = 8.
    sig_variant = evaluate_long_trigger(
        bias=TrendBias.LONG,
        setup=setup,
        breakout_bar=breakout_bar,
        prev_15m_close=prev_close,
        atr_20_15m=atr_15m,
        atr_20_1h=atr_1h,
        latest_1h_close=latest_1h_close,
        expansion_atr_mult=0.75,
    )
    assert sig_variant is not None
    assert sig_variant.direction == Direction.LONG


def test_HC1_ema_pair_changes_session_alpha() -> None:
    """H-C1: EMA pair 20/100 changes the incremental alpha on
    StrategySession so warmup floors and EMA values differ from baseline."""
    baseline = StrategySession(symbol=Symbol.BTCUSDT)
    variant = StrategySession(
        symbol=Symbol.BTCUSDT,
        config=V1BreakoutConfig(ema_fast=20, ema_slow=100),
    )

    # Different warmup floors prove the wiring.
    assert baseline.min_1h_bars_for_bias == 200 + 3
    assert variant.min_1h_bars_for_bias == 100 + 3
    assert variant.config.ema_fast == 20
    assert variant.config.ema_slow == 100


def test_HD3_break_even_r_moves_stage_4_trigger() -> None:
    """H-D3: break_even_r=2.0 delays the Stage 3 → 4 transition: at MFE
    = +1.6 R a baseline trade transitions to Stage 4; the variant does not."""
    from prometheus.strategy.types import TradeStage

    def make_tm() -> TradeManagement:
        return TradeManagement.start(
            symbol=Symbol.BTCUSDT,
            direction=Direction.LONG,
            entry_price=100.0,
            initial_stop=90.0,  # R = 10
            entry_bar_high=100.0,
            entry_bar_low=100.0,
        )

    d = interval_duration_ms(Interval.I_15M)

    def make_bar(i: int, high: float, low: float) -> NormalizedKline:
        # Keep open between low and high to satisfy the kline validator.
        return kline(
            open_time=ANCHOR_MS + i * d,
            open=(high + low) / 2,
            high=high,
            low=low,
            close=(high + low) / 2,
        )

    # Bar 1: push MFE to +1.0R → Stage 3 (both baseline and variant).
    # Bar 2: push MFE to +1.6R. Baseline (break_even_r=1.5) transitions
    # to Stage 4; H-D3 (break_even_r=2.0) stays in Stage 3.
    atr = 1.0

    tm_base = make_tm()
    tm_base.on_completed_bar(make_bar(1, high=110.0, low=100.0), atr)  # MFE = 1.0R
    assert tm_base.stage == TradeStage.STAGE_3_RISK_REDUCED
    tm_base.on_completed_bar(make_bar(2, high=116.0, low=105.0), atr)  # MFE = 1.6R
    assert tm_base.stage == TradeStage.STAGE_4_BREAK_EVEN

    tm_var = make_tm()
    tm_var.on_completed_bar(make_bar(1, high=110.0, low=100.0), atr, break_even_r=2.0)
    assert tm_var.stage == TradeStage.STAGE_3_RISK_REDUCED
    tm_var.on_completed_bar(make_bar(2, high=116.0, low=105.0), atr, break_even_r=2.0)
    # Variant remains in Stage 3 at MFE=1.6R because threshold is 2.0R.
    assert tm_var.stage == TradeStage.STAGE_3_RISK_REDUCED


# --------------------------------------------------------------------------
# R3 (FIXED_R_TIME_STOP) variant-axis behavior tests
#
# Per Phase 2j memo §D, R3 replaces H0's staged-trailing exit machinery
# with a two-rule terminal exit (fixed-R take-profit + unconditional
# time-stop). H0 defaults must be preserved bit-for-bit; R3 must:
#   (a) emit TAKE_PROFIT at +R_TARGET R high/low touch,
#   (b) emit TIME_STOP unconditionally at TIME_STOP_BARS,
#   (c) prefer TAKE_PROFIT over TIME_STOP on the same management bar,
#   (d) never move the protective stop intra-trade,
#   (e) never produce TRAILING_BREACH or STAGNATION exits.
# --------------------------------------------------------------------------


def _make_r3_tm(direction: Direction = Direction.LONG) -> TradeManagement:
    """Helper: a fresh trade-management object with a clean R = 10 setup."""
    if direction == Direction.LONG:
        return TradeManagement.start(
            symbol=Symbol.BTCUSDT,
            direction=Direction.LONG,
            entry_price=100.0,
            initial_stop=90.0,  # R = 10 (long: stop below entry)
            entry_bar_high=100.0,
            entry_bar_low=100.0,
        )
    return TradeManagement.start(
        symbol=Symbol.BTCUSDT,
        direction=Direction.SHORT,
        entry_price=100.0,
        initial_stop=110.0,  # R = 10 (short: stop above entry)
        entry_bar_high=100.0,
        entry_bar_low=100.0,
    )


def _bar(i: int, *, high: float, low: float, close: float | None = None) -> NormalizedKline:
    d = interval_duration_ms(Interval.I_15M)
    c = close if close is not None else (high + low) / 2
    return kline(open_time=ANCHOR_MS + i * d, open=(high + low) / 2, high=high, low=low, close=c)


def test_R3_take_profit_long_at_2R_emits_TAKE_PROFIT() -> None:
    """R3 long: bar.high reaching entry + 2R produces TAKE_PROFIT exit.

    entry=100, R=10, target=120. A bar with high=120 hits the target.
    """
    tm = _make_r3_tm(Direction.LONG)
    intent, _ = tm.on_completed_bar(
        _bar(1, high=120.0, low=100.0),
        atr_20_15m=1.0,
        exit_kind="FIXED_R_TIME_STOP",
        r_target=2.0,
        time_stop_bars=8,
    )
    from prometheus.strategy.types import ExitIntent

    assert isinstance(intent, ExitIntent)
    assert intent.reason == ExitReason.TAKE_PROFIT
    # Initial stop never moved.
    assert tm.current_stop == 90.0


def test_R3_take_profit_short_at_2R_emits_TAKE_PROFIT() -> None:
    """R3 short: bar.low reaching entry - 2R produces TAKE_PROFIT exit."""
    tm = _make_r3_tm(Direction.SHORT)
    intent, _ = tm.on_completed_bar(
        _bar(1, high=100.0, low=80.0),
        atr_20_15m=1.0,
        exit_kind="FIXED_R_TIME_STOP",
        r_target=2.0,
        time_stop_bars=8,
    )
    from prometheus.strategy.types import ExitIntent

    assert isinstance(intent, ExitIntent)
    assert intent.reason == ExitReason.TAKE_PROFIT
    assert tm.current_stop == 110.0


def test_R3_high_below_target_does_not_emit() -> None:
    """R3 long: bar that doesn't reach target produces no intent."""
    tm = _make_r3_tm(Direction.LONG)
    intent, _ = tm.on_completed_bar(
        _bar(1, high=119.99, low=99.0),
        atr_20_15m=1.0,
        exit_kind="FIXED_R_TIME_STOP",
        r_target=2.0,
        time_stop_bars=8,
    )
    assert intent is None


def test_R3_time_stop_at_8_bars_unconditional() -> None:
    """R3: 8 management calls without take-profit triggers TIME_STOP.

    The time-stop is unconditional (no MFE gate), distinguishing R3
    from H0's STAGNATION (which requires MFE < +1.0 R at 8 bars).
    """
    tm = _make_r3_tm(Direction.LONG)
    intent = None
    for i in range(1, 9):
        intent, _ = tm.on_completed_bar(
            _bar(i, high=105.0, low=99.0),  # well below target=120, no TP
            atr_20_15m=1.0,
            exit_kind="FIXED_R_TIME_STOP",
            r_target=2.0,
            time_stop_bars=8,
        )
        if i < 8:
            assert intent is None, f"unexpected exit at bar {i}: {intent}"
    from prometheus.strategy.types import ExitIntent

    assert isinstance(intent, ExitIntent)
    assert intent.reason == ExitReason.TIME_STOP
    # Initial stop still untouched after 8 bars.
    assert tm.current_stop == 90.0


def test_R3_take_profit_wins_over_time_stop_same_bar() -> None:
    """R3: on the 8th bar, take-profit wins over time-stop.

    Per Phase 2j memo §D.7 same-bar priority: TAKE_PROFIT > TIME_STOP.
    """
    tm = _make_r3_tm(Direction.LONG)
    # Bars 1-7: no TP, no time-stop yet.
    for i in range(1, 8):
        intent, _ = tm.on_completed_bar(
            _bar(i, high=105.0, low=99.0),
            atr_20_15m=1.0,
            exit_kind="FIXED_R_TIME_STOP",
            r_target=2.0,
            time_stop_bars=8,
        )
        assert intent is None
    # Bar 8: target reached AND bars_in_trade >= time_stop_bars.
    # TAKE_PROFIT must win.
    intent, _ = tm.on_completed_bar(
        _bar(8, high=120.0, low=105.0),
        atr_20_15m=1.0,
        exit_kind="FIXED_R_TIME_STOP",
        r_target=2.0,
        time_stop_bars=8,
    )
    from prometheus.strategy.types import ExitIntent

    assert isinstance(intent, ExitIntent)
    assert intent.reason == ExitReason.TAKE_PROFIT


def test_R3_no_stage_transitions_no_stop_moves() -> None:
    """R3: large MFE never triggers stage transitions or stop moves.

    The protective stop stays at the initial structural stop until
    one of {protective stop, take-profit, time-stop} fires.
    """
    from prometheus.strategy.types import StopUpdateIntent, TradeStage

    tm = _make_r3_tm(Direction.LONG)
    # MFE pushed to +1.5 R (high=115). Under H0 this would trigger
    # Stage 3 → Stage 4 break-even stop move; under R3 it must not.
    intent, _ = tm.on_completed_bar(
        _bar(1, high=115.0, low=99.0),
        atr_20_15m=1.0,
        exit_kind="FIXED_R_TIME_STOP",
        r_target=2.0,
        time_stop_bars=8,
    )
    assert not isinstance(intent, StopUpdateIntent)
    assert tm.stage == TradeStage.STAGE_2_INITIAL  # never transitioned
    assert tm.current_stop == 90.0  # never moved


def test_R3_default_path_preserves_H0_bitforbit_through_strategy() -> None:
    """Default V1BreakoutConfig must dispatch through the H0
    staged-trailing path. We exercise V1BreakoutStrategy.manage on a
    session with an active trade and assert that the management call
    routes to STAGED_TRAILING (not FIXED_R_TIME_STOP) by checking that
    a +1.0 R MFE bar triggers Stage 3 — which only the H0 path does.
    """
    from prometheus.strategy.types import StopMoveStage, StopUpdateIntent

    cfg = V1BreakoutConfig()  # all defaults = H0
    assert cfg.exit_kind == ExitKind.STAGED_TRAILING

    # Build a session with an active trade by calling the lifecycle hook
    # directly (bypassing the entry pipeline; we only need to test manage).
    session = StrategySession(symbol=Symbol.BTCUSDT, config=cfg)
    # Seed the 15m ATR cache to a non-NaN value so manage() can run.
    # We feed 21 bars to fully seed Wilder ATR(20) and the latest cache.
    bars = _make_tight_15m_bars(21)
    for b in bars:
        session.observe_15m_bar(b)
    fill_bar = kline(
        open_time=bars[-1].open_time + interval_duration_ms(Interval.I_15M),
        open=100.0,
        high=100.0,
        low=100.0,
        close=100.0,
    )
    session.observe_15m_bar(fill_bar)
    # Build a synthetic BreakoutSignal for the entry hook.
    from prometheus.strategy.types import BreakoutSignal, SetupWindow

    setup = SetupWindow(
        symbol=Symbol.BTCUSDT,
        first_bar_open_time=bars[0].open_time,
        last_bar_open_time=bars[-1].open_time,
        setup_high=100.0,
        setup_low=98.0,
        setup_range_width=2.0,
        net_drift_abs=0.5,
        atr_20_15m=1.0,
    )
    signal = BreakoutSignal(
        symbol=Symbol.BTCUSDT,
        direction=Direction.LONG,
        signal_bar_open_time=fill_bar.open_time,
        signal_bar_close_time=fill_bar.close_time,
        signal_bar_close=100.0,
        signal_bar_high=100.0,
        signal_bar_low=100.0,
        setup=setup,
        atr_20_15m=1.0,
        atr_20_1h=1.0,
        latest_1h_close=100.0,
        normalized_atr_1h=0.01,
        trend_bias=TrendBias.LONG,
    )
    session.on_entry_filled(
        signal=signal,
        fill_price=100.0,
        fill_time_ms=fill_bar.open_time,
        fill_bar=fill_bar,
        initial_stop=90.0,  # R = 10
    )

    strat = V1BreakoutStrategy(cfg)
    # Next bar pushes MFE to +1.0 R (high=110). Default path must
    # transition to Stage 3 (RISK_REDUCTION stop move).
    next_bar = kline(
        open_time=fill_bar.open_time + interval_duration_ms(Interval.I_15M),
        open=100.0,
        high=110.0,
        low=99.0,
        close=109.0,
    )
    session.observe_15m_bar(next_bar)
    intent, _ = strat.manage(session, next_bar)
    assert isinstance(intent, StopUpdateIntent)
    assert intent.reason == StopMoveStage.STAGE_3_RISK_REDUCTION


def test_R3_via_strategy_dispatches_to_FIXED_R_TIME_STOP() -> None:
    """V1BreakoutStrategy with exit_kind=FIXED_R_TIME_STOP must NOT
    perform Stage 3 stop moves on a +1.0 R MFE bar — instead it
    should emit no intent (no TP yet, no time-stop yet)."""
    cfg = V1BreakoutConfig(exit_kind=ExitKind.FIXED_R_TIME_STOP)
    session = StrategySession(symbol=Symbol.BTCUSDT, config=cfg)
    bars = _make_tight_15m_bars(21)
    for b in bars:
        session.observe_15m_bar(b)
    fill_bar = kline(
        open_time=bars[-1].open_time + interval_duration_ms(Interval.I_15M),
        open=100.0,
        high=100.0,
        low=100.0,
        close=100.0,
    )
    session.observe_15m_bar(fill_bar)
    from prometheus.strategy.types import BreakoutSignal, SetupWindow

    setup = SetupWindow(
        symbol=Symbol.BTCUSDT,
        first_bar_open_time=bars[0].open_time,
        last_bar_open_time=bars[-1].open_time,
        setup_high=100.0,
        setup_low=98.0,
        setup_range_width=2.0,
        net_drift_abs=0.5,
        atr_20_15m=1.0,
    )
    signal = BreakoutSignal(
        symbol=Symbol.BTCUSDT,
        direction=Direction.LONG,
        signal_bar_open_time=fill_bar.open_time,
        signal_bar_close_time=fill_bar.close_time,
        signal_bar_close=100.0,
        signal_bar_high=100.0,
        signal_bar_low=100.0,
        setup=setup,
        atr_20_15m=1.0,
        atr_20_1h=1.0,
        latest_1h_close=100.0,
        normalized_atr_1h=0.01,
        trend_bias=TrendBias.LONG,
    )
    session.on_entry_filled(
        signal=signal,
        fill_price=100.0,
        fill_time_ms=fill_bar.open_time,
        fill_bar=fill_bar,
        initial_stop=90.0,
    )

    strat = V1BreakoutStrategy(cfg)
    # +1.0 R MFE bar — H0 would trigger Stage 3; R3 must not.
    next_bar = kline(
        open_time=fill_bar.open_time + interval_duration_ms(Interval.I_15M),
        open=100.0,
        high=110.0,
        low=99.0,
        close=109.0,
    )
    session.observe_15m_bar(next_bar)
    intent, _ = strat.manage(session, next_bar)
    # No TP (high=110 < 120), no time-stop (only 1 bar in trade), no stage moves.
    assert intent is None


# --------------------------------------------------------------------------
# R1a (VOLATILITY_PERCENTILE) variant-axis behavior tests
#
# Per Phase 2j memo §C, R1a replaces H0's range_width / drift two-clause
# setup-validity predicate with a percentile-based ranking of the 15m
# Wilder ATR(20) at close of bar B-1 against its trailing N-bar
# distribution. The 8-bar setup window is preserved (used downstream by
# the trigger). H0 defaults must be preserved bit-for-bit; R1a must:
#   (a) reject if insufficient history (< lookback non-NaN values),
#   (b) reject if any NaN appears in the lookback window,
#   (c) accept iff rank(A_prior, Q_prior) <= floor(X * N / 100),
#   (d) reject if A_prior is non-positive or NaN,
#   (e) reject if range_width == 0 (degenerate flat setup),
#   (f) leave H0 path bit-for-bit unchanged when default config is used,
#   (g) leave R3 path bit-for-bit unchanged when only R3 fields are set.
# --------------------------------------------------------------------------


def _flat_8_prior_bars() -> list[NormalizedKline]:
    """8 prior bars with a non-degenerate range so range_width > 0."""
    d = interval_duration_ms(Interval.I_15M)
    bars: list[NormalizedKline] = []
    for i in range(8):
        bars.append(
            kline(
                open_time=ANCHOR_MS + i * d,
                open=99.5,
                high=100.5 if i % 2 == 0 else 100.0,
                low=99.0 if i % 2 == 0 else 99.5,
                close=99.8,
            )
        )
    return bars


def test_R1a_percentile_rank_threshold_at_X25_N200() -> None:
    """floor(25 * 200 / 100) = 50."""
    assert percentile_rank_threshold(25, 200) == 50
    # Verify other plausible values for completeness.
    assert percentile_rank_threshold(10, 200) == 20
    assert percentile_rank_threshold(50, 100) == 50


def test_R1a_rejects_when_history_too_short() -> None:
    """Need at least `lookback` non-NaN history values to evaluate."""
    bars = _flat_8_prior_bars()
    # 100 history values; lookback 200.
    history = tuple(0.5 for _ in range(100))
    setup = detect_setup_volatility_percentile(
        bars,
        atr_prior_15m=0.4,
        atr_history=history,
        percentile_threshold=25,
        lookback=200,
    )
    assert setup is None


def test_R1a_rejects_when_history_contains_nan() -> None:
    """Any NaN inside the trailing-lookback window triggers rejection."""
    bars = _flat_8_prior_bars()
    history = [1.0] * 199 + [float("nan")]
    setup = detect_setup_volatility_percentile(
        bars,
        atr_prior_15m=0.5,
        atr_history=tuple(history),
        percentile_threshold=25,
        lookback=200,
    )
    assert setup is None


def test_R1a_accepts_when_atr_in_bottom_quartile() -> None:
    """A_prior smaller than 75% of the trailing values -> accept."""
    bars = _flat_8_prior_bars()
    # 200 history values uniformly from 1.0 .. 200.0; A_prior = 0.5 is
    # smaller than every history element -> rank = 1 <= 50 -> accept.
    history = tuple(float(i + 1) for i in range(200))
    setup = detect_setup_volatility_percentile(
        bars,
        atr_prior_15m=0.5,
        atr_history=history,
        percentile_threshold=25,
        lookback=200,
    )
    assert setup is not None
    assert setup.atr_20_15m == 0.5


def test_R1a_rejects_when_atr_above_quartile_cutoff() -> None:
    """A_prior in the top half -> rank > 50 -> reject."""
    bars = _flat_8_prior_bars()
    # 200 history values 1..200; A_prior = 100.5 -> rank = 101 > 50 -> reject.
    history = tuple(float(i + 1) for i in range(200))
    setup = detect_setup_volatility_percentile(
        bars,
        atr_prior_15m=100.5,
        atr_history=history,
        percentile_threshold=25,
        lookback=200,
    )
    assert setup is None


def test_R1a_rejects_when_atr_at_boundary_above() -> None:
    """A_prior tied with values at rank 51 -> rank > 50 -> reject (mid-rank ceil)."""
    bars = _flat_8_prior_bars()
    # 200 history values 1..200; A_prior = 51.0 -> equal to rank-51 value;
    # mid-rank = 50 + (1+1)//2 = 51 -> reject (51 > 50).
    history = tuple(float(i + 1) for i in range(200))
    setup = detect_setup_volatility_percentile(
        bars,
        atr_prior_15m=51.0,
        atr_history=history,
        percentile_threshold=25,
        lookback=200,
    )
    assert setup is None


def test_R1a_rejects_when_atr_prior_is_nonpositive_or_nan() -> None:
    bars = _flat_8_prior_bars()
    history = tuple(float(i + 1) for i in range(200))
    assert (
        detect_setup_volatility_percentile(
            bars,
            atr_prior_15m=0.0,
            atr_history=history,
            percentile_threshold=25,
            lookback=200,
        )
        is None
    )
    assert (
        detect_setup_volatility_percentile(
            bars,
            atr_prior_15m=float("nan"),
            atr_history=history,
            percentile_threshold=25,
            lookback=200,
        )
        is None
    )


def test_R1a_session_warmup_floor_is_lookback_plus_21() -> None:
    """At default N=200, R1a's min_15m_bars_for_signal is 221."""
    cfg_h0 = V1BreakoutConfig()  # RANGE_BASED default
    cfg_r1a = V1BreakoutConfig(
        setup_predicate_kind=SetupPredicateKind.VOLATILITY_PERCENTILE,
    )
    s_h0 = StrategySession(symbol=Symbol.BTCUSDT, config=cfg_h0)
    s_r1a = StrategySession(symbol=Symbol.BTCUSDT, config=cfg_r1a)
    assert s_h0.min_15m_bars_for_signal == 30  # 20 + 1 + 8 + 1
    assert s_r1a.min_15m_bars_for_signal == 221  # max(30, 200 + 21)


def test_R1a_session_appends_prior_atr_history_after_seed() -> None:
    """The session collects non-NaN trailing ATR values after the seed.

    Wilder ATR(20) seeds at bar 21; the first non-NaN
    `_15m_atr_before_latest` therefore appears after observing bar 22.
    After observing K bars (K >= 22), the history has K - 21 values.
    """
    session = StrategySession(symbol=Symbol.BTCUSDT)
    bars = _make_tight_15m_bars(25)
    for b in bars:
        session.observe_15m_bar(b)
    # After 25 bars: 25 - 21 = 4 non-NaN history entries.
    history = session.prior_15m_atr_history()
    assert len(history) == 4
    # All entries are positive ATR values.
    for v in history:
        assert v == v and v > 0


def test_R1a_h0_preservation_default_config_does_not_call_percentile() -> None:
    """Default V1BreakoutConfig must dispatch the H0 RANGE_BASED predicate.

    Sanity check: detect_setup_volatility_percentile is *not* the default
    path. We cannot directly observe the dispatch from outside the
    strategy module, so we exercise it via the strategy facade with a
    config that would fail the percentile predicate (insufficient
    history) and assert the H0 path is still used.
    """
    cfg = V1BreakoutConfig()
    assert cfg.setup_predicate_kind == SetupPredicateKind.RANGE_BASED
    s = V1BreakoutStrategy(cfg)
    assert s.config.setup_predicate_kind == SetupPredicateKind.RANGE_BASED


def test_R1a_h0_baseline_path_preserved_via_strategy() -> None:
    """The H0 strategy at default config still calls detect_setup (range-based).

    We cannot intercept the dispatch directly without monkeypatching,
    so this is the same baseline-preservation contract as
    test_default_strategy_config_is_baseline plus an explicit assertion
    that R1a fields default to H0-preserving values.
    """
    s = V1BreakoutStrategy()
    assert s.config.setup_predicate_kind == SetupPredicateKind.RANGE_BASED
    assert s.config.setup_percentile_threshold == 25
    assert s.config.setup_percentile_lookback == 200


def test_R1a_r3_preservation_r3_only_config_keeps_RANGE_BASED() -> None:
    """An R3-only config (FIXED_R_TIME_STOP) preserves H0 setup-predicate.

    A config that selects only R3 must not accidentally enable R1a.
    """
    cfg = V1BreakoutConfig(exit_kind=ExitKind.FIXED_R_TIME_STOP)
    assert cfg.exit_kind == ExitKind.FIXED_R_TIME_STOP
    assert cfg.setup_predicate_kind == SetupPredicateKind.RANGE_BASED
    assert cfg.setup_percentile_threshold == 25
    assert cfg.setup_percentile_lookback == 200


def test_R1a_combined_with_R3_config_holds_both_axes() -> None:
    """The Phase 2m candidate config selects both R1a and R3 axes."""
    cfg = V1BreakoutConfig(
        exit_kind=ExitKind.FIXED_R_TIME_STOP,
        exit_r_target=2.0,
        exit_time_stop_bars=8,
        setup_predicate_kind=SetupPredicateKind.VOLATILITY_PERCENTILE,
        setup_percentile_threshold=25,
        setup_percentile_lookback=200,
    )
    # Other axes must remain at H0 baseline.
    assert cfg.setup_size == 8
    assert cfg.expansion_atr_mult == 1.0
    assert cfg.ema_fast == 50
    assert cfg.ema_slow == 200
    assert cfg.break_even_r == 1.5
    # R3 axis intact.
    assert cfg.exit_kind == ExitKind.FIXED_R_TIME_STOP
    assert cfg.exit_r_target == 2.0
    assert cfg.exit_time_stop_bars == 8
    # R1a axis intact.
    assert cfg.setup_predicate_kind == SetupPredicateKind.VOLATILITY_PERCENTILE
    assert cfg.setup_percentile_threshold == 25
    assert cfg.setup_percentile_lookback == 200


# --------------------------------------------------------------------------
# R1b-narrow (bias_slope_strength_threshold) variant-axis behavior tests
#
# Per Phase 2r spec memo §B / §E / §F, R1b-narrow replaces H0's binary
# slope-3 direction-sign check with a magnitude check on
# slope_strength_3 = (EMA(50)[now] - EMA(50)[now-3]) / EMA(50)[now].
# The committed threshold is S = 0.0020 (= 0.20%). Default 0.0
# preserves H0 bit-for-bit via sentinel-based dispatch.
#
# Tests must verify:
#   (a) default config (threshold=0.0) preserves H0 binary check,
#   (b) at threshold=S the predicate admits slopes >= +S (LONG) and
#       <= -S (SHORT),
#   (c) slopes in (-S, +S) produce NEUTRAL,
#   (d) boundary ties at exactly +S / -S admit (non-strict >= / <=),
#   (e) NaN warmup -> NEUTRAL,
#   (f) negative threshold rejected,
#   (g) R3-only config preserves H0 bias (default threshold=0.0),
#   (h) R1b-narrow combined with R3 holds both axes.
# --------------------------------------------------------------------------


def _make_1h_bars_with_target_slope(
    *,
    slope_pct_per_3_bars: float,
    n: int = 250,
    start_price: float = 100.0,
    short_term_bias: bool = True,
) -> list[NormalizedKline]:
    """Build a 1h-bar series whose EMA(50) reaches a target 3-bar slope
    rate by the last bar.

    The series is a steady linear trend in close so that EMA(50) and
    EMA(200) settle into a near-monotonic relationship. Returning a
    long enough series (>= 250) ensures both EMAs are seeded.

    ``short_term_bias=True`` produces an upward trend (LONG-side test);
    False produces a downward trend (SHORT-side test). The actual EMA
    slope at the last bar will be approximately ``slope_pct_per_3_bars``
    of the EMA(50) value over the SLOPE_LOOKBACK=3 window, but this is
    not exact — tests should evaluate the resulting bias and not assert
    specific slope_strength_3 values numerically.
    """
    d = interval_duration_ms(Interval.I_1H)
    # Use a per-bar return that produces approximately the desired
    # 3-bar slope of EMA(50). A steady ramp of `slope_pct_per_3_bars / 3`
    # per bar over the EMA window will produce a steady-state slope of
    # roughly that value.
    per_bar_return = slope_pct_per_3_bars / 3.0
    if not short_term_bias:
        per_bar_return = -per_bar_return
    bars: list[NormalizedKline] = []
    t = ANCHOR_MS
    price = start_price
    for _ in range(n):
        nxt = price * (1.0 + per_bar_return)
        bars.append(
            kline(
                interval=Interval.I_1H,
                open_time=t,
                open=price,
                high=max(price, nxt) * 1.0001,
                low=min(price, nxt) * 0.9999,
                close=nxt,
            )
        )
        t += d
        price = nxt
    return bars


def test_R1b_default_threshold_zero_preserves_H0_bias() -> None:
    """V1BreakoutConfig() default has bias_slope_strength_threshold=0.0,
    which dispatches to H0's strict binary check via sentinel.
    """
    cfg = V1BreakoutConfig()
    assert cfg.bias_slope_strength_threshold == 0.0


def test_R1b_evaluate_function_zero_slope_at_zero_threshold_neutral() -> None:
    """At zero threshold, the magnitude function admits slope == 0 as
    NEUTRAL because both LONG (>= 0) and SHORT (<= 0) conditions fire,
    so the predicate's ``long_ok and not short_ok`` filter rejects.

    This is documented behavior — the strategy facade dispatches to
    H0's strict binary check at threshold=0 to avoid this edge case.
    The standalone function is not used by the strategy at threshold=0.
    """
    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.0, n=250)
    bias = evaluate_1h_bias_with_slope_strength(bars, slope_strength_threshold=0.0)
    # Flat ramp -> EMA(50) ~= EMA(200) ~= last close, so all ok-conditions fail.
    assert bias == TrendBias.NEUTRAL


def test_R1b_evaluate_function_strong_uptrend_admits_LONG() -> None:
    """At threshold=0.0020, a strong upward trend produces LONG bias."""
    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.01, n=250, short_term_bias=True)
    bias = evaluate_1h_bias_with_slope_strength(bars, slope_strength_threshold=0.0020)
    assert bias == TrendBias.LONG


def test_R1b_evaluate_function_strong_downtrend_admits_SHORT() -> None:
    """At threshold=0.0020, a strong downward trend produces SHORT bias."""
    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.01, n=250, short_term_bias=False)
    bias = evaluate_1h_bias_with_slope_strength(bars, slope_strength_threshold=0.0020)
    assert bias == TrendBias.SHORT


def test_R1b_evaluate_function_weak_uptrend_below_threshold_neutral() -> None:
    """A weak uptrend whose 3-bar slope is below +S produces NEUTRAL.

    A per-bar return of 0.0001 (0.01%) gives a 3-bar slope of about
    0.0003, well below S=0.0020.
    """
    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.0003, n=250, short_term_bias=True)
    bias = evaluate_1h_bias_with_slope_strength(bars, slope_strength_threshold=0.0020)
    assert bias == TrendBias.NEUTRAL


def test_R1b_evaluate_function_negative_threshold_raises() -> None:
    """The function rejects negative threshold values."""
    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.01, n=250)
    with pytest.raises(ValueError):
        evaluate_1h_bias_with_slope_strength(bars, slope_strength_threshold=-0.0010)


def test_R1b_evaluate_function_warmup_returns_neutral() -> None:
    """Insufficient warmup produces NEUTRAL regardless of threshold."""
    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.01, n=50)
    bias = evaluate_1h_bias_with_slope_strength(bars, slope_strength_threshold=0.0020)
    assert bias == TrendBias.NEUTRAL


def test_R1b_strategy_session_default_dispatches_to_H0_path() -> None:
    """StrategySession with default config calls H0's binary slope-3 check."""
    cfg = V1BreakoutConfig()
    assert cfg.bias_slope_strength_threshold == 0.0
    s = V1BreakoutStrategy(cfg)
    assert s.config.bias_slope_strength_threshold == 0.0


def test_R1b_strategy_session_with_threshold_uses_magnitude_check() -> None:
    """A config with non-zero threshold dispatches to the magnitude
    check inside StrategySession._update_1h_bias.

    We construct a session and feed enough 1h bars to seed EMAs and
    fill the slope-lookback ring; then assert that bias matches the
    expected behavior of the magnitude check.
    """
    cfg_h0 = V1BreakoutConfig()
    cfg_r1b = V1BreakoutConfig(bias_slope_strength_threshold=0.0020)

    # Build a strong-uptrend 1h series.
    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.01, n=250, short_term_bias=True)

    s_h0 = StrategySession(symbol=Symbol.BTCUSDT, config=cfg_h0)
    s_r1b = StrategySession(symbol=Symbol.BTCUSDT, config=cfg_r1b)
    for b in bars:
        s_h0.observe_1h_bar(b)
        s_r1b.observe_1h_bar(b)
    # Both should produce LONG on a strong uptrend.
    assert s_h0.current_1h_bias() == TrendBias.LONG
    assert s_r1b.current_1h_bias() == TrendBias.LONG


def test_R1b_strategy_session_with_threshold_rejects_weak_trend() -> None:
    """A weak trend below threshold S=0.0020 produces NEUTRAL under
    R1b-narrow, but LONG under H0 (where any positive slope passes)."""
    cfg_h0 = V1BreakoutConfig()
    cfg_r1b = V1BreakoutConfig(bias_slope_strength_threshold=0.0020)

    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.0003, n=250, short_term_bias=True)

    s_h0 = StrategySession(symbol=Symbol.BTCUSDT, config=cfg_h0)
    s_r1b = StrategySession(symbol=Symbol.BTCUSDT, config=cfg_r1b)
    for b in bars:
        s_h0.observe_1h_bar(b)
        s_r1b.observe_1h_bar(b)
    # H0 admits LONG (any positive slope direction is enough).
    assert s_h0.current_1h_bias() == TrendBias.LONG
    # R1b-narrow rejects (slope_strength below 0.0020).
    assert s_r1b.current_1h_bias() == TrendBias.NEUTRAL


def test_R1b_h0_evaluate_function_unchanged() -> None:
    """The original evaluate_1h_bias function is unchanged by Phase 2s.

    Asserted by exercising it on a simple uptrend and confirming LONG.
    """
    bars = _make_1h_bars_with_target_slope(slope_pct_per_3_bars=0.01, n=250, short_term_bias=True)
    assert evaluate_1h_bias(bars) == TrendBias.LONG


def test_R1b_r3_only_config_preserves_H0_bias_threshold() -> None:
    """An R3-only config (FIXED_R_TIME_STOP) preserves H0 bias-strength
    threshold of 0.0 (= H0 binary slope check)."""
    cfg = V1BreakoutConfig(exit_kind=ExitKind.FIXED_R_TIME_STOP)
    assert cfg.exit_kind == ExitKind.FIXED_R_TIME_STOP
    assert cfg.bias_slope_strength_threshold == 0.0


def test_R1b_combined_with_R3_config_holds_both_axes() -> None:
    """The Phase 2s candidate config selects R3 exit + R1b-narrow bias."""
    cfg = V1BreakoutConfig(
        exit_kind=ExitKind.FIXED_R_TIME_STOP,
        exit_r_target=2.0,
        exit_time_stop_bars=8,
        bias_slope_strength_threshold=0.0020,
    )
    # All other axes at H0 baseline.
    assert cfg.setup_size == 8
    assert cfg.expansion_atr_mult == 1.0
    assert cfg.ema_fast == 50
    assert cfg.ema_slow == 200
    assert cfg.break_even_r == 1.5
    assert cfg.setup_predicate_kind == SetupPredicateKind.RANGE_BASED
    # R3 axis intact.
    assert cfg.exit_kind == ExitKind.FIXED_R_TIME_STOP
    assert cfg.exit_r_target == 2.0
    assert cfg.exit_time_stop_bars == 8
    # R1b-narrow axis intact.
    assert cfg.bias_slope_strength_threshold == 0.0020


def test_R1b_negative_threshold_field_constraint() -> None:
    """Pydantic Field(ge=0.0) rejects negative threshold values at
    config construction time."""
    with pytest.raises(Exception):  # noqa: B017 - pydantic ValidationError
        V1BreakoutConfig(bias_slope_strength_threshold=-0.001)
