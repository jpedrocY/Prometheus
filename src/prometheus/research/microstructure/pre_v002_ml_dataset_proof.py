"""Phase 4bn-AF — pre-v002 ML dataset builder proof schema (pure, offline).

Inert, machine-checkable **proof-schema builders and validators** over synthetic
inputs only. Defines the shape a future data-reading builder's leakage /
split-integrity proof (and its Phase 4bb-F canonical sidecar) would take, without
building a dataset, reading any data, or writing any sidecar.

This module performs **no I/O**: it reads and writes no files, resolves no path,
creates no directory, and never writes a sidecar. It imports only the standard
library, the inert contract-constant module, the inert split-policy artefact, and
the builder skeleton's error type.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import pre_v002_ml_dataset_contract as contract
from . import pre_v002_split_policy as split_policy
from .pre_v002_ml_dataset_builder import PreV002MlDatasetError

# ---------------------------------------------------------------------------
# Budget-preflight caps (Phase 4bn-L; interface-shape only, never measured here)
# ---------------------------------------------------------------------------

DERIVED_FOOTPRINT_WARN_GIB = 75
DERIVED_FOOTPRINT_HARD_GIB = 125
TOTAL_DERIVED_STACK_WARN_GIB = 250
TOTAL_DERIVED_STACK_HARD_GIB = 300
RUNTIME_WARN_HOURS = 4
RUNTIME_HARD_HOURS = 8
TEMP_WARN_GIB = 50
TEMP_HARD_GIB = 100
D_DRIVE_MIN_FREE_GIB_BEFORE = 500
D_DRIVE_FAIL_CLOSED_DURING_GIB = 350


# ---------------------------------------------------------------------------
# Proof dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SplitProof:
    """Split-integrity proof section."""

    split_policy_name: str = split_policy.SPLIT_POLICY_NAME
    split_policy_module_path: str = contract.SPLIT_POLICY_MODULE_PATH
    split_policy_commit_sha: str = "unknown"
    train_date_count: int = 214
    train_validation_embargo_count: int = 1
    validation_date_count: int = 45
    validation_holdout_embargo_count: int = 1
    holdout_date_count: int = 14
    no_missing_in_segment_dates: bool = True
    no_duplicate_in_segment_dates: bool = True
    no_multi_assigned_in_segment_dates: bool = True
    no_embargo_date_used: bool = True
    out_of_segment_dates: int = 0
    v002_terminal_window_read: bool = False
    sealed_test_split_touched: bool = False
    test_rows_loaded: int = 0
    no_random: bool = True
    no_shuffle: bool = True
    no_kfold: bool = True
    no_bootstrap: bool = True
    deterministic_assignment_by_source_transact_time_ms_utc_date: bool = True
    per_horizon_zero_earlier_split_boundary_crossing_rows: bool = True


@dataclass(frozen=True)
class AlignmentProof:
    """Strict feature/label key-alignment proof section."""

    strict_positional_alignment: bool = True
    key_alignment_row_count: int = 0
    mismatched_rows: int = 0
    join_repair_used: bool = False
    reorder_used: bool = False
    fill_used: bool = False
    tolerance_merge_used: bool = False


@dataclass(frozen=True)
class FilteringProof:
    """Target null/censored/invalid filtering proof section (by split)."""

    dropped_by_split_and_reason: dict[str, dict[str, int]] = field(
        default_factory=dict
    )
    targets_imputed: bool = False


@dataclass(frozen=True)
class EvaluationPreregistrationProof:
    """Phase 4bn-AE amendment-001 pre-registration proof section."""

    active_feature_list_hash: str = "synthetic-placeholder"
    forbidden_column_scan_empty: bool = True
    mandatory_metrics: tuple[str, ...] = contract.MANDATORY_METRICS
    metric_granularities: tuple[str, ...] = contract.METRIC_GRANULARITIES
    row_level_metrics_descriptive_only: bool = True
    decision_block_units: tuple[str, ...] = contract.DECISION_BLOCK_UNITS
    dependence_caveat_present: bool = True
    decimation_stride: int | None = None
    calibration_schema_present: bool = True
    high_confidence_threshold: float = contract.HIGH_CONFIDENCE_THRESHOLD
    cost_descriptive_fields_present: bool = True
    locked_round_trip_cost_bps: float = contract.LOCKED_ROUND_TRIP_COST_BPS
    success_accuracy_uplift_pp: float = contract.SUCCESS_ACCURACY_UPLIFT_PP
    success_balanced_accuracy_uplift_pp: float = (
        contract.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP
    )
    success_macro_f1_uplift: float = contract.SUCCESS_MACRO_F1_UPLIFT
    claim_scope_allowed: tuple[str, ...] = contract.CLAIM_SCOPE_ALLOWED
    claim_scope_forbidden: tuple[str, ...] = contract.CLAIM_SCOPE_FORBIDDEN
    no_strategy_boundary: bool = True


@dataclass(frozen=True)
class BudgetPreflightPlaceholder:
    """Interface-shape-only budget preflight (never measures disk / writes)."""

    is_placeholder: bool = True
    ran_preflight: bool = False
    measured_disk: bool = False
    wrote_output: bool = False
    derived_footprint_warn_gib: int = DERIVED_FOOTPRINT_WARN_GIB
    derived_footprint_hard_gib: int = DERIVED_FOOTPRINT_HARD_GIB
    total_derived_stack_warn_gib: int = TOTAL_DERIVED_STACK_WARN_GIB
    total_derived_stack_hard_gib: int = TOTAL_DERIVED_STACK_HARD_GIB
    runtime_warn_hours: int = RUNTIME_WARN_HOURS
    runtime_hard_hours: int = RUNTIME_HARD_HOURS
    temp_warn_gib: int = TEMP_WARN_GIB
    temp_hard_gib: int = TEMP_HARD_GIB
    d_drive_min_free_gib_before: int = D_DRIVE_MIN_FREE_GIB_BEFORE
    d_drive_fail_closed_during_gib: int = D_DRIVE_FAIL_CLOSED_DURING_GIB


@dataclass(frozen=True)
class NonAuthorizationProof:
    """Non-authorization proof section (all flags False)."""

    ml_authorized: bool = False
    diagnostics_authorized: bool = False
    strategy_authorized: bool = False
    signals_authorized: bool = False
    pnl_authorized: bool = False
    backtest_authorized: bool = False
    live_authorized: bool = False
    exchange_write_authorized: bool = False


@dataclass(frozen=True)
class DatasetBuilderProof:
    """Top-level inert dataset-builder proof (synthetic; writes no sidecar)."""

    contract_name: str
    amendment_id: str
    split: SplitProof
    alignment: AlignmentProof
    filtering: FilteringProof
    evaluation: EvaluationPreregistrationProof
    budget_preflight: BudgetPreflightPlaceholder
    non_authorization: NonAuthorizationProof
    output_namespace_path: str = contract.OUTPUT_NAMESPACE_PATH
    output_namespace_created: bool = False
    no_data_io: bool = True


def build_dataset_builder_proof(
    *,
    split_policy_commit_sha: str = "unknown",
    active_feature_list_hash: str = "synthetic-placeholder",
    key_alignment_row_count: int = 0,
    dropped_by_split_and_reason: dict[str, dict[str, int]] | None = None,
) -> DatasetBuilderProof:
    """Return an inert :class:`DatasetBuilderProof` from synthetic arguments.

    Reads no data and creates no output. The returned proof asserts, by
    construction, the conservative pre-v002 posture (no v002/sealed access, all
    non-authorization flags False, no output namespace created).
    """
    return DatasetBuilderProof(
        contract_name=contract.CONTRACT_NAME,
        amendment_id=contract.CONTRACT_AMENDMENT_ID,
        split=SplitProof(split_policy_commit_sha=split_policy_commit_sha),
        alignment=AlignmentProof(key_alignment_row_count=key_alignment_row_count),
        filtering=FilteringProof(
            dropped_by_split_and_reason=dropped_by_split_and_reason or {}
        ),
        evaluation=EvaluationPreregistrationProof(
            active_feature_list_hash=active_feature_list_hash
        ),
        budget_preflight=BudgetPreflightPlaceholder(),
        non_authorization=NonAuthorizationProof(),
    )


def validate_dataset_builder_proof(proof: DatasetBuilderProof) -> None:
    """Fail closed unless *proof* encodes the conservative pre-v002 posture.

    Verifies the split counts, the no-v002 / no-sealed / zero-test-rows flags,
    empty forbidden-column scan, presence of the mandatory metric registry and
    granularities, the descriptive-only + dependence + decimation posture, the
    pre-registered success constants, the budget-preflight placeholder shape, and
    that all non-authorization flags are False and no output namespace was
    created.
    """
    s = proof.split
    if (
        s.train_date_count != 214
        or s.validation_date_count != 45
        or s.holdout_date_count != 14
        or s.train_validation_embargo_count != 1
        or s.validation_holdout_embargo_count != 1
    ):
        raise PreV002MlDatasetError(
            "split proof date counts must be 214 / 1 / 45 / 1 / 14"
        )
    if s.split_policy_name != split_policy.SPLIT_POLICY_NAME:
        raise PreV002MlDatasetError("split proof policy name mismatch")
    for flag_name, value in (
        ("v002_terminal_window_read", s.v002_terminal_window_read),
        ("sealed_test_split_touched", s.sealed_test_split_touched),
    ):
        if value is not False:
            raise PreV002MlDatasetError(f"split proof {flag_name} must be False")
    if s.test_rows_loaded != 0:
        raise PreV002MlDatasetError("split proof test_rows_loaded must be 0")
    if s.out_of_segment_dates != 0:
        raise PreV002MlDatasetError("split proof out_of_segment_dates must be 0")
    for flag_name, value in (
        ("no_random", s.no_random),
        ("no_shuffle", s.no_shuffle),
        ("no_kfold", s.no_kfold),
        ("no_bootstrap", s.no_bootstrap),
    ):
        if value is not True:
            raise PreV002MlDatasetError(f"split proof {flag_name} must be True")

    if proof.filtering.targets_imputed is not False:
        raise PreV002MlDatasetError("filtering proof must not impute targets")

    e = proof.evaluation
    if not e.forbidden_column_scan_empty:
        raise PreV002MlDatasetError("evaluation proof forbidden-column scan not empty")
    missing_metrics = set(contract.MANDATORY_METRICS) - set(e.mandatory_metrics)
    if missing_metrics:
        raise PreV002MlDatasetError(
            f"evaluation proof missing mandatory metrics: {sorted(missing_metrics)!r}"
        )
    missing_gran = set(contract.METRIC_GRANULARITIES) - set(e.metric_granularities)
    if missing_gran:
        raise PreV002MlDatasetError(
            f"evaluation proof missing granularities: {sorted(missing_gran)!r}"
        )
    if e.row_level_metrics_descriptive_only is not True:
        raise PreV002MlDatasetError(
            "evaluation proof row_level_metrics_descriptive_only must be True"
        )
    if not e.dependence_caveat_present:
        raise PreV002MlDatasetError("evaluation proof missing dependence caveat")
    if e.decimation_stride is not None:
        raise PreV002MlDatasetError("evaluation proof decimation_stride must be None")
    if not e.calibration_schema_present:
        raise PreV002MlDatasetError("evaluation proof missing calibration schema")
    if not e.cost_descriptive_fields_present:
        raise PreV002MlDatasetError("evaluation proof missing cost descriptive fields")
    if e.success_accuracy_uplift_pp != contract.SUCCESS_ACCURACY_UPLIFT_PP:
        raise PreV002MlDatasetError("evaluation proof accuracy uplift mismatch")
    if e.success_macro_f1_uplift != contract.SUCCESS_MACRO_F1_UPLIFT:
        raise PreV002MlDatasetError("evaluation proof macro-f1 uplift mismatch")
    if e.no_strategy_boundary is not True:
        raise PreV002MlDatasetError("evaluation proof missing no-strategy boundary")

    if not proof.budget_preflight.is_placeholder:
        raise PreV002MlDatasetError("budget preflight must be a placeholder")
    if proof.budget_preflight.measured_disk or proof.budget_preflight.wrote_output:
        raise PreV002MlDatasetError(
            "budget preflight placeholder must not measure disk or write output"
        )

    na = proof.non_authorization
    for flag_name in (
        "ml_authorized",
        "diagnostics_authorized",
        "strategy_authorized",
        "signals_authorized",
        "pnl_authorized",
        "backtest_authorized",
        "live_authorized",
        "exchange_write_authorized",
    ):
        if getattr(na, flag_name) is not False:
            raise PreV002MlDatasetError(
                f"non-authorization proof {flag_name} must be False"
            )

    if proof.output_namespace_created is not False:
        raise PreV002MlDatasetError("proof output_namespace_created must be False")
    if proof.no_data_io is not True:
        raise PreV002MlDatasetError("proof no_data_io must be True")


__all__ = [
    "AlignmentProof",
    "BudgetPreflightPlaceholder",
    "DatasetBuilderProof",
    "EvaluationPreregistrationProof",
    "FilteringProof",
    "NonAuthorizationProof",
    "SplitProof",
    "build_dataset_builder_proof",
    "validate_dataset_builder_proof",
]
