"""Phase 4bn-W — Label-Only Pre-V002 BTCUSDT aggTrades Segment Execution.

Bounded, standalone orchestrator authorised by the Phase 4bn-W
authorization prompt and recommended by the Phase 4bn-V label
manifest / versioning memo
(``docs/00-meta/implementation-reports/2026-06-05_phase-4bn-v_label-manifest-versioning-memo.md``).

This script label-derives the **local, gitignored, non-eligible** Phase
4bn-S pre-v002 feature segment + Phase 4bn-O pre-v002 normalized segment
(BTCUSDT / Binance USDⓈ-M futures / aggTrades; 2024-03-01 .. 2024-11-30
inclusive UTC; 275 days; 400,001,695 rows) into a phase-scoped **pre-v002
label segment** of the existing v002 label family
``microstructure_labels_aggtrades_v001`` and writes:

- 275 per-day label Parquet files + canonical ``.sha256`` sidecars under
  ``data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w/BTCUSDT/<YYYY>/<MM>/``;
- one non-eligible label **segment** manifest + canonical sidecar under
  ``data/microstructure/manifests/``.

It reuses the locked Phase 4bm-O v002 label primitives unchanged
(``labels_schema_v002``, ``labels_compute_v002``, ``labels_io``) and adds
only bounded orchestration that implements the Phase 4bn-V selected
conventions:

- the **non-eligible-source precondition** (Phase 4bn-S feature segment
  manifest + Phase 4bn-T feature-layer gate PASS + Phase 4bn-O normalized
  segment manifest + Phase 4bn-P normalized-layer gate PASS), replacing
  the Phase 4bm-L Stage-5 research-use successor-state;
- the **segment-scoped ``label_config_hash``** builder
  ``build_label_config_hash_v002_pre_v002_segment`` (re-specified
  future-reference envelope clause; Phase 4bn-T / 4bn-P gate witnesses;
  ``feature_config_hash = 0726b41d…``, never ``819cfa7a…``);
- the **lineage re-mapping** of the two terminal-specific lineage columns
  (``source_phase_4bm_j_gate_report_sha256`` → Phase 4bn-T gate SHA;
  ``source_feature_successor_state_sha256`` → Phase 4bn-P gate SHA),
  recorded in the manifest ``lineage_column_reinterpretation`` block;
- the **pre-v002 envelope terminal** (max ``source_transact_time_ms`` /
  ``feature_timestamp_ms`` within 2024-11-30), so 1s/5s/15s/60s horizons
  crossing it censor and never read 2024-12-01+ or sealed-test rows;
- the segment output directory / manifest naming and the Phase 4bn-L
  budget caps.

Strict scope — this script does NOT and MUST NOT:

- run ML, score models, generate predictions, run diagnostics;
- run strategy / signals / PnL / backtests;
- create ``data/research`` outputs;
- create barrier / target-before-stop / stop / MFE / MAE / R-multiple /
  PnL-label semantics (the locked forbidden-substring guard is enforced);
- flip ``research_eligible`` or transition ``eligibility_gate_status``;
- create a chronological split policy;
- read the v002 terminal feature / normalized / raw window or any
  sealed-test date;
- read or mutate the published label / feature / normalized ``__v002``
  family;
- create v003, a database (``.duckdb`` / ``.sqlite``), or compact Parquet;
- acquire data, call endpoints, download archives, use credentials,
  ``.env``, ``.mcp.json``, MCP, Graphify, WebSocket, or private APIs;
- commit any artefact under ``data/microstructure`` or ``data/research``;
- authorize any successor.

The orchestrator is intentionally narrow: Python standard library plus
pyarrow plus the locked v002 label scaffold. No networking import is
present. All writes are atomic (temp + ``os.replace``), refuse to
overwrite finalised outputs, and are restricted to the gitignored
``data/microstructure/labels/`` and ``data/microstructure/manifests/``
namespaces. Any precondition / per-day / aggregate / budget breach fails
closed BEFORE the label segment manifest is written; partial per-day
label Parquets that may exist remain independently verifiable via their
sidecars and remain non-eligible / gitignored.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# Locked Phase 4bm-O v002 label primitives — reused verbatim, unchanged.
from prometheus.research.microstructure.labels_compute_v002 import (  # noqa: E402
    LabelComputationErrorV002,
    LabelLineageV002,
    LabelMultiDaySummaryV002,
    compute_aggtrade_labels_v002_for_day,
    load_normalized_day_ref,
    write_label_dataset_v002,
)
from prometheus.research.microstructure.labels_io import (  # noqa: E402
    LABEL_DATASET_FAMILY,
    LABELS_FAMILY_SUBDIR,
    assert_label_manifest_path_under_manifests,
    assert_label_path_under_data_microstructure,
    assert_output_path_under_labels,
    atomic_write_label_manifest,
    write_label_sha256_sidecar,
)
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
    assert_no_forbidden_label_substrings_v002,
)

# ---------------------------------------------------------------------------
# Locked identity / boundary constants (Phase 4bn-W prompt + Phase 4bn-V memo).
# ---------------------------------------------------------------------------

PHASE_ID = "4bn-W"
PHASE_ID_FULL = "phase-4bn-w"
PHASE_ID_TOKEN = "4bn_w"
SOURCE_PHASE_BOUNDARY = "4bn-T"

LABEL_FAMILY_ID = "microstructure_labels_aggtrades_v001"
LABEL_DATASET_VERSION = "v002"
VERSION = "v002"
LABEL_SCHEMA_VERSION = "v001"
SEGMENT_LABEL = "pre_v002_segment"
DATA_FAMILY = "aggTrades"
MARKET = "usdm_futures"
DATASET_CATEGORY = "labels"
SYMBOL = "BTCUSDT"

SOURCE_FEATURE_DATASET_FAMILY = "microstructure_features_aggtrades_v001"
SOURCE_FEATURE_DATASET_VERSION = "v002"
SOURCE_FEATURE_SCHEMA_VERSION = "FEATURE_SCHEMA_V002"
SOURCE_NORMALIZED_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
SOURCE_NORMALIZED_DATASET_VERSION = "v002"
SOURCE_NORMALIZED_SCHEMA_VERSION = "NORMALIZED_SCHEMA_V001"

# Segment output directory / manifest naming (distinct from published __v002).
SEGMENT_SUFFIX = f"{LABEL_DATASET_VERSION}_pre_v002_segment_{PHASE_ID_TOKEN}"
FAMILY_DIR_NAME = f"{LABEL_FAMILY_ID}__{SEGMENT_SUFFIX}"
SEGMENT_MANIFEST_BASENAME = f"{FAMILY_DIR_NAME}.json"

PUBLISHED_V002_LABEL_DIR_NAME = f"{LABEL_FAMILY_ID}__{LABEL_DATASET_VERSION}"
PUBLISHED_V002_LABEL_MANIFEST_REL = (
    f"data/microstructure/manifests/{LABEL_FAMILY_ID}__{LABEL_DATASET_VERSION}.json"
)

# Window contract.
EXPECTED_DATE_COUNT = 275
EXPECTED_DATE_START = "2024-03-01"
EXPECTED_DATE_END = "2024-11-30"
EXPECTED_TOTAL_ROW_COUNT = 400_001_695
FULL_ENVELOPE_START = "2024-03-01"
FULL_ENVELOPE_END = "2025-02-28"

# Reference-only v002 terminal / sealed-test boundaries (never read here).
V002_TERMINAL_START = "2024-12-01"
V002_TERMINAL_END = "2025-02-28"
SEALED_TEST_START = "2025-02-14"
SEALED_TEST_END = "2025-02-28"

# Default base SHA = Phase 4bn-V final main SHA (operator-pinned).
BASE_COMMIT_SHA_4BN_V_FINAL = "e53652a11e8586d26803aebb616a87fccd571353"

# Locked source-artefact SHA256s (Phase 4bn-V selected non-eligible-source set).
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
EXPECTED_RAW_SEGMENT_MANIFEST_SHA = (
    "1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1"
)
EXPECTED_FEATURE_CONFIG_HASH = (
    "0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c"
)
# Explicitly INVALID for this pre-v002 segment (published v002 feature lock).
PUBLISHED_V002_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)

# Default source/output relative paths.
DEFAULT_FEATURE_SEGMENT_MANIFEST_REL = (
    "data/microstructure/manifests/"
    "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json"
)
DEFAULT_FEATURE_GATE_REPORT_REL = (
    "data/microstructure/gate-reports/features/"
    "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s__"
    "phase-4bn-t__1780674917156__e647435c81d7.json"
)
DEFAULT_NORMALIZED_SEGMENT_MANIFEST_REL = (
    "data/microstructure/manifests/"
    "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json"
)
DEFAULT_NORMALIZED_GATE_REPORT_REL = (
    "data/microstructure/gate-reports/normalized/"
    "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o__"
    "phase-4bn-p__1780599605192__3fd795ceac4f.json"
)
DEFAULT_LABELS_ROOT_REL = "data/microstructure/labels"
DEFAULT_MANIFESTS_ROOT_REL = "data/microstructure/manifests"

# Per-row lineage re-mapping (Phase 4bn-V §17): the two terminal-specific
# columns carry the Phase 4bn admissibility witnesses for this segment.
#   source_phase_4bm_j_gate_report_sha256  -> Phase 4bn-T feature-layer gate
#   source_feature_successor_state_sha256  -> Phase 4bn-P normalized-layer gate
LINEAGE_REMAP_FEATURE_LAYER_GATE_KEY = "source_phase_4bm_j_gate_report_sha256"
LINEAGE_REMAP_NORMALIZED_LAYER_GATE_KEY = "source_feature_successor_state_sha256"

# ---------------------------------------------------------------------------
# Budget caps (Phase 4bn-L derived-stack storage-budget memo; LABEL layer).
# ---------------------------------------------------------------------------

GIB = 1024**3
LABEL_WARN_BYTES = 75 * GIB
LABEL_HARD_BYTES = 125 * GIB
RUNTIME_WARN_SECONDS = 4 * 3600
RUNTIME_HARD_SECONDS = 8 * 3600
TEMP_WARN_BYTES = 50 * GIB
TEMP_HARD_BYTES = 100 * GIB
TOTAL_STACK_WARN_BYTES = 250 * GIB
TOTAL_STACK_HARD_BYTES = 300 * GIB
D_FREE_FLOOR_BYTES = 500 * GIB  # preflight floor
D_FREE_MIN_BYTES = 350 * GIB  # in-execution floor

# Conservative per-row label footprint estimate (40 narrow columns, zstd).
PREFLIGHT_BYTES_PER_ROW = 160

# Existing local derived-stack footprint (Phase 4bn-O normalized + Phase 4bn-S
# feature segments) carried forward by reference for the total-stack estimate.
EXISTING_DERIVED_STACK_BYTES = 3_954_532_918 + 54_254_406_538

# ---------------------------------------------------------------------------
# Forbidden scope tokens / manifest field-name substrings (label-appropriate).
# ---------------------------------------------------------------------------

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

# Forbidden label-manifest field-name substrings. NOTE: ``label``, ``forward``,
# ``future``, ``ml``, ``strategy``, ``backtest``, ``diagnostics`` are NOT in
# this set because they legitimately appear in label identity / schema /
# policy / governance-declaration keys (e.g. ``label_config_hash``,
# ``future_reference_policy``, ``strategy_use``). The three explicitly
# validated declaration subtrees are not rescanned.
FORBIDDEN_MANIFEST_KEY_SUBSTRINGS: tuple[str, ...] = (
    "model",
    "prediction",
    "_score",
    "signal",
    "_entry",
    "_exit",
    "pnl",
    "equity",
    "profit",
    "_loss",
    "_position",
    "alpha",
    "_edge",
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
    "research_ready",
    "admissible",
    "approved_for_backtest",
)

_DECLARATION_SUBTREES = frozenset(
    {"governance_labels", "non_authorization_flags", "boundary_confirmations"}
)


# ---------------------------------------------------------------------------
# Result / error types
# ---------------------------------------------------------------------------


class Phase4bnWOrchestrationError(RuntimeError):
    """Raised when the Phase 4bn-W orchestrator fails closed."""


class Phase4bnWValidationError(Phase4bnWOrchestrationError):
    """Raised when a precondition / per-day / aggregate / budget check fails."""


@dataclass
class CheckResult:
    """One named check outcome."""

    check_id: str
    title: str
    status: str  # "pass" | "warn" | "fail"
    detail: str = ""


@dataclass
class PerDayLabelSource:
    """Resolved per-date feature + normalized source paths/SHAs for one day."""

    date: str
    symbol: str
    feature_parquet_path: Path
    feature_parquet_rel_path: str
    feature_parquet_sha256: str
    normalized_parquet_path: Path
    normalized_parquet_rel_path: str
    normalized_parquet_sha256: str
    row_count: int
    last_transact_time_ms: int


@dataclass
class PerDayLabelRecord:
    """Per-date label production record for the segment manifest inventory."""

    date: str
    symbol: str
    label_parquet_path: str
    label_parquet_sha256: str
    label_parquet_size_bytes: int
    row_count: int
    per_horizon_censored_counts: dict[str, int]
    invalid_price_row_count: int
    label_sidecar_path: str
    label_sidecar_sha256: str
    label_sidecar_size_bytes: int
    paired_source_feature_parquet_sha256: str
    paired_source_normalized_parquet_sha256: str
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


def _ms_to_utc_date(ms: int) -> str:
    """Return the UTC ``YYYY-MM-DD`` date of *ms* (epoch milliseconds)."""
    return datetime.fromtimestamp(ms / 1000, tz=UTC).strftime("%Y-%m-%d")


def _disk_free_bytes(path: Path) -> int:
    """Return free bytes on the filesystem hosting *path* (or nearest parent)."""
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
        raise Phase4bnWValidationError(f"date not YYYY-MM-DD: {date!r}")
    try:
        datetime.strptime(date, "%Y-%m-%d")  # reject malformed (e.g. 2024-13-40)
    except ValueError as exc:
        raise Phase4bnWValidationError(f"malformed date: {date!r}") from exc
    if date >= V002_TERMINAL_START:
        raise Phase4bnWValidationError(
            f"date {date} is in/after the v002 terminal window "
            f"(>= {V002_TERMINAL_START}); rejected"
        )
    if SEALED_TEST_START <= date <= SEALED_TEST_END:
        raise Phase4bnWValidationError(f"date {date} is a sealed-test date; rejected")
    if date < EXPECTED_DATE_START:
        raise Phase4bnWValidationError(
            f"date {date} is before segment start {EXPECTED_DATE_START}; rejected"
        )
    if date > EXPECTED_DATE_END:
        raise Phase4bnWValidationError(
            f"date {date} is after segment end {EXPECTED_DATE_END}; rejected"
        )


def _assert_symbol(symbol: str) -> None:
    """Fail closed on any symbol other than BTCUSDT."""
    if symbol != SYMBOL:
        raise Phase4bnWValidationError(
            f"symbol {symbol!r} rejected; only {SYMBOL} permitted"
        )


def _assert_no_forbidden_scope_tokens(text: str, *, where: str) -> None:
    """Fail closed if any forbidden scope token appears in *text*."""
    low = text.lower()
    for token in FORBIDDEN_SCOPE_TOKENS:
        if token in low:
            raise Phase4bnWValidationError(
                f"forbidden scope token {token!r} found in {where}"
            )


def _assert_segment_naming() -> None:
    """Fail closed if the segment directory/manifest collide with v003 / __v002."""
    if "v003" in FAMILY_DIR_NAME or "v003" in SEGMENT_MANIFEST_BASENAME:
        raise Phase4bnWValidationError("v003 token present in segment naming")
    if FAMILY_DIR_NAME == PUBLISHED_V002_LABEL_DIR_NAME:
        raise Phase4bnWValidationError(
            "segment family dir must differ from published __v002 label directory"
        )
    if f"{LABEL_FAMILY_ID}__{LABEL_DATASET_VERSION}.json" == SEGMENT_MANIFEST_BASENAME:
        raise Phase4bnWValidationError(
            "segment manifest must differ from published __v002 label manifest"
        )
    if LABEL_FAMILY_ID != LABEL_DATASET_FAMILY or LABEL_FAMILY_ID != LABEL_DATASET_FAMILY_V002:
        raise Phase4bnWValidationError("label family id drift")


def derive_label_segment_parquet_path(
    *, labels_root: Path, symbol: str, utc_date: str
) -> Path:
    """Compute the pre-v002 label segment Parquet path for ``(symbol, utc_date)``.

    Layout (relative to *labels_root*, which must resolve to
    ``data/microstructure/labels/``):
    ``<FAMILY_DIR_NAME>/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-labels-aggtrades-<YYYY-MM-DD>.parquet``.
    """
    assert_label_path_under_data_microstructure(labels_root, label="labels_root")
    if labels_root.name != LABELS_FAMILY_SUBDIR:
        raise Phase4bnWValidationError(
            f"labels_root must end in {LABELS_FAMILY_SUBDIR!r} (got {labels_root.name!r})"
        )
    if not symbol or not symbol.isalnum() or symbol != symbol.upper():
        raise Phase4bnWValidationError("symbol must be uppercase alphanumeric")
    parts = utc_date.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise Phase4bnWValidationError(f"utc_date must be YYYY-MM-DD; got {utc_date!r}")
    yyyy, mm, _dd = parts
    out = (
        labels_root
        / FAMILY_DIR_NAME
        / symbol
        / yyyy
        / mm
        / f"{symbol}-labels-aggtrades-{utc_date}.parquet"
    )
    assert_output_path_under_labels(out, label="pre-v002 label segment parquet path")
    stripped = out.as_posix().replace(FAMILY_DIR_NAME, "")
    if (
        f"{PUBLISHED_V002_LABEL_DIR_NAME}/" in stripped
        or f"/{LABEL_FAMILY_ID}/" in stripped
    ):
        raise Phase4bnWValidationError(
            "label output path must not resolve under the published __v002 / "
            "generic label directory"
        )
    return out


def _git_head_sha(repo_root: Path) -> str:
    """Return the current HEAD SHA by reading ``.git`` directly (no subprocess)."""
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


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Segment-scoped label_config_hash builder (Phase 4bn-V §16)
# ---------------------------------------------------------------------------

# The published v002 future-reference policy embeds the v002 90-day envelope
# clause; the pre-v002 segment must re-specify it to the segment terminal.
_V002_ENVELOPE_CLAUSE = (
    "envelope_terminal_unix_ms="
    "max_source_transact_time_ms_across_v002_90day_envelope"
)
_SEGMENT_ENVELOPE_CLAUSE = (
    "envelope_terminal_unix_ms="
    "max_source_transact_time_ms_across_pre_v002_segment_2024-03-01_to_2024-11-30"
)


def _segment_future_reference_policy() -> str:
    """Return the pre-v002-segment future-reference policy string.

    Identical to ``FUTURE_REFERENCE_POLICY_V002`` except the envelope clause
    is re-specified to the pre-v002 segment terminal. Fails closed if the
    locked v002 clause is absent (kernel drift).
    """
    if _V002_ENVELOPE_CLAUSE not in FUTURE_REFERENCE_POLICY_V002:
        raise Phase4bnWValidationError(
            "locked FUTURE_REFERENCE_POLICY_V002 envelope clause not found; kernel drift"
        )
    out = FUTURE_REFERENCE_POLICY_V002.replace(
        _V002_ENVELOPE_CLAUSE, _SEGMENT_ENVELOPE_CLAUSE
    )
    if out == FUTURE_REFERENCE_POLICY_V002 or _V002_ENVELOPE_CLAUSE in out:
        raise Phase4bnWValidationError(
            "segment future-reference policy did not re-specify the envelope clause"
        )
    return out


LABEL_CONFIG_HASH_INPUT_FIELDS: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "label_schema_version",
    "segment_label",
    "label_list",
    "support_column_list",
    "lineage_column_list",
    "horizon_list",
    "horizon_ms_list",
    "anchor_policy",
    "future_reference_policy_pre_v002_segment",
    "direction_threshold_policy",
    "null_censoring_policy",
    "dtype_policy",
    "source_feature_manifest_sha256",
    "source_feature_layer_gate_report_sha256",
    "source_normalized_manifest_sha256",
    "source_normalized_layer_gate_report_sha256",
    "source_raw_manifest_sha256",
    "feature_config_hash",
)


def build_label_config_hash_v002_pre_v002_segment(
    *,
    source_feature_manifest_sha256: str,
    source_feature_layer_gate_report_sha256: str,
    source_normalized_manifest_sha256: str,
    source_normalized_layer_gate_report_sha256: str,
    source_raw_manifest_sha256: str,
    feature_config_hash: str,
) -> str:
    """Return the deterministic segment-scoped ``label_config_hash``.

    Preserves the locked v002 label policy fields (anchor / direction /
    null-censoring / dtype + schema / horizon / lineage lists) but:

    - re-specifies the future-reference envelope clause to the pre-v002
      segment terminal (2024-03-01 .. 2024-11-30);
    - replaces the Stage-5 successor-state input with the Phase 4bn-T
      feature-layer gate and Phase 4bn-P normalized-layer gate witnesses;
    - binds the pre-v002 ``feature_config_hash`` (``0726b41d…``), never the
      published v002 lock (``819cfa7a…``);
    - adds a ``segment_label = "pre_v002_segment"`` discriminator.
    """
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
            raise Phase4bnWValidationError(f"{name} must be 64-char lowercase hex")
    if feature_config_hash == PUBLISHED_V002_FEATURE_CONFIG_HASH:
        raise Phase4bnWValidationError(
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
# Source artefact loading + non-eligible-source precondition enforcement
# ---------------------------------------------------------------------------


@dataclass
class SourceArtefactSet:
    """Resolved read-only inputs + pre-state SHAs for the non-eligible source."""

    feature_manifest_path: Path
    feature_manifest_sha_before: str
    feature_manifest_sidecar_sha_before: str
    feature_gate_report_path: Path
    feature_gate_report_sha_before: str
    normalized_manifest_path: Path
    normalized_manifest_sha_before: str
    normalized_manifest_sidecar_sha_before: str
    normalized_gate_report_path: Path
    normalized_gate_report_sha_before: str
    per_day_sources: list[PerDayLabelSource]
    envelope_terminal_unix_ms: int


def _verify_manifest_identity_and_posture(
    parsed: Mapping[str, Any], *, dataset_family: str, kind: str
) -> None:
    """Shared identity / non-eligible posture / window contract checks."""
    if parsed.get("symbol_list") != [SYMBOL]:
        raise Phase4bnWValidationError(f"{kind} manifest symbol_list != [{SYMBOL!r}]")
    if str(parsed.get("data_family", "")) != DATA_FAMILY:
        raise Phase4bnWValidationError(f"{kind} manifest data_family != {DATA_FAMILY}")
    if str(parsed.get("market", "")) != MARKET:
        raise Phase4bnWValidationError(f"{kind} manifest market != {MARKET}")
    if (
        parsed.get("dataset_family") != dataset_family
        or parsed.get("dataset_version") != "v002"
        or parsed.get("segment_label") != SEGMENT_LABEL
    ):
        raise Phase4bnWValidationError(f"{kind} manifest identity does not match")
    if parsed.get("research_eligible") is not False:
        raise Phase4bnWValidationError(f"{kind} manifest research_eligible must be false")
    if parsed.get("eligibility_gate_status") != "pending":
        raise Phase4bnWValidationError(
            f"{kind} manifest eligibility_gate_status must be 'pending'"
        )
    if parsed.get("v002_terminal_window_mode") != "by_reference":
        raise Phase4bnWValidationError(
            f"{kind} manifest v002_terminal_window_mode must be 'by_reference'"
        )
    if parsed.get("sealed_test_split_touched") is not False:
        raise Phase4bnWValidationError(
            f"{kind} manifest sealed_test_split_touched must be false"
        )
    if parsed.get("test_holdout_touched") is not False:
        raise Phase4bnWValidationError(
            f"{kind} manifest test_holdout_touched must be false"
        )
    if parsed.get("test_rows_loaded") != 0:
        raise Phase4bnWValidationError(f"{kind} manifest test_rows_loaded must be 0")
    if (
        parsed.get("date_start") != EXPECTED_DATE_START
        or parsed.get("date_end") != EXPECTED_DATE_END
        or parsed.get("date_count") != EXPECTED_DATE_COUNT
        or parsed.get("expected_file_count") != EXPECTED_DATE_COUNT
        or parsed.get("produced_file_count") != EXPECTED_DATE_COUNT
        or parsed.get("total_row_count") != EXPECTED_TOTAL_ROW_COUNT
    ):
        raise Phase4bnWValidationError(f"{kind} manifest window contract does not match")


def _verify_gate_report(
    *,
    gate_report_path: Path,
    expected_sha: str,
    required_verdict: str,
    expected_checks: int,
    manifest_link_field: str,
    expected_manifest_sha: str,
    kind: str,
) -> str:
    """Verify a Phase 4bn-P / 4bn-T gate report: SHA + PASS + flags. Return SHA."""
    if not gate_report_path.exists():
        raise Phase4bnWValidationError(f"{kind} gate report missing: {gate_report_path}")
    gate_sha, _ = _sha256_file(gate_report_path)
    if gate_sha != expected_sha:
        raise Phase4bnWValidationError(
            f"{kind} gate report SHA mismatch: got {gate_sha}, expected {expected_sha}"
        )
    gp = json.loads(gate_report_path.read_bytes().decode("utf-8"))
    if not isinstance(gp, dict):
        raise Phase4bnWValidationError(f"{kind} gate report is not a JSON object")
    if gp.get("overall_status") != "pass":
        raise Phase4bnWValidationError(f"{kind} gate report overall_status is not 'pass'")
    if gp.get("gate_result_state") != required_verdict:
        raise Phase4bnWValidationError(
            f"{kind} gate report gate_result_state is not the required PASS verdict"
        )
    if "PASS" not in str(gp.get("gate_verdict", "")):
        raise Phase4bnWValidationError(f"{kind} gate report verdict is not a PASS")
    gate_checks = gp.get("checks") or []
    n_pass = sum(1 for c in gate_checks if str(c.get("status")) == "pass")
    if len(gate_checks) != expected_checks or n_pass != expected_checks:
        raise Phase4bnWValidationError(
            f"{kind} gate report must record {expected_checks}/{expected_checks} PASS "
            f"(got {n_pass}/{len(gate_checks)})"
        )
    for flag, want in (
        ("segment_non_eligible", True),
        ("research_eligible_after", False),
        ("no_successor_authorization", True),
        ("v002_terminal_window_read", False),
        ("sealed_test_split_touched", False),
        ("published_v002_mutated", False),
        ("data_committed", False),
    ):
        if gp.get(flag) is not want:
            raise Phase4bnWValidationError(
                f"{kind} gate report {flag} must be {want} (got {gp.get(flag)!r})"
            )
    if gp.get("eligibility_gate_status_after") != "pending":
        raise Phase4bnWValidationError(
            f"{kind} gate report eligibility_gate_status_after must be 'pending'"
        )
    if gp.get(manifest_link_field) != expected_manifest_sha:
        raise Phase4bnWValidationError(
            f"{kind} gate report {manifest_link_field} does not match the segment manifest"
        )
    return gate_sha


def verify_preconditions(
    *,
    feature_manifest_path: Path,
    feature_gate_report_path: Path,
    normalized_manifest_path: Path,
    normalized_gate_report_path: Path,
    repo_root: Path,
    checks: list[CheckResult],
) -> SourceArtefactSet:
    """Verify all input preconditions; fail closed before any output is written."""
    _assert_segment_naming()
    data_root = repo_root / "data"

    # --- 1. feature segment manifest: SHA + sidecar + identity + posture ---
    if not feature_manifest_path.exists():
        raise Phase4bnWValidationError(
            f"feature segment manifest missing: {feature_manifest_path}"
        )
    feat_sha, _ = _sha256_file(feature_manifest_path)
    if feat_sha != EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA:
        raise Phase4bnWValidationError(
            f"feature segment manifest SHA mismatch: got {feat_sha}, "
            f"expected {EXPECTED_FEATURE_SEGMENT_MANIFEST_SHA}"
        )
    feat_parsed = json.loads(feature_manifest_path.read_bytes().decode("utf-8"))
    if not isinstance(feat_parsed, dict):
        raise Phase4bnWValidationError("feature segment manifest is not a JSON object")
    feat_sidecar_path = feature_manifest_path.with_suffix(
        feature_manifest_path.suffix + ".sha256"
    )
    if not feat_sidecar_path.exists():
        raise Phase4bnWValidationError(
            f"feature segment manifest sidecar missing: {feat_sidecar_path}"
        )
    feat_sidecar_sha, _ = _sha256_file(feat_sidecar_path)
    if feat_sidecar_sha != EXPECTED_FEATURE_SEGMENT_MANIFEST_SIDECAR_SHA:
        raise Phase4bnWValidationError(
            "feature segment manifest sidecar SHA mismatch"
        )
    if feat_sidecar_path.read_bytes() != (
        f"{feat_sha}  {feature_manifest_path.name}\n".encode("ascii")
    ):
        raise Phase4bnWValidationError(
            "feature segment manifest sidecar is not the canonical two-space body"
        )
    _verify_manifest_identity_and_posture(
        feat_parsed, dataset_family=SOURCE_FEATURE_DATASET_FAMILY, kind="feature"
    )
    if feat_parsed.get("feature_config_hash") != EXPECTED_FEATURE_CONFIG_HASH:
        raise Phase4bnWValidationError(
            f"feature segment manifest feature_config_hash must be "
            f"{EXPECTED_FEATURE_CONFIG_HASH} (got {feat_parsed.get('feature_config_hash')!r})"
        )
    if feat_parsed.get("feature_config_hash") == PUBLISHED_V002_FEATURE_CONFIG_HASH:
        raise Phase4bnWValidationError(
            "feature segment carries the published v002 feature_config_hash; rejected"
        )
    checks.append(
        CheckResult(
            "4bn-W.1",
            "feature segment manifest present + SHA + sidecar + posture + config hash",
            "pass",
            feat_sha,
        )
    )

    # --- 2. Phase 4bn-T feature-layer gate report: SHA + 27/27 PASS ---
    feat_gate_sha = _verify_gate_report(
        gate_report_path=feature_gate_report_path,
        expected_sha=EXPECTED_FEATURE_LAYER_GATE_REPORT_SHA,
        required_verdict=REQUIRED_FEATURE_GATE_VERDICT,
        expected_checks=27,
        manifest_link_field="input_feature_manifest_sha256",
        expected_manifest_sha=feat_sha,
        kind="feature-layer (4bn-T)",
    )
    checks.append(
        CheckResult(
            "4bn-W.2",
            "Phase 4bn-T feature-layer gate report present + SHA + 27/27 PASS",
            "pass",
            feat_gate_sha,
        )
    )

    # --- 3. normalized segment manifest: SHA + sidecar + identity + posture ---
    if not normalized_manifest_path.exists():
        raise Phase4bnWValidationError(
            f"normalized segment manifest missing: {normalized_manifest_path}"
        )
    norm_sha, _ = _sha256_file(normalized_manifest_path)
    if norm_sha != EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA:
        raise Phase4bnWValidationError(
            f"normalized segment manifest SHA mismatch: got {norm_sha}, "
            f"expected {EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA}"
        )
    norm_parsed = json.loads(normalized_manifest_path.read_bytes().decode("utf-8"))
    if not isinstance(norm_parsed, dict):
        raise Phase4bnWValidationError("normalized segment manifest is not a JSON object")
    norm_sidecar_path = normalized_manifest_path.with_suffix(
        normalized_manifest_path.suffix + ".sha256"
    )
    if not norm_sidecar_path.exists():
        raise Phase4bnWValidationError(
            f"normalized segment manifest sidecar missing: {norm_sidecar_path}"
        )
    norm_sidecar_sha, _ = _sha256_file(norm_sidecar_path)
    if norm_sidecar_sha != EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA:
        raise Phase4bnWValidationError("normalized segment manifest sidecar SHA mismatch")
    if norm_sidecar_path.read_bytes() != (
        f"{norm_sha}  {normalized_manifest_path.name}\n".encode("ascii")
    ):
        raise Phase4bnWValidationError(
            "normalized segment manifest sidecar is not the canonical two-space body"
        )
    _verify_manifest_identity_and_posture(
        norm_parsed, dataset_family=SOURCE_NORMALIZED_DATASET_FAMILY, kind="normalized"
    )
    checks.append(
        CheckResult(
            "4bn-W.3",
            "normalized segment manifest present + SHA + sidecar + posture",
            "pass",
            norm_sha,
        )
    )

    # --- 4. Phase 4bn-P normalized-layer gate report: SHA + 25/25 PASS ---
    norm_gate_sha = _verify_gate_report(
        gate_report_path=normalized_gate_report_path,
        expected_sha=EXPECTED_NORMALIZED_GATE_REPORT_SHA,
        required_verdict=REQUIRED_NORMALIZED_GATE_VERDICT,
        expected_checks=25,
        manifest_link_field="input_normalized_manifest_sha256",
        expected_manifest_sha=norm_sha,
        kind="normalized-layer (4bn-P)",
    )
    checks.append(
        CheckResult(
            "4bn-W.4",
            "Phase 4bn-P normalized-layer gate report present + SHA + 25/25 PASS",
            "pass",
            norm_gate_sha,
        )
    )

    # --- 5. build per-day sources from both inventories; cross-bind + verify ---
    feat_inv: list[dict[str, Any]] = list(feat_parsed.get("per_file_inventory", []))
    norm_inv: list[dict[str, Any]] = list(norm_parsed.get("per_file_inventory", []))
    if len(feat_inv) != EXPECTED_DATE_COUNT or len(norm_inv) != EXPECTED_DATE_COUNT:
        raise Phase4bnWValidationError("per_file_inventory length != 275")
    norm_by_date = {str(e["date"]): e for e in norm_inv}
    if len(norm_by_date) != EXPECTED_DATE_COUNT:
        raise Phase4bnWValidationError("normalized inventory has duplicate dates")

    per_day_sources: list[PerDayLabelSource] = []
    prev_date: str | None = None
    for entry in feat_inv:
        date = str(entry["date"])
        _assert_date_in_segment(date)
        _assert_symbol(str(entry["symbol"]))
        if prev_date is not None and date <= prev_date:
            raise Phase4bnWValidationError("feature inventory dates not strictly increasing")
        prev_date = date

        if date not in norm_by_date:
            raise Phase4bnWValidationError(f"normalized inventory missing date {date}")
        n_entry = norm_by_date[date]

        feat_rel = str(entry["feature_parquet_path"])
        norm_rel = str(entry["paired_source_normalized_parquet_path"])
        norm_rel2 = str(n_entry["local_parquet_path"])
        for rel, where in (
            (feat_rel, f"feature parquet path {date}"),
            (norm_rel, f"paired normalized parquet path {date}"),
        ):
            _assert_no_forbidden_scope_tokens(rel, where=where)
        if norm_rel != norm_rel2:
            raise Phase4bnWValidationError(
                f"feature paired normalized path != normalized inventory path for {date}"
            )
        # Cross-bind: feature's paired normalized SHA == normalized inventory SHA.
        if str(entry["paired_source_normalized_parquet_sha256"]) != str(
            n_entry["parquet_sha256"]
        ):
            raise Phase4bnWValidationError(
                f"paired normalized SHA mismatch between feature/normalized inventory ({date})"
            )
        # Reject any path resolving under a published __v002 family directory.
        for rel in (feat_rel, norm_rel):
            if (
                f"{SOURCE_FEATURE_DATASET_FAMILY}__{SOURCE_FEATURE_DATASET_VERSION}/" in rel
                or (
                    f"{SOURCE_NORMALIZED_DATASET_FAMILY}__"
                    f"{SOURCE_NORMALIZED_DATASET_VERSION}/"
                )
                in rel
                or f"{PUBLISHED_V002_LABEL_DIR_NAME}/" in rel
            ):
                raise Phase4bnWValidationError(
                    f"source path resolves under a published __v002 family: {rel}"
                )
        feat_path = data_root / feat_rel
        norm_path = data_root / norm_rel
        if not feat_path.exists():
            raise Phase4bnWValidationError(f"feature parquet missing for {date}: {feat_path}")
        if not norm_path.exists():
            raise Phase4bnWValidationError(
                f"normalized parquet missing for {date}: {norm_path}"
            )

        row_count = int(entry["row_count"])
        if row_count != int(n_entry["event_count"]):
            raise Phase4bnWValidationError(
                f"feature/normalized row count mismatch for {date}"
            )
        per_day_sources.append(
            PerDayLabelSource(
                date=date,
                symbol=SYMBOL,
                feature_parquet_path=feat_path,
                feature_parquet_rel_path=feat_rel,
                feature_parquet_sha256=str(entry["feature_parquet_sha256"]),
                normalized_parquet_path=norm_path,
                normalized_parquet_rel_path=norm_rel,
                normalized_parquet_sha256=str(n_entry["parquet_sha256"]),
                row_count=row_count,
                last_transact_time_ms=int(n_entry["last_transact_time_ms"]),
            )
        )

    if len(per_day_sources) != EXPECTED_DATE_COUNT:
        raise Phase4bnWValidationError("resolved per-day sources != 275")
    if per_day_sources[0].date != EXPECTED_DATE_START:
        raise Phase4bnWValidationError("first segment date != 2024-03-01")
    if per_day_sources[-1].date != EXPECTED_DATE_END:
        raise Phase4bnWValidationError("last segment date != 2024-11-30")
    if sum(s.row_count for s in per_day_sources) != EXPECTED_TOTAL_ROW_COUNT:
        raise Phase4bnWValidationError("total source row count != 400,001,695")

    # --- 6. envelope terminal = max normalized last_transact_time_ms; on 11-30 ---
    envelope_terminal = max(s.last_transact_time_ms for s in per_day_sources)
    term_date = _ms_to_utc_date(envelope_terminal)
    if term_date != EXPECTED_DATE_END:
        raise Phase4bnWValidationError(
            f"envelope terminal date {term_date} != {EXPECTED_DATE_END}"
        )
    if envelope_terminal != per_day_sources[-1].last_transact_time_ms:
        raise Phase4bnWValidationError(
            "envelope terminal is not the last day's last transact_time_ms"
        )
    checks.append(
        CheckResult(
            "4bn-W.5",
            "275 per-day feature+normalized sources resolved + cross-bound; "
            "envelope terminal on 2024-11-30",
            "pass",
            f"{len(per_day_sources)} days; terminal={envelope_terminal} ({term_date})",
        )
    )

    return SourceArtefactSet(
        feature_manifest_path=feature_manifest_path,
        feature_manifest_sha_before=feat_sha,
        feature_manifest_sidecar_sha_before=feat_sidecar_sha,
        feature_gate_report_path=feature_gate_report_path,
        feature_gate_report_sha_before=feat_gate_sha,
        normalized_manifest_path=normalized_manifest_path,
        normalized_manifest_sha_before=norm_sha,
        normalized_manifest_sidecar_sha_before=norm_sidecar_sha,
        normalized_gate_report_path=normalized_gate_report_path,
        normalized_gate_report_sha_before=norm_gate_sha,
        per_day_sources=per_day_sources,
        envelope_terminal_unix_ms=envelope_terminal,
    )


# ---------------------------------------------------------------------------
# Preflight budget estimation (Phase 4bn-L; LABEL layer)
# ---------------------------------------------------------------------------


@dataclass
class PreflightEstimate:
    """Preflight footprint / runtime / free-space estimate."""

    d_free_bytes: int
    estimated_label_bytes: int
    estimated_temp_bytes: int
    estimated_total_stack_bytes: int


def run_preflight(
    *,
    artefacts: SourceArtefactSet,
    labels_root: Path,
    checks: list[CheckResult],
) -> PreflightEstimate:
    """Estimate footprints + check Phase 4bn-L caps + D: floor before writing."""
    total_rows = sum(s.row_count for s in artefacts.per_day_sources)
    max_day_rows = max(s.row_count for s in artefacts.per_day_sources)

    est_label = total_rows * PREFLIGHT_BYTES_PER_ROW
    est_temp = max_day_rows * PREFLIGHT_BYTES_PER_ROW
    est_total = EXISTING_DERIVED_STACK_BYTES + est_label + est_temp
    if est_label <= 0:
        raise Phase4bnWValidationError("preflight cannot estimate label output footprint")

    d_free = _disk_free_bytes(labels_root)
    if d_free < D_FREE_FLOOR_BYTES:
        raise Phase4bnWValidationError(
            f"D: free space {d_free / GIB:.1f} GiB below preflight floor "
            f"{D_FREE_FLOOR_BYTES / GIB:.0f} GiB"
        )
    if est_label > LABEL_HARD_BYTES:
        raise Phase4bnWValidationError(
            f"preflight label estimate {est_label / GIB:.1f} GiB exceeds hard cap "
            f"{LABEL_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_temp > TEMP_HARD_BYTES:
        raise Phase4bnWValidationError(
            f"preflight temp estimate {est_temp / GIB:.1f} GiB exceeds hard cap "
            f"{TEMP_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_total > TOTAL_STACK_HARD_BYTES:
        raise Phase4bnWValidationError(
            f"preflight total derived-stack estimate {est_total / GIB:.1f} GiB exceeds "
            f"hard cap {TOTAL_STACK_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_label > LABEL_WARN_BYTES:
        checks.append(
            CheckResult(
                "4bn-W.preflight.warn",
                "label footprint estimate above warning threshold",
                "warn",
                f"{est_label / GIB:.1f} GiB",
            )
        )
    if est_total > TOTAL_STACK_WARN_BYTES:
        checks.append(
            CheckResult(
                "4bn-W.preflight.stack.warn",
                "total derived-stack estimate above warning threshold",
                "warn",
                f"{est_total / GIB:.1f} GiB",
            )
        )
    checks.append(
        CheckResult(
            "4bn-W.preflight",
            "preflight footprint/free-space within Phase 4bn-L caps",
            "pass",
            f"est_label={est_label / GIB:.2f} GiB; "
            f"est_total_stack={est_total / GIB:.2f} GiB; D_free={d_free / GIB:.0f} GiB",
        )
    )
    return PreflightEstimate(
        d_free_bytes=d_free,
        estimated_label_bytes=est_label,
        estimated_temp_bytes=est_temp,
        estimated_total_stack_bytes=est_total,
    )


# ---------------------------------------------------------------------------
# Per-day label computation
# ---------------------------------------------------------------------------


def _read_feature_anchor_table(parquet_path: Path) -> Any:
    """Read only the four anchor columns from a feature Parquet."""
    import pyarrow.parquet as pq

    return pq.read_table(
        parquet_path,
        columns=[
            "row_index",
            "agg_trade_id",
            "feature_timestamp_ms",
            "source_transact_time_ms",
        ],
    )


def _compute_one_day(
    *,
    day: PerDayLabelSource,
    current_ref: Any,
    next_ref: Any,
    envelope_terminal_unix_ms: int,
    labels_root: Path,
    lineage_const: Mapping[str, str],
    repo_root: Path,
) -> tuple[PerDayLabelRecord, int]:
    """Compute one day's pre-v002 label Parquet + sidecar; return its record."""
    # Hash-verify the source parquets before compute (fail closed on drift).
    feat_sha, _ = _sha256_file(day.feature_parquet_path)
    if feat_sha != day.feature_parquet_sha256:
        raise Phase4bnWValidationError(
            f"feature parquet SHA mismatch for {day.date}: got {feat_sha}, "
            f"expected {day.feature_parquet_sha256}"
        )
    norm_sha, _ = _sha256_file(day.normalized_parquet_path)
    if norm_sha != day.normalized_parquet_sha256:
        raise Phase4bnWValidationError(
            f"normalized parquet SHA mismatch for {day.date}: got {norm_sha}, "
            f"expected {day.normalized_parquet_sha256}"
        )

    feature_table = _read_feature_anchor_table(day.feature_parquet_path)
    if feature_table.num_rows != day.row_count:
        raise Phase4bnWValidationError(
            f"feature row count mismatch for {day.date}: "
            f"parquet={feature_table.num_rows} manifest={day.row_count}"
        )
    if current_ref.utc_date != day.date:
        raise Phase4bnWValidationError(
            f"current_ref date {current_ref.utc_date} != {day.date}"
        )

    lineage = LabelLineageV002(
        source_feature_manifest_sha256=lineage_const["feature_manifest_sha256"],
        source_feature_parquet_sha256=day.feature_parquet_sha256,
        # Phase 4bn-V §17 re-map: successor-state slot -> Phase 4bn-P gate SHA.
        source_feature_successor_state_sha256=lineage_const["normalized_gate_sha256"],
        # Phase 4bn-V §17 re-map: Phase 4bm-J slot -> Phase 4bn-T gate SHA.
        source_phase_4bm_j_gate_report_sha256=lineage_const["feature_gate_sha256"],
        source_normalized_manifest_sha256=lineage_const["normalized_manifest_sha256"],
        source_raw_manifest_sha256=lineage_const["raw_manifest_sha256"],
        label_config_hash=lineage_const["label_config_hash"],
    )
    table, summary = compute_aggtrade_labels_v002_for_day(
        feature_table=feature_table,
        current_day=current_ref,
        next_day=next_ref,
        envelope_terminal_unix_ms=envelope_terminal_unix_ms,
        symbol=SYMBOL,
        utc_date=day.date,
        lineage=lineage,
    )
    out_path = derive_label_segment_parquet_path(
        labels_root=labels_root, symbol=SYMBOL, utc_date=day.date
    )
    (
        _written_path,
        parquet_sha,
        parquet_size,
        sidecar_path,
        sidecar_sha,
    ) = write_label_dataset_v002(
        table=table, output_path=out_path, write_sha256_sidecar=True
    )
    if sidecar_path is None or sidecar_sha is None:
        raise Phase4bnWValidationError(f"label sidecar not written for {day.date}")
    sidecar_size = sidecar_path.stat().st_size

    data_root = repo_root / "data"
    rel_parquet = out_path.resolve().relative_to(data_root.resolve()).as_posix()
    rel_sidecar = sidecar_path.resolve().relative_to(data_root.resolve()).as_posix()
    record = PerDayLabelRecord(
        date=day.date,
        symbol=SYMBOL,
        label_parquet_path=rel_parquet,
        label_parquet_sha256=parquet_sha,
        label_parquet_size_bytes=parquet_size,
        row_count=summary.row_count,
        per_horizon_censored_counts=dict(summary.censored_per_horizon),
        invalid_price_row_count=summary.invalid_price_row_count,
        label_sidecar_path=rel_sidecar,
        label_sidecar_sha256=sidecar_sha,
        label_sidecar_size_bytes=sidecar_size,
        paired_source_feature_parquet_sha256=day.feature_parquet_sha256,
        paired_source_normalized_parquet_sha256=day.normalized_parquet_sha256,
        status="produced_verified",
    )
    if summary.row_count != day.row_count:
        raise Phase4bnWValidationError(
            f"label row count {summary.row_count} != source row count {day.row_count} "
            f"for {day.date}"
        )
    return record, parquet_size + sidecar_size


def _enforce_budgets(
    *,
    running_label_bytes: int,
    elapsed: float,
    d_free: int,
    temp_peak: int,
    warnings_crossed: list[str],
) -> None:
    """Fail closed on any hard cap; record warning crossings."""
    if running_label_bytes > LABEL_HARD_BYTES:
        raise Phase4bnWValidationError(
            f"label footprint {running_label_bytes / GIB:.1f} GiB exceeds hard cap"
        )
    if elapsed > RUNTIME_HARD_SECONDS:
        raise Phase4bnWValidationError(
            f"runtime {elapsed:.0f}s exceeds hard cap {RUNTIME_HARD_SECONDS}s"
        )
    if d_free < D_FREE_MIN_BYTES:
        raise Phase4bnWValidationError(
            f"D: free {d_free / GIB:.1f} GiB fell below in-execution floor "
            f"{D_FREE_MIN_BYTES / GIB:.0f} GiB"
        )
    if temp_peak > TEMP_HARD_BYTES:
        raise Phase4bnWValidationError(
            f"temporary workspace {temp_peak / GIB:.1f} GiB exceeds hard cap"
        )
    if running_label_bytes > LABEL_WARN_BYTES and "label_warn" not in warnings_crossed:
        warnings_crossed.append("label_warn")
    if elapsed > RUNTIME_WARN_SECONDS and "runtime_warn" not in warnings_crossed:
        warnings_crossed.append("runtime_warn")
    if temp_peak > TEMP_WARN_BYTES and "temp_warn" not in warnings_crossed:
        warnings_crossed.append("temp_warn")


# ---------------------------------------------------------------------------
# Segment manifest builder + field contract
# ---------------------------------------------------------------------------


def build_segment_manifest(
    *,
    artefacts: SourceArtefactSet,
    per_day_records: Sequence[PerDayLabelRecord],
    aggregate: LabelMultiDaySummaryV002,
    base_commit_sha: str,
    code_commit_sha: str,
    label_config_hash: str,
    created_at_unix_ms: int,
    created_at_utc: str,
    total_label_footprint_bytes: int,
    total_label_row_count: int,
    budget_witnesses: Mapping[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    """Construct the Phase 4bn-W pre-v002 label segment manifest dict."""

    def _rel_to_repo(p: Path) -> str:
        return str(p.resolve().relative_to(repo_root.resolve())).replace(os.sep, "/")

    date_list = [r.date for r in per_day_records]
    inventory_entries: list[dict[str, Any]] = [
        {
            "date": r.date,
            "symbol": r.symbol,
            "label_parquet_path": r.label_parquet_path,
            "label_parquet_sha256": r.label_parquet_sha256,
            "label_parquet_size_bytes": r.label_parquet_size_bytes,
            "row_count": r.row_count,
            "per_horizon_censored_counts": r.per_horizon_censored_counts,
            "invalid_price_row_count": r.invalid_price_row_count,
            "label_sidecar_path": r.label_sidecar_path,
            "label_sidecar_sha256": r.label_sidecar_sha256,
            "label_sidecar_size_bytes": r.label_sidecar_size_bytes,
            "paired_source_feature_parquet_sha256": (
                r.paired_source_feature_parquet_sha256
            ),
            "paired_source_normalized_parquet_sha256": (
                r.paired_source_normalized_parquet_sha256
            ),
            "status": r.status,
        }
        for r in per_day_records
    ]

    governance_labels: dict[str, str] = {
        "phase": PHASE_ID,
        "phase_id": PHASE_ID_FULL,
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "label_computation": "performed_pre_v002_segment_non_eligible_by_phase_4bn_w",
        "labels": "allowed_by_future_phase_only",
        "targets": "allowed_by_future_phase_only",
        "ml": "forbidden",
        "diagnostics": "forbidden",
        "strategy": "forbidden",
        "backtest": "forbidden",
        "acquisition": "unauthorized",
        "paper_shadow_live": "forbidden",
        "deployment": "forbidden",
        "exchange_write": "forbidden",
        "research_use": "forbidden",
        "segment": "true",
    }
    non_authorization_flags: dict[str, bool] = {
        "diagnostics_authorized": False,
        "ml_authorized": False,
        "strategy_authorized": False,
        "backtest_authorized": False,
        "acquisition_authorized": False,
        "successor_authorization_after": False,
        "stage_5_label_cleared": False,
        "label_family_research_use_authorized": False,
    }
    boundary_confirmations: dict[str, bool] = {
        "no_ml": True,
        "no_diagnostics": True,
        "no_strategy": True,
        "no_backtest": True,
        "no_acquisition": True,
        "no_network": True,
        "no_credentials": True,
        "no_mcp_or_graphify": True,
        "no_future_lookahead_beyond_envelope_terminal": True,
        "no_v002_terminal_read": True,
        "no_sealed_test_read": True,
        "no_published_v002_label_mutation": True,
        "no_database_or_parquet_compaction": True,
        "no_v003": True,
        "no_data_research_output": True,
        "phase_4aw_flip_research_eligible_invariant_preserved": True,
    }

    return {
        # Identity / family.
        "dataset_family": LABEL_FAMILY_ID,
        "dataset_version": LABEL_DATASET_VERSION,
        "version": VERSION,
        "label_schema_version": LABEL_SCHEMA_VERSION,
        "segment_label": SEGMENT_LABEL,
        "data_family": DATA_FAMILY,
        "symbol": SYMBOL,
        "symbol_list": [SYMBOL],
        "market": MARKET,
        "dataset_category": DATASET_CATEGORY,
        "label_family_id": LABEL_FAMILY_ID,
        # Segment / phase / provenance.
        "phase": PHASE_ID,
        "phase_id": PHASE_ID_FULL,
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "created_at_unix_ms": created_at_unix_ms,
        "created_at_utc": created_at_utc,
        "code_commit_sha": code_commit_sha,
        "base_commit_sha": base_commit_sha,
        # Label schema.
        "column_count": len(LABEL_SCHEMA_V002),
        "lineage_column_count": len(LABEL_LINEAGE_COLUMNS_V002),
        "label_column_count": len(LABEL_NAMES_V002),
        "support_column_count": len(LABEL_SUPPORT_COLUMN_NAMES_V002),
        "schema_column_list": list(LABEL_SCHEMA_V002),
        "lineage_column_list": list(LABEL_LINEAGE_COLUMNS_V002),
        "label_list": list(LABEL_NAMES_V002),
        "support_column_list": list(LABEL_SUPPORT_COLUMN_NAMES_V002),
        # Label kernel policy.
        "dtype_policy": DTYPE_POLICY_V002,
        "anchor_policy": ANCHOR_POLICY_V002,
        "future_reference_policy": _segment_future_reference_policy(),
        "direction_threshold_policy": DIRECTION_THRESHOLD_POLICY_V002,
        "null_censoring_policy": NULL_CENSORING_POLICY_V002,
        "horizon_list": list(LABEL_HORIZONS_V002),
        "horizon_ms_list": list(LABEL_HORIZON_MS_V002),
        "forbidden_label_column_substrings": list(FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002),
        # Config hash + lineage re-mapping.
        "label_config_hash": label_config_hash,
        "label_config_hash_input_fields": list(LABEL_CONFIG_HASH_INPUT_FIELDS),
        "feature_config_hash": EXPECTED_FEATURE_CONFIG_HASH,
        "lineage_column_reinterpretation": {
            LINEAGE_REMAP_FEATURE_LAYER_GATE_KEY: {
                "segment_meaning": "feature_layer_gate_report",
                "bound_artefact": "phase_4bn_t_feature_layer_gate_report",
                "value": artefacts.feature_gate_report_sha_before,
            },
            LINEAGE_REMAP_NORMALIZED_LAYER_GATE_KEY: {
                "segment_meaning": "non_eligible_admissibility_witness",
                "bound_artefact": "phase_4bn_p_normalized_layer_gate_report",
                "value": artefacts.normalized_gate_report_sha_before,
                "note": (
                    "no Stage-5 research-use successor-state exists or is required "
                    "for this non-eligible pre-v002 segment"
                ),
            },
        },
        # Window / inventory.
        "date_start": EXPECTED_DATE_START,
        "date_end": EXPECTED_DATE_END,
        "date_count": EXPECTED_DATE_COUNT,
        "date_list": date_list,
        "expected_file_count": EXPECTED_DATE_COUNT,
        "produced_file_count": len(per_day_records),
        "total_row_count": total_label_row_count,
        "total_footprint_bytes": total_label_footprint_bytes,
        "per_day_outputs": inventory_entries,
        # Censoring aggregates.
        "envelope_terminal_unix_ms": artefacts.envelope_terminal_unix_ms,
        "envelope_terminal_utc_date": EXPECTED_DATE_END,
        "censored_per_horizon": dict(aggregate.censored_per_horizon),
        "invalid_price_row_count": aggregate.total_invalid_price_row_count,
        # Non-eligible-source lineage (Phase 4bn-V §15).
        "source_feature_dataset_family": SOURCE_FEATURE_DATASET_FAMILY,
        "source_feature_dataset_version": SOURCE_FEATURE_DATASET_VERSION,
        "source_feature_segment_manifest_path": _rel_to_repo(
            artefacts.feature_manifest_path
        ),
        "source_feature_segment_manifest_sha256": artefacts.feature_manifest_sha_before,
        "source_feature_segment_manifest_sidecar_sha256": (
            artefacts.feature_manifest_sidecar_sha_before
        ),
        "source_feature_layer_gate_report_path": _rel_to_repo(
            artefacts.feature_gate_report_path
        ),
        "source_feature_layer_gate_report_sha256": (
            artefacts.feature_gate_report_sha_before
        ),
        "source_normalized_dataset_family": SOURCE_NORMALIZED_DATASET_FAMILY,
        "source_normalized_dataset_version": SOURCE_NORMALIZED_DATASET_VERSION,
        "source_normalized_segment_manifest_path": _rel_to_repo(
            artefacts.normalized_manifest_path
        ),
        "source_normalized_segment_manifest_sha256": (
            artefacts.normalized_manifest_sha_before
        ),
        "source_normalized_segment_manifest_sidecar_sha256": (
            artefacts.normalized_manifest_sidecar_sha_before
        ),
        "source_normalized_layer_gate_report_path": _rel_to_repo(
            artefacts.normalized_gate_report_path
        ),
        "source_normalized_layer_gate_report_sha256": (
            artefacts.normalized_gate_report_sha_before
        ),
        "source_raw_segment_manifest_path": (
            "data/microstructure/manifests/"
            "microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json"
        ),
        "source_raw_segment_manifest_sha256": EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
        "source_feature_schema_version": SOURCE_FEATURE_SCHEMA_VERSION,
        "source_normalized_schema_version": SOURCE_NORMALIZED_SCHEMA_VERSION,
        "source_eligibility_posture": "non_eligible_gate_passed_pending",
        # Published v002 label family by reference only (never read/mutated).
        "existing_v002_label_reference": {
            "path": PUBLISHED_V002_LABEL_MANIFEST_REL,
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
        "chronological_split_policy": "not_yet_defined",
        "governance_labels": governance_labels,
        "no_successor_authorization": True,
        "boundary_confirmations": boundary_confirmations,
        "non_authorization_flags": non_authorization_flags,
        # Sealed-test / terminal boundary witnesses.
        "v002_terminal_window_mode": "by_reference",
        "existing_v002_terminal_window": {
            "start": V002_TERMINAL_START,
            "end": V002_TERMINAL_END,
            "read": False,
            "feature_normalized_raw_dates_read": False,
        },
        "sealed_test_split_touched": False,
        "existing_v002_sealed_test_split": {
            "start": SEALED_TEST_START,
            "end": SEALED_TEST_END,
            "touched": False,
        },
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        # Label posture.
        "label_computation": "non_eligible_pre_v002_segment",
        "ml_use": "forbidden",
        "diagnostics_use": "forbidden",
        "strategy_use": "forbidden",
        "backtest_use": "forbidden",
        # Partitioning / storage.
        "partitioning_rule": "<SYMBOL>/<YYYY>/<MM>/",
        "primary_key": ["symbol", "utc_date", "agg_trade_id", "row_index"],
        "storage_format": "parquet_zstd",
        "sidecar_policy": "canonical_two_space_sha256",
        # Budget witnesses (Phase 4bn-L).
        "budget_witnesses": dict(budget_witnesses),
    }


REQUIRED_MANIFEST_KEYS: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "version",
    "label_schema_version",
    "segment_label",
    "data_family",
    "symbol",
    "market",
    "dataset_category",
    "label_family_id",
    "phase_id",
    "source_phase_boundary",
    "created_at_unix_ms",
    "created_at_utc",
    "code_commit_sha",
    "base_commit_sha",
    "column_count",
    "lineage_column_count",
    "label_column_count",
    "support_column_count",
    "schema_column_list",
    "lineage_column_list",
    "label_list",
    "support_column_list",
    "dtype_policy",
    "anchor_policy",
    "future_reference_policy",
    "direction_threshold_policy",
    "null_censoring_policy",
    "horizon_list",
    "horizon_ms_list",
    "forbidden_label_column_substrings",
    "label_config_hash",
    "label_config_hash_input_fields",
    "feature_config_hash",
    "lineage_column_reinterpretation",
    "date_start",
    "date_end",
    "date_count",
    "date_list",
    "expected_file_count",
    "produced_file_count",
    "total_row_count",
    "total_footprint_bytes",
    "per_day_outputs",
    "envelope_terminal_unix_ms",
    "envelope_terminal_utc_date",
    "censored_per_horizon",
    "invalid_price_row_count",
    "source_feature_segment_manifest_path",
    "source_feature_segment_manifest_sha256",
    "source_feature_layer_gate_report_path",
    "source_feature_layer_gate_report_sha256",
    "source_normalized_segment_manifest_path",
    "source_normalized_segment_manifest_sha256",
    "source_normalized_layer_gate_report_path",
    "source_normalized_layer_gate_report_sha256",
    "source_raw_segment_manifest_path",
    "source_raw_segment_manifest_sha256",
    "source_feature_schema_version",
    "source_normalized_schema_version",
    "source_eligibility_posture",
    "existing_v002_label_reference",
    "full_intended_envelope_start",
    "full_intended_envelope_end",
    "research_eligible",
    "eligibility_gate_status",
    "chronological_split_policy",
    "governance_labels",
    "no_successor_authorization",
    "boundary_confirmations",
    "non_authorization_flags",
    "v002_terminal_window_mode",
    "existing_v002_terminal_window",
    "sealed_test_split_touched",
    "existing_v002_sealed_test_split",
    "test_holdout_touched",
    "test_rows_loaded",
    "label_computation",
    "ml_use",
    "diagnostics_use",
    "strategy_use",
    "backtest_use",
    "partitioning_rule",
    "primary_key",
    "storage_format",
    "sidecar_policy",
    "budget_witnesses",
)


def assert_manifest_field_contract(manifest: Mapping[str, Any]) -> None:
    """Fail closed if the label segment manifest violates the field contract."""
    missing = [k for k in REQUIRED_MANIFEST_KEYS if k not in manifest]
    if missing:
        raise Phase4bnWValidationError(f"label segment manifest missing keys: {missing}")

    if manifest["dataset_family"] != LABEL_FAMILY_ID:
        raise Phase4bnWValidationError("manifest dataset_family must be the v002 label family")
    if manifest["dataset_version"] != "v002" or manifest["version"] != "v002":
        raise Phase4bnWValidationError("manifest dataset_version/version must be 'v002'")
    if manifest["label_schema_version"] != "v001":
        raise Phase4bnWValidationError("manifest label_schema_version must be 'v001'")
    if manifest["segment_label"] != SEGMENT_LABEL:
        raise Phase4bnWValidationError("manifest segment_label must be 'pre_v002_segment'")
    if manifest["column_count"] != 40:
        raise Phase4bnWValidationError("manifest column_count must be 40")
    if manifest["lineage_column_count"] != 17:
        raise Phase4bnWValidationError("manifest lineage_column_count must be 17")
    if manifest["label_column_count"] != 8:
        raise Phase4bnWValidationError("manifest label_column_count must be 8")
    if manifest["support_column_count"] != 14:
        raise Phase4bnWValidationError("manifest support_column_count must be 14")
    if tuple(manifest["schema_column_list"]) != LABEL_SCHEMA_V002:
        raise Phase4bnWValidationError("manifest schema_column_list != LABEL_SCHEMA_V002")
    if manifest["feature_config_hash"] != EXPECTED_FEATURE_CONFIG_HASH:
        raise Phase4bnWValidationError("manifest feature_config_hash must be 0726b41d…")
    if manifest["feature_config_hash"] == PUBLISHED_V002_FEATURE_CONFIG_HASH:
        raise Phase4bnWValidationError("manifest must not bind the published v002 config hash")
    if manifest["horizon_list"] != list(LABEL_HORIZONS_V002):
        raise Phase4bnWValidationError("manifest horizon_list must be 1s/5s/15s/60s")
    if manifest["horizon_ms_list"] != list(LABEL_HORIZON_MS_V002):
        raise Phase4bnWValidationError("manifest horizon_ms_list must be 1000/5000/15000/60000")
    if manifest["envelope_terminal_utc_date"] != EXPECTED_DATE_END:
        raise Phase4bnWValidationError("manifest envelope_terminal_utc_date must be 2024-11-30")
    if _ms_to_utc_date(int(manifest["envelope_terminal_unix_ms"])) != EXPECTED_DATE_END:
        raise Phase4bnWValidationError("manifest envelope terminal not on 2024-11-30")

    # Non-eligible posture.
    if manifest["research_eligible"] is not False:
        raise Phase4bnWValidationError("manifest research_eligible must be False")
    if manifest["eligibility_gate_status"] != "pending":
        raise Phase4bnWValidationError("manifest eligibility_gate_status must be 'pending'")
    if manifest["chronological_split_policy"] != "not_yet_defined":
        raise Phase4bnWValidationError(
            "manifest chronological_split_policy must be 'not_yet_defined'"
        )
    if manifest["no_successor_authorization"] is not True:
        raise Phase4bnWValidationError("manifest no_successor_authorization must be True")
    if manifest["source_eligibility_posture"] != "non_eligible_gate_passed_pending":
        raise Phase4bnWValidationError("manifest source_eligibility_posture invalid")
    if manifest["v002_terminal_window_mode"] != "by_reference":
        raise Phase4bnWValidationError("manifest v002_terminal_window_mode must be 'by_reference'")
    for key in ("ml_use", "diagnostics_use", "strategy_use", "backtest_use"):
        if manifest[key] != "forbidden":
            raise Phase4bnWValidationError(f"manifest {key} must be 'forbidden'")
    if manifest["label_computation"] != "non_eligible_pre_v002_segment":
        raise Phase4bnWValidationError("manifest label_computation invalid")

    gov = manifest["governance_labels"]
    for key in ("ml", "strategy", "backtest", "diagnostics"):
        if gov.get(key) != "forbidden":
            raise Phase4bnWValidationError(f"governance label {key!r} must be 'forbidden'")
    if gov.get("acquisition") != "unauthorized":
        raise Phase4bnWValidationError("governance label 'acquisition' must be 'unauthorized'")
    if gov.get("labels") != "allowed_by_future_phase_only":
        raise Phase4bnWValidationError("governance label 'labels' must be future-phase-only")

    na = manifest["non_authorization_flags"]
    if any(na.values()):
        raise Phase4bnWValidationError("all non_authorization_flags must be False")
    for req in ("successor_authorization_after", "ml_authorized", "stage_5_label_cleared"):
        if req not in na:
            raise Phase4bnWValidationError(f"non_authorization_flags missing {req}")
    bc = manifest["boundary_confirmations"]
    if not all(bc.values()):
        raise Phase4bnWValidationError("all boundary_confirmations must be True")
    if "phase_4aw_flip_research_eligible_invariant_preserved" not in bc:
        raise Phase4bnWValidationError("boundary_confirmations missing 4aw invariant key")

    ref = manifest["existing_v002_label_reference"]
    if ref.get("read") is not False or ref.get("mutated") is not False:
        raise Phase4bnWValidationError("existing_v002_label_reference must be read/mutated False")
    term = manifest["existing_v002_terminal_window"]
    if (
        term.get("read") is not False
        or term.get("feature_normalized_raw_dates_read") is not False
    ):
        raise Phase4bnWValidationError("existing_v002_terminal_window must be read False")
    if manifest["sealed_test_split_touched"] is not False:
        raise Phase4bnWValidationError("sealed_test_split_touched must be False")
    if manifest["test_rows_loaded"] != 0 or manifest["test_holdout_touched"] is not False:
        raise Phase4bnWValidationError("test holdout must be untouched (rows_loaded=0)")

    # Forbidden field-name scan (recursive over keys). Declaration subtrees
    # (governance / non_authorization / boundary_confirmations) are not rescanned.
    def _scan(obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                low = str(k).lower()
                for needle in FORBIDDEN_MANIFEST_KEY_SUBSTRINGS:
                    if needle in low:
                        raise Phase4bnWValidationError(
                            f"forbidden manifest field substring {needle!r} in key {k!r}"
                        )
                if k in _DECLARATION_SUBTREES:
                    continue
                _scan(v)
        elif isinstance(obj, list):
            for item in obj:
                _scan(item)

    _scan(manifest)


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------


@dataclass
class OrchestrationResult:
    """Top-level result of one Phase 4bn-W label execution run."""

    overall_status: str  # "pass" | "fail_closed"
    output_manifest_path: Path | None
    output_manifest_sha256: str | None
    output_manifest_sidecar_path: Path | None
    output_manifest_sidecar_sha256: str | None
    produced_file_count: int
    total_label_row_count: int
    total_label_footprint_bytes: int
    label_config_hash: str | None
    envelope_terminal_unix_ms: int | None
    per_day_records: list[PerDayLabelRecord]
    aggregate: LabelMultiDaySummaryV002
    checks: list[CheckResult]
    budget_witnesses: Mapping[str, Any]
    wall_clock_seconds: float
    warning_thresholds_crossed: list[str]
    hard_caps_crossed: bool
    failed_check_id: str | None = None
    failure_message: str | None = None
    result_state: str = ""


def run(
    *,
    feature_manifest_path: Path,
    feature_gate_report_path: Path,
    normalized_manifest_path: Path,
    normalized_gate_report_path: Path,
    labels_root: Path,
    manifests_root: Path,
    repo_root: Path,
    refuse_overwrite: bool = True,
    code_commit_sha: str | None = None,
    base_commit_sha: str | None = None,
) -> OrchestrationResult:
    """Run the full Phase 4bn-W label execution once. Fail-closed on any breach."""
    start = time.monotonic()
    checks: list[CheckResult] = []
    per_day_records: list[PerDayLabelRecord] = []
    aggregate = LabelMultiDaySummaryV002()
    warnings_crossed: list[str] = []
    running_label_bytes = 0
    temp_peak = 0
    d_free_min_observed = _disk_free_bytes(labels_root)

    assert_label_path_under_data_microstructure(labels_root, label="labels_root")
    assert_label_manifest_path_under_manifests(
        manifests_root / "x.json", label="manifests_root probe"
    )

    # Locked-schema integrity + forbidden-column guard (defence in depth).
    if len(LABEL_SCHEMA_V002) != 40:
        raise Phase4bnWValidationError("LABEL_SCHEMA_V002 is not 40 columns")
    if len(LABEL_LINEAGE_COLUMNS_V002) != 17 or len(LABEL_NAMES_V002) != 8:
        raise Phase4bnWValidationError("LABEL_SCHEMA_V002 composition drifted")
    if len(LABEL_SUPPORT_COLUMN_NAMES_V002) != 14:
        raise Phase4bnWValidationError("LABEL support column count drifted")
    assert_no_forbidden_label_substrings_v002(LABEL_SCHEMA_V002)

    try:
        artefacts = verify_preconditions(
            feature_manifest_path=feature_manifest_path,
            feature_gate_report_path=feature_gate_report_path,
            normalized_manifest_path=normalized_manifest_path,
            normalized_gate_report_path=normalized_gate_report_path,
            repo_root=repo_root,
            checks=checks,
        )
        preflight = run_preflight(
            artefacts=artefacts, labels_root=labels_root, checks=checks
        )
        d_free_min_observed = min(d_free_min_observed, preflight.d_free_bytes)

        commit_sha = code_commit_sha or _git_head_sha(repo_root)
        base_sha = base_commit_sha or BASE_COMMIT_SHA_4BN_V_FINAL

        # Segment-scoped label_config_hash (Phase 4bn-V §16).
        label_config_hash = build_label_config_hash_v002_pre_v002_segment(
            source_feature_manifest_sha256=artefacts.feature_manifest_sha_before,
            source_feature_layer_gate_report_sha256=(
                artefacts.feature_gate_report_sha_before
            ),
            source_normalized_manifest_sha256=artefacts.normalized_manifest_sha_before,
            source_normalized_layer_gate_report_sha256=(
                artefacts.normalized_gate_report_sha_before
            ),
            source_raw_manifest_sha256=EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
            feature_config_hash=EXPECTED_FEATURE_CONFIG_HASH,
        )
        checks.append(
            CheckResult(
                "4bn-W.config_hash",
                "segment-scoped label_config_hash built",
                "pass",
                label_config_hash,
            )
        )

        manifest_out_path = manifests_root / SEGMENT_MANIFEST_BASENAME
        manifest_sidecar_path = manifest_out_path.with_suffix(
            manifest_out_path.suffix + ".sha256"
        )
        # Refuse-to-overwrite check for manifest + all per-day outputs.
        for label, p in (
            ("label segment manifest", manifest_out_path),
            ("label segment manifest sidecar", manifest_sidecar_path),
        ):
            if p.exists():
                raise Phase4bnWValidationError(f"refuse-to-overwrite: {label} exists at {p}")
        for src in artefacts.per_day_sources:
            out_p = derive_label_segment_parquet_path(
                labels_root=labels_root, symbol=SYMBOL, utc_date=src.date
            )
            if out_p.exists() or out_p.with_suffix(out_p.suffix + ".sha256").exists():
                raise Phase4bnWValidationError(
                    f"refuse-to-overwrite: label output already exists at {out_p}"
                )

        lineage_const = {
            "feature_manifest_sha256": artefacts.feature_manifest_sha_before,
            "feature_gate_sha256": artefacts.feature_gate_report_sha_before,
            "normalized_manifest_sha256": artefacts.normalized_manifest_sha_before,
            "normalized_gate_sha256": artefacts.normalized_gate_report_sha_before,
            "raw_manifest_sha256": EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
            "label_config_hash": label_config_hash,
        }

        # Per-day computation with a rolling normalized-day reference cache.
        prev_loaded = None  # NormalizedDayRef loaded as next_day in prior iteration
        n_days = len(artefacts.per_day_sources)
        prev_month = None
        for i, src in enumerate(artefacts.per_day_sources):
            if prev_loaded is not None and prev_loaded.utc_date == src.date:
                current_ref = prev_loaded
            else:
                current_ref = load_normalized_day_ref(
                    parquet_path=src.normalized_parquet_path
                )
            next_ref = None
            if i + 1 < n_days:
                next_ref = load_normalized_day_ref(
                    parquet_path=artefacts.per_day_sources[i + 1].normalized_parquet_path
                )
            record, written_bytes = _compute_one_day(
                day=src,
                current_ref=current_ref,
                next_ref=next_ref,
                envelope_terminal_unix_ms=artefacts.envelope_terminal_unix_ms,
                labels_root=labels_root,
                lineage_const=lineage_const,
                repo_root=repo_root,
            )
            per_day_records.append(record)
            aggregate.absorb(
                _summary_from_record(record)
            )
            running_label_bytes += written_bytes
            temp_peak = max(temp_peak, record.label_parquet_size_bytes)
            prev_loaded = next_ref

            elapsed = time.monotonic() - start
            d_free = _disk_free_bytes(labels_root)
            d_free_min_observed = min(d_free_min_observed, d_free)
            _enforce_budgets(
                running_label_bytes=running_label_bytes,
                elapsed=elapsed,
                d_free=d_free,
                temp_peak=temp_peak,
                warnings_crossed=warnings_crossed,
            )
            month = src.date[:7]
            if month != prev_month:
                checks.append(
                    CheckResult(
                        f"4bn-W.month.{month}",
                        f"month {month} boundary budget OK",
                        "pass",
                        f"label={running_label_bytes / GIB:.2f} GiB; "
                        f"D_free={d_free / GIB:.0f} GiB; elapsed={elapsed:.0f}s",
                    )
                )
                prev_month = month
            print(
                f"[phase-4bn-w]   day {i + 1}/{n_days} {src.date} "
                f"rows={record.row_count} "
                f"label_bytes={running_label_bytes / GIB:.2f}GiB "
                f"elapsed={elapsed:.0f}s",
                flush=True,
            )

        # Aggregate checks.
        if len(per_day_records) != EXPECTED_DATE_COUNT:
            raise Phase4bnWValidationError(
                f"produced_file_count {len(per_day_records)} != {EXPECTED_DATE_COUNT}"
            )
        total_rows = sum(r.row_count for r in per_day_records)
        if total_rows != EXPECTED_TOTAL_ROW_COUNT:
            raise Phase4bnWValidationError(
                f"total label row count {total_rows} != {EXPECTED_TOTAL_ROW_COUNT}"
            )
        if aggregate.total_row_count != EXPECTED_TOTAL_ROW_COUNT:
            raise Phase4bnWValidationError("aggregate row count != 400,001,695")
        checks.append(
            CheckResult(
                "4bn-W.aggregate",
                "produced 275 label parquets; total rows == source rows",
                "pass",
                str(total_rows),
            )
        )

        runtime_s = time.monotonic() - start
        budget_witnesses: dict[str, Any] = {
            "label_warn_bytes": LABEL_WARN_BYTES,
            "label_hard_bytes": LABEL_HARD_BYTES,
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
            "d_free_after_bytes": _disk_free_bytes(labels_root),
            "measured_label_footprint_bytes": running_label_bytes,
            "measured_temp_footprint_pre_cleanup_bytes": temp_peak,
            "measured_temp_footprint_post_cleanup_bytes": 0,
            "measured_runtime_seconds": runtime_s,
            "preflight_estimated_label_bytes": preflight.estimated_label_bytes,
            "preflight_estimated_total_stack_bytes": (
                preflight.estimated_total_stack_bytes
            ),
            "warning_thresholds_crossed": list(warnings_crossed),
            "hard_caps_crossed": False,
        }

        now_unix_ms = int(time.time() * 1000)
        now_utc = datetime.now(UTC).isoformat()
        manifest_dict = build_segment_manifest(
            artefacts=artefacts,
            per_day_records=per_day_records,
            aggregate=aggregate,
            base_commit_sha=base_sha,
            code_commit_sha=commit_sha,
            label_config_hash=label_config_hash,
            created_at_unix_ms=now_unix_ms,
            created_at_utc=now_utc,
            total_label_footprint_bytes=running_label_bytes,
            total_label_row_count=total_rows,
            budget_witnesses=budget_witnesses,
            repo_root=repo_root,
        )
        assert_manifest_field_contract(manifest_dict)
        checks.append(
            CheckResult("4bn-W.manifest", "label segment manifest field contract OK", "pass")
        )

        manifest_sha, _ = atomic_write_label_manifest(
            manifest_out_path, manifest_dict, refuse_overwrite=refuse_overwrite
        )
        manifest_sidecar_sha, _ = write_label_sha256_sidecar(
            manifest_sidecar_path,
            target_filename=manifest_out_path.name,
            sha256_hex=manifest_sha,
            refuse_overwrite=refuse_overwrite,
        )
        checks.append(
            CheckResult("4bn-W.write", "label segment manifest + sidecar written", "pass")
        )

        # Post-write source immutability re-hash (fail closed on drift).
        for label, p, want in (
            ("feature segment manifest", artefacts.feature_manifest_path,
             artefacts.feature_manifest_sha_before),
            ("feature-layer gate report", artefacts.feature_gate_report_path,
             artefacts.feature_gate_report_sha_before),
            ("normalized segment manifest", artefacts.normalized_manifest_path,
             artefacts.normalized_manifest_sha_before),
            ("normalized-layer gate report", artefacts.normalized_gate_report_path,
             artefacts.normalized_gate_report_sha_before),
        ):
            actual, _ = _sha256_file(p)
            if actual != want:
                raise Phase4bnWValidationError(
                    f"POST-WRITE source immutability violation for {label}"
                )
        checks.append(
            CheckResult("4bn-W.immutability", "all source inputs byte-identical pre/post", "pass")
        )

        return OrchestrationResult(
            overall_status="pass",
            output_manifest_path=manifest_out_path,
            output_manifest_sha256=manifest_sha,
            output_manifest_sidecar_path=manifest_sidecar_path,
            output_manifest_sidecar_sha256=manifest_sidecar_sha,
            produced_file_count=len(per_day_records),
            total_label_row_count=total_rows,
            total_label_footprint_bytes=running_label_bytes,
            label_config_hash=label_config_hash,
            envelope_terminal_unix_ms=artefacts.envelope_terminal_unix_ms,
            per_day_records=per_day_records,
            aggregate=aggregate,
            checks=checks,
            budget_witnesses=budget_witnesses,
            wall_clock_seconds=runtime_s,
            warning_thresholds_crossed=warnings_crossed,
            hard_caps_crossed=False,
            result_state=(
                "LABEL_EXECUTION_SUCCEEDED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
            ),
        )
    except (Phase4bnWOrchestrationError, LabelComputationErrorV002) as exc:
        failed_id = checks[-1].check_id if checks else "4bn-W.precondition"
        return OrchestrationResult(
            overall_status="fail_closed",
            output_manifest_path=None,
            output_manifest_sha256=None,
            output_manifest_sidecar_path=None,
            output_manifest_sidecar_sha256=None,
            produced_file_count=len(per_day_records),
            total_label_row_count=sum(r.row_count for r in per_day_records),
            total_label_footprint_bytes=running_label_bytes,
            label_config_hash=None,
            envelope_terminal_unix_ms=None,
            per_day_records=per_day_records,
            aggregate=aggregate,
            checks=checks,
            budget_witnesses={},
            wall_clock_seconds=time.monotonic() - start,
            warning_thresholds_crossed=warnings_crossed,
            hard_caps_crossed="hard cap" in str(exc).lower(),
            failed_check_id=failed_id,
            failure_message=str(exc),
            result_state="LABEL_EXECUTION_PARTIAL__FAIL_CLOSED__REMAIN_PAUSED"
            if per_day_records
            else "LABEL_EXECUTION_NOT_RUN__MISSING_LOCAL_ARTEFACTS__REMAIN_PAUSED",
        )


def _summary_from_record(record: PerDayLabelRecord) -> Any:
    """Adapt a PerDayLabelRecord back into a LabelComputationSummaryV002-shape."""
    from prometheus.research.microstructure.labels_compute_v002 import (
        LabelComputationSummaryV002,
    )

    return LabelComputationSummaryV002(
        utc_date=record.date,
        row_count=record.row_count,
        invalid_price_row_count=record.invalid_price_row_count,
        censored_per_horizon=dict(record.per_horizon_censored_counts),
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Phase 4bn-W — Label-Only Pre-V002 BTCUSDT aggTrades Segment Execution. "
            "Bounded, offline, local-gitignored, non-eligible label segment generator."
        )
    )
    p.add_argument("--repo-root", type=Path, default=_REPO_ROOT)
    p.add_argument("--feature-manifest", type=Path, default=None)
    p.add_argument("--feature-gate-report", type=Path, default=None)
    p.add_argument("--normalized-manifest", type=Path, default=None)
    p.add_argument("--normalized-gate-report", type=Path, default=None)
    p.add_argument("--labels-root", type=Path, default=None)
    p.add_argument("--manifests-root", type=Path, default=None)
    p.add_argument("--code-commit-sha", type=str, default=None)
    p.add_argument("--base-commit-sha", type=str, default=None)
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="run preconditions + preflight and exit before any compute / write",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root: Path = args.repo_root.resolve()
    if not (repo_root / "src" / "prometheus").exists():
        raise Phase4bnWOrchestrationError(
            f"repo_root does not look like the Prometheus repo: {repo_root}"
        )
    feature_manifest_path = (
        args.feature_manifest or repo_root / DEFAULT_FEATURE_SEGMENT_MANIFEST_REL
    ).resolve()
    feature_gate_report_path = (
        args.feature_gate_report or repo_root / DEFAULT_FEATURE_GATE_REPORT_REL
    ).resolve()
    normalized_manifest_path = (
        args.normalized_manifest or repo_root / DEFAULT_NORMALIZED_SEGMENT_MANIFEST_REL
    ).resolve()
    normalized_gate_report_path = (
        args.normalized_gate_report or repo_root / DEFAULT_NORMALIZED_GATE_REPORT_REL
    ).resolve()
    labels_root = (args.labels_root or repo_root / DEFAULT_LABELS_ROOT_REL).resolve()
    manifests_root = (
        args.manifests_root or repo_root / DEFAULT_MANIFESTS_ROOT_REL
    ).resolve()
    labels_root.mkdir(parents=True, exist_ok=True)
    manifests_root.mkdir(parents=True, exist_ok=True)

    print(f"[phase-4bn-w] repo_root          : {repo_root}", flush=True)
    print(f"[phase-4bn-w] feature_manifest   : {feature_manifest_path}", flush=True)
    print(f"[phase-4bn-w] feature_gate       : {feature_gate_report_path}", flush=True)
    print(f"[phase-4bn-w] normalized_manifest: {normalized_manifest_path}", flush=True)
    print(f"[phase-4bn-w] normalized_gate    : {normalized_gate_report_path}", flush=True)
    print(f"[phase-4bn-w] labels_root        : {labels_root}", flush=True)
    print(f"[phase-4bn-w] manifests_root     : {manifests_root}", flush=True)
    print(f"[phase-4bn-w] dry_run            : {args.dry_run}", flush=True)

    if args.dry_run:
        checks: list[CheckResult] = []
        artefacts = verify_preconditions(
            feature_manifest_path=feature_manifest_path,
            feature_gate_report_path=feature_gate_report_path,
            normalized_manifest_path=normalized_manifest_path,
            normalized_gate_report_path=normalized_gate_report_path,
            repo_root=repo_root,
            checks=checks,
        )
        run_preflight(artefacts=artefacts, labels_root=labels_root, checks=checks)
        lch = build_label_config_hash_v002_pre_v002_segment(
            source_feature_manifest_sha256=artefacts.feature_manifest_sha_before,
            source_feature_layer_gate_report_sha256=(
                artefacts.feature_gate_report_sha_before
            ),
            source_normalized_manifest_sha256=artefacts.normalized_manifest_sha_before,
            source_normalized_layer_gate_report_sha256=(
                artefacts.normalized_gate_report_sha_before
            ),
            source_raw_manifest_sha256=EXPECTED_RAW_SEGMENT_MANIFEST_SHA,
            feature_config_hash=EXPECTED_FEATURE_CONFIG_HASH,
        )
        for c in checks:
            print(f"[phase-4bn-w]   {c.status.upper():4s} {c.check_id}: {c.title}", flush=True)
        print(f"[phase-4bn-w]   label_config_hash = {lch}", flush=True)
        print(
            f"[phase-4bn-w]   envelope_terminal_unix_ms = "
            f"{artefacts.envelope_terminal_unix_ms}",
            flush=True,
        )
        print("[phase-4bn-w] dry-run complete; exiting before compute / write", flush=True)
        return 0

    result = run(
        feature_manifest_path=feature_manifest_path,
        feature_gate_report_path=feature_gate_report_path,
        normalized_manifest_path=normalized_manifest_path,
        normalized_gate_report_path=normalized_gate_report_path,
        labels_root=labels_root,
        manifests_root=manifests_root,
        repo_root=repo_root,
        refuse_overwrite=True,
        code_commit_sha=args.code_commit_sha,
        base_commit_sha=args.base_commit_sha,
    )
    for c in result.checks:
        print(f"[phase-4bn-w]   {c.status.upper():4s} {c.check_id}: {c.title}", flush=True)
    if result.overall_status != "pass":
        print(
            f"[phase-4bn-w] FAIL_CLOSED at {result.failed_check_id}: "
            f"{result.failure_message}",
            file=sys.stderr,
            flush=True,
        )
        return 2
    print(
        f"[phase-4bn-w] DONE produced={result.produced_file_count} "
        f"rows={result.total_label_row_count} "
        f"footprint={result.total_label_footprint_bytes / GIB:.2f} GiB "
        f"label_config_hash={result.label_config_hash} "
        f"envelope_terminal={result.envelope_terminal_unix_ms} "
        f"manifest_sha={result.output_manifest_sha256} "
        f"sidecar_sha={result.output_manifest_sidecar_sha256} "
        f"elapsed={result.wall_clock_seconds:.1f}s "
        f"result_state={result.result_state}",
        flush=True,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - script entry
    try:
        sys.exit(main())
    except Phase4bnWOrchestrationError as exc:
        print(f"[phase-4bn-w] FAIL_CLOSED: {exc}", file=sys.stderr, flush=True)
        sys.exit(2)
