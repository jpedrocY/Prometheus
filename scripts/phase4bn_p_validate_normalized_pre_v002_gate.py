"""Phase 4bn-P — Normalized-Layer Eligibility Gate for the Pre-V002 BTCUSDT
aggTrades Normalized Segment.

Bounded, read-only gate over the Phase 4bn-O local normalized pre-v002 segment
(BTCUSDT / Binance USDⓈ-M futures / aggTrades; 2024-03-01 .. 2024-11-30
inclusive UTC; 275 dates; 400,001,695 events). It validates that the local
normalized segment is structurally complete, internally consistent,
manifest-consistent, predecessor-consistent, schema-consistent, path-consistent,
sidecar-consistent, and governance-consistent, and writes at most one local
gitignored normalized-layer gate report + canonical sidecar under
``data/microstructure/gate-reports/normalized/``.

The gate is **read-only** with respect to every data artefact:

- it never mutates the segment manifest, any Parquet, any sidecar, the
  published ``__v002`` family, or any predecessor artefact;
- it never flips ``research_eligible`` and never transitions
  ``eligibility_gate_status`` (a passing gate authorizes nothing);
- it performs NO network I/O, NO acquisition, NO normalization rerun, NO raw
  gate rerun, NO features / labels / ML / diagnostics / strategy / backtests,
  NO database / Parquet compaction / storage migration / v003;
- it never reads the v002 terminal raw window, the sealed-test split, or any
  published ``__v002`` Parquet / manifest (the published ``__v002`` is treated
  by reference only).

Performance discipline (mirrors the Phase 4bm-D multi-day gate): for every one
of the 275 files the gate streams the Parquet SHA256 (full hash integrity),
records the on-disk size, and reads ``ParquetFile.metadata`` for the row count
and column names (no row-group materialisation); full ``pyarrow.Table`` content
checks (half-open UTC bounds, agg-id monotonicity/uniqueness, first/last/min/max
vs the manifest inventory, dtypes) are bounded to a small predeclared date
sample. Per-file SHA equality to the manifest inventory transitively confirms
the non-sampled files' content matches what Phase 4bn-O verified and recorded.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure.normalize_aggtrades import (  # noqa: E402
    NORMALIZATION_SCHEMA_VERSION,
    NORMALIZED_SCHEMA_V001,
)
from prometheus.research.microstructure.normalize_io import (  # noqa: E402
    NormalizationIOError,
    assert_path_under_microstructure,
    compute_bytes_sha256,
    compute_file_sha256,
    write_sha256_sidecar,
)

# ---------------------------------------------------------------------------
# Locked identity / expectation constants
# ---------------------------------------------------------------------------

PHASE_ID = "phase-4bn-p"
PHASE_ID_TOKEN = "4bn_p"
REPORT_SCHEMA_VERSION = "v001"

BASE_MAIN_SHA = "3fd795ceac4fc6804015301f7f21b4ef7b22f78b"
BASE_MAIN_SHORT = "3fd795ceac4f"

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

# The segment under gate was produced by Phase 4bn-O; its family-dir token is fixed.
FAMILY_DIR_NAME = "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o"
SEGMENT_MANIFEST_BASENAME = f"{FAMILY_DIR_NAME}.json"
PUBLISHED_V002_FAMILY_DIR_NAME = (
    f"{NORMALIZED_DATASET_FAMILY}__{NORMALIZED_DATASET_VERSION}"
)
PUBLISHED_V002_NORMALIZED_MANIFEST_REL = (
    "data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json"
)

EXPECTED_DATE_COUNT = 275
EXPECTED_DATE_START = "2024-03-01"
EXPECTED_DATE_END = "2024-11-30"
EXPECTED_TOTAL_EVENT_COUNT = 400_001_695
EXPECTED_TOTAL_FOOTPRINT_BYTES = 3_954_532_918
FULL_ENVELOPE_START = "2024-03-01"
FULL_ENVELOPE_END = "2025-02-28"
UTC_DAY_MS = 86_400_000

V002_TERMINAL_START = "2024-12-01"
V002_TERMINAL_END = "2025-02-28"
SEALED_TEST_START = "2025-02-14"
SEALED_TEST_END = "2025-02-28"

EXPECTED_MANIFEST_SHA = (
    "0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa"
)
EXPECTED_MANIFEST_SIDECAR_SHA = (
    "5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402"
)
EXPECTED_RAW_SEGMENT_MANIFEST_SHA = (
    "1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1"
)
EXPECTED_RAW_GATE_REPORT_SHA = (
    "051bed7b3a146278e389bd8e265243d30fd541b5f36061d0573f3522920f9c24"
)
EXPECTED_RAW_ACQUISITION_LOG_SHA = (
    "0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93"
)

DEFAULT_MANIFEST_REL = (
    "data/microstructure/manifests/"
    "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json"
)
DEFAULT_GATE_REPORTS_ROOT_REL = "data/microstructure/gate-reports/normalized"

# Forbidden normalized column-name substrings (locked Phase 4bd guard, extended).
FORBIDDEN_COLUMN_SUBSTRINGS: tuple[str, ...] = (
    "label", "target", "future", "signal", "entry", "exit", "pnl", "profit",
    "loss", "mfe", "mae", "r_multiple", "equity", "position", "alpha", "edge",
    "prediction", "model", "score", "decision", "strategy", "liquidation",
    "funding", "open_interest", "order_book", "mark_price", "spot",
    "cross_venue", "tick", "ethusdt", "v003",
)

# Forbidden segment-manifest field-name substrings (Phase 4bn-N §13).
FORBIDDEN_MANIFEST_KEY_SUBSTRINGS: tuple[str, ...] = (
    "model", "prediction", "_score", "label_", "target_", "future_", "_future",
    "signal", "entry", "exit", "pnl", "equity", "profit", "loss", "position",
    "backtest", "strategy", "alpha", "edge", "mfe", "mae", "r_multiple",
    "barrier", "mark_price", "funding", "open_interest", "order_book",
    "cross_venue", "ethusdt", "v003", "chronological_split_policy",
    "diagnostics_authorized", "ml_authorized", "research_ready", "admissible",
    "approved_for_backtest",
)

# Manifest required fields (Phase 4bn-N §12).
REQUIRED_MANIFEST_FIELDS: tuple[str, ...] = (
    "dataset_family", "dataset_version", "version", "schema_version",
    "segment_label", "data_family", "symbol_list", "market", "dataset_category",
    "phase", "phase_id", "source_phase_boundary", "created_at_unix_ms",
    "created_at_utc", "code_commit_sha", "base_commit_sha", "capture_config_hash",
    "date_start", "date_end", "date_count", "date_list", "expected_file_count",
    "produced_file_count", "total_event_count", "total_row_count",
    "per_file_inventory", "total_normalized_footprint_bytes",
    "source_dataset_family", "source_dataset_version",
    "source_raw_segment_manifest_path", "source_raw_segment_manifest_sha256",
    "source_raw_gate_report_path", "source_raw_gate_report_id",
    "source_raw_gate_report_sha256", "source_raw_acquisition_log_path",
    "source_raw_acquisition_log_sha256", "existing_v002_normalized_reference",
    "full_intended_envelope_start", "full_intended_envelope_end",
    "research_eligible", "eligibility_gate_status", "governance_labels",
    "no_successor_authorization", "v002_terminal_window_mode",
    "existing_v002_terminal_window", "sealed_test_split_touched",
    "existing_v002_sealed_test_split", "test_holdout_touched", "test_rows_loaded",
    "partitioning_rule", "primary_key", "storage_format", "sidecar_policy",
    "invalid_windows", "budget_witnesses",
)

GATE_PASS = "NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
GATE_FAIL = "NORMALIZED_LAYER_GATE_FAILED__REMAIN_PAUSED"
GATE_NOT_RUN_MISSING = "NORMALIZED_LAYER_GATE_NOT_RUN__MISSING_LOCAL_ARTEFACTS__REMAIN_PAUSED"


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class CheckResult:
    check_id: str
    title: str
    status: str  # "pass" | "fail"
    detail: str = ""


def _add(checks: list[CheckResult], cid: str, title: str, ok: bool, detail: str = "") -> None:
    """Append a pass/fail CheckResult."""
    checks.append(CheckResult(cid, title, "pass" if ok else "fail", detail))


@dataclass
class GateResult:
    result_state: str
    overall_status: str  # "pass" | "fail" | "not_run"
    checks: list[CheckResult] = field(default_factory=list)
    report_path: Path | None = None
    report_sha256: str | None = None
    report_sidecar_path: Path | None = None
    report_sidecar_sha256: str | None = None
    recomputed_total_rows: int = 0
    recomputed_total_footprint_bytes: int = 0
    parquet_count: int = 0
    sidecar_count: int = 0
    sample_dates: list[str] = field(default_factory=list)
    wall_clock_seconds: float = 0.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _utc_date_to_day_start_ms(utc_date: str) -> int:
    day = datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(day.timestamp() * 1000)


def _date_in_segment(date: str) -> bool:
    return EXPECTED_DATE_START <= date <= EXPECTED_DATE_END and date < V002_TERMINAL_START


def _validate_canonical_sidecar(
    sidecar_path: Path, expected_basename: str
) -> tuple[bool, str, str]:
    """Validate canonical ``<sha>  <basename>\\n`` sidecar. Return (ok, sha, detail)."""
    raw = sidecar_path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return False, "", "sidecar has BOM"
    if b"\r" in raw:
        return False, "", "sidecar has CR (not LF-only)"
    if not raw.endswith(b"\n"):
        return False, "", "sidecar missing trailing LF"
    text = raw.decode("ascii")
    if text.count("\n") != 1:
        return False, "", "sidecar has extra lines"
    line = text[:-1]
    if "  " not in line:
        return False, "", "sidecar missing two-space separator"
    sha, sep, basename = line.partition("  ")
    if sep != "  " or "  " in basename or " " in basename:
        return False, "", "sidecar separator/format invalid"
    if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
        return False, "", "sidecar sha not 64-char lowercase hex"
    if basename != expected_basename:
        return False, "", f"sidecar basename {basename!r} != {expected_basename!r}"
    return True, sha, "ok"


def _resolve_local_path(repo_root: Path, rel: str) -> Path:
    """Resolve a manifest 'microstructure/...' relative path to an absolute path."""
    micro_root = repo_root / "data" / "microstructure"
    r = rel
    if r.startswith("microstructure/"):
        r = r[len("microstructure/"):]
    return micro_root / r


# ---------------------------------------------------------------------------
# Gate core
# ---------------------------------------------------------------------------


def _check_manifest_contract(manifest: Mapping[str, Any], checks: list[CheckResult]) -> bool:
    """Validate required-field + forbidden-field + posture contract."""
    ok = True
    missing = [k for k in REQUIRED_MANIFEST_FIELDS if k not in manifest]
    _add(checks, "manifest.required_fields", "required fields present",
         not missing, f"missing: {missing}" if missing else "")
    ok = ok and not missing

    identity_ok = (
        manifest.get("dataset_family") == NORMALIZED_DATASET_FAMILY
        and manifest.get("dataset_version") == NORMALIZED_DATASET_VERSION
        and manifest.get("version") == NORMALIZED_DATASET_VERSION
        and manifest.get("schema_version") == SCHEMA_VERSION
        and manifest.get("segment_label") == SEGMENT_LABEL
        and manifest.get("data_family") == DATA_FAMILY
        and manifest.get("symbol_list") == [SYMBOL]
        and manifest.get("market") == MARKET
        and manifest.get("dataset_category") == DATASET_CATEGORY
    )
    _add(checks, "manifest.identity", "identity/scope fields match", identity_ok,
         "" if identity_ok else "identity mismatch")
    ok = ok and identity_ok

    base_ok = manifest.get("base_commit_sha") == "f55b47ff94637e72ebacc40f1a133a5526afaef6"
    _add(checks, "manifest.base_commit", "base_commit_sha = 4bn-O base", base_ok,
         str(manifest.get("base_commit_sha")))
    ok = ok and base_ok

    window_ok = (
        manifest.get("date_start") == EXPECTED_DATE_START
        and manifest.get("date_end") == EXPECTED_DATE_END
        and manifest.get("date_count") == EXPECTED_DATE_COUNT
        and manifest.get("expected_file_count") == EXPECTED_DATE_COUNT
        and manifest.get("produced_file_count") == EXPECTED_DATE_COUNT
        and manifest.get("total_event_count") == EXPECTED_TOTAL_EVENT_COUNT
        and manifest.get("total_row_count") == EXPECTED_TOTAL_EVENT_COUNT
        and manifest.get("total_normalized_footprint_bytes") == EXPECTED_TOTAL_FOOTPRINT_BYTES
        and manifest.get("full_intended_envelope_start") == FULL_ENVELOPE_START
        and manifest.get("full_intended_envelope_end") == FULL_ENVELOPE_END
    )
    _add(checks, "manifest.window", "window/inventory totals match", window_ok,
         "" if window_ok else "window mismatch")
    ok = ok and window_ok

    lineage_ok = (
        manifest.get("source_dataset_family") == SOURCE_DATASET_FAMILY
        and manifest.get("source_dataset_version") == SOURCE_DATASET_VERSION
        and manifest.get("source_raw_segment_manifest_sha256") == EXPECTED_RAW_SEGMENT_MANIFEST_SHA
        and manifest.get("source_raw_gate_report_sha256") == EXPECTED_RAW_GATE_REPORT_SHA
        and manifest.get("source_raw_acquisition_log_sha256") == EXPECTED_RAW_ACQUISITION_LOG_SHA
    )
    _add(checks, "manifest.lineage", "predecessor lineage SHAs recorded", lineage_ok,
         "" if lineage_ok else "lineage mismatch")
    ok = ok and lineage_ok

    posture_ok = (
        manifest.get("research_eligible") is False
        and manifest.get("eligibility_gate_status") == "pending"
        and manifest.get("no_successor_authorization") is True
        and manifest.get("v002_terminal_window_mode") == "by_reference"
        and manifest.get("sealed_test_split_touched") is False
        and manifest.get("test_holdout_touched") is False
        and manifest.get("test_rows_loaded") == 0
    )
    gov = manifest.get("governance_labels") or {}
    posture_ok = posture_ok and gov.get("feature_computation") == "forbidden" \
        and gov.get("strategy_use") == "forbidden"
    ref = manifest.get("existing_v002_normalized_reference") or {}
    posture_ok = posture_ok and ref.get("read") is False and ref.get("mutated") is False
    term = manifest.get("existing_v002_terminal_window") or {}
    posture_ok = posture_ok and all(
        term.get(k) is False for k in ("read", "overwritten", "redownloaded", "re_normalized")
    )
    sealed = manifest.get("existing_v002_sealed_test_split") or {}
    posture_ok = posture_ok and sealed.get("touched") is False
    _add(checks, "manifest.posture", "non-eligible/by-reference/sealed posture", posture_ok,
         "" if posture_ok else "posture mismatch")
    ok = ok and posture_ok

    # Forbidden field-name scan (skip governance_labels subtree).
    forbidden_hits: list[str] = []

    def _scan(obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                low = str(k).lower()
                for needle in FORBIDDEN_MANIFEST_KEY_SUBSTRINGS:
                    if needle in low:
                        forbidden_hits.append(f"{needle} in {k}")
                if k == "governance_labels":
                    continue
                _scan(v)
        elif isinstance(obj, list):
            for item in obj:
                _scan(item)

    _scan(manifest)
    _add(checks, "manifest.forbidden_fields", "no forbidden field names", not forbidden_hits,
         "" if not forbidden_hits else f"hits: {forbidden_hits}")
    ok = ok and not forbidden_hits
    return ok


def _sample_dates(date_list: Sequence[str]) -> list[str]:
    """Representative deep-check sample: month-firsts + final date."""
    sample = {date_list[0], date_list[-1]}
    sample.update(d for d in date_list if d.endswith("-01"))
    return sorted(sample)


def run_gate(
    *,
    manifest_path: Path,
    gate_reports_root: Path,
    repo_root: Path,
    write_report: bool = True,
    refuse_overwrite: bool = True,
) -> GateResult:
    """Run the Phase 4bn-P normalized-layer eligibility gate once (read-only)."""
    import pyarrow.parquet as pq

    start = time.monotonic()
    checks: list[CheckResult] = []

    if not manifest_path.exists():
        return GateResult(result_state=GATE_NOT_RUN_MISSING, overall_status="not_run",
                          checks=[CheckResult("manifest.exists", "segment manifest exists",
                                              "fail", str(manifest_path))],
                          wall_clock_seconds=time.monotonic() - start)

    # Manifest hash + sidecar.
    man_sha, _ = compute_file_sha256(manifest_path)
    man_sha_ok = man_sha == EXPECTED_MANIFEST_SHA
    checks.append(CheckResult("manifest.sha", "segment manifest SHA256 matches",
                              "pass" if man_sha_ok else "fail", man_sha))
    sidecar_path = manifest_path.with_suffix(manifest_path.suffix + ".sha256")
    if not sidecar_path.exists():
        checks.append(CheckResult("manifest.sidecar", "manifest sidecar exists", "fail",
                                  str(sidecar_path)))
    else:
        sc_ok, sc_sha, sc_detail = _validate_canonical_sidecar(sidecar_path, manifest_path.name)
        sc_match = sc_ok and sc_sha == man_sha
        checks.append(CheckResult("manifest.sidecar", "manifest sidecar canonical + matches",
                                  "pass" if sc_match else "fail",
                                  sc_detail if not sc_ok else (
                                      "ok" if sc_match else "sidecar sha != manifest sha")))

    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    _check_manifest_contract(manifest, checks)

    inventory: list[dict[str, Any]] = list(manifest.get("per_file_inventory", []))
    date_list: list[str] = list(manifest.get("date_list", []))

    # Date coverage.
    coverage_ok = (
        len(inventory) == EXPECTED_DATE_COUNT
        and len(date_list) == EXPECTED_DATE_COUNT
        and len(set(date_list)) == EXPECTED_DATE_COUNT
        and [e["date"] for e in inventory] == date_list
        and date_list[0] == EXPECTED_DATE_START
        and date_list[-1] == EXPECTED_DATE_END
        and all(_date_in_segment(d) for d in date_list)
        and all(d < V002_TERMINAL_START for d in date_list)
        and not any(SEALED_TEST_START <= d <= SEALED_TEST_END for d in date_list)
    )
    # contiguous daily coverage
    if coverage_ok:
        expected = []
        cur = datetime.strptime(EXPECTED_DATE_START, "%Y-%m-%d").replace(tzinfo=UTC)
        end = datetime.strptime(EXPECTED_DATE_END, "%Y-%m-%d").replace(tzinfo=UTC)
        while cur <= end:
            expected.append(cur.strftime("%Y-%m-%d"))
            cur = datetime.fromtimestamp(cur.timestamp() + 86400, UTC)
        coverage_ok = date_list == expected
    checks.append(CheckResult("coverage", "exactly 275 contiguous in-segment dates",
                              "pass" if coverage_ok else "fail",
                              f"{len(date_list)} dates"))

    samples = _sample_dates(date_list) if date_list else []
    sample_set = set(samples)

    # Per-file walk.
    total_rows = 0
    total_bytes = 0
    parquet_count = 0
    sidecar_count = 0
    per_file_fail = 0
    schema_fail = 0
    path_fail = 0
    hash_fail = 0
    rowcount_fail = 0
    sample_fail = 0
    forbidden_col_fail = 0
    prev_last_ms = -1
    adjacency_fail = 0

    for entry in inventory:
        date = str(entry["date"])
        yyyy, mm, _dd = date.split("-")
        pq_path = _resolve_local_path(repo_root, str(entry["local_parquet_path"]))
        sc_path = _resolve_local_path(repo_root, str(entry["local_sidecar_path"]))

        # Path layout.
        expect_parts = (FAMILY_DIR_NAME, SYMBOL, yyyy, mm)
        layout_ok = (
            all(p in pq_path.parts for p in expect_parts)
            and pq_path.name == f"{SYMBOL}-aggTrades-{date}.parquet"
            and PUBLISHED_V002_FAMILY_DIR_NAME not in pq_path.parts
            and "v003" not in str(pq_path)
            and _date_in_segment(date)
        )
        if not layout_ok:
            path_fail += 1

        if not pq_path.exists():
            per_file_fail += 1
            continue
        parquet_count += 1
        actual_sha, actual_size = compute_file_sha256(pq_path)
        total_bytes += actual_size
        if actual_sha != str(entry["parquet_sha256"]):
            hash_fail += 1
        if actual_size != int(entry["parquet_size_bytes"]):
            hash_fail += 1

        # Sidecar. The manifest's total_normalized_footprint_bytes (written by
        # Phase 4bn-O) is the sum of parquet + sidecar bytes per date, so the
        # gate accumulates both for an exact footprint recomputation.
        if not sc_path.exists():
            per_file_fail += 1
        else:
            sidecar_count += 1
            total_bytes += sc_path.stat().st_size
            sc_ok, sc_sha, _d = _validate_canonical_sidecar(sc_path, pq_path.name)
            if not sc_ok or sc_sha != actual_sha or sc_sha != str(entry["parquet_sha256"]):
                hash_fail += 1

        # Metadata-only schema + row count. Fail closed (no crash) on a
        # corrupt / unreadable Parquet.
        try:
            pqf = pq.ParquetFile(str(pq_path))
            names = tuple(pqf.schema_arrow.names)
            if names != NORMALIZED_SCHEMA_V001:
                schema_fail += 1
            for col in names:
                low = col.lower()
                if any(n in low for n in FORBIDDEN_COLUMN_SUBSTRINGS):
                    forbidden_col_fail += 1
            nrows = pqf.metadata.num_rows
            total_rows += nrows
            expected_n = int(entry.get("row_count", entry.get("event_count", -1)))
            if nrows != expected_n:
                rowcount_fail += 1
            if date in sample_set and not _deep_check_date(pq, pq_path, date, entry):
                sample_fail += 1
        except Exception:  # noqa: BLE001 - any read error is a gate failure
            schema_fail += 1
            rowcount_fail += 1

        # Adjacency from manifest inventory.
        first_ms = int(entry["first_transact_time_ms"])
        last_ms = int(entry["last_transact_time_ms"])
        if prev_last_ms >= 0 and prev_last_ms >= first_ms:
            adjacency_fail += 1
        prev_last_ms = last_ms

    _add(checks, "files.present", "all 275 parquet+sidecar present",
         per_file_fail == 0, f"missing groups: {per_file_fail}")
    _add(checks, "files.hash_integrity", "parquet SHA == sidecar == manifest inventory",
         hash_fail == 0, f"hash failures: {hash_fail}")
    _add(checks, "files.path_layout", "segment path layout + basename correct",
         path_fail == 0, f"path failures: {path_fail}")
    _add(checks, "files.schema", "every parquet schema == NORMALIZED_SCHEMA_V001",
         schema_fail == 0, f"schema failures: {schema_fail}")
    _add(checks, "files.forbidden_columns", "no forbidden columns",
         forbidden_col_fail == 0, f"forbidden-col hits: {forbidden_col_fail}")
    _add(checks, "files.row_counts", "per-file row count == manifest inventory",
         rowcount_fail == 0, f"rowcount failures: {rowcount_fail}")
    _add(checks, "files.adjacency", "adjacent-date non-overlap (274 pairs)",
         adjacency_fail == 0, f"overlaps: {adjacency_fail}")
    _add(checks, "files.sample_deep",
         f"deep row-level checks on {len(samples)} sampled dates",
         sample_fail == 0, f"sample failures: {sample_fail}")

    rows_ok = total_rows == EXPECTED_TOTAL_EVENT_COUNT
    _add(checks, "aggregate.rows", "recomputed total rows == 400,001,695", rows_ok, str(total_rows))
    bytes_ok = total_bytes == EXPECTED_TOTAL_FOOTPRINT_BYTES
    _add(checks, "aggregate.footprint", "recomputed footprint == 3,954,532,918 B",
         bytes_ok, str(total_bytes))
    count_ok = parquet_count == EXPECTED_DATE_COUNT and sidecar_count == EXPECTED_DATE_COUNT
    _add(checks, "aggregate.counts", "275 parquets + 275 sidecars", count_ok,
         f"{parquet_count}/{sidecar_count}")

    # Predecessor integrity (read-only; only the predecessor governance files).
    _check_predecessors(manifest, repo_root, checks)

    # Published __v002 immutability / by-reference (no open of published files).
    pub_ok = (
        FAMILY_DIR_NAME != PUBLISHED_V002_FAMILY_DIR_NAME
        and SEGMENT_MANIFEST_BASENAME
        != "microstructure_normalized_aggtrades_v001__v002.json"
        and (manifest.get("existing_v002_normalized_reference") or {}).get("read") is False
        and (manifest.get("existing_v002_normalized_reference") or {}).get("mutated") is False
    )
    _add(checks, "published_v002.by_reference",
         "published __v002 path-disjoint, by-reference, not mutated", pub_ok, "")

    overall = "pass" if all(c.status == "pass" for c in checks) else "fail"
    result_state = GATE_PASS if overall == "pass" else GATE_FAIL

    res = GateResult(
        result_state=result_state, overall_status=overall, checks=checks,
        recomputed_total_rows=total_rows, recomputed_total_footprint_bytes=total_bytes,
        parquet_count=parquet_count, sidecar_count=sidecar_count, sample_dates=samples,
        wall_clock_seconds=time.monotonic() - start,
    )

    if write_report:
        _write_gate_report(
            res=res, manifest=manifest, manifest_path=manifest_path, manifest_sha=man_sha,
            gate_reports_root=gate_reports_root, repo_root=repo_root,
            refuse_overwrite=refuse_overwrite,
        )
    res.wall_clock_seconds = time.monotonic() - start
    return res


def _deep_check_date(pq: Any, pq_path: Path, date: str, entry: Mapping[str, Any]) -> bool:
    """Full-table row-level validation for a single sampled date."""
    table = pq.read_table(pq_path)
    if tuple(table.schema.names) != NORMALIZED_SCHEMA_V001:
        return False
    cols = {n: table.column(n) for n in table.schema.names}
    n = table.num_rows
    if n != int(entry.get("row_count", entry.get("event_count", -1))):
        return False
    if any(cols["dataset_version"][i].as_py() != "v002" for i in (0, n - 1)):
        return False
    if any(cols["source_dataset_version"][i].as_py() != "v002" for i in (0, n - 1)):
        return False
    if any(cols["normalization_schema_version"][i].as_py() != NORMALIZATION_SCHEMA_VERSION
           for i in (0, n - 1)):
        return False
    if any(cols["symbol"][i].as_py() != SYMBOL for i in (0, n - 1)):
        return False
    if any(cols["utc_date"][i].as_py() != date for i in (0, n - 1)):
        return False
    day_start = _utc_date_to_day_start_ms(date)
    day_end = day_start + UTC_DAY_MS
    t = cols["transact_time_ms"].to_pylist()
    a = cols["agg_trade_id"].to_pylist()
    if t[0] != int(entry["first_transact_time_ms"]) or t[-1] != int(entry["last_transact_time_ms"]):
        return False
    if min(a) != int(entry["min_agg_trade_id"]) or max(a) != int(entry["max_agg_trade_id"]):
        return False
    if not all(day_start <= x < day_end for x in t):
        return False
    if any(t[i] > t[i + 1] for i in range(n - 1)):
        return False
    # Strictly increasing agg_trade_id => unique + monotone.
    return not any(a[i] >= a[i + 1] for i in range(n - 1))


def _check_predecessors(
    manifest: Mapping[str, Any], repo_root: Path, checks: list[CheckResult]
) -> None:
    """Verify predecessor governance-file SHAs (read-only)."""
    def _abs(rel: str) -> Path:
        p = Path(rel)
        return p if p.is_absolute() else repo_root / rel

    raw_man = _abs(str(manifest.get("source_raw_segment_manifest_path", "")))
    raw_man_ok = (
        raw_man.exists()
        and compute_file_sha256(raw_man)[0] == EXPECTED_RAW_SEGMENT_MANIFEST_SHA
    )
    _add(checks, "predecessor.raw_manifest", "raw segment manifest SHA matches",
         raw_man_ok, str(raw_man))

    gate = _abs(str(manifest.get("source_raw_gate_report_path", "")))
    gate_ok = gate.exists() and compute_file_sha256(gate)[0] == EXPECTED_RAW_GATE_REPORT_SHA
    if gate_ok:
        gp = json.loads(gate.read_bytes().decode("utf-8"))
        gate_ok = gp.get("overall_status") == "pass" and "PASS" in str(gp.get("gate_verdict", ""))
    _add(checks, "predecessor.raw_gate", "raw gate report SHA matches + PASS", gate_ok, str(gate))

    acq = _abs(str(manifest.get("source_raw_acquisition_log_path", "")))
    acq_ok = acq.exists() and compute_file_sha256(acq)[0] == EXPECTED_RAW_ACQUISITION_LOG_SHA
    _add(checks, "predecessor.acq_log", "raw acquisition log SHA matches", acq_ok, str(acq))


def _atomic_write_json(
    path: Path, obj: Mapping[str, Any], *, refuse_overwrite: bool
) -> tuple[str, int]:
    if not isinstance(path, Path):
        raise NormalizationIOError("path must be a pathlib.Path")
    assert_path_under_microstructure(path, label="gate report path")
    if refuse_overwrite and path.exists():
        raise NormalizationIOError(f"refusing to overwrite existing file: {path}")
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


def _write_gate_report(
    *, res: GateResult, manifest: Mapping[str, Any], manifest_path: Path, manifest_sha: str,
    gate_reports_root: Path, repo_root: Path, refuse_overwrite: bool,
) -> None:
    run_id = int(time.time() * 1000)
    report_basename = (
        f"{FAMILY_DIR_NAME}__phase-4bn-p__{run_id}__{BASE_MAIN_SHORT}.json"
    )
    report_path = gate_reports_root / report_basename
    report = {
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "phase": PHASE_ID,
        "phase_id": PHASE_ID,
        "artefact_type": "normalized_layer_eligibility_gate_report",
        "base_commit_sha": BASE_MAIN_SHA,
        "created_at_unix_ms": run_id,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "gate_result_state": res.result_state,
        "overall_status": res.overall_status,
        "gate_verdict": "NORMALIZED_LAYER_GATE_PASS" if res.overall_status == "pass"
        else "NORMALIZED_LAYER_GATE_FAIL",
        "input_normalized_manifest_path": str(
            manifest_path.resolve().relative_to(repo_root.resolve())).replace(os.sep, "/"),
        "input_normalized_manifest_sha256": manifest_sha,
        "input_normalized_segment_directory": (
            f"data/microstructure/normalized/{FAMILY_DIR_NAME}/"),
        "dataset_family": NORMALIZED_DATASET_FAMILY,
        "dataset_version": NORMALIZED_DATASET_VERSION,
        "segment_label": SEGMENT_LABEL,
        "symbol_list": [SYMBOL],
        "market": MARKET,
        "data_family": DATA_FAMILY,
        "date_start": EXPECTED_DATE_START,
        "date_end": EXPECTED_DATE_END,
        "date_count": EXPECTED_DATE_COUNT,
        "recomputed_parquet_count": res.parquet_count,
        "recomputed_sidecar_count": res.sidecar_count,
        "recomputed_total_row_count": res.recomputed_total_rows,
        "recomputed_total_footprint_bytes": res.recomputed_total_footprint_bytes,
        "sample_dates_deep_checked": res.sample_dates,
        "checks": [{"check_id": c.check_id, "title": c.title, "status": c.status,
                    "detail": c.detail} for c in res.checks],
        "segment_non_eligible": True,
        "research_eligible_after": False,
        "eligibility_gate_status_after": "pending",
        "no_successor_authorization": True,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "published_v002_mutated": False,
        "data_committed": False,
        "predecessor_raw_segment_manifest_sha256": EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
        "predecessor_raw_gate_report_sha256": EXPECTED_RAW_GATE_REPORT_SHA,
        "predecessor_raw_acquisition_log_sha256": EXPECTED_RAW_ACQUISITION_LOG_SHA,
    }
    # Writer invariants (unconditional).
    if (
        report["research_eligible_after"] is not False
        or report["no_successor_authorization"] is not True
    ):
        raise NormalizationIOError("gate report invariant violation")
    report_sha, _ = _atomic_write_json(report_path, report, refuse_overwrite=refuse_overwrite)
    sidecar_path = report_path.with_suffix(report_path.suffix + ".sha256")
    sidecar_sha, _ = write_sha256_sidecar(
        sidecar_path, target_filename=report_path.name, sha256_hex=report_sha,
        refuse_overwrite=refuse_overwrite,
    )
    res.report_path = report_path
    res.report_sha256 = report_sha
    res.report_sidecar_path = sidecar_path
    res.report_sidecar_sha256 = sidecar_sha


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Phase 4bn-P — Normalized-Layer Eligibility Gate over the Phase 4bn-O "
            "pre-v002 normalized segment. Read-only on data; writes at most one "
            "gitignored gate report + sidecar."
        )
    )
    p.add_argument("--manifest", type=Path, default=None)
    p.add_argument("--gate-reports-root", type=Path, default=None)
    p.add_argument("--dry-run", action="store_true", help="Validate manifest presence only.")
    p.add_argument("--no-write-report", action="store_true")
    p.add_argument("--allow-overwrite", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = _REPO_ROOT
    manifest_path = args.manifest or repo_root / DEFAULT_MANIFEST_REL
    gate_reports_root = args.gate_reports_root or repo_root / DEFAULT_GATE_REPORTS_ROOT_REL

    if args.dry_run:
        if not manifest_path.exists():
            print(f"[dry-run] MISSING manifest: {manifest_path}")
            return 1
        print(f"[dry-run] manifest present: {manifest_path}")
        return 0

    res = run_gate(
        manifest_path=manifest_path, gate_reports_root=gate_reports_root, repo_root=repo_root,
        write_report=not args.no_write_report, refuse_overwrite=not args.allow_overwrite,
    )
    print(f"[Phase 4bn-P] {res.result_state}")
    print(f"  overall={res.overall_status}; parquets={res.parquet_count}; "
          f"sidecars={res.sidecar_count}; rows={res.recomputed_total_rows}; "
          f"footprint={res.recomputed_total_footprint_bytes} B; "
          f"runtime={res.wall_clock_seconds:.1f}s")
    for c in res.checks:
        if c.status != "pass":
            print(f"  FAIL {c.check_id}: {c.title} -- {c.detail}")
    if res.report_path is not None:
        print(f"  report: {res.report_path} (sha256={res.report_sha256})")
    return 0 if res.overall_status == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
