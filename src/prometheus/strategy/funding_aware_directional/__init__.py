"""D1-A funding-aware directional / carry-aware strategy family.

A new strategy family parallel to ``v1_breakout`` and
``mean_reversion_overextension``. Per the binding Phase 3g spec §6
(with §5.6 RR/target sanity Option A revising the target to +2.0R)
and the Phase 3h timing-clarification amendments, the strategy is:

    - 15m signal timeframe, completed bars only, no lookahead.
    - Bidirectional contrarian (long + short symmetric).
    - Fires when |Z_F(funding_rate at most recent completed event)|
      >= 2.0, with Z-score computed over trailing 90 days (270
      events) excluding the current event.
    - Funding event eligible for a 15m signal bar IFF
      funding_time <= bar_close_time (non-strict; equality eligible).
    - Direction: Z >= +2 -> SHORT; Z <= -2 -> LONG (contrarian).
    - Market entry at open(B+1).
    - Stop = fill_price ± 1.0 × ATR(20) at fill, never moved
      intra-trade, MARK_PRICE trigger.
    - TARGET = fill_price ± 2.0 × stop_distance (recorded as TARGET,
      not TAKE_PROFIT).
    - TARGET trigger on completed-bar close confirmation only;
      TARGET fills at next bar open. No intrabar target-touch fill.
    - Same-bar priority STOP > TARGET > TIME_STOP, evaluated on the
      completed bar; trigger at bar close, fill at next bar open.
    - Unconditional time-stop at 32 completed 15m bars from entry
      fill (= 8 hours = one funding cycle); triggers at close of bar
      B+1+32; fills at open of bar B+1+33.
    - Per-funding-event cooldown: same-direction re-entry requires
      a fresh funding event after position close; opposite-direction
      always allowed.
    - Stop-distance admissibility band: [0.60, 1.80] × ATR(20)
      (D1-A's 1.0 × ATR is inside the band by construction).
    - No regime filter.

Phase 3i-A scope (this module):

    - Locked, frozen :class:`FundingAwareConfig` (no tuning, no
      alternatives, no sweeps).
    - Pure primitive functions: Z-score, funding-event alignment,
      extreme-event detection, signal direction, stop / target /
      time-stop computation, stop-distance admissibility,
      per-event cooldown.
    - A thin :class:`FundingAwareStrategy` facade exposing per-bar
      evaluation for unit tests.
    - The backtest engine is intentionally NOT wired to this family
      yet. Phase 3i-B1 will add per-bar engine dispatch and runtime
      counters; Phase 3j (or Phase 3i-B2) will run D1-A backtests.
      Phase 3i-A only proves the module compiles, types check, has
      unit tests, and that existing V1 H0/R3 + F1 runs reproduce
      bit-for-bit.

The public surface is intentionally narrow.
"""

from __future__ import annotations

from .primitives import (
    FundingEvent,
    align_funding_event_to_bar,
    can_re_enter,
    compute_funding_z_score,
    compute_stop,
    compute_target,
    funding_extreme_event,
    passes_stop_distance_filter,
    signal_direction,
    time_stop_bar_index,
)
from .strategy import FundingAwareEntrySignal, FundingAwareStrategy
from .variant_config import FundingAwareConfig

__all__ = [
    "FundingAwareConfig",
    "FundingAwareEntrySignal",
    "FundingAwareStrategy",
    "FundingEvent",
    "align_funding_event_to_bar",
    "can_re_enter",
    "compute_funding_z_score",
    "compute_stop",
    "compute_target",
    "funding_extreme_event",
    "passes_stop_distance_filter",
    "signal_direction",
    "time_stop_bar_index",
]
