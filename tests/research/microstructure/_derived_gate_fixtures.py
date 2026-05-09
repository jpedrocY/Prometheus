"""Shared mini-fixture helpers for the Phase 4bf derived-family gate tests.

These helpers construct minimal canonical :class:`DerivedGateContext`
instances that allow per-check PASS / FAIL tests without rebuilding
the real 1.68M-row Phase 4bd Parquet. The fixtures live entirely in
caller-provided ``tmp_path`` directories and never touch the real
``data/microstructure/`` tree.

For checks that depend on row count or parquet content, tests use
``monkeypatch`` to override the relevant ``EXPECTED_*`` constant in
:mod:`derived_gate_checks` and build a tiny pyarrow table with the
canonical 19-column schema plus values that match the reduced
constants.
"""
from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from typing import Any

import pyarrow as pa

# Import the module so we can read EXPECTED_* constants dynamically at call
# time (so monkeypatch.setattr(dgc.EXPECTED_*, ...) propagates into helpers).
from prometheus.research.microstructure import derived_gate_checks as dgc
from prometheus.research.microstructure.derived_gate_checks import (
    CANONICAL_DATASET_FAMILY,
    CANONICAL_DATASET_VERSION,
    CANONICAL_NORMALIZATION_SCHEMA_VERSION,
    CANONICAL_SOURCE_DATASET_FAMILY,
    CANONICAL_SOURCE_DATASET_VERSION,
    CANONICAL_SYMBOL,
    CANONICAL_UTC_DATE,
    EXPECTED_FIRST_PRICE,
    EXPECTED_FIRST_QUANTITY,
    EXPECTED_LAST_PRICE,
    EXPECTED_LAST_QUANTITY,
    DerivedGateContext,
)


def make_canonical_table(num_rows: int = 5) -> pa.Table:
    """Build a tiny canonical 19-column pyarrow Table.

    The resulting table satisfies all schema, type, lineage, row-index,
    agg-trade-id, timestamp-boundary, and first/last-row checks
    *provided* the caller monkeypatches the row-count-sensitive
    EXPECTED_* constants (event count, last_T, last_agg_trade_id) to
    match this minimal table.
    """
    if num_rows < 2:
        raise ValueError("need at least 2 rows to satisfy first/last-row checks")
    # row_index 0 .. num_rows-1
    row_indices = list(range(num_rows))
    # agg_trade_id strictly increasing starting at the canonical first
    agg_ids = [dgc.EXPECTED_FIRST_AGG_TRADE_ID + i for i in row_indices]
    # transact_time_ms strictly increasing inside the canonical UTC day
    t_values = [dgc.EXPECTED_FIRST_T + i for i in row_indices]
    # Override last position to canonical last values
    agg_ids[-1] = dgc.EXPECTED_LAST_AGG_TRADE_ID
    t_values[-1] = dgc.EXPECTED_LAST_T

    prices = [EXPECTED_FIRST_PRICE] + ["98000.0"] * (num_rows - 2) + [EXPECTED_LAST_PRICE]
    quantities = [EXPECTED_FIRST_QUANTITY] + ["0.123"] * (num_rows - 2) + [EXPECTED_LAST_QUANTITY]
    is_buyer_maker = [True] * num_rows
    first_trade_ids = [5_840_262_657 + i * 10 for i in row_indices]
    last_trade_ids = [5_840_262_665 + i * 10 for i in row_indices]

    n = num_rows
    columns: dict[str, list[Any]] = {
        "dataset_family": [CANONICAL_DATASET_FAMILY] * n,
        "dataset_version": [CANONICAL_DATASET_VERSION] * n,
        "source_dataset_family": [CANONICAL_SOURCE_DATASET_FAMILY] * n,
        "source_dataset_version": [CANONICAL_SOURCE_DATASET_VERSION] * n,
        "symbol": [CANONICAL_SYMBOL] * n,
        "utc_date": [CANONICAL_UTC_DATE] * n,
        "agg_trade_id": agg_ids,
        "price": prices,
        "quantity": quantities,
        "first_trade_id": first_trade_ids,
        "last_trade_id": last_trade_ids,
        "transact_time_ms": t_values,
        "is_buyer_maker": is_buyer_maker,
        "source_file_sha256": [dgc.EXPECTED_RAW_ZIP_SHA] * n,
        "source_manifest_sha256": [dgc.EXPECTED_RAW_MANIFEST_SHA] * n,
        "source_gate_report_id": [dgc.EXPECTED_GATE_REPORT_ID] * n,
        "source_gate_report_sha256": [dgc.EXPECTED_GATE_REPORT_SHA] * n,
        "row_index": row_indices,
        "normalization_schema_version": [CANONICAL_NORMALIZATION_SCHEMA_VERSION] * n,
    }
    schema = pa.schema(
        [
            pa.field("dataset_family", pa.string()),
            pa.field("dataset_version", pa.string()),
            pa.field("source_dataset_family", pa.string()),
            pa.field("source_dataset_version", pa.string()),
            pa.field("symbol", pa.string()),
            pa.field("utc_date", pa.string()),
            pa.field("agg_trade_id", pa.int64()),
            pa.field("price", pa.string()),
            pa.field("quantity", pa.string()),
            pa.field("first_trade_id", pa.int64()),
            pa.field("last_trade_id", pa.int64()),
            pa.field("transact_time_ms", pa.int64()),
            pa.field("is_buyer_maker", pa.bool_()),
            pa.field("source_file_sha256", pa.string()),
            pa.field("source_manifest_sha256", pa.string()),
            pa.field("source_gate_report_id", pa.string()),
            pa.field("source_gate_report_sha256", pa.string()),
            pa.field("row_index", pa.int64()),
            pa.field("normalization_schema_version", pa.string()),
        ]
    )
    # pyarrow requires column order to match schema; build via from_pydict + cast
    return pa.Table.from_pydict(columns, schema=schema)


def make_canonical_derived_manifest(*, event_count: int = 5) -> dict[str, Any]:
    return {
        "dataset_family": CANONICAL_DATASET_FAMILY,
        "version": CANONICAL_DATASET_VERSION,
        "symbol": CANONICAL_SYMBOL,
        "utc_date": CANONICAL_UTC_DATE,
        "start_time_ms": dgc.EXPECTED_FIRST_T,
        "end_time_ms": dgc.EXPECTED_LAST_T,
        "event_count": event_count,
        "file_count": 1,
        "files": [
            {
                "path": "normalized/foo.parquet",
                "sha256": dgc.EXPECTED_NORMALIZED_PARQUET_SHA,
                "start_time_ms": dgc.EXPECTED_FIRST_T,
                "end_time_ms": dgc.EXPECTED_LAST_T,
                "event_count": event_count,
            }
        ],
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "invalid_windows": [],
        "governance_labels": {
            "phase": "4bd",
            "source_phase_boundary": "4bb-D",
            "source_dataset_family": CANONICAL_SOURCE_DATASET_FAMILY,
            "source_dataset_version": CANONICAL_SOURCE_DATASET_VERSION,
            "source_manifest_path": "manifests/x.json",
            "source_manifest_sha256": dgc.EXPECTED_RAW_MANIFEST_SHA,
            "source_raw_zip_path": "raw/x.zip",
            "source_raw_zip_sha256": dgc.EXPECTED_RAW_ZIP_SHA,
            "source_gate_report_id": dgc.EXPECTED_GATE_REPORT_ID,
            "source_gate_report_sha256": dgc.EXPECTED_GATE_REPORT_SHA,
            "source_gate_report_code_commit_sha": "aa612ba2778c97a5150b80064244b90d024bfa54",
            "validator": "phase_4ax_aggtrades_v001",
            "stop_trigger_domain": "trade_price_backtest_candidate",
            "feature_computation": "forbidden",
            "strategy_use": "forbidden",
        },
    }


def make_canonical_raw_manifest() -> dict[str, Any]:
    return {
        "dataset_family": CANONICAL_SOURCE_DATASET_FAMILY,
        "version": CANONICAL_SOURCE_DATASET_VERSION,
        "symbol": CANONICAL_SYMBOL,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "start_time_ms": dgc.EXPECTED_FIRST_T,
        "end_time_ms": dgc.EXPECTED_LAST_T,
        "event_count": 1_681_098,
        "file_count": 1,
        "files": [
            {
                "path": "raw/microstructure_raw_aggtrades_v001/x.zip",
                "sha256": dgc.EXPECTED_RAW_ZIP_SHA,
            }
        ],
    }


def make_canonical_context(
    *,
    derived_manifest_path: Path,
    derived_manifest_sidecar_path: Path,
    normalized_parquet_path: Path,
    normalized_parquet_sidecar_path: Path,
    raw_manifest_path: Path,
    raw_zip_path: Path,
    raw_sidecar_path: Path,
    acquisition_log_path: Path,
    gate_report_path: Path,
    parquet_num_rows: int = 5,
    derived_manifest: dict[str, Any] | None = None,
    raw_manifest: dict[str, Any] | None = None,
) -> DerivedGateContext:
    """Build a fully canonical PASS-shaped DerivedGateContext."""
    if derived_manifest is None:
        derived_manifest = make_canonical_derived_manifest(event_count=parquet_num_rows)
    if raw_manifest is None:
        raw_manifest = make_canonical_raw_manifest()
    derived_bytes = json.dumps(derived_manifest, sort_keys=True).encode("utf-8")
    table = make_canonical_table(num_rows=parquet_num_rows)
    return DerivedGateContext(
        derived_manifest_path=derived_manifest_path,
        derived_manifest_sidecar_path=derived_manifest_sidecar_path,
        normalized_parquet_path=normalized_parquet_path,
        normalized_parquet_sidecar_path=normalized_parquet_sidecar_path,
        raw_manifest_path=raw_manifest_path,
        raw_zip_path=raw_zip_path,
        raw_sidecar_path=raw_sidecar_path,
        acquisition_log_path=acquisition_log_path,
        gate_report_path=gate_report_path,
        derived_manifest=derived_manifest,
        derived_manifest_bytes=derived_bytes,
        derived_manifest_sha=dgc.EXPECTED_DERIVED_MANIFEST_SHA,
        derived_sidecar_first_64=dgc.EXPECTED_DERIVED_MANIFEST_SHA,
        normalized_parquet_sha=dgc.EXPECTED_NORMALIZED_PARQUET_SHA,
        normalized_sidecar_first_64=dgc.EXPECTED_NORMALIZED_PARQUET_SHA,
        raw_manifest=raw_manifest,
        raw_manifest_sha=dgc.EXPECTED_RAW_MANIFEST_SHA,
        raw_zip_sha=dgc.EXPECTED_RAW_ZIP_SHA,
        raw_sidecar_sha=dgc.EXPECTED_RAW_SIDECAR_SHA,
        raw_sidecar_first_64=dgc.EXPECTED_RAW_ZIP_SHA,  # sidecar contains zip SHA
        acquisition_log_sha=dgc.EXPECTED_ACQUISITION_LOG_SHA,
        gate_report_sha=dgc.EXPECTED_GATE_REPORT_SHA,
        parquet_table=table,
    )


def build_real_paths(microstructure_root: Path) -> dict[str, Path]:
    """Compute path-discipline-correct paths under a tmp_path microstructure root."""
    return {
        "derived_manifest_path": microstructure_root
        / "manifests"
        / "microstructure_normalized_aggtrades_v001__v001.json",
        "derived_manifest_sidecar_path": microstructure_root
        / "manifests"
        / "microstructure_normalized_aggtrades_v001__v001.json.sha256",
        "normalized_parquet_path": microstructure_root
        / "normalized"
        / "microstructure_normalized_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-aggTrades-2025-01-15.parquet",
        "normalized_parquet_sidecar_path": microstructure_root
        / "normalized"
        / "microstructure_normalized_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-aggTrades-2025-01-15.parquet.sha256",
        "raw_manifest_path": microstructure_root
        / "manifests"
        / "microstructure_raw_aggtrades_v001__v001.json",
        "raw_zip_path": microstructure_root
        / "raw"
        / "microstructure_raw_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-aggTrades-2025-01-15.zip",
        "raw_sidecar_path": microstructure_root
        / "raw"
        / "microstructure_raw_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-aggTrades-2025-01-15.zip.sha256",
        "acquisition_log_path": microstructure_root
        / "manifests"
        / "microstructure_raw_aggtrades_v001__v001_acquisition_log.json",
        "gate_report_path": microstructure_root
        / "gate-reports"
        / "gate-reports"
        / f"{dgc.EXPECTED_GATE_REPORT_ID}.json",
        "output_root": microstructure_root / "gate-reports" / "normalized",
    }


def replace_ctx_field(ctx: DerivedGateContext, **overrides: Any) -> DerivedGateContext:
    """Return a copy of *ctx* with the given attribute overrides."""
    # DerivedGateContext is a non-frozen dataclass; deepcopy then setattr.
    new_ctx = deepcopy(ctx)
    for key, value in overrides.items():
        setattr(new_ctx, key, value)
    return new_ctx


def replace_manifest_field(
    ctx: DerivedGateContext, *, key: str, value: Any
) -> DerivedGateContext:
    """Return a copy of *ctx* with one derived-manifest field overridden."""
    new_manifest = deepcopy(ctx.derived_manifest)
    if "." in key:
        outer, inner = key.split(".", 1)
        new_manifest.setdefault(outer, {})
        new_manifest[outer][inner] = value
    else:
        new_manifest[key] = value
    new_ctx = deepcopy(ctx)
    new_ctx.derived_manifest = new_manifest
    return new_ctx


def replace_raw_manifest_field(
    ctx: DerivedGateContext, *, key: str, value: Any
) -> DerivedGateContext:
    new_raw = deepcopy(ctx.raw_manifest)
    new_raw[key] = value
    new_ctx = deepcopy(ctx)
    new_ctx.raw_manifest = new_raw
    return new_ctx


def patch_event_count_constant(monkeypatch: Any, value: int) -> None:
    """Override ``EXPECTED_EVENT_COUNT`` for a single test."""
    monkeypatch.setattr(
        "prometheus.research.microstructure.derived_gate_checks.EXPECTED_EVENT_COUNT",
        value,
        raising=True,
    )


def patch_last_t_constant(monkeypatch: Any, value: int) -> None:
    monkeypatch.setattr(
        "prometheus.research.microstructure.derived_gate_checks.EXPECTED_LAST_T",
        value,
        raising=True,
    )


def patch_last_agg_id_constant(monkeypatch: Any, value: int) -> None:
    monkeypatch.setattr(
        "prometheus.research.microstructure.derived_gate_checks.EXPECTED_LAST_AGG_TRADE_ID",
        value,
        raising=True,
    )


def make_minimal_context(
    *,
    tmp_path: Path,
    parquet_num_rows: int = 5,
    derived_manifest: dict[str, Any] | None = None,
    raw_manifest: dict[str, Any] | None = None,
    create_files: bool = True,
) -> DerivedGateContext:
    """Build a tmp_path-rooted DerivedGateContext for orchestrator-level tests."""
    microstructure_root = tmp_path / "data" / "microstructure"
    paths = build_real_paths(microstructure_root)
    if create_files:
        for p in [
            paths["derived_manifest_path"],
            paths["derived_manifest_sidecar_path"],
            paths["normalized_parquet_path"],
            paths["normalized_parquet_sidecar_path"],
            paths["raw_manifest_path"],
            paths["raw_zip_path"],
            paths["raw_sidecar_path"],
            paths["acquisition_log_path"],
            paths["gate_report_path"],
        ]:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"")
    return make_canonical_context(
        derived_manifest_path=paths["derived_manifest_path"],
        derived_manifest_sidecar_path=paths["derived_manifest_sidecar_path"],
        normalized_parquet_path=paths["normalized_parquet_path"],
        normalized_parquet_sidecar_path=paths["normalized_parquet_sidecar_path"],
        raw_manifest_path=paths["raw_manifest_path"],
        raw_zip_path=paths["raw_zip_path"],
        raw_sidecar_path=paths["raw_sidecar_path"],
        acquisition_log_path=paths["acquisition_log_path"],
        gate_report_path=paths["gate_report_path"],
        parquet_num_rows=parquet_num_rows,
        derived_manifest=derived_manifest,
        raw_manifest=raw_manifest,
    )


__all__ = [
    "build_real_paths",
    "make_canonical_context",
    "make_canonical_derived_manifest",
    "make_canonical_raw_manifest",
    "make_canonical_table",
    "make_minimal_context",
    "patch_event_count_constant",
    "patch_last_agg_id_constant",
    "patch_last_t_constant",
    "replace_ctx_field",
    "replace_manifest_field",
    "replace_raw_manifest_field",
]


# Re-export Decimal for tests that build per-row variants if they want to.
_unused = Decimal, replace
