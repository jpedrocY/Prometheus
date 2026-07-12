"""Phase 4bn-AQ — offline tests for the long-horizon ML dataset run proof.

Assemble a synthetic Phase 4bn-AQ run proof and exercise every fail-closed
branch of :func:`validate_builder_run_proof`, plus the no-model / all-flags-False
invariants. No data is read; the heavy run is exercised separately.
"""

from __future__ import annotations

import pytest

from prometheus.research.microstructure import (
    build_longhorizon_ml_dataset_v001 as run_mod,
)
from prometheus.research.microstructure import (
    longhorizon_ml_dataset_contract_v001 as contract,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_builder as builder,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_proof as proof,
)
from prometheus.research.microstructure.build_longhorizon_ml_dataset_v001 import (
    BuilderRunProof,
    LongHorizonMlDatasetRunError,
    RealBudgetPreflight,
)

_ZERO_CROSSINGS = {
    f"{sp}:{h}": 0
    for sp in ("train", "validation")
    for h in contract.HORIZONS
}


def _valid_run_proof(**overrides) -> BuilderRunProof:
    base = dict(
        contract_name=contract.CONTRACT_NAME,
        amendment_id=contract.CONTRACT_AMENDMENT_ID,
        split=proof.SplitProof(split_policy_commit_sha="deadbeef"),
        alignment=proof.AlignmentProof(key_alignment_row_count=400_001_695),
        filtering=proof.FilteringProof(
            dropped_by_split_and_reason={"train": {"censored": 0}},
            targets_imputed=False,
        ),
        evaluation=proof.EvaluationPreregistrationProof(
            active_feature_list_hash=run_mod.feature_list_hash()
        ),
        non_authorization=proof.NonAuthorizationProof(),
        budget_preflight=RealBudgetPreflight(passed=True, d_free_gib_before=1200.0),
        split_policy_commit_sha="deadbeef",
        active_feature_list_hash=run_mod.feature_list_hash(),
        label_family=contract.LABEL_FAMILY,
        label_config_hash=contract.LABEL_CONFIG_HASH,
        output_namespace_path=run_mod.OUTPUT_NAMESPACE + "/",
        output_namespace_created=True,
        no_data_io=False,
        per_horizon_boundary_crossing_rows=dict(_ZERO_CROSSINGS),
    )
    base.update(overrides)
    return BuilderRunProof(**base)


def test_validate_accepts_valid_run():
    run_mod.validate_builder_run_proof(_valid_run_proof())


def test_rejects_placeholder_budget():
    rp = _valid_run_proof(
        budget_preflight=proof.BudgetPreflightPlaceholder()  # type: ignore[arg-type]
    )
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.validate_builder_run_proof(rp)


def test_rejects_failed_budget():
    rp = _valid_run_proof(
        budget_preflight=RealBudgetPreflight(
            passed=False, breaches=("low disk",), d_free_gib_before=100.0
        )
    )
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.validate_builder_run_proof(rp)


def test_rejects_no_data_io_true():
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.validate_builder_run_proof(_valid_run_proof(no_data_io=True))


def test_rejects_output_namespace_not_created():
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.validate_builder_run_proof(
            _valid_run_proof(output_namespace_created=False)
        )


def test_rejects_wrong_label_family():
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.validate_builder_run_proof(
            _valid_run_proof(label_family="microstructure_labels_aggtrades_v001")
        )


def test_rejects_wrong_label_config_hash():
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.validate_builder_run_proof(
            _valid_run_proof(label_config_hash="0" * 64)
        )


def test_rejects_nonzero_boundary_crossing():
    crossings = dict(_ZERO_CROSSINGS)
    crossings["train:5m"] = 1
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.validate_builder_run_proof(
            _valid_run_proof(per_horizon_boundary_crossing_rows=crossings)
        )


def test_rejects_nonzero_alignment_mismatch():
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.validate_builder_run_proof(
            _valid_run_proof(
                alignment=proof.AlignmentProof(
                    key_alignment_row_count=400_001_695, mismatched_rows=3
                )
            )
        )


def test_rejects_v002_read_flag():
    rp = _valid_run_proof(split=proof.SplitProof(v002_terminal_window_read=True))
    with pytest.raises(builder.PreV002MlDatasetError):
        run_mod.validate_builder_run_proof(rp)


def test_rejects_nonzero_test_rows():
    rp = _valid_run_proof(split=proof.SplitProof(test_rows_loaded=5))
    with pytest.raises(builder.PreV002MlDatasetError):
        run_mod.validate_builder_run_proof(rp)


def test_rejects_imputed_targets():
    rp = _valid_run_proof(filtering=proof.FilteringProof(targets_imputed=True))
    with pytest.raises(builder.PreV002MlDatasetError):
        run_mod.validate_builder_run_proof(rp)


def test_rejects_any_true_non_authorization_flag():
    rp = _valid_run_proof(
        non_authorization=proof.NonAuthorizationProof(ml_authorized=True)
    )
    with pytest.raises(builder.PreV002MlDatasetError):
        run_mod.validate_builder_run_proof(rp)


def test_no_model_invariant_flags_all_false_in_contract():
    assert all(v is False for v in contract.NON_AUTHORIZATION_FLAGS.values())
