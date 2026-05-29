"""Phase 4bn-E — Multi-day v002 train-vs-validation feature drift diagnostics.

Strictly descriptive, two-pass, bounded-memory diagnostic kernel for the
Phase 4bn-B 45-column v002 computed-feature matrix. Reads one per-day
partition at a time, applies the Phase 4bm-U recorded chronological
split policy ``CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO``,
accumulates exact streaming statistics per ``(split, feature)`` and
fixed-width approximate-quantile histograms, and emits descriptive
train-vs-validation drift summaries.

Design constraints (Phase 4bn-E authorization + Phase 4bn-D C-D scope):

- Test holdout (``policy.TEST``) is **never** loaded or iterated. The
  partition iterator raises if asked for the test split.
- Only the 45 Phase 4bn-B ``COMPUTED_FEATURE_COLUMN_NAMES`` are read
  from each feature parquet. The 17 lineage columns are not requested.
  Any column whose name contains a forbidden substring is rejected.
- Read-only against every ``data/microstructure/`` artefact. No
  manifest, sidecar, parquet, gate report, or successor-state file is
  mutated.
- Bounded memory: only the per-feature accumulators (sums, sumsqs,
  min/max, histogram bin counts) are retained across the 90 days.
- Descriptive only. The fixed a-priori drift classification thresholds
  declared here are not selected from results, are not used to rank,
  select, prune, or exclude features, and are not converted into a
  trade signal, threshold, or strategy artefact.
- No model is trained, scored, or predicted. No model binary or
  row-level prediction is persisted. No reusable split mask is
  materialised. No manifest is mutated.
- No network, no credentials, no ``.env``, no ``.mcp.json``, no MCP,
  no Graphify.
"""

from __future__ import annotations

import math
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from . import diagnostics_split_policy_v002 as policy
from . import ml_baseline_design_v002 as design

# ---------------------------------------------------------------------------
# Phase identity
# ---------------------------------------------------------------------------

PHASE_ID = "4bn-e"
SCHEMA_VERSION = "v001"

# ---------------------------------------------------------------------------
# Allowed / forbidden splits (test holdout sealed)
# ---------------------------------------------------------------------------

SUPERVISED_SPLITS: tuple[str, str] = (policy.TRAIN, policy.VALIDATION)
FORBIDDEN_SPLITS: tuple[str, ...] = (policy.TEST,)

# ---------------------------------------------------------------------------
# Histogram parameters (approximate quantiles)
# ---------------------------------------------------------------------------

HISTOGRAM_N_BINS: int = 4096
HISTOGRAM_PADDING: float = 1e-9  # avoid degenerate zero-width ranges

# ---------------------------------------------------------------------------
# Fixed a-priori drift classification thresholds
# ---------------------------------------------------------------------------

# Magnitudes on the standardized mean delta scale. These are predeclared,
# not selected from results, and are not used to rank, select, or prune
# any feature. The classification is descriptive only.
LOW_DRIFT_STD_MEAN_DELTA_MAX: float = 0.10
HIGH_DRIFT_STD_MEAN_DELTA_MIN: float = 0.50

# Minimum train standard deviation considered "safe" for forming
# standardized deltas / std ratios. Below this threshold the feature is
# classified as ``undefined_due_to_zero_or_missing_train_std``.
SAFE_TRAIN_STD_MIN: float = 1e-12

DRIFT_CLASS_LOW = "low_descriptive_drift"
DRIFT_CLASS_MODERATE = "moderate_descriptive_drift"
DRIFT_CLASS_HIGH = "high_descriptive_drift"
DRIFT_CLASS_UNDEFINED = "undefined_due_to_zero_or_missing_train_std"

DRIFT_CLASSES: tuple[str, ...] = (
    DRIFT_CLASS_LOW,
    DRIFT_CLASS_MODERATE,
    DRIFT_CLASS_HIGH,
    DRIFT_CLASS_UNDEFINED,
)

# Strict non-authorization flags emitted on every payload.
NON_AUTHORIZATION_FLAGS: dict[str, bool] = {
    "test_holdout_used": False,
    "models_trained": False,
    "models_scored": False,
    "predictions_generated": False,
    "feature_ranking_authorized": False,
    "feature_selection_authorized": False,
    "feature_pruning_authorized": False,
    "feature_engineering_authorized": False,
    "hyperparameter_tuning_authorized": False,
    "threshold_tuning_authorized": False,
    "probability_to_signal_conversion_authorized": False,
    "strategy_authorized": False,
    "signals_generated": False,
    "pnl_or_backtest_authorized": False,
    "acquisition_authorized": False,
    "manifest_mutation_authorized": False,
    "successor_state_mutation_authorized": False,
    "model_binary_persisted": False,
    "row_level_predictions_persisted": False,
    "reusable_split_mask_persisted": False,
    "data_microstructure_committed": False,
    "data_research_committed": False,
    "called_public_endpoints": False,
    "called_authenticated_endpoints": False,
    "called_private_endpoints": False,
    "opened_websockets": False,
    "opened_user_stream": False,
    "used_credentials": False,
    "read_env_file": False,
    "read_mcp_json": False,
    "used_mcp": False,
    "used_graphify": False,
    "authorized_successor_phase": False,
}


class FeatureDriftError(RuntimeError):
    """Raised when a feature drift diagnostic precondition or input is invalid."""


# ---------------------------------------------------------------------------
# Forbidden-column guard
# ---------------------------------------------------------------------------


def assert_feature_columns_allowed(column_names: Sequence[str]) -> None:
    """Raise :class:`FeatureDriftError` if any forbidden column is in the list.

    A forbidden column is any column that
    :func:`ml_baseline_design_v002.assert_no_forbidden_model_matrix_column`
    rejects (lineage columns + label / split / horizon substrings). This
    helper exists so the diagnostic can fail closed at the very first
    schema check before any data is read.
    """
    for name in column_names:
        try:
            design.assert_no_forbidden_model_matrix_column(name)
        except ValueError as exc:
            raise FeatureDriftError(
                f"forbidden column in drift feature list: {name!r} ({exc})"
            ) from exc


# ---------------------------------------------------------------------------
# Partition reader (raw float64, nulls preserved as NaN)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FeaturePartitionRef:
    """Per-day feature partition reference, scoped to the diagnostic only."""

    utc_date: str
    split: str
    feature_parquet_path: Path


def _feature_columns_to_read() -> tuple[str, ...]:
    """Return the exact list of feature columns the diagnostic reads.

    Only the 45 computed feature columns are read from each per-day
    feature parquet. Lineage columns are never requested.
    """
    return tuple(design.COMPUTED_FEATURE_COLUMN_NAMES)


def _column_to_float64_raw(table: Any, name: str) -> np.ndarray:
    """Return *name* as a float64 ndarray, nulls preserved as NaN.

    Mirrors :func:`ml_baseline_dataset_v002._column_to_float64` but does
    **not** impute nulls. The Decimal-as-string columns are vectorised
    via :func:`pyarrow.compute.cast`. Boolean columns are cast to
    ``{0.0, 1.0}``; the v002 schema guarantees they are non-null, but we
    still pass them through ``float64`` so the accumulator type is
    uniform across all 45 features.
    """
    col = table.column(name)
    if name in design.DECIMAL_AS_STRING_FEATURE_COLUMN_NAMES:
        casted = pc.cast(col, pa.float64())
        return casted.to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
    if name in design.BOOLEAN_FEATURE_COLUMN_NAMES:
        np_arr = col.to_numpy(zero_copy_only=False)
        return np_arr.astype(np.float64)
    return col.to_numpy(zero_copy_only=False).astype(np.float64)


# ---------------------------------------------------------------------------
# Pass 1: streaming exact statistics per (split, feature)
# ---------------------------------------------------------------------------


@dataclass
class FeatureSplitAccumulator:
    """Streaming exact accumulator for one ``(split, feature)`` pair."""

    feature_name: str
    split: str
    count_non_null: int = 0
    null_count: int = 0
    sum_x: float = 0.0
    sum_x2: float = 0.0
    min_value: float = math.inf
    max_value: float = -math.inf

    # Filled by the second pass.
    bin_edges: np.ndarray | None = None
    bin_counts: np.ndarray | None = None
    n_below_min: int = 0
    n_above_max: int = 0

    def update_pass1(self, col_f64: np.ndarray) -> None:
        """Update exact streaming statistics for one per-day column."""
        if col_f64.ndim != 1:
            raise FeatureDriftError(
                f"expected 1-D column for {self.feature_name!r}; got shape {col_f64.shape!r}"
            )
        finite_mask = np.isfinite(col_f64)
        n_finite = int(np.count_nonzero(finite_mask))
        n_null = int(col_f64.shape[0] - n_finite)
        self.count_non_null += n_finite
        self.null_count += n_null
        if n_finite == 0:
            return
        finite = col_f64[finite_mask]
        self.sum_x += float(finite.sum())
        self.sum_x2 += float(np.square(finite).sum())
        local_min = float(finite.min())
        local_max = float(finite.max())
        if local_min < self.min_value:
            self.min_value = local_min
        if local_max > self.max_value:
            self.max_value = local_max

    @property
    def mean(self) -> float:
        if self.count_non_null == 0:
            return float("nan")
        return self.sum_x / float(self.count_non_null)

    @property
    def std(self) -> float:
        if self.count_non_null < 2:
            return 0.0
        mu = self.mean
        var = self.sum_x2 / float(self.count_non_null) - mu * mu
        if var < 0.0:
            var = 0.0
        return math.sqrt(var)

    @property
    def missing_rate(self) -> float:
        n_total = self.count_non_null + self.null_count
        if n_total == 0:
            return 0.0
        return self.null_count / float(n_total)

    def initialise_histogram(self) -> None:
        """Initialise fixed-width bin edges from the min/max collected in pass 1."""
        if not math.isfinite(self.min_value) or not math.isfinite(self.max_value):
            # No finite samples observed; do not allocate histogram.
            self.bin_edges = None
            self.bin_counts = None
            return
        lo = self.min_value
        hi = self.max_value
        if lo == hi:
            # Degenerate single-value distribution; widen by a small epsilon.
            lo = lo - HISTOGRAM_PADDING
            hi = hi + HISTOGRAM_PADDING
        self.bin_edges = np.linspace(lo, hi, HISTOGRAM_N_BINS + 1, dtype=np.float64)
        self.bin_counts = np.zeros(HISTOGRAM_N_BINS, dtype=np.int64)
        self.n_below_min = 0
        self.n_above_max = 0

    def update_pass2(self, col_f64: np.ndarray) -> None:
        """Update histogram bin counts for one per-day column."""
        if self.bin_edges is None or self.bin_counts is None:
            return
        finite_mask = np.isfinite(col_f64)
        if not np.any(finite_mask):
            return
        finite = col_f64[finite_mask]
        edges = self.bin_edges
        lo = float(edges[0])
        hi = float(edges[-1])
        below = finite < lo
        above = finite > hi
        self.n_below_min += int(np.count_nonzero(below))
        self.n_above_max += int(np.count_nonzero(above))
        in_range = finite[~(below | above)]
        if in_range.size == 0:
            return
        idx = np.searchsorted(edges, in_range, side="right") - 1
        # Right-most edge belongs in the last bin.
        np.clip(idx, 0, HISTOGRAM_N_BINS - 1, out=idx)
        np.add.at(self.bin_counts, idx, 1)

    def approximate_quantile(self, q: float) -> float:
        """Return the approximate q-quantile from cumulative bin counts."""
        if not 0.0 <= q <= 1.0:
            raise FeatureDriftError(f"quantile probability out of range: {q!r}")
        if self.bin_edges is None or self.bin_counts is None:
            return float("nan")
        total_in_range = int(self.bin_counts.sum())
        total = total_in_range + self.n_below_min + self.n_above_max
        if total == 0:
            return float("nan")
        target = q * float(total)
        # Below-range slab first.
        if target <= float(self.n_below_min):
            return float(self.min_value)
        # In-range bins.
        cum = float(self.n_below_min)
        for j in range(HISTOGRAM_N_BINS):
            c = float(self.bin_counts[j])
            if cum + c >= target:
                edge_lo = float(self.bin_edges[j])
                edge_hi = float(self.bin_edges[j + 1])
                if c <= 0.0:
                    return edge_lo
                # Linear interpolation within the bin.
                frac = (target - cum) / c
                return edge_lo + frac * (edge_hi - edge_lo)
            cum += c
        # Above-range slab.
        return float(self.max_value)

    def as_dict(self) -> dict[str, Any]:
        return {
            "feature_name": self.feature_name,
            "split": self.split,
            "count_non_null": int(self.count_non_null),
            "null_count": int(self.null_count),
            "missing_rate": float(self.missing_rate),
            "mean": float(self.mean) if math.isfinite(self.mean) else None,
            "std": float(self.std),
            "min": (
                float(self.min_value) if math.isfinite(self.min_value) else None
            ),
            "max": (
                float(self.max_value) if math.isfinite(self.max_value) else None
            ),
            "p01": float(self.approximate_quantile(0.01)),
            "p05": float(self.approximate_quantile(0.05)),
            "p25": float(self.approximate_quantile(0.25)),
            "median": float(self.approximate_quantile(0.50)),
            "p75": float(self.approximate_quantile(0.75)),
            "p95": float(self.approximate_quantile(0.95)),
            "p99": float(self.approximate_quantile(0.99)),
            "n_below_histogram_range": int(self.n_below_min),
            "n_above_histogram_range": int(self.n_above_max),
        }


# ---------------------------------------------------------------------------
# Partition iteration helpers
# ---------------------------------------------------------------------------


def filter_refs_to_supervised(
    refs: Sequence[Any],
) -> tuple[list[Any], list[Any], list[Any]]:
    """Split partition refs into train / validation / sealed-test buckets.

    The returned ``test`` list is for *evidence* only — it records the
    number of test partitions the diagnostic refused to open. The
    diagnostic must never iterate the test list.
    """
    train_refs = [r for r in refs if r.split == policy.TRAIN]
    validation_refs = [r for r in refs if r.split == policy.VALIDATION]
    test_refs = [r for r in refs if r.split == policy.TEST]
    return train_refs, validation_refs, test_refs


def iter_supervised_refs(refs: Sequence[Any], split: str) -> Iterator[Any]:
    """Yield refs for *split*, refusing the sealed test split."""
    if split not in SUPERVISED_SPLITS:
        raise FeatureDriftError(
            f"split {split!r} is not supervised by Phase 4bn-E; "
            f"only {SUPERVISED_SPLITS!r} are allowed"
        )
    for r in refs:
        if r.split == split:
            yield r


def read_feature_columns(path: Path) -> dict[str, np.ndarray]:
    """Return ``{name: float64 ndarray with NaN for nulls}`` for the 45 features."""
    cols = list(_feature_columns_to_read())
    assert_feature_columns_allowed(cols)
    table = pq.read_table(path, columns=cols)
    out: dict[str, np.ndarray] = {}
    for name in cols:
        out[name] = _column_to_float64_raw(table, name)
    return out


# ---------------------------------------------------------------------------
# Two-pass driver
# ---------------------------------------------------------------------------


def make_accumulators() -> dict[tuple[str, str], FeatureSplitAccumulator]:
    """Return a ``(split, feature) -> accumulator`` map for the diagnostic."""
    out: dict[tuple[str, str], FeatureSplitAccumulator] = {}
    for split in SUPERVISED_SPLITS:
        for name in design.COMPUTED_FEATURE_COLUMN_NAMES:
            out[(split, name)] = FeatureSplitAccumulator(
                feature_name=name, split=split
            )
    return out


def run_pass1(
    accumulators: Mapping[tuple[str, str], FeatureSplitAccumulator],
    *,
    refs: Sequence[Any],
    on_partition: Any = None,
) -> None:
    """Run pass 1 (exact streaming stats) over train + validation partitions."""
    for split in SUPERVISED_SPLITS:
        for ref in iter_supervised_refs(refs, split):
            cols = read_feature_columns(ref.feature_parquet_path)
            for name, arr in cols.items():
                accumulators[(split, name)].update_pass1(arr)
            if on_partition is not None:
                on_partition(split=split, ref=ref, n_rows=arr.shape[0])


def initialise_histograms(
    accumulators: Mapping[tuple[str, str], FeatureSplitAccumulator],
) -> None:
    """Initialise per-(split, feature) histogram bin edges from pass-1 min/max."""
    for acc in accumulators.values():
        acc.initialise_histogram()


def run_pass2(
    accumulators: Mapping[tuple[str, str], FeatureSplitAccumulator],
    *,
    refs: Sequence[Any],
    on_partition: Any = None,
) -> None:
    """Run pass 2 (histogram bin counts) over train + validation partitions."""
    for split in SUPERVISED_SPLITS:
        for ref in iter_supervised_refs(refs, split):
            cols = read_feature_columns(ref.feature_parquet_path)
            for name, arr in cols.items():
                accumulators[(split, name)].update_pass2(arr)
            if on_partition is not None:
                on_partition(split=split, ref=ref, n_rows=arr.shape[0])


# ---------------------------------------------------------------------------
# Drift metric / classification
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FeatureDriftRow:
    """Per-feature train-vs-validation drift summary."""

    feature_name: str
    train_count_non_null: int
    train_null_count: int
    train_missing_rate: float
    train_mean: float
    train_std: float
    train_min: float
    train_max: float
    train_p01: float
    train_p05: float
    train_p25: float
    train_median: float
    train_p75: float
    train_p95: float
    train_p99: float
    validation_count_non_null: int
    validation_null_count: int
    validation_missing_rate: float
    validation_mean: float
    validation_std: float
    validation_min: float
    validation_max: float
    validation_p01: float
    validation_p05: float
    validation_p25: float
    validation_median: float
    validation_p75: float
    validation_p95: float
    validation_p99: float
    absolute_mean_delta: float
    standardized_mean_delta: float | None
    absolute_median_delta: float
    validation_to_train_std_ratio: float | None
    absolute_p95_delta: float
    absolute_p05_delta: float
    missing_rate_delta: float
    train_std_is_safe: bool
    drift_classification: str


def classify_drift(
    standardized_mean_delta: float | None,
    *,
    train_std_is_safe: bool,
) -> str:
    """Classify a feature's drift using fixed a-priori magnitude bins.

    The thresholds are predeclared (Phase 4bn-E constants
    :data:`LOW_DRIFT_STD_MEAN_DELTA_MAX` and
    :data:`HIGH_DRIFT_STD_MEAN_DELTA_MIN`), are not selected from
    results, and are not used to rank / select / prune / tune any
    feature. The classification is descriptive only.
    """
    if not train_std_is_safe or standardized_mean_delta is None:
        return DRIFT_CLASS_UNDEFINED
    if not math.isfinite(standardized_mean_delta):
        return DRIFT_CLASS_UNDEFINED
    mag = abs(standardized_mean_delta)
    if mag <= LOW_DRIFT_STD_MEAN_DELTA_MAX:
        return DRIFT_CLASS_LOW
    if mag >= HIGH_DRIFT_STD_MEAN_DELTA_MIN:
        return DRIFT_CLASS_HIGH
    return DRIFT_CLASS_MODERATE


def _safe_div(num: float, denom: float) -> float | None:
    if not math.isfinite(num) or not math.isfinite(denom):
        return None
    if abs(denom) < SAFE_TRAIN_STD_MIN:
        return None
    return num / denom


def compute_drift_row(
    *,
    train_acc: FeatureSplitAccumulator,
    validation_acc: FeatureSplitAccumulator,
) -> FeatureDriftRow:
    """Return the per-feature drift summary for one feature pair."""
    train_mean = train_acc.mean
    train_std = train_acc.std
    val_mean = validation_acc.mean
    val_std = validation_acc.std

    abs_mean_delta = (
        abs(val_mean - train_mean)
        if math.isfinite(val_mean) and math.isfinite(train_mean)
        else float("nan")
    )

    train_std_is_safe = (
        math.isfinite(train_std) and train_std >= SAFE_TRAIN_STD_MIN
    )
    std_mean_delta: float | None
    if train_std_is_safe and math.isfinite(val_mean) and math.isfinite(train_mean):
        std_mean_delta = (val_mean - train_mean) / train_std
    else:
        std_mean_delta = None

    train_median = train_acc.approximate_quantile(0.5)
    val_median = validation_acc.approximate_quantile(0.5)
    abs_median_delta = (
        abs(val_median - train_median)
        if math.isfinite(val_median) and math.isfinite(train_median)
        else float("nan")
    )

    val_train_std_ratio = _safe_div(val_std, train_std) if train_std_is_safe else None

    train_p95 = train_acc.approximate_quantile(0.95)
    val_p95 = validation_acc.approximate_quantile(0.95)
    abs_p95_delta = (
        abs(val_p95 - train_p95)
        if math.isfinite(val_p95) and math.isfinite(train_p95)
        else float("nan")
    )
    train_p05 = train_acc.approximate_quantile(0.05)
    val_p05 = validation_acc.approximate_quantile(0.05)
    abs_p05_delta = (
        abs(val_p05 - train_p05)
        if math.isfinite(val_p05) and math.isfinite(train_p05)
        else float("nan")
    )

    missing_rate_delta = (
        validation_acc.missing_rate - train_acc.missing_rate
    )

    classification = classify_drift(
        std_mean_delta, train_std_is_safe=train_std_is_safe
    )

    return FeatureDriftRow(
        feature_name=train_acc.feature_name,
        train_count_non_null=train_acc.count_non_null,
        train_null_count=train_acc.null_count,
        train_missing_rate=train_acc.missing_rate,
        train_mean=train_mean,
        train_std=train_std,
        train_min=train_acc.min_value if math.isfinite(train_acc.min_value) else float("nan"),
        train_max=train_acc.max_value if math.isfinite(train_acc.max_value) else float("nan"),
        train_p01=train_acc.approximate_quantile(0.01),
        train_p05=train_p05,
        train_p25=train_acc.approximate_quantile(0.25),
        train_median=train_median,
        train_p75=train_acc.approximate_quantile(0.75),
        train_p95=train_p95,
        train_p99=train_acc.approximate_quantile(0.99),
        validation_count_non_null=validation_acc.count_non_null,
        validation_null_count=validation_acc.null_count,
        validation_missing_rate=validation_acc.missing_rate,
        validation_mean=val_mean,
        validation_std=val_std,
        validation_min=(
            validation_acc.min_value
            if math.isfinite(validation_acc.min_value)
            else float("nan")
        ),
        validation_max=(
            validation_acc.max_value
            if math.isfinite(validation_acc.max_value)
            else float("nan")
        ),
        validation_p01=validation_acc.approximate_quantile(0.01),
        validation_p05=val_p05,
        validation_p25=validation_acc.approximate_quantile(0.25),
        validation_median=val_median,
        validation_p75=validation_acc.approximate_quantile(0.75),
        validation_p95=val_p95,
        validation_p99=validation_acc.approximate_quantile(0.99),
        absolute_mean_delta=abs_mean_delta,
        standardized_mean_delta=std_mean_delta,
        absolute_median_delta=abs_median_delta,
        validation_to_train_std_ratio=val_train_std_ratio,
        absolute_p95_delta=abs_p95_delta,
        absolute_p05_delta=abs_p05_delta,
        missing_rate_delta=missing_rate_delta,
        train_std_is_safe=train_std_is_safe,
        drift_classification=classification,
    )


def compute_all_drift_rows(
    accumulators: Mapping[tuple[str, str], FeatureSplitAccumulator],
) -> list[FeatureDriftRow]:
    """Return the per-feature drift rows in the locked feature column order."""
    out: list[FeatureDriftRow] = []
    for name in design.COMPUTED_FEATURE_COLUMN_NAMES:
        train_acc = accumulators[(policy.TRAIN, name)]
        val_acc = accumulators[(policy.VALIDATION, name)]
        out.append(compute_drift_row(train_acc=train_acc, validation_acc=val_acc))
    return out


# ---------------------------------------------------------------------------
# Aggregate summary
# ---------------------------------------------------------------------------


def compute_overview(rows: Sequence[FeatureDriftRow]) -> dict[str, Any]:
    """Return the aggregate-overview JSON payload for the diagnostic."""
    class_counts: dict[str, int] = {c: 0 for c in DRIFT_CLASSES}
    safe_count = 0
    highest_abs_std_mean_delta = float("nan")
    highest_abs_missing_rate_delta = float("nan")
    for r in rows:
        class_counts[r.drift_classification] += 1
        if r.train_std_is_safe:
            safe_count += 1
        if r.standardized_mean_delta is not None and math.isfinite(
            r.standardized_mean_delta
        ):
            mag = abs(r.standardized_mean_delta)
            if not math.isfinite(highest_abs_std_mean_delta) or mag > highest_abs_std_mean_delta:
                highest_abs_std_mean_delta = mag
        miss_mag = abs(r.missing_rate_delta)
        if (
            not math.isfinite(highest_abs_missing_rate_delta)
            or miss_mag > highest_abs_missing_rate_delta
        ):
            highest_abs_missing_rate_delta = miss_mag
    return {
        "phase_id": PHASE_ID,
        "schema_version": SCHEMA_VERSION,
        "n_features_analyzed": len(rows),
        "n_features_low_drift": class_counts[DRIFT_CLASS_LOW],
        "n_features_moderate_drift": class_counts[DRIFT_CLASS_MODERATE],
        "n_features_high_drift": class_counts[DRIFT_CLASS_HIGH],
        "n_features_undefined": class_counts[DRIFT_CLASS_UNDEFINED],
        "n_features_with_safe_train_std": safe_count,
        "n_features_with_zero_or_unsafe_train_std": len(rows) - safe_count,
        "highest_absolute_standardized_mean_delta": (
            float(highest_abs_std_mean_delta)
            if math.isfinite(highest_abs_std_mean_delta)
            else None
        ),
        "highest_absolute_missing_rate_delta": (
            float(highest_abs_missing_rate_delta)
            if math.isfinite(highest_abs_missing_rate_delta)
            else None
        ),
        "drift_classification_thresholds": {
            "low_max_inclusive": LOW_DRIFT_STD_MEAN_DELTA_MAX,
            "high_min_inclusive": HIGH_DRIFT_STD_MEAN_DELTA_MIN,
            "safe_train_std_min": SAFE_TRAIN_STD_MIN,
            "scale": "standardized_mean_delta_magnitude",
            "thresholds_are_fixed_a_priori": True,
            "thresholds_not_selected_from_results": True,
        },
        "no_feature_ranked": True,
        "no_feature_selected": True,
        "no_feature_pruned": True,
        "no_feature_engineered": True,
        "no_strategy_or_signals_generated": True,
        "no_pnl_simulated": True,
        "no_backtest_run": True,
        "no_threshold_tuned": True,
        "no_test_holdout_used": True,
        "non_authorization": dict(NON_AUTHORIZATION_FLAGS),
    }


__all__ = [
    "DRIFT_CLASSES",
    "DRIFT_CLASS_HIGH",
    "DRIFT_CLASS_LOW",
    "DRIFT_CLASS_MODERATE",
    "DRIFT_CLASS_UNDEFINED",
    "FORBIDDEN_SPLITS",
    "FeatureDriftError",
    "FeatureDriftRow",
    "FeaturePartitionRef",
    "FeatureSplitAccumulator",
    "HIGH_DRIFT_STD_MEAN_DELTA_MIN",
    "HISTOGRAM_N_BINS",
    "LOW_DRIFT_STD_MEAN_DELTA_MAX",
    "NON_AUTHORIZATION_FLAGS",
    "PHASE_ID",
    "SAFE_TRAIN_STD_MIN",
    "SCHEMA_VERSION",
    "SUPERVISED_SPLITS",
    "assert_feature_columns_allowed",
    "classify_drift",
    "compute_all_drift_rows",
    "compute_drift_row",
    "compute_overview",
    "filter_refs_to_supervised",
    "initialise_histograms",
    "iter_supervised_refs",
    "make_accumulators",
    "read_feature_columns",
    "run_pass1",
    "run_pass2",
]
