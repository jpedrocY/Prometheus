"""Phase 4bm-W — descriptive diagnostics aggregation, verdict, and report I/O.

Aggregates the per-partition summaries produced by
:mod:`prometheus.research.microstructure.descriptive_diagnostics_v002` into
per-split and global descriptive summaries, derives a report-level descriptive
diagnostics verdict, and writes local gitignored diagnostic outputs (summary
JSON + paired canonical Phase 4bb-F sidecar, per-split / per-day CSV tables,
and a diagnostics manifest + sidecar) under an approved gitignored research
namespace (``data/research/microstructure/diagnostics/phase-4bm-w/``).

Verdict semantics (descriptive-only; never an ML / strategy / backtest
readiness signal):

- ``DESCRIPTIVE_DIAGNOSTICS_PASS`` — all required descriptive diagnostics
  completed and no blocking structural issue and no caveat was found.
- ``DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`` — completed with non-blocking
  caveats (e.g. the known envelope-terminal censoring asymmetry, boundary
  embargo exclusions, or the approximate-quantile method).
- ``DESCRIPTIVE_DIAGNOSTICS_FAIL`` — at least one blocking structural issue.
- ``DESCRIPTIVE_DIAGNOSTICS_ERROR`` — execution could not complete (raised by
  the caller around :func:`build_report`).

Phase 4bm-W runs descriptive diagnostics only. This module mutates no
manifest, no successor-state artefact, and no ``data/microstructure/``
artefact; it writes only into the research-output namespace.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import diagnostics_split_policy_v002 as policy
from .canonical_paths import (
    compose_canonical_sidecar_body,
    compute_file_sha256,
)
from .descriptive_diagnostics_v002 import (
    EXPECTED_CENSORED_PER_HORIZON,
    EXPECTED_FEATURE_CONFIG_HASH,
    EXPECTED_INVALID_PRICE_ROW_COUNT,
    EXPECTED_LABEL_CONFIG_HASH,
    EXPECTED_PARTITION_COUNT,
    EXPECTED_TOTAL_ROW_COUNT,
    HISTOGRAM_BIN_WIDTH,
    HISTOGRAM_RANGE,
    HORIZONS,
    DiagnosticsRun,
    HorizonStats,
    PartitionSummary,
)

VERDICT_PASS = "DESCRIPTIVE_DIAGNOSTICS_PASS"
VERDICT_PASS_WITH_CAVEATS = "DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS"
VERDICT_FAIL = "DESCRIPTIVE_DIAGNOSTICS_FAIL"
VERDICT_ERROR = "DESCRIPTIVE_DIAGNOSTICS_ERROR"

PHASE_ID = "4bm-w"
DIAGNOSTICS_SCHEMA_VERSION = "v001"


class DiagnosticsReportError(RuntimeError):
    """Raised when report assembly or output writing fails."""


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


@dataclass
class SplitAggregate:
    """Per-split aggregate of partition summaries."""

    split: str
    partition_count: int = 0
    row_count: int = 0
    embargo_excluded: int = 0
    invalid_price: int = 0
    any_censored: int = 0
    boundary_crossing_per_horizon: dict[str, int] | None = None
    horizon_stats: dict[str, HorizonStats] | None = None


def _new_split_aggregate(split: str) -> SplitAggregate:
    agg = SplitAggregate(split=split)
    agg.boundary_crossing_per_horizon = dict.fromkeys(HORIZONS, 0)
    agg.horizon_stats = {h: HorizonStats() for h in HORIZONS}
    for hs in agg.horizon_stats.values():
        hs.ensure_initialised()
    return agg


def aggregate_by_split(
    summaries: list[PartitionSummary],
) -> dict[str, SplitAggregate]:
    """Merge per-day partition summaries into per-split aggregates."""
    out = {s: _new_split_aggregate(s) for s in policy.SPLIT_NAMES}
    for ps in summaries:
        agg = out[ps.split]
        agg.partition_count += 1
        agg.row_count += ps.row_count
        agg.embargo_excluded += ps.embargo_count
        agg.invalid_price += ps.n_invalid_price
        agg.any_censored += ps.n_any_censored
        assert agg.boundary_crossing_per_horizon is not None
        assert agg.horizon_stats is not None
        for h in HORIZONS:
            agg.boundary_crossing_per_horizon[h] += (
                ps.boundary_crossing_per_horizon[h]
            )
            agg.horizon_stats[h].merge(ps.horizon_stats[h])
    return out


def _sum_structural(summaries: list[PartitionSummary]) -> dict[str, int]:
    """Sum the structural-violation counters across all partitions."""
    totals = {
        "any_censored_flag_mismatch": 0,
        "row_index_violation": 0,
        "src_ne_feature_ts": 0,
        "out_of_partition_day": 0,
        "split_assignment_mismatch": 0,
        "invalid_price": 0,
        "censor_rule_mismatch": 0,
        "censored_row_not_null": 0,
        "direction_domain_violation": 0,
        "direction_sign_mismatch": 0,
        "symbol_violation": 0,
        "dataset_version_violation": 0,
        "label_config_hash_violation": 0,
    }
    for ps in summaries:
        totals["any_censored_flag_mismatch"] += ps.n_any_censored_flag_mismatch
        totals["row_index_violation"] += ps.n_row_index_violation
        totals["src_ne_feature_ts"] += ps.n_src_ne_feature_ts
        totals["out_of_partition_day"] += ps.n_out_of_partition_day
        totals["split_assignment_mismatch"] += ps.n_split_assignment_mismatch
        totals["invalid_price"] += ps.n_invalid_price
        totals["symbol_violation"] += 0 if ps.symbol_ok else 1
        totals["dataset_version_violation"] += 0 if ps.dataset_version_ok else 1
        totals["label_config_hash_violation"] += 0 if ps.label_config_hash_ok else 1
        for h in HORIZONS:
            hs = ps.horizon_stats[h]
            totals["censor_rule_mismatch"] += hs.n_censor_rule_mismatch
            totals["censored_row_not_null"] += hs.n_censored_not_null
            totals["direction_domain_violation"] += hs.n_dir_domain_violation
            totals["direction_sign_mismatch"] += hs.n_dir_sign_mismatch
    return totals


def _sum_alignment(run: DiagnosticsRun) -> dict[str, int]:
    totals = {
        "row_count_mismatch_days": 0,
        "row_index_mismatch": 0,
        "agg_trade_id_mismatch": 0,
        "feature_timestamp_mismatch": 0,
        "source_transact_time_mismatch": 0,
        "feature_config_hash_mismatch_days": 0,
    }
    for al in run.alignment_summaries:
        totals["row_count_mismatch_days"] += 0 if al.row_count_match else 1
        totals["row_index_mismatch"] += al.n_row_index_mismatch
        totals["agg_trade_id_mismatch"] += al.n_agg_trade_id_mismatch
        totals["feature_timestamp_mismatch"] += al.n_feature_timestamp_mismatch
        totals["source_transact_time_mismatch"] += (
            al.n_source_transact_time_mismatch
        )
        totals["feature_config_hash_mismatch_days"] += (
            0 if al.feature_config_hash_match else 1
        )
    return totals


def _global_censored_per_horizon(
    summaries: list[PartitionSummary],
) -> dict[str, int]:
    out = dict.fromkeys(HORIZONS, 0)
    for ps in summaries:
        for h in HORIZONS:
            out[h] += ps.horizon_stats[h].n_censored
    return out


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------


@dataclass
class VerdictResult:
    verdict: str
    blocking_failures: list[str]
    caveats: list[str]


def derive_verdict(
    run: DiagnosticsRun,
    split_aggs: Mapping[str, SplitAggregate],
    structural: Mapping[str, int],
    alignment: Mapping[str, int],
    global_censored: Mapping[str, int],
) -> VerdictResult:
    """Derive the descriptive verdict from aggregated diagnostics (no tuning)."""
    blocking: list[str] = []
    caveats: list[str] = []

    total_rows = sum(a.row_count for a in split_aggs.values())
    if total_rows != EXPECTED_TOTAL_ROW_COUNT:
        blocking.append(
            f"total_row_count {total_rows} != expected {EXPECTED_TOTAL_ROW_COUNT}"
        )
    total_partitions = sum(a.partition_count for a in split_aggs.values())
    if total_partitions != EXPECTED_PARTITION_COUNT:
        blocking.append(
            f"partition_count {total_partitions} != {EXPECTED_PARTITION_COUNT}"
        )
    for label, count in (
        ("label_partition", run.label_partition_count_on_disk),
        ("feature_partition", run.feature_partition_count_on_disk),
        ("label_sidecar", run.label_sidecar_count_on_disk),
        ("feature_sidecar", run.feature_sidecar_count_on_disk),
    ):
        if count != EXPECTED_PARTITION_COUNT:
            blocking.append(f"{label}_count_on_disk {count} != 90")

    if split_aggs["train"].partition_count != policy.EXPECTED_TRAIN_DATE_COUNT:
        blocking.append("train partition count != 45")
    if (
        split_aggs["validation"].partition_count
        != policy.EXPECTED_VALIDATION_DATE_COUNT
    ):
        blocking.append("validation partition count != 30")
    if split_aggs["test"].partition_count != policy.EXPECTED_TEST_DATE_COUNT:
        blocking.append("test partition count != 15")

    # Structural integrity (every counter must be zero).
    for key, val in structural.items():
        if val != 0:
            blocking.append(f"structural.{key} = {val} (expected 0)")
    for key, val in alignment.items():
        if val != 0:
            blocking.append(f"alignment.{key} = {val} (expected 0)")

    if structural["invalid_price"] != EXPECTED_INVALID_PRICE_ROW_COUNT:
        blocking.append("invalid_price_row_count != 0")

    # Global per-horizon censored counts must match the recorded manifest.
    for h in HORIZONS:
        if global_censored[h] != EXPECTED_CENSORED_PER_HORIZON[h]:
            blocking.append(
                f"censored[{h}] {global_censored[h]} != "
                f"{EXPECTED_CENSORED_PER_HORIZON[h]}"
            )

    # Non-blocking caveats (known, documented asymmetries / methods).
    total_censored = sum(global_censored.values())
    if total_censored > 0:
        test_hs = split_aggs["test"].horizon_stats
        assert test_hs is not None
        test_censored = sum(test_hs[h].n_censored for h in HORIZONS)
        caveats.append(
            "envelope-terminal censoring present "
            f"(total {total_censored}; {test_censored} in test split); "
            "horizon availability is asymmetric across splits — descriptive only"
        )
    total_embargo = sum(a.embargo_excluded for a in split_aggs.values())
    if total_embargo > 0:
        caveats.append(
            f"60s boundary embargo excludes {total_embargo} earlier-split rows "
            "(descriptive estimate; per-row masks only, no parquet rewrite)"
        )
    caveats.append(
        "forward-return quantiles are approximate (fixed-width histogram, "
        f"range +/-{HISTOGRAM_RANGE}, bin width {HISTOGRAM_BIN_WIDTH:g}); "
        "exact additive moments (mean/std/min/max) are not approximate"
    )
    # Manifest historical authorization flags predate this phase's prompt.
    if run.label_manifest.get("diagnostics_authorized") is False:
        caveats.append(
            "v002 label manifest records diagnostics_authorized=false "
            "(historical flag predating Phase 4bm-W; authorization derives from "
            "the Phase 4bm-W operator prompt, not the manifest; manifest unmutated)"
        )

    if blocking:
        return VerdictResult(VERDICT_FAIL, blocking, caveats)
    if caveats:
        return VerdictResult(VERDICT_PASS_WITH_CAVEATS, blocking, caveats)
    return VerdictResult(VERDICT_PASS, blocking, caveats)


# ---------------------------------------------------------------------------
# Payload assembly
# ---------------------------------------------------------------------------


def _split_aggregate_payload(agg: SplitAggregate) -> dict[str, Any]:
    assert agg.horizon_stats is not None
    assert agg.boundary_crossing_per_horizon is not None
    return {
        "split": agg.split,
        "partition_count": agg.partition_count,
        "row_count": agg.row_count,
        "embargo_excluded_rows": agg.embargo_excluded,
        "invalid_price_rows": agg.invalid_price,
        "any_censored_rows": agg.any_censored,
        "boundary_crossing_per_horizon": dict(agg.boundary_crossing_per_horizon),
        "per_horizon": {h: agg.horizon_stats[h].as_dict() for h in HORIZONS},
    }


def build_payload(
    run: DiagnosticsRun,
    *,
    created_at_unix_ms: int,
    code_commit_sha: str,
) -> dict[str, Any]:
    """Build the deterministic descriptive-diagnostics summary payload."""
    split_aggs = aggregate_by_split(run.partition_summaries)
    structural = _sum_structural(run.partition_summaries)
    alignment = _sum_alignment(run)
    global_censored = _global_censored_per_horizon(run.partition_summaries)
    verdict = derive_verdict(
        run, split_aggs, structural, alignment, global_censored
    )

    per_day = [
        {
            "utc_date": ps.utc_date,
            "split": ps.split,
            "row_count": ps.row_count,
            "any_censored_rows": ps.n_any_censored,
            "invalid_price_rows": ps.n_invalid_price,
            "embargo_excluded_rows": ps.embargo_count,
            "censored_per_horizon": {
                h: ps.horizon_stats[h].n_censored for h in HORIZONS
            },
        }
        for ps in sorted(run.partition_summaries, key=lambda p: p.utc_date)
    ]

    return {
        "phase_id": PHASE_ID,
        "diagnostics_schema_version": DIAGNOSTICS_SCHEMA_VERSION,
        "created_at_unix_ms": created_at_unix_ms,
        "code_commit_sha": code_commit_sha,
        "diagnostics_verdict": verdict.verdict,
        "verdict_blocking_failures": verdict.blocking_failures,
        "verdict_caveats": verdict.caveats,
        "descriptive_only": True,
        "is_ml_readiness": False,
        "is_strategy_readiness": False,
        "is_backtest_readiness": False,
        "dataset_identity": {
            "label_family_id": "microstructure_labels_aggtrades_v001",
            "feature_family_id": "microstructure_features_aggtrades_v001",
            "dataset_version": "v002",
            "symbol": "BTCUSDT",
            "date_start": policy.TRAIN_START_DATE,
            "date_end": policy.TEST_END_DATE,
            "expected_total_rows": EXPECTED_TOTAL_ROW_COUNT,
            "expected_partition_count": EXPECTED_PARTITION_COUNT,
            "label_config_hash": EXPECTED_LABEL_CONFIG_HASH,
            "feature_config_hash": EXPECTED_FEATURE_CONFIG_HASH,
            "envelope_terminal_unix_ms": policy.ENVELOPE_TERMINAL_UNIX_MS,
            "horizons": list(HORIZONS),
        },
        "split_policy": policy.SplitPolicySnapshot().as_dict(),
        "inventory": {
            "total_row_count_observed": sum(
                a.row_count for a in split_aggs.values()
            ),
            "total_partition_count_observed": sum(
                a.partition_count for a in split_aggs.values()
            ),
            "label_partition_count_on_disk": run.label_partition_count_on_disk,
            "feature_partition_count_on_disk": run.feature_partition_count_on_disk,
            "label_sidecar_count_on_disk": run.label_sidecar_count_on_disk,
            "feature_sidecar_count_on_disk": run.feature_sidecar_count_on_disk,
        },
        "split_summaries": {
            s: _split_aggregate_payload(split_aggs[s]) for s in policy.SPLIT_NAMES
        },
        "structural_violation_totals": dict(structural),
        "alignment_violation_totals": dict(alignment),
        "global_censored_per_horizon_observed": dict(global_censored),
        "global_censored_per_horizon_expected": dict(EXPECTED_CENSORED_PER_HORIZON),
        "embargo_summary": {
            "minimum_boundary_embargo_seconds": (
                policy.MIN_BOUNDARY_EMBARGO_SECONDS
            ),
            "boundary_train_validation_ms": policy.BOUNDARY_TRAIN_VALIDATION_MS,
            "boundary_validation_test_ms": policy.BOUNDARY_VALIDATION_TEST_MS,
            "total_embargo_excluded_rows": sum(
                a.embargo_excluded for a in split_aggs.values()
            ),
            "boundary_crossing_rule": "exclude_from_earlier_split",
        },
        "holdout_protection": {
            "test_holdout_used_for_tuning_or_design": False,
            "test_holdout_used_for_feature_selection": False,
            "test_holdout_used_for_model_selection": False,
            "test_holdout_used_for_threshold_tuning": False,
            "test_holdout_used_for_diagnostic_iteration": False,
            "no_shuffle": True,
            "no_random_split": True,
            "no_bootstrap": True,
            "test_holdout_summarised_descriptively_only": True,
        },
        "non_authorization": {
            "ran_ml": False,
            "selected_models": False,
            "ranked_features": False,
            "selected_features": False,
            "tuned_hyperparameters": False,
            "tuned_thresholds": False,
            "designed_strategy": False,
            "ran_backtests": False,
            "ran_walk_forward": False,
            "acquired_data": False,
            "called_endpoints": False,
            "used_credentials": False,
            "mutated_manifest": False,
            "mutated_successor_state": False,
            "committed_data_microstructure": False,
            "authorized_phase_4bm_x": False,
        },
        "per_day": per_day,
    }


# ---------------------------------------------------------------------------
# Output writing (research namespace; gitignored; never data/microstructure)
# ---------------------------------------------------------------------------


def _write_atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def _write_sidecar(json_path: Path) -> tuple[Path, str]:
    sha = compute_file_sha256(json_path)
    body = compose_canonical_sidecar_body(
        json_sha256_hex=sha, json_basename=json_path.name
    )
    sidecar = json_path.with_suffix(json_path.suffix + ".sha256")
    _write_atomic_bytes(sidecar, body)
    return sidecar, sha


@dataclass
class WrittenOutputs:
    summary_json_path: Path
    summary_json_sha256: str
    summary_sidecar_path: Path
    summary_sidecar_sha256: str
    manifest_json_path: Path
    manifest_json_sha256: str
    manifest_sidecar_path: Path
    manifest_sidecar_sha256: str
    table_paths: list[Path]


def _write_csv_tables(
    output_root: Path, payload: Mapping[str, Any]
) -> list[Path]:
    tables_dir = output_root / "descriptive_diagnostics_tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    per_day_path = tables_dir / "per_day_inventory.csv"
    rows = payload["per_day"]
    with per_day_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "utc_date",
                "split",
                "row_count",
                "any_censored_rows",
                "invalid_price_rows",
                "embargo_excluded_rows",
                "censored_1s",
                "censored_5s",
                "censored_15s",
                "censored_60s",
            ]
        )
        for r in rows:
            cph = r["censored_per_horizon"]
            w.writerow(
                [
                    r["utc_date"],
                    r["split"],
                    r["row_count"],
                    r["any_censored_rows"],
                    r["invalid_price_rows"],
                    r["embargo_excluded_rows"],
                    cph["1s"],
                    cph["5s"],
                    cph["15s"],
                    cph["60s"],
                ]
            )
    paths.append(per_day_path)

    split_path = tables_dir / "per_split_horizon_summary.csv"
    with split_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "split",
                "horizon",
                "n_rows",
                "n_censored",
                "n_return_nonnull",
                "n_return_null",
                "n_return_pos",
                "n_return_neg",
                "n_return_zero",
                "return_mean",
                "return_std",
                "return_min",
                "return_max",
                "dir_plus_one",
                "dir_zero",
                "dir_minus_one",
                "dir_null",
            ]
        )
        for split in policy.SPLIT_NAMES:
            ph = payload["split_summaries"][split]["per_horizon"]
            for h in HORIZONS:
                d = ph[h]
                db = d["direction_balance"]
                w.writerow(
                    [
                        split,
                        h,
                        d["n_rows"],
                        d["n_censored"],
                        d["n_return_nonnull"],
                        d["n_return_null"],
                        d["n_return_pos"],
                        d["n_return_neg"],
                        d["n_return_zero"],
                        d["return_mean"],
                        d["return_std"],
                        d["return_min"],
                        d["return_max"],
                        db["plus_one"],
                        db["zero"],
                        db["minus_one"],
                        db["null"],
                    ]
                )
    paths.append(split_path)
    return paths


def write_outputs(
    output_root: Path,
    payload: Mapping[str, Any],
    *,
    created_at_unix_ms: int,
    code_commit_sha: str,
) -> WrittenOutputs:
    """Write summary JSON + sidecar, CSV tables, and a diagnostics manifest.

    All outputs live under *output_root* (the gitignored research namespace).
    Refuses to write anywhere under ``data/microstructure/``.
    """
    resolved = output_root.resolve(strict=False)
    if "microstructure" in resolved.parts and "research" not in resolved.parts:
        raise DiagnosticsReportError(
            f"refusing to write diagnostics under {output_root} "
            "(must be a research-output namespace, not data/microstructure)"
        )
    output_root.mkdir(parents=True, exist_ok=True)

    summary_json = output_root / "descriptive_diagnostics_summary.json"
    body = (
        json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode("ascii")
    _write_atomic_bytes(summary_json, body)
    summary_sidecar, summary_sha = _write_sidecar(summary_json)
    summary_sidecar_sha = compute_file_sha256(summary_sidecar)

    table_paths = _write_csv_tables(output_root, payload)

    manifest_outputs = [
        (summary_json, summary_sha),
        (summary_sidecar, summary_sidecar_sha),
    ]
    for tp in table_paths:
        manifest_outputs.append((tp, compute_file_sha256(tp)))

    manifest_payload = {
        "phase_id": PHASE_ID,
        "diagnostics_schema_version": DIAGNOSTICS_SCHEMA_VERSION,
        "created_at_unix_ms": created_at_unix_ms,
        "code_commit_sha": code_commit_sha,
        "diagnostics_verdict": payload["diagnostics_verdict"],
        "output_namespace": "data/research/microstructure/diagnostics/phase-4bm-w",
        "outputs": [
            {
                "basename": p.name,
                "relative_path": p.name
                if p.parent == output_root
                else f"{p.parent.name}/{p.name}",
                "sha256": sha,
                "size_bytes": p.stat().st_size,
            }
            for p, sha in manifest_outputs
        ],
    }
    manifest_json = output_root / "diagnostics_manifest.json"
    manifest_body = (
        json.dumps(manifest_payload, sort_keys=True, indent=2, ensure_ascii=True)
        + "\n"
    ).encode("ascii")
    _write_atomic_bytes(manifest_json, manifest_body)
    manifest_sidecar, manifest_sha = _write_sidecar(manifest_json)
    manifest_sidecar_sha = compute_file_sha256(manifest_sidecar)

    return WrittenOutputs(
        summary_json_path=summary_json,
        summary_json_sha256=summary_sha,
        summary_sidecar_path=summary_sidecar,
        summary_sidecar_sha256=summary_sidecar_sha,
        manifest_json_path=manifest_json,
        manifest_json_sha256=manifest_sha,
        manifest_sidecar_path=manifest_sidecar,
        manifest_sidecar_sha256=manifest_sidecar_sha,
        table_paths=table_paths,
    )
