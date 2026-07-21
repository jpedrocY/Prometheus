"""Phase 4bn-BB — tests for the corrected CF-1 artefact writers.

Covers: output-root confinement; deterministic JSON; sidecar body format and verification; the
target-layer schema carrying exactly two feature columns (never the mean); the paired-prediction
schema; the provenance / governance / non-authorization block; inventory validation; and the
fail-closed rejection of the prohibited mean column in any runtime schema. No market data is
opened; all writes go to a tmp path.
"""

from __future__ import annotations

from pathlib import Path

import pyarrow as pa
import pytest

from prometheus.research.microstructure import cf1_corrected_artifacts_v002 as art
from prometheus.research.microstructure import cf1_corrected_contract_v002 as cc


def _repo_root(tmp_path: Path) -> Path:
    art.ensure_output_dirs(tmp_path)
    return tmp_path


def test_output_dirs_and_confinement(tmp_path: Path) -> None:
    root = art.ensure_output_dirs(tmp_path)
    assert root == tmp_path / cc.OUTPUT_ROOT_REL
    for sub in art.SUBDIRS:
        assert (root / sub).is_dir()
    # Writing outside the output root fails closed.
    outside = tmp_path / "elsewhere" / "x.json"
    with pytest.raises(art.Cf1CorrectedArtifactError):
        art.write_json_with_sidecar(outside, {"a": 1}, tmp_path)


def test_deterministic_json_bytes() -> None:
    payload = {"b": 2, "a": 1, "c": [3, 2, 1]}
    b1 = art.canonical_json_bytes(payload)
    b2 = art.canonical_json_bytes(dict(payload))
    assert b1 == b2
    assert b1.endswith(b"\n")
    # Sorted keys.
    assert b1.index(b'"a"') < b1.index(b'"b"') < b1.index(b'"c"')


def test_sidecar_body_and_roundtrip() -> None:
    sha = "a" * 64
    body = art.compose_sidecar_body(sha, "file.json")
    assert body == b"a" * 64 + b"  file.json\n"
    parsed_sha, name = art.parse_sidecar(body.decode())
    assert parsed_sha == sha
    assert name == "file.json"
    with pytest.raises(art.Cf1CorrectedArtifactError):
        art.compose_sidecar_body("short", "file.json")


def test_json_sidecar_written_and_validated(tmp_path: Path) -> None:
    repo = _repo_root(tmp_path)
    path = art.output_root(repo) / "manifests" / "m.json"
    art.write_json_with_sidecar(path, {"k": "v"}, repo)
    assert path.is_file()
    assert path.with_suffix(".json.sha256").is_file()
    assert art.validate_json_sidecar(path) is True
    # Tamper the file -> validation fails.
    path.write_text('{"k": "TAMPERED"}\n', encoding="utf-8")
    assert art.validate_json_sidecar(path) is False


def test_filename_convention() -> None:
    name = art.compose_filename(
        family=art.FAMILY_TARGET_LAYER,
        context=art.FILENAME_CONTEXT,
        unix_ms=1700000000000,
        code_commit_sha="0123456789abcdef" * 2 + "01234567",
        ext="parquet",
    )
    assert name == (
        "cf1_corrected_realized_variance_target_layer_v002__v002__1700000000000__"
        "0123456789ab.parquet"
    )


def test_target_layer_two_feature_columns_no_mean(tmp_path: Path) -> None:
    rows = [
        {
            "origin_timestamp_ms": 1,
            "rolling_aggtrade_count_60s": 3.0,
            "rolling_quantity_sum_60s": 12.5,
            "rv_target": 0.1,
        }
    ]
    table = art.target_layer_table(rows)
    assert "rolling_aggtrade_count_60s" in table.column_names
    assert "rolling_quantity_sum_60s" in table.column_names
    assert cc.PROHIBITED_FEATURE_COLUMN not in table.column_names


def test_prohibited_mean_in_schema_fails_closed() -> None:
    bad = pa.table({"rolling_quantity_mean_60s": [1.0], "x": [2.0]})
    with pytest.raises(art.Cf1CorrectedArtifactError):
        art.assert_no_prohibited_feature_in_schema(bad.column_names)
    # And through the table builders.
    with pytest.raises(art.Cf1CorrectedArtifactError):
        art.target_layer_table([{"rolling_quantity_mean_60s": 1.0}])


def test_paired_prediction_schema() -> None:
    rows = [
        {
            "origin_timestamp_ms": 1,
            "evaluation_block": "B1",
            "yhat_baseline": 0.1,
            "yhat_augmented": 0.2,
            "qlike_baseline": 0.3,
            "qlike_augmented": 0.25,
            "loss_differential": 0.05,
        }
    ]
    table = art.paired_predictions_table(rows)
    assert set(rows[0]).issubset(set(table.column_names))
    assert cc.PROHIBITED_FEATURE_COLUMN not in table.column_names


def test_provenance_block_fields() -> None:
    prov = art.provenance_block(code_commit_sha="f" * 40, command="cmd")
    assert prov["phase_id"] == "phase-4bn-bb"
    assert prov["base_main_commit_sha"] == cc.BASE_MAIN_COMMIT_SHA
    assert prov["phase_4bn_ba_merge_commit_sha"] == cc.PHASE_4BN_BA_MERGE_COMMIT_SHA
    assert prov["phase_4bn_ba_contract_tip_sha"] == cc.PHASE_4BN_BA_CONTRACT_TIP_SHA
    assert prov["phase_4bn_ay_contract_tip_sha"] == cc.PHASE_4BN_AY_CONTRACT_TIP_SHA
    assert prov["phase_4bn_az_implementation_sha"] == cc.PHASE_4BN_AZ_IMPLEMENTATION_SHA
    assert prov["feature_list"] == ["rolling_aggtrade_count_60s", "rolling_quantity_sum_60s"]
    assert prov["feature_count"] == 2
    assert prov["allowed_utc_date_count"] == 244
    assert all(v is False for v in prov["non_authorization_flags"].values())
    assert prov["test_rows_loaded"] == 0
    assert prov["az_output_root_read"] is False
    assert "python_version" in prov and "numpy_version" in prov and "pyarrow_version" in prov


def test_inventory_build_and_validate(tmp_path: Path) -> None:
    repo = _repo_root(tmp_path)
    p = art.output_root(repo) / "proofs" / "x.json"
    sha, _ = art.write_json_with_sidecar(p, {"k": 1}, repo)
    entry = art.ArtifactEntry("fam", "proofs/x.json", sha, "proofs/x.json.sha256")
    inv = art.build_inventory(code_commit_sha="a" * 40, command="cmd", entries=[entry])
    assert inv["artifact_family"] == art.FAMILY_ARTIFACT_INVENTORY
    assert inv["artifact_count"] == 1
    assert inv["entries"][0]["relative_path"] == "proofs/x.json"


def test_family_names_are_corrected_v002() -> None:
    assert art.FAMILY_SYMBOLIC_PROOF == "cf1_corrected_symbolic_estimability_proof_v002"
    assert art.FAMILY_TIMESTAMP_PROOF == "cf1_corrected_timestamp_boundary_proof_v002"
    assert art.FAMILY_ACCESS_START == "cf1_corrected_execution_access_start_v002"
    assert art.FAMILY_LEAKAGE_PROOF == "cf1_corrected_leakage_split_coverage_proof_v002"
    assert art.FAMILY_TARGET_LAYER == "cf1_corrected_realized_variance_target_layer_v002"
    assert art.FAMILY_PAIRED_PREDICTIONS == "cf1_corrected_paired_model_predictions_v002"
    assert art.FAMILY_MODEL_RUN_MANIFEST == "cf1_corrected_model_run_manifest_v002"
    assert art.FAMILY_ARTIFACT_INVENTORY == "cf1_corrected_execution_artifact_inventory_v002"
