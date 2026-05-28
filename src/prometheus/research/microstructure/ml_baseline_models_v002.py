"""Phase 4bn-B — Multi-day v002 ML-baseline model implementations.

Pure-numpy implementations of the fixed-a-priori baseline families from
Phase 4bn-A §15. No tuning, no model selection through results, no
hyperparameter search, no ensemble selection. Each family is run once with
the locked settings declared in :mod:`ml_baseline_design_v002`.

Baseline families (Phase 4bn-A §15):

1. ``majority_class_prior`` — predicts the train-prior majority class on
   every validation row; reports probabilities equal to the train prior.
2. ``persistence_past_return_sign`` — predicts the sign of the existing
   ``rolling_log_return_past_window_{horizon}`` feature; reports
   probabilities concentrated on the predicted class.
3. ``multinomial_logistic_regression_l2`` — softmax regression over 3
   classes with L2 weight decay, fit by mini-batch SGD on the train split
   for exactly ``SGD_EPOCHS`` passes with the fixed learning rate,
   gradient clipping, and L2 strength.
4. ``multinomial_linear_classifier_l1`` — softmax regression over 3
   classes with L1 weight decay (subgradient soft-thresholding); same
   fixed-a-priori SGD scaffolding as the L2 variant.

The shallow tree from §15 is intentionally NOT implemented because Phase
4bn-B fail-closes rather than running an unbounded tree fit over 74M+
train rows. The design records that decision verbatim.

No I/O. No network. No credentials. Imports only numpy + sibling modules.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Protocol

import numpy as np

from . import ml_baseline_design_v002 as design


class MlBaselineModelError(RuntimeError):
    """Raised when a baseline-model invariant is violated."""


# ---------------------------------------------------------------------------
# Protocol & predictions
# ---------------------------------------------------------------------------


@dataclass
class BatchPredictions:
    """A batch of (predicted_class, predicted_proba) outputs."""

    predicted_class: np.ndarray  # int8 in {-1, 0, +1}
    predicted_proba: np.ndarray  # shape (n, 3) over CLASS_LABELS order


class TrainedBaseline(Protocol):
    """Common protocol shared by the four implemented baseline families."""

    family: str

    def predict_batch(self, X_standardised: np.ndarray) -> BatchPredictions:
        ...


# ---------------------------------------------------------------------------
# Majority-class / class-prior baseline
# ---------------------------------------------------------------------------


@dataclass
class MajorityClassBaseline:
    """Predict the train-prior majority class with prior-probability outputs."""

    family: str
    train_prior_counts: dict[int, int]
    train_prior_total: int

    def majority_label(self) -> int:
        best_label = design.CLASS_LABELS[0]
        best_count = self.train_prior_counts[best_label]
        for cls in design.CLASS_LABELS[1:]:
            c = self.train_prior_counts[cls]
            if c > best_count or (c == best_count and cls < best_label):
                best_count = c
                best_label = cls
        return best_label

    def prior_proba(self) -> np.ndarray:
        if self.train_prior_total <= 0:
            raise MlBaselineModelError(
                "majority-class baseline has zero train prior total"
            )
        return np.array(
            [
                self.train_prior_counts[c] / float(self.train_prior_total)
                for c in design.CLASS_LABELS
            ],
            dtype=np.float64,
        )

    def predict_batch(self, X_standardised: np.ndarray) -> BatchPredictions:
        n = X_standardised.shape[0]
        label = self.majority_label()
        pred_class = np.full(n, label, dtype=np.int8)
        prior = self.prior_proba()
        proba = np.broadcast_to(prior, (n, 3)).copy()
        return BatchPredictions(predicted_class=pred_class, predicted_proba=proba)


def fit_majority_class_baseline(
    train_class_counts: dict[int, int], train_total: int
) -> MajorityClassBaseline:
    return MajorityClassBaseline(
        family=design.BASELINE_MAJORITY_CLASS,
        train_prior_counts=dict(train_class_counts),
        train_prior_total=int(train_total),
    )


# ---------------------------------------------------------------------------
# Persistence (past-window return sign) baseline
# ---------------------------------------------------------------------------


@dataclass
class PersistenceBaseline:
    """Predict ``sign(rolling_log_return_past_window_{horizon})`` per row.

    The baseline has no learned parameters and does not depend on training
    statistics. Predicted probabilities concentrate full mass on the
    predicted class (1.0 on the chosen class; 0.0 on the others). The
    ``persistence_signs`` channel on each per-day matrix is computed in
    :mod:`ml_baseline_dataset_v002` from the past-window feature.
    """

    family: str = design.BASELINE_PERSISTENCE_PAST_RETURN

    @staticmethod
    def predict_from_signs(persistence_signs: np.ndarray) -> BatchPredictions:
        if persistence_signs.dtype != np.int8:
            persistence_signs = persistence_signs.astype(np.int8, copy=False)
        n = persistence_signs.shape[0]
        proba = np.zeros((n, 3), dtype=np.float64)
        for cls_idx, cls in enumerate(design.CLASS_LABELS):
            proba[persistence_signs == cls, cls_idx] = 1.0
        return BatchPredictions(
            predicted_class=persistence_signs.copy(), predicted_proba=proba
        )

    def predict_batch(self, X_standardised: np.ndarray) -> BatchPredictions:
        raise MlBaselineModelError(
            "persistence baseline must be evaluated via predict_from_signs "
            "(it depends on the per-day persistence_signs channel, not the "
            "standardised feature matrix)"
        )


# ---------------------------------------------------------------------------
# Softmax regression with mini-batch SGD (L2 / L1 variants)
# ---------------------------------------------------------------------------


def _softmax_rowwise(logits: np.ndarray) -> np.ndarray:
    m = np.max(logits, axis=1, keepdims=True)
    exps = np.exp(logits - m)
    return exps / np.sum(exps, axis=1, keepdims=True)


@dataclass
class SoftmaxRegressionModel:
    """Trained-once 3-class softmax regression model (pure numpy).

    Parameters are a ``(n_features+1, 3)`` weight matrix where the trailing
    bias row is the per-class bias; ``predict_batch`` consumes the
    standardised feature matrix produced by the
    :class:`StreamingStandardizer`.
    """

    family: str
    weights: np.ndarray  # shape (n_features + 1, 3); last row is bias
    n_features: int
    epochs: int
    batch_size: int
    learning_rate: float
    penalty: str
    penalty_strength: float
    gradient_clip_norm: float
    rng_seed: int
    train_n_batches: int

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if X.shape[1] != self.n_features:
            raise MlBaselineModelError(
                f"feature width mismatch (model {self.n_features}, "
                f"input {X.shape[1]})"
            )
        logits = X @ self.weights[:-1, :] + self.weights[-1, :]
        return _softmax_rowwise(logits)

    def predict_class_indices(self, X: np.ndarray) -> np.ndarray:
        return np.argmax(self.predict_proba(X), axis=1)

    def predict_batch(self, X_standardised: np.ndarray) -> BatchPredictions:
        proba = self.predict_proba(X_standardised)
        idx = np.argmax(proba, axis=1)
        labels = np.array(
            [design.label_of_class_index(int(i)) for i in idx], dtype=np.int8
        )
        return BatchPredictions(predicted_class=labels, predicted_proba=proba)


def _one_hot_indices(y: np.ndarray) -> np.ndarray:
    """Map signed ``{-1, 0, +1}`` labels to 0-based class indices."""
    out = np.empty(y.shape[0], dtype=np.int64)
    out[y == -1] = 0
    out[y == 0] = 1
    out[y == 1] = 2
    return out


def _sgd_step_l2(
    weights: np.ndarray,
    X_bias: np.ndarray,
    y_idx: np.ndarray,
    *,
    learning_rate: float,
    penalty_strength: float,
    clip_norm: float,
) -> None:
    """One mini-batch SGD step for softmax regression with L2 penalty."""
    logits = X_bias @ weights
    proba = _softmax_rowwise(logits)
    # Cross-entropy gradient.
    proba[np.arange(y_idx.shape[0]), y_idx] -= 1.0
    grad = X_bias.T @ proba / float(X_bias.shape[0])
    # L2 regularisation on the weight rows (not on the bias row).
    grad[:-1, :] += penalty_strength * weights[:-1, :]
    # Global gradient-norm clip (deterministic, fixed clip threshold).
    norm = float(np.linalg.norm(grad))
    if clip_norm > 0.0 and norm > clip_norm:
        grad *= clip_norm / norm
    weights -= learning_rate * grad


def _sgd_step_l1(
    weights: np.ndarray,
    X_bias: np.ndarray,
    y_idx: np.ndarray,
    *,
    learning_rate: float,
    penalty_strength: float,
    clip_norm: float,
) -> None:
    """One mini-batch SGD step for softmax regression with L1 penalty.

    Uses a proximal sub-gradient step: a standard gradient step on the
    softmax cross-entropy followed by soft-thresholding on the non-bias
    weights (the bias row is left unpenalised).
    """
    logits = X_bias @ weights
    proba = _softmax_rowwise(logits)
    proba[np.arange(y_idx.shape[0]), y_idx] -= 1.0
    grad = X_bias.T @ proba / float(X_bias.shape[0])
    norm = float(np.linalg.norm(grad))
    if clip_norm > 0.0 and norm > clip_norm:
        grad *= clip_norm / norm
    weights -= learning_rate * grad
    # Soft-thresholding (proximal step) for L1.
    thresh = learning_rate * penalty_strength
    w_nob = weights[:-1, :]
    sign = np.sign(w_nob)
    weights[:-1, :] = sign * np.maximum(np.abs(w_nob) - thresh, 0.0)


@dataclass
class SoftmaxTrainer:
    """Mini-batch SGD trainer for softmax regression baselines.

    The trainer iterates a stream of supervised ``(X_standardised, y)``
    chunks (one per train partition) and applies fixed mini-batch SGD
    updates with the locked hyperparameters. No early stopping. No
    learning-rate schedule. No validation feedback.
    """

    family: str
    n_features: int
    penalty: str
    penalty_strength: float
    learning_rate: float = design.SGD_LEARNING_RATE
    batch_size: int = design.SGD_BATCH_SIZE
    epochs: int = design.SGD_EPOCHS
    gradient_clip_norm: float = design.SGD_GRADIENT_CLIP_NORM
    rng_seed: int = design.RNG_SEED
    _weights: np.ndarray = field(init=False)
    _rng: np.random.Generator = field(init=False)
    _train_n_batches: int = 0
    _epoch_completed: int = 0

    def __post_init__(self) -> None:
        if self.penalty not in ("l1", "l2"):
            raise MlBaselineModelError(
                f"penalty must be 'l1' or 'l2', got {self.penalty!r}"
            )
        self._weights = np.zeros((self.n_features + 1, 3), dtype=np.float64)
        self._rng = np.random.default_rng(self.rng_seed)

    def partial_fit(self, X_standardised: np.ndarray, y: np.ndarray) -> None:
        if X_standardised.shape[1] != self.n_features:
            raise MlBaselineModelError(
                f"feature width mismatch (trainer {self.n_features}, "
                f"input {X_standardised.shape[1]})"
            )
        n = X_standardised.shape[0]
        if n == 0:
            return
        y_idx = _one_hot_indices(y)
        # Deterministic per-partition shuffle.
        perm = self._rng.permutation(n)
        X_shuf = X_standardised[perm]
        y_shuf = y_idx[perm]
        for start in range(0, n, self.batch_size):
            end = min(start + self.batch_size, n)
            X_chunk = X_shuf[start:end]
            y_chunk = y_shuf[start:end]
            X_bias = np.concatenate(
                [X_chunk, np.ones((X_chunk.shape[0], 1), dtype=np.float64)], axis=1
            )
            if self.penalty == "l2":
                _sgd_step_l2(
                    self._weights,
                    X_bias,
                    y_chunk,
                    learning_rate=self.learning_rate,
                    penalty_strength=self.penalty_strength,
                    clip_norm=self.gradient_clip_norm,
                )
            else:
                _sgd_step_l1(
                    self._weights,
                    X_bias,
                    y_chunk,
                    learning_rate=self.learning_rate,
                    penalty_strength=self.penalty_strength,
                    clip_norm=self.gradient_clip_norm,
                )
            self._train_n_batches += 1

    def finalize(self) -> SoftmaxRegressionModel:
        return SoftmaxRegressionModel(
            family=self.family,
            weights=self._weights.copy(),
            n_features=self.n_features,
            epochs=self.epochs,
            batch_size=self.batch_size,
            learning_rate=self.learning_rate,
            penalty=self.penalty,
            penalty_strength=self.penalty_strength,
            gradient_clip_norm=self.gradient_clip_norm,
            rng_seed=self.rng_seed,
            train_n_batches=self._train_n_batches,
        )


def build_l2_logistic_regression_trainer(n_features: int) -> SoftmaxTrainer:
    return SoftmaxTrainer(
        family=design.BASELINE_LOGISTIC_REGRESSION_L2,
        n_features=n_features,
        penalty="l2",
        penalty_strength=design.SGD_L2_REGULARIZATION_STRENGTH,
    )


def build_l1_linear_classifier_trainer(n_features: int) -> SoftmaxTrainer:
    return SoftmaxTrainer(
        family=design.BASELINE_LINEAR_CLASSIFIER_L1,
        n_features=n_features,
        penalty="l1",
        penalty_strength=design.SGD_L1_REGULARIZATION_STRENGTH,
    )


# ---------------------------------------------------------------------------
# Streaming evaluation accumulator (shared across baselines)
# ---------------------------------------------------------------------------


@dataclass
class StreamingEvaluator:
    """Accumulate descriptive evaluation statistics across one (split × horizon)."""

    family: str
    split: str
    horizon: str
    n_rows: int = 0
    confusion: np.ndarray = field(
        default_factory=lambda: np.zeros((3, 3), dtype=np.int64)
    )
    sum_log_loss: float = 0.0
    sum_brier: float = 0.0
    n_probabilistic_rows: int = 0
    # Cost-aware descriptive accumulators (Phase 4bn-A §18; descriptive
    # only — never strategy / PnL / backtest):
    abs_return_sum_by_multiple: dict[float, int] = field(default_factory=dict)
    abs_return_total: int = 0

    def __post_init__(self) -> None:
        if not self.abs_return_sum_by_multiple:
            for m in design.COST_COMMENSURABILITY_MULTIPLES:
                self.abs_return_sum_by_multiple[m] = 0

    def update(
        self,
        *,
        y_true: np.ndarray,
        predicted_class: np.ndarray,
        predicted_proba: np.ndarray,
        forward_log_returns: np.ndarray | None = None,
    ) -> None:
        n = int(y_true.shape[0])
        if n == 0:
            return
        self.n_rows += n
        # Confusion matrix in CLASS_LABELS order (rows = true, cols = pred).
        true_idx = _one_hot_indices(y_true)
        pred_idx = _one_hot_indices(predicted_class)
        np.add.at(self.confusion, (true_idx, pred_idx), 1)
        # Probabilistic metrics on rows where probabilities are defined.
        if predicted_proba.shape[1] != 3:
            raise MlBaselineModelError(
                f"predicted_proba must have 3 columns, got {predicted_proba.shape!r}"
            )
        # Clip for numerical safety in log-loss.
        proba_safe = np.clip(predicted_proba, 1e-12, 1.0 - 1e-12)
        chosen = proba_safe[np.arange(n), true_idx]
        self.sum_log_loss += float(-np.log(chosen).sum())
        # Brier score (multi-class one-hot).
        one_hot = np.zeros_like(proba_safe)
        one_hot[np.arange(n), true_idx] = 1.0
        self.sum_brier += float(np.square(proba_safe - one_hot).sum(axis=1).sum())
        self.n_probabilistic_rows += n
        # Cost-aware descriptive (validation-only callers compute this).
        if forward_log_returns is not None:
            ret = np.abs(forward_log_returns)
            self.abs_return_total += int(ret.shape[0])
            cost = design.COST_ROUND_TRIP_DECIMAL
            for m in design.COST_COMMENSURABILITY_MULTIPLES:
                self.abs_return_sum_by_multiple[m] += int(
                    np.count_nonzero(ret > m * cost)
                )

    def confusion_dict(self) -> dict[str, dict[str, int]]:
        labels = design.CLASS_LABELS
        out: dict[str, dict[str, int]] = {}
        for i, true_cls in enumerate(labels):
            out_row: dict[str, int] = {}
            for j, pred_cls in enumerate(labels):
                key = f"pred_{design.CLASS_DISPLAY_NAMES[pred_cls]}"
                out_row[key] = int(self.confusion[i, j])
            out[f"true_{design.CLASS_DISPLAY_NAMES[true_cls]}"] = out_row
        return out

    def accuracy(self) -> float:
        if self.n_rows == 0:
            return 0.0
        return float(np.trace(self.confusion)) / float(self.n_rows)

    def per_class_precision_recall(self) -> dict[str, dict[str, float]]:
        out: dict[str, dict[str, float]] = {}
        for i, cls in enumerate(design.CLASS_LABELS):
            tp = float(self.confusion[i, i])
            fp = float(self.confusion[:, i].sum()) - tp
            fn = float(self.confusion[i, :].sum()) - tp
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = (
                2.0 * precision * recall / (precision + recall)
                if (precision + recall) > 0
                else 0.0
            )
            out[design.CLASS_DISPLAY_NAMES[cls]] = {
                "precision": precision,
                "recall": recall,
                "f1": f1,
            }
        return out

    def macro_f1(self) -> float:
        pc = self.per_class_precision_recall()
        if not pc:
            return 0.0
        return float(sum(v["f1"] for v in pc.values()) / len(pc))

    def balanced_accuracy(self) -> float:
        pc = self.per_class_precision_recall()
        if not pc:
            return 0.0
        return float(sum(v["recall"] for v in pc.values()) / len(pc))

    def mean_log_loss(self) -> float | None:
        if self.n_probabilistic_rows == 0:
            return None
        return self.sum_log_loss / float(self.n_probabilistic_rows)

    def mean_brier(self) -> float | None:
        if self.n_probabilistic_rows == 0:
            return None
        return self.sum_brier / float(self.n_probabilistic_rows)

    def cost_commensurability_fractions(self) -> dict[str, float]:
        if self.abs_return_total == 0:
            return {f"frac_abs_return_gt_{m}x_rt_cost": 0.0
                    for m in design.COST_COMMENSURABILITY_MULTIPLES}
        out: dict[str, float] = {}
        for m in design.COST_COMMENSURABILITY_MULTIPLES:
            n = self.abs_return_sum_by_multiple[m]
            out[f"frac_abs_return_gt_{m}x_rt_cost"] = n / float(self.abs_return_total)
        return out

    def as_dict(self) -> dict[str, object]:
        return {
            "family": self.family,
            "split": self.split,
            "horizon": self.horizon,
            "n_rows": int(self.n_rows),
            "confusion_matrix": self.confusion_dict(),
            "accuracy": self.accuracy(),
            "balanced_accuracy": self.balanced_accuracy(),
            "macro_f1": self.macro_f1(),
            "per_class": self.per_class_precision_recall(),
            "mean_log_loss": self.mean_log_loss(),
            "mean_brier_score": self.mean_brier(),
            "n_probabilistic_rows": int(self.n_probabilistic_rows),
            "cost_commensurability": self.cost_commensurability_fractions(),
            "cost_lock_bps_per_side": design.COST_BPS_PER_SIDE,
            "cost_lock_bps_round_trip": design.COST_BPS_ROUND_TRIP,
        }


def evaluate_predictions(
    *,
    family: str,
    split: str,
    horizon: str,
    batches: Iterable[
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray | None]
    ],
) -> StreamingEvaluator:
    """Convenience: build and update a :class:`StreamingEvaluator` over batches.

    Each batch is a ``(y_true, predicted_class, predicted_proba,
    forward_log_returns)`` tuple. ``forward_log_returns`` may be ``None``
    when cost-aware summaries are not desired (e.g. on the train split).
    """
    ev = StreamingEvaluator(family=family, split=split, horizon=horizon)
    for y_true, pred_class, pred_proba, ret in batches:
        ev.update(
            y_true=y_true,
            predicted_class=pred_class,
            predicted_proba=pred_proba,
            forward_log_returns=ret,
        )
    return ev


__all__ = [
    "BatchPredictions",
    "MajorityClassBaseline",
    "MlBaselineModelError",
    "PersistenceBaseline",
    "SoftmaxRegressionModel",
    "SoftmaxTrainer",
    "StreamingEvaluator",
    "TrainedBaseline",
    "build_l1_linear_classifier_trainer",
    "build_l2_logistic_regression_trainer",
    "evaluate_predictions",
    "fit_majority_class_baseline",
]
