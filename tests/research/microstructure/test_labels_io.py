"""Phase 4bj-C label I/O tests (tmp_path only)."""

from __future__ import annotations

from pathlib import Path

import pyarrow as pa
import pytest

from prometheus.research.microstructure.labels_io import (
    LABEL_DATASET_FAMILY,
    LabelIOError,
    atomic_write_label_manifest,
    atomic_write_label_parquet,
    derive_label_manifest_output_path,
    derive_label_output_path,
    write_label_sha256_sidecar,
)


def _make_tiny_table() -> pa.Table:
    return pa.Table.from_pydict(
        {
            "row_index": pa.array([0, 1, 2], type=pa.int64()),
            "value": pa.array(["a", "b", "c"], type=pa.string()),
        }
    )


def _build_microstructure_root(tmp_path: Path) -> Path:
    root = tmp_path / "data" / "microstructure"
    root.mkdir(parents=True, exist_ok=True)
    return root


def test_derive_label_output_path(tmp_path: Path) -> None:
    root = _build_microstructure_root(tmp_path) / "labels"
    p = derive_label_output_path(
        output_root=root, symbol="BTCUSDT", utc_date="2025-01-15"
    )
    assert p.as_posix().endswith(
        f"data/microstructure/labels/{LABEL_DATASET_FAMILY}/"
        "BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet"
    )


def test_derive_label_output_path_rejects_outside_microstructure(tmp_path: Path) -> None:
    bad_root = tmp_path / "data" / "labels"
    bad_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        derive_label_output_path(
            output_root=bad_root, symbol="BTCUSDT", utc_date="2025-01-15"
        )


def test_derive_label_output_path_rejects_bad_symbol_or_date(tmp_path: Path) -> None:
    root = _build_microstructure_root(tmp_path) / "labels"
    with pytest.raises(LabelIOError):
        derive_label_output_path(
            output_root=root, symbol="btcusdt", utc_date="2025-01-15"
        )
    with pytest.raises(LabelIOError):
        derive_label_output_path(
            output_root=root, symbol="BTCUSDT", utc_date="2025/01/15"
        )


def test_derive_label_manifest_output_path(tmp_path: Path) -> None:
    root = _build_microstructure_root(tmp_path) / "manifests"
    p = derive_label_manifest_output_path(manifests_root=root)
    assert p.name == f"{LABEL_DATASET_FAMILY}__v001.json"
    assert "data/microstructure/manifests/" in p.as_posix()


def test_atomic_write_label_parquet_atomic_and_sidecar(tmp_path: Path) -> None:
    root = _build_microstructure_root(tmp_path) / "labels"
    target = root / "x.parquet"
    sha, size = atomic_write_label_parquet(target, _make_tiny_table())
    assert target.exists()
    assert size == target.stat().st_size
    sidecar = target.with_suffix(target.suffix + ".sha256")
    sidecar_sha, sidecar_size = write_label_sha256_sidecar(
        sidecar, target_filename=target.name, sha256_hex=sha
    )
    assert sidecar.exists()
    payload = sidecar.read_text(encoding="ascii")
    assert payload.startswith(sha)
    assert target.name in payload
    assert sidecar_size == len(payload.encode("utf-8"))
    assert sidecar_sha


def test_atomic_write_label_parquet_refuses_overwrite(tmp_path: Path) -> None:
    root = _build_microstructure_root(tmp_path) / "labels"
    target = root / "y.parquet"
    atomic_write_label_parquet(target, _make_tiny_table())
    with pytest.raises(LabelIOError):
        atomic_write_label_parquet(target, _make_tiny_table())


def test_atomic_write_label_parquet_rejects_outside_labels(tmp_path: Path) -> None:
    bad_target = tmp_path / "data" / "microstructure" / "wrong" / "x.parquet"
    bad_target.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        atomic_write_label_parquet(bad_target, _make_tiny_table())


def test_atomic_write_label_parquet_rejects_outside_data_microstructure(
    tmp_path: Path,
) -> None:
    bad_target = tmp_path / "some" / "labels" / "x.parquet"
    bad_target.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        atomic_write_label_parquet(bad_target, _make_tiny_table())


def test_atomic_write_label_manifest_atomic(tmp_path: Path) -> None:
    root = _build_microstructure_root(tmp_path) / "manifests"
    target = root / "x.json"
    payload = {"dataset_family": "microstructure_labels_aggtrades_v001"}
    sha, size = atomic_write_label_manifest(target, payload)
    assert target.exists()
    text = target.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert "microstructure_labels_aggtrades_v001" in text
    assert size == target.stat().st_size
    assert sha


def test_atomic_write_label_manifest_refuses_overwrite(tmp_path: Path) -> None:
    root = _build_microstructure_root(tmp_path) / "manifests"
    target = root / "y.json"
    atomic_write_label_manifest(target, {"k": "v"})
    with pytest.raises(LabelIOError):
        atomic_write_label_manifest(target, {"k": "w"})


def test_atomic_write_label_manifest_rejects_outside_manifests(tmp_path: Path) -> None:
    bad_target = tmp_path / "data" / "microstructure" / "wrong" / "x.json"
    bad_target.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        atomic_write_label_manifest(bad_target, {"k": "v"})


def test_write_label_sha256_sidecar_refuses_invalid_hash(tmp_path: Path) -> None:
    root = _build_microstructure_root(tmp_path) / "labels"
    sidecar = root / "x.parquet.sha256"
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        write_label_sha256_sidecar(
            sidecar, target_filename="x.parquet", sha256_hex="not-hex"
        )


def test_write_label_sha256_sidecar_refuses_outside_data_microstructure(
    tmp_path: Path,
) -> None:
    sidecar = tmp_path / "elsewhere" / "x.sha256"
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        write_label_sha256_sidecar(
            sidecar, target_filename="x", sha256_hex="0" * 64
        )
