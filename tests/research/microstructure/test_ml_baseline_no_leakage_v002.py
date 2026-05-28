"""Phase 4bn-B — no-leakage tests for the ML-baseline model feature matrix.

Ensures the 45-column model feature matrix never includes any of the 17
v002 lineage columns, never includes any label column, never includes any
split-flag column, and never includes any column containing one of the
forbidden substrings declared in
:data:`ml_baseline_design_v002.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`. Also
verifies that train-only standardization is preserved (the validation
mean/std is never re-fit).
"""

from __future__ import annotations

import numpy as np

from prometheus.research.microstructure import (
    diagnostics_split_policy_v002 as policy,
)
from prometheus.research.microstructure import ml_baseline_dataset_v002 as ds
from prometheus.research.microstructure import ml_baseline_design_v002 as design


def test_no_lineage_columns_in_model_matrix_name_list() -> None:
    for name in design.EXCLUDED_LINEAGE_COLUMN_NAMES:
        assert name not in design.COMPUTED_FEATURE_COLUMN_NAMES, (
            f"lineage column {name!r} must not appear in the model matrix"
        )


def test_no_forbidden_substrings_in_model_matrix_name_list() -> None:
    for col in design.COMPUTED_FEATURE_COLUMN_NAMES:
        for sub in design.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS:
            assert sub not in col, (
                f"column {col!r} contains forbidden substring {sub!r}"
            )


def test_assert_no_forbidden_model_matrix_column_raises_on_lineage() -> None:
    for name in design.EXCLUDED_LINEAGE_COLUMN_NAMES:
        try:
            design.assert_no_forbidden_model_matrix_column(name)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError on lineage {name!r}")


def test_assert_no_forbidden_model_matrix_column_raises_on_label() -> None:
    for name in (
        "forward_log_return_15s",
        "forward_direction_60s",
        "horizon_censored_flag_15s",
        "label_invalid_price_flag",
    ):
        try:
            design.assert_no_forbidden_model_matrix_column(name)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError on label/derived {name!r}")


def test_assert_no_forbidden_model_matrix_column_accepts_each_feature_name() -> None:
    for name in design.COMPUTED_FEATURE_COLUMN_NAMES:
        # Should NOT raise.
        design.assert_no_forbidden_model_matrix_column(name)


def test_train_only_standardizer_refuses_non_train_partition() -> None:
    sd = ds.StreamingStandardizer(n_features=4)

    # Build a synthetic non-train partition matrix to fit.
    pm = ds.PartitionMatrices(
        utc_date="2025-01-15",
        split=policy.VALIDATION,
        horizon="15s",
        n_rows_total=4,
        n_rows_censored=0,
        n_rows_embargoed=0,
        n_rows_supervised=4,
        feature_matrix=np.zeros((4, 4)),
        direction_labels=np.zeros(4, dtype=np.int8),
        forward_log_returns=np.zeros(4),
        source_transact_time_ms=np.zeros(4, dtype=np.int64),
        persistence_signs=np.zeros(4, dtype=np.int8),
    )
    try:
        sd.fit_partition(pm)
    except ds.MlBaselineDatasetError:
        return
    raise AssertionError("expected MlBaselineDatasetError on validation partition")


def test_train_only_standardizer_runs_on_train_partition() -> None:
    sd = ds.StreamingStandardizer(n_features=3)
    pm = ds.PartitionMatrices(
        utc_date="2024-12-01",
        split=policy.TRAIN,
        horizon="15s",
        n_rows_total=2,
        n_rows_censored=0,
        n_rows_embargoed=0,
        n_rows_supervised=2,
        feature_matrix=np.array([[1.0, 2.0, 3.0], [3.0, 4.0, 5.0]]),
        direction_labels=np.array([1, -1], dtype=np.int8),
        forward_log_returns=np.array([1e-5, -1e-5]),
        source_transact_time_ms=np.array([0, 1], dtype=np.int64),
        persistence_signs=np.array([1, -1], dtype=np.int8),
    )
    sd.fit_partition(pm)
    sd.finalize()
    np.testing.assert_allclose(sd.mean, np.array([2.0, 3.0, 4.0]))
    assert sd.train_n_supervised_rows == 2


def test_excluded_lineage_count_is_seventeen() -> None:
    assert len(design.EXCLUDED_LINEAGE_COLUMN_NAMES) == 17


def test_computed_feature_count_is_fortyfive() -> None:
    assert len(design.COMPUTED_FEATURE_COLUMN_NAMES) == 45
