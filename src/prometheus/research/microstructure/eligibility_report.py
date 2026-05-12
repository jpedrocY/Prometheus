"""Gate-report data model + JSON serialisation for Phase 4bb-C.

Phase 4bb-C scope: the :class:`AggTradesGateReport` data model and the
:func:`write_report_atomic` helper that writes the report JSON plus a
paired ``.sha256`` sidecar under ``data/microstructure/gate-reports/``
via the Phase 4aw :class:`raw_writer.RawWriter` discipline.

This module:

- writes only under ``data/microstructure/gate-reports/`` (gitignored);
- never overwrites an existing report;
- does not mutate any other file.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .eligibility_io import GATE_REPORTS_SUBDIR, assert_path_under_microstructure


@dataclass(frozen=True)
class AggTradesGateReport:
    """JSON-serialisable gate report."""

    report_id: str
    dataset_family: str
    version: str
    symbol: str
    source_manifest_path: str
    raw_zip_path: str
    sidecar_path: str
    acquisition_log_path: str
    created_at_utc_ms: int
    code_commit_sha: str
    overall_status: str
    research_eligible_after: bool
    eligibility_gate_status_after: str
    checks: tuple[Mapping[str, Any], ...]
    invalid_window_candidates: tuple[Mapping[str, Any], ...]
    measured_summary: Mapping[str, Any]
    boundary_confirmations: Mapping[str, bool]
    no_successor_authorization: bool

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a JSON-friendly mapping."""
        return {
            "report_id": self.report_id,
            "dataset_family": self.dataset_family,
            "version": self.version,
            "symbol": self.symbol,
            "source_manifest_path": self.source_manifest_path,
            "raw_zip_path": self.raw_zip_path,
            "sidecar_path": self.sidecar_path,
            "acquisition_log_path": self.acquisition_log_path,
            "created_at_utc_ms": self.created_at_utc_ms,
            "code_commit_sha": self.code_commit_sha,
            "overall_status": self.overall_status,
            "research_eligible_after": self.research_eligible_after,
            "eligibility_gate_status_after": self.eligibility_gate_status_after,
            "checks": [dict(c) for c in self.checks],
            "invalid_window_candidates": [
                dict(c) for c in self.invalid_window_candidates
            ],
            "measured_summary": dict(self.measured_summary),
            "boundary_confirmations": dict(self.boundary_confirmations),
            "no_successor_authorization": self.no_successor_authorization,
        }


def _ensure_directory(path: Path) -> None:
    """Create *path* (and parents) if it does not already exist."""
    path.mkdir(parents=True, exist_ok=True)


def _atomic_write_json_with_sha(
    payload: dict[str, Any],
    target_json: Path,
) -> Path:
    """Write *payload* as JSON to *target_json* atomically with a paired SHA256.

    Refuses to overwrite an existing report. The companion sidecar is written
    after the JSON is renamed into place.
    """
    if target_json.exists():
        raise FileExistsError(
            f"refusing to overwrite existing gate report at {target_json}"
        )
    target_json.parent.mkdir(parents=True, exist_ok=True)

    # Atomic write via tempfile + rename. The tempfile lives in the same
    # directory to ensure the rename is atomic on Windows / POSIX.
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{target_json.name}.",
        suffix=".tmp",
        dir=str(target_json.parent),
    )
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(body)
            f.flush()
            with contextlib.suppress(OSError):
                os.fsync(f.fileno())
        os.replace(tmp_name, target_json)
    finally:
        if os.path.exists(tmp_name):
            with contextlib.suppress(OSError):
                os.unlink(tmp_name)

    # Paired sidecar.
    sidecar = target_json.with_suffix(target_json.suffix + ".sha256")
    digest = hashlib.sha256(body).hexdigest()
    sidecar_body = (
        f"{digest}  {target_json.name}\n"
    ).encode()
    fd2, tmp_name2 = tempfile.mkstemp(
        prefix=f".{sidecar.name}.",
        suffix=".tmp",
        dir=str(sidecar.parent),
    )
    try:
        with os.fdopen(fd2, "wb") as f:
            f.write(sidecar_body)
            f.flush()
            with contextlib.suppress(OSError):
                os.fsync(f.fileno())
        os.replace(tmp_name2, sidecar)
    finally:
        if os.path.exists(tmp_name2):
            with contextlib.suppress(OSError):
                os.unlink(tmp_name2)

    return target_json


def write_report_atomic(
    report: AggTradesGateReport,
    output_root: Path,
    *,
    family_subdir: str | None = None,
) -> Path:
    """Write *report* under the gate-reports subdirectory of *output_root*.

    *output_root* must resolve under ``data/microstructure/``. The report
    file name is derived from ``report.report_id`` and is paired with a
    ``.sha256`` sidecar.

    Backward-compatible placement (Phase 4bb-C original convention):

    - When *family_subdir* is ``None`` (the default), the report is
      written under ``<output_root>/<GATE_REPORTS_SUBDIR>/`` exactly as
      it was prior to Phase 4bb-F-implementation. Existing local
      gitignored artefacts produced under this convention (notably the
      Phase 4bb-D report under ``data/microstructure/gate-reports/
      gate-reports/``) remain valid and are not affected.

    Canonical placement (Phase 4bb-F-implementation; opt-in):

    - When *family_subdir* is a non-empty string (e.g. ``"raw"``), the
      report is written under ``<output_root>/<family_subdir>/`` and
      the legacy ``gate-reports`` subdirectory injection is skipped.
      Canonical raw-gate callers pass ``output_root =
      data/microstructure/gate-reports`` and ``family_subdir = "raw"``
      to produce the Phase 4bb-F canonical placement
      ``data/microstructure/gate-reports/raw/<report_id>.json``.

    The function never modifies any existing file. It refuses to
    overwrite an existing report or sidecar.
    """
    if not isinstance(output_root, Path):
        raise TypeError("output_root must be a pathlib.Path")
    assert_path_under_microstructure(output_root, label="output_root")

    if family_subdir is None:
        gate_dir = output_root / GATE_REPORTS_SUBDIR
    else:
        if not isinstance(family_subdir, str) or not family_subdir:
            raise ValueError(
                "family_subdir must be a non-empty string when provided"
            )
        if "/" in family_subdir or "\\" in family_subdir:
            raise ValueError(
                f"family_subdir must not contain path separators "
                f"(got {family_subdir!r})"
            )
        gate_dir = output_root / family_subdir

    _ensure_directory(gate_dir)

    target = gate_dir / f"{report.report_id}.json"
    payload = report.to_dict()
    return _atomic_write_json_with_sha(payload, target)
