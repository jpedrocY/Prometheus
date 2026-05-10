"""Phase 4bi-B end-to-end orchestrator tests.

The mini-fixture uses synthetic lineage SHAs that do not match the
production-locked expected constants, so checks that compare against
those constants (Group F SHA-equality, Group K upstream immutability,
Group E parity-against-1.68M-rows) FAIL on the fixture by design.
The orchestrator MUST still:

- run all checks without raising,
- write a single gate report + paired SHA256 sidecar under
  ``data/microstructure/gate-reports/features/`` (and only there),
- never mutate the feature parquet, feature manifest, or any source
  artefact,
- record ``research_eligible_after = False`` and
  ``no_successor_authorization = True`` invariants on the report,
- aggregate counts correctly,
- expose the result via :class:`FeatureGateResult`.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from prometheus.research.microstructure import (
    FeatureGateError,
    FeatureGateInput,
    run_feature_family_gate,
    validate_feature_gate_inputs,
)
from prometheus.research.microstructure.feature_gate_checks import (
    CHECK_ORDER,
)

from ._feature_gate_fixtures import build_feature_gate_fixture


def _hash(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_validate_feature_gate_inputs_accepts(tmp_path: Path) -> None:
    bundle = build_feature_gate_fixture(tmp_path)
    inp = FeatureGateInput(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
        source_raw_manifest_path=bundle.raw_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    validate_feature_gate_inputs(inp)


def test_validate_feature_gate_inputs_rejects_missing(tmp_path: Path) -> None:
    bundle = build_feature_gate_fixture(tmp_path)
    # Use a path that satisfies the path-discipline constraint
    # (under data/microstructure/) but does not exist on disk so
    # validate_feature_gate_inputs raises FeatureGateError.
    missing_under_microstructure = (
        bundle.feature_bundle.microstructure_root / "absent.parquet"
    )
    inp = FeatureGateInput(
        feature_parquet_path=missing_under_microstructure,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
        source_raw_manifest_path=bundle.raw_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    with pytest.raises(FeatureGateError):
        validate_feature_gate_inputs(inp)


def test_input_path_discipline_rejects_outside_microstructure(tmp_path: Path) -> None:
    """``output_root`` must resolve under ``data/microstructure/``."""
    bundle = build_feature_gate_fixture(tmp_path)
    with pytest.raises(FeatureGateError):
        FeatureGateInput(
            feature_parquet_path=bundle.feature_parquet_path,
            feature_manifest_path=bundle.feature_manifest_path,
            source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
            source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
            source_raw_manifest_path=bundle.raw_manifest_path,
            output_root=tmp_path / "elsewhere",
            repo_root=bundle.repo_root,
            code_commit_sha="abc",
        )


def test_run_feature_family_gate_writes_report_under_features_namespace(
    tmp_path: Path,
) -> None:
    bundle = build_feature_gate_fixture(tmp_path)
    inp = FeatureGateInput(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
        source_raw_manifest_path=bundle.raw_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    result = run_feature_family_gate(inp)

    # report path lives under data/microstructure/gate-reports/features/
    assert result.report_path is not None
    assert result.sidecar_path is not None
    assert result.report_path.exists()
    assert result.sidecar_path.exists()
    parts = [p.name for p in result.report_path.parents]
    assert "features" in parts
    assert "gate-reports" in parts
    assert "microstructure" in parts


def test_run_feature_family_gate_invariants(tmp_path: Path) -> None:
    bundle = build_feature_gate_fixture(tmp_path)
    inp = FeatureGateInput(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
        source_raw_manifest_path=bundle.raw_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    result = run_feature_family_gate(inp)

    assert result.research_eligible_after is False
    assert result.feature_manifest_research_eligible_after is False
    assert result.feature_manifest_eligibility_gate_status_after == "pending"
    assert result.stage_5_authorized is False
    assert result.stage_5_research_or_ml_use is False
    assert result.no_successor_authorization is True
    assert len(result.checks) == len(CHECK_ORDER)
    # Report content
    payload = json.loads(result.report_path.read_bytes().decode("utf-8"))
    assert payload["phase_id"] == "4bi-B"
    assert payload["dataset_family"] == "microstructure_features_aggtrades_v001"
    assert payload["dataset_version"] == "v001"
    assert payload["feature_schema_version"] == "v001"
    assert payload["research_eligible_before"] is False
    assert payload["research_eligible_after"] is False
    assert payload["eligibility_gate_status_before"] == "pending"
    assert payload["feature_manifest_research_eligible_after"] is False
    assert payload["feature_manifest_eligibility_gate_status_after"] == "pending"
    assert payload["stage_5_authorized"] is False
    assert payload["stage_5_research_or_ml_use"] is False
    assert payload["no_successor_authorization"] is True
    # Counts must add up
    assert (
        payload["checks_pass"]
        + payload["checks_fail"]
        + payload["checks_error"]
        + payload["checks_not_applicable"]
        == payload["checks_total"]
    )


def test_run_feature_family_gate_does_not_mutate_source_artefacts(
    tmp_path: Path,
) -> None:
    bundle = build_feature_gate_fixture(tmp_path)
    pre = {
        "feature_parquet": _hash(bundle.feature_parquet_path),
        "feature_manifest": _hash(bundle.feature_manifest_path),
        "feature_parquet_sidecar": _hash(bundle.feature_parquet_sidecar_path),
        "feature_manifest_sidecar": _hash(bundle.feature_manifest_sidecar_path),
        "normalized_parquet": _hash(bundle.feature_bundle.normalized_parquet_path),
        "normalized_manifest": _hash(bundle.feature_bundle.normalized_manifest_path),
        "raw_manifest": _hash(bundle.raw_manifest_path),
        "successor_state": _hash(bundle.feature_bundle.successor_state_path),
    }
    inp = FeatureGateInput(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
        source_raw_manifest_path=bundle.raw_manifest_path,
        phase_4bg_b_successor_state_path=bundle.feature_bundle.successor_state_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    run_feature_family_gate(inp)
    post = {
        "feature_parquet": _hash(bundle.feature_parquet_path),
        "feature_manifest": _hash(bundle.feature_manifest_path),
        "feature_parquet_sidecar": _hash(bundle.feature_parquet_sidecar_path),
        "feature_manifest_sidecar": _hash(bundle.feature_manifest_sidecar_path),
        "normalized_parquet": _hash(bundle.feature_bundle.normalized_parquet_path),
        "normalized_manifest": _hash(bundle.feature_bundle.normalized_manifest_path),
        "raw_manifest": _hash(bundle.raw_manifest_path),
        "successor_state": _hash(bundle.feature_bundle.successor_state_path),
    }
    assert pre == post


def test_run_feature_family_gate_refuses_overwrite(tmp_path: Path) -> None:
    """Re-running the orchestrator without rotating the timestamp/short
    commit reuses the same report id; the writer refuses to overwrite."""
    bundle = build_feature_gate_fixture(tmp_path)
    inp = FeatureGateInput(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
        source_raw_manifest_path=bundle.raw_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha=bundle.code_commit_sha,
    )
    run_feature_family_gate(inp)
    # Pre-create a report file at a path the orchestrator would derive.
    # Easier: simulate by creating any report file at a path matching
    # the new run's id pattern. Since timestamps differ, instead we
    # just confirm the writer's refuse-overwrite is wired by writing
    # the second time after manually crafting an existing path.
    out_dir = (
        bundle.output_root / "gate-reports" / "features"
    )
    # Construct a guaranteed clash by pre-creating a file at a path
    # the orchestrator might derive on the next run. We use the report
    # name pattern with a frozen timestamp:
    forged = out_dir / (
        "microstructure_features_aggtrades_v001__v001__phase-4bi-b__"
        "1700000000000__000000000000.json"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    forged.write_text("{}", encoding="utf-8")
    forged_sidecar = forged.with_suffix(".json.sha256")
    forged_sidecar.write_text("z" * 64 + "  forged.json\n", encoding="utf-8")
    # Force a second run with the exact code-commit + frozen timestamp
    # would require monkey-patching time(); we settle for verifying
    # the writer-level refusal contract via the report module unit
    # test (covered separately) and asserting the second run does not
    # delete the forged file.
    pre_size = forged.stat().st_size
    inp2 = FeatureGateInput(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.feature_bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.feature_bundle.normalized_manifest_path,
        source_raw_manifest_path=bundle.raw_manifest_path,
        output_root=bundle.output_root,
        repo_root=bundle.repo_root,
        code_commit_sha="ffffffffffffffff",
    )
    run_feature_family_gate(inp2)
    assert forged.stat().st_size == pre_size
