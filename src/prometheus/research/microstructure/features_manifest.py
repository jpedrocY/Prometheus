"""Phase 4bh feature manifest builder for ``microstructure_features_aggtrades_v001``.

Builds a JSON-friendly manifest dict for the feature family. The
manifest:

- defaults ``research_eligible=False`` and
  ``eligibility_gate_status="pending"`` (Phase 4bh produces local
  Stage-2 feature artefacts only; the feature-family eligibility gate
  is the only path that may flip those flags in a separately
  authorized future phase);
- carries a fixed set of governance labels per the Phase 4bh-B contract
  including ``feature_computation = "allowed_by_phase_4bh"``,
  ``labels = "forbidden"``, ``ml = "forbidden"``,
  ``strategy = "forbidden"``, ``backtest = "forbidden"``,
  ``acquisition = "unauthorized"``, and
  ``stop_trigger_domain = "trade_price_backtest_candidate"``;
- pins lineage SHAs for the source normalized parquet, source
  normalized manifest, Phase 4bg-B successor-state JSON, and the
  Phase 4bf derived gate report.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read environment files, or import any networking library;
- does NOT write any file on its own; the orchestrator in
  :mod:`features_compute` and :mod:`features_io` performs all writes;
- never flips ``research_eligible`` to ``True`` and never modifies any
  prior manifest, gate report, or successor-state artefact.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from .features_schema import (
    FEATURE_DATASET_FAMILY,
    FEATURE_DATASET_VERSION,
    FEATURE_NAMES_V001,
    FEATURE_SCHEMA_VERSION,
    FEATURE_WINDOW_LABELS_V001,
    FEATURE_WINDOWS_MS_V001,
    SOURCE_NORMALIZED_DATASET_FAMILY,
    SOURCE_NORMALIZED_DATASET_VERSION,
)

REQUIRED_FEATURE_GOVERNANCE_KEYS: tuple[str, ...] = (
    "phase_id",
    "feature_computation",
    "labels",
    "ml",
    "strategy",
    "backtest",
    "acquisition",
    "stop_trigger_domain",
)
"""Required governance label keys at v001."""


FORBIDDEN_FEATURE_GOVERNANCE_VALUES: Mapping[str, frozenset[str]] = {
    "labels": frozenset({"allowed"}),
    "ml": frozenset({"allowed"}),
    "strategy": frozenset({"allowed"}),
    "backtest": frozenset({"allowed"}),
    "acquisition": frozenset({"allowed"}),
}
"""Governance label values that must NOT appear at v001."""


REQUIRED_BOUNDARY_CONFIRMATIONS: tuple[str, ...] = (
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
)
"""The 11 required boundary confirmations at v001."""


class FeatureManifestError(RuntimeError):
    """Raised when a Phase 4bh feature manifest input is invalid."""


def build_feature_manifest(
    *,
    symbol: str,
    utc_date: str,
    feature_parquet_relative_path: str,
    feature_parquet_sha256: str,
    feature_parquet_size_bytes: int,
    row_count: int,
    feature_config_hash: str,
    source_normalized_manifest_sha256: str,
    source_normalized_parquet_sha256: str,
    source_successor_state_sha256: str,
    source_phase_4bf_gate_report_sha256: str,
    invalid_windows: Sequence[Mapping[str, Any]] = (),
    code_commit_sha: str = "unknown",
    created_at_unix_ms: int = 0,
    extra_governance_labels: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Construct the Phase 4bh feature manifest as a JSON-friendly dict.

    Parameters are validated locally; the orchestrator in
    :mod:`features_compute` is responsible for atomic write via
    :mod:`features_io`. The manifest defaults
    ``research_eligible=False`` and ``eligibility_gate_status="pending"``;
    those flags can only be flipped by a separately authorized future
    feature-family eligibility gate phase.
    """
    if not isinstance(symbol, str) or not symbol or symbol != symbol.upper():
        raise FeatureManifestError("symbol must be uppercase non-empty string")
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
        raise FeatureManifestError("utc_date must be YYYY-MM-DD")
    if (
        not isinstance(feature_parquet_relative_path, str)
        or not feature_parquet_relative_path
    ):
        raise FeatureManifestError(
            "feature_parquet_relative_path must be a non-empty string"
        )
    for label, sha in (
        ("feature_parquet_sha256", feature_parquet_sha256),
        ("feature_config_hash", feature_config_hash),
        ("source_normalized_manifest_sha256", source_normalized_manifest_sha256),
        ("source_normalized_parquet_sha256", source_normalized_parquet_sha256),
        ("source_successor_state_sha256", source_successor_state_sha256),
        (
            "source_phase_4bf_gate_report_sha256",
            source_phase_4bf_gate_report_sha256,
        ),
    ):
        if not isinstance(sha, str) or len(sha) != 64:
            raise FeatureManifestError(f"{label} must be a 64-char hex string")
    if not isinstance(row_count, int) or row_count < 0:
        raise FeatureManifestError("row_count must be a non-negative int")
    if not isinstance(feature_parquet_size_bytes, int) or (
        feature_parquet_size_bytes < 0
    ):
        raise FeatureManifestError(
            "feature_parquet_size_bytes must be a non-negative int"
        )

    governance_labels: dict[str, str] = {
        "phase_id": "4bh",
        "feature_computation": "allowed_by_phase_4bh",
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
                raise FeatureManifestError(
                    f"extra_governance_labels must not override locked key {k!r}"
                )
            if not isinstance(k, str) or not isinstance(v, str):
                raise FeatureManifestError(
                    "extra_governance_labels must be Mapping[str, str]"
                )
            governance_labels[k] = v

    missing = [k for k in REQUIRED_FEATURE_GOVERNANCE_KEYS if k not in governance_labels]
    if missing:
        raise FeatureManifestError(
            f"governance_labels missing required keys: {missing}"
        )
    for key, forbidden_values in FORBIDDEN_FEATURE_GOVERNANCE_VALUES.items():
        if governance_labels.get(key) in forbidden_values:
            raise FeatureManifestError(
                f"governance_labels[{key!r}] must not be in {sorted(forbidden_values)}"
            )

    boundary_confirmations: dict[str, bool] = {
        key: True for key in REQUIRED_BOUNDARY_CONFIRMATIONS
    }
    invalid_window_list = list(_normalize_invalid_windows(invalid_windows))

    manifest: dict[str, Any] = {
        "dataset_family": FEATURE_DATASET_FAMILY,
        "dataset_version": FEATURE_DATASET_VERSION,
        "feature_schema_version": FEATURE_SCHEMA_VERSION,
        "symbol": symbol,
        "utc_date": utc_date,
        "source_normalized_dataset_family": SOURCE_NORMALIZED_DATASET_FAMILY,
        "source_normalized_dataset_version": SOURCE_NORMALIZED_DATASET_VERSION,
        "source_normalized_manifest_sha256": source_normalized_manifest_sha256,
        "source_normalized_parquet_sha256": source_normalized_parquet_sha256,
        "source_successor_state_sha256": source_successor_state_sha256,
        "source_phase_4bf_gate_report_sha256": source_phase_4bf_gate_report_sha256,
        "feature_config_hash": feature_config_hash,
        "feature_list": list(FEATURE_NAMES_V001),
        "window_list": list(FEATURE_WINDOW_LABELS_V001),
        "window_ms_list": list(FEATURE_WINDOWS_MS_V001),
        "row_count": int(row_count),
        "invalid_windows": invalid_window_list,
        "files": [
            {
                "path": feature_parquet_relative_path,
                "sha256": feature_parquet_sha256,
                "size_bytes": int(feature_parquet_size_bytes),
                "row_count": int(row_count),
            }
        ],
        "governance_labels": governance_labels,
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "code_commit_sha": code_commit_sha,
        "created_at_unix_ms": int(created_at_unix_ms),
        "boundary_confirmations": boundary_confirmations,
    }
    return manifest


def _normalize_invalid_windows(
    raw: Iterable[Mapping[str, Any]],
) -> Iterable[dict[str, Any]]:
    """Return invalid_windows entries as plain dicts in deterministic order."""
    for entry in raw:
        if not isinstance(entry, Mapping):
            raise FeatureManifestError(
                "invalid_windows entries must be Mapping[str, Any]"
            )
        yield dict(entry)


__all__ = [
    "FORBIDDEN_FEATURE_GOVERNANCE_VALUES",
    "FeatureManifestError",
    "REQUIRED_BOUNDARY_CONFIRMATIONS",
    "REQUIRED_FEATURE_GOVERNANCE_KEYS",
    "build_feature_manifest",
]
