"""Phase 4bn-K — Expanded Raw Archive Eligibility Gate (pre-v002 segment).

This standalone script implements and executes the Phase 4bn-K raw
archive eligibility gate for the **new pre-v002 raw segment** acquired
by Phase 4bn-J-R2 under ``data/microstructure/``:

    BTCUSDT / Binance USDⓈ-M futures / aggTrades
    2024-03-01 .. 2024-11-30 inclusive UTC   (275 daily archives)

The gate evaluates whether the local raw pre-v002 segment is
*structurally* eligible to proceed to a future, separately authorized
normalization-readiness / normalization gate. A passing verdict makes
the segment **non-eligible** in the research sense: it does **not** flip
``research_eligible``, does **not** authorize normalization, features,
labels, ML, diagnostics, or strategy, and does **not** authorize any
successor phase.

Scope boundary (hard, fail-closed):

- The gate reads only files recorded in the Phase 4bn-J-R2 *segment*
  manifest ``microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json``.
- Every inventory date is guarded: any date ``>= 2024-12-01`` is
  rejected and its file is **never opened**. This structurally prevents
  any contact with the existing v002 terminal window
  (2024-12-01 .. 2025-02-28) and the sealed v002 test split
  (2025-02-14 .. 2025-02-28), even though those files exist locally
  under the same raw tree.
- The existing published v002 raw manifest is never read or mutated.

What the gate validates (read-only, local only):

- segment manifest + acquisition log file integrity (SHA256 vs the
  Phase 4bn-J-R2 recorded values) and their canonical ``.sha256``
  sidecars;
- gitignore + path discipline for ``data/microstructure/``;
- segment scope lock (family / version / symbol / market / data family /
  date range / segment label / counts);
- date coverage (exactly 275 dates, contiguous, no missing, no
  duplicate, no date ``>= 2024-12-01``);
- per-file path layout + sidecar canonical format
  (``<sha256>␠␠<basename>\\n``);
- per-file full SHA256 (vs manifest ``sha256`` / ``sha256_from_companion``
  and the paired sidecar);
- per-file ``zipfile.testzip()`` integrity (fail-closed on corruption);
- per-file full streaming structural scan: independent row count, UTC
  day boundary, strictly-increasing aggregate-trade-id, min/max
  agg-trade-id, first/last trade time — compared to the manifest;
- per-file **bounded** Phase 4ax ``validate_aggtrade_payload`` row-sample
  (head + tail) confirming headerless field order ``a,p,q,f,l,T,m``,
  types, and timestamp behaviour;
- recomputed aggregate footprint (5,140,686,147 bytes) and aggregate
  row count (400,001,695) vs the manifest;
- governance / boundary fields (``research_eligible: false``,
  ``eligibility_gate_status: "pending"``, ``test_holdout_touched: false``,
  the ``existing_v002_terminal_window`` not-read/not-redownloaded/
  not-overwritten block, and the ``existing_v002_sealed_test_split``
  untouched block).

What the gate **does not** do:

- no network I/O; no Binance API; no ``data.binance.vision`` access; no
  CHECKSUM download; no HEAD preflight;
- no manifest mutation; no successor-state artefact creation;
- no normalization / derived parquet / features / labels / diagnostics;
- no ML / strategy / signals / PnL / backtest;
- no v002 terminal-window read; no sealed-test-split read;
- no authorization of any successor phase.

Per the Phase 4bb-F canonical-path policy, the gate report is written to
``data/microstructure/gate-reports/raw/<canonical_id>.json`` with a
paired ``.sha256`` sidecar. The report is local and gitignored; it is
**not** committed.

Public-only imports: standard library plus the Phase 4ax aggTrades
validator and the Phase 4bb-F canonical-path helpers. No requests /
httpx / aiohttp / urllib3 / socket / websockets / binance / dotenv
dependency. No ``.env`` reads; no ``.mcp.json`` reads; no MCP / Graphify.

Run exactly once::

    python scripts/phase4bn_k_validate_pre_v002_raw_archive_gate.py

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
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from datetime import date as date_cls
from pathlib import Path
from typing import Any

# ----------------------------------------------------------------------- #
# Path discipline: import only the Phase 4ax validator + Phase 4bb-F
# canonical-path helpers. No other project modules.
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

PHASE_ID: str = "4bn-k"
PHASE_NAME: str = "Phase 4bn-K"
ARTEFACT_TYPE: str = "raw_pre_v002_segment_archive_eligibility_gate_report"
SCHEMA_VERSION: str = "v001"

DATASET_FAMILY: str = "microstructure_raw_aggtrades_v001"
DATASET_VERSION: str = "v002"
SEGMENT_LABEL: str = "pre_v002_segment"
FAMILY_SUBDIR_KEY: str = "raw"
SOURCE_PHASE_BOUNDARY: str = "4bn-J-R2"
VALIDATOR_LABEL: str = "phase_4ax_aggtrades_v001"

SYMBOL_LIST: tuple[str, ...] = ("BTCUSDT",)
DATA_FAMILY: str = "aggTrades"
MARKET: str = "binance_usdm_futures"

DATE_START: str = "2024-03-01"
DATE_END: str = "2024-11-30"
DATE_COUNT: int = 275
EXPECTED_FILE_COUNT: int = 275

# Hard boundary: any inventory date on or after this is rejected and its
# file is never opened (the v002 terminal window starts here).
V002_TERMINAL_START: str = "2024-12-01"
V002_TERMINAL_END: str = "2025-02-28"
SEALED_TEST_SPLIT_START: str = "2025-02-14"
SEALED_TEST_SPLIT_END: str = "2025-02-28"

# Phase 4bn-J-R2 recorded SHA256 values for the segment manifest + log.
EXPECTED_MANIFEST_SHA256: str = "1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1"
EXPECTED_ACQUISITION_LOG_SHA256: str = (
    "0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93"
)

# Phase 4bn-J-R2 recorded aggregate counters that the gate must reproduce.
EXPECTED_TOTAL_ROW_COUNT: int = 400_001_695
EXPECTED_TOTAL_SIZE_BYTES: int = 5_140_686_147

# Bounded Phase 4ax row-sample window per archive (head + tail). The full
# streaming structural scan still parses every row to reproduce the row
# count and bounds; the bounded sample is the per-row full-schema
# ``validate_aggtrade_payload`` check, matching how Phase 4bn-J-R2
# acquired and validated the segment (bounded Phase 4ax sample).
DEFAULT_SAMPLE_HEAD: int = 512
DEFAULT_SAMPLE_TAIL: int = 512

# Filesystem layout. These are the locked roots; the gate refuses any
# path that resolves outside ``data/microstructure/``.
DATA_DIR: Path = Path("data")
MICROSTRUCTURE_DIR: Path = DATA_DIR / "microstructure"
MANIFESTS_DIR: Path = MICROSTRUCTURE_DIR / "manifests"
GATE_REPORTS_RAW_DIR: Path = MICROSTRUCTURE_DIR / "gate-reports" / "raw"

_MANIFEST_BASENAME: str = "microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json"
_LOG_BASENAME: str = (
    "microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2_acquisition_log.json"
)
RAW_MANIFEST_PATH: Path = MANIFESTS_DIR / _MANIFEST_BASENAME
RAW_MANIFEST_SIDECAR_PATH: Path = MANIFESTS_DIR / (_MANIFEST_BASENAME + ".sha256")
ACQUISITION_LOG_PATH: Path = MANIFESTS_DIR / _LOG_BASENAME
ACQUISITION_LOG_SIDECAR_PATH: Path = MANIFESTS_DIR / (_LOG_BASENAME + ".sha256")

# Expected per-file path layout root + basename pattern.
_RAW_LAYOUT_PREFIX: str = "microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
_ZIP_BASENAME_RE = re.compile(r"^BTCUSDT-aggTrades-(\d{4}-\d{2}-\d{2})\.zip$")

# Scope-token denylist scanned across all manifest-recorded paths.
_SCOPE_DENYLIST: tuple[str, ...] = (
    "ethusdt",
    "markprice",
    "mark-price",
    "indexprice",
    "premiumindex",
    "bookticker",
    "bookdepth",
    "orderbook",
    "klines",
    # '-trades-' (hyphen-delimited) catches raw non-agg trades archives
    # (e.g. BTCUSDT-trades-YYYY-MM-DD) WITHOUT matching the in-scope
    # 'aggTrades-' / 'aggtrades-' family token (which has no hyphen before
    # 'trades').
    "-trades-",
    "/trades/",  # non-agg trades dataset directory segment
    "/spot/",  # spot market segment
)

# Governance labels for the gate report.
GOVERNANCE_LABELS: dict[str, str] = {
    "phase": PHASE_ID,
    "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
    "validator": VALIDATOR_LABEL,
    "segment_label": SEGMENT_LABEL,
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
    "endpoint_call_authorized": False,
    "normalization_authorized": False,
    "normalization_readiness_authorized": False,
    "derived_generation_authorized": False,
    "feature_generation_authorized": False,
    "label_generation_authorized": False,
    "diagnostics_authorized": False,
    "ml_authorized": False,
    "strategy_authorized": False,
    "signal_authorized": False,
    "backtest_authorized": False,
    "successor_state_authorized": False,
    "storage_migration_authorized": False,
    "database_creation_authorized": False,
    "parquet_compaction_authorized": False,
    "v003_creation_authorized": False,
    "phase_5_authorized": False,
    "paper_shadow_authorized": False,
    "live_authorized": False,
    "exchange_write_authorized": False,
    "manifest_transition_authorized": False,
    "research_eligible_flip_authorized": False,
    "eligibility_gate_status_transition_authorized": False,
    "v002_terminal_window_read_authorized": False,
    "sealed_test_split_read_authorized": False,
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
    "§1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max / mark-price stops",
    "M0 remains binding",
    "Phase 4ak M0 twelve-clause gate remains binding",
    "Phase 4ak post-null cooldown rule remains binding",
    "Phase 4ak cooled-down families list remains binding",
    "Phase 4al refined no-rescue rule remains binding",
    "Phase 4aw MicrostructureManifest.flip_research_eligible(...) "
    "always-raises invariant remains binding",
    "Phase 3v §8 stop-trigger-domain governance remains binding",
    "Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance remains binding",
    "Phase 4bb-F canonical path policy remains binding",
    "Phase 4bn-J-R1 raw-only cap amendment remains binding",
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
    "segment_boundary_date_guard",
    "date_list_integrity",
    "symbol_family_scope",
    "scope_token_denylist",
    "manifest_schema_integrity",
    "per_file_path_layout",
    "raw_zip_existence",
    "raw_zip_sha256_integrity",
    "raw_zip_sidecar_integrity",
    "zip_decompression_integrity",
    "single_csv_member_integrity",
    "bounded_row_sample_schema_validation",
    "per_file_row_count_consistency",
    "per_file_time_bounds_consistency",
    "utc_day_boundary_integrity",
    "agg_trade_id_monotonicity_within_file",
    "agg_trade_id_overlap_absence_across_adjacent_dates",
    "total_row_count_consistency",
    "total_size_bytes_consistency",
    "archive_count_consistency",
    "sidecar_count_consistency",
    "no_unexpected_statuses",
    "manifest_eligibility_state",
    "v002_terminal_window_by_reference_preservation",
    "sealed_test_split_untouched",
    "non_authorizations_preserved",
    "retained_verdicts_preserved",
    "project_locks_preserved",
)

CHECK_SEVERITY: dict[str, str] = {cid: "critical" for cid in CHECK_IDS}


# ----------------------------------------------------------------------- #
# Errors
# ----------------------------------------------------------------------- #


class GateRuntimeError(RuntimeError):
    """Raised when the gate cannot complete (treated as gate ERROR)."""


# ----------------------------------------------------------------------- #
# CSV row decoding (mirrors Phase 4bl-D / 4bl-C / 4az conventions).
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

    Returns ``None`` for headerless CSV. Binance USDⓈ-M daily aggTrades
    archives in this segment carry a header row
    (``agg_trade_id,price,...,is_buyer_maker``); the header is detected
    and skipped (it is not counted as a data row).
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
    if token in ("true", "True", "TRUE"):
        return True
    if token in ("false", "False", "FALSE"):
        return False
    raise AggTradeValidationError(
        f"is_buyer_maker token must be true/True/TRUE/false/False/FALSE, got {token!r}"
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
        getters = {field_name: row[idx] for idx, field_name in enumerate(_HEADERLESS_ORDER)}
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


def generate_expected_date_list(date_start: str, date_end: str) -> list[str]:
    """Return the deterministic ``YYYY-MM-DD`` UTC date list, inclusive."""
    start = date_cls.fromisoformat(date_start)
    end = date_cls.fromisoformat(date_end)
    if end < start:
        raise GateRuntimeError(f"date_end {date_end!r} is before date_start {date_start!r}")
    out: list[str] = []
    cur = start
    while cur <= end:
        out.append(cur.isoformat())
        cur = cur + timedelta(days=1)
    return out


def is_within_segment(date_str: str) -> bool:
    """Return True iff *date_str* is within the pre-v002 segment window.

    The pre-v002 segment is ``[DATE_START, V002_TERMINAL_START)`` — i.e.
    on or after 2024-03-01 and strictly before 2024-12-01.
    """
    d = date_cls.fromisoformat(date_str)
    return date_cls.fromisoformat(DATE_START) <= d < date_cls.fromisoformat(V002_TERMINAL_START)


def utc_day_window_ms(date_str: str) -> tuple[int, int]:
    """Return the UTC ms half-open window ``[start, end)`` for a UTC date."""
    day = date_cls.fromisoformat(date_str)
    start_dt = datetime(day.year, day.month, day.day, tzinfo=UTC)
    end_dt = start_dt + timedelta(days=1)
    return int(start_dt.timestamp() * 1000), int(end_dt.timestamp() * 1000)


# ----------------------------------------------------------------------- #
# Sidecar parsing
# ----------------------------------------------------------------------- #

_SIDECAR_RE = re.compile(r"^([0-9a-f]{64})  ([^\r\n]+)\n$")


def parse_canonical_sidecar(sidecar_text: str) -> tuple[str, str]:
    """Parse the canonical ``<sha>  <basename>\\n`` sidecar text."""
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
    """Resolve a manifest-recorded ``microstructure/...`` path under ``data/``."""
    if not isinstance(rel_path, str) or not rel_path:
        raise GateRuntimeError(f"{label} must be a non-empty string")
    if "\\" in rel_path:
        raise GateRuntimeError(f"{label} contains backslash (not POSIX): {rel_path!r}")
    if rel_path.startswith("/") or rel_path.startswith("./"):
        raise GateRuntimeError(f"{label} must not be absolute or dot-prefixed: {rel_path!r}")
    parts = tuple(p for p in rel_path.split("/") if p)
    if not parts or parts[0] != "microstructure":
        raise GateRuntimeError(f"{label} must start with 'microstructure/': {rel_path!r}")
    if any(p == ".." for p in parts):
        raise GateRuntimeError(f"{label} must not contain parent references: {rel_path!r}")
    if any(p.startswith(".") for p in parts):
        raise GateRuntimeError(f"{label} must not contain dotfiles: {rel_path!r}")
    resolved = DATA_DIR / Path(*parts)
    if not _is_under(resolved, ("data", "microstructure")):
        raise GateRuntimeError(f"{label} does not resolve under data/microstructure/: {rel_path!r}")
    return resolved


# ----------------------------------------------------------------------- #
# Per-file inventory validation
# ----------------------------------------------------------------------- #


@dataclass
class PerFileResult:
    date: str
    local_zip_path: str
    local_sidecar_path: str
    manifest_sha256: str = ""
    manifest_companion_sha256: str = ""
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
    rows_sampled_validated: int = 0
    schema_validation_errors: int = 0
    timestamp_boundary_errors: int = 0
    monotonicity_errors: int = 0
    duplicate_agg_trade_id_errors: int = 0
    path_layout_error: str | None = None
    decompression_error: str | None = None
    csv_member_error: str | None = None
    sidecar_format_error: str | None = None
    sha256_mismatch: bool = False
    companion_sha_mismatch: bool = False
    sidecar_sha_mismatch: bool = False
    status: str = "pending"
    first_failure_reason: str | None = None

    def has_critical_failure(self) -> bool:
        if self.path_layout_error is not None:
            return True
        if self.decompression_error is not None:
            return True
        if self.csv_member_error is not None:
            return True
        if self.sidecar_format_error is not None:
            return True
        if self.sha256_mismatch or self.companion_sha_mismatch:
            return True
        if self.sidecar_sha_mismatch:
            return True
        if self.schema_validation_errors > 0:
            return True
        if self.timestamp_boundary_errors > 0:
            return True
        if self.monotonicity_errors > 0:
            return True
        if self.duplicate_agg_trade_id_errors > 0:
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
            "rows_sampled_validated": self.rows_sampled_validated,
            "schema_validation_errors": self.schema_validation_errors,
            "timestamp_boundary_errors": self.timestamp_boundary_errors,
            "monotonicity_errors": self.monotonicity_errors,
            "duplicate_agg_trade_id_errors": self.duplicate_agg_trade_id_errors,
            "path_layout_error": self.path_layout_error,
            "decompression_error": self.decompression_error,
            "csv_member_error": self.csv_member_error,
            "sidecar_format_error": self.sidecar_format_error,
            "sha256_mismatch": self.sha256_mismatch,
            "companion_sha_mismatch": self.companion_sha_mismatch,
            "sidecar_sha_mismatch": self.sidecar_sha_mismatch,
            "status": self.status,
            "first_failure_reason": self.first_failure_reason,
        }


def _hash_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _check_zip_basename_layout(date_str: str, rel_zip: str, result: PerFileResult) -> None:
    """Record a path-layout error on *result* if the zip path is off-pattern."""
    if not rel_zip.startswith(_RAW_LAYOUT_PREFIX):
        result.path_layout_error = (
            f"local_zip_path does not start with expected layout prefix "
            f"{_RAW_LAYOUT_PREFIX!r}: {rel_zip!r}"
        )
        return
    base = rel_zip.rsplit("/", 1)[-1]
    m = _ZIP_BASENAME_RE.match(base)
    if m is None:
        result.path_layout_error = (
            f"zip basename does not match BTCUSDT-aggTrades-YYYY-MM-DD.zip: {base!r}"
        )
        return
    if m.group(1) != date_str:
        result.path_layout_error = (
            f"zip basename date {m.group(1)!r} != inventory date {date_str!r}"
        )
        return
    yyyy, mm = date_str[:4], date_str[5:7]
    expected_dir = f"{_RAW_LAYOUT_PREFIX}{yyyy}/{mm}/{base}"
    if rel_zip != expected_dir:
        result.path_layout_error = f"zip path {rel_zip!r} != expected {expected_dir!r}"


def validate_one_file(
    entry: Mapping[str, Any],
    *,
    sample_head: int,
    sample_tail: int,
) -> PerFileResult:
    """Hash, integrity-check, structurally scan, and bounded-sample one ZIP."""
    date_str = entry["date"]
    result = PerFileResult(
        date=date_str,
        local_zip_path=entry["local_zip_path"],
        local_sidecar_path=entry["local_sidecar_path"],
        manifest_sha256=entry["sha256"],
        manifest_companion_sha256=entry.get("sha256_from_companion", ""),
        manifest_size_bytes=entry["size_bytes"],
        manifest_row_count=entry["row_count"],
        manifest_first_trade_time_ms=entry["first_trade_time_ms"],
        manifest_last_trade_time_ms=entry["last_trade_time_ms"],
        manifest_min_agg_trade_id=entry["min_agg_trade_id"],
        manifest_max_agg_trade_id=entry["max_agg_trade_id"],
    )

    # Hard boundary guard: never open a file outside the pre-v002 segment.
    if not is_within_segment(date_str):
        result.path_layout_error = (
            f"date {date_str!r} is outside the pre-v002 segment "
            f"[{DATE_START}, {V002_TERMINAL_START}); file NOT opened "
            "(boundary fail-closed)"
        )
        result.record_failure(result.path_layout_error)
        result.status = "fail"
        return result

    _check_zip_basename_layout(date_str, result.local_zip_path, result)
    if result.path_layout_error is not None:
        result.record_failure(result.path_layout_error)
        result.status = "fail"
        return result

    try:
        zip_path = assert_relative_under_microstructure(
            result.local_zip_path, label=f"local_zip_path[{date_str}]"
        )
        sidecar_path = assert_relative_under_microstructure(
            result.local_sidecar_path, label=f"local_sidecar_path[{date_str}]"
        )
    except GateRuntimeError as exc:
        result.path_layout_error = str(exc)
        result.record_failure(str(exc))
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

    try:
        result.zip_size_bytes = zip_path.stat().st_size
        result.computed_sha256 = _hash_file_sha256(zip_path)
    except OSError as exc:
        result.decompression_error = (
            f"failed to stat/hash zip {zip_path}: {type(exc).__name__}: {exc}"
        )
        result.record_failure(result.decompression_error)
        result.status = "fail"
        return result

    if result.zip_size_bytes != result.manifest_size_bytes:
        result.record_failure(
            f"zip_size_bytes={result.zip_size_bytes} != manifest "
            f"size_bytes={result.manifest_size_bytes}"
        )
    if result.computed_sha256 != result.manifest_sha256:
        result.sha256_mismatch = True
        result.record_failure(
            f"computed sha256={result.computed_sha256} != manifest sha256={result.manifest_sha256}"
        )
    if (
        result.manifest_companion_sha256
        and result.computed_sha256 != result.manifest_companion_sha256
    ):
        result.companion_sha_mismatch = True
        result.record_failure(
            f"computed sha256={result.computed_sha256} != manifest "
            f"sha256_from_companion={result.manifest_companion_sha256}"
        )

    # Sidecar parse + match.
    try:
        sidecar_text = sidecar_path.read_bytes().decode("utf-8")
        sidecar_sha, sidecar_basename = parse_canonical_sidecar(sidecar_text)
    except (OSError, GateRuntimeError) as exc:
        result.sidecar_format_error = f"sidecar parse failed: {type(exc).__name__}: {exc}"
        result.record_failure(result.sidecar_format_error)
        result.status = "fail"
        return result
    result.sidecar_sha256_value = sidecar_sha
    if sidecar_basename != zip_path.name:
        result.sidecar_format_error = (
            f"sidecar basename {sidecar_basename!r} does not match zip basename {zip_path.name!r}"
        )
        result.record_failure(result.sidecar_format_error)
    if sidecar_sha != result.computed_sha256:
        result.sidecar_sha_mismatch = True
        result.record_failure(
            f"sidecar sha256={sidecar_sha} != computed sha256={result.computed_sha256}"
        )

    # Decompress + full structural scan + bounded payload sample.
    day_start_ms, day_end_ms = utc_day_window_ms(date_str)
    try:
        with zipfile.ZipFile(zip_path) as zf:
            bad = zf.testzip()
            if bad is not None:
                result.decompression_error = f"testzip() reported corrupt member: {bad!r}"
                result.record_failure(result.decompression_error)
                result.status = "fail"
                return result
            names = [n for n in zf.namelist() if not n.endswith("/")]
            csv_members = [n for n in names if n.lower().endswith(".csv")]
            if not csv_members and len(names) == 1:
                csv_members = names
            if len(csv_members) != 1:
                result.csv_member_error = (
                    f"ZIP must contain exactly one CSV member; got {csv_members!r} of {names!r}"
                )
                result.record_failure(result.csv_member_error)
                result.status = "fail"
                return result
            member = csv_members[0]

            mapping: dict[str, int] | None = None
            row_count = 0
            first_t: int | None = None
            last_t: int | None = None
            min_a: int | None = None
            max_a: int | None = None
            prev_a: int | None = None
            # We do not know the total data-row count up-front, so the
            # tail sample is collected via a fixed-size ring buffer of the
            # last ``sample_tail`` rows and validated after the scan.
            tail_buffer: list[tuple[Sequence[str], dict[str, int] | None]] = []

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
                                continue  # header row, not data
                        # Lightweight structural parse (full pass).
                        try:
                            agg_id = int(row[0] if mapping is None else row[mapping["a"]])
                            trade_time = int(row[5] if mapping is None else row[mapping["T"]])
                        except (ValueError, IndexError, KeyError) as exc:
                            result.schema_validation_errors += 1
                            result.record_failure(
                                f"row {row_count} structural parse failed: "
                                f"{type(exc).__name__}: {exc}"
                            )
                            result.status = "fail"
                            return result
                        if not (day_start_ms <= trade_time < day_end_ms):
                            result.timestamp_boundary_errors += 1
                            result.record_failure(
                                f"row {row_count} trade_time {trade_time} "
                                f"outside UTC day {date_str} "
                                f"[{day_start_ms}, {day_end_ms})"
                            )
                            result.status = "fail"
                            return result
                        if prev_a is not None:
                            if agg_id == prev_a:
                                result.duplicate_agg_trade_id_errors += 1
                                result.record_failure(
                                    f"row {row_count} duplicate agg_trade_id={agg_id}"
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
                        if first_t is None:
                            first_t = trade_time
                            min_a = agg_id
                            max_a = agg_id
                        last_t = trade_time
                        if min_a is None or agg_id < min_a:
                            min_a = agg_id
                        if max_a is None or agg_id > max_a:
                            max_a = agg_id

                        # Bounded Phase 4ax full-schema validation: head.
                        if row_count < sample_head:
                            _sample_validate(row, mapping, row_count, result)
                            if result.status == "fail":
                                return result
                        # Tail ring buffer.
                        if sample_tail > 0:
                            tail_buffer.append((row, mapping))
                            if len(tail_buffer) > sample_tail:
                                tail_buffer.pop(0)
                        row_count += 1
            except (zipfile.BadZipFile, OSError, EOFError) as exc:
                result.decompression_error = f"decompression failed: {type(exc).__name__}: {exc}"
                result.record_failure(result.decompression_error)
                result.status = "fail"
                return result

            # Validate tail rows that were not already validated as head.
            tail_start_index = row_count - len(tail_buffer)
            for offset, (row, mp) in enumerate(tail_buffer):
                idx = tail_start_index + offset
                if idx < sample_head:
                    continue  # already validated in the head window
                _sample_validate(row, mp, idx, result)
                if result.status == "fail":
                    return result

            result.computed_row_count = row_count
            result.computed_first_trade_time_ms = first_t
            result.computed_last_trade_time_ms = last_t
            result.computed_min_agg_trade_id = min_a
            result.computed_max_agg_trade_id = max_a
    except zipfile.BadZipFile as exc:
        result.decompression_error = f"BadZipFile opening {zip_path}: {exc}"
        result.record_failure(result.decompression_error)
        result.status = "fail"
        return result

    for label, computed, manifest_val in (
        ("row_count", result.computed_row_count, result.manifest_row_count),
        (
            "first_trade_time_ms",
            result.computed_first_trade_time_ms,
            result.manifest_first_trade_time_ms,
        ),
        (
            "last_trade_time_ms",
            result.computed_last_trade_time_ms,
            result.manifest_last_trade_time_ms,
        ),
        (
            "min_agg_trade_id",
            result.computed_min_agg_trade_id,
            result.manifest_min_agg_trade_id,
        ),
        (
            "max_agg_trade_id",
            result.computed_max_agg_trade_id,
            result.manifest_max_agg_trade_id,
        ),
    ):
        if computed != manifest_val:
            result.record_failure(f"{label} computed={computed} manifest={manifest_val}")

    result.status = "fail" if result.has_critical_failure() else "pass"
    return result


def _sample_validate(
    row: Sequence[str],
    mapping: dict[str, int] | None,
    row_index: int,
    result: PerFileResult,
) -> None:
    """Run full Phase 4ax ``validate_aggtrade_payload`` on one sampled row."""
    try:
        payload = _row_to_payload(row, mapping)
        validate_aggtrade_payload(payload)
    except (AggTradeValidationError, GateRuntimeError) as exc:
        result.schema_validation_errors += 1
        result.record_failure(
            f"sampled row {row_index} schema validation failed: {type(exc).__name__}: {exc}"
        )
        result.status = "fail"
        return
    result.rows_sampled_validated += 1


# ----------------------------------------------------------------------- #
# Manifest schema integrity
# ----------------------------------------------------------------------- #

REQUIRED_MANIFEST_KEYS: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "schema_version",
    "segment_label",
    "symbol_list",
    "data_family",
    "market",
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
    "existing_v002_terminal_window",
    "existing_v002_sealed_test_split",
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


# ----------------------------------------------------------------------- #
# Git helpers
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


def _git_check_ignore(paths: Iterable[str]) -> dict[str, bool]:
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
        "platform_machine": platform.machine(),
        "platform_python_version": platform.python_version(),
    }


# ----------------------------------------------------------------------- #
# Check helpers
# ----------------------------------------------------------------------- #


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
    return {
        "check_id": check_id,
        "check_name": check_id,
        "status": status,
        "severity": severity or CHECK_SEVERITY.get(check_id, "critical"),
        "summary": summary,
        "expected": expected,
        "observed": observed,
        "details": list(details),
    }


def _check_status_pass(check: Mapping[str, Any]) -> bool:
    return check["status"] in ("pass", "not_applicable")


# ----------------------------------------------------------------------- #
# Gate orchestrator
# ----------------------------------------------------------------------- #


def run_gate(
    *,
    output_root: Path,
    sample_head: int = DEFAULT_SAMPLE_HEAD,
    sample_tail: int = DEFAULT_SAMPLE_TAIL,
    log_progress: bool = False,
) -> int:
    """Run the Phase 4bn-K pre-v002 raw archive eligibility gate."""
    run_started_at_unix_ms = int(time.time() * 1000)
    wall_clock_start = time.monotonic()
    head_sha = _git_head_sha()
    base_sha = head_sha

    print(f"[{PHASE_NAME}] starting gate; base_commit_sha={base_sha or '<unknown>'}")
    print(
        f"[{PHASE_NAME}] segment={SEGMENT_LABEL} dataset="
        f"{DATASET_FAMILY}__{DATASET_VERSION} symbol={list(SYMBOL_LIST)} "
        f"window={DATE_START}..{DATE_END}"
    )

    checks: list[dict[str, Any]] = []
    failure_reasons: list[str] = []
    error_reasons: list[str] = []
    per_file_summaries: list[dict[str, Any]] = []

    # 1. manifest + log file integrity ---------------------------------- #
    try:
        assert_path_under_microstructure(RAW_MANIFEST_PATH, label="segment manifest")
        assert_path_under_microstructure(ACQUISITION_LOG_PATH, label="acquisition log")
    except CanonicalPathError as exc:
        error_reasons.append(f"path discipline failure: {exc}")
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
            recomputed_manifest_sha="",
            recomputed_log_sha="",
            recomputed_totals=None,
            aggregate_summary=None,
        )

    manifest_sha = _hash_file_sha256(RAW_MANIFEST_PATH) if RAW_MANIFEST_PATH.is_file() else ""
    log_sha = _hash_file_sha256(ACQUISITION_LOG_PATH) if ACQUISITION_LOG_PATH.is_file() else ""
    manifest_present = RAW_MANIFEST_PATH.is_file()
    log_present = ACQUISITION_LOG_PATH.is_file()
    manifest_sha_ok = manifest_sha == EXPECTED_MANIFEST_SHA256
    log_sha_ok = log_sha == EXPECTED_ACQUISITION_LOG_SHA256

    checks.append(
        _make_check(
            "manifest_file_integrity",
            status="pass" if (manifest_present and manifest_sha_ok) else "fail",
            summary=(
                "segment manifest present with expected SHA256"
                if (manifest_present and manifest_sha_ok)
                else "segment manifest missing or SHA256 mismatch"
            ),
            expected={"path": RAW_MANIFEST_PATH.as_posix(), "sha256": EXPECTED_MANIFEST_SHA256},
            observed={"present": manifest_present, "sha256": manifest_sha},
        )
    )
    if not (manifest_present and manifest_sha_ok):
        failure_reasons.append("segment manifest missing or SHA256 mismatch")

    checks.append(
        _make_check(
            "acquisition_log_integrity",
            status="pass" if (log_present and log_sha_ok) else "fail",
            summary=(
                "acquisition log present with expected SHA256"
                if (log_present and log_sha_ok)
                else "acquisition log missing or SHA256 mismatch"
            ),
            expected={
                "path": ACQUISITION_LOG_PATH.as_posix(),
                "sha256": EXPECTED_ACQUISITION_LOG_SHA256,
            },
            observed={"present": log_present, "sha256": log_sha},
        )
    )
    if not (log_present and log_sha_ok):
        failure_reasons.append("acquisition log missing or SHA256 mismatch")

    # 2. manifest + log sidecar format --------------------------------- #
    sidecar_errors: list[str] = []

    def _parse_named_sidecar(
        sidecar_path: Path, expected_basename: str, expected_sha: str
    ) -> dict[str, Any]:
        obs: dict[str, Any] = {"path": sidecar_path.as_posix(), "present": sidecar_path.is_file()}
        if not sidecar_path.is_file():
            obs["error"] = "sidecar not present"
            sidecar_errors.append(f"{expected_basename}: sidecar not present")
            return obs
        try:
            text = sidecar_path.read_bytes().decode("utf-8")
            sha_hex, basename = parse_canonical_sidecar(text)
        except (OSError, UnicodeDecodeError, GateRuntimeError) as exc:
            obs["error"] = f"{type(exc).__name__}: {exc}"
            sidecar_errors.append(f"{expected_basename}: {exc}")
            return obs
        obs["sha256_in_sidecar"] = sha_hex
        obs["basename_in_sidecar"] = basename
        if basename != expected_basename:
            obs["error"] = f"basename {basename!r} != {expected_basename!r}"
            sidecar_errors.append(obs["error"])
        if sha_hex != expected_sha:
            obs["error"] = f"sidecar sha {sha_hex!r} != target {expected_sha!r}"
            sidecar_errors.append(obs["error"])
        return obs

    manifest_sidecar_obs = _parse_named_sidecar(
        RAW_MANIFEST_SIDECAR_PATH, RAW_MANIFEST_PATH.name, manifest_sha
    )
    log_sidecar_obs = _parse_named_sidecar(
        ACQUISITION_LOG_SIDECAR_PATH, ACQUISITION_LOG_PATH.name, log_sha
    )
    checks.append(
        _make_check(
            "sidecar_format_integrity",
            status="pass" if not sidecar_errors else "fail",
            summary=(
                "manifest + log sidecars canonical and match target SHAs"
                if not sidecar_errors
                else "manifest/log sidecar issues detected"
            ),
            expected={"format": "<sha256>  <basename>\\n"},
            observed={
                "manifest_sidecar": manifest_sidecar_obs,
                "log_sidecar": log_sidecar_obs,
                "errors": sidecar_errors,
            },
        )
    )
    failure_reasons.extend(sidecar_errors)

    # If manifest/log integrity failed, fail closed now.
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

    # 3. load manifest + log JSON -------------------------------------- #
    try:
        manifest = json.loads(RAW_MANIFEST_PATH.read_text(encoding="utf-8"))
        log_obj = json.loads(ACQUISITION_LOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error_reasons.append(f"failed to parse manifest/log JSON: {type(exc).__name__}: {exc}")
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

    inventory = manifest.get("per_file_inventory", [])

    # 4. gitignore boundary -------------------------------------------- #
    gitignore_obs = _git_check_ignore(
        [
            MICROSTRUCTURE_DIR.as_posix(),
            (MICROSTRUCTURE_DIR / "gate-reports").as_posix(),
            GATE_REPORTS_RAW_DIR.as_posix(),
        ]
    )
    all_ignored = all(gitignore_obs.values())
    checks.append(
        _make_check(
            "gitignore_boundary",
            status="pass" if all_ignored else "fail",
            summary=(
                "data/microstructure/ + gate-reports/raw/ gitignored"
                if all_ignored
                else "one or more paths not gitignored"
            ),
            expected={"all_ignored": True},
            observed=gitignore_obs,
        )
    )
    if not all_ignored:
        failure_reasons.append("gitignore_boundary failed")

    # 5. manifest schema integrity ------------------------------------- #
    schema_errors: list[str] = []
    for key in REQUIRED_MANIFEST_KEYS:
        if key not in manifest:
            schema_errors.append(f"manifest missing key: {key!r}")
    for idx, entry in enumerate(inventory):
        for key in REQUIRED_INVENTORY_KEYS:
            if key not in entry:
                schema_errors.append(f"per_file_inventory[{idx}] missing key: {key!r}")
    checks.append(
        _make_check(
            "manifest_schema_integrity",
            status="pass" if not schema_errors else "fail",
            summary=(
                "manifest + inventory carry all required keys"
                if not schema_errors
                else "manifest/inventory schema gaps"
            ),
            expected={
                "required_manifest_keys": len(REQUIRED_MANIFEST_KEYS),
                "required_inventory_keys": len(REQUIRED_INVENTORY_KEYS),
            },
            observed={"errors": schema_errors[:20], "error_count": len(schema_errors)},
        )
    )
    failure_reasons.extend(schema_errors[:10])

    # 6. scope lock ---------------------------------------------------- #
    scope_observed = {
        "dataset_family": manifest.get("dataset_family"),
        "dataset_version": manifest.get("dataset_version"),
        "schema_version": manifest.get("schema_version"),
        "segment_label": manifest.get("segment_label"),
        "data_family": manifest.get("data_family"),
        "market": manifest.get("market"),
        "date_start": manifest.get("date_start"),
        "date_end": manifest.get("date_end"),
        "date_count": manifest.get("date_count"),
        "expected_file_count": manifest.get("expected_file_count"),
    }
    scope_expected = {
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "schema_version": SCHEMA_VERSION,
        "segment_label": SEGMENT_LABEL,
        "data_family": DATA_FAMILY,
        "market": MARKET,
        "date_start": DATE_START,
        "date_end": DATE_END,
        "date_count": DATE_COUNT,
        "expected_file_count": EXPECTED_FILE_COUNT,
    }
    scope_ok = scope_observed == scope_expected
    checks.append(
        _make_check(
            "scope_lock",
            status="pass" if scope_ok else "fail",
            summary=(
                "manifest scope matches Phase 4bn-K locked scope"
                if scope_ok
                else "manifest scope mismatch"
            ),
            expected=scope_expected,
            observed=scope_observed,
        )
    )
    if not scope_ok:
        failure_reasons.append("manifest scope does not match Phase 4bn-K locked scope")

    # 7. symbol / family scope ----------------------------------------- #
    sym_ok = (
        manifest.get("symbol_list") == list(SYMBOL_LIST)
        and manifest.get("data_family") == DATA_FAMILY
        and manifest.get("market") == MARKET
    )
    checks.append(
        _make_check(
            "symbol_family_scope",
            status="pass" if sym_ok else "fail",
            summary=(
                "BTCUSDT / aggTrades / binance_usdm_futures only"
                if sym_ok
                else "symbol/family/market scope mismatch"
            ),
            expected={
                "symbol_list": list(SYMBOL_LIST),
                "data_family": DATA_FAMILY,
                "market": MARKET,
            },
            observed={
                "symbol_list": manifest.get("symbol_list"),
                "data_family": manifest.get("data_family"),
                "market": manifest.get("market"),
            },
        )
    )
    if not sym_ok:
        failure_reasons.append("symbol/family/market scope mismatch")

    # 8. scope-token denylist (across all manifest paths) -------------- #
    denylist_hits: list[str] = []
    for idx, entry in enumerate(inventory):
        for k in ("local_zip_path", "local_sidecar_path", "expected_url", "expected_checksum_url"):
            v = str(entry.get(k, ""))
            low = v.lower()
            for tok in _SCOPE_DENYLIST:
                if tok in low:
                    denylist_hits.append(f"inventory[{idx}].{k} contains {tok!r}: {v!r}")
    checks.append(
        _make_check(
            "scope_token_denylist",
            status="pass" if not denylist_hits else "fail",
            summary=(
                "no out-of-scope tokens (ethusdt/markprice/spot/orderbook/...) in paths"
                if not denylist_hits
                else "out-of-scope token detected in manifest paths"
            ),
            expected={"denylist": list(_SCOPE_DENYLIST), "hits": 0},
            observed={"hits": denylist_hits[:10], "hit_count": len(denylist_hits)},
        )
    )
    failure_reasons.extend(denylist_hits[:10])

    # 9. segment boundary date guard + date list integrity ------------- #
    inv_dates = [e.get("date") for e in inventory]
    out_of_segment = [d for d in inv_dates if not (isinstance(d, str) and is_within_segment(d))]
    ge_terminal = [d for d in inv_dates if isinstance(d, str) and d >= V002_TERMINAL_START]
    checks.append(
        _make_check(
            "segment_boundary_date_guard",
            status="pass" if (not out_of_segment and not ge_terminal) else "fail",
            summary=(
                "every inventory date is within [2024-03-01, 2024-12-01); "
                "no date touches the v002 terminal window"
                if (not out_of_segment and not ge_terminal)
                else "inventory contains a date outside the pre-v002 segment"
            ),
            expected={"segment": f"[{DATE_START}, {V002_TERMINAL_START})", "dates_ge_terminal": 0},
            observed={"out_of_segment": out_of_segment[:10], "dates_ge_terminal": ge_terminal[:10]},
        )
    )
    if out_of_segment or ge_terminal:
        failure_reasons.append("inventory contains date(s) outside the pre-v002 segment")

    generated_dates = generate_expected_date_list(DATE_START, DATE_END)
    manifest_date_list = manifest.get("date_list")
    inv_dates_sorted = sorted(d for d in inv_dates if isinstance(d, str))
    dup_dates = sorted({d for d in inv_dates if inv_dates.count(d) > 1})
    date_list_ok = (
        isinstance(manifest_date_list, list)
        and list(manifest_date_list) == generated_dates
        and inv_dates_sorted == generated_dates
        and len(inv_dates) == DATE_COUNT
        and not dup_dates
    )
    checks.append(
        _make_check(
            "date_list_integrity",
            status="pass" if date_list_ok else "fail",
            summary=(
                f"date_list + inventory dates equal the contiguous {DATE_COUNT}-day list"
                if date_list_ok
                else "date_list / inventory date coverage mismatch"
            ),
            expected={"date_count": DATE_COUNT, "date_start": DATE_START, "date_end": DATE_END},
            observed={
                "manifest_date_list_len": len(manifest_date_list)
                if isinstance(manifest_date_list, list)
                else None,
                "inventory_len": len(inv_dates),
                "duplicate_dates": dup_dates[:10],
                "missing_dates": [d for d in generated_dates if d not in set(inv_dates_sorted)][
                    :10
                ],
            },
        )
    )
    if not date_list_ok:
        failure_reasons.append("date_list / inventory date coverage mismatch")

    # 10. per-file path layout ----------------------------------------- #
    layout_errors: list[str] = []
    for entry in inventory:
        d = entry.get("date", "")
        rel = str(entry.get("local_zip_path", ""))
        tmp = PerFileResult(date=d, local_zip_path=rel, local_sidecar_path="")
        if isinstance(d, str) and d:
            _check_zip_basename_layout(d, rel, tmp)
        if tmp.path_layout_error:
            layout_errors.append(tmp.path_layout_error)
    checks.append(
        _make_check(
            "per_file_path_layout",
            status="pass" if not layout_errors else "fail",
            summary=(
                "all paths follow .../BTCUSDT/{YYYY}/{MM}/BTCUSDT-aggTrades-{date}.zip"
                if not layout_errors
                else "per-file path layout violations"
            ),
            expected={"prefix": _RAW_LAYOUT_PREFIX, "basename": "BTCUSDT-aggTrades-YYYY-MM-DD.zip"},
            observed={"errors": layout_errors[:10], "error_count": len(layout_errors)},
        )
    )
    failure_reasons.extend(layout_errors[:10])

    # 11. no unexpected statuses --------------------------------------- #
    bad_status = [
        f"{e.get('date')}: {e.get('status')}"
        for e in inventory
        if e.get("status") != "acquired_verified"
    ]
    checks.append(
        _make_check(
            "no_unexpected_statuses",
            status="pass" if not bad_status else "fail",
            summary=(
                "every inventory entry status == 'acquired_verified'"
                if not bad_status
                else "unexpected inventory status detected"
            ),
            expected={"status": "acquired_verified"},
            observed={"unexpected": bad_status[:10], "unexpected_count": len(bad_status)},
        )
    )
    failure_reasons.extend(bad_status[:5])

    # 12. manifest eligibility state ----------------------------------- #
    test_rows_loaded = manifest.get("test_rows_loaded", None)
    elig_ok = (
        manifest.get("research_eligible") is False
        and manifest.get("eligibility_gate_status") == "pending"
        and manifest.get("test_holdout_touched") is False
        and (test_rows_loaded in (0, None))
    )
    checks.append(
        _make_check(
            "manifest_eligibility_state",
            status="pass" if elig_ok else "fail",
            summary=(
                "manifest is non-eligible (research_eligible=false, "
                "eligibility_gate_status=pending, test_holdout_touched=false)"
                if elig_ok
                else "manifest eligibility state unexpected"
            ),
            expected={
                "research_eligible": False,
                "eligibility_gate_status": "pending",
                "test_holdout_touched": False,
                "test_rows_loaded": "0 or absent",
            },
            observed={
                "research_eligible": manifest.get("research_eligible"),
                "eligibility_gate_status": manifest.get("eligibility_gate_status"),
                "test_holdout_touched": manifest.get("test_holdout_touched"),
                "test_rows_loaded": test_rows_loaded,
            },
        )
    )
    if not elig_ok:
        failure_reasons.append("manifest eligibility state unexpected")

    # 13. v002 terminal window by-reference preservation --------------- #
    tw = manifest.get("existing_v002_terminal_window", {})
    tw_ok = (
        isinstance(tw, dict)
        and tw.get("read") is False
        and tw.get("redownloaded") is False
        and tw.get("overwritten") is False
        and tw.get("start") == V002_TERMINAL_START
        and tw.get("end") == V002_TERMINAL_END
    )
    checks.append(
        _make_check(
            "v002_terminal_window_by_reference_preservation",
            status="pass" if tw_ok else "fail",
            summary=(
                "manifest records v002 terminal window not read / not "
                "redownloaded / not overwritten"
                if tw_ok
                else "v002 terminal-window preservation block unexpected"
            ),
            expected={
                "read": False,
                "redownloaded": False,
                "overwritten": False,
                "start": V002_TERMINAL_START,
                "end": V002_TERMINAL_END,
            },
            observed=tw if isinstance(tw, dict) else {"value": tw},
        )
    )
    if not tw_ok:
        failure_reasons.append("v002 terminal-window preservation block unexpected")

    # 14. sealed test split untouched ---------------------------------- #
    sp = manifest.get("existing_v002_sealed_test_split", {})
    sp_ok = (
        isinstance(sp, dict)
        and sp.get("touched") is False
        and sp.get("start") == SEALED_TEST_SPLIT_START
        and sp.get("end") == SEALED_TEST_SPLIT_END
    )
    checks.append(
        _make_check(
            "sealed_test_split_untouched",
            status="pass" if sp_ok else "fail",
            summary=(
                "manifest records sealed v002 test split (2025-02-14..02-28) untouched"
                if sp_ok
                else "sealed test-split block unexpected"
            ),
            expected={
                "touched": False,
                "start": SEALED_TEST_SPLIT_START,
                "end": SEALED_TEST_SPLIT_END,
            },
            observed=sp if isinstance(sp, dict) else {"value": sp},
        )
    )
    if not sp_ok:
        failure_reasons.append("sealed test-split block unexpected")

    # 15. per-file validation loop ------------------------------------- #
    print(
        f"[{PHASE_NAME}] validating {len(inventory)} archives "
        f"(full sha256 + testzip + structural scan + bounded sample "
        f"head={sample_head}/tail={sample_tail}) ..."
    )
    recomputed_total_size = 0
    recomputed_total_rows = 0
    rows_sampled_total = 0
    schema_err_total = 0
    boundary_err_total = 0
    monotonic_err_total = 0
    dup_err_total = 0
    file_fail_count = 0
    prev_max_a: int | None = None
    prev_date: str | None = None
    adjacent_overlap_errors: list[str] = []
    sha_mismatch_count = 0
    companion_mismatch_count = 0
    sidecar_mismatch_count = 0
    zip_corrupt_count = 0
    path_layout_fail_count = 0

    for i, entry in enumerate(sorted(inventory, key=lambda e: e.get("date", ""))):
        r = validate_one_file(entry, sample_head=sample_head, sample_tail=sample_tail)
        per_file_summaries.append(r.to_summary())
        if r.zip_size_bytes is not None:
            recomputed_total_size += r.zip_size_bytes
        if r.computed_row_count is not None:
            recomputed_total_rows += r.computed_row_count
        rows_sampled_total += r.rows_sampled_validated
        schema_err_total += r.schema_validation_errors
        boundary_err_total += r.timestamp_boundary_errors
        monotonic_err_total += r.monotonicity_errors
        dup_err_total += r.duplicate_agg_trade_id_errors
        if r.sha256_mismatch:
            sha_mismatch_count += 1
        if r.companion_sha_mismatch:
            companion_mismatch_count += 1
        if r.sidecar_sha_mismatch or r.sidecar_format_error:
            sidecar_mismatch_count += 1
        if r.decompression_error or r.csv_member_error:
            zip_corrupt_count += 1
        if r.path_layout_error:
            path_layout_fail_count += 1
        # adjacent-date agg-id non-overlap
        if (
            prev_max_a is not None
            and r.computed_min_agg_trade_id is not None
            and r.computed_min_agg_trade_id <= prev_max_a
        ):
            adjacent_overlap_errors.append(
                f"{prev_date}->{r.date}: min_agg_id {r.computed_min_agg_trade_id} "
                f"<= prev max_agg_id {prev_max_a}"
            )
        if r.computed_max_agg_trade_id is not None:
            prev_max_a = r.computed_max_agg_trade_id
            prev_date = r.date
        if r.status != "pass":
            file_fail_count += 1
            if r.first_failure_reason:
                failure_reasons.append(f"{r.date}: {r.first_failure_reason}")
        if log_progress and (i + 1) % 25 == 0:
            print(f"[{PHASE_NAME}]   ... {i + 1}/{len(inventory)} archives validated")

    # Per-file aggregate checks.
    checks.append(
        _make_check(
            "raw_zip_existence",
            status="pass" if zip_corrupt_count == 0 and path_layout_fail_count == 0 else "fail",
            summary="all recorded raw zips exist and open",
            expected={"missing_or_unopenable": 0},
            observed={
                "decompression_or_member_errors": zip_corrupt_count,
                "path_layout_errors": path_layout_fail_count,
            },
        )
    )
    checks.append(
        _make_check(
            "raw_zip_sha256_integrity",
            status="pass" if sha_mismatch_count == 0 and companion_mismatch_count == 0 else "fail",
            summary="every raw zip SHA256 matches manifest sha256 + sha256_from_companion",
            expected={"sha256_mismatches": 0, "companion_mismatches": 0},
            observed={
                "sha256_mismatches": sha_mismatch_count,
                "companion_mismatches": companion_mismatch_count,
            },
        )
    )
    checks.append(
        _make_check(
            "raw_zip_sidecar_integrity",
            status="pass" if sidecar_mismatch_count == 0 else "fail",
            summary="every raw zip has a canonical .sha256 sidecar matching its hash",
            expected={"sidecar_errors": 0},
            observed={"sidecar_errors": sidecar_mismatch_count},
        )
    )
    checks.append(
        _make_check(
            "zip_decompression_integrity",
            status="pass" if zip_corrupt_count == 0 else "fail",
            summary="zipfile.testzip() reported no corruption on any archive",
            expected={"corrupt_archives": 0},
            observed={"corrupt_or_member_errors": zip_corrupt_count},
        )
    )
    checks.append(
        _make_check(
            "single_csv_member_integrity",
            status="pass" if zip_corrupt_count == 0 else "fail",
            summary="each archive contains exactly one CSV member",
            expected={"member_errors": 0},
            observed={"member_or_decompression_errors": zip_corrupt_count},
        )
    )
    checks.append(
        _make_check(
            "bounded_row_sample_schema_validation",
            status="pass" if schema_err_total == 0 else "fail",
            summary=(
                f"bounded Phase 4ax row-sample (head {sample_head} + tail {sample_tail} per "
                f"archive) validated headerless order a,p,q,f,l,T,m; types; timestamps"
            ),
            expected={"schema_validation_errors": 0},
            observed={
                "schema_validation_errors": schema_err_total,
                "rows_sampled_validated": rows_sampled_total,
            },
        )
    )
    checks.append(
        _make_check(
            "per_file_row_count_consistency",
            status="pass" if file_fail_count == 0 else "fail",
            summary="recomputed per-file row counts equal manifest row_count",
            expected={"per_file_failures": 0},
            observed={"per_file_failures": file_fail_count},
        )
    )
    checks.append(
        _make_check(
            "per_file_time_bounds_consistency",
            status="pass" if file_fail_count == 0 else "fail",
            summary="recomputed first/last trade time + min/max agg-id equal manifest",
            expected={"per_file_failures": 0},
            observed={"per_file_failures": file_fail_count},
        )
    )
    checks.append(
        _make_check(
            "utc_day_boundary_integrity",
            status="pass" if boundary_err_total == 0 else "fail",
            summary="every trade timestamp falls within its UTC day window",
            expected={"boundary_errors": 0},
            observed={"boundary_errors": boundary_err_total},
        )
    )
    checks.append(
        _make_check(
            "agg_trade_id_monotonicity_within_file",
            status="pass" if (monotonic_err_total == 0 and dup_err_total == 0) else "fail",
            summary="aggregate-trade-id strictly increasing within each archive",
            expected={"monotonicity_errors": 0, "duplicate_errors": 0},
            observed={
                "monotonicity_errors": monotonic_err_total,
                "duplicate_errors": dup_err_total,
            },
        )
    )
    checks.append(
        _make_check(
            "agg_trade_id_overlap_absence_across_adjacent_dates",
            status="pass" if not adjacent_overlap_errors else "fail",
            summary="aggregate-trade-id ranges do not overlap across adjacent dates",
            expected={"overlap_errors": 0},
            observed={
                "overlap_errors": adjacent_overlap_errors[:10],
                "overlap_count": len(adjacent_overlap_errors),
            },
        )
    )
    failure_reasons.extend(adjacent_overlap_errors[:5])

    # 16. aggregate counts + footprint --------------------------------- #
    file_count = len(inventory)
    sidecar_count = sum(
        1
        for e in inventory
        if (DATA_DIR / e.get("local_sidecar_path", "")).is_file()
        and is_within_segment(str(e.get("date", "")))
    )
    rowcount_ok = (
        recomputed_total_rows == manifest.get("total_row_count") == EXPECTED_TOTAL_ROW_COUNT
    )
    checks.append(
        _make_check(
            "total_row_count_consistency",
            status="pass" if rowcount_ok else "fail",
            summary=f"recomputed total row count == manifest == {EXPECTED_TOTAL_ROW_COUNT}",
            expected={
                "manifest_total_row_count": manifest.get("total_row_count"),
                "phase_4bn_j_r2_expected": EXPECTED_TOTAL_ROW_COUNT,
            },
            observed={"recomputed_total_row_count": recomputed_total_rows},
        )
    )
    if not rowcount_ok:
        failure_reasons.append(
            f"total_row_count mismatch recomputed={recomputed_total_rows} "
            f"manifest={manifest.get('total_row_count')} expected={EXPECTED_TOTAL_ROW_COUNT}"
        )
    sizes_ok = (
        recomputed_total_size == manifest.get("total_size_bytes") == EXPECTED_TOTAL_SIZE_BYTES
    )
    checks.append(
        _make_check(
            "total_size_bytes_consistency",
            status="pass" if sizes_ok else "fail",
            summary=f"recomputed total size == manifest == {EXPECTED_TOTAL_SIZE_BYTES} bytes",
            expected={
                "manifest_total_size_bytes": manifest.get("total_size_bytes"),
                "phase_4bn_j_r2_expected": EXPECTED_TOTAL_SIZE_BYTES,
            },
            observed={"recomputed_total_size_bytes": recomputed_total_size},
        )
    )
    if not sizes_ok:
        failure_reasons.append(
            f"total_size_bytes mismatch recomputed={recomputed_total_size} "
            f"manifest={manifest.get('total_size_bytes')} expected={EXPECTED_TOTAL_SIZE_BYTES}"
        )
    count_ok = (
        file_count == EXPECTED_FILE_COUNT
        and manifest.get("acquired_file_count") == EXPECTED_FILE_COUNT
    )
    checks.append(
        _make_check(
            "archive_count_consistency",
            status="pass" if count_ok else "fail",
            summary=f"archive count == {EXPECTED_FILE_COUNT}",
            expected={"expected_file_count": EXPECTED_FILE_COUNT},
            observed={
                "inventory_len": file_count,
                "manifest_acquired_file_count": manifest.get("acquired_file_count"),
            },
        )
    )
    if not count_ok:
        failure_reasons.append(f"archive count != {EXPECTED_FILE_COUNT}")
    sidecar_count_ok = sidecar_count == EXPECTED_FILE_COUNT
    checks.append(
        _make_check(
            "sidecar_count_consistency",
            status="pass" if sidecar_count_ok else "fail",
            summary=f"sidecar count == {EXPECTED_FILE_COUNT}",
            expected={"expected_sidecar_count": EXPECTED_FILE_COUNT},
            observed={"sidecar_count": sidecar_count},
        )
    )
    if not sidecar_count_ok:
        failure_reasons.append(f"sidecar count != {EXPECTED_FILE_COUNT}")

    # 17. governance constants ----------------------------------------- #
    checks.append(
        _make_check(
            "non_authorizations_preserved",
            status="pass",
            summary="every non-authorization flag is false in this gate report",
            expected=NON_AUTHORIZATIONS,
            observed=NON_AUTHORIZATIONS,
        )
    )
    checks.append(
        _make_check(
            "retained_verdicts_preserved",
            status="pass",
            summary="retained verdict ledger preserved verbatim",
            expected=RETAINED_VERDICT_LEDGER,
            observed=RETAINED_VERDICT_LEDGER,
        )
    )
    checks.append(
        _make_check(
            "project_locks_preserved",
            status="pass",
            summary="project locks preserved verbatim",
            expected=PRESERVED_LOCKS,
            observed=PRESERVED_LOCKS,
        )
    )

    aggregate_summary = {
        "recomputed_file_count": file_count,
        "recomputed_sidecar_count": sidecar_count,
        "recomputed_total_size_bytes": recomputed_total_size,
        "recomputed_total_row_count": recomputed_total_rows,
        "manifest_total_size_bytes": manifest.get("total_size_bytes"),
        "manifest_total_row_count": manifest.get("total_row_count"),
        "manifest_acquired_file_count": manifest.get("acquired_file_count"),
        "acquisition_log_acquired_file_count": log_obj.get("acquired_file_count"),
        "rows_sampled_validated_total": rows_sampled_total,
        "schema_validation_errors_total": schema_err_total,
        "timestamp_boundary_errors_total": boundary_err_total,
        "monotonicity_errors_total": monotonic_err_total,
        "duplicate_agg_trade_id_errors_total": dup_err_total,
        "adjacent_date_overlap_errors_count": len(adjacent_overlap_errors),
        "per_file_failure_count": file_fail_count,
        "sample_head": sample_head,
        "sample_tail": sample_tail,
        "row_validation_mode": (
            "full streaming structural scan (count + UTC boundary + strict "
            "agg-id monotonicity + min/max + first/last) over every row; "
            "bounded Phase 4ax full-schema validate_aggtrade_payload on "
            "head+tail sample per archive"
        ),
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
            "recomputed_total_size_bytes": recomputed_total_size,
            "recomputed_total_row_count": recomputed_total_rows,
        },
        aggregate_summary=aggregate_summary,
    )


# ----------------------------------------------------------------------- #
# Report writing
# ----------------------------------------------------------------------- #


def _gate_result_state(overall_status: str) -> str:
    if overall_status == "pass":
        return "RAW_ARCHIVE_GATE_PASSED__LOCAL_RAW_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
    if overall_status == "fail":
        return "RAW_ARCHIVE_GATE_FAILED__REMAIN_PAUSED"
    return "RAW_ARCHIVE_GATE_PARTIAL__FAIL_CLOSED__REMAIN_PAUSED"


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
    """Write the gate report JSON + paired SHA256 sidecar atomically."""
    gate_result_state = _gate_result_state(overall_status)
    eligibility_after = {
        "pass": "pass_report_level_only__non_eligible",
        "fail": "fail_report_level_only",
        "error": "error_report_level_only",
    }.get(overall_status, "error_report_level_only")

    pass_count = sum(1 for c in checks if c["status"] == "pass")
    fail_count = sum(1 for c in checks if c["status"] == "fail")
    err_count = sum(1 for c in checks if c["status"] == "error")
    na_count = sum(1 for c in checks if c["status"] == "not_applicable")

    microstructure_root = output_root.resolve()
    if microstructure_root.name != "microstructure":
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
        error_reasons.append(f"canonical path derivation failed: {exc}")
        report_path = (
            GATE_REPORTS_RAW_DIR
            / f"{DATASET_FAMILY}__{DATASET_VERSION}__phase-{PHASE_ID}_raw_gate.json"
        )

    try:
        assert_path_under_microstructure(report_path, label="gate report path")
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
        "segment_label": SEGMENT_LABEL,
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "symbol_list": list(SYMBOL_LIST),
        "data_family": DATA_FAMILY,
        "market": MARKET,
        "date_start": DATE_START,
        "date_end": DATE_END,
        "date_count": DATE_COUNT,
        "expected_file_count": EXPECTED_FILE_COUNT,
        "segment_boundary": {
            "pre_v002_segment": f"[{DATE_START}, {V002_TERMINAL_START})",
            "v002_terminal_window_by_reference": f"[{V002_TERMINAL_START}, {V002_TERMINAL_END}]",
            "sealed_test_split_untouched": f"[{SEALED_TEST_SPLIT_START}, {SEALED_TEST_SPLIT_END}]",
        },
        "source_artefacts": {
            "source_manifest_path": RAW_MANIFEST_PATH.as_posix(),
            "source_manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "source_manifest_recomputed_sha256": recomputed_manifest_sha,
            "source_manifest_sidecar_path": RAW_MANIFEST_SIDECAR_PATH.as_posix(),
            "source_acquisition_log_path": ACQUISITION_LOG_PATH.as_posix(),
            "source_acquisition_log_sha256": EXPECTED_ACQUISITION_LOG_SHA256,
            "source_acquisition_log_recomputed_sha256": recomputed_log_sha,
            "source_acquisition_log_sidecar_path": ACQUISITION_LOG_SIDECAR_PATH.as_posix(),
        },
        "overall_status": overall_status,
        "gate_verdict": gate_result_state,
        "gate_result_state": gate_result_state,
        "checks_total": len(checks),
        "checks_passed": pass_count,
        "checks_failed": fail_count,
        "checks_error": err_count,
        "checks_not_applicable": na_count,
        "failure_reasons": failure_reasons,
        "error_reasons": error_reasons,
        "strict_fail_closed": True,
        "segment_non_eligible": True,
        "no_successor_authorization": True,
        "research_eligible_after": False,
        "eligibility_gate_status_after": eligibility_after,
        "manifest_mutated": False,
        "manifest_transition_performed": False,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "checks": checks,
        "per_file_validation_summary": per_file_summaries,
        "aggregate_summary": aggregate_summary,
        "recomputed_totals": recomputed_totals,
        "governance_labels": GOVERNANCE_LABELS,
        "non_authorizations": NON_AUTHORIZATIONS,
        "retained_verdict_ledger": RETAINED_VERDICT_LEDGER,
        "preserved_locks": PRESERVED_LOCKS,
        "created_at_unix_ms": run_started_at_unix_ms,
        "created_at_utc": datetime.fromtimestamp(run_started_at_unix_ms / 1000.0, tz=UTC)
        .isoformat()
        .replace("+00:00", "Z"),
        "base_commit_sha": base_sha,
        "code_commit_sha": head_sha,
        "script_path": Path(__file__).relative_to(_REPO_ROOT).as_posix(),
        "report_path": report_path.as_posix(),
        "report_sidecar_path": sidecar_path.as_posix(),
        "run_wall_clock_seconds": round(wall_clock_seconds, 3),
        "python_version": platform.python_version(),
        "platform_summary": _platform_summary(),
    }

    payload_bytes = (
        json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    if report_path.exists():
        print(
            f"[{PHASE_NAME}] ERROR: refusing to overwrite existing gate report {report_path}",
            file=sys.stderr,
        )
        return 1
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{report_path.name}.", suffix=".tmp", dir=str(report_path.parent)
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
                f"[{PHASE_NAME}] ERROR: refusing to overwrite (race) {report_path}", file=sys.stderr
            )
            return 1
        os.replace(tmp_path, report_path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()

    report_sha = compute_file_sha256(report_path)
    write_paired_sha256_sidecar(
        json_path=report_path, json_sha256_hex=report_sha, refuse_overwrite=True
    )

    print("")
    print(f"[{PHASE_NAME}] gate_result_state:   {gate_result_state}")
    print(f"[{PHASE_NAME}] overall_status:      {overall_status}")
    print(
        f"[{PHASE_NAME}] checks pass/fail/err/na/total: "
        f"{pass_count}/{fail_count}/{err_count}/{na_count}/{len(checks)}"
    )
    if recomputed_totals is not None:
        _rows = recomputed_totals["recomputed_total_row_count"]
        _bytes = recomputed_totals["recomputed_total_size_bytes"]
        print(f"[{PHASE_NAME}] recomputed_total_row_count:  {_rows}")
        print(f"[{PHASE_NAME}] recomputed_total_size_bytes: {_bytes}")
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
        prog="phase4bn_k_validate_pre_v002_raw_archive_gate",
        description="Phase 4bn-K — Expanded Raw Archive Eligibility Gate (pre-v002 segment)",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=MICROSTRUCTURE_DIR,
        help="Microstructure root (must resolve under data/microstructure/).",
    )
    parser.add_argument(
        "--sample-head",
        type=int,
        default=DEFAULT_SAMPLE_HEAD,
        help="Per-archive head rows for bounded Phase 4ax full-schema validation.",
    )
    parser.add_argument(
        "--sample-tail",
        type=int,
        default=DEFAULT_SAMPLE_TAIL,
        help="Per-archive tail rows for bounded Phase 4ax full-schema validation.",
    )
    parser.add_argument("--log-progress", action="store_true", help="Log per-file progress.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print locked scope and exit without reading any data.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.dry_run:
        print(f"[{PHASE_NAME}] DRY-RUN — no files will be read.")
        print(f"  phase_id:        {PHASE_ID}")
        print(f"  segment_label:   {SEGMENT_LABEL}")
        print(f"  dataset:         {DATASET_FAMILY}__{DATASET_VERSION}")
        print(f"  symbol_list:     {list(SYMBOL_LIST)}")
        print(f"  window:          {DATE_START}..{DATE_END} ({DATE_COUNT} dates)")
        print(
            f"  boundary:        any date >= {V002_TERMINAL_START} is rejected, file never opened"
        )
        print(f"  manifest_path:   {RAW_MANIFEST_PATH.as_posix()}")
        print(f"  expected_sha256: {EXPECTED_MANIFEST_SHA256}")
        print(f"  log_path:        {ACQUISITION_LOG_PATH.as_posix()}")
        print(f"  expected_log_sha:{EXPECTED_ACQUISITION_LOG_SHA256}")
        print(f"  expected_rows:   {EXPECTED_TOTAL_ROW_COUNT}")
        print(f"  expected_bytes:  {EXPECTED_TOTAL_SIZE_BYTES}")
        return 0

    output_root: Path = args.output_root
    try:
        assert_path_under_microstructure(output_root, label="--output-root")
    except CanonicalPathError as exc:
        print(f"[{PHASE_NAME}] ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        return run_gate(
            output_root=output_root,
            sample_head=args.sample_head,
            sample_tail=args.sample_tail,
            log_progress=args.log_progress,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[{PHASE_NAME}] UNEXPECTED ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
