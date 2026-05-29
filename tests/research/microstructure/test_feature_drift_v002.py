"""Phase 4bn-E — feature drift diagnostic kernel tests.

Verifies that the Phase 4bn-E feature drift kernel:

- rejects forbidden columns at the schema check (lineage, label,
  split, censored, horizon substrings) before any data is read;
- refuses to iterate the sealed test split by construction;
- handles a zero-train-std feature without raising
  ``ZeroDivisionError`` and classifies it as
  ``undefined_due_to_zero_or_missing_train_std``;
- uses the fixed a-priori drift classification thresholds (low /
  moderate / high / undefined);
- does not emit a feature ranking, feature selection list, threshold
  recommendation, or strategy artefact;
- writes CSV / JSON outputs that pass the canonical Phase 4bb-F
  sidecar discipline used by Phase 4bn-B.
"""

from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from prometheus.research.microstructure import (
    diagnostics_split_policy_v002 as policy,
)
from prometheus.research.microstructure import feature_drift_v002 as drift
from prometheus.research.microstructure import ml_baseline_design_v002 as design
from prometheus.research.microstructure import ml_baseline_report_v002 as report


def _hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# Forbidden-column guard
# ---------------------------------------------------------------------------


def test_assert_feature_columns_allowed_passes_for_45_locked_features() -> None:
    drift.assert_feature_columns_allowed(design.COMPUTED_FEATURE_COLUMN_NAMES)


def test_assert_feature_columns_allowed_rejects_lineage_columns() -> None:
    for lineage in design.EXCLUDED_LINEAGE_COLUMN_NAMES:
        try:
            drift.assert_feature_columns_allowed([lineage])
        except drift.FeatureDriftError:
            continue
        raise AssertionError(f"lineage column {lineage!r} was not rejected")


def test_assert_feature_columns_allowed_rejects_label_substrings() -> None:
    for name in (
        "forward_log_return_15s",
        "forward_direction_60s",
        "horizon_censored_flag_15s",
        "label_config_hash",
        "split_train",
        "censored_count",
    ):
        try:
            drift.assert_feature_columns_allowed([name])
        except drift.FeatureDriftError:
            continue
        raise AssertionError(f"forbidden column {name!r} was not rejected")


# ---------------------------------------------------------------------------
# Test-split rejection by construction
# ---------------------------------------------------------------------------


class _DummyRef:
    def __init__(self, utc_date: str, split: str) -> None:
        self.utc_date = utc_date
        self.split = split


def test_iter_supervised_refs_rejects_test_split_by_construction() -> None:
    refs = [
        _DummyRef("2025-01-01", policy.TRAIN),
        _DummyRef("2025-02-20", policy.TEST),
    ]
    try:
        list(drift.iter_supervised_refs(refs, policy.TEST))
    except drift.FeatureDriftError as exc:
        assert "test" in str(exc).lower()
        return
    raise AssertionError("iter_supervised_refs(test) must fail closed")


def test_filter_refs_to_supervised_buckets_correctly() -> None:
    refs = [
        _DummyRef("2024-12-01", policy.TRAIN),
        _DummyRef("2025-01-15", policy.VALIDATION),
        _DummyRef("2025-02-14", policy.TEST),
        _DummyRef("2025-02-15", policy.TEST),
    ]
    train, validation, test = drift.filter_refs_to_supervised(refs)
    assert [r.utc_date for r in train] == ["2024-12-01"]
    assert [r.utc_date for r in validation] == ["2025-01-15"]
    assert [r.utc_date for r in test] == ["2025-02-14", "2025-02-15"]


def test_iter_supervised_refs_does_not_yield_test_rows() -> None:
    refs = [
        _DummyRef("2024-12-01", policy.TRAIN),
        _DummyRef("2025-01-15", policy.VALIDATION),
        _DummyRef("2025-02-14", policy.TEST),
    ]
    train_yielded = [r.utc_date for r in drift.iter_supervised_refs(refs, policy.TRAIN)]
    val_yielded = [
        r.utc_date for r in drift.iter_supervised_refs(refs, policy.VALIDATION)
    ]
    assert train_yielded == ["2024-12-01"]
    assert val_yielded == ["2025-01-15"]


# ---------------------------------------------------------------------------
# Accumulator math + zero-train-std handling
# ---------------------------------------------------------------------------


def test_accumulator_exact_stats_on_finite_values() -> None:
    acc = drift.FeatureSplitAccumulator(feature_name="f", split=policy.TRAIN)
    acc.update_pass1(np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64))
    assert acc.count_non_null == 5
    assert acc.null_count == 0
    assert math.isclose(acc.mean, 3.0)
    # Welford-ish exact: variance = mean(x^2) - mean(x)^2 = 11 - 9 = 2 → std = sqrt(2)
    assert math.isclose(acc.std, math.sqrt(2.0), rel_tol=1e-9)
    assert acc.min_value == 1.0
    assert acc.max_value == 5.0


def test_accumulator_handles_nan_as_null() -> None:
    acc = drift.FeatureSplitAccumulator(feature_name="f", split=policy.TRAIN)
    acc.update_pass1(np.array([1.0, float("nan"), 3.0, float("nan")], dtype=np.float64))
    assert acc.count_non_null == 2
    assert acc.null_count == 2
    assert math.isclose(acc.missing_rate, 0.5)
    assert math.isclose(acc.mean, 2.0)


def test_accumulator_zero_std_handled_without_zero_division() -> None:
    acc = drift.FeatureSplitAccumulator(feature_name="constant", split=policy.TRAIN)
    acc.update_pass1(np.full(10, 7.5, dtype=np.float64))
    # std is exactly zero (single-valued sample); the accumulator must
    # not raise when computing it.
    assert acc.std == 0.0
    # Building a drift row with a zero-train-std feature must not raise.
    val_acc = drift.FeatureSplitAccumulator(
        feature_name="constant", split=policy.VALIDATION
    )
    val_acc.update_pass1(np.full(5, 7.6, dtype=np.float64))
    row = drift.compute_drift_row(train_acc=acc, validation_acc=val_acc)
    assert row.train_std == 0.0
    assert row.train_std_is_safe is False
    assert row.standardized_mean_delta is None
    assert row.validation_to_train_std_ratio is None
    assert row.drift_classification == drift.DRIFT_CLASS_UNDEFINED


# ---------------------------------------------------------------------------
# Classification uses fixed a-priori thresholds
# ---------------------------------------------------------------------------


def test_classify_drift_uses_fixed_a_priori_thresholds() -> None:
    assert drift.classify_drift(0.0, train_std_is_safe=True) == drift.DRIFT_CLASS_LOW
    assert (
        drift.classify_drift(drift.LOW_DRIFT_STD_MEAN_DELTA_MAX, train_std_is_safe=True)
        == drift.DRIFT_CLASS_LOW
    )
    assert (
        drift.classify_drift(
            drift.LOW_DRIFT_STD_MEAN_DELTA_MAX + 1e-6, train_std_is_safe=True
        )
        == drift.DRIFT_CLASS_MODERATE
    )
    assert (
        drift.classify_drift(0.3, train_std_is_safe=True) == drift.DRIFT_CLASS_MODERATE
    )
    assert (
        drift.classify_drift(
            drift.HIGH_DRIFT_STD_MEAN_DELTA_MIN, train_std_is_safe=True
        )
        == drift.DRIFT_CLASS_HIGH
    )
    assert (
        drift.classify_drift(-2.0, train_std_is_safe=True) == drift.DRIFT_CLASS_HIGH
    )
    assert (
        drift.classify_drift(None, train_std_is_safe=False)
        == drift.DRIFT_CLASS_UNDEFINED
    )
    assert (
        drift.classify_drift(0.1, train_std_is_safe=False)
        == drift.DRIFT_CLASS_UNDEFINED
    )


def test_classification_is_descriptive_and_not_a_ranking() -> None:
    rows = [
        drift.FeatureDriftRow(
            feature_name=f"feat_{i}",
            train_count_non_null=100,
            train_null_count=0,
            train_missing_rate=0.0,
            train_mean=0.0,
            train_std=1.0,
            train_min=-1.0,
            train_max=1.0,
            train_p01=-1.0,
            train_p05=-0.9,
            train_p25=-0.5,
            train_median=0.0,
            train_p75=0.5,
            train_p95=0.9,
            train_p99=1.0,
            validation_count_non_null=100,
            validation_null_count=0,
            validation_missing_rate=0.0,
            validation_mean=float(i) * 0.05,
            validation_std=1.0,
            validation_min=-1.0,
            validation_max=1.0,
            validation_p01=-1.0,
            validation_p05=-0.9,
            validation_p25=-0.5,
            validation_median=0.0,
            validation_p75=0.5,
            validation_p95=0.9,
            validation_p99=1.0,
            absolute_mean_delta=float(i) * 0.05,
            standardized_mean_delta=float(i) * 0.05,
            absolute_median_delta=0.0,
            validation_to_train_std_ratio=1.0,
            absolute_p95_delta=0.0,
            absolute_p05_delta=0.0,
            missing_rate_delta=0.0,
            train_std_is_safe=True,
            drift_classification=drift.classify_drift(
                float(i) * 0.05, train_std_is_safe=True
            ),
        )
        for i in range(20)
    ]
    overview = drift.compute_overview(rows)
    # The overview must NOT name a "top feature" or emit a per-feature rank.
    assert "top_feature" not in overview
    assert "best_feature" not in overview
    assert "worst_feature" not in overview
    assert "ranked_features" not in overview
    assert "selected_features" not in overview
    assert overview["no_feature_ranked"] is True
    assert overview["no_feature_selected"] is True
    assert overview["no_feature_pruned"] is True
    assert overview["no_feature_engineered"] is True
    assert overview["no_strategy_or_signals_generated"] is True
    assert overview["no_pnl_simulated"] is True
    assert overview["no_backtest_run"] is True
    assert overview["no_threshold_tuned"] is True
    assert overview["no_test_holdout_used"] is True


# ---------------------------------------------------------------------------
# Output schema invariants
# ---------------------------------------------------------------------------


def _required_csv_header() -> set[str]:
    return {
        "feature_name",
        "train_count_non_null",
        "train_null_count",
        "train_missing_rate",
        "train_mean",
        "train_std",
        "train_min",
        "train_max",
        "train_p01",
        "train_p05",
        "train_p25",
        "train_median",
        "train_p75",
        "train_p95",
        "train_p99",
        "validation_count_non_null",
        "validation_null_count",
        "validation_missing_rate",
        "validation_mean",
        "validation_std",
        "validation_min",
        "validation_max",
        "validation_p01",
        "validation_p05",
        "validation_p25",
        "validation_median",
        "validation_p75",
        "validation_p95",
        "validation_p99",
        "absolute_mean_delta",
        "standardized_mean_delta",
        "absolute_median_delta",
        "validation_to_train_std_ratio",
        "absolute_p95_delta",
        "absolute_p05_delta",
        "missing_rate_delta",
        "train_std_is_safe",
        "drift_classification",
    }


def test_drift_summary_csv_header_contains_required_columns() -> None:
    # Import the header builder from the runner module to keep coupling
    # tight to the actual writer.
    from scripts import phase4bn_e_run_feature_drift_v002 as runner

    header = set(runner._drift_summary_header())
    assert _required_csv_header().issubset(header), (
        f"missing columns: {_required_csv_header() - header}"
    )


# ---------------------------------------------------------------------------
# Quantile histogram is approximate but reasonable on a uniform sample
# ---------------------------------------------------------------------------


def test_approximate_quantile_within_one_percent_on_uniform_sample() -> None:
    acc = drift.FeatureSplitAccumulator(feature_name="uniform", split=policy.TRAIN)
    rng = np.random.default_rng(20260529)
    x = rng.uniform(0.0, 10.0, size=200_000)
    acc.update_pass1(x)
    acc.initialise_histogram()
    acc.update_pass2(x)
    # Approximate p50 should be within 0.05 of 5.0 for this resolution.
    assert abs(acc.approximate_quantile(0.50) - 5.0) < 0.05
    assert abs(acc.approximate_quantile(0.05) - 0.5) < 0.05
    assert abs(acc.approximate_quantile(0.95) - 9.5) < 0.05


# ---------------------------------------------------------------------------
# Sidecar discipline (canonical Phase 4bb-F)
# ---------------------------------------------------------------------------


def test_overview_json_writer_writes_canonical_sidecar(tmp_path: Path) -> None:
    out_root = tmp_path / "data" / "research" / "microstructure" / "ml-baselines" / "phase-4bn-e"
    rows: list[drift.FeatureDriftRow] = []
    overview = drift.compute_overview(rows)
    path, sha, sidecar, sidecar_sha = report.write_json_artefact(
        output_root=out_root,
        basename="feature_drift_overview.json",
        payload=overview,
    )
    assert path.exists()
    assert sidecar.exists()
    body = sidecar.read_bytes()
    assert body == f"{sha}  {path.name}\n".encode()
    assert b"\r" not in body
    assert not body.startswith(b"\xef\xbb\xbf")
    assert sidecar_sha == _hash_bytes(body)
    assert re.fullmatch(
        rb"[0-9a-f]{64}  feature_drift_overview\.json\n", body
    ) is not None


def test_summary_csv_writer_writes_canonical_sidecar(tmp_path: Path) -> None:
    from scripts import phase4bn_e_run_feature_drift_v002 as runner

    out_root = tmp_path / "data" / "research" / "microstructure" / "ml-baselines" / "phase-4bn-e"
    header = runner._drift_summary_header()
    path, sha, sidecar, sidecar_sha = report.write_csv_table(
        output_root=out_root,
        basename="feature_drift_summary.csv",
        header=header,
        rows=[],
    )
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "\r" not in text
    body = sidecar.read_bytes()
    assert body == f"{sha}  {path.name}\n".encode()


# ---------------------------------------------------------------------------
# End-to-end on a tiny fixture: read pass1 + pass2 over real parquets
# ---------------------------------------------------------------------------


def _write_minimal_feature_parquet(path: Path, n_rows: int, mean_shift: float) -> None:
    """Write a feature parquet for the diagnostic to read."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[pa.Field] = []
    data: dict[str, list] = {}
    rng = np.random.default_rng(42)
    for name in design.COMPUTED_FEATURE_COLUMN_NAMES:
        if name in design.BOOLEAN_FEATURE_COLUMN_NAMES:
            fields.append(pa.field(name, pa.bool_(), nullable=False))
            data[name] = [False] * n_rows
        elif name in design.DECIMAL_AS_STRING_FEATURE_COLUMN_NAMES:
            fields.append(pa.field(name, pa.string(), nullable=True))
            data[name] = [f"{i * 0.01:.6f}" for i in range(n_rows)]
        elif (
            name == "milliseconds_since_day_start"
            or name.startswith("utc_")
            or name.startswith("rolling_aggressive_buy_count")
            or name.startswith("rolling_aggressive_sell_count")
            or name.startswith("rolling_aggtrade_count")
        ):
            fields.append(pa.field(name, pa.int64(), nullable=False))
            data[name] = [int(i % 100) for i in range(n_rows)]
        else:
            fields.append(pa.field(name, pa.float64(), nullable=True))
            data[name] = [float(rng.normal(mean_shift, 1.0)) for _ in range(n_rows)]
    table = pa.Table.from_pydict(data, schema=pa.schema(fields))
    pq.write_table(table, path)


def test_end_to_end_pass1_and_pass2_on_tiny_synthetic_parquet(tmp_path: Path) -> None:
    train_path = tmp_path / "train.parquet"
    val_path = tmp_path / "val.parquet"
    _write_minimal_feature_parquet(train_path, n_rows=500, mean_shift=0.0)
    _write_minimal_feature_parquet(val_path, n_rows=500, mean_shift=0.0)

    class _R:
        def __init__(self, utc_date: str, split: str, p: Path) -> None:
            self.utc_date = utc_date
            self.split = split
            self.feature_parquet_path = p

    refs = [
        _R("2025-01-01", policy.TRAIN, train_path),
        _R("2025-01-15", policy.VALIDATION, val_path),
    ]
    accumulators = drift.make_accumulators()
    drift.run_pass1(accumulators, refs=refs)
    drift.initialise_histograms(accumulators)
    drift.run_pass2(accumulators, refs=refs)
    rows = drift.compute_all_drift_rows(accumulators)
    assert len(rows) == len(design.COMPUTED_FEATURE_COLUMN_NAMES) == 45
    # No row should explode on the descriptive computation.
    for r in rows:
        # When standardized_mean_delta is defined it must be finite.
        if r.standardized_mean_delta is not None:
            assert math.isfinite(r.standardized_mean_delta)
        # Classification must be one of the four allowed values.
        assert r.drift_classification in drift.DRIFT_CLASSES


def test_end_to_end_refuses_to_load_test_partition(tmp_path: Path) -> None:
    train_path = tmp_path / "train.parquet"
    test_path = tmp_path / "test.parquet"
    _write_minimal_feature_parquet(train_path, n_rows=100, mean_shift=0.0)
    _write_minimal_feature_parquet(test_path, n_rows=100, mean_shift=0.0)

    class _R:
        def __init__(self, utc_date: str, split: str, p: Path) -> None:
            self.utc_date = utc_date
            self.split = split
            self.feature_parquet_path = p

    refs = [
        _R("2025-01-01", policy.TRAIN, train_path),
        _R("2025-02-15", policy.TEST, test_path),
    ]
    accumulators = drift.make_accumulators()
    # Pass 1 must run over only the train and validation partitions; the
    # test partition is silently skipped by the supervised-split filter.
    visited: list[str] = []

    def _on(*, split: str, ref: object, n_rows: int) -> None:
        visited.append(f"{split}:{getattr(ref, 'utc_date', '?')}")

    drift.run_pass1(accumulators, refs=refs, on_partition=_on)
    assert all(not v.startswith("test:") for v in visited)


# ---------------------------------------------------------------------------
# Aggregate overview math
# ---------------------------------------------------------------------------


def test_overview_aggregates_class_counts() -> None:
    # Build five rows: 2 low / 1 moderate / 1 high / 1 undefined.
    def _row(idx: int, std_delta: float | None, train_safe: bool) -> drift.FeatureDriftRow:
        return drift.FeatureDriftRow(
            feature_name=f"f{idx}",
            train_count_non_null=10,
            train_null_count=0,
            train_missing_rate=0.0,
            train_mean=0.0,
            train_std=(1.0 if train_safe else 0.0),
            train_min=-1.0,
            train_max=1.0,
            train_p01=-1.0,
            train_p05=-0.9,
            train_p25=-0.5,
            train_median=0.0,
            train_p75=0.5,
            train_p95=0.9,
            train_p99=1.0,
            validation_count_non_null=10,
            validation_null_count=0,
            validation_missing_rate=0.0,
            validation_mean=0.0 if std_delta is None else std_delta,
            validation_std=1.0,
            validation_min=-1.0,
            validation_max=1.0,
            validation_p01=-1.0,
            validation_p05=-0.9,
            validation_p25=-0.5,
            validation_median=0.0,
            validation_p75=0.5,
            validation_p95=0.9,
            validation_p99=1.0,
            absolute_mean_delta=abs(std_delta) if std_delta is not None else 0.0,
            standardized_mean_delta=std_delta,
            absolute_median_delta=0.0,
            validation_to_train_std_ratio=1.0 if train_safe else None,
            absolute_p95_delta=0.0,
            absolute_p05_delta=0.0,
            missing_rate_delta=0.0,
            train_std_is_safe=train_safe,
            drift_classification=drift.classify_drift(
                std_delta, train_std_is_safe=train_safe
            ),
        )

    rows = [
        _row(0, 0.0, True),
        _row(1, 0.05, True),
        _row(2, 0.25, True),
        _row(3, 1.0, True),
        _row(4, None, False),
    ]
    overview = drift.compute_overview(rows)
    assert overview["n_features_analyzed"] == 5
    assert overview["n_features_low_drift"] == 2
    assert overview["n_features_moderate_drift"] == 1
    assert overview["n_features_high_drift"] == 1
    assert overview["n_features_undefined"] == 1
    assert overview["n_features_with_safe_train_std"] == 4
    assert overview["n_features_with_zero_or_unsafe_train_std"] == 1
    assert overview["highest_absolute_standardized_mean_delta"] == 1.0


# ---------------------------------------------------------------------------
# Non-authorization invariants on the manifest payload
# ---------------------------------------------------------------------------


def test_non_authorization_flags_are_all_false() -> None:
    for k, v in drift.NON_AUTHORIZATION_FLAGS.items():
        assert v is False, f"non-authorization flag {k} must be False"
