"""Phase 4bj-C label schema tests."""

from __future__ import annotations

from prometheus.research.microstructure.labels_schema import (
    FORBIDDEN_LABEL_COLUMN_SUBSTRINGS,
    LABEL_DATASET_FAMILY_V001,
    LABEL_DATASET_VERSION_V001,
    LABEL_HORIZON_MS_V001,
    LABEL_HORIZONS_V001,
    LABEL_LINEAGE_COLUMNS_V001,
    LABEL_NAMES_V001,
    LABEL_SCHEMA_COLUMNS_V001,
    LABEL_SCHEMA_V001,
    LABEL_SCHEMA_VERSION_V001,
    LABEL_SUPPORT_COLUMN_NAMES_V001,
    LabelSchemaError,
    assert_no_forbidden_label_substrings,
    build_label_config_hash,
)


def test_constants_locked() -> None:
    assert LABEL_DATASET_FAMILY_V001 == "microstructure_labels_aggtrades_v001"
    assert LABEL_DATASET_VERSION_V001 == "v001"
    assert LABEL_SCHEMA_VERSION_V001 == "v001"


def test_horizons_locked() -> None:
    assert LABEL_HORIZONS_V001 == ("1s", "5s", "15s", "60s")
    assert LABEL_HORIZON_MS_V001 == (1000, 5000, 15000, 60000)
    assert len(LABEL_HORIZONS_V001) == len(LABEL_HORIZON_MS_V001) == 4


def test_label_names_exactly_eight() -> None:
    assert len(LABEL_NAMES_V001) == 8
    assert LABEL_NAMES_V001 == (
        "forward_log_return_1s",
        "forward_log_return_5s",
        "forward_log_return_15s",
        "forward_log_return_60s",
        "forward_direction_1s",
        "forward_direction_5s",
        "forward_direction_15s",
        "forward_direction_60s",
    )


def test_support_column_names_exactly_fourteen() -> None:
    assert len(LABEL_SUPPORT_COLUMN_NAMES_V001) == 14
    assert LABEL_SUPPORT_COLUMN_NAMES_V001 == (
        "reference_row_index_1s",
        "reference_timestamp_ms_1s",
        "horizon_censored_flag_1s",
        "reference_row_index_5s",
        "reference_timestamp_ms_5s",
        "horizon_censored_flag_5s",
        "reference_row_index_15s",
        "reference_timestamp_ms_15s",
        "horizon_censored_flag_15s",
        "reference_row_index_60s",
        "reference_timestamp_ms_60s",
        "horizon_censored_flag_60s",
        "label_invalid_price_flag",
        "label_any_censored_flag",
    )


def test_schema_total_count_39() -> None:
    assert len(LABEL_SCHEMA_V001) == 39
    assert LABEL_SCHEMA_COLUMNS_V001 == LABEL_SCHEMA_V001


def test_schema_lineage_block_first_seventeen() -> None:
    assert LABEL_SCHEMA_V001[:17] == LABEL_LINEAGE_COLUMNS_V001
    assert len(LABEL_LINEAGE_COLUMNS_V001) == 17


def test_schema_canonical_order_lineage_then_labels_then_support() -> None:
    assert LABEL_SCHEMA_V001[:17] == LABEL_LINEAGE_COLUMNS_V001
    assert LABEL_SCHEMA_V001[17:25] == LABEL_NAMES_V001
    assert LABEL_SCHEMA_V001[25:] == LABEL_SUPPORT_COLUMN_NAMES_V001


def test_schema_does_not_include_thirty_seconds_or_five_minutes() -> None:
    for col in LABEL_SCHEMA_V001:
        assert "30s" not in col
        assert "5m" not in col
        assert "300s" not in col


def test_label_config_hash_deterministic() -> None:
    digest1 = build_label_config_hash(
        source_feature_manifest_sha256="0" * 64,
        source_feature_parquet_sha256="1" * 64,
        source_feature_successor_state_sha256="2" * 64,
        source_phase_4bi_b_gate_report_sha256="3" * 64,
    )
    digest2 = build_label_config_hash(
        source_feature_manifest_sha256="0" * 64,
        source_feature_parquet_sha256="1" * 64,
        source_feature_successor_state_sha256="2" * 64,
        source_phase_4bi_b_gate_report_sha256="3" * 64,
    )
    assert digest1 == digest2
    assert len(digest1) == 64
    assert all(ch in "0123456789abcdef" for ch in digest1)


def test_label_config_hash_changes_when_source_changes() -> None:
    base = build_label_config_hash(
        source_feature_manifest_sha256="0" * 64,
        source_feature_parquet_sha256="1" * 64,
        source_feature_successor_state_sha256="2" * 64,
        source_phase_4bi_b_gate_report_sha256="3" * 64,
    )
    flipped = build_label_config_hash(
        source_feature_manifest_sha256="0" * 63 + "1",
        source_feature_parquet_sha256="1" * 64,
        source_feature_successor_state_sha256="2" * 64,
        source_phase_4bi_b_gate_report_sha256="3" * 64,
    )
    assert base != flipped


def test_label_config_hash_rejects_non_hex64() -> None:
    import pytest

    with pytest.raises(LabelSchemaError):
        build_label_config_hash(
            source_feature_manifest_sha256="not-hex",
            source_feature_parquet_sha256="1" * 64,
            source_feature_successor_state_sha256="2" * 64,
            source_phase_4bi_b_gate_report_sha256="3" * 64,
        )


def test_no_forbidden_substrings_in_canonical_schema() -> None:
    # The canonical schema must be free of every forbidden token.
    assert_no_forbidden_label_substrings(LABEL_SCHEMA_V001)


def test_forbidden_substring_detector_fails_on_violation() -> None:
    import pytest

    with pytest.raises(LabelSchemaError):
        assert_no_forbidden_label_substrings(("dataset_family", "forward_pnl_1s"))


def test_forbidden_substring_set_locked() -> None:
    # The set is locked at v001 and must include the key prohibitions.
    forbidden = set(FORBIDDEN_LABEL_COLUMN_SUBSTRINGS)
    required = {
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
        "entry",
        "exit",
        "signal",
        "target",
        "barrier",
        "liquidation",
    }
    assert required.issubset(forbidden)
