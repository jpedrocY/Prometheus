"""Phase 4bm-O multi-day v002 aggTrades label I/O helpers.

This module provides v002-specific path helpers for the multi-day
label family. Atomic Parquet / JSON / sidecar writers are reused
verbatim from the v001 :mod:`labels_io` module; this module only adds
path discipline for the v002 directory layout

    data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-labels-aggtrades-<YYYY-MM-DD>.parquet

The ``__v002`` directory suffix mirrors the v002 normalized and v002
feature directory layouts (Phase 4bm-B / Phase 4bm-H) and preserves the
refuse-to-overwrite rule against any prior v001 single-day artefact at
``microstructure_labels_aggtrades_v001/.../2025-01-15.parquet`` produced
by Phase 4bj-C.

The corresponding multi-day label manifest is

    data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json

paired with its canonical Phase 4bb-F sidecar.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute labels, signals, returns, or any execution-quality
  / order-flow proxy;
- only declares path constants and small deterministic path helpers.
"""

from __future__ import annotations

from pathlib import Path

from .labels_io import (
    LABEL_DATASET_FAMILY,
    LABELS_FAMILY_SUBDIR,
    LabelIOError,
    assert_label_manifest_path_under_manifests,
    assert_label_path_under_data_microstructure,
    assert_output_path_under_labels,
)
from .labels_schema_v002 import LABEL_DATASET_VERSION_V002

V002_LABEL_DIR_SEGMENT = f"{LABEL_DATASET_FAMILY}__{LABEL_DATASET_VERSION_V002}"
"""Directory segment under ``data/microstructure/labels/`` for v002 output."""

V002_LABEL_MANIFEST_BASENAME = (
    f"{LABEL_DATASET_FAMILY}__{LABEL_DATASET_VERSION_V002}.json"
)
"""Filename of the v002 label manifest under ``data/microstructure/manifests/``."""


def derive_v002_label_parquet_path(
    *,
    labels_root: Path,
    symbol: str,
    utc_date: str,
) -> Path:
    """Compute the v002 label Parquet path for ``(symbol, utc_date)``.

    Layout (relative to *labels_root*, which itself must resolve to
    ``data/microstructure/labels/``):
    ``microstructure_labels_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-labels-aggtrades-<YYYY-MM-DD>.parquet``.
    """
    if not isinstance(labels_root, Path):
        raise LabelIOError("labels_root must be a pathlib.Path")
    assert_label_path_under_data_microstructure(labels_root, label="labels_root")
    if labels_root.name != LABELS_FAMILY_SUBDIR:
        raise LabelIOError(
            f"labels_root must end in {LABELS_FAMILY_SUBDIR!r} "
            f"(got name={labels_root.name!r})"
        )
    if not symbol or not symbol.isalnum() or symbol != symbol.upper():
        raise LabelIOError("symbol must be uppercase alphanumeric")
    parts = utc_date.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise LabelIOError(f"utc_date must be YYYY-MM-DD; got {utc_date!r}")
    yyyy, mm, _dd = parts
    out = (
        labels_root
        / V002_LABEL_DIR_SEGMENT
        / symbol
        / yyyy
        / mm
        / f"{symbol}-labels-aggtrades-{utc_date}.parquet"
    )
    # Verify the resolved path still lies under data/microstructure/labels/.
    assert_output_path_under_labels(out, label="v002 label parquet output path")
    return out


def derive_v002_label_manifest_path(*, manifests_root: Path) -> Path:
    """Compute the v002 label manifest path under ``data/microstructure/manifests/``."""
    if not isinstance(manifests_root, Path):
        raise LabelIOError("manifests_root must be a pathlib.Path")
    out = manifests_root / V002_LABEL_MANIFEST_BASENAME
    assert_label_manifest_path_under_manifests(
        out, label="v002 label manifest output path"
    )
    return out


def compose_canonical_sidecar_v002_label(
    *, sha256_hex: str, basename: str
) -> bytes:
    """Compose the canonical Phase 4bb-F sidecar body as ASCII bytes.

    Format: ``<sha256_lowercase_hex><two ASCII spaces><basename><LF>``.
    """
    if not isinstance(sha256_hex, str) or len(sha256_hex) != 64:
        raise LabelIOError("sha256_hex must be a 64-char lowercase hex string")
    if sha256_hex.lower() != sha256_hex:
        raise LabelIOError("sha256_hex must be lowercase hex")
    if not isinstance(basename, str) or not basename or "\n" in basename:
        raise LabelIOError("basename must be a non-empty single-line string")
    return f"{sha256_hex}  {basename}\n".encode("ascii")


__all__ = [
    "V002_LABEL_DIR_SEGMENT",
    "V002_LABEL_MANIFEST_BASENAME",
    "compose_canonical_sidecar_v002_label",
    "derive_v002_label_manifest_path",
    "derive_v002_label_parquet_path",
]
