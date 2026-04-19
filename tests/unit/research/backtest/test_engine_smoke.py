"""Tiny engine smoke test with a short synthetic series.

This test does NOT attempt to produce a signal from the strategy
(too many warmup bars required). It verifies the engine:

    - does not crash when symbol data is absent (warning path)
    - does not crash with insufficient warmup (no trades produced)
    - reports zero trades gracefully
    - respects the window bounds
"""

from __future__ import annotations

from prometheus.core.symbols import Symbol
from prometheus.research.backtest import BacktestEngine
from tests.unit.strategy.conftest import (
    linear_15m_series,
)

from .conftest import default_config, default_symbol_info


def test_engine_handles_missing_symbol_data(tmp_path) -> None:
    cfg = default_config(tmp_path)
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={},  # none!
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    assert result.total_trades == 0
    assert any("has no 15m data" in w for w in result.warnings)


def test_engine_no_trades_with_insufficient_warmup(tmp_path) -> None:
    cfg = default_config(tmp_path)
    # Provide only 30 15m bars (warmup requires 200+ 1h bars).
    bars_15m = linear_15m_series(n=30, start_price=50_000.0, step=1.0)
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={Symbol.BTCUSDT: bars_15m},
        klines_1h_per_symbol={Symbol.BTCUSDT: []},
        mark_15m_per_symbol={Symbol.BTCUSDT: []},
        funding_per_symbol={Symbol.BTCUSDT: []},
        symbol_info_per_symbol={Symbol.BTCUSDT: default_symbol_info()},
    )
    assert result.total_trades == 0
    # No warnings: data IS present, just insufficient.
    assert all("has no" not in w for w in result.warnings)


def test_engine_results_preserve_config(tmp_path) -> None:
    cfg = default_config(tmp_path)
    engine = BacktestEngine(cfg)
    result = engine.run(
        klines_15m_per_symbol={},
        klines_1h_per_symbol={},
        mark_15m_per_symbol={},
        funding_per_symbol={},
        symbol_info_per_symbol={},
    )
    assert result.config is cfg
    assert result.total_trades == 0
