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
    StrategySession,
    V1BreakoutConfig,
    V1BreakoutStrategy,
    detect_setup,
    evaluate_long_trigger,
)
from prometheus.strategy.v1_breakout.bias import EMA_FAST, EMA_SLOW
from prometheus.strategy.v1_breakout.management import STAGE_4_MFE_R, TradeManagement
from prometheus.strategy.v1_breakout.setup import SETUP_SIZE
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
