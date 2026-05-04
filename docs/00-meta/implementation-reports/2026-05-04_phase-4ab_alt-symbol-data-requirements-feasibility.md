# Phase 4ab — Alt-Symbol Data-Requirements and Feasibility Memo

**Authority:** Operator authorization for Phase 4ab (docs-only research-planning memo translating the completed Phase 4aa alt-symbol market-selection / admissibility memo into a precise data-requirements and feasibility plan for possible future alt-symbol research on Binance USDⓈ-M perpetuals). Phase 4aa (alt-symbol market-selection and admissibility memo; merged a8e81bd; recommendations and admissibility framework remain recommendations only and are NOT adopted as binding governance); Phase 4z (post-rejection research-process redesign memo; merged 6fb0c6c; recommendations remain recommendations only and are NOT adopted governance); Phase 4y (post-C1 consolidation); Phase 4x (C1 backtest execution; Verdict C HARD REJECT — terminal); Phase 4w (C1 backtest-plan); Phase 4v (C1 strategy spec); Phase 4u (C1 hypothesis-spec); Phase 4t (post-G1 fresh-hypothesis discovery); Phase 4s (post-G1 consolidation); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal); Phase 4q (G1 backtest-plan); Phase 4p (G1 strategy spec); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery); Phase 4m (post-V2 consolidation; 18-requirement validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal); Phase 4k (V2 backtest-plan); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4h (V2 data-requirements / feasibility memo); Phase 4g (V2 strategy spec); Phase 4f (external strategy research landscape); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3q (5m supplemental acquisition; mark-price 5m known invalid windows); Phase 3p §4.7 (strict integrity gate); Phase 3t §12 (validity gate); Phase 3k (post-D1-A consolidation); Phase 3e (post-F1 consolidation); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/04-data/data-requirements.md`; `docs/04-data/historical-data-spec.md`; `docs/04-data/live-data-spec.md`; `docs/04-data/timestamp-policy.md`; `docs/04-data/dataset-versioning.md`; `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4ab — **Alt-Symbol Data-Requirements and Feasibility Memo** (docs-only research-planning memo). Translates Phase 4aa's alt-symbol market-selection / admissibility question into concrete docs-only data requirements and feasibility planning for possible future alt-symbol research on Binance USDⓈ-M perpetuals. **Phase 4ab is text-only.** No data acquired, downloaded, modified, patched, regenerated, or replaced. No API call. No endpoint call. No `data.binance.vision` access. No public-endpoint code. No authenticated REST. No private endpoint. No user stream. No WebSocket. No listenKey. No credentials. No `.env`. No network I/O. No manifest created. No manifest modified. No backtest run. No diagnostic run. No Q1–Q7 rerun. No strategy candidate named. No hypothesis-spec memo. No strategy-spec memo. No backtest-plan memo. No implementation code. No `src/prometheus/`, tests, or scripts modified. No retained verdict revised. No project lock changed. No governance file amended (beyond the narrow `docs/00-meta/current-project-state.md` update required to record Phase 4ab). No successor phase authorized.

**Branch:** `phase-4ab/alt-symbol-data-requirements-feasibility`. **Memo date:** 2026-05-04 UTC.

---

## 1. Purpose

Phase 4ab translates Phase 4aa's alt-symbol market-selection / admissibility question into a concrete docs-only data-requirements and feasibility plan. Phase 4ab determines what data **would** be required, what feasibility risks **must** be resolved, what existing data can be reused, and what new public unauthenticated data would be needed in a future acquisition phase, *if* the operator ever separately authorizes one.

**Phase 4ab is docs-only.**

- **No data acquisition.** No new dataset is downloaded, ingested, normalized, or materialized.
- **No data download.** No network I/O. No `data.binance.vision` call. No Binance API call. No authenticated REST. No private endpoint. No public-endpoint code. No user stream / WebSocket / listenKey. No credentials.
- **No manifest creation or modification.** Existing manifests are inspected read-only for documentation/planning context only.
- **No backtest.** No backtest is run, planned, or scoped.
- **No diagnostics.** No Q1–Q7 rerun. No new diagnostic phase.
- **No strategy spec.** No new strategy candidate is named, defined, or specified.
- **No hypothesis-spec memo.** No new hypothesis is named.
- **No backtest-plan memo.** No backtest methodology is specified.
- **No implementation.** No `src/prometheus/`, tests, or scripts modified.
- **No live-readiness.** No paper / shadow / live operation authorized, planned, or implied.
- **No exchange-write.** No production keys, authenticated APIs, private endpoints, user stream, WebSocket, exchange-write capability, MCP, Graphify, or `.mcp.json` touched.

Phase 4ab records data-requirements and feasibility planning as **recommendations** for any future docs-and-data acquisition phase; the recommendations are **not** adopted as binding governance.

## 2. Relationship to Phase 4aa

### Brief Phase 4aa summary

- Phase 4aa evaluated whether future strategy research should remain restricted to BTCUSDT / ETHUSDT (the project's substrate from Phase 2 onward) or expand to liquid large-cap Binance USDⓈ-M perpetual alt symbols.
- Phase 4aa core comparison universe (recorded as candidate symbol universe; not authorized for acquisition):

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

- Phase 4aa optional secondary watchlist:

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

- Phase 4aa proposed eight pre-backtest symbol-admissibility gates:
  1. Listing / continuity gate.
  2. Public-data availability gate.
  3. Cost-to-volatility gate.
  4. Opportunity-rate gate.
  5. Liquidity / execution-risk gate.
  6. Wick / stop-pathology gate.
  7. Idiosyncratic-risk gate.
  8. Governance-label compatibility gate.

### Governance status carried into Phase 4ab

- **Phase 4aa recommendations remain recommendations only.** They were not adopted as binding governance at the Phase 4aa merge.
- **Phase 4aa admissibility framework is not binding governance.** It is a planning input that any future feasibility memo or acquisition phase could refer to, but no project lock, phase gate, or specialist governance file was updated to enforce it.
- **Phase 4ab does not make the Phase 4aa framework binding governance.** Phase 4ab uses Phase 4aa as a planning input only.
- **Phase 4z recommendations also remain recommendations only.** Phase 4ab does not adopt them as binding governance either.
- **Phase 4ab's own recommendations are recommendations only.** Adoption of any Phase 4ab recommendation as binding governance would require a separately authorized governance-update phase, which Phase 4ab does NOT initiate.

## 3. Research Question

```text
What data would be required, and what feasibility risks must be resolved,
before the project can responsibly decide whether SOLUSDT / XRPUSDT / ADAUSDT
or other liquid USDⓈ-M perpetual alt symbols deserve future strategy research?
```

**Phase 4ab does not answer whether alt symbols are better than BTC/ETH.** Phase 4ab does not claim that alt-symbol research will produce different outcomes from the V2 / G1 / C1 results. Phase 4ab defines how the project would safely gather evidence later, *if* the operator ever separately authorizes a future docs-and-data acquisition phase.

The question's importance does not depend on having an answer; it depends on the project not having previously planned how to answer it. Phase 4ab plans how to answer it.

## 4. Existing Data Inventory

This section inspects committed manifests and committed acquisition / backtest script names read-only for documentation and planning context. **No manifest is modified.** **No script is executed.** **No data file is touched.** Local non-committed files under `data/raw/`, `data/normalized/`, or `data/research/` are treated as gitignored / reproducible artefacts; only committed manifests and committed scripts are authoritative for the project record.

### 4.1 BTCUSDT / ETHUSDT trade-price kline datasets (committed manifests)

```text
Phase 2 v001 / v002 (15m + derived 1h):
  binance_usdm_btcusdt_15m__v001.manifest.json
  binance_usdm_btcusdt_15m__v002.manifest.json
  binance_usdm_btcusdt_1h_derived__v001.manifest.json
  binance_usdm_btcusdt_1h_derived__v002.manifest.json
  binance_usdm_ethusdt_15m__v001.manifest.json
  binance_usdm_ethusdt_15m__v002.manifest.json
  binance_usdm_ethusdt_1h_derived__v001.manifest.json
  binance_usdm_ethusdt_1h_derived__v002.manifest.json
```

**Provenance:** Phase 2 strategy-research arc; v002 is the verdict-provenance dataset family per Phase 2p §C.1 (R3 baseline-of-record) preserved verbatim in current governance.

```text
Phase 4i v001 (30m + 4h):
  binance_usdm_btcusdt_30m__v001.manifest.json
  binance_usdm_btcusdt_4h__v001.manifest.json
  binance_usdm_ethusdt_30m__v001.manifest.json
  binance_usdm_ethusdt_4h__v001.manifest.json
```

**Provenance:** Phase 4i V2 acquisition phase; the 30m and 4h kline datasets PASSED Phase 4h §17 strict integrity gate and are research-eligible for any future kline-based research that respects the verdict-provenance and forbidden-input governance.

### 4.2 BTCUSDT / ETHUSDT mark-price kline datasets (committed manifests)

```text
v001 / v002 (15m):
  binance_usdm_btcusdt_markprice_15m__v001.manifest.json
  binance_usdm_btcusdt_markprice_15m__v002.manifest.json
  binance_usdm_ethusdt_markprice_15m__v001.manifest.json
  binance_usdm_ethusdt_markprice_15m__v002.manifest.json
```

**Provenance:** Phase 2 supplemental mark-price 15m datasets; have known invalid windows under Phase 3r §8 mark-price gap governance.

```text
Phase 3q v001 (5m supplemental):
  binance_usdm_btcusdt_markprice_5m__v001.manifest.json
  binance_usdm_ethusdt_markprice_5m__v001.manifest.json
```

**Provenance:** Phase 3q supplemental mark-price 5m datasets; documented invalid windows (BTC: 2022-07-30/31, 2022-10-02, 2023-02-24, 2023-11-10; ETH: 2022-07-12, 2022-10-02, 2023-02-24, 2023-11-10) recorded in manifests with `research_eligible: false` per Phase 3p §4.7 / Phase 3r §8 strict integrity rules — no patching, no forward-fill, no interpolation, no imputation.

### 4.3 BTCUSDT / ETHUSDT funding-rate datasets (committed manifests)

```text
v001 / v002:
  binance_usdm_btcusdt_funding__v001.manifest.json
  binance_usdm_btcusdt_funding__v002.manifest.json
  binance_usdm_ethusdt_funding__v001.manifest.json
  binance_usdm_ethusdt_funding__v002.manifest.json
```

**Provenance:** Funding-rate history covering the project's research window; v002 is the verdict-provenance dataset family.

### 4.4 BTCUSDT / ETHUSDT 5m supplemental trade-price datasets (committed manifests)

```text
Phase 3q v001:
  binance_usdm_btcusdt_5m__v001.manifest.json
  binance_usdm_ethusdt_5m__v001.manifest.json
```

**Provenance:** Phase 3q supplemental 5m trade-price datasets; PASSED Phase 3p §4.7 strict integrity gate (446 688 bars each; 0 gaps); 5m diagnostic thread is OPERATIONALLY CLOSED per Phase 3t.

### 4.5 BTCUSDT / ETHUSDT metrics datasets (committed manifests)

```text
Phase 4i v001:
  binance_usdm_btcusdt_metrics__v001.manifest.json
  binance_usdm_ethusdt_metrics__v001.manifest.json
```

**Provenance:** Phase 4i V2 acquisition; FAILED Phase 4h §17 strict integrity gate at the family level (intra-day 5-minute missing observations; ratio-column NaN concentrations in early-2022 data). Manifests record `research_eligible: false` globally.

**Phase 4j §11 partial-eligibility rule:** the OI subset (`create_time`, `symbol`, `sum_open_interest`, `sum_open_interest_value`) is *partially* research-eligible at the per-bar level under the binding Phase 4j §11 rule (any 30m bar requires all six aligned 5-minute records present with non-NaN OI; per-bar exclusion algorithm restated verbatim; optional ratio columns remain forbidden). Phase 4j §11 governance is preserved verbatim by Phase 4ab.

### 4.6 No alt-symbol manifests exist

**No manifest exists for any of:** SOLUSDT, XRPUSDT, ADAUSDT, BNBUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT, or any other alt symbol on Binance USDⓈ-M perpetuals. Phase 4ab inspected `data/manifests/` and found only BTCUSDT / ETHUSDT entries.

**Phase 4ab does NOT create alt-symbol manifests.**

### 4.7 Existing committed acquisition / backtest scripts (read-only for context)

```text
Acquisition scripts (read-only context; not executed in Phase 4ab):
  scripts/phase3q_5m_acquisition.py     (5m supplemental trade-price + mark-price)
  scripts/phase4i_v2_acquisition.py     (V2 acquisition: 30m / 4h klines + metrics)

Backtest scripts (read-only context; not executed in Phase 4ab):
  scripts/phase2e_baseline_backtest.py
  scripts/phase2g_variant_wave1.py
  scripts/phase2l_R3_first_execution.py
  scripts/phase2m_R1a_on_R3_execution.py
  scripts/phase2s_R1b_narrow_execution.py
  scripts/phase2w_R2_execution.py
  scripts/phase3d_F1_execution.py
  scripts/phase3j_D1A_execution.py
  scripts/phase4l_v2_backtest.py
  scripts/phase4r_g1_backtest.py
  scripts/phase4x_c1_backtest.py
```

**No script is executed by Phase 4ab.** **No script is modified by Phase 4ab.** **No new script is created by Phase 4ab.** The list is recorded for provenance and to support a future docs-and-data Phase 4ac (if ever authorized) in establishing pattern continuity for any new acquisition orchestrator (e.g., a hypothetical `scripts/phase4ac_alt_symbol_acquisition.py` would mirror the standalone-script discipline of `scripts/phase3q_5m_acquisition.py` and `scripts/phase4i_v2_acquisition.py` — *if* Phase 4ac is ever authorized; Phase 4ab does NOT authorize it).

### 4.8 Data treated as authoritative

**Authoritative for Phase 4ab planning:** committed manifests under `data/manifests/` (read-only inspection); committed governance docs under `docs/04-data/` (read-only inspection); committed prior phase reports under `docs/00-meta/implementation-reports/` (read-only inspection).

**NOT authoritative:** local non-committed files under `data/raw/`, `data/normalized/`, `data/research/`, or any other gitignored path. These are treated as gitignored / reproducible artefacts; the project record relies on committed manifests + committed orchestrator scripts to establish provenance.

**No invented datasets.** Phase 4ab does NOT claim a dataset exists unless its manifest is committed. If repository evidence is uncertain about a particular data family, Phase 4ab states explicitly that future inspection or acquisition would be required.

## 5. Proposed Future Symbol Scope

### Required future core acquisition-planning set (recommendation)

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

**Rationale:**

- **BTCUSDT / ETHUSDT:** required as continuity anchors and controls. The project's six-failure topology (R2 / F1 / D1-A / V2 / G1 / C1) is established on BTC primary / ETH comparison; any future alt-symbol research must preserve this anchor pair so that cross-substrate comparison is possible. BTC and ETH datasets already exist (per §4); future Phase 4ac would not need to re-acquire them at the same intervals already covered, but would need to establish dataset-version continuity.
- **SOLUSDT / XRPUSDT / ADAUSDT:** the first alt-symbol substrate candidates from Phase 4aa Section 4 primary comparison set. Three alts are sufficient to test substrate-level differences (vs. one alt, which would not distinguish symbol-specific from substrate-class effects) but small enough to avoid a symbol-mining exercise.
- **Five symbols total** balances substrate diversity against acquisition-burden and avoids the Phase 4z-observed risk of "more candidates always look promising at admissibility" by keeping the set fixed before acquisition.

### Deferred secondary watchlist (recommendation)

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

**Rationale:**

- **Keep as secondary watchlist.** BNB carries exchange-token risk; DOGE carries social-flow / meme-driven risk; LINK carries oracle-update / protocol-event risk; AVAX carries ecosystem-driven risk. Each is liquid enough to be a candidate but adds idiosyncratic-risk axes that complicate first-pass evaluation.
- **Do not include in first acquisition unless a future operator decision explicitly widens the scope.** If the core five-symbol set is ever evaluated and produces sufficiently informative evidence to justify expansion, the operator can authorize a separate later step. Premature widening risks symbol-mining (the temptation to "find one alt that works" by trying many).
- **Avoid excess data work before the core set is evaluated.** Phase 4ab's recommendation is: minimal viable acquisition first, then evaluate, then potentially expand.

### Explicit non-authorization

**Phase 4ab does NOT authorize acquisition for any symbol** — neither the core set nor the watchlist. The recommendation is for a possible future docs-and-data Phase 4ac acquisition phase only, *if* the operator separately authorizes one. **Phase 4ab does NOT authorize Phase 4ac.**

## 6. Proposed Future Data Families

This section defines future data families that **would** be required or optional for any future docs-and-data Phase 4ac acquisition phase. **None of these families is acquired or modified by Phase 4ab.**

### A. Standard trade-price klines — REQUIRED

Required for each future core symbol.

**Recommended intervals:**

```text
15m
30m
1h
4h
```

**Rationale:**

- **15m** preserves continuity with original V1 / R-family research and supports stop / timing diagnostics (Phase 2 arc; Phase 3s 5m diagnostics treated 15m as primary signal-bar reference).
- **30m** preserves continuity with V2 / G1 / C1 research arcs (Phase 4i acquired 30m for BTC/ETH; Phase 4l / 4r / 4x evaluated strategies on 30m primary).
- **1h** supports session / aggregation / intermediate bias analyses; Phase 2 / Phase 4f research used 1h as HTF context.
- **4h** supports higher-timeframe bias and broad trend / regime context; Phase 4i acquired 4h for BTC/ETH; Phase 4f research catalog used 4h as a primary HTF candidate.

**Manifest naming pattern (recommendation; see §8):**

```text
binance_usdm_<symbol>_<interval>__v001  (e.g., binance_usdm_solusdt_30m__v001)
```

### B. Funding-rate history — REQUIRED

Required for each future core symbol if available.

**Rationale:**

- Funding / cost context remains important after the D1-A arc and the V2 / G1 / C1 derivative-flow lessons.
- Funding should be acquired but should NOT become a standalone rescue trigger without a future ex-ante hypothesis. Phase 4y §"Forbidden cross-strategy rescue interpretations" preserved verbatim: no D1-A-prime / D1-B / V1-D1 / F1-D1 hybrid; funding as risk-context only, not directional trigger, unless a separately authorized fresh-hypothesis discovery memo names a candidate that uses it differently.
- Funding-rate datasets are smaller than klines (per-event records, not per-bar) and are operationally low-cost to acquire.

**Manifest naming pattern (recommendation):**

```text
binance_usdm_<symbol>_funding__v001
```

### C. Mark-price klines — CONDITIONAL REQUIRED

Recommended as **conditional required** if any future research evaluates:

- mark-price stop-domain behavior (Phase 3v §8 stop-trigger-domain governance preserved);
- stop-trigger-domain compatibility (`mark_price_runtime` requires mark-price datasets);
- mark-vs-trade stop-lag diagnostics (Phase 3s Q6 D1-A finding established mark-stop lag as descriptive);
- live-readiness-relevant stop modeling (no live-readiness authorized; this is a future-planning consideration).

**Suggested intervals:**

```text
15m
30m
1h
4h
```

**5m mark-price** should be considered ONLY if a future diagnostic memo explicitly requires stop-pathology timing at 5m resolution (analogous to Phase 3q's 5m mark-price acquisition for Q6 D1-A diagnostics; Phase 3q established that mark-price 5m has known invalid windows). Default recommendation: do NOT include 5m mark-price in a first alt-symbol acquisition.

**Phase 3p / 3r preservation:**

- **Phase 3p §4.7 strict mark-price integrity logic preserved verbatim.** No relaxation.
- **Phase 3r §8 invalid-window exclusion rule preserved verbatim.** Known invalid windows are exclusion zones, not patch zones; per-trade (or per-bar) exclusion test based on analysis-window intersection.
- **No patching / forward-fill / interpolation / imputation.** Phase 4i precedent honored: any partial-pass outcome would require a separately authorized governance memo (analogous to Phase 4j §11 metrics OI-subset rule) *before* any strategy spec uses the dataset.
- **Mark-price acquisition risk:** alt symbols may have mark-price gap patterns different from BTC / ETH. Phase 4ab cannot predict the gap distribution; future Phase 4ac (if authorized) would need to evaluate per-symbol mark-price integrity empirically.

**Manifest naming pattern (recommendation):**

```text
binance_usdm_<symbol>_markprice_<interval>__v001
```

### D. Metrics / open-interest data — OPTIONAL / CONDITIONAL

Optional and conditional. Acquire ONLY if a future hypothesis requires derivatives-flow context.

**Phase 4i / Phase 4j lesson preservation:**

- **Global metrics family may fail strict research eligibility** due to missing observations and ratio-column NaNs (Phase 4i precedent: BTC / ETH metrics families globally `research_eligible: false`).
- **OI subset may be partially eligible only** under the Phase 4j §11 metrics OI-subset partial-eligibility rule (per-bar exclusion algorithm; six aligned 5-minute records required at offsets 0/5/10/15/20/25 minutes from 30m bar open with non-NaN `sum_open_interest` and `sum_open_interest_value`).
- **Optional ratio columns must remain forbidden** (Phase 4j §11.3): `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`, `count_long_short_ratio`, `sum_taker_long_short_vol_ratio`. A future Phase 4ac that acquires alt-symbol metrics datasets must enforce the same column-list restriction.

**Default recommendation:** do NOT include metrics in a first alt-symbol acquisition unless a future ex-ante hypothesis (which would need separate operator authorization) explicitly requires OI features. The C1 first-spec did not use metrics; the operator may choose to omit metrics from a first alt-symbol acquisition entirely.

**Manifest naming pattern (recommendation):**

```text
binance_usdm_<symbol>_metrics__v001
```

### E. AggTrades / tick / order-book data — DEFERRED / NOT RECOMMENDED NOW

aggTrades, tick-level data, and order-book data are **NOT recommended** for the first alt-symbol feasibility acquisition. Reasons:

- **Higher complexity.** Tick-level data multiplies storage and processing cost by orders of magnitude vs. kline data.
- **Larger storage burden.** A single symbol's tick data over the project's research period would dwarf the entire current `data/raw/` footprint.
- **More microstructure noise.** Without a microstructure-specific hypothesis (Phase 4t Candidate F was rejected at boundary because of unavailable-data dependency and microstructure-research adjacency), tick data adds noise without signal.
- **Higher risk of shifting into execution / microstructure research prematurely.** Phase 4f / Phase 4t evidence: microstructure / liquidity-timing research is a different research family (F-4 in the Phase 4z proposed taxonomy); shifting substrate AND research-family in the same step contaminates attribution per Phase 4aa Section 5.
- **Not necessary for first substrate-viability checks.** Cost-to-volatility, opportunity-rate, wick / stop-pathology, liquidity / execution-risk, and idiosyncratic-risk feasibility (per §11 below) can all be assessed with kline + funding + mark-price data; aggTrades / tick / order-book data are required only if a future hypothesis explicitly depends on microstructure features.

**Phase 4ab recommendation:** if a future hypothesis ever requires microstructure data, that requirement must be predeclared in a separate hypothesis-spec memo, and the operator would authorize a corresponding acquisition phase separately. **Phase 4ab does NOT recommend acquiring aggTrades / tick / order-book data as part of any first alt-symbol acquisition.**

### F. Exchange metadata snapshots — REQUIRED WHERE AVAILABLE

Future acquisition plan should include symbol metadata where Binance publishes it:

- **Tick size** (price-precision granularity per symbol).
- **Step size** (quantity-precision granularity per symbol).
- **Min quantity** (minimum order quantity).
- **Min notional** where applicable (minimum notional value).
- **Contract status** (TRADING / BREAK / SETTLING / etc.).
- **Leverage bracket** where available (notional-tier leverage caps).
- **Funding interval assumptions** if available (most USDⓈ-M perpetuals settle every 8h; per-symbol exceptions exist).

**Rationale:** sizing calculations require step / tick / min-quantity / min-notional to round positions correctly; leverage bracket affects internal notional cap reasoning (§1.7.3 2× leverage cap is the live default but exchange leverage brackets cap maximum notional per tier, which may differ across alt symbols); funding interval affects cost modeling. Without metadata, future strategy specs cannot be sized correctly.

**Sources:** Binance publishes exchange-info via `GET /fapi/v1/exchangeInfo` and similar endpoints; metadata snapshots are typically obtained as point-in-time JSON. **No metadata is acquired by Phase 4ab.**

**Manifest naming pattern (recommendation):**

```text
binance_usdm_exchange_info__v001  (single multi-symbol snapshot)
```

OR per-symbol:

```text
binance_usdm_<symbol>_metadata__v001
```

The exact naming choice should be made by the future Phase 4ac (if ever authorized) using existing repository conventions.

## 7. Proposed Future Date Range

### Recommended range

```text
2022-01-01 through the latest fully completed month available at acquisition time
```

**Rationale:**

- **2022-01-01** is the start of the project's research window per Phase 2e v002 datasets, Phase 3q 5m supplemental datasets, and Phase 4i 30m / 4h kline datasets. Continuity with existing BTC / ETH evidence is preserved by reusing the same start.
- **Latest fully completed month available at acquisition time** is consistent with Phase 3q / Phase 4i precedent: each acquisition phase fixed its end date to the latest month with complete data at that time. A future Phase 4ac would set its end date at authorization time.

### Listing-date constraints

Alt symbols may not have continuous Binance USDⓈ-M perpetual trading history covering the full 2022-01-01 onward window:

- **SOLUSDT-PERP:** has history before 2022-01 (earlier listing); covers full 2022-01 onward window.
- **XRPUSDT-PERP:** has history before 2022-01 (earlier listing); covers full 2022-01 onward window.
- **ADAUSDT-PERP:** has history before 2022-01 (earlier listing); covers full 2022-01 onward window.
- Watchlist symbols (BNB / DOGE / LINK / AVAX): listing-date situations vary; future Phase 4ac would need to verify per-symbol.

**Phase 4ab does NOT independently verify these listing dates.** The recorded dates above are general industry knowledge and would need to be confirmed empirically (without acquisition; e.g., via existing public exchange-info snapshots if any) at the time of any future Phase 4ac authorization.

### Listing-coverage policy (recommendation)

Future Phase 4ac (if authorized) should:

- **If a symbol was listed before 2022-01-01:** use 2022-01-01 as dataset start (consistent with BTC / ETH).
- **If a symbol was listed after 2022-01-01:** use the symbol's first complete trading month as dataset start; record reduced history as a per-symbol field in the manifest.
- **Do NOT fabricate pre-listing data.** No backfill, no synthetic data, no proxy from spot or another instrument.
- **Do NOT silently compare full-history BTC / ETH to shorter-history alts.** Cross-symbol comparison must label coverage mismatches explicitly.

### Common-overlap policy (recommendation)

Future analysis (if any) must support both:

- **Full-available-history view:** each symbol uses its own listing-date-onward history. Useful for per-symbol behavior characterization.
- **Common-overlap view:** all symbols restricted to the intersection of available trading windows. Useful for cross-symbol fairness comparison.

Both views must be reported when cross-symbol comparison is presented; a future spec must NOT silently use one view for some symbols and a different view for others.

### Train / validation / OOS implications

The Phase 4k / Phase 4q / Phase 4w window structure (train 2022-01-01..2023-06-30 / validation 2023-07-01..2024-06-30 / OOS 2024-07-01..end) was calibrated to BTC / ETH full-history coverage. Alt symbols that were listed before 2022-01-01 (the expected case for SOL / XRP / ADA) can use the same windows; alt symbols listed after 2022-01-01 would have shorter train windows and require either:

- **adapted window structure** (proportionally shorter train per symbol; same validation / OOS for cross-symbol comparison); OR
- **exclusion from comparative cells** where window mismatch is structural.

A future spec would need to predeclare this window-handling policy *before* any data is acquired so that cross-symbol comparison rules are fixed ex-ante.

### Statistical-confidence implications

Shorter alt histories reduce per-symbol sample size for statistical tests (bootstrap CIs, deflated Sharpe, PBO, CSCV). A future spec must:

- recompute sample-size-dependent statistics per symbol (NOT pool across symbols);
- weight cross-symbol consistency checks by per-symbol sample size where applicable;
- preserve the "ETH cannot rescue BTC" / "no symbol rescues another" principle from Phase 4y.

## 8. Proposed Future Dataset Naming and Directory Convention

### Naming pattern (recommendation)

Continuing the project's existing naming convention from Phase 2 / Phase 3q / Phase 4i:

```text
binance_usdm_<symbol>_<interval>__v001
binance_usdm_<symbol>_markprice_<interval>__v001
binance_usdm_<symbol>_funding__v001
binance_usdm_<symbol>_metrics__v001
binance_usdm_exchange_info__v001  (or per-symbol variant)
```

Explicit examples for the proposed core SOL alt symbol (these manifests **do NOT exist yet** and **are NOT created by Phase 4ab**):

```text
binance_usdm_solusdt_15m__v001
binance_usdm_solusdt_30m__v001
binance_usdm_solusdt_1h__v001
binance_usdm_solusdt_4h__v001
binance_usdm_solusdt_markprice_15m__v001
binance_usdm_solusdt_markprice_30m__v001
binance_usdm_solusdt_markprice_1h__v001
binance_usdm_solusdt_markprice_4h__v001
binance_usdm_solusdt_funding__v001
binance_usdm_solusdt_metrics__v001
```

XRPUSDT / ADAUSDT / BNBUSDT / DOGEUSDT / LINKUSDT / AVAXUSDT would follow the identical pattern.

### Directory convention (recommendation)

Continuing existing repository convention:

- `data/raw/...` — gitignored; raw archive files from public unauthenticated sources.
- `data/normalized/...` — gitignored; canonical Parquet files with project-standard schema.
- `data/manifests/...` — committed; manifest JSON files (committed as project record).

**Exact directory layout** must follow the existing repository conventions established in `docs/04-data/historical-data-spec.md` and `docs/04-data/dataset-versioning.md`. Phase 4ab does NOT propose a new layout; it proposes that any future Phase 4ac follow the existing layout verbatim.

**No directory or file is created by Phase 4ab.**

### Versioning convention

`__v001` is the recommended initial version for any new alt-symbol family. The project's existing versioning convention (`__v001` for first acquisition; `__v002` for replacement / re-acquisition with material methodology change; never silent overwrite) should be preserved verbatim per Phase 2 / Phase 3q / Phase 4i precedent.

Phase 4ab does NOT recommend creating `__v003` or any other version bump for existing BTC / ETH families as part of an alt-symbol acquisition; the alt symbols would be added as their own `__v001` families alongside existing versioned families.

## 9. Future Manifest Requirements

A future Phase 4ac (if authorized) would create manifest JSON files under `data/manifests/` for each acquired family. The required manifest fields are recommended below, continuing the existing repository convention.

**No manifest is created or modified by Phase 4ab.**

### Required manifest fields (recommendation)

```text
dataset_family             : e.g., binance_usdm_solusdt_30m__v001
symbol                     : e.g., SOLUSDT
interval                   : e.g., 30m (or "funding" / "metrics" / etc. for non-kline)
data_family                : kline | markprice_kline | funding | metrics |
                              exchange_info | aggtrades (deferred; not for first
                              alt-symbol acquisition)
venue                      : binance
market_type                : usdm_perpetual
source                     : data.binance.vision (public bulk archive) or other
                              public source identifier
source_endpoint_family     : e.g., data.binance.vision/futures/um/monthly/klines
                              (descriptive only; no endpoint call by manifest)
acquisition_method         : e.g., public_bulk_archive_with_sha256_companion
date_range_start_utc       : YYYY-MM-DD
date_range_end_utc         : YYYY-MM-DD
listing_date_utc           : YYYY-MM-DD (per-symbol; null if before research window)
expected_rows              : computed from interval × range
actual_rows                : measured at acquisition time
gap_count                  : measured at acquisition time
duplicate_count            : measured at acquisition time
malformed_row_count        : measured at acquisition time
invalid_windows            : list of (start_utc, end_utc, reason) tuples;
                              recorded verbatim per Phase 3p / 3r rules
sha256_verification        : pairwise SHA256 evidence vs. .CHECKSUM companion
                              files where applicable
schema_version             : e.g., kline_schema_v1
canonical_timestamp_field  : open_time
timezone_policy            : utc_unix_milliseconds (per docs/04-data/timestamp-policy.md)
research_eligible          : true | false (boolean; fail-closed per
                              docs/04-data/dataset-versioning.md)
partial_eligibility        : null | { feature_subset, eligibility_rule_reference }
                              (e.g., for OI subset under Phase 4j §11)
known_exclusions           : list of feature subsets explicitly excluded
                              (e.g., optional ratio columns in metrics families)
governance_references      : list of governance docs that gate this dataset's use
                              (e.g., Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11,
                              Phase 4k methodology, Phase 4ac authorization brief)
created_at_utc_ms          : acquisition timestamp
acquisition_script_commit  : git commit SHA of the orchestrator script if used
operator_authorization_ref : reference to the operator authorization phase brief
                              (e.g., "Phase 4ac authorization brief, 2026-MM-DD")
```

### Manifest discipline (recommendation)

- **One manifest per dataset family.** Do not combine multiple families in a single manifest.
- **No silent updates.** Manifest content is fixed at acquisition time and is not edited later. Any post-acquisition correction requires a new manifest version (`__v002`) with provenance documented.
- **Committed.** Manifests are committed to git per existing repository convention; raw and normalized data remain gitignored.
- **Reproducible.** Manifest content + orchestrator script commit SHA + public source identifier together specify a reproducible acquisition.

**Phase 4ab does NOT create or modify any manifest.**

## 10. Future Integrity Gates

A future Phase 4ac (if authorized) would apply strict integrity gates to each acquired dataset family. The gates are recommended below, continuing Phase 3p §4.7 and Phase 4h §17 precedent.

### Required integrity gates (recommendation)

- **No duplicate canonical keys.** Each `(symbol, interval, open_time)` tuple must appear at most once.
- **No malformed OHLCV rows.** Each kline row must have valid open / high / low / close / volume fields with correct types and non-degenerate values (e.g., `low <= open <= high`, `low <= close <= high`, `volume >= 0`).
- **No missing required columns.** Schema-required columns must be present in every row.
- **Monotonic timestamps.** `open_time` strictly increasing within a dataset.
- **UTC Unix milliseconds.** Per `docs/04-data/timestamp-policy.md`; canonical timestamp policy preserved.
- **`open_time` as canonical bar key.** Per existing repository convention.
- **Expected interval continuity.** For 30m klines, consecutive `open_time` values differ by exactly 30 × 60 × 1000 ms; gap detection compares against this expectation.
- **Gap detection.** Any deviation from expected interval continuity is recorded as a gap (start_utc, end_utc, missing_bar_count) without patching.
- **Volume sanity.** Volume must be non-negative; zero-volume bars permitted but logged.
- **No negative prices / quantities.** Trade-price fields must be positive; quantity fields must be non-negative.
- **Funding timestamp continuity.** For funding datasets: funding events must occur at expected intervals (typically 8h on USDⓈ-M perpetuals; per-symbol exceptions verified against exchange metadata).
- **Mark-price gaps recorded, not patched.** Any mark-price kline gap is recorded as `invalid_windows`; Phase 3r §8 governance preserved.
- **Metrics missing observations recorded, not patched.** Any metrics-family missing 5-minute observation is recorded; Phase 4j §11 governance preserved.
- **Optional metrics columns forbidden** unless separately governed. Phase 4j §11.3 preserved.
- **No forward-fill / interpolation / imputation.** No silent data manipulation. Strict integrity is preserved.

### Pass / fail outcomes

- **PASS = `research_eligible: true`.** Dataset passes all integrity gates and is admissible for future research.
- **PARTIAL PASS = `research_eligible: false` globally** with `partial_eligibility` populated for specific feature subsets, only if separately governed by a later docs-only governance memo (analogous to Phase 4j §11 metrics OI-subset rule). Phase 4ab does NOT create such a governance memo; if a future Phase 4ac produces a partial-pass outcome, a separate Phase 4ac-equivalent governance memo would be required *before* the dataset's partial subset is used by any future strategy spec.
- **FAIL = `research_eligible: false`.** Dataset does not pass integrity gates; cannot be used by future research absent a partial-eligibility governance memo.
- **Unknown = fail closed.** Any dataset whose integrity status is uncertain is treated as `research_eligible: false`; default fail-closed.

### Empirical risk recognition

Phase 4i precedent demonstrated that:

- **Trade-price kline integrity** generally passes strict gates on Binance USDⓈ-M perpetuals (BTC / ETH 30m / 4h klines passed; 5m supplemental klines passed).
- **Mark-price kline integrity** has known invalid-window failures (Phase 3q mark-price 5m had 4 invalid windows per symbol; corresponding 15m families have similar gaps).
- **Metrics integrity** failed at the family level for BTC / ETH (intra-day missing observations + ratio NaN concentrations); only the OI subset is partially eligible.

Alt symbols may have different integrity profiles. **Phase 4ab does NOT predict alt-symbol integrity.** Future Phase 4ac (if authorized) must evaluate empirically and apply Phase 3r §8 / Phase 4j §11 governance pattern to any partial-pass outcome.

## 11. Feasibility Checks Enabled by Future Data

This section defines the analyses that future data **would** enable. **Phase 4ab does NOT run any of these analyses.** They are listed here as planning targets for any future Phase 4ac feasibility report or any later docs-only feasibility-analysis memo.

### A. Cost-to-volatility feasibility

For each candidate symbol:

- **ATR / median range vs. §11.6 HIGH cost.** Compute typical ATR(20) on the candidate's primary signal timeframe; compare against 8 bps per side cost. A symbol whose typical ATR is small relative to cost is structurally cost-fragile (R2 lesson).
- **Expected stop distance vs. cost.** Compute typical structural stop distance for plausible setup geometries; compare against round-trip cost.
- **Expected move size vs. cost.** Compute distribution of typical R-distance moves; compare against round-trip cost.
- **Funding burden vs. holding horizon.** Compute funding-rate distribution; estimate funding-cost burden for plausible holding horizons.
- **Slippage proxy requirements.** Phase 4ab notes that slippage cannot be estimated from kline data alone; future feasibility memo would either accept §11.6 = 8 bps as the conservative bound or note the requirement for separately authorized aggTrades / order-book acquisition (NOT recommended in first alt-symbol step per §6.E).

### B. Opportunity-rate feasibility

For each candidate symbol:

- **Expansion event frequency.** For a hypothetical breakout-style setup, frequency of qualifying setup events per N bars.
- **Breakout-candidate frequency.** For a hypothetical close-beyond-range trigger, frequency of qualifying triggers.
- **Trend-regime frequency.** For a hypothetical HTF trend filter, frequency of qualifying regime states.
- **Joint-condition sparsity risk.** For a hypothetical multi-condition setup, frequency of joint events (G1 lesson: multi-condition AND classifiers naturally produce sparse intersections).
- **Minimum candidate-event floor.** Per the Phase 4u / Phase 4w / CFP-9 framework, predeclare a per-symbol minimum candidate-event floor before any strategy-spec authorization.

### C. Wick / stop-pathology feasibility

For each candidate symbol:

- **Wick fraction around adverse stop exits.** For a hypothetical structural stop, fraction of stop exits whose post-stop continuation is "wick-and-back" rather than "sustained adverse move." Phase 3s Q2 5m diagnostic on BTC established V1-family wick-fractions of 0.571–1.000; alt-symbol equivalents may be worse.
- **Mark-vs-trade stop-domain differences.** Phase 3s Q6 D1-A established mark-stop lag on BTC; alt-symbol equivalents would need to be evaluated separately.
- **Stop-hostile noise vs. sustained expansion.** Distinguish "moves that retrace after stop" from "moves that continue beyond stop"; a healthy setup substrate has more of the latter than the former.

### D. Liquidity / execution-risk feasibility

For each candidate symbol:

- **Volume stability.** Per-bar volume distribution across the research window; flag long volume-collapse windows.
- **Notional turnover proxy.** Volume × close as a per-bar notional proxy; per-symbol distribution.
- **Spread / slippage proxy requirements.** Phase 4ab notes that spread cannot be estimated from kline data alone; future feasibility memo would either accept the conservative §11.6 = 8 bps bound or note the requirement for separately authorized aggTrades / order-book acquisition.
- **Metadata constraints.** Per-symbol tick / step / min-quantity / min-notional vs. project sizing (0.25% risk × sizing equity / R-distance must produce position sizes that respect lot-size rounding).
- **Minimum size compatibility with §1.7.3 locks.** 0.25% risk on a research equity assumption × 1/R must produce a feasible position size on the candidate symbol.

### E. Idiosyncratic-risk feasibility

For each candidate symbol:

- **Listing continuity.** Verify continuous trading; flag delisting / relisting / suspension events.
- **Known ecosystem / regulatory / news risk categories.** Per-symbol qualitative risk profile (recorded in the future feasibility memo, not here).
- **Event-window labeling needs.** Identify whether known idiosyncratic events should be:
  - **excluded** (treat as out-of-distribution and drop from research populations);
  - **labeled** (keep in research populations but tag for sensitivity analysis);
  - **treated as unavoidable noise** (no special handling; accept variance).
- **Phase 4ab note:** event-windows are NOT to be treated as tradable signal (this would be event-trading; out of v1 scope per `.claude/rules/prometheus-core.md`).

### F. Cross-symbol comparability

Define for any future analysis:

- **Full-history view.** Each symbol uses its own listing-date-onward history.
- **Common-overlap view.** All symbols restricted to the intersection of available trading windows.
- **BTC / ETH continuity anchors.** Existing Phase 2 / Phase 4i evidence is preserved; any future alt-symbol candidate's evidence must be evaluated independently per symbol.
- **Alt-symbol independent pass / fail.** Each symbol passes or fails on its own evidence; ETH does not rescue BTC; no alt symbol rescues another alt symbol; cross-symbol consistency is a non-rescue check, not a promotion mechanism.
- **No symbol rescues another symbol.** Phase 4y forbidden-rescue principle preserved verbatim.

## 12. Explicit Non-Goals

Phase 4ab and any future data phase do NOT:

- **prove alt symbols are better than BTC / ETH.** Phase 4ab makes NO directional claim about alt-symbol superiority; alt-symbol strategy quality remains genuinely unknown until evidence exists.
- **create an alt-symbol strategy.** No strategy candidate is named, defined, or specified.
- **justify rerunning failed strategies on alts.** Re-evaluating R3 / R2 / F1 / D1-A / V2 / G1 / C1 on alt symbols is retrospective rescue and is forbidden by Phase 4m / Phase 4s / Phase 4y / Phase 4aa governance.
- **revise verdicts.** All retained verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1) preserved verbatim.
- **revise locks.** §11.6 / §1.7.3 / Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w preserved verbatim.
- **authorize backtests.** No backtest authorized by Phase 4ab; future Phase 4ac (if ever authorized) would also be docs-and-data only, not backtest.
- **authorize live / paper work.** Phase 4 canonical / paper / shadow remain unauthorized.
- **authorize market-type expansion.** No spot / COIN-M / options / cross-venue work authorized.

## 13. Recommended Future Phase Design

### Possible future phase name (recommendation; NOT authorized)

```text
Potential future Phase 4ac — Alt-Symbol Public Data Acquisition and Integrity Validation
```

(The name `Phase 4ac` is a placeholder; the operator may choose a different name. **Phase 4ab does NOT authorize this phase.** Phase 4ab only describes what such a phase would look like.)

### Recommended Phase 4ac scope (if ever authorized)

- **Docs-and-data.** Analogous to Phase 3q (5m supplemental acquisition) and Phase 4i (V2 acquisition). Phase 4ac would create a standalone acquisition orchestrator script (e.g., `scripts/phase4ac_alt_symbol_acquisition.py`), download public unauthenticated data, normalize to project-standard schema, generate manifests, run integrity gates, and produce a report.
- **Public unauthenticated bulk archives only.** `data.binance.vision` precedent. **No credentials.** **No `.env`.** **No authenticated REST.** **No private endpoints.** **No public-endpoint code calls** (the orchestrator must NOT call live endpoints; bulk archives are the only acquisition path). **No user stream.** **No WebSocket.** **No listenKey lifecycle.** **No exchange-write.**
- **No backtests.** Phase 4ac would be acquisition + integrity validation only.
- **No diagnostics.** Phase 4ac would NOT run Q1–Q7 or any other diagnostic.
- **No strategy specs.** No strategy candidate named.
- **Strict integrity gates.** Phase 3p §4.7 / Phase 4h §17 precedent preserved verbatim.
- **Manifests committed.** Per existing repository convention; raw and normalized data remain gitignored.
- **Closeout report required.** Phase 4ac closeout would record verdict (PASS / PARTIAL PASS / FAIL per family per symbol), commit SHAs, manifest references, and any partial-eligibility governance requirements that would need separate authorization before strategy use.

### Explicit non-authorization

- **Phase 4ac is NOT authorized by Phase 4ab.** Each future authorization is operator-driven and would be separately approved.
- **Phase 4ac would require a separate operator-authored authorization brief** locking the symbol set, intervals, data families, and integrity-gate parameters before execution.
- **The operator may also choose to remain paused indefinitely.** Authorizing Phase 4ac is not required after Phase 4ab.

## 14. Research Decision Menu

### Option A — Remain paused

Always procedurally valid. The strongest-evidence position remains unchanged after Phase 4ab: six terminal negative strategy outcomes versus two positive anchors (H0, R3) and two retained-research-only positions (R1a, R1b-narrow). Adding a data-requirements memo to the project record does not by itself produce strategy evidence; the operator may choose to remain paused for any duration.

### Option B — Merge Phase 4ab to main, then stop

Recommended (as primary) once Phase 4ab is operator-reviewed and accepted. Merging Phase 4ab adds the data-requirements / feasibility plan to the project record; subsequently, the operator may remain paused or separately authorize Phase 4ac (or any other phase). Merging Phase 4ab does NOT authorize Phase 4ac.

### Option C — Future Phase 4ac public data acquisition and integrity validation

Conditional next research step. Acceptable only **after** Phase 4ab is reviewed and the operator separately authorizes Phase 4ac. Phase 4ac would be docs-and-data, public unauthenticated only, no credentials, strict integrity gates, no backtests, no strategy specs.

### Option D — Narrow Phase 4ac scope further before acquisition

Acceptable if the operator wants fewer symbols (e.g., add only SOL first, defer XRP / ADA) or fewer data families (e.g., omit metrics and mark-price entirely from a first pass) before authorizing Phase 4ac. Narrowing reduces acquisition burden and keeps attribution cleaner.

### Option E — Jump directly to strategy discovery

**Not recommended.** Substrate evidence is still missing; without it, any new strategy-discovery memo on alt symbols would repeat the V2 / G1 / C1 pattern of substrate-blind candidate selection. Phase 4z observed that design-family adjacency was insufficiently filtered; analogously, substrate adjacency would be insufficiently filtered without first establishing alt-symbol substrate evidence.

### Option F — Direct old-strategy alt-symbol rerun

**Forbidden / not recommended.** Re-evaluating R3 / R2 / F1 / D1-A / V2 / G1 / C1 on alt symbols is retrospective rescue per Phase 4m / 4s / 4y / 4aa governance.

### Option G — Spot / COIN-M / options / other venue expansion

**Not recommended now.** Per Phase 4aa Section 5, mixing market-type and symbol-substrate axes contaminates attribution.

### Option H — Paper / shadow / live-readiness / exchange-write

**Forbidden / not authorized.** No validated strategy exists; phase-gate requirements not met.

## 15. Recommendation

```text
Primary recommendation:
After review, merge Phase 4ab into main, then remain paused unless the operator
separately authorizes a docs-and-data Phase 4ac public alt-symbol acquisition
and integrity-validation phase.

If Phase 4ac is later authorized, keep scope limited to Binance USDⓈ-M perpetuals,
the core five-symbol set (BTCUSDT / ETHUSDT / SOLUSDT / XRPUSDT / ADAUSDT), and
predeclared public unauthenticated data families per §6 (standard trade-price
klines required; funding required; mark-price klines conditional required;
metrics / OI optional conditional; aggTrades / tick / order-book deferred;
exchange metadata where available required).

Do not backtest yet.
Do not create a strategy yet.
Do not rescue prior strategies.
Do not expand market type yet.
```

**Phase 4ab primary recommendation: Option B — merge Phase 4ab to main, then stop (i.e., remain paused unless Phase 4ac is separately authorized).**

**Phase 4ab conditional secondary: Option A — remain paused without merging Phase 4ab.** Always procedurally valid. The operator may defer the merge for any duration.

**Phase 4ab NOT recommended:**

- **Option E — direct strategy discovery** — REJECTED.
- **Option F — direct old-strategy alt-symbol rerun** — FORBIDDEN.
- **Option G — market-type expansion** — premature.

**Phase 4ab FORBIDDEN:**

- **Option H — paper / shadow / live / exchange-write** — phase-gate requirements not met.

## 16. Preserved Locks and Boundaries

Phase 4ab preserves every retained verdict and project lock verbatim. **No verdict is revised. No project lock is changed. No governance file is amended.**

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

§11.6        : 8 bps HIGH per side (preserved verbatim)
§1.7.3       : project-level locks (preserved):
                - 0.25% risk per trade;
                - 2× leverage cap;
                - one position maximum;
                - mark-price stops where applicable.
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved;
                              strategy-agnostic)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility rule
                              (preserved)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4p                    : G1 strategy spec (preserved)
Phase 4q                    : G1 backtest-plan methodology (preserved)
Phase 4v                    : C1 strategy spec (preserved)
Phase 4w                    : C1 backtest-plan methodology (preserved)
Phase 4f / 4g / 4h / 4i / 4l / 4m / 4n / 4o / 4r / 4s / 4t / 4u / 4x / 4y / 4z / 4aa
                            : all preserved verbatim
Phase 4z recommendations    : remain recommendations only;
                              NOT adopted as binding governance by 4ab
Phase 4aa admissibility framework : remains recommendation only;
                                    NOT adopted as binding governance by 4ab
Phase 4ab recommendations   : remain recommendations only
                              (this memo's recommendations are not binding
                              governance; adoption requires a separate
                              governance-update phase)
```

## 17. Explicit Non-Authorization Statement

Phase 4ab does NOT authorize:

- **Phase 4ac** (alt-symbol public data acquisition and integrity validation; described conceptually but explicitly not authorized).
- **Phase 5.**
- **Phase 4 canonical.**
- **Any other named successor phase.**
- **Data acquisition** (no symbol; no interval; no funding; no mark-price; no metrics; no aggTrades; no order book).
- **Data download** (no `data.binance.vision` call; no Binance API call; no public-endpoint code).
- **Data modification** (no patching; no forward-fill; no interpolation; no imputation; no replacement; no regeneration).
- **Manifest creation** (no new manifests under `data/manifests/`).
- **Manifest modification** (existing manifests unchanged).
- **v003 or any other dataset version.**
- **Backtests** (none of any kind).
- **Diagnostics** (no Q1–Q7 rerun; no new diagnostic phase).
- **Strategy specs.**
- **Hypothesis specs.**
- **Backtest plans.**
- **Implementation** (no `src/prometheus/` modification; no test modification; no script modification; no script creation; no runtime code).
- **Old-strategy rescue** (no R3 / R2 / F1 / D1-A / V2 / G1 / C1 rescue; no R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid).
- **Paper / shadow / live operation.**
- **Live-readiness.**
- **Deployment.**
- **Production-key creation.**
- **Authenticated APIs.**
- **Private endpoints.**
- **Public endpoint calls in code.**
- **User stream / WebSocket / listenKey lifecycle.**
- **Exchange-write capability.**
- **MCP tooling.**
- **Graphify tooling.**
- **`.mcp.json` creation or modification.**
- **Credentials** (no `.env`; no key storage; no key request).
- **Adoption of Phase 4z recommendations as binding governance.**
- **Adoption of Phase 4aa admissibility framework as binding governance.**
- **Adoption of any Phase 4ab recommendation as binding governance.**
- **Successor phase.**

**Phase 4ab does NOT modify:**

- source code under `src/prometheus/`;
- tests;
- scripts (no modification of any existing acquisition / backtest / analysis script; no new script created);
- data under `data/raw/`, `data/normalized/`, or `data/manifests/`;
- existing strategy specifications (`docs/03-strategy-research/v1-breakout-strategy-spec.md` and related are preserved verbatim);
- governance files (`docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, or any specialist governance document — except the narrow `docs/00-meta/current-project-state.md` update required to record Phase 4ab);
- project locks, retained verdicts, or any prior phase's substantive content.

**Phase 4ab output:**

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ab_alt-symbol-data-requirements-feasibility.md` (this memo);
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ab_closeout.md` (closeout);
- narrow update to `docs/00-meta/current-project-state.md` recording Phase 4ab (no broad documentation refresh).

**Phase 4ab is preserved on its feature branch unless and until the operator separately instructs a merge.** main remains unchanged at `a8e81bdf86164f86fcf3b09aaac5f40a15f55fc3` after Phase 4ab branch creation.

---

**Phase 4ab is text-only. No source code, tests, scripts, data, manifests, governance files, retained verdicts, or project locks were created or modified. Phase 4ab translates Phase 4aa's alt-symbol substrate question into concrete docs-only data-requirements and feasibility planning. Phase 4ab does NOT authorize data acquisition, manifest creation, backtest, diagnostics, strategy spec, hypothesis spec, backtest-plan, implementation, paper / shadow / live operation, exchange-write, production keys, authenticated APIs, private endpoints, public endpoint calls in code, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, or any successor phase. C1 first-spec remains terminally HARD REJECTED. V2 / G1 / R2 / F1 / D1-A all preserved per accumulated governance. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. R1a / R1b-narrow remain RETAINED — NON-LEADING. Phase 4z recommendations remain recommendations only. Phase 4aa admissibility framework remains recommendation only. Phase 4ab recommendations remain recommendations only. Recommended state: remain paused (primary; Option B merge Phase 4ab then stop) — Phase 4ac (conditional next; not authorized by Phase 4ab). No next phase authorized.**
