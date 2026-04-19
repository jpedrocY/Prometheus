# Phase 2c — Gate 2 Review

**Date:** 2026-04-19
**Phase:** 2c — Mark-Price Klines, Funding History, and Public Exchange Metadata
**Branch:** `phase-2c/public-market-data-completion` (off `main` at `731088f`, not pushed)
**Status:** Working-tree only. No commits yet. Awaiting operator Gate 2 approval.

---

## 1. Purpose

Gate 2 artifact for Phase 2c. Captures the implementation, TD-006 source verification for the three new public endpoints, the real bounded download run, quality-gate output, and the proposed commit structure.

**212 tests pass**; mypy clean on 25 source files; ruff + ruff format clean on 57 files. Real run completed all three datasets successfully with SHA256s matching WebFetch pre-captured values where applicable.

---

## 2. Operator conditions at Gate 1 (recap)

| # | Condition | Status |
| --- | --- | --- |
| 1 | Branch `phase-2c/public-market-data-completion` off clean main | **Satisfied.** |
| 2 | No new deps (beyond Phase 2b httpx) | **Satisfied.** `uv sync` shows 28 packages, same as Phase 2b. |
| 3 | Official-source verification before coding | **Satisfied.** 5 WebFetch calls to Binance docs + `data.binance.vision` CHECKSUM endpoints. See §3. |
| 4 | fundingRate 500/5min/IP shared limit correction | **Satisfied verbatim.** See §3.3 and `binance_rest.py` inline evidence. Default `pace_ms=1000`. |
| 5 | Network scope narrow: data.binance.vision + public /fapi/fundingRate + /fapi/exchangeInfo only | **Satisfied.** No other endpoints touched. No auth headers. |
| 6 | Initial real run: BTC+ETH mark-price 15m 2026-03, BTC+ETH funding 2026-03, one exchangeInfo snapshot | **Satisfied.** See §6. |
| 7 | Raw/normalized/state under git-ignored data/ | **Satisfied.** `git check-ignore` confirmed for 4 sampled paths. |
| 8 | Auth boundary: no auth in BinanceRestClient, mechanical guardrail test | **Satisfied.** `test_binance_rest_has_no_auth_surface` + `test_binance_rest_request_never_sends_auth_header` both pass. |
| 9 | Implementation scope bounded | **Satisfied.** Only approved modules added. No runtime/strategy/risk/etc. |
| 10 | Tests use MockTransport; no network | **Satisfied.** All 212 tests offline. |
| 11 | Ambiguity log + Gate 2 report under implementation-reports/ | **Satisfied.** GAPs 011–013 logged. |
| 12 | Stop before committing | **Satisfied.** No `git add`/`commit` performed. |

---

## 3. Official-source verification evidence (TD-006 extension)

Verified via WebFetch on 2026-04-19. Evidence blocks embedded in each module.

### 3.1 Bulk mark-price path

- URL: `https://data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYM>/<INTV>/<SYM>-<INTV>-<YYYY>-<MM>.zip`
- Checksum: `<zip>.CHECKSUM` with `<sha256hex>  <filename>` (two-space format identical to standard klines).
- Sample 2024-01 CHECKSUM fetch returned 90 bytes: `aa64b8b765a37c28f11235f2f2ff59f8558b9ff62251315de8b789a22698c926  BTCUSDT-15m-2024-01.zip` ✓
- 2026-03 target CHECKSUMs captured pre-run:
  - BTCUSDT: `79edfb409a35630cfb8894b883c2bcc4d5a3d6f78bf4d449585cc9e6e8f475e3`
  - ETHUSDT: `d30d71f35e0935783bedadcbc905537153c1e8980c1336a7c0403be12ba73762`
- CSV column layout: **undocumented in README** (confirmed); parser applies positional extraction + GAP-010-style header detection. Logged as GAP-013, resolved by runtime verification.

### 3.2 REST `/fapi/v1/fundingRate`

Verified via WebFetch of the official Get-Funding-Rate-History docs page:

- `GET /fapi/v1/fundingRate` at `https://fapi.binance.com`; public, no auth.
- Params (case-sensitive): `symbol` (STRING, opt), `startTime` (LONG ms, opt), `endTime` (LONG ms, opt), `limit` (INT, default 100, max 1000).
- Response: array of `{symbol STRING, fundingRate STRING decimal, fundingTime LONG ms, markPrice STRING decimal}`.
- Rate limit (verbatim): `"share 500/5min/IP rate limit with GET /fapi/v1/fundingInfo"` — logged as GAP-012.
- Pagination (verbatim): `"If the number of data between startTime and endTime is larger than limit, return as startTime + limit. In ascending order."`

### 3.3 REST `/fapi/v1/exchangeInfo`

Verified via WebFetch of the official Exchange-Information docs page:

- `GET /fapi/v1/exchangeInfo` at `https://fapi.binance.com`; public, no auth, no params.
- Weight: 1.
- Top-level fields: `timezone`, `serverTime`, `rateLimits`, `exchangeFilters`, `assets`, `symbols`.
- Per-symbol fields: 24 documented (subset modeled in `ExchangeInfoSnapshot.SymbolInfo` with `extra="ignore"`).
- Filter types: `PRICE_FILTER`, `LOT_SIZE`, `MARKET_LOT_SIZE`, `MAX_NUM_ORDERS`, `MIN_NOTIONAL`, `PERCENT_PRICE`.

### 3.4 Divergences

None triggered escalation. Mark-price CSV column layout was undocumented (expected; logged GAP-013) but parsed cleanly at runtime. All three real-run ingests completed without raising.

---

## 4. Commands run (in order)

```
# Pre-flight
uv --version                 → uv 0.11.7
python --version              → Python 3.12.4
git status --short            → clean except Gate 1 plan untracked
git rev-list --left-right     → 0  0

# Step 1
git checkout -b phase-2c/public-market-data-completion

# Step 2: env verify
uv sync                       → 28 packages (no new deps needed)

# Step 3: TD-006 WebFetch verification (no code yet)
WebFetch github.com/binance/binance-public-data  (mark-price column layout check → not documented)
WebFetch data.binance.vision/.../markPriceKlines/BTCUSDT/15m/2024-01.zip.CHECKSUM  (path pattern + format ✓)
WebFetch data.binance.vision/.../markPriceKlines/BTCUSDT/15m/2026-03.zip.CHECKSUM  (target exists)
WebFetch data.binance.vision/.../markPriceKlines/ETHUSDT/15m/2026-03.zip.CHECKSUM  (target exists)
WebFetch developer-docs Get-Funding-Rate-History page
WebFetch developer-docs Exchange-Information page

# Steps 4-10: write code + tests
# (core models; REST client; mark-price; funding-rate; exchangeInfo;
#  storage extensions; quality extensions; ingest extensions; __init__;
#  configs)

# Quality gates (pre-real-run)
uv run ruff check .           → 4 errors; fixed via Edit + ruff --fix
uv run ruff format .          → 13 files reformatted
uv run ruff format --check .  → 57 files already formatted
uv run mypy                   → Success: 25 source files
uv run pytest                 → 212 passed in 0.92s

# Step 11: real bounded run
uv run python -c <ingest script for all 3 datasets>  → SUCCESS

# Post-run disk + ignore verification
find data/ -type f            → 24 files (2.1 MB total)
git check-ignore <4 sampled paths>  → all ignored

# Gate 2 write-up
```

No destructive git. No `--force`. No `git add -f`. No commits. No push. No credentials.

---

## 5. `uv sync` summary

No new packages. `uv sync` rebuilt the editable `prometheus` package only:

```
Resolved 28 packages in 1ms
Prepared 1 package in 661ms
Installed 1 package in 5ms
 ~ prometheus==0.0.0 (from file:///C:/Prometheus)
```

Total environment: still 28 packages (httpx + friends from Phase 2b, pyarrow+duckdb+pydantic from Phase 2, dev deps from Phase 1).

---

## 6. Real bounded download — results

All three datasets ingested in a single `uv run python -c` invocation.

### 6.1 Mark-price 15m 2026-03

| Symbol | SHA256 | Rows | Pre-verified match |
| --- | --- | --- | --- |
| BTCUSDT | `79edfb409a35630cfb8894b883c2bcc4d5a3d6f78bf4d449585cc9e6e8f475e3` | 2976 | ✓ matches WebFetch |
| ETHUSDT | `d30d71f35e0935783bedadcbc905537153c1e8980c1336a7c0403be12ba73762` | 2976 | ✓ matches WebFetch |

- Both ZIPs checksum-verified by `BulkDownloader` before parsing.
- CSV layout (undocumented) confirmed as 12-column with positional extraction of the 6 meaningful fields.
- 2976 rows = 31 × 96 bars/day/symbol. Zero malformed rows.
- Manifests: `binance_usdm_btcusdt_markprice_15m__v001.manifest.json` (990 B), `binance_usdm_ethusdt_markprice_15m__v001.manifest.json` (990 B).

### 6.2 Funding-rate 2026-03

| Symbol | Event count | First funding_time | Last funding_time | Duration |
| --- | --- | --- | --- | --- |
| BTCUSDT | 93 | 2026-03-01T00:00:00Z | 2026-03-31T16:00:00Z | 31 days |
| ETHUSDT | 93 | 2026-03-01T00:00:00Z | 2026-03-31T16:00:00Z | 31 days |

- 93 events = 31 days × 3 per day (8-hour cadence). Expected exactly.
- Zero rate-limit errors. 1000ms pacing respected (per `fundingRate` 500/5min/IP shared limit).
- Pagination short-circuited (each symbol's 93 events fit in the first page of 1000).
- Manifests: `binance_usdm_btcusdt_funding__v001.manifest.json` (927 B), `binance_usdm_ethusdt_funding__v001.manifest.json` (927 B).

### 6.3 ExchangeInfo snapshot

- Single GET, HTTP 200.
- Raw body SHA256: `7657b7280f3a453018174ee3e2f86a807ed9cadfba7d3e10b51e57d36f4c2289`.
- Raw body size: 877,772 bytes (full exchange has ~500 perpetuals).
- Parsed + filtered to `{BTCUSDT, ETHUSDT}` → 2 `SymbolInfo` entries with tickSize/stepSize/minNotional filters populated.
- Server time: 1776628813962 ms = 2026-04-19T21:20:13Z (within seconds of local clock).
- Manifest-style artifacts:
  - Raw: `data/raw/binance_usdm/exchange_info/2026-04-19T21-22-59Z.json` (877,772 B)
  - Derived summary: `data/derived/exchange_info/2026-04-19T21-22-59Z.json` (2,073 B)

---

## 7. Disk footprint

| Artifact family | Count | Bytes |
| --- | --- | --- |
| Mark-price raw ZIPs | 2 | 161,841 |
| Standard-kline raw ZIPs (Phase 2b carryover) | 2 | 293,579 |
| ExchangeInfo raw JSON | 1 | 877,772 |
| Mark-price Parquet | 2 | 221,195 |
| Standard-kline Parquet (Phase 2b) | 2 | 371,834 |
| Funding-rate Parquet | 2 | 8,729 |
| 1h derived Parquet (Phase 2b) | 2 | 101,428 |
| ExchangeInfo derived JSON | 1 | 2,073 |
| Manifests | 8 | 7,506 |
| Download state | 2 | 1,550 |
| **Total** | **24** | **~2.1 MB** |

All 24 artifacts confirmed git-ignored. `git check-ignore` matched all 4 sampled paths (raw ZIP, mark-price Parquet, funding Parquet, exchangeInfo JSON).

---

## 8. Files changed

### 8.1 Tracked files modified (8)

```
configs/dev.example.yaml                       +23 lines  (mark_price + funding + exchange_info subkeys)
docs/00-meta/implementation-ambiguity-log.md   +64 lines  (GAP-011, GAP-012, GAP-013)
src/prometheus/core/__init__.py                +18 lines  (3 new models re-exported)
src/prometheus/research/data/__init__.py       +57 lines  (new names re-exported)
src/prometheus/research/data/binance_bulk.py   +53 lines  (BulkFamily StrEnum + family-aware URLs/partition)
src/prometheus/research/data/ingest.py        +208 lines  (ingest_mark_price_monthly_range, ingest_funding_range)
src/prometheus/research/data/quality.py        +70 lines  (funding-rate checks)
src/prometheus/research/data/storage.py       +262 lines  (mark-price + funding-rate schemas + I/O)
```

Total: **+747 insertions, −8 deletions** across 8 tracked files.

### 8.2 Untracked new files (15)

```
docs/00-meta/implementation-reports/2026-04-19_phase-2c_gate-1-plan.md
docs/00-meta/implementation-reports/2026-04-19_phase-2c_gate-2-review.md        ← this file
src/prometheus/core/events.py
src/prometheus/core/exchange_info.py
src/prometheus/core/mark_price_klines.py
src/prometheus/research/data/binance_rest.py
src/prometheus/research/data/exchange_info.py
src/prometheus/research/data/funding_rate.py
src/prometheus/research/data/mark_price.py
tests/unit/core/test_events.py
tests/unit/core/test_exchange_info.py
tests/unit/core/test_mark_price_klines.py
tests/unit/research/data/test_binance_rest.py
tests/unit/research/data/test_exchange_info.py
tests/unit/research/data/test_funding_rate.py
tests/unit/research/data/test_mark_price.py
```

---

## 9. `git status` / `diff --stat`

```
$ git status --short
 M configs/dev.example.yaml
 M docs/00-meta/implementation-ambiguity-log.md
 M src/prometheus/core/__init__.py
 M src/prometheus/research/data/__init__.py
 M src/prometheus/research/data/binance_bulk.py
 M src/prometheus/research/data/ingest.py
 M src/prometheus/research/data/quality.py
 M src/prometheus/research/data/storage.py
?? docs/00-meta/implementation-reports/2026-04-19_phase-2c_gate-1-plan.md
?? docs/00-meta/implementation-reports/2026-04-19_phase-2c_gate-2-review.md
?? src/prometheus/core/events.py
?? src/prometheus/core/exchange_info.py
?? src/prometheus/core/mark_price_klines.py
?? src/prometheus/research/data/binance_rest.py
?? src/prometheus/research/data/exchange_info.py
?? src/prometheus/research/data/funding_rate.py
?? src/prometheus/research/data/mark_price.py
?? tests/unit/core/test_events.py
?? tests/unit/core/test_exchange_info.py
?? tests/unit/core/test_mark_price_klines.py
?? tests/unit/research/data/test_binance_rest.py
?? tests/unit/research/data/test_exchange_info.py
?? tests/unit/research/data/test_funding_rate.py
?? tests/unit/research/data/test_mark_price.py
```

No `uv.lock` change (no new deps). No `pyproject.toml` change.

---

## 10. Quality-gate results

```
$ uv run ruff check .
All checks passed!

$ uv run ruff format --check .
57 files already formatted

$ uv run mypy
Success: no issues found in 25 source files

$ uv run pytest
........................................................................ [ 33%]
........................................................................ [ 67%]
....................................................................     [100%]
212 passed in 0.92s
```

Test-count evolution: 2 (Phase 1) → 79 (Phase 2) → 136 (Phase 2b) → **212** (Phase 2c, +76 new).

New tests by module:
- `test_mark_price_klines.py` — 9
- `test_events.py` — 10
- `test_exchange_info.py` (core) — 8
- `test_binance_rest.py` — 13 (includes the 2 auth-surface guardrails)
- `test_mark_price.py` — 15
- `test_funding_rate.py` — 12
- `test_exchange_info.py` (research/data) — 9

Total: **76 new tests** in Phase 2c.

### Auth-surface mechanical guardrails (per Gate 1 condition 8)

```python
def test_binance_rest_has_no_auth_surface() -> None:
    # Fails the build if api_key, secret, sign_request, etc. ever appear
    # on BinanceRestClient or its __init__ signature.

def test_binance_rest_request_never_sends_auth_header() -> None:
    # Verifies no X-MBX-APIKEY or Authorization header on outgoing requests.
```

Both pass.

---

## 11. Quality-check results on real data

| Check | Mark-price BTC | Mark-price ETH | Funding BTC | Funding ETH | ExchangeInfo |
| --- | --- | --- | --- | --- | --- |
| SHA256 matches pre-verified | ✓ | ✓ | N/A (REST) | N/A (REST) | ✓ recorded in manifest |
| Expected row count | ✓ 2976 | ✓ 2976 | ✓ 93 | ✓ 93 | ✓ 2 symbols matched |
| Model-level invariants | pass | pass | pass | pass | pass |
| Duplicates | 0 | 0 | 0 | 0 | N/A |
| Non-monotonic | 0 | 0 | 0 | 0 | N/A |
| Missing bars | 0 | 0 | N/A | N/A | N/A |
| Required symbols present | N/A | N/A | N/A | N/A | ✓ |

Zero data-quality issues across all three datasets.

---

## 12. Safety checklist

| Check | Result |
| --- | --- |
| Production Binance API keys | **Not created, not requested, not used.** |
| Real secrets / `.env` | **None touched.** |
| Exchange-write capability | **None.** Only GETs to data.binance.vision + fapi.binance.com public endpoints. |
| Signed requests | **None.** No HMAC code, no `X-MBX-APIKEY`. Mechanically tested. |
| Account-authenticated endpoints | **Not touched.** `leverageBracket`, `commissionRate`, `/fapi/v1/account/*`, all deferred. |
| WebSockets / user-stream | **None.** |
| Third-party market-data sources | **None.** |
| `.mcp.json` / Graphify | **Not created / not enabled.** |
| Real data committed | **None** — all 24 artifacts under git-ignored `data/`. |
| `.claude/*` / `CLAUDE.md` / current-project-state | **Not modified.** |
| `docs/12-roadmap/technical-debt-register.md` | **Not modified** (per operator directive; TD-006 remains OPEN). |
| Runtime DB | **Not touched.** |
| Destructive git / `git add -f` | **None.** |
| Dependencies added | **None.** No `pyproject.toml` / `uv.lock` changes. |
| Network during tests | **Zero.** `httpx.MockTransport` for all 212 tests. Real downloads only via explicit `uv run python -c` invocation. |

---

## 13. Ambiguity-log entries (Phase 2c)

Appended to `docs/00-meta/implementation-ambiguity-log.md`:

| ID | Status | Summary |
| --- | --- | --- |
| GAP-20260419-011 | **RESOLVED** | `DatasetManifest` accepts `intervals=()` for event-type datasets (funding). |
| GAP-20260419-012 | **RESOLVED** | Binance `fundingRate` shares `500/5min/IP` rate limit with `fundingInfo`; Phase 2c paces at 1000ms (40% margin). |
| GAP-20260419-013 | **RESOLVED** | Mark-price bulk CSV column layout is undocumented in the README; parsed positionally with defensive header detection; real ZIP SHA256s match WebFetch pre-captured values. |

No HIGH-risk GAPs raised during execution. No operator escalations triggered beyond the initial Gate 1 approval.

---

## 14. Phase 2c Gate 1 acceptance-criteria self-check

Per Phase 2c Gate 1 plan §F:

| Criterion | Result |
| --- | --- |
| Historical mark-price path reproducible | **Pass** — BulkDownloader with family=MARK_PRICE_KLINES; SHA256-verified; Hive-partitioned Parquet; round-trippable. |
| Funding-rate history captured for BTC+ETH 2026-03 | **Pass** — 93 events each; manifest-tracked; Parquet persistence. |
| ExchangeInfo snapshot parseable with BTC+ETH metadata | **Pass** — raw + derived JSON; SHA256 recorded; filters extracted. |
| Auth boundary strictly preserved | **Pass** — mechanical negative-hasattr test + header test. |
| TD-006 partial-resolution expanded | **Pass** — bulk mark-price, fundingRate REST, exchangeInfo REST all verified and documented inline. |
| No credential path, no signed requests | **Pass.** |
| `configs/dev.example.yaml` documentation-only | **Pass.** 23 new lines; no loader consumes them. |

---

## 15. Proposed commit structure

Five small commits + post-Gate-2 checkpoint, same Phase 2/2b cadence.

| # | Title | Files |
| --- | --- | --- |
| 1 | `phase-2c: core data models (MarkPriceKline, FundingRateEvent, ExchangeInfoSnapshot)` | `src/prometheus/core/{mark_price_klines,events,exchange_info,__init__}.py`, `tests/unit/core/test_{mark_price_klines,events,exchange_info}.py` |
| 2 | `phase-2c: public GET-only REST client with auth-surface guardrails` | `src/prometheus/research/data/binance_rest.py`, `tests/unit/research/data/test_binance_rest.py` |
| 3 | `phase-2c: bulk mark-price + BulkFamily refactor + mark-price tests` | `src/prometheus/research/data/binance_bulk.py`, `src/prometheus/research/data/mark_price.py`, `tests/unit/research/data/test_mark_price.py` |
| 4 | `phase-2c: funding-rate REST + exchangeInfo REST + ingest orchestrators + storage/quality extensions` | `src/prometheus/research/data/{funding_rate,exchange_info,ingest,storage,quality,__init__}.py`, `tests/unit/research/data/test_{funding_rate,exchange_info}.py`, `configs/dev.example.yaml` |
| 5 | `phase-2c: ambiguity log + Gate-1/Gate-2 reports` | `docs/00-meta/implementation-ambiguity-log.md`, both Phase 2c implementation-reports docs |
| 6 (post-Gate-2) | `phase-2c: checkpoint report` | Checkpoint report. |

No push. No PR during execution. Operator decides when to merge.

---

## 16. Items explicitly out of scope (confirmed untouched)

- `CLAUDE.md`, `README.md`, `docs/00-meta/current-project-state.md`, `docs/12-roadmap/technical-debt-register.md`
- All specialist docs under `docs/03-*` through `docs/11-*` (except the ambiguity log appended)
- `.claude/` (agents, rules, settings)
- `.mcp.example.json`, `.mcp.graphify.template.json`, `.mcp.json` (last not created)
- `research/`, `infra/`, `notebooks/` top-level directories
- `pyproject.toml`, `uv.lock` (no new deps)
- No leverageBracket, commissionRate, or any `/fapi/v1/account/*` code
- No strategy/risk/execution/exchange-adapter/persistence/operator/runtime/dashboard modules introduced

---

## 17. Recommended next step

Two viable paths (operator decides).

1. **Phase 3 — Backtesting and Strategy Conformance.** All four public data foundations now in place:
   - Standard 15m klines (Phase 2 + 2b)
   - Derived 1h bars (Phase 2)
   - Mark-price 15m klines (Phase 2c) — for realistic stop-hit modeling
   - Funding-rate events (Phase 2c) — for funding-cost accounting
   - ExchangeInfo (Phase 2c) — for tick/step/minNotional rounding
   Phase 3 can begin with 2026-03 real data + synthetic fixtures.

2. **Phase 2d — authenticated public-account data (leverageBracket, commissionRate).** Requires credential gate opening. Lower priority; Phase 3 can use placeholder commission values until Phase 2d lands.

Phase 3 is the natural next step given Phase 2c closes the public-data loop.

**Awaiting operator Gate 2 approval.**
