"""Phase 4bm-H multi-day v002 aggTrades feature manifest builder.

Builds the JSON-friendly v002 feature manifest for the multi-day
feature family
``microstructure_features_aggtrades_v001`` at ``dataset_version =
"v002"``. The manifest:

- defaults ``research_eligible = false`` and
  ``eligibility_gate_status = "pending"`` (Phase 4bm-H produces local
  Stage-2 feature artefacts only; the future feature-family
  eligibility gate is the only path that may flip those flags in a
  separately authorized future phase);
- carries explicit non-authorization labels for Stage-4, label
  computation, diagnostics, ML, strategy, backtest, acquisition, and
  successor authorization;
- pins all v002 lineage SHAs (v002 derived multi-day index manifest,
  Phase 4bm-D gate report, Phase 4bm-F successor-state JSON, Phase
  4bl-D-R raw multi-day gate report, Phase 4bl-E raw multi-day
  successor-state JSON, v002 raw manifest, v002 acquisition log);
- itemizes every per-day feature Parquet output (path, SHA256, row
  count, sidecar path, sidecar SHA256, paired source per-day Parquet
  SHA256).

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT write any file on its own; the orchestrator in
  :mod:`features_compute_v002` and :mod:`features_io` performs all
  writes;
- never flips ``research_eligible`` to ``True`` and never modifies any
  prior manifest, gate report, or successor-state artefact.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from .features_schema import FEATURE_DATASET_FAMILY
from .features_schema_v002 import (
    CROSS_DAY_LOOKBACK_POLICY_V002,
    CROSS_DAY_TAIL_BUFFER_MS,
    DECIMAL_POLICY_V002,
    FEATURE_DATASET_VERSION_V002,
    FEATURE_NAMES_V002,
    FEATURE_SCHEMA_V002,
    FEATURE_SCHEMA_VERSION_V002,
    FEATURE_WINDOW_LABELS_V002,
    FEATURE_WINDOWS_MS_V002,
    FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002,
    INVALID_WINDOW_POLICY_V002,
    LEAKAGE_POLICY_V002,
    LINEAGE_COLUMNS_V002,
    NULL_POLICY_V002,
    PHASE_4BM_E_OUTCOME_LITERAL,
    SAME_TIMESTAMP_TIE_RULE_V002,
    SOURCE_NORMALIZED_DATASET_FAMILY_V002,
    SOURCE_NORMALIZED_DATASET_VERSION_V002,
    TIMESTAMP_POLICY_V002,
    WINDOW_BOUNDARY_POLICY_V002,
)

REQUIRED_V002_GOVERNANCE_KEYS: tuple[str, ...] = (
    "phase_id",
    "feature_computation",
    "labels",
    "ml",
    "strategy",
    "backtest",
    "acquisition",
    "stop_trigger_domain",
)
"""Required governance label keys at v002 (mirror v001 contract)."""

FORBIDDEN_V002_GOVERNANCE_VALUES: Mapping[str, frozenset[str]] = {
    "labels": frozenset({"allowed"}),
    "ml": frozenset({"allowed"}),
    "strategy": frozenset({"allowed"}),
    "backtest": frozenset({"allowed"}),
    "acquisition": frozenset({"allowed"}),
}
"""Governance label values that must NOT appear at v002."""


REQUIRED_V002_BOUNDARY_CONFIRMATIONS: tuple[str, ...] = (
    "no_labels",
    "no_targets",
    "no_signals",
    "no_ml",
    "no_strategy",
    "no_backtest",
    "no_acquisition",
    "no_network",
    "no_credentials",
    "no_manifest_mutation",
    "no_source_artefact_mutation",
    "no_future_lookahead",
    "no_centered_windows",
    "no_full_day_distribution_normalization",
    "no_split_assignment",
    "no_random_shuffle",
    "no_mcp_or_graphify",
    "phase_4aw_flip_research_eligible_invariant_preserved",
)
"""Required v002 boundary confirmations (extends the v001 11-key set)."""


REQUIRED_V002_NON_AUTHORIZATION_FLAGS: tuple[str, ...] = (
    "stage_4_feature_cleared",
    "label_computation_authorized",
    "diagnostics_authorized",
    "ml_authorized",
    "strategy_authorized",
    "backtest_authorized",
    "acquisition_authorized",
    "successor_authorization_after",
)
"""Required v002 non-authorization flags (all must be ``False``)."""


class FeatureManifestErrorV002(RuntimeError):
    """Raised when a Phase 4bm-H v002 feature manifest input is invalid."""


def build_feature_manifest_v002(
    *,
    symbol: str,
    input_date_start: str,
    input_date_end: str,
    date_count: int,
    expected_event_count: int,
    actual_feature_row_count: int,
    per_day_outputs: Sequence[Mapping[str, Any]],
    feature_dtypes: Mapping[str, str],
    feature_config_hash: str,
    source_normalized_manifest_path: str,
    source_normalized_manifest_sha256: str,
    source_successor_state_path: str,
    source_successor_state_sha256: str,
    source_phase_4bm_d_gate_report_sha256: str,
    source_phase_4bm_f_successor_state_sha256: str,
    source_phase_4bl_d_r_raw_gate_report_sha256: str,
    source_phase_4bl_e_raw_successor_state_sha256: str,
    source_v002_raw_manifest_sha256: str,
    source_v002_acquisition_log_sha256: str,
    code_commit_sha: str = "unknown",
    created_at_unix_ms: int = 0,
    extra_governance_labels: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Construct the Phase 4bm-H v002 feature manifest as a JSON-friendly dict.

    Parameters are validated locally; the orchestrator is responsible
    for atomic write via :mod:`features_io`. The manifest defaults
    ``research_eligible = False`` and
    ``eligibility_gate_status = "pending"``; those flags can only be
    flipped by a separately authorized future feature-family
    eligibility gate phase.
    """
    if not isinstance(symbol, str) or not symbol or symbol != symbol.upper():
        raise FeatureManifestErrorV002("symbol must be uppercase non-empty string")
    for label, val in (("input_date_start", input_date_start), ("input_date_end", input_date_end)):
        if (
            not isinstance(val, str)
            or len(val) != 10
            or val[4] != "-"
            or val[7] != "-"
        ):
            raise FeatureManifestErrorV002(f"{label} must be YYYY-MM-DD")
    if not isinstance(date_count, int) or date_count <= 0:
        raise FeatureManifestErrorV002("date_count must be a positive int")
    if (
        not isinstance(expected_event_count, int)
        or expected_event_count < 0
    ):
        raise FeatureManifestErrorV002("expected_event_count must be a non-negative int")
    if (
        not isinstance(actual_feature_row_count, int)
        or actual_feature_row_count < 0
    ):
        raise FeatureManifestErrorV002(
            "actual_feature_row_count must be a non-negative int"
        )
    if len(per_day_outputs) != date_count:
        raise FeatureManifestErrorV002(
            f"per_day_outputs length ({len(per_day_outputs)}) != date_count ({date_count})"
        )
    for sha_label, sha_val in (
        ("feature_config_hash", feature_config_hash),
        ("source_normalized_manifest_sha256", source_normalized_manifest_sha256),
        ("source_successor_state_sha256", source_successor_state_sha256),
        ("source_phase_4bm_d_gate_report_sha256", source_phase_4bm_d_gate_report_sha256),
        ("source_phase_4bm_f_successor_state_sha256", source_phase_4bm_f_successor_state_sha256),
        (
            "source_phase_4bl_d_r_raw_gate_report_sha256",
            source_phase_4bl_d_r_raw_gate_report_sha256,
        ),
        (
            "source_phase_4bl_e_raw_successor_state_sha256",
            source_phase_4bl_e_raw_successor_state_sha256,
        ),
        ("source_v002_raw_manifest_sha256", source_v002_raw_manifest_sha256),
        ("source_v002_acquisition_log_sha256", source_v002_acquisition_log_sha256),
    ):
        if not isinstance(sha_val, str) or len(sha_val) != 64:
            raise FeatureManifestErrorV002(
                f"{sha_label} must be a 64-char hex string"
            )
    if tuple(feature_dtypes.keys()) != FEATURE_SCHEMA_V002:
        raise FeatureManifestErrorV002(
            "feature_dtypes keys must equal FEATURE_SCHEMA_V002 in canonical order"
        )

    per_day_normalized: list[dict[str, Any]] = list(_validate_per_day_outputs(per_day_outputs))

    governance_labels: dict[str, str] = {
        "phase_id": "4bm-H",
        "feature_computation": "allowed_by_phase_4bm_h",
        "labels": "forbidden",
        "ml": "forbidden",
        "strategy": "forbidden",
        "backtest": "forbidden",
        "acquisition": "unauthorized",
        "stop_trigger_domain": "trade_price_backtest_candidate",
    }
    if extra_governance_labels:
        for k, v in extra_governance_labels.items():
            if k in governance_labels:
                raise FeatureManifestErrorV002(
                    f"extra_governance_labels must not override locked key {k!r}"
                )
            if not isinstance(k, str) or not isinstance(v, str):
                raise FeatureManifestErrorV002(
                    "extra_governance_labels must be Mapping[str, str]"
                )
            governance_labels[k] = v

    missing = [k for k in REQUIRED_V002_GOVERNANCE_KEYS if k not in governance_labels]
    if missing:
        raise FeatureManifestErrorV002(
            f"governance_labels missing required keys: {missing}"
        )
    for key, forbidden_values in FORBIDDEN_V002_GOVERNANCE_VALUES.items():
        if governance_labels.get(key) in forbidden_values:
            raise FeatureManifestErrorV002(
                f"governance_labels[{key!r}] must not be in {sorted(forbidden_values)}"
            )

    boundary_confirmations: dict[str, bool] = {
        key: True for key in REQUIRED_V002_BOUNDARY_CONFIRMATIONS
    }
    non_authorization_flags: dict[str, bool] = {
        key: False for key in REQUIRED_V002_NON_AUTHORIZATION_FLAGS
    }

    manifest: dict[str, Any] = {
        "dataset_family": FEATURE_DATASET_FAMILY,
        "dataset_version": FEATURE_DATASET_VERSION_V002,
        "feature_schema_version": FEATURE_SCHEMA_VERSION_V002,
        "source_dataset_family": SOURCE_NORMALIZED_DATASET_FAMILY_V002,
        "source_dataset_version": SOURCE_NORMALIZED_DATASET_VERSION_V002,
        "source_normalized_manifest_path": source_normalized_manifest_path,
        "source_normalized_manifest_sha256": source_normalized_manifest_sha256,
        "source_successor_state_path": source_successor_state_path,
        "source_successor_state_sha256": source_successor_state_sha256,
        "source_phase_4bm_d_gate_report_sha256": source_phase_4bm_d_gate_report_sha256,
        "source_phase_4bm_e_outcome": PHASE_4BM_E_OUTCOME_LITERAL,
        "source_phase_4bm_f_successor_state_sha256": source_phase_4bm_f_successor_state_sha256,
        "source_phase_4bl_d_r_raw_gate_report_sha256": (
            source_phase_4bl_d_r_raw_gate_report_sha256
        ),
        "source_phase_4bl_e_raw_successor_state_sha256": (
            source_phase_4bl_e_raw_successor_state_sha256
        ),
        "source_v002_raw_manifest_sha256": source_v002_raw_manifest_sha256,
        "source_v002_acquisition_log_sha256": source_v002_acquisition_log_sha256,
        "input_date_start": input_date_start,
        "input_date_end": input_date_end,
        "date_count": int(date_count),
        "symbol": symbol,
        "expected_event_count": int(expected_event_count),
        "actual_feature_row_count": int(actual_feature_row_count),
        "feature_column_names": list(FEATURE_SCHEMA_V002),
        "lineage_column_names": list(LINEAGE_COLUMNS_V002),
        "computed_feature_column_names": list(FEATURE_NAMES_V002),
        "feature_dtypes": {k: feature_dtypes[k] for k in FEATURE_SCHEMA_V002},
        "feature_config_hash": feature_config_hash,
        "feature_windows_ms": list(FEATURE_WINDOWS_MS_V002),
        "feature_window_labels": list(FEATURE_WINDOW_LABELS_V002),
        "window_boundary_policy": WINDOW_BOUNDARY_POLICY_V002,
        "invalid_window_policy": dict(INVALID_WINDOW_POLICY_V002),
        "timestamp_policy": TIMESTAMP_POLICY_V002,
        "leakage_policy": LEAKAGE_POLICY_V002,
        "same_timestamp_tie_rule": SAME_TIMESTAMP_TIE_RULE_V002,
        "cross_day_lookback_policy": CROSS_DAY_LOOKBACK_POLICY_V002,
        "cross_day_tail_buffer_ms": int(CROSS_DAY_TAIL_BUFFER_MS),
        "decimal_policy": dict(DECIMAL_POLICY_V002),
        "null_policy": dict(NULL_POLICY_V002),
        "forbidden_substring_detector_tokens": list(
            FORBIDDEN_FEATURE_COLUMN_SUBSTRINGS_V002
        ),
        "per_day_outputs": per_day_normalized,
        "governance_labels": governance_labels,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        **non_authorization_flags,
        "no_network_io": True,
        "no_credentials": True,
        "no_mcp_or_graphify": True,
        "no_manifest_mutation": True,
        "phase_4aw_flip_research_eligible_invariant_preserved": True,
        "code_commit_sha": code_commit_sha,
        "created_at_unix_ms": int(created_at_unix_ms),
        "boundary_confirmations": boundary_confirmations,
    }
    return manifest


def _validate_per_day_outputs(
    raw: Iterable[Mapping[str, Any]],
) -> Iterable[dict[str, Any]]:
    """Validate and normalize per_day_outputs entries to plain dicts."""
    required_keys = (
        "utc_date",
        "feature_parquet_path",
        "feature_parquet_sha256",
        "feature_parquet_size_bytes",
        "row_count",
        "feature_sidecar_path",
        "feature_sidecar_sha256",
        "source_normalized_parquet_per_day_sha256",
    )
    for entry in raw:
        if not isinstance(entry, Mapping):
            raise FeatureManifestErrorV002(
                "per_day_outputs entries must be Mapping[str, Any]"
            )
        missing = [k for k in required_keys if k not in entry]
        if missing:
            raise FeatureManifestErrorV002(
                f"per_day_outputs entry missing keys: {missing}"
            )
        for sha_key in (
            "feature_parquet_sha256",
            "feature_sidecar_sha256",
            "source_normalized_parquet_per_day_sha256",
        ):
            v = entry[sha_key]
            if not isinstance(v, str) or len(v) != 64:
                raise FeatureManifestErrorV002(
                    f"per_day_outputs[{sha_key}] must be 64-char hex"
                )
        if (
            not isinstance(entry["row_count"], int)
            or entry["row_count"] < 0
        ):
            raise FeatureManifestErrorV002(
                "per_day_outputs row_count must be a non-negative int"
            )
        if (
            not isinstance(entry["feature_parquet_size_bytes"], int)
            or entry["feature_parquet_size_bytes"] < 0
        ):
            raise FeatureManifestErrorV002(
                "per_day_outputs feature_parquet_size_bytes must be non-negative int"
            )
        utc_date = entry["utc_date"]
        if (
            not isinstance(utc_date, str)
            or len(utc_date) != 10
            or utc_date[4] != "-"
            or utc_date[7] != "-"
        ):
            raise FeatureManifestErrorV002(
                f"per_day_outputs utc_date must be YYYY-MM-DD; got {utc_date!r}"
            )
        yield dict(entry)


def feature_dtypes_v002() -> dict[str, str]:
    """Return the canonical dtype map for every v002 feature column.

    The dtype names match the pyarrow schema constructed by
    :func:`compute_aggtrades_features_v002`.
    """
    int64_cols = {
        "agg_trade_id",
        "row_index",
        "feature_timestamp_ms",
        "source_transact_time_ms",
        "milliseconds_since_day_start",
    }
    int8_cols = {"utc_hour", "utc_minute"}
    bool_cols = {"invalid_window_flag", "rolling_missing_window_flag"}
    int64_count_prefixes = (
        "rolling_aggtrade_count_",
        "rolling_aggressive_buy_count_",
        "rolling_aggressive_sell_count_",
    )
    nullable_float_prefixes = (
        "rolling_aggressive_flow_ratio_",
        "rolling_log_return_past_window_",
    )
    non_null_decimal_prefixes = (
        "rolling_quantity_sum_",
        "rolling_aggressive_buy_quantity_",
        "rolling_aggressive_sell_quantity_",
        "rolling_aggressive_quantity_imbalance_",
    )
    nullable_decimal_prefixes = ("rolling_quantity_mean_",)

    out: dict[str, str] = {}
    for col in FEATURE_SCHEMA_V002:
        if col in int64_cols:
            out[col] = "int64"
        elif col in int8_cols:
            out[col] = "int8"
        elif col in bool_cols:
            out[col] = "bool"
        elif col.startswith(int64_count_prefixes):
            out[col] = "int64"
        elif col.startswith(nullable_float_prefixes):
            out[col] = "float64_nullable"
        elif col.startswith(non_null_decimal_prefixes):
            out[col] = "decimal_string"
        elif col.startswith(nullable_decimal_prefixes):
            out[col] = "decimal_string_nullable"
        else:
            out[col] = "string"
    return out


__all__ = [
    "FORBIDDEN_V002_GOVERNANCE_VALUES",
    "FeatureManifestErrorV002",
    "REQUIRED_V002_BOUNDARY_CONFIRMATIONS",
    "REQUIRED_V002_GOVERNANCE_KEYS",
    "REQUIRED_V002_NON_AUTHORIZATION_FLAGS",
    "build_feature_manifest_v002",
    "feature_dtypes_v002",
]
