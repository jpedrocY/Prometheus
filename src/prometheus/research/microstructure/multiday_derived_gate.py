"""Phase 4bm-D multi-day derived-family eligibility-gate orchestrator.

This module is the multi-day analogue of :mod:`derived_gate` (Phase 4bf).

It reads the Phase 4bm-B v002 multi-day derived family read-only,
walks the full 90-entry per_file_inventory using cheap per-file
measurements (streaming SHA + size + ``pyarrow.parquet.ParquetFile``
metadata-only row counts), additionally loads full ``pyarrow.Table``
content for a bounded predeclared sample of dates
(:data:`SAMPLE_DATES`), runs the full 60-check
:data:`CHECK_ORDER` suite, derives the three-state verdict
(``DERIVED_GATE_PASS`` / ``DERIVED_GATE_FAIL`` /
``DERIVED_GATE_INCOMPLETE``), re-hashes every governance artefact +
every per-file Parquet + every raw zip post-checks for immutability,
and (when ``write_report=True``) atomically emits one gate report
JSON + paired ``.sha256`` sidecar under
``data/microstructure/gate-reports/normalized/``.

Hard invariants enforced unconditionally:

* the orchestrator never mutates the derived manifest, any of the 90
  Parquets or sidecars, the raw v002 manifest, the 90 raw zips, the
  acquisition log, the Phase 4bl-D-R gate report, the Phase 4bl-E
  successor-state record, or any other on-disk governance artefact;
* ``research_eligible_after`` is hard-wired to ``False`` and
  ``no_successor_authorization`` to ``True`` on every emitted
  result; the writer in :mod:`multiday_derived_gate_report` also
  refuses to serialise any report that violates those invariants;
* no network I/O, no credentials, no ``.env`` reads, no MCP /
  Graphify hooks. The static no-network scan in
  ``tests/research/microstructure/test_multiday_derived_gate_no_network.py``
  enforces the source-level guarantee.

Performance discipline: the gate must not load all 90 Parquets fully
into memory (the dataset is ~155 M events / ~1.4 GiB). Per-file row
counts come from ``ParquetFile.metadata.num_rows`` without
materialising row groups. Full per-row content checks are bounded
to :data:`SAMPLE_DATES`. SHA hashing is streamed in 1 MiB chunks.
"""
from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

from .multiday_derived_gate_checks import (
    CANONICAL_DATASET_FAMILY,
    CANONICAL_DATASET_VERSION,
    CANONICAL_DATE_END,
    CANONICAL_DATE_START,
    CANONICAL_SYMBOL,
    CHECK_ORDER,
    EXPECTED_DATE_COUNT,
    PHASE_4BMC_CLOSEOUT_PATH,
    PHASE_4BMC_MERGE_CLOSEOUT_PATH,
    PHASE_4BMC_QA_PATH,
    SAMPLE_DATES,
    MultidayDerivedAggTradesCheckResult,
    MultidayDerivedAggTradesCheckStatus,
    MultidayDerivedGateContext,
    MultidayPerFileMeasured,
    run_all_checks,
)
from .multiday_derived_gate_io import (
    GateIOError,
    MultidayDerivedSourceArtefactPaths,
    MultidayLoadedArtefactBundle,
    MultidayPerFileArtefactPaths,
    assert_path_under_microstructure,
    compute_bytes_sha256,
    compute_file_sha256,
    compute_file_size,
    parse_manifest_bytes,
    read_manifest_bytes,
    read_sidecar_first_64,
    resolve_multiday_derived_source_artefact_paths,
)
from .multiday_derived_gate_report import (
    GATE_VERDICT_FAIL,
    GATE_VERDICT_INCOMPLETE,
    GATE_VERDICT_PASS,
    build_report,
    write_gate_report,
)


class MultidayDerivedAggTradesGateInputError(Exception):
    """Raised on input-construction or path-discipline errors."""


class MultidayDerivedAggTradesGateUnsupportedError(Exception):
    """Raised on reserved-but-disabled features (e.g. successor manifest writing)."""


@dataclass(frozen=True)
class MultidayDerivedAggTradesGateInput:
    """Frozen orchestrator input."""

    derived_manifest_path: Path
    output_root: Path
    code_commit_sha: str
    write_report: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.derived_manifest_path, Path):
            raise MultidayDerivedAggTradesGateInputError(
                "derived_manifest_path must be Path"
            )
        if not isinstance(self.output_root, Path):
            raise MultidayDerivedAggTradesGateInputError(
                "output_root must be Path"
            )
        if not self.code_commit_sha or not isinstance(self.code_commit_sha, str):
            raise MultidayDerivedAggTradesGateInputError(
                "code_commit_sha must be a non-empty str"
            )
        try:
            assert_path_under_microstructure(
                self.derived_manifest_path, label="derived_manifest_path"
            )
            assert_path_under_microstructure(
                self.output_root, label="output_root"
            )
        except GateIOError as exc:
            raise MultidayDerivedAggTradesGateInputError(str(exc)) from exc


@dataclass(frozen=True)
class MultidayDerivedAggTradesGateResult:
    """Frozen orchestrator result."""

    overall_status: str
    gate_verdict: str
    research_eligible_after: bool
    eligibility_gate_status_after: str
    no_successor_authorization: bool
    checks: tuple[MultidayDerivedAggTradesCheckResult, ...]
    report_path: Path | None
    report_id: str
    boundary_confirmations: dict[str, bool]
    measured_summary: dict[str, Any]
    invalid_window_candidates: tuple[Any, ...] = field(default_factory=tuple)


# Boundary confirmation keys recorded on every result (multi-day analogue
# of the Phase 4bf ``_BOUNDARY_KEYS`` list, extended with multi-day
# specific keys that track the 90-Parquet immutability invariant).
_BOUNDARY_KEYS: tuple[str, ...] = (
    "no_manifest_mutation",
    "no_per_file_parquet_mutation",
    "no_per_file_sidecar_mutation",
    "no_raw_zip_mutation",
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
    "no_successor_authorization",
)


def _classify_overall_status(
    checks: tuple[MultidayDerivedAggTradesCheckResult, ...],
) -> str:
    """Return the textual ``overall_status`` for the report.

    The taxonomy is:

    * ``pass`` — every check PASS (no FAIL, no ERROR, no NOT_APPLICABLE);
    * ``incomplete`` — at least one NOT_APPLICABLE and no FAIL / ERROR;
    * ``fail`` — at least one FAIL or ERROR.

    FAIL dominates ERROR, which dominates NOT_APPLICABLE, which
    dominates PASS, matching the Phase 4bf classifier semantics
    extended for the multi-day three-state verdict.
    """
    has_fail = any(
        c.status == MultidayDerivedAggTradesCheckStatus.FAIL for c in checks
    )
    has_error = any(
        c.status == MultidayDerivedAggTradesCheckStatus.ERROR for c in checks
    )
    has_na = any(
        c.status == MultidayDerivedAggTradesCheckStatus.NOT_APPLICABLE for c in checks
    )
    if has_fail or has_error:
        return "fail"
    if has_na:
        return "incomplete"
    return "pass"


def _classify_gate_verdict(overall_status: str) -> str:
    """Map ``overall_status`` to the Phase 4bm-D gate verdict taxonomy."""
    if overall_status == "pass":
        return GATE_VERDICT_PASS
    if overall_status == "incomplete":
        return GATE_VERDICT_INCOMPLETE
    return GATE_VERDICT_FAIL


def _measure_per_file(
    paths_per_file: tuple[MultidayPerFileArtefactPaths, ...],
    *,
    sample_dates: frozenset[str],
) -> dict[str, MultidayPerFileMeasured]:
    """Walk all 90 per-file entries and take cheap measurements.

    For every date:

    * stream the Parquet SHA256 in 1 MiB chunks,
    * record the on-disk Parquet size,
    * stream the sidecar SHA256, read its first-64 chars, record size,
    * stream the source zip SHA256,
    * open the Parquet via ``ParquetFile`` and record
      ``metadata.num_rows`` (no row-group materialisation).

    For dates in ``sample_dates`` only: additionally load the full
    ``pyarrow.Table`` for use by the per-row content checks. The five
    sample tables together are a small fraction of the dataset.
    """
    out: dict[str, MultidayPerFileMeasured] = {}
    for pf in paths_per_file:
        m = MultidayPerFileMeasured(date=pf.date)
        m.parquet_sha = compute_file_sha256(pf.parquet_path)
        m.parquet_size = compute_file_size(pf.parquet_path)
        m.sidecar_sha = compute_file_sha256(pf.parquet_sidecar_path)
        m.sidecar_size = compute_file_size(pf.parquet_sidecar_path)
        m.sidecar_first_64 = read_sidecar_first_64(pf.parquet_sidecar_path)
        m.source_zip_sha = compute_file_sha256(pf.source_zip_path)
        # Cheap metadata-only num_rows read.
        pq_file = pq.ParquetFile(str(pf.parquet_path))
        m.parquet_num_rows = pq_file.metadata.num_rows
        # Full-table load only for the predeclared sample dates.
        if pf.date in sample_dates:
            m.sample_table = pq.read_table(pf.parquet_path)
        out[pf.date] = m
    return out


def _build_loaded_bundle(
    *,
    derived_manifest_bytes: bytes,
    derived_manifest: dict[str, Any],
    derived_sidecar_first_64: str,
    raw_manifest_bytes: bytes,
    raw_manifest: dict[str, Any],
    raw_manifest_sidecar_first_64: str,
    acquisition_log_sha: str,
    acquisition_log_sidecar_first_64: str,
    gate_report_sha: str,
    gate_report_sidecar_first_64: str,
    successor_state_sha: str,
    successor_state_sidecar_first_64: str,
) -> MultidayLoadedArtefactBundle:
    """Construct the immutable governance-artefact bundle."""
    return MultidayLoadedArtefactBundle(
        derived_manifest_bytes=derived_manifest_bytes,
        derived_manifest_sha=compute_bytes_sha256(derived_manifest_bytes),
        derived_manifest=derived_manifest,
        derived_sidecar_first_64=derived_sidecar_first_64,
        raw_manifest_bytes=raw_manifest_bytes,
        raw_manifest_sha=compute_bytes_sha256(raw_manifest_bytes),
        raw_manifest=raw_manifest,
        raw_manifest_sidecar_first_64=raw_manifest_sidecar_first_64,
        acquisition_log_sha=acquisition_log_sha,
        acquisition_log_sidecar_first_64=acquisition_log_sidecar_first_64,
        gate_report_sha=gate_report_sha,
        gate_report_sidecar_first_64=gate_report_sidecar_first_64,
        successor_state_sha=successor_state_sha,
        successor_state_sidecar_first_64=successor_state_sidecar_first_64,
    )


def _build_boundary_confirmations(
    *,
    pre_governance: Mapping[str, str],
    post_governance: Mapping[str, str],
    per_file_pre: Mapping[str, str],
    per_file_post: Mapping[str, str],
    per_file_sidecar_pre: Mapping[str, str],
    per_file_sidecar_post: Mapping[str, str],
    raw_zip_pre: Mapping[str, str],
    raw_zip_post: Mapping[str, str],
) -> dict[str, bool]:
    """Re-hash every artefact post-checks and build the boundary block."""
    no_manifest_mutation = all(
        pre_governance[k] == post_governance[k] for k in pre_governance
    )
    no_per_file_parquet_mutation = all(
        per_file_pre[d] == per_file_post[d] for d in per_file_pre
    )
    no_per_file_sidecar_mutation = all(
        per_file_sidecar_pre[d] == per_file_sidecar_post[d]
        for d in per_file_sidecar_pre
    )
    no_raw_zip_mutation = all(
        raw_zip_pre[d] == raw_zip_post[d] for d in raw_zip_pre
    )
    confirmations: dict[str, bool] = {k: True for k in _BOUNDARY_KEYS}
    confirmations["no_manifest_mutation"] = no_manifest_mutation
    confirmations["no_per_file_parquet_mutation"] = no_per_file_parquet_mutation
    confirmations["no_per_file_sidecar_mutation"] = no_per_file_sidecar_mutation
    confirmations["no_raw_zip_mutation"] = no_raw_zip_mutation
    # The two safety invariants are unconditional; the writer also enforces them.
    confirmations["research_eligible_after_is_false_for_derived_family"] = True
    confirmations["no_successor_authorization"] = True
    return confirmations


def _build_measured_summary(
    *,
    derived_manifest_path: Path,
    pre_governance: Mapping[str, str],
    post_governance: Mapping[str, str],
    total_recomputed_event_count: int,
    declared_total_event_count: int,
    total_recomputed_parquet_bytes: int,
    per_file_pre_count: int,
    sample_dates: tuple[str, ...],
) -> dict[str, Any]:
    """Construct the structured ``measured_summary`` for the report."""
    return {
        "derived_manifest_path": str(derived_manifest_path),
        "derived_manifest_sha_pre": pre_governance["derived_manifest"],
        "derived_manifest_sha_post": post_governance["derived_manifest"],
        "raw_manifest_sha_pre": pre_governance["raw_manifest"],
        "raw_manifest_sha_post": post_governance["raw_manifest"],
        "acquisition_log_sha_pre": pre_governance["acquisition_log"],
        "acquisition_log_sha_post": post_governance["acquisition_log"],
        "gate_report_sha_pre": pre_governance["gate_report"],
        "gate_report_sha_post": post_governance["gate_report"],
        "successor_state_sha_pre": pre_governance["successor_state"],
        "successor_state_sha_post": post_governance["successor_state"],
        "per_file_count": per_file_pre_count,
        "sample_dates": list(sample_dates),
        "total_recomputed_event_count": total_recomputed_event_count,
        "declared_total_event_count": declared_total_event_count,
        "total_recomputed_parquet_bytes": total_recomputed_parquet_bytes,
    }


def _build_input_artefacts(
    *,
    paths: MultidayDerivedSourceArtefactPaths,
    derived_manifest_sha: str,
    raw_manifest_sha: str,
    acquisition_log_sha: str,
    gate_report_sha: str,
    successor_state_sha: str,
    derived_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    """Construct the structured ``input_artefacts`` block for the report."""
    gov = derived_manifest.get("governance_labels") or {}
    return {
        "derived_manifest_path": str(paths.derived_manifest_path),
        "derived_manifest_sha256": derived_manifest_sha,
        "raw_manifest_path": str(paths.raw_manifest_path),
        "raw_manifest_sha256": raw_manifest_sha,
        "acquisition_log_path": str(paths.acquisition_log_path),
        "acquisition_log_sha256": acquisition_log_sha,
        "raw_gate_report_path": str(paths.gate_report_path),
        "raw_gate_report_id": gov.get("source_gate_report_id") or "",
        "raw_gate_report_sha256": gate_report_sha,
        "successor_state_path": str(paths.successor_state_path),
        "successor_state_sha256": successor_state_sha,
        "phase_4bmc_qa_memo_path": str(PHASE_4BMC_QA_PATH),
        "phase_4bmc_closeout_path": str(PHASE_4BMC_CLOSEOUT_PATH),
        "phase_4bmc_merge_closeout_path": str(PHASE_4BMC_MERGE_CLOSEOUT_PATH),
        "per_file_count": len(paths.per_file),
        "sample_dates": list(SAMPLE_DATES),
    }


def run_multiday_derived_aggtrades_gate(
    inp: MultidayDerivedAggTradesGateInput,
) -> MultidayDerivedAggTradesGateResult:
    """Run the Phase 4bm-D 60-check multi-day derived-family gate exactly once.

    The orchestrator is read-only on data files. It only writes the
    gate report JSON + paired SHA256 sidecar under
    ``data/microstructure/gate-reports/normalized/`` (and only when
    ``inp.write_report=True``).
    """
    # ---- Governance artefact eager load + SHAs -------------------------
    derived_manifest_bytes = read_manifest_bytes(inp.derived_manifest_path)
    derived_manifest = parse_manifest_bytes(derived_manifest_bytes)

    paths = resolve_multiday_derived_source_artefact_paths(
        derived_manifest_path=inp.derived_manifest_path,
        derived_manifest=derived_manifest,
    )

    derived_sidecar_first_64 = (
        read_sidecar_first_64(paths.derived_manifest_sidecar_path)
        if paths.derived_manifest_sidecar_path.exists()
        else ""
    )

    raw_manifest_bytes = read_manifest_bytes(paths.raw_manifest_path)
    raw_manifest = parse_manifest_bytes(raw_manifest_bytes)
    raw_manifest_sidecar_first_64 = (
        read_sidecar_first_64(paths.raw_manifest_sidecar_path)
        if paths.raw_manifest_sidecar_path.exists()
        else ""
    )

    acquisition_log_sha_pre = compute_file_sha256(paths.acquisition_log_path)
    acquisition_log_sidecar_first_64 = (
        read_sidecar_first_64(paths.acquisition_log_sidecar_path)
        if paths.acquisition_log_sidecar_path.exists()
        else ""
    )

    gate_report_sha_pre = compute_file_sha256(paths.gate_report_path)
    gate_report_sidecar_first_64 = (
        read_sidecar_first_64(paths.gate_report_sidecar_path)
        if paths.gate_report_sidecar_path.exists()
        else ""
    )

    successor_state_sha_pre = compute_file_sha256(paths.successor_state_path)
    successor_state_sidecar_first_64 = (
        read_sidecar_first_64(paths.successor_state_sidecar_path)
        if paths.successor_state_sidecar_path.exists()
        else ""
    )

    bundle = _build_loaded_bundle(
        derived_manifest_bytes=derived_manifest_bytes,
        derived_manifest=derived_manifest,
        derived_sidecar_first_64=derived_sidecar_first_64,
        raw_manifest_bytes=raw_manifest_bytes,
        raw_manifest=raw_manifest,
        raw_manifest_sidecar_first_64=raw_manifest_sidecar_first_64,
        acquisition_log_sha=acquisition_log_sha_pre,
        acquisition_log_sidecar_first_64=acquisition_log_sidecar_first_64,
        gate_report_sha=gate_report_sha_pre,
        gate_report_sidecar_first_64=gate_report_sidecar_first_64,
        successor_state_sha=successor_state_sha_pre,
        successor_state_sidecar_first_64=successor_state_sidecar_first_64,
    )

    derived_manifest_sha_pre = bundle.derived_manifest_sha
    raw_manifest_sha_pre = bundle.raw_manifest_sha

    # ---- Per-file measurement walk (all 90 dates) ---------------------
    sample_set = frozenset(SAMPLE_DATES)
    perfile = _measure_per_file(paths.per_file, sample_dates=sample_set)

    # Capture pre-check per-file Parquet / sidecar / raw-zip SHAs for the
    # post-check immutability cross-verification.
    per_file_pre: dict[str, str] = {
        d: m.parquet_sha for d, m in perfile.items() if m.parquet_sha is not None
    }
    per_file_sidecar_pre: dict[str, str] = {
        d: m.sidecar_sha for d, m in perfile.items() if m.sidecar_sha is not None
    }
    raw_zip_pre: dict[str, str] = {
        d: m.source_zip_sha for d, m in perfile.items() if m.source_zip_sha is not None
    }

    # ---- Run all 60 checks --------------------------------------------
    ctx = MultidayDerivedGateContext(
        paths=paths,
        bundle=bundle,
        perfile=perfile,
    )
    checks = run_all_checks(ctx)
    if len(checks) != len(CHECK_ORDER):  # pragma: no cover - defensive
        raise MultidayDerivedAggTradesGateUnsupportedError(
            f"check count drift: got {len(checks)} expected {len(CHECK_ORDER)}"
        )

    overall_status = _classify_overall_status(checks)
    gate_verdict = _classify_gate_verdict(overall_status)

    # ---- Post-check governance + per-file immutability re-hash --------
    derived_manifest_sha_post = compute_file_sha256(paths.derived_manifest_path)
    raw_manifest_sha_post = compute_file_sha256(paths.raw_manifest_path)
    acquisition_log_sha_post = compute_file_sha256(paths.acquisition_log_path)
    gate_report_sha_post = compute_file_sha256(paths.gate_report_path)
    successor_state_sha_post = compute_file_sha256(paths.successor_state_path)

    pre_governance: dict[str, str] = {
        "derived_manifest": derived_manifest_sha_pre,
        "raw_manifest": raw_manifest_sha_pre,
        "acquisition_log": acquisition_log_sha_pre,
        "gate_report": gate_report_sha_pre,
        "successor_state": successor_state_sha_pre,
    }
    post_governance: dict[str, str] = {
        "derived_manifest": derived_manifest_sha_post,
        "raw_manifest": raw_manifest_sha_post,
        "acquisition_log": acquisition_log_sha_post,
        "gate_report": gate_report_sha_post,
        "successor_state": successor_state_sha_post,
    }

    per_file_post: dict[str, str] = {}
    per_file_sidecar_post: dict[str, str] = {}
    raw_zip_post: dict[str, str] = {}
    for pf in paths.per_file:
        per_file_post[pf.date] = compute_file_sha256(pf.parquet_path)
        per_file_sidecar_post[pf.date] = compute_file_sha256(
            pf.parquet_sidecar_path
        )
        raw_zip_post[pf.date] = compute_file_sha256(pf.source_zip_path)

    boundary_confirmations = _build_boundary_confirmations(
        pre_governance=pre_governance,
        post_governance=post_governance,
        per_file_pre=per_file_pre,
        per_file_post=per_file_post,
        per_file_sidecar_pre=per_file_sidecar_pre,
        per_file_sidecar_post=per_file_sidecar_post,
        raw_zip_pre=raw_zip_pre,
        raw_zip_post=raw_zip_post,
    )

    # eligibility_gate_status_after is a report-level recommendation only;
    # it never mutates the on-disk derived manifest.
    if overall_status == "pass":
        eligibility_gate_status_after = "pass"
    elif overall_status == "incomplete":
        eligibility_gate_status_after = "incomplete"
    else:
        eligibility_gate_status_after = "fail"

    total_recomputed_event_count = sum(
        (m.parquet_num_rows or 0) for m in perfile.values()
    )
    total_recomputed_parquet_bytes = sum(
        (m.parquet_size or 0) for m in perfile.values()
    )
    declared_total_event_count = derived_manifest.get("total_event_count") or 0

    measured_summary = _build_measured_summary(
        derived_manifest_path=paths.derived_manifest_path,
        pre_governance=pre_governance,
        post_governance=post_governance,
        total_recomputed_event_count=total_recomputed_event_count,
        declared_total_event_count=int(declared_total_event_count),
        total_recomputed_parquet_bytes=total_recomputed_parquet_bytes,
        per_file_pre_count=len(per_file_pre),
        sample_dates=SAMPLE_DATES,
    )

    input_artefacts = _build_input_artefacts(
        paths=paths,
        derived_manifest_sha=derived_manifest_sha_pre,
        raw_manifest_sha=raw_manifest_sha_pre,
        acquisition_log_sha=acquisition_log_sha_pre,
        gate_report_sha=gate_report_sha_pre,
        successor_state_sha=successor_state_sha_pre,
        derived_manifest=derived_manifest,
    )

    generated_at_unix_ms = int(time.time() * 1000)
    short_commit = inp.code_commit_sha[:12]
    report_id = (
        f"{CANONICAL_DATASET_FAMILY}__{CANONICAL_DATASET_VERSION}__"
        f"phase-4bm-d__{generated_at_unix_ms}__{short_commit}"
    )

    report_path: Path | None = None
    if inp.write_report:
        report = build_report(
            report_id=report_id,
            dataset_family=CANONICAL_DATASET_FAMILY,
            dataset_version=CANONICAL_DATASET_VERSION,
            symbol=CANONICAL_SYMBOL,
            utc_date_start=CANONICAL_DATE_START,
            utc_date_end=CANONICAL_DATE_END,
            date_count=EXPECTED_DATE_COUNT,
            generated_at_unix_ms=generated_at_unix_ms,
            code_commit_sha=inp.code_commit_sha,
            input_artefacts=input_artefacts,
            checks=[c.to_dict() for c in checks],
            overall_status=overall_status,
            gate_verdict=gate_verdict,
            eligibility_gate_status_after=eligibility_gate_status_after,
            boundary_confirmations=boundary_confirmations,
            measured_summary=measured_summary,
        )
        paths_out, _report_sha, _report_size = write_gate_report(
            report, output_root=inp.output_root, refuse_overwrite=True
        )
        report_path = paths_out.report_path
        report_id = paths_out.report_id

    return MultidayDerivedAggTradesGateResult(
        overall_status=overall_status,
        gate_verdict=gate_verdict,
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
