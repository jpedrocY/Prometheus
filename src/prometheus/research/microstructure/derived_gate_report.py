"""Phase 4bf gate report data model and JSON serialiser.

The derived-family gate report is written under
``data/microstructure/gate-reports/normalized/`` with paired
``.sha256`` sidecar via atomic write-then-rename + refuse-to-overwrite
discipline. The report serialises an exact list of 55 check results
plus boundary confirmations and result invariants.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .derived_gate_io import (
    GateIOError,
    GateReportPaths,
    atomic_write_json,
    derive_report_paths,
    write_sha256_sidecar,
)

REPORT_SCHEMA_VERSION = "v001"
PHASE_ID = "4bf"


@dataclass(frozen=True)
class DerivedAggTradesGateReport:
    """In-memory data model that mirrors the JSON gate report exactly."""

    report_schema_version: str
    phase_id: str
    report_id: str
    dataset_family: str
    dataset_version: str
    symbol: str
    utc_date: str
    generated_at_unix_ms: int
    code_commit_sha: str
    input_artefacts: dict[str, Any]
    checks: list[dict[str, Any]]
    overall_status: str
    research_eligible_after: bool
    eligibility_gate_status_after: str
    no_successor_authorization: bool
    boundary_confirmations: dict[str, bool]
    measured_summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def write_gate_report(
    report: DerivedAggTradesGateReport,
    *,
    output_root: Path,
    refuse_overwrite: bool = True,
) -> tuple[GateReportPaths, str, int]:
    """Write the report and paired SHA256 sidecar atomically.

    Returns ``(paths, report_sha256_hex, report_size_bytes)``.
    """
    if report.research_eligible_after is not False:
        raise GateIOError(
            "research_eligible_after must be False for the derived family"
        )
    if report.no_successor_authorization is not True:
        raise GateIOError("no_successor_authorization must be True")
    paths = derive_report_paths(
        output_root=output_root,
        dataset_family=report.dataset_family,
        dataset_version=report.dataset_version,
        generated_at_unix_ms=report.generated_at_unix_ms,
        code_commit_sha=report.code_commit_sha,
    )
    sha, size = atomic_write_json(
        paths.report_path, report.to_dict(), refuse_overwrite=refuse_overwrite
    )
    write_sha256_sidecar(
        paths.sidecar_path,
        target_filename=paths.report_path.name,
        sha256_hex=sha,
        refuse_overwrite=refuse_overwrite,
    )
    return paths, sha, size


def build_report(
    *,
    report_id: str,
    dataset_family: str,
    dataset_version: str,
    symbol: str,
    utc_date: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
    input_artefacts: Mapping[str, Any],
    checks: list[dict[str, Any]],
    overall_status: str,
    eligibility_gate_status_after: str,
    boundary_confirmations: Mapping[str, bool],
    measured_summary: Mapping[str, Any],
) -> DerivedAggTradesGateReport:
    """Construct a :class:`DerivedAggTradesGateReport` with hard invariants."""
    return DerivedAggTradesGateReport(
        report_schema_version=REPORT_SCHEMA_VERSION,
        phase_id=PHASE_ID,
        report_id=report_id,
        dataset_family=dataset_family,
        dataset_version=dataset_version,
        symbol=symbol,
        utc_date=utc_date,
        generated_at_unix_ms=generated_at_unix_ms,
        code_commit_sha=code_commit_sha,
        input_artefacts=dict(input_artefacts),
        checks=list(checks),
        overall_status=overall_status,
        research_eligible_after=False,
        eligibility_gate_status_after=eligibility_gate_status_after,
        no_successor_authorization=True,
        boundary_confirmations=dict(boundary_confirmations),
        measured_summary=dict(measured_summary),
    )
