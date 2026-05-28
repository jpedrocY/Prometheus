"""Phase 4bn-B — Multi-day v002 ML-baseline runner.

Standalone offline orchestrator authorised by the Phase 4bn-B authorization
prompt. Implements exactly the Phase 4bn-A design over the existing
90-day v002 BTCUSDT feature/label family:

- 3-class direction classification ``{-1, 0, +1}`` (zero class preserved);
- horizons 15s and 60s only (1s / 5s deferred);
- train/validation only (test/final holdout sealed; 0 rows of test loaded);
- 45 computed v002 feature columns (17 lineage columns excluded);
- train-only mean/std fitting; validation transformed with the same fit;
- per-horizon censored-row exclusion and 60s boundary embargo enforced;
- four fixed-a-priori baselines (majority-prior, persistence past-return
  sign, multinomial logistic regression L2, regularized linear L1);
- descriptive ML metrics + §11.6-locked cost-commensurability summary;
- canonical Phase 4bb-F sidecars for every local gitignored output under
  ``data/research/microstructure/ml-baselines/phase-4bn-b/``.

Phase 4bn-B runs no strategy, no signals, no PnL, no backtest, no test
inference, no hyperparameter / threshold tuning, no feature ranking or
selection, no model selection through results, no manifest mutation, no
successor-state mutation, no acquisition, no endpoint, no credentials.
"""

from __future__ import annotations

import argparse
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
from prometheus.research.microstructure import ml_baseline_design_v002 as design  # noqa: E402
from prometheus.research.microstructure import ml_baseline_metrics_v002 as metrics  # noqa: E402
from prometheus.research.microstructure import ml_baseline_models_v002 as models  # noqa: E402
from prometheus.research.microstructure import ml_baseline_report_v002 as report  # noqa: E402
from prometheus.research.microstructure.canonical_paths import (  # noqa: E402
    compute_file_sha256,
)
from prometheus.research.microstructure.ml_baseline_dataset_v002 import (  # noqa: E402
    PartitionRef,
    StreamingClassPrior,
    StreamingStandardizer,
    discover_partition_refs,
    load_partition_matrices,
)


def _runtime_env_snapshot() -> dict[str, object]:
    return {
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "executable_basename": Path(sys.executable).name,
    }


def _run_horizon(
    *,
    horizon: str,
    train_refs: list[PartitionRef],
    validation_refs: list[PartitionRef],
    standardizer: StreamingStandardizer,
    class_prior: StreamingClassPrior,
) -> tuple[
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    int,
    int,
    int,
    int,
    int,
    int,
]:
    """Train and evaluate all baselines for a single horizon.

    Returns ``(train_metrics_by_family, validation_metrics_by_family,
    n_train_supervised, n_validation_supervised, n_train_censored,
    n_validation_censored, n_train_embargo, n_validation_embargo)``.
    """
    # ------------------------------------------------------------------ Pass A.
    # Train pass A: accumulate streaming standardizer + class prior. This
    # pass also re-loads each train partition once.
    n_train_supervised = 0
    n_train_censored = 0
    n_train_embargo = 0
    for ref in train_refs:
        pm = load_partition_matrices(ref=ref, horizon=horizon)
        n_train_supervised += pm.n_rows_supervised
        n_train_censored += pm.n_rows_censored
        n_train_embargo += pm.n_rows_embargoed
        standardizer.update(pm.feature_matrix)
        class_prior.update(pm.direction_labels)
        print(
            f"[phase-4bn-b] horizon={horizon} pass=fit-stats train "
            f"date={pm.utc_date} sup={pm.n_rows_supervised} "
            f"cens={pm.n_rows_censored} emb={pm.n_rows_embargoed}",
            flush=True,
        )
    standardizer.finalize()
    class_prior.finalize()

    # ------------------------------------------------------------------ Train.
    # Pass B: train trainers (SGD softmax with L2 and L1) over train rows.
    majority_baseline = models.fit_majority_class_baseline(
        train_class_counts=class_prior.counts,
        train_total=class_prior.total,
    )
    l2_trainer = models.build_l2_logistic_regression_trainer(
        n_features=len(design.COMPUTED_FEATURE_COLUMN_NAMES)
    )
    l1_trainer = models.build_l1_linear_classifier_trainer(
        n_features=len(design.COMPUTED_FEATURE_COLUMN_NAMES)
    )

    # Train evaluators (same family set as validation).
    train_evaluators: dict[str, models.StreamingEvaluator] = {}
    for fam in design.BASELINE_FAMILIES_INCLUDED:
        train_evaluators[fam] = models.StreamingEvaluator(
            family=fam, split=policy.TRAIN, horizon=horizon
        )

    for ref in train_refs:
        pm = load_partition_matrices(ref=ref, horizon=horizon)
        Xs = standardizer.transform(pm.feature_matrix)
        l2_trainer.partial_fit(Xs, pm.direction_labels)
        l1_trainer.partial_fit(Xs, pm.direction_labels)
        print(
            f"[phase-4bn-b] horizon={horizon} pass=train date={pm.utc_date} "
            f"rows={pm.n_rows_supervised}",
            flush=True,
        )

    l2_model = l2_trainer.finalize()
    l1_model = l1_trainer.finalize()

    # Train evaluation pass (predict on train rows; descriptive train fit).
    for ref in train_refs:
        pm = load_partition_matrices(ref=ref, horizon=horizon)
        Xs = standardizer.transform(pm.feature_matrix)
        # Majority baseline.
        maj_pred = majority_baseline.predict_batch(Xs)
        train_evaluators[design.BASELINE_MAJORITY_CLASS].update(
            y_true=pm.direction_labels,
            predicted_class=maj_pred.predicted_class,
            predicted_proba=maj_pred.predicted_proba,
        )
        # Persistence baseline.
        per_pred = models.PersistenceBaseline.predict_from_signs(pm.persistence_signs)
        train_evaluators[design.BASELINE_PERSISTENCE_PAST_RETURN].update(
            y_true=pm.direction_labels,
            predicted_class=per_pred.predicted_class,
            predicted_proba=per_pred.predicted_proba,
        )
        # L2 softmax regression.
        l2_pred = l2_model.predict_batch(Xs)
        train_evaluators[design.BASELINE_LOGISTIC_REGRESSION_L2].update(
            y_true=pm.direction_labels,
            predicted_class=l2_pred.predicted_class,
            predicted_proba=l2_pred.predicted_proba,
        )
        # L1 softmax regression.
        l1_pred = l1_model.predict_batch(Xs)
        train_evaluators[design.BASELINE_LINEAR_CLASSIFIER_L1].update(
            y_true=pm.direction_labels,
            predicted_class=l1_pred.predicted_class,
            predicted_proba=l1_pred.predicted_proba,
        )
        print(
            f"[phase-4bn-b] horizon={horizon} pass=train-eval date={pm.utc_date}",
            flush=True,
        )

    # ------------------------------------------------------------ Validation.
    validation_evaluators: dict[str, models.StreamingEvaluator] = {}
    calibration_summaries: dict[str, metrics.CalibrationSummary] = {}
    for fam in design.BASELINE_FAMILIES_INCLUDED:
        validation_evaluators[fam] = models.StreamingEvaluator(
            family=fam, split=policy.VALIDATION, horizon=horizon
        )
        calibration_summaries[fam] = metrics.CalibrationSummary(
            family=fam, split=policy.VALIDATION, horizon=horizon
        )

    n_val_supervised = 0
    n_val_censored = 0
    n_val_embargo = 0
    for ref in validation_refs:
        pm = load_partition_matrices(ref=ref, horizon=horizon)
        n_val_supervised += pm.n_rows_supervised
        n_val_censored += pm.n_rows_censored
        n_val_embargo += pm.n_rows_embargoed
        Xs = standardizer.transform(pm.feature_matrix)
        # Majority baseline.
        maj_pred = majority_baseline.predict_batch(Xs)
        validation_evaluators[design.BASELINE_MAJORITY_CLASS].update(
            y_true=pm.direction_labels,
            predicted_class=maj_pred.predicted_class,
            predicted_proba=maj_pred.predicted_proba,
            forward_log_returns=pm.forward_log_returns,
        )
        calibration_summaries[design.BASELINE_MAJORITY_CLASS].update(
            predicted_proba=maj_pred.predicted_proba,
            predicted_class=maj_pred.predicted_class,
            y_true=pm.direction_labels,
        )
        # Persistence baseline.
        per_pred = models.PersistenceBaseline.predict_from_signs(pm.persistence_signs)
        validation_evaluators[design.BASELINE_PERSISTENCE_PAST_RETURN].update(
            y_true=pm.direction_labels,
            predicted_class=per_pred.predicted_class,
            predicted_proba=per_pred.predicted_proba,
            forward_log_returns=pm.forward_log_returns,
        )
        calibration_summaries[design.BASELINE_PERSISTENCE_PAST_RETURN].update(
            predicted_proba=per_pred.predicted_proba,
            predicted_class=per_pred.predicted_class,
            y_true=pm.direction_labels,
        )
        # L2 softmax regression.
        l2_pred = l2_model.predict_batch(Xs)
        validation_evaluators[design.BASELINE_LOGISTIC_REGRESSION_L2].update(
            y_true=pm.direction_labels,
            predicted_class=l2_pred.predicted_class,
            predicted_proba=l2_pred.predicted_proba,
            forward_log_returns=pm.forward_log_returns,
        )
        calibration_summaries[design.BASELINE_LOGISTIC_REGRESSION_L2].update(
            predicted_proba=l2_pred.predicted_proba,
            predicted_class=l2_pred.predicted_class,
            y_true=pm.direction_labels,
        )
        # L1 softmax regression.
        l1_pred = l1_model.predict_batch(Xs)
        validation_evaluators[design.BASELINE_LINEAR_CLASSIFIER_L1].update(
            y_true=pm.direction_labels,
            predicted_class=l1_pred.predicted_class,
            predicted_proba=l1_pred.predicted_proba,
            forward_log_returns=pm.forward_log_returns,
        )
        calibration_summaries[design.BASELINE_LINEAR_CLASSIFIER_L1].update(
            predicted_proba=l1_pred.predicted_proba,
            predicted_class=l1_pred.predicted_class,
            y_true=pm.direction_labels,
        )
        print(
            f"[phase-4bn-b] horizon={horizon} pass=val-eval date={pm.utc_date} "
            f"sup={pm.n_rows_supervised} cens={pm.n_rows_censored} "
            f"emb={pm.n_rows_embargoed}",
            flush=True,
        )

    # Assemble per-horizon block.
    train_metrics_block: dict[str, dict[str, object]] = {}
    val_metrics_block: dict[str, dict[str, object]] = {}
    for fam in design.BASELINE_FAMILIES_INCLUDED:
        train_metrics_block[fam] = train_evaluators[fam].as_dict()
        val_metrics_block[fam] = validation_evaluators[fam].as_dict()
        # Calibration is validation-only (Phase 4bn-A §17).
        val_metrics_block[fam]["calibration"] = calibration_summaries[fam].as_dict()
        val_metrics_block[fam]["train_validation_stability"] = (
            metrics.summarize_train_validation_stability(
                train_metrics=train_metrics_block[fam],
                validation_metrics=val_metrics_block[fam],
            )
        )

    return (
        train_metrics_block,
        val_metrics_block,
        n_train_supervised,
        n_val_supervised,
        n_train_censored,
        n_val_censored,
        n_train_embargo,
        n_val_embargo,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 4bn-B multi-day v002 ML-baseline runner"
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
        else report.resolve_output_root(repo_root)
    )

    print(f"[phase-4bn-b] repo_root       : {repo_root}", flush=True)
    print(f"[phase-4bn-b] code_commit_sha : {args.code_commit_sha}", flush=True)
    print(f"[phase-4bn-b] output_root     : {output_root}", flush=True)
    print(
        f"[phase-4bn-b] label_manifest  : {label_manifest_path}",
        flush=True,
    )
    print(
        f"[phase-4bn-b] feature_manifest: {feature_manifest_path}",
        flush=True,
    )

    label_manifest_sha = compute_file_sha256(label_manifest_path)
    feature_manifest_sha = compute_file_sha256(feature_manifest_path)
    label_manifest, feature_manifest, refs = discover_partition_refs(
        repo_root=repo_root,
        label_manifest_path=label_manifest_path,
        feature_manifest_path=feature_manifest_path,
    )
    train_refs = [r for r in refs if r.split == policy.TRAIN]
    validation_refs = [r for r in refs if r.split == policy.VALIDATION]
    test_refs = [r for r in refs if r.split == policy.TEST]
    print(
        f"[phase-4bn-b] discovered      : train={len(train_refs)} "
        f"validation={len(validation_refs)} test_sealed={len(test_refs)}",
        flush=True,
    )

    started_at = time.time()
    created_at_unix_ms = int(started_at * 1000)

    # Run each included horizon end-to-end. Each horizon uses its own
    # standardizer and class prior so the per-horizon censoring + embargo
    # masks are honoured at fit time.
    per_horizon_results: dict[str, dict[str, dict[str, object]]] = {}
    train_supervised_rows_per_horizon: dict[str, int] = {}
    validation_supervised_rows_per_horizon: dict[str, int] = {}
    train_censored_rows_per_horizon: dict[str, int] = {}
    validation_censored_rows_per_horizon: dict[str, int] = {}
    train_embargo_total = 0
    validation_embargo_total = 0
    class_balance_blocks: dict[str, dict[str, object]] = {}
    metrics_csv_rows: list[list[object]] = []
    class_balance_csv_rows: list[list[object]] = []
    calibration_csv_rows: list[list[object]] = []

    last_standardizer_dict: dict[str, object] = {}
    for horizon in design.INCLUDED_HORIZONS:
        standardizer = StreamingStandardizer(
            n_features=len(design.COMPUTED_FEATURE_COLUMN_NAMES)
        )
        class_prior = StreamingClassPrior()
        (
            train_block,
            val_block,
            n_train_sup,
            n_val_sup,
            n_train_cens,
            n_val_cens,
            n_train_emb,
            n_val_emb,
        ) = _run_horizon(
            horizon=horizon,
            train_refs=train_refs,
            validation_refs=validation_refs,
            standardizer=standardizer,
            class_prior=class_prior,
        )
        per_horizon_results[horizon] = {"train": train_block, "validation": val_block}
        train_supervised_rows_per_horizon[horizon] = n_train_sup
        validation_supervised_rows_per_horizon[horizon] = n_val_sup
        train_censored_rows_per_horizon[horizon] = n_train_cens
        validation_censored_rows_per_horizon[horizon] = n_val_cens
        train_embargo_total += n_train_emb
        validation_embargo_total += n_val_emb
        last_standardizer_dict = standardizer.as_dict()

        # Class balance per (split × horizon).
        for split_name, n_sup, n_cens, n_emb, fam_block in (
            (policy.TRAIN, n_train_sup, n_train_cens, n_train_emb, train_block),
            (policy.VALIDATION, n_val_sup, n_val_cens, n_val_emb, val_block),
        ):
            # Recover class counts from the majority-class block (the
            # majority baseline emits the streaming class counts on the
            # confusion matrix's row sums).
            maj_block = fam_block[design.BASELINE_MAJORITY_CLASS]
            cm = maj_block["confusion_matrix"]
            assert isinstance(cm, dict)
            row_sums = {
                "down": sum(int(v) for v in cm["true_down"].values()),
                "flat": sum(int(v) for v in cm["true_flat"].values()),
                "up": sum(int(v) for v in cm["true_up"].values()),
            }
            class_balance_blocks[f"{split_name}:{horizon}"] = {
                "split": split_name,
                "horizon": horizon,
                "n_rows_total": int(n_sup + n_cens + n_emb),
                "n_rows_supervised": int(n_sup),
                "n_rows_censored": int(n_cens),
                "n_rows_embargoed": int(n_emb),
                "counts": row_sums,
                "prevalence": {
                    k: (v / n_sup) if n_sup else 0.0 for k, v in row_sums.items()
                },
            }
            class_balance_csv_rows.append(
                [
                    split_name,
                    horizon,
                    int(n_sup + n_cens + n_emb),
                    int(n_sup),
                    int(n_cens),
                    int(n_emb),
                    int(row_sums["down"]),
                    int(row_sums["flat"]),
                    int(row_sums["up"]),
                    (row_sums["down"] / n_sup) if n_sup else 0.0,
                    (row_sums["flat"] / n_sup) if n_sup else 0.0,
                    (row_sums["up"] / n_sup) if n_sup else 0.0,
                ]
            )

        # Metrics CSV rows: one per (family, split, metric).
        for fam in design.BASELINE_FAMILIES_INCLUDED:
            for r in metrics.flatten_metric_rows(
                family=fam,
                train_metrics=train_block[fam],
                validation_metrics=val_block[fam],
            ):
                metrics_csv_rows.append(
                    [
                        r["family"],
                        r["split"],
                        r["horizon"],
                        r["metric_name"],
                        r["metric_value"],
                    ]
                )
            # Calibration rows for validation.
            cal = val_block[fam].get("calibration")
            if isinstance(cal, dict) and isinstance(cal.get("bins"), list):
                for b in cal["bins"]:
                    calibration_csv_rows.append(
                        [
                            fam,
                            policy.VALIDATION,
                            horizon,
                            b["bin_low"],
                            b["bin_high"],
                            b["n_rows"],
                            b["mean_max_predicted_proba"],
                            b["empirical_accuracy"],
                            b["reliability_gap"],
                        ]
                    )

    duration_seconds = float(time.time() - started_at)

    # Write outputs (JSON artefacts first; CSV tables second). Each gets a
    # canonical Phase 4bb-F sidecar paired beside it.
    output_root.mkdir(parents=True, exist_ok=True)
    sha256s: dict[str, str] = {}
    sidecar_basenames: dict[str, str] = {}
    sidecar_sha256s: dict[str, str] = {}
    basenames: dict[str, str] = {}

    feature_schema_payload = report.build_feature_schema_payload()
    _, fs_sha, fs_side, fs_side_sha = report.write_json_artefact(
        output_root=output_root,
        basename=design.OUTPUT_FEATURE_SCHEMA_BASENAME,
        payload=feature_schema_payload,
    )
    sha256s["feature_schema"] = fs_sha
    sidecar_sha256s["feature_schema"] = fs_side_sha
    sidecar_basenames["feature_schema"] = fs_side.name
    basenames["feature_schema"] = design.OUTPUT_FEATURE_SCHEMA_BASENAME

    transform_payload = report.build_transform_metadata_payload(
        standardizer_dict=last_standardizer_dict,
        train_n_partitions=len(train_refs),
        train_n_supervised_rows_per_horizon=train_supervised_rows_per_horizon,
    )
    _, tr_sha, tr_side, tr_side_sha = report.write_json_artefact(
        output_root=output_root,
        basename=design.OUTPUT_TRANSFORM_METADATA_BASENAME,
        payload=transform_payload,
    )
    sha256s["transform_metadata"] = tr_sha
    sidecar_sha256s["transform_metadata"] = tr_side_sha
    sidecar_basenames["transform_metadata"] = tr_side.name
    basenames["transform_metadata"] = design.OUTPUT_TRANSFORM_METADATA_BASENAME

    per_horizon_payload = report.build_per_horizon_summary_payload(
        per_horizon=per_horizon_results,
        class_balance_by_split_horizon=class_balance_blocks,
    )
    _, ph_sha, ph_side, ph_side_sha = report.write_json_artefact(
        output_root=output_root,
        basename=design.OUTPUT_PER_HORIZON_SUMMARY_BASENAME,
        payload=per_horizon_payload,
    )
    sha256s["per_horizon_summary"] = ph_sha
    sidecar_sha256s["per_horizon_summary"] = ph_side_sha
    sidecar_basenames["per_horizon_summary"] = ph_side.name
    basenames["per_horizon_summary"] = design.OUTPUT_PER_HORIZON_SUMMARY_BASENAME

    # CSV tables.
    _, mt_sha, mt_side, mt_side_sha = report.write_csv_table(
        output_root=output_root,
        basename=design.OUTPUT_METRICS_TABLE_BASENAME,
        header=report.metrics_csv_header(),
        rows=metrics_csv_rows,
    )
    sha256s["metrics_csv"] = mt_sha
    sidecar_sha256s["metrics_csv"] = mt_side_sha
    sidecar_basenames["metrics_csv"] = mt_side.name
    basenames["metrics_csv"] = design.OUTPUT_METRICS_TABLE_BASENAME

    _, cb_sha, cb_side, cb_side_sha = report.write_csv_table(
        output_root=output_root,
        basename=design.OUTPUT_CLASS_BALANCE_TABLE_BASENAME,
        header=report.class_balance_csv_header(),
        rows=class_balance_csv_rows,
    )
    sha256s["class_balance_csv"] = cb_sha
    sidecar_sha256s["class_balance_csv"] = cb_side_sha
    sidecar_basenames["class_balance_csv"] = cb_side.name
    basenames["class_balance_csv"] = design.OUTPUT_CLASS_BALANCE_TABLE_BASENAME

    _, cl_sha, cl_side, cl_side_sha = report.write_csv_table(
        output_root=output_root,
        basename=design.OUTPUT_CALIBRATION_TABLE_BASENAME,
        header=report.calibration_csv_header(),
        rows=calibration_csv_rows,
    )
    sha256s["calibration_csv"] = cl_sha
    sidecar_sha256s["calibration_csv"] = cl_side_sha
    sidecar_basenames["calibration_csv"] = cl_side.name
    basenames["calibration_csv"] = design.OUTPUT_CALIBRATION_TABLE_BASENAME

    # Run manifest (must be written last so that it can record the SHA256s of
    # the other artefacts produced in this run).
    run_manifest_payload = report.build_run_manifest_payload(
        created_at_unix_ms=created_at_unix_ms,
        code_commit_sha=args.code_commit_sha,
        label_manifest_sha256=label_manifest_sha,
        feature_manifest_sha256=feature_manifest_sha,
        label_manifest_path=str(label_manifest_path.relative_to(repo_root)),
        feature_manifest_path=str(feature_manifest_path.relative_to(repo_root)),
        output_basenames=basenames,
        output_sha256s=sha256s,
        output_sidecar_basenames=sidecar_basenames,
        output_sidecar_sha256s=sidecar_sha256s,
        run_duration_seconds=duration_seconds,
        train_n_partitions=len(train_refs),
        validation_n_partitions=len(validation_refs),
        test_n_partitions_unused=len(test_refs),
        train_supervised_rows_per_horizon=train_supervised_rows_per_horizon,
        validation_supervised_rows_per_horizon=validation_supervised_rows_per_horizon,
        train_censored_rows_per_horizon=train_censored_rows_per_horizon,
        validation_censored_rows_per_horizon=validation_censored_rows_per_horizon,
        train_embargoed_rows=train_embargo_total,
        validation_embargoed_rows=validation_embargo_total,
        test_rows_loaded=0,
        runtime_environment=_runtime_env_snapshot(),
    )
    _, rm_sha, rm_side, rm_side_sha = report.write_json_artefact(
        output_root=output_root,
        basename=design.OUTPUT_RUN_MANIFEST_BASENAME,
        payload=run_manifest_payload,
    )
    sha256s["run_manifest"] = rm_sha
    sidecar_sha256s["run_manifest"] = rm_side_sha
    sidecar_basenames["run_manifest"] = rm_side.name
    basenames["run_manifest"] = design.OUTPUT_RUN_MANIFEST_BASENAME

    print(f"[phase-4bn-b] outputs written : {len(sha256s)} JSON/CSV files", flush=True)
    for key, sha in sha256s.items():
        print(
            f"[phase-4bn-b]   {key:>22s} sha256={sha} sidecar_sha={sidecar_sha256s[key]}",
            flush=True,
        )
    print(f"[phase-4bn-b] duration_sec    : {duration_seconds:.1f}", flush=True)
    # Pin down a few summary numbers for the operator.
    print(
        f"[phase-4bn-b] train supervised rows per horizon: "
        f"{train_supervised_rows_per_horizon}",
        flush=True,
    )
    print(
        f"[phase-4bn-b] validation supervised rows per horizon: "
        f"{validation_supervised_rows_per_horizon}",
        flush=True,
    )
    # Carry-forward sanity on the test-holdout-not-loaded invariant.
    # (We never opened any test parquet in this run.)
    _ = label_manifest  # used by _discover_partition_refs side-effects only
    _ = feature_manifest
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
