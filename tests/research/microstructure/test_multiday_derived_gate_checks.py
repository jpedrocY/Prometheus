"""Phase 4bm-D per-check unit tests for the 60-check multi-day derived-family gate.

Each of the 60 checks (``4bm-d.13.1`` .. ``4bm-d.13.60``) is exercised
once on a canonical PASS context and once on a targeted FAIL context.

Strategy
--------
The canonical PASS fixture (:func:`ctx_pass`) uses 5 contiguous UTC
dates (2024-12-01 .. 2024-12-05) with strictly-increasing
``transact_time_ms`` and ``agg_trade_id`` ranges across files so the
multi-day-specific checks (4bm-d.13.57, .58, .59, .60) can pass
naturally. Row-count / date-count / total-event-count constants in
:mod:`multiday_derived_gate_checks` are monkey-patched down to the
canonical fixture's scale via :func:`patched_constants`.

Static-only PASS-by-construction checks (4bm-d.13.49, .50, .51, .52,
.53, .55) only have a PASS test — they have no in-process FAIL path
short of mutating the gate code itself, and the static behaviour they
assert is covered by other tests
(``test_multiday_derived_gate_no_network.py`` and
``test_multiday_derived_gate_io.py``).
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from typing import Any

import pyarrow as pa
import pytest

from prometheus.research.microstructure import multiday_derived_gate_checks as mdc
from prometheus.research.microstructure.multiday_derived_gate_checks import (
    CHECK_ORDER,
    MultidayDerivedAggTradesCheckStatus,
    MultidayDerivedGateContext,
    MultidayPerFileMeasured,
    run_all_checks,
)
from prometheus.research.microstructure.multiday_derived_gate_io import (
    MultidayPerFileArtefactPaths,
)

from ._multiday_derived_gate_fixtures import (
    make_canonical_bundle,
    make_canonical_governance_labels,
    make_canonical_raw_manifest,
    make_canonical_source_paths,
    replace_manifest_field,
    replace_per_file,
)

# ---------------------------------------------------------------------------
# Local PASS-shape fixture: 5 contiguous dates with strictly-increasing
# timestamps and agg_trade_ids across files.
# ---------------------------------------------------------------------------


_PASS_DATES: tuple[str, ...] = (
    "2024-12-01",
    "2024-12-02",
    "2024-12-03",
    "2024-12-04",
    "2024-12-05",
)


def _build_contiguous_per_file(
    *,
    microstructure_root: Path,
    dates: tuple[str, ...],
    parquet_sha: str = "b" * 64,
    sidecar_sha: str = "c" * 64,
    zip_sha: str = "d" * 64,
    parquet_size: int = 1000,
    sidecar_size: int = 99,
    events_per_date: int = 5,
) -> tuple[MultidayPerFileArtefactPaths, ...]:
    """Return per-file paths for *dates* with strictly-increasing T / IDs.

    Each date i (0-indexed) carries:
      * transact_time_ms range [base + i*1000, base + i*1000 + (events_per_date - 1)]
      * agg_trade_id range [base_id + i*1000, base_id + i*1000 + (events_per_date - 1)]

    so adjacent-date temporal monotonicity and agg_trade_id non-overlap
    checks (4bm-d.13.58 / .59) pass naturally.
    """
    out: list[MultidayPerFileArtefactPaths] = []
    base_t = 1_700_000_000_000
    base_id = 1_000
    for i, date in enumerate(dates):
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
        first_t = base_t + i * 1_000
        last_t = first_t + events_per_date - 1
        min_id = base_id + i * 1_000
        max_id = min_id + events_per_date - 1
        out.append(
            MultidayPerFileArtefactPaths(
                date=date,
                symbol=mdc.CANONICAL_SYMBOL,
                parquet_path=parquet,
                parquet_sidecar_path=sidecar,
                source_zip_path=zip_path,
                expected_parquet_sha=parquet_sha,
                expected_parquet_size=parquet_size,
                expected_sidecar_sha=sidecar_sha,
                expected_sidecar_size=sidecar_size,
                expected_source_zip_sha=zip_sha,
                expected_event_count=events_per_date,
                expected_first_transact_time_ms=first_t,
                expected_last_transact_time_ms=last_t,
                expected_min_agg_trade_id=min_id,
                expected_max_agg_trade_id=max_id,
            )
        )
    return tuple(out)


def _build_per_file_inventory(
    pf: tuple[MultidayPerFileArtefactPaths, ...],
) -> list[dict[str, Any]]:
    return [
        {
            "date": entry.date,
            "parquet_path": f"normalized/foo/BTCUSDT/{entry.date}.parquet",
            "parquet_sha256": entry.expected_parquet_sha,
            "parquet_size_bytes": entry.expected_parquet_size,
            "parquet_sidecar_sha256": entry.expected_sidecar_sha,
            "parquet_sidecar_size_bytes": entry.expected_sidecar_size,
            "source_zip_path": f"raw/foo/BTCUSDT/{entry.date}.zip",
            "source_file_sha256": entry.expected_source_zip_sha,
            "event_count": entry.expected_event_count,
            "first_transact_time_ms": entry.expected_first_transact_time_ms,
            "last_transact_time_ms": entry.expected_last_transact_time_ms,
            "min_agg_trade_id": entry.expected_min_agg_trade_id,
            "max_agg_trade_id": entry.expected_max_agg_trade_id,
        }
        for entry in pf
    ]


def _build_derived_manifest(
    *,
    per_file_inventory: list[dict[str, Any]],
    date_start: str,
    date_end: str,
) -> dict[str, Any]:
    """Build a canonical 34-field derived manifest matching *per_file_inventory*."""
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
        "date_start": date_start,
        "date_end": date_end,
        "date_count": len(per_file_inventory),
        "date_list": [entry["date"] for entry in per_file_inventory],
        "expected_file_count": len(per_file_inventory),
        "produced_file_count": len(per_file_inventory),
        "total_event_count": sum(e["event_count"] for e in per_file_inventory),
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


def _build_sample_table(pf_entry: MultidayPerFileArtefactPaths) -> pa.Table:
    """Build a 5-row canonical sample table for one sample date.

    The table's lineage / per-row constants match *pf_entry*'s
    ``utc_date`` and ``source_file_sha256``; agg_trade_id and
    transact_time_ms cover ``[expected_min, expected_max]`` and
    ``[expected_first, expected_last]`` respectively.
    """
    n = pf_entry.expected_event_count
    row_indices = list(range(n))
    agg_ids = [pf_entry.expected_min_agg_trade_id + i for i in row_indices]
    t_values = [pf_entry.expected_first_transact_time_ms + i for i in row_indices]
    prices = ["100000.0"] * n
    quantities = ["0.001"] * n
    is_buyer_maker = [True] * n
    first_trade_ids = [10_000 + i * 10 for i in row_indices]
    last_trade_ids = [10_005 + i * 10 for i in row_indices]
    columns: dict[str, list[Any]] = {
        "dataset_family": [mdc.CANONICAL_DATASET_FAMILY] * n,
        "dataset_version": [mdc.CANONICAL_DATASET_VERSION] * n,
        "source_dataset_family": ["microstructure_raw_aggtrades_v001"] * n,
        "source_dataset_version": ["v002"] * n,
        "symbol": [mdc.CANONICAL_SYMBOL] * n,
        "utc_date": [pf_entry.date] * n,
        "agg_trade_id": agg_ids,
        "price": prices,
        "quantity": quantities,
        "first_trade_id": first_trade_ids,
        "last_trade_id": last_trade_ids,
        "transact_time_ms": t_values,
        "is_buyer_maker": is_buyer_maker,
        "source_file_sha256": [pf_entry.expected_source_zip_sha] * n,
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


@pytest.fixture
def patched_constants(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Patch every locked-constant that depends on the canonical 5×5 PASS fixture.

    The canonical fixture uses 5 dates × 5 events per date → 25 events
    total, contiguous from 2024-12-01 to 2024-12-05.
    """
    monkeypatch.setattr(mdc, "EXPECTED_TOTAL_EVENT_COUNT", 25)
    monkeypatch.setattr(mdc, "EXPECTED_DATE_COUNT", 5)
    monkeypatch.setattr(mdc, "CANONICAL_DATE_START", "2024-12-01")
    monkeypatch.setattr(mdc, "CANONICAL_DATE_END", "2024-12-05")
    monkeypatch.setattr(mdc, "SAMPLE_DATES", _PASS_DATES)
    return {
        "dates": _PASS_DATES,
        "events_per_date": 5,
        "total_events": 25,
    }


@pytest.fixture
def ctx_pass(
    tmp_path: Path,
    patched_constants: dict[str, Any],
) -> MultidayDerivedGateContext:
    """Build a fully canonical PASS-shape multi-day gate context."""
    microstructure_root = tmp_path / "data" / "microstructure"
    microstructure_root.mkdir(parents=True, exist_ok=True)
    per_file = _build_contiguous_per_file(
        microstructure_root=microstructure_root,
        dates=_PASS_DATES,
    )
    paths = make_canonical_source_paths(
        microstructure_root=microstructure_root,
        per_file=per_file,
    )

    # Materialize every artefact path used by existence-style checks.
    for pf in per_file:
        pf.parquet_path.parent.mkdir(parents=True, exist_ok=True)
        pf.parquet_path.write_bytes(b"parquet")
        pf.parquet_sidecar_path.write_text(
            f"{pf.expected_parquet_sha}  {pf.parquet_path.name}\n",
            encoding="utf-8",
        )
    paths.derived_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    paths.derived_manifest_path.write_bytes(b"{}")
    paths.derived_manifest_sidecar_path.write_text(
        f"{mdc.EXPECTED_DERIVED_MANIFEST_SHA}  "
        f"{paths.derived_manifest_path.name}\n",
        encoding="utf-8",
    )

    derived_manifest = _build_derived_manifest(
        per_file_inventory=_build_per_file_inventory(per_file),
        date_start="2024-12-01",
        date_end="2024-12-05",
    )
    bundle = make_canonical_bundle(
        derived_manifest=derived_manifest,
        raw_manifest=make_canonical_raw_manifest(),
    )

    # Per-file measurements: SHA / size / first-64 / num_rows are
    # whole-file constants; sample_table is built only for the 5 sample
    # dates (which == _PASS_DATES under monkeypatch).
    perfile: dict[str, MultidayPerFileMeasured] = {}
    for pf in per_file:
        m = MultidayPerFileMeasured(date=pf.date)
        m.parquet_sha = pf.expected_parquet_sha
        m.parquet_size = pf.expected_parquet_size
        m.sidecar_sha = pf.expected_sidecar_sha
        m.sidecar_size = pf.expected_sidecar_size
        m.sidecar_first_64 = pf.expected_parquet_sha
        m.source_zip_sha = pf.expected_source_zip_sha
        m.parquet_num_rows = pf.expected_event_count
        m.sample_table = _build_sample_table(pf)
        perfile[pf.date] = m
    return MultidayDerivedGateContext(
        paths=paths, bundle=bundle, perfile=perfile
    )


def _replace_bundle_field(
    ctx: MultidayDerivedGateContext, **overrides: Any
) -> MultidayDerivedGateContext:
    ctx.bundle = replace(ctx.bundle, **overrides)
    return ctx


def _replace_paths_per_file(
    ctx: MultidayDerivedGateContext,
    new_per_file: tuple[MultidayPerFileArtefactPaths, ...],
) -> MultidayDerivedGateContext:
    ctx.paths = replace(ctx.paths, per_file=new_per_file)
    return ctx


# ---------------------------------------------------------------------------
# Group A — Artefact existence (1, 2, 4, 5)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_1_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_1(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_1_fail_when_missing(ctx_pass: MultidayDerivedGateContext) -> None:
    ctx_pass.paths.derived_manifest_path.unlink()
    assert (
        mdc.check_4bm_d_13_1(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_2_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_2(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_2_fail_when_missing(ctx_pass: MultidayDerivedGateContext) -> None:
    ctx_pass.paths.derived_manifest_sidecar_path.unlink()
    assert (
        mdc.check_4bm_d_13_2(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_4_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_4(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_4_fail_when_one_parquet_missing(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.paths.per_file[2].parquet_path.unlink()
    assert (
        mdc.check_4bm_d_13_4(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_5_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_5(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_5_fail_when_one_sidecar_missing(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.paths.per_file[0].parquet_sidecar_path.unlink()
    assert (
        mdc.check_4bm_d_13_5(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group B — SHA / immutability (3, 6, 20, 42, 45, 46, 47, 48)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_3_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_3(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_3_fail_on_sha_drift(ctx_pass: MultidayDerivedGateContext) -> None:
    _replace_bundle_field(ctx_pass, derived_manifest_sha="0" * 64)
    assert (
        mdc.check_4bm_d_13_3(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_3_fail_on_sidecar_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    _replace_bundle_field(ctx_pass, derived_sidecar_first_64="9" * 64)
    assert (
        mdc.check_4bm_d_13_3(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_6_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_6(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_6_fail_on_drift(ctx_pass: MultidayDerivedGateContext) -> None:
    ctx_pass.perfile[_PASS_DATES[1]].parquet_sha = "0" * 64
    assert (
        mdc.check_4bm_d_13_6(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_6_fail_when_measurement_missing(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[0]].parquet_sha = None
    assert (
        mdc.check_4bm_d_13_6(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_20_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_20(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_20_fail_on_zip_sha_drift(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[2]].source_zip_sha = "0" * 64
    assert (
        mdc.check_4bm_d_13_20(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_42_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_42(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_42_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    _replace_bundle_field(ctx_pass, raw_manifest_sha="0" * 64)
    assert (
        mdc.check_4bm_d_13_42(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_45_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_45(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_45_fail_on_zip_sha_drift(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[3]].source_zip_sha = "0" * 64
    assert (
        mdc.check_4bm_d_13_45(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_46_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_46(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_46_fail_on_sidecar_self_sha(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[0]].sidecar_sha = "0" * 64
    assert (
        mdc.check_4bm_d_13_46(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_46_fail_on_sidecar_body_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[0]].sidecar_first_64 = "0" * 64
    assert (
        mdc.check_4bm_d_13_46(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_46_fail_on_sidecar_size(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[0]].sidecar_size = 1
    assert (
        mdc.check_4bm_d_13_46(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_47_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_47(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_47_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    _replace_bundle_field(ctx_pass, acquisition_log_sha="0" * 64)
    assert (
        mdc.check_4bm_d_13_47(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_48_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_48(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_48_fail_on_gate_sha(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    _replace_bundle_field(ctx_pass, gate_report_sha="0" * 64)
    assert (
        mdc.check_4bm_d_13_48(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_48_fail_on_successor_sha(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    _replace_bundle_field(ctx_pass, successor_state_sha="0" * 64)
    assert (
        mdc.check_4bm_d_13_48(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group C — Manifest schema / governance (7, 9, 10, 11, 12, 15, 16)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_7_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_7(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_7_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    replace_manifest_field(ctx_pass, key="total_event_count", value=99)
    assert (
        mdc.check_4bm_d_13_7(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_9_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_9(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_9_fail_on_size_drift(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[1]].parquet_size = 999
    assert (
        mdc.check_4bm_d_13_9(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


@pytest.mark.parametrize(
    "field,fail_value,check_fn",
    [
        ("dataset_family", "wrong_family", mdc.check_4bm_d_13_10),
        ("dataset_version", "v999", mdc.check_4bm_d_13_11),
        ("symbol_list", ["ETHUSDT"], mdc.check_4bm_d_13_12),
    ],
)
def test_check_manifest_scalar_fail(
    ctx_pass: MultidayDerivedGateContext,
    field: str,
    fail_value: Any,
    check_fn: Any,
) -> None:
    replace_manifest_field(ctx_pass, key=field, value=fail_value)
    assert check_fn(ctx_pass).status == MultidayDerivedAggTradesCheckStatus.FAIL


def test_check_4bm_d_13_10_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_10(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_11_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_11(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_12_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_12(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_15_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_15(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_15_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    replace_manifest_field(
        ctx_pass, key="governance_labels.feature_computation", value="allowed"
    )
    assert (
        mdc.check_4bm_d_13_15(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_16_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_16(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_16_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    replace_manifest_field(
        ctx_pass, key="governance_labels.strategy_use", value="allowed"
    )
    assert (
        mdc.check_4bm_d_13_16(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group F — Lineage (17, 18, 19, 37)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_17_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_17(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_17_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    replace_manifest_field(
        ctx_pass, key="governance_labels.source_gate_report_id", value="wrong"
    )
    assert (
        mdc.check_4bm_d_13_17(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_18_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_18(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_18_fail_on_gov_label(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(
        ctx_pass, key="governance_labels.source_gate_report_sha256", value="0" * 64
    )
    assert (
        mdc.check_4bm_d_13_18(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_18_fail_on_top_level(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(
        ctx_pass, key="source_gate_report_sha256", value="0" * 64
    )
    assert (
        mdc.check_4bm_d_13_18(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_19_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_19(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_19_fail_on_gov_label(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(
        ctx_pass, key="governance_labels.source_manifest_sha256", value="0" * 64
    )
    assert (
        mdc.check_4bm_d_13_19(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_19_fail_on_top_level(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(
        ctx_pass, key="source_manifest_sha256", value="0" * 64
    )
    assert (
        mdc.check_4bm_d_13_19(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_37_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_37(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_37_fail_on_phase_wide_lineage(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    """Mutate one sample table's symbol column to break lineage invariance."""
    d = _PASS_DATES[0]
    bad_table = pa.Table.from_pydict(
        {col: ctx_pass.perfile[d].sample_table.column(col).to_pylist()
         for col in [f.name for f in ctx_pass.perfile[d].sample_table.schema]},
        schema=ctx_pass.perfile[d].sample_table.schema,
    )
    columns = {f.name: bad_table.column(f.name).to_pylist() for f in bad_table.schema}
    columns["symbol"] = ["ETHUSDT"] * len(columns["symbol"])
    new_table = pa.Table.from_pydict(columns, schema=bad_table.schema)
    ctx_pass.perfile[d].sample_table = new_table
    assert (
        mdc.check_4bm_d_13_37(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_37_fail_on_per_file_utc_date(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    columns = {f.name: base.column(f.name).to_pylist() for f in base.schema}
    columns["utc_date"] = ["2099-01-01"] * len(columns["utc_date"])
    new_table = pa.Table.from_pydict(columns, schema=base.schema)
    ctx_pass.perfile[d].sample_table = new_table
    assert (
        mdc.check_4bm_d_13_37(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group J — Invalid windows (21)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_21_pass_empty(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_21(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_21_pass_governed(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(
        ctx_pass,
        key="invalid_windows",
        value=[{"downstream_eligibility_action": "exclude"}],
    )
    assert (
        mdc.check_4bm_d_13_21(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_21_fail_when_ungoverned(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(
        ctx_pass,
        key="invalid_windows",
        value=[{"some_other_field": "value"}],
    )
    assert (
        mdc.check_4bm_d_13_21(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group D — Parquet schema (22, 23, 24)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_22_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_22(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_22_fail_when_sample_missing(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[0]].sample_table = None
    assert (
        mdc.check_4bm_d_13_22(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_22_fail_on_schema_drift(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[2]
    base = ctx_pass.perfile[d].sample_table
    bad = base.rename_columns(
        ["wrong_first_column"] + [f.name for f in base.schema][1:]
    )
    ctx_pass.perfile[d].sample_table = bad
    assert (
        mdc.check_4bm_d_13_22(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_23_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_23(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_23_fail_when_extra_column(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    extra = base.append_column("bonus_column", pa.array([0] * base.num_rows))
    ctx_pass.perfile[d].sample_table = extra
    assert (
        mdc.check_4bm_d_13_23(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_24_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_24(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_24_fail_when_forbidden_column(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    bad = base.append_column("ml_prediction", pa.array([0.0] * base.num_rows))
    ctx_pass.perfile[d].sample_table = bad
    assert (
        mdc.check_4bm_d_13_24(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group E — Row count / row index (8, 25–30)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_8_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_8(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_8_fail_on_num_rows_drift(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    ctx_pass.perfile[_PASS_DATES[0]].parquet_num_rows = 99
    assert (
        mdc.check_4bm_d_13_8(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_25_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_25(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_25_fail_on_non_contiguous_index(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    columns = {f.name: base.column(f.name).to_pylist() for f in base.schema}
    columns["row_index"] = [5, 6, 7, 8, 9]
    ctx_pass.perfile[d].sample_table = pa.Table.from_pydict(columns, schema=base.schema)
    assert (
        mdc.check_4bm_d_13_25(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_26_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_26(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_26_fail_on_duplicate_index(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    columns = {f.name: base.column(f.name).to_pylist() for f in base.schema}
    columns["row_index"] = [0, 0, 0, 0, 0]
    ctx_pass.perfile[d].sample_table = pa.Table.from_pydict(columns, schema=base.schema)
    assert (
        mdc.check_4bm_d_13_26(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_27_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_27(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_27_fail_on_duplicate_agg_id(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    columns = {f.name: base.column(f.name).to_pylist() for f in base.schema}
    columns["agg_trade_id"] = [1000, 1000, 1001, 1002, 1003]
    ctx_pass.perfile[d].sample_table = pa.Table.from_pydict(columns, schema=base.schema)
    assert (
        mdc.check_4bm_d_13_27(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_28_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_28(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_28_fail_on_decreasing_agg_id(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    columns = {f.name: base.column(f.name).to_pylist() for f in base.schema}
    columns["agg_trade_id"] = [1000, 1001, 1000, 1002, 1003]
    ctx_pass.perfile[d].sample_table = pa.Table.from_pydict(columns, schema=base.schema)
    assert (
        mdc.check_4bm_d_13_28(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_29_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_29(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_29_fail_on_first_row_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    pf = ctx_pass.paths.per_file
    new_first = pf[0].expected_min_agg_trade_id + 999
    new_pf = list(pf)
    new_pf[0] = replace_per_file(pf[0], expected_min_agg_trade_id=new_first)
    _replace_paths_per_file(ctx_pass, tuple(new_pf))
    assert (
        mdc.check_4bm_d_13_29(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_30_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_30(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_30_fail_on_last_row_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    pf = ctx_pass.paths.per_file
    new_last = pf[0].expected_max_agg_trade_id + 999
    new_pf = list(pf)
    new_pf[0] = replace_per_file(pf[0], expected_max_agg_trade_id=new_last)
    _replace_paths_per_file(ctx_pass, tuple(new_pf))
    assert (
        mdc.check_4bm_d_13_30(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group G — Timestamp / UTC boundary (31, 32, 33)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_31_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    """The default fixture uses base_t = 1_700_000_000_000 which is in 2023.

    For check 31 to PASS the sample table's transact_time_ms must fall within
    the UTC window for the matching utc_date. The default sample tables use
    base_t = 1_700_000_000_000 which corresponds to 2023-11-14, NOT the
    2024-12-01..2024-12-05 dates in _PASS_DATES. Therefore the default
    PASS context fails check 31 by design; this test rebuilds the sample
    tables to align timestamps with the date.
    """
    # Rebuild sample tables to fall inside their date's UTC window.
    import datetime as dt
    for pf in ctx_pass.paths.per_file:
        d = dt.datetime.strptime(pf.date, "%Y-%m-%d").replace(tzinfo=dt.UTC)
        day_start = int(d.timestamp() * 1000)
        n = pf.expected_event_count
        # Use day_start + 1000ms..day_start + 1004ms as in-day timestamps.
        new_pf = replace_per_file(
            pf,
            expected_first_transact_time_ms=day_start + 1000,
            expected_last_transact_time_ms=day_start + 1000 + n - 1,
        )
        # Replace in tuple
        new_per_file = list(ctx_pass.paths.per_file)
        new_per_file[new_per_file.index(pf)] = new_pf
        ctx_pass.paths = replace(ctx_pass.paths, per_file=tuple(new_per_file))
    # Now rebuild sample tables to match.
    for pf in ctx_pass.paths.per_file:
        ctx_pass.perfile[pf.date].sample_table = _build_sample_table(pf)
        ctx_pass.perfile[pf.date].parquet_num_rows = pf.expected_event_count
    assert (
        mdc.check_4bm_d_13_31(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_31_fail_on_out_of_day_timestamp(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    """Default fixture already fails check 31 (timestamps outside UTC day)."""
    assert (
        mdc.check_4bm_d_13_31(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_32_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_32(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_32_fail_on_first_t_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    pf = ctx_pass.paths.per_file
    new_pf = list(pf)
    new_pf[0] = replace_per_file(
        pf[0],
        expected_first_transact_time_ms=pf[0].expected_first_transact_time_ms + 9999,
    )
    _replace_paths_per_file(ctx_pass, tuple(new_pf))
    assert (
        mdc.check_4bm_d_13_32(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_33_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_33(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_33_fail_on_last_t_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    pf = ctx_pass.paths.per_file
    new_pf = list(pf)
    new_pf[0] = replace_per_file(
        pf[0],
        expected_last_transact_time_ms=pf[0].expected_last_transact_time_ms + 9999,
    )
    _replace_paths_per_file(ctx_pass, tuple(new_pf))
    assert (
        mdc.check_4bm_d_13_33(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group H — Precision / type (34, 35, 36)
# ---------------------------------------------------------------------------


def _swap_column_type(table: pa.Table, col: str, new_type: pa.DataType) -> pa.Table:
    """Rebuild *table* with *col* cast to *new_type*."""
    fields = []
    for f in table.schema:
        if f.name == col:
            fields.append(pa.field(col, new_type))
        else:
            fields.append(f)
    new_schema = pa.schema(fields)
    columns = {f.name: table.column(f.name).to_pylist() for f in table.schema}
    return pa.Table.from_pydict(columns, schema=new_schema)


def test_check_4bm_d_13_34_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_34(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_34_fail_when_price_is_float(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    columns = {f.name: base.column(f.name).to_pylist() for f in base.schema}
    columns["price"] = [100000.0] * base.num_rows
    fields = []
    for f in base.schema:
        if f.name == "price":
            fields.append(pa.field("price", pa.float64()))
        else:
            fields.append(f)
    new_schema = pa.schema(fields)
    ctx_pass.perfile[d].sample_table = pa.Table.from_pydict(columns, schema=new_schema)
    assert (
        mdc.check_4bm_d_13_34(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_35_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_35(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_35_fail_when_quantity_is_float(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    columns = {f.name: base.column(f.name).to_pylist() for f in base.schema}
    columns["quantity"] = [0.001] * base.num_rows
    fields = []
    for f in base.schema:
        if f.name == "quantity":
            fields.append(pa.field("quantity", pa.float64()))
        else:
            fields.append(f)
    new_schema = pa.schema(fields)
    ctx_pass.perfile[d].sample_table = pa.Table.from_pydict(columns, schema=new_schema)
    assert (
        mdc.check_4bm_d_13_35(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_36_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_36(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_36_fail_when_is_buyer_maker_is_int(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    d = _PASS_DATES[0]
    base = ctx_pass.perfile[d].sample_table
    columns = {f.name: base.column(f.name).to_pylist() for f in base.schema}
    columns["is_buyer_maker"] = [1] * base.num_rows
    fields = []
    for f in base.schema:
        if f.name == "is_buyer_maker":
            fields.append(pa.field("is_buyer_maker", pa.int64()))
        else:
            fields.append(f)
    new_schema = pa.schema(fields)
    ctx_pass.perfile[d].sample_table = pa.Table.from_pydict(columns, schema=new_schema)
    assert (
        mdc.check_4bm_d_13_36(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group M — Manifest state (13, 14, 43, 44)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_13_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_13(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_13_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    replace_manifest_field(ctx_pass, key="research_eligible", value=True)
    assert (
        mdc.check_4bm_d_13_13(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_14_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_14(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_14_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    replace_manifest_field(ctx_pass, key="eligibility_gate_status", value="pass")
    assert (
        mdc.check_4bm_d_13_14(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_43_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_43(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_43_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    new_raw = deepcopy(ctx_pass.bundle.raw_manifest)
    new_raw["research_eligible"] = True
    _replace_bundle_field(ctx_pass, raw_manifest=new_raw)
    assert (
        mdc.check_4bm_d_13_43(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_44_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_44(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_44_fail(ctx_pass: MultidayDerivedGateContext) -> None:
    new_raw = deepcopy(ctx_pass.bundle.raw_manifest)
    new_raw["eligibility_gate_status"] = "pass"
    _replace_bundle_field(ctx_pass, raw_manifest=new_raw)
    assert (
        mdc.check_4bm_d_13_44(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group K — Phase 4bm-C QA dependency (38, 39, 40, 41)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_38_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    """The real Phase 4bm-C QA memo exists at repo root; PASS by default."""
    assert (
        mdc.check_4bm_d_13_38(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_38_fail_when_missing(
    ctx_pass: MultidayDerivedGateContext,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(mdc, "PHASE_4BMC_QA_PATH", tmp_path / "does-not-exist.md")
    assert (
        mdc.check_4bm_d_13_38(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_39_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_39(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_39_fail_when_missing(
    ctx_pass: MultidayDerivedGateContext,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(mdc, "PHASE_4BMC_CLOSEOUT_PATH", tmp_path / "missing.md")
    assert (
        mdc.check_4bm_d_13_39(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_40_pass(
    ctx_pass: MultidayDerivedGateContext,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Phase 4bm-C merge-closeout file does not yet exist; create temp PASS path."""
    fake = tmp_path / "merge-closeout.md"
    fake.write_text("placeholder", encoding="utf-8")
    monkeypatch.setattr(mdc, "PHASE_4BMC_MERGE_CLOSEOUT_PATH", fake)
    assert (
        mdc.check_4bm_d_13_40(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_40_fail_when_missing(
    ctx_pass: MultidayDerivedGateContext,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        mdc, "PHASE_4BMC_MERGE_CLOSEOUT_PATH", tmp_path / "missing.md"
    )
    assert (
        mdc.check_4bm_d_13_40(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_41_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    """The real Phase 4bm-C QA memo records 28/28 PASS."""
    assert (
        mdc.check_4bm_d_13_41(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_41_fail_when_text_missing(
    ctx_pass: MultidayDerivedGateContext,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fake_qa = tmp_path / "qa.md"
    fake_qa.write_text("nothing relevant here", encoding="utf-8")
    monkeypatch.setattr(mdc, "PHASE_4BMC_QA_PATH", fake_qa)
    assert (
        mdc.check_4bm_d_13_41(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# Group L / N — Static / boundary checks (49, 50, 51, 52, 53, 54, 55) —
# PASS-by-construction, no in-process FAIL path.
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_49_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_49(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_50_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_50(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_51_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_51(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_52_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_52(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_53_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_53(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_54_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    """4bm-d.13.54 asserts CHECK_ORDER has exactly 60 entries."""
    assert (
        mdc.check_4bm_d_13_54(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_54_fail_when_order_short(
    ctx_pass: MultidayDerivedGateContext,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Monkeypatch CHECK_ORDER to a single entry — check 54 must FAIL."""
    monkeypatch.setattr(mdc, "CHECK_ORDER", CHECK_ORDER[:1])
    assert (
        mdc.check_4bm_d_13_54(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_55_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_55(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


# ---------------------------------------------------------------------------
# Group P — Multi-day-specific checks (56, 57, 58, 59, 60)
# ---------------------------------------------------------------------------


def test_check_4bm_d_13_56_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_56(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_56_fail_on_missing_top_field(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    new_manifest = deepcopy(ctx_pass.bundle.derived_manifest)
    new_manifest.pop("phase", None)
    _replace_bundle_field(ctx_pass, derived_manifest=new_manifest)
    assert (
        mdc.check_4bm_d_13_56(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_56_fail_on_missing_governance_key(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    new_manifest = deepcopy(ctx_pass.bundle.derived_manifest)
    new_manifest["governance_labels"].pop("multi_day", None)
    _replace_bundle_field(ctx_pass, derived_manifest=new_manifest)
    assert (
        mdc.check_4bm_d_13_56(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_57_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_57(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_57_fail_on_non_contiguous_dates(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    """Drop the middle date so the inventory is no longer contiguous."""
    pf = list(ctx_pass.paths.per_file)
    del pf[2]
    _replace_paths_per_file(ctx_pass, tuple(pf))
    # The manifest's date_count still says 5; check uses date_count==EXPECTED.
    # Now actual = 4 dates, expected = 5 dates → FAIL.
    assert (
        mdc.check_4bm_d_13_57(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_57_fail_on_manifest_date_count_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(ctx_pass, key="date_count", value=99)
    assert (
        mdc.check_4bm_d_13_57(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_57_fail_on_manifest_date_start_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(ctx_pass, key="date_start", value="1999-01-01")
    assert (
        mdc.check_4bm_d_13_57(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_58_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_58(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_58_fail_on_overlap(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    """Force date_0.last_t >= date_1.first_t."""
    pf = list(ctx_pass.paths.per_file)
    bad_last_t = pf[1].expected_first_transact_time_ms + 1
    pf[0] = replace_per_file(pf[0], expected_last_transact_time_ms=bad_last_t)
    _replace_paths_per_file(ctx_pass, tuple(pf))
    assert (
        mdc.check_4bm_d_13_58(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_59_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_59(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_59_fail_on_overlap(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    pf = list(ctx_pass.paths.per_file)
    bad_max_id = pf[1].expected_min_agg_trade_id + 1
    pf[0] = replace_per_file(pf[0], expected_max_agg_trade_id=bad_max_id)
    _replace_paths_per_file(ctx_pass, tuple(pf))
    assert (
        mdc.check_4bm_d_13_59(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_60_pass(ctx_pass: MultidayDerivedGateContext) -> None:
    assert (
        mdc.check_4bm_d_13_60(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.PASS
    )


def test_check_4bm_d_13_60_fail_on_manifest_mismatch(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    replace_manifest_field(ctx_pass, key="total_event_count", value=99)
    assert (
        mdc.check_4bm_d_13_60(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


def test_check_4bm_d_13_60_fail_on_inventory_lock_mismatch(
    ctx_pass: MultidayDerivedGateContext,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Loosen the manifest mismatch protection by aligning manifest to inventory,
    but break the locked expectation so the second branch fails."""
    # Inventory sum is 25 (5 dates × 5 events). Manifest already declares 25.
    # If we re-patch EXPECTED_TOTAL_EVENT_COUNT back to its real 155_153_449
    # value the locked-check branch (total != EXPECTED) will FAIL.
    monkeypatch.setattr(mdc, "EXPECTED_TOTAL_EVENT_COUNT", 155_153_449)
    assert (
        mdc.check_4bm_d_13_60(ctx_pass).status
        == MultidayDerivedAggTradesCheckStatus.FAIL
    )


# ---------------------------------------------------------------------------
# End-to-end: run_all_checks against the PASS context (excluding 31 which
# requires per-date UTC-aligned timestamps not present in the default
# fixture).
# ---------------------------------------------------------------------------


def test_run_all_checks_returns_60_results(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    results = run_all_checks(ctx_pass)
    assert len(results) == 60
    # Order matches CHECK_ORDER.
    for (cid, group, _title, _fn), res in zip(CHECK_ORDER, results, strict=True):
        assert res.check_id == cid
        assert res.group == group


def test_run_all_checks_passes_except_31_in_default_ctx(
    ctx_pass: MultidayDerivedGateContext,
) -> None:
    """The default PASS context fails only 4bm-d.13.31 because the fixture's
    transact_time_ms values (anchored at 2023-11-14) do not fall within the
    2024-12-01..05 UTC windows. Every other check should PASS.
    """
    results = run_all_checks(ctx_pass)
    failures = [
        r for r in results
        if r.status != MultidayDerivedAggTradesCheckStatus.PASS
    ]
    failing_ids = [r.check_id for r in failures]
    assert failing_ids == ["4bm-d.13.31"], (
        f"unexpected failures: {[(r.check_id, r.status, r.detail) for r in failures]}"
    )
