"""v1 breakout strategy — rules-based breakout continuation with 1h trend bias.

Locked decisions per docs/03-strategy-research/v1-breakout-strategy-spec.md:

    Signal timeframe: 15m
    Higher-timeframe bias: 1h EMA(50)/EMA(200) + slope
    Setup window: 8 completed 15m bars
    Breakout buffer: 0.10 * ATR(20)
    Stop buffer: 0.10 * ATR(20)
    Stop-distance filter: 0.60 * ATR(20) <= d <= 1.80 * ATR(20)
    Stage 2->3 at +1.0R MFE (stop to -0.25R)
    Stage 3->4 at +1.5R MFE (stop to break-even)
    Stage 4->5 at +2.0R MFE (trailing active)
    Trail multiplier: 2.5 * ATR(20)
    Stage 7 stagnation exit: 8 bars without +1.0R MFE
    Re-entry: new complete setup + trigger required after exit
"""

from __future__ import annotations

from .bias import evaluate_1h_bias
from .management import TradeManagement
from .setup import detect_setup
from .stop import compute_initial_stop, passes_stop_distance_filter
from .strategy import StrategySession, V1BreakoutStrategy
from .trigger import evaluate_long_trigger, evaluate_short_trigger

__all__ = [
    "StrategySession",
    "TradeManagement",
    "V1BreakoutStrategy",
    "compute_initial_stop",
    "detect_setup",
    "evaluate_1h_bias",
    "evaluate_long_trigger",
    "evaluate_short_trigger",
    "passes_stop_distance_filter",
]
