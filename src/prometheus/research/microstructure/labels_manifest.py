"""Phase 4bj-C label manifest builder.

Builds a JSON-friendly manifest dict for the future label family
``microstructure_labels_aggtrades_v001``. The manifest:

- defaults ``research_eligible=False`` and
  ``eligibility_gate_status="pending"`` (Phase 4bj-C produces local
  gitignored label artefacts only);
- carries the Phase 4bj-C governance label block locking
  ``ml = "forbidden"``, ``strategy = "forbidden"``,
  ``backtest = "forbidden"``, ``acquisition = "unauthorized"``,
  ``paper_shadow_live = "forbidden"``, ``deployment = "forbidden"``,
  and ``exchange_write = "forbidden"``;
- pins the source feature lineage SHAs and the source normalized
  parquet SHA;
- records the locked schema descriptors (``label_list``,
  ``support_column_list``, ``schema_column_list``, ``horizon_list``,
  ``horizon_ms_list``);
- records the deterministic ``label_config_hash`` and the policy
  identifiers (``nullable_tail_policy``, ``reference_price_policy``,
  ``direction_threshold_policy``);
- defaults ``chronological_split_policy`` to ``"not_yet_defined"``;
- records the per-run counts (``invalid_price_row_count``,
  ``censored_per_horizon``);
- declares the 13 boundary confirmations all ``True``.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT write any file on its own; the caller is responsible for
  atomic write via :mod:`labels_io`.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from .labels_schema import (
    ANCHOR_POLICY_V001,
    DIRECTION_THRESHOLD_POLICY_V001,
    DTYPE_POLICY_V001,
    FUTURE_REFERENCE_POLICY_V001,
    LABEL_DATASET_FAMILY_V001,
    LABEL_DATASET_VERSION_V001,
    LABEL_HORIZON_MS_V001,
    LABEL_HORIZONS_V001,
    LABEL_NAMES_V001,
    LABEL_SCHEMA_V001,
    LABEL_SCHEMA_VERSION_V001,
    LABEL_SUPPORT_COLUMN_NAMES_V001,
    NULL_CENSORING_POLICY_V001,
    SOURCE_FEATURE_DATASET_FAMILY_V001,
    SOURCE_FEATURE_DATASET_VERSION_V001,
)

REQUIRED_LABEL_GOVERNANCE_KEYS: tuple[str, ...] = (
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
"""Required governance label keys at v001."""

FORBIDDEN_LABEL_GOVERNANCE_VALUES: Mapping[str, frozenset[str]] = {
    "ml": frozenset({"allowed"}),
    "strategy": frozenset({"allowed"}),
    "backtest": frozenset({"allowed"}),
    "acquisition": frozenset({"allowed"}),
    "paper_shadow_live": frozenset({"allowed"}),
    "deployment": frozenset({"allowed"}),
    "exchange_write": frozenset({"allowed"}),
}
"""Governance label values that must NOT appear at v001."""

REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS: tuple[str, ...] = (
    "no_ml",
    "no_strategy",
    "no_backtest",
    "no_acquisition",
    "no_network",
    "no_credentials",
    "no_feature_manifest_mutation",
    "no_feature_parquet_mutation",
    "no_feature_successor_state_mutation",
    "no_feature_gate_report_mutation",
    "no_label_gate_report",
    "no_label_successor_state",
    "no_successor_authorization",
)
"""The 13 required boundary confirmations at v001."""


_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


class LabelManifestError(RuntimeError):
    """Raised when a Phase 4bj-C label manifest input is invalid."""


def build_label_manifest_v001(
    *,
    symbol: str,
    utc_date: str,
    label_parquet_relative_path: str,
    label_parquet_sha256: str,
    label_parquet_size_bytes: int,
    row_count: int,
    label_config_hash: str,
    source_feature_manifest_sha256: str,
    source_feature_parquet_sha256: str,
    source_feature_successor_state_sha256: str,
    source_phase_4bi_b_gate_report_sha256: str,
    source_normalized_parquet_sha256: str,
    invalid_price_row_count: int,
    censored_per_horizon: Mapping[str, int],
    code_commit_sha: str = "unknown",
    created_at_unix_ms: int = 0,
    created_at_utc: str = "",
    extra_governance_labels: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Construct the Phase 4bj-C label manifest as a JSON-friendly dict.

    Parameters are validated locally; the caller is responsible for
    atomic write via :mod:`labels_io`. The manifest defaults
    ``research_eligible=False`` and ``eligibility_gate_status="pending"``;
    those flags can only be flipped by a separately authorized future
    label-family eligibility gate phase (Phase 4bj-E or equivalent).
    """
    if not isinstance(symbol, str) or not symbol or symbol != symbol.upper():
        raise LabelManifestError("symbol must be uppercase non-empty string")
    if (
        not isinstance(utc_date, str)
        or len(utc_date) != 10
        or utc_date[4] != "-"
        or utc_date[7] != "-"
        or not (
            utc_date[:4].isdigit()
            and utc_date[5:7].isdigit()
            and utc_date[8:10].isdigit()
        )
    ):
        raise LabelManifestError("utc_date must be YYYY-MM-DD")
    if (
        not isinstance(label_parquet_relative_path, str)
        or not label_parquet_relative_path
    ):
        raise LabelManifestError(
            "label_parquet_relative_path must be a non-empty string"
        )
    for label, sha in (
        ("label_parquet_sha256", label_parquet_sha256),
        ("label_config_hash", label_config_hash),
        ("source_feature_manifest_sha256", source_feature_manifest_sha256),
        ("source_feature_parquet_sha256", source_feature_parquet_sha256),
        (
            "source_feature_successor_state_sha256",
            source_feature_successor_state_sha256,
        ),
        (
            "source_phase_4bi_b_gate_report_sha256",
            source_phase_4bi_b_gate_report_sha256,
        ),
        ("source_normalized_parquet_sha256", source_normalized_parquet_sha256),
    ):
        if not isinstance(sha, str) or not _HEX64_RE.match(sha):
            raise LabelManifestError(f"{label} must be a 64-char hex string")
    if not isinstance(row_count, int) or row_count < 0:
        raise LabelManifestError("row_count must be a non-negative int")
    if not isinstance(label_parquet_size_bytes, int) or label_parquet_size_bytes < 0:
        raise LabelManifestError(
            "label_parquet_size_bytes must be a non-negative int"
        )
    if not isinstance(invalid_price_row_count, int) or invalid_price_row_count < 0:
        raise LabelManifestError(
            "invalid_price_row_count must be a non-negative int"
        )
    if not isinstance(censored_per_horizon, Mapping):
        raise LabelManifestError("censored_per_horizon must be a Mapping[str, int]")
    if tuple(censored_per_horizon.keys()) != LABEL_HORIZONS_V001 and set(
        censored_per_horizon.keys()
    ) != set(LABEL_HORIZONS_V001):
        raise LabelManifestError(
            "censored_per_horizon keys must equal LABEL_HORIZONS_V001"
        )
    for k, v in censored_per_horizon.items():
        if not isinstance(v, int) or v < 0:
            raise LabelManifestError(
                f"censored_per_horizon[{k!r}] must be a non-negative int"
            )
    if not isinstance(code_commit_sha, str) or not (
        _SHA1_RE.match(code_commit_sha) or code_commit_sha == "unknown"
    ):
        raise LabelManifestError(
            "code_commit_sha must be a 40-char lowercase hex SHA or 'unknown'"
        )

    governance_labels: dict[str, str] = {
        "phase_id": "4bj-C",
        "labels": "allowed_by_phase_4bj_c",
        "targets": "allowed_by_phase_4bj_c",
        "ml": "forbidden",
        "strategy": "forbidden",
        "backtest": "forbidden",
        "acquisition": "unauthorized",
        "paper_shadow_live": "forbidden",
        "deployment": "forbidden",
        "exchange_write": "forbidden",
    }
    if extra_governance_labels:
        for extra_key, extra_value in extra_governance_labels.items():
            if extra_key in governance_labels:
                raise LabelManifestError(
                    f"extra_governance_labels must not override locked key {extra_key!r}"
                )
            if not isinstance(extra_key, str) or not isinstance(extra_value, str):
                raise LabelManifestError(
                    "extra_governance_labels must be Mapping[str, str]"
                )
            governance_labels[extra_key] = extra_value

    missing = [
        k for k in REQUIRED_LABEL_GOVERNANCE_KEYS if k not in governance_labels
    ]
    if missing:
        raise LabelManifestError(
            f"governance_labels missing required keys: {missing}"
        )
    for key, forbidden_values in FORBIDDEN_LABEL_GOVERNANCE_VALUES.items():
        if governance_labels.get(key) in forbidden_values:
            raise LabelManifestError(
                f"governance_labels[{key!r}] must not be in {sorted(forbidden_values)}"
            )

    boundary_confirmations: dict[str, bool] = {
        key: True for key in REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS
    }

    censored_dict: dict[str, int] = {
        label: int(censored_per_horizon[label]) for label in LABEL_HORIZONS_V001
    }

    manifest: dict[str, Any] = {
        "dataset_family": LABEL_DATASET_FAMILY_V001,
        "dataset_version": LABEL_DATASET_VERSION_V001,
        "label_schema_version": LABEL_SCHEMA_VERSION_V001,
        "symbol": symbol,
        "utc_date": utc_date,
        "source_feature_dataset_family": SOURCE_FEATURE_DATASET_FAMILY_V001,
        "source_feature_dataset_version": SOURCE_FEATURE_DATASET_VERSION_V001,
        "source_feature_manifest_sha256": source_feature_manifest_sha256,
        "source_feature_parquet_sha256": source_feature_parquet_sha256,
        "source_feature_successor_state_sha256": source_feature_successor_state_sha256,
        "source_phase_4bi_b_gate_report_sha256": (
            source_phase_4bi_b_gate_report_sha256
        ),
        "source_normalized_parquet_sha256": source_normalized_parquet_sha256,
        "label_config_hash": label_config_hash,
        "label_list": list(LABEL_NAMES_V001),
        "support_column_list": list(LABEL_SUPPORT_COLUMN_NAMES_V001),
        "schema_column_list": list(LABEL_SCHEMA_V001),
        "horizon_list": list(LABEL_HORIZONS_V001),
        "horizon_ms_list": list(LABEL_HORIZON_MS_V001),
        "row_count": int(row_count),
        "column_count": len(LABEL_SCHEMA_V001),
        "nullable_tail_policy": NULL_CENSORING_POLICY_V001,
        "reference_price_policy": (
            ANCHOR_POLICY_V001 + " | " + FUTURE_REFERENCE_POLICY_V001
        ),
        "direction_threshold_policy": DIRECTION_THRESHOLD_POLICY_V001,
        "dtype_policy": DTYPE_POLICY_V001,
        "chronological_split_policy": "not_yet_defined",
        "invalid_price_row_count": int(invalid_price_row_count),
        "censored_per_horizon": censored_dict,
        "files": [
            {
                "path": label_parquet_relative_path,
                "sha256": label_parquet_sha256,
                "size_bytes": int(label_parquet_size_bytes),
                "row_count": int(row_count),
            }
        ],
        "governance_labels": governance_labels,
        "boundary_confirmations": boundary_confirmations,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "code_commit_sha": code_commit_sha,
        "created_at_unix_ms": int(created_at_unix_ms),
        "created_at_utc": str(created_at_utc),
    }
    return manifest


__all__ = [
    "FORBIDDEN_LABEL_GOVERNANCE_VALUES",
    "LabelManifestError",
    "REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS",
    "REQUIRED_LABEL_GOVERNANCE_KEYS",
    "build_label_manifest_v001",
]
