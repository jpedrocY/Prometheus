"""Phase 4bn-S — Feature-Only Pre-V002 BTCUSDT aggTrades Segment Execution.

Bounded, standalone orchestrator authorised by the Phase 4bn-S
authorization prompt and recommended by the Phase 4bn-R feature
manifest / versioning memo
(``docs/00-meta/implementation-reports/2026-06-04_phase-4bn-r_feature-manifest-versioning-memo.md``).

This script feature-derives the **local, gitignored, non-eligible**
Phase 4bn-O pre-v002 normalized BTCUSDT aggTrades segment
(2024-03-01 .. 2024-11-30 inclusive UTC; 275 days; 400,001,695 events)
into a phase-scoped **pre-v002 feature segment** of the existing v002
feature family ``microstructure_features_aggtrades_v001`` and writes:

- 275 per-day feature Parquet files + canonical ``.sha256`` sidecars
  under
  ``data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/``;
- one non-eligible feature **segment** manifest + canonical sidecar
  under ``data/microstructure/manifests/``.

It reuses the locked Phase 4bm-H v002 feature primitives unchanged
(``features_schema_v002``, ``features_compute_v002``, ``features_io``)
and adds only bounded orchestration: non-eligible-source precondition
enforcement (Phase 4bn-P normalized-layer gate report PASS over the
Phase 4bn-O normalized segment manifest), exact date-range / symbol /
family guards, no-network posture, Phase 4bn-L budget caps, segment
output naming, and the Phase 4bn-R segment-manifest contract.

Strict scope — this script does NOT and MUST NOT:

- derive / create labels, targets, future returns, MFE / MAE /
  R-multiple / barrier outputs;
- run ML, score models, generate predictions, run diagnostics;
- run strategy / signals / PnL / backtests;
- create ``data/research`` outputs;
- run feature ranking / selection / pruning / tuning / calibration;
- flip ``research_eligible`` or transition ``eligibility_gate_status``;
- create a chronological split policy;
- read the v002 terminal normalized/raw window or any sealed-test date;
- read or mutate the published normalized / feature ``__v002`` family;
- create v003, a database (``.duckdb`` / ``.sqlite``), or compact Parquet;
- acquire data, call endpoints, download archives, use credentials,
  ``.env``, ``.mcp.json``, MCP, Graphify, WebSocket, or private APIs;
- commit any artefact under ``data/microstructure`` or ``data/research``;
- authorize any successor.

The orchestrator is intentionally narrow: Python standard library plus
pyarrow plus the locked v002 feature scaffold. No networking import is
present. All writes are atomic (temp + ``os.replace``), refuse to
overwrite finalised outputs, and are restricted to the gitignored
``data/microstructure/features/`` and ``data/microstructure/manifests/``
namespaces. Any precondition / per-day / aggregate / budget breach
fails closed BEFORE the feature segment manifest is written; partial
per-day feature Parquets that may exist remain independently verifiable
via their sidecars and remain non-eligible / gitignored.
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

# Locked Phase 4bm-H v002 feature primitives — reused verbatim, unchanged.
from prometheus.research.microstructure.features_compute_v002 import (  # noqa: E402
    CROSS_DAY_TAIL_BUFFER_MS,
    FeatureLineageV002,
    compute_aggtrades_features_v002,
    slice_prior_day_tail,
    write_feature_dataset_v002,
)
from prometheus.research.microstructure.features_io import (  # noqa: E402
    assert_manifest_output_path_under_manifests,
    assert_output_path_under_features,
    assert_path_under_data_microstructure,
    atomic_write_feature_manifest,
    write_feature_sha256_sidecar,
)
from prometheus.research.microstructure.features_manifest_v002 import (  # noqa: E402
    REQUIRED_V002_BOUNDARY_CONFIRMATIONS,
    REQUIRED_V002_NON_AUTHORIZATION_FLAGS,
    feature_dtypes_v002,
)
from prometheus.research.microstructure.features_schema_v002 import (  # noqa: E402
    CROSS_DAY_LOOKBACK_POLICY_V002,
    FEATURE_NAMES_V002,
    FEATURE_SCHEMA_V002,
    FEATURE_SCHEMA_VERSION_V002,
    FEATURE_WINDOW_LABELS_V002,
    FEATURE_WINDOWS_MS_V002,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002,
    INVALID_WINDOW_POLICY_V002,
    LEAKAGE_POLICY_V002,
    LINEAGE_COLUMNS_V002,
    SAME_TIMESTAMP_TIE_RULE_V002,
    TIMESTAMP_POLICY_V002,
    WINDOW_BOUNDARY_POLICY_V002,
    assert_no_forbidden_substrings_v002,
    build_feature_config_v002,
)

# ---------------------------------------------------------------------------
# Locked identity / boundary constants (Phase 4bn-S prompt + Phase 4bn-R memo).
# ---------------------------------------------------------------------------

PHASE_ID = "4bn-S"
PHASE_ID_FULL = "phase-4bn-s"
PHASE_ID_TOKEN = "4bn_s"
SOURCE_PHASE_BOUNDARY = "4bn-P"

FEATURE_FAMILY_ID = "microstructure_features_aggtrades_v001"
FEATURE_DATASET_VERSION = "v002"
VERSION = "v002"
FEATURE_SCHEMA_VERSION = "v001"
SEGMENT_LABEL = "pre_v002_segment"
DATA_FAMILY = "aggTrades"
MARKET = "usdm_futures"
DATASET_CATEGORY = "features"

SOURCE_NORMALIZED_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
SOURCE_NORMALIZED_DATASET_VERSION = "v002"
SOURCE_NORMALIZED_SCHEMA_VERSION = "NORMALIZED_SCHEMA_V001"
SYMBOL = "BTCUSDT"

# Segment output directory / manifest naming (distinct from published __v002).
SEGMENT_SUFFIX = f"{FEATURE_DATASET_VERSION}_pre_v002_segment_{PHASE_ID_TOKEN}"
FAMILY_DIR_NAME = f"{FEATURE_FAMILY_ID}__{SEGMENT_SUFFIX}"
SEGMENT_MANIFEST_BASENAME = f"{FAMILY_DIR_NAME}.json"

PUBLISHED_V002_FEATURE_DIR_NAME = f"{FEATURE_FAMILY_ID}__{FEATURE_DATASET_VERSION}"
PUBLISHED_V002_FEATURE_MANIFEST_REL = (
    f"data/microstructure/manifests/{FEATURE_FAMILY_ID}__{FEATURE_DATASET_VERSION}.json"
)
PUBLISHED_V002_NORMALIZED_MANIFEST_REL = (
    f"data/microstructure/manifests/"
    f"{SOURCE_NORMALIZED_DATASET_FAMILY}__{FEATURE_DATASET_VERSION}.json"
)

# Window contract.
EXPECTED_DATE_COUNT = 275
EXPECTED_DATE_START = "2024-03-01"
EXPECTED_DATE_END = "2024-11-30"
EXPECTED_TOTAL_EVENT_COUNT = 400_001_695
EXPECTED_TOTAL_NORMALIZED_FOOTPRINT_BYTES = 3_954_532_918
FULL_ENVELOPE_START = "2024-03-01"
FULL_ENVELOPE_END = "2025-02-28"
UTC_DAY_MS = 86_400_000

# Reference-only v002 terminal / sealed-test boundaries (never read here).
V002_TERMINAL_START = "2024-12-01"
V002_TERMINAL_END = "2025-02-28"
SEALED_TEST_START = "2025-02-14"
SEALED_TEST_END = "2025-02-28"

# Default base SHA = BASE_SHA_4BN_R_FINAL (operator-pinned Phase 4bn-R final).
BASE_COMMIT_SHA_4BN_R_FINAL = "40f0b3e54392e0e108b8664beedf25169a2d9778"

# Locked source-artefact SHA256s (Phase 4bn-O segment + Phase 4bn-P gate report).
EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA = (
    "0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa"
)
EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA = (
    "5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402"
)
EXPECTED_NORMALIZED_GATE_REPORT_SHA = (
    "3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134"
)
REQUIRED_GATE_RESULT_STATE = (
    "NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
)

# Default source/output relative paths.
DEFAULT_NORMALIZED_SEGMENT_MANIFEST_REL = (
    "data/microstructure/manifests/"
    "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json"
)
DEFAULT_NORMALIZED_GATE_REPORT_REL = (
    "data/microstructure/gate-reports/normalized/"
    "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o__"
    "phase-4bn-p__1780599605192__3fd795ceac4f.json"
)
DEFAULT_FEATURES_ROOT_REL = "data/microstructure/features"
DEFAULT_MANIFESTS_ROOT_REL = "data/microstructure/manifests"

# Per-row lineage sentinel: this pre-v002 segment has NO Stage-3 successor-state.
NO_SUCCESSOR_STATE_SENTINEL = "non_eligible_pre_v002_segment_no_successor_state"

# ---------------------------------------------------------------------------
# Budget caps (Phase 4bn-L derived-stack storage-budget memo; FEATURE layer).
# ---------------------------------------------------------------------------

GIB = 1024**3
FEATURE_WARN_BYTES = 50 * GIB
FEATURE_HARD_BYTES = 100 * GIB
RUNTIME_WARN_SECONDS = 4 * 3600
RUNTIME_HARD_SECONDS = 8 * 3600
TEMP_WARN_BYTES = 50 * GIB
TEMP_HARD_BYTES = 100 * GIB
TOTAL_STACK_WARN_BYTES = 250 * GIB
TOTAL_STACK_HARD_BYTES = 300 * GIB
D_FREE_FLOOR_BYTES = 500 * GIB  # preflight floor
D_FREE_MIN_BYTES = 350 * GIB  # in-execution floor

# Conservative per-event feature footprint estimate (published v002 ~133 B/row).
PREFLIGHT_BYTES_PER_EVENT = 160

# ---------------------------------------------------------------------------
# Forbidden scope tokens / manifest field-name substrings.
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

# Forbidden segment-manifest field-name substrings (Phase 4bn-N §13 lineage,
# extended for the feature layer). The three explicitly-validated declaration
# subtrees (governance_labels / non_authorization_flags / boundary_confirmations)
# legitimately carry forbidden-as-declaration keys and are NOT rescanned.
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
    "_loss",
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

_DECLARATION_SUBTREES = frozenset(
    {"governance_labels", "non_authorization_flags", "boundary_confirmations"}
)


# ---------------------------------------------------------------------------
# Result / error types
# ---------------------------------------------------------------------------


class Phase4bnSOrchestrationError(RuntimeError):
    """Raised when the Phase 4bn-S orchestrator fails closed."""


class Phase4bnSValidationError(Phase4bnSOrchestrationError):
    """Raised when a precondition / per-day / aggregate / budget check fails."""


@dataclass
class CheckResult:
    """One named check outcome."""

    check_id: str
    title: str
    status: str  # "pass" | "warn" | "fail"
    detail: str = ""


@dataclass
class PerDaySource:
    """Resolved per-date normalized source paths/SHAs from the 4bn-O inventory."""

    date: str
    symbol: str
    parquet_path: Path
    parquet_rel_path: str
    parquet_sha256: str
    sidecar_path: Path
    sidecar_sha256: str
    event_count: int
    first_transact_time_ms: int
    last_transact_time_ms: int
    min_agg_trade_id: int
    max_agg_trade_id: int


@dataclass
class PerDayFeatureRecord:
    """Per-date feature production record for the segment manifest inventory."""

    date: str
    symbol: str
    feature_parquet_path: str
    feature_parquet_sha256: str
    feature_parquet_size_bytes: int
    row_count: int
    feature_sidecar_path: str
    feature_sidecar_sha256: str
    feature_sidecar_size_bytes: int
    paired_source_normalized_parquet_path: str
    paired_source_normalized_parquet_sha256: str
    first_transact_time_ms: int
    last_transact_time_ms: int
    min_agg_trade_id: int
    max_agg_trade_id: int
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


def _utc_day_start_ms(utc_date: str) -> int:
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
        raise Phase4bnSValidationError(f"date not YYYY-MM-DD: {date!r}")
    try:
        datetime.strptime(date, "%Y-%m-%d")  # reject malformed (e.g. 2024-13-40)
    except ValueError as exc:
        raise Phase4bnSValidationError(f"malformed date: {date!r}") from exc
    if date >= V002_TERMINAL_START:
        raise Phase4bnSValidationError(
            f"date {date} is in/after the v002 terminal window "
            f"(>= {V002_TERMINAL_START}); rejected"
        )
    if SEALED_TEST_START <= date <= SEALED_TEST_END:
        raise Phase4bnSValidationError(f"date {date} is a sealed-test date; rejected")
    if date < EXPECTED_DATE_START:
        raise Phase4bnSValidationError(
            f"date {date} is before segment start {EXPECTED_DATE_START}; rejected"
        )
    if date > EXPECTED_DATE_END:
        raise Phase4bnSValidationError(
            f"date {date} is after segment end {EXPECTED_DATE_END}; rejected"
        )


def _assert_symbol(symbol: str) -> None:
    """Fail closed on any symbol other than BTCUSDT."""
    if symbol != SYMBOL:
        raise Phase4bnSValidationError(
            f"symbol {symbol!r} rejected; only {SYMBOL} permitted"
        )


def _assert_data_family(family: str) -> None:
    """Fail closed on any data family other than aggTrades."""
    if family != DATA_FAMILY:
        raise Phase4bnSValidationError(
            f"data_family {family!r} rejected; only {DATA_FAMILY} permitted"
        )


def _assert_no_forbidden_scope_tokens(text: str, *, where: str) -> None:
    """Fail closed if any forbidden scope token appears in *text*."""
    low = text.lower()
    for token in FORBIDDEN_SCOPE_TOKENS:
        if token in low:
            raise Phase4bnSValidationError(
                f"forbidden scope token {token!r} found in {where}"
            )


def _assert_segment_naming() -> None:
    """Fail closed if the segment directory/manifest collide with v003 / __v002."""
    if "v003" in FAMILY_DIR_NAME or "v003" in SEGMENT_MANIFEST_BASENAME:
        raise Phase4bnSValidationError("v003 token present in segment naming")
    if FAMILY_DIR_NAME == PUBLISHED_V002_FEATURE_DIR_NAME:
        raise Phase4bnSValidationError(
            "segment family dir must differ from published __v002 feature directory"
        )
    if f"{FEATURE_FAMILY_ID}__{FEATURE_DATASET_VERSION}.json" == SEGMENT_MANIFEST_BASENAME:
        raise Phase4bnSValidationError(
            "segment manifest must differ from published __v002 feature manifest"
        )


def _derive_feature_parquet_path(
    *, features_root: Path, symbol: str, utc_date: str
) -> Path:
    """Compute the pre-v002 feature segment Parquet path for ``(symbol, utc_date)``.

    Layout (relative to *features_root*, which must resolve to
    ``data/microstructure/features/``):
    ``<FAMILY_DIR_NAME>/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-features-aggtrades-<YYYY-MM-DD>.parquet``.
    """
    assert_path_under_data_microstructure(features_root, label="features_root")
    if features_root.name != "features":
        raise Phase4bnSValidationError(
            f"features_root must end in 'features' (got {features_root.name!r})"
        )
    if not symbol or not symbol.isalnum() or symbol != symbol.upper():
        raise Phase4bnSValidationError("symbol must be uppercase alphanumeric")
    parts = utc_date.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise Phase4bnSValidationError(f"utc_date must be YYYY-MM-DD; got {utc_date!r}")
    yyyy, mm, _dd = parts
    out = (
        features_root
        / FAMILY_DIR_NAME
        / symbol
        / yyyy
        / mm
        / f"{symbol}-features-aggtrades-{utc_date}.parquet"
    )
    assert_output_path_under_features(out, label="pre-v002 feature segment parquet path")
    if PUBLISHED_V002_FEATURE_DIR_NAME + "/" in (
        out.as_posix().replace(FAMILY_DIR_NAME, "")
    ):
        raise Phase4bnSValidationError(
            "feature output path must not resolve under the published __v002 dir"
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


# ---------------------------------------------------------------------------
# Source artefact loading + non-eligible-source precondition enforcement
# ---------------------------------------------------------------------------


@dataclass
class SourceArtefactSet:
    """Resolved read-only inputs + pre-state SHAs for the non-eligible source."""

    segment_manifest_path: Path
    segment_manifest_sha_before: str
    segment_manifest_parsed: dict[str, Any]
    segment_manifest_sidecar_path: Path
    segment_manifest_sidecar_sha_before: str
    gate_report_path: Path
    gate_report_sha_before: str
    gate_report_parsed: dict[str, Any]
    per_day_sources: list[PerDaySource]


def verify_preconditions(
    *,
    segment_manifest_path: Path,
    gate_report_path: Path,
    repo_root: Path,
    checks: list[CheckResult],
) -> SourceArtefactSet:
    """Verify all input preconditions; fail closed before any output is written."""
    _assert_segment_naming()

    # 1. normalized segment manifest exists + SHA matches.
    if not segment_manifest_path.exists():
        raise Phase4bnSValidationError(
            f"normalized segment manifest missing: {segment_manifest_path}"
        )
    seg_sha, _ = _sha256_file(segment_manifest_path)
    if seg_sha != EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA:
        raise Phase4bnSValidationError(
            f"normalized segment manifest SHA mismatch: got {seg_sha}, "
            f"expected {EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SHA}"
        )
    parsed = json.loads(segment_manifest_path.read_bytes().decode("utf-8"))
    if not isinstance(parsed, dict):
        raise Phase4bnSValidationError("normalized segment manifest is not a JSON object")
    checks.append(
        CheckResult(
            "4bn-S.1", "normalized segment manifest present + SHA matches", "pass", seg_sha
        )
    )

    # 2. normalized segment manifest sidecar canonical format + SHA matches.
    seg_sidecar_path = segment_manifest_path.with_suffix(
        segment_manifest_path.suffix + ".sha256"
    )
    if not seg_sidecar_path.exists():
        raise Phase4bnSValidationError(
            f"normalized segment manifest sidecar missing: {seg_sidecar_path}"
        )
    seg_sidecar_sha, _ = _sha256_file(seg_sidecar_path)
    if seg_sidecar_sha != EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA:
        raise Phase4bnSValidationError(
            f"normalized segment manifest sidecar SHA mismatch: got {seg_sidecar_sha}, "
            f"expected {EXPECTED_NORMALIZED_SEGMENT_MANIFEST_SIDECAR_SHA}"
        )
    expected_sidecar_body = f"{seg_sha}  {segment_manifest_path.name}\n"
    if seg_sidecar_path.read_bytes() != expected_sidecar_body.encode("ascii"):
        raise Phase4bnSValidationError(
            "normalized segment manifest sidecar is not the canonical two-space body"
        )
    checks.append(
        CheckResult("4bn-S.2", "normalized segment manifest sidecar canonical + SHA", "pass")
    )

    # 3. identity / scope locks.
    if parsed.get("symbol_list") != [SYMBOL]:
        raise Phase4bnSValidationError(
            f"segment manifest symbol_list != [{SYMBOL!r}]: {parsed.get('symbol_list')!r}"
        )
    _assert_data_family(str(parsed.get("data_family", "")))
    if str(parsed.get("market", "")) != MARKET:
        raise Phase4bnSValidationError(
            f"segment manifest market != {MARKET}: {parsed.get('market')!r}"
        )
    if (
        parsed.get("dataset_family") != SOURCE_NORMALIZED_DATASET_FAMILY
        or parsed.get("dataset_version") != SOURCE_NORMALIZED_DATASET_VERSION
        or parsed.get("segment_label") != SEGMENT_LABEL
    ):
        raise Phase4bnSValidationError("segment manifest identity does not match")
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
        CheckResult("4bn-S.3", "segment manifest identity / scope locks match", "pass")
    )

    # 4. window contract.
    if (
        parsed.get("date_start") != EXPECTED_DATE_START
        or parsed.get("date_end") != EXPECTED_DATE_END
        or parsed.get("date_count") != EXPECTED_DATE_COUNT
        or parsed.get("expected_file_count") != EXPECTED_DATE_COUNT
        or parsed.get("produced_file_count") != EXPECTED_DATE_COUNT
        or parsed.get("total_row_count") != EXPECTED_TOTAL_EVENT_COUNT
        or parsed.get("total_event_count") != EXPECTED_TOTAL_EVENT_COUNT
        or parsed.get("total_normalized_footprint_bytes")
        != EXPECTED_TOTAL_NORMALIZED_FOOTPRINT_BYTES
    ):
        raise Phase4bnSValidationError("segment manifest window contract does not match")
    checks.append(
        CheckResult(
            "4bn-S.4",
            "segment manifest window contract matches (275 dates / 400,001,695 rows)",
            "pass",
        )
    )

    # 5. non-eligible posture + sealed-test / terminal boundary witnesses.
    if parsed.get("research_eligible") is not False:
        raise Phase4bnSValidationError("segment manifest research_eligible must be false")
    if parsed.get("eligibility_gate_status") != "pending":
        raise Phase4bnSValidationError(
            "segment manifest eligibility_gate_status must be 'pending'"
        )
    if parsed.get("v002_terminal_window_mode") != "by_reference":
        raise Phase4bnSValidationError(
            "segment manifest v002_terminal_window_mode must be 'by_reference'"
        )
    if parsed.get("sealed_test_split_touched") is not False:
        raise Phase4bnSValidationError(
            "segment manifest sealed_test_split_touched must be false"
        )
    if parsed.get("test_holdout_touched") is not False:
        raise Phase4bnSValidationError("segment manifest test_holdout_touched must be false")
    if parsed.get("test_rows_loaded") != 0:
        raise Phase4bnSValidationError("segment manifest test_rows_loaded must be 0")
    term = parsed.get("existing_v002_terminal_window") or {}
    if term.get("read") is not False:
        raise Phase4bnSValidationError("segment manifest v002 terminal read must be false")
    sealed = parsed.get("existing_v002_sealed_test_split") or {}
    if sealed.get("touched") is not False:
        raise Phase4bnSValidationError(
            "segment manifest sealed test split touched must be false"
        )
    checks.append(
        CheckResult("4bn-S.5", "segment manifest non-eligible / boundary posture OK", "pass")
    )

    # 6. Phase 4bn-P normalized-layer gate report exists + SHA matches + PASS.
    if not gate_report_path.exists():
        raise Phase4bnSValidationError(
            f"normalized-layer gate report missing: {gate_report_path}"
        )
    gate_sha, _ = _sha256_file(gate_report_path)
    if gate_sha != EXPECTED_NORMALIZED_GATE_REPORT_SHA:
        raise Phase4bnSValidationError(
            f"normalized-layer gate report SHA mismatch: got {gate_sha}, "
            f"expected {EXPECTED_NORMALIZED_GATE_REPORT_SHA}"
        )
    gate_parsed = json.loads(gate_report_path.read_bytes().decode("utf-8"))
    if not isinstance(gate_parsed, dict):
        raise Phase4bnSValidationError("normalized-layer gate report is not a JSON object")
    if gate_parsed.get("overall_status") != "pass":
        raise Phase4bnSValidationError("gate report overall_status is not 'pass'")
    if gate_parsed.get("gate_result_state") != REQUIRED_GATE_RESULT_STATE:
        raise Phase4bnSValidationError(
            "gate report gate_result_state is not the required PASS / non-eligible verdict"
        )
    if "PASS" not in str(gate_parsed.get("gate_verdict", "")):
        raise Phase4bnSValidationError("gate report verdict is not a PASS")
    gate_checks = gate_parsed.get("checks") or []
    n_pass = sum(1 for c in gate_checks if str(c.get("status")) == "pass")
    if len(gate_checks) != 25 or n_pass != 25:
        raise Phase4bnSValidationError(
            f"gate report must record 25/25 PASS checks (got {n_pass}/{len(gate_checks)})"
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
        if gate_parsed.get(flag) is not want:
            raise Phase4bnSValidationError(
                f"gate report {flag} must be {want} (got {gate_parsed.get(flag)!r})"
            )
    if gate_parsed.get("eligibility_gate_status_after") != "pending":
        raise Phase4bnSValidationError(
            "gate report eligibility_gate_status_after must be 'pending'"
        )
    # Predecessor linkage: the gate report must gate THIS segment manifest.
    if gate_parsed.get("input_normalized_manifest_sha256") != seg_sha:
        raise Phase4bnSValidationError(
            "gate report input_normalized_manifest_sha256 does not match the segment manifest"
        )
    checks.append(
        CheckResult(
            "4bn-S.6",
            "Phase 4bn-P normalized-layer gate report present + SHA + 25/25 PASS",
            "pass",
            gate_sha,
        )
    )

    # 7. exactly 275 inventory entries; per-day parquet + sidecar verified.
    inventory: list[dict[str, Any]] = list(parsed.get("per_file_inventory", []))
    if len(inventory) != EXPECTED_DATE_COUNT:
        raise Phase4bnSValidationError(
            f"per_file_inventory length {len(inventory)} != {EXPECTED_DATE_COUNT}"
        )
    date_list = list(parsed.get("date_list", []))
    if len(date_list) != EXPECTED_DATE_COUNT or len(set(date_list)) != EXPECTED_DATE_COUNT:
        raise Phase4bnSValidationError("date_list length / uniqueness invalid")
    if [str(e["date"]) for e in inventory] != date_list:
        raise Phase4bnSValidationError("per_file_inventory dates do not match date_list")

    micro_root = repo_root / "data" / "microstructure"
    expected_seg_dir = (
        f"{SOURCE_NORMALIZED_DATASET_FAMILY}__{FEATURE_DATASET_VERSION}_pre_v002_segment_4bn_o"
    )
    per_day_sources: list[PerDaySource] = []
    for entry in inventory:
        date = str(entry["date"])
        _assert_date_in_segment(date)
        _assert_symbol(str(entry["symbol"]))

        rel_parquet = str(entry["local_parquet_path"])
        _assert_no_forbidden_scope_tokens(rel_parquet, where=f"normalized parquet path {date}")
        if expected_seg_dir not in rel_parquet:
            raise Phase4bnSValidationError(
                f"normalized parquet path outside the pre-v002 segment dir: {rel_parquet}"
            )
        if f"{PUBLISHED_V002_FEATURE_DIR_NAME}/" in rel_parquet or (
            f"{SOURCE_NORMALIZED_DATASET_FAMILY}__{FEATURE_DATASET_VERSION}/" in rel_parquet
        ):
            raise Phase4bnSValidationError(
                f"normalized parquet path resolves to a published __v002 family: {rel_parquet}"
            )
        if "BTCUSDT" not in rel_parquet or "aggTrades" not in Path(rel_parquet).name:
            raise Phase4bnSValidationError(
                f"normalized parquet path outside BTCUSDT aggTrades convention: {rel_parquet}"
            )
        rel_strip = rel_parquet[len("microstructure/"):] if rel_parquet.startswith(
            "microstructure/"
        ) else rel_parquet
        parquet_path = micro_root / rel_strip
        if not parquet_path.exists():
            raise Phase4bnSValidationError(
                f"normalized parquet missing for {date}: {parquet_path}"
            )
        actual_sha, _ = _sha256_file(parquet_path)
        if actual_sha != str(entry["parquet_sha256"]):
            raise Phase4bnSValidationError(
                f"normalized parquet SHA mismatch for {date}: got {actual_sha}, "
                f"expected {entry['parquet_sha256']}"
            )

        rel_sidecar = str(entry["local_sidecar_path"])
        rel_sc_strip = rel_sidecar[len("microstructure/"):] if rel_sidecar.startswith(
            "microstructure/"
        ) else rel_sidecar
        sidecar_path = micro_root / rel_sc_strip
        if not sidecar_path.exists():
            raise Phase4bnSValidationError(
                f"normalized parquet sidecar missing for {date}: {sidecar_path}"
            )
        sidecar_sha, _ = _sha256_file(sidecar_path)
        if sidecar_path.read_bytes() != f"{actual_sha}  {parquet_path.name}\n".encode("ascii"):
            raise Phase4bnSValidationError(
                f"normalized parquet sidecar not canonical for {date}: {sidecar_path}"
            )

        per_day_sources.append(
            PerDaySource(
                date=date,
                symbol=str(entry["symbol"]),
                parquet_path=parquet_path,
                parquet_rel_path=rel_parquet,
                parquet_sha256=actual_sha,
                sidecar_path=sidecar_path,
                sidecar_sha256=sidecar_sha,
                event_count=int(entry["event_count"]),
                first_transact_time_ms=int(entry["first_transact_time_ms"]),
                last_transact_time_ms=int(entry["last_transact_time_ms"]),
                min_agg_trade_id=int(entry["min_agg_trade_id"]),
                max_agg_trade_id=int(entry["max_agg_trade_id"]),
            )
        )
    checks.append(
        CheckResult(
            "4bn-S.7",
            f"all {EXPECTED_DATE_COUNT} normalized parquets + sidecars verified; dates in segment",
            "pass",
            f"{len(per_day_sources)} parquets",
        )
    )

    return SourceArtefactSet(
        segment_manifest_path=segment_manifest_path,
        segment_manifest_sha_before=seg_sha,
        segment_manifest_parsed=parsed,
        segment_manifest_sidecar_path=seg_sidecar_path,
        segment_manifest_sidecar_sha_before=seg_sidecar_sha,
        gate_report_path=gate_report_path,
        gate_report_sha_before=gate_sha,
        gate_report_parsed=gate_parsed,
        per_day_sources=per_day_sources,
    )


# ---------------------------------------------------------------------------
# Preflight budget estimation (Phase 4bn-L; FEATURE layer)
# ---------------------------------------------------------------------------


@dataclass
class PreflightEstimate:
    """Preflight footprint / runtime / free-space estimate."""

    d_free_bytes: int
    estimated_feature_bytes: int
    estimated_temp_bytes: int
    estimated_total_stack_bytes: int


def run_preflight(
    *,
    artefacts: SourceArtefactSet,
    features_root: Path,
    checks: list[CheckResult],
) -> PreflightEstimate:
    """Estimate footprints + check Phase 4bn-L caps + D: floor before writing."""
    total_events = sum(s.event_count for s in artefacts.per_day_sources)
    max_day_events = max(s.event_count for s in artefacts.per_day_sources)

    est_feature = total_events * PREFLIGHT_BYTES_PER_EVENT
    est_temp = max_day_events * PREFLIGHT_BYTES_PER_EVENT
    est_total = est_feature + est_temp
    if est_feature <= 0:
        raise Phase4bnSValidationError("preflight cannot estimate feature output footprint")

    d_free = _disk_free_bytes(features_root)
    if d_free < D_FREE_FLOOR_BYTES:
        raise Phase4bnSValidationError(
            f"D: free space {d_free / GIB:.1f} GiB below preflight floor "
            f"{D_FREE_FLOOR_BYTES / GIB:.0f} GiB"
        )
    if est_feature > FEATURE_HARD_BYTES:
        raise Phase4bnSValidationError(
            f"preflight feature estimate {est_feature / GIB:.1f} GiB exceeds hard cap "
            f"{FEATURE_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_temp > TEMP_HARD_BYTES:
        raise Phase4bnSValidationError(
            f"preflight temp estimate {est_temp / GIB:.1f} GiB exceeds hard cap "
            f"{TEMP_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_total > TOTAL_STACK_HARD_BYTES:
        raise Phase4bnSValidationError(
            f"preflight total derived-stack estimate {est_total / GIB:.1f} GiB exceeds "
            f"hard cap {TOTAL_STACK_HARD_BYTES / GIB:.0f} GiB"
        )
    if est_feature > FEATURE_WARN_BYTES:
        checks.append(
            CheckResult(
                "4bn-S.preflight.warn",
                "feature footprint estimate above warning threshold",
                "warn",
                f"{est_feature / GIB:.1f} GiB",
            )
        )
    checks.append(
        CheckResult(
            "4bn-S.preflight",
            "preflight footprint/runtime/free-space within Phase 4bn-L caps",
            "pass",
            f"est_feature={est_feature / GIB:.2f} GiB; D_free={d_free / GIB:.0f} GiB",
        )
    )
    return PreflightEstimate(
        d_free_bytes=d_free,
        estimated_feature_bytes=est_feature,
        estimated_temp_bytes=est_temp,
        estimated_total_stack_bytes=est_total,
    )


# ---------------------------------------------------------------------------
# Per-day feature computation
# ---------------------------------------------------------------------------


def _compute_one_day(
    *,
    day: PerDaySource,
    prior_day: PerDaySource | None,
    features_root: Path,
    config: Any,
    lineage_const: Mapping[str, str],
    repo_root: Path,
) -> tuple[PerDayFeatureRecord, int]:
    """Compute one day's pre-v002 feature Parquet + sidecar; return its record."""
    import pyarrow.parquet as pq

    current_table = pq.read_table(day.parquet_path)
    if current_table.num_rows != day.event_count:
        raise Phase4bnSValidationError(
            f"row_count mismatch for {day.date}: "
            f"parquet={current_table.num_rows} manifest={day.event_count}"
        )

    prior_tail = None
    if prior_day is not None:
        prior_table = pq.read_table(prior_day.parquet_path)
        prior_tail = slice_prior_day_tail(
            prior_table,
            current_day_start_ms=_utc_day_start_ms(day.date),
            tail_buffer_ms=CROSS_DAY_TAIL_BUFFER_MS,
        )

    lineage = FeatureLineageV002(
        source_normalized_parquet_per_day_sha256=day.parquet_sha256,
        source_normalized_manifest_sha256=lineage_const["normalized_manifest_sha256"],
        source_successor_state_sha256=lineage_const["successor_state_sentinel"],
        source_phase_4bm_d_gate_report_sha256=lineage_const["gate_report_sha256"],
        feature_config_hash=config.feature_config_hash,
    )
    feature_table = compute_aggtrades_features_v002(
        current_day_table=current_table,
        prior_day_tail_table=prior_tail,
        config=config,
        lineage=lineage,
    )
    out_path = _derive_feature_parquet_path(
        features_root=features_root, symbol=SYMBOL, utc_date=day.date
    )
    write_result = write_feature_dataset_v002(
        table=feature_table, output_path=out_path, write_sha256_sidecar=True
    )

    data_root = repo_root / "data"
    rel_parquet = out_path.resolve().relative_to(data_root.resolve()).as_posix()
    rel_sidecar = (
        write_result.sidecar_path.resolve().relative_to(data_root.resolve()).as_posix()
    )
    record = PerDayFeatureRecord(
        date=day.date,
        symbol=SYMBOL,
        feature_parquet_path=rel_parquet,
        feature_parquet_sha256=write_result.parquet_sha256,
        feature_parquet_size_bytes=write_result.parquet_size_bytes,
        row_count=write_result.row_count,
        feature_sidecar_path=rel_sidecar,
        feature_sidecar_sha256=write_result.sidecar_sha256,
        feature_sidecar_size_bytes=write_result.sidecar_size_bytes,
        paired_source_normalized_parquet_path=day.parquet_rel_path,
        paired_source_normalized_parquet_sha256=day.parquet_sha256,
        first_transact_time_ms=day.first_transact_time_ms,
        last_transact_time_ms=day.last_transact_time_ms,
        min_agg_trade_id=day.min_agg_trade_id,
        max_agg_trade_id=day.max_agg_trade_id,
        status="produced_verified",
    )
    return record, write_result.parquet_size_bytes


def _enforce_budgets(
    *,
    running_feature_bytes: int,
    elapsed: float,
    d_free: int,
    temp_peak: int,
    warnings_crossed: list[str],
) -> None:
    """Fail closed on any hard cap; record warning crossings."""
    if running_feature_bytes > FEATURE_HARD_BYTES:
        raise Phase4bnSValidationError(
            f"feature footprint {running_feature_bytes / GIB:.1f} GiB exceeds hard cap"
        )
    if elapsed > RUNTIME_HARD_SECONDS:
        raise Phase4bnSValidationError(
            f"runtime {elapsed:.0f}s exceeds hard cap {RUNTIME_HARD_SECONDS}s"
        )
    if d_free < D_FREE_MIN_BYTES:
        raise Phase4bnSValidationError(
            f"D: free {d_free / GIB:.1f} GiB fell below in-execution floor "
            f"{D_FREE_MIN_BYTES / GIB:.0f} GiB"
        )
    if temp_peak > TEMP_HARD_BYTES:
        raise Phase4bnSValidationError(
            f"temporary workspace {temp_peak / GIB:.1f} GiB exceeds hard cap"
        )
    if running_feature_bytes > FEATURE_WARN_BYTES and "feature_warn" not in warnings_crossed:
        warnings_crossed.append("feature_warn")
    if elapsed > RUNTIME_WARN_SECONDS and "runtime_warn" not in warnings_crossed:
        warnings_crossed.append("runtime_warn")
    if temp_peak > TEMP_WARN_BYTES and "temp_warn" not in warnings_crossed:
        warnings_crossed.append("temp_warn")


# ---------------------------------------------------------------------------
# Segment manifest builder + field contract
# ---------------------------------------------------------------------------


def _feature_schema_hash() -> str:
    """Deterministic SHA256 over the locked 62-column schema + dtype map."""
    payload = json.dumps(
        {
            "feature_column_names": list(FEATURE_SCHEMA_V002),
            "feature_dtypes": feature_dtypes_v002(),
            "feature_schema_version": FEATURE_SCHEMA_VERSION_V002,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_segment_manifest(
    *,
    artefacts: SourceArtefactSet,
    per_day_records: Sequence[PerDayFeatureRecord],
    base_commit_sha: str,
    code_commit_sha: str,
    feature_config_hash: str,
    created_at_unix_ms: int,
    created_at_utc: str,
    total_feature_footprint_bytes: int,
    total_feature_row_count: int,
    budget_witnesses: Mapping[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    """Construct the Phase 4bn-S pre-v002 feature segment manifest dict."""

    def _rel_to_repo(p: Path) -> str:
        return str(p.resolve().relative_to(repo_root.resolve())).replace(os.sep, "/")

    date_list = [r.date for r in per_day_records]
    inventory_entries: list[dict[str, Any]] = [
        {
            "date": r.date,
            "symbol": r.symbol,
            "feature_parquet_path": r.feature_parquet_path,
            "feature_parquet_sha256": r.feature_parquet_sha256,
            "feature_parquet_size_bytes": r.feature_parquet_size_bytes,
            "row_count": r.row_count,
            "feature_sidecar_path": r.feature_sidecar_path,
            "feature_sidecar_sha256": r.feature_sidecar_sha256,
            "feature_sidecar_size_bytes": r.feature_sidecar_size_bytes,
            "paired_source_normalized_parquet_path": (
                r.paired_source_normalized_parquet_path
            ),
            "paired_source_normalized_parquet_sha256": (
                r.paired_source_normalized_parquet_sha256
            ),
            "first_transact_time_ms": r.first_transact_time_ms,
            "last_transact_time_ms": r.last_transact_time_ms,
            "min_agg_trade_id": r.min_agg_trade_id,
            "max_agg_trade_id": r.max_agg_trade_id,
            "status": r.status,
        }
        for r in per_day_records
    ]

    governance_labels: dict[str, str] = {
        "phase": PHASE_ID,
        "phase_id": PHASE_ID_FULL,
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "feature_computation": "performed_pre_v002_segment_non_eligible_by_phase_4bn_s",
        "labels": "forbidden",
        "ml": "forbidden",
        "diagnostics": "forbidden",
        "strategy": "forbidden",
        "backtest": "forbidden",
        "acquisition": "unauthorized",
        "research_use": "forbidden",
        "stop_trigger_domain": "trade_price_backtest_candidate",
        "segment": "true",
    }

    boundary_confirmations = {key: True for key in REQUIRED_V002_BOUNDARY_CONFIRMATIONS}
    non_authorization_flags = {
        key: False for key in REQUIRED_V002_NON_AUTHORIZATION_FLAGS
    }

    return {
        # Identity / family.
        "dataset_family": FEATURE_FAMILY_ID,
        "dataset_version": FEATURE_DATASET_VERSION,
        "version": VERSION,
        "feature_schema_version": FEATURE_SCHEMA_VERSION,
        "segment_label": SEGMENT_LABEL,
        "data_family": DATA_FAMILY,
        "symbol": SYMBOL,
        "symbol_list": [SYMBOL],
        "market": MARKET,
        "dataset_category": DATASET_CATEGORY,
        "feature_family_id": FEATURE_FAMILY_ID,
        # Segment / phase / lineage.
        "phase": PHASE_ID,
        "phase_id": PHASE_ID_FULL,
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "created_at_unix_ms": created_at_unix_ms,
        "created_at_utc": created_at_utc,
        "code_commit_sha": code_commit_sha,
        "base_commit_sha": base_commit_sha,
        "feature_config_hash": feature_config_hash,
        "feature_schema_hash": _feature_schema_hash(),
        # Schema description.
        "feature_column_count": len(FEATURE_SCHEMA_V002),
        "lineage_column_count": len(LINEAGE_COLUMNS_V002),
        "feature_quality_column_count": len(FEATURE_NAMES_V002),
        "feature_column_names": list(FEATURE_SCHEMA_V002),
        "lineage_column_names": list(LINEAGE_COLUMNS_V002),
        "computed_feature_column_names": list(FEATURE_NAMES_V002),
        "feature_dtypes": feature_dtypes_v002(),
        # Feature kernel policy.
        "leakage_policy": LEAKAGE_POLICY_V002,
        "cross_day_lookback_policy": CROSS_DAY_LOOKBACK_POLICY_V002,
        "cross_day_tail_buffer_ms": int(CROSS_DAY_TAIL_BUFFER_MS),
        "feature_windows_ms": list(FEATURE_WINDOWS_MS_V002),
        "feature_window_labels": list(FEATURE_WINDOW_LABELS_V002),
        "window_boundary_policy": WINDOW_BOUNDARY_POLICY_V002,
        "invalid_window_policy": dict(INVALID_WINDOW_POLICY_V002),
        "same_timestamp_tie_rule": SAME_TIMESTAMP_TIE_RULE_V002,
        "timestamp_policy": TIMESTAMP_POLICY_V002,
        "forbidden_substring_detector_tokens": list(
            FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002
        ),
        # Window / inventory.
        "date_start": EXPECTED_DATE_START,
        "date_end": EXPECTED_DATE_END,
        "date_count": EXPECTED_DATE_COUNT,
        "date_list": date_list,
        "expected_file_count": EXPECTED_DATE_COUNT,
        "produced_file_count": len(per_day_records),
        "total_row_count": total_feature_row_count,
        "actual_feature_row_count": total_feature_row_count,
        "total_footprint_bytes": total_feature_footprint_bytes,
        "per_file_inventory": inventory_entries,
        # Source linkage (non-eligible normalized segment + 4bn-P gate report).
        "source_dataset_family": SOURCE_NORMALIZED_DATASET_FAMILY,
        "source_dataset_version": SOURCE_NORMALIZED_DATASET_VERSION,
        "source_normalized_segment_manifest_path": _rel_to_repo(
            artefacts.segment_manifest_path
        ),
        "source_normalized_segment_manifest_sha256": (
            artefacts.segment_manifest_sha_before
        ),
        "source_normalized_segment_manifest_sidecar_sha256": (
            artefacts.segment_manifest_sidecar_sha_before
        ),
        "source_normalized_layer_gate_report_path": _rel_to_repo(
            artefacts.gate_report_path
        ),
        "source_normalized_layer_gate_report_sha256": artefacts.gate_report_sha_before,
        "source_normalized_schema_version": SOURCE_NORMALIZED_SCHEMA_VERSION,
        "source_eligibility_posture": "non_eligible_gate_passed_pending",
        # Per-row lineage column value map (documentation; no successor-state).
        "lineage_column_value_map": {
            "source_normalized_manifest_sha256": artefacts.segment_manifest_sha_before,
            "source_phase_4bm_d_gate_report_sha256": (
                "holds the Phase 4bn-P normalized-layer gate report SHA256 for this "
                "pre-v002 segment: " + artefacts.gate_report_sha_before
            ),
            "source_successor_state_sha256": (
                "no Stage-3 successor-state exists for this non-eligible pre-v002 "
                "segment; sentinel value: " + NO_SUCCESSOR_STATE_SENTINEL
            ),
        },
        # Published v002 feature family by reference only (never read/mutated).
        "existing_v002_feature_reference": {
            "path": PUBLISHED_V002_FEATURE_MANIFEST_REL,
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
        "boundary_confirmations": boundary_confirmations,
        "non_authorization_flags": non_authorization_flags,
        # Sealed-test / terminal boundary witnesses.
        "v002_terminal_window_mode": "by_reference",
        "existing_v002_terminal_window": {
            "start": V002_TERMINAL_START,
            "end": V002_TERMINAL_END,
            "read": False,
            "normalized_dates_read": False,
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
        "primary_key": ["symbol", "utc_date", "agg_trade_id", "row_index"],
        "storage_format": "parquet_zstd",
        "sidecar_policy": "canonical_two_space_sha256",
        "invalid_windows": [],
        # Budget witnesses (Phase 4bn-L).
        "budget_witnesses": dict(budget_witnesses),
    }


REQUIRED_MANIFEST_KEYS: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "version",
    "feature_schema_version",
    "segment_label",
    "data_family",
    "symbol",
    "market",
    "dataset_category",
    "feature_family_id",
    "phase_id",
    "source_phase_boundary",
    "created_at_unix_ms",
    "created_at_utc",
    "code_commit_sha",
    "base_commit_sha",
    "feature_config_hash",
    "feature_schema_hash",
    "feature_column_count",
    "lineage_column_count",
    "feature_quality_column_count",
    "feature_column_names",
    "lineage_column_names",
    "computed_feature_column_names",
    "feature_dtypes",
    "leakage_policy",
    "cross_day_lookback_policy",
    "cross_day_tail_buffer_ms",
    "feature_windows_ms",
    "feature_window_labels",
    "window_boundary_policy",
    "invalid_window_policy",
    "same_timestamp_tie_rule",
    "timestamp_policy",
    "forbidden_substring_detector_tokens",
    "date_start",
    "date_end",
    "date_count",
    "date_list",
    "expected_file_count",
    "produced_file_count",
    "total_row_count",
    "actual_feature_row_count",
    "total_footprint_bytes",
    "per_file_inventory",
    "source_dataset_family",
    "source_dataset_version",
    "source_normalized_segment_manifest_path",
    "source_normalized_segment_manifest_sha256",
    "source_normalized_layer_gate_report_path",
    "source_normalized_layer_gate_report_sha256",
    "source_normalized_schema_version",
    "source_eligibility_posture",
    "existing_v002_feature_reference",
    "full_intended_envelope_start",
    "full_intended_envelope_end",
    "research_eligible",
    "eligibility_gate_status",
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
    "partitioning_rule",
    "primary_key",
    "storage_format",
    "sidecar_policy",
    "invalid_windows",
    "budget_witnesses",
)


def assert_manifest_field_contract(manifest: Mapping[str, Any]) -> None:
    """Fail closed if the feature segment manifest violates the field contract."""
    missing = [k for k in REQUIRED_MANIFEST_KEYS if k not in manifest]
    if missing:
        raise Phase4bnSValidationError(f"feature segment manifest missing keys: {missing}")

    # Identity / versioning convention (Phase 4bn-R carried forward).
    if manifest["dataset_family"] != FEATURE_FAMILY_ID:
        raise Phase4bnSValidationError("manifest dataset_family must be the v002 feature family")
    if manifest["dataset_version"] != "v002" or manifest["version"] != "v002":
        raise Phase4bnSValidationError("manifest dataset_version/version must be 'v002'")
    if manifest["feature_schema_version"] != "v001":
        raise Phase4bnSValidationError("manifest feature_schema_version must be 'v001'")
    if manifest["segment_label"] != SEGMENT_LABEL:
        raise Phase4bnSValidationError("manifest segment_label must be 'pre_v002_segment'")
    if manifest["feature_column_count"] != 62:
        raise Phase4bnSValidationError("manifest feature_column_count must be 62")
    if manifest["lineage_column_count"] != 17:
        raise Phase4bnSValidationError("manifest lineage_column_count must be 17")
    if manifest["feature_quality_column_count"] != 45:
        raise Phase4bnSValidationError("manifest feature_quality_column_count must be 45")
    if tuple(manifest["feature_column_names"]) != FEATURE_SCHEMA_V002:
        raise Phase4bnSValidationError("manifest feature_column_names != FEATURE_SCHEMA_V002")
    if manifest["base_commit_sha"] != BASE_COMMIT_SHA_4BN_R_FINAL:
        raise Phase4bnSValidationError(
            "manifest base_commit_sha must equal BASE_SHA_4BN_R_FINAL"
        )

    # Non-eligible posture (Phase 4bn-R non-eligible-source precondition).
    if manifest["research_eligible"] is not False:
        raise Phase4bnSValidationError("manifest research_eligible must be False")
    if manifest["eligibility_gate_status"] != "pending":
        raise Phase4bnSValidationError("manifest eligibility_gate_status must be 'pending'")
    if manifest["no_successor_authorization"] is not True:
        raise Phase4bnSValidationError("manifest no_successor_authorization must be True")
    if manifest["source_eligibility_posture"] != "non_eligible_gate_passed_pending":
        raise Phase4bnSValidationError(
            "manifest source_eligibility_posture must be 'non_eligible_gate_passed_pending'"
        )
    if manifest["v002_terminal_window_mode"] != "by_reference":
        raise Phase4bnSValidationError("manifest v002_terminal_window_mode must be 'by_reference'")

    gov = manifest["governance_labels"]
    for key in ("labels", "ml", "strategy", "backtest"):
        if gov.get(key) != "forbidden":
            raise Phase4bnSValidationError(f"governance label {key!r} must be 'forbidden'")
    if gov.get("acquisition") != "unauthorized":
        raise Phase4bnSValidationError("governance label 'acquisition' must be 'unauthorized'")

    bc = manifest["boundary_confirmations"]
    if set(bc) != set(REQUIRED_V002_BOUNDARY_CONFIRMATIONS) or not all(bc.values()):
        raise Phase4bnSValidationError(
            "boundary_confirmations must be the 18-key set, all True"
        )
    if (
        "no_future_lookahead" not in bc
        or "phase_4aw_flip_research_eligible_invariant_preserved" not in bc
    ):
        raise Phase4bnSValidationError(
            "boundary_confirmations missing required no_future_lookahead / 4aw invariant key"
        )
    na = manifest["non_authorization_flags"]
    if set(na) != set(REQUIRED_V002_NON_AUTHORIZATION_FLAGS) or any(na.values()):
        raise Phase4bnSValidationError(
            "non_authorization_flags must be the 8-key set, all False"
        )
    if "successor_authorization_after" not in na:
        raise Phase4bnSValidationError(
            "non_authorization_flags missing successor_authorization_after"
        )

    ref = manifest["existing_v002_feature_reference"]
    if ref.get("read") is not False or ref.get("mutated") is not False:
        raise Phase4bnSValidationError("existing_v002_feature_reference must be read/mutated False")
    term = manifest["existing_v002_terminal_window"]
    if term.get("read") is not False or term.get("normalized_dates_read") is not False:
        raise Phase4bnSValidationError(
            "existing_v002_terminal_window read / normalized_dates_read must be False"
        )
    if manifest["sealed_test_split_touched"] is not False:
        raise Phase4bnSValidationError("sealed_test_split_touched must be False")
    if manifest["test_rows_loaded"] != 0 or manifest["test_holdout_touched"] is not False:
        raise Phase4bnSValidationError("test holdout must be untouched (rows_loaded=0)")

    # Forbidden field-name scan (recursive over keys). The three explicitly
    # validated declaration subtrees are not rescanned.
    def _scan(obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                low = str(k).lower()
                for needle in FORBIDDEN_MANIFEST_KEY_SUBSTRINGS:
                    if needle in low:
                        raise Phase4bnSValidationError(
                            f"forbidden manifest field substring {needle!r} in key {k!r}"
                        )
                if k in _DECLARATION_SUBTREES:
                    continue
                _scan(v)
        elif isinstance(obj, list):
            for item in obj:
                _scan(item)

    _scan(manifest)


def _atomic_write_segment_manifest(
    path: Path, obj: Mapping[str, Any], *, refuse_overwrite: bool = True
) -> tuple[str, int]:
    """Atomic write of the feature segment manifest under manifests/."""
    return atomic_write_feature_manifest(path, obj, refuse_overwrite=refuse_overwrite)


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------


@dataclass
class OrchestrationResult:
    """Top-level result of one Phase 4bn-S feature execution run."""

    overall_status: str  # "pass" | "fail_closed"
    output_manifest_path: Path | None
    output_manifest_sha256: str | None
    output_manifest_sidecar_path: Path | None
    output_manifest_sidecar_sha256: str | None
    produced_file_count: int
    total_feature_row_count: int
    total_feature_footprint_bytes: int
    per_day_records: list[PerDayFeatureRecord]
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
    segment_manifest_path: Path,
    gate_report_path: Path,
    features_root: Path,
    manifests_root: Path,
    repo_root: Path,
    refuse_overwrite: bool = True,
    code_commit_sha: str | None = None,
    base_commit_sha: str | None = None,
) -> OrchestrationResult:
    """Run the full Phase 4bn-S feature execution once. Fail-closed on any breach."""
    start = time.monotonic()
    checks: list[CheckResult] = []
    per_day_records: list[PerDayFeatureRecord] = []
    warnings_crossed: list[str] = []
    running_feature_bytes = 0
    temp_pre_cleanup_peak = 0
    d_free_min_observed = _disk_free_bytes(features_root)

    assert_path_under_data_microstructure(features_root, label="features_root")
    assert_manifest_output_path_under_manifests(
        manifests_root / "x.json", label="manifests_root probe"
    )

    # Locked-schema integrity + forbidden-column guard (defence in depth).
    if tuple(LINEAGE_COLUMNS_V002) + tuple(FEATURE_NAMES_V002) != FEATURE_SCHEMA_V002:
        raise Phase4bnSValidationError("FEATURE_SCHEMA_V002 composition drifted")
    if len(FEATURE_SCHEMA_V002) != 62:
        raise Phase4bnSValidationError("FEATURE_SCHEMA_V002 is not 62 columns")
    assert_no_forbidden_substrings_v002(FEATURE_SCHEMA_V002)

    try:
        artefacts = verify_preconditions(
            segment_manifest_path=segment_manifest_path,
            gate_report_path=gate_report_path,
            repo_root=repo_root,
            checks=checks,
        )
        preflight = run_preflight(
            artefacts=artefacts, features_root=features_root, checks=checks
        )
        d_free_min_observed = min(d_free_min_observed, preflight.d_free_bytes)

        commit_sha = code_commit_sha or _git_head_sha(repo_root)
        base_sha = base_commit_sha or BASE_COMMIT_SHA_4BN_R_FINAL

        # Build the locked feature config (deterministic config hash).
        manifest_out_path = manifests_root / SEGMENT_MANIFEST_BASENAME
        config = build_feature_config_v002(
            source_normalized_manifest_path=str(
                artefacts.segment_manifest_path.resolve()
                .relative_to(repo_root.resolve())
                .as_posix()
            ),
            source_successor_state_path=NO_SUCCESSOR_STATE_SENTINEL,
            output_feature_manifest_path=str(
                manifest_out_path.resolve().relative_to(repo_root.resolve()).as_posix()
            )
            if _is_relative_to(manifest_out_path.resolve(), repo_root.resolve())
            else str(manifest_out_path),
            output_feature_root_dir=str(
                features_root.resolve().relative_to(repo_root.resolve()).as_posix()
            )
            if _is_relative_to(features_root.resolve(), repo_root.resolve())
            else str(features_root),
            code_commit_sha=commit_sha,
        )

        lineage_const = {
            "normalized_manifest_sha256": artefacts.segment_manifest_sha_before,
            "gate_report_sha256": artefacts.gate_report_sha_before,
            "successor_state_sentinel": NO_SUCCESSOR_STATE_SENTINEL,
        }

        # Refuse-to-overwrite check for manifest + all per-day outputs.
        manifest_sidecar_path = manifest_out_path.with_suffix(
            manifest_out_path.suffix + ".sha256"
        )
        for label, p in (
            ("feature segment manifest", manifest_out_path),
            ("feature segment manifest sidecar", manifest_sidecar_path),
        ):
            if p.exists():
                raise Phase4bnSValidationError(f"refuse-to-overwrite: {label} exists at {p}")
        for src in artefacts.per_day_sources:
            out_p = _derive_feature_parquet_path(
                features_root=features_root, symbol=SYMBOL, utc_date=src.date
            )
            if out_p.exists() or out_p.with_suffix(out_p.suffix + ".sha256").exists():
                raise Phase4bnSValidationError(
                    f"refuse-to-overwrite: feature output already exists at {out_p}"
                )

        # Per-day computation.
        prev_month = None
        for i, src in enumerate(artefacts.per_day_sources):
            prior = artefacts.per_day_sources[i - 1] if i > 0 else None
            record, parquet_size = _compute_one_day(
                day=src,
                prior_day=prior,
                features_root=features_root,
                config=config,
                lineage_const=lineage_const,
                repo_root=repo_root,
            )
            per_day_records.append(record)
            running_feature_bytes += (
                record.feature_parquet_size_bytes + record.feature_sidecar_size_bytes
            )
            temp_pre_cleanup_peak = max(temp_pre_cleanup_peak, parquet_size)

            elapsed = time.monotonic() - start
            d_free = _disk_free_bytes(features_root)
            d_free_min_observed = min(d_free_min_observed, d_free)
            _enforce_budgets(
                running_feature_bytes=running_feature_bytes,
                elapsed=elapsed,
                d_free=d_free,
                temp_peak=temp_pre_cleanup_peak,
                warnings_crossed=warnings_crossed,
            )
            month = src.date[:7]
            if month != prev_month:
                checks.append(
                    CheckResult(
                        f"4bn-S.month.{month}",
                        f"month {month} boundary budget OK",
                        "pass",
                        f"feat={running_feature_bytes / GIB:.2f} GiB; "
                        f"D_free={d_free / GIB:.0f} GiB; elapsed={elapsed:.0f}s",
                    )
                )
                prev_month = month

        # Aggregate checks.
        if len(per_day_records) != EXPECTED_DATE_COUNT:
            raise Phase4bnSValidationError(
                f"produced_file_count {len(per_day_records)} != {EXPECTED_DATE_COUNT}"
            )
        total_rows = sum(r.row_count for r in per_day_records)
        if total_rows != EXPECTED_TOTAL_EVENT_COUNT:
            raise Phase4bnSValidationError(
                f"total feature row count {total_rows} != {EXPECTED_TOTAL_EVENT_COUNT}"
            )
        checks.append(
            CheckResult(
                "4bn-S.aggregate",
                "produced 275 feature parquets; total rows == source events",
                "pass",
                str(total_rows),
            )
        )

        budget_witnesses: dict[str, Any] = {
            "feature_warn_bytes": FEATURE_WARN_BYTES,
            "feature_hard_bytes": FEATURE_HARD_BYTES,
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
            "measured_feature_footprint_bytes": running_feature_bytes,
            "measured_temp_footprint_pre_cleanup_bytes": temp_pre_cleanup_peak,
            "measured_temp_footprint_post_cleanup_bytes": 0,
            "measured_runtime_seconds": time.monotonic() - start,
            "preflight_estimated_feature_bytes": preflight.estimated_feature_bytes,
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
            feature_config_hash=config.feature_config_hash,
            created_at_unix_ms=now_unix_ms,
            created_at_utc=now_utc,
            total_feature_footprint_bytes=running_feature_bytes,
            total_feature_row_count=total_rows,
            budget_witnesses=budget_witnesses,
            repo_root=repo_root,
        )
        assert_manifest_field_contract(manifest_dict)
        checks.append(
            CheckResult("4bn-S.manifest", "feature segment manifest field contract OK", "pass")
        )

        manifest_sha, _ = _atomic_write_segment_manifest(
            manifest_out_path, manifest_dict, refuse_overwrite=refuse_overwrite
        )
        manifest_sidecar_sha, _ = write_feature_sha256_sidecar(
            manifest_sidecar_path,
            target_filename=manifest_out_path.name,
            sha256_hex=manifest_sha,
            refuse_overwrite=refuse_overwrite,
        )
        checks.append(
            CheckResult("4bn-S.write", "feature segment manifest + sidecar written", "pass")
        )

        # Post-write source immutability re-hash (fail closed on drift).
        for label, p, want in (
            (
                "normalized segment manifest",
                artefacts.segment_manifest_path,
                artefacts.segment_manifest_sha_before,
            ),
            (
                "normalized-layer gate report",
                artefacts.gate_report_path,
                artefacts.gate_report_sha_before,
            ),
        ):
            actual, _ = _sha256_file(p)
            if actual != want:
                raise Phase4bnSValidationError(
                    f"POST-WRITE source immutability violation for {label}: "
                    f"expected {want} got {actual}"
                )
        for src in artefacts.per_day_sources:
            actual, _ = _sha256_file(src.parquet_path)
            if actual != src.parquet_sha256:
                raise Phase4bnSValidationError(
                    f"POST-WRITE normalized parquet mutated for {src.date}"
                )
        checks.append(
            CheckResult("4bn-S.immutability", "all source inputs byte-identical pre/post", "pass")
        )

        return OrchestrationResult(
            overall_status="pass",
            output_manifest_path=manifest_out_path,
            output_manifest_sha256=manifest_sha,
            output_manifest_sidecar_path=manifest_sidecar_path,
            output_manifest_sidecar_sha256=manifest_sidecar_sha,
            produced_file_count=len(per_day_records),
            total_feature_row_count=total_rows,
            total_feature_footprint_bytes=running_feature_bytes,
            per_day_records=per_day_records,
            checks=checks,
            budget_witnesses=budget_witnesses,
            wall_clock_seconds=time.monotonic() - start,
            warning_thresholds_crossed=warnings_crossed,
            hard_caps_crossed=False,
            result_state=(
                "FEATURE_EXECUTION_SUCCEEDED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED"
            ),
        )
    except Phase4bnSOrchestrationError as exc:
        failed_id = checks[-1].check_id if checks else "4bn-S.precondition"
        return OrchestrationResult(
            overall_status="fail_closed",
            output_manifest_path=None,
            output_manifest_sha256=None,
            output_manifest_sidecar_path=None,
            output_manifest_sidecar_sha256=None,
            produced_file_count=len(per_day_records),
            total_feature_row_count=sum(r.row_count for r in per_day_records),
            total_feature_footprint_bytes=running_feature_bytes,
            per_day_records=per_day_records,
            checks=checks,
            budget_witnesses={},
            wall_clock_seconds=time.monotonic() - start,
            warning_thresholds_crossed=warnings_crossed,
            hard_caps_crossed="hard cap" in str(exc).lower(),
            failed_check_id=failed_id,
            failure_message=str(exc),
            result_state="FEATURE_EXECUTION_PARTIAL__FAIL_CLOSED__REMAIN_PAUSED"
            if per_day_records
            else "FEATURE_EXECUTION_NOT_RUN__PREFLIGHT_OR_PRECONDITION_FAIL__REMAIN_PAUSED",
        )


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Phase 4bn-S — Feature-Only Pre-V002 BTCUSDT aggTrades Segment Execution. "
            "Bounded, offline, local-gitignored, non-eligible feature segment generator."
        )
    )
    p.add_argument("--repo-root", type=Path, default=_REPO_ROOT)
    p.add_argument(
        "--source-manifest",
        type=Path,
        default=None,
        help="Phase 4bn-O normalized segment manifest (default: locked rel path)",
    )
    p.add_argument(
        "--gate-report",
        type=Path,
        default=None,
        help="Phase 4bn-P normalized-layer gate report (default: locked rel path)",
    )
    p.add_argument("--features-root", type=Path, default=None)
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
        raise Phase4bnSOrchestrationError(
            f"repo_root does not look like the Prometheus repo: {repo_root}"
        )
    segment_manifest_path = (
        args.source_manifest or repo_root / DEFAULT_NORMALIZED_SEGMENT_MANIFEST_REL
    ).resolve()
    gate_report_path = (
        args.gate_report or repo_root / DEFAULT_NORMALIZED_GATE_REPORT_REL
    ).resolve()
    features_root = (
        args.features_root or repo_root / DEFAULT_FEATURES_ROOT_REL
    ).resolve()
    manifests_root = (
        args.manifests_root or repo_root / DEFAULT_MANIFESTS_ROOT_REL
    ).resolve()
    features_root.mkdir(parents=True, exist_ok=True)
    manifests_root.mkdir(parents=True, exist_ok=True)

    print(f"[phase-4bn-s] repo_root        : {repo_root}", flush=True)
    print(f"[phase-4bn-s] source_manifest  : {segment_manifest_path}", flush=True)
    print(f"[phase-4bn-s] gate_report      : {gate_report_path}", flush=True)
    print(f"[phase-4bn-s] features_root    : {features_root}", flush=True)
    print(f"[phase-4bn-s] manifests_root   : {manifests_root}", flush=True)
    print(f"[phase-4bn-s] dry_run          : {args.dry_run}", flush=True)

    if args.dry_run:
        checks: list[CheckResult] = []
        artefacts = verify_preconditions(
            segment_manifest_path=segment_manifest_path,
            gate_report_path=gate_report_path,
            repo_root=repo_root,
            checks=checks,
        )
        run_preflight(artefacts=artefacts, features_root=features_root, checks=checks)
        for c in checks:
            print(f"[phase-4bn-s]   {c.status.upper():4s} {c.check_id}: {c.title}", flush=True)
        print("[phase-4bn-s] dry-run complete; exiting before compute / write", flush=True)
        return 0

    result = run(
        segment_manifest_path=segment_manifest_path,
        gate_report_path=gate_report_path,
        features_root=features_root,
        manifests_root=manifests_root,
        repo_root=repo_root,
        refuse_overwrite=True,
        code_commit_sha=args.code_commit_sha,
        base_commit_sha=args.base_commit_sha,
    )
    for c in result.checks:
        print(f"[phase-4bn-s]   {c.status.upper():4s} {c.check_id}: {c.title}", flush=True)
    if result.overall_status != "pass":
        print(
            f"[phase-4bn-s] FAIL_CLOSED at {result.failed_check_id}: "
            f"{result.failure_message}",
            file=sys.stderr,
            flush=True,
        )
        return 2
    print(
        f"[phase-4bn-s] DONE produced={result.produced_file_count} "
        f"rows={result.total_feature_row_count} "
        f"footprint={result.total_feature_footprint_bytes / GIB:.2f} GiB "
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
    except Phase4bnSOrchestrationError as exc:
        print(f"[phase-4bn-s] FAIL_CLOSED: {exc}", file=sys.stderr, flush=True)
        sys.exit(2)
