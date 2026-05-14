"""Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate Rerun.

This is a thin wrapper around the Phase 4bl-D gate script
(``scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py``). It:

1. Imports the Phase 4bl-D gate module unchanged.
2. Monkey-patches the gate module's three identity constants at module
   level so that the gate emits a Phase 4bl-D-R-shaped report under
   the canonical Phase 4bb-F path
   ``data/microstructure/gate-reports/raw/<dataset_family>__<dataset_version>__phase-4bl-d-r__<unix_ms>__<short_commit>.json``.
3. Modifies the gate module's ``GOVERNANCE_LABELS`` dict in place so the
   rerun's source phase boundary is recorded as ``4bl-D-S2`` (the
   remediation phase that canonicalised the 2025-01-15 sidecar) rather
   than the Phase 4bl-D source boundary ``4bl-C``.
4. Calls the gate's ``run_gate(...)`` once. The full 33-check Phase 4bl-D
   protocol runs verbatim, including full per-row Phase 4ax
   ``validate_aggtrade_payload`` validation across every row of the
   Phase 4bl-C v002 90-day BTCUSDT raw dataset.
5. After the gate's atomic write completes, reads the produced report
   JSON, augments it in memory with Phase 4bl-D-R-specific lineage
   fields:

   * ``predecessor_gate_phase``, ``predecessor_gate_id``,
     ``predecessor_gate_report_path``,
     ``predecessor_gate_report_sha256``,
     ``predecessor_gate_verdict``,
     ``predecessor_gate_overall_status``,
     ``predecessor_gate_failure_summary``;
   * ``remediation_phase``, ``remediation_type``,
     ``remediation_report_path``,
     ``remediation_report_sha256``,
     ``canonicalized_sidecar_path``,
     ``canonicalized_sidecar_pre_sha256``,
     ``canonicalized_sidecar_post_sha256``,
     ``target_raw_zip_sha256``,
     ``target_raw_zip_path``.

   It also normalises the ``phase_id`` field to the brief-specified
   mixed-case ``"4bl-D-R"`` in the report body (the canonical filename
   keeps the lowercase ``phase-4bl-d-r`` segment to honour the
   Phase 4bb-F lowercase filename convention).
6. Deletes the gate's own report + sidecar pair (the wrapper's own
   outputs from this same run) and atomically rewrites both with the
   augmented report. The deterministic-JSON formatting (sorted keys,
   indent=2, trailing newline) is preserved exactly.

The wrapper does NOT modify the gate script.

The wrapper does NOT weaken the 33-check Phase 4bl-D protocol.

The wrapper does NOT touch any upstream artefact (raw zip, sidecar,
v002 manifest, acquisition log, Phase 4bl-D gate report, Phase 4bl-D-S2
canonicalisation report).

The wrapper does NOT contact a network endpoint, open a WebSocket, use
credentials, read ``.env``, create ``.mcp.json``, enable MCP, enable
Graphify, or perform any exchange-write.

The wrapper does NOT flip ``research_eligible`` on any manifest.

The wrapper does NOT transition ``eligibility_gate_status`` on any
actual manifest.

The wrapper does NOT authorise Phase 4bl-E, Phase 4bm-*, Phase 5, or
any successor phase.

Per the Phase 4bk-A workflow standard, this rerun runs only on a
branch; it is not project-complete until a separately authorised
merge phase records its merge-closeout on ``main``.

Run:

    uv run python scripts/phase4bl_d_r_rerun_raw_gate.py

with the optional ``--log-progress`` flag forwarded to the gate.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Any

_REPO_ROOT: Path = Path(__file__).resolve().parent.parent
_GATE_SCRIPT_PATH: Path = (
    _REPO_ROOT
    / "scripts"
    / "phase4bl_d_validate_multiday_raw_manifest_gate.py"
)

# --------------------------------------------------------------------------- #
# Locked Phase 4bl-D-R identity constants
# --------------------------------------------------------------------------- #

# Lowercase phase id is used to compose the canonical Phase 4bb-F filename
# segment ``phase-4bl-d-r``. The report body itself records the
# brief-specified mixed-case form ``4bl-D-R`` (see ``_AUGMENT_PHASE_ID``).
_GATE_PHASE_ID: str = "4bl-d-r"
_GATE_PHASE_NAME: str = "Phase 4bl-D-R"
_GATE_ARTEFACT_TYPE: str = (
    "raw_multiday_manifest_eligibility_gate_rerun_report"
)
_AUGMENT_PHASE_ID: str = "4bl-D-R"

# Remediation lineage points at the Phase 4bl-D-S2 canonicalisation phase,
# not at Phase 4bl-C (which is the Phase 4bl-D source phase boundary).
_REMEDIATION_PHASE: str = "4bl-D-S2"
_REMEDIATION_TYPE: str = (
    "metadata_sidecar_line_ending_canonicalization"
)

# Predecessor lineage: Phase 4bl-D produced the
# ``RAW_MULTIDAY_GATE_FAIL`` whose only failing check root cause was the
# pre-canonicalisation CRLF sidecar.
_PREDECESSOR_PHASE: str = "4bl-D"
_PREDECESSOR_PHASE_ID: str = "4bl-d"
_PREDECESSOR_GATE_REPORT_REL_PATH: str = (
    "data/microstructure/gate-reports/raw/"
    "microstructure_raw_aggtrades_v001__v002__phase-4bl-d__"
    "1778627360966__2576a004c18a.json"
)
_PREDECESSOR_GATE_REPORT_SHA256: str = (
    "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7"
)
_PREDECESSOR_GATE_VERDICT: str = "RAW_MULTIDAY_GATE_FAIL"
_PREDECESSOR_GATE_OVERALL_STATUS: str = "fail"
_PREDECESSOR_GATE_FAILURE_SUMMARY: str = (
    "Phase 4bl-D produced overall_status=fail / "
    "gate_verdict=RAW_MULTIDAY_GATE_FAIL with 29 of 33 checks PASS and 4 "
    "FAIL. The single root cause for all 4 failed checks was the "
    "pre-existing Phase 4az 2025-01-15 sidecar at "
    "data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
    "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256 using Windows CRLF "
    "(\\r\\n) line terminator (100 bytes) instead of canonical "
    "Phase 4bb-F LF (\\n) terminator. The raw zip itself was byte-"
    "identical to the Phase 4az fixture (SHA256 f560c2e5...). Phase "
    "4bl-D-S2 canonicalised the sidecar to LF (99 bytes), preserving the "
    "embedded SHA value and basename byte-identically. Phase 4bl-D-R is "
    "the operator-authorised rerun of the Phase 4bl-D protocol against "
    "the unchanged v002 dataset with the canonicalised sidecar in "
    "place."
)
_PREDECESSOR_GATE_FAILED_CHECK_IDS: list[str] = [
    "raw_zip_sidecar_integrity",
    "per_file_row_count_consistency",
    "per_file_time_bounds_consistency",
    "total_row_count_consistency",
]

# Remediation report (Phase 4bl-D-S2 canonicalisation report).
_REMEDIATION_REPORT_REL_PATH: str = (
    "data/microstructure/canonicalization-reports/raw/"
    "microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__"
    "1778713761225__0d51bd7bac1e.json"
)
_REMEDIATION_REPORT_SHA256: str = (
    "8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3"
)
_TARGET_SIDECAR_REL_PATH: str = (
    "data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
    "2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256"
)
_TARGET_SIDECAR_PRE_SHA256: str = (
    "b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d"
)
_TARGET_SIDECAR_POST_SHA256: str = (
    "c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc"
)
_TARGET_RAW_ZIP_REL_PATH: str = (
    "data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/"
    "2025/01/BTCUSDT-aggTrades-2025-01-15.zip"
)
_TARGET_RAW_ZIP_SHA256: str = (
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
)

# --------------------------------------------------------------------------- #
# Public augmentation entry point (also used by offline tests)
# --------------------------------------------------------------------------- #


def augment_report(report: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of ``report`` with Phase 4bl-D-R-specific lineage fields.

    The original dict is left unchanged. The returned dict adds:

    - ``phase_id`` is normalised to the mixed-case ``"4bl-D-R"``
      brief-specified form.
    - ``predecessor_gate_*`` fields naming Phase 4bl-D and its FAIL
      verdict and report SHA.
    - ``remediation_*`` fields naming Phase 4bl-D-S2, the
      canonicalisation report SHA, the target sidecar path with
      pre/post SHAs, and the target raw zip path with its SHA.

    All other gate-produced fields (checks, per-file summaries,
    aggregate summary, governance labels, retained verdict ledger,
    preserved locks, etc.) are preserved verbatim.
    """
    out: dict[str, Any] = dict(report)
    out["phase_id"] = _AUGMENT_PHASE_ID
    out["predecessor_gate_phase"] = _PREDECESSOR_PHASE
    out["predecessor_gate_id"] = _PREDECESSOR_PHASE_ID
    out["predecessor_gate_report_path"] = _PREDECESSOR_GATE_REPORT_REL_PATH
    out["predecessor_gate_report_sha256"] = (
        _PREDECESSOR_GATE_REPORT_SHA256
    )
    out["predecessor_gate_verdict"] = _PREDECESSOR_GATE_VERDICT
    out["predecessor_gate_overall_status"] = (
        _PREDECESSOR_GATE_OVERALL_STATUS
    )
    out["predecessor_gate_failure_summary"] = (
        _PREDECESSOR_GATE_FAILURE_SUMMARY
    )
    out["predecessor_gate_failed_check_ids"] = list(
        _PREDECESSOR_GATE_FAILED_CHECK_IDS
    )
    out["remediation_phase"] = _REMEDIATION_PHASE
    out["remediation_type"] = _REMEDIATION_TYPE
    out["remediation_report_path"] = _REMEDIATION_REPORT_REL_PATH
    out["remediation_report_sha256"] = _REMEDIATION_REPORT_SHA256
    out["canonicalized_sidecar_path"] = _TARGET_SIDECAR_REL_PATH
    out["canonicalized_sidecar_pre_sha256"] = _TARGET_SIDECAR_PRE_SHA256
    out["canonicalized_sidecar_post_sha256"] = (
        _TARGET_SIDECAR_POST_SHA256
    )
    out["target_raw_zip_path"] = _TARGET_RAW_ZIP_REL_PATH
    out["target_raw_zip_sha256"] = _TARGET_RAW_ZIP_SHA256

    # The wrapper preserves the rerun's strict no-mutation / no-
    # authorisation posture verbatim. Re-assert the invariants here so
    # readers of the augmented report do not have to cross-reference
    # the gate-produced fields.
    out["wrapper_phase"] = _GATE_PHASE_NAME
    out["wrapper_phase_id_lowercase"] = _GATE_PHASE_ID
    out["wrapper_artefact_type"] = _GATE_ARTEFACT_TYPE
    return out


# --------------------------------------------------------------------------- #
# Wrapper internals
# --------------------------------------------------------------------------- #


def _compute_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    """Atomic write-then-rename. Refuse to overwrite."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise RuntimeError(
            f"refusing to overwrite existing file at {path}"
        )
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        if path.exists():
            raise RuntimeError(
                f"refusing to overwrite existing file (race) at {path}"
            )
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()


def _serialise_report(report: dict[str, Any]) -> bytes:
    """Deterministic JSON serialisation matching the gate's format."""
    text = json.dumps(
        report, sort_keys=True, indent=2, ensure_ascii=False
    ) + "\n"
    return text.encode("utf-8")


def _write_sidecar(json_path: Path, json_sha256_hex: str) -> Path:
    sidecar_path = json_path.with_suffix(json_path.suffix + ".sha256")
    body = f"{json_sha256_hex}  {json_path.name}\n".encode("ascii")
    _atomic_write_bytes(sidecar_path, body)
    return sidecar_path


# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #


def _load_gate_module() -> Any:
    """Load the Phase 4bl-D gate module by file path.

    The gate script lives under ``scripts/`` which is not a Python
    package (no ``__init__.py``), so we use ``importlib.util`` to load
    it directly from its file path. The returned module reference can
    be monkey-patched in place.
    """
    if not _GATE_SCRIPT_PATH.exists():
        raise FileNotFoundError(
            f"Phase 4bl-D gate script missing at {_GATE_SCRIPT_PATH}"
        )
    module_name = "phase4bl_d_validate_multiday_raw_manifest_gate"
    spec = importlib.util.spec_from_file_location(
        module_name,
        _GATE_SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"failed to build importlib spec for {_GATE_SCRIPT_PATH}"
        )
    module = importlib.util.module_from_spec(spec)
    # Register before exec so that decorators like ``@dataclass`` can
    # resolve ``cls.__module__`` back to a real entry in ``sys.modules``.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _patch_gate_module() -> Any:
    """Load the Phase 4bl-D gate module and monkeypatch identity constants.

    Returns the patched module reference.
    """
    gate = _load_gate_module()
    gate.PHASE_ID = _GATE_PHASE_ID
    gate.PHASE_NAME = _GATE_PHASE_NAME
    gate.ARTEFACT_TYPE = _GATE_ARTEFACT_TYPE
    gate.GOVERNANCE_LABELS["phase"] = _GATE_PHASE_ID
    gate.GOVERNANCE_LABELS["source_phase_boundary"] = _REMEDIATION_PHASE
    return gate


def run_rerun(
    *, output_root: Path, log_progress: bool = False
) -> int:
    """Run the gate rerun and rewrite the report with Phase 4bl-D-R lineage.

    Returns the exit code of the underlying gate (0 = pass, 1 = fail/error).

    The on-disk report and its paired SHA256 sidecar are atomically
    rewritten with the augmented report. The post-rewrite SHA256 of the
    JSON matches the sidecar verbatim.
    """
    gate = _patch_gate_module()
    exit_code = gate.run_gate(
        output_root=output_root, log_progress=log_progress
    )

    # Locate the report the gate produced. The gate prints the path,
    # but we can re-derive it from the directory listing under
    # ``data/microstructure/gate-reports/raw/`` filtered by the
    # ``phase-4bl-d-r`` segment.
    raw_dir = (output_root / "gate-reports" / "raw").resolve()
    if not raw_dir.exists():
        print(
            f"[Phase 4bl-D-R] ERROR: gate-reports/raw/ directory missing "
            f"at {raw_dir}",
            file=sys.stderr,
        )
        return 1
    candidates = sorted(
        p
        for p in raw_dir.glob(
            f"microstructure_raw_aggtrades_v001__v002__phase-"
            f"{_GATE_PHASE_ID}__*.json"
        )
        if not p.name.endswith(".sha256")
    )
    if not candidates:
        print(
            f"[Phase 4bl-D-R] ERROR: no Phase 4bl-D-R gate report found "
            f"under {raw_dir}",
            file=sys.stderr,
        )
        return 1
    # The wrapper expects exactly one rerun per branch. If several files
    # exist, pick the latest by unix_ms in the filename. This is
    # conservative: it never deletes an unrelated report.
    report_path = candidates[-1]
    sidecar_path = report_path.with_suffix(report_path.suffix + ".sha256")

    with open(report_path, encoding="utf-8") as fh:
        original_report: dict[str, Any] = json.load(fh)

    augmented = augment_report(original_report)
    payload_bytes = _serialise_report(augmented)

    # Atomic rewrite: delete the gate's own outputs (from this same
    # run), then atomically rewrite both. The wrapper never deletes a
    # report it did not just produce: the path is verified to live
    # under gate-reports/raw/ with the phase-4bl-d-r segment.
    if "phase-4bl-d-r" not in report_path.name:
        print(
            f"[Phase 4bl-D-R] ERROR: refusing to rewrite a report whose "
            f"name does not contain 'phase-4bl-d-r': {report_path.name}",
            file=sys.stderr,
        )
        return 1
    if sidecar_path.exists():
        sidecar_path.unlink()
    report_path.unlink()

    _atomic_write_bytes(report_path, payload_bytes)
    rewritten_sha = _compute_file_sha256(report_path)
    _write_sidecar(report_path, rewritten_sha)

    print("")
    print(f"[Phase 4bl-D-R] augmented report path: {report_path.as_posix()}")
    print(f"[Phase 4bl-D-R] augmented report sha256: {rewritten_sha}")
    print(f"[Phase 4bl-D-R] augmented sidecar path: {sidecar_path.as_posix()}")
    print(
        f"[Phase 4bl-D-R] underlying gate exit_code: {exit_code} "
        f"(0 = PASS, 1 = FAIL/ERROR)"
    )

    return exit_code


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="phase4bl_d_r_rerun_raw_gate",
        description=(
            "Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate "
            "Rerun (thin wrapper around the Phase 4bl-D gate)."
        ),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("data") / "microstructure",
        help=(
            "Microstructure root (must resolve under "
            "data/microstructure/). Defaults to data/microstructure."
        ),
    )
    parser.add_argument(
        "--log-progress",
        action="store_true",
        help="Log per-file progress to stdout (verbose).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    return run_rerun(
        output_root=args.output_root,
        log_progress=args.log_progress,
    )


if __name__ == "__main__":
    raise SystemExit(main())
