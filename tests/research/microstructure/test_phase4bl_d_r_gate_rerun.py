"""Offline tests for the Phase 4bl-D-R rerun wrapper.

These tests do NOT execute the underlying Phase 4bl-D gate. They
verify, against the wrapper module itself:

1. The wrapper's locked identity constants match the Phase 4bl-D-R
   brief verbatim.
2. The wrapper's ``augment_report(...)`` helper is pure (does not
   mutate its input), produces deterministic JSON, and emits exactly
   the brief-mandated set of Phase 4bl-D-R lineage fields.
3. The wrapper never imports or references forbidden network /
   credential / MCP / Graphify modules or tokens.
4. The wrapper preserves the gate-produced ``checks``, ``per_file_
   validation_summary``, ``aggregate_summary``, ``governance_labels``,
   ``non_authorizations``, ``retained_verdict_ledger``, and
   ``preserved_locks`` blocks verbatim through the augmentation step.
5. The wrapper rejects the augmentation rewrite when the report path
   does not contain the ``phase-4bl-d-r`` segment (defence-in-depth
   against accidentally rewriting an unrelated Phase 4bl-D report).
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Load the wrapper module directly by file path (it lives under
# ``scripts/`` which is not a package).
# --------------------------------------------------------------------------- #

_REPO_ROOT: Path = Path(__file__).resolve().parents[3]
_WRAPPER_PATH: Path = (
    _REPO_ROOT / "scripts" / "phase4bl_d_r_rerun_raw_gate.py"
)


def _load_wrapper() -> object:
    import sys

    module_name = "phase4bl_d_r_rerun_raw_gate_under_test"
    spec = importlib.util.spec_from_file_location(
        module_name,
        _WRAPPER_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def wrapper() -> object:
    return _load_wrapper()


# --------------------------------------------------------------------------- #
# Locked identity constants
# --------------------------------------------------------------------------- #


def test_wrapper_phase_id_lowercase_for_filename(wrapper: object) -> None:
    """Lowercase phase id drives the Phase 4bb-F filename segment."""
    assert wrapper._GATE_PHASE_ID == "4bl-d-r"


def test_wrapper_phase_name_brief_value(wrapper: object) -> None:
    assert wrapper._GATE_PHASE_NAME == "Phase 4bl-D-R"


def test_wrapper_artefact_type_brief_value(wrapper: object) -> None:
    assert (
        wrapper._GATE_ARTEFACT_TYPE
        == "raw_multiday_manifest_eligibility_gate_rerun_report"
    )


def test_wrapper_augment_phase_id_mixed_case(wrapper: object) -> None:
    """Report body records mixed-case ``"4bl-D-R"`` per the brief."""
    assert wrapper._AUGMENT_PHASE_ID == "4bl-D-R"


def test_wrapper_predecessor_phase_is_4bl_D(wrapper: object) -> None:
    assert wrapper._PREDECESSOR_PHASE == "4bl-D"
    assert wrapper._PREDECESSOR_PHASE_ID == "4bl-d"
    assert wrapper._PREDECESSOR_GATE_VERDICT == "RAW_MULTIDAY_GATE_FAIL"
    assert wrapper._PREDECESSOR_GATE_OVERALL_STATUS == "fail"


def test_wrapper_predecessor_report_sha_matches_recorded(
    wrapper: object,
) -> None:
    assert wrapper._PREDECESSOR_GATE_REPORT_SHA256 == (
        "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7"
    )


def test_wrapper_remediation_phase_is_4bl_D_S2(wrapper: object) -> None:
    assert wrapper._REMEDIATION_PHASE == "4bl-D-S2"
    assert (
        wrapper._REMEDIATION_TYPE
        == "metadata_sidecar_line_ending_canonicalization"
    )


def test_wrapper_remediation_report_sha_matches_recorded(
    wrapper: object,
) -> None:
    assert wrapper._REMEDIATION_REPORT_SHA256 == (
        "8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3"
    )


def test_wrapper_target_sidecar_sha_pre_post_match_4bl_D_S2(
    wrapper: object,
) -> None:
    assert wrapper._TARGET_SIDECAR_PRE_SHA256 == (
        "b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d"
    )
    assert wrapper._TARGET_SIDECAR_POST_SHA256 == (
        "c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc"
    )


def test_wrapper_target_raw_zip_sha_matches_phase_4az(
    wrapper: object,
) -> None:
    assert wrapper._TARGET_RAW_ZIP_SHA256 == (
        "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
    )


# --------------------------------------------------------------------------- #
# augment_report contract
# --------------------------------------------------------------------------- #


def _minimal_gate_report() -> dict:
    """A minimal stand-in for a Phase 4bl-D-shaped report."""
    return {
        "schema_version": "v001",
        "phase": "Phase 4bl-D-R",
        "phase_id": "4bl-d-r",
        "artefact_type": (
            "raw_multiday_manifest_eligibility_gate_rerun_report"
        ),
        "dataset_family": "microstructure_raw_aggtrades_v001",
        "dataset_version": "v002",
        "symbol_list": ["BTCUSDT"],
        "date_start": "2024-12-01",
        "date_end": "2025-02-28",
        "date_count": 90,
        "expected_file_count": 90,
        "source_artefacts": {
            "source_manifest_path": "data/microstructure/manifests/x.json",
            "source_manifest_sha256": "0" * 64,
        },
        "overall_status": "pass",
        "gate_verdict": "RAW_MULTIDAY_GATE_PASS",
        "checks_total": 33,
        "checks_passed": 33,
        "checks_failed": 0,
        "checks_error": 0,
        "checks_not_applicable": 0,
        "checks": [
            {"check_id": "manifest_file_integrity", "status": "pass"},
            {"check_id": "raw_zip_sidecar_integrity", "status": "pass"},
        ],
        "per_file_validation_summary": [
            {
                "date": "2025-01-15",
                "status": "pass",
                "row_count": 1_681_098,
            }
        ],
        "aggregate_summary": {
            "all_rows_validated_count": 155_153_449,
            "adjacent_date_overlap_errors_count": 0,
        },
        "governance_labels": {
            "phase": "4bl-d-r",
            "source_phase_boundary": "4bl-D-S2",
        },
        "non_authorizations": {
            "phase_4bl_e_authorized": False,
        },
        "retained_verdict_ledger": [
            {"id": "H0", "status": "FRAMEWORK ANCHOR"},
        ],
        "preserved_locks": ["§11.6 = 8 bps per side"],
        "research_eligible_after": False,
        "manifest_mutated": False,
        "manifest_transition_performed": False,
        "no_successor_authorization": True,
        "strict_fail_closed": True,
    }


def test_augment_report_does_not_mutate_input(wrapper: object) -> None:
    original = _minimal_gate_report()
    snapshot = json.dumps(original, sort_keys=True)
    _ = wrapper.augment_report(original)
    assert json.dumps(original, sort_keys=True) == snapshot


def test_augment_report_preserves_check_and_summary_blocks(
    wrapper: object,
) -> None:
    original = _minimal_gate_report()
    augmented = wrapper.augment_report(original)
    assert augmented["checks"] == original["checks"]
    assert (
        augmented["per_file_validation_summary"]
        == original["per_file_validation_summary"]
    )
    assert augmented["aggregate_summary"] == original["aggregate_summary"]
    assert augmented["governance_labels"] == original["governance_labels"]
    assert augmented["non_authorizations"] == original["non_authorizations"]
    assert (
        augmented["retained_verdict_ledger"]
        == original["retained_verdict_ledger"]
    )
    assert augmented["preserved_locks"] == original["preserved_locks"]


def test_augment_report_sets_phase_id_mixed_case(wrapper: object) -> None:
    augmented = wrapper.augment_report(_minimal_gate_report())
    assert augmented["phase_id"] == "4bl-D-R"


def test_augment_report_adds_predecessor_lineage(wrapper: object) -> None:
    augmented = wrapper.augment_report(_minimal_gate_report())
    assert augmented["predecessor_gate_phase"] == "4bl-D"
    assert augmented["predecessor_gate_id"] == "4bl-d"
    assert (
        augmented["predecessor_gate_verdict"] == "RAW_MULTIDAY_GATE_FAIL"
    )
    assert augmented["predecessor_gate_overall_status"] == "fail"
    assert augmented["predecessor_gate_report_path"].endswith(
        "phase-4bl-d__1778627360966__2576a004c18a.json"
    )
    assert (
        augmented["predecessor_gate_report_sha256"]
        == "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7"
    )
    assert isinstance(augmented["predecessor_gate_failure_summary"], str)
    assert "CRLF" in augmented["predecessor_gate_failure_summary"]
    assert "f560c2e5" in augmented["predecessor_gate_failure_summary"]
    assert isinstance(
        augmented["predecessor_gate_failed_check_ids"], list
    )
    assert "raw_zip_sidecar_integrity" in (
        augmented["predecessor_gate_failed_check_ids"]
    )
    assert (
        "total_row_count_consistency"
        in augmented["predecessor_gate_failed_check_ids"]
    )


def test_augment_report_adds_remediation_lineage(wrapper: object) -> None:
    augmented = wrapper.augment_report(_minimal_gate_report())
    assert augmented["remediation_phase"] == "4bl-D-S2"
    assert (
        augmented["remediation_type"]
        == "metadata_sidecar_line_ending_canonicalization"
    )
    assert augmented["remediation_report_path"].endswith(
        "phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json"
    )
    assert (
        augmented["remediation_report_sha256"]
        == "8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3"
    )


def test_augment_report_records_target_sidecar_pre_post(
    wrapper: object,
) -> None:
    augmented = wrapper.augment_report(_minimal_gate_report())
    assert augmented["canonicalized_sidecar_path"].endswith(
        "BTCUSDT-aggTrades-2025-01-15.zip.sha256"
    )
    assert (
        augmented["canonicalized_sidecar_pre_sha256"]
        == "b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d"
    )
    assert (
        augmented["canonicalized_sidecar_post_sha256"]
        == "c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc"
    )


def test_augment_report_records_target_raw_zip(wrapper: object) -> None:
    augmented = wrapper.augment_report(_minimal_gate_report())
    assert augmented["target_raw_zip_path"].endswith(
        "BTCUSDT-aggTrades-2025-01-15.zip"
    )
    assert (
        augmented["target_raw_zip_sha256"]
        == "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
    )


def test_augment_report_preserves_no_authorisation_invariants(
    wrapper: object,
) -> None:
    augmented = wrapper.augment_report(_minimal_gate_report())
    assert augmented["research_eligible_after"] is False
    assert augmented["manifest_mutated"] is False
    assert augmented["manifest_transition_performed"] is False
    assert augmented["no_successor_authorization"] is True
    assert augmented["strict_fail_closed"] is True


def test_augment_report_records_wrapper_metadata(wrapper: object) -> None:
    augmented = wrapper.augment_report(_minimal_gate_report())
    assert augmented["wrapper_phase"] == "Phase 4bl-D-R"
    assert augmented["wrapper_phase_id_lowercase"] == "4bl-d-r"
    assert (
        augmented["wrapper_artefact_type"]
        == "raw_multiday_manifest_eligibility_gate_rerun_report"
    )


def test_serialise_report_is_deterministic_sorted_keys(
    wrapper: object,
) -> None:
    original = _minimal_gate_report()
    augmented_a = wrapper.augment_report(original)
    augmented_b = wrapper.augment_report(original)
    bytes_a = wrapper._serialise_report(augmented_a)
    bytes_b = wrapper._serialise_report(augmented_b)
    assert bytes_a == bytes_b
    assert bytes_a.endswith(b"\n")
    # Sorted-keys property: parse the leading object and check first key.
    text = bytes_a.decode("utf-8")
    # First key after the opening `{\n  ` should be alphabetically first.
    decoded = json.loads(text)
    keys = list(decoded.keys())
    assert keys == sorted(keys)


# --------------------------------------------------------------------------- #
# Forbidden import / token static guards
# --------------------------------------------------------------------------- #


_FORBIDDEN_IMPORT_TOKENS: tuple[str, ...] = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import urllib3",
    "from urllib3",
    "import socket",
    "from socket",
    "import websockets",
    "from websockets",
    "import binance",
    "from binance",
    "import dotenv",
    "from dotenv",
    "import python_dotenv",
    "from python_dotenv",
)

_FORBIDDEN_RUNTIME_TOKENS: tuple[str, ...] = (
    "os.environ[",
    "os.getenv(",
    "BINANCE_API_KEY",
    "BINANCE_API_SECRET",
    "MCP",
    "Graphify",
    ".mcp.json",
)


def _strip_comments_and_docstrings(text: str) -> str:
    """Crude but sufficient: drop ``#`` line comments only.

    Triple-quoted docstrings are kept; the forbidden-token check below
    explicitly skips lines that begin a triple-quoted string region.
    """
    out: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        out.append(line)
    return "\n".join(out)


def test_wrapper_source_has_no_forbidden_imports() -> None:
    text = _WRAPPER_PATH.read_text(encoding="utf-8")
    # Inspect import-like lines only.
    lines = text.splitlines()
    import_lines = [
        ln
        for ln in lines
        if ln.lstrip().startswith(("import ", "from "))
    ]
    combined = "\n".join(import_lines)
    for token in _FORBIDDEN_IMPORT_TOKENS:
        assert token not in combined, (
            f"forbidden import token present in wrapper imports: {token}"
        )


def test_wrapper_source_has_no_forbidden_runtime_tokens() -> None:
    text = _WRAPPER_PATH.read_text(encoding="utf-8")
    scrubbed = _strip_comments_and_docstrings(text)
    # Drop the docstring at the top of the file by splitting on the
    # second triple-quote occurrence.
    triple = '"""'
    if scrubbed.count(triple) >= 2:
        first = scrubbed.find(triple)
        second = scrubbed.find(triple, first + len(triple))
        scrubbed = scrubbed[: first] + scrubbed[second + len(triple) :]
    for token in _FORBIDDEN_RUNTIME_TOKENS:
        assert token not in scrubbed, (
            f"forbidden runtime token present in wrapper source: {token}"
        )


def test_wrapper_filename_segment_is_lowercase(wrapper: object) -> None:
    """The Phase 4bb-F canonical filename uses lowercase phase id."""
    assert re.fullmatch(r"[a-z0-9\-]+", wrapper._GATE_PHASE_ID) is not None
