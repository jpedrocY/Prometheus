"""F1 mean-reversion-after-overextension strategy family.

A new strategy family parallel to ``v1_breakout``. Per the binding
Phase 3b spec §4 the strategy is:

    - 15m signal timeframe, completed bars only, no lookahead.
    - Bidirectional (long + short symmetric).
    - Fires when |close(B) - close(B-8)| > 1.75 * ATR(20)(B).
        - Positive cumulative displacement -> SHORT candidate.
        - Negative cumulative displacement -> LONG candidate.
    - Mean reference is SMA(8) of close on bar B (frozen at signal time).
    - Market entry at open(B+1).
    - Long protective stop = lowest_low([B-7..B]) - 0.10 * ATR(20)(B).
    - Short protective stop = highest_high([B-7..B]) + 0.10 * ATR(20)(B).
    - Stop never moves intra-trade.
    - Target exit (long) when first completed bar t > B has close(t) >=
      frozen target; short mirror on close(t) <= frozen target. Fill at
      open(t+1).
    - Unconditional time stop at 8 completed bars from entry-fill bar.
    - Cooldown after exit: same-direction re-entry blocked until the
      cumulative displacement unwinds AND a fresh same-direction
      overextension re-forms.
    - Stop-distance admissibility: reject if stop_distance is outside
      [0.60, 1.80] * ATR(20)(B), evaluated on the de-slipped raw
      open(B+1).
    - No 1h regime filter.

Phase 3d-A scope (this module):

    - Locked, frozen :class:`MeanReversionConfig` (no tuning, no
      alternatives, no sweeps).
    - Pure feature / stop / target / cooldown helpers.
    - A thin :class:`MeanReversionStrategy` facade exposing per-bar
      evaluation for unit tests.
    - The backtest engine is intentionally NOT wired to this family
      yet. Phase 3d-B will add per-bar engine dispatch and run F1
      backtests; Phase 3d-A only proves the module compiles, types
      check, has unit tests, and that the existing V1 H0/R3 runs
      reproduce bit-for-bit.

The public surface is intentionally narrow.
"""

from __future__ import annotations

from .cooldown import can_re_enter, cooldown_unwound
from .features import (
    cumulative_displacement_8bar,
    overextension_event,
    sma_8_close,
)
from .stop import compute_initial_stop, passes_stop_distance_filter
from .strategy import MeanReversionEntrySignal, MeanReversionStrategy
from .target import compute_target, target_hit
from .variant_config import MeanReversionConfig

__all__ = [
    "MeanReversionConfig",
    "MeanReversionEntrySignal",
    "MeanReversionStrategy",
    "can_re_enter",
    "compute_initial_stop",
    "compute_target",
    "cooldown_unwound",
    "cumulative_displacement_8bar",
    "overextension_event",
    "passes_stop_distance_filter",
    "sma_8_close",
    "target_hit",
]
