"""Phase 4bm-D multi-day derived-family gate report data model and writer.

The multi-day gate report is written under
``data/microstructure/gate-reports/normalized/`` with paired
``.sha256`` sidecar via atomic write-then-rename + refuse-to-overwrite
discipline. The report serialises 60 check results plus boundary
confirmations and the multi-day result invariants.

Mirrors :mod:`derived_gate_report` (Phase 4bf) but with multi-day
fields (``utc_date_start`` / ``utc_date_end`` / ``date_count`` instead
of a single ``utc_date``) and a multi-day ``gate_verdict`` taxonomy:

* ``DERIVED_GATE_PASS`` — every check PASS (and zero FAIL / ERROR /
  NOT_APPLICABLE).
* ``DERIVED_GATE_FAIL`` — at least one FAIL or ERROR.
* ``DERIVED_GATE_INCOMPLETE`` — at least one NOT_APPLICABLE and no
  FAIL / ERROR.

Two writer-level invariants are enforced unconditionally:

* ``research_eligible_after`` must be ``False`` (raises
  :class:`GateIOError` otherwise).
* ``no_successor_authorization`` must be ``True`` (raises
  :class:`GateIOError` otherwise).
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .multiday_derived_gate_io import (
    GateIOError,
    MultidayGateReportPaths,
    atomic_write_json,
    derive_report_paths,
    write_sha256_sidecar,
)

REPORT_SCHEMA_VERSION = "v001"
PHASE_ID = "4bm-d"

GATE_VERDICT_PASS = "DERIVED_GATE_PASS"
GATE_VERDICT_FAIL = "DERIVED_GATE_FAIL"
GATE_VERDICT_INCOMPLETE = "DERIVED_GATE_INCOMPLETE"

ALLOWED_GATE_VERDICTS: frozenset[str] = frozenset(
    {GATE_VERDICT_PASS, GATE_VERDICT_FAIL, GATE_VERDICT_INCOMPLETE}
)

ALLOWED_OVERALL_STATUSES: frozenset[str] = frozenset({"pass", "fail", "incomplete"})


@dataclass(frozen=True)
class MultidayDerivedAggTradesGateReport:
    """In-memory data model that mirrors the JSON multi-day gate report exactly."""

    report_schema_version: str
    phase_id: str
    report_id: str
    dataset_family: str
    dataset_version: str
    symbol: str
    utc_date_start: str
    utc_date_end: str
    date_count: int
    generated_at_unix_ms: int
    code_commit_sha: str
    input_artefacts: dict[str, Any]
    checks: list[dict[str, Any]]
    overall_status: str
    gate_verdict: str
    research_eligible_after: bool
    eligibility_gate_status_after: str
    no_successor_authorization: bool
    boundary_confirmations: dict[str, bool]
    measured_summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def write_gate_report(
    report: MultidayDerivedAggTradesGateReport,
    *,
    output_root: Path,
    refuse_overwrite: bool = True,
) -> tuple[MultidayGateReportPaths, str, int]:
    """Write the multi-day report and paired SHA256 sidecar atomically.

    Returns ``(paths, report_sha256_hex, report_size_bytes)``.

    Enforces both writer-level invariants
    (``research_eligible_after is False`` and
    ``no_successor_authorization is True``) before any path or file
    work happens; the report does not reach disk if either invariant
    is violated.
    """
    if report.research_eligible_after is not False:
        raise GateIOError(
            "research_eligible_after must be False for the derived family"
        )
    if report.no_successor_authorization is not True:
        raise GateIOError("no_successor_authorization must be True")
    if report.gate_verdict not in ALLOWED_GATE_VERDICTS:
        raise GateIOError(
            f"gate_verdict must be one of {sorted(ALLOWED_GATE_VERDICTS)!r}; "
            f"got {report.gate_verdict!r}"
        )
    if report.overall_status not in ALLOWED_OVERALL_STATUSES:
        raise GateIOError(
            f"overall_status must be one of {sorted(ALLOWED_OVERALL_STATUSES)!r}; "
            f"got {report.overall_status!r}"
        )
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
    utc_date_start: str,
    utc_date_end: str,
    date_count: int,
    generated_at_unix_ms: int,
    code_commit_sha: str,
    input_artefacts: Mapping[str, Any],
    checks: list[dict[str, Any]],
    overall_status: str,
    gate_verdict: str,
    eligibility_gate_status_after: str,
    boundary_confirmations: Mapping[str, bool],
    measured_summary: Mapping[str, Any],
) -> MultidayDerivedAggTradesGateReport:
    """Construct a :class:`MultidayDerivedAggTradesGateReport` with hard invariants.

    The constructor always sets ``research_eligible_after=False`` and
    ``no_successor_authorization=True``; the writer raises if either
    is later mutated by a caller using the unsafe constructor and
    then attempting to write.
    """
    return MultidayDerivedAggTradesGateReport(
        report_schema_version=REPORT_SCHEMA_VERSION,
        phase_id=PHASE_ID,
        report_id=report_id,
        dataset_family=dataset_family,
        dataset_version=dataset_version,
        symbol=symbol,
        utc_date_start=utc_date_start,
        utc_date_end=utc_date_end,
        date_count=date_count,
        generated_at_unix_ms=generated_at_unix_ms,
        code_commit_sha=code_commit_sha,
        input_artefacts=dict(input_artefacts),
        checks=list(checks),
        overall_status=overall_status,
        gate_verdict=gate_verdict,
        research_eligible_after=False,
        eligibility_gate_status_after=eligibility_gate_status_after,
        no_successor_authorization=True,
        boundary_confirmations=dict(boundary_confirmations),
        measured_summary=dict(measured_summary),
    )
