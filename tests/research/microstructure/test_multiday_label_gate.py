"""Phase 4bm-Q orchestrator end-to-end smoke test against real local
gitignored Phase 4bm-O label artefacts (executed read-only,
``write_report=False``).

Skipped when the real artefacts are not present (CI environment without
``data/microstructure/`` outputs).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.microstructure import (
    MULTIDAY_LABEL_GATE_VERDICT_PASS,
    MultidayLabelGateError,
    MultidayLabelGateInput,
    run_multiday_label_family_gate,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
MS = REPO_ROOT / "data" / "microstructure"
LABEL_MANIFEST = MS / "manifests" / "microstructure_labels_aggtrades_v001__v002.json"


def _resolve_unique(directory: Path, *, prefix: str, suffix: str) -> Path | None:
    if not directory.exists():
        return None
    candidates = sorted(
        p for p in directory.glob(f"{prefix}*{suffix}")
        if not p.name.endswith(".sha256.sha256")
    )
    return candidates[-1] if candidates else None


def _build_real_input(write_report: bool = False) -> MultidayLabelGateInput | None:
    if not LABEL_MANIFEST.exists():
        return None
    manifests = MS / "manifests"
    gate_raw = MS / "gate-reports" / "raw"
    gate_norm = MS / "gate-reports" / "normalized"
    gate_feat = MS / "gate-reports" / "features"
    succ = MS / "successor-state"
    bm_d = _resolve_unique(
        gate_norm,
        prefix="microstructure_normalized_aggtrades_v001__v002__phase-4bm-d",
        suffix=".json",
    )
    bm_f = _resolve_unique(
        succ,
        prefix=(
            "microstructure_normalized_aggtrades_v001__v002__"
            "stage3_research_eligible__phase-4bm-f"
        ),
        suffix=".json",
    )
    bl_d_r = _resolve_unique(
        gate_raw,
        prefix="microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r",
        suffix=".json",
    )
    bl_e = _resolve_unique(
        succ,
        prefix=(
            "microstructure_raw_aggtrades_v001__v002__"
            "stage2_raw_admissible__phase-4bl-e"
        ),
        suffix=".json",
    )
    bm_j = _resolve_unique(
        gate_feat,
        prefix="microstructure_features_aggtrades_v001__v002__phase-4bm-j",
        suffix=".json",
    )
    bm_l = _resolve_unique(
        succ,
        prefix=(
            "microstructure_features_aggtrades_v001__v002__"
            "stage5_research_use_approved__phase-4bm-l"
        ),
        suffix=".json",
    )
    if not all([bm_d, bm_f, bl_d_r, bl_e, bm_j, bm_l]):
        return None
    return MultidayLabelGateInput(
        repo_root=REPO_ROOT,
        label_manifest_path=LABEL_MANIFEST,
        label_manifest_sidecar_path=Path(str(LABEL_MANIFEST) + ".sha256"),
        labels_root=MS / "labels" / "microstructure_labels_aggtrades_v001__v002",
        feature_manifest_path=manifests
        / "microstructure_features_aggtrades_v001__v002.json",
        feature_manifest_sidecar_path=manifests
        / "microstructure_features_aggtrades_v001__v002.json.sha256",
        phase_4bm_j_gate_report_path=bm_j,  # type: ignore[arg-type]
        phase_4bm_j_gate_sidecar_path=Path(str(bm_j) + ".sha256"),
        phase_4bm_l_successor_state_path=bm_l,  # type: ignore[arg-type]
        phase_4bm_l_successor_state_sidecar_path=Path(str(bm_l) + ".sha256"),
        derived_manifest_path=manifests
        / "microstructure_normalized_aggtrades_v001__v002.json",
        derived_manifest_sidecar_path=manifests
        / "microstructure_normalized_aggtrades_v001__v002.json.sha256",
        raw_manifest_path=manifests
        / "microstructure_raw_aggtrades_v001__v002.json",
        acquisition_log_path=manifests
        / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json",
        phase_4bm_d_gate_report_path=bm_d,  # type: ignore[arg-type]
        phase_4bm_d_sidecar_path=Path(str(bm_d) + ".sha256"),
        phase_4bm_f_successor_state_path=bm_f,  # type: ignore[arg-type]
        phase_4bm_f_successor_state_sidecar_path=Path(str(bm_f) + ".sha256"),
        phase_4bl_d_r_gate_report_path=bl_d_r,  # type: ignore[arg-type]
        phase_4bl_e_successor_state_path=bl_e,  # type: ignore[arg-type]
        output_root=MS / "gate-reports" / "labels",
        code_commit_sha="unknown",
        write_report=write_report,
    )


REAL_INPUT = _build_real_input(write_report=False)


@pytest.mark.skipif(
    REAL_INPUT is None,
    reason="Phase 4bm-O local artefacts not present in this environment",
)
def test_orchestrator_passes_against_real_artefacts() -> None:
    assert REAL_INPUT is not None
    result = run_multiday_label_family_gate(REAL_INPUT)
    fails = [r for r in result.results if r.status.value in {"FAIL", "ERROR"}]
    assert fails == [], (
        f"unexpected non-PASS checks: "
        f"{[(r.check_id, r.status.value, r.observed) for r in fails]}"
    )
    assert result.report.gate_verdict == MULTIDAY_LABEL_GATE_VERDICT_PASS
    assert result.report.pass_count == 60
    # No write requested → no on-disk side effect.
    assert result.report_path is None
    assert result.sidecar_path is None


def test_orchestrator_rejects_non_path_inputs() -> None:
    with pytest.raises(MultidayLabelGateError):
        MultidayLabelGateInput(  # type: ignore[arg-type]
            repo_root="not_a_path",  # type: ignore[arg-type]
            label_manifest_path=Path("x"),
            label_manifest_sidecar_path=Path("x"),
            labels_root=Path("x"),
            feature_manifest_path=Path("x"),
            feature_manifest_sidecar_path=Path("x"),
            phase_4bm_j_gate_report_path=Path("x"),
            phase_4bm_j_gate_sidecar_path=Path("x"),
            phase_4bm_l_successor_state_path=Path("x"),
            phase_4bm_l_successor_state_sidecar_path=Path("x"),
            derived_manifest_path=Path("x"),
            derived_manifest_sidecar_path=Path("x"),
            raw_manifest_path=Path("x"),
            acquisition_log_path=Path("x"),
            phase_4bm_d_gate_report_path=Path("x"),
            phase_4bm_d_sidecar_path=Path("x"),
            phase_4bm_f_successor_state_path=Path("x"),
            phase_4bm_f_successor_state_sidecar_path=Path("x"),
            phase_4bl_d_r_gate_report_path=Path("x"),
            phase_4bl_e_successor_state_path=Path("x"),
            output_root=Path("x"),
            code_commit_sha="unknown",
        )


def test_orchestrator_rejects_output_root_outside_microstructure(tmp_path: Path) -> None:
    with pytest.raises(MultidayLabelGateError):
        MultidayLabelGateInput(
            repo_root=tmp_path,
            label_manifest_path=tmp_path / "data" / "microstructure" / "x.json",
            label_manifest_sidecar_path=tmp_path / "x.json.sha256",
            labels_root=tmp_path / "data" / "microstructure" / "labels",
            feature_manifest_path=tmp_path / "data" / "microstructure" / "f.json",
            feature_manifest_sidecar_path=tmp_path / "f.json.sha256",
            phase_4bm_j_gate_report_path=tmp_path / "j.json",
            phase_4bm_j_gate_sidecar_path=tmp_path / "j.json.sha256",
            phase_4bm_l_successor_state_path=tmp_path / "l.json",
            phase_4bm_l_successor_state_sidecar_path=tmp_path / "l.json.sha256",
            derived_manifest_path=tmp_path / "d.json",
            derived_manifest_sidecar_path=tmp_path / "d.json.sha256",
            raw_manifest_path=tmp_path / "r.json",
            acquisition_log_path=tmp_path / "a.json",
            phase_4bm_d_gate_report_path=tmp_path / "dg.json",
            phase_4bm_d_sidecar_path=tmp_path / "dg.json.sha256",
            phase_4bm_f_successor_state_path=tmp_path / "fs.json",
            phase_4bm_f_successor_state_sidecar_path=tmp_path / "fs.json.sha256",
            phase_4bl_d_r_gate_report_path=tmp_path / "br.json",
            phase_4bl_e_successor_state_path=tmp_path / "be.json",
            output_root=tmp_path / "elsewhere",  # NOT under data/microstructure
            code_commit_sha="unknown",
        )
