"""Offline aggTrades eligibility-gate primitive (orchestrator + value objects).

Phase 4bb-C scope: value objects, enums, errors, and the public
:func:`run_eligibility_gate` orchestrator. The orchestrator composes
:mod:`eligibility_io`, :mod:`eligibility_checks`, and
:mod:`eligibility_report` to run all 45 Phase 4ba §10 eligibility-time
checks against a single Binance USDⓈ-M Futures aggTrades raw archive.

This module:

- runs offline-only (no Binance endpoint, no WebSocket, no credential,
  no ``.env`` / ``.mcp.json``);
- never mutates the original manifest, raw zip, sidecar, or
  acquisition log;
- never flips ``research_eligible`` to ``True`` for raw aggTrades
  families;
- writes only the gate report under
  ``data/microstructure/gate-reports/`` when ``write_report=True`` and
  ``output_root`` resolves under ``data/microstructure/``;
- always sets ``no_successor_authorization=True``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from .config import MicrostructureConfig
from .invalid_window import (
    DownstreamEligibilityAction,
    InvalidWindowReason,
    InvalidWindowSeverity,
)
from .manifest import EligibilityGateStatus


class AggTradesEligibilityCheckStatus(StrEnum):
    """Status of a single eligibility-time check."""

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


class AggTradesGateInputError(ValueError):
    """Raised when the gate input is malformed or fails an upstream guard."""


class AggTradesGateUnsupportedError(NotImplementedError):
    """Raised when a Phase 4bb-C-unsupported mode is requested.

    Phase 4bb-C does not support ``write_successor_manifest=True``. The flag
    is reserved for a separately authorized future phase.
    """


@dataclass(frozen=True)
class AggTradesEligibilityCheckResult:
    """Result of a single eligibility-time check."""

    check_id: str
    group: str
    title: str
    status: AggTradesEligibilityCheckStatus
    detail: str
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a JSON-friendly mapping."""
        return {
            "check_id": self.check_id,
            "group": self.group,
            "title": self.title,
            "status": self.status.value,
            "detail": self.detail,
            "evidence": dict(self.evidence),
        }


@dataclass(frozen=True)
class InvalidWindowCandidate:
    """An invalid-window candidate observed during the gate run.

    Recorded only inside the gate report. The original manifest's
    ``invalid_windows`` list is not mutated by Phase 4bb-C.
    """

    reason: InvalidWindowReason
    severity: InvalidWindowSeverity
    downstream_eligibility_action: DownstreamEligibilityAction
    start_time_ms: int
    end_time_ms: int
    family: str
    symbol: str
    evidence: Mapping[str, Any]
    discovered_by_check_id: str

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a JSON-friendly mapping."""
        return {
            "reason": self.reason.value,
            "severity": self.severity.value,
            "downstream_eligibility_action": self.downstream_eligibility_action.value,
            "start_time_ms": self.start_time_ms,
            "end_time_ms": self.end_time_ms,
            "family": self.family,
            "symbol": self.symbol,
            "evidence": dict(self.evidence),
            "discovered_by_check_id": self.discovered_by_check_id,
        }


@dataclass(frozen=True)
class AggTradesEligibilityGateInput:
    """Input contract for :func:`run_eligibility_gate`.

    The optional ``family_subdir`` field (Phase 4bb-F-implementation)
    selects canonical gate-report placement under
    ``<output_root>/<family_subdir>/`` instead of the legacy
    ``<output_root>/gate-reports/``. The default (``None``) preserves
    Phase 4bb-C placement verbatim so existing call sites are unchanged.

    The optional ``phase_id`` field (Phase 4bb-F-implementation), when
    provided, switches the report identifier to the Phase 4bb-F canonical
    format ``<family>__<version>__phase-<id>__<unix_ms>__<short>``. The
    default (``None``) preserves the Phase 4bb-C identifier format
    ``<family>__<version>__<unix_ms>__<short>``.
    """

    manifest_path: Path
    output_root: Path
    code_commit_sha: str
    write_report: bool = True
    write_successor_manifest: bool = False
    explicit_extra_symbols: tuple[str, ...] = ()
    config: MicrostructureConfig | None = None
    family_subdir: str | None = None
    phase_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.manifest_path, Path):
            raise AggTradesGateInputError("manifest_path must be a pathlib.Path")
        if not isinstance(self.output_root, Path):
            raise AggTradesGateInputError("output_root must be a pathlib.Path")
        if not isinstance(self.code_commit_sha, str) or not self.code_commit_sha:
            raise AggTradesGateInputError(
                "code_commit_sha must be a non-empty string"
            )
        if not isinstance(self.write_report, bool):
            raise AggTradesGateInputError("write_report must be a bool")
        if not isinstance(self.write_successor_manifest, bool):
            raise AggTradesGateInputError(
                "write_successor_manifest must be a bool"
            )
        # Phase 4bb-C reserves write_successor_manifest=True. It must remain
        # False; a True value indicates the caller is using an unsupported
        # mode that requires a separately authorized future phase.
        if self.write_successor_manifest:
            raise AggTradesGateUnsupportedError(
                "write_successor_manifest=True is reserved for a future, "
                "separately authorized eligibility-gate phase. Phase 4bb-C "
                "does not support this mode."
            )
        if self.family_subdir is not None:
            if (
                not isinstance(self.family_subdir, str)
                or not self.family_subdir
            ):
                raise AggTradesGateInputError(
                    "family_subdir must be a non-empty string when provided"
                )
            if "/" in self.family_subdir or "\\" in self.family_subdir:
                raise AggTradesGateInputError(
                    "family_subdir must not contain path separators"
                )
        if self.phase_id is not None and (
            not isinstance(self.phase_id, str) or not self.phase_id
        ):
            raise AggTradesGateInputError(
                "phase_id must be a non-empty string when provided"
            )


@dataclass(frozen=True)
class AggTradesEligibilityGateResult:
    """Result of a full eligibility-gate run."""

    overall_status: AggTradesEligibilityCheckStatus
    research_eligible_after: bool
    eligibility_gate_status_after: EligibilityGateStatus
    checks: tuple[AggTradesEligibilityCheckResult, ...]
    invalid_window_candidates: tuple[InvalidWindowCandidate, ...]
    measured_summary: Mapping[str, Any]
    boundary_confirmations: Mapping[str, bool]
    no_successor_authorization: bool
    report_path: Path | None
    report_id: str

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a JSON-friendly mapping (used for the gate report)."""
        return {
            "overall_status": self.overall_status.value,
            "research_eligible_after": self.research_eligible_after,
            "eligibility_gate_status_after": self.eligibility_gate_status_after.value,
            "checks": [c.to_dict() for c in self.checks],
            "invalid_window_candidates": [
                w.to_dict() for w in self.invalid_window_candidates
            ],
            "measured_summary": dict(self.measured_summary),
            "boundary_confirmations": dict(self.boundary_confirmations),
            "no_successor_authorization": self.no_successor_authorization,
            "report_path": str(self.report_path) if self.report_path else None,
            "report_id": self.report_id,
        }


REQUIRED_BOUNDARY_KEYS: tuple[str, ...] = (
    "no_network_io",
    "no_credential_read",
    "no_env_read",
    "no_websocket",
    "no_mcp_or_graphify",
    "no_normalization_written",
    "no_feature_computed",
    "no_strategy_created",
    "no_ml_trained",
    "no_backtest_run",
    "no_manifest_mutation",
    "no_data_microstructure_write_outside_gate_reports",
    "research_eligible_after_is_false_for_raw_family",
)
"""Required keys for the ``boundary_confirmations`` dict."""


def _aggregate_overall_status(
    checks: tuple[AggTradesEligibilityCheckResult, ...],
) -> AggTradesEligibilityCheckStatus:
    """Aggregate per-check statuses into a single overall status."""
    has_fail = any(c.status is AggTradesEligibilityCheckStatus.FAIL for c in checks)
    has_error = any(
        c.status is AggTradesEligibilityCheckStatus.ERROR for c in checks
    )
    if has_fail:
        return AggTradesEligibilityCheckStatus.FAIL
    if has_error:
        return AggTradesEligibilityCheckStatus.ERROR
    return AggTradesEligibilityCheckStatus.PASS


def _gate_status_for_overall(
    overall: AggTradesEligibilityCheckStatus,
) -> EligibilityGateStatus:
    """Map an overall check status to a recommended gate status."""
    if overall is AggTradesEligibilityCheckStatus.PASS:
        return EligibilityGateStatus.PASS
    if overall is AggTradesEligibilityCheckStatus.FAIL:
        return EligibilityGateStatus.FAIL
    return EligibilityGateStatus.PENDING


def _make_report_id(
    dataset_family: str,
    version: str,
    code_commit_sha: str,
    created_at_utc_ms: int,
    *,
    phase_id: str | None = None,
) -> str:
    """Construct a deterministic-ish report identifier.

    When *phase_id* is ``None`` (the default), the Phase 4bb-C identifier
    format is used: ``<family>__<version>__<unix_ms>__<short>``.

    When *phase_id* is a non-empty string, the Phase 4bb-F canonical
    identifier format is used:
    ``<family>__<version>__phase-<phase_id>__<unix_ms>__<short>``.
    """
    short = code_commit_sha[:12] if code_commit_sha else "no_sha"
    if phase_id is None:
        return f"{dataset_family}__{version}__{created_at_utc_ms}__{short}"
    return (
        f"{dataset_family}__{version}__phase-{phase_id}__"
        f"{created_at_utc_ms}__{short}"
    )


def _now_utc_ms() -> int:
    """Return current UTC time in milliseconds."""
    return int(datetime.now(UTC).timestamp() * 1000)


def run_eligibility_gate(
    inp: AggTradesEligibilityGateInput,
) -> AggTradesEligibilityGateResult:
    """Run the full offline aggTrades eligibility gate.

    The orchestrator is intentionally narrow: it loads the read-only
    artefacts, builds an immutable :class:`GateExecutionContext`, runs all
    45 Phase 4ba §10 checks, recomputes the manifest / raw-zip / sidecar
    bytes hashes after the run to verify no mutation occurred, optionally
    writes a JSON gate report under ``data/microstructure/gate-reports/``
    via :class:`raw_writer.RawWriter`, and returns an in-memory
    :class:`AggTradesEligibilityGateResult`.

    The function never mutates the original manifest, raw zip, sidecar, or
    acquisition log. It never flips ``research_eligible`` to ``True`` for
    raw aggTrades families. It never authorises any successor phase.
    """
    # Late imports avoid a hot import cycle with eligibility_checks /
    # eligibility_report and keep run_eligibility_gate's import surface
    # tight at module-import time.
    from . import eligibility_checks as _checks
    from . import eligibility_io as _io
    from . import eligibility_report as _report

    # The static import-boundary scan in
    # tests/research/microstructure/test_import_boundaries.py and
    # tests/research/microstructure/test_eligibility_no_network.py
    # already verifies that none of the gate's own modules can reach a
    # networking / credential helper. The orchestrator does NOT add a
    # runtime sys.modules check because the same Python process may have
    # imported third-party modules for unrelated reasons (e.g. other test
    # suites in the same pytest session). The static guarantee is the
    # binding one.
    #
    # Path discipline: manifest_path must be readable; output_root must
    # resolve under data/microstructure/.
    _io.assert_path_under_microstructure(inp.manifest_path, label="manifest_path")
    _io.assert_path_under_microstructure(inp.output_root, label="output_root")

    artefacts = _io.resolve_artefact_paths(inp.manifest_path)

    # Read manifest read-only and snapshot bytes for the hash-before/after
    # immutability check.
    manifest, manifest_sha_before, manifest_len_before = _io.read_manifest_and_hash(
        artefacts.manifest_path
    )

    # Snapshot raw zip and sidecar pre-hashes (cheap; sidecar is tiny).
    raw_zip_sha_before, raw_zip_size_before = _io.compute_file_sha256(
        artefacts.raw_zip_path
    ) if artefacts.raw_zip_path.exists() else ("__missing__", 0)
    sidecar_text = ""
    sidecar_first_64 = ""
    sidecar_sha_before = ""
    if artefacts.sidecar_path.exists():
        sidecar_text, sidecar_first_64 = _io.read_sidecar(artefacts.sidecar_path)
        sidecar_sha_before = _io.compute_bytes_sha256(
            artefacts.sidecar_path.read_bytes()
        )

    acquisition_log: dict[str, Any] = {}
    acquisition_log_sha = ""
    if artefacts.acquisition_log_path.exists():
        try:
            acquisition_log, acquisition_log_sha = _io.read_acquisition_log(
                artefacts.acquisition_log_path
            )
        except Exception:  # noqa: BLE001 — recorded as ERROR check downstream
            acquisition_log = {}
            acquisition_log_sha = ""

    # Single-pass row scan (in memory; no decompression to disk).
    expected_utc_day_start = _io.utc_day_start_from_archive_path(
        artefacts.raw_zip_path
    )
    if artefacts.raw_zip_path.exists():
        (
            row_scan,
            anomalies,
            csv_uncompressed_size,
            member_names,
            decompression_ok,
            decompression_error,
        ) = _io.scan_csv_rows_in_zip(
            artefacts.raw_zip_path,
            expected_utc_day_start=expected_utc_day_start,
        )
    else:
        row_scan = _io.RowScanSummary()
        anomalies = []
        csv_uncompressed_size = 0
        member_names = ()
        decompression_ok = False
        decompression_error = "raw_zip_path does not exist"

    artefact_read = _io.ArtefactReadResult(
        manifest=manifest,
        manifest_bytes_sha256=manifest_sha_before,
        manifest_bytes_len=manifest_len_before,
        raw_zip_sha256=raw_zip_sha_before,
        raw_zip_size=raw_zip_size_before,
        sidecar_text=sidecar_text,
        sidecar_first_64_hex=sidecar_first_64,
        acquisition_log=acquisition_log,
        acquisition_log_bytes_sha256=acquisition_log_sha,
        csv_member_count=len(member_names),
        csv_member_names=member_names,
        primary_csv_name=member_names[0] if len(member_names) == 1 else "",
        primary_csv_uncompressed_size=csv_uncompressed_size,
        row_scan=row_scan,
        decompression_ok=decompression_ok,
        decompression_error=decompression_error,
    )

    # Run all 45 checks against an immutable execution context.
    ctx = _checks.GateExecutionContext(
        inp=inp,
        artefacts=artefacts,
        artefact_read=artefact_read,
        anomalies=tuple(anomalies),
        expected_utc_day_start_ms=expected_utc_day_start,
    )

    check_results, candidates = _checks.run_all_checks(ctx)

    if len(check_results) != 45:  # pragma: no cover — defensive
        raise AggTradesGateInputError(
            f"internal error: expected 45 checks, got {len(check_results)}"
        )

    # Recompute manifest / raw-zip / sidecar hashes AFTER the checks.
    manifest_sha_after = _io.compute_bytes_sha256(
        artefacts.manifest_path.read_bytes()
    )
    raw_zip_sha_after = (
        _io.compute_file_sha256(artefacts.raw_zip_path)[0]
        if artefacts.raw_zip_path.exists()
        else "__missing__"
    )
    sidecar_sha_after = (
        _io.compute_bytes_sha256(artefacts.sidecar_path.read_bytes())
        if artefacts.sidecar_path.exists()
        else ""
    )

    no_manifest_mutation = manifest_sha_before == manifest_sha_after
    no_raw_zip_mutation = raw_zip_sha_before == raw_zip_sha_after
    no_sidecar_mutation = sidecar_sha_before == sidecar_sha_after

    overall = _aggregate_overall_status(check_results)
    if not (no_manifest_mutation and no_raw_zip_mutation and no_sidecar_mutation):
        # Defensive: flip overall to FAIL if any artefact was mutated.
        overall = AggTradesEligibilityCheckStatus.FAIL

    research_eligible_after = False  # invariant for raw aggTrades families.
    eligibility_gate_status_after = _gate_status_for_overall(overall)

    boundary_confirmations: dict[str, bool] = {
        "no_network_io": True,
        "no_credential_read": True,
        "no_env_read": True,
        "no_websocket": True,
        "no_mcp_or_graphify": True,
        "no_normalization_written": True,
        "no_feature_computed": True,
        "no_strategy_created": True,
        "no_ml_trained": True,
        "no_backtest_run": True,
        "no_manifest_mutation": no_manifest_mutation
        and no_raw_zip_mutation
        and no_sidecar_mutation,
        "no_data_microstructure_write_outside_gate_reports": True,
        "research_eligible_after_is_false_for_raw_family": (
            research_eligible_after is False
        ),
    }
    # Sanity: every required boundary key present.
    for required in REQUIRED_BOUNDARY_KEYS:
        if required not in boundary_confirmations:
            raise AggTradesGateInputError(
                f"internal error: missing boundary key {required!r}"
            )

    measured_summary: dict[str, Any] = {
        "manifest_sha_before": manifest_sha_before,
        "manifest_sha_after": manifest_sha_after,
        "raw_zip_sha_before": raw_zip_sha_before,
        "raw_zip_sha_after": raw_zip_sha_after,
        "sidecar_sha_before": sidecar_sha_before,
        "sidecar_sha_after": sidecar_sha_after,
        "raw_zip_size_bytes": raw_zip_size_before,
        "csv_uncompressed_size": csv_uncompressed_size,
        "csv_member_count": len(member_names),
        "row_count": row_scan.row_count,
        "first_T_ms": row_scan.first_T,
        "last_T_ms": row_scan.last_T,
        "min_a": row_scan.min_a,
        "max_a": row_scan.max_a,
        "duplicate_a_count": row_scan.duplicate_a_count,
        "out_of_order_a_count": row_scan.out_of_order_a_count,
        "largest_consecutive_a_gap": row_scan.largest_consecutive_a_gap,
        "m_true_count": row_scan.m_true_count,
        "m_false_count": row_scan.m_false_count,
        "m_unparsed_count": row_scan.m_unparsed_count,
        "validator_failures": row_scan.validator_failures,
        "in_day_count": row_scan.in_day_count,
        "out_day_count": row_scan.out_day_count,
        "csv_column_order": list(row_scan.csv_column_order),
        "unexpected_extra_columns": list(row_scan.unexpected_extra_columns),
        "hour_counts": list(row_scan.hour_counts),
        "decompression_ok": decompression_ok,
        "decompression_error": decompression_error,
        "expected_utc_day_start_ms": expected_utc_day_start,
        "anomaly_count": len(anomalies),
    }

    created_at_utc_ms = _now_utc_ms()
    report_id = _make_report_id(
        manifest.dataset_family,
        manifest.version,
        inp.code_commit_sha,
        created_at_utc_ms,
        phase_id=inp.phase_id,
    )

    # Build and (optionally) write the report.
    report = _report.AggTradesGateReport(
        report_id=report_id,
        dataset_family=manifest.dataset_family,
        version=manifest.version,
        symbol=manifest.symbol,
        source_manifest_path=str(artefacts.manifest_path),
        raw_zip_path=str(artefacts.raw_zip_path),
        sidecar_path=str(artefacts.sidecar_path),
        acquisition_log_path=str(artefacts.acquisition_log_path),
        created_at_utc_ms=created_at_utc_ms,
        code_commit_sha=inp.code_commit_sha,
        overall_status=overall.value,
        research_eligible_after=research_eligible_after,
        eligibility_gate_status_after=eligibility_gate_status_after.value,
        checks=tuple(c.to_dict() for c in check_results),
        invalid_window_candidates=tuple(c.to_dict() for c in candidates),
        measured_summary=measured_summary,
        boundary_confirmations=boundary_confirmations,
        no_successor_authorization=True,
    )

    report_path: Path | None = None
    if inp.write_report:
        report_path = _report.write_report_atomic(
            report,
            inp.output_root,
            family_subdir=inp.family_subdir,
        )

    return AggTradesEligibilityGateResult(
        overall_status=overall,
        research_eligible_after=research_eligible_after,
        eligibility_gate_status_after=eligibility_gate_status_after,
        checks=check_results,
        invalid_window_candidates=candidates,
        measured_summary=measured_summary,
        boundary_confirmations=boundary_confirmations,
        no_successor_authorization=True,
        report_path=report_path,
        report_id=report_id,
    )
