"""Phase 4bh aggTrades feature-dataset I/O helpers.

This module provides read-only loaders for the source normalized
parquet, source normalized manifest, and Phase 4bg-B successor-state
JSON, plus atomic Parquet/JSON writers restricted to the gitignored
``data/microstructure/features/`` and ``data/microstructure/manifests/``
namespaces.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute features, labels, or signals (helpers only);
- does NOT mutate any source artefact (normalized parquet, normalized
  manifest, raw artefacts, Phase 4bb-D / 4bf gate reports, Phase 4bg-B
  successor-state JSON);
- writes only under
  ``data/microstructure/features/microstructure_features_aggtrades_v001/``
  for Parquet and ``data/microstructure/manifests/`` for JSON manifest;
- refuses to overwrite an existing finalised feature output.
"""

from __future__ import annotations

import contextlib
import json
import os
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
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


FEATURES_FAMILY_SUBDIR = "features"
"""Subdirectory under ``data/microstructure/`` reserved for feature output."""

FEATURE_DATASET_FAMILY = "microstructure_features_aggtrades_v001"
"""Constant feature family name for Phase 4bh."""


class FeatureIOError(RuntimeError):
    """Raised when a Phase 4bh feature I/O operation fails closed."""


# ---------------------------------------------------------------------------
# Path discipline
# ---------------------------------------------------------------------------


def assert_path_under_data_microstructure(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/``."""
    if not isinstance(path, Path):
        raise FeatureIOError(f"{label} must be a pathlib.Path")
    if not _resolve_path_parts_under(path, DEFAULT_DATA_MICROSTRUCTURE_PARTS):
        raise FeatureIOError(
            f"{label} must resolve under data/microstructure/ (got {path!s})"
        )


def assert_output_path_under_features(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/features/``."""
    assert_path_under_data_microstructure(path, label=label)
    if not _resolve_path_parts_under(
        path, DEFAULT_DATA_MICROSTRUCTURE_PARTS + (FEATURES_FAMILY_SUBDIR,)
    ):
        raise FeatureIOError(
            f"{label} must resolve under data/microstructure/features/ (got {path!s})"
        )


def assert_manifest_output_path_under_manifests(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/manifests/``."""
    assert_path_under_data_microstructure(path, label=label)
    if not _resolve_path_parts_under(
        path, DEFAULT_DATA_MICROSTRUCTURE_PARTS + (MANIFESTS_SUBDIR,)
    ):
        raise FeatureIOError(
            f"{label} must resolve under data/microstructure/manifests/ (got {path!s})"
        )


def derive_feature_output_path(
    *,
    output_root: Path,
    symbol: str,
    utc_date: str,
) -> Path:
    """Compute the feature Parquet path for ``(symbol, utc_date)``.

    Layout (relative to *output_root*):
    ``microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-features-aggtrades-<YYYY-MM-DD>.parquet``.
    """
    if not isinstance(output_root, Path):
        raise FeatureIOError("output_root must be a pathlib.Path")
    assert_path_under_data_microstructure(output_root, label="output_root")
    if not symbol or not symbol.isalnum() or symbol != symbol.upper():
        raise FeatureIOError("symbol must be uppercase alphanumeric")
    parts = utc_date.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise FeatureIOError(
            f"utc_date must be YYYY-MM-DD; got {utc_date!r}"
        )
    yyyy, mm, _dd = parts
    return (
        output_root
        / FEATURE_DATASET_FAMILY
        / symbol
        / yyyy
        / mm
        / f"{symbol}-features-aggtrades-{utc_date}.parquet"
    )


def derive_feature_manifest_output_path(*, manifests_root: Path) -> Path:
    """Compute the feature manifest path under ``data/microstructure/manifests/``."""
    if not isinstance(manifests_root, Path):
        raise FeatureIOError("manifests_root must be a pathlib.Path")
    assert_manifest_output_path_under_manifests(
        manifests_root, label="manifests_root"
    )
    return manifests_root / f"{FEATURE_DATASET_FAMILY}__v001.json"


def resolve_default_manifests_root(*, microstructure_root: Path) -> Path:
    """Return ``data/microstructure/manifests/`` derived from *microstructure_root*."""
    if not isinstance(microstructure_root, Path):
        raise FeatureIOError("microstructure_root must be a pathlib.Path")
    assert_path_under_data_microstructure(
        microstructure_root, label="microstructure_root"
    )
    return microstructure_root / MANIFESTS_SUBDIR


# ---------------------------------------------------------------------------
# Read-only source loaders
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceArtefactSummary:
    """Hashed summary of one source artefact (read-only)."""

    path: Path
    sha256: str
    size_bytes: int


def hash_source_file(path: Path, *, label: str) -> SourceArtefactSummary:
    """Recompute SHA256 of *path*; raise :class:`FeatureIOError` if missing."""
    if not isinstance(path, Path):
        raise FeatureIOError(f"{label} must be a pathlib.Path")
    if not path.exists():
        raise FeatureIOError(f"{label} does not exist: {path}")
    sha, size = compute_file_sha256(path)
    return SourceArtefactSummary(path=path, sha256=sha, size_bytes=size)


def read_source_normalized_manifest(path: Path) -> tuple[dict[str, Any], str]:
    """Read and parse the source normalized manifest read-only.

    Returns ``(parsed_dict, sha256)``. Verifies that
    ``research_eligible`` is ``False`` and ``eligibility_gate_status``
    is ``"pending"`` per the Phase 4bb-E successor-state policy.
    """
    if not isinstance(path, Path):
        raise FeatureIOError("normalized manifest path must be a pathlib.Path")
    if not path.exists():
        raise FeatureIOError(
            f"normalized manifest does not exist: {path}"
        )
    raw = path.read_bytes()
    sha = compute_bytes_sha256(raw)
    parsed = json.loads(raw.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise FeatureIOError("source normalized manifest is not a JSON object")
    if parsed.get("research_eligible") is not False:
        raise FeatureIOError(
            "source normalized manifest research_eligible must be false"
        )
    if parsed.get("eligibility_gate_status") != "pending":
        raise FeatureIOError(
            "source normalized manifest eligibility_gate_status must be 'pending'"
        )
    return parsed, sha


def read_successor_state(path: Path) -> tuple[dict[str, Any], str]:
    """Read and parse the Phase 4bg-B successor-state JSON read-only.

    Returns ``(parsed_dict, sha256)``. Verifies that ``successor_stage``
    is ``"Stage-3"``, ``successor_research_eligible`` is ``True``, and
    ``successor_eligibility_gate_status`` is ``"pass"``. The original
    derived manifest remains immutable; this read does not affect it.
    """
    if not isinstance(path, Path):
        raise FeatureIOError("successor-state path must be a pathlib.Path")
    if not path.exists():
        raise FeatureIOError(
            f"successor-state JSON does not exist: {path}"
        )
    raw = path.read_bytes()
    sha = compute_bytes_sha256(raw)
    parsed = json.loads(raw.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise FeatureIOError("successor-state is not a JSON object")
    if parsed.get("successor_stage") != "Stage-3":
        raise FeatureIOError(
            "successor-state successor_stage must be 'Stage-3'"
        )
    if parsed.get("successor_research_eligible") is not True:
        raise FeatureIOError(
            "successor-state successor_research_eligible must be true"
        )
    if parsed.get("successor_eligibility_gate_status") != "pass":
        raise FeatureIOError(
            "successor-state successor_eligibility_gate_status must be 'pass'"
        )
    return parsed, sha


def read_normalized_parquet(path: Path) -> tuple[pa.Table, str, int]:
    """Read the source normalized parquet read-only via pyarrow.

    Returns ``(table, sha256, size_bytes)``. The on-disk file is hashed
    before reading so that pre-/post-run immutability is provable.
    """
    if not isinstance(path, Path):
        raise FeatureIOError("normalized parquet path must be a pathlib.Path")
    if not path.exists():
        raise FeatureIOError(f"normalized parquet does not exist: {path}")
    sha, size = compute_file_sha256(path)
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover - environment guard
        raise FeatureIOError("pyarrow is required for Phase 4bh") from exc
    table = pq.read_table(path)
    return table, sha, size


# ---------------------------------------------------------------------------
# Atomic writers
# ---------------------------------------------------------------------------


def atomic_write_feature_parquet(
    path: Path,
    table: pa.Table,
    *,
    refuse_overwrite: bool = True,
    compression: str = "zstd",
) -> tuple[str, int]:
    """Atomically write *table* to *path* as Parquet; return ``(sha256, size)``.

    Path discipline: must resolve under
    ``data/microstructure/features/``. Refuses to overwrite an existing
    finalised file when *refuse_overwrite* is ``True``.
    """
    if not isinstance(path, Path):
        raise FeatureIOError("path must be a pathlib.Path")
    assert_output_path_under_features(path, label="feature parquet output path")
    if refuse_overwrite and path.exists():
        raise FeatureIOError(f"refusing to overwrite existing file: {path}")
    if path.with_suffix(path.suffix + ".tmp").exists():
        raise FeatureIOError(
            f"stale .tmp companion exists: {path.with_suffix(path.suffix + '.tmp')}"
        )
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover - environment guard
        raise FeatureIOError(
            "pyarrow is required for Phase 4bh feature parquet output"
        ) from exc
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


def atomic_write_feature_manifest(
    path: Path,
    obj: Mapping[str, Any] | dict[str, Any],
    *,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Atomically write *obj* as JSON to *path*; return ``(sha256, size)``.

    Path discipline: must resolve under ``data/microstructure/manifests/``.
    """
    if not isinstance(path, Path):
        raise FeatureIOError("path must be a pathlib.Path")
    assert_manifest_output_path_under_manifests(
        path, label="feature manifest output path"
    )
    if refuse_overwrite and path.exists():
        raise FeatureIOError(f"refusing to overwrite existing file: {path}")
    if path.with_suffix(path.suffix + ".tmp").exists():
        raise FeatureIOError(
            f"stale .tmp companion exists: {path.with_suffix(path.suffix + '.tmp')}"
        )
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


def write_feature_sha256_sidecar(
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
        raise FeatureIOError("path must be a pathlib.Path")
    assert_path_under_data_microstructure(path, label="sidecar path")
    if refuse_overwrite and path.exists():
        raise FeatureIOError(f"refusing to overwrite existing file: {path}")
    if len(sha256_hex) != 64:
        raise FeatureIOError("sha256_hex must be 64 lowercase hex chars")
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
    "FEATURES_FAMILY_SUBDIR",
    "FEATURE_DATASET_FAMILY",
    "FeatureIOError",
    "SourceArtefactSummary",
    "assert_output_path_under_features",
    "atomic_write_feature_manifest",
    "atomic_write_feature_parquet",
    "derive_feature_manifest_output_path",
    "derive_feature_output_path",
    "hash_source_file",
    "read_normalized_parquet",
    "read_source_normalized_manifest",
    "read_successor_state",
    "resolve_default_manifests_root",
    "write_feature_sha256_sidecar",
]
