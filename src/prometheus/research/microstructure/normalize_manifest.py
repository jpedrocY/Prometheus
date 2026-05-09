"""Phase 4bd derived manifest builder for normalized aggTrades.

Builds the derived :class:`MicrostructureManifest` for the normalized
family ``microstructure_normalized_aggtrades_v001``. The manifest:

- defaults ``research_eligible=False`` and
  ``eligibility_gate_status=PENDING`` (Phase 4bd produces Stage-0
  derived artefacts only);
- preserves the Phase 4aw
  :meth:`MicrostructureManifest.flip_research_eligible` always-raises
  invariant;
- carries 14+ ``governance_labels`` keys with full lineage to the
  source manifest, raw zip, sidecar, acquisition log, and Phase 4bb-D
  gate report.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read ``.env`` / ``.mcp.json``, or import any networking library;
- does NOT write any file on its own. The orchestrator in
  :mod:`normalize_aggtrades` performs all writes via
  :mod:`normalize_io` helpers.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .invalid_window import InvalidWindow
from .manifest import EligibilityGateStatus, FileEntry, MicrostructureManifest

NORMALIZED_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
SOURCE_DATASET_FAMILY = "microstructure_raw_aggtrades_v001"

REQUIRED_GOVERNANCE_LABEL_KEYS: tuple[str, ...] = (
    "phase",
    "source_phase_boundary",
    "source_dataset_family",
    "source_dataset_version",
    "source_manifest_path",
    "source_manifest_sha256",
    "source_raw_zip_path",
    "source_raw_zip_sha256",
    "source_gate_report_id",
    "source_gate_report_sha256",
    "source_gate_report_code_commit_sha",
    "validator",
    "stop_trigger_domain",
    "feature_computation",
    "strategy_use",
)
"""The 15 required governance label keys for the derived manifest."""

FORBIDDEN_GOVERNANCE_LABEL_VALUES: Mapping[str, frozenset[str]] = {
    "feature_computation": frozenset({"allowed"}),
    "strategy_use": frozenset({"allowed"}),
}
"""Governance label values that must NOT appear at v001."""


class NormalizationManifestError(RuntimeError):
    """Raised when the derived manifest builder rejects an input."""


@dataclass(frozen=True)
class NormalizationManifestDraft:
    """Pre-manifest draft for the derived family.

    Converts to a :class:`MicrostructureManifest` via :meth:`to_manifest`.
    The conversion preserves ``research_eligible=False`` and
    ``eligibility_gate_status=PENDING`` defaults; the Phase 4aw
    always-raises invariant on ``flip_research_eligible`` is unchanged.
    """

    symbol: str
    utc_date: str
    start_time_ms: int
    end_time_ms: int
    event_count: int
    output_relative_path: str
    output_sha256: str
    governance_labels: dict[str, str]
    invalid_windows: tuple[InvalidWindow, ...]
    capture_config_hash: str
    code_commit_sha: str

    def __post_init__(self) -> None:
        # Symbol / date discipline
        if not isinstance(self.symbol, str) or not self.symbol.isalnum():
            raise NormalizationManifestError("symbol must be alphanumeric")
        if self.symbol != self.symbol.upper():
            raise NormalizationManifestError("symbol must be uppercase")
        if not isinstance(self.utc_date, str) or len(self.utc_date) != 10:
            raise NormalizationManifestError("utc_date must be YYYY-MM-DD")
        # Counts
        for label, value in (
            ("start_time_ms", self.start_time_ms),
            ("end_time_ms", self.end_time_ms),
            ("event_count", self.event_count),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise NormalizationManifestError(f"{label} must be an int")
            if value < 0:
                raise NormalizationManifestError(f"{label} must be >= 0")
        if self.end_time_ms < self.start_time_ms:
            raise NormalizationManifestError(
                "end_time_ms must be >= start_time_ms"
            )
        # Governance labels
        if not isinstance(self.governance_labels, dict):
            raise NormalizationManifestError("governance_labels must be a dict")
        missing = [
            k for k in REQUIRED_GOVERNANCE_LABEL_KEYS if k not in self.governance_labels
        ]
        if missing:
            raise NormalizationManifestError(
                f"governance_labels missing required keys: {missing}"
            )
        for k, forbidden_values in FORBIDDEN_GOVERNANCE_LABEL_VALUES.items():
            v = self.governance_labels.get(k, "")
            if v in forbidden_values:
                raise NormalizationManifestError(
                    f"governance_labels[{k!r}] must not be in {forbidden_values}"
                )
        # Hash discipline
        if len(self.output_sha256) != 64 or any(
            c not in "0123456789abcdef" for c in self.output_sha256
        ):
            raise NormalizationManifestError(
                "output_sha256 must be 64-char lowercase hex"
            )
        if not isinstance(self.output_relative_path, str) or not self.output_relative_path:
            raise NormalizationManifestError(
                "output_relative_path must be a non-empty string"
            )
        if not isinstance(self.capture_config_hash, str) or not self.capture_config_hash:
            raise NormalizationManifestError(
                "capture_config_hash must be a non-empty string"
            )
        if not isinstance(self.code_commit_sha, str) or not self.code_commit_sha:
            raise NormalizationManifestError(
                "code_commit_sha must be a non-empty string"
            )

    def to_manifest(self) -> MicrostructureManifest:
        """Build the Phase 4aw :class:`MicrostructureManifest` representation."""
        manifest = MicrostructureManifest(
            dataset_family=NORMALIZED_DATASET_FAMILY,
            version="v001",
            symbol=self.symbol,
            source=f"derived_from_{SOURCE_DATASET_FAMILY}",
            endpoint="derived",
            capture_mode="derived",
            schema_version="v001",
            endpoint_docs_reference="derived_no_endpoint",
            capture_config_hash=self.capture_config_hash,
            code_commit_sha=self.code_commit_sha,
            governance_labels=dict(self.governance_labels),
            research_eligible=False,
            eligibility_gate_status=EligibilityGateStatus.PENDING,
        )
        manifest.append_file(
            FileEntry(
                path=self.output_relative_path,
                sha256=self.output_sha256,
                event_count=self.event_count,
                start_time_ms=self.start_time_ms,
                end_time_ms=self.end_time_ms,
            )
        )
        for window in self.invalid_windows:
            manifest.append_invalid_window(window)
        return manifest


def propagate_invalid_windows(
    *,
    source_invalid_windows: tuple[InvalidWindow, ...] = (),
    normalization_runtime_invalid_windows: tuple[InvalidWindow, ...] = (),
) -> tuple[InvalidWindow, ...]:
    """Propagate invalid windows for the derived manifest.

    At v001:

    - source-derived invalid windows are propagated verbatim;
    - normalization-runtime invalid windows are appended after;
    - if any runtime entry has ``severity = ERROR``, the orchestrator
      must abort the run; this helper does not enforce that itself.
    """
    return tuple(source_invalid_windows) + tuple(normalization_runtime_invalid_windows)


__all__ = [
    "FORBIDDEN_GOVERNANCE_LABEL_VALUES",
    "NORMALIZED_DATASET_FAMILY",
    "NormalizationManifestDraft",
    "NormalizationManifestError",
    "REQUIRED_GOVERNANCE_LABEL_KEYS",
    "SOURCE_DATASET_FAMILY",
    "propagate_invalid_windows",
]
