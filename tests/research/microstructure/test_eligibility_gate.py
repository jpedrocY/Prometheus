"""Phase 4bb-C orchestrator-level tests for the offline aggTrades eligibility gate.

All tests are offline and use ``pytest tmp_path`` only. They never touch the
real project ``data/microstructure/`` tree.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

# Local import shim: place tests/research/microstructure on the path so we can
# import the shared fixture builder without making it a package member.
sys.path.insert(0, str(Path(__file__).parent))
from _eligibility_fixtures import (  # noqa: E402
    build_happy_fixture,
    sha256_of_file,
)

from prometheus.research.microstructure import (  # noqa: E402
    AggTradesEligibilityCheckStatus,
    AggTradesEligibilityGateInput,
    AggTradesGateInputError,
    AggTradesGateUnsupportedError,
    EligibilityGateStatus,
    run_eligibility_gate,
)


def _git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()


def test_run_eligibility_gate_passes_on_happy_mini_fixture(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    inp = AggTradesEligibilityGateInput(
        manifest_path=fb.manifest_path,
        output_root=fb.output_root,
        code_commit_sha=sha,
    )
    res = run_eligibility_gate(inp)

    assert res.overall_status is AggTradesEligibilityCheckStatus.PASS
    assert res.research_eligible_after is False
    assert res.eligibility_gate_status_after is EligibilityGateStatus.PASS
    assert res.no_successor_authorization is True
    assert len(res.checks) == 45
    assert all(
        c.status in (
            AggTradesEligibilityCheckStatus.PASS,
            AggTradesEligibilityCheckStatus.NOT_APPLICABLE,
        )
        for c in res.checks
    )
    assert res.report_path is not None
    assert res.report_path.exists()
    assert res.report_path.suffix == ".json"


def test_report_writes_under_gate_reports_subdirectory(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
        )
    )
    assert res.report_path is not None
    assert res.report_path.parent.name == "gate-reports"
    assert res.report_path.parent.parent.name == "microstructure"
    sidecar = res.report_path.with_suffix(".json.sha256")
    assert sidecar.exists()


def test_run_eligibility_gate_does_not_mutate_original_manifest(
    tmp_path: Path,
) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    before = sha256_of_file(fb.manifest_path)
    run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
        )
    )
    after = sha256_of_file(fb.manifest_path)
    assert before == after


def test_run_eligibility_gate_does_not_mutate_raw_zip_or_sidecar(
    tmp_path: Path,
) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    zip_before = sha256_of_file(fb.raw_zip_path)
    sidecar_before = fb.sidecar_path.read_text(encoding="utf-8")
    run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
        )
    )
    assert sha256_of_file(fb.raw_zip_path) == zip_before
    assert fb.sidecar_path.read_text(encoding="utf-8") == sidecar_before


def test_research_eligible_after_is_false_for_raw_family(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
        )
    )
    assert res.research_eligible_after is False


def test_exactly_45_checks_in_result(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
        )
    )
    ids = [c.check_id for c in res.checks]
    assert len(ids) == 45
    assert len(set(ids)) == 45


def test_write_successor_manifest_true_is_rejected(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    with pytest.raises(AggTradesGateUnsupportedError):
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_successor_manifest=True,
        )


def test_output_root_outside_data_microstructure_rejected(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    bad_output = tmp_path / "elsewhere"
    bad_output.mkdir(parents=True, exist_ok=True)
    inp = AggTradesEligibilityGateInput(
        manifest_path=fb.manifest_path,
        output_root=bad_output,
        code_commit_sha=sha,
    )
    from prometheus.research.microstructure import GateIOError

    with pytest.raises(GateIOError):
        run_eligibility_gate(inp)


def test_input_requires_pathlib_paths(tmp_path: Path) -> None:
    with pytest.raises(AggTradesGateInputError):
        AggTradesEligibilityGateInput(
            manifest_path="not_a_path",  # type: ignore[arg-type]
            output_root=tmp_path,
            code_commit_sha="abc",
        )
    with pytest.raises(AggTradesGateInputError):
        AggTradesEligibilityGateInput(
            manifest_path=tmp_path,
            output_root="not_a_path",  # type: ignore[arg-type]
            code_commit_sha="abc",
        )
    with pytest.raises(AggTradesGateInputError):
        AggTradesEligibilityGateInput(
            manifest_path=tmp_path,
            output_root=tmp_path,
            code_commit_sha="",
        )


def test_rerunning_gate_does_not_overwrite_existing_report(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    inp = AggTradesEligibilityGateInput(
        manifest_path=fb.manifest_path,
        output_root=fb.output_root,
        code_commit_sha=sha,
    )
    first = run_eligibility_gate(inp)
    assert first.report_path is not None and first.report_path.exists()

    # The second run must produce a distinct report_id (created_at_utc_ms
    # differs across calls). To reliably observe a distinct report path, we
    # avoid stamp collision by passing a slightly different code_commit_sha.
    inp2 = AggTradesEligibilityGateInput(
        manifest_path=fb.manifest_path,
        output_root=fb.output_root,
        code_commit_sha=sha + "x",
    )
    second = run_eligibility_gate(inp2)
    assert second.report_path is not None and second.report_path.exists()
    assert second.report_path != first.report_path


def test_rerun_on_same_input_yields_same_overall_status(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    a = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    b = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    assert a.overall_status is b.overall_status


def test_boundary_confirmations_all_true_on_pass(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
        )
    )
    for k, v in res.boundary_confirmations.items():
        assert v is True, f"boundary {k} should be True on PASS"


def test_no_successor_authorization_invariant(tmp_path: Path) -> None:
    sha = _git_head()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    assert res.no_successor_authorization is True
