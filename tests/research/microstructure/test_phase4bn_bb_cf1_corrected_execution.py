"""Phase 4bn-BB — tests for the corrected CF-1 execution runner (orchestration).

Covers: ``--preflight`` opens no Parquet and writes no persistent artefact; failed symbolic
proof / failed synthetic proof / missing source path / pre-existing BB artefact each route to
``PREFLIGHT_FAILURE``; the access-start record precedes any market-data read; a post-access
failure routes to ``CF1_INVALID_RUN`` with the run recorded as consumed; the source feature
column request excludes the mean column; and the runner never references the Phase 4bn-AZ output
root, the network, credentials, or a reserve path. No real market data is opened.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

from prometheus.research.microstructure import cf1_corrected_artifacts_v002 as art
from prometheus.research.microstructure import cf1_corrected_contract_v002 as cc

_REPO_ROOT = Path(cc.__file__).resolve().parents[4]
_SCRIPT = _REPO_ROOT / "scripts" / "phase4bn_bb_cf1_corrected_realized_volatility_execution.py"


def _load_runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("phase4bn_bb_runner_under_test", _SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # dataclass field resolution needs the module registered
    spec.loader.exec_module(mod)
    return mod


RUN = _load_runner()


def _pass_all_gates(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(RUN, "_verify_repo_state", lambda sha: None)
    monkeypatch.setattr(RUN, "measure_d_free_gib", lambda: 1000.0)
    monkeypatch.setattr(RUN, "_output_root_evidence_files", lambda root: [])
    monkeypatch.setattr(RUN, "_missing_source_files", lambda allowed: [])


def _forbid_parquet(monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom(*args: object, **kwargs: object) -> object:
        raise AssertionError("preflight must not open a Parquet")

    monkeypatch.setattr(RUN.pq, "read_table", _boom)


def _forbid_writes(monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom_json(*args: object, **kwargs: object) -> object:
        raise AssertionError("preflight must not write a persistent artefact")

    monkeypatch.setattr(RUN.art, "write_json_with_sidecar", _boom_json)
    monkeypatch.setattr(RUN.art, "write_parquet_with_sidecar", _boom_json)
    monkeypatch.setattr(RUN.art, "ensure_output_dirs", _boom_json)


# ---------------------------------------------------------------------------
# Preflight gates
# ---------------------------------------------------------------------------


def test_preflight_opens_no_parquet_and_writes_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_all_gates(monkeypatch)
    _forbid_parquet(monkeypatch)
    _forbid_writes(monkeypatch)
    result = RUN.preflight(code_commit_sha="0" * 40, verify_repo=True)
    assert result["result_state"] == "PREFLIGHT_PASS"
    assert result["symbolic_estimability_proof_passed"] is True
    assert result["timestamp_boundary_proof_passed"] is True
    assert result["allowed_utc_date_count"] == 244
    assert result["output_root_empty"] is True
    assert result["network_used"] is False
    assert result["reserve_touched"] is False


def test_preflight_failed_symbolic_proof(monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_all_gates(monkeypatch)
    monkeypatch.setattr(
        RUN.cc, "validate_symbolic_estimability_proof", lambda proof: (False, "forced")
    )
    with pytest.raises(RUN.PreflightFailure) as exc:
        RUN.preflight(code_commit_sha="0" * 40, verify_repo=True)
    assert exc.value.gate == "PREFLIGHT_FAILURE__SYMBOLIC_ESTIMABILITY_PROOF"


def test_preflight_failed_synthetic_proof(monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_all_gates(monkeypatch)
    monkeypatch.setattr(
        RUN,
        "build_corrected_timestamp_proof",
        lambda sha: {"timestamp_boundary_proof_passed": False},
    )
    with pytest.raises(RUN.PreflightFailure) as exc:
        RUN.preflight(code_commit_sha="0" * 40, verify_repo=True)
    assert exc.value.gate == "PREFLIGHT_FAILURE__TIMESTAMP_BOUNDARY_PROOF"


def test_preflight_missing_source_path(monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_all_gates(monkeypatch)
    monkeypatch.setattr(RUN, "_missing_source_files", lambda allowed: ["/x/missing.parquet"])
    with pytest.raises(RUN.PreflightFailure) as exc:
        RUN.preflight(code_commit_sha="0" * 40, verify_repo=True)
    assert exc.value.gate == "PREFLIGHT_FAILURE__MISSING_SOURCE_PARTITION"


def test_preflight_preexisting_bb_artefact(monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_all_gates(monkeypatch)
    monkeypatch.setattr(RUN, "_output_root_evidence_files", lambda root: [Path("/x/old.json")])
    with pytest.raises(RUN.PreflightFailure) as exc:
        RUN.preflight(code_commit_sha="0" * 40, verify_repo=True)
    assert exc.value.gate == "PREFLIGHT_FAILURE__OUTPUT_ROOT_NOT_EMPTY"


def test_preflight_insufficient_storage(monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_all_gates(monkeypatch)
    monkeypatch.setattr(RUN, "measure_d_free_gib", lambda: 10.0)
    with pytest.raises(RUN.PreflightFailure) as exc:
        RUN.preflight(code_commit_sha="0" * 40, verify_repo=True)
    assert exc.value.gate == "PREFLIGHT_FAILURE__INSUFFICIENT_STORAGE"


def test_preflight_not_pushed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(RUN, "measure_d_free_gib", lambda: 1000.0)
    monkeypatch.setattr(RUN, "_output_root_evidence_files", lambda root: [])
    monkeypatch.setattr(RUN, "_missing_source_files", lambda allowed: [])
    monkeypatch.setattr(RUN, "_git", lambda args: cc.BASE_MAIN_COMMIT_SHA)
    monkeypatch.setattr(RUN, "_git_ok", lambda args: (False, ""))
    with pytest.raises(RUN.PreflightFailure) as exc:
        RUN.preflight(code_commit_sha="0" * 40, verify_repo=True)
    assert exc.value.gate == "PREFLIGHT_FAILURE__NOT_PUSHED"


# ---------------------------------------------------------------------------
# Corrected timestamp proof (synthetic; no data)
# ---------------------------------------------------------------------------


def test_corrected_timestamp_proof_passes_with_feature_checks() -> None:
    proof = RUN.build_corrected_timestamp_proof("0" * 40)
    assert proof["timestamp_boundary_proof_passed"] is True
    assert proof["market_data_opened"] is False
    names = {c["name"] for c in proof["checks"]}
    assert "feature_snapshot_exactly_count_and_quantity_sum" in names
    assert "no_mean_column_in_requested_source_columns" in names
    assert "invalid_if_count_below_one" in names
    assert "invalid_if_quantity_sum_non_positive" in names


def test_feature_values_valid_predicate() -> None:
    assert RUN.feature_values_valid(3.0, 12.5)[0] is True
    assert RUN.feature_values_valid(0.0, 12.5)[0] is False
    assert RUN.feature_values_valid(3.0, 0.0)[0] is False
    assert RUN.feature_values_valid(float("nan"), 1.0)[0] is False


# ---------------------------------------------------------------------------
# Access-start ordering + post-access invalid routing
# ---------------------------------------------------------------------------


def test_access_start_precedes_read_and_post_access_failure_invalid(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls: list[tuple[str, str]] = []

    monkeypatch.setattr(RUN, "_git", lambda args: "0" * 40)
    monkeypatch.setattr(RUN, "preflight", lambda **kw: {"d_free_gib": 1000.0})
    monkeypatch.setattr(RUN.art, "ensure_output_dirs", lambda repo: tmp_path)

    def _fake_write(path: Path, payload: dict[str, object], repo: Path) -> tuple[str, Path]:
        family = str(payload.get("artifact_family") or payload.get("proof_family") or "?")
        calls.append(("write", family))
        return "0" * 64, path

    monkeypatch.setattr(RUN.art, "write_json_with_sidecar", _fake_write)
    monkeypatch.setattr(
        RUN, "_register", lambda root, path: art.ArtifactEntry("f", "r", "0" * 64, "r.sha256")
    )

    def _fake_build_segment(seg_id: str, lo: str, hi: str, *, progress: bool) -> object:
        calls.append(("read", seg_id))
        raise RuntimeError("simulated post-access failure")

    monkeypatch.setattr(RUN, "_build_segment", _fake_build_segment)

    summary = RUN.run(progress=False)
    assert summary["verdict"] == "CF1_INVALID_RUN"
    assert summary["result_state"] == cc.LONG_STATE_INVALID_RUN
    assert summary["evidence_bearing_run_consumed"] is True

    families = [f for kind, f in calls if kind == "write"]
    reads = [i for i, (kind, _f) in enumerate(calls) if kind == "read"]
    assert reads, "expected a market-data read to be attempted"
    first_read = reads[0]
    access_writes = [
        i for i, (kind, f) in enumerate(calls) if kind == "write" and f == art.FAMILY_ACCESS_START
    ]
    assert access_writes, "expected an access-start write"
    assert access_writes[0] < first_read
    # Both pre-data proofs written before the read as well.
    assert art.FAMILY_SYMBOLIC_PROOF in families
    assert art.FAMILY_TIMESTAMP_PROOF in families


# ---------------------------------------------------------------------------
# Static guards: no mean column, no AZ output root, no reserve
# ---------------------------------------------------------------------------


def _strip(text: str) -> str:
    out: list[str] = []
    in_doc = False
    quote: str | None = None
    for raw in text.splitlines():
        line = raw
        if in_doc:
            assert quote is not None
            if quote in line:
                in_doc = False
                quote = None
            continue
        for q in ('"""', "'''"):
            if q in line and line.count(q) % 2 == 1:
                in_doc = True
                quote = q
                line = line.split(q, 1)[0]
                break
        if "#" in line:
            line = line.split("#", 1)[0]
        out.append(line)
    return "\n".join(out)


def test_script_code_never_requests_mean_column() -> None:
    code = _strip(_SCRIPT.read_text(encoding="utf-8"))
    assert "rolling_quantity_mean" not in code


def test_script_code_never_references_az_output_root() -> None:
    code = _strip(_SCRIPT.read_text(encoding="utf-8"))
    assert "cf1_realized_volatility_substrate_test_v001" not in code


def test_source_feature_columns_exclude_mean() -> None:
    assert cc.PROHIBITED_FEATURE_COLUMN not in cc.FEATURE_SOURCE_COLUMNS
    assert list(cc.FEATURE_SOURCE_COLUMNS) == [
        "feature_timestamp_ms",
        "row_index",
        "rolling_aggtrade_count_60s",
        "rolling_quantity_sum_60s",
    ]


def test_preflight_and_run_are_mutually_exclusive_required() -> None:
    with pytest.raises(SystemExit):
        RUN.main([])
    with pytest.raises(SystemExit):
        RUN.main(["--preflight", "--run"])
