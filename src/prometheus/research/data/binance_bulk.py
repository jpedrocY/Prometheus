"""Binance public bulk-download client for historical USD-M futures klines.

## TD-006 verification evidence (2026-04-19)

This module implements a targeted subset of TD-006
(`docs/12-roadmap/technical-debt-register.md`). Only the bulk-CSV path
is verified here; REST klines and user-stream verifications remain OPEN
for later phases.

Verified against official Binance sources on 2026-04-19:

1. Bulk-data repository: https://github.com/binance/binance-public-data
   README confirms:
     * Base URL is ``https://data.binance.vision/``.
     * Each ZIP has a paired ``.CHECKSUM`` file for integrity verification.
     * Kline CSV columns (12 in order): open_time, open, high, low, close,
       volume, close_time, quote_asset_volume, Number of trades,
       Taker buy base asset volume, Taker buy quote asset volume, Ignore.
     * Supported interval strings include ``15m`` and ``1h``.
     * SPOT data switched to microseconds on 2025-01-01. USD-M futures
       remain on UTC milliseconds per the README examples. Runtime parsing
       validates open_time alignment to catch any future drift.

   Correction (GAP-20260419-010): the README shows the column names in
   a table but does NOT explicitly state whether the on-disk CSV has a
   header row. Real BTCUSDT-15m-2026-03 CSV was observed on 2026-04-19
   to contain a header row as line 1 with comma-separated column names
   (``open_time,open,high,low,close,volume,close_time,quote_volume,count,
   taker_buy_volume,taker_buy_quote_volume,ignore``). The ingest helper
   :func:`prometheus.research.data.ingest.extract_rows_from_zip` detects
   and skips the header defensively; files without a header also parse
   correctly. Non-numeric, non-header first rows raise
   :class:`DataIntegrityError` - no silent skipping of unknown content.

2. USD-M futures monthly kline path pattern verified by directly fetching
   https://data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/15m/BTCUSDT-15m-2024-01.zip.CHECKSUM
   Response (90 bytes, binary/octet-stream):
       "76953983fcd4cc35ac181c4a1c69d28cbb4ef8b983021aac84a111ea4e82ef69  BTCUSDT-15m-2024-01.zip"

   This confirms:
     * Path: /data/futures/um/monthly/klines/<SYMBOL>/<INTERVAL>/
     * ZIP name: <SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip
     * Checksum name: same, with ``.CHECKSUM`` suffix.
     * Checksum format: "<sha256hex>  <filename>" (exactly two spaces).

3. Target months for Gate 2 bounded run verified to exist on 2026-04-19:
     * BTCUSDT-15m-2026-03.zip SHA256
       ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8
     * ETHUSDT-15m-2026-03.zip SHA256
       8070870b512ab7c312329a7fc1a45217fc7aff5ed7bbb4f805d96caf7c99fd5d

Not verified at coding time (tracked as GAPs in the ambiguity log):
  * Rate limits (README does not document; pacing is conservative below).
  * ZIP internal member name convention. The README does not document it;
    this module opens the single entry in the archive regardless of its
    name and validates the CSV column count on the first row.
"""

from __future__ import annotations

import hashlib
import os
import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import httpx

from prometheus.core.errors import DataIntegrityError, PrometheusError
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol

# ---------------------------------------------------------------------------
# URL construction
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "https://data.binance.vision"


class BulkFamily(StrEnum):
    """Bulk-data family directory on ``data.binance.vision``.

    Used to parameterize the URL builders and partition layout so the
    Phase 2b :class:`BulkDownloader` can serve both Phase 2b standard
    klines and Phase 2c mark-price klines without code duplication.

    Values match the Binance bulk-path directory name exactly.
    """

    KLINES = "klines"
    MARK_PRICE_KLINES = "markPriceKlines"


_FAMILY_MONTHLY_PATH = {
    BulkFamily.KLINES: "data/futures/um/monthly/klines",
    BulkFamily.MARK_PRICE_KLINES: "data/futures/um/monthly/markPriceKlines",
}

# Kept for backward compatibility (Phase 2b) — resolves to the klines family.
_MONTHLY_KLINES_PATH = _FAMILY_MONTHLY_PATH[BulkFamily.KLINES]
_DEFAULT_USER_AGENT = "Prometheus-Research/0.0.0 (+https://github.com/jpedrocY/Prometheus)"
_SHA256_HEX_LENGTH = 64
_CHECKSUM_SEPARATOR = "  "  # exactly two spaces per observed format
_MAX_RETRIES = 5
_BACKOFF_START_S = 1.0
_BACKOFF_CAP_S = 30.0
_DEFAULT_PACE_MS = 100
_CHUNK_SIZE = 64 * 1024


def monthly_zip_filename(symbol: Symbol, interval: Interval, year: int, month: int) -> str:
    if not 1 <= month <= 12:
        raise ValueError(f"month must be in [1, 12], got {month}")
    return f"{symbol.value}-{interval.value}-{year:04d}-{month:02d}.zip"


def monthly_zip_url(
    symbol: Symbol,
    interval: Interval,
    year: int,
    month: int,
    *,
    base_url: str = DEFAULT_BASE_URL,
    family: BulkFamily = BulkFamily.KLINES,
) -> str:
    filename = monthly_zip_filename(symbol, interval, year, month)
    path_prefix = _FAMILY_MONTHLY_PATH[family]
    return f"{base_url.rstrip('/')}/{path_prefix}/{symbol.value}/{interval.value}/{filename}"


def monthly_checksum_url(
    symbol: Symbol,
    interval: Interval,
    year: int,
    month: int,
    *,
    base_url: str = DEFAULT_BASE_URL,
    family: BulkFamily = BulkFamily.KLINES,
) -> str:
    return (
        monthly_zip_url(symbol, interval, year, month, base_url=base_url, family=family)
        + ".CHECKSUM"
    )


# ---------------------------------------------------------------------------
# Checksum parsing
# ---------------------------------------------------------------------------


def parse_checksum_line(text: str, *, expected_filename: str) -> str:
    """Parse a Binance ``.CHECKSUM`` file body and return the SHA256 hex.

    The documented format is ``<sha256hex>  <filename>`` (two spaces).
    Raises :class:`DataIntegrityError` on any deviation.
    """
    line = text.strip()
    if _CHECKSUM_SEPARATOR not in line:
        raise DataIntegrityError(f"checksum line missing two-space separator: {line!r}")
    hex_part, _, filename_part = line.partition(_CHECKSUM_SEPARATOR)
    if len(hex_part) != _SHA256_HEX_LENGTH or not all(c in "0123456789abcdef" for c in hex_part):
        raise DataIntegrityError(
            f"checksum hex malformed (expected 64 lowercase hex chars): {hex_part!r}"
        )
    if filename_part != expected_filename:
        raise DataIntegrityError(
            f"checksum filename mismatch: expected {expected_filename!r}, got {filename_part!r}"
        )
    return hex_part


# ---------------------------------------------------------------------------
# Downloader
# ---------------------------------------------------------------------------


class BulkDownloadError(PrometheusError):
    """Raised when a bulk download fails permanently after retries."""


@dataclass(frozen=True)
class DownloadOutcome:
    """Result of downloading and verifying a single monthly ZIP."""

    url: str
    local_path: Path
    sha256: str
    bytes_downloaded: int
    was_cached: bool


class BulkDownloader:
    """HTTP client for Binance public bulk kline downloads.

    Takes a pre-configured :class:`httpx.Client` so tests can inject an
    ``httpx.MockTransport``. The downloader is strictly read-only: only
    ``GET`` requests to ``base_url``.
    """

    def __init__(
        self,
        client: httpx.Client,
        *,
        raw_root: Path,
        base_url: str = DEFAULT_BASE_URL,
        user_agent: str = _DEFAULT_USER_AGENT,
        pace_ms: int = _DEFAULT_PACE_MS,
        family: BulkFamily = BulkFamily.KLINES,
        clock: Callable[[], float] | None = None,
        sleep: Callable[[float], None] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self._client = client
        self._raw_root = raw_root
        self._base_url = base_url.rstrip("/")
        self._user_agent = user_agent
        self._pace_ms = pace_ms
        self._family = family
        self._monotonic = clock or time.monotonic
        self._sleep = sleep or time.sleep
        self._rng = rng or random.Random()
        self._last_request_at: float | None = None

    @property
    def family(self) -> BulkFamily:
        return self._family

    # -- local path layout -----------------------------------------------

    def partition_dir(self, symbol: Symbol, interval: Interval, year: int, month: int) -> Path:
        return (
            self._raw_root
            / "binance_usdm"
            / self._family.value
            / f"symbol={symbol.value}"
            / f"interval={interval.value}"
            / f"year={year:04d}"
            / f"month={month:02d}"
        )

    def local_zip_path(self, symbol: Symbol, interval: Interval, year: int, month: int) -> Path:
        return self.partition_dir(symbol, interval, year, month) / monthly_zip_filename(
            symbol, interval, year, month
        )

    # -- HTTP with retry/backoff -----------------------------------------

    def _pace(self) -> None:
        if self._last_request_at is None:
            self._last_request_at = self._monotonic()
            return
        elapsed_s = self._monotonic() - self._last_request_at
        required_s = self._pace_ms / 1000.0
        if elapsed_s < required_s:
            self._sleep(required_s - elapsed_s)
        self._last_request_at = self._monotonic()

    def _should_retry_status(self, status: int) -> bool:
        return status in {408, 425, 429} or 500 <= status < 600

    def _get_with_retry(self, url: str, *, stream: bool) -> httpx.Response:
        headers = {"User-Agent": self._user_agent}
        last_error: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            self._pace()
            try:
                if stream:
                    response = self._client.send(
                        self._client.build_request("GET", url, headers=headers),
                        stream=True,
                    )
                else:
                    response = self._client.get(url, headers=headers)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt >= _MAX_RETRIES:
                    break
                self._backoff(attempt)
                continue

            if self._should_retry_status(response.status_code):
                if stream:
                    response.close()
                last_error = BulkDownloadError(f"retriable HTTP {response.status_code} from {url}")
                if attempt >= _MAX_RETRIES:
                    break
                self._backoff(attempt)
                continue

            if response.status_code >= 400:
                if stream:
                    response.close()
                raise BulkDownloadError(f"non-retriable HTTP {response.status_code} from {url}")

            return response

        raise BulkDownloadError(f"exhausted {_MAX_RETRIES} retries fetching {url}: {last_error!r}")

    def _backoff(self, attempt: int) -> None:
        base = min(_BACKOFF_CAP_S, _BACKOFF_START_S * (2 ** (attempt - 1)))
        jitter = self._rng.uniform(0.0, base * 0.25)
        self._sleep(base + jitter)

    # -- checksum + zip fetches ------------------------------------------

    def fetch_checksum(self, symbol: Symbol, interval: Interval, year: int, month: int) -> str:
        """Return the expected SHA256 hex for the monthly ZIP."""
        url = monthly_checksum_url(
            symbol, interval, year, month, base_url=self._base_url, family=self._family
        )
        response = self._get_with_retry(url, stream=False)
        return parse_checksum_line(
            response.text,
            expected_filename=monthly_zip_filename(symbol, interval, year, month),
        )

    def download_month(
        self,
        symbol: Symbol,
        interval: Interval,
        year: int,
        month: int,
    ) -> DownloadOutcome:
        """Download and SHA256-verify one monthly kline ZIP.

        Idempotent: if the target file already exists and its SHA256
        matches the published ``.CHECKSUM``, the file is reused and
        ``was_cached=True`` in the outcome.
        """
        url = monthly_zip_url(
            symbol, interval, year, month, base_url=self._base_url, family=self._family
        )
        dest = self.local_zip_path(symbol, interval, year, month)
        expected_sha256 = self.fetch_checksum(symbol, interval, year, month)

        if dest.is_file():
            actual = _sha256_of(dest)
            if actual == expected_sha256:
                return DownloadOutcome(
                    url=url,
                    local_path=dest,
                    sha256=actual,
                    bytes_downloaded=0,
                    was_cached=True,
                )
            # Stale on-disk file; fall through to re-download.
            dest.unlink()

        dest.parent.mkdir(parents=True, exist_ok=True)
        partial = dest.with_suffix(dest.suffix + ".partial")

        response = self._get_with_retry(url, stream=True)
        hasher = hashlib.sha256()
        bytes_written = 0
        try:
            with partial.open("wb") as fh:
                for chunk in response.iter_bytes(chunk_size=_CHUNK_SIZE):
                    if not chunk:
                        continue
                    fh.write(chunk)
                    hasher.update(chunk)
                    bytes_written += len(chunk)
        finally:
            response.close()

        actual_sha256 = hasher.hexdigest()
        if actual_sha256 != expected_sha256:
            partial.unlink(missing_ok=True)
            raise DataIntegrityError(
                f"checksum mismatch for {url}: expected {expected_sha256}, got {actual_sha256}"
            )

        os.replace(partial, dest)
        return DownloadOutcome(
            url=url,
            local_path=dest,
            sha256=actual_sha256,
            bytes_downloaded=bytes_written,
            was_cached=False,
        )


def _sha256_of(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(_CHUNK_SIZE), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
