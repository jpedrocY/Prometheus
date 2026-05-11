"""Phase 4bj-E label-family eligibility-gate I/O primitives.

This module provides offline-only, read-only loaders plus a single
atomic JSON writer + paired SHA256 sidecar writer for the Phase 4bj-E
label-family gate report. It enforces strict path discipline:
gate-report writes are only allowed under
``data/microstructure/gate-reports/labels/``. No network I/O,
no credentials, no ``.env`` reads, no MCP / Graphify hooks.

Phase 4bj-E reference: ``Phase 4bj-E — Label-Family Eligibility Gate
Design + Implementation + Execution``. The gate verifies the Phase
4bj-C local Stage-0 label artefacts (label parquet, label parquet
sidecar, label manifest, label manifest sidecar) against the Phase
4bj-B v001 contract; it never mutates the label parquet, label
manifest, or any source artefact, and it never flips
``research_eligible``.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DATA_MICROSTRUCTURE_PARTS: tuple[str, ...] = ("data", "microstructure")
LABEL_GATE_REPORT_PARTS: tuple[str, ...] = (
    "data",
    "microstructure",
    "gate-reports",
    "labels",
)


class LabelGateIOError(RuntimeError):
    """Raised when a Phase 4bj-E label-gate I/O operation fails closed."""


@dataclass(frozen=True)
class LabelGateReportPaths:
    """Output paths for the label-gate report and paired SHA256 sidecar."""

    report_path: Path
    sidecar_path: Path
    report_id: str


def compute_file_sha256(path: Path, *, chunk_size: int = 1 << 20) -> str:
    """Return the hex SHA-256 digest of *path*."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            buf = fh.read(chunk_size)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def compute_bytes_sha256(payload: bytes) -> str:
    """Return the hex SHA-256 digest of *payload*."""
    return hashlib.sha256(payload).hexdigest()


def _resolve_parts(path: Path) -> tuple[str, ...]:
    return tuple(part for part in path.resolve().parts)


def _path_starts_with(path: Path, expected_tail: tuple[str, ...]) -> bool:
    parts = _resolve_parts(path)
    for i in range(len(parts) - len(expected_tail) + 1):
        if parts[i : i + len(expected_tail)] == expected_tail:
            return True
    return False


def assert_path_under_microstructure(path: Path, *, label: str = "path") -> None:
    """Reject any *path* that does not resolve under ``data/microstructure/``."""
    if not isinstance(path, Path):
        raise LabelGateIOError(f"{label} must be a pathlib.Path")
    if not _path_starts_with(path, DATA_MICROSTRUCTURE_PARTS):
        raise LabelGateIOError(
            f"{label} must resolve under data/microstructure/ (got {path!s})"
        )


def assert_label_gate_report_path(path: Path, *, label: str = "report path") -> None:
    """Reject any *path* not under ``data/microstructure/gate-reports/labels/``."""
    if not isinstance(path, Path):
        raise LabelGateIOError(f"{label} must be a pathlib.Path")
    if not _path_starts_with(path, LABEL_GATE_REPORT_PARTS):
        raise LabelGateIOError(
            f"{label} must resolve under "
            f"data/microstructure/gate-reports/labels/ (got {path!s})"
        )


def read_manifest_bytes(path: Path) -> bytes:
    """Return the raw bytes of *path* without parsing."""
    if not isinstance(path, Path):
        raise LabelGateIOError("manifest path must be a pathlib.Path")
    if not path.exists():
        raise LabelGateIOError(f"manifest does not exist: {path!s}")
    return path.read_bytes()


def parse_manifest_bytes(payload: bytes) -> dict[str, Any]:
    """Decode JSON manifest bytes into a dict, preserving key order."""
    obj = json.loads(payload.decode("utf-8"))
    if not isinstance(obj, dict):
        raise LabelGateIOError("manifest JSON root must be a dict")
    return obj


def read_sidecar_first_64(path: Path) -> str:
    """Return the leading 64 hex chars of a SHA256 sidecar file."""
    if not isinstance(path, Path):
        raise LabelGateIOError("sidecar path must be a pathlib.Path")
    if not path.exists():
        raise LabelGateIOError(f"sidecar does not exist: {path!s}")
    text = path.read_text(encoding="ascii").strip()
    return text[:64]


def derive_label_gate_report_id(
    *,
    dataset_family: str,
    dataset_version: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
) -> str:
    """Build the canonical Phase 4bj-E report id."""
    short = code_commit_sha[:12]
    return (
        f"{dataset_family}__{dataset_version}__phase-4bj-e__"
        f"{generated_at_unix_ms}__{short}"
    )


def derive_label_gate_report_paths(
    *,
    output_root: Path,
    dataset_family: str,
    dataset_version: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
) -> LabelGateReportPaths:
    """Compute the canonical report path + sidecar path under the namespace."""
    if not isinstance(output_root, Path):
        raise LabelGateIOError("output_root must be a pathlib.Path")
    assert_path_under_microstructure(output_root, label="output_root")
    report_id = derive_label_gate_report_id(
        dataset_family=dataset_family,
        dataset_version=dataset_version,
        generated_at_unix_ms=generated_at_unix_ms,
        code_commit_sha=code_commit_sha,
    )
    report_path = (output_root / f"{report_id}.json").resolve()
    sidecar_path = report_path.with_suffix(".json.sha256")
    assert_label_gate_report_path(report_path, label="report path")
    assert_label_gate_report_path(sidecar_path, label="sidecar path")
    return LabelGateReportPaths(
        report_path=report_path,
        sidecar_path=sidecar_path,
        report_id=report_id,
    )


def atomic_write_json(
    path: Path,
    obj: Mapping[str, Any],
    *,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Atomically write *obj* as sorted-keys JSON to *path*.

    Returns ``(sha256_hex, size_bytes)``.
    """
    if refuse_overwrite and path.exists():
        raise LabelGateIOError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False).encode(
        "utf-8"
    )
    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=str(path.parent)
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(payload)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        if refuse_overwrite and path.exists():
            raise LabelGateIOError(f"refusing to overwrite existing file: {path}")
        os.replace(tmp_path, path)
        sha = compute_bytes_sha256(payload)
        return sha, len(payload)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()


def write_sha256_sidecar(
    sidecar_path: Path,
    *,
    target_filename: str,
    sha256_hex: str,
    refuse_overwrite: bool = True,
) -> None:
    """Write a paired ``<file>.sha256`` sidecar containing ``<sha>  <name>``."""
    if refuse_overwrite and sidecar_path.exists():
        raise LabelGateIOError(
            f"refusing to overwrite existing sidecar: {sidecar_path}"
        )
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    line = f"{sha256_hex}  {target_filename}\n"
    fd, tmp_name = tempfile.mkstemp(
        prefix=sidecar_path.name + ".",
        suffix=".tmp",
        dir=str(sidecar_path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(line.encode("utf-8"))
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        if refuse_overwrite and sidecar_path.exists():
            raise LabelGateIOError(
                f"refusing to overwrite existing sidecar: {sidecar_path}"
            )
        os.replace(tmp_path, sidecar_path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()
