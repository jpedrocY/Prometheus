"""Phase 4bl-D-S2 — Controlled Sidecar Canonicalization Execution.

This standalone script performs exactly one operation: it normalizes
the line terminator of one hard-coded raw zip sidecar from Windows
CRLF (`\\r\\n`) to canonical Phase 4bb-F LF (`\\n`).

It is the executor of the Phase 4bl-D-S1 governance memo's Option B1
recommendation. It is metadata canonicalization, not market-data
mutation.

Strict guarantees:

- The script imports only Python standard library modules.
- The script performs zero network I/O.
- The script reads zero credentials, no `.env`, no `.mcp.json`.
- The script does not invoke MCP, Graphify, or any external tool.
- The script verifies every predeclared precondition before any
  mutation, and fails closed if any precondition differs.
- The script rewrites exactly one file (the target sidecar) via an
  atomic write-then-rename.
- The script verifies every predeclared postcondition after the
  mutation, including the byte-identical preservation of every
  upstream artefact (raw zip, v002 manifest, v002 acquisition log,
  Phase 4bl-D gate report).
- The script writes one deterministic canonicalization report JSON
  under the gitignored `data/microstructure/canonicalization-reports/`
  namespace, plus one paired `.sha256` sidecar in canonical
  Phase 4bb-F format.
- The script refuses to write any file path other than the target
  sidecar, the canonicalization report, and the report's sidecar.
- The script never runs the Phase 4bl-D gate.
- The script never modifies the raw zip, v002 manifest, v002
  acquisition log, Phase 4bl-D gate report, any other sidecar, or
  any other artefact under `data/microstructure/`.
- The script never authorizes any successor phase.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import platform
import sys
import tempfile
import time
from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Locked Phase 4bl-D-S2 constants (binding; do not edit without separately
# authorized phase).
# ---------------------------------------------------------------------------

SCHEMA_VERSION: Final[str] = "v001"
PHASE: Final[str] = "Phase 4bl-D-S2"
PHASE_ID: Final[str] = "4bl-D-S2"
ARTEFACT_TYPE: Final[str] = "sidecar_canonicalization_report"
DATASET_FAMILY: Final[str] = "microstructure_raw_aggtrades_v001"
DATASET_VERSION: Final[str] = "v002"
MUTATION_TYPE: Final[str] = "metadata_sidecar_line_ending_canonicalization"

TARGET_SYMBOL: Final[str] = "BTCUSDT"
TARGET_UTC_DATE: Final[str] = "2025-01-15"

# Path constants are written using forward slashes for cross-platform
# portability. Path() converts them as needed.
TARGET_SIDECAR_REL: Final[str] = (
    "data/microstructure/raw/microstructure_raw_aggtrades_v001/"
    "BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
)
TARGET_ZIP_REL: Final[str] = (
    "data/microstructure/raw/microstructure_raw_aggtrades_v001/"
    "BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
)
V002_MANIFEST_REL: Final[str] = (
    "data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json"
)
V002_ACQ_LOG_REL: Final[str] = (
    "data/microstructure/manifests/"
    "microstructure_raw_aggtrades_v001__v002_acquisition_log.json"
)
PHASE_4BL_D_GATE_REPORT_REL: Final[str] = (
    "data/microstructure/gate-reports/raw/"
    "microstructure_raw_aggtrades_v001__v002__phase-4bl-d__"
    "1778627360966__2576a004c18a.json"
)

EXPECTED_ZIP_SHA: Final[str] = (
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
)
EXPECTED_ZIP_SIZE: Final[int] = 21_271_119
EXPECTED_TARGET_BASENAME: Final[str] = "BTCUSDT-aggTrades-2025-01-15.zip"
EXPECTED_V002_MANIFEST_SHA: Final[str] = (
    "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"
)
EXPECTED_V002_ACQ_LOG_SHA: Final[str] = (
    "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"
)
EXPECTED_PHASE_4BL_D_GATE_REPORT_SHA: Final[str] = (
    "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7"
)

EXPECTED_PRE_SIDECAR_SIZE: Final[int] = 100
EXPECTED_POST_SIDECAR_SIZE: Final[int] = 99

CANONICALIZATION_REPORTS_ROOT_REL: Final[str] = (
    "data/microstructure/canonicalization-reports/raw"
)

# Sidecar body construction:
#   <hex_sha>  <basename>\n   (two spaces; one trailing LF).
TWO_SPACES: Final[str] = "  "
LF: Final[bytes] = b"\n"
CRLF: Final[bytes] = b"\r\n"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class CanonicalizationPreconditionError(RuntimeError):
    """A predeclared precondition did not hold; abort before any mutation."""


class CanonicalizationPostconditionError(RuntimeError):
    """A predeclared postcondition did not hold; abort and report."""


class CanonicalizationPathRefusedError(RuntimeError):
    """The script refuses to write to the requested path."""


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------


def compute_sha256(path: Path) -> str:
    """Compute SHA256 of the file at *path* using chunked reads."""
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def parse_canonical_sidecar_body(body_bytes: bytes) -> tuple[str, str, str]:
    """Parse a canonical Phase 4bb-F sidecar body.

    Returns ``(embedded_sha_hex, embedded_basename, line_ending_label)``
    where ``line_ending_label`` is one of ``"CRLF"`` or ``"LF"``.

    Raises ``CanonicalizationPreconditionError`` if the body is not a
    well-formed sidecar (must have hex SHA, two spaces, basename, and a
    trailing newline).
    """
    if body_bytes.endswith(CRLF):
        line_ending = "CRLF"
        without_terminator = body_bytes[: -len(CRLF)]
    elif body_bytes.endswith(LF):
        line_ending = "LF"
        without_terminator = body_bytes[: -len(LF)]
    else:
        raise CanonicalizationPreconditionError(
            "sidecar body does not end with CRLF or LF"
        )
    try:
        decoded = without_terminator.decode("ascii")
    except UnicodeDecodeError as exc:
        raise CanonicalizationPreconditionError(
            "sidecar body is not ASCII"
        ) from exc
    parts = decoded.split(TWO_SPACES, 1)
    if len(parts) != 2:
        raise CanonicalizationPreconditionError(
            "sidecar body must contain exactly two-space separator"
        )
    embedded_sha, embedded_basename = parts
    if len(embedded_sha) != 64 or any(
        c not in "0123456789abcdef" for c in embedded_sha
    ):
        raise CanonicalizationPreconditionError(
            "embedded SHA must be 64 lowercase hex characters"
        )
    if not embedded_basename:
        raise CanonicalizationPreconditionError(
            "sidecar basename is empty"
        )
    return embedded_sha, embedded_basename, line_ending


def render_canonical_sidecar_body(sha_hex: str, basename: str) -> bytes:
    """Render a canonical Phase 4bb-F sidecar body bytes.

    Returns ``f"{sha_hex}  {basename}\\n".encode("ascii")``.
    """
    if len(sha_hex) != 64 or any(
        c not in "0123456789abcdef" for c in sha_hex
    ):
        raise ValueError("sha_hex must be 64 lowercase hex characters")
    if not basename or "/" in basename or "\\" in basename or "\n" in basename:
        raise ValueError("invalid basename for sidecar body")
    return f"{sha_hex}{TWO_SPACES}{basename}\n".encode("ascii")


# ---------------------------------------------------------------------------
# Path discipline
# ---------------------------------------------------------------------------


def _under_repo_root(path: Path, repo_root: Path) -> bool:
    try:
        path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return False
    return True


def assert_target_sidecar_path(target_path: Path, repo_root: Path) -> None:
    """Refuse to write any path other than the exact predeclared target."""
    expected = (repo_root / TARGET_SIDECAR_REL).resolve()
    if target_path.resolve() != expected:
        raise CanonicalizationPathRefusedError(
            f"refusing to mutate non-target path: {target_path}"
        )


def assert_report_path_under_canonicalization_reports(
    report_path: Path, repo_root: Path
) -> None:
    """Refuse to write canonicalization report outside its canonical root."""
    root = (repo_root / CANONICALIZATION_REPORTS_ROOT_REL).resolve()
    try:
        report_path.resolve().relative_to(root)
    except ValueError as exc:
        raise CanonicalizationPathRefusedError(
            f"refusing to write report outside {root}: {report_path}"
        ) from exc


# ---------------------------------------------------------------------------
# Atomic file write
# ---------------------------------------------------------------------------


def atomic_write_bytes(
    target_path: Path, payload: bytes, *, refuse_overwrite_if_identical: bool = True
) -> None:
    """Write *payload* to *target_path* atomically via tempfile + os.replace.

    If ``refuse_overwrite_if_identical`` is true and the existing file has
    identical bytes, no write occurs. Otherwise, the file is replaced
    atomically.

    The script is intentionally narrow: target_path's parent directory
    must already exist. No mkdir is performed by this helper.
    """
    parent = target_path.parent
    if not parent.is_dir():
        raise CanonicalizationPathRefusedError(
            f"refusing to write: parent directory missing: {parent}"
        )
    if target_path.exists() and refuse_overwrite_if_identical:
        existing = target_path.read_bytes()
        if existing == payload:
            return
    fd, tmp_name = tempfile.mkstemp(
        dir=str(parent),
        prefix=target_path.name + ".tmp.",
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(payload)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        os.replace(tmp_path, target_path)
    except Exception:
        try:
            tmp_path.unlink(missing_ok=True)
        finally:
            raise


# ---------------------------------------------------------------------------
# Precondition / postcondition verification
# ---------------------------------------------------------------------------


def _check_artefact_size_and_sha(
    label: str,
    path: Path,
    expected_size: int | None,
    expected_sha: str,
) -> tuple[int, str]:
    if not path.is_file():
        raise CanonicalizationPreconditionError(
            f"{label} not found at {path}"
        )
    size = path.stat().st_size
    if expected_size is not None and size != expected_size:
        raise CanonicalizationPreconditionError(
            f"{label} size {size} != expected {expected_size}"
        )
    sha = compute_sha256(path)
    if sha != expected_sha:
        raise CanonicalizationPreconditionError(
            f"{label} SHA256 {sha} != expected {expected_sha}"
        )
    return size, sha


def verify_preconditions(repo_root: Path) -> dict:
    target_sidecar = (repo_root / TARGET_SIDECAR_REL).resolve()
    target_zip = (repo_root / TARGET_ZIP_REL).resolve()
    manifest = (repo_root / V002_MANIFEST_REL).resolve()
    acq_log = (repo_root / V002_ACQ_LOG_REL).resolve()
    gate_report = (repo_root / PHASE_4BL_D_GATE_REPORT_REL).resolve()

    if not target_sidecar.is_file():
        raise CanonicalizationPreconditionError(
            f"target sidecar missing: {target_sidecar}"
        )
    sidecar_bytes = target_sidecar.read_bytes()
    sidecar_size = len(sidecar_bytes)
    if sidecar_size != EXPECTED_PRE_SIDECAR_SIZE:
        raise CanonicalizationPreconditionError(
            f"target sidecar pre-size {sidecar_size} != "
            f"expected {EXPECTED_PRE_SIDECAR_SIZE}"
        )
    embedded_sha, embedded_basename, line_ending = parse_canonical_sidecar_body(
        sidecar_bytes
    )
    if line_ending != "CRLF":
        raise CanonicalizationPreconditionError(
            f"target sidecar line ending {line_ending} != expected CRLF"
        )
    if embedded_sha != EXPECTED_ZIP_SHA:
        raise CanonicalizationPreconditionError(
            f"embedded SHA {embedded_sha} != expected {EXPECTED_ZIP_SHA}"
        )
    if embedded_basename != EXPECTED_TARGET_BASENAME:
        raise CanonicalizationPreconditionError(
            f"embedded basename {embedded_basename!r} != "
            f"expected {EXPECTED_TARGET_BASENAME!r}"
        )
    pre_sidecar_sha = hashlib.sha256(sidecar_bytes).hexdigest()

    zip_size, zip_sha = _check_artefact_size_and_sha(
        "raw zip", target_zip, EXPECTED_ZIP_SIZE, EXPECTED_ZIP_SHA
    )
    _, manifest_sha = _check_artefact_size_and_sha(
        "v002 manifest", manifest, None, EXPECTED_V002_MANIFEST_SHA
    )
    _, acq_log_sha = _check_artefact_size_and_sha(
        "v002 acquisition log", acq_log, None, EXPECTED_V002_ACQ_LOG_SHA
    )
    _, gate_report_sha = _check_artefact_size_and_sha(
        "Phase 4bl-D gate report",
        gate_report,
        None,
        EXPECTED_PHASE_4BL_D_GATE_REPORT_SHA,
    )

    return {
        "target_sidecar_path": str(target_sidecar),
        "target_zip_path": str(target_zip),
        "v002_manifest_path": str(manifest),
        "v002_acq_log_path": str(acq_log),
        "phase_4bl_d_gate_report_path": str(gate_report),
        "pre_sidecar_bytes": sidecar_bytes,
        "pre_sidecar_size": sidecar_size,
        "pre_sidecar_sha256": pre_sidecar_sha,
        "pre_sidecar_line_ending": line_ending,
        "embedded_sha": embedded_sha,
        "embedded_basename": embedded_basename,
        "raw_zip_size_before": zip_size,
        "raw_zip_sha_before": zip_sha,
        "v002_manifest_sha_before": manifest_sha,
        "v002_acq_log_sha_before": acq_log_sha,
        "phase_4bl_d_gate_report_sha_before": gate_report_sha,
    }


def verify_postconditions(
    repo_root: Path,
    pre: dict,
) -> dict:
    target_sidecar = Path(pre["target_sidecar_path"])
    target_zip = Path(pre["target_zip_path"])
    manifest = Path(pre["v002_manifest_path"])
    acq_log = Path(pre["v002_acq_log_path"])
    gate_report = Path(pre["phase_4bl_d_gate_report_path"])

    post_bytes = target_sidecar.read_bytes()
    post_size = len(post_bytes)
    if post_size != EXPECTED_POST_SIDECAR_SIZE:
        raise CanonicalizationPostconditionError(
            f"target sidecar post-size {post_size} != "
            f"expected {EXPECTED_POST_SIDECAR_SIZE}"
        )
    embedded_sha, embedded_basename, line_ending = parse_canonical_sidecar_body(
        post_bytes
    )
    if line_ending != "LF":
        raise CanonicalizationPostconditionError(
            f"target sidecar post line ending {line_ending} != expected LF"
        )
    if embedded_sha != EXPECTED_ZIP_SHA:
        raise CanonicalizationPostconditionError(
            f"post embedded SHA {embedded_sha} != expected {EXPECTED_ZIP_SHA}"
        )
    if embedded_basename != EXPECTED_TARGET_BASENAME:
        raise CanonicalizationPostconditionError(
            f"post embedded basename {embedded_basename!r} != "
            f"expected {EXPECTED_TARGET_BASENAME!r}"
        )
    post_sidecar_sha = hashlib.sha256(post_bytes).hexdigest()

    zip_size_after, zip_sha_after = _check_artefact_size_and_sha(
        "raw zip (post)", target_zip, EXPECTED_ZIP_SIZE, EXPECTED_ZIP_SHA
    )
    _, manifest_sha_after = _check_artefact_size_and_sha(
        "v002 manifest (post)", manifest, None, EXPECTED_V002_MANIFEST_SHA
    )
    _, acq_log_sha_after = _check_artefact_size_and_sha(
        "v002 acquisition log (post)",
        acq_log,
        None,
        EXPECTED_V002_ACQ_LOG_SHA,
    )
    _, gate_report_sha_after = _check_artefact_size_and_sha(
        "Phase 4bl-D gate report (post)",
        gate_report,
        None,
        EXPECTED_PHASE_4BL_D_GATE_REPORT_SHA,
    )

    byte_delta = post_size - pre["pre_sidecar_size"]
    if byte_delta != -1:
        raise CanonicalizationPostconditionError(
            f"byte_delta {byte_delta} != expected -1"
        )

    return {
        "post_sidecar_bytes": post_bytes,
        "post_sidecar_size": post_size,
        "post_sidecar_sha256": post_sidecar_sha,
        "post_sidecar_line_ending": line_ending,
        "embedded_sha_after": embedded_sha,
        "embedded_basename_after": embedded_basename,
        "raw_zip_size_after": zip_size_after,
        "raw_zip_sha_after": zip_sha_after,
        "v002_manifest_sha_after": manifest_sha_after,
        "v002_acq_log_sha_after": acq_log_sha_after,
        "phase_4bl_d_gate_report_sha_after": gate_report_sha_after,
        "byte_delta": byte_delta,
    }


# ---------------------------------------------------------------------------
# Report rendering and writing
# ---------------------------------------------------------------------------


def _short_commit(commit_sha: str | None) -> str:
    if not commit_sha:
        return "unknown00000"
    return commit_sha[:12]


def build_report(
    *,
    repo_root: Path,
    pre: dict,
    post: dict,
    created_at_unix_ms: int,
    created_at_utc: str,
    base_commit_sha: str | None,
    code_commit_sha: str | None,
    script_path: Path | None,
    report_path: Path,
    report_sidecar_path: Path,
) -> dict:
    short_commit = _short_commit(code_commit_sha)
    report = {
        # identity
        "schema_version": SCHEMA_VERSION,
        "phase": PHASE,
        "phase_id": PHASE_ID,
        "artefact_type": ARTEFACT_TYPE,
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "mutation_type": MUTATION_TYPE,
        # target
        "target_sidecar_path": TARGET_SIDECAR_REL,
        "target_zip_path": TARGET_ZIP_REL,
        "target_symbol": TARGET_SYMBOL,
        "target_utc_date": TARGET_UTC_DATE,
        # pre-state
        "pre_sidecar_sha256": pre["pre_sidecar_sha256"],
        "pre_sidecar_size_bytes": pre["pre_sidecar_size"],
        "pre_sidecar_line_ending": pre["pre_sidecar_line_ending"],
        "pre_sidecar_body_repr": repr(pre["pre_sidecar_bytes"]),
        "embedded_zip_sha256_before": pre["embedded_sha"],
        "embedded_basename_before": pre["embedded_basename"],
        "target_zip_sha256_before": pre["raw_zip_sha_before"],
        "target_zip_size_bytes_before": pre["raw_zip_size_before"],
        "v002_manifest_sha256_before": pre["v002_manifest_sha_before"],
        "v002_acquisition_log_sha256_before": pre["v002_acq_log_sha_before"],
        "phase_4bl_d_gate_report_sha256_before": pre[
            "phase_4bl_d_gate_report_sha_before"
        ],
        # post-state
        "post_sidecar_sha256": post["post_sidecar_sha256"],
        "post_sidecar_size_bytes": post["post_sidecar_size"],
        "post_sidecar_line_ending": post["post_sidecar_line_ending"],
        "post_sidecar_body_repr": repr(post["post_sidecar_bytes"]),
        "embedded_zip_sha256_after": post["embedded_sha_after"],
        "embedded_basename_after": post["embedded_basename_after"],
        "target_zip_sha256_after": post["raw_zip_sha_after"],
        "target_zip_size_bytes_after": post["raw_zip_size_after"],
        "v002_manifest_sha256_after": post["v002_manifest_sha_after"],
        "v002_acquisition_log_sha256_after": post["v002_acq_log_sha_after"],
        "phase_4bl_d_gate_report_sha256_after": post[
            "phase_4bl_d_gate_report_sha_after"
        ],
        # mutation summary
        "byte_delta": post["byte_delta"],
        "market_data_mutated": False,
        "raw_zip_mutated": False,
        "manifest_mutated": False,
        "acquisition_log_mutated": False,
        "gate_report_mutated": False,
        "other_sidecars_mutated": False,
        "only_target_sidecar_mutated": True,
        "phase_4bb_f_policy_amended": False,
        "phase_4bl_d_gate_amended": False,
        "gate_rerun_performed": False,
        "successor_authorized": False,
        # execution metadata
        "created_at_utc": created_at_utc,
        "created_at_unix_ms": created_at_unix_ms,
        "base_commit_sha": base_commit_sha,
        "code_commit_sha": code_commit_sha,
        "code_commit_sha_short": short_commit,
        "script_path": str(script_path) if script_path else None,
        "report_path": str(report_path.relative_to(repo_root))
        if _under_repo_root(report_path, repo_root)
        else str(report_path),
        "report_sidecar_path": str(report_sidecar_path.relative_to(repo_root))
        if _under_repo_root(report_sidecar_path, repo_root)
        else str(report_sidecar_path),
        "python_version": platform.python_version(),
        "platform_summary": (
            f"{platform.system()} {platform.release()} ({platform.machine()})"
        ),
        # non-authorizations
        "phase_4bl_d_r_authorized": False,
        "phase_4bl_e_authorized": False,
        "phase_4bm_authorized": False,
        "phase_4bn_authorized": False,
        "phase_4bo_authorized": False,
        "phase_4bp_authorized": False,
        "phase_4bq_authorized": False,
        "phase_5_authorized": False,
        "phase_4_canonical_authorized": False,
        "successor_state_recording_authorized": False,
        "manifest_research_eligible_flip_authorized": False,
        "manifest_eligibility_gate_status_transition_authorized": False,
        "chronological_split_policy_change_authorized": False,
        "normalization_authorized": False,
        "derived_generation_authorized": False,
        "feature_computation_authorized": False,
        "label_computation_authorized": False,
        "diagnostics_authorized": False,
        "label_statistics_authorized": False,
        "ml_training_authorized": False,
        "strategy_implementation_authorized": False,
        "signal_computation_authorized": False,
        "backtest_execution_authorized": False,
        "acquisition_authorized": False,
        "public_endpoint_call_in_code_authorized": False,
        "binance_api_authorized": False,
        "authenticated_api_authorized": False,
        "private_endpoint_authorized": False,
        "websocket_authorized": False,
        "user_stream_authorized": False,
        "credentials_authorized": False,
        "env_file_authorized": False,
        "mcp_json_authorized": False,
        "mcp_authorized": False,
        "graphify_authorized": False,
        "paper_shadow_authorized": False,
        "live_readiness_authorized": False,
        "deployment_authorized": False,
        "exchange_write_authorized": False,
        "phase_4bb_f_amendment_authorized": False,
        "phase_4bl_d_gate_amendment_authorized": False,
    }
    return report


def serialize_report(report: dict) -> bytes:
    """Serialize the report deterministically (sorted keys; LF newline)."""
    text = json.dumps(
        report,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
    )
    if not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def write_report_and_sidecar(
    *,
    repo_root: Path,
    report: dict,
    report_path: Path,
) -> tuple[Path, str, Path, str, int, int]:
    """Write the canonicalization report JSON and its paired SHA256 sidecar."""
    assert_report_path_under_canonicalization_reports(report_path, repo_root)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = serialize_report(report)
    atomic_write_bytes(report_path, payload)
    report_sha = hashlib.sha256(payload).hexdigest()
    report_size = len(payload)
    sidecar_path = report_path.with_name(report_path.name + ".sha256")
    assert_report_path_under_canonicalization_reports(sidecar_path, repo_root)
    sidecar_body = render_canonical_sidecar_body(report_sha, report_path.name)
    atomic_write_bytes(sidecar_path, sidecar_body)
    sidecar_sha = hashlib.sha256(sidecar_body).hexdigest()
    return report_path, report_sha, sidecar_path, sidecar_sha, report_size, len(
        sidecar_body
    )


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Phase 4bl-D-S2 controlled sidecar canonicalization."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root (defaults to the parent of scripts/).",
    )
    parser.add_argument(
        "--base-commit-sha",
        default=None,
        help="Pre-execution main SHA (recorded in report).",
    )
    parser.add_argument(
        "--code-commit-sha",
        default=None,
        help="Branch HEAD SHA at execution time (recorded in report).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run preconditions only; do not mutate.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    if not repo_root.is_dir():
        raise CanonicalizationPathRefusedError(
            f"repo root not found: {repo_root}"
        )

    pre = verify_preconditions(repo_root)
    if args.dry_run:
        print("Phase 4bl-D-S2 dry-run: preconditions PASS")
        print(
            "pre_sidecar_sha256:",
            pre["pre_sidecar_sha256"],
        )
        print(
            "pre_sidecar_size:",
            pre["pre_sidecar_size"],
        )
        print(
            "pre_sidecar_line_ending:",
            pre["pre_sidecar_line_ending"],
        )
        return 0

    # Perform the canonicalization (atomic rewrite).
    target_sidecar = Path(pre["target_sidecar_path"])
    assert_target_sidecar_path(target_sidecar, repo_root)
    canonical_body = render_canonical_sidecar_body(
        pre["embedded_sha"], pre["embedded_basename"]
    )
    atomic_write_bytes(target_sidecar, canonical_body)

    post = verify_postconditions(repo_root, pre)

    # Build report after both checks pass.
    created_at_unix_ms = int(time.time() * 1000)
    created_at_utc = time.strftime(
        "%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(created_at_unix_ms / 1000)
    )
    short = _short_commit(args.code_commit_sha)
    report_filename = (
        f"{DATASET_FAMILY}__{DATASET_VERSION}__phase-{PHASE_ID.lower()}__"
        f"{created_at_unix_ms}__{short}.json"
    )
    report_path = (
        repo_root / CANONICALIZATION_REPORTS_ROOT_REL / report_filename
    )
    sidecar_path = report_path.with_name(report_path.name + ".sha256")

    report = build_report(
        repo_root=repo_root,
        pre=pre,
        post=post,
        created_at_unix_ms=created_at_unix_ms,
        created_at_utc=created_at_utc,
        base_commit_sha=args.base_commit_sha,
        code_commit_sha=args.code_commit_sha,
        script_path=Path(__file__).resolve(),
        report_path=report_path,
        report_sidecar_path=sidecar_path,
    )
    (
        written_report_path,
        report_sha,
        written_sidecar_path,
        sidecar_sha,
        report_size,
        sidecar_size,
    ) = write_report_and_sidecar(
        repo_root=repo_root, report=report, report_path=report_path
    )

    # Console summary for the operator report.
    print("Phase 4bl-D-S2: controlled sidecar canonicalization SUCCESS")
    print(f"target_sidecar: {target_sidecar}")
    print(
        "  pre:  size="
        f"{pre['pre_sidecar_size']} sha={pre['pre_sidecar_sha256']} "
        f"line_ending={pre['pre_sidecar_line_ending']}"
    )
    print(
        "  post: size="
        f"{post['post_sidecar_size']} sha={post['post_sidecar_sha256']} "
        f"line_ending={post['post_sidecar_line_ending']}"
    )
    print(f"byte_delta: {post['byte_delta']}")
    print(
        "embedded_sha unchanged: "
        f"{pre['embedded_sha'] == post['embedded_sha_after']}"
    )
    print(
        "embedded_basename unchanged: "
        f"{pre['embedded_basename'] == post['embedded_basename_after']}"
    )
    print(
        "raw_zip_sha unchanged: "
        f"{pre['raw_zip_sha_before'] == post['raw_zip_sha_after']}"
    )
    print(
        "v002_manifest_sha unchanged: "
        f"{pre['v002_manifest_sha_before'] == post['v002_manifest_sha_after']}"
    )
    print(
        "v002_acquisition_log_sha unchanged: "
        f"{pre['v002_acq_log_sha_before'] == post['v002_acq_log_sha_after']}"
    )
    gate_sha_unchanged = (
        pre["phase_4bl_d_gate_report_sha_before"]
        == post["phase_4bl_d_gate_report_sha_after"]
    )
    print(f"phase_4bl_d_gate_report_sha unchanged: {gate_sha_unchanged}")
    print(f"report_path: {written_report_path}")
    print(f"report_sha256: {report_sha}")
    print(f"report_size_bytes: {report_size}")
    print(f"report_sidecar_path: {written_sidecar_path}")
    print(f"report_sidecar_sha256: {sidecar_sha}")
    print(f"report_sidecar_size_bytes: {sidecar_size}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
