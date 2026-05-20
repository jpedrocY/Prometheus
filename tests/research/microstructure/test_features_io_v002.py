"""Phase 4bm-H v002 feature path helpers and canonical sidecar tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.microstructure import (
    V002_FEATURE_DIR_SEGMENT,
    V002_FEATURE_MANIFEST_BASENAME,
    compose_canonical_sidecar_v002,
    derive_v002_feature_manifest_path,
    derive_v002_feature_parquet_path,
)
from prometheus.research.microstructure.features_io import FeatureIOError


def test_v002_path_constants() -> None:
    assert V002_FEATURE_DIR_SEGMENT == "microstructure_features_aggtrades_v001__v002"
    assert V002_FEATURE_MANIFEST_BASENAME == "microstructure_features_aggtrades_v001__v002.json"


def test_derive_v002_feature_parquet_path_layout(tmp_path: Path) -> None:
    features_root = tmp_path / "data" / "microstructure" / "features"
    features_root.mkdir(parents=True)
    out = derive_v002_feature_parquet_path(
        features_root=features_root, symbol="BTCUSDT", utc_date="2024-12-01"
    )
    rel = out.relative_to(features_root)
    assert rel.as_posix() == (
        "microstructure_features_aggtrades_v001__v002/BTCUSDT/2024/12/"
        "BTCUSDT-features-aggtrades-2024-12-01.parquet"
    )


def test_derive_v002_feature_manifest_path_layout(tmp_path: Path) -> None:
    manifests_root = tmp_path / "data" / "microstructure" / "manifests"
    manifests_root.mkdir(parents=True)
    p = derive_v002_feature_manifest_path(manifests_root=manifests_root)
    assert p.name == V002_FEATURE_MANIFEST_BASENAME
    assert p.parent == manifests_root


def test_derive_v002_path_rejects_lowercase_symbol(tmp_path: Path) -> None:
    features_root = tmp_path / "data" / "microstructure" / "features"
    features_root.mkdir(parents=True)
    with pytest.raises(FeatureIOError):
        derive_v002_feature_parquet_path(
            features_root=features_root, symbol="btcusdt", utc_date="2024-12-01"
        )


def test_derive_v002_path_rejects_bad_date(tmp_path: Path) -> None:
    features_root = tmp_path / "data" / "microstructure" / "features"
    features_root.mkdir(parents=True)
    with pytest.raises(FeatureIOError):
        derive_v002_feature_parquet_path(
            features_root=features_root, symbol="BTCUSDT", utc_date="2024/12/01"
        )


def test_derive_v002_path_rejects_non_microstructure_root(tmp_path: Path) -> None:
    bad_root = tmp_path / "not_microstructure"
    bad_root.mkdir(parents=True)
    with pytest.raises(FeatureIOError):
        derive_v002_feature_parquet_path(
            features_root=bad_root, symbol="BTCUSDT", utc_date="2024-12-01"
        )


def test_compose_canonical_sidecar_v002_format() -> None:
    """Canonical Phase 4bb-F sidecar format: <sha><2-space><basename><LF>."""
    body = compose_canonical_sidecar_v002(
        sha256_hex="a" * 64, basename="BTCUSDT-features-aggtrades-2024-12-01.parquet"
    )
    expected = b"a" * 64 + b"  BTCUSDT-features-aggtrades-2024-12-01.parquet\n"
    assert body == expected
    # Exactly two ASCII spaces between SHA and basename.
    assert body[64:66] == b"  "
    # Trailing LF.
    assert body.endswith(b"\n")
    # No CR / no BOM.
    assert b"\r" not in body
    assert not body.startswith(b"\xef\xbb\xbf")


def test_compose_canonical_sidecar_v002_rejects_invalid_inputs() -> None:
    with pytest.raises(FeatureIOError):
        compose_canonical_sidecar_v002(sha256_hex="tooshort", basename="x.parquet")
    with pytest.raises(FeatureIOError):
        compose_canonical_sidecar_v002(sha256_hex="A" * 64, basename="x.parquet")
    with pytest.raises(FeatureIOError):
        compose_canonical_sidecar_v002(sha256_hex="a" * 64, basename="")
    with pytest.raises(FeatureIOError):
        compose_canonical_sidecar_v002(sha256_hex="a" * 64, basename="x\ny.parquet")
