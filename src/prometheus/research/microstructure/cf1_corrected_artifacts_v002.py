"""Phase 4bn-BB — corrected CF-1 artefact writers: deterministic JSON, Parquet, sidecars.

Owns the local (gitignored) artefact surface for the corrected CF-1 substrate-test execution:

- deterministic pretty JSON serialization (sorted keys, ``\\n`` newline) with a paired
  ``.sha256`` sidecar (``<hex-sha256>␠␠<basename>\\n``);
- compact Parquet writers (PyArrow) with paired ``.sha256`` sidecars;
- the canonical filename convention ``<family>__v002__<unix_ms>__<short_commit>.<ext>``;
- the required provenance / governance / non-authorization block stamped into every JSON
  artefact, carrying the full Phase 4bn-BB lineage (base main, BA merge, BA contract tip, AY
  contract tip, AZ historical SHAs);
- an artefact inventory builder and validators.

Output root (must remain gitignored), distinct from the Phase 4bn-AZ v001 root:
``data/research/cf1_corrected_realized_volatility_substrate_test_v002/``.

The target-layer schema carries **exactly two** microstructure snapshot columns
(``rolling_aggtrade_count_60s``, ``rolling_quantity_sum_60s``); the prohibited
``rolling_quantity_mean_60s`` column is never emitted. No network, no credentials, no data
acquisition, no reserve read; writes only inside the BB output root and refuses to write
anywhere else.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from . import cf1_corrected_contract_v002 as cc
from . import cf1_realized_volatility_v001 as cf1

# Local (gitignored) output root and subdirectories (from the corrected contract).
OUTPUT_ROOT_REL = cc.OUTPUT_ROOT_REL
SUBDIRS: tuple[str, ...] = cc.OUTPUT_SUBDIRS

# Artefact families (Phase 4bn-BB §12). All carry the ``cf1_corrected_*_v002`` identity.
FAMILY_SYMBOLIC_PROOF = "cf1_corrected_symbolic_estimability_proof_v002"
FAMILY_TIMESTAMP_PROOF = "cf1_corrected_timestamp_boundary_proof_v002"
FAMILY_ACCESS_START = "cf1_corrected_execution_access_start_v002"
FAMILY_LEAKAGE_PROOF = "cf1_corrected_leakage_split_coverage_proof_v002"
FAMILY_TARGET_LAYER = "cf1_corrected_realized_variance_target_layer_v002"
FAMILY_PAIRED_PREDICTIONS = "cf1_corrected_paired_model_predictions_v002"
FAMILY_MODEL_RUN_MANIFEST = "cf1_corrected_model_run_manifest_v002"
FAMILY_ARTIFACT_INVENTORY = "cf1_corrected_execution_artifact_inventory_v002"

FILENAME_CONTEXT = "v002"

# Governance / non-authorization flags (from the corrected contract; all false).
NON_AUTHORIZATION_FLAGS: dict[str, bool] = dict(cc.NON_AUTHORIZATION_FLAGS)
GOVERNANCE_FLAGS: dict[str, Any] = dict(cc.GOVERNANCE_FLAGS)

# The two target-layer microstructure snapshot columns (no mean column).
TARGET_LAYER_FEATURE_COLUMNS: tuple[str, str] = cc.CORRECTED_FEATURE_COLUMNS


class Cf1CorrectedArtifactError(RuntimeError):
    """Raised when an artefact path, serialization, or sidecar invariant fails closed."""


# ---------------------------------------------------------------------------
# Paths + filenames
# ---------------------------------------------------------------------------


def output_root(repo_root: Path) -> Path:
    return repo_root / OUTPUT_ROOT_REL


def ensure_output_dirs(repo_root: Path) -> Path:
    """Create the BB output root and its subdirectories; return the root path."""
    root = output_root(repo_root)
    root.mkdir(parents=True, exist_ok=True)
    for sub in SUBDIRS:
        (root / sub).mkdir(parents=True, exist_ok=True)
    return root


def _assert_under_output_root(path: Path, repo_root: Path) -> None:
    root = output_root(repo_root).resolve()
    try:
        resolved = path.resolve()
    except OSError as exc:
        raise Cf1CorrectedArtifactError(f"cannot resolve {path}: {exc}") from exc
    if root not in resolved.parents and resolved != root:
        raise Cf1CorrectedArtifactError(f"refusing to write outside BB output root: {path}")


def short_commit(code_commit_sha: str, length: int = 12) -> str:
    if not isinstance(code_commit_sha, str) or len(code_commit_sha) < length:
        raise Cf1CorrectedArtifactError("code_commit_sha too short")
    s = code_commit_sha[:length].lower()
    if not all(c in "0123456789abcdef" for c in s):
        raise Cf1CorrectedArtifactError("code_commit_sha must be hex")
    return s


def compose_filename(
    *, family: str, context: str, unix_ms: int, code_commit_sha: str, ext: str
) -> str:
    """Return ``<family>__<context>__<unix_ms>__<short_commit>.<ext>``."""
    if not family or not context or not ext:
        raise Cf1CorrectedArtifactError("family/context/ext must be non-empty")
    if isinstance(unix_ms, bool) or not isinstance(unix_ms, int) or unix_ms < 0:
        raise Cf1CorrectedArtifactError("unix_ms must be a non-negative int")
    return f"{family}__{context}__{unix_ms}__{short_commit(code_commit_sha)}.{ext}"


# ---------------------------------------------------------------------------
# Hashing + sidecars
# ---------------------------------------------------------------------------


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def compose_sidecar_body(sha_hex: str, basename: str) -> bytes:
    if len(sha_hex) != 64 or not all(c in "0123456789abcdef" for c in sha_hex.lower()):
        raise Cf1CorrectedArtifactError("sha256 must be 64-char hex")
    if "/" in basename or "\\" in basename:
        raise Cf1CorrectedArtifactError("basename must not contain path separators")
    return f"{sha_hex.lower()}  {basename}\n".encode()


def parse_sidecar(text: str) -> tuple[str, str]:
    line = text.strip("\n")
    if "  " not in line:
        raise Cf1CorrectedArtifactError("malformed sidecar (missing two-space separator)")
    sha, name = line.split("  ", 1)
    return sha, name


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            with contextlib.suppress(OSError):
                os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            with contextlib.suppress(OSError):
                tmp.unlink()


def write_sidecar(json_or_parquet_path: Path, sha_hex: str) -> Path:
    sidecar = json_or_parquet_path.with_suffix(json_or_parquet_path.suffix + ".sha256")
    _atomic_write_bytes(sidecar, compose_sidecar_body(sha_hex, json_or_parquet_path.name))
    return sidecar


def canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")


def write_json_with_sidecar(
    path: Path, payload: dict[str, Any], repo_root: Path
) -> tuple[str, Path]:
    """Write deterministic JSON + a paired ``.sha256`` sidecar; return ``(sha, path)``."""
    _assert_under_output_root(path, repo_root)
    data = canonical_json_bytes(payload)
    _atomic_write_bytes(path, data)
    sha = sha256_bytes(data)
    write_sidecar(path, sha)
    return sha, path


def write_parquet_with_sidecar(path: Path, table: pa.Table, repo_root: Path) -> tuple[str, Path]:
    """Write a compact Parquet table + a paired ``.sha256`` sidecar; return ``(sha, path)``."""
    _assert_under_output_root(path, repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, path, compression="zstd")
    sha = sha256_file(path)
    write_sidecar(path, sha)
    return sha, path


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------


def environment_versions() -> dict[str, str]:
    return {
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "pyarrow_version": pa.__version__,
    }


def now_provenance() -> dict[str, Any]:
    now = datetime.now(tz=UTC)
    return {
        "created_at_unix_ms": int(now.timestamp() * 1000),
        "created_at_utc": now.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
    }


def provenance_block(*, code_commit_sha: str, command: str) -> dict[str, Any]:
    """Return the required provenance / governance / non-authorization block."""
    block: dict[str, Any] = {
        **now_provenance(),
        "phase_id": cc.PHASE_ID,
        "symbol": cc.SYMBOL,
        "contract_version": cc.CONTRACT_VERSION,
        "base_main_commit_sha": cc.BASE_MAIN_COMMIT_SHA,
        "phase_4bn_ba_finalization_sha": cc.PHASE_4BN_BA_FINALIZATION_SHA,
        "phase_4bn_ba_merge_commit_sha": cc.PHASE_4BN_BA_MERGE_COMMIT_SHA,
        "phase_4bn_ba_merge_closeout_branch_sha": cc.PHASE_4BN_BA_MERGE_CLOSEOUT_BRANCH_SHA,
        "phase_4bn_ba_contract_tip_sha": cc.PHASE_4BN_BA_CONTRACT_TIP_SHA,
        "phase_4bn_ay_contract_tip_sha": cc.PHASE_4BN_AY_CONTRACT_TIP_SHA,
        "phase_4bn_az_implementation_sha": cc.PHASE_4BN_AZ_IMPLEMENTATION_SHA,
        "phase_4bn_az_merge_commit_sha": cc.PHASE_4BN_AZ_MERGE_COMMIT_SHA,
        "code_commit_sha": code_commit_sha,
        "command": command,
        "feature_list": list(cc.CORRECTED_FEATURE_COLUMNS),
        "feature_count": cc.CORRECTED_FEATURE_COUNT,
        "prohibited_feature": cc.PROHIBITED_FEATURE_COLUMN,
        "allowed_utc_dates": list(cf1.allowed_utc_dates()),
        "allowed_utc_date_count": cc.EXPECTED_ALLOWED_DATE_COUNT,
        "forbidden_utc_ranges": [
            {"reason": reason, "start": lo, "end": hi}
            for reason, lo, hi in cf1.forbidden_date_ranges()
        ],
        "non_authorization_flags": dict(NON_AUTHORIZATION_FLAGS),
    }
    block.update(environment_versions())
    block.update(GOVERNANCE_FLAGS)
    return block


# ---------------------------------------------------------------------------
# Inventory + validation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArtifactEntry:
    family: str
    relative_path: str
    sha256: str
    sidecar: str


def build_inventory(
    *, code_commit_sha: str, command: str, entries: list[ArtifactEntry]
) -> dict[str, Any]:
    payload = provenance_block(code_commit_sha=code_commit_sha, command=command)
    payload["artifact_family"] = FAMILY_ARTIFACT_INVENTORY
    payload["artifact_count"] = len(entries)
    payload["entries"] = [
        {
            "family": e.family,
            "relative_path": e.relative_path,
            "sha256": e.sha256,
            "sidecar": e.sidecar,
        }
        for e in sorted(entries, key=lambda e: e.relative_path)
    ]
    return payload


def validate_json_sidecar(json_path: Path) -> bool:
    """Return True iff ``json_path``'s ``.sha256`` sidecar matches the file bytes + name."""
    sidecar = json_path.with_suffix(json_path.suffix + ".sha256")
    if not json_path.is_file() or not sidecar.is_file():
        raise Cf1CorrectedArtifactError(f"missing artefact or sidecar for {json_path}")
    sha, name = parse_sidecar(sidecar.read_text(encoding="utf-8"))
    return name == json_path.name and sha == sha256_file(json_path)


def validate_no_forbidden_dates_in_list(utc_dates: list[str]) -> bool:
    """Return True iff *utc_dates* contains no forbidden CF-1 date (all openable)."""
    return all(cf1.is_allowed_date(d) for d in utc_dates)


def assert_no_prohibited_feature_in_schema(column_names: list[str]) -> None:
    """Fail closed if the prohibited mean column appears in an emitted schema."""
    if cc.PROHIBITED_FEATURE_COLUMN in column_names:
        raise Cf1CorrectedArtifactError(
            f"prohibited feature {cc.PROHIBITED_FEATURE_COLUMN} present in schema {column_names}"
        )


# ---------------------------------------------------------------------------
# Parquet table builders (compact hourly-origin layer + paired predictions)
# ---------------------------------------------------------------------------


def target_layer_table(rows: list[dict[str, Any]]) -> pa.Table:
    """Build the compact realized-variance target-layer Parquet table (two feature columns)."""
    table = pa.Table.from_pylist(rows)
    assert_no_prohibited_feature_in_schema(table.column_names)
    return table


def paired_predictions_table(rows: list[dict[str, Any]]) -> pa.Table:
    """Build the per-origin paired baseline/augmented prediction + loss Parquet table."""
    table = pa.Table.from_pylist(rows)
    assert_no_prohibited_feature_in_schema(table.column_names)
    return table


__all__ = [
    "FAMILY_ACCESS_START",
    "FAMILY_ARTIFACT_INVENTORY",
    "FAMILY_LEAKAGE_PROOF",
    "FAMILY_MODEL_RUN_MANIFEST",
    "FAMILY_PAIRED_PREDICTIONS",
    "FAMILY_SYMBOLIC_PROOF",
    "FAMILY_TARGET_LAYER",
    "FAMILY_TIMESTAMP_PROOF",
    "FILENAME_CONTEXT",
    "GOVERNANCE_FLAGS",
    "NON_AUTHORIZATION_FLAGS",
    "OUTPUT_ROOT_REL",
    "SUBDIRS",
    "TARGET_LAYER_FEATURE_COLUMNS",
    "ArtifactEntry",
    "Cf1CorrectedArtifactError",
    "assert_no_prohibited_feature_in_schema",
    "build_inventory",
    "canonical_json_bytes",
    "compose_filename",
    "compose_sidecar_body",
    "ensure_output_dirs",
    "environment_versions",
    "now_provenance",
    "output_root",
    "paired_predictions_table",
    "parse_sidecar",
    "provenance_block",
    "sha256_bytes",
    "sha256_file",
    "target_layer_table",
    "validate_json_sidecar",
    "validate_no_forbidden_dates_in_list",
    "write_json_with_sidecar",
    "write_parquet_with_sidecar",
]
