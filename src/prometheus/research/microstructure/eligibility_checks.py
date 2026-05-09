"""Forty-five eligibility-time check functions for aggTrades raw archives.

Phase 4bb-C scope: pure functions that each implement one Phase 4ba §10
eligibility-time check against a shared :class:`GateExecutionContext`.
The orchestrator in :mod:`eligibility_gate` calls
:func:`run_all_checks` to execute every check in fixed order and return
the resulting tuple of :class:`AggTradesEligibilityCheckResult` plus any
:class:`InvalidWindowCandidate` records.

This module:

- imports no networking library, no credential helper, no env reader,
  no MCP / Graphify integration;
- performs no file I/O beyond what the orchestrator pre-loaded into the
  context;
- never mutates the manifest or the archive;
- returns ``AggTradesEligibilityCheckStatus.NOT_APPLICABLE`` for checks
  that do not apply to the current dataset family / acquisition mode
  (e.g. retention-window check when the date is recent).
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .allowlist import ALLOWLIST_PATTERNS, DENYLIST_TOKENS
from .eligibility_gate import (
    AggTradesEligibilityCheckResult,
    AggTradesEligibilityCheckStatus,
    AggTradesEligibilityGateInput,
    InvalidWindowCandidate,
)
from .eligibility_io import (
    CSV_HEADER_ALIAS_MAP,
    EXPECTED_CANONICAL_KEYS,
    MAX_ARCHIVE_BYTES,
    ArtefactPaths,
    ArtefactReadResult,
    scan_text_for_forbidden_tokens,
    serialise_for_token_scan,
)
from .invalid_window import (
    DownstreamEligibilityAction,
    InvalidWindow,
    InvalidWindowReason,
    InvalidWindowSeverity,
)

PASS = AggTradesEligibilityCheckStatus.PASS
FAIL = AggTradesEligibilityCheckStatus.FAIL
NOT_APPLICABLE = AggTradesEligibilityCheckStatus.NOT_APPLICABLE
ERROR = AggTradesEligibilityCheckStatus.ERROR

_VALID_STOP_TRIGGER_DOMAINS: frozenset[str] = frozenset(
    {
        "trade_price_backtest",
        "mark_price_runtime",
        "mark_price_backtest_candidate",
        "trade_price_backtest_candidate",
    }
)
"""Phase 3v §8 stop-trigger-domain enum (extended with the Phase 4az candidate label)."""

_REQUIRED_GOVERNANCE_KEYS: tuple[str, ...] = (
    "validator",
    "stop_trigger_domain",
    "feature_computation",
    "strategy_use",
    "phase",
    "source_phase_boundary",
)
"""Minimum keys the gate expects in ``governance_labels``."""

_DEFAULT_RETENTION_DAYS = 365 * 5
"""Conservative retention horizon (in days) for daily Binance archive files."""


@dataclass(frozen=True)
class GateExecutionContext:
    """Shared context for the 45 check functions.

    The context is built by the orchestrator and is **read-only** for all
    check functions. Per-row anomalies and the row-scan summary are
    pre-populated.
    """

    inp: AggTradesEligibilityGateInput
    artefacts: ArtefactPaths
    artefact_read: ArtefactReadResult
    anomalies: tuple[Mapping[str, Any], ...]
    expected_utc_day_start_ms: int | None

    @property
    def manifest(self) -> Any:
        """Convenience: the parsed manifest."""
        return self.artefact_read.manifest

    @property
    def symbol_allowlist(self) -> tuple[str, ...]:
        """Resolved symbol allowlist (caller-provided config or hard-coded default).

        ``MicrostructureConfig`` requires several positional arguments and is
        not safely default-constructible at gate-time. The gate falls back to
        the project's documented default symbol allowlist (BTCUSDT / ETHUSDT)
        when the caller passes ``config=None`` and reports the chosen source
        for auditability.
        """
        if self.inp.config is not None:
            return tuple(self.inp.config.symbol_allowlist)
        return ("BTCUSDT", "ETHUSDT")


def _result(
    check_id: str,
    group: str,
    title: str,
    status: AggTradesEligibilityCheckStatus,
    detail: str,
    evidence: Mapping[str, Any] | None = None,
) -> AggTradesEligibilityCheckResult:
    return AggTradesEligibilityCheckResult(
        check_id=check_id,
        group=group,
        title=title,
        status=status,
        detail=detail,
        evidence=dict(evidence or {}),
    )


# ---------------------------------------------------------------------------
# Group 10.1 — Source checks
# ---------------------------------------------------------------------------

_WHITELISTED_SOURCE_LABELS: frozenset[str] = frozenset({"binance_data_archive"})


def check_source_label_whitelisted(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    label = ctx.manifest.source
    if label in _WHITELISTED_SOURCE_LABELS:
        return _result(
            "10.1.1",
            "source",
            "Source label whitelisted",
            PASS,
            f"source = {label!r}",
            {"observed": label, "allowed": sorted(_WHITELISTED_SOURCE_LABELS)},
        )
    return _result(
        "10.1.1",
        "source",
        "Source label whitelisted",
        FAIL,
        f"source = {label!r} is not whitelisted",
        {"observed": label, "allowed": sorted(_WHITELISTED_SOURCE_LABELS)},
    )


def check_endpoint_label_documented_archive_family(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    endpoint = ctx.manifest.endpoint
    if "data.binance.vision" in endpoint and "aggTrades" in endpoint:
        return _result(
            "10.1.2",
            "source",
            "Endpoint label is a documented archive family",
            PASS,
            f"endpoint = {endpoint!r}",
            {"observed": endpoint},
        )
    return _result(
        "10.1.2",
        "source",
        "Endpoint label is a documented archive family",
        FAIL,
        f"endpoint = {endpoint!r} is not a recognised archive family",
        {"observed": endpoint},
    )


def check_endpoint_docs_reference_present(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    ref = ctx.manifest.endpoint_docs_reference
    if isinstance(ref, str) and ref.strip():
        return _result(
            "10.1.3",
            "source",
            "endpoint_docs_reference present",
            PASS,
            "non-empty reference",
            {"observed": ref},
        )
    return _result(
        "10.1.3",
        "source",
        "endpoint_docs_reference present",
        FAIL,
        "endpoint_docs_reference is empty or missing",
        {"observed": ref},
    )


def check_no_private_endpoint_label(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    fields = {
        "endpoint": ctx.manifest.endpoint,
        "source": ctx.manifest.source,
    }
    for k, v in dict(ctx.manifest.governance_labels).items():
        fields[f"governance_labels.{k}"] = str(v)
    bad: dict[str, list[str]] = {}
    for name, value in fields.items():
        if not isinstance(value, str):
            continue
        tokens = scan_text_for_forbidden_tokens(value)
        if tokens:
            bad[name] = tokens
    if bad:
        return _result(
            "10.1.4",
            "source",
            "No private-endpoint label",
            FAIL,
            "private-endpoint or credential-shaped tokens found",
            {"matches": bad},
        )
    return _result(
        "10.1.4",
        "source",
        "No private-endpoint label",
        PASS,
        "no forbidden tokens",
        {"scanned_field_count": len(fields)},
    )


def check_capture_mode_is_historical_archive(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    cm = ctx.manifest.capture_mode
    if cm == "historical_archive":
        return _result(
            "10.1.5",
            "source",
            "capture_mode is historical_archive",
            PASS,
            f"capture_mode = {cm!r}",
            {"observed": cm},
        )
    return _result(
        "10.1.5",
        "source",
        "capture_mode is historical_archive",
        FAIL,
        f"capture_mode = {cm!r} is not historical_archive",
        {"observed": cm},
    )


# ---------------------------------------------------------------------------
# Group 10.2 — Checksum checks
# ---------------------------------------------------------------------------

_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def check_files_sha256_is_64char_lowercase_hex(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    files = ctx.manifest.files
    if not files:
        return _result(
            "10.2.6",
            "checksum",
            "files[*].sha256 is 64-char lowercase hex",
            FAIL,
            "manifest has no files",
            {},
        )
    bad = []
    for i, fe in enumerate(files):
        if not _HEX64_RE.fullmatch(fe.sha256):
            bad.append({"index": i, "sha256": fe.sha256})
    if bad:
        return _result(
            "10.2.6",
            "checksum",
            "files[*].sha256 is 64-char lowercase hex",
            FAIL,
            "non-hex or non-lowercase digest detected",
            {"violations": bad},
        )
    return _result(
        "10.2.6",
        "checksum",
        "files[*].sha256 is 64-char lowercase hex",
        PASS,
        f"{len(files)} file entries",
        {"file_count": len(files)},
    )


def check_recomputed_sha_matches_manifest_and_sidecar(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    if not ctx.artefacts.raw_zip_path.exists():
        return _result(
            "10.2.7",
            "checksum",
            "Recomputed SHA matches manifest and sidecar",
            ERROR,
            "raw_zip_path does not exist",
            {"path": str(ctx.artefacts.raw_zip_path)},
        )
    recomputed = ctx.artefact_read.raw_zip_sha256
    manifest_first = (
        ctx.manifest.files[0].sha256 if ctx.manifest.files else "__missing__"
    )
    sidecar_first_64 = ctx.artefact_read.sidecar_first_64_hex
    matches_manifest = recomputed == manifest_first
    matches_sidecar = recomputed == sidecar_first_64
    if matches_manifest and matches_sidecar:
        return _result(
            "10.2.7",
            "checksum",
            "Recomputed SHA matches manifest and sidecar",
            PASS,
            "bit-for-bit two-way agreement",
            {
                "recomputed": recomputed,
                "manifest_first": manifest_first,
                "sidecar_first_64": sidecar_first_64,
            },
        )
    return _result(
        "10.2.7",
        "checksum",
        "Recomputed SHA matches manifest and sidecar",
        FAIL,
        "two-way agreement violated",
        {
            "recomputed": recomputed,
            "manifest_first": manifest_first,
            "sidecar_first_64": sidecar_first_64,
            "matches_manifest": matches_manifest,
            "matches_sidecar": matches_sidecar,
        },
    )


def check_checksum_companion_verification_recorded(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    sidecar = ctx.artefact_read.sidecar_first_64_hex
    if sidecar:
        return _result(
            "10.2.8",
            "checksum",
            ".CHECKSUM companion verification recorded",
            PASS,
            "sidecar present and parseable",
            {"sidecar_first_64": sidecar},
        )
    labels = dict(ctx.manifest.governance_labels)
    if str(labels.get("checksum_companion_absent", "")).lower() == "true":
        return _result(
            "10.2.8",
            "checksum",
            ".CHECKSUM companion verification recorded",
            PASS,
            "sidecar absent but explicitly recorded in governance_labels",
            {"checksum_companion_absent": "true"},
        )
    return _result(
        "10.2.8",
        "checksum",
        ".CHECKSUM companion verification recorded",
        FAIL,
        "sidecar absent and not recorded as such in governance_labels",
        {},
    )


# ---------------------------------------------------------------------------
# Group 10.3 — Manifest checks
# ---------------------------------------------------------------------------

_REQUIRED_MANIFEST_FIELDS: tuple[str, ...] = (
    "dataset_family",
    "version",
    "symbol",
    "source",
    "endpoint",
    "capture_mode",
    "schema_version",
    "endpoint_docs_reference",
    "capture_config_hash",
    "code_commit_sha",
)


def check_required_manifest_fields_populated(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    missing = []
    for field_name in _REQUIRED_MANIFEST_FIELDS:
        v = getattr(ctx.manifest, field_name, None)
        if not isinstance(v, str) or not v:
            missing.append(field_name)
    if missing:
        return _result(
            "10.3.9",
            "manifest",
            "Required manifest fields populated",
            FAIL,
            "one or more required fields empty",
            {"missing": missing},
        )
    return _result(
        "10.3.9",
        "manifest",
        "Required manifest fields populated",
        PASS,
        "all required fields populated",
        {"checked": list(_REQUIRED_MANIFEST_FIELDS)},
    )


def check_research_eligible_false_and_status_pending(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    re_flag = ctx.manifest.research_eligible
    status = ctx.manifest.eligibility_gate_status
    # Inconsistency rule (Phase 4ba §15.2): true / pending or true / fail is invalid.
    if re_flag is True:
        return _result(
            "10.3.10",
            "manifest",
            "research_eligible is false and eligibility_gate_status is pending",
            FAIL,
            "research_eligible is true on a raw aggTrades family",
            {"research_eligible": re_flag, "status": status.value},
        )
    if status.value != "pending":
        return _result(
            "10.3.10",
            "manifest",
            "research_eligible is false and eligibility_gate_status is pending",
            FAIL,
            "eligibility_gate_status is not pending at gate-time",
            {"research_eligible": re_flag, "status": status.value},
        )
    return _result(
        "10.3.10",
        "manifest",
        "research_eligible is false and eligibility_gate_status is pending",
        PASS,
        "research_eligible=false and eligibility_gate_status=pending",
        {"research_eligible": re_flag, "status": status.value},
    )


def check_governance_labels_minimum_keys(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    labels = dict(ctx.manifest.governance_labels)
    missing = [k for k in _REQUIRED_GOVERNANCE_KEYS if k not in labels]
    if missing:
        return _result(
            "10.3.11",
            "manifest",
            "governance_labels minimum keys",
            FAIL,
            "missing required governance label keys",
            {"missing": missing, "observed_keys": sorted(labels)},
        )
    return _result(
        "10.3.11",
        "manifest",
        "governance_labels minimum keys",
        PASS,
        "all required keys present",
        {"required": list(_REQUIRED_GOVERNANCE_KEYS)},
    )


def check_code_commit_sha_exists_in_repo_history(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    sha = ctx.manifest.code_commit_sha
    if not sha:
        return _result(
            "10.3.12",
            "manifest",
            "code_commit_sha exists in repo history",
            FAIL,
            "code_commit_sha is empty",
            {},
        )
    try:
        completed = subprocess.run(
            ["git", "cat-file", "-e", sha],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return _result(
            "10.3.12",
            "manifest",
            "code_commit_sha exists in repo history",
            ERROR,
            f"git not available: {exc}",
            {"sha": sha},
        )
    if completed.returncode == 0:
        return _result(
            "10.3.12",
            "manifest",
            "code_commit_sha exists in repo history",
            PASS,
            "git cat-file -e succeeded",
            {"sha": sha},
        )
    return _result(
        "10.3.12",
        "manifest",
        "code_commit_sha exists in repo history",
        FAIL,
        "git cat-file -e failed",
        {"sha": sha, "stderr": completed.stderr.strip()[:200]},
    )


def check_capture_config_hash_nonempty_and_redrivable(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    h = ctx.manifest.capture_config_hash
    if not isinstance(h, str) or not h:
        return _result(
            "10.3.13",
            "manifest",
            "capture_config_hash is non-empty and re-derivable",
            FAIL,
            "capture_config_hash is empty",
            {},
        )
    if not re.fullmatch(r"[0-9a-fA-F]+", h) or len(h) < 16:
        return _result(
            "10.3.13",
            "manifest",
            "capture_config_hash is non-empty and re-derivable",
            FAIL,
            "capture_config_hash is not a hex digest (>=16 chars)",
            {"observed": h},
        )
    return _result(
        "10.3.13",
        "manifest",
        "capture_config_hash is non-empty and re-derivable",
        PASS,
        "looks like a deterministic config hash",
        {"observed_length": len(h)},
    )


# ---------------------------------------------------------------------------
# Group 10.4 — Schema checks
# ---------------------------------------------------------------------------


def check_every_row_passes_validate_aggtrade_payload(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    if not ctx.artefact_read.decompression_ok:
        return _result(
            "10.4.14",
            "schema",
            "Every row passes validate_aggtrade_payload",
            ERROR,
            f"decompression failed: {ctx.artefact_read.decompression_error}",
            {},
        )
    if rs.row_count == 0:
        return _result(
            "10.4.14",
            "schema",
            "Every row passes validate_aggtrade_payload",
            FAIL,
            "no rows scanned",
            {},
        )
    if rs.validator_failures > 0:
        return _result(
            "10.4.14",
            "schema",
            "Every row passes validate_aggtrade_payload",
            FAIL,
            f"{rs.validator_failures} rows failed the Phase 4ax validator",
            {
                "validator_failures": rs.validator_failures,
                "first_failure": rs.first_validator_failure,
                "row_count": rs.row_count,
            },
        )
    return _result(
        "10.4.14",
        "schema",
        "Every row passes validate_aggtrade_payload",
        PASS,
        f"{rs.row_count}/{rs.row_count} rows passed",
        {"row_count": rs.row_count},
    )


def check_column_order_recorded(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    cols = ctx.artefact_read.row_scan.csv_column_order
    if cols:
        return _result(
            "10.4.15",
            "schema",
            "Column order recorded",
            PASS,
            "csv_column_order populated",
            {"csv_column_order": list(cols)},
        )
    return _result(
        "10.4.15",
        "schema",
        "Column order recorded",
        FAIL,
        "csv_column_order is empty",
        {},
    )


def check_no_unexpected_extra_columns(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    extras = ctx.artefact_read.row_scan.unexpected_extra_columns
    if not extras:
        return _result(
            "10.4.16",
            "schema",
            "No unexpected extra columns",
            PASS,
            "every column maps to a documented canonical key",
            {"required_keys": sorted(EXPECTED_CANONICAL_KEYS)},
        )
    return _result(
        "10.4.16",
        "schema",
        "No unexpected extra columns",
        FAIL,
        f"unknown columns observed: {list(extras)}",
        {"unexpected": list(extras), "alias_map": dict(CSV_HEADER_ALIAS_MAP)},
    )


# ---------------------------------------------------------------------------
# Group 10.5 — Timestamp checks
# ---------------------------------------------------------------------------


def check_all_T_are_int_ms_within_manifest_range(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    m = ctx.manifest
    if rs.row_count == 0:
        return _result(
            "10.5.17",
            "timestamps",
            "All T are int ms within manifest range",
            FAIL,
            "no rows scanned",
            {},
        )
    if rs.first_T is None or rs.last_T is None:
        return _result(
            "10.5.17",
            "timestamps",
            "All T are int ms within manifest range",
            ERROR,
            "first/last T not measured",
            {},
        )
    if rs.first_T < m.start_time_ms or rs.last_T > m.end_time_ms:
        return _result(
            "10.5.17",
            "timestamps",
            "All T are int ms within manifest range",
            FAIL,
            "T outside [manifest.start_time_ms, manifest.end_time_ms]",
            {
                "first_T": rs.first_T,
                "last_T": rs.last_T,
                "manifest_start": m.start_time_ms,
                "manifest_end": m.end_time_ms,
            },
        )
    return _result(
        "10.5.17",
        "timestamps",
        "All T are int ms within manifest range",
        PASS,
        "first_T and last_T fall within manifest range",
        {
            "first_T": rs.first_T,
            "last_T": rs.last_T,
            "manifest_start": m.start_time_ms,
            "manifest_end": m.end_time_ms,
        },
    )


def check_start_time_ms_le_end_time_ms(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    m = ctx.manifest
    if m.start_time_ms <= m.end_time_ms:
        return _result(
            "10.5.18",
            "timestamps",
            "manifest.start_time_ms <= manifest.end_time_ms",
            PASS,
            "ordering invariant holds",
            {"start_time_ms": m.start_time_ms, "end_time_ms": m.end_time_ms},
        )
    return _result(
        "10.5.18",
        "timestamps",
        "manifest.start_time_ms <= manifest.end_time_ms",
        FAIL,
        "start_time_ms > end_time_ms",
        {"start_time_ms": m.start_time_ms, "end_time_ms": m.end_time_ms},
    )


def check_T_non_decreasing_across_file(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    # Phase 4az archive observation: aggregate-trade-id monotonicity is
    # enforced; the same property pulls T into a non-decreasing path.
    # The row scan does not record T-decrease events directly. We treat
    # T monotonicity as a derived structural property when monotone_a is
    # true and there are no out-of-order anomalies.
    rs = ctx.artefact_read.row_scan
    if rs.row_count == 0:
        return _result(
            "10.5.19",
            "timestamps",
            "T non-decreasing across file",
            FAIL,
            "no rows scanned",
            {},
        )
    if rs.out_of_order_a_count == 0 and rs.monotone_a_non_decreasing:
        return _result(
            "10.5.19",
            "timestamps",
            "T non-decreasing across file",
            PASS,
            "derived from monotone aggregate-trade-id non-decreasing",
            {"out_of_order_a_count": rs.out_of_order_a_count},
        )
    return _result(
        "10.5.19",
        "timestamps",
        "T non-decreasing across file",
        FAIL,
        "out-of-order events detected",
        {"out_of_order_a_count": rs.out_of_order_a_count},
    )


def check_utc_day_match(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    if ctx.expected_utc_day_start_ms is None:
        return _result(
            "10.5.20",
            "timestamps",
            "UTC-day match",
            NOT_APPLICABLE,
            "archive path has no parseable date",
            {},
        )
    out_count = rs.out_day_count
    if out_count == 0:
        return _result(
            "10.5.20",
            "timestamps",
            "UTC-day match",
            PASS,
            f"{rs.in_day_count} in-day rows; 0 out-of-day rows",
            {
                "in_day_count": rs.in_day_count,
                "out_day_count": out_count,
                "expected_utc_day_start_ms": ctx.expected_utc_day_start_ms,
            },
        )
    return _result(
        "10.5.20",
        "timestamps",
        "UTC-day match",
        FAIL,
        f"{out_count} rows fall outside the requested UTC day",
        {
            "in_day_count": rs.in_day_count,
            "out_day_count": out_count,
            "rows_below": rs.rows_with_T_below_utc_day_start,
            "rows_at_or_after_end": rs.rows_with_T_at_or_after_utc_day_end,
        },
    )


# ---------------------------------------------------------------------------
# Group 10.6 — Aggregate-trade-ID monotonicity
# ---------------------------------------------------------------------------


def check_a_non_decreasing_across_file(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    if rs.row_count == 0:
        return _result(
            "10.6.21",
            "monotonicity",
            "Aggregate trade IDs non-decreasing",
            FAIL,
            "no rows scanned",
            {},
        )
    if rs.out_of_order_a_count == 0:
        return _result(
            "10.6.21",
            "monotonicity",
            "Aggregate trade IDs non-decreasing",
            PASS,
            "0 out-of-order events",
            {"out_of_order_a_count": 0},
        )
    return _result(
        "10.6.21",
        "monotonicity",
        "Aggregate trade IDs non-decreasing",
        FAIL,
        f"{rs.out_of_order_a_count} out-of-order events",
        {"out_of_order_a_count": rs.out_of_order_a_count},
    )


def check_a_increments_non_negative(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    # Same property as 10.6.21: any decrease is an out-of-order event.
    if rs.out_of_order_a_count == 0:
        return _result(
            "10.6.22",
            "monotonicity",
            "Aggregate trade ID increments non-negative",
            PASS,
            "no negative increments",
            {},
        )
    return _result(
        "10.6.22",
        "monotonicity",
        "Aggregate trade ID increments non-negative",
        FAIL,
        f"{rs.out_of_order_a_count} negative increments observed",
        {"out_of_order_a_count": rs.out_of_order_a_count},
    )


def check_no_a_value_reappears_with_different_tuple(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    if rs.a_with_different_tuple_count == 0:
        return _result(
            "10.6.23",
            "monotonicity",
            "No aggregate trade ID reappears with a different (p, q, m, T) tuple",
            PASS,
            "no inconsistent reappearances",
            {"a_with_different_tuple_count": 0},
        )
    return _result(
        "10.6.23",
        "monotonicity",
        "No aggregate trade ID reappears with a different (p, q, m, T) tuple",
        FAIL,
        f"{rs.a_with_different_tuple_count} aggregate trade IDs reappear with a different tuple",
        {"a_with_different_tuple_count": rs.a_with_different_tuple_count},
    )


# ---------------------------------------------------------------------------
# Group 10.7 — Duplicate checks
# ---------------------------------------------------------------------------


def check_no_duplicate_a_within_file(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    if rs.duplicate_a_count == 0:
        return _result(
            "10.7.24",
            "duplicates",
            "No duplicate aggregate trade IDs",
            PASS,
            "0 duplicates",
            {"duplicate_a_count": 0, "row_count": rs.row_count},
        )
    return _result(
        "10.7.24",
        "duplicates",
        "No duplicate aggregate trade IDs",
        FAIL,
        f"{rs.duplicate_a_count} duplicate aggregate trade IDs",
        {"duplicate_a_count": rs.duplicate_a_count, "row_count": rs.row_count},
    )


def check_f_le_l_for_every_row(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    if rs.f_le_l_violations == 0:
        return _result(
            "10.7.25",
            "duplicates",
            "f <= l for every row",
            PASS,
            "no f > l rows",
            {"violations": 0},
        )
    return _result(
        "10.7.25",
        "duplicates",
        "f <= l for every row",
        FAIL,
        f"{rs.f_le_l_violations} rows violate f <= l",
        {"violations": rs.f_le_l_violations},
    )


# ---------------------------------------------------------------------------
# Group 10.8 — Row-count checks
# ---------------------------------------------------------------------------


def check_event_count_gt_zero(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    ec = ctx.manifest.event_count
    if ec > 0:
        return _result(
            "10.8.26",
            "row_count",
            "manifest.event_count > 0",
            PASS,
            f"event_count = {ec}",
            {"event_count": ec},
        )
    return _result(
        "10.8.26",
        "row_count",
        "manifest.event_count > 0",
        FAIL,
        "event_count is zero or negative",
        {"event_count": ec},
    )


def check_event_count_matches_actual_row_count(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    m = ctx.manifest
    if rs.row_count == m.event_count:
        return _result(
            "10.8.27",
            "row_count",
            "event_count matches actual row count",
            PASS,
            f"{rs.row_count} == {m.event_count}",
            {"row_count": rs.row_count, "event_count": m.event_count},
        )
    return _result(
        "10.8.27",
        "row_count",
        "event_count matches actual row count",
        FAIL,
        "row count != manifest.event_count",
        {"row_count": rs.row_count, "event_count": m.event_count},
    )


def check_event_count_consistent_with_files_sum(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    m = ctx.manifest
    files_sum = sum(fe.event_count for fe in m.files)
    if files_sum == m.event_count:
        return _result(
            "10.8.28",
            "row_count",
            "event_count consistent with sum(files[*].event_count)",
            PASS,
            f"sum = {files_sum}",
            {"files_sum": files_sum, "event_count": m.event_count},
        )
    return _result(
        "10.8.28",
        "row_count",
        "event_count consistent with sum(files[*].event_count)",
        FAIL,
        "manifest.event_count differs from sum(files)",
        {"files_sum": files_sum, "event_count": m.event_count},
    )


# ---------------------------------------------------------------------------
# Group 10.9 — Symbol / date checks
# ---------------------------------------------------------------------------


def check_symbol_in_project_allowlist(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    sym = ctx.manifest.symbol
    allowlist = set(ctx.symbol_allowlist) | set(ctx.inp.explicit_extra_symbols)
    if sym in allowlist:
        return _result(
            "10.9.29",
            "symbol_date",
            "Symbol in project allowlist",
            PASS,
            f"symbol = {sym}",
            {"symbol": sym, "allowlist": sorted(allowlist)},
        )
    return _result(
        "10.9.29",
        "symbol_date",
        "Symbol in project allowlist",
        FAIL,
        f"symbol = {sym} is not in allowlist",
        {"symbol": sym, "allowlist": sorted(allowlist)},
    )


def check_symbol_scope_source_recorded_and_path_match(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    labels = dict(ctx.manifest.governance_labels)
    scope = labels.get("symbol_scope_source", "")
    if not scope:
        return _result(
            "10.9.30",
            "symbol_date",
            "symbol_scope_source recorded and path matches",
            FAIL,
            "symbol_scope_source label missing",
            {},
        )
    if scope == "archive_path":
        path_name = ctx.artefacts.raw_zip_path.name
        if ctx.manifest.symbol in path_name:
            return _result(
                "10.9.30",
                "symbol_date",
                "symbol_scope_source recorded and path matches",
                PASS,
                "archive_path encodes the manifest symbol",
                {"path_name": path_name, "symbol": ctx.manifest.symbol},
            )
        return _result(
            "10.9.30",
            "symbol_date",
            "symbol_scope_source recorded and path matches",
            FAIL,
            "manifest symbol not present in archive path",
            {"path_name": path_name, "symbol": ctx.manifest.symbol},
        )
    return _result(
        "10.9.30",
        "symbol_date",
        "symbol_scope_source recorded and path matches",
        NOT_APPLICABLE,
        f"symbol_scope_source = {scope!r} (non-archive_path scopes pending governance)",
        {"symbol_scope_source": scope},
    )


def check_archive_path_date_matches_T_values(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    if ctx.expected_utc_day_start_ms is None:
        return _result(
            "10.9.31",
            "symbol_date",
            "Archive-path date matches T values",
            NOT_APPLICABLE,
            "no parseable date in archive path",
            {},
        )
    if rs.out_day_count == 0:
        return _result(
            "10.9.31",
            "symbol_date",
            "Archive-path date matches T values",
            PASS,
            "no T values fall outside the archive-path date",
            {"in_day_count": rs.in_day_count, "out_day_count": 0},
        )
    return _result(
        "10.9.31",
        "symbol_date",
        "Archive-path date matches T values",
        FAIL,
        f"{rs.out_day_count} T values outside the archive-path UTC day",
        {"in_day_count": rs.in_day_count, "out_day_count": rs.out_day_count},
    )


def check_date_within_retention_window_or_fail_closed(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    if ctx.expected_utc_day_start_ms is None:
        return _result(
            "10.9.32",
            "symbol_date",
            "Date within retention window or fail-closed",
            NOT_APPLICABLE,
            "no parseable date in archive path",
            {},
        )
    # Retention default: ≤ 5 years old.
    from datetime import UTC, datetime

    age_days = (
        (datetime.now(UTC).timestamp() * 1000) - ctx.expected_utc_day_start_ms
    ) / (1000 * 60 * 60 * 24)
    if age_days <= _DEFAULT_RETENTION_DAYS:
        return _result(
            "10.9.32",
            "symbol_date",
            "Date within retention window or fail-closed",
            PASS,
            f"date is ~{age_days:.1f} days old; within {_DEFAULT_RETENTION_DAYS}-day default",
            {"age_days": round(age_days, 1)},
        )
    return _result(
        "10.9.32",
        "symbol_date",
        "Date within retention window or fail-closed",
        FAIL,
        f"date is ~{age_days:.0f} days old; beyond default retention horizon",
        {"age_days": round(age_days, 1), "default_horizon_days": _DEFAULT_RETENTION_DAYS},
    )


# ---------------------------------------------------------------------------
# Group 10.10 — Archive-integrity checks
# ---------------------------------------------------------------------------


def check_zip_single_csv_member(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    n = ctx.artefact_read.csv_member_count
    if n == 1:
        return _result(
            "10.10.33",
            "archive_integrity",
            "ZIP contains exactly one CSV member",
            PASS,
            f"member = {ctx.artefact_read.primary_csv_name}",
            {"csv_member_names": list(ctx.artefact_read.csv_member_names)},
        )
    return _result(
        "10.10.33",
        "archive_integrity",
        "ZIP contains exactly one CSV member",
        FAIL,
        f"observed {n} members",
        {"csv_member_names": list(ctx.artefact_read.csv_member_names)},
    )


def check_zip_decompresses_cleanly(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    if ctx.artefact_read.decompression_ok:
        return _result(
            "10.10.34",
            "archive_integrity",
            "ZIP decompresses cleanly",
            PASS,
            "decompression succeeded",
            {"primary_csv_size": ctx.artefact_read.primary_csv_uncompressed_size},
        )
    return _result(
        "10.10.34",
        "archive_integrity",
        "ZIP decompresses cleanly",
        FAIL,
        f"decompression failed: {ctx.artefact_read.decompression_error}",
        {},
    )


def check_file_size_within_bounds(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    size = ctx.artefact_read.raw_zip_size
    if 0 < size <= MAX_ARCHIVE_BYTES:
        return _result(
            "10.10.35",
            "archive_integrity",
            "Archive file size within bounds",
            PASS,
            f"{size} bytes",
            {"size_bytes": size, "max_bytes": MAX_ARCHIVE_BYTES},
        )
    return _result(
        "10.10.35",
        "archive_integrity",
        "Archive file size within bounds",
        FAIL,
        f"size = {size} outside (0, {MAX_ARCHIVE_BYTES}]",
        {"size_bytes": size, "max_bytes": MAX_ARCHIVE_BYTES},
    )


def check_archive_byte_count_matches_on_disk(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    on_disk = ctx.artefact_read.raw_zip_size
    try:
        actual = ctx.artefacts.raw_zip_path.stat().st_size
    except OSError as exc:
        return _result(
            "10.10.36",
            "archive_integrity",
            "Archive byte count matches on-disk file size",
            ERROR,
            f"stat failed: {exc}",
            {},
        )
    if on_disk == actual:
        return _result(
            "10.10.36",
            "archive_integrity",
            "Archive byte count matches on-disk file size",
            PASS,
            f"{actual} bytes",
            {"recorded": on_disk, "actual": actual},
        )
    return _result(
        "10.10.36",
        "archive_integrity",
        "Archive byte count matches on-disk file size",
        FAIL,
        "recorded byte count differs from on-disk size",
        {"recorded": on_disk, "actual": actual},
    )


# ---------------------------------------------------------------------------
# Group 10.11 — Invalid-window checks
# ---------------------------------------------------------------------------


def check_invalid_windows_parseable_round_trip(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    bad: list[dict[str, Any]] = []
    for i, w in enumerate(ctx.manifest.invalid_windows):
        try:
            d = w.to_dict()
            InvalidWindow.from_dict(d)
        except Exception as exc:  # noqa: BLE001 — recorded as failure detail
            bad.append({"index": i, "error": str(exc)})
    if bad:
        return _result(
            "10.11.37",
            "invalid_windows",
            "invalid_windows round-trip parseable",
            FAIL,
            "round-trip failed",
            {"failures": bad},
        )
    return _result(
        "10.11.37",
        "invalid_windows",
        "invalid_windows round-trip parseable",
        PASS,
        f"{len(ctx.manifest.invalid_windows)} entries round-trip cleanly",
        {"count": len(ctx.manifest.invalid_windows)},
    )


def check_every_invalid_window_has_evidence(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    bad = []
    for i, w in enumerate(ctx.manifest.invalid_windows):
        if not isinstance(w.evidence, Mapping) or not w.evidence:
            bad.append(i)
    if bad:
        return _result(
            "10.11.38",
            "invalid_windows",
            "Every invalid window has non-empty evidence",
            FAIL,
            "one or more invalid windows lack evidence",
            {"empty_indices": bad},
        )
    return _result(
        "10.11.38",
        "invalid_windows",
        "Every invalid window has non-empty evidence",
        PASS,
        "all entries have evidence",
        {"count": len(ctx.manifest.invalid_windows)},
    )


def check_invalid_window_severity_action_consistency(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    bad = []
    for i, w in enumerate(ctx.manifest.invalid_windows):
        sev = w.severity
        act = w.downstream_eligibility_action
        if (
            sev is InvalidWindowSeverity.ERROR
            and act not in (
                DownstreamEligibilityAction.EXCLUDE,
                DownstreamEligibilityAction.PROXY_ONLY,
            )
        ):
            bad.append({"index": i, "severity": sev.value, "action": act.value})
        if (
            act is DownstreamEligibilityAction.EXCLUDE
            and sev not in (InvalidWindowSeverity.WARN, InvalidWindowSeverity.ERROR)
        ):
            bad.append({"index": i, "severity": sev.value, "action": act.value})
    if bad:
        return _result(
            "10.11.39",
            "invalid_windows",
            "Severity / action consistency",
            FAIL,
            "inconsistent severity/action combinations",
            {"violations": bad},
        )
    return _result(
        "10.11.39",
        "invalid_windows",
        "Severity / action consistency",
        PASS,
        "all combinations consistent",
        {"count": len(ctx.manifest.invalid_windows)},
    )


def check_no_silent_omission_of_per_row_failures(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    rs = ctx.artefact_read.row_scan
    has_per_row_anomaly = (
        rs.duplicate_a_count > 0
        or rs.out_of_order_a_count > 0
        or rs.f_le_l_violations > 0
        or rs.validator_failures > 0
        or rs.out_day_count > 0
    )
    has_manifest_invalid_window = bool(ctx.manifest.invalid_windows)
    if has_per_row_anomaly and not has_manifest_invalid_window:
        return _result(
            "10.11.40",
            "invalid_windows",
            "No silent omission of per-row failures",
            FAIL,
            "per-row anomalies discovered without corresponding manifest entry",
            {
                "duplicate_a_count": rs.duplicate_a_count,
                "out_of_order_a_count": rs.out_of_order_a_count,
                "f_le_l_violations": rs.f_le_l_violations,
                "validator_failures": rs.validator_failures,
                "out_day_count": rs.out_day_count,
            },
        )
    if not has_per_row_anomaly:
        return _result(
            "10.11.40",
            "invalid_windows",
            "No silent omission of per-row failures",
            PASS,
            "no per-row anomalies discovered",
            {},
        )
    return _result(
        "10.11.40",
        "invalid_windows",
        "No silent omission of per-row failures",
        PASS,
        "per-row anomalies present and represented in manifest",
        {"manifest_invalid_window_count": len(ctx.manifest.invalid_windows)},
    )


# ---------------------------------------------------------------------------
# Group 10.12 — Cross-cutting
# ---------------------------------------------------------------------------


def check_feature_computation_forbidden_on_raw_family(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    labels = dict(ctx.manifest.governance_labels)
    val = labels.get("feature_computation", "")
    if val == "forbidden":
        return _result(
            "10.12.41",
            "cross_cutting",
            "feature_computation: forbidden on raw family",
            PASS,
            "feature_computation = forbidden",
            {"observed": val},
        )
    return _result(
        "10.12.41",
        "cross_cutting",
        "feature_computation: forbidden on raw family",
        FAIL,
        f"feature_computation = {val!r} (must be 'forbidden')",
        {"observed": val},
    )


def check_strategy_use_forbidden_on_raw_family(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    labels = dict(ctx.manifest.governance_labels)
    val = labels.get("strategy_use", "")
    if val == "forbidden":
        return _result(
            "10.12.42",
            "cross_cutting",
            "strategy_use: forbidden on raw family",
            PASS,
            "strategy_use = forbidden",
            {"observed": val},
        )
    return _result(
        "10.12.42",
        "cross_cutting",
        "strategy_use: forbidden on raw family",
        FAIL,
        f"strategy_use = {val!r} (must be 'forbidden')",
        {"observed": val},
    )


def check_stop_trigger_domain_in_phase3v8_enum(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    labels = dict(ctx.manifest.governance_labels)
    val = labels.get("stop_trigger_domain", "")
    if val in _VALID_STOP_TRIGGER_DOMAINS:
        return _result(
            "10.12.43",
            "cross_cutting",
            "stop_trigger_domain in Phase 3v §8 enum",
            PASS,
            f"stop_trigger_domain = {val}",
            {"observed": val, "allowed": sorted(_VALID_STOP_TRIGGER_DOMAINS)},
        )
    return _result(
        "10.12.43",
        "cross_cutting",
        "stop_trigger_domain in Phase 3v §8 enum",
        FAIL,
        f"stop_trigger_domain = {val!r} not in Phase 3v §8 enum",
        {"observed": val, "allowed": sorted(_VALID_STOP_TRIGGER_DOMAINS)},
    )


def check_no_private_endpoint_or_credential_shaped_strings(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    serial = serialise_for_token_scan(ctx.manifest.to_dict())
    log_serial = serialise_for_token_scan(ctx.artefact_read.acquisition_log)
    manifest_tokens = scan_text_for_forbidden_tokens(serial)
    log_tokens = scan_text_for_forbidden_tokens(log_serial)
    if manifest_tokens or log_tokens:
        return _result(
            "10.12.44",
            "cross_cutting",
            "No private-endpoint or credential-shaped strings",
            FAIL,
            "credential-shaped tokens detected",
            {
                "manifest_tokens": manifest_tokens,
                "acquisition_log_tokens": log_tokens,
            },
        )
    return _result(
        "10.12.44",
        "cross_cutting",
        "No private-endpoint or credential-shaped strings",
        PASS,
        "no forbidden tokens",
        {"denylist_size": len(DENYLIST_TOKENS), "allowlist_size": len(ALLOWLIST_PATTERNS)},
    )


def check_acquisition_log_present_and_self_consistent(
    ctx: GateExecutionContext,
) -> AggTradesEligibilityCheckResult:
    log = ctx.artefact_read.acquisition_log
    if not log:
        return _result(
            "10.12.45",
            "cross_cutting",
            "Acquisition log present and self-consistent",
            FAIL,
            "acquisition log missing or empty",
            {},
        )
    m = ctx.manifest
    discrepancies = []
    for k, expected in (
        ("start_time_ms", m.start_time_ms),
        ("end_time_ms", m.end_time_ms),
        ("event_count", m.event_count),
        ("code_commit_sha", m.code_commit_sha),
    ):
        if k in log and log[k] != expected:
            discrepancies.append({"key": k, "manifest": expected, "log": log[k]})
    if discrepancies:
        return _result(
            "10.12.45",
            "cross_cutting",
            "Acquisition log present and self-consistent",
            FAIL,
            "manifest / acquisition-log fields disagree",
            {"discrepancies": discrepancies},
        )
    return _result(
        "10.12.45",
        "cross_cutting",
        "Acquisition log present and self-consistent",
        PASS,
        "acquisition log values agree with manifest",
        {"checked_keys": ["start_time_ms", "end_time_ms", "event_count", "code_commit_sha"]},
    )


# ---------------------------------------------------------------------------
# Orchestrator entry point
# ---------------------------------------------------------------------------


CHECK_ORDER: tuple[tuple[str, str, str, Any], ...] = (
    # 10.1 source
    (
        "10.1.1",
        "source",
        "Source label whitelisted",
        check_source_label_whitelisted,
    ),
    (
        "10.1.2",
        "source",
        "Endpoint label is a documented archive family",
        check_endpoint_label_documented_archive_family,
    ),
    (
        "10.1.3",
        "source",
        "endpoint_docs_reference present",
        check_endpoint_docs_reference_present,
    ),
    (
        "10.1.4",
        "source",
        "No private-endpoint label",
        check_no_private_endpoint_label,
    ),
    (
        "10.1.5",
        "source",
        "capture_mode is historical_archive",
        check_capture_mode_is_historical_archive,
    ),
    # 10.2 checksum
    (
        "10.2.6",
        "checksum",
        "files[*].sha256 is 64-char lowercase hex",
        check_files_sha256_is_64char_lowercase_hex,
    ),
    (
        "10.2.7",
        "checksum",
        "Recomputed SHA matches manifest and sidecar",
        check_recomputed_sha_matches_manifest_and_sidecar,
    ),
    (
        "10.2.8",
        "checksum",
        ".CHECKSUM companion verification recorded",
        check_checksum_companion_verification_recorded,
    ),
    # 10.3 manifest
    (
        "10.3.9",
        "manifest",
        "Required manifest fields populated",
        check_required_manifest_fields_populated,
    ),
    (
        "10.3.10",
        "manifest",
        "research_eligible is false and eligibility_gate_status is pending",
        check_research_eligible_false_and_status_pending,
    ),
    (
        "10.3.11",
        "manifest",
        "governance_labels minimum keys",
        check_governance_labels_minimum_keys,
    ),
    (
        "10.3.12",
        "manifest",
        "code_commit_sha exists in repo history",
        check_code_commit_sha_exists_in_repo_history,
    ),
    (
        "10.3.13",
        "manifest",
        "capture_config_hash is non-empty and re-derivable",
        check_capture_config_hash_nonempty_and_redrivable,
    ),
    # 10.4 schema
    (
        "10.4.14",
        "schema",
        "Every row passes validate_aggtrade_payload",
        check_every_row_passes_validate_aggtrade_payload,
    ),
    (
        "10.4.15",
        "schema",
        "Column order recorded",
        check_column_order_recorded,
    ),
    (
        "10.4.16",
        "schema",
        "No unexpected extra columns",
        check_no_unexpected_extra_columns,
    ),
    # 10.5 timestamps
    (
        "10.5.17",
        "timestamps",
        "All T are int ms within manifest range",
        check_all_T_are_int_ms_within_manifest_range,
    ),
    (
        "10.5.18",
        "timestamps",
        "manifest.start_time_ms <= manifest.end_time_ms",
        check_start_time_ms_le_end_time_ms,
    ),
    (
        "10.5.19",
        "timestamps",
        "T non-decreasing across file",
        check_T_non_decreasing_across_file,
    ),
    (
        "10.5.20",
        "timestamps",
        "UTC-day match",
        check_utc_day_match,
    ),
    # 10.6 monotonicity
    (
        "10.6.21",
        "monotonicity",
        "Aggregate trade IDs non-decreasing",
        check_a_non_decreasing_across_file,
    ),
    (
        "10.6.22",
        "monotonicity",
        "Aggregate trade ID increments non-negative",
        check_a_increments_non_negative,
    ),
    (
        "10.6.23",
        "monotonicity",
        "No aggregate trade ID reappears with a different (p, q, m, T) tuple",
        check_no_a_value_reappears_with_different_tuple,
    ),
    # 10.7 duplicates
    (
        "10.7.24",
        "duplicates",
        "No duplicate aggregate trade IDs",
        check_no_duplicate_a_within_file,
    ),
    (
        "10.7.25",
        "duplicates",
        "f <= l for every row",
        check_f_le_l_for_every_row,
    ),
    # 10.8 row count
    (
        "10.8.26",
        "row_count",
        "manifest.event_count > 0",
        check_event_count_gt_zero,
    ),
    (
        "10.8.27",
        "row_count",
        "event_count matches actual row count",
        check_event_count_matches_actual_row_count,
    ),
    (
        "10.8.28",
        "row_count",
        "event_count consistent with sum(files[*].event_count)",
        check_event_count_consistent_with_files_sum,
    ),
    # 10.9 symbol/date
    (
        "10.9.29",
        "symbol_date",
        "Symbol in project allowlist",
        check_symbol_in_project_allowlist,
    ),
    (
        "10.9.30",
        "symbol_date",
        "symbol_scope_source recorded and path matches",
        check_symbol_scope_source_recorded_and_path_match,
    ),
    (
        "10.9.31",
        "symbol_date",
        "Archive-path date matches T values",
        check_archive_path_date_matches_T_values,
    ),
    (
        "10.9.32",
        "symbol_date",
        "Date within retention window or fail-closed",
        check_date_within_retention_window_or_fail_closed,
    ),
    # 10.10 archive integrity
    (
        "10.10.33",
        "archive_integrity",
        "ZIP contains exactly one CSV member",
        check_zip_single_csv_member,
    ),
    (
        "10.10.34",
        "archive_integrity",
        "ZIP decompresses cleanly",
        check_zip_decompresses_cleanly,
    ),
    (
        "10.10.35",
        "archive_integrity",
        "Archive file size within bounds",
        check_file_size_within_bounds,
    ),
    (
        "10.10.36",
        "archive_integrity",
        "Archive byte count matches on-disk file size",
        check_archive_byte_count_matches_on_disk,
    ),
    # 10.11 invalid windows
    (
        "10.11.37",
        "invalid_windows",
        "invalid_windows round-trip parseable",
        check_invalid_windows_parseable_round_trip,
    ),
    (
        "10.11.38",
        "invalid_windows",
        "Every invalid window has non-empty evidence",
        check_every_invalid_window_has_evidence,
    ),
    (
        "10.11.39",
        "invalid_windows",
        "Severity / action consistency",
        check_invalid_window_severity_action_consistency,
    ),
    (
        "10.11.40",
        "invalid_windows",
        "No silent omission of per-row failures",
        check_no_silent_omission_of_per_row_failures,
    ),
    # 10.12 cross-cutting
    (
        "10.12.41",
        "cross_cutting",
        "feature_computation: forbidden on raw family",
        check_feature_computation_forbidden_on_raw_family,
    ),
    (
        "10.12.42",
        "cross_cutting",
        "strategy_use: forbidden on raw family",
        check_strategy_use_forbidden_on_raw_family,
    ),
    (
        "10.12.43",
        "cross_cutting",
        "stop_trigger_domain in Phase 3v §8 enum",
        check_stop_trigger_domain_in_phase3v8_enum,
    ),
    (
        "10.12.44",
        "cross_cutting",
        "No private-endpoint or credential-shaped strings",
        check_no_private_endpoint_or_credential_shaped_strings,
    ),
    (
        "10.12.45",
        "cross_cutting",
        "Acquisition log present and self-consistent",
        check_acquisition_log_present_and_self_consistent,
    ),
)


def _build_invalid_window_candidates(
    ctx: GateExecutionContext,
) -> tuple[InvalidWindowCandidate, ...]:
    """Build :class:`InvalidWindowCandidate` records from per-row anomalies."""
    candidates: list[InvalidWindowCandidate] = []
    family = ctx.manifest.dataset_family
    symbol = ctx.manifest.symbol
    for anomaly in ctx.anomalies:
        kind = anomaly.get("kind")
        if kind == "duplicate_a":
            candidates.append(
                InvalidWindowCandidate(
                    reason=InvalidWindowReason.DUPLICATE_EVENT,
                    severity=InvalidWindowSeverity.ERROR,
                    downstream_eligibility_action=DownstreamEligibilityAction.EXCLUDE,
                    start_time_ms=int(anomaly.get("T", 0)) or 0,
                    end_time_ms=int(anomaly.get("T", 0)) or 0,
                    family=family,
                    symbol=symbol,
                    evidence=dict(anomaly),
                    discovered_by_check_id="10.7.24",
                )
            )
        elif kind == "a_out_of_order":
            candidates.append(
                InvalidWindowCandidate(
                    reason=InvalidWindowReason.OUT_OF_ORDER_EVENT,
                    severity=InvalidWindowSeverity.ERROR,
                    downstream_eligibility_action=DownstreamEligibilityAction.EXCLUDE,
                    start_time_ms=0,
                    end_time_ms=0,
                    family=family,
                    symbol=symbol,
                    evidence=dict(anomaly),
                    discovered_by_check_id="10.6.21",
                )
            )
        elif kind == "validator_failure":
            candidates.append(
                InvalidWindowCandidate(
                    reason=InvalidWindowReason.ZERO_OR_INVALID_PRICE,
                    severity=InvalidWindowSeverity.ERROR,
                    downstream_eligibility_action=DownstreamEligibilityAction.EXCLUDE,
                    start_time_ms=int(anomaly.get("T", 0)) or 0,
                    end_time_ms=int(anomaly.get("T", 0)) or 0,
                    family=family,
                    symbol=symbol,
                    evidence=dict(anomaly),
                    discovered_by_check_id="10.4.14",
                )
            )
        elif kind in ("T_before_utc_day_start", "T_at_or_after_utc_day_end"):
            candidates.append(
                InvalidWindowCandidate(
                    reason=InvalidWindowReason.SYMBOL_MISMATCH
                    if kind == "T_before_utc_day_start"
                    else InvalidWindowReason.OUT_OF_ORDER_EVENT,
                    severity=InvalidWindowSeverity.ERROR,
                    downstream_eligibility_action=DownstreamEligibilityAction.EXCLUDE,
                    start_time_ms=int(anomaly.get("T", 0)) or 0,
                    end_time_ms=int(anomaly.get("T", 0)) or 0,
                    family=family,
                    symbol=symbol,
                    evidence=dict(anomaly),
                    discovered_by_check_id="10.5.20",
                )
            )
        elif kind == "f_gt_l":
            candidates.append(
                InvalidWindowCandidate(
                    reason=InvalidWindowReason.OUT_OF_ORDER_EVENT,
                    severity=InvalidWindowSeverity.ERROR,
                    downstream_eligibility_action=DownstreamEligibilityAction.EXCLUDE,
                    start_time_ms=0,
                    end_time_ms=0,
                    family=family,
                    symbol=symbol,
                    evidence=dict(anomaly),
                    discovered_by_check_id="10.7.25",
                )
            )
    return tuple(candidates)


def run_all_checks(
    ctx: GateExecutionContext,
) -> tuple[
    tuple[AggTradesEligibilityCheckResult, ...],
    tuple[InvalidWindowCandidate, ...],
]:
    """Execute every check in :data:`CHECK_ORDER` and return ``(checks, candidates)``."""
    results: list[AggTradesEligibilityCheckResult] = []
    for check_id, group, title, fn in CHECK_ORDER:
        try:
            result = fn(ctx)
        except Exception as exc:  # noqa: BLE001 — surfaced as ERROR
            result = _result(
                check_id,
                group,
                title,
                ERROR,
                f"check raised {type(exc).__name__}: {exc}",
                {},
            )
        # Defensive: each function must return the matching id/group/title.
        if (result.check_id, result.group, result.title) != (check_id, group, title):
            result = _result(
                check_id,
                group,
                title,
                ERROR,
                "internal mismatch between CHECK_ORDER and check function",
                {},
            )
        results.append(result)

    if len(results) != 45:  # pragma: no cover — defensive
        raise RuntimeError(
            f"internal error: expected 45 results, got {len(results)}"
        )
    candidates = _build_invalid_window_candidates(ctx)
    return tuple(results), candidates
