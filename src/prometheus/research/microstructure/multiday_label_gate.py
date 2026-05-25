"""Phase 4bm-Q multi-day v002 label-family eligibility gate orchestrator.

Reads the Phase 4bm-O v002 label artefacts read-only, runs the Phase
4bm-Q check suite, and (when ``write_report=True``) atomically emits
a JSON gate report plus paired Phase 4bb-F sidecar under
``data/microstructure/gate-reports/labels/``. Never mutates any source
artefact. Never flips ``research_eligible``. Never authorizes any
successor phase.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from .multiday_label_gate_checks import (
    MultidayLabelGateCheckResult,
    MultidayLabelGateContext,
    run_all_checks,
)
from .multiday_label_gate_io import (
    MultidayLabelGateIOError,
    assert_path_under_microstructure,
    derive_gate_report_id,
    derive_gate_report_paths,
)
from .multiday_label_gate_report import (
    MultidayLabelGateReport,
    build_report,
    write_gate_report,
)


class MultidayLabelGateError(RuntimeError):
    """Raised on orchestrator input or run errors."""


@dataclass(frozen=True)
class MultidayLabelGateInput:
    """Frozen input dataclass for the Phase 4bm-Q orchestrator."""

    repo_root: Path
    label_manifest_path: Path
    label_manifest_sidecar_path: Path
    labels_root: Path
    feature_manifest_path: Path
    feature_manifest_sidecar_path: Path
    phase_4bm_j_gate_report_path: Path
    phase_4bm_j_gate_sidecar_path: Path
    phase_4bm_l_successor_state_path: Path
    phase_4bm_l_successor_state_sidecar_path: Path
    derived_manifest_path: Path
    derived_manifest_sidecar_path: Path
    raw_manifest_path: Path
    acquisition_log_path: Path
    phase_4bm_d_gate_report_path: Path
    phase_4bm_d_sidecar_path: Path
    phase_4bm_f_successor_state_path: Path
    phase_4bm_f_successor_state_sidecar_path: Path
    phase_4bl_d_r_gate_report_path: Path
    phase_4bl_e_successor_state_path: Path
    output_root: Path
    code_commit_sha: str
    structural_qa_phase: str = "4bm-P"
    structural_qa_verdict: str = "LABEL_STRUCTURAL_QA_PASS"
    write_report: bool = True

    def __post_init__(self) -> None:
        for attr in (
            "repo_root",
            "label_manifest_path",
            "label_manifest_sidecar_path",
            "labels_root",
            "feature_manifest_path",
            "feature_manifest_sidecar_path",
            "phase_4bm_j_gate_report_path",
            "phase_4bm_j_gate_sidecar_path",
            "phase_4bm_l_successor_state_path",
            "phase_4bm_l_successor_state_sidecar_path",
            "derived_manifest_path",
            "derived_manifest_sidecar_path",
            "raw_manifest_path",
            "acquisition_log_path",
            "phase_4bm_d_gate_report_path",
            "phase_4bm_d_sidecar_path",
            "phase_4bm_f_successor_state_path",
            "phase_4bm_f_successor_state_sidecar_path",
            "phase_4bl_d_r_gate_report_path",
            "phase_4bl_e_successor_state_path",
            "output_root",
        ):
            v = getattr(self, attr)
            if not isinstance(v, Path):
                raise MultidayLabelGateError(
                    f"{attr} must be Path; got {type(v).__name__}"
                )
        try:
            assert_path_under_microstructure(self.output_root, label="output_root")
            assert_path_under_microstructure(
                self.label_manifest_path, label="label_manifest_path"
            )
        except MultidayLabelGateIOError as exc:
            raise MultidayLabelGateError(str(exc)) from exc
        if not isinstance(self.code_commit_sha, str) or not self.code_commit_sha:
            raise MultidayLabelGateError("code_commit_sha must be a non-empty str")


@dataclass(frozen=True)
class MultidayLabelGateResult:
    """Result of one Phase 4bm-Q gate run."""

    context: MultidayLabelGateContext
    results: tuple[MultidayLabelGateCheckResult, ...]
    report: MultidayLabelGateReport
    report_path: Path | None
    report_sha256: str | None
    report_size_bytes: int | None
    sidecar_path: Path | None
    sidecar_sha256: str | None
    sidecar_size_bytes: int | None


def run_multiday_label_family_gate(inp: MultidayLabelGateInput) -> MultidayLabelGateResult:
    """Run the Phase 4bm-Q gate end-to-end."""
    if not isinstance(inp, MultidayLabelGateInput):
        raise MultidayLabelGateError("inp must be MultidayLabelGateInput")

    ctx = MultidayLabelGateContext(
        repo_root=inp.repo_root,
        label_manifest_path=inp.label_manifest_path,
        label_manifest_sidecar_path=inp.label_manifest_sidecar_path,
        labels_root=inp.labels_root,
        feature_manifest_path=inp.feature_manifest_path,
        feature_manifest_sidecar_path=inp.feature_manifest_sidecar_path,
        phase_4bm_j_gate_report_path=inp.phase_4bm_j_gate_report_path,
        phase_4bm_j_gate_sidecar_path=inp.phase_4bm_j_gate_sidecar_path,
        phase_4bm_l_successor_state_path=inp.phase_4bm_l_successor_state_path,
        phase_4bm_l_successor_state_sidecar_path=inp.phase_4bm_l_successor_state_sidecar_path,
        derived_manifest_path=inp.derived_manifest_path,
        derived_manifest_sidecar_path=inp.derived_manifest_sidecar_path,
        raw_manifest_path=inp.raw_manifest_path,
        acquisition_log_path=inp.acquisition_log_path,
        phase_4bm_d_gate_report_path=inp.phase_4bm_d_gate_report_path,
        phase_4bm_d_sidecar_path=inp.phase_4bm_d_sidecar_path,
        phase_4bm_f_successor_state_path=inp.phase_4bm_f_successor_state_path,
        phase_4bm_f_successor_state_sidecar_path=inp.phase_4bm_f_successor_state_sidecar_path,
        phase_4bl_d_r_gate_report_path=inp.phase_4bl_d_r_gate_report_path,
        phase_4bl_e_successor_state_path=inp.phase_4bl_e_successor_state_path,
        structural_qa_phase=inp.structural_qa_phase,
        structural_qa_verdict=inp.structural_qa_verdict,
    )

    results, manifest = run_all_checks(ctx)
    parquet_count = len(sorted((ctx.labels_root / "BTCUSDT").glob("*/*/*.parquet")))
    sidecar_count = len(sorted((ctx.labels_root / "BTCUSDT").glob("*/*/*.parquet.sha256")))
    now_ms = int(time.time() * 1000)
    report = build_report(
        results=results,
        manifest=manifest,
        label_manifest_path=inp.label_manifest_path,
        created_at_utc_ms=now_ms,
        code_commit_sha=inp.code_commit_sha,
        label_parquet_count=parquet_count,
        label_sidecar_count=sidecar_count,
        structural_qa_phase=inp.structural_qa_phase,
        structural_qa_verdict=inp.structural_qa_verdict,
    )

    if not inp.write_report:
        return MultidayLabelGateResult(
            context=ctx,
            results=results,
            report=report,
            report_path=None,
            report_sha256=None,
            report_size_bytes=None,
            sidecar_path=None,
            sidecar_sha256=None,
            sidecar_size_bytes=None,
        )

    short_commit = inp.code_commit_sha[:12]
    report_id = derive_gate_report_id(
        dataset_family="microstructure_labels_aggtrades_v001",
        dataset_version="v002",
        phase_id="4bm-q",
        unix_ms=now_ms,
        short_commit=short_commit,
    )
    json_path, sidecar_path = derive_gate_report_paths(
        output_root=inp.output_root, report_id=report_id
    )
    rep_sha, rep_size, side_sha, side_size = write_gate_report(
        report=report,
        report_path=json_path,
        sidecar_path=sidecar_path,
    )
    return MultidayLabelGateResult(
        context=ctx,
        results=results,
        report=report,
        report_path=json_path,
        report_sha256=rep_sha,
        report_size_bytes=rep_size,
        sidecar_path=sidecar_path,
        sidecar_sha256=side_sha,
        sidecar_size_bytes=side_size,
    )


__all__ = [
    "MultidayLabelGateError",
    "MultidayLabelGateInput",
    "MultidayLabelGateResult",
    "run_multiday_label_family_gate",
]
