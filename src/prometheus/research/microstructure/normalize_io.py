"""Phase 4bd offline aggTrades normalization I/O helpers.

This module provides:

- read-only loaders that share the Phase 4bb-C eligibility-gate I/O
  surface for source raw artefacts;
- output-path discipline for normalized derived artefacts under
  ``data/microstructure/normalized/`` only;
- atomic write helpers for Parquet and JSON outputs;
- SHA256 helpers shared with the rest of the microstructure stack.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read ``.env`` / ``.mcp.json``, or import any networking library;
- does NOT mutate any source raw artefact (manifest, raw zip, sidecar,
  acquisition log) or the existing Phase 4bb-D gate report;
- decompresses the raw zip in memory only and reads it once;
- writes only under the gitignored ``data/microstructure/normalized/``
  partition tree (for Parquet) or
  ``data/microstructure/manifests/`` (for the derived manifest), and
  refuses to overwrite an existing finalised file;
- never computes features, labels, signals, returns, alpha, edge, or
  any execution-quality / order-flow proxy.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import tempfile
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - type-only
    import pyarrow as pa

NORMALIZED_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
"""Constant derived family name for Phase 4bd."""

NORMALIZED_FAMILY_SUBDIR = "normalized"
"""Subdirectory under ``data/microstructure/`` reserved for normalized output."""

MANIFESTS_SUBDIR = "manifests"
"""Subdirectory under ``data/microstructure/`` for manifest files."""

DEFAULT_DATA_MICROSTRUCTURE_PARTS: tuple[str, ...] = ("data", "microstructure")
"""Path parts identifying the gitignored microstructure namespace."""


class NormalizationIOError(RuntimeError):
    """Raised when a Phase 4bd normalizer I/O operation fails closed."""


@dataclass(frozen=True)
class SourceArtefactPaths:
    """Resolved on-disk paths for the four read-only source artefacts."""

    manifest_path: Path
    raw_zip_path: Path
    sidecar_path: Path
    acquisition_log_path: Path


def _resolve_path_parts_under(path: Path, parts: tuple[str, ...]) -> bool:
    """Return ``True`` iff *path*'s resolved-or-best-effort parts contain *parts*."""
    try:
        resolved = path.resolve(strict=False)
    except OSError:
        resolved = path
    candidates = (resolved.parts, path.parts)
    needle = tuple(parts)
    for candidate in candidates:
        for i in range(len(candidate) - len(needle) + 1):
            if tuple(candidate[i : i + len(needle)]) == needle:
                return True
    return False


def assert_path_under_microstructure(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/``."""
    if not isinstance(path, Path):
        raise NormalizationIOError(f"{label} must be a pathlib.Path")
    if not _resolve_path_parts_under(path, DEFAULT_DATA_MICROSTRUCTURE_PARTS):
        raise NormalizationIOError(
            f"{label} must resolve under data/microstructure/ (got {path!s})"
        )


def assert_output_path_under_normalized(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/normalized/``."""
    assert_path_under_microstructure(path, label=label)
    if not _resolve_path_parts_under(
        path, DEFAULT_DATA_MICROSTRUCTURE_PARTS + (NORMALIZED_FAMILY_SUBDIR,)
    ):
        raise NormalizationIOError(
            f"{label} must resolve under data/microstructure/normalized/ (got {path!s})"
        )


def assert_manifest_path_under_manifests(path: Path, *, label: str) -> None:
    """Fail closed if *path* is not under ``data/microstructure/manifests/``."""
    assert_path_under_microstructure(path, label=label)
    if not _resolve_path_parts_under(
        path, DEFAULT_DATA_MICROSTRUCTURE_PARTS + (MANIFESTS_SUBDIR,)
    ):
        raise NormalizationIOError(
            f"{label} must resolve under data/microstructure/manifests/ (got {path!s})"
        )


def compute_file_sha256(path: Path) -> tuple[str, int]:
    """Recompute SHA256 of *path*; return ``(hex_digest, size_bytes)``."""
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def compute_bytes_sha256(data: bytes) -> str:
    """Return SHA256 hex digest of in-memory bytes."""
    return hashlib.sha256(data).hexdigest()


def read_manifest_bytes(manifest_path: Path) -> tuple[bytes, str]:
    """Return ``(raw_bytes, sha256)`` for the source manifest."""
    if not isinstance(manifest_path, Path):
        raise NormalizationIOError("manifest_path must be a pathlib.Path")
    if not manifest_path.exists():
        raise NormalizationIOError(f"manifest_path does not exist: {manifest_path}")
    raw = manifest_path.read_bytes()
    return raw, compute_bytes_sha256(raw)


def parse_manifest_bytes(raw: bytes) -> dict[str, Any]:
    """Parse manifest bytes as a JSON object."""
    parsed = json.loads(raw.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise NormalizationIOError("source manifest is not a JSON object")
    return parsed


def read_sidecar(sidecar_path: Path) -> tuple[str, str, str]:
    """Return ``(raw_text, first_64_hex, sidecar_sha)`` for a `.sha256` sidecar."""
    if not sidecar_path.exists():
        raise NormalizationIOError(f"sidecar_path does not exist: {sidecar_path}")
    raw = sidecar_path.read_bytes()
    sha = compute_bytes_sha256(raw)
    text = raw.decode("utf-8").strip()
    first_field = text.split()[0] if text else ""
    first_64 = first_field[:64] if len(first_field) >= 64 else first_field
    return text, first_64, sha


def read_acquisition_log(log_path: Path) -> tuple[dict[str, Any], str]:
    """Return ``(parsed_dict, sha256)`` for the acquisition log JSON."""
    if not log_path.exists():
        raise NormalizationIOError(f"acquisition_log_path does not exist: {log_path}")
    raw = log_path.read_bytes()
    sha = compute_bytes_sha256(raw)
    parsed = json.loads(raw.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise NormalizationIOError("acquisition log is not a JSON object")
    return parsed, sha


def resolve_source_artefact_paths(manifest_path: Path) -> SourceArtefactPaths:
    """Resolve the four source artefact paths from the manifest path."""
    if not isinstance(manifest_path, Path):
        raise NormalizationIOError("manifest_path must be a pathlib.Path")
    assert_manifest_path_under_manifests(manifest_path, label="manifest_path")
    if not manifest_path.exists():
        raise NormalizationIOError(f"manifest_path does not exist: {manifest_path}")
    raw, _ = read_manifest_bytes(manifest_path)
    parsed = parse_manifest_bytes(raw)
    files = parsed.get("files")
    if not isinstance(files, list) or not files:
        raise NormalizationIOError("source manifest has no files entry")
    first = files[0]
    if not isinstance(first, Mapping) or "path" not in first:
        raise NormalizationIOError("source manifest files[0] missing 'path'")
    relative_zip_path = Path(str(first["path"]))
    microstructure_root = _ascend_to_microstructure_root(manifest_path)
    raw_zip_path = microstructure_root / relative_zip_path
    sidecar_path = raw_zip_path.with_suffix(raw_zip_path.suffix + ".sha256")
    acquisition_log_path = manifest_path.with_name(
        manifest_path.stem + "_acquisition_log.json"
    )
    return SourceArtefactPaths(
        manifest_path=manifest_path,
        raw_zip_path=raw_zip_path,
        sidecar_path=sidecar_path,
        acquisition_log_path=acquisition_log_path,
    )


def _ascend_to_microstructure_root(start: Path) -> Path:
    """Return the directory ``data/microstructure`` ancestor of *start*."""
    current = start.resolve(strict=False)
    while current.parent != current:
        if current.parts[-2:] == DEFAULT_DATA_MICROSTRUCTURE_PARTS:
            return current
        current = current.parent
    raise NormalizationIOError(
        f"could not locate data/microstructure ancestor of {start!s}"
    )


def open_zip_single_csv_in_memory(zip_path: Path) -> tuple[str, str, int]:
    """Read the single CSV member of *zip_path* in memory.

    Returns ``(member_name, csv_text, uncompressed_size)``. Raises
    :class:`NormalizationIOError` if the archive does not contain
    exactly one CSV member or if decompression fails.
    """
    try:
        with zipfile.ZipFile(zip_path) as zf:
            members = zf.namelist()
            if len(members) != 1:
                raise NormalizationIOError(
                    f"zip archive must contain exactly one CSV member; "
                    f"got {len(members)}"
                )
            member = members[0]
            info = zf.getinfo(member)
            with zf.open(member) as raw:
                data = raw.read()
            return member, data.decode("utf-8"), int(info.file_size)
    except zipfile.BadZipFile as exc:
        raise NormalizationIOError(f"zip decompression failed: {exc}") from exc


def atomic_write_parquet(
    path: Path,
    table: pa.Table,
    *,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Atomically write *table* to *path* as Parquet; return ``(sha256, size)``.

    Uses ``tempfile.mkstemp`` next to *path* and ``os.replace`` to swap.
    If *refuse_overwrite* and the final path exists, raises.
    """
    import pyarrow.parquet as pq

    if not isinstance(path, Path):
        raise NormalizationIOError("path must be a pathlib.Path")
    assert_output_path_under_normalized(path, label="parquet output path")
    if refuse_overwrite and path.exists():
        raise NormalizationIOError(f"refusing to overwrite existing file: {path}")
    if path.with_suffix(path.suffix + ".tmp").exists():
        raise NormalizationIOError(
            f"stale .tmp companion exists: {path.with_suffix(path.suffix + '.tmp')}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_str = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=path.parent,
    )
    tmp_path = Path(tmp_str)
    try:
        os.close(fd)
        pq.write_table(table, tmp_path, compression="zstd")
        with tmp_path.open("rb") as f, contextlib.suppress(OSError):
            os.fsync(f.fileno())
        sha, size = compute_file_sha256(tmp_path)
        os.replace(tmp_path, path)
        return sha, size
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise


def atomic_write_json(
    path: Path,
    obj: Mapping[str, Any] | dict[str, Any],
    *,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Atomically write *obj* as JSON to *path*; return ``(sha256, size)``.

    Used for the derived manifest under ``data/microstructure/manifests/``.
    """
    if not isinstance(path, Path):
        raise NormalizationIOError("path must be a pathlib.Path")
    assert_manifest_path_under_manifests(path, label="manifest output path")
    if refuse_overwrite and path.exists():
        raise NormalizationIOError(f"refusing to overwrite existing file: {path}")
    if path.with_suffix(path.suffix + ".tmp").exists():
        raise NormalizationIOError(
            f"stale .tmp companion exists: {path.with_suffix(path.suffix + '.tmp')}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(dict(obj), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
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


def write_sha256_sidecar(
    path: Path,
    *,
    target_filename: str,
    sha256_hex: str,
    refuse_overwrite: bool = True,
) -> tuple[str, int]:
    """Write a paired ``.sha256`` sidecar at *path*; return ``(sha256, size)``.

    Format: ``<sha256_hex>  <target_filename>\n`` (two-space separator,
    matching common ``sha256sum``-style sidecars).
    """
    if not isinstance(path, Path):
        raise NormalizationIOError("path must be a pathlib.Path")
    assert_path_under_microstructure(path, label="sidecar path")
    if refuse_overwrite and path.exists():
        raise NormalizationIOError(f"refusing to overwrite existing file: {path}")
    if len(sha256_hex) != 64:
        raise NormalizationIOError("sha256_hex must be 64 lowercase hex chars")
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


def derive_normalized_output_path(
    *,
    output_root: Path,
    symbol: str,
    utc_date: str,
) -> Path:
    """Compute the normalized Parquet path for ``(symbol, utc_date)``.

    Layout (relative to *output_root*):
    ``microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet``.
    """
    if not isinstance(output_root, Path):
        raise NormalizationIOError("output_root must be a pathlib.Path")
    assert_path_under_microstructure(output_root, label="output_root")
    if not symbol or not symbol.isalnum() or symbol != symbol.upper():
        raise NormalizationIOError("symbol must be uppercase alphanumeric")
    parts = utc_date.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise NormalizationIOError(
            f"utc_date must be YYYY-MM-DD; got {utc_date!r}"
        )
    yyyy, mm, _dd = parts
    return (
        output_root
        / NORMALIZED_DATASET_FAMILY
        / symbol
        / yyyy
        / mm
        / f"{symbol}-aggTrades-{utc_date}.parquet"
    )


def derive_manifest_output_path(*, manifests_root: Path) -> Path:
    """Compute the derived manifest path."""
    if not isinstance(manifests_root, Path):
        raise NormalizationIOError("manifests_root must be a pathlib.Path")
    assert_manifest_path_under_manifests(manifests_root, label="manifests_root")
    return manifests_root / f"{NORMALIZED_DATASET_FAMILY}__v001.json"


def relative_to_microstructure_root(path: Path) -> str:
    """Return the path relative to the ``data/microstructure`` root, as a string."""
    root = _ascend_to_microstructure_root(path)
    try:
        rel = path.resolve(strict=False).relative_to(root)
    except ValueError:
        rel = path.relative_to(root) if str(path).startswith(str(root)) else path
    return str(rel).replace(os.sep, "/")


__all__ = [
    "MANIFESTS_SUBDIR",
    "NORMALIZED_DATASET_FAMILY",
    "NORMALIZED_FAMILY_SUBDIR",
    "NormalizationIOError",
    "SourceArtefactPaths",
    "assert_manifest_path_under_manifests",
    "assert_output_path_under_normalized",
    "assert_path_under_microstructure",
    "atomic_write_json",
    "atomic_write_parquet",
    "compute_bytes_sha256",
    "compute_file_sha256",
    "derive_manifest_output_path",
    "derive_normalized_output_path",
    "open_zip_single_csv_in_memory",
    "parse_manifest_bytes",
    "read_acquisition_log",
    "read_manifest_bytes",
    "read_sidecar",
    "relative_to_microstructure_root",
    "resolve_source_artefact_paths",
    "write_sha256_sidecar",
]


def _read_io_text(text: str) -> io.StringIO:  # pragma: no cover - shim used by tests
    """Internal helper: wrap text in a StringIO for csv readers."""
    return io.StringIO(text)
