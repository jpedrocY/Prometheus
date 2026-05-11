"""Phase 4bj-E label-family eligibility-gate report data model and writer.

The label-family gate report is written under
``data/microstructure/gate-reports/labels/`` with paired
``.sha256`` sidecar via atomic write-then-rename + refuse-to-overwrite
discipline. The report serialises the locked invariant fields plus the
ordered list of stable label-gate check results.

The label manifest is never mutated by this writer. The report invariant
``research_eligible_after = False`` is enforced before write.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .label_gate_io import (
    LabelGateIOError,
    LabelGateReportPaths,
    atomic_write_json,
    derive_label_gate_report_paths,
    write_sha256_sidecar,
)

REPORT_SCHEMA_VERSION = "v001"
PHASE_ID = "4bj-E"


class LabelGateReportError(RuntimeError):
    """Raised when a label-gate report invariant is violated."""


@dataclass(frozen=True)
class LabelGateReport:
    """In-memory data model that mirrors the JSON gate report exactly."""

    report_schema_version: str
    phase_id: str
    report_id: str
    dataset_family: str
    dataset_version: str
    label_schema_version: str
    symbol: str
    utc_date: str
    generated_at_unix_ms: int
    code_commit_sha: str
    input_artefacts: dict[str, Any]
    expected_row_count: int
    observed_row_count: int
    expected_schema_columns: list[str]
    observed_schema_columns: list[str]
    expected_label_columns: list[str]
    observed_label_columns: list[str]
    expected_support_columns: list[str]
    observed_support_columns: list[str]
    expected_lineage_columns: list[str]
    observed_lineage_columns: list[str]
    label_config_hash: str
    expected_invalid_price_row_count: int
    observed_invalid_price_row_count: int
    expected_censored_per_horizon: dict[str, int]
    observed_censored_per_horizon: dict[str, int]
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
    chronological_split_policy_before: str
    chronological_split_policy_after: str
    label_manifest_research_eligible_after: bool
    label_manifest_eligibility_gate_status_after: str
    label_manifest_chronological_split_policy_after: str
    stage_5_authorized: bool
    stage_5_research_or_ml_use: bool
    no_successor_authorization: bool
    boundary_confirmations: dict[str, bool]
    measured_summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_label_gate_report(
    *,
    report_id: str,
    dataset_family: str,
    dataset_version: str,
    label_schema_version: str,
    symbol: str,
    utc_date: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
    input_artefacts: Mapping[str, Any],
    expected_row_count: int,
    observed_row_count: int,
    expected_schema_columns: list[str],
    observed_schema_columns: list[str],
    expected_label_columns: list[str],
    observed_label_columns: list[str],
    expected_support_columns: list[str],
    observed_support_columns: list[str],
    expected_lineage_columns: list[str],
    observed_lineage_columns: list[str],
    label_config_hash: str,
    expected_invalid_price_row_count: int,
    observed_invalid_price_row_count: int,
    expected_censored_per_horizon: Mapping[str, int],
    observed_censored_per_horizon: Mapping[str, int],
    checks: list[dict[str, Any]],
    overall_status: str,
    eligibility_gate_status_after: str,
    boundary_confirmations: Mapping[str, bool],
    measured_summary: Mapping[str, Any],
) -> LabelGateReport:
    """Construct a :class:`LabelGateReport` with hard invariants enforced."""
    counts = {"pass": 0, "fail": 0, "error": 0, "not_applicable": 0}
    for c in checks:
        s = str(c.get("status", "")).lower()
        if s in counts:
            counts[s] += 1
    return LabelGateReport(
        report_schema_version=REPORT_SCHEMA_VERSION,
        phase_id=PHASE_ID,
        report_id=report_id,
        dataset_family=dataset_family,
        dataset_version=dataset_version,
        label_schema_version=label_schema_version,
        symbol=symbol,
        utc_date=utc_date,
        generated_at_unix_ms=generated_at_unix_ms,
        code_commit_sha=code_commit_sha,
        input_artefacts=dict(input_artefacts),
        expected_row_count=expected_row_count,
        observed_row_count=observed_row_count,
        expected_schema_columns=list(expected_schema_columns),
        observed_schema_columns=list(observed_schema_columns),
        expected_label_columns=list(expected_label_columns),
        observed_label_columns=list(observed_label_columns),
        expected_support_columns=list(expected_support_columns),
        observed_support_columns=list(observed_support_columns),
        expected_lineage_columns=list(expected_lineage_columns),
        observed_lineage_columns=list(observed_lineage_columns),
        label_config_hash=label_config_hash,
        expected_invalid_price_row_count=expected_invalid_price_row_count,
        observed_invalid_price_row_count=observed_invalid_price_row_count,
        expected_censored_per_horizon=dict(expected_censored_per_horizon),
        observed_censored_per_horizon=dict(observed_censored_per_horizon),
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
        chronological_split_policy_before="not_yet_defined",
        chronological_split_policy_after="not_yet_defined",
        label_manifest_research_eligible_after=False,
        label_manifest_eligibility_gate_status_after="pending",
        label_manifest_chronological_split_policy_after="not_yet_defined",
        stage_5_authorized=False,
        stage_5_research_or_ml_use=False,
        no_successor_authorization=True,
        boundary_confirmations=dict(boundary_confirmations),
        measured_summary=dict(measured_summary),
    )


def write_label_gate_report(
    report: LabelGateReport,
    *,
    output_root: Path,
    refuse_overwrite: bool = True,
) -> tuple[LabelGateReportPaths, str, int]:
    """Write the report and paired SHA256 sidecar atomically.

    Returns ``(paths, report_sha256_hex, report_size_bytes)``. Hard
    invariants are checked before the write:

    - ``research_eligible_after = False`` (the gate never flips the
      label family to research-eligible);
    - ``label_manifest_research_eligible_after = False`` and
      ``label_manifest_eligibility_gate_status_after = "pending"`` (the
      gate never mutates the on-disk manifest);
    - ``label_manifest_chronological_split_policy_after = "not_yet_defined"``;
    - ``stage_5_authorized = False`` and
      ``stage_5_research_or_ml_use = False``;
    - ``no_successor_authorization = True`` (no successor phase is
      authorized by gate output alone).
    """
    if report.research_eligible_after is not False:
        raise LabelGateReportError(
            "research_eligible_after must be False for the label family"
        )
    if report.label_manifest_research_eligible_after is not False:
        raise LabelGateReportError(
            "label_manifest_research_eligible_after must be False"
        )
    if report.label_manifest_eligibility_gate_status_after != "pending":
        raise LabelGateReportError(
            "label_manifest_eligibility_gate_status_after must be 'pending'"
        )
    if report.label_manifest_chronological_split_policy_after != "not_yet_defined":
        raise LabelGateReportError(
            "label_manifest_chronological_split_policy_after must be 'not_yet_defined'"
        )
    if report.stage_5_authorized is not False:
        raise LabelGateReportError("stage_5_authorized must be False")
    if report.stage_5_research_or_ml_use is not False:
        raise LabelGateReportError("stage_5_research_or_ml_use must be False")
    if report.no_successor_authorization is not True:
        raise LabelGateReportError("no_successor_authorization must be True")
    paths = derive_label_gate_report_paths(
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
    except LabelGateIOError:
        raise
    write_sha256_sidecar(
        paths.sidecar_path,
        target_filename=paths.report_path.name,
        sha256_hex=sha,
        refuse_overwrite=refuse_overwrite,
    )
    return paths, sha, size
