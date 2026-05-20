"""Phase 4bm-H v002 feature schema unit tests."""

from __future__ import annotations

import pytest

from prometheus.research.microstructure import (
    CROSS_DAY_LOOKBACK_POLICY_V002,
    CROSS_DAY_TAIL_BUFFER_MS,
    FEATURE_DATASET_VERSION_V002,
    FEATURE_NAMES_V002,
    FEATURE_SCHEMA_V002,
    FEATURE_SCHEMA_VERSION_V002,
    FEATURE_WINDOWS_MS_V002,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002,
    LINEAGE_COLUMNS_V002,
    PHASE_4BM_E_OUTCOME_LITERAL,
    SOURCE_NORMALIZED_DATASET_FAMILY_V002,
    SOURCE_NORMALIZED_DATASET_VERSION_V002,
    assert_no_forbidden_substrings_v002,
    build_feature_config_v002,
    compute_feature_config_hash_v002,
)
from prometheus.research.microstructure.features_schema import FeatureSchemaError


def test_v002_schema_has_62_columns_in_canonical_order() -> None:
    assert len(FEATURE_SCHEMA_V002) == 62
    assert len(LINEAGE_COLUMNS_V002) == 17
    assert len(FEATURE_NAMES_V002) == 45
    assert FEATURE_SCHEMA_V002 == LINEAGE_COLUMNS_V002 + FEATURE_NAMES_V002


def test_v002_lineage_columns_match_phase_4bm_g_design() -> None:
    expected = (
        "dataset_family",
        "dataset_version",
        "source_dataset_family",
        "source_dataset_version",
        "feature_schema_version",
        "symbol",
        "utc_date",
        "agg_trade_id",
        "row_index",
        "feature_timestamp_ms",
        "source_transact_time_ms",
        "source_normalized_parquet_per_day_sha256",
        "source_normalized_manifest_sha256",
        "source_successor_state_sha256",
        "source_phase_4bm_d_gate_report_sha256",
        "source_phase_4bm_e_outcome",
        "feature_config_hash",
    )
    assert expected == LINEAGE_COLUMNS_V002


def test_v002_identity_constants() -> None:
    assert FEATURE_DATASET_VERSION_V002 == "v002"
    assert FEATURE_SCHEMA_VERSION_V002 == "v001"
    assert SOURCE_NORMALIZED_DATASET_FAMILY_V002 == "microstructure_normalized_aggtrades_v001"
    assert SOURCE_NORMALIZED_DATASET_VERSION_V002 == "v002"
    assert PHASE_4BM_E_OUTCOME_LITERAL == "Option B / Decision form 2"
    assert FEATURE_WINDOWS_MS_V002 == (1000, 5000, 15000, 60000)
    assert CROSS_DAY_LOOKBACK_POLICY_V002 == "causal_cross_day_lookback"
    assert CROSS_DAY_TAIL_BUFFER_MS == 60_000


def test_forbidden_substring_detector_passes_v002_schema() -> None:
    # Must not raise on the actual v002 schema.
    assert_no_forbidden_substrings_v002(FEATURE_SCHEMA_V002)


@pytest.mark.parametrize("token", FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002)
def test_forbidden_substring_detector_rejects_each_token(token: str) -> None:
    bad_col = f"rolling_{token}_60s"
    with pytest.raises(FeatureSchemaError):
        assert_no_forbidden_substrings_v002((bad_col,))


def test_forbidden_substring_list_matches_v001_26_tokens() -> None:
    # The Phase 4bm-G memo §13 forbidden-substring set is the v001
    # Phase 4bh-B 26-token list verbatim.
    assert len(FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002) == 26
    assert "label" in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002
    assert "target" in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002
    assert "future" in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002


def test_feature_config_v002_hash_is_deterministic(tmp_path) -> None:
    cfg_a = build_feature_config_v002(
        source_normalized_manifest_path=tmp_path / "norm.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_manifest_path=tmp_path / "feat_manifest.json",
        output_feature_root_dir=tmp_path / "features",
        code_commit_sha="0" * 40,
    )
    cfg_b = build_feature_config_v002(
        source_normalized_manifest_path=tmp_path / "norm.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_manifest_path=tmp_path / "feat_manifest.json",
        output_feature_root_dir=tmp_path / "features",
        code_commit_sha="0" * 40,
    )
    assert cfg_a.feature_config_hash == cfg_b.feature_config_hash
    assert len(cfg_a.feature_config_hash) == 64
    assert all(c in "0123456789abcdef" for c in cfg_a.feature_config_hash)


def test_feature_config_v002_hash_changes_when_path_changes(tmp_path) -> None:
    cfg_a = build_feature_config_v002(
        source_normalized_manifest_path=tmp_path / "a.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_manifest_path=tmp_path / "feat_manifest.json",
        output_feature_root_dir=tmp_path / "features",
    )
    cfg_b = build_feature_config_v002(
        source_normalized_manifest_path=tmp_path / "b.json",
        source_successor_state_path=tmp_path / "succ.json",
        output_feature_manifest_path=tmp_path / "feat_manifest.json",
        output_feature_root_dir=tmp_path / "features",
    )
    assert cfg_a.feature_config_hash != cfg_b.feature_config_hash


def test_feature_config_v002_hash_helper_is_canonical_json_sha256() -> None:
    h = compute_feature_config_hash_v002({"b": 2, "a": 1})
    h2 = compute_feature_config_hash_v002({"a": 1, "b": 2})
    assert h == h2
    assert len(h) == 64


def test_feature_config_v002_rejects_wrong_dataset_version(tmp_path) -> None:
    # Must reject if we try to construct the dataclass directly with a
    # wrong dataset_version.
    from prometheus.research.microstructure import FeatureComputationConfigV002

    with pytest.raises(FeatureSchemaError):
        FeatureComputationConfigV002(
            dataset_family="microstructure_features_aggtrades_v001",
            dataset_version="v003",  # wrong
            feature_schema_version=FEATURE_SCHEMA_VERSION_V002,
            source_dataset_family=SOURCE_NORMALIZED_DATASET_FAMILY_V002,
            source_dataset_version=SOURCE_NORMALIZED_DATASET_VERSION_V002,
            source_normalized_manifest_path="x",
            source_successor_state_path="x",
            output_feature_manifest_path="x",
            output_feature_root_dir="x",
            windows_ms=FEATURE_WINDOWS_MS_V002,
            feature_names=FEATURE_NAMES_V002,
            timestamp_alignment="event_aligned",
            timestamp_policy="event_aligned_utc_ms_int64",
            causal_window_rule="trailing_right_open_left",
            leakage_policy="causal_only_no_future_lookahead",
            same_timestamp_tie_rule="row_index_le_R",
            cross_day_lookback_policy="causal_cross_day_lookback",
            cross_day_tail_buffer_ms=60_000,
        )


def test_feature_schema_v002_is_a_module_level_constant_used_by_kernel() -> None:
    # Schema equality test: the canonical column tuple must equal
    # ``LINEAGE_COLUMNS_V002 + FEATURE_NAMES_V002`` and is the single
    # source of truth for column order across schema / compute /
    # manifest / validation.
    assert tuple(list(LINEAGE_COLUMNS_V002) + list(FEATURE_NAMES_V002)) == FEATURE_SCHEMA_V002
