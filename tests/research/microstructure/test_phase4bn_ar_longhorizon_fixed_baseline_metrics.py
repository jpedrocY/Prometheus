"""Phase 4bn-AR — metric / standardizer / block / calibration-tail tests.

Synthetic-array tests for the reusable metric machinery: the train-only
standardizer (applies the AQ transform, imputes non-finite to fixed zero, boolean
passthrough), the 60s persistence index, per-date/month "beats both floors" block
computation, the >= 0.8 confidence-tail summary + calibration verdict, and
deterministic majority/model behaviour on fixtures. No real Parquet is read.
"""

from __future__ import annotations

import numpy as np
import pytest

from prometheus.research.microstructure import longhorizon_fixed_baseline_run_v001 as ar
from prometheus.research.microstructure import longhorizon_ml_dataset_contract_v001 as contract
from prometheus.research.microstructure import ml_baseline_design_v002 as design
from prometheus.research.microstructure import ml_baseline_metrics_v002 as metrics
from prometheus.research.microstructure import ml_baseline_models_v002 as models


def _synthetic_transform() -> dict:
    per = {}
    for c in contract.ALLOWED_FEATURE_COLUMNS:
        per[c] = {"train_mean": 1.0, "train_std": 2.0, "train_count": 10, "train_null_count": 0}
    return {
        "fit_split": "train",
        "standardization_rule": contract.STANDARDIZATION_RULE,
        "standardization_epsilon": contract.STANDARDIZATION_EPSILON,
        "imputation_rule": contract.IMPUTATION_RULE,
        "imputation_fill_value": contract.IMPUTATION_FILL_VALUE,
        "standardize_boolean_flags": contract.STANDARDIZE_BOOLEAN_FLAGS,
        "feature_count": 45,
        "feature_list_hash": ar.aq.feature_list_hash(),
        "per_feature": per,
    }


def test_standardizer_applies_train_transform_and_boolean_passthrough() -> None:
    std = ar.build_standardizer(_synthetic_transform())
    assert std.columns == tuple(contract.ALLOWED_FEATURE_COLUMNS)
    x = np.full((3, 45), 5.0, dtype=np.float64)
    out = std.transform(x)
    bool_cols = frozenset(design.BOOLEAN_FEATURE_COLUMN_NAMES)
    for j, c in enumerate(std.columns):
        if c in bool_cols:
            assert np.allclose(out[:, j], 5.0)  # passthrough
        else:
            assert np.allclose(out[:, j], 2.0)  # (5 - 1) / max(2, eps)


def test_standardizer_imputes_nonfinite_to_fixed_zero() -> None:
    std = ar.build_standardizer(_synthetic_transform())
    x = np.full((2, 45), np.nan, dtype=np.float64)
    out = std.transform(x)
    bool_cols = frozenset(design.BOOLEAN_FEATURE_COLUMN_NAMES)
    for j, c in enumerate(std.columns):
        if c in bool_cols:
            assert np.allclose(out[:, j], 0.0)
        else:
            assert np.allclose(out[:, j], -0.5)  # (0 - 1) / 2


def test_persistence_index_points_at_60s_past_window() -> None:
    std = ar.build_standardizer(_synthetic_transform())
    assert std.columns[std.persistence_index] == ar.PERSISTENCE_FEATURE
    assert ar.PERSISTENCE_FEATURE == "rolling_log_return_past_window_60s"


def test_persistence_predicts_sign_of_past_window() -> None:
    signs = np.array([-1, 0, 1, 1, -1], dtype=np.int8)
    pred = models.PersistenceBaseline.predict_from_signs(signs)
    assert np.array_equal(pred.predicted_class, signs)
    for i, s in enumerate(signs):
        assert pred.predicted_proba[i, design.class_index_of(int(s))] == 1.0


def test_majority_from_train_counts_per_horizon() -> None:
    m = ar.models.fit_majority_class_baseline({-1: 10, 0: 1, 1: 20}, 31)
    assert m.majority_label() == 1
    pred = m.predict_batch(np.zeros((4, 45), dtype=np.float64))
    assert np.all(pred.predicted_class == 1)


def test_streaming_evaluator_accuracy_and_confusion_correct() -> None:
    ev = models.StreamingEvaluator(family="x", split="validation", horizon="5m")
    y = np.array([-1, 0, 1, 1], dtype=np.int8)
    pred = np.array([-1, 0, 1, -1], dtype=np.int8)
    proba = np.tile(np.array([0.2, 0.3, 0.5]), (4, 1))
    ev.update(y_true=y, predicted_class=pred, predicted_proba=proba)
    assert ev.n_rows == 4
    assert ev.accuracy() == pytest.approx(0.75)
    d = ar._enrich_metrics(ev)
    assert d["true_class_distribution"] == {"down": 1, "flat": 1, "up": 2}
    assert d["predicted_class_distribution"] == {"down": 2, "flat": 1, "up": 1}


def _feed(reg: ar.EvalRegistry, horizon: str, family: str, split: str, date: str,
          y: np.ndarray, pred: np.ndarray) -> None:
    proba = np.zeros((y.shape[0], 3), dtype=np.float64)
    for i, c in enumerate(pred):
        proba[i, design.class_index_of(int(c))] = 1.0
    reg.update(
        horizon=horizon, family=family, split=split, month=date[:7], date=date,
        y_true=y, pred_class=pred, pred_proba=proba,
    )


def test_block_beats_both_counts_dates_where_l2_beats_both_floors() -> None:
    reg = ar.EvalRegistry()
    y = np.array([-1, 1], dtype=np.int8)
    perfect = np.array([-1, 1], dtype=np.int8)
    const_up = np.array([1, 1], dtype=np.int8)
    lin, maj, per = ar.FAMILY_LINEAR, ar.FAMILY_MAJORITY, ar.FAMILY_PERSISTENCE
    # Date A: L2 perfect; majority 0.5, persistence 0.5 -> L2 beats both.
    _feed(reg, "5m", lin, "validation", "2024-09-01", y, perfect)
    _feed(reg, "5m", maj, "validation", "2024-09-01", y, const_up)
    _feed(reg, "5m", per, "validation", "2024-09-01", y, const_up)
    # Date B: L2 ties persistence (both perfect) -> not strictly beating both.
    _feed(reg, "5m", lin, "validation", "2024-09-02", y, perfect)
    _feed(reg, "5m", maj, "validation", "2024-09-02", y, const_up)
    _feed(reg, "5m", per, "validation", "2024-09-02", y, perfect)
    total, beats, per_block = ar._block_beats_both(reg, "5m", "validation", "date")
    assert total == 2
    assert beats == 1
    assert per_block == {"2024-09-01": True, "2024-09-02": False}


def test_confidence_tail_summary_and_calibration_verdict() -> None:
    cs = metrics.CalibrationSummary(family=ar.FAMILY_LINEAR, split="validation", horizon="5m")
    # 10 rows at max-proba 0.9 (>=0.8 tail); 6 correct -> tail_acc 0.6.
    n = 10
    proba = np.zeros((n, 3), dtype=np.float64)
    proba[:, 2] = 0.9
    proba[:, 0] = 0.05
    proba[:, 1] = 0.05
    pred = np.full(n, 1, dtype=np.int8)  # class index 2 == label +1
    y = np.array([1, 1, 1, 1, 1, 1, -1, -1, -1, -1], dtype=np.int8)
    cs.update(predicted_proba=proba, predicted_class=pred, y_true=y)
    tail = ar._confidence_tail(cs, majority_acc=0.5)
    assert tail["confidence_tail_n"] == 10
    assert tail["confidence_tail_accuracy"] == pytest.approx(0.6)
    assert tail["confidence_tail_beats_majority_floor"] is True
    # emp acc 0.6 vs mean prob 0.9 -> overconfident -> ranking_only.
    assert tail["calibration_verdict"] == ar.verdict_mod.CALIBRATION_RANKING_ONLY


def test_l2_training_is_deterministic_on_fixture() -> None:
    rng = np.random.default_rng(0)
    x = rng.standard_normal((200, 45))
    y = np.where(x[:, 0] > 0, 1, -1).astype(np.int8)
    m1 = ar.models.build_l2_logistic_regression_trainer(45)
    m1.partial_fit(x, y)
    fm1 = m1.finalize()
    m2 = ar.models.build_l2_logistic_regression_trainer(45)
    m2.partial_fit(x, y)
    fm2 = m2.finalize()
    assert np.array_equal(fm1.weights, fm2.weights)
    assert bool(np.all(np.isfinite(fm1.weights)))
