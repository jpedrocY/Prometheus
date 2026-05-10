"""Phase 4bj-C aggTrades label schema constants and config helpers.

Implements the exact Phase 4bj-B v001 label schema for the future
label family ``microstructure_labels_aggtrades_v001``:

- 4 forward horizons only: ``1s``, ``5s``, ``15s``, ``60s`` paired
  with ``[1000, 5000, 15000, 60000]`` ms;
- 8 label columns (4 regression ``forward_log_return_*`` and 4
  classification ``forward_direction_*``);
- 14 support columns (4 each of ``reference_row_index_*``,
  ``reference_timestamp_ms_*``, ``horizon_censored_flag_*``, plus
  ``label_invalid_price_flag`` and ``label_any_censored_flag``);
- 17 lineage / identity / metadata columns
  (``label_config_hash`` is included here);
- 39-column total schema in canonical column order.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT compute labels (it only declares constants and a
  deterministic ``label_config_hash`` builder);
- does NOT mutate any artefact.

The ``label_config_hash`` is a SHA256 over the canonical-JSON
serialisation (sorted keys, ASCII, no whitespace) of the locked
schema-policy fields plus the source-lineage SHAs.
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

LABEL_DATASET_FAMILY_V001: Final = "microstructure_labels_aggtrades_v001"
LABEL_DATASET_VERSION_V001: Final = "v001"
LABEL_SCHEMA_VERSION_V001: Final = "v001"

SOURCE_FEATURE_DATASET_FAMILY_V001: Final = "microstructure_features_aggtrades_v001"
SOURCE_FEATURE_DATASET_VERSION_V001: Final = "v001"


# ---------------------------------------------------------------------------
# Horizon constants
# ---------------------------------------------------------------------------

LABEL_HORIZONS_V001: Final[tuple[str, ...]] = ("1s", "5s", "15s", "60s")
"""Horizon labels in canonical order."""

LABEL_HORIZON_MS_V001: Final[tuple[int, ...]] = (1000, 5000, 15000, 60000)
"""Horizon offsets in milliseconds paired 1:1 with ``LABEL_HORIZONS_V001``."""


# ---------------------------------------------------------------------------
# Label and support column names
# ---------------------------------------------------------------------------


def _build_label_names() -> tuple[str, ...]:
    names: list[str] = []
    for label in LABEL_HORIZONS_V001:
        names.append(f"forward_log_return_{label}")
    for label in LABEL_HORIZONS_V001:
        names.append(f"forward_direction_{label}")
    return tuple(names)


LABEL_NAMES_V001: Final[tuple[str, ...]] = _build_label_names()
"""The 8 label column names in canonical order (regression then classification)."""


def _build_support_column_names() -> tuple[str, ...]:
    names: list[str] = []
    for label in LABEL_HORIZONS_V001:
        names.append(f"reference_row_index_{label}")
        names.append(f"reference_timestamp_ms_{label}")
        names.append(f"horizon_censored_flag_{label}")
    names.append("label_invalid_price_flag")
    names.append("label_any_censored_flag")
    return tuple(names)


LABEL_SUPPORT_COLUMN_NAMES_V001: Final[tuple[str, ...]] = _build_support_column_names()
"""The 14 support column names in canonical order."""


# ---------------------------------------------------------------------------
# Lineage / identity / metadata columns
# ---------------------------------------------------------------------------

LABEL_LINEAGE_COLUMNS_V001: Final[tuple[str, ...]] = (
    "dataset_family",
    "dataset_version",
    "label_schema_version",
    "source_feature_dataset_family",
    "source_feature_dataset_version",
    "source_feature_manifest_sha256",
    "source_feature_parquet_sha256",
    "source_feature_successor_state_sha256",
    "source_phase_4bi_b_gate_report_sha256",
    "symbol",
    "utc_date",
    "row_index",
    "agg_trade_id",
    "feature_timestamp_ms",
    "source_transact_time_ms",
    "source_normalized_parquet_sha256",
    "label_config_hash",
)
"""The 17 lineage / identity / metadata columns in canonical order."""


# ---------------------------------------------------------------------------
# Full canonical schema (lineage + labels + support)
# ---------------------------------------------------------------------------

LABEL_SCHEMA_V001: Final[tuple[str, ...]] = (
    LABEL_LINEAGE_COLUMNS_V001 + LABEL_NAMES_V001 + LABEL_SUPPORT_COLUMN_NAMES_V001
)
"""All 39 columns in canonical order."""

LABEL_SCHEMA_COLUMNS_V001: Final[tuple[str, ...]] = LABEL_SCHEMA_V001
"""Alias for :data:`LABEL_SCHEMA_V001` exposed for explicit naming parity."""


# ---------------------------------------------------------------------------
# Forbidden-substring detector (per Phase 4bj-B schema lock)
# ---------------------------------------------------------------------------

FORBIDDEN_LABEL_COLUMN_SUBSTRINGS: Final[tuple[str, ...]] = (
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
"""Forbidden substrings that must not appear in any v001 output column name."""


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class LabelSchemaError(RuntimeError):
    """Raised when a Phase 4bj-C label schema invariant fails closed."""


def assert_no_forbidden_label_substrings(column_names: Sequence[str]) -> None:
    """Fail closed if any column name (lowercased) contains a forbidden token."""
    for col in column_names:
        lower = col.lower()
        for token in FORBIDDEN_LABEL_COLUMN_SUBSTRINGS:
            if token in lower:
                raise LabelSchemaError(
                    f"forbidden substring {token!r} found in column {col!r}"
                )


# ---------------------------------------------------------------------------
# Policy descriptors (constant strings used in the canonical-JSON hash)
# ---------------------------------------------------------------------------

ANCHOR_POLICY_V001: Final[str] = (
    "anchor_row=feature_row_R; anchor_timestamp=feature_timestamp_ms; "
    "anchor_source_timestamp=source_transact_time_ms; "
    "anchor_price=trade_price_of_normalized_aggtrade_row_identified_by_"
    "(agg_trade_id,row_index); no_mark_price; no_index_price; no_bid_or_ask; "
    "no_book; no_external_data; no_future_feature_values"
)
"""Constant string describing the anchor policy for hashing."""

FUTURE_REFERENCE_POLICY_V001: Final[str] = (
    "target_timestamp_ms=feature_timestamp_ms+H_ms; "
    "if target_timestamp_ms>max(source_normalized_transact_time_ms)_for_utc_date "
    "then all_horizon_labels_null_and_horizon_censored_flag_true; "
    "else reference_row=latest_normalized_aggtrade_row_with_"
    "transact_time_ms_le_target_timestamp_ms; "
    "same_timestamp_tie_break=largest_row_index_at_that_timestamp; "
    "reference_timestamp_ms_H=transact_time_ms_of_reference_row; "
    "reference_trade_price_H=trade_price_of_reference_row; "
    "no_first_trade_after_target; no_look_past_target; "
    "no_mark_price; no_index_price; no_book; no_external_data; "
    "no_future_feature_columns; no_cross_midnight"
)
"""Constant string describing the future-reference policy for hashing."""

DIRECTION_THRESHOLD_POLICY_V001: Final[str] = (
    "forward_direction_H_derived_only_from_forward_log_return_H; "
    "plus_one_if_strictly_positive; zero_if_exactly_zero; "
    "minus_one_if_strictly_negative; null_if_forward_log_return_H_is_null; "
    "strict_sign_threshold_zero_log_return; "
    "no_deadband; no_bp_threshold; no_threshold_optimization; "
    "no_cost_based_threshold_at_v001"
)
"""Constant string describing the direction-threshold policy for hashing."""

NULL_CENSORING_POLICY_V001: Final[str] = (
    "keep_all_feature_rows; per_horizon_independent_right_edge_censoring; "
    "horizon_censored_flag_true_when_target_exceeds_final_source_T; "
    "label_any_censored_flag_true_if_any_horizon_censored; "
    "label_invalid_price_flag_true_if_anchor_or_reference_price_le_zero; "
    "no_forward_fill; no_cross_midnight; no_nan_no_inf_in_outputs"
)
"""Constant string describing the null / censoring policy for hashing."""

DTYPE_POLICY_V001: Final[str] = (
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
        raise LabelSchemaError(f"{label} must be 64-char lowercase hex (got {value!r})")


def _canonical_json(obj: Mapping[str, Any]) -> str:
    """Serialize *obj* with sorted keys, no whitespace, and ASCII escapes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


# ---------------------------------------------------------------------------
# label_config_hash builder
# ---------------------------------------------------------------------------


def build_label_config_hash(
    *,
    source_feature_manifest_sha256: str,
    source_feature_parquet_sha256: str,
    source_feature_successor_state_sha256: str,
    source_phase_4bi_b_gate_report_sha256: str,
) -> str:
    """Return the deterministic ``label_config_hash`` for the v001 schema lock.

    Builds a canonical-JSON object (sorted keys, ASCII, no whitespace)
    containing exactly:

    - ``dataset_family``
    - ``dataset_version``
    - ``label_schema_version``
    - ``label_list``
    - ``support_column_list``
    - ``horizon_list``
    - ``horizon_ms_list``
    - ``anchor_policy``
    - ``future_reference_policy``
    - ``direction_threshold_policy``
    - ``null_censoring_policy``
    - ``dtype_policy``
    - ``source_feature_manifest_sha256``
    - ``source_feature_parquet_sha256``
    - ``source_feature_successor_state_sha256``
    - ``source_phase_4bi_b_gate_report_sha256``

    and returns the lowercase hex SHA256 of its UTF-8 encoding.
    """
    _require_hex64(source_feature_manifest_sha256, label="source_feature_manifest_sha256")
    _require_hex64(source_feature_parquet_sha256, label="source_feature_parquet_sha256")
    _require_hex64(
        source_feature_successor_state_sha256,
        label="source_feature_successor_state_sha256",
    )
    _require_hex64(
        source_phase_4bi_b_gate_report_sha256,
        label="source_phase_4bi_b_gate_report_sha256",
    )
    payload: dict[str, Any] = {
        "dataset_family": LABEL_DATASET_FAMILY_V001,
        "dataset_version": LABEL_DATASET_VERSION_V001,
        "label_schema_version": LABEL_SCHEMA_VERSION_V001,
        "label_list": list(LABEL_NAMES_V001),
        "support_column_list": list(LABEL_SUPPORT_COLUMN_NAMES_V001),
        "horizon_list": list(LABEL_HORIZONS_V001),
        "horizon_ms_list": list(LABEL_HORIZON_MS_V001),
        "anchor_policy": ANCHOR_POLICY_V001,
        "future_reference_policy": FUTURE_REFERENCE_POLICY_V001,
        "direction_threshold_policy": DIRECTION_THRESHOLD_POLICY_V001,
        "null_censoring_policy": NULL_CENSORING_POLICY_V001,
        "dtype_policy": DTYPE_POLICY_V001,
        "source_feature_manifest_sha256": source_feature_manifest_sha256,
        "source_feature_parquet_sha256": source_feature_parquet_sha256,
        "source_feature_successor_state_sha256": source_feature_successor_state_sha256,
        "source_phase_4bi_b_gate_report_sha256": source_phase_4bi_b_gate_report_sha256,
    }
    encoded = _canonical_json(payload).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ---------------------------------------------------------------------------
# Import-time sanity assertions
# ---------------------------------------------------------------------------

assert LABEL_HORIZONS_V001 == ("1s", "5s", "15s", "60s")
assert LABEL_HORIZON_MS_V001 == (1000, 5000, 15000, 60000)
assert len(LABEL_HORIZONS_V001) == len(LABEL_HORIZON_MS_V001) == 4
assert len(LABEL_NAMES_V001) == 8
assert len(LABEL_SUPPORT_COLUMN_NAMES_V001) == 14
assert len(LABEL_LINEAGE_COLUMNS_V001) == 17
assert len(LABEL_SCHEMA_V001) == 39

# Canonical ordering invariants used by tests.
assert LABEL_SCHEMA_V001[0] == "dataset_family"
assert LABEL_SCHEMA_V001[16] == "label_config_hash"
assert LABEL_SCHEMA_V001[17] == "forward_log_return_1s"
assert LABEL_SCHEMA_V001[20] == "forward_log_return_60s"
assert LABEL_SCHEMA_V001[21] == "forward_direction_1s"
assert LABEL_SCHEMA_V001[24] == "forward_direction_60s"
assert LABEL_SCHEMA_V001[25] == "reference_row_index_1s"
assert LABEL_SCHEMA_V001[37] == "label_invalid_price_flag"
assert LABEL_SCHEMA_V001[38] == "label_any_censored_flag"


__all__ = [
    "ANCHOR_POLICY_V001",
    "DIRECTION_THRESHOLD_POLICY_V001",
    "DTYPE_POLICY_V001",
    "FORBIDDEN_LABEL_COLUMN_SUBSTRINGS",
    "FUTURE_REFERENCE_POLICY_V001",
    "LABEL_DATASET_FAMILY_V001",
    "LABEL_DATASET_VERSION_V001",
    "LABEL_HORIZONS_V001",
    "LABEL_HORIZON_MS_V001",
    "LABEL_LINEAGE_COLUMNS_V001",
    "LABEL_NAMES_V001",
    "LABEL_SCHEMA_COLUMNS_V001",
    "LABEL_SCHEMA_V001",
    "LABEL_SCHEMA_VERSION_V001",
    "LABEL_SUPPORT_COLUMN_NAMES_V001",
    "LabelSchemaError",
    "NULL_CENSORING_POLICY_V001",
    "SOURCE_FEATURE_DATASET_FAMILY_V001",
    "SOURCE_FEATURE_DATASET_VERSION_V001",
    "assert_no_forbidden_label_substrings",
    "build_label_config_hash",
]
