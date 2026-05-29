"""Phase 4bn-E — Multi-day v002 train-vs-validation feature drift runner.

Standalone offline orchestrator authorised by the Phase 4bn-E
authorization prompt. Streams the existing v002 train and validation
partitions twice over the 45 Phase 4bn-B computed feature columns,
accumulates exact per-feature streaming statistics and approximate
quantile histograms, and writes three local gitignored output files
under ``data/research/microstructure/ml-baselines/phase-4bn-e/``:

- ``feature_drift_summary.csv`` (one row per feature with train and
  validation statistics + train-vs-validation deltas + the fixed
  a-priori drift classification).
- ``feature_drift_overview.json`` (aggregate counts per drift class +
  highest observed deltas + fixed-thresholds metadata).
- ``feature_drift_manifest.json`` (run manifest with phase identity,
  base SHA, input artefact references, output basenames and SHA256s,
  and the explicit non-authorization block).

Each output is paired with a canonical Phase 4bb-F sidecar
(``<sha>  <basename>\\n``). The diagnostic does not train any model,
score any model, generate any prediction, rank any feature, select any
feature, prune any feature, tune any threshold, define any strategy,
simulate any PnL, run any backtest, acquire any data, call any
endpoint, open any WebSocket / user stream, use any credential, read
``.env`` / ``.mcp.json`` / MCP / Graphify, mutate any manifest, mutate
any successor-state artefact, persist any model binary, persist any
row-level prediction, materialise any reusable split mask, commit any
``data/microstructure/`` artefact, or commit any ``data/research/``
artefact. The sealed test holdout is never loaded.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure import (  # noqa: E402
    diagnostics_split_policy_v002 as policy,
)
from prometheus.research.microstructure import feature_drift_v002 as drift  # noqa: E402
from prometheus.research.microstructure import (  # noqa: E402
    ml_baseline_design_v002 as design,
)
from prometheus.research.microstructure import (  # noqa: E402
    ml_baseline_report_v002 as report,
)
from prometheus.research.microstructure.canonical_paths import (  # noqa: E402
    compute_file_sha256,
)
from prometheus.research.microstructure.ml_baseline_dataset_v002 import (  # noqa: E402
    discover_partition_refs,
)

_OUTPUT_NAMESPACE_PARTS: tuple[str, ...] = (
    "data",
    "research",
    "microstructure",
    "ml-baselines",
    "phase-4bn-e",
)

_OUTPUT_DRIFT_SUMMARY_BASENAME = "feature_drift_summary.csv"
_OUTPUT_DRIFT_OVERVIEW_BASENAME = "feature_drift_overview.json"
_OUTPUT_DRIFT_MANIFEST_BASENAME = "feature_drift_manifest.json"

# Phase 4bn-D scoping-memo SHA-finalization commit (base SHA carried verbatim
# from the authorization prompt; not validated against the working tree).
_PHASE_4BN_D_FINAL_MAIN_SHA = "254cdacfdfebf37ab9f56fb9b7c0a79ce9d92f84"


def _resolve_output_root(repo_root: Path) -> Path:
    out = repo_root
    for p in _OUTPUT_NAMESPACE_PARTS:
        out = out / p
    return out


def _runtime_env_snapshot() -> dict[str, object]:
    return {
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "executable_basename": Path(sys.executable).name,
    }


def _drift_summary_header() -> list[str]:
    return [
        "feature_name",
        "train_count_non_null",
        "train_null_count",
        "train_missing_rate",
        "train_mean",
        "train_std",
        "train_min",
        "train_max",
        "train_p01",
        "train_p05",
        "train_p25",
        "train_median",
        "train_p75",
        "train_p95",
        "train_p99",
        "validation_count_non_null",
        "validation_null_count",
        "validation_missing_rate",
        "validation_mean",
        "validation_std",
        "validation_min",
        "validation_max",
        "validation_p01",
        "validation_p05",
        "validation_p25",
        "validation_median",
        "validation_p75",
        "validation_p95",
        "validation_p99",
        "absolute_mean_delta",
        "standardized_mean_delta",
        "absolute_median_delta",
        "validation_to_train_std_ratio",
        "absolute_p95_delta",
        "absolute_p05_delta",
        "missing_rate_delta",
        "train_std_is_safe",
        "drift_classification",
    ]


def _format_float(value: float | None) -> object:
    if value is None:
        return ""
    if isinstance(value, float) and not math.isfinite(value):
        return ""
    return value


def _drift_row_to_csv(row: drift.FeatureDriftRow) -> list[object]:
    return [
        row.feature_name,
        int(row.train_count_non_null),
        int(row.train_null_count),
        _format_float(row.train_missing_rate),
        _format_float(row.train_mean),
        _format_float(row.train_std),
        _format_float(row.train_min),
        _format_float(row.train_max),
        _format_float(row.train_p01),
        _format_float(row.train_p05),
        _format_float(row.train_p25),
        _format_float(row.train_median),
        _format_float(row.train_p75),
        _format_float(row.train_p95),
        _format_float(row.train_p99),
        int(row.validation_count_non_null),
        int(row.validation_null_count),
        _format_float(row.validation_missing_rate),
        _format_float(row.validation_mean),
        _format_float(row.validation_std),
        _format_float(row.validation_min),
        _format_float(row.validation_max),
        _format_float(row.validation_p01),
        _format_float(row.validation_p05),
        _format_float(row.validation_p25),
        _format_float(row.validation_median),
        _format_float(row.validation_p75),
        _format_float(row.validation_p95),
        _format_float(row.validation_p99),
        _format_float(row.absolute_mean_delta),
        _format_float(row.standardized_mean_delta),
        _format_float(row.absolute_median_delta),
        _format_float(row.validation_to_train_std_ratio),
        _format_float(row.absolute_p95_delta),
        _format_float(row.absolute_p05_delta),
        _format_float(row.missing_rate_delta),
        bool(row.train_std_is_safe),
        row.drift_classification,
    ]


def _drift_row_to_json_dict(row: drift.FeatureDriftRow) -> dict[str, object]:
    raw = dataclasses.asdict(row)
    # Replace NaN with None for JSON cleanliness.
    out: dict[str, object] = {}
    for k, v in raw.items():
        if isinstance(v, float) and not math.isfinite(v):
            out[k] = None
        else:
            out[k] = v
    return out


def _build_overview_payload(rows: list[drift.FeatureDriftRow]) -> dict[str, object]:
    overview = drift.compute_overview(rows)
    overview["per_feature"] = [_drift_row_to_json_dict(r) for r in rows]
    overview["feature_column_order"] = list(design.COMPUTED_FEATURE_COLUMN_NAMES)
    return overview


def _build_manifest_payload(
    *,
    created_at_unix_ms: int,
    code_commit_sha: str,
    base_main_sha: str,
    label_manifest_path: str,
    feature_manifest_path: str,
    label_manifest_sha: str,
    feature_manifest_sha: str,
    output_basenames: dict[str, str],
    output_sha256s: dict[str, str],
    output_sidecar_basenames: dict[str, str],
    output_sidecar_sha256s: dict[str, str],
    run_duration_seconds: float,
    train_n_partitions: int,
    validation_n_partitions: int,
    test_n_partitions_unused: int,
    runtime_environment: dict[str, object],
    exact_command: str,
) -> dict[str, object]:
    return {
        "phase_id": drift.PHASE_ID,
        "schema_version": drift.SCHEMA_VERSION,
        "scope": "C-D train-vs-validation feature drift diagnostics",
        "base_main_sha": base_main_sha,
        "created_at_unix_ms": int(created_at_unix_ms),
        "code_commit_sha": str(code_commit_sha),
        "run_duration_seconds": float(run_duration_seconds),
        "dataset_identity": {
            "feature_family": design.EXPECTED_FEATURE_FAMILY,
            "label_family": design.EXPECTED_LABEL_FAMILY,
            "dataset_version": design.EXPECTED_DATASET_VERSION,
            "symbol": design.EXPECTED_SYMBOL,
            "feature_config_hash": design.EXPECTED_FEATURE_CONFIG_HASH,
            "label_config_hash": design.EXPECTED_LABEL_CONFIG_HASH,
            "expected_partition_count": design.EXPECTED_PARTITION_COUNT,
        },
        "source_manifests": {
            "label_manifest_path": label_manifest_path,
            "label_manifest_sha256": label_manifest_sha,
            "feature_manifest_path": feature_manifest_path,
            "feature_manifest_sha256": feature_manifest_sha,
        },
        "split_policy": policy.SplitPolicySnapshot().as_dict(),
        "supervised_splits_used": list(drift.SUPERVISED_SPLITS),
        "feature_count": int(len(design.COMPUTED_FEATURE_COLUMN_NAMES)),
        "feature_column_order": list(design.COMPUTED_FEATURE_COLUMN_NAMES),
        "excluded_lineage_column_names": list(design.EXCLUDED_LINEAGE_COLUMN_NAMES),
        "forbidden_model_matrix_substrings": list(
            design.FORBIDDEN_MODEL_MATRIX_SUBSTRINGS
        ),
        "test_holdout_sealed": True,
        "test_holdout_used": False,
        "test_n_partitions_unused": int(test_n_partitions_unused),
        "split_partition_counts": {
            policy.TRAIN: int(train_n_partitions),
            policy.VALIDATION: int(validation_n_partitions),
            policy.TEST: int(test_n_partitions_unused),
        },
        "histogram": {
            "n_bins": drift.HISTOGRAM_N_BINS,
            "edge_method": "linspace(global_min, global_max) from pass 1",
            "quantiles_are_approximate_via_histogram": True,
        },
        "drift_classification_thresholds": {
            "low_max_inclusive": drift.LOW_DRIFT_STD_MEAN_DELTA_MAX,
            "high_min_inclusive": drift.HIGH_DRIFT_STD_MEAN_DELTA_MIN,
            "safe_train_std_min": drift.SAFE_TRAIN_STD_MIN,
            "scale": "standardized_mean_delta_magnitude",
            "thresholds_are_fixed_a_priori": True,
            "thresholds_not_selected_from_results": True,
        },
        "models_trained": False,
        "predictions_generated": False,
        "feature_ranking_authorized": False,
        "feature_selection_authorized": False,
        "feature_pruning_authorized": False,
        "feature_engineering_authorized": False,
        "threshold_tuning_authorized": False,
        "strategy_authorized": False,
        "pnl_or_backtest_authorized": False,
        "acquisition_authorized": False,
        "manifest_mutation_authorized": False,
        "successor_state_mutation_authorized": False,
        "model_binary_persisted": False,
        "row_level_predictions_persisted": False,
        "reusable_split_mask_persisted": False,
        "data_committed": False,
        "data_microstructure_committed": False,
        "data_research_committed": False,
        "exact_command_used": exact_command,
        "outputs": {
            "basenames": dict(output_basenames),
            "sha256s": dict(output_sha256s),
            "sidecar_basenames": dict(output_sidecar_basenames),
            "sidecar_sha256s": dict(output_sidecar_sha256s),
        },
        "runtime_environment": dict(runtime_environment),
        "non_authorization": dict(drift.NON_AUTHORIZATION_FLAGS),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 4bn-E multi-day v002 feature drift diagnostic runner"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=_REPO_ROOT,
        help="repository root (defaults to script's parent)",
    )
    parser.add_argument(
        "--code-commit-sha",
        type=str,
        default="unknown",
        help="40-char lowercase hex code commit SHA (or 'unknown')",
    )
    parser.add_argument(
        "--base-main-sha",
        type=str,
        default=_PHASE_4BN_D_FINAL_MAIN_SHA,
        help="base main SHA carried forward from Phase 4bn-D",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=None,
        help="research-output namespace root (defaults to the approved path)",
    )
    args = parser.parse_args(argv)
    repo_root: Path = args.repo_root.resolve()
    if not (repo_root / "src" / "prometheus").exists():
        raise SystemExit(
            f"repo_root does not look like the Prometheus repo: {repo_root}"
        )

    manifests_dir = repo_root / "data" / "microstructure" / "manifests"
    label_manifest_path = (
        manifests_dir / "microstructure_labels_aggtrades_v001__v002.json"
    )
    feature_manifest_path = (
        manifests_dir / "microstructure_features_aggtrades_v001__v002.json"
    )
    output_root = (
        args.output_root if args.output_root is not None
        else _resolve_output_root(repo_root)
    )

    print(f"[phase-4bn-e] repo_root       : {repo_root}", flush=True)
    print(f"[phase-4bn-e] code_commit_sha : {args.code_commit_sha}", flush=True)
    print(f"[phase-4bn-e] base_main_sha   : {args.base_main_sha}", flush=True)
    print(f"[phase-4bn-e] output_root     : {output_root}", flush=True)
    print(f"[phase-4bn-e] label_manifest  : {label_manifest_path}", flush=True)
    print(f"[phase-4bn-e] feature_manifest: {feature_manifest_path}", flush=True)

    label_manifest_sha = compute_file_sha256(label_manifest_path)
    feature_manifest_sha = compute_file_sha256(feature_manifest_path)
    label_manifest, feature_manifest, refs = discover_partition_refs(
        repo_root=repo_root,
        label_manifest_path=label_manifest_path,
        feature_manifest_path=feature_manifest_path,
    )
    _ = label_manifest
    _ = feature_manifest
    train_refs, validation_refs, test_refs = drift.filter_refs_to_supervised(refs)
    print(
        f"[phase-4bn-e] discovered      : train={len(train_refs)} "
        f"validation={len(validation_refs)} test_sealed={len(test_refs)}",
        flush=True,
    )

    if len(train_refs) != policy.EXPECTED_TRAIN_DATE_COUNT:
        raise SystemExit(
            f"expected {policy.EXPECTED_TRAIN_DATE_COUNT} train refs; "
            f"got {len(train_refs)}"
        )
    if len(validation_refs) != policy.EXPECTED_VALIDATION_DATE_COUNT:
        raise SystemExit(
            f"expected {policy.EXPECTED_VALIDATION_DATE_COUNT} validation refs; "
            f"got {len(validation_refs)}"
        )
    if len(test_refs) != policy.EXPECTED_TEST_DATE_COUNT:
        raise SystemExit(
            f"expected {policy.EXPECTED_TEST_DATE_COUNT} test refs; "
            f"got {len(test_refs)}"
        )

    accumulators = drift.make_accumulators()

    def _on_partition(*, split: str, ref: object, n_rows: int) -> None:
        utc = getattr(ref, "utc_date", "?")
        print(
            f"[phase-4bn-e] split={split} date={utc} rows={n_rows}",
            flush=True,
        )

    started_at = time.time()
    created_at_unix_ms = int(started_at * 1000)
    print("[phase-4bn-e] pass=1 exact-stats", flush=True)
    drift.run_pass1(accumulators, refs=refs, on_partition=_on_partition)
    print("[phase-4bn-e] pass=1 complete; initialising histograms", flush=True)
    drift.initialise_histograms(accumulators)
    print("[phase-4bn-e] pass=2 histograms", flush=True)
    drift.run_pass2(accumulators, refs=refs, on_partition=_on_partition)
    print("[phase-4bn-e] pass=2 complete; computing drift rows", flush=True)
    drift_rows = drift.compute_all_drift_rows(accumulators)
    duration_seconds = float(time.time() - started_at)

    output_root.mkdir(parents=True, exist_ok=True)

    csv_path, csv_sha, csv_side, csv_side_sha = report.write_csv_table(
        output_root=output_root,
        basename=_OUTPUT_DRIFT_SUMMARY_BASENAME,
        header=_drift_summary_header(),
        rows=[_drift_row_to_csv(r) for r in drift_rows],
    )

    overview_payload = _build_overview_payload(drift_rows)
    ov_path, ov_sha, ov_side, ov_side_sha = report.write_json_artefact(
        output_root=output_root,
        basename=_OUTPUT_DRIFT_OVERVIEW_BASENAME,
        payload=overview_payload,
    )

    output_basenames = {
        "feature_drift_summary": _OUTPUT_DRIFT_SUMMARY_BASENAME,
        "feature_drift_overview": _OUTPUT_DRIFT_OVERVIEW_BASENAME,
    }
    output_sha256s = {
        "feature_drift_summary": csv_sha,
        "feature_drift_overview": ov_sha,
    }
    output_sidecar_basenames = {
        "feature_drift_summary": csv_side.name,
        "feature_drift_overview": ov_side.name,
    }
    output_sidecar_sha256s = {
        "feature_drift_summary": csv_side_sha,
        "feature_drift_overview": ov_side_sha,
    }

    exact_command = (
        f"python scripts/phase4bn_e_run_feature_drift_v002.py "
        f"--repo-root {repo_root} "
        f"--code-commit-sha {args.code_commit_sha} "
        f"--base-main-sha {args.base_main_sha}"
    )

    manifest_payload = _build_manifest_payload(
        created_at_unix_ms=created_at_unix_ms,
        code_commit_sha=args.code_commit_sha,
        base_main_sha=args.base_main_sha,
        label_manifest_path=str(label_manifest_path.relative_to(repo_root)),
        feature_manifest_path=str(feature_manifest_path.relative_to(repo_root)),
        label_manifest_sha=label_manifest_sha,
        feature_manifest_sha=feature_manifest_sha,
        output_basenames=output_basenames,
        output_sha256s=output_sha256s,
        output_sidecar_basenames=output_sidecar_basenames,
        output_sidecar_sha256s=output_sidecar_sha256s,
        run_duration_seconds=duration_seconds,
        train_n_partitions=len(train_refs),
        validation_n_partitions=len(validation_refs),
        test_n_partitions_unused=len(test_refs),
        runtime_environment=_runtime_env_snapshot(),
        exact_command=exact_command,
    )
    mf_path, mf_sha, mf_side, mf_side_sha = report.write_json_artefact(
        output_root=output_root,
        basename=_OUTPUT_DRIFT_MANIFEST_BASENAME,
        payload=manifest_payload,
    )

    print(
        f"[phase-4bn-e] outputs written : {csv_path.name}, {ov_path.name}, "
        f"{mf_path.name}",
        flush=True,
    )
    print(f"[phase-4bn-e]   summary sha256  : {csv_sha}", flush=True)
    print(f"[phase-4bn-e]   overview sha256 : {ov_sha}", flush=True)
    print(f"[phase-4bn-e]   manifest sha256 : {mf_sha}", flush=True)
    print(f"[phase-4bn-e]   summary sidecar : {csv_side.name} sha256={csv_side_sha}", flush=True)
    print(f"[phase-4bn-e]   overview sidecar: {ov_side.name} sha256={ov_side_sha}", flush=True)
    print(f"[phase-4bn-e]   manifest sidecar: {mf_side.name} sha256={mf_side_sha}", flush=True)
    print(f"[phase-4bn-e] duration_sec    : {duration_seconds:.1f}", flush=True)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
