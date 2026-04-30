"""Phase 3q — 5m supplemental dataset acquisition + integrity validation.

Authority: Phase 3p §4 (data requirements), §5 (versioning approach: supplemental
v001-of-5m alongside v002), §6 (manifest + integrity-check evidence). Phase 3q
brief: docs-and-data, public unauthenticated endpoints only, no credentials, no
exchange-write paths.

This script is a standalone orchestrator. It does NOT modify any existing v002
dataset, v002 manifest, or existing ingest function. It does NOT extend the
Interval enum. It uses only raw httpx + pyarrow + standard library, with the
data.binance.vision URL convention proven by `prometheus.research.data.binance_bulk`
in Phase 2b/2c.

Outputs:
- Raw ZIPs:           data/raw/binance_usdm/<klines|markPriceKlines>/symbol=X/interval=5m/year=Y/month=M/X-5m-Y-M.zip
- Normalized parquet: data/normalized/<klines|mark_price_klines>/symbol=X/interval=5m/year=Y/month=M/part-0000.parquet
- Manifests:          data/manifests/<dataset_version>.manifest.json (4 new manifests)

Idempotent. If a raw ZIP already exists with valid SHA256, the download is
skipped. If a parquet partition already exists, it is regenerated from raw ZIP.

Phase 3q runs Phase 3p §4.7 / §6.2 integrity checks across all data and embeds
the results in each manifest's quality_checks field. Any check failure
classifies the dataset as not research-eligible and the orchestrator stops.
"""

from __future__ import annotations

import dataclasses
import hashlib
import io
import json
import sys
import time
import zipfile
from datetime import datetime, timezone
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
NORMALIZED_MARKPRICE_ROOT = REPO_ROOT / "data" / "normalized" / "mark_price_klines"
MANIFESTS_ROOT = REPO_ROOT / "data" / "manifests"

BASE_URL = "https://data.binance.vision"
USER_AGENT = "Prometheus-Research/0.0.0 (+Phase3q/5m-acquisition)"

INTERVAL = "5m"
INTERVAL_MS = 5 * 60 * 1000

# Phase 3p §4 required scope.
SYMBOLS = ("BTCUSDT", "ETHUSDT")
START_YEAR, START_MONTH = 2022, 1
END_YEAR, END_MONTH = 2026, 3  # Strict superset of trade range 2022-01..2026-02 plus margin.

# Family identifiers (data.binance.vision URL prefix; local raw subdir).
FAMILIES: dict[str, dict[str, Any]] = {
    "klines": {
        "url_prefix": "data/futures/um/monthly/klines",
        "raw_subdir": "klines",
        "normalized_root": NORMALIZED_KLINES_ROOT,
        "manifest_dataset_category": "normalized_kline",
        "manifest_schema_version": "kline_v1",
    },
    "markPriceKlines": {
        "url_prefix": "data/futures/um/monthly/markPriceKlines",
        "raw_subdir": "markPriceKlines",
        "normalized_root": NORMALIZED_MARKPRICE_ROOT,
        "manifest_dataset_category": "mark_price_kline",
        "manifest_schema_version": "mark_price_kline_v1",
    },
}

PIPELINE_VERSION = "prometheus@0.0.0"
GENERATOR = "scripts.phase3q_5m_acquisition"

PACE_MS = 100  # Conservative pacing between requests.
MAX_RETRIES = 5
BACKOFF_START_S = 1.0
BACKOFF_CAP_S = 30.0


# ---------------------------------------------------------------------------
# HTTP helpers (public, unauthenticated only)
# ---------------------------------------------------------------------------

class AcquisitionError(Exception):
    """Raised on any non-recoverable acquisition or validation problem."""


def http_get(client: httpx.Client, url: str) -> bytes:
    """GET with retry/backoff. Public endpoints only. No credentials."""
    last_exc: Exception | None = None
    delay = BACKOFF_START_S
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = client.get(url, follow_redirects=True, timeout=60)
            if resp.status_code == 200:
                return resp.content
            if resp.status_code == 404:
                raise AcquisitionError(f"404 for {url}")
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


# ---------------------------------------------------------------------------
# Month iteration
# ---------------------------------------------------------------------------

def iter_months() -> list[tuple[int, int]]:
    months: list[tuple[int, int]] = []
    y, m = START_YEAR, START_MONTH
    while (y, m) <= (END_YEAR, END_MONTH):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months


# ---------------------------------------------------------------------------
# Per-month acquisition
# ---------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class MonthRecord:
    family: str
    symbol: str
    year: int
    month: int
    url: str
    sha256: str
    row_count: int
    raw_path: Path
    parquet_path: Path
    first_open_time_ms: int
    last_open_time_ms: int


def raw_path(family: str, symbol: str, year: int, month: int) -> Path:
    fam = FAMILIES[family]
    fname = f"{symbol}-{INTERVAL}-{year:04d}-{month:02d}.zip"
    return (
        RAW_ROOT
        / fam["raw_subdir"]
        / f"symbol={symbol}"
        / f"interval={INTERVAL}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / fname
    )


def parquet_path(family: str, symbol: str, year: int, month: int) -> Path:
    fam = FAMILIES[family]
    return (
        fam["normalized_root"]
        / f"symbol={symbol}"
        / f"interval={INTERVAL}"
        / f"year={year:04d}"
        / f"month={month:02d}"
        / "part-0000.parquet"
    )


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


KLINE_COLUMNS_EXPECTED = 12  # Binance bulk CSV column count


def parse_kline_zip(zip_path: Path) -> list[dict[str, Any]]:
    """Parse a Binance bulk klines ZIP. Returns rows with int / float fields.

    Schema is the v002 trade-price kline schema (12 columns):
      open_time, open, high, low, close, volume, close_time, quote_asset_volume,
      trade_count, taker_buy_base_volume, taker_buy_quote_volume, ignore.
    """
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
                        f"{zip_path} line {index}: expected {KLINE_COLUMNS_EXPECTED} cols, got {len(parts)}"
                    )
                if not seen_first:
                    seen_first = True
                    if parts[0].strip().lower() == "open_time":
                        continue  # header row
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
                            "trade_count": int(parts[8]),
                            "taker_buy_base_volume": float(parts[9]),
                            "taker_buy_quote_volume": float(parts[10]),
                        }
                    )
                except ValueError as exc:
                    raise AcquisitionError(
                        f"{zip_path} line {index}: bad numeric ({exc})"
                    ) from exc
    return rows


def parse_markprice_zip(zip_path: Path) -> list[dict[str, Any]]:
    """Parse a Binance bulk markPriceKlines ZIP.

    Mark-price klines have only OHLC + open_time + close_time + ignore (no
    volume / trade_count / taker_buy fields). Binance bulk markPriceKlines CSVs
    are 12 columns with zeros / placeholders in the volume positions; we keep
    only the price-and-time columns.
    """
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
                        f"{zip_path} line {index}: expected {KLINE_COLUMNS_EXPECTED} cols, got {len(parts)}"
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
        pa.field("trade_count", pa.int64(), nullable=False),
        pa.field("taker_buy_base_volume", pa.float64(), nullable=False),
        pa.field("taker_buy_quote_volume", pa.float64(), nullable=False),
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


def write_klines_parquet(
    rows: list[dict[str, Any]], symbol: str, source_url: str, dest: Path
) -> None:
    n = len(rows)
    table = pa.table(
        {
            "symbol": pa.array([symbol] * n, type=pa.string()),
            "interval": pa.array([INTERVAL] * n, type=pa.string()),
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
            "trade_count": pa.array([r["trade_count"] for r in rows], type=pa.int64()),
            "taker_buy_base_volume": pa.array(
                [r["taker_buy_base_volume"] for r in rows], type=pa.float64()
            ),
            "taker_buy_quote_volume": pa.array(
                [r["taker_buy_quote_volume"] for r in rows], type=pa.float64()
            ),
            "source": pa.array([source_url] * n, type=pa.string()),
        },
        schema=KLINES_SCHEMA,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, dest, compression="zstd", compression_level=3)


def write_markprice_parquet(
    rows: list[dict[str, Any]], symbol: str, source_url: str, dest: Path
) -> None:
    n = len(rows)
    table = pa.table(
        {
            "symbol": pa.array([symbol] * n, type=pa.string()),
            "interval": pa.array([INTERVAL] * n, type=pa.string()),
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


# ---------------------------------------------------------------------------
# Per-month pipeline
# ---------------------------------------------------------------------------

def acquire_one_month(
    client: httpx.Client, family: str, symbol: str, year: int, month: int
) -> MonthRecord:
    fam = FAMILIES[family]
    fname = f"{symbol}-{INTERVAL}-{year:04d}-{month:02d}.zip"
    url = f"{BASE_URL}/{fam['url_prefix']}/{symbol}/{INTERVAL}/{fname}"
    checksum_url = url + ".CHECKSUM"

    rp = raw_path(family, symbol, year, month)

    # Step 1: ensure raw ZIP present + sha256 verified.
    if rp.exists():
        try:
            checksum_text = http_get(client, checksum_url).decode("utf-8")
            expected = parse_checksum(checksum_text, fname)
        except AcquisitionError as e:
            raise AcquisitionError(f"checksum fetch failed for {url}: {e}") from e
        actual = file_sha256(rp)
        if actual != expected:
            # Stale or corrupt: re-download.
            rp.unlink()
        else:
            sha = expected
    if not rp.exists():
        time.sleep(PACE_MS / 1000)
        zip_bytes = http_get(client, url)
        time.sleep(PACE_MS / 1000)
        checksum_text = http_get(client, checksum_url).decode("utf-8")
        expected = parse_checksum(checksum_text, fname)
        actual = hashlib.sha256(zip_bytes).hexdigest()
        if actual != expected:
            raise AcquisitionError(
                f"sha256 mismatch for {url}: expected {expected}, got {actual}"
            )
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_bytes(zip_bytes)
        sha = actual

    # Step 2: parse rows.
    if family == "klines":
        rows = parse_kline_zip(rp)
    else:
        rows = parse_markprice_zip(rp)
    if not rows:
        raise AcquisitionError(f"empty rows from {rp}")

    # Step 3: write parquet.
    pp = parquet_path(family, symbol, year, month)
    if family == "klines":
        write_klines_parquet(rows, symbol, url, pp)
    else:
        write_markprice_parquet(rows, symbol, url, pp)

    return MonthRecord(
        family=family,
        symbol=symbol,
        year=year,
        month=month,
        url=url,
        sha256=sha,
        row_count=len(rows),
        raw_path=rp,
        parquet_path=pp,
        first_open_time_ms=rows[0]["open_time"],
        last_open_time_ms=rows[-1]["open_time"],
    )


# ---------------------------------------------------------------------------
# Integrity checks (Phase 3p §4.7 / §6.2)
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class IntegrityReport:
    bar_count: int
    first_open_time_ms: int
    last_open_time_ms: int
    gaps_detected: int
    gap_locations: list[dict[str, int]]
    monotone_timestamps: bool
    boundary_alignment_violations: int
    close_time_consistency_violations: int
    ohlc_sanity_violations: int
    volume_sanity_violations: int  # 0 by definition for markprice (no volume)
    symbol_consistency_violations: int
    interval_consistency_violations: int
    date_range_coverage: bool
    coverage_required_first_ms: int
    coverage_required_last_ms: int

    def passes(self) -> bool:
        return (
            self.gaps_detected == 0
            and self.monotone_timestamps
            and self.boundary_alignment_violations == 0
            and self.close_time_consistency_violations == 0
            and self.ohlc_sanity_violations == 0
            and self.volume_sanity_violations == 0
            and self.symbol_consistency_violations == 0
            and self.interval_consistency_violations == 0
            and self.date_range_coverage
        )


# Coverage requirement: 5m data must fully cover the v002 trade range.
# Computed from all retained-evidence trade_log.parquet files: signal min
# 1641014100000 (2022-01-01 05:15 UTC), exit max 1770879600000 (2026-02-12 07:00 UTC).
COVERAGE_REQUIRED_FIRST_MS = 1641014100000
COVERAGE_REQUIRED_LAST_MS = 1770879600000


def integrity_check_dataset(
    family: str, symbol: str, records: list[MonthRecord]
) -> IntegrityReport:
    if not records:
        raise AcquisitionError(f"no records for {family} {symbol}")

    # Re-read parquet partitions, concatenated in time order.
    # Use ParquetFile to avoid Hive-partition column inference from the
    # surrounding directory tree (symbol=, interval=, year=, month=).
    months_sorted = sorted(records, key=lambda r: (r.year, r.month))
    tables = []
    for r in months_sorted:
        tables.append(pq.ParquetFile(str(r.parquet_path)).read())
    combined = pa.concat_tables(tables)
    open_times = combined.column("open_time").to_pylist()
    close_times = combined.column("close_time").to_pylist()
    syms = combined.column("symbol").to_pylist()
    ivls = combined.column("interval").to_pylist()
    opens = combined.column("open").to_pylist()
    highs = combined.column("high").to_pylist()
    lows = combined.column("low").to_pylist()
    closes = combined.column("close").to_pylist()
    if family == "klines":
        volumes = combined.column("volume").to_pylist()
        qvols = combined.column("quote_asset_volume").to_pylist()
        tcounts = combined.column("trade_count").to_pylist()
    else:
        volumes = qvols = tcounts = None

    bar_count = len(open_times)

    # Boundary alignment
    boundary_violations = sum(1 for ot in open_times if ot % INTERVAL_MS != 0)
    # Close time consistency
    close_violations = sum(
        1 for ot, ct in zip(open_times, close_times) if ct != ot + INTERVAL_MS - 1
    )
    # Monotone & gaps
    monotone = True
    gaps: list[dict[str, int]] = []
    for i in range(1, bar_count):
        prev = open_times[i - 1]
        curr = open_times[i]
        if curr <= prev:
            monotone = False
        elif curr - prev != INTERVAL_MS:
            gaps.append(
                {"prev_open_time_ms": int(prev), "next_open_time_ms": int(curr)}
            )
    gaps_detected = len(gaps)

    # OHLC sanity
    ohlc_violations = 0
    for o, h, l, c in zip(opens, highs, lows, closes):
        if not (l > 0 and h > 0 and o > 0 and c > 0):
            ohlc_violations += 1
            continue
        if not (l <= o <= h):
            ohlc_violations += 1
            continue
        if not (l <= c <= h):
            ohlc_violations += 1
            continue

    # Volume sanity
    volume_violations = 0
    if family == "klines":
        for v, qv, tc in zip(volumes, qvols, tcounts):
            if v < 0 or qv < 0 or tc < 0:
                volume_violations += 1

    # Symbol / interval consistency
    sym_violations = sum(1 for s in syms if s != symbol)
    ivl_violations = sum(1 for v in ivls if v != INTERVAL)

    # Date range coverage (Phase 3p §4.3 strict superset).
    first_ot = min(open_times)
    last_ot = max(open_times)
    coverage_ok = first_ot <= COVERAGE_REQUIRED_FIRST_MS and last_ot >= COVERAGE_REQUIRED_LAST_MS

    return IntegrityReport(
        bar_count=bar_count,
        first_open_time_ms=int(first_ot),
        last_open_time_ms=int(last_ot),
        gaps_detected=gaps_detected,
        gap_locations=gaps[:50],  # cap stored gap locations
        monotone_timestamps=monotone,
        boundary_alignment_violations=boundary_violations,
        close_time_consistency_violations=close_violations,
        ohlc_sanity_violations=ohlc_violations,
        volume_sanity_violations=volume_violations,
        symbol_consistency_violations=sym_violations,
        interval_consistency_violations=ivl_violations,
        date_range_coverage=coverage_ok,
        coverage_required_first_ms=COVERAGE_REQUIRED_FIRST_MS,
        coverage_required_last_ms=COVERAGE_REQUIRED_LAST_MS,
    )


# ---------------------------------------------------------------------------
# Manifests
# ---------------------------------------------------------------------------

def write_manifest(
    *,
    dataset_version: str,
    family: str,
    symbol: str,
    records: list[MonthRecord],
    integrity: IntegrityReport,
    predecessor_versions: list[str],
) -> Path:
    fam = FAMILIES[family]
    dataset_name = dataset_version.rsplit("__v", 1)[0]
    sources = sorted(r.url for r in records)
    months = sorted({(r.year, r.month) for r in records})
    invalid_windows = [
        {
            "start_open_time_ms": g["prev_open_time_ms"] + INTERVAL_MS,
            "end_open_time_ms": g["next_open_time_ms"] - INTERVAL_MS,
            "reason": "upstream_data.binance.vision_archive_gap",
        }
        for g in integrity.gap_locations
    ]
    manifest = {
        "schema_version": fam["manifest_schema_version"],
        "dataset_category": fam["manifest_dataset_category"],
        "dataset_name": dataset_name,
        "dataset_version": dataset_version,
        "created_at_utc_ms": int(time.time() * 1000),
        "canonical_timezone": "UTC",
        "canonical_timestamp_format": "unix_milliseconds",
        "symbols": [symbol],
        "intervals": [INTERVAL],
        "sources": sources,
        "pipeline_version": PIPELINE_VERSION,
        "partitioning": ["symbol", "interval", "year", "month"],
        "primary_key": ["symbol", "interval", "open_time"],
        "generator": GENERATOR,
        "predecessor_dataset_versions": predecessor_versions,
        "invalid_windows": invalid_windows,
        "notes": (
            f"Phase 3q supplemental 5m bulk ingest from data.binance.vision. "
            f"Months: {months[0][0]:04d}-{months[0][1]:02d} to {months[-1][0]:04d}-{months[-1][1]:02d}. "
            f"Phase 3p Option B versioning (supplemental v001-of-5m alongside v002). "
            f"v002 datasets and manifests untouched. Public unauthenticated endpoints only."
        ),
        "date_range_start_open_time_utc_ms": integrity.first_open_time_ms,
        "date_range_end_open_time_utc_ms": integrity.last_open_time_ms,
        "bar_count": integrity.bar_count,
        "quality_checks": {
            "gaps_detected": integrity.gaps_detected,
            "gap_locations": integrity.gap_locations,
            "monotone_timestamps": integrity.monotone_timestamps,
            "boundary_alignment_violations": integrity.boundary_alignment_violations,
            "close_time_consistency_violations": integrity.close_time_consistency_violations,
            "ohlc_sanity_violations": integrity.ohlc_sanity_violations,
            "volume_sanity_violations": integrity.volume_sanity_violations,
            "symbol_consistency_violations": integrity.symbol_consistency_violations,
            "interval_consistency_violations": integrity.interval_consistency_violations,
            "date_range_coverage": integrity.date_range_coverage,
            "coverage_required_first_open_time_ms": integrity.coverage_required_first_ms,
            "coverage_required_last_open_time_ms": integrity.coverage_required_last_ms,
            "research_eligible": integrity.passes(),
        },
    }
    path = MANIFESTS_ROOT / f"{dataset_version}.manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


def dataset_version_for(family: str, symbol: str) -> str:
    sym = symbol.lower()
    if family == "klines":
        return f"binance_usdm_{sym}_5m__v001"
    if family == "markPriceKlines":
        return f"binance_usdm_{sym}_markprice_5m__v001"
    raise ValueError(family)


def predecessor_versions_for(family: str, symbol: str) -> list[str]:
    sym = symbol.lower()
    if family == "klines":
        return [f"binance_usdm_{sym}_15m__v002"]
    if family == "markPriceKlines":
        return [f"binance_usdm_{sym}_markprice_15m__v002"]
    raise ValueError(family)


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------

def main() -> int:
    months = iter_months()
    families = list(FAMILIES.keys())

    all_records: dict[tuple[str, str], list[MonthRecord]] = {
        (f, s): [] for f in families for s in SYMBOLS
    }

    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(headers=headers) as client:
        n_total = len(months) * len(families) * len(SYMBOLS)
        n_done = 0
        for family in families:
            for symbol in SYMBOLS:
                for year, month in months:
                    n_done += 1
                    rec = acquire_one_month(client, family, symbol, year, month)
                    all_records[(family, symbol)].append(rec)
                    if n_done % 25 == 0 or n_done == n_total:
                        print(
                            f"[{n_done}/{n_total}] {family} {symbol} {year:04d}-{month:02d} sha={rec.sha256[:12]} rows={rec.row_count}"
                        )
                        sys.stdout.flush()

    # Integrity check + manifest per (family, symbol).
    failed: list[tuple[str, str]] = []
    manifest_paths: list[Path] = []
    for family in families:
        for symbol in SYMBOLS:
            recs = all_records[(family, symbol)]
            integrity = integrity_check_dataset(family, symbol, recs)
            dv = dataset_version_for(family, symbol)
            preds = predecessor_versions_for(family, symbol)
            mp = write_manifest(
                dataset_version=dv,
                family=family,
                symbol=symbol,
                records=recs,
                integrity=integrity,
                predecessor_versions=preds,
            )
            manifest_paths.append(mp)
            print(
                f"manifest {dv}: bars={integrity.bar_count} "
                f"gaps={integrity.gaps_detected} mono={integrity.monotone_timestamps} "
                f"coverage={integrity.date_range_coverage} eligible={integrity.passes()}"
            )
            sys.stdout.flush()
            if not integrity.passes():
                failed.append((family, symbol))

    if failed:
        print(f"INTEGRITY FAILURE: {failed}")
        return 1
    print(f"Phase 3q acquisition + integrity validation complete. {len(manifest_paths)} manifests written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
