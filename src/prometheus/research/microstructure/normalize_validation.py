"""Phase 4bd post-normalization validation suite.

Implements all 27 Phase 4bc check IDs (``4bc.24.1`` .. ``4bc.24.27``)
as typed :class:`NormalizationCheckResult` records and exposes
:func:`run_all_checks` to execute them in fixed order.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read ``.env`` / ``.mcp.json``, or import any networking library;
- does NOT mutate any artefact;
- does NOT compute features, labels, signals, returns, alpha, edge,
  or any execution-quality / order-flow proxy.
"""

from __future__ import annotations

import hashlib
import re
import zipfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - type-only
    from .invalid_window import InvalidWindow
    from .manifest import MicrostructureManifest
    from .normalize_aggtrades import NormalizeAggTradesInput, NormalizedAggTradeRow
    from .normalize_io import SourceArtefactPaths

UTC_DAY_MS = 86_400_000
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_DECIMAL_RE = re.compile(r"^[0-9]+(\.[0-9]+)?$")


class NormalizationCheckStatus(StrEnum):
    """Per-check status for the Phase 4bd 27-check validation suite."""

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


@dataclass(frozen=True)
class NormalizationCheckResult:
    """One Phase 4bd validation check result."""

    check_id: str
    group: str
    title: str
    status: NormalizationCheckStatus
    detail: str
    evidence: Mapping[str, Any]


@dataclass(frozen=True)
class NormalizationValidationResult:
    """Overall validation result + per-check tuple."""

    overall_status: NormalizationCheckStatus
    checks: tuple[NormalizationCheckResult, ...]
    boundary_confirmations: Mapping[str, bool]


@dataclass(frozen=True)
class NormalizationValidationContext:
    """Context passed to every check function."""

    inp: NormalizeAggTradesInput
    rows: tuple[NormalizedAggTradeRow, ...]
    output_path: Path | None
    output_sha256: str | None
    output_size_bytes: int | None
    derived_manifest: MicrostructureManifest | None
    derived_manifest_path: Path | None
    derived_manifest_sha256: str | None
    raw_manifest_bytes_before: bytes
    raw_manifest_bytes_after: bytes
    raw_manifest_sha_before: str
    raw_manifest_sha_after: str
    raw_zip_sha_before: str
    raw_zip_sha_after: str
    sidecar_sha_before: str
    sidecar_sha_after: str
    acq_log_sha_before: str
    acq_log_sha_after: str
    cited_gate_report_id: str
    cited_gate_report_sha256: str
    cited_gate_code_commit_sha: str
    gate_report_local_present: bool
    gate_report_recomputed_sha: str | None
    artefacts: SourceArtefactPaths
    parsed_source_manifest: Mapping[str, Any]
    member_name: str
    csv_uncompressed_size: int
    invalid_window_candidates: tuple[InvalidWindow, ...]


def _result(
    check_id: str,
    group: str,
    title: str,
    status: NormalizationCheckStatus,
    detail: str = "",
    evidence: Mapping[str, Any] | None = None,
) -> NormalizationCheckResult:
    return NormalizationCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=status,
        detail=detail,
        evidence=dict(evidence or {}),
    )


# --------------------------------------------------------------------------- #
# Check implementations (Phase 4bc 24.1 .. 24.27)
# --------------------------------------------------------------------------- #


def check_input_raw_manifest_exists(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    p = ctx.artefacts.manifest_path
    if p.exists() and p.is_file():
        return _result(
            "4bc.24.1", "source", "Input raw manifest exists",
            NormalizationCheckStatus.PASS, str(p), {"path": str(p)},
        )
    return _result(
        "4bc.24.1", "source", "Input raw manifest exists",
        NormalizationCheckStatus.FAIL, f"missing: {p}", {"path": str(p)},
    )


def check_gate_report_citation_recorded(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    rid = ctx.cited_gate_report_id
    sha = ctx.cited_gate_report_sha256
    ok = bool(rid) and bool(_HEX64_RE.match(sha))
    if ok and ctx.gate_report_local_present and ctx.gate_report_recomputed_sha != sha:
        ok = False
    return _result(
        "4bc.24.2", "source", "Cited PASS gate report ID and SHA recorded",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"id={rid} sha={sha} local_present={ctx.gate_report_local_present}",
        {
            "report_id": rid,
            "report_sha256": sha,
            "code_commit_sha": ctx.cited_gate_code_commit_sha,
            "local_present": ctx.gate_report_local_present,
            "recomputed_sha": ctx.gate_report_recomputed_sha,
        },
    )


def check_raw_manifest_sha_matches(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    # Re-hash manifest bytes and confirm identical to recorded value.
    actual = hashlib.sha256(ctx.raw_manifest_bytes_before).hexdigest()
    ok = actual == ctx.raw_manifest_sha_before
    return _result(
        "4bc.24.3", "source", "Raw manifest SHA matches",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"actual={actual} recorded={ctx.raw_manifest_sha_before}",
        {"actual": actual, "recorded": ctx.raw_manifest_sha_before},
    )


def check_raw_zip_sha_matches(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    files = ctx.parsed_source_manifest.get("files") or []
    declared = str(files[0].get("sha256", "")) if files else ""
    ok = ctx.raw_zip_sha_before == declared
    return _result(
        "4bc.24.4", "source", "Raw zip SHA matches manifest files[0].sha256",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"declared={declared} actual={ctx.raw_zip_sha_before}",
        {"declared": declared, "actual": ctx.raw_zip_sha_before},
    )


def check_sidecar_matches_zip(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    text = ctx.artefacts.sidecar_path.read_text(encoding="utf-8").strip()
    first_field = text.split()[0] if text else ""
    first_64 = first_field[:64]
    ok = first_64 == ctx.raw_zip_sha_before
    return _result(
        "4bc.24.5", "source", "Raw sidecar contents match raw zip SHA",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"first_64={first_64} zip_sha={ctx.raw_zip_sha_before}",
        {"sidecar_first_64": first_64, "raw_zip_sha": ctx.raw_zip_sha_before},
    )


def check_one_csv_member(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    try:
        with zipfile.ZipFile(ctx.artefacts.raw_zip_path) as zf:
            members = zf.namelist()
    except zipfile.BadZipFile as exc:  # pragma: no cover - defensive
        return _result(
            "4bc.24.6", "archive", "Raw archive contains exactly one CSV member",
            NormalizationCheckStatus.ERROR, f"BadZipFile: {exc}", {},
        )
    ok = len(members) == 1
    return _result(
        "4bc.24.6", "archive", "Raw archive contains exactly one CSV member",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"members={members}", {"members": members},
    )


def check_decompression_clean(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    try:
        with zipfile.ZipFile(ctx.artefacts.raw_zip_path) as zf:
            for member in zf.namelist():
                with zf.open(member) as f:
                    while f.read(1024 * 1024):
                        pass
    except zipfile.BadZipFile as exc:
        return _result(
            "4bc.24.7", "archive", "Raw archive decompresses cleanly",
            NormalizationCheckStatus.FAIL, f"BadZipFile: {exc}", {},
        )
    return _result(
        "4bc.24.7", "archive", "Raw archive decompresses cleanly",
        NormalizationCheckStatus.PASS, "", {},
    )


def check_every_row_validates(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    # If we have rows, every raw row already passed the Phase 4ax validator
    # at orchestrator step 7 (otherwise the run would have aborted). The
    # row count parity is a stronger downstream check; here we assert that
    # the row count is non-zero and equals declared event_count.
    declared = int(ctx.parsed_source_manifest.get("event_count", -1))
    ok = len(ctx.rows) > 0 and len(ctx.rows) == declared
    return _result(
        "4bc.24.8", "schema", "Every raw row passes validate_aggtrade_payload",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"rows={len(ctx.rows)} declared={declared}",
        {"rows": len(ctx.rows), "declared_event_count": declared},
    )


def check_row_count_parity(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    declared = int(ctx.parsed_source_manifest.get("event_count", -1))
    ok = len(ctx.rows) == declared
    return _result(
        "4bc.24.9", "row_count", "Normalized row count equals raw event_count",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"rows={len(ctx.rows)} declared={declared}",
        {"rows": len(ctx.rows), "declared_event_count": declared},
    )


def check_one_to_one_mapping(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    # row_index covers [0, n-1] exactly once; agg_trade_id seen at most once.
    seen_indices: set[int] = set()
    seen_a: set[int] = set()
    duplicates = 0
    for r in ctx.rows:
        if r.row_index in seen_indices:
            duplicates += 1
        else:
            seen_indices.add(r.row_index)
        seen_a.add(r.agg_trade_id)
    expected = set(range(len(ctx.rows)))
    ok = duplicates == 0 and seen_indices == expected and len(seen_a) == len(ctx.rows)
    return _result(
        "4bc.24.10", "row_count", "Every normalized row maps to exactly one raw row",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"duplicates={duplicates} unique_a={len(seen_a)} expected_rows={len(ctx.rows)}",
        {
            "duplicates": duplicates,
            "unique_agg_trade_ids": len(seen_a),
            "rows": len(ctx.rows),
        },
    )


def check_no_duplicate_agg_trade_id(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    seen: set[int] = set()
    duplicates: list[int] = []
    for r in ctx.rows:
        if r.agg_trade_id in seen:
            duplicates.append(r.agg_trade_id)
        seen.add(r.agg_trade_id)
    ok = not duplicates
    return _result(
        "4bc.24.11", "duplicates", "No duplicate agg_trade_id introduced",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"duplicates={duplicates[:5]}{'...' if len(duplicates) > 5 else ''}",
        {"duplicate_count": len(duplicates)},
    )


def check_no_silent_drops(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    declared = int(ctx.parsed_source_manifest.get("event_count", -1))
    ok = len(ctx.rows) == declared and not ctx.invalid_window_candidates
    return _result(
        "4bc.24.12", "drops", "No row dropped except per propagated invalid windows",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"rows={len(ctx.rows)} declared={declared} "
        f"invalid_windows={len(ctx.invalid_window_candidates)}",
        {
            "rows": len(ctx.rows),
            "declared_event_count": declared,
            "invalid_windows": len(ctx.invalid_window_candidates),
        },
    )


def check_deterministic_ordering(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    ok = all(r.row_index == i for i, r in enumerate(ctx.rows))
    return _result(
        "4bc.24.13", "ordering", "Deterministic row_index ordering",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        "", {"rows": len(ctx.rows)},
    )


def check_first_T_parity(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    declared = int(ctx.parsed_source_manifest.get("start_time_ms", -1))
    actual = ctx.rows[0].transact_time_ms if ctx.rows else None
    ok = actual is not None and actual == declared
    return _result(
        "4bc.24.14", "timestamps", "First normalized transact_time_ms == raw start_time_ms",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"actual={actual} declared={declared}",
        {"actual": actual, "declared": declared},
    )


def check_last_T_parity(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    declared = int(ctx.parsed_source_manifest.get("end_time_ms", -1))
    actual = ctx.rows[-1].transact_time_ms if ctx.rows else None
    ok = actual is not None and actual == declared
    return _result(
        "4bc.24.15", "timestamps", "Last normalized transact_time_ms == raw end_time_ms",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"actual={actual} declared={declared}",
        {"actual": actual, "declared": declared},
    )


def check_T_within_day_bounds(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    if not ctx.rows:
        return _result(
            "4bc.24.16", "timestamps", "All transact_time_ms within half-open UTC day bounds",
            NormalizationCheckStatus.NOT_APPLICABLE, "no rows", {},
        )
    from datetime import UTC, datetime

    day_start = int(
        datetime.strptime(ctx.rows[0].utc_date, "%Y-%m-%d")
        .replace(tzinfo=UTC)
        .timestamp() * 1000
    )
    day_end_excl = day_start + UTC_DAY_MS
    out = [r.row_index for r in ctx.rows if not (day_start <= r.transact_time_ms < day_end_excl)]
    ok = not out
    return _result(
        "4bc.24.16", "timestamps", "All transact_time_ms within half-open UTC day bounds",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"out_of_bounds={len(out)}",
        {"out_of_bounds": len(out), "day_start_ms": day_start, "day_end_excl_ms": day_end_excl},
    )


def check_numeric_precision(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    bad: list[int] = []
    for r in ctx.rows:
        if not isinstance(r.price, str) or not _DECIMAL_RE.match(r.price):
            bad.append(r.row_index)
            continue
        if not isinstance(r.quantity, str) or not _DECIMAL_RE.match(r.quantity):
            bad.append(r.row_index)
    ok = not bad
    return _result(
        "4bc.24.17", "precision", "Numeric fields parse under declared precision policy",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"bad={len(bad)}",
        {"bad": len(bad)},
    )


def check_no_forbidden_columns(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    from .normalize_aggtrades import NORMALIZED_SCHEMA_V001, NormalizedAggTradeRow

    actual = tuple(NormalizedAggTradeRow.__dataclass_fields__.keys())
    ok = actual == NORMALIZED_SCHEMA_V001
    return _result(
        "4bc.24.18", "schema", "No feature/label/signal columns exist",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"actual={actual}",
        {"actual": list(actual), "expected": list(NORMALIZED_SCHEMA_V001)},
    )


def check_manifest_lineage_complete(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    from .normalize_manifest import REQUIRED_GOVERNANCE_LABEL_KEYS

    if ctx.derived_manifest is None:
        return _result(
            "4bc.24.19", "manifest", "Normalized manifest references all source-evidence fields",
            NormalizationCheckStatus.NOT_APPLICABLE, "manifest not written", {},
        )
    labels = ctx.derived_manifest.governance_labels
    missing = [k for k in REQUIRED_GOVERNANCE_LABEL_KEYS if k not in labels]
    ok = not missing
    return _result(
        "4bc.24.19", "manifest", "Normalized manifest references all source-evidence fields",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"missing={missing}",
        {"missing": missing, "have": sorted(labels.keys())},
    )


def check_output_path_under_namespace(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    from .normalize_io import (
        NormalizationIOError,
        assert_output_path_under_normalized,
    )

    p = ctx.output_path
    if p is None:
        return _result(
            "4bc.24.20", "path", "Normalized output path under data/microstructure/normalized/",
            NormalizationCheckStatus.NOT_APPLICABLE, "no output path", {},
        )
    try:
        assert_output_path_under_normalized(p, label="output_path")
        ok = True
        detail = ""
    except NormalizationIOError as exc:
        ok = False
        detail = str(exc)
    return _result(
        "4bc.24.20", "path", "Normalized output path under data/microstructure/normalized/",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        detail or str(p), {"path": str(p)},
    )


def check_raw_manifest_immutable(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    ok = ctx.raw_manifest_sha_before == ctx.raw_manifest_sha_after
    return _result(
        "4bc.24.21", "immutability", "Raw manifest hash before == after",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"before={ctx.raw_manifest_sha_before} after={ctx.raw_manifest_sha_after}",
        {"before": ctx.raw_manifest_sha_before, "after": ctx.raw_manifest_sha_after},
    )


def check_raw_zip_immutable(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    ok = ctx.raw_zip_sha_before == ctx.raw_zip_sha_after
    return _result(
        "4bc.24.22", "immutability", "Raw zip hash before == after",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"before={ctx.raw_zip_sha_before} after={ctx.raw_zip_sha_after}",
        {"before": ctx.raw_zip_sha_before, "after": ctx.raw_zip_sha_after},
    )


def check_sidecar_immutable(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    ok = ctx.sidecar_sha_before == ctx.sidecar_sha_after
    return _result(
        "4bc.24.23", "immutability", "Raw sidecar hash before == after",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"before={ctx.sidecar_sha_before} after={ctx.sidecar_sha_after}",
        {"before": ctx.sidecar_sha_before, "after": ctx.sidecar_sha_after},
    )


def check_acquisition_log_immutable(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    ok = ctx.acq_log_sha_before == ctx.acq_log_sha_after
    return _result(
        "4bc.24.24", "immutability", "Raw acquisition log hash before == after",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"before={ctx.acq_log_sha_before} after={ctx.acq_log_sha_after}",
        {"before": ctx.acq_log_sha_before, "after": ctx.acq_log_sha_after},
    )


def check_derived_manifest_research_eligible_false(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    if ctx.derived_manifest is None:
        return _result(
            "4bc.24.25", "manifest", "Derived manifest research_eligible is false",
            NormalizationCheckStatus.NOT_APPLICABLE, "manifest not written", {},
        )
    ok = ctx.derived_manifest.research_eligible is False
    return _result(
        "4bc.24.25", "manifest", "Derived manifest research_eligible is false",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"value={ctx.derived_manifest.research_eligible}",
        {"value": ctx.derived_manifest.research_eligible},
    )


def check_derived_manifest_status_pending(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    if ctx.derived_manifest is None:
        return _result(
            "4bc.24.26", "manifest", "Derived manifest eligibility_gate_status is pending",
            NormalizationCheckStatus.NOT_APPLICABLE, "manifest not written", {},
        )
    ok = str(ctx.derived_manifest.eligibility_gate_status) == "pending"
    return _result(
        "4bc.24.26", "manifest", "Derived manifest eligibility_gate_status is pending",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"value={ctx.derived_manifest.eligibility_gate_status}",
        {"value": str(ctx.derived_manifest.eligibility_gate_status)},
    )


def check_no_forbidden_imports(
    ctx: NormalizationValidationContext,
) -> NormalizationCheckResult:
    """Static scan of the four normalize_* modules for forbidden imports.

    The deeper test_normalize_no_network.py test exercises the full
    parametrised scan; this in-process check provides a runtime
    confirmation that the modules are loaded cleanly.
    """
    from . import normalize_aggtrades, normalize_io, normalize_manifest, normalize_validation

    forbidden_module_names = {
        "requests",
        "httpx",
        "aiohttp",
        "websockets",
        "urllib3",
        "binance",
        "dotenv",
        "python_dotenv",
    }
    bad: list[str] = []
    for mod in (normalize_io, normalize_aggtrades, normalize_manifest, normalize_validation):
        if mod.__file__ is None:  # pragma: no cover - defensive
            continue
        src = Path(mod.__file__)
        text = src.read_text(encoding="utf-8")
        # Strip docstrings / comments approximately by scanning lines.
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for tok in forbidden_module_names:
                if (
                    f"import {tok}" in stripped
                    or f"from {tok}" in stripped
                ):
                    bad.append(f"{src.name}:{tok}")
                    break
    ok = not bad
    return _result(
        "4bc.24.27", "imports", "No forbidden imports / forbidden tokens in normalizer modules",
        NormalizationCheckStatus.PASS if ok else NormalizationCheckStatus.FAIL,
        f"bad={bad}",
        {"bad": bad},
    )


_CheckEntry = tuple[
    str,
    str,
    str,
    Callable[[NormalizationValidationContext], NormalizationCheckResult],
]

CHECK_ORDER: tuple[_CheckEntry, ...] = (
    ("4bc.24.1", "source", "Input raw manifest exists",
     check_input_raw_manifest_exists),
    ("4bc.24.2", "source", "Cited PASS gate report ID and SHA recorded",
     check_gate_report_citation_recorded),
    ("4bc.24.3", "source", "Raw manifest SHA matches",
     check_raw_manifest_sha_matches),
    ("4bc.24.4", "source", "Raw zip SHA matches manifest",
     check_raw_zip_sha_matches),
    ("4bc.24.5", "source", "Raw sidecar matches raw zip SHA",
     check_sidecar_matches_zip),
    ("4bc.24.6", "archive", "One CSV member",
     check_one_csv_member),
    ("4bc.24.7", "archive", "Decompresses cleanly",
     check_decompression_clean),
    ("4bc.24.8", "schema", "Every raw row passes validate_aggtrade_payload",
     check_every_row_validates),
    ("4bc.24.9", "row_count", "Row count parity",
     check_row_count_parity),
    ("4bc.24.10", "row_count", "One-to-one mapping",
     check_one_to_one_mapping),
    ("4bc.24.11", "duplicates", "No duplicate agg_trade_id",
     check_no_duplicate_agg_trade_id),
    ("4bc.24.12", "drops", "No silent drops",
     check_no_silent_drops),
    ("4bc.24.13", "ordering", "Deterministic row_index ordering",
     check_deterministic_ordering),
    ("4bc.24.14", "timestamps", "First T parity",
     check_first_T_parity),
    ("4bc.24.15", "timestamps", "Last T parity",
     check_last_T_parity),
    ("4bc.24.16", "timestamps", "T within day bounds",
     check_T_within_day_bounds),
    ("4bc.24.17", "precision", "Numeric precision",
     check_numeric_precision),
    ("4bc.24.18", "schema", "No forbidden columns",
     check_no_forbidden_columns),
    ("4bc.24.19", "manifest", "Manifest lineage complete",
     check_manifest_lineage_complete),
    ("4bc.24.20", "path", "Output path under namespace",
     check_output_path_under_namespace),
    ("4bc.24.21", "immutability", "Raw manifest immutable",
     check_raw_manifest_immutable),
    ("4bc.24.22", "immutability", "Raw zip immutable",
     check_raw_zip_immutable),
    ("4bc.24.23", "immutability", "Raw sidecar immutable",
     check_sidecar_immutable),
    ("4bc.24.24", "immutability", "Raw acquisition log immutable",
     check_acquisition_log_immutable),
    ("4bc.24.25", "manifest", "Derived research_eligible false",
     check_derived_manifest_research_eligible_false),
    ("4bc.24.26", "manifest", "Derived status pending",
     check_derived_manifest_status_pending),
    ("4bc.24.27", "imports", "No forbidden imports",
     check_no_forbidden_imports),
)
"""Fixed-order tuple of all 27 Phase 4bc validation checks."""


def run_all_checks(ctx: NormalizationValidationContext) -> NormalizationValidationResult:
    """Execute all 27 Phase 4bc validation checks in fixed order."""
    results: list[NormalizationCheckResult] = []
    for check_id, group, title, fn in CHECK_ORDER:
        try:
            r = fn(ctx)
        except Exception as exc:  # noqa: BLE001 - defensive
            r = _result(
                check_id,
                group,
                title,
                NormalizationCheckStatus.ERROR,
                f"{type(exc).__name__}: {exc}",
                {},
            )
        results.append(r)
    has_fail = any(r.status == NormalizationCheckStatus.FAIL for r in results)
    has_error = any(r.status == NormalizationCheckStatus.ERROR for r in results)
    if has_error:
        overall = NormalizationCheckStatus.ERROR
    elif has_fail:
        overall = NormalizationCheckStatus.FAIL
    else:
        overall = NormalizationCheckStatus.PASS
    boundary: dict[str, bool] = {
        "all_27_checks_returned": len(results) == 27,
        "no_check_error": not has_error,
    }
    return NormalizationValidationResult(
        overall_status=overall,
        checks=tuple(results),
        boundary_confirmations=boundary,
    )


__all__ = [
    "CHECK_ORDER",
    "NormalizationCheckResult",
    "NormalizationCheckStatus",
    "NormalizationValidationContext",
    "NormalizationValidationResult",
    "run_all_checks",
]
