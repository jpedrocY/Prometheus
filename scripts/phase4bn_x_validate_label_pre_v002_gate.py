"""Phase 4bn-X — Label-Layer Eligibility Gate for the Pre-V002 BTCUSDT
aggTrades Label Segment.

Bounded, read-only gate over the Phase 4bn-W local label pre-v002 segment
(BTCUSDT / Binance USDⓈ-M futures / aggTrades; 2024-03-01 .. 2024-11-30
inclusive UTC; 275 dates; 400,001,695 label rows). It validates that the
local label segment is structurally complete, internally consistent,
manifest-consistent, predecessor-consistent, schema-consistent, path-consistent,
sidecar-consistent, governance-consistent, hash-consistent, lineage-consistent,
and envelope-/censoring-consistent, and writes at most one local gitignored
label-layer gate report + canonical sidecar under
``data/microstructure/gate-reports/labels/``.

The gate is **read-only** with respect to every data artefact:

- it never mutates the segment manifest, any label Parquet, any sidecar, the
  published ``__v002`` label family, or any predecessor artefact;
- it never flips ``research_eligible`` and never transitions
  ``eligibility_gate_status`` (a passing gate authorizes nothing);
- it performs NO network I/O, NO acquisition, NO label derivation rerun, NO
  feature execution rerun, NO normalization rerun, NO raw/normalized/feature
  layer-gate rerun, NO ML / diagnostics / strategy / signals / PnL / backtests,
  NO database / Parquet compaction / storage migration / v003;
- it never reads the v002 terminal raw/normalized/feature/label window, the
  sealed-test split, or any published ``__v002`` Parquet / manifest content
  (the published ``__v002`` label family is treated by reference only).

Unlike the feature-layer (Phase 4bn-T) and normalized-layer (Phase 4bn-P)
gates — which bound their row-level deep checks to a sampled set of dates —
this label-layer gate performs a **full scan of all 275 label Parquets**.
For every file it streams the Parquet SHA256 (full hash integrity), records
the on-disk size, reads ``ParquetFile.metadata`` for the row count / column
names, and materialises the identity / censoring / direction / flag columns to
validate per-row envelope-terminal censoring, per-horizon censored counts,
reference-timestamp bounds, the any-censored OR invariant, and the invalid-
price count. Constant lineage / identity / ``label_config_hash`` columns are
verified exhaustively (every value equal to the locked constant, zero nulls)
across every file. No check is silently downgraded to sampling — this is the
eligibility gate for the full label layer.
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
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure.labels_schema_v002 import (  # noqa: E402
    ANCHOR_POLICY_V002,
    DIRECTION_THRESHOLD_POLICY_V002,
    DTYPE_POLICY_V002,
    FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002,
    FUTURE_REFERENCE_POLICY_V002,
    LABEL_DATASET_FAMILY_V002,
    LABEL_DATASET_VERSION_V002,
    LABEL_HORIZON_MS_V002,
    LABEL_HORIZONS_V002,
    LABEL_LINEAGE_COLUMNS_V002,
    LABEL_NAMES_V002,
    LABEL_SCHEMA_V002,
    LABEL_SCHEMA_VERSION_V002,
    LABEL_SUPPORT_COLUMN_NAMES_V002,
    NULL_CENSORING_POLICY_V002,
)
from prometheus.research.microstructure.normalize_io import (  # noqa: E402
    NormalizationIOError,
    assert_path_under_microstructure,
    compute_bytes_sha256,
    compute_file_sha256,
    write_sha256_sidecar,
)

# ---------------------------------------------------------------------------
# Locked identity / expectation constants (Phase 4bn-X prompt + Phase 4bn-W
# label segment manifest).
# ---------------------------------------------------------------------------

PHASE_ID = "phase-4bn-x"
PHASE_ID_TOKEN = "4bn_x"
REPORT_SCHEMA_VERSION = "v001"

# Base = Phase 4bn-W final main SHA (operator-pinned for this branch).
BASE_MAIN_SHA = "5bcae53ee843759a6c81c14d71a66dc241023e31"
BASE_MAIN_SHORT = "5bcae53ee843"

LABEL_DATASET_FAMILY = "microstructure_labels_aggtrades_v001"
LABEL_DATASET_VERSION = "v002"
LABEL_SCHEMA_VERSION = "v001"
SEGMENT_LABEL = "pre_v002_segment"
DATA_FAMILY = "aggTrades"
MARKET = "usdm_futures"
DATASET_CATEGORY = "labels"
SYMBOL = "BTCUSDT"
SEGMENT_PRODUCER_PHASE_ID = "phase-4bn-w"

# The segment under gate was produced by Phase 4bn-W; its family-dir token is fixed.
FAMILY_DIR_NAME = "microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w"
SEGMENT_MANIFEST_BASENAME = f"{FAMILY_DIR_NAME}.json"
PUBLISHED_V002_LABEL_DIR_NAME = f"{LABEL_DATASET_FAMILY}__{LABEL_DATASET_VERSION}"
PUBLISHED_V002_LABEL_MANIFEST_BASENAME = (
    f"{LABEL_DATASET_FAMILY}__{LABEL_DATASET_VERSION}.json"
)
PUBLISHED_V002_LABEL_MANIFEST_REL = (
    f"data/microstructure/manifests/{PUBLISHED_V002_LABEL_MANIFEST_BASENAME}"
)

EXPECTED_DATE_COUNT = 275
EXPECTED_DATE_START = "2024-03-01"
EXPECTED_DATE_END = "2024-11-30"
EXPECTED_TOTAL_ROW_COUNT = 400_001_695
EXPECTED_TOTAL_FOOTPRINT_BYTES = 15_654_082_679
EXPECTED_COLUMN_COUNT = 40
EXPECTED_LABEL_COLUMN_COUNT = 8
EXPECTED_SUPPORT_COLUMN_COUNT = 14
EXPECTED_LINEAGE_COLUMN_COUNT = 17
FULL_ENVELOPE_START = "2024-03-01"
FULL_ENVELOPE_END = "2025-02-28"

V002_TERMINAL_START = "2024-12-01"
V002_TERMINAL_END = "2025-02-28"
SEALED_TEST_START = "2025-02-14"
SEALED_TEST_END = "2025-02-28"

EXPECTED_ENVELOPE_TERMINAL_UNIX_MS = 1_733_011_199_331
EXPECTED_ENVELOPE_TERMINAL_UTC_DATE = "2024-11-30"

EXPECTED_INVALID_PRICE_ROW_COUNT = 0
EXPECTED_CENSORED_PER_HORIZON: dict[str, int] = {
    "1s": 3,
    "5s": 20,
    "15s": 42,
    "60s": 216,
}

EXPECTED_MANIFEST_SHA = (
    "69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161"
)
EXPECTED_MANIFEST_SIDECAR_SHA = (
    "636a4c1a0159364e7d67f502dda48664f18fc16545c993935e6429ccdf868239"
)

EXPECTED_LABEL_CONFIG_HASH = (
    "b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970"
)
EXPECTED_FEATURE_CONFIG_HASH = (
    "0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c"
)
# Explicitly INVALID for this pre-v002 segment (published v002 feature lock).
PUBLISHED_V002_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)

# Predecessor evidence (Phase 4bn-S feature segment + Phase 4bn-T feature-layer
# gate; Phase 4bn-O normalized segment + Phase 4bn-P normalized-layer gate; raw).
EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA = (
    "4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52"
)
EXPECTED_FEATURE_SEGMENT_MANIFEST_SIDECAR_SHA = (
    "f2ca2f48a5ac8ccfb892d0460cdfbbbb891451b9d94135adb3bff0936c8592e5"
)
EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA = (
    "db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08"
)
REQUIRED_FEATURE_GATE_VERDICT = (
    "FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
)
EXPECTED_FEATURE_GATE_CHECK_COUNT = 27
EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA = (
    "0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa"
)
EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA = (
    "5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402"
)
EXPECTED_NORMALIZED_GATE_REPORT_SHA = (
    "3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134"
)
REQUIRED_NORMALIZED_GATE_VERDICT = (
    "NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
)
EXPECTED_NORMALIZED_GATE_CHECK_COUNT = 25
EXPECTED_RAW_SEGMENT_MANIFEST_SHA = (
    "1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1"
)

# Per-row lineage re-mapping (Phase 4bn-V §17 / Phase 4bn-W): the two
# terminal-specific lineage columns carry the Phase 4bn admissibility witnesses.
#   source_phase_4bm_j_gate_report_sha256  -> Phase 4bn-T feature-layer gate SHA
#   source_feature_successor_state_sha256  -> Phase 4bn-P normalized-layer gate SHA
LINEAGE_REMAP_FEATURE_LAYER_GATE_COLUMN = "source_phase_4bm_j_gate_report_sha256"
LINEAGE_REMAP_NORMALIZED_LAYER_GATE_COLUMN = "source_feature_successor_state_sha256"

DEFAULT_MANIFEST_REL = (
    "data/microstructure/manifests/"
    "microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w.json"
)
DEFAULT_GATE_REPORTS_ROOT_REL = "data/microstructure/gate-reports/labels"

# Forbidden label column-name substrings (locked Phase 4bm-N §27 guard).
FORBIDDEN_COLUMN_SUBSTRINGS: tuple[str, ...] = FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002

# Forbidden label-manifest field-name substrings. NOTE: ``label``, ``forward``,
# ``future``, ``ml``, ``strategy``, ``backtest``, ``diagnostics`` are NOT in this
# set because they legitimately appear in label identity / schema / policy /
# governance-declaration keys (e.g. ``label_config_hash``,
# ``future_reference_policy``, ``strategy_use``). The explicitly validated
# declaration subtrees are not rescanned.
FORBIDDEN_MANIFEST_KEY_SUBSTRINGS: tuple[str, ...] = (
    "model", "prediction", "_score", "signal", "_entry", "_exit", "pnl",
    "equity", "profit", "_loss", "_position", "alpha", "_edge", "mfe", "mae",
    "r_multiple", "barrier", "mark_price", "funding", "open_interest",
    "order_book", "cross_venue", "ethusdt", "v003", "research_ready",
    "admissible", "approved_for_backtest",
)
_MANIFEST_SCAN_SKIP_SUBTREES: frozenset[str] = frozenset(
    {"governance_labels", "non_authorization_flags", "boundary_confirmations"}
)

# Manifest required fields (Phase 4bn-W label segment manifest contract).
REQUIRED_MANIFEST_FIELDS: tuple[str, ...] = (
    "dataset_family", "dataset_version", "version", "label_schema_version",
    "label_family_id", "segment_label", "data_family", "symbol", "symbol_list",
    "market", "dataset_category", "phase", "phase_id", "source_phase_boundary",
    "created_at_unix_ms", "created_at_utc", "code_commit_sha", "base_commit_sha",
    "label_config_hash", "feature_config_hash", "column_count",
    "label_column_count", "support_column_count", "lineage_column_count",
    "schema_column_list", "label_list", "support_column_list",
    "lineage_column_list", "horizon_list", "horizon_ms_list",
    "envelope_terminal_unix_ms", "envelope_terminal_utc_date",
    "censored_per_horizon", "invalid_price_row_count", "anchor_policy",
    "future_reference_policy", "direction_threshold_policy",
    "null_censoring_policy", "dtype_policy", "label_config_hash_input_fields",
    "lineage_column_reinterpretation", "date_start", "date_end", "date_count",
    "date_list", "expected_file_count", "produced_file_count",
    "total_row_count", "total_footprint_bytes", "per_day_outputs",
    "source_feature_dataset_family", "source_feature_dataset_version",
    "source_feature_segment_manifest_path",
    "source_feature_segment_manifest_sha256",
    "source_feature_segment_manifest_sidecar_sha256",
    "source_feature_layer_gate_report_path",
    "source_feature_layer_gate_report_sha256", "source_feature_schema_version",
    "source_normalized_dataset_family", "source_normalized_dataset_version",
    "source_normalized_segment_manifest_path",
    "source_normalized_segment_manifest_sha256",
    "source_normalized_segment_manifest_sidecar_sha256",
    "source_normalized_layer_gate_report_path",
    "source_normalized_layer_gate_report_sha256",
    "source_normalized_schema_version", "source_raw_segment_manifest_path",
    "source_raw_segment_manifest_sha256", "source_eligibility_posture",
    "existing_v002_label_reference", "existing_v002_terminal_window",
    "existing_v002_sealed_test_split", "full_intended_envelope_start",
    "full_intended_envelope_end", "research_eligible", "eligibility_gate_status",
    "no_successor_authorization", "ml_use", "diagnostics_use", "strategy_use",
    "backtest_use", "chronological_split_policy", "governance_labels",
    "boundary_confirmations", "non_authorization_flags",
    "v002_terminal_window_mode", "sealed_test_split_touched",
    "test_holdout_touched", "test_rows_loaded", "partitioning_rule",
    "primary_key", "storage_format", "sidecar_policy", "budget_witnesses",
)

# Governance-label keys that must read ``forbidden`` at the label layer.
REQUIRED_FORBIDDEN_GOVERNANCE_KEYS: tuple[str, ...] = (
    "ml", "diagnostics", "strategy", "backtest", "research_use",
    "paper_shadow_live", "deployment", "exchange_write",
)
# Non-authorization flags that must read ``False``.
REQUIRED_NON_AUTHORIZATION_FLAG_KEYS: tuple[str, ...] = (
    "acquisition_authorized", "backtest_authorized", "diagnostics_authorized",
    "label_family_research_use_authorized", "ml_authorized",
    "stage_5_label_cleared", "strategy_authorized",
    "successor_authorization_after",
)

GATE_PASS = (
    "LABEL_LAYER_GATE_PASSED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
)
GATE_FAIL = "LABEL_LAYER_GATE_FAILED__REMAIN_PAUSED"
GATE_NOT_RUN_MISSING = (
    "LABEL_LAYER_GATE_NOT_RUN__MISSING_LOCAL_ARTEFACTS__REMAIN_PAUSED"
)


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
    recomputed_label_config_hash: str | None = None
    recomputed_envelope_terminal_unix_ms: int = 0
    recomputed_censored_per_horizon: dict[str, int] = field(default_factory=dict)
    recomputed_invalid_price_row_count: int = 0
    wall_clock_seconds: float = 0.0


# ---------------------------------------------------------------------------
# Segment-scoped label_config_hash recomputation (mirrors the locked Phase
# 4bn-W builder ``build_label_config_hash_v002_pre_v002_segment`` exactly).
# ---------------------------------------------------------------------------

_V002_ENVELOPE_CLAUSE = (
    "envelope_terminal_unix_ms="
    "max_source_transact_time_ms_across_v002_90day_envelope"
)
_SEGMENT_ENVELOPE_CLAUSE = (
    "envelope_terminal_unix_ms="
    "max_source_transact_time_ms_across_pre_v002_segment_2024-03-01_to_2024-11-30"
)


def _segment_future_reference_policy() -> str:
    """Return the pre-v002-segment future-reference policy string (read-only)."""
    if _V002_ENVELOPE_CLAUSE not in FUTURE_REFERENCE_POLICY_V002:
        raise NormalizationIOError(
            "locked FUTURE_REFERENCE_POLICY_V002 envelope clause not found; kernel drift"
        )
    out = FUTURE_REFERENCE_POLICY_V002.replace(
        _V002_ENVELOPE_CLAUSE, _SEGMENT_ENVELOPE_CLAUSE
    )
    if out == FUTURE_REFERENCE_POLICY_V002 or _V002_ENVELOPE_CLAUSE in out:
        raise NormalizationIOError(
            "segment future-reference policy did not re-specify the envelope clause"
        )
    return out


def recompute_segment_label_config_hash(
    *,
    source_feature_manifest_sha256: str,
    source_feature_layer_gate_report_sha256: str,
    source_normalized_manifest_sha256: str,
    source_normalized_layer_gate_report_sha256: str,
    source_raw_manifest_sha256: str,
    feature_config_hash: str,
) -> str:
    """Recompute the deterministic segment-scoped ``label_config_hash``."""
    hex64 = {
        "source_feature_manifest_sha256": source_feature_manifest_sha256,
        "source_feature_layer_gate_report_sha256": (
            source_feature_layer_gate_report_sha256
        ),
        "source_normalized_manifest_sha256": source_normalized_manifest_sha256,
        "source_normalized_layer_gate_report_sha256": (
            source_normalized_layer_gate_report_sha256
        ),
        "source_raw_manifest_sha256": source_raw_manifest_sha256,
        "feature_config_hash": feature_config_hash,
    }
    for name, val in hex64.items():
        if not isinstance(val, str) or len(val) != 64 or val.lower() != val:
            raise NormalizationIOError(f"{name} must be 64-char lowercase hex")
    if feature_config_hash == PUBLISHED_V002_FEATURE_CONFIG_HASH:
        raise NormalizationIOError(
            "published v002 feature_config_hash (819cfa7a…) is not valid for the "
            "pre-v002 segment"
        )
    payload: dict[str, Any] = {
        "dataset_family": LABEL_DATASET_FAMILY_V002,
        "dataset_version": LABEL_DATASET_VERSION_V002,
        "label_schema_version": LABEL_SCHEMA_VERSION_V002,
        "segment_label": SEGMENT_LABEL,
        "label_list": list(LABEL_NAMES_V002),
        "support_column_list": list(LABEL_SUPPORT_COLUMN_NAMES_V002),
        "lineage_column_list": list(LABEL_LINEAGE_COLUMNS_V002),
        "horizon_list": list(LABEL_HORIZONS_V002),
        "horizon_ms_list": list(LABEL_HORIZON_MS_V002),
        "anchor_policy": ANCHOR_POLICY_V002,
        "future_reference_policy_pre_v002_segment": _segment_future_reference_policy(),
        "direction_threshold_policy": DIRECTION_THRESHOLD_POLICY_V002,
        "null_censoring_policy": NULL_CENSORING_POLICY_V002,
        "dtype_policy": DTYPE_POLICY_V002,
        "source_feature_manifest_sha256": source_feature_manifest_sha256,
        "source_feature_layer_gate_report_sha256": (
            source_feature_layer_gate_report_sha256
        ),
        "source_normalized_manifest_sha256": source_normalized_manifest_sha256,
        "source_normalized_layer_gate_report_sha256": (
            source_normalized_layer_gate_report_sha256
        ),
        "source_raw_manifest_sha256": source_raw_manifest_sha256,
        "feature_config_hash": feature_config_hash,
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _utc_date_to_day_start_ms(utc_date: str) -> int:
    day = datetime.strptime(utc_date, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(day.timestamp() * 1000)


def _ms_to_utc_date(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=UTC).strftime("%Y-%m-%d")


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


def _assert_under_gate_reports_labels(path: Path, repo_root: Path) -> None:
    """Fail closed unless *path* resolves under data/microstructure/gate-reports/labels/."""
    assert_path_under_microstructure(path, label="label gate report path")
    expected_root = (
        repo_root / "data" / "microstructure" / "gate-reports" / "labels"
    ).resolve()
    try:
        path.resolve().relative_to(expected_root)
    except ValueError as exc:
        raise NormalizationIOError(
            f"label gate report path must be under {expected_root}"
        ) from exc


def _git_branch(repo_root: Path) -> str | None:
    """Return the current branch name by reading ``.git/HEAD`` (no subprocess)."""
    head_file = repo_root / ".git" / "HEAD"
    if not head_file.exists():
        return None
    head_ref = head_file.read_text(encoding="utf-8").strip()
    if head_ref.startswith("ref:"):
        ref = head_ref.split(" ", 1)[1].strip()
        return ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ref
    return "DETACHED"


# ---------------------------------------------------------------------------
# Manifest contract
# ---------------------------------------------------------------------------


def _check_manifest_contract(manifest: Mapping[str, Any], checks: list[CheckResult]) -> bool:
    """Validate required-field + identity + schema + posture + governance + lineage."""
    ok = True
    missing = [k for k in REQUIRED_MANIFEST_FIELDS if k not in manifest]
    _add(checks, "manifest.required_fields", "required fields present",
         not missing, f"missing: {missing}" if missing else "")
    ok = ok and not missing

    identity_ok = (
        manifest.get("dataset_family") == LABEL_DATASET_FAMILY
        and manifest.get("dataset_version") == LABEL_DATASET_VERSION
        and manifest.get("version") == LABEL_DATASET_VERSION
        and manifest.get("label_schema_version") == LABEL_SCHEMA_VERSION
        and manifest.get("label_family_id") == LABEL_DATASET_FAMILY
        and manifest.get("segment_label") == SEGMENT_LABEL
        and manifest.get("data_family") == DATA_FAMILY
        and manifest.get("symbol") == SYMBOL
        and manifest.get("symbol_list") == [SYMBOL]
        and manifest.get("market") == MARKET
        and manifest.get("dataset_category") == DATASET_CATEGORY
        and manifest.get("phase_id") == SEGMENT_PRODUCER_PHASE_ID
    )
    _add(checks, "manifest.identity", "identity/scope fields match", identity_ok,
         "" if identity_ok else "identity mismatch")
    ok = ok and identity_ok

    schema_ok = (
        manifest.get("column_count") == EXPECTED_COLUMN_COUNT
        and manifest.get("label_column_count") == EXPECTED_LABEL_COLUMN_COUNT
        and manifest.get("support_column_count") == EXPECTED_SUPPORT_COLUMN_COUNT
        and manifest.get("lineage_column_count") == EXPECTED_LINEAGE_COLUMN_COUNT
        and tuple(manifest.get("schema_column_list", ())) == LABEL_SCHEMA_V002
        and tuple(manifest.get("label_list", ())) == LABEL_NAMES_V002
        and tuple(manifest.get("support_column_list", ())) == LABEL_SUPPORT_COLUMN_NAMES_V002
        and tuple(manifest.get("lineage_column_list", ())) == LABEL_LINEAGE_COLUMNS_V002
        and list(manifest.get("horizon_list", ())) == list(LABEL_HORIZONS_V002)
        and list(manifest.get("horizon_ms_list", ())) == list(LABEL_HORIZON_MS_V002)
    )
    _add(checks, "manifest.schema_description",
         "schema counts/order == LABEL_SCHEMA_V002 (40 cols)", schema_ok,
         "" if schema_ok else "schema description mismatch")
    ok = ok and schema_ok

    window_ok = (
        manifest.get("date_start") == EXPECTED_DATE_START
        and manifest.get("date_end") == EXPECTED_DATE_END
        and manifest.get("date_count") == EXPECTED_DATE_COUNT
        and manifest.get("expected_file_count") == EXPECTED_DATE_COUNT
        and manifest.get("produced_file_count") == EXPECTED_DATE_COUNT
        and manifest.get("total_row_count") == EXPECTED_TOTAL_ROW_COUNT
        and manifest.get("total_footprint_bytes") == EXPECTED_TOTAL_FOOTPRINT_BYTES
        and manifest.get("full_intended_envelope_start") == FULL_ENVELOPE_START
        and manifest.get("full_intended_envelope_end") == FULL_ENVELOPE_END
    )
    _add(checks, "manifest.window", "window/inventory totals match", window_ok,
         "" if window_ok else "window mismatch")
    ok = ok and window_ok

    hash_ok = (
        manifest.get("label_config_hash") == EXPECTED_LABEL_CONFIG_HASH
        and manifest.get("feature_config_hash") == EXPECTED_FEATURE_CONFIG_HASH
        and manifest.get("feature_config_hash") != PUBLISHED_V002_FEATURE_CONFIG_HASH
        and manifest.get("envelope_terminal_unix_ms") == EXPECTED_ENVELOPE_TERMINAL_UNIX_MS
        and manifest.get("envelope_terminal_utc_date") == EXPECTED_ENVELOPE_TERMINAL_UTC_DATE
        and manifest.get("invalid_price_row_count") == EXPECTED_INVALID_PRICE_ROW_COUNT
        and dict(manifest.get("censored_per_horizon", {})) == EXPECTED_CENSORED_PER_HORIZON
    )
    _add(checks, "manifest.hash_envelope_censoring",
         "label/feature config hashes, envelope terminal, censored/invalid totals",
         hash_ok, "" if hash_ok else "hash/envelope/censoring mismatch")
    ok = ok and hash_ok

    lineage_ok = (
        manifest.get("source_feature_dataset_family")
        == "microstructure_features_aggtrades_v001"
        and manifest.get("source_normalized_dataset_family")
        == "microstructure_normalized_aggtrades_v001"
        and manifest.get("source_feature_segment_manifest_sha256")
        == EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA
        and manifest.get("source_feature_segment_manifest_sidecar_sha256")
        == EXPECTED_FEATURE_SEGMENT_MANIFEST_SIDECAR_SHA
        and manifest.get("source_feature_layer_gate_report_sha256")
        == EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA
        and manifest.get("source_normalized_segment_manifest_sha256")
        == EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA
        and manifest.get("source_normalized_segment_manifest_sidecar_sha256")
        == EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA
        and manifest.get("source_normalized_layer_gate_report_sha256")
        == EXPECTED_NORMALIZED_GATE_REPORT_SHA
        and manifest.get("source_raw_segment_manifest_sha256")
        == EXPECTED_RAW_SEGMENT_MANIFEST_SHA
        and manifest.get("source_eligibility_posture")
        == "non_eligible_gate_passed_pending"
    )
    _add(checks, "manifest.lineage", "predecessor lineage SHAs/posture recorded",
         lineage_ok, "" if lineage_ok else "lineage mismatch")
    ok = ok and lineage_ok

    reinterp = manifest.get("lineage_column_reinterpretation") or {}
    feat_remap = reinterp.get(LINEAGE_REMAP_FEATURE_LAYER_GATE_COLUMN) or {}
    norm_remap = reinterp.get(LINEAGE_REMAP_NORMALIZED_LAYER_GATE_COLUMN) or {}
    remap_ok = (
        feat_remap.get("value") == EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA
        and norm_remap.get("value") == EXPECTED_NORMALIZED_GATE_REPORT_SHA
    )
    _add(checks, "manifest.lineage_remap",
         "lineage_column_reinterpretation binds 4bn-T/4bn-P gate SHAs", remap_ok,
         "" if remap_ok else "lineage remap mismatch")
    ok = ok and remap_ok

    posture_ok = (
        manifest.get("research_eligible") is False
        and manifest.get("eligibility_gate_status") == "pending"
        and manifest.get("no_successor_authorization") is True
        and manifest.get("chronological_split_policy") == "not_yet_defined"
    )
    _add(checks, "manifest.posture",
         "non-eligible posture (research_eligible/pending/no-successor)", posture_ok,
         "" if posture_ok else "posture mismatch")
    ok = ok and posture_ok

    gov = manifest.get("governance_labels") or {}
    governance_ok = (
        manifest.get("ml_use") == "forbidden"
        and manifest.get("diagnostics_use") == "forbidden"
        and manifest.get("strategy_use") == "forbidden"
        and manifest.get("backtest_use") == "forbidden"
        and all(gov.get(k) == "forbidden" for k in REQUIRED_FORBIDDEN_GOVERNANCE_KEYS)
        and gov.get("acquisition") == "unauthorized"
    )
    _add(checks, "manifest.governance",
         "ml/diagnostics/strategy/backtest forbidden governance", governance_ok,
         "" if governance_ok else "governance mismatch")
    ok = ok and governance_ok

    naf = manifest.get("non_authorization_flags") or {}
    naf_ok = all(naf.get(k) is False for k in REQUIRED_NON_AUTHORIZATION_FLAG_KEYS)
    _add(checks, "manifest.non_authorization",
         "all non-authorization flags false", naf_ok,
         "" if naf_ok else "non-authorization flag set")
    ok = ok and naf_ok

    term = manifest.get("existing_v002_terminal_window") or {}
    sealed = manifest.get("existing_v002_sealed_test_split") or {}
    v002_ok = (
        manifest.get("v002_terminal_window_mode") == "by_reference"
        and term.get("read") is False
        and term.get("feature_normalized_raw_dates_read") is False
        and manifest.get("sealed_test_split_touched") is False
        and manifest.get("test_holdout_touched") is False
        and manifest.get("test_rows_loaded") == 0
        and sealed.get("touched") is False
    )
    _add(checks, "manifest.v002_terminal_sealed",
         "v002 terminal by-reference + sealed-test untouched + test_rows_loaded=0",
         v002_ok, "" if v002_ok else "v002 terminal/sealed posture mismatch")
    ok = ok and v002_ok

    ref = manifest.get("existing_v002_label_reference") or {}
    pub_ok = (
        ref.get("read") is False
        and ref.get("mutated") is False
        and ref.get("path") == PUBLISHED_V002_LABEL_MANIFEST_REL
        and FAMILY_DIR_NAME != PUBLISHED_V002_LABEL_DIR_NAME
        and SEGMENT_MANIFEST_BASENAME != PUBLISHED_V002_LABEL_MANIFEST_BASENAME
    )
    _add(checks, "manifest.published_v002_by_reference",
         "published __v002 label by-reference, unread, not mutated, path-disjoint",
         pub_ok, "" if pub_ok else "published __v002 reference mismatch")
    ok = ok and pub_ok

    storage_ok = (
        manifest.get("partitioning_rule") == "<SYMBOL>/<YYYY>/<MM>/"
        and manifest.get("primary_key") == ["symbol", "utc_date", "agg_trade_id", "row_index"]
        and manifest.get("storage_format") == "parquet_zstd"
        and manifest.get("sidecar_policy") == "canonical_two_space_sha256"
    )
    _add(checks, "manifest.storage", "partition/primary-key/storage/sidecar policy",
         storage_ok, "" if storage_ok else "storage policy mismatch")
    ok = ok and storage_ok

    # Forbidden field-name scan (skip declaration subtrees).
    forbidden_hits: list[str] = []

    def _scan(obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                low = str(k).lower()
                for needle in FORBIDDEN_MANIFEST_KEY_SUBSTRINGS:
                    if needle in low:
                        forbidden_hits.append(f"{needle} in {k}")
                if k in _MANIFEST_SCAN_SKIP_SUBTREES:
                    continue
                _scan(v)
        elif isinstance(obj, list):
            for item in obj:
                _scan(item)

    _scan(manifest)
    _add(checks, "manifest.forbidden_fields", "no forbidden field names", not forbidden_hits,
         "" if not forbidden_hits else f"hits: {forbidden_hits}")
    ok = ok and not forbidden_hits

    # Recompute the segment-scoped label_config_hash from the manifest inputs.
    try:
        recomputed = recompute_segment_label_config_hash(
            source_feature_manifest_sha256=str(
                manifest.get("source_feature_segment_manifest_sha256", "")),
            source_feature_layer_gate_report_sha256=str(
                manifest.get("source_feature_layer_gate_report_sha256", "")),
            source_normalized_manifest_sha256=str(
                manifest.get("source_normalized_segment_manifest_sha256", "")),
            source_normalized_layer_gate_report_sha256=str(
                manifest.get("source_normalized_layer_gate_report_sha256", "")),
            source_raw_manifest_sha256=str(
                manifest.get("source_raw_segment_manifest_sha256", "")),
            feature_config_hash=str(manifest.get("feature_config_hash", "")),
        )
    except NormalizationIOError:
        recomputed = "<error>"
    recompute_ok = (
        recomputed == EXPECTED_LABEL_CONFIG_HASH
        and recomputed == manifest.get("label_config_hash")
    )
    _add(checks, "manifest.label_config_hash_recompute",
         "label_config_hash recomputes from manifest inputs", recompute_ok,
         recomputed)
    ok = ok and recompute_ok
    return ok


# ---------------------------------------------------------------------------
# Per-file full-scan validation
# ---------------------------------------------------------------------------

# Numeric/flag columns materialised for per-row censoring validation.
_HORIZON_FLAG_COLS = [f"horizon_censored_flag_{h}" for h in LABEL_HORIZONS_V002]
_HORIZON_REFTS_COLS = [f"reference_timestamp_ms_{h}" for h in LABEL_HORIZONS_V002]
_HORIZON_FLR_COLS = [f"forward_log_return_{h}" for h in LABEL_HORIZONS_V002]
_HORIZON_DIR_COLS = [f"forward_direction_{h}" for h in LABEL_HORIZONS_V002]

_NUMERIC_SCAN_COLS = (
    ["row_index", "agg_trade_id", "feature_timestamp_ms", "source_transact_time_ms"]
    + _HORIZON_FLAG_COLS + _HORIZON_REFTS_COLS + _HORIZON_FLR_COLS + _HORIZON_DIR_COLS
    + ["label_invalid_price_flag", "label_any_censored_flag"]
)


def _constant_string_expectations() -> dict[str, str]:
    return {
        "dataset_family": LABEL_DATASET_FAMILY,
        "dataset_version": LABEL_DATASET_VERSION,
        "label_schema_version": LABEL_SCHEMA_VERSION,
        "symbol": SYMBOL,
        "label_config_hash": EXPECTED_LABEL_CONFIG_HASH,
        "source_feature_manifest_sha256": EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA,
        LINEAGE_REMAP_FEATURE_LAYER_GATE_COLUMN: EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA,
        LINEAGE_REMAP_NORMALIZED_LAYER_GATE_COLUMN: EXPECTED_NORMALIZED_GATE_REPORT_SHA,
        "source_normalized_manifest_sha256": EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA,
        "source_raw_manifest_sha256": EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
    }


@dataclass
class FileScanResult:
    ok: bool
    row_count: int
    censored_per_horizon: dict[str, int]
    invalid_price_count: int
    max_feature_ts: int
    detail: str = ""


def _deep_scan_label_file(
    pq: Any, pc: Any, np: Any, pq_path: Path, date: str, entry: Mapping[str, Any],
) -> FileScanResult:
    """Full per-row scan of a single label Parquet (no sampling).

    Validates schema, forbidden columns, constant lineage/hash columns,
    row identity, per-horizon envelope-terminal censoring, reference-timestamp
    bounds, the any-censored OR invariant, direction domain, and the
    invalid-price count for *every* row in the file.
    """
    pqf = pq.ParquetFile(str(pq_path))
    names = tuple(pqf.schema_arrow.names)
    if names != LABEL_SCHEMA_V002:
        return FileScanResult(False, 0, {}, 0, 0, "schema != LABEL_SCHEMA_V002")
    for col in names:
        low = col.lower()
        if any(n in low for n in FORBIDDEN_COLUMN_SUBSTRINGS):
            return FileScanResult(False, 0, {}, 0, 0, f"forbidden column {col!r}")
    n_meta = pqf.metadata.num_rows
    if n_meta != int(entry.get("row_count", -1)):
        return FileScanResult(False, 0, {}, 0, 0,
                              f"metadata rows {n_meta} != manifest {entry.get('row_count')}")

    needed = _NUMERIC_SCAN_COLS + list(_constant_string_expectations().keys()) + ["utc_date"]
    table = pq.read_table(str(pq_path), columns=needed)
    n = table.num_rows
    if n != n_meta:
        return FileScanResult(False, 0, {}, 0, 0, "table rows != metadata rows")

    # --- constant string lineage / identity / hash columns (exhaustive) ---
    for col_name, expected in _constant_string_expectations().items():
        col = table.column(col_name)
        if col.null_count != 0 or not bool(
            pc.all(pc.equal(col, pa_scalar(pc, expected))).as_py()
        ):
            return FileScanResult(False, 0, {}, 0, 0, f"{col_name} not constant=={expected}")
    utc_col = table.column("utc_date")
    if utc_col.null_count != 0 or not bool(
        pc.all(pc.equal(utc_col, pa_scalar(pc, date))).as_py()
    ):
        return FileScanResult(False, 0, {}, 0, 0, f"utc_date != {date}")

    # --- identity columns ---
    ri = table.column("row_index").combine_chunks().to_numpy(zero_copy_only=False)
    ft = table.column("feature_timestamp_ms").combine_chunks().to_numpy(zero_copy_only=False)
    src = table.column("source_transact_time_ms").combine_chunks().to_numpy(zero_copy_only=False)
    agg = table.column("agg_trade_id")
    if agg.null_count != 0:
        return FileScanResult(False, 0, {}, 0, 0, "agg_trade_id has nulls")
    if not np.array_equal(ri, np.arange(n, dtype=ri.dtype)):
        return FileScanResult(False, 0, {}, 0, 0, "row_index != arange(n)")
    if not np.array_equal(ft, src):
        return FileScanResult(False, 0, {}, 0, 0, "feature_timestamp_ms != source_transact_time_ms")
    max_ft = int(ft.max()) if n else 0
    if max_ft > EXPECTED_ENVELOPE_TERMINAL_UNIX_MS:
        return FileScanResult(False, 0, {}, 0, 0, "anchor feature_timestamp past envelope terminal")

    # --- invalid-price flag ---
    invalid = _bool_np(table.column("label_invalid_price_flag"))
    invalid_count = int(invalid.sum())
    if invalid_count != int(entry.get("invalid_price_row_count", -1)):
        return FileScanResult(False, 0, {}, 0, 0, "invalid_price count != manifest")

    # --- per-horizon censoring / reference / direction / log-return ---
    censored_per_horizon: dict[str, int] = {}
    any_expected = np.zeros(n, dtype=bool)
    terminal = np.int64(EXPECTED_ENVELOPE_TERMINAL_UNIX_MS)
    for h, h_ms in zip(LABEL_HORIZONS_V002, LABEL_HORIZON_MS_V002, strict=True):
        target = ft.astype(np.int64) + np.int64(h_ms)
        expected_censored = target > terminal
        any_expected = any_expected | expected_censored

        flag = _bool_np(table.column(f"horizon_censored_flag_{h}"))
        if not np.array_equal(flag, expected_censored):
            return FileScanResult(False, 0, {}, 0, 0, f"censor flag mismatch {h}")
        censored_per_horizon[h] = int(expected_censored.sum())

        ref_vals, ref_null = _nullable_np(pc, np, table.column(f"reference_timestamp_ms_{h}"), 0)
        if not np.array_equal(ref_null, expected_censored):
            return FileScanResult(False, 0, {}, 0, 0, f"reference null!=censored {h}")
        nz = ~expected_censored
        if nz.any():
            if not bool((ref_vals[nz] <= target[nz]).all()):
                return FileScanResult(False, 0, {}, 0, 0, f"reference_ts > target {h}")
            if not bool((ref_vals[nz] <= terminal).all()):
                return FileScanResult(False, 0, {}, 0, 0, f"reference_ts > terminal {h}")

        expected_label_null = expected_censored | invalid
        _flr_vals, flr_null = _nullable_np(pc, np, table.column(f"forward_log_return_{h}"), 0.0)
        if not np.array_equal(flr_null, expected_label_null):
            return FileScanResult(False, 0, {}, 0, 0, f"forward_log_return null!=expected {h}")
        dir_vals, dir_null = _nullable_np(pc, np, table.column(f"forward_direction_{h}"), 0)
        if not np.array_equal(dir_null, expected_label_null):
            return FileScanResult(False, 0, {}, 0, 0, f"forward_direction null!=expected {h}")
        dn = ~expected_label_null
        if dn.any() and not bool(np.isin(dir_vals[dn], np.array([-1, 0, 1])).all()):
            return FileScanResult(False, 0, {}, 0, 0, f"forward_direction not in -1/0/1 {h}")

    any_flag = _bool_np(table.column("label_any_censored_flag"))
    if not np.array_equal(any_flag, any_expected):
        return FileScanResult(False, 0, {}, 0, 0, "label_any_censored_flag != OR(horizons)")

    return FileScanResult(True, n, censored_per_horizon, invalid_count, max_ft, "ok")


def pa_scalar(pc: Any, value: Any) -> Any:
    """Build a pyarrow scalar for an equality compare (string columns)."""
    import pyarrow as pa
    return pa.scalar(value, type=pa.string())


def _bool_np(col: Any) -> Any:
    """Materialise a non-nullable boolean column to a numpy bool array."""
    return col.combine_chunks().to_numpy(zero_copy_only=False).astype(bool)


def _nullable_np(pc: Any, np: Any, col: Any, fill: Any) -> tuple[Any, Any]:
    """Return ``(values, null_mask)`` numpy arrays for a nullable column."""
    null_mask = pc.is_null(col).combine_chunks().to_numpy(zero_copy_only=False).astype(bool)
    vals = pc.fill_null(col, fill).combine_chunks().to_numpy(zero_copy_only=False)
    return vals, null_mask


# ---------------------------------------------------------------------------
# Predecessor integrity
# ---------------------------------------------------------------------------


def _check_predecessors(
    manifest: Mapping[str, Any], repo_root: Path, checks: list[CheckResult]
) -> None:
    """Verify predecessor manifest/gate SHAs + verdicts (read-only)."""
    def _abs(rel: str) -> Path:
        p = Path(rel)
        return p if p.is_absolute() else repo_root / rel

    # Feature segment manifest + sidecar.
    feat_man = _abs(str(manifest.get("source_feature_segment_manifest_path", "")))
    feat_man_ok = (
        feat_man.exists()
        and compute_file_sha256(feat_man)[0] == EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA
    )
    feat_sc = feat_man.with_suffix(feat_man.suffix + ".sha256")
    feat_sc_ok = (
        feat_sc.exists()
        and compute_file_sha256(feat_sc)[0] == EXPECTED_FEATURE_SEGMENT_MANIFEST_SIDECAR_SHA
    )
    if feat_man_ok:
        fp = json.loads(feat_man.read_bytes().decode("utf-8"))
        feat_post_ok = (
            fp.get("research_eligible") is False
            and fp.get("eligibility_gate_status") == "pending"
            and fp.get("feature_config_hash") == EXPECTED_FEATURE_CONFIG_HASH
        )
    else:
        feat_post_ok = False
    _add(checks, "predecessor.feature_manifest",
         "feature segment manifest SHA + sidecar + non-eligible/pending",
         feat_man_ok and feat_sc_ok and feat_post_ok, str(feat_man))

    # Feature-layer gate report (Phase 4bn-T): SHA + verdict + 27/27 PASS.
    feat_gate = _abs(str(manifest.get("source_feature_layer_gate_report_path", "")))
    feat_gate_ok = (
        feat_gate.exists()
        and compute_file_sha256(feat_gate)[0] == EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA
    )
    if feat_gate_ok:
        gp = json.loads(feat_gate.read_bytes().decode("utf-8"))
        rc = gp.get("checks", [])
        feat_gate_ok = (
            gp.get("overall_status") == "pass"
            and gp.get("gate_result_state") == REQUIRED_FEATURE_GATE_VERDICT
            and len(rc) == EXPECTED_FEATURE_GATE_CHECK_COUNT
            and sum(1 for c in rc if c.get("status") == "pass")
            == EXPECTED_FEATURE_GATE_CHECK_COUNT
            and gp.get("segment_non_eligible") is True
            and gp.get("research_eligible_after") is False
        )
    _add(checks, "predecessor.feature_gate",
         "feature-layer gate (4bn-T) SHA + verdict + 27/27 PASS", feat_gate_ok,
         str(feat_gate))

    # Normalized segment manifest + sidecar.
    norm_man = _abs(str(manifest.get("source_normalized_segment_manifest_path", "")))
    norm_man_ok = (
        norm_man.exists()
        and compute_file_sha256(norm_man)[0] == EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA
    )
    norm_sc = norm_man.with_suffix(norm_man.suffix + ".sha256")
    norm_sc_ok = (
        norm_sc.exists()
        and compute_file_sha256(norm_sc)[0] == EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA
    )
    if norm_man_ok:
        npm = json.loads(norm_man.read_bytes().decode("utf-8"))
        norm_post_ok = (
            npm.get("research_eligible") is False
            and npm.get("eligibility_gate_status") == "pending"
        )
    else:
        norm_post_ok = False
    _add(checks, "predecessor.normalized_manifest",
         "normalized segment manifest SHA + sidecar + non-eligible/pending",
         norm_man_ok and norm_sc_ok and norm_post_ok, str(norm_man))

    # Normalized-layer gate report (Phase 4bn-P): SHA + verdict + 25/25 PASS.
    norm_gate = _abs(str(manifest.get("source_normalized_layer_gate_report_path", "")))
    norm_gate_ok = (
        norm_gate.exists()
        and compute_file_sha256(norm_gate)[0] == EXPECTED_NORMALIZED_GATE_REPORT_SHA
    )
    if norm_gate_ok:
        gp = json.loads(norm_gate.read_bytes().decode("utf-8"))
        rc = gp.get("checks", [])
        norm_gate_ok = (
            gp.get("overall_status") == "pass"
            and gp.get("gate_result_state") == REQUIRED_NORMALIZED_GATE_VERDICT
            and len(rc) == EXPECTED_NORMALIZED_GATE_CHECK_COUNT
            and sum(1 for c in rc if c.get("status") == "pass")
            == EXPECTED_NORMALIZED_GATE_CHECK_COUNT
            and gp.get("segment_non_eligible") is True
            and gp.get("research_eligible_after") is False
        )
    _add(checks, "predecessor.normalized_gate",
         "normalized-layer gate (4bn-P) SHA + verdict + 25/25 PASS", norm_gate_ok,
         str(norm_gate))

    # Raw segment manifest SHA.
    raw_man = _abs(str(manifest.get("source_raw_segment_manifest_path", "")))
    raw_man_ok = (
        raw_man.exists()
        and compute_file_sha256(raw_man)[0] == EXPECTED_RAW_SEGMENT_MANIFEST_SHA
    )
    _add(checks, "predecessor.raw_manifest", "raw segment manifest SHA matches",
         raw_man_ok, str(raw_man))


# ---------------------------------------------------------------------------
# Gate core
# ---------------------------------------------------------------------------


def run_gate(
    *,
    manifest_path: Path,
    gate_reports_root: Path,
    repo_root: Path,
    write_report: bool = True,
    refuse_overwrite: bool = True,
) -> GateResult:
    """Run the Phase 4bn-X label-layer eligibility gate once (read-only)."""
    import numpy as np
    import pyarrow.compute as pc
    import pyarrow.parquet as pq

    start = time.monotonic()
    checks: list[CheckResult] = []

    if not manifest_path.exists():
        return GateResult(result_state=GATE_NOT_RUN_MISSING, overall_status="not_run",
                          checks=[CheckResult("manifest.exists", "label segment manifest exists",
                                              "fail", str(manifest_path))],
                          wall_clock_seconds=time.monotonic() - start)

    # --- repo / gitignore context ---
    branch = _git_branch(repo_root)
    repo_ctx_ok = branch is None or branch not in ("main", "master")
    _add(checks, "context.repo_branch", "running off the protected default branch is refused",
         repo_ctx_ok, f"branch={branch}")
    gi = repo_root / ".gitignore"
    if gi.exists():
        gi_text = gi.read_text(encoding="utf-8")
        gi_ok = "data/microstructure/" in gi_text and "data/research/" in gi_text
    else:
        gi_ok = False
    _add(checks, "context.gitignore",
         "data/microstructure and data/research are gitignored", gi_ok, str(gi))

    # --- manifest hash + sidecar ---
    man_sha, _ = compute_file_sha256(manifest_path)
    man_sha_ok = man_sha == EXPECTED_MANIFEST_SHA
    checks.append(CheckResult("manifest.sha", "label manifest SHA256 matches",
                              "pass" if man_sha_ok else "fail", man_sha))
    sidecar_path = manifest_path.with_suffix(manifest_path.suffix + ".sha256")
    if not sidecar_path.exists():
        checks.append(CheckResult("manifest.sidecar", "manifest sidecar exists", "fail",
                                  str(sidecar_path)))
    else:
        sc_ok, sc_sha, sc_detail = _validate_canonical_sidecar(sidecar_path, manifest_path.name)
        sidecar_self_sha = compute_file_sha256(sidecar_path)[0]
        sc_match = (
            sc_ok
            and sc_sha == man_sha
            and sidecar_self_sha == EXPECTED_MANIFEST_SIDECAR_SHA
        )
        checks.append(CheckResult("manifest.sidecar", "manifest sidecar canonical + matches",
                                  "pass" if sc_match else "fail",
                                  sc_detail if not sc_ok else (
                                      "ok" if sc_match else "sidecar sha mismatch")))

    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    _check_manifest_contract(manifest, checks)

    inventory: list[dict[str, Any]] = list(manifest.get("per_day_outputs", []))
    date_list: list[str] = list(manifest.get("date_list", []))

    # --- date coverage ---
    coverage_ok = (
        len(inventory) == EXPECTED_DATE_COUNT
        and len(date_list) == EXPECTED_DATE_COUNT
        and len(set(date_list)) == EXPECTED_DATE_COUNT
        and [e["date"] for e in inventory] == date_list
        and bool(date_list)
        and date_list[0] == EXPECTED_DATE_START
        and date_list[-1] == EXPECTED_DATE_END
        and all(_date_in_segment(d) for d in date_list)
        and all(d < V002_TERMINAL_START for d in date_list)
        and not any(SEALED_TEST_START <= d <= SEALED_TEST_END for d in date_list)
    )
    if coverage_ok:
        expected = []
        cur = datetime.strptime(EXPECTED_DATE_START, "%Y-%m-%d").replace(tzinfo=UTC)
        end = datetime.strptime(EXPECTED_DATE_END, "%Y-%m-%d").replace(tzinfo=UTC)
        while cur <= end:
            expected.append(cur.strftime("%Y-%m-%d"))
            cur = datetime.fromtimestamp(cur.timestamp() + 86400, UTC)
        coverage_ok = date_list == expected
    checks.append(CheckResult("coverage", "exactly 275 contiguous in-segment dates",
                              "pass" if coverage_ok else "fail", f"{len(date_list)} dates"))

    # --- per-file full scan ---
    total_rows = 0
    total_bytes = 0
    parquet_count = 0
    sidecar_count = 0
    per_file_fail = 0
    path_fail = 0
    hash_fail = 0
    schema_fail = 0
    forbidden_col_fail = 0
    rowcount_fail = 0
    scan_fail = 0
    censor_count_fail = 0
    censored_total: dict[str, int] = dict.fromkeys(LABEL_HORIZONS_V002, 0)
    invalid_total = 0
    max_terminal = 0
    first_scan_fail_detail = ""

    for entry in inventory:
        date = str(entry["date"])
        yyyy, mm, _dd = date.split("-")
        pq_path = _resolve_local_path(repo_root, str(entry["label_parquet_path"]))
        sc_path = _resolve_local_path(repo_root, str(entry["label_sidecar_path"]))

        expect_parts = (FAMILY_DIR_NAME, SYMBOL, yyyy, mm)
        layout_ok = (
            all(p in pq_path.parts for p in expect_parts)
            and pq_path.name == f"{SYMBOL}-labels-aggtrades-{date}.parquet"
            and PUBLISHED_V002_LABEL_DIR_NAME not in pq_path.parts
            and "v003" not in str(pq_path)
            and str(entry.get("symbol")) == SYMBOL
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
        if actual_sha != str(entry["label_parquet_sha256"]):
            hash_fail += 1
        if actual_size != int(entry["label_parquet_size_bytes"]):
            hash_fail += 1

        if not sc_path.exists():
            per_file_fail += 1
        else:
            sidecar_count += 1
            total_bytes += sc_path.stat().st_size
            sc_ok, sc_sha, _d = _validate_canonical_sidecar(sc_path, pq_path.name)
            if not sc_ok or sc_sha != actual_sha or sc_sha != str(entry["label_parquet_sha256"]):
                hash_fail += 1

        try:
            scan = _deep_scan_label_file(pq, pc, np, pq_path, date, entry)
        except Exception as exc:  # noqa: BLE001 - any read error is a gate failure
            scan = FileScanResult(False, 0, {}, 0, 0, f"read error: {exc!r}")
        if not scan.ok:
            scan_fail += 1
            if not first_scan_fail_detail:
                first_scan_fail_detail = f"{date}: {scan.detail}"
            if "schema" in scan.detail:
                schema_fail += 1
            if "forbidden" in scan.detail:
                forbidden_col_fail += 1
            if "rows" in scan.detail:
                rowcount_fail += 1
            continue
        total_rows += scan.row_count
        max_terminal = max(max_terminal, scan.max_feature_ts)
        invalid_total += scan.invalid_price_count
        for h in LABEL_HORIZONS_V002:
            censored_total[h] += scan.censored_per_horizon.get(h, 0)
        # Per-day censored-count cross-check against the manifest inventory.
        man_cph = entry.get("per_horizon_censored_counts") or {}
        if {h: scan.censored_per_horizon.get(h, 0) for h in LABEL_HORIZONS_V002} != {
            h: int(man_cph.get(h, -1)) for h in LABEL_HORIZONS_V002
        }:
            censor_count_fail += 1

    _add(checks, "files.present", "all 275 parquet+sidecar present",
         per_file_fail == 0, f"missing groups: {per_file_fail}")
    _add(checks, "files.hash_integrity", "parquet SHA == sidecar == manifest inventory",
         hash_fail == 0, f"hash failures: {hash_fail}")
    _add(checks, "files.path_layout", "segment path layout + basename correct",
         path_fail == 0, f"path failures: {path_fail}")
    _add(checks, "files.schema", "every parquet schema == LABEL_SCHEMA_V002 (40 cols)",
         schema_fail == 0, f"schema failures: {schema_fail}")
    _add(checks, "files.forbidden_columns", "no forbidden label columns",
         forbidden_col_fail == 0, f"forbidden-col hits: {forbidden_col_fail}")
    _add(checks, "files.row_counts", "per-file row count == manifest inventory",
         rowcount_fail == 0, f"rowcount failures: {rowcount_fail}")
    _add(checks, "files.full_scan",
         "full per-row scan (schema/constants/censoring/direction/OR/bounds)",
         scan_fail == 0, first_scan_fail_detail or f"scan failures: {scan_fail}")
    _add(checks, "files.censored_counts_per_day",
         "per-day per-horizon censored counts == manifest inventory",
         censor_count_fail == 0, f"per-day censor mismatches: {censor_count_fail}")

    rows_ok = total_rows == EXPECTED_TOTAL_ROW_COUNT
    _add(checks, "aggregate.rows", "recomputed total rows == 400,001,695", rows_ok, str(total_rows))
    bytes_ok = total_bytes == EXPECTED_TOTAL_FOOTPRINT_BYTES
    _add(checks, "aggregate.footprint", "recomputed footprint == 15,654,082,679 B",
         bytes_ok, str(total_bytes))
    count_ok = parquet_count == EXPECTED_DATE_COUNT and sidecar_count == EXPECTED_DATE_COUNT
    _add(checks, "aggregate.counts", "275 parquets + 275 sidecars", count_ok,
         f"{parquet_count}/{sidecar_count}")
    censored_ok = censored_total == EXPECTED_CENSORED_PER_HORIZON
    _add(checks, "aggregate.censored_per_horizon",
         "recomputed censored counts == 1s=3 5s=20 15s=42 60s=216", censored_ok,
         str(censored_total))
    invalid_ok = invalid_total == EXPECTED_INVALID_PRICE_ROW_COUNT
    _add(checks, "aggregate.invalid_price", "recomputed invalid-price row count == 0",
         invalid_ok, str(invalid_total))
    terminal_ok = (
        max_terminal == EXPECTED_ENVELOPE_TERMINAL_UNIX_MS
        and _ms_to_utc_date(max_terminal) == EXPECTED_ENVELOPE_TERMINAL_UTC_DATE
    )
    _add(checks, "aggregate.envelope_terminal",
         "max anchor feature_timestamp == envelope terminal 1733011199331 (2024-11-30)",
         terminal_ok, str(max_terminal))

    # --- label_config_hash recompute (segment-scoped, from manifest inputs) ---
    try:
        recomputed_hash = recompute_segment_label_config_hash(
            source_feature_manifest_sha256=str(
                manifest.get("source_feature_segment_manifest_sha256", "")),
            source_feature_layer_gate_report_sha256=str(
                manifest.get("source_feature_layer_gate_report_sha256", "")),
            source_normalized_manifest_sha256=str(
                manifest.get("source_normalized_segment_manifest_sha256", "")),
            source_normalized_layer_gate_report_sha256=str(
                manifest.get("source_normalized_layer_gate_report_sha256", "")),
            source_raw_manifest_sha256=str(
                manifest.get("source_raw_segment_manifest_sha256", "")),
            feature_config_hash=str(manifest.get("feature_config_hash", "")),
        )
    except NormalizationIOError as exc:
        recomputed_hash = f"<error: {exc}>"
    hash_recompute_ok = recomputed_hash == EXPECTED_LABEL_CONFIG_HASH
    _add(checks, "aggregate.label_config_hash_recompute",
         "segment label_config_hash recomputes to b3bd5d2b…", hash_recompute_ok,
         recomputed_hash)

    # --- predecessor integrity ---
    _check_predecessors(manifest, repo_root, checks)

    overall = "pass" if all(c.status == "pass" for c in checks) else "fail"
    result_state = GATE_PASS if overall == "pass" else GATE_FAIL

    res = GateResult(
        result_state=result_state, overall_status=overall, checks=checks,
        recomputed_total_rows=total_rows, recomputed_total_footprint_bytes=total_bytes,
        parquet_count=parquet_count, sidecar_count=sidecar_count,
        recomputed_label_config_hash=recomputed_hash,
        recomputed_envelope_terminal_unix_ms=max_terminal,
        recomputed_censored_per_horizon=dict(censored_total),
        recomputed_invalid_price_row_count=invalid_total,
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


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------


def _atomic_write_json(
    path: Path, obj: Mapping[str, Any], *, repo_root: Path, refuse_overwrite: bool
) -> tuple[str, int]:
    if not isinstance(path, Path):
        raise NormalizationIOError("path must be a pathlib.Path")
    _assert_under_gate_reports_labels(path, repo_root)
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
        f"{FAMILY_DIR_NAME}__{PHASE_ID}__{run_id}__{BASE_MAIN_SHORT}.json"
    )
    report_path = gate_reports_root / report_basename
    n_pass = sum(1 for c in res.checks if c.status == "pass")
    n_fail = sum(1 for c in res.checks if c.status == "fail")
    report = {
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "phase": PHASE_ID,
        "phase_id": PHASE_ID,
        "artefact_type": "label_layer_eligibility_gate_report",
        "base_commit_sha": BASE_MAIN_SHA,
        "created_at_unix_ms": run_id,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "gate_result_state": res.result_state,
        "overall_status": res.overall_status,
        "gate_verdict": "LABEL_LAYER_GATE_PASS" if res.overall_status == "pass"
        else "LABEL_LAYER_GATE_FAIL",
        "checks_passed": n_pass,
        "checks_failed": n_fail,
        "input_label_manifest_path": str(
            manifest_path.resolve().relative_to(repo_root.resolve())).replace(os.sep, "/"),
        "input_label_manifest_sha256": manifest_sha,
        "input_label_manifest_sidecar_path": str(
            manifest_path.resolve().relative_to(repo_root.resolve())).replace(os.sep, "/")
        + ".sha256",
        "input_label_manifest_sidecar_sha256": EXPECTED_MANIFEST_SIDECAR_SHA,
        "input_label_segment_directory": (
            f"data/microstructure/labels/{FAMILY_DIR_NAME}/"),
        "input_label_parquet_count": res.parquet_count,
        "input_label_sidecar_count": res.sidecar_count,
        "dataset_family": LABEL_DATASET_FAMILY,
        "dataset_version": LABEL_DATASET_VERSION,
        "label_schema_version": LABEL_SCHEMA_VERSION,
        "segment_label": SEGMENT_LABEL,
        "symbol_list": [SYMBOL],
        "market": MARKET,
        "data_family": DATA_FAMILY,
        "date_start": EXPECTED_DATE_START,
        "date_end": EXPECTED_DATE_END,
        "date_count": EXPECTED_DATE_COUNT,
        "recomputed_total_row_count": res.recomputed_total_rows,
        "recomputed_total_footprint_bytes": res.recomputed_total_footprint_bytes,
        "recomputed_label_config_hash": res.recomputed_label_config_hash,
        "recomputed_envelope_terminal_unix_ms": res.recomputed_envelope_terminal_unix_ms,
        "recomputed_envelope_terminal_utc_date": (
            _ms_to_utc_date(res.recomputed_envelope_terminal_unix_ms)
            if res.recomputed_envelope_terminal_unix_ms else None),
        "recomputed_censored_per_horizon": res.recomputed_censored_per_horizon,
        "recomputed_invalid_price_row_count": res.recomputed_invalid_price_row_count,
        "expected_label_config_hash": EXPECTED_LABEL_CONFIG_HASH,
        "expected_feature_config_hash": EXPECTED_FEATURE_CONFIG_HASH,
        "checks": [{"check_id": c.check_id, "title": c.title, "status": c.status,
                    "detail": c.detail} for c in res.checks],
        "predecessor_feature_segment_manifest_sha256":
            EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA,
        "predecessor_feature_layer_gate_report_sha256":
            EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA,
        "predecessor_feature_layer_gate_verdict": REQUIRED_FEATURE_GATE_VERDICT,
        "predecessor_normalized_segment_manifest_sha256":
            EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA,
        "predecessor_normalized_layer_gate_report_sha256":
            EXPECTED_NORMALIZED_GATE_REPORT_SHA,
        "predecessor_normalized_layer_gate_verdict": REQUIRED_NORMALIZED_GATE_VERDICT,
        "predecessor_raw_segment_manifest_sha256": EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
        "wall_clock_seconds": round(res.wall_clock_seconds, 3),
        "segment_non_eligible": True,
        "research_eligible_after": False,
        "eligibility_gate_status_after": "pending",
        "no_successor_authorization": True,
        "label_execution_rerun": False,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        "published_v002_label_mutated": False,
        "published_v002_label_read": False,
        "ml_run": False,
        "diagnostics_run": False,
        "strategy_run": False,
        "backtest_run": False,
        "data_research_output_created": False,
        "data_committed": False,
        "explicit_non_authorizations": [
            "no_eligibility_flip", "no_eligibility_gate_status_transition",
            "no_successor_authorization", "no_ml", "no_diagnostics", "no_strategy",
            "no_signals", "no_pnl", "no_backtests", "no_chronological_split_policy",
            "no_storage_migration", "no_database", "no_parquet_compaction", "no_v003",
            "no_data_research_output", "no_published_v002_mutation",
            "no_v002_terminal_read", "no_sealed_test_read",
        ],
    }
    # Writer invariants (unconditional).
    if (
        report["research_eligible_after"] is not False
        or report["eligibility_gate_status_after"] != "pending"
        or report["no_successor_authorization"] is not True
        or report["label_execution_rerun"] is not False
        or report["published_v002_label_mutated"] is not False
        or report["sealed_test_split_touched"] is not False
        or report["v002_terminal_window_read"] is not False
    ):
        raise NormalizationIOError("gate report invariant violation")
    report_sha, _ = _atomic_write_json(
        report_path, report, repo_root=repo_root, refuse_overwrite=refuse_overwrite)
    sidecar_path = report_path.with_suffix(report_path.suffix + ".sha256")
    _assert_under_gate_reports_labels(sidecar_path, repo_root)
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
            "Phase 4bn-X — Label-Layer Eligibility Gate over the Phase 4bn-W "
            "pre-v002 label segment. Read-only on data; writes at most one "
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
    print(f"[Phase 4bn-X] {res.result_state}")
    print(f"  overall={res.overall_status}; parquets={res.parquet_count}; "
          f"sidecars={res.sidecar_count}; rows={res.recomputed_total_rows}; "
          f"footprint={res.recomputed_total_footprint_bytes} B; "
          f"censored={res.recomputed_censored_per_horizon}; "
          f"invalid_price={res.recomputed_invalid_price_row_count}; "
          f"runtime={res.wall_clock_seconds:.1f}s")
    for c in res.checks:
        if c.status != "pass":
            print(f"  FAIL {c.check_id}: {c.title} -- {c.detail}")
    if res.report_path is not None:
        print(f"  report: {res.report_path} (sha256={res.report_sha256})")
    return 0 if res.overall_status == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
