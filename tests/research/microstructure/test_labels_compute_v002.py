"""Phase 4bm-O v002 label compute kernel tests (synthetic fixtures only)."""

from __future__ import annotations

import math
from decimal import Decimal
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure.labels_compute_v002 import (
    LabelComputationErrorV002,
    LabelLineageV002,
    NormalizedDayRef,
    compute_aggtrade_labels_v002_for_day,
    load_normalized_day_ref,
    write_label_dataset_v002,
)
from prometheus.research.microstructure.labels_schema_v002 import (
    LABEL_HORIZON_MS_V002,
    LABEL_HORIZONS_V002,
    LABEL_SCHEMA_V002,
)

from ._labels_fixtures_v002 import (
    build_feature_table_v002,
    build_normalized_table_v002,
    write_temp_parquet,
)


@pytest.fixture()
def standard_lineage() -> LabelLineageV002:
    return LabelLineageV002(
        source_feature_manifest_sha256="0" * 64,
        source_feature_parquet_sha256="1" * 64,
        source_feature_successor_state_sha256="2" * 64,
        source_phase_4bm_j_gate_report_sha256="3" * 64,
        source_normalized_manifest_sha256="4" * 64,
        source_raw_manifest_sha256="5" * 64,
        label_config_hash="6" * 64,
    )


def _day_ref(
    *, normalized: pa.Table, utc_date: str = "2024-12-01"
) -> NormalizedDayRef:
    import numpy as np

    return NormalizedDayRef(
        utc_date=utc_date,
        transact_time_ms=(
            normalized.column("transact_time_ms")
            .to_numpy(zero_copy_only=False)
            .astype(np.int64)
        ),
        prices_decimal=[Decimal(p) for p in normalized.column("price").to_pylist()],
        agg_trade_id=(
            normalized.column("agg_trade_id")
            .to_numpy(zero_copy_only=False)
            .astype(np.int64)
        ),
    )


# ---------------------------------------------------------------------------
# Canonical schema + simple smoke test
# ---------------------------------------------------------------------------


def test_simple_two_row_table_has_canonical_schema(
    standard_lineage: LabelLineageV002,
) -> None:
    # Need envelope_terminal large enough so all horizons are non-censored.
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000],
        prices=["100", "200"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, summary = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm, utc_date="2024-12-01"),
        next_day=None,
        envelope_terminal_unix_ms=2_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    assert tuple(table.column_names) == LABEL_SCHEMA_V002
    assert table.num_rows == 2
    assert summary.row_count == 2
    assert summary.utc_date == "2024-12-01"


# ---------------------------------------------------------------------------
# Anchor alignment / lineage propagation
# ---------------------------------------------------------------------------


def test_anchor_alignment_per_row(standard_lineage: LabelLineageV002) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 5_000, 10_000, 20_000, 80_000],
        prices=["100", "110", "120", "130", "140"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, _summary = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=80_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    assert table.column("row_index").to_pylist() == [0, 1, 2, 3, 4]
    assert table.column("agg_trade_id").to_pylist() == norm.column(
        "agg_trade_id"
    ).to_pylist()
    assert table.column("feature_timestamp_ms").to_pylist() == [
        1_000, 5_000, 10_000, 20_000, 80_000,
    ]
    # source_transact_time_ms parity.
    assert table.column("source_transact_time_ms").to_pylist() == [
        1_000, 5_000, 10_000, 20_000, 80_000,
    ]
    # Lineage / identity strings constant per row.
    assert set(table.column("dataset_family").to_pylist()) == {
        "microstructure_labels_aggtrades_v001"
    }
    assert set(table.column("dataset_version").to_pylist()) == {"v002"}
    assert set(table.column("label_schema_version").to_pylist()) == {"v001"}
    assert set(table.column("symbol").to_pylist()) == {"BTCUSDT"}
    assert set(table.column("utc_date").to_pylist()) == {"2024-12-01"}
    assert set(table.column("source_raw_manifest_sha256").to_pylist()) == {
        "5" * 64
    }
    assert set(table.column("label_config_hash").to_pylist()) == {"6" * 64}


# ---------------------------------------------------------------------------
# Envelope-terminal censoring
# ---------------------------------------------------------------------------


def test_envelope_terminal_censoring(standard_lineage: LabelLineageV002) -> None:
    # Final transact_time_ms = 4_000 in single-day mode; envelope_terminal = 4_000.
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_500, 3_500, 4_000],
        prices=["100", "100", "100", "100"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, summary = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=4_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    # For 1s horizon (target = T + 1000):
    # row 0: target=2_000 <= 4_000, NOT censored
    # row 1: target=3_500 <= 4_000, NOT censored
    # row 2: target=4_500 > 4_000, censored
    # row 3: target=5_000 > 4_000, censored
    cens_1s = table.column("horizon_censored_flag_1s").to_pylist()
    assert cens_1s == [False, False, True, True]
    # For 60s horizon (target = T + 60_000), all are censored.
    cens_60s = table.column("horizon_censored_flag_60s").to_pylist()
    assert cens_60s == [True, True, True, True]
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


def test_target_equal_envelope_terminal_is_valid_when_row_exists(
    standard_lineage: LabelLineageV002,
) -> None:
    # Anchor at T=1_000; horizon 1s -> target=2_000; row at 2_000 exists.
    # envelope_terminal = 2_000 (the last available row).
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000],
        prices=["100", "200"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, _summary = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=2_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    cens_1s = table.column("horizon_censored_flag_1s").to_pylist()
    # row 0 not censored; row 1's 1s-target is 3_000 > 2_000 => censored.
    assert cens_1s[0] is False
    assert cens_1s[1] is True
    assert table.column("forward_log_return_1s").to_pylist()[0] is not None


# ---------------------------------------------------------------------------
# Reference row selection: same-timestamp tie-break
# ---------------------------------------------------------------------------


def test_future_reference_uses_largest_row_at_or_before_target(
    standard_lineage: LabelLineageV002,
) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000, 2_000, 2_000, 80_000],
        prices=["100", "110", "120", "130", "140"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, _summary = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=80_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    ref_idx_1s = table.column("reference_row_index_1s").to_pylist()
    ref_ts_1s = table.column("reference_timestamp_ms_1s").to_pylist()
    # row 0 anchor at T=1_000; target_1s=2_000; max row_index with T<=2_000 is 3.
    assert ref_idx_1s[0] == 3
    assert ref_ts_1s[0] == 2_000
    log_ret = table.column("forward_log_return_1s").to_pylist()[0]
    assert log_ret is not None
    expected = math.log(Decimal("130") / Decimal("100"))
    assert math.isclose(log_ret, expected, rel_tol=1e-9, abs_tol=0)
    assert table.column("forward_direction_1s").to_pylist()[0] == 1


# ---------------------------------------------------------------------------
# Cross-day reference resolution (envelope-bounded)
# ---------------------------------------------------------------------------


def test_cross_day_reference_resolves_into_next_day(
    standard_lineage: LabelLineageV002,
) -> None:
    # Day 1: timestamps in the last 60s of a synthetic "day" (say day_end_ms = 100_000).
    # Day 2: starts at 100_500 ms.
    # Anchor in day 1 at 99_500 ms; 1s horizon -> target 100_500 which is in day 2.
    day1 = build_normalized_table_v002(
        transact_time_ms=[90_000, 99_500],
        prices=["100", "100"],
        utc_date="2024-12-01",
    )
    day2 = build_normalized_table_v002(
        transact_time_ms=[100_500, 101_000],
        prices=["200", "300"],
        agg_trade_id_offset=2_000_000,
        utc_date="2024-12-02",
    )
    feat = build_feature_table_v002(normalized=day1)
    table, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=day1, utc_date="2024-12-01"),
        next_day=_day_ref(normalized=day2, utc_date="2024-12-02"),
        envelope_terminal_unix_ms=101_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    # For anchor row 1 (T=99_500), 1s target = 100_500 -> reference is day 2's row 0.
    ref_idx_1s = table.column("reference_row_index_1s").to_pylist()
    ref_ts_1s = table.column("reference_timestamp_ms_1s").to_pylist()
    assert ref_idx_1s[1] == 0  # local row_index within day 2
    assert ref_ts_1s[1] == 100_500
    log_ret_1s = table.column("forward_log_return_1s").to_pylist()[1]
    assert log_ret_1s is not None
    expected = math.log(Decimal("200") / Decimal("100"))
    assert math.isclose(log_ret_1s, expected, rel_tol=1e-12, abs_tol=0)


def test_cross_day_reference_uses_largest_row_in_next_day(
    standard_lineage: LabelLineageV002,
) -> None:
    # Anchor T=99_500; horizon 5s -> target=104_500. Day 2 rows at 100_500 and
    # 101_000 are both <= target. Reference must be the LATER one (largest in
    # day 2).
    day1 = build_normalized_table_v002(
        transact_time_ms=[99_500],
        prices=["100"],
        utc_date="2024-12-01",
    )
    day2 = build_normalized_table_v002(
        transact_time_ms=[100_500, 101_000, 200_000],
        prices=["200", "300", "400"],
        agg_trade_id_offset=2_000_000,
        utc_date="2024-12-02",
    )
    feat = build_feature_table_v002(normalized=day1)
    table, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=day1, utc_date="2024-12-01"),
        next_day=_day_ref(normalized=day2, utc_date="2024-12-02"),
        envelope_terminal_unix_ms=200_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    # 5s horizon: target=104_500.
    # day 2: rows at 100_500 (idx 0), 101_000 (idx 1); both <= 104_500.
    # Latest idx in day 2 with ts <= target is 1.
    ref_idx_5s = table.column("reference_row_index_5s").to_pylist()
    ref_ts_5s = table.column("reference_timestamp_ms_5s").to_pylist()
    assert ref_idx_5s[0] == 1
    assert ref_ts_5s[0] == 101_000


def test_cross_day_target_beyond_envelope_censors(
    standard_lineage: LabelLineageV002,
) -> None:
    # Anchor at T=200_000; horizon 1s -> target=201_000 which equals envelope.
    # Use next_day; envelope_terminal=200_000 (anchor's own timestamp).
    day1 = build_normalized_table_v002(
        transact_time_ms=[200_000],
        prices=["100"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=day1)
    table, summary = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=day1, utc_date="2024-12-01"),
        next_day=None,
        envelope_terminal_unix_ms=200_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    # All horizons censored (target > 200_000 for every H).
    for h in LABEL_HORIZONS_V002:
        assert table.column(f"horizon_censored_flag_{h}").to_pylist() == [True]
        assert table.column(f"forward_log_return_{h}").to_pylist() == [None]
        assert table.column(f"forward_direction_{h}").to_pylist() == [None]
        assert summary.censored_per_horizon[h] == 1


# ---------------------------------------------------------------------------
# Direction / formula tests
# ---------------------------------------------------------------------------


def test_forward_direction_strict_sign(standard_lineage: LabelLineageV002) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000, 80_000],
        prices=["100", "200", "200"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=80_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    assert table.column("forward_direction_1s").to_pylist()[0] == 1

    norm2 = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000, 80_000],
        prices=["200", "100", "100"],
        utc_date="2024-12-01",
    )
    feat2 = build_feature_table_v002(normalized=norm2)
    table2, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat2,
        current_day=_day_ref(normalized=norm2),
        next_day=None,
        envelope_terminal_unix_ms=80_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    assert table2.column("forward_direction_1s").to_pylist()[0] == -1

    norm3 = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000, 80_000],
        prices=["200", "200", "200"],
        utc_date="2024-12-01",
    )
    feat3 = build_feature_table_v002(normalized=norm3)
    table3, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat3,
        current_day=_day_ref(normalized=norm3),
        next_day=None,
        envelope_terminal_unix_ms=80_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    # ln(1) == 0 -> 0
    assert table3.column("forward_direction_1s").to_pylist()[0] == 0


def test_forward_log_return_uses_decimal_then_float64(
    standard_lineage: LabelLineageV002,
) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000, 80_000],
        prices=["100.12345", "100.54321", "100.54321"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=80_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    log_ret = table.column("forward_log_return_1s").to_pylist()[0]
    expected = math.log(Decimal("100.54321") / Decimal("100.12345"))
    assert log_ret is not None
    assert math.isfinite(log_ret)
    assert math.isclose(log_ret, expected, rel_tol=1e-12, abs_tol=0)


# ---------------------------------------------------------------------------
# Invalid price
# ---------------------------------------------------------------------------


def test_invalid_anchor_price_sets_flag_and_nulls_returns(
    standard_lineage: LabelLineageV002,
) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 1_500],
        prices=["0", "100"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, summary = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=1_500,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    flags = table.column("label_invalid_price_flag").to_pylist()
    assert flags[0] is True
    for label in LABEL_HORIZONS_V002:
        assert table.column(f"forward_log_return_{label}").to_pylist()[0] is None
        assert table.column(f"forward_direction_{label}").to_pylist()[0] is None
    assert summary.invalid_price_row_count >= 1


# ---------------------------------------------------------------------------
# Row alignment + no NaN/inf
# ---------------------------------------------------------------------------


def test_no_nan_or_inf_in_outputs(standard_lineage: LabelLineageV002) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 1_500, 70_000],
        prices=["100", "110", "120"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=70_000,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    for label in LABEL_HORIZONS_V002:
        for v in table.column(f"forward_log_return_{label}").to_pylist():
            if v is None:
                continue
            assert math.isfinite(v)


def test_row_alignment_mismatch_fails(standard_lineage: LabelLineageV002) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000],
        prices=["100", "110"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    shifted = pa.Table.from_pydict(
        {
            "row_index": feat.column("row_index"),
            "agg_trade_id": feat.column("agg_trade_id"),
            "feature_timestamp_ms": pa.array([1_000, 3_000], type=pa.int64()),
            "source_transact_time_ms": pa.array([1_000, 3_000], type=pa.int64()),
        },
        schema=feat.schema,
    )
    with pytest.raises(LabelComputationErrorV002):
        compute_aggtrade_labels_v002_for_day(
            feature_table=shifted,
            current_day=_day_ref(normalized=norm),
            next_day=None,
            envelope_terminal_unix_ms=10_000,
            symbol="BTCUSDT",
            utc_date="2024-12-01",
            lineage=standard_lineage,
        )


def test_horizon_ms_values_locked() -> None:
    assert LABEL_HORIZON_MS_V002 == (1000, 5000, 15000, 60000)


# ---------------------------------------------------------------------------
# Write helpers + load_normalized_day_ref
# ---------------------------------------------------------------------------


def test_write_label_dataset_v002_atomic(
    tmp_path: Path, standard_lineage: LabelLineageV002
) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 1_500],
        prices=["100", "110"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=1_500,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    root = (
        tmp_path
        / "data"
        / "microstructure"
        / "labels"
        / "microstructure_labels_aggtrades_v001__v002"
        / "BTCUSDT"
        / "2024"
        / "12"
    )
    target = root / "BTCUSDT-labels-aggtrades-2024-12-01.parquet"
    out_path, sha, size, sidecar_path, sidecar_sha = write_label_dataset_v002(
        table=table, output_path=target, write_sha256_sidecar=True
    )
    assert out_path == target
    assert out_path.exists()
    assert sidecar_path is not None and sidecar_path.exists()
    assert sidecar_sha is not None
    reread = pq.read_table(out_path)
    assert tuple(reread.column_names) == LABEL_SCHEMA_V002
    assert size == target.stat().st_size
    assert sha


def test_write_label_dataset_v002_refuses_overwrite(
    tmp_path: Path, standard_lineage: LabelLineageV002
) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 1_500],
        prices=["100", "110"],
        utc_date="2024-12-01",
    )
    feat = build_feature_table_v002(normalized=norm)
    table, _ = compute_aggtrade_labels_v002_for_day(
        feature_table=feat,
        current_day=_day_ref(normalized=norm),
        next_day=None,
        envelope_terminal_unix_ms=1_500,
        symbol="BTCUSDT",
        utc_date="2024-12-01",
        lineage=standard_lineage,
    )
    root = (
        tmp_path
        / "data"
        / "microstructure"
        / "labels"
        / "microstructure_labels_aggtrades_v001__v002"
        / "BTCUSDT"
        / "2024"
        / "12"
    )
    target = root / "BTCUSDT-labels-aggtrades-2024-12-01.parquet"
    write_label_dataset_v002(
        table=table, output_path=target, write_sha256_sidecar=True
    )
    # Second write must fail closed.
    from prometheus.research.microstructure.labels_io import LabelIOError

    with pytest.raises(LabelIOError):
        write_label_dataset_v002(
            table=table, output_path=target, write_sha256_sidecar=True
        )


def test_load_normalized_day_ref_round_trip(tmp_path: Path) -> None:
    norm = build_normalized_table_v002(
        transact_time_ms=[1_000, 2_000, 3_000],
        prices=["100", "110", "120"],
        utc_date="2024-12-01",
    )
    p = tmp_path / "norm.parquet"
    write_temp_parquet(p, norm)
    ref = load_normalized_day_ref(parquet_path=p)
    assert ref.utc_date == "2024-12-01"
    assert len(ref.transact_time_ms) == 3
    assert int(ref.transact_time_ms[0]) == 1_000
    assert ref.prices_decimal[0] == Decimal("100")


def test_load_normalized_day_ref_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(LabelComputationErrorV002):
        load_normalized_day_ref(parquet_path=tmp_path / "does_not_exist.parquet")
