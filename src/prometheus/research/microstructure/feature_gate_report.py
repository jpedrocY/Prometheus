"""Phase 4bi-B feature-family eligibility-gate report data model and writer.

The feature-family gate report is written under
``data/microstructure/gate-reports/features/`` with paired
``.sha256`` sidecar via atomic write-then-rename + refuse-to-overwrite
discipline. The report serialises the locked invariant fields plus the
ordered list of stable feature-gate check results.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .feature_gate_io import (
    FeatureGateIOError,
    FeatureGateReportPaths,
    atomic_write_json,
    derive_feature_gate_report_paths,
    write_sha256_sidecar,
)

REPORT_SCHEMA_VERSION = "v001"
PHASE_ID = "4bi-B"


class FeatureGateReportError(RuntimeError):
    """Raised when a feature-gate report invariant is violated."""


@dataclass(frozen=True)
class FeatureGateReport:
    """In-memory data model that mirrors the JSON gate report exactly."""

    report_schema_version: str
    phase_id: str
    report_id: str
    dataset_family: str
    dataset_version: str
    feature_schema_version: str
    symbol: str
    utc_date: str
    generated_at_unix_ms: int
    code_commit_sha: str
    input_artefacts: dict[str, Any]
    expected_row_count: int
    observed_row_count: int
    expected_schema_columns: list[str]
    observed_schema_columns: list[str]
    expected_feature_columns: list[str]
    observed_feature_columns: list[str]
    expected_lineage_columns: list[str]
    observed_lineage_columns: list[str]
    feature_config_hash: str
    checks: list[dict[str, Any]]
    checks_total: int
    checks_pass: int
    checks_fail: int
    checks_error: int
    checks_not_applicable: int
    overall_status: str
    research_eligible_before: bool
    research_eligible_after: bool
    eligibility_gate_status_before: str
    eligibility_gate_status_after: str
    feature_manifest_research_eligible_after: bool
    feature_manifest_eligibility_gate_status_after: str
    stage_5_authorized: bool
    stage_5_research_or_ml_use: bool
    no_successor_authorization: bool
    boundary_confirmations: dict[str, bool]
    measured_summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_feature_gate_report(
    *,
    report_id: str,
    dataset_family: str,
    dataset_version: str,
    feature_schema_version: str,
    symbol: str,
    utc_date: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
    input_artefacts: Mapping[str, Any],
    expected_row_count: int,
    observed_row_count: int,
    expected_schema_columns: list[str],
    observed_schema_columns: list[str],
    expected_feature_columns: list[str],
    observed_feature_columns: list[str],
    expected_lineage_columns: list[str],
    observed_lineage_columns: list[str],
    feature_config_hash: str,
    checks: list[dict[str, Any]],
    overall_status: str,
    eligibility_gate_status_after: str,
    boundary_confirmations: Mapping[str, bool],
    measured_summary: Mapping[str, Any],
) -> FeatureGateReport:
    """Construct a :class:`FeatureGateReport` with hard invariants enforced."""
    counts = {"pass": 0, "fail": 0, "error": 0, "not_applicable": 0}
    for c in checks:
        s = str(c.get("status", "")).lower()
        if s in counts:
            counts[s] += 1
    return FeatureGateReport(
        report_schema_version=REPORT_SCHEMA_VERSION,
        phase_id=PHASE_ID,
        report_id=report_id,
        dataset_family=dataset_family,
        dataset_version=dataset_version,
        feature_schema_version=feature_schema_version,
        symbol=symbol,
        utc_date=utc_date,
        generated_at_unix_ms=generated_at_unix_ms,
        code_commit_sha=code_commit_sha,
        input_artefacts=dict(input_artefacts),
        expected_row_count=expected_row_count,
        observed_row_count=observed_row_count,
        expected_schema_columns=list(expected_schema_columns),
        observed_schema_columns=list(observed_schema_columns),
        expected_feature_columns=list(expected_feature_columns),
        observed_feature_columns=list(observed_feature_columns),
        expected_lineage_columns=list(expected_lineage_columns),
        observed_lineage_columns=list(observed_lineage_columns),
        feature_config_hash=feature_config_hash,
        checks=list(checks),
        checks_total=len(checks),
        checks_pass=counts["pass"],
        checks_fail=counts["fail"],
        checks_error=counts["error"],
        checks_not_applicable=counts["not_applicable"],
        overall_status=overall_status,
        research_eligible_before=False,
        research_eligible_after=False,
        eligibility_gate_status_before="pending",
        eligibility_gate_status_after=eligibility_gate_status_after,
        feature_manifest_research_eligible_after=False,
        feature_manifest_eligibility_gate_status_after="pending",
        stage_5_authorized=False,
        stage_5_research_or_ml_use=False,
        no_successor_authorization=True,
        boundary_confirmations=dict(boundary_confirmations),
        measured_summary=dict(measured_summary),
    )


def write_feature_gate_report(
    report: FeatureGateReport,
    *,
    output_root: Path,
    refuse_overwrite: bool = True,
) -> tuple[FeatureGateReportPaths, str, int]:
    """Write the report and paired SHA256 sidecar atomically.

    Returns ``(paths, report_sha256_hex, report_size_bytes)``. The
    invariants ``research_eligible_after = False`` and
    ``no_successor_authorization = True`` and
    ``feature_manifest_research_eligible_after = False`` and
    ``feature_manifest_eligibility_gate_status_after = "pending"`` and
    ``stage_5_authorized = False`` and
    ``stage_5_research_or_ml_use = False`` are checked before the write.
    """
    if report.research_eligible_after is not False:
        raise FeatureGateReportError(
            "research_eligible_after must be False for the feature family"
        )
    if report.feature_manifest_research_eligible_after is not False:
        raise FeatureGateReportError(
            "feature_manifest_research_eligible_after must be False"
        )
    if report.feature_manifest_eligibility_gate_status_after != "pending":
        raise FeatureGateReportError(
            "feature_manifest_eligibility_gate_status_after must be 'pending'"
        )
    if report.stage_5_authorized is not False:
        raise FeatureGateReportError("stage_5_authorized must be False")
    if report.stage_5_research_or_ml_use is not False:
        raise FeatureGateReportError("stage_5_research_or_ml_use must be False")
    if report.no_successor_authorization is not True:
        raise FeatureGateReportError("no_successor_authorization must be True")
    paths = derive_feature_gate_report_paths(
        output_root=output_root,
        dataset_family=report.dataset_family,
        dataset_version=report.dataset_version,
        generated_at_unix_ms=report.generated_at_unix_ms,
        code_commit_sha=report.code_commit_sha,
    )
    try:
        sha, size = atomic_write_json(
            paths.report_path,
            report.to_dict(),
            refuse_overwrite=refuse_overwrite,
        )
    except FeatureGateIOError:
        raise
    write_sha256_sidecar(
        paths.sidecar_path,
        target_filename=paths.report_path.name,
        sha256_hex=sha,
        refuse_overwrite=refuse_overwrite,
    )
    return paths, sha, size
