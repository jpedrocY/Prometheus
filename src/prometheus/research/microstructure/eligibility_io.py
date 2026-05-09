"""Offline eligibility-gate read-only artefact I/O for aggTrades.

Phase 4bb-C scope: read-only artefact loaders and a single-pass row
scanner used by the offline aggTrades eligibility-gate primitive.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read ``.env`` / ``.mcp.json``, or import any networking library;
- does NOT mutate any file under ``data/microstructure/`` or any
  manifest, sidecar, or acquisition log;
- does NOT normalize, decompress to disk, or write derived datasets;
- decompresses the archive in memory only and iterates rows once.

It is consumed by :mod:`eligibility_checks` and :mod:`eligibility_gate`.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from collections import Counter
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any

from .aggtrades import AggTradeValidationError, validate_aggtrade_payload
from .manifest import MicrostructureManifest

UTC_DAY_MS = 86_400_000
"""Number of milliseconds in a UTC day."""

MAX_ARCHIVE_BYTES = 5 * 1024 * 1024 * 1024
"""Predeclared upper bound on archive size in bytes (Phase 4ay §10 / Phase 4ba §10.10)."""

PROJECT_DATA_MICROSTRUCTURE_PARTS: tuple[str, ...] = ("data", "microstructure")
"""Path parts identifying the project's gitignored microstructure namespace."""

GATE_REPORTS_SUBDIR = "gate-reports"
"""Subdirectory under ``data/microstructure/`` reserved for gate reports."""

CSV_HEADER_ALIAS_MAP: dict[str, str] = {
    "agg_trade_id": "a",
    "price": "p",
    "quantity": "q",
    "first_trade_id": "f",
    "last_trade_id": "l",
    "transact_time": "T",
    "is_buyer_maker": "m",
    "is_best_match": "best",
}
"""Header name to canonical key mapping for Binance public archive aggTrades."""

HEADERLESS_CANONICAL_ORDER: tuple[str, ...] = ("a", "p", "q", "f", "l", "T", "m", "best")
"""Headerless CSV column order for archives that omit a header row."""

EXPECTED_CANONICAL_KEYS: frozenset[str] = frozenset({"a", "p", "q", "f", "l", "T", "m"})
"""Canonical keys the Phase 4ax validator requires (besides the optional ``best`` / ``E``)."""


class GateIOError(RuntimeError):
    """Raised when the gate cannot read an artefact safely."""


@dataclass(frozen=True)
class ArtefactPaths:
    """Resolved on-disk paths for the four read-only artefacts."""

    manifest_path: Path
    raw_zip_path: Path
    sidecar_path: Path
    acquisition_log_path: Path


@dataclass
class RowScanSummary:
    """Per-row structural summary produced by the single-pass scanner.

    Reported as structural shape only; not features.
    """

    row_count: int = 0
    first_T: int | None = None
    last_T: int | None = None
    in_day_count: int = 0
    out_day_count: int = 0
    monotone_a_non_decreasing: bool = True
    duplicate_a_count: int = 0
    out_of_order_a_count: int = 0
    min_a: int | None = None
    max_a: int | None = None
    largest_consecutive_a_gap: int = 0
    f_le_l_violations: int = 0
    m_true_count: int = 0
    m_false_count: int = 0
    m_unparsed_count: int = 0
    validator_failures: int = 0
    first_validator_failure: tuple[int, str] | None = None
    csv_column_order: tuple[str, ...] = ()
    unexpected_extra_columns: tuple[str, ...] = ()
    hour_counts: tuple[int, ...] = ()
    has_header: bool = True
    a_with_different_tuple_count: int = 0
    rows_with_T_below_utc_day_start: int = 0
    rows_with_T_at_or_after_utc_day_end: int = 0
    seen_a_count: int = 0
    csv_uncompressed_size: int = 0
    sample_anomalies: tuple[Mapping[str, Any], ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ArtefactReadResult:
    """In-memory snapshot of read-only artefact state."""

    manifest: MicrostructureManifest
    manifest_bytes_sha256: str
    manifest_bytes_len: int
    raw_zip_sha256: str
    raw_zip_size: int
    sidecar_text: str
    sidecar_first_64_hex: str
    acquisition_log: dict[str, Any]
    acquisition_log_bytes_sha256: str
    csv_member_count: int
    csv_member_names: tuple[str, ...]
    primary_csv_name: str
    primary_csv_uncompressed_size: int
    row_scan: RowScanSummary
    decompression_ok: bool
    decompression_error: str | None


def _resolve_under_microstructure(path: Path) -> bool:
    """Return ``True`` iff *path* resolves under ``data/microstructure/``."""
    try:
        resolved = path.resolve(strict=False)
    except OSError:
        return False
    parts = resolved.parts
    needle = ("data", "microstructure")
    return any(
        parts[i : i + len(needle)] == needle
        for i in range(len(parts) - len(needle) + 1)
    )


def assert_path_under_microstructure(path: Path, *, label: str) -> None:
    """Fail closed if *path* does not resolve under ``data/microstructure/``."""
    if not isinstance(path, Path):
        raise GateIOError(f"{label} must be a pathlib.Path")
    if not _resolve_under_microstructure(path):
        raise GateIOError(
            f"{label} must resolve under data/microstructure/ (got {path!s})"
        )


def resolve_artefact_paths(manifest_path: Path) -> ArtefactPaths:
    """Resolve raw zip, sidecar, and acquisition log paths from a manifest.

    The manifest's ``files[0].path`` is treated as repo-relative (relative to
    the parent of ``data/microstructure/``). The paired ``.sha256`` sidecar
    lives next to the raw zip. The acquisition log lives next to the manifest.
    """
    if not isinstance(manifest_path, Path):
        raise GateIOError("manifest_path must be a pathlib.Path")
    if not manifest_path.exists():
        raise GateIOError(f"manifest_path does not exist: {manifest_path}")
    if not manifest_path.is_file():
        raise GateIOError(f"manifest_path is not a file: {manifest_path}")
    assert_path_under_microstructure(manifest_path, label="manifest_path")

    text = manifest_path.read_text(encoding="utf-8")
    data = json.loads(text)
    files = data.get("files", [])
    if not isinstance(files, list) or not files:
        raise GateIOError("manifest has no files entry")
    first = files[0]
    if not isinstance(first, Mapping) or "path" not in first:
        raise GateIOError("manifest files[0] missing 'path'")

    relative_zip_path = Path(str(first["path"]))
    # The manifest's path is relative to the data/microstructure/ root.
    microstructure_root = _ascend_to_microstructure_root(manifest_path)
    raw_zip_path = microstructure_root / relative_zip_path
    sidecar_path = raw_zip_path.with_suffix(raw_zip_path.suffix + ".sha256")

    # Acquisition log convention: <manifest_stem>_acquisition_log.json
    acquisition_log_path = manifest_path.with_name(
        manifest_path.stem + "_acquisition_log.json"
    )

    return ArtefactPaths(
        manifest_path=manifest_path,
        raw_zip_path=raw_zip_path,
        sidecar_path=sidecar_path,
        acquisition_log_path=acquisition_log_path,
    )


def _ascend_to_microstructure_root(start: Path) -> Path:
    """Return the directory ``data/microstructure`` ancestor of *start*."""
    current = start.resolve(strict=False)
    while current.parent != current:
        if current.parts[-2:] == ("data", "microstructure"):
            return current
        current = current.parent
    raise GateIOError(
        f"could not locate data/microstructure ancestor of {start!s}"
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


def read_manifest_and_hash(
    manifest_path: Path,
) -> tuple[MicrostructureManifest, str, int]:
    """Read a manifest read-only and return ``(manifest, sha256, byte_len)``."""
    raw = manifest_path.read_bytes()
    sha = compute_bytes_sha256(raw)
    manifest = MicrostructureManifest.from_dict(json.loads(raw.decode("utf-8")))
    return manifest, sha, len(raw)


def read_sidecar(sidecar_path: Path) -> tuple[str, str]:
    """Return ``(raw_text, first_64_hex)`` for a `.sha256` sidecar."""
    if not sidecar_path.exists():
        raise GateIOError(f"sidecar_path does not exist: {sidecar_path}")
    text = sidecar_path.read_text(encoding="utf-8").strip()
    first_field = text.split()[0] if text else ""
    first_64 = first_field[:64] if len(first_field) >= 64 else first_field
    return text, first_64


def read_acquisition_log(log_path: Path) -> tuple[dict[str, Any], str]:
    """Return ``(parsed_dict, sha256)`` for the acquisition log JSON."""
    if not log_path.exists():
        raise GateIOError(f"acquisition_log_path does not exist: {log_path}")
    raw = log_path.read_bytes()
    sha = compute_bytes_sha256(raw)
    parsed = json.loads(raw.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise GateIOError("acquisition log is not a JSON object")
    return parsed, sha


def _detect_header(first_row: list[str]) -> bool:
    """Return ``True`` iff *first_row* looks like a header (non-numeric first cell)."""
    if not first_row:
        return False
    try:
        int(first_row[0])
        return False
    except ValueError:
        return True


def _coerce_m(raw: str) -> bool | None:
    """Coerce a string ``m`` value to a strict bool; return ``None`` on unknown."""
    if raw in ("true", "True", "TRUE"):
        return True
    if raw in ("false", "False", "FALSE"):
        return False
    return None


def _utc_day_start_for(t: int) -> int:
    """Return the UTC day midnight (in ms) for *t* (also in ms)."""
    return (t // UTC_DAY_MS) * UTC_DAY_MS


def scan_csv_rows_in_zip(
    zip_path: Path,
    *,
    expected_utc_day_start: int | None = None,
) -> tuple[
    RowScanSummary,
    list[Mapping[str, Any]],
    int,
    tuple[str, ...],
    bool,
    str | None,
]:
    """Iterate the single CSV member of *zip_path* once and return scan results.

    Returns ``(summary, anomalies, csv_uncompressed_size, member_names,
    decompression_ok, decompression_error)``.
    """
    summary = RowScanSummary()
    anomalies: list[Mapping[str, Any]] = []
    member_names: tuple[str, ...] = ()
    decompression_ok = True
    decompression_error: str | None = None
    csv_uncompressed_size = 0

    try:
        with zipfile.ZipFile(zip_path) as zf:
            member_names = tuple(zf.namelist())
            if len(member_names) != 1:
                # Surface as decompression-ok-but-wrong-shape; row scan skipped.
                summary.has_header = True
                return (
                    summary,
                    anomalies,
                    csv_uncompressed_size,
                    member_names,
                    True,
                    None,
                )
            member = member_names[0]
            info = zf.getinfo(member)
            csv_uncompressed_size = info.file_size
            with zf.open(member) as raw:
                data = raw.read()
    except zipfile.BadZipFile as exc:
        return (
            summary,
            anomalies,
            csv_uncompressed_size,
            member_names,
            False,
            f"BadZipFile: {exc}",
        )
    except Exception as exc:  # noqa: BLE001 — read-time fail-closed
        return (
            summary,
            anomalies,
            csv_uncompressed_size,
            member_names,
            False,
            f"{type(exc).__name__}: {exc}",
        )

    text = data.decode("utf-8")
    reader = csv.reader(io.StringIO(text))
    try:
        first_row = next(reader)
    except StopIteration:
        return (
            summary,
            anomalies,
            csv_uncompressed_size,
            member_names,
            decompression_ok,
            decompression_error,
        )

    has_header = _detect_header(first_row)
    summary.has_header = has_header

    if has_header:
        canonical_columns = tuple(
            CSV_HEADER_ALIAS_MAP.get(c, c) for c in first_row
        )
        rows_iter: Iterator[list[str]] = reader
    else:
        canonical_columns = HEADERLESS_CANONICAL_ORDER[: len(first_row)]
        rows_iter = iter([first_row, *reader])

    summary.csv_column_order = canonical_columns
    optional_keys = {"best", "E"}
    unknown_keys = {
        k
        for k in canonical_columns
        if k not in EXPECTED_CANONICAL_KEYS and k not in optional_keys
    }
    summary.unexpected_extra_columns = tuple(sorted(unknown_keys))

    seen_a: dict[int, tuple[str, str, bool | None, int]] = {}
    prev_a: int | None = None
    hour_counts = Counter[int]()

    for row_idx, raw_row in enumerate(rows_iter):
        if not raw_row:
            continue
        rec = dict(zip(canonical_columns, raw_row, strict=False))
        try:
            a = int(rec.get("a", ""))
            p_str = rec.get("p", "")
            q_str = rec.get("q", "")
            f_id = int(rec.get("f", ""))
            l_id = int(rec.get("l", ""))
            T = int(rec.get("T", ""))
            m_raw = rec.get("m", "").strip()
        except (ValueError, AttributeError) as exc:
            summary.validator_failures += 1
            if summary.first_validator_failure is None:
                summary.first_validator_failure = (row_idx, f"row parse: {exc}")
            anomalies.append(
                {
                    "kind": "row_parse_error",
                    "row_index": row_idx,
                    "row_content_preview": str(raw_row)[:160],
                    "error": str(exc),
                }
            )
            continue

        m_b = _coerce_m(m_raw)
        if m_b is True:
            summary.m_true_count += 1
        elif m_b is False:
            summary.m_false_count += 1
        else:
            summary.m_unparsed_count += 1

        # Phase 4ax validator (REST-shaped) with bool-coerced m.
        try:
            payload = {"a": a, "p": p_str, "q": q_str, "f": f_id, "l": l_id, "T": T, "m": m_b}
            validate_aggtrade_payload(payload)
        except AggTradeValidationError as exc:
            summary.validator_failures += 1
            if summary.first_validator_failure is None:
                summary.first_validator_failure = (row_idx, str(exc))
            anomalies.append(
                {
                    "kind": "validator_failure",
                    "row_index": row_idx,
                    "a": a,
                    "T": T,
                    "error": str(exc),
                }
            )

        # Per-row structural state (row count is incremented unconditionally
        # so failures are still represented in row-count cross-checks).
        summary.row_count += 1

        if summary.first_T is None:
            summary.first_T = T
        summary.last_T = T

        if expected_utc_day_start is not None:
            day_end = expected_utc_day_start + UTC_DAY_MS
            if expected_utc_day_start > T:
                summary.rows_with_T_below_utc_day_start += 1
                summary.out_day_count += 1
                anomalies.append(
                    {
                        "kind": "T_before_utc_day_start",
                        "row_index": row_idx,
                        "T": T,
                        "utc_day_start_ms": expected_utc_day_start,
                    }
                )
            elif day_end <= T:
                summary.rows_with_T_at_or_after_utc_day_end += 1
                summary.out_day_count += 1
                anomalies.append(
                    {
                        "kind": "T_at_or_after_utc_day_end",
                        "row_index": row_idx,
                        "T": T,
                        "utc_day_end_ms": day_end,
                    }
                )
            else:
                summary.in_day_count += 1
                hour = (T - expected_utc_day_start) // (3600 * 1000)
                hour_counts[int(hour)] += 1
        else:
            summary.in_day_count += 1

        # Aggregate-trade-id continuity.
        if summary.min_a is None or a < summary.min_a:
            summary.min_a = a
        if summary.max_a is None or a > summary.max_a:
            summary.max_a = a

        tup = (p_str, q_str, m_b, T)
        if a in seen_a:
            summary.duplicate_a_count += 1
            if seen_a[a] != tup:
                summary.a_with_different_tuple_count += 1
            anomalies.append(
                {
                    "kind": "duplicate_a",
                    "row_index": row_idx,
                    "a": a,
                }
            )
        else:
            seen_a[a] = tup

        if prev_a is not None:
            if a < prev_a:
                summary.out_of_order_a_count += 1
                summary.monotone_a_non_decreasing = False
                anomalies.append(
                    {
                        "kind": "a_out_of_order",
                        "row_index": row_idx,
                        "a": a,
                        "prev_a": prev_a,
                    }
                )
            else:
                gap = a - prev_a
                if gap > summary.largest_consecutive_a_gap:
                    summary.largest_consecutive_a_gap = gap
        prev_a = a

        # f / l rule.
        if l_id < f_id:
            summary.f_le_l_violations += 1
            anomalies.append(
                {
                    "kind": "f_gt_l",
                    "row_index": row_idx,
                    "f": f_id,
                    "l": l_id,
                }
            )

    if expected_utc_day_start is not None:
        summary.hour_counts = tuple(hour_counts.get(h, 0) for h in range(24))
    summary.csv_uncompressed_size = csv_uncompressed_size
    summary.seen_a_count = len(seen_a)

    return (
        summary,
        anomalies,
        csv_uncompressed_size,
        member_names,
        decompression_ok,
        decompression_error,
    )


def _build_credential_pattern() -> re.Pattern[str]:
    """Compile a regex matching any Phase 4aw denylist token (case-insensitive).

    Constructed dynamically from :data:`allowlist.DENYLIST_TOKENS` so the
    credential-shaped literals exist only in the allowlist module, which is
    the project's canonical encoding of denylist tokens.
    """
    from .allowlist import DENYLIST_TOKENS

    parts = sorted(
        (re.escape(token) for token in DENYLIST_TOKENS),
        key=len,
        reverse=True,
    )
    return re.compile("(" + "|".join(parts) + ")", re.IGNORECASE)


CREDENTIAL_PATTERN: re.Pattern[str] = _build_credential_pattern()
"""Regex matching credential-shaped or forbidden tokens in arbitrary text."""


def scan_text_for_forbidden_tokens(text: str) -> list[str]:
    """Return the list of forbidden tokens found in *text* (case-insensitive)."""
    found = CREDENTIAL_PATTERN.findall(text)
    return sorted({m.lower() for m in found})


def serialise_for_token_scan(value: object) -> str:
    """Serialise an arbitrary structured value to a string for token scanning."""
    if isinstance(value, (str, bytes)):
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return value
    if isinstance(value, Mapping):
        return json.dumps(_jsonable(value), sort_keys=True)
    if isinstance(value, (list, tuple)):
        return json.dumps([_jsonable(x) for x in value], sort_keys=True)
    return repr(value)


def _jsonable(value: object) -> object:
    """Best-effort coerce *value* for ``json.dumps``."""
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, Decimal):
        return str(value)
    return repr(value)


def utc_day_start_from_archive_path(zip_path: Path) -> int | None:
    """Parse ``YYYY-MM-DD`` from an archive filename; return the UTC day start in ms.

    Phase 4az archive paths are e.g.
    ``BTCUSDT-aggTrades-2025-01-15.zip``. Returns ``None`` if no date can be
    parsed.
    """
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", zip_path.name)
    if not match:
        return None
    y, mo, d = (int(x) for x in match.groups())
    # Compute days since epoch (Jan 1 1970) using zeller-like construction;
    # we use a UTC-only stdlib calculation without importing datetime to keep
    # the function pure.
    from datetime import UTC, datetime

    return int(datetime(y, mo, d, 0, 0, 0, tzinfo=UTC).timestamp() * 1000)


def assert_no_dangerous_imports_loaded() -> None:
    """Verify that no networking / credential modules are present in sys.modules.

    This is a runtime guard. The gate's import-boundary tests cover the static
    case; this guard catches dynamic / monkey-patched cases.
    """
    import sys

    forbidden = {
        "requests",
        "httpx",
        "aiohttp",
        "websockets",
        "binance",
        "dotenv",
        "python_dotenv",
    }
    intersect = forbidden & set(sys.modules)
    if intersect:
        raise GateIOError(
            f"forbidden modules already loaded into sys.modules: {sorted(intersect)}"
        )
