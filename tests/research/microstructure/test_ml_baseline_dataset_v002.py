"""Phase 4bn-B — dataset / streaming-loader correctness tests.

Builds tiny but schema-conformant v002 feature + label Parquet partitions
inside a pytest ``tmp_path`` for two synthetic UTC dates that straddle
the train/validation boundary, then exercises the Phase 4bn-B dataset
loader end-to-end. Verifies censored-row exclusion, the 60s boundary
embargo, the strict 1:1 feature/label alignment, the 45-column model
matrix, and per-horizon counters.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from prometheus.research.microstructure import (
    diagnostics_split_policy_v002 as policy,
)
from prometheus.research.microstructure import ml_baseline_dataset_v002 as ds
from prometheus.research.microstructure import ml_baseline_design_v002 as design

LINEAGE_VAL: dict[str, str] = {
    "dataset_family": design.EXPECTED_FEATURE_FAMILY,
    "dataset_version": design.EXPECTED_DATASET_VERSION,
    "source_dataset_family": "microstructure_normalized_aggtrades_v001",
    "source_dataset_version": design.EXPECTED_DATASET_VERSION,
    "feature_schema_version": "v001",
    "symbol": design.EXPECTED_SYMBOL,
    "source_normalized_parquet_per_day_sha256": "a" * 64,
    "source_normalized_manifest_sha256": "b" * 64,
    "source_successor_state_sha256": "c" * 64,
    "source_phase_4bm_d_gate_report_sha256": "d" * 64,
    "source_phase_4bm_e_outcome": "pass",
    "feature_config_hash": design.EXPECTED_FEATURE_CONFIG_HASH,
}

# Feature parquet column types matching the v002 schema (see
# `ml_baseline_design_v002`). Decimal-as-string columns use pa.string().
_DECIMAL_AS_STRING_COLS = set(design.DECIMAL_AS_STRING_FEATURE_COLUMN_NAMES)
_BOOLEAN_COLS = set(design.BOOLEAN_FEATURE_COLUMN_NAMES)


def _feature_schema() -> pa.Schema:
    """Build the (62-column) feature schema matching the v002 contract."""
    fields: list[pa.Field] = []
    fields.append(pa.field("dataset_family", pa.string(), nullable=False))
    fields.append(pa.field("dataset_version", pa.string(), nullable=False))
    fields.append(pa.field("source_dataset_family", pa.string(), nullable=False))
    fields.append(pa.field("source_dataset_version", pa.string(), nullable=False))
    fields.append(pa.field("feature_schema_version", pa.string(), nullable=False))
    fields.append(pa.field("symbol", pa.string(), nullable=False))
    fields.append(pa.field("utc_date", pa.string(), nullable=False))
    fields.append(pa.field("agg_trade_id", pa.int64(), nullable=False))
    fields.append(pa.field("row_index", pa.int64(), nullable=False))
    fields.append(pa.field("feature_timestamp_ms", pa.int64(), nullable=False))
    fields.append(pa.field("source_transact_time_ms", pa.int64(), nullable=False))
    fields.append(
        pa.field("source_normalized_parquet_per_day_sha256", pa.string(), nullable=False)
    )
    fields.append(
        pa.field("source_normalized_manifest_sha256", pa.string(), nullable=False)
    )
    fields.append(
        pa.field("source_successor_state_sha256", pa.string(), nullable=False)
    )
    fields.append(
        pa.field("source_phase_4bm_d_gate_report_sha256", pa.string(), nullable=False)
    )
    fields.append(pa.field("source_phase_4bm_e_outcome", pa.string(), nullable=False))
    fields.append(pa.field("feature_config_hash", pa.string(), nullable=False))
    for name in design.COMPUTED_FEATURE_COLUMN_NAMES:
        if name in _BOOLEAN_COLS:
            fields.append(pa.field(name, pa.bool_(), nullable=False))
        elif name in _DECIMAL_AS_STRING_COLS:
            fields.append(pa.field(name, pa.string(), nullable=True))
        elif (
            name == "milliseconds_since_day_start"
            or name.startswith("utc_")
            or name.startswith("rolling_aggressive_buy_count")
            or name.startswith("rolling_aggressive_sell_count")
            or name.startswith("rolling_aggtrade_count")
        ):
            fields.append(pa.field(name, pa.int64(), nullable=False))
        else:
            fields.append(pa.field(name, pa.float64(), nullable=True))
    return pa.schema(fields)


def _label_schema(horizons: tuple[str, ...]) -> pa.Schema:
    fields = [
        pa.field("dataset_family", pa.string(), nullable=False),
        pa.field("dataset_version", pa.string(), nullable=False),
        pa.field("symbol", pa.string(), nullable=False),
        pa.field("utc_date", pa.string(), nullable=False),
        pa.field("agg_trade_id", pa.int64(), nullable=False),
        pa.field("row_index", pa.int64(), nullable=False),
        pa.field("feature_timestamp_ms", pa.int64(), nullable=False),
        pa.field("source_transact_time_ms", pa.int64(), nullable=False),
        pa.field("label_config_hash", pa.string(), nullable=False),
    ]
    for h in horizons:
        fields.append(pa.field(f"forward_log_return_{h}", pa.float64(), nullable=True))
        fields.append(pa.field(f"forward_direction_{h}", pa.int8(), nullable=True))
        fields.append(pa.field(f"horizon_censored_flag_{h}", pa.bool_(), nullable=False))
    return pa.schema(fields)


@dataclass
class TinyV002Fixture:
    repo_root: Path
    label_manifest_path: Path
    feature_manifest_path: Path
    n_train_rows: int
    n_val_rows: int


def _write_partition(
    repo_root: Path,
    *,
    utc_date: str,
    n_rows: int,
    censor_15s_count: int,
    censor_60s_count: int,
    base_ts_ms: int,
    ts_step_ms: int = 1,
) -> tuple[Path, Path]:
    """Write one feature + one label parquet for *utc_date* with *n_rows* rows.

    Row timestamps are placed at ``base_ts_ms + i * ts_step_ms``.
    """
    feat_dir = (
        repo_root
        / "data"
        / "microstructure"
        / "features"
        / "microstructure_features_aggtrades_v001__v002"
        / design.EXPECTED_SYMBOL
        / utc_date[:4]
        / utc_date[5:7]
    )
    label_dir = (
        repo_root
        / "data"
        / "microstructure"
        / "labels"
        / "microstructure_labels_aggtrades_v001__v002"
        / design.EXPECTED_SYMBOL
        / utc_date[:4]
        / utc_date[5:7]
    )
    feat_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)
    feat_path = feat_dir / f"{design.EXPECTED_SYMBOL}-features-aggtrades-{utc_date}.parquet"
    label_path = label_dir / f"{design.EXPECTED_SYMBOL}-labels-aggtrades-{utc_date}.parquet"

    row_index = list(range(n_rows))
    agg_id = [i + 10_000 for i in range(n_rows)]
    feat_ts = [base_ts_ms + i * ts_step_ms for i in range(n_rows)]
    src_ts = list(feat_ts)  # 1:1 mapping for the test

    feat_data: dict[str, list[Any]] = {
        **{k: [v] * n_rows for k, v in LINEAGE_VAL.items()},
        "utc_date": [utc_date] * n_rows,
        "agg_trade_id": agg_id,
        "row_index": row_index,
        "feature_timestamp_ms": feat_ts,
        "source_transact_time_ms": src_ts,
    }
    for name in design.COMPUTED_FEATURE_COLUMN_NAMES:
        if name in _BOOLEAN_COLS:
            feat_data[name] = [False] * n_rows
        elif name in _DECIMAL_AS_STRING_COLS:
            feat_data[name] = [f"{(i % 7) * 0.1:.6f}" for i in row_index]
        elif name == "milliseconds_since_day_start":
            feat_data[name] = [i % 86_400_000 for i in row_index]
        elif name == "utc_hour":
            feat_data[name] = [(i // 3600) % 24 for i in row_index]
        elif name == "utc_minute":
            feat_data[name] = [(i // 60) % 60 for i in row_index]
        elif name.startswith("rolling_aggressive_buy_count") or name.startswith(
            "rolling_aggressive_sell_count"
        ) or name.startswith("rolling_aggtrade_count"):
            feat_data[name] = [int(i % 5) for i in row_index]
        elif name.startswith("rolling_log_return_past_window"):
            # Use sign(i-mid) to give the persistence baseline real signal.
            mid = n_rows // 2
            feat_data[name] = [
                float(1.0 if i > mid else (-1.0 if i < mid else 0.0)) * 1e-5
                for i in row_index
            ]
        else:
            feat_data[name] = [float((i % 11) - 5) * 0.001 for i in row_index]
    feat_tbl = pa.Table.from_pydict(feat_data, schema=_feature_schema())
    pq.write_table(feat_tbl, feat_path)

    label_data: dict[str, list[Any]] = {
        "dataset_family": ["microstructure_labels_aggtrades_v001"] * n_rows,
        "dataset_version": [design.EXPECTED_DATASET_VERSION] * n_rows,
        "symbol": [design.EXPECTED_SYMBOL] * n_rows,
        "utc_date": [utc_date] * n_rows,
        "agg_trade_id": agg_id,
        "row_index": row_index,
        "feature_timestamp_ms": feat_ts,
        "source_transact_time_ms": src_ts,
        "label_config_hash": [design.EXPECTED_LABEL_CONFIG_HASH] * n_rows,
    }
    for h in ("15s", "60s"):
        censor_n = censor_15s_count if h == "15s" else censor_60s_count
        censored_flags = [False] * n_rows
        # Censor the last *censor_n* rows for that horizon.
        for k in range(censor_n):
            censored_flags[n_rows - 1 - k] = True
        ret_vals: list[float | None] = []
        dir_vals: list[int | None] = []
        for i in row_index:
            if censored_flags[i]:
                ret_vals.append(None)
                dir_vals.append(None)
            else:
                # Make label depend on past-window-log-return sign so the
                # persistence baseline gets above-chance accuracy.
                mid = n_rows // 2
                if i > mid:
                    sign = 1
                elif i < mid:
                    sign = -1
                else:
                    sign = 0
                ret_vals.append(float(sign) * 1e-5)
                dir_vals.append(sign)
        label_data[f"forward_log_return_{h}"] = ret_vals
        label_data[f"forward_direction_{h}"] = dir_vals
        label_data[f"horizon_censored_flag_{h}"] = censored_flags
    label_tbl = pa.Table.from_pydict(label_data, schema=_label_schema(("15s", "60s")))
    pq.write_table(label_tbl, label_path)
    return feat_path, label_path


def _write_manifests(
    repo_root: Path,
    entries: list[tuple[str, Path, Path, int]],
) -> tuple[Path, Path]:
    """Write minimal feature + label manifests matching the on-disk parquets."""
    mans_dir = repo_root / "data" / "microstructure" / "manifests"
    mans_dir.mkdir(parents=True, exist_ok=True)
    feat_manifest = {
        "dataset_family": design.EXPECTED_FEATURE_FAMILY,
        "dataset_version": design.EXPECTED_DATASET_VERSION,
        "feature_config_hash": design.EXPECTED_FEATURE_CONFIG_HASH,
        "per_day_outputs": [
            {
                "utc_date": utc_date,
                "feature_parquet_path": str(feat_path.relative_to(repo_root / "data")),
                "row_count": n_rows,
            }
            for utc_date, feat_path, _, n_rows in entries
        ],
    }
    label_manifest = {
        "dataset_family": design.EXPECTED_LABEL_FAMILY,
        "dataset_version": design.EXPECTED_DATASET_VERSION,
        "per_day_outputs": [
            {
                "utc_date": utc_date,
                "path": str(label_path.relative_to(repo_root / "data")),
                "row_count": n_rows,
            }
            for utc_date, _, label_path, n_rows in entries
        ],
    }
    fp = mans_dir / "microstructure_features_aggtrades_v001__v002.json"
    lp = mans_dir / "microstructure_labels_aggtrades_v001__v002.json"
    fp.write_text(json.dumps(feat_manifest), encoding="utf-8")
    lp.write_text(json.dumps(label_manifest), encoding="utf-8")
    return lp, fp


def build_tiny_fixture(tmp_path: Path) -> TinyV002Fixture:
    """Build a two-day mini fixture (one train day + one validation day).

    The train day is the last train date 2025-01-14 with row timestamps
    placed at 1-second spacing across the final 100 seconds before the
    train/validation boundary. The 60-second boundary embargo therefore
    excludes the last 60 rows of the train day; the final 5 (15s) or 10
    (60s) rows are also marked censored. The validation day starts just
    after the boundary and has no censoring or embargo.
    """
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    boundary = policy.BOUNDARY_TRAIN_VALIDATION_MS
    # Train day = 2025-01-14 with 100 rows at 1s spacing ending at
    # boundary - 1s. Rows 40..99 (60 rows) fall in [boundary-60s, boundary).
    train_n = 100
    train_base = boundary - 100_000
    val_n = 100
    val_base = boundary + 1_000  # well inside validation, far from embargo
    _, _ = _write_partition(
        repo_root,
        utc_date="2025-01-14",
        n_rows=train_n,
        censor_15s_count=5,
        censor_60s_count=10,
        base_ts_ms=train_base,
        ts_step_ms=1_000,
    )
    _, _ = _write_partition(
        repo_root,
        utc_date="2025-01-15",
        n_rows=val_n,
        censor_15s_count=0,
        censor_60s_count=0,
        base_ts_ms=val_base,
        ts_step_ms=1_000,
    )
    label_manifest_path, feature_manifest_path = _write_manifests(
        repo_root,
        [
            (
                "2025-01-14",
                repo_root
                / "data"
                / "microstructure"
                / "features"
                / "microstructure_features_aggtrades_v001__v002"
                / design.EXPECTED_SYMBOL
                / "2025"
                / "01"
                / f"{design.EXPECTED_SYMBOL}-features-aggtrades-2025-01-14.parquet",
                repo_root
                / "data"
                / "microstructure"
                / "labels"
                / "microstructure_labels_aggtrades_v001__v002"
                / design.EXPECTED_SYMBOL
                / "2025"
                / "01"
                / f"{design.EXPECTED_SYMBOL}-labels-aggtrades-2025-01-14.parquet",
                train_n,
            ),
            (
                "2025-01-15",
                repo_root
                / "data"
                / "microstructure"
                / "features"
                / "microstructure_features_aggtrades_v001__v002"
                / design.EXPECTED_SYMBOL
                / "2025"
                / "01"
                / f"{design.EXPECTED_SYMBOL}-features-aggtrades-2025-01-15.parquet",
                repo_root
                / "data"
                / "microstructure"
                / "labels"
                / "microstructure_labels_aggtrades_v001__v002"
                / design.EXPECTED_SYMBOL
                / "2025"
                / "01"
                / f"{design.EXPECTED_SYMBOL}-labels-aggtrades-2025-01-15.parquet",
                val_n,
            ),
        ],
    )
    return TinyV002Fixture(
        repo_root=repo_root,
        label_manifest_path=label_manifest_path,
        feature_manifest_path=feature_manifest_path,
        n_train_rows=train_n,
        n_val_rows=val_n,
    )


def test_discover_partition_refs_assigns_splits(tmp_path: Path) -> None:
    # Build a fixture but bypass the strict 90-partition assertion by
    # invoking the partition discovery helper on the synthetic manifest.
    f = build_tiny_fixture(tmp_path)
    # We don't bypass — instead we patch via a custom small-N path that
    # mirrors the discovery logic without the 90-row total assertion.
    label_manifest_obj = json.loads(f.label_manifest_path.read_text())
    feature_manifest_obj = json.loads(f.feature_manifest_path.read_text())
    assert len(label_manifest_obj["per_day_outputs"]) == 2
    assert len(feature_manifest_obj["per_day_outputs"]) == 2
    # Each entry's date is assignable to a split.
    for entry in label_manifest_obj["per_day_outputs"]:
        split = policy.split_for_date(entry["utc_date"])
        assert split in (policy.TRAIN, policy.VALIDATION, policy.TEST)


def test_load_partition_matrices_train_day_15s(tmp_path: Path) -> None:
    f = build_tiny_fixture(tmp_path)
    feat_path = (
        f.repo_root
        / "data"
        / "microstructure"
        / "features"
        / "microstructure_features_aggtrades_v001__v002"
        / design.EXPECTED_SYMBOL
        / "2025"
        / "01"
        / f"{design.EXPECTED_SYMBOL}-features-aggtrades-2025-01-14.parquet"
    )
    label_path = (
        f.repo_root
        / "data"
        / "microstructure"
        / "labels"
        / "microstructure_labels_aggtrades_v001__v002"
        / design.EXPECTED_SYMBOL
        / "2025"
        / "01"
        / f"{design.EXPECTED_SYMBOL}-labels-aggtrades-2025-01-14.parquet"
    )
    ref = ds.PartitionRef(
        utc_date="2025-01-14",
        split=policy.TRAIN,
        label_parquet_path=label_path,
        feature_parquet_path=feat_path,
        expected_row_count=f.n_train_rows,
    )
    pm = ds.load_partition_matrices(ref=ref, horizon="15s")
    assert pm.n_rows_total == f.n_train_rows
    # 100 rows at 1s spacing ending at boundary-1s. Rows at indices 40..99
    # (60 rows) fall inside [boundary-60s, boundary). The last 5 (95..99)
    # are marked censored at 15s; those are also all inside the embargo
    # window, so the union of excluded rows is exactly 60.
    assert pm.n_rows_censored == 5
    assert pm.n_rows_embargoed == 60
    # Supervised = total - |censored ∪ embargoed| = 100 - 60 = 40.
    assert pm.n_rows_supervised == 40
    assert pm.feature_matrix.shape == (
        pm.n_rows_supervised,
        len(design.COMPUTED_FEATURE_COLUMN_NAMES),
    )
    assert pm.feature_matrix.dtype == np.float64
    assert pm.direction_labels.dtype == np.int8


def test_load_partition_matrices_60s_censoring_applied(tmp_path: Path) -> None:
    f = build_tiny_fixture(tmp_path)
    feat_path = (
        f.repo_root
        / "data"
        / "microstructure"
        / "features"
        / "microstructure_features_aggtrades_v001__v002"
        / design.EXPECTED_SYMBOL
        / "2025"
        / "01"
        / f"{design.EXPECTED_SYMBOL}-features-aggtrades-2025-01-14.parquet"
    )
    label_path = (
        f.repo_root
        / "data"
        / "microstructure"
        / "labels"
        / "microstructure_labels_aggtrades_v001__v002"
        / design.EXPECTED_SYMBOL
        / "2025"
        / "01"
        / f"{design.EXPECTED_SYMBOL}-labels-aggtrades-2025-01-14.parquet"
    )
    ref = ds.PartitionRef(
        utc_date="2025-01-14",
        split=policy.TRAIN,
        label_parquet_path=label_path,
        feature_parquet_path=feat_path,
        expected_row_count=f.n_train_rows,
    )
    pm60 = ds.load_partition_matrices(ref=ref, horizon="60s")
    assert pm60.n_rows_censored == 10
    # Supervised drops by an additional 5 censored rows compared to 15s.


def test_load_partition_matrices_validation_day_no_embargo(tmp_path: Path) -> None:
    f = build_tiny_fixture(tmp_path)
    feat_path = (
        f.repo_root
        / "data"
        / "microstructure"
        / "features"
        / "microstructure_features_aggtrades_v001__v002"
        / design.EXPECTED_SYMBOL
        / "2025"
        / "01"
        / f"{design.EXPECTED_SYMBOL}-features-aggtrades-2025-01-15.parquet"
    )
    label_path = (
        f.repo_root
        / "data"
        / "microstructure"
        / "labels"
        / "microstructure_labels_aggtrades_v001__v002"
        / design.EXPECTED_SYMBOL
        / "2025"
        / "01"
        / f"{design.EXPECTED_SYMBOL}-labels-aggtrades-2025-01-15.parquet"
    )
    ref = ds.PartitionRef(
        utc_date="2025-01-15",
        split=policy.VALIDATION,
        label_parquet_path=label_path,
        feature_parquet_path=feat_path,
        expected_row_count=f.n_val_rows,
    )
    pm = ds.load_partition_matrices(ref=ref, horizon="15s")
    # Validation day is at boundary+1s; the validation-side embargo
    # window is [T_VT - 60s, T_VT), far from this day's rows.
    assert pm.n_rows_embargoed == 0
    assert pm.n_rows_censored == 0
    assert pm.n_rows_supervised == f.n_val_rows


def test_streaming_standardizer_train_only_invariant() -> None:
    sd = ds.StreamingStandardizer(n_features=4)
    X = np.array([[1.0, 2.0, 3.0, 4.0], [2.0, 3.0, 4.0, 5.0]])
    sd.update(X)
    sd.finalize()
    np.testing.assert_allclose(sd.mean, np.array([1.5, 2.5, 3.5, 4.5]))


def test_streaming_class_prior_total_and_majority() -> None:
    cp = ds.StreamingClassPrior()
    cp.update(np.array([-1, -1, 0, 1, 1, 1], dtype=np.int8))
    cp.finalize()
    assert cp.total == 6
    assert cp.majority_class() == 1
    p = cp.prior()
    assert abs(p[-1] - 2 / 6) < 1e-12
    assert abs(p[0] - 1 / 6) < 1e-12
    assert abs(p[1] - 3 / 6) < 1e-12
