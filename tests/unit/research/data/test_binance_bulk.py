from __future__ import annotations

import hashlib
import random
from pathlib import Path
from typing import Any

import httpx
import pytest

from prometheus.core.errors import DataIntegrityError
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.binance_bulk import (
    BulkDownloader,
    BulkDownloadError,
    monthly_checksum_url,
    monthly_zip_filename,
    monthly_zip_url,
    parse_checksum_line,
)

# ---------------------------------------------------------------------------
# URL construction
# ---------------------------------------------------------------------------


def test_monthly_zip_filename_format() -> None:
    assert (
        monthly_zip_filename(Symbol.BTCUSDT, Interval.I_15M, 2026, 3) == "BTCUSDT-15m-2026-03.zip"
    )


def test_monthly_zip_filename_rejects_bad_month() -> None:
    with pytest.raises(ValueError):
        monthly_zip_filename(Symbol.BTCUSDT, Interval.I_15M, 2026, 13)


def test_monthly_zip_url_default_base() -> None:
    url = monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    assert url == (
        "https://data.binance.vision/data/futures/um/monthly/klines/"
        "BTCUSDT/15m/BTCUSDT-15m-2026-03.zip"
    )


def test_monthly_checksum_url_is_zip_plus_suffix() -> None:
    checksum = monthly_checksum_url(Symbol.ETHUSDT, Interval.I_15M, 2026, 3)
    zip_url = monthly_zip_url(Symbol.ETHUSDT, Interval.I_15M, 2026, 3)
    assert checksum == zip_url + ".CHECKSUM"


def test_monthly_zip_url_respects_custom_base() -> None:
    url = monthly_zip_url(
        Symbol.BTCUSDT, Interval.I_15M, 2026, 3, base_url="https://mirror.example/"
    )
    assert url.startswith("https://mirror.example/data/futures/um/monthly/klines/")


# ---------------------------------------------------------------------------
# parse_checksum_line
# ---------------------------------------------------------------------------


def test_parse_checksum_line_happy() -> None:
    line = (
        "ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8  BTCUSDT-15m-2026-03.zip"
    )
    assert (
        parse_checksum_line(line, expected_filename="BTCUSDT-15m-2026-03.zip")
        == "ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8"
    )


def test_parse_checksum_line_strips_trailing_newline() -> None:
    line = (
        "ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8"
        "  BTCUSDT-15m-2026-03.zip\n"
    )
    assert parse_checksum_line(line, expected_filename="BTCUSDT-15m-2026-03.zip")


def test_parse_checksum_line_rejects_single_space() -> None:
    # README and observed format use TWO spaces; one space must fail.
    line = (
        "ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8 BTCUSDT-15m-2026-03.zip"
    )
    with pytest.raises(DataIntegrityError):
        parse_checksum_line(line, expected_filename="BTCUSDT-15m-2026-03.zip")


def test_parse_checksum_line_rejects_short_hex() -> None:
    line = "abc123  BTCUSDT-15m-2026-03.zip"
    with pytest.raises(DataIntegrityError):
        parse_checksum_line(line, expected_filename="BTCUSDT-15m-2026-03.zip")


def test_parse_checksum_line_rejects_uppercase_hex() -> None:
    line = "EA" + "0" * 62 + "  BTCUSDT-15m-2026-03.zip"
    with pytest.raises(DataIntegrityError):
        parse_checksum_line(line, expected_filename="BTCUSDT-15m-2026-03.zip")


def test_parse_checksum_line_rejects_filename_mismatch() -> None:
    line = (
        "ea25e84ddffdcc8b7ba68fb47363daee6a9ef53941f152c9ebf6d4e165d32bf8  BTCUSDT-15m-2026-02.zip"
    )
    with pytest.raises(DataIntegrityError):
        parse_checksum_line(line, expected_filename="BTCUSDT-15m-2026-03.zip")


# ---------------------------------------------------------------------------
# BulkDownloader with httpx.MockTransport
# ---------------------------------------------------------------------------


class _MockServer:
    """Scriptable mock server returning a fixed response for each URL."""

    def __init__(self, responses: dict[str, list[Any]]) -> None:
        # For each URL, a list of (status, body) or Exception entries consumed in order.
        self._responses = {url: list(queue) for url, queue in responses.items()}
        self.call_log: list[str] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        self.call_log.append(url)
        queue = self._responses.get(url)
        if not queue:
            return httpx.Response(404, content=b"not configured")
        entry = queue.pop(0)
        if isinstance(entry, Exception):
            raise entry
        status, body = entry
        return httpx.Response(status, content=body)


def _fixed_downloader(
    handler: httpx.MockTransport, tmp_path: Path, *, pace_ms: int = 0
) -> BulkDownloader:
    client = httpx.Client(transport=handler)
    return BulkDownloader(
        client=client,
        raw_root=tmp_path,
        pace_ms=pace_ms,
        sleep=lambda _: None,
        rng=random.Random(0),
    )


def _make_content_and_hash(size: int) -> tuple[bytes, str]:
    body = bytes((i % 256) for i in range(size))
    return body, hashlib.sha256(body).hexdigest()


def test_download_happy_path(tmp_path: Path) -> None:
    filename = "BTCUSDT-15m-2026-03.zip"
    body, sha = _make_content_and_hash(512)
    checksum_body = f"{sha}  {filename}".encode()
    zip_url = monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    checksum_url = monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)

    server = _MockServer(
        {
            checksum_url: [(200, checksum_body)],
            zip_url: [(200, body)],
        }
    )
    downloader = _fixed_downloader(httpx.MockTransport(server.handler), tmp_path)
    outcome = downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)

    assert outcome.sha256 == sha
    assert outcome.bytes_downloaded == 512
    assert outcome.was_cached is False
    assert outcome.local_path.name == filename
    assert outcome.local_path.is_file()
    assert outcome.local_path.read_bytes() == body
    # No .partial file left behind.
    assert not outcome.local_path.with_suffix(".zip.partial").exists()


def test_download_user_agent_header_present(tmp_path: Path) -> None:
    body, sha = _make_content_and_hash(64)
    filename = "BTCUSDT-15m-2026-03.zip"
    checksum_body = f"{sha}  {filename}".encode()
    zip_url = monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    checksum_url = monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)

    observed_user_agents: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        observed_user_agents.append(request.headers.get("User-Agent"))
        if str(request.url) == checksum_url:
            return httpx.Response(200, content=checksum_body)
        if str(request.url) == zip_url:
            return httpx.Response(200, content=body)
        return httpx.Response(404)

    downloader = _fixed_downloader(httpx.MockTransport(handler), tmp_path)
    downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    assert all(ua and ua.startswith("Prometheus-Research/") for ua in observed_user_agents)


def test_download_checksum_mismatch_raises(tmp_path: Path) -> None:
    filename = "BTCUSDT-15m-2026-03.zip"
    body, _ = _make_content_and_hash(256)
    wrong_sha = "0" * 64  # doesn't match body
    checksum_body = f"{wrong_sha}  {filename}".encode()

    server = _MockServer(
        {
            monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(200, checksum_body)],
            monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(200, body)],
        }
    )
    downloader = _fixed_downloader(httpx.MockTransport(server.handler), tmp_path)
    with pytest.raises(DataIntegrityError):
        downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)

    # .partial cleaned up; final file not written.
    final = downloader.local_zip_path(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    assert not final.exists()
    assert not final.with_suffix(".zip.partial").exists()


def test_download_retries_on_429_then_succeeds(tmp_path: Path) -> None:
    filename = "BTCUSDT-15m-2026-03.zip"
    body, sha = _make_content_and_hash(64)
    checksum_body = f"{sha}  {filename}".encode()

    server = _MockServer(
        {
            monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [
                (429, b""),
                (429, b""),
                (200, checksum_body),
            ],
            monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(200, body)],
        }
    )
    downloader = _fixed_downloader(httpx.MockTransport(server.handler), tmp_path)
    outcome = downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    assert outcome.sha256 == sha
    # At least 3 calls for the checksum URL.
    checksum_calls = [
        c
        for c in server.call_log
        if c == monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    ]
    assert len(checksum_calls) == 3


def test_download_exhausts_retries_on_persistent_5xx(tmp_path: Path) -> None:
    server = _MockServer(
        {monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(503, b"")] * 10}
    )
    downloader = _fixed_downloader(httpx.MockTransport(server.handler), tmp_path)
    with pytest.raises(BulkDownloadError):
        downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)


def test_download_non_retriable_404_raises(tmp_path: Path) -> None:
    server = _MockServer(
        {
            monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(404, b"")],
        }
    )
    downloader = _fixed_downloader(httpx.MockTransport(server.handler), tmp_path)
    with pytest.raises(BulkDownloadError):
        downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)


def test_download_is_idempotent_when_local_matches(tmp_path: Path) -> None:
    filename = "BTCUSDT-15m-2026-03.zip"
    body, sha = _make_content_and_hash(128)
    checksum_body = f"{sha}  {filename}".encode()

    server = _MockServer(
        {
            monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [
                (200, checksum_body),
                (200, checksum_body),
            ],
            monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(200, body)],
        }
    )
    downloader = _fixed_downloader(httpx.MockTransport(server.handler), tmp_path)
    first = downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    second = downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    assert first.was_cached is False
    assert second.was_cached is True
    assert second.bytes_downloaded == 0
    # ZIP endpoint fetched exactly once.
    zip_calls = [
        c for c in server.call_log if c == monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    ]
    assert len(zip_calls) == 1


def test_download_redownloads_when_local_is_stale(tmp_path: Path) -> None:
    filename = "BTCUSDT-15m-2026-03.zip"
    body, sha = _make_content_and_hash(128)
    checksum_body = f"{sha}  {filename}".encode()

    downloader_path_holder: list[Path] = []

    class _Seed(BulkDownloader):
        def local_zip_path(self, symbol: Symbol, interval: Interval, year: int, month: int) -> Path:
            path = super().local_zip_path(symbol, interval, year, month)
            downloader_path_holder.append(path)
            return path

    server = _MockServer(
        {
            monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [
                (200, checksum_body),
            ],
            monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(200, body)],
        }
    )
    client = httpx.Client(transport=httpx.MockTransport(server.handler))
    downloader = _Seed(
        client=client, raw_root=tmp_path, pace_ms=0, sleep=lambda _: None, rng=random.Random(0)
    )
    # Pre-seed with wrong bytes at the canonical path.
    stale_path = downloader.local_zip_path(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    stale_path.parent.mkdir(parents=True, exist_ok=True)
    stale_path.write_bytes(b"not the right bytes")

    outcome = downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    assert outcome.was_cached is False
    assert outcome.local_path.read_bytes() == body


def test_pace_delay_is_observed(tmp_path: Path) -> None:
    """pace_ms enforces a minimum delay between successive requests."""
    body, sha = _make_content_and_hash(32)
    filename = "BTCUSDT-15m-2026-03.zip"
    checksum_body = f"{sha}  {filename}".encode()

    server = _MockServer(
        {
            monthly_checksum_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(200, checksum_body)],
            monthly_zip_url(Symbol.BTCUSDT, Interval.I_15M, 2026, 3): [(200, body)],
        }
    )
    fake_clock_values = [0.0, 0.001, 0.002]  # monotonic starts near 0
    clock_iter = iter(fake_clock_values + [1.0] * 10)
    slept: list[float] = []
    client = httpx.Client(transport=httpx.MockTransport(server.handler))
    downloader = BulkDownloader(
        client=client,
        raw_root=tmp_path,
        pace_ms=500,
        clock=lambda: next(clock_iter),
        sleep=lambda duration: slept.append(duration),
        rng=random.Random(0),
    )
    downloader.download_month(Symbol.BTCUSDT, Interval.I_15M, 2026, 3)
    # At least one pace-induced sleep should have occurred (close to 0.5s).
    assert any(d >= 0.4 for d in slept)
