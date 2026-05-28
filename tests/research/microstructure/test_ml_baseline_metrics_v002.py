"""Phase 4bn-B — unit tests for descriptive ML-baseline metrics helpers."""

from __future__ import annotations

import numpy as np

from prometheus.research.microstructure import ml_baseline_design_v002 as design
from prometheus.research.microstructure import ml_baseline_metrics_v002 as metrics
from prometheus.research.microstructure import ml_baseline_models_v002 as models


def test_class_balance_counts_and_prevalence() -> None:
    cb = metrics.ClassBalance(split="train", horizon="15s")
    y = np.array([-1, -1, -1, 0, 1, 1], dtype=np.int8)
    cb.update(labels=y, n_total=8, n_censored=1, n_embargoed=1)
    assert cb.n_rows_supervised == 6
    assert cb.n_rows_censored == 1
    assert cb.n_rows_embargoed == 1
    prev = cb.prevalence()
    assert prev[-1] == 0.5
    assert prev[0] == 1 / 6
    assert prev[1] == 1 / 3
    d = cb.as_dict()
    assert d["counts"]["down"] == 3
    assert d["counts"]["flat"] == 1
    assert d["counts"]["up"] == 2
    assert abs(d["prevalence"]["up"] - 1 / 3) < 1e-12


def test_calibration_summary_with_uniform_predictions() -> None:
    cs = metrics.CalibrationSummary(family="t", split="validation", horizon="15s")
    n = 100
    rng = np.random.default_rng(0)
    proba = np.full((n, 3), 1.0 / 3.0)
    pred = np.ones(n, dtype=np.int8)
    y_true = rng.choice([-1, 0, 1], size=n).astype(np.int8)
    cs.update(predicted_proba=proba, predicted_class=pred, y_true=y_true)
    d = cs.as_dict()
    # All max-probabilities = 1/3 fall into the [0.3, 0.4) bin (index 3).
    bins = d["bins"]
    assert isinstance(bins, list)
    assert any(b["n_rows"] == n for b in bins)


def test_stability_delta_returns_none_on_none_input() -> None:
    assert metrics.stability_delta(None, 0.5) is None
    assert metrics.stability_delta(0.5, None) is None
    assert metrics.stability_delta(0.4, 0.6) == 0.6 - 0.4


def test_summarize_train_validation_stability_keys() -> None:
    train = {"accuracy": 0.5, "balanced_accuracy": 0.4, "macro_f1": 0.45,
             "mean_log_loss": 1.0, "mean_brier_score": 0.6}
    val = {"accuracy": 0.45, "balanced_accuracy": 0.35, "macro_f1": 0.4,
           "mean_log_loss": 1.1, "mean_brier_score": 0.65}
    s = metrics.summarize_train_validation_stability(
        train_metrics=train, validation_metrics=val
    )
    assert abs(s["accuracy_validation_minus_train"] - (-0.05)) < 1e-9  # type: ignore[arg-type, operator]
    assert (
        abs(s["balanced_accuracy_validation_minus_train"] - (-0.05)) < 1e-9  # type: ignore[arg-type, operator]
    )
    assert abs(s["mean_log_loss_validation_minus_train"] - 0.1) < 1e-9  # type: ignore[arg-type, operator]
    assert abs(s["mean_brier_validation_minus_train"] - 0.05) < 1e-9  # type: ignore[arg-type, operator]


def test_flatten_metric_rows_emits_per_class_and_cost_rows() -> None:
    # Build a streaming evaluator with known counts and pass its block.
    ev = models.StreamingEvaluator(family="x", split="train", horizon="15s")
    y_true = np.array([-1, 0, 1, 1, 0, -1], dtype=np.int8)
    pred = np.array([-1, 0, 1, 1, 0, -1], dtype=np.int8)
    proba = np.zeros((6, 3))
    proba[np.arange(6), [0, 1, 2, 2, 1, 0]] = 1.0
    ev.update(y_true=y_true, predicted_class=pred, predicted_proba=proba)
    block = ev.as_dict()
    rows = metrics.flatten_metric_rows(
        family="x", train_metrics=block, validation_metrics=None
    )
    metric_names = {r["metric_name"] for r in rows}
    assert "accuracy" in metric_names
    assert "balanced_accuracy" in metric_names
    assert "macro_f1" in metric_names
    assert any(m.startswith("per_class.down.") for m in metric_names)
    assert any(m.startswith("cost_commensurability.") for m in metric_names)


def test_classBalance_zero_supervised_safe() -> None:
    cb = metrics.ClassBalance(split="validation", horizon="60s")
    d = cb.as_dict()
    for k in ("down", "flat", "up"):
        assert d["prevalence"][k] == 0.0
        assert d["counts"][k] == 0


def test_design_class_index_round_trip() -> None:
    for cls in design.CLASS_LABELS:
        idx = design.class_index_of(cls)
        assert design.label_of_class_index(idx) == cls
