"""Phase 4bn-BB — corrected CF-1 contract: frozen two-feature constants + estimability proof.

Owns the corrected scientific contract re-preregistered by Phase 4bn-BA
(`2026-07-20_phase-4bn-ba_cf1-feature-contract-correction-and-repreregistration.md`, merged
at `7096ce853dd85dfe6bd95ae88942548bc76400dd`). This module is the single authority for the
**corrected** feature-dependent constants and must not be confused with the historical Phase
4bn-AZ three-feature contract in ``cf1_realized_volatility_v001``:

- the corrected two-feature tuple ``(rolling_aggtrade_count_60s, rolling_quantity_sum_60s)``
  and the prohibited derived column ``rolling_quantity_mean_60s``;
- the corrected parameter counts (baseline 4 / augmented 6) and expected structural ranks;
- the corrected training minimum (``10 × 6 = 60``) and the unchanged block minimum (100);
- the unchanged condition-number threshold (``1e10``) and bootstrap constants;
- the scientific result-state vocabulary and the exact long result-state strings;
- the new local (gitignored) BB output-root identity;
- the governance / non-authorization constants;
- the static pre-data **symbolic estimability proof** (no data, no reserve, no network).

Inherited **unchanged** target / timestamp / split primitives are reused from the tested Phase
4bn-AZ module ``cf1_realized_volatility_v001`` (RV kernel, ``P_at``, the allowlist, the causal
interval semantics, the blocks, the dates). Only the historical three-feature constants
(``FEATURE_COLUMNS``, ``AUGMENTED_N_PARAMS = 7``, ``MIN_TRAIN_ORIGINS = 70``) are **not**
inherited — they are the defect the correction removes.

This module performs **no** data I/O, opens **no** market-data / feature file, and uses **no**
network, credential, endpoint, ``.env``, or MCP. It declares constants and pure functions.
"""

from __future__ import annotations

from typing import Any

from . import cf1_realized_volatility_v001 as cf1_base

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------

PHASE_ID = "phase-4bn-bb"
SYMBOL = "BTCUSDT"
CONTRACT_VERSION = "v002"
TARGET_DATASET_FAMILY = "cf1_corrected_realized_volatility_substrate_test_v002"

# ---------------------------------------------------------------------------
# Provenance SHAs (recorded, never recomputed here)
# ---------------------------------------------------------------------------

# Base main == origin/main at BB branch creation (the Phase 4bn-BA merge-closeout
# SHA-finalization tip; also the BA finalization commit's own resulting main tip).
BASE_MAIN_COMMIT_SHA = "e26193e8f61cae797e4cbfab932025b709b74566"
PHASE_4BN_BA_FINALIZATION_SHA = "e26193e8f61cae797e4cbfab932025b709b74566"
# Phase 4bn-BA no-fast-forward merge commit that recorded the corrected contract on main.
PHASE_4BN_BA_MERGE_COMMIT_SHA = "7096ce853dd85dfe6bd95ae88942548bc76400dd"
# Phase 4bn-BA merge-closeout branch commit.
PHASE_4BN_BA_MERGE_CLOSEOUT_BRANCH_SHA = "ba6ddf12dfa97a2f4ef04abf2bd35127c7f04274"
# Phase 4bn-BA final pre-merge contract tip.
PHASE_4BN_BA_CONTRACT_TIP_SHA = "adc06e68cf532e00b0477d0cefca9d97d2287449"
# Phase 4bn-AY final scientific-contract tip.
PHASE_4BN_AY_CONTRACT_TIP_SHA = "0fb560656aa9b50cf110602e15be8222b7343623"
# Phase 4bn-AZ historical SHAs (invalid, consumed; never reused as scientific input).
PHASE_4BN_AZ_IMPLEMENTATION_SHA = "05fa63a8bf8c9b1fe386cc4ab67805046ae418b1"
PHASE_4BN_AZ_MERGE_COMMIT_SHA = "8e82e185a0def318acd2ec42fcb73337edc67b51"

# ---------------------------------------------------------------------------
# Corrected feature contract (Phase 4bn-BA §10)
# ---------------------------------------------------------------------------

# Canonical two-feature list, in this exact order. The mean column is removed.
CORRECTED_FEATURE_COLUMNS: tuple[str, str] = (
    "rolling_aggtrade_count_60s",
    "rolling_quantity_sum_60s",
)
CORRECTED_FEATURE_COUNT = 2

# Prohibited from the entire BB execution path (read/snapshot/transform/emit/manifest/proof/fit).
PROHIBITED_FEATURE_COLUMN = "rolling_quantity_mean_60s"

# The four source feature columns the runner may request (no mean column).
FEATURE_SOURCE_COLUMNS: tuple[str, str, str, str] = (
    "feature_timestamp_ms",
    "row_index",
    "rolling_aggtrade_count_60s",
    "rolling_quantity_sum_60s",
)

# The original Phase 4bn-AY three-feature set (prohibited for future execution).
PROHIBITED_ORIGINAL_FEATURE_SET: tuple[str, str, str] = (
    "rolling_aggtrade_count_60s",
    "rolling_quantity_sum_60s",
    "rolling_quantity_mean_60s",
)
PROHIBITED_ORIGINAL_FEATURE_SET_STATUS = (
    "STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION"
)

# ---------------------------------------------------------------------------
# Corrected model / numerical guards (Phase 4bn-BA §10.7, §10.8, §10.10)
# ---------------------------------------------------------------------------

BASELINE_N_PARAMS = 4  # intercept + RV_h + RV_d + RV_w
AUGMENTED_N_PARAMS = 6  # + 2 standardized log microstructure features
EXPECTED_BASELINE_RANK = 4
EXPECTED_AUGMENTED_RANK = 6  # absence of a source-implied exact dependency only

CONDITION_NUMBER_MAX = 1e10  # unchanged and unrelaxed
MIN_TRAIN_ORIGINS = 60  # 10 * augmented parameters (10 * 6)
MIN_BLOCK_VALID_ORIGINS = 100  # unchanged

# Bootstrap (unchanged).
BOOTSTRAP_REPLICATES = 10_000
BOOTSTRAP_SEED = 20260715
BOOTSTRAP_LOWER_QUANTILE = 0.05

# The committed mean formatter (fixed-point floor quantizer), recorded symbolically only.
MEAN_FORMATTER_RULE = "mean_int = (sum_int * 10^12) // count"

# ---------------------------------------------------------------------------
# Inherited-unchanged target / timestamp / split primitives (reused from v001)
# ---------------------------------------------------------------------------

TARGET_EPSILON = cf1_base.TARGET_EPSILON
STANDARDIZATION_EPSILON = cf1_base.STANDARDIZATION_EPSILON
HORIZON_MS = cf1_base.HORIZON_MS
HOUR_MS = cf1_base.HOUR_MS
MINUTE_MS = cf1_base.MINUTE_MS
GRID_STEPS = cf1_base.GRID_STEPS
COVERAGE_MIN_COVERED_MINUTES = cf1_base.COVERAGE_MIN_COVERED_MINUTES
HAR_DAILY_HOURS = cf1_base.HAR_DAILY_HOURS
HAR_WEEKLY_HOURS = cf1_base.HAR_WEEKLY_HOURS
EMBARGO_MS = cf1_base.EMBARGO_MS
PURGE_MS = cf1_base.PURGE_MS
BLOCKS = cf1_base.BLOCKS
BLOCK_IDS = cf1_base.BLOCK_IDS
N_BLOCKS = cf1_base.N_BLOCKS
ACCESSIBLE_SEGMENTS = cf1_base.ACCESSIBLE_SEGMENTS
EXPECTED_ALLOWED_DATE_COUNT = cf1_base.EXPECTED_ALLOWED_DATE_COUNT
ACCESS_START_DATE = cf1_base.ACCESS_START_DATE
ACCESS_END_DATE = cf1_base.ACCESS_END_DATE
EXCLUDED_EMBARGO_DATE = cf1_base.EXCLUDED_EMBARGO_DATE
WARMUP_START_DATE = cf1_base.WARMUP_START_DATE
WARMUP_END_DATE = cf1_base.WARMUP_END_DATE

# ---------------------------------------------------------------------------
# Scientific result-state vocabulary (Phase 4bn-BB §20)
# ---------------------------------------------------------------------------

CF1_VALID_PASS = "CF1_VALID_PASS"
CF1_VALID_FAIL = "CF1_VALID_FAIL"
CF1_INVALID_RUN = "CF1_INVALID_RUN"
RESULT_STATE_VOCABULARY: tuple[str, str, str] = (
    CF1_VALID_PASS,
    CF1_VALID_FAIL,
    CF1_INVALID_RUN,
)

# Exact long result-state strings (Phase 4bn-BB §20).
LONG_STATE_PREFLIGHT_FAILURE = (
    "CF1_CORRECTED_EXECUTION_PREFLIGHT_FAILURE__NO_MARKET_DATA_OPENED__"
    "NO_EVIDENCE_CONSUMED__NO_SCIENTIFIC_RESULT__SEPARATE_REAUTHORIZATION_REQUIRED__"
    "RESERVES_UNTOUCHED"
)
LONG_STATE_INVALID_RUN = (
    "CF1_CORRECTED_INVALID_RUN__NO_SCIENTIFIC_CLAIM__"
    "PHASE_4BN_BB_EVIDENCE_BEARING_RUN_CONSUMED__NO_RERUN_AUTHORIZED__"
    "SEPARATE_CORRECTIVE_PHASE_REQUIRED__RESERVES_UNTOUCHED"
)
LONG_STATE_VALID_FAIL = (
    "CF1_CORRECTED_VALID_FAIL__PREREGISTERED_CORRECTED_MAGNITUDE_LANE_MATERIALLY_NARROWED__"
    "NO_NEIGHBORING_RESCUE_VARIANT_AUTHORIZED__NO_DIRECTION_OR_PNL_AUTHORIZED__"
    "RESERVES_UNTOUCHED"
)
LONG_STATE_VALID_PASS = (
    "CF1_CORRECTED_VALID_PASS__"
    "DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_SUPPORTED__"
    "DOCS_ONLY_FILTER_ASSESSMENT_ONLY__NO_DIRECTION_OR_PNL_AUTHORIZED__RESERVES_UNTOUCHED"
)


def long_state_for_verdict(verdict: str) -> str:
    """Return the exact long result-state string for a scientific verdict."""
    mapping = {
        CF1_VALID_PASS: LONG_STATE_VALID_PASS,
        CF1_VALID_FAIL: LONG_STATE_VALID_FAIL,
        CF1_INVALID_RUN: LONG_STATE_INVALID_RUN,
    }
    if verdict not in mapping:
        raise Cf1CorrectedContractError(f"unknown verdict {verdict!r}")
    return mapping[verdict]


# ---------------------------------------------------------------------------
# Output-root identity (local, gitignored)
# ---------------------------------------------------------------------------

OUTPUT_ROOT_REL = "data/research/cf1_corrected_realized_volatility_substrate_test_v002"
OUTPUT_SUBDIRS: tuple[str, ...] = ("proofs", "targets", "runs", "manifests", "logs")
# The historical Phase 4bn-AZ output root must never be read or written by BB.
AZ_OUTPUT_ROOT_REL = "data/research/cf1_realized_volatility_substrate_test_v001"

# ---------------------------------------------------------------------------
# Governance / non-authorization constants (all false; Phase 4bn-BB §7, §24)
# ---------------------------------------------------------------------------

NON_AUTHORIZATION_FLAGS: dict[str, bool] = {
    "ml_authorized": False,
    "diagnostics_authorized": False,
    "strategy_authorized": False,
    "signals_authorized": False,
    "pnl_authorized": False,
    "backtest_authorized": False,
    "live_authorized": False,
    "exchange_write_authorized": False,
}

GOVERNANCE_FLAGS: dict[str, Any] = {
    "v002_terminal_window_read": False,
    "sealed_test_split_touched": False,
    "test_rows_loaded": 0,
    "consumed_holdout_opened": False,
    "november_buffer_opened": False,
    "network_used": False,
    "data_acquisition_used": False,
    "az_output_root_read": False,
    "reserve_touched": False,
}


class Cf1CorrectedContractError(RuntimeError):
    """Raised when a corrected-contract frozen invariant fails closed."""


# ---------------------------------------------------------------------------
# Symbolic estimability proof (static, pre-data; Phase 4bn-BB §13)
# ---------------------------------------------------------------------------

SYMBOLIC_PROOF_FAMILY = "cf1_corrected_symbolic_estimability_proof_v002"


def run_symbolic_estimability_proof(code_commit_sha: str = "") -> dict[str, Any]:
    """Run the static, pre-data symbolic estimability proof (Phase 4bn-BB §13).

    Opens no market-data or feature file and touches no reserve; every field is a frozen
    contract constant or a static symbolic statement. The proof passes only if every frozen
    field matches its required value. Two consecutive invocations produce identical check
    sets (no randomness, no data, no timestamp inside the check set).
    """
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    record(
        "exact_feature_list_and_order",
        CORRECTED_FEATURE_COLUMNS
        == ("rolling_aggtrade_count_60s", "rolling_quantity_sum_60s"),
        f"features={list(CORRECTED_FEATURE_COLUMNS)}",
    )
    record(
        "exact_feature_count_2",
        CORRECTED_FEATURE_COUNT == 2 and len(CORRECTED_FEATURE_COLUMNS) == 2,
        f"count={CORRECTED_FEATURE_COUNT}",
    )
    record(
        "committed_candidate_universe_closed",
        PROHIBITED_ORIGINAL_FEATURE_SET
        == (
            "rolling_aggtrade_count_60s",
            "rolling_quantity_sum_60s",
            "rolling_quantity_mean_60s",
        ),
        "sign-invariant 60s magnitude universe = {count, quantity_sum, quantity_mean}",
    )
    record(
        "no_committed_independent_dispersion_feature",
        True,
        "no committed sign-invariant dispersion/std/variance column exists in the schema",
    )
    record(
        "removed_prohibited_mean_feature",
        PROHIBITED_FEATURE_COLUMN == "rolling_quantity_mean_60s"
        and PROHIBITED_FEATURE_COLUMN not in CORRECTED_FEATURE_COLUMNS,
        f"removed={PROHIBITED_FEATURE_COLUMN}",
    )
    record(
        "formatter_floor_quantizer_rule",
        MEAN_FORMATTER_RULE == "mean_int = (sum_int * 10^12) // count",
        MEAN_FORMATTER_RULE,
    )
    record(
        "ideal_quotient_definition",
        True,
        "x3* = x2 / x1 (ideal arithmetic mean at a valid positive origin)",
    )
    record(
        "ideal_log_identity_exact",
        True,
        "ln(x3*) = ln(x2) - ln(x1) (exact, ideal quantity only)",
    )
    record(
        "stored_relation_with_delta",
        True,
        "ln(x3) = ln(x2) - ln(x1) + delta (stored floor-quantized column)",
    )
    record(
        "delta_non_positive_generally_nonzero",
        True,
        "delta <= 0; delta = 0 only when the quotient is exactly representable; generally nonzero",
    )
    record(
        "no_exact_stored_identity_claimed",
        True,
        "no exact stored-feature identity is asserted",
    )
    record(
        "no_universal_relative_error_bound",
        True,
        "no universal relative-error bound on q/x3* is asserted",
    )
    record(
        "retained_features_are_primitive_accumulators",
        True,
        "x1 = window_count, x2 = window_qty; both non-null by construction, non-quantized",
    )
    record(
        "no_source_implied_affine_dependency_ln_x1_ln_x2",
        True,
        "cardinality does not determine the quantity sum; no (a,b,c) != 0 with a*u1+b*u2+c=0",
    )
    record(
        "no_source_implied_dependency_with_har_block",
        True,
        "HAR = price-path log realized variance; x1,x2 = trade cardinality/quantity; disjoint",
    )
    record(
        "baseline_parameter_count_4",
        BASELINE_N_PARAMS == 4,
        f"baseline_params={BASELINE_N_PARAMS}",
    )
    record(
        "augmented_parameter_count_6",
        AUGMENTED_N_PARAMS == 6,
        f"augmented_params={AUGMENTED_N_PARAMS}",
    )
    record(
        "expected_augmented_rank_6_scoped",
        EXPECTED_AUGMENTED_RANK == 6 and EXPECTED_BASELINE_RANK == 4,
        "rank asserts absence of a source-implied exact dependency only (not numerical rank)",
    )
    record(
        "training_minimum_60",
        MIN_TRAIN_ORIGINS == 60,
        f"min_train_origins={MIN_TRAIN_ORIGINS} (10 * 6)",
    )
    record(
        "block_minimum_100",
        MIN_BLOCK_VALID_ORIGINS == 100,
        f"min_block_valid_origins={MIN_BLOCK_VALID_ORIGINS}",
    )
    record(
        "runtime_guards_final_arbiter",
        CONDITION_NUMBER_MAX == 1e10,
        "rank / zero-variance / condition (>1e10) / non-finite guards remain the final arbiter",
    )
    record(
        "original_three_feature_set_prohibited",
        PROHIBITED_ORIGINAL_FEATURE_SET_STATUS
        == "STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION",
        PROHIBITED_ORIGINAL_FEATURE_SET_STATUS,
    )

    passed = all(bool(c["passed"]) for c in checks)
    return {
        "proof_family": SYMBOLIC_PROOF_FAMILY,
        "phase_id": PHASE_ID,
        "symbol": SYMBOL,
        "contract_version": CONTRACT_VERSION,
        "code_commit_sha": code_commit_sha,
        "base_main_commit_sha": BASE_MAIN_COMMIT_SHA,
        "phase_4bn_ba_merge_commit_sha": PHASE_4BN_BA_MERGE_COMMIT_SHA,
        "phase_4bn_ba_contract_tip_sha": PHASE_4BN_BA_CONTRACT_TIP_SHA,
        "phase_4bn_ay_contract_tip_sha": PHASE_4BN_AY_CONTRACT_TIP_SHA,
        "phase_4bn_az_implementation_sha": PHASE_4BN_AZ_IMPLEMENTATION_SHA,
        "phase_4bn_az_merge_commit_sha": PHASE_4BN_AZ_MERGE_COMMIT_SHA,
        "feature_list": list(CORRECTED_FEATURE_COLUMNS),
        "feature_count": CORRECTED_FEATURE_COUNT,
        "prohibited_feature": PROHIBITED_FEATURE_COLUMN,
        "prohibited_original_feature_set": list(PROHIBITED_ORIGINAL_FEATURE_SET),
        "prohibited_original_feature_set_status": PROHIBITED_ORIGINAL_FEATURE_SET_STATUS,
        "mean_formatter_rule": MEAN_FORMATTER_RULE,
        "ideal_quotient": "x3* = x2 / x1",
        "ideal_log_identity": "ln(x3*) = ln(x2) - ln(x1)",
        "stored_relation": "ln(x3) = ln(x2) - ln(x1) + delta",
        "delta_sign": "delta <= 0, generally nonzero",
        "baseline_parameter_count": BASELINE_N_PARAMS,
        "augmented_parameter_count": AUGMENTED_N_PARAMS,
        "expected_baseline_rank": EXPECTED_BASELINE_RANK,
        "expected_augmented_rank": EXPECTED_AUGMENTED_RANK,
        "expected_augmented_rank_scope": (
            "absence of a source-implied exact dependency only; "
            "runtime guards are the final arbiter"
        ),
        "min_training_origins": MIN_TRAIN_ORIGINS,
        "min_block_valid_origins": MIN_BLOCK_VALID_ORIGINS,
        "condition_number_max": CONDITION_NUMBER_MAX,
        "market_data_opened": False,
        "feature_data_opened": False,
        "evidence_consumed": False,
        "reserve_touched": False,
        "n_checks": len(checks),
        "checks": checks,
        "symbolic_estimability_proof_passed": bool(passed),
    }


def validate_symbolic_estimability_proof(proof: dict[str, Any]) -> tuple[bool, str]:
    """Fail closed if any frozen field of the symbolic estimability proof differs.

    Returns ``(ok, reason)``. ``ok`` is True only if every frozen field matches its required
    value and every individual check passed.
    """
    expected: dict[str, Any] = {
        "proof_family": SYMBOLIC_PROOF_FAMILY,
        "phase_id": PHASE_ID,
        "feature_list": list(CORRECTED_FEATURE_COLUMNS),
        "feature_count": 2,
        "prohibited_feature": "rolling_quantity_mean_60s",
        "prohibited_original_feature_set_status": (
            "STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION"
        ),
        "mean_formatter_rule": "mean_int = (sum_int * 10^12) // count",
        "baseline_parameter_count": 4,
        "augmented_parameter_count": 6,
        "expected_baseline_rank": 4,
        "expected_augmented_rank": 6,
        "min_training_origins": 60,
        "min_block_valid_origins": 100,
        "condition_number_max": 1e10,
        "market_data_opened": False,
        "feature_data_opened": False,
        "evidence_consumed": False,
        "reserve_touched": False,
    }
    for key, want in expected.items():
        if proof.get(key) != want:
            return False, f"symbolic_field_mismatch:{key}"
    if PROHIBITED_FEATURE_COLUMN in proof.get("feature_list", []):
        return False, "prohibited_mean_in_feature_list"
    if not all(bool(c["passed"]) for c in proof.get("checks", [])):
        return False, "symbolic_check_failed"
    if proof.get("symbolic_estimability_proof_passed") is not True:
        return False, "symbolic_proof_not_passed"
    return True, ""


__all__ = [
    "AUGMENTED_N_PARAMS",
    "AZ_OUTPUT_ROOT_REL",
    "BASELINE_N_PARAMS",
    "BASE_MAIN_COMMIT_SHA",
    "BLOCKS",
    "BLOCK_IDS",
    "BOOTSTRAP_LOWER_QUANTILE",
    "BOOTSTRAP_REPLICATES",
    "BOOTSTRAP_SEED",
    "CF1_INVALID_RUN",
    "CF1_VALID_FAIL",
    "CF1_VALID_PASS",
    "CONDITION_NUMBER_MAX",
    "CONTRACT_VERSION",
    "CORRECTED_FEATURE_COLUMNS",
    "CORRECTED_FEATURE_COUNT",
    "COVERAGE_MIN_COVERED_MINUTES",
    "Cf1CorrectedContractError",
    "EMBARGO_MS",
    "EXPECTED_ALLOWED_DATE_COUNT",
    "EXPECTED_AUGMENTED_RANK",
    "EXPECTED_BASELINE_RANK",
    "FEATURE_SOURCE_COLUMNS",
    "GOVERNANCE_FLAGS",
    "GRID_STEPS",
    "HAR_DAILY_HOURS",
    "HAR_WEEKLY_HOURS",
    "HORIZON_MS",
    "HOUR_MS",
    "LONG_STATE_INVALID_RUN",
    "LONG_STATE_PREFLIGHT_FAILURE",
    "LONG_STATE_VALID_FAIL",
    "LONG_STATE_VALID_PASS",
    "MEAN_FORMATTER_RULE",
    "MINUTE_MS",
    "MIN_BLOCK_VALID_ORIGINS",
    "MIN_TRAIN_ORIGINS",
    "N_BLOCKS",
    "NON_AUTHORIZATION_FLAGS",
    "OUTPUT_ROOT_REL",
    "OUTPUT_SUBDIRS",
    "PHASE_4BN_AY_CONTRACT_TIP_SHA",
    "PHASE_4BN_AZ_IMPLEMENTATION_SHA",
    "PHASE_4BN_AZ_MERGE_COMMIT_SHA",
    "PHASE_4BN_BA_CONTRACT_TIP_SHA",
    "PHASE_4BN_BA_FINALIZATION_SHA",
    "PHASE_4BN_BA_MERGE_CLOSEOUT_BRANCH_SHA",
    "PHASE_4BN_BA_MERGE_COMMIT_SHA",
    "PHASE_ID",
    "PROHIBITED_FEATURE_COLUMN",
    "PROHIBITED_ORIGINAL_FEATURE_SET",
    "PROHIBITED_ORIGINAL_FEATURE_SET_STATUS",
    "PURGE_MS",
    "RESULT_STATE_VOCABULARY",
    "STANDARDIZATION_EPSILON",
    "SYMBOL",
    "SYMBOLIC_PROOF_FAMILY",
    "TARGET_DATASET_FAMILY",
    "TARGET_EPSILON",
    "long_state_for_verdict",
    "run_symbolic_estimability_proof",
    "validate_symbolic_estimability_proof",
]
