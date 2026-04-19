"""Pure strategy calculations for Prometheus v1.

This package contains rules-based strategy logic ONLY. It must not
import from ``prometheus.research.backtest``, ``prometheus.exchange``,
or any module that does network, persistence, or live-runtime I/O.

The strategy layer emits typed intents (``EntryIntent``,
``StopUpdateIntent``, ``ExitIntent``); the consumer (a backtest
engine or, later, a live execution layer) decides whether and how
to act on them.

Per docs/08-architecture/codebase-structure.md §"Strategy boundary rule":
the strategy may say "I'd like to open a long here"; it must not say
"place a market order."
"""

from __future__ import annotations

from .indicators import ema, true_range, wilder_atr
from .types import (
    BreakoutSignal,
    Direction,
    EntryIntent,
    ExitIntent,
    ExitReason,
    SetupWindow,
    StopMoveStage,
    StopUpdateIntent,
    TradeStage,
    TrendBias,
)

__all__ = [
    "BreakoutSignal",
    "Direction",
    "EntryIntent",
    "ExitIntent",
    "ExitReason",
    "SetupWindow",
    "StopMoveStage",
    "StopUpdateIntent",
    "TradeStage",
    "TrendBias",
    "ema",
    "true_range",
    "wilder_atr",
]
