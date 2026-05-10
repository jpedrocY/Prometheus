"""Phase 4bh aggTrades feature schema constants and config builder.

This module defines the exact, finalised feature schema for the
derived family ``microstructure_features_aggtrades_v001`` per the
Phase 4bh-B contract:

- 4 trailing-window sizes only: 1s, 5s, 15s, 60s;
- 45 feature/quality columns:

  - 40 windowed (4 windows x 10 features per window),
  - 3 time-context (``utc_hour``, ``utc_minute``,
    ``milliseconds_since_day_start``),
  - 2 data-quality (``invalid_window_flag``,
    ``rolling_missing_window_flag``);

- 16 lineage / identity / metadata columns;
- 61-column total schema, in canonical column order.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute features, labels, signals, returns, or any
  execution-quality / order-flow proxy;
- only declares constants and a small, deterministic config builder
  that produces a stable :data:`feature_config_hash`.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Identity / version constants
# ---------------------------------------------------------------------------

FEATURE_DATASET_FAMILY = "microstructure_features_aggtrades_v001"
"""Constant feature family name for Phase 4bh."""

FEATURE_DATASET_VERSION = "v001"
FEATURE_SCHEMA_VERSION = "v001"

SOURCE_NORMALIZED_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
SOURCE_NORMALIZED_DATASET_VERSION = "v001"


# ---------------------------------------------------------------------------
# Window definitions
# ---------------------------------------------------------------------------

FEATURE_WINDOWS_MS_V001: tuple[int, ...] = (1000, 5000, 15000, 60000)
"""Trailing-window sizes in milliseconds, in canonical order."""

FEATURE_WINDOW_LABELS_V001: tuple[str, ...] = ("1s", "5s", "15s", "60s")
"""Human-readable window labels paired 1:1 with :data:`FEATURE_WINDOWS_MS_V001`."""


# ---------------------------------------------------------------------------
# Feature / quality column construction
# ---------------------------------------------------------------------------

PER_WINDOW_FEATURE_TEMPLATES: tuple[str, ...] = (
    "rolling_aggtrade_count_{w}",
    "rolling_quantity_sum_{w}",
    "rolling_quantity_mean_{w}",
    "rolling_aggressive_buy_quantity_{w}",
    "rolling_aggressive_sell_quantity_{w}",
    "rolling_aggressive_buy_count_{w}",
    "rolling_aggressive_sell_count_{w}",
    "rolling_aggressive_flow_ratio_{w}",
    "rolling_aggressive_quantity_imbalance_{w}",
    "rolling_log_return_past_window_{w}",
)
"""The ten per-window feature name templates, in canonical order."""


def _build_feature_names() -> tuple[str, ...]:
    names: list[str] = []
    for label in FEATURE_WINDOW_LABELS_V001:
        for tpl in PER_WINDOW_FEATURE_TEMPLATES:
            names.append(tpl.format(w=label))
    names.extend(
        (
            "utc_hour",
            "utc_minute",
            "milliseconds_since_day_start",
            "invalid_window_flag",
            "rolling_missing_window_flag",
        )
    )
    return tuple(names)


FEATURE_NAMES_V001: tuple[str, ...] = _build_feature_names()
"""All 45 feature / quality columns in canonical order."""


# ---------------------------------------------------------------------------
# Lineage / identity / metadata columns
# ---------------------------------------------------------------------------

LINEAGE_COLUMNS_V001: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "source_dataset_family",
    "source_dataset_version",
    "source_feature_schema_version",
    "symbol",
    "utc_date",
    "agg_trade_id",
    "row_index",
    "feature_timestamp_ms",
    "source_transact_time_ms",
    "source_normalized_parquet_sha256",
    "source_normalized_manifest_sha256",
    "source_successor_state_sha256",
    "source_phase_4bf_gate_report_sha256",
    "feature_config_hash",
)
"""The 16 identity / lineage / metadata columns, in canonical order."""


# ---------------------------------------------------------------------------
# Full schema (lineage + features)
# ---------------------------------------------------------------------------

FEATURE_SCHEMA_V001: tuple[str, ...] = LINEAGE_COLUMNS_V001 + FEATURE_NAMES_V001
"""All 61 columns (lineage + feature/quality) in canonical order."""


# ---------------------------------------------------------------------------
# Forbidden-substring detector
# ---------------------------------------------------------------------------

FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS: tuple[str, ...] = (
    "label",
    "target",
    "future",
    "signal",
    "entry",
    "exit",
    "pnl",
    "profit",
    "loss",
    "mfe",
    "mae",
    "r_multiple",
    "equity",
    "position",
    "alpha",
    "edge",
    "prediction",
    "model",
    "score",
    "decision",
    "strategy",
    "liquidation",
    "funding",
    "open_interest",
    "order_book",
    "mark_price",
)
"""26 forbidden substrings that must NOT appear in any output column name."""


def assert_no_forbidden_substrings(column_names: tuple[str, ...]) -> None:
    """Fail closed if any column name (lowercased) contains a forbidden token."""
    for col in column_names:
        lower = col.lower()
        for token in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS:
            if token in lower:
                raise FeatureSchemaError(
                    f"forbidden substring {token!r} found in column {col!r}"
                )


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class FeatureSchemaError(RuntimeError):
    """Raised when a Phase 4bh schema or config invariant fails closed."""


# ---------------------------------------------------------------------------
# Decimal / null policy descriptor
# ---------------------------------------------------------------------------

DECIMAL_POLICY_V001: Mapping[str, Any] = {
    "raw_price_storage": "decimal_string",
    "raw_quantity_storage": "decimal_string",
    "ratio_storage": "float64_nullable",
    "log_return_storage": "float64_nullable",
    "decimal_module": "stdlib_decimal",
    "decimal_precision_digits": 50,
    "decimal_rounding": "ROUND_HALF_EVEN",
}
"""Deterministic Decimal / float storage policy at v001."""

NULL_POLICY_V001: Mapping[str, Any] = {
    "rolling_quantity_mean": "null_when_empty",
    "rolling_aggressive_flow_ratio": "null_when_zero_denominator",
    "rolling_log_return_past_window": "null_when_no_prior_reference_or_zero_price",
    "no_imputation_across_invalid_windows": True,
    "no_nan_no_inf_for_floats": True,
}
"""Deterministic null policy for nullable feature columns at v001."""

INVALID_WINDOW_POLICY_V001: Mapping[str, Any] = {
    "propagate_from_source_manifest": True,
    "invalid_window_flag_set_when_row_in_invalid_window": True,
    "rolling_missing_window_flag_set_when_any_window_intersects_invalid": True,
    "no_imputation_inside_invalid_windows": True,
}
"""Invalid-window propagation policy at v001."""


_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


# ---------------------------------------------------------------------------
# Feature computation config
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FeatureComputationConfig:
    """Frozen, deterministic config record for one Phase 4bh feature run.

    The :attr:`feature_config_hash` is a SHA256 over the canonical-JSON
    serialization of the key fields (sorted keys, no spaces, ASCII-only)
    so that any change to any field deterministically changes the hash.
    """

    dataset_family: str
    dataset_version: str
    feature_schema_version: str
    source_normalized_parquet_path: str
    source_normalized_manifest_path: str
    source_successor_state_path: str
    output_feature_parquet_path: str
    output_feature_manifest_path: str
    windows_ms: tuple[int, ...]
    feature_names: tuple[str, ...]
    timestamp_alignment: str
    causal_window_rule: str
    same_timestamp_tie_rule: str
    null_policy: Mapping[str, Any] = field(default_factory=lambda: dict(NULL_POLICY_V001))
    invalid_window_policy: Mapping[str, Any] = field(
        default_factory=lambda: dict(INVALID_WINDOW_POLICY_V001)
    )
    decimal_policy: Mapping[str, Any] = field(
        default_factory=lambda: dict(DECIMAL_POLICY_V001)
    )
    code_commit_sha: str = "unknown"
    feature_config_hash: str = ""

    def __post_init__(self) -> None:
        if self.dataset_family != FEATURE_DATASET_FAMILY:
            raise FeatureSchemaError(
                f"dataset_family must be {FEATURE_DATASET_FAMILY!r}"
            )
        if self.dataset_version != FEATURE_DATASET_VERSION:
            raise FeatureSchemaError(
                f"dataset_version must be {FEATURE_DATASET_VERSION!r}"
            )
        if self.feature_schema_version != FEATURE_SCHEMA_VERSION:
            raise FeatureSchemaError(
                f"feature_schema_version must be {FEATURE_SCHEMA_VERSION!r}"
            )
        if tuple(self.windows_ms) != FEATURE_WINDOWS_MS_V001:
            raise FeatureSchemaError(
                f"windows_ms must equal {FEATURE_WINDOWS_MS_V001!r}"
            )
        if tuple(self.feature_names) != FEATURE_NAMES_V001:
            raise FeatureSchemaError(
                "feature_names must equal FEATURE_NAMES_V001 (count and order)"
            )
        if self.timestamp_alignment != "event_aligned":
            raise FeatureSchemaError("timestamp_alignment must be 'event_aligned'")
        if self.causal_window_rule != "trailing_right_open_left":
            raise FeatureSchemaError(
                "causal_window_rule must be 'trailing_right_open_left' "
                "(window is (T - window_ms, T], with same-timestamp tie-break "
                "row_index <= R)"
            )
        if self.same_timestamp_tie_rule != "row_index_le_R":
            raise FeatureSchemaError(
                "same_timestamp_tie_rule must be 'row_index_le_R'"
            )
        if not isinstance(self.code_commit_sha, str) or not (
            _SHA1_RE.match(self.code_commit_sha) or self.code_commit_sha == "unknown"
        ):
            raise FeatureSchemaError(
                "code_commit_sha must be a 40-char lowercase hex SHA "
                "(or the literal 'unknown')"
            )
        if self.feature_config_hash and not _HEX64_RE.match(self.feature_config_hash):
            raise FeatureSchemaError(
                "feature_config_hash must be 64-char lowercase hex when set"
            )

    def to_canonical_dict(self) -> dict[str, Any]:
        """Return a sorted-key dict suitable for canonical-JSON hashing."""
        return {
            "dataset_family": self.dataset_family,
            "dataset_version": self.dataset_version,
            "feature_schema_version": self.feature_schema_version,
            "source_normalized_parquet_path": self.source_normalized_parquet_path,
            "source_normalized_manifest_path": self.source_normalized_manifest_path,
            "source_successor_state_path": self.source_successor_state_path,
            "output_feature_parquet_path": self.output_feature_parquet_path,
            "output_feature_manifest_path": self.output_feature_manifest_path,
            "windows_ms": list(self.windows_ms),
            "feature_names": list(self.feature_names),
            "timestamp_alignment": self.timestamp_alignment,
            "causal_window_rule": self.causal_window_rule,
            "same_timestamp_tie_rule": self.same_timestamp_tie_rule,
            "null_policy": dict(self.null_policy),
            "invalid_window_policy": dict(self.invalid_window_policy),
            "decimal_policy": dict(self.decimal_policy),
            "code_commit_sha": self.code_commit_sha,
        }


def _canonical_json(obj: Mapping[str, Any]) -> str:
    """Serialize *obj* with sorted keys, no whitespace, and ASCII escapes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def compute_feature_config_hash(cfg_dict: Mapping[str, Any]) -> str:
    """Return ``sha256(canonical_json(cfg_dict))`` as a lowercase hex string."""
    payload = _canonical_json(cfg_dict).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_feature_config(
    *,
    source_normalized_parquet_path: Path | str,
    source_normalized_manifest_path: Path | str,
    source_successor_state_path: Path | str,
    output_feature_parquet_path: Path | str,
    output_feature_manifest_path: Path | str,
    code_commit_sha: str = "unknown",
) -> FeatureComputationConfig:
    """Construct a :class:`FeatureComputationConfig` and stamp its hash.

    The schema-related fields (windows, names, rules, policies) are
    locked to the Phase 4bh-B v001 contract; only the path fields and
    ``code_commit_sha`` are accepted as inputs. The returned config has
    a non-empty :attr:`feature_config_hash` derived from a canonical-JSON
    serialization of the locked fields.
    """
    base = FeatureComputationConfig(
        dataset_family=FEATURE_DATASET_FAMILY,
        dataset_version=FEATURE_DATASET_VERSION,
        feature_schema_version=FEATURE_SCHEMA_VERSION,
        source_normalized_parquet_path=str(source_normalized_parquet_path),
        source_normalized_manifest_path=str(source_normalized_manifest_path),
        source_successor_state_path=str(source_successor_state_path),
        output_feature_parquet_path=str(output_feature_parquet_path),
        output_feature_manifest_path=str(output_feature_manifest_path),
        windows_ms=FEATURE_WINDOWS_MS_V001,
        feature_names=FEATURE_NAMES_V001,
        timestamp_alignment="event_aligned",
        causal_window_rule="trailing_right_open_left",
        same_timestamp_tie_rule="row_index_le_R",
        null_policy=dict(NULL_POLICY_V001),
        invalid_window_policy=dict(INVALID_WINDOW_POLICY_V001),
        decimal_policy=dict(DECIMAL_POLICY_V001),
        code_commit_sha=code_commit_sha,
        feature_config_hash="",
    )
    digest = compute_feature_config_hash(base.to_canonical_dict())
    return FeatureComputationConfig(
        dataset_family=base.dataset_family,
        dataset_version=base.dataset_version,
        feature_schema_version=base.feature_schema_version,
        source_normalized_parquet_path=base.source_normalized_parquet_path,
        source_normalized_manifest_path=base.source_normalized_manifest_path,
        source_successor_state_path=base.source_successor_state_path,
        output_feature_parquet_path=base.output_feature_parquet_path,
        output_feature_manifest_path=base.output_feature_manifest_path,
        windows_ms=base.windows_ms,
        feature_names=base.feature_names,
        timestamp_alignment=base.timestamp_alignment,
        causal_window_rule=base.causal_window_rule,
        same_timestamp_tie_rule=base.same_timestamp_tie_rule,
        null_policy=base.null_policy,
        invalid_window_policy=base.invalid_window_policy,
        decimal_policy=base.decimal_policy,
        code_commit_sha=base.code_commit_sha,
        feature_config_hash=digest,
    )


# ---------------------------------------------------------------------------
# Module sanity assertions executed at import time
# ---------------------------------------------------------------------------

# 16 lineage + 45 feature/quality = 61 total columns.
assert len(LINEAGE_COLUMNS_V001) == 16
assert len(FEATURE_NAMES_V001) == 45
assert len(FEATURE_SCHEMA_V001) == 61

# 4 windows x 10 templates = 40 windowed feature names.
_windowed_count = len(FEATURE_WINDOWS_MS_V001) * len(PER_WINDOW_FEATURE_TEMPLATES)
assert _windowed_count == 40

# 4 windows total, in canonical order.
assert FEATURE_WINDOWS_MS_V001 == (1000, 5000, 15000, 60000)
assert FEATURE_WINDOW_LABELS_V001 == ("1s", "5s", "15s", "60s")


__all__ = [
    "DECIMAL_POLICY_V001",
    "FEATURE_DATASET_FAMILY",
    "FEATURE_DATASET_VERSION",
    "FEATURE_NAMES_V001",
    "FEATURE_SCHEMA_V001",
    "FEATURE_SCHEMA_VERSION",
    "FEATURE_WINDOWS_MS_V001",
    "FEATURE_WINDOW_LABELS_V001",
    "FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS",
    "FeatureComputationConfig",
    "FeatureSchemaError",
    "INVALID_WINDOW_POLICY_V001",
    "LINEAGE_COLUMNS_V001",
    "NULL_POLICY_V001",
    "PER_WINDOW_FEATURE_TEMPLATES",
    "SOURCE_NORMALIZED_DATASET_FAMILY",
    "SOURCE_NORMALIZED_DATASET_VERSION",
    "assert_no_forbidden_substrings",
    "build_feature_config",
    "compute_feature_config_hash",
]
