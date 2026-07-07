"""Phase 4bn-AF — pre-v002 ML dataset contract constants (pure, offline).

Inert, declarative contract module for the conservative **pre-v002-only** ML
dataset path. It encodes, as pure constants and frozen dataclasses:

- the Phase 4bn-AC source contract (``microstructure_ml_dataset_aggtrades_pre_v002_contract_v001``):
  source scope, expected manifest / config / gate-report hashes, the 45-column
  causal feature allowlist, the forbidden model-matrix columns, and the primary
  ``forward_direction_15s`` target;
- the Phase 4bn-AE amendment-001 pre-registration layer: the evaluation claim
  scope, the mandatory metric registry, the overlapping-label dependence posture
  (row-level metrics descriptive-only; decision by UTC date / month block;
  decimation reserved-not-adopted), the calibration / cost-realism posture, the
  pre-registered success thresholds, and the strategy / PnL non-authorization
  posture.

This module performs **no I/O**. It reads no manifest, Parquet, sidecar, or gate
report; it writes nothing; it resolves no filesystem path; it creates no
directory. :data:`OUTPUT_NAMESPACE_PATH` is an inert string constant only — it is
never created, resolved, or written. The module imports only the standard library
and sibling **inert** schema-constant modules (``features_schema``,
``features_schema_v002``, ``labels_schema_v002``), each of which is itself
side-effect-free at import time.

It builds no dataset, trains nothing, scores nothing, sets no manifest field,
flips no eligibility, and authorizes no successor.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .features_schema_v002 import FEATURE_NAMES_V002, LINEAGE_COLUMNS_V002
from .labels_schema_v002 import (
    DIRECTION_THRESHOLD_POLICY_V002,
    LABEL_DATASET_FAMILY_V002,
    LABEL_HORIZON_MS_V002,
    LABEL_HORIZONS_V002,
    LABEL_NAMES_V002,
    LABEL_SUPPORT_COLUMN_NAMES_V002,
)

# ---------------------------------------------------------------------------
# Contract identity
# ---------------------------------------------------------------------------

CONTRACT_NAME = "microstructure_ml_dataset_aggtrades_pre_v002_contract_v001"
CONTRACT_AMENDMENT_ID = "amendment_001"

# ---------------------------------------------------------------------------
# Source scope (Phase 4bn-AC §7 / §8)
# ---------------------------------------------------------------------------

SYMBOL = "BTCUSDT"
MARKET = "binance_usdm_futures"
SOURCE_FAMILY = "aggTrades"
START_DATE = "2024-03-01"
END_DATE = "2024-11-30"

EXPECTED_FEATURE_PARTITION_COUNT = 275
EXPECTED_LABEL_PARTITION_COUNT = 275
EXPECTED_NORMALIZED_PARTITION_COUNT = 275
EXPECTED_ROW_COUNT = 400_001_695

# Out-of-scope windows (recorded so the builder can fail closed; never read).
V002_TERMINAL_START_DATE = "2024-12-01"
V002_TERMINAL_END_DATE = "2025-02-28"
SEALED_TEST_START_DATE = "2025-02-14"
SEALED_TEST_END_DATE = "2025-02-28"

# ---------------------------------------------------------------------------
# Target / horizon (Phase 4bn-AC §12; Phase 4bn-AE §9)
# ---------------------------------------------------------------------------

PRIMARY_TARGET = "forward_direction_15s"
PRIMARY_LOG_RETURN = "forward_log_return_15s"
PRIMARY_CENSORED_FLAG = "horizon_censored_flag_15s"
PRIMARY_HORIZON_MS = 15000
TARGET_CLASSES: tuple[int, int, int] = (-1, 0, 1)
ZERO_CLASS_PRESERVED = True
LABEL_INVALID_PRICE_FLAG = "label_invalid_price_flag"

# The direction-threshold policy string is the committed v002 lock (strict sign
# at zero log-return; no deadband; no threshold optimization). Carried by
# reference so the contract records that this target is non-economic.
DIRECTION_THRESHOLD_POLICY = DIRECTION_THRESHOLD_POLICY_V002

# Contract-known horizons (multi-horizon model use deferred by Phase 4bn-AC §12).
CONTRACT_KNOWN_HORIZONS: tuple[str, ...] = tuple(LABEL_HORIZONS_V002)
CONTRACT_KNOWN_HORIZON_MS: tuple[int, ...] = tuple(LABEL_HORIZON_MS_V002)

TARGET_FAMILY = LABEL_DATASET_FAMILY_V002  # microstructure_labels_aggtrades_v001

# ---------------------------------------------------------------------------
# Phase 4bn-AE amendment-001 evaluation-layer constants
# ---------------------------------------------------------------------------

ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY = True
DECISION_BLOCK_UNITS: tuple[str, str] = ("utc_date", "utc_month")
DECIMATION_STRIDE: int | None = None
DECIMATION_POLICY = "reserved_not_adopted"
HIGH_CONFIDENCE_THRESHOLD = 0.8

# Cost lock (§11.6 = 8 bps/side; round-trip 16 bps). Descriptive only.
LOCKED_COST_BPS_PER_SIDE = 8.0
LOCKED_ROUND_TRIP_COST_BPS = 16.0

# Inert output-namespace string. Never created, resolved, or written.
OUTPUT_NAMESPACE_PATH = (
    "data/research/microstructure/ml_datasets/pre_v002_contract_v001/"
)

# ---------------------------------------------------------------------------
# Expected manifest / config / gate-report hashes (Phase 4bn-AC §10)
# ---------------------------------------------------------------------------

EXPECTED_NORMALIZED_MANIFEST_SHA256 = (
    "0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa"
)
EXPECTED_FEATURE_MANIFEST_SHA256 = (
    "4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52"
)
EXPECTED_FEATURE_CONFIG_HASH = (
    "0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c"
)
EXPECTED_LABEL_MANIFEST_SHA256 = (
    "69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161"
)
EXPECTED_LABEL_CONFIG_HASH = (
    "b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970"
)
EXPECTED_NORMALIZED_GATE_REPORT_SHA256 = (
    "3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134"
)
EXPECTED_FEATURE_GATE_REPORT_SHA256 = (
    "db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08"
)
EXPECTED_LABEL_GATE_REPORT_SHA256 = (
    "ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984"
)

# Rejected v002-terminal-bound identity (Phase 4bn-AC §10). Full values from the
# committed ``ml_baseline_design_v002`` design constants, plus prefixes.
REJECTED_V002_FEATURE_CONFIG_HASH = (
    "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
)
REJECTED_V002_LABEL_CONFIG_HASH = (
    "352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560"
)
REJECTED_V002_FEATURE_CONFIG_HASH_PREFIX = "819cfa7a"
REJECTED_V002_LABEL_CONFIG_HASH_PREFIX = "352bad41"

# ---------------------------------------------------------------------------
# Feature allowlist and forbidden columns (Phase 4bn-AC §14 / §15)
# ---------------------------------------------------------------------------

# The exact 45 causal computed FEATURE_SCHEMA_V002 feature/quality columns,
# imported (not re-typed) from the committed schema so the count and order are
# authoritative. 40 windowed + 3 time-context + 2 quality flags = 45.
ALLOWED_FEATURE_COLUMNS: tuple[str, ...] = tuple(FEATURE_NAMES_V002)

# The 17 lineage columns to exclude (imported from the committed v002 schema;
# identical to the design module's EXCLUDED_LINEAGE_COLUMN_NAMES).
EXCLUDED_LINEAGE_COLUMNS: tuple[str, ...] = tuple(LINEAGE_COLUMNS_V002)

# Label / support columns that must never enter the model matrix.
LABEL_COLUMNS: tuple[str, ...] = tuple(LABEL_NAMES_V002)
LABEL_SUPPORT_COLUMNS: tuple[str, ...] = tuple(LABEL_SUPPORT_COLUMN_NAMES_V002)

FORBIDDEN_MODEL_MATRIX_SUBSTRINGS: tuple[str, ...] = (
    "forward_log_return",
    "forward_direction",
    "horizon_censored_flag",
    "label_",
    "split_",
    "censored_",
)

# Raw-price / book / mark-price columns are forbidden as model features unless a
# future contract revision explicitly authorizes them.
FORBIDDEN_RAW_PRICE_COLUMNS: tuple[str, ...] = (
    "price",
    "raw_price",
    "trade_price",
    "last_price",
    "mark_price",
    "index_price",
    "mid_price",
    "bid",
    "ask",
    "bid_price",
    "ask_price",
)

# Strict per-row alignment keys the builder must verify (Phase 4bn-AC §16).
ALIGNMENT_KEYS: tuple[str, ...] = (
    "row_index",
    "agg_trade_id",
    "feature_timestamp_ms",
    "source_transact_time_ms",
)
OPTIONAL_ALIGNMENT_KEYS: tuple[str, ...] = ("symbol", "utc_date")

# ---------------------------------------------------------------------------
# Train-only transform rule (Phase 4bn-AC §18) — inert plan constants
# ---------------------------------------------------------------------------

STANDARDIZATION_RULE = "subtract_train_mean_divide_by_max_train_std_epsilon"
STANDARDIZATION_EPSILON = 1e-8
IMPUTATION_RULE = "fixed_zero_for_null_numeric"
IMPUTATION_FILL_VALUE = 0.0
STANDARDIZE_BOOLEAN_FLAGS = False
TRAIN_ONLY_FIT_SPLIT = "train"

# ---------------------------------------------------------------------------
# Mandatory metric registry (Phase 4bn-AE §13)
# ---------------------------------------------------------------------------

MANDATORY_METRICS: tuple[str, ...] = (
    "majority_accuracy_floor",
    "majority_balanced_accuracy_floor",
    "majority_macro_f1_floor",
    "persistence_baseline",
    "accuracy",
    "balanced_accuracy",
    "macro_f1",
    "per_class_precision_recall_f1",
    "confusion_matrix",
    "predicted_class_distribution",
    "zero_class_prevalence",
    "predicted_zero_rate",
    "log_loss",
    "brier_score",
    "calibration_reliability_table",
    "high_confidence_tail_size",
    "high_confidence_tail_accuracy",
    "train_validation_delta",
    "validation_holdout_delta",
    "filtered_row_date_counts",
    "dropped_rows_by_reason",
)

METRIC_GRANULARITIES: tuple[str, ...] = ("aggregate", "utc_month", "utc_date")

# ---------------------------------------------------------------------------
# Pre-registered success thresholds (Phase 4bn-AE §16)
# ---------------------------------------------------------------------------

SUCCESS_ACCURACY_UPLIFT_PP = 2.0
SUCCESS_BALANCED_ACCURACY_UPLIFT_PP = 1.0
SUCCESS_MACRO_F1_UPLIFT = 0.03

CONTINUE_FOLLOWUP_CATEGORIES: tuple[str, ...] = (
    "longer_horizon_label_memo",
    "bookticker_midprice_data_admissibility_memo",
    "code_only_evaluation_framework_extension",
    "fixed_capacity_model_comparison_memo",
)

# ---------------------------------------------------------------------------
# Claim scope (Phase 4bn-AE §8)
# ---------------------------------------------------------------------------

CLAIM_SCOPE_ALLOWED: tuple[str, ...] = (
    "directional_information_diagnostic",
    "v002_small_lift_sign_reproduction",
    "calibration_confidence_tail_assessment",
)
CLAIM_SCOPE_FORBIDDEN: tuple[str, ...] = (
    "tradability",
    "profitability",
    "strategy_viability",
    "execution_viability",
    "slippage_spread_adequacy",
    "live_readiness",
    "paper_shadow_readiness",
    "pnl",
    "backtest_validity",
    "production_suitability",
    "economic_significance",
)

# ---------------------------------------------------------------------------
# Non-authorization flags (all False) — Phase 4bn-AE §19
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

# ---------------------------------------------------------------------------
# Split-policy binding reference (the sole split authority is Phase 4bn-AA)
# ---------------------------------------------------------------------------

SPLIT_POLICY_NAME = "CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO"
SPLIT_POLICY_MODULE_PATH = (
    "prometheus.research.microstructure.pre_v002_split_policy"
)
EXPECTED_SPLIT_DATE_COUNTS: dict[str, int] = {
    "train": 214,
    "embargo_1": 1,
    "validation": 45,
    "embargo_2": 1,
    "holdout": 14,
}


# ---------------------------------------------------------------------------
# Frozen dataclass snapshots
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ContractIdentity:
    """Immutable contract identity + amendment tag."""

    contract_name: str = CONTRACT_NAME
    amendment_id: str = CONTRACT_AMENDMENT_ID
    symbol: str = SYMBOL
    market: str = MARKET
    source_family: str = SOURCE_FAMILY


@dataclass(frozen=True)
class SourceScope:
    """Immutable pre-v002 source scope."""

    start_date: str = START_DATE
    end_date: str = END_DATE
    expected_feature_partitions: int = EXPECTED_FEATURE_PARTITION_COUNT
    expected_label_partitions: int = EXPECTED_LABEL_PARTITION_COUNT
    expected_normalized_partitions: int = EXPECTED_NORMALIZED_PARTITION_COUNT
    expected_row_count: int = EXPECTED_ROW_COUNT


@dataclass(frozen=True)
class ManifestBinding:
    """Immutable expected manifest / config / gate-report bindings."""

    normalized_manifest_sha256: str = EXPECTED_NORMALIZED_MANIFEST_SHA256
    feature_manifest_sha256: str = EXPECTED_FEATURE_MANIFEST_SHA256
    feature_config_hash: str = EXPECTED_FEATURE_CONFIG_HASH
    label_manifest_sha256: str = EXPECTED_LABEL_MANIFEST_SHA256
    label_config_hash: str = EXPECTED_LABEL_CONFIG_HASH
    normalized_gate_report_sha256: str = EXPECTED_NORMALIZED_GATE_REPORT_SHA256
    feature_gate_report_sha256: str = EXPECTED_FEATURE_GATE_REPORT_SHA256
    label_gate_report_sha256: str = EXPECTED_LABEL_GATE_REPORT_SHA256


@dataclass(frozen=True)
class EvaluationPreregistration:
    """Immutable Phase 4bn-AE evaluation pre-registration snapshot."""

    primary_target: str = PRIMARY_TARGET
    primary_horizon_ms: int = PRIMARY_HORIZON_MS
    row_level_metrics_descriptive_only: bool = ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY
    decision_block_units: tuple[str, ...] = DECISION_BLOCK_UNITS
    decimation_stride: int | None = DECIMATION_STRIDE
    decimation_policy: str = DECIMATION_POLICY
    high_confidence_threshold: float = HIGH_CONFIDENCE_THRESHOLD
    success_accuracy_uplift_pp: float = SUCCESS_ACCURACY_UPLIFT_PP
    success_balanced_accuracy_uplift_pp: float = SUCCESS_BALANCED_ACCURACY_UPLIFT_PP
    success_macro_f1_uplift: float = SUCCESS_MACRO_F1_UPLIFT
    mandatory_metrics: tuple[str, ...] = MANDATORY_METRICS
    metric_granularities: tuple[str, ...] = METRIC_GRANULARITIES
    locked_round_trip_cost_bps: float = LOCKED_ROUND_TRIP_COST_BPS


@dataclass(frozen=True)
class NonAuthorizationPosture:
    """Immutable non-authorization posture (all flags False)."""

    flags: tuple[tuple[str, bool], ...] = field(
        default_factory=lambda: tuple(NON_AUTHORIZATION_FLAGS.items())
    )
    no_strategy_boundary: bool = True
    no_data_io: bool = True
    creates_output_namespace: bool = False


# ---------------------------------------------------------------------------
# Import-time sanity assertions (constant-only; no I/O)
# ---------------------------------------------------------------------------

assert len(ALLOWED_FEATURE_COLUMNS) == 45
assert len(set(ALLOWED_FEATURE_COLUMNS)) == 45
assert len(EXCLUDED_LINEAGE_COLUMNS) == 17
assert PRIMARY_TARGET == "forward_direction_15s"
assert PRIMARY_HORIZON_MS == 15000
assert TARGET_CLASSES == (-1, 0, 1)
assert DECIMATION_STRIDE is None
assert (
    EXPECTED_FEATURE_PARTITION_COUNT
    == EXPECTED_LABEL_PARTITION_COUNT
    == EXPECTED_NORMALIZED_PARTITION_COUNT
    == 275
)
assert EXPECTED_ROW_COUNT == 400_001_695
assert LOCKED_COST_BPS_PER_SIDE == 8.0
assert LOCKED_ROUND_TRIP_COST_BPS == 16.0
assert all(v is False for v in NON_AUTHORIZATION_FLAGS.values())
# No allowed feature column may itself contain a forbidden model-matrix token.
for _c in ALLOWED_FEATURE_COLUMNS:
    for _sub in FORBIDDEN_MODEL_MATRIX_SUBSTRINGS:
        assert _sub not in _c, (_c, _sub)


__all__ = [
    "ALIGNMENT_KEYS",
    "ALLOWED_FEATURE_COLUMNS",
    "CLAIM_SCOPE_ALLOWED",
    "CLAIM_SCOPE_FORBIDDEN",
    "CONTINUE_FOLLOWUP_CATEGORIES",
    "CONTRACT_AMENDMENT_ID",
    "CONTRACT_KNOWN_HORIZONS",
    "CONTRACT_KNOWN_HORIZON_MS",
    "CONTRACT_NAME",
    "ContractIdentity",
    "DECIMATION_POLICY",
    "DECIMATION_STRIDE",
    "DECISION_BLOCK_UNITS",
    "DIRECTION_THRESHOLD_POLICY",
    "END_DATE",
    "EXCLUDED_LINEAGE_COLUMNS",
    "EXPECTED_FEATURE_CONFIG_HASH",
    "EXPECTED_FEATURE_GATE_REPORT_SHA256",
    "EXPECTED_FEATURE_MANIFEST_SHA256",
    "EXPECTED_FEATURE_PARTITION_COUNT",
    "EXPECTED_LABEL_CONFIG_HASH",
    "EXPECTED_LABEL_GATE_REPORT_SHA256",
    "EXPECTED_LABEL_MANIFEST_SHA256",
    "EXPECTED_LABEL_PARTITION_COUNT",
    "EXPECTED_NORMALIZED_GATE_REPORT_SHA256",
    "EXPECTED_NORMALIZED_MANIFEST_SHA256",
    "EXPECTED_NORMALIZED_PARTITION_COUNT",
    "EXPECTED_ROW_COUNT",
    "EXPECTED_SPLIT_DATE_COUNTS",
    "EvaluationPreregistration",
    "FORBIDDEN_MODEL_MATRIX_SUBSTRINGS",
    "FORBIDDEN_RAW_PRICE_COLUMNS",
    "HIGH_CONFIDENCE_THRESHOLD",
    "IMPUTATION_FILL_VALUE",
    "IMPUTATION_RULE",
    "LABEL_COLUMNS",
    "LABEL_INVALID_PRICE_FLAG",
    "LABEL_SUPPORT_COLUMNS",
    "LOCKED_COST_BPS_PER_SIDE",
    "LOCKED_ROUND_TRIP_COST_BPS",
    "MANDATORY_METRICS",
    "MARKET",
    "METRIC_GRANULARITIES",
    "ManifestBinding",
    "NON_AUTHORIZATION_FLAGS",
    "NonAuthorizationPosture",
    "OPTIONAL_ALIGNMENT_KEYS",
    "OUTPUT_NAMESPACE_PATH",
    "PRIMARY_CENSORED_FLAG",
    "PRIMARY_HORIZON_MS",
    "PRIMARY_LOG_RETURN",
    "PRIMARY_TARGET",
    "REJECTED_V002_FEATURE_CONFIG_HASH",
    "REJECTED_V002_FEATURE_CONFIG_HASH_PREFIX",
    "REJECTED_V002_LABEL_CONFIG_HASH",
    "REJECTED_V002_LABEL_CONFIG_HASH_PREFIX",
    "SEALED_TEST_END_DATE",
    "SEALED_TEST_START_DATE",
    "SOURCE_FAMILY",
    "SPLIT_POLICY_MODULE_PATH",
    "SPLIT_POLICY_NAME",
    "STANDARDIZATION_EPSILON",
    "STANDARDIZATION_RULE",
    "STANDARDIZE_BOOLEAN_FLAGS",
    "START_DATE",
    "SUCCESS_ACCURACY_UPLIFT_PP",
    "SUCCESS_BALANCED_ACCURACY_UPLIFT_PP",
    "SUCCESS_MACRO_F1_UPLIFT",
    "SYMBOL",
    "SourceScope",
    "TARGET_CLASSES",
    "TARGET_FAMILY",
    "TRAIN_ONLY_FIT_SPLIT",
    "V002_TERMINAL_END_DATE",
    "V002_TERMINAL_START_DATE",
    "ZERO_CLASS_PRESERVED",
]
