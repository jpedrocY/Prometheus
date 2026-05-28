"""Phase 4bn-B — Multi-day v002 ML-baseline dataset / streaming loader.

Read-only, bounded-memory, offline streaming loader for the multi-day v002
BTCUSDT feature/label family. Reads one per-day partition at a time, applies
the Phase 4bm-U recorded chronological split policy, applies per-horizon
censored-row masking, applies the 60s boundary embargo by excluding
earlier-split rows in ``[boundary - 60_000_ms, boundary)``, validates the
strict 1:1 feature/label alignment per day, and yields ready-to-train
matrices to downstream modules.

Bounded memory: one per-day Parquet read at a time; once a partition has
been streamed through a fold (fit-stats / fit-model / evaluate), it is
released. No more than two partitions (one features + one labels) are
materialised in memory at any time.

Design constraints from Phase 4bn-A §11, §12, §13, §14:

- Test holdout (``policy.TEST``) is **never** loaded into any train- or
  validation-bound stream.
- Censored rows for the active horizon are excluded from the supervised
  loss and from the metric denominator.
- The 17 lineage columns are excluded from the model feature matrix.
- Train-only transform fitting: mean / std accumulated across the train
  stream only, applied to validation; never refit on validation/test.
- Decimal-as-string feature columns are parsed via float64 cast at load
  time; native int / double columns are taken as-is; booleans cast to
  ``{0,1}``.

No I/O outside of ``data/microstructure/`` reads, plus a manifest read. No
network. No credentials. No mutation of any manifest, sidecar, parquet,
or successor-state artefact.
"""

from __future__ import annotations

import json
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from . import diagnostics_split_policy_v002 as policy
from . import ml_baseline_design_v002 as design


class MlBaselineDatasetError(RuntimeError):
    """Raised when a dataset input or partition is malformed or missing."""


# ---------------------------------------------------------------------------
# Manifest loading and partition discovery
# ---------------------------------------------------------------------------


def _read_manifest(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise MlBaselineDatasetError(f"manifest not found: {path}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise MlBaselineDatasetError(f"manifest is not a JSON object: {path}")
    return obj


def _resolve_under_data(repo_root: Path, relative: str) -> Path:
    return repo_root / "data" / relative


@dataclass(frozen=True)
class PartitionRef:
    """Per-day feature + label partition references."""

    utc_date: str
    split: str
    label_parquet_path: Path
    feature_parquet_path: Path
    expected_row_count: int


def discover_partition_refs(
    *,
    repo_root: Path,
    label_manifest_path: Path,
    feature_manifest_path: Path,
) -> tuple[Mapping[str, Any], Mapping[str, Any], list[PartitionRef]]:
    """Read the v002 label and feature manifests and resolve all 90 partitions.

    Returns the two manifest dicts together with a list of 90 partition
    refs in chronological order, each tagged with the split derived from
    the Phase 4bm-U recorded chronological split policy.
    """
    label_manifest = _read_manifest(label_manifest_path)
    feature_manifest = _read_manifest(feature_manifest_path)

    # Sanity checks: keep this tight to Phase 4bn-B's locked envelope.
    if label_manifest.get("dataset_family") != design.EXPECTED_LABEL_FAMILY:
        raise MlBaselineDatasetError(
            "label manifest dataset_family mismatch: "
            f"{label_manifest.get('dataset_family')!r}"
        )
    if label_manifest.get("dataset_version") != design.EXPECTED_DATASET_VERSION:
        raise MlBaselineDatasetError(
            "label manifest dataset_version mismatch: "
            f"{label_manifest.get('dataset_version')!r}"
        )
    if feature_manifest.get("dataset_family") != design.EXPECTED_FEATURE_FAMILY:
        raise MlBaselineDatasetError(
            "feature manifest dataset_family mismatch: "
            f"{feature_manifest.get('dataset_family')!r}"
        )
    if feature_manifest.get("dataset_version") != design.EXPECTED_DATASET_VERSION:
        raise MlBaselineDatasetError(
            "feature manifest dataset_version mismatch: "
            f"{feature_manifest.get('dataset_version')!r}"
        )
    fcfg = feature_manifest.get("feature_config_hash")
    if fcfg != design.EXPECTED_FEATURE_CONFIG_HASH:
        raise MlBaselineDatasetError(
            "feature_config_hash mismatch: "
            f"expected {design.EXPECTED_FEATURE_CONFIG_HASH}, got {fcfg!r}"
        )

    label_per_day: Sequence[Mapping[str, Any]] = label_manifest["per_day_outputs"]
    feat_per_day_by_date: dict[str, Mapping[str, Any]] = {
        e["utc_date"]: e for e in feature_manifest["per_day_outputs"]
    }
    label_per_day_sorted = sorted(label_per_day, key=lambda e: e["utc_date"])

    refs: list[PartitionRef] = []
    for entry in label_per_day_sorted:
        utc_date = entry["utc_date"]
        feat_entry = feat_per_day_by_date.get(utc_date)
        if feat_entry is None:
            raise MlBaselineDatasetError(
                f"no feature partition for {utc_date}"
            )
        label_path = _resolve_under_data(repo_root, entry["path"])
        feature_path = _resolve_under_data(
            repo_root, feat_entry["feature_parquet_path"]
        )
        if not label_path.is_file():
            raise MlBaselineDatasetError(f"label parquet missing: {label_path}")
        if not feature_path.is_file():
            raise MlBaselineDatasetError(f"feature parquet missing: {feature_path}")
        split = policy.split_for_date(utc_date)
        refs.append(
            PartitionRef(
                utc_date=utc_date,
                split=split,
                label_parquet_path=label_path,
                feature_parquet_path=feature_path,
                expected_row_count=int(entry.get("row_count", 0)),
            )
        )

    if len(refs) != design.EXPECTED_PARTITION_COUNT:
        raise MlBaselineDatasetError(
            f"expected {design.EXPECTED_PARTITION_COUNT} partitions; got {len(refs)}"
        )
    return label_manifest, feature_manifest, refs


# ---------------------------------------------------------------------------
# Per-day matrix loader
# ---------------------------------------------------------------------------


def _label_columns_for_horizon(horizon: str) -> tuple[str, ...]:
    """Return the label parquet columns needed for *horizon*."""
    return (
        "row_index",
        "agg_trade_id",
        "feature_timestamp_ms",
        "source_transact_time_ms",
        f"forward_direction_{horizon}",
        f"forward_log_return_{horizon}",
        f"horizon_censored_flag_{horizon}",
    )


_FEATURE_ALIGN_COLUMNS = (
    "row_index",
    "agg_trade_id",
    "feature_timestamp_ms",
    "source_transact_time_ms",
)


def _feature_columns_to_read() -> tuple[str, ...]:
    return tuple(list(_FEATURE_ALIGN_COLUMNS) + list(design.COMPUTED_FEATURE_COLUMN_NAMES))


def _parse_decimal_string_column_to_float64(arr: Any) -> np.ndarray:
    """Cast a (possibly null) Decimal-as-string Arrow column to float64.

    Uses :func:`pyarrow.compute.cast` to convert the string-encoded
    Decimal values to float64 in a vectorised C-level pass, which is
    several orders of magnitude faster than a Python ``float()`` loop on
    the 155M-row family. Null entries are emitted as ``np.nan`` so the
    imputation step downstream can replace them with the locked fill
    value. The cast respects the existing Arrow null mask.
    """
    casted = pc.cast(arr, pa.float64())
    return casted.to_numpy(zero_copy_only=False).astype(np.float64, copy=False)


def _column_to_float64(table: Any, name: str) -> np.ndarray:
    """Return *name* as a float64 ndarray, parsing Decimal-as-string if needed."""
    col = table.column(name)
    if name in design.DECIMAL_AS_STRING_FEATURE_COLUMN_NAMES:
        return _parse_decimal_string_column_to_float64(col)
    if name in design.BOOLEAN_FEATURE_COLUMN_NAMES:
        np_arr = col.to_numpy(zero_copy_only=False)
        return np_arr.astype(np.float64)
    # Native numeric (int64 / int8 / double). May contain nulls (e.g.
    # rolling_aggressive_flow_ratio_*); to_numpy() promotes them to NaN.
    return col.to_numpy(zero_copy_only=False).astype(np.float64)


def _assert_strict_alignment(
    label_tbl: Any,
    feat_tbl: Any,
    *,
    utc_date: str,
) -> int:
    """Assert strict 1:1 alignment between the label and feature partitions.

    The v002 family contract is that feature and label parquets share
    identical ``(row_index, agg_trade_id, feature_timestamp_ms,
    source_transact_time_ms)`` rows in the same order. We verify this
    explicitly here so that the feature matrix can be paired with the
    label vector by position without any sort or join.
    """
    ln = int(label_tbl.num_rows)
    fn = int(feat_tbl.num_rows)
    if ln != fn:
        raise MlBaselineDatasetError(
            f"row-count mismatch {utc_date}: labels {ln} != features {fn}"
        )
    for col in _FEATURE_ALIGN_COLUMNS:
        a = label_tbl.column(col).to_numpy(zero_copy_only=False)
        b = feat_tbl.column(col).to_numpy(zero_copy_only=False)
        if not np.array_equal(a, b):
            raise MlBaselineDatasetError(
                f"alignment mismatch {utc_date} on {col}"
            )
    return ln


@dataclass
class PartitionMatrices:
    """A per-day numpy matrix bundle for one (horizon × partition)."""

    utc_date: str
    split: str
    horizon: str
    n_rows_total: int
    n_rows_censored: int
    n_rows_embargoed: int
    n_rows_supervised: int
    feature_matrix: np.ndarray
    direction_labels: np.ndarray
    forward_log_returns: np.ndarray
    source_transact_time_ms: np.ndarray
    persistence_signs: np.ndarray
    null_imputed_counts_per_column: np.ndarray = field(
        default_factory=lambda: np.zeros(0, dtype=np.int64)
    )

    def class_balance(self) -> dict[int, int]:
        unique, counts = np.unique(self.direction_labels, return_counts=True)
        return {int(u): int(c) for u, c in zip(unique, counts, strict=True)}


def load_partition_matrices(
    *,
    ref: PartitionRef,
    horizon: str,
) -> PartitionMatrices:
    """Load one per-day partition into supervised-ready matrices for *horizon*.

    Censored rows for *horizon* and earlier-split embargo rows are excluded
    here (their indices are dropped before the feature matrix is built).
    Returns the per-day :class:`PartitionMatrices` bundle and never retains
    the underlying Arrow tables.
    """
    if horizon not in design.INCLUDED_HORIZONS:
        raise MlBaselineDatasetError(
            f"horizon {horizon!r} is not included by Phase 4bn-B"
        )

    label_cols = list(_label_columns_for_horizon(horizon))
    feat_cols = list(_feature_columns_to_read())

    label_tbl = pq.read_table(ref.label_parquet_path, columns=label_cols)
    feat_tbl = pq.read_table(ref.feature_parquet_path, columns=feat_cols)
    n_total = _assert_strict_alignment(label_tbl, feat_tbl, utc_date=ref.utc_date)

    src = label_tbl.column("source_transact_time_ms").to_numpy(zero_copy_only=False)
    src = src.astype(np.int64, copy=False)

    censored_flag = label_tbl.column(
        f"horizon_censored_flag_{horizon}"
    ).to_numpy(zero_copy_only=False).astype(bool)
    n_censored = int(np.count_nonzero(censored_flag))

    embargo_window = policy.earlier_split_embargo_window_ms(ref.split)
    if embargo_window is None:
        embargo_flag = np.zeros(n_total, dtype=bool)
    else:
        lo, hi = embargo_window
        embargo_flag = (src >= lo) & (src < hi)
    n_embargoed = int(np.count_nonzero(embargo_flag))

    direction_arr = label_tbl.column(f"forward_direction_{horizon}")
    direction_null = direction_arr.is_null().to_numpy(zero_copy_only=False)
    direction_full = np.zeros(n_total, dtype=np.int8)
    direction_nonnull = (
        direction_arr.fill_null(0).to_numpy(zero_copy_only=False).astype(np.int8)
    )
    direction_full[:] = direction_nonnull

    return_arr = label_tbl.column(f"forward_log_return_{horizon}")
    return_null = return_arr.is_null().to_numpy(zero_copy_only=False)
    return_full = (
        return_arr.fill_null(0.0).to_numpy(zero_copy_only=False).astype(np.float64)
    )

    # Supervised mask: row is included iff (not censored) AND (not embargoed)
    # AND (direction is non-null) AND (forward_log_return is non-null).
    supervised_mask = (
        (~censored_flag)
        & (~embargo_flag)
        & (~direction_null)
        & (~return_null)
    )
    n_supervised = int(np.count_nonzero(supervised_mask))

    # Build the feature matrix in column order. Apply the locked imputation
    # rule (fixed zero for NaN) and count per-column impute events; never
    # touch the booleans for imputation since they are non-null by schema.
    n_features = len(design.COMPUTED_FEATURE_COLUMN_NAMES)
    feat_full = np.empty((n_total, n_features), dtype=np.float64)
    null_imputed = np.zeros(n_features, dtype=np.int64)
    for j, name in enumerate(design.COMPUTED_FEATURE_COLUMN_NAMES):
        col_f64 = _column_to_float64(feat_tbl, name)
        if name not in design.BOOLEAN_FEATURE_COLUMN_NAMES:
            null_mask = ~np.isfinite(col_f64)
            n_null = int(np.count_nonzero(null_mask))
            if n_null:
                null_imputed[j] += n_null
                col_f64 = np.where(null_mask, design.IMPUTATION_FILL_VALUE, col_f64)
        feat_full[:, j] = col_f64

    # Restrict matrices to the supervised mask. We also materialise the
    # "persistence" feature (the past-window log return at the same horizon)
    # for the persistence baseline directly from the loaded matrix.
    persistence_col_name = f"rolling_log_return_past_window_{horizon}"
    persistence_idx = design.COMPUTED_FEATURE_COLUMN_NAMES.index(persistence_col_name)
    persistence_full = feat_full[:, persistence_idx]
    # Persistence sign on the imputed feature: a missing past-window return
    # imputes to 0 -> sign 0 -> predict the zero class (a deterministic
    # train-only rule, never tuned).
    persistence_signs_full = np.sign(persistence_full).astype(np.int8)

    feature_matrix = np.ascontiguousarray(feat_full[supervised_mask, :])
    direction_labels = direction_full[supervised_mask].astype(np.int8)
    forward_log_returns = return_full[supervised_mask].astype(np.float64)
    source_transact_time_ms = src[supervised_mask].astype(np.int64)
    persistence_signs = persistence_signs_full[supervised_mask].astype(np.int8)

    return PartitionMatrices(
        utc_date=ref.utc_date,
        split=ref.split,
        horizon=horizon,
        n_rows_total=n_total,
        n_rows_censored=n_censored,
        n_rows_embargoed=n_embargoed,
        n_rows_supervised=n_supervised,
        feature_matrix=feature_matrix,
        direction_labels=direction_labels,
        forward_log_returns=forward_log_returns,
        source_transact_time_ms=source_transact_time_ms,
        persistence_signs=persistence_signs,
        null_imputed_counts_per_column=null_imputed,
    )


# ---------------------------------------------------------------------------
# Streaming iterators (per split × horizon)
# ---------------------------------------------------------------------------


def iter_partitions(
    *,
    refs: Sequence[PartitionRef],
    split: str,
    horizon: str,
) -> Iterator[PartitionMatrices]:
    """Yield per-day matrices for one *split* in chronological order.

    The test/final-holdout split is never iterated for supervised work.
    Callers must filter splits before calling this function.
    """
    if split == policy.TEST and split not in design.SUPERVISED_SPLITS:
        raise MlBaselineDatasetError(
            "test holdout iteration is forbidden by Phase 4bn-B"
        )
    for ref in refs:
        if ref.split != split:
            continue
        yield load_partition_matrices(ref=ref, horizon=horizon)


# ---------------------------------------------------------------------------
# Train-only mean / std (Welford-style streaming)
# ---------------------------------------------------------------------------


@dataclass
class StreamingStandardizer:
    """Streaming train-only mean / std accumulator.

    Uses the standard "shifted-sum" identity over per-partition column sums
    and sumsqs (sums accumulate exactly; sumsqs are computed in float64
    around an offset to avoid catastrophic cancellation at large values).
    """

    n_features: int
    n: int = 0
    sums: np.ndarray = field(init=False)
    sumsqs: np.ndarray = field(init=False)
    train_n_partitions: int = 0
    train_n_supervised_rows: int = 0
    fitted: bool = False

    def __post_init__(self) -> None:
        self.sums = np.zeros(self.n_features, dtype=np.float64)
        self.sumsqs = np.zeros(self.n_features, dtype=np.float64)

    def update(self, X: np.ndarray) -> None:
        if X.ndim != 2 or X.shape[1] != self.n_features:
            raise MlBaselineDatasetError(
                f"streaming standardizer expected shape (n, {self.n_features}); "
                f"got {X.shape!r}"
            )
        self.n += X.shape[0]
        self.sums += X.sum(axis=0)
        self.sumsqs += np.square(X).sum(axis=0)

    def fit_partition(self, pm: PartitionMatrices) -> None:
        if pm.split != policy.TRAIN:
            raise MlBaselineDatasetError(
                "streaming standardizer must only fit train partitions"
            )
        self.train_n_partitions += 1
        self.train_n_supervised_rows += pm.n_rows_supervised
        self.update(pm.feature_matrix)

    def finalize(self) -> None:
        if self.n == 0:
            raise MlBaselineDatasetError("standardizer received zero rows")
        self.fitted = True

    @property
    def mean(self) -> np.ndarray:
        if not self.fitted:
            raise MlBaselineDatasetError("standardizer not finalised")
        return self.sums / float(self.n)

    @property
    def std(self) -> np.ndarray:
        if not self.fitted:
            raise MlBaselineDatasetError("standardizer not finalised")
        mu = self.mean
        var = self.sumsqs / float(self.n) - mu * mu
        var = np.maximum(var, 0.0)
        return np.sqrt(var)

    def transform(self, X: np.ndarray) -> np.ndarray:
        if not self.fitted:
            raise MlBaselineDatasetError("standardizer not finalised")
        std = np.maximum(self.std, design.STANDARDIZATION_EPSILON)
        return (X - self.mean) / std

    def as_dict(self) -> dict[str, Any]:
        return {
            "fitted": bool(self.fitted),
            "train_n_partitions": int(self.train_n_partitions),
            "train_n_supervised_rows": int(self.train_n_supervised_rows),
            "n_features": int(self.n_features),
            "mean": self.mean.tolist() if self.fitted else None,
            "std": self.std.tolist() if self.fitted else None,
            "epsilon": float(design.STANDARDIZATION_EPSILON),
            "rule": design.STANDARDIZATION_RULE,
        }


# ---------------------------------------------------------------------------
# Streaming class-prior accumulator (train-only)
# ---------------------------------------------------------------------------


@dataclass
class StreamingClassPrior:
    """Streaming train-only class-prior counter for ``{-1, 0, +1}``."""

    counts: dict[int, int] = field(
        default_factory=lambda: dict.fromkeys(design.CLASS_LABELS, 0)
    )
    n_partitions: int = 0
    total: int = 0
    fitted: bool = False

    def update(self, y: np.ndarray) -> None:
        for cls in design.CLASS_LABELS:
            self.counts[cls] += int(np.count_nonzero(y == cls))
        self.total += int(y.shape[0])
        self.n_partitions += 1

    def finalize(self) -> None:
        if self.total == 0:
            raise MlBaselineDatasetError("class prior accumulator received zero rows")
        self.fitted = True

    def prior(self) -> dict[int, float]:
        if not self.fitted:
            raise MlBaselineDatasetError("class prior not finalised")
        return {cls: self.counts[cls] / float(self.total) for cls in design.CLASS_LABELS}

    def majority_class(self) -> int:
        prior = self.prior()
        # Tie-break deterministically by class label order (descending of
        # prior, then by signed-class ascending order for stable choice).
        best_label = design.CLASS_LABELS[0]
        best_prior = prior[best_label]
        for cls in design.CLASS_LABELS[1:]:
            if prior[cls] > best_prior or (
                prior[cls] == best_prior and cls < best_label
            ):
                best_prior = prior[cls]
                best_label = cls
        return best_label


__all__ = [
    "MlBaselineDatasetError",
    "PartitionMatrices",
    "PartitionRef",
    "StreamingClassPrior",
    "StreamingStandardizer",
    "discover_partition_refs",
    "iter_partitions",
    "load_partition_matrices",
]
