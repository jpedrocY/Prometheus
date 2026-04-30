"""Phase 4a tests for the stop-validation skeleton."""

from __future__ import annotations

import pytest

from prometheus.core.governance import (
    GovernanceLabelError,
    StopTriggerDomain,
)
from prometheus.core.symbols import Symbol
from prometheus.risk.exposure import PositionSide
from prometheus.risk.stop_validation import (
    MissingMetadataError,
    StopRequest,
    StopUpdateRequest,
    StopValidationError,
    validate_initial_stop,
    validate_stop_update,
)


def _long_stop_request(**overrides: object) -> StopRequest:
    base = dict(
        symbol=Symbol.BTCUSDT,
        side=PositionSide.LONG,
        proposed_entry_price=50_000.0,
        initial_stop_price=49_500.0,
        atr=500.0,
        tick_size=0.10,
        price_precision=2,
        stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
    )
    base.update(overrides)
    return StopRequest(**base)  # type: ignore[arg-type]


def test_long_stop_below_entry_passes() -> None:
    validate_initial_stop(_long_stop_request())


def test_long_stop_at_or_above_entry_rejects() -> None:
    with pytest.raises(StopValidationError):
        validate_initial_stop(
            _long_stop_request(initial_stop_price=50_000.0)
        )
    with pytest.raises(StopValidationError):
        validate_initial_stop(
            _long_stop_request(initial_stop_price=51_000.0)
        )


def test_short_stop_above_entry_passes() -> None:
    validate_initial_stop(
        _long_stop_request(
            side=PositionSide.SHORT,
            initial_stop_price=50_500.0,
        )
    )


def test_short_stop_below_entry_rejects() -> None:
    with pytest.raises(StopValidationError):
        validate_initial_stop(
            _long_stop_request(
                side=PositionSide.SHORT,
                initial_stop_price=49_500.0,
            )
        )


def test_stop_too_tight_rejects() -> None:
    # 0.60 * 500 = 300; stop distance 200 is too tight.
    with pytest.raises(StopValidationError):
        validate_initial_stop(
            _long_stop_request(
                initial_stop_price=49_800.0,
                atr=500.0,
            )
        )


def test_stop_too_wide_rejects() -> None:
    # 1.80 * 500 = 900; stop distance 1_000 is too wide.
    with pytest.raises(StopValidationError):
        validate_initial_stop(
            _long_stop_request(
                initial_stop_price=49_000.0,
                atr=500.0,
            )
        )


def test_mixed_or_unknown_stop_trigger_domain_fails_closed() -> None:
    """The most important Phase 3v §8.4 fail-closed rule at the
    stop-validation boundary."""
    with pytest.raises(GovernanceLabelError):
        validate_initial_stop(
            _long_stop_request(
                stop_trigger_domain=StopTriggerDomain.MIXED_OR_UNKNOWN
            )
        )


def test_metadata_validation_rejects_zero_atr() -> None:
    with pytest.raises(MissingMetadataError):
        validate_initial_stop(_long_stop_request(atr=0))


def test_metadata_validation_rejects_negative_tick_size() -> None:
    with pytest.raises(MissingMetadataError):
        validate_initial_stop(_long_stop_request(tick_size=-1))


def test_stop_update_long_widening_rejected() -> None:
    """For a long, lowering the stop widens risk."""
    request = StopUpdateRequest(
        symbol=Symbol.BTCUSDT,
        side=PositionSide.LONG,
        current_stop_price=49_500.0,
        proposed_new_stop_price=49_000.0,
        stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
    )
    with pytest.raises(StopValidationError):
        validate_stop_update(request)


def test_stop_update_long_risk_reducing_accepted() -> None:
    request = StopUpdateRequest(
        symbol=Symbol.BTCUSDT,
        side=PositionSide.LONG,
        current_stop_price=49_500.0,
        proposed_new_stop_price=49_700.0,
        stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
    )
    validate_stop_update(request)


def test_stop_update_short_widening_rejected() -> None:
    request = StopUpdateRequest(
        symbol=Symbol.BTCUSDT,
        side=PositionSide.SHORT,
        current_stop_price=50_500.0,
        proposed_new_stop_price=51_000.0,
        stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
    )
    with pytest.raises(StopValidationError):
        validate_stop_update(request)


def test_stop_update_short_risk_reducing_accepted() -> None:
    request = StopUpdateRequest(
        symbol=Symbol.BTCUSDT,
        side=PositionSide.SHORT,
        current_stop_price=50_500.0,
        proposed_new_stop_price=50_300.0,
        stop_trigger_domain=StopTriggerDomain.MARK_PRICE_RUNTIME,
    )
    validate_stop_update(request)


def test_stop_update_mixed_or_unknown_fails_closed_at_construction() -> None:
    """Phase 3v §8.4: stop_trigger_domain validation runs in the
    pydantic model_validator. ``GovernanceLabelError`` is propagated
    directly (pydantic v2 wraps only ``ValueError`` / ``AssertionError``)."""
    with pytest.raises(GovernanceLabelError):
        StopUpdateRequest(
            symbol=Symbol.BTCUSDT,
            side=PositionSide.LONG,
            current_stop_price=49_500.0,
            proposed_new_stop_price=49_700.0,
            stop_trigger_domain=StopTriggerDomain.MIXED_OR_UNKNOWN,
        )
