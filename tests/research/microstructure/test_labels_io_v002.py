"""Phase 4bm-O v002 label IO and path-discipline tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.microstructure.labels_io import LabelIOError
from prometheus.research.microstructure.labels_io_v002 import (
    V002_LABEL_DIR_SEGMENT,
    V002_LABEL_MANIFEST_BASENAME,
    compose_canonical_sidecar_v002_label,
    derive_v002_label_manifest_path,
    derive_v002_label_parquet_path,
)


def test_v002_label_dir_segment_constant() -> None:
    assert V002_LABEL_DIR_SEGMENT == "microstructure_labels_aggtrades_v001__v002"


def test_v002_label_manifest_basename_constant() -> None:
    assert (
        V002_LABEL_MANIFEST_BASENAME
        == "microstructure_labels_aggtrades_v001__v002.json"
    )


def test_derive_v002_label_parquet_path_under_labels(tmp_path: Path) -> None:
    labels_root = tmp_path / "data" / "microstructure" / "labels"
    labels_root.mkdir(parents=True, exist_ok=True)
    out = derive_v002_label_parquet_path(
        labels_root=labels_root,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
    )
    assert out == (
        labels_root
        / "microstructure_labels_aggtrades_v001__v002"
        / "BTCUSDT"
        / "2024"
        / "12"
        / "BTCUSDT-labels-aggtrades-2024-12-01.parquet"
    )


def test_derive_v002_label_parquet_path_requires_labels_root(tmp_path: Path) -> None:
    bad_root = tmp_path / "data" / "microstructure" / "features"
    bad_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        derive_v002_label_parquet_path(
            labels_root=bad_root, symbol="BTCUSDT", utc_date="2024-12-01"
        )


def test_derive_v002_label_parquet_path_rejects_bad_symbol(tmp_path: Path) -> None:
    labels_root = tmp_path / "data" / "microstructure" / "labels"
    labels_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        derive_v002_label_parquet_path(
            labels_root=labels_root, symbol="btcusdt", utc_date="2024-12-01"
        )


def test_derive_v002_label_parquet_path_rejects_bad_date(tmp_path: Path) -> None:
    labels_root = tmp_path / "data" / "microstructure" / "labels"
    labels_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        derive_v002_label_parquet_path(
            labels_root=labels_root, symbol="BTCUSDT", utc_date="2024/12/01"
        )


def test_derive_v002_label_manifest_path_under_manifests(tmp_path: Path) -> None:
    manifests_root = tmp_path / "data" / "microstructure" / "manifests"
    manifests_root.mkdir(parents=True, exist_ok=True)
    out = derive_v002_label_manifest_path(manifests_root=manifests_root)
    assert out == manifests_root / V002_LABEL_MANIFEST_BASENAME


def test_derive_v002_label_manifest_path_rejects_bad_root(tmp_path: Path) -> None:
    bad_root = tmp_path / "wrong_place"
    bad_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelIOError):
        derive_v002_label_manifest_path(manifests_root=bad_root)


# ---------------------------------------------------------------------------
# Canonical sidecar composer (Phase 4bb-F two-space format)
# ---------------------------------------------------------------------------


def test_compose_canonical_sidecar_v002_label_format() -> None:
    out = compose_canonical_sidecar_v002_label(
        sha256_hex="0" * 64,
        basename="BTCUSDT-labels-aggtrades-2024-12-01.parquet",
    )
    # exactly: <sha256><two spaces><basename><LF>
    expected = b"0" * 64 + b"  BTCUSDT-labels-aggtrades-2024-12-01.parquet\n"
    assert out == expected


def test_compose_canonical_sidecar_v002_label_rejects_short_sha() -> None:
    with pytest.raises(LabelIOError):
        compose_canonical_sidecar_v002_label(sha256_hex="abc", basename="file")


def test_compose_canonical_sidecar_v002_label_rejects_uppercase_sha() -> None:
    with pytest.raises(LabelIOError):
        compose_canonical_sidecar_v002_label(
            sha256_hex="A" * 64, basename="file"
        )


def test_compose_canonical_sidecar_v002_label_rejects_basename_newline() -> None:
    with pytest.raises(LabelIOError):
        compose_canonical_sidecar_v002_label(
            sha256_hex="0" * 64, basename="bad\nname.parquet"
        )


def test_compose_canonical_sidecar_v002_label_uses_lf_only() -> None:
    out = compose_canonical_sidecar_v002_label(
        sha256_hex="0" * 64, basename="file.parquet"
    )
    assert b"\r" not in out
    assert out.endswith(b"\n")
