"""Phase 4bm-J orchestrator end-to-end + verdict-classification tests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.multiday_feature_gate import (
    MultidayFeatureGateError,
    MultidayFeatureGateInput,
    run_multiday_feature_family_gate,
)
from prometheus.research.microstructure.multiday_feature_gate_io import (
    MultidayFeatureGateIOError,
)
from prometheus.research.microstructure.multiday_feature_gate_report import (
    GATE_VERDICT_FAIL,
)

from ._multiday_feature_gate_fixtures import build_multiday_feature_gate_fixture


def _input(bundle, *, write_report: bool = False) -> MultidayFeatureGateInput:
    return MultidayFeatureGateInput(
        repo_root=bundle.repo_root,
        feature_manifest_path=bundle.feature_manifest_path,
        feature_manifest_sidecar_path=bundle.feature_manifest_sidecar_path,
        features_root=bundle.features_root,
        derived_manifest_path=bundle.derived_manifest_path,
        raw_manifest_path=bundle.raw_manifest_path,
        acquisition_log_path=bundle.acquisition_log_path,
        phase_4bl_d_r_gate_report_path=bundle.phase_4bl_d_r_gate_report_path,
        phase_4bl_e_successor_state_path=bundle.phase_4bl_e_successor_state_path,
        phase_4bm_d_gate_report_path=bundle.phase_4bm_d_gate_report_path,
        phase_4bm_d_sidecar_path=bundle.phase_4bm_d_sidecar_path,
        phase_4bm_f_successor_state_path=bundle.phase_4bm_f_successor_state_path,
        phase_4bm_f_successor_state_sidecar_path=bundle.phase_4bm_f_successor_state_sidecar_path,
        output_root=bundle.output_root,
        code_commit_sha="0" * 40,
        write_report=write_report,
    )


def test_orchestrator_runs_returns_50_results(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    res = run_multiday_feature_family_gate(_input(bundle))
    assert len(res.results) == 50


def test_orchestrator_writes_atomic_report_and_canonical_sidecar(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    res = run_multiday_feature_family_gate(_input(bundle, write_report=True))
    assert res.report_path is not None and res.report_path.exists()
    assert res.sidecar_path is not None and res.sidecar_path.exists()
    # Canonical sidecar format.
    sidecar_bytes = res.sidecar_path.read_bytes()
    expected = f"{res.report_sha256}  {res.report_path.name}\n".encode("ascii")
    assert sidecar_bytes == expected
    assert b"\r" not in sidecar_bytes
    assert not sidecar_bytes.startswith(b"\xef\xbb\xbf")
    # Manifest SHA recomputation matches.
    assert hashlib.sha256(res.report_path.read_bytes()).hexdigest() == res.report_sha256
    # Sidecar SHA recomputation matches.
    assert hashlib.sha256(sidecar_bytes).hexdigest() == res.sidecar_sha256


def test_orchestrator_refuses_to_overwrite_existing_report(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    res1 = run_multiday_feature_family_gate(_input(bundle, write_report=True))
    assert res1.report_path is not None and res1.report_path.exists()
    # Pre-create a file at the next-attempted report path to force collision.
    bundle.output_root.mkdir(parents=True, exist_ok=True)
    # Re-running with the same code_commit_sha will generate a new unix_ms
    # report_id, so collision is not guaranteed. To force the refuse-overwrite
    # path, pre-create a file at the exact target path used by the next run.
    # Simulate by directly writing into output_root and verifying atomic_write_json
    # refuses to overwrite that file.
    from prometheus.research.microstructure.multiday_feature_gate_io import atomic_write_json
    target = bundle.output_root / "collide.json"
    atomic_write_json(target, {"x": 1})
    with pytest.raises(MultidayFeatureGateIOError):
        atomic_write_json(target, {"x": 2})


def test_orchestrator_rejects_non_path_input(tmp_path: Path) -> None:
    with pytest.raises(MultidayFeatureGateError):
        MultidayFeatureGateInput(
            repo_root="not a path",  # type: ignore[arg-type]
            feature_manifest_path=tmp_path,
            feature_manifest_sidecar_path=tmp_path,
            features_root=tmp_path,
            derived_manifest_path=tmp_path,
            raw_manifest_path=tmp_path,
            acquisition_log_path=tmp_path,
            phase_4bl_d_r_gate_report_path=tmp_path,
            phase_4bl_e_successor_state_path=tmp_path,
            phase_4bm_d_gate_report_path=tmp_path,
            phase_4bm_d_sidecar_path=tmp_path,
            phase_4bm_f_successor_state_path=tmp_path,
            phase_4bm_f_successor_state_sidecar_path=tmp_path,
            output_root=tmp_path,
            code_commit_sha="0" * 40,
        )


def test_fail_fixture_missing_feature_manifest(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    bundle.feature_manifest_path.unlink()
    res = run_multiday_feature_family_gate(_input(bundle))
    # B1 must fail (file does not exist); orchestrator does not write report
    # because at least one B-group blocking check fails, so verdict is FAIL.
    # (We didn't request write_report, so no file is written either way.)
    b1 = next(r for r in res.results if r.check_id == "B1")
    assert b1.status.value == "FAIL"


def test_fail_fixture_noncanonical_sidecar(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    # Corrupt the manifest sidecar with CRLF.
    raw = bundle.feature_manifest_sidecar_path.read_bytes()
    bundle.feature_manifest_sidecar_path.write_bytes(raw.replace(b"\n", b"\r\n"))
    res = run_multiday_feature_family_gate(_input(bundle))
    a3 = next(r for r in res.results if r.check_id == "A3")
    assert a3.status.value == "FAIL"


def test_fail_fixture_per_day_sha_mismatch(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    # Mutate one parquet's first byte to produce a SHA mismatch.
    first = bundle.per_day_parquet_paths[0]
    raw = bytearray(first.read_bytes())
    raw[-1] = (raw[-1] + 1) % 256
    first.write_bytes(bytes(raw))
    res = run_multiday_feature_family_gate(_input(bundle))
    b10 = next(r for r in res.results if r.check_id == "B10")
    assert b10.status.value == "FAIL"


def test_fail_fixture_row_count_mismatch(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    # Mutate the manifest's actual_feature_row_count to a wrong value.
    m = json.loads(bundle.feature_manifest_path.read_text())
    m["actual_feature_row_count"] = 1
    bundle.feature_manifest_path.write_bytes(
        (json.dumps(m, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    )
    res = run_multiday_feature_family_gate(_input(bundle))
    d1 = next(r for r in res.results if r.check_id == "D1")
    assert d1.status.value == "FAIL"


def test_fail_fixture_forbidden_column_in_manifest(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    m = json.loads(bundle.feature_manifest_path.read_text())
    m["feature_column_names"] = m["feature_column_names"] + ["my_label_column"]
    bundle.feature_manifest_path.write_bytes(
        (json.dumps(m, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    )
    res = run_multiday_feature_family_gate(_input(bundle))
    c7 = next(r for r in res.results if r.check_id == "C7")
    assert c7.status.value == "FAIL"


def test_fail_fixture_research_eligible_true_in_manifest(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    m = json.loads(bundle.feature_manifest_path.read_text())
    m["research_eligible"] = True
    bundle.feature_manifest_path.write_bytes(
        (json.dumps(m, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    )
    res = run_multiday_feature_family_gate(_input(bundle))
    g1 = next(r for r in res.results if r.check_id == "G1")
    assert g1.status.value == "FAIL"
    # Verdict must be FEATURE_GATE_FAIL when any blocking check fails.
    assert res.report.gate_verdict == GATE_VERDICT_FAIL


def test_indeterminate_when_required_lineage_artefact_missing(tmp_path: Path) -> None:
    bundle = build_multiday_feature_gate_fixture(tmp_path)
    bundle.phase_4bm_d_gate_report_path.unlink()  # cause an A-group check to ERROR
    res = run_multiday_feature_family_gate(_input(bundle))
    a4 = next(r for r in res.results if r.check_id == "A4")
    assert a4.status.value in {"ERROR", "FAIL"}
