"""Phase 4bd offline aggTrades normalization orchestrator.

This module is the public entry point for Phase 4bd. It:

- reads source raw artefacts read-only via :mod:`normalize_io`;
- iterates the raw zip in memory once;
- validates every raw row via the Phase 4ax
  :func:`prometheus.research.microstructure.aggtrades.validate_aggtrade_payload`;
- maps every raw row to exactly one
  :class:`NormalizedAggTradeRow` with deterministic ``row_index``;
- enforces schema equality against
  :data:`NORMALIZED_SCHEMA_V001`;
- atomically writes a Parquet file under
  ``data/microstructure/normalized/...``;
- atomically writes a derived manifest under
  ``data/microstructure/manifests/...`` with
  ``research_eligible=False`` and
  ``eligibility_gate_status=pending`` defaults preserved;
- runs the Phase 4bc 27-check validation suite;
- proves raw artefact immutability hash-pre vs hash-post;
- returns an :class:`NormalizeAggTradesResult` with
  ``research_eligible_after = False`` and
  ``no_successor_authorization = True`` invariants enforced.

This module:

- does NOT call any endpoint, open any WebSocket, use any credential,
  read ``.env`` / ``.mcp.json``, or import any networking library;
- does NOT compute features, labels, signals, returns, alpha, edge,
  or any execution-quality / order-flow proxy;
- does NOT mutate any source raw artefact or the existing Phase 4bb-D
  gate report;
- writes only under the gitignored
  ``data/microstructure/normalized/`` partition tree (Parquet) and
  ``data/microstructure/manifests/`` (derived manifest, paired
  ``.sha256`` sidecar) and refuses to overwrite an existing finalised
  file.
"""

from __future__ import annotations

import csv
import io
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .aggtrades import AggTradePayload, AggTradeValidationError, validate_aggtrade_payload
from .invalid_window import InvalidWindow
from .normalize_io import (
    NormalizationIOError,
    assert_manifest_path_under_manifests,
    assert_path_under_microstructure,
    atomic_write_json,
    atomic_write_parquet,
    compute_bytes_sha256,
    compute_file_sha256,
    derive_manifest_output_path,
    derive_normalized_output_path,
    open_zip_single_csv_in_memory,
    parse_manifest_bytes,
    read_acquisition_log,
    read_manifest_bytes,
    read_sidecar,
    relative_to_microstructure_root,
    resolve_source_artefact_paths,
    write_sha256_sidecar,
)
from .normalize_manifest import NormalizationManifestDraft

if TYPE_CHECKING:  # pragma: no cover - type-only
    from .normalize_validation import (
        NormalizationCheckResult,
        NormalizationCheckStatus,
    )

NORMALIZATION_SCHEMA_VERSION = "v001"
"""Constant schema version for Phase 4bd."""

NORMALIZED_DATASET_FAMILY = "microstructure_normalized_aggtrades_v001"
SOURCE_DATASET_FAMILY = "microstructure_raw_aggtrades_v001"
SOURCE_DATASET_VERSION = "v001"

NORMALIZED_SCHEMA_V001: tuple[str, ...] = (
    "dataset_family",
    "dataset_version",
    "source_dataset_family",
    "source_dataset_version",
    "symbol",
    "utc_date",
    "agg_trade_id",
    "price",
    "quantity",
    "first_trade_id",
    "last_trade_id",
    "transact_time_ms",
    "is_buyer_maker",
    "source_file_sha256",
    "source_manifest_sha256",
    "source_gate_report_id",
    "source_gate_report_sha256",
    "row_index",
    "normalization_schema_version",
)
"""The 19-column normalized schema, in canonical column order (Phase 4bc §11)."""

UTC_DAY_MS = 86_400_000

_DECIMAL_RE = re.compile(r"^[0-9]+(\.[0-9]+)?$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class NormalizationValidationError(RuntimeError):
    """Raised when Phase 4bd normalization fails a validation invariant."""


@dataclass(frozen=True)
class NormalizedAggTradeRow:
    """One normalized aggTrade row matching the Phase 4bc 19-column schema."""

    dataset_family: str
    dataset_version: str
    source_dataset_family: str
    source_dataset_version: str
    symbol: str
    utc_date: str
    agg_trade_id: int
    price: str
    quantity: str
    first_trade_id: int
    last_trade_id: int
    transact_time_ms: int
    is_buyer_maker: bool
    source_file_sha256: str
    source_manifest_sha256: str
    source_gate_report_id: str
    source_gate_report_sha256: str
    row_index: int
    normalization_schema_version: str

    def __post_init__(self) -> None:
        # Constants
        if self.dataset_family != NORMALIZED_DATASET_FAMILY:
            raise NormalizationValidationError(
                f"dataset_family must be {NORMALIZED_DATASET_FAMILY!r}"
            )
        if self.dataset_version != "v001":
            raise NormalizationValidationError("dataset_version must be 'v001'")
        if self.source_dataset_family != SOURCE_DATASET_FAMILY:
            raise NormalizationValidationError(
                f"source_dataset_family must be {SOURCE_DATASET_FAMILY!r}"
            )
        if self.source_dataset_version != SOURCE_DATASET_VERSION:
            raise NormalizationValidationError(
                f"source_dataset_version must be {SOURCE_DATASET_VERSION!r}"
            )
        if self.normalization_schema_version != NORMALIZATION_SCHEMA_VERSION:
            raise NormalizationValidationError(
                "normalization_schema_version must be "
                f"{NORMALIZATION_SCHEMA_VERSION!r}"
            )

        # Symbol / date
        if not isinstance(self.symbol, str) or not self.symbol.isalnum():
            raise NormalizationValidationError("symbol must be alphanumeric")
        if self.symbol != self.symbol.upper():
            raise NormalizationValidationError("symbol must be uppercase")
        if not isinstance(self.utc_date, str) or not _DATE_RE.match(self.utc_date):
            raise NormalizationValidationError("utc_date must be YYYY-MM-DD")

        # Integers (strict; reject bool implicit)
        int_fields: tuple[tuple[str, int], ...] = (
            ("agg_trade_id", self.agg_trade_id),
            ("first_trade_id", self.first_trade_id),
            ("last_trade_id", self.last_trade_id),
            ("transact_time_ms", self.transact_time_ms),
            ("row_index", self.row_index),
        )
        for label, int_value in int_fields:
            if isinstance(int_value, bool) or not isinstance(int_value, int):
                raise NormalizationValidationError(f"{label} must be an int")
            if int_value < 0:
                raise NormalizationValidationError(f"{label} must be >= 0")
        if self.last_trade_id < self.first_trade_id:
            raise NormalizationValidationError(
                "last_trade_id must be >= first_trade_id"
            )
        if self.transact_time_ms <= 0:
            raise NormalizationValidationError("transact_time_ms must be > 0")

        # Bool (strict)
        if not isinstance(self.is_buyer_maker, bool):
            raise NormalizationValidationError("is_buyer_maker must be strict bool")

        # Decimal-parsable strings (no float storage)
        decimal_fields: tuple[tuple[str, str], ...] = (
            ("price", self.price),
            ("quantity", self.quantity),
        )
        for label, dec_value in decimal_fields:
            if not isinstance(dec_value, str):
                raise NormalizationValidationError(
                    f"{label} must be a Decimal-parsable string"
                )
            if not _DECIMAL_RE.match(dec_value):
                raise NormalizationValidationError(
                    f"{label} must match /^[0-9]+(\\.[0-9]+)?$/ (got {dec_value!r})"
                )
            if Decimal(dec_value) <= 0:
                raise NormalizationValidationError(f"{label} must parse > 0")

        # Hex SHAs
        sha_fields: tuple[tuple[str, str], ...] = (
            ("source_file_sha256", self.source_file_sha256),
            ("source_manifest_sha256", self.source_manifest_sha256),
            ("source_gate_report_sha256", self.source_gate_report_sha256),
        )
        for label, sha_value in sha_fields:
            if not isinstance(sha_value, str) or not _HEX64_RE.match(sha_value):
                raise NormalizationValidationError(
                    f"{label} must be 64-char lowercase hex"
                )

        if not isinstance(self.source_gate_report_id, str) or not self.source_gate_report_id:
            raise NormalizationValidationError(
                "source_gate_report_id must be a non-empty string"
            )

        # UTC day-bound: transact_time_ms must lie inside the half-open day.
        try:
            from datetime import UTC, datetime

            day = datetime.strptime(self.utc_date, "%Y-%m-%d").replace(tzinfo=UTC)
            day_start = int(day.timestamp() * 1000)
        except ValueError as exc:
            raise NormalizationValidationError(f"utc_date parse failed: {exc}") from exc
        day_end_excl = day_start + UTC_DAY_MS
        if not (day_start <= self.transact_time_ms < day_end_excl):
            raise NormalizationValidationError(
                "transact_time_ms outside half-open UTC day bounds"
            )


def assert_schema_equals_v001(field_set: Sequence[str]) -> None:
    """Fail closed if *field_set* != the canonical 19-column schema."""
    if tuple(field_set) != NORMALIZED_SCHEMA_V001:
        raise NormalizationValidationError(
            "normalized field set does not match NORMALIZED_SCHEMA_V001 "
            f"(got {tuple(field_set)!r})"
        )


@dataclass(frozen=True)
class NormalizationLineage:
    """Pre-computed source-evidence constants threaded through the mapper."""

    symbol: str
    utc_date: str
    raw_zip_sha: str
    raw_manifest_sha: str
    gate_report_id: str
    gate_report_sha: str


def _map_raw_row_to_normalized(
    payload: AggTradePayload,
    row_index: int,
    lineage: NormalizationLineage,
) -> NormalizedAggTradeRow:
    """Map one validated aggTrade payload to a normalized row."""
    return NormalizedAggTradeRow(
        dataset_family=NORMALIZED_DATASET_FAMILY,
        dataset_version="v001",
        source_dataset_family=SOURCE_DATASET_FAMILY,
        source_dataset_version=SOURCE_DATASET_VERSION,
        symbol=lineage.symbol,
        utc_date=lineage.utc_date,
        agg_trade_id=int(payload.aggregate_trade_id),
        price=str(payload.price),
        quantity=str(payload.quantity),
        first_trade_id=int(payload.first_trade_id),
        last_trade_id=int(payload.last_trade_id),
        transact_time_ms=int(payload.trade_time_ms),
        is_buyer_maker=bool(payload.buyer_is_maker),
        source_file_sha256=lineage.raw_zip_sha,
        source_manifest_sha256=lineage.raw_manifest_sha,
        source_gate_report_id=lineage.gate_report_id,
        source_gate_report_sha256=lineage.gate_report_sha,
        row_index=int(row_index),
        normalization_schema_version=NORMALIZATION_SCHEMA_VERSION,
    )


def _coerce_m(raw: str) -> bool:
    """Coerce a CSV ``m`` value to a strict bool; raise on unknown."""
    if raw in ("true", "True", "TRUE"):
        return True
    if raw in ("false", "False", "FALSE"):
        return False
    raise NormalizationValidationError(f"unparseable m value: {raw!r}")


def _detect_header(first_row: list[str]) -> bool:
    """Return ``True`` iff *first_row* looks like a header (non-numeric first cell)."""
    if not first_row:
        return False
    try:
        int(first_row[0])
        return False
    except ValueError:
        return True


_CSV_HEADER_ALIAS_MAP: dict[str, str] = {
    "agg_trade_id": "a",
    "price": "p",
    "quantity": "q",
    "first_trade_id": "f",
    "last_trade_id": "l",
    "transact_time": "T",
    "is_buyer_maker": "m",
    "is_best_match": "best",
}
_HEADERLESS_CANONICAL_ORDER: tuple[str, ...] = ("a", "p", "q", "f", "l", "T", "m", "best")


def iter_aggtrade_rows_from_csv(
    csv_text: str,
) -> Sequence[AggTradePayload]:
    """Iterate aggTrade rows from CSV text and return validated payloads.

    Header detection mirrors the Phase 4bb-C eligibility-gate I/O logic.
    """
    reader = csv.reader(io.StringIO(csv_text))
    try:
        first_row = next(reader)
    except StopIteration:
        return ()
    has_header = _detect_header(first_row)
    if has_header:
        canonical = tuple(_CSV_HEADER_ALIAS_MAP.get(c, c) for c in first_row)
        rows: list[list[str]] = list(reader)
    else:
        canonical = _HEADERLESS_CANONICAL_ORDER[: len(first_row)]
        rows = [first_row, *reader]

    payloads: list[AggTradePayload] = []
    for row_idx, raw_row in enumerate(rows):
        if not raw_row:
            raise NormalizationValidationError(f"empty CSV row at index {row_idx}")
        rec = dict(zip(canonical, raw_row, strict=False))
        try:
            a = int(rec.get("a", ""))
            f_id = int(rec.get("f", ""))
            l_id = int(rec.get("l", ""))
            T = int(rec.get("T", ""))
        except (KeyError, ValueError) as exc:
            raise NormalizationValidationError(
                f"row {row_idx} has unparseable integer field: {exc}"
            ) from exc
        m_b = _coerce_m(rec.get("m", "").strip())
        payload_dict: dict[str, Any] = {
            "a": a,
            "p": rec.get("p", ""),
            "q": rec.get("q", ""),
            "f": f_id,
            "l": l_id,
            "T": T,
            "m": m_b,
        }
        try:
            payload = validate_aggtrade_payload(payload_dict)
        except AggTradeValidationError as exc:
            raise NormalizationValidationError(
                f"row {row_idx} failed Phase 4ax validator: {exc}"
            ) from exc
        payloads.append(payload)
    return tuple(payloads)


@dataclass(frozen=True)
class NormalizeAggTradesInput:
    """Frozen input record for :func:`run_normalize_aggtrades`."""

    manifest_path: Path
    output_root: Path
    code_commit_sha: str
    cited_gate_report_id: str
    cited_gate_report_sha256: str
    cited_gate_report_path: Path | None = None
    cited_gate_code_commit_sha: str = ""
    write_output: bool = True
    write_manifest: bool = True
    write_sha256_sidecars: bool = True
    explicit_extra_symbols: tuple[str, ...] = ()
    capture_config_hash: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.manifest_path, Path):
            raise NormalizationIOError("manifest_path must be a pathlib.Path")
        if not isinstance(self.output_root, Path):
            raise NormalizationIOError("output_root must be a pathlib.Path")
        if not isinstance(self.code_commit_sha, str) or not (
            _SHA1_RE.match(self.code_commit_sha) or self.code_commit_sha == "unknown"
        ):
            raise NormalizationIOError(
                "code_commit_sha must be a 40-char lowercase hex SHA "
                "(or the literal 'unknown' for offline tests)"
            )
        if not isinstance(self.cited_gate_report_id, str) or not self.cited_gate_report_id:
            raise NormalizationIOError("cited_gate_report_id must be non-empty")
        if not _HEX64_RE.match(self.cited_gate_report_sha256):
            raise NormalizationIOError(
                "cited_gate_report_sha256 must be 64-char lowercase hex"
            )
        if self.write_manifest and not self.write_output:
            raise NormalizationIOError(
                "cannot write manifest without writing output"
            )
        # Path discipline: manifest under manifests/, output_root under
        # data/microstructure/.
        assert_manifest_path_under_manifests(
            self.manifest_path, label="manifest_path"
        )
        assert_path_under_microstructure(self.output_root, label="output_root")


@dataclass(frozen=True)
class NormalizeAggTradesResult:
    """Result of one Phase 4bd normalization run."""

    overall_status: NormalizationCheckStatus
    output_path: Path | None
    output_sha256: str | None
    derived_manifest_path: Path | None
    derived_manifest_sha256: str | None
    event_count: int
    file_count: int
    checks: tuple[NormalizationCheckResult, ...]
    invalid_window_candidates: tuple[InvalidWindow, ...]
    measured_summary: Mapping[str, Any]
    boundary_confirmations: Mapping[str, bool]
    research_eligible_after: bool
    no_successor_authorization: bool


def _utc_date_from_manifest(parsed: Mapping[str, Any]) -> str:
    """Derive ``utc_date`` (``YYYY-MM-DD``) from manifest start_time_ms."""
    from datetime import UTC, datetime

    start_ms = int(parsed.get("start_time_ms", 0))
    if start_ms <= 0:
        raise NormalizationIOError(
            "source manifest start_time_ms must be a positive int"
        )
    return datetime.fromtimestamp(start_ms / 1000, UTC).strftime("%Y-%m-%d")


def run_normalize_aggtrades(inp: NormalizeAggTradesInput) -> NormalizeAggTradesResult:
    """Execute the Phase 4bd offline aggTrades normalizer once.

    Returns a :class:`NormalizeAggTradesResult` with
    ``research_eligible_after = False`` and
    ``no_successor_authorization = True`` invariants enforced.
    """
    measured: dict[str, Any] = {}
    boundary: dict[str, bool] = {
        "no_network_io": True,
        "no_websocket": True,
        "no_credential_read": True,
        "no_env_read": True,
        "no_mcp_or_graphify": True,
        "no_manifest_mutation": False,  # set True after immutability proven
        "no_data_microstructure_write_outside_normalized": False,
        "no_normalization_written_outside_namespace": False,
        "no_feature_computed": True,
        "no_label_computed": True,
        "no_signal_computed": True,
        "no_ml_trained": True,
        "no_strategy_created": True,
        "no_backtest_run": True,
        "research_eligible_after_is_false_for_derived_family": True,
    }
    invalid_window_candidates: tuple[InvalidWindow, ...] = ()

    # --- Step 1: path discipline ---
    artefacts = resolve_source_artefact_paths(inp.manifest_path)
    target_output: Path | None = None
    target_manifest: Path | None = None

    # --- Step 2: read source raw manifest and hash ---
    raw_manifest_bytes_before, manifest_sha_before = read_manifest_bytes(
        artefacts.manifest_path
    )
    parsed_manifest = parse_manifest_bytes(raw_manifest_bytes_before)
    measured["manifest_sha_before"] = manifest_sha_before
    measured["manifest_path"] = str(artefacts.manifest_path)
    if parsed_manifest.get("research_eligible") is not False:
        raise NormalizationValidationError(
            "source manifest research_eligible must be false"
        )
    if parsed_manifest.get("eligibility_gate_status") != "pending":
        raise NormalizationValidationError(
            "source manifest eligibility_gate_status must be 'pending'"
        )
    files = parsed_manifest.get("files") or []
    if not files:
        raise NormalizationValidationError("source manifest has no files entry")
    declared_zip_sha = str(files[0].get("sha256", ""))
    declared_event_count = int(parsed_manifest.get("event_count", 0))
    declared_start_ms = int(parsed_manifest.get("start_time_ms", 0))
    declared_end_ms = int(parsed_manifest.get("end_time_ms", 0))
    declared_symbol = str(parsed_manifest.get("symbol", "")).upper()
    if not declared_symbol:
        raise NormalizationValidationError("source manifest symbol missing")
    utc_date = _utc_date_from_manifest(parsed_manifest)
    measured["declared_event_count"] = declared_event_count
    measured["declared_zip_sha"] = declared_zip_sha
    measured["symbol"] = declared_symbol
    measured["utc_date"] = utc_date

    # --- Step 3: read raw sidecar and raw zip hash ---
    sidecar_text, sidecar_first_64, sidecar_sha_before = read_sidecar(
        artefacts.sidecar_path
    )
    raw_zip_sha_before, raw_zip_size = compute_file_sha256(artefacts.raw_zip_path)
    measured["raw_zip_sha_before"] = raw_zip_sha_before
    measured["raw_zip_size_bytes"] = raw_zip_size
    measured["sidecar_sha_before"] = sidecar_sha_before
    measured["sidecar_first_64"] = sidecar_first_64
    measured["sidecar_text"] = sidecar_text

    # --- Step 4: read acquisition log and hash ---
    acq_log, acq_log_sha_before = read_acquisition_log(artefacts.acquisition_log_path)
    measured["acquisition_log_sha_before"] = acq_log_sha_before
    measured["acquisition_log_keys_present"] = sorted(acq_log.keys())

    # --- Step 5: verify Phase 4bb-D PASS gate report reference ---
    gate_report_local_present = False
    gate_report_recomputed_sha: str | None = None
    if inp.cited_gate_report_path is not None and inp.cited_gate_report_path.exists():
        gate_report_local_present = True
        gate_report_recomputed_sha, _ = compute_file_sha256(inp.cited_gate_report_path)
        if gate_report_recomputed_sha != inp.cited_gate_report_sha256:
            raise NormalizationValidationError(
                "cited gate-report SHA256 mismatch with local file"
            )
    measured["gate_report_local_present"] = gate_report_local_present
    measured["gate_report_recomputed_sha"] = gate_report_recomputed_sha
    measured["cited_gate_report_id"] = inp.cited_gate_report_id
    measured["cited_gate_report_sha256"] = inp.cited_gate_report_sha256
    measured["cited_gate_code_commit_sha"] = inp.cited_gate_code_commit_sha

    # --- Step 6: iterate raw zip in memory ---
    member_name, csv_text, csv_size = open_zip_single_csv_in_memory(
        artefacts.raw_zip_path
    )
    measured["zip_member_name"] = member_name
    measured["csv_uncompressed_size"] = csv_size

    # --- Step 7 + 8: per-row Phase 4ax validation + one-to-one mapping ---
    payloads = iter_aggtrade_rows_from_csv(csv_text)
    lineage = NormalizationLineage(
        symbol=declared_symbol,
        utc_date=utc_date,
        raw_zip_sha=raw_zip_sha_before,
        raw_manifest_sha=manifest_sha_before,
        gate_report_id=inp.cited_gate_report_id,
        gate_report_sha=inp.cited_gate_report_sha256,
    )
    rows: list[NormalizedAggTradeRow] = []
    seen_a: set[int] = set()
    prev_a = -1
    for row_index, payload in enumerate(payloads):
        row = _map_raw_row_to_normalized(payload, row_index, lineage)
        if row.agg_trade_id in seen_a:
            raise NormalizationValidationError(
                f"duplicate agg_trade_id {row.agg_trade_id} at row {row_index}"
            )
        seen_a.add(row.agg_trade_id)
        if row.agg_trade_id < prev_a:
            raise NormalizationValidationError(
                f"agg_trade_id non-monotone at row {row_index}: "
                f"{row.agg_trade_id} < {prev_a}"
            )
        prev_a = row.agg_trade_id
        rows.append(row)
    measured["row_count"] = len(rows)
    if len(rows) != declared_event_count:
        raise NormalizationValidationError(
            f"row count {len(rows)} does not match declared event_count "
            f"{declared_event_count}"
        )
    if rows:
        measured["first_transact_time_ms"] = rows[0].transact_time_ms
        measured["last_transact_time_ms"] = rows[-1].transact_time_ms
        if rows[0].transact_time_ms != declared_start_ms:
            raise NormalizationValidationError(
                "first transact_time_ms does not match manifest start_time_ms"
            )
        if rows[-1].transact_time_ms != declared_end_ms:
            raise NormalizationValidationError(
                "last transact_time_ms does not match manifest end_time_ms"
            )

    # --- Step 9: schema-equality assertion ---
    # The dataclass field order is the canonical order of NORMALIZED_SCHEMA_V001.
    actual_fields = tuple(NormalizedAggTradeRow.__dataclass_fields__)
    assert_schema_equals_v001(actual_fields)

    # --- Step 10 + 11: atomic Parquet write + file SHA ---
    output_sha: str | None = None
    output_size: int | None = None
    if inp.write_output and rows:
        try:
            import pyarrow as pa
        except ImportError as exc:  # pragma: no cover - environment guard
            raise NormalizationIOError(
                "pyarrow is required for Phase 4bd Parquet output"
            ) from exc
        column_data: dict[str, list[Any]] = {col: [] for col in NORMALIZED_SCHEMA_V001}
        for r in rows:
            column_data["dataset_family"].append(r.dataset_family)
            column_data["dataset_version"].append(r.dataset_version)
            column_data["source_dataset_family"].append(r.source_dataset_family)
            column_data["source_dataset_version"].append(r.source_dataset_version)
            column_data["symbol"].append(r.symbol)
            column_data["utc_date"].append(r.utc_date)
            column_data["agg_trade_id"].append(r.agg_trade_id)
            column_data["price"].append(r.price)
            column_data["quantity"].append(r.quantity)
            column_data["first_trade_id"].append(r.first_trade_id)
            column_data["last_trade_id"].append(r.last_trade_id)
            column_data["transact_time_ms"].append(r.transact_time_ms)
            column_data["is_buyer_maker"].append(r.is_buyer_maker)
            column_data["source_file_sha256"].append(r.source_file_sha256)
            column_data["source_manifest_sha256"].append(r.source_manifest_sha256)
            column_data["source_gate_report_id"].append(r.source_gate_report_id)
            column_data["source_gate_report_sha256"].append(r.source_gate_report_sha256)
            column_data["row_index"].append(r.row_index)
            column_data["normalization_schema_version"].append(
                r.normalization_schema_version
            )
        schema = pa.schema(
            [
                ("dataset_family", pa.string()),
                ("dataset_version", pa.string()),
                ("source_dataset_family", pa.string()),
                ("source_dataset_version", pa.string()),
                ("symbol", pa.string()),
                ("utc_date", pa.string()),
                ("agg_trade_id", pa.int64()),
                ("price", pa.string()),
                ("quantity", pa.string()),
                ("first_trade_id", pa.int64()),
                ("last_trade_id", pa.int64()),
                ("transact_time_ms", pa.int64()),
                ("is_buyer_maker", pa.bool_()),
                ("source_file_sha256", pa.string()),
                ("source_manifest_sha256", pa.string()),
                ("source_gate_report_id", pa.string()),
                ("source_gate_report_sha256", pa.string()),
                ("row_index", pa.int64()),
                ("normalization_schema_version", pa.string()),
            ]
        )
        # Sanity: schema field order matches NORMALIZED_SCHEMA_V001.
        assert_schema_equals_v001(tuple(schema.names))
        table = pa.Table.from_pydict(column_data, schema=schema)
        target_output = derive_normalized_output_path(
            output_root=inp.output_root,
            symbol=declared_symbol,
            utc_date=utc_date,
        )
        output_sha, output_size = atomic_write_parquet(
            target_output,
            table,
            refuse_overwrite=True,
        )
        measured["output_path"] = str(target_output)
        measured["output_sha256"] = output_sha
        measured["output_size_bytes"] = output_size
        boundary["no_data_microstructure_write_outside_normalized"] = True
        boundary["no_normalization_written_outside_namespace"] = True
        if inp.write_sha256_sidecars:
            sidecar_target = target_output.with_suffix(target_output.suffix + ".sha256")
            write_sha256_sidecar(
                sidecar_target,
                target_filename=target_output.name,
                sha256_hex=output_sha,
                refuse_overwrite=True,
            )
            measured["output_sidecar_path"] = str(sidecar_target)
    else:
        target_output = None

    # --- Step 12: derived manifest builder + atomic write ---
    derived_manifest_sha: str | None = None
    if inp.write_manifest and target_output is not None and output_sha is not None:
        # Determine manifests root from manifest_path's parent.
        manifests_root = artefacts.manifest_path.parent
        target_manifest = derive_manifest_output_path(manifests_root=manifests_root)
        if target_manifest.exists():
            raise NormalizationIOError(
                f"refusing to overwrite existing derived manifest: {target_manifest}"
            )
        relative_output = relative_to_microstructure_root(target_output)
        relative_raw_zip = relative_to_microstructure_root(artefacts.raw_zip_path)
        relative_raw_manifest = relative_to_microstructure_root(artefacts.manifest_path)
        governance: dict[str, str] = {
            "phase": "4bd",
            "source_phase_boundary": "4bb-D",
            "source_dataset_family": SOURCE_DATASET_FAMILY,
            "source_dataset_version": SOURCE_DATASET_VERSION,
            "source_manifest_path": relative_raw_manifest,
            "source_manifest_sha256": manifest_sha_before,
            "source_raw_zip_path": relative_raw_zip,
            "source_raw_zip_sha256": raw_zip_sha_before,
            "source_gate_report_id": inp.cited_gate_report_id,
            "source_gate_report_sha256": inp.cited_gate_report_sha256,
            "source_gate_report_code_commit_sha": (
                inp.cited_gate_code_commit_sha or "unknown"
            ),
            "validator": "phase_4ax_aggtrades_v001",
            "stop_trigger_domain": "trade_price_backtest_candidate",
            "feature_computation": "forbidden",
            "strategy_use": "forbidden",
            "phase_4bd_no_successor_authorization": "true",
        }
        capture_config_hash = inp.capture_config_hash or compute_bytes_sha256(
            json.dumps(
                {
                    "schema": NORMALIZED_SCHEMA_V001,
                    "schema_version": NORMALIZATION_SCHEMA_VERSION,
                    "source_dataset_family": SOURCE_DATASET_FAMILY,
                    "source_dataset_version": SOURCE_DATASET_VERSION,
                    "source_manifest_sha256": manifest_sha_before,
                    "source_raw_zip_sha256": raw_zip_sha_before,
                    "cited_gate_report_id": inp.cited_gate_report_id,
                    "cited_gate_report_sha256": inp.cited_gate_report_sha256,
                },
                sort_keys=True,
            ).encode("utf-8")
        )
        draft = NormalizationManifestDraft(
            symbol=declared_symbol,
            utc_date=utc_date,
            start_time_ms=rows[0].transact_time_ms,
            end_time_ms=rows[-1].transact_time_ms,
            event_count=len(rows),
            output_relative_path=relative_output,
            output_sha256=output_sha,
            governance_labels=governance,
            invalid_windows=invalid_window_candidates,
            capture_config_hash=capture_config_hash,
            code_commit_sha=inp.code_commit_sha,
        )
        derived_manifest = draft.to_manifest()
        manifest_dict = derived_manifest.to_dict()
        derived_manifest_sha, _ = atomic_write_json(
            target_manifest, manifest_dict, refuse_overwrite=True
        )
        measured["derived_manifest_path"] = str(target_manifest)
        measured["derived_manifest_sha256"] = derived_manifest_sha
        if inp.write_sha256_sidecars:
            sidecar_target = target_manifest.with_suffix(
                target_manifest.suffix + ".sha256"
            )
            write_sha256_sidecar(
                sidecar_target,
                target_filename=target_manifest.name,
                sha256_hex=derived_manifest_sha,
                refuse_overwrite=True,
            )
            measured["derived_manifest_sidecar_path"] = str(sidecar_target)
    else:
        derived_manifest = None
        target_manifest = None

    # --- Step 14: re-hash raw artefacts (immutability) ---
    raw_manifest_bytes_after, manifest_sha_after = read_manifest_bytes(
        artefacts.manifest_path
    )
    raw_zip_sha_after, _ = compute_file_sha256(artefacts.raw_zip_path)
    _, _, sidecar_sha_after = read_sidecar(artefacts.sidecar_path)
    _, acq_log_sha_after = read_acquisition_log(artefacts.acquisition_log_path)
    measured["manifest_sha_after"] = manifest_sha_after
    measured["raw_zip_sha_after"] = raw_zip_sha_after
    measured["sidecar_sha_after"] = sidecar_sha_after
    measured["acquisition_log_sha_after"] = acq_log_sha_after
    immutable_ok = (
        manifest_sha_before == manifest_sha_after
        and raw_zip_sha_before == raw_zip_sha_after
        and sidecar_sha_before == sidecar_sha_after
        and acq_log_sha_before == acq_log_sha_after
    )
    boundary["no_manifest_mutation"] = immutable_ok
    if not immutable_ok:
        raise NormalizationValidationError(
            "raw artefact immutability violated across the run"
        )

    # --- Step 13: 27-check validation suite ---
    # Function-local import breaks the module-level cycle:
    # normalize_validation imports NormalizedAggTradeRow / NormalizeAggTradesInput
    # from this module at the top level.
    from .normalize_validation import (
        NormalizationValidationContext,
        run_all_checks,
    )

    ctx = NormalizationValidationContext(
        inp=inp,
        rows=tuple(rows),
        output_path=target_output,
        output_sha256=output_sha,
        output_size_bytes=output_size,
        derived_manifest=derived_manifest,
        derived_manifest_path=target_manifest,
        derived_manifest_sha256=derived_manifest_sha,
        raw_manifest_bytes_before=raw_manifest_bytes_before,
        raw_manifest_bytes_after=raw_manifest_bytes_after,
        raw_manifest_sha_before=manifest_sha_before,
        raw_manifest_sha_after=manifest_sha_after,
        raw_zip_sha_before=raw_zip_sha_before,
        raw_zip_sha_after=raw_zip_sha_after,
        sidecar_sha_before=sidecar_sha_before,
        sidecar_sha_after=sidecar_sha_after,
        acq_log_sha_before=acq_log_sha_before,
        acq_log_sha_after=acq_log_sha_after,
        cited_gate_report_id=inp.cited_gate_report_id,
        cited_gate_report_sha256=inp.cited_gate_report_sha256,
        cited_gate_code_commit_sha=inp.cited_gate_code_commit_sha,
        gate_report_local_present=gate_report_local_present,
        gate_report_recomputed_sha=gate_report_recomputed_sha,
        artefacts=artefacts,
        parsed_source_manifest=parsed_manifest,
        member_name=member_name,
        csv_uncompressed_size=csv_size,
        invalid_window_candidates=invalid_window_candidates,
    )
    validation = run_all_checks(ctx)

    # --- Step 15: result construction with invariants ---
    return NormalizeAggTradesResult(
        overall_status=validation.overall_status,
        output_path=target_output,
        output_sha256=output_sha,
        derived_manifest_path=target_manifest,
        derived_manifest_sha256=derived_manifest_sha,
        event_count=len(rows),
        file_count=1 if target_output is not None else 0,
        checks=validation.checks,
        invalid_window_candidates=invalid_window_candidates,
        measured_summary=measured,
        boundary_confirmations=dict(boundary),
        research_eligible_after=False,  # invariant for derived raw-source family
        no_successor_authorization=True,  # invariant
    )


__all__ = [
    "NORMALIZATION_SCHEMA_VERSION",
    "NORMALIZED_DATASET_FAMILY",
    "NORMALIZED_SCHEMA_V001",
    "NormalizationLineage",
    "NormalizationValidationError",
    "NormalizeAggTradesInput",
    "NormalizeAggTradesResult",
    "NormalizedAggTradeRow",
    "SOURCE_DATASET_FAMILY",
    "SOURCE_DATASET_VERSION",
    "assert_schema_equals_v001",
    "iter_aggtrade_rows_from_csv",
    "run_normalize_aggtrades",
]
