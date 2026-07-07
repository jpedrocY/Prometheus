"""Phase 4bn-AH — offline tests for the pre-v002 data-reading ML dataset builder.

These tests exercise the new data-reading builder's pure logic and fail-closed
guards against **synthetic in-memory fixtures and temp dirs only**. They read no
local dataset, and they do not invoke the heavy single run (which reads the real
275+275 partitions). The heavy run is exercised once, separately, by the
Phase 4bn-AH controlled run and recorded in the implementation report.
"""

from __future__ import annotations

import datetime as dt
import json

import pytest

from prometheus.research.microstructure import (
    pre_v002_ml_dataset_builder as builder,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_contract as contract,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_proof as proof,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_run as run_mod,
)
from prometheus.research.microstructure import (
    pre_v002_split_policy as sp,
)
from prometheus.research.microstructure.pre_v002_ml_dataset_run import (
    BuilderRunProof,
    PreV002MlDatasetRunError,
    RealBudgetPreflight,
)

# ---------------------------------------------------------------------------
# Budget preflight
# ---------------------------------------------------------------------------


def test_budget_preflight_passes_with_ample_free_space():
    pf = run_mod.evaluate_budget_preflight(1200.0)
    assert pf.passed is True
    assert pf.breaches == ()
    assert pf.is_placeholder is False
    assert pf.ran_preflight is True
    assert pf.measured_disk is True
    assert pf.d_drive_min_free_gib_before == 500
    assert pf.d_drive_fail_closed_during_gib == 350


def test_budget_preflight_fails_below_500_before():
    pf = run_mod.evaluate_budget_preflight(499.9)
    assert pf.passed is False
    assert pf.breaches and "before start" in pf.breaches[0]


def test_budget_thresholds_match_phase_4bn_l():
    assert run_mod.DERIVED_FOOTPRINT_WARN_GIB == 75
    assert run_mod.DERIVED_FOOTPRINT_HARD_GIB == 125
    assert run_mod.TOTAL_DERIVED_STACK_WARN_GIB == 250
    assert run_mod.TOTAL_DERIVED_STACK_HARD_GIB == 300
    assert run_mod.RUNTIME_WARN_HOURS == 4
    assert run_mod.RUNTIME_HARD_HOURS == 8
    assert run_mod.TEMP_WARN_GIB == 50
    assert run_mod.TEMP_HARD_GIB == 100
    assert run_mod.D_DRIVE_MIN_FREE_GIB_BEFORE == 500
    assert run_mod.D_DRIVE_FAIL_CLOSED_DURING_GIB == 350


def test_assert_budget_during_raises_below_floor(monkeypatch, tmp_path):
    monkeypatch.setattr(run_mod, "measure_d_free_gib", lambda *_a, **_k: 300.0)
    with pytest.raises(PreV002MlDatasetRunError):
        run_mod.assert_budget_during(tmp_path)


# ---------------------------------------------------------------------------
# Phase 4bb-F sidecars
# ---------------------------------------------------------------------------


def test_sidecar_roundtrip():
    line = run_mod.sidecar_line("a" * 64, "dataset_manifest.json")
    assert line == "a" * 64 + "  dataset_manifest.json\n"
    sha, name = run_mod.parse_sidecar(line)
    assert sha == "a" * 64
    assert name == "dataset_manifest.json"


@pytest.mark.parametrize(
    "bad",
    [
        "abc def.json",  # sha not 64-hex
        "a" * 64 + " single_space.json",  # single space
        "z" * 64 + "  x.json",  # non-hex
        "a" * 64 + "  ",  # missing name
    ],
)
def test_parse_sidecar_fails_closed(bad):
    with pytest.raises(PreV002MlDatasetRunError):
        run_mod.parse_sidecar(bad)


def test_write_json_with_sidecar_confined_to_dir(tmp_path):
    payload = {"b": 2, "a": 1}
    path = tmp_path / "artefact.json"
    digest, sidecar_name = run_mod.write_json_with_sidecar(path, payload)
    assert path.exists()
    assert (tmp_path / "artefact.json.sha256").exists()
    assert sidecar_name == "artefact.json.sha256"
    # sidecar records the artefact's real sha and canonical two-space form
    sha, name = run_mod.parse_sidecar((tmp_path / "artefact.json.sha256").read_text())
    assert sha == digest
    assert name == "artefact.json"
    # only the two intended files were created in the dir
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "artefact.json",
        "artefact.json.sha256",
    ]
    # deterministic, sorted-key JSON
    assert json.loads(path.read_text()) == payload


# ---------------------------------------------------------------------------
# Feature-list hash / boundary crossings
# ---------------------------------------------------------------------------


def test_feature_list_hash_is_deterministic_over_45_columns():
    h1 = run_mod.feature_list_hash()
    h2 = run_mod.feature_list_hash(contract.ALLOWED_FEATURE_COLUMNS)
    assert h1 == h2
    assert len(h1) == 64
    assert len(contract.ALLOWED_FEATURE_COLUMNS) == 45


def test_per_horizon_boundary_crossings_zero_for_realistic_maxima():
    max_train = int(
        dt.datetime(2024, 9, 30, 23, 59, 59, 999000, tzinfo=dt.UTC)
        .timestamp() * 1000
    )
    max_val = int(
        dt.datetime(2024, 11, 15, 23, 59, 59, 999000, tzinfo=dt.UTC)
        .timestamp() * 1000
    )
    out = run_mod.per_horizon_boundary_crossings(
        {sp.TRAIN: max_train, sp.VALIDATION: max_val}
    )
    assert out == {"1000ms": 0, "5000ms": 0, "15000ms": 0, "60000ms": 0}


# ---------------------------------------------------------------------------
# Run proof assembly + validation (reuses the skeleton conservative path)
# ---------------------------------------------------------------------------


def _valid_run_proof(**overrides) -> BuilderRunProof:
    base = dict(
        contract_name=contract.CONTRACT_NAME,
        amendment_id=contract.CONTRACT_AMENDMENT_ID,
        split=proof.SplitProof(split_policy_commit_sha="deadbeef"),
        alignment=proof.AlignmentProof(key_alignment_row_count=400_001_695),
        filtering=proof.FilteringProof(
            dropped_by_split_and_reason={"train": {"censored": 1}},
            targets_imputed=False,
        ),
        evaluation=proof.EvaluationPreregistrationProof(
            active_feature_list_hash=run_mod.feature_list_hash()
        ),
        non_authorization=proof.NonAuthorizationProof(),
        budget_preflight=RealBudgetPreflight(
            passed=True, d_free_gib_before=1200.0
        ),
        split_policy_commit_sha="deadbeef",
        active_feature_list_hash=run_mod.feature_list_hash(),
        output_namespace_path=run_mod.OUTPUT_NAMESPACE + "/",
        output_namespace_created=True,
        no_data_io=False,
        per_horizon_boundary_crossing_rows={
            "1000ms": 0,
            "5000ms": 0,
            "15000ms": 0,
            "60000ms": 0,
        },
    )
    base.update(overrides)
    return BuilderRunProof(**base)


def test_validate_builder_run_proof_accepts_valid_run():
    run_mod.validate_builder_run_proof(_valid_run_proof())


def test_run_proof_rejects_placeholder_budget():
    rp = _valid_run_proof(
        budget_preflight=proof.BudgetPreflightPlaceholder()  # type: ignore[arg-type]
    )
    with pytest.raises(PreV002MlDatasetRunError):
        run_mod.validate_builder_run_proof(rp)


def test_run_proof_rejects_failed_budget():
    rp = _valid_run_proof(
        budget_preflight=RealBudgetPreflight(
            passed=False, breaches=("low disk",), d_free_gib_before=100.0
        )
    )
    with pytest.raises(PreV002MlDatasetRunError):
        run_mod.validate_builder_run_proof(rp)


def test_run_proof_rejects_no_data_io_true():
    with pytest.raises(PreV002MlDatasetRunError):
        run_mod.validate_builder_run_proof(_valid_run_proof(no_data_io=True))


def test_run_proof_rejects_output_namespace_not_created():
    with pytest.raises(PreV002MlDatasetRunError):
        run_mod.validate_builder_run_proof(
            _valid_run_proof(output_namespace_created=False)
        )


def test_run_proof_rejects_nonzero_boundary_crossing():
    with pytest.raises(PreV002MlDatasetRunError):
        run_mod.validate_builder_run_proof(
            _valid_run_proof(
                per_horizon_boundary_crossing_rows={
                    "1000ms": 0,
                    "5000ms": 0,
                    "15000ms": 1,
                    "60000ms": 0,
                }
            )
        )


def test_run_proof_rejects_v002_read_flag():
    # Conservative-posture violations are caught by the reused skeleton validator,
    # which raises the parent PreV002MlDatasetError (the run error is a subclass).
    rp = _valid_run_proof(
        split=proof.SplitProof(v002_terminal_window_read=True)
    )
    with pytest.raises(builder.PreV002MlDatasetError):
        run_mod.validate_builder_run_proof(rp)


def test_run_proof_rejects_nonzero_test_rows():
    rp = _valid_run_proof(split=proof.SplitProof(test_rows_loaded=5))
    with pytest.raises(builder.PreV002MlDatasetError):
        run_mod.validate_builder_run_proof(rp)


def test_run_proof_rejects_imputed_targets():
    rp = _valid_run_proof(
        filtering=proof.FilteringProof(targets_imputed=True)
    )
    with pytest.raises(builder.PreV002MlDatasetError):
        run_mod.validate_builder_run_proof(rp)


def test_run_proof_rejects_any_true_non_authorization_flag():
    rp = _valid_run_proof(
        non_authorization=proof.NonAuthorizationProof(ml_authorized=True)
    )
    with pytest.raises(builder.PreV002MlDatasetError):
        run_mod.validate_builder_run_proof(rp)


# ---------------------------------------------------------------------------
# Reused skeleton fail-closed guards (the run binds these before reading)
# ---------------------------------------------------------------------------


def test_run_reuses_v002_hash_rejection():
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_manifest_hashes(
            normalized_like={"manifest_sha256": contract.EXPECTED_NORMALIZED_MANIFEST_SHA256},
            feature_like={
                "manifest_sha256": contract.EXPECTED_FEATURE_MANIFEST_SHA256,
                "feature_config_hash": contract.REJECTED_V002_FEATURE_CONFIG_HASH,
            },
            label_like={
                "manifest_sha256": contract.EXPECTED_LABEL_MANIFEST_SHA256,
                "label_config_hash": contract.EXPECTED_LABEL_CONFIG_HASH,
            },
        )


def test_run_reuses_source_scope_v002_rejection():
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_source_scope(
            {
                "symbol": "BTCUSDT",
                "market": "binance_usdm_futures",
                "source_family": "aggTrades",
                "start_date": "2024-03-01",
                "end_date": "2024-11-30",
                "contains_v002_terminal": True,
            }
        )


# ---------------------------------------------------------------------------
# One-run guard (no heavy read; monkeypatched REPO_ROOT)
# ---------------------------------------------------------------------------


def test_run_refuses_when_dataset_already_built(monkeypatch, tmp_path):
    monkeypatch.setattr(run_mod, "REPO_ROOT", tmp_path)
    out = tmp_path / run_mod.OUTPUT_NAMESPACE
    out.mkdir(parents=True)
    (out / "dataset_manifest.json").write_text("{}", encoding="utf-8")
    with pytest.raises(PreV002MlDatasetRunError) as exc:
        run_mod.run(progress=False)
    assert "rerun requires separate operator authorization" in str(exc.value)


def test_output_namespace_is_gitignored_research_path():
    assert run_mod.OUTPUT_NAMESPACE == (
        "data/research/microstructure/ml_datasets/pre_v002_contract_v001"
    )
    assert run_mod.OUTPUT_NAMESPACE.startswith("data/research/")
