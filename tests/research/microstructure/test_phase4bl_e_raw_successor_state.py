"""Offline tests for Phase 4bl-E v002 multi-day raw successor-state recording.

These tests exercise the Phase 4bl-E recording script in isolation
using ``pytest`` ``tmp_path``. They never touch real Phase 4bl-C /
4bl-D / 4bl-D-S2 / 4bl-D-R artefacts; they never require the real
``data/microstructure/`` tree to exist; they never run the Phase
4bl-D gate; they never perform any network I/O.

Forbidden-import scan ensures the recording script imports nothing
outside the Python standard library and contains no credential /
network / MCP / Graphify tokens.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path

import pytest

# Resolve the script under test by file path (the ``scripts/``
# directory is not a package, so we import via
# ``importlib.util.spec_from_file_location``).
REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts"
    / "phase4bl_e_record_multiday_raw_successor_state.py"
)


@pytest.fixture(scope="module")
def script_module():
    spec = importlib.util.spec_from_file_location(
        "phase4bl_e_record_multiday_raw_successor_state", SCRIPT_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["phase4bl_e_record_multiday_raw_successor_state"] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Locked-constant assertions
# ---------------------------------------------------------------------------


def test_locked_identity_constants(script_module) -> None:
    assert script_module.PHASE_ID == "4bl-e"
    assert script_module.PHASE_NAME == "Phase 4bl-E"
    assert script_module.SCHEMA_VERSION == "v001"
    assert script_module.ARTEFACT_TYPE == "raw_multiday_successor_state_record"
    assert script_module.DATASET_FAMILY == "microstructure_raw_aggtrades_v001"
    assert script_module.DATASET_VERSION == "v002"
    assert script_module.STAGE_MARKER == "stage2_raw_admissible"
    assert script_module.SUCCESSOR_STATE == "stage2_raw_admissible"
    assert script_module.SOURCE_PHASE_BOUNDARY == "Phase 4bl-D-R"
    assert script_module.SYMBOL_LIST == ("BTCUSDT",)
    assert script_module.DATE_START == "2024-12-01"
    assert script_module.DATE_END == "2025-02-28"
    assert script_module.DATE_COUNT == 90
    assert script_module.EXPECTED_TOTAL_ROW_COUNT == 155_153_449
    assert script_module.EXPECTED_TOTAL_SIZE_BYTES == 1_943_823_208


def test_expected_shas_dict_has_ten_keys(script_module) -> None:
    keys = set(script_module.EXPECTED_SHAS.keys())
    assert keys == {
        "v002_raw_manifest",
        "v002_raw_manifest_sidecar",
        "v002_acquisition_log",
        "v002_acquisition_log_sidecar",
        "phase_4bl_d_r_report",
        "phase_4bl_d_r_report_sidecar",
        "phase_4bl_d_fail_report",
        "phase_4bl_d_s2_canon_report",
        "canonicalized_2025_01_15_sidecar",
        "raw_2025_01_15_zip",
    }
    for value in script_module.EXPECTED_SHAS.values():
        assert isinstance(value, str)
        assert len(value) == 64
        assert all(c in "0123456789abcdef" for c in value)


def test_phase_4bl_d_r_result_block_is_pass(script_module) -> None:
    block = script_module.PHASE_4BL_D_R_RESULT
    assert block["verdict"] == "RAW_MULTIDAY_GATE_PASS"
    assert block["overall_status"] == "pass"
    assert block["checks_total"] == 33
    assert block["checks_passed"] == 33
    assert block["checks_failed"] == 0
    assert block["full_per_row_validation_completed"] is True
    assert block["rows_validated"] == 155_153_449
    assert block["bytes_validated"] == 1_943_823_208


# ---------------------------------------------------------------------------
# Pure-helper tests
# ---------------------------------------------------------------------------


def test_compute_file_sha256_matches_hashlib(tmp_path, script_module) -> None:
    payload = b"\x00\x01\x02test payload\n"
    target = tmp_path / "blob.bin"
    target.write_bytes(payload)
    expected = hashlib.sha256(payload).hexdigest()
    actual = script_module.compute_file_sha256(target)
    assert actual == expected


def test_serialize_successor_state_is_deterministic(script_module) -> None:
    payload = {"b": 2, "a": 1, "nested": {"y": 0, "x": 9}}
    body_1 = script_module.serialize_successor_state(payload)
    body_2 = script_module.serialize_successor_state(payload)
    assert body_1 == body_2


def test_serialize_successor_state_no_trailing_newline(script_module) -> None:
    payload = {"a": 1}
    body = script_module.serialize_successor_state(payload)
    # Phase 4bb-G precedent: no trailing newline.
    assert not body.endswith(b"\n")
    # Sorted keys + indent=2.
    text = body.decode("utf-8")
    assert text == '{\n  "a": 1\n}'


def test_serialize_successor_state_sorted_keys(script_module) -> None:
    payload = {"zebra": 1, "alpha": 2, "mango": 3}
    text = script_module.serialize_successor_state(payload).decode("utf-8")
    alpha_pos = text.index('"alpha"')
    mango_pos = text.index('"mango"')
    zebra_pos = text.index('"zebra"')
    assert alpha_pos < mango_pos < zebra_pos


def test_compose_canonical_sidecar_body_format(script_module) -> None:
    sha = "f" * 64
    basename = "x.json"
    body = script_module.compose_canonical_sidecar_body(
        json_sha256_hex=sha, json_basename=basename
    )
    assert body == f"{sha}  {basename}\n".encode()
    # Two spaces separator.
    assert b"  " in body
    # Trailing LF, not CRLF.
    assert body.endswith(b"\n")
    assert b"\r\n" not in body


def test_compose_canonical_sidecar_body_rejects_bad_sha(script_module) -> None:
    with pytest.raises(script_module.SuccessorStateError):
        script_module.compose_canonical_sidecar_body(
            json_sha256_hex="too-short", json_basename="x.json"
        )


def test_compose_canonical_sidecar_body_rejects_non_hex(script_module) -> None:
    with pytest.raises(script_module.SuccessorStateError):
        script_module.compose_canonical_sidecar_body(
            json_sha256_hex="g" * 64, json_basename="x.json"
        )


def test_compose_canonical_sidecar_body_rejects_path_separators(script_module) -> None:
    with pytest.raises(script_module.SuccessorStateError):
        script_module.compose_canonical_sidecar_body(
            json_sha256_hex="f" * 64, json_basename="dir/x.json"
        )
    with pytest.raises(script_module.SuccessorStateError):
        script_module.compose_canonical_sidecar_body(
            json_sha256_hex="f" * 64, json_basename="dir\\x.json"
        )


def test_compose_canonical_sidecar_body_rejects_empty_basename(script_module) -> None:
    with pytest.raises(script_module.SuccessorStateError):
        script_module.compose_canonical_sidecar_body(
            json_sha256_hex="f" * 64, json_basename=""
        )


def test_derive_short_commit_returns_lowercase_hex(script_module) -> None:
    assert script_module.derive_short_commit("ABCDEF0123456789aaaa") == "abcdef012345"
    assert script_module.derive_short_commit("0" * 40, length=7) == "0000000"


def test_derive_short_commit_rejects_short_sha(script_module) -> None:
    with pytest.raises(script_module.SuccessorStateError):
        script_module.derive_short_commit("abc", length=12)


def test_derive_short_commit_rejects_non_hex(script_module) -> None:
    with pytest.raises(script_module.SuccessorStateError):
        script_module.derive_short_commit("z" * 40, length=12)


# ---------------------------------------------------------------------------
# Payload tests
# ---------------------------------------------------------------------------


def _build_synthetic_payload(script_module) -> dict:
    """Build a deterministic payload using fake but legal arguments."""
    return script_module.build_successor_state_payload(
        expected_shas=dict(script_module.EXPECTED_SHAS),
        base_commit_sha="0" * 40,
        code_commit_sha="1" * 40,
        created_at_unix_ms=1_700_000_000_000,
        created_at_utc="2024-11-14T22:13:20+00:00",
        successor_state_basename=(
            "microstructure_raw_aggtrades_v001__v002__"
            "stage2_raw_admissible__phase-4bl-e.json"
        ),
        sidecar_basename=(
            "microstructure_raw_aggtrades_v001__v002__"
            "stage2_raw_admissible__phase-4bl-e.json.sha256"
        ),
        script_path="scripts/phase4bl_e_record_multiday_raw_successor_state.py",
        python_version="3.12.4",
        platform_summary="Windows-10",
    )


def test_payload_contains_required_identity_fields(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    assert payload["phase"] == "Phase 4bl-E"
    assert payload["phase_id"] == "4BL-E"
    assert payload["artefact_type"] == "raw_multiday_successor_state_record"
    assert payload["successor_state"] == "stage2_raw_admissible"
    assert payload["successor_state_status"] == "recorded"
    assert payload["successor_state_family"] == "microstructure_raw_aggtrades_v001"
    assert payload["successor_state_version"] == "v002"
    assert payload["successor_admissibility_status"] == (
        "admissible_in_principle_policy_level_only"
    )
    assert payload["successor_research_use_admissible"] == "conditional_future_only"
    assert payload["successor_ml_use_admissible"] is False
    assert payload["successor_raw_use_admissible"] is True


def test_payload_dataset_scope_locked(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    assert payload["dataset_family"] == "microstructure_raw_aggtrades_v001"
    assert payload["dataset_version"] == "v002"
    assert payload["symbol_list"] == ["BTCUSDT"]
    assert payload["date_start"] == "2024-12-01"
    assert payload["date_end"] == "2025-02-28"
    assert payload["date_count"] == 90
    assert payload["total_row_count"] == 155_153_449
    assert payload["total_size_bytes"] == 1_943_823_208


def test_payload_records_phase_4bl_d_r_pass(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    assert payload["latest_gate_phase"] == "Phase 4bl-D-R"
    assert payload["latest_gate_verdict"] == "RAW_MULTIDAY_GATE_PASS"
    assert payload["latest_gate_overall_status"] == "pass"
    assert payload["latest_gate_checks_total"] == 33
    assert payload["latest_gate_checks_passed"] == 33
    assert payload["latest_gate_checks_failed"] == 0
    assert payload["full_per_row_validation_completed"] is True


def test_payload_records_predecessor_fail_lineage(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    assert payload["predecessor_failed_gate_phase"] == "Phase 4bl-D"
    assert payload["predecessor_failed_gate_verdict"] == "RAW_MULTIDAY_GATE_FAIL"
    assert "CRLF" in payload["predecessor_failed_gate_summary"]
    assert "Phase 4bb-F LF" in payload["predecessor_failed_gate_summary"]


def test_payload_records_remediation_lineage(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    assert payload["remediation_governance_phase"] == "Phase 4bl-D-S1"
    assert payload["remediation_execution_phase"] == "Phase 4bl-D-S2"
    assert payload["remediation_type"] == (
        "metadata_sidecar_line_ending_canonicalization"
    )
    assert "2026-05-13_phase-4bl-d-s1" in payload["remediation_governance_memo_path"]
    assert "2026-05-13_phase-4bl-d-s2" in payload["remediation_execution_memo_path"]


def test_payload_lineage_chain_has_eight_entries(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    chain = payload["lineage_chain"]
    assert isinstance(chain, list)
    assert len(chain) == 8
    assert chain[0].startswith("Phase 4bl-A")
    assert chain[-1].startswith("Phase 4bl-E")


def test_payload_manifest_state_preservation_flags(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    assert payload["manifest_mutated"] is False
    assert payload["manifest_transition_performed"] is False
    assert payload["research_eligible_before"] is False
    assert payload["research_eligible_after"] is False
    assert payload["eligibility_gate_status_before"] == "pending"
    assert payload["eligibility_gate_status_after"] == "pending"
    assert payload["eligibility_gate_status_transition_performed"] is False
    assert payload["chronological_split_policy_changed"] is False
    assert payload["manifest_mutation_permitted"] is False
    assert payload["report_level_gate_status"] == "pass_report_level_only"
    assert payload["successor_state_record_is_sibling_artefact"] is True


def test_payload_governance_labels_forbidden_set(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    labels = payload["governance_labels"]
    for key in (
        "feature_computation",
        "labels",
        "diagnostics",
        "ml",
        "strategy",
        "backtest",
        "strategy_use",
    ):
        assert labels[key] == "forbidden", f"governance_labels[{key!r}] must be forbidden"
    assert labels["phase"] == "4bl-e"
    assert labels["source_phase_boundary"] == "4bl-D-R"
    assert labels["dataset_family"] == "microstructure_raw_aggtrades_v001"
    assert labels["dataset_version"] == "v002"
    assert labels["stop_trigger_domain"] == "trade_price_backtest_candidate"


def test_payload_non_authorizations_all_false(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    non_auths = payload["non_authorizations"]
    # Every value must be exactly False.
    for key, value in non_auths.items():
        assert value is False, f"non_authorizations[{key!r}] must be False"
    # Spot-check critical keys are present.
    for required in (
        "phase_4bm_authorized",
        "phase_4bm_a_authorized",
        "phase_5_authorized",
        "phase_4_canonical_authorized",
        "acquisition_authorized",
        "normalization_authorized",
        "feature_generation_authorized",
        "label_generation_authorized",
        "ml_authorized",
        "strategy_authorized",
        "backtest_authorized",
        "paper_shadow_authorized",
        "live_authorized",
        "deployment_authorized",
        "exchange_write_authorized",
        "production_keys_authorized",
        "authenticated_apis_authorized",
        "private_endpoints_authorized",
        "user_stream_authorized",
        "websocket_authorized",
        "mcp_authorized",
        "graphify_authorized",
        "credentials_authorized",
        "manifest_research_eligible_flip_authorized",
        "manifest_eligibility_gate_status_transition_authorized",
        "chronological_split_policy_change_authorized",
        "successor_authorizes_next_phase",
    ):
        assert required in non_auths


def test_payload_boundary_confirmations_all_true(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    boundaries = payload["boundary_confirmations"]
    for key, value in boundaries.items():
        assert value is True, f"boundary_confirmations[{key!r}] must be True"
    for required in (
        "no_v002_manifest_mutation",
        "no_v002_acquisition_log_mutation",
        "no_phase_4bl_d_r_gate_report_mutation",
        "no_phase_4bl_d_fail_report_mutation",
        "no_phase_4bl_d_s2_canon_report_mutation",
        "no_canonicalized_sidecar_mutation",
        "no_raw_zip_mutation",
        "no_research_eligible_manifest_flip",
        "no_eligibility_gate_status_manifest_transition",
        "no_chronological_split_policy_change",
        "no_gate_rerun",
        "no_data_acquisition",
        "no_normalization",
        "no_feature_parquet_created",
        "no_label_parquet_created",
        "no_diagnostics_run",
        "no_signal_computed",
        "no_ml_training",
        "no_strategy_creation",
        "no_backtest",
        "no_strategy_output_metrics",
        "no_public_endpoint_use",
        "no_binance_api_use",
        "no_authenticated_api_use",
        "no_private_endpoint_use",
        "no_user_stream_use",
        "no_websocket",
        "no_credentials",
        "no_env",
        "no_mcp_or_graphify",
        "no_phase_4bb_f_amendment",
        "no_phase_4bl_d_gate_amendment",
        "no_check_weakening",
        "no_sidecar_parser_relaxation",
        "no_retained_verdict_revision",
        "no_project_lock_change",
        "no_m0_amendment",
        "no_successor_authorization",
        "phase_4aw_flip_research_eligible_invariant_preserved",
    ):
        assert required in boundaries


def test_payload_retained_verdict_ledger_verbatim(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    ledger = payload["retained_verdict_ledger"]
    assert ledger["H0"] == "FRAMEWORK ANCHOR"
    assert ledger["R3"] == "BASELINE-OF-RECORD"
    assert ledger["R1a"] == "RETAINED - NON-LEADING"
    assert ledger["R1b_narrow"] == "RETAINED - NON-LEADING"
    assert ledger["R2"] == "FAILED - section_11_6"
    assert ledger["F1"] == "HARD REJECT"
    assert ledger["D1_A"] == "MECHANISM PASS / FRAMEWORK FAIL"
    assert ledger["five_minute_thread"] == "OPERATIONALLY CLOSED (Phase 3t)"
    assert ledger["V2"] == "HARD REJECT - terminal for V2 first-spec"
    assert ledger["G1"] == "HARD REJECT - terminal for G1 first-spec"
    assert ledger["C1"] == "HARD REJECT - terminal for C1 first-spec"


def test_payload_preserved_locks_listed(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    locks = payload["preserved_project_locks"]
    assert isinstance(locks, list)
    joined = "\n".join(locks)
    assert "section_11_6 = 8 bps per side" in joined
    assert "section_1_7_3" in joined
    assert "Phase 4ak M0 twelve-clause gate" in joined
    assert "Phase 4al refined no-rescue rule" in joined
    assert "Phase 4aw" in joined
    assert "Phase 4bb-F canonical path policy" in joined
    assert "Phase 4bl-D 33-check raw eligibility-gate" in joined
    assert "Phase 4bl-D-S2 sidecar canonicalisation" in joined


def test_payload_no_rescue_statement_present(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    statement = payload["no_rescue_statement"]
    assert "Phase 4bl-E" in statement
    assert "cooled-down family" in statement
    assert "R2" in statement and "F1" in statement
    assert "M0" in statement


def test_payload_serializes_to_valid_json(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    body = script_module.serialize_successor_state(payload)
    reparsed = json.loads(body.decode("utf-8"))
    assert reparsed == payload


def test_payload_round_trip_byte_identical(script_module) -> None:
    payload = _build_synthetic_payload(script_module)
    body_1 = script_module.serialize_successor_state(payload)
    body_2 = script_module.serialize_successor_state(payload)
    assert body_1 == body_2


# ---------------------------------------------------------------------------
# Fake-repo fixture builder
# ---------------------------------------------------------------------------


def _write_with_sha(target: Path, body: bytes) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    return hashlib.sha256(body).hexdigest()


def _build_v002_manifest_payload(
    *,
    research_eligible: bool = False,
    eligibility_gate_status: str = "pending",
    date_count: int = 90,
    total_row_count: int = 155_153_449,
    total_size_bytes: int = 1_943_823_208,
) -> bytes:
    """Build a JSON v002 manifest body matching the script's verifier expectations."""
    manifest = {
        "dataset_family": "microstructure_raw_aggtrades_v001",
        "dataset_version": "v002",
        "symbol_list": ["BTCUSDT"],
        "date_start": "2024-12-01",
        "date_end": "2025-02-28",
        "date_count": date_count,
        "total_row_count": total_row_count,
        "total_size_bytes": total_size_bytes,
        "research_eligible": research_eligible,
        "eligibility_gate_status": eligibility_gate_status,
    }
    return json.dumps(manifest, sort_keys=True, indent=2).encode("utf-8")


def _build_gate_report_payload(
    *,
    overall_status: str = "pass",
    verdict: str = "RAW_MULTIDAY_GATE_PASS",
) -> bytes:
    report = {
        "phase": "Phase 4bl-D-R",
        "overall_status": overall_status,
        "gate_verdict": verdict,
        "checks_total": 33,
        "checks_passed": 33,
        "checks_failed": 0,
    }
    return json.dumps(report, sort_keys=True, indent=2).encode("utf-8")


def _setup_fake_repo(
    tmp_path: Path,
    script_module,
    *,
    manifest_overrides: Mapping[str, object] | None = None,
    gate_report_overrides: Mapping[str, object] | None = None,
    monkeypatch_target,
) -> dict[str, object]:
    """Build a tmp data tree, write all 10 inputs, and monkeypatch script paths.

    Returns a dict of recomputed SHAs (matching the new EXPECTED_SHAS the
    monkeypatch installs into the script module).
    """
    micro = tmp_path / "data" / "microstructure"
    manifests_dir = micro / "manifests"
    raw_dir = (
        micro
        / "raw"
        / "microstructure_raw_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
    )
    gate_dir = micro / "gate-reports" / "raw"
    canon_dir = micro / "canonicalization-reports" / "raw"
    successor_dir = micro / "successor-state"

    # v002 manifest + sidecar.
    manifest_body_kwargs: dict[str, object] = {}
    if manifest_overrides:
        manifest_body_kwargs.update(manifest_overrides)
    manifest_body = _build_v002_manifest_payload(**manifest_body_kwargs)  # type: ignore[arg-type]
    v002_manifest_path = (
        manifests_dir / "microstructure_raw_aggtrades_v001__v002.json"
    )
    v002_manifest_sha = _write_with_sha(v002_manifest_path, manifest_body)
    v002_manifest_sidecar_path = v002_manifest_path.with_suffix(
        v002_manifest_path.suffix + ".sha256"
    )
    sidecar_body_manifest = (
        f"{v002_manifest_sha}  {v002_manifest_path.name}\n".encode()
    )
    v002_manifest_sidecar_sha = _write_with_sha(
        v002_manifest_sidecar_path, sidecar_body_manifest
    )

    # v002 acquisition log + sidecar.
    acq_body = b'{"events":[],"summary":"fake acquisition log"}\n'
    v002_acq_log_path = (
        manifests_dir
        / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json"
    )
    v002_acq_log_sha = _write_with_sha(v002_acq_log_path, acq_body)
    v002_acq_log_sidecar_path = v002_acq_log_path.with_suffix(
        v002_acq_log_path.suffix + ".sha256"
    )
    sidecar_body_acq = (
        f"{v002_acq_log_sha}  {v002_acq_log_path.name}\n".encode()
    )
    v002_acq_log_sidecar_sha = _write_with_sha(
        v002_acq_log_sidecar_path, sidecar_body_acq
    )

    # Phase 4bl-D-R gate report + sidecar (PASS by default).
    report_body_kwargs: dict[str, object] = {}
    if gate_report_overrides:
        report_body_kwargs.update(gate_report_overrides)
    report_body = _build_gate_report_payload(**report_body_kwargs)  # type: ignore[arg-type]
    report_path = (
        gate_dir
        / "microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__"
          "1778717359124__69e45280f080.json"
    )
    report_sha = _write_with_sha(report_path, report_body)
    report_sidecar_path = report_path.with_suffix(report_path.suffix + ".sha256")
    sidecar_body_report = f"{report_sha}  {report_path.name}\n".encode()
    report_sidecar_sha = _write_with_sha(report_sidecar_path, sidecar_body_report)

    # Phase 4bl-D FAIL report (historical evidence).
    fail_body = json.dumps(
        {
            "phase": "Phase 4bl-D",
            "overall_status": "fail",
            "gate_verdict": "RAW_MULTIDAY_GATE_FAIL",
        },
        sort_keys=True,
        indent=2,
    ).encode("utf-8")
    fail_report_path = (
        gate_dir
        / "microstructure_raw_aggtrades_v001__v002__phase-4bl-d__"
          "1778627360966__2576a004c18a.json"
    )
    fail_report_sha = _write_with_sha(fail_report_path, fail_body)

    # Phase 4bl-D-S2 canonicalisation report.
    canon_body = json.dumps(
        {
            "phase": "Phase 4bl-D-S2",
            "mutation_type": "metadata_sidecar_line_ending_canonicalization",
        },
        sort_keys=True,
        indent=2,
    ).encode("utf-8")
    canon_report_path = (
        canon_dir
        / "microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__"
          "1778713761225__0d51bd7bac1e.json"
    )
    canon_report_sha = _write_with_sha(canon_report_path, canon_body)

    # Canonicalized 2025-01-15 sidecar + raw zip.
    raw_zip_body = b"FAKE-2025-01-15-RAW-ZIP-PAYLOAD"
    raw_zip_path = raw_dir / "BTCUSDT-aggTrades-2025-01-15.zip"
    raw_zip_sha = _write_with_sha(raw_zip_path, raw_zip_body)
    canonicalized_sidecar_body = (
        f"{raw_zip_sha}  {raw_zip_path.name}\n".encode()
    )
    canonicalized_sidecar_path = raw_zip_path.with_suffix(
        raw_zip_path.suffix + ".sha256"
    )
    canonicalized_sidecar_sha = _write_with_sha(
        canonicalized_sidecar_path, canonicalized_sidecar_body
    )

    # Monkeypatch all 10 paths + successor-state directory.
    monkeypatch_target.setattr(script_module, "REPO_ROOT", tmp_path)
    monkeypatch_target.setattr(script_module, "DATA_MICRO", micro)
    monkeypatch_target.setattr(script_module, "SUCCESSOR_STATE_DIR", successor_dir)
    monkeypatch_target.setattr(script_module, "V002_MANIFEST_PATH", v002_manifest_path)
    monkeypatch_target.setattr(
        script_module,
        "V002_MANIFEST_SIDECAR_PATH",
        v002_manifest_sidecar_path,
    )
    monkeypatch_target.setattr(script_module, "V002_ACQ_LOG_PATH", v002_acq_log_path)
    monkeypatch_target.setattr(
        script_module,
        "V002_ACQ_LOG_SIDECAR_PATH",
        v002_acq_log_sidecar_path,
    )
    monkeypatch_target.setattr(
        script_module, "PHASE_4BL_D_R_REPORT_PATH", report_path
    )
    monkeypatch_target.setattr(
        script_module,
        "PHASE_4BL_D_R_REPORT_SIDECAR_PATH",
        report_sidecar_path,
    )
    monkeypatch_target.setattr(
        script_module, "PHASE_4BL_D_FAIL_REPORT_PATH", fail_report_path
    )
    monkeypatch_target.setattr(
        script_module,
        "PHASE_4BL_D_S2_CANON_REPORT_PATH",
        canon_report_path,
    )
    monkeypatch_target.setattr(
        script_module,
        "CANONICALIZED_2025_01_15_SIDECAR_PATH",
        canonicalized_sidecar_path,
    )
    monkeypatch_target.setattr(
        script_module, "RAW_2025_01_15_ZIP_PATH", raw_zip_path
    )

    fake_shas = {
        "v002_raw_manifest": v002_manifest_sha,
        "v002_raw_manifest_sidecar": v002_manifest_sidecar_sha,
        "v002_acquisition_log": v002_acq_log_sha,
        "v002_acquisition_log_sidecar": v002_acq_log_sidecar_sha,
        "phase_4bl_d_r_report": report_sha,
        "phase_4bl_d_r_report_sidecar": report_sidecar_sha,
        "phase_4bl_d_fail_report": fail_report_sha,
        "phase_4bl_d_s2_canon_report": canon_report_sha,
        "canonicalized_2025_01_15_sidecar": canonicalized_sidecar_sha,
        "raw_2025_01_15_zip": raw_zip_sha,
    }
    monkeypatch_target.setattr(script_module, "EXPECTED_SHAS", fake_shas)
    return {
        "successor_dir": successor_dir,
        "v002_manifest_path": v002_manifest_path,
        "report_path": report_path,
        "raw_zip_path": raw_zip_path,
        "fake_shas": fake_shas,
    }


# ---------------------------------------------------------------------------
# End-to-end run() tests using monkeypatched paths and SHAs
# ---------------------------------------------------------------------------


def test_run_happy_path_writes_two_outputs(tmp_path, script_module, monkeypatch):
    fakes = _setup_fake_repo(tmp_path, script_module, monkeypatch_target=monkeypatch)
    rc = script_module.run()
    assert rc == 0
    successor_dir = fakes["successor_dir"]
    expected_basename = (
        "microstructure_raw_aggtrades_v001__v002__"
        "stage2_raw_admissible__phase-4bl-e.json"
    )
    target = successor_dir / expected_basename
    sidecar = successor_dir / f"{expected_basename}.sha256"
    assert target.exists()
    assert sidecar.exists()
    body = target.read_bytes()
    sidecar_body = sidecar.read_bytes()
    # The JSON must parse and contain the expected top-level keys.
    payload = json.loads(body.decode("utf-8"))
    assert payload["phase"] == "Phase 4bl-E"
    assert payload["successor_state"] == "stage2_raw_admissible"
    assert payload["dataset_version"] == "v002"
    # Sidecar body format: "<sha>  <basename>\n", trailing LF, no CRLF.
    expected_sha = hashlib.sha256(body).hexdigest()
    assert sidecar_body == f"{expected_sha}  {expected_basename}\n".encode()
    assert sidecar_body.endswith(b"\n")
    assert b"\r\n" not in sidecar_body


def test_run_is_idempotent(tmp_path, script_module, monkeypatch):
    """When repeated calls produce byte-identical content, the second
    call is a no-op (the writer returns early because the existing file
    bytes match the new body). To make consecutive calls byte-identical,
    pin the timestamp helpers + git-rev helpers so both invocations
    serialise the same payload."""
    _setup_fake_repo(tmp_path, script_module, monkeypatch_target=monkeypatch)

    fixed_now = "2026-05-14T01:00:00+00:00"
    fixed_ms = 1_778_805_600_000

    class _FixedDatetime:
        @staticmethod
        def now(_tz=None):  # noqa: ARG004
            class _Stamp:
                @staticmethod
                def timestamp() -> float:
                    return fixed_ms / 1000.0

                @staticmethod
                def isoformat() -> str:
                    return fixed_now

            return _Stamp()

    monkeypatch.setattr(script_module, "datetime", _FixedDatetime)
    monkeypatch.setattr(script_module, "_git_rev_parse_head", lambda: "a" * 40)
    monkeypatch.setattr(script_module, "_git_rev_parse_main", lambda: "b" * 40)

    rc1 = script_module.run()
    rc2 = script_module.run()
    assert rc1 == 0
    assert rc2 == 0


def test_run_refuses_overwrite_when_existing_bytes_differ(
    tmp_path, script_module, monkeypatch
):
    fakes = _setup_fake_repo(tmp_path, script_module, monkeypatch_target=monkeypatch)
    rc = script_module.run()
    assert rc == 0
    # Mutate the existing successor-state file so the next run sees a
    # non-byte-identical existing target.
    successor_dir = fakes["successor_dir"]
    target = successor_dir / (
        "microstructure_raw_aggtrades_v001__v002__"
        "stage2_raw_admissible__phase-4bl-e.json"
    )
    target.write_bytes(target.read_bytes() + b"\nDIRTY")
    with pytest.raises(script_module.SuccessorStateError):
        script_module.run()


def test_run_refuses_when_verdict_is_not_pass(tmp_path, script_module, monkeypatch):
    _setup_fake_repo(
        tmp_path,
        script_module,
        monkeypatch_target=monkeypatch,
        gate_report_overrides={
            "overall_status": "fail",
            "verdict": "RAW_MULTIDAY_GATE_FAIL",
        },
    )
    # SHA mismatch is the proximate failure mode (the gate report body
    # SHA changes when the verdict changes, but EXPECTED_SHAS still
    # carries the recomputed SHA for that fail body — so the verdict
    # itself is what trips).
    with pytest.raises(script_module.SuccessorStateError):
        script_module.run()


def test_run_refuses_when_manifest_research_eligible_is_true(
    tmp_path, script_module, monkeypatch
):
    _setup_fake_repo(
        tmp_path,
        script_module,
        monkeypatch_target=monkeypatch,
        manifest_overrides={"research_eligible": True},
    )
    with pytest.raises(script_module.SuccessorStateError):
        script_module.run()


def test_run_refuses_when_manifest_gate_status_is_pass(
    tmp_path, script_module, monkeypatch
):
    _setup_fake_repo(
        tmp_path,
        script_module,
        monkeypatch_target=monkeypatch,
        manifest_overrides={"eligibility_gate_status": "pass"},
    )
    with pytest.raises(script_module.SuccessorStateError):
        script_module.run()


def test_run_refuses_when_manifest_row_count_is_wrong(
    tmp_path, script_module, monkeypatch
):
    _setup_fake_repo(
        tmp_path,
        script_module,
        monkeypatch_target=monkeypatch,
        manifest_overrides={"total_row_count": 12345},
    )
    with pytest.raises(script_module.SuccessorStateError):
        script_module.run()


def test_run_refuses_when_manifest_date_count_is_wrong(
    tmp_path, script_module, monkeypatch
):
    _setup_fake_repo(
        tmp_path,
        script_module,
        monkeypatch_target=monkeypatch,
        manifest_overrides={"date_count": 30},
    )
    with pytest.raises(script_module.SuccessorStateError):
        script_module.run()


def test_run_refuses_when_input_sha_mismatch(tmp_path, script_module, monkeypatch):
    fakes = _setup_fake_repo(tmp_path, script_module, monkeypatch_target=monkeypatch)
    # Corrupt the v002 manifest body so its SHA no longer matches the
    # recomputed EXPECTED_SHAS value the fake fixture installed.
    fakes["v002_manifest_path"].write_bytes(b"{}")
    with pytest.raises(script_module.SuccessorStateError):
        script_module.run()


def test_run_refuses_when_required_input_missing(
    tmp_path, script_module, monkeypatch
):
    fakes = _setup_fake_repo(tmp_path, script_module, monkeypatch_target=monkeypatch)
    fakes["report_path"].unlink()
    with pytest.raises(script_module.SuccessorStateError):
        script_module.run()


def test_run_output_path_is_under_successor_state_namespace(
    tmp_path, script_module, monkeypatch
):
    fakes = _setup_fake_repo(tmp_path, script_module, monkeypatch_target=monkeypatch)
    rc = script_module.run()
    assert rc == 0
    target = next(fakes["successor_dir"].glob("*.json"))
    parts = target.resolve().parts
    needle = ("data", "microstructure", "successor-state")
    assert any(
        parts[i : i + len(needle)] == needle
        for i in range(len(parts) - len(needle) + 1)
    )


def test_run_does_not_mutate_inputs(tmp_path, script_module, monkeypatch):
    fakes = _setup_fake_repo(tmp_path, script_module, monkeypatch_target=monkeypatch)
    pre = {
        "manifest": hashlib.sha256(
            fakes["v002_manifest_path"].read_bytes()
        ).hexdigest(),
        "report": hashlib.sha256(fakes["report_path"].read_bytes()).hexdigest(),
        "raw_zip": hashlib.sha256(fakes["raw_zip_path"].read_bytes()).hexdigest(),
    }
    rc = script_module.run()
    assert rc == 0
    post = {
        "manifest": hashlib.sha256(
            fakes["v002_manifest_path"].read_bytes()
        ).hexdigest(),
        "report": hashlib.sha256(fakes["report_path"].read_bytes()).hexdigest(),
        "raw_zip": hashlib.sha256(fakes["raw_zip_path"].read_bytes()).hexdigest(),
    }
    assert pre == post


# ---------------------------------------------------------------------------
# Forbidden-import scan (static)
# ---------------------------------------------------------------------------


FORBIDDEN_IMPORT_MODULES: Iterable[str] = (
    "requests",
    "httpx",
    "aiohttp",
    "urllib3",
    "websockets",
    "binance",
    "dotenv",
    "python_dotenv",
    "socket",
    "urllib.request",
    "urllib.parse",
    "urllib.error",
    "urllib",
)

FORBIDDEN_RUNTIME_TOKENS: Iterable[str] = (
    "API_KEY",
    "secret(",
    "signature(",
    "listenKey",
    "userDataStream",
    "/fapi/v1/order",
    "/fapi/v2/account",
    "/fapi/v2/positionRisk",
    "/fapi/v1/leverage",
    "/fapi/v1/marginType",
    "/fapi/v1/forceOrders",
    "Graphify",
    "os.environ",
    "os.getenv",
    "getpass",
)


def _iter_import_lines(source: str):
    """Yield logical import lines from *source* (excluding comments)."""
    for raw_line in source.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            continue
        if stripped.startswith(("import ", "from ")):
            yield stripped


def test_script_has_no_forbidden_imports():
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    import_lines = list(_iter_import_lines(source))
    head_tokens: list[str] = []
    for line in import_lines:
        head = line.split("#", 1)[0].strip()
        head = head.split(" as ", 1)[0]
        parts = head.split()
        if not parts:
            continue
        if parts[0] == "import":
            head_tokens.extend(parts[1:])
        elif parts[0] == "from" and len(parts) >= 2:
            head_tokens.append(parts[1])
    for forbidden in FORBIDDEN_IMPORT_MODULES:
        for tok in head_tokens:
            assert not tok.startswith(forbidden), (
                f"forbidden import found: {tok!r} (matches {forbidden!r})"
            )


def test_script_has_no_runtime_credential_tokens():
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    # Drop the module docstring header (which is allowed to mention these
    # tokens descriptively in the safety preamble).
    stripped = source.split('"""', 2)
    body = stripped[2] if len(stripped) == 3 else source
    body = "\n".join(
        line for line in body.splitlines() if not line.lstrip().startswith("#")
    )
    for tok in FORBIDDEN_RUNTIME_TOKENS:
        assert tok not in body, f"forbidden runtime token found: {tok!r}"


def test_script_has_no_prometheus_import():
    """The Phase 4bl-E script must not import any prometheus.* module."""
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    import_lines = list(_iter_import_lines(source))
    for line in import_lines:
        head = line.split("#", 1)[0].strip()
        head = head.split(" as ", 1)[0]
        parts = head.split()
        if not parts:
            continue
        target = parts[1] if parts[0] in {"import", "from"} else ""
        assert not target.startswith("prometheus"), (
            f"forbidden prometheus.* import found: {line!r}"
        )
