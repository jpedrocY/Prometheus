"""Phase 4bn-AQ — offline tests for the long-horizon ML dataset builder.

These exercise the data-reading builder's pure logic and fail-closed guards
against **synthetic in-memory fixtures and temp dirs only**. They read no local
dataset and never invoke the heavy single run (which reads the real 275+275
partitions). The heavy run is exercised once, separately, by the Phase 4bn-AQ
controlled run and recorded in the implementation report.
"""

from __future__ import annotations

import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import (
    build_longhorizon_ml_dataset_v001 as run_mod,
)
from prometheus.research.microstructure import (
    longhorizon_ml_dataset_contract_v001 as contract,
)
from prometheus.research.microstructure import (
    pre_v002_split_policy as sp,
)
from prometheus.research.microstructure.build_longhorizon_ml_dataset_v001 import (
    LongHorizonMlDatasetRunError,
    PartitionRef,
    _process_partition,
    _RunAccumulators,
)

# ---------------------------------------------------------------------------
# Synthetic parquet fixtures
# ---------------------------------------------------------------------------


def _write_partition(
    tmp_path,
    *,
    date: str,
    n: int,
    feature_values: dict[str, list[float]] | None = None,
    invalid: list[bool] | None = None,
    direction: dict[str, list[int | None]] | None = None,
    censored: dict[str, list[bool]] | None = None,
    reference_ts: dict[str, list[int | None]] | None = None,
    key_offset: int = 0,
    break_alignment_key: str | None = None,
) -> PartitionRef:
    """Write an aligned feature+label parquet pair; return a PartitionRef.

    Defaults produce ``n`` fully-valid rows (no invalid / censored / null) with
    small reference timestamps well inside the segment.
    """
    keys = list(range(key_offset, key_offset + n))
    row_index = keys
    agg_trade_id = [k + 1 for k in keys]
    ft_ms = [1_710_000_000_000 + k for k in keys]
    stt_ms = list(ft_ms)
    utc = [date] * n

    # Feature table: keys + all 45 features (float64).
    feat_cols: dict[str, pa.Array] = {
        "row_index": pa.array(row_index, pa.int64()),
        "agg_trade_id": pa.array(agg_trade_id, pa.int64()),
        "feature_timestamp_ms": pa.array(ft_ms, pa.int64()),
        "source_transact_time_ms": pa.array(stt_ms, pa.int64()),
        "utc_date": pa.array(utc, pa.string()),
    }
    feature_values = feature_values or {}
    for col in contract.ALLOWED_FEATURE_COLUMNS:
        vals = feature_values.get(col, [float(i) for i in range(n)])
        feat_cols[col] = pa.array(vals, pa.float64())
    ftab = pa.table(feat_cols)

    # Label table: keys + invalid flag + per-horizon direction/censored/ref-ts.
    lab_keys = dict(row_index=row_index, agg_trade_id=agg_trade_id,
                    feature_timestamp_ms=ft_ms, source_transact_time_ms=stt_ms,
                    utc_date=utc)
    if break_alignment_key is not None:
        # Corrupt one alignment key on the label side to force a mismatch.
        broken = list(lab_keys[break_alignment_key])
        broken[-1] = broken[-1] + 999_999 if break_alignment_key != "utc_date" else "1999-01-01"
        lab_keys[break_alignment_key] = broken

    lab_cols: dict[str, pa.Array] = {
        "row_index": pa.array(lab_keys["row_index"], pa.int64()),
        "agg_trade_id": pa.array(lab_keys["agg_trade_id"], pa.int64()),
        "feature_timestamp_ms": pa.array(lab_keys["feature_timestamp_ms"], pa.int64()),
        "source_transact_time_ms": pa.array(
            lab_keys["source_transact_time_ms"], pa.int64()
        ),
        "utc_date": pa.array(lab_keys["utc_date"], pa.string()),
        contract.LABEL_INVALID_PRICE_FLAG: pa.array(
            invalid or [False] * n, pa.bool_()
        ),
    }
    for h in contract.HORIZONS:
        dvals = (direction or {}).get(h, [1] * n)
        cvals = (censored or {}).get(h, [False] * n)
        rvals = (reference_ts or {}).get(h, [1_710_000_100_000 + i for i in range(n)])
        lab_cols[contract.DIRECTION_COLUMN_BY_HORIZON[h]] = pa.array(dvals, pa.int8())
        lab_cols[contract.CENSORED_FLAG_COLUMN_BY_HORIZON[h]] = pa.array(
            cvals, pa.bool_()
        )
        lab_cols[contract.REFERENCE_TIMESTAMP_COLUMN_BY_HORIZON[h]] = pa.array(
            rvals, pa.int64()
        )
    ltab = pa.table(lab_cols)

    fpath = tmp_path / f"feat-{date}.parquet"
    lpath = tmp_path / f"lab-{date}.parquet"
    pq.write_table(ftab, fpath)
    pq.write_table(ltab, lpath)
    return PartitionRef(
        date=date,
        split=sp.split_for_date(date),
        feature_parquet=fpath,
        label_parquet=lpath,
        feature_sha256="x" * 64,
        label_sha256="y" * 64,
        row_count=n,
    )


# ---------------------------------------------------------------------------
# Budget preflight / sidecars / hashes
# ---------------------------------------------------------------------------


def test_budget_preflight_passes_and_fails_at_floor():
    assert run_mod.evaluate_budget_preflight(1200.0).passed is True
    pf = run_mod.evaluate_budget_preflight(499.9)
    assert pf.passed is False
    assert pf.breaches and "before start" in pf.breaches[0]


def test_budget_thresholds_match_phase_4bn_l():
    assert run_mod.DERIVED_FOOTPRINT_HARD_GIB == 125
    assert run_mod.D_DRIVE_MIN_FREE_GIB_BEFORE == 500
    assert run_mod.D_DRIVE_FAIL_CLOSED_DURING_GIB == 350


def test_sidecar_roundtrip_and_determinism(tmp_path):
    line = run_mod.sidecar_line("a" * 64, "dataset_manifest.json")
    assert line == "a" * 64 + "  dataset_manifest.json\n"
    sha, name = run_mod.parse_sidecar(line)
    assert sha == "a" * 64 and name == "dataset_manifest.json"

    payload = {"b": 2, "a": 1}
    p = tmp_path / "artefact.json"
    d1, sc = run_mod.write_json_with_sidecar(p, payload)
    body1 = p.read_text()
    # Rewrite the same payload → identical bytes and identical digest.
    d2, _ = run_mod.write_json_with_sidecar(p, payload)
    assert d1 == d2
    assert p.read_text() == body1
    assert sc == "artefact.json.sha256"
    assert json.loads(body1) == payload


@pytest.mark.parametrize(
    "bad",
    ["abc def.json", "a" * 64 + " single.json", "z" * 64 + "  x.json", "a" * 64 + "  "],
)
def test_parse_sidecar_fails_closed(bad):
    with pytest.raises(LongHorizonMlDatasetRunError):
        run_mod.parse_sidecar(bad)


def test_feature_list_hash_matches_ah_45_column_hash():
    h = run_mod.feature_list_hash()
    assert len(h) == 64
    # The long-horizon dataset reuses the exact AH 45-feature list, so its list
    # hash is the well-known AH value.
    assert h.startswith("8e705ba8")


def test_dataset_contract_hash_deterministic():
    assert run_mod.dataset_contract_hash() == run_mod.dataset_contract_hash()
    assert len(run_mod.dataset_contract_hash()) == 64


# ---------------------------------------------------------------------------
# Streaming: alignment / per-horizon support / censoring / transform
# ---------------------------------------------------------------------------


def test_process_partition_counts_full_support_all_horizons(tmp_path):
    ref = _write_partition(tmp_path, date="2024-03-15", n=6)  # train date
    acc = _RunAccumulators()
    _process_partition(ref, acc)
    assert acc.alignment_rows_checked == 6
    assert acc.split_raw_rows["train"] == 6
    for h in contract.HORIZONS:
        assert acc.split_horizon["train"][h]["valid_target"] == 6
        assert acc.split_horizon["train"][h]["censored"] == 0
        assert acc.split_horizon["train"][h]["null_direction"] == 0
        assert acc.split_horizon["train"][h]["class_1"] == 6
    # Train-only transform fit ran over all 6 primary-valid rows.
    assert acc.train_primary_valid_rows == 6
    col = contract.ALLOWED_FEATURE_COLUMNS[0]
    assert acc.feature_stats[col].count == 6


def test_process_partition_excludes_censored_and_invalid_without_imputation(tmp_path):
    # 5 rows: row0 invalid; row1 censored@5m; row2 null direction@5m.
    ref = _write_partition(
        tmp_path,
        date="2024-03-16",  # train
        n=5,
        invalid=[True, False, False, False, False],
        censored={"5m": [False, True, False, False, False],
                  "30m": [False] * 5, "1h": [False] * 5},
        direction={"5m": [1, 1, None, -1, 0],
                   "30m": [1, 1, 1, 1, 1], "1h": [1, 1, 1, 1, 1]},
    )
    acc = _RunAccumulators()
    _process_partition(ref, acc)
    h5 = acc.split_horizon["train"]["5m"]
    assert h5["invalid_price"] == 1
    assert h5["censored"] == 1
    assert h5["null_direction"] == 1
    assert h5["valid_target"] == 2  # rows 3 (dir -1) and 4 (dir 0)
    assert h5["class_-1"] == 1
    assert h5["class_0"] == 1
    assert h5["class_1"] == 0
    # 30m only loses the invalid-price row (precedence: invalid before censored).
    h30 = acc.split_horizon["train"]["30m"]
    assert h30["invalid_price"] == 1
    assert h30["censored"] == 0
    assert h30["valid_target"] == 4
    # Transform fits on 2 primary-valid rows only (row0/row1/row2 excluded).
    assert acc.train_primary_valid_rows == 2
    col = contract.ALLOWED_FEATURE_COLUMNS[0]
    assert acc.feature_stats[col].count == 2


def test_transform_fits_train_only_not_validation(tmp_path):
    val_ref = _write_partition(tmp_path, date="2024-10-15", n=4)  # validation date
    assert val_ref.split == "validation"
    acc = _RunAccumulators()
    _process_partition(val_ref, acc)
    # Validation rows are accounted for support but never enter the transform fit.
    assert acc.split_horizon["validation"]["5m"]["valid_target"] == 4
    assert acc.train_primary_valid_rows == 0
    col = contract.ALLOWED_FEATURE_COLUMNS[0]
    assert acc.feature_stats[col].count == 0


def test_transform_train_mean_is_deterministic_over_kept_rows(tmp_path):
    col = contract.ALLOWED_FEATURE_COLUMNS[0]
    ref = _write_partition(
        tmp_path,
        date="2024-04-01",  # train
        n=4,
        feature_values={col: [10.0, 20.0, 30.0, 40.0]},
        invalid=[True, False, False, False],
        censored={"5m": [False, True, False, False],
                  "30m": [False] * 4, "1h": [False] * 4},
    )
    acc = _RunAccumulators()
    _process_partition(ref, acc)
    # Kept primary rows: indices 2,3 → values 30,40 → mean 35, std 5.
    mean, std = acc.feature_stats[col].mean_std()
    assert mean == pytest.approx(35.0)
    assert std == pytest.approx(5.0)


def test_embargo_date_dropped_in_full_no_horizon_accounting(tmp_path):
    ref = _write_partition(tmp_path, date="2024-10-01", n=3)  # embargo date
    assert ref.split == "embargo"
    acc = _RunAccumulators()
    _process_partition(ref, acc)
    assert acc.split_raw_rows["embargo"] == 3
    assert acc.train_primary_valid_rows == 0
    # No per-horizon model accounting for embargo split.
    assert "embargo" not in acc.split_horizon
    assert acc.per_date[-1]["split"] == "embargo"


def test_alignment_mismatch_fails_closed(tmp_path):
    ref = _write_partition(
        tmp_path, date="2024-03-17", n=4, break_alignment_key="agg_trade_id"
    )
    acc = _RunAccumulators()
    with pytest.raises(LongHorizonMlDatasetRunError):
        _process_partition(ref, acc)


def test_utc_date_mismatch_fails_closed(tmp_path):
    ref = _write_partition(
        tmp_path, date="2024-03-18", n=4, break_alignment_key="utc_date"
    )
    acc = _RunAccumulators()
    with pytest.raises(LongHorizonMlDatasetRunError):
        _process_partition(ref, acc)


# ---------------------------------------------------------------------------
# Boundary crossing (earlier-model-split leakage guard)
# ---------------------------------------------------------------------------


def test_no_boundary_crossing_for_in_bounds_reference_timestamps(tmp_path):
    ref = _write_partition(tmp_path, date="2024-03-20", n=4)  # train
    acc = _RunAccumulators()
    _process_partition(ref, acc)
    assert all(v == 0 for v in acc.boundary_crossings.values())


def test_reference_timestamp_past_boundary_is_counted(tmp_path):
    boundary = sp.BOUNDARY_TRAIN_VALIDATION_MS
    ref = _write_partition(
        tmp_path,
        date="2024-09-30",  # last train date
        n=3,
        reference_ts={
            "5m": [boundary - 10, boundary, boundary + 5],  # 2 crossings
            "30m": [boundary - 1, boundary - 1, boundary - 1],
            "1h": [boundary - 1, boundary - 1, boundary - 1],
        },
    )
    acc = _RunAccumulators()
    _process_partition(ref, acc)
    assert acc.boundary_crossings["train:5m"] == 2
    assert acc.boundary_crossings["train:30m"] == 0


# ---------------------------------------------------------------------------
# One-run guard / namespace / gitignore
# ---------------------------------------------------------------------------


def test_run_refuses_when_dataset_already_built(monkeypatch, tmp_path):
    monkeypatch.setattr(run_mod, "REPO_ROOT", tmp_path)
    out = tmp_path / run_mod.OUTPUT_NAMESPACE
    out.mkdir(parents=True)
    (out / "dataset_manifest.json").write_text("{}", encoding="utf-8")
    with pytest.raises(LongHorizonMlDatasetRunError) as exc:
        run_mod.run(progress=False)
    assert "rerun requires separate operator authorization" in str(exc.value)


def test_output_namespace_is_gitignored_research_path():
    assert run_mod.OUTPUT_NAMESPACE == (
        "data/research/microstructure/ml_datasets/longhorizon_pre_v001"
    )
    assert run_mod.OUTPUT_NAMESPACE.startswith("data/research/")


def test_label_manifest_path_is_the_an_research_namespace():
    assert run_mod.LABEL_MANIFEST_PATH.startswith(
        "data/research/microstructure/labels/"
        "microstructure_labels_longhorizon_aggtrades_v001_pre_v002/"
    )
    assert run_mod.LABEL_MANIFEST_PATH.endswith(".manifest.json")
