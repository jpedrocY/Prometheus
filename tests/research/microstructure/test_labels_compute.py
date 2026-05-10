"""Phase 4bj-C label compute kernel tests (synthetic fixtures only)."""

from __future__ import annotations

import math
from decimal import Decimal
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure.labels_compute import (
    LabelComputationError,
    LabelLineage,
    compute_aggtrade_labels_v001,
    write_label_dataset_v001,
)
from prometheus.research.microstructure.labels_schema import (
    LABEL_HORIZON_MS_V001,
    LABEL_HORIZONS_V001,
    LABEL_SCHEMA_V001,
)

from ._labels_fixtures import build_feature_table, build_normalized_table


@pytest.fixture()
def standard_lineage() -> LabelLineage:
    return LabelLineage(
        source_feature_manifest_sha256="0" * 64,
        source_feature_parquet_sha256="1" * 64,
        source_feature_successor_state_sha256="2" * 64,
        source_phase_4bi_b_gate_report_sha256="3" * 64,
        source_normalized_parquet_sha256="4" * 64,
        label_config_hash="5" * 64,
    )


def test_simple_two_row_table_has_canonical_schema(
    standard_lineage: LabelLineage,
) -> None:
    norm = build_normalized_table(
        transact_time_ms=[1_000, 2_000],
        prices=["100", "200"],
    )
    feat = build_feature_table(normalized=norm)
    table, summary = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    assert tuple(table.column_names) == LABEL_SCHEMA_V001
    assert table.num_rows == 2
    assert summary.row_count == 2


def test_anchor_alignment_per_row(standard_lineage: LabelLineage) -> None:
    norm = build_normalized_table(
        transact_time_ms=[1_000, 5_000, 10_000, 20_000],
        prices=["100", "110", "120", "130"],
    )
    feat = build_feature_table(normalized=norm)
    table, _summary = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    # row_index parity
    assert table.column("row_index").to_pylist() == [0, 1, 2, 3]
    assert table.column("agg_trade_id").to_pylist() == norm.column(
        "agg_trade_id"
    ).to_pylist()
    assert table.column("feature_timestamp_ms").to_pylist() == [
        1_000,
        5_000,
        10_000,
        20_000,
    ]


def test_right_edge_horizon_censoring(standard_lineage: LabelLineage) -> None:
    # Final transact_time_ms = 4_000; for 1s horizon (target 5_000) all rows
    # are censored except those whose target <= 4_000.
    norm = build_normalized_table(
        transact_time_ms=[1_000, 2_500, 3_500, 4_000],
        prices=["100", "100", "100", "100"],
    )
    feat = build_feature_table(normalized=norm)
    table, summary = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    # Final T = 4_000. For 1s horizon (target = T+1000):
    # row 0: target=2_000 <= 4_000, NOT censored
    # row 1: target=3_500 <= 4_000, NOT censored
    # row 2: target=4_500 > 4_000, censored
    # row 3: target=5_000 > 4_000, censored
    cens_1s = table.column("horizon_censored_flag_1s").to_pylist()
    assert cens_1s == [False, False, True, True]
    # For 60s horizon (target = T+60_000), all are censored.
    cens_60s = table.column("horizon_censored_flag_60s").to_pylist()
    assert cens_60s == [True, True, True, True]
    # label_any_censored_flag = OR
    any_cens = table.column("label_any_censored_flag").to_pylist()
    assert any_cens == [True, True, True, True]
    # Censored support fields must be null.
    ret_60s = table.column("forward_log_return_60s").to_pylist()
    dir_60s = table.column("forward_direction_60s").to_pylist()
    ref_idx_60s = table.column("reference_row_index_60s").to_pylist()
    ref_ts_60s = table.column("reference_timestamp_ms_60s").to_pylist()
    assert ret_60s == [None, None, None, None]
    assert dir_60s == [None, None, None, None]
    assert ref_idx_60s == [None, None, None, None]
    assert ref_ts_60s == [None, None, None, None]

    assert summary.censored_per_horizon["1s"] == 2
    assert summary.censored_per_horizon["60s"] == 4


def test_future_reference_uses_largest_row_at_or_before_target(
    standard_lineage: LabelLineage,
) -> None:
    # Three trades at the same exact timestamp: 2_000, 2_000, 2_000.
    # Anchor row 0 (T=1_000), target_1s = 2_000. The reference must be the
    # *largest* row_index whose transact_time_ms <= 2_000 — i.e. row 3.
    norm = build_normalized_table(
        transact_time_ms=[1_000, 2_000, 2_000, 2_000, 60_000],
        prices=["100", "110", "120", "130", "140"],
    )
    feat = build_feature_table(normalized=norm)
    table, _summary = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    ref_idx_1s = table.column("reference_row_index_1s").to_pylist()
    ref_ts_1s = table.column("reference_timestamp_ms_1s").to_pylist()
    # row 0 anchor at T=1_000; target_1s=2_000; max row_index with T<=2_000 is 3.
    assert ref_idx_1s[0] == 3
    assert ref_ts_1s[0] == 2_000
    # forward_log_return_1s[0] = ln(130 / 100) > 0
    log_ret = table.column("forward_log_return_1s").to_pylist()[0]
    assert log_ret is not None
    expected = math.log(Decimal("130") / Decimal("100"))
    assert math.isclose(log_ret, expected, rel_tol=1e-9, abs_tol=0)
    # Direction strictly positive.
    assert table.column("forward_direction_1s").to_pylist()[0] == 1


def test_forward_direction_strict_sign(standard_lineage: LabelLineage) -> None:
    # Three rows: anchor row 0 at T=1000, reference row at T=2000
    # (>= anchor + 1000ms), final row well past the 60s horizon so
    # row 0's 1s horizon is NOT censored.
    norm = build_normalized_table(
        transact_time_ms=[1_000, 2_000, 80_000],
        prices=["100", "200", "200"],
    )
    feat = build_feature_table(normalized=norm)
    table, _ = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    # ln(200/100) > 0 -> +1
    assert table.column("forward_direction_1s").to_pylist()[0] == 1

    norm2 = build_normalized_table(
        transact_time_ms=[1_000, 2_000, 80_000],
        prices=["200", "100", "100"],
    )
    feat2 = build_feature_table(normalized=norm2)
    table2, _ = compute_aggtrade_labels_v001(
        feature_table=feat2,
        normalized_table=norm2,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    # ln(100/200) < 0 -> -1
    assert table2.column("forward_direction_1s").to_pylist()[0] == -1

    norm3 = build_normalized_table(
        transact_time_ms=[1_000, 2_000, 80_000],
        prices=["200", "200", "200"],
    )
    feat3 = build_feature_table(normalized=norm3)
    table3, _ = compute_aggtrade_labels_v001(
        feature_table=feat3,
        normalized_table=norm3,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    # ln(1) == 0 -> 0
    assert table3.column("forward_direction_1s").to_pylist()[0] == 0


def test_forward_log_return_uses_decimal_then_float64(
    standard_lineage: LabelLineage,
) -> None:
    # Slightly off-round prices to exercise Decimal-into-ratio path.
    # The third row at T=80_000 is past the 60s horizon so row 0's 1s
    # horizon is NOT censored (target=2000 <= 80_000).
    norm = build_normalized_table(
        transact_time_ms=[1_000, 2_000, 80_000],
        prices=["100.12345", "100.54321", "100.54321"],
    )
    feat = build_feature_table(normalized=norm)
    table, _ = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    log_ret = table.column("forward_log_return_1s").to_pylist()[0]
    expected = math.log(Decimal("100.54321") / Decimal("100.12345"))
    assert log_ret is not None
    assert math.isfinite(log_ret)
    assert math.isclose(log_ret, expected, rel_tol=1e-12, abs_tol=0)


def test_invalid_anchor_price_sets_flag_and_nulls_returns(
    standard_lineage: LabelLineage,
) -> None:
    norm = build_normalized_table(
        transact_time_ms=[1_000, 1_500],
        prices=["0", "100"],
    )
    feat = build_feature_table(normalized=norm)
    table, summary = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    # Row 0 has anchor price 0 -> invalid.
    flags = table.column("label_invalid_price_flag").to_pylist()
    assert flags[0] is True
    # forward_log_return_* for row 0 must be null.
    for label in LABEL_HORIZONS_V001:
        assert table.column(f"forward_log_return_{label}").to_pylist()[0] is None
        assert table.column(f"forward_direction_{label}").to_pylist()[0] is None
    assert summary.invalid_price_row_count >= 1


def test_label_any_censored_flag_or_semantics(
    standard_lineage: LabelLineage,
) -> None:
    # Two rows, second row anchor near end, both censored at long horizons.
    norm = build_normalized_table(
        transact_time_ms=[1_000, 2_000],
        prices=["100", "100"],
    )
    feat = build_feature_table(normalized=norm)
    table, _ = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    any_cens = table.column("label_any_censored_flag").to_pylist()
    for i in range(len(any_cens)):
        observed = any(
            table.column(f"horizon_censored_flag_{label}").to_pylist()[i]
            for label in LABEL_HORIZONS_V001
        )
        assert any_cens[i] == observed


def test_no_nan_or_inf_in_outputs(standard_lineage: LabelLineage) -> None:
    norm = build_normalized_table(
        transact_time_ms=[1_000, 1_500, 70_000],
        prices=["100", "110", "120"],
    )
    feat = build_feature_table(normalized=norm)
    table, _ = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    for label in LABEL_HORIZONS_V001:
        for v in table.column(f"forward_log_return_{label}").to_pylist():
            if v is None:
                continue
            assert math.isfinite(v)


def test_row_alignment_mismatch_fails(standard_lineage: LabelLineage) -> None:
    norm = build_normalized_table(
        transact_time_ms=[1_000, 2_000],
        prices=["100", "110"],
    )
    feat = build_feature_table(normalized=norm)
    # Force a mismatch by rebuilding the feature table with shifted timestamps.
    shifted = pa.Table.from_pydict(
        {
            "row_index": feat.column("row_index"),
            "agg_trade_id": feat.column("agg_trade_id"),
            "feature_timestamp_ms": pa.array(
                [1_000, 3_000], type=pa.int64()
            ),
            "source_transact_time_ms": pa.array(
                [1_000, 3_000], type=pa.int64()
            ),
        },
        schema=feat.schema,
    )
    with pytest.raises(LabelComputationError):
        compute_aggtrade_labels_v001(
            feature_table=shifted,
            normalized_table=norm,
            symbol="BTCUSDT",
            utc_date="2025-01-15",
            lineage=standard_lineage,
        )


def test_write_label_dataset_v001_atomic(
    tmp_path: Path, standard_lineage: LabelLineage
) -> None:
    norm = build_normalized_table(
        transact_time_ms=[1_000, 1_500],
        prices=["100", "110"],
    )
    feat = build_feature_table(normalized=norm)
    table, _ = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=standard_lineage,
    )
    root = (
        tmp_path
        / "data"
        / "microstructure"
        / "labels"
        / "microstructure_labels_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
    )
    target = root / "BTCUSDT-labels-aggtrades-2025-01-15.parquet"
    out_path, sha, size, sidecar_path, sidecar_sha = write_label_dataset_v001(
        table=table, output_path=target, write_sha256_sidecar=True
    )
    assert out_path == target
    assert out_path.exists()
    assert sidecar_path is not None and sidecar_path.exists()
    assert sidecar_sha is not None
    # Re-read parquet and confirm schema parity.
    reread = pq.read_table(out_path)
    assert tuple(reread.column_names) == LABEL_SCHEMA_V001
    assert size == target.stat().st_size
    assert sha


def test_horizon_ms_values_locked(standard_lineage: LabelLineage) -> None:
    # Sanity: confirm horizon ms tuple is preserved at runtime.
    assert LABEL_HORIZON_MS_V001 == (1000, 5000, 15000, 60000)
