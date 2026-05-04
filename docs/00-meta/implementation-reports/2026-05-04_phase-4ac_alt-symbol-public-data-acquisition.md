# Phase 4ac — Alt-Symbol Public Data Acquisition and Integrity Validation

**Authority:** Operator authorization for Phase 4ac (docs-and-data acquisition / integrity-validation phase translating Phase 4ab's data-requirements / feasibility plan into actual public unauthenticated alt-symbol dataset acquisition on Binance USDⓈ-M perpetuals). Phase 4ab (alt-symbol data-requirements / feasibility memo); Phase 4aa (alt-symbol market-selection / admissibility memo); Phase 4i (V2 acquisition pattern: standalone-script discipline; manifest convention; SHA256 verification); Phase 3q (5m supplemental + mark-price acquisition pattern; mark-price gap precedent); Phase 3p §4.7 (strict integrity gate); Phase 3r §8 (mark-price gap governance); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/04-data/historical-data-spec.md`; `docs/04-data/dataset-versioning.md`; `docs/04-data/timestamp-policy.md`; `docs/04-data/data-requirements.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4ac — **Alt-Symbol Public Data Acquisition and Integrity Validation** (docs-and-data, standalone-script mode). Acquired the predeclared Phase 4ab core alt-symbol public datasets from public unauthenticated `data.binance.vision` bulk archives only. **No backtest. No diagnostics. No strategy spec. No implementation. No live-readiness. No exchange-write.** **No authenticated API. No private endpoint. No public-endpoint code call. No user stream / WebSocket / listenKey. No credentials. No `.env`. No MCP / Graphify / `.mcp.json`.** No retained verdict revised. No project lock changed. No governance file amended (beyond the narrow `docs/00-meta/current-project-state.md` update). No successor phase authorized.

**Branch:** `phase-4ac/alt-symbol-public-data-acquisition`. **Phase date:** 2026-05-04 UTC.

---

## 1. Purpose

Phase 4ac is **docs-and-data acquisition / integrity validation only.** Phase 4ac translates the completed Phase 4ab data-requirements / feasibility memo into actual public unauthenticated bulk-archive acquisition for the predeclared core alt-symbol set on Binance USDⓈ-M perpetuals.

**Phase 4ac does NOT:**

- run any backtest;
- run any diagnostic;
- rerun Q1–Q7;
- create a new strategy candidate;
- create a hypothesis-spec memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- implement runtime code;
- imply live-readiness;
- enable exchange-write.

Phase 4ac records what data is now research-eligible, what failed strict integrity gates, and what feasibility implications follow. It is data evidence only. **Phase 4ac results are NOT adopted as binding governance.**

## 2. Authorization and Boundaries

- **Operator authorization:** Phase 4ac brief, 2026-05-04. Authorized scope is the Phase 4ab-recommended core symbol set + REQUIRED kline / mark-price / funding families with strict integrity gates and a fallback end-month policy.
- **Public unauthenticated only.** Source: `data.binance.vision` monthly bulk archives. SHA256 verification against paired `.CHECKSUM` companion files. **No credentials.** **No `.env`.** **No authenticated REST.** **No private endpoint.** **No public-endpoint code call.** **No user stream / WebSocket / listenKey.** **No exchange-write.** **No MCP / Graphify / `.mcp.json`.**
- **No patching / forward-fill / interpolation / imputation.** Strict integrity per Phase 3p §4.7 / Phase 3r §8 / Phase 4h §17 precedent. Failed gates produce `research_eligible: false` manifests recorded verbatim.
- **No modification of existing committed manifests.** Phase 4ac skips any (symbol, family, interval) where a `data/manifests/<dataset_version>.manifest.json` file already exists.
- **No metrics / OI acquisition.** Deferred per Phase 4ab §6.D.
- **No aggTrades / tick / order-book.** Deferred per Phase 4ab §6.E.
- **No exchange metadata acquisition.** Source-scope-restricted; would require live public REST endpoint not currently authorized for Phase 4ac. Recorded as not-acquired finding per §8.

## 3. Scope

### Core symbol set (acquired)

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

### Deferred secondary watchlist (NOT acquired)

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

### Data families and intervals

| Family | Intervals | Status |
| --- | --- | --- |
| Standard trade-price klines | 15m / 30m / 1h / 4h | REQUIRED — acquired |
| Mark-price klines | 15m / 30m / 1h / 4h | CONDITIONAL REQUIRED — acquired |
| Funding-rate history (monthly) | per-symbol | REQUIRED — acquired |
| Metrics / open-interest | n/a | DEFERRED — NOT acquired |
| AggTrades / tick / order-book | n/a | DEFERRED / FORBIDDEN — NOT acquired |
| Exchange metadata snapshots | n/a | NOT acquired (source-scope-restricted; see §8) |

### Date range

- **Start:** 2022-01-01 UTC.
- **End:** 2026-04-30 UTC.
- **End-month probe outcome:** BTCUSDT 15m kline `.CHECKSUM` companion for 2026-04 was available on `data.binance.vision`. End month accepted at 2026-04 (no fallback to 2026-03 needed).
- **No partial 2026-05.** No fabricated months.

### Skip-if-already-covered (no manifest modification)

For BTCUSDT and ETHUSDT, some `__v001` manifests already exist from Phase 2 / Phase 3q / Phase 4i. Phase 4ac skipped 10 (symbol, family, interval) entries with existing manifests:

```text
SKIP BTCUSDT klines 15m              (manifest_exists; Phase 2 v001/v002)
SKIP BTCUSDT klines 30m              (manifest_exists; Phase 4i v001)
SKIP BTCUSDT klines 4h               (manifest_exists; Phase 4i v001)
SKIP BTCUSDT markPriceKlines 15m     (manifest_exists; Phase 2 v001/v002)
SKIP BTCUSDT fundingRate             (manifest_exists; Phase 2 v001/v002)
SKIP ETHUSDT klines 15m              (manifest_exists; Phase 2 v001/v002)
SKIP ETHUSDT klines 30m              (manifest_exists; Phase 4i v001)
SKIP ETHUSDT klines 4h               (manifest_exists; Phase 4i v001)
SKIP ETHUSDT markPriceKlines 15m     (manifest_exists; Phase 2 v001/v002)
SKIP ETHUSDT fundingRate             (manifest_exists; Phase 2 v001/v002)
```

35 (symbol, family, interval) entries acquired by Phase 4ac:

```text
PLAN BTCUSDT klines 1h
PLAN BTCUSDT markPriceKlines 30m
PLAN BTCUSDT markPriceKlines 1h
PLAN BTCUSDT markPriceKlines 4h
PLAN ETHUSDT klines 1h
PLAN ETHUSDT markPriceKlines 30m
PLAN ETHUSDT markPriceKlines 1h
PLAN ETHUSDT markPriceKlines 4h
PLAN SOLUSDT klines {15m, 30m, 1h, 4h}
PLAN SOLUSDT markPriceKlines {15m, 30m, 1h, 4h}
PLAN SOLUSDT fundingRate
PLAN XRPUSDT klines {15m, 30m, 1h, 4h}
PLAN XRPUSDT markPriceKlines {15m, 30m, 1h, 4h}
PLAN XRPUSDT fundingRate
PLAN ADAUSDT klines {15m, 30m, 1h, 4h}
PLAN ADAUSDT markPriceKlines {15m, 30m, 1h, 4h}
PLAN ADAUSDT fundingRate
```

## 4. Acquisition Method

- **Public source path family:** `https://data.binance.vision/data/futures/um/monthly/{klines|markPriceKlines|fundingRate}/<SYMBOL>/[<INTERVAL>/]<SYMBOL>-<INTERVAL|fundingRate>-YYYY-MM.zip`.
- **Pairwise SHA256 verification** against `.CHECKSUM` companion files. Mismatch fails closed.
- **No authenticated APIs. No private endpoints. No public-endpoint code call. No WebSocket. No user stream. No listenKey lifecycle.**
- **Concurrency:** 8 workers; 50 ms inter-request pacing; 5 retries with exponential backoff (1.0 → 30.0 s cap).
- **Idempotent:** existing raw archives with valid SHA256 are not re-downloaded.

### Script

- **Path:** `scripts/phase4ac_alt_symbol_acquisition.py` (committed; new).
- **Pattern:** Standalone orchestrator. Imports: `argparse`, `dataclasses`, `hashlib`, `io`, `json`, `sys`, `threading`, `time`, `zipfile`, `concurrent.futures`, `datetime`, `pathlib`, `httpx`, `pyarrow`, `pyarrow.parquet`. **No** `prometheus.runtime` / `prometheus.execution` / `prometheus.persistence` / `prometheus.research.data.*` imports. **No** Binance private clients. **No** authenticated REST. **No** WebSocket. **No** `requests` / `aiohttp` / `urllib3` / `urllib.request` / `websockets` / `websocket` imports.
- **Quality:** ruff clean; py compileall clean.

### Storage layout

- **Raw archives** (gitignored): `data/raw/binance_usdm/{klines|markPriceKlines|fundingRate}/symbol=X/[interval=Y/]year=YYYY/month=MM/X-...-YYYY-MM.zip`
- **Normalized Parquet** (gitignored): `data/normalized/{klines|markprice_klines|funding}/symbol=X/[interval=Y/]year=YYYY/month=MM/part-0000.parquet`
- **Manifests** (committed): `data/manifests/<dataset_version>.manifest.json`

## 5. Dataset Inventory

35 manifests written. All 35 are committed under `data/manifests/`.

| # | Symbol | Family | Interval | Bars/Records | Months acquired | Months 404 | Middle gaps | Gaps detected | research_eligible | Manifest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BTCUSDT | klines | 1h | 37 944 | 52 | 0 | 0 | 0 | **true** | binance_usdm_btcusdt_1h__v001 |
| 2 | BTCUSDT | markPriceKlines | 30m | 75 744 | 52 | 0 | 0 | 3 | false | binance_usdm_btcusdt_markprice_30m__v001 |
| 3 | BTCUSDT | markPriceKlines | 1h | 37 872 | 52 | 0 | 0 | 3 | false | binance_usdm_btcusdt_markprice_1h__v001 |
| 4 | BTCUSDT | markPriceKlines | 4h | 9 468 | 52 | 0 | 0 | 3 | false | binance_usdm_btcusdt_markprice_4h__v001 |
| 5 | ETHUSDT | klines | 1h | 37 944 | 52 | 0 | 0 | 0 | **true** | binance_usdm_ethusdt_1h__v001 |
| 6 | ETHUSDT | markPriceKlines | 30m | 75 792 | 52 | 0 | 0 | 2 | false | binance_usdm_ethusdt_markprice_30m__v001 |
| 7 | ETHUSDT | markPriceKlines | 1h | 37 896 | 52 | 0 | 0 | 2 | false | binance_usdm_ethusdt_markprice_1h__v001 |
| 8 | ETHUSDT | markPriceKlines | 4h | 9 474 | 52 | 0 | 0 | 2 | false | binance_usdm_ethusdt_markprice_4h__v001 |
| 9 | SOLUSDT | klines | 15m | 151 296 | 52 | 0 | 0 | 2 | false | binance_usdm_solusdt_15m__v001 |
| 10 | SOLUSDT | klines | 30m | 75 648 | 52 | 0 | 0 | 2 | false | binance_usdm_solusdt_30m__v001 |
| 11 | SOLUSDT | klines | 1h | 37 824 | 52 | 0 | 0 | 2 | false | binance_usdm_solusdt_1h__v001 |
| 12 | SOLUSDT | klines | 4h | 9 456 | 52 | 0 | 0 | 2 | false | binance_usdm_solusdt_4h__v001 |
| 13 | SOLUSDT | markPriceKlines | 15m | 151 583 | 52 | 0 | 0 | 3 | false | binance_usdm_solusdt_markprice_15m__v001 |
| 14 | SOLUSDT | markPriceKlines | 30m | 75 792 | 52 | 0 | 0 | 2 | false | binance_usdm_solusdt_markprice_30m__v001 |
| 15 | SOLUSDT | markPriceKlines | 1h | 37 896 | 52 | 0 | 0 | 2 | false | binance_usdm_solusdt_markprice_1h__v001 |
| 16 | SOLUSDT | markPriceKlines | 4h | 9 474 | 52 | 0 | 0 | 2 | false | binance_usdm_solusdt_markprice_4h__v001 |
| 17 | SOLUSDT | fundingRate | — | 4 818 | 52 | 0 | 0 | n/a | **true** | binance_usdm_solusdt_funding__v001 |
| 18 | XRPUSDT | klines | 15m | 151 296 | 52 | 0 | 0 | 2 | false | binance_usdm_xrpusdt_15m__v001 |
| 19 | XRPUSDT | klines | 30m | 75 648 | 52 | 0 | 0 | 2 | false | binance_usdm_xrpusdt_30m__v001 |
| 20 | XRPUSDT | klines | 1h | 37 824 | 52 | 0 | 0 | 2 | false | binance_usdm_xrpusdt_1h__v001 |
| 21 | XRPUSDT | klines | 4h | 9 456 | 52 | 0 | 0 | 2 | false | binance_usdm_xrpusdt_4h__v001 |
| 22 | XRPUSDT | markPriceKlines | 15m | 151 583 | 52 | 0 | 0 | 3 | false | binance_usdm_xrpusdt_markprice_15m__v001 |
| 23 | XRPUSDT | markPriceKlines | 30m | 75 792 | 52 | 0 | 0 | 2 | false | binance_usdm_xrpusdt_markprice_30m__v001 |
| 24 | XRPUSDT | markPriceKlines | 1h | 37 896 | 52 | 0 | 0 | 2 | false | binance_usdm_xrpusdt_markprice_1h__v001 |
| 25 | XRPUSDT | markPriceKlines | 4h | 9 474 | 52 | 0 | 0 | 2 | false | binance_usdm_xrpusdt_markprice_4h__v001 |
| 26 | XRPUSDT | fundingRate | — | 4 743 | 52 | 0 | 0 | n/a | **true** | binance_usdm_xrpusdt_funding__v001 |
| 27 | ADAUSDT | klines | 15m | 151 776 | 52 | 0 | 0 | 0 | **true** | binance_usdm_adausdt_15m__v001 |
| 28 | ADAUSDT | klines | 30m | 75 888 | 52 | 0 | 0 | 0 | **true** | binance_usdm_adausdt_30m__v001 |
| 29 | ADAUSDT | klines | 1h | 37 944 | 52 | 0 | 0 | 0 | **true** | binance_usdm_adausdt_1h__v001 |
| 30 | ADAUSDT | klines | 4h | 9 486 | 52 | 0 | 0 | 0 | **true** | binance_usdm_adausdt_4h__v001 |
| 31 | ADAUSDT | markPriceKlines | 15m | 151 583 | 52 | 0 | 0 | 3 | false | binance_usdm_adausdt_markprice_15m__v001 |
| 32 | ADAUSDT | markPriceKlines | 30m | 75 792 | 52 | 0 | 0 | 2 | false | binance_usdm_adausdt_markprice_30m__v001 |
| 33 | ADAUSDT | markPriceKlines | 1h | 37 896 | 52 | 0 | 0 | 2 | false | binance_usdm_adausdt_markprice_1h__v001 |
| 34 | ADAUSDT | markPriceKlines | 4h | 9 474 | 52 | 0 | 0 | 2 | false | binance_usdm_adausdt_markprice_4h__v001 |
| 35 | ADAUSDT | fundingRate | — | 4 743 | 52 | 0 | 0 | n/a | **true** | binance_usdm_adausdt_funding__v001 |

**SHA256 verification:** every monthly archive verified against `.CHECKSUM` companion. Zero checksum mismatches.
**Months 404:** zero across all 35 families. Every requested 2022-01..2026-04 archive was available.

## 6. Integrity Results

### PASS (research_eligible: true) — 9 of 35 families

| Symbol | Family | Interval | Notes |
| --- | --- | --- | --- |
| BTCUSDT | klines | 1h | clean; 0 gaps |
| ETHUSDT | klines | 1h | clean; 0 gaps |
| ADAUSDT | klines | 15m / 30m / 1h / 4h | clean; 0 gaps; full 2022-01..2026-04 coverage |
| SOLUSDT | fundingRate | — | clean; 4 818 funding events |
| XRPUSDT | fundingRate | — | clean; 4 743 funding events |
| ADAUSDT | fundingRate | — | clean; 4 743 funding events |

### FAIL (research_eligible: false) — 26 of 35 families

| Failure pattern | Affected families |
| --- | --- |
| 3 BTCUSDT mark-price gaps (2022-07-31 + 2022-10-02 + 2023-02-24) | BTCUSDT mark-price 30m / 1h / 4h |
| 2 ETHUSDT mark-price gaps (2022-10-02 + 2023-02-24) | ETHUSDT mark-price 30m / 1h / 4h |
| 2 SOLUSDT trade-price kline gaps (2022-02-26 + 2022-04-01) | SOLUSDT klines 15m / 30m / 1h / 4h |
| 2 SOLUSDT mark-price gaps (2022-10-02 + 2023-02-24) plus 1 extra at 15m (2023-11-10) | SOLUSDT mark-price 15m / 30m / 1h / 4h |
| 2 XRPUSDT trade-price kline gaps (2022-02-26 + 2022-04-01) | XRPUSDT klines 15m / 30m / 1h / 4h |
| 2 XRPUSDT mark-price gaps (2022-10-02 + 2023-02-24) plus 1 extra at 15m (2023-11-10) | XRPUSDT mark-price 15m / 30m / 1h / 4h |
| 2 ADAUSDT mark-price gaps (2022-10-02 + 2023-02-24) plus 1 extra at 15m (2023-11-10) | ADAUSDT mark-price 15m / 30m / 1h / 4h |

**Strict gate semantics preserved:** `research_eligible: false` for every family with even one gap. **No patching, no forward-fill, no interpolation, no imputation, no silent omission, no Phase 3p §4.7 relaxation.** All gap windows recorded verbatim in the affected manifests' `quality_checks.gap_locations` and `invalid_windows`.

## 7. Invalid Windows and Gaps

### BTC / ETH / SOL / XRP / ADA mark-price gaps (consistent across symbols within each gap window)

These match the previously-documented Phase 3q / Phase 3r §8 mark-price invalid-window pattern. They are upstream Binance maintenance windows where mark-price data is unavailable in `data.binance.vision` bulk archives.

| Gap window (UTC) | Symbols affected (mark-price) |
| --- | --- |
| 2022-07-30 23:30 .. 2022-08-01 00:00 | BTC only |
| 2022-10-01 23:30 .. 2022-10-03 00:00 | BTC, ETH, SOL, XRP, ADA |
| 2023-02-23 23:30 .. 2023-02-25 00:00 | BTC, ETH, SOL, XRP, ADA |
| 2023-11-10 03:30 .. 2023-11-10 04:00 | SOL, XRP, ADA (visible only at 15m granularity; submerged inside other-interval bars at 30m/1h/4h) |

**Phase 3r §8 mark-price gap governance preserved.** Gap windows are exclusion zones, not patch zones. No Phase 4ac action is required; any future research that uses mark-price datasets must apply the Phase 3r §8 per-trade or per-bar exclusion rule and would need a separately authorized Phase 3r §8-equivalent governance decision.

### SOL / XRP early-2022 trade-price kline gaps

A previously-undocumented (in the project record) per-symbol early-2022 trade-price kline gap pattern is now visible for SOL and XRP:

| Gap window (UTC) | Symbols affected (trade-price klines) |
| --- | --- |
| 2022-02-25 23:45 .. 2022-03-01 00:00 (≈ 2 days) | SOL, XRP |
| 2022-03-31 23:45 .. 2022-04-03 00:00 (≈ 2 days) | SOL, XRP |

ADA does NOT exhibit these gaps (ADA klines pass strict gate at all four intervals). BTC and ETH klines were not re-acquired by Phase 4ac (Phase 2 / Phase 4i v001 manifests already cover them with no comparable gap pattern reported).

This is a **factual finding from Phase 4ac**, not a project verdict. It does not by itself preclude future research on SOL or XRP — a separately authorized governance memo (analogous to Phase 3r §8 / Phase 4j §11) could specify a per-trade or per-bar exclusion rule for these windows. **Phase 4ac does NOT propose such a rule.**

## 8. Source Availability Findings

### 2026-04 availability

The end-month probe confirmed that `BTCUSDT-15m-2026-04.zip.CHECKSUM` was available at `data.binance.vision`. End month accepted at 2026-04. **No fallback to 2026-03 was needed.** All 35 families covered through 2026-04 inclusive.

### Funding archive availability

Funding-rate monthly bulk archives at `data.binance.vision/data/futures/um/monthly/fundingRate/<symbol>/` were available for all three new symbols (SOL, XRP, ADA) for the full 2022-01..2026-04 window. **No fallback to authenticated REST was needed.** Funding family is research-eligible for all three new symbols.

### Mark-price archive availability

Mark-price monthly bulk archives at `data.binance.vision/data/futures/um/monthly/markPriceKlines/<symbol>/<interval>/` were available for all four newly-acquired (symbol, interval) combinations across all 52 months. The **content** has known invalid windows (per §7), but the **archives themselves** are present.

### Exchange metadata snapshots

**Not acquired in Phase 4ac.** Binance USDⓈ-M exchange-info is published via the public REST endpoint `GET /fapi/v1/exchangeInfo` rather than as a `data.binance.vision` bulk archive. Phase 4ac brief restricted source scope to `data.binance.vision` bulk archives ("Use public `data.binance.vision` bulk archives only where possible"; "If only live public REST endpoint is available: Do NOT call it unless it is clearly public unauthenticated and the repository acquisition policy permits it; Prefer documenting metadata as 'not acquired in Phase 4ac due to source-scope restriction' rather than expanding source scope"). Phase 4ac honors that restriction. Exchange metadata is recorded as a feasibility-finding gap; future authorized phases could acquire it through a separately scoped pathway.

## 9. Storage and Reproducibility

- **Raw data:** `data/raw/binance_usdm/...` (gitignored; 189.0 MiB local; 1 820 monthly archives acquired by Phase 4ac, plus archives retained from prior phases).
- **Normalized data:** `data/normalized/{klines|markprice_klines|funding}/...` (gitignored; 257.6 MiB local; ~257 MiB Phase 4ac-attributable, with prior phases sharing the directory).
- **Total local footprint** (across all phases combined): ~447 MiB. Reproducible by re-running the orchestrator script with the same date range.
- **Archives on disk total:** 5 534 (includes Phase 3q + Phase 4i + Phase 4ac).
- **Phase 4ac archives acquired:** 35 families × 52 months = **1 820 monthly archives**, all SHA256-verified.
- **Manifests committed:** 35 (under `data/manifests/`).
- **Script committed:** `scripts/phase4ac_alt_symbol_acquisition.py`.

### Reproduction command

```text
.venv/Scripts/python scripts/phase4ac_alt_symbol_acquisition.py --workers 8
```

(Defaults to symbols BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT/ADAUSDT; start 2022-01; end probe 2026-04 with fallback 2026-03.)

## 10. Feasibility Implications

This section discusses **data feasibility only**. It does NOT infer that alt symbols are better or worse for strategy research. It does NOT infer strategy verdicts. It does NOT propose or rescue any strategy.

### Now research-eligible (PASS)

- **BTCUSDT 1h direct trade-price klines** (Phase 4ac NEW): adds 1h direct kline support alongside the existing 1h_derived__v002 family.
- **ETHUSDT 1h direct trade-price klines** (Phase 4ac NEW): symmetric to BTC.
- **ADAUSDT 15m / 30m / 1h / 4h trade-price klines** (Phase 4ac NEW): full ADA trade-price kline coverage 2022-01..2026-04.
- **SOLUSDT / XRPUSDT / ADAUSDT funding rate history** (Phase 4ac NEW): three new alt-symbol funding families, each with 52 monthly archives and ~4 700–4 800 funding events.

### Not research-eligible (FAIL)

- **BTCUSDT mark-price 30m / 1h / 4h:** known mark-price upstream gaps (per Phase 3q / Phase 3r §8 precedent). Future research that requires BTC mark-price at these intervals would need a separately authorized Phase 3r §8-equivalent governance memo specifying a per-bar exclusion rule.
- **ETHUSDT mark-price 30m / 1h / 4h:** symmetric to BTC.
- **SOLUSDT / XRPUSDT trade-price klines (all four intervals):** two early-2022 archive gaps (Feb 26 and Apr 1, 2022). Future research would need either a separate governance memo for per-bar exclusion, or restriction to a 2022-04-03-onward research window.
- **SOLUSDT / XRPUSDT / ADAUSDT mark-price klines (all four intervals each):** same upstream mark-price gaps as BTC / ETH at 2022-10-02 and 2023-02-24, plus a 2023-11-10 gap visible at 15m granularity. Future mark-price research on alt symbols would need a separately authorized exclusion-rule governance memo analogous to Phase 3r §8.

### What this enables (data only)

- Cross-symbol trade-price kline comparison on **ADA at four intervals** (full coverage) plus **BTC / ETH 1h** (full coverage) plus **SOL / XRP at four intervals subject to exclusion of two early-2022 windows**.
- Alt-symbol funding context analysis for SOL / XRP / ADA (full coverage).
- Phase 4ab §11 feasibility-check work would now be possible **for the PASS subset**: cost-to-volatility, opportunity-rate, wick / stop-pathology, liquidity / execution-risk, idiosyncratic-risk profiling. **Phase 4ac does NOT perform any such analysis.**

### What this does NOT enable

- **Mark-price stop-domain feasibility** would require a separate governance memo before any Phase 3r §8-style mark-price analysis can use the new alt-symbol mark-price datasets.
- **Cross-symbol fairness comparison on klines** at intervals where SOL / XRP have gaps would require either a common-overlap window post-2022-04-03 or a separately authorized exclusion-rule.
- **No backtest. No diagnostic. No strategy spec. No implementation. No live-readiness. No exchange-write.** Phase 4ac data is research-eligibility evidence only.

### What this forbids (preserved verbatim)

- **No strategy verdict revision.** All retained verdicts preserved.
- **No old-strategy alt-symbol rerun.** Re-evaluating R3 / R2 / F1 / D1-A / V2 / G1 / C1 on alt symbols is retrospective rescue (Phase 4m / 4s / 4y / 4aa preserved).
- **No new strategy candidate creation.** Phase 4ac does NOT name a candidate.
- **No paper / shadow / live implication.** §1.7.3 mark-price-stop lock and Phase 3v §8 stop-trigger-domain governance preserved; alt-symbol mark-price datasets failing strict gate cannot be used for runtime-relevant stop modeling without a separately authorized governance memo.

## 11. Recommendation

### Recommended next step (conditional)

Phase 4ac core datasets passed sufficiently for several research-substrate cells (BTC 1h, ETH 1h, ADA at all four intervals, SOL / XRP / ADA funding). However, **mark-price datasets for all alt symbols failed strict gate**, and SOL / XRP trade-price klines failed strict gate due to early-2022 archive gaps. The right next step is a **docs-only governance / scope memo** that decides how to handle the failure pattern *before* any feasibility analysis or future strategy work is authorized.

### Two acceptable conditional-next paths (operator decision)

- **Option A — Future docs-only Phase 4ad gap-governance / scope-revision memo** (analogous to Phase 4j §11 metrics OI-subset partial-eligibility rule). Phase 4ad would specify per-trade or per-bar exclusion rules for the SOL / XRP early-2022 trade-price gaps and the cross-symbol mark-price gaps, restate Phase 3r §8 governance prospectively for alt symbols, and decide whether mark-price datasets can be partially eligible for future research. Phase 4ad would NOT acquire data, would NOT run analysis, would NOT name a strategy.
- **Option B — Future docs-only Phase 4ad substrate-feasibility analysis memo restricted to the PASS subset.** Phase 4ad would describe cost-to-volatility / opportunity-rate / wick / liquidity / idiosyncratic-risk profiling using only research-eligible families (BTC 1h, ETH 1h, ADA × {15m, 30m, 1h, 4h}, SOL / XRP / ADA funding) without using mark-price or SOL / XRP klines. Phase 4ad-B would NOT acquire data, would NOT run a backtest, would NOT name a strategy.

### Recommended primary next step

**Option A is recommended as primary** because the pattern of mark-price gaps and SOL / XRP early-2022 kline gaps will affect both PASS-subset analysis and any later mark-price-using research; resolving governance first avoids analyzing-then-amending. **Phase 4ad is NOT authorized by Phase 4ac.** Either option requires separate operator authorization.

**Always procedurally valid:** remain paused without authorizing Phase 4ad.

### NOT recommended / forbidden

- Old-strategy alt-symbol rerun — FORBIDDEN (retrospective rescue).
- Direct strategy-spec memo on alt symbols — REJECTED (substrate evidence still being established).
- Direct backtest — REJECTED.
- Paper / shadow / live / exchange-write — FORBIDDEN.
- Spot / COIN-M / options / cross-venue expansion — premature.

## 12. Preserved Locks and Boundaries

Phase 4ac preserves every retained verdict and project lock verbatim. **No verdict revised. No project lock changed. No governance file amended (beyond the narrow `current-project-state.md` update).**

```text
H0           : FRAMEWORK ANCHOR (preserved)
R3           : BASELINE-OF-RECORD (preserved)
R1a          : RETAINED — NON-LEADING (preserved)
R1b-narrow   : RETAINED — NON-LEADING (preserved)
R2           : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1           : HARD REJECT (preserved)
D1-A         : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
5m thread    : OPERATIONALLY CLOSED (Phase 3t; preserved)
V2           : HARD REJECT — terminal for V2 first-spec (preserved)
G1           : HARD REJECT — terminal for G1 first-spec (preserved)
C1           : HARD REJECT — terminal for C1 first-spec (preserved)

§11.6                       : 8 bps HIGH per side (preserved verbatim)
§1.7.3                      : project-level locks preserved
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility rule (preserved)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4p                    : G1 strategy spec (preserved)
Phase 4q                    : G1 backtest-plan methodology (preserved)
Phase 4v                    : C1 strategy spec (preserved)
Phase 4w                    : C1 backtest-plan methodology (preserved)
Phase 4z recommendations    : remain recommendations only; NOT adopted by 4ac
Phase 4aa admissibility framework : remain recommendation only; NOT adopted by 4ac
Phase 4ab recommendations   : remain recommendations only; NOT adopted by 4ac
Phase 4ac results           : data/integrity evidence only; NOT binding governance
```

## 13. Explicit Non-Authorization Statement

Phase 4ac does NOT authorize:

- Phase 4ad (any kind);
- Phase 5;
- Phase 4 canonical;
- any other named successor phase;
- backtests (any kind);
- diagnostics (any kind);
- Q1–Q7 rerun;
- strategy specs;
- hypothesis specs;
- backtest plans;
- implementation (no `src/prometheus/` modification by Phase 4ac);
- old-strategy rescue (no R3 / R2 / F1 / D1-A / V2 / G1 / C1 rescue; no R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid);
- paper / shadow / live operation;
- live-readiness;
- deployment;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public endpoint code calls;
- user stream / WebSocket / listenKey lifecycle;
- exchange-write capability;
- MCP tooling;
- Graphify tooling;
- `.mcp.json` creation or modification;
- credentials;
- adoption of Phase 4z recommendations as binding governance;
- adoption of Phase 4aa admissibility framework as binding governance;
- adoption of Phase 4ab recommendations as binding governance;
- adoption of Phase 4ac results or recommendations as binding governance;
- successor phase.

**Phase 4ac modified:**

- `scripts/phase4ac_alt_symbol_acquisition.py` (new; standalone orchestrator);
- 35 manifest JSON files under `data/manifests/` (new; one per acquired family);
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ac_alt-symbol-public-data-acquisition.md` (this report; new);
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ac_closeout.md` (closeout; new);
- `docs/00-meta/current-project-state.md` (narrow Phase 4ac paragraph addition).

**Phase 4ac did NOT modify:**

- any source under `src/prometheus/`;
- any test;
- any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`);
- any existing manifest in `data/manifests/`;
- any specialist governance file (`docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, `docs/03-strategy-research/v1-breakout-strategy-spec.md`, `docs/03-strategy-research/v1-breakout-backtest-plan.md`, `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`, `docs/04-data/data-requirements.md`, `docs/04-data/historical-data-spec.md`, `docs/04-data/timestamp-policy.md`, `docs/04-data/dataset-versioning.md`, `docs/04-data/live-data-spec.md`);
- existing strategy specifications;
- project locks, retained verdicts, or any prior phase's substantive content (beyond the narrow `current-project-state.md` update).

**Phase 4ac is preserved on its feature branch unless and until the operator separately instructs a merge.** main remains unchanged at `9db120741413ec9cb5b02ffd9622d0f43a1d8c57` after Phase 4ac branch creation.

---

**Phase 4ac is docs-and-data acquisition / integrity validation only. No source code under `src/prometheus/` modified. No tests modified. No existing scripts modified. No existing manifests modified. No backtests / diagnostics / Q1–Q7 rerun. No strategy candidate created. No old strategy rescued. No retained verdict revised. No project lock changed. Phase 4z recommendations remain recommendations only. Phase 4aa admissibility framework remains recommendation only. Phase 4ab recommendations remain recommendations only. Phase 4ac results are data/integrity evidence only and are NOT adopted as binding governance. C1 first-spec remains terminally HARD REJECTED. V2 / G1 first-specs remain terminally HARD REJECTED. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. Recommended state: remain paused (primary) — Phase 4ad gap-governance / scope-revision memo OR Phase 4ad-B PASS-subset substrate-feasibility analysis memo (conditional next; not authorized by Phase 4ac). No next phase authorized.**
