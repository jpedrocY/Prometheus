"""Phase 4a tests for the exposure-gate skeleton."""

from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol
from prometheus.risk.exposure import (
    ExposureGateError,
    ExposureSnapshot,
    PositionSide,
    evaluate_entry_candidate,
)


def _flat_snapshot(symbol: Symbol = Symbol.BTCUSDT) -> ExposureSnapshot:
    return ExposureSnapshot(
        symbol=symbol,
        has_position=False,
        position_side=None,
        protection_confirmed=False,
        entry_in_flight=False,
        manual_or_non_bot_exposure=False,
    )


def _positioned_snapshot(
    side: PositionSide, *, protection_confirmed: bool = True
) -> ExposureSnapshot:
    return ExposureSnapshot(
        symbol=Symbol.BTCUSDT,
        has_position=True,
        position_side=side,
        protection_confirmed=protection_confirmed,
        entry_in_flight=False,
        manual_or_non_bot_exposure=False,
    )


def test_flat_snapshot_allows_btcusdt_long_entry() -> None:
    decision = evaluate_entry_candidate(
        candidate_symbol=Symbol.BTCUSDT,
        candidate_side=PositionSide.LONG,
        snapshot=_flat_snapshot(),
    )
    assert decision.allowed is True


def test_non_btcusdt_live_entry_rejected_by_rule_1() -> None:
    decision = evaluate_entry_candidate(
        candidate_symbol=Symbol.ETHUSDT,
        candidate_side=PositionSide.LONG,
        snapshot=_flat_snapshot(symbol=Symbol.ETHUSDT),
    )
    assert decision.allowed is False
    assert "Rule 1" in decision.reason


def test_pyramiding_rejected_by_rule_3() -> None:
    decision = evaluate_entry_candidate(
        candidate_symbol=Symbol.BTCUSDT,
        candidate_side=PositionSide.LONG,
        snapshot=_positioned_snapshot(PositionSide.LONG),
    )
    assert decision.allowed is False
    assert "Rule 3" in decision.reason


def test_reversal_while_positioned_rejected_by_rule_4() -> None:
    decision = evaluate_entry_candidate(
        candidate_symbol=Symbol.BTCUSDT,
        candidate_side=PositionSide.LONG,
        snapshot=_positioned_snapshot(PositionSide.SHORT),
    )
    assert decision.allowed is False
    assert "Rule 4" in decision.reason


def test_multiple_positions_blocked_via_existing_position() -> None:
    """Rule 2: any existing strategy-owned position blocks new entries."""
    # Same direction triggers Rule 3 message, opposite triggers Rule 4;
    # but in either case allowed is False. Test both directions to confirm
    # there is no path that allows a second concurrent position.
    for incoming in (PositionSide.LONG, PositionSide.SHORT):
        for existing in (PositionSide.LONG, PositionSide.SHORT):
            decision = evaluate_entry_candidate(
                candidate_symbol=Symbol.BTCUSDT,
                candidate_side=incoming,
                snapshot=_positioned_snapshot(existing),
            )
            assert decision.allowed is False


def test_unprotected_position_blocks_new_entries() -> None:
    decision = evaluate_entry_candidate(
        candidate_symbol=Symbol.BTCUSDT,
        candidate_side=PositionSide.LONG,
        snapshot=_positioned_snapshot(
            PositionSide.LONG, protection_confirmed=False
        ),
    )
    assert decision.allowed is False
    assert "Rule 9" in decision.reason


def test_entry_in_flight_blocks_new_entries() -> None:
    snap = _flat_snapshot().model_copy(update={"entry_in_flight": True})
    decision = evaluate_entry_candidate(
        candidate_symbol=Symbol.BTCUSDT,
        candidate_side=PositionSide.LONG,
        snapshot=snap,
    )
    assert decision.allowed is False
    assert "Rule 7" in decision.reason


def test_manual_exposure_blocks_new_entries() -> None:
    snap = _flat_snapshot().model_copy(update={"manual_or_non_bot_exposure": True})
    decision = evaluate_entry_candidate(
        candidate_symbol=Symbol.BTCUSDT,
        candidate_side=PositionSide.LONG,
        snapshot=snap,
    )
    assert decision.allowed is False
    assert "manual" in decision.reason


def test_inconsistent_snapshot_raises() -> None:
    """has_position=True but position_side=None is structurally invalid."""
    bad = ExposureSnapshot(
        symbol=Symbol.BTCUSDT,
        has_position=True,
        position_side=None,
        protection_confirmed=True,
        entry_in_flight=False,
        manual_or_non_bot_exposure=False,
    )
    with pytest.raises(ExposureGateError):
        evaluate_entry_candidate(
            candidate_symbol=Symbol.BTCUSDT,
            candidate_side=PositionSide.LONG,
            snapshot=bad,
        )


def test_snapshot_symbol_mismatch_raises() -> None:
    snap = _flat_snapshot(symbol=Symbol.ETHUSDT)
    with pytest.raises(ExposureGateError):
        evaluate_entry_candidate(
            candidate_symbol=Symbol.BTCUSDT,
            candidate_side=PositionSide.LONG,
            snapshot=snap,
        )
