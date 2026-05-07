"""Phase 4az — Public AggTrades Archive Acquisition (BTCUSDT, 2025-01-15 UTC).

Standalone acquisition script authorised by the Phase 4ay
authorization-boundary memo. Acquires exactly one Binance USDⓈ-M
Futures aggTrades daily archive for BTCUSDT on 2025-01-15 UTC from
the public ``data.binance.vision`` archive, validates row integrity
against the Phase 4ax aggTrades validator under a strict integrity
gate, and writes the raw archive plus a manifest under the gitignored
``data/microstructure/`` tree.

This script is intentionally narrow:

- Standard library only (`urllib.request`, `zipfile`, `csv`,
  `hashlib`, `json`, `argparse`, ...) plus the Phase 4aw / 4ax
  microstructure scaffold modules.
- Two and only two authorised network requests:
  1. The ``.CHECKSUM`` companion file (downloaded first).
  2. The archive ``.zip`` (downloaded only after checksum is parsed
     and validated).
- No Binance API endpoints (no ``fapi.binance.com``).
- No REST polling, no WebSocket, no credentials, no ``.env`` reads.
- No private endpoints, no user stream, no listenKey, no order /
  account / position / leverage / margin / forceOrders REST.
- No imports from ``prometheus.runtime`` / ``prometheus.execution``
  / ``prometheus.persistence``.
- Fail closed on any uncertainty: checksum mismatch, schema
  violation, duplicate / out-of-order trade IDs, timestamp drift
  outside the requested UTC day, multi-member ZIP, or any
  unexpected condition aborts before the final raw file is moved
  into place. Staging artefacts are preserved on failure for
  operator inspection.
- Raw archive only. No normalised JSONL or Parquet is created.
- Manifest is written with ``research_eligible=false`` and
  ``eligibility_gate_status=pending`` per Phase 4ay §12.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

# Make the in-repo ``src/prometheus`` package importable when this
# script is invoked directly (``python scripts/phase4az_*.py``). The
# pyproject.toml pytest config already prepends ``src`` for tests; the
# CLI path needs the same treatment without relying on an editable
# install.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# Phase 4ax / 4aw scaffold imports. These are inert and impose the
# allowed-file-path discipline (RawWriter is not used directly here
# because we are persisting the raw .zip rather than line-streaming
# JSON, but its boundary discipline is mirrored).
from prometheus.research.microstructure.aggtrades import (  # noqa: E402
    AggTradeValidationError,
    TakerSide,
    validate_aggtrade_payload,
)

# ---------------------------------------------------------------------------- #
# Phase constants (predeclared by the operator brief; not configurable)
# ---------------------------------------------------------------------------- #

PHASE_ID = "4az"
DATASET_FAMILY = "microstructure_raw_aggtrades_v001"
DATASET_VERSION = "v001"
SYMBOL = "BTCUSDT"
DATE_STR = "2025-01-15"
ARCHIVE_URL = (
    "https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/"
    "BTCUSDT-aggTrades-2025-01-15.zip"
)
CHECKSUM_URL = ARCHIVE_URL + ".CHECKSUM"
ENDPOINT_LABEL = "data.binance.vision/data/futures/um/daily/aggTrades"
CAPTURE_MODE = "historical_archive"
SCHEMA_VERSION = "v001"
ENDPOINT_DOCS_REFERENCE = (
    "https://github.com/binance/binance-public-data#trades"
    " (futures aggTrades daily archive convention)"
)

# Allowed network host. Any other host is denied.
ALLOWED_HOSTS: tuple[str, ...] = ("data.binance.vision",)

# Maximum allowed download size (5 GiB, predeclared per Phase 4ay §10.4).
MAX_DOWNLOAD_BYTES = 5 * 1024 * 1024 * 1024

# UTC window for the requested day.
DAY_START_UTC = datetime(2025, 1, 15, 0, 0, 0, tzinfo=UTC)
DAY_END_UTC = datetime(2025, 1, 16, 0, 0, 0, tzinfo=UTC)
DAY_START_MS = int(DAY_START_UTC.timestamp() * 1000)
DAY_END_MS = int(DAY_END_UTC.timestamp() * 1000)


# ---------------------------------------------------------------------------- #
# Errors
# ---------------------------------------------------------------------------- #


class AcquisitionError(RuntimeError):
    """Base error for Phase 4az fail-closed conditions."""


# ---------------------------------------------------------------------------- #
# Acquisition result
# ---------------------------------------------------------------------------- #


@dataclass(frozen=True)
class AcquisitionResult:
    status: str  # "SUCCESSFUL_ACQUISITION" | "FAIL_CLOSED_NO_ACQUISITION"
    failure_reason: str | None
    raw_path: Path | None
    sha_path: Path | None
    manifest_path: Path | None
    log_path: Path | None
    event_count: int
    start_time_ms: int
    end_time_ms: int
    sha256_hex: str
    staging_preserved: bool


# ---------------------------------------------------------------------------- #
# URL allowlist
# ---------------------------------------------------------------------------- #


def assert_archive_url_allowed(url: str) -> None:
    """Reject any URL outside the allowlist or pointing at non-archive hosts."""
    if not isinstance(url, str) or not url:
        raise AcquisitionError("URL must be a non-empty string")
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("https",):
        raise AcquisitionError(
            f"URL scheme must be https, got {parsed.scheme!r} for {url!r}"
        )
    if parsed.hostname not in ALLOWED_HOSTS:
        raise AcquisitionError(
            f"URL host {parsed.hostname!r} is not in the allowed set "
            f"{ALLOWED_HOSTS!r} for {url!r}"
        )
    if "/aggTrades/" not in parsed.path:
        raise AcquisitionError(
            f"URL path {parsed.path!r} is not an aggTrades archive path"
        )
    forbidden_substrings = (
        "fapi.binance.com",
        "/fapi/",
        "/v1/order",
        "/v1/account",
        "/v2/account",
        "/v2/positionRisk",
        "/v1/leverage",
        "/v1/marginType",
        "/v1/forceOrders",
        "/v1/listenKey",
        "userDataStream",
        "api_key",
        "apiKey",
        "secret_key",
        "secretKey",
        "signature",
        "X-MBX-APIKEY",
        ".mcp.json",
        "Graphify",
        "MCP",
        ".env",
    )
    lowered = url.lower()
    for token in forbidden_substrings:
        if token.lower() in lowered:
            raise AcquisitionError(
                f"URL {url!r} contains forbidden token {token!r}"
            )


# ---------------------------------------------------------------------------- #
# Checksum parsing
# ---------------------------------------------------------------------------- #


def parse_sha256_from_checksum(content: str) -> str:
    """Parse the first 64 hex characters of a Binance checksum file body.

    Binance public-data ``.CHECKSUM`` files generally contain a line of
    the form ``<sha256-hex>  <filename>``. We accept the hex prefix as
    the canonical SHA256 and ignore the filename label, but fail closed
    on anything that is not a full 64-character lowercase hex digest.
    """
    if not isinstance(content, str):
        raise AcquisitionError("checksum content must be a str")
    stripped = content.strip()
    if not stripped:
        raise AcquisitionError("checksum content is empty")
    first_token = stripped.split()[0] if stripped.split() else ""
    if len(first_token) != 64:
        raise AcquisitionError(
            f"checksum prefix is not 64 hex characters: {first_token!r}"
        )
    if not all(c in "0123456789abcdefABCDEF" for c in first_token):
        raise AcquisitionError(
            f"checksum prefix is not hex: {first_token!r}"
        )
    return first_token.lower()


# ---------------------------------------------------------------------------- #
# Network fetch (urllib.request only, allowed host only)
# ---------------------------------------------------------------------------- #


def _http_get(url: str, dest_path: Path) -> int:
    """Download ``url`` to ``dest_path`` with a size cap. Returns bytes written.

    No retries. No redirects to other hosts (Python's default urllib follows
    same-scheme redirects but we re-check the host via the response URL).
    Bounded by :data:`MAX_DOWNLOAD_BYTES` to prevent runaway downloads.
    """
    assert_archive_url_allowed(url)
    request = urllib.request.Request(url, method="GET")
    written = 0
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 (allow-listed)
        final_url = response.geturl()
        if final_url != url:
            assert_archive_url_allowed(final_url)
        with dest_path.open("wb") as fh:
            while True:
                chunk = response.read(65_536)
                if not chunk:
                    break
                written += len(chunk)
                if written > MAX_DOWNLOAD_BYTES:
                    raise AcquisitionError(
                        f"download exceeded MAX_DOWNLOAD_BYTES "
                        f"({MAX_DOWNLOAD_BYTES}) for {url}"
                    )
                fh.write(chunk)
    if written == 0:
        raise AcquisitionError(f"download produced empty file for {url}")
    return written


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65_536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------- #
# CSV row decoding
# ---------------------------------------------------------------------------- #


# Header column aliases. Binance has used different headers over time; we
# accept a small allow-list of synonyms for each Phase 4ax payload field.
_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "a": ("agg_trade_id", "aggregate_trade_id", "a"),
    "p": ("price", "p"),
    "q": ("quantity", "q"),
    "f": ("first_trade_id", "f"),
    "l": ("last_trade_id", "l"),
    "T": ("transact_time", "trade_time", "T"),
    "m": ("is_buyer_maker", "m"),
}


# Fixed positional order used when no header is present. This matches the
# documented Binance public-data aggTrades archive schema.
_HEADERLESS_ORDER: tuple[str, ...] = ("a", "p", "q", "f", "l", "T", "m")


def _resolve_header_mapping(
    raw_header: list[str],
) -> dict[str, int] | None:
    """Map header column names to Phase 4ax payload field positions.

    Returns ``None`` if ``raw_header`` does not look like a header row
    (e.g. all values look numeric / non-alphabetic). On a partial match,
    the function fails closed: any required Phase 4ax field that cannot
    be mapped raises :class:`AcquisitionError`.
    """
    if not raw_header:
        return None

    # Heuristic: aggregate trade IDs are integer-shaped, so if the
    # first cell parses cleanly as ``int`` the row is data, not a
    # header. Anything else (alphabetic, mixed) is treated as a header
    # candidate. This avoids spurious matches when a data row happens
    # to contain the substring of a single-character synonym (e.g.
    # ``"false"`` contains ``"f"``).
    first_cell = raw_header[0].strip()
    try:
        int(first_cell)
        return None
    except ValueError:
        pass

    mapping: dict[str, int] = {}
    lowered = [cell.strip().lower() for cell in raw_header]
    for field, synonyms in _HEADER_ALIASES.items():
        for idx, cell in enumerate(lowered):
            if cell in {syn.lower() for syn in synonyms}:
                mapping[field] = idx
                break
        if field not in mapping:
            raise AcquisitionError(
                f"CSV header missing required field {field!r} "
                f"(expected one of {synonyms!r}); got header={raw_header!r}"
            )
    return mapping


def _coerce_buyer_is_maker(token: str) -> bool:
    if token in ("true", "True", "TRUE"):
        return True
    if token in ("false", "False", "FALSE"):
        return False
    raise AcquisitionError(
        f"is_buyer_maker token must be one of true/True/TRUE/false/False/FALSE, "
        f"got {token!r}"
    )


def _row_to_payload(
    row: list[str],
    mapping: dict[str, int] | None,
) -> dict[str, object]:
    """Convert a CSV row to a Phase 4ax aggTrade payload mapping."""
    if mapping is None:
        if len(row) < len(_HEADERLESS_ORDER):
            raise AcquisitionError(
                f"headerless row has too few columns: expected at least "
                f"{len(_HEADERLESS_ORDER)}, got {len(row)}; row={row!r}"
            )
        getters = {field: row[idx] for idx, field in enumerate(_HEADERLESS_ORDER)}
    else:
        getters = {field: row[idx] for field, idx in mapping.items()}

    payload: dict[str, object] = {
        "a": getters["a"],
        "p": getters["p"],
        "q": getters["q"],
        "f": getters["f"],
        "l": getters["l"],
        "T": getters["T"],
        "m": _coerce_buyer_is_maker(getters["m"]),
    }
    return payload


# ---------------------------------------------------------------------------- #
# CSV iteration over a member of a ZIP
# ---------------------------------------------------------------------------- #


def _iter_csv_rows(
    zip_path: Path,
) -> Iterator[tuple[dict[str, int] | None, list[str]]]:
    """Yield ``(header_mapping, row)`` pairs from the single CSV in the ZIP.

    Fails closed if the ZIP does not contain exactly one CSV-like member.
    The header mapping is yielded once per row to keep the validation
    code simple; tests do not need to special-case the first row.
    """
    with zipfile.ZipFile(zip_path) as zf:
        names = [name for name in zf.namelist() if not name.endswith("/")]
        csv_members = [n for n in names if n.lower().endswith(".csv")]
        if not csv_members:
            # Some Binance public-data archives use no .csv extension on
            # the inner member. Fall back to the unique member if there
            # is exactly one, otherwise fail closed.
            if len(names) == 1:
                csv_members = names
            else:
                raise AcquisitionError(
                    f"ZIP {zip_path} does not contain a .csv member "
                    f"and is not single-member; members={names!r}"
                )
        if len(csv_members) != 1:
            raise AcquisitionError(
                f"ZIP {zip_path} must contain exactly one CSV member; "
                f"got {csv_members!r}"
            )
        member = csv_members[0]
        with zf.open(member, "r") as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
            reader = csv.reader(text)
            mapping: dict[str, int] | None = None
            first_row = True
            for row in reader:
                if not row:
                    continue
                if first_row:
                    mapping = _resolve_header_mapping(row)
                    first_row = False
                    if mapping is not None:
                        # Header row consumed; do not yield it as a data row.
                        continue
                yield mapping, row


# ---------------------------------------------------------------------------- #
# Validation pass
# ---------------------------------------------------------------------------- #


@dataclass
class ValidationSummary:
    event_count: int
    start_time_ms: int
    end_time_ms: int
    taker_side_buy_count: int
    taker_side_sell_count: int


def validate_aggtrades_archive(zip_path: Path) -> ValidationSummary:
    """Validate every row of the aggTrades archive against the Phase 4ax validator."""
    last_agg_id: int | None = None
    seen_ids: set[int] = set()
    earliest_ms: int | None = None
    latest_ms: int | None = None
    buy_count = 0
    sell_count = 0
    row_count = 0

    for mapping, row in _iter_csv_rows(zip_path):
        try:
            payload = _row_to_payload(row, mapping)
        except AcquisitionError:
            raise
        try:
            validated = validate_aggtrade_payload(payload)
        except AggTradeValidationError as exc:
            raise AcquisitionError(
                f"row {row_count} failed Phase 4ax validation: {exc}"
            ) from exc

        # Trade-time within the requested UTC day (inclusive start, exclusive end).
        if validated.trade_time_ms < DAY_START_MS or validated.trade_time_ms >= DAY_END_MS:
            raise AcquisitionError(
                f"row {row_count} trade_time_ms={validated.trade_time_ms} "
                f"is outside the UTC window [{DAY_START_MS}, {DAY_END_MS})"
            )

        # Aggregate trade-id duplicate / monotonicity.
        if validated.aggregate_trade_id in seen_ids:
            raise AcquisitionError(
                f"row {row_count} duplicate aggregate_trade_id="
                f"{validated.aggregate_trade_id}"
            )
        seen_ids.add(validated.aggregate_trade_id)
        if last_agg_id is not None and validated.aggregate_trade_id < last_agg_id:
            raise AcquisitionError(
                f"row {row_count} out-of-order aggregate_trade_id="
                f"{validated.aggregate_trade_id} < previous {last_agg_id}"
            )
        last_agg_id = validated.aggregate_trade_id

        if earliest_ms is None or validated.trade_time_ms < earliest_ms:
            earliest_ms = validated.trade_time_ms
        if latest_ms is None or validated.trade_time_ms > latest_ms:
            latest_ms = validated.trade_time_ms

        if validated.taker_side is TakerSide.BUY:
            buy_count += 1
        else:
            sell_count += 1
        row_count += 1

    if row_count == 0:
        raise AcquisitionError("aggTrades archive contained zero rows")

    assert earliest_ms is not None
    assert latest_ms is not None
    return ValidationSummary(
        event_count=row_count,
        start_time_ms=earliest_ms,
        end_time_ms=latest_ms,
        taker_side_buy_count=buy_count,
        taker_side_sell_count=sell_count,
    )


# ---------------------------------------------------------------------------- #
# Manifest writer
# ---------------------------------------------------------------------------- #


def _commit_sha_or_pending() -> str:
    """Return current HEAD SHA if available; otherwise a pending label."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if result.returncode == 0:
            sha = result.stdout.strip()
            if sha:
                return sha
    except Exception:  # noqa: BLE001
        pass
    return "pending_commit_sha"


def _write_manifest(
    manifest_path: Path,
    *,
    raw_relpath: str,
    sha256_hex: str,
    summary: ValidationSummary,
    capture_config_hash: str,
) -> None:
    manifest = {
        "dataset_family": DATASET_FAMILY,
        "version": DATASET_VERSION,
        "symbol": SYMBOL,
        "source": "binance_data_archive",
        "endpoint": ENDPOINT_LABEL,
        "capture_mode": CAPTURE_MODE,
        "start_time_ms": summary.start_time_ms,
        "end_time_ms": summary.end_time_ms,
        "event_count": summary.event_count,
        "file_count": 1,
        "files": [
            {
                "path": raw_relpath,
                "sha256": sha256_hex,
                "event_count": summary.event_count,
                "start_time_ms": summary.start_time_ms,
                "end_time_ms": summary.end_time_ms,
            }
        ],
        "schema_version": SCHEMA_VERSION,
        "endpoint_docs_reference": ENDPOINT_DOCS_REFERENCE,
        "capture_config_hash": capture_config_hash,
        "code_commit_sha": _commit_sha_or_pending(),
        "invalid_windows": [],
        "retention_warning": None,
        "proxy_warning": None,
        "governance_labels": {
            "phase": "4az",
            "source_phase_boundary": "4ay",
            "validator": "phase_4ax_aggtrades_v001",
            "stop_trigger_domain": "trade_price_backtest_candidate",
            "symbol_scope_source": "archive_path",
            "feature_computation": "forbidden",
            "strategy_use": "forbidden",
        },
        "research_eligible": False,
        "eligibility_gate_status": "pending",
    }
    if manifest_path.exists():
        raise AcquisitionError(
            f"refusing to overwrite existing manifest at {manifest_path}"
        )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _write_acquisition_log(
    log_path: Path,
    *,
    status: str,
    failure_reason: str | None,
    raw_relpath: str | None,
    sha256_hex: str | None,
    summary: ValidationSummary | None,
    archive_url: str,
    checksum_url: str,
    staging_dir: Path,
) -> None:
    log = {
        "phase": PHASE_ID,
        "status": status,
        "failure_reason": failure_reason,
        "archive_url": archive_url,
        "checksum_url": checksum_url,
        "raw_relpath": raw_relpath,
        "sha256": sha256_hex,
        "event_count": summary.event_count if summary is not None else None,
        "start_time_ms": summary.start_time_ms if summary is not None else None,
        "end_time_ms": summary.end_time_ms if summary is not None else None,
        "taker_side_buy_count": (
            summary.taker_side_buy_count if summary is not None else None
        ),
        "taker_side_sell_count": (
            summary.taker_side_sell_count if summary is not None else None
        ),
        "staging_dir": str(staging_dir),
        "staging_preserved": staging_dir.exists(),
        "code_commit_sha": _commit_sha_or_pending(),
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists():
        raise AcquisitionError(
            f"refusing to overwrite existing acquisition log at {log_path}"
        )
    log_path.write_text(
        json.dumps(log, indent=2, sort_keys=True),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------- #
# Capture-config hash
# ---------------------------------------------------------------------------- #


def compute_capture_config_hash() -> str:
    payload = {
        "phase": PHASE_ID,
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "symbol": SYMBOL,
        "date": DATE_STR,
        "archive_url": ARCHIVE_URL,
        "checksum_url": CHECKSUM_URL,
        "max_download_bytes": MAX_DOWNLOAD_BYTES,
        "schema_version": SCHEMA_VERSION,
        "day_start_ms": DAY_START_MS,
        "day_end_ms": DAY_END_MS,
    }
    canonical = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


# ---------------------------------------------------------------------------- #
# Acquisition orchestration
# ---------------------------------------------------------------------------- #


def acquire(
    *,
    output_root: Path,
    fail_if_existing: bool = True,
    do_network: bool = True,
) -> AcquisitionResult:
    """Run the Phase 4az acquisition.

    ``do_network=False`` is an internal hook used by tests that pre-stage
    a checksum + ZIP fixture in the staging directory; production
    invocations always use ``do_network=True``.
    """
    output_root = output_root.resolve()
    staging_dir = output_root / "staging" / DATASET_FAMILY / SYMBOL / "2025" / "01"
    raw_dir = output_root / "raw" / DATASET_FAMILY / SYMBOL / "2025" / "01"
    manifests_dir = output_root / "manifests"
    raw_filename = f"{SYMBOL}-aggTrades-{DATE_STR}.zip"
    raw_relpath = f"raw/{DATASET_FAMILY}/{SYMBOL}/2025/01/{raw_filename}"
    final_raw = raw_dir / raw_filename
    final_sha = raw_dir / f"{raw_filename}.sha256"
    manifest_path = manifests_dir / f"{DATASET_FAMILY}__{DATASET_VERSION}.json"
    log_path = manifests_dir / f"{DATASET_FAMILY}__{DATASET_VERSION}_acquisition_log.json"

    staging_zip = staging_dir / f"{raw_filename}.tmp"
    staging_checksum = staging_dir / f"{raw_filename}.CHECKSUM"

    failure_reason: str | None = None
    sha256_hex = ""
    summary: ValidationSummary | None = None

    try:
        # Preflight: refuse to overwrite any existing artefact.
        if fail_if_existing:
            for existing in (final_raw, final_sha, manifest_path, log_path):
                if existing.exists():
                    raise AcquisitionError(
                        f"refusing to overwrite existing artefact: {existing}"
                    )

        # URL allowlist enforcement (also enforced inside _http_get).
        assert_archive_url_allowed(ARCHIVE_URL)
        assert_archive_url_allowed(CHECKSUM_URL)

        # Create staging directory after preflight passes.
        staging_dir.mkdir(parents=True, exist_ok=True)

        # 1. Checksum first.
        if do_network:
            _http_get(CHECKSUM_URL, staging_checksum)
        if not staging_checksum.exists() or staging_checksum.stat().st_size == 0:
            raise AcquisitionError("checksum file is missing or empty after fetch")
        checksum_text = staging_checksum.read_text(encoding="utf-8")
        expected_sha = parse_sha256_from_checksum(checksum_text)

        # 2. Archive ZIP only after checksum is parsed.
        if do_network:
            _http_get(ARCHIVE_URL, staging_zip)
        if not staging_zip.exists() or staging_zip.stat().st_size == 0:
            raise AcquisitionError("archive file is missing or empty after fetch")
        if staging_zip.stat().st_size > MAX_DOWNLOAD_BYTES:
            raise AcquisitionError(
                f"archive size exceeds MAX_DOWNLOAD_BYTES "
                f"({MAX_DOWNLOAD_BYTES})"
            )

        # 3. Verify SHA256.
        sha256_hex = _sha256_file(staging_zip)
        if sha256_hex != expected_sha:
            raise AcquisitionError(
                f"checksum mismatch: expected {expected_sha}, got {sha256_hex}"
            )

        # 4. Validate every row.
        summary = validate_aggtrades_archive(staging_zip)

        # 5. Atomic move staging -> final raw.
        raw_dir.mkdir(parents=True, exist_ok=True)
        staging_zip.replace(final_raw)
        final_sha.write_text(f"{sha256_hex}  {raw_filename}\n", encoding="utf-8")

        # 6. Write manifest.
        _write_manifest(
            manifest_path,
            raw_relpath=raw_relpath,
            sha256_hex=sha256_hex,
            summary=summary,
            capture_config_hash=compute_capture_config_hash(),
        )

        # 7. Write acquisition log.
        _write_acquisition_log(
            log_path,
            status="SUCCESSFUL_ACQUISITION",
            failure_reason=None,
            raw_relpath=raw_relpath,
            sha256_hex=sha256_hex,
            summary=summary,
            archive_url=ARCHIVE_URL,
            checksum_url=CHECKSUM_URL,
            staging_dir=staging_dir,
        )

        # 8. Best-effort staging cleanup on success.
        try:
            if staging_checksum.exists():
                staging_checksum.unlink()
            if staging_zip.exists():
                staging_zip.unlink()
            # Try to remove empty staging dirs going up.
            for parent in (staging_dir, *staging_dir.parents):
                if not parent.is_relative_to(output_root / "staging"):
                    break
                try:
                    parent.rmdir()
                except OSError:
                    break
        except OSError:
            # Non-fatal: leave staging artefacts; success path already complete.
            pass

        return AcquisitionResult(
            status="SUCCESSFUL_ACQUISITION",
            failure_reason=None,
            raw_path=final_raw,
            sha_path=final_sha,
            manifest_path=manifest_path,
            log_path=log_path,
            event_count=summary.event_count,
            start_time_ms=summary.start_time_ms,
            end_time_ms=summary.end_time_ms,
            sha256_hex=sha256_hex,
            staging_preserved=False,
        )

    except (AcquisitionError, AggTradeValidationError, urllib.error.URLError, OSError) as exc:
        failure_reason = f"{type(exc).__name__}: {exc}"
        # Best-effort: write a fail-closed acquisition log into manifests dir
        # if it does not already exist. We deliberately do NOT write a
        # manifest on failure.
        try:
            if not log_path.exists():
                _write_acquisition_log(
                    log_path,
                    status="FAIL_CLOSED_NO_ACQUISITION",
                    failure_reason=failure_reason,
                    raw_relpath=None,
                    sha256_hex=None,
                    summary=None,
                    archive_url=ARCHIVE_URL,
                    checksum_url=CHECKSUM_URL,
                    staging_dir=staging_dir,
                )
        except Exception:  # noqa: BLE001
            # Logging the failure is best-effort; the caller still gets the
            # AcquisitionResult.
            pass

        return AcquisitionResult(
            status="FAIL_CLOSED_NO_ACQUISITION",
            failure_reason=failure_reason,
            raw_path=None,
            sha_path=None,
            manifest_path=None,
            log_path=log_path if log_path.exists() else None,
            event_count=0,
            start_time_ms=0,
            end_time_ms=0,
            sha256_hex="",
            staging_preserved=staging_dir.exists(),
        )


# ---------------------------------------------------------------------------- #
# CLI
# ---------------------------------------------------------------------------- #


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Phase 4az: acquire one BTCUSDT public aggTrades daily archive "
            "from data.binance.vision under strict integrity controls."
        ),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("data/microstructure"),
        help="Output root (must resolve under data/microstructure/).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned paths and authorized URLs without downloading.",
    )
    parser.add_argument(
        "--fail-if-existing",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Refuse to run if final artefacts already exist (default: true).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)
    output_root: Path = args.output_root.resolve()

    # Refuse output roots that would write outside data/microstructure/. This
    # mirrors the Phase 4aw RawWriter discipline and protects the project
    # data tree.
    if "data/microstructure" not in str(output_root).replace("\\", "/").lower():
        print(
            f"refusing to use --output-root outside data/microstructure/: "
            f"{output_root}",
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        print("Phase 4az dry-run plan:")
        print(f"  symbol         : {SYMBOL}")
        print(f"  date           : {DATE_STR}")
        print(f"  dataset_family : {DATASET_FAMILY}")
        print(f"  archive_url    : {ARCHIVE_URL}")
        print(f"  checksum_url   : {CHECKSUM_URL}")
        print(f"  output_root    : {output_root}")
        print(
            f"  planned_raw    : "
            f"{output_root}/raw/{DATASET_FAMILY}/{SYMBOL}/2025/01/"
            f"{SYMBOL}-aggTrades-{DATE_STR}.zip"
        )
        print(
            f"  planned_manifest: "
            f"{output_root}/manifests/{DATASET_FAMILY}__{DATASET_VERSION}.json"
        )
        print("No download will be performed.")
        return 0

    result = acquire(
        output_root=output_root,
        fail_if_existing=args.fail_if_existing,
        do_network=True,
    )

    if result.status == "SUCCESSFUL_ACQUISITION":
        print("Phase 4az: SUCCESSFUL_ACQUISITION")
        print(f"  raw            : {result.raw_path}")
        print(f"  sha256         : {result.sha256_hex}")
        print(f"  event_count    : {result.event_count}")
        print(f"  start_time_ms  : {result.start_time_ms}")
        print(f"  end_time_ms    : {result.end_time_ms}")
        print(f"  manifest       : {result.manifest_path}")
        print(f"  acquisition_log: {result.log_path}")
        return 0

    print("Phase 4az: FAIL_CLOSED_NO_ACQUISITION", file=sys.stderr)
    print(f"  failure_reason   : {result.failure_reason}", file=sys.stderr)
    print(f"  staging_preserved: {result.staging_preserved}", file=sys.stderr)
    if result.log_path is not None:
        print(f"  acquisition_log  : {result.log_path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
