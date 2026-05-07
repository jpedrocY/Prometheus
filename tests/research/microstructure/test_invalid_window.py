"""Tests for the microstructure invalid-window taxonomy (Phase 4aw)."""

from __future__ import annotations

import pytest

from prometheus.research.microstructure.invalid_window import (
    DownstreamEligibilityAction,
    InvalidWindow,
    InvalidWindowReason,
    InvalidWindowSeverity,
)

EXPECTED_REASONS: tuple[str, ...] = (
    "missing_sequence",
    "out_of_order_event",
    "duplicate_event",
    "gap_after_reconnect",
    "snapshot_mismatch",
    "clock_skew",
    "symbol_mismatch",
    "stale_stream",
    "stale_book",
    "impossible_spread",
    "negative_size",
    "zero_or_invalid_price",
    "archive_checksum_mismatch",
    "rest_retention_gap",
    "force_order_proxy_incompleteness",
    "failed_atomic_write",
    "partial_file_recovery_event",
)


def test_seventeen_reasons_exact_set() -> None:
    actual = tuple(r.value for r in InvalidWindowReason)
    assert len(actual) == 17
    assert set(actual) == set(EXPECTED_REASONS)


def test_severity_enum_minimum_set() -> None:
    actual = {s.value for s in InvalidWindowSeverity}
    assert {"info", "warn", "error"} <= actual


def test_action_enum_minimum_set() -> None:
    actual = {a.value for a in DownstreamEligibilityAction}
    assert {"flag", "exclude", "proxy_only"} <= actual


def _valid_window() -> InvalidWindow:
    return InvalidWindow(
        start_time_ms=1_000,
        end_time_ms=2_000,
        family="microstructure_raw_aggtrades_v001",
        symbol="BTCUSDT",
        reason=InvalidWindowReason.MISSING_SEQUENCE,
        severity=InvalidWindowSeverity.WARN,
        downstream_eligibility_action=DownstreamEligibilityAction.FLAG,
        evidence={"missing_seq_count": 1, "expected": 100, "received": 102},
    )


def test_valid_window_constructs() -> None:
    w = _valid_window()
    assert w.symbol == "BTCUSDT"
    assert w.reason is InvalidWindowReason.MISSING_SEQUENCE


def test_end_before_start_rejected() -> None:
    with pytest.raises(ValueError):
        InvalidWindow(
            start_time_ms=2_000,
            end_time_ms=1_000,
            family="f",
            symbol="BTCUSDT",
            reason=InvalidWindowReason.MISSING_SEQUENCE,
            severity=InvalidWindowSeverity.WARN,
            downstream_eligibility_action=DownstreamEligibilityAction.FLAG,
            evidence={"k": "v"},
        )


def test_empty_family_rejected() -> None:
    with pytest.raises(ValueError):
        InvalidWindow(
            start_time_ms=1,
            end_time_ms=2,
            family="",
            symbol="BTCUSDT",
            reason=InvalidWindowReason.MISSING_SEQUENCE,
            severity=InvalidWindowSeverity.WARN,
            downstream_eligibility_action=DownstreamEligibilityAction.FLAG,
            evidence={"k": "v"},
        )


def test_empty_symbol_rejected() -> None:
    with pytest.raises(ValueError):
        InvalidWindow(
            start_time_ms=1,
            end_time_ms=2,
            family="f",
            symbol="",
            reason=InvalidWindowReason.MISSING_SEQUENCE,
            severity=InvalidWindowSeverity.WARN,
            downstream_eligibility_action=DownstreamEligibilityAction.FLAG,
            evidence={"k": "v"},
        )


def test_empty_evidence_rejected() -> None:
    with pytest.raises(ValueError):
        InvalidWindow(
            start_time_ms=1,
            end_time_ms=2,
            family="f",
            symbol="BTCUSDT",
            reason=InvalidWindowReason.MISSING_SEQUENCE,
            severity=InvalidWindowSeverity.WARN,
            downstream_eligibility_action=DownstreamEligibilityAction.FLAG,
            evidence={},
        )


def test_round_trip_to_from_dict() -> None:
    original = _valid_window()
    payload = original.to_dict()
    restored = InvalidWindow.from_dict(payload)
    assert restored == original


def test_to_dict_emits_string_enum_values() -> None:
    payload = _valid_window().to_dict()
    assert payload["reason"] == "missing_sequence"
    assert payload["severity"] == "warn"
    assert payload["downstream_eligibility_action"] == "flag"


def test_invalid_reason_string_rejected_on_round_trip() -> None:
    payload = _valid_window().to_dict()
    payload["reason"] = "not_a_reason"
    with pytest.raises(ValueError):
        InvalidWindow.from_dict(payload)


def test_frozen_dataclass_immutable() -> None:
    w = _valid_window()
    # frozen=True dataclasses raise FrozenInstanceError on attribute assignment.
    with pytest.raises((AttributeError, TypeError)):
        w.symbol = "ETHUSDT"  # type: ignore[misc]
