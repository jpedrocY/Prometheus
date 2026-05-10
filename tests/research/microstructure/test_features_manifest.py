"""Phase 4bh tests: features_manifest.build_feature_manifest."""

from __future__ import annotations

import pytest

from prometheus.research.microstructure import (
    FEATURE_DATASET_FAMILY,
    FEATURE_DATASET_VERSION,
    FEATURE_NAMES_V001,
    FEATURE_SCHEMA_VERSION,
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    REQUIRED_BOUNDARY_CONFIRMATIONS,
    REQUIRED_FEATURE_GOVERNANCE_KEYS,
    FeatureManifestError,
    build_feature_manifest,
)

_VALID_KW = {
    "symbol": "BTCUSDT",
    "utc_date": "2025-01-15",
    "feature_parquet_relative_path": (
        "features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/"
        "BTCUSDT-features-aggtrades-2025-01-15.parquet"
    ),
    "feature_parquet_sha256": "a" * 64,
    "feature_parquet_size_bytes": 12345,
    "row_count": 1681098,
    "feature_config_hash": "b" * 64,
    "source_normalized_manifest_sha256": "c" * 64,
    "source_normalized_parquet_sha256": "d" * 64,
    "source_successor_state_sha256": "e" * 64,
    "source_phase_4bf_gate_report_sha256": "f" * 64,
    "code_commit_sha": "0" * 40,
    "created_at_unix_ms": 1_700_000_000_000,
}


def test_manifest_locked_keys_present() -> None:
    m = build_feature_manifest(**_VALID_KW)
    assert m["dataset_family"] == FEATURE_DATASET_FAMILY
    assert m["dataset_version"] == FEATURE_DATASET_VERSION
    assert m["feature_schema_version"] == FEATURE_SCHEMA_VERSION
    assert m["symbol"] == "BTCUSDT"
    assert m["utc_date"] == "2025-01-15"
    assert tuple(m["feature_list"]) == FEATURE_NAMES_V001
    assert tuple(m["window_list"]) == FEATURE_WINDOW_LABELS_V001
    assert tuple(m["window_ms_list"]) == FEATURE_WINDOWS_MS_V001
    assert m["row_count"] == 1681098
    assert m["files"][0]["sha256"] == _VALID_KW["feature_parquet_sha256"]
    assert m["files"][0]["row_count"] == 1681098


def test_manifest_research_eligible_false_and_pending() -> None:
    m = build_feature_manifest(**_VALID_KW)
    assert m["research_eligible"] is False
    assert m["eligibility_gate_status"] == "pending"


def test_manifest_governance_labels_locked() -> None:
    m = build_feature_manifest(**_VALID_KW)
    g = m["governance_labels"]
    for key in REQUIRED_FEATURE_GOVERNANCE_KEYS:
        assert key in g
    assert g["phase_id"] == "4bh"
    assert g["feature_computation"] == "allowed_by_phase_4bh"
    assert g["labels"] == "forbidden"
    assert g["ml"] == "forbidden"
    assert g["strategy"] == "forbidden"
    assert g["backtest"] == "forbidden"
    assert g["acquisition"] == "unauthorized"
    assert g["stop_trigger_domain"] == "trade_price_backtest_candidate"


def test_manifest_boundary_confirmations_all_true() -> None:
    m = build_feature_manifest(**_VALID_KW)
    boundary = m["boundary_confirmations"]
    for key in REQUIRED_BOUNDARY_CONFIRMATIONS:
        assert boundary[key] is True


def test_manifest_invalid_windows_default_empty() -> None:
    m = build_feature_manifest(**_VALID_KW)
    assert m["invalid_windows"] == []


def test_manifest_propagates_invalid_windows() -> None:
    m = build_feature_manifest(
        **{**_VALID_KW},
        invalid_windows=[{"start_time_ms": 1, "end_time_ms": 2, "reason": "demo"}],
    )
    assert m["invalid_windows"] == [
        {"start_time_ms": 1, "end_time_ms": 2, "reason": "demo"}
    ]


def test_manifest_extra_governance_labels_must_not_override_locked() -> None:
    with pytest.raises(FeatureManifestError):
        build_feature_manifest(
            **{**_VALID_KW},
            extra_governance_labels={"phase_id": "different"},
        )


def test_manifest_rejects_lowercase_symbol() -> None:
    with pytest.raises(FeatureManifestError):
        build_feature_manifest(**{**_VALID_KW, "symbol": "btcusdt"})


def test_manifest_rejects_short_sha() -> None:
    with pytest.raises(FeatureManifestError):
        build_feature_manifest(
            **{**_VALID_KW, "feature_parquet_sha256": "abc"}
        )


def test_manifest_rejects_negative_row_count() -> None:
    with pytest.raises(FeatureManifestError):
        build_feature_manifest(**{**_VALID_KW, "row_count": -1})


def test_manifest_rejects_negative_size_bytes() -> None:
    with pytest.raises(FeatureManifestError):
        build_feature_manifest(**{**_VALID_KW, "feature_parquet_size_bytes": -1})


def test_manifest_files_entry_has_sha_and_size() -> None:
    m = build_feature_manifest(**_VALID_KW)
    assert m["files"][0]["sha256"] == _VALID_KW["feature_parquet_sha256"]
    assert m["files"][0]["size_bytes"] == _VALID_KW["feature_parquet_size_bytes"]


def test_manifest_extra_governance_labels_added() -> None:
    m = build_feature_manifest(
        **{**_VALID_KW},
        extra_governance_labels={"custom_label": "custom_value"},
    )
    assert m["governance_labels"]["custom_label"] == "custom_value"


def test_manifest_rejects_bad_utc_date() -> None:
    with pytest.raises(FeatureManifestError):
        build_feature_manifest(**{**_VALID_KW, "utc_date": "2025/01/15"})


def test_manifest_rejects_empty_relative_path() -> None:
    with pytest.raises(FeatureManifestError):
        build_feature_manifest(
            **{**_VALID_KW, "feature_parquet_relative_path": ""}
        )
