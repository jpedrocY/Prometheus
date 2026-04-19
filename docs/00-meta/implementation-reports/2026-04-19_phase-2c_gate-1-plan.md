# Phase 2c — Gate 1 Plan

**Date:** 2026-04-19
**Phase:** 2c — Mark-Price Klines, Funding History, and Public Exchange Metadata
**Current branch:** `main` (after Phase 2b merged via PR #3; commit `731088f`)
**Status:** PLAN ONLY. No branch created. No files edited. No dependencies installed. No network activity. Awaiting operator Gate 1 approval.

---

## 1. Executive Summary

Phase 2c completes the public-market-data foundation by adding the three remaining datasets Phase 3's backtester needs for realistic fill + cost modeling: **mark-price klines**, **funding-rate history**, and **exchangeInfo snapshots**. All three are **public** endpoints; no API keys, no signed requests, no `/fapi/*` authenticated endpoints touched. The account-authenticated cousins (`leverageBracket`, `commissionRate`) remain explicitly deferred.

**Key scoping choices proposed for operator approval:**

- **Three datasets per source:**
  - **Mark-price klines** — bulk-first via `data.binance.vision` (mirroring Phase 2b). Fallback: REST `/fapi/v1/markPriceKlines` only if bulk proves unavailable at Gate 2 verification time.
  - **Funding-rate history** — public REST `/fapi/v1/fundingRate` only (Binance does not publish bulk funding files). Paginated.
  - **ExchangeInfo snapshot** — public REST `/fapi/v1/exchangeInfo`, single GET per snapshot. JSON-body persistence.
- **One new source module family:** a small public-REST client (`binance_rest.py`) with timeout/retry/backoff, no credential path, no signed-request code. Three dataset-specific modules sit on top of it.
- **Three new typed models:** `MarkPriceKline`, `FundingRateEvent`, `ExchangeInfoSnapshot`. All frozen / strict / Pydantic v2 — same pattern as `NormalizedKline` / `DatasetManifest`.
- **No new dependencies.** `httpx` is already installed (Phase 2b). Everything else is stdlib or already-installed (`pyarrow`, `duckdb`, `pydantic`).
- **Authentication boundary is hard-coded into the module layout:** `binance_rest.py` has no credential injection point and no request-signing code; any future authenticated access requires a new module gate, documented and phase-gated.
- **TD-006 partial-resolution expansion:** Phase 2b resolved the bulk-CSV kline slice. Phase 2c adds three more slices (bulk mark-price klines, REST `fundingRate`, REST `exchangeInfo`). User-stream and account-authenticated endpoints remain OPEN for later phases.
- **Bounded Gate 2 real-data run:** BTCUSDT + ETHUSDT mark-price 15m for 2026-03, BTC + ETH funding events for 2026-03, and one exchangeInfo snapshot. Total estimated footprint: under 1.5 MB.
- **Commits:** 5 small + post-Gate-2 checkpoint, same cadence as Phase 2 and Phase 2b.

Runtime capability at end of Phase 2c: still zero live trading, zero exchange-write, zero credentials. Research capability: complete public-data foundation sufficient for Phase 3 backtester fill + funding modeling.

---

## 2. Current branch/status verification commands

```bash
git -C c:/Prometheus rev-parse --abbrev-ref HEAD                  # → main
git -C c:/Prometheus status --short                                # → (clean)
git -C c:/Prometheus log --oneline -6                               # → 731088f Merge PR #3 (phase-2b), then Phase 2b commits
git -C c:/Prometheus rev-list --left-right --count HEAD...@{u}      # → 0  0
git -C c:/Prometheus branch -vv
```

Confirmed at planning time:

- branch: `main`
- working tree: clean
- sync: `0 0` (up-to-date with `origin/main`)
- last commit: `731088f Merge pull request #3 from jpedrocY/phase-2b/real-historical-download`

These are re-run at Phase 2c Step 0 pre-flight before any edit.

---

## 3. Proposed Phase 2c branch name

```
phase-2c/public-market-data-completion
```

Branch off current `main` (`731088f`). No push during Phase 2c execution. PR into `main` after Gate 2, same pattern as Phase 2 / 2b.

---

## 4. Exact scope

Phase 2c delivers three dataset pipelines and the minimal shared infrastructure they share:

### 4.1 Shared infrastructure

1. **`src/prometheus/research/data/binance_rest.py`** — generic public-REST client.
   - `BinanceRestClient` — `httpx.Client`-injected (testable via `MockTransport`). GET-only. No `Authorization` header construction. No `X-MBX-APIKEY` header construction. No signed-request code of any kind. Timeouts + retry + exponential backoff identical to `BulkDownloader`'s posture, plus weight-aware pacing via `X-MBX-USED-WEIGHT-1M` response-header tracking.
   - Strictly limited to base URL `https://fapi.binance.com`.
   - Per-TD-006: URL patterns, response shapes, and status-code semantics verified via WebFetch at Gate 2 before any real REST call.

### 4.2 Dataset pipelines

2. **Mark-price klines** (`mark_price.py`, reusing `binance_bulk.py` patterns).
   - `MarkPriceBulkDownloader` or extension of `BulkDownloader` for the mark-price URL variant.
   - Bulk CSV path (assumed, must verify): `https://data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/<INTERVAL>/<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip` and paired `.CHECKSUM`.
   - Same checksum verification, atomic `.partial` → rename, idempotency, retry/backoff as Phase 2b.
   - `parse_binance_mark_price_csv_row` + `extract_mark_price_rows_from_zip` — trimmed schema (9 columns instead of 12; no volumes, no trade count, no taker buy volumes).
   - REST fallback deferred: if bulk files are unavailable at Gate 2 verification, **escalate**; do not silently fall back to REST without an operator decision.

3. **Funding-rate history** (`funding_rate.py`).
   - `FundingRateRestSource` — uses `BinanceRestClient`.
   - Endpoint: `GET /fapi/v1/fundingRate?symbol={SYM}&startTime={ms}&endTime={ms}&limit=1000` (verify at Gate 2).
   - Pagination: iterate with incrementing `startTime` until empty page returned.
   - Parses each event into `FundingRateEvent(symbol, funding_time, funding_rate, mark_price, source)`.
   - No bulk source — Binance does not publish funding-rate bulk files (to my knowledge; verify at Gate 2).

4. **ExchangeInfo snapshot** (`exchange_info.py`).
   - `ExchangeInfoRestSource` — uses `BinanceRestClient`.
   - Endpoint: `GET /fapi/v1/exchangeInfo` (verify at Gate 2).
   - Single GET returning a large JSON. The raw JSON body is persisted verbatim as `data/raw/binance_usdm/exchange_info/<YYYY-MM-DDTHH-MM-SSZ>.json` (operator-local, git-ignored).
   - Parsed into a structured `ExchangeInfoSnapshot(timezone, server_time_ms, snapshot_time_ms, symbols: tuple[SymbolInfo, ...], filters, ...)` — typed model.
   - Filters stored for only the Prometheus-relevant symbols (BTCUSDT, ETHUSDT) in a derived summary JSON alongside the raw snapshot; the raw JSON is retained for reproducibility.

### 4.3 Data models

5. **`src/prometheus/core/mark_price_klines.py`** (new).
   - `MarkPriceKline` Pydantic model, frozen/strict/extra=forbid.
   - Schema from `docs/04-data/historical-data-spec.md`: `symbol, interval, open_time, close_time, open, high, low, close, source`. Primary key: `(symbol, interval, open_time)`.
   - Enforces interval alignment, `close_time = open_time + duration - 1`, OHLC sanity.
   - No volume / trade_count / taker fields (those don't exist on mark-price klines).

6. **`src/prometheus/core/events.py`** (new).
   - `FundingRateEvent` Pydantic model. Schema: `symbol, funding_time, funding_rate, mark_price, source`. Primary key: `(symbol, funding_time)`.
   - `funding_time` in UTC ms. Sanity: `-1 < funding_rate < 1` (extremely wide guardrail; flag beyond ±1% as an invalid-window candidate, not a hard error).

7. **`src/prometheus/core/exchange_info.py`** (new, NOT in research/data/).
   - `SymbolInfo` — per-symbol metadata (symbol, contract_type, status, quote_asset, price_precision, quantity_precision, filters, ...).
   - `ExchangeInfoSnapshot` — the full wrapper (timezone, server_time_ms, snapshot_fetched_at_utc_ms, symbols).
   - This is a domain primitive consumed by strategy / risk later, so it lives in `core/` (per codebase-structure.md "core owns common domain types").

### 4.4 Storage layer extensions

8. **`src/prometheus/research/data/storage.py`** (modified).
   - Add `MARK_PRICE_KLINE_COLUMNS` + `MARK_PRICE_KLINE_ARROW_SCHEMA` (9-column variant).
   - Add `FUNDING_RATE_EVENT_COLUMNS` + `FUNDING_RATE_EVENT_ARROW_SCHEMA`.
   - Add `write_mark_price_klines` and `read_mark_price_klines` (Hive partitioning: `symbol=<SYM>/interval=<INTV>/year=YYYY/month=MM/`).
   - Add `write_funding_rate_events` and `read_funding_rate_events` (Hive partitioning: `symbol=<SYM>/year=YYYY/month=MM/` — no interval dimension).
   - ExchangeInfo does NOT use Parquet — persisted as JSON (raw + derived summary). Reasons: it's a snapshot, not a time-series; it's small; JSON round-trip is already tested via the Phase 2 manifest machinery.

### 4.5 Ingest orchestrators

9. **`src/prometheus/research/data/ingest.py`** (extended, not replaced).
   - `ingest_mark_price_monthly_range(...)` — mirrors `ingest_monthly_range` for mark-price data. Reuses `BulkDownloader` (or a mark-price variant thereof), `normalize_mark_price_rows`, `write_mark_price_klines`.
   - `ingest_funding_range(...)` — REST-driven, paginated, writes Parquet partitioned by `(symbol, year, month)`.
   - `fetch_exchange_info_snapshot(...)` — single REST call, writes raw JSON + derived summary + manifest entry.
   - Each produces a `DatasetManifest` of the appropriate `dataset_category`.

### 4.6 Quality

10. **Dataset-specific quality checks** (extend `quality.py` or new module):
    - Mark-price: reuses `check_no_duplicates`, `check_timestamp_monotonic`, `check_no_missing_bars`, `check_no_future_bars` (all applicable — mark-price is bar-indexed identically to standard klines).
    - Funding: `check_no_duplicate_funding_events(events)` — keyed by `(symbol, funding_time)`. `check_funding_rate_magnitude(events, threshold=0.01)` — flags events > 1% as likely-anomalous (not hard fail; recorded as invalid-window candidates).
    - ExchangeInfo: `check_exchange_info_contains_symbols(snapshot, required)` — asserts BTCUSDT + ETHUSDT are present.

### 4.7 Fixtures + tests

11. **Synthetic mark-price ZIP fixture** — hand-rolled 9-column CSV mirroring Phase 2b's test pattern.
12. **Synthetic funding-rate JSON fixture** — small array of funding events.
13. **Synthetic exchangeInfo JSON fixture** — trimmed to BTCUSDT + ETHUSDT only.
14. **Comprehensive tests** — see §25.

---

## 5. Explicit non-goals

- **No account-authenticated endpoints.** Explicitly excluded: `/fapi/v1/leverageBracket`, `/fapi/v2/commissionRate`, all `/fapi/v1/account/*`, all `/fapi/v1/openOrders`, all `/fapi/v1/userDataStream` calls. These require API keys (which do not exist in this project) or signed requests (which no module implements).
- **No API keys created or requested.** `binance_rest.py` will have no `api_key` parameter, no `secret` parameter, no `sign_request` function, no `X-MBX-APIKEY` header construction. Any future phase that needs authenticated access must add a separate module under an explicit phase gate.
- **No Binance testnet use.** Production public endpoints only. Testnet decision remains TD-007, deferred to pre-paper-shadow.
- **No WebSocket code.** User-stream, market-stream, combined-stream — all deferred.
- **No full historical backfill.** Operator-run with the same `ingest_*` calls over expanded ranges; not a Phase 2c deliverable.
- **No mark-price bulk fallback to REST without operator approval.** If bulk turns out to be unavailable at Gate 2 verification, escalate before using the REST endpoint.
- **No `src/prometheus/market_data/` runtime module.** Runtime kline consumption belongs to Phase 5/6/7.
- **No strategy, risk, execution, exchange adapter, persistence, operator, runtime, dashboard modules.**
- **No CLI script.** `scripts/fetch_historical_data.py` + friends remain deferred.
- **No config loader.** `configs/dev.example.yaml` gains new documentation keys only; no runtime consumption.
- **No edits to `docs/12-roadmap/technical-debt-register.md`** without stopping and asking first (per Phase 2b operator instruction).
- **No edits to `CLAUDE.md`, `docs/00-meta/current-project-state.md`, `.claude/*`, `.mcp.*` templates.**
- **No `.mcp.json` creation.** No Graphify activation.
- **No pre-commit hooks, no CI workflow.** Still deferred.

---

## 6. Proposed files/directories to create or modify

### 6.1 New source files (under `src/prometheus/core/`)

```
src/prometheus/core/mark_price_klines.py   # MarkPriceKline model (9-field)
src/prometheus/core/events.py               # FundingRateEvent model
src/prometheus/core/exchange_info.py        # ExchangeInfoSnapshot + SymbolInfo models
```

### 6.2 New source files (under `src/prometheus/research/data/`)

```
src/prometheus/research/data/binance_rest.py          # generic public-REST client (no auth)
src/prometheus/research/data/mark_price.py            # bulk mark-price downloader + CSV parser
src/prometheus/research/data/funding_rate.py          # REST funding-rate source + pagination
src/prometheus/research/data/exchange_info.py         # REST exchangeInfo snapshot fetcher + parser
```

### 6.3 Modified existing files

| File | Change | Justification |
| --- | --- | --- |
| `src/prometheus/research/data/storage.py` | Add mark-price + funding-rate Arrow schemas, `write_/read_` helpers | Parquet partitioning for the two new time-series datasets |
| `src/prometheus/research/data/ingest.py` | Add `ingest_mark_price_monthly_range`, `ingest_funding_range`, `fetch_exchange_info_snapshot` | Orchestrators for the three datasets, reusing the Phase 2 & 2b pipeline primitives |
| `src/prometheus/research/data/quality.py` | Add `check_no_duplicate_funding_events`, `check_funding_rate_magnitude`, `check_exchange_info_contains_symbols` | Dataset-specific integrity checks |
| `src/prometheus/research/data/__init__.py` | Extend `__all__` + re-exports with new public names | Keep the research.data surface discoverable |
| `configs/dev.example.yaml` | Add `mark_price:` + `funding:` + `exchange_info:` subsections under `research_data:` | Documentation of default paths; no loader consumes them yet |
| `docs/00-meta/implementation-ambiguity-log.md` | Append GAP-011..GAP-013 (expected Phase 2c entries; see §27) | Standard ambiguity-log discipline |

### 6.4 New tests (under `tests/`)

```
tests/unit/core/test_mark_price_klines.py
tests/unit/core/test_events.py
tests/unit/core/test_exchange_info.py
tests/unit/research/data/test_binance_rest.py
tests/unit/research/data/test_mark_price.py
tests/unit/research/data/test_funding_rate.py
tests/unit/research/data/test_exchange_info.py
tests/unit/research/data/test_storage_mark_price.py   # or merge into test_storage.py
tests/unit/research/data/test_storage_funding_rate.py # or merge
tests/integration/test_mark_price_end_to_end.py
tests/integration/test_funding_rate_end_to_end.py
tests/integration/test_exchange_info_end_to_end.py
```

### 6.5 New fixtures

```
tests/fixtures/market_data/binance_bulk/
  BTCUSDT_markPrice-15m-2026-03.zip          (synthetic mini)
  BTCUSDT_markPrice-15m-2026-03.zip.CHECKSUM (matching)
  ETHUSDT_markPrice-15m-2026-03.zip          (synthetic mini)
  ETHUSDT_markPrice-15m-2026-03.zip.CHECKSUM (matching)
tests/fixtures/market_data/binance_rest/
  fundingRate_BTCUSDT_2026-03.json           (synthetic mini, ~6 events)
  fundingRate_ETHUSDT_2026-03.json           (synthetic mini, ~6 events)
  exchangeInfo_small.json                     (trimmed: BTCUSDT + ETHUSDT + minimal filters)
```

All committed fixtures are **synthetic**; no real Binance data in the repo.

### 6.6 New docs

```
docs/00-meta/implementation-reports/2026-04-19_phase-2c_gate-2-review.md   # after implementation
docs/00-meta/implementation-reports/2026-04-19_phase-2c-checkpoint-report.md # after Gate 2 approval
```

Plus appended entries to `docs/00-meta/implementation-ambiguity-log.md`.

---

## 7. Dependency additions

**None.** Phase 2c has zero new runtime or dev-group dependencies. Everything needed is already installed:

| Need | Already satisfied by |
| --- | --- |
| HTTP client | `httpx>=0.27` (Phase 2b) |
| Parquet I/O | `pyarrow>=17` (Phase 2) |
| SQL over Parquet | `duckdb>=1.1` (Phase 2) |
| Typed models | `pydantic>=2.8` (Phase 2) |
| Lint / format / type / test | `ruff`, `mypy`, `pytest`, `pytest-cov` (Phase 1 dev group) |

No `uv sync` needed structurally, but I will still run `uv sync` at Gate 1 wake-up to confirm `uv.lock` still resolves cleanly under the Phase 2b pins.

---

## 8. Official Binance public-source options to verify at implementation time

Per TD-006, the following URL patterns and response shapes are **assumptions that Phase 2c must verify against official Binance sources** (via WebFetch of the README and direct fetches of small sample files) **before writing any code that depends on them.**

### 8.1 Mark-price klines (bulk)

- **Assumed bulk path:** `https://data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/<INTERVAL>/<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip`
- **Assumed checksum:** `<zip-url>.CHECKSUM` with the same `<sha256hex>  <filename>` format as standard klines (verified in Phase 2b).
- **Assumed CSV columns:** per `historical-data-spec.md` §"Mark-price kline schema": `open_time, open, high, low, close, ignore1, close_time, ignore2, ignore3, ignore4, ignore5, ignore6` (12 positional fields; only 6 are meaningful; no volume / trade_count / taker fields).
- **Header row:** status unknown — GAP-010 taught us to test defensively. `_is_mark_price_csv_header` predicate will apply.

### 8.2 Mark-price klines (REST fallback, not planned to be implemented in 2c)

- **Endpoint:** `GET /fapi/v1/markPriceKlines` at `https://fapi.binance.com`.
- **Docs URL:** `https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Mark-Price-Kline-Candlestick-Data` (per `historical-data-spec.md`).
- **Scope gate:** only to be implemented if bulk mark-price turns out to be unavailable at Gate 2 verification. Otherwise deferred.

### 8.3 Funding-rate history (REST)

- **Endpoint:** `GET /fapi/v1/fundingRate` at `https://fapi.binance.com`.
- **Docs URL:** `https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History`.
- **Assumed params:** `symbol`, `startTime` (ms), `endTime` (ms), `limit` (max 1000).
- **Assumed response shape:** array of `{symbol, fundingTime, fundingRate, markPrice}` (or similar — verify field names exactly at Gate 2). `fundingTime` assumed UTC milliseconds.
- **Weight assumption:** 1 (to verify).
- **Pagination rule assumption:** if response length == 1000, advance `startTime` to last event's `fundingTime + 1` and continue. Stop on an empty or partial page.

### 8.4 ExchangeInfo (REST)

- **Endpoint:** `GET /fapi/v1/exchangeInfo` at `https://fapi.binance.com`.
- **Docs URL:** `https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information`.
- **Weight assumption:** 1 (to verify).
- **Response shape:** large JSON with `timezone`, `serverTime`, `rateLimits`, `exchangeFilters`, `assets`, `symbols` (~ 200+ symbols). To verify exact field set at Gate 2.

### 8.5 Deferred (NOT Phase 2c scope — account-authenticated)

| Endpoint | Auth required? | Status |
| --- | --- | --- |
| `/fapi/v1/leverageBracket` | **Yes** (API key) | Deferred to credential-gated phase |
| `/fapi/v2/commissionRate` | **Yes** (signed) | Deferred to credential-gated phase |
| `/fapi/v1/account/*` | **Yes** (signed) | Deferred |
| `/fapi/v1/openOrders` | **Yes** (signed) | Deferred |
| `/fapi/v1/userDataStream` | **Yes** (API key) | Deferred |

### 8.6 Verification deliverable in Phase 2c

Each of `binance_rest.py`, `mark_price.py`, `funding_rate.py`, `exchange_info.py` will carry a `## TD-006 verification evidence` block comment at the top, documenting:

1. Each assumption (URL, params, response fields, status codes).
2. The official Binance doc URL checked.
3. The verification date.
4. Any divergence → GAP entry → escalation before writing code.

This is identical to the Phase 2b pattern that worked well (caught GAP-010).

---

## 9. Recommendation per dataset

### 9.1 Mark-price klines: **bulk-first**

Same reasoning as Phase 2b. Monthly ZIPs are immutable, ship with SHA256 checksums, do not require pagination, and do not pressure REST rate limits. REST fallback only on operator approval.

### 9.2 Funding-rate history: **REST-only**

To my knowledge Binance does not publish bulk funding-rate files on `data.binance.vision`. Phase 2c's Gate 2 verification will confirm this one way or the other before the code runs. If bulk turns out to exist, Phase 2c will use bulk (cheaper, immutable, checksummed). If not, REST with pagination + rate-limit awareness.

### 9.3 ExchangeInfo: **REST snapshot**

ExchangeInfo is fundamentally a point-in-time snapshot, not a time-series. There is no bulk option. Single GET. Persist the raw JSON verbatim (for reproducibility) plus a parsed `ExchangeInfoSnapshot` model (for typed consumption).

---

## 10. Authentication boundary (hard rule)

Phase 2c's `BinanceRestClient` is constructed without any credential parameters. Its public surface is:

```python
class BinanceRestClient:
    def __init__(
        self,
        client: httpx.Client,
        *,
        base_url: str = "https://fapi.binance.com",
        user_agent: str = _DEFAULT_USER_AGENT,
        pace_ms: int = _DEFAULT_PACE_MS,
        clock: Callable[[], float] | None = None,
        sleep: Callable[[float], None] | None = None,
    ) -> None: ...

    def get_json(self, path: str, *, params: dict[str, Any] | None = None) -> Any: ...
```

There is **no** `api_key` parameter, **no** `secret` parameter, **no** `sign_request` method, **no** `X-MBX-APIKEY` header construction, **no** HMAC-SHA256 code. Adding any of those to `binance_rest.py` would be an explicit scope violation and requires a new phase gate.

A unit test `test_binance_rest_has_no_auth_surface` will assert the class does not expose any of those names (`hasattr` negative checks) — a mechanical guardrail against future drift.

---

## 11. Bounded smoke ranges for Gate 2

Three small, complete operator-reviewable slices:

| Dataset | Symbols | Range | Estimated raw size | Why this choice |
| --- | --- | --- | --- | --- |
| Mark-price 15m bulk | BTCUSDT + ETHUSDT | 2026-03 | ~2 × 120 KB = ~240 KB | Same month as Phase 2b standard klines — enables cross-comparison |
| Funding rate | BTCUSDT + ETHUSDT | 2026-03 | ~93 events × 2 × ~100 B = ~18 KB | 3 events/day × 31 days per symbol; 1 paginated request per symbol |
| ExchangeInfo | full exchange (parsed for BTCUSDT + ETHUSDT) | Snapshot at `utc_now_ms()` | ~200 KB raw JSON | Single GET; persist raw + derived summary |

Total bounded Gate 2 footprint: **under 1.5 MB** across raw, Parquet, and manifests. Comfortably smaller than Phase 2b (796 KB) plus mark-price duplication.

---

## 12. Estimated disk footprint

For the Gate 2 run (all three datasets, one month each, two symbols):

| Artifact | Location | Estimate |
| --- | --- | --- |
| Mark-price raw ZIPs (2) | `data/raw/binance_usdm/markPriceKlines/symbol=<SYM>/interval=15m/year=2026/month=03/` | ~240 KB |
| Mark-price normalized Parquet (2) | `data/normalized/mark_price_klines/symbol=<SYM>/interval=15m/year=2026/month=03/` | ~220 KB |
| Funding-rate normalized Parquet (2) | `data/normalized/funding_rate/symbol=<SYM>/year=2026/month=03/` | ~8 KB (Parquet header overhead dominates vs ~18 KB raw events) |
| ExchangeInfo raw JSON (1) | `data/raw/binance_usdm/exchange_info/YYYY-MM-DDTHH-MM-SSZ.json` | ~200 KB |
| ExchangeInfo derived summary JSON (1) | `data/derived/exchange_info/latest.json` | ~10 KB |
| Manifests (5) | `data/manifests/` | ~5 KB |
| Download state files (2: mark-price + funding) | `data/manifests/_downloads/` | ~2 KB |
| **Total Gate 2 footprint** | `data/` (all git-ignored) | **~690 KB** |

Smaller than I initially estimated, because funding-rate Parquet is tiny (3 events/day is nothing).

---

## 13. Resumability plan

Each of the three pipelines resumes differently because their natures differ:

### 13.1 Mark-price (bulk)

Identical to Phase 2b's pattern. Per-month `DownloadStatus` state in `data/manifests/_downloads/binance_usdm_btcusdt_markprice_15m__state.json`. Existing `DownloadStatus` enum + `MonthDownloadState` reused verbatim; no schema changes needed.

### 13.2 Funding-rate (REST paginated)

State file `data/manifests/_downloads/binance_usdm_btcusdt_funding__state.json`:

```json
{
  "dataset_name": "binance_usdm_btcusdt_funding",
  "schema_version": "funding_state_v1",
  "months": {
    "2026-03": {
      "status": "NORMALIZED",
      "first_funding_time_ms": 1772323200000,
      "last_funding_time_ms": 1772924280000,
      "event_count": 93,
      "normalized_path": "data/normalized/funding_rate/symbol=BTCUSDT/year=2026/month=03/part-0000.parquet"
    }
  }
}
```

Per-month idempotency: if a month is in `NORMALIZED`, skip entirely. Pagination checkpoints are not persisted within a month — an interrupted month is re-fetched from its start. This keeps state simple at a tiny cost (re-fetching up to 1000 events).

### 13.3 ExchangeInfo (single REST)

No pagination, no multi-month concept. Each snapshot is a new file timestamped `YYYY-MM-DDTHH-MM-SSZ.json`. Re-running the fetch simply creates a new snapshot. A small `data/manifests/_downloads/exchange_info__state.json` records `last_snapshot_fetched_at_utc_ms` and the latest file path. No resume concept needed.

---

## 14. Rate-limit / retry / backoff plan

Bulk endpoint (mark-price): identical to Phase 2b (100 ms pacing, up to 5 retries with exponential backoff, 429 / 408 / 5xx retriable).

REST endpoints (funding + exchangeInfo):

- **Timeouts:** connect 10s, read 30s, write 10s.
- **Pacing:** minimum 100 ms between requests; additionally, parse the `X-MBX-USED-WEIGHT-1M` response header and pause to stay under the per-minute limit. A default ceiling of 1000 weight / minute (conservative vs Binance's typical 2400) is used.
- **Retry:** 5 attempts, exponential backoff 1s → 30s + jitter. Retriable statuses: `429`, `408`, `418` (IP banned — in practice should raise a harder warning), `5xx`.
- **Non-retriable 4xx raises** immediately.
- **No parallel requests.** Sequential, symbol-by-symbol.

### 14.1 Funding-rate pagination

Pseudocode:

```
start_ms = expected_start_ms
while True:
    events = GET /fapi/v1/fundingRate?symbol=X&startTime=start_ms&endTime=end_ms&limit=1000
    if not events: break
    write_batch(events)
    if len(events) < 1000: break
    start_ms = events[-1].funding_time + 1
```

Empty and short pages both terminate. Safe against infinite loops via a hard upper bound of 100 page iterations per month (far exceeds any realistic symbol's event count per month).

---

## 15. Checksum / file validation plan

Bulk mark-price: same as Phase 2b (paired `.CHECKSUM` SHA256, streaming verification, atomic `.partial` → rename).

REST (funding + exchangeInfo): no SHA256 upstream. Integrity instead relies on:

- **Strict response-shape validation** at parse time. Any divergence from expected fields raises `DataIntegrityError`.
- **Structural sanity** — exchangeInfo must contain `symbols` key, must contain `BTCUSDT` and `ETHUSDT`, must have `serverTime` and `timezone`.
- **Response-content SHA256** computed locally and recorded in the manifest's `notes` field for audit, even though Binance doesn't publish it. This makes reproducibility possible — two Gate 2 runs on the same response body produce identical hashes.

---

## 16. Raw data preservation plan

### 16.1 Bulk (mark-price)

Same as Phase 2b: raw ZIPs + `.CHECKSUM` files preserved under git-ignored `data/raw/binance_usdm/markPriceKlines/...`. Never modified. Downstream normalization opens the ZIP each time.

### 16.2 REST (funding + exchangeInfo)

Because REST responses have no upstream immutability guarantee, Phase 2c captures:

- **Raw response body**, verbatim, written to `data/raw/binance_usdm/funding_rate/symbol=<SYM>/year=YYYY/month=MM/fundingRate_<SYM>_<YYYY>-<MM>_page<N>.json` (one file per paginated page) and `data/raw/binance_usdm/exchange_info/<YYYY-MM-DDTHH-MM-SSZ>.json`.
- **Request URL + parameters + timestamp** embedded as a small sidecar `.meta.json` next to each raw response, so every request is traceable.

Normalization reads the raw files. Re-normalization without re-fetching is possible: if an operator deletes `data/normalized/funding_rate/` + `data/manifests/_downloads/*funding*`, the pipeline can re-compose from `data/raw/...` without another REST round-trip.

---

## 17. Normalized Parquet output plan

Identical to Phase 2 / 2b where applicable:

- **Mark-price Parquet**: Hive-partitioned `symbol=<SYM>/interval=<INTV>/year=YYYY/month=MM/part-0000.parquet`, zstd level 3, 65,536-row row groups, custom file metadata (`dataset_version`, `schema_version`, `pipeline_version`). Schema: the 9-field `MarkPriceKline` Arrow schema.
- **Funding-rate Parquet**: Hive-partitioned `symbol=<SYM>/year=YYYY/month=MM/part-0000.parquet` (no interval dimension — funding is a symbol-level event). Same metadata convention. Schema: the 4-field `FundingRateEvent` Arrow schema.
- **ExchangeInfo**: NOT Parquet. JSON raw + derived. Rationale: it's a snapshot, not a time-series, and keeping the JSON verbatim preserves full fidelity for reproducibility. The derived summary is also JSON for human readability.

---

## 18. Dataset manifest / versioning plan

One manifest per dataset per version:

```
data/manifests/binance_usdm_btcusdt_markprice_15m__v001.manifest.json
data/manifests/binance_usdm_ethusdt_markprice_15m__v001.manifest.json
data/manifests/binance_usdm_btcusdt_funding__v001.manifest.json
data/manifests/binance_usdm_ethusdt_funding__v001.manifest.json
data/manifests/binance_usdm_exchange_info__v001.manifest.json
```

Phase 2c introduces three new `dataset_category` values (added to the existing free-string field; no enum change):

| Category | Used by | Notes |
| --- | --- | --- |
| `mark_price_kline` | mark-price manifests | New. Analogous to Phase 2's `normalized_kline`. |
| `funding_rate_event` | funding manifests | New. Event-type data. |
| `exchange_info_snapshot` | exchangeInfo manifest | New. Point-in-time snapshot. |

All use the existing `DatasetManifest` model from Phase 2 — no model changes needed. `DatasetManifest.intervals` is a tuple; for funding and exchangeInfo (which have no interval concept) we set `intervals=()`.

Actually — current `DatasetManifest` requires non-empty `symbols`. There's no requirement that `intervals` is non-empty. We'll verify at coding time that `intervals=()` is accepted by the model. If not, a `GAP-011` will record the observation and propose either (a) relaxing the validator, or (b) using a sentinel interval like `"N/A"`. Default recommendation: relax to `intervals` can be empty — this matches the real shape of event-type data.

---

## 19. Invalid-window logging plan

### 19.1 Mark-price

Identical to Phase 2b (duplicates, monotonic, missing, future — all reuse the same quality functions; mark-price is bar-indexed the same way).

### 19.2 Funding-rate

- `check_no_duplicate_funding_events(events)` — keyed by `(symbol, funding_time)`.
- `check_funding_rate_magnitude(events, threshold=0.01)` — flags events where `|funding_rate| > threshold` as invalid-window candidates (not hard fails; recorded for operator attention).
- `check_funding_events_within_window(events, start_ms, end_ms)` — flags events outside the expected window.
- No `check_no_missing_events` — funding events can be missing for a legitimate reason (e.g., exchange downtime); we do not want to flag those as errors. Instead, the manifest's `event_count` field records what was found, and the operator compares against expected cadence (3 events/day) externally.

### 19.3 ExchangeInfo

- `check_exchange_info_contains_symbols(snapshot, required=("BTCUSDT", "ETHUSDT"))` — asserts required symbols are present. Hard fail.
- `check_exchange_info_server_time_sane(snapshot, now_ms)` — asserts `serverTime` is within ±5 minutes of local clock. Warning, not hard fail (large clock drift is possible in transit but shouldn't be silent).
- No duplicate / monotonic concept (single snapshot).

---

## 20. UTC Unix millisecond validation plan

Same three-layer enforcement as Phase 2 / 2b:

1. **Pydantic validators** in `MarkPriceKline` (reuses the same interval-alignment + `close_time` invariants as `NormalizedKline`) and `FundingRateEvent` (`funding_time > 0`, `|funding_rate| < 1.0` soft cap).
2. **Cross-dataset quality**: `check_timestamp_monotonic` (mark-price only; funding events can be non-monotonic within pagination pages? — no, they should be monotonic per symbol; the check applies).
3. **Boundary checks at ingest**: every timestamp verified as `int64` UTC ms before Pydantic construction. Microsecond-valued inputs (should Binance ever switch futures to microseconds) fail closed at the Pydantic `open_time > 0 and aligned-to-interval` validator.

ExchangeInfo: `serverTime` in ms is recorded, `snapshot_fetched_at_utc_ms` is the local fetch time in ms.

---

## 21. Duplicate / missing / malformed detection plan

### 21.1 Mark-price (bar-indexed)

- **Duplicates:** `check_no_duplicates` reused (keyed by `(symbol, interval, open_time)`).
- **Missing:** `check_no_missing_bars` reused.
- **Monotonic:** `check_timestamp_monotonic` reused.
- **Malformed CSV rows:** `parse_binance_mark_price_csv_row` — explicit 12-column check (9 meaningful + 3 trailing ignore/reserved), explicit numeric casts. Header detection via a `_is_mark_price_csv_header` predicate mirroring the standard-kline pattern from GAP-010.

### 21.2 Funding-rate (event-indexed)

- **Duplicates:** `check_no_duplicate_funding_events` (keyed by `(symbol, funding_time)`).
- **Malformed JSON:** per-event Pydantic construction raises on missing / wrong-type fields.
- **Out-of-window events:** `check_funding_events_within_window`.
- **Extreme rates:** `check_funding_rate_magnitude` — soft flag, not hard fail.

### 21.3 ExchangeInfo (snapshot)

- **Malformed JSON:** full `ExchangeInfoSnapshot.model_validate()` with strict mode. Any missing required field raises.
- **Required symbols present:** `check_exchange_info_contains_symbols`.
- **Server-time drift:** `check_exchange_info_server_time_sane`.

---

## 22. BTCUSDT + ETHUSDT coverage plan

All three datasets cover both symbols uniformly:

- **Mark-price**: one monthly ZIP per (symbol, 2026-03). Parquet partition per (symbol, 15m, 2026, 03). Two manifests.
- **Funding-rate**: one set of paginated REST calls per (symbol, 2026-03 window). Parquet partition per (symbol, 2026, 03). Two manifests.
- **ExchangeInfo**: one snapshot covers both symbols (single GET returns all exchange symbols; we filter for BTCUSDT + ETHUSDT in the derived summary). One manifest covering both.

Coverage completeness is recorded in each manifest's `invalid_windows` and `notes`.

---

## 23. How Phase 2c data supports Phase 3 backtesting

The Phase 3 backtester will need:

1. **Standard 15m klines** (`NormalizedKline` from Phase 2b) for the fill model's next-bar-open assumption.
2. **Mark-price 15m klines** (new in 2c) for realistic stop-loss behavior — protective stops in v1 use `workingType=MARK_PRICE`, so the backtester must evaluate stop hits against mark price, not trade price. Without mark-price data, stop-hit modeling would be systematically wrong.
3. **Funding-rate events** (new in 2c) for cumulative funding-cost accounting during positions open across funding timestamps. V1 strategy is breakout-continuation with potentially multi-hour trade durations; ignoring funding would distort PnL.
4. **ExchangeInfo** (new in 2c) for `tickSize`, `stepSize`, `minNotional`, `minQty`, `maxLeverage`, price/quantity precision. Without these, the backtester can't simulate realistic order rounding or reject under-minimum orders.

Together, Phase 2b + Phase 2c cover **all the public data** Phase 3's fill + cost model needs. Account-authenticated datasets (`leverageBracket` notional caps, `commissionRate` per-symbol fees) remain deferred; until they arrive, Phase 3 will use placeholder commission rates documented in `docs/03-strategy-research/v1-breakout-backtest-plan.md`.

---

## 24. Tests / checks to run

All tests offline. Zero real network calls during `pytest`.

### 24.1 Quality gates (must pass before Gate 2)

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Expected post-Phase-2c test count: **~170–190** (136 from Phase 2b + ~40–50 new).

### 24.2 New tests summary

| Module | Coverage |
| --- | --- |
| `test_mark_price_klines.py` (core) | Construction, frozen, strict, extra=forbid, interval alignment, close_time, OHLC sanity, no volume fields. |
| `test_events.py` (core) | `FundingRateEvent` — primary key invariants, funding-rate soft-bound, funding_time positivity. |
| `test_exchange_info.py` (core) | `ExchangeInfoSnapshot` + `SymbolInfo` — model construction, required-fields, strict mode. |
| `test_binance_rest.py` | GET-only; no auth headers constructed; timeout; retry on 429/5xx; retry exhaustion; non-retriable 404; weight-header parsing; pacing observance; **negative hasattr test for `api_key`, `secret`, `sign_request`**. |
| `test_mark_price.py` | URL construction for `markPriceKlines`, CSV parse, header-skip, ZIP extraction with mark-price schema. |
| `test_funding_rate.py` | Pagination (short page stops, full page continues, empty page stops), 1000-item page boundary, extreme-rate soft flag, duplicate detection. |
| `test_exchange_info.py` (research.data) | Parse sample exchangeInfo JSON, missing-symbol check, server-time drift check. |
| `test_storage_mark_price.py` / extensions to `test_storage.py` | Mark-price write/read round-trip, DuckDB view, Hive partitioning `symbol=/interval=/year=/month=/`. |
| `test_storage_funding_rate.py` / extensions | Funding-rate write/read round-trip, partitioning `symbol=/year=/month=/` (no interval). |
| `test_mark_price_end_to_end.py` | Full bulk → normalize → Parquet → DuckDB round-trip on synthetic ZIP. |
| `test_funding_rate_end_to_end.py` | Full REST → paginate → normalize → Parquet round-trip on synthetic JSON pages. |
| `test_exchange_info_end_to_end.py` | Full REST → parse → persist (raw + derived + manifest) on synthetic JSON. |

### 24.3 Negative auth-surface test (hard guardrail)

`test_binance_rest_has_no_auth_surface`:

```python
def test_binance_rest_has_no_auth_surface():
    from prometheus.research.data import binance_rest
    cls = binance_rest.BinanceRestClient
    for forbidden in ("api_key", "secret", "sign_request", "_sign", "X-MBX-APIKEY"):
        assert not hasattr(cls, forbidden), f"auth surface leaked: {forbidden}"
    # Also check no constructor parameter is named those.
    import inspect
    sig = inspect.signature(cls.__init__)
    for p in sig.parameters.values():
        assert p.name not in ("api_key", "secret", "key", "apikey"), p.name
```

This is a mechanical guardrail against future drift — if anyone later adds an auth parameter, CI fails.

---

## 25. Safety constraints

All prior-phase constraints preserved. Phase 2c-specific posture:

| Check | How Phase 2c preserves it |
| --- | --- |
| Production Binance API keys | **None created, none requested, none used.** `BinanceRestClient` has no auth surface. |
| Real secrets / `.env` | **None touched.** |
| Exchange-write | **None.** Only `GET` requests. |
| Authenticated endpoints | **Not touched.** `leverageBracket`, `commissionRate`, `/fapi/v1/account/*`, all deferred. |
| WebSockets | **None.** |
| Third-party market-data sources | **None.** Only `data.binance.vision` (bulk) and `fapi.binance.com` (public REST). |
| `.mcp.json` / Graphify | **Not created / not enabled.** |
| Real downloaded data committed | **None** — all artifacts under git-ignored `data/`. |
| `.claude/*` / `CLAUDE.md` / `docs/00-meta/current-project-state.md` | **Not modified.** |
| `docs/12-roadmap/technical-debt-register.md` | **Not modified without explicit operator approval.** |
| Runtime DB | **Not touched.** |
| Destructive git / `git add -f` | **None.** |
| Installs beyond `.venv/` | **None.** No new deps at all. |
| Network during tests | **Zero.** `httpx.MockTransport` for all tests. Real downloads only via `uv run python -c` at Gate 2. |
| Auth-surface drift in `binance_rest.py` | **Mechanically asserted** by `test_binance_rest_has_no_auth_surface`. |

---

## 26. Ambiguity / spec-gap items to log during execution

Expected GAP-011 through approximately GAP-014 (to be logged as actually encountered):

- **GAP-011 (likely):** `DatasetManifest` validator — does `intervals=()` pass? If not, document the workaround (sentinel string) or propose relaxing the validator. Either way, record the decision.
- **GAP-012 (expected):** exact response field names for `/fapi/v1/fundingRate` (is it `fundingTime` or `funding_time`? `fundingRate` or `funding_rate`? `markPrice` or `mark_price`?). Will verify via a single read-only WebFetch at Gate 2 before writing the parser. Record the verified names.
- **GAP-013 (expected):** existence of bulk mark-price files on `data.binance.vision`. If missing, escalate — do not silently fall back to REST.
- **GAP-014 (possible):** CSV header-row behavior for mark-price bulk files — applying the GAP-010 lesson defensively, but whether mark-price files have a header or not remains unknown until observed.
- **GAP-015 (possible):** `/fapi/v1/fundingRate` rate-limit weight — Binance docs may list this; we'll verify. If the weight is higher than assumed, widen pacing.
- **GAP-016 (possible):** `/fapi/v1/exchangeInfo` response may contain non-USD-M-perpetual symbol types (e.g., coin-M, spot). Filter defensively and record what was filtered.

Each, when logged, follows the Phase 1/2/2b format. Safety-relevant findings pause execution and request operator review **before any real network call** — same protocol as GAP-010.

---

## 27. TD-006 partial-resolution plan

Phase 2c extends the TD-006 partial-resolution coverage established by Phase 2b:

| Slice | Verified as of | Phase |
| --- | --- | --- |
| Bulk standard kline CSV | 2026-04-19 | Phase 2b ✓ |
| Bulk mark-price kline CSV | (Phase 2c) | Phase 2c — to verify at Gate 2 |
| REST `/fapi/v1/fundingRate` | (Phase 2c) | Phase 2c — to verify at Gate 2 |
| REST `/fapi/v1/exchangeInfo` | (Phase 2c) | Phase 2c — to verify at Gate 2 |
| REST `/fapi/v1/klines` | — | later |
| REST `/fapi/v1/markPriceKlines` | — | later (fallback only) |
| User-stream / WebSocket | — | later |
| Account-authenticated | — | credential-gated future phase |

No edits to `docs/12-roadmap/technical-debt-register.md` without stopping and asking (per operator directive in Phase 2b). The evidence blocks in `binance_rest.py`, `mark_price.py`, `funding_rate.py`, `exchange_info.py` document the per-module verification; TD-006's register entry can be annotated in a separate operator-approved follow-up if desired.

---

## 28. Proposed commit structure

Five small reviewable commits on `phase-2c/public-market-data-completion` + a post-Gate-2 checkpoint commit.

| # | Title | Contents |
| --- | --- | --- |
| 1 | `phase-2c: new core data models (MarkPriceKline, FundingRateEvent, ExchangeInfoSnapshot)` | `src/prometheus/core/mark_price_klines.py`, `src/prometheus/core/events.py`, `src/prometheus/core/exchange_info.py`, their unit tests. Updates to `core/__init__.py` re-exports. |
| 2 | `phase-2c: public-REST client with auth-surface guardrails` | `src/prometheus/research/data/binance_rest.py` + tests including the negative auth-surface test. TD-006 evidence block for the REST base URL + header conventions. |
| 3 | `phase-2c: mark-price bulk download + ingest + storage` | `mark_price.py`, extensions to `storage.py` (mark-price schema + read/write), extensions to `ingest.py` (`ingest_mark_price_monthly_range`), `quality.py` untouched (reuses existing), unit tests, synthetic ZIP fixtures. TD-006 evidence block. |
| 4 | `phase-2c: funding-rate REST + exchangeInfo REST + their ingest paths` | `funding_rate.py`, `exchange_info.py`, ingest additions, storage extensions for funding-rate Parquet, new quality checks, unit tests, synthetic JSON fixtures. TD-006 evidence blocks. |
| 5 | `phase-2c: integration tests, __init__ re-exports, ambiguity log + Gate-1/Gate-2 reports` | All three end-to-end integration tests, full `research/data/__init__.py` update, ambiguity-log entries (GAP-011..whatever-was-actually-encountered), both Phase 2c implementation-reports docs. |
| 6 (post-Gate-2) | `phase-2c: checkpoint report` | Checkpoint report. Any TD-006 status annotation bundled here only if operator approves the edit to `technical-debt-register.md`. |

All commit messages follow Phase 1/2/2b convention (no `Co-Authored-By`).

No push, no PR during execution. Operator decides when to merge.

---

## 29. Gate 2 review / checkpoint report format

Matches Phase 2b exactly. Gate 2 review at `docs/00-meta/implementation-reports/2026-04-19_phase-2c_gate-2-review.md`:

1. Purpose
2. Operator conditions at Gate 1 recap
3. Official-source verification evidence (TD-006 extensions — 3 new slices)
4. Any mid-run divergence + GAP + resolution (if any — similar to GAP-010 pattern)
5. Commands run
6. Real bounded download results (3 datasets × 2 symbols, SHA256s + row counts + quality summaries)
7. Disk footprint
8. Files changed (tracked + untracked)
9. `git status` / `git diff --stat` / `git diff`
10. Quality-gate results
11. Quality-check results on real data
12. Safety checklist
13. Ambiguity-log entries
14. Phase 2c Gate 1 acceptance-criteria self-check
15. Proposed commit list
16. Items out of scope
17. Recommended next step

Checkpoint report at `docs/00-meta/implementation-reports/2026-04-19_phase-2c-checkpoint-report.md` — same template as Phase 2b checkpoint, with Phase 2c-specific sections for per-dataset summaries.

---

## 30. Before-implementation verification requirement

Same TD-006 discipline Phase 2b used: before any real network call, Phase 2c must WebFetch the relevant official Binance documentation pages, verify assumptions in §8, and **escalate** on any divergence instead of silently proceeding. Specifically:

- **GitHub `binance-public-data` README** — confirm presence/absence of bulk mark-price path and any funding bulk path.
- **`/fapi/v1/fundingRate` docs page** — confirm URL, params, response fields, weight, pagination semantics.
- **`/fapi/v1/exchangeInfo` docs page** — confirm URL, response shape (`symbols`, `serverTime`, `timezone`, `rateLimits`).
- **Direct fetch of one sample** for each endpoint — e.g., fetch `fundingRate?symbol=BTCUSDT&limit=2` to inspect the exact field names and types. This is the equivalent of Phase 2b's direct `.CHECKSUM` fetch that caught the GAP-010 header row.

Evidence blocks in each module's docstring record the verification URL + date + outcome, same format as `binance_bulk.py`.

---

## 31. Approval gates

Same cadence as Phase 1 / 2 / 2b:

1. **Gate 1 — plan approval (right now).**
2. **Gate 2 — pre-commit review.** After implementation, quality gates, and bounded real run.
3. **Optional Gate 3 — push / PR.**

No edits, no branch creation, no `uv sync`, no file writes, no WebFetch of Binance docs until Gate 1 is approved.

**Awaiting operator Gate 1 approval.**
