"""Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate / Raw QA.

This standalone script implements and executes the Phase 4bl-D raw
eligibility-gate / raw QA pass for the Phase 4bl-C v002 multi-day
BTCUSDT aggTrades acquisition under ``data/microstructure/``.

What the gate validates (read-only):

- Phase 4bl-C v002 raw manifest (file + canonical sidecar);
- Phase 4bl-C v002 acquisition log (file + canonical sidecar);
- the 90 local raw BTCUSDT aggTrades ZIPs and their paired
  ``.zip.sha256`` sidecars under the manifest-recorded paths;
- per-file inventory schema, statuses, sizes, SHA256, row counts,
  time bounds, and aggregate-trade-id bounds;
- decompression (one CSV member per ZIP) and **full per-row**
  ``validate_aggtrade_payload`` schema validation across every row;
- UTC-day timestamp boundaries per file;
- aggregate-trade-id monotonicity (strictly increasing) within each
  file and non-overlap of adjacent dates;
- recomputed totals (total_size_bytes, total_row_count) vs. manifest;
- existing 2025-01-15 fixture preservation;
- governance boundaries (no manifest mutation, no successor-state, no
  research_eligible flip, no eligibility_gate_status transition).

What the gate **does not** do:

- no network I/O; no Binance API; no ``data.binance.vision`` access;
- no manifest mutation; no successor-state artefact creation;
- no normalization / derived parquet / features / labels / diagnostics;
- no ML / strategy / signals / backtest;
- no authorization of any successor phase.

Public-only imports: standard library plus the Phase 4ax aggTrades
validator and the Phase 4bb-F canonical-path helpers from
``src/prometheus/research/microstructure/``. No requests / httpx /
aiohttp / urllib3 / socket / websockets / binance / dotenv dependency.
No ``.env`` reads; no ``.mcp.json`` reads; no MCP / Graphify.

Per Phase 4bb-F canonical-path policy, the gate report is written to
``data/microstructure/gate-reports/raw/<canonical_id>.json`` with
paired ``.sha256`` sidecar via
``prometheus.research.microstructure.canonical_paths``. The brief
suggested a static ``...__phase-4bl-d_raw_gate.json`` filename; we
follow the established canonical-path policy instead, and explain the
deviation in the Phase 4bl-D implementation report.

Run exactly once::

    python scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py

Exit status: 0 on pass, 1 on fail-closed (gate fail or error).
"""

from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
import traceback
import zipfile
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from datetime import date as date_cls
from pathlib import Path
from typing import Any

# ----------------------------------------------------------------------- #
# Path discipline: import only the Phase 4ax validator + Phase 4bb-F
# canonical-path helpers. No other project modules. No top-level src/
# imports beyond these two scaffold modules.
# ----------------------------------------------------------------------- #

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# ruff: noqa: E402
from prometheus.research.microstructure.aggtrades import (
    AggTradeValidationError,
    validate_aggtrade_payload,
)
from prometheus.research.microstructure.canonical_paths import (
    CanonicalPathError,
    assert_path_under_gate_reports_subdir,
    assert_path_under_microstructure,
    compute_file_sha256,
    derive_canonical_gate_report_path,
    derive_sidecar_path,
    write_paired_sha256_sidecar,
)

# ----------------------------------------------------------------------- #
# Locked scope constants
# ----------------------------------------------------------------------- #

PHASE_ID: str = "4bl-d"
PHASE_NAME: str = "Phase 4bl-D"
ARTEFACT_TYPE: str = "raw_multiday_manifest_eligibility_gate_report"
SCHEMA_VERSION: str = "v001"

DATASET_FAMILY: str = "microstructure_raw_aggtrades_v001"
DATASET_VERSION: str = "v002"
FAMILY_SUBDIR_KEY: str = "raw"
SOURCE_PHASE_BOUNDARY: str = "4bl-C"
VALIDATOR_LABEL: str = "phase_4ax_aggtrades_v001"

SYMBOL_LIST: tuple[str, ...] = ("BTCUSDT",)
DATE_START: str = "2024-12-01"
DATE_END: str = "2025-02-28"
DATE_COUNT: int = 90
EXPECTED_FILE_COUNT: int = 90

EXISTING_FIXTURE_DATE: str = "2025-01-15"
EXISTING_FIXTURE_REL_ZIP: str = (
    "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
    "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
)
EXISTING_FIXTURE_SHA256: str = (
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
)

# Phase 4bl-C recorded SHA256 values for the v002 manifest + log + sidecars.
EXPECTED_MANIFEST_SHA256: str = (
    "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
)
EXPECTED_MANIFEST_SIDECAR_SHA256: str = (
    "adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26"
)
EXPECTED_ACQUISITION_LOG_SHA256: str = (
    "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"
)
EXPECTED_ACQUISITION_LOG_SIDECAR_SHA256: str = (
    "975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958"
)

# Phase 4bl-C recorded aggregate counters that the gate must reproduce.
EXPECTED_TOTAL_ROW_COUNT: int = 155_153_449
EXPECTED_TOTAL_SIZE_BYTES: int = 1_943_823_208

# Filesystem layout. These are the locked roots; the gate refuses any
# path that resolves outside ``data/microstructure/``.
DATA_DIR: Path = Path("data")
MICROSTRUCTURE_DIR: Path = DATA_DIR / "microstructure"
MANIFESTS_DIR: Path = MICROSTRUCTURE_DIR / "manifests"
GATE_REPORTS_RAW_DIR: Path = MICROSTRUCTURE_DIR / "gate-reports" / "raw"

RAW_MANIFEST_PATH: Path = (
    MANIFESTS_DIR / "microstructure_raw_aggtrades_v001__v002.json"
)
RAW_MANIFEST_SIDECAR_PATH: Path = (
    MANIFESTS_DIR / "microstructure_raw_aggtrades_v001__v002.json.sha256"
)
ACQUISITION_LOG_PATH: Path = (
    MANIFESTS_DIR
    / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json"
)
ACQUISITION_LOG_SIDECAR_PATH: Path = (
    MANIFESTS_DIR
    / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256"
)

# Governance labels for the gate report.
GOVERNANCE_LABELS: dict[str, str] = {
    "phase": PHASE_ID,
    "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
    "validator": VALIDATOR_LABEL,
    "stop_trigger_domain": "trade_price_backtest_candidate",
    "feature_computation": "forbidden",
    "labels": "forbidden",
    "ml": "forbidden",
    "strategy": "forbidden",
    "strategy_use": "forbidden",
    "diagnostics": "forbidden",
    "backtest": "forbidden",
}

# Non-authorizations embedded in the gate report.
NON_AUTHORIZATIONS: dict[str, bool] = {
    "acquisition_authorized": False,
    "additional_downloads_authorized": False,
    "normalization_authorized": False,
    "derived_generation_authorized": False,
    "feature_generation_authorized": False,
    "label_generation_authorized": False,
    "diagnostics_authorized": False,
    "label_statistics_authorized": False,
    "ml_authorized": False,
    "strategy_authorized": False,
    "signal_authorized": False,
    "backtest_authorized": False,
    "successor_state_authorized": False,
    "phase_4bl_e_authorized": False,
    "phase_5_authorized": False,
    "paper_shadow_authorized": False,
    "live_authorized": False,
    "exchange_write_authorized": False,
    "manifest_transition_authorized": False,
    "research_eligible_flip_authorized": False,
    "eligibility_gate_status_transition_authorized": False,
}

RETAINED_VERDICT_LEDGER: list[dict[str, str]] = [
    {"id": "H0", "status": "FRAMEWORK ANCHOR"},
    {"id": "R3", "status": "BASELINE-OF-RECORD"},
    {"id": "R1a", "status": "RETAINED — NON-LEADING"},
    {"id": "R1b-narrow", "status": "RETAINED — NON-LEADING"},
    {"id": "R2", "status": "FAILED — §11.6"},
    {"id": "F1", "status": "HARD REJECT"},
    {"id": "D1-A", "status": "MECHANISM PASS / FRAMEWORK FAIL"},
    {"id": "5m_thread", "status": "OPERATIONALLY CLOSED"},
    {"id": "V2", "status": "HARD REJECT — terminal for V2 first-spec"},
    {"id": "G1", "status": "HARD REJECT — terminal for G1 first-spec"},
    {"id": "C1", "status": "HARD REJECT — terminal for C1 first-spec"},
]

PRESERVED_LOCKS: list[str] = [
    "§11.6 = 8 bps per side",
    "round-trip = 16 bps",
    "§1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max / "
    "mark-price stops",
    "M0 remains binding",
    "Phase 4ak M0 twelve-clause gate remains binding",
    "Phase 4ak post-null cooldown rule remains binding",
    "Phase 4ak cooled-down families list remains binding",
    "Phase 4al refined no-rescue rule remains binding",
    "Phase 4aw MicrostructureManifest.flip_research_eligible(...) "
    "always-raises invariant remains binding",
    "Phase 3v §8 stop-trigger-domain governance remains binding",
    "Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance "
    "remains binding",
    "Phase 4bb-F canonical path policy remains binding",
]


# ----------------------------------------------------------------------- #
# Check identifiers
# ----------------------------------------------------------------------- #

CHECK_IDS: tuple[str, ...] = (
    "manifest_file_integrity",
    "acquisition_log_integrity",
    "sidecar_format_integrity",
    "gitignore_boundary",
    "path_boundary",
    "scope_lock",
    "date_list_integrity",
    "symbol_list_integrity",
    "manifest_schema_integrity",
    "acquisition_log_schema_integrity",
    "manifest_log_counter_consistency",
    "per_file_inventory_integrity",
    "raw_zip_existence",
    "raw_zip_sha256_integrity",
    "raw_zip_sidecar_integrity",
    "zip_decompression_integrity",
    "single_csv_member_integrity",
    "full_row_schema_validation",
    "per_file_row_count_consistency",
    "per_file_time_bounds_consistency",
    "utc_day_boundary_integrity",
    "agg_trade_id_monotonicity_within_file",
    "agg_trade_id_duplicate_absence_within_file",
    "agg_trade_id_overlap_absence_across_adjacent_dates",
    "total_row_count_consistency",
    "total_size_bytes_consistency",
    "existing_fixture_preservation",
    "no_extra_dates",
    "no_missing_dates",
    "no_unexpected_statuses",
    "non_authorizations_preserved",
    "retained_verdicts_preserved",
    "project_locks_preserved",
)

# Check severities. Every recorded check has a fixed severity; the
# overall verdict is FAIL if any ``critical`` check fails.
CHECK_SEVERITY: dict[str, str] = {
    cid: "critical" for cid in CHECK_IDS
}


# ----------------------------------------------------------------------- #
# Errors
# ----------------------------------------------------------------------- #


class GateRuntimeError(RuntimeError):
    """Raised when the gate cannot complete (treated as RAW_MULTIDAY_GATE_ERROR)."""


# ----------------------------------------------------------------------- #
# CSV row decoding mirroring Phase 4bl-C / Phase 4az conventions.
# ----------------------------------------------------------------------- #

_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "a": ("agg_trade_id", "aggregate_trade_id", "a"),
    "p": ("price", "p"),
    "q": ("quantity", "q"),
    "f": ("first_trade_id", "f"),
    "l": ("last_trade_id", "l"),
    "T": ("transact_time", "trade_time", "T"),
    "m": ("is_buyer_maker", "m"),
}

_HEADERLESS_ORDER: tuple[str, ...] = ("a", "p", "q", "f", "l", "T", "m")


def _resolve_header_mapping(raw_header: Sequence[str]) -> dict[str, int] | None:
    """Map header column names to Phase 4ax payload field positions.

    Returns ``None`` for headerless CSV (Binance public archive default).
    """
    if not raw_header:
        return None
    first_cell = (raw_header[0] or "").strip()
    try:
        int(first_cell)
        return None
    except ValueError:
        pass

    mapping: dict[str, int] = {}
    lowered = [(cell or "").strip().lower() for cell in raw_header]
    for field_name, synonyms in _HEADER_ALIASES.items():
        for idx, cell in enumerate(lowered):
            if cell in {syn.lower() for syn in synonyms}:
                mapping[field_name] = idx
                break
        if field_name not in mapping:
            raise GateRuntimeError(
                f"CSV header missing required field {field_name!r} "
                f"(expected one of {synonyms!r}); got header={raw_header!r}"
            )
    return mapping


def _coerce_buyer_is_maker(token: str) -> bool:
    """Coerce the Binance ``m`` column to a strict bool.

    Accepts ``true / True / TRUE`` and ``false / False / FALSE``.
    """
    if token in ("true", "True", "TRUE"):
        return True
    if token in ("false", "False", "FALSE"):
        return False
    raise AggTradeValidationError(
        f"is_buyer_maker token must be true/True/TRUE/false/False/FALSE, "
        f"got {token!r}"
    )


def _row_to_payload(
    row: Sequence[str],
    mapping: dict[str, int] | None,
) -> dict[str, object]:
    if mapping is None:
        if len(row) < len(_HEADERLESS_ORDER):
            raise GateRuntimeError(
                f"headerless row has too few columns: expected at least "
                f"{len(_HEADERLESS_ORDER)}, got {len(row)}; row={list(row)!r}"
            )
        getters = {
            field_name: row[idx] for idx, field_name in enumerate(_HEADERLESS_ORDER)
        }
    else:
        getters = {field_name: row[idx] for field_name, idx in mapping.items()}

    return {
        "a": getters["a"],
        "p": getters["p"],
        "q": getters["q"],
        "f": getters["f"],
        "l": getters["l"],
        "T": getters["T"],
        "m": _coerce_buyer_is_maker(getters["m"]),
    }


# ----------------------------------------------------------------------- #
# Date list discipline
# ----------------------------------------------------------------------- #


def generate_expected_date_list(
    date_start: str, date_end: str
) -> list[str]:
    """Return the deterministic ``YYYY-MM-DD`` UTC date list, inclusive.

    Validates that ``date_end`` is on or after ``date_start`` and that the
    final list length is positive.
    """
    start = date_cls.fromisoformat(date_start)
    end = date_cls.fromisoformat(date_end)
    if end < start:
        raise GateRuntimeError(
            f"date_end {date_end!r} is before date_start {date_start!r}"
        )
    out: list[str] = []
    cur = start
    while cur <= end:
        out.append(cur.isoformat())
        cur = cur + timedelta(days=1)
    return out


def utc_day_window_ms(date_str: str) -> tuple[int, int]:
    """Return the UTC ms half-open window ``[start, end)`` for a UTC date.

    Inclusive of the start of *date_str* and exclusive of the start of
    the next UTC day.
    """
    day = date_cls.fromisoformat(date_str)
    start_dt = datetime(day.year, day.month, day.day, tzinfo=UTC)
    end_dt = start_dt + timedelta(days=1)
    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)
    return start_ms, end_ms


# ----------------------------------------------------------------------- #
# Sidecar parsing
# ----------------------------------------------------------------------- #

_SIDECAR_RE = re.compile(
    r"^([0-9a-f]{64})  ([^\r\n]+)\n$"
)


def parse_canonical_sidecar(sidecar_text: str) -> tuple[str, str]:
    """Parse the canonical ``<sha>  <basename>\\n`` sidecar text.

    Returns ``(sha_hex, basename)``. Raises ``GateRuntimeError`` if the
    sidecar does not match the canonical body shape (Phase 4bb-F).
    """
    m = _SIDECAR_RE.match(sidecar_text)
    if m is None:
        raise GateRuntimeError(
            f"sidecar text does not match canonical format "
            f"'<sha>  <basename>\\n'; got {sidecar_text!r}"
        )
    return m.group(1).lower(), m.group(2)


# ----------------------------------------------------------------------- #
# Path discipline
# ----------------------------------------------------------------------- #


def _is_under(path: Path, root_parts: tuple[str, ...]) -> bool:
    parts = tuple(part for part in path.parts if part not in ("", "."))
    if len(parts) < len(root_parts):
        return False
    return parts[: len(root_parts)] == root_parts


def assert_relative_under_microstructure(rel_path: str, *, label: str) -> Path:
    """Resolve a manifest-recorded ``microstructure/...`` path under ``data/``.

    The Phase 4bl-C acquisition orchestrator records ``local_zip_path``
    and ``local_sidecar_path`` as POSIX strings relative to ``data/``
    (e.g. ``microstructure/raw/.../BTCUSDT-aggTrades-2024-12-01.zip``).
    This helper validates the recorded path is genuinely under
    ``microstructure/`` and returns ``data/<rel_path>`` as a Path. Any
    backslash, drive letter, parent reference, or other escape is
    rejected.
    """
    if not isinstance(rel_path, str) or not rel_path:
        raise GateRuntimeError(f"{label} must be a non-empty string")
    if "\\" in rel_path:
        raise GateRuntimeError(
            f"{label} contains backslash (not POSIX): {rel_path!r}"
        )
    if rel_path.startswith("/") or rel_path.startswith("./"):
        raise GateRuntimeError(
            f"{label} must not be absolute or dot-prefixed: {rel_path!r}"
        )
    parts = tuple(p for p in rel_path.split("/") if p)
    if not parts or parts[0] != "microstructure":
        raise GateRuntimeError(
            f"{label} must start with 'microstructure/': {rel_path!r}"
        )
    if any(p == ".." for p in parts):
        raise GateRuntimeError(
            f"{label} must not contain parent references: {rel_path!r}"
        )
    if any(p.startswith(".") for p in parts):
        raise GateRuntimeError(
            f"{label} must not contain dotfiles: {rel_path!r}"
        )
    resolved = DATA_DIR / Path(*parts)
    if not _is_under(resolved, ("data", "microstructure")):
        raise GateRuntimeError(
            f"{label} does not resolve under data/microstructure/: {rel_path!r}"
        )
    return resolved


# ----------------------------------------------------------------------- #
# Per-file inventory: streamed full per-row validation
# ----------------------------------------------------------------------- #


@dataclass
class PerFileResult:
    """Per-file validation result and computed values.

    Critical errors are collected separately so the gate report can
    enumerate failure reasons precisely.
    """

    date: str
    local_zip_path: str
    local_sidecar_path: str
    manifest_sha256: str = ""
    computed_sha256: str | None = None
    sidecar_sha256_value: str | None = None
    zip_size_bytes: int | None = None
    manifest_size_bytes: int = 0
    computed_row_count: int | None = None
    manifest_row_count: int = 0
    computed_first_trade_time_ms: int | None = None
    manifest_first_trade_time_ms: int = 0
    computed_last_trade_time_ms: int | None = None
    manifest_last_trade_time_ms: int = 0
    computed_min_agg_trade_id: int | None = None
    manifest_min_agg_trade_id: int = 0
    computed_max_agg_trade_id: int | None = None
    manifest_max_agg_trade_id: int = 0
    rows_validated: int = 0
    schema_validation_errors: int = 0
    timestamp_boundary_errors: int = 0
    duplicate_agg_trade_id_errors: int = 0
    monotonicity_errors: int = 0
    decompression_error: str | None = None
    csv_member_error: str | None = None
    sidecar_format_error: str | None = None
    sha256_mismatch: bool = False
    sidecar_sha_mismatch: bool = False
    status: str = "pending"
    first_failure_reason: str | None = None

    def has_critical_failure(self) -> bool:
        if self.decompression_error is not None:
            return True
        if self.csv_member_error is not None:
            return True
        if self.sidecar_format_error is not None:
            return True
        if self.sha256_mismatch:
            return True
        if self.sidecar_sha_mismatch:
            return True
        if self.schema_validation_errors > 0:
            return True
        if self.timestamp_boundary_errors > 0:
            return True
        if self.duplicate_agg_trade_id_errors > 0:
            return True
        if self.monotonicity_errors > 0:
            return True
        if self.computed_row_count is None:
            return True
        if self.computed_row_count != self.manifest_row_count:
            return True
        if self.zip_size_bytes != self.manifest_size_bytes:
            return True
        return self.computed_sha256 != self.manifest_sha256

    def record_failure(self, reason: str) -> None:
        if self.first_failure_reason is None:
            self.first_failure_reason = reason

    def to_summary(self) -> dict[str, Any]:
        return {
            "date": self.date,
            "local_zip_path": self.local_zip_path,
            "local_sidecar_path": self.local_sidecar_path,
            "manifest_sha256": self.manifest_sha256,
            "computed_sha256": self.computed_sha256,
            "sidecar_sha256_value": self.sidecar_sha256_value,
            "zip_size_bytes": self.zip_size_bytes,
            "manifest_size_bytes": self.manifest_size_bytes,
            "computed_row_count": self.computed_row_count,
            "manifest_row_count": self.manifest_row_count,
            "computed_first_trade_time_ms": self.computed_first_trade_time_ms,
            "manifest_first_trade_time_ms": self.manifest_first_trade_time_ms,
            "computed_last_trade_time_ms": self.computed_last_trade_time_ms,
            "manifest_last_trade_time_ms": self.manifest_last_trade_time_ms,
            "computed_min_agg_trade_id": self.computed_min_agg_trade_id,
            "manifest_min_agg_trade_id": self.manifest_min_agg_trade_id,
            "computed_max_agg_trade_id": self.computed_max_agg_trade_id,
            "manifest_max_agg_trade_id": self.manifest_max_agg_trade_id,
            "rows_validated": self.rows_validated,
            "schema_validation_errors": self.schema_validation_errors,
            "timestamp_boundary_errors": self.timestamp_boundary_errors,
            "duplicate_agg_trade_id_errors": self.duplicate_agg_trade_id_errors,
            "monotonicity_errors": self.monotonicity_errors,
            "decompression_error": self.decompression_error,
            "csv_member_error": self.csv_member_error,
            "sidecar_format_error": self.sidecar_format_error,
            "sha256_mismatch": self.sha256_mismatch,
            "sidecar_sha_mismatch": self.sidecar_sha_mismatch,
            "status": self.status,
            "first_failure_reason": self.first_failure_reason,
        }


def _hash_file_sha256(path: Path) -> str:
    """Return the SHA256 hex digest of *path*, read in 1 MiB chunks."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_one_file(
    entry: Mapping[str, Any],
    *,
    log_progress: bool = False,
) -> PerFileResult:
    """Decompress one ZIP and run full per-row aggTrades validation.

    Returns a :class:`PerFileResult`. The function is fail-closed: a
    decompression error, schema-validation error, monotonicity error,
    or other invariant violation is recorded but does not raise. The
    caller is responsible for aggregating per-file results and turning
    the aggregate into overall pass / fail / error.
    """
    date_str = entry["date"]
    local_zip_rel = entry["local_zip_path"]
    local_sidecar_rel = entry["local_sidecar_path"]
    manifest_sha = entry["sha256"]
    manifest_size_bytes = entry["size_bytes"]
    manifest_row_count = entry["row_count"]
    manifest_first_t = entry["first_trade_time_ms"]
    manifest_last_t = entry["last_trade_time_ms"]
    manifest_min_a = entry["min_agg_trade_id"]
    manifest_max_a = entry["max_agg_trade_id"]

    result = PerFileResult(
        date=date_str,
        local_zip_path=local_zip_rel,
        local_sidecar_path=local_sidecar_rel,
        manifest_sha256=manifest_sha,
        manifest_size_bytes=manifest_size_bytes,
        manifest_row_count=manifest_row_count,
        manifest_first_trade_time_ms=manifest_first_t,
        manifest_last_trade_time_ms=manifest_last_t,
        manifest_min_agg_trade_id=manifest_min_a,
        manifest_max_agg_trade_id=manifest_max_a,
    )

    # Resolve paths under data/microstructure/.
    try:
        zip_path = assert_relative_under_microstructure(
            local_zip_rel, label=f"local_zip_path[{date_str}]"
        )
        sidecar_path = assert_relative_under_microstructure(
            local_sidecar_rel, label=f"local_sidecar_path[{date_str}]"
        )
    except GateRuntimeError as exc:
        result.decompression_error = str(exc)
        result.record_failure(f"path_resolution: {exc}")
        result.status = "fail"
        return result

    if not zip_path.is_file():
        result.decompression_error = f"raw zip not found: {zip_path}"
        result.record_failure(result.decompression_error)
        result.status = "fail"
        return result
    if not sidecar_path.is_file():
        result.sidecar_format_error = f"sidecar not found: {sidecar_path}"
        result.record_failure(result.sidecar_format_error)
        result.status = "fail"
        return result

    # Recompute file size and SHA256.
    try:
        result.zip_size_bytes = zip_path.stat().st_size
        result.computed_sha256 = _hash_file_sha256(zip_path)
    except OSError as exc:
        result.decompression_error = (
            f"failed to stat/hash zip {zip_path}: "
            f"{type(exc).__name__}: {exc}"
        )
        result.record_failure(result.decompression_error)
        result.status = "fail"
        return result

    if result.zip_size_bytes != manifest_size_bytes:
        result.record_failure(
            f"zip_size_bytes={result.zip_size_bytes} != manifest "
            f"size_bytes={manifest_size_bytes}"
        )
    if result.computed_sha256 != manifest_sha:
        result.sha256_mismatch = True
        result.record_failure(
            f"computed sha256={result.computed_sha256} != manifest "
            f"sha256={manifest_sha}"
        )

    # Parse paired sidecar (read bytes to preserve the literal trailing
    # newline; Path.read_text discards newline mode in Python 3.13+).
    try:
        sidecar_text = sidecar_path.read_bytes().decode("utf-8")
        sidecar_sha, sidecar_basename = parse_canonical_sidecar(sidecar_text)
    except (OSError, GateRuntimeError) as exc:
        result.sidecar_format_error = (
            f"sidecar parse failed: {type(exc).__name__}: {exc}"
        )
        result.record_failure(result.sidecar_format_error)
        result.status = "fail"
        return result

    result.sidecar_sha256_value = sidecar_sha
    if sidecar_basename != zip_path.name:
        result.sidecar_format_error = (
            f"sidecar basename {sidecar_basename!r} does not match zip "
            f"basename {zip_path.name!r}"
        )
        result.record_failure(result.sidecar_format_error)
    if sidecar_sha != result.computed_sha256:
        result.sidecar_sha_mismatch = True
        result.record_failure(
            f"sidecar sha256={sidecar_sha} != computed sha256="
            f"{result.computed_sha256}"
        )

    # Decompress and validate every row.
    day_start_ms, day_end_ms = utc_day_window_ms(date_str)

    try:
        with zipfile.ZipFile(zip_path) as zf:
            bad = zf.testzip()
            if bad is not None:
                result.decompression_error = (
                    f"testzip() reported corrupt member: {bad!r}"
                )
                result.record_failure(result.decompression_error)
                result.status = "fail"
                return result
            names = [n for n in zf.namelist() if not n.endswith("/")]
            if not names:
                result.decompression_error = "ZIP contains no non-directory members"
                result.record_failure(result.decompression_error)
                result.status = "fail"
                return result
            csv_members = [n for n in names if n.lower().endswith(".csv")]
            if not csv_members and len(names) == 1:
                csv_members = names
            if len(csv_members) != 1:
                result.csv_member_error = (
                    f"ZIP must contain exactly one CSV member; got "
                    f"{csv_members!r} of {names!r}"
                )
                result.record_failure(result.csv_member_error)
                result.status = "fail"
                return result
            member = csv_members[0]

            # Stream rows, full per-row validation.
            mapping: dict[str, int] | None = None
            row_count = 0
            first_t: int | None = None
            last_t: int | None = None
            min_a: int | None = None
            max_a: int | None = None
            prev_a: int | None = None
            try:
                with zf.open(member, "r") as raw:
                    text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
                    reader = csv.reader(text)
                    first_row = True
                    for row in reader:
                        if not row:
                            continue
                        if first_row:
                            mapping = _resolve_header_mapping(row)
                            first_row = False
                            if mapping is not None:
                                continue
                        # Decode to payload + validate via Phase 4ax.
                        try:
                            payload = _row_to_payload(row, mapping)
                            validated = validate_aggtrade_payload(payload)
                        except (AggTradeValidationError, GateRuntimeError) as exc:
                            result.schema_validation_errors += 1
                            result.record_failure(
                                f"row {row_count} validation failed: "
                                f"{type(exc).__name__}: {exc}"
                            )
                            # Per brief: do not downgrade to sampling.
                            # Fail closed for this file but continue to
                            # collect aggregate counters across remaining
                            # files.
                            result.status = "fail"
                            return result
                        agg_id = validated.aggregate_trade_id
                        trade_time = validated.trade_time_ms
                        # UTC day boundary.
                        if not (day_start_ms <= trade_time < day_end_ms):
                            result.timestamp_boundary_errors += 1
                            result.record_failure(
                                f"row {row_count} trade_time {trade_time} "
                                f"outside UTC day {date_str} "
                                f"[{day_start_ms}, {day_end_ms})"
                            )
                            result.status = "fail"
                            return result
                        # Monotonicity / duplicates: require strict increase.
                        if prev_a is not None:
                            if agg_id == prev_a:
                                result.duplicate_agg_trade_id_errors += 1
                                result.record_failure(
                                    f"row {row_count} duplicate agg_trade_id="
                                    f"{agg_id} (== previous {prev_a})"
                                )
                                result.status = "fail"
                                return result
                            if agg_id < prev_a:
                                result.monotonicity_errors += 1
                                result.record_failure(
                                    f"row {row_count} out-of-order agg_trade_id="
                                    f"{agg_id} (< previous {prev_a})"
                                )
                                result.status = "fail"
                                return result
                        prev_a = agg_id
                        # Bounds.
                        if first_t is None:
                            first_t = trade_time
                            last_t = trade_time
                            min_a = agg_id
                            max_a = agg_id
                        else:
                            if trade_time < first_t:
                                first_t = trade_time
                            if last_t is None or trade_time > last_t:
                                last_t = trade_time
                            if min_a is None or agg_id < min_a:
                                min_a = agg_id
                            if max_a is None or agg_id > max_a:
                                max_a = agg_id
                        row_count += 1
            except (zipfile.BadZipFile, OSError, EOFError) as exc:
                result.decompression_error = (
                    f"decompression failed: {type(exc).__name__}: {exc}"
                )
                result.record_failure(result.decompression_error)
                result.status = "fail"
                return result

            result.computed_row_count = row_count
            result.computed_first_trade_time_ms = first_t
            result.computed_last_trade_time_ms = last_t
            result.computed_min_agg_trade_id = min_a
            result.computed_max_agg_trade_id = max_a
            result.rows_validated = row_count
    except zipfile.BadZipFile as exc:
        result.decompression_error = (
            f"BadZipFile opening {zip_path}: {exc}"
        )
        result.record_failure(result.decompression_error)
        result.status = "fail"
        return result

    # Compare computed values to manifest values.
    mismatches: list[str] = []
    if result.computed_row_count != manifest_row_count:
        mismatches.append(
            f"row_count computed={result.computed_row_count} "
            f"manifest={manifest_row_count}"
        )
    if result.computed_first_trade_time_ms != manifest_first_t:
        mismatches.append(
            f"first_trade_time_ms computed="
            f"{result.computed_first_trade_time_ms} "
            f"manifest={manifest_first_t}"
        )
    if result.computed_last_trade_time_ms != manifest_last_t:
        mismatches.append(
            f"last_trade_time_ms computed="
            f"{result.computed_last_trade_time_ms} "
            f"manifest={manifest_last_t}"
        )
    if result.computed_min_agg_trade_id != manifest_min_a:
        mismatches.append(
            f"min_agg_trade_id computed="
            f"{result.computed_min_agg_trade_id} "
            f"manifest={manifest_min_a}"
        )
    if result.computed_max_agg_trade_id != manifest_max_a:
        mismatches.append(
            f"max_agg_trade_id computed="
            f"{result.computed_max_agg_trade_id} "
            f"manifest={manifest_max_a}"
        )
    if mismatches:
        for m in mismatches:
            result.record_failure(m)

    result.status = "fail" if result.has_critical_failure() else "pass"
    return result


# ----------------------------------------------------------------------- #
# Manifest schema integrity checks
# ----------------------------------------------------------------------- #

REQUIRED_MANIFEST_KEYS: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "schema_version",
    "symbol_list",
    "date_start",
    "date_end",
    "date_count",
    "expected_file_count",
    "acquired_file_count",
    "missing_file_count",
    "checksum_mismatch_count",
    "decompression_failure_count",
    "total_size_bytes",
    "total_row_count",
    "research_eligible",
    "eligibility_gate_status",
    "base_commit_sha",
    "code_commit_sha",
    "capture_config_hash",
    "acquisition_log_sha256",
    "acquisition_log_path",
    "date_list",
    "per_file_inventory",
    "governance_labels",
)

REQUIRED_INVENTORY_KEYS: tuple[str, ...] = (
    "date",
    "expected_url",
    "expected_checksum_url",
    "local_zip_path",
    "local_sidecar_path",
    "sha256",
    "sha256_from_companion",
    "size_bytes",
    "row_count",
    "first_trade_time_ms",
    "last_trade_time_ms",
    "min_agg_trade_id",
    "max_agg_trade_id",
    "retry_count",
    "status",
    "failure_reason",
    "acquired_at_unix_ms",
)


def check_manifest_schema(
    manifest: Mapping[str, Any], errors: list[str]
) -> None:
    """Record schema errors into *errors* if the manifest is missing keys.

    All errors are accumulated; the caller decides how to report.
    """
    for key in REQUIRED_MANIFEST_KEYS:
        if key not in manifest:
            errors.append(f"manifest missing required key: {key!r}")


def check_inventory_schema(
    inventory: Sequence[Mapping[str, Any]], errors: list[str]
) -> None:
    for idx, entry in enumerate(inventory):
        for key in REQUIRED_INVENTORY_KEYS:
            if key not in entry:
                errors.append(
                    f"per_file_inventory[{idx}] missing required key: {key!r}"
                )


# ----------------------------------------------------------------------- #
# Git helpers (for embedding base_commit_sha / code_commit_sha)
# ----------------------------------------------------------------------- #


def _git_head_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(_REPO_ROOT),
            stderr=subprocess.STDOUT,
        )
        return out.decode("ascii", errors="strict").strip()
    except (subprocess.CalledProcessError, OSError, FileNotFoundError):
        return ""


# ----------------------------------------------------------------------- #
# Gate orchestrator
# ----------------------------------------------------------------------- #


@dataclass
class CheckResult:
    check_id: str
    check_name: str
    status: str  # pass / fail / error / not_applicable
    severity: str  # info / warning / critical
    summary: str
    expected: Any
    observed: Any
    details: list[str] = field(default_factory=list)


def _make_check(
    check_id: str,
    *,
    status: str,
    summary: str,
    expected: Any,
    observed: Any,
    details: Sequence[str] = (),
    severity: str | None = None,
) -> dict[str, Any]:
    sev = severity or CHECK_SEVERITY.get(check_id, "critical")
    return {
        "check_id": check_id,
        "check_name": check_id,
        "status": status,
        "severity": sev,
        "summary": summary,
        "expected": expected,
        "observed": observed,
        "details": list(details),
    }


def _check_status_pass(check: Mapping[str, Any]) -> bool:
    return check["status"] in ("pass", "not_applicable")


def run_gate(*, output_root: Path, log_progress: bool = False) -> int:
    """Run the Phase 4bl-D raw multi-day eligibility gate.

    Returns process exit status: 0 on RAW_MULTIDAY_GATE_PASS, 1 on
    RAW_MULTIDAY_GATE_FAIL, 1 on RAW_MULTIDAY_GATE_ERROR.
    """
    run_started_at_unix_ms = int(time.time() * 1000)
    wall_clock_start = time.monotonic()
    head_sha = _git_head_sha()
    base_sha = head_sha  # The branch is created from main; HEAD reflects it.

    print(f"[{PHASE_NAME}] starting gate; base_commit_sha={base_sha or '<unknown>'}")
    print(f"[{PHASE_NAME}] phase_id={PHASE_ID} dataset={DATASET_FAMILY}__{DATASET_VERSION}")
    print(
        f"[{PHASE_NAME}] symbol_list={list(SYMBOL_LIST)} "
        f"date_start={DATE_START} date_end={DATE_END}"
    )

    checks: list[dict[str, Any]] = []
    failure_reasons: list[str] = []
    error_reasons: list[str] = []
    per_file_summaries: list[dict[str, Any]] = []

    # ------------------------------------------------------------------- #
    # 1. manifest_file_integrity  +  acquisition_log_integrity
    # ------------------------------------------------------------------- #

    try:
        assert_path_under_microstructure(
            RAW_MANIFEST_PATH, label="raw manifest path"
        )
        assert_path_under_microstructure(
            ACQUISITION_LOG_PATH, label="acquisition log path"
        )
    except CanonicalPathError as exc:
        error_reasons.append(f"path discipline failure: {exc}")
        return _write_error_report(
            output_root=output_root,
            checks=checks,
            failure_reasons=failure_reasons,
            error_reasons=error_reasons,
            per_file_summaries=per_file_summaries,
            head_sha=head_sha,
            base_sha=base_sha,
            run_started_at_unix_ms=run_started_at_unix_ms,
            wall_clock_seconds=time.monotonic() - wall_clock_start,
        )

    manifest_sha = _hash_file_sha256(RAW_MANIFEST_PATH) if RAW_MANIFEST_PATH.is_file() else ""
    log_sha = _hash_file_sha256(ACQUISITION_LOG_PATH) if ACQUISITION_LOG_PATH.is_file() else ""

    manifest_present = RAW_MANIFEST_PATH.is_file()
    manifest_sha_ok = manifest_sha == EXPECTED_MANIFEST_SHA256
    if manifest_present and manifest_sha_ok:
        checks.append(
            _make_check(
                "manifest_file_integrity",
                status="pass",
                summary="v002 raw manifest present with expected SHA256",
                expected={
                    "path": str(RAW_MANIFEST_PATH.as_posix()),
                    "sha256": EXPECTED_MANIFEST_SHA256,
                },
                observed={
                    "path": str(RAW_MANIFEST_PATH.as_posix()),
                    "sha256": manifest_sha,
                },
            )
        )
    else:
        reason = "manifest missing" if not manifest_present else "manifest SHA256 mismatch"
        failure_reasons.append(reason)
        checks.append(
            _make_check(
                "manifest_file_integrity",
                status="fail",
                summary=reason,
                expected={
                    "path": str(RAW_MANIFEST_PATH.as_posix()),
                    "sha256": EXPECTED_MANIFEST_SHA256,
                },
                observed={
                    "path": str(RAW_MANIFEST_PATH.as_posix()),
                    "sha256": manifest_sha,
                    "present": manifest_present,
                },
            )
        )

    log_present = ACQUISITION_LOG_PATH.is_file()
    log_sha_ok = log_sha == EXPECTED_ACQUISITION_LOG_SHA256
    if log_present and log_sha_ok:
        checks.append(
            _make_check(
                "acquisition_log_integrity",
                status="pass",
                summary="v002 acquisition log present with expected SHA256",
                expected={
                    "path": str(ACQUISITION_LOG_PATH.as_posix()),
                    "sha256": EXPECTED_ACQUISITION_LOG_SHA256,
                },
                observed={
                    "path": str(ACQUISITION_LOG_PATH.as_posix()),
                    "sha256": log_sha,
                },
            )
        )
    else:
        reason = (
            "acquisition log missing"
            if not log_present
            else "acquisition log SHA256 mismatch"
        )
        failure_reasons.append(reason)
        checks.append(
            _make_check(
                "acquisition_log_integrity",
                status="fail",
                summary=reason,
                expected={
                    "path": str(ACQUISITION_LOG_PATH.as_posix()),
                    "sha256": EXPECTED_ACQUISITION_LOG_SHA256,
                },
                observed={
                    "path": str(ACQUISITION_LOG_PATH.as_posix()),
                    "sha256": log_sha,
                    "present": log_present,
                },
            )
        )

    # ------------------------------------------------------------------- #
    # 2. sidecar_format_integrity (manifest + log sidecars)
    # ------------------------------------------------------------------- #

    sidecar_errors: list[str] = []
    manifest_sidecar_present = RAW_MANIFEST_SIDECAR_PATH.is_file()
    log_sidecar_present = ACQUISITION_LOG_SIDECAR_PATH.is_file()

    def _parse_named_sidecar(
        sidecar_path: Path, expected_basename: str, expected_sha: str
    ) -> tuple[bool, dict[str, Any]]:
        observed: dict[str, Any] = {
            "path": str(sidecar_path.as_posix()),
            "present": sidecar_path.is_file(),
        }
        if not sidecar_path.is_file():
            observed["error"] = "sidecar not present"
            return False, observed
        try:
            text = sidecar_path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            observed["error"] = f"read failed: {type(exc).__name__}: {exc}"
            return False, observed
        try:
            sha_hex, basename = parse_canonical_sidecar(text)
        except GateRuntimeError as exc:
            observed["error"] = str(exc)
            return False, observed
        observed["sha256_in_sidecar"] = sha_hex
        observed["basename_in_sidecar"] = basename
        if basename != expected_basename:
            observed["error"] = (
                f"sidecar basename {basename!r} != expected "
                f"{expected_basename!r}"
            )
            return False, observed
        if sha_hex != expected_sha:
            observed["error"] = (
                f"sidecar sha256 {sha_hex!r} != target file sha256 "
                f"{expected_sha!r}"
            )
            return False, observed
        return True, observed

    manifest_sidecar_ok, manifest_sidecar_obs = _parse_named_sidecar(
        RAW_MANIFEST_SIDECAR_PATH,
        RAW_MANIFEST_PATH.name,
        manifest_sha,
    )
    log_sidecar_ok, log_sidecar_obs = _parse_named_sidecar(
        ACQUISITION_LOG_SIDECAR_PATH,
        ACQUISITION_LOG_PATH.name,
        log_sha,
    )

    if not manifest_sidecar_ok:
        sidecar_errors.append(
            "manifest sidecar: " + manifest_sidecar_obs.get("error", "<none>")
        )
    if not log_sidecar_ok:
        sidecar_errors.append(
            "acquisition log sidecar: "
            + log_sidecar_obs.get("error", "<none>")
        )

    # Also verify sidecar self-SHAs match the expected (recorded) values.
    manifest_sidecar_self_sha = (
        _hash_file_sha256(RAW_MANIFEST_SIDECAR_PATH)
        if manifest_sidecar_present
        else ""
    )
    log_sidecar_self_sha = (
        _hash_file_sha256(ACQUISITION_LOG_SIDECAR_PATH)
        if log_sidecar_present
        else ""
    )
    manifest_sidecar_self_ok = (
        manifest_sidecar_self_sha == EXPECTED_MANIFEST_SIDECAR_SHA256
    )
    log_sidecar_self_ok = (
        log_sidecar_self_sha == EXPECTED_ACQUISITION_LOG_SIDECAR_SHA256
    )
    if not manifest_sidecar_self_ok:
        sidecar_errors.append(
            f"manifest sidecar self-sha {manifest_sidecar_self_sha!r} != "
            f"expected {EXPECTED_MANIFEST_SIDECAR_SHA256!r}"
        )
    if not log_sidecar_self_ok:
        sidecar_errors.append(
            f"acquisition log sidecar self-sha {log_sidecar_self_sha!r} != "
            f"expected {EXPECTED_ACQUISITION_LOG_SIDECAR_SHA256!r}"
        )

    if not sidecar_errors:
        checks.append(
            _make_check(
                "sidecar_format_integrity",
                status="pass",
                summary=(
                    "manifest and acquisition-log sidecars parse, match "
                    "target SHAs, and have expected self-SHAs"
                ),
                expected={
                    "manifest_sidecar_sha256": EXPECTED_MANIFEST_SIDECAR_SHA256,
                    "log_sidecar_sha256": EXPECTED_ACQUISITION_LOG_SIDECAR_SHA256,
                },
                observed={
                    "manifest_sidecar": manifest_sidecar_obs,
                    "log_sidecar": log_sidecar_obs,
                    "manifest_sidecar_self_sha": manifest_sidecar_self_sha,
                    "log_sidecar_self_sha": log_sidecar_self_sha,
                },
            )
        )
    else:
        for err in sidecar_errors:
            failure_reasons.append(err)
        checks.append(
            _make_check(
                "sidecar_format_integrity",
                status="fail",
                summary="manifest/log sidecar integrity issues detected",
                expected={
                    "manifest_sidecar_sha256": EXPECTED_MANIFEST_SIDECAR_SHA256,
                    "log_sidecar_sha256": EXPECTED_ACQUISITION_LOG_SIDECAR_SHA256,
                },
                observed={
                    "manifest_sidecar": manifest_sidecar_obs,
                    "log_sidecar": log_sidecar_obs,
                    "manifest_sidecar_self_sha": manifest_sidecar_self_sha,
                    "log_sidecar_self_sha": log_sidecar_self_sha,
                    "errors": sidecar_errors,
                },
            )
        )

    # If the v002 manifest or log SHA mismatches, we cannot reasonably
    # parse or trust the rest. Return a fail report immediately.
    if not (manifest_present and manifest_sha_ok and log_present and log_sha_ok):
        return _finalise_and_write(
            overall_status="fail",
            output_root=output_root,
            checks=checks,
            failure_reasons=failure_reasons,
            error_reasons=error_reasons,
            per_file_summaries=per_file_summaries,
            head_sha=head_sha,
            base_sha=base_sha,
            run_started_at_unix_ms=run_started_at_unix_ms,
            wall_clock_seconds=time.monotonic() - wall_clock_start,
            recomputed_manifest_sha=manifest_sha,
            recomputed_log_sha=log_sha,
            recomputed_totals=None,
            aggregate_summary=None,
        )

    # ------------------------------------------------------------------- #
    # 3. Load manifest + acquisition log JSON
    # ------------------------------------------------------------------- #

    try:
        manifest = json.loads(RAW_MANIFEST_PATH.read_text(encoding="utf-8"))
        log_obj = json.loads(ACQUISITION_LOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error_reasons.append(
            f"failed to parse manifest/log JSON: "
            f"{type(exc).__name__}: {exc}"
        )
        return _finalise_and_write(
            overall_status="error",
            output_root=output_root,
            checks=checks,
            failure_reasons=failure_reasons,
            error_reasons=error_reasons,
            per_file_summaries=per_file_summaries,
            head_sha=head_sha,
            base_sha=base_sha,
            run_started_at_unix_ms=run_started_at_unix_ms,
            wall_clock_seconds=time.monotonic() - wall_clock_start,
            recomputed_manifest_sha=manifest_sha,
            recomputed_log_sha=log_sha,
            recomputed_totals=None,
            aggregate_summary=None,
        )

    # ------------------------------------------------------------------- #
    # 4. gitignore_boundary
    # ------------------------------------------------------------------- #

    gitignore_obs = _git_check_ignore(
        [
            str(MICROSTRUCTURE_DIR.as_posix()),
            str((MICROSTRUCTURE_DIR / "gate-reports").as_posix()),
            str(GATE_REPORTS_RAW_DIR.as_posix()),
        ]
    )
    all_ignored = all(v for v in gitignore_obs.values())
    if all_ignored:
        checks.append(
            _make_check(
                "gitignore_boundary",
                status="pass",
                summary=(
                    "data/microstructure/, gate-reports/, and "
                    "gate-reports/raw/ are gitignored"
                ),
                expected={"all_ignored": True},
                observed=gitignore_obs,
            )
        )
    else:
        failure_reasons.append("gitignore_boundary failed for one or more paths")
        checks.append(
            _make_check(
                "gitignore_boundary",
                status="fail",
                summary=(
                    "one or more required paths under data/microstructure/ "
                    "are not gitignored"
                ),
                expected={"all_ignored": True},
                observed=gitignore_obs,
            )
        )

    # ------------------------------------------------------------------- #
    # 5. path_boundary (manifest paths only refer to data/microstructure/)
    # ------------------------------------------------------------------- #

    path_boundary_violations: list[str] = []
    inventory = manifest.get("per_file_inventory", [])
    for idx, entry in enumerate(inventory):
        for k in ("local_zip_path", "local_sidecar_path"):
            v = entry.get(k)
            if not isinstance(v, str):
                path_boundary_violations.append(
                    f"per_file_inventory[{idx}].{k} not a string: {v!r}"
                )
                continue
            try:
                assert_relative_under_microstructure(v, label=f"per_file[{idx}].{k}")
            except GateRuntimeError as exc:
                path_boundary_violations.append(str(exc))

    if not path_boundary_violations:
        checks.append(
            _make_check(
                "path_boundary",
                status="pass",
                summary="all manifest paths resolve under data/microstructure/",
                expected={"path_root": "data/microstructure"},
                observed={"violations": []},
            )
        )
    else:
        failure_reasons.extend(path_boundary_violations[:10])
        checks.append(
            _make_check(
                "path_boundary",
                status="fail",
                summary="manifest path-boundary violations detected",
                expected={"path_root": "data/microstructure"},
                observed={"violations": path_boundary_violations},
            )
        )

    # ------------------------------------------------------------------- #
    # 6. scope_lock
    # ------------------------------------------------------------------- #

    scope_observed = {
        "dataset_family": manifest.get("dataset_family"),
        "dataset_version": manifest.get("dataset_version"),
        "schema_version": manifest.get("schema_version"),
        "symbol_list": manifest.get("symbol_list"),
        "date_start": manifest.get("date_start"),
        "date_end": manifest.get("date_end"),
        "date_count": manifest.get("date_count"),
        "expected_file_count": manifest.get("expected_file_count"),
    }
    scope_expected = {
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "schema_version": SCHEMA_VERSION,
        "symbol_list": list(SYMBOL_LIST),
        "date_start": DATE_START,
        "date_end": DATE_END,
        "date_count": DATE_COUNT,
        "expected_file_count": EXPECTED_FILE_COUNT,
    }
    if scope_observed == scope_expected:
        checks.append(
            _make_check(
                "scope_lock",
                status="pass",
                summary="manifest scope matches Phase 4bl-D locked scope",
                expected=scope_expected,
                observed=scope_observed,
            )
        )
    else:
        failure_reasons.append("manifest scope does not match Phase 4bl-D locked scope")
        checks.append(
            _make_check(
                "scope_lock",
                status="fail",
                summary="manifest scope does not match Phase 4bl-D locked scope",
                expected=scope_expected,
                observed=scope_observed,
            )
        )

    # ------------------------------------------------------------------- #
    # 7. date_list_integrity
    # ------------------------------------------------------------------- #

    generated_dates = generate_expected_date_list(DATE_START, DATE_END)
    manifest_date_list = manifest.get("date_list")
    if (
        isinstance(manifest_date_list, list)
        and list(manifest_date_list) == generated_dates
        and len(generated_dates) == DATE_COUNT
    ):
        checks.append(
            _make_check(
                "date_list_integrity",
                status="pass",
                summary=(
                    f"manifest date_list equals generated {DATE_COUNT}-day list"
                ),
                expected={
                    "date_count": DATE_COUNT,
                    "date_start": DATE_START,
                    "date_end": DATE_END,
                },
                observed={
                    "len": len(manifest_date_list),
                    "first": manifest_date_list[:3] if manifest_date_list else [],
                    "last": manifest_date_list[-3:] if manifest_date_list else [],
                },
            )
        )
    else:
        failure_reasons.append("manifest date_list does not match generated date list")
        checks.append(
            _make_check(
                "date_list_integrity",
                status="fail",
                summary="manifest date_list mismatch",
                expected={
                    "date_count": DATE_COUNT,
                    "date_start": DATE_START,
                    "date_end": DATE_END,
                },
                observed={
                    "type": type(manifest_date_list).__name__,
                    "len": (
                        len(manifest_date_list)
                        if isinstance(manifest_date_list, list)
                        else None
                    ),
                },
            )
        )

    # ------------------------------------------------------------------- #
    # 8. symbol_list_integrity
    # ------------------------------------------------------------------- #

    if manifest.get("symbol_list") == list(SYMBOL_LIST):
        checks.append(
            _make_check(
                "symbol_list_integrity",
                status="pass",
                summary="symbol_list equals [BTCUSDT]",
                expected=list(SYMBOL_LIST),
                observed=manifest.get("symbol_list"),
            )
        )
    else:
        failure_reasons.append("symbol_list mismatch")
        checks.append(
            _make_check(
                "symbol_list_integrity",
                status="fail",
                summary="symbol_list mismatch",
                expected=list(SYMBOL_LIST),
                observed=manifest.get("symbol_list"),
            )
        )

    # ------------------------------------------------------------------- #
    # 9. manifest_schema_integrity
    # ------------------------------------------------------------------- #

    schema_errors: list[str] = []
    check_manifest_schema(manifest, schema_errors)
    if not schema_errors:
        checks.append(
            _make_check(
                "manifest_schema_integrity",
                status="pass",
                summary="manifest contains all required keys",
                expected=list(REQUIRED_MANIFEST_KEYS),
                observed={"missing_keys": []},
            )
        )
    else:
        failure_reasons.extend(schema_errors)
        checks.append(
            _make_check(
                "manifest_schema_integrity",
                status="fail",
                summary="manifest schema integrity failures",
                expected=list(REQUIRED_MANIFEST_KEYS),
                observed={"missing_keys": schema_errors},
            )
        )

    # ------------------------------------------------------------------- #
    # 10. acquisition_log_schema_integrity
    # ------------------------------------------------------------------- #

    log_required = ("overall_status", "summary", "events", "errors")
    log_missing = [k for k in log_required if k not in log_obj]
    if not log_missing:
        checks.append(
            _make_check(
                "acquisition_log_schema_integrity",
                status="pass",
                summary="acquisition log contains required top-level keys",
                expected=list(log_required),
                observed={"missing_keys": []},
            )
        )
    else:
        failure_reasons.append(f"acquisition log missing keys: {log_missing!r}")
        checks.append(
            _make_check(
                "acquisition_log_schema_integrity",
                status="fail",
                summary="acquisition log schema integrity failure",
                expected=list(log_required),
                observed={"missing_keys": log_missing},
            )
        )

    # ------------------------------------------------------------------- #
    # 11. manifest_log_counter_consistency
    # ------------------------------------------------------------------- #

    log_summary = log_obj.get("summary", {}) if isinstance(log_obj.get("summary"), dict) else {}
    log_acquired_file_count = log_summary.get("acquired_file_count")
    manifest_acquired = manifest.get("acquired_file_count")
    log_total_size = log_summary.get("total_size_bytes")
    log_total_rows = log_summary.get("total_row_count")
    counter_errors: list[str] = []
    if log_acquired_file_count != manifest_acquired:
        counter_errors.append(
            f"log.acquired_file_count={log_acquired_file_count} != "
            f"manifest.acquired_file_count={manifest_acquired}"
        )
    if log_total_size is not None and log_total_size != manifest.get("total_size_bytes"):
        counter_errors.append(
            f"log.total_size_bytes={log_total_size} != "
            f"manifest.total_size_bytes={manifest.get('total_size_bytes')}"
        )
    if log_total_rows is not None and log_total_rows != manifest.get("total_row_count"):
        counter_errors.append(
            f"log.total_row_count={log_total_rows} != "
            f"manifest.total_row_count={manifest.get('total_row_count')}"
        )
    if not counter_errors:
        checks.append(
            _make_check(
                "manifest_log_counter_consistency",
                status="pass",
                summary="manifest and log counters agree",
                expected={
                    "acquired_file_count": manifest_acquired,
                    "total_size_bytes": manifest.get("total_size_bytes"),
                    "total_row_count": manifest.get("total_row_count"),
                },
                observed={
                    "log_acquired_file_count": log_acquired_file_count,
                    "log_total_size_bytes": log_total_size,
                    "log_total_row_count": log_total_rows,
                },
            )
        )
    else:
        failure_reasons.extend(counter_errors)
        checks.append(
            _make_check(
                "manifest_log_counter_consistency",
                status="fail",
                summary="manifest and log counters do not agree",
                expected={
                    "acquired_file_count": manifest_acquired,
                    "total_size_bytes": manifest.get("total_size_bytes"),
                    "total_row_count": manifest.get("total_row_count"),
                },
                observed={
                    "errors": counter_errors,
                    "log_summary": log_summary,
                },
            )
        )

    # ------------------------------------------------------------------- #
    # 12. per_file_inventory_integrity
    # ------------------------------------------------------------------- #

    inv_errors: list[str] = []
    check_inventory_schema(inventory, inv_errors)
    if not inv_errors:
        checks.append(
            _make_check(
                "per_file_inventory_integrity",
                status="pass",
                summary=(
                    f"per_file_inventory has all required keys for "
                    f"{len(inventory)} entries"
                ),
                expected=list(REQUIRED_INVENTORY_KEYS),
                observed={"count": len(inventory)},
            )
        )
    else:
        failure_reasons.extend(inv_errors[:10])
        checks.append(
            _make_check(
                "per_file_inventory_integrity",
                status="fail",
                summary="per_file_inventory schema errors",
                expected=list(REQUIRED_INVENTORY_KEYS),
                observed={"errors": inv_errors},
            )
        )

    # ------------------------------------------------------------------- #
    # 13/14/15/16/17/18/19/20/21/22/23: per-file deep validation
    # ------------------------------------------------------------------- #

    # If we've already accumulated failures that mean the manifest is
    # untrustworthy (e.g. scope mismatch, schema errors, date_list mismatch),
    # we still proceed with per-file validation. We do not skip it: the
    # per-file evidence is informative regardless. Per-file fail-closed is
    # recorded into aggregate checks below.

    inventory_by_date: dict[str, Mapping[str, Any]] = {}
    for entry in inventory:
        d = entry.get("date")
        if isinstance(d, str):
            if d in inventory_by_date:
                inv_errors.append(f"duplicate date in per_file_inventory: {d!r}")
            inventory_by_date[d] = entry

    expected_dates_set = set(generated_dates)
    inventory_dates_set = set(inventory_by_date.keys())

    extra_dates = sorted(inventory_dates_set - expected_dates_set)
    missing_dates = sorted(expected_dates_set - inventory_dates_set)

    # no_extra_dates
    if not extra_dates:
        checks.append(
            _make_check(
                "no_extra_dates",
                status="pass",
                summary="no extra dates outside locked date list",
                expected={"extra_dates": []},
                observed={"extra_dates": []},
            )
        )
    else:
        failure_reasons.append(f"extra dates: {extra_dates}")
        checks.append(
            _make_check(
                "no_extra_dates",
                status="fail",
                summary="extra dates outside locked date list",
                expected={"extra_dates": []},
                observed={"extra_dates": extra_dates},
            )
        )

    # no_missing_dates
    if not missing_dates:
        checks.append(
            _make_check(
                "no_missing_dates",
                status="pass",
                summary="every locked date present in per_file_inventory",
                expected={"missing_dates": []},
                observed={"missing_dates": []},
            )
        )
    else:
        failure_reasons.append(f"missing dates: {missing_dates}")
        checks.append(
            _make_check(
                "no_missing_dates",
                status="fail",
                summary="missing dates in per_file_inventory",
                expected={"missing_dates": []},
                observed={"missing_dates": missing_dates},
            )
        )

    # Walk dates in chronological order. Build per-file results.
    results: list[PerFileResult] = []
    file_count = 0
    sidecar_count = 0
    schema_validation_errors_total = 0
    timestamp_boundary_errors_total = 0
    duplicate_agg_trade_id_errors_total = 0
    monotonicity_errors_total = 0
    decompression_failure_count = 0
    csv_member_failure_count = 0
    sidecar_format_failure_count = 0
    sha256_mismatch_count = 0
    sidecar_sha_mismatch_count = 0
    recomputed_total_row_count = 0
    recomputed_total_size_bytes = 0
    rows_validated_total = 0
    fixture_preserved = False
    fixture_observed_sha: str | None = None
    prev_max_a: int | None = None
    prev_date: str | None = None
    adjacent_overlap_errors: list[str] = []
    unexpected_status_errors: list[str] = []

    for idx, date_str in enumerate(generated_dates, start=1):
        entry = inventory_by_date.get(date_str)
        if entry is None:
            # Already recorded under no_missing_dates.
            continue
        status_value = entry.get("status")
        if status_value != "acquired_verified":
            unexpected_status_errors.append(
                f"{date_str}: status={status_value!r} != 'acquired_verified'"
            )
        result = validate_one_file(entry)
        results.append(result)
        per_file_summaries.append(result.to_summary())
        file_count += 1
        # Sidecar presence already counted inside validate_one_file by
        # checking sidecar_format_error; if no sidecar error, count as
        # present-and-valid sidecar.
        if result.sidecar_format_error is None:
            sidecar_count += 1
        schema_validation_errors_total += result.schema_validation_errors
        timestamp_boundary_errors_total += result.timestamp_boundary_errors
        duplicate_agg_trade_id_errors_total += result.duplicate_agg_trade_id_errors
        monotonicity_errors_total += result.monotonicity_errors
        if result.decompression_error is not None:
            decompression_failure_count += 1
        if result.csv_member_error is not None:
            csv_member_failure_count += 1
        if result.sidecar_format_error is not None:
            sidecar_format_failure_count += 1
        if result.sha256_mismatch:
            sha256_mismatch_count += 1
        if result.sidecar_sha_mismatch:
            sidecar_sha_mismatch_count += 1
        if result.computed_row_count is not None:
            recomputed_total_row_count += result.computed_row_count
            rows_validated_total += result.rows_validated
        if result.zip_size_bytes is not None:
            recomputed_total_size_bytes += result.zip_size_bytes
        # Adjacent-date overlap check using strictly-increasing aggregate
        # trade IDs across dates.
        if (
            prev_max_a is not None
            and result.computed_min_agg_trade_id is not None
            and result.computed_min_agg_trade_id <= prev_max_a
        ):
            msg = (
                f"adjacent-date overlap between {prev_date} (max_a="
                f"{prev_max_a}) and {date_str} (min_a="
                f"{result.computed_min_agg_trade_id})"
            )
            adjacent_overlap_errors.append(msg)
        # Update for next iteration.
        if result.computed_max_agg_trade_id is not None:
            prev_max_a = result.computed_max_agg_trade_id
            prev_date = date_str
        # Fixture preservation: 2025-01-15 file's computed SHA must
        # equal the recorded value.
        if date_str == EXISTING_FIXTURE_DATE:
            fixture_observed_sha = result.computed_sha256
            if (
                result.computed_sha256 == EXISTING_FIXTURE_SHA256
                and entry.get("local_zip_path") == EXISTING_FIXTURE_REL_ZIP
            ):
                fixture_preserved = True

        if log_progress:
            print(
                f"[{PHASE_NAME}] [{idx}/{len(generated_dates)}] {date_str} "
                f"rows={result.computed_row_count} size={result.zip_size_bytes} "
                f"status={result.status}"
            )

    # raw_zip_existence
    nonexistent = [
        r.date
        for r in results
        if r.decompression_error and "not found" in r.decompression_error
    ]
    if not nonexistent:
        checks.append(
            _make_check(
                "raw_zip_existence",
                status="pass",
                summary=f"all {len(results)} manifest-recorded raw zips exist",
                expected={"file_count": EXPECTED_FILE_COUNT},
                observed={"file_count": len(results)},
            )
        )
    else:
        failure_reasons.append(f"raw zips not found for dates: {nonexistent[:5]}")
        checks.append(
            _make_check(
                "raw_zip_existence",
                status="fail",
                summary="one or more manifest-recorded raw zips do not exist",
                expected={"file_count": EXPECTED_FILE_COUNT},
                observed={"missing_dates": nonexistent},
            )
        )

    # raw_zip_sha256_integrity
    if sha256_mismatch_count == 0:
        checks.append(
            _make_check(
                "raw_zip_sha256_integrity",
                status="pass",
                summary=(
                    "every raw zip's computed SHA256 matches the manifest "
                    "per_file_inventory[].sha256"
                ),
                expected={"sha256_mismatch_count": 0},
                observed={"sha256_mismatch_count": 0},
            )
        )
    else:
        failure_reasons.append(f"sha256 mismatch count={sha256_mismatch_count}")
        checks.append(
            _make_check(
                "raw_zip_sha256_integrity",
                status="fail",
                summary="raw zip SHA256 mismatch detected",
                expected={"sha256_mismatch_count": 0},
                observed={
                    "sha256_mismatch_count": sha256_mismatch_count,
                    "mismatched_dates": [
                        r.date for r in results if r.sha256_mismatch
                    ],
                },
            )
        )

    # raw_zip_sidecar_integrity
    if sidecar_format_failure_count == 0 and sidecar_sha_mismatch_count == 0:
        checks.append(
            _make_check(
                "raw_zip_sidecar_integrity",
                status="pass",
                summary=(
                    "every raw zip sidecar parses canonically and matches "
                    "the zip's computed SHA256"
                ),
                expected={
                    "sidecar_count": EXPECTED_FILE_COUNT,
                    "sidecar_format_failure_count": 0,
                    "sidecar_sha_mismatch_count": 0,
                },
                observed={
                    "sidecar_count": sidecar_count,
                    "sidecar_format_failure_count": sidecar_format_failure_count,
                    "sidecar_sha_mismatch_count": sidecar_sha_mismatch_count,
                },
            )
        )
    else:
        failure_reasons.append(
            f"sidecar format failures={sidecar_format_failure_count}, "
            f"sidecar sha mismatches={sidecar_sha_mismatch_count}"
        )
        checks.append(
            _make_check(
                "raw_zip_sidecar_integrity",
                status="fail",
                summary="raw zip sidecar integrity issues detected",
                expected={
                    "sidecar_count": EXPECTED_FILE_COUNT,
                    "sidecar_format_failure_count": 0,
                    "sidecar_sha_mismatch_count": 0,
                },
                observed={
                    "sidecar_count": sidecar_count,
                    "sidecar_format_failure_count": sidecar_format_failure_count,
                    "sidecar_sha_mismatch_count": sidecar_sha_mismatch_count,
                    "format_error_dates": [
                        r.date for r in results if r.sidecar_format_error
                    ],
                    "sha_mismatch_dates": [
                        r.date for r in results if r.sidecar_sha_mismatch
                    ],
                },
            )
        )

    # zip_decompression_integrity
    if decompression_failure_count == 0:
        checks.append(
            _make_check(
                "zip_decompression_integrity",
                status="pass",
                summary="every raw zip decompresses cleanly (testzip() OK)",
                expected={"decompression_failure_count": 0},
                observed={"decompression_failure_count": 0},
            )
        )
    else:
        failure_reasons.append(
            f"decompression failures={decompression_failure_count}"
        )
        checks.append(
            _make_check(
                "zip_decompression_integrity",
                status="fail",
                summary="one or more raw zips failed decompression",
                expected={"decompression_failure_count": 0},
                observed={
                    "decompression_failure_count": decompression_failure_count,
                    "failed_dates": [
                        r.date for r in results if r.decompression_error
                    ],
                },
            )
        )

    # single_csv_member_integrity
    if csv_member_failure_count == 0:
        checks.append(
            _make_check(
                "single_csv_member_integrity",
                status="pass",
                summary="every raw zip contains exactly one CSV member",
                expected={"csv_member_failure_count": 0},
                observed={"csv_member_failure_count": 0},
            )
        )
    else:
        failure_reasons.append(f"csv member failures={csv_member_failure_count}")
        checks.append(
            _make_check(
                "single_csv_member_integrity",
                status="fail",
                summary="one or more raw zips violate single-CSV-member rule",
                expected={"csv_member_failure_count": 0},
                observed={
                    "csv_member_failure_count": csv_member_failure_count,
                    "failed_dates": [
                        r.date for r in results if r.csv_member_error
                    ],
                },
            )
        )

    # full_row_schema_validation
    if schema_validation_errors_total == 0:
        checks.append(
            _make_check(
                "full_row_schema_validation",
                status="pass",
                summary=(
                    f"all {rows_validated_total} aggTrade rows passed Phase 4ax "
                    "validate_aggtrade_payload"
                ),
                expected={"schema_validation_errors": 0},
                observed={
                    "schema_validation_errors": 0,
                    "rows_validated": rows_validated_total,
                },
            )
        )
    else:
        failure_reasons.append(
            f"schema validation errors={schema_validation_errors_total}"
        )
        checks.append(
            _make_check(
                "full_row_schema_validation",
                status="fail",
                summary="one or more aggTrade rows failed schema validation",
                expected={"schema_validation_errors": 0},
                observed={
                    "schema_validation_errors": schema_validation_errors_total,
                    "failed_dates": [
                        r.date for r in results if r.schema_validation_errors > 0
                    ],
                },
            )
        )

    # per_file_row_count_consistency
    row_count_mismatches = [
        r.date for r in results if r.computed_row_count != r.manifest_row_count
    ]
    if not row_count_mismatches:
        checks.append(
            _make_check(
                "per_file_row_count_consistency",
                status="pass",
                summary="every file's computed row_count matches the manifest",
                expected={"mismatched_dates": []},
                observed={"mismatched_dates": []},
            )
        )
    else:
        failure_reasons.append(
            f"row count mismatches at {row_count_mismatches[:5]}"
        )
        checks.append(
            _make_check(
                "per_file_row_count_consistency",
                status="fail",
                summary="row_count mismatches between computed and manifest",
                expected={"mismatched_dates": []},
                observed={"mismatched_dates": row_count_mismatches},
            )
        )

    # per_file_time_bounds_consistency
    time_bounds_mismatches: list[str] = []
    for r in results:
        if r.computed_first_trade_time_ms != r.manifest_first_trade_time_ms:
            time_bounds_mismatches.append(f"{r.date}: first_trade_time_ms")
        if r.computed_last_trade_time_ms != r.manifest_last_trade_time_ms:
            time_bounds_mismatches.append(f"{r.date}: last_trade_time_ms")
        if r.computed_min_agg_trade_id != r.manifest_min_agg_trade_id:
            time_bounds_mismatches.append(f"{r.date}: min_agg_trade_id")
        if r.computed_max_agg_trade_id != r.manifest_max_agg_trade_id:
            time_bounds_mismatches.append(f"{r.date}: max_agg_trade_id")
    if not time_bounds_mismatches:
        checks.append(
            _make_check(
                "per_file_time_bounds_consistency",
                status="pass",
                summary=(
                    "every file's computed first/last trade times and min/max "
                    "agg_trade_ids match the manifest"
                ),
                expected={"mismatches": []},
                observed={"mismatches": []},
            )
        )
    else:
        failure_reasons.append(
            f"per-file time/agg-id bounds mismatches: {time_bounds_mismatches[:5]}"
        )
        checks.append(
            _make_check(
                "per_file_time_bounds_consistency",
                status="fail",
                summary=(
                    "per-file time / agg-id bounds mismatch between computed and "
                    "manifest"
                ),
                expected={"mismatches": []},
                observed={"mismatches": time_bounds_mismatches},
            )
        )

    # utc_day_boundary_integrity
    if timestamp_boundary_errors_total == 0:
        checks.append(
            _make_check(
                "utc_day_boundary_integrity",
                status="pass",
                summary=(
                    "every row's trade_time lies within its UTC-day "
                    "[start, end) window"
                ),
                expected={"timestamp_boundary_errors": 0},
                observed={"timestamp_boundary_errors": 0},
            )
        )
    else:
        failure_reasons.append(
            f"utc-day boundary errors={timestamp_boundary_errors_total}"
        )
        checks.append(
            _make_check(
                "utc_day_boundary_integrity",
                status="fail",
                summary="one or more rows violate UTC-day boundary",
                expected={"timestamp_boundary_errors": 0},
                observed={
                    "timestamp_boundary_errors": timestamp_boundary_errors_total,
                    "failed_dates": [
                        r.date for r in results if r.timestamp_boundary_errors > 0
                    ],
                },
            )
        )

    # agg_trade_id_monotonicity_within_file
    if monotonicity_errors_total == 0:
        checks.append(
            _make_check(
                "agg_trade_id_monotonicity_within_file",
                status="pass",
                summary="every file has strictly-increasing aggregate trade IDs",
                expected={"monotonicity_errors": 0},
                observed={"monotonicity_errors": 0},
            )
        )
    else:
        failure_reasons.append(f"monotonicity errors={monotonicity_errors_total}")
        checks.append(
            _make_check(
                "agg_trade_id_monotonicity_within_file",
                status="fail",
                summary="one or more files violate agg-id monotonicity",
                expected={"monotonicity_errors": 0},
                observed={"monotonicity_errors": monotonicity_errors_total},
            )
        )

    # agg_trade_id_duplicate_absence_within_file
    if duplicate_agg_trade_id_errors_total == 0:
        checks.append(
            _make_check(
                "agg_trade_id_duplicate_absence_within_file",
                status="pass",
                summary="every file has unique aggregate trade IDs (no duplicates)",
                expected={"duplicate_errors": 0},
                observed={"duplicate_errors": 0},
            )
        )
    else:
        failure_reasons.append(
            f"duplicate agg_trade_id errors={duplicate_agg_trade_id_errors_total}"
        )
        checks.append(
            _make_check(
                "agg_trade_id_duplicate_absence_within_file",
                status="fail",
                summary="one or more files have duplicate aggregate trade IDs",
                expected={"duplicate_errors": 0},
                observed={
                    "duplicate_errors": duplicate_agg_trade_id_errors_total,
                },
            )
        )

    # agg_trade_id_overlap_absence_across_adjacent_dates
    if not adjacent_overlap_errors:
        checks.append(
            _make_check(
                "agg_trade_id_overlap_absence_across_adjacent_dates",
                status="pass",
                summary=(
                    "aggregate trade IDs are strictly non-overlapping across "
                    "adjacent dates"
                ),
                expected={"overlap_errors": 0},
                observed={"overlap_errors": 0},
            )
        )
    else:
        failure_reasons.extend(adjacent_overlap_errors[:5])
        checks.append(
            _make_check(
                "agg_trade_id_overlap_absence_across_adjacent_dates",
                status="fail",
                summary="aggregate trade IDs overlap across adjacent dates",
                expected={"overlap_errors": 0},
                observed={
                    "overlap_errors": len(adjacent_overlap_errors),
                    "details": adjacent_overlap_errors,
                },
            )
        )

    # total_row_count_consistency
    if (
        recomputed_total_row_count == manifest.get("total_row_count")
        and recomputed_total_row_count == EXPECTED_TOTAL_ROW_COUNT
    ):
        checks.append(
            _make_check(
                "total_row_count_consistency",
                status="pass",
                summary=(
                    f"recomputed total_row_count={recomputed_total_row_count} "
                    "matches manifest and Phase 4bl-C expected"
                ),
                expected={
                    "manifest_total_row_count": manifest.get("total_row_count"),
                    "phase_4bl_c_expected": EXPECTED_TOTAL_ROW_COUNT,
                },
                observed={
                    "recomputed_total_row_count": recomputed_total_row_count,
                },
            )
        )
    else:
        failure_reasons.append(
            f"total_row_count mismatch: recomputed="
            f"{recomputed_total_row_count} manifest="
            f"{manifest.get('total_row_count')} expected={EXPECTED_TOTAL_ROW_COUNT}"
        )
        checks.append(
            _make_check(
                "total_row_count_consistency",
                status="fail",
                summary="total_row_count mismatch",
                expected={
                    "manifest_total_row_count": manifest.get("total_row_count"),
                    "phase_4bl_c_expected": EXPECTED_TOTAL_ROW_COUNT,
                },
                observed={
                    "recomputed_total_row_count": recomputed_total_row_count,
                },
            )
        )

    # total_size_bytes_consistency
    if (
        recomputed_total_size_bytes == manifest.get("total_size_bytes")
        and recomputed_total_size_bytes == EXPECTED_TOTAL_SIZE_BYTES
    ):
        checks.append(
            _make_check(
                "total_size_bytes_consistency",
                status="pass",
                summary=(
                    f"recomputed total_size_bytes={recomputed_total_size_bytes} "
                    "matches manifest and Phase 4bl-C expected"
                ),
                expected={
                    "manifest_total_size_bytes": manifest.get("total_size_bytes"),
                    "phase_4bl_c_expected": EXPECTED_TOTAL_SIZE_BYTES,
                },
                observed={
                    "recomputed_total_size_bytes": recomputed_total_size_bytes,
                },
            )
        )
    else:
        failure_reasons.append(
            f"total_size_bytes mismatch: recomputed="
            f"{recomputed_total_size_bytes} manifest="
            f"{manifest.get('total_size_bytes')} expected="
            f"{EXPECTED_TOTAL_SIZE_BYTES}"
        )
        checks.append(
            _make_check(
                "total_size_bytes_consistency",
                status="fail",
                summary="total_size_bytes mismatch",
                expected={
                    "manifest_total_size_bytes": manifest.get("total_size_bytes"),
                    "phase_4bl_c_expected": EXPECTED_TOTAL_SIZE_BYTES,
                },
                observed={
                    "recomputed_total_size_bytes": recomputed_total_size_bytes,
                },
            )
        )

    # existing_fixture_preservation
    if fixture_preserved:
        checks.append(
            _make_check(
                "existing_fixture_preservation",
                status="pass",
                summary=(
                    f"existing fixture {EXISTING_FIXTURE_DATE} SHA matches "
                    "Phase 4az recorded value"
                ),
                expected={
                    "date": EXISTING_FIXTURE_DATE,
                    "local_zip_path": EXISTING_FIXTURE_REL_ZIP,
                    "sha256": EXISTING_FIXTURE_SHA256,
                },
                observed={
                    "date": EXISTING_FIXTURE_DATE,
                    "sha256": fixture_observed_sha,
                    "preserved": True,
                },
            )
        )
    else:
        failure_reasons.append(
            f"existing fixture {EXISTING_FIXTURE_DATE} not preserved: "
            f"sha={fixture_observed_sha}"
        )
        checks.append(
            _make_check(
                "existing_fixture_preservation",
                status="fail",
                summary="existing Phase 4az fixture preservation failed",
                expected={
                    "date": EXISTING_FIXTURE_DATE,
                    "local_zip_path": EXISTING_FIXTURE_REL_ZIP,
                    "sha256": EXISTING_FIXTURE_SHA256,
                },
                observed={
                    "date": EXISTING_FIXTURE_DATE,
                    "sha256": fixture_observed_sha,
                    "preserved": False,
                },
            )
        )

    # no_unexpected_statuses
    if not unexpected_status_errors:
        checks.append(
            _make_check(
                "no_unexpected_statuses",
                status="pass",
                summary="every per_file_inventory entry has status='acquired_verified'",
                expected={"unexpected_status_count": 0},
                observed={"unexpected_status_count": 0},
            )
        )
    else:
        failure_reasons.extend(unexpected_status_errors[:5])
        checks.append(
            _make_check(
                "no_unexpected_statuses",
                status="fail",
                summary="unexpected per_file_inventory status values detected",
                expected={"unexpected_status_count": 0},
                observed={"errors": unexpected_status_errors},
            )
        )

    # non_authorizations_preserved
    checks.append(
        _make_check(
            "non_authorizations_preserved",
            status="pass",
            summary="every non-authorization flag is false in this gate report",
            expected=NON_AUTHORIZATIONS,
            observed=NON_AUTHORIZATIONS,
        )
    )

    # retained_verdicts_preserved
    checks.append(
        _make_check(
            "retained_verdicts_preserved",
            status="pass",
            summary="retained verdict ledger preserved verbatim",
            expected=RETAINED_VERDICT_LEDGER,
            observed=RETAINED_VERDICT_LEDGER,
        )
    )

    # project_locks_preserved
    checks.append(
        _make_check(
            "project_locks_preserved",
            status="pass",
            summary="project locks preserved verbatim",
            expected=PRESERVED_LOCKS,
            observed=PRESERVED_LOCKS,
        )
    )

    # ------------------------------------------------------------------- #
    # Aggregate summary
    # ------------------------------------------------------------------- #

    aggregate_summary = {
        "recomputed_file_count": file_count,
        "recomputed_sidecar_count": sidecar_count,
        "recomputed_total_size_bytes": recomputed_total_size_bytes,
        "recomputed_total_row_count": recomputed_total_row_count,
        "manifest_total_size_bytes": manifest.get("total_size_bytes"),
        "manifest_total_row_count": manifest.get("total_row_count"),
        "manifest_acquired_file_count": manifest_acquired,
        "acquisition_log_acquired_file_count": log_acquired_file_count,
        "all_dates_status_acquired_verified": len(unexpected_status_errors) == 0,
        "all_rows_validated_count": rows_validated_total,
        "all_schema_validation_errors_count": schema_validation_errors_total,
        "all_timestamp_boundary_errors_count": timestamp_boundary_errors_total,
        "all_duplicate_agg_trade_id_errors_count": duplicate_agg_trade_id_errors_total,
        "all_monotonicity_errors_count": monotonicity_errors_total,
        "adjacent_date_overlap_errors_count": len(adjacent_overlap_errors),
    }

    overall_status = "pass" if all(_check_status_pass(c) for c in checks) else "fail"
    return _finalise_and_write(
        overall_status=overall_status,
        output_root=output_root,
        checks=checks,
        failure_reasons=failure_reasons,
        error_reasons=error_reasons,
        per_file_summaries=per_file_summaries,
        head_sha=head_sha,
        base_sha=base_sha,
        run_started_at_unix_ms=run_started_at_unix_ms,
        wall_clock_seconds=time.monotonic() - wall_clock_start,
        recomputed_manifest_sha=manifest_sha,
        recomputed_log_sha=log_sha,
        recomputed_totals={
            "recomputed_total_size_bytes": recomputed_total_size_bytes,
            "recomputed_total_row_count": recomputed_total_row_count,
        },
        aggregate_summary=aggregate_summary,
    )


# ----------------------------------------------------------------------- #
# Report writing
# ----------------------------------------------------------------------- #


def _write_error_report(
    *,
    output_root: Path,
    checks: list[dict[str, Any]],
    failure_reasons: list[str],
    error_reasons: list[str],
    per_file_summaries: list[dict[str, Any]],
    head_sha: str,
    base_sha: str,
    run_started_at_unix_ms: int,
    wall_clock_seconds: float,
) -> int:
    return _finalise_and_write(
        overall_status="error",
        output_root=output_root,
        checks=checks,
        failure_reasons=failure_reasons,
        error_reasons=error_reasons,
        per_file_summaries=per_file_summaries,
        head_sha=head_sha,
        base_sha=base_sha,
        run_started_at_unix_ms=run_started_at_unix_ms,
        wall_clock_seconds=wall_clock_seconds,
        recomputed_manifest_sha="",
        recomputed_log_sha="",
        recomputed_totals=None,
        aggregate_summary=None,
    )


def _git_check_ignore(paths: Iterable[str]) -> dict[str, bool]:
    """Return ``{path: gitignored?}`` using ``git check-ignore``."""
    out: dict[str, bool] = {}
    for p in paths:
        try:
            res = subprocess.run(
                ["git", "check-ignore", "--quiet", p],
                cwd=str(_REPO_ROOT),
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            out[p] = res.returncode == 0
        except (OSError, FileNotFoundError):
            out[p] = False
    return out


def _platform_summary() -> dict[str, str]:
    return {
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "platform_machine": platform.machine(),
        "platform_python_version": platform.python_version(),
    }


def _finalise_and_write(
    *,
    overall_status: str,
    output_root: Path,
    checks: list[dict[str, Any]],
    failure_reasons: list[str],
    error_reasons: list[str],
    per_file_summaries: list[dict[str, Any]],
    head_sha: str,
    base_sha: str,
    run_started_at_unix_ms: int,
    wall_clock_seconds: float,
    recomputed_manifest_sha: str,
    recomputed_log_sha: str,
    recomputed_totals: dict[str, int] | None,
    aggregate_summary: dict[str, Any] | None,
) -> int:
    """Write the gate report JSON + paired SHA256 sidecar atomically.

    Returns exit status 0 for pass, 1 otherwise.
    """
    if overall_status == "pass":
        gate_verdict = "RAW_MULTIDAY_GATE_PASS"
        eligibility_after = "pass_report_level_only"
    elif overall_status == "fail":
        gate_verdict = "RAW_MULTIDAY_GATE_FAIL"
        eligibility_after = "fail_report_level_only"
    elif overall_status == "error":
        gate_verdict = "RAW_MULTIDAY_GATE_ERROR"
        eligibility_after = "error_report_level_only"
    else:  # defensive
        gate_verdict = "RAW_MULTIDAY_GATE_ERROR"
        eligibility_after = "error_report_level_only"

    pass_count = sum(1 for c in checks if c["status"] == "pass")
    fail_count = sum(1 for c in checks if c["status"] == "fail")
    err_count = sum(1 for c in checks if c["status"] == "error")
    na_count = sum(1 for c in checks if c["status"] == "not_applicable")
    total = len(checks)

    # Compose canonical gate report path.
    microstructure_root = output_root.resolve()
    if microstructure_root.name != "microstructure":
        # The caller is responsible for passing data/microstructure/.
        # We fall back to MICROSTRUCTURE_DIR when not under it.
        microstructure_root = MICROSTRUCTURE_DIR.resolve()
    try:
        report_path = derive_canonical_gate_report_path(
            microstructure_root=microstructure_root,
            family=FAMILY_SUBDIR_KEY,
            dataset_family=DATASET_FAMILY,
            dataset_version=DATASET_VERSION,
            phase_id=PHASE_ID,
            generated_at_unix_ms=run_started_at_unix_ms,
            code_commit_sha=head_sha or ("0" * 40),
        )
    except CanonicalPathError as exc:
        # Fall back to a stable path; record the error.
        error_reasons.append(f"canonical path derivation failed: {exc}")
        report_path = (
            GATE_REPORTS_RAW_DIR
            / f"{DATASET_FAMILY}__{DATASET_VERSION}__phase-{PHASE_ID}_raw_gate.json"
        )

    try:
        assert_path_under_microstructure(
            report_path, label="gate report path"
        )
        assert_path_under_gate_reports_subdir(
            report_path, family=FAMILY_SUBDIR_KEY, label="gate report path"
        )
    except CanonicalPathError as exc:
        error_reasons.append(f"gate report path discipline failed: {exc}")

    sidecar_path = derive_sidecar_path(report_path)

    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "phase": PHASE_NAME,
        "phase_id": PHASE_ID,
        "artefact_type": ARTEFACT_TYPE,
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "symbol_list": list(SYMBOL_LIST),
        "date_start": DATE_START,
        "date_end": DATE_END,
        "date_count": DATE_COUNT,
        "expected_file_count": EXPECTED_FILE_COUNT,
        "source_artefacts": {
            "source_manifest_path": str(RAW_MANIFEST_PATH.as_posix()),
            "source_manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "source_manifest_recomputed_sha256": recomputed_manifest_sha,
            "source_manifest_sidecar_path": str(
                RAW_MANIFEST_SIDECAR_PATH.as_posix()
            ),
            "source_manifest_sidecar_sha256": EXPECTED_MANIFEST_SIDECAR_SHA256,
            "source_acquisition_log_path": str(ACQUISITION_LOG_PATH.as_posix()),
            "source_acquisition_log_sha256": EXPECTED_ACQUISITION_LOG_SHA256,
            "source_acquisition_log_recomputed_sha256": recomputed_log_sha,
            "source_acquisition_log_sidecar_path": str(
                ACQUISITION_LOG_SIDECAR_PATH.as_posix()
            ),
            "source_acquisition_log_sidecar_sha256": (
                EXPECTED_ACQUISITION_LOG_SIDECAR_SHA256
            ),
        },
        "overall_status": overall_status,
        "gate_verdict": gate_verdict,
        "checks_total": total,
        "checks_passed": pass_count,
        "checks_failed": fail_count,
        "checks_error": err_count,
        "checks_not_applicable": na_count,
        "failure_reasons": failure_reasons,
        "error_reasons": error_reasons,
        "strict_fail_closed": True,
        "no_successor_authorization": True,
        "research_eligible_after": False,
        "eligibility_gate_status_after": eligibility_after,
        "manifest_mutated": False,
        "manifest_transition_performed": False,
        "checks": checks,
        "per_file_validation_summary": per_file_summaries,
        "aggregate_summary": aggregate_summary,
        "recomputed_totals": recomputed_totals,
        "governance_labels": GOVERNANCE_LABELS,
        "non_authorizations": NON_AUTHORIZATIONS,
        "retained_verdict_ledger": RETAINED_VERDICT_LEDGER,
        "preserved_locks": PRESERVED_LOCKS,
        "created_at_unix_ms": run_started_at_unix_ms,
        "created_at_utc": datetime.fromtimestamp(
            run_started_at_unix_ms / 1000.0, tz=UTC
        )
        .isoformat()
        .replace("+00:00", "Z"),
        "base_commit_sha": base_sha,
        "code_commit_sha": head_sha,
        "script_path": str(
            Path(__file__).relative_to(_REPO_ROOT).as_posix()
        ),
        "report_path": str(report_path.as_posix()),
        "report_sidecar_path": str(sidecar_path.as_posix()),
        "run_wall_clock_seconds": round(wall_clock_seconds, 3),
        "python_version": platform.python_version(),
        "platform_summary": _platform_summary(),
    }

    # Deterministic JSON: sorted keys, indent=2, trailing newline.
    payload_bytes = (
        json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False)
        + "\n"
    ).encode("utf-8")

    # Atomic write-then-rename.
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if report_path.exists():
        # Refuse to overwrite an existing report.
        print(
            f"[{PHASE_NAME}] ERROR: refusing to overwrite existing gate report "
            f"at {report_path}",
            file=sys.stderr,
        )
        return 1
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{report_path.name}.",
        suffix=".tmp",
        dir=str(report_path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(payload_bytes)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        if report_path.exists():
            print(
                f"[{PHASE_NAME}] ERROR: refusing to overwrite existing gate "
                f"report (race) at {report_path}",
                file=sys.stderr,
            )
            return 1
        os.replace(tmp_path, report_path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()

    # Compute final SHA256 of the on-disk report.
    report_sha = compute_file_sha256(report_path)
    write_paired_sha256_sidecar(
        json_path=report_path,
        json_sha256_hex=report_sha,
        refuse_overwrite=True,
    )

    # Console summary.
    print("")
    print(f"[{PHASE_NAME}] gate verdict:        {gate_verdict}")
    print(f"[{PHASE_NAME}] overall_status:      {overall_status}")
    print(f"[{PHASE_NAME}] checks pass/fail/err/na/total: "
          f"{pass_count}/{fail_count}/{err_count}/{na_count}/{total}")
    if recomputed_totals is not None:
        print(
            f"[{PHASE_NAME}] recomputed_total_row_count:  "
            f"{recomputed_totals['recomputed_total_row_count']}"
        )
        print(
            f"[{PHASE_NAME}] recomputed_total_size_bytes: "
            f"{recomputed_totals['recomputed_total_size_bytes']}"
        )
    print(f"[{PHASE_NAME}] report_path:         {report_path.as_posix()}")
    print(f"[{PHASE_NAME}] report_sha256:       {report_sha}")
    print(f"[{PHASE_NAME}] sidecar_path:        {sidecar_path.as_posix()}")
    print(f"[{PHASE_NAME}] wall_clock_seconds:  {wall_clock_seconds:.2f}")
    if failure_reasons:
        print(f"[{PHASE_NAME}] failure_reasons (first 5):")
        for r in failure_reasons[:5]:
            print(f"  - {r}")
    if error_reasons:
        print(f"[{PHASE_NAME}] error_reasons (first 5):")
        for r in error_reasons[:5]:
            print(f"  - {r}")

    return 0 if overall_status == "pass" else 1


# ----------------------------------------------------------------------- #
# CLI
# ----------------------------------------------------------------------- #


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="phase4bl_d_validate_multiday_raw_manifest_gate",
        description=(
            "Phase 4bl-D — Multi-Day Raw Manifest Eligibility Gate / Raw QA"
        ),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=MICROSTRUCTURE_DIR,
        help=(
            "Microstructure root (must resolve under data/microstructure/). "
            "Defaults to data/microstructure."
        ),
    )
    parser.add_argument(
        "--log-progress",
        action="store_true",
        help="Log per-file progress to stdout (verbose).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Print locked scope (symbol list, date range, paths, SHA256s) and "
            "exit without reading any data."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.dry_run:
        print(f"[{PHASE_NAME}] DRY-RUN — no files will be read.")
        print(f"  phase_id:        {PHASE_ID}")
        print(f"  dataset:         {DATASET_FAMILY}__{DATASET_VERSION}")
        print(f"  symbol_list:     {list(SYMBOL_LIST)}")
        print(f"  date_start:      {DATE_START}")
        print(f"  date_end:        {DATE_END}")
        print(f"  date_count:      {DATE_COUNT}")
        print(f"  manifest_path:   {RAW_MANIFEST_PATH.as_posix()}")
        print(f"  expected_sha256: {EXPECTED_MANIFEST_SHA256}")
        print(f"  log_path:        {ACQUISITION_LOG_PATH.as_posix()}")
        print(f"  expected_log_sha: {EXPECTED_ACQUISITION_LOG_SHA256}")
        return 0

    output_root: Path = args.output_root
    try:
        assert_path_under_microstructure(
            output_root, label="--output-root"
        )
    except CanonicalPathError as exc:
        print(
            f"[{PHASE_NAME}] ERROR: {exc}",
            file=sys.stderr,
        )
        return 1

    try:
        return run_gate(output_root=output_root, log_progress=args.log_progress)
    except Exception as exc:  # noqa: BLE001
        # Last-resort safety net: any unexpected exception is recorded as
        # RAW_MULTIDAY_GATE_ERROR via an emergency report.
        print(
            f"[{PHASE_NAME}] UNEXPECTED ERROR: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
