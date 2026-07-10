"""Phase 4bn-AQ — long-horizon ML dataset contract constants (pure, offline).

Inert, declarative contract module for the **long-horizon** pre-v002 ML dataset
build. It binds the already-verified Phase 4bn-AH 45-feature causal aggTrades
source to the Phase 4bn-AN long-horizon label family
(``microstructure_labels_longhorizon_aggtrades_v001``; horizons ``5m/30m/1h``)
under one new dataset contract identity:

``microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001``.

It is a *sibling* of the frozen short-horizon Phase 4bn-AF/AH contract
``microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`` (primary target
``forward_direction_15s``). It reuses that contract's frozen 45-feature
allowlist, forbidden-column scan, alignment keys, split policy, and train-only
transform policy **verbatim by import** so the two datasets cannot drift on the
feature side, while re-pointing the target to the long-horizon direction family:

- primary target: ``forward_direction_5m`` (the sole decision horizon);
- secondary diagnostics: ``forward_direction_30m`` / ``forward_direction_1h``.

This module performs **no I/O**. It reads no manifest, Parquet, sidecar, or gate
report; it writes nothing; it resolves no filesystem path; it creates no
directory. :data:`OUTPUT_NAMESPACE_PATH` is an inert string constant only. It
imports only the standard library and sibling **inert** contract / schema /
split-policy modules, each side-effect-free at import time.

It builds no dataset, trains nothing, scores nothing, produces no prediction,
computes no metric, sets no manifest field, flips no eligibility, and authorizes
no successor.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import pre_v002_ml_dataset_contract as ah_contract
from . import pre_v002_split_policy as split_policy
from .longhorizon_labels_schema_v001 import (
    LONGHORIZON_CONTRACT_NAME as LABEL_CONTRACT_NAME,
)
from .longhorizon_labels_schema_v001 import (
    LONGHORIZON_HORIZON_MS,
    LONGHORIZON_HORIZONS,
    LONGHORIZON_LABEL_DATASET_FAMILY,
    LONGHORIZON_LABEL_NAMES,
    LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES,
    LONGHORIZON_LEAD,
    LONGHORIZON_SECONDARY,
)

# ---------------------------------------------------------------------------
# Dataset / contract identity (new long-horizon family)
# ---------------------------------------------------------------------------

DATASET_FAMILY = "microstructure_ml_dataset_longhorizon_pre_v001"
CONTRACT_NAME = (
    "microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001"
)
CONTRACT_VERSION = "v001"
DATASET_VERSION = "longhorizon_pre_v001"

# The frozen short-horizon sibling this dataset parallels but never mutates.
SIBLING_SHORT_HORIZON_CONTRACT = ah_contract.CONTRACT_NAME  # 15s dataset contract

# The Phase 4bn-AE amendment-001 evaluation pre-registration layer is shared
# (the same mandatory-metric registry, dependence posture, success thresholds,
# and cost lock apply to the long-horizon baseline per Phase 4bn-AP).
CONTRACT_AMENDMENT_ID = ah_contract.CONTRACT_AMENDMENT_ID  # "amendment_001"

# ---------------------------------------------------------------------------
# Source scope (identical admitted pre-v002 segment as AH / AN)
# ---------------------------------------------------------------------------

SYMBOL = ah_contract.SYMBOL          # BTCUSDT
MARKET = ah_contract.MARKET          # binance_usdm_futures
SOURCE_FAMILY = ah_contract.SOURCE_FAMILY  # aggTrades
START_DATE = ah_contract.START_DATE  # 2024-03-01
END_DATE = ah_contract.END_DATE      # 2024-11-30

EXPECTED_PARTITION_COUNT = ah_contract.EXPECTED_FEATURE_PARTITION_COUNT  # 275
EXPECTED_ROW_COUNT = ah_contract.EXPECTED_ROW_COUNT  # 400_001_695

# Out-of-scope windows (recorded so the builder can fail closed; never read).
V002_TERMINAL_START_DATE = ah_contract.V002_TERMINAL_START_DATE
V002_TERMINAL_END_DATE = ah_contract.V002_TERMINAL_END_DATE
SEALED_TEST_START_DATE = ah_contract.SEALED_TEST_START_DATE
SEALED_TEST_END_DATE = ah_contract.SEALED_TEST_END_DATE

# ---------------------------------------------------------------------------
# Feature source binding (Phase 4bn-AH 45-feature source, reused verbatim)
# ---------------------------------------------------------------------------

# Exactly the frozen 45 causal aggTrades feature/quality columns (imported, not
# re-typed, so count and order remain authoritative and cannot drift from AH).
ALLOWED_FEATURE_COLUMNS: tuple[str, ...] = ah_contract.ALLOWED_FEATURE_COLUMNS
FEATURE_COUNT = len(ALLOWED_FEATURE_COLUMNS)

EXCLUDED_LINEAGE_COLUMNS: tuple[str, ...] = ah_contract.EXCLUDED_LINEAGE_COLUMNS
FORBIDDEN_MODEL_MATRIX_SUBSTRINGS: tuple[str, ...] = (
    ah_contract.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS
)
FORBIDDEN_RAW_PRICE_COLUMNS: tuple[str, ...] = (
    ah_contract.FORBIDDEN_RAW_PRICE_COLUMNS
)

# Expected committed feature / normalized source witnesses (same source AH read).
EXPECTED_NORMALIZED_MANIFEST_SHA256 = ah_contract.EXPECTED_NORMALIZED_MANIFEST_SHA256
EXPECTED_FEATURE_MANIFEST_SHA256 = ah_contract.EXPECTED_FEATURE_MANIFEST_SHA256
EXPECTED_FEATURE_CONFIG_HASH = ah_contract.EXPECTED_FEATURE_CONFIG_HASH
EXPECTED_NORMALIZED_GATE_REPORT_SHA256 = (
    ah_contract.EXPECTED_NORMALIZED_GATE_REPORT_SHA256
)
EXPECTED_FEATURE_GATE_REPORT_SHA256 = ah_contract.EXPECTED_FEATURE_GATE_REPORT_SHA256

# Rejected v002-terminal-bound feature identity (fail closed if encountered).
REJECTED_V002_FEATURE_CONFIG_HASH = ah_contract.REJECTED_V002_FEATURE_CONFIG_HASH
REJECTED_V002_FEATURE_CONFIG_HASH_PREFIX = (
    ah_contract.REJECTED_V002_FEATURE_CONFIG_HASH_PREFIX
)

# ---------------------------------------------------------------------------
# Label source binding (Phase 4bn-AN long-horizon label family)
# ---------------------------------------------------------------------------

LABEL_FAMILY = LONGHORIZON_LABEL_DATASET_FAMILY  # microstructure_labels_longhorizon_aggtrades_v001
LABEL_FAMILY_CONTRACT_NAME = LABEL_CONTRACT_NAME
LABEL_CONFIG_HASH = (
    "edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118"
)

# The rejected v002-terminal-bound label identity (short-horizon family; a
# long-horizon dataset must never bind it).
REJECTED_V002_LABEL_CONFIG_HASH = ah_contract.REJECTED_V002_LABEL_CONFIG_HASH
REJECTED_V002_LABEL_CONFIG_HASH_PREFIX = (
    ah_contract.REJECTED_V002_LABEL_CONFIG_HASH_PREFIX
)
# The frozen short-horizon 15s label identity is out of scope for this dataset.
REJECTED_SHORT_HORIZON_LABEL_CONFIG_HASH = ah_contract.EXPECTED_LABEL_CONFIG_HASH

# ---------------------------------------------------------------------------
# Target horizons (5m primary; 30m / 1h secondary diagnostic)
# ---------------------------------------------------------------------------

HORIZONS: tuple[str, ...] = tuple(LONGHORIZON_HORIZONS)          # ("5m", "30m", "1h")
HORIZON_MS: tuple[int, ...] = tuple(LONGHORIZON_HORIZON_MS)      # (300000, 1800000, 3600000)
HORIZON_MS_BY_LABEL: dict[str, int] = dict(zip(HORIZONS, HORIZON_MS, strict=True))

PRIMARY_HORIZON = LONGHORIZON_LEAD                     # "5m"
PRIMARY_TARGET = f"forward_direction_{PRIMARY_HORIZON}"   # forward_direction_5m
PRIMARY_HORIZON_MS = HORIZON_MS_BY_LABEL[PRIMARY_HORIZON]  # 300000

SECONDARY_HORIZONS: tuple[str, ...] = tuple(LONGHORIZON_SECONDARY)  # ("30m", "1h")
SECONDARY_TARGETS: tuple[str, ...] = tuple(
    f"forward_direction_{h}" for h in SECONDARY_HORIZONS
)

TARGET_CLASSES: tuple[int, int, int] = (-1, 0, 1)
ZERO_CLASS_PRESERVED = True

# Per-horizon column families (labels are TARGETS, never model features).
DIRECTION_COLUMN_BY_HORIZON: dict[str, str] = {
    h: f"forward_direction_{h}" for h in HORIZONS
}
LOG_RETURN_COLUMN_BY_HORIZON: dict[str, str] = {
    h: f"forward_log_return_{h}" for h in HORIZONS
}
CENSORED_FLAG_COLUMN_BY_HORIZON: dict[str, str] = {
    h: f"horizon_censored_flag_{h}" for h in HORIZONS
}
REFERENCE_TIMESTAMP_COLUMN_BY_HORIZON: dict[str, str] = {
    h: f"reference_timestamp_ms_{h}" for h in HORIZONS
}

DIRECTION_TARGET_COLUMNS: tuple[str, ...] = tuple(
    DIRECTION_COLUMN_BY_HORIZON[h] for h in HORIZONS
)
RETURN_METADATA_COLUMNS: tuple[str, ...] = tuple(
    LOG_RETURN_COLUMN_BY_HORIZON[h] for h in HORIZONS
)

LABEL_INVALID_PRICE_FLAG = "label_invalid_price_flag"
LABEL_ANY_CENSORED_FLAG = "label_any_censored_flag"

# The full set of label / support column names (targets + support). None of
# these may ever enter the model feature matrix.
LABEL_COLUMNS: tuple[str, ...] = tuple(LONGHORIZON_LABEL_NAMES)
LABEL_SUPPORT_COLUMNS: tuple[str, ...] = tuple(
    LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES
)

# ---------------------------------------------------------------------------
# Strict per-row alignment keys (feature <-> label), reused from AH.
# ---------------------------------------------------------------------------

ALIGNMENT_KEYS: tuple[str, ...] = ah_contract.ALIGNMENT_KEYS
OPTIONAL_ALIGNMENT_KEYS: tuple[str, ...] = ah_contract.OPTIONAL_ALIGNMENT_KEYS

# ---------------------------------------------------------------------------
# Train-only transform rule (shared Phase 4bn-AJ/AP policy; reused from AH).
# ---------------------------------------------------------------------------

STANDARDIZATION_RULE = ah_contract.STANDARDIZATION_RULE
STANDARDIZATION_EPSILON = ah_contract.STANDARDIZATION_EPSILON
IMPUTATION_RULE = ah_contract.IMPUTATION_RULE
IMPUTATION_FILL_VALUE = ah_contract.IMPUTATION_FILL_VALUE
STANDARDIZE_BOOLEAN_FLAGS = ah_contract.STANDARDIZE_BOOLEAN_FLAGS
TRAIN_ONLY_FIT_SPLIT = ah_contract.TRAIN_ONLY_FIT_SPLIT  # "train"

# ---------------------------------------------------------------------------
# Split-policy binding reference (sole split authority is Phase 4bn-AA).
# ---------------------------------------------------------------------------

SPLIT_POLICY_NAME = split_policy.SPLIT_POLICY_NAME
SPLIT_POLICY_MODULE_PATH = ah_contract.SPLIT_POLICY_MODULE_PATH
EXPECTED_SPLIT_DATE_COUNTS: dict[str, int] = {
    "train": 214,
    "embargo_1": 1,
    "validation": 45,
    "embargo_2": 1,
    "holdout": 14,
}

# ---------------------------------------------------------------------------
# Shared evaluation-layer constants (Phase 4bn-AE amendment-001), reused.
# ---------------------------------------------------------------------------

ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY = ah_contract.ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY
DECISION_BLOCK_UNITS: tuple[str, ...] = ah_contract.DECISION_BLOCK_UNITS
DECIMATION_STRIDE: int | None = ah_contract.DECIMATION_STRIDE
DECIMATION_POLICY = ah_contract.DECIMATION_POLICY
METRIC_GRANULARITIES: tuple[str, ...] = ah_contract.METRIC_GRANULARITIES

# Cost lock (descriptive only; never enters a target).
LOCKED_COST_BPS_PER_SIDE = ah_contract.LOCKED_COST_BPS_PER_SIDE
LOCKED_ROUND_TRIP_COST_BPS = ah_contract.LOCKED_ROUND_TRIP_COST_BPS

# Claim scope (unchanged from Phase 4bn-AE).
CLAIM_SCOPE_ALLOWED: tuple[str, ...] = ah_contract.CLAIM_SCOPE_ALLOWED
CLAIM_SCOPE_FORBIDDEN: tuple[str, ...] = ah_contract.CLAIM_SCOPE_FORBIDDEN

# ---------------------------------------------------------------------------
# Output namespace (one new local/gitignored namespace; never AH's).
# ---------------------------------------------------------------------------

OUTPUT_NAMESPACE = (
    "data/research/microstructure/ml_datasets/longhorizon_pre_v001"
)
OUTPUT_NAMESPACE_PATH = OUTPUT_NAMESPACE + "/"

# ---------------------------------------------------------------------------
# Non-authorization flags (all False).
# ---------------------------------------------------------------------------

NON_AUTHORIZATION_FLAGS: dict[str, bool] = dict(
    ah_contract.NON_AUTHORIZATION_FLAGS
)


# ---------------------------------------------------------------------------
# Frozen dataclass snapshots
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LongHorizonDatasetIdentity:
    """Immutable long-horizon dataset / contract identity."""

    dataset_family: str = DATASET_FAMILY
    contract_name: str = CONTRACT_NAME
    contract_version: str = CONTRACT_VERSION
    amendment_id: str = CONTRACT_AMENDMENT_ID
    symbol: str = SYMBOL
    market: str = MARKET
    source_family: str = SOURCE_FAMILY
    sibling_short_horizon_contract: str = SIBLING_SHORT_HORIZON_CONTRACT


@dataclass(frozen=True)
class FeatureSourceBinding:
    """Immutable expected feature/normalized source witnesses (AH source)."""

    normalized_manifest_sha256: str = EXPECTED_NORMALIZED_MANIFEST_SHA256
    feature_manifest_sha256: str = EXPECTED_FEATURE_MANIFEST_SHA256
    feature_config_hash: str = EXPECTED_FEATURE_CONFIG_HASH
    normalized_gate_report_sha256: str = EXPECTED_NORMALIZED_GATE_REPORT_SHA256
    feature_gate_report_sha256: str = EXPECTED_FEATURE_GATE_REPORT_SHA256
    feature_count: int = FEATURE_COUNT


@dataclass(frozen=True)
class LabelSourceBinding:
    """Immutable expected long-horizon label-family witnesses (AN source)."""

    label_family: str = LABEL_FAMILY
    label_family_contract_name: str = LABEL_FAMILY_CONTRACT_NAME
    label_config_hash: str = LABEL_CONFIG_HASH
    horizons: tuple[str, ...] = HORIZONS
    horizon_ms: tuple[int, ...] = HORIZON_MS
    primary_target: str = PRIMARY_TARGET
    secondary_targets: tuple[str, ...] = SECONDARY_TARGETS


@dataclass(frozen=True)
class NonAuthorizationPosture:
    """Immutable non-authorization posture (all flags False)."""

    flags: tuple[tuple[str, bool], ...] = field(
        default_factory=lambda: tuple(NON_AUTHORIZATION_FLAGS.items())
    )
    no_models: bool = True
    no_predictions: bool = True
    no_metrics: bool = True
    no_strategy_boundary: bool = True
    creates_output_namespace: bool = False


# ---------------------------------------------------------------------------
# Pure validators (no I/O)
# ---------------------------------------------------------------------------


class LongHorizonMlDatasetContractError(RuntimeError):
    """Raised when a long-horizon ML dataset contract invariant fails closed."""


def validate_target_horizons(horizons: tuple[str, ...]) -> None:
    """Fail closed unless *horizons* is exactly the long-horizon set 5m/30m/1h."""
    if tuple(horizons) != HORIZONS:
        raise LongHorizonMlDatasetContractError(
            f"target horizons must be {HORIZONS!r}, got {tuple(horizons)!r}"
        )


def validate_feature_scope_disjoint_from_labels() -> None:
    """Fail closed if any allowed feature collides with a label/support column.

    Complements the import-time forbidden-substring guard: proves the 45-feature
    allowlist shares no column name with the long-horizon target / support /
    return / censoring columns.
    """
    label_like = (
        set(LABEL_COLUMNS)
        | set(LABEL_SUPPORT_COLUMNS)
        | {LABEL_INVALID_PRICE_FLAG, LABEL_ANY_CENSORED_FLAG}
    )
    overlap = set(ALLOWED_FEATURE_COLUMNS) & label_like
    if overlap:
        raise LongHorizonMlDatasetContractError(
            f"feature allowlist overlaps label/support columns: {sorted(overlap)!r}"
        )


# ---------------------------------------------------------------------------
# Import-time sanity assertions (constant-only; no I/O)
# ---------------------------------------------------------------------------

assert FEATURE_COUNT == 45
assert len(set(ALLOWED_FEATURE_COLUMNS)) == 45
assert HORIZONS == ("5m", "30m", "1h")
assert HORIZON_MS == (300_000, 1_800_000, 3_600_000)
assert PRIMARY_TARGET == "forward_direction_5m"
assert PRIMARY_HORIZON_MS == 300_000
assert SECONDARY_TARGETS == ("forward_direction_30m", "forward_direction_1h")
assert TARGET_CLASSES == (-1, 0, 1)
assert LABEL_CONFIG_HASH != REJECTED_V002_LABEL_CONFIG_HASH
assert LABEL_CONFIG_HASH != REJECTED_SHORT_HORIZON_LABEL_CONFIG_HASH
assert CONTRACT_NAME != SIBLING_SHORT_HORIZON_CONTRACT
assert DATASET_FAMILY != ah_contract.CONTRACT_NAME
assert EXPECTED_PARTITION_COUNT == 275
assert EXPECTED_ROW_COUNT == 400_001_695
assert OUTPUT_NAMESPACE.startswith("data/research/")
assert ah_contract.OUTPUT_NAMESPACE_PATH.rstrip("/") != OUTPUT_NAMESPACE
assert all(v is False for v in NON_AUTHORIZATION_FLAGS.values())
# No allowed feature column may itself contain a forbidden model-matrix token.
for _c in ALLOWED_FEATURE_COLUMNS:
    for _sub in FORBIDDEN_MODEL_MATRIX_SUBSTRINGS:
        assert _sub not in _c, (_c, _sub)
# The feature allowlist must be disjoint from every long-horizon label column.
validate_feature_scope_disjoint_from_labels()


__all__ = [
    "ALIGNMENT_KEYS",
    "ALLOWED_FEATURE_COLUMNS",
    "CENSORED_FLAG_COLUMN_BY_HORIZON",
    "CLAIM_SCOPE_ALLOWED",
    "CLAIM_SCOPE_FORBIDDEN",
    "CONTRACT_AMENDMENT_ID",
    "CONTRACT_NAME",
    "CONTRACT_VERSION",
    "DATASET_FAMILY",
    "DATASET_VERSION",
    "DECIMATION_POLICY",
    "DECIMATION_STRIDE",
    "DECISION_BLOCK_UNITS",
    "DIRECTION_COLUMN_BY_HORIZON",
    "DIRECTION_TARGET_COLUMNS",
    "END_DATE",
    "EXCLUDED_LINEAGE_COLUMNS",
    "EXPECTED_FEATURE_CONFIG_HASH",
    "EXPECTED_FEATURE_GATE_REPORT_SHA256",
    "EXPECTED_FEATURE_MANIFEST_SHA256",
    "EXPECTED_NORMALIZED_GATE_REPORT_SHA256",
    "EXPECTED_NORMALIZED_MANIFEST_SHA256",
    "EXPECTED_PARTITION_COUNT",
    "EXPECTED_ROW_COUNT",
    "EXPECTED_SPLIT_DATE_COUNTS",
    "FEATURE_COUNT",
    "FORBIDDEN_MODEL_MATRIX_SUBSTRINGS",
    "FORBIDDEN_RAW_PRICE_COLUMNS",
    "FeatureSourceBinding",
    "HORIZONS",
    "HORIZON_MS",
    "HORIZON_MS_BY_LABEL",
    "IMPUTATION_FILL_VALUE",
    "IMPUTATION_RULE",
    "LABEL_ANY_CENSORED_FLAG",
    "LABEL_COLUMNS",
    "LABEL_CONFIG_HASH",
    "LABEL_FAMILY",
    "LABEL_FAMILY_CONTRACT_NAME",
    "LABEL_INVALID_PRICE_FLAG",
    "LABEL_SUPPORT_COLUMNS",
    "LOCKED_COST_BPS_PER_SIDE",
    "LOCKED_ROUND_TRIP_COST_BPS",
    "LOG_RETURN_COLUMN_BY_HORIZON",
    "LongHorizonDatasetIdentity",
    "LongHorizonMlDatasetContractError",
    "LabelSourceBinding",
    "MARKET",
    "METRIC_GRANULARITIES",
    "NON_AUTHORIZATION_FLAGS",
    "NonAuthorizationPosture",
    "OPTIONAL_ALIGNMENT_KEYS",
    "OUTPUT_NAMESPACE",
    "OUTPUT_NAMESPACE_PATH",
    "PRIMARY_HORIZON",
    "PRIMARY_HORIZON_MS",
    "PRIMARY_TARGET",
    "REFERENCE_TIMESTAMP_COLUMN_BY_HORIZON",
    "REJECTED_SHORT_HORIZON_LABEL_CONFIG_HASH",
    "REJECTED_V002_FEATURE_CONFIG_HASH",
    "REJECTED_V002_FEATURE_CONFIG_HASH_PREFIX",
    "REJECTED_V002_LABEL_CONFIG_HASH",
    "REJECTED_V002_LABEL_CONFIG_HASH_PREFIX",
    "RETURN_METADATA_COLUMNS",
    "ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY",
    "SEALED_TEST_END_DATE",
    "SEALED_TEST_START_DATE",
    "SECONDARY_HORIZONS",
    "SECONDARY_TARGETS",
    "SIBLING_SHORT_HORIZON_CONTRACT",
    "SOURCE_FAMILY",
    "SPLIT_POLICY_MODULE_PATH",
    "SPLIT_POLICY_NAME",
    "STANDARDIZATION_EPSILON",
    "STANDARDIZATION_RULE",
    "STANDARDIZE_BOOLEAN_FLAGS",
    "START_DATE",
    "SYMBOL",
    "TARGET_CLASSES",
    "TRAIN_ONLY_FIT_SPLIT",
    "V002_TERMINAL_END_DATE",
    "V002_TERMINAL_START_DATE",
    "ZERO_CLASS_PRESERVED",
    "validate_feature_scope_disjoint_from_labels",
    "validate_target_horizons",
]
