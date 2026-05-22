"""Phase 4bm-J multi-day v002 feature-family eligibility gate orchestrator.

Reads the Phase 4bm-H v002 feature artefacts read-only, runs the
Phase 4bm-J check suite, and (when ``write_report=True``) atomically
emits a JSON gate report plus paired Phase 4bb-F sidecar under
``data/microstructure/gate-reports/features/``. Never mutates any
source artefact. Never flips ``research_eligible``.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from .multiday_feature_gate_checks import (
    MultidayFeatureGateCheckResult,
    MultidayFeatureGateContext,
    run_all_checks,
)
from .multiday_feature_gate_io import (
    MultidayFeatureGateIOError,
    assert_path_under_microstructure,
    derive_gate_report_id,
    derive_gate_report_paths,
)
from .multiday_feature_gate_report import (
    MultidayFeatureGateReport,
    build_report,
    write_gate_report,
)


class MultidayFeatureGateError(RuntimeError):
    """Raised on orchestrator input or run errors."""


@dataclass(frozen=True)
class MultidayFeatureGateInput:
    """Frozen input dataclass for the Phase 4bm-J orchestrator."""

    repo_root: Path
    feature_manifest_path: Path
    feature_manifest_sidecar_path: Path
    features_root: Path
    derived_manifest_path: Path
    raw_manifest_path: Path
    acquisition_log_path: Path
    phase_4bl_d_r_gate_report_path: Path
    phase_4bl_e_successor_state_path: Path
    phase_4bm_d_gate_report_path: Path
    phase_4bm_d_sidecar_path: Path
    phase_4bm_f_successor_state_path: Path
    phase_4bm_f_successor_state_sidecar_path: Path
    output_root: Path
    code_commit_sha: str
    structural_qa_phase: str = "4bm-I"
    structural_qa_verdict: str = "FEATURE_STRUCTURAL_QA_PASS"
    write_report: bool = True

    def __post_init__(self) -> None:
        for attr in (
            "repo_root",
            "feature_manifest_path",
            "feature_manifest_sidecar_path",
            "features_root",
            "derived_manifest_path",
            "raw_manifest_path",
            "acquisition_log_path",
            "phase_4bl_d_r_gate_report_path",
            "phase_4bl_e_successor_state_path",
            "phase_4bm_d_gate_report_path",
            "phase_4bm_d_sidecar_path",
            "phase_4bm_f_successor_state_path",
            "phase_4bm_f_successor_state_sidecar_path",
            "output_root",
        ):
            v = getattr(self, attr)
            if not isinstance(v, Path):
                raise MultidayFeatureGateError(
                    f"{attr} must be Path; got {type(v).__name__}"
                )
        try:
            assert_path_under_microstructure(self.output_root, label="output_root")
            assert_path_under_microstructure(
                self.feature_manifest_path, label="feature_manifest_path"
            )
        except MultidayFeatureGateIOError as exc:
            raise MultidayFeatureGateError(str(exc)) from exc
        if not isinstance(self.code_commit_sha, str) or not self.code_commit_sha:
            raise MultidayFeatureGateError("code_commit_sha must be a non-empty str")


@dataclass(frozen=True)
class MultidayFeatureGateResult:
    """Result of one Phase 4bm-J gate run."""

    context: MultidayFeatureGateContext
    results: tuple[MultidayFeatureGateCheckResult, ...]
    report: MultidayFeatureGateReport
    report_path: Path | None
    report_sha256: str | None
    report_size_bytes: int | None
    sidecar_path: Path | None
    sidecar_sha256: str | None
    sidecar_size_bytes: int | None


def run_multiday_feature_family_gate(inp: MultidayFeatureGateInput) -> MultidayFeatureGateResult:
    """Run the Phase 4bm-J gate end-to-end."""
    if not isinstance(inp, MultidayFeatureGateInput):
        raise MultidayFeatureGateError("inp must be MultidayFeatureGateInput")

    ctx = MultidayFeatureGateContext(
        repo_root=inp.repo_root,
        feature_manifest_path=inp.feature_manifest_path,
        feature_manifest_sidecar_path=inp.feature_manifest_sidecar_path,
        features_root=inp.features_root,
        derived_manifest_path=inp.derived_manifest_path,
        raw_manifest_path=inp.raw_manifest_path,
        acquisition_log_path=inp.acquisition_log_path,
        phase_4bl_d_r_gate_report_path=inp.phase_4bl_d_r_gate_report_path,
        phase_4bl_e_successor_state_path=inp.phase_4bl_e_successor_state_path,
        phase_4bm_d_gate_report_path=inp.phase_4bm_d_gate_report_path,
        phase_4bm_d_sidecar_path=inp.phase_4bm_d_sidecar_path,
        phase_4bm_f_successor_state_path=inp.phase_4bm_f_successor_state_path,
        phase_4bm_f_successor_state_sidecar_path=inp.phase_4bm_f_successor_state_sidecar_path,
        structural_qa_phase=inp.structural_qa_phase,
        structural_qa_verdict=inp.structural_qa_verdict,
    )

    results, manifest = run_all_checks(ctx)
    parquet_count = len(sorted((ctx.features_root / "BTCUSDT").glob("*/*/*.parquet")))
    sidecar_count = len(sorted((ctx.features_root / "BTCUSDT").glob("*/*/*.parquet.sha256")))
    now_ms = int(time.time() * 1000)
    report = build_report(
        results=results,
        manifest=manifest,
        feature_manifest_path=inp.feature_manifest_path,
        created_at_utc_ms=now_ms,
        code_commit_sha=inp.code_commit_sha,
        feature_parquet_count=parquet_count,
        feature_sidecar_count=sidecar_count,
        structural_qa_phase=inp.structural_qa_phase,
        structural_qa_verdict=inp.structural_qa_verdict,
    )

    if not inp.write_report:
        return MultidayFeatureGateResult(
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
        dataset_family="microstructure_features_aggtrades_v001",
        dataset_version="v002",
        phase_id="4bm-j",
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
    return MultidayFeatureGateResult(
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
    "MultidayFeatureGateError",
    "MultidayFeatureGateInput",
    "MultidayFeatureGateResult",
    "run_multiday_feature_family_gate",
]
