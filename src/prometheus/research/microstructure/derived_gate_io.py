"""I/O primitives for the Phase 4bf derived-family eligibility gate.

This module provides offline-only, read-only loaders plus a single
atomic JSON writer + paired SHA256 sidecar writer for the gate report.
It enforces strict path discipline: gate-report writes are only allowed
under ``data/microstructure/gate-reports/normalized/``. No network I/O,
no credentials, no `.env` reads, no MCP / Graphify hooks.

Phase 4bf-A §11 / §12 / §13 reference: see
``docs/00-meta/implementation-reports/
2026-05-07_phase-4bf-a_aggtrades-derived-family-eligibility-gate-design.md``.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Reuse the canonical Phase 4bb-C exception so the public package
# surface exposes exactly one ``GateIOError`` symbol.
from .eligibility_io import GateIOError as GateIOError

DATA_MICROSTRUCTURE_PARTS: tuple[str, ...] = ("data", "microstructure")
GATE_REPORT_PARTS: tuple[str, ...] = ("data", "microstructure", "gate-reports", "normalized")


@dataclass(frozen=True)
class DerivedSourceArtefactPaths:
    """Bundle of read-only source artefact paths used by the gate."""

    derived_manifest_path: Path
    derived_manifest_sidecar_path: Path
    normalized_parquet_path: Path
    normalized_parquet_sidecar_path: Path
    raw_manifest_path: Path
    raw_zip_path: Path
    raw_sidecar_path: Path
    acquisition_log_path: Path
    gate_report_path: Path


@dataclass(frozen=True)
class GateReportPaths:
    """Output paths for the gate report and paired SHA256 sidecar."""

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
    if not _path_starts_with(path, DATA_MICROSTRUCTURE_PARTS):
        raise GateIOError(
            f"{label} must resolve under data/microstructure/ (got {path})"
        )


def assert_gate_report_path_under_namespace(path: Path, *, label: str = "gate report path") -> None:
    """Reject any *path* that does not resolve under the normalized gate-report namespace."""
    if not _path_starts_with(path, GATE_REPORT_PARTS):
        raise GateIOError(
            f"{label} must resolve under data/microstructure/gate-reports/normalized/ (got {path})"
        )


def read_manifest_bytes(path: Path) -> bytes:
    """Return the raw bytes of *path* without parsing."""
    return path.read_bytes()


def parse_manifest_bytes(payload: bytes) -> dict[str, Any]:
    """Decode JSON manifest bytes into a dict, preserving key order."""
    obj = json.loads(payload.decode("utf-8"))
    if not isinstance(obj, dict):
        raise GateIOError("manifest JSON root must be a dict")
    return obj


def read_sidecar_first_64(path: Path) -> str:
    """Return the leading 64 hex chars of a SHA256 sidecar file."""
    text = path.read_text(encoding="utf-8").strip()
    return text[:64]


def derive_report_id(
    *,
    dataset_family: str,
    dataset_version: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
) -> str:
    """Build the canonical Phase 4bf report id."""
    short = code_commit_sha[:12]
    return f"{dataset_family}__{dataset_version}__{generated_at_unix_ms}__{short}"


def derive_report_paths(
    *,
    output_root: Path,
    dataset_family: str,
    dataset_version: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
) -> GateReportPaths:
    """Compute the canonical report path + sidecar path under the namespace."""
    assert_path_under_microstructure(output_root, label="output_root")
    report_id = derive_report_id(
        dataset_family=dataset_family,
        dataset_version=dataset_version,
        generated_at_unix_ms=generated_at_unix_ms,
        code_commit_sha=code_commit_sha,
    )
    report_path = (output_root / f"{report_id}.json").resolve()
    sidecar_path = report_path.with_suffix(".json.sha256")
    assert_gate_report_path_under_namespace(report_path, label="report path")
    assert_gate_report_path_under_namespace(sidecar_path, label="sidecar path")
    return GateReportPaths(report_path=report_path, sidecar_path=sidecar_path, report_id=report_id)


def atomic_write_json(
    path: Path,
    obj: Mapping[str, Any],
    *,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Atomically write *obj* as sorted-keys JSON to *path*.

    Returns ``(sha256_hex, size_bytes)``. The temporary file is created
    in the same directory and renamed via :func:`os.replace` for
    atomicity. When *refuse_overwrite* is ``True`` (the default), the
    write is rejected if the final path already exists.
    """
    if refuse_overwrite and path.exists():
        raise GateIOError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8")
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(payload)
            fh.flush()
            # Some platforms (e.g. tmpfs in CI) reject fsync; the
            # write-then-rename invariant is still preserved.
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        if refuse_overwrite and path.exists():
            raise GateIOError(f"refusing to overwrite existing file: {path}")
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
        raise GateIOError(f"refusing to overwrite existing sidecar: {sidecar_path}")
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    line = f"{sha256_hex}  {target_filename}\n"
    fd, tmp_name = tempfile.mkstemp(
        prefix=sidecar_path.name + ".", suffix=".tmp", dir=str(sidecar_path.parent)
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(line.encode("utf-8"))
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        if refuse_overwrite and sidecar_path.exists():
            raise GateIOError(f"refusing to overwrite existing sidecar: {sidecar_path}")
        os.replace(tmp_path, sidecar_path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()


def resolve_derived_source_artefact_paths(
    *,
    derived_manifest_path: Path,
    derived_manifest: Mapping[str, Any],
    raw_manifest_path: Path,
    raw_manifest: Mapping[str, Any],
) -> DerivedSourceArtefactPaths:
    """Resolve all source artefact paths used by the gate.

    The derived manifest's ``files[0].path`` is interpreted as relative
    to ``data/microstructure/`` (the Phase 4bd writer convention). The
    raw manifest's ``files[0].path`` is interpreted the same way. The
    Phase 4bb-D gate report path is reconstructed from the derived
    manifest's ``governance_labels.source_gate_report_id`` value.
    """
    files = derived_manifest.get("files") or []
    if not files:
        raise GateIOError("derived manifest has no files[] entries")
    parquet_relpath = files[0].get("path")
    if not parquet_relpath:
        raise GateIOError("derived manifest files[0].path is missing")
    microstructure_root = derived_manifest_path.parent.parent
    normalized_parquet_path = (microstructure_root / parquet_relpath).resolve()
    normalized_sidecar_path = Path(str(normalized_parquet_path) + ".sha256")
    derived_sidecar_path = Path(str(derived_manifest_path) + ".sha256")

    raw_files = raw_manifest.get("files") or []
    if not raw_files:
        raise GateIOError("raw manifest has no files[] entries")
    raw_relpath = raw_files[0].get("path")
    if not raw_relpath:
        raise GateIOError("raw manifest files[0].path is missing")
    raw_zip_path = (microstructure_root / raw_relpath).resolve()
    raw_sidecar_path = Path(str(raw_zip_path) + ".sha256")

    raw_manifest_basename = Path(raw_manifest_path).name
    acq_log_basename = raw_manifest_basename.replace(".json", "_acquisition_log.json")
    acq_log_path = (raw_manifest_path.parent / acq_log_basename).resolve()

    gov = derived_manifest.get("governance_labels") or {}
    gate_report_id = gov.get("source_gate_report_id")
    if not gate_report_id:
        raise GateIOError(
            "derived manifest governance_labels.source_gate_report_id is missing"
        )
    gate_report_path = (
        microstructure_root
        / "gate-reports"
        / "gate-reports"
        / f"{gate_report_id}.json"
    ).resolve()

    return DerivedSourceArtefactPaths(
        derived_manifest_path=derived_manifest_path,
        derived_manifest_sidecar_path=derived_sidecar_path,
        normalized_parquet_path=normalized_parquet_path,
        normalized_parquet_sidecar_path=normalized_sidecar_path,
        raw_manifest_path=raw_manifest_path,
        raw_zip_path=raw_zip_path,
        raw_sidecar_path=raw_sidecar_path,
        acquisition_log_path=acq_log_path,
        gate_report_path=gate_report_path,
    )


@dataclass(frozen=True)
class LoadedArtefactBundle:
    """Pre-loaded SHAs and bytes used by the check functions."""

    derived_manifest_bytes: bytes
    derived_manifest_sha: str
    derived_manifest: dict[str, Any]
    derived_sidecar_first_64: str
    normalized_parquet_sha: str
    normalized_sidecar_first_64: str
    raw_manifest_bytes: bytes
    raw_manifest_sha: str
    raw_manifest: dict[str, Any]
    raw_zip_sha: str
    raw_sidecar_sha: str
    raw_sidecar_first_64: str
    acquisition_log_sha: str
    gate_report_sha: str
    measured: dict[str, Any] = field(default_factory=dict)
