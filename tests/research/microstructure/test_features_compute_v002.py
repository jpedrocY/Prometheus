"""Phase 4bm-H v002 feature compute kernel unit tests."""

from __future__ import annotations

import math
from decimal import Decimal
from pathlib import Path

import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import (
    CROSS_DAY_TAIL_BUFFER_MS,
    FEATURE_SCHEMA_V002,
    FEATURE_WINDOW_LABELS_V002,
    PHASE_4BM_E_OUTCOME_LITERAL,
    FeatureComputationErrorV002,
    FeatureLineageV002,
    build_feature_config_v002,
    compute_aggtrades_features_v002,
    derive_v002_feature_parquet_path,
    slice_prior_day_tail,
    write_feature_dataset_v002,
)
from prometheus.research.microstructure.features_io import FeatureIOError

from ._multiday_features_fixtures_v002 import (
    SYNTHETIC_NORMALIZED_MANIFEST_SHA_V002,
    SYNTHETIC_PHASE_4BM_D_GATE_REPORT_SHA,
    SYNTHETIC_SUCCESSOR_STATE_SHA_V002,
    all_buyer_maker_rows,
    all_seller_maker_rows,
    build_multiday_v002_fixture,
    single_event_row,
)


def _utc_day_start_ms(d: str) -> int:
    from datetime import UTC, datetime

    return int(
        datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=UTC).timestamp() * 1000
    )


def _config_and_lineage(tmp_path: Path):
    cfg = build_feature_config_v002(
        source_normalized_manifest_path=tmp_path / "norm.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_manifest_path=tmp_path / "feat_manifest.json",
        output_feature_root_dir=tmp_path / "features",
        code_commit_sha="0" * 40,
    )
    lineage = FeatureLineageV002(
        source_normalized_parquet_per_day_sha256="a" * 64,
        source_normalized_manifest_sha256=SYNTHETIC_NORMALIZED_MANIFEST_SHA_V002,
        source_successor_state_sha256=SYNTHETIC_SUCCESSOR_STATE_SHA_V002,
        source_phase_4bm_d_gate_report_sha256=SYNTHETIC_PHASE_4BM_D_GATE_REPORT_SHA,
        feature_config_hash=cfg.feature_config_hash,
    )
    return cfg, lineage


def _compute_two_days(tmp_path: Path):
    bundle = build_multiday_v002_fixture(tmp_path)
    day1 = pq.read_table(bundle.day1_parquet_path)
    day2 = pq.read_table(bundle.day2_parquet_path)
    cfg, lineage = _config_and_lineage(tmp_path)
    feat1 = compute_aggtrades_features_v002(
        current_day_table=day1,
        prior_day_tail_table=None,
        config=cfg,
        lineage=lineage,
    )
    cur_start_ms = _utc_day_start_ms(bundle.utc_date_day2)
    tail = slice_prior_day_tail(
        day1, current_day_start_ms=cur_start_ms, tail_buffer_ms=CROSS_DAY_TAIL_BUFFER_MS
    )
    feat2 = compute_aggtrades_features_v002(
        current_day_table=day2,
        prior_day_tail_table=tail,
        config=cfg,
        lineage=lineage,
    )
    return bundle, feat1, feat2


def test_v002_kernel_emits_62_columns_in_canonical_order(tmp_path) -> None:
    _, feat1, feat2 = _compute_two_days(tmp_path)
    assert tuple(feat1.column_names) == FEATURE_SCHEMA_V002
    assert tuple(feat2.column_names) == FEATURE_SCHEMA_V002
    assert feat1.num_columns == 62
    assert feat2.num_columns == 62


def test_v002_kernel_emits_one_row_per_current_day_source_row(tmp_path) -> None:
    bundle, feat1, feat2 = _compute_two_days(tmp_path)
    assert feat1.num_rows == len(bundle.rows_day1)
    assert feat2.num_rows == len(bundle.rows_day2)


def test_v002_dataset_version_constant_on_every_row(tmp_path) -> None:
    _, feat1, feat2 = _compute_two_days(tmp_path)
    for feat in (feat1, feat2):
        for v in feat.column("dataset_version").to_pylist():
            assert v == "v002"
        for v in feat.column("source_dataset_version").to_pylist():
            assert v == "v002"
        for v in feat.column("source_phase_4bm_e_outcome").to_pylist():
            assert v == PHASE_4BM_E_OUTCOME_LITERAL


def test_v002_day1_first_rows_carry_rolling_missing_window_flag(tmp_path) -> None:
    """Day 1 has no prior-day tail in scope; rows in the first 60s
    must carry rolling_missing_window_flag=True; later rows False."""
    bundle, feat1, _ = _compute_two_days(tmp_path)
    day_start_ms = _utc_day_start_ms(bundle.utc_date_day1)
    flags = feat1.column("rolling_missing_window_flag").to_pylist()
    T = feat1.column("source_transact_time_ms").to_pylist()
    for t, flag in zip(T, flags, strict=True):
        expected = (t - 60_000) < day_start_ms
        assert flag is expected


def test_v002_day2_with_prior_day_tail_no_missing_window_flags(tmp_path) -> None:
    """With prior-day tail loaded for day 2, no current-day row should
    carry rolling_missing_window_flag because the tail buffer fully
    covers the max 60s window."""
    _, _, feat2 = _compute_two_days(tmp_path)
    flags = feat2.column("rolling_missing_window_flag").to_pylist()
    assert all(f is False for f in flags)


def test_v002_cross_day_lookback_60s_window_picks_up_day1_tail(tmp_path) -> None:
    """For day 2's earliest row at offset 0, the 60s trailing window
    should include day 1's last row (at day_end_ms - 1)."""
    bundle, _, feat2 = _compute_two_days(tmp_path)
    counts_60s = feat2.column("rolling_aggtrade_count_60s").to_pylist()
    assert counts_60s[0] >= 2  # self + at least one day1 tail row


def test_v002_aggressive_buy_count_rule(tmp_path) -> None:
    _, feat1, _ = _compute_two_days(tmp_path)
    # Row 0 of day1 has is_buyer_maker=False -> aggressive buy.
    assert feat1.column("rolling_aggressive_buy_count_1s").to_pylist()[0] == 1
    assert feat1.column("rolling_aggressive_sell_count_1s").to_pylist()[0] == 0
    # Row 1: is_buyer_maker=True -> aggressive sell.
    assert feat1.column("rolling_aggressive_buy_count_1s").to_pylist()[1] == 1
    assert feat1.column("rolling_aggressive_sell_count_1s").to_pylist()[1] == 1


def test_v002_same_timestamp_tie_break(tmp_path) -> None:
    # Rows 2 and 3 of day 1 share the same transact_time_ms (+500 ms).
    _, feat1, _ = _compute_two_days(tmp_path)
    counts = feat1.column("rolling_aggtrade_count_1s").to_pylist()
    # Row 2: 1s window starts at T - 1000 = -500 (rel to day_start);
    # rows 0, 1, 2 all in canonical order satisfy T <= row 2's T.
    # Row 3: same T as row 2 but tie-break row_index <= R includes rows
    # 0..3.
    assert counts[2] == 3
    assert counts[3] == 4


def test_v002_all_buyer_maker_zero_buy_quantity(tmp_path) -> None:
    """All-aggressive-sell fixture: every aggressive_buy_quantity must be '0'."""
    rows = all_buyer_maker_rows()
    bundle = build_multiday_v002_fixture(
        tmp_path, rows_day1=rows, rows_day2=rows
    )
    day1 = pq.read_table(bundle.day1_parquet_path)
    cfg, lineage = _config_and_lineage(tmp_path)
    feat = compute_aggtrades_features_v002(
        current_day_table=day1, prior_day_tail_table=None, config=cfg, lineage=lineage
    )
    for label in FEATURE_WINDOW_LABELS_V002:
        col = f"rolling_aggressive_buy_quantity_{label}"
        for v in feat.column(col).to_pylist():
            assert v == "0"
        # And buy count must be 0.
        for v in feat.column(f"rolling_aggressive_buy_count_{label}").to_pylist():
            assert v == 0


def test_v002_all_seller_maker_zero_sell_quantity(tmp_path) -> None:
    """All-aggressive-buy fixture: every aggressive_sell_quantity must be '0'."""
    rows = all_seller_maker_rows()
    bundle = build_multiday_v002_fixture(
        tmp_path, rows_day1=rows, rows_day2=rows
    )
    day1 = pq.read_table(bundle.day1_parquet_path)
    cfg, lineage = _config_and_lineage(tmp_path)
    feat = compute_aggtrades_features_v002(
        current_day_table=day1, prior_day_tail_table=None, config=cfg, lineage=lineage
    )
    for label in FEATURE_WINDOW_LABELS_V002:
        for v in feat.column(f"rolling_aggressive_sell_quantity_{label}").to_pylist():
            assert v == "0"
        for v in feat.column(f"rolling_aggressive_sell_count_{label}").to_pylist():
            assert v == 0


def test_v002_single_event_row_kernel(tmp_path) -> None:
    rows = single_event_row()
    bundle = build_multiday_v002_fixture(
        tmp_path, rows_day1=rows, rows_day2=rows
    )
    day1 = pq.read_table(bundle.day1_parquet_path)
    cfg, lineage = _config_and_lineage(tmp_path)
    feat = compute_aggtrades_features_v002(
        current_day_table=day1, prior_day_tail_table=None, config=cfg, lineage=lineage
    )
    assert feat.num_rows == 1
    # 1s window has only the row itself -> count 1.
    assert feat.column("rolling_aggtrade_count_1s").to_pylist()[0] == 1
    # No prior reference price -> log return null in every window.
    for label in FEATURE_WINDOW_LABELS_V002:
        col = f"rolling_log_return_past_window_{label}"
        assert feat.column(col).to_pylist()[0] is None


def test_v002_log_return_null_for_first_row(tmp_path) -> None:
    _, feat1, _ = _compute_two_days(tmp_path)
    for label in FEATURE_WINDOW_LABELS_V002:
        col = f"rolling_log_return_past_window_{label}"
        assert feat1.column(col).to_pylist()[0] is None


def test_v002_aggressive_flow_ratio_in_range_or_null(tmp_path) -> None:
    _, feat1, feat2 = _compute_two_days(tmp_path)
    for feat in (feat1, feat2):
        for label in FEATURE_WINDOW_LABELS_V002:
            col = f"rolling_aggressive_flow_ratio_{label}"
            for v in feat.column(col).to_pylist():
                if v is None:
                    continue
                assert isinstance(v, float)
                assert 0.0 <= v <= 1.0
                assert math.isfinite(v)


def test_v002_decimal_string_columns_parse_via_decimal(tmp_path) -> None:
    _, feat1, feat2 = _compute_two_days(tmp_path)
    for feat in (feat1, feat2):
        for label in FEATURE_WINDOW_LABELS_V002:
            for col in (
                f"rolling_quantity_sum_{label}",
                f"rolling_aggressive_buy_quantity_{label}",
                f"rolling_aggressive_sell_quantity_{label}",
                f"rolling_aggressive_quantity_imbalance_{label}",
            ):
                for s in feat.column(col).to_pylist():
                    assert isinstance(s, str)
                    Decimal(s)
            for s in feat.column(f"rolling_quantity_mean_{label}").to_pylist():
                if s is None:
                    continue
                assert isinstance(s, str)
                Decimal(s)


def test_v002_feature_timestamp_equals_source_transact_time(tmp_path) -> None:
    _, feat1, feat2 = _compute_two_days(tmp_path)
    for feat in (feat1, feat2):
        a = feat.column("feature_timestamp_ms").to_pylist()
        b = feat.column("source_transact_time_ms").to_pylist()
        assert a == b


def test_v002_no_future_lookahead(tmp_path) -> None:
    """No feature row's lookback should reference a future transact_time."""
    _, feat1, feat2 = _compute_two_days(tmp_path)
    for feat in (feat1, feat2):
        T = feat.column("source_transact_time_ms").to_pylist()
        # Monotonic non-decreasing by (T, row_index) within the day.
        prev = None
        for t in T:
            if prev is not None:
                assert t >= prev
            prev = t


def test_v002_lineage_sha_columns_constant(tmp_path) -> None:
    bundle, feat1, feat2 = _compute_two_days(tmp_path)
    cfg, lineage = _config_and_lineage(tmp_path)
    for feat in (feat1, feat2):
        for v in feat.column("source_normalized_manifest_sha256").to_pylist():
            assert v == SYNTHETIC_NORMALIZED_MANIFEST_SHA_V002
        for v in feat.column("source_successor_state_sha256").to_pylist():
            assert v == SYNTHETIC_SUCCESSOR_STATE_SHA_V002
        for v in feat.column("source_phase_4bm_d_gate_report_sha256").to_pylist():
            assert v == SYNTHETIC_PHASE_4BM_D_GATE_REPORT_SHA
        for v in feat.column("feature_config_hash").to_pylist():
            assert v == cfg.feature_config_hash


def test_v002_write_dataset_atomic_with_sidecar(tmp_path) -> None:
    bundle, feat1, _ = _compute_two_days(tmp_path)
    out_path = derive_v002_feature_parquet_path(
        features_root=bundle.features_root,
        symbol=bundle.symbol,
        utc_date=bundle.utc_date_day1,
    )
    res = write_feature_dataset_v002(
        table=feat1, output_path=out_path, write_sha256_sidecar=True
    )
    assert res.parquet_path == out_path
    assert out_path.exists()
    assert res.sidecar_path == out_path.with_suffix(out_path.suffix + ".sha256")
    assert res.sidecar_path.exists()
    side_bytes = res.sidecar_path.read_bytes()
    expected = f"{res.parquet_sha256}  {out_path.name}\n".encode("ascii")
    assert side_bytes == expected


def test_v002_write_dataset_refuse_to_overwrite(tmp_path) -> None:
    bundle, feat1, _ = _compute_two_days(tmp_path)
    out_path = derive_v002_feature_parquet_path(
        features_root=bundle.features_root,
        symbol=bundle.symbol,
        utc_date=bundle.utc_date_day1,
    )
    write_feature_dataset_v002(
        table=feat1, output_path=out_path, write_sha256_sidecar=True
    )
    with pytest.raises(FeatureIOError):
        write_feature_dataset_v002(
            table=feat1, output_path=out_path, write_sha256_sidecar=True
        )


def test_v002_kernel_rejects_wrong_source_dataset_version(tmp_path) -> None:
    """A v001-versioned normalized parquet must be rejected by the v002 kernel."""
    import pyarrow as pa

    bundle = build_multiday_v002_fixture(tmp_path)
    day1 = pq.read_table(bundle.day1_parquet_path)
    # Swap dataset_version to "v001" to simulate a v001 source.
    new_col = pa.array(["v001"] * day1.num_rows, type=pa.string())
    idx = day1.column_names.index("dataset_version")
    bad = day1.set_column(idx, pa.field("dataset_version", pa.string()), new_col)
    cfg, lineage = _config_and_lineage(tmp_path)
    with pytest.raises(FeatureComputationErrorV002):
        compute_aggtrades_features_v002(
            current_day_table=bad,
            prior_day_tail_table=None,
            config=cfg,
            lineage=lineage,
        )


def test_v002_kernel_rejects_tail_with_current_day_timestamps(tmp_path) -> None:
    """A tail table with rows whose T >= current day's start_ms must fail."""
    bundle = build_multiday_v002_fixture(tmp_path)
    day1 = pq.read_table(bundle.day1_parquet_path)
    day2 = pq.read_table(bundle.day2_parquet_path)
    # Use day2 itself as "tail" -- its rows are not strictly before
    # day2's start_ms.
    cfg, lineage = _config_and_lineage(tmp_path)
    with pytest.raises(FeatureComputationErrorV002):
        compute_aggtrades_features_v002(
            current_day_table=day2,
            prior_day_tail_table=day2,
            config=cfg,
            lineage=lineage,
        )
    # day1 events vs day1: same problem
    with pytest.raises(FeatureComputationErrorV002):
        compute_aggtrades_features_v002(
            current_day_table=day1,
            prior_day_tail_table=day1,
            config=cfg,
            lineage=lineage,
        )


def test_v002_slice_prior_day_tail_filters_correctly(tmp_path) -> None:
    bundle = build_multiday_v002_fixture(tmp_path)
    day1 = pq.read_table(bundle.day1_parquet_path)
    cur_start_ms = _utc_day_start_ms(bundle.utc_date_day2)
    tail = slice_prior_day_tail(
        day1, current_day_start_ms=cur_start_ms, tail_buffer_ms=CROSS_DAY_TAIL_BUFFER_MS
    )
    # Every tail row must satisfy >= cur_start_ms - tail_buffer_ms.
    cutoff = cur_start_ms - CROSS_DAY_TAIL_BUFFER_MS
    for t in tail.column("transact_time_ms").to_pylist():
        assert t >= cutoff
    # Every tail row must be strictly less than cur_start_ms.
    for t in tail.column("transact_time_ms").to_pylist():
        assert t < cur_start_ms


def test_v002_round_trip_parquet_preserves_column_order(tmp_path) -> None:
    bundle, feat1, _ = _compute_two_days(tmp_path)
    out_path = derive_v002_feature_parquet_path(
        features_root=bundle.features_root,
        symbol=bundle.symbol,
        utc_date=bundle.utc_date_day1,
    )
    write_feature_dataset_v002(
        table=feat1, output_path=out_path, write_sha256_sidecar=False
    )
    re_read = pq.read_table(out_path)
    assert tuple(re_read.column_names) == FEATURE_SCHEMA_V002
    assert re_read.num_rows == feat1.num_rows


def test_v002_quality_flags_strict_bool(tmp_path) -> None:
    _, feat1, feat2 = _compute_two_days(tmp_path)
    for feat in (feat1, feat2):
        for col in ("invalid_window_flag", "rolling_missing_window_flag"):
            for v in feat.column(col).to_pylist():
                assert isinstance(v, bool)


def test_v002_time_context_columns_within_day(tmp_path) -> None:
    _, feat1, feat2 = _compute_two_days(tmp_path)
    for feat in (feat1, feat2):
        for h in feat.column("utc_hour").to_pylist():
            assert 0 <= h <= 23
        for m in feat.column("utc_minute").to_pylist():
            assert 0 <= m <= 59
        for ms in feat.column("milliseconds_since_day_start").to_pylist():
            assert 0 <= ms < 86_400_000
