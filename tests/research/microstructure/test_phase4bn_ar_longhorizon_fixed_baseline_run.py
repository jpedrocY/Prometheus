"""Phase 4bn-AR — runner tests: AQ verification, one-run guard, end-to-end fixture.

The AQ artefact verification is exercised fail-closed on a synthetic namespace; the
one-run/no-overwrite guard is enforced; and the full ``run()`` orchestration is
exercised end-to-end on a tiny synthetic feature/label Parquet fixture (all AQ
source-binding checks monkeypatched to synthetic values) to prove it trains, scores,
computes a verdict, writes only compact artefacts (no row-level predictions), keeps
every published authorization flag ``False``, and never invokes
``flip_research_eligible``. The heavy real streaming run is exercised only by the
single authorized controlled run (recorded in the Phase 4bn-AR report), not here.
"""

from __future__ import annotations

import json

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import build_longhorizon_ml_dataset_v001 as aq
from prometheus.research.microstructure import longhorizon_fixed_baseline_run_v001 as ar
from prometheus.research.microstructure import longhorizon_ml_dataset_contract_v001 as contract

# ---------------------------------------------------------------------------
# Synthetic AQ artefact namespace (structure + sidecar verification)
# ---------------------------------------------------------------------------


def _support_block(valid: int) -> dict:
    return {"valid_target": valid, "censored": 0, "null_direction": 0, "invalid_price": 0,
            "class_-1": valid // 2, "class_0": 0, "class_1": valid - valid // 2}


def _synthetic_aq_artefacts() -> dict[str, dict]:
    per_feature = {c: {"train_mean": 0.0, "train_std": 1.0, "standardization_denominator": 1.0,
                       "train_count": 10, "train_null_count": 0}
                   for c in contract.ALLOWED_FEATURE_COLUMNS}
    manifest = {
        "dataset_contract_hash": ar.EXPECTED_DATASET_CONTRACT_HASH,
        "feature_count": 45,
        "feature_list": list(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list_hash": ar.EXPECTED_FEATURE_LIST_HASH,
        "streamed_row_count": contract.EXPECTED_ROW_COUNT,
        "source_bindings": {
            "label_family": contract.LABEL_FAMILY,
            "label_config_hash": contract.LABEL_CONFIG_HASH,
            "label_manifest_sha256": ar.EXPECTED_AN_LABEL_MANIFEST_SHA256,
            "feature_manifest_sha256": "f" * 64,
        },
        "split_raw_rows": {
            "train": 304_816_127, "embargo": 3_071_370,
            "validation": 68_578_296, "holdout": 23_535_902,
        },
        "per_split_horizon_support": {
            sp: {h: _support_block(v) for h, v in hm.items()}
            for sp, hm in ar.EXPECTED_SUPPORT.items()
        },
        "non_authorization_flags": {"a": False, "b": False},
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "test_rows_loaded": 0,
        "dependence_caveat": "overlapping long-horizon labels; rows are NOT independent.",
    }
    per_date = (
        [{"date": f"t{i}", "split": "train"} for i in range(214)]
        + [{"date": f"e{i}", "split": "embargo"} for i in range(2)]
        + [{"date": f"v{i}", "split": "validation"} for i in range(45)]
        + [{"date": f"h{i}", "split": "holdout"} for i in range(14)]
    )
    return {
        "dataset_manifest.json": manifest,
        "split_index.json": {"per_date": per_date},
        "train_only_transform.json": {
            "fit_split": "train",
            "standardization_rule": contract.STANDARDIZATION_RULE,
            "standardization_epsilon": contract.STANDARDIZATION_EPSILON,
            "imputation_fill_value": contract.IMPUTATION_FILL_VALUE,
            "train_primary_valid_rows": 304_816_127,
            "feature_list_hash": ar.EXPECTED_FEATURE_LIST_HASH,
            "per_feature": per_feature,
        },
        "leakage_split_integrity_proof.json": {
            "dataset_contract_hash": ar.EXPECTED_DATASET_CONTRACT_HASH,
            "alignment_mismatches": 0,
            "per_horizon_boundary_crossing_rows": {"train:5m": 0, "validation:5m": 0},
            "v002_terminal_window_read": False,
            "sealed_test_split_touched": False,
            "test_rows_loaded": 0,
            "data_committed": False,
        },
        "source_binding.json": {"dataset_contract_hash": ar.EXPECTED_DATASET_CONTRACT_HASH},
        "sidecar_inventory.json": {"entries": []},
        "build_run_record.json": {"phase": "phase-4bn-aq"},
    }


def _write_aq_namespace(base, artefacts: dict[str, dict]) -> None:
    base.mkdir(parents=True, exist_ok=True)
    for name, payload in artefacts.items():
        aq.write_json_with_sidecar(base / name, payload)


def test_load_and_verify_aq_artefacts_passes(tmp_path, monkeypatch) -> None:
    ns = tmp_path / "aq_ns"
    _write_aq_namespace(ns, _synthetic_aq_artefacts())
    monkeypatch.setattr(ar, "REPO_ROOT", tmp_path)
    art = ar.load_and_verify_aq_artefacts(namespace="aq_ns")
    assert art.manifest["feature_count"] == 45
    assert art.transform["fit_split"] == "train"
    assert len(art.sha256) == 7


def test_missing_aq_artefact_fails_closed(tmp_path, monkeypatch) -> None:
    (tmp_path / "aq_ns").mkdir()
    monkeypatch.setattr(ar, "REPO_ROOT", tmp_path)
    with pytest.raises(ar.LongHorizonFixedBaselineError, match="missing AQ artefact"):
        ar.load_and_verify_aq_artefacts(namespace="aq_ns")


def test_corrupted_sidecar_fails_closed(tmp_path, monkeypatch) -> None:
    ns = tmp_path / "aq_ns"
    _write_aq_namespace(ns, _synthetic_aq_artefacts())
    p = ns / "dataset_manifest.json"
    p.write_text(p.read_text(encoding="utf-8") + " ", encoding="utf-8")
    monkeypatch.setattr(ar, "REPO_ROOT", tmp_path)
    with pytest.raises(ar.LongHorizonFixedBaselineError, match="!= sidecar"):
        ar.load_and_verify_aq_artefacts(namespace="aq_ns")


def test_contract_hash_drift_fails_closed(tmp_path, monkeypatch) -> None:
    arts = _synthetic_aq_artefacts()
    arts["dataset_manifest.json"]["dataset_contract_hash"] = "0" * 64
    _write_aq_namespace(tmp_path / "aq_ns", arts)
    monkeypatch.setattr(ar, "REPO_ROOT", tmp_path)
    with pytest.raises(ar.LongHorizonFixedBaselineError, match="dataset_contract_hash"):
        ar.load_and_verify_aq_artefacts(namespace="aq_ns")


def test_support_drift_fails_closed(tmp_path, monkeypatch) -> None:
    arts = _synthetic_aq_artefacts()
    arts["dataset_manifest.json"]["per_split_horizon_support"]["holdout"]["5m"][
        "valid_target"
    ] = 999
    _write_aq_namespace(tmp_path / "aq_ns", arts)
    monkeypatch.setattr(ar, "REPO_ROOT", tmp_path)
    with pytest.raises(ar.LongHorizonFixedBaselineError, match="support holdout/5m"):
        ar.load_and_verify_aq_artefacts(namespace="aq_ns")


def test_leakage_flag_regression_fails_closed(tmp_path, monkeypatch) -> None:
    arts = _synthetic_aq_artefacts()
    arts["leakage_split_integrity_proof.json"]["test_rows_loaded"] = 7
    _write_aq_namespace(tmp_path / "aq_ns", arts)
    monkeypatch.setattr(ar, "REPO_ROOT", tmp_path)
    with pytest.raises(ar.LongHorizonFixedBaselineError, match="test_rows_loaded"):
        ar.load_and_verify_aq_artefacts(namespace="aq_ns")


def test_one_run_guard_refuses_overwrite(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(ar, "REPO_ROOT", tmp_path)
    out = tmp_path / ar.OUTPUT_NAMESPACE
    out.mkdir(parents=True)
    (out / "verdict.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(aq, "measure_d_free_gib", lambda *a, **k: 9_999.0)
    with pytest.raises(ar.LongHorizonFixedBaselineError, match="already run"):
        ar.run(progress=False)


# ---------------------------------------------------------------------------
# End-to-end fixture run
# ---------------------------------------------------------------------------


def _write_partition(dir_path, date: str, split: str, n: int, seed: int):
    rng = np.random.default_rng(seed)
    row_index = np.arange(n, dtype=np.int64)
    keys = {
        "row_index": row_index,
        "agg_trade_id": row_index + 1000,
        "feature_timestamp_ms": row_index * 1000,
        "source_transact_time_ms": row_index * 1000,
        "utc_date": pa.array([date] * n),
    }
    feat_cols = dict(keys)
    x0 = rng.standard_normal(n)
    for j, c in enumerate(contract.ALLOWED_FEATURE_COLUMNS):
        feat_cols[c] = (x0 if j == 0 else rng.standard_normal(n)).astype(np.float64)
    ftab = pa.table(feat_cols)
    fpath = dir_path / f"feat_{split}_{date}.parquet"
    pq.write_table(ftab, fpath)

    direction = np.where(x0 > 0.3, 1, np.where(x0 < -0.3, -1, 0)).astype(np.int8)
    lab_cols = dict(keys)
    lab_cols[contract.LABEL_INVALID_PRICE_FLAG] = pa.array([False] * n)
    for h in contract.HORIZONS:
        lab_cols[contract.DIRECTION_COLUMN_BY_HORIZON[h]] = pa.array(direction, type=pa.int8())
        lab_cols[contract.CENSORED_FLAG_COLUMN_BY_HORIZON[h]] = pa.array([False] * n)
    ltab = pa.table(lab_cols)
    lpath = dir_path / f"lab_{split}_{date}.parquet"
    pq.write_table(ltab, lpath)

    return aq.PartitionRef(
        date=date, split=split, feature_parquet=fpath, label_parquet=lpath,
        feature_sha256="f" * 64, label_sha256="a" * 64, row_count=n,
    ), direction


def test_end_to_end_fixture_run_writes_verdict_and_no_row_level(tmp_path, monkeypatch) -> None:
    data_dir = tmp_path / "src_data"
    data_dir.mkdir()
    refs = []
    train_dirs = []
    plan = [
        ("2024-06-01", "train", 80, 1), ("2024-06-02", "train", 80, 2),
        ("2024-06-03", "embargo", 40, 3),
        ("2024-09-01", "validation", 70, 4), ("2024-10-01", "validation", 70, 5),
        ("2024-11-01", "holdout", 60, 6),
    ]
    for date, split, n, seed in plan:
        ref, direction = _write_partition(data_dir, date, split, n, seed)
        refs.append(ref)
        if split == "train":
            train_dirs.append(direction)

    # Train class counts per horizon (all horizons identical in the fixture).
    train_dir_all = np.concatenate(train_dirs)
    train_counts = {int(c): int((train_dir_all == c).sum()) for c in (-1, 0, 1)}
    n_train = int(train_dir_all.size)

    # Synthetic AQ artefacts whose train support/class counts match the fixture.
    arts = _synthetic_aq_artefacts()
    for h in contract.HORIZONS:
        arts["dataset_manifest.json"]["per_split_horizon_support"]["train"][h] = {
            "valid_target": n_train,
            "class_-1": train_counts[-1], "class_0": train_counts[0], "class_1": train_counts[1],
        }
    art = ar.AqArtefacts(
        manifest=arts["dataset_manifest.json"],
        split_index=arts["split_index.json"],
        transform=arts["train_only_transform.json"],
        proof=arts["leakage_split_integrity_proof.json"],
        source_binding=arts["source_binding.json"],
        sidecar_inventory=arts["sidecar_inventory.json"],
        build_run_record=arts["build_run_record.json"],
        sha256={n: "0" * 64 for n in ar._AQ_ARTEFACTS},
    )

    monkeypatch.setattr(ar, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(ar, "EXPECTED_PARTITION_COUNT", len(refs))
    monkeypatch.setattr(ar, "EXPECTED_SUPPORT",
                        {**ar.EXPECTED_SUPPORT, "train": {h: n_train for h in contract.HORIZONS}})
    monkeypatch.setattr(ar, "load_and_verify_aq_artefacts", lambda *a, **k: art)
    monkeypatch.setattr(aq, "measure_d_free_gib", lambda *a, **k: 9_999.0)
    monkeypatch.setattr(aq, "assert_budget_during", lambda *a, **k: 9_999.0)
    monkeypatch.setattr(
        aq, "verify_feature_source_binding",
        lambda: ("n" * 64, "f" * 64, "c" * 64, "g" * 64, "h" * 64, {"m": 1}),
    )
    monkeypatch.setattr(
        aq, "verify_label_source_binding",
        lambda feat_sha: ({"m": 1}, ar.EXPECTED_AN_LABEL_MANIFEST_SHA256),
    )
    monkeypatch.setattr(aq, "bind_split_authority", lambda: "deadbeef")
    monkeypatch.setattr(aq, "verify_per_parquet_sidecars_and_inventory",
                        lambda fm, lm, progress=False: refs)
    monkeypatch.setattr(aq, "dataset_contract_hash", lambda: ar.EXPECTED_DATASET_CONTRACT_HASH)

    summary = ar.run(progress=False)

    # Verdict is one of the three frozen Phase 4bn-AP outcomes.
    assert summary["verdict"] in (
        ar.verdict_mod.VERDICT_CONTINUE,
        ar.verdict_mod.VERDICT_INVESTIGATE,
        ar.verdict_mod.VERDICT_STOP,
    )
    out_dir = tmp_path / ar.OUTPUT_NAMESPACE
    # Exactly the compact artefact set + sidecars was written.
    written = {p.name for p in out_dir.iterdir()}
    for name in (
        "run_manifest.json", "frozen_config.json", "source_binding.json",
        "model_parameters.json", "aggregate_metrics.json", "per_date_metrics.json",
        "per_month_metrics.json", "calibration_summary.json",
        "confidence_tail_summary.json", "verdict.json", "run_record.json",
        "sidecar_inventory.json",
    ):
        assert name in written, name
        assert f"{name}.sha256" in written, f"{name}.sha256"

    # No row-level prediction artefact of any kind.
    assert not any("prediction" in n.lower() for n in written)
    assert not any(n.endswith(".parquet") or n.endswith(".npy") for n in written)

    verdict = json.loads((out_dir / "verdict.json").read_text(encoding="utf-8"))
    assert verdict["primary_horizon"] == "5m"
    assert verdict["successor_authorized"] is False

    run_record = json.loads((out_dir / "run_record.json").read_text(encoding="utf-8"))
    for flag in (
        "ml_authorized", "diagnostics_authorized", "strategy_authorized",
        "signals_authorized", "pnl_authorized", "backtest_authorized",
        "live_authorized", "exchange_write_authorized",
        "flip_research_eligible_invoked", "authorized_successor_phase",
        "persisted_row_level_predictions", "second_full_run",
    ):
        assert run_record[flag] is False, flag

    # Model parameters recorded per horizon with the frozen class ordering.
    mp = json.loads((out_dir / "model_parameters.json").read_text(encoding="utf-8"))
    for h in contract.HORIZONS:
        assert mp[h]["class_ordering"] == [-1, 0, 1]
        assert mp[h]["numerical_guard_all_finite"] is True
        assert mp[h]["train_rows_consumed"] == n_train

    # One-run guard now trips on a second attempt.
    with pytest.raises(ar.LongHorizonFixedBaselineError, match="already run"):
        ar.run(progress=False)
