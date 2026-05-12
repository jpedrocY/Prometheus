"""Phase 4bb-F-implementation canonical path policy helpers.

Implements the Phase 4bb-F locked canonical path policy for gate
reports and successor-state JSON artefacts under the project's
gitignored ``data/microstructure/`` namespace.

Canonical gate-report path layout:

    data/microstructure/gate-reports/<family-subdir>/<canonical-filename>.json

Canonical gate-report filename:

    <dataset_family>__<dataset_version>__phase-<phase_id>__<unix_ms>__<short_commit>.json

Canonical successor-state path layout:

    data/microstructure/successor-state/<canonical-filename>.json

Canonical successor-state filename:

    <dataset_family>__<dataset_version>__<stage_marker>__phase-<phase_id>.json

Canonical paired SHA256 sidecar:

    <json_sha256_hex>  <json_basename>\\n   (two spaces, trailing newline)

This module is additive. Existing writers under
:mod:`prometheus.research.microstructure.eligibility_report`,
:mod:`prometheus.research.microstructure.derived_gate_report`,
:mod:`prometheus.research.microstructure.feature_gate_report`, and
:mod:`prometheus.research.microstructure.label_gate_report` continue to
work unchanged. Future call sites opt into the canonical placement by
calling the helpers in this module, or by passing the optional
``family_subdir`` kwarg threaded through the raw-gate writer /
orchestrator.

Backward-compatibility guarantee:

- This module never modifies any existing artefact.
- This module never moves, renames, or rewrites any prior local
  gitignored gate report or successor-state file. All seven prior
  local artefacts produced under the legacy paths
  (``gate-reports/gate-reports/`` for Phase 4bb-D and
  ``gate-reports/normalized/``, ``gate-reports/features/``,
  ``gate-reports/labels/``, ``successor-state/``) remain valid at
  their recorded paths and SHA256 digests.

This module does not perform any real ``data/microstructure/`` I/O at
import time. The sidecar writer ``write_paired_sha256_sidecar`` only
writes when called explicitly; tests use ``tmp_path`` only.

This module never imports ``requests``, ``httpx``, ``aiohttp``,
``urllib.request``, ``urllib3``, ``socket``, ``websockets``,
``binance``, ``dotenv``, ``python_dotenv``, ``os.environ``, or
``getenv``. It never reads ``.env``, never creates ``.mcp.json``, never
contacts any endpoint.
"""

from __future__ import annotations

import contextlib
import hashlib
import os
import tempfile
from pathlib import Path

FAMILY_SUBDIRS: dict[str, str] = {
    "raw": "raw",
    "normalized": "normalized",
    "features": "features",
    "labels": "labels",
}
"""Recognised family name → gate-reports subdirectory mapping.

Per the Phase 4bb-F locked canonical policy, every future gate-report
must live under ``data/microstructure/gate-reports/<family-subdir>/``.
"""

MICROSTRUCTURE_ROOT_PARTS: tuple[str, ...] = ("data", "microstructure")
GATE_REPORTS_ROOT_PARTS: tuple[str, ...] = ("data", "microstructure", "gate-reports")
SUCCESSOR_STATE_ROOT_PARTS: tuple[str, ...] = ("data", "microstructure", "successor-state")


class CanonicalPathError(RuntimeError):
    """Raised when a canonical path, filename, or sidecar is invalid."""


def _validate_short_commit(short: str) -> str:
    """Return *short* lower-cased after validating it is non-empty hex."""
    if not isinstance(short, str) or not short:
        raise CanonicalPathError("short_commit must be a non-empty string")
    if not all(c in "0123456789abcdef" for c in short.lower()):
        raise CanonicalPathError(f"short_commit must be hex (got {short!r})")
    return short.lower()


def derive_short_commit(code_commit_sha: str, *, length: int = 12) -> str:
    """Return the leading *length* hex chars of a full git SHA.

    The default ``length`` (12) matches the Phase 4bb-D / Phase 4bf /
    Phase 4bi-B / Phase 4bj-E precedent for gate-report identifiers.
    """
    if not isinstance(code_commit_sha, str):
        raise CanonicalPathError("code_commit_sha must be a string")
    if length < 7:
        raise CanonicalPathError("length must be >= 7")
    if len(code_commit_sha) < length:
        raise CanonicalPathError(
            f"code_commit_sha must be >= {length} hex chars "
            f"(got {len(code_commit_sha)})"
        )
    return _validate_short_commit(code_commit_sha[:length])


def normalize_family(family: str) -> str:
    """Return the canonical family-subdir name for *family*.

    Accepts the lower-cased family name (``raw``, ``normalized``,
    ``features``, ``labels``) and returns the corresponding subdirectory
    name from :data:`FAMILY_SUBDIRS`.
    """
    if not isinstance(family, str) or not family:
        raise CanonicalPathError("family must be a non-empty string")
    key = family.lower()
    if key not in FAMILY_SUBDIRS:
        raise CanonicalPathError(
            f"unknown family {family!r}; expected one of "
            f"{sorted(FAMILY_SUBDIRS)}"
        )
    return FAMILY_SUBDIRS[key]


def compose_canonical_gate_report_id(
    *,
    dataset_family: str,
    dataset_version: str,
    phase_id: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
) -> str:
    """Build the Phase 4bb-F canonical gate-report identifier.

    Format::

        <dataset_family>__<dataset_version>__phase-<phase_id>__<unix_ms>__<short>

    where ``<short>`` is the leading 12 hex chars of *code_commit_sha*.
    """
    if not isinstance(dataset_family, str) or not dataset_family:
        raise CanonicalPathError("dataset_family must be a non-empty string")
    if not isinstance(dataset_version, str) or not dataset_version:
        raise CanonicalPathError("dataset_version must be a non-empty string")
    if not isinstance(phase_id, str) or not phase_id:
        raise CanonicalPathError("phase_id must be a non-empty string")
    if not isinstance(generated_at_unix_ms, int) or isinstance(
        generated_at_unix_ms, bool
    ):
        raise CanonicalPathError("generated_at_unix_ms must be an int")
    if generated_at_unix_ms < 0:
        raise CanonicalPathError("generated_at_unix_ms must be >= 0")
    short = derive_short_commit(code_commit_sha)
    return (
        f"{dataset_family}__{dataset_version}__phase-{phase_id}__"
        f"{generated_at_unix_ms}__{short}"
    )


def compose_canonical_successor_state_filename(
    *,
    dataset_family: str,
    dataset_version: str,
    stage_marker: str,
    phase_id: str,
) -> str:
    """Build the Phase 4bb-F canonical successor-state filename (without ``.json``).

    Format::

        <dataset_family>__<dataset_version>__<stage_marker>__phase-<phase_id>
    """
    if not isinstance(dataset_family, str) or not dataset_family:
        raise CanonicalPathError("dataset_family must be a non-empty string")
    if not isinstance(dataset_version, str) or not dataset_version:
        raise CanonicalPathError("dataset_version must be a non-empty string")
    if not isinstance(stage_marker, str) or not stage_marker:
        raise CanonicalPathError("stage_marker must be a non-empty string")
    if not isinstance(phase_id, str) or not phase_id:
        raise CanonicalPathError("phase_id must be a non-empty string")
    return (
        f"{dataset_family}__{dataset_version}__{stage_marker}__phase-{phase_id}"
    )


def derive_canonical_gate_report_path(
    *,
    microstructure_root: Path,
    family: str,
    dataset_family: str,
    dataset_version: str,
    phase_id: str,
    generated_at_unix_ms: int,
    code_commit_sha: str,
) -> Path:
    """Return the canonical gate-report ``.json`` path.

    Result::

        <microstructure_root>/gate-reports/<family-subdir>/<canonical_id>.json

    *microstructure_root* must be a ``pathlib.Path`` pointing at the
    project's ``data/microstructure`` directory. The function does not
    create directories and does not touch the filesystem.
    """
    if not isinstance(microstructure_root, Path):
        raise CanonicalPathError("microstructure_root must be a pathlib.Path")
    subdir = normalize_family(family)
    report_id = compose_canonical_gate_report_id(
        dataset_family=dataset_family,
        dataset_version=dataset_version,
        phase_id=phase_id,
        generated_at_unix_ms=generated_at_unix_ms,
        code_commit_sha=code_commit_sha,
    )
    return microstructure_root / "gate-reports" / subdir / f"{report_id}.json"


def derive_canonical_successor_state_path(
    *,
    microstructure_root: Path,
    dataset_family: str,
    dataset_version: str,
    stage_marker: str,
    phase_id: str,
) -> Path:
    """Return the canonical successor-state ``.json`` path.

    Result::

        <microstructure_root>/successor-state/<canonical_filename>.json
    """
    if not isinstance(microstructure_root, Path):
        raise CanonicalPathError("microstructure_root must be a pathlib.Path")
    name = compose_canonical_successor_state_filename(
        dataset_family=dataset_family,
        dataset_version=dataset_version,
        stage_marker=stage_marker,
        phase_id=phase_id,
    )
    return microstructure_root / "successor-state" / f"{name}.json"


def _resolve_parts(path: Path) -> tuple[str, ...]:
    """Return ``path.resolve().parts`` falling back to ``path.parts`` on OSError."""
    try:
        return tuple(path.resolve(strict=False).parts)
    except OSError:
        return tuple(path.parts)


def _contains_sequence(parts: tuple[str, ...], needle: tuple[str, ...]) -> bool:
    if not needle or len(needle) > len(parts):
        return False
    return any(
        parts[i : i + len(needle)] == needle
        for i in range(len(parts) - len(needle) + 1)
    )


def assert_path_under_microstructure(path: Path, *, label: str = "path") -> None:
    """Fail closed if *path* does not resolve under ``data/microstructure/``."""
    if not isinstance(path, Path):
        raise CanonicalPathError(f"{label} must be a pathlib.Path")
    if not _contains_sequence(_resolve_parts(path), MICROSTRUCTURE_ROOT_PARTS):
        raise CanonicalPathError(
            f"{label} must resolve under data/microstructure/ (got {path})"
        )


def assert_path_under_gate_reports_subdir(
    path: Path,
    *,
    family: str,
    label: str = "path",
) -> None:
    """Fail closed if *path* is not under ``data/microstructure/gate-reports/<family>/``."""
    if not isinstance(path, Path):
        raise CanonicalPathError(f"{label} must be a pathlib.Path")
    subdir = normalize_family(family)
    expected = GATE_REPORTS_ROOT_PARTS + (subdir,)
    if not _contains_sequence(_resolve_parts(path), expected):
        raise CanonicalPathError(
            f"{label} must resolve under data/microstructure/gate-reports/{subdir}/ "
            f"(got {path})"
        )


def assert_path_under_successor_state(
    path: Path,
    *,
    label: str = "path",
) -> None:
    """Fail closed if *path* is not under ``data/microstructure/successor-state/``."""
    if not isinstance(path, Path):
        raise CanonicalPathError(f"{label} must be a pathlib.Path")
    if not _contains_sequence(_resolve_parts(path), SUCCESSOR_STATE_ROOT_PARTS):
        raise CanonicalPathError(
            f"{label} must resolve under data/microstructure/successor-state/ "
            f"(got {path})"
        )


def _validate_sha256_hex(value: str) -> str:
    if not isinstance(value, str):
        raise CanonicalPathError("sha256 hex must be a string")
    if len(value) != 64:
        raise CanonicalPathError(
            f"sha256 hex must be exactly 64 chars (got {len(value)})"
        )
    if not all(c in "0123456789abcdef" for c in value.lower()):
        raise CanonicalPathError("sha256 hex must be lower-case hex")
    return value.lower()


def derive_sidecar_path(json_path: Path) -> Path:
    """Return the canonical ``<json_path>.sha256`` sidecar path."""
    if not isinstance(json_path, Path):
        raise CanonicalPathError("json_path must be a pathlib.Path")
    return json_path.with_suffix(json_path.suffix + ".sha256")


def compose_canonical_sidecar_body(
    *,
    json_sha256_hex: str,
    json_basename: str,
) -> bytes:
    """Return the canonical sidecar body bytes.

    Format: ``<sha>  <basename>\\n`` (two spaces, trailing newline).
    """
    sha = _validate_sha256_hex(json_sha256_hex)
    if not isinstance(json_basename, str) or not json_basename:
        raise CanonicalPathError("json_basename must be a non-empty string")
    if "/" in json_basename or "\\" in json_basename:
        raise CanonicalPathError(
            f"json_basename must not contain path separators (got {json_basename!r})"
        )
    return f"{sha}  {json_basename}\n".encode()


def write_paired_sha256_sidecar(
    *,
    json_path: Path,
    json_sha256_hex: str,
    refuse_overwrite: bool = True,
) -> Path:
    """Write the canonical paired ``.sha256`` sidecar next to *json_path*.

    Sidecar body: ``<sha>  <basename>\\n`` (two spaces, trailing newline).
    Sidecar path: ``<json_path>.sha256``.
    Atomic write-then-rename. Refuses to overwrite by default.

    *json_path* is not required to exist; the caller is responsible for
    ensuring *json_sha256_hex* is the SHA256 hex of the bytes at
    *json_path*. The sidecar parent directory is created if missing.

    Returns the final sidecar path.
    """
    if not isinstance(json_path, Path):
        raise CanonicalPathError("json_path must be a pathlib.Path")
    sidecar_path = derive_sidecar_path(json_path)
    if refuse_overwrite and sidecar_path.exists():
        raise CanonicalPathError(
            f"refusing to overwrite existing sidecar: {sidecar_path}"
        )
    body = compose_canonical_sidecar_body(
        json_sha256_hex=json_sha256_hex,
        json_basename=json_path.name,
    )
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{sidecar_path.name}.",
        suffix=".tmp",
        dir=str(sidecar_path.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(body)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        if refuse_overwrite and sidecar_path.exists():
            raise CanonicalPathError(
                f"refusing to overwrite existing sidecar: {sidecar_path}"
            )
        os.replace(tmp_path, sidecar_path)
    finally:
        if tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()
    return sidecar_path


def compute_file_sha256(path: Path, *, chunk_size: int = 1 << 20) -> str:
    """Return the SHA256 hex digest of *path*, read in chunks."""
    if not isinstance(path, Path):
        raise CanonicalPathError("path must be a pathlib.Path")
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()
