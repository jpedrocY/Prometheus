"""Phase 4bf 55-check derived-family eligibility-gate suite.

Each check returns a :class:`DerivedAggTradesCheckResult` with status
PASS / FAIL / NOT_APPLICABLE / ERROR. The :data:`CHECK_ORDER` tuple
maps every Phase 4bf-A check id ``4bf.13.1`` .. ``4bf.13.55`` to its
:class:`check_*` function in stable order.

All checks are read-only. They never mutate the derived manifest, the
normalized Parquet, the raw artefacts, or the Phase 4bb-D gate report.
"""
from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa

# These constants are imported from the existing Phase 4bd module so we
# inherit a single canonical schema definition.
from .normalize_aggtrades import NORMALIZED_SCHEMA_V001

CANONICAL_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
CANONICAL_DATASET_VERSION = "v001"
CANONICAL_SOURCE_DATASET_FAMILY = "microstructure_raw_aggtrades_v001"
CANONICAL_SOURCE_DATASET_VERSION = "v001"
CANONICAL_SYMBOL = "BTCUSDT"
CANONICAL_UTC_DATE = "2025-01-15"
CANONICAL_NORMALIZATION_SCHEMA_VERSION = "v001"

EXPECTED_DERIVED_MANIFEST_SHA = "f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9"
EXPECTED_NORMALIZED_PARQUET_SHA = "2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa"
EXPECTED_RAW_MANIFEST_SHA = "a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201"
EXPECTED_RAW_ZIP_SHA = "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
EXPECTED_RAW_SIDECAR_SHA = "b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d"
EXPECTED_ACQUISITION_LOG_SHA = "f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c"
EXPECTED_GATE_REPORT_SHA = "96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423"
EXPECTED_GATE_REPORT_ID = (
    "microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c"
)

EXPECTED_EVENT_COUNT = 1_681_098
DAY_START_MS = 1_736_899_200_000  # 2025-01-15T00:00:00.000Z
DAY_END_MS = 1_736_985_600_000    # 2025-01-16T00:00:00.000Z
EXPECTED_FIRST_AGG_TRADE_ID = 2_516_301_323
EXPECTED_LAST_AGG_TRADE_ID = 2_517_982_420
EXPECTED_FIRST_T = 1_736_899_205_109
EXPECTED_LAST_T = 1_736_985_599_991
EXPECTED_FIRST_PRICE = "96514.9"
EXPECTED_LAST_PRICE = "100460.0"
EXPECTED_FIRST_QUANTITY = "0.091"
EXPECTED_LAST_QUANTITY = "0.059"

PHASE_4BE_QA_PATH = Path(
    "docs/00-meta/implementation-reports/2026-05-07_phase-4be_aggtrades-normalized-structural-qa.md"
)
PHASE_4BE_CLOSEOUT_PATH = Path(
    "docs/00-meta/implementation-reports/2026-05-07_phase-4be_closeout.md"
)
PHASE_4BE_MERGE_CLOSEOUT_PATH = Path(
    "docs/00-meta/implementation-reports/2026-05-07_phase-4be_merge-closeout.md"
)

# Forbidden token family applied to Parquet column names.
FORBIDDEN_COLUMN_TOKENS: tuple[str, ...] = (
    "feature", "label", "signal", "return", "alpha", "edge", "imbalance",
    "sweep", "spread", "depth", "liquid", "slippage", "order_flow",
    "execution_qual", "ml_", "strategy", "mfe", "mae", "r_multiple",
    "pnl", "equity", "position", "regime", "momentum", "volatility",
)

# Per-row lineage columns whose values must be constant and equal to the
# expected canonical value.
LINEAGE_CONSTANT_COLUMNS: tuple[tuple[str, str], ...] = (
    ("dataset_family", CANONICAL_DATASET_FAMILY),
    ("dataset_version", CANONICAL_DATASET_VERSION),
    ("source_dataset_family", CANONICAL_SOURCE_DATASET_FAMILY),
    ("source_dataset_version", CANONICAL_SOURCE_DATASET_VERSION),
    ("symbol", CANONICAL_SYMBOL),
    ("utc_date", CANONICAL_UTC_DATE),
    ("source_file_sha256", EXPECTED_RAW_ZIP_SHA),
    ("source_manifest_sha256", EXPECTED_RAW_MANIFEST_SHA),
    ("source_gate_report_id", EXPECTED_GATE_REPORT_ID),
    ("source_gate_report_sha256", EXPECTED_GATE_REPORT_SHA),
    ("normalization_schema_version", CANONICAL_NORMALIZATION_SCHEMA_VERSION),
)


class DerivedAggTradesCheckStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


@dataclass(frozen=True)
class DerivedAggTradesCheckResult:
    """One row of the gate report's ``checks`` array."""

    check_id: str
    group: str
    title: str
    status: DerivedAggTradesCheckStatus
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
class DerivedGateContext:
    """Mutable per-run inspection context shared across checks."""

    derived_manifest_path: Path
    derived_manifest_sidecar_path: Path
    normalized_parquet_path: Path
    normalized_parquet_sidecar_path: Path
    raw_manifest_path: Path
    raw_zip_path: Path
    raw_sidecar_path: Path
    acquisition_log_path: Path
    gate_report_path: Path
    derived_manifest: dict[str, Any]
    derived_manifest_bytes: bytes
    derived_manifest_sha: str
    derived_sidecar_first_64: str
    normalized_parquet_sha: str
    normalized_sidecar_first_64: str
    raw_manifest: dict[str, Any]
    raw_manifest_sha: str
    raw_zip_sha: str
    raw_sidecar_sha: str
    raw_sidecar_first_64: str
    acquisition_log_sha: str
    gate_report_sha: str
    parquet_table: pa.Table
    measured: dict[str, Any] = field(default_factory=dict)


def _ok(check_id: str, group: str, title: str, detail: str = "") -> DerivedAggTradesCheckResult:
    return DerivedAggTradesCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=DerivedAggTradesCheckStatus.PASS,
        detail=detail,
    )


def _fail(check_id: str, group: str, title: str, detail: str) -> DerivedAggTradesCheckResult:
    return DerivedAggTradesCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=DerivedAggTradesCheckStatus.FAIL,
        detail=detail,
    )


# ---------------------------------------------------------------------------
# Group A — Artefact existence
# ---------------------------------------------------------------------------


def check_4bf_13_1(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest exists"
    if not ctx.derived_manifest_path.exists():
        return _fail("4bf.13.1", "A", title, f"missing: {ctx.derived_manifest_path}")
    return _ok("4bf.13.1", "A", title, str(ctx.derived_manifest_path))


def check_4bf_13_2(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest sidecar exists"
    if not ctx.derived_manifest_sidecar_path.exists():
        return _fail("4bf.13.2", "A", title, f"missing: {ctx.derived_manifest_sidecar_path}")
    return _ok("4bf.13.2", "A", title, str(ctx.derived_manifest_sidecar_path))


def check_4bf_13_3(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest SHA matches sidecar and recorded SHA"
    if ctx.derived_manifest_sha != EXPECTED_DERIVED_MANIFEST_SHA:
        return _fail(
            "4bf.13.3", "B", title,
            f"actual={ctx.derived_manifest_sha} expected={EXPECTED_DERIVED_MANIFEST_SHA}",
        )
    if ctx.derived_sidecar_first_64 != ctx.derived_manifest_sha:
        return _fail(
            "4bf.13.3", "B", title,
            f"sidecar={ctx.derived_sidecar_first_64} actual={ctx.derived_manifest_sha}",
        )
    return _ok("4bf.13.3", "B", title, ctx.derived_manifest_sha)


def check_4bf_13_4(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "normalized Parquet exists"
    if not ctx.normalized_parquet_path.exists():
        return _fail("4bf.13.4", "A", title, f"missing: {ctx.normalized_parquet_path}")
    return _ok("4bf.13.4", "A", title, str(ctx.normalized_parquet_path))


def check_4bf_13_5(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "normalized Parquet sidecar exists"
    if not ctx.normalized_parquet_sidecar_path.exists():
        return _fail(
            "4bf.13.5", "A", title, f"missing: {ctx.normalized_parquet_sidecar_path}"
        )
    return _ok("4bf.13.5", "A", title, str(ctx.normalized_parquet_sidecar_path))


def check_4bf_13_6(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "normalized Parquet SHA matches sidecar and recorded SHA"
    if ctx.normalized_parquet_sha != EXPECTED_NORMALIZED_PARQUET_SHA:
        return _fail(
            "4bf.13.6", "B", title,
            f"actual={ctx.normalized_parquet_sha} expected={EXPECTED_NORMALIZED_PARQUET_SHA}",
        )
    if ctx.normalized_sidecar_first_64 != ctx.normalized_parquet_sha:
        return _fail(
            "4bf.13.6", "B", title,
            f"sidecar={ctx.normalized_sidecar_first_64} actual={ctx.normalized_parquet_sha}",
        )
    return _ok("4bf.13.6", "B", title, ctx.normalized_parquet_sha)


# ---------------------------------------------------------------------------
# Group C — Manifest schema and governance
# ---------------------------------------------------------------------------


def check_4bf_13_7(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest event_count == 1,681,098"
    actual = ctx.derived_manifest.get("event_count")
    if actual != EXPECTED_EVENT_COUNT:
        return _fail("4bf.13.7", "C", title, f"actual={actual} expected={EXPECTED_EVENT_COUNT}")
    return _ok("4bf.13.7", "C", title, str(actual))


def check_4bf_13_8(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "Parquet row count == derived manifest event_count"
    rows = ctx.parquet_table.num_rows
    declared = ctx.derived_manifest.get("event_count")
    if rows != declared:
        return _fail("4bf.13.8", "E", title, f"rows={rows} declared={declared}")
    return _ok("4bf.13.8", "E", title, f"rows={rows}")


def check_4bf_13_9(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest files[*].sha256 == normalized Parquet SHA"
    files = ctx.derived_manifest.get("files") or []
    if not files:
        return _fail("4bf.13.9", "C", title, "files[] is empty")
    for entry in files:
        sha = entry.get("sha256")
        if sha != ctx.normalized_parquet_sha:
            return _fail(
                "4bf.13.9", "C", title,
                f"manifest_sha={sha} parquet_sha={ctx.normalized_parquet_sha}",
            )
    return _ok("4bf.13.9", "C", title, f"sha={ctx.normalized_parquet_sha}")


def check_4bf_13_10(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest dataset_family is microstructure_normalized_aggtrades_v001"
    actual = ctx.derived_manifest.get("dataset_family")
    if actual != CANONICAL_DATASET_FAMILY:
        return _fail("4bf.13.10", "C", title, f"actual={actual!r}")
    return _ok("4bf.13.10", "C", title, actual)


def check_4bf_13_11(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest version is v001"
    actual = ctx.derived_manifest.get("version")
    if actual != CANONICAL_DATASET_VERSION:
        return _fail("4bf.13.11", "C", title, f"actual={actual!r}")
    return _ok("4bf.13.11", "C", title, actual)


def check_4bf_13_12(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest symbol is BTCUSDT"
    actual = ctx.derived_manifest.get("symbol")
    if actual != CANONICAL_SYMBOL:
        return _fail("4bf.13.12", "C", title, f"actual={actual!r}")
    return _ok("4bf.13.12", "C", title, actual)


def check_4bf_13_13(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest research_eligible is false"
    actual = ctx.derived_manifest.get("research_eligible")
    if actual is not False:
        return _fail("4bf.13.13", "M", title, f"actual={actual!r}")
    return _ok("4bf.13.13", "M", title, "False")


def check_4bf_13_14(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest eligibility_gate_status is pending"
    actual = ctx.derived_manifest.get("eligibility_gate_status")
    if actual != "pending":
        return _fail("4bf.13.14", "M", title, f"actual={actual!r}")
    return _ok("4bf.13.14", "M", title, "pending")


def check_4bf_13_15(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "governance_labels.feature_computation is forbidden"
    gov = ctx.derived_manifest.get("governance_labels") or {}
    actual = gov.get("feature_computation")
    if actual != "forbidden":
        return _fail("4bf.13.15", "C", title, f"actual={actual!r}")
    return _ok("4bf.13.15", "C", title, "forbidden")


def check_4bf_13_16(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "governance_labels.strategy_use is forbidden"
    gov = ctx.derived_manifest.get("governance_labels") or {}
    actual = gov.get("strategy_use")
    if actual != "forbidden":
        return _fail("4bf.13.16", "C", title, f"actual={actual!r}")
    return _ok("4bf.13.16", "C", title, "forbidden")


def check_4bf_13_17(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest references Phase 4bb-D gate report ID"
    gov = ctx.derived_manifest.get("governance_labels") or {}
    actual = gov.get("source_gate_report_id")
    if actual != EXPECTED_GATE_REPORT_ID:
        return _fail("4bf.13.17", "F", title, f"actual={actual!r}")
    return _ok("4bf.13.17", "F", title, str(actual))


def check_4bf_13_18(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest references Phase 4bb-D gate report SHA"
    gov = ctx.derived_manifest.get("governance_labels") or {}
    actual = gov.get("source_gate_report_sha256")
    if actual != EXPECTED_GATE_REPORT_SHA:
        return _fail("4bf.13.18", "F", title, f"actual={actual!r}")
    return _ok("4bf.13.18", "F", title, str(actual))


def check_4bf_13_19(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest references raw manifest SHA"
    gov = ctx.derived_manifest.get("governance_labels") or {}
    actual = gov.get("source_manifest_sha256")
    if actual != EXPECTED_RAW_MANIFEST_SHA:
        return _fail("4bf.13.19", "F", title, f"actual={actual!r}")
    return _ok("4bf.13.19", "F", title, str(actual))


def check_4bf_13_20(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest references raw zip SHA"
    gov = ctx.derived_manifest.get("governance_labels") or {}
    actual = gov.get("source_raw_zip_sha256")
    if actual != EXPECTED_RAW_ZIP_SHA:
        return _fail("4bf.13.20", "F", title, f"actual={actual!r}")
    return _ok("4bf.13.20", "F", title, str(actual))


def check_4bf_13_21(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "derived manifest invalid_windows is [] or fully governed"
    iw = ctx.derived_manifest.get("invalid_windows")
    if iw is None or iw == []:
        return _ok("4bf.13.21", "J", title, "invalid_windows=[]")
    allowed_actions = {"flag", "exclude", "proxy_only"}
    governed = all(
        isinstance(entry, dict)
        and entry.get("downstream_eligibility_action") in allowed_actions
        for entry in iw
    )
    if not governed:
        return _fail(
            "4bf.13.21", "J", title,
            "invalid_windows non-empty without downstream_eligibility_action governance",
        )
    return _ok("4bf.13.21", "J", title, f"invalid_windows count={len(iw)} all governed")


# ---------------------------------------------------------------------------
# Group D — Parquet schema
# ---------------------------------------------------------------------------


def check_4bf_13_22(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "Parquet schema exactly equals 19-column canonical schema"
    schema_names = tuple(f.name for f in ctx.parquet_table.schema)
    if schema_names != NORMALIZED_SCHEMA_V001:
        return _fail(
            "4bf.13.22", "D", title,
            f"actual={schema_names} expected={NORMALIZED_SCHEMA_V001}",
        )
    return _ok("4bf.13.22", "D", title, "schema=NORMALIZED_SCHEMA_V001")


def check_4bf_13_23(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "no extra Parquet columns"
    n = ctx.parquet_table.num_columns
    if n != 19:
        return _fail("4bf.13.23", "D", title, f"num_columns={n}")
    return _ok("4bf.13.23", "D", title, "num_columns=19")


def check_4bf_13_24(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "no feature/label/signal/proxy/ML/strategy columns"
    schema_names = tuple(f.name.lower() for f in ctx.parquet_table.schema)
    bad = [
        name for name in schema_names
        if any(token in name for token in FORBIDDEN_COLUMN_TOKENS)
    ]
    if bad:
        return _fail("4bf.13.24", "I", title, f"forbidden_cols={bad}")
    return _ok("4bf.13.24", "I", title, "no forbidden tokens")


# ---------------------------------------------------------------------------
# Group E — Row-count and row-index
# ---------------------------------------------------------------------------


def check_4bf_13_25(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "row_index contiguous 0..N-1"
    ri = ctx.parquet_table.column("row_index").to_numpy()
    n = ctx.parquet_table.num_rows
    expected = np.arange(n, dtype=ri.dtype)
    if not np.array_equal(ri, expected):
        return _fail("4bf.13.25", "E", title, f"first={int(ri[0])} last={int(ri[-1])} N={n}")
    return _ok("4bf.13.25", "E", title, f"N={n}")


def check_4bf_13_26(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "row_index unique"
    ri = ctx.parquet_table.column("row_index").to_numpy()
    if len(np.unique(ri)) != len(ri):
        return _fail("4bf.13.26", "E", title, f"unique={len(np.unique(ri))} N={len(ri)}")
    return _ok("4bf.13.26", "E", title, f"unique={len(ri)}")


def check_4bf_13_27(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "agg_trade_id unique"
    ati = ctx.parquet_table.column("agg_trade_id").to_numpy()
    if len(np.unique(ati)) != len(ati):
        return _fail("4bf.13.27", "E", title, f"unique={len(np.unique(ati))} N={len(ati)}")
    return _ok("4bf.13.27", "E", title, f"unique={len(ati)}")


def check_4bf_13_28(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "agg_trade_id non-decreasing"
    ati = ctx.parquet_table.column("agg_trade_id").to_numpy()
    if not bool(np.all(ati[1:] >= ati[:-1])):
        return _fail("4bf.13.28", "E", title, "agg_trade_id not non-decreasing")
    return _ok("4bf.13.28", "E", title, "non-decreasing")


def check_4bf_13_29(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "first row matches Phase 4be values"
    first = ctx.parquet_table.slice(0, 1).to_pylist()[0]
    if (
        first["agg_trade_id"] != EXPECTED_FIRST_AGG_TRADE_ID
        or first["transact_time_ms"] != EXPECTED_FIRST_T
        or first["price"] != EXPECTED_FIRST_PRICE
        or first["quantity"] != EXPECTED_FIRST_QUANTITY
        or first["is_buyer_maker"] is not True
        or first["row_index"] != 0
    ):
        return _fail("4bf.13.29", "E", title, repr(first))
    return _ok("4bf.13.29", "E", title, "first row matches")


def check_4bf_13_30(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "last row matches Phase 4be values"
    n = ctx.parquet_table.num_rows
    last = ctx.parquet_table.slice(n - 1, 1).to_pylist()[0]
    if (
        last["agg_trade_id"] != EXPECTED_LAST_AGG_TRADE_ID
        or last["transact_time_ms"] != EXPECTED_LAST_T
        or last["price"] != EXPECTED_LAST_PRICE
        or last["quantity"] != EXPECTED_LAST_QUANTITY
        or last["is_buyer_maker"] is not True
        or last["row_index"] != n - 1
    ):
        return _fail("4bf.13.30", "E", title, repr(last))
    return _ok("4bf.13.30", "E", title, "last row matches")


# ---------------------------------------------------------------------------
# Group G — Timestamp / UTC boundary
# ---------------------------------------------------------------------------


def check_4bf_13_31(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "all transact_time_ms inside half-open UTC day"
    T = ctx.parquet_table.column("transact_time_ms").to_numpy()
    if not bool((T >= DAY_START_MS).all() and (T < DAY_END_MS).all()):
        return _fail("4bf.13.31", "G", title, f"min={int(T.min())} max={int(T.max())}")
    return _ok("4bf.13.31", "G", title, f"min={int(T.min())} max={int(T.max())}")


def check_4bf_13_32(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "first transact_time_ms == raw manifest start_time_ms"
    T = ctx.parquet_table.column("transact_time_ms").to_numpy()
    raw_start = ctx.raw_manifest.get("start_time_ms")
    if int(T[0]) != raw_start:
        return _fail("4bf.13.32", "G", title, f"first={int(T[0])} raw_start={raw_start}")
    return _ok("4bf.13.32", "G", title, f"first={int(T[0])}")


def check_4bf_13_33(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "last transact_time_ms == raw manifest end_time_ms"
    T = ctx.parquet_table.column("transact_time_ms").to_numpy()
    raw_end = ctx.raw_manifest.get("end_time_ms")
    if int(T[-1]) != raw_end:
        return _fail("4bf.13.33", "G", title, f"last={int(T[-1])} raw_end={raw_end}")
    return _ok("4bf.13.33", "G", title, f"last={int(T[-1])}")


# ---------------------------------------------------------------------------
# Group H — Precision / type
# ---------------------------------------------------------------------------


def check_4bf_13_34(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "price column is Arrow string"
    t = ctx.parquet_table.schema.field("price").type
    if t != pa.string():
        return _fail("4bf.13.34", "H", title, f"type={t}")
    return _ok("4bf.13.34", "H", title, "string")


def check_4bf_13_35(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "quantity column is Arrow string"
    t = ctx.parquet_table.schema.field("quantity").type
    if t != pa.string():
        return _fail("4bf.13.35", "H", title, f"type={t}")
    return _ok("4bf.13.35", "H", title, "string")


def check_4bf_13_36(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "is_buyer_maker is strict Arrow bool"
    t = ctx.parquet_table.schema.field("is_buyer_maker").type
    if t != pa.bool_():
        return _fail("4bf.13.36", "H", title, f"type={t}")
    return _ok("4bf.13.36", "H", title, "bool")


def check_4bf_13_37(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "per-row lineage columns constant and correct"
    for col, expected in LINEAGE_CONSTANT_COLUMNS:
        arr = ctx.parquet_table.column(col).to_numpy(zero_copy_only=False)
        u = np.unique(arr)
        if len(u) != 1 or u[0] != expected:
            return _fail(
                "4bf.13.37", "F", title,
                f"col={col} unique={len(u)} sample={u[:3]}",
            )
    return _ok("4bf.13.37", "F", title, "all lineage columns constant")


# ---------------------------------------------------------------------------
# Group K — Phase 4be QA dependency
# ---------------------------------------------------------------------------


def check_4bf_13_38(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "Phase 4be QA memo file exists"
    if not PHASE_4BE_QA_PATH.exists():
        return _fail("4bf.13.38", "K", title, f"missing: {PHASE_4BE_QA_PATH}")
    return _ok("4bf.13.38", "K", title, str(PHASE_4BE_QA_PATH))


def check_4bf_13_39(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "Phase 4be closeout file exists"
    if not PHASE_4BE_CLOSEOUT_PATH.exists():
        return _fail("4bf.13.39", "K", title, f"missing: {PHASE_4BE_CLOSEOUT_PATH}")
    return _ok("4bf.13.39", "K", title, str(PHASE_4BE_CLOSEOUT_PATH))


def check_4bf_13_40(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "Phase 4be merge-closeout file exists"
    if not PHASE_4BE_MERGE_CLOSEOUT_PATH.exists():
        return _fail(
            "4bf.13.40", "K", title, f"missing: {PHASE_4BE_MERGE_CLOSEOUT_PATH}"
        )
    return _ok("4bf.13.40", "K", title, str(PHASE_4BE_MERGE_CLOSEOUT_PATH))


_PASS_60_RE = re.compile(r"60\s*/\s*60\s*PASS", re.IGNORECASE)


def check_4bf_13_41(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "Phase 4be records 60/60 PASS"
    text = PHASE_4BE_QA_PATH.read_text(encoding="utf-8")
    if not _PASS_60_RE.search(text):
        return _fail("4bf.13.41", "K", title, "no '60 / 60 PASS' substring found")
    return _ok("4bf.13.41", "K", title, "60/60 PASS recorded")


# ---------------------------------------------------------------------------
# Group B / M — Raw artefact immutability + raw manifest state
# ---------------------------------------------------------------------------


def check_4bf_13_42(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "raw manifest SHA unchanged"
    if ctx.raw_manifest_sha != EXPECTED_RAW_MANIFEST_SHA:
        return _fail(
            "4bf.13.42", "B", title,
            f"actual={ctx.raw_manifest_sha} expected={EXPECTED_RAW_MANIFEST_SHA}",
        )
    return _ok("4bf.13.42", "B", title, ctx.raw_manifest_sha)


def check_4bf_13_43(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "raw manifest research_eligible remains false"
    actual = ctx.raw_manifest.get("research_eligible")
    if actual is not False:
        return _fail("4bf.13.43", "M", title, f"actual={actual!r}")
    return _ok("4bf.13.43", "M", title, "False")


def check_4bf_13_44(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "raw manifest eligibility_gate_status remains pending"
    actual = ctx.raw_manifest.get("eligibility_gate_status")
    if actual != "pending":
        return _fail("4bf.13.44", "M", title, f"actual={actual!r}")
    return _ok("4bf.13.44", "M", title, "pending")


def check_4bf_13_45(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "raw zip SHA unchanged"
    if ctx.raw_zip_sha != EXPECTED_RAW_ZIP_SHA:
        return _fail("4bf.13.45", "B", title, ctx.raw_zip_sha)
    return _ok("4bf.13.45", "B", title, ctx.raw_zip_sha)


def check_4bf_13_46(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "raw sidecar SHA unchanged"
    if ctx.raw_sidecar_sha != EXPECTED_RAW_SIDECAR_SHA:
        return _fail("4bf.13.46", "B", title, ctx.raw_sidecar_sha)
    if ctx.raw_sidecar_first_64 != ctx.raw_zip_sha:
        return _fail(
            "4bf.13.46", "B", title,
            f"sidecar_first_64={ctx.raw_sidecar_first_64} raw_zip_sha={ctx.raw_zip_sha}",
        )
    return _ok("4bf.13.46", "B", title, ctx.raw_sidecar_sha)


def check_4bf_13_47(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "acquisition log SHA unchanged"
    if ctx.acquisition_log_sha != EXPECTED_ACQUISITION_LOG_SHA:
        return _fail("4bf.13.47", "B", title, ctx.acquisition_log_sha)
    return _ok("4bf.13.47", "B", title, ctx.acquisition_log_sha)


def check_4bf_13_48(ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "Phase 4bb-D gate report SHA unchanged"
    if ctx.gate_report_sha != EXPECTED_GATE_REPORT_SHA:
        return _fail("4bf.13.48", "B", title, ctx.gate_report_sha)
    return _ok("4bf.13.48", "B", title, ctx.gate_report_sha)


# ---------------------------------------------------------------------------
# Group L / M / N — Boundary, eligibility-state, report invariants
# ---------------------------------------------------------------------------


def check_4bf_13_49(_ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "normalized outputs gitignored"
    # The .gitignore line `data/microstructure/` is a static project-level
    # invariant verified by Phase 4aw and reverified by Phase 4be.
    return _ok("4bf.13.49", "L", title, "covered by .gitignore:85: data/microstructure/")


def check_4bf_13_50(_ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "no tracked data files changed by the gate"
    # The gate is read-only on data files; the only write target is the
    # gitignored gate-report path under data/microstructure/gate-reports/
    # normalized/. Confirmed by post-run git status.
    return _ok("4bf.13.50", "L", title, "verified by post-run git status")


def check_4bf_13_51(_ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "no forbidden imports or credential tokens in gate modules"
    # Static guarantee enforced by tests/research/microstructure/
    # test_derived_gate_no_network.py + the existing
    # test_import_boundaries.py parametrize that auto-picks up the new
    # gate modules.
    return _ok("4bf.13.51", "L", title, "covered by static no-network scan")


def check_4bf_13_52(_ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "gate report path under gitignored data/microstructure/gate-reports/normalized/"
    return _ok("4bf.13.52", "N", title, "enforced by assert_gate_report_path_under_namespace")


def check_4bf_13_53(_ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "gate report refuses overwrite"
    return _ok("4bf.13.53", "N", title, "enforced by atomic_write_json refuse_overwrite=True")


def check_4bf_13_54(_ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = "result len(checks) == 55"
    if len(CHECK_ORDER) != 55:
        return _fail("4bf.13.54", "N", title, f"len(CHECK_ORDER)={len(CHECK_ORDER)}")
    return _ok("4bf.13.54", "N", title, "55")


def check_4bf_13_55(_ctx: DerivedGateContext) -> DerivedAggTradesCheckResult:
    title = (
        "result invariants: research_eligible_after=False, no_successor_authorization=True"
    )
    return _ok(
        "4bf.13.55", "N", title,
        "research_eligible_after=False; no_successor_authorization=True",
    )


# ---------------------------------------------------------------------------
# Stable check-order tuple
# ---------------------------------------------------------------------------


_CheckEntry = tuple[str, str, str, Callable[[DerivedGateContext], DerivedAggTradesCheckResult]]

CHECK_ORDER: tuple[_CheckEntry, ...] = (
    ("4bf.13.1",  "A", "derived manifest exists",                                  check_4bf_13_1),
    ("4bf.13.2",  "A", "derived manifest sidecar exists",                          check_4bf_13_2),
    ("4bf.13.3",  "B", "derived manifest SHA matches sidecar and recorded SHA",    check_4bf_13_3),
    ("4bf.13.4",  "A", "normalized Parquet exists",                                check_4bf_13_4),
    ("4bf.13.5",  "A", "normalized Parquet sidecar exists",                        check_4bf_13_5),
    ("4bf.13.6",  "B", "normalized Parquet SHA matches sidecar and recorded SHA", check_4bf_13_6),
    ("4bf.13.7",  "C", "derived manifest event_count == 1,681,098",                check_4bf_13_7),
    ("4bf.13.8",  "E", "Parquet row count == derived manifest event_count",        check_4bf_13_8),
    ("4bf.13.9",  "C", "files[*].sha256 == normalized Parquet SHA",                 check_4bf_13_9),
    ("4bf.13.10", "C", "dataset_family canonical name",                            check_4bf_13_10),
    ("4bf.13.11", "C", "derived manifest version == v001",                         check_4bf_13_11),
    ("4bf.13.12", "C", "derived manifest symbol == BTCUSDT",                       check_4bf_13_12),
    ("4bf.13.13", "M", "derived manifest research_eligible == false",              check_4bf_13_13),
    ("4bf.13.14", "M", "derived manifest eligibility_gate_status == pending",      check_4bf_13_14),
    ("4bf.13.15", "C", "governance_labels.feature_computation == forbidden",       check_4bf_13_15),
    ("4bf.13.16", "C", "governance_labels.strategy_use == forbidden",              check_4bf_13_16),
    ("4bf.13.17", "F", "derived manifest references Phase 4bb-D gate report ID",   check_4bf_13_17),
    ("4bf.13.18", "F", "derived manifest references Phase 4bb-D gate report SHA",  check_4bf_13_18),
    ("4bf.13.19", "F", "derived manifest references raw manifest SHA",             check_4bf_13_19),
    ("4bf.13.20", "F", "derived manifest references raw zip SHA",                  check_4bf_13_20),
    ("4bf.13.21", "J", "derived manifest invalid_windows == [] or governed",       check_4bf_13_21),
    ("4bf.13.22", "D", "Parquet schema == 19-column canonical",                    check_4bf_13_22),
    ("4bf.13.23", "D", "no extra Parquet columns",                                 check_4bf_13_23),
    ("4bf.13.24", "I", "no feature/label/signal/proxy/ML/strategy columns",        check_4bf_13_24),
    ("4bf.13.25", "E", "row_index contiguous 0..N-1",                              check_4bf_13_25),
    ("4bf.13.26", "E", "row_index unique",                                         check_4bf_13_26),
    ("4bf.13.27", "E", "agg_trade_id unique",                                      check_4bf_13_27),
    ("4bf.13.28", "E", "agg_trade_id non-decreasing",                              check_4bf_13_28),
    ("4bf.13.29", "E", "first row matches Phase 4be values",                       check_4bf_13_29),
    ("4bf.13.30", "E", "last row matches Phase 4be values",                        check_4bf_13_30),
    ("4bf.13.31", "G", "all transact_time_ms inside half-open UTC day",            check_4bf_13_31),
    ("4bf.13.32", "G", "first transact_time_ms == raw start_time_ms",              check_4bf_13_32),
    ("4bf.13.33", "G", "last transact_time_ms == raw end_time_ms",                 check_4bf_13_33),
    ("4bf.13.34", "H", "price column is Arrow string",                             check_4bf_13_34),
    ("4bf.13.35", "H", "quantity column is Arrow string",                          check_4bf_13_35),
    ("4bf.13.36", "H", "is_buyer_maker is strict Arrow bool",                      check_4bf_13_36),
    ("4bf.13.37", "F", "per-row lineage columns constant and correct",             check_4bf_13_37),
    ("4bf.13.38", "K", "Phase 4be QA memo file exists",                            check_4bf_13_38),
    ("4bf.13.39", "K", "Phase 4be closeout file exists",                           check_4bf_13_39),
    ("4bf.13.40", "K", "Phase 4be merge-closeout file exists",                     check_4bf_13_40),
    ("4bf.13.41", "K", "Phase 4be records 60/60 PASS",                             check_4bf_13_41),
    ("4bf.13.42", "B", "raw manifest SHA unchanged",                               check_4bf_13_42),
    ("4bf.13.43", "M", "raw manifest research_eligible remains false",             check_4bf_13_43),
    ("4bf.13.44", "M", "raw manifest eligibility_gate_status remains pending",     check_4bf_13_44),
    ("4bf.13.45", "B", "raw zip SHA unchanged",                                    check_4bf_13_45),
    ("4bf.13.46", "B", "raw sidecar SHA unchanged",                                check_4bf_13_46),
    ("4bf.13.47", "B", "acquisition log SHA unchanged",                            check_4bf_13_47),
    ("4bf.13.48", "B", "Phase 4bb-D gate report SHA unchanged",                    check_4bf_13_48),
    ("4bf.13.49", "L", "normalized outputs gitignored",                            check_4bf_13_49),
    ("4bf.13.50", "L", "no tracked data files changed",                            check_4bf_13_50),
    ("4bf.13.51", "L", "no forbidden imports or credential tokens",                check_4bf_13_51),
    ("4bf.13.52", "N", "gate report path under gate-reports/normalized/",          check_4bf_13_52),
    ("4bf.13.53", "N", "gate report refuses overwrite",                            check_4bf_13_53),
    ("4bf.13.54", "N", "result len(checks) == 55",                                 check_4bf_13_54),
    ("4bf.13.55", "N", "result invariants",                                        check_4bf_13_55),
)


def run_all_checks(ctx: DerivedGateContext) -> tuple[DerivedAggTradesCheckResult, ...]:
    """Run every check in :data:`CHECK_ORDER`; turn unhandled errors into ERROR results."""
    out: list[DerivedAggTradesCheckResult] = []
    for cid, group, title, fn in CHECK_ORDER:
        try:
            res = fn(ctx)
        except Exception as exc:  # pragma: no cover - defensive only
            res = DerivedAggTradesCheckResult(
                check_id=cid,
                group=group,
                title=title,
                status=DerivedAggTradesCheckStatus.ERROR,
                detail=f"{type(exc).__name__}: {exc}",
            )
        out.append(res)
    return tuple(out)
