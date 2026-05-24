"""Phase 4bm-O multi-day v002 aggTrades label schema constants and config helpers.

Implements the exact Phase 4bm-N 40-column label schema for the future
label family ``microstructure_labels_aggtrades_v001 @ v002``:

- 4 forward horizons: ``1s``, ``5s``, ``15s``, ``60s`` paired with
  ``[1000, 5000, 15000, 60000]`` ms (mirrors v001 Phase 4bj-B verbatim);
- 8 label columns (4 regression ``forward_log_return_*`` and 4
  classification ``forward_direction_*``);
- 12 per-horizon support columns plus 2 global support columns
  (``label_invalid_price_flag``, ``label_any_censored_flag``);
- 17 lineage / identity / metadata columns;
- a single ``label_config_hash`` column;
- 40-column total schema in canonical column order.

Schema-level differences from the v001 Phase 4bj-B contract:

- v002 lineage replaces the v001 per-day ``source_normalized_parquet_sha256``
  with the multi-day ``source_normalized_manifest_sha256`` (since the v002
  normalized family is indexed by a 90-day multi-day manifest);
- v002 lineage adds ``source_raw_manifest_sha256`` as a fully required
  column (v002-explicit raw lineage; v001 omitted this);
- v002 lineage replaces the v001 ``source_phase_4bi_b_gate_report_sha256``
  with the v002 ``source_phase_4bm_j_gate_report_sha256`` and replaces the
  v001 ``source_feature_successor_state_sha256`` semantics with the v002
  Phase 4bm-L successor-state SHA;
- the column count rises from v001's 39 to v002's 40.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute labels (it only declares constants and a
  deterministic ``label_config_hash`` builder);
- does NOT mutate any artefact.

The ``label_config_hash`` is a SHA256 over the canonical-JSON
serialisation (sorted keys, ASCII, no whitespace) of the locked
schema-policy fields plus the v002 upstream lineage SHAs.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any, Final

# ---------------------------------------------------------------------------
# Identity / version constants
# ---------------------------------------------------------------------------

LABEL_DATASET_FAMILY_V002: Final = "microstructure_labels_aggtrades_v001"
LABEL_DATASET_VERSION_V002: Final = "v002"
LABEL_SCHEMA_VERSION_V002: Final = "v001"

SOURCE_FEATURE_DATASET_FAMILY_V002: Final = "microstructure_features_aggtrades_v001"
SOURCE_FEATURE_DATASET_VERSION_V002: Final = "v002"

SOURCE_NORMALIZED_DATASET_FAMILY_V002: Final = (
    "microstructure_normalized_aggtrades_v001"
)
SOURCE_NORMALIZED_DATASET_VERSION_V002: Final = "v002"

SOURCE_RAW_DATASET_FAMILY_V002: Final = "microstructure_raw_aggtrades_v001"
SOURCE_RAW_DATASET_VERSION_V002: Final = "v002"

LABEL_SYMBOL_V002: Final = "BTCUSDT"
LABEL_SYMBOL_LIST_V002: Final[tuple[str, ...]] = ("BTCUSDT",)

LABEL_UTC_DATE_START_V002: Final = "2024-12-01"
LABEL_UTC_DATE_END_V002: Final = "2025-02-28"
LABEL_DATE_COUNT_V002: Final = 90
LABEL_EXPECTED_ROW_COUNT_V002: Final = 155_153_449


# ---------------------------------------------------------------------------
# Horizon constants (mirror Phase 4bj-B verbatim)
# ---------------------------------------------------------------------------

LABEL_HORIZONS_V002: Final[tuple[str, ...]] = ("1s", "5s", "15s", "60s")
"""Horizon labels in canonical order."""

LABEL_HORIZON_MS_V002: Final[tuple[int, ...]] = (1000, 5000, 15000, 60000)
"""Horizon offsets in milliseconds paired 1:1 with ``LABEL_HORIZONS_V002``."""


# ---------------------------------------------------------------------------
# Label and support column names
# ---------------------------------------------------------------------------


def _build_label_names() -> tuple[str, ...]:
    names: list[str] = []
    for label in LABEL_HORIZONS_V002:
        names.append(f"forward_log_return_{label}")
    for label in LABEL_HORIZONS_V002:
        names.append(f"forward_direction_{label}")
    return tuple(names)


LABEL_NAMES_V002: Final[tuple[str, ...]] = _build_label_names()
"""The 8 label column names in canonical order (regression then classification)."""


def _build_support_column_names() -> tuple[str, ...]:
    names: list[str] = []
    for label in LABEL_HORIZONS_V002:
        names.append(f"reference_row_index_{label}")
        names.append(f"reference_timestamp_ms_{label}")
        names.append(f"horizon_censored_flag_{label}")
    names.append("label_invalid_price_flag")
    names.append("label_any_censored_flag")
    return tuple(names)


LABEL_SUPPORT_COLUMN_NAMES_V002: Final[tuple[str, ...]] = _build_support_column_names()
"""The 14 support column names in canonical order."""


# ---------------------------------------------------------------------------
# Lineage / identity / metadata columns
# ---------------------------------------------------------------------------

LABEL_LINEAGE_COLUMNS_V002: Final[tuple[str, ...]] = (
    "dataset_family",
    "dataset_version",
    "label_schema_version",
    "source_feature_dataset_family",
    "source_feature_dataset_version",
    "source_feature_manifest_sha256",
    "source_feature_parquet_sha256",
    "source_feature_successor_state_sha256",
    "source_phase_4bm_j_gate_report_sha256",
    "source_normalized_manifest_sha256",
    "source_raw_manifest_sha256",
    "symbol",
    "utc_date",
    "row_index",
    "agg_trade_id",
    "feature_timestamp_ms",
    "source_transact_time_ms",
)
"""The 17 lineage / identity / metadata columns in canonical order."""


# ---------------------------------------------------------------------------
# Full canonical schema (lineage + label_config_hash + labels + support)
# ---------------------------------------------------------------------------

LABEL_SCHEMA_V002: Final[tuple[str, ...]] = (
    LABEL_LINEAGE_COLUMNS_V002
    + ("label_config_hash",)
    + LABEL_NAMES_V002
    + LABEL_SUPPORT_COLUMN_NAMES_V002
)
"""All 40 columns in canonical order."""

LABEL_SCHEMA_COLUMNS_V002: Final[tuple[str, ...]] = LABEL_SCHEMA_V002
"""Alias for :data:`LABEL_SCHEMA_V002` exposed for explicit naming parity."""


# ---------------------------------------------------------------------------
# Forbidden-substring detector (per Phase 4bm-N §27 verbatim)
# ---------------------------------------------------------------------------

FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002: Final[tuple[str, ...]] = (
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
    "entry",
    "exit",
    "signal",
    "target",
    "barrier",
    "liquidation",
)
"""Forbidden substrings that must not appear in any v002 output column name."""


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class LabelSchemaErrorV002(RuntimeError):
    """Raised when a Phase 4bm-O label schema invariant fails closed."""


def assert_no_forbidden_label_substrings_v002(column_names: Sequence[str]) -> None:
    """Fail closed if any column name (lowercased) contains a forbidden token."""
    for col in column_names:
        lower = col.lower()
        for token in FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002:
            if token in lower:
                raise LabelSchemaErrorV002(
                    f"forbidden substring {token!r} found in column {col!r}"
                )


# ---------------------------------------------------------------------------
# Policy descriptors (constant strings used in the canonical-JSON hash)
# ---------------------------------------------------------------------------

ANCHOR_POLICY_V002: Final[str] = (
    "anchor_row=feature_row_R; anchor_timestamp=feature_timestamp_ms; "
    "anchor_source_timestamp=source_transact_time_ms; "
    "anchor_price=trade_price_of_normalized_aggtrade_row_identified_by_"
    "(agg_trade_id,row_index)_inside_anchor_per_day_normalized_parquet; "
    "no_mark_price; no_index_price; no_bid_or_ask; "
    "no_book; no_external_data; no_future_feature_values"
)
"""Constant string describing the anchor policy for hashing."""

FUTURE_REFERENCE_POLICY_V002: Final[str] = (
    "target_timestamp_ms=feature_timestamp_ms+H_ms; "
    "envelope_terminal_unix_ms=max_source_transact_time_ms_across_v002_90day_envelope; "
    "if target_timestamp_ms>envelope_terminal_unix_ms "
    "then all_horizon_labels_null_and_horizon_censored_flag_true; "
    "else reference_row=largest_row_index_normalized_aggtrade_row_across_envelope_with_"
    "transact_time_ms_le_target_timestamp_ms; "
    "cross_day_reference_allowed_within_envelope; "
    "same_timestamp_tie_break=largest_row_index_at_that_timestamp_"
    "inside_its_per_day_source_parquet; "
    "reference_timestamp_ms_H=transact_time_ms_of_reference_row; "
    "reference_trade_price_H=trade_price_of_reference_row; "
    "no_first_trade_after_target; no_look_past_target; "
    "no_look_past_envelope_terminal_unix_ms; "
    "no_mark_price; no_index_price; no_book; no_external_data; "
    "no_future_feature_columns; no_synthetic_extrapolation; "
    "no_zero_padding; no_fabricated_rows"
)
"""Constant string describing the future-reference policy for hashing."""

DIRECTION_THRESHOLD_POLICY_V002: Final[str] = (
    "forward_direction_H_derived_only_from_forward_log_return_H; "
    "plus_one_if_strictly_positive; zero_if_exactly_zero; "
    "minus_one_if_strictly_negative; null_if_forward_log_return_H_is_null; "
    "strict_sign_threshold_zero_log_return; "
    "no_deadband; no_bp_threshold; no_threshold_optimization; "
    "no_cost_based_threshold_at_v002"
)
"""Constant string describing the direction-threshold policy for hashing."""

NULL_CENSORING_POLICY_V002: Final[str] = (
    "keep_all_feature_rows; per_horizon_independent_envelope_terminal_censoring; "
    "horizon_censored_flag_true_when_target_exceeds_envelope_terminal_unix_ms; "
    "no_per_day_censoring; cross_day_reference_allowed_within_envelope; "
    "label_any_censored_flag_true_if_any_horizon_censored; "
    "label_invalid_price_flag_true_if_anchor_or_reference_price_le_zero; "
    "no_forward_fill_beyond_envelope; no_cross_envelope_stitching; "
    "no_nan_no_inf_in_outputs"
)
"""Constant string describing the null / censoring policy for hashing."""

DTYPE_POLICY_V002: Final[str] = (
    "row_index=int64; agg_trade_id=int64; "
    "feature_timestamp_ms=int64_utc_ms; source_transact_time_ms=int64_utc_ms; "
    "reference_row_index_per_horizon=nullable_int64; "
    "reference_timestamp_ms_per_horizon=nullable_int64_utc_ms; "
    "dataset_ids_versions_hashes_symbol_utc_date_label_config_hash=string; "
    "forward_log_return_per_horizon=nullable_float64; "
    "forward_direction_per_horizon=nullable_int8_in_minus1_0_plus1; "
    "horizon_censored_flag_per_horizon=non_nullable_bool; "
    "label_invalid_price_flag=non_nullable_bool; "
    "label_any_censored_flag=non_nullable_bool"
)
"""Constant string describing the dtype policy for hashing."""


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def _require_hex64(value: str, *, label: str) -> None:
    if not isinstance(value, str) or not _HEX64_RE.match(value):
        raise LabelSchemaErrorV002(
            f"{label} must be 64-char lowercase hex (got {value!r})"
        )


def _canonical_json(obj: Mapping[str, Any]) -> str:
    """Serialize *obj* with sorted keys, no whitespace, and ASCII escapes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


# ---------------------------------------------------------------------------
# label_config_hash builder (Phase 4bm-N §25)
# ---------------------------------------------------------------------------


def build_label_config_hash_v002(
    *,
    source_feature_manifest_sha256: str,
    source_feature_successor_state_sha256: str,
    source_phase_4bm_j_gate_report_sha256: str,
    source_normalized_manifest_sha256: str,
    source_raw_manifest_sha256: str,
    feature_config_hash: str,
) -> str:
    """Return the deterministic ``label_config_hash`` for the v002 schema lock.

    Builds a canonical-JSON object (sorted keys, ASCII, no whitespace)
    containing exactly the fields named in Phase 4bm-N §25 and returns
    the lowercase hex SHA256 of its UTF-8 encoding.
    """
    _require_hex64(
        source_feature_manifest_sha256, label="source_feature_manifest_sha256"
    )
    _require_hex64(
        source_feature_successor_state_sha256,
        label="source_feature_successor_state_sha256",
    )
    _require_hex64(
        source_phase_4bm_j_gate_report_sha256,
        label="source_phase_4bm_j_gate_report_sha256",
    )
    _require_hex64(
        source_normalized_manifest_sha256, label="source_normalized_manifest_sha256"
    )
    _require_hex64(source_raw_manifest_sha256, label="source_raw_manifest_sha256")
    _require_hex64(feature_config_hash, label="feature_config_hash")
    payload: dict[str, Any] = {
        "dataset_family": LABEL_DATASET_FAMILY_V002,
        "dataset_version": LABEL_DATASET_VERSION_V002,
        "label_schema_version": LABEL_SCHEMA_VERSION_V002,
        "label_list": list(LABEL_NAMES_V002),
        "support_column_list": list(LABEL_SUPPORT_COLUMN_NAMES_V002),
        "lineage_column_list": list(LABEL_LINEAGE_COLUMNS_V002),
        "horizon_list": list(LABEL_HORIZONS_V002),
        "horizon_ms_list": list(LABEL_HORIZON_MS_V002),
        "anchor_policy": ANCHOR_POLICY_V002,
        "future_reference_policy": FUTURE_REFERENCE_POLICY_V002,
        "direction_threshold_policy": DIRECTION_THRESHOLD_POLICY_V002,
        "null_censoring_policy": NULL_CENSORING_POLICY_V002,
        "dtype_policy": DTYPE_POLICY_V002,
        "source_feature_manifest_sha256": source_feature_manifest_sha256,
        "source_feature_successor_state_sha256": source_feature_successor_state_sha256,
        "source_phase_4bm_j_gate_report_sha256": source_phase_4bm_j_gate_report_sha256,
        "source_normalized_manifest_sha256": source_normalized_manifest_sha256,
        "source_raw_manifest_sha256": source_raw_manifest_sha256,
        "feature_config_hash": feature_config_hash,
    }
    encoded = _canonical_json(payload).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ---------------------------------------------------------------------------
# Import-time sanity assertions
# ---------------------------------------------------------------------------

assert LABEL_HORIZONS_V002 == ("1s", "5s", "15s", "60s")
assert LABEL_HORIZON_MS_V002 == (1000, 5000, 15000, 60000)
assert len(LABEL_HORIZONS_V002) == len(LABEL_HORIZON_MS_V002) == 4
assert len(LABEL_NAMES_V002) == 8
assert len(LABEL_SUPPORT_COLUMN_NAMES_V002) == 14
assert len(LABEL_LINEAGE_COLUMNS_V002) == 17
assert len(LABEL_SCHEMA_V002) == 40

# Canonical ordering invariants (Phase 4bm-N §14 verbatim).
assert LABEL_SCHEMA_V002[0] == "dataset_family"
assert LABEL_SCHEMA_V002[10] == "source_raw_manifest_sha256"
assert LABEL_SCHEMA_V002[16] == "source_transact_time_ms"
assert LABEL_SCHEMA_V002[17] == "label_config_hash"
assert LABEL_SCHEMA_V002[18] == "forward_log_return_1s"
assert LABEL_SCHEMA_V002[21] == "forward_log_return_60s"
assert LABEL_SCHEMA_V002[22] == "forward_direction_1s"
assert LABEL_SCHEMA_V002[25] == "forward_direction_60s"
assert LABEL_SCHEMA_V002[26] == "reference_row_index_1s"
assert LABEL_SCHEMA_V002[38] == "label_invalid_price_flag"
assert LABEL_SCHEMA_V002[39] == "label_any_censored_flag"


__all__ = [
    "ANCHOR_POLICY_V002",
    "DIRECTION_THRESHOLD_POLICY_V002",
    "DTYPE_POLICY_V002",
    "FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002",
    "FUTURE_REFERENCE_POLICY_V002",
    "LABEL_DATASET_FAMILY_V002",
    "LABEL_DATASET_VERSION_V002",
    "LABEL_DATE_COUNT_V002",
    "LABEL_EXPECTED_ROW_COUNT_V002",
    "LABEL_HORIZONS_V002",
    "LABEL_HORIZON_MS_V002",
    "LABEL_LINEAGE_COLUMNS_V002",
    "LABEL_NAMES_V002",
    "LABEL_SCHEMA_COLUMNS_V002",
    "LABEL_SCHEMA_V002",
    "LABEL_SCHEMA_VERSION_V002",
    "LABEL_SUPPORT_COLUMN_NAMES_V002",
    "LABEL_SYMBOL_LIST_V002",
    "LABEL_SYMBOL_V002",
    "LABEL_UTC_DATE_END_V002",
    "LABEL_UTC_DATE_START_V002",
    "LabelSchemaErrorV002",
    "NULL_CENSORING_POLICY_V002",
    "SOURCE_FEATURE_DATASET_FAMILY_V002",
    "SOURCE_FEATURE_DATASET_VERSION_V002",
    "SOURCE_NORMALIZED_DATASET_FAMILY_V002",
    "SOURCE_NORMALIZED_DATASET_VERSION_V002",
    "SOURCE_RAW_DATASET_FAMILY_V002",
    "SOURCE_RAW_DATASET_VERSION_V002",
    "assert_no_forbidden_label_substrings_v002",
    "build_label_config_hash_v002",
]
