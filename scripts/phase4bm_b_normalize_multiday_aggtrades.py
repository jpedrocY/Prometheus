"""Phase 4bm-B — Multi-Day aggTrades Normalization Implementation (BTCUSDT, 90 UTC days).

Standalone orchestrator authorised by the Phase 4bm-B authorization-boundary
prompt and the Phase 4bm-A design memo
(``docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_multi-day-normalization-design-memo.md``).

This script normalises the locked v002 multi-day BTCUSDT aggTrades raw archive
(90 contiguous UTC dates 2024-12-01 through 2025-02-28; 155,153,449 events;
1,943,823,208 bytes) acquired by Phase 4bl-C and admitted by the Phase 4bl-D-R
PASS gate report (SHA ``f9493fd10d1c...6f1c46``) and the Phase 4bl-E Stage-2
raw successor-state (SHA ``a0576ca656bd...1f751d``) into a future normalized
derived dataset family identified as:

- ``dataset_family``: ``microstructure_normalized_aggtrades_v001`` (reused,
  schema is byte-identical to Phase 4bd / Phase 4bc);
- ``dataset_version``: ``v002`` (new; the bounded-source-dataset
  discriminator);
- ``schema_version``: ``v001`` (unchanged).

The orchestrator preserves the Phase 4bd 19-column ``NORMALIZED_SCHEMA_V001``
contract verbatim, applies the Phase 4bm-A 65-criterion strict-fail-closed
validation contract, writes only under the gitignored
``data/microstructure/normalized/`` and ``data/microstructure/manifests/``
namespaces, refuses to overwrite existing artefacts, and preserves the Phase
4aw ``MicrostructureManifest.flip_research_eligible(...)`` always-raises
invariant end-to-end (the new multi-day index manifest is a sibling shape
that mirrors the Phase 4bl-C raw v002 multi-day manifest; it does NOT use
the single-file ``MicrostructureManifest`` data class).

This script is intentionally narrow:

- Python standard library only (``hashlib``, ``json``, ``argparse``,
  ``zipfile``, ``csv``, ``io``, ``os``, ``contextlib``, ``tempfile``,
  ``re``, ``sys``, ``time``, ``datetime``) plus pyarrow plus the Phase 4ax
  / 4bd microstructure scaffold primitives.
- NO network access (no ``urllib``, no ``requests``, no ``httpx``, no
  ``aiohttp``, no ``websockets``, no ``socket``, no ``binance``).
- NO credentials, no ``.env`` reads, no ``.mcp.json`` reads, no MCP, no
  Graphify.
- NO modification of any source raw artefact (v002 raw manifest, v002 raw
  manifest sidecar, v002 acquisition log, v002 acquisition log sidecar, any
  of the 90 v002 raw zips, any of the 90 v002 raw zip sidecars, Phase
  4bl-D-R PASS gate report, Phase 4bl-D-R gate report sidecar, Phase 4bl-E
  successor-state, Phase 4bl-E successor-state sidecar).
- NO modification of any prior derived artefact (Phase 4bd v001 normalized
  parquet, Phase 4bd v001 derived manifest, Phase 4bf v001 derived gate
  report, Phase 4bg-B v001 successor-state, Phase 4bh feature parquet,
  Phase 4bj-C label parquet, etc).
- Refuses to overwrite an existing finalised output file.
- Atomic write-then-rename via ``os.replace`` and ``tempfile.mkstemp``.
- Pre/post SHA256 immutability check across the 4 governance artefacts +
  4 governance sidecars + 90 raw zips + 90 raw zip sidecars (= 188
  immutability witnesses).
- Strict fail-closed semantics: any precondition / per-day / aggregate /
  immutability / governance / quality-gate failure aborts the run BEFORE
  writing the multi-day index manifest. Partial per-day parquets that may
  have been written before the failure are preserved (each is independently
  verifiable via its paired sidecar) but the manifest is NOT written, so
  the v002 derived family is not Stage-0-complete on failure.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
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

# Phase 4ax / 4bd scaffold imports. The CSV iterator and validator are
# reused verbatim from the Phase 4bd single-day normalizer.
from prometheus.research.microstructure.normalize_aggtrades import (  # noqa: E402
    NORMALIZATION_SCHEMA_VERSION,
    NORMALIZED_SCHEMA_V001,
    iter_aggtrade_rows_from_csv,
)
from prometheus.research.microstructure.normalize_io import (  # noqa: E402
    NormalizationIOError,
    assert_manifest_path_under_manifests,
    assert_path_under_microstructure,
    atomic_write_parquet,
    compute_bytes_sha256,
    write_sha256_sidecar,
)

# Locked identity constants (binding per Phase 4bm-A §5 / §6 / §8).
PHASE_ID = "4bm-B"
SOURCE_PHASE_BOUNDARY = "4bl-E"
NORMALIZED_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
NORMALIZED_DATASET_VERSION = "v002"
SCHEMA_VERSION = "v001"
SOURCE_DATASET_FAMILY = "microstructure_raw_aggtrades_v001"
SOURCE_DATASET_VERSION = "v002"
SYMBOL = "BTCUSDT"
EXPECTED_DATE_COUNT = 90
EXPECTED_DATE_START = "2024-12-01"
EXPECTED_DATE_END = "2025-02-28"
EXPECTED_TOTAL_EVENT_COUNT = 155_153_449
UTC_DAY_MS = 86_400_000

# Locked precondition SHAs (Phase 4bm-A §4 + §12.1 1-9).
EXPECTED_SOURCE_MANIFEST_SHA = (
    "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
)
EXPECTED_SOURCE_MANIFEST_SIDECAR_SHA = (
    "adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26"
)
EXPECTED_ACQUISITION_LOG_SHA = (
    "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"
)
EXPECTED_ACQUISITION_LOG_SIDECAR_SHA = (
    "975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958"
)
EXPECTED_GATE_REPORT_SHA = (
    "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"
)
EXPECTED_GATE_REPORT_SIDECAR_SHA = (
    "84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02"
)
EXPECTED_SUCCESSOR_STATE_SHA = (
    "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d"
)
EXPECTED_SUCCESSOR_STATE_SIDECAR_SHA = (
    "63d97bf54e1063f2fd70024d40639db711e9c24d929074cdd63b2db385302b4f"
)

DEFAULT_SOURCE_MANIFEST_REL = (
    "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json"
)
DEFAULT_GATE_REPORT_REL = (
    "data/microstructure/gate-reports/raw/"
    "microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__"
    "1778717359124__69e45280f080.json"
)
DEFAULT_SUCCESSOR_STATE_REL = (
    "data/microstructure/successor-state/"
    "microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__"
    "phase-4bl-e.json"
)
DEFAULT_OUTPUT_ROOT_REL = "data/microstructure/normalized"
DEFAULT_MANIFESTS_ROOT_REL = "data/microstructure/manifests"


# ---------------------------------------------------------------------------
# Result / error types
# ---------------------------------------------------------------------------


class Phase4bmBOrchestrationError(RuntimeError):
    """Raised when the Phase 4bm-B orchestrator fails closed."""


class Phase4bmBValidationError(Phase4bmBOrchestrationError):
    """Raised when a validation criterion (1-65) fails closed."""


@dataclass
class CheckResult:
    """One validation criterion outcome."""

    check_id: str
    title: str
    status: str  # "pass" | "fail"
    detail: str = ""


@dataclass
class PerDayProductionRecord:
    """Per-date production record for the multi-day index manifest."""

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
    source_file_sha256: str
    source_zip_path: str
    status: str


# ---------------------------------------------------------------------------
# SHA helpers (local, mirror normalize_io behaviour without re-importing).
# ---------------------------------------------------------------------------


def _sha256_file(path: Path) -> tuple[str, int]:
    """Return ``(sha256_hex, size_bytes)`` for *path*, streamed."""
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def _utc_date_to_day_start_ms(utc_date: str) -> int:
    """Return UTC ms timestamp for the start of *utc_date*."""
    day = datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(day.timestamp() * 1000)


# ---------------------------------------------------------------------------
# Precondition checks (criteria 1-10).
# ---------------------------------------------------------------------------


@dataclass
class SourceArtefactSet:
    """Resolved on-disk paths and pre-state SHAs for all source artefacts."""

    source_manifest_path: Path
    source_manifest_sha_before: str
    source_manifest_parsed: dict[str, Any]
    source_manifest_sidecar_path: Path
    source_manifest_sidecar_sha_before: str
    acquisition_log_path: Path
    acquisition_log_sha_before: str
    acquisition_log_sidecar_path: Path
    acquisition_log_sidecar_sha_before: str
    gate_report_path: Path
    gate_report_sha_before: str
    gate_report_sidecar_path: Path
    gate_report_sidecar_sha_before: str
    successor_state_path: Path
    successor_state_sha_before: str
    successor_state_sidecar_path: Path
    successor_state_sidecar_sha_before: str
    raw_zip_paths: list[Path]
    raw_zip_sha_before: list[str]
    raw_zip_sidecar_paths: list[Path]
    raw_zip_sidecar_sha_before: list[str]
    raw_zip_size_before: list[int]


def verify_preconditions(
    *,
    source_manifest_path: Path,
    gate_report_path: Path,
    successor_state_path: Path,
    repo_root: Path,
    checks: list[CheckResult],
) -> SourceArtefactSet:
    """Verify Phase 4bm-A §12.1 criteria 1-10 and load source artefacts."""
    # 1. source manifest exists.
    if not source_manifest_path.exists():
        raise Phase4bmBValidationError(
            f"v002 raw manifest missing: {source_manifest_path}"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.1",
            "v002 raw manifest exists at recorded path",
            "pass",
            str(source_manifest_path),
        )
    )

    # 2. source manifest SHA matches.
    source_manifest_sha, _ = _sha256_file(source_manifest_path)
    if source_manifest_sha != EXPECTED_SOURCE_MANIFEST_SHA:
        raise Phase4bmBValidationError(
            f"v002 raw manifest SHA mismatch: got {source_manifest_sha}, "
            f"expected {EXPECTED_SOURCE_MANIFEST_SHA}"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.2",
            "v002 raw manifest SHA256 matches predeclared value",
            "pass",
            source_manifest_sha,
        )
    )

    # 3. source manifest sidecar matches.
    source_manifest_sidecar_path = source_manifest_path.with_suffix(
        source_manifest_path.suffix + ".sha256"
    )
    if not source_manifest_sidecar_path.exists():
        raise Phase4bmBValidationError(
            f"v002 raw manifest sidecar missing: {source_manifest_sidecar_path}"
        )
    source_manifest_sidecar_sha, _ = _sha256_file(source_manifest_sidecar_path)
    if source_manifest_sidecar_sha != EXPECTED_SOURCE_MANIFEST_SIDECAR_SHA:
        raise Phase4bmBValidationError(
            f"v002 raw manifest sidecar SHA mismatch: got "
            f"{source_manifest_sidecar_sha}, expected "
            f"{EXPECTED_SOURCE_MANIFEST_SIDECAR_SHA}"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.3",
            "v002 raw manifest sidecar SHA256 matches predeclared value",
            "pass",
            source_manifest_sidecar_sha,
        )
    )

    # Load manifest JSON.
    parsed = json.loads(source_manifest_path.read_bytes().decode("utf-8"))
    if not isinstance(parsed, dict):
        raise Phase4bmBValidationError(
            "v002 raw manifest is not a JSON object"
        )
    # Cross-check identity.
    if (
        parsed.get("dataset_family") != SOURCE_DATASET_FAMILY
        or parsed.get("dataset_version") != SOURCE_DATASET_VERSION
        or parsed.get("symbol_list") != [SYMBOL]
        or parsed.get("date_count") != EXPECTED_DATE_COUNT
        or parsed.get("total_row_count") != EXPECTED_TOTAL_EVENT_COUNT
        or parsed.get("research_eligible") is not False
        or parsed.get("eligibility_gate_status") != "pending"
    ):
        raise Phase4bmBValidationError(
            "v002 raw manifest identity / locks do not match predeclared design"
        )

    # 4. acquisition log SHA matches.
    acquisition_log_path = source_manifest_path.with_name(
        source_manifest_path.stem + "_acquisition_log.json"
    )
    if not acquisition_log_path.exists():
        raise Phase4bmBValidationError(
            f"v002 acquisition log missing: {acquisition_log_path}"
        )
    acquisition_log_sha, _ = _sha256_file(acquisition_log_path)
    if acquisition_log_sha != EXPECTED_ACQUISITION_LOG_SHA:
        raise Phase4bmBValidationError(
            f"v002 acquisition log SHA mismatch: got {acquisition_log_sha}, "
            f"expected {EXPECTED_ACQUISITION_LOG_SHA}"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.4",
            "v002 acquisition log SHA256 matches predeclared value",
            "pass",
            acquisition_log_sha,
        )
    )

    # 5. acquisition log sidecar SHA matches.
    acquisition_log_sidecar_path = acquisition_log_path.with_suffix(
        acquisition_log_path.suffix + ".sha256"
    )
    if not acquisition_log_sidecar_path.exists():
        raise Phase4bmBValidationError(
            f"v002 acquisition log sidecar missing: {acquisition_log_sidecar_path}"
        )
    acquisition_log_sidecar_sha, _ = _sha256_file(acquisition_log_sidecar_path)
    if acquisition_log_sidecar_sha != EXPECTED_ACQUISITION_LOG_SIDECAR_SHA:
        raise Phase4bmBValidationError(
            "v002 acquisition log sidecar SHA mismatch"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.5",
            "v002 acquisition log sidecar SHA256 matches predeclared value",
            "pass",
            acquisition_log_sidecar_sha,
        )
    )

    # 6. gate report SHA matches.
    if not gate_report_path.exists():
        raise Phase4bmBValidationError(
            f"Phase 4bl-D-R PASS gate report missing: {gate_report_path}"
        )
    gate_report_sha, _ = _sha256_file(gate_report_path)
    if gate_report_sha != EXPECTED_GATE_REPORT_SHA:
        raise Phase4bmBValidationError(
            f"Phase 4bl-D-R gate report SHA mismatch: got {gate_report_sha}, "
            f"expected {EXPECTED_GATE_REPORT_SHA}"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.6",
            "Phase 4bl-D-R PASS gate report SHA256 matches predeclared value",
            "pass",
            gate_report_sha,
        )
    )

    # Cross-check gate verdict for safety.
    gate_parsed = json.loads(gate_report_path.read_bytes().decode("utf-8"))
    if (
        gate_parsed.get("overall_status") != "pass"
        or gate_parsed.get("gate_verdict") != "RAW_MULTIDAY_GATE_PASS"
    ):
        raise Phase4bmBValidationError(
            "Phase 4bl-D-R gate report is not a multi-day PASS"
        )
    # Per Phase 4bb-F canonical-path convention the report_id is the basename
    # without the .json suffix. Fall back to the in-body field only when the
    # writer explicitly recorded one.
    gate_report_id = str(gate_parsed.get("report_id", "")).strip()
    if not gate_report_id:
        gate_report_id = gate_report_path.stem
    if not gate_report_id:
        raise Phase4bmBValidationError(
            "Phase 4bl-D-R gate report has no report_id"
        )

    # 7. gate report sidecar SHA matches.
    gate_report_sidecar_path = gate_report_path.with_suffix(
        gate_report_path.suffix + ".sha256"
    )
    if not gate_report_sidecar_path.exists():
        raise Phase4bmBValidationError(
            f"Phase 4bl-D-R gate report sidecar missing: "
            f"{gate_report_sidecar_path}"
        )
    gate_report_sidecar_sha, _ = _sha256_file(gate_report_sidecar_path)
    if gate_report_sidecar_sha != EXPECTED_GATE_REPORT_SIDECAR_SHA:
        raise Phase4bmBValidationError(
            "Phase 4bl-D-R gate report sidecar SHA mismatch"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.7",
            "Phase 4bl-D-R gate report sidecar SHA256 matches predeclared value",
            "pass",
            gate_report_sidecar_sha,
        )
    )

    # 8. successor-state SHA matches.
    if not successor_state_path.exists():
        raise Phase4bmBValidationError(
            f"Phase 4bl-E successor-state missing: {successor_state_path}"
        )
    successor_state_sha, _ = _sha256_file(successor_state_path)
    if successor_state_sha != EXPECTED_SUCCESSOR_STATE_SHA:
        raise Phase4bmBValidationError(
            f"Phase 4bl-E successor-state SHA mismatch: got "
            f"{successor_state_sha}, expected {EXPECTED_SUCCESSOR_STATE_SHA}"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.8",
            "Phase 4bl-E successor-state SHA256 matches predeclared value",
            "pass",
            successor_state_sha,
        )
    )

    # 9. successor-state sidecar SHA matches.
    successor_state_sidecar_path = successor_state_path.with_suffix(
        successor_state_path.suffix + ".sha256"
    )
    if not successor_state_sidecar_path.exists():
        raise Phase4bmBValidationError(
            f"Phase 4bl-E successor-state sidecar missing: "
            f"{successor_state_sidecar_path}"
        )
    successor_state_sidecar_sha, _ = _sha256_file(successor_state_sidecar_path)
    if successor_state_sidecar_sha != EXPECTED_SUCCESSOR_STATE_SIDECAR_SHA:
        raise Phase4bmBValidationError(
            "Phase 4bl-E successor-state sidecar SHA mismatch"
        )
    checks.append(
        CheckResult(
            "4bm-B.12.1.9",
            "Phase 4bl-E successor-state sidecar SHA256 matches predeclared value",
            "pass",
            successor_state_sidecar_sha,
        )
    )

    # Cross-check successor-state for admissibility.
    succ_parsed = json.loads(successor_state_path.read_bytes().decode("utf-8"))
    if (
        succ_parsed.get("successor_state") != "stage2_raw_admissible"
        or succ_parsed.get("successor_admissibility_status")
        != "admissible_in_principle_policy_level_only"
    ):
        raise Phase4bmBValidationError(
            "Phase 4bl-E successor-state is not Stage-2 raw admissible"
        )

    # 10. all 90 raw zips exist and SHAs match per_file_inventory.
    inventory: list[dict[str, Any]] = list(parsed.get("per_file_inventory", []))
    if len(inventory) != EXPECTED_DATE_COUNT:
        raise Phase4bmBValidationError(
            f"per_file_inventory length {len(inventory)} != "
            f"{EXPECTED_DATE_COUNT}"
        )
    raw_zip_paths: list[Path] = []
    raw_zip_sha_before: list[str] = []
    raw_zip_sidecar_paths: list[Path] = []
    raw_zip_sidecar_sha_before: list[str] = []
    raw_zip_size_before: list[int] = []
    micro_root = repo_root / "data" / "microstructure"
    for entry in inventory:
        rel_zip = str(entry["local_zip_path"])
        # paths are prefixed with "microstructure/" — strip the leading
        # "microstructure/" because we anchor at data/microstructure already.
        if rel_zip.startswith("microstructure/"):
            rel_zip = rel_zip[len("microstructure/") :]
        zip_path = micro_root / rel_zip
        if not zip_path.exists():
            raise Phase4bmBValidationError(
                f"raw zip missing for date {entry['date']}: {zip_path}"
            )
        actual_sha, actual_size = _sha256_file(zip_path)
        expected_sha = str(entry["sha256"])
        expected_size = int(entry["size_bytes"])
        if actual_sha != expected_sha:
            raise Phase4bmBValidationError(
                f"raw zip SHA mismatch for date {entry['date']}: got "
                f"{actual_sha}, expected {expected_sha}"
            )
        if actual_size != expected_size:
            raise Phase4bmBValidationError(
                f"raw zip size mismatch for date {entry['date']}: got "
                f"{actual_size}, expected {expected_size}"
            )

        rel_sidecar = str(entry["local_sidecar_path"])
        if rel_sidecar.startswith("microstructure/"):
            rel_sidecar = rel_sidecar[len("microstructure/") :]
        sidecar_path = micro_root / rel_sidecar
        if not sidecar_path.exists():
            raise Phase4bmBValidationError(
                f"raw zip sidecar missing for date {entry['date']}: "
                f"{sidecar_path}"
            )
        sidecar_sha, _ = _sha256_file(sidecar_path)

        raw_zip_paths.append(zip_path)
        raw_zip_sha_before.append(actual_sha)
        raw_zip_sidecar_paths.append(sidecar_path)
        raw_zip_sidecar_sha_before.append(sidecar_sha)
        raw_zip_size_before.append(actual_size)
    checks.append(
        CheckResult(
            "4bm-B.12.1.10",
            f"all {EXPECTED_DATE_COUNT} v002 raw zip SHAs match per_file_inventory",
            "pass",
            f"{len(raw_zip_paths)} zips verified",
        )
    )

    return SourceArtefactSet(
        source_manifest_path=source_manifest_path,
        source_manifest_sha_before=source_manifest_sha,
        source_manifest_parsed=parsed,
        source_manifest_sidecar_path=source_manifest_sidecar_path,
        source_manifest_sidecar_sha_before=source_manifest_sidecar_sha,
        acquisition_log_path=acquisition_log_path,
        acquisition_log_sha_before=acquisition_log_sha,
        acquisition_log_sidecar_path=acquisition_log_sidecar_path,
        acquisition_log_sidecar_sha_before=acquisition_log_sidecar_sha,
        gate_report_path=gate_report_path,
        gate_report_sha_before=gate_report_sha,
        gate_report_sidecar_path=gate_report_sidecar_path,
        gate_report_sidecar_sha_before=gate_report_sidecar_sha,
        successor_state_path=successor_state_path,
        successor_state_sha_before=successor_state_sha,
        successor_state_sidecar_path=successor_state_sidecar_path,
        successor_state_sidecar_sha_before=successor_state_sidecar_sha,
        raw_zip_paths=raw_zip_paths,
        raw_zip_sha_before=raw_zip_sha_before,
        raw_zip_sidecar_paths=raw_zip_sidecar_paths,
        raw_zip_sidecar_sha_before=raw_zip_sidecar_sha_before,
        raw_zip_size_before=raw_zip_size_before,
    )


# ---------------------------------------------------------------------------
# Per-day normalization
# ---------------------------------------------------------------------------


_PA = None


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
    """Normalise one date's raw zip; return a :class:`PerDayProductionRecord`."""
    import pyarrow as pa  # local import; pyarrow not allowed at module top per
                          # the Phase 4bd convention (already imported via type-only).

    date_str = str(inventory_entry["date"])
    expected_event_count = int(inventory_entry["row_count"])
    expected_first_ms = int(inventory_entry["first_trade_time_ms"])
    expected_last_ms = int(inventory_entry["last_trade_time_ms"])
    expected_min_a = int(inventory_entry["min_agg_trade_id"])
    expected_max_a = int(inventory_entry["max_agg_trade_id"])

    # Open ZIP in memory.
    with zipfile.ZipFile(raw_zip_path) as zf:
        members = zf.namelist()
        if len(members) != 1:
            raise Phase4bmBValidationError(
                f"date {date_str}: zip must contain exactly one CSV member; "
                f"got {len(members)}"
            )
        with zf.open(members[0]) as raw:
            csv_text = raw.read().decode("utf-8")

    payloads = iter_aggtrade_rows_from_csv(csv_text)
    if len(payloads) != expected_event_count:
        raise Phase4bmBValidationError(
            f"date {date_str}: row count {len(payloads)} != manifest "
            f"row_count {expected_event_count}"
        )

    day_start_ms = _utc_date_to_day_start_ms(date_str)
    day_end_excl_ms = day_start_ms + UTC_DAY_MS

    # Build column data with full per-row verification.
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
        T = int(payload.trade_time_ms)
        if a in seen_a:
            raise Phase4bmBValidationError(
                f"date {date_str}: duplicate agg_trade_id {a} at row {row_index}"
            )
        seen_a.add(a)
        if a < prev_a:
            raise Phase4bmBValidationError(
                f"date {date_str}: agg_trade_id non-monotone at row "
                f"{row_index}: {a} < {prev_a}"
            )
        if prev_t > T:
            raise Phase4bmBValidationError(
                f"date {date_str}: transact_time_ms non-monotone at row "
                f"{row_index}: {T} < {prev_t}"
            )
        if not (day_start_ms <= T < day_end_excl_ms):
            raise Phase4bmBValidationError(
                f"date {date_str}: transact_time_ms {T} outside half-open "
                f"day bound [{day_start_ms}, {day_end_excl_ms})"
            )
        prev_a = a
        prev_t = T
        if a < min_a:
            min_a = a
        if a > max_a:
            max_a = a
        if row_index == 0:
            first_ms = T
        last_ms = T

        col_agg_trade_id.append(a)
        col_price.append(str(payload.price))
        col_quantity.append(str(payload.quantity))
        col_first_trade_id.append(int(payload.first_trade_id))
        col_last_trade_id.append(int(payload.last_trade_id))
        col_transact_time_ms.append(T)
        col_is_buyer_maker.append(bool(payload.buyer_is_maker))
        col_row_index.append(row_index)

    # Cross-check inventory-vs-recomputed.
    if first_ms != expected_first_ms:
        raise Phase4bmBValidationError(
            f"date {date_str}: first_transact_time_ms {first_ms} != "
            f"inventory {expected_first_ms}"
        )
    if last_ms != expected_last_ms:
        raise Phase4bmBValidationError(
            f"date {date_str}: last_transact_time_ms {last_ms} != "
            f"inventory {expected_last_ms}"
        )
    if min_a != expected_min_a:
        raise Phase4bmBValidationError(
            f"date {date_str}: min_agg_trade_id {min_a} != inventory "
            f"{expected_min_a}"
        )
    if max_a != expected_max_a:
        raise Phase4bmBValidationError(
            f"date {date_str}: max_agg_trade_id {max_a} != inventory "
            f"{expected_max_a}"
        )

    # Build constant lineage columns.
    n = len(payloads)
    col_dataset_family = [NORMALIZED_DATASET_FAMILY] * n
    col_dataset_version = [NORMALIZED_DATASET_VERSION] * n
    col_source_dataset_family = [SOURCE_DATASET_FAMILY] * n
    col_source_dataset_version = [SOURCE_DATASET_VERSION] * n
    col_symbol = [SYMBOL] * n
    col_utc_date = [date_str] * n
    col_source_file_sha256 = [raw_zip_sha] * n
    col_source_manifest_sha256 = [source_manifest_sha] * n
    col_source_gate_report_id = [gate_report_id] * n
    col_source_gate_report_sha256 = [gate_report_sha] * n
    col_normalization_schema_version = [NORMALIZATION_SCHEMA_VERSION] * n

    schema = _pa_schema()
    # Schema equality assertion — fail closed if anything deviates from
    # NORMALIZED_SCHEMA_V001.
    if tuple(schema.names) != NORMALIZED_SCHEMA_V001:
        raise Phase4bmBValidationError(
            f"date {date_str}: pyarrow schema names {tuple(schema.names)} != "
            f"NORMALIZED_SCHEMA_V001 {NORMALIZED_SCHEMA_V001}"
        )

    table = pa.Table.from_pydict(
        {
            "dataset_family": col_dataset_family,
            "dataset_version": col_dataset_version,
            "source_dataset_family": col_source_dataset_family,
            "source_dataset_version": col_source_dataset_version,
            "symbol": col_symbol,
            "utc_date": col_utc_date,
            "agg_trade_id": col_agg_trade_id,
            "price": col_price,
            "quantity": col_quantity,
            "first_trade_id": col_first_trade_id,
            "last_trade_id": col_last_trade_id,
            "transact_time_ms": col_transact_time_ms,
            "is_buyer_maker": col_is_buyer_maker,
            "source_file_sha256": col_source_file_sha256,
            "source_manifest_sha256": col_source_manifest_sha256,
            "source_gate_report_id": col_source_gate_report_id,
            "source_gate_report_sha256": col_source_gate_report_sha256,
            "row_index": col_row_index,
            "normalization_schema_version": col_normalization_schema_version,
        },
        schema=schema,
    )

    # Derive output path. Layout (relative to output_root):
    # microstructure_normalized_aggtrades_v001__v002/<SYMBOL>/<YYYY>/<MM>/
    # <SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet
    #
    # Family-directory segment is version-suffixed (`__<dataset_version>`) so
    # the v002 multi-day output coexists cleanly with the existing v001
    # single-day Phase 4bd Parquet (per Phase 4bm-A design memo §7 "the
    # 2025-01-15 v002 file coexists with the existing v001 single-day Phase
    # 4bd Parquet"). This mirrors the existing manifest filename convention
    # (`microstructure_normalized_aggtrades_v001__v001.json` for v001 and
    # `microstructure_normalized_aggtrades_v001__v002.json` for v002).
    yyyy, mm, _dd = date_str.split("-")
    family_dir = f"{NORMALIZED_DATASET_FAMILY}__{NORMALIZED_DATASET_VERSION}"
    target = (
        output_root
        / family_dir
        / SYMBOL
        / yyyy
        / mm
        / f"{SYMBOL}-aggTrades-{date_str}.parquet"
    )
    target.parent.mkdir(parents=True, exist_ok=True)

    # Atomic Parquet write (reuses Phase 4bd primitive).
    parquet_sha, parquet_size = atomic_write_parquet(
        target, table, refuse_overwrite=refuse_overwrite
    )

    # Paired sidecar.
    sidecar_target = target.with_suffix(target.suffix + ".sha256")
    sidecar_sha, sidecar_size = write_sha256_sidecar(
        sidecar_target,
        target_filename=target.name,
        sha256_hex=parquet_sha,
        refuse_overwrite=refuse_overwrite,
    )

    # Forbidden-substring scan on schema names.
    forbidden = (
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
    )
    for col in NORMALIZED_SCHEMA_V001:
        col_lower = col.lower()
        for needle in forbidden:
            if needle in col_lower:
                raise Phase4bmBValidationError(
                    f"date {date_str}: forbidden substring {needle!r} in "
                    f"column name {col!r}"
                )

    # Build per-day production record.
    local_parquet_rel = "microstructure/" + str(
        target.relative_to(target.parents[5])
    ).replace(os.sep, "/")
    # ^ Walk back from <SYMBOL>-aggTrades-<DATE>.parquet to data/microstructure
    # parents: 0=mm, 1=yyyy, 2=SYMBOL, 3=<family>__<version>,
    # 4=normalized, 5=microstructure
    local_sidecar_rel = local_parquet_rel + ".sha256"

    # Source zip relative path mirrors inventory entry's local_zip_path.
    source_zip_path = str(inventory_entry["local_zip_path"])

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
        source_file_sha256=raw_zip_sha,
        source_zip_path=source_zip_path,
        status="produced_verified",
    )


# ---------------------------------------------------------------------------
# Multi-day index manifest
# ---------------------------------------------------------------------------


def build_multiday_manifest(
    *,
    artefacts: SourceArtefactSet,
    per_day_records: Sequence[PerDayProductionRecord],
    gate_report_id: str,
    gate_report_code_commit_sha: str,
    base_commit_sha: str,
    code_commit_sha: str,
    capture_config_hash: str,
    created_at_unix_ms: int,
    created_at_utc: str,
    source_manifest_path: Path,
    repo_root: Path,
) -> dict[str, Any]:
    """Construct the v002 derived multi-day index manifest dict."""

    def _rel_to_repo(p: Path) -> str:
        return str(p.resolve().relative_to(repo_root.resolve())).replace(
            os.sep, "/"
        )

    parsed = artefacts.source_manifest_parsed
    date_list = list(parsed.get("date_list", []))
    inventory_entries: list[dict[str, Any]] = []
    for record in per_day_records:
        inventory_entries.append(
            {
                "date": record.date,
                "symbol": record.symbol,
                "local_parquet_path": record.local_parquet_path,
                "local_sidecar_path": record.local_sidecar_path,
                "parquet_sha256": record.parquet_sha256,
                "sidecar_sha256": record.sidecar_sha256,
                "parquet_size_bytes": record.parquet_size_bytes,
                "sidecar_size_bytes": record.sidecar_size_bytes,
                "event_count": record.event_count,
                "first_transact_time_ms": record.first_transact_time_ms,
                "last_transact_time_ms": record.last_transact_time_ms,
                "min_agg_trade_id": record.min_agg_trade_id,
                "max_agg_trade_id": record.max_agg_trade_id,
                "source_file_sha256": record.source_file_sha256,
                "source_zip_path": record.source_zip_path,
                "status": record.status,
            }
        )

    total_event_count = sum(r.event_count for r in per_day_records)
    produced_file_count = len(per_day_records)

    governance_labels: dict[str, str] = {
        "phase": PHASE_ID,
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "source_dataset_family": SOURCE_DATASET_FAMILY,
        "source_dataset_version": SOURCE_DATASET_VERSION,
        "source_manifest_path": _rel_to_repo(artefacts.source_manifest_path),
        "source_manifest_sha256": artefacts.source_manifest_sha_before,
        "source_gate_report_id": gate_report_id,
        "source_gate_report_sha256": artefacts.gate_report_sha_before,
        "source_gate_report_code_commit_sha": gate_report_code_commit_sha,
        "source_successor_state_sha256": artefacts.successor_state_sha_before,
        "validator": "phase_4ax_aggtrades_v001",
        "stop_trigger_domain": "trade_price_backtest_candidate",
        "feature_computation": "forbidden",
        "strategy_use": "forbidden",
        "phase_4bm_b_no_successor_authorization": "true",
        "multi_day": "true",
    }

    return {
        "dataset_family": NORMALIZED_DATASET_FAMILY,
        "dataset_version": NORMALIZED_DATASET_VERSION,
        "schema_version": SCHEMA_VERSION,
        "symbol_list": [SYMBOL],
        "date_start": EXPECTED_DATE_START,
        "date_end": EXPECTED_DATE_END,
        "date_count": EXPECTED_DATE_COUNT,
        "date_list": date_list,
        "expected_file_count": EXPECTED_DATE_COUNT,
        "produced_file_count": produced_file_count,
        "total_event_count": total_event_count,
        "per_file_inventory": inventory_entries,
        "source_dataset_family": SOURCE_DATASET_FAMILY,
        "source_dataset_version": SOURCE_DATASET_VERSION,
        "source_manifest_path": _rel_to_repo(artefacts.source_manifest_path),
        "source_manifest_sha256": artefacts.source_manifest_sha_before,
        "source_acquisition_log_path": _rel_to_repo(
            artefacts.acquisition_log_path
        ),
        "source_acquisition_log_sha256": artefacts.acquisition_log_sha_before,
        "source_gate_report_id": gate_report_id,
        "source_gate_report_path": _rel_to_repo(artefacts.gate_report_path),
        "source_gate_report_sha256": artefacts.gate_report_sha_before,
        "source_successor_state_path": _rel_to_repo(
            artefacts.successor_state_path
        ),
        "source_successor_state_sha256": artefacts.successor_state_sha_before,
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "governance_labels": governance_labels,
        "invalid_windows": [],
        "created_at_unix_ms": created_at_unix_ms,
        "created_at_utc": created_at_utc,
        "code_commit_sha": code_commit_sha,
        "base_commit_sha": base_commit_sha,
        "capture_config_hash": capture_config_hash,
        "phase": PHASE_ID,
    }


def _atomic_write_index_manifest(
    path: Path, obj: Mapping[str, Any], *, refuse_overwrite: bool = True
) -> tuple[str, int]:
    """Atomic write of the multi-day index manifest under
    ``data/microstructure/manifests/``. Mirrors normalize_io.atomic_write_json
    but without the v001-flavoured filename constraint.
    """
    if not isinstance(path, Path):
        raise NormalizationIOError("path must be a pathlib.Path")
    assert_manifest_path_under_manifests(path, label="multi-day manifest path")
    if refuse_overwrite and path.exists():
        raise NormalizationIOError(f"refusing to overwrite existing file: {path}")
    tmp_companion = path.with_suffix(path.suffix + ".tmp")
    if tmp_companion.exists():
        raise NormalizationIOError(f"stale .tmp companion exists: {tmp_companion}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(dict(obj), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    fd, tmp_str = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
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


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------


@dataclass
class OrchestrationResult:
    """Top-level result of one Phase 4bm-B normalisation run."""

    overall_status: str  # "pass" | "fail_closed"
    output_manifest_path: Path | None
    output_manifest_sha256: str | None
    output_manifest_sidecar_path: Path | None
    output_manifest_sidecar_sha256: str | None
    produced_file_count: int
    total_event_count: int
    per_day_records: list[PerDayProductionRecord] = field(default_factory=list)
    checks: list[CheckResult] = field(default_factory=list)
    failed_check_id: str | None = None
    failure_message: str | None = None
    wall_clock_seconds: float = 0.0


def _git_head_sha(repo_root: Path) -> str:
    head_file = repo_root / ".git" / "HEAD"
    if not head_file.exists():
        return "unknown"
    head_ref = head_file.read_text(encoding="utf-8").strip()
    if head_ref.startswith("ref:"):
        ref_path = head_ref.split(" ", 1)[1].strip()
        sha_file = repo_root / ".git" / ref_path
        if not sha_file.exists():
            packed = repo_root / ".git" / "packed-refs"
            if packed.exists():
                for line in packed.read_text(encoding="utf-8").splitlines():
                    if line.startswith("#") or not line.strip():
                        continue
                    parts = line.split(" ", 1)
                    if len(parts) == 2 and parts[1] == ref_path:
                        return parts[0].strip()
            return "unknown"
        return sha_file.read_text(encoding="utf-8").strip()
    return head_ref


def run(
    *,
    source_manifest_path: Path,
    gate_report_path: Path,
    successor_state_path: Path,
    output_root: Path,
    manifests_root: Path,
    repo_root: Path,
    refuse_overwrite: bool = True,
    code_commit_sha: str | None = None,
    base_commit_sha: str | None = None,
) -> OrchestrationResult:
    """Run the full Phase 4bm-B normalisation."""
    start = time.monotonic()
    checks: list[CheckResult] = []
    failed_id: str | None = None
    failure_msg: str | None = None
    per_day_records: list[PerDayProductionRecord] = []
    manifest_path: Path | None = None
    manifest_sha: str | None = None
    manifest_sidecar_path: Path | None = None
    manifest_sidecar_sha: str | None = None

    assert_path_under_microstructure(output_root, label="output_root")
    assert_manifest_path_under_manifests(
        manifests_root / "x.json", label="manifests_root probe"
    )

    artefacts: SourceArtefactSet | None = None
    try:
        # --- 12.1 Precondition checks (criteria 1-10) ---
        artefacts = verify_preconditions(
            source_manifest_path=source_manifest_path,
            gate_report_path=gate_report_path,
            successor_state_path=successor_state_path,
            repo_root=repo_root,
            checks=checks,
        )

        gate_parsed = json.loads(gate_report_path.read_bytes().decode("utf-8"))
        gate_report_id = str(gate_parsed.get("report_id", "")).strip()
        if not gate_report_id:
            gate_report_id = gate_report_path.stem
        gate_report_code_commit_sha = str(
            gate_parsed.get("code_commit_sha", "unknown")
        ).strip() or "unknown"

        commit_sha = code_commit_sha or _git_head_sha(repo_root)
        base_sha = base_commit_sha or commit_sha

        capture_config_hash = compute_bytes_sha256(
            json.dumps(
                {
                    "phase": PHASE_ID,
                    "schema_version": SCHEMA_VERSION,
                    "schema_columns": list(NORMALIZED_SCHEMA_V001),
                    "dataset_family": NORMALIZED_DATASET_FAMILY,
                    "dataset_version": NORMALIZED_DATASET_VERSION,
                    "source_dataset_family": SOURCE_DATASET_FAMILY,
                    "source_dataset_version": SOURCE_DATASET_VERSION,
                    "source_manifest_sha256": artefacts.source_manifest_sha_before,
                    "source_gate_report_sha256": artefacts.gate_report_sha_before,
                    "source_successor_state_sha256": (
                        artefacts.successor_state_sha_before
                    ),
                    "expected_date_count": EXPECTED_DATE_COUNT,
                    "expected_total_event_count": EXPECTED_TOTAL_EVENT_COUNT,
                },
                sort_keys=True,
            ).encode("utf-8")
        )

        # --- 12.2 Per-day normalisation (criteria 11-31 per date × 90) ---
        inventory_entries = list(
            artefacts.source_manifest_parsed.get("per_file_inventory", [])
        )

        # Also verify date_list ordering / no duplicates / matches inventory.
        date_list = list(artefacts.source_manifest_parsed.get("date_list", []))
        if len(date_list) != EXPECTED_DATE_COUNT:
            raise Phase4bmBValidationError(
                f"date_list length {len(date_list)} != {EXPECTED_DATE_COUNT}"
            )
        if len(set(date_list)) != EXPECTED_DATE_COUNT:
            raise Phase4bmBValidationError("date_list contains duplicates")
        if [e["date"] for e in inventory_entries] != date_list:
            raise Phase4bmBValidationError(
                "per_file_inventory dates do not match date_list ordering"
            )

        for i, entry in enumerate(inventory_entries):
            record = normalize_one_date(
                inventory_entry=entry,
                raw_zip_path=artefacts.raw_zip_paths[i],
                raw_zip_sha=artefacts.raw_zip_sha_before[i],
                source_manifest_sha=artefacts.source_manifest_sha_before,
                gate_report_id=gate_report_id,
                gate_report_sha=artefacts.gate_report_sha_before,
                output_root=output_root,
                refuse_overwrite=refuse_overwrite,
            )
            per_day_records.append(record)
        checks.append(
            CheckResult(
                "4bm-B.12.2",
                f"per-day normalisation completed for {EXPECTED_DATE_COUNT} dates",
                "pass",
                f"{len(per_day_records)} parquets produced",
            )
        )

        # --- 12.3 Aggregate / multi-day checks ---
        if len(per_day_records) != EXPECTED_DATE_COUNT:
            raise Phase4bmBValidationError(
                f"produced_file_count {len(per_day_records)} != "
                f"{EXPECTED_DATE_COUNT}"
            )
        total_events = sum(r.event_count for r in per_day_records)
        if total_events != EXPECTED_TOTAL_EVENT_COUNT:
            raise Phase4bmBValidationError(
                f"total_event_count {total_events} != "
                f"{EXPECTED_TOTAL_EVENT_COUNT}"
            )
        checks.append(
            CheckResult(
                "4bm-B.12.3.34",
                "produced_file_count == 90",
                "pass",
                str(len(per_day_records)),
            )
        )
        checks.append(
            CheckResult(
                "4bm-B.12.3.35",
                "total_event_count matches v002 raw manifest exactly",
                "pass",
                str(total_events),
            )
        )

        # Adjacent-date overlap check.
        for i in range(len(per_day_records) - 1):
            d_i = per_day_records[i]
            d_j = per_day_records[i + 1]
            if d_i.last_transact_time_ms >= d_j.first_transact_time_ms:
                raise Phase4bmBValidationError(
                    f"adjacent-date overlap between {d_i.date} (last "
                    f"{d_i.last_transact_time_ms}) and {d_j.date} (first "
                    f"{d_j.first_transact_time_ms})"
                )
        checks.append(
            CheckResult(
                "4bm-B.12.3.39",
                "adjacent-date overlap check passes for all 89 pairs",
                "pass",
                "no overlap detected",
            )
        )

        # --- 12.4 Lineage / immutability checks (raw artefact pre/post) ---
        # Pre/post hash equality across all governance artefacts and raw zips.
        manifest_sha_after, _ = _sha256_file(artefacts.source_manifest_path)
        if manifest_sha_after != artefacts.source_manifest_sha_before:
            raise Phase4bmBValidationError(
                "v002 raw manifest mutated during run"
            )
        manifest_sidecar_sha_after, _ = _sha256_file(
            artefacts.source_manifest_sidecar_path
        )
        if (
            manifest_sidecar_sha_after
            != artefacts.source_manifest_sidecar_sha_before
        ):
            raise Phase4bmBValidationError(
                "v002 raw manifest sidecar mutated during run"
            )
        acq_log_sha_after, _ = _sha256_file(artefacts.acquisition_log_path)
        if acq_log_sha_after != artefacts.acquisition_log_sha_before:
            raise Phase4bmBValidationError(
                "v002 acquisition log mutated during run"
            )
        acq_log_sidecar_sha_after, _ = _sha256_file(
            artefacts.acquisition_log_sidecar_path
        )
        if (
            acq_log_sidecar_sha_after
            != artefacts.acquisition_log_sidecar_sha_before
        ):
            raise Phase4bmBValidationError(
                "v002 acquisition log sidecar mutated during run"
            )
        for i, zp in enumerate(artefacts.raw_zip_paths):
            after_sha, after_size = _sha256_file(zp)
            if after_sha != artefacts.raw_zip_sha_before[i]:
                raise Phase4bmBValidationError(
                    f"raw zip {zp} mutated during run"
                )
            if after_size != artefacts.raw_zip_size_before[i]:
                raise Phase4bmBValidationError(
                    f"raw zip {zp} size changed during run"
                )
        for i, sp in enumerate(artefacts.raw_zip_sidecar_paths):
            after_sha, _ = _sha256_file(sp)
            if after_sha != artefacts.raw_zip_sidecar_sha_before[i]:
                raise Phase4bmBValidationError(
                    f"raw zip sidecar {sp} mutated during run"
                )
        gate_report_sha_after, _ = _sha256_file(artefacts.gate_report_path)
        if gate_report_sha_after != artefacts.gate_report_sha_before:
            raise Phase4bmBValidationError(
                "Phase 4bl-D-R gate report mutated during run"
            )
        gate_report_sidecar_sha_after, _ = _sha256_file(
            artefacts.gate_report_sidecar_path
        )
        if (
            gate_report_sidecar_sha_after
            != artefacts.gate_report_sidecar_sha_before
        ):
            raise Phase4bmBValidationError(
                "Phase 4bl-D-R gate report sidecar mutated during run"
            )
        successor_state_sha_after, _ = _sha256_file(artefacts.successor_state_path)
        if successor_state_sha_after != artefacts.successor_state_sha_before:
            raise Phase4bmBValidationError(
                "Phase 4bl-E successor-state mutated during run"
            )
        successor_state_sidecar_sha_after, _ = _sha256_file(
            artefacts.successor_state_sidecar_path
        )
        if (
            successor_state_sidecar_sha_after
            != artefacts.successor_state_sidecar_sha_before
        ):
            raise Phase4bmBValidationError(
                "Phase 4bl-E successor-state sidecar mutated during run"
            )
        checks.append(
            CheckResult(
                "4bm-B.12.4",
                "all 188 lineage / immutability witnesses byte-identical pre/post",
                "pass",
                "4 governance + 4 sidecars + 90 zips + 90 zip sidecars all stable",
            )
        )

        # --- 12.5 Governance / boundary checks happen at manifest build below ---

        # --- Build multi-day index manifest ---
        now_unix_ms = int(time.time() * 1000)
        now_utc = datetime.now(UTC).isoformat()
        manifest_dict = build_multiday_manifest(
            artefacts=artefacts,
            per_day_records=per_day_records,
            gate_report_id=gate_report_id,
            gate_report_code_commit_sha=gate_report_code_commit_sha,
            base_commit_sha=base_sha,
            code_commit_sha=commit_sha,
            capture_config_hash=capture_config_hash,
            created_at_unix_ms=now_unix_ms,
            created_at_utc=now_utc,
            source_manifest_path=artefacts.source_manifest_path,
            repo_root=repo_root,
        )

        # --- 12.5 governance checks ---
        if manifest_dict["research_eligible"] is not False:
            raise Phase4bmBValidationError(
                "multi-day manifest research_eligible must be False"
            )
        if manifest_dict["eligibility_gate_status"] != "pending":
            raise Phase4bmBValidationError(
                "multi-day manifest eligibility_gate_status must be 'pending'"
            )
        gov = manifest_dict["governance_labels"]
        if gov.get("feature_computation") != "forbidden":
            raise Phase4bmBValidationError(
                "governance_labels.feature_computation must be 'forbidden'"
            )
        if gov.get("strategy_use") != "forbidden":
            raise Phase4bmBValidationError(
                "governance_labels.strategy_use must be 'forbidden'"
            )
        if gov.get("phase_4bm_b_no_successor_authorization") != "true":
            raise Phase4bmBValidationError(
                "governance_labels.phase_4bm_b_no_successor_authorization "
                "must be 'true'"
            )
        checks.append(
            CheckResult(
                "4bm-B.12.5",
                "governance / boundary checks pass",
                "pass",
                "research_eligible=False; eligibility_gate_status=pending; "
                "forbidden labels locked",
            )
        )

        # --- Write multi-day manifest atomically ---
        manifest_path = (
            manifests_root
            / f"{NORMALIZED_DATASET_FAMILY}__{NORMALIZED_DATASET_VERSION}.json"
        )
        manifest_sha, _ = _atomic_write_index_manifest(
            manifest_path, manifest_dict, refuse_overwrite=refuse_overwrite
        )
        manifest_sidecar_path = manifest_path.with_suffix(
            manifest_path.suffix + ".sha256"
        )
        manifest_sidecar_sha, _ = write_sha256_sidecar(
            manifest_sidecar_path,
            target_filename=manifest_path.name,
            sha256_hex=manifest_sha,
            refuse_overwrite=refuse_overwrite,
        )
        checks.append(
            CheckResult(
                "4bm-B.12.3.32",
                "multi-day index manifest written",
                "pass",
                str(manifest_path),
            )
        )
        checks.append(
            CheckResult(
                "4bm-B.12.3.33",
                "multi-day index manifest sidecar written",
                "pass",
                str(manifest_sidecar_path),
            )
        )

        wall = time.monotonic() - start
        return OrchestrationResult(
            overall_status="pass",
            output_manifest_path=manifest_path,
            output_manifest_sha256=manifest_sha,
            output_manifest_sidecar_path=manifest_sidecar_path,
            output_manifest_sidecar_sha256=manifest_sidecar_sha,
            produced_file_count=len(per_day_records),
            total_event_count=sum(r.event_count for r in per_day_records),
            per_day_records=per_day_records,
            checks=checks,
            wall_clock_seconds=wall,
        )
    except Phase4bmBValidationError as exc:
        failed_id = checks[-1].check_id if checks else "4bm-B.precondition"
        failure_msg = str(exc)
        wall = time.monotonic() - start
        return OrchestrationResult(
            overall_status="fail_closed",
            output_manifest_path=None,
            output_manifest_sha256=None,
            output_manifest_sidecar_path=None,
            output_manifest_sidecar_sha256=None,
            produced_file_count=len(per_day_records),
            total_event_count=sum(r.event_count for r in per_day_records),
            per_day_records=per_day_records,
            checks=checks,
            failed_check_id=failed_id,
            failure_message=failure_msg,
            wall_clock_seconds=wall,
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Phase 4bm-B — Multi-Day aggTrades Normalization Implementation. "
            "Reads v002 raw artefacts read-only, produces 90 normalized "
            "Parquet files + 90 sidecars + 1 multi-day index manifest + 1 "
            "manifest sidecar under data/microstructure/."
        )
    )
    p.add_argument(
        "--source-manifest",
        type=Path,
        default=None,
        help="Path to v002 raw manifest (defaults to repo path).",
    )
    p.add_argument(
        "--gate-report",
        type=Path,
        default=None,
        help="Path to Phase 4bl-D-R PASS gate report.",
    )
    p.add_argument(
        "--successor-state",
        type=Path,
        default=None,
        help="Path to Phase 4bl-E successor-state JSON.",
    )
    p.add_argument(
        "--output-root",
        type=Path,
        default=None,
        help="Output root (must be under data/microstructure).",
    )
    p.add_argument(
        "--manifests-root",
        type=Path,
        default=None,
        help="Manifests root (must be under data/microstructure/manifests).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Inspect / verify preconditions then exit without writing.",
    )
    p.add_argument(
        "--allow-overwrite",
        action="store_true",
        help="Allow overwriting existing outputs (not recommended).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    repo_root = _REPO_ROOT
    source_manifest_path = (
        args.source_manifest
        if args.source_manifest is not None
        else repo_root / DEFAULT_SOURCE_MANIFEST_REL
    )
    gate_report_path = (
        args.gate_report
        if args.gate_report is not None
        else repo_root / DEFAULT_GATE_REPORT_REL
    )
    successor_state_path = (
        args.successor_state
        if args.successor_state is not None
        else repo_root / DEFAULT_SUCCESSOR_STATE_REL
    )
    output_root = (
        args.output_root
        if args.output_root is not None
        else repo_root / DEFAULT_OUTPUT_ROOT_REL
    )
    manifests_root = (
        args.manifests_root
        if args.manifests_root is not None
        else repo_root / DEFAULT_MANIFESTS_ROOT_REL
    )

    output_root.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        checks: list[CheckResult] = []
        try:
            verify_preconditions(
                source_manifest_path=source_manifest_path,
                gate_report_path=gate_report_path,
                successor_state_path=successor_state_path,
                repo_root=repo_root,
                checks=checks,
            )
        except Phase4bmBValidationError as exc:
            print(f"[dry-run] PRECONDITION FAILED: {exc}")
            for c in checks:
                print(f"  - {c.check_id} {c.status.upper()}: {c.title}")
            return 1
        print("[dry-run] preconditions PASS")
        for c in checks:
            print(f"  - {c.check_id} {c.status.upper()}: {c.title}")
        return 0

    result = run(
        source_manifest_path=source_manifest_path,
        gate_report_path=gate_report_path,
        successor_state_path=successor_state_path,
        output_root=output_root,
        manifests_root=manifests_root,
        repo_root=repo_root,
        refuse_overwrite=not args.allow_overwrite,
    )
    if result.overall_status == "pass":
        print(
            f"[Phase 4bm-B] PASS — produced "
            f"{result.produced_file_count} parquets totalling "
            f"{result.total_event_count} events in "
            f"{result.wall_clock_seconds:.1f}s; "
            f"manifest at {result.output_manifest_path} "
            f"(sha256={result.output_manifest_sha256})"
        )
        return 0
    print(
        f"[Phase 4bm-B] FAIL_CLOSED — check {result.failed_check_id}: "
        f"{result.failure_message}"
    )
    print(
        f"[Phase 4bm-B] partial: {result.produced_file_count} parquets "
        f"produced; manifest NOT written; multi-day index manifest absent."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
