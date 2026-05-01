"""Phase 4i - V2 Public Data Acquisition and Integrity Validation.

Authority: Phase 4g (V2 strategy spec); Phase 4h (data requirements / feasibility).
Brief: docs-and-data, public unauthenticated `data.binance.vision` bulk archives
only, no credentials, no exchange-write paths, no private endpoints.

This script is a standalone orchestrator. It does NOT modify any existing v002
or v001-of-5m dataset, manifest, or ingest function. It uses only raw httpx +
pyarrow + standard library, with the URL convention proven by Phase 3q.

Acquired families (six datasets):

  binance_usdm_btcusdt_30m__v001       (4-year monthly klines, 30m)
  binance_usdm_ethusdt_30m__v001       (4-year monthly klines, 30m)
  binance_usdm_btcusdt_4h__v001        (4-year monthly klines, 4h)
  binance_usdm_ethusdt_4h__v001        (4-year monthly klines, 4h)
  binance_usdm_btcusdt_metrics__v001   (4-year daily metrics, 5m records)
  binance_usdm_ethusdt_metrics__v001   (4-year daily metrics, 5m records)

Outputs:
  data/raw/binance_usdm/klines/symbol=X/interval=Y/year=YYYY/month=MM/X-Y-YYYY-MM.zip
  data/raw/binance_usdm/metrics/symbol=X/year=YYYY/month=MM/X-metrics-YYYY-MM-DD.zip
  data/normalized/klines/symbol=X/interval=Y/year=YYYY/month=MM/part-0000.parquet
  data/normalized/metrics/symbol=X/granularity=5m/year=YYYY/month=MM/part-0000.parquet
  data/manifests/<dataset_version>.manifest.json (six new manifests)

Idempotent. If a raw ZIP already exists with valid SHA256, the download is
skipped. If a parquet partition already exists, it is regenerated from raw ZIP.
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, date, datetime, timedelta
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
NORMALIZED_METRICS_ROOT = REPO_ROOT / "data" / "normalized" / "metrics"
MANIFESTS_ROOT = REPO_ROOT / "data" / "manifests"

BASE_URL = "https://data.binance.vision"
USER_AGENT = "Prometheus-Research/0.0.0 (+Phase4i/v2-acquisition)"

PIPELINE_VERSION = "prometheus@0.0.0"
GENERATOR = "scripts.phase4i_v2_acquisition"

# Phase 4h coverage requirement: 2022-01-01 .. 2026-03-31 UTC.
SYMBOLS = ("BTCUSDT", "ETHUSDT")
START_DATE = date(2022, 1, 1)
END_DATE = date(2026, 3, 31)

INTERVAL_MS = {
    "30m": 30 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
    "5m": 5 * 60 * 1000,
}

# Phase 4h coverage gates.
COVERAGE_FIRST_OPEN_MS = 1640995200000  # 2022-01-01 00:00 UTC
# Last bar `open_time` requirements per interval:
#   2026-03-31 23:30 UTC for 30m  = 1774999800000
#   2026-03-31 20:00 UTC for 4h   = 1774987200000
#   2026-03-31 23:55 UTC for 5m   = 1775001300000
COVERAGE_LAST_OPEN_MS = {
    "30m": 1774999800000,
    "4h": 1774987200000,
    "5m": 1775001300000,
}

# Concurrency / pacing.
DEFAULT_WORKERS = 8
PACE_MS = 50
MAX_RETRIES = 5
BACKOFF_START_S = 1.0
BACKOFF_CAP_S = 30.0

KLINE_COLUMNS_EXPECTED = 12
METRICS_COLUMNS_EXPECTED = 8


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


class AcquisitionError(Exception):
    """Raised on non-recoverable acquisition or validation problem."""


class MissingArchiveError(AcquisitionError):
    """Raised when an expected public archive returns 404."""


def http_get(client: httpx.Client, url: str) -> bytes:
    """GET with retry/backoff. Public endpoints only. No credentials."""
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
    raise AcquisitionError(f"GET failed after {MAX_RETRIES} attempts: {url} ({last_exc})")


def parse_checksum(text: str, expected_filename: str) -> str:
    line = text.strip()
    if "  " not in line:
        raise AcquisitionError(f"checksum missing two-space separator: {line!r}")
    sha, _, fname = line.partition("  ")
    if len(sha) != 64 or not all(c in "0123456789abcdef" for c in sha):
        raise AcquisitionError(f"checksum sha malformed: {sha!r}")
    if fname != expected_filename:
        raise AcquisitionError(f"checksum filename mismatch: {fname!r} != {expected_filename!r}")
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


def iter_months() -> list[tuple[int, int]]:
    months: list[tuple[int, int]] = []
    y, m = START_DATE.year, START_DATE.month
    while (y, m) <= (END_DATE.year, END_DATE.month):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months


def iter_days() -> list[date]:
    days: list[date] = []
    d = START_DATE
    while d <= END_DATE:
        days.append(d)
        d += timedelta(days=1)
    return days


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


def metrics_raw_path(symbol: str, d: date) -> Path:
    fname = f"{symbol}-metrics-{d.isoformat()}.zip"
    return (
        RAW_ROOT
        / "metrics"
        / f"symbol={symbol}"
        / f"year={d.year:04d}"
        / f"month={d.month:02d}"
        / fname
    )


def metrics_parquet_path(symbol: str, year: int, month: int) -> Path:
    return (
        NORMALIZED_METRICS_ROOT
        / f"symbol={symbol}"
        / "granularity=5m"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / "part-0000.parquet"
    )


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


# Kline schema follows Binance bulk CSV column naming as preserved by the
# Phase 4i brief: open_time, open, high, low, close, volume, close_time,
# quote_asset_volume, count, taker_buy_volume, taker_buy_quote_asset_volume,
# ignore, plus symbol+interval+source.
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

METRICS_SCHEMA = pa.schema(
    [
        pa.field("symbol", pa.string(), nullable=False),
        pa.field("create_time", pa.int64(), nullable=False),
        pa.field("sum_open_interest", pa.float64(), nullable=False),
        pa.field("sum_open_interest_value", pa.float64(), nullable=False),
        pa.field("count_toptrader_long_short_ratio", pa.float64(), nullable=False),
        pa.field("sum_toptrader_long_short_ratio", pa.float64(), nullable=False),
        pa.field("count_long_short_ratio", pa.float64(), nullable=False),
        pa.field("sum_taker_long_short_vol_ratio", pa.float64(), nullable=False),
        pa.field("source", pa.string(), nullable=False),
    ]
)


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


def parse_kline_zip(zip_path: Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if len(names) != 1:
            raise AcquisitionError(f"expected one CSV in {zip_path}, got {names}")
        with zf.open(names[0]) as fh:
            text = io.TextIOWrapper(fh, encoding="utf-8", newline="")
            rows: list[dict[str, Any]] = []
            seen_first = False
            for index, raw in enumerate(text, start=1):
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


def _parse_create_time(raw: str) -> int:
    """Binance metrics CSVs may emit create_time as either an integer
    millisecond timestamp or an ISO-like 'YYYY-MM-DD HH:MM:SS' string. Accept
    either; always return UTC ms."""
    s = raw.strip()
    if s.isdigit():
        return int(s)
    # Try common datetime formats.
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.strptime(s, fmt).replace(tzinfo=UTC)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    raise AcquisitionError(f"unrecognized create_time format: {raw!r}")


def _parse_metrics_float(raw: str) -> float:
    """Binance metrics CSVs can emit numeric fields as empty `""` quoted
    strings (or bare empty) when an upstream collector had no data for that
    5-minute window. Treat those as NaN; the integrity check then counts them
    via `nonfinite_violations` and fails closed without silently substituting
    a zero or forward-fill."""
    s = raw.strip().strip('"')
    if not s:
        return float("nan")
    return float(s)


def parse_metrics_zip(zip_path: Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if len(names) != 1:
            raise AcquisitionError(f"expected one CSV in {zip_path}, got {names}")
        with zf.open(names[0]) as fh:
            text = io.TextIOWrapper(fh, encoding="utf-8", newline="")
            rows: list[dict[str, Any]] = []
            seen_first = False
            for index, raw in enumerate(text, start=1):
                line = raw.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != METRICS_COLUMNS_EXPECTED:
                    raise AcquisitionError(
                        f"{zip_path} line {index}: expected "
                        f"{METRICS_COLUMNS_EXPECTED} cols, got {len(parts)}"
                    )
                if not seen_first:
                    seen_first = True
                    if parts[0].strip().lower() == "create_time":
                        continue
                try:
                    rows.append(
                        {
                            "create_time": _parse_create_time(parts[0]),
                            "symbol": parts[1].strip().strip('"'),
                            "sum_open_interest": _parse_metrics_float(parts[2]),
                            "sum_open_interest_value": _parse_metrics_float(parts[3]),
                            "count_toptrader_long_short_ratio": _parse_metrics_float(parts[4]),
                            "sum_toptrader_long_short_ratio": _parse_metrics_float(parts[5]),
                            "count_long_short_ratio": _parse_metrics_float(parts[6]),
                            "sum_taker_long_short_vol_ratio": _parse_metrics_float(parts[7]),
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


def write_klines_parquet(
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


def write_metrics_parquet(
    rows: list[dict[str, Any]], symbol: str, source_url: str, dest: Path
) -> None:
    n = len(rows)
    table = pa.table(
        {
            "symbol": pa.array([symbol] * n, type=pa.string()),
            "create_time": pa.array([r["create_time"] for r in rows], type=pa.int64()),
            "sum_open_interest": pa.array(
                [r["sum_open_interest"] for r in rows], type=pa.float64()
            ),
            "sum_open_interest_value": pa.array(
                [r["sum_open_interest_value"] for r in rows], type=pa.float64()
            ),
            "count_toptrader_long_short_ratio": pa.array(
                [r["count_toptrader_long_short_ratio"] for r in rows], type=pa.float64()
            ),
            "sum_toptrader_long_short_ratio": pa.array(
                [r["sum_toptrader_long_short_ratio"] for r in rows], type=pa.float64()
            ),
            "count_long_short_ratio": pa.array(
                [r["count_long_short_ratio"] for r in rows], type=pa.float64()
            ),
            "sum_taker_long_short_vol_ratio": pa.array(
                [r["sum_taker_long_short_vol_ratio"] for r in rows], type=pa.float64()
            ),
            "source": pa.array([source_url] * n, type=pa.string()),
        },
        schema=METRICS_SCHEMA,
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
    """Idempotently download + SHA256-verify a single bulk archive."""
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
            # Fall through to re-download.
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
class KlineMonthRecord:
    symbol: str
    interval: str
    year: int
    month: int
    url: str
    sha256: str
    raw_path: Path
    parquet_path: Path
    row_count: int


@dataclasses.dataclass
class MetricsDayRecord:
    symbol: str
    day: date
    url: str
    sha256: str
    raw_path: Path
    row_count: int


@dataclasses.dataclass
class MetricsMonthRecord:
    """Aggregated per-month metrics partition produced by combining the month's
    daily archive records into one Parquet file."""

    symbol: str
    year: int
    month: int
    parquet_path: Path
    row_count: int
    daily_records: list[MetricsDayRecord]


def acquire_klines_family(
    client: httpx.Client, symbol: str, interval: str, workers: int
) -> list[KlineMonthRecord]:
    months = iter_months()
    raws: dict[tuple[int, int], ArchiveResult] = {}

    def _job(year: int, month: int) -> tuple[int, int, ArchiveResult]:
        fname = f"{symbol}-{interval}-{year:04d}-{month:02d}.zip"
        url = (
            f"{BASE_URL}/data/futures/um/monthly/klines/{symbol}/{interval}/{fname}"
        )
        rp = kline_raw_path(symbol, interval, year, month)
        return year, month, acquire_archive(client, url, rp, fname)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_job, y, m) for (y, m) in months]
        for completed, fut in enumerate(as_completed(futures), start=1):
            year, month, res = fut.result()
            raws[(year, month)] = res
            if completed % 10 == 0 or completed == len(months):
                _log(
                    f"  klines {symbol} {interval}: {completed}/{len(months)} "
                    f"latest={year:04d}-{month:02d}"
                )

    records: list[KlineMonthRecord] = []
    for (year, month) in months:
        res = raws[(year, month)]
        rows = parse_kline_zip(res.raw_path)
        if not rows:
            raise AcquisitionError(f"empty rows from {res.raw_path}")
        pp = kline_parquet_path(symbol, interval, year, month)
        write_klines_parquet(rows, symbol, interval, res.url, pp)
        records.append(
            KlineMonthRecord(
                symbol=symbol,
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
    return records


def acquire_metrics_family(
    client: httpx.Client, symbol: str, workers: int
) -> tuple[list[MetricsDayRecord], list[date]]:
    days = iter_days()
    raws: dict[date, ArchiveResult] = {}
    missing: list[date] = []

    def _job(d: date) -> tuple[date, ArchiveResult | None]:
        fname = f"{symbol}-metrics-{d.isoformat()}.zip"
        url = f"{BASE_URL}/data/futures/um/daily/metrics/{symbol}/{fname}"
        rp = metrics_raw_path(symbol, d)
        try:
            return d, acquire_archive(client, url, rp, fname)
        except MissingArchiveError:
            return d, None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_job, d) for d in days]
        for completed, fut in enumerate(as_completed(futures), start=1):
            d, res = fut.result()
            if res is None:
                missing.append(d)
            else:
                raws[d] = res
            if completed % 100 == 0 or completed == len(days):
                _log(
                    f"  metrics {symbol}: {completed}/{len(days)} "
                    f"missing_so_far={len(missing)}"
                )

    records: list[MetricsDayRecord] = []
    for d in days:
        if d not in raws:
            continue
        res = raws[d]
        rows = parse_metrics_zip(res.raw_path)
        if not rows:
            raise AcquisitionError(f"empty rows from {res.raw_path}")
        records.append(
            MetricsDayRecord(
                symbol=symbol,
                day=d,
                url=res.url,
                sha256=res.sha256,
                raw_path=res.raw_path,
                row_count=len(rows),
            )
        )
    return records, sorted(missing)


def normalize_metrics_to_monthly(
    symbol: str, day_records: list[MetricsDayRecord]
) -> list[MetricsMonthRecord]:
    """Combine the daily metrics records into per-month parquet partitions.
    All days that fall in the same calendar month are concatenated and sorted
    by create_time."""
    by_month: dict[tuple[int, int], list[MetricsDayRecord]] = {}
    for rec in day_records:
        key = (rec.day.year, rec.day.month)
        by_month.setdefault(key, []).append(rec)

    out: list[MetricsMonthRecord] = []
    for (year, month), recs in sorted(by_month.items()):
        recs_sorted = sorted(recs, key=lambda r: r.day)
        all_rows: list[dict[str, Any]] = []
        # Combine all days into one month-Parquet, in chronological day order.
        for r in recs_sorted:
            all_rows.extend(parse_metrics_zip(r.raw_path))
        all_rows.sort(key=lambda x: x["create_time"])
        pp = metrics_parquet_path(symbol, year, month)
        # Source URL on rows: keep the day-level URLs; we record month-level URL
        # set in manifest.sources. For the parquet `source` column we record the
        # day URL each row originated from. To avoid the cost of preserving
        # per-row provenance we use a synthesized month-level marker.
        month_marker = (
            f"{BASE_URL}/data/futures/um/daily/metrics/{symbol}/"
            f"{symbol}-metrics-{year:04d}-{month:02d}-XX.zip"
        )
        write_metrics_parquet(all_rows, symbol, month_marker, pp)
        out.append(
            MetricsMonthRecord(
                symbol=symbol,
                year=year,
                month=month,
                parquet_path=pp,
                row_count=len(all_rows),
                daily_records=recs_sorted,
            )
        )
    return out


# ---------------------------------------------------------------------------
# Integrity checks
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class KlineIntegrityReport:
    bar_count: int
    first_open_time_ms: int
    last_open_time_ms: int
    gaps_detected: int
    gap_locations: list[dict[str, int]]
    monotone_timestamps: bool
    duplicate_timestamps: int
    boundary_alignment_violations: int
    close_time_consistency_violations: int
    ohlc_sanity_violations: int
    volume_sanity_violations: int
    taker_buy_volume_present: bool
    taker_buy_volume_violations: int
    symbol_consistency_violations: int
    interval_consistency_violations: int
    date_range_coverage: bool
    coverage_required_first_open_time_ms: int
    coverage_required_last_open_time_ms: int

    def passes(self) -> bool:
        return (
            self.gaps_detected == 0
            and self.monotone_timestamps
            and self.duplicate_timestamps == 0
            and self.boundary_alignment_violations == 0
            and self.close_time_consistency_violations == 0
            and self.ohlc_sanity_violations == 0
            and self.volume_sanity_violations == 0
            and self.taker_buy_volume_present
            and self.taker_buy_volume_violations == 0
            and self.symbol_consistency_violations == 0
            and self.interval_consistency_violations == 0
            and self.date_range_coverage
        )


def integrity_check_klines(
    symbol: str, interval: str, records: list[KlineMonthRecord]
) -> KlineIntegrityReport:
    if not records:
        raise AcquisitionError(f"no records for klines {symbol} {interval}")

    interval_ms = INTERVAL_MS[interval]
    months_sorted = sorted(records, key=lambda r: (r.year, r.month))
    tables = [pq.ParquetFile(str(r.parquet_path)).read() for r in months_sorted]
    combined = pa.concat_tables(tables)

    open_times = combined.column("open_time").to_pylist()
    close_times = combined.column("close_time").to_pylist()
    syms = combined.column("symbol").to_pylist()
    ivls = combined.column("interval").to_pylist()
    opens = combined.column("open").to_pylist()
    highs = combined.column("high").to_pylist()
    lows = combined.column("low").to_pylist()
    closes = combined.column("close").to_pylist()
    volumes = combined.column("volume").to_pylist()
    qvols = combined.column("quote_asset_volume").to_pylist()
    counts = combined.column("count").to_pylist()
    taker_buy = combined.column("taker_buy_volume").to_pylist()

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
            gaps.append({"prev_open_time_ms": int(prev), "next_open_time_ms": int(curr)})
    gaps_detected = len(gaps)

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

    volume_violations = sum(
        1
        for v, qv, tc in zip(volumes, qvols, counts, strict=True)
        if v < 0 or qv < 0 or tc < 0
    )

    # taker_buy_volume must be present AND <= volume.
    taker_present = all(tb is not None for tb in taker_buy)
    taker_violations = sum(
        1
        for tb, v in zip(taker_buy, volumes, strict=True)
        if tb is None or tb < 0 or tb > v + 1e-9
    )

    sym_violations = sum(1 for s in syms if s != symbol)
    ivl_violations = sum(1 for v in ivls if v != interval)

    first_ot = min(open_times)
    last_ot = max(open_times)
    coverage_ok = (
        first_ot <= COVERAGE_FIRST_OPEN_MS
        and last_ot >= COVERAGE_LAST_OPEN_MS[interval]
    )

    return KlineIntegrityReport(
        bar_count=bar_count,
        first_open_time_ms=int(first_ot),
        last_open_time_ms=int(last_ot),
        gaps_detected=gaps_detected,
        gap_locations=gaps[:50],
        monotone_timestamps=monotone,
        duplicate_timestamps=duplicates,
        boundary_alignment_violations=boundary_violations,
        close_time_consistency_violations=close_violations,
        ohlc_sanity_violations=ohlc_violations,
        volume_sanity_violations=volume_violations,
        taker_buy_volume_present=taker_present,
        taker_buy_volume_violations=taker_violations,
        symbol_consistency_violations=sym_violations,
        interval_consistency_violations=ivl_violations,
        date_range_coverage=coverage_ok,
        coverage_required_first_open_time_ms=COVERAGE_FIRST_OPEN_MS,
        coverage_required_last_open_time_ms=COVERAGE_LAST_OPEN_MS[interval],
    )


@dataclasses.dataclass
class MetricsIntegrityReport:
    record_count: int
    first_create_time_ms: int
    last_create_time_ms: int
    monotone_timestamps: bool
    duplicate_timestamps: int
    boundary_alignment_violations: int
    expected_records: int
    missing_observations: int
    gap_locations: list[dict[str, int]]
    missing_days: list[str]
    symbol_consistency_violations: int
    nonfinite_violations: int
    nonnegative_oi_violations: int
    nonnegative_ratio_violations: int
    date_range_coverage: bool
    coverage_required_first_create_time_ms: int
    coverage_required_last_create_time_ms: int
    invalid_windows: list[dict[str, Any]]

    def passes(self) -> bool:
        return (
            self.monotone_timestamps
            and self.duplicate_timestamps == 0
            and self.boundary_alignment_violations == 0
            and self.missing_observations == 0
            and not self.missing_days
            and self.symbol_consistency_violations == 0
            and self.nonfinite_violations == 0
            and self.nonnegative_oi_violations == 0
            and self.nonnegative_ratio_violations == 0
            and self.date_range_coverage
        )


def integrity_check_metrics(
    symbol: str,
    month_records: list[MetricsMonthRecord],
    missing_days: list[date],
) -> MetricsIntegrityReport:
    if not month_records:
        raise AcquisitionError(f"no metrics records for {symbol}")

    interval_ms = INTERVAL_MS["5m"]
    tables = [pq.ParquetFile(str(r.parquet_path)).read() for r in month_records]
    combined = pa.concat_tables(tables)

    create_times = combined.column("create_time").to_pylist()
    syms = combined.column("symbol").to_pylist()
    sum_oi = combined.column("sum_open_interest").to_pylist()
    sum_oi_value = combined.column("sum_open_interest_value").to_pylist()
    cnt_top = combined.column("count_toptrader_long_short_ratio").to_pylist()
    sum_top = combined.column("sum_toptrader_long_short_ratio").to_pylist()
    cnt_ls = combined.column("count_long_short_ratio").to_pylist()
    sum_taker = combined.column("sum_taker_long_short_vol_ratio").to_pylist()

    record_count = len(create_times)

    boundary_violations = sum(1 for t in create_times if t % interval_ms != 0)
    monotone = True
    duplicates = 0
    gaps: list[dict[str, int]] = []
    for i in range(1, record_count):
        prev = create_times[i - 1]
        curr = create_times[i]
        if curr == prev:
            duplicates += 1
        elif curr < prev:
            monotone = False
        elif curr - prev != interval_ms:
            gaps.append({"prev_create_time_ms": int(prev), "next_create_time_ms": int(curr)})
    missing_observations = len(gaps)

    sym_violations = sum(1 for s in syms if s != symbol)

    nonfinite_violations = 0
    nonneg_oi = 0
    nonneg_ratio = 0
    for oi, oiv, ct, st, cl, str_ in zip(
        sum_oi, sum_oi_value, cnt_top, sum_top, cnt_ls, sum_taker, strict=True
    ):
        for v in (oi, oiv, ct, st, cl, str_):
            if v != v or v in (float("inf"), float("-inf")):  # NaN or Inf
                nonfinite_violations += 1
                break
        if oi < 0 or oiv < 0:
            nonneg_oi += 1
        if ct < 0 or st < 0 or cl < 0 or str_ < 0:
            nonneg_ratio += 1

    first_ct = min(create_times) if create_times else 0
    last_ct = max(create_times) if create_times else 0
    coverage_ok = (
        first_ct <= COVERAGE_FIRST_OPEN_MS
        and last_ct >= COVERAGE_LAST_OPEN_MS["5m"]
        and not missing_days
    )

    expected_records = len(iter_days()) * (24 * 60 // 5)

    invalid_windows = [
        {
            "start_create_time_ms": g["prev_create_time_ms"] + interval_ms,
            "end_create_time_ms": g["next_create_time_ms"] - interval_ms,
            "reason": "upstream_data.binance.vision_metrics_archive_gap",
        }
        for g in gaps
    ]
    for d in missing_days:
        start_ms = int(
            datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp() * 1000
        )
        end_ms = start_ms + (24 * 60 * 60 * 1000) - interval_ms
        invalid_windows.append(
            {
                "start_create_time_ms": start_ms,
                "end_create_time_ms": end_ms,
                "reason": "missing_daily_metrics_archive",
            }
        )

    return MetricsIntegrityReport(
        record_count=record_count,
        first_create_time_ms=int(first_ct),
        last_create_time_ms=int(last_ct),
        monotone_timestamps=monotone,
        duplicate_timestamps=duplicates,
        boundary_alignment_violations=boundary_violations,
        expected_records=expected_records,
        missing_observations=missing_observations,
        gap_locations=gaps[:50],
        missing_days=[d.isoformat() for d in missing_days],
        symbol_consistency_violations=sym_violations,
        nonfinite_violations=nonfinite_violations,
        nonnegative_oi_violations=nonneg_oi,
        nonnegative_ratio_violations=nonneg_ratio,
        date_range_coverage=coverage_ok,
        coverage_required_first_create_time_ms=COVERAGE_FIRST_OPEN_MS,
        coverage_required_last_create_time_ms=COVERAGE_LAST_OPEN_MS["5m"],
        invalid_windows=invalid_windows[:200],
    )


# ---------------------------------------------------------------------------
# Manifests
# ---------------------------------------------------------------------------


def _command_used() -> str:
    return " ".join(sys.argv)


def write_kline_manifest(
    *,
    symbol: str,
    interval: str,
    records: list[KlineMonthRecord],
    integrity: KlineIntegrityReport,
) -> Path:
    sym_lower = symbol.lower()
    dataset_name = f"binance_usdm_{sym_lower}_{interval}"
    dataset_version = f"{dataset_name}__v001"
    sources = sorted(r.url for r in records)
    raw_sha256_index = {r.raw_path.name: r.sha256 for r in records}
    months = sorted({(r.year, r.month) for r in records})

    invalid_windows = [
        {
            "start_open_time_ms": g["prev_open_time_ms"] + INTERVAL_MS[interval],
            "end_open_time_ms": g["next_open_time_ms"] - INTERVAL_MS[interval],
            "reason": "upstream_data.binance.vision_kline_archive_gap",
        }
        for g in integrity.gap_locations
    ]

    predecessor = (
        f"binance_usdm_{sym_lower}_15m__v002"
        if interval == "30m"
        else f"binance_usdm_{sym_lower}_1h_derived__v002"
    )

    manifest = {
        "schema_version": "kline_v1",
        "dataset_category": "normalized_kline",
        "dataset_name": dataset_name,
        "dataset_version": dataset_version,
        "created_at_utc_ms": int(time.time() * 1000),
        "canonical_timezone": "UTC",
        "canonical_timestamp_format": "unix_milliseconds",
        "symbols": [symbol],
        "market": "binance_usdm",
        "instrument_type": "perpetual_futures",
        "intervals": [interval],
        "sources": sources,
        "pipeline_version": PIPELINE_VERSION,
        "partitioning": ["symbol", "interval", "year", "month"],
        "primary_key": ["symbol", "interval", "open_time"],
        "generator": GENERATOR,
        "predecessor_dataset_versions": [predecessor],
        "invalid_windows": invalid_windows,
        "notes": (
            f"Phase 4i V2 acquisition: {interval} trade-price klines. "
            f"Months: {months[0][0]:04d}-{months[0][1]:02d} to "
            f"{months[-1][0]:04d}-{months[-1][1]:02d}. "
            "Public unauthenticated data.binance.vision bulk archive only."
        ),
        "date_range_start_open_time_utc_ms": integrity.first_open_time_ms,
        "date_range_end_open_time_utc_ms": integrity.last_open_time_ms,
        "bar_count": integrity.bar_count,
        "raw_archive_count": len(records),
        "raw_sha256_index": raw_sha256_index,
        "quality_checks": {
            "monotone_timestamps": integrity.monotone_timestamps,
            "duplicate_timestamps": integrity.duplicate_timestamps,
            "boundary_alignment_violations": integrity.boundary_alignment_violations,
            "close_time_consistency_violations": integrity.close_time_consistency_violations,
            "gaps_detected": integrity.gaps_detected,
            "gap_locations": integrity.gap_locations,
            "ohlc_sanity_violations": integrity.ohlc_sanity_violations,
            "volume_sanity_violations": integrity.volume_sanity_violations,
            "taker_buy_volume_present": integrity.taker_buy_volume_present,
            "taker_buy_volume_violations": integrity.taker_buy_volume_violations,
            "symbol_consistency_violations": integrity.symbol_consistency_violations,
            "interval_consistency_violations": integrity.interval_consistency_violations,
            "date_range_coverage": integrity.date_range_coverage,
            "coverage_required_first_open_time_ms": (
                integrity.coverage_required_first_open_time_ms
            ),
            "coverage_required_last_open_time_ms": (
                integrity.coverage_required_last_open_time_ms
            ),
            "research_eligible": integrity.passes(),
        },
        "research_eligible": integrity.passes(),
        "command_used": _command_used(),
        "no_credentials_confirmation": True,
        "private_endpoint_used": False,
    }
    path = MANIFESTS_ROOT / f"{dataset_version}.manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


def write_metrics_manifest(
    *,
    symbol: str,
    day_records: list[MetricsDayRecord],
    integrity: MetricsIntegrityReport,
) -> Path:
    sym_lower = symbol.lower()
    dataset_name = f"binance_usdm_{sym_lower}_metrics"
    dataset_version = f"{dataset_name}__v001"
    sources = sorted(r.url for r in day_records)
    raw_sha256_index = {r.raw_path.name: r.sha256 for r in day_records}

    manifest = {
        "schema_version": "metrics_v1",
        "dataset_category": "metrics_record",
        "dataset_name": dataset_name,
        "dataset_version": dataset_version,
        "created_at_utc_ms": int(time.time() * 1000),
        "canonical_timezone": "UTC",
        "canonical_timestamp_format": "unix_milliseconds",
        "symbols": [symbol],
        "market": "binance_usdm",
        "instrument_type": "perpetual_futures",
        "intervals": ["5m"],
        "granularity": "5m",
        "sources": sources,
        "pipeline_version": PIPELINE_VERSION,
        "partitioning": ["symbol", "granularity", "year", "month"],
        "primary_key": ["symbol", "create_time"],
        "generator": GENERATOR,
        "predecessor_dataset_versions": [],
        "invalid_windows": integrity.invalid_windows,
        "notes": (
            "Phase 4i V2 acquisition: per-symbol metrics (open interest + "
            "long/short ratio + taker buy/sell volume ratio) at 5-minute "
            "granularity, sourced from data.binance.vision daily archives. "
            "Public unauthenticated bulk archive only. Each row is one 5-minute "
            "snapshot."
        ),
        "date_range_start_create_time_utc_ms": integrity.first_create_time_ms,
        "date_range_end_create_time_utc_ms": integrity.last_create_time_ms,
        "record_count": integrity.record_count,
        "expected_records": integrity.expected_records,
        "raw_archive_count": len(day_records),
        "raw_sha256_index": raw_sha256_index,
        "quality_checks": {
            "monotone_timestamps": integrity.monotone_timestamps,
            "duplicate_timestamps": integrity.duplicate_timestamps,
            "boundary_alignment_violations": integrity.boundary_alignment_violations,
            "missing_observations": integrity.missing_observations,
            "missing_days": integrity.missing_days,
            "gap_locations": integrity.gap_locations,
            "symbol_consistency_violations": integrity.symbol_consistency_violations,
            "nonfinite_violations": integrity.nonfinite_violations,
            "nonnegative_oi_violations": integrity.nonnegative_oi_violations,
            "nonnegative_ratio_violations": integrity.nonnegative_ratio_violations,
            "date_range_coverage": integrity.date_range_coverage,
            "coverage_required_first_create_time_ms": (
                integrity.coverage_required_first_create_time_ms
            ),
            "coverage_required_last_create_time_ms": (
                integrity.coverage_required_last_create_time_ms
            ),
            "research_eligible": integrity.passes(),
        },
        "research_eligible": integrity.passes(),
        "command_used": _command_used(),
        "no_credentials_confirmation": True,
        "private_endpoint_used": False,
    }
    path = MANIFESTS_ROOT / f"{dataset_version}.manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 4i V2 acquisition")
    p.add_argument("--start", default=START_DATE.strftime("%Y-%m"))
    p.add_argument("--end", default=END_DATE.strftime("%Y-%m"))
    p.add_argument("--symbols", nargs="+", default=list(SYMBOLS))
    p.add_argument(
        "--families",
        nargs="+",
        default=["klines_30m", "klines_4h", "metrics"],
        choices=["klines_30m", "klines_4h", "metrics"],
    )
    p.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    p.add_argument(
        "--limit-days",
        type=int,
        default=0,
        help="If > 0, limit metrics-family acquisition to first N days for testing.",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    # Validate symbols.
    for s in args.symbols:
        if s not in SYMBOLS:
            raise AcquisitionError(f"unsupported symbol: {s}")

    # Override iteration if test slice requested.
    global START_DATE, END_DATE
    sy, sm = (int(p) for p in args.start.split("-"))
    ey, em = (int(p) for p in args.end.split("-"))
    START_DATE = date(sy, sm, 1)
    last_day_of_end = (date(ey + (em // 12), (em % 12) + 1, 1) - timedelta(days=1))
    END_DATE = last_day_of_end

    headers = {"User-Agent": USER_AGENT}
    klines_results: dict[tuple[str, str], list[KlineMonthRecord]] = {}
    metrics_day_results: dict[str, list[MetricsDayRecord]] = {}
    metrics_missing: dict[str, list[date]] = {}
    metrics_month_results: dict[str, list[MetricsMonthRecord]] = {}

    with httpx.Client(headers=headers) as client:
        for family in args.families:
            for symbol in args.symbols:
                if family == "klines_30m":
                    _log(f"acquire klines 30m {symbol} ...")
                    recs = acquire_klines_family(client, symbol, "30m", args.workers)
                    klines_results[(symbol, "30m")] = recs
                elif family == "klines_4h":
                    _log(f"acquire klines 4h {symbol} ...")
                    recs = acquire_klines_family(client, symbol, "4h", args.workers)
                    klines_results[(symbol, "4h")] = recs
                elif family == "metrics":
                    _log(f"acquire metrics {symbol} ...")
                    days, missing = acquire_metrics_family(
                        client, symbol, args.workers
                    )
                    metrics_day_results[symbol] = days
                    metrics_missing[symbol] = missing
                else:
                    raise AcquisitionError(f"unknown family: {family}")

    # Normalize metrics into per-month parquet partitions.
    for symbol, day_records in metrics_day_results.items():
        if not day_records:
            continue
        _log(f"normalize metrics {symbol} -> per-month parquet ...")
        metrics_month_results[symbol] = normalize_metrics_to_monthly(
            symbol, day_records
        )

    # Integrity + manifests.
    failed: list[str] = []
    manifest_paths: list[Path] = []

    for (symbol, interval), recs in sorted(klines_results.items()):
        report = integrity_check_klines(symbol, interval, recs)
        mp = write_kline_manifest(
            symbol=symbol, interval=interval, records=recs, integrity=report
        )
        manifest_paths.append(mp)
        _log(
            f"manifest {mp.name}: bars={report.bar_count} "
            f"gaps={report.gaps_detected} mono={report.monotone_timestamps} "
            f"coverage={report.date_range_coverage} eligible={report.passes()}"
        )
        if not report.passes():
            failed.append(mp.name)

    for symbol, day_records in sorted(metrics_day_results.items()):
        if symbol not in metrics_month_results:
            continue
        m_report = integrity_check_metrics(
            symbol, metrics_month_results[symbol], metrics_missing[symbol]
        )
        mp = write_metrics_manifest(
            symbol=symbol,
            day_records=day_records,
            integrity=m_report,
        )
        manifest_paths.append(mp)
        _log(
            f"manifest {mp.name}: records={m_report.record_count} "
            f"missing_obs={m_report.missing_observations} "
            f"missing_days={len(m_report.missing_days)} "
            f"mono={m_report.monotone_timestamps} "
            f"coverage={m_report.date_range_coverage} eligible={m_report.passes()}"
        )
        if not m_report.passes():
            failed.append(mp.name)

    if failed:
        _log(f"INTEGRITY FAILURE: {failed}")
        return 1
    _log(
        f"Phase 4i acquisition + integrity validation complete. "
        f"{len(manifest_paths)} manifests written."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
