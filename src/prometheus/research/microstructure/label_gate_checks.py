"""Phase 4bj-E label-family eligibility-gate check suite.

Each check returns a :class:`LabelGateCheckResult` with status PASS /
FAIL / NOT_APPLICABLE / ERROR. The :data:`CHECK_ORDER` tuple maps every
Phase 4bj-E check id to its check function in stable order.

Group taxonomy:

A — Artefact presence
B — Gitignore / tracked-file boundary
C — Label manifest governance
D — Schema / column-order / label-list
E — Row-count / row-identity / row-alignment
F — Hash / lineage
G — Manifest scalar counts (invalid_price_row_count, censored_per_horizon)
H — Per-horizon flag-count parity (parquet vs manifest)
I — Dtype / value sanity
J — Pre/post immutability (no parquet / no manifest mutation during gate)
K — One-row-per-feature-row evidence (optional, vs source feature parquet)
L — Forbidden output / consistency / no-rescue
M — Stage interpretation (research_eligible / eligibility_gate_status)
N — Boundary confirmations
O — Chronological split policy

All checks are read-only. They never mutate the label parquet, the
label manifest, the source feature parquet, the source feature
manifest, the Phase 4bi-D successor-state JSON, the Phase 4bi-B
feature-family gate report, the normalized parquet, the original
derived manifest, the raw manifest, or the raw zip.
"""
from __future__ import annotations

import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from .labels_schema import (
    FORBIDDEN_LABEL_COLUMN_SUBSTRINGS,
    LABEL_DATASET_FAMILY_V001,
    LABEL_DATASET_VERSION_V001,
    LABEL_HORIZON_MS_V001,
    LABEL_HORIZONS_V001,
    LABEL_LINEAGE_COLUMNS_V001,
    LABEL_NAMES_V001,
    LABEL_SCHEMA_V001,
    LABEL_SCHEMA_VERSION_V001,
    LABEL_SUPPORT_COLUMN_NAMES_V001,
)

# ---------------------------------------------------------------------------
# Expected canonical values (Phase 4bj-C real-run constants)
# ---------------------------------------------------------------------------

EXPECTED_LABEL_PARQUET_SHA = (
    "ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26"
)
EXPECTED_LABEL_MANIFEST_SHA = (
    "181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3"
)
EXPECTED_LABEL_CONFIG_HASH = (
    "fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00"
)
EXPECTED_SOURCE_FEATURE_PARQUET_SHA = (
    "618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f"
)
EXPECTED_SOURCE_FEATURE_MANIFEST_SHA = (
    "624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718"
)
EXPECTED_SOURCE_FEATURE_SUCCESSOR_STATE_SHA = (
    "8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a"
)
EXPECTED_SOURCE_PHASE_4BI_B_GATE_REPORT_SHA = (
    "aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988"
)
EXPECTED_SOURCE_NORMALIZED_PARQUET_SHA = (
    "2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa"
)

EXPECTED_DATASET_FAMILY = LABEL_DATASET_FAMILY_V001
EXPECTED_DATASET_VERSION = LABEL_DATASET_VERSION_V001
EXPECTED_LABEL_SCHEMA_VERSION = LABEL_SCHEMA_VERSION_V001
EXPECTED_SYMBOL = "BTCUSDT"
EXPECTED_UTC_DATE = "2025-01-15"
EXPECTED_ROW_COUNT = 1_681_098

EXPECTED_INVALID_PRICE_ROW_COUNT = 0
EXPECTED_CENSORED_PER_HORIZON: dict[str, int] = {
    "1s": 9,
    "5s": 42,
    "15s": 118,
    "60s": 507,
}
EXPECTED_LABEL_ANY_CENSORED_TRUE_COUNT = 507
"""Equals censored_per_horizon["60s"] because per-horizon censoring is
nested: 1s ⊆ 5s ⊆ 15s ⊆ 60s. The label_any_censored_flag is the OR of
the four per-horizon flags, so its true-count equals the 60s count."""

REQUIRED_GOVERNANCE_FORBIDDEN_KEYS: tuple[str, ...] = (
    "ml",
    "strategy",
    "backtest",
    "paper_shadow_live",
    "deployment",
    "exchange_write",
)

REQUIRED_BOUNDARY_KEYS: tuple[str, ...] = (
    "no_ml",
    "no_strategy",
    "no_backtest",
    "no_acquisition",
    "no_network",
    "no_credentials",
    "no_feature_manifest_mutation",
    "no_feature_parquet_mutation",
    "no_feature_successor_state_mutation",
    "no_feature_gate_report_mutation",
    "no_label_gate_report",
    "no_label_successor_state",
    "no_successor_authorization",
)

EXPECTED_LABEL_LIST = list(LABEL_NAMES_V001)
EXPECTED_HORIZON_LIST = list(LABEL_HORIZONS_V001)
EXPECTED_HORIZON_MS_LIST = list(LABEL_HORIZON_MS_V001)
EXPECTED_SCHEMA_COLUMN_LIST = list(LABEL_SCHEMA_V001)
EXPECTED_SUPPORT_COLUMN_LIST = list(LABEL_SUPPORT_COLUMN_NAMES_V001)


# ---------------------------------------------------------------------------
# Status / result types
# ---------------------------------------------------------------------------


class LabelGateCheckStatus(StrEnum):
    """Tri+1-state label-gate check status."""

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


@dataclass(frozen=True)
class LabelGateCheckResult:
    """One row of the label-gate report's ``checks`` array."""

    check_id: str
    group: str
    title: str
    status: LabelGateCheckStatus
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
class LabelGateContext:
    """Mutable per-run inspection context shared across checks."""

    # paths
    label_parquet_path: Path
    label_parquet_sidecar_path: Path
    label_manifest_path: Path
    label_manifest_sidecar_path: Path
    source_feature_parquet_path: Path | None
    source_feature_manifest_path: Path | None

    # parsed manifest
    label_manifest: dict[str, Any]
    label_manifest_bytes: bytes
    label_manifest_sha: str
    label_manifest_sidecar_first_64: str

    # parquet table
    label_table: pa.Table
    source_feature_table: pa.Table | None

    # SHAs
    label_parquet_sha: str
    label_parquet_sidecar_first_64: str
    source_feature_parquet_sha: str | None
    source_feature_manifest_sha: str | None

    # gitignore evidence (computed once via subprocess at runtime; cached here)
    gitignore_results: dict[str, bool]

    measured: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Constructors
# ---------------------------------------------------------------------------


def _ok(check_id: str, group: str, title: str, detail: str = "") -> LabelGateCheckResult:
    return LabelGateCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=LabelGateCheckStatus.PASS,
        detail=detail,
    )


def _fail(check_id: str, group: str, title: str, detail: str) -> LabelGateCheckResult:
    return LabelGateCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=LabelGateCheckStatus.FAIL,
        detail=detail,
    )


def _na(check_id: str, group: str, title: str, detail: str) -> LabelGateCheckResult:
    return LabelGateCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=LabelGateCheckStatus.NOT_APPLICABLE,
        detail=detail,
    )


def _err(check_id: str, group: str, title: str, detail: str) -> LabelGateCheckResult:
    return LabelGateCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=LabelGateCheckStatus.ERROR,
        detail=detail,
    )


# ---------------------------------------------------------------------------
# Group A — Artefact presence
# ---------------------------------------------------------------------------


def check_a01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet exists"
    if not ctx.label_parquet_path.exists():
        return _fail("4bj-e.A01", "A", title, f"missing: {ctx.label_parquet_path}")
    return _ok("4bj-e.A01", "A", title, str(ctx.label_parquet_path))


def check_a02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet sidecar exists"
    if not ctx.label_parquet_sidecar_path.exists():
        return _fail(
            "4bj-e.A02", "A", title, f"missing: {ctx.label_parquet_sidecar_path}"
        )
    return _ok("4bj-e.A02", "A", title, str(ctx.label_parquet_sidecar_path))


def check_a03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest exists"
    if not ctx.label_manifest_path.exists():
        return _fail("4bj-e.A03", "A", title, f"missing: {ctx.label_manifest_path}")
    return _ok("4bj-e.A03", "A", title, str(ctx.label_manifest_path))


def check_a04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest sidecar exists"
    if not ctx.label_manifest_sidecar_path.exists():
        return _fail(
            "4bj-e.A04", "A", title, f"missing: {ctx.label_manifest_sidecar_path}"
        )
    return _ok("4bj-e.A04", "A", title, str(ctx.label_manifest_sidecar_path))


# ---------------------------------------------------------------------------
# Group B — Gitignore / tracked-file boundary
# ---------------------------------------------------------------------------


def check_b01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "data/microstructure/ is gitignored"
    if ctx.gitignore_results.get("data/microstructure/", False):
        return _ok("4bj-e.B01", "B", title, "ignored")
    return _fail("4bj-e.B01", "B", title, "not ignored")


def check_b02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "data/microstructure/labels/ is gitignored"
    if ctx.gitignore_results.get("data/microstructure/labels/", False):
        return _ok("4bj-e.B02", "B", title, "ignored")
    return _fail("4bj-e.B02", "B", title, "not ignored")


def check_b03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "data/microstructure/manifests/ is gitignored"
    if ctx.gitignore_results.get("data/microstructure/manifests/", False):
        return _ok("4bj-e.B03", "B", title, "ignored")
    return _fail("4bj-e.B03", "B", title, "not ignored")


def check_b04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "data/microstructure/gate-reports/labels/ is gitignored"
    if ctx.gitignore_results.get(
        "data/microstructure/gate-reports/labels/", False
    ):
        return _ok("4bj-e.B04", "B", title, "ignored")
    return _fail("4bj-e.B04", "B", title, "not ignored")


# ---------------------------------------------------------------------------
# Group C — Label manifest governance
# ---------------------------------------------------------------------------


def check_c01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest dataset_family"
    actual = ctx.label_manifest.get("dataset_family")
    if actual != EXPECTED_DATASET_FAMILY:
        return _fail("4bj-e.C01", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C01", "C", title, actual)


def check_c02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest dataset_version"
    actual = ctx.label_manifest.get("dataset_version")
    if actual != EXPECTED_DATASET_VERSION:
        return _fail("4bj-e.C02", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C02", "C", title, actual)


def check_c03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest label_schema_version"
    actual = ctx.label_manifest.get("label_schema_version")
    if actual != EXPECTED_LABEL_SCHEMA_VERSION:
        return _fail("4bj-e.C03", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C03", "C", title, actual)


def check_c04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest symbol"
    actual = ctx.label_manifest.get("symbol")
    if actual != EXPECTED_SYMBOL:
        return _fail("4bj-e.C04", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C04", "C", title, actual)


def check_c05(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest utc_date"
    actual = ctx.label_manifest.get("utc_date")
    if actual != EXPECTED_UTC_DATE:
        return _fail("4bj-e.C05", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C05", "C", title, actual)


def check_c06(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest row_count"
    actual = ctx.label_manifest.get("row_count")
    if actual != EXPECTED_ROW_COUNT:
        return _fail("4bj-e.C06", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C06", "C", title, str(actual))


def check_c07(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest research_eligible is false"
    actual = ctx.label_manifest.get("research_eligible")
    if actual is not False:
        return _fail("4bj-e.C07", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C07", "C", title, "False")


def check_c08(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest eligibility_gate_status is pending"
    actual = ctx.label_manifest.get("eligibility_gate_status")
    if actual != "pending":
        return _fail("4bj-e.C08", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C08", "C", title, "pending")


def check_c09(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest chronological_split_policy is not_yet_defined"
    actual = ctx.label_manifest.get("chronological_split_policy")
    if actual != "not_yet_defined":
        return _fail("4bj-e.C09", "C", title, f"actual={actual!r}")
    return _ok("4bj-e.C09", "C", title, "not_yet_defined")


def check_c10(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest governance labels (forbidden + acquisition unauthorized)"
    gov = ctx.label_manifest.get("governance_labels") or {}
    for key in REQUIRED_GOVERNANCE_FORBIDDEN_KEYS:
        actual = gov.get(key)
        if actual != "forbidden":
            return _fail(
                "4bj-e.C10", "C", title, f"governance_labels.{key}={actual!r}"
            )
    if gov.get("acquisition") != "unauthorized":
        return _fail(
            "4bj-e.C10",
            "C",
            title,
            f"governance_labels.acquisition={gov.get('acquisition')!r}",
        )
    return _ok("4bj-e.C10", "C", title, "all forbidden + acquisition unauthorized")


# ---------------------------------------------------------------------------
# Group D — Schema / column-order / label-list
# ---------------------------------------------------------------------------


def check_d01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet column count == 39"
    cols = ctx.label_table.column_names
    if len(cols) != 39:
        return _fail("4bj-e.D01", "D", title, f"actual={len(cols)}")
    return _ok("4bj-e.D01", "D", title, str(len(cols)))


def check_d02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet column order == LABEL_SCHEMA_V001"
    cols = tuple(ctx.label_table.column_names)
    if cols != LABEL_SCHEMA_V001:
        diff = [
            (i, a, b)
            for i, (a, b) in enumerate(zip(cols, LABEL_SCHEMA_V001, strict=False))
            if a != b
        ]
        return _fail("4bj-e.D02", "D", title, f"first_diff={diff[:3]!r}")
    return _ok("4bj-e.D02", "D", title, "matches")


def check_d03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label column count == 8"
    label_cols = [c for c in ctx.label_table.column_names if c in LABEL_NAMES_V001]
    if len(label_cols) != 8:
        return _fail("4bj-e.D03", "D", title, f"actual={len(label_cols)}")
    return _ok("4bj-e.D03", "D", title, str(len(label_cols)))


def check_d04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "support column count == 14"
    support_cols = [
        c for c in ctx.label_table.column_names if c in LABEL_SUPPORT_COLUMN_NAMES_V001
    ]
    if len(support_cols) != 14:
        return _fail("4bj-e.D04", "D", title, f"actual={len(support_cols)}")
    return _ok("4bj-e.D04", "D", title, str(len(support_cols)))


def check_d05(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "lineage column count == 17"
    lineage_cols = [
        c for c in ctx.label_table.column_names if c in LABEL_LINEAGE_COLUMNS_V001
    ]
    if len(lineage_cols) != 17:
        return _fail("4bj-e.D05", "D", title, f"actual={len(lineage_cols)}")
    return _ok("4bj-e.D05", "D", title, str(len(lineage_cols)))


def check_d06(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest label_list == LABEL_NAMES_V001"
    actual = ctx.label_manifest.get("label_list")
    if actual != EXPECTED_LABEL_LIST:
        return _fail("4bj-e.D06", "D", title, "label_list does not match canonical")
    return _ok("4bj-e.D06", "D", title, "matches")


def check_d07(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = 'manifest horizon_list == ["1s","5s","15s","60s"]'
    actual = ctx.label_manifest.get("horizon_list")
    if actual != EXPECTED_HORIZON_LIST:
        return _fail("4bj-e.D07", "D", title, f"actual={actual!r}")
    return _ok("4bj-e.D07", "D", title, str(actual))


def check_d08(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest horizon_ms_list == [1000,5000,15000,60000]"
    actual = ctx.label_manifest.get("horizon_ms_list")
    if actual != EXPECTED_HORIZON_MS_LIST:
        return _fail("4bj-e.D08", "D", title, f"actual={actual!r}")
    return _ok("4bj-e.D08", "D", title, str(actual))


def check_d09(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest schema_column_list matches LABEL_SCHEMA_V001"
    actual = ctx.label_manifest.get("schema_column_list")
    if actual != EXPECTED_SCHEMA_COLUMN_LIST:
        return _fail("4bj-e.D09", "D", title, "schema_column_list mismatch")
    return _ok("4bj-e.D09", "D", title, "matches")


def check_d10(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "no forbidden column substrings present in parquet schema"
    cols_lower = [c.lower() for c in ctx.label_table.column_names]
    found: list[tuple[str, str]] = []
    for col in cols_lower:
        for tok in FORBIDDEN_LABEL_COLUMN_SUBSTRINGS:
            if tok in col:
                found.append((col, tok))
                break
    if found:
        return _fail("4bj-e.D10", "D", title, f"found={found[:3]!r}")
    return _ok("4bj-e.D10", "D", title, "none")


# ---------------------------------------------------------------------------
# Group E — Row-count / row-identity / row-alignment
# ---------------------------------------------------------------------------


def check_e01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet row count == 1,681,098"
    rows = ctx.label_table.num_rows
    if rows != EXPECTED_ROW_COUNT:
        return _fail("4bj-e.E01", "E", title, f"rows={rows}")
    return _ok("4bj-e.E01", "E", title, f"rows={rows}")


def check_e02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet row count == manifest row_count"
    mf_rows = ctx.label_manifest.get("row_count")
    rows = ctx.label_table.num_rows
    if mf_rows != rows:
        return _fail(
            "4bj-e.E02",
            "E",
            title,
            f"parquet_rows={rows} manifest_row_count={mf_rows!r}",
        )
    return _ok("4bj-e.E02", "E", title, f"both={rows}")


def check_e03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "row_index contiguous 0..row_count-1"
    n = ctx.label_table.num_rows
    arr = ctx.label_table.column("row_index").to_numpy()
    expected = np.arange(n, dtype=arr.dtype)
    if arr.shape != expected.shape or not np.array_equal(arr, expected):
        first_bad = (
            int(np.argmax(arr != expected)) if arr.shape == expected.shape else -1
        )
        return _fail("4bj-e.E03", "E", title, f"first_bad_idx={first_bad}")
    return _ok("4bj-e.E03", "E", title, "contiguous")


def check_e04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet row_count matches manifest files[0].row_count"
    files = ctx.label_manifest.get("files") or []
    if not files or not isinstance(files, list):
        return _fail("4bj-e.E04", "E", title, "manifest.files is empty or not a list")
    file_entry = files[0]
    if not isinstance(file_entry, dict):
        return _fail("4bj-e.E04", "E", title, "manifest.files[0] is not a dict")
    file_rows = file_entry.get("row_count")
    rows = ctx.label_table.num_rows
    if file_rows != rows:
        return _fail(
            "4bj-e.E04",
            "E",
            title,
            f"parquet_rows={rows} manifest_file_row_count={file_rows!r}",
        )
    return _ok("4bj-e.E04", "E", title, f"both={rows}")


# ---------------------------------------------------------------------------
# Group F — Hash / lineage
# ---------------------------------------------------------------------------


def check_f01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet SHA matches expected"
    if ctx.label_parquet_sha != EXPECTED_LABEL_PARQUET_SHA:
        return _fail(
            "4bj-e.F01",
            "F",
            title,
            f"actual={ctx.label_parquet_sha} expected={EXPECTED_LABEL_PARQUET_SHA}",
        )
    return _ok("4bj-e.F01", "F", title, ctx.label_parquet_sha)


def check_f02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label parquet sidecar matches recomputed bytes"
    if ctx.label_parquet_sidecar_first_64 != ctx.label_parquet_sha:
        return _fail(
            "4bj-e.F02",
            "F",
            title,
            f"sidecar={ctx.label_parquet_sidecar_first_64} parquet={ctx.label_parquet_sha}",
        )
    return _ok("4bj-e.F02", "F", title, "matches")


def check_f03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest SHA matches expected"
    if ctx.label_manifest_sha != EXPECTED_LABEL_MANIFEST_SHA:
        return _fail(
            "4bj-e.F03",
            "F",
            title,
            f"actual={ctx.label_manifest_sha} expected={EXPECTED_LABEL_MANIFEST_SHA}",
        )
    return _ok("4bj-e.F03", "F", title, ctx.label_manifest_sha)


def check_f04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest sidecar matches recomputed bytes"
    if ctx.label_manifest_sidecar_first_64 != ctx.label_manifest_sha:
        return _fail(
            "4bj-e.F04",
            "F",
            title,
            f"sidecar={ctx.label_manifest_sidecar_first_64} manifest={ctx.label_manifest_sha}",
        )
    return _ok("4bj-e.F04", "F", title, "matches")


def check_f05(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label_config_hash matches expected"
    actual = ctx.label_manifest.get("label_config_hash")
    if actual != EXPECTED_LABEL_CONFIG_HASH:
        return _fail("4bj-e.F05", "F", title, f"actual={actual!r}")
    return _ok("4bj-e.F05", "F", title, str(actual))


def check_f06(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest source_feature_parquet_sha256 matches expected"
    actual = ctx.label_manifest.get("source_feature_parquet_sha256")
    if actual != EXPECTED_SOURCE_FEATURE_PARQUET_SHA:
        return _fail("4bj-e.F06", "F", title, f"actual={actual!r}")
    return _ok("4bj-e.F06", "F", title, str(actual))


def check_f07(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest source_feature_manifest_sha256 matches expected"
    actual = ctx.label_manifest.get("source_feature_manifest_sha256")
    if actual != EXPECTED_SOURCE_FEATURE_MANIFEST_SHA:
        return _fail("4bj-e.F07", "F", title, f"actual={actual!r}")
    return _ok("4bj-e.F07", "F", title, str(actual))


def check_f08(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest source_feature_successor_state_sha256 matches expected"
    actual = ctx.label_manifest.get("source_feature_successor_state_sha256")
    if actual != EXPECTED_SOURCE_FEATURE_SUCCESSOR_STATE_SHA:
        return _fail("4bj-e.F08", "F", title, f"actual={actual!r}")
    return _ok("4bj-e.F08", "F", title, str(actual))


def check_f09(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest source_phase_4bi_b_gate_report_sha256 matches expected"
    actual = ctx.label_manifest.get("source_phase_4bi_b_gate_report_sha256")
    if actual != EXPECTED_SOURCE_PHASE_4BI_B_GATE_REPORT_SHA:
        return _fail("4bj-e.F09", "F", title, f"actual={actual!r}")
    return _ok("4bj-e.F09", "F", title, str(actual))


def check_f10(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest source_normalized_parquet_sha256 matches expected"
    actual = ctx.label_manifest.get("source_normalized_parquet_sha256")
    if actual != EXPECTED_SOURCE_NORMALIZED_PARQUET_SHA:
        return _fail("4bj-e.F10", "F", title, f"actual={actual!r}")
    return _ok("4bj-e.F10", "F", title, str(actual))


def check_f11(ctx: LabelGateContext) -> LabelGateCheckResult:
    """Spot-check constant per-row lineage SHA columns on the parquet."""
    title = "lineage SHA columns constant per-row and match expected"
    expected_pairs = (
        ("source_feature_parquet_sha256", EXPECTED_SOURCE_FEATURE_PARQUET_SHA),
        ("source_feature_manifest_sha256", EXPECTED_SOURCE_FEATURE_MANIFEST_SHA),
        (
            "source_feature_successor_state_sha256",
            EXPECTED_SOURCE_FEATURE_SUCCESSOR_STATE_SHA,
        ),
        (
            "source_phase_4bi_b_gate_report_sha256",
            EXPECTED_SOURCE_PHASE_4BI_B_GATE_REPORT_SHA,
        ),
        ("source_normalized_parquet_sha256", EXPECTED_SOURCE_NORMALIZED_PARQUET_SHA),
        ("label_config_hash", EXPECTED_LABEL_CONFIG_HASH),
    )
    n = ctx.label_table.num_rows
    sample_indices = (0, n // 4, n // 2, n - 1) if n >= 4 else tuple(range(n))
    for col_name, expected in expected_pairs:
        if col_name not in ctx.label_table.column_names:
            return _fail("4bj-e.F11", "F", title, f"column {col_name} missing")
        col = ctx.label_table.column(col_name)
        for idx in sample_indices:
            v = col[idx].as_py()
            if v != expected:
                return _fail(
                    "4bj-e.F11",
                    "F",
                    title,
                    f"{col_name} idx={idx} value={v!r} expected={expected}",
                )
    return _ok("4bj-e.F11", "F", title, "all constant")


# ---------------------------------------------------------------------------
# Group G — Manifest scalar counts
# ---------------------------------------------------------------------------


def check_g01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest invalid_price_row_count == 0"
    actual = ctx.label_manifest.get("invalid_price_row_count")
    if actual != EXPECTED_INVALID_PRICE_ROW_COUNT:
        return _fail("4bj-e.G01", "G", title, f"actual={actual!r}")
    return _ok("4bj-e.G01", "G", title, "0")


def check_g02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest censored_per_horizon == expected"
    actual = ctx.label_manifest.get("censored_per_horizon")
    if not isinstance(actual, dict):
        return _fail("4bj-e.G02", "G", title, f"actual={actual!r}")
    for k, v in EXPECTED_CENSORED_PER_HORIZON.items():
        if actual.get(k) != v:
            return _fail(
                "4bj-e.G02",
                "G",
                title,
                f"censored_per_horizon.{k}={actual.get(k)!r} expected={v}",
            )
    return _ok("4bj-e.G02", "G", title, str(actual))


# ---------------------------------------------------------------------------
# Group H — Per-horizon flag-count parity (parquet vs manifest)
# ---------------------------------------------------------------------------


def _count_true(col: pa.ChunkedArray) -> int:
    arr = col.to_numpy(zero_copy_only=False)
    return int(arr.sum())


def check_h01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "horizon_censored_flag_1s true-count == manifest censored_per_horizon[1s]"
    cnt = _count_true(ctx.label_table.column("horizon_censored_flag_1s"))
    exp = EXPECTED_CENSORED_PER_HORIZON["1s"]
    if cnt != exp:
        return _fail("4bj-e.H01", "H", title, f"actual={cnt} expected={exp}")
    return _ok("4bj-e.H01", "H", title, str(cnt))


def check_h02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "horizon_censored_flag_5s true-count == manifest censored_per_horizon[5s]"
    cnt = _count_true(ctx.label_table.column("horizon_censored_flag_5s"))
    exp = EXPECTED_CENSORED_PER_HORIZON["5s"]
    if cnt != exp:
        return _fail("4bj-e.H02", "H", title, f"actual={cnt} expected={exp}")
    return _ok("4bj-e.H02", "H", title, str(cnt))


def check_h03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "horizon_censored_flag_15s true-count == manifest censored_per_horizon[15s]"
    cnt = _count_true(ctx.label_table.column("horizon_censored_flag_15s"))
    exp = EXPECTED_CENSORED_PER_HORIZON["15s"]
    if cnt != exp:
        return _fail("4bj-e.H03", "H", title, f"actual={cnt} expected={exp}")
    return _ok("4bj-e.H03", "H", title, str(cnt))


def check_h04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "horizon_censored_flag_60s true-count == manifest censored_per_horizon[60s]"
    cnt = _count_true(ctx.label_table.column("horizon_censored_flag_60s"))
    exp = EXPECTED_CENSORED_PER_HORIZON["60s"]
    if cnt != exp:
        return _fail("4bj-e.H04", "H", title, f"actual={cnt} expected={exp}")
    return _ok("4bj-e.H04", "H", title, str(cnt))


# ---------------------------------------------------------------------------
# Group I — Dtype / value sanity
# ---------------------------------------------------------------------------


def check_i01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "row_index is int64"
    col = ctx.label_table.column("row_index")
    if not pa.types.is_int64(col.type):
        return _fail("4bj-e.I01", "I", title, f"type={col.type}")
    return _ok("4bj-e.I01", "I", title, "int64")


def check_i02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "feature_timestamp_ms is int64"
    col = ctx.label_table.column("feature_timestamp_ms")
    if not pa.types.is_int64(col.type):
        return _fail("4bj-e.I02", "I", title, f"type={col.type}")
    return _ok("4bj-e.I02", "I", title, "int64")


def check_i03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "forward_log_return_* dtype float64 and null-or-finite"
    bad: list[str] = []
    for label in LABEL_HORIZONS_V001:
        col_name = f"forward_log_return_{label}"
        col = ctx.label_table.column(col_name)
        if not pa.types.is_float64(col.type):
            bad.append(f"{col_name}:type={col.type}")
            continue
        arr = col.to_numpy(zero_copy_only=False)
        non_null = arr[~np.isnan(arr)]
        if non_null.size and not np.isfinite(non_null).all():
            bad.append(f"{col_name}:non-finite")
    if bad:
        return _fail("4bj-e.I03", "I", title, f"{bad[:3]!r}")
    return _ok("4bj-e.I03", "I", title, "ok")


def check_i04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "forward_direction_* dtype int8 nullable and in {-1,0,1}"
    bad: list[str] = []
    allowed: set[int | None] = {-1, 0, 1, None}
    for label in LABEL_HORIZONS_V001:
        col_name = f"forward_direction_{label}"
        col = ctx.label_table.column(col_name)
        if not pa.types.is_int8(col.type):
            bad.append(f"{col_name}:type={col.type}")
            continue
        # Walk via .to_pylist to capture None preservation alongside ints.
        # Cheap sampling: scan a handful of representative indices.
        n = ctx.label_table.num_rows
        sample_indices = (
            0,
            n // 4,
            n // 2,
            3 * n // 4,
            n - 1,
        ) if n >= 4 else tuple(range(n))
        for idx in sample_indices:
            v = col[idx].as_py()
            if v not in allowed:
                bad.append(f"{col_name}:idx={idx}:value={v!r}")
                break
    if bad:
        return _fail("4bj-e.I04", "I", title, f"{bad[:3]!r}")
    return _ok("4bj-e.I04", "I", title, "ok")


def check_i05(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "horizon_censored_flag_* dtype bool"
    bad: list[str] = []
    for label in LABEL_HORIZONS_V001:
        col_name = f"horizon_censored_flag_{label}"
        col = ctx.label_table.column(col_name)
        if not pa.types.is_boolean(col.type):
            bad.append(f"{col_name}:type={col.type}")
    if bad:
        return _fail("4bj-e.I05", "I", title, f"{bad!r}")
    return _ok("4bj-e.I05", "I", title, "ok")


def check_i06(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label_invalid_price_flag dtype bool"
    col = ctx.label_table.column("label_invalid_price_flag")
    if not pa.types.is_boolean(col.type):
        return _fail("4bj-e.I06", "I", title, f"type={col.type}")
    return _ok("4bj-e.I06", "I", title, "bool")


def check_i07(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label_any_censored_flag dtype bool"
    col = ctx.label_table.column("label_any_censored_flag")
    if not pa.types.is_boolean(col.type):
        return _fail("4bj-e.I07", "I", title, f"type={col.type}")
    return _ok("4bj-e.I07", "I", title, "bool")


def check_i08(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "lineage SHA columns are strings"
    string_cols = (
        "source_feature_parquet_sha256",
        "source_feature_manifest_sha256",
        "source_feature_successor_state_sha256",
        "source_phase_4bi_b_gate_report_sha256",
        "source_normalized_parquet_sha256",
        "label_config_hash",
    )
    bad: list[str] = []
    for col_name in string_cols:
        col = ctx.label_table.column(col_name)
        if not pa.types.is_string(col.type):
            bad.append(f"{col_name}:type={col.type}")
    if bad:
        return _fail("4bj-e.I08", "I", title, f"{bad!r}")
    return _ok("4bj-e.I08", "I", title, "ok")


def check_i09(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label_invalid_price_flag all false (Phase 4bj-C run had 0)"
    cnt = _count_true(ctx.label_table.column("label_invalid_price_flag"))
    if cnt != 0:
        return _fail("4bj-e.I09", "I", title, f"true-count={cnt}")
    return _ok("4bj-e.I09", "I", title, "all false")


# ---------------------------------------------------------------------------
# Group J — Pre/post immutability
# ---------------------------------------------------------------------------


def check_j01(ctx: LabelGateContext) -> LabelGateCheckResult:
    """The orchestrator stamps pre/post measured SHAs via the
    ``ctx.measured`` dict. This check confirms parquet SHA pre == post.
    """
    title = "label parquet SHA pre/post identical during gate run"
    pre = ctx.measured.get("label_parquet_sha_pre")
    post = ctx.measured.get("label_parquet_sha_post")
    if pre is None or post is None:
        return _err(
            "4bj-e.J01",
            "J",
            title,
            "pre/post SHA missing from measured (orchestrator wiring error)",
        )
    if pre != post:
        return _fail("4bj-e.J01", "J", title, f"pre={pre} post={post}")
    return _ok("4bj-e.J01", "J", title, "identical")


def check_j02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label manifest SHA pre/post identical during gate run"
    pre = ctx.measured.get("label_manifest_sha_pre")
    post = ctx.measured.get("label_manifest_sha_post")
    if pre is None or post is None:
        return _err(
            "4bj-e.J02",
            "J",
            title,
            "pre/post SHA missing from measured (orchestrator wiring error)",
        )
    if pre != post:
        return _fail("4bj-e.J02", "J", title, f"pre={pre} post={post}")
    return _ok("4bj-e.J02", "J", title, "identical")


# ---------------------------------------------------------------------------
# Group K — One-row-per-feature-row evidence (optional, vs source feature parquet)
# ---------------------------------------------------------------------------


def check_k01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "source feature parquet row count matches label row count (when available)"
    if ctx.source_feature_table is None:
        return _na(
            "4bj-e.K01",
            "K",
            title,
            "source_feature_parquet_path not provided; skipped",
        )
    if ctx.source_feature_table.num_rows != ctx.label_table.num_rows:
        return _fail(
            "4bj-e.K01",
            "K",
            title,
            f"feature_rows={ctx.source_feature_table.num_rows} "
            f"label_rows={ctx.label_table.num_rows}",
        )
    return _ok("4bj-e.K01", "K", title, str(ctx.label_table.num_rows))


def check_k02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "agg_trade_id matches source feature parquet per-row"
    if ctx.source_feature_table is None:
        return _na(
            "4bj-e.K02",
            "K",
            title,
            "source_feature_parquet_path not provided; skipped",
        )
    if "agg_trade_id" not in ctx.source_feature_table.column_names:
        return _na(
            "4bj-e.K02",
            "K",
            title,
            "source feature table has no agg_trade_id column; skipped",
        )
    a = ctx.label_table.column("agg_trade_id").to_numpy()
    b = ctx.source_feature_table.column("agg_trade_id").to_numpy()
    if a.shape != b.shape or not np.array_equal(a, b):
        return _fail("4bj-e.K02", "K", title, "agg_trade_id mismatch")
    return _ok("4bj-e.K02", "K", title, "matches")


def check_k03(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "feature_timestamp_ms matches source feature parquet per-row"
    if ctx.source_feature_table is None:
        return _na(
            "4bj-e.K03",
            "K",
            title,
            "source_feature_parquet_path not provided; skipped",
        )
    if "feature_timestamp_ms" not in ctx.source_feature_table.column_names:
        return _na(
            "4bj-e.K03",
            "K",
            title,
            "source feature table has no feature_timestamp_ms column; skipped",
        )
    a = ctx.label_table.column("feature_timestamp_ms").to_numpy()
    b = ctx.source_feature_table.column("feature_timestamp_ms").to_numpy()
    if a.shape != b.shape or not np.array_equal(a, b):
        return _fail("4bj-e.K03", "K", title, "feature_timestamp_ms mismatch")
    return _ok("4bj-e.K03", "K", title, "matches")


def check_k04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "row_index matches source feature parquet per-row"
    if ctx.source_feature_table is None:
        return _na(
            "4bj-e.K04",
            "K",
            title,
            "source_feature_parquet_path not provided; skipped",
        )
    if "row_index" not in ctx.source_feature_table.column_names:
        return _na(
            "4bj-e.K04",
            "K",
            title,
            "source feature table has no row_index column; skipped",
        )
    a = ctx.label_table.column("row_index").to_numpy()
    b = ctx.source_feature_table.column("row_index").to_numpy()
    if a.shape != b.shape or not np.array_equal(a, b):
        return _fail("4bj-e.K04", "K", title, "row_index mismatch")
    return _ok("4bj-e.K04", "K", title, "matches")


# ---------------------------------------------------------------------------
# Group L — Forbidden output / consistency / no-rescue
# ---------------------------------------------------------------------------


def check_l01(ctx: LabelGateContext) -> LabelGateCheckResult:
    """Confirm label_any_censored_flag equals OR of per-horizon flags.

    Per-horizon censoring is nested (1s ⊆ 5s ⊆ 15s ⊆ 60s) by the
    future-reference policy. Therefore the OR collapses to the 60s
    flag: ``label_any_censored_flag[i] == horizon_censored_flag_60s[i]``
    for every row.
    """
    title = "label_any_censored_flag == OR of per-horizon flags"
    any_arr = ctx.label_table.column("label_any_censored_flag").to_numpy(
        zero_copy_only=False
    )
    h60_arr = ctx.label_table.column("horizon_censored_flag_60s").to_numpy(
        zero_copy_only=False
    )
    h15_arr = ctx.label_table.column("horizon_censored_flag_15s").to_numpy(
        zero_copy_only=False
    )
    h5_arr = ctx.label_table.column("horizon_censored_flag_5s").to_numpy(
        zero_copy_only=False
    )
    h1_arr = ctx.label_table.column("horizon_censored_flag_1s").to_numpy(
        zero_copy_only=False
    )
    or_arr = h60_arr | h15_arr | h5_arr | h1_arr
    if not np.array_equal(any_arr, or_arr):
        diff = int((any_arr != or_arr).sum())
        return _fail(
            "4bj-e.L01",
            "L",
            title,
            f"{diff} rows disagree",
        )
    return _ok("4bj-e.L01", "L", title, "matches")


def check_l02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = (
        "label_any_censored_flag true-count == expected (== 60s count under nesting)"
    )
    cnt = _count_true(ctx.label_table.column("label_any_censored_flag"))
    if cnt != EXPECTED_LABEL_ANY_CENSORED_TRUE_COUNT:
        return _fail(
            "4bj-e.L02",
            "L",
            title,
            f"actual={cnt} expected={EXPECTED_LABEL_ANY_CENSORED_TRUE_COUNT}",
        )
    return _ok("4bj-e.L02", "L", title, str(cnt))


def check_l03(ctx: LabelGateContext) -> LabelGateCheckResult:
    """Confirm censoring is nested: 1s ⊆ 5s ⊆ 15s ⊆ 60s."""
    title = "per-horizon censoring is nested (1s ⊆ 5s ⊆ 15s ⊆ 60s)"
    h1 = ctx.label_table.column("horizon_censored_flag_1s").to_numpy(
        zero_copy_only=False
    )
    h5 = ctx.label_table.column("horizon_censored_flag_5s").to_numpy(
        zero_copy_only=False
    )
    h15 = ctx.label_table.column("horizon_censored_flag_15s").to_numpy(
        zero_copy_only=False
    )
    h60 = ctx.label_table.column("horizon_censored_flag_60s").to_numpy(
        zero_copy_only=False
    )
    # subset: h1 implies h5 implies h15 implies h60
    if (h1 & ~h5).any():
        return _fail("4bj-e.L03", "L", title, "1s not a subset of 5s")
    if (h5 & ~h15).any():
        return _fail("4bj-e.L03", "L", title, "5s not a subset of 15s")
    if (h15 & ~h60).any():
        return _fail("4bj-e.L03", "L", title, "15s not a subset of 60s")
    return _ok("4bj-e.L03", "L", title, "nested")


def check_l04(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest boundary_confirmations all required keys present and true"
    bc = ctx.label_manifest.get("boundary_confirmations") or {}
    missing = [k for k in REQUIRED_BOUNDARY_KEYS if k not in bc]
    if missing:
        return _fail("4bj-e.L04", "L", title, f"missing keys={missing}")
    bad = [k for k in REQUIRED_BOUNDARY_KEYS if bc.get(k) is not True]
    if bad:
        return _fail("4bj-e.L04", "L", title, f"non-true={bad}")
    return _ok("4bj-e.L04", "L", title, "all true")


# ---------------------------------------------------------------------------
# Group M — Stage interpretation
# ---------------------------------------------------------------------------


def check_m01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label_manifest_research_eligible_after invariant False"
    actual = ctx.label_manifest.get("research_eligible")
    if actual is not False:
        return _fail("4bj-e.M01", "M", title, f"actual={actual!r}")
    return _ok("4bj-e.M01", "M", title, "False")


def check_m02(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label_manifest_eligibility_gate_status_after invariant pending"
    actual = ctx.label_manifest.get("eligibility_gate_status")
    if actual != "pending":
        return _fail("4bj-e.M02", "M", title, f"actual={actual!r}")
    return _ok("4bj-e.M02", "M", title, "pending")


# ---------------------------------------------------------------------------
# Group N — Boundary confirmations
# ---------------------------------------------------------------------------


def check_n01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "manifest boundary_confirmations contains every required key"
    bc = ctx.label_manifest.get("boundary_confirmations") or {}
    missing = [k for k in REQUIRED_BOUNDARY_KEYS if k not in bc]
    if missing:
        return _fail("4bj-e.N01", "N", title, f"missing={missing}")
    return _ok("4bj-e.N01", "N", title, "all present")


# ---------------------------------------------------------------------------
# Group O — Chronological split policy
# ---------------------------------------------------------------------------


def check_o01(ctx: LabelGateContext) -> LabelGateCheckResult:
    title = "label_manifest_chronological_split_policy_after invariant not_yet_defined"
    actual = ctx.label_manifest.get("chronological_split_policy")
    if actual != "not_yet_defined":
        return _fail("4bj-e.O01", "O", title, f"actual={actual!r}")
    return _ok("4bj-e.O01", "O", title, "not_yet_defined")


# ---------------------------------------------------------------------------
# Check order (canonical, stable)
# ---------------------------------------------------------------------------


CHECK_ORDER: tuple[
    tuple[str, Callable[[LabelGateContext], LabelGateCheckResult]], ...
] = (
    ("4bj-e.A01", check_a01),
    ("4bj-e.A02", check_a02),
    ("4bj-e.A03", check_a03),
    ("4bj-e.A04", check_a04),
    ("4bj-e.B01", check_b01),
    ("4bj-e.B02", check_b02),
    ("4bj-e.B03", check_b03),
    ("4bj-e.B04", check_b04),
    ("4bj-e.C01", check_c01),
    ("4bj-e.C02", check_c02),
    ("4bj-e.C03", check_c03),
    ("4bj-e.C04", check_c04),
    ("4bj-e.C05", check_c05),
    ("4bj-e.C06", check_c06),
    ("4bj-e.C07", check_c07),
    ("4bj-e.C08", check_c08),
    ("4bj-e.C09", check_c09),
    ("4bj-e.C10", check_c10),
    ("4bj-e.D01", check_d01),
    ("4bj-e.D02", check_d02),
    ("4bj-e.D03", check_d03),
    ("4bj-e.D04", check_d04),
    ("4bj-e.D05", check_d05),
    ("4bj-e.D06", check_d06),
    ("4bj-e.D07", check_d07),
    ("4bj-e.D08", check_d08),
    ("4bj-e.D09", check_d09),
    ("4bj-e.D10", check_d10),
    ("4bj-e.E01", check_e01),
    ("4bj-e.E02", check_e02),
    ("4bj-e.E03", check_e03),
    ("4bj-e.E04", check_e04),
    ("4bj-e.F01", check_f01),
    ("4bj-e.F02", check_f02),
    ("4bj-e.F03", check_f03),
    ("4bj-e.F04", check_f04),
    ("4bj-e.F05", check_f05),
    ("4bj-e.F06", check_f06),
    ("4bj-e.F07", check_f07),
    ("4bj-e.F08", check_f08),
    ("4bj-e.F09", check_f09),
    ("4bj-e.F10", check_f10),
    ("4bj-e.F11", check_f11),
    ("4bj-e.G01", check_g01),
    ("4bj-e.G02", check_g02),
    ("4bj-e.H01", check_h01),
    ("4bj-e.H02", check_h02),
    ("4bj-e.H03", check_h03),
    ("4bj-e.H04", check_h04),
    ("4bj-e.I01", check_i01),
    ("4bj-e.I02", check_i02),
    ("4bj-e.I03", check_i03),
    ("4bj-e.I04", check_i04),
    ("4bj-e.I05", check_i05),
    ("4bj-e.I06", check_i06),
    ("4bj-e.I07", check_i07),
    ("4bj-e.I08", check_i08),
    ("4bj-e.I09", check_i09),
    ("4bj-e.J01", check_j01),
    ("4bj-e.J02", check_j02),
    ("4bj-e.K01", check_k01),
    ("4bj-e.K02", check_k02),
    ("4bj-e.K03", check_k03),
    ("4bj-e.K04", check_k04),
    ("4bj-e.L01", check_l01),
    ("4bj-e.L02", check_l02),
    ("4bj-e.L03", check_l03),
    ("4bj-e.L04", check_l04),
    ("4bj-e.M01", check_m01),
    ("4bj-e.M02", check_m02),
    ("4bj-e.N01", check_n01),
    ("4bj-e.O01", check_o01),
)


def run_all_checks(ctx: LabelGateContext) -> tuple[LabelGateCheckResult, ...]:
    """Run every Phase 4bj-E check function and return the result tuple."""
    out: list[LabelGateCheckResult] = []
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
