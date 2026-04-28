"""F1 strategy facade for unit tests and the future engine integration.

Phase 3d-A scope: stateless per-call evaluation only. State (cooldown
tracking, frozen target after entry, time-stop counter, etc.) is
left to the engine integration in Phase 3d-B.

The facade combines the pure feature / stop / target helpers into
a single :func:`MeanReversionStrategy.evaluate_entry_signal` method
so unit tests can exercise the full setup -> stop -> target -> band
pipeline without touching the backtest engine.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ..types import Direction
from .features import overextension_event
from .stop import compute_initial_stop, passes_stop_distance_filter
from .target import compute_target
from .variant_config import MeanReversionConfig


@dataclass(frozen=True)
class MeanReversionEntrySignal:
    """A validated F1 entry signal at the close of bar B.

    Phase 3d-A scope. The signal carries the direction, the bar index
    of B, the reference price used for the stop-distance band check
    (which the caller passes in as the de-slipped raw open(B+1)), the
    initial stop, the frozen target, and bookkeeping numbers. The
    engine integration in Phase 3d-B will use this dataclass to
    submit a market order at open(B+1) and seed the per-trade state.
    """

    direction: Direction
    signal_bar_index: int
    reference_price: float
    initial_stop: float
    frozen_target: float
    atr_at_signal: float
    stop_distance: float
    displacement_at_signal: float


class MeanReversionStrategy:
    """Stateless F1 strategy facade.

    Holds a frozen :class:`MeanReversionConfig` and exposes a single
    per-bar entry-evaluation method plus pure delegators for the
    stop / target helpers. Engine integration (Phase 3d-B) will be
    responsible for cooldown bookkeeping, time-stop counting, and
    fill mechanics.
    """

    def __init__(self, config: MeanReversionConfig | None = None) -> None:
        self._config: MeanReversionConfig = config if config is not None else MeanReversionConfig()

    @property
    def config(self) -> MeanReversionConfig:
        return self._config

    def evaluate_entry_signal(
        self,
        *,
        b_index: int,
        closes: Sequence[float],
        highs: Sequence[float],
        lows: Sequence[float],
        atr20: Sequence[float],
        reference_price: float,
    ) -> MeanReversionEntrySignal | None:
        """Evaluate the F1 entry pipeline at signal-time bar B.

        Returns a :class:`MeanReversionEntrySignal` iff:

            1. An overextension event fires at B
               (``abs(cumulative_displacement_8bar(B)) > threshold * ATR(20)(B)``).
            2. The resulting stop_distance is in the locked admissibility
               band ``[stop_distance_min_atr, stop_distance_max_atr] * ATR(20)(B)``.

        Returns ``None`` otherwise. Per Phase 3b §4 a rejected
        admissibility check does NOT trigger cooldown — no trade was
        opened — so cooldown bookkeeping in the engine should treat
        ``None`` as "no event".

        ``reference_price`` MUST be the raw (de-slipped) ``open(B+1)``
        per Phase 3b §4. The strategy facade does not compute it from
        the input series because the caller (engine in Phase 3d-B, or
        unit tests) is the source of truth for the next-bar open.
        """
        if reference_price <= 0.0:
            raise ValueError(f"reference_price must be positive, got {reference_price}")
        if b_index >= len(atr20):
            raise IndexError(f"b_index={b_index} out of range len(atr20)={len(atr20)}")
        atr_b = float(atr20[b_index])

        fires, sign = overextension_event(
            closes=closes,
            atr20=atr20,
            b_index=b_index,
            threshold_atr_multiple=self._config.overextension_threshold_atr_multiple,
        )
        if not fires:
            return None

        # Sign convention from features.overextension_event:
        #   +1 -> upward displacement -> SHORT candidate
        #   -1 -> downward displacement -> LONG candidate
        direction = Direction.SHORT if sign > 0 else Direction.LONG

        initial_stop = compute_initial_stop(
            direction=direction,
            lows=lows,
            highs=highs,
            atr20_at_b=atr_b,
            b_index=b_index,
            stop_buffer_atr_multiple=self._config.stop_buffer_atr_multiple,
        )
        stop_distance = abs(reference_price - initial_stop)
        if not passes_stop_distance_filter(
            stop_distance=stop_distance,
            atr20_at_b=atr_b,
            min_atr_multiple=self._config.stop_distance_min_atr,
            max_atr_multiple=self._config.stop_distance_max_atr,
        ):
            return None

        frozen_target = compute_target(closes=closes, b_index=b_index)

        # Compute displacement for telemetry / diagnostics on the signal.
        displacement = float(closes[b_index]) - float(
            closes[b_index - self._config.overextension_window_bars]
        )

        return MeanReversionEntrySignal(
            direction=direction,
            signal_bar_index=b_index,
            reference_price=reference_price,
            initial_stop=initial_stop,
            frozen_target=frozen_target,
            atr_at_signal=atr_b,
            stop_distance=stop_distance,
            displacement_at_signal=displacement,
        )
