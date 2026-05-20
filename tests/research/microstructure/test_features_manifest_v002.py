"""Phase 4bm-H v002 feature manifest builder unit tests."""

from __future__ import annotations

import pytest

from prometheus.research.microstructure import (
    FEATURE_SCHEMA_V002,
    PHASE_4BM_E_OUTCOME_LITERAL,
    REQUIRED_V002_BOUNDARY_CONFIRMATIONS,
    REQUIRED_V002_GOVERNANCE_KEYS,
    REQUIRED_V002_NON_AUTHORIZATION_FLAGS,
    FeatureManifestErrorV002,
    build_feature_manifest_v002,
    feature_dtypes_v002,
)


def _per_day(n: int = 90) -> list[dict]:
    return [
        {
            "utc_date": f"2024-12-{i + 1:02d}" if i < 31 else f"2025-01-{i - 30:02d}",
            "feature_parquet_path": f"microstructure/features/m_v002/BTCUSDT/2024/12/x-{i}.parquet",
            "feature_parquet_sha256": "a" * 64,
            "feature_parquet_size_bytes": 100,
            "row_count": 1000,
            "feature_sidecar_path": (
                f"microstructure/features/m_v002/BTCUSDT/2024/12/x-{i}.parquet.sha256"
            ),
            "feature_sidecar_sha256": "b" * 64,
            "source_normalized_parquet_per_day_sha256": "c" * 64,
        }
        for i in range(n)
    ]


def _common_kwargs() -> dict:
    return {
        "symbol": "BTCUSDT",
        "input_date_start": "2024-12-01",
        "input_date_end": "2025-02-28",
        "date_count": 90,
        "expected_event_count": 155_153_449,
        "actual_feature_row_count": 90_000,
        "per_day_outputs": _per_day(90),
        "feature_dtypes": feature_dtypes_v002(),
        "feature_config_hash": "d" * 64,
        "source_normalized_manifest_path": "data/microstructure/manifests/norm.json",
        "source_normalized_manifest_sha256": "1" * 64,
        "source_successor_state_path": "data/microstructure/successor-state/s.json",
        "source_successor_state_sha256": "2" * 64,
        "source_phase_4bm_d_gate_report_sha256": "3" * 64,
        "source_phase_4bm_f_successor_state_sha256": "2" * 64,
        "source_phase_4bl_d_r_raw_gate_report_sha256": "4" * 64,
        "source_phase_4bl_e_raw_successor_state_sha256": "5" * 64,
        "source_v002_raw_manifest_sha256": "6" * 64,
        "source_v002_acquisition_log_sha256": "7" * 64,
    }


def test_v002_manifest_carries_required_identity_fields() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    assert m["dataset_family"] == "microstructure_features_aggtrades_v001"
    assert m["dataset_version"] == "v002"
    assert m["feature_schema_version"] == "v001"
    assert m["source_dataset_family"] == "microstructure_normalized_aggtrades_v001"
    assert m["source_dataset_version"] == "v002"
    assert m["source_phase_4bm_e_outcome"] == PHASE_4BM_E_OUTCOME_LITERAL


def test_v002_manifest_defaults_research_eligible_false() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    assert m["research_eligible"] is False
    assert m["eligibility_gate_status"] == "pending"


def test_v002_manifest_carries_all_non_authorization_flags_false() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    for key in REQUIRED_V002_NON_AUTHORIZATION_FLAGS:
        assert m[key] is False, f"{key} must default False"


def test_v002_manifest_boundary_confirmations_all_true() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    for key in REQUIRED_V002_BOUNDARY_CONFIRMATIONS:
        assert m["boundary_confirmations"][key] is True


def test_v002_manifest_governance_keys_locked() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    for key in REQUIRED_V002_GOVERNANCE_KEYS:
        assert key in m["governance_labels"]
    assert m["governance_labels"]["phase_id"] == "4bm-H"
    assert m["governance_labels"]["feature_computation"] == "allowed_by_phase_4bm_h"
    assert m["governance_labels"]["labels"] == "forbidden"
    assert m["governance_labels"]["ml"] == "forbidden"
    assert m["governance_labels"]["strategy"] == "forbidden"
    assert m["governance_labels"]["backtest"] == "forbidden"
    assert m["governance_labels"]["acquisition"] == "unauthorized"


def test_v002_manifest_carries_full_lineage_sha_block() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    assert m["source_normalized_manifest_sha256"] == "1" * 64
    assert m["source_successor_state_sha256"] == "2" * 64
    assert m["source_phase_4bm_d_gate_report_sha256"] == "3" * 64
    assert m["source_phase_4bl_d_r_raw_gate_report_sha256"] == "4" * 64
    assert m["source_phase_4bl_e_raw_successor_state_sha256"] == "5" * 64
    assert m["source_v002_raw_manifest_sha256"] == "6" * 64
    assert m["source_v002_acquisition_log_sha256"] == "7" * 64


def test_v002_manifest_feature_dtypes_cover_all_columns() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    assert tuple(m["feature_dtypes"].keys()) == FEATURE_SCHEMA_V002


def test_v002_manifest_per_day_outputs_length_must_match_date_count() -> None:
    kwargs = _common_kwargs()
    kwargs["per_day_outputs"] = _per_day(89)  # too few
    with pytest.raises(FeatureManifestErrorV002):
        build_feature_manifest_v002(**kwargs)


def test_v002_manifest_records_window_and_timestamp_policies() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    assert m["feature_windows_ms"] == [1000, 5000, 15000, 60000]
    assert m["window_boundary_policy"] == "trailing_right_closed_left_open"
    assert m["timestamp_policy"] == "event_aligned_utc_ms_int64"
    assert m["leakage_policy"] == "causal_only_no_future_lookahead"
    assert m["same_timestamp_tie_rule"] == "row_index_le_R"
    assert m["cross_day_lookback_policy"] == "causal_cross_day_lookback"
    assert m["cross_day_tail_buffer_ms"] == 60_000


def test_v002_manifest_includes_forbidden_substring_detector_tokens() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    tokens = m["forbidden_substring_detector_tokens"]
    assert "label" in tokens
    assert "target" in tokens
    assert "future" in tokens
    assert len(tokens) == 26


def test_v002_manifest_records_immutability_and_network_flags() -> None:
    m = build_feature_manifest_v002(**_common_kwargs())
    assert m["no_network_io"] is True
    assert m["no_credentials"] is True
    assert m["no_mcp_or_graphify"] is True
    assert m["no_manifest_mutation"] is True
    assert m["phase_4aw_flip_research_eligible_invariant_preserved"] is True


def test_v002_manifest_rejects_bad_sha_field() -> None:
    kwargs = _common_kwargs()
    kwargs["source_phase_4bm_d_gate_report_sha256"] = "tooshort"
    with pytest.raises(FeatureManifestErrorV002):
        build_feature_manifest_v002(**kwargs)


def test_v002_manifest_rejects_per_day_entry_missing_keys() -> None:
    kwargs = _common_kwargs()
    bad = _per_day(90)
    bad[0].pop("feature_parquet_sha256")
    kwargs["per_day_outputs"] = bad
    with pytest.raises(FeatureManifestErrorV002):
        build_feature_manifest_v002(**kwargs)
