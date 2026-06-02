"""Phase 4bn-J-R2 — Revised Acquisition-Only BTCUSDT aggTrades Raw Retry.

Standalone, bounded, raw-only acquisition script authorised by the
Phase 4bn-J-R1 *Workspace Relocation + Raw-Only Acquisition Cap
Amendment*. It acquires exactly the **275 new pre-v002** Binance
USDⓈ-M Futures aggTrades daily archives for BTCUSDT covering UTC dates
``2024-03-01`` through ``2024-11-30`` inclusive from the public
``data.binance.vision`` archive, validates a bounded row sample per ZIP
against the Phase 4ax validator, and writes raw archives plus a sibling
**segment** manifest + acquisition log under the gitignored
``data/microstructure/`` tree.

This script is a deliberate sibling of
``scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`` (which is
locked to the 90-day v002 terminal window 2024-12-01 .. 2025-02-28 and
must NOT be repointed). It reuses the proven Phase 4bl-C patterns —
host allowlist, URL/path pattern, CHECKSUM-first ordering, SHA256
verification, ``zipfile.testzip()``, bounded row-sample validation via
the Phase 4ax validator, Phase 4bb-F canonical sidecars, refuse-
overwrite, and a non-eligible raw manifest seed — and adds the
amended raw-only disk cap (10 GiB warning / 25 GiB hard) and runtime
cap (2 h warning / 4 h hard) enforced at per-day boundaries.

Hard boundaries (any violation fails closed):

- Symbol: BTCUSDT only. aggTrades only.
- Exact new acquisition segment: 2024-03-01 .. 2024-11-30 inclusive UTC.
- Any date ``>= 2024-12-01`` is rejected (the existing v002 terminal
  window 2024-12-01 .. 2025-02-28 is NOT re-downloaded, NOT
  overwritten, NOT read).
- Any date ``< 2024-03-01`` or ``> 2024-11-30`` is rejected.
- The existing v002 sealed test split 2025-02-14 .. 2025-02-28 is
  never read, counted, sampled, hashed, summarised, or inspected.
- No ETHUSDT, mark-price, spot, cross-venue, order-book, tick, extra
  horizon, or v003.

Network access only to ``https://data.binance.vision`` URLs matching
the locked daily futures aggTrades path pattern. No ``fapi.binance.com``,
no ``api.binance.com``, no ``stream.binance.com``, no authenticated
APIs, no private endpoints, no user streams, no WebSockets, no
listenKey lifecycle, no credentials, no ``.env``, no MCP / Graphify /
``.mcp.json``.

This script is acquisition-only / raw-only. It MUST NOT normalize,
derive features, derive labels, run gates, create gate reports, create
successor-state artefacts, run diagnostics, compute returns / PnL /
strategy metrics, train ML, create signals, create strategy logic, run
backtests, create databases, compact Parquet, or create v003. It MUST
NOT flip ``research_eligible`` or transition ``eligibility_gate_status``
on any manifest. The segment manifest is written with
``research_eligible=false`` and ``eligibility_gate_status="pending"``.
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
# script is invoked directly (``python scripts/phase4bn_j_r2_*.py``).
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
# Phase constants (predeclared by the Phase 4bn-J-R2 operator brief and the
# Phase 4bn-J-R1 amendment)
# ---------------------------------------------------------------------------- #

PHASE_ID = "4bn-J-R2"
SOURCE_PHASE_BOUNDARY = "4bn-J-R1"
# Phase 4bn-J-R1 SHA-finalised main (base for this retry branch).
BASE_COMMIT_SHA = "03dc876cab9ecd3db982beb0ba51712858cbdf9c"

DATASET_FAMILY = "microstructure_raw_aggtrades_v001"
# This retry is a *backward extension segment* of the existing v002
# dataset envelope; it is NOT a new dataset version. It writes a
# distinct, phase-scoped segment manifest and never mutates the
# published ``microstructure_raw_aggtrades_v001__v002.json`` manifest.
DATASET_VERSION = "v002"
SEGMENT_LABEL = "pre_v002_segment"
MANIFEST_STEM = f"{DATASET_FAMILY}__{DATASET_VERSION}_{SEGMENT_LABEL}_4bn_j_r2"
SCHEMA_VERSION = "v001"
SYMBOL = "BTCUSDT"
SYMBOL_LIST: tuple[str, ...] = (SYMBOL,)
DATA_FAMILY = "aggTrades"
MARKET = "binance_usdm_futures"

# New acquisition segment (inclusive UTC).
DATE_START = date(2024, 3, 1)
DATE_END = date(2024, 11, 30)
EXPECTED_DATE_COUNT = 275

# Existing v002 terminal window — never re-downloaded / overwritten / read.
V002_TERMINAL_START = date(2024, 12, 1)
V002_TERMINAL_END = date(2025, 2, 28)
# Existing v002 sealed test split — never read / counted / sampled / hashed.
V002_TEST_SPLIT_START = date(2025, 2, 14)
V002_TEST_SPLIT_END = date(2025, 2, 28)
# Full intended 12-month envelope (only the pre-v002 segment is fetched here).
FULL_ENVELOPE_START = date(2024, 3, 1)
FULL_ENVELOPE_END = date(2025, 2, 28)

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

# Maximum allowed single-archive download size (5 GiB; Phase 4ay precedent).
MAX_DOWNLOAD_BYTES = 5 * 1024 * 1024 * 1024

# Amended raw-only disk-footprint caps (Phase 4bn-J-R1 amendment).
RAW_WARN_BYTES = 10 * 1024 * 1024 * 1024  # 10 GiB additional raw footprint
RAW_HARD_BYTES = 25 * 1024 * 1024 * 1024  # 25 GiB additional raw footprint

# Runtime caps (Phase 4bn-I, unchanged).
RUNTIME_WARN_SECONDS = 2 * 60 * 60  # 2 hours wall-clock
RUNTIME_HARD_SECONDS = 4 * 60 * 60  # 4 hours wall-clock

# Retry policy (mirrors Phase 4bl-B §12).
MAX_RETRIES = 3
RETRY_BACKOFFS_SECONDS: tuple[int, ...] = (2, 4, 8)
PER_ATTEMPT_TIMEOUT_SECONDS = 60
PER_DATE_BUDGET_SECONDS = 5 * 60  # 5 minutes

# Row-sample validation policy (mirrors Phase 4bl-B §11.5).
ROW_SAMPLE_HEAD = 100
ROW_SAMPLE_TAIL = 100
ROW_SAMPLE_MIDDLE = 100


# ---------------------------------------------------------------------------- #
# Errors
# ---------------------------------------------------------------------------- #


class AcquisitionFailClosed(RuntimeError):
    """Raised when the acquisition orchestrator must halt the entire run."""


# ---------------------------------------------------------------------------- #
# Symbol / family / date guards (segment-specific, fail-closed)
# ---------------------------------------------------------------------------- #


# Forbidden symbol / family / scope tokens. Any of these in an input
# value fails closed, before any URL is built or any network call made.
_FORBIDDEN_SCOPE_TOKENS: tuple[str, ...] = (
    "ETHUSDT",
    "ETH",
    "markprice",
    "markPrice",
    "mark_price",
    "indexprice",
    "premiumindex",
    "spot",
    "coin-m",
    "coinm",
    "/cm/",
    "orderbook",
    "order_book",
    "bookdepth",
    "bookTicker",
    "depth",
    "tick",
    "trades",  # plain (non-agg) trades family is out of scope
    "klines",
    "metrics",
    "fundingRate",
    "openInterest",
    "cross",
    "v003",
)


def assert_symbol_btcusdt(symbol: str) -> None:
    """Reject any symbol other than the locked BTCUSDT."""
    if not isinstance(symbol, str) or symbol != SYMBOL:
        raise AcquisitionFailClosed(
            f"symbol must be exactly {SYMBOL!r}; got {symbol!r}"
        )


def assert_family_aggtrades(family: str) -> None:
    """Reject any data family other than the locked aggTrades."""
    if not isinstance(family, str) or family != DATA_FAMILY:
        raise AcquisitionFailClosed(
            f"data family must be exactly {DATA_FAMILY!r}; got {family!r}"
        )


def assert_scope_token_allowed(value: str) -> None:
    """Reject any value containing a forbidden out-of-scope token."""
    if not isinstance(value, str):
        raise AcquisitionFailClosed(f"scope value must be a str; got {value!r}")
    lowered = value.lower()
    for token in _FORBIDDEN_SCOPE_TOKENS:
        # ``trades`` is a substring of ``aggTrades``; only reject a bare
        # ``trades`` token that is NOT part of ``aggtrades``.
        if token == "trades":
            stripped = lowered.replace("aggtrades", "")
            if "trades" in stripped:
                raise AcquisitionFailClosed(
                    f"value {value!r} contains forbidden token {token!r}"
                )
            continue
        if token.lower() in lowered:
            raise AcquisitionFailClosed(
                f"value {value!r} contains forbidden token {token!r}"
            )


def assert_date_in_segment(date_str: str) -> date:
    """Parse ``date_str`` and reject any date outside the locked segment.

    The locked segment is 2024-03-01 .. 2024-11-30 inclusive UTC. Any
    date ``>= 2024-12-01`` (the existing v002 terminal window) is
    rejected, as is any date before 2024-03-01 or after 2024-11-30.
    """
    if not isinstance(date_str, str):
        raise AcquisitionFailClosed(f"date must be a str; got {date_str!r}")
    try:
        parsed = date.fromisoformat(date_str)
    except ValueError as exc:
        raise AcquisitionFailClosed(
            f"date {date_str!r} is not an ISO-8601 date: {exc}"
        ) from exc
    if parsed >= V002_TERMINAL_START:
        raise AcquisitionFailClosed(
            f"date {date_str} is in or after the existing v002 terminal "
            f"window (>= {V002_TERMINAL_START.isoformat()}); refusing to "
            f"touch v002 / sealed test data"
        )
    if parsed < DATE_START:
        raise AcquisitionFailClosed(
            f"date {date_str} is before the segment start "
            f"{DATE_START.isoformat()}"
        )
    if parsed > DATE_END:
        raise AcquisitionFailClosed(
            f"date {date_str} is after the segment end {DATE_END.isoformat()}"
        )
    return parsed


# ---------------------------------------------------------------------------- #
# Date list generation
# ---------------------------------------------------------------------------- #


def generate_segment_date_list() -> list[str]:
    """Return the locked 275-date ISO-8601 list (chronologically sorted)."""
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
    # Every generated date must pass the segment guard.
    for d in out:
        assert_date_in_segment(d)
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


def build_archive_url(date_str: str) -> str:
    """Build and validate the archive URL for an in-segment date."""
    assert_date_in_segment(date_str)
    url = ARCHIVE_URL_TEMPLATE.format(date=date_str)
    assert_archive_url_allowed(url)
    return url


def build_checksum_url(date_str: str) -> str:
    """Build and validate the checksum companion URL for an in-segment date."""
    assert_date_in_segment(date_str)
    url = CHECKSUM_URL_TEMPLATE.format(date=date_str)
    assert_archive_url_allowed(url)
    return url


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
    norm = str(output_root_resolved).replace("\\", "/").lower()
    if _MICROSTRUCTURE_ROOT not in norm:
        raise AcquisitionFailClosed(
            f"output_root {output_root!r} is not under {_MICROSTRUCTURE_ROOT}"
        )


# ---------------------------------------------------------------------------- #
# Gitignore verification
# ---------------------------------------------------------------------------- #


def verify_gitignored(path: Path, *, repo_root: Path) -> bool:
    """Return True if ``git check-ignore --verbose`` reports the path ignored."""
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


def _http_head_content_length(url: str) -> int | None:
    """Issue an allow-listed HTTP HEAD and return Content-Length, or None.

    Used only by the disk-footprint preflight estimate. It downloads no
    body bytes.
    """
    assert_archive_url_allowed(url)
    request = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(  # noqa: S310 (allow-listed)
        request, timeout=PER_ATTEMPT_TIMEOUT_SECONDS
    ) as response:
        final_url = response.geturl()
        if final_url != url:
            assert_archive_url_allowed(final_url)
        length = response.headers.get("Content-Length")
    if length is None:
        return None
    try:
        return int(length)
    except (TypeError, ValueError):
        return None


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
            with contextlib.suppress(OSError):
                src.unlink()
            return
        raise AcquisitionFailClosed(
            f"refusing to overwrite non-identical existing file at "
            f"{dst}: src_sha={src_sha}, dst_sha={dst_sha}"
        )
    os.replace(src, dst)


# ---------------------------------------------------------------------------- #
# CSV row decoding (mirrors Phase 4az/4bl-C _row_to_payload)
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
        getters = {
            field_name: row[idx]
            for idx, field_name in enumerate(_HEADERLESS_ORDER)
        }
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
# ZIP inventory + bounded row-sample validation
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


def inventory_and_validate_zip(zip_path: Path, *, date_str: str) -> ZipInventory:
    """Decompress the ZIP once and compute inventory + bounded row-sample check.

    Failures in decompression or row-sample validation are returned as
    fields on the ZipInventory rather than raised, so the orchestrator
    can record per-date status and continue.
    """
    try:
        with zipfile.ZipFile(zip_path) as zf:
            bad = zf.testzip()
            if bad is not None:
                return ZipInventory(
                    0, 0, 0, 0, 0, False, None,
                    f"testzip() reported corrupt member: {bad!r}",
                )
            names = [n for n in zf.namelist() if not n.endswith("/")]
            if not names:
                return ZipInventory(
                    0, 0, 0, 0, 0, False, None,
                    "ZIP contains no non-directory members",
                )
            csv_members = [n for n in names if n.lower().endswith(".csv")]
            if not csv_members and len(names) == 1:
                csv_members = names
            if len(csv_members) != 1:
                return ZipInventory(
                    0, 0, 0, 0, 0, False, None,
                    f"ZIP must contain exactly one CSV member; "
                    f"got {csv_members!r} of {names!r}",
                )
            member = csv_members[0]

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
                                0, 0, 0, 0, 0, False, None,
                                f"row {row_count} could not be parsed: "
                                f"{type(exc).__name__}: {exc}",
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
                    0, 0, 0, 0, 0, False, None,
                    f"decompression failed: {type(exc).__name__}: {exc}",
                )

            if row_count == 0:
                return ZipInventory(
                    0, 0, 0, 0, 0, False, None,
                    "ZIP contained zero data rows",
                )

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

            failure_reason: str | None = None
            for mapping_used, row_payload in head_rows + tail_rows + middle_rows:
                try:
                    payload = _row_to_payload(row_payload, mapping_used)
                except AcquisitionFailClosed as exc:
                    failure_reason = f"row decoding failed: {exc}"
                    break
                try:
                    validated = validate_aggtrade_payload(payload)
                except AggTradeValidationError as exc:
                    failure_reason = f"row validation failed: {exc}"
                    break
                else:
                    _ = validated.taker_side  # noqa: F841

            row_sample_passed = failure_reason is None
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
            0, 0, 0, 0, 0, False, None,
            f"ZIP open failed: {type(exc).__name__}: {exc}",
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
    "skipped_cap_breach",
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
    """Download ``url`` with retry policy. Returns (content, retries, error)."""
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
        _emit_event(
            events,
            event_type="download_attempt",
            date_str=date_str,
            details=attempt_event,
        )
        try:
            content = _http_get_bytes(url)
            _emit_event(
                events,
                event_type="download_success",
                date_str=date_str,
                details={
                    "url": url,
                    "retry_count": retries,
                    "size_bytes": len(content),
                },
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
        except (
            urllib.error.URLError,
            AcquisitionFailClosed,
            OSError,
            TimeoutError,
        ) as exc:
            last_error = f"{type(exc).__name__}: {exc}"

        _emit_event(
            events,
            event_type="download_failure",
            date_str=date_str,
            details={"url": url, "retry_count": retries, "error": last_error},
        )

        if retries >= MAX_RETRIES:
            return None, retries, "retry_exhausted"
        elapsed = (_now_ms() - start_unix_ms) / 1000.0
        if elapsed >= PER_DATE_BUDGET_SECONDS:
            return None, retries, "retry_exhausted"
        backoff = RETRY_BACKOFFS_SECONDS[
            min(retries, len(RETRY_BACKOFFS_SECONDS) - 1)
        ]
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
            cwd=str(_REPO_ROOT),
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
        "segment_label": SEGMENT_LABEL,
        "schema_version": SCHEMA_VERSION,
        "symbol_list": list(SYMBOL_LIST),
        "data_family": DATA_FAMILY,
        "market": MARKET,
        "date_start": DATE_START.isoformat(),
        "date_end": DATE_END.isoformat(),
        "date_count": EXPECTED_DATE_COUNT,
        "date_list": date_list,
        "archive_url_template": ARCHIVE_URL_TEMPLATE,
        "checksum_url_template": CHECKSUM_URL_TEMPLATE,
        "endpoint_label": ENDPOINT_LABEL,
        "capture_mode": CAPTURE_MODE,
        "max_download_bytes": MAX_DOWNLOAD_BYTES,
        "raw_warn_bytes": RAW_WARN_BYTES,
        "raw_hard_bytes": RAW_HARD_BYTES,
        "runtime_warn_seconds": RUNTIME_WARN_SECONDS,
        "runtime_hard_seconds": RUNTIME_HARD_SECONDS,
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
    """Acquire one in-segment date and return its result.

    Never raises; all failures are recorded on the returned
    :class:`DateResult` so the orchestrator can continue.
    """
    # Hard guard: this script only ever touches in-segment dates.
    assert_date_in_segment(date_str)

    final_zip, final_sha = _expected_local_paths(date_str, output_root)
    staging_dir, staging_zip, staging_chk = _staging_paths(date_str, output_root)
    expected_url = build_archive_url(date_str)
    expected_chk_url = build_checksum_url(date_str)
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
        status="retry_exhausted",
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

    # If a final ZIP already exists with byte-identical content, treat as
    # already-acquired; if not byte-identical, refuse to overwrite.
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

    # If existing local file already matches the published SHA, no
    # redownload is needed.
    if existing_sha is not None and existing_sha == expected_sha:
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
        result.failure_reason = f"sidecar write failed: {type(exc).__name__}: {exc}"
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
# Cap evaluation (pure, testable without network)
# ---------------------------------------------------------------------------- #


@dataclass(frozen=True)
class CapStatus:
    warn_disk: bool
    hard_disk: bool
    warn_runtime: bool
    hard_runtime: bool

    @property
    def hard_breached(self) -> bool:
        return self.hard_disk or self.hard_runtime


def evaluate_caps(cumulative_bytes: int, elapsed_seconds: float) -> CapStatus:
    """Evaluate the amended raw-only disk cap and runtime cap."""
    return CapStatus(
        warn_disk=cumulative_bytes >= RAW_WARN_BYTES,
        hard_disk=cumulative_bytes > RAW_HARD_BYTES,
        warn_runtime=elapsed_seconds >= RUNTIME_WARN_SECONDS,
        hard_runtime=elapsed_seconds >= RUNTIME_HARD_SECONDS,
    )


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


def _non_authorizations() -> dict[str, str]:
    """Explicit non-authorizations recorded inside the manifest and log."""
    return {
        "acquisition_of_additional_data": "unauthorized",
        "authenticated_apis": "forbidden",
        "backtest": "forbidden",
        "credentials": "forbidden",
        "cross_venue": "forbidden",
        "database_creation": "forbidden",
        "decompression_beyond_inventory_and_row_sample": "forbidden",
        "deployment": "forbidden",
        "diagnostics": "forbidden",
        "eligibility_gate_execution": "forbidden",
        "ethusdt": "forbidden",
        "exchange_write": "forbidden",
        "extra_horizons": "forbidden",
        "feature_computation": "forbidden",
        "graphify": "forbidden",
        "label_computation": "forbidden",
        "live_readiness": "forbidden",
        "mark_price": "forbidden",
        "mcp": "forbidden",
        "ml_training": "forbidden",
        "normalization": "forbidden",
        "order_book": "forbidden",
        "paper_shadow": "forbidden",
        "parquet_compaction": "forbidden",
        "private_endpoints": "forbidden",
        "production_keys": "forbidden",
        "research_eligible_flip": "forbidden",
        "sealed_test_split_read": "forbidden",
        "spot": "forbidden",
        "storage_migration": "forbidden",
        "strategy_creation": "forbidden",
        "successor_authorization": "forbidden",
        "successor_state_creation": "forbidden",
        "tick_data": "forbidden",
        "user_stream": "forbidden",
        "v003_creation": "forbidden",
        "v002_terminal_window_read": "forbidden",
        "websockets": "forbidden",
    }


def _platform_summary() -> dict[str, str]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_implementation": platform.python_implementation(),
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
    warnings: list[str],
    hard_caps_crossed: bool,
    fail_closed_stop_conditions: list[str],
) -> None:
    summary = {
        "acquired_file_count": sum(
            1 for e in entries if e.status == "acquired_verified"
        ),
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
        "expected_file_count": EXPECTED_DATE_COUNT,
        "hard_caps_crossed": hard_caps_crossed,
        "missing_file_count": sum(1 for e in entries if e.status == "missing_404"),
        "non_authorizations_preserved": True,
        "research_eligible_after_acquisition": False,
        "row_sample_validation_failure_count": sum(
            1 for e in entries if e.status == "row_sample_validation_failure"
        ),
        "skipped_cap_breach_count": sum(
            1 for e in entries if e.status == "skipped_cap_breach"
        ),
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        "total_row_count": sum((e.row_count or 0) for e in entries),
        "total_size_bytes": sum((e.size_bytes or 0) for e in entries),
    }
    log = {
        "acquired_segment_end": DATE_END.isoformat(),
        "acquired_segment_start": DATE_START.isoformat(),
        "acquisition_run_id": acquisition_run_id,
        "base_commit_sha": BASE_COMMIT_SHA,
        "checksum_url_pattern": CHECKSUM_URL_TEMPLATE,
        "code_commit_sha": code_commit_sha,
        "data_family": DATA_FAMILY,
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
        "fail_closed_stop_conditions": fail_closed_stop_conditions,
        "finished_at_unix_ms": finished_at_unix_ms,
        "finished_at_utc": datetime.fromtimestamp(
            finished_at_unix_ms / 1000.0, tz=UTC
        ).isoformat(),
        "hard_caps_crossed": hard_caps_crossed,
        "market": MARKET,
        "non_authorizations": _non_authorizations(),
        "overall_status": overall_status,
        "per_file_results": [_entry_to_inventory_dict(e) for e in entries],
        "phase": "Phase 4bn-J-R2",
        "phase_id": PHASE_ID,
        "platform_summary": _platform_summary(),
        "python_version": sys.version,
        "raw_hard_bytes": RAW_HARD_BYTES,
        "raw_warn_bytes": RAW_WARN_BYTES,
        "retries_attempted": sum(e.retry_count for e in entries),
        "runtime_hard_seconds": RUNTIME_HARD_SECONDS,
        "runtime_warn_seconds": RUNTIME_WARN_SECONDS,
        "schema_version": SCHEMA_VERSION,
        "segment_label": SEGMENT_LABEL,
        "source_url_pattern": ARCHIVE_URL_TEMPLATE,
        "started_at_unix_ms": started_at_unix_ms,
        "started_at_utc": datetime.fromtimestamp(
            started_at_unix_ms / 1000.0, tz=UTC
        ).isoformat(),
        "strict_fail_closed": strict_fail_closed,
        "summary": summary,
        "symbol_list": list(SYMBOL_LIST),
        "wall_clock_seconds": (finished_at_unix_ms - started_at_unix_ms) // 1000,
        "warnings": warnings,
    }
    atomic_write_text(log_path, json.dumps(log, indent=2, sort_keys=True) + "\n")


def write_segment_manifest(
    manifest_path: Path,
    *,
    code_commit_sha: str,
    date_list: list[str],
    entries: list[DateResult],
    acquisition_log_path: Path,
    acquisition_log_sha256: str,
    output_root: Path,
    warnings: list[str],
    hard_caps_crossed: bool,
    fail_closed_stop_conditions: list[str],
    runtime_seconds: int,
) -> None:
    capture_config_hash = compute_capture_config_hash(date_list, code_commit_sha)
    total_size_bytes = sum((e.size_bytes or 0) for e in entries)
    manifest: dict[str, object] = {
        "acquired_file_count": sum(
            1 for e in entries if e.status == "acquired_verified"
        ),
        "acquired_segment_end": DATE_END.isoformat(),
        "acquired_segment_start": DATE_START.isoformat(),
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
        "checksum_url_pattern": CHECKSUM_URL_TEMPLATE,
        "code_commit_sha": code_commit_sha,
        "created_at_unix_ms": _now_ms(),
        "created_at_utc": datetime.now(tz=UTC).isoformat(),
        "data_family": DATA_FAMILY,
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
        "existing_v002_sealed_test_split": {
            "start": V002_TEST_SPLIT_START.isoformat(),
            "end": V002_TEST_SPLIT_END.isoformat(),
            "touched": False,
        },
        "existing_v002_terminal_window": {
            "start": V002_TERMINAL_START.isoformat(),
            "end": V002_TERMINAL_END.isoformat(),
            "read": False,
            "overwritten": False,
            "redownloaded": False,
        },
        "expected_file_count": EXPECTED_DATE_COUNT,
        "fail_closed_stop_conditions": fail_closed_stop_conditions,
        "full_intended_envelope_end": FULL_ENVELOPE_END.isoformat(),
        "full_intended_envelope_start": FULL_ENVELOPE_START.isoformat(),
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
        "hard_caps_crossed": hard_caps_crossed,
        "invalid_windows": [],
        "market": MARKET,
        "missing_file_count": sum(1 for e in entries if e.status == "missing_404"),
        "non_authorizations": _non_authorizations(),
        "per_file_inventory": [_entry_to_inventory_dict(e) for e in entries],
        "proxy_warning": None,
        "raw_hard_bytes": RAW_HARD_BYTES,
        "raw_warn_bytes": RAW_WARN_BYTES,
        "research_eligible": False,
        "retention_warning": None,
        "runtime_hard_seconds": RUNTIME_HARD_SECONDS,
        "runtime_seconds_measured": runtime_seconds,
        "runtime_warn_seconds": RUNTIME_WARN_SECONDS,
        "schema_version": SCHEMA_VERSION,
        "segment_label": SEGMENT_LABEL,
        "source": SOURCE_LABEL,
        "source_class": SOURCE_CLASS,
        "source_url_pattern": ARCHIVE_URL_TEMPLATE,
        "symbol_list": list(SYMBOL_LIST),
        "test_holdout_touched": False,
        "test_rows_loaded": 0,
        "total_row_count": sum((e.row_count or 0) for e in entries),
        "total_size_bytes": total_size_bytes,
        "version": DATASET_VERSION,
        "warnings": warnings,
    }
    atomic_write_text(
        manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )


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
    warnings: list[str]
    hard_caps_crossed: bool
    fail_closed_stop_conditions: list[str]


def run_acquisition(
    output_root: Path,
    *,
    do_network: bool = True,
    progress_stream: object | None = None,
) -> AcquisitionRunResult:
    """Run the full Phase 4bn-J-R2 segment acquisition with cap enforcement."""
    output_root = output_root.resolve()
    if "data/microstructure" not in str(output_root).replace("\\", "/").lower():
        raise AcquisitionFailClosed(
            f"output_root {output_root!r} is not under data/microstructure/"
        )

    date_list = generate_segment_date_list()
    code_commit_sha = _commit_sha_or_pending()

    manifests_dir = output_root / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = manifests_dir / f"{MANIFEST_STEM}.json"
    log_path = manifests_dir / f"{MANIFEST_STEM}_acquisition_log.json"
    manifest_sha_path = manifest_path.with_suffix(manifest_path.suffix + ".sha256")
    log_sha_path = log_path.with_suffix(log_path.suffix + ".sha256")

    # Refuse to mutate the published v002 manifest, ever.
    published_v002 = manifests_dir / f"{DATASET_FAMILY}__{DATASET_VERSION}.json"
    for p in (manifest_path, log_path, manifest_sha_path, log_sha_path):
        if p.resolve() == published_v002.resolve():
            raise AcquisitionFailClosed(
                "refusing to write to the published v002 manifest path"
            )
        assert_path_under_microstructure(p, output_root)

    repo_root = _REPO_ROOT
    for sample in (
        manifest_path,
        log_path,
        manifest_sha_path,
        log_sha_path,
        output_root / "raw" / DATASET_FAMILY / SYMBOL / "2024" / "03"
        / f"{SYMBOL}-aggTrades-2024-03-01.zip",
        output_root / "staging" / DATASET_FAMILY,
    ):
        if not verify_gitignored(sample, repo_root=repo_root):
            raise AcquisitionFailClosed(
                f"intended output path is not gitignored: {sample}"
            )

    acquisition_run_id = f"phase-{PHASE_ID}-{_now_ms()}-{uuid.uuid4().hex[:8]}"
    events: list[dict[str, object]] = []
    entries: list[DateResult] = []
    warnings: list[str] = []
    fail_closed_stop_conditions: list[str] = []
    warned_disk = False
    warned_runtime = False
    hard_caps_crossed = False
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

    cumulative_bytes = 0
    for i, date_str in enumerate(date_list):
        if progress_stream is not None:
            with contextlib.suppress(AttributeError, OSError):
                progress_stream.write(
                    f"[{i+1}/{EXPECTED_DATE_COUNT}] {date_str} ..."
                )
                progress_stream.flush()
        entry = acquire_one_date(
            date_str,
            output_root=output_root,
            events=events,
            do_network=do_network,
        )
        entries.append(entry)
        cumulative_bytes += entry.size_bytes or 0
        elapsed_seconds = (_now_ms() - started_at_unix_ms) / 1000.0
        caps = evaluate_caps(cumulative_bytes, elapsed_seconds)

        if caps.warn_disk and not warned_disk:
            warned_disk = True
            msg = (
                f"raw-only disk warning threshold crossed: "
                f"{cumulative_bytes} bytes >= {RAW_WARN_BYTES} (10 GiB) "
                f"after {date_str}"
            )
            warnings.append(msg)
            _emit_event(events, event_type="disk_warning", date_str=date_str,
                        details={"cumulative_bytes": cumulative_bytes})
        if caps.warn_runtime and not warned_runtime:
            warned_runtime = True
            msg = (
                f"runtime warning threshold crossed: {elapsed_seconds:.0f}s "
                f">= {RUNTIME_WARN_SECONDS}s (2h) after {date_str}"
            )
            warnings.append(msg)
            _emit_event(events, event_type="runtime_warning", date_str=date_str,
                        details={"elapsed_seconds": elapsed_seconds})

        if progress_stream is not None:
            with contextlib.suppress(AttributeError, OSError):
                progress_stream.write(
                    f" {entry.status}"
                    + (f" ({entry.failure_reason})" if entry.failure_reason else "")
                    + "\n"
                )
                progress_stream.flush()

        if caps.hard_breached:
            hard_caps_crossed = True
            if caps.hard_disk:
                cond = (
                    f"raw-only disk hard cap exceeded: {cumulative_bytes} bytes "
                    f"> {RAW_HARD_BYTES} (25 GiB) after {date_str}; stopped"
                )
            else:
                cond = (
                    f"runtime hard cap exceeded: {elapsed_seconds:.0f}s >= "
                    f"{RUNTIME_HARD_SECONDS}s (4h) after {date_str}; stopped"
                )
            fail_closed_stop_conditions.append(cond)
            warnings.append(cond)
            _emit_event(events, event_type="hard_cap_breach", date_str=date_str,
                        details={"condition": cond})
            # Do not proceed to another day after a hard-cap breach.
            for remaining in date_list[i + 1:]:
                skip_zip, skip_sha = _expected_local_paths(remaining, output_root)
                entries.append(
                    DateResult(
                        date=remaining,
                        expected_url=ARCHIVE_URL_TEMPLATE.format(date=remaining),
                        expected_checksum_url=CHECKSUM_URL_TEMPLATE.format(
                            date=remaining
                        ),
                        local_zip_path=skip_zip.relative_to(
                            output_root.parent
                        ).as_posix(),
                        local_sidecar_path=skip_sha.relative_to(
                            output_root.parent
                        ).as_posix(),
                        status="skipped_cap_breach",
                        sha256=None,
                        sha256_from_companion=None,
                        size_bytes=None,
                        row_count=None,
                        first_trade_time_ms=None,
                        last_trade_time_ms=None,
                        min_agg_trade_id=None,
                        max_agg_trade_id=None,
                        retry_count=0,
                        failure_reason="skipped after hard-cap breach",
                        acquired_at_unix_ms=None,
                    )
                )
            break

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
    if hard_caps_crossed:
        overall_status = "FAIL_CLOSED_CAP_BREACH"
        strict_fail_closed = True
    elif acquired == 0:
        overall_status = "FAIL_CLOSED_NO_ACQUISITION"
        strict_fail_closed = True
    elif acquired == EXPECTED_DATE_COUNT:
        overall_status = "SUCCESSFUL_ACQUISITION"
        strict_fail_closed = False
    else:
        overall_status = "PARTIAL_ACQUISITION"
        strict_fail_closed = False

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
        warnings=warnings,
        hard_caps_crossed=hard_caps_crossed,
        fail_closed_stop_conditions=fail_closed_stop_conditions,
    )
    log_sha = sha256_file(log_path)
    atomic_write_text(log_sha_path, make_sidecar_body(log_sha, log_path.name))

    write_segment_manifest(
        manifest_path,
        code_commit_sha=code_commit_sha,
        date_list=date_list,
        entries=entries,
        acquisition_log_path=log_path,
        acquisition_log_sha256=log_sha,
        output_root=output_root,
        warnings=warnings,
        hard_caps_crossed=hard_caps_crossed,
        fail_closed_stop_conditions=fail_closed_stop_conditions,
        runtime_seconds=(finished_at_unix_ms - started_at_unix_ms) // 1000,
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
        warnings=warnings,
        hard_caps_crossed=hard_caps_crossed,
        fail_closed_stop_conditions=fail_closed_stop_conditions,
    )


# ---------------------------------------------------------------------------- #
# Disk-footprint preflight (HEAD only; no body download)
# ---------------------------------------------------------------------------- #


def preflight_estimate(*, sample_limit: int | None = None) -> dict[str, object]:
    """Estimate the raw footprint via HTTP HEAD Content-Length.

    Downloads no archive bodies. Returns a dict with the per-date sizes
    observed, the extrapolated total, and a fail-closed verdict against
    the 25 GiB hard cap.
    """
    date_list = generate_segment_date_list()
    probe_dates = (
        date_list[:sample_limit] if sample_limit is not None else date_list
    )
    sizes: dict[str, int] = {}
    missing: list[str] = []
    for date_str in probe_dates:
        url = build_archive_url(date_str)
        try:
            length = _http_head_content_length(url)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            missing.append(f"{date_str}: {type(exc).__name__}: {exc}")
            continue
        if length is None:
            missing.append(f"{date_str}: no Content-Length header")
            continue
        sizes[date_str] = length
    probed_total = sum(sizes.values())
    probed_count = len(sizes)
    avg = 0.0 if probed_count == 0 else probed_total / probed_count
    estimated_total = int(round(avg * EXPECTED_DATE_COUNT))
    return {
        "probed_count": probed_count,
        "probed_total_bytes": probed_total,
        "avg_bytes_per_day": avg,
        "estimated_total_bytes": estimated_total,
        "estimated_total_gib": estimated_total / (1024 ** 3),
        "raw_hard_bytes": RAW_HARD_BYTES,
        "raw_warn_bytes": RAW_WARN_BYTES,
        "exceeds_hard_cap": estimated_total > RAW_HARD_BYTES,
        "exceeds_warn_threshold": estimated_total >= RAW_WARN_BYTES,
        "missing": missing,
    }


# ---------------------------------------------------------------------------- #
# CLI
# ---------------------------------------------------------------------------- #


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Phase 4bn-J-R2: acquire the 275 new pre-v002 BTCUSDT public "
            "aggTrades daily archives (2024-03-01 .. 2024-11-30 inclusive "
            "UTC) from data.binance.vision, raw-only, with the amended "
            "10 GiB / 25 GiB raw-only disk cap and 2 h / 4 h runtime cap."
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
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="HEAD-only disk-footprint estimate (no archive bodies).",
    )
    parser.add_argument(
        "--preflight-sample",
        type=int,
        default=None,
        help="Probe only the first N dates during --preflight (HEAD only).",
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
        date_list = generate_segment_date_list()
        print("Phase 4bn-J-R2 dry-run plan:")
        print(f"  symbols        : {SYMBOL_LIST}")
        print(f"  market         : {MARKET}")
        print(f"  data_family    : {DATA_FAMILY}")
        print(f"  date_start     : {DATE_START.isoformat()}")
        print(f"  date_end       : {DATE_END.isoformat()}")
        print(f"  date_count     : {len(date_list)}")
        print(f"  url_template   : {ARCHIVE_URL_TEMPLATE}")
        print(f"  output_root    : {output_root}")
        print(f"  manifest_path  : {output_root}/manifests/{MANIFEST_STEM}.json")
        print(
            f"  log_path       : "
            f"{output_root}/manifests/{MANIFEST_STEM}_acquisition_log.json"
        )
        print(f"  raw_warn_bytes : {RAW_WARN_BYTES} (10 GiB)")
        print(f"  raw_hard_bytes : {RAW_HARD_BYTES} (25 GiB)")
        print(f"  first_3_dates  : {date_list[:3]}")
        print(f"  last_3_dates   : {date_list[-3:]}")
        print("No download will be performed.")
        return 0

    if args.preflight:
        est = preflight_estimate(sample_limit=args.preflight_sample)
        print("Phase 4bn-J-R2 disk-footprint preflight (HEAD only):")
        for k in (
            "probed_count",
            "probed_total_bytes",
            "avg_bytes_per_day",
            "estimated_total_bytes",
            "estimated_total_gib",
            "exceeds_warn_threshold",
            "exceeds_hard_cap",
        ):
            print(f"  {k:24s}: {est[k]}")
        if est["missing"]:
            print(f"  missing_or_errors       : {len(est['missing'])}")
            for m in est["missing"][:10]:
                print(f"    - {m}")
        if est["exceeds_hard_cap"]:
            print(
                "FAIL_CLOSED: estimated raw footprint exceeds 25 GiB hard cap.",
                file=sys.stderr,
            )
            return 3
        return 0

    try:
        result = run_acquisition(
            output_root=output_root,
            do_network=True,
            progress_stream=sys.stdout,
        )
    except AcquisitionFailClosed as exc:
        print(f"Phase 4bn-J-R2: FAIL_CLOSED ({exc})", file=sys.stderr)
        return 1

    print("Phase 4bn-J-R2: " + result.overall_status)
    summary = {
        "acquired": sum(
            1 for e in result.entries if e.status == "acquired_verified"
        ),
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
        "skipped_cap_breach": sum(
            1 for e in result.entries if e.status == "skipped_cap_breach"
        ),
    }
    for k, v in summary.items():
        print(f"  {k:32s}: {v}")
    total_bytes = sum((e.size_bytes or 0) for e in result.entries)
    print(f"  manifest_path                   : {result.manifest_path}")
    print(f"  manifest_sha256                 : {result.manifest_sha256}")
    print(f"  acquisition_log_path            : {result.acquisition_log_path}")
    print(f"  acquisition_log_sha256          : {result.acquisition_log_sha256}")
    print(f"  total_size_bytes                : {total_bytes}")
    print(f"  total_size_gib                  : {total_bytes / (1024 ** 3):.3f}")
    print(
        f"  total_row_count                 : "
        f"{sum((e.row_count or 0) for e in result.entries)}"
    )
    print(f"  hard_caps_crossed               : {result.hard_caps_crossed}")
    print(f"  warnings                        : {len(result.warnings)}")
    for w in result.warnings:
        print(f"    - {w}")
    print(
        f"  wall_clock_seconds              : "
        f"{(result.finished_at_unix_ms - result.started_at_unix_ms) // 1000}"
    )

    if result.overall_status.startswith("FAIL_CLOSED"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
