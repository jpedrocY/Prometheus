"""Phase 4bj-E label-gate report data model tests.

Tests the invariant enforcement of :func:`write_label_gate_report` and
the structural shape of :class:`LabelGateReport`.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.label_gate_report import (
    LabelGateReport,
    LabelGateReportError,
    build_label_gate_report,
    write_label_gate_report,
)


def _build_minimal_report(**overrides) -> LabelGateReport:
    base = dict(
        report_id="microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1__000000000000",
        dataset_family="microstructure_labels_aggtrades_v001",
        dataset_version="v001",
        label_schema_version="v001",
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        generated_at_unix_ms=1,
        code_commit_sha="0" * 40,
        input_artefacts={"x": "y"},
        expected_row_count=1_681_098,
        observed_row_count=1_681_098,
        expected_schema_columns=["a"],
        observed_schema_columns=["a"],
        expected_label_columns=["a"],
        observed_label_columns=["a"],
        expected_support_columns=["b"],
        observed_support_columns=["b"],
        expected_lineage_columns=["c"],
        observed_lineage_columns=["c"],
        label_config_hash="0" * 64,
        expected_invalid_price_row_count=0,
        observed_invalid_price_row_count=0,
        expected_censored_per_horizon={"1s": 1},
        observed_censored_per_horizon={"1s": 1},
        checks=[{"status": "pass"}, {"status": "fail"}],
        overall_status="pass",
        eligibility_gate_status_after="pass_report_level_only",
        boundary_confirmations={"k": True},
        measured_summary={"m": 1},
    )
    base.update(overrides)
    return build_label_gate_report(**base)


def test_build_label_gate_report_counts_statuses() -> None:
    report = _build_minimal_report()
    assert report.checks_total == 2
    assert report.checks_pass == 1
    assert report.checks_fail == 1
    assert report.checks_error == 0
    assert report.checks_not_applicable == 0


def test_build_label_gate_report_invariants() -> None:
    report = _build_minimal_report()
    assert report.research_eligible_before is False
    assert report.research_eligible_after is False
    assert report.eligibility_gate_status_before == "pending"
    assert report.label_manifest_research_eligible_after is False
    assert report.label_manifest_eligibility_gate_status_after == "pending"
    assert (
        report.label_manifest_chronological_split_policy_after == "not_yet_defined"
    )
    assert report.chronological_split_policy_after == "not_yet_defined"
    assert report.stage_5_authorized is False
    assert report.stage_5_research_or_ml_use is False
    assert report.no_successor_authorization is True


def test_write_label_gate_report_writes_under_labels_namespace(
    tmp_path: Path,
) -> None:
    report = _build_minimal_report()
    output_root = (
        tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    )
    output_root.mkdir(parents=True, exist_ok=True)
    paths, sha, size = write_label_gate_report(report, output_root=output_root)
    assert paths.report_path.exists()
    assert paths.sidecar_path.exists()
    payload = json.loads(paths.report_path.read_bytes().decode("utf-8"))
    assert payload["phase_id"] == "4bj-E"
    assert payload["dataset_family"] == "microstructure_labels_aggtrades_v001"
    assert payload["research_eligible_after"] is False
    assert payload["label_manifest_research_eligible_after"] is False
    assert payload["label_manifest_eligibility_gate_status_after"] == "pending"
    assert (
        payload["label_manifest_chronological_split_policy_after"]
        == "not_yet_defined"
    )
    assert payload["no_successor_authorization"] is True
    assert size > 0
    assert len(sha) == 64


def test_write_label_gate_report_refuses_overwrite(tmp_path: Path) -> None:
    report = _build_minimal_report()
    output_root = (
        tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    )
    output_root.mkdir(parents=True, exist_ok=True)
    paths, _sha, _size = write_label_gate_report(report, output_root=output_root)
    # Re-running with same generated_at_unix_ms + code_commit_sha derives same path.
    from prometheus.research.microstructure.label_gate_io import LabelGateIOError

    with pytest.raises(LabelGateIOError):
        write_label_gate_report(report, output_root=output_root)
    assert paths.report_path.exists()


@pytest.mark.parametrize(
    "kwargs",
    [
        # research_eligible_after invariant
        # We construct a frozen dataclass directly to bypass the builder
        # and force a violation, then call the writer.
    ],
)
def test_write_label_gate_report_invariant_violations_param(kwargs) -> None:
    """Parametrised placeholder (kept for symmetry with sibling test files).

    The actual invariant-violation tests use ``dataclasses.replace`` to
    flip one invariant at a time and confirm the writer raises.
    """
    # The empty parametrize() above means this test is collected but
    # not run. The real invariant tests are below.
    pytest.skip("see explicit invariant violation tests below")


def _frozen_replace(report: LabelGateReport, **overrides: object) -> LabelGateReport:
    """Helper to flip an invariant on a frozen LabelGateReport."""
    import dataclasses

    return dataclasses.replace(report, **overrides)


def test_write_label_gate_report_rejects_research_eligible_after_true(
    tmp_path: Path,
) -> None:
    report = _frozen_replace(_build_minimal_report(), research_eligible_after=True)
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelGateReportError):
        write_label_gate_report(report, output_root=out)


def test_write_label_gate_report_rejects_manifest_research_eligible_after_true(
    tmp_path: Path,
) -> None:
    report = _frozen_replace(
        _build_minimal_report(), label_manifest_research_eligible_after=True
    )
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelGateReportError):
        write_label_gate_report(report, output_root=out)


def test_write_label_gate_report_rejects_manifest_egs_after_non_pending(
    tmp_path: Path,
) -> None:
    report = _frozen_replace(
        _build_minimal_report(),
        label_manifest_eligibility_gate_status_after="pass",
    )
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelGateReportError):
        write_label_gate_report(report, output_root=out)


def test_write_label_gate_report_rejects_manifest_csp_after_not_not_yet_defined(
    tmp_path: Path,
) -> None:
    report = _frozen_replace(
        _build_minimal_report(),
        label_manifest_chronological_split_policy_after="defined",
    )
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelGateReportError):
        write_label_gate_report(report, output_root=out)


def test_write_label_gate_report_rejects_stage_5_authorized_true(
    tmp_path: Path,
) -> None:
    report = _frozen_replace(_build_minimal_report(), stage_5_authorized=True)
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelGateReportError):
        write_label_gate_report(report, output_root=out)


def test_write_label_gate_report_rejects_stage_5_research_or_ml_use_true(
    tmp_path: Path,
) -> None:
    report = _frozen_replace(
        _build_minimal_report(), stage_5_research_or_ml_use=True
    )
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelGateReportError):
        write_label_gate_report(report, output_root=out)


def test_write_label_gate_report_rejects_no_successor_authorization_false(
    tmp_path: Path,
) -> None:
    report = _frozen_replace(
        _build_minimal_report(), no_successor_authorization=False
    )
    out = tmp_path / "data" / "microstructure" / "gate-reports" / "labels"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(LabelGateReportError):
        write_label_gate_report(report, output_root=out)
