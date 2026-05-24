"""Phase 4bm-O v002 label schema and config hash tests."""

from __future__ import annotations

import json

import pytest

from prometheus.research.microstructure.labels_schema_v002 import (
    ANCHOR_POLICY_V002,
    DIRECTION_THRESHOLD_POLICY_V002,
    DTYPE_POLICY_V002,
    FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002,
    FUTURE_REFERENCE_POLICY_V002,
    LABEL_DATASET_FAMILY_V002,
    LABEL_DATASET_VERSION_V002,
    LABEL_HORIZON_MS_V002,
    LABEL_HORIZONS_V002,
    LABEL_LINEAGE_COLUMNS_V002,
    LABEL_NAMES_V002,
    LABEL_SCHEMA_V002,
    LABEL_SCHEMA_VERSION_V002,
    LABEL_SUPPORT_COLUMN_NAMES_V002,
    NULL_CENSORING_POLICY_V002,
    LabelSchemaErrorV002,
    assert_no_forbidden_label_substrings_v002,
    build_label_config_hash_v002,
)

# ---------------------------------------------------------------------------
# Identity / horizon / column constants
# ---------------------------------------------------------------------------


def test_dataset_identity_constants() -> None:
    assert LABEL_DATASET_FAMILY_V002 == "microstructure_labels_aggtrades_v001"
    assert LABEL_DATASET_VERSION_V002 == "v002"
    assert LABEL_SCHEMA_VERSION_V002 == "v001"


def test_horizon_constants() -> None:
    assert LABEL_HORIZONS_V002 == ("1s", "5s", "15s", "60s")
    assert LABEL_HORIZON_MS_V002 == (1000, 5000, 15000, 60000)


def test_label_names_canonical_order() -> None:
    assert LABEL_NAMES_V002 == (
        "forward_log_return_1s",
        "forward_log_return_5s",
        "forward_log_return_15s",
        "forward_log_return_60s",
        "forward_direction_1s",
        "forward_direction_5s",
        "forward_direction_15s",
        "forward_direction_60s",
    )


def test_support_column_names_canonical_order() -> None:
    assert LABEL_SUPPORT_COLUMN_NAMES_V002 == (
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


def test_lineage_columns_canonical_order() -> None:
    assert LABEL_LINEAGE_COLUMNS_V002 == (
        "dataset_family",
        "dataset_version",
        "label_schema_version",
        "source_feature_dataset_family",
        "source_feature_dataset_version",
        "source_feature_manifest_sha256",
        "source_feature_parquet_sha256",
        "source_feature_successor_state_sha256",
        "source_phase_4bm_j_gate_report_sha256",
        "source_normalized_manifest_sha256",
        "source_raw_manifest_sha256",
        "symbol",
        "utc_date",
        "row_index",
        "agg_trade_id",
        "feature_timestamp_ms",
        "source_transact_time_ms",
    )


def test_schema_has_exactly_40_columns_in_phase_4bm_n_order() -> None:
    assert len(LABEL_SCHEMA_V002) == 40
    # First 17 are lineage.
    assert LABEL_SCHEMA_V002[:17] == LABEL_LINEAGE_COLUMNS_V002
    # Position 18 (index 17) is label_config_hash.
    assert LABEL_SCHEMA_V002[17] == "label_config_hash"
    # Positions 19-26 (indices 18-25) are the 8 labels.
    assert LABEL_SCHEMA_V002[18:26] == LABEL_NAMES_V002
    # Positions 27-40 (indices 26-39) are the 14 support columns.
    assert LABEL_SCHEMA_V002[26:] == LABEL_SUPPORT_COLUMN_NAMES_V002


def test_schema_column_uniqueness() -> None:
    assert len(set(LABEL_SCHEMA_V002)) == len(LABEL_SCHEMA_V002)


# ---------------------------------------------------------------------------
# Forbidden substrings
# ---------------------------------------------------------------------------


def test_forbidden_substring_list() -> None:
    expected = (
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
    )
    assert expected == FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002


def test_no_forbidden_substring_in_canonical_schema() -> None:
    # The canonical schema must pass the detector.
    assert_no_forbidden_label_substrings_v002(LABEL_SCHEMA_V002)


@pytest.mark.parametrize(
    "bad_col",
    [
        "pnl_total",
        "forward_pnl_1s",
        "mae_window",
        "exit_price",
        "model_score",
        "prediction_1s",
        "barrier_up",
        "target_band",
        "strategy_action",
        "liquidation_flag",
    ],
)
def test_forbidden_substring_detector_flags_bad_columns(bad_col: str) -> None:
    with pytest.raises(LabelSchemaErrorV002):
        assert_no_forbidden_label_substrings_v002([*LABEL_SCHEMA_V002, bad_col])


# ---------------------------------------------------------------------------
# label_config_hash
# ---------------------------------------------------------------------------


def _baseline_kwargs() -> dict[str, str]:
    return {
        "source_feature_manifest_sha256": "a" * 64,
        "source_feature_successor_state_sha256": "b" * 64,
        "source_phase_4bm_j_gate_report_sha256": "c" * 64,
        "source_normalized_manifest_sha256": "d" * 64,
        "source_raw_manifest_sha256": "e" * 64,
        "feature_config_hash": "f" * 64,
    }


def test_label_config_hash_is_deterministic() -> None:
    h1 = build_label_config_hash_v002(**_baseline_kwargs())
    h2 = build_label_config_hash_v002(**_baseline_kwargs())
    assert h1 == h2
    assert len(h1) == 64
    assert all(c in "0123456789abcdef" for c in h1)


def test_label_config_hash_changes_with_each_input() -> None:
    base = build_label_config_hash_v002(**_baseline_kwargs())
    for key in _baseline_kwargs():
        kwargs = _baseline_kwargs()
        # Toggle the field to a different valid hex.
        kwargs[key] = "9" * 64
        assert build_label_config_hash_v002(**kwargs) != base, (
            f"changing {key} did not change the hash"
        )


def test_label_config_hash_rejects_non_hex_inputs() -> None:
    for key in _baseline_kwargs():
        kwargs = _baseline_kwargs()
        kwargs[key] = "not-a-hex"
        with pytest.raises(LabelSchemaErrorV002):
            build_label_config_hash_v002(**kwargs)


def test_label_config_hash_canonical_json_includes_all_required_fields() -> None:
    # Re-derive the payload manually using the exposed constants and
    # confirm the hash matches. This locks down the canonical-JSON
    # serialisation policy (sorted keys, ASCII, no whitespace).
    import hashlib

    payload = {
        "dataset_family": LABEL_DATASET_FAMILY_V002,
        "dataset_version": LABEL_DATASET_VERSION_V002,
        "label_schema_version": LABEL_SCHEMA_VERSION_V002,
        "label_list": list(LABEL_NAMES_V002),
        "support_column_list": list(LABEL_SUPPORT_COLUMN_NAMES_V002),
        "lineage_column_list": list(LABEL_LINEAGE_COLUMNS_V002),
        "horizon_list": list(LABEL_HORIZONS_V002),
        "horizon_ms_list": list(LABEL_HORIZON_MS_V002),
        "anchor_policy": ANCHOR_POLICY_V002,
        "future_reference_policy": FUTURE_REFERENCE_POLICY_V002,
        "direction_threshold_policy": DIRECTION_THRESHOLD_POLICY_V002,
        "null_censoring_policy": NULL_CENSORING_POLICY_V002,
        "dtype_policy": DTYPE_POLICY_V002,
        **_baseline_kwargs(),
    }
    expected = hashlib.sha256(
        json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
    ).hexdigest()
    assert build_label_config_hash_v002(**_baseline_kwargs()) == expected


def test_label_config_hash_differs_from_v001_hash() -> None:
    # v001 uses 4 lineage SHAs; v002 uses 6 lineage SHAs and adds the
    # ``lineage_column_list`` payload entry. The two should not collide
    # even when given the same source_feature_* hashes.
    from prometheus.research.microstructure.labels_schema import (
        build_label_config_hash,
    )

    v001_hash = build_label_config_hash(
        source_feature_manifest_sha256="a" * 64,
        source_feature_parquet_sha256="b" * 64,
        source_feature_successor_state_sha256="c" * 64,
        source_phase_4bi_b_gate_report_sha256="d" * 64,
    )
    v002_hash = build_label_config_hash_v002(**_baseline_kwargs())
    assert v001_hash != v002_hash
