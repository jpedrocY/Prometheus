# Phase 4ad — Alt-Symbol Gap-Governance and Scope-Revision Memo

**Authority:** Operator authorization for Phase 4ad (docs-only governance / scope-revision memo resolving how future alt-symbol substrate-feasibility work may treat Phase 4ac gap / invalid-window findings before any substrate-feasibility analysis, strategy discovery, backtest, diagnostics, or strategy work is allowed). Phase 4ac (alt-symbol public data acquisition / integrity validation; merged 3478d05); Phase 4ab (alt-symbol data-requirements / feasibility memo); Phase 4aa (alt-symbol market-selection / admissibility memo); Phase 4i (V2 acquisition pattern); Phase 3q (5m supplemental + mark-price acquisition); Phase 3p §4.7 (strict integrity gate); Phase 3r §8 (mark-price gap governance precedent); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 4j §11 (metrics OI-subset partial-eligibility binding precedent); Phase 4k (V2 backtest-plan); Phase 4p (G1 strategy spec); Phase 4q (G1 backtest-plan); Phase 4v (C1 strategy spec); Phase 4w (C1 backtest-plan); Phase 4z (post-rejection research-process redesign); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/04-data/historical-data-spec.md`; `docs/04-data/dataset-versioning.md`; `docs/04-data/timestamp-policy.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4ad — **Alt-Symbol Gap-Governance and Scope-Revision Memo** (docs-only). Defines explicit future-use rules for treatment of Phase 4ac gap / invalid-window findings (mark-price upstream invalid windows; SOL/XRP early-2022 trade-price kline gaps); proposes the Phase 4ad Mark-Price Invalid-Window Exclusion Rule (Rule A) and the Phase 4ad SOL/XRP Early-2022 Kline Gap Scope Rule (Rule B; with three policy options B1/B2/B3); proposes a conservative PASS-Only Subset Rule (Rule C); recommends scope for any future Phase 4ae substrate-feasibility analysis memo. **Phase 4ad is text-only.** No data acquired or modified. No manifest created or modified. No backtest run. No diagnostic run. No Q1–Q7 rerun. No substrate-feasibility execution. No strategy candidate, hypothesis-spec, strategy-spec, or backtest-plan created. No `src/prometheus/`, tests, or scripts modified. No retained verdict revised. No project lock changed. No governance file amended (beyond the narrow `current-project-state.md` update). **No successor phase authorized.**

**Branch:** `phase-4ad/alt-symbol-gap-governance-scope-revision`. **Memo date:** 2026-05-04 UTC.

---

## 1. Purpose

Phase 4ad resolves how future alt-symbol substrate-feasibility work may treat the Phase 4ac gap / invalid-window findings — *before* any substrate-feasibility analysis, strategy discovery, backtest, diagnostics, or strategy work is allowed.

**Phase 4ad is docs-only.**

- **No data acquisition.** No new dataset is downloaded, ingested, normalized, or materialized.
- **No data modification.** No patching / forward-fill / interpolation / imputation / synthesis / regeneration / replacement.
- **No manifest creation or modification.** Existing manifests inspected read-only for documentation/planning context only; no manifest is altered.
- **No backtest.** No backtest is run, planned, or scoped.
- **No diagnostics.** No Q1–Q7 rerun. No new diagnostic phase.
- **No substrate-feasibility execution.** Phase 4ad does NOT perform cost-to-volatility / opportunity-rate / wick / liquidity / idiosyncratic-risk / cross-symbol comparability calculations; those would belong to a future separately authorized Phase 4ae substrate-feasibility analysis memo.
- **No strategy candidate.** No new strategy is named, defined, or specified.
- **No hypothesis-spec memo.** No new hypothesis is named.
- **No strategy-spec memo.** No new strategy spec is authored.
- **No backtest-plan memo.** No backtest methodology is specified.
- **No implementation.** No `src/prometheus/`, tests, or scripts modified.
- **No live-readiness.** No paper / shadow / live operation authorized, planned, or implied.
- **No exchange-write.** No production keys, authenticated APIs, private endpoints, user stream, WebSocket, exchange-write capability, MCP, Graphify, or `.mcp.json` touched.

Phase 4ad records future-use governance rules as **proposals adopted by Phase 4ad** for any future Phase 4ae-equivalent substrate-feasibility analysis memo. The rules apply prospectively to future research-use of Phase 4ac data only; they do **not** rewrite manifests, modify data, revise prior verdicts, or change project locks.

## 2. Relationship to Phase 4ac

### Brief Phase 4ac summary

Phase 4ac (merged at `3478d05`) acquired the predeclared core symbol set:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

It used public unauthenticated `data.binance.vision` bulk archives only. It acquired 35 dataset families × 52 monthly archives = **1 820 monthly archives** total, all SHA256-verified against `.CHECKSUM` companions with **zero mismatches**.

It created 35 manifests under `data/manifests/`:

- **9** datasets `research_eligible: true`;
- **26** datasets `research_eligible: false`.

### Carry-over governance status

- **Phase 4ac did not authorize Phase 4ad** or any successor phase. The operator separately authorized Phase 4ad as a docs-only governance / scope-revision memo on top of Phase 4ac evidence.
- **Phase 4ac results were data / integrity evidence only**, not binding governance.
- Phase 4ad uses Phase 4ac evidence as a planning input only.
- Phase 4ad does **not** alter any Phase 4ac manifest. Phase 4ad does **not** flip any Phase 4ac `research_eligible` flag.
- Phase 4ad's proposed rules apply **prospectively** to future analysis-time use of Phase 4ac data; they do not modify Phase 4ac data on disk or in committed manifests.

## 3. Phase 4ac Gap Topology

This section restates the relevant gap topology recorded by the Phase 4ac merge-closeout. The same gap windows are also recorded verbatim in the affected manifests' `quality_checks.gap_locations` and `invalid_windows`.

### A. Clean PASS datasets (`research_eligible: true`)

```text
binance_usdm_btcusdt_1h__v001              (37 944 bars; 0 gaps)
binance_usdm_ethusdt_1h__v001              (37 944 bars; 0 gaps)
binance_usdm_adausdt_15m__v001            (151 776 bars; 0 gaps)
binance_usdm_adausdt_30m__v001             (75 888 bars; 0 gaps)
binance_usdm_adausdt_1h__v001              (37 944 bars; 0 gaps)
binance_usdm_adausdt_4h__v001               (9 486 bars; 0 gaps)
binance_usdm_solusdt_funding__v001          (4 818 events)
binance_usdm_xrpusdt_funding__v001          (4 743 events)
binance_usdm_adausdt_funding__v001          (4 743 events)
```

These 9 datasets passed the strict Phase 3p §4.7 / Phase 4h §17 integrity gate with zero gaps and full 2022-01..2026-04 coverage where applicable. They are research-eligible globally without requiring any Phase 4ad rule.

### B. Mark-price invalid-window datasets (`research_eligible: false`; bounded upstream gaps)

Cross-symbol upstream mark-price gaps recorded by Phase 4ac (consistent with the previously-documented Phase 3q / Phase 3r §8 mark-price invalid-window pattern):

| Gap window (UTC) | Symbols affected (mark-price family) |
| --- | --- |
| 2022-07-30 23:30 .. 2022-08-01 00:00 | BTC only |
| 2022-10-01 23:30 .. 2022-10-03 00:00 | BTC, ETH, SOL, XRP, ADA |
| 2023-02-23 23:30 .. 2023-02-25 00:00 | BTC, ETH, SOL, XRP, ADA |
| 2023-11-10 03:30 .. 2023-11-10 04:00 | SOL, XRP, ADA (visible at 15m granularity; submerged inside other-interval bars at 30m / 1h / 4h) |

Affected manifests:

```text
binance_usdm_btcusdt_markprice_30m__v001       (3 gap windows)
binance_usdm_btcusdt_markprice_1h__v001        (3 gap windows)
binance_usdm_btcusdt_markprice_4h__v001        (3 gap windows)
binance_usdm_ethusdt_markprice_30m__v001       (2 gap windows)
binance_usdm_ethusdt_markprice_1h__v001        (2 gap windows)
binance_usdm_ethusdt_markprice_4h__v001        (2 gap windows)
binance_usdm_solusdt_markprice_15m__v001       (3 gap windows)
binance_usdm_solusdt_markprice_30m__v001       (2 gap windows)
binance_usdm_solusdt_markprice_1h__v001        (2 gap windows)
binance_usdm_solusdt_markprice_4h__v001        (2 gap windows)
binance_usdm_xrpusdt_markprice_15m__v001       (3 gap windows)
binance_usdm_xrpusdt_markprice_30m__v001       (2 gap windows)
binance_usdm_xrpusdt_markprice_1h__v001        (2 gap windows)
binance_usdm_xrpusdt_markprice_4h__v001        (2 gap windows)
binance_usdm_adausdt_markprice_15m__v001       (3 gap windows)
binance_usdm_adausdt_markprice_30m__v001       (2 gap windows)
binance_usdm_adausdt_markprice_1h__v001        (2 gap windows)
binance_usdm_adausdt_markprice_4h__v001        (2 gap windows)
```

All 18 mark-price kline manifests are globally `research_eligible: false`. The gap pattern is bounded, well-documented, and upstream (i.e., the source `data.binance.vision` archives themselves do not contain bars within these windows).

### C. SOL / XRP early-2022 trade-price kline gaps (`research_eligible: false`)

Per-symbol early-2022 trade-price kline gaps observed only in SOL and XRP (NOT in ADA, NOT in BTC, NOT in ETH):

| Gap window (UTC) | Symbols affected (trade-price kline family) |
| --- | --- |
| 2022-02-25 23:45 .. 2022-03-01 00:00 (≈ 2 days) | SOL, XRP |
| 2022-03-31 23:45 .. 2022-04-03 00:00 (≈ 2 days) | SOL, XRP |

Affected manifests:

```text
binance_usdm_solusdt_15m__v001    (2 gap windows)
binance_usdm_solusdt_30m__v001    (2 gap windows)
binance_usdm_solusdt_1h__v001     (2 gap windows)
binance_usdm_solusdt_4h__v001     (2 gap windows)
binance_usdm_xrpusdt_15m__v001    (2 gap windows)
binance_usdm_xrpusdt_30m__v001    (2 gap windows)
binance_usdm_xrpusdt_1h__v001     (2 gap windows)
binance_usdm_xrpusdt_4h__v001     (2 gap windows)
```

All 8 SOL / XRP trade-price kline manifests are globally `research_eligible: false`. The gap pattern is symmetric across SOL and XRP; ADA does **not** show these gaps.

### D. ADA clean trade-price subset

ADAUSDT 15m / 30m / 1h / 4h trade-price klines passed the strict gate with full 2022-01-01..2026-04-30 coverage and zero gaps. ADA is the only alt symbol with a clean kline subset in Phase 4ac evidence.

## 4. Governance Question

```text
Can future alt-symbol substrate-feasibility analysis use datasets that failed
strict global eligibility due to known, bounded, source-side gaps, and if so,
under what explicit exclusion rules?
```

### Phase 4ad answer (binding only as Phase 4ad-defined future-use rules)

Phase 4ad answers **yes, under explicit exclusion rules**, with the following constraints:

1. **Global `research_eligible: false` remains true** for every affected manifest. Phase 4ad does **not** flip eligibility flags. The Phase 4ac manifests remain unchanged.
2. **Phase 4ad defines future-use partial-eligibility / exclusion rules** that any future Phase 4ae-equivalent substrate-feasibility analysis memo *must* apply if it intends to consume the affected datasets. The rules are Rule A (mark-price invalid-window exclusion), Rule B (SOL/XRP early-2022 kline scope policy), and Rule C (PASS-only fallback).
3. **The rules apply prospectively to future analysis only.** They do not rewrite manifests. They do not modify on-disk data. They do not retroactively re-classify any Phase 4ac dataset's research-eligibility flag.
4. **No data is patched.** No forward-fill / interpolation / imputation / synthesis / replacement / silent omission. Bounded upstream gaps remain bounded upstream gaps.
5. **No prior verdict is revised.** All retained verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1) preserved verbatim.
6. **No project lock is changed.** All Phase 2 / Phase 3 / Phase 4 governance preserved verbatim.

## 5. Existing Precedents

Two project precedents serve as templates for Phase 4ad. Each is restated read-only and preserved verbatim.

### 5.1 Phase 3r §8 mark-price gap governance (precedent)

Phase 3r §8 established the project's binding pattern for mark-price gap handling in retrospective Q6-style analysis:

- **Known invalid windows are exclusion zones, not patch zones.**
- **Per-trade exclusion test** based on Q6 analysis-window intersection: any trade whose analysis window intersects a known invalid window is excluded from that trade's mark-price-dependent analysis.
- **Excluded trades counted and reported** by candidate / symbol / side / exit-type / gap-window.
- **Q6 conclusions labeled** "conditional on valid mark-price coverage" verbatim.
- **No automatic prior-verdict revision.**
- **No strategy rescue.**
- **No parameter change.**
- **No live-readiness implication.**
- **No silent §8 rule revision.**
- **Per-trade exclusion algorithm must be predeclared** in any future diagnostics-execution phase brief that intends to use Q6 with mark-price data.

Phase 3r §8 is preserved verbatim by Phase 4ad. Phase 4ad's Rule A (below) is structurally analogous to Phase 3r §8 but applies prospectively to future alt-symbol substrate-feasibility analysis (rather than retrospective Q6 5m diagnostics).

### 5.2 Phase 4j §11 metrics OI-subset partial-eligibility rule (precedent)

Phase 4j §11 established the project's binding pattern for partial-eligibility within a globally-failed dataset:

- **Global metrics family remains `research_eligible: false`.**
- **OI subset** (`create_time`, `symbol`, `sum_open_interest`, `sum_open_interest_value`) **may be partial-eligible** under strict per-bar completeness conditions: any 30m signal bar requires **all six aligned 5-minute records** present at offsets 0, 5, 10, 15, 20, 25 minutes from the bar's `open_time` AND each must have non-NaN `sum_open_interest` AND non-NaN `sum_open_interest_value`.
- **Optional ratio columns remain forbidden** (Phase 4j §11.3): `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`, `count_long_short_ratio`, `sum_taker_long_short_vol_ratio`.
- **Partial eligibility does NOT create broad dataset eligibility.** It is a narrow, predeclared, per-bar feature-subset eligibility scoped to a specific governance memo.
- **The per-bar exclusion algorithm must be predeclared** verbatim in any future research phase that intends to use the OI subset.

Phase 4j §11 is preserved verbatim by Phase 4ad. Phase 4ad does **not** propose using the metrics OI subset (Phase 4ac did not acquire metrics families for alt symbols). Phase 4j §11 is recorded as the relevant template precedent for narrow partial-eligibility.

### 5.3 Use of precedents

Phase 4ad uses Phase 3r §8 and Phase 4j §11 as **templates, not as excuses to relax integrity**. Strict-gate pass / fail semantics are preserved; partial-eligibility rules narrow the scope of allowed use rather than broaden the eligibility flag.

## 6. Proposed Rule A — Mark-Price Invalid-Window Exclusion Rule for Alt-Symbol Research

**Rule name:** Phase 4ad Mark-Price Invalid-Window Exclusion Rule.

**Scope:** prospective; applies only to future research-time use of Phase 4ac mark-price datasets in any future separately authorized Phase 4ae-equivalent substrate-feasibility analysis memo.

### 6.1 Rule statement

1. **Global eligibility remains false.** Mark-price kline manifests with known invalid windows remain globally `research_eligible: false`. Phase 4ad does NOT flip this flag.
2. **Conditional usability.** They MAY be treated as conditionally usable only for analyses that explicitly apply the Phase 4ad Mark-Price Invalid-Window Exclusion Rule.
3. **Per-window exclusion test.** Any of the following observation types must be excluded from mark-price-dependent analysis if it intersects a known mark-price invalid window:
   - bar (one mark-price kline);
   - trade (a candidate or actual trade observation);
   - candidate event (an event under feasibility-statistic computation);
   - diagnostic window (a window over which a metric is computed);
   - stop-domain window (a window over which mark-price stop behavior is examined);
   - any other analysis window that uses mark-price data over a time interval intersecting an invalid window.
4. **Exclusion counts must be reported** by:
   - symbol;
   - interval;
   - data family (mark-price kline at a specific interval);
   - side, if applicable;
   - candidate / strategy, if applicable (NOT for Phase 4ad-scope analysis since Phase 4ad does not authorize strategy work);
   - event type, if applicable;
   - invalid-window ID (one row per (symbol, interval, gap window)).
5. **No patching / forward-fill / interpolation / imputation / synthesis / replacement.** Bounded upstream gaps remain bounded upstream gaps.
6. **Conclusions must be labeled verbatim:**

   ```text
   conditional on valid mark-price coverage
   ```

   in the future analysis report. Conclusions that omit this label are invalid under Rule A.

### 6.2 Authorization scope

Rule A authorizes only:

- Phase 4ae-equivalent **substrate-feasibility analysis** computations limited to the Section 10 allowed-output list.

Rule A does **NOT** authorize:

- mark-price backtests;
- live-readiness;
- mark-price stop modeling for paper / live;
- any change to Phase 3v stop-trigger-domain governance;
- any revision of any existing verdict;
- any strategy candidate creation;
- any old-strategy rescue.

### 6.3 Predeclaration requirement

Any future analysis intending to apply Rule A must:

- predeclare the exact list of intended observation-window types (per §6.1.3);
- predeclare the exact set of invalid windows being honored (per §3.B);
- predeclare the per-symbol and per-interval reporting tables (per §6.1.4);
- include the verbatim conclusion-label phrase (per §6.1.6) in its predeclaration;
- include explicit non-authorization acknowledgements (per §6.2 forbidden list).

Rule A predeclaration discipline mirrors Phase 3r §8 / Phase 3p §4.7 / Phase 4j §11 conventions.

## 7. Proposed Rule B — SOL / XRP Early-2022 Trade-Price Kline Gap Scope Rule

**Rule name:** Phase 4ad SOL/XRP Early-2022 Kline Gap Scope Rule.

**Scope:** prospective; applies only to future research-time use of Phase 4ac SOL / XRP trade-price kline datasets in any future separately authorized Phase 4ae-equivalent substrate-feasibility analysis memo.

### 7.1 Rule statement

1. **Global eligibility remains false** for the 8 affected SOL / XRP kline manifests (per §3.C). Phase 4ad does NOT flip these flags.
2. **Conditional usability under a declared scope policy.** SOL / XRP trade-price klines MAY be conditionally usable only under one of three predeclared scope policies (B1, B2, B3 below). Any future analysis must select **exactly one** policy *before* analysis begins, and must apply it consistently throughout the analysis.

### 7.2 Policy B1 — Common post-gap start (cross-symbol fairness)

**Use:**

```text
Analysis start: 2022-04-03 00:00 UTC
              (the first complete bar after the second gap)
```

**Apply consistently:**

- For SOL and XRP, use 2022-04-03 onward as analysis start.
- If cross-symbol fairness is required (e.g., comparing SOL / XRP / ADA / BTC / ETH on equal time windows), apply the **same common-overlap start** to **all** symbols in the comparison.
- Do NOT use 2022-01-01..2022-04-02 SOL / XRP data even if BTC / ETH / ADA data exists in that window. Cross-symbol comparison must use a common time domain.

**When to choose B1:** when cross-symbol comparison fairness is the primary methodological concern. This is the recommended default for cross-symbol substrate-feasibility analysis.

### 7.3 Policy B2 — Full-history with invalid-window exclusion

**Use:**

```text
Analysis start: 2022-01-01 00:00 UTC (full history per symbol)

Per-bar / per-event / per-window exclusions for SOL and XRP only:
  Exclude observations intersecting:
    2022-02-25 23:45 .. 2022-03-01 00:00
    2022-03-31 23:45 .. 2022-04-03 00:00
```

**Reporting requirement:**

- All exclusions counted by symbol, interval, observation type, and gap-window ID.
- Exclusion totals reported in the future analysis output tables.

**When to choose B2:** when full-history descriptive analysis is needed and the exclusions can be fully reported. NOT recommended for cross-symbol fairness comparison (B1 preferred for that case).

### 7.4 Policy B3 — PASS-only subset (do not use SOL / XRP klines)

**Use:**

```text
Do NOT use SOL / XRP trade-price kline datasets for substrate-feasibility
analysis until a future acquisition or governance change exists.

Restrict future analysis to the Phase 4ac PASS subset (per §3.A).
```

**When to choose B3:** when conservative PASS-only analysis is desired. Most-conservative fallback. Limited substrate coverage (excludes SOL / XRP price-action substrate at kline level).

### 7.5 Recommended default

Phase 4ad recommends **Policy B1 (common post-gap start)** as default for cross-symbol substrate-feasibility analysis. Rationale:

- Preserves fairness across symbols (every symbol uses the same time domain).
- Avoids per-event exclusion complexity.
- Honors the 2-day gap as a structural artefact rather than amortizing it across many small per-bar exclusions.
- Compatible with the project's BTCUSDT-primary / ETHUSDT-comparison protocol (Phase 4y forbidden-rescue principle preserved: ETH cannot rescue BTC; no symbol rescues another symbol; Rule B does not authorize cross-symbol rescue).

**Policy B2 is allowed** for full-history descriptive analysis only when exclusions are fully reported in compliance with §7.3.

**Policy B3 is acceptable** for highly conservative PASS-only analysis. It is more restrictive than B1 / B2; substrate-feasibility coverage is correspondingly narrower.

### 7.6 Authorization scope

Rule B authorizes only:

- Phase 4ae-equivalent **substrate-feasibility analysis** computations limited to the Section 10 allowed-output list, under one of B1 / B2 / B3 with predeclaration.

Rule B does **NOT** authorize:

- backtests on SOL / XRP klines;
- old-strategy alt-symbol rerun (forbidden as retrospective rescue per Phase 4m / 4s / 4y / 4aa);
- strategy candidate creation;
- live-readiness;
- any revision of any existing verdict;
- mixing of policies within a single analysis (must select B1 OR B2 OR B3, not multiple).

## 8. Proposed Rule C — PASS-Only Subset Rule (conservative fallback)

**Rule name:** Phase 4ad PASS-Only Subset Rule.

**Scope:** prospective; applies as a conservative fallback for any future substrate-feasibility analysis that wishes to avoid Rule A and Rule B exclusion-handling entirely.

### 8.1 PASS-only allowed datasets

```text
binance_usdm_btcusdt_1h__v001              (1h direct trade-price klines)
binance_usdm_ethusdt_1h__v001              (1h direct trade-price klines)
binance_usdm_adausdt_15m__v001             (15m trade-price klines)
binance_usdm_adausdt_30m__v001             (30m trade-price klines)
binance_usdm_adausdt_1h__v001              (1h trade-price klines)
binance_usdm_adausdt_4h__v001              (4h trade-price klines)
binance_usdm_solusdt_funding__v001         (funding events)
binance_usdm_xrpusdt_funding__v001         (funding events)
binance_usdm_adausdt_funding__v001         (funding events)
```

These 9 datasets are globally `research_eligible: true` and may be used directly by any future substrate-feasibility analysis without invoking Rule A or Rule B.

### 8.2 Limitations of Rule C

- **PASS-only analysis cannot evaluate SOL / XRP price-action substrate at kline level.** SOL / XRP klines are excluded under Rule C.
- **PASS-only analysis cannot evaluate mark-price stop-domain behavior.** All mark-price datasets are excluded under Rule C (because they all carry upstream invalid windows).
- **PASS-only analysis cannot perform full cross-symbol kline comparison at common intervals.** The PASS subset includes BTC / ETH only at 1h, plus ADA at all four intervals. SOL / XRP are absent from the kline subset.
- **PASS-only analysis can still support limited substrate-feasibility framing**, including cross-symbol funding behavior comparison and ADA-vs-{BTC/ETH at 1h} kline behavior comparison.
- **PASS-only analysis is too narrow for the full Phase 4ab substrate question** because it cannot compare SOL / XRP kline behavior to BTC / ETH / ADA at any interval.

### 8.3 When to choose Rule C

- When the operator wants the most conservative posture and is willing to accept narrow coverage.
- When future authorization wishes to avoid Rule A / Rule B exclusion-handling complexity entirely.
- As a baseline against which Rule A or Rule B analyses can be compared (i.e., a future analysis could optionally report PASS-only baseline numbers alongside Rule A or Rule B numbers).

### 8.4 Authorization scope

Rule C authorizes only:

- Phase 4ae-equivalent **substrate-feasibility analysis** computations limited to the Section 10 allowed-output list, restricted to the 9 PASS datasets.

Rule C does **NOT** authorize:

- backtests on PASS datasets;
- old-strategy reruns on PASS datasets;
- strategy candidate creation;
- live-readiness;
- any revision of any existing verdict.

## 9. Recommended Future Analysis Scope

This section recommends the scope for any future Phase 4ae substrate-feasibility analysis memo. **Phase 4ad does NOT authorize Phase 4ae.** The recommendation below is conditional and applies only if the operator separately authorizes a future Phase 4ae-equivalent phase.

### 9.1 Recommended scope

For any future Phase 4ae substrate-feasibility analysis (if ever authorized):

- **Symbols:** the Phase 4ac core five — BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, ADAUSDT.
- **Trade-price kline scope policy:** Rule B Policy B1 (common post-gap start at 2022-04-03 UTC) for cross-symbol comparison.
  - For SOL / XRP, use 2022-04-03 onward.
  - For BTC / ETH / ADA, also use 2022-04-03 onward in cross-symbol comparison cells (so the comparison time domain is identical).
  - Per-symbol full-history descriptive cells may use Policy B2 with reported exclusions if useful.
- **Trade-price kline intervals available:**
  - BTC: 15m / 30m / 4h are covered by Phase 2 / Phase 4i existing manifests (NOT acquired by Phase 4ac); 1h direct kline is Phase 4ac NEW (PASS).
  - ETH: same shape as BTC (15m / 30m / 4h from Phase 2 / Phase 4i; 1h NEW PASS from Phase 4ac).
  - ADA: 15m / 30m / 1h / 4h all NEW PASS from Phase 4ac.
  - SOL: 15m / 30m / 1h / 4h NEW from Phase 4ac, all `research_eligible: false`; usable only under Rule B.
  - XRP: same shape as SOL.
- **Mark-price kline scope policy:** Rule A. Mark-price datasets used **only** if the future analysis explicitly needs stop-domain or mark-vs-trade behavior; otherwise default to NOT using mark-price datasets at all.
- **Mark-price kline intervals available (under Rule A):**
  - BTC: 15m (Phase 2; existing); 30m / 1h / 4h (Phase 4ac NEW; `research_eligible: false`).
  - ETH: same shape as BTC.
  - SOL / XRP / ADA: 15m / 30m / 1h / 4h (Phase 4ac NEW; `research_eligible: false`).
- **Funding history scope:**
  - BTC / ETH: existing Phase 2 v001 / v002 funding manifests.
  - SOL / XRP / ADA: Phase 4ac NEW funding manifests (PASS).
- **Metrics / OI:** NOT used. Phase 4ac did not acquire metrics for alt symbols, and Phase 4j §11 is preserved as governance template only (not invoked by Phase 4ad / Phase 4ae scope).
- **AggTrades / tick / order-book:** NOT used (Phase 4ab §6.E deferred / NOT recommended; Phase 4ac did not acquire).
- **No strategy performance evaluation.** No strategy reruns. No PnL.
- **No prior-strategy alt-symbol rerun** (forbidden retrospective rescue).

### 9.2 Anti-rescue discipline preserved

Any future Phase 4ae analysis must:

- preserve the Phase 4y forbidden-rescue principle: no symbol rescues another symbol; ETH cannot rescue BTC; no alt symbol rescues any other alt symbol;
- preserve the Phase 4m 18-requirement fresh-hypothesis validity gate (recorded as recommendation);
- preserve the Phase 4z proposed admissibility framework (recorded as recommendation);
- NOT attempt to revive any rejected strategy on any alt symbol;
- NOT introduce any strategy candidate;
- NOT propose any threshold or rule from Phase 4ac forensic numbers (e.g., the ADA clean-coverage observation does NOT license an ADA-only strategy candidate).

## 10. Future Analysis Outputs Allowed

This section enumerates what a future Phase 4ae substrate-feasibility analysis memo **may compute**, if separately authorized. The list is bounded by §10.1 (allowed) and §10.2 (forbidden).

### 10.1 Allowed (substrate-feasibility metrics only)

Allowed only as substrate-feasibility metrics, **not** as strategy signals:

- **Cost-to-volatility ratios** per symbol per interval (§11.6 = 8 bps HIGH per side preserved).
- **ATR / median range distributions** per symbol per interval.
- **Expansion-event frequencies** per symbol per interval (descriptive only, not predictive).
- **Trend-regime frequencies** per symbol per interval (descriptive only, not predictive).
- **Wick / stop-pathology descriptive measures** per symbol per interval (analogous in form to Phase 3s Q2 5m diagnostic but applied to substrate-feasibility characterization, NOT to strategy signals).
- **Funding-rate distributions** per symbol.
- **Volume / notional turnover proxies** from kline data (volume × close per bar) per symbol per interval.
- **Common-overlap coverage tables** per symbol set per interval per scope policy.
- **Event-count sufficiency summaries** for any predeclared event type (e.g., expansion frequency above some threshold; descriptive only).
- **Per-symbol gap / exclusion tabulation** under Rule A and / or Rule B reporting requirements.
- **Cross-symbol descriptive comparison** of any of the above metrics, with cross-symbol fairness preserved per Rule B Policy B1 (or Policy B2 with reported exclusions).

### 10.2 Forbidden

Forbidden for any future Phase 4ae substrate-feasibility analysis (regardless of which Rule is used):

- **Strategy PnL** computation.
- **Entry / exit rule backtests.**
- **Optimization** (parameter search; threshold tuning; cost-cell optimization).
- **Threshold selection for a strategy.**
- **Old-strategy reruns** (R3 / R2 / F1 / D1-A / V2 / G1 / C1 on any symbol).
- **R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid** creation.
- **Candidate strategy naming.**
- **Hypothesis-spec or strategy-spec or backtest-plan** creation.
- **Paper / live conclusions.**
- **Live-readiness conclusions.**
- **Mark-price stop-modeling for paper / live operation** (Phase 3v §8 governance preserved; Rule A is for descriptive substrate-feasibility characterization only).

## 11. Decision Menu

Phase 4ad offers the following operator decision menu. Each option represents a possible next step; the operator decides which (if any) to authorize. **Phase 4ad does NOT authorize any of these options; each requires separate operator authorization.**

### Option A — Remain paused

Always procedurally valid.

### Option B — Merge Phase 4ad to main, then stop

Recommended if Phase 4ad is operator-reviewed and accepted. Merging Phase 4ad adopts Rules A / B / C as Phase 4ad-defined future-use rules (recorded in this memo); subsequently, the operator may remain paused or separately authorize Phase 4ae.

### Option C — Future Phase 4ae substrate-feasibility analysis memo

Conditional next step after Phase 4ad is merged and separately authorized. Docs-only or analysis-only depending on operator brief; **no strategy / backtest** in any case.

### Option D — Future narrower PASS-only feasibility memo

Acceptable conservative alternative under Rule C. Defers Rule A / B exclusion-handling.

### Option E — Future data re-acquisition / alternate-source memo

**Not recommended now** unless gaps block all useful analysis. The Phase 4ac gaps are bounded; Rule A and Rule B handle them prospectively without re-acquisition.

### Option F — Direct strategy discovery

**Not recommended.** Substrate-feasibility evidence is still being established. Skipping substrate work and going directly to discovery would repeat the V2 / G1 / C1 design-pattern of substrate-blind candidate selection.

### Option G — Direct old-strategy alt-symbol rerun

**Forbidden.** Re-evaluating R3 / R2 / F1 / D1-A / V2 / G1 / C1 on alt symbols is retrospective rescue per Phase 4m / 4s / 4y / 4aa governance preserved verbatim.

### Option H — Backtest / diagnostics / Q1–Q7 rerun

**Forbidden** unless separately authorized after substrate-feasibility and strategy-spec work. Phase 4ad does NOT authorize any of these.

### Option I — Paper / shadow / live-readiness / exchange-write

**Forbidden.** No validated strategy exists; phase-gate requirements not met.

## 12. Recommendation

```text
Primary recommendation:
Merge Phase 4ad into main, then remain paused unless the operator separately
authorizes a Phase 4ae substrate-feasibility analysis memo.

For any future Phase 4ae cross-symbol substrate-feasibility analysis, use the
Phase 4ad SOL/XRP Early-2022 Kline Gap Scope Rule with Policy B1 common
post-gap start as the default.

Use the Phase 4ad Mark-Price Invalid-Window Exclusion Rule for any mark-
price-dependent analysis.

Do not backtest yet.
Do not create a strategy yet.
Do not rescue prior strategies.
Do not expand market type yet.
```

**Phase 4ad primary recommendation: Option B — merge Phase 4ad to main, then stop (i.e., remain paused unless Phase 4ae is separately authorized).**

**Phase 4ad conditional secondary: Option A — remain paused without merging Phase 4ad.** Always procedurally valid.

**Phase 4ad NOT recommended:**

- **Option E — data re-acquisition** — premature; bounded gaps are well-handled by Rules A / B.
- **Option F — direct strategy discovery** — REJECTED; substrate evidence still being established.

**Phase 4ad FORBIDDEN:**

- **Option G — old-strategy alt-symbol rerun** — FORBIDDEN.
- **Option H — backtest / diagnostics / Q1–Q7 rerun** — FORBIDDEN at this boundary.
- **Option I — paper / shadow / live / exchange-write** — FORBIDDEN.

## 13. Preserved Locks and Boundaries

Phase 4ad preserves every retained verdict and project lock verbatim. **No verdict revised. No project lock changed. No governance file amended (beyond the narrow `current-project-state.md` update).**

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
                               (0.25% risk; 2× leverage; one position max;
                               mark-price stops where applicable)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                               (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility rule (preserved;
                               not invoked by Phase 4ad / Phase 4ae scope)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4p                    : G1 strategy spec (preserved)
Phase 4q                    : G1 backtest-plan methodology (preserved)
Phase 4v                    : C1 strategy spec (preserved)
Phase 4w                    : C1 backtest-plan methodology (preserved)
Phase 4z recommendations    : remain recommendations only;
                               NOT adopted as binding governance by 4ad
Phase 4aa admissibility framework : remain recommendation only;
                                    NOT adopted as binding governance by 4ad
Phase 4ab recommendations   : remain recommendations only;
                               NOT adopted as binding governance by 4ad
Phase 4ac results           : remain data / integrity evidence only,
                               EXCEPT that Phase 4ad explicitly defines
                               Phase 4ad future-use scope rules (Rule A /
                               Rule B / Rule C) for prospective analysis-time
                               use of Phase 4ac data only.
                               Phase 4ad rules do NOT modify Phase 4ac
                               manifests, do NOT flip eligibility flags,
                               and do NOT revise prior verdicts or locks.
```

## 14. Explicit Non-Authorization Statement

Phase 4ad does NOT authorize:

- **Phase 4ae** (any kind);
- **Phase 5;**
- **Phase 4 canonical;**
- **any other named successor phase;**
- **data acquisition;**
- **data download;**
- **API calls;**
- **endpoint calls;**
- **data modification;**
- **manifest creation;**
- **manifest modification;**
- **v003 or any other dataset version;**
- **backtests** (any kind);
- **diagnostics** (any kind);
- **Q1–Q7 rerun;**
- **substrate-feasibility execution;**
- **strategy specs;**
- **hypothesis specs;**
- **backtest plans;**
- **implementation** (no `src/prometheus/` modification);
- **old-strategy rescue** (R3 / R2 / F1 / D1-A / V2 / G1 / C1 on any symbol);
- **R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid;**
- **paper / shadow / live operation;**
- **live-readiness;**
- **deployment;**
- **production-key creation;**
- **authenticated APIs;**
- **private endpoints;**
- **public endpoint calls in code;**
- **user stream / WebSocket / listenKey lifecycle;**
- **exchange-write capability;**
- **MCP tooling;**
- **Graphify tooling;**
- **`.mcp.json` creation or modification;**
- **credentials;**
- **adoption of Phase 4z recommendations as binding governance;**
- **adoption of Phase 4aa admissibility framework as binding governance;**
- **adoption of Phase 4ab recommendations as binding governance;**
- **broadening of Phase 4ac results beyond data / integrity evidence** (Phase 4ad's Rule A / B / C are narrowly-scoped future-use rules for prospective analysis only; they do NOT broaden Phase 4ac results into binding cross-project governance);
- **modification of any specialist governance file** (`docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, or any specialist document) **except** the narrow `docs/00-meta/current-project-state.md` update required to record Phase 4ad;
- **successor phase.**

**Phase 4ad does NOT modify:**

- source code under `src/prometheus/`;
- tests;
- scripts (no modification of any existing acquisition / backtest / analysis script; no new script created);
- raw data;
- normalized data;
- any manifest;
- existing strategy specifications;
- governance files (except the narrow `current-project-state.md` update);
- project locks, retained verdicts, or any prior phase's substantive content.

**Phase 4ad output:**

- `docs/00-meta/implementation-reports/2026-05-04_phase-4ad_alt-symbol-gap-governance-scope-revision.md` (this memo);
- `docs/00-meta/implementation-reports/2026-05-04_phase-4ad_closeout.md` (closeout);
- narrow update to `docs/00-meta/current-project-state.md` recording Phase 4ad (no broad documentation refresh).

**Phase 4ad is preserved on its feature branch unless and until the operator separately instructs a merge.** main remains unchanged at `3478d05d97c43ee9ef885ae3defa4d1559189605` after Phase 4ad branch creation.

---

**Phase 4ad is text-only. No source code, tests, scripts, data, manifests, governance files, retained verdicts, or project locks were created or modified. Phase 4ad defines Phase 4ad-scope future-use rules (Rule A mark-price invalid-window exclusion; Rule B SOL/XRP early-2022 kline gap scope policy with B1 / B2 / B3; Rule C PASS-only subset) that apply prospectively to future Phase 4ae-equivalent substrate-feasibility analysis only. Phase 4ad does NOT modify Phase 4ac manifests, does NOT flip any `research_eligible` flag, does NOT revise any retained verdict, does NOT change any project lock, does NOT broaden Phase 4ac results into binding governance. Phase 4ad does NOT authorize Phase 4ae, data acquisition, manifest modification, backtest, diagnostic, Q1–Q7 rerun, substrate-feasibility execution, strategy spec, hypothesis spec, backtest-plan, implementation, paper / shadow / live operation, exchange-write, production keys, authenticated APIs, private endpoints, public endpoint calls in code, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, or any successor phase. C1 first-spec remains terminally HARD REJECTED. V2 / G1 first-specs remain terminally HARD REJECTED. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. R1a / R1b-narrow remain RETAINED — NON-LEADING. Phase 4z recommendations remain recommendations only. Phase 4aa admissibility framework remains recommendation only. Phase 4ab recommendations remain recommendations only. Phase 4ac results remain data / integrity evidence only (with Phase 4ad future-use scope rules applying prospectively to analysis-time use). Recommended state: remain paused (primary; Option B merge Phase 4ad then stop); Phase 4ae substrate-feasibility analysis memo (conditional next; not authorized by Phase 4ad). No next phase authorized.**
