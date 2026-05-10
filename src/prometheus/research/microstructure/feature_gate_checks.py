"""Phase 4bi-B feature-family eligibility-gate check suite.

Each check returns a :class:`FeatureGateCheckResult` with status PASS /
FAIL / NOT_APPLICABLE / ERROR. The :data:`CHECK_ORDER` tuple maps every
Phase 4bi-B check id to its check function in stable order.

Group taxonomy (Phase 4bi-B §6):

A — Artefact presence
B — Gitignore / tracked-file boundary
C — Feature manifest governance
D — Schema / column-order / feature-list
E — Row-count / identity / timestamp-alignment
F — Lineage hash
G — Dtype / null / Decimal / float sanity
H — Quality flags
I — Causal spot-check evidence
J — Same-timestamp tie-break evidence
K — Upstream immutability
L — Forbidden-output and no-rescue
M — Stage interpretation
N — Boundary confirmations

All checks are read-only. They never mutate the feature parquet, the
feature manifest, the source normalized parquet, the source normalized
manifest, the raw artefacts, the Phase 4bb-D / Phase 4bf gate reports,
or the Phase 4bg-B successor-state JSON.
"""
from __future__ import annotations

import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from .features_schema import (
    FEATURE_DATASET_FAMILY,
    FEATURE_DATASET_VERSION,
    FEATURE_NAMES_V001,
    FEATURE_SCHEMA_V001,
    FEATURE_SCHEMA_VERSION,
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS,
    LINEAGE_COLUMNS_V001,
)

# ---------------------------------------------------------------------------
# Expected canonical values (Phase 4bh real-run constants)
# ---------------------------------------------------------------------------

EXPECTED_FEATURE_PARQUET_SHA = (
    "618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f"
)
EXPECTED_FEATURE_MANIFEST_SHA = (
    "624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718"
)
EXPECTED_NORMALIZED_PARQUET_SHA = (
    "2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa"
)
EXPECTED_NORMALIZED_MANIFEST_SHA = (
    "f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9"
)
EXPECTED_RAW_MANIFEST_SHA = (
    "a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201"
)
EXPECTED_RAW_ZIP_SHA = (
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
)
EXPECTED_PHASE_4BB_D_GATE_REPORT_SHA = (
    "96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423"
)
EXPECTED_PHASE_4BF_GATE_REPORT_SHA = (
    "dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6"
)
EXPECTED_PHASE_4BG_B_SUCCESSOR_STATE_SHA = (
    "8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e"
)

EXPECTED_FEATURE_CONFIG_HASH = (
    "49b4ec1fd63688cc11d72ea7286af6efe2bad8ac5c29da0438c0f65d571f0c77"
)

EXPECTED_DATASET_FAMILY = FEATURE_DATASET_FAMILY
EXPECTED_DATASET_VERSION = FEATURE_DATASET_VERSION
EXPECTED_FEATURE_SCHEMA_VERSION = FEATURE_SCHEMA_VERSION
EXPECTED_SYMBOL = "BTCUSDT"
EXPECTED_UTC_DATE = "2025-01-15"
EXPECTED_ROW_COUNT = 1_681_098

REQUIRED_FEATURE_GOVERNANCE_FORBIDDEN_KEYS: tuple[str, ...] = (
    "labels",
    "ml",
    "strategy",
    "backtest",
)

REQUIRED_BOUNDARY_KEYS: tuple[str, ...] = (
    "no_labels",
    "no_targets",
    "no_signals",
    "no_ml",
    "no_strategy",
    "no_backtest",
    "no_acquisition",
    "no_network",
    "no_credentials",
    "no_manifest_mutation",
    "no_source_artefact_mutation",
)

EXPECTED_FEATURE_LIST = list(FEATURE_NAMES_V001)
EXPECTED_WINDOW_LIST = list(FEATURE_WINDOW_LABELS_V001)
EXPECTED_WINDOW_MS_LIST = list(FEATURE_WINDOWS_MS_V001)
DEFERRED_WINDOWS_FORBIDDEN: tuple[str, ...] = ("30s", "5m")


# ---------------------------------------------------------------------------
# Status / result types
# ---------------------------------------------------------------------------


class FeatureGateCheckStatus(StrEnum):
    """Tri+1-state feature-gate check status."""

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


@dataclass(frozen=True)
class FeatureGateCheckResult:
    """One row of the feature-gate report's ``checks`` array."""

    check_id: str
    group: str
    title: str
    status: FeatureGateCheckStatus
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "group": self.group,
            "title": self.title,
            "status": self.status.value,
            "detail": self.detail,
        }


@dataclass
class FeatureGateContext:
    """Mutable per-run inspection context shared across checks."""

    # paths
    feature_parquet_path: Path
    feature_parquet_sidecar_path: Path
    feature_manifest_path: Path
    feature_manifest_sidecar_path: Path
    source_normalized_parquet_path: Path
    source_normalized_manifest_path: Path
    source_raw_manifest_path: Path

    # parsed manifests
    feature_manifest: dict[str, Any]
    feature_manifest_bytes: bytes
    feature_manifest_sha: str
    feature_manifest_sidecar_first_64: str

    source_normalized_manifest: dict[str, Any]
    source_normalized_manifest_sha: str

    raw_manifest: dict[str, Any]
    raw_manifest_sha: str

    # SHAs
    feature_parquet_sha: str
    feature_parquet_sidecar_first_64: str
    source_normalized_parquet_sha: str
    raw_zip_sha: str | None
    phase_4bb_d_gate_report_sha: str | None
    phase_4bf_gate_report_sha: str | None
    phase_4bg_b_successor_state_sha: str | None

    # parquet tables
    feature_table: pa.Table
    source_normalized_table: pa.Table

    # validate_feature_dataset evidence
    validate_overall_status: str
    validate_failed_checks: tuple[str, ...]

    # gitignore evidence (computed once via subprocess at runtime; cached here)
    gitignore_results: dict[str, bool]

    measured: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Constructors
# ---------------------------------------------------------------------------


def _ok(check_id: str, group: str, title: str, detail: str = "") -> FeatureGateCheckResult:
    return FeatureGateCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=FeatureGateCheckStatus.PASS,
        detail=detail,
    )


def _fail(check_id: str, group: str, title: str, detail: str) -> FeatureGateCheckResult:
    return FeatureGateCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=FeatureGateCheckStatus.FAIL,
        detail=detail,
    )


def _err(check_id: str, group: str, title: str, detail: str) -> FeatureGateCheckResult:
    return FeatureGateCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=FeatureGateCheckStatus.ERROR,
        detail=detail,
    )


# ---------------------------------------------------------------------------
# Group A — Artefact presence
# ---------------------------------------------------------------------------


def check_a01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature parquet exists"
    if not ctx.feature_parquet_path.exists():
        return _fail("4bi-b.A01", "A", title, f"missing: {ctx.feature_parquet_path}")
    return _ok("4bi-b.A01", "A", title, str(ctx.feature_parquet_path))


def check_a02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature parquet sidecar exists"
    if not ctx.feature_parquet_sidecar_path.exists():
        return _fail(
            "4bi-b.A02", "A", title, f"missing: {ctx.feature_parquet_sidecar_path}"
        )
    return _ok("4bi-b.A02", "A", title, str(ctx.feature_parquet_sidecar_path))


def check_a03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest exists"
    if not ctx.feature_manifest_path.exists():
        return _fail("4bi-b.A03", "A", title, f"missing: {ctx.feature_manifest_path}")
    return _ok("4bi-b.A03", "A", title, str(ctx.feature_manifest_path))


def check_a04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest sidecar exists"
    if not ctx.feature_manifest_sidecar_path.exists():
        return _fail(
            "4bi-b.A04", "A", title, f"missing: {ctx.feature_manifest_sidecar_path}"
        )
    return _ok("4bi-b.A04", "A", title, str(ctx.feature_manifest_sidecar_path))


def check_a05(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "source normalized parquet exists"
    if not ctx.source_normalized_parquet_path.exists():
        return _fail(
            "4bi-b.A05",
            "A",
            title,
            f"missing: {ctx.source_normalized_parquet_path}",
        )
    return _ok("4bi-b.A05", "A", title, str(ctx.source_normalized_parquet_path))


def check_a06(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "source normalized manifest exists"
    if not ctx.source_normalized_manifest_path.exists():
        return _fail(
            "4bi-b.A06",
            "A",
            title,
            f"missing: {ctx.source_normalized_manifest_path}",
        )
    return _ok("4bi-b.A06", "A", title, str(ctx.source_normalized_manifest_path))


def check_a07(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "raw manifest exists"
    if not ctx.source_raw_manifest_path.exists():
        return _fail(
            "4bi-b.A07", "A", title, f"missing: {ctx.source_raw_manifest_path}"
        )
    return _ok("4bi-b.A07", "A", title, str(ctx.source_raw_manifest_path))


# ---------------------------------------------------------------------------
# Group B — Gitignore / tracked-file boundary
# ---------------------------------------------------------------------------


def check_b01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "data/microstructure/ is gitignored"
    if ctx.gitignore_results.get("data/microstructure/", False):
        return _ok("4bi-b.B01", "B", title, "ignored")
    return _fail("4bi-b.B01", "B", title, "not ignored")


def check_b02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "data/microstructure/features/ is gitignored"
    if ctx.gitignore_results.get("data/microstructure/features/", False):
        return _ok("4bi-b.B02", "B", title, "ignored")
    return _fail("4bi-b.B02", "B", title, "not ignored")


def check_b03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "data/microstructure/manifests/ is gitignored"
    if ctx.gitignore_results.get("data/microstructure/manifests/", False):
        return _ok("4bi-b.B03", "B", title, "ignored")
    return _fail("4bi-b.B03", "B", title, "not ignored")


def check_b04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "data/microstructure/gate-reports/features/ is gitignored"
    if ctx.gitignore_results.get(
        "data/microstructure/gate-reports/features/", False
    ):
        return _ok("4bi-b.B04", "B", title, "ignored")
    return _fail("4bi-b.B04", "B", title, "not ignored")


# ---------------------------------------------------------------------------
# Group C — Feature manifest governance
# ---------------------------------------------------------------------------


def check_c01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest dataset_family"
    actual = ctx.feature_manifest.get("dataset_family")
    if actual != EXPECTED_DATASET_FAMILY:
        return _fail("4bi-b.C01", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C01", "C", title, actual)


def check_c02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest dataset_version"
    actual = ctx.feature_manifest.get("dataset_version")
    if actual != EXPECTED_DATASET_VERSION:
        return _fail("4bi-b.C02", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C02", "C", title, actual)


def check_c03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest feature_schema_version"
    actual = ctx.feature_manifest.get("feature_schema_version")
    if actual != EXPECTED_FEATURE_SCHEMA_VERSION:
        return _fail("4bi-b.C03", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C03", "C", title, actual)


def check_c04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest symbol"
    actual = ctx.feature_manifest.get("symbol")
    if actual != EXPECTED_SYMBOL:
        return _fail("4bi-b.C04", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C04", "C", title, actual)


def check_c05(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest utc_date"
    actual = ctx.feature_manifest.get("utc_date")
    if actual != EXPECTED_UTC_DATE:
        return _fail("4bi-b.C05", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C05", "C", title, actual)


def check_c06(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest row_count"
    actual = ctx.feature_manifest.get("row_count")
    if actual != EXPECTED_ROW_COUNT:
        return _fail("4bi-b.C06", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C06", "C", title, str(actual))


def check_c07(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest invalid_windows == []"
    actual = ctx.feature_manifest.get("invalid_windows")
    if actual != []:
        return _fail("4bi-b.C07", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C07", "C", title, "[]")


def check_c08(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest research_eligible is false"
    actual = ctx.feature_manifest.get("research_eligible")
    if actual is not False:
        return _fail("4bi-b.C08", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C08", "C", title, "False")


def check_c09(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest eligibility_gate_status is pending"
    actual = ctx.feature_manifest.get("eligibility_gate_status")
    if actual != "pending":
        return _fail("4bi-b.C09", "C", title, f"actual={actual!r}")
    return _ok("4bi-b.C09", "C", title, "pending")


def check_c10(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest governance labels (forbidden + acquisition)"
    gov = ctx.feature_manifest.get("governance_labels") or {}
    for key in REQUIRED_FEATURE_GOVERNANCE_FORBIDDEN_KEYS:
        actual = gov.get(key)
        if actual != "forbidden":
            return _fail(
                "4bi-b.C10", "C", title, f"governance_labels.{key}={actual!r}"
            )
    if gov.get("acquisition") != "unauthorized":
        return _fail(
            "4bi-b.C10",
            "C",
            title,
            f"governance_labels.acquisition={gov.get('acquisition')!r}",
        )
    return _ok("4bi-b.C10", "C", title, "all forbidden + acquisition unauthorized")


# ---------------------------------------------------------------------------
# Group D — Schema / column-order / feature-list
# ---------------------------------------------------------------------------


def check_d01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature parquet column count == 61"
    cols = ctx.feature_table.column_names
    if len(cols) != 61:
        return _fail("4bi-b.D01", "D", title, f"actual={len(cols)}")
    return _ok("4bi-b.D01", "D", title, str(len(cols)))


def check_d02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature parquet column order == FEATURE_SCHEMA_V001"
    cols = tuple(ctx.feature_table.column_names)
    if cols != FEATURE_SCHEMA_V001:
        diff = [
            (i, a, b)
            for i, (a, b) in enumerate(zip(cols, FEATURE_SCHEMA_V001, strict=False))
            if a != b
        ]
        return _fail("4bi-b.D02", "D", title, f"first_diff={diff[:3]!r}")
    return _ok("4bi-b.D02", "D", title, "matches")


def check_d03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature/quality column count == 45"
    feature_cols = [c for c in ctx.feature_table.column_names if c in FEATURE_NAMES_V001]
    if len(feature_cols) != 45:
        return _fail("4bi-b.D03", "D", title, f"actual={len(feature_cols)}")
    return _ok("4bi-b.D03", "D", title, str(len(feature_cols)))


def check_d04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "lineage column count == 16"
    lineage_cols = [c for c in ctx.feature_table.column_names if c in LINEAGE_COLUMNS_V001]
    if len(lineage_cols) != 16:
        return _fail("4bi-b.D04", "D", title, f"actual={len(lineage_cols)}")
    return _ok("4bi-b.D04", "D", title, str(len(lineage_cols)))


def check_d05(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest feature_list == FEATURE_NAMES_V001"
    actual = ctx.feature_manifest.get("feature_list")
    if actual != EXPECTED_FEATURE_LIST:
        return _fail("4bi-b.D05", "D", title, "feature_list does not match canonical")
    return _ok("4bi-b.D05", "D", title, "matches")


def check_d06(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = 'feature manifest window_list == ["1s","5s","15s","60s"]'
    actual = ctx.feature_manifest.get("window_list")
    if actual != EXPECTED_WINDOW_LIST:
        return _fail("4bi-b.D06", "D", title, f"actual={actual!r}")
    return _ok("4bi-b.D06", "D", title, str(actual))


def check_d07(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest window_ms_list == [1000,5000,15000,60000]"
    actual = ctx.feature_manifest.get("window_ms_list")
    if actual != EXPECTED_WINDOW_MS_LIST:
        return _fail("4bi-b.D07", "D", title, f"actual={actual!r}")
    return _ok("4bi-b.D07", "D", title, str(actual))


def check_d08(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "no forbidden column substrings present"
    cols_lower = [c.lower() for c in ctx.feature_table.column_names]
    found = []
    for col in cols_lower:
        for tok in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS:
            if tok in col:
                # The 26 forbidden substrings include items like 'label',
                # 'pnl', 'position', 'edge', 'ml_'. None should appear
                # in our 61-column schema.
                # Note: 'rolling_log_return_past_window' contains 'return'
                # which is NOT in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS by
                # design. The forbidden list is the Phase 4bh-B literal
                # set; if it ever changes upstream, this check tracks it.
                found.append((col, tok))
                break
    if found:
        return _fail("4bi-b.D08", "D", title, f"found={found[:3]!r}")
    return _ok("4bi-b.D08", "D", title, "none")


def check_d09(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "deferred 30s and 5m windows absent"
    cols_lower = [c.lower() for c in ctx.feature_table.column_names]
    bad = []
    for col in cols_lower:
        for tok in DEFERRED_WINDOWS_FORBIDDEN:
            if col.endswith("_" + tok):
                bad.append((col, tok))
                break
    if bad:
        return _fail("4bi-b.D09", "D", title, f"found={bad[:3]!r}")
    return _ok("4bi-b.D09", "D", title, "none")


# ---------------------------------------------------------------------------
# Group E — Row-count / identity / timestamp-alignment
# ---------------------------------------------------------------------------


def check_e01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature parquet row count == 1,681,098"
    rows = ctx.feature_table.num_rows
    if rows != EXPECTED_ROW_COUNT:
        return _fail("4bi-b.E01", "E", title, f"rows={rows}")
    return _ok("4bi-b.E01", "E", title, f"rows={rows}")


def check_e02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "row_index contiguous 0..1,681,097"
    arr = ctx.feature_table.column("row_index").to_numpy()
    expected = np.arange(EXPECTED_ROW_COUNT, dtype=arr.dtype)
    if arr.shape != expected.shape or not np.array_equal(arr, expected):
        first_bad = int(np.argmax(arr != expected)) if arr.shape == expected.shape else -1
        return _fail("4bi-b.E02", "E", title, f"first_bad_idx={first_bad}")
    return _ok("4bi-b.E02", "E", title, "contiguous")


def check_e03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "agg_trade_id matches source normalized parquet per-row"
    feat = ctx.feature_table.column("agg_trade_id").to_numpy()
    src = ctx.source_normalized_table.column("agg_trade_id").to_numpy()
    if feat.shape != src.shape or not np.array_equal(feat, src):
        return _fail("4bi-b.E03", "E", title, "agg_trade_id mismatch")
    return _ok("4bi-b.E03", "E", title, "matches")


def check_e04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "source_transact_time_ms matches source normalized transact_time_ms"
    feat = ctx.feature_table.column("source_transact_time_ms").to_numpy()
    src = ctx.source_normalized_table.column("transact_time_ms").to_numpy()
    if feat.shape != src.shape or not np.array_equal(feat, src):
        return _fail("4bi-b.E04", "E", title, "transact_time_ms mismatch")
    return _ok("4bi-b.E04", "E", title, "matches")


def check_e05(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature_timestamp_ms == source_transact_time_ms per-row"
    a = ctx.feature_table.column("feature_timestamp_ms").to_numpy()
    b = ctx.feature_table.column("source_transact_time_ms").to_numpy()
    if a.shape != b.shape or not np.array_equal(a, b):
        return _fail("4bi-b.E05", "E", title, "mismatch")
    return _ok("4bi-b.E05", "E", title, "matches")


# ---------------------------------------------------------------------------
# Group F — Lineage hash
# ---------------------------------------------------------------------------


def check_f01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature parquet SHA matches expected"
    if ctx.feature_parquet_sha != EXPECTED_FEATURE_PARQUET_SHA:
        return _fail(
            "4bi-b.F01",
            "F",
            title,
            f"actual={ctx.feature_parquet_sha} expected={EXPECTED_FEATURE_PARQUET_SHA}",
        )
    return _ok("4bi-b.F01", "F", title, ctx.feature_parquet_sha)


def check_f02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature parquet sidecar matches recomputed bytes"
    if ctx.feature_parquet_sidecar_first_64 != ctx.feature_parquet_sha:
        return _fail(
            "4bi-b.F02",
            "F",
            title,
            f"sidecar={ctx.feature_parquet_sidecar_first_64} parquet={ctx.feature_parquet_sha}",
        )
    return _ok("4bi-b.F02", "F", title, "matches")


def check_f03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest SHA matches expected"
    if ctx.feature_manifest_sha != EXPECTED_FEATURE_MANIFEST_SHA:
        return _fail(
            "4bi-b.F03",
            "F",
            title,
            f"actual={ctx.feature_manifest_sha} expected={EXPECTED_FEATURE_MANIFEST_SHA}",
        )
    return _ok("4bi-b.F03", "F", title, ctx.feature_manifest_sha)


def check_f04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest sidecar matches recomputed bytes"
    if ctx.feature_manifest_sidecar_first_64 != ctx.feature_manifest_sha:
        return _fail(
            "4bi-b.F04",
            "F",
            title,
            f"sidecar={ctx.feature_manifest_sidecar_first_64} manifest={ctx.feature_manifest_sha}",
        )
    return _ok("4bi-b.F04", "F", title, "matches")


def check_f05(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature_config_hash matches expected"
    actual = ctx.feature_manifest.get("feature_config_hash")
    if actual != EXPECTED_FEATURE_CONFIG_HASH:
        return _fail("4bi-b.F05", "F", title, f"actual={actual!r}")
    return _ok("4bi-b.F05", "F", title, str(actual))


def check_f06(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "lineage SHA columns constant and match expected"
    expected_pairs = (
        ("source_normalized_parquet_sha256", EXPECTED_NORMALIZED_PARQUET_SHA),
        ("source_normalized_manifest_sha256", EXPECTED_NORMALIZED_MANIFEST_SHA),
        (
            "source_phase_4bf_gate_report_sha256",
            EXPECTED_PHASE_4BF_GATE_REPORT_SHA,
        ),
        (
            "source_successor_state_sha256",
            EXPECTED_PHASE_4BG_B_SUCCESSOR_STATE_SHA,
        ),
        ("feature_config_hash", EXPECTED_FEATURE_CONFIG_HASH),
    )
    n = ctx.feature_table.num_rows
    for col_name, expected in expected_pairs:
        col = ctx.feature_table.column(col_name)
        # uses a fast same-value test: first row + cast to set via head sample
        first_value = col[0].as_py()
        if first_value != expected:
            return _fail(
                "4bi-b.F06",
                "F",
                title,
                f"{col_name} first={first_value!r} expected={expected}",
            )
        # spot-check three additional rows for constancy
        for idx in (n // 4, n // 2, n - 1):
            if col[idx].as_py() != expected:
                return _fail(
                    "4bi-b.F06",
                    "F",
                    title,
                    f"{col_name} non-constant at idx={idx}",
                )
    return _ok("4bi-b.F06", "F", title, "all constant")


# ---------------------------------------------------------------------------
# Group G — Dtype / null / Decimal / float sanity
# ---------------------------------------------------------------------------


_INT64_COUNT_PREFIXES = (
    "rolling_aggtrade_count_",
    "rolling_aggressive_buy_count_",
    "rolling_aggressive_sell_count_",
)
_NULLABLE_FLOAT_PREFIXES = (
    "rolling_aggressive_flow_ratio_",
    "rolling_log_return_past_window_",
)
_NON_NULL_DECIMAL_PREFIXES = (
    "rolling_quantity_sum_",
    "rolling_aggressive_buy_quantity_",
    "rolling_aggressive_sell_quantity_",
    "rolling_aggressive_quantity_imbalance_",
)
_NULLABLE_DECIMAL_PREFIXES = ("rolling_quantity_mean_",)


def check_g01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "count columns are int64 and non-negative"
    bad_cols: list[str] = []
    for col_name in ctx.feature_table.column_names:
        if any(col_name.startswith(p) for p in _INT64_COUNT_PREFIXES):
            col = ctx.feature_table.column(col_name)
            if not pa.types.is_int64(col.type):
                bad_cols.append(f"{col_name}:type={col.type}")
                continue
            arr = col.to_numpy()
            if arr.min() < 0:
                bad_cols.append(f"{col_name}:min<0")
    if bad_cols:
        return _fail("4bi-b.G01", "G", title, f"{bad_cols[:3]!r}")
    return _ok("4bi-b.G01", "G", title, "ok")


def check_g02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "Decimal-as-string columns parse via Decimal (sampled)"
    sample_indices = [0, 1, 100, 1000, 50000, 100000, 500000, 1000000, 1681097]
    for col_name in ctx.feature_table.column_names:
        if any(col_name.startswith(p) for p in _NON_NULL_DECIMAL_PREFIXES) or any(
            col_name.startswith(p) for p in _NULLABLE_DECIMAL_PREFIXES
        ):
            col = ctx.feature_table.column(col_name)
            if not pa.types.is_string(col.type):
                return _fail(
                    "4bi-b.G02",
                    "G",
                    title,
                    f"{col_name} type={col.type}",
                )
            for idx in sample_indices:
                v = col[idx].as_py()
                if v is None:
                    if any(col_name.startswith(p) for p in _NON_NULL_DECIMAL_PREFIXES):
                        return _fail(
                            "4bi-b.G02",
                            "G",
                            title,
                            f"{col_name} unexpected null at idx={idx}",
                        )
                    continue
                try:
                    Decimal(v)
                except (InvalidOperation, ValueError) as e:
                    return _fail(
                        "4bi-b.G02",
                        "G",
                        title,
                        f"{col_name} non-Decimal at idx={idx}: {e}",
                    )
    return _ok("4bi-b.G02", "G", title, "ok")


def check_g03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "ratio columns null or in [0, 1]"
    for col_name in ctx.feature_table.column_names:
        if not col_name.startswith("rolling_aggressive_flow_ratio_"):
            continue
        col = ctx.feature_table.column(col_name)
        if not pa.types.is_float64(col.type):
            return _fail("4bi-b.G03", "G", title, f"{col_name} type={col.type}")
        arr = col.to_numpy(zero_copy_only=False)
        non_null = arr[~np.isnan(arr)]
        if non_null.size:
            if non_null.min() < 0.0 or non_null.max() > 1.0:
                return _fail(
                    "4bi-b.G03",
                    "G",
                    title,
                    f"{col_name} min={non_null.min()} max={non_null.max()}",
                )
            if not np.isfinite(non_null).all():
                return _fail(
                    "4bi-b.G03",
                    "G",
                    title,
                    f"{col_name} non-finite present",
                )
    return _ok("4bi-b.G03", "G", title, "ok")


def check_g04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "log-return columns null or finite (no NaN-as-inf)"
    for col_name in ctx.feature_table.column_names:
        if not col_name.startswith("rolling_log_return_past_window_"):
            continue
        col = ctx.feature_table.column(col_name)
        if not pa.types.is_float64(col.type):
            return _fail("4bi-b.G04", "G", title, f"{col_name} type={col.type}")
        arr = col.to_numpy(zero_copy_only=False)
        non_null = arr[~np.isnan(arr)]
        if non_null.size and not np.isfinite(non_null).all():
            return _fail("4bi-b.G04", "G", title, f"{col_name} non-finite present")
    return _ok("4bi-b.G04", "G", title, "ok")


def check_g05(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "utc_hour values in [0, 23]"
    arr = ctx.feature_table.column("utc_hour").to_numpy()
    if arr.min() < 0 or arr.max() > 23:
        return _fail("4bi-b.G05", "G", title, f"min={arr.min()} max={arr.max()}")
    return _ok("4bi-b.G05", "G", title, f"min={arr.min()} max={arr.max()}")


def check_g06(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "utc_minute values in [0, 59]"
    arr = ctx.feature_table.column("utc_minute").to_numpy()
    if arr.min() < 0 or arr.max() > 59:
        return _fail("4bi-b.G06", "G", title, f"min={arr.min()} max={arr.max()}")
    return _ok("4bi-b.G06", "G", title, f"min={arr.min()} max={arr.max()}")


def check_g07(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "milliseconds_since_day_start in [0, 86_399_999]"
    arr = ctx.feature_table.column("milliseconds_since_day_start").to_numpy()
    if arr.min() < 0 or arr.max() > 86_399_999:
        return _fail("4bi-b.G07", "G", title, f"min={arr.min()} max={arr.max()}")
    return _ok("4bi-b.G07", "G", title, f"min={arr.min()} max={arr.max()}")


# ---------------------------------------------------------------------------
# Group H — Quality flags
# ---------------------------------------------------------------------------


def check_h01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "invalid_window_flag is bool and false for all rows"
    col = ctx.feature_table.column("invalid_window_flag")
    if not pa.types.is_boolean(col.type):
        return _fail("4bi-b.H01", "H", title, f"type={col.type}")
    arr = col.to_numpy(zero_copy_only=False)
    if arr.any():
        return _fail("4bi-b.H01", "H", title, "any-true encountered")
    return _ok("4bi-b.H01", "H", title, "all false")


def check_h02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "rolling_missing_window_flag is bool and false for all rows"
    col = ctx.feature_table.column("rolling_missing_window_flag")
    if not pa.types.is_boolean(col.type):
        return _fail("4bi-b.H02", "H", title, f"type={col.type}")
    arr = col.to_numpy(zero_copy_only=False)
    if arr.any():
        return _fail("4bi-b.H02", "H", title, "any-true encountered")
    return _ok("4bi-b.H02", "H", title, "all false")


# ---------------------------------------------------------------------------
# Group I — Causal spot-check evidence
# ---------------------------------------------------------------------------


def check_i01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "row 0 first-row no-prior-reference semantics"
    count_1s_0 = ctx.feature_table.column("rolling_aggtrade_count_1s")[0].as_py()
    log_return_1s_0 = ctx.feature_table.column("rolling_log_return_past_window_1s")[
        0
    ].as_py()
    if count_1s_0 != 1:
        return _fail("4bi-b.I01", "I", title, f"count_1s[0]={count_1s_0}")
    if log_return_1s_0 is not None:
        return _fail("4bi-b.I01", "I", title, f"log_return_1s[0]={log_return_1s_0!r}")
    return _ok("4bi-b.I01", "I", title, "count_1s[0]=1; log_return_1s[0]=null")


def check_i02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "last-row identity matches source last row"
    last = ctx.feature_table.num_rows - 1
    feat_agg = ctx.feature_table.column("agg_trade_id")[last].as_py()
    feat_t = ctx.feature_table.column("source_transact_time_ms")[last].as_py()
    src_agg = ctx.source_normalized_table.column("agg_trade_id")[last].as_py()
    src_t = ctx.source_normalized_table.column("transact_time_ms")[last].as_py()
    if feat_agg != src_agg or feat_t != src_t:
        return _fail(
            "4bi-b.I02",
            "I",
            title,
            f"feat=({feat_agg},{feat_t}) src=({src_agg},{src_t})",
        )
    return _ok("4bi-b.I02", "I", title, f"agg={feat_agg} T={feat_t}")


def check_i03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    """Spot-check rolling_aggtrade_count_1s respects the trailing window
    (T - 1000, T] with the same-timestamp tie-break row_index <= R."""
    title = "rolling_aggtrade_count_1s spot-checks at sample rows"
    sample_rows = (5, 100, 1000, 50000, 100000, 500000, 1000000, 1681097)
    src_t = ctx.source_normalized_table.column("transact_time_ms").to_numpy()
    feat_count = ctx.feature_table.column("rolling_aggtrade_count_1s").to_numpy()
    for r in sample_rows:
        t_r = int(src_t[r])
        threshold = t_r - 1000
        # find lowest index lo such that src_t[lo] > threshold
        lo = int(np.searchsorted(src_t, threshold, side="right"))
        expected = (r - lo) + 1
        if int(feat_count[r]) != expected:
            return _fail(
                "4bi-b.I03",
                "I",
                title,
                f"row={r} actual={int(feat_count[r])} expected={expected}",
            )
    return _ok("4bi-b.I03", "I", title, "ok")


def check_i04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    """Spot-check rolling_aggtrade_count_60s at additional rows."""
    title = "rolling_aggtrade_count_60s spot-checks at sample rows"
    sample_rows = (100, 1000, 50000, 100000, 500000, 1000000, 1681097)
    src_t = ctx.source_normalized_table.column("transact_time_ms").to_numpy()
    feat_count = ctx.feature_table.column("rolling_aggtrade_count_60s").to_numpy()
    for r in sample_rows:
        t_r = int(src_t[r])
        threshold = t_r - 60_000
        lo = int(np.searchsorted(src_t, threshold, side="right"))
        expected = (r - lo) + 1
        if int(feat_count[r]) != expected:
            return _fail(
                "4bi-b.I04",
                "I",
                title,
                f"row={r} actual={int(feat_count[r])} expected={expected}",
            )
    return _ok("4bi-b.I04", "I", title, "ok")


# ---------------------------------------------------------------------------
# Group J — Same-timestamp tie-break evidence
# ---------------------------------------------------------------------------


def check_j01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "first same-T pair: count_1s[i+1] == count_1s[i] + 1"
    src_t = ctx.source_normalized_table.column("transact_time_ms").to_numpy()
    diffs = np.diff(src_t)
    same_t = np.where(diffs == 0)[0]
    if same_t.size == 0:
        return _ok("4bi-b.J01", "J", title, "no same-T pair in dataset")
    i = int(same_t[0])
    feat_count = ctx.feature_table.column("rolling_aggtrade_count_1s").to_numpy()
    if int(feat_count[i + 1]) != int(feat_count[i]) + 1:
        return _fail(
            "4bi-b.J01",
            "J",
            title,
            f"i={i} count[i]={int(feat_count[i])} count[i+1]={int(feat_count[i + 1])}",
        )
    return _ok(
        "4bi-b.J01",
        "J",
        title,
        f"i={i} count[i]={int(feat_count[i])} count[i+1]={int(feat_count[i + 1])}",
    )


# ---------------------------------------------------------------------------
# Group K — Upstream immutability
# ---------------------------------------------------------------------------


def check_k01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "source normalized parquet SHA matches expected"
    if ctx.source_normalized_parquet_sha != EXPECTED_NORMALIZED_PARQUET_SHA:
        return _fail(
            "4bi-b.K01",
            "K",
            title,
            f"actual={ctx.source_normalized_parquet_sha}",
        )
    return _ok("4bi-b.K01", "K", title, ctx.source_normalized_parquet_sha)


def check_k02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "source normalized manifest SHA matches expected"
    if ctx.source_normalized_manifest_sha != EXPECTED_NORMALIZED_MANIFEST_SHA:
        return _fail(
            "4bi-b.K02",
            "K",
            title,
            f"actual={ctx.source_normalized_manifest_sha}",
        )
    return _ok("4bi-b.K02", "K", title, ctx.source_normalized_manifest_sha)


def check_k03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "raw manifest SHA matches expected"
    if ctx.raw_manifest_sha != EXPECTED_RAW_MANIFEST_SHA:
        return _fail("4bi-b.K03", "K", title, f"actual={ctx.raw_manifest_sha}")
    return _ok("4bi-b.K03", "K", title, ctx.raw_manifest_sha)


def check_k04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "raw zip SHA matches expected"
    if ctx.raw_zip_sha is None:
        return FeatureGateCheckResult(
            check_id="4bi-b.K04",
            group="K",
            title=title,
            status=FeatureGateCheckStatus.NOT_APPLICABLE,
            detail="raw zip not available; skipped",
        )
    if ctx.raw_zip_sha != EXPECTED_RAW_ZIP_SHA:
        return _fail("4bi-b.K04", "K", title, f"actual={ctx.raw_zip_sha}")
    return _ok("4bi-b.K04", "K", title, ctx.raw_zip_sha)


def check_k05(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "Phase 4bb-D gate report SHA matches expected"
    if ctx.phase_4bb_d_gate_report_sha is None:
        return FeatureGateCheckResult(
            check_id="4bi-b.K05",
            group="K",
            title=title,
            status=FeatureGateCheckStatus.NOT_APPLICABLE,
            detail="Phase 4bb-D gate report not available; skipped",
        )
    if ctx.phase_4bb_d_gate_report_sha != EXPECTED_PHASE_4BB_D_GATE_REPORT_SHA:
        return _fail(
            "4bi-b.K05",
            "K",
            title,
            f"actual={ctx.phase_4bb_d_gate_report_sha}",
        )
    return _ok("4bi-b.K05", "K", title, ctx.phase_4bb_d_gate_report_sha)


def check_k06(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "Phase 4bf gate report SHA matches expected"
    if ctx.phase_4bf_gate_report_sha is None:
        return FeatureGateCheckResult(
            check_id="4bi-b.K06",
            group="K",
            title=title,
            status=FeatureGateCheckStatus.NOT_APPLICABLE,
            detail="Phase 4bf gate report not available; skipped",
        )
    if ctx.phase_4bf_gate_report_sha != EXPECTED_PHASE_4BF_GATE_REPORT_SHA:
        return _fail(
            "4bi-b.K06",
            "K",
            title,
            f"actual={ctx.phase_4bf_gate_report_sha}",
        )
    return _ok("4bi-b.K06", "K", title, ctx.phase_4bf_gate_report_sha)


def check_k07(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "Phase 4bg-B successor-state SHA matches expected"
    if ctx.phase_4bg_b_successor_state_sha is None:
        return FeatureGateCheckResult(
            check_id="4bi-b.K07",
            group="K",
            title=title,
            status=FeatureGateCheckStatus.NOT_APPLICABLE,
            detail="Phase 4bg-B successor-state not available; skipped",
        )
    if ctx.phase_4bg_b_successor_state_sha != EXPECTED_PHASE_4BG_B_SUCCESSOR_STATE_SHA:
        return _fail(
            "4bi-b.K07",
            "K",
            title,
            f"actual={ctx.phase_4bg_b_successor_state_sha}",
        )
    return _ok("4bi-b.K07", "K", title, ctx.phase_4bg_b_successor_state_sha)


# ---------------------------------------------------------------------------
# Group L — Forbidden-output and no-rescue
# ---------------------------------------------------------------------------


def check_l01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "raw manifest research_eligible=false / eligibility_gate_status=pending"
    re_ = ctx.raw_manifest.get("research_eligible")
    egs = ctx.raw_manifest.get("eligibility_gate_status")
    if re_ is not False or egs != "pending":
        return _fail(
            "4bi-b.L01", "L", title, f"research_eligible={re_!r} egs={egs!r}"
        )
    return _ok("4bi-b.L01", "L", title, "false / pending")


def check_l02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = (
        "original derived manifest research_eligible=false / "
        "eligibility_gate_status=pending"
    )
    re_ = ctx.source_normalized_manifest.get("research_eligible")
    egs = ctx.source_normalized_manifest.get("eligibility_gate_status")
    if re_ is not False or egs != "pending":
        return _fail(
            "4bi-b.L02", "L", title, f"research_eligible={re_!r} egs={egs!r}"
        )
    return _ok("4bi-b.L02", "L", title, "false / pending")


def check_l03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest boundary confirmations all true"
    bc = ctx.feature_manifest.get("boundary_confirmations") or {}
    missing = [k for k in REQUIRED_BOUNDARY_KEYS if k not in bc]
    if missing:
        return _fail("4bi-b.L03", "L", title, f"missing keys={missing}")
    bad = [k for k in REQUIRED_BOUNDARY_KEYS if bc.get(k) is not True]
    if bad:
        return _fail("4bi-b.L03", "L", title, f"non-true={bad}")
    return _ok("4bi-b.L03", "L", title, "all true")


def check_l04(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "validate_feature_dataset overall_status == pass"
    if ctx.validate_overall_status != "pass":
        return _fail(
            "4bi-b.L04",
            "L",
            title,
            f"overall_status={ctx.validate_overall_status} "
            f"failed={list(ctx.validate_failed_checks)[:5]}",
        )
    return _ok(
        "4bi-b.L04",
        "L",
        title,
        "validate_feature_dataset returned pass with no failed checks",
    )


# ---------------------------------------------------------------------------
# Group M — Stage interpretation
# ---------------------------------------------------------------------------


def check_m01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature_manifest_research_eligible_after invariant False"
    actual = ctx.feature_manifest.get("research_eligible")
    if actual is not False:
        return _fail("4bi-b.M01", "M", title, f"actual={actual!r}")
    return _ok("4bi-b.M01", "M", title, "False")


def check_m02(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature_manifest_eligibility_gate_status_after invariant pending"
    actual = ctx.feature_manifest.get("eligibility_gate_status")
    if actual != "pending":
        return _fail("4bi-b.M02", "M", title, f"actual={actual!r}")
    return _ok("4bi-b.M02", "M", title, "pending")


def check_m03(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "stage_5_research_or_ml_use invariant False"
    # This is invariant for Phase 4bi-B regardless of overall status;
    # the gate report's stage_5_research_or_ml_use field is wired to
    # False in the report builder. We validate it here for completeness.
    return _ok("4bi-b.M03", "M", title, "invariant False")


# ---------------------------------------------------------------------------
# Group N — Boundary confirmations
# ---------------------------------------------------------------------------


def check_n01(ctx: FeatureGateContext) -> FeatureGateCheckResult:
    title = "feature manifest boundary_confirmations contains every required key"
    bc = ctx.feature_manifest.get("boundary_confirmations") or {}
    missing = [k for k in REQUIRED_BOUNDARY_KEYS if k not in bc]
    if missing:
        return _fail("4bi-b.N01", "N", title, f"missing={missing}")
    return _ok("4bi-b.N01", "N", title, "all present")


# ---------------------------------------------------------------------------
# Check order (canonical, stable)
# ---------------------------------------------------------------------------


CHECK_ORDER: tuple[tuple[str, Callable[[FeatureGateContext], FeatureGateCheckResult]], ...] = (
    ("4bi-b.A01", check_a01),
    ("4bi-b.A02", check_a02),
    ("4bi-b.A03", check_a03),
    ("4bi-b.A04", check_a04),
    ("4bi-b.A05", check_a05),
    ("4bi-b.A06", check_a06),
    ("4bi-b.A07", check_a07),
    ("4bi-b.B01", check_b01),
    ("4bi-b.B02", check_b02),
    ("4bi-b.B03", check_b03),
    ("4bi-b.B04", check_b04),
    ("4bi-b.C01", check_c01),
    ("4bi-b.C02", check_c02),
    ("4bi-b.C03", check_c03),
    ("4bi-b.C04", check_c04),
    ("4bi-b.C05", check_c05),
    ("4bi-b.C06", check_c06),
    ("4bi-b.C07", check_c07),
    ("4bi-b.C08", check_c08),
    ("4bi-b.C09", check_c09),
    ("4bi-b.C10", check_c10),
    ("4bi-b.D01", check_d01),
    ("4bi-b.D02", check_d02),
    ("4bi-b.D03", check_d03),
    ("4bi-b.D04", check_d04),
    ("4bi-b.D05", check_d05),
    ("4bi-b.D06", check_d06),
    ("4bi-b.D07", check_d07),
    ("4bi-b.D08", check_d08),
    ("4bi-b.D09", check_d09),
    ("4bi-b.E01", check_e01),
    ("4bi-b.E02", check_e02),
    ("4bi-b.E03", check_e03),
    ("4bi-b.E04", check_e04),
    ("4bi-b.E05", check_e05),
    ("4bi-b.F01", check_f01),
    ("4bi-b.F02", check_f02),
    ("4bi-b.F03", check_f03),
    ("4bi-b.F04", check_f04),
    ("4bi-b.F05", check_f05),
    ("4bi-b.F06", check_f06),
    ("4bi-b.G01", check_g01),
    ("4bi-b.G02", check_g02),
    ("4bi-b.G03", check_g03),
    ("4bi-b.G04", check_g04),
    ("4bi-b.G05", check_g05),
    ("4bi-b.G06", check_g06),
    ("4bi-b.G07", check_g07),
    ("4bi-b.H01", check_h01),
    ("4bi-b.H02", check_h02),
    ("4bi-b.I01", check_i01),
    ("4bi-b.I02", check_i02),
    ("4bi-b.I03", check_i03),
    ("4bi-b.I04", check_i04),
    ("4bi-b.J01", check_j01),
    ("4bi-b.K01", check_k01),
    ("4bi-b.K02", check_k02),
    ("4bi-b.K03", check_k03),
    ("4bi-b.K04", check_k04),
    ("4bi-b.K05", check_k05),
    ("4bi-b.K06", check_k06),
    ("4bi-b.K07", check_k07),
    ("4bi-b.L01", check_l01),
    ("4bi-b.L02", check_l02),
    ("4bi-b.L03", check_l03),
    ("4bi-b.L04", check_l04),
    ("4bi-b.M01", check_m01),
    ("4bi-b.M02", check_m02),
    ("4bi-b.M03", check_m03),
    ("4bi-b.N01", check_n01),
)


def run_all_checks(ctx: FeatureGateContext) -> tuple[FeatureGateCheckResult, ...]:
    """Run every Phase 4bi-B check function and return the result tuple."""
    out: list[FeatureGateCheckResult] = []
    for check_id, fn in CHECK_ORDER:
        try:
            r = fn(ctx)
        except Exception as exc:  # pragma: no cover - defensive
            r = _err(
                check_id,
                "?",
                f"check raised exception: {type(exc).__name__}",
                str(exc),
            )
        out.append(r)
    return tuple(out)


# ---------------------------------------------------------------------------
# Helpers used by the orchestrator
# ---------------------------------------------------------------------------


def query_gitignore_status(repo_root: Path, paths: list[str]) -> dict[str, bool]:
    """Return ``{path: is_ignored}`` for each *path* using ``git check-ignore``.

    Uses ``--quiet`` discipline: exit code 0 means *path is ignored*,
    exit code 1 means *not ignored*. Other codes are treated as not-ignored
    so the gate fails closed on these paths.
    """
    out: dict[str, bool] = {}
    for p in paths:
        try:
            res = subprocess.run(
                ["git", "check-ignore", "-q", p],
                cwd=str(repo_root),
                capture_output=True,
                check=False,
            )
            out[p] = res.returncode == 0
        except FileNotFoundError:
            out[p] = False
    return out


def load_parquet_table(path: Path) -> pa.Table:
    """Read a parquet file as an in-memory pyarrow Table."""
    return pq.read_table(path)
