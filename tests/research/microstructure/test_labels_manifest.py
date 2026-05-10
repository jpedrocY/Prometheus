"""Phase 4bj-C label manifest builder tests."""

from __future__ import annotations

import pytest

from prometheus.research.microstructure.labels_manifest import (
    REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS,
    REQUIRED_LABEL_GOVERNANCE_KEYS,
    LabelManifestError,
    build_label_manifest_v001,
)
from prometheus.research.microstructure.labels_schema import (
    LABEL_HORIZON_MS_V001,
    LABEL_HORIZONS_V001,
    LABEL_NAMES_V001,
    LABEL_SCHEMA_V001,
    LABEL_SUPPORT_COLUMN_NAMES_V001,
)


def _kwargs() -> dict[str, object]:
    return {
        "symbol": "BTCUSDT",
        "utc_date": "2025-01-15",
        "label_parquet_relative_path": (
            "data/microstructure/labels/microstructure_labels_aggtrades_v001/"
            "BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet"
        ),
        "label_parquet_sha256": "0" * 64,
        "label_parquet_size_bytes": 12_345,
        "row_count": 1_681_098,
        "label_config_hash": "1" * 64,
        "source_feature_manifest_sha256": "2" * 64,
        "source_feature_parquet_sha256": "3" * 64,
        "source_feature_successor_state_sha256": "4" * 64,
        "source_phase_4bi_b_gate_report_sha256": "5" * 64,
        "source_normalized_parquet_sha256": "6" * 64,
        "invalid_price_row_count": 0,
        "censored_per_horizon": {"1s": 1, "5s": 2, "15s": 3, "60s": 4},
        "code_commit_sha": "0" * 40,
        "created_at_unix_ms": 1_700_000_000_000,
        "created_at_utc": "2025-01-15T00:00:00Z",
    }


def test_required_governance_and_boundary_keys_present() -> None:
    m = build_label_manifest_v001(**_kwargs())
    for k in REQUIRED_LABEL_GOVERNANCE_KEYS:
        assert k in m["governance_labels"]
    for k in REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS:
        assert m["boundary_confirmations"].get(k) is True


def test_research_eligible_and_status_locked_defaults() -> None:
    m = build_label_manifest_v001(**_kwargs())
    assert m["research_eligible"] is False
    assert m["eligibility_gate_status"] == "pending"


def test_label_list_and_support_match_constants() -> None:
    m = build_label_manifest_v001(**_kwargs())
    assert tuple(m["label_list"]) == LABEL_NAMES_V001
    assert tuple(m["support_column_list"]) == LABEL_SUPPORT_COLUMN_NAMES_V001
    assert tuple(m["schema_column_list"]) == LABEL_SCHEMA_V001
    assert m["column_count"] == 39


def test_horizon_lists_match_constants() -> None:
    m = build_label_manifest_v001(**_kwargs())
    assert tuple(m["horizon_list"]) == LABEL_HORIZONS_V001
    assert tuple(m["horizon_ms_list"]) == LABEL_HORIZON_MS_V001


def test_censored_per_horizon_is_dict_per_horizon() -> None:
    m = build_label_manifest_v001(**_kwargs())
    assert m["censored_per_horizon"] == {"1s": 1, "5s": 2, "15s": 3, "60s": 4}


def test_files_entry_records_path_sha_size_row_count() -> None:
    m = build_label_manifest_v001(**_kwargs())
    files = m["files"]
    assert isinstance(files, list)
    assert len(files) == 1
    entry = files[0]
    assert entry["sha256"] == "0" * 64
    assert entry["row_count"] == 1_681_098
    assert entry["size_bytes"] == 12_345


def test_governance_locks_forbidden_values() -> None:
    m = build_label_manifest_v001(**_kwargs())
    gov = m["governance_labels"]
    assert gov["ml"] == "forbidden"
    assert gov["strategy"] == "forbidden"
    assert gov["backtest"] == "forbidden"
    assert gov["acquisition"] == "unauthorized"
    assert gov["paper_shadow_live"] == "forbidden"
    assert gov["deployment"] == "forbidden"
    assert gov["exchange_write"] == "forbidden"
    assert gov["phase_id"] == "4bj-C"


def test_governance_labels_extra_can_add_safe_key_but_not_override() -> None:
    kwargs = _kwargs()
    m = build_label_manifest_v001(**kwargs, extra_governance_labels={"audit": "x"})
    assert m["governance_labels"]["audit"] == "x"
    with pytest.raises(LabelManifestError):
        build_label_manifest_v001(
            **kwargs,
            extra_governance_labels={"ml": "anything"},
        )


def test_rejects_invalid_symbol_or_date() -> None:
    kwargs = _kwargs()
    kwargs["symbol"] = "btcusdt"
    with pytest.raises(LabelManifestError):
        build_label_manifest_v001(**kwargs)
    kwargs = _kwargs()
    kwargs["utc_date"] = "2025/01/15"
    with pytest.raises(LabelManifestError):
        build_label_manifest_v001(**kwargs)


def test_rejects_bad_sha_lengths() -> None:
    kwargs = _kwargs()
    kwargs["label_parquet_sha256"] = "not-hex"
    with pytest.raises(LabelManifestError):
        build_label_manifest_v001(**kwargs)


def test_rejects_negative_row_count_or_size() -> None:
    kwargs = _kwargs()
    kwargs["row_count"] = -1
    with pytest.raises(LabelManifestError):
        build_label_manifest_v001(**kwargs)
    kwargs = _kwargs()
    kwargs["label_parquet_size_bytes"] = -1
    with pytest.raises(LabelManifestError):
        build_label_manifest_v001(**kwargs)


def test_rejects_bad_censored_per_horizon() -> None:
    kwargs = _kwargs()
    kwargs["censored_per_horizon"] = {"1s": 1, "5s": 2}
    with pytest.raises(LabelManifestError):
        build_label_manifest_v001(**kwargs)
    kwargs = _kwargs()
    kwargs["censored_per_horizon"] = {"1s": -1, "5s": 2, "15s": 3, "60s": 4}
    with pytest.raises(LabelManifestError):
        build_label_manifest_v001(**kwargs)


def test_chronological_split_policy_default_not_yet_defined() -> None:
    m = build_label_manifest_v001(**_kwargs())
    assert m["chronological_split_policy"] == "not_yet_defined"


def test_dtype_and_reference_policy_recorded() -> None:
    m = build_label_manifest_v001(**_kwargs())
    assert "dtype_policy" in m and isinstance(m["dtype_policy"], str)
    assert "reference_price_policy" in m
    assert "direction_threshold_policy" in m
