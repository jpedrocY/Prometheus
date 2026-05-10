"""Phase 4bh tests: schema constants, FeatureComputationConfig, hash."""

from __future__ import annotations

import json

import pytest

from prometheus.research.microstructure import (
    DECIMAL_POLICY_V001,
    FEATURE_DATASET_FAMILY,
    FEATURE_DATASET_VERSION,
    FEATURE_NAMES_V001,
    FEATURE_SCHEMA_V001,
    FEATURE_SCHEMA_VERSION,
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS,
    INVALID_WINDOW_POLICY_V001,
    LINEAGE_COLUMNS_V001,
    NULL_POLICY_V001,
    PER_WINDOW_FEATURE_TEMPLATES,
    SOURCE_NORMALIZED_DATASET_FAMILY,
    SOURCE_NORMALIZED_DATASET_VERSION,
    FeatureComputationConfig,
    FeatureSchemaError,
    assert_no_forbidden_substrings,
    build_feature_config,
    compute_feature_config_hash,
)


def test_full_schema_has_61_columns_in_canonical_order() -> None:
    assert len(FEATURE_SCHEMA_V001) == 61
    # First 16 columns are lineage / identity / metadata in canonical order.
    assert FEATURE_SCHEMA_V001[:16] == LINEAGE_COLUMNS_V001
    # Last 45 columns are the feature / quality columns.
    assert FEATURE_SCHEMA_V001[16:] == FEATURE_NAMES_V001
    # No duplicate column names.
    assert len(set(FEATURE_SCHEMA_V001)) == 61


def test_feature_names_count_45_and_window_breakdown() -> None:
    assert len(FEATURE_NAMES_V001) == 45
    # 4 windows x 10 templates per window = 40 windowed columns.
    expected_windowed: list[str] = []
    for label in FEATURE_WINDOW_LABELS_V001:
        for tpl in PER_WINDOW_FEATURE_TEMPLATES:
            expected_windowed.append(tpl.format(w=label))
    assert FEATURE_NAMES_V001[:40] == tuple(expected_windowed)
    # Last 5 entries are time-context + quality.
    assert FEATURE_NAMES_V001[40:] == (
        "utc_hour",
        "utc_minute",
        "milliseconds_since_day_start",
        "invalid_window_flag",
        "rolling_missing_window_flag",
    )


def test_feature_windows_ms_locked_and_paired() -> None:
    assert FEATURE_WINDOWS_MS_V001 == (1000, 5000, 15000, 60000)
    assert FEATURE_WINDOW_LABELS_V001 == ("1s", "5s", "15s", "60s")
    assert len(FEATURE_WINDOWS_MS_V001) == len(FEATURE_WINDOW_LABELS_V001)


def test_lineage_columns_count_16_and_in_canonical_order() -> None:
    assert len(LINEAGE_COLUMNS_V001) == 16
    assert LINEAGE_COLUMNS_V001[0] == "dataset_family"
    assert LINEAGE_COLUMNS_V001[-1] == "feature_config_hash"
    # Spot-check: agg_trade_id, row_index, timestamps, hash trio.
    assert "agg_trade_id" in LINEAGE_COLUMNS_V001
    assert "row_index" in LINEAGE_COLUMNS_V001
    assert "feature_timestamp_ms" in LINEAGE_COLUMNS_V001
    assert "source_transact_time_ms" in LINEAGE_COLUMNS_V001
    assert "source_normalized_parquet_sha256" in LINEAGE_COLUMNS_V001
    assert "source_normalized_manifest_sha256" in LINEAGE_COLUMNS_V001
    assert "source_successor_state_sha256" in LINEAGE_COLUMNS_V001
    assert "source_phase_4bf_gate_report_sha256" in LINEAGE_COLUMNS_V001


def test_per_window_feature_templates_are_ten() -> None:
    assert len(PER_WINDOW_FEATURE_TEMPLATES) == 10
    # Required canonical names.
    for required in (
        "rolling_aggtrade_count_{w}",
        "rolling_quantity_sum_{w}",
        "rolling_quantity_mean_{w}",
        "rolling_aggressive_buy_quantity_{w}",
        "rolling_aggressive_sell_quantity_{w}",
        "rolling_aggressive_buy_count_{w}",
        "rolling_aggressive_sell_count_{w}",
        "rolling_aggressive_flow_ratio_{w}",
        "rolling_aggressive_quantity_imbalance_{w}",
        "rolling_log_return_past_window_{w}",
    ):
        assert required in PER_WINDOW_FEATURE_TEMPLATES


def test_forbidden_substring_set_has_26_entries() -> None:
    assert len(FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS) == 26
    for required in (
        "label",
        "target",
        "future",
        "signal",
        "entry",
        "exit",
        "pnl",
        "profit",
        "loss",
        "mfe",
        "mae",
        "r_multiple",
        "equity",
        "position",
        "alpha",
        "edge",
        "prediction",
        "model",
        "score",
        "decision",
        "strategy",
        "liquidation",
        "funding",
        "open_interest",
        "order_book",
        "mark_price",
    ):
        assert required in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS


def test_canonical_schema_passes_forbidden_detector() -> None:
    # The full schema must NOT contain any forbidden substring.
    assert_no_forbidden_substrings(FEATURE_SCHEMA_V001)


def test_forbidden_detector_flags_obvious_label_column() -> None:
    with pytest.raises(FeatureSchemaError):
        assert_no_forbidden_substrings(("label_demo",))


def test_forbidden_detector_flags_pnl_column() -> None:
    with pytest.raises(FeatureSchemaError):
        assert_no_forbidden_substrings(("rolling_pnl_proxy",))


def test_forbidden_detector_negative_case_passes() -> None:
    # Sanity check: a clearly safe column passes.
    assert_no_forbidden_substrings(("rolling_quantity_sum_1s",))


def test_decimal_policy_locked_v001() -> None:
    assert DECIMAL_POLICY_V001["raw_price_storage"] == "decimal_string"
    assert DECIMAL_POLICY_V001["raw_quantity_storage"] == "decimal_string"
    assert DECIMAL_POLICY_V001["ratio_storage"] == "float64_nullable"
    assert DECIMAL_POLICY_V001["log_return_storage"] == "float64_nullable"


def test_null_policy_locked_v001() -> None:
    assert NULL_POLICY_V001["rolling_aggressive_flow_ratio"] == (
        "null_when_zero_denominator"
    )
    assert NULL_POLICY_V001["rolling_log_return_past_window"] == (
        "null_when_no_prior_reference_or_zero_price"
    )
    assert NULL_POLICY_V001["no_imputation_across_invalid_windows"] is True
    assert NULL_POLICY_V001["no_nan_no_inf_for_floats"] is True


def test_invalid_window_policy_locked_v001() -> None:
    assert (
        INVALID_WINDOW_POLICY_V001["propagate_from_source_manifest"] is True
    )
    assert (
        INVALID_WINDOW_POLICY_V001["no_imputation_inside_invalid_windows"] is True
    )


def test_build_feature_config_locks_schema_fields(tmp_path) -> None:
    cfg = build_feature_config(
        source_normalized_parquet_path=tmp_path / "src.parquet",
        source_normalized_manifest_path=tmp_path / "src.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_parquet_path=tmp_path / "feat.parquet",
        output_feature_manifest_path=tmp_path / "feat.json",
        code_commit_sha="0" * 40,
    )
    assert cfg.dataset_family == FEATURE_DATASET_FAMILY
    assert cfg.dataset_version == FEATURE_DATASET_VERSION
    assert cfg.feature_schema_version == FEATURE_SCHEMA_VERSION
    assert cfg.windows_ms == FEATURE_WINDOWS_MS_V001
    assert cfg.feature_names == FEATURE_NAMES_V001
    assert cfg.timestamp_alignment == "event_aligned"
    assert cfg.causal_window_rule == "trailing_right_open_left"
    assert cfg.same_timestamp_tie_rule == "row_index_le_R"
    assert len(cfg.feature_config_hash) == 64
    # Verify hash is deterministic.
    cfg2 = build_feature_config(
        source_normalized_parquet_path=tmp_path / "src.parquet",
        source_normalized_manifest_path=tmp_path / "src.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_parquet_path=tmp_path / "feat.parquet",
        output_feature_manifest_path=tmp_path / "feat.json",
        code_commit_sha="0" * 40,
    )
    assert cfg.feature_config_hash == cfg2.feature_config_hash


def test_build_feature_config_changes_hash_on_path_change(tmp_path) -> None:
    cfg1 = build_feature_config(
        source_normalized_parquet_path=tmp_path / "a.parquet",
        source_normalized_manifest_path=tmp_path / "src.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_parquet_path=tmp_path / "feat.parquet",
        output_feature_manifest_path=tmp_path / "feat.json",
    )
    cfg2 = build_feature_config(
        source_normalized_parquet_path=tmp_path / "b.parquet",
        source_normalized_manifest_path=tmp_path / "src.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_parquet_path=tmp_path / "feat.parquet",
        output_feature_manifest_path=tmp_path / "feat.json",
    )
    assert cfg1.feature_config_hash != cfg2.feature_config_hash


def test_compute_feature_config_hash_uses_canonical_json() -> None:
    payload = {"b": 2, "a": 1}
    digest = compute_feature_config_hash(payload)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    import hashlib

    expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert digest == expected


def test_feature_computation_config_rejects_wrong_dataset_family(tmp_path) -> None:
    with pytest.raises(FeatureSchemaError):
        FeatureComputationConfig(
            dataset_family="wrong_family",
            dataset_version="v001",
            feature_schema_version="v001",
            source_normalized_parquet_path=str(tmp_path / "a"),
            source_normalized_manifest_path=str(tmp_path / "b"),
            source_successor_state_path=str(tmp_path / "c"),
            output_feature_parquet_path=str(tmp_path / "d"),
            output_feature_manifest_path=str(tmp_path / "e"),
            windows_ms=FEATURE_WINDOWS_MS_V001,
            feature_names=FEATURE_NAMES_V001,
            timestamp_alignment="event_aligned",
            causal_window_rule="trailing_right_open_left",
            same_timestamp_tie_rule="row_index_le_R",
            code_commit_sha="unknown",
        )


def test_feature_computation_config_rejects_wrong_window_set(tmp_path) -> None:
    with pytest.raises(FeatureSchemaError):
        FeatureComputationConfig(
            dataset_family=FEATURE_DATASET_FAMILY,
            dataset_version=FEATURE_DATASET_VERSION,
            feature_schema_version=FEATURE_SCHEMA_VERSION,
            source_normalized_parquet_path=str(tmp_path / "a"),
            source_normalized_manifest_path=str(tmp_path / "b"),
            source_successor_state_path=str(tmp_path / "c"),
            output_feature_parquet_path=str(tmp_path / "d"),
            output_feature_manifest_path=str(tmp_path / "e"),
            windows_ms=(1000, 5000),  # too few windows
            feature_names=FEATURE_NAMES_V001,
            timestamp_alignment="event_aligned",
            causal_window_rule="trailing_right_open_left",
            same_timestamp_tie_rule="row_index_le_R",
            code_commit_sha="unknown",
        )


def test_feature_computation_config_rejects_wrong_causal_rule(tmp_path) -> None:
    with pytest.raises(FeatureSchemaError):
        FeatureComputationConfig(
            dataset_family=FEATURE_DATASET_FAMILY,
            dataset_version=FEATURE_DATASET_VERSION,
            feature_schema_version=FEATURE_SCHEMA_VERSION,
            source_normalized_parquet_path=str(tmp_path / "a"),
            source_normalized_manifest_path=str(tmp_path / "b"),
            source_successor_state_path=str(tmp_path / "c"),
            output_feature_parquet_path=str(tmp_path / "d"),
            output_feature_manifest_path=str(tmp_path / "e"),
            windows_ms=FEATURE_WINDOWS_MS_V001,
            feature_names=FEATURE_NAMES_V001,
            timestamp_alignment="event_aligned",
            causal_window_rule="bogus_rule",
            same_timestamp_tie_rule="row_index_le_R",
            code_commit_sha="unknown",
        )


def test_feature_computation_config_rejects_wrong_tie_rule(tmp_path) -> None:
    with pytest.raises(FeatureSchemaError):
        FeatureComputationConfig(
            dataset_family=FEATURE_DATASET_FAMILY,
            dataset_version=FEATURE_DATASET_VERSION,
            feature_schema_version=FEATURE_SCHEMA_VERSION,
            source_normalized_parquet_path=str(tmp_path / "a"),
            source_normalized_manifest_path=str(tmp_path / "b"),
            source_successor_state_path=str(tmp_path / "c"),
            output_feature_parquet_path=str(tmp_path / "d"),
            output_feature_manifest_path=str(tmp_path / "e"),
            windows_ms=FEATURE_WINDOWS_MS_V001,
            feature_names=FEATURE_NAMES_V001,
            timestamp_alignment="event_aligned",
            causal_window_rule="trailing_right_open_left",
            same_timestamp_tie_rule="bogus_tie",
            code_commit_sha="unknown",
        )


def test_feature_computation_config_rejects_bad_commit_sha(tmp_path) -> None:
    with pytest.raises(FeatureSchemaError):
        FeatureComputationConfig(
            dataset_family=FEATURE_DATASET_FAMILY,
            dataset_version=FEATURE_DATASET_VERSION,
            feature_schema_version=FEATURE_SCHEMA_VERSION,
            source_normalized_parquet_path=str(tmp_path / "a"),
            source_normalized_manifest_path=str(tmp_path / "b"),
            source_successor_state_path=str(tmp_path / "c"),
            output_feature_parquet_path=str(tmp_path / "d"),
            output_feature_manifest_path=str(tmp_path / "e"),
            windows_ms=FEATURE_WINDOWS_MS_V001,
            feature_names=FEATURE_NAMES_V001,
            timestamp_alignment="event_aligned",
            causal_window_rule="trailing_right_open_left",
            same_timestamp_tie_rule="row_index_le_R",
            code_commit_sha="not_a_sha",
        )


def test_source_dataset_constants_pin_normalized_family() -> None:
    assert SOURCE_NORMALIZED_DATASET_FAMILY == "microstructure_normalized_aggtrades_v001"
    assert SOURCE_NORMALIZED_DATASET_VERSION == "v001"
