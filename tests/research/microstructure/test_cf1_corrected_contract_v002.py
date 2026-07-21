"""Phase 4bn-BB — tests for the corrected CF-1 contract constants + symbolic proof.

Covers: the exact two-feature tuple and order; the prohibited mean column absent from the
active contract; parameter counts 4/6; minima 60/100; the condition threshold; the bootstrap
seed / replicates; the exact result-state vocabulary and long strings; the inherited exact
dates and blocks; and the static symbolic estimability proof (pass, determinism, fail-closed
validation). No market data is opened.
"""

from __future__ import annotations

from prometheus.research.microstructure import cf1_corrected_contract_v002 as cc
from prometheus.research.microstructure import cf1_realized_volatility_v001 as cf1


def test_exact_two_feature_tuple_and_order() -> None:
    assert cc.CORRECTED_FEATURE_COLUMNS == (
        "rolling_aggtrade_count_60s",
        "rolling_quantity_sum_60s",
    )
    assert cc.CORRECTED_FEATURE_COUNT == 2
    assert len(cc.CORRECTED_FEATURE_COLUMNS) == 2


def test_prohibited_mean_column_not_in_active_contract() -> None:
    assert cc.PROHIBITED_FEATURE_COLUMN == "rolling_quantity_mean_60s"
    assert cc.PROHIBITED_FEATURE_COLUMN not in cc.CORRECTED_FEATURE_COLUMNS
    assert cc.PROHIBITED_FEATURE_COLUMN not in cc.FEATURE_SOURCE_COLUMNS
    assert cc.FEATURE_SOURCE_COLUMNS == (
        "feature_timestamp_ms",
        "row_index",
        "rolling_aggtrade_count_60s",
        "rolling_quantity_sum_60s",
    )


def test_parameter_counts_4_and_6() -> None:
    assert cc.BASELINE_N_PARAMS == 4
    assert cc.AUGMENTED_N_PARAMS == 6
    assert cc.EXPECTED_BASELINE_RANK == 4
    assert cc.EXPECTED_AUGMENTED_RANK == 6


def test_minima_60_and_100() -> None:
    assert cc.MIN_TRAIN_ORIGINS == 60
    assert cc.MIN_TRAIN_ORIGINS == 10 * cc.AUGMENTED_N_PARAMS
    assert cc.MIN_BLOCK_VALID_ORIGINS == 100


def test_condition_threshold_unchanged() -> None:
    assert cc.CONDITION_NUMBER_MAX == 1e10


def test_bootstrap_constants() -> None:
    assert cc.BOOTSTRAP_REPLICATES == 10_000
    assert cc.BOOTSTRAP_SEED == 20260715
    assert cc.BOOTSTRAP_LOWER_QUANTILE == 0.05


def test_result_state_vocabulary_exact() -> None:
    assert cc.RESULT_STATE_VOCABULARY == (
        "CF1_VALID_PASS",
        "CF1_VALID_FAIL",
        "CF1_INVALID_RUN",
    )
    assert cc.long_state_for_verdict(cc.CF1_VALID_PASS) == cc.LONG_STATE_VALID_PASS
    assert cc.long_state_for_verdict(cc.CF1_VALID_FAIL) == cc.LONG_STATE_VALID_FAIL
    assert cc.long_state_for_verdict(cc.CF1_INVALID_RUN) == cc.LONG_STATE_INVALID_RUN


def test_long_state_strings_carry_required_tokens() -> None:
    assert cc.LONG_STATE_PREFLIGHT_FAILURE.startswith("CF1_CORRECTED_EXECUTION_PREFLIGHT_FAILURE")
    assert "NO_MARKET_DATA_OPENED" in cc.LONG_STATE_PREFLIGHT_FAILURE
    assert "NO_EVIDENCE_CONSUMED" in cc.LONG_STATE_PREFLIGHT_FAILURE
    assert "PHASE_4BN_BB_EVIDENCE_BEARING_RUN_CONSUMED" in cc.LONG_STATE_INVALID_RUN
    assert "NO_RERUN_AUTHORIZED" in cc.LONG_STATE_INVALID_RUN
    assert "MATERIALLY_NARROWED" in cc.LONG_STATE_VALID_FAIL
    assert "DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_SUPPORTED" in (
        cc.LONG_STATE_VALID_PASS
    )
    for s in (
        cc.LONG_STATE_PREFLIGHT_FAILURE,
        cc.LONG_STATE_INVALID_RUN,
        cc.LONG_STATE_VALID_FAIL,
        cc.LONG_STATE_VALID_PASS,
    ):
        assert s.endswith("RESERVES_UNTOUCHED")


def test_inherited_exact_dates_and_blocks() -> None:
    assert cc.EXPECTED_ALLOWED_DATE_COUNT == 244
    assert len(cf1.allowed_utc_dates()) == 244
    assert "2024-10-01" not in cf1.allowed_utc_dates()
    assert cc.BLOCKS == (
        ("B1", "2024-04-01", "2024-04-30"),
        ("B2", "2024-05-01", "2024-05-31"),
        ("B3", "2024-06-01", "2024-06-30"),
        ("B4", "2024-07-01", "2024-07-31"),
        ("B5", "2024-08-01", "2024-08-31"),
        ("B6", "2024-09-01", "2024-09-30"),
        ("B7", "2024-10-02", "2024-10-31"),
    )
    assert cc.N_BLOCKS == 7


def test_output_root_identity_distinct_from_az() -> None:
    assert cc.OUTPUT_ROOT_REL == (
        "data/research/cf1_corrected_realized_volatility_substrate_test_v002"
    )
    assert cc.AZ_OUTPUT_ROOT_REL == "data/research/cf1_realized_volatility_substrate_test_v001"
    assert cc.OUTPUT_ROOT_REL != cc.AZ_OUTPUT_ROOT_REL


def test_lineage_shas_are_frozen() -> None:
    assert cc.BASE_MAIN_COMMIT_SHA == "e26193e8f61cae797e4cbfab932025b709b74566"
    assert cc.PHASE_4BN_BA_MERGE_COMMIT_SHA == "7096ce853dd85dfe6bd95ae88942548bc76400dd"
    assert cc.PHASE_4BN_BA_MERGE_CLOSEOUT_BRANCH_SHA == (
        "ba6ddf12dfa97a2f4ef04abf2bd35127c7f04274"
    )
    assert cc.PHASE_4BN_BA_CONTRACT_TIP_SHA == "adc06e68cf532e00b0477d0cefca9d97d2287449"
    assert cc.PHASE_4BN_AY_CONTRACT_TIP_SHA == "0fb560656aa9b50cf110602e15be8222b7343623"
    assert cc.PHASE_4BN_AZ_IMPLEMENTATION_SHA == "05fa63a8bf8c9b1fe386cc4ab67805046ae418b1"
    assert cc.PHASE_4BN_AZ_MERGE_COMMIT_SHA == "8e82e185a0def318acd2ec42fcb73337edc67b51"


def test_non_authorization_and_governance_flags() -> None:
    assert all(v is False for v in cc.NON_AUTHORIZATION_FLAGS.values())
    assert len(cc.NON_AUTHORIZATION_FLAGS) == 8
    g = cc.GOVERNANCE_FLAGS
    assert g["v002_terminal_window_read"] is False
    assert g["sealed_test_split_touched"] is False
    assert g["test_rows_loaded"] == 0
    assert g["consumed_holdout_opened"] is False
    assert g["november_buffer_opened"] is False
    assert g["az_output_root_read"] is False
    assert g["reserve_touched"] is False


# ---------------------------------------------------------------------------
# Symbolic estimability proof
# ---------------------------------------------------------------------------


def test_symbolic_proof_passes_and_validates() -> None:
    proof = cc.run_symbolic_estimability_proof("0" * 40)
    assert proof["symbolic_estimability_proof_passed"] is True
    assert proof["feature_list"] == ["rolling_aggtrade_count_60s", "rolling_quantity_sum_60s"]
    assert proof["feature_count"] == 2
    assert proof["augmented_parameter_count"] == 6
    assert proof["baseline_parameter_count"] == 4
    assert proof["min_training_origins"] == 60
    assert proof["min_block_valid_origins"] == 100
    assert proof["market_data_opened"] is False
    assert proof["evidence_consumed"] is False
    assert proof["reserve_touched"] is False
    assert proof["mean_formatter_rule"] == "mean_int = (sum_int * 10^12) // count"
    assert cc.PROHIBITED_FEATURE_COLUMN not in proof["feature_list"]
    ok, why = cc.validate_symbolic_estimability_proof(proof)
    assert ok is True
    assert why == ""


def test_symbolic_proof_deterministic_check_set() -> None:
    p1 = cc.run_symbolic_estimability_proof("a" * 40)
    p2 = cc.run_symbolic_estimability_proof("a" * 40)
    assert p1["checks"] == p2["checks"]
    assert p1["n_checks"] == p2["n_checks"]


def test_symbolic_proof_validation_fails_closed_on_tamper() -> None:
    proof = cc.run_symbolic_estimability_proof("b" * 40)
    proof["augmented_parameter_count"] = 7
    ok, why = cc.validate_symbolic_estimability_proof(proof)
    assert ok is False
    assert why == "symbolic_field_mismatch:augmented_parameter_count"


def test_symbolic_proof_validation_fails_on_mean_in_feature_list() -> None:
    proof = cc.run_symbolic_estimability_proof("c" * 40)
    proof["feature_list"] = [
        "rolling_aggtrade_count_60s",
        "rolling_quantity_sum_60s",
        "rolling_quantity_mean_60s",
    ]
    ok, why = cc.validate_symbolic_estimability_proof(proof)
    assert ok is False
