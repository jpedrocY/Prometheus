"""Phase 4bn-B — Multi-day v002 ML-baseline descriptive metrics helpers.

Pure-numpy descriptive metric helpers for the Phase 4bn-B baselines:
class-balance summaries (split × horizon), reliability/calibration
summaries (validation-only descriptive bins), and train/validation
stability deltas.

Phase 4bn-A §16 / §17 constrain Phase 4bn-B to descriptive metrics only.
This module computes no PnL, no backtest, no Sharpe / Sortino / drawdown,
no hit-rate-as-strategy, no threshold-tuned metric, and no test-set
metric in the first implementation.

No I/O. No network. No credentials. Imports only numpy + sibling modules.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

import numpy as np

from . import ml_baseline_design_v002 as design


class MlBaselineMetricsError(RuntimeError):
    """Raised when a metrics input is malformed."""


# ---------------------------------------------------------------------------
# Class-balance summaries (split × horizon)
# ---------------------------------------------------------------------------


@dataclass
class ClassBalance:
    """Counts and prevalences of the three signed classes in one split × horizon."""

    split: str
    horizon: str
    n_rows_supervised: int = 0
    n_rows_censored: int = 0
    n_rows_embargoed: int = 0
    n_rows_total: int = 0
    counts: dict[int, int] = field(
        default_factory=lambda: dict.fromkeys(design.CLASS_LABELS, 0)
    )

    def update(
        self,
        *,
        labels: np.ndarray,
        n_total: int,
        n_censored: int,
        n_embargoed: int,
    ) -> None:
        for cls in design.CLASS_LABELS:
            self.counts[cls] += int(np.count_nonzero(labels == cls))
        self.n_rows_supervised += int(labels.shape[0])
        self.n_rows_total += int(n_total)
        self.n_rows_censored += int(n_censored)
        self.n_rows_embargoed += int(n_embargoed)

    def prevalence(self) -> dict[int, float]:
        if self.n_rows_supervised == 0:
            return dict.fromkeys(design.CLASS_LABELS, 0.0)
        return {
            cls: self.counts[cls] / float(self.n_rows_supervised)
            for cls in design.CLASS_LABELS
        }

    def as_dict(self) -> dict[str, object]:
        prev = self.prevalence()
        return {
            "split": self.split,
            "horizon": self.horizon,
            "n_rows_total": int(self.n_rows_total),
            "n_rows_supervised": int(self.n_rows_supervised),
            "n_rows_censored": int(self.n_rows_censored),
            "n_rows_embargoed": int(self.n_rows_embargoed),
            "counts": {
                design.CLASS_DISPLAY_NAMES[c]: int(self.counts[c])
                for c in design.CLASS_LABELS
            },
            "prevalence": {
                design.CLASS_DISPLAY_NAMES[c]: float(prev[c])
                for c in design.CLASS_LABELS
            },
        }


# ---------------------------------------------------------------------------
# Reliability / calibration summaries (validation-only, descriptive)
# ---------------------------------------------------------------------------


CALIBRATION_BIN_EDGES: tuple[float, ...] = (
    0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
)


@dataclass
class CalibrationSummary:
    """Descriptive reliability summary for the chosen-class probability.

    For each row we record the probability assigned to the *predicted*
    class (max-class probability) and accumulate the count of rows whose
    prediction was correct, bucketed by max-probability decile. We never
    apply any calibration transform — this is descriptive only. Phase
    4bn-A §17 forbids threshold tuning and probability-to-signal
    conversion.
    """

    family: str
    split: str
    horizon: str
    bin_edges: tuple[float, ...] = field(default_factory=lambda: CALIBRATION_BIN_EDGES)
    bin_counts: list[int] = field(default_factory=list)
    bin_correct: list[int] = field(default_factory=list)
    bin_prob_sum: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        n_bins = len(self.bin_edges) - 1
        if not self.bin_counts:
            self.bin_counts = [0] * n_bins
        if not self.bin_correct:
            self.bin_correct = [0] * n_bins
        if not self.bin_prob_sum:
            self.bin_prob_sum = [0.0] * n_bins

    def update(
        self,
        *,
        predicted_proba: np.ndarray,
        predicted_class: np.ndarray,
        y_true: np.ndarray,
    ) -> None:
        n = int(y_true.shape[0])
        if n == 0:
            return
        max_prob = np.max(predicted_proba, axis=1)
        correct = (predicted_class == y_true).astype(np.int64)
        edges = np.asarray(self.bin_edges, dtype=np.float64)
        # np.digitize returns 1-based indices; clamp to valid bin range.
        idx = np.clip(np.digitize(max_prob, edges, right=False) - 1, 0, len(edges) - 2)
        for b in range(len(edges) - 1):
            mask = idx == b
            if not np.any(mask):
                continue
            n_b = int(mask.sum())
            self.bin_counts[b] += n_b
            self.bin_correct[b] += int(correct[mask].sum())
            self.bin_prob_sum[b] += float(max_prob[mask].sum())

    def as_dict(self) -> dict[str, object]:
        rows: list[dict[str, object]] = []
        for b, (lo, hi) in enumerate(
            zip(self.bin_edges[:-1], self.bin_edges[1:], strict=True)
        ):
            n_b = self.bin_counts[b]
            mean_prob = self.bin_prob_sum[b] / n_b if n_b > 0 else 0.0
            empirical_acc = self.bin_correct[b] / n_b if n_b > 0 else 0.0
            rows.append(
                {
                    "bin_low": float(lo),
                    "bin_high": float(hi),
                    "n_rows": int(n_b),
                    "mean_max_predicted_proba": float(mean_prob),
                    "empirical_accuracy": float(empirical_acc),
                    "reliability_gap": float(empirical_acc - mean_prob),
                }
            )
        return {
            "family": self.family,
            "split": self.split,
            "horizon": self.horizon,
            "bins": rows,
        }


# ---------------------------------------------------------------------------
# Train / validation stability deltas
# ---------------------------------------------------------------------------


def stability_delta(
    train_metric: float | None, validation_metric: float | None
) -> float | None:
    """Return ``validation - train`` if both are non-None, else ``None``."""
    if train_metric is None or validation_metric is None:
        return None
    return float(validation_metric - train_metric)


def summarize_train_validation_stability(
    *,
    train_metrics: Mapping[str, object],
    validation_metrics: Mapping[str, object],
) -> dict[str, object]:
    """Return the per-metric ``validation - train`` delta block.

    Keys with values that are not float / int are skipped (descriptive
    only; no PnL / strategy metric ever appears).
    """
    out: dict[str, object] = {}
    for key in ("accuracy", "balanced_accuracy", "macro_f1"):
        t = train_metrics.get(key)
        v = validation_metrics.get(key)
        if isinstance(t, (int, float)) and isinstance(v, (int, float)):
            out[f"{key}_validation_minus_train"] = stability_delta(t, v)
    # Probabilistic deltas (None if either is None).
    t_ll = train_metrics.get("mean_log_loss")
    v_ll = validation_metrics.get("mean_log_loss")
    out["mean_log_loss_validation_minus_train"] = stability_delta(
        t_ll if isinstance(t_ll, (int, float)) else None,
        v_ll if isinstance(v_ll, (int, float)) else None,
    )
    t_br = train_metrics.get("mean_brier_score")
    v_br = validation_metrics.get("mean_brier_score")
    out["mean_brier_validation_minus_train"] = stability_delta(
        t_br if isinstance(t_br, (int, float)) else None,
        v_br if isinstance(v_br, (int, float)) else None,
    )
    return out


# ---------------------------------------------------------------------------
# Helpers for the report-table flattening step
# ---------------------------------------------------------------------------


def flatten_metric_rows(
    *,
    family: str,
    train_metrics: Mapping[str, object] | None,
    validation_metrics: Mapping[str, object] | None,
) -> list[dict[str, object]]:
    """Flatten train/validation metric blocks into CSV-friendly rows.

    Each emitted row carries (family, split, horizon, metric_name,
    metric_value). Returns an empty list if both inputs are None.
    """
    rows: list[dict[str, object]] = []

    def _emit(block: Mapping[str, object] | None) -> None:
        if block is None:
            return
        split = block.get("split")
        horizon = block.get("horizon")
        for key in (
            "n_rows",
            "accuracy",
            "balanced_accuracy",
            "macro_f1",
            "mean_log_loss",
            "mean_brier_score",
            "n_probabilistic_rows",
        ):
            val = block.get(key)
            rows.append(
                {
                    "family": family,
                    "split": split,
                    "horizon": horizon,
                    "metric_name": key,
                    "metric_value": val,
                }
            )
        per_class = block.get("per_class")
        if isinstance(per_class, dict):
            for cls_name, vals in per_class.items():
                if not isinstance(vals, dict):
                    continue
                for vk, vv in vals.items():
                    rows.append(
                        {
                            "family": family,
                            "split": split,
                            "horizon": horizon,
                            "metric_name": f"per_class.{cls_name}.{vk}",
                            "metric_value": vv,
                        }
                    )
        cost = block.get("cost_commensurability")
        if isinstance(cost, dict):
            for ck, cv in cost.items():
                rows.append(
                    {
                        "family": family,
                        "split": split,
                        "horizon": horizon,
                        "metric_name": f"cost_commensurability.{ck}",
                        "metric_value": cv,
                    }
                )

    _emit(train_metrics)
    _emit(validation_metrics)
    return rows


__all__ = [
    "CALIBRATION_BIN_EDGES",
    "CalibrationSummary",
    "ClassBalance",
    "MlBaselineMetricsError",
    "flatten_metric_rows",
    "stability_delta",
    "summarize_train_validation_stability",
]


