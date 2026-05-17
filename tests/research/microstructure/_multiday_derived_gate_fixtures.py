"""Shared mini-fixture helpers for the Phase 4bm-D multi-day derived-family gate tests.

These helpers construct minimal canonical :class:`MultidayDerivedGateContext`
instances that allow per-check PASS / FAIL tests without rebuilding the
real 155 M-row Phase 4bm-B v002 multi-day derived family. The fixtures
live entirely in caller-provided ``tmp_path`` directories and never
touch the real ``data/microstructure/`` tree.

For checks that depend on the locked 60-check semantics (event count,
specific SHA matches, dates, file count, ...), tests use
``monkeypatch`` to override the relevant ``EXPECTED_*`` /
``CANONICAL_*`` constant in :mod:`multiday_derived_gate_checks` and
build a tiny canonical fixture that satisfies the reduced constants.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from typing import Any

import pyarrow as pa

from prometheus.research.microstructure import multiday_derived_gate_checks as mdc
from prometheus.research.microstructure.multiday_derived_gate_checks import (
    MultidayDerivedGateContext,
    MultidayPerFileMeasured,
)
from prometheus.research.microstructure.multiday_derived_gate_io import (
    MultidayDerivedSourceArtefactPaths,
    MultidayLoadedArtefactBundle,
    MultidayPerFileArtefactPaths,
)


def make_canonical_table(num_rows: int = 5) -> pa.Table:
    """Build a tiny canonical 19-column pyarrow Table.

    The resulting table satisfies the per-row content checks for a
    sample date when the caller monkeypatches the relevant per-file
    inventory expected values to match.
    """
    if num_rows < 2:
        raise ValueError("need at least 2 rows to satisfy first/last-row checks")
    row_indices = list(range(num_rows))
    agg_ids = list(range(1_000, 1_000 + num_rows))
    t_values = list(range(1_700_000_000_000, 1_700_000_000_000 + num_rows))
    prices = ["100000.0"] * num_rows
    quantities = ["0.001"] * num_rows
    is_buyer_maker = [True] * num_rows
    first_trade_ids = [10_000 + i * 10 for i in row_indices]
    last_trade_ids = [10_005 + i * 10 for i in row_indices]
    n = num_rows
    columns: dict[str, list[Any]] = {
        "dataset_family": [mdc.CANONICAL_DATASET_FAMILY] * n,
        "dataset_version": [mdc.CANONICAL_DATASET_VERSION] * n,
        "source_dataset_family": ["microstructure_raw_aggtrades_v001"] * n,
        "source_dataset_version": ["v002"] * n,
        "symbol": [mdc.CANONICAL_SYMBOL] * n,
        "utc_date": [mdc.SAMPLE_DATES[0]] * n,
        "agg_trade_id": agg_ids,
        "price": prices,
        "quantity": quantities,
        "first_trade_id": first_trade_ids,
        "last_trade_id": last_trade_ids,
        "transact_time_ms": t_values,
        "is_buyer_maker": is_buyer_maker,
        "source_file_sha256": ["a" * 64] * n,
        "source_manifest_sha256": [mdc.EXPECTED_RAW_MANIFEST_SHA] * n,
        "source_gate_report_id": [mdc.EXPECTED_GATE_REPORT_ID] * n,
        "source_gate_report_sha256": [mdc.EXPECTED_GATE_REPORT_SHA] * n,
        "row_index": row_indices,
        "normalization_schema_version": ["v001"] * n,
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
    return pa.Table.from_pydict(columns, schema=schema)


def make_canonical_per_file_paths(
    *,
    microstructure_root: Path,
    dates: tuple[str, ...] | None = None,
) -> tuple[MultidayPerFileArtefactPaths, ...]:
    """Return a tuple of canonical per-file path entries for the given dates."""
    if dates is None:
        dates = mdc.SAMPLE_DATES
    out: list[MultidayPerFileArtefactPaths] = []
    for date in dates:
        yyyy, mm, _ = date.split("-")
        parquet = (
            microstructure_root
            / "normalized"
            / mdc.CANONICAL_DATASET_FAMILY
            / mdc.CANONICAL_SYMBOL
            / yyyy
            / mm
            / f"{mdc.CANONICAL_SYMBOL}-aggTrades-{date}.parquet"
        )
        sidecar = parquet.with_suffix(parquet.suffix + ".sha256")
        zip_path = (
            microstructure_root
            / "raw"
            / "microstructure_raw_aggtrades_v001"
            / mdc.CANONICAL_SYMBOL
            / yyyy
            / mm
            / f"{mdc.CANONICAL_SYMBOL}-aggTrades-{date}.zip"
        )
        out.append(
            MultidayPerFileArtefactPaths(
                date=date,
                symbol=mdc.CANONICAL_SYMBOL,
                parquet_path=parquet,
                parquet_sidecar_path=sidecar,
                source_zip_path=zip_path,
                expected_parquet_sha="b" * 64,
                expected_parquet_size=1000,
                expected_sidecar_sha="c" * 64,
                expected_sidecar_size=99,
                expected_source_zip_sha="d" * 64,
                expected_event_count=5,
                expected_first_transact_time_ms=1_700_000_000_000,
                expected_last_transact_time_ms=1_700_000_000_004,
                expected_min_agg_trade_id=1_000,
                expected_max_agg_trade_id=1_004,
            )
        )
    return tuple(out)


def make_canonical_source_paths(
    *,
    microstructure_root: Path,
    per_file: tuple[MultidayPerFileArtefactPaths, ...],
) -> MultidayDerivedSourceArtefactPaths:
    return MultidayDerivedSourceArtefactPaths(
        derived_manifest_path=microstructure_root
        / "manifests"
        / "microstructure_normalized_aggtrades_v001__v002.json",
        derived_manifest_sidecar_path=microstructure_root
        / "manifests"
        / "microstructure_normalized_aggtrades_v001__v002.json.sha256",
        raw_manifest_path=microstructure_root
        / "manifests"
        / "microstructure_raw_aggtrades_v001__v002.json",
        raw_manifest_sidecar_path=microstructure_root
        / "manifests"
        / "microstructure_raw_aggtrades_v001__v002.json.sha256",
        acquisition_log_path=microstructure_root
        / "manifests"
        / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json",
        acquisition_log_sidecar_path=microstructure_root
        / "manifests"
        / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json.sha256",
        gate_report_path=microstructure_root
        / "gate-reports"
        / "raw"
        / f"{mdc.EXPECTED_GATE_REPORT_ID}.json",
        gate_report_sidecar_path=microstructure_root
        / "gate-reports"
        / "raw"
        / f"{mdc.EXPECTED_GATE_REPORT_ID}.json.sha256",
        successor_state_path=microstructure_root
        / "successor-state"
        / "microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json",
        successor_state_sidecar_path=microstructure_root
        / "successor-state"
        / "microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json.sha256",
        per_file=per_file,
    )


def make_canonical_derived_manifest(
    *, per_file_inventory: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    if per_file_inventory is None:
        per_file_inventory = [
            {
                "date": date,
                "parquet_path": f"normalized/foo/BTCUSDT/{date}.parquet",
                "parquet_sha256": "b" * 64,
                "parquet_size_bytes": 1000,
                "parquet_sidecar_sha256": "c" * 64,
                "parquet_sidecar_size_bytes": 99,
                "source_zip_path": f"raw/foo/BTCUSDT/{date}.zip",
                "source_file_sha256": "a" * 64,
                "event_count": 5,
                "first_transact_time_ms": 1_700_000_000_000,
                "last_transact_time_ms": 1_700_000_000_004,
                "min_agg_trade_id": 1_000,
                "max_agg_trade_id": 1_004,
            }
            for date in mdc.SAMPLE_DATES
        ]
    return {
        "dataset_family": mdc.CANONICAL_DATASET_FAMILY,
        "dataset_version": mdc.CANONICAL_DATASET_VERSION,
        "schema_version": "v001",
        "source_dataset_family": "microstructure_raw_aggtrades_v001",
        "source_dataset_version": "v002",
        "source_phase_boundary": "4bl-E",
        "source_manifest_path": "manifests/raw.json",
        "source_manifest_sha256": mdc.EXPECTED_RAW_MANIFEST_SHA,
        "source_acquisition_log_path": "manifests/raw_log.json",
        "source_acquisition_log_sha256": mdc.EXPECTED_ACQUISITION_LOG_SHA,
        "source_gate_report_path": "gate-reports/raw/x.json",
        "source_gate_report_id": mdc.EXPECTED_GATE_REPORT_ID,
        "source_gate_report_sha256": mdc.EXPECTED_GATE_REPORT_SHA,
        "source_successor_state_path": "successor-state/x.json",
        "source_successor_state_sha256": mdc.EXPECTED_SUCCESSOR_STATE_SHA,
        "symbol_list": [mdc.CANONICAL_SYMBOL],
        "date_start": mdc.CANONICAL_DATE_START,
        "date_end": mdc.CANONICAL_DATE_END,
        "date_count": len(per_file_inventory),
        "date_list": [entry["date"] for entry in per_file_inventory],
        "expected_file_count": len(per_file_inventory),
        "produced_file_count": len(per_file_inventory),
        "total_event_count": sum(entry["event_count"] for entry in per_file_inventory),
        "per_file_inventory": per_file_inventory,
        "invalid_windows": [],
        "governance_labels": make_canonical_governance_labels(),
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "code_commit_sha": "0" * 40,
        "base_commit_sha": "0" * 40,
        "capture_config_hash": "deadbeef" * 8,
        "created_at_unix_ms": 1_700_000_000_000,
        "created_at_utc": "2024-12-01T00:00:00Z",
        "phase": "4bm-b",
    }


def make_canonical_governance_labels() -> dict[str, Any]:
    return {
        "phase": "4bm-b",
        "source_phase_boundary": "4bl-E",
        "validator": "phase_4ax_aggtrades_v001",
        "stop_trigger_domain": "trade_price_backtest_candidate",
        "feature_computation": "forbidden",
        "strategy_use": "forbidden",
        "source_dataset_family": "microstructure_raw_aggtrades_v001",
        "source_dataset_version": "v002",
        "source_manifest_path": "manifests/raw.json",
        "source_manifest_sha256": mdc.EXPECTED_RAW_MANIFEST_SHA,
        "source_gate_report_id": mdc.EXPECTED_GATE_REPORT_ID,
        "source_gate_report_sha256": mdc.EXPECTED_GATE_REPORT_SHA,
        "source_gate_report_code_commit_sha": "0" * 40,
        "source_successor_state_sha256": mdc.EXPECTED_SUCCESSOR_STATE_SHA,
        "multi_day": True,
        "phase_4bm_b_no_successor_authorization": True,
    }


def make_canonical_raw_manifest() -> dict[str, Any]:
    return {
        "dataset_family": "microstructure_raw_aggtrades_v001",
        "dataset_version": "v002",
        "symbol_list": [mdc.CANONICAL_SYMBOL],
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "total_row_count": mdc.EXPECTED_TOTAL_EVENT_COUNT,
        "date_count": mdc.EXPECTED_DATE_COUNT,
    }


def make_canonical_bundle(
    *,
    derived_manifest: dict[str, Any] | None = None,
    raw_manifest: dict[str, Any] | None = None,
) -> MultidayLoadedArtefactBundle:
    if derived_manifest is None:
        derived_manifest = make_canonical_derived_manifest()
    if raw_manifest is None:
        raw_manifest = make_canonical_raw_manifest()
    return MultidayLoadedArtefactBundle(
        derived_manifest_bytes=b"{}",
        derived_manifest_sha=mdc.EXPECTED_DERIVED_MANIFEST_SHA,
        derived_manifest=derived_manifest,
        derived_sidecar_first_64=mdc.EXPECTED_DERIVED_MANIFEST_SHA,
        raw_manifest_bytes=b"{}",
        raw_manifest_sha=mdc.EXPECTED_RAW_MANIFEST_SHA,
        raw_manifest=raw_manifest,
        raw_manifest_sidecar_first_64=mdc.EXPECTED_RAW_MANIFEST_SHA,
        acquisition_log_sha=mdc.EXPECTED_ACQUISITION_LOG_SHA,
        acquisition_log_sidecar_first_64=mdc.EXPECTED_ACQUISITION_LOG_SHA,
        gate_report_sha=mdc.EXPECTED_GATE_REPORT_SHA,
        gate_report_sidecar_first_64=mdc.EXPECTED_GATE_REPORT_SHA,
        successor_state_sha=mdc.EXPECTED_SUCCESSOR_STATE_SHA,
        successor_state_sidecar_first_64=mdc.EXPECTED_SUCCESSOR_STATE_SHA,
    )


def make_canonical_perfile_measurements(
    paths: MultidayDerivedSourceArtefactPaths,
    *,
    sample_table: pa.Table | None = None,
) -> dict[str, MultidayPerFileMeasured]:
    """Build canonical measurements that match the canonical per-file paths."""
    if sample_table is None:
        sample_table = make_canonical_table(num_rows=5)
    out: dict[str, MultidayPerFileMeasured] = {}
    for pf in paths.per_file:
        m = MultidayPerFileMeasured(date=pf.date)
        m.parquet_sha = pf.expected_parquet_sha
        m.parquet_size = pf.expected_parquet_size
        m.sidecar_sha = pf.expected_sidecar_sha
        m.sidecar_size = pf.expected_sidecar_size
        m.sidecar_first_64 = pf.expected_parquet_sha
        m.source_zip_sha = pf.expected_source_zip_sha
        m.parquet_num_rows = pf.expected_event_count
        if pf.date in mdc.SAMPLE_DATES:
            m.sample_table = sample_table
        out[pf.date] = m
    return out


def make_canonical_context(
    *,
    microstructure_root: Path,
    dates: tuple[str, ...] | None = None,
) -> MultidayDerivedGateContext:
    """Build a fully canonical PASS-shaped MultidayDerivedGateContext."""
    if dates is None:
        dates = mdc.SAMPLE_DATES
    per_file = make_canonical_per_file_paths(
        microstructure_root=microstructure_root, dates=dates,
    )
    paths = make_canonical_source_paths(
        microstructure_root=microstructure_root, per_file=per_file,
    )
    bundle = make_canonical_bundle()
    perfile = make_canonical_perfile_measurements(paths)
    return MultidayDerivedGateContext(paths=paths, bundle=bundle, perfile=perfile)


def replace_per_file(
    pf: MultidayPerFileArtefactPaths, **overrides: Any
) -> MultidayPerFileArtefactPaths:
    return replace(pf, **overrides)


def replace_manifest_field(
    ctx: MultidayDerivedGateContext, *, key: str, value: Any
) -> MultidayDerivedGateContext:
    """Return *ctx* with one derived-manifest field overridden."""
    new_manifest = deepcopy(ctx.bundle.derived_manifest)
    if "." in key:
        outer, inner = key.split(".", 1)
        new_manifest.setdefault(outer, {})
        new_manifest[outer][inner] = value
    else:
        new_manifest[key] = value
    ctx.bundle = replace(
        ctx.bundle,
        derived_manifest=new_manifest,
    )
    return ctx
