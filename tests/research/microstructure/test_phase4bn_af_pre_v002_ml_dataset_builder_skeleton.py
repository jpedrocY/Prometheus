"""Phase 4bn-AF — offline tests for the pre-v002 ML dataset builder skeleton.

Pure, offline, synthetic tests of the three Phase 4bn-AF skeleton modules
(``pre_v002_ml_dataset_contract``, ``pre_v002_ml_dataset_builder``,
``pre_v002_ml_dataset_proof``). No production data, no ``data/microstructure``,
no ``data/research``, no manifests, no Parquet, no sidecars, no network, no RNG,
and no dependence on the local machine timezone. Includes explicit no-data-I/O
and no-output-namespace proofs.
"""

from __future__ import annotations

import builtins
import pathlib
from datetime import UTC, datetime

import pytest

from prometheus.research.microstructure import (
    pre_v002_ml_dataset_builder as builder,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_contract as contract,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_proof as proof,
)
from prometheus.research.microstructure import (
    pre_v002_split_policy as split_policy,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
FUTURE_NAMESPACE = (
    REPO_ROOT / "data" / "research" / "microstructure" / "ml_datasets"
    / "pre_v002_contract_v001"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ms(iso_date: str, *, hms: str = "12:00:00") -> int:
    """Return epoch ms for a UTC ``YYYY-MM-DD`` date at *hms*."""
    dt = datetime.fromisoformat(f"{iso_date}T{hms}").replace(tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def _good_source_scope() -> dict[str, object]:
    return {
        "symbol": "BTCUSDT",
        "market": "binance_usdm_futures",
        "source_family": "aggTrades",
        "start_date": "2024-03-01",
        "end_date": "2024-11-30",
        "feature_partition_count": 275,
        "label_partition_count": 275,
        "normalized_partition_count": 275,
        "row_count": 400_001_695,
    }


def _good_normalized() -> dict[str, object]:
    return {
        "manifest_sha256": contract.EXPECTED_NORMALIZED_MANIFEST_SHA256,
        "gate_report_sha256": contract.EXPECTED_NORMALIZED_GATE_REPORT_SHA256,
        "partition_count": 275,
    }


def _good_feature() -> dict[str, object]:
    return {
        "manifest_sha256": contract.EXPECTED_FEATURE_MANIFEST_SHA256,
        "feature_config_hash": contract.EXPECTED_FEATURE_CONFIG_HASH,
        "gate_report_sha256": contract.EXPECTED_FEATURE_GATE_REPORT_SHA256,
        "partition_count": 275,
    }


def _good_label() -> dict[str, object]:
    return {
        "manifest_sha256": contract.EXPECTED_LABEL_MANIFEST_SHA256,
        "label_config_hash": contract.EXPECTED_LABEL_CONFIG_HASH,
        "gate_report_sha256": contract.EXPECTED_LABEL_GATE_REPORT_SHA256,
        "partition_count": 275,
    }


def _good_eval_schema() -> dict[str, object]:
    return {
        "metrics": list(contract.MANDATORY_METRICS),
        "granularities": list(contract.METRIC_GRANULARITIES),
        "row_level_metrics_descriptive_only": True,
        "dependence_caveat": "rows are not independent; blocks govern decisions",
        "decimation_stride": None,
        "success_thresholds": {
            "accuracy_uplift_pp": 2.0,
            "balanced_accuracy_uplift_pp": 1.0,
            "macro_f1_uplift": 0.03,
        },
        "calibration_schema": {"bins": 10, "high_confidence_threshold": 0.8},
        "cost_descriptive_fields": {"round_trip_bps": 16.0},
        "no_strategy_boundary": True,
    }


def _row(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "row_index": 1,
        "agg_trade_id": 100,
        "feature_timestamp_ms": 1_700_000_000_000,
        "source_transact_time_ms": 1_700_000_000_000,
        "symbol": "BTCUSDT",
        "utc_date": "2024-06-01",
        contract.PRIMARY_TARGET: 1,
        contract.PRIMARY_LOG_RETURN: 0.0001,
        contract.PRIMARY_CENSORED_FLAG: False,
        contract.LABEL_INVALID_PRICE_FLAG: False,
    }
    base.update(overrides)
    return base


def _key(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "row_index": 1,
        "agg_trade_id": 100,
        "feature_timestamp_ms": 1_700_000_000_000,
        "source_transact_time_ms": 1_700_000_000_000,
        "symbol": "BTCUSDT",
        "utc_date": "2024-06-01",
    }
    base.update(overrides)
    return base


def _exercise_full_surface() -> None:
    """Call the complete public skeleton + proof surface with synthetic inputs."""
    builder.validate_source_scope(_good_source_scope())
    builder.validate_manifest_hashes(_good_normalized(), _good_feature(), _good_label())
    builder.validate_feature_allowlist(list(contract.ALLOWED_FEATURE_COLUMNS))
    assert builder.scan_forbidden_columns(list(contract.ALLOWED_FEATURE_COLUMNS)) == ()
    builder.assert_no_forbidden_columns(list(contract.ALLOWED_FEATURE_COLUMNS))
    builder.filter_targets([_row(), _row(**{contract.PRIMARY_TARGET: None})])
    builder.assert_strict_alignment([_key()], [_key()])
    assert builder.assign_split(_ms("2024-06-01")) == split_policy.TRAIN
    assert builder.should_drop_for_split(split_policy.EMBARGO) is True
    builder.validate_no_boundary_crossing(_ms("2024-06-01"), 15000)
    builder.plan_train_only_transform()
    builder.validate_evaluation_schema(_good_eval_schema())
    builder.build_skeleton_plan()
    p = proof.build_dataset_builder_proof()
    proof.validate_dataset_builder_proof(p)


# ---------------------------------------------------------------------------
# 1. Import / no side effects
# ---------------------------------------------------------------------------


def test_imports_do_not_create_future_namespace() -> None:
    assert not FUTURE_NAMESPACE.exists()


def test_modules_expose_all() -> None:
    for mod in (contract, builder, proof):
        assert isinstance(mod.__all__, list)
        assert mod.__all__, f"{mod.__name__} has empty __all__"
        for name in mod.__all__:
            assert hasattr(mod, name), f"{mod.__name__} missing {name}"


# ---------------------------------------------------------------------------
# 2. Contract constants
# ---------------------------------------------------------------------------


def test_contract_identity_constants() -> None:
    assert contract.CONTRACT_NAME == (
        "microstructure_ml_dataset_aggtrades_pre_v002_contract_v001"
    )
    assert contract.CONTRACT_AMENDMENT_ID == "amendment_001"
    assert contract.SYMBOL == "BTCUSDT"
    assert contract.MARKET == "binance_usdm_futures"
    assert contract.SOURCE_FAMILY == "aggTrades"
    assert contract.START_DATE == "2024-03-01"
    assert contract.END_DATE == "2024-11-30"


def test_contract_scope_and_target_constants() -> None:
    assert contract.EXPECTED_FEATURE_PARTITION_COUNT == 275
    assert contract.EXPECTED_LABEL_PARTITION_COUNT == 275
    assert contract.EXPECTED_NORMALIZED_PARTITION_COUNT == 275
    assert contract.EXPECTED_ROW_COUNT == 400_001_695
    assert contract.PRIMARY_TARGET == "forward_direction_15s"
    assert contract.PRIMARY_HORIZON_MS == 15000
    assert contract.TARGET_CLASSES == (-1, 0, 1)
    assert contract.ZERO_CLASS_PRESERVED is True
    assert contract.HIGH_CONFIDENCE_THRESHOLD == 0.8
    assert contract.LOCKED_COST_BPS_PER_SIDE == 8.0
    assert contract.LOCKED_ROUND_TRIP_COST_BPS == 16.0


def test_output_namespace_is_inert_string() -> None:
    assert contract.OUTPUT_NAMESPACE_PATH == (
        "data/research/microstructure/ml_datasets/pre_v002_contract_v001/"
    )
    assert isinstance(contract.OUTPUT_NAMESPACE_PATH, str)


# ---------------------------------------------------------------------------
# 3. Feature allowlist
# ---------------------------------------------------------------------------


def test_feature_allowlist_is_exactly_45() -> None:
    assert len(contract.ALLOWED_FEATURE_COLUMNS) == 45
    assert len(set(contract.ALLOWED_FEATURE_COLUMNS)) == 45


def test_validate_feature_allowlist_accepts_exact_45() -> None:
    out = builder.validate_feature_allowlist(list(contract.ALLOWED_FEATURE_COLUMNS))
    assert out == contract.ALLOWED_FEATURE_COLUMNS
    # Order-independent input still accepted.
    shuffled = list(reversed(contract.ALLOWED_FEATURE_COLUMNS))
    assert builder.validate_feature_allowlist(shuffled) == contract.ALLOWED_FEATURE_COLUMNS


def test_validate_feature_allowlist_rejects_missing() -> None:
    cols = list(contract.ALLOWED_FEATURE_COLUMNS)[:-1]
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_feature_allowlist(cols)


def test_validate_feature_allowlist_rejects_extra() -> None:
    cols = list(contract.ALLOWED_FEATURE_COLUMNS) + ["utc_hour"]  # duplicate-as-extra
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_feature_allowlist(cols)


def test_validate_feature_allowlist_rejects_duplicate() -> None:
    cols = list(contract.ALLOWED_FEATURE_COLUMNS)
    cols[0] = cols[1]  # introduce a duplicate, drop one distinct
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_feature_allowlist(cols)


@pytest.mark.parametrize(
    "bad",
    [
        "forward_direction_15s",
        "forward_log_return_15s",
        "horizon_censored_flag_15s",
        "label_any_censored_flag",
        "split_label",
        "trade_price",
        "mark_price",
    ],
)
def test_validate_feature_allowlist_rejects_forbidden(bad: str) -> None:
    cols = list(contract.ALLOWED_FEATURE_COLUMNS)[:-1] + [bad]
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_feature_allowlist(cols)


def test_scan_forbidden_columns_returns_hits_and_asserts() -> None:
    assert builder.scan_forbidden_columns(list(contract.ALLOWED_FEATURE_COLUMNS)) == ()
    found = builder.scan_forbidden_columns(["utc_hour", "forward_direction_15s"])
    assert found == ("forward_direction_15s",)
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.assert_no_forbidden_columns(["label_any_censored_flag"])


# ---------------------------------------------------------------------------
# 4. Manifest/hash/gate binding
# ---------------------------------------------------------------------------


def test_manifest_hashes_accept_correct() -> None:
    builder.validate_manifest_hashes(_good_normalized(), _good_feature(), _good_label())


@pytest.mark.parametrize(
    "layer,key",
    [
        ("normalized", "manifest_sha256"),
        ("feature", "manifest_sha256"),
        ("feature", "feature_config_hash"),
        ("label", "manifest_sha256"),
        ("label", "label_config_hash"),
        ("normalized", "gate_report_sha256"),
    ],
)
def test_manifest_hashes_reject_wrong(layer: str, key: str) -> None:
    norm, feat, lab = _good_normalized(), _good_feature(), _good_label()
    target = {"normalized": norm, "feature": feat, "label": lab}[layer]
    target[key] = "0" * 64
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_manifest_hashes(norm, feat, lab)


def test_manifest_hashes_reject_v002_feature_prefix() -> None:
    feat = _good_feature()
    feat["feature_config_hash"] = contract.REJECTED_V002_FEATURE_CONFIG_HASH
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_manifest_hashes(_good_normalized(), feat, _good_label())


def test_manifest_hashes_reject_v002_label_prefix() -> None:
    lab = _good_label()
    lab["label_config_hash"] = contract.REJECTED_V002_LABEL_CONFIG_HASH
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_manifest_hashes(_good_normalized(), _good_feature(), lab)


def test_manifest_hashes_reject_wrong_partition_count() -> None:
    feat = _good_feature()
    feat["partition_count"] = 90
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_manifest_hashes(_good_normalized(), feat, _good_label())


# ---------------------------------------------------------------------------
# 5. Source scope
# ---------------------------------------------------------------------------


def test_source_scope_accepts_correct() -> None:
    builder.validate_source_scope(_good_source_scope())


@pytest.mark.parametrize(
    "key,value",
    [
        ("symbol", "ETHUSDT"),
        ("market", "binance_spot"),
        ("source_family", "trades"),
        ("start_date", "2024-12-01"),
        ("end_date", "2025-02-28"),
        ("feature_partition_count", 90),
        ("row_count", 155_153_449),
        ("contains_v002_terminal", True),
        ("contains_sealed_test", True),
        ("full_envelope", True),
        ("private_source", True),
        ("authenticated_source", True),
        ("external_source", True),
    ],
)
def test_source_scope_rejects_bad(key: str, value: object) -> None:
    scope = _good_source_scope()
    scope[key] = value
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_source_scope(scope)


def test_source_scope_rejects_missing_required() -> None:
    scope = _good_source_scope()
    del scope["symbol"]
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_source_scope(scope)


# ---------------------------------------------------------------------------
# 6. Split assignment
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "date,expected",
    [
        ("2024-03-01", split_policy.TRAIN),
        ("2024-09-30", split_policy.TRAIN),
        ("2024-10-01", split_policy.EMBARGO),
        ("2024-10-02", split_policy.VALIDATION),
        ("2024-11-15", split_policy.VALIDATION),
        ("2024-11-16", split_policy.EMBARGO),
        ("2024-11-17", split_policy.HOLDOUT),
        ("2024-11-30", split_policy.HOLDOUT),
    ],
)
def test_assign_split_in_segment(date: str, expected: str) -> None:
    assert builder.assign_split(_ms(date)) == expected


@pytest.mark.parametrize("date", ["2024-12-01", "2025-02-14", "2025-02-28", "2024-02-29"])
def test_assign_split_out_of_segment_raises(date: str) -> None:
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.assign_split(_ms(date))


def test_should_drop_for_split() -> None:
    assert builder.should_drop_for_split(split_policy.EMBARGO) is True
    assert builder.should_drop_for_split(split_policy.TRAIN) is False
    assert builder.should_drop_for_split(split_policy.VALIDATION) is False
    assert builder.should_drop_for_split(split_policy.HOLDOUT) is False
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.should_drop_for_split("unknown")


# ---------------------------------------------------------------------------
# 7. Boundary-crossing / horizon validation
# ---------------------------------------------------------------------------


def test_boundary_crossing_accepts_valid_horizon_non_crossing() -> None:
    builder.validate_no_boundary_crossing(_ms("2024-06-01"), 15000)
    # Holdout is the latest pre-v002 split and never crosses forward.
    builder.validate_no_boundary_crossing(_ms("2024-11-20"), 15000)


def test_boundary_crossing_rejects_invalid_horizon() -> None:
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_no_boundary_crossing(_ms("2024-06-01"), 7000)


def test_boundary_crossing_rejects_embargo_row() -> None:
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_no_boundary_crossing(_ms("2024-10-01"), 15000)


def test_holdout_never_embargoes_itself() -> None:
    assert split_policy.earlier_split_embargo_window_ms(split_policy.HOLDOUT) is None
    assert (
        split_policy.is_earlier_split_boundary_crossing(
            _ms("2024-11-20"), 15000, split_policy.HOLDOUT
        )
        is False
    )


def test_train_row_does_not_cross_due_to_one_day_purge() -> None:
    # The 1-day embargo dominates the 60s horizon: a real in-TRAIN row never
    # crosses the validation boundary. Documented guarantee.
    assert (
        split_policy.is_earlier_split_boundary_crossing(
            _ms("2024-09-30", hms="23:59:59"), 60000, split_policy.TRAIN
        )
        is False
    )


# ---------------------------------------------------------------------------
# 8. Target filtering
# ---------------------------------------------------------------------------


def test_filter_targets_retains_valid_row() -> None:
    res = builder.filter_targets([_row()])
    assert len(res.valid_rows) == 1
    assert res.total_dropped == 0


def test_filter_targets_drops_by_reason() -> None:
    rows = [
        _row(),
        _row(**{contract.PRIMARY_TARGET: None}),
        _row(**{contract.PRIMARY_LOG_RETURN: None}),
        _row(**{contract.PRIMARY_CENSORED_FLAG: True}),
        _row(**{contract.LABEL_INVALID_PRICE_FLAG: True}),
    ]
    res = builder.filter_targets(rows)
    assert len(res.valid_rows) == 1
    assert res.dropped_by_reason == {
        "invalid_price": 1,
        "censored": 1,
        "null_direction": 1,
        "null_log_return": 1,
    }


def test_filter_targets_does_not_impute() -> None:
    row = _row(**{contract.PRIMARY_TARGET: None})
    res = builder.filter_targets([row])
    assert res.valid_rows == ()
    # The original mapping is unchanged (no imputation / mutation).
    assert row[contract.PRIMARY_TARGET] is None


# ---------------------------------------------------------------------------
# 9. Strict alignment
# ---------------------------------------------------------------------------


def test_alignment_accepts_matching() -> None:
    builder.assert_strict_alignment([_key(), _key(row_index=2, agg_trade_id=2)],
                                    [_key(), _key(row_index=2, agg_trade_id=2)])


@pytest.mark.parametrize(
    "field",
    ["row_index", "agg_trade_id", "feature_timestamp_ms", "source_transact_time_ms",
     "symbol", "utc_date"],
)
def test_alignment_rejects_mismatch(field: str) -> None:
    fkey = _key()
    lkey = _key(**{field: "DIFFERENT" if isinstance(_key()[field], str) else 999})
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.assert_strict_alignment([fkey], [lkey])


def test_alignment_rejects_length_mismatch() -> None:
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.assert_strict_alignment([_key()], [_key(), _key()])


def test_alignment_rejects_reorder() -> None:
    a = _key(row_index=1, agg_trade_id=1)
    b = _key(row_index=2, agg_trade_id=2)
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.assert_strict_alignment([a, b], [b, a])


# ---------------------------------------------------------------------------
# 10. Train-only transform planning
# ---------------------------------------------------------------------------


def test_train_only_transform_plan() -> None:
    plan = builder.plan_train_only_transform()
    assert plan.fit_split == split_policy.TRAIN
    assert plan.imputation_rule == "fixed_zero_for_null_numeric"
    assert plan.standardize_boolean_flags is False
    assert split_policy.TRAIN not in plan.applied_splits


@pytest.mark.parametrize("bad_split", ["validation", "holdout", "test", "embargo"])
def test_train_only_transform_rejects_non_train_fit(bad_split: str) -> None:
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.plan_train_only_transform(fit_split=bad_split)


# ---------------------------------------------------------------------------
# 11. Phase 4bn-AE amendment encoding
# ---------------------------------------------------------------------------


def test_evaluation_schema_accepts_complete() -> None:
    builder.validate_evaluation_schema(_good_eval_schema())


def test_metric_registry_complete_and_block_units() -> None:
    for m in (
        "majority_accuracy_floor",
        "persistence_baseline",
        "macro_f1",
        "calibration_reliability_table",
        "high_confidence_tail_accuracy",
        "dropped_rows_by_reason",
    ):
        assert m in contract.MANDATORY_METRICS
    assert contract.DECISION_BLOCK_UNITS == ("utc_date", "utc_month")
    assert contract.DECIMATION_STRIDE is None
    assert contract.DECIMATION_POLICY == "reserved_not_adopted"


def test_success_thresholds_and_claim_scope() -> None:
    assert contract.SUCCESS_ACCURACY_UPLIFT_PP == 2.0
    assert contract.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP == 1.0
    assert contract.SUCCESS_MACRO_F1_UPLIFT == 0.03
    assert "tradability" in contract.CLAIM_SCOPE_FORBIDDEN
    assert "pnl" in contract.CLAIM_SCOPE_FORBIDDEN
    assert "directional_information_diagnostic" in contract.CLAIM_SCOPE_ALLOWED
    assert all(v is False for v in contract.NON_AUTHORIZATION_FLAGS.values())


@pytest.mark.parametrize(
    "mutate",
    [
        lambda s: s.__setitem__("metrics", ["accuracy"]),
        lambda s: s.__setitem__("granularities", ["aggregate"]),
        lambda s: s.__setitem__("row_level_metrics_descriptive_only", False),
        lambda s: s.__setitem__("dependence_caveat", ""),
        lambda s: s.__setitem__("decimation_stride", 10),
        lambda s: s.__setitem__("no_strategy_boundary", False),
        lambda s: s["success_thresholds"].__setitem__("accuracy_uplift_pp", 0.5),
    ],
)
def test_evaluation_schema_rejects_bad(mutate) -> None:  # type: ignore[no-untyped-def]
    schema = _good_eval_schema()
    mutate(schema)
    with pytest.raises(builder.PreV002MlDatasetError):
        builder.validate_evaluation_schema(schema)


# ---------------------------------------------------------------------------
# 12. Proof schema
# ---------------------------------------------------------------------------


def test_proof_builder_returns_all_sections() -> None:
    p = proof.build_dataset_builder_proof()
    assert p.split.train_date_count == 214
    assert p.split.validation_date_count == 45
    assert p.split.holdout_date_count == 14
    assert p.split.v002_terminal_window_read is False
    assert p.split.sealed_test_split_touched is False
    assert p.split.test_rows_loaded == 0
    assert p.split.no_random and p.split.no_shuffle and p.split.no_kfold
    assert p.split.no_bootstrap
    assert p.evaluation.forbidden_column_scan_empty is True
    assert p.budget_preflight.is_placeholder is True
    assert p.budget_preflight.measured_disk is False
    assert p.output_namespace_created is False
    proof.validate_dataset_builder_proof(p)


def test_proof_validator_rejects_true_critical_flag() -> None:
    p = proof.build_dataset_builder_proof()
    bad = proof.DatasetBuilderProof(
        contract_name=p.contract_name,
        amendment_id=p.amendment_id,
        split=proof.SplitProof(test_rows_loaded=1),
        alignment=p.alignment,
        filtering=p.filtering,
        evaluation=p.evaluation,
        budget_preflight=p.budget_preflight,
        non_authorization=p.non_authorization,
    )
    with pytest.raises(builder.PreV002MlDatasetError):
        proof.validate_dataset_builder_proof(bad)


def test_proof_validator_rejects_authorized_flag() -> None:
    p = proof.build_dataset_builder_proof()
    bad = proof.DatasetBuilderProof(
        contract_name=p.contract_name,
        amendment_id=p.amendment_id,
        split=p.split,
        alignment=p.alignment,
        filtering=p.filtering,
        evaluation=p.evaluation,
        budget_preflight=p.budget_preflight,
        non_authorization=proof.NonAuthorizationProof(ml_authorized=True),
    )
    with pytest.raises(builder.PreV002MlDatasetError):
        proof.validate_dataset_builder_proof(bad)


def test_proof_validator_rejects_missing_metrics() -> None:
    p = proof.build_dataset_builder_proof()
    bad = proof.DatasetBuilderProof(
        contract_name=p.contract_name,
        amendment_id=p.amendment_id,
        split=p.split,
        alignment=p.alignment,
        filtering=p.filtering,
        evaluation=proof.EvaluationPreregistrationProof(mandatory_metrics=("accuracy",)),
        budget_preflight=p.budget_preflight,
        non_authorization=p.non_authorization,
    )
    with pytest.raises(builder.PreV002MlDatasetError):
        proof.validate_dataset_builder_proof(bad)


def test_proof_validator_rejects_imputed_targets() -> None:
    p = proof.build_dataset_builder_proof()
    bad = proof.DatasetBuilderProof(
        contract_name=p.contract_name,
        amendment_id=p.amendment_id,
        split=p.split,
        alignment=p.alignment,
        filtering=proof.FilteringProof(targets_imputed=True),
        evaluation=p.evaluation,
        budget_preflight=p.budget_preflight,
        non_authorization=p.non_authorization,
    )
    with pytest.raises(builder.PreV002MlDatasetError):
        proof.validate_dataset_builder_proof(bad)


# ---------------------------------------------------------------------------
# 13. No-data-I/O proof
# ---------------------------------------------------------------------------


def test_public_surface_performs_no_filesystem_io(monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom(*args: object, **kwargs: object) -> object:
        raise AssertionError("filesystem I/O attempted by the skeleton")

    monkeypatch.setattr(builtins, "open", _boom)
    monkeypatch.setattr(pathlib.Path, "mkdir", _boom)
    monkeypatch.setattr(pathlib.Path, "read_text", _boom)
    monkeypatch.setattr(pathlib.Path, "write_text", _boom)
    monkeypatch.setattr(pathlib.Path, "open", _boom)

    pa_pq = pytest.importorskip("pyarrow.parquet")
    monkeypatch.setattr(pa_pq, "read_table", _boom)
    monkeypatch.setattr(pa_pq, "write_table", _boom)

    # The entire public surface runs with the guards armed and must not trip them.
    _exercise_full_surface()


# ---------------------------------------------------------------------------
# 14. No output namespace
# ---------------------------------------------------------------------------


def test_no_output_namespace_created() -> None:
    existed_before = FUTURE_NAMESPACE.exists()
    _exercise_full_surface()
    existed_after = FUTURE_NAMESPACE.exists()
    assert existed_before == existed_after
    # The skeleton must never create it; the phase asserts it does not exist.
    assert not existed_after


# ---------------------------------------------------------------------------
# 15. Skeleton plan / public API stability
# ---------------------------------------------------------------------------


def test_build_skeleton_plan() -> None:
    plan = builder.build_skeleton_plan()
    assert plan.contract_name == contract.CONTRACT_NAME
    assert plan.amendment_id == contract.CONTRACT_AMENDMENT_ID
    assert plan.split_policy_name == split_policy.SPLIT_POLICY_NAME
    assert plan.primary_target == "forward_direction_15s"
    assert plan.feature_count == 45
    assert plan.output_namespace_path == contract.OUTPUT_NAMESPACE_PATH
    assert plan.no_data_io is True
    assert plan.creates_output_namespace is False
    assert all(value is False for _, value in plan.non_authorization_flags)


def test_public_api_names_exported() -> None:
    for name in (
        "validate_source_scope",
        "validate_manifest_hashes",
        "validate_feature_allowlist",
        "scan_forbidden_columns",
        "filter_targets",
        "assert_strict_alignment",
        "assign_split",
        "should_drop_for_split",
        "validate_no_boundary_crossing",
        "plan_train_only_transform",
        "validate_evaluation_schema",
        "build_skeleton_plan",
    ):
        assert name in builder.__all__
    for name in ("build_dataset_builder_proof", "validate_dataset_builder_proof"):
        assert name in proof.__all__
