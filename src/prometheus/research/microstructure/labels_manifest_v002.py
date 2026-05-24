"""Phase 4bm-O multi-day v002 aggTrades label manifest builder.

Builds the JSON-friendly v002 label manifest for the multi-day label
family ``microstructure_labels_aggtrades_v001`` at
``dataset_version = "v002"``. The manifest:

- defaults ``research_eligible = false`` and
  ``eligibility_gate_status = "pending"`` (Phase 4bm-O produces local
  gitignored label artefacts only; the future label-family
  eligibility gate is the only path that may flip those flags in a
  separately authorized future phase);
- carries explicit non-authorization labels for label-family research-
  use, ML, strategy, backtest, acquisition, paper-shadow-live,
  deployment, exchange-write, and successor authorization;
- pins all v002 lineage SHAs (v002 feature manifest + sidecar, Phase
  4bm-L successor-state + sidecar, Phase 4bm-J gate report + sidecar,
  v002 derived multi-day index manifest + sidecar, Phase 4bm-F
  successor-state, Phase 4bm-D gate report, v002 raw manifest, v002
  acquisition log, Phase 4bl-E raw successor-state, Phase 4bl-D-R raw
  gate report);
- itemises every per-day label Parquet output (path, SHA256, sidecar
  path, sidecar SHA256, byte size, row count, per-horizon censored
  counts, invalid-price row count, paired source feature parquet
  SHA256).

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT write any file on its own; the orchestrator in
  :mod:`scripts.phase4bm_o_compute_multiday_labels` performs all
  writes via :mod:`labels_io`;
- never flips ``research_eligible`` to ``True`` and never modifies any
  prior manifest, gate report, or successor-state artefact.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from .labels_schema_v002 import (
    ANCHOR_POLICY_V002,
    DIRECTION_THRESHOLD_POLICY_V002,
    DTYPE_POLICY_V002,
    FUTURE_REFERENCE_POLICY_V002,
    LABEL_DATASET_FAMILY_V002,
    LABEL_DATASET_VERSION_V002,
    LABEL_HORIZON_MS_V002,
    LABEL_HORIZONS_V002,
    LABEL_LINEAGE_COLUMNS_V002,
    LABEL_NAMES_V002,
    LABEL_SCHEMA_V002,
    LABEL_SCHEMA_VERSION_V002,
    LABEL_SUPPORT_COLUMN_NAMES_V002,
    LABEL_SYMBOL_LIST_V002,
    LABEL_SYMBOL_V002,
    NULL_CENSORING_POLICY_V002,
    SOURCE_FEATURE_DATASET_FAMILY_V002,
    SOURCE_FEATURE_DATASET_VERSION_V002,
)

REQUIRED_LABEL_GOVERNANCE_KEYS_V002: tuple[str, ...] = (
    "phase_id",
    "labels",
    "targets",
    "ml",
    "strategy",
    "backtest",
    "acquisition",
    "paper_shadow_live",
    "deployment",
    "exchange_write",
)
"""Required governance label keys at v002 (mirror v001 contract)."""

FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002: Mapping[str, frozenset[str]] = {
    "ml": frozenset({"allowed"}),
    "strategy": frozenset({"allowed"}),
    "backtest": frozenset({"allowed"}),
    "acquisition": frozenset({"allowed"}),
    "paper_shadow_live": frozenset({"allowed"}),
    "deployment": frozenset({"allowed"}),
    "exchange_write": frozenset({"allowed"}),
}
"""Governance label values that must NOT appear at v002."""

REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS_V002: tuple[str, ...] = (
    "no_ml",
    "no_strategy",
    "no_backtest",
    "no_acquisition",
    "no_network",
    "no_credentials",
    "no_mcp_or_graphify",
    "no_feature_manifest_mutation",
    "no_feature_parquet_mutation",
    "no_feature_successor_state_mutation",
    "no_feature_gate_report_mutation",
    "no_normalized_manifest_mutation",
    "no_raw_manifest_mutation",
    "no_label_gate_report",
    "no_label_successor_state",
    "no_successor_authorization",
    "phase_4aw_flip_research_eligible_invariant_preserved",
)
"""Required v002 label boundary confirmations."""


_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


class LabelManifestErrorV002(RuntimeError):
    """Raised when a Phase 4bm-O v002 label manifest input is invalid."""


def _validate_per_day_outputs(
    raw: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Validate and normalize per_day_outputs entries to plain dicts."""
    required_keys = (
        "utc_date",
        "path",
        "sha256",
        "sidecar_path",
        "sidecar_sha256",
        "byte_size",
        "row_count",
        "per_horizon_censored_counts",
        "invalid_price_row_count",
        "source_feature_parquet_sha256",
    )
    out: list[dict[str, Any]] = []
    for entry in raw:
        if not isinstance(entry, Mapping):
            raise LabelManifestErrorV002(
                "per_day_outputs entries must be Mapping[str, Any]"
            )
        missing = [k for k in required_keys if k not in entry]
        if missing:
            raise LabelManifestErrorV002(
                f"per_day_outputs entry missing keys: {missing}"
            )
        for sha_key in (
            "sha256",
            "sidecar_sha256",
            "source_feature_parquet_sha256",
        ):
            v = entry[sha_key]
            if not isinstance(v, str) or not _HEX64_RE.match(v):
                raise LabelManifestErrorV002(
                    f"per_day_outputs[{sha_key}] must be 64-char lowercase hex"
                )
        if not isinstance(entry["row_count"], int) or entry["row_count"] < 0:
            raise LabelManifestErrorV002(
                "per_day_outputs row_count must be a non-negative int"
            )
        if not isinstance(entry["byte_size"], int) or entry["byte_size"] < 0:
            raise LabelManifestErrorV002(
                "per_day_outputs byte_size must be a non-negative int"
            )
        if (
            not isinstance(entry["invalid_price_row_count"], int)
            or entry["invalid_price_row_count"] < 0
        ):
            raise LabelManifestErrorV002(
                "per_day_outputs invalid_price_row_count must be a non-negative int"
            )
        per_horizon = entry["per_horizon_censored_counts"]
        if not isinstance(per_horizon, Mapping):
            raise LabelManifestErrorV002(
                "per_day_outputs per_horizon_censored_counts must be Mapping[str, int]"
            )
        if set(per_horizon.keys()) != set(LABEL_HORIZONS_V002):
            raise LabelManifestErrorV002(
                "per_day_outputs per_horizon_censored_counts keys must equal "
                "LABEL_HORIZONS_V002"
            )
        for k, v in per_horizon.items():
            if not isinstance(v, int) or v < 0:
                raise LabelManifestErrorV002(
                    f"per_day_outputs per_horizon_censored_counts[{k!r}] must be "
                    "a non-negative int"
                )
        utc_date = entry["utc_date"]
        if (
            not isinstance(utc_date, str)
            or len(utc_date) != 10
            or utc_date[4] != "-"
            or utc_date[7] != "-"
        ):
            raise LabelManifestErrorV002(
                f"per_day_outputs utc_date must be YYYY-MM-DD; got {utc_date!r}"
            )
        out.append(
            {
                "utc_date": utc_date,
                "path": str(entry["path"]),
                "sha256": entry["sha256"],
                "sidecar_path": str(entry["sidecar_path"]),
                "sidecar_sha256": entry["sidecar_sha256"],
                "byte_size": int(entry["byte_size"]),
                "row_count": int(entry["row_count"]),
                "per_horizon_censored_counts": {
                    h: int(per_horizon[h]) for h in LABEL_HORIZONS_V002
                },
                "invalid_price_row_count": int(entry["invalid_price_row_count"]),
                "source_feature_parquet_sha256": entry["source_feature_parquet_sha256"],
            }
        )
    return out


def build_label_manifest_v002(
    *,
    symbol: str,
    utc_date_start: str,
    utc_date_end: str,
    date_count: int,
    row_count: int,
    per_day_outputs: Sequence[Mapping[str, Any]],
    label_config_hash: str,
    feature_config_hash: str,
    envelope_terminal_unix_ms: int,
    invalid_price_row_count: int,
    censored_per_horizon: Mapping[str, int],
    source_feature_manifest_sha256: str,
    source_feature_manifest_sidecar_sha256: str,
    source_feature_successor_state_sha256: str,
    source_feature_successor_state_sidecar_sha256: str,
    source_phase_4bm_j_gate_report_sha256: str,
    source_phase_4bm_j_gate_sidecar_sha256: str,
    source_normalized_manifest_sha256: str,
    source_normalized_manifest_sidecar_sha256: str,
    source_phase_4bm_f_derived_successor_state_sha256: str,
    source_phase_4bm_d_derived_gate_report_sha256: str,
    source_raw_manifest_sha256: str,
    source_acquisition_log_sha256: str,
    source_phase_4bl_e_raw_successor_state_sha256: str,
    source_phase_4bl_d_r_raw_gate_report_sha256: str,
    code_commit_sha: str = "unknown",
    created_at_unix_ms: int = 0,
    extra_governance_labels: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Construct the Phase 4bm-O v002 label manifest as a JSON-friendly dict."""
    if not isinstance(symbol, str) or not symbol or symbol != symbol.upper():
        raise LabelManifestErrorV002("symbol must be uppercase non-empty string")
    if symbol != LABEL_SYMBOL_V002:
        raise LabelManifestErrorV002(
            f"symbol must equal {LABEL_SYMBOL_V002!r} for v002"
        )
    for label, val in (
        ("utc_date_start", utc_date_start),
        ("utc_date_end", utc_date_end),
    ):
        if (
            not isinstance(val, str)
            or len(val) != 10
            or val[4] != "-"
            or val[7] != "-"
        ):
            raise LabelManifestErrorV002(f"{label} must be YYYY-MM-DD")
    if not isinstance(date_count, int) or date_count <= 0:
        raise LabelManifestErrorV002("date_count must be a positive int")
    if not isinstance(row_count, int) or row_count < 0:
        raise LabelManifestErrorV002("row_count must be a non-negative int")
    if not isinstance(envelope_terminal_unix_ms, int) or envelope_terminal_unix_ms <= 0:
        raise LabelManifestErrorV002(
            "envelope_terminal_unix_ms must be a positive int"
        )
    if not isinstance(invalid_price_row_count, int) or invalid_price_row_count < 0:
        raise LabelManifestErrorV002(
            "invalid_price_row_count must be a non-negative int"
        )
    if not isinstance(censored_per_horizon, Mapping):
        raise LabelManifestErrorV002(
            "censored_per_horizon must be Mapping[str, int]"
        )
    if set(censored_per_horizon.keys()) != set(LABEL_HORIZONS_V002):
        raise LabelManifestErrorV002(
            "censored_per_horizon keys must equal LABEL_HORIZONS_V002"
        )
    for k, v in censored_per_horizon.items():
        if not isinstance(v, int) or v < 0:
            raise LabelManifestErrorV002(
                f"censored_per_horizon[{k!r}] must be a non-negative int"
            )
    for sha_label, sha_val in (
        ("label_config_hash", label_config_hash),
        ("feature_config_hash", feature_config_hash),
        ("source_feature_manifest_sha256", source_feature_manifest_sha256),
        (
            "source_feature_manifest_sidecar_sha256",
            source_feature_manifest_sidecar_sha256,
        ),
        (
            "source_feature_successor_state_sha256",
            source_feature_successor_state_sha256,
        ),
        (
            "source_feature_successor_state_sidecar_sha256",
            source_feature_successor_state_sidecar_sha256,
        ),
        (
            "source_phase_4bm_j_gate_report_sha256",
            source_phase_4bm_j_gate_report_sha256,
        ),
        ("source_phase_4bm_j_gate_sidecar_sha256", source_phase_4bm_j_gate_sidecar_sha256),
        ("source_normalized_manifest_sha256", source_normalized_manifest_sha256),
        (
            "source_normalized_manifest_sidecar_sha256",
            source_normalized_manifest_sidecar_sha256,
        ),
        (
            "source_phase_4bm_f_derived_successor_state_sha256",
            source_phase_4bm_f_derived_successor_state_sha256,
        ),
        (
            "source_phase_4bm_d_derived_gate_report_sha256",
            source_phase_4bm_d_derived_gate_report_sha256,
        ),
        ("source_raw_manifest_sha256", source_raw_manifest_sha256),
        ("source_acquisition_log_sha256", source_acquisition_log_sha256),
        (
            "source_phase_4bl_e_raw_successor_state_sha256",
            source_phase_4bl_e_raw_successor_state_sha256,
        ),
        (
            "source_phase_4bl_d_r_raw_gate_report_sha256",
            source_phase_4bl_d_r_raw_gate_report_sha256,
        ),
    ):
        if not isinstance(sha_val, str) or not _HEX64_RE.match(sha_val):
            raise LabelManifestErrorV002(
                f"{sha_label} must be a 64-char lowercase hex string"
            )
    if not isinstance(code_commit_sha, str) or not (
        _SHA1_RE.match(code_commit_sha) or code_commit_sha == "unknown"
    ):
        raise LabelManifestErrorV002(
            "code_commit_sha must be a 40-char lowercase hex SHA or 'unknown'"
        )
    if not isinstance(created_at_unix_ms, int) or created_at_unix_ms < 0:
        raise LabelManifestErrorV002(
            "created_at_unix_ms must be a non-negative int"
        )

    per_day_normalized = _validate_per_day_outputs(per_day_outputs)
    if len(per_day_normalized) != date_count:
        raise LabelManifestErrorV002(
            f"per_day_outputs length ({len(per_day_normalized)}) "
            f"!= date_count ({date_count})"
        )

    governance_labels: dict[str, str] = {
        "phase_id": "4bm-O",
        "labels": "allowed_by_future_phase_only",
        "targets": "allowed_by_future_phase_only",
        "ml": "forbidden",
        "strategy": "forbidden",
        "backtest": "forbidden",
        "acquisition": "unauthorized",
        "paper_shadow_live": "forbidden",
        "deployment": "forbidden",
        "exchange_write": "forbidden",
    }
    if extra_governance_labels:
        for k, v in extra_governance_labels.items():
            if k in governance_labels:
                raise LabelManifestErrorV002(
                    f"extra_governance_labels must not override locked key {k!r}"
                )
            if not isinstance(k, str) or not isinstance(v, str):
                raise LabelManifestErrorV002(
                    "extra_governance_labels must be Mapping[str, str]"
                )
            governance_labels[k] = v

    missing = [
        k for k in REQUIRED_LABEL_GOVERNANCE_KEYS_V002 if k not in governance_labels
    ]
    if missing:
        raise LabelManifestErrorV002(
            f"governance_labels missing required keys: {missing}"
        )
    for key, forbidden_values in FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002.items():
        if governance_labels.get(key) in forbidden_values:
            raise LabelManifestErrorV002(
                f"governance_labels[{key!r}] must not be in {sorted(forbidden_values)}"
            )

    boundary_confirmations: dict[str, bool] = {
        key: True for key in REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS_V002
    }
    censored_dict: dict[str, int] = {
        h: int(censored_per_horizon[h]) for h in LABEL_HORIZONS_V002
    }

    manifest: dict[str, Any] = {
        "dataset_family": LABEL_DATASET_FAMILY_V002,
        "dataset_version": LABEL_DATASET_VERSION_V002,
        "label_schema_version": LABEL_SCHEMA_VERSION_V002,
        "source_feature_dataset_family": SOURCE_FEATURE_DATASET_FAMILY_V002,
        "source_feature_dataset_version": SOURCE_FEATURE_DATASET_VERSION_V002,
        "source_feature_manifest_sha256": source_feature_manifest_sha256,
        "source_feature_manifest_sidecar_sha256": source_feature_manifest_sidecar_sha256,
        "source_feature_successor_state_sha256": source_feature_successor_state_sha256,
        "source_feature_successor_state_sidecar_sha256": (
            source_feature_successor_state_sidecar_sha256
        ),
        "source_phase_4bm_j_gate_report_sha256": source_phase_4bm_j_gate_report_sha256,
        "source_phase_4bm_j_gate_sidecar_sha256": source_phase_4bm_j_gate_sidecar_sha256,
        "source_normalized_manifest_sha256": source_normalized_manifest_sha256,
        "source_normalized_manifest_sidecar_sha256": (
            source_normalized_manifest_sidecar_sha256
        ),
        "source_phase_4bm_f_derived_successor_state_sha256": (
            source_phase_4bm_f_derived_successor_state_sha256
        ),
        "source_phase_4bm_d_derived_gate_report_sha256": (
            source_phase_4bm_d_derived_gate_report_sha256
        ),
        "source_raw_manifest_sha256": source_raw_manifest_sha256,
        "source_acquisition_log_sha256": source_acquisition_log_sha256,
        "source_phase_4bl_e_raw_successor_state_sha256": (
            source_phase_4bl_e_raw_successor_state_sha256
        ),
        "source_phase_4bl_d_r_raw_gate_report_sha256": (
            source_phase_4bl_d_r_raw_gate_report_sha256
        ),
        "feature_config_hash": feature_config_hash,
        "label_config_hash": label_config_hash,
        "symbol": symbol,
        "symbol_list": list(LABEL_SYMBOL_LIST_V002),
        "utc_date_start": utc_date_start,
        "utc_date_end": utc_date_end,
        "date_count": int(date_count),
        "row_count": int(row_count),
        "column_count": len(LABEL_SCHEMA_V002),
        "label_list": list(LABEL_NAMES_V002),
        "support_column_list": list(LABEL_SUPPORT_COLUMN_NAMES_V002),
        "lineage_column_list": list(LABEL_LINEAGE_COLUMNS_V002),
        "schema_column_list": list(LABEL_SCHEMA_V002),
        "horizon_list": list(LABEL_HORIZONS_V002),
        "horizon_ms_list": list(LABEL_HORIZON_MS_V002),
        "envelope_terminal_unix_ms": int(envelope_terminal_unix_ms),
        "nullable_tail_policy": NULL_CENSORING_POLICY_V002,
        "reference_price_policy": (
            ANCHOR_POLICY_V002 + " | " + FUTURE_REFERENCE_POLICY_V002
        ),
        "direction_threshold_policy": DIRECTION_THRESHOLD_POLICY_V002,
        "dtype_policy": DTYPE_POLICY_V002,
        "chronological_split_policy": "not_yet_defined",
        "invalid_price_row_count": int(invalid_price_row_count),
        "censored_per_horizon": censored_dict,
        "per_day_outputs": per_day_normalized,
        "governance_labels": governance_labels,
        "boundary_confirmations": boundary_confirmations,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "label_family_research_use_authorized": False,
        "stage_5_label_cleared": False,
        "label_computation_authorized": True,
        "label_structural_qa_authorized": False,
        "label_family_eligibility_gate_authorized": False,
        "diagnostics_authorized": False,
        "ml_authorized": False,
        "strategy_authorized": False,
        "backtest_authorized": False,
        "acquisition_authorized": False,
        "successor_authorization_after": False,
        "no_network_io": True,
        "no_credentials": True,
        "no_mcp_or_graphify": True,
        "no_manifest_mutation": True,
        "phase_4aw_flip_research_eligible_invariant_preserved": True,
        "code_commit_sha": code_commit_sha,
        "created_at_unix_ms": int(created_at_unix_ms),
    }
    return manifest


__all__ = [
    "FORBIDDEN_LABEL_GOVERNANCE_VALUES_V002",
    "LabelManifestErrorV002",
    "REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS_V002",
    "REQUIRED_LABEL_GOVERNANCE_KEYS_V002",
    "build_label_manifest_v002",
]
