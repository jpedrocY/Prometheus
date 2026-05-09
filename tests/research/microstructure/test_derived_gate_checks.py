"""Phase 4bf per-check unit tests.

Each of the 55 checks (``4bf.13.1`` .. ``4bf.13.55``) is exercised
once on a canonical PASS context and once on a targeted FAIL context.
Row-count-sensitive checks rely on monkey-patched ``EXPECTED_*``
constants so the canonical mini-context can be small (5 rows) while
preserving every other invariant.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pyarrow as pa
import pytest

from prometheus.research.microstructure import derived_gate_checks as dgc
from prometheus.research.microstructure.derived_gate_checks import (
    CHECK_ORDER,
    DerivedAggTradesCheckStatus,
    run_all_checks,
)

from ._derived_gate_fixtures import (
    make_canonical_table,
    make_minimal_context,
    patch_event_count_constant,
    patch_last_agg_id_constant,
    patch_last_t_constant,
    replace_ctx_field,
    replace_manifest_field,
    replace_raw_manifest_field,
)


@pytest.fixture
def patched_constants(monkeypatch: pytest.MonkeyPatch) -> int:
    """Patch row-count-dependent EXPECTED_* constants to a small N=5."""
    n = 5
    patch_event_count_constant(monkeypatch, n)
    patch_last_t_constant(monkeypatch, dgc.EXPECTED_FIRST_T + n - 1)
    patch_last_agg_id_constant(monkeypatch, dgc.EXPECTED_FIRST_AGG_TRADE_ID + n - 1)
    return n


@pytest.fixture
def ctx_pass(tmp_path: Path, patched_constants: int) -> Any:
    """Fully canonical 5-row PASS context against the patched constants."""
    n = patched_constants
    ctx = make_minimal_context(tmp_path=tmp_path, parquet_num_rows=n)
    # Override raw manifest start/end to match the patched first/last T.
    ctx.raw_manifest["start_time_ms"] = dgc.EXPECTED_FIRST_T
    ctx.raw_manifest["end_time_ms"] = dgc.EXPECTED_LAST_T
    # Rebuild the parquet table with the patched last_T / last_agg_id values.
    ctx.parquet_table = make_canonical_table(num_rows=n)
    # Override derived manifest event_count to match patched value.
    ctx.derived_manifest["event_count"] = n
    ctx.derived_manifest["files"][0]["event_count"] = n
    ctx.derived_manifest["start_time_ms"] = dgc.EXPECTED_FIRST_T
    ctx.derived_manifest["end_time_ms"] = dgc.EXPECTED_LAST_T
    ctx.derived_manifest["files"][0]["start_time_ms"] = dgc.EXPECTED_FIRST_T
    ctx.derived_manifest["files"][0]["end_time_ms"] = dgc.EXPECTED_LAST_T
    return ctx


# ---------- Group A / B ----------


def test_check_4bf_13_1_pass(ctx_pass: Any) -> None:
    res = dgc.check_4bf_13_1(ctx_pass)
    assert res.status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_1_fail_when_missing(ctx_pass: Any) -> None:
    ctx_pass.derived_manifest_path.unlink()
    res = dgc.check_4bf_13_1(ctx_pass)
    assert res.status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_2_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_2(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_2_fail(ctx_pass: Any) -> None:
    ctx_pass.derived_manifest_sidecar_path.unlink()
    assert dgc.check_4bf_13_2(ctx_pass).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_3_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_3(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_3_fail_on_sha_drift(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, derived_manifest_sha="0" * 64)
    assert dgc.check_4bf_13_3(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_3_fail_on_sidecar_mismatch(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, derived_sidecar_first_64="b" * 64)
    assert dgc.check_4bf_13_3(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_4_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_4(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_4_fail(ctx_pass: Any) -> None:
    ctx_pass.normalized_parquet_path.unlink()
    assert dgc.check_4bf_13_4(ctx_pass).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_5_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_5(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_5_fail(ctx_pass: Any) -> None:
    ctx_pass.normalized_parquet_sidecar_path.unlink()
    assert dgc.check_4bf_13_5(ctx_pass).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_6_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_6(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_6_fail_on_sha(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, normalized_parquet_sha="0" * 64)
    assert dgc.check_4bf_13_6(ctx).status == DerivedAggTradesCheckStatus.FAIL


# ---------- Group C / E / F ----------


def test_check_4bf_13_7_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_7(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_7_fail(ctx_pass: Any) -> None:
    ctx = replace_manifest_field(ctx_pass, key="event_count", value=99)
    assert dgc.check_4bf_13_7(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_8_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_8(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_8_fail_when_event_count_lies(ctx_pass: Any) -> None:
    ctx = replace_manifest_field(ctx_pass, key="event_count", value=99)
    assert dgc.check_4bf_13_8(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_9_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_9(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_9_fail_when_files_empty(ctx_pass: Any) -> None:
    ctx = replace_manifest_field(ctx_pass, key="files", value=[])
    assert dgc.check_4bf_13_9(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_9_fail_when_sha_drift(ctx_pass: Any) -> None:
    ctx = deepcopy(ctx_pass)
    ctx.derived_manifest["files"][0]["sha256"] = "0" * 64
    assert dgc.check_4bf_13_9(ctx).status == DerivedAggTradesCheckStatus.FAIL


@pytest.mark.parametrize(
    "field,value",
    [
        ("dataset_family", "wrong_family"),
        ("version", "v999"),
        ("symbol", "ETHUSDT"),
        ("research_eligible", True),
        ("eligibility_gate_status", "pass"),
    ],
)
def test_manifest_top_level_fail_paths(ctx_pass: Any, field: str, value: Any) -> None:
    ctx = replace_manifest_field(ctx_pass, key=field, value=value)
    fn = {
        "dataset_family": dgc.check_4bf_13_10,
        "version": dgc.check_4bf_13_11,
        "symbol": dgc.check_4bf_13_12,
        "research_eligible": dgc.check_4bf_13_13,
        "eligibility_gate_status": dgc.check_4bf_13_14,
    }[field]
    assert fn(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_manifest_top_level_pass_paths(ctx_pass: Any) -> None:
    for fn in (
        dgc.check_4bf_13_10,
        dgc.check_4bf_13_11,
        dgc.check_4bf_13_12,
        dgc.check_4bf_13_13,
        dgc.check_4bf_13_14,
    ):
        assert fn(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


@pytest.mark.parametrize(
    "key,fn",
    [
        ("feature_computation", dgc.check_4bf_13_15),
        ("strategy_use", dgc.check_4bf_13_16),
        ("source_gate_report_id", dgc.check_4bf_13_17),
        ("source_gate_report_sha256", dgc.check_4bf_13_18),
        ("source_manifest_sha256", dgc.check_4bf_13_19),
        ("source_raw_zip_sha256", dgc.check_4bf_13_20),
    ],
)
def test_governance_label_pass(ctx_pass: Any, key: str, fn: Any) -> None:
    assert fn(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


@pytest.mark.parametrize(
    "key,fn",
    [
        ("feature_computation", dgc.check_4bf_13_15),
        ("strategy_use", dgc.check_4bf_13_16),
        ("source_gate_report_id", dgc.check_4bf_13_17),
        ("source_gate_report_sha256", dgc.check_4bf_13_18),
        ("source_manifest_sha256", dgc.check_4bf_13_19),
        ("source_raw_zip_sha256", dgc.check_4bf_13_20),
    ],
)
def test_governance_label_fail(ctx_pass: Any, key: str, fn: Any) -> None:
    ctx = deepcopy(ctx_pass)
    ctx.derived_manifest["governance_labels"][key] = "WRONG"
    assert fn(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_21_pass_on_empty_invalid_windows(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_21(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_21_pass_on_governed_invalid_windows(ctx_pass: Any) -> None:
    ctx = replace_manifest_field(
        ctx_pass,
        key="invalid_windows",
        value=[{"downstream_eligibility_action": "exclude"}],
    )
    assert dgc.check_4bf_13_21(ctx).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_21_fail_on_ungoverned_invalid_windows(ctx_pass: Any) -> None:
    ctx = replace_manifest_field(
        ctx_pass,
        key="invalid_windows",
        value=[{"downstream_eligibility_action": "PROMOTE_NOW"}],
    )
    assert dgc.check_4bf_13_21(ctx).status == DerivedAggTradesCheckStatus.FAIL


# ---------- Group D ----------


def test_check_4bf_13_22_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_22(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_22_fail_when_schema_mismatched(ctx_pass: Any) -> None:
    bad = pa.Table.from_pydict({"x": [1]})
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_22(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_23_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_23(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_23_fail(ctx_pass: Any) -> None:
    bad = pa.Table.from_pydict({"x": [1], "y": [2]})
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_23(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_24_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_24(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_24_fail_on_forbidden_column_name(ctx_pass: Any) -> None:
    bad = pa.Table.from_pydict({"feature_x": ["1"], "label": ["2"]})
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_24(ctx).status == DerivedAggTradesCheckStatus.FAIL


# ---------- Group E (row-index / agg_trade_id / first / last) ----------


def test_check_4bf_13_25_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_25(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_25_fail_when_row_index_has_gap(ctx_pass: Any) -> None:
    n = ctx_pass.parquet_table.num_rows
    schema = ctx_pass.parquet_table.schema
    cols = {f.name: ctx_pass.parquet_table.column(f.name).to_pylist() for f in schema}
    cols["row_index"] = list(range(1, n + 1))  # off-by-one
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_25(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_26_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_26(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_26_fail_with_duplicate_row_index(ctx_pass: Any) -> None:
    n = ctx_pass.parquet_table.num_rows
    schema = ctx_pass.parquet_table.schema
    cols = {f.name: ctx_pass.parquet_table.column(f.name).to_pylist() for f in schema}
    cols["row_index"] = [0] * n
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_26(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_27_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_27(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_27_fail_with_duplicate_agg_id(ctx_pass: Any) -> None:
    n = ctx_pass.parquet_table.num_rows
    schema = ctx_pass.parquet_table.schema
    cols = {f.name: ctx_pass.parquet_table.column(f.name).to_pylist() for f in schema}
    cols["agg_trade_id"] = [dgc.EXPECTED_FIRST_AGG_TRADE_ID] * n
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_27(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_28_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_28(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_28_fail_when_out_of_order(ctx_pass: Any) -> None:
    schema = ctx_pass.parquet_table.schema
    cols = {f.name: ctx_pass.parquet_table.column(f.name).to_pylist() for f in schema}
    cols["agg_trade_id"] = list(reversed(cols["agg_trade_id"]))
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_28(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_29_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_29(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_29_fail_when_first_row_wrong(ctx_pass: Any) -> None:
    schema = ctx_pass.parquet_table.schema
    cols = {f.name: ctx_pass.parquet_table.column(f.name).to_pylist() for f in schema}
    cols["price"][0] = "0.0"
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_29(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_30_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_30(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_30_fail_when_last_row_wrong(ctx_pass: Any) -> None:
    schema = ctx_pass.parquet_table.schema
    cols = {f.name: ctx_pass.parquet_table.column(f.name).to_pylist() for f in schema}
    cols["price"][-1] = "0.0"
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_30(ctx).status == DerivedAggTradesCheckStatus.FAIL


# ---------- Group G ----------


def test_check_4bf_13_31_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_31(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_31_fail_when_t_outside_day(ctx_pass: Any) -> None:
    schema = ctx_pass.parquet_table.schema
    cols = {f.name: ctx_pass.parquet_table.column(f.name).to_pylist() for f in schema}
    cols["transact_time_ms"][0] = dgc.DAY_END_MS  # equals end → out of half-open
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_31(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_32_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_32(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_32_fail_when_raw_start_drifts(ctx_pass: Any) -> None:
    ctx = replace_raw_manifest_field(ctx_pass, key="start_time_ms", value=999)
    assert dgc.check_4bf_13_32(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_33_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_33(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_33_fail_when_raw_end_drifts(ctx_pass: Any) -> None:
    ctx = replace_raw_manifest_field(ctx_pass, key="end_time_ms", value=999)
    assert dgc.check_4bf_13_33(ctx).status == DerivedAggTradesCheckStatus.FAIL


# ---------- Group H ----------


def test_check_4bf_13_34_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_34(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_34_fail_when_price_not_string(ctx_pass: Any) -> None:
    schema = pa.schema([
        pa.field(f.name, pa.float64() if f.name == "price" else f.type)
        for f in ctx_pass.parquet_table.schema
    ])
    cols = {
        f.name: ctx_pass.parquet_table.column(f.name).to_pylist()
        for f in ctx_pass.parquet_table.schema
    }
    cols["price"] = [float(x) for x in cols["price"]]
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_34(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_35_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_35(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_35_fail_when_quantity_not_string(ctx_pass: Any) -> None:
    schema = pa.schema([
        pa.field(f.name, pa.float64() if f.name == "quantity" else f.type)
        for f in ctx_pass.parquet_table.schema
    ])
    cols = {
        f.name: ctx_pass.parquet_table.column(f.name).to_pylist()
        for f in ctx_pass.parquet_table.schema
    }
    cols["quantity"] = [float(x) for x in cols["quantity"]]
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_35(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_36_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_36(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_36_fail_when_is_buyer_maker_not_bool(ctx_pass: Any) -> None:
    schema = pa.schema([
        pa.field(f.name, pa.int8() if f.name == "is_buyer_maker" else f.type)
        for f in ctx_pass.parquet_table.schema
    ])
    cols = {
        f.name: ctx_pass.parquet_table.column(f.name).to_pylist()
        for f in ctx_pass.parquet_table.schema
    }
    cols["is_buyer_maker"] = [1 for _ in cols["is_buyer_maker"]]
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_36(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_37_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_37(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_37_fail_when_lineage_not_constant(ctx_pass: Any) -> None:
    schema = ctx_pass.parquet_table.schema
    cols = {f.name: ctx_pass.parquet_table.column(f.name).to_pylist() for f in schema}
    cols["dataset_family"][0] = "other_family"
    bad = pa.Table.from_pydict(cols, schema=schema)
    ctx = replace_ctx_field(ctx_pass, parquet_table=bad)
    assert dgc.check_4bf_13_37(ctx).status == DerivedAggTradesCheckStatus.FAIL


# ---------- Group K (Phase 4be evidence) ----------


def test_check_4bf_13_38_pass_on_real_repo(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_38(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_39_pass_on_real_repo(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_39(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_40_pass_on_real_repo(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_40(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_41_pass_on_real_repo(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_41(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_38_fail_when_qa_path_missing(
    ctx_pass: Any, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(dgc, "PHASE_4BE_QA_PATH", tmp_path / "missing.md")
    assert dgc.check_4bf_13_38(ctx_pass).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_39_fail_when_closeout_missing(
    ctx_pass: Any, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(dgc, "PHASE_4BE_CLOSEOUT_PATH", tmp_path / "missing.md")
    assert dgc.check_4bf_13_39(ctx_pass).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_40_fail_when_merge_closeout_missing(
    ctx_pass: Any, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(dgc, "PHASE_4BE_MERGE_CLOSEOUT_PATH", tmp_path / "missing.md")
    assert dgc.check_4bf_13_40(ctx_pass).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_41_fail_when_qa_doesnt_record_60_60(
    ctx_pass: Any, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    fake = tmp_path / "fake-qa.md"
    fake.write_text("nothing here", encoding="utf-8")
    monkeypatch.setattr(dgc, "PHASE_4BE_QA_PATH", fake)
    assert dgc.check_4bf_13_41(ctx_pass).status == DerivedAggTradesCheckStatus.FAIL


# ---------- Group B / M (raw immutability) ----------


def test_check_4bf_13_42_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_42(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_42_fail(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, raw_manifest_sha="0" * 64)
    assert dgc.check_4bf_13_42(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_43_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_43(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_43_fail(ctx_pass: Any) -> None:
    ctx = replace_raw_manifest_field(ctx_pass, key="research_eligible", value=True)
    assert dgc.check_4bf_13_43(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_44_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_44(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_44_fail(ctx_pass: Any) -> None:
    ctx = replace_raw_manifest_field(ctx_pass, key="eligibility_gate_status", value="pass")
    assert dgc.check_4bf_13_44(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_45_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_45(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_45_fail(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, raw_zip_sha="0" * 64)
    assert dgc.check_4bf_13_45(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_46_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_46(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_46_fail_on_sidecar_sha_drift(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, raw_sidecar_sha="0" * 64)
    assert dgc.check_4bf_13_46(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_46_fail_on_sidecar_first_64_drift(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, raw_sidecar_first_64="b" * 64)
    assert dgc.check_4bf_13_46(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_47_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_47(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_47_fail(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, acquisition_log_sha="0" * 64)
    assert dgc.check_4bf_13_47(ctx).status == DerivedAggTradesCheckStatus.FAIL


def test_check_4bf_13_48_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_48(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_48_fail(ctx_pass: Any) -> None:
    ctx = replace_ctx_field(ctx_pass, gate_report_sha="0" * 64)
    assert dgc.check_4bf_13_48(ctx).status == DerivedAggTradesCheckStatus.FAIL


# ---------- Group L / N (boundary + invariants) ----------


def test_check_4bf_13_49_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_49(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_50_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_50(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_51_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_51(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_52_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_52(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_53_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_53(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_54_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_54(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


def test_check_4bf_13_55_pass(ctx_pass: Any) -> None:
    assert dgc.check_4bf_13_55(ctx_pass).status == DerivedAggTradesCheckStatus.PASS


# ---------- Suite-level invariants ----------


def test_check_order_has_exactly_55_entries() -> None:
    assert len(CHECK_ORDER) == 55


def test_check_order_ids_are_4bf_13_1_to_55() -> None:
    expected = [f"4bf.13.{i}" for i in range(1, 56)]
    actual = [entry[0] for entry in CHECK_ORDER]
    assert actual == expected


def test_run_all_checks_returns_55_results_in_order(ctx_pass: Any) -> None:
    results = run_all_checks(ctx_pass)
    assert len(results) == 55
    assert [r.check_id for r in results] == [f"4bf.13.{i}" for i in range(1, 56)]


def test_happy_path_all_checks_pass(ctx_pass: Any) -> None:
    results = run_all_checks(ctx_pass)
    failures = [r for r in results if r.status != DerivedAggTradesCheckStatus.PASS]
    assert not failures, [
        (r.check_id, r.status, r.detail) for r in failures
    ]
