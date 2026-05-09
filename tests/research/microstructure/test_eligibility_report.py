"""Phase 4bb-C tests for the gate-report data model and atomic JSON write."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from _eligibility_fixtures import build_happy_fixture  # noqa: E402

from prometheus.research.microstructure import (  # noqa: E402
    AggTradesEligibilityGateInput,
    AggTradesGateReport,
    GateIOError,
    run_eligibility_gate,
)
from prometheus.research.microstructure.eligibility_report import (  # noqa: E402
    write_report_atomic,
)


def _make_report(report_id: str = "x__v001__1__abc") -> AggTradesGateReport:
    return AggTradesGateReport(
        report_id=report_id,
        dataset_family="microstructure_raw_aggtrades_v001",
        version="v001",
        symbol="BTCUSDT",
        source_manifest_path="data/microstructure/manifests/m.json",
        raw_zip_path="data/microstructure/raw/.../x.zip",
        sidecar_path="data/microstructure/raw/.../x.zip.sha256",
        acquisition_log_path="data/microstructure/manifests/m_acquisition_log.json",
        created_at_utc_ms=1,
        code_commit_sha="abc",
        overall_status="pass",
        research_eligible_after=False,
        eligibility_gate_status_after="pass",
        checks=(),
        invalid_window_candidates=(),
        measured_summary={"row_count": 0},
        boundary_confirmations={"no_network_io": True},
        no_successor_authorization=True,
    )


def test_to_dict_round_trips_through_json(tmp_path: Path) -> None:
    report = _make_report()
    body = json.dumps(report.to_dict(), sort_keys=True)
    parsed = json.loads(body)
    assert parsed["report_id"] == "x__v001__1__abc"
    assert parsed["research_eligible_after"] is False
    assert parsed["no_successor_authorization"] is True


def test_write_report_atomic_writes_under_gate_reports(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True, exist_ok=True)
    report = _make_report()
    written = write_report_atomic(report, output_root)
    assert written.exists()
    assert written.parent.name == "gate-reports"
    sidecar = written.with_suffix(".json.sha256")
    assert sidecar.exists()
    sha = hashlib.sha256(written.read_bytes()).hexdigest()
    assert sha in sidecar.read_text(encoding="utf-8")


def test_write_report_atomic_rejects_paths_outside_microstructure(tmp_path: Path) -> None:
    bad = tmp_path / "elsewhere"
    bad.mkdir(parents=True, exist_ok=True)
    with pytest.raises(GateIOError):
        write_report_atomic(_make_report(), bad)


def test_write_report_atomic_refuses_overwrite(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True, exist_ok=True)
    report = _make_report("samename")
    write_report_atomic(report, output_root)
    with pytest.raises(FileExistsError):
        write_report_atomic(report, output_root)


def test_full_gate_report_has_all_required_fields(tmp_path: Path) -> None:
    import subprocess

    sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
        )
    )
    assert res.report_path is not None
    payload = json.loads(res.report_path.read_text(encoding="utf-8"))
    required = {
        "report_id",
        "dataset_family",
        "version",
        "symbol",
        "source_manifest_path",
        "raw_zip_path",
        "sidecar_path",
        "acquisition_log_path",
        "created_at_utc_ms",
        "code_commit_sha",
        "overall_status",
        "research_eligible_after",
        "eligibility_gate_status_after",
        "checks",
        "invalid_window_candidates",
        "measured_summary",
        "boundary_confirmations",
        "no_successor_authorization",
    }
    assert required.issubset(set(payload))
    assert payload["research_eligible_after"] is False
    assert payload["no_successor_authorization"] is True
    assert len(payload["checks"]) == 45
