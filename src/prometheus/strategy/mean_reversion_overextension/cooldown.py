"""F1 same-direction cooldown logic (Phase 3b §4).

Cooldown rule (Phase 3b §4):

    After exit (any reason): no same-direction entry until
        (a) the cumulative displacement unwinds (exists at least one
            completed bar with abs(displacement) <= threshold * ATR(20))
        AND
        (b) a fresh same-direction overextension re-forms after that
            unwind.

Phase 3d-A scope: pure helper functions only. The state machine that
remembers ``last_exit_direction`` and ``unwind_seen_since`` flags
will be threaded through the engine in Phase 3d-B; this module
provides the predicates so the engine can keep its own bookkeeping.
"""

from __future__ import annotations

from collections.abc import Sequence

from ..types import Direction


def cooldown_unwound(
    displacement_history: Sequence[float],
    atr20_history: Sequence[float],
    threshold_atr_multiple: float,
    since_index: int,
    current_index: int,
) -> bool:
    """Return True iff the cooldown unwind has occurred in (since_index, current_index].

    The unwind condition (Phase 3b §4): there exists at least one
    completed bar ``t`` with ``since_index < t <= current_index`` such
    that ``abs(displacement_history[t]) <= threshold * atr20_history[t]``.

    Both histories must be aligned by bar index. Index ``since_index``
    is exclusive (the exit bar itself does not count); ``current_index``
    is inclusive.
    """
    if since_index < 0:
        raise ValueError(f"since_index must be >= 0, got {since_index}")
    if current_index >= len(displacement_history):
        raise IndexError(
            f"current_index={current_index} out of range "
            f"len(displacement_history)={len(displacement_history)}"
        )
    if current_index >= len(atr20_history):
        raise IndexError(
            f"current_index={current_index} out of range len(atr20_history)={len(atr20_history)}"
        )
    if current_index <= since_index:
        return False
    for t in range(since_index + 1, current_index + 1):
        atr_t = float(atr20_history[t])
        if atr_t <= 0.0:
            # Skip warmup / invalid ATR bars; they cannot evidence an unwind.
            continue
        disp_t = float(displacement_history[t])
        if abs(disp_t) <= threshold_atr_multiple * atr_t:
            return True
    return False


def can_re_enter(
    candidate_direction: Direction,
    last_exit_direction: Direction | None,
    last_exit_index: int | None,
    displacement_history: Sequence[float],
    atr20_history: Sequence[float],
    current_index: int,
    threshold_atr_multiple: float,
) -> bool:
    """Return True iff a fresh same-direction entry is permitted at ``current_index``.

    Same-direction (vs. ``last_exit_direction``) entries are blocked
    until the cooldown unwind has occurred since the last exit. Opposite-
    direction entries are never blocked by cooldown — the operator-spec
    only constrains repeated same-direction trades.

    A fresh same-direction overextension re-forming is checked elsewhere
    by :func:`prometheus.strategy.mean_reversion_overextension.features.
    overextension_event`; this helper only handles the unwind half of the
    rule. The engine combines the two: cooldown allows, AND a fresh
    overextension event fires at the candidate bar.

    If there is no prior exit (``last_exit_direction is None``), entry
    is permitted regardless.
    """
    if last_exit_direction is None or last_exit_index is None:
        return True
    if candidate_direction != last_exit_direction:
        # Opposite direction is never cooldown-blocked.
        return True
    return cooldown_unwound(
        displacement_history=displacement_history,
        atr20_history=atr20_history,
        threshold_atr_multiple=threshold_atr_multiple,
        since_index=last_exit_index,
        current_index=current_index,
    )
