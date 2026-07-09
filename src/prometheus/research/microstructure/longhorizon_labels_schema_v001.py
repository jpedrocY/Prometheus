"""Phase 4bn-AN longer-horizon aggTrades label schema (new sibling family).

Declarative schema constants for the **new sibling** longer-horizon label
family recommended by Phase 4bn-AM and authorised by the Phase 4bn-AN build
prompt:

``microstructure_labels_longhorizon_aggtrades_v001``

This family is a *sibling* of the frozen short-horizon v002 family
``microstructure_labels_aggtrades_v001`` (horizons ``1s/5s/15s/60s``). It
reuses the exact v002 label schema *pattern* — the per-horizon
``forward_log_return_H`` / ``forward_direction_H`` columns, the per-horizon
``reference_row_index_H`` / ``reference_timestamp_ms_H`` /
``horizon_censored_flag_H`` support columns, the two global support flags, the
17 lineage columns + ``label_config_hash``, the strict-sign direction policy,
and the per-horizon envelope-terminal censoring policy — applied to the **new
horizon set** ``5m / 30m / 1h``. It does **not** mutate the frozen v002 family
and imports the frozen v002 forbidden-substring guard and lineage columns
verbatim so the two families cannot drift.

This module performs **no I/O**, computes **no** label, reads **no** data,
trains **nothing**, and authorises **no** successor. It is pure constants +
validators + a deterministic ``label_config_hash`` builder.

Direction policy (strict-sign only): ``forward_direction_H`` is ``+1`` when
``forward_log_return_H > 0``, ``0`` when ``== 0``, ``-1`` when ``< 0``, and
``null`` when ``forward_log_return_H`` is null / censored / invalid. No
deadband, no bp threshold, no cost-based / learned / optimised threshold. The
locked cost reference (8 bps/side · 16 bps round-trip) is **descriptive only**
and never enters the target.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Final

from .labels_schema_v002 import (
    FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002,
    LABEL_LINEAGE_COLUMNS_V002,
    LabelSchemaErrorV002,
    assert_no_forbidden_label_substrings_v002,
)

# ---------------------------------------------------------------------------
# Identity / version constants (new sibling family)
# ---------------------------------------------------------------------------

LONGHORIZON_LABEL_DATASET_FAMILY: Final = "microstructure_labels_longhorizon_aggtrades_v001"
LONGHORIZON_LABEL_DATASET_VERSION: Final = "v002"
LONGHORIZON_LABEL_SCHEMA_VERSION: Final = "v001"
LONGHORIZON_SEGMENT_LABEL: Final = "pre_v002_segment"
LONGHORIZON_CONTRACT_NAME: Final = (
    "microstructure_longhorizon_label_aggtrades_pre_v002_contract_v001"
)

# The frozen short-horizon sibling this family parallels but never mutates.
FROZEN_SHORT_HORIZON_FAMILY: Final = "microstructure_labels_aggtrades_v001"

SOURCE_FEATURE_DATASET_FAMILY: Final = "microstructure_features_aggtrades_v001"
SOURCE_FEATURE_DATASET_VERSION: Final = "v002"
SOURCE_NORMALIZED_DATASET_FAMILY: Final = "microstructure_normalized_aggtrades_v001"
SOURCE_NORMALIZED_DATASET_VERSION: Final = "v002"

LONGHORIZON_SYMBOL: Final = "BTCUSDT"

# ---------------------------------------------------------------------------
# Horizon constants (the new longer-horizon set; distinct from 1s/5s/15s/60s)
# ---------------------------------------------------------------------------

LONGHORIZON_HORIZONS: Final[tuple[str, str, str]] = ("5m", "30m", "1h")
"""Longer-horizon labels in canonical ascending order; 5m is the lead horizon."""

LONGHORIZON_HORIZON_MS: Final[tuple[int, int, int]] = (300_000, 1_800_000, 3_600_000)
"""Horizon offsets in milliseconds paired 1:1 with :data:`LONGHORIZON_HORIZONS`."""

LONGHORIZON_LEAD: Final = "5m"
LONGHORIZON_SECONDARY: Final[tuple[str, str]] = ("30m", "1h")

# Every longer horizon (max 1h = 3_600_000 ms) is strictly less than one UTC day
# (86_400_000 ms), so the frozen v002 kernel's current-day-or-next-day
# cross-day reference resolution remains valid unchanged for this family.
UTC_DAY_MS: Final = 86_400_000

# ---------------------------------------------------------------------------
# Label and support column names (same pattern as v002, new horizons)
# ---------------------------------------------------------------------------


def _build_label_names() -> tuple[str, ...]:
    names: list[str] = []
    for label in LONGHORIZON_HORIZONS:
        names.append(f"forward_log_return_{label}")
    for label in LONGHORIZON_HORIZONS:
        names.append(f"forward_direction_{label}")
    return tuple(names)


LONGHORIZON_LABEL_NAMES: Final[tuple[str, ...]] = _build_label_names()
"""The 6 label column names (regression then classification)."""


def _build_support_column_names() -> tuple[str, ...]:
    names: list[str] = []
    for label in LONGHORIZON_HORIZONS:
        names.append(f"reference_row_index_{label}")
        names.append(f"reference_timestamp_ms_{label}")
        names.append(f"horizon_censored_flag_{label}")
    names.append("label_invalid_price_flag")
    names.append("label_any_censored_flag")
    return tuple(names)


LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES: Final[tuple[str, ...]] = (
    _build_support_column_names()
)
"""The 11 support column names in canonical order."""

# Lineage columns reused verbatim from the frozen v002 schema (identical set).
LONGHORIZON_LABEL_LINEAGE_COLUMNS: Final[tuple[str, ...]] = tuple(
    LABEL_LINEAGE_COLUMNS_V002
)

# ---------------------------------------------------------------------------
# Full canonical schema (lineage + label_config_hash + labels + support)
# ---------------------------------------------------------------------------

LONGHORIZON_LABEL_SCHEMA: Final[tuple[str, ...]] = (
    LONGHORIZON_LABEL_LINEAGE_COLUMNS
    + ("label_config_hash",)
    + LONGHORIZON_LABEL_NAMES
    + LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES
)
"""All columns in canonical order (17 lineage + 1 config-hash + 6 label + 11 support)."""

# ---------------------------------------------------------------------------
# Policy descriptors (constant strings used in the canonical-JSON config hash)
# ---------------------------------------------------------------------------

LONGHORIZON_ANCHOR_POLICY: Final[str] = (
    "anchor_row=feature_row_R; anchor_timestamp=feature_timestamp_ms; "
    "anchor_source_timestamp=source_transact_time_ms; "
    "anchor_price=trade_price_of_normalized_aggtrade_row_identified_by_"
    "(agg_trade_id,row_index)_inside_anchor_per_day_normalized_parquet; "
    "no_mark_price; no_index_price; no_bid_or_ask; "
    "no_book; no_external_data; no_future_feature_values"
)

# Future-reference policy: identical structure to the v002 policy but the
# envelope-terminal clause is pinned to the pre-v002 segment terminal.
LONGHORIZON_FUTURE_REFERENCE_POLICY: Final[str] = (
    "target_timestamp_ms=feature_timestamp_ms+H_ms; "
    "envelope_terminal_unix_ms="
    "max_source_transact_time_ms_across_pre_v002_segment_2024-03-01_to_2024-11-30; "
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

LONGHORIZON_DIRECTION_THRESHOLD_POLICY: Final[str] = (
    "forward_direction_H_derived_only_from_forward_log_return_H; "
    "plus_one_if_strictly_positive; zero_if_exactly_zero; "
    "minus_one_if_strictly_negative; null_if_forward_log_return_H_is_null; "
    "strict_sign_threshold_zero_log_return; "
    "no_deadband; no_bp_threshold; no_threshold_optimization; "
    "no_cost_based_threshold; no_learned_threshold; no_magnitude_label; "
    "no_neutral_band; cost_reference_8bps_per_side_16bps_round_trip_descriptive_only"
)

LONGHORIZON_NULL_CENSORING_POLICY: Final[str] = (
    "keep_all_feature_rows; per_horizon_independent_envelope_terminal_censoring; "
    "horizon_censored_flag_true_when_target_exceeds_envelope_terminal_unix_ms; "
    "no_per_day_censoring; cross_day_reference_allowed_within_envelope; "
    "label_any_censored_flag_true_if_any_horizon_censored; "
    "label_invalid_price_flag_true_if_anchor_or_reference_price_le_zero; "
    "no_forward_fill_beyond_envelope; no_cross_envelope_stitching; "
    "no_nan_no_inf_in_outputs"
)

LONGHORIZON_DTYPE_POLICY: Final[str] = (
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

# Locked descriptive cost reference (never enters the target).
LOCKED_COST_BPS_PER_SIDE: Final[float] = 8.0
LOCKED_ROUND_TRIP_COST_BPS: Final[float] = 16.0

# Non-authorization posture (all False). Threaded into the build proof.
NON_AUTHORIZATION_FLAGS: Final[dict[str, bool]] = {
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
# Validators + deterministic label_config_hash builder
# ---------------------------------------------------------------------------

_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def _require_hex64(value: str, *, label: str) -> None:
    if not isinstance(value, str) or not _HEX64_RE.match(value):
        raise LabelSchemaErrorV002(
            f"{label} must be 64-char lowercase hex (got {value!r})"
        )


LONGHORIZON_LABEL_CONFIG_HASH_INPUT_FIELDS: Final[tuple[str, ...]] = (
    "dataset_family",
    "dataset_version",
    "label_schema_version",
    "segment_label",
    "label_list",
    "support_column_list",
    "lineage_column_list",
    "horizon_list",
    "horizon_ms_list",
    "anchor_policy",
    "future_reference_policy_pre_v002_segment",
    "direction_threshold_policy",
    "null_censoring_policy",
    "dtype_policy",
    "source_feature_manifest_sha256",
    "source_feature_layer_gate_report_sha256",
    "source_normalized_manifest_sha256",
    "source_normalized_layer_gate_report_sha256",
    "source_raw_manifest_sha256",
    "feature_config_hash",
)


def build_longhorizon_label_config_hash(
    *,
    source_feature_manifest_sha256: str,
    source_feature_layer_gate_report_sha256: str,
    source_normalized_manifest_sha256: str,
    source_normalized_layer_gate_report_sha256: str,
    source_raw_manifest_sha256: str,
    feature_config_hash: str,
) -> str:
    """Return the deterministic sibling ``label_config_hash`` for this family.

    Canonical-JSON (sorted keys, ASCII, no whitespace) of the sibling family
    identity + policy strings + horizon set + the pre-v002 source-binding
    witnesses. Distinct from the v002 hash because the family name, horizon
    set, and future-reference envelope clause differ.
    """
    for name, val in (
        ("source_feature_manifest_sha256", source_feature_manifest_sha256),
        (
            "source_feature_layer_gate_report_sha256",
            source_feature_layer_gate_report_sha256,
        ),
        ("source_normalized_manifest_sha256", source_normalized_manifest_sha256),
        (
            "source_normalized_layer_gate_report_sha256",
            source_normalized_layer_gate_report_sha256,
        ),
        ("source_raw_manifest_sha256", source_raw_manifest_sha256),
        ("feature_config_hash", feature_config_hash),
    ):
        _require_hex64(val, label=name)
    payload: dict[str, Any] = {
        "dataset_family": LONGHORIZON_LABEL_DATASET_FAMILY,
        "dataset_version": LONGHORIZON_LABEL_DATASET_VERSION,
        "label_schema_version": LONGHORIZON_LABEL_SCHEMA_VERSION,
        "segment_label": LONGHORIZON_SEGMENT_LABEL,
        "label_list": list(LONGHORIZON_LABEL_NAMES),
        "support_column_list": list(LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES),
        "lineage_column_list": list(LONGHORIZON_LABEL_LINEAGE_COLUMNS),
        "horizon_list": list(LONGHORIZON_HORIZONS),
        "horizon_ms_list": list(LONGHORIZON_HORIZON_MS),
        "anchor_policy": LONGHORIZON_ANCHOR_POLICY,
        "future_reference_policy_pre_v002_segment": LONGHORIZON_FUTURE_REFERENCE_POLICY,
        "direction_threshold_policy": LONGHORIZON_DIRECTION_THRESHOLD_POLICY,
        "null_censoring_policy": LONGHORIZON_NULL_CENSORING_POLICY,
        "dtype_policy": LONGHORIZON_DTYPE_POLICY,
        "source_feature_manifest_sha256": source_feature_manifest_sha256,
        "source_feature_layer_gate_report_sha256": (
            source_feature_layer_gate_report_sha256
        ),
        "source_normalized_manifest_sha256": source_normalized_manifest_sha256,
        "source_normalized_layer_gate_report_sha256": (
            source_normalized_layer_gate_report_sha256
        ),
        "source_raw_manifest_sha256": source_raw_manifest_sha256,
        "feature_config_hash": feature_config_hash,
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ---------------------------------------------------------------------------
# Import-time sanity assertions (constant-only; no I/O)
# ---------------------------------------------------------------------------

assert LONGHORIZON_HORIZONS == ("5m", "30m", "1h")
assert LONGHORIZON_HORIZON_MS == (300_000, 1_800_000, 3_600_000)
assert len(LONGHORIZON_HORIZONS) == len(LONGHORIZON_HORIZON_MS) == 3
assert all(ms < UTC_DAY_MS for ms in LONGHORIZON_HORIZON_MS)
assert LONGHORIZON_LEAD == "5m"
assert LONGHORIZON_SECONDARY == ("30m", "1h")
assert len(LONGHORIZON_LABEL_NAMES) == 6
assert len(LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES) == 11
assert len(LONGHORIZON_LABEL_LINEAGE_COLUMNS) == 17
assert len(LONGHORIZON_LABEL_SCHEMA) == 17 + 1 + 6 + 11
assert len(set(LONGHORIZON_LABEL_SCHEMA)) == len(LONGHORIZON_LABEL_SCHEMA)
# Runtime tripwire: the sibling family name must differ from the frozen family.
# ``str(...)`` keeps this a genuine runtime check without a static-literal
# comparison-overlap warning.
assert str(LONGHORIZON_LABEL_DATASET_FAMILY) != str(FROZEN_SHORT_HORIZON_FAMILY)
# The sibling family must never carry a forbidden column-name substring.
assert_no_forbidden_label_substrings_v002(LONGHORIZON_LABEL_SCHEMA)
assert all(v is False for v in NON_AUTHORIZATION_FLAGS.values())
# No sibling horizon token may collide with a frozen v002 horizon token.
for _h in LONGHORIZON_HORIZONS:
    assert _h not in ("1s", "5s", "15s", "60s")


__all__ = [
    "FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002",
    "FROZEN_SHORT_HORIZON_FAMILY",
    "LOCKED_COST_BPS_PER_SIDE",
    "LOCKED_ROUND_TRIP_COST_BPS",
    "LONGHORIZON_ANCHOR_POLICY",
    "LONGHORIZON_CONTRACT_NAME",
    "LONGHORIZON_DIRECTION_THRESHOLD_POLICY",
    "LONGHORIZON_DTYPE_POLICY",
    "LONGHORIZON_FUTURE_REFERENCE_POLICY",
    "LONGHORIZON_HORIZONS",
    "LONGHORIZON_HORIZON_MS",
    "LONGHORIZON_LABEL_CONFIG_HASH_INPUT_FIELDS",
    "LONGHORIZON_LABEL_DATASET_FAMILY",
    "LONGHORIZON_LABEL_DATASET_VERSION",
    "LONGHORIZON_LABEL_LINEAGE_COLUMNS",
    "LONGHORIZON_LABEL_NAMES",
    "LONGHORIZON_LABEL_SCHEMA",
    "LONGHORIZON_LABEL_SCHEMA_VERSION",
    "LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES",
    "LONGHORIZON_LEAD",
    "LONGHORIZON_NULL_CENSORING_POLICY",
    "LONGHORIZON_SECONDARY",
    "LONGHORIZON_SEGMENT_LABEL",
    "LONGHORIZON_SYMBOL",
    "NON_AUTHORIZATION_FLAGS",
    "SOURCE_FEATURE_DATASET_FAMILY",
    "SOURCE_FEATURE_DATASET_VERSION",
    "SOURCE_NORMALIZED_DATASET_FAMILY",
    "SOURCE_NORMALIZED_DATASET_VERSION",
    "build_longhorizon_label_config_hash",
]
