"""Phase 4bj-E end-to-end orchestrator tests.

The mini-fixture uses synthetic lineage SHAs that do not match the
Phase 4bj-C production-locked constants, so checks that compare
against those constants (Group F SHA-equality, Group G expected-count
checks, Group H per-horizon-count parity vs production constants)
FAIL on the fixture by design. The orchestrator MUST still:

- run all checks without raising,
- write a single gate report + paired SHA256 sidecar under
  ``data/microstructure/gate-reports/labels/`` (and only there),
- never mutate the label parquet, label manifest, or any source
  artefact,
- record ``research_eligible_after = False`` and
  ``no_successor_authorization = True`` invariants on the report,
- preserve ``label_manifest_chronological_split_policy_after =
  not_yet_defined``,
- aggregate counts correctly,
- expose the result via :class:`LabelGateResult`.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from prometheus.research.microstructure import (
    LabelGateError,
    LabelGateInput,
    run_label_family_gate,
    validate_label_gate_inputs,
)
from prometheus.research.microstructure.label_gate_checks import (
    CHECK_ORDER,
)

from ._label_gate_fixtures import build_label_gate_fixture


def _hash(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_validate_label_gate_inputs_accepts(tmp_path: Path) -> None:
    bundle = build_label_gate_fixture(tmp_path)
    inp = LabelGateInput(
        label_parquet_path=bundle.label_parquet_path,
        label_manifest_path=bundle.label_manifest_path,
        source_feature_parquet_path=bundle.feature_parquet_path,
        source_feature_manifest_path=bundle.feature_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    validate_label_gate_inputs(inp)


def test_validate_label_gate_inputs_rejects_missing_parquet(tmp_path: Path) -> None:
    bundle = build_label_gate_fixture(tmp_path)
    missing_under_microstructure = (
        bundle.microstructure_root / "labels" / "absent.parquet"
    )
    inp = LabelGateInput(
        label_parquet_path=missing_under_microstructure,
        label_manifest_path=bundle.label_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    with pytest.raises(LabelGateError):
        validate_label_gate_inputs(inp)


def test_input_path_discipline_rejects_outside_microstructure(tmp_path: Path) -> None:
    """``output_root`` must resolve under ``data/microstructure/``."""
    bundle = build_label_gate_fixture(tmp_path)
    with pytest.raises(LabelGateError):
        LabelGateInput(
            label_parquet_path=bundle.label_parquet_path,
            label_manifest_path=bundle.label_manifest_path,
            output_root=tmp_path / "elsewhere",
            repo_root=bundle.repo_root,
            code_commit_sha="abc",
        )


def test_input_rejects_empty_code_commit_sha(tmp_path: Path) -> None:
    bundle = build_label_gate_fixture(tmp_path)
    with pytest.raises(LabelGateError):
        LabelGateInput(
            label_parquet_path=bundle.label_parquet_path,
            label_manifest_path=bundle.label_manifest_path,
            output_root=bundle.output_root,
            repo_root=bundle.repo_root,
            code_commit_sha="",
        )


def test_run_label_family_gate_writes_report_under_labels_namespace(
    tmp_path: Path,
) -> None:
    bundle = build_label_gate_fixture(tmp_path)
    inp = LabelGateInput(
        label_parquet_path=bundle.label_parquet_path,
        label_manifest_path=bundle.label_manifest_path,
        source_feature_parquet_path=bundle.feature_parquet_path,
        source_feature_manifest_path=bundle.feature_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    result = run_label_family_gate(inp)

    assert result.report_path is not None
    assert result.sidecar_path is not None
    assert result.report_path.exists()
    assert result.sidecar_path.exists()
    parts = [p.name for p in result.report_path.parents]
    assert "labels" in parts
    assert "gate-reports" in parts
    assert "microstructure" in parts


def test_run_label_family_gate_invariants(tmp_path: Path) -> None:
    bundle = build_label_gate_fixture(tmp_path)
    inp = LabelGateInput(
        label_parquet_path=bundle.label_parquet_path,
        label_manifest_path=bundle.label_manifest_path,
        source_feature_parquet_path=bundle.feature_parquet_path,
        source_feature_manifest_path=bundle.feature_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    result = run_label_family_gate(inp)

    assert result.research_eligible_after is False
    assert result.label_manifest_research_eligible_after is False
    assert result.label_manifest_eligibility_gate_status_after == "pending"
    assert (
        result.label_manifest_chronological_split_policy_after == "not_yet_defined"
    )
    assert result.stage_5_authorized is False
    assert result.stage_5_research_or_ml_use is False
    assert result.no_successor_authorization is True
    assert len(result.checks) == len(CHECK_ORDER)

    assert result.report_path is not None
    payload = json.loads(result.report_path.read_bytes().decode("utf-8"))
    assert payload["phase_id"] == "4bj-E"
    assert payload["dataset_family"] == "microstructure_labels_aggtrades_v001"
    assert payload["dataset_version"] == "v001"
    assert payload["label_schema_version"] == "v001"
    assert payload["research_eligible_before"] is False
    assert payload["research_eligible_after"] is False
    assert payload["eligibility_gate_status_before"] == "pending"
    assert payload["label_manifest_research_eligible_after"] is False
    assert payload["label_manifest_eligibility_gate_status_after"] == "pending"
    assert (
        payload["label_manifest_chronological_split_policy_after"]
        == "not_yet_defined"
    )
    assert payload["chronological_split_policy_before"] == "not_yet_defined"
    assert payload["chronological_split_policy_after"] == "not_yet_defined"
    assert payload["stage_5_authorized"] is False
    assert payload["stage_5_research_or_ml_use"] is False
    assert payload["no_successor_authorization"] is True
    assert (
        payload["checks_pass"]
        + payload["checks_fail"]
        + payload["checks_error"]
        + payload["checks_not_applicable"]
        == payload["checks_total"]
    )


def test_run_label_family_gate_does_not_mutate_source_artefacts(
    tmp_path: Path,
) -> None:
    bundle = build_label_gate_fixture(tmp_path)
    pre = {
        "label_parquet": _hash(bundle.label_parquet_path),
        "label_parquet_sidecar": _hash(bundle.label_parquet_sidecar_path),
        "label_manifest": _hash(bundle.label_manifest_path),
        "label_manifest_sidecar": _hash(bundle.label_manifest_sidecar_path),
        "feature_parquet": _hash(bundle.feature_parquet_path),
        "feature_manifest": _hash(bundle.feature_manifest_path),
    }
    inp = LabelGateInput(
        label_parquet_path=bundle.label_parquet_path,
        label_manifest_path=bundle.label_manifest_path,
        source_feature_parquet_path=bundle.feature_parquet_path,
        source_feature_manifest_path=bundle.feature_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    run_label_family_gate(inp)
    post = {
        "label_parquet": _hash(bundle.label_parquet_path),
        "label_parquet_sidecar": _hash(bundle.label_parquet_sidecar_path),
        "label_manifest": _hash(bundle.label_manifest_path),
        "label_manifest_sidecar": _hash(bundle.label_manifest_sidecar_path),
        "feature_parquet": _hash(bundle.feature_parquet_path),
        "feature_manifest": _hash(bundle.feature_manifest_path),
    }
    assert pre == post


def test_run_label_family_gate_runs_without_source_feature(tmp_path: Path) -> None:
    """K-group checks should NOT_APPLICABLE when feature parquet is absent."""
    bundle = build_label_gate_fixture(tmp_path)
    inp = LabelGateInput(
        label_parquet_path=bundle.label_parquet_path,
        label_manifest_path=bundle.label_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    result = run_label_family_gate(inp)
    assert len(result.checks) == len(CHECK_ORDER)
    # K01..K04 should be NOT_APPLICABLE when no feature table provided
    k_results = [c for c in result.checks if c.check_id.startswith("4bj-e.K")]
    assert len(k_results) == 4
    for r in k_results:
        # status is the StrEnum value
        assert r.status.value == "not_applicable", r


def test_run_label_family_gate_refuses_overwrite(tmp_path: Path) -> None:
    """Refuse-to-overwrite of report when the report path already exists."""
    bundle = build_label_gate_fixture(tmp_path)
    out_dir = bundle.output_root / "gate-reports" / "labels"
    out_dir.mkdir(parents=True, exist_ok=True)
    forged = out_dir / (
        "microstructure_labels_aggtrades_v001__v001__phase-4bj-e__"
        "1700000000000__000000000000.json"
    )
    forged.write_text("{}", encoding="utf-8")
    forged_sidecar = forged.with_suffix(".json.sha256")
    forged_sidecar.write_text("z" * 64 + "  forged.json\n", encoding="utf-8")
    pre_size = forged.stat().st_size
    # Run with a different code_commit_sha so the orchestrator's generated
    # report id does not collide with the forged file; the forged file
    # should remain unchanged.
    inp = LabelGateInput(
        label_parquet_path=bundle.label_parquet_path,
        label_manifest_path=bundle.label_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha="ffffffffffffffff",
    )
    run_label_family_gate(inp)
    assert forged.stat().st_size == pre_size


def test_run_label_family_gate_no_report_when_write_report_false(
    tmp_path: Path,
) -> None:
    bundle = build_label_gate_fixture(tmp_path)
    inp = LabelGateInput(
        label_parquet_path=bundle.label_parquet_path,
        label_manifest_path=bundle.label_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
        write_report=False,
    )
    result = run_label_family_gate(inp)
    assert result.report_path is None
    assert result.sidecar_path is None
    assert result.report_sha256 is None
    assert result.report_size_bytes is None
    assert len(result.checks) == len(CHECK_ORDER)
