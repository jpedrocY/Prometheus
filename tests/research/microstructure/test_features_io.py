"""Phase 4bh tests: features_io path discipline + atomic writers."""

from __future__ import annotations

import json

import pytest

from prometheus.research.microstructure import (
    FEATURE_DATASET_FAMILY,
    FeatureIOError,
    assert_output_path_under_features,
    atomic_write_feature_manifest,
    derive_feature_manifest_output_path,
    derive_feature_output_path,
    hash_source_file,
    read_normalized_parquet,
    read_source_normalized_manifest,
    read_successor_state,
    resolve_default_manifests_root,
    write_feature_sha256_sidecar,
)

from ._features_fixtures import build_feature_fixture


def test_assert_output_path_under_features_accepts_features_path(tmp_path) -> None:
    p = (
        tmp_path
        / "data"
        / "microstructure"
        / "features"
        / FEATURE_DATASET_FAMILY
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-features-aggtrades-2025-01-15.parquet"
    )
    p.parent.mkdir(parents=True, exist_ok=True)
    assert_output_path_under_features(p, label="ok")


def test_assert_output_path_under_features_rejects_outside(tmp_path) -> None:
    bad = tmp_path / "data" / "microstructure" / "normalized" / "x.parquet"
    bad.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(FeatureIOError):
        assert_output_path_under_features(bad, label="bad")


def test_assert_output_path_under_features_rejects_outside_microstructure(
    tmp_path,
) -> None:
    bad = tmp_path / "data" / "research" / "x.parquet"
    bad.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(FeatureIOError):
        assert_output_path_under_features(bad, label="bad")


def test_derive_feature_output_path_layout(tmp_path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "features"
    output_root.mkdir(parents=True, exist_ok=True)
    p = derive_feature_output_path(
        output_root=output_root, symbol="BTCUSDT", utc_date="2025-01-15"
    )
    expected_tail = (
        f"features/{FEATURE_DATASET_FAMILY}/BTCUSDT/2025/01/"
        "BTCUSDT-features-aggtrades-2025-01-15.parquet"
    )
    assert str(p).replace("\\", "/").endswith(expected_tail)


def test_derive_feature_output_path_rejects_lowercase_symbol(tmp_path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "features"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(FeatureIOError):
        derive_feature_output_path(
            output_root=output_root, symbol="btcusdt", utc_date="2025-01-15"
        )


def test_derive_feature_manifest_output_path_uses_canonical_filename(
    tmp_path,
) -> None:
    manifests_root = tmp_path / "data" / "microstructure" / "manifests"
    manifests_root.mkdir(parents=True, exist_ok=True)
    p = derive_feature_manifest_output_path(manifests_root=manifests_root)
    assert p.name == f"{FEATURE_DATASET_FAMILY}__v001.json"


def test_resolve_default_manifests_root(tmp_path) -> None:
    micro = tmp_path / "data" / "microstructure"
    micro.mkdir(parents=True, exist_ok=True)
    root = resolve_default_manifests_root(microstructure_root=micro)
    assert root.name == "manifests"
    assert root.parent == micro


def test_atomic_write_feature_manifest_refuses_overwrite(tmp_path) -> None:
    manifests_root = tmp_path / "data" / "microstructure" / "manifests"
    manifests_root.mkdir(parents=True, exist_ok=True)
    target = manifests_root / "x.json"
    sha1, _ = atomic_write_feature_manifest(target, {"a": 1}, refuse_overwrite=True)
    with pytest.raises(FeatureIOError):
        atomic_write_feature_manifest(target, {"a": 2}, refuse_overwrite=True)
    assert json.loads(target.read_text())["a"] == 1
    assert len(sha1) == 64


def test_write_feature_sha256_sidecar_format(tmp_path) -> None:
    target = tmp_path / "data" / "microstructure" / "features" / "x.sha256"
    target.parent.mkdir(parents=True, exist_ok=True)
    sha = "1" * 64
    sha_of_sidecar, size = write_feature_sha256_sidecar(
        target, target_filename="x.parquet", sha256_hex=sha, refuse_overwrite=True
    )
    assert target.read_text(encoding="ascii") == f"{sha}  x.parquet\n"
    assert len(sha_of_sidecar) == 64
    assert size > 0


def test_write_feature_sha256_sidecar_refuses_overwrite(tmp_path) -> None:
    target = tmp_path / "data" / "microstructure" / "features" / "y.sha256"
    target.parent.mkdir(parents=True, exist_ok=True)
    sha = "2" * 64
    write_feature_sha256_sidecar(
        target, target_filename="y.parquet", sha256_hex=sha, refuse_overwrite=True
    )
    with pytest.raises(FeatureIOError):
        write_feature_sha256_sidecar(
            target, target_filename="y.parquet", sha256_hex=sha, refuse_overwrite=True
        )


def test_write_feature_sha256_sidecar_rejects_short_sha(tmp_path) -> None:
    target = tmp_path / "data" / "microstructure" / "features" / "z.sha256"
    target.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(FeatureIOError):
        write_feature_sha256_sidecar(
            target, target_filename="z.parquet", sha256_hex="abc", refuse_overwrite=True
        )


def test_read_normalized_parquet_round_trip(tmp_path) -> None:
    bundle = build_feature_fixture(tmp_path)
    table, sha, size = read_normalized_parquet(bundle.normalized_parquet_path)
    assert table.num_rows == bundle.row_count
    assert sha == bundle.normalized_parquet_sha256
    assert size > 0


def test_read_source_normalized_manifest_requires_pending(tmp_path) -> None:
    bundle = build_feature_fixture(tmp_path)
    parsed, sha = read_source_normalized_manifest(bundle.normalized_manifest_path)
    assert parsed["research_eligible"] is False
    assert parsed["eligibility_gate_status"] == "pending"
    assert sha == bundle.normalized_manifest_sha256


def test_read_source_normalized_manifest_rejects_research_eligible_true(
    tmp_path,
) -> None:
    bundle = build_feature_fixture(tmp_path)
    text = bundle.normalized_manifest_path.read_text(encoding="utf-8")
    parsed = json.loads(text)
    parsed["research_eligible"] = True
    bundle.normalized_manifest_path.write_text(
        json.dumps(parsed, sort_keys=True, indent=2), encoding="utf-8"
    )
    with pytest.raises(FeatureIOError):
        read_source_normalized_manifest(bundle.normalized_manifest_path)


def test_read_successor_state_requires_stage3_eligible_pass(tmp_path) -> None:
    bundle = build_feature_fixture(tmp_path)
    parsed, sha = read_successor_state(bundle.successor_state_path)
    assert parsed["successor_stage"] == "Stage-3"
    assert parsed["successor_research_eligible"] is True
    assert parsed["successor_eligibility_gate_status"] == "pass"
    assert sha == bundle.successor_state_sha256


def test_read_successor_state_rejects_non_stage3(tmp_path) -> None:
    bundle = build_feature_fixture(tmp_path)
    text = bundle.successor_state_path.read_text(encoding="utf-8")
    parsed = json.loads(text)
    parsed["successor_stage"] = "Stage-2"
    bundle.successor_state_path.write_text(
        json.dumps(parsed, sort_keys=True, indent=2), encoding="utf-8"
    )
    with pytest.raises(FeatureIOError):
        read_successor_state(bundle.successor_state_path)


def test_hash_source_file_returns_path_and_size(tmp_path) -> None:
    p = tmp_path / "x.bin"
    p.write_bytes(b"abc" * 100)
    summary = hash_source_file(p, label="x")
    assert summary.path == p
    assert summary.size_bytes == len(p.read_bytes())
    assert len(summary.sha256) == 64


def test_hash_source_file_missing_path_raises(tmp_path) -> None:
    p = tmp_path / "missing.bin"
    with pytest.raises(FeatureIOError):
        hash_source_file(p, label="missing")


def test_atomic_write_feature_manifest_outside_manifests_rejected(tmp_path) -> None:
    bad = tmp_path / "data" / "microstructure" / "features" / "x.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(FeatureIOError):
        atomic_write_feature_manifest(bad, {"a": 1}, refuse_overwrite=True)


def test_assert_output_path_under_features_rejects_non_path() -> None:
    with pytest.raises(FeatureIOError):
        assert_output_path_under_features("not-a-path", label="bad")  # type: ignore[arg-type]
