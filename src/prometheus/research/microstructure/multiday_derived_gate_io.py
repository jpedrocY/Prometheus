"""I/O primitives for the Phase 4bm-D multi-day derived-family gate.

This module mirrors :mod:`derived_gate_io` (Phase 4bf) but is adapted
to the multi-day v002 manifest shape produced by Phase 4bm-B:

* the derived manifest has a flat 90-entry ``per_file_inventory``
  instead of a single ``files[0]`` reference,
* governance artefact paths (raw manifest, raw acquisition log,
  Phase 4bl-D-R raw gate report, Phase 4bl-E raw successor-state) are
  carried verbatim as full ``data/microstructure/...`` paths under
  top-level manifest keys (``source_manifest_path`` etc.) rather than
  reconstructed from a short id,
* per-file ``local_parquet_path`` / ``local_sidecar_path`` /
  ``source_zip_path`` are relative to the ``data/`` root (they begin
  with ``microstructure/...``), so resolving an absolute on-disk path
  requires prepending exactly ``Path("data")`` once.

The module is read-only on data: it never modifies any manifest,
parquet, sidecar, raw zip, governance artefact, or prior gate
report. The only writes it performs are the gate report JSON and
its paired ``.sha256`` sidecar under
``data/microstructure/gate-reports/normalized/``.

No network I/O, no credentials, no ``.env`` reads, no MCP / Graphify
hooks. The static no-network scan in
``test_multiday_derived_gate_no_network.py`` enforces these
boundaries.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Reuse the canonical Phase 4bb-C exception so the public package
# surface exposes exactly one ``GateIOError`` symbol.
from .eligibility_io import GateIOError as GateIOError

DATA_MICROSTRUCTURE_PARTS: tuple[str, ...] = ("data", "microstructure")
GATE_REPORT_PARTS: tuple[str, ...] = (
    "data",
    "microstructure",
    "gate-reports",
    "normalized",
)

# Phase 4bm-D filename convention follows Phase 4bb-F canonical form
# with the explicit ``phase-4bm-d`` segment between dataset version
# and unix-ms timestamp.
PHASE_4BM_D_ID_SEGMENT: str = "phase-4bm-d"


@dataclass(frozen=True)
class MultidayPerFileArtefactPaths:
    """Per-day Parquet + sidecar + source-zip paths plus expected SHAs.

    The expected SHAs come from the ``per_file_inventory`` entry and
    are checked by the gate checks. The ``source_zip_path`` is the
    upstream raw zip preserved by Phase 4bl-C / Phase 4bl-D-R and is
    re-hashed by the gate to confirm that Phase 4bm-B normalization
    did not mutate it (it is not opened for read by the gate beyond
    that hash).
    """

    date: str
    symbol: str
    parquet_path: Path
    parquet_sidecar_path: Path
    source_zip_path: Path
    expected_parquet_sha: str
    expected_parquet_size: int
    expected_sidecar_sha: str
    expected_sidecar_size: int
    expected_source_zip_sha: str
    expected_event_count: int
    expected_first_transact_time_ms: int
    expected_last_transact_time_ms: int
    expected_min_agg_trade_id: int
    expected_max_agg_trade_id: int


@dataclass(frozen=True)
class MultidayDerivedSourceArtefactPaths:
    """Bundle of read-only source artefact paths used by the multi-day gate."""

    derived_manifest_path: Path
    derived_manifest_sidecar_path: Path
    raw_manifest_path: Path
    raw_manifest_sidecar_path: Path
    acquisition_log_path: Path
    acquisition_log_sidecar_path: Path
    gate_report_path: Path
    gate_report_sidecar_path: Path
    successor_state_path: Path
    successor_state_sidecar_path: Path
    per_file: tuple[MultidayPerFileArtefactPaths, ...]


@dataclass(frozen=True)
class MultidayGateReportPaths:
    """Output paths for the multi-day gate report and paired SHA256 sidecar."""

    report_path: Path
    sidecar_path: Path
    report_id: str


def compute_file_sha256(path: Path, *, chunk_size: int = 1 << 20) -> str:
    """Return the hex SHA-256 digest of *path* via 1 MiB streaming reads."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            buf = fh.read(chunk_size)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def compute_file_size(path: Path) -> int:
    """Return the size of *path* in bytes via ``os.stat``."""
    return path.stat().st_size


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


def assert_gate_report_path_under_namespace(
    path: Path, *, label: str = "gate report path"
) -> None:
    """Reject any *path* that does not resolve under the gate-report namespace."""
    if not _path_starts_with(path, GATE_REPORT_PARTS):
        raise GateIOError(
            f"{label} must resolve under data/microstructure/gate-reports/normalized/ (got {path})"
        )


def read_manifest_bytes(path: Path) -> bytes:
    """Return the raw bytes of *path* without parsing."""
    return path.read_bytes()


def parse_manifest_bytes(payload: bytes) -> dict[str, Any]:
    """Decode JSON manifest bytes into a dict; reject non-dict roots."""
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
    """Build the canonical Phase 4bm-D report id.

    Format::

        <dataset_family>__<dataset_version>__phase-4bm-d__<unix_ms>__<short>

    where ``short`` is the first 12 characters of ``code_commit_sha``.
    This matches the Phase 4bb-F canonical filename convention and
    mirrors the explicit ``phase-<id>`` segment used by Phase 4bl-D-R
    and Phase 4bj-E gate reports.
    """
    short = code_commit_sha[:12]
    return (
        f"{dataset_family}__{dataset_version}__"
        f"{PHASE_4BM_D_ID_SEGMENT}__{generated_at_unix_ms}__{short}"
    )


def derive_report_paths(
    *,
    output_root: Path,
    dataset_family: str,
    dataset_version: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
) -> MultidayGateReportPaths:
    """Compute the canonical multi-day report path + sidecar path."""
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
    return MultidayGateReportPaths(
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

    Returns ``(sha256_hex, size_bytes)``. The temporary file is
    created in the same directory and renamed via :func:`os.replace`
    for atomicity. When *refuse_overwrite* is ``True`` (the default),
    the write is rejected if the final path already exists.
    """
    if refuse_overwrite and path.exists():
        raise GateIOError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        obj, sort_keys=True, indent=2, ensure_ascii=False
    ).encode("utf-8")
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
    """Write a paired ``<file>.sha256`` sidecar in Phase 4bb-F format.

    Body format: ``<sha256_lowercase_hex>  <basename>\\n`` (two ASCII
    spaces, single trailing LF, no CRLF, no BOM).
    """
    if refuse_overwrite and sidecar_path.exists():
        raise GateIOError(
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
            raise GateIOError(
                f"refusing to overwrite existing sidecar: {sidecar_path}"
            )
        os.replace(tmp_path, sidecar_path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()


def _require_str(d: Mapping[str, Any], key: str, *, where: str) -> str:
    """Return ``d[key]`` as a non-empty string or raise."""
    value = d.get(key)
    if not isinstance(value, str) or not value:
        raise GateIOError(f"{where}: missing or non-string field '{key}'")
    return value


def _require_int(d: Mapping[str, Any], key: str, *, where: str) -> int:
    """Return ``d[key]`` as an int or raise."""
    value = d.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise GateIOError(f"{where}: missing or non-int field '{key}'")
    return value


def _resolve_data_relative(rel: str) -> Path:
    """Prepend ``data/`` to a manifest-relative path that begins with ``microstructure/``."""
    if rel.startswith("data/") or rel.startswith("data\\"):
        return Path(rel).resolve()
    return (Path("data") / rel).resolve()


def _build_per_file(entries: Sequence[Mapping[str, Any]]) -> tuple[
    MultidayPerFileArtefactPaths, ...
]:
    out: list[MultidayPerFileArtefactPaths] = []
    for i, raw in enumerate(entries):
        where = f"per_file_inventory[{i}]"
        date = _require_str(raw, "date", where=where)
        symbol = _require_str(raw, "symbol", where=where)
        parquet_rel = _require_str(raw, "local_parquet_path", where=where)
        sidecar_rel = _require_str(raw, "local_sidecar_path", where=where)
        zip_rel = _require_str(raw, "source_zip_path", where=where)
        parquet_sha = _require_str(raw, "parquet_sha256", where=where)
        sidecar_sha = _require_str(raw, "sidecar_sha256", where=where)
        source_file_sha = _require_str(raw, "source_file_sha256", where=where)
        parquet_size = _require_int(raw, "parquet_size_bytes", where=where)
        sidecar_size = _require_int(raw, "sidecar_size_bytes", where=where)
        event_count = _require_int(raw, "event_count", where=where)
        first_t = _require_int(raw, "first_transact_time_ms", where=where)
        last_t = _require_int(raw, "last_transact_time_ms", where=where)
        min_id = _require_int(raw, "min_agg_trade_id", where=where)
        max_id = _require_int(raw, "max_agg_trade_id", where=where)
        out.append(
            MultidayPerFileArtefactPaths(
                date=date,
                symbol=symbol,
                parquet_path=_resolve_data_relative(parquet_rel),
                parquet_sidecar_path=_resolve_data_relative(sidecar_rel),
                source_zip_path=_resolve_data_relative(zip_rel),
                expected_parquet_sha=parquet_sha,
                expected_parquet_size=parquet_size,
                expected_sidecar_sha=sidecar_sha,
                expected_sidecar_size=sidecar_size,
                expected_source_zip_sha=source_file_sha,
                expected_event_count=event_count,
                expected_first_transact_time_ms=first_t,
                expected_last_transact_time_ms=last_t,
                expected_min_agg_trade_id=min_id,
                expected_max_agg_trade_id=max_id,
            )
        )
    return tuple(out)


def resolve_multiday_derived_source_artefact_paths(
    *,
    derived_manifest_path: Path,
    derived_manifest: Mapping[str, Any],
) -> MultidayDerivedSourceArtefactPaths:
    """Resolve every source-artefact path referenced by the multi-day manifest.

    The v002 derived manifest carries top-level ``source_manifest_path``,
    ``source_acquisition_log_path``, ``source_gate_report_path``, and
    ``source_successor_state_path`` keys as full ``data/microstructure/...``
    strings. Their paired ``.sha256`` sidecars sit next to them.

    The ``per_file_inventory`` entries carry
    ``local_parquet_path`` / ``local_sidecar_path`` / ``source_zip_path``
    relative to ``data/`` (each begins with ``microstructure/...``).
    """
    derived_sidecar_path = Path(str(derived_manifest_path) + ".sha256")

    raw_manifest_rel = _require_str(
        derived_manifest, "source_manifest_path", where="derived manifest"
    )
    raw_manifest_path = Path(raw_manifest_rel).resolve()
    assert_path_under_microstructure(
        raw_manifest_path, label="source_manifest_path"
    )
    raw_manifest_sidecar_path = Path(str(raw_manifest_path) + ".sha256")

    acq_rel = _require_str(
        derived_manifest, "source_acquisition_log_path", where="derived manifest"
    )
    acq_path = Path(acq_rel).resolve()
    assert_path_under_microstructure(
        acq_path, label="source_acquisition_log_path"
    )
    acq_sidecar_path = Path(str(acq_path) + ".sha256")

    gate_rel = _require_str(
        derived_manifest, "source_gate_report_path", where="derived manifest"
    )
    gate_path = Path(gate_rel).resolve()
    assert_path_under_microstructure(
        gate_path, label="source_gate_report_path"
    )
    gate_sidecar_path = Path(str(gate_path) + ".sha256")

    succ_rel = _require_str(
        derived_manifest, "source_successor_state_path", where="derived manifest"
    )
    succ_path = Path(succ_rel).resolve()
    assert_path_under_microstructure(
        succ_path, label="source_successor_state_path"
    )
    succ_sidecar_path = Path(str(succ_path) + ".sha256")

    inventory = derived_manifest.get("per_file_inventory")
    if not isinstance(inventory, list) or not inventory:
        raise GateIOError("derived manifest per_file_inventory is missing or empty")
    per_file = _build_per_file(inventory)

    return MultidayDerivedSourceArtefactPaths(
        derived_manifest_path=derived_manifest_path,
        derived_manifest_sidecar_path=derived_sidecar_path,
        raw_manifest_path=raw_manifest_path,
        raw_manifest_sidecar_path=raw_manifest_sidecar_path,
        acquisition_log_path=acq_path,
        acquisition_log_sidecar_path=acq_sidecar_path,
        gate_report_path=gate_path,
        gate_report_sidecar_path=gate_sidecar_path,
        successor_state_path=succ_path,
        successor_state_sidecar_path=succ_sidecar_path,
        per_file=per_file,
    )


@dataclass(frozen=True)
class MultidayLoadedArtefactBundle:
    """Pre-loaded SHAs and bytes used by the multi-day check functions.

    Per-file Parquet SHAs are loaded lazily inside the check phase;
    only the bundle's *governance* artefacts are eagerly hashed at
    bundle construction time.
    """

    derived_manifest_bytes: bytes
    derived_manifest_sha: str
    derived_manifest: dict[str, Any]
    derived_sidecar_first_64: str
    raw_manifest_bytes: bytes
    raw_manifest_sha: str
    raw_manifest: dict[str, Any]
    raw_manifest_sidecar_first_64: str
    acquisition_log_sha: str
    acquisition_log_sidecar_first_64: str
    gate_report_sha: str
    gate_report_sidecar_first_64: str
    successor_state_sha: str
    successor_state_sidecar_first_64: str
    measured: dict[str, Any] = field(default_factory=dict)
