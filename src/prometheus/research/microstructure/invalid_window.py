"""Microstructure invalid-window taxonomy.

Phase 4aw scaffold-only. Defines the seventeen invalid-window reasons
catalogued in Phase 4au §23 and Phase 4av §17, plus severity and
downstream-eligibility-action enums and a frozen
:class:`InvalidWindow` data model.

Note on naming: Phase 2 introduced a separate ``InvalidWindow`` model
in :mod:`prometheus.research.data.manifests` for historical kline gap
tracking. This microstructure ``InvalidWindow`` covers stream- and
capture-related faults and is a distinct concept; the two coexist in
their own packages.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class InvalidWindowReason(StrEnum):
    """Seventeen invalid-window triggers (Phase 4au §23)."""

    MISSING_SEQUENCE = "missing_sequence"
    OUT_OF_ORDER_EVENT = "out_of_order_event"
    DUPLICATE_EVENT = "duplicate_event"
    GAP_AFTER_RECONNECT = "gap_after_reconnect"
    SNAPSHOT_MISMATCH = "snapshot_mismatch"
    CLOCK_SKEW = "clock_skew"
    SYMBOL_MISMATCH = "symbol_mismatch"
    STALE_STREAM = "stale_stream"
    STALE_BOOK = "stale_book"
    IMPOSSIBLE_SPREAD = "impossible_spread"
    NEGATIVE_SIZE = "negative_size"
    ZERO_OR_INVALID_PRICE = "zero_or_invalid_price"
    ARCHIVE_CHECKSUM_MISMATCH = "archive_checksum_mismatch"
    REST_RETENTION_GAP = "rest_retention_gap"
    FORCE_ORDER_PROXY_INCOMPLETENESS = "force_order_proxy_incompleteness"
    FAILED_ATOMIC_WRITE = "failed_atomic_write"
    PARTIAL_FILE_RECOVERY_EVENT = "partial_file_recovery_event"


class InvalidWindowSeverity(StrEnum):
    """Severity classification for a single invalid window."""

    INFO = "info"
    WARN = "warn"
    ERROR = "error"


class DownstreamEligibilityAction(StrEnum):
    """Action the future eligibility gate should take downstream."""

    FLAG = "flag"
    EXCLUDE = "exclude"
    PROXY_ONLY = "proxy_only"


@dataclass(frozen=True)
class InvalidWindow:
    """A single recorded invalid window for a microstructure dataset.

    ``evidence`` carries free-form structured context (sequence numbers,
    timestamps, observed values) and is required to be a non-empty
    mapping. Phase 4aw does not enforce a schema on the evidence
    contents — that is left to future eligibility-gate logic.
    """

    start_time_ms: int
    end_time_ms: int
    family: str
    symbol: str
    reason: InvalidWindowReason
    severity: InvalidWindowSeverity
    downstream_eligibility_action: DownstreamEligibilityAction
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.start_time_ms, int) or isinstance(self.start_time_ms, bool):
            raise ValueError("start_time_ms must be an int")
        if not isinstance(self.end_time_ms, int) or isinstance(self.end_time_ms, bool):
            raise ValueError("end_time_ms must be an int")
        if self.end_time_ms < self.start_time_ms:
            raise ValueError(
                f"end_time_ms ({self.end_time_ms}) must be >= "
                f"start_time_ms ({self.start_time_ms})"
            )
        if not isinstance(self.family, str) or not self.family:
            raise ValueError("family must be a non-empty string")
        if not isinstance(self.symbol, str) or not self.symbol:
            raise ValueError("symbol must be a non-empty string")
        if not isinstance(self.reason, InvalidWindowReason):
            raise ValueError("reason must be an InvalidWindowReason")
        if not isinstance(self.severity, InvalidWindowSeverity):
            raise ValueError("severity must be an InvalidWindowSeverity")
        if not isinstance(self.downstream_eligibility_action, DownstreamEligibilityAction):
            raise ValueError(
                "downstream_eligibility_action must be a DownstreamEligibilityAction"
            )
        if not isinstance(self.evidence, Mapping) or not self.evidence:
            raise ValueError("evidence must be a non-empty mapping")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-friendly ``dict`` (enums emitted as values)."""
        return {
            "start_time_ms": self.start_time_ms,
            "end_time_ms": self.end_time_ms,
            "family": self.family,
            "symbol": self.symbol,
            "reason": self.reason.value,
            "severity": self.severity.value,
            "downstream_eligibility_action": self.downstream_eligibility_action.value,
            "evidence": dict(self.evidence),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> InvalidWindow:
        """Round-trip from :meth:`to_dict` output."""
        return cls(
            start_time_ms=int(data["start_time_ms"]),
            end_time_ms=int(data["end_time_ms"]),
            family=str(data["family"]),
            symbol=str(data["symbol"]),
            reason=InvalidWindowReason(data["reason"]),
            severity=InvalidWindowSeverity(data["severity"]),
            downstream_eligibility_action=DownstreamEligibilityAction(
                data["downstream_eligibility_action"]
            ),
            evidence=dict(data["evidence"]),
        )
