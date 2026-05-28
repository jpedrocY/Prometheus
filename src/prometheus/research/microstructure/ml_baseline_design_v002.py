"""Phase 4bn-B — Multi-day v002 ML-baseline pre-declared design constants.

Pure, inert, offline declarative design module. Encodes the exact, fixed,
a-priori-specified design from Phase 4bn-A §9 – §20 as constants and helper
predicates that the dataset / model / metric / report / runner modules
reuse without copying or re-deriving them.

Phase 4bn-B implements Phase 4bn-A §8: train/validation only; test holdout
sealed; horizons 15s and 60s only; direction classification with the zero
class preserved; the frozen 45-column v002 computed-feature matrix; the 17
lineage columns excluded; train-only transform fitting; fixed a-priori
baselines run once each; descriptive ML metrics plus a §11.6 cost-aware
descriptive summary; canonical Phase 4bb-F sidecars for every local
gitignored output. This module declares nothing about strategy, signals,
PnL, backtests, thresholds, model selection, or feature ranking.

No I/O. No environment access. No network. No credentials. Imports only
the Python standard library and a sibling inert split-policy module.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import diagnostics_split_policy_v002 as policy

# ---------------------------------------------------------------------------
# Phase identity (recorded on every output payload)
# ---------------------------------------------------------------------------

PHASE_ID = "4bn-b"
ML_BASELINE_SCHEMA_VERSION = "v001"

# ---------------------------------------------------------------------------
# Dataset identity (read-only; never mutated by Phase 4bn-B)
# ---------------------------------------------------------------------------

EXPECTED_SYMBOL = "BTCUSDT"
EXPECTED_DATASET_VERSION = "v002"
EXPECTED_FEATURE_FAMILY = "microstructure_features_aggtrades_v001"
EXPECTED_LABEL_FAMILY = "microstructure_labels_aggtrades_v001"
EXPECTED_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)
EXPECTED_LABEL_CONFIG_HASH = (
    "352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560"
)
EXPECTED_TOTAL_ROW_COUNT = 155_153_449
EXPECTED_PARTITION_COUNT = 90
EXPECTED_DATE_START = policy.TRAIN_START_DATE
EXPECTED_DATE_END = policy.TEST_END_DATE

# ---------------------------------------------------------------------------
# Horizons included / deferred (Phase 4bn-A §10)
# ---------------------------------------------------------------------------

INCLUDED_HORIZONS: tuple[str, ...] = ("15s", "60s")
DEFERRED_HORIZONS: tuple[str, ...] = ("1s", "5s")
HORIZON_MS: dict[str, int] = {"15s": 15000, "60s": 60000}

# ---------------------------------------------------------------------------
# Splits used (train/validation only — test sealed)
# ---------------------------------------------------------------------------

TRAINING_SPLIT = policy.TRAIN
EVALUATION_SPLIT = policy.VALIDATION
TEST_HOLDOUT_SPLIT_SEALED = policy.TEST
SUPERVISED_SPLITS: tuple[str, ...] = (TRAINING_SPLIT, EVALUATION_SPLIT)

# ---------------------------------------------------------------------------
# Label/target framing (Phase 4bn-A §9): direction classification, 3-class
# {-1, 0, +1}; zero class preserved; per-horizon-independent. No regression,
# no ordinal, no meta-labeling, no binary collapse.
# ---------------------------------------------------------------------------

CLASS_LABELS: tuple[int, int, int] = (-1, 0, 1)
CLASS_DISPLAY_NAMES: dict[int, str] = {-1: "down", 0: "flat", 1: "up"}
TARGET_FRAMING = "direction_classification_3class_signed"

# ---------------------------------------------------------------------------
# Frozen 45-column computed feature matrix (Phase 4bn-A §13).
# Order is fixed; do not reorder.
# ---------------------------------------------------------------------------

_FEATURE_WINDOWS = ("1s", "5s", "15s", "60s")
_PER_WINDOW_FEATURE_PREFIXES = (
    "rolling_aggtrade_count",
    "rolling_quantity_sum",
    "rolling_quantity_mean",
    "rolling_aggressive_buy_quantity",
    "rolling_aggressive_sell_quantity",
    "rolling_aggressive_buy_count",
    "rolling_aggressive_sell_count",
    "rolling_aggressive_flow_ratio",
    "rolling_aggressive_quantity_imbalance",
    "rolling_log_return_past_window",
)
_NON_WINDOWED_FEATURE_NAMES: tuple[str, ...] = (
    "utc_hour",
    "utc_minute",
    "milliseconds_since_day_start",
    "invalid_window_flag",
    "rolling_missing_window_flag",
)


def _build_computed_feature_column_names() -> tuple[str, ...]:
    out: list[str] = []
    for w in _FEATURE_WINDOWS:
        for p in _PER_WINDOW_FEATURE_PREFIXES:
            out.append(f"{p}_{w}")
    out.extend(_NON_WINDOWED_FEATURE_NAMES)
    return tuple(out)


COMPUTED_FEATURE_COLUMN_NAMES: tuple[str, ...] = (
    _build_computed_feature_column_names()
)
assert len(COMPUTED_FEATURE_COLUMN_NAMES) == 45

# Decimal-as-string-encoded computed feature columns from the v002 schema.
# These must be parsed via float64 cast at load time (the Decimal precision
# is far below float64 dynamic range for these dimensionless quantities).
DECIMAL_AS_STRING_FEATURE_COLUMN_NAMES: tuple[str, ...] = tuple(
    f"{p}_{w}"
    for w in _FEATURE_WINDOWS
    for p in (
        "rolling_quantity_sum",
        "rolling_quantity_mean",
        "rolling_aggressive_buy_quantity",
        "rolling_aggressive_sell_quantity",
        "rolling_aggressive_quantity_imbalance",
    )
)

# Boolean-valued computed feature columns (must be cast to {0,1}).
BOOLEAN_FEATURE_COLUMN_NAMES: tuple[str, ...] = (
    "invalid_window_flag",
    "rolling_missing_window_flag",
)

# Native-double / native-int feature columns: the remainder of the 45.
NUMERIC_NATIVE_FEATURE_COLUMN_NAMES: tuple[str, ...] = tuple(
    c
    for c in COMPUTED_FEATURE_COLUMN_NAMES
    if c not in DECIMAL_AS_STRING_FEATURE_COLUMN_NAMES
    and c not in BOOLEAN_FEATURE_COLUMN_NAMES
)

# ---------------------------------------------------------------------------
# 17 lineage columns to *exclude* from the model matrix (Phase 4bn-A §13).
# Excluded because they encode row identity / lineage / split-leak signals.
# ---------------------------------------------------------------------------

EXCLUDED_LINEAGE_COLUMN_NAMES: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "source_dataset_family",
    "source_dataset_version",
    "feature_schema_version",
    "symbol",
    "utc_date",
    "agg_trade_id",
    "row_index",
    "feature_timestamp_ms",
    "source_transact_time_ms",
    "source_normalized_parquet_per_day_sha256",
    "source_normalized_manifest_sha256",
    "source_successor_state_sha256",
    "source_phase_4bm_d_gate_report_sha256",
    "source_phase_4bm_e_outcome",
    "feature_config_hash",
)
assert len(EXCLUDED_LINEAGE_COLUMN_NAMES) == 17

# Columns that must NEVER appear in the feature matrix even if accidentally
# present in a parquet file: lineage, label, support, and split markers.
FORBIDDEN_MODEL_MATRIX_SUBSTRINGS: tuple[str, ...] = (
    "forward_log_return",
    "forward_direction",
    "horizon_censored_flag",
    "label_",
    "split_",
    "censored_",
)

# ---------------------------------------------------------------------------
# Train-only preprocessing rule (Phase 4bn-A §14): fit-once-on-train,
# apply-elsewhere. Fixed a-priori; nothing is fit on validation/test.
# ---------------------------------------------------------------------------

# Imputation rule for null numeric values: fixed constant zero (the two
# explicit flag columns rolling_missing_window_flag / invalid_window_flag
# capture missingness; imputation value need not depend on train statistics,
# so we use a fixed zero, declared up-front, which is train-only by virtue
# of being fit-free). No imputation is performed for the boolean flags
# themselves (they are never null in the v002 schema).
IMPUTATION_RULE = "fixed_zero_for_null_numeric"
IMPUTATION_FILL_VALUE: float = 0.0

# Standardization rule: subtract train-mean and divide by max(train-std,
# epsilon). Fitted on train only; never refit. Boolean flags pass through
# without standardization (they are {0,1}).
STANDARDIZATION_RULE = "subtract_train_mean_divide_by_max_train_std_epsilon"
STANDARDIZATION_EPSILON: float = 1e-8
STANDARDIZE_BOOLEAN_FLAGS: bool = False

# Class encoding policy: preserve {-1, 0, +1} (no binary collapse).
CLASS_ENCODING_POLICY = "preserve_signed_three_class"

# ---------------------------------------------------------------------------
# Fixed-a-priori baseline families (Phase 4bn-A §15): each is run once with
# pre-declared, fixed, documented settings. No search, no result-based
# model-family selection, no ensemble selection.
# ---------------------------------------------------------------------------

# Deterministic RNG seed used wherever stochasticity cannot be avoided.
RNG_SEED: int = 20260528

# Pre-declared softmax-regression SGD hyperparameters (FIXED; not tuned).
# These are deliberately conservative: a single epoch over the train split,
# a small batch size, and a fixed learning rate. Each variant pre-declares
# its penalty exactly; nothing is selected through results.
SGD_BATCH_SIZE: int = 8192
SGD_EPOCHS: int = 1
SGD_LEARNING_RATE: float = 0.1
SGD_L2_REGULARIZATION_STRENGTH: float = 1e-4
SGD_L1_REGULARIZATION_STRENGTH: float = 1e-4
SGD_GRADIENT_CLIP_NORM: float = 10.0

# Baseline family identifiers (string-stable across reports).
BASELINE_MAJORITY_CLASS = "majority_class_prior"
BASELINE_PERSISTENCE_PAST_RETURN = "persistence_past_return_sign"
BASELINE_LOGISTIC_REGRESSION_L2 = "multinomial_logistic_regression_l2"
BASELINE_LINEAR_CLASSIFIER_L1 = "multinomial_linear_classifier_l1"

BASELINE_FAMILIES_INCLUDED: tuple[str, ...] = (
    BASELINE_MAJORITY_CLASS,
    BASELINE_PERSISTENCE_PAST_RETURN,
    BASELINE_LOGISTIC_REGRESSION_L2,
    BASELINE_LINEAR_CLASSIFIER_L1,
)

# Optional shallow tree is explicitly *not* implemented in Phase 4bn-B per
# §15 ("Optionally one shallow tree baseline only if complexity and leakage
# controls are explicitly bounded"). Phase 4bn-B fail-closes on memory
# rather than running an unbounded tree fit over 74M train rows; the
# decision-tree depth-1 cell is left as future-phase scope and is not
# eligible for inclusion here.
BASELINE_SHALLOW_TREE_INCLUDED: bool = False

# Baseline families explicitly forbidden by Phase 4bn-A §15.
FORBIDDEN_BASELINE_FAMILIES: tuple[str, ...] = (
    "deep_learning",
    "neural_network",
    "transformer",
    "gradient_boosting",
    "xgboost",
    "lightgbm",
    "catboost",
    "random_forest",
    "ensemble",
    "stacking",
    "voting_classifier",
    "hyperparameter_search",
    "grid_search",
    "random_search",
    "bayesian_search",
    "cv_search",
)

# ---------------------------------------------------------------------------
# Cost lock (Phase 4bn-A §18): §11.6 = 8 bps per side / 16 bps round trip.
# Used only for descriptive cost-commensurability summaries. Never for
# strategy / PnL / backtest / threshold tuning.
# ---------------------------------------------------------------------------

COST_BPS_PER_SIDE: float = 8.0
COST_BPS_ROUND_TRIP: float = 16.0
COST_ROUND_TRIP_DECIMAL: float = COST_BPS_ROUND_TRIP / 10_000.0

# Descriptive cost-commensurability magnitude thresholds (multiples of the
# locked round-trip cost). Each threshold is a |forward_log_return| level.
COST_COMMENSURABILITY_MULTIPLES: tuple[float, ...] = (0.5, 1.0, 2.0, 5.0)

# ---------------------------------------------------------------------------
# Output namespace (Phase 4bn-A §19): local + gitignored under
# data/research/microstructure/ml-baselines/phase-4bn-b/. Never committed.
# ---------------------------------------------------------------------------

OUTPUT_NAMESPACE_PARTS: tuple[str, ...] = (
    "data",
    "research",
    "microstructure",
    "ml-baselines",
    "phase-4bn-b",
)

# Output file basenames (Phase 4bn-A §19). Each is paired with a canonical
# Phase 4bb-F sidecar in the same directory.
OUTPUT_RUN_MANIFEST_BASENAME = "ml_baseline_run_manifest.json"
OUTPUT_PER_HORIZON_SUMMARY_BASENAME = "per_horizon_model_summary.json"
OUTPUT_METRICS_TABLE_BASENAME = "metrics_train_validation.csv"
OUTPUT_CALIBRATION_TABLE_BASENAME = "calibration_summary.csv"
OUTPUT_CLASS_BALANCE_TABLE_BASENAME = "class_balance_summary.csv"
OUTPUT_FEATURE_SCHEMA_BASENAME = "feature_schema_used.json"
OUTPUT_TRANSFORM_METADATA_BASENAME = "transform_metadata.json"

OUTPUT_BASENAMES: tuple[str, ...] = (
    OUTPUT_RUN_MANIFEST_BASENAME,
    OUTPUT_PER_HORIZON_SUMMARY_BASENAME,
    OUTPUT_METRICS_TABLE_BASENAME,
    OUTPUT_CALIBRATION_TABLE_BASENAME,
    OUTPUT_CLASS_BALANCE_TABLE_BASENAME,
    OUTPUT_FEATURE_SCHEMA_BASENAME,
    OUTPUT_TRANSFORM_METADATA_BASENAME,
)

# Strict non-authorization flags recorded on every payload (Phase 4bn-A
# §21 + §25). All ``False`` / forbidden — written as evidence on disk.
NON_AUTHORIZATION_FLAGS: dict[str, bool] = {
    "ran_strategy": False,
    "generated_signals": False,
    "simulated_pnl": False,
    "ran_backtests": False,
    "ran_walk_forward_optimization": False,
    "tuned_hyperparameters": False,
    "tuned_thresholds": False,
    "selected_models_through_results": False,
    "ranked_features": False,
    "selected_features": False,
    "performed_feature_pruning": False,
    "used_test_holdout_for_training": False,
    "used_test_holdout_for_calibration": False,
    "used_test_holdout_for_evaluation": False,
    "used_test_holdout_for_tuning": False,
    "used_test_holdout_for_design": False,
    "used_test_holdout_for_model_selection": False,
    "fit_transforms_on_validation": False,
    "fit_transforms_on_test": False,
    "mutated_manifest": False,
    "mutated_successor_state_artefact": False,
    "committed_data_microstructure": False,
    "committed_data_research": False,
    "persisted_model_binaries": False,
    "persisted_row_level_predictions": False,
    "created_reusable_split_masks": False,
    "acquired_data": False,
    "called_public_endpoints": False,
    "called_authenticated_endpoints": False,
    "called_private_endpoints": False,
    "opened_websockets": False,
    "opened_user_stream": False,
    "used_credentials": False,
    "read_env_file": False,
    "read_mcp_json": False,
    "used_mcp": False,
    "used_graphify": False,
    "authorized_successor_phase": False,
    "authorized_phase_4bn_c": False,
    "authorized_phase_5": False,
    "authorized_paper_shadow": False,
    "authorized_live_readiness": False,
    "authorized_deployment": False,
    "authorized_exchange_write": False,
}


# ---------------------------------------------------------------------------
# Convenience dataclass snapshots
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BaselineSettingsSnapshot:
    """An inert, serialisable snapshot of the fixed-a-priori baseline settings."""

    rng_seed: int = RNG_SEED
    sgd_batch_size: int = SGD_BATCH_SIZE
    sgd_epochs: int = SGD_EPOCHS
    sgd_learning_rate: float = SGD_LEARNING_RATE
    sgd_l2_strength: float = SGD_L2_REGULARIZATION_STRENGTH
    sgd_l1_strength: float = SGD_L1_REGULARIZATION_STRENGTH
    sgd_gradient_clip_norm: float = SGD_GRADIENT_CLIP_NORM
    imputation_rule: str = IMPUTATION_RULE
    imputation_fill_value: float = IMPUTATION_FILL_VALUE
    standardization_rule: str = STANDARDIZATION_RULE
    standardization_epsilon: float = STANDARDIZATION_EPSILON
    standardize_boolean_flags: bool = STANDARDIZE_BOOLEAN_FLAGS
    class_encoding_policy: str = CLASS_ENCODING_POLICY
    target_framing: str = TARGET_FRAMING

    def as_dict(self) -> dict[str, object]:
        return {
            "rng_seed": self.rng_seed,
            "sgd_batch_size": self.sgd_batch_size,
            "sgd_epochs": self.sgd_epochs,
            "sgd_learning_rate": self.sgd_learning_rate,
            "sgd_l2_strength": self.sgd_l2_strength,
            "sgd_l1_strength": self.sgd_l1_strength,
            "sgd_gradient_clip_norm": self.sgd_gradient_clip_norm,
            "imputation_rule": self.imputation_rule,
            "imputation_fill_value": self.imputation_fill_value,
            "standardization_rule": self.standardization_rule,
            "standardization_epsilon": self.standardization_epsilon,
            "standardize_boolean_flags": self.standardize_boolean_flags,
            "class_encoding_policy": self.class_encoding_policy,
            "target_framing": self.target_framing,
        }


def class_index_of(label: int) -> int:
    """Return the 0-based class index for *label* in :data:`CLASS_LABELS`."""
    if label == -1:
        return 0
    if label == 0:
        return 1
    if label == 1:
        return 2
    raise ValueError(f"unknown class label {label!r}; expected one of {CLASS_LABELS!r}")


def label_of_class_index(idx: int) -> int:
    """Inverse of :func:`class_index_of`."""
    if idx == 0:
        return -1
    if idx == 1:
        return 0
    if idx == 2:
        return 1
    raise ValueError(f"unknown class index {idx!r}; expected 0/1/2")


def included_horizon_ms(horizon: str) -> int:
    """Return the horizon ms for *horizon*, raising on a forbidden horizon."""
    if horizon not in INCLUDED_HORIZONS:
        raise ValueError(
            f"horizon {horizon!r} is not included by Phase 4bn-B "
            f"(included: {INCLUDED_HORIZONS!r}; deferred: {DEFERRED_HORIZONS!r})"
        )
    return HORIZON_MS[horizon]


def assert_no_forbidden_model_matrix_column(name: str) -> None:
    """Raise :class:`ValueError` if *name* is forbidden in the model matrix."""
    if name in EXCLUDED_LINEAGE_COLUMN_NAMES:
        raise ValueError(
            f"lineage column {name!r} must not be in the model matrix"
        )
    for sub in FORBIDDEN_MODEL_MATRIX_SUBSTRINGS:
        if sub in name:
            raise ValueError(
                f"column {name!r} contains forbidden substring {sub!r}"
            )
