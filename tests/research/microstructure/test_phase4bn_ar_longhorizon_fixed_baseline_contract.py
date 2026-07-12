"""Phase 4bn-AR — contract / binding tests for the fixed long-horizon baseline run.

Pure-logic tests: exact AQ dataset identity, contract hash, feature count / list
hash, AN label family / config hash, target hierarchy, baseline families, frozen
persistence definition + L2 constants, class ordering, transform binding, feature /
label disjointness, and the gitignored output namespace. No Parquet is read; no
model is trained on real data.
"""

from __future__ import annotations

from prometheus.research.microstructure import longhorizon_baseline_verdict_v001 as verdict
from prometheus.research.microstructure import longhorizon_fixed_baseline_run_v001 as ar
from prometheus.research.microstructure import longhorizon_ml_dataset_contract_v001 as contract
from prometheus.research.microstructure import ml_baseline_design_v002 as design
from prometheus.research.microstructure import pre_v002_ml_dataset_contract as ae


def test_dataset_identity_and_contract_hash_bound() -> None:
    assert contract.DATASET_FAMILY == "microstructure_ml_dataset_longhorizon_pre_v001"
    assert contract.CONTRACT_NAME == (
        "microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001"
    )
    assert ar.EXPECTED_DATASET_CONTRACT_HASH == (
        "a310eabf7854ae13ffed1baa2d57a8cf557a3d90dec24337a61e4ca26a9c3873"
    )


def test_feature_count_and_list_hash_bound() -> None:
    assert len(contract.ALLOWED_FEATURE_COLUMNS) == 45
    assert ar.EXPECTED_FEATURE_LIST_HASH == (
        "8e705ba8800421ae0ccc55cdbf115a36dce9f27f8682e552e2b59c4ab83df7b9"
    )
    from prometheus.research.microstructure import build_longhorizon_ml_dataset_v001 as aq

    assert aq.feature_list_hash() == ar.EXPECTED_FEATURE_LIST_HASH


def test_label_family_and_config_hash_bound() -> None:
    assert contract.LABEL_FAMILY == "microstructure_labels_longhorizon_aggtrades_v001"
    assert contract.LABEL_CONFIG_HASH == (
        "edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118"
    )
    assert ar.EXPECTED_AN_LABEL_MANIFEST_SHA256 == (
        "b1ee9afd8dadc410216516f6fa291aa49a26ba788480eb7d98126fc45919f4c0"
    )


def test_target_hierarchy_5m_primary_30m_1h_secondary() -> None:
    assert ar.PRIMARY_HORIZON == "5m"
    assert contract.PRIMARY_TARGET == "forward_direction_5m"
    assert ar.SECONDARY_HORIZONS == ("30m", "1h")
    assert contract.SECONDARY_TARGETS == (
        "forward_direction_30m",
        "forward_direction_1h",
    )
    assert ar.HORIZONS == ("5m", "30m", "1h")


def test_baseline_families_are_exactly_the_three_preregistered() -> None:
    assert ar.FAMILIES == (
        design.BASELINE_MAJORITY_CLASS,
        design.BASELINE_PERSISTENCE_PAST_RETURN,
        design.BASELINE_LOGISTIC_REGRESSION_L2,
    )
    assert ar.FAMILY_LINEAR == "multinomial_logistic_regression_l2"


def test_persistence_definition_is_60s_past_window() -> None:
    assert ar.PERSISTENCE_FEATURE == "rolling_log_return_past_window_60s"
    # The 60s past-window return is one of the frozen 45 features (no new feature).
    assert ar.PERSISTENCE_FEATURE in contract.ALLOWED_FEATURE_COLUMNS
    # No horizon-matched 5m/30m/1h past-window feature exists / is created.
    for h in ("5m", "30m", "1h"):
        assert f"rolling_log_return_past_window_{h}" not in contract.ALLOWED_FEATURE_COLUMNS


def test_frozen_l2_constants() -> None:
    assert design.SGD_EPOCHS == 1
    assert design.SGD_BATCH_SIZE == 8192
    assert design.SGD_LEARNING_RATE == 0.1
    assert design.SGD_L2_REGULARIZATION_STRENGTH == 1e-4
    assert design.SGD_GRADIENT_CLIP_NORM == 10.0
    assert design.RNG_SEED == 20260528
    trainer = ar.models.build_l2_logistic_regression_trainer(45)
    assert trainer.epochs == 1 and trainer.penalty == "l2"
    assert trainer.batch_size == 8192 and trainer.learning_rate == 0.1
    assert trainer.penalty_strength == 1e-4 and trainer.gradient_clip_norm == 10.0
    assert trainer.rng_seed == 20260528


def test_class_ordering_frozen_signed_three_class() -> None:
    assert design.CLASS_LABELS == (-1, 0, 1)
    assert contract.TARGET_CLASSES == (-1, 0, 1)


def test_transform_binding_matches_contract() -> None:
    assert contract.STANDARDIZATION_RULE == (
        "subtract_train_mean_divide_by_max_train_std_epsilon"
    )
    assert contract.STANDARDIZATION_EPSILON == 1e-8
    assert contract.STANDARDIZE_BOOLEAN_FLAGS is False
    assert contract.IMPUTATION_RULE == "fixed_zero_for_null_numeric"
    assert contract.IMPUTATION_FILL_VALUE == 0.0
    assert contract.TRAIN_ONLY_FIT_SPLIT == "train"


def test_no_target_support_reference_censoring_columns_as_features() -> None:
    label_like = (
        set(contract.LABEL_COLUMNS)
        | set(contract.LABEL_SUPPORT_COLUMNS)
        | set(contract.DIRECTION_TARGET_COLUMNS)
        | set(contract.RETURN_METADATA_COLUMNS)
        | set(contract.CENSORED_FLAG_COLUMN_BY_HORIZON.values())
        | set(contract.REFERENCE_TIMESTAMP_COLUMN_BY_HORIZON.values())
        | {contract.LABEL_INVALID_PRICE_FLAG, contract.LABEL_ANY_CENSORED_FLAG}
    )
    assert set(contract.ALLOWED_FEATURE_COLUMNS).isdisjoint(label_like)
    for c in contract.ALLOWED_FEATURE_COLUMNS:
        for sub in contract.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS:
            assert sub not in c


def test_success_thresholds_are_the_frozen_ae_constants() -> None:
    assert ae.SUCCESS_ACCURACY_UPLIFT_PP == 2.0
    assert ae.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP == 1.0
    assert ae.SUCCESS_MACRO_F1_UPLIFT == 0.03
    assert ae.HIGH_CONFIDENCE_THRESHOLD == 0.8
    assert verdict.SUCCESS_ACCURACY_UPLIFT_PP == 2.0
    assert verdict.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP == 1.0
    assert verdict.SUCCESS_MACRO_F1_UPLIFT == 0.03


def test_output_namespace_is_gitignored_research_path() -> None:
    assert ar.OUTPUT_NAMESPACE == (
        "data/research/microstructure/ml_baselines/longhorizon_pre_v001_fixed_run"
    )
    assert ar.OUTPUT_NAMESPACE.startswith("data/research/")
    # AR must not write into the AQ dataset namespace.
    assert ar.OUTPUT_NAMESPACE != ar.AQ_NAMESPACE


def test_claim_scope_forbidden_fields_present() -> None:
    for forbidden in (
        "tradability", "profitability", "pnl", "backtest_validity",
        "economic_significance",
    ):
        assert forbidden in ae.CLAIM_SCOPE_FORBIDDEN


def test_verdict_identifiers_are_the_ap_hierarchy() -> None:
    assert verdict.VERDICT_CONTINUE == "CONTINUE_ONE_BOUNDED_FOLLOWUP"
    assert verdict.VERDICT_INVESTIGATE == "INVESTIGATE_AMBIGUOUS"
    assert verdict.VERDICT_STOP == "STOP_LONGHORIZON_ML_ARC"
