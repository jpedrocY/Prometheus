"""Offline tests for the Phase 4bn-W pre-v002 label-only execution wrapper.

These tests use only small synthetic fixtures and temporary directories.
They never read production data, never touch the sealed-test split, never
call the network, never read local ``data/microstructure`` artefacts, and
never create ``data/research`` outputs.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCRIPT_PATH = _REPO_ROOT / "scripts" / "phase4bn_w_compute_pre_v002_labels.py"


def _load_module():
    name = "phase4bn_w_mod"
    spec = importlib.util.spec_from_file_location(name, _SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    # Register before exec so dataclass annotation resolution can find the module.
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


W = _load_module()

# A few real upstream SHAs (referenced only as constants; no files are read).
FEAT_MAN_SHA = "4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52"
FEAT_GATE_SHA = "db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08"
NORM_MAN_SHA = "0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa"
NORM_GATE_SHA = "3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134"
RAW_MAN_SHA = "1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1"
FEAT_CONFIG_HASH = "0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c"
PUBLISHED_V002_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)


# ---------------------------------------------------------------------------
# Network-free / forbidden-import posture
# ---------------------------------------------------------------------------


def test_script_is_network_free() -> None:
    # Scan for forbidden *import statements* (the safety docstring legitimately
    # names ``.env`` / ``.mcp.json`` / Graphify as things it does NOT use).
    text = _SCRIPT_PATH.read_text(encoding="utf-8")
    for forbidden in (
        "import requests",
        "import socket",
        "import urllib",
        "import http.client",
        "import websocket",
        "import aiohttp",
        "import boto3",
        "from dotenv",
        "import dotenv",
    ):
        assert forbidden not in text, f"forbidden import {forbidden!r} present"


def test_identity_constants() -> None:
    assert W.PHASE_ID == "4bn-W"
    assert W.FAMILY_DIR_NAME == (
        "microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w"
    )
    assert W.SEGMENT_MANIFEST_BASENAME == W.FAMILY_DIR_NAME + ".json"
    assert W.SEGMENT_LABEL == "pre_v002_segment"
    assert W.EXPECTED_DATE_START == "2024-03-01"
    assert W.EXPECTED_DATE_END == "2024-11-30"
    assert W.EXPECTED_DATE_COUNT == 275
    assert W.EXPECTED_TOTAL_ROW_COUNT == 400_001_695
    assert W.EXPECTED_FEATURE_CONFIG_HASH == FEAT_CONFIG_HASH
    assert W.PUBLISHED_V002_FEATURE_CONFIG_HASH == PUBLISHED_V002_FEATURE_CONFIG_HASH


# ---------------------------------------------------------------------------
# Path construction
# ---------------------------------------------------------------------------


def _labels_root(tmp_path: Path) -> Path:
    root = tmp_path / "data" / "microstructure" / "labels"
    root.mkdir(parents=True, exist_ok=True)
    return root


def test_segment_parquet_path_layout(tmp_path: Path) -> None:
    labels_root = _labels_root(tmp_path)
    p = W.derive_label_segment_parquet_path(
        labels_root=labels_root, symbol="BTCUSDT", utc_date="2024-03-01"
    )
    rel = p.as_posix()
    assert W.FAMILY_DIR_NAME in rel
    assert rel.endswith("BTCUSDT/2024/03/BTCUSDT-labels-aggtrades-2024-03-01.parquet")
    assert "data/microstructure/labels/" in rel


def test_reject_published_v002_dir() -> None:
    # The segment dir must differ from the published __v002 dir and not be v003.
    assert W.FAMILY_DIR_NAME != W.PUBLISHED_V002_LABEL_DIR_NAME
    assert "v003" not in W.FAMILY_DIR_NAME


def test_reject_bad_date_and_symbol(tmp_path: Path) -> None:
    labels_root = _labels_root(tmp_path)
    # The path helper rejects a non-BTCUSDT / lowercase symbol.
    with pytest.raises(W.Phase4bnWValidationError):
        W.derive_label_segment_parquet_path(
            labels_root=labels_root, symbol="ethusdt", utc_date="2024-03-01"
        )
    # Malformed dates are rejected by the segment date guard.
    with pytest.raises(W.Phase4bnWValidationError):
        W._assert_date_in_segment("2024-3-1")


def test_segment_naming_guard() -> None:
    # Must not raise for the locked naming.
    W._assert_segment_naming()


def test_date_guard_rejects_terminal_and_sealed() -> None:
    W._assert_date_in_segment("2024-03-01")
    W._assert_date_in_segment("2024-11-30")
    for bad in ("2024-12-01", "2025-02-14", "2025-02-28", "2024-02-29", "2024-12-31"):
        with pytest.raises(W.Phase4bnWValidationError):
            W._assert_date_in_segment(bad)


# ---------------------------------------------------------------------------
# Segment-scoped label_config_hash builder
# ---------------------------------------------------------------------------


def _build_hash(**overrides) -> str:
    kwargs = dict(
        source_feature_manifest_sha256=FEAT_MAN_SHA,
        source_feature_layer_gate_report_sha256=FEAT_GATE_SHA,
        source_normalized_manifest_sha256=NORM_MAN_SHA,
        source_normalized_layer_gate_report_sha256=NORM_GATE_SHA,
        source_raw_manifest_sha256=RAW_MAN_SHA,
        feature_config_hash=FEAT_CONFIG_HASH,
    )
    kwargs.update(overrides)
    return W.build_label_config_hash_v002_pre_v002_segment(**kwargs)


def test_config_hash_is_deterministic() -> None:
    assert _build_hash() == _build_hash()
    assert len(_build_hash()) == 64


def test_config_hash_changes_with_feature_config_hash() -> None:
    other = "a" * 64
    assert _build_hash() != _build_hash(feature_config_hash=other)


def test_config_hash_changes_with_gate_shas() -> None:
    assert _build_hash() != _build_hash(
        source_feature_layer_gate_report_sha256="b" * 64
    )
    assert _build_hash() != _build_hash(
        source_normalized_layer_gate_report_sha256="c" * 64
    )


def test_config_hash_rejects_published_v002_feature_config() -> None:
    with pytest.raises(W.Phase4bnWValidationError):
        _build_hash(feature_config_hash=PUBLISHED_V002_FEATURE_CONFIG_HASH)


def test_config_hash_rejects_non_hex() -> None:
    with pytest.raises(W.Phase4bnWValidationError):
        _build_hash(source_raw_manifest_sha256="not-hex")


def test_segment_future_reference_policy_respecifies_envelope() -> None:
    pol = W._segment_future_reference_policy()
    assert "across_v002_90day_envelope" not in pol
    assert "across_pre_v002_segment_2024-03-01_to_2024-11-30" in pol


def test_config_hash_differs_from_v002_style_inputs() -> None:
    # The segment builder uses gate witnesses + segment label, so even with
    # the same six SHA inputs the hash is segment-distinct by construction
    # (the envelope clause + segment_label discriminator differ).
    seg = _build_hash()
    # Recompute a "v002-style" payload (no segment label, v002 envelope clause).
    payload = {
        "dataset_family": W.LABEL_DATASET_FAMILY_V002,
        "dataset_version": "v002",
        "label_schema_version": "v001",
        "feature_config_hash": FEAT_CONFIG_HASH,
    }
    v002ish = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    assert seg != v002ish


# ---------------------------------------------------------------------------
# Schema / lineage preservation
# ---------------------------------------------------------------------------


def test_label_schema_preserved_exactly() -> None:
    assert len(W.LABEL_SCHEMA_V002) == 40
    assert len(W.LABEL_LINEAGE_COLUMNS_V002) == 17
    assert len(W.LABEL_NAMES_V002) == 8
    assert len(W.LABEL_SUPPORT_COLUMN_NAMES_V002) == 14
    assert W.LABEL_SCHEMA_VERSION == "v001"
    assert W.LABEL_HORIZONS_V002 == ("1s", "5s", "15s", "60s")
    assert W.LABEL_HORIZON_MS_V002 == (1000, 5000, 15000, 60000)


def test_lineage_remap_keys() -> None:
    assert W.LINEAGE_REMAP_FEATURE_LAYER_GATE_KEY == "source_phase_4bm_j_gate_report_sha256"
    assert (
        W.LINEAGE_REMAP_NORMALIZED_LAYER_GATE_KEY
        == "source_feature_successor_state_sha256"
    )
    # Both re-mapped columns are part of the locked 17-column lineage set.
    assert W.LINEAGE_REMAP_FEATURE_LAYER_GATE_KEY in W.LABEL_LINEAGE_COLUMNS_V002
    assert W.LINEAGE_REMAP_NORMALIZED_LAYER_GATE_KEY in W.LABEL_LINEAGE_COLUMNS_V002


def test_forbidden_substring_guard_blocks_forbidden_columns() -> None:
    from prometheus.research.microstructure.labels_schema_v002 import (
        LabelSchemaErrorV002,
    )

    with pytest.raises(LabelSchemaErrorV002):
        W.assert_no_forbidden_label_substrings_v002(("forward_log_return_1s", "pnl_total"))
    # The real schema must pass.
    W.assert_no_forbidden_label_substrings_v002(W.LABEL_SCHEMA_V002)


# ---------------------------------------------------------------------------
# Manifest field contract
# ---------------------------------------------------------------------------


def _good_manifest() -> dict:
    """A minimal-but-complete valid label segment manifest for contract tests."""
    horizons = list(W.LABEL_HORIZONS_V002)
    per_day = [
        {
            "date": "2024-03-01",
            "symbol": "BTCUSDT",
            "label_parquet_path": (
                f"microstructure/labels/{W.FAMILY_DIR_NAME}/BTCUSDT/2024/03/"
                "BTCUSDT-labels-aggtrades-2024-03-01.parquet"
            ),
            "label_parquet_sha256": "0" * 64,
            "label_parquet_size_bytes": 1000,
            "row_count": 100,
            "per_horizon_censored_counts": {h: 0 for h in horizons},
            "invalid_price_row_count": 0,
            "label_sidecar_path": "microstructure/labels/x.sha256",
            "label_sidecar_sha256": "1" * 64,
            "label_sidecar_size_bytes": 100,
            "paired_source_feature_parquet_sha256": "2" * 64,
            "paired_source_normalized_parquet_sha256": "3" * 64,
            "status": "produced_verified",
        }
    ]
    return {
        "dataset_family": W.LABEL_FAMILY_ID,
        "dataset_version": "v002",
        "version": "v002",
        "label_schema_version": "v001",
        "segment_label": "pre_v002_segment",
        "data_family": "aggTrades",
        "symbol": "BTCUSDT",
        "symbol_list": ["BTCUSDT"],
        "market": "usdm_futures",
        "dataset_category": "labels",
        "label_family_id": W.LABEL_FAMILY_ID,
        "phase": "4bn-W",
        "phase_id": "phase-4bn-w",
        "source_phase_boundary": "4bn-T",
        "created_at_unix_ms": 1,
        "created_at_utc": "2026-06-05T00:00:00+00:00",
        "code_commit_sha": "unknown",
        "base_commit_sha": W.BASE_COMMIT_SHA_4BN_V_FINAL,
        "column_count": 40,
        "lineage_column_count": 17,
        "label_column_count": 8,
        "support_column_count": 14,
        "schema_column_list": list(W.LABEL_SCHEMA_V002),
        "lineage_column_list": list(W.LABEL_LINEAGE_COLUMNS_V002),
        "label_list": list(W.LABEL_NAMES_V002),
        "support_column_list": list(W.LABEL_SUPPORT_COLUMN_NAMES_V002),
        "dtype_policy": W.DTYPE_POLICY_V002,
        "anchor_policy": W.ANCHOR_POLICY_V002,
        "future_reference_policy": W._segment_future_reference_policy(),
        "direction_threshold_policy": W.DIRECTION_THRESHOLD_POLICY_V002,
        "null_censoring_policy": W.NULL_CENSORING_POLICY_V002,
        "horizon_list": horizons,
        "horizon_ms_list": list(W.LABEL_HORIZON_MS_V002),
        "forbidden_label_column_substrings": list(
            W.FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002
        ),
        "label_config_hash": "d" * 64,
        "label_config_hash_input_fields": list(W.LABEL_CONFIG_HASH_INPUT_FIELDS),
        "feature_config_hash": FEAT_CONFIG_HASH,
        "lineage_column_reinterpretation": {
            W.LINEAGE_REMAP_FEATURE_LAYER_GATE_KEY: {
                "segment_meaning": "feature_layer_gate_report",
                "bound_artefact": "phase_4bn_t_feature_layer_gate_report",
                "value": FEAT_GATE_SHA,
            },
            W.LINEAGE_REMAP_NORMALIZED_LAYER_GATE_KEY: {
                "segment_meaning": "non_eligible_admissibility_witness",
                "bound_artefact": "phase_4bn_p_normalized_layer_gate_report",
                "value": NORM_GATE_SHA,
            },
        },
        "date_start": "2024-03-01",
        "date_end": "2024-11-30",
        "date_count": 275,
        "date_list": ["2024-03-01"],
        "expected_file_count": 275,
        "produced_file_count": 275,
        "total_row_count": 400_001_695,
        "total_footprint_bytes": 123,
        "per_day_outputs": per_day,
        "envelope_terminal_unix_ms": 1733011199000,
        "envelope_terminal_utc_date": "2024-11-30",
        "censored_per_horizon": {h: 0 for h in horizons},
        "invalid_price_row_count": 0,
        "source_feature_dataset_family": W.SOURCE_FEATURE_DATASET_FAMILY,
        "source_feature_dataset_version": "v002",
        "source_feature_segment_manifest_path": "data/microstructure/manifests/x.json",
        "source_feature_segment_manifest_sha256": FEAT_MAN_SHA,
        "source_feature_segment_manifest_sidecar_sha256": "5" * 64,
        "source_feature_layer_gate_report_path": "data/microstructure/gate-reports/x.json",
        "source_feature_layer_gate_report_sha256": FEAT_GATE_SHA,
        "source_normalized_dataset_family": W.SOURCE_NORMALIZED_DATASET_FAMILY,
        "source_normalized_dataset_version": "v002",
        "source_normalized_segment_manifest_path": "data/microstructure/manifests/y.json",
        "source_normalized_segment_manifest_sha256": NORM_MAN_SHA,
        "source_normalized_segment_manifest_sidecar_sha256": "6" * 64,
        "source_normalized_layer_gate_report_path": "data/microstructure/gate-reports/y.json",
        "source_normalized_layer_gate_report_sha256": NORM_GATE_SHA,
        "source_raw_segment_manifest_path": "data/microstructure/manifests/raw.json",
        "source_raw_segment_manifest_sha256": RAW_MAN_SHA,
        "source_feature_schema_version": "FEATURE_SCHEMA_V002",
        "source_normalized_schema_version": "NORMALIZED_SCHEMA_V001",
        "source_eligibility_posture": "non_eligible_gate_passed_pending",
        "existing_v002_label_reference": {
            "path": W.PUBLISHED_V002_LABEL_MANIFEST_REL,
            "window_start": "2024-12-01",
            "window_end": "2025-02-28",
            "read": False,
            "mutated": False,
        },
        "full_intended_envelope_start": "2024-03-01",
        "full_intended_envelope_end": "2025-02-28",
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "chronological_split_policy": "not_yet_defined",
        "governance_labels": {
            "labels": "allowed_by_future_phase_only",
            "targets": "allowed_by_future_phase_only",
            "ml": "forbidden",
            "diagnostics": "forbidden",
            "strategy": "forbidden",
            "backtest": "forbidden",
            "acquisition": "unauthorized",
        },
        "no_successor_authorization": True,
        "boundary_confirmations": {
            "no_ml": True,
            "phase_4aw_flip_research_eligible_invariant_preserved": True,
        },
        "non_authorization_flags": {
            "successor_authorization_after": False,
            "ml_authorized": False,
            "stage_5_label_cleared": False,
        },
        "v002_terminal_window_mode": "by_reference",
        "existing_v002_terminal_window": {
            "read": False,
            "feature_normalized_raw_dates_read": False,
        },
        "sealed_test_split_touched": False,
        "existing_v002_sealed_test_split": {"touched": False},
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        "label_computation": "non_eligible_pre_v002_segment",
        "ml_use": "forbidden",
        "diagnostics_use": "forbidden",
        "strategy_use": "forbidden",
        "backtest_use": "forbidden",
        "partitioning_rule": "<SYMBOL>/<YYYY>/<MM>/",
        "primary_key": ["symbol", "utc_date", "agg_trade_id", "row_index"],
        "storage_format": "parquet_zstd",
        "sidecar_policy": "canonical_two_space_sha256",
        "budget_witnesses": {"hard_caps_crossed": False},
    }


def test_manifest_contract_accepts_good_manifest() -> None:
    W.assert_manifest_field_contract(_good_manifest())


def test_manifest_contract_rejects_research_eligible_true() -> None:
    m = _good_manifest()
    m["research_eligible"] = True
    with pytest.raises(W.Phase4bnWValidationError):
        W.assert_manifest_field_contract(m)


def test_manifest_contract_rejects_eligible_status() -> None:
    m = _good_manifest()
    m["eligibility_gate_status"] = "eligible"
    with pytest.raises(W.Phase4bnWValidationError):
        W.assert_manifest_field_contract(m)


def test_manifest_contract_rejects_published_config_hash() -> None:
    m = _good_manifest()
    m["feature_config_hash"] = PUBLISHED_V002_FEATURE_CONFIG_HASH
    with pytest.raises(W.Phase4bnWValidationError):
        W.assert_manifest_field_contract(m)


def test_manifest_contract_rejects_forbidden_field() -> None:
    m = _good_manifest()
    m["model_score_field"] = 1.0
    with pytest.raises(W.Phase4bnWValidationError):
        W.assert_manifest_field_contract(m)


def test_manifest_contract_rejects_split_policy_change() -> None:
    m = _good_manifest()
    m["chronological_split_policy"] = "time_ordered_70_15_15"
    with pytest.raises(W.Phase4bnWValidationError):
        W.assert_manifest_field_contract(m)


def test_manifest_contract_rejects_authorized_flag() -> None:
    m = _good_manifest()
    m["non_authorization_flags"]["ml_authorized"] = True
    with pytest.raises(W.Phase4bnWValidationError):
        W.assert_manifest_field_contract(m)


def test_manifest_contract_requires_governance_forbidden() -> None:
    m = _good_manifest()
    m["governance_labels"]["ml"] = "allowed"
    with pytest.raises(W.Phase4bnWValidationError):
        W.assert_manifest_field_contract(m)


# ---------------------------------------------------------------------------
# Budget caps
# ---------------------------------------------------------------------------


def test_budget_caps_inherited() -> None:
    assert W.LABEL_WARN_BYTES == 75 * W.GIB
    assert W.LABEL_HARD_BYTES == 125 * W.GIB
    assert W.RUNTIME_HARD_SECONDS == 8 * 3600
    assert W.TEMP_HARD_BYTES == 100 * W.GIB
    assert W.TOTAL_STACK_HARD_BYTES == 300 * W.GIB
    assert W.D_FREE_FLOOR_BYTES == 500 * W.GIB
    assert W.D_FREE_MIN_BYTES == 350 * W.GIB


def test_enforce_budgets_hard_cap_label() -> None:
    with pytest.raises(W.Phase4bnWValidationError):
        W._enforce_budgets(
            running_label_bytes=W.LABEL_HARD_BYTES + 1,
            elapsed=10,
            d_free=W.D_FREE_MIN_BYTES + 1,
            temp_peak=0,
            warnings_crossed=[],
        )


def test_enforce_budgets_hard_cap_runtime() -> None:
    with pytest.raises(W.Phase4bnWValidationError):
        W._enforce_budgets(
            running_label_bytes=0,
            elapsed=W.RUNTIME_HARD_SECONDS + 1,
            d_free=W.D_FREE_MIN_BYTES + 1,
            temp_peak=0,
            warnings_crossed=[],
        )


def test_enforce_budgets_d_free_floor() -> None:
    with pytest.raises(W.Phase4bnWValidationError):
        W._enforce_budgets(
            running_label_bytes=0,
            elapsed=10,
            d_free=W.D_FREE_MIN_BYTES - 1,
            temp_peak=0,
            warnings_crossed=[],
        )


def test_enforce_budgets_records_warnings() -> None:
    warns: list[str] = []
    W._enforce_budgets(
        running_label_bytes=W.LABEL_WARN_BYTES + 1,
        elapsed=W.RUNTIME_WARN_SECONDS + 1,
        d_free=W.D_FREE_MIN_BYTES + 1,
        temp_peak=W.TEMP_WARN_BYTES + 1,
        warnings_crossed=warns,
    )
    assert "label_warn" in warns
    assert "runtime_warn" in warns
    assert "temp_warn" in warns


# ---------------------------------------------------------------------------
# Non-eligible-source precondition (gate report verification)
# ---------------------------------------------------------------------------


def _write_canonical(path: Path, obj: dict) -> str:
    payload = (
        json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    path.write_bytes(payload)
    return hashlib.sha256(payload).hexdigest()


def _good_gate(sha_link_field: str, manifest_sha: str, n_checks: int) -> dict:
    return {
        "overall_status": "pass",
        "gate_result_state": "X_GATE_PASSED",
        "gate_verdict": "X_GATE_PASS",
        "checks": [{"status": "pass"} for _ in range(n_checks)],
        "segment_non_eligible": True,
        "research_eligible_after": False,
        "no_successor_authorization": True,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "published_v002_mutated": False,
        "data_committed": False,
        "eligibility_gate_status_after": "pending",
        sha_link_field: manifest_sha,
    }


def test_gate_report_pass(tmp_path: Path) -> None:
    gp = _good_gate("input_feature_manifest_sha256", FEAT_MAN_SHA, 27)
    path = tmp_path / "gate.json"
    sha = _write_canonical(path, gp)
    out = W._verify_gate_report(
        gate_report_path=path,
        expected_sha=sha,
        required_verdict="X_GATE_PASSED",
        expected_checks=27,
        manifest_link_field="input_feature_manifest_sha256",
        expected_manifest_sha=FEAT_MAN_SHA,
        kind="feature",
    )
    assert out == sha


def test_gate_report_rejects_research_eligible_after(tmp_path: Path) -> None:
    gp = _good_gate("input_feature_manifest_sha256", FEAT_MAN_SHA, 27)
    gp["research_eligible_after"] = True
    path = tmp_path / "gate.json"
    sha = _write_canonical(path, gp)
    with pytest.raises(W.Phase4bnWValidationError):
        W._verify_gate_report(
            gate_report_path=path,
            expected_sha=sha,
            required_verdict="X_GATE_PASSED",
            expected_checks=27,
            manifest_link_field="input_feature_manifest_sha256",
            expected_manifest_sha=FEAT_MAN_SHA,
            kind="feature",
        )


def test_gate_report_rejects_wrong_check_count(tmp_path: Path) -> None:
    gp = _good_gate("input_feature_manifest_sha256", FEAT_MAN_SHA, 20)
    path = tmp_path / "gate.json"
    sha = _write_canonical(path, gp)
    with pytest.raises(W.Phase4bnWValidationError):
        W._verify_gate_report(
            gate_report_path=path,
            expected_sha=sha,
            required_verdict="X_GATE_PASSED",
            expected_checks=27,
            manifest_link_field="input_feature_manifest_sha256",
            expected_manifest_sha=FEAT_MAN_SHA,
            kind="feature",
        )


def test_gate_report_rejects_sha_mismatch(tmp_path: Path) -> None:
    gp = _good_gate("input_feature_manifest_sha256", FEAT_MAN_SHA, 27)
    path = tmp_path / "gate.json"
    _write_canonical(path, gp)
    with pytest.raises(W.Phase4bnWValidationError):
        W._verify_gate_report(
            gate_report_path=path,
            expected_sha="f" * 64,
            required_verdict="X_GATE_PASSED",
            expected_checks=27,
            manifest_link_field="input_feature_manifest_sha256",
            expected_manifest_sha=FEAT_MAN_SHA,
            kind="feature",
        )


def test_identity_posture_helper_rejects_eligible() -> None:
    parsed = {
        "symbol_list": ["BTCUSDT"],
        "data_family": "aggTrades",
        "market": "usdm_futures",
        "dataset_family": W.SOURCE_FEATURE_DATASET_FAMILY,
        "dataset_version": "v002",
        "segment_label": "pre_v002_segment",
        "research_eligible": True,  # invalid
        "eligibility_gate_status": "pending",
        "v002_terminal_window_mode": "by_reference",
        "sealed_test_split_touched": False,
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        "date_start": "2024-03-01",
        "date_end": "2024-11-30",
        "date_count": 275,
        "expected_file_count": 275,
        "produced_file_count": 275,
        "total_row_count": 400_001_695,
    }
    with pytest.raises(W.Phase4bnWValidationError):
        W._verify_manifest_identity_and_posture(
            parsed, dataset_family=W.SOURCE_FEATURE_DATASET_FAMILY, kind="feature"
        )


def test_ms_to_utc_date() -> None:
    assert W._ms_to_utc_date(1709251200019) == "2024-03-01"
    # 1732924799872 ms == 2024-11-29 ... ensure a known 2024-11-30 ms maps right.
    assert W._ms_to_utc_date(1733011199000) == "2024-11-30"
