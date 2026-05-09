"""Phase 4bf orchestrator end-to-end + input/result invariant tests."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import derived_gate_checks as dgc
from prometheus.research.microstructure.derived_gate import (
    DerivedAggTradesGateInput,
    DerivedAggTradesGateInputError,
    run_derived_aggtrades_gate,
)
from prometheus.research.microstructure.derived_gate_checks import (
    DerivedAggTradesCheckStatus,
)
from prometheus.research.microstructure.derived_gate_io import (
    GateIOError,
    compute_file_sha256,
)

from ._derived_gate_fixtures import (
    build_real_paths,
    make_canonical_derived_manifest,
    make_canonical_raw_manifest,
    make_canonical_table,
    patch_event_count_constant,
    patch_last_agg_id_constant,
    patch_last_t_constant,
)


def _materialize_full_fixture(
    tmp_path: Path,
    *,
    num_rows: int = 5,
    derived_manifest_overrides: dict | None = None,
) -> dict[str, Path]:
    micro_root = tmp_path / "data" / "microstructure"
    paths = build_real_paths(micro_root)
    paths["output_root"].mkdir(parents=True, exist_ok=True)
    paths["derived_manifest_path"].parent.mkdir(parents=True, exist_ok=True)
    paths["normalized_parquet_path"].parent.mkdir(parents=True, exist_ok=True)
    paths["raw_zip_path"].parent.mkdir(parents=True, exist_ok=True)
    paths["gate_report_path"].parent.mkdir(parents=True, exist_ok=True)

    # Canonical Parquet
    table = make_canonical_table(num_rows=num_rows)
    pq.write_table(table, paths["normalized_parquet_path"])
    parquet_sha = compute_file_sha256(paths["normalized_parquet_path"])
    paths["normalized_parquet_sidecar_path"].write_text(
        f"{parquet_sha}  {paths['normalized_parquet_path'].name}\n", encoding="utf-8"
    )

    # Derived manifest references the relative parquet path under `data/microstructure/`.
    manifest = make_canonical_derived_manifest(event_count=num_rows)
    parquet_relpath = (
        f"normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/"
        f"{paths['normalized_parquet_path'].name}"
    )
    manifest["files"][0]["path"] = parquet_relpath
    manifest["files"][0]["sha256"] = parquet_sha
    manifest["start_time_ms"] = dgc.EXPECTED_FIRST_T
    manifest["end_time_ms"] = dgc.EXPECTED_LAST_T
    manifest["files"][0]["start_time_ms"] = dgc.EXPECTED_FIRST_T
    manifest["files"][0]["end_time_ms"] = dgc.EXPECTED_LAST_T
    if derived_manifest_overrides:
        manifest.update(derived_manifest_overrides)
    derived_payload = json.dumps(manifest, sort_keys=True, indent=2).encode("utf-8")
    paths["derived_manifest_path"].write_bytes(derived_payload)
    paths["derived_manifest_sidecar_path"].write_text(
        f"{hashlib.sha256(derived_payload).hexdigest()}  {paths['derived_manifest_path'].name}\n",
        encoding="utf-8",
    )

    # Raw manifest
    raw_manifest = make_canonical_raw_manifest()
    raw_relpath = (
        f"raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/{paths['raw_zip_path'].name}"
    )
    raw_manifest["files"][0]["path"] = raw_relpath
    raw_manifest["start_time_ms"] = dgc.EXPECTED_FIRST_T
    raw_manifest["end_time_ms"] = dgc.EXPECTED_LAST_T
    raw_payload = json.dumps(raw_manifest, sort_keys=True, indent=2).encode("utf-8")
    paths["raw_manifest_path"].write_bytes(raw_payload)

    # Raw zip + sidecar
    with zipfile.ZipFile(paths["raw_zip_path"], "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("BTCUSDT-aggTrades-2025-01-15.csv", "agg_trade_id,price\n1,1.0\n")
    raw_zip_sha = compute_file_sha256(paths["raw_zip_path"])
    paths["raw_sidecar_path"].write_text(
        f"{raw_zip_sha}  {paths['raw_zip_path'].name}\n", encoding="utf-8"
    )

    # Acquisition log
    paths["acquisition_log_path"].write_text(
        json.dumps({"phase": "4az", "status": "ok"}, sort_keys=True), encoding="utf-8"
    )

    # Phase 4bb-D gate report stub (any valid JSON; SHA mismatch is expected here)
    paths["gate_report_path"].write_text(
        json.dumps({"phase": "4bb-D", "stub": True}, sort_keys=True), encoding="utf-8"
    )

    return paths


@pytest.fixture
def patched_constants(monkeypatch: pytest.MonkeyPatch) -> int:
    n = 5
    patch_event_count_constant(monkeypatch, n)
    patch_last_t_constant(monkeypatch, dgc.EXPECTED_FIRST_T + n - 1)
    patch_last_agg_id_constant(monkeypatch, dgc.EXPECTED_FIRST_AGG_TRADE_ID + n - 1)
    return n


def _patch_expected_shas(
    monkeypatch: pytest.MonkeyPatch,
    *,
    derived_manifest_sha: str,
    parquet_sha: str,
    raw_manifest_sha: str,
    raw_zip_sha: str,
    raw_sidecar_sha: str,
    acquisition_log_sha: str,
    gate_report_sha: str,
) -> None:
    monkeypatch.setattr(dgc, "EXPECTED_DERIVED_MANIFEST_SHA", derived_manifest_sha)
    monkeypatch.setattr(dgc, "EXPECTED_NORMALIZED_PARQUET_SHA", parquet_sha)
    monkeypatch.setattr(dgc, "EXPECTED_RAW_MANIFEST_SHA", raw_manifest_sha)
    monkeypatch.setattr(dgc, "EXPECTED_RAW_ZIP_SHA", raw_zip_sha)
    monkeypatch.setattr(dgc, "EXPECTED_RAW_SIDECAR_SHA", raw_sidecar_sha)
    monkeypatch.setattr(dgc, "EXPECTED_ACQUISITION_LOG_SHA", acquisition_log_sha)
    monkeypatch.setattr(dgc, "EXPECTED_GATE_REPORT_SHA", gate_report_sha)
    # Also patch the lineage-column expected values that referenced raw SHAs.
    new_lineage = tuple(
        (col, raw_zip_sha) if col == "source_file_sha256"
        else (col, raw_manifest_sha) if col == "source_manifest_sha256"
        else (col, gate_report_sha) if col == "source_gate_report_sha256"
        else (col, expected)
        for col, expected in dgc.LINEAGE_CONSTANT_COLUMNS
    )
    monkeypatch.setattr(dgc, "LINEAGE_CONSTANT_COLUMNS", new_lineage)


def _build_passing_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, num_rows: int = 5
) -> tuple[DerivedAggTradesGateInput, dict[str, Path]]:
    paths = _materialize_full_fixture(tmp_path, num_rows=num_rows)
    derived_sha = compute_file_sha256(paths["derived_manifest_path"])
    parquet_sha = compute_file_sha256(paths["normalized_parquet_path"])
    raw_manifest_sha = compute_file_sha256(paths["raw_manifest_path"])
    raw_zip_sha = compute_file_sha256(paths["raw_zip_path"])
    raw_sidecar_sha = compute_file_sha256(paths["raw_sidecar_path"])
    acq_log_sha = compute_file_sha256(paths["acquisition_log_path"])
    gate_report_sha = compute_file_sha256(paths["gate_report_path"])

    _patch_expected_shas(
        monkeypatch,
        derived_manifest_sha=derived_sha,
        parquet_sha=parquet_sha,
        raw_manifest_sha=raw_manifest_sha,
        raw_zip_sha=raw_zip_sha,
        raw_sidecar_sha=raw_sidecar_sha,
        acquisition_log_sha=acq_log_sha,
        gate_report_sha=gate_report_sha,
    )

    # The mini-fixture's parquet rows reference the canonical raw zip / manifest /
    # gate-report SHAs. We need to rebuild the parquet so its lineage columns
    # reflect the patched (tmp_path-local) SHA values, and rewrite the derived
    # manifest's files[0].sha256 + governance_labels accordingly.
    existing_table = pq.read_table(paths["normalized_parquet_path"])
    schema = existing_table.schema
    cols = {
        f.name: existing_table.column(f.name).to_pylist() for f in schema
    }
    cols["source_file_sha256"] = [raw_zip_sha] * num_rows
    cols["source_manifest_sha256"] = [raw_manifest_sha] * num_rows
    cols["source_gate_report_sha256"] = [gate_report_sha] * num_rows
    new_table = pa.Table.from_pydict(cols, schema=schema)
    pq.write_table(new_table, paths["normalized_parquet_path"])
    new_parquet_sha = compute_file_sha256(paths["normalized_parquet_path"])
    paths["normalized_parquet_sidecar_path"].write_text(
        f"{new_parquet_sha}  {paths['normalized_parquet_path'].name}\n", encoding="utf-8"
    )
    monkeypatch.setattr(dgc, "EXPECTED_NORMALIZED_PARQUET_SHA", new_parquet_sha)

    # Update derived manifest files[0].sha256 + governance labels to match patched SHAs.
    payload = json.loads(paths["derived_manifest_path"].read_text(encoding="utf-8"))
    payload["files"][0]["sha256"] = new_parquet_sha
    payload["governance_labels"]["source_manifest_sha256"] = raw_manifest_sha
    payload["governance_labels"]["source_raw_zip_sha256"] = raw_zip_sha
    payload["governance_labels"]["source_gate_report_sha256"] = gate_report_sha
    new_payload = json.dumps(payload, sort_keys=True, indent=2).encode("utf-8")
    paths["derived_manifest_path"].write_bytes(new_payload)
    new_derived_sha = hashlib.sha256(new_payload).hexdigest()
    paths["derived_manifest_sidecar_path"].write_text(
        f"{new_derived_sha}  {paths['derived_manifest_path'].name}\n", encoding="utf-8"
    )
    monkeypatch.setattr(dgc, "EXPECTED_DERIVED_MANIFEST_SHA", new_derived_sha)

    inp = DerivedAggTradesGateInput(
        derived_manifest_path=paths["derived_manifest_path"],
        output_root=paths["output_root"],
        code_commit_sha="testcommit01abcdef",
        write_report=True,
    )
    return inp, paths


# ---------- Input dataclass invariants ----------


def test_input_rejects_non_path_derived_manifest() -> None:
    with pytest.raises(DerivedAggTradesGateInputError):
        DerivedAggTradesGateInput(
            derived_manifest_path="not-a-path",  # type: ignore[arg-type]
            output_root=Path("data/microstructure/gate-reports/normalized"),
            code_commit_sha="x",
        )


def test_input_rejects_empty_commit_sha(tmp_path: Path) -> None:
    micro = tmp_path / "data" / "microstructure"
    p = micro / "manifests" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{}", encoding="utf-8")
    with pytest.raises(DerivedAggTradesGateInputError):
        DerivedAggTradesGateInput(
            derived_manifest_path=p,
            output_root=micro / "gate-reports" / "normalized",
            code_commit_sha="",
        )


def test_input_rejects_path_outside_microstructure(tmp_path: Path) -> None:
    p = tmp_path / "elsewhere" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{}", encoding="utf-8")
    with pytest.raises(DerivedAggTradesGateInputError):
        DerivedAggTradesGateInput(
            derived_manifest_path=p,
            output_root=tmp_path / "data" / "microstructure" / "gate-reports" / "normalized",
            code_commit_sha="abc",
        )


# ---------- End-to-end happy path ----------


def test_happy_path_returns_pass_and_writes_report(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp, paths = _build_passing_input(tmp_path, monkeypatch)
    result = run_derived_aggtrades_gate(inp)
    assert result.overall_status == DerivedAggTradesCheckStatus.PASS
    assert result.research_eligible_after is False
    assert result.no_successor_authorization is True
    assert result.eligibility_gate_status_after == "pass"
    assert len(result.checks) == 55
    assert result.report_path is not None
    assert result.report_path.exists()
    sidecar = Path(str(result.report_path) + ".sha256")
    assert sidecar.exists()
    assert all(v is True for v in result.boundary_confirmations.values())


def test_run_returns_55_checks_in_order(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp, _ = _build_passing_input(tmp_path, monkeypatch)
    result = run_derived_aggtrades_gate(inp)
    assert [c.check_id for c in result.checks] == [f"4bf.13.{i}" for i in range(1, 56)]


def test_run_writes_paired_sidecar_with_matching_sha(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp, _ = _build_passing_input(tmp_path, monkeypatch)
    result = run_derived_aggtrades_gate(inp)
    assert result.report_path is not None
    sidecar = Path(str(result.report_path) + ".sha256")
    text = sidecar.read_text(encoding="utf-8").strip()
    assert text.endswith(f"  {result.report_path.name}")
    sha_in_sidecar = text.split()[0]
    assert sha_in_sidecar == compute_file_sha256(result.report_path)


def test_run_with_write_report_false_does_not_write_anything(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp_full, paths = _build_passing_input(tmp_path, monkeypatch)
    inp = DerivedAggTradesGateInput(
        derived_manifest_path=inp_full.derived_manifest_path,
        output_root=inp_full.output_root,
        code_commit_sha=inp_full.code_commit_sha,
        write_report=False,
    )
    result = run_derived_aggtrades_gate(inp)
    assert result.overall_status == DerivedAggTradesCheckStatus.PASS
    assert result.report_path is None
    # Verify nothing was written under output_root.
    written = list(paths["output_root"].glob("*.json"))
    assert written == []


# ---------- End-to-end FAIL paths ----------


def test_run_fails_when_event_count_drifts(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp, paths = _build_passing_input(tmp_path, monkeypatch)
    payload = json.loads(paths["derived_manifest_path"].read_text(encoding="utf-8"))
    payload["event_count"] = 99
    new = json.dumps(payload, sort_keys=True, indent=2).encode("utf-8")
    paths["derived_manifest_path"].write_bytes(new)
    new_sha = hashlib.sha256(new).hexdigest()
    paths["derived_manifest_sidecar_path"].write_text(
        f"{new_sha}  {paths['derived_manifest_path'].name}\n", encoding="utf-8"
    )
    monkeypatch.setattr(dgc, "EXPECTED_DERIVED_MANIFEST_SHA", new_sha)

    result = run_derived_aggtrades_gate(inp)
    assert result.overall_status == DerivedAggTradesCheckStatus.FAIL
    failed_ids = [c.check_id for c in result.checks if c.status == DerivedAggTradesCheckStatus.FAIL]
    assert "4bf.13.7" in failed_ids
    # research_eligible_after / no_successor_authorization remain invariant.
    assert result.research_eligible_after is False
    assert result.no_successor_authorization is True
    assert result.eligibility_gate_status_after == "fail"


def test_run_fails_when_research_eligible_poisoned(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp, paths = _build_passing_input(tmp_path, monkeypatch)
    payload = json.loads(paths["derived_manifest_path"].read_text(encoding="utf-8"))
    payload["research_eligible"] = True  # poison
    new = json.dumps(payload, sort_keys=True, indent=2).encode("utf-8")
    paths["derived_manifest_path"].write_bytes(new)
    new_sha = hashlib.sha256(new).hexdigest()
    paths["derived_manifest_sidecar_path"].write_text(
        f"{new_sha}  {paths['derived_manifest_path'].name}\n", encoding="utf-8"
    )
    monkeypatch.setattr(dgc, "EXPECTED_DERIVED_MANIFEST_SHA", new_sha)

    result = run_derived_aggtrades_gate(inp)
    assert result.overall_status == DerivedAggTradesCheckStatus.FAIL
    failed_ids = [c.check_id for c in result.checks if c.status == DerivedAggTradesCheckStatus.FAIL]
    assert "4bf.13.13" in failed_ids
    # The result invariants still hold: research_eligible_after=False.
    assert result.research_eligible_after is False


def test_run_refuses_to_overwrite_existing_report(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp, _ = _build_passing_input(tmp_path, monkeypatch)
    # First run succeeds.
    first = run_derived_aggtrades_gate(inp)
    assert first.report_path is not None and first.report_path.exists()
    # Second run with the same code_commit_sha and `unix_ms` could in
    # principle overwrite the same path. We force the same path by
    # patching ``time.time``.
    fixed_unix_ms = first.report_path.stem.split("__")[-2]
    monkeypatch.setattr(
        "prometheus.research.microstructure.derived_gate.time.time",
        lambda: int(fixed_unix_ms) / 1000.0,
    )
    with pytest.raises(GateIOError):
        run_derived_aggtrades_gate(inp)


def test_run_records_pre_post_immutability(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp, paths = _build_passing_input(tmp_path, monkeypatch)
    derived_pre = compute_file_sha256(paths["derived_manifest_path"])
    parquet_pre = compute_file_sha256(paths["normalized_parquet_path"])
    raw_manifest_pre = compute_file_sha256(paths["raw_manifest_path"])

    result = run_derived_aggtrades_gate(inp)
    assert result.boundary_confirmations["no_manifest_mutation"] is True

    # Files unchanged after the run.
    assert compute_file_sha256(paths["derived_manifest_path"]) == derived_pre
    assert compute_file_sha256(paths["normalized_parquet_path"]) == parquet_pre
    assert compute_file_sha256(paths["raw_manifest_path"]) == raw_manifest_pre


def test_report_payload_records_invariants(
    tmp_path: Path, patched_constants: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    inp, _ = _build_passing_input(tmp_path, monkeypatch)
    result = run_derived_aggtrades_gate(inp)
    assert result.report_path is not None
    payload = json.loads(result.report_path.read_text(encoding="utf-8"))
    assert payload["research_eligible_after"] is False
    assert payload["no_successor_authorization"] is True
    assert payload["report_schema_version"] == "v001"
    assert payload["phase_id"] == "4bf"
    assert len(payload["checks"]) == 55


def test_input_rejects_output_root_outside_microstructure(tmp_path: Path) -> None:
    p = tmp_path / "data" / "microstructure" / "manifests" / "x.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{}", encoding="utf-8")
    with pytest.raises(DerivedAggTradesGateInputError):
        DerivedAggTradesGateInput(
            derived_manifest_path=p,
            output_root=tmp_path / "elsewhere",
            code_commit_sha="abc",
        )
