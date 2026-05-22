"""Phase 4bm-J multi-day v002 feature-family eligibility gate report.

Builds and writes the deterministic JSON gate report produced by the
Phase 4bm-J check suite. The report aggregates per-check results plus
identity / lineage / non-authorization fields per the Phase 4bm-J
authorization prompt. The writer is atomic write-then-rename + refuse-
to-overwrite + paired canonical Phase 4bb-F sidecar.

This module:

- never mutates any artefact other than writing the new gate report
  + paired sidecar under
  ``data/microstructure/gate-reports/features/`` (gitignored);
- enforces ``research_eligible_after = false``,
  ``eligibility_gate_status_after = "pending"``,
  ``stage_4_feature_cleared_after = false`` as build-time invariants;
- never authorizes any successor phase.
"""
# ruff: noqa: E501  (Phase 4bm-J: long v002 SHA literals + lineage column names)
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .multiday_feature_gate_checks import (
    EXPECTED_DATE_COUNT,
    EXPECTED_DATE_END,
    EXPECTED_DATE_START,
    EXPECTED_FEATURE_COLUMN_COUNT,
    EXPECTED_FEATURE_CONFIG_HASH,
    EXPECTED_FEATURE_MANIFEST_SHA,
    EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA,
    EXPECTED_FEATURE_SCHEMA_COLUMN_COUNT,
    EXPECTED_LINEAGE_COLUMN_COUNT,
    EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA,
    EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA,
    EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA,
    EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA,
    EXPECTED_SYMBOL,
    EXPECTED_TOTAL_FEATURE_ROW_COUNT,
    EXPECTED_V002_DERIVED_MANIFEST_SHA,
    EXPECTED_V002_RAW_MANIFEST_SHA,
    MultidayFeatureGateCheckResult,
    MultidayFeatureGateCheckStatus,
)
from .multiday_feature_gate_io import (
    atomic_write_json,
    atomic_write_sidecar,
)

GATE_VERDICT_PASS = "FEATURE_GATE_PASS"
GATE_VERDICT_FAIL = "FEATURE_GATE_FAIL"
GATE_VERDICT_INDETERMINATE = "FEATURE_GATE_INDETERMINATE"

ALLOWED_GATE_VERDICTS = frozenset({
    GATE_VERDICT_PASS, GATE_VERDICT_FAIL, GATE_VERDICT_INDETERMINATE,
})


class MultidayFeatureGateReportError(RuntimeError):
    """Raised when a gate-report build / write invariant fails closed."""


@dataclass(frozen=True)
class MultidayFeatureGateReport:
    """Frozen Phase 4bm-J gate report data model."""

    report_schema_version: str
    phase_id: str
    phase_name: str
    created_at_utc_ms: int
    dataset_family: str
    dataset_version: str
    feature_schema_version: str
    symbol: str
    utc_date_start: str
    utc_date_end: str
    date_count: int
    expected_feature_row_count: int
    actual_feature_row_count: int
    feature_manifest_path: str
    feature_manifest_sha256: str
    feature_manifest_sidecar_sha256: str
    feature_config_hash: str
    feature_parquet_count: int
    feature_sidecar_count: int
    feature_schema_column_count: int
    lineage_column_count: int
    feature_column_count: int
    structural_qa_phase: str
    structural_qa_verdict: str
    source_successor_state_sha256: str
    source_phase_4bl_d_r_raw_gate_report_sha256: str
    source_phase_4bl_e_raw_successor_state_sha256: str
    source_normalized_manifest_sha256: str
    source_raw_manifest_sha256: str
    source_phase_4bm_d_gate_report_sha256: str
    gate_verdict: str
    overall_status: str
    pass_count: int
    fail_count: int
    error_count: int
    not_applicable_count: int
    blocking_fail_count: int
    checks: tuple[dict[str, Any], ...]
    boundary_confirmations: dict[str, bool]
    research_eligible_after: bool
    eligibility_gate_status_after: str
    stage_4_feature_cleared_after: bool
    feature_family_research_use_authorized: bool
    successor_state_authorized: bool
    label_computation_authorized: bool
    diagnostics_authorized: bool
    ml_authorized: bool
    strategy_authorized: bool
    backtest_authorized: bool
    acquisition_authorized: bool
    no_manifest_mutation: bool
    no_successor_state_created: bool
    no_feature_recomputation: bool
    no_label_computed: bool
    no_signal_computed: bool
    no_ml_trained: bool
    no_strategy_created: bool
    no_backtest_run: bool
    no_network_io: bool
    no_credentials: bool
    no_mcp_or_graphify: bool
    no_exchange_write: bool
    retained_verdicts_preserved: bool
    governance_locks_preserved: bool
    code_commit_sha: str
    notes: str

    def __post_init__(self) -> None:
        if self.gate_verdict not in ALLOWED_GATE_VERDICTS:
            raise MultidayFeatureGateReportError(
                f"gate_verdict must be one of {sorted(ALLOWED_GATE_VERDICTS)}; "
                f"got {self.gate_verdict!r}"
            )
        if self.research_eligible_after is not False:
            raise MultidayFeatureGateReportError(
                "research_eligible_after must be False (hard invariant)"
            )
        if self.eligibility_gate_status_after != "pending":
            raise MultidayFeatureGateReportError(
                "eligibility_gate_status_after must be 'pending' (hard invariant)"
            )
        if self.stage_4_feature_cleared_after is not False:
            raise MultidayFeatureGateReportError(
                "stage_4_feature_cleared_after must be False (hard invariant)"
            )
        for label in (
            "feature_family_research_use_authorized",
            "successor_state_authorized",
            "label_computation_authorized",
            "diagnostics_authorized",
            "ml_authorized",
            "strategy_authorized",
            "backtest_authorized",
            "acquisition_authorized",
        ):
            if getattr(self, label) is not False:
                raise MultidayFeatureGateReportError(
                    f"{label} must be False (hard invariant)"
                )
        for label in (
            "no_manifest_mutation",
            "no_successor_state_created",
            "no_feature_recomputation",
            "no_label_computed",
            "no_signal_computed",
            "no_ml_trained",
            "no_strategy_created",
            "no_backtest_run",
            "no_network_io",
            "no_credentials",
            "no_mcp_or_graphify",
            "no_exchange_write",
            "retained_verdicts_preserved",
            "governance_locks_preserved",
        ):
            if getattr(self, label) is not True:
                raise MultidayFeatureGateReportError(
                    f"{label} must be True (hard invariant)"
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_schema_version": self.report_schema_version,
            "phase_id": self.phase_id,
            "phase_name": self.phase_name,
            "created_at_utc_ms": int(self.created_at_utc_ms),
            "dataset_family": self.dataset_family,
            "dataset_version": self.dataset_version,
            "feature_schema_version": self.feature_schema_version,
            "symbol": self.symbol,
            "utc_date_start": self.utc_date_start,
            "utc_date_end": self.utc_date_end,
            "date_count": int(self.date_count),
            "expected_feature_row_count": int(self.expected_feature_row_count),
            "actual_feature_row_count": int(self.actual_feature_row_count),
            "feature_manifest_path": self.feature_manifest_path,
            "feature_manifest_sha256": self.feature_manifest_sha256,
            "feature_manifest_sidecar_sha256": self.feature_manifest_sidecar_sha256,
            "feature_config_hash": self.feature_config_hash,
            "feature_parquet_count": int(self.feature_parquet_count),
            "feature_sidecar_count": int(self.feature_sidecar_count),
            "feature_schema_column_count": int(self.feature_schema_column_count),
            "lineage_column_count": int(self.lineage_column_count),
            "feature_column_count": int(self.feature_column_count),
            "structural_qa_phase": self.structural_qa_phase,
            "structural_qa_verdict": self.structural_qa_verdict,
            "source_successor_state_sha256": self.source_successor_state_sha256,
            "source_phase_4bl_d_r_raw_gate_report_sha256": self.source_phase_4bl_d_r_raw_gate_report_sha256,
            "source_phase_4bl_e_raw_successor_state_sha256": self.source_phase_4bl_e_raw_successor_state_sha256,
            "source_normalized_manifest_sha256": self.source_normalized_manifest_sha256,
            "source_raw_manifest_sha256": self.source_raw_manifest_sha256,
            "source_phase_4bm_d_gate_report_sha256": self.source_phase_4bm_d_gate_report_sha256,
            "gate_verdict": self.gate_verdict,
            "overall_status": self.overall_status,
            "pass_count": int(self.pass_count),
            "fail_count": int(self.fail_count),
            "error_count": int(self.error_count),
            "not_applicable_count": int(self.not_applicable_count),
            "blocking_fail_count": int(self.blocking_fail_count),
            "checks": list(self.checks),
            "boundary_confirmations": dict(self.boundary_confirmations),
            "research_eligible_after": bool(self.research_eligible_after),
            "eligibility_gate_status_after": self.eligibility_gate_status_after,
            "stage_4_feature_cleared_after": bool(self.stage_4_feature_cleared_after),
            "feature_family_research_use_authorized": bool(self.feature_family_research_use_authorized),
            "successor_state_authorized": bool(self.successor_state_authorized),
            "label_computation_authorized": bool(self.label_computation_authorized),
            "diagnostics_authorized": bool(self.diagnostics_authorized),
            "ml_authorized": bool(self.ml_authorized),
            "strategy_authorized": bool(self.strategy_authorized),
            "backtest_authorized": bool(self.backtest_authorized),
            "acquisition_authorized": bool(self.acquisition_authorized),
            "no_manifest_mutation": bool(self.no_manifest_mutation),
            "no_successor_state_created": bool(self.no_successor_state_created),
            "no_feature_recomputation": bool(self.no_feature_recomputation),
            "no_label_computed": bool(self.no_label_computed),
            "no_signal_computed": bool(self.no_signal_computed),
            "no_ml_trained": bool(self.no_ml_trained),
            "no_strategy_created": bool(self.no_strategy_created),
            "no_backtest_run": bool(self.no_backtest_run),
            "no_network_io": bool(self.no_network_io),
            "no_credentials": bool(self.no_credentials),
            "no_mcp_or_graphify": bool(self.no_mcp_or_graphify),
            "no_exchange_write": bool(self.no_exchange_write),
            "retained_verdicts_preserved": bool(self.retained_verdicts_preserved),
            "governance_locks_preserved": bool(self.governance_locks_preserved),
            "code_commit_sha": self.code_commit_sha,
            "notes": self.notes,
        }


def _classify_gate_verdict(
    results: Iterable[MultidayFeatureGateCheckResult],
) -> tuple[str, int, int, int, int, int]:
    p = f = e = na = blocking = 0
    for r in results:
        if r.status == MultidayFeatureGateCheckStatus.PASS:
            p += 1
        elif r.status == MultidayFeatureGateCheckStatus.FAIL:
            f += 1
            if r.blocking:
                blocking += 1
        elif r.status == MultidayFeatureGateCheckStatus.ERROR:
            e += 1
            if r.blocking:
                blocking += 1
        elif r.status == MultidayFeatureGateCheckStatus.NOT_APPLICABLE:
            na += 1
    if e > 0 and f == 0:
        verdict = GATE_VERDICT_INDETERMINATE
    elif blocking > 0:
        verdict = GATE_VERDICT_FAIL
    else:
        verdict = GATE_VERDICT_PASS
    return verdict, p, f, e, na, blocking


def build_report(
    *,
    results: tuple[MultidayFeatureGateCheckResult, ...],
    manifest: Mapping[str, Any],
    feature_manifest_path: Path,
    created_at_utc_ms: int,
    code_commit_sha: str,
    feature_parquet_count: int,
    feature_sidecar_count: int,
    structural_qa_phase: str = "4bm-I",
    structural_qa_verdict: str = "FEATURE_STRUCTURAL_QA_PASS",
) -> MultidayFeatureGateReport:
    verdict, p, f, e, na, blocking = _classify_gate_verdict(results)
    overall = "pass" if verdict == GATE_VERDICT_PASS else ("fail" if verdict == GATE_VERDICT_FAIL else "indeterminate")

    boundary_confirmations = {
        "no_feature_recomputation": True,
        "no_manifest_mutation": True,
        "no_successor_state_created": True,
        "no_label_computed": True,
        "no_signal_computed": True,
        "no_ml_trained": True,
        "no_strategy_created": True,
        "no_backtest_run": True,
        "no_network_io": True,
        "no_credentials": True,
        "no_mcp_or_graphify": True,
        "no_exchange_write": True,
        "no_acquisition": True,
        "no_data_microstructure_artefact_modified": True,
        "no_research_eligible_flip": True,
        "no_eligibility_gate_status_transition": True,
        "no_stage_4_feature_cleared": True,
        "no_successor_phase_authorized": True,
        "phase_4aw_flip_research_eligible_invariant_preserved": True,
        "retained_verdicts_preserved": True,
        "governance_locks_preserved": True,
    }
    notes = (
        "Phase 4bm-J is the multi-day v002 analogue of Phase 4bi-B (v001 feature-family "
        "eligibility gate). FEATURE_GATE_PASS, if achieved, is REPORT-LEVEL ONLY and "
        "does NOT authorize feature-family research-use, successor-state recording, "
        "labels, diagnostics, ML, strategy, backtests, acquisition, paper / shadow, "
        "live-readiness, deployment, exchange-write, or any successor phase. The "
        "actual v002 feature manifest carries research_eligible=false / "
        "eligibility_gate_status='pending' / stage_4_feature_cleared=false byte-"
        "identically before and after this gate report. The Phase 4aw "
        "MicrostructureManifest.flip_research_eligible(...) always-raises invariant "
        "remains preserved end-to-end and was NEVER invoked."
    )

    return MultidayFeatureGateReport(
        report_schema_version="v001",
        phase_id="4bm-J",
        phase_name="Multi-Day V002 Feature-Family Eligibility Gate Design / Implementation / Execution",
        created_at_utc_ms=created_at_utc_ms,
        dataset_family="microstructure_features_aggtrades_v001",
        dataset_version="v002",
        feature_schema_version="v001",
        symbol=EXPECTED_SYMBOL,
        utc_date_start=EXPECTED_DATE_START,
        utc_date_end=EXPECTED_DATE_END,
        date_count=EXPECTED_DATE_COUNT,
        expected_feature_row_count=EXPECTED_TOTAL_FEATURE_ROW_COUNT,
        actual_feature_row_count=int(manifest.get("actual_feature_row_count", 0)),
        feature_manifest_path=str(feature_manifest_path),
        feature_manifest_sha256=EXPECTED_FEATURE_MANIFEST_SHA,
        feature_manifest_sidecar_sha256=EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA,
        feature_config_hash=EXPECTED_FEATURE_CONFIG_HASH,
        feature_parquet_count=int(feature_parquet_count),
        feature_sidecar_count=int(feature_sidecar_count),
        feature_schema_column_count=EXPECTED_FEATURE_SCHEMA_COLUMN_COUNT,
        lineage_column_count=EXPECTED_LINEAGE_COLUMN_COUNT,
        feature_column_count=EXPECTED_FEATURE_COLUMN_COUNT,
        structural_qa_phase=structural_qa_phase,
        structural_qa_verdict=structural_qa_verdict,
        source_successor_state_sha256=EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA,
        source_phase_4bl_d_r_raw_gate_report_sha256=EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA,
        source_phase_4bl_e_raw_successor_state_sha256=EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA,
        source_normalized_manifest_sha256=EXPECTED_V002_DERIVED_MANIFEST_SHA,
        source_raw_manifest_sha256=EXPECTED_V002_RAW_MANIFEST_SHA,
        source_phase_4bm_d_gate_report_sha256=EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA,
        gate_verdict=verdict,
        overall_status=overall,
        pass_count=p,
        fail_count=f,
        error_count=e,
        not_applicable_count=na,
        blocking_fail_count=blocking,
        checks=tuple(r.to_dict() for r in results),
        boundary_confirmations=boundary_confirmations,
        research_eligible_after=False,
        eligibility_gate_status_after="pending",
        stage_4_feature_cleared_after=False,
        feature_family_research_use_authorized=False,
        successor_state_authorized=False,
        label_computation_authorized=False,
        diagnostics_authorized=False,
        ml_authorized=False,
        strategy_authorized=False,
        backtest_authorized=False,
        acquisition_authorized=False,
        no_manifest_mutation=True,
        no_successor_state_created=True,
        no_feature_recomputation=True,
        no_label_computed=True,
        no_signal_computed=True,
        no_ml_trained=True,
        no_strategy_created=True,
        no_backtest_run=True,
        no_network_io=True,
        no_credentials=True,
        no_mcp_or_graphify=True,
        no_exchange_write=True,
        retained_verdicts_preserved=True,
        governance_locks_preserved=True,
        code_commit_sha=code_commit_sha,
        notes=notes,
    )


def write_gate_report(
    *,
    report: MultidayFeatureGateReport,
    report_path: Path,
    sidecar_path: Path,
) -> tuple[str, int, str, int]:
    """Atomically write report + sidecar; return ``(report_sha, report_size, sidecar_sha, sidecar_size)``."""
    rep_sha, rep_size = atomic_write_json(report_path, report.to_dict(), refuse_overwrite=True)
    side_sha, side_size = atomic_write_sidecar(
        sidecar_path,
        target_basename=report_path.name,
        sha256_hex=rep_sha,
        refuse_overwrite=True,
    )
    return rep_sha, rep_size, side_sha, side_size


__all__ = [
    "ALLOWED_GATE_VERDICTS",
    "GATE_VERDICT_FAIL",
    "GATE_VERDICT_INDETERMINATE",
    "GATE_VERDICT_PASS",
    "MultidayFeatureGateReport",
    "MultidayFeatureGateReportError",
    "build_report",
    "write_gate_report",
]
