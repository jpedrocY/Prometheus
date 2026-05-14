"""Phase 4bl-E — Multi-Day Raw Manifest Successor-State Recording.

This standalone script records exactly one local gitignored sibling
successor-state JSON artefact for the v002 multi-day BTCUSDT
aggTrades raw dataset (`microstructure_raw_aggtrades_v001`,
`dataset_version=v002`) after the Phase 4bl-D-R rerun produced
``RAW_MULTIDAY_GATE_PASS`` (33 / 33 PASS). It also writes the
paired canonical Phase 4bb-F ``.sha256`` sidecar.

The script:

- reads local files only;
- never opens a network socket;
- never reads or creates credentials, ``.env``, or ``.mcp.json``;
- never modifies the v002 raw manifest;
- never flips ``research_eligible``;
- never transitions ``eligibility_gate_status`` on any manifest;
- never reruns the raw gate;
- never creates a new gate report;
- verifies eight SHA256 inputs by recomputation;
- writes exactly two outputs (one JSON + one ``.sha256`` sidecar)
  under the gitignored ``data/microstructure/successor-state/``
  namespace;
- refuses to overwrite either output unless byte-identical;
- emits a clear console summary.

The deterministic JSON serialisation uses ``sort_keys=True``,
``indent=2``, ``ensure_ascii=False``, and **no trailing newline**
(matching the Phase 4bb-G raw successor-state precedent verbatim
so byte-comparison across raw-family successor-state artefacts is
straightforward).

The paired ``.sha256`` sidecar uses the canonical Phase 4bb-F
format ``<sha256_hex>  <basename>\\n`` (two spaces; trailing LF;
no CRLF; no BOM).

The script is invoked once at branch execution time. It is also
re-runnable: a second invocation against the same inputs is a
no-op (refuse-overwrite returns successfully because the
recomputed bytes are byte-identical to the already-written
outputs).

Forbidden imports (statically scanned by
``tests/research/microstructure/test_phase4bl_e_raw_successor_state.py``):
``requests``, ``httpx``, ``aiohttp``, ``urllib.request``,
``urllib3``, ``socket``, ``websockets``, ``binance``, ``dotenv``,
``python_dotenv``, ``os.environ``, ``getenv``.

Phase 4aw ``MicrostructureManifest.flip_research_eligible(...)``
always-raises invariant: never invoked by this script. The script
does not import any ``prometheus`` module.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Locked constants (predeclared by the Phase 4bl-E authorization prompt)
# ---------------------------------------------------------------------------

PHASE_ID: str = "4bl-e"
PHASE_NAME: str = "Phase 4bl-E"
SCHEMA_VERSION: str = "v001"
ARTEFACT_TYPE: str = "raw_multiday_successor_state_record"

DATASET_FAMILY: str = "microstructure_raw_aggtrades_v001"
DATASET_VERSION: str = "v002"
STAGE_MARKER: str = "stage2_raw_admissible"
SUCCESSOR_STATE: str = "stage2_raw_admissible"
SOURCE_PHASE_BOUNDARY: str = "Phase 4bl-D-R"

SYMBOL_LIST: tuple[str, ...] = ("BTCUSDT",)
DATE_START: str = "2024-12-01"
DATE_END: str = "2025-02-28"
DATE_COUNT: int = 90
EXPECTED_TOTAL_ROW_COUNT: int = 155_153_449
EXPECTED_TOTAL_SIZE_BYTES: int = 1_943_823_208

# ---------------------------------------------------------------------------
# Expected input artefact paths and SHAs (predeclared)
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_MICRO: Path = REPO_ROOT / "data" / "microstructure"
SUCCESSOR_STATE_DIR: Path = DATA_MICRO / "successor-state"

V002_MANIFEST_PATH: Path = (
    DATA_MICRO / "manifests" / "microstructure_raw_aggtrades_v001__v002.json"
)
V002_MANIFEST_SIDECAR_PATH: Path = V002_MANIFEST_PATH.with_suffix(
    V002_MANIFEST_PATH.suffix + ".sha256"
)
V002_ACQ_LOG_PATH: Path = (
    DATA_MICRO
    / "manifests"
    / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json"
)
V002_ACQ_LOG_SIDECAR_PATH: Path = V002_ACQ_LOG_PATH.with_suffix(
    V002_ACQ_LOG_PATH.suffix + ".sha256"
)
PHASE_4BL_D_R_REPORT_PATH: Path = (
    DATA_MICRO
    / "gate-reports"
    / "raw"
    / "microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json"
)
PHASE_4BL_D_R_REPORT_SIDECAR_PATH: Path = PHASE_4BL_D_R_REPORT_PATH.with_suffix(
    PHASE_4BL_D_R_REPORT_PATH.suffix + ".sha256"
)
PHASE_4BL_D_FAIL_REPORT_PATH: Path = (
    DATA_MICRO
    / "gate-reports"
    / "raw"
    / "microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json"
)
PHASE_4BL_D_S2_CANON_REPORT_PATH: Path = (
    DATA_MICRO
    / "canonicalization-reports"
    / "raw"
    / "microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__1778713761225__0d51bd7bac1e.json"
)
CANONICALIZED_2025_01_15_SIDECAR_PATH: Path = (
    DATA_MICRO
    / "raw"
    / "microstructure_raw_aggtrades_v001"
    / "BTCUSDT"
    / "2025"
    / "01"
    / "BTCUSDT-aggTrades-2025-01-15.zip.sha256"
)
RAW_2025_01_15_ZIP_PATH: Path = (
    DATA_MICRO
    / "raw"
    / "microstructure_raw_aggtrades_v001"
    / "BTCUSDT"
    / "2025"
    / "01"
    / "BTCUSDT-aggTrades-2025-01-15.zip"
)

EXPECTED_SHAS: dict[str, str] = {
    "v002_raw_manifest": (
        "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
    ),
    "v002_raw_manifest_sidecar": (
        "adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26"
    ),
    "v002_acquisition_log": (
        "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"
    ),
    "v002_acquisition_log_sidecar": (
        "975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958"
    ),
    "phase_4bl_d_r_report": (
        "f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"
    ),
    "phase_4bl_d_r_report_sidecar": (
        "84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02"
    ),
    "phase_4bl_d_fail_report": (
        "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7"
    ),
    "phase_4bl_d_s2_canon_report": (
        "8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3"
    ),
    "canonicalized_2025_01_15_sidecar": (
        "c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc"
    ),
    "raw_2025_01_15_zip": (
        "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
    ),
}

# ---------------------------------------------------------------------------
# Phase 4bl-D-R gate-result facts (predeclared by the authorization prompt)
# ---------------------------------------------------------------------------

PHASE_4BL_D_R_RESULT: dict[str, object] = {
    "phase": "Phase 4bl-D-R",
    "verdict": "RAW_MULTIDAY_GATE_PASS",
    "overall_status": "pass",
    "checks_total": 33,
    "checks_passed": 33,
    "checks_failed": 0,
    "checks_error": 0,
    "checks_not_applicable": 0,
    "full_per_row_validation_completed": True,
    "rows_validated": 155_153_449,
    "bytes_validated": 1_943_823_208,
    "all_dates_passed": True,
    "schema_validation_errors": 0,
    "timestamp_boundary_errors": 0,
    "duplicate_agg_trade_id_errors": 0,
    "monotonicity_errors": 0,
    "adjacent_date_overlap_errors": 0,
}


class SuccessorStateError(RuntimeError):
    """Raised when a precondition or postcondition fails."""


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------


def compute_file_sha256(path: Path, *, chunk_size: int = 1 << 20) -> str:
    """Return the SHA256 hex digest of *path*, read in chunks."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def serialize_successor_state(payload: Mapping[str, object]) -> bytes:
    """Serialise *payload* deterministically.

    Uses ``sort_keys=True``, ``indent=2``, ``ensure_ascii=False`` and
    **no trailing newline**, matching the Phase 4bb-G raw
    successor-state precedent verbatim. The encoded bytes are UTF-8.
    """
    return json.dumps(
        payload,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
    ).encode("utf-8")


def compose_canonical_sidecar_body(*, json_sha256_hex: str, json_basename: str) -> bytes:
    """Return the canonical Phase 4bb-F sidecar body bytes.

    Format: ``<sha>  <basename>\\n`` (lower-case 64-char hex; two
    spaces; trailing LF; no CRLF; no BOM).
    """
    if not isinstance(json_sha256_hex, str) or len(json_sha256_hex) != 64:
        raise SuccessorStateError("json_sha256_hex must be 64-char hex")
    if not all(c in "0123456789abcdef" for c in json_sha256_hex.lower()):
        raise SuccessorStateError("json_sha256_hex must be lower-case hex")
    if not isinstance(json_basename, str) or not json_basename:
        raise SuccessorStateError("json_basename must be a non-empty string")
    if "/" in json_basename or "\\" in json_basename:
        raise SuccessorStateError(
            f"json_basename must not contain path separators (got {json_basename!r})"
        )
    return f"{json_sha256_hex.lower()}  {json_basename}\n".encode()


def derive_short_commit(code_commit_sha: str, *, length: int = 12) -> str:
    """Return the leading *length* hex chars of *code_commit_sha*."""
    if not isinstance(code_commit_sha, str):
        raise SuccessorStateError("code_commit_sha must be a string")
    if length < 7:
        raise SuccessorStateError("length must be >= 7")
    if len(code_commit_sha) < length:
        raise SuccessorStateError(
            f"code_commit_sha must be >= {length} hex chars "
            f"(got {len(code_commit_sha)})"
        )
    short = code_commit_sha[:length].lower()
    if not all(c in "0123456789abcdef" for c in short):
        raise SuccessorStateError(f"code_commit_sha must be hex (got {short!r})")
    return short


# ---------------------------------------------------------------------------
# Atomic write helpers
# ---------------------------------------------------------------------------


def _resolve_parts(path: Path) -> tuple[str, ...]:
    try:
        return tuple(path.resolve(strict=False).parts)
    except OSError:
        return tuple(path.parts)


def _assert_path_under_successor_state(path: Path) -> None:
    parts = _resolve_parts(path)
    needle = ("data", "microstructure", "successor-state")
    if not any(
        parts[i : i + len(needle)] == needle
        for i in range(len(parts) - len(needle) + 1)
    ):
        raise SuccessorStateError(
            f"path must resolve under data/microstructure/successor-state/ "
            f"(got {path})"
        )


def _atomic_write_bytes(*, target: Path, body: bytes, refuse_overwrite: bool = True) -> None:
    """Write *body* to *target* atomically, refusing overwrite unless byte-identical."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        existing = target.read_bytes()
        if existing == body:
            # Idempotent no-op: byte-identical re-write is allowed.
            return
        if refuse_overwrite:
            raise SuccessorStateError(
                f"refusing to overwrite existing non-identical file: {target}"
            )
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(body)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        os.replace(tmp_path, target)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()


# ---------------------------------------------------------------------------
# Precondition checks
# ---------------------------------------------------------------------------


def _verify_sha(path: Path, expected_key: str, *, expected_shas: Mapping[str, str]) -> str:
    """Recompute SHA256 of *path* and verify it matches expected_shas[expected_key]."""
    if not path.exists():
        raise SuccessorStateError(f"required input missing: {path}")
    actual = compute_file_sha256(path)
    expected = expected_shas[expected_key]
    if actual != expected:
        raise SuccessorStateError(
            f"SHA mismatch for {expected_key} ({path}): "
            f"expected {expected}, got {actual}"
        )
    return actual


def _verify_manifest_state(path: Path) -> dict[str, object]:
    """Return the v002 manifest dict and verify research_eligible / gate status."""
    with path.open("rb") as fh:
        manifest = json.load(fh)
    if not isinstance(manifest, dict):
        raise SuccessorStateError("v002 manifest must be a JSON object")
    if manifest.get("research_eligible") is not False:
        raise SuccessorStateError(
            f"v002 manifest research_eligible must be False "
            f"(got {manifest.get('research_eligible')!r})"
        )
    if manifest.get("eligibility_gate_status") != "pending":
        raise SuccessorStateError(
            f"v002 manifest eligibility_gate_status must be 'pending' "
            f"(got {manifest.get('eligibility_gate_status')!r})"
        )
    if manifest.get("date_count") != DATE_COUNT:
        raise SuccessorStateError(
            f"v002 manifest date_count must be {DATE_COUNT} "
            f"(got {manifest.get('date_count')!r})"
        )
    if manifest.get("total_row_count") != EXPECTED_TOTAL_ROW_COUNT:
        raise SuccessorStateError(
            f"v002 manifest total_row_count must be {EXPECTED_TOTAL_ROW_COUNT} "
            f"(got {manifest.get('total_row_count')!r})"
        )
    if manifest.get("total_size_bytes") != EXPECTED_TOTAL_SIZE_BYTES:
        raise SuccessorStateError(
            f"v002 manifest total_size_bytes must be {EXPECTED_TOTAL_SIZE_BYTES} "
            f"(got {manifest.get('total_size_bytes')!r})"
        )
    return manifest


def _verify_gate_report_pass(path: Path) -> dict[str, object]:
    """Return the Phase 4bl-D-R gate report dict and verify it is a PASS."""
    with path.open("rb") as fh:
        report = json.load(fh)
    if not isinstance(report, dict):
        raise SuccessorStateError("Phase 4bl-D-R gate report must be a JSON object")
    if report.get("overall_status") != "pass":
        raise SuccessorStateError(
            f"Phase 4bl-D-R gate report overall_status must be 'pass' "
            f"(got {report.get('overall_status')!r})"
        )
    verdict = report.get("gate_verdict") or report.get("verdict")
    if verdict != "RAW_MULTIDAY_GATE_PASS":
        raise SuccessorStateError(
            f"Phase 4bl-D-R gate verdict must be 'RAW_MULTIDAY_GATE_PASS' "
            f"(got {verdict!r})"
        )
    return report


# ---------------------------------------------------------------------------
# Payload builder
# ---------------------------------------------------------------------------


def build_successor_state_payload(
    *,
    expected_shas: Mapping[str, str],
    base_commit_sha: str,
    code_commit_sha: str,
    created_at_unix_ms: int,
    created_at_utc: str,
    successor_state_basename: str,
    sidecar_basename: str,
    script_path: str,
    python_version: str,
    platform_summary: str,
) -> dict[str, object]:
    """Build the deterministic Phase 4bl-E successor-state payload."""
    return {
        "$schema_note": "Phase 4bl-E v002 multi-day raw successor-state record",
        "schema_version": SCHEMA_VERSION,
        "phase": PHASE_NAME,
        "phase_id": PHASE_ID.upper(),
        "phase_name": "Multi-Day Raw Manifest Successor-State Recording",
        "artefact_type": ARTEFACT_TYPE,
        "successor_state": SUCCESSOR_STATE,
        "successor_state_status": "recorded",
        "successor_state_family": DATASET_FAMILY,
        "successor_state_version": DATASET_VERSION,
        "successor_state_kind": "raw_family_v002_stage2_admissibility_marker",
        "successor_state_type": "raw_family_v002_successor_state_record",
        "successor_admissibility_status": "admissible_in_principle_policy_level_only",
        "successor_admissibility_kind": (
            "raw_family_v002_structural_integrity_admissibility_only"
        ),
        "successor_raw_use_admissible": True,
        "successor_research_use_admissible": "conditional_future_only",
        "successor_ml_use_admissible": False,
        "successor_stage": "raw_family_v002_successor_state_recorded",
        "successor_stage_ladder_position": (
            "Phase 4ba 5-stage ladder: Stage-2 gate-passed at report level "
            "(Phase 4bl-D-R PASS). Raw-family research_eligible MUST remain "
            "false permanently on the original manifest. Stage-3 "
            "(research-eligible) is unreachable for the raw family by "
            "design; Stage-3 applies only to derived families."
        ),
        "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
        "source_phase_boundary_id": "4bl-D-R",
        # Dataset scope (locked).
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "source_dataset_family": DATASET_FAMILY,
        "source_dataset_version": DATASET_VERSION,
        "symbol_list": list(SYMBOL_LIST),
        "date_start": DATE_START,
        "date_end": DATE_END,
        "date_count": DATE_COUNT,
        "total_row_count": EXPECTED_TOTAL_ROW_COUNT,
        "total_size_bytes": EXPECTED_TOTAL_SIZE_BYTES,
        "source_class": (
            "binance_usdm_futures_public_daily_aggtrades_archive"
        ),
        # Source artefacts (v002 manifest + acquisition log + sidecars).
        "v002_manifest_path": str(V002_MANIFEST_PATH.as_posix()),
        "v002_manifest_sha256": expected_shas["v002_raw_manifest"],
        "v002_manifest_sidecar_path": str(V002_MANIFEST_SIDECAR_PATH.as_posix()),
        "v002_manifest_sidecar_sha256": expected_shas["v002_raw_manifest_sidecar"],
        "v002_acquisition_log_path": str(V002_ACQ_LOG_PATH.as_posix()),
        "v002_acquisition_log_sha256": expected_shas["v002_acquisition_log"],
        "v002_acquisition_log_sidecar_path": str(V002_ACQ_LOG_SIDECAR_PATH.as_posix()),
        "v002_acquisition_log_sidecar_sha256": expected_shas[
            "v002_acquisition_log_sidecar"
        ],
        # Phase 4bl-D-R PASS gate report (latest gate evidence).
        "latest_gate_phase": "Phase 4bl-D-R",
        "latest_gate_verdict": "RAW_MULTIDAY_GATE_PASS",
        "latest_gate_overall_status": "pass",
        "latest_gate_checks_total": 33,
        "latest_gate_checks_passed": 33,
        "latest_gate_checks_failed": 0,
        "latest_gate_checks_error": 0,
        "latest_gate_checks_not_applicable": 0,
        "full_per_row_validation_completed": True,
        "rows_validated": EXPECTED_TOTAL_ROW_COUNT,
        "bytes_validated": EXPECTED_TOTAL_SIZE_BYTES,
        "all_dates_passed": True,
        "schema_validation_errors": 0,
        "timestamp_boundary_errors": 0,
        "duplicate_agg_trade_id_errors": 0,
        "monotonicity_errors": 0,
        "adjacent_date_overlap_errors": 0,
        "phase_4bl_d_r_gate_report_path": str(PHASE_4BL_D_R_REPORT_PATH.as_posix()),
        "phase_4bl_d_r_gate_report_sha256": expected_shas["phase_4bl_d_r_report"],
        "phase_4bl_d_r_gate_report_sidecar_path": str(
            PHASE_4BL_D_R_REPORT_SIDECAR_PATH.as_posix()
        ),
        "phase_4bl_d_r_gate_report_sidecar_sha256": expected_shas[
            "phase_4bl_d_r_report_sidecar"
        ],
        # Predecessor FAIL lineage (Phase 4bl-D).
        "predecessor_failed_gate_phase": "Phase 4bl-D",
        "predecessor_failed_gate_verdict": "RAW_MULTIDAY_GATE_FAIL",
        "predecessor_failed_gate_report_path": str(
            PHASE_4BL_D_FAIL_REPORT_PATH.as_posix()
        ),
        "predecessor_failed_gate_report_sha256": expected_shas[
            "phase_4bl_d_fail_report"
        ],
        "predecessor_failed_gate_summary": (
            "Phase 4bl-D produced RAW_MULTIDAY_GATE_FAIL (29 PASS / 4 FAIL / "
            "0 ERROR / 0 NA out of 33 total). Root cause: the pre-existing "
            "Phase 4az 2025-01-15 sidecar used Windows CRLF (100 bytes) "
            "instead of the canonical Phase 4bb-F LF terminator. All 89 "
            "Phase 4bl-C newly-acquired sidecars were already canonical LF. "
            "The 2025-01-15 raw zip was byte-identical to the Phase 4az "
            "fixture; the data was not corrupt. Only the sidecar's line "
            "terminator differed from canonical Phase 4bb-F. The Phase "
            "4bl-D gate report is preserved as historical evidence and is "
            "byte-identical to its recorded SHA."
        ),
        # Remediation lineage (Phase 4bl-D-S1 governance + Phase 4bl-D-S2 execution).
        "remediation_governance_phase": "Phase 4bl-D-S1",
        "remediation_execution_phase": "Phase 4bl-D-S2",
        "remediation_type": "metadata_sidecar_line_ending_canonicalization",
        "remediation_governance_memo_path": (
            "docs/00-meta/implementation-reports/"
            "2026-05-13_phase-4bl-d-s1_sidecar-canonicalization-governance-memo.md"
        ),
        "remediation_execution_memo_path": (
            "docs/00-meta/implementation-reports/"
            "2026-05-13_phase-4bl-d-s2_controlled-sidecar-canonicalization-execution.md"
        ),
        "remediation_report_path": str(PHASE_4BL_D_S2_CANON_REPORT_PATH.as_posix()),
        "remediation_report_sha256": expected_shas["phase_4bl_d_s2_canon_report"],
        "canonicalized_sidecar_path": str(
            CANONICALIZED_2025_01_15_SIDECAR_PATH.as_posix()
        ),
        "canonicalized_sidecar_sha256": expected_shas[
            "canonicalized_2025_01_15_sidecar"
        ],
        "target_raw_zip_path": str(RAW_2025_01_15_ZIP_PATH.as_posix()),
        "target_raw_zip_sha256": expected_shas["raw_2025_01_15_zip"],
        "remediation_summary": (
            "Phase 4bl-D-S2 atomically rewrote the single Phase 4az "
            "2025-01-15 sidecar from CRLF (100 bytes) to canonical "
            "Phase 4bb-F LF (99 bytes), preserving the embedded SHA value "
            "and basename byte-identically. The target raw zip and all "
            "other upstream artefacts were byte-identical pre/post. The "
            "Phase 4bl-D-S2 canonicalisation report is preserved as "
            "historical evidence and is byte-identical to its recorded "
            "SHA."
        ),
        # Lineage chain (predecessor / remediation / current).
        "lineage_chain": [
            "Phase 4bl-A (multi-day expansion requirements memo)",
            "Phase 4bl-B (multi-day acquisition authorization / design memo)",
            "Phase 4bl-C (multi-day aggTrades acquisition execution)",
            "Phase 4bl-D (multi-day raw eligibility gate; FAIL)",
            "Phase 4bl-D-S1 (sidecar canonicalization governance memo)",
            "Phase 4bl-D-S2 (controlled sidecar canonicalization execution)",
            "Phase 4bl-D-R (multi-day raw eligibility gate rerun; PASS)",
            "Phase 4bl-E (this multi-day raw successor-state record)",
        ],
        # Manifest state preservation (binding).
        "manifest_mutated": False,
        "manifest_transition_performed": False,
        "research_eligible_before": False,
        "research_eligible_after": False,
        "eligibility_gate_status_before": "pending",
        "eligibility_gate_status_after": "pending",
        "eligibility_gate_status_transition_performed": False,
        "chronological_split_policy_changed": False,
        "report_level_gate_status": "pass_report_level_only",
        "successor_state_record_is_sibling_artefact": True,
        "original_v002_manifest_mutated": False,
        "original_v002_manifest_must_remain_byte_identical": True,
        "original_v002_acquisition_log_mutated": False,
        "original_v002_acquisition_log_must_remain_byte_identical": True,
        "original_phase_4bl_d_r_gate_report_mutated": False,
        "original_phase_4bl_d_r_gate_report_must_remain_byte_identical": True,
        "original_phase_4bl_d_fail_report_mutated": False,
        "original_phase_4bl_d_fail_report_must_remain_byte_identical": True,
        "original_phase_4bl_d_s2_canon_report_mutated": False,
        "original_phase_4bl_d_s2_canon_report_must_remain_byte_identical": True,
        "original_canonicalized_sidecar_mutated": False,
        "original_canonicalized_sidecar_must_remain_byte_identical": True,
        "original_raw_zip_mutated": False,
        "original_raw_zip_must_remain_byte_identical": True,
        "manifest_mutation_permitted": False,
        # Admissibility statement.
        "raw_family_stage": SUCCESSOR_STATE,
        "raw_family_admissible_for_next_pipeline_stage": True,
        "next_pipeline_stage_name": "multi_day_normalization_derived_arc",
        "next_pipeline_stage_authorized": False,
        "admissibility_explanation": (
            "This successor-state records that the v002 raw multi-day "
            "BTCUSDT aggTrades dataset passed the raw eligibility gate at "
            "report level (Phase 4bl-D-R: RAW_MULTIDAY_GATE_PASS, 33 / 33 "
            "PASS, full per-row validation across 155,153,449 rows / "
            "1,943,823,208 bytes / 90 / 90 dates). It does not mutate the "
            "v002 manifest, does not flip research_eligible, does not "
            "transition eligibility_gate_status on the actual manifest, "
            "and does not authorize any downstream pipeline stage."
        ),
        # Governance labels.
        "governance_labels": {
            "phase": PHASE_ID,
            "source_phase_boundary": "4bl-D-R",
            "dataset_family": DATASET_FAMILY,
            "dataset_version": DATASET_VERSION,
            "stage": "raw_successor_state",
            "feature_computation": "forbidden",
            "labels": "forbidden",
            "diagnostics": "forbidden",
            "ml": "forbidden",
            "strategy": "forbidden",
            "backtest": "forbidden",
            "strategy_use": "forbidden",
            "stop_trigger_domain": "trade_price_backtest_candidate",
        },
        # Non-authorizations (exhaustive).
        "non_authorizations": {
            "phase_4bm_authorized": False,
            "phase_4bm_a_authorized": False,
            "phase_4bn_authorized": False,
            "phase_4bo_authorized": False,
            "phase_4bp_authorized": False,
            "phase_4bq_authorized": False,
            "phase_5_authorized": False,
            "phase_4_canonical_authorized": False,
            "acquisition_authorized": False,
            "additional_downloads_authorized": False,
            "normalization_authorized": False,
            "derived_generation_authorized": False,
            "feature_generation_authorized": False,
            "label_generation_authorized": False,
            "diagnostics_authorized": False,
            "label_statistics_authorized": False,
            "split_authorized": False,
            "ml_authorized": False,
            "strategy_authorized": False,
            "signal_authorized": False,
            "backtest_authorized": False,
            "paper_shadow_authorized": False,
            "live_authorized": False,
            "live_readiness_authorized": False,
            "deployment_authorized": False,
            "exchange_write_authorized": False,
            "production_keys_authorized": False,
            "authenticated_apis_authorized": False,
            "private_endpoints_authorized": False,
            "public_endpoint_calls_authorized": False,
            "user_stream_authorized": False,
            "websocket_authorized": False,
            "mcp_authorized": False,
            "graphify_authorized": False,
            "credentials_authorized": False,
            "manifest_research_eligible_flip_authorized": False,
            "manifest_eligibility_gate_status_transition_authorized": False,
            "chronological_split_policy_change_authorized": False,
            "successor_authorizes_next_phase": False,
        },
        # Boundary confirmations (every claim a downstream reader needs).
        "boundary_confirmations": {
            "no_v002_manifest_mutation": True,
            "no_v002_acquisition_log_mutation": True,
            "no_phase_4bl_d_r_gate_report_mutation": True,
            "no_phase_4bl_d_fail_report_mutation": True,
            "no_phase_4bl_d_s2_canon_report_mutation": True,
            "no_canonicalized_sidecar_mutation": True,
            "no_raw_zip_mutation": True,
            "no_other_sidecar_mutation": True,
            "no_research_eligible_manifest_flip": True,
            "no_eligibility_gate_status_manifest_transition": True,
            "no_chronological_split_policy_change": True,
            "no_gate_rerun": True,
            "no_new_gate_report_created": True,
            "no_data_acquisition": True,
            "no_additional_downloads": True,
            "no_normalization": True,
            "no_derived_parquet_created": True,
            "no_feature_parquet_created": True,
            "no_feature_manifest_created": True,
            "no_label_parquet_created": True,
            "no_label_manifest_created": True,
            "no_diagnostics_run": True,
            "no_label_statistics_computed": True,
            "no_split_artefact_created": True,
            "no_signal_computed": True,
            "no_ml_training": True,
            "no_ml_architecture_design": True,
            "no_feature_ranking": True,
            "no_meta_labeling": True,
            "no_strategy_creation": True,
            "no_backtest": True,
            "no_strategy_output_metrics": True,
            "no_data_microstructure_artefact_committed": True,
            "no_data_microstructure_write_outside_successor_state_namespace": True,
            "no_public_endpoint_use": True,
            "no_binance_api_use": True,
            "no_data_binance_vision_use": True,
            "no_fapi_binance_com_use": True,
            "no_api_binance_com_use": True,
            "no_authenticated_api_use": True,
            "no_private_endpoint_use": True,
            "no_user_stream_use": True,
            "no_websocket": True,
            "no_listenkey_lifecycle": True,
            "no_credentials": True,
            "no_env": True,
            "no_mcp_or_graphify": True,
            "no_mcp_json": True,
            "no_existing_gate_report_migration": True,
            "no_existing_successor_state_migration": True,
            "no_phase_4bb_f_amendment": True,
            "no_phase_4bl_d_gate_amendment": True,
            "no_check_weakening": True,
            "no_sidecar_parser_relaxation": True,
            "no_retained_verdict_revision": True,
            "no_project_lock_change": True,
            "no_m0_amendment": True,
            "no_successor_authorization": True,
            "phase_4aw_flip_research_eligible_invariant_preserved": True,
        },
        # Retained verdict ledger (verbatim).
        "retained_verdict_ledger": {
            "H0": "FRAMEWORK ANCHOR",
            "R3": "BASELINE-OF-RECORD",
            "R1a": "RETAINED - NON-LEADING",
            "R1b_narrow": "RETAINED - NON-LEADING",
            "R2": "FAILED - section_11_6",
            "F1": "HARD REJECT",
            "D1_A": "MECHANISM PASS / FRAMEWORK FAIL",
            "five_minute_thread": "OPERATIONALLY CLOSED (Phase 3t)",
            "V2": "HARD REJECT - terminal for V2 first-spec",
            "G1": "HARD REJECT - terminal for G1 first-spec",
            "C1": "HARD REJECT - terminal for C1 first-spec",
        },
        # Preserved project locks (verbatim).
        "preserved_project_locks": [
            "section_11_6 = 8 bps per side",
            "round-trip = 16 bps",
            (
                "section_1_7_3 = 0.25% risk / 2x leverage / one-position / "
                "mark-price stops"
            ),
            (
                "Phase 3p section_4_7 strict integrity gate "
                "(multi-day extension applied by Phase 4bl-D; rerun by Phase 4bl-D-R)"
            ),
            "Phase 3r section_8 mark-price gap governance",
            "Phase 3v section_8 stop-trigger-domain governance",
            (
                "Phase 3w section_6 / section_7 / section_8 break-even / "
                "EMA slope / stagnation governance"
            ),
            "Phase 4j section_11 metrics OI-subset partial-eligibility rule",
            "Phase 4k V2 backtest-plan methodology",
            "Phase 4p G1 strategy-spec memo",
            "Phase 4q G1 backtest-plan methodology",
            "Phase 4v C1 strategy-spec memo",
            "Phase 4w C1 backtest-plan methodology",
            (
                "Phase 4ak M0 twelve-clause gate + post-null cooldown + "
                "cooled-down families list + memo template"
            ),
            (
                "Phase 4al refined no-rescue rule + section_13 boundary + "
                "section_14 hierarchy"
            ),
            (
                "Phase 4aw MicrostructureManifest.flip_research_eligible(...) "
                "always-raises invariant"
            ),
            "Phase 4bb-F canonical path policy (prospective only)",
            (
                "Phase 4bb-G raw v001 successor-state precedent "
                "(preserved verbatim; not migrated)"
            ),
            (
                "Phase 4bl-D 33-check raw eligibility-gate protocol "
                "(rerun verbatim; no check weakened)"
            ),
            "Phase 4bl-D RAW_MULTIDAY_GATE_FAIL preserved as historical evidence",
            "Phase 4bl-D-S2 sidecar canonicalisation outcome preserved verbatim",
        ],
        # No-rescue statement (verbatim).
        "no_rescue_statement": (
            "Phase 4bl-E is a multi-day v002 raw-family successor-state "
            "policy marker ONLY. It does NOT reopen any cooled-down family "
            "(R2, F1, D1-A, V2, G1, C1, the 5m thread), does NOT authorize "
            "any strategy hypothesis, does NOT authorize any ML or "
            "label-evaluation phase, does NOT authorize Phase 4 canonical, "
            "Phase 5, paper / shadow, live-readiness, exchange-write, "
            "deployment, or production-key creation, and does NOT license "
            "any rescue interpretation of the cumulative six-candidate "
            "rejection topology. The Phase 4ak M0 twelve-clause gate, "
            "post-null cooldown rule, cooled-down families list, and "
            "Phase 4al refined no-rescue rule remain binding."
        ),
        "phase_4aw_invariant": (
            "MicrostructureManifest.flip_research_eligible(...) "
            "always-raises invariant preserved (never invoked by "
            "Phase 4bl-E)."
        ),
        # Successor-state file metadata.
        "successor_state_path": str(
            (SUCCESSOR_STATE_DIR / successor_state_basename).as_posix()
        ),
        "successor_state_sidecar_path": str(
            (SUCCESSOR_STATE_DIR / sidecar_basename).as_posix()
        ),
        "successor_state_basename": successor_state_basename,
        "successor_state_sidecar_basename": sidecar_basename,
        "successor_state_must_not_be_treated_as_research_eligible_flip": True,
        # Execution metadata.
        "created_at_unix_ms": created_at_unix_ms,
        "created_at_utc": created_at_utc,
        "base_commit_sha": base_commit_sha,
        "code_commit_sha": code_commit_sha,
        "script_path": script_path,
        "python_version": python_version,
        "platform_summary": platform_summary,
        "writer_module": "scripts.phase4bl_e_record_multiday_raw_successor_state",
        "recommended_state": "remain_paused",
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def _git_rev_parse_head() -> str | None:
    """Return the current git HEAD SHA, or None if git is unavailable."""
    try:
        out = subprocess.run(  # noqa: S603 - intentional local-only invocation
            ["git", "rev-parse", "HEAD"],  # noqa: S607 - PATH-resolved git is acceptable
            cwd=str(REPO_ROOT),
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None
    return out.stdout.strip() or None


def _git_rev_parse_main() -> str | None:
    """Return the current `main` ref SHA, or None if git is unavailable."""
    try:
        out = subprocess.run(  # noqa: S603
            ["git", "rev-parse", "main"],  # noqa: S607
            cwd=str(REPO_ROOT),
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None
    return out.stdout.strip() or None


def run(*, expected_shas: Mapping[str, str] | None = None) -> int:
    """Execute the Phase 4bl-E successor-state recording exactly once."""
    shas = dict(expected_shas) if expected_shas is not None else dict(EXPECTED_SHAS)

    print(f"[{PHASE_NAME}] Verifying eight upstream input SHAs...")
    _verify_sha(V002_MANIFEST_PATH, "v002_raw_manifest", expected_shas=shas)
    _verify_sha(V002_MANIFEST_SIDECAR_PATH, "v002_raw_manifest_sidecar", expected_shas=shas)
    _verify_sha(V002_ACQ_LOG_PATH, "v002_acquisition_log", expected_shas=shas)
    _verify_sha(V002_ACQ_LOG_SIDECAR_PATH, "v002_acquisition_log_sidecar", expected_shas=shas)
    _verify_sha(PHASE_4BL_D_R_REPORT_PATH, "phase_4bl_d_r_report", expected_shas=shas)
    _verify_sha(
        PHASE_4BL_D_R_REPORT_SIDECAR_PATH,
        "phase_4bl_d_r_report_sidecar",
        expected_shas=shas,
    )
    _verify_sha(PHASE_4BL_D_FAIL_REPORT_PATH, "phase_4bl_d_fail_report", expected_shas=shas)
    _verify_sha(
        PHASE_4BL_D_S2_CANON_REPORT_PATH,
        "phase_4bl_d_s2_canon_report",
        expected_shas=shas,
    )
    _verify_sha(
        CANONICALIZED_2025_01_15_SIDECAR_PATH,
        "canonicalized_2025_01_15_sidecar",
        expected_shas=shas,
    )
    _verify_sha(RAW_2025_01_15_ZIP_PATH, "raw_2025_01_15_zip", expected_shas=shas)
    print(f"[{PHASE_NAME}] All ten input SHAs verified.")

    print(f"[{PHASE_NAME}] Verifying v002 manifest state...")
    _verify_manifest_state(V002_MANIFEST_PATH)
    print(
        f"[{PHASE_NAME}] v002 manifest: research_eligible=false, "
        f"eligibility_gate_status=pending (unchanged)."
    )

    print(f"[{PHASE_NAME}] Verifying Phase 4bl-D-R PASS verdict...")
    _verify_gate_report_pass(PHASE_4BL_D_R_REPORT_PATH)
    print(f"[{PHASE_NAME}] Phase 4bl-D-R gate report: RAW_MULTIDAY_GATE_PASS.")

    # Derive output filenames per Phase 4bb-F canonical successor-state pattern.
    successor_state_basename = (
        f"{DATASET_FAMILY}__{DATASET_VERSION}__{STAGE_MARKER}__phase-{PHASE_ID}.json"
    )
    sidecar_basename = f"{successor_state_basename}.sha256"
    successor_state_path = SUCCESSOR_STATE_DIR / successor_state_basename
    sidecar_path = SUCCESSOR_STATE_DIR / sidecar_basename
    _assert_path_under_successor_state(successor_state_path)
    _assert_path_under_successor_state(sidecar_path)

    # Build payload.
    now = datetime.now(UTC)
    created_at_unix_ms = int(now.timestamp() * 1000)
    created_at_utc = now.isoformat()
    base_commit_sha = _git_rev_parse_main() or ""
    code_commit_sha = _git_rev_parse_head() or base_commit_sha

    payload = build_successor_state_payload(
        expected_shas=shas,
        base_commit_sha=base_commit_sha,
        code_commit_sha=code_commit_sha,
        created_at_unix_ms=created_at_unix_ms,
        created_at_utc=created_at_utc,
        successor_state_basename=successor_state_basename,
        sidecar_basename=sidecar_basename,
        script_path="scripts/phase4bl_e_record_multiday_raw_successor_state.py",
        python_version=sys.version.split()[0],
        platform_summary=f"{platform.system()}-{platform.release()}",
    )

    body = serialize_successor_state(payload)
    json_sha256 = hashlib.sha256(body).hexdigest()

    print(f"[{PHASE_NAME}] Writing successor-state JSON ({len(body)} bytes)...")
    _atomic_write_bytes(target=successor_state_path, body=body, refuse_overwrite=True)

    sidecar_body = compose_canonical_sidecar_body(
        json_sha256_hex=json_sha256,
        json_basename=successor_state_basename,
    )
    print(f"[{PHASE_NAME}] Writing paired SHA256 sidecar ({len(sidecar_body)} bytes)...")
    _atomic_write_bytes(target=sidecar_path, body=sidecar_body, refuse_overwrite=True)

    # Postcondition: recompute on-disk SHAs and confirm they match.
    on_disk_json_sha = compute_file_sha256(successor_state_path)
    on_disk_sidecar_sha = compute_file_sha256(sidecar_path)
    if on_disk_json_sha != json_sha256:
        raise SuccessorStateError(
            f"post-write JSON SHA mismatch: expected {json_sha256}, "
            f"got {on_disk_json_sha}"
        )
    sidecar_parsed = sidecar_path.read_bytes().decode("utf-8")
    expected_sidecar_line = f"{json_sha256}  {successor_state_basename}\n"
    if sidecar_parsed != expected_sidecar_line:
        raise SuccessorStateError(
            f"post-write sidecar body mismatch: expected {expected_sidecar_line!r}, "
            f"got {sidecar_parsed!r}"
        )

    # Postcondition: recompute upstream input SHAs (immutability proof).
    print(f"[{PHASE_NAME}] Verifying upstream artefact immutability post-write...")
    _verify_sha(V002_MANIFEST_PATH, "v002_raw_manifest", expected_shas=shas)
    _verify_sha(V002_ACQ_LOG_PATH, "v002_acquisition_log", expected_shas=shas)
    _verify_sha(PHASE_4BL_D_R_REPORT_PATH, "phase_4bl_d_r_report", expected_shas=shas)
    _verify_sha(PHASE_4BL_D_FAIL_REPORT_PATH, "phase_4bl_d_fail_report", expected_shas=shas)
    _verify_sha(
        PHASE_4BL_D_S2_CANON_REPORT_PATH,
        "phase_4bl_d_s2_canon_report",
        expected_shas=shas,
    )
    _verify_sha(
        CANONICALIZED_2025_01_15_SIDECAR_PATH,
        "canonicalized_2025_01_15_sidecar",
        expected_shas=shas,
    )
    _verify_sha(RAW_2025_01_15_ZIP_PATH, "raw_2025_01_15_zip", expected_shas=shas)
    print(f"[{PHASE_NAME}] All upstream artefacts byte-identical pre/post.")

    print()
    print(f"[{PHASE_NAME}] SUCCESSOR_STATE_RECORDED")
    print(f"  JSON path:       {successor_state_path.as_posix()}")
    print(f"  JSON size:       {len(body)} bytes")
    print(f"  JSON SHA256:     {json_sha256}")
    print(f"  Sidecar path:    {sidecar_path.as_posix()}")
    print(f"  Sidecar size:    {len(sidecar_body)} bytes")
    print(f"  Sidecar SHA256:  {on_disk_sidecar_sha}")
    print(f"  base_commit_sha: {base_commit_sha}")
    print(f"  code_commit_sha: {code_commit_sha}")
    print(f"  created_at_utc:  {created_at_utc}")
    print()
    print(f"[{PHASE_NAME}] No manifest mutated. No gate rerun. No data acquired.")
    print(f"[{PHASE_NAME}] Phase 4bm-A / Phase 5 / any successor remain UNAUTHORIZED.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Record the Phase 4bl-E v002 multi-day raw successor-state "
            "artefact under data/microstructure/successor-state/."
        )
    )
    parser.parse_args(argv)
    return run()


if __name__ == "__main__":  # pragma: no cover - script entrypoint
    sys.exit(main())
