"""Phase 4bn-AJ — offline tests for the pre-v002 fixed baseline runner.

Synthetic-fixture / pure-logic tests only. No real feature/label Parquet is read,
no v002 terminal / sealed test is touched, no model is trained on real data, and
no output is written outside a pytest ``tmp_path``. The heavy streaming ``run()``
orchestration is exercised end-to-end only by the single authorized controlled
run (recorded in the Phase 4bn-AJ implementation report), not by this suite.
"""

from __future__ import annotations

import numpy as np
import pytest

from prometheus.research.microstructure import ml_baseline_design_v002 as design
from prometheus.research.microstructure import pre_v002_fixed_baseline_run as aj
from prometheus.research.microstructure import pre_v002_ml_dataset_contract as contract
from prometheus.research.microstructure import pre_v002_ml_dataset_run as ah

# ---------------------------------------------------------------------------
# Synthetic AH artefact namespace helpers
# ---------------------------------------------------------------------------


def _synthetic_transform() -> dict:
    per = {}
    for c in contract.ALLOWED_FEATURE_COLUMNS:
        per[c] = {
            "train_mean": 1.0,
            "train_std": 2.0,
            "train_count": 304_816_127,
            "train_null_count": 0,
        }
    return {
        "fit_split": "train",
        "standardization_rule": contract.STANDARDIZATION_RULE,
        "standardization_epsilon": contract.STANDARDIZATION_EPSILON,
        "imputation_rule": contract.IMPUTATION_RULE,
        "imputation_fill_value": contract.IMPUTATION_FILL_VALUE,
        "standardize_boolean_flags": contract.STANDARDIZE_BOOLEAN_FLAGS,
        "feature_count": 45,
        "feature_list_hash": ah.feature_list_hash(),
        "per_feature": per,
    }


def _synthetic_manifest() -> dict:
    return {
        "streamed_row_count": contract.EXPECTED_ROW_COUNT,
        "feature_list_hash": ah.feature_list_hash(),
        "split_raw_rows": {
            "train": 304_816_127, "embargo": 3_071_370,
            "validation": 68_578_296, "holdout": 23_535_902,
        },
        "split_filtered_rows": {
            "train": 304_816_127, "validation": 68_578_296, "holdout": 23_535_860,
        },
        "split_class_counts": {
            "train": {"-1": 150_077_008, "0": 3_590_082, "1": 151_149_037},
            "validation": {"-1": 33_619_134, "0": 1_013_759, "1": 33_945_403},
            "holdout": {"-1": 11_532_338, "0": 228_247, "1": 11_775_275},
        },
        "dropped_by_split_and_reason": {
            "holdout": {
                "censored": 42, "invalid_price": 0, "null_direction": 0, "null_log_return": 0,
            },
            "train": {
                "censored": 0, "invalid_price": 0, "null_direction": 0, "null_log_return": 0,
            },
            "validation": {
                "censored": 0, "invalid_price": 0, "null_direction": 0, "null_log_return": 0,
            },
        },
        "dependence_caveat": "overlapping 15s labels; rows are NOT independent.",
    }


def _synthetic_proof() -> dict:
    return {
        "active_feature_list_hash": ah.feature_list_hash(),
        "per_horizon_boundary_crossing_rows": {
            "1000ms": 0, "5000ms": 0, "15000ms": 0, "60000ms": 0,
        },
        "split": {
            "v002_terminal_window_read": False,
            "sealed_test_split_touched": False,
            "test_rows_loaded": 0,
            "no_random": True, "no_shuffle": True, "no_kfold": True, "no_bootstrap": True,
            "no_embargo_date_used": True,
        },
    }


# ---------------------------------------------------------------------------
# AH artefact verification (fail-closed)
# ---------------------------------------------------------------------------


def test_load_and_verify_ah_artefacts_passes(tmp_path, monkeypatch):
    ns = tmp_path / "ah_ns"
    ns.mkdir()
    for name, payload in (
        ("dataset_manifest.json", _synthetic_manifest()),
        ("train_only_transform.json", _synthetic_transform()),
        ("split_index.json", {"per_date": [{"date": f"d{i}"} for i in range(275)]}),
        ("leakage_split_integrity_proof.json", _synthetic_proof()),
    ):
        ah.write_json_with_sidecar(ns / name, payload)
    monkeypatch.setattr(aj, "REPO_ROOT", tmp_path)
    art = aj.load_and_verify_ah_artefacts(namespace="ah_ns")
    assert art.manifest["streamed_row_count"] == contract.EXPECTED_ROW_COUNT
    assert art.transform["fit_split"] == "train"


def test_missing_artefact_fails_closed(tmp_path, monkeypatch):
    ns = tmp_path / "ah_ns"
    ns.mkdir()
    monkeypatch.setattr(aj, "REPO_ROOT", tmp_path)
    with pytest.raises(aj.PreV002FixedBaselineError, match="missing AH artefact"):
        aj.load_and_verify_ah_artefacts(namespace="ah_ns")


def test_mismatched_sidecar_fails_closed(tmp_path, monkeypatch):
    ns = tmp_path / "ah_ns"
    ns.mkdir()
    for name, payload in (
        ("dataset_manifest.json", _synthetic_manifest()),
        ("train_only_transform.json", _synthetic_transform()),
        ("split_index.json", {"per_date": [{"date": f"d{i}"} for i in range(275)]}),
        ("leakage_split_integrity_proof.json", _synthetic_proof()),
    ):
        ah.write_json_with_sidecar(ns / name, payload)
    # Corrupt one artefact's body without updating its sidecar.
    p = ns / "dataset_manifest.json"
    p.write_text(p.read_text(encoding="utf-8") + " ", encoding="utf-8")
    monkeypatch.setattr(aj, "REPO_ROOT", tmp_path)
    with pytest.raises(aj.PreV002FixedBaselineError, match="!= sidecar"):
        aj.load_and_verify_ah_artefacts(namespace="ah_ns")


def test_proof_flag_regression_fails_closed(tmp_path, monkeypatch):
    ns = tmp_path / "ah_ns"
    ns.mkdir()
    bad_proof = _synthetic_proof()
    bad_proof["split"]["test_rows_loaded"] = 5
    for name, payload in (
        ("dataset_manifest.json", _synthetic_manifest()),
        ("train_only_transform.json", _synthetic_transform()),
        ("split_index.json", {"per_date": [{"date": f"d{i}"} for i in range(275)]}),
        ("leakage_split_integrity_proof.json", bad_proof),
    ):
        ah.write_json_with_sidecar(ns / name, payload)
    monkeypatch.setattr(aj, "REPO_ROOT", tmp_path)
    with pytest.raises(aj.PreV002FixedBaselineError, match="test_rows_loaded"):
        aj.load_and_verify_ah_artefacts(namespace="ah_ns")


def test_manifest_count_regression_fails_closed(tmp_path, monkeypatch):
    ns = tmp_path / "ah_ns"
    ns.mkdir()
    bad_man = _synthetic_manifest()
    bad_man["split_filtered_rows"]["holdout"] = 999
    for name, payload in (
        ("dataset_manifest.json", bad_man),
        ("train_only_transform.json", _synthetic_transform()),
        ("split_index.json", {"per_date": [{"date": f"d{i}"} for i in range(275)]}),
        ("leakage_split_integrity_proof.json", _synthetic_proof()),
    ):
        ah.write_json_with_sidecar(ns / name, payload)
    monkeypatch.setattr(aj, "REPO_ROOT", tmp_path)
    with pytest.raises(aj.PreV002FixedBaselineError, match="split_filtered_rows"):
        aj.load_and_verify_ah_artefacts(namespace="ah_ns")


# ---------------------------------------------------------------------------
# Standardizer (applies the AH transform; boolean passthrough; imputation)
# ---------------------------------------------------------------------------


def test_standardizer_applies_train_transform_and_imputes(tmp_path):
    std = aj.build_standardizer(_synthetic_transform())
    assert std.columns == tuple(contract.ALLOWED_FEATURE_COLUMNS)
    x = np.ones((3, 45), dtype=np.float64) * 5.0
    out = std.transform(x)
    # Non-boolean columns: (5 - 1) / max(2, eps) = 2.0.
    bool_cols = frozenset(design.BOOLEAN_FEATURE_COLUMN_NAMES)
    for j, c in enumerate(std.columns):
        if c in bool_cols:
            assert np.allclose(out[:, j], 5.0)  # passthrough
        else:
            assert np.allclose(out[:, j], 2.0)


def test_standardizer_imputes_nan_to_fill_value(tmp_path):
    std = aj.build_standardizer(_synthetic_transform())
    x = np.full((2, 45), np.nan, dtype=np.float64)
    out = std.transform(x)
    # Non-boolean: (0 - 1)/2 = -0.5; boolean: passthrough 0.
    bool_cols = frozenset(design.BOOLEAN_FEATURE_COLUMN_NAMES)
    for j, c in enumerate(std.columns):
        if c in bool_cols:
            assert np.allclose(out[:, j], 0.0)
        else:
            assert np.allclose(out[:, j], -0.5)


def test_persistence_index_points_at_15s_pastwindow():
    std = aj.build_standardizer(_synthetic_transform())
    assert std.columns[std.persistence_index] == aj.PERSISTENCE_FEATURE
    assert aj.PERSISTENCE_FEATURE == "rolling_log_return_past_window_15s"


# ---------------------------------------------------------------------------
# Cost realism (descriptive; share > 16 bps exact; approx quantiles)
# ---------------------------------------------------------------------------


def test_cost_realism_share_above_thresholds_exact():
    cr = aj.CostRealism()
    # returns in decimal: 4 bps, 12 bps, 20 bps, 40 bps (as log-return).
    rets = np.array([4, 12, 20, 40], dtype=np.float64) / 10_000.0
    cr.update(rets)
    d = cr.as_dict()
    assert d["n_rows"] == 4
    # > 16 bps: 20 and 40 → 2/4 = 0.5
    assert d["share_abs_return_gt_16bps_round_trip"] == pytest.approx(0.5)
    # > 8 bps: 12, 20, 40 → 3/4 = 0.75
    assert d["share_abs_return_gt_8bps_one_way"] == pytest.approx(0.75)
    assert d["max_abs_return_bps"] == pytest.approx(40.0)


# ---------------------------------------------------------------------------
# Verdict logic (Phase 4bn-AE §16/§17) with synthetic metrics
# ---------------------------------------------------------------------------


def _base_inputs(**over) -> aj.VerdictInputs:
    d = dict(
        val_acc_linear=0.55, val_acc_majority=0.50, val_acc_persistence=0.51,
        val_balacc_linear=0.36, val_balacc_majority=0.3333,
        val_macro_f1_linear=0.36, val_macro_f1_majority=0.22,
        holdout_acc_uplift_vs_majority=0.03, holdout_macro_f1_uplift_vs_majority=0.10,
        val_date_block_agreement=0.9, val_month_block_agreement=0.9,
        calibration_usable=True, high_conf_tail_beats_majority=True,
        cost_share_gt_16bps=0.05,
    )
    d.update(over)
    return aj.VerdictInputs(**d)


def test_verdict_continue_when_all_margins_met():
    out = aj.compute_verdict(_base_inputs())
    assert out["verdict"] == aj.VERDICT_CONTINUE
    assert out["kill_reasons"] == []


def test_verdict_kill_when_accuracy_margin_missed():
    # Linear barely beats majority (+0.5 pp) → fails the +2.0 pp both-floors rule.
    out = aj.compute_verdict(_base_inputs(val_acc_linear=0.505))
    assert out["verdict"] == aj.VERDICT_KILL
    assert any("beat BOTH" in r for r in out["kill_reasons"])


def test_verdict_kill_when_holdout_sign_reverses():
    out = aj.compute_verdict(_base_inputs(holdout_acc_uplift_vs_majority=-0.01))
    assert out["verdict"] == aj.VERDICT_KILL
    assert any("reverses the sign" in r for r in out["kill_reasons"])


def test_verdict_kill_when_blocks_not_majority():
    out = aj.compute_verdict(_base_inputs(val_date_block_agreement=0.3))
    assert out["verdict"] == aj.VERDICT_KILL
    assert any("majority of validation" in r for r in out["kill_reasons"])


def test_verdict_thresholds_are_the_frozen_ae_constants():
    out = aj.compute_verdict(_base_inputs())
    assert out["thresholds"]["success_accuracy_uplift_pp"] == 2.0
    assert out["thresholds"]["success_balanced_accuracy_uplift_pp"] == 1.0
    assert out["thresholds"]["success_macro_f1_uplift"] == 0.03
    assert contract.SUCCESS_ACCURACY_UPLIFT_PP == 2.0
    assert contract.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP == 1.0
    assert contract.SUCCESS_MACRO_F1_UPLIFT == 0.03


def test_verdict_kill_is_not_softened_by_good_calibration():
    # Accuracy margin fails; calibration is fine → still KILL (no rescue).
    out = aj.compute_verdict(
        _base_inputs(val_acc_linear=0.505, calibration_usable=True)
    )
    assert out["verdict"] == aj.VERDICT_KILL


# ---------------------------------------------------------------------------
# Baseline definitions locked (no unregistered families; frozen linear config)
# ---------------------------------------------------------------------------


def test_baseline_families_are_exactly_the_three_preregistered():
    assert aj.FAMILIES == (
        design.BASELINE_MAJORITY_CLASS,
        design.BASELINE_PERSISTENCE_PAST_RETURN,
        design.BASELINE_LOGISTIC_REGRESSION_L2,
    )
    assert aj.FAMILY_LINEAR == "multinomial_logistic_regression_l2"


def test_linear_config_is_frozen_single_epoch_sgd():
    trainer = aj.models.build_l2_logistic_regression_trainer(45)
    assert trainer.epochs == 1
    assert trainer.penalty == "l2"
    assert trainer.penalty_strength == design.SGD_L2_REGULARIZATION_STRENGTH
    assert trainer.learning_rate == design.SGD_LEARNING_RATE
    assert trainer.batch_size == design.SGD_BATCH_SIZE
    assert trainer.rng_seed == design.RNG_SEED


def test_majority_label_from_train_counts():
    counts = {-1: 150_077_008, 0: 3_590_082, 1: 151_149_037}
    m = aj.models.fit_majority_class_baseline(counts, 304_816_127)
    assert m.majority_label() == 1  # up class is modal in the pre-v002 train split


def test_allowlist_is_45_and_forbidden_columns_excluded():
    assert len(contract.ALLOWED_FEATURE_COLUMNS) == 45
    for c in contract.ALLOWED_FEATURE_COLUMNS:
        for sub in contract.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS:
            assert sub not in c


def test_claim_scope_forbidden_fields_present():
    for forbidden in (
        "tradability", "profitability", "pnl", "backtest_validity", "economic_significance",
    ):
        assert forbidden in contract.CLAIM_SCOPE_FORBIDDEN


def test_output_namespace_is_gitignored_research_path():
    assert aj.OUTPUT_NAMESPACE == (
        "data/research/microstructure/ml_baselines/pre_v002_fixed_baseline_v001"
    )
    assert aj.OUTPUT_NAMESPACE.startswith("data/research/")


# ---------------------------------------------------------------------------
# Persistence sign + majority prediction behaviour
# ---------------------------------------------------------------------------


def test_persistence_predicts_sign_of_past_window():
    signs = np.array([-1, 0, 1, 1, -1], dtype=np.int8)
    pred = aj.models.PersistenceBaseline.predict_from_signs(signs)
    assert np.array_equal(pred.predicted_class, signs)
    # one-hot proba on the predicted class
    for i, s in enumerate(signs):
        assert pred.predicted_proba[i, design.class_index_of(int(s))] == 1.0


def test_majority_predicts_constant_modal_class():
    m = aj.models.fit_majority_class_baseline({-1: 10, 0: 1, 1: 20}, 31)
    pred = m.predict_batch(np.zeros((4, 45), dtype=np.float64))
    assert np.all(pred.predicted_class == 1)
