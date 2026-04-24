"""Phase 2e wider historical backfill runner.

Covers BTCUSDT + ETHUSDT USDⓈ-M perpetual futures for 2022-01
through 2026-03 across four datasets:

  - Standard 15m klines            -> binance_usdm_<sym>_15m__v002
  - Derived 1h bars                -> binance_usdm_<sym>_1h_derived__v002
  - Mark-price 15m klines          -> binance_usdm_<sym>_markprice_15m__v002
  - Funding-rate events            -> binance_usdm_<sym>_funding__v002

v001 manifests (Phase 2b/2c, 2026-03 only) are preserved unchanged
as audit trail. v002 manifests supersede v001 for the wider range.

Per GAP-20260420-029 (resolved 2026-04-20): funding events before
~2024-01-01 have empty markPrice from Binance; they still normalize
cleanly with mark_price=None under the Option C model.

Per Phase 2e Gate 1 + operator approvals:

  - No parameter tuning. No threshold changes.
  - No authenticated endpoints. No credentials. Public data only.
  - No new dependencies.
  - All artifacts under data/ are git-ignored and must NOT be
    committed.
  - No push; no merge; Gate-2 stop before any commit.

Usage::

    uv run python scripts/phase2e_backfill.py

Idempotent re-runs:

  - Standard klines: state file in data/manifests/_downloads/
    tracks NORMALIZED months; re-runs skip completed months.
  - Mark-price klines: BulkDownloader is checksum-idempotent on the
    ZIP level; Parquet writes overwrite existing partition files
    with byte-identical content. Re-run is safe.
  - Funding: REST paginator re-fetches the full window. ~10 REST
    calls for the 4-year+ range at 1s pacing per client.
"""

from __future__ import annotations

from pathlib import Path

import httpx

from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol
from prometheus.research.data.binance_bulk import BulkDownloader, BulkFamily
from prometheus.research.data.binance_rest import BinanceRestClient
from prometheus.research.data.ingest import (
    ingest_funding_range,
    ingest_mark_price_monthly_range,
    ingest_monthly_range,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"

START_YEAR = 2022
START_MONTH = 1
END_YEAR = 2026
END_MONTH = 3

# UTC ms window for funding. Inclusive both ends at day boundaries.
# 2022-01-01 00:00:00 UTC = 1640995200000
# 2026-04-01 00:00:00 UTC = 1775001600000 (exclusive upper bound; we use
#   end_time_ms = 2026-03-31T23:59:59.999Z to match month-end coverage)
FUNDING_START_MS = 1_640_995_200_000
FUNDING_END_MS = 1_775_001_599_999  # 2026-03-31T23:59:59.999Z


SYMBOLS = (Symbol.BTCUSDT, Symbol.ETHUSDT)


def _v002(symbol: Symbol, dataset: str) -> str:
    """Return the v002 dataset version string for a (symbol, dataset) pair."""
    return f"binance_usdm_{symbol.value.lower()}_{dataset}__v002"


def _banner(title: str) -> None:
    bar = "=" * 72
    print(f"\n{bar}\n{title}\n{bar}")


def run_kline_backfill() -> None:
    _banner("Standard 15m klines + derived 1h bars (v002)")
    http = httpx.Client(timeout=60.0, follow_redirects=True)
    downloader = BulkDownloader(
        http,
        raw_root=DATA_ROOT / "raw",
        family=BulkFamily.KLINES,
        pace_ms=100,
    )
    normalized_root = DATA_ROOT / "normalized" / "klines"
    derived_root = DATA_ROOT / "derived" / "bars_1h" / "standard"
    manifests_root = DATA_ROOT / "manifests"
    state_root = DATA_ROOT / "manifests" / "_downloads"

    for symbol in SYMBOLS:
        dataset_v002_15m = _v002(symbol, "15m")
        dataset_v002_1h = _v002(symbol, "1h_derived")
        print(f"\n-- {symbol.value} -- 15m: {dataset_v002_15m}  1h: {dataset_v002_1h}")
        result = ingest_monthly_range(
            downloader,
            symbol=symbol,
            interval=Interval.I_15M,
            start_year=START_YEAR,
            start_month=START_MONTH,
            end_year=END_YEAR,
            end_month=END_MONTH,
            normalized_root=normalized_root,
            derived_root=derived_root,
            manifests_root=manifests_root,
            state_root=state_root,
            dataset_version_15m=dataset_v002_15m,
            dataset_version_1h=dataset_v002_1h,
        )
        cached = sum(1 for m in result.months if m.was_cached)
        downloaded = len(result.months) - cached
        print(f"   months: {len(result.months)} total, {downloaded} downloaded, {cached} cached")
        print(f"   total 15m rows: {result.total_row_count:,}")
        print(f"   invalid 15m windows: {len(result.invalid_windows_15m)}")
        print(f"   derived 1h rows:  {result.derived_1h_row_count:,}")
        print(f"   derived invalid windows: {len(result.derived_invalid_windows)}")
    http.close()


def run_mark_price_backfill() -> None:
    _banner("Mark-price 15m klines (v002)")
    http = httpx.Client(timeout=60.0, follow_redirects=True)
    downloader = BulkDownloader(
        http,
        raw_root=DATA_ROOT / "raw",
        family=BulkFamily.MARK_PRICE_KLINES,
        pace_ms=100,
    )
    normalized_root = DATA_ROOT / "normalized" / "mark_price_klines"
    manifests_root = DATA_ROOT / "manifests"

    for symbol in SYMBOLS:
        dataset_v002 = _v002(symbol, "markprice_15m")
        print(f"\n-- {symbol.value} -- mark-price: {dataset_v002}")
        result = ingest_mark_price_monthly_range(
            downloader,
            symbol=symbol,
            interval=Interval.I_15M,
            start_year=START_YEAR,
            start_month=START_MONTH,
            end_year=END_YEAR,
            end_month=END_MONTH,
            normalized_root=normalized_root,
            manifests_root=manifests_root,
            dataset_version=dataset_v002,
        )
        print(f"   total rows: {result.total_row_count:,}")
        print(f"   months:     {len(result.months_processed)}")
    http.close()


def run_funding_backfill() -> None:
    _banner("Funding-rate events (v002) -- per GAP-20260420-029, mark_price may be None")
    http = httpx.Client(timeout=60.0, follow_redirects=True)
    rest = BinanceRestClient(
        http,
        base_url="https://fapi.binance.com",
        pace_ms=1000,  # per GAP-20260419-012: 500/5min/IP shared limit
    )
    normalized_root = DATA_ROOT / "normalized" / "funding_rate"
    manifests_root = DATA_ROOT / "manifests"

    for symbol in SYMBOLS:
        dataset_v002 = _v002(symbol, "funding")
        print(f"\n-- {symbol.value} -- funding: {dataset_v002}")
        result = ingest_funding_range(
            rest,
            symbol=symbol,
            start_time_ms=FUNDING_START_MS,
            end_time_ms=FUNDING_END_MS,
            normalized_root=normalized_root,
            manifests_root=manifests_root,
            dataset_version=dataset_v002,
        )
        # Report mark_price coverage per GAP-20260420-029.
        from prometheus.research.data.storage import read_funding_rate_events

        events = read_funding_rate_events(normalized_root, symbol=symbol)
        with_mp = sum(1 for e in events if e.mark_price is not None)
        without_mp = sum(1 for e in events if e.mark_price is None)
        print(f"   event_count: {result.event_count:,}")
        print(f"   first_funding_time_ms: {result.first_funding_time_ms}")
        print(f"   last_funding_time_ms:  {result.last_funding_time_ms}")
        print(f"   mark_price populated: {with_mp:,}")
        print(f"   mark_price is None:   {without_mp:,}")
    http.close()


def main() -> None:
    _banner(
        f"Phase 2e wider historical backfill\n"
        f"Range: {START_YEAR}-{START_MONTH:02d} through {END_YEAR}-{END_MONTH:02d}\n"
        f"Symbols: {', '.join(s.value for s in SYMBOLS)}\n"
        f"Manifest version: v002 (v001 preserved as audit trail)"
    )
    run_kline_backfill()
    run_mark_price_backfill()
    run_funding_backfill()
    _banner("Phase 2e backfill complete")


if __name__ == "__main__":
    main()
