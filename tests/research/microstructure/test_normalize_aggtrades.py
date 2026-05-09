"""Phase 4bd tests for normalize_aggtrades orchestrator + row mapping."""

from __future__ import annotations

from pathlib import Path

import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure.normalize_aggtrades import (
    NORMALIZED_SCHEMA_V001,
    NormalizationLineage,
    NormalizationValidationError,
    NormalizeAggTradesInput,
    NormalizedAggTradeRow,
    assert_schema_equals_v001,
    iter_aggtrade_rows_from_csv,
    run_normalize_aggtrades,
)
from prometheus.research.microstructure.normalize_io import NormalizationIOError

from ._eligibility_fixtures import make_default_rows
from ._normalize_fixtures import (
    CITED_GATE_CODE_COMMIT_SHA,
    CITED_GATE_REPORT_ID,
    CITED_GATE_REPORT_SHA,
    build_normalize_fixture,
    synthetic_gate_report_with_sha,
)


def _valid_lineage() -> NormalizationLineage:
    return NormalizationLineage(
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        raw_zip_sha="f" * 64,
        raw_manifest_sha="a" * 64,
        gate_report_id=CITED_GATE_REPORT_ID,
        gate_report_sha=CITED_GATE_REPORT_SHA,
    )


def _valid_row(**overrides) -> dict:
    base: dict = dict(
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v001",
        source_dataset_family="microstructure_raw_aggtrades_v001",
        source_dataset_version="v001",
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        agg_trade_id=1_000_000,
        price="100000",
        quantity="0.001",
        first_trade_id=10_000_000,
        last_trade_id=10_000_001,
        transact_time_ms=1736899201000,  # 2025-01-15 00:00:01 UTC
        is_buyer_maker=True,
        source_file_sha256="f" * 64,
        source_manifest_sha256="a" * 64,
        source_gate_report_id=CITED_GATE_REPORT_ID,
        source_gate_report_sha256=CITED_GATE_REPORT_SHA,
        row_index=0,
        normalization_schema_version="v001",
    )
    base.update(overrides)
    return base


def test_schema_constant_is_19_columns() -> None:
    assert len(NORMALIZED_SCHEMA_V001) == 19


def test_normalized_row_constructs_with_canonical_field_set() -> None:
    row = NormalizedAggTradeRow(**_valid_row())
    actual = tuple(row.__dataclass_fields__)
    assert actual == NORMALIZED_SCHEMA_V001


def test_normalized_row_rejects_float_price() -> None:
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(price=100000.0))  # type: ignore[arg-type]


def test_normalized_row_rejects_decimal_with_trailing_letter() -> None:
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(price="100000a"))


def test_normalized_row_rejects_zero_price() -> None:
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(price="0"))


def test_normalized_row_rejects_lowercase_symbol() -> None:
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(symbol="btcusdt"))


def test_normalized_row_rejects_bad_utc_date() -> None:
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(utc_date="2025/01/15"))


def test_normalized_row_rejects_T_outside_day() -> None:
    # 2025-01-16 00:00:00 UTC is past the half-open day for 2025-01-15.
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(transact_time_ms=1736985600001))


def test_normalized_row_rejects_negative_row_index() -> None:
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(row_index=-1))


def test_normalized_row_rejects_bool_in_int_field() -> None:
    # Python treats bool as int subclass; constructor must reject explicitly.
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(agg_trade_id=True))  # type: ignore[arg-type]


def test_normalized_row_rejects_bad_sha() -> None:
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(source_file_sha256="abc"))


def test_normalized_row_rejects_dataset_family_mismatch() -> None:
    with pytest.raises(NormalizationValidationError):
        NormalizedAggTradeRow(**_valid_row(dataset_family="something_else"))


def test_assert_schema_equals_v001_passes() -> None:
    assert_schema_equals_v001(NORMALIZED_SCHEMA_V001)


def test_assert_schema_equals_v001_rejects_extra_field() -> None:
    bad = NORMALIZED_SCHEMA_V001 + ("forbidden_feature",)
    with pytest.raises(NormalizationValidationError):
        assert_schema_equals_v001(bad)


def test_iter_aggtrade_rows_from_csv_with_header() -> None:
    rows = make_default_rows(n=3)
    csv = "agg_trade_id,price,quantity,first_trade_id,last_trade_id,transact_time,is_buyer_maker\n"
    csv += "\n".join(
        f"{r.a},{r.p},{r.q},{r.f},{r.l},{r.T},{'true' if r.m else 'false'}"
        for r in rows
    )
    payloads = iter_aggtrade_rows_from_csv(csv)
    assert len(payloads) == 3
    assert payloads[0].aggregate_trade_id == rows[0].a


def test_iter_aggtrade_rows_from_csv_headerless() -> None:
    rows = make_default_rows(n=2)
    csv = "\n".join(
        f"{r.a},{r.p},{r.q},{r.f},{r.l},{r.T},{'true' if r.m else 'false'}"
        for r in rows
    )
    payloads = iter_aggtrade_rows_from_csv(csv)
    assert len(payloads) == 2


def test_input_rejects_manifest_outside_manifests_namespace(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    bad_manifest = bundle.eligibility_bundle.raw_zip_path
    with pytest.raises(NormalizationIOError):
        NormalizeAggTradesInput(
            manifest_path=bad_manifest,
            output_root=bundle.output_root,
            code_commit_sha="0" * 40,
            cited_gate_report_id=CITED_GATE_REPORT_ID,
            cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
        )


def test_input_rejects_output_root_outside_microstructure(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    with pytest.raises(NormalizationIOError):
        NormalizeAggTradesInput(
            manifest_path=bundle.eligibility_bundle.manifest_path,
            output_root=tmp_path / "elsewhere",
            code_commit_sha="0" * 40,
            cited_gate_report_id=CITED_GATE_REPORT_ID,
            cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
        )


def test_input_rejects_bad_code_commit_sha(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    with pytest.raises(NormalizationIOError):
        NormalizeAggTradesInput(
            manifest_path=bundle.eligibility_bundle.manifest_path,
            output_root=bundle.output_root,
            code_commit_sha="not-a-sha",
            cited_gate_report_id=CITED_GATE_REPORT_ID,
            cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
        )


def test_input_accepts_unknown_for_offline_tests(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path)
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
    )
    assert inp.code_commit_sha == "unknown"


def test_run_normalize_aggtrades_happy_path(tmp_path: Path) -> None:
    # Use synthetic gate report whose SHA we recompute and cite verbatim.
    gate_report_path, recomputed = synthetic_gate_report_with_sha(tmp_path)
    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=recomputed,
        cited_gate_report_path=gate_report_path,
        cited_gate_code_commit_sha=CITED_GATE_CODE_COMMIT_SHA,
    )
    result = run_normalize_aggtrades(inp)
    assert result.research_eligible_after is False
    assert result.no_successor_authorization is True
    assert result.event_count == 8  # default fixture row count
    assert result.file_count == 1
    assert len(result.checks) == 27
    assert result.output_path is not None
    assert result.output_path.exists()
    assert result.output_sha256 is not None
    assert result.derived_manifest_path is not None
    assert result.derived_manifest_path.exists()


def test_run_normalize_aggtrades_writes_correct_schema(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
    )
    result = run_normalize_aggtrades(inp)
    assert result.output_path is not None
    table = pq.read_table(result.output_path)
    assert tuple(table.schema.names) == NORMALIZED_SCHEMA_V001


def test_run_normalize_aggtrades_refuses_overwrite(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
    )
    run_normalize_aggtrades(inp)
    with pytest.raises(NormalizationIOError):
        run_normalize_aggtrades(inp)


def test_run_normalize_aggtrades_preserves_raw_artefact_hashes(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    raw_zip = bundle.eligibility_bundle.raw_zip_path
    raw_zip_bytes_before = raw_zip.read_bytes()
    manifest = bundle.eligibility_bundle.manifest_path
    manifest_bytes_before = manifest.read_bytes()
    inp = NormalizeAggTradesInput(
        manifest_path=manifest,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
    )
    run_normalize_aggtrades(inp)
    assert raw_zip.read_bytes() == raw_zip_bytes_before
    assert manifest.read_bytes() == manifest_bytes_before


def test_run_normalize_aggtrades_local_report_sha_mismatch_aborts(
    tmp_path: Path,
) -> None:
    gate_report_path, recomputed = synthetic_gate_report_with_sha(tmp_path)
    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    # Cite a different SHA than the local file's actual SHA.
    cited_wrong_sha = "0" * 64
    assert cited_wrong_sha != recomputed
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=cited_wrong_sha,
        cited_gate_report_path=gate_report_path,
    )
    with pytest.raises(NormalizationValidationError):
        run_normalize_aggtrades(inp)
