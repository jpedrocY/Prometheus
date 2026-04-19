"""Minimal end-to-end: session observes bars; strategy maybe_entry returns None.

The full strategy loop is exercised by the backtest engine tests and
the simulation end-to-end tests. Here we confirm:

    - A fresh session is not ready_to_signal.
    - maybe_entry returns None before warmup is complete.
    - observe_* enforces monotonicity and symbol/interval consistency.
"""

from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol
from prometheus.strategy.v1_breakout import StrategySession, V1BreakoutStrategy

from ..conftest import hours_of_flat_1h, linear_15m_series


def test_fresh_session_not_ready() -> None:
    s = StrategySession(symbol=Symbol.BTCUSDT)
    assert s.flat
    assert not s.in_trade
    assert not s.ready_to_signal
    assert s.can_re_enter


def test_maybe_entry_none_before_warmup() -> None:
    s = StrategySession(symbol=Symbol.BTCUSDT)
    # Feed only 10 15m bars and 10 1h bars; warmup requires 200+.
    for b in linear_15m_series(n=10, start_price=100.0, step=0.1):
        s.observe_15m_bar(b)
    for h in hours_of_flat_1h(n=10, price=100.0):
        s.observe_1h_bar(h)
    strat = V1BreakoutStrategy()
    assert strat.maybe_entry(s) is None


def test_symbol_mismatch_raises() -> None:
    s = StrategySession(symbol=Symbol.BTCUSDT)
    bar = linear_15m_series(n=1, start_price=100.0, step=0.1, symbol=Symbol.ETHUSDT)[0]
    with pytest.raises(ValueError):
        s.observe_15m_bar(bar)


def test_monotonic_15m_required() -> None:
    s = StrategySession(symbol=Symbol.BTCUSDT)
    bars = linear_15m_series(n=3, start_price=100.0, step=0.1)
    s.observe_15m_bar(bars[2])
    with pytest.raises(ValueError):
        s.observe_15m_bar(bars[1])


def test_interval_mismatch_raises() -> None:
    s = StrategySession(symbol=Symbol.BTCUSDT)
    h_bar = hours_of_flat_1h(n=1, price=100.0)[0]
    with pytest.raises(ValueError):
        s.observe_15m_bar(h_bar)


def test_manage_returns_none_when_flat() -> None:
    s = StrategySession(symbol=Symbol.BTCUSDT)
    bars = linear_15m_series(n=1, start_price=100.0, step=0.1)
    strat = V1BreakoutStrategy()
    intent, diag = strat.manage(s, bars[0])
    assert intent is None
    assert diag is None


def test_session_window_sizes_are_safe_multiples() -> None:
    # We want a window large enough to cover EMA(200) + slope + breakout
    # plus room for re-entry lookback. 400 bars at 1h > 200 + slope lookback.
    s = StrategySession(symbol=Symbol.BTCUSDT)
    # Internal: 400-element deques. Feed 300 bars and confirm deque cap still OK.
    for b in linear_15m_series(n=300, start_price=100.0, step=0.001):
        s.observe_15m_bar(b)
    for h in hours_of_flat_1h(n=300, price=100.0):
        s.observe_1h_bar(h)
    assert len(s._15m_window) == 300
    assert len(s._1h_window) == 300
