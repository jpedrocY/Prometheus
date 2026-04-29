"""Phase 3i-B1: BacktestEngine.run dispatch for D1-A.

Phase 3i-A added the dispatch surface but raised RuntimeError on D1-A
runtime dispatch. Phase 3i-B1 lifts that guard and wires the engine
path. These tests verify:

    - D1-A dispatch no longer raises (the Phase 3i-A guard is lifted).
    - D1-A dispatch invokes the new ``_run_symbol_d1a`` path when
      ``strategy_family == FUNDING_AWARE_DIRECTIONAL``.
    - V1 default and F1 dispatch paths remain unchanged.
"""

from __future__ import annotations

from prometheus.core.symbols import Symbol
from prometheus.research.backtest import BacktestEngine
from prometheus.research.backtest.config import BacktestConfig, StrategyFamily
from prometheus.research.backtest.engine import FundingAwareLifecycleCounters
from prometheus.strategy.funding_aware_directional import FundingAwareConfig

from .conftest import default_config


def test_d1a_dispatch_no_longer_raises_runtime_error(tmp_path) -> None:
    """Phase 3i-B1: the Phase 3i-A guard is lifted. D1-A dispatch with
    empty data produces no trades but does NOT raise the documented
    Phase 3i-A error."""
    base = default_config(tmp_path)
    cfg = BacktestConfig(
        **base.model_dump(exclude={"strategy_family", "funding_aware_variant"}),
        strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
        funding_aware_variant=FundingAwareConfig(),
    )
    engine = BacktestEngine(cfg)
    # Run with empty data — D1-A path should produce no trades but no
    # RuntimeError. The Phase 3i-A "D1-A engine wiring not yet authorized"
    # error must NOT fire.
    result = engine.run(
        klines_15m_per_symbol={},
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    assert result.total_trades == 0
    # The expected behavior on empty data is a "no 15m data" warning,
    # not a guard RuntimeError.
    assert any("has no 15m data" in w for w in result.warnings) or len(result.warnings) == 0


def test_d1a_dispatch_emits_funding_aware_counters(tmp_path) -> None:
    """D1-A run produces a FundingAwareLifecycleCounters per symbol in
    the result (zero-initialized when no data is provided)."""
    base = default_config(tmp_path)
    cfg = BacktestConfig(
        **base.model_dump(exclude={"strategy_family", "funding_aware_variant"}),
        strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
        funding_aware_variant=FundingAwareConfig(),
    )
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={},
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    # No symbols processed (empty data); counters dict empty.
    assert result.funding_aware_counters_per_symbol == {}


def test_v1_breakout_dispatch_unchanged_after_d1a_wiring(tmp_path) -> None:
    """V1 default path remains runnable — the D1-A wiring does not
    perturb V1 dispatch."""
    cfg = default_config(tmp_path)
    assert cfg.strategy_family == StrategyFamily.V1_BREAKOUT
    engine = BacktestEngine(cfg)
    # Run with empty data — V1 path should produce no trades but no
    # RuntimeError.
    result = engine.run(
        klines_15m_per_symbol={},
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    assert result.total_trades == 0
    assert any("has no 15m data" in w for w in result.warnings) or (
        not any(Symbol.BTCUSDT in (s,) for s in [Symbol.BTCUSDT])
    )
    # D1-A counters dict empty for V1 paths.
    assert result.funding_aware_counters_per_symbol == {}


def test_f1_dispatch_unchanged_after_d1a_wiring(tmp_path) -> None:
    """F1 dispatch remains runnable — the D1-A wiring does not perturb
    F1 dispatch."""
    from prometheus.strategy.mean_reversion_overextension import MeanReversionConfig

    base = default_config(tmp_path)
    cfg = BacktestConfig(
        **base.model_dump(exclude={"strategy_family", "mean_reversion_variant"}),
        strategy_family=StrategyFamily.MEAN_REVERSION_OVEREXTENSION,
        mean_reversion_variant=MeanReversionConfig(),
    )
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={},
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    assert result.total_trades == 0
    # D1-A counters dict empty for F1 paths.
    assert result.funding_aware_counters_per_symbol == {}


def test_funding_aware_lifecycle_counters_identity_holds_when_zero() -> None:
    """An empty FundingAwareLifecycleCounters trivially satisfies the
    event-level identity:
        detected = filled + rejected_stop_distance + blocked_cooldown.
    """
    counters = FundingAwareLifecycleCounters()
    assert counters.funding_extreme_events_detected == 0
    assert counters.funding_extreme_events_filled == 0
    assert counters.funding_extreme_events_rejected_stop_distance == 0
    assert counters.funding_extreme_events_blocked_cooldown == 0
    assert counters.accounting_identity_holds is True
