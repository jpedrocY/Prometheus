"""Phase 4bl-C — Multi-Day aggTrades Acquisition Execution (BTCUSDT, 90 UTC days).

Standalone acquisition script authorised by the Phase 4bl-B
authorization-boundary memo. Acquires exactly 90 contiguous Binance
USDⓈ-M Futures aggTrades daily archives for BTCUSDT covering UTC dates
2024-12-01 through 2025-02-28 inclusive from the public
``data.binance.vision`` archive, validates a small row sample per ZIP
against the Phase 4ax validator, and writes raw archives plus a sibling
v002 multi-day manifest + acquisition log under the gitignored
``data/microstructure/`` tree.

This script is intentionally narrow:

- Python standard library only (``urllib.request``, ``zipfile``,
  ``csv``, ``hashlib``, ``json``, ``argparse``, ``random``, ``time``,
  ``platform``, ``uuid``, ``subprocess``, ...) plus the Phase 4aw /
  4ax microstructure scaffold modules (``validate_aggtrade_payload``,
  ``AggTradeValidationError``, ``TakerSide``).
- Network access only to ``https://data.binance.vision`` URLs matching
  the locked daily futures aggTrades path pattern. No
  ``fapi.binance.com``, no ``api.binance.com``, no
  ``stream.binance.com``, no authenticated APIs, no private endpoints,
  no user streams, no WebSockets, no listenKey lifecycle, no
  credentials, no ``.env``, no MCP / Graphify / ``.mcp.json``.
- For each locked date:
  1. The ``.CHECKSUM`` companion file is downloaded first.
  2. The archive ``.zip`` is downloaded only after the companion is
     parsed.
  3. The downloaded ZIP's local SHA256 is verified against the
     companion value bit-for-bit.
  4. ``zipfile.ZipFile.testzip()`` is run to confirm decompression
     integrity.
  5. A bounded row sample (first 100, last 100, up to 100 deterministic
     middle rows) is validated via the Phase 4ax
     ``validate_aggtrade_payload`` function.
  6. The ZIP is atomically moved into ``data/microstructure/raw/...``
     with a paired ``.sha256`` sidecar in canonical Phase 4bb-F
     format.
- The existing one-day Phase 4az fixture (``2025-01-15``) is
  detected, its SHA verified against the recorded value, and reused
  in place. The script MUST NOT overwrite the existing fixture even
  if Binance has somehow re-published a different archive for that
  date.
- Per-date failure (HTTP 404, checksum mismatch, decompression
  failure, row-sample validation failure, retry exhaustion,
  finalisation failure) is recorded explicitly per the Phase 4bl-B
  §12 failure / retry / missing-file policy. No date is silently
  skipped. No date is substituted. There is no fallback to APIs.
- Exactly one acquisition log and one v002 multi-day manifest are
  written, each with paired SHA256 sidecars.
- All local outputs live under the gitignored ``data/microstructure/``
  tree; the script verifies gitignore coverage before writing.

Phase 4bl-C is acquisition-only. It MUST NOT normalize, derive,
compute features, compute labels, run gates, create gate reports,
create successor-state artefacts, run diagnostics, compute label
statistics, compute returns / PnL / strategy metrics, train ML,
create signals, create strategy logic, or run backtests. It MUST
NOT flip ``research_eligible`` or transition
``eligibility_gate_status`` on any manifest. The manifest is
written with ``research_eligible=false`` and
``eligibility_gate_status="pending"`` per the Phase 4bl-B §8 design.
"""

from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import os
import platform
import random
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

# Make the in-repo ``src/prometheus`` package importable when this
# script is invoked directly (``python scripts/phase4bl_c_*.py``). The
# pyproject.toml pytest config already prepends ``src`` for tests; the
# CLI path needs the same treatment without relying on an editable
# install.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# Phase 4ax / 4aw scaffold imports. The validator is used for the
# row-sample smoke check on each acquired ZIP.
from prometheus.research.microstructure.aggtrades import (  # noqa: E402
    AggTradeValidationError,
    validate_aggtrade_payload,
)

# ---------------------------------------------------------------------------- #
# Phase constants (predeclared by the Phase 4bl-B operator brief)
# ---------------------------------------------------------------------------- #

PHASE_ID = "4bl-C"
SOURCE_PHASE_BOUNDARY = "4bl-B"
BASE_COMMIT_SHA = "dc2240e7a43047823c8b964d52112432b7a61c79"  # Phase 4bl-B base

DATASET_FAMILY = "microstructure_raw_aggtrades_v001"
DATASET_VERSION = "v002"
SCHEMA_VERSION = "v001"
SYMBOL = "BTCUSDT"
SYMBOL_LIST: tuple[str, ...] = (SYMBOL,)

DATE_START = date(2024, 12, 1)
DATE_END = date(2025, 2, 28)
EXPECTED_DATE_COUNT = 90

CAPTURE_MODE = "historical_archive"
SOURCE_LABEL = "binance_data_archive"
SOURCE_CLASS = "public_unauthenticated_daily_archive"
ENDPOINT_LABEL = "data.binance.vision/data/futures/um/daily/aggTrades"
ENDPOINT_DOCS_REFERENCE = (
    "https://github.com/binance/binance-public-data#trades"
    " (futures aggTrades daily archive convention)"
)

ARCHIVE_URL_TEMPLATE = (
    "https://data.binance.vision/data/futures/um/daily/aggTrades/"
    "BTCUSDT/BTCUSDT-aggTrades-{date}.zip"
)
CHECKSUM_URL_TEMPLATE = ARCHIVE_URL_TEMPLATE + ".CHECKSUM"

# Allowed network host. Any other host is denied.
ALLOWED_HOSTS: tuple[str, ...] = ("data.binance.vision",)

# Maximum allowed download size (5 GiB per Phase 4ay precedent).
MAX_DOWNLOAD_BYTES = 5 * 1024 * 1024 * 1024

# Existing one-day Phase 4az fixture for 2025-01-15.
EXISTING_FIXTURE_DATE = "2025-01-15"
EXISTING_FIXTURE_SHA256 = (
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"
)

# Retry policy (Phase 4bl-B §12).
MAX_RETRIES = 3
RETRY_BACKOFFS_SECONDS: tuple[int, ...] = (2, 4, 8)
PER_ATTEMPT_TIMEOUT_SECONDS = 60
PER_DATE_BUDGET_SECONDS = 5 * 60  # 5 minutes

# Row-sample validation policy (Phase 4bl-B §11.5).
ROW_SAMPLE_HEAD = 100
ROW_SAMPLE_TAIL = 100
ROW_SAMPLE_MIDDLE = 100


# ---------------------------------------------------------------------------- #
# Errors
# ---------------------------------------------------------------------------- #


class AcquisitionFailClosed(RuntimeError):
    """Raised when the acquisition orchestrator must halt the entire run."""


# ---------------------------------------------------------------------------- #
# Date list generation
# ---------------------------------------------------------------------------- #


def generate_locked_date_list() -> list[str]:
    """Return the locked 90-date ISO-8601 list (chronologically sorted)."""
    out: list[str] = []
    cur = DATE_START
    while cur <= DATE_END:
        out.append(cur.isoformat())
        cur = cur + timedelta(days=1)
    if len(out) != EXPECTED_DATE_COUNT:
        raise AcquisitionFailClosed(
            f"date list cardinality mismatch: expected "
            f"{EXPECTED_DATE_COUNT}, got {len(out)}"
        )
    if EXISTING_FIXTURE_DATE not in out:
        raise AcquisitionFailClosed(
            f"existing fixture date {EXISTING_FIXTURE_DATE} missing from "
            f"locked range"
        )
    return out


# ---------------------------------------------------------------------------- #
# URL allowlist
# ---------------------------------------------------------------------------- #


_FORBIDDEN_URL_SUBSTRINGS: tuple[str, ...] = (
    "fapi.binance.com",
    "api.binance.com",
    "stream.binance.com",
    "/fapi/",
    "/api/v1/",
    "/api/v3/",
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
    "/monthly/",
    "/data/spot/",
    "/data/option/",
    "/data/futures/cm/",
    "/klines/",
    "/markPriceKlines/",
    "/indexPriceKlines/",
    "/premiumIndexKlines/",
    "/metrics/",
    "/fundingRate/",
    "/openInterest/",
)


def assert_archive_url_allowed(url: str) -> None:
    """Reject any URL outside the allowlist or pointing at non-archive paths."""
    if not isinstance(url, str) or not url:
        raise AcquisitionFailClosed("URL must be a non-empty string")
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("https",):
        raise AcquisitionFailClosed(
            f"URL scheme must be https, got {parsed.scheme!r} for {url!r}"
        )
    if parsed.hostname not in ALLOWED_HOSTS:
        raise AcquisitionFailClosed(
            f"URL host {parsed.hostname!r} is not in the allowed set "
            f"{ALLOWED_HOSTS!r} for {url!r}"
        )
    if not parsed.path.startswith("/data/futures/um/daily/aggTrades/BTCUSDT/"):
        raise AcquisitionFailClosed(
            f"URL path {parsed.path!r} is not the locked daily aggTrades "
            f"BTCUSDT path pattern"
        )
    if "BTCUSDT-aggTrades-" not in parsed.path:
        raise AcquisitionFailClosed(
            f"URL path {parsed.path!r} does not match the locked filename "
            f"pattern"
        )
    lowered = url.lower()
    for token in _FORBIDDEN_URL_SUBSTRINGS:
        if token.lower() in lowered:
            raise AcquisitionFailClosed(
                f"URL {url!r} contains forbidden token {token!r}"
            )


# ---------------------------------------------------------------------------- #
# Output path discipline
# ---------------------------------------------------------------------------- #


_MICROSTRUCTURE_ROOT = "data/microstructure"


def assert_path_under_microstructure(path: Path, output_root: Path) -> None:
    """Reject any path that would resolve outside data/microstructure/."""
    resolved = path.resolve()
    output_root_resolved = output_root.resolve()
    try:
        resolved.relative_to(output_root_resolved)
    except ValueError as exc:
        raise AcquisitionFailClosed(
            f"path {path!r} resolves outside output_root {output_root!r}"
        ) from exc
    # Also explicitly check that the output_root itself is under
    # data/microstructure. The CLI also enforces this.
    norm = str(output_root_resolved).replace("\\", "/").lower()
    if _MICROSTRUCTURE_ROOT not in norm:
        raise AcquisitionFailClosed(
            f"output_root {output_root!r} is not under "
            f"{_MICROSTRUCTURE_ROOT}"
        )


# ---------------------------------------------------------------------------- #
# Gitignore verification
# ---------------------------------------------------------------------------- #


def verify_gitignored(path: Path, *, repo_root: Path) -> bool:
    """Return True if ``git check-ignore --verbose`` reports the path is ignored."""
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--verbose", str(path)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
            cwd=str(repo_root),
        )
    except (OSError, subprocess.SubprocessError):
        return False
    # git check-ignore exit 0 = ignored, 1 = not ignored, 128 = error.
    return result.returncode == 0


# ---------------------------------------------------------------------------- #
# Network fetch
# ---------------------------------------------------------------------------- #


def _http_get_bytes(url: str) -> bytes:
    """Download ``url`` into memory with a size cap. Returns content bytes."""
    assert_archive_url_allowed(url)
    request = urllib.request.Request(url, method="GET")
    buf = bytearray()
    with urllib.request.urlopen(  # noqa: S310 (allow-listed)
        request, timeout=PER_ATTEMPT_TIMEOUT_SECONDS
    ) as response:
        final_url = response.geturl()
        if final_url != url:
            assert_archive_url_allowed(final_url)
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            buf.extend(chunk)
            if len(buf) > MAX_DOWNLOAD_BYTES:
                raise AcquisitionFailClosed(
                    f"download exceeded MAX_DOWNLOAD_BYTES "
                    f"({MAX_DOWNLOAD_BYTES}) for {url}"
                )
    if not buf:
        raise urllib.error.URLError(f"empty response for {url}")
    return bytes(buf)


# ---------------------------------------------------------------------------- #
# Checksum parsing
# ---------------------------------------------------------------------------- #


def parse_sha256_from_checksum(content: str | bytes) -> str:
    """Parse the first 64 hex characters of a Binance ``.CHECKSUM`` file body."""
    if isinstance(content, bytes):
        try:
            content = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AcquisitionFailClosed(
                f"checksum content is not valid UTF-8: {exc}"
            ) from exc
    if not isinstance(content, str):
        raise AcquisitionFailClosed("checksum content must be a str or bytes")
    stripped = content.strip()
    if not stripped:
        raise AcquisitionFailClosed("checksum content is empty")
    first_token = stripped.split()[0] if stripped.split() else ""
    if len(first_token) != 64:
        raise AcquisitionFailClosed(
            f"checksum prefix is not 64 hex characters: {first_token!r}"
        )
    if not all(c in "0123456789abcdefABCDEF" for c in first_token):
        raise AcquisitionFailClosed(
            f"checksum prefix is not hex: {first_token!r}"
        )
    return first_token.lower()


# ---------------------------------------------------------------------------- #
# SHA256 utilities
# ---------------------------------------------------------------------------- #


def sha256_file(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Return the lowercase hex SHA256 of the file's bytes (chunked)."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def make_sidecar_body(sha256_hex: str, basename: str) -> str:
    """Return the canonical Phase 4bb-F sidecar body: ``<sha>  <basename>\\n``."""
    if not isinstance(sha256_hex, str) or len(sha256_hex) != 64:
        raise AcquisitionFailClosed(
            f"sha256_hex must be a 64-char hex string; got {sha256_hex!r}"
        )
    if not all(c in "0123456789abcdefABCDEF" for c in sha256_hex):
        raise AcquisitionFailClosed(
            f"sha256_hex must contain only hex characters; got {sha256_hex!r}"
        )
    if not isinstance(basename, str) or not basename:
        raise AcquisitionFailClosed("basename must be a non-empty string")
    if "/" in basename or "\\" in basename:
        raise AcquisitionFailClosed(
            f"basename must not contain path separators; got {basename!r}"
        )
    return f"{sha256_hex.lower()}  {basename}\n"


# ---------------------------------------------------------------------------- #
# Atomic write helpers
# ---------------------------------------------------------------------------- #


def atomic_write_bytes(target: Path, content: bytes) -> None:
    """Atomically write ``content`` to ``target`` via tempfile + os.replace.

    Refuses to overwrite a non-identical existing file. If the existing
    file's bytes are identical, the write is a no-op.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        existing = target.read_bytes()
        if existing == content:
            return
        raise AcquisitionFailClosed(
            f"refusing to overwrite non-identical existing file: {target}"
        )
    tmp = target.with_suffix(target.suffix + ".tmp")
    with tmp.open("wb") as fh:
        fh.write(content)
        try:
            fh.flush()
            os.fsync(fh.fileno())
        except (OSError, AttributeError):
            pass
    os.replace(tmp, target)


def atomic_write_text(target: Path, content: str) -> None:
    atomic_write_bytes(target, content.encode("utf-8"))


def atomic_move_file(src: Path, dst: Path) -> None:
    """Atomically move ``src`` to ``dst``. Refuses overwrite of non-identical dst."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst_sha = sha256_file(dst)
        src_sha = sha256_file(src)
        if dst_sha == src_sha:
            # No-op; remove source.
            with contextlib.suppress(OSError):
                src.unlink()
            return
        raise AcquisitionFailClosed(
            f"refusing to overwrite non-identical existing file at "
            f"{dst}: src_sha={src_sha}, dst_sha={dst_sha}"
        )
    os.replace(src, dst)


# ---------------------------------------------------------------------------- #
# CSV row decoding (mirrors Phase 4az _row_to_payload)
# ---------------------------------------------------------------------------- #


_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "a": ("agg_trade_id", "aggregate_trade_id", "a"),
    "p": ("price", "p"),
    "q": ("quantity", "q"),
    "f": ("first_trade_id", "f"),
    "l": ("last_trade_id", "l"),
    "T": ("transact_time", "trade_time", "T"),
    "m": ("is_buyer_maker", "m"),
}

_HEADERLESS_ORDER: tuple[str, ...] = ("a", "p", "q", "f", "l", "T", "m")


def _resolve_header_mapping(raw_header: list[str]) -> dict[str, int] | None:
    """Map header column names to Phase 4ax payload field positions."""
    if not raw_header:
        return None
    first_cell = raw_header[0].strip()
    try:
        int(first_cell)
        return None
    except ValueError:
        pass

    mapping: dict[str, int] = {}
    lowered = [cell.strip().lower() for cell in raw_header]
    for field_name, synonyms in _HEADER_ALIASES.items():
        for idx, cell in enumerate(lowered):
            if cell in {syn.lower() for syn in synonyms}:
                mapping[field_name] = idx
                break
        if field_name not in mapping:
            raise AcquisitionFailClosed(
                f"CSV header missing required field {field_name!r} "
                f"(expected one of {synonyms!r}); got header={raw_header!r}"
            )
    return mapping


def _coerce_buyer_is_maker(token: str) -> bool:
    if token in ("true", "True", "TRUE"):
        return True
    if token in ("false", "False", "FALSE"):
        return False
    raise AcquisitionFailClosed(
        f"is_buyer_maker token must be true/True/TRUE/false/False/FALSE, "
        f"got {token!r}"
    )


def _row_to_payload(
    row: list[str],
    mapping: dict[str, int] | None,
) -> dict[str, object]:
    if mapping is None:
        if len(row) < len(_HEADERLESS_ORDER):
            raise AcquisitionFailClosed(
                f"headerless row has too few columns: expected at least "
                f"{len(_HEADERLESS_ORDER)}, got {len(row)}; row={row!r}"
            )
        getters = {field_name: row[idx] for idx, field_name in enumerate(_HEADERLESS_ORDER)}
    else:
        getters = {field_name: row[idx] for field_name, idx in mapping.items()}

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
# ZIP inventory: decompress once for row_count, time bounds, agg-id bounds,
# and bounded row-sample validation
# ---------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ZipInventory:
    row_count: int
    first_trade_time_ms: int
    last_trade_time_ms: int
    min_agg_trade_id: int
    max_agg_trade_id: int
    row_sample_validation_passed: bool
    row_sample_failure_reason: str | None
    decompression_failure_reason: str | None


def _select_sample_indices(
    row_count: int,
    *,
    head: int,
    tail: int,
    middle: int,
    seed: int,
) -> list[int]:
    """Return sorted unique indices to sample for row-sample validation."""
    if row_count <= 0:
        return []
    indices: set[int] = set()
    for i in range(min(head, row_count)):
        indices.add(i)
    for i in range(min(tail, row_count)):
        indices.add(row_count - 1 - i)
    if middle > 0 and row_count > head + tail:
        # Deterministic sampling over the middle band.
        rng = random.Random(seed)
        middle_start = head
        middle_end = row_count - tail
        if middle_end > middle_start:
            for _ in range(min(middle, middle_end - middle_start)):
                indices.add(rng.randrange(middle_start, middle_end))
    return sorted(indices)


def inventory_and_validate_zip(zip_path: Path, *, date_str: str) -> ZipInventory:
    """Decompress the ZIP once and compute manifest inventory + row-sample check.

    Failures in decompression or row-sample validation are returned as
    fields on the ZipInventory rather than raised, so the orchestrator
    can record per-date status and continue. This function does not
    raise except for unexpected internal errors.
    """
    try:
        with zipfile.ZipFile(zip_path) as zf:
            bad = zf.testzip()
            if bad is not None:
                return ZipInventory(
                    row_count=0,
                    first_trade_time_ms=0,
                    last_trade_time_ms=0,
                    min_agg_trade_id=0,
                    max_agg_trade_id=0,
                    row_sample_validation_passed=False,
                    row_sample_failure_reason=None,
                    decompression_failure_reason=(
                        f"testzip() reported corrupt member: {bad!r}"
                    ),
                )
            names = [n for n in zf.namelist() if not n.endswith("/")]
            if not names:
                return ZipInventory(
                    row_count=0,
                    first_trade_time_ms=0,
                    last_trade_time_ms=0,
                    min_agg_trade_id=0,
                    max_agg_trade_id=0,
                    row_sample_validation_passed=False,
                    row_sample_failure_reason=None,
                    decompression_failure_reason=(
                        "ZIP contains no non-directory members"
                    ),
                )
            csv_members = [n for n in names if n.lower().endswith(".csv")]
            if not csv_members and len(names) == 1:
                csv_members = names
            if len(csv_members) != 1:
                return ZipInventory(
                    row_count=0,
                    first_trade_time_ms=0,
                    last_trade_time_ms=0,
                    min_agg_trade_id=0,
                    max_agg_trade_id=0,
                    row_sample_validation_passed=False,
                    row_sample_failure_reason=None,
                    decompression_failure_reason=(
                        f"ZIP must contain exactly one CSV member; "
                        f"got {csv_members!r} of {names!r}"
                    ),
                )
            member = csv_members[0]

            # Pass 1: row count + min/max trade time + min/max agg id +
            # capture head and tail rows for row-sample validation.
            head_rows: list[tuple[dict[str, int] | None, list[str]]] = []
            tail_rows: list[tuple[dict[str, int] | None, list[str]]] = []
            mapping: dict[str, int] | None = None
            row_count = 0
            first_trade_time_ms = 0
            last_trade_time_ms = 0
            min_agg_id: int | None = None
            max_agg_id: int | None = None
            try:
                with zf.open(member, "r") as raw:
                    text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
                    reader = csv.reader(text)
                    first_row = True
                    for row in reader:
                        if not row:
                            continue
                        if first_row:
                            mapping = _resolve_header_mapping(row)
                            first_row = False
                            if mapping is not None:
                                continue
                        # Extract trade time and agg id for bounds without
                        # full payload validation (to avoid full-row gate
                        # in Phase 4bl-C).
                        if mapping is None:
                            a_idx = 0
                            t_idx = 5
                        else:
                            a_idx = mapping["a"]
                            t_idx = mapping["T"]
                        try:
                            agg_id = int(row[a_idx])
                            trade_time = int(row[t_idx])
                        except (ValueError, IndexError) as exc:
                            return ZipInventory(
                                row_count=0,
                                first_trade_time_ms=0,
                                last_trade_time_ms=0,
                                min_agg_trade_id=0,
                                max_agg_trade_id=0,
                                row_sample_validation_passed=False,
                                row_sample_failure_reason=None,
                                decompression_failure_reason=(
                                    f"row {row_count} could not be parsed: "
                                    f"{type(exc).__name__}: {exc}"
                                ),
                            )
                        if min_agg_id is None or agg_id < min_agg_id:
                            min_agg_id = agg_id
                        if max_agg_id is None or agg_id > max_agg_id:
                            max_agg_id = agg_id
                        if row_count == 0:
                            first_trade_time_ms = trade_time
                            last_trade_time_ms = trade_time
                        else:
                            if trade_time < first_trade_time_ms:
                                first_trade_time_ms = trade_time
                            if trade_time > last_trade_time_ms:
                                last_trade_time_ms = trade_time
                        if len(head_rows) < ROW_SAMPLE_HEAD:
                            head_rows.append((mapping, row))
                        else:
                            tail_rows.append((mapping, row))
                            if len(tail_rows) > ROW_SAMPLE_TAIL:
                                tail_rows.pop(0)
                        row_count += 1
            except (zipfile.BadZipFile, OSError, EOFError) as exc:
                return ZipInventory(
                    row_count=0,
                    first_trade_time_ms=0,
                    last_trade_time_ms=0,
                    min_agg_trade_id=0,
                    max_agg_trade_id=0,
                    row_sample_validation_passed=False,
                    row_sample_failure_reason=None,
                    decompression_failure_reason=(
                        f"decompression failed: {type(exc).__name__}: {exc}"
                    ),
                )

            if row_count == 0:
                return ZipInventory(
                    row_count=0,
                    first_trade_time_ms=0,
                    last_trade_time_ms=0,
                    min_agg_trade_id=0,
                    max_agg_trade_id=0,
                    row_sample_validation_passed=False,
                    row_sample_failure_reason=None,
                    decompression_failure_reason="ZIP contained zero data rows",
                )

            # Pass 2: middle-row sampling. We already captured head and
            # tail above; here we sample up to ROW_SAMPLE_MIDDLE middle
            # rows deterministically by streaming the file again.
            middle_indices = _select_sample_indices(
                row_count,
                head=0,
                tail=0,
                middle=ROW_SAMPLE_MIDDLE,
                seed=int(date_str.replace("-", "")),
            )
            # Restrict middle band: [ROW_SAMPLE_HEAD, row_count - ROW_SAMPLE_TAIL).
            band_lo = ROW_SAMPLE_HEAD
            band_hi = row_count - ROW_SAMPLE_TAIL
            middle_target: set[int] = set()
            if band_hi > band_lo:
                rng = random.Random(int(date_str.replace("-", "")))
                count = min(ROW_SAMPLE_MIDDLE, band_hi - band_lo)
                while len(middle_target) < count:
                    middle_target.add(rng.randrange(band_lo, band_hi))
            middle_rows: list[tuple[dict[str, int] | None, list[str]]] = []
            if middle_target:
                with zf.open(member, "r") as raw:
                    text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
                    reader = csv.reader(text)
                    first_row = True
                    idx = 0
                    for row in reader:
                        if not row:
                            continue
                        if first_row:
                            map_check = _resolve_header_mapping(row)
                            first_row = False
                            if map_check is not None:
                                continue
                        if idx in middle_target:
                            middle_rows.append((mapping, row))
                            if len(middle_rows) >= len(middle_target):
                                break
                        idx += 1

            # Now run row-sample validation against head, tail, and
            # middle row sets.
            failure_reason: str | None = None
            for mapping_used, row_payload in head_rows + tail_rows + middle_rows:
                try:
                    payload = _row_to_payload(row_payload, mapping_used)
                except AcquisitionFailClosed as exc:
                    failure_reason = (
                        f"row decoding failed: {exc}"
                    )
                    break
                try:
                    validated = validate_aggtrade_payload(payload)
                except AggTradeValidationError as exc:
                    failure_reason = (
                        f"row validation failed: {exc}"
                    )
                    break
                else:
                    # Touch validated to ensure no dead-code stripping.
                    _ = validated.taker_side  # noqa: F841

            row_sample_passed = failure_reason is None
            # Avoid unused-variable warning for middle_indices, kept for
            # deterministic-seed transparency in tests.
            _ = middle_indices  # noqa: F841

            assert min_agg_id is not None
            assert max_agg_id is not None
            return ZipInventory(
                row_count=row_count,
                first_trade_time_ms=first_trade_time_ms,
                last_trade_time_ms=last_trade_time_ms,
                min_agg_trade_id=min_agg_id,
                max_agg_trade_id=max_agg_id,
                row_sample_validation_passed=row_sample_passed,
                row_sample_failure_reason=failure_reason,
                decompression_failure_reason=None,
            )
    except (zipfile.BadZipFile, OSError) as exc:
        return ZipInventory(
            row_count=0,
            first_trade_time_ms=0,
            last_trade_time_ms=0,
            min_agg_trade_id=0,
            max_agg_trade_id=0,
            row_sample_validation_passed=False,
            row_sample_failure_reason=None,
            decompression_failure_reason=(
                f"ZIP open failed: {type(exc).__name__}: {exc}"
            ),
        )


# ---------------------------------------------------------------------------- #
# Per-date acquisition logic
# ---------------------------------------------------------------------------- #


def _expected_local_paths(date_str: str, output_root: Path) -> tuple[Path, Path]:
    yyyy = date_str[0:4]
    mm = date_str[5:7]
    raw_dir = output_root / "raw" / DATASET_FAMILY / SYMBOL / yyyy / mm
    raw_filename = f"{SYMBOL}-aggTrades-{date_str}.zip"
    return raw_dir / raw_filename, raw_dir / f"{raw_filename}.sha256"


def _staging_paths(date_str: str, output_root: Path) -> tuple[Path, Path, Path]:
    yyyy = date_str[0:4]
    mm = date_str[5:7]
    staging = output_root / "staging" / DATASET_FAMILY / SYMBOL / yyyy / mm
    raw_filename = f"{SYMBOL}-aggTrades-{date_str}.zip"
    return (
        staging,
        staging / f"{raw_filename}.tmp",
        staging / f"{raw_filename}.CHECKSUM",
    )


@dataclass
class DateResult:
    date: str
    expected_url: str
    expected_checksum_url: str
    local_zip_path: str
    local_sidecar_path: str
    status: str
    sha256: str | None
    sha256_from_companion: str | None
    size_bytes: int | None
    row_count: int | None
    first_trade_time_ms: int | None
    last_trade_time_ms: int | None
    min_agg_trade_id: int | None
    max_agg_trade_id: int | None
    retry_count: int
    failure_reason: str | None
    acquired_at_unix_ms: int | None
    events: list[dict[str, object]] = field(default_factory=list)


_VALID_STATUSES: tuple[str, ...] = (
    "acquired_verified",
    "missing_404",
    "checksum_mismatch",
    "checksum_companion_unavailable",
    "decompression_failure",
    "row_sample_validation_failure",
    "finalisation_failure",
    "retry_exhausted",
)


def _now_ms() -> int:
    return int(time.time() * 1000)


def _emit_event(
    events: list[dict[str, object]],
    *,
    event_type: str,
    date_str: str,
    details: dict[str, object] | None = None,
) -> None:
    events.append(
        {
            "timestamp_unix_ms": _now_ms(),
            "event_type": event_type,
            "date": date_str,
            "details": details or {},
        }
    )


def _try_download_with_retry(
    url: str,
    date_str: str,
    events: list[dict[str, object]],
    *,
    do_network: bool = True,
    fake_response: bytes | None = None,
    fake_status: int | None = None,
) -> tuple[bytes | None, int, str | None]:
    """Download ``url`` with retry policy. Returns (content, retries, error).

    On HTTP 404, returns ``(None, retries, "missing_404")`` without retry.
    On exhaustion, returns ``(None, retries, "retry_exhausted")``.
    On success, returns ``(content, retries, None)``.

    ``do_network=False`` is a test-only hook that returns fake_response
    or fake_status without any network call.
    """
    if not do_network:
        if fake_status == 404:
            return None, 0, "missing_404"
        if fake_response is not None:
            return fake_response, 0, None
        return None, 0, "no_fake_response_supplied"

    retries = 0
    start_unix_ms = _now_ms()
    last_error: str | None = None
    while True:
        attempt_event = {
            "url": url,
            "retry_count": retries,
            "attempt_started_unix_ms": _now_ms(),
        }
        _emit_event(events, event_type="download_attempt", date_str=date_str, details=attempt_event)
        try:
            content = _http_get_bytes(url)
            _emit_event(
                events,
                event_type="download_success",
                date_str=date_str,
                details={"url": url, "retry_count": retries, "size_bytes": len(content)},
            )
            return content, retries, None
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                _emit_event(
                    events,
                    event_type="download_404",
                    date_str=date_str,
                    details={"url": url, "retry_count": retries},
                )
                return None, retries, "missing_404"
            last_error = f"HTTPError {exc.code}: {exc.reason}"
        except (urllib.error.URLError, AcquisitionFailClosed, OSError, TimeoutError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"

        _emit_event(
            events,
            event_type="download_failure",
            date_str=date_str,
            details={"url": url, "retry_count": retries, "error": last_error},
        )

        if retries >= MAX_RETRIES:
            return None, retries, "retry_exhausted"
        # Check per-date wallclock budget before backoff.
        elapsed = (_now_ms() - start_unix_ms) / 1000.0
        if elapsed >= PER_DATE_BUDGET_SECONDS:
            return None, retries, "retry_exhausted"
        backoff = RETRY_BACKOFFS_SECONDS[min(retries, len(RETRY_BACKOFFS_SECONDS) - 1)]
        # Add small jitter up to ±25% to avoid thundering herd.
        jitter = random.uniform(-0.25, 0.25)
        sleep_s = max(0.1, backoff * (1.0 + jitter))
        time.sleep(sleep_s)
        retries += 1


def _commit_sha_or_pending() -> str:
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
    except (OSError, subprocess.SubprocessError):
        pass
    return "pending_commit_sha"


# ---------------------------------------------------------------------------- #
# Capture-config hash
# ---------------------------------------------------------------------------- #


def compute_capture_config_hash(date_list: list[str], code_commit_sha: str) -> str:
    payload = {
        "phase_id": PHASE_ID,
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "schema_version": SCHEMA_VERSION,
        "symbol_list": list(SYMBOL_LIST),
        "date_start": DATE_START.isoformat(),
        "date_end": DATE_END.isoformat(),
        "date_count": EXPECTED_DATE_COUNT,
        "date_list": date_list,
        "archive_url_template": ARCHIVE_URL_TEMPLATE,
        "checksum_url_template": CHECKSUM_URL_TEMPLATE,
        "endpoint_label": ENDPOINT_LABEL,
        "capture_mode": CAPTURE_MODE,
        "max_download_bytes": MAX_DOWNLOAD_BYTES,
        "max_retries": MAX_RETRIES,
        "row_sample_head": ROW_SAMPLE_HEAD,
        "row_sample_tail": ROW_SAMPLE_TAIL,
        "row_sample_middle": ROW_SAMPLE_MIDDLE,
        "code_commit_sha": code_commit_sha,
    }
    canonical = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


# ---------------------------------------------------------------------------- #
# Acquisition orchestration
# ---------------------------------------------------------------------------- #


def acquire_one_date(
    date_str: str,
    *,
    output_root: Path,
    events: list[dict[str, object]],
    do_network: bool = True,
) -> DateResult:
    """Acquire one locked date and return its result.

    Internal helper. Never raises; all failures are recorded on the
    returned :class:`DateResult` so the orchestrator can continue.
    """
    final_zip, final_sha = _expected_local_paths(date_str, output_root)
    staging_dir, staging_zip, staging_chk = _staging_paths(date_str, output_root)
    expected_url = ARCHIVE_URL_TEMPLATE.format(date=date_str)
    expected_chk_url = CHECKSUM_URL_TEMPLATE.format(date=date_str)
    assert_archive_url_allowed(expected_url)
    assert_archive_url_allowed(expected_chk_url)
    assert_path_under_microstructure(final_zip, output_root)
    assert_path_under_microstructure(final_sha, output_root)
    assert_path_under_microstructure(staging_zip, output_root)
    assert_path_under_microstructure(staging_chk, output_root)

    raw_relpath = final_zip.relative_to(output_root.parent).as_posix()
    sidecar_relpath = final_sha.relative_to(output_root.parent).as_posix()

    result = DateResult(
        date=date_str,
        expected_url=expected_url,
        expected_checksum_url=expected_chk_url,
        local_zip_path=raw_relpath,
        local_sidecar_path=sidecar_relpath,
        status="retry_exhausted",  # default, overwritten by every path below
        sha256=None,
        sha256_from_companion=None,
        size_bytes=None,
        row_count=None,
        first_trade_time_ms=None,
        last_trade_time_ms=None,
        min_agg_trade_id=None,
        max_agg_trade_id=None,
        retry_count=0,
        failure_reason=None,
        acquired_at_unix_ms=None,
        events=events,
    )

    # ------------------------------------------------------------------ #
    # Existing fixture handling (Phase 4bl-B §14)
    # ------------------------------------------------------------------ #
    if date_str == EXISTING_FIXTURE_DATE and final_zip.exists():
        _emit_event(
            events,
            event_type="date_skipped_existing_fixture",
            date_str=date_str,
            details={"local_zip_path": raw_relpath},
        )
        existing_local_sha = sha256_file(final_zip)
        if existing_local_sha != EXISTING_FIXTURE_SHA256:
            result.status = "checksum_mismatch"
            result.failure_reason = (
                f"existing fixture SHA mismatch: recorded "
                f"{EXISTING_FIXTURE_SHA256}, fresh local "
                f"{existing_local_sha}"
            )
            _emit_event(
                events,
                event_type="checksum_mismatch",
                date_str=date_str,
                details={
                    "recorded": EXISTING_FIXTURE_SHA256,
                    "fresh_local": existing_local_sha,
                },
            )
            return result

        # Fetch fresh companion and cross-verify.
        chk_content, chk_retries, chk_err = _try_download_with_retry(
            expected_chk_url, date_str, events, do_network=do_network
        )
        result.retry_count = max(result.retry_count, chk_retries)
        if chk_err == "missing_404":
            result.status = "checksum_companion_unavailable"
            result.failure_reason = (
                "existing fixture companion missing (404); existing file "
                "preserved untouched"
            )
            return result
        if chk_err == "retry_exhausted" or chk_content is None:
            result.status = "retry_exhausted"
            result.failure_reason = (
                f"existing fixture companion download exhausted retries: "
                f"{chk_err}"
            )
            return result
        try:
            expected_companion_sha = parse_sha256_from_checksum(chk_content)
        except AcquisitionFailClosed as exc:
            result.status = "checksum_mismatch"
            result.failure_reason = f"could not parse companion: {exc}"
            return result
        result.sha256_from_companion = expected_companion_sha
        if expected_companion_sha != EXISTING_FIXTURE_SHA256:
            result.status = "checksum_mismatch"
            result.failure_reason = (
                f"existing fixture companion mismatch: recorded "
                f"{EXISTING_FIXTURE_SHA256}, companion "
                f"{expected_companion_sha}; existing file preserved untouched"
            )
            return result

        # Read existing sidecar and verify format / content (Phase 4bl-B §10.6).
        if not final_sha.exists():
            result.status = "finalisation_failure"
            result.failure_reason = (
                f"existing fixture sidecar missing at {sidecar_relpath}"
            )
            return result
        sidecar_text = final_sha.read_text(encoding="utf-8")
        expected_sidecar = make_sidecar_body(
            EXISTING_FIXTURE_SHA256, final_zip.name
        )
        if sidecar_text != expected_sidecar:
            # The existing sidecar may use a different canonical format;
            # we accept it as long as the SHA prefix matches and we do NOT
            # rewrite it.
            try:
                parsed = parse_sha256_from_checksum(sidecar_text)
            except AcquisitionFailClosed:
                result.status = "finalisation_failure"
                result.failure_reason = (
                    "existing fixture sidecar could not be parsed as SHA256"
                )
                return result
            if parsed != EXISTING_FIXTURE_SHA256:
                result.status = "finalisation_failure"
                result.failure_reason = (
                    f"existing fixture sidecar SHA mismatch: parsed "
                    f"{parsed}, expected {EXISTING_FIXTURE_SHA256}"
                )
                return result

        # Inventory + row-sample validation on the existing ZIP.
        inv = inventory_and_validate_zip(final_zip, date_str=date_str)
        if inv.decompression_failure_reason is not None:
            result.status = "decompression_failure"
            result.failure_reason = inv.decompression_failure_reason
            return result

        result.sha256 = EXISTING_FIXTURE_SHA256
        result.size_bytes = final_zip.stat().st_size
        result.row_count = inv.row_count
        result.first_trade_time_ms = inv.first_trade_time_ms
        result.last_trade_time_ms = inv.last_trade_time_ms
        result.min_agg_trade_id = inv.min_agg_trade_id
        result.max_agg_trade_id = inv.max_agg_trade_id
        result.acquired_at_unix_ms = _now_ms()

        if not inv.row_sample_validation_passed:
            result.status = "row_sample_validation_failure"
            result.failure_reason = (
                inv.row_sample_failure_reason
                or "row sample validation failed on existing fixture"
            )
            return result

        result.status = "acquired_verified"
        _emit_event(
            events,
            event_type="existing_fixture_verified",
            date_str=date_str,
            details={
                "local_sha": existing_local_sha,
                "companion_sha": expected_companion_sha,
                "recorded_sha": EXISTING_FIXTURE_SHA256,
            },
        )
        return result

    # ------------------------------------------------------------------ #
    # Normal acquisition path (download companion, then ZIP)
    # ------------------------------------------------------------------ #

    # If a non-fixture final ZIP exists with byte-identical content,
    # treat as already-acquired; if not byte-identical, refuse to
    # overwrite per §10.4 / §11.4.
    if final_zip.exists():
        existing_sha = sha256_file(final_zip)
        _emit_event(
            events,
            event_type="existing_local_file_detected",
            date_str=date_str,
            details={"local_sha": existing_sha},
        )
    else:
        existing_sha = None

    # 1. Download .CHECKSUM companion first.
    chk_content, chk_retries, chk_err = _try_download_with_retry(
        expected_chk_url, date_str, events, do_network=do_network
    )
    result.retry_count = max(result.retry_count, chk_retries)
    if chk_err == "missing_404":
        result.status = "checksum_companion_unavailable"
        result.failure_reason = "checksum companion HTTP 404"
        return result
    if chk_err == "retry_exhausted" or chk_content is None:
        result.status = "retry_exhausted"
        result.failure_reason = (
            f"checksum companion download exhausted retries: {chk_err}"
        )
        return result
    try:
        expected_sha = parse_sha256_from_checksum(chk_content)
    except AcquisitionFailClosed as exc:
        result.status = "checksum_mismatch"
        result.failure_reason = f"could not parse companion: {exc}"
        return result
    result.sha256_from_companion = expected_sha

    # If the existing local file already matches the published SHA, no
    # redownload is needed (re-run discipline per §11.4).
    if existing_sha is not None and existing_sha == expected_sha:
        # Verify sidecar exists and matches.
        if not final_sha.exists():
            result.status = "finalisation_failure"
            result.failure_reason = (
                f"existing local file present but sidecar missing at "
                f"{sidecar_relpath}"
            )
            return result
        inv = inventory_and_validate_zip(final_zip, date_str=date_str)
        if inv.decompression_failure_reason is not None:
            result.status = "decompression_failure"
            result.failure_reason = inv.decompression_failure_reason
            return result
        result.sha256 = existing_sha
        result.size_bytes = final_zip.stat().st_size
        result.row_count = inv.row_count
        result.first_trade_time_ms = inv.first_trade_time_ms
        result.last_trade_time_ms = inv.last_trade_time_ms
        result.min_agg_trade_id = inv.min_agg_trade_id
        result.max_agg_trade_id = inv.max_agg_trade_id
        result.acquired_at_unix_ms = _now_ms()
        if not inv.row_sample_validation_passed:
            result.status = "row_sample_validation_failure"
            result.failure_reason = (
                inv.row_sample_failure_reason
                or "row sample validation failed on existing local file"
            )
            return result
        result.status = "acquired_verified"
        return result

    # Refuse to overwrite an existing local file with a different SHA.
    if existing_sha is not None and existing_sha != expected_sha:
        result.status = "checksum_mismatch"
        result.failure_reason = (
            f"existing local SHA {existing_sha} differs from companion "
            f"SHA {expected_sha}; refusing to overwrite"
        )
        return result

    # 2. Download the ZIP.
    zip_content, zip_retries, zip_err = _try_download_with_retry(
        expected_url, date_str, events, do_network=do_network
    )
    result.retry_count = max(result.retry_count, zip_retries)
    if zip_err == "missing_404":
        result.status = "missing_404"
        result.failure_reason = "archive HTTP 404"
        return result
    if zip_err == "retry_exhausted" or zip_content is None:
        result.status = "retry_exhausted"
        result.failure_reason = f"archive download exhausted retries: {zip_err}"
        return result

    # 3. Verify checksum.
    local_sha = sha256_bytes(zip_content)
    if local_sha != expected_sha:
        _emit_event(
            events,
            event_type="checksum_mismatch",
            date_str=date_str,
            details={"expected": expected_sha, "got": local_sha},
        )
        result.status = "checksum_mismatch"
        result.sha256 = local_sha
        result.failure_reason = (
            f"checksum mismatch: companion {expected_sha}, local {local_sha}"
        )
        return result
    _emit_event(
        events,
        event_type="checksum_match",
        date_str=date_str,
        details={"sha256": local_sha, "size_bytes": len(zip_content)},
    )

    # 4. Stage write + atomic move to final raw path.
    staging_dir.mkdir(parents=True, exist_ok=True)
    try:
        with staging_zip.open("wb") as fh:
            fh.write(zip_content)
            try:
                fh.flush()
                os.fsync(fh.fileno())
            except (OSError, AttributeError):
                pass
        atomic_move_file(staging_zip, final_zip)
    except (AcquisitionFailClosed, OSError) as exc:
        result.status = "finalisation_failure"
        result.failure_reason = (
            f"finalisation failed: {type(exc).__name__}: {exc}"
        )
        return result

    # 5. Write paired SHA256 sidecar.
    try:
        atomic_write_text(final_sha, make_sidecar_body(local_sha, final_zip.name))
    except (AcquisitionFailClosed, OSError) as exc:
        result.status = "finalisation_failure"
        result.failure_reason = (
            f"sidecar write failed: {type(exc).__name__}: {exc}"
        )
        return result
    _emit_event(
        events,
        event_type="sidecar_write",
        date_str=date_str,
        details={"path": sidecar_relpath},
    )

    # 6. Decompression test + inventory + row-sample validation.
    inv = inventory_and_validate_zip(final_zip, date_str=date_str)
    if inv.decompression_failure_reason is not None:
        result.status = "decompression_failure"
        result.failure_reason = inv.decompression_failure_reason
        result.sha256 = local_sha
        result.size_bytes = final_zip.stat().st_size
        return result
    result.sha256 = local_sha
    result.size_bytes = final_zip.stat().st_size
    result.row_count = inv.row_count
    result.first_trade_time_ms = inv.first_trade_time_ms
    result.last_trade_time_ms = inv.last_trade_time_ms
    result.min_agg_trade_id = inv.min_agg_trade_id
    result.max_agg_trade_id = inv.max_agg_trade_id
    result.acquired_at_unix_ms = _now_ms()
    if not inv.row_sample_validation_passed:
        result.status = "row_sample_validation_failure"
        result.failure_reason = (
            inv.row_sample_failure_reason
            or "row sample validation failed on newly acquired ZIP"
        )
        return result

    result.status = "acquired_verified"
    _emit_event(
        events,
        event_type="finalisation_success",
        date_str=date_str,
        details={
            "sha256": local_sha,
            "size_bytes": result.size_bytes,
            "row_count": result.row_count,
        },
    )

    # 7. Best-effort staging cleanup on success.
    with contextlib.suppress(OSError):
        if staging_chk.exists():
            staging_chk.unlink()
        if staging_zip.exists():
            staging_zip.unlink()
        with contextlib.suppress(OSError):
            staging_dir.rmdir()

    return result


# ---------------------------------------------------------------------------- #
# Manifest and acquisition log writers
# ---------------------------------------------------------------------------- #


def _entry_to_inventory_dict(entry: DateResult) -> dict[str, object]:
    if entry.status not in _VALID_STATUSES:
        raise AcquisitionFailClosed(
            f"invalid status {entry.status!r} for date {entry.date}"
        )
    return {
        "acquired_at_unix_ms": entry.acquired_at_unix_ms,
        "date": entry.date,
        "expected_checksum_url": entry.expected_checksum_url,
        "expected_url": entry.expected_url,
        "failure_reason": entry.failure_reason,
        "first_trade_time_ms": entry.first_trade_time_ms,
        "last_trade_time_ms": entry.last_trade_time_ms,
        "local_sidecar_path": entry.local_sidecar_path,
        "local_zip_path": entry.local_zip_path,
        "max_agg_trade_id": entry.max_agg_trade_id,
        "min_agg_trade_id": entry.min_agg_trade_id,
        "retry_count": entry.retry_count,
        "row_count": entry.row_count,
        "sha256": entry.sha256,
        "sha256_from_companion": entry.sha256_from_companion,
        "size_bytes": entry.size_bytes,
        "status": entry.status,
    }


def write_acquisition_log(
    log_path: Path,
    *,
    acquisition_run_id: str,
    code_commit_sha: str,
    started_at_unix_ms: int,
    finished_at_unix_ms: int,
    date_list: list[str],
    events: list[dict[str, object]],
    entries: list[DateResult],
    overall_status: str,
    strict_fail_closed: bool,
) -> None:
    summary = {
        "acquired_file_count": sum(1 for e in entries if e.status == "acquired_verified"),
        "checksum_companion_unavailable_count": sum(
            1 for e in entries if e.status == "checksum_companion_unavailable"
        ),
        "checksum_mismatch_count": sum(
            1 for e in entries if e.status == "checksum_mismatch"
        ),
        "decompression_failure_count": sum(
            1 for e in entries if e.status == "decompression_failure"
        ),
        "eligibility_gate_status_after_acquisition": "pending",
        "existing_fixture_reused": any(
            e.date == EXISTING_FIXTURE_DATE and e.status == "acquired_verified"
            for e in entries
        ),
        "existing_fixture_sha_match": any(
            e.date == EXISTING_FIXTURE_DATE
            and e.sha256 == EXISTING_FIXTURE_SHA256
            for e in entries
        ),
        "expected_file_count": EXPECTED_DATE_COUNT,
        "missing_file_count": sum(1 for e in entries if e.status == "missing_404"),
        "non_authorizations_preserved": True,
        "research_eligible_after_acquisition": False,
        "row_sample_validation_failure_count": sum(
            1 for e in entries if e.status == "row_sample_validation_failure"
        ),
        "total_row_count": sum((e.row_count or 0) for e in entries),
        "total_size_bytes": sum((e.size_bytes or 0) for e in entries),
    }
    log = {
        "acquisition_run_id": acquisition_run_id,
        "base_commit_sha": BASE_COMMIT_SHA,
        "code_commit_sha": code_commit_sha,
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "date_count": EXPECTED_DATE_COUNT,
        "date_end": DATE_END.isoformat(),
        "date_list": date_list,
        "date_start": DATE_START.isoformat(),
        "errors": [
            e.failure_reason for e in entries if e.failure_reason is not None
        ],
        "events": events,
        "finished_at_unix_ms": finished_at_unix_ms,
        "finished_at_utc": datetime.fromtimestamp(
            finished_at_unix_ms / 1000.0, tz=UTC
        ).isoformat(),
        "non_authorizations": _non_authorizations(),
        "overall_status": overall_status,
        "per_file_results": [_entry_to_inventory_dict(e) for e in entries],
        "phase": "Phase 4bl-C",
        "phase_id": PHASE_ID,
        "platform_summary": _platform_summary(),
        "python_version": sys.version,
        "retries_attempted": sum(e.retry_count for e in entries),
        "schema_version": SCHEMA_VERSION,
        "source_url_pattern": ARCHIVE_URL_TEMPLATE,
        "checksum_url_pattern": CHECKSUM_URL_TEMPLATE,
        "started_at_unix_ms": started_at_unix_ms,
        "started_at_utc": datetime.fromtimestamp(
            started_at_unix_ms / 1000.0, tz=UTC
        ).isoformat(),
        "strict_fail_closed": strict_fail_closed,
        "summary": summary,
        "symbol_list": list(SYMBOL_LIST),
        "wall_clock_seconds": (finished_at_unix_ms - started_at_unix_ms) // 1000,
        "warnings": [],
    }
    atomic_write_text(log_path, json.dumps(log, indent=2, sort_keys=True) + "\n")


def write_multiday_manifest(
    manifest_path: Path,
    *,
    code_commit_sha: str,
    date_list: list[str],
    entries: list[DateResult],
    acquisition_log_path: Path,
    acquisition_log_sha256: str,
    output_root: Path,
) -> None:
    capture_config_hash = compute_capture_config_hash(date_list, code_commit_sha)
    manifest: dict[str, object] = {
        "acquired_file_count": sum(
            1 for e in entries if e.status == "acquired_verified"
        ),
        "acquisition_log_path": acquisition_log_path.relative_to(
            output_root.parent
        ).as_posix(),
        "acquisition_log_sha256": acquisition_log_sha256,
        "base_commit_sha": BASE_COMMIT_SHA,
        "capture_config_hash": capture_config_hash,
        "capture_mode": CAPTURE_MODE,
        "checksum_mismatch_count": sum(
            1 for e in entries if e.status == "checksum_mismatch"
        ),
        "code_commit_sha": code_commit_sha,
        "created_at_unix_ms": _now_ms(),
        "created_at_utc": datetime.now(tz=UTC).isoformat(),
        "dataset_family": DATASET_FAMILY,
        "dataset_version": DATASET_VERSION,
        "date_count": EXPECTED_DATE_COUNT,
        "date_end": DATE_END.isoformat(),
        "date_list": date_list,
        "date_start": DATE_START.isoformat(),
        "decompression_failure_count": sum(
            1 for e in entries if e.status == "decompression_failure"
        ),
        "eligibility_gate_status": "pending",
        "endpoint": ENDPOINT_LABEL,
        "endpoint_docs_reference": ENDPOINT_DOCS_REFERENCE,
        "expected_file_count": EXPECTED_DATE_COUNT,
        "governance_labels": {
            "feature_computation": "forbidden",
            "labels": "forbidden",
            "ml": "forbidden",
            "phase": PHASE_ID,
            "source_phase_boundary": SOURCE_PHASE_BOUNDARY,
            "stop_trigger_domain": "trade_price_backtest_candidate",
            "strategy": "forbidden",
            "strategy_use": "forbidden",
            "symbol_scope_source": "archive_path",
            "validator": "phase_4ax_aggtrades_v001",
        },
        "invalid_windows": [],
        "missing_file_count": sum(1 for e in entries if e.status == "missing_404"),
        "non_authorizations": _non_authorizations(),
        "per_file_inventory": [_entry_to_inventory_dict(e) for e in entries],
        "proxy_warning": None,
        "research_eligible": False,
        "retention_warning": None,
        "schema_version": SCHEMA_VERSION,
        "source": SOURCE_LABEL,
        "source_class": SOURCE_CLASS,
        "symbol_list": list(SYMBOL_LIST),
        "total_row_count": sum((e.row_count or 0) for e in entries),
        "total_size_bytes": sum((e.size_bytes or 0) for e in entries),
        "version": DATASET_VERSION,
    }
    atomic_write_text(manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def _non_authorizations() -> dict[str, str]:
    """Explicit non-authorizations recorded inside the manifest and log."""
    return {
        "acquisition_of_additional_data": "unauthorized",
        "authenticated_apis": "forbidden",
        "backtest": "forbidden",
        "credentials": "forbidden",
        "decompression_beyond_inventory_and_row_sample": "forbidden",
        "deployment": "forbidden",
        "diagnostics": "forbidden",
        "eligibility_gate_execution": "forbidden",
        "exchange_write": "forbidden",
        "feature_computation": "forbidden",
        "graphify": "forbidden",
        "label_computation": "forbidden",
        "live_readiness": "forbidden",
        "mcp": "forbidden",
        "ml_training": "forbidden",
        "normalization": "forbidden",
        "paper_shadow": "forbidden",
        "private_endpoints": "forbidden",
        "production_keys": "forbidden",
        "research_eligible_flip": "forbidden",
        "strategy_creation": "forbidden",
        "successor_state_creation": "forbidden",
        "user_stream": "forbidden",
        "websockets": "forbidden",
    }


def _platform_summary() -> dict[str, str]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_implementation": platform.python_implementation(),
    }


# ---------------------------------------------------------------------------- #
# Top-level orchestrator
# ---------------------------------------------------------------------------- #


@dataclass(frozen=True)
class AcquisitionRunResult:
    overall_status: str
    acquisition_log_path: Path
    acquisition_log_sha256: str
    manifest_path: Path
    manifest_sha256: str
    entries: list[DateResult]
    started_at_unix_ms: int
    finished_at_unix_ms: int


def run_acquisition(
    output_root: Path,
    *,
    do_network: bool = True,
    progress_stream: object | None = None,
) -> AcquisitionRunResult:
    """Run the full Phase 4bl-C acquisition.

    The orchestrator never raises for per-date failures (each date's
    failure is recorded in the manifest and log). It DOES raise
    :class:`AcquisitionFailClosed` for run-level fail-closed conditions
    (path discipline, gitignore guard, etc).
    """
    output_root = output_root.resolve()
    if "data/microstructure" not in str(output_root).replace("\\", "/").lower():
        raise AcquisitionFailClosed(
            f"output_root {output_root!r} is not under data/microstructure/"
        )

    date_list = generate_locked_date_list()
    code_commit_sha = _commit_sha_or_pending()

    manifests_dir = output_root / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = manifests_dir / f"{DATASET_FAMILY}__{DATASET_VERSION}.json"
    log_path = manifests_dir / f"{DATASET_FAMILY}__{DATASET_VERSION}_acquisition_log.json"
    manifest_sha_path = manifest_path.with_suffix(manifest_path.suffix + ".sha256")
    log_sha_path = log_path.with_suffix(log_path.suffix + ".sha256")

    for p in (manifest_path, log_path, manifest_sha_path, log_sha_path):
        assert_path_under_microstructure(p, output_root)

    # Verify gitignore coverage. We accept either an explicit
    # data/microstructure/ rule (current state) or an exact-path rule.
    repo_root = _REPO_ROOT
    for sample in (
        manifest_path,
        log_path,
        manifest_sha_path,
        log_sha_path,
        output_root / "raw" / DATASET_FAMILY / SYMBOL / "2024" / "12"
            / f"{SYMBOL}-aggTrades-2024-12-01.zip",
        output_root / "staging" / DATASET_FAMILY,
    ):
        if not verify_gitignored(sample, repo_root=repo_root):
            raise AcquisitionFailClosed(
                f"intended output path is not gitignored: {sample}"
            )

    acquisition_run_id = (
        f"phase-{PHASE_ID}-{_now_ms()}-{uuid.uuid4().hex[:8]}"
    )
    events: list[dict[str, object]] = []
    entries: list[DateResult] = []
    started_at_unix_ms = _now_ms()
    _emit_event(
        events,
        event_type="run_started",
        date_str="all",
        details={
            "acquisition_run_id": acquisition_run_id,
            "date_count": EXPECTED_DATE_COUNT,
            "code_commit_sha": code_commit_sha,
        },
    )

    for i, date_str in enumerate(date_list):
        if progress_stream is not None:
            try:
                progress_stream.write(
                    f"[{i+1}/{EXPECTED_DATE_COUNT}] {date_str} ..."
                )
                progress_stream.flush()
            except (AttributeError, OSError):
                pass
        entry = acquire_one_date(
            date_str,
            output_root=output_root,
            events=events,
            do_network=do_network,
        )
        entries.append(entry)
        if progress_stream is not None:
            try:
                progress_stream.write(
                    f" {entry.status}"
                    + (f" ({entry.failure_reason})" if entry.failure_reason else "")
                    + "\n"
                )
                progress_stream.flush()
            except (AttributeError, OSError):
                pass

    finished_at_unix_ms = _now_ms()
    _emit_event(
        events,
        event_type="run_finished",
        date_str="all",
        details={
            "acquired_file_count": sum(
                1 for e in entries if e.status == "acquired_verified"
            ),
            "wall_clock_seconds": (finished_at_unix_ms - started_at_unix_ms) // 1000,
        },
    )

    acquired = sum(1 for e in entries if e.status == "acquired_verified")
    if acquired == 0:
        overall_status = "FAIL_CLOSED_NO_ACQUISITION"
        strict_fail_closed = True
    elif acquired == EXPECTED_DATE_COUNT:
        overall_status = "SUCCESSFUL_ACQUISITION"
        strict_fail_closed = False
    else:
        overall_status = "PARTIAL_ACQUISITION"
        strict_fail_closed = False

    # Write acquisition log first; its SHA goes into the manifest.
    write_acquisition_log(
        log_path,
        acquisition_run_id=acquisition_run_id,
        code_commit_sha=code_commit_sha,
        started_at_unix_ms=started_at_unix_ms,
        finished_at_unix_ms=finished_at_unix_ms,
        date_list=date_list,
        events=events,
        entries=entries,
        overall_status=overall_status,
        strict_fail_closed=strict_fail_closed,
    )
    log_sha = sha256_file(log_path)
    atomic_write_text(log_sha_path, make_sidecar_body(log_sha, log_path.name))

    # Write manifest.
    write_multiday_manifest(
        manifest_path,
        code_commit_sha=code_commit_sha,
        date_list=date_list,
        entries=entries,
        acquisition_log_path=log_path,
        acquisition_log_sha256=log_sha,
        output_root=output_root,
    )
    manifest_sha = sha256_file(manifest_path)
    atomic_write_text(
        manifest_sha_path, make_sidecar_body(manifest_sha, manifest_path.name)
    )

    return AcquisitionRunResult(
        overall_status=overall_status,
        acquisition_log_path=log_path,
        acquisition_log_sha256=log_sha,
        manifest_path=manifest_path,
        manifest_sha256=manifest_sha,
        entries=entries,
        started_at_unix_ms=started_at_unix_ms,
        finished_at_unix_ms=finished_at_unix_ms,
    )


# ---------------------------------------------------------------------------- #
# CLI
# ---------------------------------------------------------------------------- #


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Phase 4bl-C: acquire 90 BTCUSDT public aggTrades daily archives "
            "from data.binance.vision under the Phase 4bl-B locked design."
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
        help="Print the locked plan without downloading anything.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)
    output_root: Path = args.output_root.resolve()

    if "data/microstructure" not in str(output_root).replace("\\", "/").lower():
        print(
            f"refusing to use --output-root outside data/microstructure/: "
            f"{output_root}",
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        date_list = generate_locked_date_list()
        print("Phase 4bl-C dry-run plan:")
        print(f"  symbols        : {SYMBOL_LIST}")
        print(f"  date_start     : {DATE_START.isoformat()}")
        print(f"  date_end       : {DATE_END.isoformat()}")
        print(f"  date_count     : {len(date_list)}")
        print(f"  url_template   : {ARCHIVE_URL_TEMPLATE}")
        print(f"  output_root    : {output_root}")
        print(f"  manifest_path  : "
              f"{output_root}/manifests/{DATASET_FAMILY}__{DATASET_VERSION}.json")
        print(f"  log_path       : "
              f"{output_root}/manifests/"
              f"{DATASET_FAMILY}__{DATASET_VERSION}_acquisition_log.json")
        print(f"  first_3_dates  : {date_list[:3]}")
        print(f"  last_3_dates   : {date_list[-3:]}")
        print("No download will be performed.")
        return 0

    try:
        result = run_acquisition(
            output_root=output_root,
            do_network=True,
            progress_stream=sys.stdout,
        )
    except AcquisitionFailClosed as exc:
        print(f"Phase 4bl-C: FAIL_CLOSED_NO_ACQUISITION ({exc})", file=sys.stderr)
        return 1

    print("Phase 4bl-C: " + result.overall_status)
    summary = {
        "acquired": sum(1 for e in result.entries if e.status == "acquired_verified"),
        "missing_404": sum(1 for e in result.entries if e.status == "missing_404"),
        "checksum_mismatch": sum(
            1 for e in result.entries if e.status == "checksum_mismatch"
        ),
        "checksum_companion_unavailable": sum(
            1 for e in result.entries
            if e.status == "checksum_companion_unavailable"
        ),
        "decompression_failure": sum(
            1 for e in result.entries if e.status == "decompression_failure"
        ),
        "row_sample_validation_failure": sum(
            1 for e in result.entries
            if e.status == "row_sample_validation_failure"
        ),
        "finalisation_failure": sum(
            1 for e in result.entries if e.status == "finalisation_failure"
        ),
        "retry_exhausted": sum(
            1 for e in result.entries if e.status == "retry_exhausted"
        ),
    }
    for k, v in summary.items():
        print(f"  {k:32s}: {v}")
    print(f"  manifest_path                   : {result.manifest_path}")
    print(f"  manifest_sha256                 : {result.manifest_sha256}")
    print(f"  acquisition_log_path            : {result.acquisition_log_path}")
    print(f"  acquisition_log_sha256          : {result.acquisition_log_sha256}")
    print(f"  total_size_bytes                : {sum((e.size_bytes or 0) for e in result.entries)}")
    print(f"  total_row_count                 : {sum((e.row_count or 0) for e in result.entries)}")
    print(f"  wall_clock_seconds              : "
          f"{(result.finished_at_unix_ms - result.started_at_unix_ms) // 1000}")

    if result.overall_status == "FAIL_CLOSED_NO_ACQUISITION":
        return 1
    if result.overall_status == "PARTIAL_ACQUISITION":
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
