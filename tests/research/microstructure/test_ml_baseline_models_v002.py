"""Phase 4bn-B — unit tests for the fixed-a-priori baseline models.

Pure-numpy tests against synthetic labels and feature matrices. Verifies
that each baseline produces deterministic, well-formed
``BatchPredictions`` outputs, that the streaming-evaluator confusion
matrix is correct, and that the L1 / L2 softmax trainers converge to the
class-prior in the trivial (random-feature) regime.
"""

from __future__ import annotations

import numpy as np

from prometheus.research.microstructure import ml_baseline_design_v002 as design
from prometheus.research.microstructure import ml_baseline_models_v002 as models


def test_majority_class_baseline_predicts_most_common_class() -> None:
    counts = {-1: 50, 0: 200, 1: 100}
    baseline = models.fit_majority_class_baseline(counts, sum(counts.values()))
    assert baseline.majority_label() == 0
    n = 16
    X = np.zeros((n, len(design.COMPUTED_FEATURE_COLUMN_NAMES)))
    out = baseline.predict_batch(X)
    assert out.predicted_class.shape == (n,)
    assert np.all(out.predicted_class == 0)
    assert out.predicted_proba.shape == (n, 3)
    # First row prior == [50, 200, 100] / 350.
    expected = np.array([50.0, 200.0, 100.0]) / 350.0
    np.testing.assert_allclose(out.predicted_proba[0], expected, rtol=1e-9)


def test_persistence_baseline_uses_persistence_signs_channel() -> None:
    signs = np.array([-1, 0, 1, -1, 1, 0, 1], dtype=np.int8)
    out = models.PersistenceBaseline.predict_from_signs(signs)
    assert out.predicted_class.tolist() == signs.tolist()
    # Each row has full mass on the predicted class.
    for i, s in enumerate(signs.tolist()):
        idx = design.class_index_of(int(s))
        assert out.predicted_proba[i, idx] == 1.0
        assert np.sum(out.predicted_proba[i]) == 1.0


def test_persistence_baseline_predict_batch_raises_on_X() -> None:
    persistence = models.PersistenceBaseline()
    X = np.zeros((4, len(design.COMPUTED_FEATURE_COLUMN_NAMES)))
    try:
        persistence.predict_batch(X)
        raise AssertionError("expected MlBaselineModelError")
    except models.MlBaselineModelError:
        pass


def _synthetic_softmax_training_data(
    n_features: int, n_samples: int, rng_seed: int = 4242
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(rng_seed)
    X = rng.standard_normal(size=(n_samples, n_features))
    # Linear class boundary: class label = sign(w · x), with the zero class
    # carved out in a small band around zero so all three classes appear.
    w_true = rng.standard_normal(size=n_features)
    score = X @ w_true
    y = np.where(score > 0.2, 1, np.where(score < -0.2, -1, 0)).astype(np.int8)
    return X, y


def test_softmax_l2_trainer_predicts_better_than_uniform() -> None:
    n_features = 8
    X, y = _synthetic_softmax_training_data(n_features, 4000)
    trainer = models.SoftmaxTrainer(
        family="test_l2",
        n_features=n_features,
        penalty="l2",
        penalty_strength=1e-4,
        learning_rate=0.1,
        batch_size=128,
        epochs=1,
    )
    trainer.partial_fit(X, y)
    model = trainer.finalize()
    preds = model.predict_batch(X)
    acc = float(np.mean(preds.predicted_class == y))
    # The uniform-class accuracy floor is 1/3; on a separable linear
    # problem a single SGD epoch easily beats 0.4.
    assert acc > 0.4
    # Probabilities are valid simplex.
    np.testing.assert_allclose(preds.predicted_proba.sum(axis=1), 1.0, rtol=1e-9)
    assert np.all(preds.predicted_proba >= 0.0)
    assert np.all(preds.predicted_proba <= 1.0)


def test_softmax_l1_trainer_soft_thresholding_zeros_some_weights() -> None:
    n_features = 8
    X, y = _synthetic_softmax_training_data(n_features, 1000)
    trainer = models.SoftmaxTrainer(
        family="test_l1",
        n_features=n_features,
        penalty="l1",
        # A strong L1 strength to ensure visible sparsity after a single
        # epoch of soft-thresholding.
        penalty_strength=1.0,
        learning_rate=0.5,
        batch_size=128,
        epochs=1,
    )
    trainer.partial_fit(X, y)
    model = trainer.finalize()
    weight_block = model.weights[:-1, :]
    # The L1 proximal step should leave at least some weights exactly zero.
    assert int(np.count_nonzero(weight_block == 0.0)) > 0


def test_streaming_evaluator_confusion_matrix_is_correct() -> None:
    ev = models.StreamingEvaluator(family="majority_test", split="train", horizon="15s")
    y_true = np.array([-1, -1, 0, 0, 1, 1], dtype=np.int8)
    pred = np.array([-1, 0, 0, 1, 1, -1], dtype=np.int8)
    proba = np.zeros((6, 3))
    proba[np.arange(6), [0, 0, 1, 1, 2, 2]] = 1.0  # one-hot on pred
    ev.update(y_true=y_true, predicted_class=pred, predicted_proba=proba)
    cm = ev.confusion_dict()
    assert cm["true_down"]["pred_down"] == 1
    assert cm["true_down"]["pred_flat"] == 1
    assert cm["true_flat"]["pred_flat"] == 1
    assert cm["true_flat"]["pred_up"] == 1
    assert cm["true_up"]["pred_up"] == 1
    assert cm["true_up"]["pred_down"] == 1
    # Accuracy = 3/6.
    assert ev.accuracy() == 0.5


def test_streaming_evaluator_cost_commensurability_descriptive() -> None:
    ev = models.StreamingEvaluator(family="test", split="validation", horizon="15s")
    n = 1000
    y_true = np.zeros(n, dtype=np.int8)
    pred = np.zeros(n, dtype=np.int8)
    proba = np.zeros((n, 3))
    proba[:, 1] = 1.0
    # Forward returns: half are exactly the round-trip cost magnitude,
    # half are 3x the cost.
    cost = design.COST_ROUND_TRIP_DECIMAL
    rng = np.random.default_rng(0)
    rets = np.empty(n)
    rets[: n // 2] = cost * 1.001
    rets[n // 2 :] = cost * 3.0
    rng.shuffle(rets)
    ev.update(
        y_true=y_true,
        predicted_class=pred,
        predicted_proba=proba,
        forward_log_returns=rets,
    )
    fr = ev.cost_commensurability_fractions()
    # |r| > 1.0x cost: all n rows.
    assert fr["frac_abs_return_gt_1.0x_rt_cost"] == 1.0
    # |r| > 2.0x cost: half the rows (those at 3x).
    assert 0.49 < fr["frac_abs_return_gt_2.0x_rt_cost"] < 0.51
