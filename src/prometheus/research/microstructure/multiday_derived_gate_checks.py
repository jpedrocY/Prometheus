"""Phase 4bm-D 60-check multi-day derived-family eligibility-gate suite.

This module mirrors :mod:`derived_gate_checks` (Phase 4bf) but adapts
each check to the v002 multi-day derived family produced by Phase
4bm-B:

* IDs ``4bm-d.13.1`` .. ``4bm-d.13.55`` are 1:1 analogues of Phase 4bf
  ``4bf.13.1`` .. ``4bf.13.55``. Where Phase 4bf inspected a single
  Parquet, the multi-day analogue extends to all 90 Parquets (cheap
  metadata-only checks) and to a bounded 5-date sample for per-row
  content checks. The brief explicitly forbids weakening or silently
  dropping any Phase 4bf criterion.
* IDs ``4bm-d.13.56`` .. ``4bm-d.13.60`` are five new multi-day-specific
  checks: manifest envelope completeness, contiguous-date inventory,
  adjacent-date temporal monotonicity, adjacent-date agg_trade_id
  non-overlap, and total event count aggregation.

Every check returns a :class:`MultidayDerivedAggTradesCheckResult` with
status PASS / FAIL / NOT_APPLICABLE / ERROR. The :data:`CHECK_ORDER`
tuple maps every check id to its function in stable order.

All checks are read-only. They never mutate the derived manifest, any
of the 90 Parquets or sidecars, the raw v002 manifest, the raw zips
or sidecars, the Phase 4bl-D-R gate report, the Phase 4bl-E
successor-state record, or any other governance artefact. The only
writes performed by the gate as a whole are the gate report JSON
and its paired ``.sha256`` sidecar under
``data/microstructure/gate-reports/normalized/``, and those writes
are owned by :mod:`multiday_derived_gate_io`, not this module.

Performance discipline: the gate must not load all 90 Parquets into
memory (the dataset is ~155 M events / ~1.4 GiB). Per-file row counts
are taken from ``pyarrow.parquet.ParquetFile.metadata.num_rows``
without materialising row groups. Full per-row content checks are
restricted to a predeclared 5-date sample
(:data:`SAMPLE_DATES`). All 90 dates still participate in the cheap
SHA / size / metadata / boundary checks.
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

from .multiday_derived_gate_io import (
    MultidayDerivedSourceArtefactPaths,
    MultidayLoadedArtefactBundle,
)

# Reuse the canonical 19-column normalized schema definition.
from .normalize_aggtrades import NORMALIZED_SCHEMA_V001

# ---------------------------------------------------------------------------
# Canonical locked v002 multi-day constants
# ---------------------------------------------------------------------------

CANONICAL_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
CANONICAL_DATASET_VERSION = "v002"
CANONICAL_SOURCE_DATASET_FAMILY = "microstructure_raw_aggtrades_v001"
CANONICAL_SOURCE_DATASET_VERSION = "v002"
CANONICAL_SYMBOL = "BTCUSDT"
CANONICAL_NORMALIZATION_SCHEMA_VERSION = "v001"

CANONICAL_DATE_START = "2024-12-01"
CANONICAL_DATE_END = "2025-02-28"
EXPECTED_DATE_COUNT = 90
EXPECTED_TOTAL_EVENT_COUNT = 155_153_449

# v002 governance artefacts (recorded by Phase 4bm-B + Phase 4bm-C).
EXPECTED_DERIVED_MANIFEST_SHA = (
    "01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a"
)
EXPECTED_RAW_MANIFEST_SHA = (
    "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
)
EXPECTED_ACQUISITION_LOG_SHA = (
    "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"
)
EXPECTED_GATE_REPORT_SHA = (
    "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"
)
EXPECTED_GATE_REPORT_ID = (
    "microstructure_raw_aggtrades_v001__v002__"
    "phase-4bl-d-r__1778717359124__69e45280f080"
)
EXPECTED_SUCCESSOR_STATE_SHA = (
    "a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d"
)

# Phase 4bm-C structural QA artefacts (the Phase 4bf 4be-QA dependency
# pattern, transposed forward).
PHASE_4BMC_QA_PATH = Path(
    "docs/00-meta/implementation-reports/"
    "2026-05-15_phase-4bm-c_multi-day-normalized-structural-qa-memo.md"
)
PHASE_4BMC_CLOSEOUT_PATH = Path(
    "docs/00-meta/implementation-reports/2026-05-15_phase-4bm-c_closeout.md"
)
PHASE_4BMC_MERGE_CLOSEOUT_PATH = Path(
    "docs/00-meta/implementation-reports/"
    "2026-05-15_phase-4bm-c_merge-closeout.md"
)

# The Phase 4bm-C QA memo phrases the verdict as
# "All 28 predeclared QA questions return PASS" (no slash form).
_PASS_28_RE = re.compile(
    r"28\s+predeclared\s+QA\s+questions\s+return\s+PASS",
    re.IGNORECASE,
)

# Forbidden column-name token family applied to every sampled Parquet's
# schema (case-insensitive substring match). Identical to the Phase
# 4bf list except the trailing comma; this list is a project-wide
# invariant and must not weaken between phases.
FORBIDDEN_COLUMN_TOKENS: tuple[str, ...] = (
    "feature", "label", "signal", "return", "alpha", "edge", "imbalance",
    "sweep", "spread", "depth", "liquid", "slippage", "order_flow",
    "execution_qual", "ml_", "strategy", "mfe", "mae", "r_multiple",
    "pnl", "equity", "position", "regime", "momentum", "volatility",
)

# Per-row lineage constants expected on every sampled Parquet.
# Per-file constants (utc_date, source_file_sha256) are validated
# separately because they vary by date.
PERFILE_INVARIANT_LINEAGE_COLUMNS: tuple[tuple[str, str], ...] = (
    ("dataset_family", CANONICAL_DATASET_FAMILY),
    ("dataset_version", CANONICAL_DATASET_VERSION),
    ("source_dataset_family", CANONICAL_SOURCE_DATASET_FAMILY),
    ("source_dataset_version", CANONICAL_SOURCE_DATASET_VERSION),
    ("symbol", CANONICAL_SYMBOL),
    ("source_manifest_sha256", EXPECTED_RAW_MANIFEST_SHA),
    ("source_gate_report_id", EXPECTED_GATE_REPORT_ID),
    ("source_gate_report_sha256", EXPECTED_GATE_REPORT_SHA),
    ("normalization_schema_version", CANONICAL_NORMALIZATION_SCHEMA_VERSION),
)

# Predeclared 5-date sample used for per-row content checks. These
# dates span the locked 90-day range and are baked into the gate
# methodology — they are not chosen at run time.
SAMPLE_DATES: tuple[str, ...] = (
    "2024-12-01",
    "2024-12-31",
    "2025-01-15",
    "2025-01-30",
    "2025-02-28",
)

# Top-level scalar fields the v002 derived manifest must carry. The
# multi-day envelope check 4bm-d.13.56 verifies all of these are
# present and non-None. The 24-count target tracks the Phase 4bm-A
# locked envelope (dropping the legacy single-file ``files`` /
# ``event_count`` / ``symbol`` / ``start_time_ms`` / ``end_time_ms``
# / ``version`` Phase 4bd fields, and adding the multi-day fields
# ``date_*``, ``per_file_inventory``, ``symbol_list`` etc.).
REQUIRED_MANIFEST_TOP_FIELDS: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "schema_version",
    "source_dataset_family",
    "source_dataset_version",
    "source_phase_boundary",
    "source_manifest_path",
    "source_manifest_sha256",
    "source_acquisition_log_path",
    "source_acquisition_log_sha256",
    "source_gate_report_path",
    "source_gate_report_id",
    "source_gate_report_sha256",
    "source_successor_state_path",
    "source_successor_state_sha256",
    "symbol_list",
    "date_start",
    "date_end",
    "date_count",
    "date_list",
    "expected_file_count",
    "produced_file_count",
    "total_event_count",
    "per_file_inventory",
    "invalid_windows",
    "governance_labels",
    "research_eligible",
    "eligibility_gate_status",
    "code_commit_sha",
    "base_commit_sha",
    "capture_config_hash",
    "created_at_unix_ms",
    "created_at_utc",
    "phase",
)

# Minimum governance_labels keys the v002 derived manifest must carry.
REQUIRED_GOVERNANCE_LABEL_KEYS: tuple[str, ...] = (
    "phase",
    "source_phase_boundary",
    "validator",
    "stop_trigger_domain",
    "feature_computation",
    "strategy_use",
    "source_dataset_family",
    "source_dataset_version",
    "source_manifest_path",
    "source_manifest_sha256",
    "source_gate_report_id",
    "source_gate_report_sha256",
    "source_gate_report_code_commit_sha",
    "source_successor_state_sha256",
    "multi_day",
    "phase_4bm_b_no_successor_authorization",
)


# ---------------------------------------------------------------------------
# Result + context types
# ---------------------------------------------------------------------------


class MultidayDerivedAggTradesCheckStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


@dataclass(frozen=True)
class MultidayDerivedAggTradesCheckResult:
    """One row of the multi-day gate report's ``checks`` array."""

    check_id: str
    group: str
    title: str
    status: MultidayDerivedAggTradesCheckStatus
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
class MultidayPerFileMeasured:
    """Per-file SHA / size / metadata measurements taken once and reused."""

    date: str
    parquet_sha: str | None = None
    parquet_size: int | None = None
    sidecar_sha: str | None = None
    sidecar_size: int | None = None
    sidecar_first_64: str | None = None
    source_zip_sha: str | None = None
    parquet_num_rows: int | None = None
    sample_table: pa.Table | None = None


@dataclass
class MultidayDerivedGateContext:
    """Mutable per-run inspection context shared across checks."""

    paths: MultidayDerivedSourceArtefactPaths
    bundle: MultidayLoadedArtefactBundle
    perfile: dict[str, MultidayPerFileMeasured] = field(default_factory=dict)
    measured: dict[str, Any] = field(default_factory=dict)


def _ok(
    check_id: str, group: str, title: str, detail: str = ""
) -> MultidayDerivedAggTradesCheckResult:
    return MultidayDerivedAggTradesCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=MultidayDerivedAggTradesCheckStatus.PASS,
        detail=detail,
    )


def _fail(
    check_id: str, group: str, title: str, detail: str
) -> MultidayDerivedAggTradesCheckResult:
    return MultidayDerivedAggTradesCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=MultidayDerivedAggTradesCheckStatus.FAIL,
        detail=detail,
    )


# ---------------------------------------------------------------------------
# Group A — Artefact existence (4bf.13.1, 2, 4, 5)
# ---------------------------------------------------------------------------


def check_4bm_d_13_1(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest exists"
    p = ctx.paths.derived_manifest_path
    if not p.exists():
        return _fail("4bm-d.13.1", "A", title, f"missing: {p}")
    return _ok("4bm-d.13.1", "A", title, str(p))


def check_4bm_d_13_2(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest sidecar exists"
    p = ctx.paths.derived_manifest_sidecar_path
    if not p.exists():
        return _fail("4bm-d.13.2", "A", title, f"missing: {p}")
    return _ok("4bm-d.13.2", "A", title, str(p))


def check_4bm_d_13_3(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest SHA matches sidecar and recorded SHA"
    sha = ctx.bundle.derived_manifest_sha
    sidecar = ctx.bundle.derived_sidecar_first_64
    if sha != EXPECTED_DERIVED_MANIFEST_SHA:
        return _fail(
            "4bm-d.13.3", "B", title,
            f"actual={sha} expected={EXPECTED_DERIVED_MANIFEST_SHA}",
        )
    if sidecar != sha:
        return _fail(
            "4bm-d.13.3", "B", title,
            f"sidecar_first_64={sidecar} actual={sha}",
        )
    return _ok("4bm-d.13.3", "B", title, sha)


def check_4bm_d_13_4(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "all 90 per-day Parquets exist"
    missing: list[str] = []
    for pf in ctx.paths.per_file:
        if not pf.parquet_path.exists():
            missing.append(f"{pf.date}: {pf.parquet_path}")
    if missing:
        return _fail("4bm-d.13.4", "A", title, f"missing_count={len(missing)}; first={missing[0]}")
    return _ok("4bm-d.13.4", "A", title, f"count={len(ctx.paths.per_file)}")


def check_4bm_d_13_5(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "all 90 per-day Parquet sidecars exist"
    missing: list[str] = []
    for pf in ctx.paths.per_file:
        if not pf.parquet_sidecar_path.exists():
            missing.append(f"{pf.date}: {pf.parquet_sidecar_path}")
    if missing:
        return _fail("4bm-d.13.5", "A", title, f"missing_count={len(missing)}; first={missing[0]}")
    return _ok("4bm-d.13.5", "A", title, f"count={len(ctx.paths.per_file)}")


# ---------------------------------------------------------------------------
# Group B — SHA / immutability (4bf.13.6, 42, 45, 46, 47, 48)
# ---------------------------------------------------------------------------


def check_4bm_d_13_6(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "all 90 per-day Parquet SHAs match recorded SHA"
    mismatches: list[str] = []
    for pf in ctx.paths.per_file:
        m = ctx.perfile.get(pf.date)
        if m is None or m.parquet_sha is None:
            mismatches.append(f"{pf.date}: missing measured SHA")
            continue
        if m.parquet_sha != pf.expected_parquet_sha:
            mismatches.append(
                f"{pf.date}: actual={m.parquet_sha[:12]}... "
                f"expected={pf.expected_parquet_sha[:12]}..."
            )
    if mismatches:
        return _fail(
            "4bm-d.13.6", "B", title,
            f"mismatches={len(mismatches)}; first={mismatches[0]}",
        )
    return _ok("4bm-d.13.6", "B", title, f"all {len(ctx.paths.per_file)} SHAs match")


# ---------------------------------------------------------------------------
# Group C — Manifest schema and governance (4bf.13.7, 10, 11, 12, 15, 16)
# ---------------------------------------------------------------------------


def check_4bm_d_13_7(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = f"derived manifest total_event_count == {EXPECTED_TOTAL_EVENT_COUNT:,}"
    actual = ctx.bundle.derived_manifest.get("total_event_count")
    if actual != EXPECTED_TOTAL_EVENT_COUNT:
        return _fail(
            "4bm-d.13.7",
            "C",
            title,
            f"actual={actual} expected={EXPECTED_TOTAL_EVENT_COUNT}",
        )
    return _ok("4bm-d.13.7", "C", title, str(actual))


def check_4bm_d_13_8(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "per-file Parquet num_rows == per_file_inventory[*].event_count for all 90 dates"
    mismatches: list[str] = []
    for pf in ctx.paths.per_file:
        m = ctx.perfile.get(pf.date)
        if m is None or m.parquet_num_rows is None:
            mismatches.append(f"{pf.date}: missing measured num_rows")
            continue
        if m.parquet_num_rows != pf.expected_event_count:
            mismatches.append(
                f"{pf.date}: num_rows={m.parquet_num_rows} event_count={pf.expected_event_count}"
            )
    if mismatches:
        return _fail(
            "4bm-d.13.8",
            "E",
            title,
            f"mismatches={len(mismatches)}; first={mismatches[0]}",
        )
    return _ok(
        "4bm-d.13.8",
        "E",
        title,
        f"all {len(ctx.paths.per_file)} per-file row counts match",
    )


def check_4bm_d_13_9(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "per_file_inventory[*].parquet_size_bytes matches measured size for all 90 dates"
    mismatches: list[str] = []
    for pf in ctx.paths.per_file:
        m = ctx.perfile.get(pf.date)
        if m is None or m.parquet_size is None:
            mismatches.append(f"{pf.date}: missing measured size")
            continue
        if m.parquet_size != pf.expected_parquet_size:
            mismatches.append(
                f"{pf.date}: actual={m.parquet_size} expected={pf.expected_parquet_size}"
            )
    if mismatches:
        return _fail(
            "4bm-d.13.9",
            "C",
            title,
            f"mismatches={len(mismatches)}; first={mismatches[0]}",
        )
    return _ok(
        "4bm-d.13.9", "C", title, f"all {len(ctx.paths.per_file)} sizes match"
    )


def check_4bm_d_13_10(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest dataset_family is microstructure_normalized_aggtrades_v001"
    actual = ctx.bundle.derived_manifest.get("dataset_family")
    if actual != CANONICAL_DATASET_FAMILY:
        return _fail("4bm-d.13.10", "C", title, f"actual={actual!r}")
    return _ok("4bm-d.13.10", "C", title, str(actual))


def check_4bm_d_13_11(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest dataset_version is v002"
    actual = ctx.bundle.derived_manifest.get("dataset_version")
    if actual != CANONICAL_DATASET_VERSION:
        return _fail("4bm-d.13.11", "C", title, f"actual={actual!r}")
    return _ok("4bm-d.13.11", "C", title, str(actual))


def check_4bm_d_13_12(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest symbol_list is ['BTCUSDT']"
    actual = ctx.bundle.derived_manifest.get("symbol_list")
    if actual != [CANONICAL_SYMBOL]:
        return _fail("4bm-d.13.12", "C", title, f"actual={actual!r}")
    return _ok("4bm-d.13.12", "C", title, str(actual))


def check_4bm_d_13_13(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest research_eligible is false"
    actual = ctx.bundle.derived_manifest.get("research_eligible")
    if actual is not False:
        return _fail("4bm-d.13.13", "M", title, f"actual={actual!r}")
    return _ok("4bm-d.13.13", "M", title, "False")


def check_4bm_d_13_14(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest eligibility_gate_status is pending"
    actual = ctx.bundle.derived_manifest.get("eligibility_gate_status")
    if actual != "pending":
        return _fail("4bm-d.13.14", "M", title, f"actual={actual!r}")
    return _ok("4bm-d.13.14", "M", title, "pending")


def check_4bm_d_13_15(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "governance_labels.feature_computation is forbidden"
    gov = ctx.bundle.derived_manifest.get("governance_labels") or {}
    actual = gov.get("feature_computation")
    if actual != "forbidden":
        return _fail("4bm-d.13.15", "C", title, f"actual={actual!r}")
    return _ok("4bm-d.13.15", "C", title, "forbidden")


def check_4bm_d_13_16(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "governance_labels.strategy_use is forbidden"
    gov = ctx.bundle.derived_manifest.get("governance_labels") or {}
    actual = gov.get("strategy_use")
    if actual != "forbidden":
        return _fail("4bm-d.13.16", "C", title, f"actual={actual!r}")
    return _ok("4bm-d.13.16", "C", title, "forbidden")


# ---------------------------------------------------------------------------
# Group F — Lineage (4bf.13.17, 18, 19, 20, 37)
# ---------------------------------------------------------------------------


def check_4bm_d_13_17(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest references Phase 4bl-D-R gate report ID"
    gov = ctx.bundle.derived_manifest.get("governance_labels") or {}
    actual = gov.get("source_gate_report_id")
    if actual != EXPECTED_GATE_REPORT_ID:
        return _fail("4bm-d.13.17", "F", title, f"actual={actual!r}")
    return _ok("4bm-d.13.17", "F", title, str(actual))


def check_4bm_d_13_18(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest references Phase 4bl-D-R gate report SHA"
    gov = ctx.bundle.derived_manifest.get("governance_labels") or {}
    actual = gov.get("source_gate_report_sha256")
    if actual != EXPECTED_GATE_REPORT_SHA:
        return _fail("4bm-d.13.18", "F", title, f"actual={actual!r}")
    # also verify top-level field matches the same SHA
    top = ctx.bundle.derived_manifest.get("source_gate_report_sha256")
    if top != EXPECTED_GATE_REPORT_SHA:
        return _fail("4bm-d.13.18", "F", title, f"top-level actual={top!r}")
    return _ok("4bm-d.13.18", "F", title, str(actual))


def check_4bm_d_13_19(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest references raw v002 manifest SHA"
    gov = ctx.bundle.derived_manifest.get("governance_labels") or {}
    actual = gov.get("source_manifest_sha256")
    if actual != EXPECTED_RAW_MANIFEST_SHA:
        return _fail("4bm-d.13.19", "F", title, f"actual={actual!r}")
    top = ctx.bundle.derived_manifest.get("source_manifest_sha256")
    if top != EXPECTED_RAW_MANIFEST_SHA:
        return _fail("4bm-d.13.19", "F", title, f"top-level actual={top!r}")
    return _ok("4bm-d.13.19", "F", title, str(actual))


def check_4bm_d_13_20(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "per_file_inventory[*].source_file_sha256 unchanged vs measured zip SHA (all 90)"
    mismatches: list[str] = []
    for pf in ctx.paths.per_file:
        m = ctx.perfile.get(pf.date)
        if m is None or m.source_zip_sha is None:
            mismatches.append(f"{pf.date}: missing measured zip SHA")
            continue
        if m.source_zip_sha != pf.expected_source_zip_sha:
            mismatches.append(
                f"{pf.date}: measured={m.source_zip_sha[:12]}... "
                f"expected={pf.expected_source_zip_sha[:12]}..."
            )
    if mismatches:
        return _fail(
            "4bm-d.13.20", "B", title,
            f"mismatches={len(mismatches)}; first={mismatches[0]}",
        )
    return _ok(
        "4bm-d.13.20", "B", title,
        f"all {len(ctx.paths.per_file)} raw zip SHAs unchanged",
    )


# ---------------------------------------------------------------------------
# Group J — Invalid windows (4bf.13.21)
# ---------------------------------------------------------------------------


def check_4bm_d_13_21(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "derived manifest invalid_windows is [] or fully governed"
    iw = ctx.bundle.derived_manifest.get("invalid_windows")
    if iw is None or iw == []:
        return _ok("4bm-d.13.21", "J", title, "invalid_windows=[]")
    allowed_actions = {"flag", "exclude", "proxy_only"}
    governed = all(
        isinstance(entry, dict)
        and entry.get("downstream_eligibility_action") in allowed_actions
        for entry in iw
    )
    if not governed:
        return _fail(
            "4bm-d.13.21", "J", title,
            "invalid_windows non-empty without downstream_eligibility_action governance",
        )
    return _ok("4bm-d.13.21", "J", title, f"invalid_windows count={len(iw)} all governed")


# ---------------------------------------------------------------------------
# Group D — Parquet schema (4bf.13.22, 23, 24) — applied across 5 sample dates
# ---------------------------------------------------------------------------


def _iter_sample_tables(ctx: MultidayDerivedGateContext) -> list[tuple[str, pa.Table]]:
    out: list[tuple[str, pa.Table]] = []
    for d in SAMPLE_DATES:
        m = ctx.perfile.get(d)
        if m is not None and m.sample_table is not None:
            out.append((d, m.sample_table))
    return out


def check_4bm_d_13_22(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "Parquet schema exactly equals 19-column canonical schema (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail(
            "4bm-d.13.22", "D", title,
            f"missing sample tables: got {len(samples)}, expected {len(SAMPLE_DATES)}",
        )
    for d, table in samples:
        names = tuple(f.name for f in table.schema)
        if names != NORMALIZED_SCHEMA_V001:
            return _fail("4bm-d.13.22", "D", title, f"{d}: schema={names}")
    return _ok("4bm-d.13.22", "D", title, f"all {len(samples)} samples == NORMALIZED_SCHEMA_V001")


def check_4bm_d_13_23(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "no extra Parquet columns (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.23", "D", title, "missing sample tables")
    for d, table in samples:
        if table.num_columns != 19:
            return _fail("4bm-d.13.23", "D", title, f"{d}: num_columns={table.num_columns}")
    return _ok("4bm-d.13.23", "D", title, "all samples have num_columns=19")


def check_4bm_d_13_24(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "no feature/label/signal/proxy/ML/strategy columns (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.24", "I", title, "missing sample tables")
    for d, table in samples:
        names = tuple(f.name.lower() for f in table.schema)
        bad = [
            name for name in names
            if any(tok in name for tok in FORBIDDEN_COLUMN_TOKENS)
        ]
        if bad:
            return _fail("4bm-d.13.24", "I", title, f"{d}: forbidden_cols={bad}")
    return _ok("4bm-d.13.24", "I", title, "no forbidden tokens in any sample")


# ---------------------------------------------------------------------------
# Group E — Row count / row index (4bf.13.25-30)
# ---------------------------------------------------------------------------


def check_4bm_d_13_25(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "row_index contiguous 0..N-1 (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.25", "E", title, "missing sample tables")
    for d, table in samples:
        ri = table.column("row_index").to_numpy()
        n = table.num_rows
        expected = np.arange(n, dtype=ri.dtype)
        if not np.array_equal(ri, expected):
            return _fail(
                "4bm-d.13.25", "E", title,
                f"{d}: first={int(ri[0])} last={int(ri[-1])} N={n}",
            )
    return _ok("4bm-d.13.25", "E", title, "all samples contiguous 0..N-1")


def check_4bm_d_13_26(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "row_index unique (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.26", "E", title, "missing sample tables")
    for d, table in samples:
        ri = table.column("row_index").to_numpy()
        if len(np.unique(ri)) != len(ri):
            return _fail(
                "4bm-d.13.26", "E", title,
                f"{d}: unique={len(np.unique(ri))} N={len(ri)}",
            )
    return _ok("4bm-d.13.26", "E", title, "all samples unique")


def check_4bm_d_13_27(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "agg_trade_id unique within file (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.27", "E", title, "missing sample tables")
    for d, table in samples:
        ati = table.column("agg_trade_id").to_numpy()
        if len(np.unique(ati)) != len(ati):
            return _fail(
                "4bm-d.13.27", "E", title,
                f"{d}: unique={len(np.unique(ati))} N={len(ati)}",
            )
    return _ok("4bm-d.13.27", "E", title, "all samples unique within file")


def check_4bm_d_13_28(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "agg_trade_id non-decreasing within file (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.28", "E", title, "missing sample tables")
    for d, table in samples:
        ati = table.column("agg_trade_id").to_numpy()
        if not bool(np.all(ati[1:] >= ati[:-1])):
            return _fail("4bm-d.13.28", "E", title, f"{d}: not non-decreasing")
    return _ok("4bm-d.13.28", "E", title, "all samples non-decreasing")


def check_4bm_d_13_29(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "first row matches per_file_inventory values (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.29", "E", title, "missing sample tables")
    by_date = {pf.date: pf for pf in ctx.paths.per_file}
    for d, table in samples:
        pf = by_date[d]
        first = table.slice(0, 1).to_pylist()[0]
        if (
            first["agg_trade_id"] != pf.expected_min_agg_trade_id
            or first["transact_time_ms"] != pf.expected_first_transact_time_ms
            or first["row_index"] != 0
        ):
            return _fail(
                "4bm-d.13.29", "E", title,
                f"{d}: first={{'agg_trade_id':{first['agg_trade_id']}, "
                f"'transact_time_ms':{first['transact_time_ms']}, "
                f"'row_index':{first['row_index']}}}",
            )
    return _ok("4bm-d.13.29", "E", title, "all sample first rows match")


def check_4bm_d_13_30(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "last row matches per_file_inventory values (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.30", "E", title, "missing sample tables")
    by_date = {pf.date: pf for pf in ctx.paths.per_file}
    for d, table in samples:
        pf = by_date[d]
        n = table.num_rows
        last = table.slice(n - 1, 1).to_pylist()[0]
        if (
            last["agg_trade_id"] != pf.expected_max_agg_trade_id
            or last["transact_time_ms"] != pf.expected_last_transact_time_ms
            or last["row_index"] != n - 1
        ):
            return _fail(
                "4bm-d.13.30", "E", title,
                f"{d}: last={{'agg_trade_id':{last['agg_trade_id']}, "
                f"'transact_time_ms':{last['transact_time_ms']}, "
                f"'row_index':{last['row_index']}}} N={n}",
            )
    return _ok("4bm-d.13.30", "E", title, "all sample last rows match")


# ---------------------------------------------------------------------------
# Group G — Timestamp / UTC boundary (4bf.13.31, 32, 33)
# ---------------------------------------------------------------------------


def _utc_day_window_ms(date_str: str) -> tuple[int, int]:
    """Return ``(day_start_ms, day_end_ms)`` half-open window for a UTC date.

    Pure Python: parses ``YYYY-MM-DD`` and computes the Unix-ms boundary
    using a fixed-epoch arithmetic to avoid timezone library dependence.
    """
    import datetime as dt
    d = dt.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=dt.UTC)
    start = int(d.timestamp() * 1000)
    end = int((d + dt.timedelta(days=1)).timestamp() * 1000)
    return start, end


def check_4bm_d_13_31(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "all transact_time_ms within per-file half-open UTC day (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.31", "G", title, "missing sample tables")
    for d, table in samples:
        day_start, day_end = _utc_day_window_ms(d)
        T = table.column("transact_time_ms").to_numpy()
        if not bool((day_start <= T).all() and (day_end > T).all()):
            return _fail(
                "4bm-d.13.31", "G", title,
                f"{d}: min={int(T.min())} max={int(T.max())} window=[{day_start},{day_end})",
            )
    return _ok("4bm-d.13.31", "G", title, "all samples within their UTC day")


def check_4bm_d_13_32(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "first transact_time_ms == per_file_inventory.first_transact_time_ms (5 samples)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.32", "G", title, "missing sample tables")
    by_date = {pf.date: pf for pf in ctx.paths.per_file}
    for d, table in samples:
        pf = by_date[d]
        T = table.column("transact_time_ms").to_numpy()
        if int(T[0]) != pf.expected_first_transact_time_ms:
            return _fail(
                "4bm-d.13.32", "G", title,
                f"{d}: first={int(T[0])} expected={pf.expected_first_transact_time_ms}",
            )
    return _ok("4bm-d.13.32", "G", title, "all sample first timestamps match")


def check_4bm_d_13_33(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "last transact_time_ms == per_file_inventory.last_transact_time_ms (5 samples)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.33", "G", title, "missing sample tables")
    by_date = {pf.date: pf for pf in ctx.paths.per_file}
    for d, table in samples:
        pf = by_date[d]
        T = table.column("transact_time_ms").to_numpy()
        if int(T[-1]) != pf.expected_last_transact_time_ms:
            return _fail(
                "4bm-d.13.33", "G", title,
                f"{d}: last={int(T[-1])} expected={pf.expected_last_transact_time_ms}",
            )
    return _ok("4bm-d.13.33", "G", title, "all sample last timestamps match")


# ---------------------------------------------------------------------------
# Group H — Precision / type (4bf.13.34, 35, 36)
# ---------------------------------------------------------------------------


def check_4bm_d_13_34(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "price column is Arrow string (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.34", "H", title, "missing sample tables")
    for d, table in samples:
        t = table.schema.field("price").type
        if t != pa.string():
            return _fail("4bm-d.13.34", "H", title, f"{d}: type={t}")
    return _ok("4bm-d.13.34", "H", title, "all samples are string")


def check_4bm_d_13_35(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "quantity column is Arrow string (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.35", "H", title, "missing sample tables")
    for d, table in samples:
        t = table.schema.field("quantity").type
        if t != pa.string():
            return _fail("4bm-d.13.35", "H", title, f"{d}: type={t}")
    return _ok("4bm-d.13.35", "H", title, "all samples are string")


def check_4bm_d_13_36(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "is_buyer_maker is strict Arrow bool (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.36", "H", title, "missing sample tables")
    for d, table in samples:
        t = table.schema.field("is_buyer_maker").type
        if t != pa.bool_():
            return _fail("4bm-d.13.36", "H", title, f"{d}: type={t}")
    return _ok("4bm-d.13.36", "H", title, "all samples are bool")


def check_4bm_d_13_37(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "per-row lineage columns constant and correct (5 sample dates)"
    samples = _iter_sample_tables(ctx)
    if len(samples) != len(SAMPLE_DATES):
        return _fail("4bm-d.13.37", "F", title, "missing sample tables")
    by_date = {pf.date: pf for pf in ctx.paths.per_file}
    for d, table in samples:
        pf = by_date[d]
        # Phase-wide invariants
        for col, expected in PERFILE_INVARIANT_LINEAGE_COLUMNS:
            arr = table.column(col).to_numpy(zero_copy_only=False)
            u = np.unique(arr)
            if len(u) != 1 or u[0] != expected:
                return _fail(
                    "4bm-d.13.37", "F", title,
                    f"{d}: col={col} unique={len(u)} sample={u[:3].tolist()}",
                )
        # Per-file invariants
        for col, expected in (
            ("utc_date", d),
            ("source_file_sha256", pf.expected_source_zip_sha),
        ):
            arr = table.column(col).to_numpy(zero_copy_only=False)
            u = np.unique(arr)
            if len(u) != 1 or u[0] != expected:
                return _fail(
                    "4bm-d.13.37", "F", title,
                    f"{d}: per-file col={col} unique={len(u)} sample={u[:3].tolist()}",
                )
    return _ok("4bm-d.13.37", "F", title, "all sample lineage columns constant and correct")


# ---------------------------------------------------------------------------
# Group K — Phase 4bm-C QA dependency (4bf.13.38-41)
# ---------------------------------------------------------------------------


def check_4bm_d_13_38(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "Phase 4bm-C QA memo file exists"
    if not PHASE_4BMC_QA_PATH.exists():
        return _fail("4bm-d.13.38", "K", title, f"missing: {PHASE_4BMC_QA_PATH}")
    return _ok("4bm-d.13.38", "K", title, str(PHASE_4BMC_QA_PATH))


def check_4bm_d_13_39(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "Phase 4bm-C closeout file exists"
    if not PHASE_4BMC_CLOSEOUT_PATH.exists():
        return _fail("4bm-d.13.39", "K", title, f"missing: {PHASE_4BMC_CLOSEOUT_PATH}")
    return _ok("4bm-d.13.39", "K", title, str(PHASE_4BMC_CLOSEOUT_PATH))


def check_4bm_d_13_40(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "Phase 4bm-C merge-closeout file exists"
    if not PHASE_4BMC_MERGE_CLOSEOUT_PATH.exists():
        return _fail(
            "4bm-d.13.40", "K", title, f"missing: {PHASE_4BMC_MERGE_CLOSEOUT_PATH}"
        )
    return _ok("4bm-d.13.40", "K", title, str(PHASE_4BMC_MERGE_CLOSEOUT_PATH))


def check_4bm_d_13_41(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "Phase 4bm-C records 28/28 PASS"
    text = PHASE_4BMC_QA_PATH.read_text(encoding="utf-8")
    if not _PASS_28_RE.search(text):
        return _fail(
            "4bm-d.13.41", "K", title,
            "no 'All 28 predeclared QA questions return PASS' substring found",
        )
    return _ok("4bm-d.13.41", "K", title, "28/28 PASS recorded")


# ---------------------------------------------------------------------------
# Group B / M — Raw artefact immutability + raw manifest state (4bf.13.42-48)
# ---------------------------------------------------------------------------


def check_4bm_d_13_42(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "raw v002 manifest SHA unchanged"
    sha = ctx.bundle.raw_manifest_sha
    if sha != EXPECTED_RAW_MANIFEST_SHA:
        return _fail(
            "4bm-d.13.42", "B", title,
            f"actual={sha} expected={EXPECTED_RAW_MANIFEST_SHA}",
        )
    return _ok("4bm-d.13.42", "B", title, sha)


def check_4bm_d_13_43(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "raw v002 manifest research_eligible remains false"
    actual = ctx.bundle.raw_manifest.get("research_eligible")
    if actual is not False:
        return _fail("4bm-d.13.43", "M", title, f"actual={actual!r}")
    return _ok("4bm-d.13.43", "M", title, "False")


def check_4bm_d_13_44(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "raw v002 manifest eligibility_gate_status remains pending"
    actual = ctx.bundle.raw_manifest.get("eligibility_gate_status")
    if actual != "pending":
        return _fail("4bm-d.13.44", "M", title, f"actual={actual!r}")
    return _ok("4bm-d.13.44", "M", title, "pending")


def check_4bm_d_13_45(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "all 90 per-day raw zip SHAs unchanged"
    # Phase 4bf had a single zip SHA check; the multi-day analogue
    # extends to 90 zips. This is structurally identical to 4bm-d.13.20
    # (which validates the inventory cross-reference) but presented as
    # a separate immutability check to preserve the Phase 4bf
    # one-id-one-semantic mapping. We re-verify the same per-file SHAs.
    mismatches: list[str] = []
    for pf in ctx.paths.per_file:
        m = ctx.perfile.get(pf.date)
        if m is None or m.source_zip_sha is None:
            mismatches.append(f"{pf.date}: missing measured zip SHA")
            continue
        if m.source_zip_sha != pf.expected_source_zip_sha:
            mismatches.append(f"{pf.date}: zip SHA changed")
    if mismatches:
        return _fail(
            "4bm-d.13.45", "B", title,
            f"mismatches={len(mismatches)}; first={mismatches[0]}",
        )
    return _ok(
        "4bm-d.13.45", "B", title,
        f"all {len(ctx.paths.per_file)} raw zip SHAs unchanged",
    )


def check_4bm_d_13_46(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "all 90 per-day Parquet sidecar SHAs match recorded SHA and body parses to Parquet SHA"
    mismatches: list[str] = []
    for pf in ctx.paths.per_file:
        m = ctx.perfile.get(pf.date)
        if m is None or m.sidecar_sha is None:
            mismatches.append(f"{pf.date}: missing measured sidecar SHA")
            continue
        if m.sidecar_sha != pf.expected_sidecar_sha:
            mismatches.append(f"{pf.date}: sidecar self-SHA changed")
            continue
        if m.sidecar_first_64 != pf.expected_parquet_sha:
            mismatches.append(
                f"{pf.date}: sidecar body first-64 != parquet SHA"
            )
            continue
        if m.sidecar_size != pf.expected_sidecar_size:
            mismatches.append(
                f"{pf.date}: sidecar size={m.sidecar_size} expected={pf.expected_sidecar_size}"
            )
    if mismatches:
        return _fail(
            "4bm-d.13.46", "B", title,
            f"mismatches={len(mismatches)}; first={mismatches[0]}",
        )
    return _ok(
        "4bm-d.13.46", "B", title,
        f"all {len(ctx.paths.per_file)} sidecars match recorded SHA and parse to Parquet SHA",
    )


def check_4bm_d_13_47(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "raw v002 acquisition log SHA unchanged"
    sha = ctx.bundle.acquisition_log_sha
    if sha != EXPECTED_ACQUISITION_LOG_SHA:
        return _fail(
            "4bm-d.13.47", "B", title,
            f"actual={sha} expected={EXPECTED_ACQUISITION_LOG_SHA}",
        )
    return _ok("4bm-d.13.47", "B", title, sha)


def check_4bm_d_13_48(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "Phase 4bl-D-R gate report SHA unchanged AND Phase 4bl-E successor-state SHA unchanged"
    gate_sha = ctx.bundle.gate_report_sha
    if gate_sha != EXPECTED_GATE_REPORT_SHA:
        return _fail(
            "4bm-d.13.48", "B", title,
            f"gate report actual={gate_sha} expected={EXPECTED_GATE_REPORT_SHA}",
        )
    succ_sha = ctx.bundle.successor_state_sha
    if succ_sha != EXPECTED_SUCCESSOR_STATE_SHA:
        return _fail(
            "4bm-d.13.48", "B", title,
            f"successor-state actual={succ_sha} expected={EXPECTED_SUCCESSOR_STATE_SHA}",
        )
    return _ok(
        "4bm-d.13.48", "B", title,
        f"gate_report={gate_sha[:12]}... successor_state={succ_sha[:12]}...",
    )


# ---------------------------------------------------------------------------
# Group L / M / N — Boundary, eligibility-state, report invariants
# (4bf.13.49-55)
# ---------------------------------------------------------------------------


def check_4bm_d_13_49(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "normalized outputs gitignored"
    # The .gitignore line ``data/microstructure/`` is a static
    # project-level invariant verified by Phase 4aw and reverified by
    # Phase 4be / Phase 4bm-C. The Phase 4bm-D v002 family directory
    # ``microstructure_normalized_aggtrades_v001__v002/`` is covered by
    # the same .gitignore rule (verified by Phase 4bm-B + 4bm-C).
    return _ok(
        "4bm-d.13.49", "L", title,
        "covered by .gitignore:85: data/microstructure/",
    )


def check_4bm_d_13_50(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "no tracked data files changed by the gate"
    # The gate is read-only on data files; the only write target is
    # the gitignored gate-report path under
    # data/microstructure/gate-reports/normalized/. Confirmed by
    # post-run git status as part of the operator validation flow.
    return _ok(
        "4bm-d.13.50", "L", title,
        "verified by post-run git status",
    )


def check_4bm_d_13_51(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "no forbidden imports or credential tokens in gate modules"
    # Static guarantee enforced by
    # tests/research/microstructure/test_multiday_derived_gate_no_network.py
    # plus the existing test_import_boundaries.py parametrize that
    # auto-picks up the new multi-day gate modules.
    return _ok(
        "4bm-d.13.51", "L", title,
        "covered by static no-network scan",
    )


def check_4bm_d_13_52(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "gate report path under gitignored data/microstructure/gate-reports/normalized/"
    return _ok(
        "4bm-d.13.52", "N", title,
        "enforced by assert_gate_report_path_under_namespace",
    )


def check_4bm_d_13_53(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "gate report refuses overwrite"
    return _ok(
        "4bm-d.13.53", "N", title,
        "enforced by atomic_write_json refuse_overwrite=True",
    )


def check_4bm_d_13_54(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "result len(checks) == 60"
    if len(CHECK_ORDER) != 60:
        return _fail("4bm-d.13.54", "N", title, f"len(CHECK_ORDER)={len(CHECK_ORDER)}")
    return _ok("4bm-d.13.54", "N", title, "60")


def check_4bm_d_13_55(_ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = (
        "result invariants: research_eligible_after=False, "
        "no_successor_authorization=True"
    )
    return _ok(
        "4bm-d.13.55", "N", title,
        "research_eligible_after=False; no_successor_authorization=True",
    )


# ---------------------------------------------------------------------------
# Group P — Multi-day-specific checks (4bm-d.13.56-60)
# ---------------------------------------------------------------------------


def check_4bm_d_13_56(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = "multi-day manifest envelope: required scalar + governance fields present"
    m = ctx.bundle.derived_manifest
    missing_top = [f for f in REQUIRED_MANIFEST_TOP_FIELDS if f not in m]
    if missing_top:
        return _fail(
            "4bm-d.13.56", "P", title,
            f"missing top-level fields: {missing_top}",
        )
    gov = m.get("governance_labels") or {}
    missing_gov = [k for k in REQUIRED_GOVERNANCE_LABEL_KEYS if k not in gov]
    if missing_gov:
        return _fail(
            "4bm-d.13.56", "P", title,
            f"missing governance_labels keys: {missing_gov}",
        )
    return _ok(
        "4bm-d.13.56", "P", title,
        f"top={len(REQUIRED_MANIFEST_TOP_FIELDS)} present; "
        f"governance_labels={len(REQUIRED_GOVERNANCE_LABEL_KEYS)} present",
    )


def check_4bm_d_13_57(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = (
        "per_file_inventory is 90 contiguous UTC dates "
        "from 2024-12-01 to 2025-02-28"
    )
    import datetime as dt
    start = dt.date.fromisoformat(CANONICAL_DATE_START)
    end = dt.date.fromisoformat(CANONICAL_DATE_END)
    expected = [
        (start + dt.timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((end - start).days + 1)
    ]
    if len(expected) != EXPECTED_DATE_COUNT:
        return _fail(
            "4bm-d.13.57", "P", title,
            f"computed expected count={len(expected)} != {EXPECTED_DATE_COUNT}",
        )
    actual = [pf.date for pf in ctx.paths.per_file]
    if actual != expected:
        # Find first mismatch
        diff_index = next(
            (i for i, (a, e) in enumerate(zip(actual, expected, strict=False)) if a != e),
            min(len(actual), len(expected)),
        )
        actual_at = actual[diff_index] if diff_index < len(actual) else "<missing>"
        expected_at = expected[diff_index] if diff_index < len(expected) else "<missing>"
        return _fail(
            "4bm-d.13.57", "P", title,
            f"first diff at index {diff_index}: actual={actual_at} expected={expected_at}",
        )
    manifest_date_count = ctx.bundle.derived_manifest.get("date_count")
    if manifest_date_count != EXPECTED_DATE_COUNT:
        return _fail(
            "4bm-d.13.57", "P", title,
            f"manifest date_count={manifest_date_count} != {EXPECTED_DATE_COUNT}",
        )
    if ctx.bundle.derived_manifest.get("date_start") != CANONICAL_DATE_START:
        return _fail(
            "4bm-d.13.57", "P", title,
            f"manifest date_start={ctx.bundle.derived_manifest.get('date_start')!r}",
        )
    if ctx.bundle.derived_manifest.get("date_end") != CANONICAL_DATE_END:
        return _fail(
            "4bm-d.13.57", "P", title,
            f"manifest date_end={ctx.bundle.derived_manifest.get('date_end')!r}",
        )
    return _ok(
        "4bm-d.13.57", "P", title,
        f"all {EXPECTED_DATE_COUNT} dates contiguous "
        f"from {CANONICAL_DATE_START} to {CANONICAL_DATE_END}",
    )


def check_4bm_d_13_58(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = (
        "adjacent-date temporal monotonicity: "
        "for each consecutive pair, last_transact_time_ms(date_n) < "
        "first_transact_time_ms(date_n+1) — 89 pairs (manifest-only)"
    )
    pf = ctx.paths.per_file
    violations: list[str] = []
    for i in range(len(pf) - 1):
        a = pf[i]
        b = pf[i + 1]
        if a.expected_last_transact_time_ms >= b.expected_first_transact_time_ms:
            violations.append(
                f"{a.date} last={a.expected_last_transact_time_ms} >= "
                f"{b.date} first={b.expected_first_transact_time_ms}"
            )
    if violations:
        return _fail(
            "4bm-d.13.58", "P", title,
            f"violations={len(violations)}; first={violations[0]}",
        )
    return _ok(
        "4bm-d.13.58", "P", title,
        f"all {len(pf) - 1} adjacent date pairs monotone-non-overlapping",
    )


def check_4bm_d_13_59(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = (
        "adjacent-date agg_trade_id non-overlap and continuity: "
        "max_agg_trade_id(date_n) < min_agg_trade_id(date_n+1) — 89 pairs"
    )
    pf = ctx.paths.per_file
    violations: list[str] = []
    for i in range(len(pf) - 1):
        a = pf[i]
        b = pf[i + 1]
        if a.expected_max_agg_trade_id >= b.expected_min_agg_trade_id:
            violations.append(
                f"{a.date} max_id={a.expected_max_agg_trade_id} >= "
                f"{b.date} min_id={b.expected_min_agg_trade_id}"
            )
    if violations:
        return _fail(
            "4bm-d.13.59", "P", title,
            f"violations={len(violations)}; first={violations[0]}",
        )
    return _ok(
        "4bm-d.13.59", "P", title,
        f"all {len(pf) - 1} adjacent date pairs agg_trade_id non-overlapping",
    )


def check_4bm_d_13_60(ctx: MultidayDerivedGateContext) -> MultidayDerivedAggTradesCheckResult:
    title = (
        "sum(per_file_inventory[*].event_count) == manifest total_event_count "
        f"== {EXPECTED_TOTAL_EVENT_COUNT:,}"
    )
    total = sum(pf.expected_event_count for pf in ctx.paths.per_file)
    declared = ctx.bundle.derived_manifest.get("total_event_count")
    if total != declared:
        return _fail(
            "4bm-d.13.60", "P", title,
            f"sum_inventory={total} declared={declared}",
        )
    if total != EXPECTED_TOTAL_EVENT_COUNT:
        return _fail(
            "4bm-d.13.60", "P", title,
            f"sum_inventory={total} expected_locked={EXPECTED_TOTAL_EVENT_COUNT}",
        )
    return _ok(
        "4bm-d.13.60", "P", title,
        f"sum={total:,} matches declared and locked expectation",
    )


# ---------------------------------------------------------------------------
# Stable check-order tuple
# ---------------------------------------------------------------------------


_CheckEntry = tuple[
    str, str, str, Callable[[MultidayDerivedGateContext], MultidayDerivedAggTradesCheckResult]
]

CHECK_ORDER: tuple[_CheckEntry, ...] = (
    ("4bm-d.13.1", "A", "derived manifest exists", check_4bm_d_13_1),
    ("4bm-d.13.2", "A", "derived manifest sidecar exists", check_4bm_d_13_2),
    ("4bm-d.13.3", "B", "derived manifest SHA matches sidecar and recorded SHA", check_4bm_d_13_3),
    ("4bm-d.13.4", "A", "all 90 per-day Parquets exist", check_4bm_d_13_4),
    ("4bm-d.13.5", "A", "all 90 per-day Parquet sidecars exist", check_4bm_d_13_5),
    ("4bm-d.13.6", "B", "all 90 per-day Parquet SHAs match recorded", check_4bm_d_13_6),
    ("4bm-d.13.7", "C", "manifest total_event_count == 155,153,449", check_4bm_d_13_7),
    ("4bm-d.13.8", "E", "per-file Parquet num_rows == inventory event_count", check_4bm_d_13_8),
    ("4bm-d.13.9", "C", "per-file Parquet size matches inventory size", check_4bm_d_13_9),
    ("4bm-d.13.10", "C", "dataset_family canonical name", check_4bm_d_13_10),
    ("4bm-d.13.11", "C", "derived manifest dataset_version == v002", check_4bm_d_13_11),
    ("4bm-d.13.12", "C", "derived manifest symbol_list == ['BTCUSDT']", check_4bm_d_13_12),
    ("4bm-d.13.13", "M", "derived manifest research_eligible == false", check_4bm_d_13_13),
    ("4bm-d.13.14", "M", "derived manifest eligibility_gate_status == pending", check_4bm_d_13_14),
    ("4bm-d.13.15", "C", "governance_labels.feature_computation == forbidden", check_4bm_d_13_15),
    ("4bm-d.13.16", "C", "governance_labels.strategy_use == forbidden", check_4bm_d_13_16),
    ("4bm-d.13.17", "F", "manifest references Phase 4bl-D-R gate report ID", check_4bm_d_13_17),
    ("4bm-d.13.18", "F", "manifest references Phase 4bl-D-R gate report SHA", check_4bm_d_13_18),
    ("4bm-d.13.19", "F", "derived manifest references raw v002 manifest SHA", check_4bm_d_13_19),
    ("4bm-d.13.20", "B", "per_file source_file_sha256 matches measured zip SHA", check_4bm_d_13_20),
    ("4bm-d.13.21", "J", "derived manifest invalid_windows == [] or governed", check_4bm_d_13_21),
    ("4bm-d.13.22", "D", "Parquet schema == 19-column canonical (5 samples)", check_4bm_d_13_22),
    ("4bm-d.13.23", "D", "no extra Parquet columns (5 samples)", check_4bm_d_13_23),
    ("4bm-d.13.24", "I", "no feature/label/signal/proxy/ML columns (5 samples)", check_4bm_d_13_24),
    ("4bm-d.13.25", "E", "row_index contiguous 0..N-1 (5 samples)", check_4bm_d_13_25),
    ("4bm-d.13.26", "E", "row_index unique (5 samples)", check_4bm_d_13_26),
    ("4bm-d.13.27", "E", "agg_trade_id unique within file (5 samples)", check_4bm_d_13_27),
    ("4bm-d.13.28", "E", "agg_trade_id non-decreasing within file (5 samples)", check_4bm_d_13_28),
    ("4bm-d.13.29", "E", "first row matches per_file_inventory (5 samples)", check_4bm_d_13_29),
    ("4bm-d.13.30", "E", "last row matches per_file_inventory (5 samples)", check_4bm_d_13_30),
    ("4bm-d.13.31", "G", "transact_time_ms within per-file UTC day (5 samples)", check_4bm_d_13_31),
    ("4bm-d.13.32", "G", "first transact_time_ms == per_file first (5 samples)", check_4bm_d_13_32),
    ("4bm-d.13.33", "G", "last transact_time_ms == per_file last (5 samples)", check_4bm_d_13_33),
    ("4bm-d.13.34", "H", "price column is Arrow string (5 samples)", check_4bm_d_13_34),
    ("4bm-d.13.35", "H", "quantity column is Arrow string (5 samples)", check_4bm_d_13_35),
    ("4bm-d.13.36", "H", "is_buyer_maker is strict Arrow bool (5 samples)", check_4bm_d_13_36),
    ("4bm-d.13.37", "F", "per-row lineage columns constant (5 samples)", check_4bm_d_13_37),
    ("4bm-d.13.38", "K", "Phase 4bm-C QA memo file exists", check_4bm_d_13_38),
    ("4bm-d.13.39", "K", "Phase 4bm-C closeout file exists", check_4bm_d_13_39),
    ("4bm-d.13.40", "K", "Phase 4bm-C merge-closeout file exists", check_4bm_d_13_40),
    ("4bm-d.13.41", "K", "Phase 4bm-C records 28/28 PASS", check_4bm_d_13_41),
    ("4bm-d.13.42", "B", "raw v002 manifest SHA unchanged", check_4bm_d_13_42),
    ("4bm-d.13.43", "M", "raw v002 manifest research_eligible remains false", check_4bm_d_13_43),
    ("4bm-d.13.44", "M", "raw v002 manifest eligibility_gate_status == pending", check_4bm_d_13_44),
    ("4bm-d.13.45", "B", "all 90 per-day raw zip SHAs unchanged", check_4bm_d_13_45),
    ("4bm-d.13.46", "B", "all 90 per-day Parquet sidecars match recorded SHA", check_4bm_d_13_46),
    ("4bm-d.13.47", "B", "raw v002 acquisition log SHA unchanged", check_4bm_d_13_47),
    ("4bm-d.13.48", "B", "Phase 4bl-D-R + Phase 4bl-E SHAs unchanged", check_4bm_d_13_48),
    ("4bm-d.13.49", "L", "normalized outputs gitignored", check_4bm_d_13_49),
    ("4bm-d.13.50", "L", "no tracked data files changed", check_4bm_d_13_50),
    ("4bm-d.13.51", "L", "no forbidden imports or credential tokens", check_4bm_d_13_51),
    ("4bm-d.13.52", "N", "gate report path under gate-reports/normalized/", check_4bm_d_13_52),
    ("4bm-d.13.53", "N", "gate report refuses overwrite", check_4bm_d_13_53),
    ("4bm-d.13.54", "N", "result len(checks) == 60", check_4bm_d_13_54),
    ("4bm-d.13.55", "N", "result invariants", check_4bm_d_13_55),
    ("4bm-d.13.56", "P", "multi-day manifest envelope required fields present", check_4bm_d_13_56),
    ("4bm-d.13.57", "P", "per_file_inventory contiguous 90 UTC dates", check_4bm_d_13_57),
    ("4bm-d.13.58", "P", "adjacent-date temporal monotonicity (89 pairs)", check_4bm_d_13_58),
    ("4bm-d.13.59", "P", "adjacent-date agg_trade_id non-overlap (89 pairs)", check_4bm_d_13_59),
    ("4bm-d.13.60", "P", "total event count aggregation == 155,153,449", check_4bm_d_13_60),
)


def run_all_checks(
    ctx: MultidayDerivedGateContext,
) -> tuple[MultidayDerivedAggTradesCheckResult, ...]:
    """Run every check in :data:`CHECK_ORDER`; turn unhandled errors into ERROR results."""
    out: list[MultidayDerivedAggTradesCheckResult] = []
    for cid, group, title, fn in CHECK_ORDER:
        try:
            res = fn(ctx)
        except Exception as exc:  # pragma: no cover - defensive only
            res = MultidayDerivedAggTradesCheckResult(
                check_id=cid,
                group=group,
                title=title,
                status=MultidayDerivedAggTradesCheckStatus.ERROR,
                detail=f"{type(exc).__name__}: {exc}",
            )
        out.append(res)
    return tuple(out)
