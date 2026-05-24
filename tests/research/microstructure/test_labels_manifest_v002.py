"""Phase 4bm-O v002 label manifest builder tests."""

from __future__ import annotations

from typing import Any

import pytest

from prometheus.research.microstructure.labels_manifest_v002 import (
    FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002,
    REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS_V002,
    REQUIRED_LABEL_GOVERNANCE_KEYS_V002,
    LabelManifestErrorV002,
    build_label_manifest_v002,
)
from prometheus.research.microstructure.labels_schema_v002 import (
    LABEL_HORIZONS_V002,
    LABEL_LINEAGE_COLUMNS_V002,
    LABEL_NAMES_V002,
    LABEL_SCHEMA_V002,
    LABEL_SUPPORT_COLUMN_NAMES_V002,
)


def _per_day_entry(date: str, idx: int) -> dict[str, Any]:
    return {
        "utc_date": date,
        "path": f"microstructure/labels/x/BTCUSDT-labels-aggtrades-{date}.parquet",
        "sha256": f"{idx:064x}",
        "sidecar_path": f"microstructure/labels/x/BTCUSDT-labels-aggtrades-{date}.parquet.sha256",
        "sidecar_sha256": f"{(idx + 1):064x}",
        "byte_size": 100 + idx,
        "row_count": 731_065,
        "per_horizon_censored_counts": dict.fromkeys(LABEL_HORIZONS_V002, 0),
        "invalid_price_row_count": 0,
        "source_feature_parquet_sha256": f"{(idx + 2):064x}",
    }


def _baseline_kwargs(*, date_count: int = 1) -> dict[str, Any]:
    dates = [f"2024-12-{i + 1:02d}" for i in range(date_count)]
    pdo = [_per_day_entry(d, i) for i, d in enumerate(dates)]
    return {
        "symbol": "BTCUSDT",
        "utc_date_start": dates[0],
        "utc_date_end": dates[-1],
        "date_count": date_count,
        "row_count": 731_065 * date_count,
        "per_day_outputs": pdo,
        "label_config_hash": "a" * 64,
        "feature_config_hash": "b" * 64,
        "envelope_terminal_unix_ms": 1_735_603_199_999,
        "invalid_price_row_count": 0,
        "censored_per_horizon": dict.fromkeys(LABEL_HORIZONS_V002, 1),
        "source_feature_manifest_sha256": "c" * 64,
        "source_feature_manifest_sidecar_sha256": "d" * 64,
        "source_feature_successor_state_sha256": "e" * 64,
        "source_feature_successor_state_sidecar_sha256": "f" * 64,
        "source_phase_4bm_j_gate_report_sha256": "0" * 64,
        "source_phase_4bm_j_gate_sidecar_sha256": "1" * 64,
        "source_normalized_manifest_sha256": "2" * 64,
        "source_normalized_manifest_sidecar_sha256": "3" * 64,
        "source_phase_4bm_f_derived_successor_state_sha256": "4" * 64,
        "source_phase_4bm_d_derived_gate_report_sha256": "5" * 64,
        "source_raw_manifest_sha256": "6" * 64,
        "source_acquisition_log_sha256": "7" * 64,
        "source_phase_4bl_e_raw_successor_state_sha256": "8" * 64,
        "source_phase_4bl_d_r_raw_gate_report_sha256": "9" * 64,
        "code_commit_sha": "unknown",
        "created_at_unix_ms": 1_700_000_000_000,
    }


# ---------------------------------------------------------------------------
# Required field presence + governance / boundary defaults
# ---------------------------------------------------------------------------


def test_manifest_required_top_level_fields_present() -> None:
    manifest = build_label_manifest_v002(**_baseline_kwargs())
    required = {
        "dataset_family",
        "dataset_version",
        "label_schema_version",
        "source_feature_dataset_family",
        "source_feature_dataset_version",
        "source_feature_manifest_sha256",
        "source_feature_manifest_sidecar_sha256",
        "source_feature_successor_state_sha256",
        "source_feature_successor_state_sidecar_sha256",
        "source_phase_4bm_j_gate_report_sha256",
        "source_phase_4bm_j_gate_sidecar_sha256",
        "source_normalized_manifest_sha256",
        "source_normalized_manifest_sidecar_sha256",
        "source_phase_4bm_f_derived_successor_state_sha256",
        "source_phase_4bm_d_derived_gate_report_sha256",
        "source_raw_manifest_sha256",
        "source_acquisition_log_sha256",
        "source_phase_4bl_e_raw_successor_state_sha256",
        "source_phase_4bl_d_r_raw_gate_report_sha256",
        "feature_config_hash",
        "label_config_hash",
        "symbol",
        "symbol_list",
        "utc_date_start",
        "utc_date_end",
        "date_count",
        "row_count",
        "column_count",
        "label_list",
        "support_column_list",
        "lineage_column_list",
        "schema_column_list",
        "horizon_list",
        "horizon_ms_list",
        "envelope_terminal_unix_ms",
        "nullable_tail_policy",
        "reference_price_policy",
        "direction_threshold_policy",
        "dtype_policy",
        "chronological_split_policy",
        "invalid_price_row_count",
        "censored_per_horizon",
        "per_day_outputs",
        "governance_labels",
        "boundary_confirmations",
        "research_eligible",
        "eligibility_gate_status",
        "label_family_research_use_authorized",
        "stage_5_label_cleared",
        "code_commit_sha",
        "created_at_unix_ms",
    }
    assert required.issubset(manifest.keys()), (
        f"missing keys: {required - manifest.keys()}"
    )


def test_manifest_governance_defaults_locked() -> None:
    manifest = build_label_manifest_v002(**_baseline_kwargs())
    assert manifest["research_eligible"] is False
    assert manifest["eligibility_gate_status"] == "pending"
    assert manifest["label_family_research_use_authorized"] is False
    assert manifest["stage_5_label_cleared"] is False
    assert manifest["chronological_split_policy"] == "not_yet_defined"
    gov = manifest["governance_labels"]
    assert gov["phase_id"] == "4bm-O"
    assert gov["labels"] == "allowed_by_future_phase_only"
    assert gov["targets"] == "allowed_by_future_phase_only"
    assert gov["ml"] == "forbidden"
    assert gov["strategy"] == "forbidden"
    assert gov["backtest"] == "forbidden"
    assert gov["acquisition"] == "unauthorized"
    assert gov["paper_shadow_live"] == "forbidden"
    assert gov["deployment"] == "forbidden"
    assert gov["exchange_write"] == "forbidden"


def test_manifest_boundary_confirmations_all_true() -> None:
    manifest = build_label_manifest_v002(**_baseline_kwargs())
    bc = manifest["boundary_confirmations"]
    for key in REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS_V002:
        assert bc[key] is True, f"boundary {key} not True"


def test_manifest_schema_introspection() -> None:
    manifest = build_label_manifest_v002(**_baseline_kwargs())
    assert manifest["dataset_family"] == "microstructure_labels_aggtrades_v001"
    assert manifest["dataset_version"] == "v002"
    assert manifest["label_schema_version"] == "v001"
    assert manifest["symbol"] == "BTCUSDT"
    assert manifest["symbol_list"] == ["BTCUSDT"]
    assert manifest["column_count"] == 40
    assert manifest["label_list"] == list(LABEL_NAMES_V002)
    assert manifest["support_column_list"] == list(LABEL_SUPPORT_COLUMN_NAMES_V002)
    assert manifest["lineage_column_list"] == list(LABEL_LINEAGE_COLUMNS_V002)
    assert manifest["schema_column_list"] == list(LABEL_SCHEMA_V002)
    assert manifest["horizon_list"] == ["1s", "5s", "15s", "60s"]
    assert manifest["horizon_ms_list"] == [1000, 5000, 15000, 60000]


def test_manifest_per_day_outputs_validated() -> None:
    manifest = build_label_manifest_v002(**_baseline_kwargs(date_count=3))
    assert len(manifest["per_day_outputs"]) == 3
    for entry in manifest["per_day_outputs"]:
        assert set(entry.keys()) >= {
            "utc_date",
            "path",
            "sha256",
            "sidecar_path",
            "sidecar_sha256",
            "byte_size",
            "row_count",
            "per_horizon_censored_counts",
            "invalid_price_row_count",
            "source_feature_parquet_sha256",
        }


# ---------------------------------------------------------------------------
# Validation rejections
# ---------------------------------------------------------------------------


def test_manifest_rejects_lower_case_symbol() -> None:
    kwargs = _baseline_kwargs()
    kwargs["symbol"] = "btcusdt"
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_rejects_non_btcusdt() -> None:
    kwargs = _baseline_kwargs()
    kwargs["symbol"] = "ETHUSDT"
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_rejects_bad_date() -> None:
    kwargs = _baseline_kwargs()
    kwargs["utc_date_start"] = "2024/12/01"
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_rejects_negative_row_count() -> None:
    kwargs = _baseline_kwargs()
    kwargs["row_count"] = -1
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_rejects_negative_envelope_terminal() -> None:
    kwargs = _baseline_kwargs()
    kwargs["envelope_terminal_unix_ms"] = 0
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_rejects_per_day_length_mismatch() -> None:
    kwargs = _baseline_kwargs(date_count=2)
    kwargs["date_count"] = 5
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_rejects_bad_censored_per_horizon_keys() -> None:
    kwargs = _baseline_kwargs()
    kwargs["censored_per_horizon"] = {"1s": 0, "5s": 0}
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_rejects_short_sha_in_lineage_field() -> None:
    kwargs = _baseline_kwargs()
    kwargs["source_feature_manifest_sha256"] = "abc"
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_rejects_overriding_locked_governance_key() -> None:
    kwargs = _baseline_kwargs()
    kwargs["extra_governance_labels"] = {"ml": "allowed"}
    with pytest.raises(LabelManifestErrorV002):
        build_label_manifest_v002(**kwargs)


def test_manifest_extra_governance_labels_allowed_when_unique() -> None:
    kwargs = _baseline_kwargs()
    kwargs["extra_governance_labels"] = {"custom_marker": "annotated"}
    manifest = build_label_manifest_v002(**kwargs)
    assert manifest["governance_labels"]["custom_marker"] == "annotated"


def test_required_governance_keys_constant() -> None:
    # Sanity: locked v002 governance contract.
    assert set(REQUIRED_LABEL_GOVERNANCE_KEYS_V002) >= {
        "phase_id",
        "labels",
        "targets",
        "ml",
        "strategy",
        "backtest",
        "acquisition",
        "paper_shadow_live",
        "deployment",
        "exchange_write",
    }


def test_forbidden_governance_values_constant() -> None:
    assert FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002["ml"] == frozenset({"allowed"})
    assert FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002["strategy"] == frozenset({"allowed"})


def test_manifest_aggregate_censored_counts_round_trip() -> None:
    kwargs = _baseline_kwargs()
    expected = {"1s": 10, "5s": 20, "15s": 30, "60s": 40}
    kwargs["censored_per_horizon"] = expected
    manifest = build_label_manifest_v002(**kwargs)
    assert manifest["censored_per_horizon"] == expected


def test_manifest_invalid_price_row_count_round_trip() -> None:
    kwargs = _baseline_kwargs()
    kwargs["invalid_price_row_count"] = 7
    manifest = build_label_manifest_v002(**kwargs)
    assert manifest["invalid_price_row_count"] == 7
