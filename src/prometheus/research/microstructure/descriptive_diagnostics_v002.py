"""Phase 4bm-W — multi-day v002 descriptive / structural diagnostics kernel.

Strictly descriptive and structural per-partition diagnostics over the
multi-day v002 BTCUSDT label/feature family
(``microstructure_labels_aggtrades_v001 @ v002``; 90 contiguous UTC dates
2024-12-01 .. 2025-02-28; 155,153,449 rows; horizons 1s/5s/15s/60s),
applying the Phase 4bm-U recorded chronological split policy
``CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`` from
:mod:`prometheus.research.microstructure.diagnostics_split_policy_v002`.

Design constraints (Phase 4bm-W authorization + Phase 4bm-V scope memo):

- Read-only against all ``data/microstructure/`` artefacts. Never writes,
  renames, rewrites, or mutates any parquet, sidecar, manifest, gate report,
  or successor-state artefact.
- Bounded memory: one per-day partition is read at a time and released; only
  exact additive summary statistics and fixed-width histogram bin counts are
  retained across the 90 days. Approximate quantiles are derived from the
  aggregated histograms and are labelled approximate.
- Descriptive only. Phase 4bm-W runs descriptive diagnostics only. This
  module selects, ranks, tunes, fits, trains, simulates, and designs nothing.
  No forward-return distribution computed here is used to select features,
  models, thresholds, or strategies; the test holdout is summarised
  descriptively only and never used for tuning or design.
- No network, no credentials, no ``.env``, no ``.mcp.json``, no MCP, no
  Graphify. This module imports only the Python standard library, numpy,
  pyarrow, and sibling inert modules.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

from . import diagnostics_split_policy_v002 as policy

# ---------------------------------------------------------------------------
# Expected locked constants (mirrors the v002 label/feature manifests)
# ---------------------------------------------------------------------------

EXPECTED_SYMBOL = "BTCUSDT"
EXPECTED_DATASET_VERSION = "v002"
EXPECTED_TOTAL_ROW_COUNT = 155_153_449
EXPECTED_PARTITION_COUNT = 90
EXPECTED_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)
EXPECTED_LABEL_CONFIG_HASH = (
    "352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560"
)
EXPECTED_CENSORED_PER_HORIZON: dict[str, int] = {
    "1s": 14,
    "5s": 39,
    "15s": 170,
    "60s": 634,
}
EXPECTED_INVALID_PRICE_ROW_COUNT = 0

HORIZONS = policy.HORIZONS
HORIZON_MS = policy.HORIZON_MS
ENVELOPE_TERMINAL_UNIX_MS = policy.ENVELOPE_TERMINAL_UNIX_MS

# Fixed-width histogram for approximate forward-log-return quantiles. Symmetric
# about zero; resolution = HISTOGRAM_BIN_WIDTH. Values outside the range are
# accumulated into explicit underflow / overflow counters (never dropped).
HISTOGRAM_RANGE = 0.02
HISTOGRAM_N_BINS = 4000
HISTOGRAM_EDGES: np.ndarray = np.linspace(
    -HISTOGRAM_RANGE, HISTOGRAM_RANGE, HISTOGRAM_N_BINS + 1
)
HISTOGRAM_BIN_WIDTH = (2.0 * HISTOGRAM_RANGE) / HISTOGRAM_N_BINS

# Descriptive |forward_log_return| extreme thresholds.
EXTREME_RETURN_THRESHOLDS: tuple[float, ...] = (1e-4, 1e-3, 5e-3, 1e-2, 5e-2)

# Quantile probabilities reported (descriptive, approximate).
REPORTED_QUANTILES: tuple[float, ...] = (
    0.001,
    0.01,
    0.05,
    0.25,
    0.5,
    0.75,
    0.95,
    0.99,
    0.999,
)

# Columns read from a label partition. The label schema carries
# ``label_config_hash`` (not ``feature_config_hash``; the latter is a
# feature-side column, verified via alignment against the feature parquet).
_LABEL_BASE_COLS = (
    "row_index",
    "agg_trade_id",
    "feature_timestamp_ms",
    "source_transact_time_ms",
    "label_invalid_price_flag",
    "label_any_censored_flag",
    "label_config_hash",
    "symbol",
    "utc_date",
    "dataset_version",
)
_LABEL_PER_HORIZON_COLS = (
    "forward_log_return_{h}",
    "forward_direction_{h}",
    "horizon_censored_flag_{h}",
)
# Shared identity columns present in both label and feature partitions.
_ALIGN_IDENTITY_COLS = (
    "row_index",
    "agg_trade_id",
    "feature_timestamp_ms",
    "source_transact_time_ms",
)
# Feature partition also carries ``feature_config_hash``.
_FEATURE_ALIGN_COLS = (*_ALIGN_IDENTITY_COLS, "feature_config_hash")


class DescriptiveDiagnosticsError(RuntimeError):
    """Raised when a diagnostic input is malformed or a partition is missing."""


# ---------------------------------------------------------------------------
# Per-horizon and per-day accumulators
# ---------------------------------------------------------------------------


@dataclass
class HorizonStats:
    """Exact additive forward-return statistics for one horizon (one scope)."""

    n_rows: int = 0
    n_censored: int = 0
    n_return_nonnull: int = 0
    n_return_null: int = 0
    n_return_pos: int = 0
    n_return_neg: int = 0
    n_return_zero: int = 0
    sum_return: float = 0.0
    sumsq_return: float = 0.0
    min_return: float = math.inf
    max_return: float = -math.inf
    n_dir_pos: int = 0
    n_dir_zero: int = 0
    n_dir_neg: int = 0
    n_dir_null: int = 0
    n_dir_domain_violation: int = 0
    n_dir_sign_mismatch: int = 0
    n_censor_rule_mismatch: int = 0
    n_censored_not_null: int = 0
    extreme_counts: dict[str, int] = field(default_factory=dict)
    hist_underflow: int = 0
    hist_overflow: int = 0
    hist_counts: list[int] = field(default_factory=list)

    def ensure_initialised(self) -> None:
        if not self.hist_counts:
            self.hist_counts = [0] * HISTOGRAM_N_BINS
        if not self.extreme_counts:
            self.extreme_counts = {
                _threshold_key(t): 0 for t in EXTREME_RETURN_THRESHOLDS
            }

    def merge(self, other: HorizonStats) -> None:
        self.ensure_initialised()
        other.ensure_initialised()
        self.n_rows += other.n_rows
        self.n_censored += other.n_censored
        self.n_return_nonnull += other.n_return_nonnull
        self.n_return_null += other.n_return_null
        self.n_return_pos += other.n_return_pos
        self.n_return_neg += other.n_return_neg
        self.n_return_zero += other.n_return_zero
        self.sum_return += other.sum_return
        self.sumsq_return += other.sumsq_return
        self.min_return = min(self.min_return, other.min_return)
        self.max_return = max(self.max_return, other.max_return)
        self.n_dir_pos += other.n_dir_pos
        self.n_dir_zero += other.n_dir_zero
        self.n_dir_neg += other.n_dir_neg
        self.n_dir_null += other.n_dir_null
        self.n_dir_domain_violation += other.n_dir_domain_violation
        self.n_dir_sign_mismatch += other.n_dir_sign_mismatch
        self.n_censor_rule_mismatch += other.n_censor_rule_mismatch
        self.n_censored_not_null += other.n_censored_not_null
        for k in self.extreme_counts:
            self.extreme_counts[k] += other.extreme_counts.get(k, 0)
        self.hist_underflow += other.hist_underflow
        self.hist_overflow += other.hist_overflow
        for i, v in enumerate(other.hist_counts):
            self.hist_counts[i] += v

    def mean(self) -> float | None:
        if self.n_return_nonnull == 0:
            return None
        return self.sum_return / self.n_return_nonnull

    def std(self) -> float | None:
        n = self.n_return_nonnull
        if n == 0:
            return None
        mean = self.sum_return / n
        var = max(self.sumsq_return / n - mean * mean, 0.0)
        return math.sqrt(var)

    def approximate_quantiles(self) -> dict[str, float | None]:
        """Approximate quantiles from the aggregated fixed-width histogram.

        Returns ``None`` per probability when the requested quantile falls in
        the underflow / overflow tail (outside the histogram range), so the
        approximation never silently fabricates a clipped value.
        """
        self.ensure_initialised()
        total = self.hist_underflow + self.hist_overflow + sum(self.hist_counts)
        out: dict[str, float | None] = {}
        if total == 0:
            return {_quantile_key(q): None for q in REPORTED_QUANTILES}
        for q in REPORTED_QUANTILES:
            target = q * total
            out[_quantile_key(q)] = _histogram_quantile(
                target, self.hist_underflow, self.hist_overflow, self.hist_counts
            )
        return out

    def as_dict(self) -> dict[str, Any]:
        self.ensure_initialised()
        return {
            "n_rows": self.n_rows,
            "n_censored": self.n_censored,
            "n_return_nonnull": self.n_return_nonnull,
            "n_return_null": self.n_return_null,
            "n_return_pos": self.n_return_pos,
            "n_return_neg": self.n_return_neg,
            "n_return_zero": self.n_return_zero,
            "return_mean": self.mean(),
            "return_std": self.std(),
            "return_min": None if self.min_return == math.inf else self.min_return,
            "return_max": (
                None if self.max_return == -math.inf else self.max_return
            ),
            "direction_balance": {
                "plus_one": self.n_dir_pos,
                "zero": self.n_dir_zero,
                "minus_one": self.n_dir_neg,
                "null": self.n_dir_null,
            },
            "direction_domain_violations": self.n_dir_domain_violation,
            "direction_sign_mismatch_vs_return": self.n_dir_sign_mismatch,
            "censor_rule_mismatch": self.n_censor_rule_mismatch,
            "censored_row_not_null_violations": self.n_censored_not_null,
            "extreme_abs_return_counts": dict(self.extreme_counts),
            "approximate_quantiles": self.approximate_quantiles(),
            "histogram_underflow": self.hist_underflow,
            "histogram_overflow": self.hist_overflow,
        }


@dataclass
class PartitionSummary:
    """Descriptive summary of one per-day label partition."""

    utc_date: str
    split: str
    row_count: int
    horizon_stats: dict[str, HorizonStats]
    n_invalid_price: int
    n_any_censored: int
    n_any_censored_flag_mismatch: int
    n_row_index_violation: int
    n_src_ne_feature_ts: int
    n_out_of_partition_day: int
    n_split_assignment_mismatch: int
    embargo_count: int
    boundary_crossing_per_horizon: dict[str, int]
    symbol_ok: bool
    dataset_version_ok: bool
    label_config_hash_ok: bool


@dataclass
class AlignmentSummary:
    """Descriptive feature/label alignment summary of one per-day partition."""

    utc_date: str
    split: str
    label_row_count: int
    feature_row_count: int
    row_count_match: bool
    n_row_index_mismatch: int
    n_agg_trade_id_mismatch: int
    n_feature_timestamp_mismatch: int
    n_source_transact_time_mismatch: int
    feature_config_hash_match: bool


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _threshold_key(t: float) -> str:
    return f"abs_gt_{t:g}"


def _quantile_key(q: float) -> str:
    return f"q{q:g}"


def _histogram_quantile(
    target: float, underflow: int, overflow: int, counts: list[int]
) -> float | None:
    """Linear-interpolated quantile from fixed-width histogram bins.

    Returns ``None`` if the target rank falls in the underflow or overflow
    tail (the true value lies outside ``[-HISTOGRAM_RANGE, +HISTOGRAM_RANGE]``).
    """
    if target <= underflow:
        return None
    cum = float(underflow)
    for i, c in enumerate(counts):
        if c == 0:
            continue
        if target <= cum + c:
            frac = (target - cum) / c
            lo = HISTOGRAM_EDGES[i]
            return float(lo + frac * HISTOGRAM_BIN_WIDTH)
        cum += c
    # Falls into the overflow tail.
    return None


def _resolve_data_path(repo_root: Path, relative: str) -> Path:
    return repo_root / "data" / relative


def _read_manifest(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise DescriptiveDiagnosticsError(f"manifest not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise DescriptiveDiagnosticsError(f"manifest is not a JSON object: {path}")
    return data


# ---------------------------------------------------------------------------
# Per-partition computation
# ---------------------------------------------------------------------------


def summarize_label_partition(
    parquet_path: Path, utc_date: str
) -> PartitionSummary:
    """Read one per-day label parquet and compute its descriptive summary.

    Bounded memory: reads only the needed columns of a single day, derives
    exact additive statistics and fixed-width histogram counts, and returns
    them. The parquet table is released when this function returns.
    """
    split = policy.split_for_date(utc_date)
    cols = list(_LABEL_BASE_COLS)
    for tmpl in _LABEL_PER_HORIZON_COLS:
        cols.extend(tmpl.format(h=h) for h in HORIZONS)
    table = pq.read_table(parquet_path, columns=cols)
    n = table.num_rows

    src = table.column("source_transact_time_ms").to_numpy(zero_copy_only=False)
    feat_ts = table.column("feature_timestamp_ms").to_numpy(zero_copy_only=False)
    row_index = table.column("row_index").to_numpy(zero_copy_only=False)

    # Structural / lineage checks.
    n_src_ne_feature_ts = int(np.count_nonzero(src != feat_ts))
    row_index_ok = bool(
        n == 0
        or (
            row_index[0] == 0
            and row_index[-1] == n - 1
            and np.array_equal(row_index, np.arange(n, dtype=row_index.dtype))
        )
    )
    n_row_index_violation = 0 if row_index_ok else n

    day_start = policy.utc_date_start_ms(utc_date)
    day_end = day_start + policy.UTC_DAY_MS
    n_out_of_partition_day = int(
        np.count_nonzero((src < day_start) | (src >= day_end))
    )

    # Split-assignment-by-source check: in-day rows must map to the partition's
    # split; out-of-day rows are already counted above. We verify the partition
    # split equals the split implied by the day window.
    n_split_assignment_mismatch = n_out_of_partition_day

    # Embargo (earlier-split rows within [boundary-60s, boundary)).
    window = policy.earlier_split_embargo_window_ms(split)
    if window is None:
        embargo_count = 0
    else:
        lo, hi = window
        embargo_count = int(np.count_nonzero((src >= lo) & (src < hi)))

    boundary_crossing: dict[str, int] = {}
    for h in HORIZONS:
        bw = policy.boundary_crossing_window_ms(split, h)
        if bw is None:
            boundary_crossing[h] = 0
        else:
            lo, hi = bw
            boundary_crossing[h] = int(np.count_nonzero((src >= lo) & (src < hi)))

    invalid_flag = table.column("label_invalid_price_flag").to_numpy(
        zero_copy_only=False
    )
    n_invalid_price = int(np.count_nonzero(invalid_flag))
    any_censored_flag = table.column("label_any_censored_flag").to_numpy(
        zero_copy_only=False
    )
    n_any_censored = int(np.count_nonzero(any_censored_flag))

    horizon_stats: dict[str, HorizonStats] = {}
    or_of_flags = np.zeros(n, dtype=bool)
    for h in HORIZONS:
        hs = _summarize_horizon(table, h, src, n)
        horizon_stats[h] = hs
        flag = table.column(f"horizon_censored_flag_{h}").to_numpy(
            zero_copy_only=False
        ).astype(bool)
        or_of_flags |= flag

    n_any_censored_flag_mismatch = int(
        np.count_nonzero(any_censored_flag.astype(bool) != or_of_flags)
    )

    # Constancy checks via Arrow-native unique() (avoids materialising a
    # 155M-row python list; only the small distinct set crosses to Python).
    symbol_ok = set(pc.unique(table.column("symbol")).to_pylist()) <= {
        EXPECTED_SYMBOL
    }
    dataset_version_ok = set(
        pc.unique(table.column("dataset_version")).to_pylist()
    ) <= {EXPECTED_DATASET_VERSION}
    label_cfg_ok = set(
        pc.unique(table.column("label_config_hash")).to_pylist()
    ) <= {EXPECTED_LABEL_CONFIG_HASH}

    return PartitionSummary(
        utc_date=utc_date,
        split=split,
        row_count=n,
        horizon_stats=horizon_stats,
        n_invalid_price=n_invalid_price,
        n_any_censored=n_any_censored,
        n_any_censored_flag_mismatch=n_any_censored_flag_mismatch,
        n_row_index_violation=n_row_index_violation,
        n_src_ne_feature_ts=n_src_ne_feature_ts,
        n_out_of_partition_day=n_out_of_partition_day,
        n_split_assignment_mismatch=n_split_assignment_mismatch,
        embargo_count=embargo_count,
        boundary_crossing_per_horizon=boundary_crossing,
        symbol_ok=bool(symbol_ok),
        dataset_version_ok=bool(dataset_version_ok),
        label_config_hash_ok=bool(label_cfg_ok),
    )


def _summarize_horizon(
    table: Any, horizon: str, src: np.ndarray, n: int
) -> HorizonStats:
    hs = HorizonStats()
    hs.ensure_initialised()
    hs.n_rows = n
    h_ms = HORIZON_MS[horizon]

    flag_arr = table.column(f"horizon_censored_flag_{horizon}")
    flag = flag_arr.to_numpy(zero_copy_only=False).astype(bool)
    hs.n_censored = int(np.count_nonzero(flag))

    # Censoring rule: flag == (source_transact_time_ms + h_ms > envelope).
    expected_flag = (src + h_ms) > ENVELOPE_TERMINAL_UNIX_MS
    hs.n_censor_rule_mismatch = int(np.count_nonzero(flag != expected_flag))

    ret_arr = table.column(f"forward_log_return_{horizon}")
    ret_null = ret_arr.is_null().to_numpy(zero_copy_only=False)
    hs.n_return_null = int(np.count_nonzero(ret_null))
    hs.n_return_nonnull = n - hs.n_return_null

    # Censored-row null discipline: censored rows must have null return.
    hs.n_censored_not_null = int(np.count_nonzero(flag & ~ret_null))

    ret_nonnull = ret_arr.drop_null().to_numpy(zero_copy_only=False).astype(
        np.float64
    )
    if ret_nonnull.size:
        hs.sum_return = float(ret_nonnull.sum())
        hs.sumsq_return = float(np.square(ret_nonnull).sum())
        hs.min_return = float(ret_nonnull.min())
        hs.max_return = float(ret_nonnull.max())
        hs.n_return_pos = int(np.count_nonzero(ret_nonnull > 0.0))
        hs.n_return_neg = int(np.count_nonzero(ret_nonnull < 0.0))
        hs.n_return_zero = int(np.count_nonzero(ret_nonnull == 0.0))
        abs_ret = np.abs(ret_nonnull)
        for t in EXTREME_RETURN_THRESHOLDS:
            hs.extreme_counts[_threshold_key(t)] = int(
                np.count_nonzero(abs_ret > t)
            )
        counts, _ = np.histogram(ret_nonnull, bins=HISTOGRAM_EDGES)
        hs.hist_counts = [int(c) for c in counts]
        hs.hist_underflow = int(np.count_nonzero(ret_nonnull < HISTOGRAM_EDGES[0]))
        hs.hist_overflow = int(np.count_nonzero(ret_nonnull > HISTOGRAM_EDGES[-1]))

    # Direction balance + value-domain + sign consistency.
    dir_arr = table.column(f"forward_direction_{horizon}")
    dir_null = dir_arr.is_null().to_numpy(zero_copy_only=False)
    hs.n_dir_null = int(np.count_nonzero(dir_null))
    dir_nn = dir_arr.drop_null()
    hs.n_dir_pos = int(pc.sum(pc.equal(dir_nn, 1)).as_py() or 0)
    hs.n_dir_zero = int(pc.sum(pc.equal(dir_nn, 0)).as_py() or 0)
    hs.n_dir_neg = int(pc.sum(pc.equal(dir_nn, -1)).as_py() or 0)
    hs.n_dir_domain_violation = (
        len(dir_nn) - hs.n_dir_pos - hs.n_dir_zero - hs.n_dir_neg
    )

    # Direction-vs-return sign consistency on rows where both are non-null.
    both = (~ret_null) & (~dir_null)
    if np.count_nonzero(both):
        # Fill nulls with 0.0 before the sign/cast so masked-out (null) rows
        # never trigger an invalid NaN->int cast; ``both`` excludes them anyway.
        ret_full = np.nan_to_num(
            ret_arr.to_numpy(zero_copy_only=False).astype(np.float64), nan=0.0
        )
        dir_full = pc.fill_null(dir_arr, 0).to_numpy(zero_copy_only=False).astype(
            np.int64
        )
        expected_dir = np.sign(ret_full).astype(np.int64)
        hs.n_dir_sign_mismatch = int(
            np.count_nonzero((dir_full != expected_dir) & both)
        )
    return hs


def summarize_alignment_partition(
    label_parquet: Path, feature_parquet: Path, utc_date: str
) -> AlignmentSummary:
    """Per-day feature/label alignment summary (bounded; reads one day each)."""
    split = policy.split_for_date(utc_date)
    label_tbl = pq.read_table(label_parquet, columns=list(_ALIGN_IDENTITY_COLS))
    feat_tbl = pq.read_table(feature_parquet, columns=list(_FEATURE_ALIGN_COLS))
    ln = int(label_tbl.num_rows)
    fn = int(feat_tbl.num_rows)
    match = ln == fn

    def _cmp(col: str) -> int:
        if not match:
            return max(ln, fn)
        a = label_tbl.column(col).to_numpy(zero_copy_only=False)
        b = feat_tbl.column(col).to_numpy(zero_copy_only=False)
        return int(np.count_nonzero(a != b))

    n_row_index = _cmp("row_index")
    n_agg = _cmp("agg_trade_id")
    n_fts = _cmp("feature_timestamp_ms")
    n_src = _cmp("source_transact_time_ms")

    fcfg = set(feat_tbl.column("feature_config_hash").to_pylist())
    cfg_match = fcfg <= {EXPECTED_FEATURE_CONFIG_HASH}

    return AlignmentSummary(
        utc_date=utc_date,
        split=split,
        label_row_count=ln,
        feature_row_count=fn,
        row_count_match=match,
        n_row_index_mismatch=n_row_index,
        n_agg_trade_id_mismatch=n_agg,
        n_feature_timestamp_mismatch=n_fts,
        n_source_transact_time_mismatch=n_src,
        feature_config_hash_match=bool(cfg_match),
    )


# ---------------------------------------------------------------------------
# Orchestration over the 90-day family
# ---------------------------------------------------------------------------


@dataclass
class DiagnosticsInput:
    """Resolved inputs for a full multi-day v002 descriptive diagnostics run."""

    repo_root: Path
    label_manifest_path: Path
    feature_manifest_path: Path


@dataclass
class DiagnosticsRun:
    """Result of a full descriptive diagnostics run (in-memory, pre-report)."""

    partition_summaries: list[PartitionSummary]
    alignment_summaries: list[AlignmentSummary]
    label_manifest: Mapping[str, Any]
    feature_manifest: Mapping[str, Any]
    label_partition_count_on_disk: int
    feature_partition_count_on_disk: int
    label_sidecar_count_on_disk: int
    feature_sidecar_count_on_disk: int


def _count_files(root: Path, suffix: str) -> int:
    if not root.is_dir():
        return 0
    return sum(1 for _ in root.rglob(f"*{suffix}"))


def run_descriptive_diagnostics(inp: DiagnosticsInput) -> DiagnosticsRun:
    """Run the full read-only descriptive diagnostics over all 90 partitions."""
    label_manifest = _read_manifest(inp.label_manifest_path)
    feature_manifest = _read_manifest(inp.feature_manifest_path)

    label_per_day: Sequence[Mapping[str, Any]] = label_manifest["per_day_outputs"]
    feature_by_date: dict[str, Mapping[str, Any]] = {
        e["utc_date"]: e for e in feature_manifest["per_day_outputs"]
    }

    partition_summaries: list[PartitionSummary] = []
    alignment_summaries: list[AlignmentSummary] = []

    for entry in sorted(label_per_day, key=lambda e: e["utc_date"]):
        utc_date = entry["utc_date"]
        label_path = _resolve_data_path(inp.repo_root, entry["path"])
        if not label_path.is_file():
            raise DescriptiveDiagnosticsError(
                f"label partition missing: {label_path}"
            )
        partition_summaries.append(
            summarize_label_partition(label_path, utc_date)
        )

        feat_entry = feature_by_date.get(utc_date)
        if feat_entry is None:
            raise DescriptiveDiagnosticsError(
                f"no feature partition for {utc_date}"
            )
        feature_path = _resolve_data_path(
            inp.repo_root, feat_entry["feature_parquet_path"]
        )
        if not feature_path.is_file():
            raise DescriptiveDiagnosticsError(
                f"feature partition missing: {feature_path}"
            )
        alignment_summaries.append(
            summarize_alignment_partition(label_path, feature_path, utc_date)
        )

    labels_root = inp.repo_root / "data" / "microstructure" / "labels"
    features_root = inp.repo_root / "data" / "microstructure" / "features"
    label_dir = labels_root / "microstructure_labels_aggtrades_v001__v002" / "BTCUSDT"
    feature_dir = (
        features_root / "microstructure_features_aggtrades_v001__v002" / "BTCUSDT"
    )

    return DiagnosticsRun(
        partition_summaries=partition_summaries,
        alignment_summaries=alignment_summaries,
        label_manifest=label_manifest,
        feature_manifest=feature_manifest,
        label_partition_count_on_disk=_count_files(label_dir, ".parquet"),
        feature_partition_count_on_disk=_count_files(feature_dir, ".parquet"),
        label_sidecar_count_on_disk=_count_files(label_dir, ".parquet.sha256"),
        feature_sidecar_count_on_disk=_count_files(feature_dir, ".parquet.sha256"),
    )
