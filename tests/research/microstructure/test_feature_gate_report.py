"""Phase 4bi-B tests for the feature-gate report data model + writer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.feature_gate_io import FeatureGateIOError
from prometheus.research.microstructure.feature_gate_report import (
    PHASE_ID,
    REPORT_SCHEMA_VERSION,
    FeatureGateReport,
    FeatureGateReportError,
    build_feature_gate_report,
    write_feature_gate_report,
)


def _sample_checks() -> list[dict[str, object]]:
    return [
        {
            "check_id": "4bi-b.A01",
            "group": "A",
            "title": "feature parquet exists",
            "status": "pass",
            "detail": "ok",
        },
        {
            "check_id": "4bi-b.A02",
            "group": "A",
            "title": "feature parquet sidecar exists",
            "status": "pass",
            "detail": "ok",
        },
        {
            "check_id": "4bi-b.C08",
            "group": "C",
            "title": "research_eligible false",
            "status": "fail",
            "detail": "actual=True",
        },
    ]


def _build_report(*, overall: str = "pass") -> FeatureGateReport:
    return build_feature_gate_report(
        report_id="r-test",
        dataset_family="microstructure_features_aggtrades_v001",
        dataset_version="v001",
        feature_schema_version="v001",
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        generated_at_unix_ms=1_700_000_000_000,
        code_commit_sha="abcdef0123456789",
        input_artefacts={"k": "v"},
        expected_row_count=10,
        observed_row_count=10,
        expected_schema_columns=["a"],
        observed_schema_columns=["a"],
        expected_feature_columns=["a"],
        observed_feature_columns=["a"],
        expected_lineage_columns=[],
        observed_lineage_columns=[],
        feature_config_hash="e" * 64,
        checks=_sample_checks(),
        overall_status=overall,
        eligibility_gate_status_after="pass_report_level_only",
        boundary_confirmations={"no_feature_manifest_mutation": True},
        measured_summary={"observed": 10},
    )


def test_build_report_locks_invariants() -> None:
    rpt = _build_report()
    assert rpt.report_schema_version == REPORT_SCHEMA_VERSION
    assert rpt.phase_id == PHASE_ID
    assert rpt.research_eligible_after is False
    assert rpt.research_eligible_before is False
    assert rpt.eligibility_gate_status_before == "pending"
    assert rpt.feature_manifest_research_eligible_after is False
    assert rpt.feature_manifest_eligibility_gate_status_after == "pending"
    assert rpt.stage_5_authorized is False
    assert rpt.stage_5_research_or_ml_use is False
    assert rpt.no_successor_authorization is True


def test_build_report_counts_check_statuses() -> None:
    rpt = _build_report()
    assert rpt.checks_total == 3
    assert rpt.checks_pass == 2
    assert rpt.checks_fail == 1
    assert rpt.checks_error == 0
    assert rpt.checks_not_applicable == 0


def test_write_feature_gate_report_writes_atomically(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "features"
    output_root.mkdir(parents=True, exist_ok=True)
    rpt = _build_report()
    paths, sha, size = write_feature_gate_report(
        rpt, output_root=output_root, refuse_overwrite=True
    )
    assert paths.report_path.exists()
    assert paths.sidecar_path.exists()
    on_disk = paths.report_path.read_bytes()
    assert size == len(on_disk)
    parsed = json.loads(on_disk.decode("utf-8"))
    assert parsed["phase_id"] == "4bi-B"
    assert parsed["dataset_family"] == "microstructure_features_aggtrades_v001"
    assert parsed["overall_status"] == "pass"
    sidecar_text = paths.sidecar_path.read_text(encoding="utf-8")
    assert sidecar_text.startswith(sha)
    assert paths.report_path.name in sidecar_text


def test_write_feature_gate_report_refuses_overwrite(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "features"
    output_root.mkdir(parents=True, exist_ok=True)
    rpt = _build_report()
    write_feature_gate_report(rpt, output_root=output_root, refuse_overwrite=True)
    with pytest.raises(FeatureGateIOError):
        write_feature_gate_report(rpt, output_root=output_root, refuse_overwrite=True)


def test_write_feature_gate_report_rejects_outside_namespace(tmp_path: Path) -> None:
    rpt = _build_report()
    with pytest.raises(FeatureGateIOError):
        write_feature_gate_report(
            rpt,
            output_root=tmp_path / "elsewhere",
            refuse_overwrite=True,
        )


def test_write_feature_gate_report_rejects_research_eligible_mutation(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports" / "features"
    output_root.mkdir(parents=True, exist_ok=True)
    rpt = _build_report()
    bad = FeatureGateReport(
        report_schema_version=rpt.report_schema_version,
        phase_id=rpt.phase_id,
        report_id=rpt.report_id,
        dataset_family=rpt.dataset_family,
        dataset_version=rpt.dataset_version,
        feature_schema_version=rpt.feature_schema_version,
        symbol=rpt.symbol,
        utc_date=rpt.utc_date,
        generated_at_unix_ms=rpt.generated_at_unix_ms,
        code_commit_sha=rpt.code_commit_sha,
        input_artefacts=rpt.input_artefacts,
        expected_row_count=rpt.expected_row_count,
        observed_row_count=rpt.observed_row_count,
        expected_schema_columns=rpt.expected_schema_columns,
        observed_schema_columns=rpt.observed_schema_columns,
        expected_feature_columns=rpt.expected_feature_columns,
        observed_feature_columns=rpt.observed_feature_columns,
        expected_lineage_columns=rpt.expected_lineage_columns,
        observed_lineage_columns=rpt.observed_lineage_columns,
        feature_config_hash=rpt.feature_config_hash,
        checks=rpt.checks,
        checks_total=rpt.checks_total,
        checks_pass=rpt.checks_pass,
        checks_fail=rpt.checks_fail,
        checks_error=rpt.checks_error,
        checks_not_applicable=rpt.checks_not_applicable,
        overall_status=rpt.overall_status,
        research_eligible_before=rpt.research_eligible_before,
        research_eligible_after=True,  # forbidden
        eligibility_gate_status_before=rpt.eligibility_gate_status_before,
        eligibility_gate_status_after=rpt.eligibility_gate_status_after,
        feature_manifest_research_eligible_after=False,
        feature_manifest_eligibility_gate_status_after="pending",
        stage_5_authorized=False,
        stage_5_research_or_ml_use=False,
        no_successor_authorization=True,
        boundary_confirmations=rpt.boundary_confirmations,
        measured_summary=rpt.measured_summary,
    )
    with pytest.raises(FeatureGateReportError):
        write_feature_gate_report(bad, output_root=output_root, refuse_overwrite=True)
