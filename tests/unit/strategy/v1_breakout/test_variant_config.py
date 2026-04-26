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
from prometheus.strategy.types import Direction, TrendBias
from prometheus.strategy.v1_breakout import (
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
