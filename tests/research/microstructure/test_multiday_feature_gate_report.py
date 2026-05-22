"""Phase 4bm-J report builder + verdict classification unit tests."""
# ruff: noqa: E501  (Phase 4bm-J: long v002 SHA literals + lineage column names)
from __future__ import annotations

from pathlib import Path

import pytest

from prometheus.research.microstructure.multiday_feature_gate_checks import (
    MultidayFeatureGateCheckResult,
    MultidayFeatureGateCheckStatus,
)
from prometheus.research.microstructure.multiday_feature_gate_report import (
    ALLOWED_GATE_VERDICTS,
    GATE_VERDICT_FAIL,
    GATE_VERDICT_INDETERMINATE,
    GATE_VERDICT_PASS,
    MultidayFeatureGateReport,
    MultidayFeatureGateReportError,
    _classify_gate_verdict,
    build_report,
)


def _make_result(check_id: str, status: MultidayFeatureGateCheckStatus, blocking: bool = True) -> MultidayFeatureGateCheckResult:
    return MultidayFeatureGateCheckResult(
        check_id=check_id, group="X", status=status, blocking=blocking,
    )


def test_classify_pass_all_pass() -> None:
    rs = [_make_result(f"A{i}", MultidayFeatureGateCheckStatus.PASS) for i in range(10)]
    v, p, f, e, na, blocking = _classify_gate_verdict(rs)
    assert v == GATE_VERDICT_PASS
    assert p == 10 and f == 0 and e == 0 and na == 0 and blocking == 0


def test_classify_fail_one_blocking() -> None:
    rs = [_make_result(f"A{i}", MultidayFeatureGateCheckStatus.PASS) for i in range(9)] + [
        _make_result("X1", MultidayFeatureGateCheckStatus.FAIL, blocking=True)
    ]
    v, p, f, e, na, blocking = _classify_gate_verdict(rs)
    assert v == GATE_VERDICT_FAIL
    assert f == 1 and blocking == 1


def test_classify_indeterminate_error_only() -> None:
    rs = [_make_result(f"A{i}", MultidayFeatureGateCheckStatus.PASS) for i in range(9)] + [
        _make_result("E1", MultidayFeatureGateCheckStatus.ERROR, blocking=True)
    ]
    v, _, _, _, _, _ = _classify_gate_verdict(rs)
    assert v == GATE_VERDICT_INDETERMINATE


def test_classify_not_applicable_count() -> None:
    rs = [_make_result(f"A{i}", MultidayFeatureGateCheckStatus.PASS) for i in range(5)] + [
        _make_result("N1", MultidayFeatureGateCheckStatus.NOT_APPLICABLE, blocking=False)
    ]
    v, p, f, e, na, blocking = _classify_gate_verdict(rs)
    assert v == GATE_VERDICT_PASS
    assert na == 1


def test_allowed_verdicts() -> None:
    assert frozenset({GATE_VERDICT_PASS, GATE_VERDICT_FAIL, GATE_VERDICT_INDETERMINATE}) == ALLOWED_GATE_VERDICTS


def _build_pass_report(tmp_path: Path) -> MultidayFeatureGateReport:
    rs = tuple(_make_result(f"A{i}", MultidayFeatureGateCheckStatus.PASS) for i in range(50))
    manifest = {"actual_feature_row_count": 155_153_449}
    return build_report(
        results=rs,
        manifest=manifest,
        feature_manifest_path=tmp_path / "f.json",
        created_at_utc_ms=1_700_000_000_000,
        code_commit_sha="0" * 40,
        feature_parquet_count=90,
        feature_sidecar_count=90,
    )


def test_build_report_pass_verdict(tmp_path: Path) -> None:
    rep = _build_pass_report(tmp_path)
    assert rep.gate_verdict == GATE_VERDICT_PASS
    assert rep.pass_count == 50
    assert rep.fail_count == 0
    assert rep.blocking_fail_count == 0
    assert rep.research_eligible_after is False
    assert rep.eligibility_gate_status_after == "pending"
    assert rep.stage_4_feature_cleared_after is False
    assert rep.no_manifest_mutation is True
    assert rep.feature_family_research_use_authorized is False
    assert rep.successor_state_authorized is False
    assert rep.no_network_io is True


def test_build_report_to_dict_includes_required_fields(tmp_path: Path) -> None:
    rep = _build_pass_report(tmp_path)
    d = rep.to_dict()
    required = {
        "report_schema_version", "phase_id", "phase_name", "created_at_utc_ms",
        "dataset_family", "dataset_version", "feature_schema_version", "symbol",
        "utc_date_start", "utc_date_end", "date_count", "expected_feature_row_count",
        "actual_feature_row_count", "feature_manifest_path", "feature_manifest_sha256",
        "feature_manifest_sidecar_sha256", "feature_config_hash", "feature_parquet_count",
        "feature_sidecar_count", "feature_schema_column_count", "lineage_column_count",
        "feature_column_count", "structural_qa_phase", "structural_qa_verdict",
        "source_successor_state_sha256", "source_normalized_manifest_sha256",
        "source_phase_4bm_d_gate_report_sha256", "gate_verdict", "overall_status",
        "pass_count", "fail_count", "error_count", "not_applicable_count",
        "blocking_fail_count", "checks", "boundary_confirmations",
        "research_eligible_after", "eligibility_gate_status_after",
        "stage_4_feature_cleared_after", "feature_family_research_use_authorized",
        "successor_state_authorized", "label_computation_authorized",
        "diagnostics_authorized", "ml_authorized", "strategy_authorized",
        "backtest_authorized", "acquisition_authorized",
        "no_manifest_mutation", "no_successor_state_created", "no_feature_recomputation",
        "no_label_computed", "no_signal_computed", "no_ml_trained", "no_strategy_created",
        "no_backtest_run", "no_network_io", "no_credentials", "no_mcp_or_graphify",
        "no_exchange_write", "retained_verdicts_preserved", "governance_locks_preserved",
        "notes",
    }
    assert required.issubset(d.keys())
    assert d["phase_id"] == "4bm-J"
    assert d["dataset_version"] == "v002"
    assert d["feature_schema_version"] == "v001"
    assert d["symbol"] == "BTCUSDT"
    assert d["date_count"] == 90
    assert d["expected_feature_row_count"] == 155_153_449
    assert d["feature_schema_column_count"] == 62
    assert d["lineage_column_count"] == 17
    assert d["feature_column_count"] == 45


def test_build_report_fail_verdict(tmp_path: Path) -> None:
    rs = tuple(
        _make_result(f"A{i}", MultidayFeatureGateCheckStatus.PASS) for i in range(49)
    ) + (_make_result("X", MultidayFeatureGateCheckStatus.FAIL, blocking=True),)
    rep = build_report(
        results=rs,
        manifest={"actual_feature_row_count": 0},
        feature_manifest_path=tmp_path / "f.json",
        created_at_utc_ms=1,
        code_commit_sha="0" * 40,
        feature_parquet_count=0,
        feature_sidecar_count=0,
    )
    assert rep.gate_verdict == GATE_VERDICT_FAIL
    assert rep.overall_status == "fail"
    assert rep.blocking_fail_count == 1
    # Invariants must still hold on FAIL.
    assert rep.research_eligible_after is False
    assert rep.eligibility_gate_status_after == "pending"


def test_build_report_invariants_never_relaxed(tmp_path: Path) -> None:
    # Invariants are enforced even in the PASS shape; we cannot construct a
    # report whose research_eligible_after=True.
    with pytest.raises(MultidayFeatureGateReportError):
        MultidayFeatureGateReport(
            report_schema_version="v001", phase_id="4bm-J", phase_name="x",
            created_at_utc_ms=1, dataset_family="x", dataset_version="v002",
            feature_schema_version="v001", symbol="BTCUSDT",
            utc_date_start="2024-12-01", utc_date_end="2025-02-28", date_count=90,
            expected_feature_row_count=1, actual_feature_row_count=1,
            feature_manifest_path="x", feature_manifest_sha256="a" * 64,
            feature_manifest_sidecar_sha256="b" * 64, feature_config_hash="c" * 64,
            feature_parquet_count=90, feature_sidecar_count=90,
            feature_schema_column_count=62, lineage_column_count=17, feature_column_count=45,
            structural_qa_phase="4bm-I", structural_qa_verdict="FEATURE_STRUCTURAL_QA_PASS",
            source_successor_state_sha256="d" * 64,
            source_phase_4bl_d_r_raw_gate_report_sha256="e" * 64,
            source_phase_4bl_e_raw_successor_state_sha256="f" * 64,
            source_normalized_manifest_sha256="9" * 64,
            source_raw_manifest_sha256="8" * 64,
            source_phase_4bm_d_gate_report_sha256="7" * 64,
            gate_verdict=GATE_VERDICT_PASS, overall_status="pass",
            pass_count=1, fail_count=0, error_count=0, not_applicable_count=0,
            blocking_fail_count=0, checks=(),
            boundary_confirmations={"x": True},
            research_eligible_after=True,  # <-- INVALID
            eligibility_gate_status_after="pending",
            stage_4_feature_cleared_after=False,
            feature_family_research_use_authorized=False,
            successor_state_authorized=False,
            label_computation_authorized=False, diagnostics_authorized=False,
            ml_authorized=False, strategy_authorized=False,
            backtest_authorized=False, acquisition_authorized=False,
            no_manifest_mutation=True, no_successor_state_created=True,
            no_feature_recomputation=True, no_label_computed=True,
            no_signal_computed=True, no_ml_trained=True, no_strategy_created=True,
            no_backtest_run=True, no_network_io=True, no_credentials=True,
            no_mcp_or_graphify=True, no_exchange_write=True,
            retained_verdicts_preserved=True, governance_locks_preserved=True,
            code_commit_sha="0" * 40, notes="x",
        )
