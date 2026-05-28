"""Phase 4bn-B — Multi-day v002 ML-baseline report payloads and output writers.

Assembles the deterministic run-manifest, per-horizon-model-summary,
feature-schema and transform-metadata payloads for Phase 4bn-B; writes
the seven local gitignored outputs and their canonical Phase 4bb-F SHA256
sidecars (``<sha>  <basename>\\n``) under the approved namespace
``data/research/microstructure/ml-baselines/phase-4bn-b/``.

All file writes use atomic write-then-rename. No source data under
``data/microstructure/`` is mutated. No file under ``data/research/`` is
committed; the directory is gitignored under ``.gitignore:88``.

This module performs no model training or scoring. It only formats payloads
that the runner module has already computed.

No network. No credentials. No environment access.
"""

from __future__ import annotations

import contextlib
import csv
import json
import os
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import diagnostics_split_policy_v002 as policy
from . import ml_baseline_design_v002 as design
from .canonical_paths import (
    compose_canonical_sidecar_body,
    compute_file_sha256,
)


class MlBaselineReportError(RuntimeError):
    """Raised when a report assembly or output write fails."""


# ---------------------------------------------------------------------------
# Output-path helpers
# ---------------------------------------------------------------------------


def resolve_output_root(repo_root: Path) -> Path:
    """Return the canonical local gitignored namespace path for Phase 4bn-B."""
    parts = design.OUTPUT_NAMESPACE_PARTS
    out = repo_root
    for p in parts:
        out = out / p
    return out


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()


def _write_json(path: Path, payload: Mapping[str, Any]) -> str:
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    _atomic_write_bytes(path, body)
    return compute_file_sha256(path)


def _write_csv(path: Path, header: list[str], rows: list[list[object]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Use newline='' so csv.writer's CRLF-control is deterministic across
    # platforms; we emit LF-only line endings via a buffered bytes pipe.
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(header)
            for r in rows:
                w.writerow(r)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()
    return compute_file_sha256(path)


def _write_sidecar(json_path: Path, sha256_hex: str) -> tuple[Path, str]:
    body = compose_canonical_sidecar_body(
        json_sha256_hex=sha256_hex, json_basename=json_path.name
    )
    sidecar_path = json_path.with_suffix(json_path.suffix + ".sha256")
    _atomic_write_bytes(sidecar_path, body)
    return sidecar_path, compute_file_sha256(sidecar_path)


# ---------------------------------------------------------------------------
# Payload assembly
# ---------------------------------------------------------------------------


def build_feature_schema_payload() -> dict[str, Any]:
    """Return the deterministic feature-schema-used payload for the run."""
    return {
        "phase_id": design.PHASE_ID,
        "schema_version": design.ML_BASELINE_SCHEMA_VERSION,
        "feature_family": design.EXPECTED_FEATURE_FAMILY,
        "feature_dataset_version": design.EXPECTED_DATASET_VERSION,
        "feature_config_hash": design.EXPECTED_FEATURE_CONFIG_HASH,
        "n_features": len(design.COMPUTED_FEATURE_COLUMN_NAMES),
        "computed_feature_column_names_in_order": list(
            design.COMPUTED_FEATURE_COLUMN_NAMES
        ),
        "decimal_as_string_columns": list(
            design.DECIMAL_AS_STRING_FEATURE_COLUMN_NAMES
        ),
        "boolean_columns": list(design.BOOLEAN_FEATURE_COLUMN_NAMES),
        "native_numeric_columns": list(design.NUMERIC_NATIVE_FEATURE_COLUMN_NAMES),
        "excluded_lineage_column_names": list(design.EXCLUDED_LINEAGE_COLUMN_NAMES),
        "forbidden_model_matrix_substrings": list(
            design.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS
        ),
        "imputation_rule": design.IMPUTATION_RULE,
        "imputation_fill_value": design.IMPUTATION_FILL_VALUE,
        "standardization_rule": design.STANDARDIZATION_RULE,
        "standardize_boolean_flags": design.STANDARDIZE_BOOLEAN_FLAGS,
    }


def build_transform_metadata_payload(
    *,
    standardizer_dict: Mapping[str, Any],
    train_n_partitions: int,
    train_n_supervised_rows_per_horizon: Mapping[str, int],
) -> dict[str, Any]:
    """Return the transform-metadata payload (train-only fit evidence)."""
    return {
        "phase_id": design.PHASE_ID,
        "schema_version": design.ML_BASELINE_SCHEMA_VERSION,
        "fit_split": policy.TRAIN,
        "validation_apply_only": True,
        "test_holdout_used_for_fit": False,
        "test_holdout_used_for_transform": False,
        "standardizer": dict(standardizer_dict),
        "train_n_partitions_fit": int(train_n_partitions),
        "train_n_supervised_rows_per_horizon": dict(
            train_n_supervised_rows_per_horizon
        ),
        "settings": design.BaselineSettingsSnapshot().as_dict(),
        "non_authorization": dict(design.NON_AUTHORIZATION_FLAGS),
    }


def build_per_horizon_summary_payload(
    *,
    per_horizon: Mapping[str, Mapping[str, Any]],
    class_balance_by_split_horizon: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Return the per-horizon-model-summary payload."""
    return {
        "phase_id": design.PHASE_ID,
        "schema_version": design.ML_BASELINE_SCHEMA_VERSION,
        "included_horizons": list(design.INCLUDED_HORIZONS),
        "deferred_horizons": list(design.DEFERRED_HORIZONS),
        "baseline_families": list(design.BASELINE_FAMILIES_INCLUDED),
        "forbidden_baseline_families": list(design.FORBIDDEN_BASELINE_FAMILIES),
        "no_model_selected_as_best": True,
        "no_threshold_tuned": True,
        "no_feature_ranked": True,
        "no_strategy_or_signals_generated": True,
        "no_pnl_simulated": True,
        "no_backtest_run": True,
        "class_balance_by_split_horizon": dict(class_balance_by_split_horizon),
        "per_horizon_results": dict(per_horizon),
        "non_authorization": dict(design.NON_AUTHORIZATION_FLAGS),
    }


def build_run_manifest_payload(
    *,
    created_at_unix_ms: int,
    code_commit_sha: str,
    label_manifest_sha256: str,
    feature_manifest_sha256: str,
    label_manifest_path: str,
    feature_manifest_path: str,
    output_basenames: Mapping[str, str],
    output_sha256s: Mapping[str, str],
    output_sidecar_basenames: Mapping[str, str],
    output_sidecar_sha256s: Mapping[str, str],
    run_duration_seconds: float,
    train_n_partitions: int,
    validation_n_partitions: int,
    test_n_partitions_unused: int,
    train_supervised_rows_per_horizon: Mapping[str, int],
    validation_supervised_rows_per_horizon: Mapping[str, int],
    train_censored_rows_per_horizon: Mapping[str, int],
    validation_censored_rows_per_horizon: Mapping[str, int],
    train_embargoed_rows: int,
    validation_embargoed_rows: int,
    test_rows_loaded: int,
    runtime_environment: Mapping[str, Any],
) -> dict[str, Any]:
    """Return the run-manifest payload describing the executed Phase 4bn-B run."""
    return {
        "phase_id": design.PHASE_ID,
        "schema_version": design.ML_BASELINE_SCHEMA_VERSION,
        "created_at_unix_ms": int(created_at_unix_ms),
        "code_commit_sha": str(code_commit_sha),
        "run_duration_seconds": float(run_duration_seconds),
        "dataset_identity": {
            "feature_family": design.EXPECTED_FEATURE_FAMILY,
            "label_family": design.EXPECTED_LABEL_FAMILY,
            "dataset_version": design.EXPECTED_DATASET_VERSION,
            "symbol": design.EXPECTED_SYMBOL,
            "date_start": design.EXPECTED_DATE_START,
            "date_end": design.EXPECTED_DATE_END,
            "feature_config_hash": design.EXPECTED_FEATURE_CONFIG_HASH,
            "label_config_hash": design.EXPECTED_LABEL_CONFIG_HASH,
            "expected_total_rows": design.EXPECTED_TOTAL_ROW_COUNT,
            "expected_partition_count": design.EXPECTED_PARTITION_COUNT,
            "horizons_included": list(design.INCLUDED_HORIZONS),
            "horizons_deferred": list(design.DEFERRED_HORIZONS),
        },
        "source_manifests": {
            "label_manifest_path": label_manifest_path,
            "label_manifest_sha256": label_manifest_sha256,
            "feature_manifest_path": feature_manifest_path,
            "feature_manifest_sha256": feature_manifest_sha256,
        },
        "split_policy": policy.SplitPolicySnapshot().as_dict(),
        "supervised_splits_used": list(design.SUPERVISED_SPLITS),
        "test_holdout_sealed": True,
        "test_rows_loaded": int(test_rows_loaded),
        "split_partition_counts": {
            policy.TRAIN: int(train_n_partitions),
            policy.VALIDATION: int(validation_n_partitions),
            policy.TEST: int(test_n_partitions_unused),
        },
        "train_supervised_rows_per_horizon": dict(train_supervised_rows_per_horizon),
        "validation_supervised_rows_per_horizon": dict(
            validation_supervised_rows_per_horizon
        ),
        "train_censored_rows_per_horizon": dict(train_censored_rows_per_horizon),
        "validation_censored_rows_per_horizon": dict(
            validation_censored_rows_per_horizon
        ),
        "train_embargoed_rows": int(train_embargoed_rows),
        "validation_embargoed_rows": int(validation_embargoed_rows),
        "settings": design.BaselineSettingsSnapshot().as_dict(),
        "outputs": {
            "basenames": dict(output_basenames),
            "sha256s": dict(output_sha256s),
            "sidecar_basenames": dict(output_sidecar_basenames),
            "sidecar_sha256s": dict(output_sidecar_sha256s),
        },
        "runtime_environment": dict(runtime_environment),
        "non_authorization": dict(design.NON_AUTHORIZATION_FLAGS),
    }


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------


@dataclass
class WrittenArtefacts:
    output_root: Path
    json_paths: dict[str, Path]
    csv_paths: dict[str, Path]
    sha256s: dict[str, str]
    sidecar_paths: dict[str, Path]
    sidecar_sha256s: dict[str, str]


def write_csv_table(
    *, output_root: Path, basename: str, header: list[str], rows: list[list[object]]
) -> tuple[Path, str, Path, str]:
    """Write a CSV table under *output_root* with a canonical sidecar."""
    path = output_root / basename
    sha = _write_csv(path, header, rows)
    sidecar, sidecar_sha = _write_sidecar(path, sha)
    return path, sha, sidecar, sidecar_sha


def write_json_artefact(
    *, output_root: Path, basename: str, payload: Mapping[str, Any]
) -> tuple[Path, str, Path, str]:
    """Write a JSON artefact under *output_root* with a canonical sidecar."""
    path = output_root / basename
    sha = _write_json(path, payload)
    sidecar, sidecar_sha = _write_sidecar(path, sha)
    return path, sha, sidecar, sidecar_sha


def metrics_csv_header() -> list[str]:
    return ["family", "split", "horizon", "metric_name", "metric_value"]


def class_balance_csv_header() -> list[str]:
    return [
        "split",
        "horizon",
        "n_rows_total",
        "n_rows_supervised",
        "n_rows_censored",
        "n_rows_embargoed",
        "n_down",
        "n_flat",
        "n_up",
        "prev_down",
        "prev_flat",
        "prev_up",
    ]


def calibration_csv_header() -> list[str]:
    return [
        "family",
        "split",
        "horizon",
        "bin_low",
        "bin_high",
        "n_rows",
        "mean_max_predicted_proba",
        "empirical_accuracy",
        "reliability_gap",
    ]


__all__ = [
    "MlBaselineReportError",
    "WrittenArtefacts",
    "build_feature_schema_payload",
    "build_per_horizon_summary_payload",
    "build_run_manifest_payload",
    "build_transform_metadata_payload",
    "calibration_csv_header",
    "class_balance_csv_header",
    "metrics_csv_header",
    "resolve_output_root",
    "write_csv_table",
    "write_json_artefact",
]
