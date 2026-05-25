"""Phase 4bm-Q multi-day v002 label-family eligibility gate I/O helpers.

Provides read-only loaders for the Phase 4bm-O v002 label artefacts plus
path discipline + atomic JSON / sidecar writers under
``data/microstructure/gate-reports/labels/`` for the gitignored gate
report output. Mirrors the Phase 4bm-J (v002 feature-family gate) IO
contract verbatim, adapted to labels.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT mutate any source artefact (label parquet, label manifest,
  label sidecars, feature parquets, feature manifest, derived manifest,
  raw manifest, gate reports, successor-state JSONs);
- writes only under ``data/microstructure/gate-reports/labels/`` for
  the new gate report JSON + paired Phase 4bb-F sidecar;
- refuses to overwrite an existing finalised output.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .normalize_io import (
    DEFAULT_DATA_MICROSTRUCTURE_PARTS,
    _resolve_path_parts_under,
)

LABEL_GATE_REPORTS_SUBDIR_PARTS = ("data", "microstructure", "gate-reports", "labels")


class MultidayLabelGateIOError(RuntimeError):
    """Raised when a Phase 4bm-Q IO operation fails closed."""


def assert_path_under_microstructure(path: Path, *, label: str) -> None:
    if not isinstance(path, Path):
        raise MultidayLabelGateIOError(f"{label} must be a pathlib.Path")
    if not _resolve_path_parts_under(path, DEFAULT_DATA_MICROSTRUCTURE_PARTS):
        raise MultidayLabelGateIOError(
            f"{label} must resolve under data/microstructure/ (got {path!s})"
        )


def assert_path_under_label_gate_reports(path: Path, *, label: str) -> None:
    assert_path_under_microstructure(path, label=label)
    if not _resolve_path_parts_under(path, LABEL_GATE_REPORTS_SUBDIR_PARTS):
        raise MultidayLabelGateIOError(
            f"{label} must resolve under data/microstructure/gate-reports/labels/ "
            f"(got {path!s})"
        )


def compute_file_sha256(path: Path) -> tuple[str, int]:
    """Stream a file's SHA256 and return ``(sha256_lowercase_hex, size_bytes)``."""
    if not isinstance(path, Path):
        raise MultidayLabelGateIOError("path must be a pathlib.Path")
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            size += len(chunk)
            h.update(chunk)
    return h.hexdigest(), size


def compute_bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json_file(path: Path) -> tuple[dict[str, Any], str, int]:
    """Read a JSON file read-only; return ``(parsed_dict, sha256, size_bytes)``."""
    if not isinstance(path, Path):
        raise MultidayLabelGateIOError("path must be a pathlib.Path")
    if not path.exists():
        raise MultidayLabelGateIOError(f"file does not exist: {path}")
    raw = path.read_bytes()
    sha = compute_bytes_sha256(raw)
    size = len(raw)
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise MultidayLabelGateIOError(
            f"file {path} is not valid JSON: {exc}"
        ) from exc
    if not isinstance(parsed, dict):
        raise MultidayLabelGateIOError(f"file {path} top-level JSON must be an object")
    return parsed, sha, size


def derive_gate_report_id(
    *,
    dataset_family: str,
    dataset_version: str,
    phase_id: str,
    unix_ms: int,
    short_commit: str,
) -> str:
    """Return ``<family>__<version>__phase-<id>__<unix_ms>__<short_commit>``."""
    if not dataset_family or not dataset_version or not phase_id:
        raise MultidayLabelGateIOError(
            "dataset_family / dataset_version / phase_id required"
        )
    if not isinstance(unix_ms, int) or unix_ms <= 0:
        raise MultidayLabelGateIOError("unix_ms must be positive int")
    if not short_commit or len(short_commit) < 8:
        raise MultidayLabelGateIOError("short_commit must be at least 8 hex chars")
    return (
        f"{dataset_family}__{dataset_version}__phase-{phase_id}__"
        f"{unix_ms}__{short_commit}"
    )


def derive_gate_report_paths(
    *,
    output_root: Path,
    report_id: str,
) -> tuple[Path, Path]:
    """Return ``(report_json_path, sidecar_path)`` under the labels gate-report root."""
    if not isinstance(output_root, Path):
        raise MultidayLabelGateIOError("output_root must be Path")
    assert_path_under_microstructure(output_root, label="output_root")
    if "gate-reports" not in output_root.parts:
        raise MultidayLabelGateIOError(
            "output_root must contain a 'gate-reports' segment"
        )
    if "labels" not in output_root.parts:
        raise MultidayLabelGateIOError(
            "output_root must contain a 'labels' segment for Phase 4bm-Q"
        )
    json_path = output_root / f"{report_id}.json"
    sidecar_path = output_root / f"{report_id}.json.sha256"
    return json_path, sidecar_path


def compose_canonical_sidecar_body(*, sha256_hex: str, basename: str) -> bytes:
    """Phase 4bb-F canonical sidecar body: ``<sha><two ASCII spaces><basename><LF>``."""
    if (
        not isinstance(sha256_hex, str)
        or len(sha256_hex) != 64
        or sha256_hex.lower() != sha256_hex
    ):
        raise MultidayLabelGateIOError("sha256_hex must be 64-char lowercase hex")
    if not isinstance(basename, str) or not basename or "\n" in basename:
        raise MultidayLabelGateIOError("basename must be a non-empty single-line string")
    return f"{sha256_hex}  {basename}\n".encode("ascii")


def atomic_write_json(
    path: Path,
    obj: Mapping[str, Any],
    *,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Atomically write *obj* as canonical sort-keys JSON; return ``(sha256, size)``."""
    if not isinstance(path, Path):
        raise MultidayLabelGateIOError("path must be Path")
    assert_path_under_label_gate_reports(path, label="gate report output")
    if refuse_overwrite and path.exists():
        raise MultidayLabelGateIOError(f"refusing to overwrite existing file: {path}")
    if path.with_suffix(path.suffix + ".tmp").exists():
        raise MultidayLabelGateIOError(
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


def atomic_write_sidecar(
    path: Path,
    *,
    target_basename: str,
    sha256_hex: str,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Write canonical Phase 4bb-F sidecar atomically; return ``(sha256, size)``."""
    if not isinstance(path, Path):
        raise MultidayLabelGateIOError("path must be Path")
    assert_path_under_microstructure(path, label="sidecar path")
    if refuse_overwrite and path.exists():
        raise MultidayLabelGateIOError(f"refusing to overwrite existing file: {path}")
    payload = compose_canonical_sidecar_body(
        sha256_hex=sha256_hex, basename=target_basename
    )
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
    "LABEL_GATE_REPORTS_SUBDIR_PARTS",
    "MultidayLabelGateIOError",
    "assert_path_under_label_gate_reports",
    "assert_path_under_microstructure",
    "atomic_write_json",
    "atomic_write_sidecar",
    "compose_canonical_sidecar_body",
    "compute_bytes_sha256",
    "compute_file_sha256",
    "derive_gate_report_id",
    "derive_gate_report_paths",
    "read_json_file",
]
