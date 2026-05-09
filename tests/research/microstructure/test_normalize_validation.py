"""Phase 4bd tests for the 27-check validation suite."""

from __future__ import annotations

from pathlib import Path

from prometheus.research.microstructure.normalize_aggtrades import (
    NormalizeAggTradesInput,
    run_normalize_aggtrades,
)
from prometheus.research.microstructure.normalize_validation import (
    CHECK_ORDER,
    NormalizationCheckStatus,
)

from ._normalize_fixtures import (
    CITED_GATE_REPORT_ID,
    CITED_GATE_REPORT_SHA,
    build_normalize_fixture,
)


def _ids(checks) -> list[str]:
    return [c.check_id for c in checks]


def test_check_order_has_exactly_27_entries() -> None:
    assert len(CHECK_ORDER) == 27


def test_check_order_ids_are_4bc_24_1_to_27() -> None:
    expected = [f"4bc.24.{i}" for i in range(1, 28)]
    actual = [entry[0] for entry in CHECK_ORDER]
    assert actual == expected


def test_run_returns_27_check_results_in_order(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
    )
    result = run_normalize_aggtrades(inp)
    assert len(result.checks) == 27
    assert _ids(result.checks) == [f"4bc.24.{i}" for i in range(1, 28)]


def test_happy_path_all_checks_pass(tmp_path: Path) -> None:
    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
    )
    result = run_normalize_aggtrades(inp)
    failures = [
        c for c in result.checks if c.status not in (NormalizationCheckStatus.PASS,)
    ]
    summary = [(c.check_id, c.status, c.detail) for c in failures]
    assert not failures, f"expected all-PASS but got: {summary}"
    assert result.overall_status == NormalizationCheckStatus.PASS


def test_immutability_check_detects_drift(tmp_path: Path) -> None:
    """Forge a context where pre/post hashes differ and confirm FAIL."""
    from prometheus.research.microstructure.normalize_io import (
        SourceArtefactPaths,
    )
    from prometheus.research.microstructure.normalize_validation import (
        NormalizationValidationContext,
        check_raw_manifest_immutable,
    )

    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
    )
    ctx = NormalizationValidationContext(
        inp=inp,
        rows=(),
        output_path=None,
        output_sha256=None,
        output_size_bytes=None,
        derived_manifest=None,
        derived_manifest_path=None,
        derived_manifest_sha256=None,
        raw_manifest_bytes_before=b"x",
        raw_manifest_bytes_after=b"y",
        raw_manifest_sha_before="a" * 64,
        raw_manifest_sha_after="b" * 64,
        raw_zip_sha_before="0" * 64,
        raw_zip_sha_after="0" * 64,
        sidecar_sha_before="0" * 64,
        sidecar_sha_after="0" * 64,
        acq_log_sha_before="0" * 64,
        acq_log_sha_after="0" * 64,
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
        cited_gate_code_commit_sha="",
        gate_report_local_present=False,
        gate_report_recomputed_sha=None,
        artefacts=SourceArtefactPaths(
            manifest_path=bundle.eligibility_bundle.manifest_path,
            raw_zip_path=bundle.eligibility_bundle.raw_zip_path,
            sidecar_path=bundle.eligibility_bundle.sidecar_path,
            acquisition_log_path=bundle.eligibility_bundle.acquisition_log_path,
        ),
        parsed_source_manifest={},
        member_name="x",
        csv_uncompressed_size=0,
        invalid_window_candidates=(),
    )
    res = check_raw_manifest_immutable(ctx)
    assert res.status == NormalizationCheckStatus.FAIL


def test_check_no_forbidden_imports_passes_on_clean_modules() -> None:
    from prometheus.research.microstructure.normalize_validation import (
        check_no_forbidden_imports,
    )

    # Build minimal context (only fields touched by this check).
    class Stub:
        pass

    stub = Stub()
    result = check_no_forbidden_imports(stub)  # type: ignore[arg-type]
    assert result.status == NormalizationCheckStatus.PASS


def test_check_one_csv_member_passes_on_fixture(tmp_path: Path) -> None:
    """Spot-check check_one_csv_member directly."""
    from prometheus.research.microstructure.normalize_io import (
        SourceArtefactPaths,
    )
    from prometheus.research.microstructure.normalize_validation import (
        NormalizationValidationContext,
        check_one_csv_member,
    )

    bundle = build_normalize_fixture(tmp_path, write_local_gate_report=False)
    inp = NormalizeAggTradesInput(
        manifest_path=bundle.eligibility_bundle.manifest_path,
        output_root=bundle.output_root,
        code_commit_sha="unknown",
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
    )
    ctx = NormalizationValidationContext(
        inp=inp,
        rows=(),
        output_path=None,
        output_sha256=None,
        output_size_bytes=None,
        derived_manifest=None,
        derived_manifest_path=None,
        derived_manifest_sha256=None,
        raw_manifest_bytes_before=b"",
        raw_manifest_bytes_after=b"",
        raw_manifest_sha_before="0" * 64,
        raw_manifest_sha_after="0" * 64,
        raw_zip_sha_before="0" * 64,
        raw_zip_sha_after="0" * 64,
        sidecar_sha_before="0" * 64,
        sidecar_sha_after="0" * 64,
        acq_log_sha_before="0" * 64,
        acq_log_sha_after="0" * 64,
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
        cited_gate_code_commit_sha="",
        gate_report_local_present=False,
        gate_report_recomputed_sha=None,
        artefacts=SourceArtefactPaths(
            manifest_path=bundle.eligibility_bundle.manifest_path,
            raw_zip_path=bundle.eligibility_bundle.raw_zip_path,
            sidecar_path=bundle.eligibility_bundle.sidecar_path,
            acquisition_log_path=bundle.eligibility_bundle.acquisition_log_path,
        ),
        parsed_source_manifest={},
        member_name="x",
        csv_uncompressed_size=0,
        invalid_window_candidates=(),
    )
    res = check_one_csv_member(ctx)
    assert res.status == NormalizationCheckStatus.PASS
