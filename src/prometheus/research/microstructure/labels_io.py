"""Phase 4bj-C aggTrades label-dataset I/O helpers.

Atomic write-then-rename helpers for label Parquet and label manifest
JSON, restricted to:

- ``data/microstructure/labels/microstructure_labels_aggtrades_v001/``
  for the label Parquet (and paired ``.sha256`` sidecar);
- ``data/microstructure/manifests/`` for the label manifest JSON
  (and paired ``.sha256`` sidecar).

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute labels or signals;
- does NOT mutate any source artefact (feature parquet, feature
  manifest, Phase 4bi-B feature-family gate report, Phase 4bi-D
  successor-state JSON, normalized parquet, original derived
  manifest, raw manifest, raw zip);
- refuses to overwrite any pre-existing finalised output.
"""

from __future__ import annotations

import contextlib
import json
import os
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .normalize_io import (
    DEFAULT_DATA_MICROSTRUCTURE_PARTS,
    MANIFESTS_SUBDIR,
    _resolve_path_parts_under,
    compute_bytes_sha256,
    compute_file_sha256,
)

if TYPE_CHECKING:  # pragma: no cover - type-only
    import pyarrow as pa


LABELS_FAMILY_SUBDIR = "labels"
"""Subdirectory under ``data/microstructure/`` reserved for label output."""

LABEL_DATASET_FAMILY = "microstructure_labels_aggtrades_v001"
"""Constant label family name for Phase 4bj-C."""


class LabelIOError(RuntimeError):
    """Raised when a Phase 4bj-C label I/O operation fails closed."""


# ---------------------------------------------------------------------------
# Path discipline
# ---------------------------------------------------------------------------


def assert_label_path_under_data_microstructure(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/``."""
    if not isinstance(path, Path):
        raise LabelIOError(f"{label} must be a pathlib.Path")
    if not _resolve_path_parts_under(path, DEFAULT_DATA_MICROSTRUCTURE_PARTS):
        raise LabelIOError(
            f"{label} must resolve under data/microstructure/ (got {path!s})"
        )


def assert_output_path_under_labels(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/labels/``."""
    assert_label_path_under_data_microstructure(path, label=label)
    if not _resolve_path_parts_under(
        path, DEFAULT_DATA_MICROSTRUCTURE_PARTS + (LABELS_FAMILY_SUBDIR,)
    ):
        raise LabelIOError(
            f"{label} must resolve under data/microstructure/labels/ (got {path!s})"
        )


def assert_label_manifest_path_under_manifests(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/manifests/``."""
    assert_label_path_under_data_microstructure(path, label=label)
    if not _resolve_path_parts_under(
        path, DEFAULT_DATA_MICROSTRUCTURE_PARTS + (MANIFESTS_SUBDIR,)
    ):
        raise LabelIOError(
            f"{label} must resolve under data/microstructure/manifests/ (got {path!s})"
        )


def derive_label_output_path(
    *,
    output_root: Path,
    symbol: str,
    utc_date: str,
) -> Path:
    """Compute the label Parquet path for ``(symbol, utc_date)``.

    Layout (relative to *output_root*):
    ``microstructure_labels_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-labels-aggtrades-<YYYY-MM-DD>.parquet``.
    """
    if not isinstance(output_root, Path):
        raise LabelIOError("output_root must be a pathlib.Path")
    assert_label_path_under_data_microstructure(output_root, label="output_root")
    if not symbol or not symbol.isalnum() or symbol != symbol.upper():
        raise LabelIOError("symbol must be uppercase alphanumeric")
    parts = utc_date.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise LabelIOError(f"utc_date must be YYYY-MM-DD; got {utc_date!r}")
    yyyy, mm, _dd = parts
    return (
        output_root
        / LABEL_DATASET_FAMILY
        / symbol
        / yyyy
        / mm
        / f"{symbol}-labels-aggtrades-{utc_date}.parquet"
    )


def derive_label_manifest_output_path(*, manifests_root: Path) -> Path:
    """Compute the label manifest path under ``data/microstructure/manifests/``."""
    if not isinstance(manifests_root, Path):
        raise LabelIOError("manifests_root must be a pathlib.Path")
    assert_label_manifest_path_under_manifests(manifests_root, label="manifests_root")
    return manifests_root / f"{LABEL_DATASET_FAMILY}__v001.json"


# ---------------------------------------------------------------------------
# Atomic writers
# ---------------------------------------------------------------------------


def atomic_write_label_parquet(
    path: Path,
    table: pa.Table,
    *,
    refuse_overwrite: bool = True,
    compression: str = "zstd",
) -> tuple[str, int]:
    """Atomically write *table* to *path* as Parquet; return ``(sha256, size)``.

    Path discipline: must resolve under ``data/microstructure/labels/``.
    """
    if not isinstance(path, Path):
        raise LabelIOError("path must be a pathlib.Path")
    assert_output_path_under_labels(path, label="label parquet output path")
    if refuse_overwrite and path.exists():
        raise LabelIOError(f"refusing to overwrite existing file: {path}")
    tmp_companion = path.with_suffix(path.suffix + ".tmp")
    if tmp_companion.exists():
        raise LabelIOError(f"stale .tmp companion exists: {tmp_companion}")
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover - environment guard
        raise LabelIOError("pyarrow is required for Phase 4bj-C") from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_str = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=path.parent,
    )
    tmp_path = Path(tmp_str)
    try:
        os.close(fd)
        pq.write_table(table, tmp_path, compression=compression)
        with tmp_path.open("rb") as f, contextlib.suppress(OSError):
            os.fsync(f.fileno())
        sha, size = compute_file_sha256(tmp_path)
        os.replace(tmp_path, path)
        return sha, size
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise


def atomic_write_label_manifest(
    path: Path,
    obj: Mapping[str, Any] | dict[str, Any],
    *,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Atomically write *obj* as JSON to *path*; return ``(sha256, size)``.

    Path discipline: must resolve under ``data/microstructure/manifests/``.
    JSON is serialised with sorted keys, two-space indent, and a
    trailing newline for deterministic output.
    """
    if not isinstance(path, Path):
        raise LabelIOError("path must be a pathlib.Path")
    assert_label_manifest_path_under_manifests(path, label="label manifest output path")
    if refuse_overwrite and path.exists():
        raise LabelIOError(f"refusing to overwrite existing file: {path}")
    tmp_companion = path.with_suffix(path.suffix + ".tmp")
    if tmp_companion.exists():
        raise LabelIOError(f"stale .tmp companion exists: {tmp_companion}")
    payload = (
        json.dumps(dict(obj), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_str = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=path.parent,
    )
    tmp_path = Path(tmp_str)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(payload)
            f.flush()
            with contextlib.suppress(OSError):
                os.fsync(f.fileno())
        sha = compute_bytes_sha256(payload)
        size = len(payload)
        os.replace(tmp_path, path)
        return sha, size
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise


def write_label_sha256_sidecar(
    path: Path,
    *,
    target_filename: str,
    sha256_hex: str,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Write a paired ``.sha256`` sidecar at *path*; return ``(sha256, size)``.

    Path discipline: must resolve under ``data/microstructure/``.
    """
    if not isinstance(path, Path):
        raise LabelIOError("path must be a pathlib.Path")
    assert_label_path_under_data_microstructure(path, label="sidecar path")
    if refuse_overwrite and path.exists():
        raise LabelIOError(f"refusing to overwrite existing file: {path}")
    if len(sha256_hex) != 64:
        raise LabelIOError("sha256_hex must be 64 lowercase hex chars")
    payload = f"{sha256_hex}  {target_filename}\n".encode("ascii")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_str = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=path.parent,
    )
    tmp_path = Path(tmp_str)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(payload)
            f.flush()
            with contextlib.suppress(OSError):
                os.fsync(f.fileno())
        sha = compute_bytes_sha256(payload)
        size = len(payload)
        os.replace(tmp_path, path)
        return sha, size
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise


__all__ = [
    "LABELS_FAMILY_SUBDIR",
    "LABEL_DATASET_FAMILY",
    "LabelIOError",
    "assert_label_manifest_path_under_manifests",
    "assert_label_path_under_data_microstructure",
    "assert_output_path_under_labels",
    "atomic_write_label_manifest",
    "atomic_write_label_parquet",
    "derive_label_manifest_output_path",
    "derive_label_output_path",
    "write_label_sha256_sidecar",
]
