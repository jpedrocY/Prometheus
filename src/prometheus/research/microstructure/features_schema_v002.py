"""Phase 4bm-H multi-day v002 aggTrades feature schema constants and config builder.

This module defines the v002 feature schema for the derived family
``microstructure_features_aggtrades_v001`` computed against the
``v002`` multi-day normalized derived family. It mirrors the v001
Phase 4bh-B feature/quality column set (4 windows × 10 per-window +
3 time context + 2 quality = 45 columns) and replaces the v001 16
lineage / identity / metadata columns with the v002 17-column lineage
contract required by the Phase 4bm-G feature-boundary design memo:

- ``source_dataset_version`` is ``"v002"`` (was ``"v001"`` at v001);
- ``source_normalized_parquet_per_day_sha256`` replaces v001's
  ``source_normalized_parquet_sha256``;
- ``source_phase_4bm_d_gate_report_sha256`` replaces v001's
  ``source_phase_4bf_gate_report_sha256``;
- new column ``source_phase_4bm_e_outcome`` is added with the
  literal value ``"Option B / Decision form 2"`` (per Phase 4bm-E /
  Phase 4bm-F);
- v001's ``source_feature_schema_version`` lineage column is dropped;
  the equivalent ``feature_schema_version`` identity column is
  retained at v001 value.

The full v002 schema therefore has 17 lineage + 45 feature/quality =
**62 columns** in canonical column order.

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

from .features_schema import (
    FEATURE_DATASET_FAMILY,
    FEATURE_NAMES_V001,
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS,
    PER_WINDOW_FEATURE_TEMPLATES,
    FeatureSchemaError,
)

# ---------------------------------------------------------------------------
# Identity / version constants for v002
# ---------------------------------------------------------------------------

FEATURE_DATASET_VERSION_V002 = "v002"
"""The dataset_version for v002 feature outputs (Phase 4bm-H)."""

FEATURE_SCHEMA_VERSION_V002 = "v001"
"""The feature_schema_version for v002 feature outputs.

The schema_version remains at ``"v001"`` because the v002 feature /
quality column set is the v001 Phase 4bh-B finalised list. Only the
lineage block changes for v002. Any future schema mutation requires a
new ``feature_schema_version`` value.
"""

SOURCE_NORMALIZED_DATASET_FAMILY_V002 = "microstructure_normalized_aggtrades_v001"
"""The source derived family (unchanged from v001; only version differs)."""

SOURCE_NORMALIZED_DATASET_VERSION_V002 = "v002"
"""The source dataset_version v002 normalization runs (Phase 4bm-B / 4bm-D)."""

PHASE_4BM_E_OUTCOME_LITERAL = "Option B / Decision form 2"
"""Locked Phase 4bm-E outcome value carried verbatim on every v002 feature row.

Phase 4bm-G §13 forbidden-substring detector flags the token
``decision`` to prevent forbidden decision-score / decision-output
computed features. The lineage column name therefore reads
``source_phase_4bm_e_outcome``; the literal **value** is the Phase
4bm-E memo's recorded outcome ``"Option B / Decision form 2"``
verbatim. The renamed column carries the same semantic content as the
v002 prompt's ``source_phase_4bm_e_decision`` field; the rename is the
Phase 4bm-G §13-mandated "adjust to a safe equivalent and document the
reason" path.
"""


# ---------------------------------------------------------------------------
# Lineage / identity / metadata columns (17 at v002)
# ---------------------------------------------------------------------------

LINEAGE_COLUMNS_V002: tuple[str, ...] = (
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
"""The 17 identity / lineage / metadata columns for v002, canonical order."""


# Re-exported aliases for clarity at call sites.
FEATURE_NAMES_V002: tuple[str, ...] = FEATURE_NAMES_V001
"""The 45 feature / quality columns (identical to v001 Phase 4bh-B contract)."""

FEATURE_WINDOWS_MS_V002: tuple[int, ...] = FEATURE_WINDOWS_MS_V001
"""Trailing-window sizes in milliseconds for v002 (= v001: 1s / 5s / 15s / 60s)."""

FEATURE_WINDOW_LABELS_V002: tuple[str, ...] = FEATURE_WINDOW_LABELS_V001
"""Human-readable window labels for v002 (= v001)."""

PER_WINDOW_FEATURE_TEMPLATES_V002: tuple[str, ...] = PER_WINDOW_FEATURE_TEMPLATES
"""Per-window feature name templates for v002 (= v001)."""


FEATURE_SCHEMA_V002: tuple[str, ...] = LINEAGE_COLUMNS_V002 + FEATURE_NAMES_V002
"""All 62 columns (17 lineage + 45 feature/quality) in canonical order."""


# ---------------------------------------------------------------------------
# Forbidden-substring detector (reused verbatim from v001)
# ---------------------------------------------------------------------------

FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002: tuple[str, ...] = (
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS
)
"""Reuses the v001 Phase 4bh-B 26-token forbidden-substring list verbatim."""


def assert_no_forbidden_substrings_v002(column_names: tuple[str, ...]) -> None:
    """Fail closed if any column name (lowercased) contains a forbidden token."""
    for col in column_names:
        lower = col.lower()
        for token in FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002:
            if token in lower:
                raise FeatureSchemaError(
                    f"forbidden substring {token!r} found in column {col!r}"
                )


# ---------------------------------------------------------------------------
# Cross-day rolling-window policy (Phase 4bm-G §16, policy 1)
# ---------------------------------------------------------------------------

CROSS_DAY_LOOKBACK_POLICY_V002 = "causal_cross_day_lookback"
"""Cross-day rolling-window policy at v002.

Phase 4bm-G §14 / §16 recommends policy 1 (causal cross-day lookback):
for each current-day output row, use prior-day tail rows as read-only
context to populate trailing windows. Day 1 has no prior day in scope;
rows on day 1 whose trailing window would extend before the v002 date
range carry ``rolling_missing_window_flag = True`` and treat the
unavailable window region as containing zero events.
"""

CROSS_DAY_TAIL_BUFFER_MS = max(FEATURE_WINDOWS_MS_V002)
"""Prior-day tail buffer in ms (= max trailing window = 60_000 ms)."""


# ---------------------------------------------------------------------------
# Decimal / null / invalid-window / boundary / timestamp / leakage policies
# ---------------------------------------------------------------------------

DECIMAL_POLICY_V002: Mapping[str, Any] = {
    "raw_price_storage": "decimal_string",
    "raw_quantity_storage": "decimal_string",
    "ratio_storage": "float64_nullable",
    "log_return_storage": "float64_nullable",
    "decimal_module": "stdlib_decimal",
    "decimal_precision_digits": 50,
    "decimal_rounding": "ROUND_HALF_EVEN",
}
"""Decimal / float storage policy at v002 (mirrors v001 Phase 4bh-B)."""

NULL_POLICY_V002: Mapping[str, Any] = {
    "rolling_quantity_mean": "null_when_empty",
    "rolling_aggressive_flow_ratio": "null_when_zero_denominator",
    "rolling_log_return_past_window": "null_when_no_prior_reference_or_zero_price",
    "no_imputation_across_invalid_windows": True,
    "no_nan_no_inf_for_floats": True,
}
"""Null policy for nullable feature columns at v002."""

INVALID_WINDOW_POLICY_V002: Mapping[str, Any] = {
    "propagate_from_source_manifest": True,
    "invalid_window_flag_set_when_row_in_invalid_window": True,
    "rolling_missing_window_flag_set_when_any_window_intersects_invalid": True,
    "rolling_missing_window_flag_set_when_window_crosses_v002_start": True,
    "no_imputation_inside_invalid_windows": True,
}
"""Invalid-window + boundary-missing propagation policy at v002."""

WINDOW_BOUNDARY_POLICY_V002 = "trailing_right_closed_left_open"
"""Window boundary policy: windows are (T - window_ms, T]."""

TIMESTAMP_POLICY_V002 = "event_aligned_utc_ms_int64"
"""Timestamp policy: UTC ms int64, feature_timestamp == source_transact_time."""

LEAKAGE_POLICY_V002 = "causal_only_no_future_lookahead"
"""Leakage policy: only rows with transact_time <= T contribute to features at T."""

SAME_TIMESTAMP_TIE_RULE_V002 = "row_index_le_R"
"""Same-timestamp tie-break by row_index (ascending) within the same day."""


_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


# ---------------------------------------------------------------------------
# Feature computation config for v002
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FeatureComputationConfigV002:
    """Frozen, deterministic config record for one Phase 4bm-H feature run.

    The :attr:`feature_config_hash` is a SHA256 over the canonical-JSON
    serialization of the locked fields (sorted keys, no spaces,
    ASCII-only) so that any change to any field deterministically
    changes the hash.
    """

    dataset_family: str
    dataset_version: str
    feature_schema_version: str
    source_dataset_family: str
    source_dataset_version: str
    source_normalized_manifest_path: str
    source_successor_state_path: str
    output_feature_manifest_path: str
    output_feature_root_dir: str
    windows_ms: tuple[int, ...]
    feature_names: tuple[str, ...]
    timestamp_alignment: str
    timestamp_policy: str
    causal_window_rule: str
    leakage_policy: str
    same_timestamp_tie_rule: str
    cross_day_lookback_policy: str
    cross_day_tail_buffer_ms: int
    null_policy: Mapping[str, Any] = field(default_factory=lambda: dict(NULL_POLICY_V002))
    invalid_window_policy: Mapping[str, Any] = field(
        default_factory=lambda: dict(INVALID_WINDOW_POLICY_V002)
    )
    decimal_policy: Mapping[str, Any] = field(
        default_factory=lambda: dict(DECIMAL_POLICY_V002)
    )
    code_commit_sha: str = "unknown"
    feature_config_hash: str = ""

    def __post_init__(self) -> None:
        if self.dataset_family != FEATURE_DATASET_FAMILY:
            raise FeatureSchemaError(
                f"dataset_family must be {FEATURE_DATASET_FAMILY!r}"
            )
        if self.dataset_version != FEATURE_DATASET_VERSION_V002:
            raise FeatureSchemaError(
                f"dataset_version must be {FEATURE_DATASET_VERSION_V002!r}"
            )
        if self.feature_schema_version != FEATURE_SCHEMA_VERSION_V002:
            raise FeatureSchemaError(
                f"feature_schema_version must be {FEATURE_SCHEMA_VERSION_V002!r}"
            )
        if self.source_dataset_family != SOURCE_NORMALIZED_DATASET_FAMILY_V002:
            raise FeatureSchemaError(
                f"source_dataset_family must be {SOURCE_NORMALIZED_DATASET_FAMILY_V002!r}"
            )
        if self.source_dataset_version != SOURCE_NORMALIZED_DATASET_VERSION_V002:
            raise FeatureSchemaError(
                f"source_dataset_version must be {SOURCE_NORMALIZED_DATASET_VERSION_V002!r}"
            )
        if tuple(self.windows_ms) != FEATURE_WINDOWS_MS_V002:
            raise FeatureSchemaError(
                f"windows_ms must equal {FEATURE_WINDOWS_MS_V002!r}"
            )
        if tuple(self.feature_names) != FEATURE_NAMES_V002:
            raise FeatureSchemaError(
                "feature_names must equal FEATURE_NAMES_V002 (count and order)"
            )
        if self.timestamp_alignment != "event_aligned":
            raise FeatureSchemaError("timestamp_alignment must be 'event_aligned'")
        if self.timestamp_policy != TIMESTAMP_POLICY_V002:
            raise FeatureSchemaError(
                f"timestamp_policy must be {TIMESTAMP_POLICY_V002!r}"
            )
        if self.causal_window_rule != "trailing_right_open_left":
            raise FeatureSchemaError(
                "causal_window_rule must be 'trailing_right_open_left' "
                "(window is (T - window_ms, T], with same-timestamp tie-break "
                "row_index <= R)"
            )
        if self.leakage_policy != LEAKAGE_POLICY_V002:
            raise FeatureSchemaError(
                f"leakage_policy must be {LEAKAGE_POLICY_V002!r}"
            )
        if self.same_timestamp_tie_rule != SAME_TIMESTAMP_TIE_RULE_V002:
            raise FeatureSchemaError(
                f"same_timestamp_tie_rule must be {SAME_TIMESTAMP_TIE_RULE_V002!r}"
            )
        if self.cross_day_lookback_policy != CROSS_DAY_LOOKBACK_POLICY_V002:
            raise FeatureSchemaError(
                f"cross_day_lookback_policy must be {CROSS_DAY_LOOKBACK_POLICY_V002!r}"
            )
        if self.cross_day_tail_buffer_ms != CROSS_DAY_TAIL_BUFFER_MS:
            raise FeatureSchemaError(
                f"cross_day_tail_buffer_ms must equal {CROSS_DAY_TAIL_BUFFER_MS!r}"
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
            "source_dataset_family": self.source_dataset_family,
            "source_dataset_version": self.source_dataset_version,
            "source_normalized_manifest_path": self.source_normalized_manifest_path,
            "source_successor_state_path": self.source_successor_state_path,
            "output_feature_manifest_path": self.output_feature_manifest_path,
            "output_feature_root_dir": self.output_feature_root_dir,
            "windows_ms": list(self.windows_ms),
            "feature_names": list(self.feature_names),
            "timestamp_alignment": self.timestamp_alignment,
            "timestamp_policy": self.timestamp_policy,
            "causal_window_rule": self.causal_window_rule,
            "leakage_policy": self.leakage_policy,
            "same_timestamp_tie_rule": self.same_timestamp_tie_rule,
            "cross_day_lookback_policy": self.cross_day_lookback_policy,
            "cross_day_tail_buffer_ms": int(self.cross_day_tail_buffer_ms),
            "null_policy": dict(self.null_policy),
            "invalid_window_policy": dict(self.invalid_window_policy),
            "decimal_policy": dict(self.decimal_policy),
            "code_commit_sha": self.code_commit_sha,
        }


def _canonical_json_v002(obj: Mapping[str, Any]) -> str:
    """Serialize *obj* with sorted keys, no whitespace, and ASCII escapes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def compute_feature_config_hash_v002(cfg_dict: Mapping[str, Any]) -> str:
    """Return ``sha256(canonical_json(cfg_dict))`` as a lowercase hex string."""
    payload = _canonical_json_v002(cfg_dict).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_feature_config_v002(
    *,
    source_normalized_manifest_path: Path | str,
    source_successor_state_path: Path | str,
    output_feature_manifest_path: Path | str,
    output_feature_root_dir: Path | str,
    code_commit_sha: str = "unknown",
) -> FeatureComputationConfigV002:
    """Construct a :class:`FeatureComputationConfigV002` and stamp its hash.

    The schema-related fields (windows, names, rules, policies) are
    locked to the Phase 4bm-G design and the Phase 4bh-B v001 feature /
    quality column set; only path fields and ``code_commit_sha`` are
    accepted as inputs. The returned config has a non-empty
    :attr:`feature_config_hash` derived from a canonical-JSON
    serialization of the locked fields.
    """
    base = FeatureComputationConfigV002(
        dataset_family=FEATURE_DATASET_FAMILY,
        dataset_version=FEATURE_DATASET_VERSION_V002,
        feature_schema_version=FEATURE_SCHEMA_VERSION_V002,
        source_dataset_family=SOURCE_NORMALIZED_DATASET_FAMILY_V002,
        source_dataset_version=SOURCE_NORMALIZED_DATASET_VERSION_V002,
        source_normalized_manifest_path=str(source_normalized_manifest_path),
        source_successor_state_path=str(source_successor_state_path),
        output_feature_manifest_path=str(output_feature_manifest_path),
        output_feature_root_dir=str(output_feature_root_dir),
        windows_ms=FEATURE_WINDOWS_MS_V002,
        feature_names=FEATURE_NAMES_V002,
        timestamp_alignment="event_aligned",
        timestamp_policy=TIMESTAMP_POLICY_V002,
        causal_window_rule="trailing_right_open_left",
        leakage_policy=LEAKAGE_POLICY_V002,
        same_timestamp_tie_rule=SAME_TIMESTAMP_TIE_RULE_V002,
        cross_day_lookback_policy=CROSS_DAY_LOOKBACK_POLICY_V002,
        cross_day_tail_buffer_ms=CROSS_DAY_TAIL_BUFFER_MS,
        null_policy=dict(NULL_POLICY_V002),
        invalid_window_policy=dict(INVALID_WINDOW_POLICY_V002),
        decimal_policy=dict(DECIMAL_POLICY_V002),
        code_commit_sha=code_commit_sha,
        feature_config_hash="",
    )
    digest = compute_feature_config_hash_v002(base.to_canonical_dict())
    return FeatureComputationConfigV002(
        dataset_family=base.dataset_family,
        dataset_version=base.dataset_version,
        feature_schema_version=base.feature_schema_version,
        source_dataset_family=base.source_dataset_family,
        source_dataset_version=base.source_dataset_version,
        source_normalized_manifest_path=base.source_normalized_manifest_path,
        source_successor_state_path=base.source_successor_state_path,
        output_feature_manifest_path=base.output_feature_manifest_path,
        output_feature_root_dir=base.output_feature_root_dir,
        windows_ms=base.windows_ms,
        feature_names=base.feature_names,
        timestamp_alignment=base.timestamp_alignment,
        timestamp_policy=base.timestamp_policy,
        causal_window_rule=base.causal_window_rule,
        leakage_policy=base.leakage_policy,
        same_timestamp_tie_rule=base.same_timestamp_tie_rule,
        cross_day_lookback_policy=base.cross_day_lookback_policy,
        cross_day_tail_buffer_ms=base.cross_day_tail_buffer_ms,
        null_policy=base.null_policy,
        invalid_window_policy=base.invalid_window_policy,
        decimal_policy=base.decimal_policy,
        code_commit_sha=base.code_commit_sha,
        feature_config_hash=digest,
    )


# ---------------------------------------------------------------------------
# Module sanity assertions executed at import time
# ---------------------------------------------------------------------------

assert len(LINEAGE_COLUMNS_V002) == 17
assert len(FEATURE_NAMES_V002) == 45
assert len(FEATURE_SCHEMA_V002) == 62
assert FEATURE_WINDOWS_MS_V002 == (1000, 5000, 15000, 60000)
assert FEATURE_WINDOW_LABELS_V002 == ("1s", "5s", "15s", "60s")
assert CROSS_DAY_TAIL_BUFFER_MS == 60_000


__all__ = [
    "CROSS_DAY_LOOKBACK_POLICY_V002",
    "CROSS_DAY_TAIL_BUFFER_MS",
    "DECIMAL_POLICY_V002",
    "FEATURE_DATASET_VERSION_V002",
    "FEATURE_NAMES_V002",
    "FEATURE_SCHEMA_V002",
    "FEATURE_SCHEMA_VERSION_V002",
    "FEATURE_WINDOWS_MS_V002",
    "FEATURE_WINDOW_LABELS_V002",
    "FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002",
    "FeatureComputationConfigV002",
    "INVALID_WINDOW_POLICY_V002",
    "LEAKAGE_POLICY_V002",
    "LINEAGE_COLUMNS_V002",
    "NULL_POLICY_V002",
    "PER_WINDOW_FEATURE_TEMPLATES_V002",
    "PHASE_4BM_E_OUTCOME_LITERAL",
    "SAME_TIMESTAMP_TIE_RULE_V002",
    "SOURCE_NORMALIZED_DATASET_FAMILY_V002",
    "SOURCE_NORMALIZED_DATASET_VERSION_V002",
    "TIMESTAMP_POLICY_V002",
    "WINDOW_BOUNDARY_POLICY_V002",
    "assert_no_forbidden_substrings_v002",
    "build_feature_config_v002",
    "compute_feature_config_hash_v002",
]
