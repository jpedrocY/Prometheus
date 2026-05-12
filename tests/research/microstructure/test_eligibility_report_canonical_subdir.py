"""Phase 4bb-F-implementation tests for the optional ``family_subdir`` kwarg.

These tests exercise the new keyword argument threaded through:

- :func:`prometheus.research.microstructure.eligibility_report.write_report_atomic`
  (direct writer);
- :class:`prometheus.research.microstructure.AggTradesEligibilityGateInput`
  and :func:`prometheus.research.microstructure.run_eligibility_gate`
  (orchestrator integration).

Backward-compatibility expectations verified here:

- when ``family_subdir`` is omitted (the default), the writer still
  composes the legacy ``<output_root>/gate-reports/<report_id>.json``
  placement exactly as Phase 4bb-C does -- this is what the Phase 4bb-D
  recorded report depends on;
- when ``family_subdir`` is supplied (e.g. ``"raw"``), the writer
  skips the ``gate-reports`` subdir injection and composes
  ``<output_root>/<family_subdir>/<report_id>.json`` directly.

These tests never touch the project's real ``data/microstructure/`` --
they use pytest ``tmp_path`` exclusively. They never read or write
``data/microstructure/`` under the repository.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from _eligibility_fixtures import build_happy_fixture  # noqa: E402

from prometheus.research.microstructure import (  # noqa: E402
    AggTradesEligibilityGateInput,
    AggTradesGateInputError,
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


def test_write_report_atomic_default_preserves_legacy_subdir(
    tmp_path: Path,
) -> None:
    """Backward-compatibility: ``family_subdir=None`` still writes under ``gate-reports/``."""
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True, exist_ok=True)
    written = write_report_atomic(_make_report("legacy_id"), output_root)
    assert written.parent.name == "gate-reports"
    assert written.parent.parent == output_root


def test_write_report_atomic_with_family_subdir_uses_canonical_subdir(
    tmp_path: Path,
) -> None:
    """Phase 4bb-F-implementation: ``family_subdir='raw'`` writes under ``raw/``."""
    output_root = tmp_path / "data" / "microstructure" / "gate-reports"
    output_root.mkdir(parents=True, exist_ok=True)
    written = write_report_atomic(
        _make_report("canonical_id"),
        output_root,
        family_subdir="raw",
    )
    # Canonical placement: <output_root>/raw/<id>.json
    assert written.parent.name == "raw"
    assert written.parent.parent == output_root
    # NOT doubled: the legacy "gate-reports" subdir injection was skipped.
    assert written.parent.name != "gate-reports"


@pytest.mark.parametrize(
    "family,expected_subdir",
    [
        ("raw", "raw"),
        ("normalized", "normalized"),
        ("features", "features"),
        ("labels", "labels"),
    ],
)
def test_write_report_atomic_family_subdir_each_family(
    tmp_path: Path, family: str, expected_subdir: str
) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports"
    output_root.mkdir(parents=True, exist_ok=True)
    written = write_report_atomic(
        _make_report(f"id_{family}"),
        output_root,
        family_subdir=family,
    )
    assert written.parent.name == expected_subdir


def test_write_report_atomic_rejects_empty_family_subdir(tmp_path: Path) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(ValueError):
        write_report_atomic(
            _make_report("id_empty"),
            output_root,
            family_subdir="",
        )


@pytest.mark.parametrize("bad", ["raw/", "raw\\sub", "x/y", "a\\b"])
def test_write_report_atomic_rejects_family_subdir_with_separators(
    tmp_path: Path, bad: str
) -> None:
    output_root = tmp_path / "data" / "microstructure"
    output_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(ValueError):
        write_report_atomic(
            _make_report("id_sep"),
            output_root,
            family_subdir=bad,
        )


def test_write_report_atomic_still_validates_output_root(tmp_path: Path) -> None:
    """Even with ``family_subdir``, the output root must be under ``data/microstructure/``."""
    bad = tmp_path / "elsewhere"
    bad.mkdir(parents=True, exist_ok=True)
    with pytest.raises(GateIOError):
        write_report_atomic(
            _make_report("id_bad"),
            bad,
            family_subdir="raw",
        )


def test_write_report_atomic_with_family_subdir_writes_sidecar(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports"
    output_root.mkdir(parents=True, exist_ok=True)
    written = write_report_atomic(
        _make_report("id_sidecar"),
        output_root,
        family_subdir="raw",
    )
    sidecar = written.with_suffix(".json.sha256")
    assert sidecar.exists()
    body = written.read_bytes()
    sha = hashlib.sha256(body).hexdigest()
    text = sidecar.read_text(encoding="utf-8")
    assert sha in text
    assert written.name in text


def test_write_report_atomic_with_family_subdir_refuses_overwrite(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "data" / "microstructure" / "gate-reports"
    output_root.mkdir(parents=True, exist_ok=True)
    write_report_atomic(_make_report("same_id"), output_root, family_subdir="raw")
    with pytest.raises(FileExistsError):
        write_report_atomic(
            _make_report("same_id"), output_root, family_subdir="raw"
        )


def test_gate_input_default_family_subdir_is_none(tmp_path: Path) -> None:
    inp = AggTradesEligibilityGateInput(
        manifest_path=tmp_path / "data" / "microstructure" / "m.json",
        output_root=tmp_path / "data" / "microstructure",
        code_commit_sha="abc",
    )
    assert inp.family_subdir is None
    assert inp.phase_id is None


def test_gate_input_accepts_family_subdir_and_phase_id(tmp_path: Path) -> None:
    inp = AggTradesEligibilityGateInput(
        manifest_path=tmp_path / "data" / "microstructure" / "m.json",
        output_root=tmp_path / "data" / "microstructure" / "gate-reports",
        code_commit_sha="abc",
        family_subdir="raw",
        phase_id="4bb-F",
    )
    assert inp.family_subdir == "raw"
    assert inp.phase_id == "4bb-F"


@pytest.mark.parametrize("bad_fs", ["", "raw/", "raw\\sub"])
def test_gate_input_rejects_bad_family_subdir(tmp_path: Path, bad_fs: str) -> None:
    with pytest.raises(AggTradesGateInputError):
        AggTradesEligibilityGateInput(
            manifest_path=tmp_path / "data" / "microstructure" / "m.json",
            output_root=tmp_path / "data" / "microstructure",
            code_commit_sha="abc",
            family_subdir=bad_fs,
        )


def test_gate_input_rejects_empty_phase_id(tmp_path: Path) -> None:
    with pytest.raises(AggTradesGateInputError):
        AggTradesEligibilityGateInput(
            manifest_path=tmp_path / "data" / "microstructure" / "m.json",
            output_root=tmp_path / "data" / "microstructure",
            code_commit_sha="abc",
            phase_id="",
        )


def _current_commit_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()


def test_orchestrator_default_preserves_legacy_doubled_path(tmp_path: Path) -> None:
    """When ``family_subdir`` is None and ``output_root`` is the microstructure root,
    the orchestrator preserves the Phase 4bb-C placement
    ``<output_root>/gate-reports/<id>.json``.
    """
    sha = _current_commit_sha()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,  # tmp_path/data/microstructure
            code_commit_sha=sha,
        )
    )
    assert res.report_path is not None
    assert res.report_path.parent.name == "gate-reports"
    assert res.report_path.parent.parent == fb.output_root
    # Phase 4bb-C report-id format (no phase- tag).
    assert "phase-" not in res.report_id


def test_orchestrator_canonical_placement_with_family_subdir_and_phase_id(
    tmp_path: Path,
) -> None:
    """Phase 4bb-F-implementation: passing ``output_root=.../gate-reports`` AND
    ``family_subdir='raw'`` AND ``phase_id='4bb-F'`` produces canonical placement.
    """
    sha = _current_commit_sha()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    canonical_root = fb.microstructure_root / "gate-reports"
    canonical_root.mkdir(parents=True, exist_ok=True)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=canonical_root,
            code_commit_sha=sha,
            family_subdir="raw",
            phase_id="4bb-F",
        )
    )
    assert res.report_path is not None
    # Canonical placement: <microstructure_root>/gate-reports/raw/<id>.json
    assert res.report_path.parent.name == "raw"
    assert res.report_path.parent.parent == canonical_root
    # Canonical report-id format: contains "phase-4bb-F".
    assert "phase-4bb-F" in res.report_id
    # The doubled "gate-reports/gate-reports/" anomaly is gone:
    parts = res.report_path.resolve().parts
    seen = sum(1 for x in parts if x == "gate-reports")
    assert seen == 1


def test_orchestrator_canonical_report_id_short_commit_length_12(
    tmp_path: Path,
) -> None:
    sha = _current_commit_sha()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    canonical_root = fb.microstructure_root / "gate-reports"
    canonical_root.mkdir(parents=True, exist_ok=True)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=canonical_root,
            code_commit_sha=sha,
            family_subdir="raw",
            phase_id="X",
        )
    )
    assert res.report_path is not None
    # report_id format: <family>__<version>__phase-X__<unix_ms>__<short(12)>
    assert "__phase-X__" in res.report_id
    last_token = res.report_id.split("__")[-1]
    assert len(last_token) == 12


def test_orchestrator_canonical_writes_sidecar_with_two_space_format(
    tmp_path: Path,
) -> None:
    sha = _current_commit_sha()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    canonical_root = fb.microstructure_root / "gate-reports"
    canonical_root.mkdir(parents=True, exist_ok=True)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=canonical_root,
            code_commit_sha=sha,
            family_subdir="raw",
            phase_id="4bb-F",
        )
    )
    assert res.report_path is not None
    sidecar = res.report_path.with_suffix(".json.sha256")
    assert sidecar.exists()
    body = res.report_path.read_bytes()
    expected_sha = hashlib.sha256(body).hexdigest()
    text = sidecar.read_text(encoding="utf-8")
    # Two-space, trailing newline format.
    assert text == f"{expected_sha}  {res.report_path.name}\n"


def test_orchestrator_preserves_manifest_immutability_under_canonical_placement(
    tmp_path: Path,
) -> None:
    sha = _current_commit_sha()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    canonical_root = fb.microstructure_root / "gate-reports"
    canonical_root.mkdir(parents=True, exist_ok=True)
    manifest_bytes_before = fb.manifest_path.read_bytes()
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=canonical_root,
            code_commit_sha=sha,
            family_subdir="raw",
            phase_id="4bb-F",
        )
    )
    assert res.report_path is not None
    # Manifest is unchanged.
    assert fb.manifest_path.read_bytes() == manifest_bytes_before


def test_orchestrator_canonical_payload_research_eligible_remains_false(
    tmp_path: Path,
) -> None:
    sha = _current_commit_sha()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)
    canonical_root = fb.microstructure_root / "gate-reports"
    canonical_root.mkdir(parents=True, exist_ok=True)
    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=canonical_root,
            code_commit_sha=sha,
            family_subdir="raw",
            phase_id="4bb-F",
        )
    )
    assert res.report_path is not None
    payload = json.loads(res.report_path.read_text(encoding="utf-8"))
    assert payload["research_eligible_after"] is False
    assert payload["no_successor_authorization"] is True
