"""Phase 4bm-Q multi-day v002 label-family eligibility gate report.

Builds and writes the deterministic JSON gate report produced by the
Phase 4bm-Q check suite. The report aggregates per-check results plus
identity / lineage / non-authorization fields per the Phase 4bm-Q
authorization prompt. The writer is atomic write-then-rename +
refuse-to-overwrite + paired canonical Phase 4bb-F sidecar.

This module:

- never mutates any artefact other than writing the new gate report
  + paired sidecar under
  ``data/microstructure/gate-reports/labels/`` (gitignored);
- enforces ``research_eligible_after = false``,
  ``eligibility_gate_status_after = "pending"``,
  ``stage_5_label_cleared_after = false``,
  ``label_family_research_use_authorized_after = false``,
  ``chronological_split_policy_after = "not_yet_defined"`` as
  build-time invariants;
- never authorizes any successor phase.
"""
# ruff: noqa: E501  (Phase 4bm-Q: long v002 SHA literals)
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .multiday_label_gate_checks import (
    EXPECTED_CENSORED_PER_HORIZON,
    EXPECTED_DATE_COUNT,
    EXPECTED_DATE_END,
    EXPECTED_DATE_START,
    EXPECTED_ENVELOPE_TERMINAL_UNIX_MS,
    EXPECTED_FEATURE_CONFIG_HASH,
    EXPECTED_FEATURE_MANIFEST_SHA,
    EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA,
    EXPECTED_INVALID_PRICE_ROW_COUNT,
    EXPECTED_LABEL_COLUMN_COUNT,
    EXPECTED_LABEL_CONFIG_HASH,
    EXPECTED_LABEL_MANIFEST_SHA,
    EXPECTED_LABEL_MANIFEST_SIDECAR_SHA,
    EXPECTED_LABEL_SCHEMA_COLUMN_COUNT,
    EXPECTED_LINEAGE_COLUMN_COUNT,
    EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA,
    EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA,
    EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA,
    EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA,
    EXPECTED_PHASE_4BM_J_GATE_REPORT_SHA,
    EXPECTED_PHASE_4BM_J_GATE_SIDECAR_SHA,
    EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SHA,
    EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SIDECAR_SHA,
    EXPECTED_SUPPORT_COLUMN_COUNT,
    EXPECTED_SYMBOL,
    EXPECTED_TOTAL_LABEL_ROW_COUNT,
    EXPECTED_V002_DERIVED_MANIFEST_SHA,
    EXPECTED_V002_RAW_MANIFEST_SHA,
    MultidayLabelGateCheckResult,
    MultidayLabelGateCheckStatus,
)
from .multiday_label_gate_io import (
    atomic_write_json,
    atomic_write_sidecar,
)

GATE_VERDICT_PASS = "LABEL_GATE_PASS"
GATE_VERDICT_FAIL = "LABEL_GATE_FAIL"
GATE_VERDICT_INDETERMINATE = "LABEL_GATE_INDETERMINATE"

ALLOWED_GATE_VERDICTS = frozenset({
    GATE_VERDICT_PASS, GATE_VERDICT_FAIL, GATE_VERDICT_INDETERMINATE,
})


class MultidayLabelGateReportError(RuntimeError):
    """Raised when a gate-report build / write invariant fails closed."""


@dataclass(frozen=True)
class MultidayLabelGateReport:
    """Frozen Phase 4bm-Q gate report data model."""

    report_schema_version: str
    phase_id: str
    phase_name: str
    created_at_utc_ms: int
    dataset_family: str
    dataset_version: str
    label_schema_version: str
    symbol: str
    utc_date_start: str
    utc_date_end: str
    date_count: int
    expected_label_row_count: int
    actual_label_row_count: int
    label_manifest_path: str
    label_manifest_sha256: str
    label_manifest_sidecar_sha256: str
    label_config_hash: str
    feature_config_hash: str
    label_parquet_count: int
    label_sidecar_count: int
    label_schema_column_count: int
    lineage_column_count: int
    label_column_count: int
    support_column_count: int
    envelope_terminal_unix_ms: int
    censored_per_horizon: dict[str, int]
    invalid_price_row_count: int
    structural_qa_phase: str
    structural_qa_verdict: str
    source_feature_manifest_sha256: str
    source_feature_manifest_sidecar_sha256: str
    source_phase_4bm_j_gate_report_sha256: str
    source_phase_4bm_j_gate_sidecar_sha256: str
    source_phase_4bm_l_successor_state_sha256: str
    source_phase_4bm_l_successor_state_sidecar_sha256: str
    source_normalized_manifest_sha256: str
    source_raw_manifest_sha256: str
    source_phase_4bm_d_gate_report_sha256: str
    source_phase_4bm_f_successor_state_sha256: str
    source_phase_4bl_d_r_gate_report_sha256: str
    source_phase_4bl_e_successor_state_sha256: str
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
    stage_5_label_cleared_after: bool
    label_family_research_use_authorized_after: bool
    chronological_split_policy_after: str
    label_family_eligibility_gate_authorized_after: bool
    successor_state_authorized: bool
    diagnostics_authorized: bool
    ml_authorized: bool
    strategy_authorized: bool
    backtest_authorized: bool
    acquisition_authorized: bool
    no_manifest_mutation: bool
    no_successor_state_created: bool
    no_label_recomputation: bool
    no_diagnostics_computed: bool
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
            raise MultidayLabelGateReportError(
                f"gate_verdict must be one of {sorted(ALLOWED_GATE_VERDICTS)}; "
                f"got {self.gate_verdict!r}"
            )
        if self.research_eligible_after is not False:
            raise MultidayLabelGateReportError(
                "research_eligible_after must be False (hard invariant)"
            )
        if self.eligibility_gate_status_after != "pending":
            raise MultidayLabelGateReportError(
                "eligibility_gate_status_after must be 'pending' (hard invariant)"
            )
        if self.stage_5_label_cleared_after is not False:
            raise MultidayLabelGateReportError(
                "stage_5_label_cleared_after must be False (hard invariant)"
            )
        if self.label_family_research_use_authorized_after is not False:
            raise MultidayLabelGateReportError(
                "label_family_research_use_authorized_after must be False (hard invariant)"
            )
        if self.chronological_split_policy_after != "not_yet_defined":
            raise MultidayLabelGateReportError(
                "chronological_split_policy_after must be 'not_yet_defined' (hard invariant)"
            )
        for label in (
            "label_family_eligibility_gate_authorized_after",
            "successor_state_authorized",
            "diagnostics_authorized",
            "ml_authorized",
            "strategy_authorized",
            "backtest_authorized",
            "acquisition_authorized",
        ):
            if getattr(self, label) is not False:
                raise MultidayLabelGateReportError(
                    f"{label} must be False (hard invariant)"
                )
        for label in (
            "no_manifest_mutation",
            "no_successor_state_created",
            "no_label_recomputation",
            "no_diagnostics_computed",
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
                raise MultidayLabelGateReportError(
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
            "label_schema_version": self.label_schema_version,
            "symbol": self.symbol,
            "utc_date_start": self.utc_date_start,
            "utc_date_end": self.utc_date_end,
            "date_count": int(self.date_count),
            "expected_label_row_count": int(self.expected_label_row_count),
            "actual_label_row_count": int(self.actual_label_row_count),
            "label_manifest_path": self.label_manifest_path,
            "label_manifest_sha256": self.label_manifest_sha256,
            "label_manifest_sidecar_sha256": self.label_manifest_sidecar_sha256,
            "label_config_hash": self.label_config_hash,
            "feature_config_hash": self.feature_config_hash,
            "label_parquet_count": int(self.label_parquet_count),
            "label_sidecar_count": int(self.label_sidecar_count),
            "label_schema_column_count": int(self.label_schema_column_count),
            "lineage_column_count": int(self.lineage_column_count),
            "label_column_count": int(self.label_column_count),
            "support_column_count": int(self.support_column_count),
            "envelope_terminal_unix_ms": int(self.envelope_terminal_unix_ms),
            "censored_per_horizon": dict(self.censored_per_horizon),
            "invalid_price_row_count": int(self.invalid_price_row_count),
            "structural_qa_phase": self.structural_qa_phase,
            "structural_qa_verdict": self.structural_qa_verdict,
            "source_feature_manifest_sha256": self.source_feature_manifest_sha256,
            "source_feature_manifest_sidecar_sha256": self.source_feature_manifest_sidecar_sha256,
            "source_phase_4bm_j_gate_report_sha256": self.source_phase_4bm_j_gate_report_sha256,
            "source_phase_4bm_j_gate_sidecar_sha256": self.source_phase_4bm_j_gate_sidecar_sha256,
            "source_phase_4bm_l_successor_state_sha256": self.source_phase_4bm_l_successor_state_sha256,
            "source_phase_4bm_l_successor_state_sidecar_sha256": self.source_phase_4bm_l_successor_state_sidecar_sha256,
            "source_normalized_manifest_sha256": self.source_normalized_manifest_sha256,
            "source_raw_manifest_sha256": self.source_raw_manifest_sha256,
            "source_phase_4bm_d_gate_report_sha256": self.source_phase_4bm_d_gate_report_sha256,
            "source_phase_4bm_f_successor_state_sha256": self.source_phase_4bm_f_successor_state_sha256,
            "source_phase_4bl_d_r_gate_report_sha256": self.source_phase_4bl_d_r_gate_report_sha256,
            "source_phase_4bl_e_successor_state_sha256": self.source_phase_4bl_e_successor_state_sha256,
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
            "stage_5_label_cleared_after": bool(self.stage_5_label_cleared_after),
            "label_family_research_use_authorized_after": bool(
                self.label_family_research_use_authorized_after
            ),
            "chronological_split_policy_after": self.chronological_split_policy_after,
            "label_family_eligibility_gate_authorized_after": bool(
                self.label_family_eligibility_gate_authorized_after
            ),
            "successor_state_authorized": bool(self.successor_state_authorized),
            "diagnostics_authorized": bool(self.diagnostics_authorized),
            "ml_authorized": bool(self.ml_authorized),
            "strategy_authorized": bool(self.strategy_authorized),
            "backtest_authorized": bool(self.backtest_authorized),
            "acquisition_authorized": bool(self.acquisition_authorized),
            "no_manifest_mutation": bool(self.no_manifest_mutation),
            "no_successor_state_created": bool(self.no_successor_state_created),
            "no_label_recomputation": bool(self.no_label_recomputation),
            "no_diagnostics_computed": bool(self.no_diagnostics_computed),
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
    results: Iterable[MultidayLabelGateCheckResult],
) -> tuple[str, int, int, int, int, int]:
    p = f = e = na = blocking = 0
    for r in results:
        if r.status == MultidayLabelGateCheckStatus.PASS:
            p += 1
        elif r.status == MultidayLabelGateCheckStatus.FAIL:
            f += 1
            if r.blocking:
                blocking += 1
        elif r.status == MultidayLabelGateCheckStatus.ERROR:
            e += 1
            if r.blocking:
                blocking += 1
        elif r.status == MultidayLabelGateCheckStatus.NOT_APPLICABLE:
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
    results: tuple[MultidayLabelGateCheckResult, ...],
    manifest: Mapping[str, Any],
    label_manifest_path: Path,
    created_at_utc_ms: int,
    code_commit_sha: str,
    label_parquet_count: int,
    label_sidecar_count: int,
    structural_qa_phase: str = "4bm-P",
    structural_qa_verdict: str = "LABEL_STRUCTURAL_QA_PASS",
) -> MultidayLabelGateReport:
    verdict, p, f, e, na, blocking = _classify_gate_verdict(results)
    overall = (
        "pass" if verdict == GATE_VERDICT_PASS
        else ("fail" if verdict == GATE_VERDICT_FAIL else "indeterminate")
    )

    boundary_confirmations = {
        "no_label_recomputation": True,
        "no_manifest_mutation": True,
        "no_successor_state_created": True,
        "no_diagnostics_computed": True,
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
        "no_stage_5_label_cleared": True,
        "no_label_family_research_use_authorization": True,
        "no_chronological_split_policy_change": True,
        "no_successor_phase_authorized": True,
        "phase_4aw_flip_research_eligible_invariant_preserved": True,
        "retained_verdicts_preserved": True,
        "governance_locks_preserved": True,
    }
    notes = (
        "Phase 4bm-Q is the multi-day v002 analogue of Phase 4bj-E (v001 "
        "label-family eligibility gate). LABEL_GATE_PASS, if achieved, is "
        "REPORT-LEVEL ONLY and does NOT authorize label-family research-use, "
        "successor-state recording, chronological-split-policy definition, "
        "diagnostics, ML, strategy, backtests, acquisition, paper/shadow, "
        "live-readiness, deployment, exchange-write, or any successor phase. "
        "The actual v002 label manifest carries research_eligible=false / "
        "eligibility_gate_status='pending' / stage_5_label_cleared=false / "
        "label_family_research_use_authorized=false / "
        "chronological_split_policy='not_yet_defined' byte-identically before "
        "and after this gate report. The Phase 4aw "
        "MicrostructureManifest.flip_research_eligible(...) always-raises "
        "invariant remains preserved end-to-end and was NEVER invoked."
    )

    return MultidayLabelGateReport(
        report_schema_version="v001",
        phase_id="4bm-Q",
        phase_name="Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution",
        created_at_utc_ms=created_at_utc_ms,
        dataset_family="microstructure_labels_aggtrades_v001",
        dataset_version="v002",
        label_schema_version="v001",
        symbol=EXPECTED_SYMBOL,
        utc_date_start=EXPECTED_DATE_START,
        utc_date_end=EXPECTED_DATE_END,
        date_count=EXPECTED_DATE_COUNT,
        expected_label_row_count=EXPECTED_TOTAL_LABEL_ROW_COUNT,
        actual_label_row_count=int(manifest.get("row_count", 0)),
        label_manifest_path=str(label_manifest_path),
        label_manifest_sha256=EXPECTED_LABEL_MANIFEST_SHA,
        label_manifest_sidecar_sha256=EXPECTED_LABEL_MANIFEST_SIDECAR_SHA,
        label_config_hash=EXPECTED_LABEL_CONFIG_HASH,
        feature_config_hash=EXPECTED_FEATURE_CONFIG_HASH,
        label_parquet_count=int(label_parquet_count),
        label_sidecar_count=int(label_sidecar_count),
        label_schema_column_count=EXPECTED_LABEL_SCHEMA_COLUMN_COUNT,
        lineage_column_count=EXPECTED_LINEAGE_COLUMN_COUNT,
        label_column_count=EXPECTED_LABEL_COLUMN_COUNT,
        support_column_count=EXPECTED_SUPPORT_COLUMN_COUNT,
        envelope_terminal_unix_ms=EXPECTED_ENVELOPE_TERMINAL_UNIX_MS,
        censored_per_horizon=dict(EXPECTED_CENSORED_PER_HORIZON),
        invalid_price_row_count=EXPECTED_INVALID_PRICE_ROW_COUNT,
        structural_qa_phase=structural_qa_phase,
        structural_qa_verdict=structural_qa_verdict,
        source_feature_manifest_sha256=EXPECTED_FEATURE_MANIFEST_SHA,
        source_feature_manifest_sidecar_sha256=EXPECTED_FEATURE_MANIFEST_SIDECAR_SHA,
        source_phase_4bm_j_gate_report_sha256=EXPECTED_PHASE_4BM_J_GATE_REPORT_SHA,
        source_phase_4bm_j_gate_sidecar_sha256=EXPECTED_PHASE_4BM_J_GATE_SIDECAR_SHA,
        source_phase_4bm_l_successor_state_sha256=EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SHA,
        source_phase_4bm_l_successor_state_sidecar_sha256=EXPECTED_PHASE_4BM_L_SUCCESSOR_STATE_SIDECAR_SHA,
        source_normalized_manifest_sha256=EXPECTED_V002_DERIVED_MANIFEST_SHA,
        source_raw_manifest_sha256=EXPECTED_V002_RAW_MANIFEST_SHA,
        source_phase_4bm_d_gate_report_sha256=EXPECTED_PHASE_4BM_D_GATE_REPORT_SHA,
        source_phase_4bm_f_successor_state_sha256=EXPECTED_PHASE_4BM_F_SUCCESSOR_STATE_SHA,
        source_phase_4bl_d_r_gate_report_sha256=EXPECTED_PHASE_4BL_D_R_GATE_REPORT_SHA,
        source_phase_4bl_e_successor_state_sha256=EXPECTED_PHASE_4BL_E_SUCCESSOR_STATE_SHA,
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
        stage_5_label_cleared_after=False,
        label_family_research_use_authorized_after=False,
        chronological_split_policy_after="not_yet_defined",
        label_family_eligibility_gate_authorized_after=False,
        successor_state_authorized=False,
        diagnostics_authorized=False,
        ml_authorized=False,
        strategy_authorized=False,
        backtest_authorized=False,
        acquisition_authorized=False,
        no_manifest_mutation=True,
        no_successor_state_created=True,
        no_label_recomputation=True,
        no_diagnostics_computed=True,
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
    report: MultidayLabelGateReport,
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
    "MultidayLabelGateReport",
    "MultidayLabelGateReportError",
    "build_report",
    "write_gate_report",
]
