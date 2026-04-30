# Phase 3p — 5m Diagnostics Data-Requirements and Execution-Plan Memo (docs-only)

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2p §C.1 (R3 baseline-of-record); Phase 2x family-review memo (V1 breakout family at useful ceiling under current framework); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved); Phase 2w §16.1 (R2 FAILED — §11.6 cost-sensitivity blocks); Phase 3d-B2 (F1 HARD REJECT); Phase 3e post-F1 research consolidation memo; Phase 3j (D1-A MECHANISM PASS / FRAMEWORK FAIL — other; Phase 3j terminal for D1-A under current locked spec); Phase 3k post-D1-A research consolidation memo (remain-paused primary recommendation); Phase 3l external execution-cost evidence review (primary assessment B — current cost model conservative but defensible; §11.6 unchanged pending stronger evidence); Phase 3m regime-first research framework memo (remain-paused primary recommendation); Phase 3n 5m timeframe feasibility / execution-timing memo (remain-paused primary recommendation; 5m framed as possible future execution / timing diagnostics layer only, not signal layer); Phase 3o 5m diagnostics-spec memo (remain-paused primary recommendation; predeclared diagnostic question set Q1–Q7 + forbidden question forms + diagnostic-term definitions + analysis boundary); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/historical-data-spec.md`; `docs/04-data/dataset-versioning.md`; `docs/04-data/timestamp-policy.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-mcp-and-secrets.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3p — Docs-only **5m diagnostics data-requirements and execution-plan memo.** Converts the Phase 3o predeclared question set Q1–Q7 into a concrete *future* diagnostics plan: defines exact 5m data requirements (without downloading data); specifies dataset-versioning approach (v003 vs supplemental); enumerates manifest / integrity evidence any future 5m dataset would require; specifies the future diagnostic outputs required to answer Q1–Q7; defines outcome-interpretation rules *before* data exists; ends with a decision menu. **No data acquired. No dataset created. No diagnostic computed. No backtest run. No code written. No implementation initiated. No successor authorized.**

**Branch:** `phase-3p/5m-diagnostics-data-requirements-and-execution-plan`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No 5m analysis. No 5m data downloaded. No v003 dataset created. No supplemental 5m dataset created. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No prior verdict revised.** R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained research evidence. R2 remains FAILED. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. §11.6 = 8 bps HIGH per side preserved. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal. **Phase 3p preserves the post-Phase-3o remain-paused recommendation.** Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3p is deciding

Phase 3p is a docs-only *planning* memo. It picks up where Phase 3o stopped: Phase 3o predeclared the *what* (Q1–Q7), the *what-not* (forbidden question forms), the *terms* (13 diagnostic definitions), and the *analysis boundary* (allowed vs forbidden). Phase 3p adds the next layer of specification — the *how-would-we-actually-run-this* layer — without running it.

Phase 3p answers four questions that Phase 3o deferred:

1. **Data requirements.** What 5m datasets, what symbols, what date ranges, what auxiliary tables, what raw-vs-derived structure would Q1–Q7 require?
2. **Dataset versioning.** Should 5m work be a v003 family bump or a supplemental v001-of-5m alongside v002? What manifest + integrity-check evidence would be required before any 5m dataset is treated as research-eligible?
3. **Diagnostic outputs.** What concrete tables, distributions, and per-question summary artifacts would a future diagnostics-execution phase need to produce in order to answer Q1–Q7?
4. **Outcome-interpretation rules.** What, *predeclared in advance*, would constitute "informative", "non-informative", or "ambiguous" outcomes for each predeclared question?

The deliverable is documentation only. Predeclaring the operational specifics *before any data exists* extends the Phase 3o discipline: question-set predeclaration prevents data dredging; data-requirements predeclaration prevents convenient ex-post boundary expansion; outcome-interpretation predeclaration prevents ex-post threshold revisionism in the diagnostic-classification step itself.

Phase 3p is **NOT**:

- Authorizing 5m data download.
- Authorizing v003 or supplemental 5m dataset creation.
- Authorizing 5m diagnostics-execution work.
- Authorizing 5m strategy signals or any 5m strategy family.
- Authorizing rerun of H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A or any controls.
- Authorizing reclassification or rescue of R2, F1, or D1-A.
- Authorizing parameter tuning, threshold revision, project-lock revision, or prior-verdict revision.
- Authorizing regime-first implementation, ML feasibility memo, formal cost-model revision, hybrid spec, or new strategy-family discovery.
- Authorizing paper/shadow planning, Phase 4 runtime / state / persistence work, live-readiness, deployment, production-key creation, or exchange-write capability.
- Enabling MCP, Graphify, `.mcp.json`, credentials, authenticated Binance APIs, or any data/ commits.

Phase 3p **IS**:

- A docs-only memo that documents (a) project-state restatement; (b) preservation of the post-Phase-3o remain-paused recommendation; (c) concrete *future* diagnostics plan converting Q1–Q7 into operational specification; (d) exact 5m data requirements (symbols, intervals, date ranges, auxiliary datasets, schema requirements, source endpoints, completeness expectations); (e) dataset-versioning approach (v003 vs supplemental v001-of-5m comparison + recommendation); (f) manifest + integrity-check evidence specification for any future 5m dataset; (g) per-question diagnostic outputs (tables / distributions / classifications); (h) per-question outcome-interpretation rules (informative / non-informative / ambiguous predeclared *before* data exists); (i) an explicit non-authorization statement; (j) a single recommended next operator decision.

The output is a consolidated 5m-diagnostics planning record + a single forward-looking operator decision recommendation. **Phase 3p produces a memo; the operator decides whether to authorize anything downstream.**

---

## 2. Current project-state restatement

| Item | State |
|------|-------|
| **R3** | V1 breakout baseline-of-record per Phase 2p §C.1; locked sub-parameters preserved. |
| **H0** | V1 breakout framework anchor per Phase 2i §1.7.3. |
| **R1a / R1b-narrow** | Retained research evidence only; non-leading. |
| **R2** | Retained research evidence only; **framework FAILED — §11.6 cost-sensitivity blocks**. |
| **F1** | Retained research evidence only; **HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal for F1. |
| **D1-A** | Retained research evidence only; **MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2; Phase 3j terminal for D1-A under current locked spec. |
| **Phase 3k consolidation** | Merged; primary recommendation: **remain paused**. |
| **Phase 3l external cost-evidence review** | Merged; primary assessment **B — current cost model conservative but defensible**; §11.6 = 8 bps HIGH per side preserved. |
| **Phase 3m regime-first framework memo** | Merged; primary recommendation: **remain paused**. |
| **Phase 3n 5m timeframe feasibility memo** | Merged; primary recommendation: **remain paused**; 5m framed as possible future execution / timing diagnostics layer only, not signal layer. |
| **Phase 3o 5m diagnostics-spec memo** | Merged; primary recommendation: **remain paused**; predeclared question set Q1–Q7 + forbidden question forms + diagnostic-term definitions + analysis boundary. |
| **§1.7.3 project-level locks** | Preserved verbatim. |
| **Phase 2f thresholds (incl. §11.6 = 8 bps HIGH per side)** | Preserved verbatim. |
| **v002 datasets** | Locked. 15m + 1h-derived + 15m mark-price + funding-event tables for BTCUSDT and ETHUSDT. **No 5m datasets exist; no v003 created.** |
| **Paper/shadow planning** | Not authorized. |
| **Phase 4 work** | Not authorized. |
| **Live-readiness / deployment / production-key / exchange-write work** | Not authorized. |
| **MCP / Graphify / `.mcp.json` / credentials** | Not activated; not requested; not used. |

Phase 3p preserves the post-Phase-3o remain-paused recommendation explicitly. This memo extends the Phase 3o predeclaration discipline to the operational specification layer; it does not weaken or revise any prior recommendation.

---

## 3. Concrete future diagnostics plan: Q1–Q7 operational structure

This section converts the Phase 3o predeclared question set into the operational structure a future diagnostics-execution phase would follow, *if such a phase were ever separately authorized*. The structure is plan-only: no computation, no data acquisition, no analysis is performed by Phase 3p.

### 3.1 Trade-source population

All Q1–Q7 outputs operate on the **v002-locked retained-evidence trade populations**:

- **R3** trades — V1 breakout baseline-of-record trade list per Phase 2p §C.1, locked to v002 datasets, BTCUSDT + ETHUSDT.
- **R2** trades — V1 breakout pullback-retest entry trade list per Phase 2w, locked to v002 datasets, BTCUSDT + ETHUSDT, both MED and HIGH slippage variants.
- **F1** trades — Mean-reversion-after-overextension trade list per Phase 3d-B2, locked to v002 datasets, BTCUSDT + ETHUSDT, both MED and HIGH slippage variants.
- **D1-A** trades — Funding-aware contrarian trade list per Phase 3j, locked to v002 datasets, BTCUSDT + ETHUSDT, both R-window and V-window where applicable.

The trade populations are **locked, immutable, and dataset-version-attributed to v002**. Any future 5m diagnostics phase must **not** regenerate, modify, or re-score these trade populations. The 5m diagnostic computation operates on *the existing trade list* by augmenting each trade with 5m-resolution path observations.

### 3.2 Per-trade augmentation structure

For each trade in the v002-locked populations, a future 5m diagnostics phase would compute the following per-trade 5m path attributes (terms predeclared in Phase 3o §7):

- IAE_N for N ∈ {1, 2, 3} 5m sub-bars after entry (Q1 input).
- IFE_N for N ∈ {1, 2, 3} 5m sub-bars after entry (Q1 input).
- First-5m-bar return (Q1 input).
- MAE / MFE over the trade's full holding period at 5m granularity (Q1, Q3 inputs).
- For STOP-exited trades: wick-stop / sustained-stop classification (Q2 input).
- For all trades: intrabar target touch presence and timing; confirmed target touch presence and timing; target-touch-then-stop event flag (Q3 inputs).
- For D1-A trades only: mean-cumulative-displacement at 5 / 10 / 15 / 30 / 60 min from funding-settlement event (Q4 input).
- For all trades: 15m next-open vs probability-weighted 5m fill simulation difference (Q5 input).
- For STOP-exited trades: mark-price stop-trigger 5m-sub-bar vs trade-price stop-trigger 5m-sub-bar timing difference (Q6 input).

### 3.3 Per-question aggregation structure

Each predeclared question Q1–Q7 maps to a fixed aggregation structure:

- **Q1 aggregation** — Distribution of IAE_1 / IAE_2 / IAE_3 by candidate, by symbol, by exit-type. Mean / median / 25th / 75th percentile reported. Cross-candidate comparison table.
- **Q2 aggregation** — Per-candidate, per-symbol counts of wick-stop events vs sustained-stop events. Fraction of STOP exits classified as wick-stop. Differential by sub-period (e.g. by year or by volatility regime, *only if* sub-period definitions are predeclared in the diagnostics-execution plan).
- **Q3 aggregation** — Per-candidate, per-symbol counts of target-touch-then-stop events; intrabar target touch frequency in STOP-exited trades; confirmed target touch frequency in STOP-exited trades. **Strict descriptive-only output**; no derived "improved exit rule" computation.
- **Q4 aggregation** — D1-A-only mean-cumulative-displacement curve at the 5 / 10 / 15 / 30 / 60-minute milestones, separately for BTC and ETH. Standard error bands. No optimization over the milestone set.
- **Q5 aggregation** — Per-candidate, per-symbol distribution of (15m next-open price − probability-weighted 5m fill simulation price) signed in trade-direction units. Mean / median reported. Compared to existing 8 bps HIGH per side cost assumption.
- **Q6 aggregation** — Per-candidate, per-symbol distribution of (mark-price stop-trigger 5m-bar − trade-price stop-trigger 5m-bar) timing difference for STOP-exited trades. Sign convention reported.
- **Q7 meta-aggregation** — Self-classification of Q1–Q6 using the predeclared replicability criteria from Phase 3o §5.7: each of Q1–Q6 receives one classification ∈ {informative, non-informative, ambiguous} based on predeclared per-question rules (§6 of this memo).

### 3.4 Output discipline

Per Phase 3o §12, the future diagnostics-execution phase output is **memo + tables**, not memo + tables + recommendations. Recommendations belong in subsequent operator-driven decisions, not in the diagnostic output itself.

---

## 4. Exact 5m data requirements (without downloading data)

This section defines the *exact* 5m data inventory any future diagnostics-execution phase would require. Phase 3p does **not** download, fetch, generate, or stage any of these datasets; this section is specification-only.

### 4.1 Required symbols

```text
BTCUSDT (perpetual, USDⓈ-M futures)
ETHUSDT (perpetual, USDⓈ-M futures)
```

These are the same two symbols covered by the existing v002 datasets. No additional symbols required.

### 4.2 Required intervals

```text
5m
```

Single new interval. The existing v002 15m + 1h-derived datasets are *not* augmented or replaced; they are *complemented* by the 5m datasets.

### 4.3 Required date range

The 5m date range must **fully cover** the v002 dataset date range. Specifically: the 5m dataset's first `open_time` must be ≤ the earliest `open_time` referenced by any v002-locked trade; the 5m dataset's last `open_time` must be ≥ the latest `open_time` referenced by any v002-locked trade.

This is a *strict superset coverage* requirement. Partial coverage (5m data covering only some sub-period of v002 trades) is unacceptable because it would systematically exclude some trades from diagnostic analysis, which is a form of selection bias prohibited by the Phase 3o §13.4 stop conditions.

### 4.4 Required dataset families

Q1–Q7 require the following 5m dataset families:

| # | Dataset family | Used by | Notes |
|---|----------------|---------|-------|
| 1 | `binance_usdm_btcusdt_5m` (klines) | Q1, Q2, Q3, Q5, Q6 | Trade-price OHLCV. |
| 2 | `binance_usdm_ethusdt_5m` (klines) | Q1, Q2, Q3, Q5, Q6 | Trade-price OHLCV. |
| 3 | `binance_usdm_btcusdt_markprice_5m` | Q6 | Mark-price OHLCV. Required only for Q6. |
| 4 | `binance_usdm_ethusdt_markprice_5m` | Q6 | Mark-price OHLCV. Required only for Q6. |

The existing v002 funding-event tables (`binance_usdm_btcusdt_funding__v002`, `binance_usdm_ethusdt_funding__v002`) are *re-used unchanged* for Q4 — funding-event timestamps already exist in v002 and do not require a 5m equivalent.

The existing v002 1h-derived tables are *not* required for any Q1–Q7 question and need not be re-derived from 5m data.

### 4.5 Required schema (per kline dataset)

Each 5m kline dataset must include at minimum:

- `symbol` (string).
- `interval` (string, fixed value `"5m"`).
- `open_time` (UTC Unix milliseconds, integer; must satisfy `open_time mod 300000 = 0`).
- `close_time` (UTC Unix milliseconds, integer; must equal `open_time + 5 × 60 × 1000 − 1`).
- `open` (decimal).
- `high` (decimal).
- `low` (decimal).
- `close` (decimal).
- `volume` (decimal; trade-price datasets only — mark-price datasets may omit or set to zero).
- `quote_volume` (decimal; trade-price datasets only).
- `trade_count` (integer; trade-price datasets only).
- `taker_buy_volume` (decimal; trade-price datasets only).
- `taker_buy_quote_volume` (decimal; trade-price datasets only).

Schema must conform to the same canonical conventions as the v002 15m kline datasets (`binance_usdm_btcusdt_15m__v002` and equivalents) wherever those conventions are defined.

### 4.6 Required source endpoints

```text
GET /fapi/v1/klines             (trade-price 5m klines, public, no authentication)
GET /fapi/v1/markPriceKlines    (mark-price 5m klines, public, no authentication)
GET /fapi/v1/fundingRate        (already in v002; not re-fetched)
```

All three endpoints are **public**. None requires authenticated access. None requires production trade-capable Binance API keys. **Phase 3p reaffirms that no credentials are requested or required.**

### 4.7 Required quality / completeness checks

Any future 5m dataset must pass the following integrity checks before it is research-eligible:

- **No gaps.** No 5m bar may be missing within the date range. Forward-fill, interpolation, or silent omission is forbidden (per `docs/04-data/data-requirements.md` forbidden patterns).
- **Monotone timestamps.** `open_time` strictly increases per (`symbol`, `interval`).
- **Boundary alignment.** Every `open_time` satisfies `open_time mod 300000 = 0`.
- **Close-time consistency.** Every `close_time = open_time + 299999`.
- **OHLC sanity.** `low ≤ open ≤ high`, `low ≤ close ≤ high`, `low > 0`, `high > 0`, `open > 0`, `close > 0`.
- **Volume sanity (trade-price datasets only).** `volume ≥ 0`, `quote_volume ≥ 0`, `trade_count ≥ 0`.
- **Symbol consistency.** All rows for a given dataset have the expected symbol.
- **Interval consistency.** All rows have `interval = "5m"`.
- **Date range coverage.** First and last `open_time` cover the v002-required date range superset (§4.3).

### 4.8 Why these requirements are exact

Each requirement above is downstream of a specific Q1–Q7 question or of a documented timestamp / dataset-versioning rule. Vague or "best-effort" requirements would create systematic bias: e.g., allowing forward-fill of missing 5m bars would silently bias IAE / IFE / wick-stop / sustained-stop classifications; allowing partial coverage would silently exclude entire sub-periods of trades. Phase 3p specifies the requirements *strictly* so any future diagnostics-execution phase has no slack to exploit.

---

## 5. Dataset-versioning approach

Phase 3p does *not* create any dataset, manifest, or version. This section defines the versioning *approach* a future 5m dataset family would follow.

### 5.1 Two valid options

Per `docs/04-data/dataset-versioning.md`, adding a new interval set is a mandatory version bump for the affected dataset family. Two valid versioning options are available:

**Option A — Coordinated v003 family bump.**

- All eight existing v002-versioned datasets bump to v003.
- New 5m datasets are added at v003: `binance_usdm_btcusdt_5m__v003`, `binance_usdm_ethusdt_5m__v003`, `binance_usdm_btcusdt_markprice_5m__v003`, `binance_usdm_ethusdt_markprice_5m__v003`.
- Existing 15m / 1h-derived / 15m mark-price / funding datasets become v003 versions of themselves.
- v002 manifests remain immutable (per `dataset-versioning.md` immutability policy); v003 manifests link back to v002 as predecessor.
- v002 trade populations remain dataset-version-attributed to v002; v003 datasets are used only for the new 5m augmentation.

**Option B — Supplemental v001-of-5m alongside v002.**

- Existing v002 datasets remain v002 with no version bump.
- New 5m datasets are added under their own version ID: `binance_usdm_btcusdt_5m__v001`, `binance_usdm_ethusdt_5m__v001`, `binance_usdm_btcusdt_markprice_5m__v001`, `binance_usdm_ethusdt_markprice_5m__v001`.
- Each 5m dataset's manifest declares predecessor relationships (where applicable) to v002 datasets.
- v002 trade populations remain unchanged and dataset-version-attributed to v002.

### 5.2 Comparison

| Dimension | Option A (v003 bump) | Option B (supplemental v001-of-5m) |
|-----------|----------------------|-------------------------------------|
| Scope of change | Eight datasets bump version | Four new datasets only |
| Risk of contaminating v002 verdicts | Lower (semantically clean separation) | Lower (v002 unchanged literally) |
| Compatibility with `dataset-versioning.md` | Clean (each family bumps to v003) | Clean (each family has its first version) |
| Maintenance overhead | Higher (v002 → v003 manifest re-issue for unchanged datasets) | Lower (only new datasets get manifests) |
| Audit clarity | Clear ("v003 includes 5m") | Clear ("5m is supplemental") |
| Risk of confusion in future analyses | Low (all datasets at v003) | Low (versioning is explicit per family) |
| Alignment with current project state | Requires re-issuing manifests for unchanged data | No effect on existing datasets |

### 5.3 Recommendation

**Option B (supplemental v001-of-5m alongside v002)** is preferred *if and when* any future 5m diagnostics-execution phase is ever authorized.

Reasoning:
- Option B preserves v002 *literally*. v002 manifests remain at the exact byte-content they have today, with no need to re-issue identical-content manifests at a new version number. This is the strongest possible preservation of v002 verdict provenance.
- Option B is lower-overhead. Only the four new 5m dataset families require manifests; the eight existing v002 datasets are untouched.
- Option B is unambiguous. "5m is supplemental data introduced after v002 was locked" is a clean audit story that matches the actual research history.
- Option A (v003 bump) is also acceptable but adds maintenance overhead with no offsetting benefit, since the v002 verdicts are already permanently dataset-version-attributed and would not be revised.

This recommendation is *advisory only* and applies *only if* the operator separately authorizes a future 5m data acquisition phase. Phase 3p does not authorize that phase. The actual versioning choice is finalized by the operator at the time of any such future authorization.

### 5.4 Phase 3p does not create any dataset, manifest, or version

Reaffirmation: Phase 3p does not create v003; does not create supplemental v001-of-5m; does not generate or stage any new manifest; does not edit existing v002 manifests. The v002 manifest set is untouched.

---

## 6. Manifest and integrity-check evidence specification

This section defines the evidence any future 5m dataset would need to produce *before* it is treated as research-eligible. Phase 3p does *not* produce any of this evidence; this section is specification-only.

### 6.1 Required manifest content (per 5m dataset)

Each 5m dataset manifest must include at minimum:

- `name` — dataset family name (e.g., `binance_usdm_btcusdt_5m`).
- `version` — dataset version ID (e.g., `v001` under Option B; `v003` under Option A).
- `category` — one of `normalized`, `derived`, `metadata`, `validation_view`.
- `created_at_utc_ms` — generation timestamp.
- `canonical_timezone` — `UTC`.
- `canonical_timestamp_format` — `unix_milliseconds`.
- `symbol_set` — single-element list (e.g., `["BTCUSDT"]`).
- `interval_set` — `["5m"]`.
- `source_endpoints` — list of source endpoint identifiers (e.g., `["GET /fapi/v1/klines"]`).
- `schema_version` — schema version identifier.
- `pipeline_version` — code/pipeline version that generated the dataset.
- `partitioning` — partition layout description.
- `primary_key` — `["symbol", "interval", "open_time"]`.
- `predecessor_dataset_versions` — list of v002 datasets used as predecessors (where applicable; e.g., trade-price 5m has no predecessor; mark-price 5m's predecessor relationship is to mark-price 15m if useful).
- `notes` — free-text notes; must record that the dataset was generated for Phase 3o-predeclared Q1–Q7 diagnostics work.
- `quality_checks` — embedded results of the integrity checks listed below (§6.2).
- `date_range_start_open_time_utc_ms` — first `open_time`.
- `date_range_end_open_time_utc_ms` — last `open_time`.
- `bar_count` — count of bars in the dataset.

### 6.2 Required integrity-check evidence

The manifest's `quality_checks` field must record the result of each check defined in §4.7. Each check must be reported as `PASS` or `FAIL` with associated counts where appropriate. A `FAIL` on any check means the dataset is **not** research-eligible and the diagnostics-execution phase must stop (per Phase 3o §13).

Required check results:

- `gaps_detected` — count of missing bars detected. Required: `0`.
- `gap_locations` — list of gap windows if any. Required: empty list `[]`.
- `monotone_timestamps` — boolean. Required: `true`.
- `boundary_alignment_violations` — count of bars failing `open_time mod 300000 = 0`. Required: `0`.
- `close_time_consistency_violations` — count of bars failing `close_time = open_time + 299999`. Required: `0`.
- `ohlc_sanity_violations` — count of bars failing OHLC sanity. Required: `0`.
- `volume_sanity_violations` — count of bars failing volume sanity (trade-price only). Required: `0`.
- `symbol_consistency_violations` — count of mismatched symbol rows. Required: `0`.
- `interval_consistency_violations` — count of rows with `interval ≠ "5m"`. Required: `0`.
- `date_range_coverage` — boolean. Required: `true` (5m date range is a strict superset of v002-locked-trade date range).

### 6.3 Required experiment linkage

Per `docs/04-data/dataset-versioning.md` Experiment Linkage Policy, any future diagnostics report must record:

- the 5m dataset versions used (`binance_usdm_btcusdt_5m__v001`, etc.);
- the v002 trade-source dataset versions used (BTCUSDT 15m v002, ETHUSDT 15m v002, BTCUSDT funding v002, etc.);
- the 5m schema version;
- the 5m pipeline version;
- the diagnostic-pipeline code reference;
- the generation timestamp of the diagnostic experiment.

### 6.4 Phase 3p does not produce any manifest or integrity evidence

Reaffirmation. Phase 3p does not generate any 5m manifest. Phase 3p does not run any integrity check. Phase 3p does not produce any quality-check evidence. The above is specification-only.

---

## 7. Future diagnostic outputs needed to answer Q1–Q7

This section specifies the *concrete tables, distributions, and per-question summary artifacts* a future diagnostics-execution phase would produce. Phase 3p does *not* produce any of these artifacts.

### 7.1 Q1 outputs — Immediate adverse excursion

**Required artifacts:**

- Q1-Table-A: Per-trade IAE_1 / IAE_2 / IAE_3 augmentation column added to each retained-evidence trade record (R3, R2, F1, D1-A; BTC + ETH).
- Q1-Table-B: Distribution summary by candidate × symbol × exit-type. Mean / median / 25th / 75th / 90th percentile.
- Q1-Table-C: Cross-candidate comparison table. Each cell: mean IAE_1 in trade-direction-signed R units.
- Q1-Plot-A (optional): IAE_1 distribution histogram per candidate, faceted by symbol. Plots are advisory; tables are authoritative.

**Required derived statistics:**

- Mean and median IAE_1 per candidate × symbol.
- Fraction of trades with IAE_1 > 0.5 R (unfavorable threshold for "immediate adverse" — predeclared but advisory; alternative thresholds may be reported but the predeclared value is canonical).

### 7.2 Q2 outputs — Wick-stop vs sustained-stop

**Required artifacts:**

- Q2-Table-A: Per-STOP-exited-trade classification (`wick_stop` | `sustained_stop`) augmentation column.
- Q2-Table-B: Per-candidate × per-symbol counts and fractions of wick-stop vs sustained-stop events.
- Q2-Table-C: Cross-candidate comparison of wick-stop fraction.

**Required derived statistics:**

- Wick-stop fraction = `count(wick_stop) / (count(wick_stop) + count(sustained_stop))` per candidate × symbol.
- Differential = `wick_stop_fraction_HIGH_slip − wick_stop_fraction_MED_slip` (where applicable).

### 7.3 Q3 outputs — Intrabar target touches in adverse-exit trades

**Required artifacts:**

- Q3-Table-A: Per-trade flags `intrabar_target_touch_present`, `confirmed_target_touch_present`, `target_touch_then_stop` augmentation columns.
- Q3-Table-B: Per-candidate × per-symbol counts of target-touch-then-stop events; intrabar target touch frequency in STOP-exited trades; confirmed target touch frequency in STOP-exited trades.

**Required output discipline:**

- **No "improved exit rule" computation.** Per Phase 3o §6.3, "Which intrabar target touch rule maximizes R?" is a forbidden question form.
- **No parameter search over target levels.** The +1R and +2R thresholds are fixed at predeclaration time.
- **No retroactive derivation of an intrabar exit policy.**

### 7.4 Q4 outputs — D1-A funding-extreme decay curve

**Required artifacts (D1-A only):**

- Q4-Table-A: Per-funding-event mean cumulative price displacement at 5 / 10 / 15 / 30 / 60 minutes after funding-settlement, signed in trade-direction R units.
- Q4-Table-B: Aggregated decay curve per symbol (BTC + ETH separately). Each row: milestone-minute → mean cumulative displacement (with standard error band).
- Q4-Plot-A (optional): Decay curve plot per symbol. Plots advisory; tables authoritative.

**Required output discipline:**

- **No optimization over the milestone set.** The {5, 10, 15, 30, 60} minute set is fixed at predeclaration time.
- **No derivation of a "better" D1-A holding period from the curve.** This would be a forbidden post-hoc parameter revision.

### 7.5 Q5 outputs — Next-15m-open fill realism

**Required artifacts:**

- Q5-Table-A: Per-trade `fill_assumption_slippage_proxy` augmentation column (defined in Phase 3o §7.12).
- Q5-Table-B: Per-candidate × per-symbol distribution. Mean / median in basis points.
- Q5-Table-C: Cross-candidate comparison vs the existing 8 bps HIGH per side cost assumption.

**Required output discipline:**

- **No revision of §11.6.** Q5 produces *one piece* of fill-realism evidence, not a §11.6 revision input. §11.6 = 8 bps HIGH per side remains preserved.
- **No definition of probability weights derived from path observations.** The 5m fill simulation probability weights must be predeclared in the diagnostics-execution plan (Phase 3o Option C deliverable, *not* part of Phase 3p) before any analysis. Phase 3p does not predeclare the weights; it predeclares only the existence of the requirement.

### 7.6 Q6 outputs — Mark/trade stop divergence

**Required artifacts:**

- Q6-Table-A: Per-STOP-exited-trade `mark_trade_stop_divergence` augmentation column (timing difference in 5m sub-bars; signed).
- Q6-Table-B: Per-candidate × per-symbol distribution of timing differences.

**Required output discipline:**

- **No revision of mark-price stop policy.** §1.7.3 project-level lock on mark-price stops is preserved verbatim.
- **No derivation of a "better" stop policy from the divergence findings.**

### 7.7 Q7 outputs — Meta-classification

**Required artifacts:**

- Q7-Table-A: Single classification per Q1–Q6: one of `informative`, `non-informative`, `ambiguous` (defined per §8 of this memo). Q7's row classifies Q7 itself: `meta`.
- Q7-Memo: Single paragraph per question explaining the classification with reference to the predeclared interpretation rules (§8 below).

**Required output discipline:**

- **No "rescue" framing.** Per Phase 3o §12.5, the words "rescue / resurrect / revive / salvage" must not appear in any output.
- **No threshold revision.** Per Phase 3o §10.4, no §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / catastrophic-floor threshold may be revised.
- **No prior-verdict revision.** Per Phase 3o §10.6, no R3 / R2 / F1 / D1-A verdict may be revised.

---

## 8. Outcome-interpretation rules (predeclared *before* data exists)

This section is the *single most procedurally important* aspect of Phase 3p. By predeclaring outcome-interpretation rules *before any 5m data exists in the repository*, Phase 3p extends Phase 3o's predeclaration discipline to the diagnostic-classification step itself. Without this predeclaration, the future analyst (Claude Code, ChatGPT, or operator) could be tempted to ex-post tighten or loosen the criteria for "informative" to fit observed findings.

### 8.1 Q1 interpretation rules

**Informative classification requires:**

- Replicability across BTC and ETH: mean IAE_1 patterns are directionally consistent (within ±0.10 R) for at least three of the four retained-evidence candidates on both symbols.
- Replicability across at least two non-overlapping date sub-ranges within v002 (e.g., a "first half" and "second half" of the v002 date range).
- Consistency with mechanism reasoning: any uniformly hostile pattern *or* any candidate-specific pattern must admit a coherent ex-ante mechanism explanation.

**Non-informative classification:**

- Symmetric distributions of IAE_1 and IFE_1 with no candidate-level differentiation, *or*
- High variance with no replicability across symbols or sub-periods, *or*
- Patterns dependent on a small number (< 5%) of outlier trades.

**Ambiguous classification:**

- Partial replicability (e.g., BTC only or ETH only) *or* sub-period instability *or* mechanism-reasoning ambiguity. An ambiguous result must be reported honestly and must not be re-interpreted toward "informative" without separately authorized formal reclassification.

### 8.2 Q2 interpretation rules

**Informative classification requires:**

- A meaningful skew in wick-stop fraction in any candidate (predeclared threshold: wick-stop fraction ≥ 60% or ≤ 40% in at least one candidate × symbol cell).
- Replicability across BTC and ETH at the candidate level for any flagged candidate.
- Differential by sub-period or slippage-cell is reported if predeclared in the diagnostics-execution plan.

**Non-informative classification:**

- Wick-stop fractions in the 40–60% range across all candidate × symbol cells with no clear differentiation.

**Ambiguous classification:**

- Skew in one symbol but not the other; sub-period instability; or skew below the threshold in some cells and above in others without a coherent pattern.

### 8.3 Q3 interpretation rules

**Informative classification requires:**

- A meaningful frequency of target-touch-then-stop events: predeclared threshold ≥ 25% of STOP-exited trades touched +1R intrabar in at least one candidate × symbol cell.
- Replicability across BTC and ETH.
- Note: even an "informative" Q3 result *cannot* license any retained-evidence candidate revision, per Phase 3o §6.3 / §10.5 / §10.6.

**Non-informative classification:**

- Frequency < 25% across all candidate × symbol cells; uniformly distributed across exit-types (i.e., no concentration in STOP-exited population).

**Ambiguous classification:**

- Frequency near the threshold; sub-period instability; or strong differentiation in one symbol and not the other.

**Critical reminder:** Q3's "informative" outcome is *purely descriptive*. It does not authorize any policy change or rule revision. The procedural separation between Q3 informativeness and any candidate revision is the single most important rule in Phase 3p.

### 8.4 Q4 interpretation rules

**Informative classification requires:**

- A coherent decay shape: monotone (or near-monotone) cumulative-displacement curve over the {5, 10, 15, 30, 60}-minute milestones for at least one symbol.
- Replicability across BTC and ETH at the *qualitative shape* level (e.g., both symbols show fast-decay or both show slow-decay; if BTC fast-decay and ETH slow-decay, that is an *ambiguous* finding rather than strong informative).
- Standard-error bands tighter than the predeclared "noise floor" (the bands at the 60-minute milestone must be tighter than the 5-minute-milestone displacement magnitude in at least one symbol, indicating the decay is statistically distinguishable from noise).

**Non-informative classification:**

- Curve has high variance with no coherent decay shape; standard-error bands wider than the displacement magnitude at all milestones.

**Ambiguous classification:**

- BTC and ETH disagree on decay shape; sub-period instability; or shape inconsistent with mechanism reasoning.

**Critical reminder:** Q4's "informative" outcome (especially fast-decay) *informs* possible operator decisions about whether to authorize a D1-A successor (D1-A-prime / D1-B / hybrid) but **does not authorize any successor**. The operator decision and the successor authorization are separate phases not contemplated by Phase 3p.

### 8.5 Q5 interpretation rules

**Informative classification requires:**

- A systematic skew in fill-assumption slippage proxy *larger than the existing 8 bps HIGH per side cost assumption* (i.e., predeclared threshold: |mean signed slippage| > 8 bps in at least one candidate × symbol cell).
- Replicability across BTC and ETH at the directional level.
- Replicability across at least two non-overlapping date sub-ranges within v002.

**Non-informative classification:**

- Skew within ±8 bps with high variance; no candidate-level differentiation; or no replicability across symbols.

**Ambiguous classification:**

- Skew exceeds 8 bps in one symbol/sub-range but not in others; or skew is borderline at the threshold.

**Critical reminder:** Q5's "informative" outcome *informs* possible operator decisions about whether to authorize a formal cost-model revision phase but **does not revise §11.6**. §11.6 = 8 bps HIGH per side remains preserved.

### 8.6 Q6 interpretation rules

**Informative classification requires:**

- A systematic timing difference (mean |timing difference| > 1 5m sub-bar) in at least one candidate × symbol cell.
- Replicability across BTC and ETH at the candidate level for any flagged candidate.

**Non-informative classification:**

- Mean |timing difference| ≤ 1 5m sub-bar across all candidate × symbol cells; or high variance with no candidate-level differentiation.

**Ambiguous classification:**

- Timing difference in one symbol but not the other; sub-period instability.

**Critical reminder:** Q6's "informative" outcome *informs* operator understanding of mark-price stop-trigger mechanism but **does not revise mark-price stop policy**. §1.7.3 project-level lock on mark-price stops is preserved verbatim.

### 8.7 Q7 interpretation rules

Q7 is meta. Q7's classification is derived from Q1–Q6 classifications under the following rules:

- Q7 = `informative` only if **at least three** of Q1–Q6 are `informative` (i.e., the diagnostics phase produced a coherent body of informative findings, not just isolated signals).
- Q7 = `non-informative` if **all** of Q1–Q6 are `non-informative` *or* if at most one of Q1–Q6 is `informative` (i.e., the diagnostics phase produced predominantly non-informative findings).
- Q7 = `ambiguous` otherwise.

A `non-informative` Q7 outcome is a **valid result** and must be reported honestly. A `non-informative` Q7 outcome *strengthens* the existing remain-paused recommendation rather than weakening it. A future operator decision following a `non-informative` Q7 should default to remain-paused.

### 8.8 Predeclaration discipline

The above rules are predeclared *before any 5m data exists in the repository*. They are immutable from the Phase 3p commit forward. Any future diagnostics-execution phase must apply these exact rules. Silent rule revision or threshold tightening / loosening between Phase 3p and the future analysis is prohibited and would constitute a procedural failure mode comparable to data dredging.

---

## 9. Explicit non-authorization

Phase 3p does **not** authorize, propose, or initiate any of the following:

- **5m data acquisition.** No HTTP request, no REST call, no WebSocket subscription, no archive import, no third-party dataset import, no data refresh, no manifest regeneration. No 5m data exists in the repository at the conclusion of Phase 3p, just as it did not at the start.
- **5m dataset creation.** No v003 family bump, no supplemental v001-of-5m dataset family, no derived 5m table, no new manifest.
- **5m diagnostics execution.** No diagnostic computation. No table generated. No plot rendered. No predeclared question answered. The Phase 3p output is a written specification of *future* operations; no operations are performed.
- **Strategy changes.** R3 / R2 / F1 / D1-A specs preserved verbatim. No new strategy family. No 5m strategy variant. No hybrid spec.
- **Parameter changes.** Locked sub-parameters (R3 Fixed-R + 8-bar time-stop; F1 cumulative-displacement threshold + SMA(8) target + structural stop + 8-bar time-stop + same-direction cooldown; D1-A |Z_F| ≥ 2.0 + 1.0 × ATR(20) stop + +2.0 R target + 32-bar time-stop + per-funding-event cooldown + band [0.60, 1.80] × ATR + contrarian + no regime filter) all preserved verbatim.
- **Threshold optimization.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 preserved verbatim. No threshold sweep, no parameter search, no boundary revision.
- **Backtests.** No backtest run. No control rerun. No fold scoring, no walk-forward analysis, no cost-sensitivity sweep, no mechanism-check rerun, no aggregate-metric computation.
- **Implementation.** No source code, no runtime code, no data-ingestion code, no analysis code, no strategy code, no execution code, no risk code, no persistence code, no exchange-adapter code, no dashboard code, no observability code, no test code, no script.
- **Paper/shadow planning.** Not authorized.
- **Phase 4 work.** No runtime / state / persistence / risk-runtime work.
- **Live-readiness work.** No live-readiness gates evaluated, planned, or initiated.
- **Deployment work.** No deployment work initiated.
- **Production-key creation.** No production Binance trade-capable API keys requested, generated, stored, or referenced.
- **Exchange-write capability.** No exchange-write paths exist or were touched.
- **MCP enablement.** No MCP servers added, configured, or used. Project rules `.claude/rules/prometheus-mcp-and-secrets.md` preserved.
- **Graphify enablement.** Not installed. Not used.
- **`.mcp.json`.** Not created. Not edited. Does not exist in the repository.
- **Credentials.** None requested. None used. None stored. None referenced.
- **`data/` commits.** No `data/` artifact was staged, edited, or committed. v002 manifests untouched.

The output of Phase 3p is this single Markdown memo. Nothing else.

---

## 10. Decision menu for the operator

The operator now has a docs-only data-requirements and execution-plan memo that fully specifies the *future* operational structure of any 5m diagnostics-execution phase. The next operator decision is operator-driven only. The following paths are *possible*; Phase 3p recommends exactly one.

### 10.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. The strategy-execution pause continues. Phase 3p joins Phase 3k / 3l / 3m / 3n / 3o as docs-only research-consolidation evidence. No 5m data acquired. No v003 created. No supplemental 5m dataset created. No diagnostics executed.

**Reasoning:**

- Phase 3p has now realized its full *operational-specification* value: data requirements, dataset-versioning approach, manifest + integrity-check evidence specification, per-question diagnostic outputs, and outcome-interpretation rules are all written down, immutable, and auditable on `main`. That value is realized whether or not any successor phase is authorized.
- Combined with Phase 3o's predeclared question set + forbidden question forms + diagnostic-term definitions + analysis boundary, the project now has a *complete specification* of any future 5m diagnostics-execution phase — produced before any 5m data exists, audited and immutable in the repository.
- The case for *running* the predeclared diagnostics is non-zero but provisional. The strongest single case (Q4 D1-A funding-decay curve) has high information value, but D1-A is already terminal under current spec; even an informative Q4 result could only inform a possible future operator decision, not authorize one.
- The case for *acquiring* 5m data is downstream of the case for running the diagnostics. Acquiring data without a clear authorization to run the diagnostics is procedurally premature.
- The cumulative pattern across Phase 3k / 3l / 3m / 3n / 3o has been "remain paused" five times. Phase 3p's *operational specification* value is realized now; the *running* of the specification is a separate decision the operator should make deliberately, not by inertia.
- The forbidden-question discipline (Phase 3o §6) and the analysis-boundary discipline (Phase 3o §10) and the outcome-interpretation discipline (Phase 3p §8) are the most procedurally important outputs of the entire 5m research thread. They are realized now and persist indefinitely whether or not data is ever acquired.

**What this preserves:** R3 baseline-of-record; H0 anchor; all retained-evidence verdicts; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; v002 dataset version; no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write commitment.

**What this rules out:** No 5m data acquired. No v003 / supplemental 5m dataset created. No diagnostics executed. No prior verdict revised. No successor authorized.

### 10.2 Option B — 5m data acquisition phase, docs-and-data (CONDITIONAL secondary alternative)

**Description:** Authorize a future docs-and-data phase to acquire the 5m datasets specified in §4 of this memo, generate manifests per §6 specifications, run integrity checks, and commit the resulting 5m datasets and manifests to the repository. **Still no diagnostics executed; data acquisition only.**

**Reasoning if selected:** Data acquisition is the next concrete step in the 5m research thread, downstream of Phase 3p's operational specification. Acquiring the data without running the diagnostics is procedurally clean: the data either passes the integrity checks (and is research-eligible) or fails them (and the operator decides whether to escalate to the data source). Either outcome is informative and bounded.

**Pre-conditions if selected:**

- Operator commits ex-ante that the data acquisition phase cannot run diagnostics or produce any diagnostic table or finding.
- Operator commits ex-ante that any data-acquisition phase failure (integrity-check failure, source-endpoint failure, coverage failure) must produce a written failure report and not be silently retried with relaxed criteria.
- Operator commits ex-ante that the chosen versioning approach (Option A v003 bump or Option B supplemental v001-of-5m) is documented in the data-acquisition phase brief at authorization time.

**Risks if selected:**

- Data acquisition requires HTTP requests to public Binance endpoints. While these endpoints do not require credentials, they do require network access from the project environment. The data-acquisition phase brief must specify how this is handled (rate limits, retries, timeouts) without escalating MCP or credential surface.
- Data acquisition produces `data/` commits. The data-acquisition phase brief must clarify whether 5m raw payloads are committed to the repository or stored separately (e.g., Parquet under `data/raw/` is appropriate per `data/raw/binance_usdm/` convention; git-lfs may be a consideration for large files).
- Procedural escalation. Six docs-only memos already exist (3k / 3l / 3m / 3n / 3o / 3p); a seventh phase that *acquires data* is a discrete escalation that should be done only if the operator is committed to seeing the diagnostics through.

### 10.3 Option C — 5m diagnostics-execution phase, docs-only (CONDITIONAL tertiary alternative)

**Description:** Authorize a future *docs-only* phase that *runs* the predeclared Q1–Q7 diagnostics on a separately-acquired 5m dataset. Output: diagnostic tables + classifications + meta-classification per Phase 3p §7 + §8.

**Reasoning if selected:** This is the operational endpoint of the 5m research thread. It produces the actual answers to Q1–Q7 under the predeclared rules.

**Pre-conditions if selected:**

- Option B (data acquisition) must already have completed, with a 5m dataset that has passed all §4.7 / §6.2 integrity checks, with manifests linking to v002 trade-source datasets.
- Operator commits ex-ante that the diagnostics-execution phase will produce only the artifacts specified in §7, with no parameter recommendations, no rescue framings, no prior-verdict revisions.
- Operator commits ex-ante that the outcome-interpretation rules specified in §8 are immutable from the Phase 3p commit forward and cannot be ex-post modified by the diagnostics-execution phase.

**Risks if selected:**

- Procedural escalation as with Option B, plus the additional commitment to actually face the diagnostic outputs and follow through on the predeclared interpretation rules.
- A `non-informative` Q7 outcome (which is a valid result per §8.7) is the most likely outcome statistically and should not be re-interpreted as a partial or ambiguous outcome.
- Even an `informative` Q4 result for D1-A only authorizes the operator to *consider* whether to authorize a separate D1-A successor proposal phase; it does not itself authorize any successor.

### 10.4 Option D — Combined data acquisition + diagnostics phase (CONDITIONAL alternative)

**Description:** Authorize a single future phase that combines Option B (data acquisition) and Option C (diagnostics execution) into one operator-authorized step.

**Phase 3p's view:** Combined phases are procedurally less clean than separate phases. Splitting Option B and Option C into two separately authorized phases preserves the operator's option to halt after data acquisition (e.g., if integrity checks fail, or if the operator's strategic priorities change between data acquisition and diagnostics execution). Option D is acceptable but not preferred.

### 10.5 Option E — Regime-first formal spec memo, docs-only (LATERAL alternative)

**Description:** Authorize the docs-only formal regime-first spec memo that Phase 3m discussed but did not start.

**Phase 3p's view:** Independent of the 5m thread. Some operators may decide regime-first is a more promising direction. Phase 3p does not endorse or oppose this option relative to Option A; it is mentioned for completeness.

### 10.6 Option F — ML feasibility memo, docs-only (CONDITIONAL alternative)

**Description:** Authorize a docs-only memo evaluating whether ML feasibility work is appropriate.

**Phase 3p's view:** Independent of the 5m thread. ML feasibility is a separate and significantly more complex question. Phase 3p does not endorse this option as a near-term direction; it is mentioned for completeness.

### 10.7 Option G — New strategy-family discovery (NOT RECOMMENDED)

**Phase 3p's view:** Three strategy-research arcs have framework-failed under unchanged discipline. Starting a fourth without addressing *why* the first three failed is procedurally premature. Not recommended.

### 10.8 Option H — Paper/shadow planning, Phase 4, live-readiness, deployment, or strategy rescue (NOT RECOMMENDED)

**Phase 3p's view:** None of these are appropriate from the current state. Strongly not recommended.

### 10.9 Recommendation

**Phase 3p recommends Option A (remain paused) as primary.**

The complete specification of the 5m diagnostics thread is now realized in the repository: Phase 3o predeclared the *what* and *what-not*; Phase 3p predeclared the *how-would-we-actually-run-this* and the *how-would-we-classify-outcomes*. The specification's procedural value is fully captured; whether to *act on* the specification is a separate operator-strategic decision that Phase 3p does not currently identify a strong motivation for.

If the operator selects Option B (data acquisition) or Option C (diagnostics execution), each is conditional on the explicit ex-ante operator commitments listed above. Selecting B or C does not authorize anything beyond the named phase.

Options D, E, F, G, and H are not recommended by Phase 3p.

Phase 3p explicitly does **NOT** recommend:

- Implementation of any kind.
- Backtesting of any kind.
- 5m data acquisition (without separate operator authorization meeting Option B pre-conditions).
- v003 / supplemental 5m dataset creation (without separate operator authorization).
- 5m diagnostics execution (without separate operator authorization meeting Option C pre-conditions).
- 5m strategy.
- Paper/shadow planning.
- Phase 4 runtime work.
- Live-readiness work.
- Deployment work.
- Strategy rescue (R2 / F1 / D1-A successor / D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid / target-subset rescue / regime-conditioned rescue).
- ML feasibility.
- Cost-model revision.
- New strategy-family discovery.
- Project-lock revision.
- Threshold revision.

If the operator selects Option A, Phase 3p is closed and the project remains at the post-Phase-3p consolidated boundary.

---

## 11. Explicit preservation

This memo preserves the following items unchanged:

- **No threshold changes.** §10.3 (Δexp ≥ +0.10 R), §10.4 (absolute floors expR > −0.50 AND PF > 0.30), §11.3 (V-window no-peeking), §11.4 (ETH non-catastrophic), §11.6 (8 bps HIGH per side cost-resilience) preserved verbatim.
- **No strategy-parameter changes.** R3 sub-parameters preserved. F1 parameters preserved. D1-A parameters preserved.
- **No project-lock changes.** §1.7.3 project-level locks preserved verbatim.
- **No prior verdict changes.** R3 remains V1 breakout baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained research evidence only. R2 remains FAILED — §11.6 cost-sensitivity blocks. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other.
- **No backtests.** No backtest run by Phase 3p.
- **No data download.** No data fetched from any source by Phase 3p.
- **No v003 creation.** v002 datasets remain canonical; no v003 dataset created or staged.
- **No supplemental 5m dataset created.**
- **No derived 5m-resolution tables created.**
- **No 5m analysis.** No diagnostic computation performed. No diagnostic table produced. No diagnostic plot produced.
- **No timestamp-policy changes.**
- **No dataset-versioning policy changes.**
- **No cost-model revision.** Phase 3l's "B — current cost model conservative but defensible" assessment stands. §11.6 unchanged.
- **No regime-first authorization.** Phase 3m's "remain paused" recommendation stands.
- **No 5m timeframe authorization.** Phase 3n's "remain paused" recommendation stands.
- **No 5m diagnostics-spec authorization beyond what Phase 3o already established.** Phase 3o's predeclared question set Q1–Q7 and forbidden question forms remain immutable.
- **No ML feasibility authorization.**
- **No new strategy-family discovery authorization.**
- **No D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid authorization.**
- **No paper/shadow planning authorization.**
- **No Phase 4 runtime / state / persistence authorization.**
- **No live-readiness authorization.**
- **No deployment authorization.**
- **No production-key creation authorization.**
- **No exchange-write capability authorization.**
- **No MCP / Graphify / `.mcp.json` activation.**
- **No credentials requested or used.**
- **No authenticated / private Binance API calls made.**
- **No data/ commits.** v002 manifests untouched.
- **No next phase started.**

The output of Phase 3p is this single memo. No code, no tests, no scripts, no data, no thresholds, no strategy parameters, no project locks, no paper/shadow, no Phase 4, no live-readiness, no deployment, no credentials, no MCP, no Graphify, no `.mcp.json`, and no exchange-write work has changed.

Phase 3p is a docs-only data-requirements and execution-plan memo. The operator decides what (if anything) follows.
