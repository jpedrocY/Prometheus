"""D1-A strategy facade for unit tests and the future engine integration.

Phase 3i-A scope: stateless per-call evaluation only. State (per-
direction consumed funding event id, position-open flag, time-stop
counter) is left to the engine integration in Phase 3i-B1.

The facade combines the pure primitive functions into a single
``FundingAwareStrategy.evaluate_entry_signal`` method so unit tests
can exercise the full Z-score → extreme-event → direction → stop →
target → admissibility pipeline without touching the backtest engine.

D1-A is deliberately non-runnable through the engine in Phase 3i-A
(see ``BacktestEngine`` guard). Phase 3i-B1 will add the engine
dispatch path; Phase 3j (or 3i-B2) will run candidate backtests.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ..types import Direction
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
from .variant_config import FundingAwareConfig


@dataclass(frozen=True)
class FundingAwareEntrySignal:
    """A validated D1-A entry signal at the close of bar B.

    Phase 3i-A scope. The signal carries the direction, the bar index
    of B (signal bar), the consumed funding event id (for cooldown
    bookkeeping), the Z-score at signal time, the reference price
    (caller-provided next-bar-open), the stop and target prices, the
    stop distance, and the time-stop trigger bar index. The engine
    integration in Phase 3i-B1 will use this dataclass to submit a
    market order at open(B+1) and seed the per-trade state.
    """

    direction: Direction
    signal_bar_index: int
    funding_event_id: str
    funding_time: int
    funding_rate: float
    funding_z_score: float
    reference_price: float
    initial_stop: float
    target_price: float
    stop_distance: float
    atr_at_signal: float
    time_stop_trigger_bar_index: int


class FundingAwareStrategy:
    """Stateless D1-A strategy facade.

    Holds a frozen :class:`FundingAwareConfig` and exposes a single
    per-bar entry-evaluation method plus pure delegators for the
    primitive helpers. Engine integration (Phase 3i-B1) will be
    responsible for cooldown bookkeeping, time-stop counting, and
    fill mechanics.
    """

    def __init__(self, config: FundingAwareConfig | None = None) -> None:
        self._config: FundingAwareConfig = config if config is not None else FundingAwareConfig()

    @property
    def config(self) -> FundingAwareConfig:
        return self._config

    def evaluate_entry_signal(
        self,
        *,
        b_index: int,
        bar_close_time: int,
        prior_funding_rates: Sequence[float],
        funding_events: Sequence[FundingEvent],
        atr20_at_b: float,
        reference_price: float,
        candidate_event_id_override: str | None = None,
        last_consumed_event_id: str | None = None,
        last_consumed_direction: Direction | None = None,
        position_open: bool = False,
    ) -> FundingAwareEntrySignal | None:
        """Evaluate the D1-A entry pipeline at signal-time bar B's close.

        Returns a :class:`FundingAwareEntrySignal` iff:

            1. A funding event is eligible for bar B
               (``align_funding_event_to_bar`` returns non-None).
            2. The Z-score of the eligible event against
               ``prior_funding_rates`` is non-NaN and satisfies the
               extreme threshold.
            3. The contrarian direction maps cleanly per
               ``signal_direction``.
            4. The cooldown gate ``can_re_enter`` permits the candidate
               (no position open; fresh event for same-direction;
               opposite-direction always allowed).
            5. The stop distance ``1.0 × ATR(20)`` lies in the
               admissibility band ``[0.60, 1.80]``.

        Otherwise returns ``None``. The engine in Phase 3i-B1 will use
        this output to submit a market entry at the next bar's open.

        ``candidate_event_id_override`` lets unit tests pass an
        explicit event id when the eligible-event lookup is mocked.
        Production code passes ``None`` and the eligible event's
        ``event_id`` is used.
        """
        eligible = align_funding_event_to_bar(funding_events, bar_close_time)
        if eligible is None:
            return None

        z = compute_funding_z_score(
            prior_funding_rates,
            eligible.funding_rate,
            lookback_events=self._config.funding_z_score_lookback_events,
        )
        if not funding_extreme_event(z, threshold=self._config.funding_z_score_threshold):
            return None

        direction = signal_direction(z, threshold=self._config.funding_z_score_threshold)
        if direction is None:
            return None

        candidate_event_id = (
            candidate_event_id_override
            if candidate_event_id_override is not None
            else eligible.event_id
        )
        if not can_re_enter(
            candidate_direction=direction,
            candidate_event_id=candidate_event_id,
            last_consumed_event_id=last_consumed_event_id,
            last_consumed_direction=last_consumed_direction,
            position_open=position_open,
        ):
            return None

        if reference_price <= 0:
            raise ValueError(f"reference_price must be > 0, got {reference_price}")
        if atr20_at_b <= 0:
            raise ValueError(f"atr20_at_b must be > 0, got {atr20_at_b}")

        initial_stop = compute_stop(
            reference_price,
            atr20_at_b,
            direction,
            multiplier=self._config.stop_distance_atr_multiplier,
        )
        stop_distance = abs(reference_price - initial_stop)

        if not passes_stop_distance_filter(
            stop_distance,
            atr20_at_b,
            min_atr=self._config.stop_distance_min_atr,
            max_atr=self._config.stop_distance_max_atr,
        ):
            return None

        target_price = compute_target(
            reference_price,
            stop_distance,
            direction,
            target_r=self._config.target_r_multiple,
        )
        ts_bar = time_stop_bar_index(
            b_index + 1,  # entry fill bar = B+1 per Phase 3g §6.4
            time_stop_bars=self._config.time_stop_bars,
        )

        return FundingAwareEntrySignal(
            direction=direction,
            signal_bar_index=b_index,
            funding_event_id=candidate_event_id,
            funding_time=eligible.funding_time,
            funding_rate=eligible.funding_rate,
            funding_z_score=z,
            reference_price=reference_price,
            initial_stop=initial_stop,
            target_price=target_price,
            stop_distance=stop_distance,
            atr_at_signal=atr20_at_b,
            time_stop_trigger_bar_index=ts_bar,
        )
