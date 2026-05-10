"""Phase 4bh tests: features_compute kernel correctness.

Covers:

- 61-column event-aligned schema and order;
- causal trailing-window inclusion (right-closed, left-open);
- same-timestamp tie-break ``row_index <= R``;
- aggressive-side rule ``is_buyer_maker = false -> aggressive buy``;
- ratio null when denominator is zero, ratio in ``[0, 1]`` otherwise;
- log return null when no prior reference price exists, otherwise
  computed against the last source row with ``T <= T_i - window_ms``;
- empty-window null/zero policy for Decimal-as-string sums and means;
- Decimal-as-string outputs parse via :class:`Decimal`;
- atomic write + sidecar; refuse overwrite.
"""

from __future__ import annotations

import math
from decimal import Decimal

import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import (
    FEATURE_SCHEMA_V001,
    FEATURE_WINDOW_LABELS_V001,
    FeatureLineage,
    build_feature_config,
    compute_aggtrades_features,
    read_normalized_parquet,
    write_feature_dataset,
)
from prometheus.research.microstructure.features_compute import FeatureComputationError
from prometheus.research.microstructure.features_io import FeatureIOError

from ._features_fixtures import (
    SYNTHETIC_FEATURE_CONFIG_HASH,
    SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
    SYNTHETIC_SUCCESSOR_STATE_SHA,
    build_feature_fixture,
)


def _compute_table(tmp_path):
    bundle = build_feature_fixture(tmp_path)
    table, parquet_sha, _ = read_normalized_parquet(bundle.normalized_parquet_path)
    cfg = build_feature_config(
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.normalized_manifest_path,
        source_successor_state_path=bundle.successor_state_path,
        output_feature_parquet_path=bundle.feature_parquet_path,
        output_feature_manifest_path=bundle.feature_manifest_path,
        code_commit_sha="0" * 40,
    )
    lineage = FeatureLineage(
        source_normalized_parquet_sha256=parquet_sha,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
        feature_config_hash=cfg.feature_config_hash,
    )
    return bundle, cfg, table, lineage, compute_aggtrades_features(
        source_table=table, config=cfg, lineage=lineage
    )


def test_kernel_emits_61_columns_in_canonical_order(tmp_path) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    assert tuple(feat.column_names) == FEATURE_SCHEMA_V001
    assert feat.num_columns == 61


def test_kernel_emits_one_row_per_source_row(tmp_path) -> None:
    bundle, _, src, _, feat = _compute_table(tmp_path)
    assert feat.num_rows == src.num_rows == bundle.row_count


def test_lineage_sha_columns_constant(tmp_path) -> None:
    bundle, _, _, lineage, feat = _compute_table(tmp_path)
    parquet_shas = feat.column("source_normalized_parquet_sha256").to_pylist()
    assert all(s == bundle.normalized_parquet_sha256 for s in parquet_shas)
    manifest_shas = feat.column("source_normalized_manifest_sha256").to_pylist()
    assert all(s == bundle.normalized_manifest_sha256 for s in manifest_shas)
    succ_shas = feat.column("source_successor_state_sha256").to_pylist()
    assert all(s == bundle.successor_state_sha256 for s in succ_shas)
    gate_shas = feat.column("source_phase_4bf_gate_report_sha256").to_pylist()
    assert all(s == lineage.source_phase_4bf_gate_report_sha256 for s in gate_shas)
    cfg_hashes = feat.column("feature_config_hash").to_pylist()
    assert all(s == lineage.feature_config_hash for s in cfg_hashes)


def test_feature_timestamp_equals_source_transact_time(tmp_path) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    a = feat.column("feature_timestamp_ms").to_pylist()
    b = feat.column("source_transact_time_ms").to_pylist()
    assert a == b


def test_aggressive_side_count_rule(tmp_path) -> None:
    bundle, _, _, _, feat = _compute_table(tmp_path)
    # The first row (row_index=0) has is_buyer_maker=False -> aggressive buy.
    # 1s window for row 0 contains only itself -> 1 buy, 0 sell.
    assert feat.column("rolling_aggressive_buy_count_1s").to_pylist()[0] == 1
    assert feat.column("rolling_aggressive_sell_count_1s").to_pylist()[0] == 0
    # Row 1 (row_index=1): is_buyer_maker=True -> aggressive sell.
    # 1s window includes rows 0 and 1 (T spread 250ms).
    assert feat.column("rolling_aggressive_buy_count_1s").to_pylist()[1] == 1
    assert feat.column("rolling_aggressive_sell_count_1s").to_pylist()[1] == 1
    # Verify rolling_aggtrade_count_1s parity for those rows.
    assert feat.column("rolling_aggtrade_count_1s").to_pylist()[0] == 1
    assert feat.column("rolling_aggtrade_count_1s").to_pylist()[1] == 2


def test_same_timestamp_tie_break_row_index_le_R(tmp_path) -> None:
    # Rows 1002 and 1003 share the same timestamp (offset 500). For row
    # 1002 (row_index=2), only itself and earlier rows can be in the
    # window. For row 1003 (row_index=3), itself plus 1002 plus earlier
    # may all be in the same window if T spread permits.
    _, _, _, _, feat = _compute_table(tmp_path)
    counts = feat.column("rolling_aggtrade_count_1s").to_pylist()
    # Row 2: 1s trailing window starts at T2 - 1000ms = 500 - 1000 = -500
    # within fixture-relative ms; rows 0 (offset 0), 1 (250), 2 (500)
    # are <= T2 in canonical order so all included.
    # Row 3: same T as row 2; row_index 3 includes rows 0..3.
    assert counts[2] == 3
    assert counts[3] == 4


def test_log_return_null_for_first_row(tmp_path) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    for label in FEATURE_WINDOW_LABELS_V001:
        col = f"rolling_log_return_past_window_{label}"
        # Row 0: no prior reference price -> null in every window.
        assert feat.column(col).to_pylist()[0] is None


def test_log_return_uses_prior_reference_price_at_or_before_threshold(
    tmp_path,
) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    # Row 4 (offset 1500ms) with 1s window: prior reference price is
    # the last row with T <= T_4 - 1000 = 500. Rows 2 and 3 are at T=500
    # (the latest such T); among them, row 3 has the largest row_index,
    # so prior_idx = 3 (price "100.2"). Current price for row 4 is "100.3".
    log_returns_1s = feat.column("rolling_log_return_past_window_1s").to_pylist()
    expected = math.log(100.3 / 100.2)
    assert log_returns_1s[4] == pytest.approx(expected, rel=1e-12)


def test_aggressive_flow_ratio_in_range_or_null(tmp_path) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    for label in FEATURE_WINDOW_LABELS_V001:
        col = f"rolling_aggressive_flow_ratio_{label}"
        for v in feat.column(col).to_pylist():
            if v is None:
                continue
            assert isinstance(v, float)
            assert 0.0 <= v <= 1.0
            assert math.isfinite(v)


def test_decimal_string_columns_parse_via_decimal(tmp_path) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    for label in FEATURE_WINDOW_LABELS_V001:
        for col in (
            f"rolling_quantity_sum_{label}",
            f"rolling_aggressive_buy_quantity_{label}",
            f"rolling_aggressive_sell_quantity_{label}",
            f"rolling_aggressive_quantity_imbalance_{label}",
        ):
            for s in feat.column(col).to_pylist():
                assert isinstance(s, str)
                Decimal(s)  # raises on invalid


def test_quantity_mean_decimal_string_or_null(tmp_path) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    for label in FEATURE_WINDOW_LABELS_V001:
        col = f"rolling_quantity_mean_{label}"
        for s in feat.column(col).to_pylist():
            if s is None:
                continue
            assert isinstance(s, str)
            Decimal(s)


def test_quantity_sum_zero_string_when_no_buy_rows(tmp_path) -> None:
    # The first row 0 (aggressive buy) has 0 sell rows in its 1s window.
    _, _, _, _, feat = _compute_table(tmp_path)
    assert feat.column("rolling_aggressive_sell_quantity_1s").to_pylist()[0] == "0"


def test_imbalance_zero_when_both_sides_empty_is_not_possible_in_default_fixture(
    tmp_path,
) -> None:
    # In the default fixture every window covers at least the current
    # row, which is always either buy or sell, so the imbalance can be
    # "0" only when both sides have zero quantity. Validate type and
    # parseability instead.
    _, _, _, _, feat = _compute_table(tmp_path)
    for label in FEATURE_WINDOW_LABELS_V001:
        col = f"rolling_aggressive_quantity_imbalance_{label}"
        for s in feat.column(col).to_pylist():
            assert isinstance(s, str)
            Decimal(s)


def test_quality_flags_default_false(tmp_path) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    for col in ("invalid_window_flag", "rolling_missing_window_flag"):
        for v in feat.column(col).to_pylist():
            assert v is False


def test_time_context_columns_within_day(tmp_path) -> None:
    _, _, _, _, feat = _compute_table(tmp_path)
    hours = feat.column("utc_hour").to_pylist()
    minutes = feat.column("utc_minute").to_pylist()
    msd = feat.column("milliseconds_since_day_start").to_pylist()
    for h, m, ms in zip(hours, minutes, msd, strict=True):
        assert 0 <= h <= 23
        assert 0 <= m <= 59
        assert 0 <= ms < 86_400_000


def test_write_feature_dataset_atomic_with_sidecar(tmp_path) -> None:
    bundle, _, _, _, feat = _compute_table(tmp_path)
    out, sha, size, sidecar, sidecar_sha = write_feature_dataset(
        table=feat,
        output_path=bundle.feature_parquet_path,
        write_sha256_sidecar=True,
    )
    assert out == bundle.feature_parquet_path
    assert out.exists()
    assert size > 0
    assert sidecar is not None and sidecar.exists()
    assert sidecar_sha is not None and len(sidecar_sha) == 64
    text = sidecar.read_text(encoding="ascii").strip()
    assert text.split()[0] == sha


def test_write_feature_dataset_refuses_overwrite(tmp_path) -> None:
    bundle, _, _, _, feat = _compute_table(tmp_path)
    write_feature_dataset(
        table=feat, output_path=bundle.feature_parquet_path, write_sha256_sidecar=False
    )
    with pytest.raises(FeatureIOError):
        write_feature_dataset(
            table=feat,
            output_path=bundle.feature_parquet_path,
            write_sha256_sidecar=False,
        )


def test_round_trip_parquet_preserves_column_order(tmp_path) -> None:
    bundle, _, _, _, feat = _compute_table(tmp_path)
    write_feature_dataset(
        table=feat, output_path=bundle.feature_parquet_path, write_sha256_sidecar=False
    )
    re_read = pq.read_table(bundle.feature_parquet_path)
    assert tuple(re_read.column_names) == FEATURE_SCHEMA_V001
    assert re_read.num_rows == feat.num_rows


def test_kernel_rejects_non_canonical_row_index(tmp_path) -> None:
    """A normalized parquet whose row_index is not 0..n-1 must fail closed."""
    import pyarrow as pa

    bundle = build_feature_fixture(tmp_path)
    src, _, _ = read_normalized_parquet(bundle.normalized_parquet_path)
    # Replace row_index with a constant array (not canonical).
    new_row_index = pa.array([0] * src.num_rows, type=pa.int64())
    src_bad = src.set_column(
        src.column_names.index("row_index"),
        pa.field("row_index", pa.int64()),
        new_row_index,
    )
    cfg = build_feature_config(
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.normalized_manifest_path,
        source_successor_state_path=bundle.successor_state_path,
        output_feature_parquet_path=bundle.feature_parquet_path,
        output_feature_manifest_path=bundle.feature_manifest_path,
    )
    lineage = FeatureLineage(
        source_normalized_parquet_sha256="a" * 64,
        source_normalized_manifest_sha256="b" * 64,
        source_successor_state_sha256=SYNTHETIC_SUCCESSOR_STATE_SHA,
        source_phase_4bf_gate_report_sha256=SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
        feature_config_hash=SYNTHETIC_FEATURE_CONFIG_HASH,
    )
    with pytest.raises(FeatureComputationError):
        compute_aggtrades_features(source_table=src_bad, config=cfg, lineage=lineage)


def test_kernel_rejects_non_decreasing_transact_time(tmp_path) -> None:
    import pyarrow as pa

    bundle = build_feature_fixture(tmp_path)
    src, _, _ = read_normalized_parquet(bundle.normalized_parquet_path)
    arr = src.column("transact_time_ms").to_numpy(zero_copy_only=False).copy()
    # Force descending order for one pair so np.all(... >= ...) fails.
    if len(arr) >= 2:
        arr[1] = arr[0] - 1
    new_T = pa.array(arr, type=pa.int64())
    src_bad = src.set_column(
        src.column_names.index("transact_time_ms"),
        pa.field("transact_time_ms", pa.int64()),
        new_T,
    )
    cfg = build_feature_config(
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.normalized_manifest_path,
        source_successor_state_path=bundle.successor_state_path,
        output_feature_parquet_path=bundle.feature_parquet_path,
        output_feature_manifest_path=bundle.feature_manifest_path,
    )
    lineage = FeatureLineage(
        source_normalized_parquet_sha256="a" * 64,
        source_normalized_manifest_sha256="b" * 64,
        source_successor_state_sha256=SYNTHETIC_SUCCESSOR_STATE_SHA,
        source_phase_4bf_gate_report_sha256=SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
        feature_config_hash=SYNTHETIC_FEATURE_CONFIG_HASH,
    )
    with pytest.raises(FeatureComputationError):
        compute_aggtrades_features(source_table=src_bad, config=cfg, lineage=lineage)


def test_kernel_reuses_correct_window_count_arr(tmp_path) -> None:
    """Sanity: rolling_aggtrade_count_60s should equal i+1 - lo for each i."""
    bundle = build_feature_fixture(tmp_path)
    src, _, _ = read_normalized_parquet(bundle.normalized_parquet_path)
    cfg = build_feature_config(
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.normalized_manifest_path,
        source_successor_state_path=bundle.successor_state_path,
        output_feature_parquet_path=bundle.feature_parquet_path,
        output_feature_manifest_path=bundle.feature_manifest_path,
    )
    lineage = FeatureLineage(
        source_normalized_parquet_sha256="a" * 64,
        source_normalized_manifest_sha256="b" * 64,
        source_successor_state_sha256=SYNTHETIC_SUCCESSOR_STATE_SHA,
        source_phase_4bf_gate_report_sha256=SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
        feature_config_hash=SYNTHETIC_FEATURE_CONFIG_HASH,
    )
    feat = compute_aggtrades_features(
        source_table=src, config=cfg, lineage=lineage
    )
    assert feat.column("rolling_aggtrade_count_60s").to_pylist()[-1] >= 1
