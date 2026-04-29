"""Phase 3i-A: BacktestEngine.run dispatch guard for D1-A.

D1-A's BacktestConfig validation is wired in Phase 3i-A but the
engine path is deliberately NOT wired. ``BacktestEngine.run`` must
raise a documented RuntimeError when ``strategy_family ==
FUNDING_AWARE_DIRECTIONAL`` until Phase 3i-B1 lifts the guard.

The guard must not perturb V1 or F1 dispatch paths.
"""

from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol
from prometheus.research.backtest import BacktestEngine
from prometheus.research.backtest.config import BacktestConfig, StrategyFamily
from prometheus.strategy.funding_aware_directional import FundingAwareConfig

from .conftest import default_config


def test_d1a_dispatch_raises_runtime_error(tmp_path) -> None:
    """Attempting to run D1-A through the engine must raise the
    Phase 3i-A guard error."""
    base = default_config(tmp_path)
    cfg = BacktestConfig(
        **base.model_dump(exclude={"strategy_family", "funding_aware_variant"}),
        strategy_family=StrategyFamily.FUNDING_AWARE_DIRECTIONAL,
        funding_aware_variant=FundingAwareConfig(),
    )
    engine = BacktestEngine(cfg)
    with pytest.raises(RuntimeError) as exc_info:
        engine.run(
            klines_15m_per_symbol={},
            klines_1h_per_symbol={},
            mark_15m_per_symbol={},
            funding_per_symbol={},
            symbol_info_per_symbol={},
        )
    assert "D1-A engine wiring not yet authorized" in str(exc_info.value)
    assert "Phase 3i-B1" in str(exc_info.value)


def test_v1_breakout_dispatch_unchanged_by_d1a_guard(tmp_path) -> None:
    """V1 default path remains runnable — the D1-A guard does not
    perturb V1 dispatch."""
    cfg = default_config(tmp_path)
    assert cfg.strategy_family == StrategyFamily.V1_BREAKOUT
    engine = BacktestEngine(cfg)
    # Run with empty data — V1 path should produce no trades but no
    # RuntimeError (no D1-A guard triggered).
    result = engine.run(
        klines_15m_per_symbol={},
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    assert result.total_trades == 0
    # The "no 15m data" warning is the V1 path's normal response.
    assert any("has no 15m data" in w for w in result.warnings) or (
        not any(Symbol.BTCUSDT in (s,) for s in [Symbol.BTCUSDT])
    )


def test_f1_dispatch_unchanged_by_d1a_guard(tmp_path) -> None:
    """F1 dispatch remains runnable — the D1-A guard does not perturb
    F1 dispatch."""
    from prometheus.strategy.mean_reversion_overextension import MeanReversionConfig

    base = default_config(tmp_path)
    cfg = BacktestConfig(
        **base.model_dump(exclude={"strategy_family", "mean_reversion_variant"}),
        strategy_family=StrategyFamily.MEAN_REVERSION_OVEREXTENSION,
        mean_reversion_variant=MeanReversionConfig(),
    )
    engine = BacktestEngine(cfg)
    # Run with empty data — F1 path should produce no trades but no
    # RuntimeError (no D1-A guard triggered).
    result = engine.run(
        klines_15m_per_symbol={},
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    assert result.total_trades == 0
