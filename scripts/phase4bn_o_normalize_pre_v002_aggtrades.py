"""Phase 4bn-O — Normalization-Only Pre-V002 BTCUSDT aggTrades Segment Execution.

Bounded standalone orchestrator authorised by the Phase 4bn-O
normalization-only execution prompt. It normalises **only** the approved
pre-v002 BTCUSDT Binance USDⓈ-M futures aggTrades raw segment
(275 contiguous UTC dates 2024-03-01 .. 2024-11-30 inclusive;
400,001,695 events; 5,140,686,147 raw bytes) — acquired by Phase 4bn-J-R2
and admitted PASS by the Phase 4bn-K raw-archive eligibility gate — into a
**phase-scoped normalized segment** of the existing v002 normalized family.

The manifest/versioning convention is the one settled by the Phase 4bn-N memo
(``2026-06-04_phase-4bn-n_normalization-manifest-versioning-memo.md`` §10/§11/
§14): a phase-scoped normalized **segment manifest** marked
``segment_label = "pre_v002_segment"`` under ``dataset_version = "v002"``,
written to a **version-suffixed segment directory distinct from the published
``__v002/`` directory**, with full-envelope and v002-terminal/sealed-test
linkage **by reference only**. It is NOT a new ``__vNNN``, NOT v003, and does
NOT mutate the published ``__v002`` normalized family.

The runner:

- reuses the **locked** Phase 4bd primitives unchanged
  (``iter_aggtrade_rows_from_csv``, ``NORMALIZED_SCHEMA_V001``,
  ``normalize_io`` path discipline + atomic zstd Parquet + canonical
  two-space ``.sha256`` sidecars + refuse-overwrite);
- adds only the bounded orchestration this phase requires: pre-v002 segment
  manifest input source; hard date-range / symbol / family guards; the Phase
  4bn-L preflight + budget caps; the §10/§14 segment naming; the §12 segment
  manifest writer;
- performs NO network access, NO credentials, NO ``.env`` / ``.mcp.json`` /
  MCP / Graphify, NO arbitrary source URLs;
- reads ONLY the approved pre-v002 raw inputs (verified by SHA256), NEVER the
  v002 terminal raw window, NEVER sealed-test dates, NEVER the published
  ``__v002`` normalized parquet/manifest;
- writes ONLY local gitignored normalized parquet + canonical sidecars under
  the §14 segment directory plus the §12 segment manifest + sidecar under
  ``data/microstructure/manifests/``; refuses to overwrite any finalised file;
  atomic write-then-rename;
- preserves the locked 19-column ``NORMALIZED_SCHEMA_V001`` verbatim and the
  forbidden-substring column guard;
- leaves every output non-eligible (``research_eligible: false``,
  ``eligibility_gate_status: "pending"``); creates no features, labels,
  research outputs, database, compacted Parquet, or v003; authorises no
  successor.

Strict fail-closed: any precondition / per-day / aggregate / immutability /
governance / budget failure aborts the run BEFORE the segment manifest is
written. Partial per-day parquets that may have been written before the
failure are preserved (each independently verifiable via its sidecar) and the
segment manifest is NOT written, so the segment is not Stage-0-complete on
failure.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
import zipfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# Locked Phase 4bd scaffold imports — reused verbatim, unchanged.
from prometheus.research.microstructure.normalize_aggtrades import (  # noqa: E402
    NORMALIZATION_SCHEMA_VERSION,
    NORMALIZED_SCHEMA_V001,
    iter_aggtrade_rows_from_csv,
)
from prometheus.research.microstructure.normalize_io import (  # noqa: E402
    NormalizationIOError,
    assert_manifest_path_under_manifests,
    assert_output_path_under_normalized,
    assert_path_under_microstructure,
    atomic_write_parquet,
    compute_bytes_sha256,
    write_sha256_sidecar,
)

# ---------------------------------------------------------------------------
# Locked identity / boundary constants (Phase 4bn-O prompt + Phase 4bn-N memo).
# ---------------------------------------------------------------------------

PHASE_ID = "4bn-O"
PHASE_ID_TOKEN = "4bn_o"
SOURCE_PHASE_BOUNDARY = "4bn-K"

NORMALIZED_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
NORMALIZED_DATASET_VERSION = "v002"
SCHEMA_VERSION = "v001"
SEGMENT_LABEL = "pre_v002_segment"
DATA_FAMILY = "aggTrades"
MARKET = "usdm_futures"
DATASET_CATEGORY = "normalized"

SOURCE_DATASET_FAMILY = "microstructure_raw_aggtrades_v001"
SOURCE_DATASET_VERSION = "v002"
SYMBOL = "BTCUSDT"

# Segment directory / manifest naming (Phase 4bn-N §10 / §14).
SEGMENT_SUFFIX = f"{NORMALIZED_DATASET_VERSION}_pre_v002_segment_{PHASE_ID_TOKEN}"
FAMILY_DIR_NAME = f"{NORMALIZED_DATASET_FAMILY}__{SEGMENT_SUFFIX}"
SEGMENT_MANIFEST_BASENAME = f"{FAMILY_DIR_NAME}.json"

# Window contract.
EXPECTED_DATE_COUNT = 275
EXPECTED_DATE_START = "2024-03-01"
EXPECTED_DATE_END = "2024-11-30"
EXPECTED_TOTAL_EVENT_COUNT = 400_001_695
FULL_ENVELOPE_START = "2024-03-01"
FULL_ENVELOPE_END = "2025-02-28"
UTC_DAY_MS = 86_400_000

# Hard boundary markers.
V002_TERMINAL_START = "2024-12-01"  # reject any date >= this
V002_TERMINAL_END = "2025-02-28"
SEALED_TEST_START = "2025-02-14"
SEALED_TEST_END = "2025-02-28"

# Locked input SHAs (Phase 4bn-J-R2 / 4bn-K committed evidence).
EXPECTED_RAW_SEGMENT_MANIFEST_SHA = (
    "1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1"
)
EXPECTED_RAW_GATE_REPORT_SHA = (
    "051bed7b3a146278e389bd8e265243d30fd541b5f36061d0573f3522920f9c24"
)
EXPECTED_RAW_ACQUISITION_LOG_SHA = (
    "0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93"
)

# Published v002 normalized family — by-reference ONLY; never read, never written.
PUBLISHED_V002_NORMALIZED_MANIFEST_REL = (
    "data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json"
)
PUBLISHED_V002_FAMILY_DIR_NAME = f"{NORMALIZED_DATASET_FAMILY}__{NORMALIZED_DATASET_VERSION}"

# Phase 4bn-L budget caps.
GIB = 1024**3
NORMALIZED_WARN_BYTES = 100 * GIB
NORMALIZED_HARD_BYTES = 150 * GIB
RUNTIME_WARN_SECONDS = 4 * 3600
RUNTIME_HARD_SECONDS = 8 * 3600
TEMP_WARN_BYTES = 50 * GIB
TEMP_HARD_BYTES = 100 * GIB
TOTAL_STACK_WARN_BYTES = 250 * GIB
TOTAL_STACK_HARD_BYTES = 300 * GIB
D_FREE_FLOOR_BYTES = 500 * GIB  # preflight floor
D_FREE_MIN_BYTES = 350 * GIB  # in-execution floor
# Conservative preflight footprint factor (bytes of normalized parquet/event).
PREFLIGHT_BYTES_PER_EVENT = 16

# Default input/output paths (relative to repo root).
DEFAULT_SOURCE_MANIFEST_REL = (
    "data/microstructure/manifests/"
    "microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json"
)
DEFAULT_GATE_REPORT_REL = (
    "data/microstructure/gate-reports/raw/"
    "microstructure_raw_aggtrades_v001__v002__phase-4bn-k__"
    "1780436389489__cf7dc4f7e663.json"
)
DEFAULT_OUTPUT_ROOT_REL = "data/microstructure/normalized"
DEFAULT_MANIFESTS_ROOT_REL = "data/microstructure/manifests"

# Forbidden scope tokens (rejected anywhere in source identity fields).
FORBIDDEN_SCOPE_TOKENS: tuple[str, ...] = (
    "ethusdt",
    "mark-price",
    "mark_price",
    "markprice",
    "spot",
    "order-book",
    "order_book",
    "orderbook",
    "tick",
    "cross-venue",
    "cross_venue",
    "crossvenue",
    "funding",
    "open_interest",
    "open-interest",
    "v003",
)

# Forbidden normalized column-name substrings (locked Phase 4bd guard, extended).
FORBIDDEN_COLUMN_SUBSTRINGS: tuple[str, ...] = (
    "label",
    "target",
    "future",
    "signal",
    "entry",
    "exit",
    "pnl",
    "profit",
    "loss",
    "mfe",
    "mae",
    "r_multiple",
    "equity",
    "position",
    "alpha",
    "edge",
    "prediction",
    "model",
    "score",
    "decision",
    "strategy",
    "liquidation",
    "funding",
    "open_interest",
    "order_book",
    "mark_price",
    "spot",
    "cross_venue",
    "tick",
    "ethusdt",
    "v003",
)

# Forbidden segment-manifest field-name substrings (Phase 4bn-N §13).
FORBIDDEN_MANIFEST_KEY_SUBSTRINGS: tuple[str, ...] = (
    "model",
    "prediction",
    "_score",
    "label_",
    "target_",
    "future_",
    "_future",
    "signal",
    "entry",
    "exit",
    "pnl",
    "equity",
    "profit",
    "loss",
    "position",
    "backtest",
    "strategy",
    "alpha",
    "edge",
    "mfe",
    "mae",
    "r_multiple",
    "barrier",
    "mark_price",
    "funding",
    "open_interest",
    "order_book",
    "cross_venue",
    "ethusdt",
    "v003",
    "chronological_split_policy",
    "diagnostics_authorized",
    "ml_authorized",
    "research_ready",
    "admissible",
    "approved_for_backtest",
)


# ---------------------------------------------------------------------------
# Result / error types
# ---------------------------------------------------------------------------


class Phase4bnOOrchestrationError(RuntimeError):
    """Raised when the Phase 4bn-O orchestrator fails closed."""


class Phase4bnOValidationError(Phase4bnOOrchestrationError):
    """Raised when a precondition / per-day / aggregate / budget check fails."""


@dataclass
class CheckResult:
    """One named check outcome."""

    check_id: str
    title: str
    status: str  # "pass" | "warn" | "fail"
    detail: str = ""


@dataclass
class PerDayProductionRecord:
    """Per-date production record for the segment manifest inventory."""

    date: str
    symbol: str
    local_parquet_path: str
    local_sidecar_path: str
    parquet_sha256: str
    sidecar_sha256: str
    parquet_size_bytes: int
    sidecar_size_bytes: int
    event_count: int
    first_transact_time_ms: int
    last_transact_time_ms: int
    min_agg_trade_id: int
    max_agg_trade_id: int
    source_zip_sha256: str
    source_zip_path: str
    status: str


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------


def _sha256_file(path: Path) -> tuple[str, int]:
    """Return ``(sha256_hex, size_bytes)`` for *path*, streamed in 1 MiB chunks."""
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def _utc_date_to_day_start_ms(utc_date: str) -> int:
    """Return the UTC ms timestamp at the start of *utc_date* (YYYY-MM-DD)."""
    day = datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(day.timestamp() * 1000)


def _disk_free_bytes(path: Path) -> int:
    """Return free bytes on the filesystem hosting *path* (or its nearest parent)."""
    probe = path
    while not probe.exists() and probe.parent != probe:
        probe = probe.parent
    return shutil.disk_usage(probe).free


def _assert_date_in_segment(date: str) -> None:
    """Fail closed if *date* is outside the approved pre-v002 segment window.

    ISO ``YYYY-MM-DD`` strings compare lexicographically, so simple string
    comparison is exact for the date guard.
    """
    if not isinstance(date, str) or len(date) != 10 or date[4] != "-" or date[7] != "-":
        raise Phase4bnOValidationError(f"date not YYYY-MM-DD: {date!r}")
    # Parse to reject malformed (e.g. 2024-13-40).
    datetime.strptime(date, "%Y-%m-%d")
    if date >= V002_TERMINAL_START:
        raise Phase4bnOValidationError(
            f"date {date} is in/after the v002 terminal window "
            f"(>= {V002_TERMINAL_START}); rejected"
        )
    if SEALED_TEST_START <= date <= SEALED_TEST_END:
        raise Phase4bnOValidationError(
            f"date {date} is a sealed-test date; rejected"
        )
    if date < EXPECTED_DATE_START:
        raise Phase4bnOValidationError(
            f"date {date} is before segment start {EXPECTED_DATE_START}; rejected"
        )
    if date > EXPECTED_DATE_END:
        raise Phase4bnOValidationError(
            f"date {date} is after segment end {EXPECTED_DATE_END}; rejected"
        )


def _assert_symbol(symbol: str) -> None:
    """Fail closed on any symbol other than BTCUSDT."""
    if symbol != SYMBOL:
        raise Phase4bnOValidationError(
            f"symbol {symbol!r} rejected; only {SYMBOL} permitted"
        )


def _assert_data_family(family: str) -> None:
    """Fail closed on any data family other than aggTrades."""
    if family != DATA_FAMILY:
        raise Phase4bnOValidationError(
            f"data_family {family!r} rejected; only {DATA_FAMILY} permitted"
        )


def _assert_no_forbidden_scope_tokens(text: str, *, where: str) -> None:
    """Fail closed if any forbidden scope token appears in *text*."""
    low = text.lower()
    for token in FORBIDDEN_SCOPE_TOKENS:
        if token in low:
            raise Phase4bnOValidationError(
                f"forbidden scope token {token!r} found in {where}"
            )


def _assert_segment_naming() -> None:
    """Fail closed if the segment directory/manifest collide with v003 / __v002."""
    if "v003" in FAMILY_DIR_NAME or "v003" in SEGMENT_MANIFEST_BASENAME:
        raise Phase4bnOValidationError("v003 token present in segment naming")
    if FAMILY_DIR_NAME == PUBLISHED_V002_FAMILY_DIR_NAME:
        raise Phase4bnOValidationError(
            "segment family dir must differ from published __v002 directory"
        )
    if SEGMENT_MANIFEST_BASENAME == "microstructure_normalized_aggtrades_v001__v002.json":
        raise Phase4bnOValidationError(
            "segment manifest must differ from published __v002 manifest"
        )


# ---------------------------------------------------------------------------
# Source artefact loading + preconditions
# ---------------------------------------------------------------------------


@dataclass
class SourceArtefactSet:
    """Resolved on-disk paths and pre-state SHAs for all read-only inputs."""

    segment_manifest_path: Path
    segment_manifest_sha_before: str
    segment_manifest_parsed: dict[str, Any]
    acquisition_log_path: Path
    acquisition_log_sha_before: str
    gate_report_path: Path
    gate_report_sha_before: str
    gate_report_id: str
    gate_report_code_commit_sha: str
    raw_zip_paths: list[Path]
    raw_zip_sha_before: list[str]
    raw_zip_size_before: list[int]
    raw_zip_sidecar_paths: list[Path]
    raw_zip_sidecar_sha_before: list[str]


def verify_preconditions(
    *,
    segment_manifest_path: Path,
    gate_report_path: Path,
    repo_root: Path,
    checks: list[CheckResult],
) -> SourceArtefactSet:
    """Verify all input preconditions and load the read-only source artefacts.

    Fails closed (raises :class:`Phase4bnOValidationError`) on the first
    failed precondition, before any output is written.
    """
    _assert_segment_naming()

    # 1. segment manifest exists + SHA matches.
    if not segment_manifest_path.exists():
        raise Phase4bnOValidationError(
            f"raw segment manifest missing: {segment_manifest_path}"
        )
    seg_sha, _ = _sha256_file(segment_manifest_path)
    if seg_sha != EXPECTED_RAW_SEGMENT_MANIFEST_SHA:
        raise Phase4bnOValidationError(
            f"raw segment manifest SHA mismatch: got {seg_sha}, "
            f"expected {EXPECTED_RAW_SEGMENT_MANIFEST_SHA}"
        )
    checks.append(
        CheckResult("4bn-O.1", "raw segment manifest present + SHA matches", "pass", seg_sha)
    )

    parsed = json.loads(segment_manifest_path.read_bytes().decode("utf-8"))
    if not isinstance(parsed, dict):
        raise Phase4bnOValidationError("raw segment manifest is not a JSON object")

    # 2. identity / scope locks.
    _assert_symbol("".join(parsed.get("symbol_list", [])) or "")
    if parsed.get("symbol_list") != [SYMBOL]:
        raise Phase4bnOValidationError(
            f"segment manifest symbol_list != [{SYMBOL!r}]: {parsed.get('symbol_list')!r}"
        )
    _assert_data_family(str(parsed.get("data_family", "")))
    if str(parsed.get("market", "")) != "binance_usdm_futures":
        raise Phase4bnOValidationError(
            f"segment manifest market != binance_usdm_futures: {parsed.get('market')!r}"
        )
    if (
        parsed.get("dataset_family") != SOURCE_DATASET_FAMILY
        or parsed.get("dataset_version") != SOURCE_DATASET_VERSION
        or parsed.get("segment_label") != SEGMENT_LABEL
    ):
        raise Phase4bnOValidationError("segment manifest identity does not match")
    _assert_no_forbidden_scope_tokens(
        " ".join(
            [
                str(parsed.get("symbol_list")),
                str(parsed.get("data_family")),
                str(parsed.get("market")),
                str(parsed.get("dataset_family")),
                str(parsed.get("segment_label")),
            ]
        ),
        where="segment manifest identity",
    )
    checks.append(
        CheckResult("4bn-O.2", "segment manifest identity / scope locks match", "pass")
    )

    # 3. window contract.
    if (
        parsed.get("date_start") != EXPECTED_DATE_START
        or parsed.get("date_end") != EXPECTED_DATE_END
        or parsed.get("date_count") != EXPECTED_DATE_COUNT
        or parsed.get("expected_file_count") != EXPECTED_DATE_COUNT
        or parsed.get("total_row_count") != EXPECTED_TOTAL_EVENT_COUNT
    ):
        raise Phase4bnOValidationError("segment manifest window contract does not match")
    checks.append(
        CheckResult(
            "4bn-O.3",
            "segment manifest window contract matches (275 dates, 2024-03-01..2024-11-30)",
            "pass",
        )
    )

    # 4. non-eligible posture.
    if parsed.get("research_eligible") is not False:
        raise Phase4bnOValidationError("segment manifest research_eligible must be false")
    if parsed.get("eligibility_gate_status") != "pending":
        raise Phase4bnOValidationError(
            "segment manifest eligibility_gate_status must be 'pending'"
        )
    if parsed.get("test_holdout_touched") is not False:
        raise Phase4bnOValidationError("segment manifest test_holdout_touched must be false")
    if parsed.get("test_rows_loaded") != 0:
        raise Phase4bnOValidationError("segment manifest test_rows_loaded must be 0")
    term = parsed.get("existing_v002_terminal_window") or {}
    if term.get("read") is not False:
        raise Phase4bnOValidationError("segment manifest v002 terminal read must be false")
    sealed = parsed.get("existing_v002_sealed_test_split") or {}
    if sealed.get("touched") is not False:
        raise Phase4bnOValidationError(
            "segment manifest sealed test split touched must be false"
        )
    checks.append(
        CheckResult("4bn-O.4", "segment manifest non-eligible / boundary posture OK", "pass")
    )

    # 5. acquisition log exists + SHA matches.
    acquisition_log_path = segment_manifest_path.with_name(
        segment_manifest_path.stem + "_acquisition_log.json"
    )
    if not acquisition_log_path.exists():
        raise Phase4bnOValidationError(
            f"raw acquisition log missing: {acquisition_log_path}"
        )
    acq_sha, _ = _sha256_file(acquisition_log_path)
    if acq_sha != EXPECTED_RAW_ACQUISITION_LOG_SHA:
        raise Phase4bnOValidationError(
            f"raw acquisition log SHA mismatch: got {acq_sha}, "
            f"expected {EXPECTED_RAW_ACQUISITION_LOG_SHA}"
        )
    checks.append(
        CheckResult("4bn-O.5", "raw acquisition log present + SHA matches", "pass", acq_sha)
    )

    # 6. gate report exists + SHA matches + PASS.
    if not gate_report_path.exists():
        raise Phase4bnOValidationError(f"raw gate report missing: {gate_report_path}")
    gate_sha, _ = _sha256_file(gate_report_path)
    if gate_sha != EXPECTED_RAW_GATE_REPORT_SHA:
        raise Phase4bnOValidationError(
            f"raw gate report SHA mismatch: got {gate_sha}, "
            f"expected {EXPECTED_RAW_GATE_REPORT_SHA}"
        )
    gate_parsed = json.loads(gate_report_path.read_bytes().decode("utf-8"))
    if gate_parsed.get("overall_status") != "pass":
        raise Phase4bnOValidationError("raw gate report overall_status is not 'pass'")
    if "PASS" not in str(gate_parsed.get("gate_verdict", "")):
        raise Phase4bnOValidationError("raw gate report verdict is not a PASS")
    gate_report_id = str(gate_parsed.get("report_id", "")).strip() or gate_report_path.stem
    gate_report_code_commit_sha = (
        str(gate_parsed.get("code_commit_sha", "unknown")).strip() or "unknown"
    )
    checks.append(
        CheckResult("4bn-O.6", "raw gate report present + SHA matches + PASS", "pass", gate_sha)
    )

    # 7. exactly 275 inventory entries; date guard; raw zips + sidecars verified.
    inventory: list[dict[str, Any]] = list(parsed.get("per_file_inventory", []))
    if len(inventory) != EXPECTED_DATE_COUNT:
        raise Phase4bnOValidationError(
            f"per_file_inventory length {len(inventory)} != {EXPECTED_DATE_COUNT}"
        )
    date_list = list(parsed.get("date_list", []))
    if len(date_list) != EXPECTED_DATE_COUNT or len(set(date_list)) != EXPECTED_DATE_COUNT:
        raise Phase4bnOValidationError("date_list length / uniqueness invalid")
    if [str(e["date"]) for e in inventory] != date_list:
        raise Phase4bnOValidationError("per_file_inventory dates do not match date_list")

    raw_zip_paths: list[Path] = []
    raw_zip_sha_before: list[str] = []
    raw_zip_size_before: list[int] = []
    raw_zip_sidecar_paths: list[Path] = []
    raw_zip_sidecar_sha_before: list[str] = []
    micro_root = repo_root / "data" / "microstructure"
    for entry in inventory:
        date = str(entry["date"])
        _assert_date_in_segment(date)

        rel_zip = str(entry["local_zip_path"])
        if rel_zip.startswith("microstructure/"):
            rel_zip = rel_zip[len("microstructure/") :]
        zip_path = micro_root / rel_zip
        if "BTCUSDT" not in zip_path.parts or "aggTrades" not in zip_path.name:
            raise Phase4bnOValidationError(
                f"raw zip path outside BTCUSDT aggTrades convention: {zip_path}"
            )
        _assert_no_forbidden_scope_tokens(str(zip_path), where=f"raw zip path {date}")
        if not zip_path.exists():
            raise Phase4bnOValidationError(f"raw zip missing for {date}: {zip_path}")
        actual_sha, actual_size = _sha256_file(zip_path)
        if actual_sha != str(entry["sha256"]):
            raise Phase4bnOValidationError(
                f"raw zip SHA mismatch for {date}: got {actual_sha}, "
                f"expected {entry['sha256']}"
            )
        if actual_size != int(entry["size_bytes"]):
            raise Phase4bnOValidationError(f"raw zip size mismatch for {date}")

        rel_sc = str(entry["local_sidecar_path"])
        if rel_sc.startswith("microstructure/"):
            rel_sc = rel_sc[len("microstructure/") :]
        sidecar_path = micro_root / rel_sc
        if not sidecar_path.exists():
            raise Phase4bnOValidationError(
                f"raw zip sidecar missing for {date}: {sidecar_path}"
            )
        sidecar_sha, _ = _sha256_file(sidecar_path)

        raw_zip_paths.append(zip_path)
        raw_zip_sha_before.append(actual_sha)
        raw_zip_size_before.append(actual_size)
        raw_zip_sidecar_paths.append(sidecar_path)
        raw_zip_sidecar_sha_before.append(sidecar_sha)
    checks.append(
        CheckResult(
            "4bn-O.7",
            f"all {EXPECTED_DATE_COUNT} raw zips + sidecars verified; dates in segment",
            "pass",
            f"{len(raw_zip_paths)} zips",
        )
    )

    return SourceArtefactSet(
        segment_manifest_path=segment_manifest_path,
        segment_manifest_sha_before=seg_sha,
        segment_manifest_parsed=parsed,
        acquisition_log_path=acquisition_log_path,
        acquisition_log_sha_before=acq_sha,
        gate_report_path=gate_report_path,
        gate_report_sha_before=gate_sha,
        gate_report_id=gate_report_id,
        gate_report_code_commit_sha=gate_report_code_commit_sha,
        raw_zip_paths=raw_zip_paths,
        raw_zip_sha_before=raw_zip_sha_before,
        raw_zip_size_before=raw_zip_size_before,
        raw_zip_sidecar_paths=raw_zip_sidecar_paths,
        raw_zip_sidecar_sha_before=raw_zip_sidecar_sha_before,
    )


# ---------------------------------------------------------------------------
# Preflight budget estimation (Phase 4bn-L)
# ---------------------------------------------------------------------------


@dataclass
class PreflightEstimate:
    """Preflight footprint / runtime / free-space estimate."""

    d_free_bytes: int
    estimated_normalized_bytes: int
    estimated_temp_bytes: int
    estimated_total_stack_bytes: int


def run_preflight(
    *,
    artefacts: SourceArtefactSet,
    output_root: Path,
    checks: list[CheckResult],
) -> PreflightEstimate:
    """Estimate footprints + check Phase 4bn-L caps + D: floor before writing."""
    inventory = list(artefacts.segment_manifest_parsed.get("per_file_inventory", []))
    total_events = sum(int(e["row_count"]) for e in inventory)
    max_day_events = max(int(e["row_count"]) for e in inventory)

    est_norm = total_events * PREFLIGHT_BYTES_PER_EVENT
    # Atomic write keeps at most one day's parquet as a transient .tmp.
    est_temp = max_day_events * PREFLIGHT_BYTES_PER_EVENT
    est_total = est_norm + est_temp

    if est_norm <= 0:
        raise Phase4bnOValidationError("preflight cannot estimate normalized footprint")

    d_free = _disk_free_bytes(output_root)
    if d_free < D_FREE_FLOOR_BYTES:
        raise Phase4bnOValidationError(
            f"D: free space {d_free / GIB:.1f} GiB below preflight floor "
            f"{D_FREE_FLOOR_BYTES / GIB:.0f} GiB"
        )
    if est_norm > NORMALIZED_HARD_BYTES:
        raise Phase4bnOValidationError(
            f"preflight normalized estimate {est_norm / GIB:.1f} GiB exceeds hard cap "
            f"{NORMALIZED_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_temp > TEMP_HARD_BYTES:
        raise Phase4bnOValidationError(
            f"preflight temp estimate {est_temp / GIB:.1f} GiB exceeds hard cap "
            f"{TEMP_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_total > TOTAL_STACK_HARD_BYTES:
        raise Phase4bnOValidationError(
            f"preflight total derived-stack estimate {est_total / GIB:.1f} GiB exceeds "
            f"hard cap {TOTAL_STACK_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_norm > NORMALIZED_WARN_BYTES:
        checks.append(
            CheckResult(
                "4bn-O.preflight.warn",
                "normalized footprint estimate above warning threshold",
                "warn",
                f"{est_norm / GIB:.1f} GiB",
            )
        )
    checks.append(
        CheckResult(
            "4bn-O.preflight",
            "preflight footprint/runtime/free-space within Phase 4bn-L caps",
            "pass",
            f"est_norm={est_norm / GIB:.2f} GiB; D_free={d_free / GIB:.0f} GiB",
        )
    )
    return PreflightEstimate(
        d_free_bytes=d_free,
        estimated_normalized_bytes=est_norm,
        estimated_temp_bytes=est_temp,
        estimated_total_stack_bytes=est_total,
    )


# ---------------------------------------------------------------------------
# Per-day normalization
# ---------------------------------------------------------------------------


def _pa_schema() -> Any:
    """Build the pyarrow schema for the 19-column NORMALIZED_SCHEMA_V001."""
    import pyarrow as pa

    return pa.schema(
        [
            ("dataset_family", pa.string()),
            ("dataset_version", pa.string()),
            ("source_dataset_family", pa.string()),
            ("source_dataset_version", pa.string()),
            ("symbol", pa.string()),
            ("utc_date", pa.string()),
            ("agg_trade_id", pa.int64()),
            ("price", pa.string()),
            ("quantity", pa.string()),
            ("first_trade_id", pa.int64()),
            ("last_trade_id", pa.int64()),
            ("transact_time_ms", pa.int64()),
            ("is_buyer_maker", pa.bool_()),
            ("source_file_sha256", pa.string()),
            ("source_manifest_sha256", pa.string()),
            ("source_gate_report_id", pa.string()),
            ("source_gate_report_sha256", pa.string()),
            ("row_index", pa.int64()),
            ("normalization_schema_version", pa.string()),
        ]
    )


def _assert_no_forbidden_columns() -> None:
    """Fail closed if any normalized column carries a forbidden substring."""
    for col in NORMALIZED_SCHEMA_V001:
        low = col.lower()
        for needle in FORBIDDEN_COLUMN_SUBSTRINGS:
            if needle in low:
                raise Phase4bnOValidationError(
                    f"forbidden substring {needle!r} in column {col!r}"
                )


def normalize_one_date(
    *,
    inventory_entry: Mapping[str, Any],
    raw_zip_path: Path,
    raw_zip_sha: str,
    source_manifest_sha: str,
    gate_report_id: str,
    gate_report_sha: str,
    output_root: Path,
    refuse_overwrite: bool,
) -> PerDayProductionRecord:
    """Normalise one date's raw zip into the segment directory; verify everything."""
    import pyarrow as pa

    date_str = str(inventory_entry["date"])
    _assert_date_in_segment(date_str)
    expected_event_count = int(inventory_entry["row_count"])
    expected_first_ms = int(inventory_entry["first_trade_time_ms"])
    expected_last_ms = int(inventory_entry["last_trade_time_ms"])
    expected_min_a = int(inventory_entry["min_agg_trade_id"])
    expected_max_a = int(inventory_entry["max_agg_trade_id"])

    with zipfile.ZipFile(raw_zip_path) as zf:
        members = zf.namelist()
        if len(members) != 1:
            raise Phase4bnOValidationError(
                f"date {date_str}: zip must contain exactly one CSV member; "
                f"got {len(members)}"
            )
        with zf.open(members[0]) as raw:
            csv_text = raw.read().decode("utf-8")

    payloads = iter_aggtrade_rows_from_csv(csv_text)
    if len(payloads) != expected_event_count:
        raise Phase4bnOValidationError(
            f"date {date_str}: row count {len(payloads)} != manifest row_count "
            f"{expected_event_count}"
        )

    day_start_ms = _utc_date_to_day_start_ms(date_str)
    day_end_excl_ms = day_start_ms + UTC_DAY_MS

    col_agg_trade_id: list[int] = []
    col_price: list[str] = []
    col_quantity: list[str] = []
    col_first_trade_id: list[int] = []
    col_last_trade_id: list[int] = []
    col_transact_time_ms: list[int] = []
    col_is_buyer_maker: list[bool] = []
    col_row_index: list[int] = []

    prev_a = -1
    prev_t = -1
    seen_a: set[int] = set()
    min_a = 2**63 - 1
    max_a = -1
    first_ms = 0
    last_ms = 0
    for row_index, payload in enumerate(payloads):
        a = int(payload.aggregate_trade_id)
        t = int(payload.trade_time_ms)
        if a in seen_a:
            raise Phase4bnOValidationError(
                f"date {date_str}: duplicate agg_trade_id {a} at row {row_index}"
            )
        seen_a.add(a)
        if a < prev_a:
            raise Phase4bnOValidationError(
                f"date {date_str}: agg_trade_id non-monotone at row {row_index}"
            )
        if prev_t > t:
            raise Phase4bnOValidationError(
                f"date {date_str}: transact_time_ms non-monotone at row {row_index}"
            )
        if not (day_start_ms <= t < day_end_excl_ms):
            raise Phase4bnOValidationError(
                f"date {date_str}: transact_time_ms {t} outside half-open day bound"
            )
        prev_a = a
        prev_t = t
        min_a = min(min_a, a)
        max_a = max(max_a, a)
        if row_index == 0:
            first_ms = t
        last_ms = t

        col_agg_trade_id.append(a)
        col_price.append(str(payload.price))
        col_quantity.append(str(payload.quantity))
        col_first_trade_id.append(int(payload.first_trade_id))
        col_last_trade_id.append(int(payload.last_trade_id))
        col_transact_time_ms.append(t)
        col_is_buyer_maker.append(bool(payload.buyer_is_maker))
        col_row_index.append(row_index)

    if first_ms != expected_first_ms:
        raise Phase4bnOValidationError(
            f"date {date_str}: first_transact_time_ms {first_ms} != "
            f"inventory {expected_first_ms}"
        )
    if last_ms != expected_last_ms:
        raise Phase4bnOValidationError(
            f"date {date_str}: last_transact_time_ms {last_ms} != "
            f"inventory {expected_last_ms}"
        )
    if min_a != expected_min_a:
        raise Phase4bnOValidationError(
            f"date {date_str}: min_agg_trade_id {min_a} != inventory {expected_min_a}"
        )
    if max_a != expected_max_a:
        raise Phase4bnOValidationError(
            f"date {date_str}: max_agg_trade_id {max_a} != inventory {expected_max_a}"
        )

    n = len(payloads)
    schema = _pa_schema()
    if tuple(schema.names) != NORMALIZED_SCHEMA_V001:
        raise Phase4bnOValidationError(
            f"date {date_str}: schema names != NORMALIZED_SCHEMA_V001"
        )
    _assert_no_forbidden_columns()

    table = pa.Table.from_pydict(
        {
            "dataset_family": [NORMALIZED_DATASET_FAMILY] * n,
            "dataset_version": [NORMALIZED_DATASET_VERSION] * n,
            "source_dataset_family": [SOURCE_DATASET_FAMILY] * n,
            "source_dataset_version": [SOURCE_DATASET_VERSION] * n,
            "symbol": [SYMBOL] * n,
            "utc_date": [date_str] * n,
            "agg_trade_id": col_agg_trade_id,
            "price": col_price,
            "quantity": col_quantity,
            "first_trade_id": col_first_trade_id,
            "last_trade_id": col_last_trade_id,
            "transact_time_ms": col_transact_time_ms,
            "is_buyer_maker": col_is_buyer_maker,
            "source_file_sha256": [raw_zip_sha] * n,
            "source_manifest_sha256": [source_manifest_sha] * n,
            "source_gate_report_id": [gate_report_id] * n,
            "source_gate_report_sha256": [gate_report_sha] * n,
            "row_index": col_row_index,
            "normalization_schema_version": [NORMALIZATION_SCHEMA_VERSION] * n,
        },
        schema=schema,
    )

    yyyy, mm, _dd = date_str.split("-")
    target = (
        output_root
        / FAMILY_DIR_NAME
        / SYMBOL
        / yyyy
        / mm
        / f"{SYMBOL}-aggTrades-{date_str}.parquet"
    )
    # Hard guard: never write into the published __v002 family directory.
    assert_output_path_under_normalized(target, label="segment parquet path")
    if PUBLISHED_V002_FAMILY_DIR_NAME in target.parts and FAMILY_DIR_NAME not in target.parts:
        raise Phase4bnOValidationError("refusing to write into published __v002 directory")
    target.parent.mkdir(parents=True, exist_ok=True)

    parquet_sha, parquet_size = atomic_write_parquet(
        target, table, refuse_overwrite=refuse_overwrite
    )
    sidecar_target = target.with_suffix(target.suffix + ".sha256")
    sidecar_sha, sidecar_size = write_sha256_sidecar(
        sidecar_target,
        target_filename=target.name,
        sha256_hex=parquet_sha,
        refuse_overwrite=refuse_overwrite,
    )

    # Relative paths under data/microstructure (mirrors raw inventory style).
    local_parquet_rel = "microstructure/" + str(
        target.relative_to(target.parents[5])
    ).replace(os.sep, "/")
    local_sidecar_rel = local_parquet_rel + ".sha256"

    return PerDayProductionRecord(
        date=date_str,
        symbol=SYMBOL,
        local_parquet_path=local_parquet_rel,
        local_sidecar_path=local_sidecar_rel,
        parquet_sha256=parquet_sha,
        sidecar_sha256=sidecar_sha,
        parquet_size_bytes=parquet_size,
        sidecar_size_bytes=sidecar_size,
        event_count=n,
        first_transact_time_ms=first_ms,
        last_transact_time_ms=last_ms,
        min_agg_trade_id=min_a,
        max_agg_trade_id=max_a,
        source_zip_sha256=raw_zip_sha,
        source_zip_path=str(inventory_entry["local_zip_path"]),
        status="produced_verified",
    )


# ---------------------------------------------------------------------------
# Segment manifest builder (Phase 4bn-N §12)
# ---------------------------------------------------------------------------


def build_segment_manifest(
    *,
    artefacts: SourceArtefactSet,
    per_day_records: Sequence[PerDayProductionRecord],
    base_commit_sha: str,
    code_commit_sha: str,
    capture_config_hash: str,
    created_at_unix_ms: int,
    created_at_utc: str,
    total_normalized_footprint_bytes: int,
    budget_witnesses: Mapping[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    """Construct the Phase 4bn-O normalized segment manifest dict."""

    def _rel_to_repo(p: Path) -> str:
        return str(p.resolve().relative_to(repo_root.resolve())).replace(os.sep, "/")

    parsed = artefacts.segment_manifest_parsed
    date_list = list(parsed.get("date_list", []))
    inventory_entries: list[dict[str, Any]] = []
    for r in per_day_records:
        inventory_entries.append(
            {
                "date": r.date,
                "symbol": r.symbol,
                "local_parquet_path": r.local_parquet_path,
                "local_sidecar_path": r.local_sidecar_path,
                "parquet_sha256": r.parquet_sha256,
                "sidecar_sha256": r.sidecar_sha256,
                "parquet_size_bytes": r.parquet_size_bytes,
                "sidecar_size_bytes": r.sidecar_size_bytes,
                "event_count": r.event_count,
                "first_transact_time_ms": r.first_transact_time_ms,
                "last_transact_time_ms": r.last_transact_time_ms,
                "min_agg_trade_id": r.min_agg_trade_id,
                "max_agg_trade_id": r.max_agg_trade_id,
                "source_zip_sha256": r.source_zip_sha256,
                "source_zip_path": r.source_zip_path,
                "status": r.status,
            }
        )

    total_event_count = sum(r.event_count for r in per_day_records)

    governance_labels: dict[str, str] = {
        "phase": PHASE_ID,
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "source_dataset_family": SOURCE_DATASET_FAMILY,
        "source_dataset_version": SOURCE_DATASET_VERSION,
        "validator": "phase_4ax_aggtrades_v001",
        "stop_trigger_domain": "trade_price_backtest_candidate",
        "feature_computation": "forbidden",
        "strategy_use": "forbidden",
        "normalization": "phase_4bn_o_segment_normalization",
        "phase_4bn_o_no_successor_authorization": "true",
        "segment": "true",
    }

    return {
        # Identity / family.
        "dataset_family": NORMALIZED_DATASET_FAMILY,
        "dataset_version": NORMALIZED_DATASET_VERSION,
        "version": NORMALIZED_DATASET_VERSION,
        "schema_version": SCHEMA_VERSION,
        "segment_label": SEGMENT_LABEL,
        "data_family": DATA_FAMILY,
        "symbol_list": [SYMBOL],
        "market": MARKET,
        "dataset_category": DATASET_CATEGORY,
        # Segment / phase.
        "phase": PHASE_ID,
        "phase_id": PHASE_ID,
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "created_at_unix_ms": created_at_unix_ms,
        "created_at_utc": created_at_utc,
        "code_commit_sha": code_commit_sha,
        "base_commit_sha": base_commit_sha,
        "capture_config_hash": capture_config_hash,
        # Window / inventory.
        "date_start": EXPECTED_DATE_START,
        "date_end": EXPECTED_DATE_END,
        "date_count": EXPECTED_DATE_COUNT,
        "date_list": date_list,
        "expected_file_count": EXPECTED_DATE_COUNT,
        "produced_file_count": len(per_day_records),
        "total_event_count": total_event_count,
        "total_row_count": total_event_count,
        "per_file_inventory": inventory_entries,
        "total_normalized_footprint_bytes": total_normalized_footprint_bytes,
        # Input lineage (predecessor linkage).
        "source_dataset_family": SOURCE_DATASET_FAMILY,
        "source_dataset_version": SOURCE_DATASET_VERSION,
        "source_raw_segment_manifest_path": _rel_to_repo(artefacts.segment_manifest_path),
        "source_raw_segment_manifest_sha256": artefacts.segment_manifest_sha_before,
        "source_raw_gate_report_path": _rel_to_repo(artefacts.gate_report_path),
        "source_raw_gate_report_id": artefacts.gate_report_id,
        "source_raw_gate_report_sha256": artefacts.gate_report_sha_before,
        "source_raw_acquisition_log_path": _rel_to_repo(artefacts.acquisition_log_path),
        "source_raw_acquisition_log_sha256": artefacts.acquisition_log_sha_before,
        # Existing-normalized linkage (by reference only; not read, not mutated).
        "existing_v002_normalized_reference": {
            "path": PUBLISHED_V002_NORMALIZED_MANIFEST_REL,
            "window_start": V002_TERMINAL_START,
            "window_end": V002_TERMINAL_END,
            "read": False,
            "mutated": False,
        },
        # Full-envelope by reference.
        "full_intended_envelope_start": FULL_ENVELOPE_START,
        "full_intended_envelope_end": FULL_ENVELOPE_END,
        # Eligibility / governance posture.
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "governance_labels": governance_labels,
        "no_successor_authorization": True,
        # Sealed-test / terminal boundary witnesses.
        "v002_terminal_window_mode": "by_reference",
        "existing_v002_terminal_window": {
            "start": V002_TERMINAL_START,
            "end": V002_TERMINAL_END,
            "read": False,
            "overwritten": False,
            "redownloaded": False,
            "re_normalized": False,
        },
        "sealed_test_split_touched": False,
        "existing_v002_sealed_test_split": {
            "start": SEALED_TEST_START,
            "end": SEALED_TEST_END,
            "touched": False,
        },
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        # Partitioning / storage.
        "partitioning_rule": "<SYMBOL>/<YYYY>/<MM>/",
        "primary_key": ["symbol", "utc_date", "agg_trade_id"],
        "storage_format": "parquet_zstd",
        "sidecar_policy": "canonical_two_space_sha256",
        "invalid_windows": [],
        # Budget witnesses (Phase 4bn-L).
        "budget_witnesses": dict(budget_witnesses),
    }


def assert_manifest_field_contract(manifest: Mapping[str, Any]) -> None:
    """Fail closed if the segment manifest violates the §12/§13 field contract."""
    required = (
        "dataset_family",
        "dataset_version",
        "version",
        "schema_version",
        "segment_label",
        "data_family",
        "symbol_list",
        "market",
        "dataset_category",
        "phase",
        "phase_id",
        "source_phase_boundary",
        "created_at_unix_ms",
        "created_at_utc",
        "code_commit_sha",
        "base_commit_sha",
        "capture_config_hash",
        "date_start",
        "date_end",
        "date_count",
        "date_list",
        "expected_file_count",
        "produced_file_count",
        "total_event_count",
        "total_row_count",
        "per_file_inventory",
        "total_normalized_footprint_bytes",
        "source_dataset_family",
        "source_dataset_version",
        "source_raw_segment_manifest_path",
        "source_raw_segment_manifest_sha256",
        "source_raw_gate_report_path",
        "source_raw_gate_report_id",
        "source_raw_gate_report_sha256",
        "source_raw_acquisition_log_path",
        "source_raw_acquisition_log_sha256",
        "existing_v002_normalized_reference",
        "full_intended_envelope_start",
        "full_intended_envelope_end",
        "research_eligible",
        "eligibility_gate_status",
        "governance_labels",
        "no_successor_authorization",
        "v002_terminal_window_mode",
        "existing_v002_terminal_window",
        "sealed_test_split_touched",
        "existing_v002_sealed_test_split",
        "test_holdout_touched",
        "test_rows_loaded",
        "partitioning_rule",
        "primary_key",
        "storage_format",
        "sidecar_policy",
        "invalid_windows",
        "budget_witnesses",
    )
    missing = [k for k in required if k not in manifest]
    if missing:
        raise Phase4bnOValidationError(f"segment manifest missing required keys: {missing}")

    # Non-eligible posture.
    if manifest["research_eligible"] is not False:
        raise Phase4bnOValidationError("manifest research_eligible must be False")
    if manifest["eligibility_gate_status"] != "pending":
        raise Phase4bnOValidationError("manifest eligibility_gate_status must be 'pending'")
    if manifest["no_successor_authorization"] is not True:
        raise Phase4bnOValidationError("manifest no_successor_authorization must be True")
    if manifest["dataset_version"] != "v002" or manifest["version"] != "v002":
        raise Phase4bnOValidationError("manifest dataset_version/version must be 'v002'")
    if manifest["segment_label"] != SEGMENT_LABEL:
        raise Phase4bnOValidationError("manifest segment_label must be 'pre_v002_segment'")
    gov = manifest["governance_labels"]
    if gov.get("feature_computation") != "forbidden":
        raise Phase4bnOValidationError("governance feature_computation must be 'forbidden'")
    if gov.get("strategy_use") != "forbidden":
        raise Phase4bnOValidationError("governance strategy_use must be 'forbidden'")
    ref = manifest["existing_v002_normalized_reference"]
    if ref.get("read") is not False or ref.get("mutated") is not False:
        raise Phase4bnOValidationError("v002 normalized reference must be read/mutated False")

    # Forbidden field-name scan (recursive over keys). The ``governance_labels``
    # subtree is validated explicitly above and legitimately carries
    # forbidden-as-declaration keys (``strategy_use``, ``feature_computation``)
    # and a locked lineage value (``stop_trigger_domain``); it is not rescanned.
    def _scan(obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                low = str(k).lower()
                for needle in FORBIDDEN_MANIFEST_KEY_SUBSTRINGS:
                    if needle in low:
                        raise Phase4bnOValidationError(
                            f"forbidden manifest field substring {needle!r} in key {k!r}"
                        )
                if k == "governance_labels":
                    continue
                _scan(v)
        elif isinstance(obj, list):
            for item in obj:
                _scan(item)

    _scan(manifest)


def _atomic_write_segment_manifest(
    path: Path, obj: Mapping[str, Any], *, refuse_overwrite: bool = True
) -> tuple[str, int]:
    """Atomic write of the segment manifest under data/microstructure/manifests/."""
    if not isinstance(path, Path):
        raise NormalizationIOError("path must be a pathlib.Path")
    assert_manifest_path_under_manifests(path, label="segment manifest path")
    if refuse_overwrite and path.exists():
        raise NormalizationIOError(f"refusing to overwrite existing file: {path}")
    tmp_companion = path.with_suffix(path.suffix + ".tmp")
    if tmp_companion.exists():
        raise NormalizationIOError(f"stale .tmp companion exists: {tmp_companion}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(dict(obj), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    fd, tmp_str = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    tmp_path = Path(tmp_str)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(payload)
            f.flush()
            with contextlib.suppress(OSError):
                os.fsync(f.fileno())
        sha = compute_bytes_sha256(payload)
        os.replace(tmp_path, path)
        return sha, len(payload)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------


@dataclass
class OrchestrationResult:
    """Top-level result of one Phase 4bn-O normalization run."""

    overall_status: str  # "pass" | "fail_closed"
    output_manifest_path: Path | None
    output_manifest_sha256: str | None
    output_manifest_sidecar_path: Path | None
    output_manifest_sidecar_sha256: str | None
    produced_file_count: int
    total_event_count: int
    total_normalized_footprint_bytes: int
    per_day_records: list[PerDayProductionRecord] = field(default_factory=list)
    checks: list[CheckResult] = field(default_factory=list)
    budget_witnesses: dict[str, Any] = field(default_factory=dict)
    failed_check_id: str | None = None
    failure_message: str | None = None
    wall_clock_seconds: float = 0.0
    warning_thresholds_crossed: list[str] = field(default_factory=list)
    hard_caps_crossed: bool = False


def _git_head_sha(repo_root: Path) -> str:
    head_file = repo_root / ".git" / "HEAD"
    if not head_file.exists():
        return "unknown"
    head_ref = head_file.read_text(encoding="utf-8").strip()
    if head_ref.startswith("ref:"):
        ref_path = head_ref.split(" ", 1)[1].strip()
        sha_file = repo_root / ".git" / ref_path
        if sha_file.exists():
            return sha_file.read_text(encoding="utf-8").strip()
        packed = repo_root / ".git" / "packed-refs"
        if packed.exists():
            for line in packed.read_text(encoding="utf-8").splitlines():
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.split(" ", 1)
                if len(parts) == 2 and parts[1] == ref_path:
                    return parts[0].strip()
        return "unknown"
    return head_ref


def _verify_raw_immutability(artefacts: SourceArtefactSet) -> None:
    """Re-hash every read-only input and fail closed on any drift."""
    after, _ = _sha256_file(artefacts.segment_manifest_path)
    if after != artefacts.segment_manifest_sha_before:
        raise Phase4bnOValidationError("raw segment manifest mutated during run")
    after, _ = _sha256_file(artefacts.acquisition_log_path)
    if after != artefacts.acquisition_log_sha_before:
        raise Phase4bnOValidationError("raw acquisition log mutated during run")
    after, _ = _sha256_file(artefacts.gate_report_path)
    if after != artefacts.gate_report_sha_before:
        raise Phase4bnOValidationError("raw gate report mutated during run")
    for i, zp in enumerate(artefacts.raw_zip_paths):
        sha, size = _sha256_file(zp)
        if sha != artefacts.raw_zip_sha_before[i] or size != artefacts.raw_zip_size_before[i]:
            raise Phase4bnOValidationError(f"raw zip mutated during run: {zp}")
    for i, sp in enumerate(artefacts.raw_zip_sidecar_paths):
        sha, _ = _sha256_file(sp)
        if sha != artefacts.raw_zip_sidecar_sha_before[i]:
            raise Phase4bnOValidationError(f"raw zip sidecar mutated during run: {sp}")


def run(
    *,
    segment_manifest_path: Path,
    gate_report_path: Path,
    output_root: Path,
    manifests_root: Path,
    repo_root: Path,
    refuse_overwrite: bool = True,
    code_commit_sha: str | None = None,
    base_commit_sha: str | None = None,
) -> OrchestrationResult:
    """Run the full Phase 4bn-O normalization once. Fail-closed on any breach."""
    start = time.monotonic()
    checks: list[CheckResult] = []
    per_day_records: list[PerDayProductionRecord] = []
    warnings_crossed: list[str] = []
    running_norm_bytes = 0
    temp_pre_cleanup_peak = 0
    d_free_min_observed = _disk_free_bytes(output_root)

    assert_path_under_microstructure(output_root, label="output_root")
    assert_manifest_path_under_manifests(
        manifests_root / "x.json", label="manifests_root probe"
    )

    try:
        artefacts = verify_preconditions(
            segment_manifest_path=segment_manifest_path,
            gate_report_path=gate_report_path,
            repo_root=repo_root,
            checks=checks,
        )
        preflight = run_preflight(
            artefacts=artefacts, output_root=output_root, checks=checks
        )
        d_free_min_observed = min(d_free_min_observed, preflight.d_free_bytes)

        commit_sha = code_commit_sha or _git_head_sha(repo_root)
        base_sha = base_commit_sha or "f55b47ff94637e72ebacc40f1a133a5526afaef6"
        capture_config_hash = compute_bytes_sha256(
            json.dumps(
                {
                    "phase": PHASE_ID,
                    "schema_version": SCHEMA_VERSION,
                    "schema_columns": list(NORMALIZED_SCHEMA_V001),
                    "dataset_family": NORMALIZED_DATASET_FAMILY,
                    "dataset_version": NORMALIZED_DATASET_VERSION,
                    "segment_label": SEGMENT_LABEL,
                    "family_dir": FAMILY_DIR_NAME,
                    "source_raw_segment_manifest_sha256": (
                        artefacts.segment_manifest_sha_before
                    ),
                    "source_raw_gate_report_sha256": artefacts.gate_report_sha_before,
                    "expected_date_count": EXPECTED_DATE_COUNT,
                    "expected_total_event_count": EXPECTED_TOTAL_EVENT_COUNT,
                },
                sort_keys=True,
            ).encode("utf-8")
        )

        inventory = list(artefacts.segment_manifest_parsed.get("per_file_inventory", []))
        prev_month = None
        for i, entry in enumerate(inventory):
            record = normalize_one_date(
                inventory_entry=entry,
                raw_zip_path=artefacts.raw_zip_paths[i],
                raw_zip_sha=artefacts.raw_zip_sha_before[i],
                source_manifest_sha=artefacts.segment_manifest_sha_before,
                gate_report_id=artefacts.gate_report_id,
                gate_report_sha=artefacts.gate_report_sha_before,
                output_root=output_root,
                refuse_overwrite=refuse_overwrite,
            )
            per_day_records.append(record)
            running_norm_bytes += record.parquet_size_bytes + record.sidecar_size_bytes
            temp_pre_cleanup_peak = max(temp_pre_cleanup_peak, record.parquet_size_bytes)

            # Day-boundary budget measurement.
            elapsed = time.monotonic() - start
            d_free = _disk_free_bytes(output_root)
            d_free_min_observed = min(d_free_min_observed, d_free)
            _enforce_budgets(
                running_norm_bytes=running_norm_bytes,
                elapsed=elapsed,
                d_free=d_free,
                temp_peak=temp_pre_cleanup_peak,
                warnings_crossed=warnings_crossed,
            )
            month = record.date[:7]
            if month != prev_month:
                checks.append(
                    CheckResult(
                        f"4bn-O.month.{month}",
                        f"month {month} boundary budget OK",
                        "pass",
                        f"norm={running_norm_bytes / GIB:.2f} GiB; "
                        f"D_free={d_free / GIB:.0f} GiB; elapsed={elapsed:.0f}s",
                    )
                )
                prev_month = month

        # Aggregate checks.
        if len(per_day_records) != EXPECTED_DATE_COUNT:
            raise Phase4bnOValidationError(
                f"produced_file_count {len(per_day_records)} != {EXPECTED_DATE_COUNT}"
            )
        total_events = sum(r.event_count for r in per_day_records)
        if total_events != EXPECTED_TOTAL_EVENT_COUNT:
            raise Phase4bnOValidationError(
                f"total_event_count {total_events} != {EXPECTED_TOTAL_EVENT_COUNT}"
            )
        for i in range(len(per_day_records) - 1):
            if (
                per_day_records[i].last_transact_time_ms
                >= per_day_records[i + 1].first_transact_time_ms
            ):
                raise Phase4bnOValidationError(
                    f"adjacent-date overlap between {per_day_records[i].date} and "
                    f"{per_day_records[i + 1].date}"
                )
        checks.append(
            CheckResult(
                "4bn-O.aggregate",
                "produced 275 parquets; total events + adjacency verified",
                "pass",
                str(total_events),
            )
        )

        _verify_raw_immutability(artefacts)
        checks.append(
            CheckResult("4bn-O.immutability", "all raw inputs byte-identical pre/post", "pass")
        )

        budget_witnesses: dict[str, Any] = {
            "normalized_warn_bytes": NORMALIZED_WARN_BYTES,
            "normalized_hard_bytes": NORMALIZED_HARD_BYTES,
            "runtime_warn_seconds": RUNTIME_WARN_SECONDS,
            "runtime_hard_seconds": RUNTIME_HARD_SECONDS,
            "temp_warn_bytes": TEMP_WARN_BYTES,
            "temp_hard_bytes": TEMP_HARD_BYTES,
            "total_stack_warn_bytes": TOTAL_STACK_WARN_BYTES,
            "total_stack_hard_bytes": TOTAL_STACK_HARD_BYTES,
            "d_free_floor_bytes": D_FREE_FLOOR_BYTES,
            "d_free_min_bytes": D_FREE_MIN_BYTES,
            "d_free_preflight_bytes": preflight.d_free_bytes,
            "d_free_min_observed_bytes": d_free_min_observed,
            "measured_normalized_footprint_bytes": running_norm_bytes,
            "measured_temp_footprint_pre_cleanup_bytes": temp_pre_cleanup_peak,
            "measured_temp_footprint_post_cleanup_bytes": 0,
            "measured_runtime_seconds": time.monotonic() - start,
            "preflight_estimated_normalized_bytes": preflight.estimated_normalized_bytes,
            "warning_thresholds_crossed": list(warnings_crossed),
            "hard_caps_crossed": False,
        }

        now_unix_ms = int(time.time() * 1000)
        now_utc = datetime.now(UTC).isoformat()
        manifest_dict = build_segment_manifest(
            artefacts=artefacts,
            per_day_records=per_day_records,
            base_commit_sha=base_sha,
            code_commit_sha=commit_sha,
            capture_config_hash=capture_config_hash,
            created_at_unix_ms=now_unix_ms,
            created_at_utc=now_utc,
            total_normalized_footprint_bytes=running_norm_bytes,
            budget_witnesses=budget_witnesses,
            repo_root=repo_root,
        )
        assert_manifest_field_contract(manifest_dict)
        checks.append(
            CheckResult("4bn-O.manifest", "segment manifest field contract satisfied", "pass")
        )

        manifest_path = manifests_root / SEGMENT_MANIFEST_BASENAME
        manifest_sha, _ = _atomic_write_segment_manifest(
            manifest_path, manifest_dict, refuse_overwrite=refuse_overwrite
        )
        manifest_sidecar_path = manifest_path.with_suffix(manifest_path.suffix + ".sha256")
        manifest_sidecar_sha, _ = write_sha256_sidecar(
            manifest_sidecar_path,
            target_filename=manifest_path.name,
            sha256_hex=manifest_sha,
            refuse_overwrite=refuse_overwrite,
        )
        checks.append(
            CheckResult("4bn-O.write", "segment manifest + sidecar written", "pass")
        )

        return OrchestrationResult(
            overall_status="pass",
            output_manifest_path=manifest_path,
            output_manifest_sha256=manifest_sha,
            output_manifest_sidecar_path=manifest_sidecar_path,
            output_manifest_sidecar_sha256=manifest_sidecar_sha,
            produced_file_count=len(per_day_records),
            total_event_count=total_events,
            total_normalized_footprint_bytes=running_norm_bytes,
            per_day_records=per_day_records,
            checks=checks,
            budget_witnesses=budget_witnesses,
            wall_clock_seconds=time.monotonic() - start,
            warning_thresholds_crossed=warnings_crossed,
            hard_caps_crossed=False,
        )
    except Phase4bnOOrchestrationError as exc:
        failed_id = checks[-1].check_id if checks else "4bn-O.precondition"
        return OrchestrationResult(
            overall_status="fail_closed",
            output_manifest_path=None,
            output_manifest_sha256=None,
            output_manifest_sidecar_path=None,
            output_manifest_sidecar_sha256=None,
            produced_file_count=len(per_day_records),
            total_event_count=sum(r.event_count for r in per_day_records),
            total_normalized_footprint_bytes=running_norm_bytes,
            per_day_records=per_day_records,
            checks=checks,
            failed_check_id=failed_id,
            failure_message=str(exc),
            wall_clock_seconds=time.monotonic() - start,
            warning_thresholds_crossed=warnings_crossed,
            hard_caps_crossed="hard cap" in str(exc).lower(),
        )


def _enforce_budgets(
    *,
    running_norm_bytes: int,
    elapsed: float,
    d_free: int,
    temp_peak: int,
    warnings_crossed: list[str],
) -> None:
    """Fail closed on any hard cap; record warning crossings."""
    if running_norm_bytes > NORMALIZED_HARD_BYTES:
        raise Phase4bnOValidationError(
            f"normalized footprint {running_norm_bytes / GIB:.1f} GiB exceeds hard cap"
        )
    if elapsed > RUNTIME_HARD_SECONDS:
        raise Phase4bnOValidationError(
            f"runtime {elapsed:.0f}s exceeds hard cap {RUNTIME_HARD_SECONDS}s"
        )
    if d_free < D_FREE_MIN_BYTES:
        raise Phase4bnOValidationError(
            f"D: free {d_free / GIB:.1f} GiB fell below in-execution floor "
            f"{D_FREE_MIN_BYTES / GIB:.0f} GiB"
        )
    if temp_peak > TEMP_HARD_BYTES:
        raise Phase4bnOValidationError(
            f"temporary workspace {temp_peak / GIB:.1f} GiB exceeds hard cap"
        )
    if running_norm_bytes > NORMALIZED_WARN_BYTES and "normalized_warn" not in warnings_crossed:
        warnings_crossed.append("normalized_warn")
    if elapsed > RUNTIME_WARN_SECONDS and "runtime_warn" not in warnings_crossed:
        warnings_crossed.append("runtime_warn")
    if temp_peak > TEMP_WARN_BYTES and "temp_warn" not in warnings_crossed:
        warnings_crossed.append("temp_warn")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Phase 4bn-O — Normalization-Only Pre-V002 BTCUSDT aggTrades Segment. "
            "Reads the approved pre-v002 raw segment read-only and produces 275 "
            "normalized Parquet files + 275 sidecars + 1 segment manifest + 1 "
            "manifest sidecar under data/microstructure/."
        )
    )
    p.add_argument("--segment-manifest", type=Path, default=None)
    p.add_argument("--gate-report", type=Path, default=None)
    p.add_argument("--output-root", type=Path, default=None)
    p.add_argument("--manifests-root", type=Path, default=None)
    p.add_argument("--dry-run", action="store_true", help="Preflight only; write nothing.")
    p.add_argument("--allow-overwrite", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = _REPO_ROOT
    segment_manifest_path = args.segment_manifest or repo_root / DEFAULT_SOURCE_MANIFEST_REL
    gate_report_path = args.gate_report or repo_root / DEFAULT_GATE_REPORT_REL
    output_root = args.output_root or repo_root / DEFAULT_OUTPUT_ROOT_REL
    manifests_root = args.manifests_root or repo_root / DEFAULT_MANIFESTS_ROOT_REL
    output_root.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        checks: list[CheckResult] = []
        try:
            artefacts = verify_preconditions(
                segment_manifest_path=segment_manifest_path,
                gate_report_path=gate_report_path,
                repo_root=repo_root,
                checks=checks,
            )
            run_preflight(artefacts=artefacts, output_root=output_root, checks=checks)
        except Phase4bnOOrchestrationError as exc:
            print(f"[dry-run] FAIL_CLOSED: {exc}")
            for c in checks:
                print(f"  - {c.check_id} {c.status.upper()}: {c.title}")
            return 1
        print("[dry-run] preconditions + preflight PASS")
        for c in checks:
            print(f"  - {c.check_id} {c.status.upper()}: {c.title}")
        return 0

    result = run(
        segment_manifest_path=segment_manifest_path,
        gate_report_path=gate_report_path,
        output_root=output_root,
        manifests_root=manifests_root,
        repo_root=repo_root,
        refuse_overwrite=not args.allow_overwrite,
    )
    if result.overall_status == "pass":
        print(
            f"[Phase 4bn-O] PASS — produced {result.produced_file_count} parquets "
            f"totalling {result.total_event_count} events "
            f"({result.total_normalized_footprint_bytes / GIB:.2f} GiB) in "
            f"{result.wall_clock_seconds:.1f}s; manifest at "
            f"{result.output_manifest_path} (sha256={result.output_manifest_sha256})"
        )
        if result.warning_thresholds_crossed:
            print(f"[Phase 4bn-O] warnings: {result.warning_thresholds_crossed}")
        return 0
    print(
        f"[Phase 4bn-O] FAIL_CLOSED — check {result.failed_check_id}: "
        f"{result.failure_message}"
    )
    print(
        f"[Phase 4bn-O] partial: {result.produced_file_count} parquets produced; "
        f"segment manifest NOT written."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
