"""Unit tests for the signal-funnel diagnostic.

The diagnostic is observational: given the same inputs, its outputs
must be stable and each decision bar must land in exactly one
rejection bucket (or in the "entry_intents_produced" flow).
"""

from __future__ import annotations

from prometheus.core.symbols import Symbol
from prometheus.research.backtest.diagnostics import (
    MIN_1H_BARS_FOR_BIAS,
    SignalFunnelCounts,
    run_signal_funnel,
)
from tests.unit.strategy.conftest import (
    hours_of_flat_1h,
    linear_15m_series,
    ramping_1h_series,
)

from .conftest import default_config, default_symbol_info


def _invariants(counts: SignalFunnelCounts) -> None:
    """Each decision bar must land in exactly one bucket (or the fill flow)."""
    accounted = (
        counts.rejected_neutral_bias
        + counts.rejected_no_valid_setup
        + counts.rejected_close_did_not_break_level
        + counts.rejected_true_range_too_small
        + counts.rejected_close_location_failed
        + counts.rejected_normalized_atr_regime_failed
        + counts.rejected_stop_distance_filter_failed
        + counts.rejected_sizing_failed
        + counts.entry_intents_produced
    )
    assert accounted == counts.decision_bars_evaluated, (
        f"funnel bucket accounting mismatch: {accounted} vs decision_bars_evaluated="
        f"{counts.decision_bars_evaluated}"
    )
    # Bias counts sum to decision bars.
    bias_sum = counts.bias_long_count + counts.bias_short_count + counts.bias_neutral_count
    assert bias_sum == counts.decision_bars_evaluated
    # Candidates are a subset of non-neutral decision bars.
    assert counts.long_breakout_candidates <= counts.bias_long_count
    assert counts.short_breakout_candidates <= counts.bias_short_count


def test_insufficient_data_returns_zero_decisions(tmp_path) -> None:
    cfg = default_config(tmp_path)
    bars_15m = linear_15m_series(n=10, start_price=50_000.0, step=1.0)
    bars_1h = hours_of_flat_1h(n=10, price=50_000.0)
    counts = run_signal_funnel(
        symbol=Symbol.BTCUSDT,
        klines_15m=bars_15m,
        klines_1h=bars_1h,
        symbol_info=default_symbol_info(),
        config=cfg,
    )
    assert counts.total_15m_bars_loaded == 10
    assert counts.total_1h_bars_loaded == 10
    assert counts.decision_bars_evaluated == 0
    assert counts.warmup_15m_bars_excluded >= 10
    assert counts.entry_intents_produced == 0


def test_flat_series_produces_only_neutral_bias_rejections(tmp_path) -> None:
    """With a flat 1h series, bias is always NEUTRAL; every post-warmup
    decision bar should land in rejected_neutral_bias."""
    cfg = default_config(tmp_path)
    # Need at least MIN_1H_BARS_FOR_BIAS 1h bars and MIN_15M_BARS_FOR_SIGNAL 15m bars.
    bars_1h = hours_of_flat_1h(n=MIN_1H_BARS_FOR_BIAS + 50, price=50_000.0)
    # 15m bars spanning the same time window (4x more bars per hour).
    bars_15m = linear_15m_series(n=4 * (MIN_1H_BARS_FOR_BIAS + 50), start_price=50_000.0, step=0.0)
    counts = run_signal_funnel(
        symbol=Symbol.BTCUSDT,
        klines_15m=bars_15m,
        klines_1h=bars_1h,
        symbol_info=default_symbol_info(),
        config=cfg,
    )
    _invariants(counts)
    assert counts.decision_bars_evaluated > 0
    # Flat series -> bias neutral -> rejection.
    assert counts.rejected_neutral_bias == counts.decision_bars_evaluated
    assert counts.bias_long_count == 0
    assert counts.bias_short_count == 0


def test_rising_series_produces_long_bias(tmp_path) -> None:
    cfg = default_config(tmp_path)
    # Strong, sustained uptrend.
    bars_1h = ramping_1h_series(
        n=MIN_1H_BARS_FOR_BIAS + 40, start_price=50_000.0, per_hour_return=0.001
    )
    # 15m bars with matching drift so forming 1h groups contain
    # aligned price action. We use a tiny 15m step.
    bars_15m = linear_15m_series(n=4 * (MIN_1H_BARS_FOR_BIAS + 40), start_price=50_000.0, step=1.0)
    counts = run_signal_funnel(
        symbol=Symbol.BTCUSDT,
        klines_15m=bars_15m,
        klines_1h=bars_1h,
        symbol_info=default_symbol_info(),
        config=cfg,
    )
    _invariants(counts)
    assert counts.bias_long_count > 0
    # A strictly linear 15m series has no consolidation, so setup
    # detection will reject. Confirm that expectation explicitly.
    assert counts.rejected_no_valid_setup > 0


def test_invariant_holds_under_realistic_engine_call_sequence(tmp_path) -> None:
    """Run the diagnostic on a larger synthetic window and assert the
    bucket accounting invariant holds."""
    cfg = default_config(tmp_path)
    bars_1h = ramping_1h_series(
        n=MIN_1H_BARS_FOR_BIAS + 200, start_price=50_000.0, per_hour_return=0.0005
    )
    bars_15m = linear_15m_series(n=4 * (MIN_1H_BARS_FOR_BIAS + 200), start_price=50_000.0, step=0.5)
    counts = run_signal_funnel(
        symbol=Symbol.BTCUSDT,
        klines_15m=bars_15m,
        klines_1h=bars_1h,
        symbol_info=default_symbol_info(),
        config=cfg,
    )
    _invariants(counts)


def test_summary_string_is_readable(tmp_path) -> None:
    cfg = default_config(tmp_path)
    counts = run_signal_funnel(
        symbol=Symbol.BTCUSDT,
        klines_15m=[],
        klines_1h=[],
        symbol_info=default_symbol_info(),
        config=cfg,
    )
    text = counts.summary()
    assert "symbol=BTCUSDT" in text
    assert "decision bars" in text
    assert "entry intents" in text


def test_empty_inputs_return_warnings(tmp_path) -> None:
    cfg = default_config(tmp_path)
    counts = run_signal_funnel(
        symbol=Symbol.BTCUSDT,
        klines_15m=[],
        klines_1h=[],
        symbol_info=default_symbol_info(),
        config=cfg,
    )
    assert counts.total_15m_bars_loaded == 0
    assert counts.warnings
    assert counts.decision_bars_evaluated == 0
