"""Pure primitive functions for the D1-A funding-aware directional family.

Phase 3i-A scope: pure helpers only. State (per-direction consumed
event id, position-open flag, time-stop counter) belongs to the
engine integration in Phase 3i-B1. This module provides the
predicates so the engine can keep its own bookkeeping.

Per Phase 3g §6 the locked specification is:

    funding signal:   |Z_F| >= 2.0 over trailing 90 days (270 events)
    direction:        Z >= +2 -> SHORT contrarian; Z <= -2 -> LONG contrarian
    entry timing:     market at next 15m bar open (engine concern)
    stop:             1.0 × ATR(20) at fill, never moved (MARK_PRICE)
    target:           +2.0R fixed (Phase 3g §5.6.5 Option A; R3 convention)
    time-stop:        32 × 15m bars (= 8h = one funding cycle)
    cooldown:         per-funding-event consumption
    admissibility:    stop_distance ∈ [0.60, 1.80] × ATR(20)

Per Phase 3h §4.5 (with timing-clarification amendment):

    - Funding event eligible for a 15m signal bar IFF
      funding_time <= bar_close_time (non-strict; equality eligible).
    - Rolling 90-day Z-score excludes the current event from its own
      mean/std normalization (no-lookahead invariant).
    - If v002 funding_time semantics are not completed-settlement
      timestamps, future implementation must STOP and escalate.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from ..types import Direction
from .variant_config import (
    FUNDING_Z_SCORE_LOOKBACK_EVENTS,
    FUNDING_Z_SCORE_THRESHOLD,
    STOP_DISTANCE_ATR_MULTIPLIER,
    STOP_DISTANCE_MAX_ATR,
    STOP_DISTANCE_MIN_ATR,
    TARGET_R_MULTIPLE,
    TIME_STOP_BARS,
)


@dataclass(frozen=True)
class FundingEvent:
    """A single Binance USDⓈ-M funding settlement event.

    ``event_id`` is a stable string identifier (e.g.,
    ``f"{symbol}-{funding_time}"``). ``funding_time`` is UTC Unix
    milliseconds at the completed settlement boundary. ``funding_rate``
    is the signed rate (e.g., +0.0001 = +0.01% per 8h cycle).
    """

    event_id: str
    funding_time: int
    funding_rate: float


def compute_funding_z_score(
    prior_funding_rates: Sequence[float],
    current_funding_rate: float,
    lookback_events: int = FUNDING_Z_SCORE_LOOKBACK_EVENTS,
) -> float:
    """Z-score of ``current_funding_rate`` against the trailing N prior events.

    Per Phase 3g §6.1 / §6.2 and Phase 3h §4.5 no-lookahead invariant:
    the rolling mean and standard deviation are computed over the most
    recent ``lookback_events`` entries of ``prior_funding_rates``,
    **excluding** the current event itself. ``prior_funding_rates``
    must NOT contain the current event.

    Returns ``float("nan")`` when:

        - fewer than ``lookback_events`` prior events are available
          (warmup);
        - the prior-event sample variance is zero (degenerate
          distribution; no signal can be safely derived).

    Sample standard deviation (Bessel's correction, ddof=1) is used.
    """
    if lookback_events <= 1:
        raise ValueError(f"lookback_events must be > 1, got {lookback_events}")
    if len(prior_funding_rates) < lookback_events:
        return float("nan")
    window = list(prior_funding_rates[-lookback_events:])
    n = len(window)
    mean = sum(window) / n
    sum_sq = sum((x - mean) * (x - mean) for x in window)
    sample_variance = sum_sq / (n - 1)
    if sample_variance <= 0.0:
        return float("nan")
    sample_std = math.sqrt(sample_variance)
    return (current_funding_rate - mean) / sample_std


def align_funding_event_to_bar(
    funding_events: Sequence[FundingEvent],
    bar_close_time: int,
) -> FundingEvent | None:
    """Return the most recent funding event eligible for ``bar_close_time``.

    Per Phase 3h §4.5 (post-clarification, non-strict ≤):

        Eligible iff ``funding_time <= bar_close_time``.
        Equality (``funding_time == bar_close_time``) IS eligible.
        ``funding_time > bar_close_time`` is forbidden.

    If no event is eligible (all events strictly after the bar close),
    returns ``None``. ``funding_events`` is not required to be sorted;
    this function performs the linear scan.
    """
    latest: FundingEvent | None = None
    for event in funding_events:
        if event.funding_time > bar_close_time:
            continue
        if latest is None or event.funding_time > latest.funding_time:
            latest = event
    return latest


def funding_extreme_event(
    z_score: float,
    threshold: float = FUNDING_Z_SCORE_THRESHOLD,
) -> bool:
    """True iff ``|z_score| >= threshold`` (extreme-funding event).

    NaN inputs (warmup or degenerate variance) return False — the
    strategy emits no signal in those cases.
    """
    if math.isnan(z_score):
        return False
    return abs(z_score) >= threshold


def signal_direction(
    z_score: float,
    threshold: float = FUNDING_Z_SCORE_THRESHOLD,
) -> Direction | None:
    """Map an extreme Z-score to a contrarian entry direction.

    Per Phase 3g §6.3:

        z_score >= +threshold  -> SHORT (contrarian to long-pay funding)
        z_score <= -threshold  -> LONG  (contrarian to short-pay funding)
        |z_score| < threshold  -> None (no signal)
        NaN z_score             -> None (warmup / degenerate)

    The thresholds are inclusive: exactly +2.0 fires SHORT and exactly
    −2.0 fires LONG.
    """
    if math.isnan(z_score):
        return None
    if z_score >= threshold:
        return Direction.SHORT
    if z_score <= -threshold:
        return Direction.LONG
    return None


def compute_stop(
    fill_price: float,
    atr20: float,
    side: Direction,
    multiplier: float = STOP_DISTANCE_ATR_MULTIPLIER,
) -> float:
    """Return the structural stop price for a D1-A trade at fill.

    Per Phase 3g §6.7: stop_distance = ``multiplier`` × ATR(20)(at fill);
    LONG stop = fill_price − stop_distance;
    SHORT stop = fill_price + stop_distance.
    """
    if fill_price <= 0:
        raise ValueError(f"fill_price must be strictly positive, got {fill_price}")
    if atr20 <= 0:
        raise ValueError(f"atr20 must be strictly positive, got {atr20}")
    if multiplier <= 0:
        raise ValueError(f"multiplier must be strictly positive, got {multiplier}")
    stop_distance = multiplier * atr20
    if side == Direction.LONG:
        return fill_price - stop_distance
    return fill_price + stop_distance


def compute_target(
    fill_price: float,
    stop_distance: float,
    side: Direction,
    target_r: float = TARGET_R_MULTIPLE,
) -> float:
    """Return the +2.0R target price for a D1-A trade at fill.

    Per Phase 3g §6.8 + §5.6.5 Option A: target = ``target_r`` ×
    stop_distance from fill, in the favorable direction. Recorded
    exit reason is TARGET (not TAKE_PROFIT).
    """
    if fill_price <= 0:
        raise ValueError(f"fill_price must be strictly positive, got {fill_price}")
    if stop_distance <= 0:
        raise ValueError(f"stop_distance must be strictly positive, got {stop_distance}")
    if target_r <= 0:
        raise ValueError(f"target_r must be strictly positive, got {target_r}")
    delta = target_r * stop_distance
    if side == Direction.LONG:
        return fill_price + delta
    return fill_price - delta


def time_stop_bar_index(
    entry_bar_idx: int,
    time_stop_bars: int = TIME_STOP_BARS,
) -> int:
    """Return the bar index whose close triggers TIME_STOP.

    Per Phase 3g §6.9 with Phase 3h §6.9 clarification: TIME_STOP
    triggers at the close of bar ``entry_bar_idx + time_stop_bars``;
    fill occurs at the open of the next bar
    (``entry_bar_idx + time_stop_bars + 1``). The fill mechanics live
    in the engine (Phase 3i-B1); this primitive only returns the
    trigger bar index.
    """
    if entry_bar_idx < 0:
        raise ValueError(f"entry_bar_idx must be >= 0, got {entry_bar_idx}")
    if time_stop_bars <= 0:
        raise ValueError(f"time_stop_bars must be > 0, got {time_stop_bars}")
    return entry_bar_idx + time_stop_bars


def passes_stop_distance_filter(
    stop_distance: float,
    atr20: float,
    min_atr: float = STOP_DISTANCE_MIN_ATR,
    max_atr: float = STOP_DISTANCE_MAX_ATR,
) -> bool:
    """True iff ``stop_distance / atr20 ∈ [min_atr, max_atr]``.

    Per Phase 3g §6.11 admissibility band [0.60, 1.80] × ATR(20).
    D1-A's stop_distance is 1.0 × ATR(20) by construction (§6.7), so
    this filter always passes for the locked spec; the check is a
    guard against any future spec drift.
    """
    if atr20 <= 0:
        return False
    if stop_distance <= 0:
        return False
    ratio = stop_distance / atr20
    return min_atr <= ratio <= max_atr


def can_re_enter(
    candidate_direction: Direction,
    candidate_event_id: str,
    last_consumed_event_id: str | None,
    last_consumed_direction: Direction | None,
    position_open: bool,
) -> bool:
    """Per-funding-event cooldown gate (Phase 3g §6.10).

    Returns True iff a fresh entry candidate at ``candidate_event_id``
    in ``candidate_direction`` is permitted, given the most recent
    consumed funding event and current position state.

    Rules:

        - If a position is currently open: blocked (one position max).
        - If no prior consumption: allowed.
        - If candidate_direction != last_consumed_direction: allowed
          (opposite-direction is never cooldown-blocked).
        - If candidate_direction == last_consumed_direction: allowed
          iff ``candidate_event_id != last_consumed_event_id`` (a fresh
          funding event has occurred since the prior position closed).

    Repeated 15m bars referencing the same funding event must NOT
    inflate event-level detected counts (Phase 3g §9.4 amended; Phase
    3h §14 P.14 invariant 5). The engine enforces this by tracking
    the last-detected event id and only invoking cooldown bookkeeping
    on first-encounter of each fresh event id.
    """
    if position_open:
        return False
    if last_consumed_event_id is None or last_consumed_direction is None:
        return True
    if candidate_direction != last_consumed_direction:
        return True
    return candidate_event_id != last_consumed_event_id
