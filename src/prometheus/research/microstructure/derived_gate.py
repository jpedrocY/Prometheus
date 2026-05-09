"""Phase 4bf derived-family eligibility-gate orchestrator.

Reads the Phase 4bd Stage-0 derived artefacts read-only, runs the 55
Phase 4bf-A checks, and (when ``write_report=True``) atomically emits a
JSON gate report plus paired SHA256 sidecar under
``data/microstructure/gate-reports/normalized/``. Never mutates any
source artefact. Never flips ``research_eligible``.
"""
from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

from .derived_gate_checks import (
    CHECK_ORDER,
    DerivedAggTradesCheckResult,
    DerivedAggTradesCheckStatus,
    DerivedGateContext,
    run_all_checks,
)
from .derived_gate_io import (
    GateIOError,
    assert_path_under_microstructure,
    compute_bytes_sha256,
    compute_file_sha256,
    parse_manifest_bytes,
    read_manifest_bytes,
    read_sidecar_first_64,
    resolve_derived_source_artefact_paths,
)
from .derived_gate_report import build_report, write_gate_report


class DerivedAggTradesGateInputError(Exception):
    """Raised on input-construction or path-discipline errors."""


class DerivedAggTradesGateUnsupportedError(Exception):
    """Raised on reserved-but-disabled features (e.g. successor manifest writing)."""


@dataclass(frozen=True)
class DerivedAggTradesGateInput:
    """Frozen orchestrator input."""

    derived_manifest_path: Path
    output_root: Path
    code_commit_sha: str
    write_report: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.derived_manifest_path, Path):
            raise DerivedAggTradesGateInputError("derived_manifest_path must be Path")
        if not isinstance(self.output_root, Path):
            raise DerivedAggTradesGateInputError("output_root must be Path")
        if not self.code_commit_sha or not isinstance(self.code_commit_sha, str):
            raise DerivedAggTradesGateInputError("code_commit_sha must be a non-empty str")
        try:
            assert_path_under_microstructure(
                self.derived_manifest_path, label="derived_manifest_path"
            )
            assert_path_under_microstructure(self.output_root, label="output_root")
        except GateIOError as exc:
            raise DerivedAggTradesGateInputError(str(exc)) from exc


@dataclass(frozen=True)
class DerivedAggTradesGateResult:
    """Frozen orchestrator result."""

    overall_status: DerivedAggTradesCheckStatus
    research_eligible_after: bool
    eligibility_gate_status_after: str
    no_successor_authorization: bool
    checks: tuple[DerivedAggTradesCheckResult, ...]
    report_path: Path | None
    report_id: str
    boundary_confirmations: dict[str, bool]
    measured_summary: dict[str, Any]
    invalid_window_candidates: tuple[Any, ...] = field(default_factory=tuple)


_BOUNDARY_KEYS = (
    "no_manifest_mutation",
    "no_normalization_written_outside_namespace",
    "no_data_microstructure_write_outside_gate_reports",
    "no_feature_computed",
    "no_label_computed",
    "no_signal_computed",
    "no_ml_trained",
    "no_strategy_created",
    "no_backtest_run",
    "no_network_io",
    "no_websocket",
    "no_credential_read",
    "no_env_read",
    "no_mcp_or_graphify",
    "research_eligible_after_is_false_for_derived_family",
)


def _classify_overall(
    checks: tuple[DerivedAggTradesCheckResult, ...],
) -> DerivedAggTradesCheckStatus:
    """Per Phase 4bf-A: PASS only if all PASS or NOT_APPLICABLE; FAIL > ERROR > PASS."""
    has_fail = any(c.status == DerivedAggTradesCheckStatus.FAIL for c in checks)
    if has_fail:
        return DerivedAggTradesCheckStatus.FAIL
    has_error = any(c.status == DerivedAggTradesCheckStatus.ERROR for c in checks)
    if has_error:
        return DerivedAggTradesCheckStatus.ERROR
    return DerivedAggTradesCheckStatus.PASS


def _build_boundary_confirmations(
    *,
    overall: DerivedAggTradesCheckStatus,
    derived_manifest_sha_pre: str,
    derived_manifest_sha_post: str,
    raw_manifest_sha_pre: str,
    raw_manifest_sha_post: str,
    raw_zip_sha_pre: str,
    raw_zip_sha_post: str,
    raw_sidecar_sha_pre: str,
    raw_sidecar_sha_post: str,
    acq_log_sha_pre: str,
    acq_log_sha_post: str,
    gate_report_sha_pre: str,
    gate_report_sha_post: str,
    normalized_parquet_sha_pre: str,
    normalized_parquet_sha_post: str,
) -> dict[str, bool]:
    no_mutation = (
        derived_manifest_sha_pre == derived_manifest_sha_post
        and raw_manifest_sha_pre == raw_manifest_sha_post
        and raw_zip_sha_pre == raw_zip_sha_post
        and raw_sidecar_sha_pre == raw_sidecar_sha_post
        and acq_log_sha_pre == acq_log_sha_post
        and gate_report_sha_pre == gate_report_sha_post
        and normalized_parquet_sha_pre == normalized_parquet_sha_post
    )
    confirmations = {key: True for key in _BOUNDARY_KEYS}
    confirmations["no_manifest_mutation"] = no_mutation
    # research_eligible_after_is_false_for_derived_family is invariant True;
    # PASS overall does not change that.
    confirmations["research_eligible_after_is_false_for_derived_family"] = True
    _ = overall  # the overall status is recorded in the report; no-op here.
    return confirmations


def run_derived_aggtrades_gate(
    inp: DerivedAggTradesGateInput,
) -> DerivedAggTradesGateResult:
    """Run the 55-check derived-family eligibility gate exactly once."""

    derived_manifest_bytes = read_manifest_bytes(inp.derived_manifest_path)
    derived_manifest_sha_pre = compute_bytes_sha256(derived_manifest_bytes)
    derived_manifest = parse_manifest_bytes(derived_manifest_bytes)

    derived_sidecar_path = Path(str(inp.derived_manifest_path) + ".sha256")
    derived_sidecar_first_64 = (
        read_sidecar_first_64(derived_sidecar_path) if derived_sidecar_path.exists() else ""
    )

    raw_manifest_path = (
        inp.derived_manifest_path.parent
        / "microstructure_raw_aggtrades_v001__v001.json"
    ).resolve()
    raw_manifest_bytes = read_manifest_bytes(raw_manifest_path)
    raw_manifest_sha_pre = compute_bytes_sha256(raw_manifest_bytes)
    raw_manifest = parse_manifest_bytes(raw_manifest_bytes)

    artefacts = resolve_derived_source_artefact_paths(
        derived_manifest_path=inp.derived_manifest_path,
        derived_manifest=derived_manifest,
        raw_manifest_path=raw_manifest_path,
        raw_manifest=raw_manifest,
    )

    normalized_parquet_sha_pre = compute_file_sha256(artefacts.normalized_parquet_path)
    normalized_sidecar_first_64 = (
        read_sidecar_first_64(artefacts.normalized_parquet_sidecar_path)
        if artefacts.normalized_parquet_sidecar_path.exists()
        else ""
    )
    raw_zip_sha_pre = compute_file_sha256(artefacts.raw_zip_path)
    raw_sidecar_sha_pre = compute_file_sha256(artefacts.raw_sidecar_path)
    raw_sidecar_first_64 = read_sidecar_first_64(artefacts.raw_sidecar_path)
    acq_log_sha_pre = compute_file_sha256(artefacts.acquisition_log_path)
    gate_report_sha_pre = compute_file_sha256(artefacts.gate_report_path)

    parquet_table = pq.read_table(artefacts.normalized_parquet_path)

    ctx = DerivedGateContext(
        derived_manifest_path=artefacts.derived_manifest_path,
        derived_manifest_sidecar_path=artefacts.derived_manifest_sidecar_path,
        normalized_parquet_path=artefacts.normalized_parquet_path,
        normalized_parquet_sidecar_path=artefacts.normalized_parquet_sidecar_path,
        raw_manifest_path=artefacts.raw_manifest_path,
        raw_zip_path=artefacts.raw_zip_path,
        raw_sidecar_path=artefacts.raw_sidecar_path,
        acquisition_log_path=artefacts.acquisition_log_path,
        gate_report_path=artefacts.gate_report_path,
        derived_manifest=derived_manifest,
        derived_manifest_bytes=derived_manifest_bytes,
        derived_manifest_sha=derived_manifest_sha_pre,
        derived_sidecar_first_64=derived_sidecar_first_64,
        normalized_parquet_sha=normalized_parquet_sha_pre,
        normalized_sidecar_first_64=normalized_sidecar_first_64,
        raw_manifest=raw_manifest,
        raw_manifest_sha=raw_manifest_sha_pre,
        raw_zip_sha=raw_zip_sha_pre,
        raw_sidecar_sha=raw_sidecar_sha_pre,
        raw_sidecar_first_64=raw_sidecar_first_64,
        acquisition_log_sha=acq_log_sha_pre,
        gate_report_sha=gate_report_sha_pre,
        parquet_table=parquet_table,
    )

    checks = run_all_checks(ctx)
    overall = _classify_overall(checks)
    if len(checks) != len(CHECK_ORDER):  # pragma: no cover - defensive
        raise DerivedAggTradesGateUnsupportedError(
            f"check count drift: got {len(checks)} expected {len(CHECK_ORDER)}"
        )

    # Re-hash all source artefacts post-checks to confirm immutability.
    derived_manifest_sha_post = compute_file_sha256(artefacts.derived_manifest_path)
    raw_manifest_sha_post = compute_file_sha256(artefacts.raw_manifest_path)
    raw_zip_sha_post = compute_file_sha256(artefacts.raw_zip_path)
    raw_sidecar_sha_post = compute_file_sha256(artefacts.raw_sidecar_path)
    acq_log_sha_post = compute_file_sha256(artefacts.acquisition_log_path)
    gate_report_sha_post = compute_file_sha256(artefacts.gate_report_path)
    normalized_parquet_sha_post = compute_file_sha256(artefacts.normalized_parquet_path)

    boundary_confirmations = _build_boundary_confirmations(
        overall=overall,
        derived_manifest_sha_pre=derived_manifest_sha_pre,
        derived_manifest_sha_post=derived_manifest_sha_post,
        raw_manifest_sha_pre=raw_manifest_sha_pre,
        raw_manifest_sha_post=raw_manifest_sha_post,
        raw_zip_sha_pre=raw_zip_sha_pre,
        raw_zip_sha_post=raw_zip_sha_post,
        raw_sidecar_sha_pre=raw_sidecar_sha_pre,
        raw_sidecar_sha_post=raw_sidecar_sha_post,
        acq_log_sha_pre=acq_log_sha_pre,
        acq_log_sha_post=acq_log_sha_post,
        gate_report_sha_pre=gate_report_sha_pre,
        gate_report_sha_post=gate_report_sha_post,
        normalized_parquet_sha_pre=normalized_parquet_sha_pre,
        normalized_parquet_sha_post=normalized_parquet_sha_post,
    )

    eligibility_gate_status_after = (
        "pass" if overall == DerivedAggTradesCheckStatus.PASS else "fail"
    )

    measured_summary: dict[str, Any] = {
        "derived_manifest_path": str(artefacts.derived_manifest_path),
        "derived_manifest_sha_pre": derived_manifest_sha_pre,
        "derived_manifest_sha_post": derived_manifest_sha_post,
        "normalized_parquet_path": str(artefacts.normalized_parquet_path),
        "normalized_parquet_sha_pre": normalized_parquet_sha_pre,
        "normalized_parquet_sha_post": normalized_parquet_sha_post,
        "raw_manifest_path": str(artefacts.raw_manifest_path),
        "raw_manifest_sha_pre": raw_manifest_sha_pre,
        "raw_manifest_sha_post": raw_manifest_sha_post,
        "raw_zip_path": str(artefacts.raw_zip_path),
        "raw_zip_sha_pre": raw_zip_sha_pre,
        "raw_zip_sha_post": raw_zip_sha_post,
        "raw_sidecar_sha_pre": raw_sidecar_sha_pre,
        "raw_sidecar_sha_post": raw_sidecar_sha_post,
        "acquisition_log_sha_pre": acq_log_sha_pre,
        "acquisition_log_sha_post": acq_log_sha_post,
        "gate_report_sha_pre": gate_report_sha_pre,
        "gate_report_sha_post": gate_report_sha_post,
        "row_count": parquet_table.num_rows,
        "expected_event_count": derived_manifest.get("event_count"),
    }

    input_artefacts: Mapping[str, Any] = {
        "derived_manifest_path": str(artefacts.derived_manifest_path),
        "derived_manifest_sha256": derived_manifest_sha_pre,
        "normalized_parquet_path": str(artefacts.normalized_parquet_path),
        "normalized_parquet_sha256": normalized_parquet_sha_pre,
        "raw_manifest_path": str(artefacts.raw_manifest_path),
        "raw_manifest_sha256": raw_manifest_sha_pre,
        "raw_zip_path": str(artefacts.raw_zip_path),
        "raw_zip_sha256": raw_zip_sha_pre,
        "raw_sidecar_sha256": raw_sidecar_sha_pre,
        "acquisition_log_path": str(artefacts.acquisition_log_path),
        "acquisition_log_sha256": acq_log_sha_pre,
        "raw_gate_report_path": str(artefacts.gate_report_path),
        "raw_gate_report_id": (
            (derived_manifest.get("governance_labels") or {}).get("source_gate_report_id")
            or ""
        ),
        "raw_gate_report_sha256": gate_report_sha_pre,
        "phase_4be_qa_memo_path": (
            "docs/00-meta/implementation-reports/"
            "2026-05-07_phase-4be_aggtrades-normalized-structural-qa.md"
        ),
        "phase_4be_closeout_path": (
            "docs/00-meta/implementation-reports/"
            "2026-05-07_phase-4be_closeout.md"
        ),
        "phase_4be_merge_closeout_path": (
            "docs/00-meta/implementation-reports/"
            "2026-05-07_phase-4be_merge-closeout.md"
        ),
    }

    generated_at_unix_ms = int(time.time() * 1000)
    short_commit = inp.code_commit_sha[:12]
    report_id = (
        f"microstructure_normalized_aggtrades_v001__v001__"
        f"{generated_at_unix_ms}__{short_commit}"
    )
    report_path: Path | None = None
    if inp.write_report:
        report = build_report(
            report_id=report_id,
            dataset_family="microstructure_normalized_aggtrades_v001",
            dataset_version="v001",
            symbol="BTCUSDT",
            utc_date="2025-01-15",
            generated_at_unix_ms=generated_at_unix_ms,
            code_commit_sha=inp.code_commit_sha,
            input_artefacts=input_artefacts,
            checks=[c.to_dict() for c in checks],
            overall_status=overall.value,
            eligibility_gate_status_after=eligibility_gate_status_after,
            boundary_confirmations=boundary_confirmations,
            measured_summary=measured_summary,
        )
        paths, _report_sha, _report_size = write_gate_report(
            report, output_root=inp.output_root, refuse_overwrite=True
        )
        report_path = paths.report_path
        report_id = paths.report_id

    return DerivedAggTradesGateResult(
        overall_status=overall,
        research_eligible_after=False,
        eligibility_gate_status_after=eligibility_gate_status_after,
        no_successor_authorization=True,
        checks=checks,
        report_path=report_path,
        report_id=report_id,
        boundary_confirmations=boundary_confirmations,
        measured_summary=measured_summary,
        invalid_window_candidates=(),
    )
