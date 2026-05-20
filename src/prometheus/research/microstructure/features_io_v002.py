"""Phase 4bm-H multi-day v002 aggTrades feature I/O helpers.

This module provides v002-specific path helpers for the multi-day
feature family. Atomic Parquet / JSON / sidecar writers and source
loaders are reused verbatim from the v001 :mod:`features_io` module;
this module only adds path discipline for the v002 directory layout

    data/microstructure/features/microstructure_features_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-features-aggtrades-<YYYY-MM-DD>.parquet

The ``__v002`` directory suffix mirrors the v002 normalized derived
family layout
``microstructure_normalized_aggtrades_v001__v002/...`` produced by
Phase 4bm-B and preserves the Phase 4bm-G refuse-to-overwrite rule
against the previously written v001 single-day artefact at
``microstructure_features_aggtrades_v001/.../2025-01-15.parquet``.

The corresponding multi-day feature manifest is

    data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json

paired with its canonical Phase 4bb-F sidecar.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute features, labels, signals, returns, or any
  execution-quality / order-flow proxy;
- only declares path constants and small deterministic path helpers.
"""

from __future__ import annotations

from pathlib import Path

from .features_io import (
    FEATURE_DATASET_FAMILY,
    FEATURES_FAMILY_SUBDIR,
    FeatureIOError,
    assert_manifest_output_path_under_manifests,
    assert_output_path_under_features,
    assert_path_under_data_microstructure,
)
from .features_schema_v002 import FEATURE_DATASET_VERSION_V002

V002_FEATURE_DIR_SEGMENT = (
    f"{FEATURE_DATASET_FAMILY}__{FEATURE_DATASET_VERSION_V002}"
)
"""Directory segment under ``data/microstructure/features/`` for v002 output."""

V002_FEATURE_MANIFEST_BASENAME = (
    f"{FEATURE_DATASET_FAMILY}__{FEATURE_DATASET_VERSION_V002}.json"
)
"""Filename of the v002 feature manifest under ``data/microstructure/manifests/``."""


def derive_v002_feature_parquet_path(
    *,
    features_root: Path,
    symbol: str,
    utc_date: str,
) -> Path:
    """Compute the v002 feature Parquet path for ``(symbol, utc_date)``.

    Layout (relative to *features_root*, which itself must resolve to
    ``data/microstructure/features/``):
    ``microstructure_features_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-features-aggtrades-<YYYY-MM-DD>.parquet``.
    """
    if not isinstance(features_root, Path):
        raise FeatureIOError("features_root must be a pathlib.Path")
    assert_path_under_data_microstructure(features_root, label="features_root")
    if features_root.name != FEATURES_FAMILY_SUBDIR:
        raise FeatureIOError(
            f"features_root must end in {FEATURES_FAMILY_SUBDIR!r} "
            f"(got name={features_root.name!r})"
        )
    if not symbol or not symbol.isalnum() or symbol != symbol.upper():
        raise FeatureIOError("symbol must be uppercase alphanumeric")
    parts = utc_date.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise FeatureIOError(f"utc_date must be YYYY-MM-DD; got {utc_date!r}")
    yyyy, mm, _dd = parts
    out = (
        features_root
        / V002_FEATURE_DIR_SEGMENT
        / symbol
        / yyyy
        / mm
        / f"{symbol}-features-aggtrades-{utc_date}.parquet"
    )
    # Verify the resolved path still lies under data/microstructure/features/.
    assert_output_path_under_features(out, label="v002 feature parquet output path")
    return out


def derive_v002_feature_manifest_path(*, manifests_root: Path) -> Path:
    """Compute the v002 feature manifest path under ``data/microstructure/manifests/``."""
    if not isinstance(manifests_root, Path):
        raise FeatureIOError("manifests_root must be a pathlib.Path")
    out = manifests_root / V002_FEATURE_MANIFEST_BASENAME
    assert_manifest_output_path_under_manifests(
        out, label="v002 feature manifest output path"
    )
    return out


def compose_canonical_sidecar_v002(*, sha256_hex: str, basename: str) -> bytes:
    """Compose the canonical Phase 4bb-F sidecar body as ASCII bytes.

    Format: ``<sha256_lowercase_hex><two ASCII spaces><basename><LF>``.
    """
    if not isinstance(sha256_hex, str) or len(sha256_hex) != 64:
        raise FeatureIOError("sha256_hex must be a 64-char lowercase hex string")
    if sha256_hex.lower() != sha256_hex:
        raise FeatureIOError("sha256_hex must be lowercase hex")
    if not isinstance(basename, str) or not basename or "\n" in basename:
        raise FeatureIOError("basename must be a non-empty single-line string")
    return f"{sha256_hex}  {basename}\n".encode("ascii")


__all__ = [
    "V002_FEATURE_DIR_SEGMENT",
    "V002_FEATURE_MANIFEST_BASENAME",
    "compose_canonical_sidecar_v002",
    "derive_v002_feature_manifest_path",
    "derive_v002_feature_parquet_path",
]
