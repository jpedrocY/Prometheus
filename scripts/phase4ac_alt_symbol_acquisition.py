"""Phase 4ac - Alt-Symbol Public Data Acquisition and Integrity Validation.

Authority: Phase 4ab (alt-symbol data-requirements / feasibility memo,
docs-only); Phase 4aa (alt-symbol market-selection / admissibility memo);
Phase 4i (V2 acquisition pattern); Phase 3q (5m supplemental + mark-price
acquisition pattern).

Brief: docs-and-data, public unauthenticated `data.binance.vision` bulk
archives only. No credentials. No `.env`. No authenticated REST. No private
endpoints. No public-endpoint code calls. No user stream. No WebSocket. No
listenKey. No exchange-write. No MCP / Graphify / `.mcp.json`.

Core symbol set:
    BTCUSDT  ETHUSDT  SOLUSDT  XRPUSDT  ADAUSDT

Data families and intervals:
    - Standard trade-price klines    : 15m / 30m / 1h / 4h     (REQUIRED)
    - Mark-price klines              : 15m / 30m / 1h / 4h     (CONDITIONAL REQUIRED)
    - Funding rate history (monthly) : per symbol              (REQUIRED if available)

Skip-if-already-covered policy:
    For BTCUSDT and ETHUSDT some __v001 manifests already exist from
    Phase 2 / Phase 3q / Phase 4i. The brief says "Do NOT modify existing
    committed manifests." We skip any (symbol, family, interval) for which
    a `data/manifests/<dataset_version>.manifest.json` file already exists.

End-month policy:
    Try 2026-04 first (current latest fully completed month per Phase 4ac
    brief). If the BTCUSDT 15m kline archive for 2026-04 is unavailable
    (404), fall back to 2026-03 across all families. No partial 2026-05
    data. No fabricated months.

Listing-date policy:
    For SOL/XRP/ADA, archives that 404 at the start of the window are
    treated as "before listing." The first available month becomes the
    dataset start; this is recorded as `listing_date_utc` and described
    in `notes`. No fabricated pre-listing data. No backfill.

Output paths (existing repository convention):
    data/raw/binance_usdm/<family>/symbol=X/[interval=Y/]year=YYYY/month=MM/X-...zip
    data/normalized/<category>/symbol=X/interval=Y/year=YYYY/month=MM/part-0000.parquet
    data/manifests/<dataset_version>.manifest.json

Idempotent. Public unauthenticated only.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import io
import json
import sys
import threading
import time
import zipfile
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import httpx
import pyarrow as pa
import pyarrow.parquet as pq

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(r"C:\Prometheus")
RAW_ROOT = REPO_ROOT / "data" / "raw" / "binance_usdm"
NORMALIZED_KLINES_ROOT = REPO_ROOT / "data" / "normalized" / "klines"
NORMALIZED_MARKPRICE_ROOT = REPO_ROOT / "data" / "normalized" / "markprice_klines"
NORMALIZED_FUNDING_ROOT = REPO_ROOT / "data" / "normalized" / "funding"
MANIFESTS_ROOT = REPO_ROOT / "data" / "manifests"

BASE_URL = "https://data.binance.vision"
USER_AGENT = "Prometheus-Research/0.0.0 (+Phase4ac/alt-symbol-acquisition)"
PIPELINE_VERSION = "prometheus@0.0.0"
GENERATOR = "scripts.phase4ac_alt_symbol_acquisition"

DEFAULT_SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT")
TRADE_PRICE_INTERVALS = ("15m", "30m", "1h", "4h")
MARK_PRICE_INTERVALS = ("15m", "30m", "1h", "4h")

DEFAULT_START = date(2022, 1, 1)
DEFAULT_END_PRIMARY = date(2026, 4, 30)
DEFAULT_END_FALLBACK = date(2026, 3, 31)

INTERVAL_MS = {
    "15m": 15 * 60 * 1000,
    "30m": 30 * 60 * 1000,
    "1h": 60 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
}

DEFAULT_WORKERS = 8
PACE_MS = 50
MAX_RETRIES = 5
BACKOFF_START_S = 1.0
BACKOFF_CAP_S = 30.0

KLINE_COLUMNS_EXPECTED = 12
MARKPRICE_COLUMNS_EXPECTED = 12
FUNDING_COLUMNS_EXPECTED = 3

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class AcquisitionError(Exception):
    """Non-recoverable acquisition or validation problem."""


class MissingArchiveError(AcquisitionError):
    """Public archive returned 404."""


# ---------------------------------------------------------------------------
# HTTP helpers (idempotent, with retry)
# ---------------------------------------------------------------------------


def http_get(client: httpx.Client, url: str) -> bytes:
    last_exc: Exception | None = None
    delay = BACKOFF_START_S
    for _attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = client.get(url, follow_redirects=True, timeout=60)
            if resp.status_code == 200:
                return resp.content
            if resp.status_code == 404:
                raise MissingArchiveError(f"404 for {url}")
            last_exc = AcquisitionError(f"HTTP {resp.status_code} for {url}")
        except (httpx.HTTPError, AcquisitionError) as exc:
            last_exc = exc
        time.sleep(min(delay, BACKOFF_CAP_S))
        delay *= 2
    raise AcquisitionError(
        f"GET failed after {MAX_RETRIES} attempts: {url} ({last_exc})"
    )


def parse_checksum(text: str, expected_filename: str) -> str:
    line = text.strip()
    if "  " not in line:
        raise AcquisitionError(f"checksum missing two-space separator: {line!r}")
    sha, _, fname = line.partition("  ")
    if len(sha) != 64 or not all(c in "0123456789abcdef" for c in sha):
        raise AcquisitionError(f"checksum sha malformed: {sha!r}")
    if fname != expected_filename:
        raise AcquisitionError(
            f"checksum filename mismatch: {fname!r} != {expected_filename!r}"
        )
    return sha


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Iteration helpers
# ---------------------------------------------------------------------------


def iter_months(start: date, end: date) -> list[tuple[int, int]]:
    months: list[tuple[int, int]] = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def kline_raw_path(symbol: str, interval: str, year: int, month: int) -> Path:
    fname = f"{symbol}-{interval}-{year:04d}-{month:02d}.zip"
    return (
        RAW_ROOT
        / "klines"
        / f"symbol={symbol}"
        / f"interval={interval}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / fname
    )


def kline_parquet_path(symbol: str, interval: str, year: int, month: int) -> Path:
    return (
        NORMALIZED_KLINES_ROOT
        / f"symbol={symbol}"
        / f"interval={interval}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / "part-0000.parquet"
    )


def markprice_raw_path(symbol: str, interval: str, year: int, month: int) -> Path:
    fname = f"{symbol}-{interval}-{year:04d}-{month:02d}.zip"
    return (
        RAW_ROOT
        / "markPriceKlines"
        / f"symbol={symbol}"
        / f"interval={interval}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / fname
    )


def markprice_parquet_path(symbol: str, interval: str, year: int, month: int) -> Path:
    return (
        NORMALIZED_MARKPRICE_ROOT
        / f"symbol={symbol}"
        / f"interval={interval}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / "part-0000.parquet"
    )


def funding_raw_path(symbol: str, year: int, month: int) -> Path:
    fname = f"{symbol}-fundingRate-{year:04d}-{month:02d}.zip"
    return (
        RAW_ROOT
        / "fundingRate"
        / f"symbol={symbol}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / fname
    )


def funding_parquet_path(symbol: str, year: int, month: int) -> Path:
    return (
        NORMALIZED_FUNDING_ROOT
        / f"symbol={symbol}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / "part-0000.parquet"
    )


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

KLINES_SCHEMA = pa.schema(
    [
        pa.field("symbol", pa.string(), nullable=False),
        pa.field("interval", pa.string(), nullable=False),
        pa.field("open_time", pa.int64(), nullable=False),
        pa.field("close_time", pa.int64(), nullable=False),
        pa.field("open", pa.float64(), nullable=False),
        pa.field("high", pa.float64(), nullable=False),
        pa.field("low", pa.float64(), nullable=False),
        pa.field("close", pa.float64(), nullable=False),
        pa.field("volume", pa.float64(), nullable=False),
        pa.field("quote_asset_volume", pa.float64(), nullable=False),
        pa.field("count", pa.int64(), nullable=False),
        pa.field("taker_buy_volume", pa.float64(), nullable=False),
        pa.field("taker_buy_quote_asset_volume", pa.float64(), nullable=False),
        pa.field("ignore", pa.float64(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
    ]
)

MARKPRICE_SCHEMA = pa.schema(
    [
        pa.field("symbol", pa.string(), nullable=False),
        pa.field("interval", pa.string(), nullable=False),
        pa.field("open_time", pa.int64(), nullable=False),
        pa.field("close_time", pa.int64(), nullable=False),
        pa.field("open", pa.float64(), nullable=False),
        pa.field("high", pa.float64(), nullable=False),
        pa.field("low", pa.float64(), nullable=False),
        pa.field("close", pa.float64(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
    ]
)

FUNDING_SCHEMA = pa.schema(
    [
        pa.field("symbol", pa.string(), nullable=False),
        pa.field("calc_time", pa.int64(), nullable=False),
        pa.field("funding_interval_hours", pa.int32(), nullable=False),
        pa.field("last_funding_rate", pa.float64(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
    ]
)


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


def _open_single_csv(zip_path: Path) -> Iterable[str]:
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if len(names) != 1:
            raise AcquisitionError(f"expected one CSV in {zip_path}, got {names}")
        with zf.open(names[0]) as fh:
            text = io.TextIOWrapper(fh, encoding="utf-8", newline="")
            yield from text


def parse_kline_zip(zip_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen_first = False
    for index, raw in enumerate(_open_single_csv(zip_path), start=1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != KLINE_COLUMNS_EXPECTED:
            raise AcquisitionError(
                f"{zip_path} line {index}: expected "
                f"{KLINE_COLUMNS_EXPECTED} cols, got {len(parts)}"
            )
        if not seen_first:
            seen_first = True
            if parts[0].strip().lower() == "open_time":
                continue
        try:
            rows.append(
                {
                    "open_time": int(parts[0]),
                    "open": float(parts[1]),
                    "high": float(parts[2]),
                    "low": float(parts[3]),
                    "close": float(parts[4]),
                    "volume": float(parts[5]),
                    "close_time": int(parts[6]),
                    "quote_asset_volume": float(parts[7]),
                    "count": int(parts[8]),
                    "taker_buy_volume": float(parts[9]),
                    "taker_buy_quote_asset_volume": float(parts[10]),
                    "ignore": float(parts[11]),
                }
            )
        except ValueError as exc:
            raise AcquisitionError(
                f"{zip_path} line {index}: bad numeric ({exc})"
            ) from exc
    return rows


def parse_markprice_zip(zip_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen_first = False
    for index, raw in enumerate(_open_single_csv(zip_path), start=1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != MARKPRICE_COLUMNS_EXPECTED:
            raise AcquisitionError(
                f"{zip_path} line {index}: expected "
                f"{MARKPRICE_COLUMNS_EXPECTED} cols, got {len(parts)}"
            )
        if not seen_first:
            seen_first = True
            if parts[0].strip().lower() == "open_time":
                continue
        try:
            rows.append(
                {
                    "open_time": int(parts[0]),
                    "open": float(parts[1]),
                    "high": float(parts[2]),
                    "low": float(parts[3]),
                    "close": float(parts[4]),
                    "close_time": int(parts[6]),
                }
            )
        except ValueError as exc:
            raise AcquisitionError(
                f"{zip_path} line {index}: bad numeric ({exc})"
            ) from exc
    return rows


def parse_funding_zip(zip_path: Path) -> list[dict[str, Any]]:
    """Parse a Binance bulk fundingRate ZIP.

    Expected columns (per current bulk format):
        calc_time, funding_interval_hours, last_funding_rate
    """
    rows: list[dict[str, Any]] = []
    seen_first = False
    for index, raw in enumerate(_open_single_csv(zip_path), start=1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != FUNDING_COLUMNS_EXPECTED:
            raise AcquisitionError(
                f"{zip_path} line {index}: expected "
                f"{FUNDING_COLUMNS_EXPECTED} cols, got {len(parts)}"
            )
        if not seen_first:
            seen_first = True
            if parts[0].strip().lower() in ("calc_time", "calctime"):
                continue
        try:
            rows.append(
                {
                    "calc_time": int(parts[0]),
                    "funding_interval_hours": int(parts[1]),
                    "last_funding_rate": float(parts[2]),
                }
            )
        except ValueError as exc:
            raise AcquisitionError(
                f"{zip_path} line {index}: bad numeric ({exc})"
            ) from exc
    return rows


# ---------------------------------------------------------------------------
# Parquet writers
# ---------------------------------------------------------------------------


def write_kline_parquet(
    rows: list[dict[str, Any]], symbol: str, interval: str, source_url: str, dest: Path
) -> None:
    n = len(rows)
    table = pa.table(
        {
            "symbol": pa.array([symbol] * n, type=pa.string()),
            "interval": pa.array([interval] * n, type=pa.string()),
            "open_time": pa.array([r["open_time"] for r in rows], type=pa.int64()),
            "close_time": pa.array([r["close_time"] for r in rows], type=pa.int64()),
            "open": pa.array([r["open"] for r in rows], type=pa.float64()),
            "high": pa.array([r["high"] for r in rows], type=pa.float64()),
            "low": pa.array([r["low"] for r in rows], type=pa.float64()),
            "close": pa.array([r["close"] for r in rows], type=pa.float64()),
            "volume": pa.array([r["volume"] for r in rows], type=pa.float64()),
            "quote_asset_volume": pa.array(
                [r["quote_asset_volume"] for r in rows], type=pa.float64()
            ),
            "count": pa.array([r["count"] for r in rows], type=pa.int64()),
            "taker_buy_volume": pa.array(
                [r["taker_buy_volume"] for r in rows], type=pa.float64()
            ),
            "taker_buy_quote_asset_volume": pa.array(
                [r["taker_buy_quote_asset_volume"] for r in rows], type=pa.float64()
            ),
            "ignore": pa.array([r["ignore"] for r in rows], type=pa.float64()),
            "source": pa.array([source_url] * n, type=pa.string()),
        },
        schema=KLINES_SCHEMA,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, dest, compression="zstd", compression_level=3)


def write_markprice_parquet(
    rows: list[dict[str, Any]], symbol: str, interval: str, source_url: str, dest: Path
) -> None:
    n = len(rows)
    table = pa.table(
        {
            "symbol": pa.array([symbol] * n, type=pa.string()),
            "interval": pa.array([interval] * n, type=pa.string()),
            "open_time": pa.array([r["open_time"] for r in rows], type=pa.int64()),
            "close_time": pa.array([r["close_time"] for r in rows], type=pa.int64()),
            "open": pa.array([r["open"] for r in rows], type=pa.float64()),
            "high": pa.array([r["high"] for r in rows], type=pa.float64()),
            "low": pa.array([r["low"] for r in rows], type=pa.float64()),
            "close": pa.array([r["close"] for r in rows], type=pa.float64()),
            "source": pa.array([source_url] * n, type=pa.string()),
        },
        schema=MARKPRICE_SCHEMA,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, dest, compression="zstd", compression_level=3)


def write_funding_parquet(
    rows: list[dict[str, Any]], symbol: str, source_url: str, dest: Path
) -> None:
    n = len(rows)
    table = pa.table(
        {
            "symbol": pa.array([symbol] * n, type=pa.string()),
            "calc_time": pa.array([r["calc_time"] for r in rows], type=pa.int64()),
            "funding_interval_hours": pa.array(
                [r["funding_interval_hours"] for r in rows], type=pa.int32()
            ),
            "last_funding_rate": pa.array(
                [r["last_funding_rate"] for r in rows], type=pa.float64()
            ),
            "source": pa.array([source_url] * n, type=pa.string()),
        },
        schema=FUNDING_SCHEMA,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, dest, compression="zstd", compression_level=3)


# ---------------------------------------------------------------------------
# Per-archive acquisition
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ArchiveResult:
    raw_path: Path
    sha256: str
    url: str


_print_lock = threading.Lock()


def _log(msg: str) -> None:
    with _print_lock:
        print(msg, flush=True)


def acquire_archive(
    client: httpx.Client, url: str, raw_dest: Path, fname: str
) -> ArchiveResult:
    """Idempotently download + SHA256-verify a single bulk archive.

    Raises MissingArchiveError if the archive is 404. Raises AcquisitionError
    on any other error.
    """
    checksum_url = url + ".CHECKSUM"

    if raw_dest.exists():
        try:
            checksum_text = http_get(client, checksum_url).decode("utf-8")
            expected = parse_checksum(checksum_text, fname)
            actual = file_sha256(raw_dest)
            if actual == expected:
                return ArchiveResult(raw_path=raw_dest, sha256=expected, url=url)
            raw_dest.unlink()
        except MissingArchiveError:
            raise
        except AcquisitionError:
            pass

    time.sleep(PACE_MS / 1000)
    zip_bytes = http_get(client, url)
    time.sleep(PACE_MS / 1000)
    checksum_text = http_get(client, checksum_url).decode("utf-8")
    expected = parse_checksum(checksum_text, fname)
    actual_sha = hashlib.sha256(zip_bytes).hexdigest()
    if actual_sha != expected:
        raise AcquisitionError(
            f"sha256 mismatch for {url}: expected {expected}, got {actual_sha}"
        )
    raw_dest.parent.mkdir(parents=True, exist_ok=True)
    raw_dest.write_bytes(zip_bytes)
    return ArchiveResult(raw_path=raw_dest, sha256=actual_sha, url=url)


# ---------------------------------------------------------------------------
# Family-level acquisition
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class MonthRecord:
    symbol: str
    family: str  # "klines" / "markPriceKlines" / "fundingRate"
    interval: str  # for klines / markPriceKlines; "" for fundingRate
    year: int
    month: int
    url: str
    sha256: str
    raw_path: Path
    parquet_path: Path
    row_count: int


def _kline_url(symbol: str, interval: str, year: int, month: int) -> tuple[str, str]:
    fname = f"{symbol}-{interval}-{year:04d}-{month:02d}.zip"
    url = f"{BASE_URL}/data/futures/um/monthly/klines/{symbol}/{interval}/{fname}"
    return url, fname


def _markprice_url(
    symbol: str, interval: str, year: int, month: int
) -> tuple[str, str]:
    fname = f"{symbol}-{interval}-{year:04d}-{month:02d}.zip"
    url = (
        f"{BASE_URL}/data/futures/um/monthly/markPriceKlines/"
        f"{symbol}/{interval}/{fname}"
    )
    return url, fname


def _funding_url(symbol: str, year: int, month: int) -> tuple[str, str]:
    fname = f"{symbol}-fundingRate-{year:04d}-{month:02d}.zip"
    url = f"{BASE_URL}/data/futures/um/monthly/fundingRate/{symbol}/{fname}"
    return url, fname


@dataclasses.dataclass
class FamilyAcquisitionResult:
    """Outcome of acquiring one (symbol, family, interval) dataset family."""

    symbol: str
    family: str
    interval: str
    months_attempted: list[tuple[int, int]]
    months_acquired: list[tuple[int, int]]
    months_404: list[tuple[int, int]]
    records: list[MonthRecord]
    listing_first_month: tuple[int, int] | None
    end_month: tuple[int, int]


def acquire_kline_family(
    client: httpx.Client,
    symbol: str,
    interval: str,
    family: str,  # "klines" or "markPriceKlines"
    months: list[tuple[int, int]],
    workers: int,
) -> FamilyAcquisitionResult:
    """Acquire monthly archives for a single (symbol, family, interval).

    Allows leading-month 404s (treated as before-listing) but treats trailing
    404s as end-of-availability. Holes in the middle of the window become
    `months_404` entries that surface as gaps in the integrity report.
    """
    raws: dict[tuple[int, int], ArchiveResult] = {}
    missing: list[tuple[int, int]] = []
    lock = threading.Lock()

    def _job(year: int, month: int) -> tuple[int, int, ArchiveResult | None]:
        if family == "klines":
            url, fname = _kline_url(symbol, interval, year, month)
            rp = kline_raw_path(symbol, interval, year, month)
        elif family == "markPriceKlines":
            url, fname = _markprice_url(symbol, interval, year, month)
            rp = markprice_raw_path(symbol, interval, year, month)
        else:
            raise AcquisitionError(f"unknown kline family: {family}")
        try:
            return year, month, acquire_archive(client, url, rp, fname)
        except MissingArchiveError:
            return year, month, None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_job, y, m) for (y, m) in months]
        completed = 0
        total = len(months)
        for fut in as_completed(futures):
            year, month, res = fut.result()
            with lock:
                if res is None:
                    missing.append((year, month))
                else:
                    raws[(year, month)] = res
                completed += 1
                if completed % 20 == 0 or completed == total:
                    _log(
                        f"  {family} {symbol} {interval}: {completed}/{total} "
                        f"acquired={len(raws)} missing={len(missing)}"
                    )

    # Determine listing-first-month: leading run of missing months from start.
    listing_first: tuple[int, int] | None = None
    months_sorted = sorted(months)
    leading_missing: set[tuple[int, int]] = set()
    for ym in months_sorted:
        if ym in raws:
            listing_first = ym
            break
        leading_missing.add(ym)

    # Trailing missing months are also acceptable (end-of-availability).
    months_404_middle: list[tuple[int, int]] = []
    after_first = False
    for ym in months_sorted:
        if ym in raws:
            after_first = True
            continue
        if not after_first:
            continue  # leading missing (pre-listing)
        # ym is missing AFTER first available; check if it's trailing.
        idx = months_sorted.index(ym)
        any_later_present = any(later in raws for later in months_sorted[idx + 1:])
        if any_later_present:
            months_404_middle.append(ym)

    # Determine end-month: last month present in raws (or if none, fail).
    if not raws:
        raise AcquisitionError(
            f"no archives acquired for {family} {symbol} {interval} "
            f"over months {months_sorted[0]}..{months_sorted[-1]}"
        )
    end_month = max(raws.keys())

    # Normalize present months into Parquet.
    records: list[MonthRecord] = []
    for ym in sorted(raws.keys()):
        year, month = ym
        res = raws[ym]
        if family == "klines":
            rows = parse_kline_zip(res.raw_path)
            pp = kline_parquet_path(symbol, interval, year, month)
            write_kline_parquet(rows, symbol, interval, res.url, pp)
        else:  # markPriceKlines
            rows = parse_markprice_zip(res.raw_path)
            pp = markprice_parquet_path(symbol, interval, year, month)
            write_markprice_parquet(rows, symbol, interval, res.url, pp)
        if not rows:
            raise AcquisitionError(f"empty rows from {res.raw_path}")
        records.append(
            MonthRecord(
                symbol=symbol,
                family=family,
                interval=interval,
                year=year,
                month=month,
                url=res.url,
                sha256=res.sha256,
                raw_path=res.raw_path,
                parquet_path=pp,
                row_count=len(rows),
            )
        )

    return FamilyAcquisitionResult(
        symbol=symbol,
        family=family,
        interval=interval,
        months_attempted=list(months_sorted),
        months_acquired=sorted(raws.keys()),
        months_404=sorted(missing),
        records=records,
        listing_first_month=listing_first,
        end_month=end_month,
    )


def acquire_funding_family(
    client: httpx.Client,
    symbol: str,
    months: list[tuple[int, int]],
    workers: int,
) -> FamilyAcquisitionResult:
    raws: dict[tuple[int, int], ArchiveResult] = {}
    missing: list[tuple[int, int]] = []
    lock = threading.Lock()

    def _job(year: int, month: int) -> tuple[int, int, ArchiveResult | None]:
        url, fname = _funding_url(symbol, year, month)
        rp = funding_raw_path(symbol, year, month)
        try:
            return year, month, acquire_archive(client, url, rp, fname)
        except MissingArchiveError:
            return year, month, None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_job, y, m) for (y, m) in months]
        completed = 0
        total = len(months)
        for fut in as_completed(futures):
            year, month, res = fut.result()
            with lock:
                if res is None:
                    missing.append((year, month))
                else:
                    raws[(year, month)] = res
                completed += 1
                if completed % 10 == 0 or completed == total:
                    _log(
                        f"  fundingRate {symbol}: {completed}/{total} "
                        f"acquired={len(raws)} missing={len(missing)}"
                    )

    months_sorted = sorted(months)
    listing_first: tuple[int, int] | None = None
    for ym in months_sorted:
        if ym in raws:
            listing_first = ym
            break

    months_404_middle: list[tuple[int, int]] = []
    after_first = False
    for ym in months_sorted:
        if ym in raws:
            after_first = True
            continue
        if not after_first:
            continue
        idx = months_sorted.index(ym)
        any_later_present = any(later in raws for later in months_sorted[idx + 1:])
        if any_later_present:
            months_404_middle.append(ym)

    if not raws:
        # Funding entirely unavailable through bulk.
        return FamilyAcquisitionResult(
            symbol=symbol,
            family="fundingRate",
            interval="",
            months_attempted=months_sorted,
            months_acquired=[],
            months_404=sorted(missing),
            records=[],
            listing_first_month=None,
            end_month=(0, 0),
        )

    end_month = max(raws.keys())

    records: list[MonthRecord] = []
    for ym in sorted(raws.keys()):
        year, month = ym
        res = raws[ym]
        rows = parse_funding_zip(res.raw_path)
        pp = funding_parquet_path(symbol, year, month)
        write_funding_parquet(rows, symbol, res.url, pp)
        records.append(
            MonthRecord(
                symbol=symbol,
                family="fundingRate",
                interval="",
                year=year,
                month=month,
                url=res.url,
                sha256=res.sha256,
                raw_path=res.raw_path,
                parquet_path=pp,
                row_count=len(rows),
            )
        )

    return FamilyAcquisitionResult(
        symbol=symbol,
        family="fundingRate",
        interval="",
        months_attempted=months_sorted,
        months_acquired=sorted(raws.keys()),
        months_404=sorted(missing),
        records=records,
        listing_first_month=listing_first,
        end_month=end_month,
    )


# ---------------------------------------------------------------------------
# Integrity reports
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class KlineIntegrityReport:
    bar_count: int
    first_open_time_ms: int
    last_open_time_ms: int
    monotone_timestamps: bool
    duplicate_timestamps: int
    boundary_alignment_violations: int
    close_time_consistency_violations: int
    gaps_detected: int
    gap_locations: list[dict[str, int]]
    ohlc_sanity_violations: int
    volume_sanity_violations: int
    taker_buy_volume_present: bool
    taker_buy_volume_violations: int
    symbol_consistency_violations: int
    interval_consistency_violations: int
    months_404: list[tuple[int, int]]
    middle_gap_months: list[tuple[int, int]]
    listing_first_month: tuple[int, int] | None
    end_month: tuple[int, int]
    family: str  # "klines" or "markPriceKlines"

    def passes(self) -> bool:
        if self.bar_count == 0:
            return False
        no_middle_gaps = not self.middle_gap_months
        ohlc_block = self.ohlc_sanity_violations == 0
        if self.family == "klines":
            volume_block = (
                self.volume_sanity_violations == 0
                and self.taker_buy_volume_present
                and self.taker_buy_volume_violations == 0
            )
        else:
            # markPriceKlines have no volume / taker fields
            volume_block = True
        return (
            self.gaps_detected == 0
            and self.monotone_timestamps
            and self.duplicate_timestamps == 0
            and self.boundary_alignment_violations == 0
            and self.close_time_consistency_violations == 0
            and ohlc_block
            and volume_block
            and self.symbol_consistency_violations == 0
            and self.interval_consistency_violations == 0
            and no_middle_gaps
        )


def _kline_table_columns(records: list[MonthRecord], family: str) -> dict[str, list]:
    """Combine all month parquet rows for a family into per-column lists."""
    if not records:
        return {}
    months_sorted = sorted(records, key=lambda r: (r.year, r.month))
    tables = [pq.ParquetFile(str(r.parquet_path)).read() for r in months_sorted]
    combined = pa.concat_tables(tables)
    cols: dict[str, list] = {
        "open_time": combined.column("open_time").to_pylist(),
        "close_time": combined.column("close_time").to_pylist(),
        "symbol": combined.column("symbol").to_pylist(),
        "interval": combined.column("interval").to_pylist(),
        "open": combined.column("open").to_pylist(),
        "high": combined.column("high").to_pylist(),
        "low": combined.column("low").to_pylist(),
        "close": combined.column("close").to_pylist(),
    }
    if family == "klines":
        cols["volume"] = combined.column("volume").to_pylist()
        cols["quote_asset_volume"] = combined.column("quote_asset_volume").to_pylist()
        cols["count"] = combined.column("count").to_pylist()
        cols["taker_buy_volume"] = combined.column("taker_buy_volume").to_pylist()
    return cols


def integrity_check_klines_family(
    fr: FamilyAcquisitionResult,
) -> KlineIntegrityReport:
    family = fr.family
    interval = fr.interval
    if family not in ("klines", "markPriceKlines"):
        raise AcquisitionError(f"integrity_check_klines_family unsupported {family}")
    cols = _kline_table_columns(fr.records, family)
    if not cols:
        return KlineIntegrityReport(
            bar_count=0,
            first_open_time_ms=0,
            last_open_time_ms=0,
            monotone_timestamps=False,
            duplicate_timestamps=0,
            boundary_alignment_violations=0,
            close_time_consistency_violations=0,
            gaps_detected=0,
            gap_locations=[],
            ohlc_sanity_violations=0,
            volume_sanity_violations=0,
            taker_buy_volume_present=False,
            taker_buy_volume_violations=0,
            symbol_consistency_violations=0,
            interval_consistency_violations=0,
            months_404=fr.months_404,
            middle_gap_months=[],
            listing_first_month=fr.listing_first_month,
            end_month=fr.end_month,
            family=family,
        )

    interval_ms = INTERVAL_MS[interval]
    open_times = cols["open_time"]
    close_times = cols["close_time"]
    syms = cols["symbol"]
    ivls = cols["interval"]
    opens = cols["open"]
    highs = cols["high"]
    lows = cols["low"]
    closes = cols["close"]

    bar_count = len(open_times)
    boundary_violations = sum(1 for ot in open_times if ot % interval_ms != 0)
    close_violations = sum(
        1
        for ot, ct in zip(open_times, close_times, strict=True)
        if ct != ot + interval_ms - 1
    )

    monotone = True
    duplicates = 0
    gaps: list[dict[str, int]] = []
    for i in range(1, bar_count):
        prev = open_times[i - 1]
        curr = open_times[i]
        if curr == prev:
            duplicates += 1
        elif curr < prev:
            monotone = False
        elif curr - prev != interval_ms:
            gaps.append(
                {"prev_open_time_ms": int(prev), "next_open_time_ms": int(curr)}
            )

    ohlc_violations = 0
    for o, h, lo, c in zip(opens, highs, lows, closes, strict=True):
        if not (lo > 0 and h > 0 and o > 0 and c > 0):
            ohlc_violations += 1
            continue
        if not (lo <= o <= h):
            ohlc_violations += 1
            continue
        if not (lo <= c <= h):
            ohlc_violations += 1

    if family == "klines":
        volumes = cols["volume"]
        qvols = cols["quote_asset_volume"]
        counts = cols["count"]
        taker_buy = cols["taker_buy_volume"]
        volume_violations = sum(
            1
            for v, qv, tc in zip(volumes, qvols, counts, strict=True)
            if v < 0 or qv < 0 or tc < 0
        )
        taker_present = all(tb is not None for tb in taker_buy)
        taker_violations = sum(
            1
            for tb, v in zip(taker_buy, volumes, strict=True)
            if tb is None or tb < 0 or tb > v + 1e-9
        )
    else:
        volume_violations = 0
        taker_present = False
        taker_violations = 0

    sym_violations = sum(1 for s in syms if s != fr.symbol)
    ivl_violations = sum(1 for v in ivls if v != interval)

    # Determine middle-gap months: months in attempted list that are missing
    # AND fall strictly between first acquired month and end month.
    if fr.listing_first_month and fr.end_month:
        first = fr.listing_first_month
        end = fr.end_month
        middle_gaps = [
            ym
            for ym in fr.months_404
            if first < ym < end
        ]
    else:
        middle_gaps = []

    return KlineIntegrityReport(
        bar_count=bar_count,
        first_open_time_ms=int(min(open_times)),
        last_open_time_ms=int(max(open_times)),
        monotone_timestamps=monotone,
        duplicate_timestamps=duplicates,
        boundary_alignment_violations=boundary_violations,
        close_time_consistency_violations=close_violations,
        gaps_detected=len(gaps),
        gap_locations=gaps[:50],
        ohlc_sanity_violations=ohlc_violations,
        volume_sanity_violations=volume_violations,
        taker_buy_volume_present=taker_present,
        taker_buy_volume_violations=taker_violations,
        symbol_consistency_violations=sym_violations,
        interval_consistency_violations=ivl_violations,
        months_404=fr.months_404,
        middle_gap_months=middle_gaps,
        listing_first_month=fr.listing_first_month,
        end_month=fr.end_month,
        family=family,
    )


@dataclasses.dataclass
class FundingIntegrityReport:
    record_count: int
    first_calc_time_ms: int
    last_calc_time_ms: int
    monotone_timestamps: bool
    duplicate_timestamps: int
    nonfinite_violations: int
    symbol_consistency_violations: int
    months_404: list[tuple[int, int]]
    middle_gap_months: list[tuple[int, int]]
    listing_first_month: tuple[int, int] | None
    end_month: tuple[int, int]

    def passes(self) -> bool:
        if self.record_count == 0:
            return False
        return (
            self.monotone_timestamps
            and self.duplicate_timestamps == 0
            and self.nonfinite_violations == 0
            and self.symbol_consistency_violations == 0
            and not self.middle_gap_months
        )


def integrity_check_funding(fr: FamilyAcquisitionResult) -> FundingIntegrityReport:
    if not fr.records:
        return FundingIntegrityReport(
            record_count=0,
            first_calc_time_ms=0,
            last_calc_time_ms=0,
            monotone_timestamps=False,
            duplicate_timestamps=0,
            nonfinite_violations=0,
            symbol_consistency_violations=0,
            months_404=fr.months_404,
            middle_gap_months=[],
            listing_first_month=fr.listing_first_month,
            end_month=fr.end_month,
        )
    months_sorted = sorted(fr.records, key=lambda r: (r.year, r.month))
    tables = [pq.ParquetFile(str(r.parquet_path)).read() for r in months_sorted]
    combined = pa.concat_tables(tables)
    calc_times = combined.column("calc_time").to_pylist()
    syms = combined.column("symbol").to_pylist()
    rates = combined.column("last_funding_rate").to_pylist()

    record_count = len(calc_times)
    monotone = True
    duplicates = 0
    for i in range(1, record_count):
        prev = calc_times[i - 1]
        curr = calc_times[i]
        if curr == prev:
            duplicates += 1
        elif curr < prev:
            monotone = False

    nonfinite = sum(
        1
        for r in rates
        if r != r or r in (float("inf"), float("-inf"))
    )
    sym_violations = sum(1 for s in syms if s != fr.symbol)

    if fr.listing_first_month and fr.end_month and fr.end_month != (0, 0):
        first = fr.listing_first_month
        end = fr.end_month
        middle_gaps = [ym for ym in fr.months_404 if first < ym < end]
    else:
        middle_gaps = []

    return FundingIntegrityReport(
        record_count=record_count,
        first_calc_time_ms=int(min(calc_times)),
        last_calc_time_ms=int(max(calc_times)),
        monotone_timestamps=monotone,
        duplicate_timestamps=duplicates,
        nonfinite_violations=nonfinite,
        symbol_consistency_violations=sym_violations,
        months_404=fr.months_404,
        middle_gap_months=middle_gaps,
        listing_first_month=fr.listing_first_month,
        end_month=fr.end_month,
    )


# ---------------------------------------------------------------------------
# Manifests
# ---------------------------------------------------------------------------


def _command_used() -> str:
    return " ".join(sys.argv)


def _ym_to_str(ym: tuple[int, int] | None) -> str | None:
    if ym is None or ym == (0, 0):
        return None
    return f"{ym[0]:04d}-{ym[1]:02d}"


def write_kline_manifest(
    *,
    fr: FamilyAcquisitionResult,
    integrity: KlineIntegrityReport,
) -> Path:
    sym_lower = fr.symbol.lower()
    if fr.family == "klines":
        dataset_name = f"binance_usdm_{sym_lower}_{fr.interval}"
    else:
        dataset_name = f"binance_usdm_{sym_lower}_markprice_{fr.interval}"
    dataset_version = f"{dataset_name}__v001"
    sources = sorted(r.url for r in fr.records)
    raw_sha256_index = {r.raw_path.name: r.sha256 for r in fr.records}

    invalid_windows: list[dict[str, Any]] = []
    interval_ms = INTERVAL_MS[fr.interval]
    for g in integrity.gap_locations:
        invalid_windows.append(
            {
                "start_open_time_ms": g["prev_open_time_ms"] + interval_ms,
                "end_open_time_ms": g["next_open_time_ms"] - interval_ms,
                "reason": "upstream_data.binance.vision_archive_gap",
            }
        )
    for ym in integrity.middle_gap_months:
        invalid_windows.append(
            {
                "missing_year": ym[0],
                "missing_month": ym[1],
                "reason": "upstream_archive_404_within_listed_window",
            }
        )

    manifest = {
        "schema_version": "kline_v1",
        "dataset_category": "normalized_kline" if fr.family == "klines" else "mark_price_kline",
        "dataset_name": dataset_name,
        "dataset_version": dataset_version,
        "created_at_utc_ms": int(time.time() * 1000),
        "canonical_timezone": "UTC",
        "canonical_timestamp_format": "unix_milliseconds",
        "symbols": [fr.symbol],
        "market": "binance_usdm",
        "instrument_type": "perpetual_futures",
        "intervals": [fr.interval],
        "sources": sources,
        "pipeline_version": PIPELINE_VERSION,
        "partitioning": ["symbol", "interval", "year", "month"],
        "primary_key": ["symbol", "interval", "open_time"],
        "generator": GENERATOR,
        "predecessor_dataset_versions": [],
        "invalid_windows": invalid_windows,
        "notes": (
            f"Phase 4ac alt-symbol acquisition: {fr.family} {fr.interval} "
            f"for {fr.symbol}. Months: "
            f"{_ym_to_str(integrity.listing_first_month)} to "
            f"{_ym_to_str(integrity.end_month)}. "
            "Public unauthenticated data.binance.vision bulk archive only."
        ),
        "listing_first_month_utc": _ym_to_str(integrity.listing_first_month),
        "end_month_utc": _ym_to_str(integrity.end_month),
        "months_404": [_ym_to_str(ym) for ym in integrity.months_404],
        "middle_gap_months": [_ym_to_str(ym) for ym in integrity.middle_gap_months],
        "date_range_start_open_time_utc_ms": integrity.first_open_time_ms,
        "date_range_end_open_time_utc_ms": integrity.last_open_time_ms,
        "bar_count": integrity.bar_count,
        "raw_archive_count": len(fr.records),
        "raw_sha256_index": raw_sha256_index,
        "quality_checks": {
            "monotone_timestamps": integrity.monotone_timestamps,
            "duplicate_timestamps": integrity.duplicate_timestamps,
            "boundary_alignment_violations": integrity.boundary_alignment_violations,
            "close_time_consistency_violations": (
                integrity.close_time_consistency_violations
            ),
            "gaps_detected": integrity.gaps_detected,
            "gap_locations": integrity.gap_locations,
            "ohlc_sanity_violations": integrity.ohlc_sanity_violations,
            "volume_sanity_violations": integrity.volume_sanity_violations,
            "taker_buy_volume_present": integrity.taker_buy_volume_present,
            "taker_buy_volume_violations": integrity.taker_buy_volume_violations,
            "symbol_consistency_violations": integrity.symbol_consistency_violations,
            "interval_consistency_violations": (
                integrity.interval_consistency_violations
            ),
            "middle_gap_months": [
                _ym_to_str(ym) for ym in integrity.middle_gap_months
            ],
            "research_eligible": integrity.passes(),
        },
        "research_eligible": integrity.passes(),
        "partial_eligibility": None,
        "known_exclusions": [],
        "governance_references": [
            "Phase 4ab data-requirements / feasibility memo",
            "Phase 4aa alt-symbol admissibility memo",
            "Phase 4i V2 acquisition pattern",
            "Phase 3p §4.7 strict integrity gate",
            "Phase 3r §8 mark-price gap governance"
            if fr.family == "markPriceKlines"
            else "Phase 4i kline integrity precedent",
        ],
        "operator_authorization_ref": "Phase 4ac authorization brief, 2026-05-04",
        "command_used": _command_used(),
        "no_credentials_confirmation": True,
        "private_endpoint_used": False,
        "authenticated_api_used": False,
        "websocket_used": False,
        "user_stream_used": False,
        "exchange_write_attempted": False,
    }
    path = MANIFESTS_ROOT / f"{dataset_version}.manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


def write_funding_manifest(
    *,
    fr: FamilyAcquisitionResult,
    integrity: FundingIntegrityReport,
) -> Path:
    sym_lower = fr.symbol.lower()
    dataset_name = f"binance_usdm_{sym_lower}_funding"
    dataset_version = f"{dataset_name}__v001"
    sources = sorted(r.url for r in fr.records)
    raw_sha256_index = {r.raw_path.name: r.sha256 for r in fr.records}

    invalid_windows: list[dict[str, Any]] = []
    for ym in integrity.middle_gap_months:
        invalid_windows.append(
            {
                "missing_year": ym[0],
                "missing_month": ym[1],
                "reason": "upstream_archive_404_within_listed_window",
            }
        )

    manifest = {
        "schema_version": "funding_rate_event_v1",
        "dataset_category": "funding_rate_event",
        "dataset_name": dataset_name,
        "dataset_version": dataset_version,
        "created_at_utc_ms": int(time.time() * 1000),
        "canonical_timezone": "UTC",
        "canonical_timestamp_format": "unix_milliseconds",
        "symbols": [fr.symbol],
        "market": "binance_usdm",
        "instrument_type": "perpetual_futures",
        "intervals": [],
        "sources": sources,
        "pipeline_version": PIPELINE_VERSION,
        "partitioning": ["symbol", "year", "month"],
        "primary_key": ["symbol", "calc_time"],
        "generator": GENERATOR,
        "predecessor_dataset_versions": [],
        "invalid_windows": invalid_windows,
        "notes": (
            f"Phase 4ac alt-symbol acquisition: monthly funding rate history "
            f"for {fr.symbol}. Months: "
            f"{_ym_to_str(integrity.listing_first_month)} to "
            f"{_ym_to_str(integrity.end_month)}. "
            "Public unauthenticated data.binance.vision bulk archive only."
        ),
        "listing_first_month_utc": _ym_to_str(integrity.listing_first_month),
        "end_month_utc": _ym_to_str(integrity.end_month),
        "months_404": [_ym_to_str(ym) for ym in integrity.months_404],
        "middle_gap_months": [_ym_to_str(ym) for ym in integrity.middle_gap_months],
        "date_range_start_calc_time_utc_ms": integrity.first_calc_time_ms,
        "date_range_end_calc_time_utc_ms": integrity.last_calc_time_ms,
        "record_count": integrity.record_count,
        "raw_archive_count": len(fr.records),
        "raw_sha256_index": raw_sha256_index,
        "quality_checks": {
            "monotone_timestamps": integrity.monotone_timestamps,
            "duplicate_timestamps": integrity.duplicate_timestamps,
            "nonfinite_violations": integrity.nonfinite_violations,
            "symbol_consistency_violations": integrity.symbol_consistency_violations,
            "middle_gap_months": [
                _ym_to_str(ym) for ym in integrity.middle_gap_months
            ],
            "research_eligible": integrity.passes(),
        },
        "research_eligible": integrity.passes(),
        "partial_eligibility": None,
        "known_exclusions": [],
        "governance_references": [
            "Phase 4ab data-requirements / feasibility memo",
            "Phase 4aa alt-symbol admissibility memo",
        ],
        "operator_authorization_ref": "Phase 4ac authorization brief, 2026-05-04",
        "command_used": _command_used(),
        "no_credentials_confirmation": True,
        "private_endpoint_used": False,
        "authenticated_api_used": False,
        "websocket_used": False,
        "user_stream_used": False,
        "exchange_write_attempted": False,
    }
    path = MANIFESTS_ROOT / f"{dataset_version}.manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Skip-if-already-covered logic
# ---------------------------------------------------------------------------


def kline_manifest_exists(symbol: str, interval: str) -> bool:
    p = MANIFESTS_ROOT / f"binance_usdm_{symbol.lower()}_{interval}__v001.manifest.json"
    return p.exists()


def markprice_manifest_exists(symbol: str, interval: str) -> bool:
    p = (
        MANIFESTS_ROOT
        / f"binance_usdm_{symbol.lower()}_markprice_{interval}__v001.manifest.json"
    )
    return p.exists()


def funding_manifest_exists(symbol: str) -> bool:
    p = MANIFESTS_ROOT / f"binance_usdm_{symbol.lower()}_funding__v001.manifest.json"
    return p.exists()


# ---------------------------------------------------------------------------
# End-month determination
# ---------------------------------------------------------------------------


def determine_end_month(client: httpx.Client) -> tuple[int, int]:
    """Probe BTCUSDT 15m for 2026-04 to decide end-month.

    Returns (year, month). If 2026-04 archive exists and checksum is reachable,
    returns (2026, 4); otherwise falls back to (2026, 3).
    """
    primary = (DEFAULT_END_PRIMARY.year, DEFAULT_END_PRIMARY.month)
    fallback = (DEFAULT_END_FALLBACK.year, DEFAULT_END_FALLBACK.month)
    probe_url, probe_fname = _kline_url("BTCUSDT", "15m", primary[0], primary[1])
    try:
        # HEAD is not necessarily available; do a tiny GET probe via checksum.
        http_get(client, probe_url + ".CHECKSUM")
        _log(f"end-month probe: {probe_fname}.CHECKSUM available -> using {primary}")
        return primary
    except MissingArchiveError:
        _log(
            f"end-month probe: {probe_fname}.CHECKSUM 404 -> "
            f"falling back to {fallback}"
        )
        return fallback


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 4ac alt-symbol acquisition")
    p.add_argument(
        "--symbols",
        nargs="+",
        default=list(DEFAULT_SYMBOLS),
        help="symbols to acquire",
    )
    p.add_argument(
        "--start", default=DEFAULT_START.strftime("%Y-%m"), help="YYYY-MM start"
    )
    p.add_argument(
        "--end",
        default="",
        help="YYYY-MM end (default: probe 2026-04, fallback 2026-03)",
    )
    p.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="print the planned acquisition list and exit",
    )
    p.add_argument(
        "--skip-funding",
        action="store_true",
        help="skip funding-family acquisition entirely (debug only)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    sy, sm = (int(p) for p in args.start.split("-"))
    start = date(sy, sm, 1)

    headers = {"User-Agent": USER_AGENT}

    with httpx.Client(headers=headers) as client:
        if args.end:
            ey, em = (int(p) for p in args.end.split("-"))
        else:
            ey, em = determine_end_month(client)
        # last day of end month
        end_excl = date(ey + 1, 1, 1) if em == 12 else date(ey, em + 1, 1)
        end = end_excl - timedelta(days=1)
        months = iter_months(start, end)

        # Plan: which (symbol, family, interval) tuples to acquire.
        plan: list[tuple[str, str, str]] = []
        skipped: list[tuple[str, str, str, str]] = []  # symbol, family, interval, reason

        for symbol in args.symbols:
            for interval in TRADE_PRICE_INTERVALS:
                if kline_manifest_exists(symbol, interval):
                    skipped.append((symbol, "klines", interval, "manifest_exists"))
                else:
                    plan.append((symbol, "klines", interval))
            for interval in MARK_PRICE_INTERVALS:
                if markprice_manifest_exists(symbol, interval):
                    skipped.append(
                        (symbol, "markPriceKlines", interval, "manifest_exists")
                    )
                else:
                    plan.append((symbol, "markPriceKlines", interval))
            if not args.skip_funding:
                if funding_manifest_exists(symbol):
                    skipped.append((symbol, "fundingRate", "", "manifest_exists"))
                else:
                    plan.append((symbol, "fundingRate", ""))

        _log("=" * 78)
        _log("Phase 4ac acquisition plan")
        _log(f"  start     : {start.isoformat()}")
        _log(f"  end       : {end.isoformat()} (months: {months[0]} .. {months[-1]})")
        _log(f"  symbols   : {args.symbols}")
        _log(f"  workers   : {args.workers}")
        _log(f"  to acquire: {len(plan)} dataset families")
        _log(f"  skipping  : {len(skipped)} dataset families "
             f"(manifests already exist)")
        for s in skipped:
            _log(f"    SKIP {s[0]} {s[1]} {s[2]} ({s[3]})")
        for p_ in plan:
            _log(f"    PLAN {p_[0]} {p_[1]} {p_[2]}")
        _log("=" * 78)

        if args.dry_run:
            _log("dry-run mode -> exiting before any download")
            return 0

        family_results: list[FamilyAcquisitionResult] = []
        manifest_paths: list[Path] = []
        family_failures: list[str] = []

        for (symbol, family, interval) in plan:
            _log(f"acquire {family} {symbol} {interval} ...")
            try:
                if family in ("klines", "markPriceKlines"):
                    fr = acquire_kline_family(
                        client, symbol, interval, family, months, args.workers
                    )
                    family_results.append(fr)
                    integrity = integrity_check_klines_family(fr)
                    mp = write_kline_manifest(fr=fr, integrity=integrity)
                    manifest_paths.append(mp)
                    _log(
                        f"  manifest {mp.name}: bars={integrity.bar_count} "
                        f"gaps={integrity.gaps_detected} "
                        f"acquired_months={len(fr.months_acquired)} "
                        f"missing_months={len(fr.months_404)} "
                        f"middle_gaps={len(integrity.middle_gap_months)} "
                        f"eligible={integrity.passes()}"
                    )
                    if not integrity.passes():
                        family_failures.append(mp.name)
                elif family == "fundingRate":
                    fr = acquire_funding_family(
                        client, symbol, months, args.workers
                    )
                    family_results.append(fr)
                    integrity = integrity_check_funding(fr)
                    if not fr.records:
                        # Funding entirely unavailable; record FAILED manifest
                        # so the report and CPS can reference it.
                        mp = write_funding_manifest(fr=fr, integrity=integrity)
                        manifest_paths.append(mp)
                        _log(
                            f"  funding {symbol}: ENTIRE FAMILY UNAVAILABLE "
                            f"(0 archives)"
                        )
                        family_failures.append(mp.name)
                    else:
                        mp = write_funding_manifest(fr=fr, integrity=integrity)
                        manifest_paths.append(mp)
                        _log(
                            f"  manifest {mp.name}: records={integrity.record_count} "
                            f"acquired_months={len(fr.months_acquired)} "
                            f"missing_months={len(fr.months_404)} "
                            f"middle_gaps={len(integrity.middle_gap_months)} "
                            f"eligible={integrity.passes()}"
                        )
                        if not integrity.passes():
                            family_failures.append(mp.name)
                else:
                    raise AcquisitionError(f"unknown family in plan: {family}")
            except AcquisitionError as exc:
                _log(f"  ERROR {family} {symbol} {interval}: {exc}")
                family_failures.append(f"{symbol}_{family}_{interval}")

        # Final summary
        _log("=" * 78)
        _log("Phase 4ac acquisition summary")
        _log(f"  families acquired      : {len(family_results)}")
        _log(f"  manifests written       : {len(manifest_paths)}")
        _log(f"  family failures         : {len(family_failures)}")
        for f in family_failures:
            _log(f"    FAIL {f}")
        _log("=" * 78)

        return 0  # do not fail the script on per-family integrity failures;
        # the manifests record `research_eligible: false` and the operator
        # reviews via the report.


if __name__ == "__main__":
    sys.exit(main())
