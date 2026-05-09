"""Phase 4bf gate-report data-model + atomic writer tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from prometheus.research.microstructure.derived_gate_io import (
    GateIOError,
    compute_file_sha256,
)
from prometheus.research.microstructure.derived_gate_report import (
    PHASE_ID,
    REPORT_SCHEMA_VERSION,
    DerivedAggTradesGateReport,
    build_report,
    write_gate_report,
)


def _output_root(tmp_path: Path) -> Path:
    root = tmp_path / "data" / "microstructure" / "gate-reports" / "normalized"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _build_default_report() -> DerivedAggTradesGateReport:
    return build_report(
        report_id="microstructure_normalized_aggtrades_v001__v001__1700000000000__testcommit01",
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v001",
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        generated_at_unix_ms=1_700_000_000_000,
        code_commit_sha="testcommit01abcdef",
        input_artefacts={"derived_manifest_path": "x"},
        checks=[{"check_id": "4bf.13.1", "status": "pass"}],
        overall_status="pass",
        eligibility_gate_status_after="pass",
        boundary_confirmations={"no_manifest_mutation": True},
        measured_summary={"row_count": 5},
    )


def test_build_report_records_invariants_and_phase_id() -> None:
    report = _build_default_report()
    assert report.research_eligible_after is False
    assert report.no_successor_authorization is True
    assert report.phase_id == PHASE_ID == "4bf"
    assert report.report_schema_version == REPORT_SCHEMA_VERSION == "v001"


def test_build_report_to_dict_returns_serialisable_payload() -> None:
    report = _build_default_report()
    payload = report.to_dict()
    text = json.dumps(payload, sort_keys=True)
    assert "research_eligible_after" in text
    assert payload["research_eligible_after"] is False
    assert payload["no_successor_authorization"] is True


def test_write_gate_report_writes_json_and_sidecar(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    paths, sha, size = write_gate_report(report, output_root=output_root)
    assert paths.report_path.exists()
    assert paths.sidecar_path.exists()
    assert size > 0
    assert sha == compute_file_sha256(paths.report_path)
    sidecar_text = paths.sidecar_path.read_text(encoding="utf-8").strip()
    assert sidecar_text == f"{sha}  {paths.report_path.name}"


def test_write_gate_report_refuses_overwrite(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    write_gate_report(report, output_root=output_root)
    with pytest.raises(GateIOError):
        write_gate_report(report, output_root=output_root)


def test_write_gate_report_path_is_under_normalized_namespace(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    report = _build_default_report()
    paths, _sha, _size = write_gate_report(report, output_root=output_root)
    parts = paths.report_path.resolve().parts
    assert parts[-5:-1] == ("data", "microstructure", "gate-reports", "normalized")


def test_write_gate_report_rejects_research_eligible_after_true(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    # Build via the unsafe constructor so we can set the bad value.
    bad = DerivedAggTradesGateReport(
        report_schema_version=REPORT_SCHEMA_VERSION,
        phase_id=PHASE_ID,
        report_id="x",
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v001",
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        generated_at_unix_ms=1,
        code_commit_sha="abc",
        input_artefacts={},
        checks=[],
        overall_status="pass",
        research_eligible_after=True,  # ← violates the invariant
        eligibility_gate_status_after="pass",
        no_successor_authorization=True,
        boundary_confirmations={},
        measured_summary={},
    )
    with pytest.raises(GateIOError, match="research_eligible_after"):
        write_gate_report(bad, output_root=output_root)


def test_write_gate_report_rejects_no_successor_authorization_false(tmp_path: Path) -> None:
    output_root = _output_root(tmp_path)
    bad = DerivedAggTradesGateReport(
        report_schema_version=REPORT_SCHEMA_VERSION,
        phase_id=PHASE_ID,
        report_id="x",
        dataset_family="microstructure_normalized_aggtrades_v001",
        dataset_version="v001",
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        generated_at_unix_ms=1,
        code_commit_sha="abc",
        input_artefacts={},
        checks=[],
        overall_status="pass",
        research_eligible_after=False,
        eligibility_gate_status_after="pass",
        no_successor_authorization=False,  # ← violates the invariant
        boundary_confirmations={},
        measured_summary={},
    )
    with pytest.raises(GateIOError, match="no_successor_authorization"):
        write_gate_report(bad, output_root=output_root)
