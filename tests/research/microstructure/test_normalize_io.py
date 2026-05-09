"""Phase 4bd tests for normalize_io helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pytest

from prometheus.research.microstructure.normalize_io import (
    NormalizationIOError,
    assert_manifest_path_under_manifests,
    assert_output_path_under_normalized,
    assert_path_under_microstructure,
    atomic_write_json,
    atomic_write_parquet,
    compute_bytes_sha256,
    compute_file_sha256,
    derive_manifest_output_path,
    derive_normalized_output_path,
    open_zip_single_csv_in_memory,
    read_acquisition_log,
    read_manifest_bytes,
    read_sidecar,
    relative_to_microstructure_root,
    resolve_source_artefact_paths,
    write_sha256_sidecar,
)

from ._normalize_fixtures import build_normalize_fixture


def test_assert_path_under_microstructure_accepts_namespace(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "x" / "y.txt"
    p.parent.mkdir(parents=True)
    p.write_text("ok")
    assert_path_under_microstructure(p, label="x")


def test_assert_path_under_microstructure_rejects_outside(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "y.txt"
    p.parent.mkdir(parents=True)
    p.write_text("ok")
    with pytest.raises(NormalizationIOError):
        assert_path_under_microstructure(p, label="x")


def test_assert_output_path_under_normalized_rejects_non_normalized(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "raw" / "y.parquet"
    p.parent.mkdir(parents=True)
    p.write_text("")
    with pytest.raises(NormalizationIOError):
        assert_output_path_under_normalized(p, label="x")


def test_assert_manifest_path_under_manifests_rejects_non_manifests(
    tmp_path: Path,
) -> None:
    p = tmp_path / "data" / "microstructure" / "raw" / "y.json"
    p.parent.mkdir(parents=True)
    p.write_text("{}")
    with pytest.raises(NormalizationIOError):
        assert_manifest_path_under_manifests(p, label="x")


def test_compute_file_sha256_matches_bytes_sha(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "x.bin"
    p.parent.mkdir(parents=True)
    p.write_bytes(b"hello world")
    sha, size = compute_file_sha256(p)
    assert size == 11
    assert sha == compute_bytes_sha256(b"hello world")


def test_atomic_write_parquet_writes_then_renames(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    target = (
        bundle.output_root
        / "normalized"
        / "microstructure_normalized_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-aggTrades-2025-01-15.parquet"
    )
    table = pa.table({"x": pa.array([1, 2, 3], type=pa.int64())})
    sha, size = atomic_write_parquet(target, table, refuse_overwrite=True)
    assert target.exists()
    recomputed, _ = compute_file_sha256(target)
    assert recomputed == sha
    assert size > 0


def test_atomic_write_parquet_rejects_path_outside_normalized(
    tmp_path: Path,
) -> None:
    bad = tmp_path / "data" / "microstructure" / "raw" / "out.parquet"
    bad.parent.mkdir(parents=True)
    table = pa.table({"x": pa.array([1], type=pa.int64())})
    with pytest.raises(NormalizationIOError):
        atomic_write_parquet(bad, table, refuse_overwrite=True)


def test_atomic_write_parquet_refuses_overwrite(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    target = (
        bundle.output_root
        / "normalized"
        / "microstructure_normalized_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-aggTrades-2025-01-15.parquet"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"existing")
    table = pa.table({"x": pa.array([1], type=pa.int64())})
    with pytest.raises(NormalizationIOError):
        atomic_write_parquet(target, table, refuse_overwrite=True)


def test_atomic_write_json_round_trip(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    target = bundle.manifests_root / "derived_manifest_test.json"
    sha, size = atomic_write_json(target, {"a": 1, "b": "x"}, refuse_overwrite=True)
    assert target.exists()
    parsed = json.loads(target.read_text(encoding="utf-8"))
    assert parsed == {"a": 1, "b": "x"}
    recomputed, _ = compute_file_sha256(target)
    assert recomputed == sha


def test_atomic_write_json_refuses_overwrite(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    target = bundle.manifests_root / "derived_manifest_test.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("{}")
    with pytest.raises(NormalizationIOError):
        atomic_write_json(target, {"a": 1}, refuse_overwrite=True)


def test_write_sha256_sidecar_format(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    sidecar = bundle.manifests_root / "x.json.sha256"
    sha = "0" * 64
    write_sha256_sidecar(
        sidecar, target_filename="x.json", sha256_hex=sha, refuse_overwrite=True
    )
    text = sidecar.read_text(encoding="utf-8")
    assert text.startswith(sha)
    assert "x.json" in text


def test_derive_normalized_output_path_layout(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    p = derive_normalized_output_path(
        output_root=bundle.output_root, symbol="BTCUSDT", utc_date="2025-01-15"
    )
    assert p.parts[-5:] == (
        "microstructure_normalized_aggtrades_v001",
        "BTCUSDT",
        "2025",
        "01",
        "BTCUSDT-aggTrades-2025-01-15.parquet",
    )


def test_derive_manifest_output_path_layout(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    p = derive_manifest_output_path(manifests_root=bundle.manifests_root)
    assert p.name == "microstructure_normalized_aggtrades_v001__v001.json"


def test_resolve_source_artefact_paths_round_trip(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    paths = resolve_source_artefact_paths(bundle.eligibility_bundle.manifest_path)
    assert paths.manifest_path.exists()
    assert paths.raw_zip_path.exists()
    assert paths.sidecar_path.exists()
    assert paths.acquisition_log_path.exists()


def test_read_manifest_and_sidecar_and_acq_log(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    raw, sha_man = read_manifest_bytes(bundle.eligibility_bundle.manifest_path)
    assert sha_man == compute_bytes_sha256(raw)
    text, first_64, sha_side = read_sidecar(bundle.eligibility_bundle.sidecar_path)
    assert len(first_64) == 64
    parsed_log, sha_log = read_acquisition_log(
        bundle.eligibility_bundle.acquisition_log_path
    )
    assert isinstance(parsed_log, dict)
    assert len(sha_log) == 64


def test_open_zip_single_csv_in_memory_reads_member(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    name, text, size = open_zip_single_csv_in_memory(
        bundle.eligibility_bundle.raw_zip_path
    )
    assert name.endswith(".csv")
    assert "agg_trade_id" in text or text.split(",")[0].isdigit()
    assert size > 0


def test_relative_to_microstructure_root_returns_relative(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    rel = relative_to_microstructure_root(bundle.eligibility_bundle.raw_zip_path)
    assert rel.startswith("raw/")
    assert rel.endswith("BTCUSDT-aggTrades-2025-01-15.zip")
