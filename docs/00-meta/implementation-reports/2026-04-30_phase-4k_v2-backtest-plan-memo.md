# Phase 4k — V2 Backtest-Plan Memo

**Authority:** Operator authorization for Phase 4k (Phase 4j §1 / §17.2
recommended next phase: docs-only V2 backtest-plan memo under the
Phase 4j §11 metrics OI-subset partial-eligibility rule); Phase 4j
§11 (binding metrics OI-subset partial-eligibility rule); Phase 4i
(V2 public data acquisition + integrity validation; partial-pass
verdict; 4 of 6 datasets research-eligible; 2 of 6 metrics datasets
NOT research-eligible); Phase 4h (V2 data requirements / feasibility
memo); Phase 4g (V2 strategy-spec memo: Participation-Confirmed
Trend Continuation; signal 30m; bias 4h; session bucket 1h; 8 entry
+ 3 exit / regime features; 512-variant predeclared threshold grid;
M1 / M2 / M3 mechanism-check decomposition; four governance-label
declarations); Phase 4f §22 (V2 hypothesis predeclaration); Phase 4e
(reconciliation-model design memo, NOT yet enforced in code); Phase
3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8
(break-even / EMA slope / stagnation governance); Phase 3r §8
(mark-price gap governance — analogous-precedent for Phase 4j §11
per-bar exclusion pattern); Phase 3q (5m supplemental acquisition
pattern); Phase 3p §4.7 / §6.2 (strict integrity gate semantics);
Phase 3o §5–§10 (predeclaration discipline); Phase 3t §12 (validity
gate for any future V2-style hypothesis); Phase 2i §1.7.3
(project-level locks); Phase 2p §C.1 (R3 baseline-of-record); Phase
2w §16.1 (R2 §11.6 cost-sensitivity FAIL); Phase 3c §7.3
(catastrophic-floor predicate); Phase 3h §11.2 (D1-A MECHANISM PASS /
FRAMEWORK FAIL — other);
`docs/03-strategy-research/v1-breakout-strategy-spec.md`;
`docs/03-strategy-research/v1-breakout-backtest-plan.md`;
`docs/05-backtesting-validation/v1-breakout-validation-checklist.md`;
`docs/04-data/data-requirements.md`;
`docs/04-data/live-data-spec.md`;
`docs/04-data/timestamp-policy.md`;
`docs/04-data/dataset-versioning.md`;
`docs/07-risk/stop-loss-policy.md`;
`docs/07-risk/position-sizing-framework.md`;
`docs/07-risk/exposure-limits.md`;
`docs/12-roadmap/phase-gates.md`;
`docs/12-roadmap/technical-debt-register.md`;
`docs/00-meta/ai-coding-handoff.md`;
`.claude/rules/prometheus-core.md`;
`.claude/rules/prometheus-safety.md`;
`.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4k — **V2 Backtest-Plan Memo** (docs-only). Predeclares
exactly how a future V2 backtest execution phase would be implemented,
validated, reported, and judged, using the Phase 4g locked V2 strategy
spec, the Phase 4i acquired datasets, and the Phase 4j §11 metrics
OI-subset governance rule. **Phase 4k does NOT run the backtest.
Phase 4k does NOT implement the backtest. Phase 4k does NOT modify
code, data, or manifests. Phase 4k does NOT write backtest code.
Phase 4k does NOT acquire data. Phase 4k does NOT modify Phase 4g V2
strategy-spec selections. Phase 4k does NOT revise prior verdicts.
Phase 4k does NOT authorize paper / shadow / live / exchange-write.**

**Branch:** `phase-4k/v2-backtest-plan-memo`. **Memo date:** 2026-04-30
UTC.

---

## Summary

Phase 4j adopted the Phase 4j §11 metrics OI-subset partial-eligibility
rule as binding governance, transposing Phase 3r §8 mark-price gap
governance from per-trade exclusion to per-bar exclusion. Under that
rule, V2 may proceed toward a future first backtest using the four
research-eligible Phase 4i kline datasets (BTC + ETH × 30m + 4h),
the OI subset of the Phase 4i metrics datasets (under strict per-bar
exclusion), and the existing v002 funding manifests, while categorically
forbidding optional ratio-column access, forward-fill, interpolation,
imputation, and any silent omission.

Phase 4k is the predeclared backtest-plan memo for that future
execution phase. Phase 4k commits — *before* any V2 backtest is run
or any V2 backtest code is written — every methodological choice
that the future execution phase will be required to honor:

- the dataset-input set (4 research-eligible kline datasets +
  metrics OI-subset under Phase 4j §11 + v002 funding manifests);
- the feature-implementation plan for each of the 8 active V2 entry
  features and 3 active V2 exit / regime features per Phase 4g §28;
- the per-bar Phase 4j §11 OI-feature-eligibility test algorithm and
  exclusion-counts reporting requirements;
- the categorical prohibition on optional ratio-column access;
- the signal-generation truth table, entry execution model
  (next-30m-bar-open market entry consistent with V1 / R3), and exit
  model (initial structural stop + ATR buffer; fixed-R take-profit
  N_R ∈ {2.0, 2.5}; unconditional time-stop T_stop ∈ {12, 16} 30m
  bars);
- the cost / slippage model (§11.6 = 8 bps HIGH per side preserved
  verbatim; LOW / MEDIUM / HIGH cells; funding cost included);
- the position-sizing assumption (0.25% risk; 2× leverage cap; one
  position; BTCUSDT primary, ETHUSDT comparison only);
- the threshold-grid handling policy (Phase 4g §29 fixed at 512
  variants; future execution phase MUST commit to either Option A —
  reduce search space at brief time — or Option B — apply full PBO /
  deflated Sharpe / CSCV with 512-variant reporting; **Phase 4k
  recommends Option B with no further reduction at brief time** so
  that Phase 4g's predeclared grid is honored verbatim);
- the chronological train / validation / holdout split (predeclared
  with exact UTC date boundaries: train 2022-01-01..2023-06-30;
  validation 2023-07-01..2024-06-30; out-of-sample holdout
  2024-07-01..2026-03-31);
- the BTCUSDT-primary / ETHUSDT-comparison protocol
  (cross-symbol consistency required; ETH cannot rescue BTC failure;
  no cross-symbol optimization);
- the M1 / M2 / M3 mechanism-check implementation plan per Phase 4g
  §30 (M1 ≥ 50% trades reach +0.5R MFE on BOTH symbols; M2 ≥ +0.10R
  expectancy uplift over participation-relaxed degenerate variant on
  BOTH symbols; M3 ≥ +0.05R expectancy uplift over derivatives-relaxed
  degenerate variant AND §11.6 HIGH cost-resilience non-degraded);
- the catastrophic-floor predicate set (insufficient trade count;
  negative OOS expectancy under HIGH cost; predeclared catastrophic
  drawdown beyond −10R cumulative or PF < 0.50; BTCUSDT failure
  even with ETHUSDT pass; train-only performance with OOS failure;
  excessive PBO > 0.5; overconcentration in one regime / month;
  sensitivity-cell failure under exclude-entire-affected-days;
  excluded-bar fraction materially changing conclusion);
- the promotion / failure / partial-pass criteria (mirroring R3 /
  R2 / F1 / D1-A retained-evidence framing);
- the required reporting tables and required-plot list;
- the stop conditions for any future execution-phase implementation;
- the reproducibility requirements (commit SHAs; manifest references;
  zero-credentials confirmation);
- the explicit forbidden-work list.

**Phase 4k is docs-only.** **Phase 4k does NOT run any backtest.**
**Phase 4k does NOT implement V2.** **Phase 4k does NOT acquire,
modify, or delete any data, manifest, or script.**

V2 remains **pre-research only**: not implemented; not backtested;
not validated; not live-ready; **not a rescue** of R3 / R2 / F1 /
D1-A.

**Verification (run on the post-Phase-4j-merge tree, captured by
Phase 4k):**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**Recommended next phase:** **Phase 4l — V2 Backtest Execution
(docs-and-code)** as primary, executing exactly this Phase 4k plan
under the Phase 4j §11 binding rule with no methodological deviation.
**Remain paused** is the conditional secondary. **No** immediate
implementation authorized; **no** paper / shadow / live; **no**
strategy-spec amendment; **no** governance-rule amendment.

**Recommended state remains paused. No successor phase has been
authorized.**

---

## Authority and boundary

Phase 4k operates strictly inside the post-Phase-4j-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10;
  Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase
  3t consolidation; Phase 3u §10 / §11; Phase 3v §8 (stop-trigger-domain
  governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope /
  stagnation governance); Phase 4a's anti-live-readiness statement;
  Phase 4d review; Phase 4e reconciliation-model design memo; Phase
  4f V2 hypothesis predeclaration; Phase 4g V2 strategy spec; Phase
  4h V2 data requirements / feasibility memo; Phase 4i V2 acquisition
  + integrity validation; **Phase 4j §11 metrics OI-subset
  partial-eligibility rule (binding from Phase 4j merge forward;
  immutable absent a separately authorized governance amendment).**
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md`
  unchanged.
- **Project-level locks preserved verbatim.** §1.7.3 (BTCUSDT primary
  live; ETHUSDT research / comparison only; one-symbol-only live;
  one-position max; 0.25% risk; 2× leverage cap; mark-price stops;
  v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 /
  §11.4 / §11.6 (= 8 bps HIGH per side).
- **Retained-evidence verdicts preserved verbatim.** R3
  baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
  F1 / D1-A retained research evidence only; R2 FAILED — §11.6;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.**
  `.claude/rules/prometheus-safety.md`.
- **MCP and secrets rules preserved verbatim.**
  `.claude/rules/prometheus-mcp-and-secrets.md`.
- **Phase 4g V2 strategy-spec selections preserved verbatim.** Phase
  4k does NOT modify Phase 4g §28 active feature set (8 entry + 3
  exit / regime), §11 timeframe matrix (signal 30m, bias 4h, session
  / volume bucket 1h), §29 threshold grid (512 variants), §30
  M1 / M2 / M3 mechanism-check decomposition, or §22–§24 governance
  labels.
- **Phase 4i manifests preserved verbatim.** All six Phase 4i
  manifests
  (`binance_usdm_<symbol>_<interval-or-metrics>__v001.manifest.json`)
  remain unchanged. The two metrics manifests retain
  `research_eligible: false`. Phase 4j made no modification; Phase
  4k makes none.
- **Phase 4j §11 binding rule preserved verbatim.** Phase 4k does
  NOT amend, relax, or extend Phase 4j §11. Phase 4k incorporates
  Phase 4j §11 as a binding constraint on the Phase 4l execution
  phase.

Phase 4k adds *only* a forward-looking backtest-plan memo without
modifying any prior phase memo, any data, any code, any rule, any
threshold, any manifest, any verdict, any lock, or any gate. The
plan binds Phase 4l execution behavior if Phase 4l is ever authorized.

---

## Starting state

```text
branch:           phase-4k/v2-backtest-plan-memo
parent commit:    afa225ac0486910f9de675844bfe499115e168cd (post-Phase-4j-merge housekeeping)
working tree:     clean before memo authoring
main:             afa225ac0486910f9de675844bfe499115e168cd (unchanged)

Phase 4a foundation:                                          merged.
Phase 4b/4c cleanup:                                          merged.
Phase 4d review:                                              merged.
Phase 4e reconciliation-model design memo:                    merged.
Phase 4f V2 hypothesis predeclaration:                        merged.
Phase 4g V2 strategy spec:                                    merged.
Phase 4h V2 data-requirements / feasibility memo:             merged.
Phase 4i V2 public data acquisition + integrity:              merged (partial-pass; metrics not eligible).
Phase 4j V2 metrics data governance memo:                     merged (Phase 4j §11 binding).

Repository quality gate:                fully clean.
research thread (5m):                   operationally complete and closed (Phase 3t).
v002 datasets:                          locked; manifests untouched.
v001-of-5m datasets:                    trade-price research-eligible; mark-price research_eligible:false (Phase 3r §8 governs).
Phase 4i datasets:                      30m + 4h klines × 2 research-eligible; metrics × 2 NOT research-eligible (Phase 4j §11 governs feature-level OI-subset use).
```

---

## Why this plan exists

Phase 4j makes V2 backtesting *procedurally permissible* under Phase
4j §11 binding rule. It does not make V2 backtesting *methodologically
authorized*. The gap between "may use the OI subset under per-bar
exclusion" and "may run a 512-variant grid backtest with chronological
holdout, deflated Sharpe / PBO / CSCV correction, and M1 / M2 / M3
mechanism-check evaluation" must be filled by a predeclared,
operator-approved methodology before any V2 backtest is run.

That gap is exactly what Phase 4f / 4g / 4h / 4i / 4j leave open:

- Phase 4f predeclared the V2 hypothesis (too abstract to test).
- Phase 4g operationalized the hypothesis into a strategy spec
  (cannot be backtested without an execution methodology).
- Phase 4h identified what data was needed (cannot be backtested
  without that data being acquired and integrity-checked).
- Phase 4i acquired the data (partial pass; metrics not eligible).
- Phase 4j adopted the metrics governance rule (V2 backtest now
  procedurally permissible *if* the rule is honored exactly).

Phase 4k closes the gap. After Phase 4k merges, the V2 backtest
methodology is fixed: a future Phase 4l execution phase MUST operate
inside the bounds Phase 4k sets here. Without Phase 4k, every
V2-backtest design degree of freedom would be unbounded, and every
choice (split dates, cost cell handling, mechanism-check thresholds,
catastrophic-floor predicates, reporting structure, sensitivity
analyses) would risk being chosen *after* observing data — exactly
the failure mode Bailey / Borwein / López de Prado / Zhu (2014)
document as the leading cause of out-of-sample collapse.

This is the same anti-data-snooping discipline the project applied
to (a) the Phase 3o predeclared 5m diagnostic question set Q1–Q7
(committed before any 5m data existed), (b) the Phase 4f predeclared
V2 hypothesis (committed before any V2 data existed), (c) the Phase
4g predeclared 8+3 feature set and 512-variant grid (committed before
any 30m / 4h V2 data existed), and (d) the Phase 4j §11 binding
metrics governance rule (committed before any V2 backtest exists).
Phase 4k extends that discipline to the V2 backtest methodology.

Phase 4k is **methodology-design discipline**, not strategy execution
or implementation. It does not authorize, prepare for, or imply any
V2 backtest, V2 implementation, paper / shadow run, live-readiness
work, or successor phase.

---

## Relationship to Phase 4f / 4g / 4h / 4i / 4j

Phase 4k is the direct backtest-methodology operationalization of the
Phase 4f → 4g → 4h → 4i → 4j chain.

| Phase | Predeclared | Phase 4k role |
|---|---|---|
| Phase 4f | V2 hypothesis (Participation-Confirmed Trend Continuation); candidate feature buckets; candidate timeframe matrix | Phase 4k inherits Phase 4f §22 hypothesis statement verbatim; references but does not modify. |
| Phase 4g | exact V2 strategy spec (signal 30m, bias 4h, session 1h, 8+3 features, 512-variant grid, M1 / M2 / M3 decomposition, four governance labels) | Phase 4k builds the backtest plan ON TOP of Phase 4g; does NOT modify Phase 4g; references all locked selections verbatim. |
| Phase 4h | exact data plan (6-family minimum acquisition; manifest schema; integrity-check rules) | Phase 4k inherits Phase 4h's research-eligibility convention and timestamp policy verbatim; references but does not modify. |
| Phase 4i | acquired data (4 of 6 research-eligible; 2 metrics not eligible); manifests committed | Phase 4k uses the 4 research-eligible kline datasets directly; uses the 2 metrics datasets only via the Phase 4j §11 OI-subset partial-eligibility rule; references but does not modify. |
| Phase 4j | metrics OI-subset partial-eligibility rule (binding; immutable) | Phase 4k incorporates Phase 4j §11 as a binding execution constraint; does NOT amend Phase 4j §11. |

Phase 4k does NOT modify Phase 4f / 4g / 4h / 4i / 4j text. Phase 4k
does NOT modify Phase 4i manifests, Phase 4i acquisition script, or
any v002 / v001-of-5m manifest. Phase 4k does NOT acquire, normalize,
or transform any data.

---

## V2 hypothesis and locked strategy spec recap

### V2 hypothesis (per Phase 4f §22; preserved verbatim)

**V2 — Participation-Confirmed Trend Continuation.**

Trade trend-continuation / breakout events on BTCUSDT perpetual **only
when four conditions align simultaneously**:

1. **Price structure** signals trend-continuation (Donchian breakout
   from recent compression with confirming HTF trend bias).
2. **Volatility regime** is in a *post-compression / expansion-friendly*
   state.
3. **Participation / volume** confirms the breakout.
4. **Derivatives-flow context** is non-pathological.

V2 is **pre-research only**: not implemented; not backtested; not
validated; not live-ready; **not a rescue** of R3 / R2 / F1 / D1-A;
**not derived from Phase 3s Q1–Q7 findings** (validity gate per
Phase 3t §12).

### V2 timeframe matrix (per Phase 4g §11; preserved verbatim)

| Role | Selected | Phase 4f candidate set |
|---|---|---|
| Signal timeframe | **30m** | 15m / 30m / 1h |
| Higher-timeframe bias | **4h** | 1h / 4h |
| Session / volume bucket | **1h** | 30m / 1h |
| 5m | **diagnostic-only, not primary signal** | 5m diagnostic-only |

### V2 active feature set (per Phase 4g §28; preserved verbatim)

**8 active entry features:**

1. HTF trend bias state (4h EMA(20)/EMA(50) discrete comparison).
2. Donchian breakout state (30m Donchian high(N1) / low(N1)).
3. Donchian width percentile (compression precondition).
4. Range-expansion ratio (breakout-bar TR vs. trailing mean).
5. Relative volume + volume z-score (parameterizing one participation
   construct with two thresholds).
6. Volume percentile by UTC hour.
7. Taker buy/sell imbalance (kline `taker_buy_volume`).
8. OI delta direction + funding-rate percentile band (parameterizing
   one derivatives-flow construct with two sub-conditions).

**3 active exit / regime features:**

1. Time-since-entry counter (drives unconditional time-stop).
2. ATR percentile regime gate (recorded; not acted on as exit).
3. HTF bias state continuity (recorded; not acted on as exit).

### V2 threshold grid (per Phase 4g §29; preserved verbatim)

**Total combinatorial search-space cardinality: 512 variants** (=
2^9 over 9 non-fixed binary axes).

The 9 non-fixed axes:

| # | Axis | Cardinality |
|---|---|---|
| 1 | N1 (Donchian breakout lookback) | 2 (`{20, 40}` 30m bars) |
| 2 | P_w max (Donchian width percentile cap) | 2 (`{25, 35}`) |
| 3 | V_rel_min (relative-volume minimum) | 2 (`{1.5, 2.0}`) |
| 4 | V_z_min (volume z-score minimum) | 2 (`{0.5, 1.0}`) |
| 5 | T_imb_min (taker-imbalance minimum) | 2 (`{0.55, 0.60}`) |
| 6 | OI_dir (OI delta direction policy) | 2 (`{aligned, non_negative}`) |
| 7 | Funding band ([P_fund_low, P_fund_high]) | 2 (`{[20, 80], [30, 70]}`) |
| 8 | N_R (fixed-R take-profit) | 2 (`{2.0, 2.5}`) |
| 9 | T_stop (time-stop horizon) | 2 (`{12, 16}` 30m bars) |

All other Phase 4g §29 parameters are fixed (cardinality 1):
`L_w`, `L_atr`, `N_re`, `[P_atr_low, P_atr_high]`, `RE min`, `L_vol`,
`Q_session`, `L_session`, `N_oi`, `[P_oi_low, P_oi_high]`, `L_fund`,
stop ATR buffer, stop-distance min / max, cooldown horizon `C`.

### V2 governance labels (per Phase 4g §22 / §23 / §24; preserved verbatim)

| Scheme | V2 declared value | Phase 3v / 3w binding |
|---|---|---|
| `stop_trigger_domain` (research) | `trade_price_backtest` | Phase 3v §8 |
| `stop_trigger_domain` (future runtime) | `mark_price_runtime` | Phase 3v §8 |
| `stop_trigger_domain` (future live-readiness validation) | `mark_price_backtest_candidate` | Phase 3v §8.5 |
| `break_even_rule` | `disabled` | Phase 3w §6.3 |
| `ema_slope_method` | `discrete_comparison` | Phase 3w §7.3 |
| `stagnation_window_role` | `metric_only` | Phase 3w §8.3 |
| `mixed_or_unknown` | invalid; fail-closed at any decision boundary | Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3 |

### V2 mechanism-check decomposition (per Phase 4g §30; preserved verbatim)

- **M1 — Price-structure mechanism:** ≥ 50% trades reach +0.5R MFE on
  BOTH BTCUSDT and ETHUSDT.
- **M2 — Participation mechanism:** mean R of full V2 ≥ mean R of
  participation-relaxed degenerate variant + 0.10R on BOTH symbols
  with bootstrap-by-trade stat-significance.
- **M3 — Derivatives-context mechanism:** mean R of full V2 ≥ mean R
  of derivatives-relaxed degenerate variant + 0.05R on BOTH symbols,
  AND §11.6 HIGH cost-resilience non-degraded.

---

## Data availability recap

Per Phase 4i acquisition + integrity validation:

### Research-eligible datasets (4 of 6)

| Dataset | Symbol | Family | Bars | First UTC | Last UTC | Eligible |
|---|---|---|---|---|---|---|
| `binance_usdm_btcusdt_30m__v001` | BTCUSDT | klines 30m | 74 448 | 2022-01-01 00:00:00 | 2026-03-31 23:30:00 | **YES** |
| `binance_usdm_ethusdt_30m__v001` | ETHUSDT | klines 30m | 74 448 | 2022-01-01 00:00:00 | 2026-03-31 23:30:00 | **YES** |
| `binance_usdm_btcusdt_4h__v001` | BTCUSDT | klines 4h | 9 306 | 2022-01-01 00:00:00 | 2026-03-31 20:00:00 | **YES** |
| `binance_usdm_ethusdt_4h__v001` | ETHUSDT | klines 4h | 9 306 | 2022-01-01 00:00:00 | 2026-03-31 20:00:00 | **YES** |

All four kline datasets PASS Phase 4h §17 strict integrity gate
(monotone timestamps; zero gaps; complete OHLC sanity; complete
`taker_buy_volume`; full date-range coverage).

### Globally non-research-eligible datasets (2 of 6)

| Dataset | Symbol | Family | Records | Missing 5m obs | NaN ratio rows | OI columns | Eligible |
|---|---|---|---|---|---|---|---|
| `binance_usdm_btcusdt_metrics__v001` | BTCUSDT | metrics 5m | 446 555 / 446 688 | 5 699 | 91 840 | **0 NaN** | **NO (globally)** |
| `binance_usdm_ethusdt_metrics__v001` | ETHUSDT | metrics 5m | 446 555 / 446 688 | 3 631 | 91 841 | **0 NaN** | **NO (globally)** |

Both metrics datasets FAIL Phase 4h §17 strict gate but the V2-required
`sum_open_interest` and `sum_open_interest_value` columns are FULLY
POPULATED (0 NaN) for both symbols across the entire 4-year coverage.
**Per Phase 4j §11, the OI subset (`create_time`, `symbol`,
`sum_open_interest`, `sum_open_interest_value`) is feature-eligible
for V2's first backtest under strict per-bar exclusion.**

### Funding manifests (reused from v002)

- `binance_usdm_btcusdt_funding__v002.manifest.json` (existing v002).
- `binance_usdm_ethusdt_funding__v002.manifest.json` (existing v002).

V2's funding-rate-percentile feature (Phase 4g §17 sub-component (b))
uses these existing v002 funding manifests directly. No re-acquisition.

### Datasets NOT used by V2 first backtest

- **Mark-price 30m / 4h klines.** DEFERRED per Phase 4h §20 / Phase
  4i §"Operator decision menu" Option C. Not acquired. Not used.
- **`aggTrades` (tick-level).** OPTIONAL / DEFERRED per Phase 4h §7.E /
  Phase 4i §"Operator decision menu" Option D. Not acquired. Not used.
- **Optional metrics ratio columns.** Categorically forbidden by
  Phase 4j §11.3 / §14. Not read. Not used.
- **Spot data.** Forbidden by §1.7.3 (perpetual-only).
- **Cross-venue data.** Forbidden by §1.7.3 (single-venue Binance
  USDⓈ-M).
- **Authenticated REST / private endpoints / user stream / WebSocket /
  listenKey lifecycle.** Forbidden by `.claude/rules/prometheus-safety.md`.

---

## Metrics governance recap

Phase 4j §11 metrics OI-subset partial-eligibility rule is binding
from the Phase 4j merge (`ea948017...`) forward. Restated for Phase
4k binding context:

1. Metrics manifests **remain globally `research_eligible: false`**.
2. **Feature-level partial-eligibility** for the OI subset
   (`create_time`, `symbol`, `sum_open_interest`,
   `sum_open_interest_value`) only.
3. **Optional ratio columns remain feature-ineligible** for V2's
   first backtest. They MUST NOT be read.
4. **Per-bar exclusion test:** any 30m V2 signal bar requires all
   six aligned 5-minute records (offsets 0, 5, 10, 15, 20, 25 minutes
   from bar open) present AND each with non-NaN `sum_open_interest`
   AND non-NaN `sum_open_interest_value`. Failing bars are excluded
   from V2 candidate setup generation entirely.
5. **No forward-fill, interpolation, imputation, replacement,
   synthetic OI data, or silent omission.**
6. **Exclusions counted and reported.** Per-symbol, per-day, per-bar,
   cumulative.
7. **Sensitivity analysis required.** main-cell vs.
   exclude-entire-affected-days.
8. **No automatic prior-verdict revision.**
9. **No strategy rescue, no parameter change, no live-readiness
   implication.**
10. **No silent rule revision.** Phase 4j §11 is immutable absent a
    separately authorized governance amendment.
11. **Per-bar exclusion algorithm must be predeclared in any future
    V2 backtest brief.** Phase 4k now satisfies this requirement
    (§"Metrics OI per-bar exclusion implementation plan" below).
12. **Optional ratio activation requires separate operator
    authorization.**

**OI delta computation rule (per Phase 4j §17 / §11.4):** for each
OI-feature-eligible 30m signal bar at `bar_open_time_ms`,

```text
oi_at_bar_close       = metrics record at create_time = bar_open_time_ms + 25*60*1000
oi_at_prev_window_close = metrics record at create_time = bar_open_time_ms -  5*60*1000
oi_delta              = oi_at_bar_close - oi_at_prev_window_close
```

(Last completed 5-minute OI of current 30m window vs. last completed
5-minute OI of previous 30m window. Point-in-time clear; no future
records; no partial windows; no mean-over-window aggregation.)

For long V2 entries: `oi_delta_aligned = oi_delta >= 0` (under
`OI_dir = non_negative`) or `oi_delta_aligned = oi_delta > 0` (under
`OI_dir = aligned`). Mirrors for shorts.

---

## Backtest purpose

The future V2 backtest is a research-only test of the following
narrowly-scoped questions:

1. **Mechanism question 1 (M1):** under V2's locked entry conditions,
   do at least half of the resulting trades reach +0.5R MFE before
   stop on each of BTCUSDT and ETHUSDT?
2. **Mechanism question 2 (M2):** does V2's participation-confirmation
   layer (relative volume + volume z-score + UTC-hour percentile +
   taker imbalance) add at least +0.10R per-trade expectancy versus
   a price-only V2 skeleton on each of BTCUSDT and ETHUSDT?
3. **Mechanism question 3 (M3):** does V2's derivatives-flow-context
   layer (OI-delta direction policy + funding-rate percentile band)
   add at least +0.05R per-trade expectancy versus a derivatives-relaxed
   V2 skeleton AND non-degrade §11.6 HIGH cost-resilience on each of
   BTCUSDT and ETHUSDT?
4. **Cost-survival question:** does the V2 framework — at each variant
   that passes M1 / M2 / M3 — produce non-negative expectancy under
   §11.6 HIGH (8 bps per side) on BTCUSDT?
5. **Cross-symbol question:** are BTCUSDT V2 results directionally
   supported by ETHUSDT comparison (sign-consistency in expectancy
   across symbols)?
6. **OOS persistence question:** do train-window-selected V2 variants
   preserve their relative ordering on the validation window and the
   2024-07..2026-03 out-of-sample holdout, after deflated-Sharpe / PBO
   correction?

The future V2 backtest **MUST NOT** be described as, framed as,
implied to be, or equated to:

- V2 implementation;
- V2 paper-shadow readiness;
- V2 live-readiness;
- V2 deployment readiness;
- V2 production-key readiness;
- V2 exchange-write readiness;
- live-readiness validation step (that requires a separately
  authorized `mark_price_backtest_candidate` modeling pass per
  Phase 3v §8.5);
- approval of any §11.6 / §1.7.3 / Phase 3r §8 / Phase 3v §8 / Phase
  3w / Phase 4j §11 governance amendment.

A V2 backtest that passes all M1 / M2 / M3 mechanism checks and the
cost-survival / cross-symbol / OOS-persistence questions still does
NOT authorize V2 implementation. Implementation authorization
requires a separately authorized phase brief AFTER the backtest
result, NOT inferred FROM the backtest result.

---

## Backtest non-goals

The future V2 backtest **MUST NOT**:

- modify any retained-evidence verdict (R3 / H0 / R1a / R1b-narrow /
  R2 / F1 / D1-A);
- modify any project lock (§1.7.3 / §11.6 / mark-price stops / v002
  verdict provenance);
- modify any threshold (§10.3 / §10.4 / §11.3 / §11.4 / §11.6);
- modify any strategy spec (Phase 4g V2; Phase 2e V1);
- modify any governance rule (Phase 3r §8; Phase 3v §8; Phase 3w §6 /
  §7 / §8; Phase 4j §11);
- propose a V2 spec amendment based on observed data;
- propose a Phase 4j §11 amendment based on observed exclusion rates;
- propose optional ratio-column activation;
- propose OI feature removal;
- propose mark-price 30m / 4h acquisition;
- propose aggTrades acquisition;
- propose v003 dataset creation;
- propose v002 dataset modification;
- propose Phase 4i manifest modification;
- propose Phase 3q v001-of-5m manifest modification;
- justify a future V2 strategy implementation;
- justify a future V2 paper / shadow run;
- justify a future V2 live-readiness implication;
- justify a future Phase 4 (canonical) start;
- justify an authentication-API / private-endpoint / WebSocket /
  user-stream / listenKey / production-alerting / Telegram / n8n
  production-route / MCP / Graphify / `.mcp.json` / credentials path;
- justify any production Binance key creation;
- justify any exchange-write capability.

---

## Backtest execution phases proposed

Phase 4k recommends a single V2 backtest execution phase named
**Phase 4l — V2 Backtest Execution (docs-and-code)**. Phase 4l would:

1. Implement a standalone V2 backtest module / script.
2. Load the four research-eligible Phase 4i kline datasets.
3. Load the metrics datasets via the Phase 4j §11 OI subset under
   per-bar exclusion.
4. Reuse the existing v002 funding manifests for funding percentiles.
5. Compute the 11 active V2 features (8 entry + 3 exit / regime).
6. Generate V2 candidate setups across the 512-variant predeclared
   threshold grid.
7. Apply the entry / exit lifecycle with Phase 4g §19 / §20 specifics.
8. Aggregate per-variant trade populations on chronological train /
   validation / out-of-sample holdout windows.
9. Compute M1 / M2 / M3 mechanism-check tables.
10. Apply deflated Sharpe / PBO / CSCV corrections per Phase 4g §31.
11. Produce the V2 backtest report.
12. Stop. Phase 4l does NOT recommend any successor phase by design.
    The operator decides post-Phase-4l next steps.

**Phase 4k does NOT authorize Phase 4l.** Phase 4k merely defines
the methodology Phase 4l would honor if Phase 4l is ever authorized.
Phase 4l authorization is a separate operator decision after Phase
4k is reviewed and merged.

---

## Required future implementation artefacts

The future Phase 4l execution phase, IF EVER AUTHORIZED, would be
allowed to create the following artefacts. **Phase 4k does NOT
create any of them.**

### Standalone V2 backtest script / module

Likely path: `scripts/phase4l_v2_backtest.py`.

Layout pattern: standalone-script analogous to
`scripts/phase4i_v2_acquisition.py` and
`scripts/phase3q_5m_acquisition.py`. NO `prometheus.research.data.*`
extension. NO `Interval` enum extension. NO `prometheus.strategy.*`
extension. NO `src/prometheus/**` modification.

Forbidden imports:

- `prometheus.execution.fake_adapter` — V2 backtest is research-only
  and does NOT exercise the Phase 4a runtime fake adapter.
- `prometheus.runtime.*` — no runtime state, no kill switch, no
  reconciliation.
- `prometheus.persistence.runtime_store` — no SQLite runtime DB
  writes.
- `prometheus.events.*` — no event-bus traffic.
- Any module that performs network I/O.
- Any module that touches authenticated APIs.
- Any module that imports from a credentials store.

Allowed imports (research-side only):

- `pandas`, `numpy`, `pyarrow`.
- Standard library: `datetime` (with `UTC`), `pathlib`, `dataclasses`,
  `typing`, `argparse`, `json`, `hashlib`, `csv`, `zipfile`,
  `concurrent.futures`, `logging`.
- `pydantic` v2 for value-object schemas (consistent with the Phase
  4i orchestrator pattern).
- `scipy.stats` for bootstrap-by-trade and CSCV computations
  (consistent with prior Phase 2 / Phase 3 conventions).

### V2 feature-generation code

Pure-function, side-effect-free feature computers, one per active
V2 feature. Each MUST take only completed-bar input data and produce
deterministic outputs without lookahead.

### V2 strategy-signal code

Pure-function entry-condition evaluators per the Phase 4g §13 truth
table. Cooldown logic per Phase 4g §22. No discretionary overrides.

### V2 validation / reporting code

Per-variant results aggregator; M1 / M2 / M3 mechanism-check
computation; deflated Sharpe / PBO / CSCV computation; chronological
holdout split; report-table emission.

### V2 backtest report

A new Markdown artefact under
`docs/00-meta/implementation-reports/`. Content exhaustively
specified in §"Required reporting tables" and §"Required plots or
diagnostics" below.

### V2 result tables

CSV / Parquet outputs under `data/research/phase4l/` (gitignored
per existing convention). Exhaustively specified in §"Required
reporting tables" below.

### Forbidden artefacts

The Phase 4l execution phase, IF EVER AUTHORIZED, **MUST NOT** create:

- live / runtime code touching real exchange endpoints;
- V2 implementation code under `src/prometheus/strategy/`;
- a V2 paper / shadow runtime;
- a V2 live-readiness configuration;
- production keys, `.env` files, `.mcp.json` modifications, MCP
  server enabling, Graphify enabling;
- mark-price 30m / 4h data, aggTrades data, spot data, cross-venue
  data;
- v003 dataset family;
- modified v002 / v001-of-5m / Phase 4i manifests;
- modified Phase 4i acquisition script (the Phase 4i orchestrator
  is preserved verbatim);
- ambiguity-log modifications driven by V2 backtest outcomes
  (V2 outcomes do not introduce or close pre-coding ambiguity-log
  items by definition; per Phase 4j §11.8 / §11.9).

**Phase 4k does NOT implement any of these. Phase 4k is text-only.**

---

## Dataset inputs

The future V2 backtest, IF EVER AUTHORIZED, MUST consume EXACTLY the
following datasets. No others.

### Phase 4i kline datasets (research-eligible; required)

| Dataset | Manifest path | Use in V2 |
|---|---|---|
| `binance_usdm_btcusdt_30m__v001` | `data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json` | Signal-timeframe bars for BTC. |
| `binance_usdm_ethusdt_30m__v001` | `data/manifests/binance_usdm_ethusdt_30m__v001.manifest.json` | Signal-timeframe bars for ETH (comparison only). |
| `binance_usdm_btcusdt_4h__v001` | `data/manifests/binance_usdm_btcusdt_4h__v001.manifest.json` | HTF bias bars for BTC. |
| `binance_usdm_ethusdt_4h__v001` | `data/manifests/binance_usdm_ethusdt_4h__v001.manifest.json` | HTF bias bars for ETH. |

The 1h session / volume bucket per Phase 4g §11.3 is computed from
the 30m klines (UTC-hour aggregation) — no separate 1h dataset is
required.

The future V2 backtest reads the corresponding Parquet partitions
under `data/normalized/klines/symbol=<SYMBOL>/interval=<INTERVAL>/year=YYYY/month=MM/`.

### Phase 4i metrics datasets (NOT research-eligible; OI-subset use only via Phase 4j §11)

| Dataset | Manifest path | Use in V2 |
|---|---|---|
| `binance_usdm_btcusdt_metrics__v001` | `data/manifests/binance_usdm_btcusdt_metrics__v001.manifest.json` | OI-subset (create_time, symbol, sum_open_interest, sum_open_interest_value) under Phase 4j §11. |
| `binance_usdm_ethusdt_metrics__v001` | `data/manifests/binance_usdm_ethusdt_metrics__v001.manifest.json` | OI-subset only. |

The future V2 backtest reads metrics Parquet partitions under
`data/normalized/metrics/symbol=<SYMBOL>/granularity=5m/year=YYYY/month=MM/`
and applies the per-bar exclusion test (§"Metrics OI per-bar exclusion
implementation plan" below) to determine which 30m signal bars are
OI-feature-eligible.

### v002 funding manifests (research-eligible; reused)

| Dataset | Manifest path | Use in V2 |
|---|---|---|
| `binance_usdm_btcusdt_funding__v002` | `data/manifests/binance_usdm_btcusdt_funding__v002.manifest.json` | Funding-rate-percentile feature (V2 entry feature 8 sub-component (b)). |
| `binance_usdm_ethusdt_funding__v002` | `data/manifests/binance_usdm_ethusdt_funding__v002.manifest.json` | Funding-rate-percentile feature for ETH. |

These v002 funding manifests are NOT modified by Phase 4l. The
existing per-funding-event records (8h cadence on BTCUSDT USDⓈ-M) are
read directly.

### Forbidden inputs

The future V2 backtest **MUST NOT** consume:

- mark-price 30m / 4h klines (deferred / not acquired);
- mark-price 5m klines (Phase 3q v001-of-5m; `research_eligible:
  false`; Phase 3r §8 governs);
- mark-price 15m klines (v002 mark-price; reserved for future
  `mark_price_backtest_candidate` validation step per Phase 3v §8.5);
- aggTrades data (deferred);
- spot data (forbidden);
- cross-venue data (forbidden);
- optional metrics ratio columns (forbidden by Phase 4j §11.3);
- any v003 dataset (does not exist; not authorized);
- any modified Phase 4i manifest (preserved verbatim);
- any authenticated REST / private endpoint / public endpoint in code /
  user stream / WebSocket / listenKey lifecycle (forbidden by safety
  rules).

### Dataset-version pinning

The future V2 backtest report MUST pin the exact dataset versions
consumed:

```text
binance_usdm_btcusdt_30m__v001                  manifest_sha256: <recorded>
binance_usdm_ethusdt_30m__v001                  manifest_sha256: <recorded>
binance_usdm_btcusdt_4h__v001                   manifest_sha256: <recorded>
binance_usdm_ethusdt_4h__v001                   manifest_sha256: <recorded>
binance_usdm_btcusdt_metrics__v001              manifest_sha256: <recorded>  research_eligible: false  feature_use: oi_subset_only_per_phase_4j_§11
binance_usdm_ethusdt_metrics__v001              manifest_sha256: <recorded>  research_eligible: false  feature_use: oi_subset_only_per_phase_4j_§11
binance_usdm_btcusdt_funding__v002              manifest_sha256: <recorded>
binance_usdm_ethusdt_funding__v002              manifest_sha256: <recorded>
```

Each `manifest_sha256` is computed from the canonical-form manifest
JSON at the time of the backtest run. The future V2 backtest fails
closed if any manifest is modified between input loading and result
emission.

---

## Feature implementation plan

For each of the 11 active V2 features (8 entry + 3 exit / regime
per Phase 4g §28), the future V2 backtest MUST implement the feature
exactly as specified below. No spec modification.

### Entry feature 1 — HTF trend bias state (4h)

**Inputs:** `binance_usdm_btcusdt_4h__v001` and
`binance_usdm_ethusdt_4h__v001` (per symbol).

**Computation:**

1. Compute EMA(20) and EMA(50) on 4h closes (recursive exponential
   moving average; standard `α = 2 / (N + 1)` formulation).
2. For each completed 4h bar at close-time `T_4h_close`:
   - **Long bias state** is active if:
     - `EMA20(T_4h_close) > EMA50(T_4h_close)`, AND
     - `close(T_4h_close) > EMA20(T_4h_close)`, AND
     - `EMA20(T_4h_close) > EMA20(T_4h_close - 3 × 4h)` (rising vs.
       3 4h bars earlier — discrete comparison per Phase 3w §7.3
       `discrete_comparison`).
   - **Short bias state** is the strict mirror.
   - Otherwise: **neutral**; V2 does not trade.
3. **Point-in-time alignment:** for any 30m signal bar at
   `T_30m_close`, the bias is determined by the most recent 4h bar
   with `T_4h_close <= T_30m_close`. No partial 4h bar is used.

**No lookahead.** Future-bar bias is never used.

**Governance compliance:** Phase 3w §7.3 `discrete_comparison`
declared per Phase 4g §22; `mixed_or_unknown` invalid.

### Entry feature 2 — Donchian breakout state (30m)

**Inputs:** `binance_usdm_<symbol>_30m__v001` (per symbol).

**Computation:**

1. For each completed 30m bar at `T_30m_close`:
   - `donchian_high(N1) = max(high[T_30m_close - N1 × 30m + 30m :
     T_30m_close - 30m])` (highest high of the previous N1 completed
     bars, EXCLUDING the current bar's high).
   - `donchian_low(N1) = min(low[...])` (mirror).
2. **Long breakout trigger:** `close(T_30m_close) > donchian_high(N1) +
   atr_buffer`, where `atr_buffer = 0.10 × ATR(20)` (Phase 4g §29
   locked stop ATR buffer).
3. **Short breakout trigger:** `close(T_30m_close) < donchian_low(N1)
   - atr_buffer` (mirror).
4. **N1 grid:** {20, 40} per Phase 4g §29 axis 1.

**No lookahead.** Donchian uses only previous-N1-bars-excluding-current.

### Entry feature 3 — Donchian width percentile (compression precondition)

**Inputs:** 30m klines.

**Computation:**

1. `donchian_width(T) = donchian_high(N1)(T) - donchian_low(N1)(T)`
   (per the same N1 above).
2. **Trailing percentile:** at `T_30m_close`, compute the percentile
   rank of `donchian_width(T_30m_close)` within the rolling distribution
   of the prior `L_w = 240` 30m bars' donchian_width values (excluding
   the current bar).
3. **Compression precondition passes** if the percentile is `≤ P_w
   max`, where `P_w max ∈ {25, 35}` per Phase 4g §29 axis 2.

**No lookahead.** Trailing distribution uses only prior bars.

### Entry feature 4 — Range-expansion ratio

**Inputs:** 30m klines.

**Computation:**

1. `tr(T) = max(high(T) - low(T), |high(T) - close(T - 30m)|,
   |low(T) - close(T - 30m)|)` (true range; standard).
2. `mean_tr(T) = mean(tr[T - N_re × 30m : T - 30m])` (mean true range
   over trailing `N_re = 20` 30m bars, excluding current).
3. `re(T) = tr(T) / mean_tr(T)`.
4. **Filter passes** if `re(T_30m_close) >= 1.0` (Phase 4g §29 fixed,
   matches V1).

**No lookahead.**

### Entry feature 5 — Relative volume + volume z-score (participation)

**Inputs:** 30m klines `volume`.

**Computation:**

1. `mean_vol(T) = mean(volume[T - L_vol × 30m : T - 30m])` over
   trailing `L_vol = 240` 30m bars.
2. `stdev_vol(T) = stdev(volume[T - L_vol × 30m : T - 30m])` (sample
   stdev with `ddof=1`).
3. `rel_vol(T) = volume(T) / mean_vol(T)`.
4. `vol_z(T) = (volume(T) - mean_vol(T)) / stdev_vol(T)`.
5. **Filter passes** if `rel_vol >= V_rel_min` AND `vol_z >= V_z_min`,
   where `V_rel_min ∈ {1.5, 2.0}` and `V_z_min ∈ {0.5, 1.0}` per Phase
   4g §29 axes 3 and 4.

Both must pass jointly per Phase 4g §16 (the dual gate is approximately
equivalent to the stricter of the two due to high correlation).

**No lookahead.**

### Entry feature 6 — Volume percentile by UTC hour (timing / participation)

**Inputs:** 30m klines `volume`, plus the 30m bar's UTC hour (= 0..23).

**Computation:**

1. For each UTC hour `h ∈ {0, 1, ..., 23}`, maintain a trailing
   distribution of 30m breakout-bar volumes that fall within UTC hour
   `h` over trailing `L_session = 60` days.
2. At `T_30m_close` with UTC hour `h*`, compute the percentile rank
   of `volume(T_30m_close)` within the hour-`h*` trailing distribution.
3. **Filter passes** if the percentile rank ≥ `Q_session = 50` (Phase
   4g §29 fixed at session-median).

**No lookahead.** Trailing 60-day distribution per UTC hour uses only
prior bars in that hour.

### Entry feature 7 — Taker buy/sell imbalance

**Inputs:** 30m klines `taker_buy_volume` and `volume`.

**Computation:**

1. `taker_buy_fraction(T) = taker_buy_volume(T) / volume(T)`.
2. For long V2 entries: filter passes if `taker_buy_fraction >=
   T_imb_min`, where `T_imb_min ∈ {0.55, 0.60}` per Phase 4g §29 axis
   5.
3. For short V2 entries: filter passes if `(1 - taker_buy_fraction) >=
   T_imb_min` (mirror; sell-imbalance toward the short direction).

**No metrics ratio column read.** Per Phase 4j §11.3 / §14, the
metrics `sum_taker_long_short_vol_ratio` MUST NOT be accessed. The
kline `taker_buy_volume` is the sole input for this feature. This
isolates the Phase 4i metrics NaN concentration in optional ratio
columns from V2's first backtest.

**No lookahead.**

### Entry feature 8 — OI delta direction + funding-rate percentile band

**Inputs:** Phase 4i metrics OI subset (under Phase 4j §11) + v002
funding manifests.

#### Sub-component (a) — OI delta direction

**Per-bar exclusion test** (Phase 4j §11.4 — see §"Metrics OI per-bar
exclusion implementation plan" below).

**OI delta computation** (Phase 4j §17 / §11.4 binding):

1. For an OI-feature-eligible 30m signal bar at `T_30m_open` (=
   `T_30m_close + 1ms - 30 × 60 × 1000`):
   - `oi_at_bar_close = sum_open_interest(create_time = T_30m_open
     + 25 × 60 × 1000)` (last 5-minute record in current 30m window).
   - `oi_at_prev_window_close = sum_open_interest(create_time =
     T_30m_open - 5 × 60 × 1000)` (last 5-minute record in PREVIOUS
     30m window).
   - `oi_delta = oi_at_bar_close - oi_at_prev_window_close`.
2. **Long-direction filter:**
   - Under `OI_dir = aligned`: filter passes if `oi_delta > 0`.
   - Under `OI_dir = non_negative`: filter passes if `oi_delta >= 0`.
3. **Short-direction filter:** mirror (`oi_delta < 0` or `oi_delta <=
   0`).
4. **N_oi grid:** `N_oi = 240` 30m bars (Phase 4g §29 fixed) — note
   that the Phase 4j §17 OI-delta computation rule supersedes the
   Phase 4g §17 N_oi-trailing rule for V2's first backtest (the
   Phase 4j rule is more conservative: it uses two specific
   point-in-time-clear records rather than a trailing average over
   N_oi bars). The future V2 backtest MUST use the Phase 4j §17 rule
   verbatim. The Phase 4g §17 N_oi parameter survives in the spec
   but is NOT a free axis in the threshold grid; it is recorded as
   `N_oi = 240` and reported in the brief as a fixed parameter that
   is NOT exercised by the Phase 4j §17 OI-delta computation.

#### Sub-component (b) — Funding-rate percentile band

**Inputs:** v002 funding manifests
(`binance_usdm_<symbol>_funding__v002`).

**Computation:**

1. At V2 candidate signal time `T_30m_close`, identify the most recent
   completed funding event with `funding_time <= T_30m_close` for
   the symbol.
2. Form the trailing distribution of funding rates over the prior
   `L_fund = 90` funding events (~30 days at 8h cadence; Phase 4g §29
   fixed).
3. Compute the percentile rank of the most recent funding rate within
   the trailing distribution.
4. **Filter passes** if the percentile rank is in
   `[P_fund_low, P_fund_high]`, where `(P_fund_low, P_fund_high) ∈
   {(20, 80), (30, 70)}` per Phase 4g §29 axis 7.

**No lookahead.** Future funding rates are never used.

#### Combined entry feature 8

V2 entry feature 8 passes if BOTH sub-component (a) AND sub-component
(b) pass.

### Exit / regime feature 1 — Time-since-entry counter

**Computation:** at every 30m bar after entry, increment a counter
of completed 30m bars since entry. At counter = `T_stop` (where
`T_stop ∈ {12, 16}` per Phase 4g §29 axis 9), exit the position at
the next 30m bar's open at market.

**Stop-precedence (Phase 4g §20):**

1. If protective stop triggers first → exit at stop.
2. Else if take-profit triggers first → exit at take-profit.
3. Else if time-stop horizon elapses → exit at next 30m open at
   market.

### Exit / regime feature 2 — ATR percentile regime

**Computation:** ATR(20) on 30m, with trailing percentile over
`L_atr = 240` 30m bars (Phase 4g §29 fixed).

**Recorded but NOT acted on as exit.** Used post-trade to classify
trade regime. Per Phase 4g §28, this is `metric_only` for exit
purposes. (Note: the same `L_atr` is also part of the entry condition
3 ATR-percentile-band check at the entry-condition stage; this exit
feature is the post-entry tracking of the same percentile.)

### Exit / regime feature 3 — HTF bias state continuity

**Computation:** at each completed 30m bar after entry, re-evaluate
the HTF bias state per Entry feature 1.

**Recorded but NOT acted on as exit.** A HTF bias flip during an open
position does NOT trigger an exit in V2's first spec; it is recorded
in the trade record for post-trade regime classification. Per Phase
4g §28, this is observed-only.

---

## Metrics OI per-bar exclusion implementation plan

The future Phase 4l execution phase MUST implement the Phase 4j §11.4
binding per-bar exclusion test exactly as predeclared by Phase 4j
§16 (pseudocode). Phase 4k restates and operationalizes it here:

### Per-bar exclusion algorithm (binding)

```python
# Predeclared by Phase 4k for Phase 4l execution.
# Phase 4l implementation MUST match this algorithm exactly.
# Deviations MUST abort the backtest.

def is_30m_bar_oi_feature_eligible(
    symbol: str,                  # "BTCUSDT" or "ETHUSDT"
    bar_open_time_ms: int,        # 30m bar's open_time in UTC ms
    metrics_records: dict[int, MetricsRecord],
        # keyed by create_time UTC ms, for the symbol, OI-subset only
) -> bool:
    expected_records_ms = [
        bar_open_time_ms + 0,
        bar_open_time_ms + 5 * 60 * 1000,
        bar_open_time_ms + 10 * 60 * 1000,
        bar_open_time_ms + 15 * 60 * 1000,
        bar_open_time_ms + 20 * 60 * 1000,
        bar_open_time_ms + 25 * 60 * 1000,
    ]
    for ts_ms in expected_records_ms:
        if ts_ms not in metrics_records:
            return False
        rec = metrics_records[ts_ms]
        if rec.symbol != symbol:
            return False
        # NaN detection via self-inequality (IEEE-754 standard)
        if rec.sum_open_interest != rec.sum_open_interest:
            return False
        if rec.sum_open_interest_value != rec.sum_open_interest_value:
            return False
    return True
```

### OI-delta record-pair lookup

For OI-feature-eligible bars, the Phase 4j §17 OI-delta computation
also requires the metrics record at `bar_open_time_ms - 5 × 60 ×
1000` (last 5-minute record in the previous 30m window). The future
Phase 4l execution phase MUST verify that this record is present
AND has non-NaN OI columns BEFORE computing OI delta. If absent,
the bar is excluded with reason `metrics_oi_prev_window_missing` (a
sub-classification of `metrics_oi_missing_or_invalid`).

### Excluded-bar logging

Every excluded 30m signal bar MUST be logged with the following
fields (Phase 4j §11.6 binding):

| Column | Type | Source |
|---|---|---|
| `symbol` | str | "BTCUSDT" or "ETHUSDT" |
| `bar_open_time_ms` | int64 | 30m bar's open_time |
| `date_utc` | str (YYYY-MM-DD) | derived from `bar_open_time_ms` |
| `exclusion_reason` | str | `metrics_oi_missing_or_invalid` or `metrics_oi_prev_window_missing` |
| `bars_excluded_per_day` | int | rolling count |
| `bars_excluded_cumulative` | int | running total |

### Sensitivity analysis (Phase 4j §11.7 binding)

Phase 4l execution MUST emit two cells:

- **Main cell:** OI-feature-eligible bars only (per the per-bar
  algorithm above).
- **Sensitivity cell — "exclude entire affected days":** ALSO excludes
  any 30m bar whose date contains ANY metrics `invalid_window` from
  the Phase 4i manifests (regardless of whether the bar's specific
  30m window is OI-feature-eligible).

The Phase 4l report MUST include comparison of:

- per-variant trade counts;
- per-variant win rate;
- per-variant mean R / median R / total R;
- per-variant max drawdown in R;
- per-variant profit factor;
- per-variant expectancy after §11.6 HIGH cost.

If main-cell vs. sensitivity-cell statistics diverge by more than
the predeclared threshold (see §"Catastrophic-floor predicates"),
the backtest MUST report the divergence and stop for operator review
before claiming results.

### Predeclared exclusion-rate range

Per Phase 4j §15 empirical scope estimate: BTC ~1.3% maximum bar
exclusion (5 699 missing 5-minute records / 6 records per 30m window
≈ 950 affected 30m bars worst-case at 74 448 30m bars total).

If the Phase 4l execution phase observes exclusion rate substantively
above this estimate (predeclared threshold: ≥ 5%), the Phase 4l
report MUST flag the exclusion-rate anomaly and the operator MUST
review before V2 backtest results are claimed valid. This is a
predeclared operator review trigger, not a strategy outcome.

---

## Optional ratio-column prohibition

Per Phase 4j §11.3 / §14 binding: the future V2 backtest **MUST NOT**
read the four optional metrics ratio columns —

- `count_toptrader_long_short_ratio`;
- `sum_toptrader_long_short_ratio`;
- `count_long_short_ratio`;
- `sum_taker_long_short_vol_ratio` —

for ANY purpose: filter, label, diagnostic, sensitivity, or feature.

### Implementation enforcement

The Phase 4l execution phase MUST enforce this prohibition AT THE CODE
LEVEL via:

1. A metrics-loader pydantic schema that exposes ONLY the OI subset
   (`create_time`, `symbol`, `sum_open_interest`,
   `sum_open_interest_value`).
2. Defensive runtime assertions that fail closed if any code path
   attempts to read a ratio column from a metrics Parquet file.
3. A CI / static-analysis check that scans the Phase 4l backtest code
   for any reference to the four ratio column names; if found, the
   build MUST fail.

### Verification by Phase 4l report

The Phase 4l report MUST include an explicit "Optional ratio-column
non-access verification" section confirming:

- code review findings (no string match for any of the four column
  names);
- runtime introspection of metrics-loader schema (only OI subset
  columns exposed);
- output of the static-analysis scan.

If the verification cannot confirm zero ratio-column access, the
backtest MUST abort and stop for operator review. The Phase 4l report
in this case is a failure report, NOT a partial-result report.

---

## Signal generation plan

Per Phase 4g §13 truth table (preserved verbatim):

### Long V2 candidate setup logical structure

A long V2 candidate setup forms at completed 30m breakout bar
`T_30m_close` if **all** of the following hold:

1. **Bar OI-feature-eligible** (Phase 4j §11 per-bar exclusion test
   passes).
2. **No active cooldown** (per Phase 4g §22; cooldown horizon `C =
   8` 30m bars per Phase 4g §29 fixed).
3. **HTF trend bias state is bullish** (Entry feature 1 long).
4. **Donchian breakout state is upward** (Entry feature 2 long).
5. **Donchian width compression** (Entry feature 3 ≤ `P_w max`).
6. **Volatility regime band** (Entry feature 3 ATR percentile band
   pass; Phase 4g §16 sub-component (b) at fixed `[25, 75]`).
7. **Range expansion** (Entry feature 4 ≥ 1.0).
8. **Participation passes** (Entry feature 5 + 6 + 7 all long-side).
9. **Derivatives-flow context passes** (Entry feature 8 long-side
   sub-component (a) AND sub-component (b)).
10. **No governance-label failure** (`stop_trigger_domain =
    trade_price_backtest`, `break_even_rule = disabled`,
    `ema_slope_method = discrete_comparison`,
    `stagnation_window_role = metric_only`; `mixed_or_unknown`
    invalid; fail-closed).
11. **No active V2 position on the symbol** (one-position-max per
    §1.7.3).

### Short V2 candidate setup logical structure

Strict mirror image with bearish HTF state, downward Donchian
breakout, mirrored participation and derivatives gates.

### Forbidden signal additions

The future V2 backtest MUST NOT include:

- **Mean-reversion overlay.** F1's mechanism is not re-introduced.
- **D1-A / F1 / R2 / R3 region re-entry.** V2 candidates that converge
  to retained-evidence parameter regions are flagged and terminated.
- **Discretionary overrides.** No human-in-the-loop signal
  modifications.
- **Post-hoc rescue variants.** No variants added after observing
  outcomes.
- **5m signal triggers.** 5m is diagnostic-only per Phase 3t §14.2.
- **UTC-hour exclusion zones** (e.g., "do not enter during 02:00–06:00
  UTC"). Such zones would be parameter choices vulnerable to
  in-sample optimization. The hour-bucket participation percentile
  (Entry feature 6) is the supported hour-aware feature.
- **Funding-window-based entry suppression.** D1-A's framing is NOT
  replicated.
- **Multi-asset / cross-sectional optimization.** v1 is BTCUSDT only.
- **Hedge mode.** Forbidden by §1.7.3.
- **Any feature not in the Phase 4g §28 active feature set.**

### Decision-time alignment

V2 signals are evaluated at completed-30m-bar-close time only:
`T_30m_close = T_30m_open + 30 × 60 × 1000 - 1` ms. No partial bar
evaluation. Consistent with Phase 4i klines manifest
`quality_checks.close_time_consistency_violations == 0`.

---

## Entry model implementation plan

Per Phase 4g §13 / §25 (preserved verbatim):

### Entry execution

For each V2 candidate setup that passes signal generation at
`T_30m_close`:

1. The entry order is a **MARKET order at the next 30m bar's open**,
   `T_30m_close + 1ms`.
2. The fill price is assumed to be the next 30m bar's open price
   (= `open(T_30m_close + 1ms)`).
3. **No intrabar entries.** No partial fills. No limit-resting entries.
4. The entry is executed only if no V2 position is currently open on
   the symbol (one-position max per §1.7.3) AND the cooldown has
   elapsed.
5. **Fees:** entry fee = 0.04% per side default for USDⓈ-M futures
   (≈ 4 bps per side; Phase 4g §26).
6. **Slippage:** per the Phase 4g §26 cost model (LOW / MEDIUM / HIGH
   cells; HIGH = 8 bps per side per Phase 2f §11.6).

### Position sizing

Per Phase 4g §25 (preserved verbatim from V1):

```text
position_size_qty = floor((equity × 0.0025) / stop_distance)

subject to:
  position_size_qty × entry_price ≤ effective_leverage_cap × equity
  position_size_qty × entry_price ≤ internal_notional_cap
  position_size_qty ≥ exchange_min_quantity (else trade rejected)
  position_size_qty rounded down to lot-size increment
```

Locked constants (per §1.7.3 binding):

- `risk_fraction = 0.0025` (0.25%).
- `effective_leverage_cap = 2.0`.
- `internal_notional_cap` = research-mode default per backtest brief
  (NOT a runtime live cap; the backtest is research-only).

### Cooldown logic

After exit, V2 enforces a cooldown of `C = 8` 30m bars (= 4 hours)
before the next entry on the same symbol (per Phase 4g §29 fixed
cooldown).

**Same-direction cooldown only.** A long-exit triggers a long-side
cooldown, not a short-side cooldown. A short-exit triggers a
short-side cooldown.

**Reason:** the cooldown prevents same-direction re-entry from
re-opening a just-closed position; opposite-direction reversal during
an open position is forbidden separately by §1.7.3 (no reversal while
positioned).

---

## Exit model implementation plan

Per Phase 4g §18 / §19 / §20 / §21 (preserved verbatim):

### Initial structural stop with ATR buffer

**Long initial stop:**

```text
initial_stop = min(setup_low, breakout_bar_low) − 0.10 × ATR(20)
```

where `setup_low = lowest low of the previous N1 30m bars` (the
Donchian lookback used for the breakout).

**Short initial stop:** mirror.

**Stop-distance filter:** trade is rejected if:

- `stop_distance < 0.60 × ATR(20)`, OR
- `stop_distance > 1.80 × ATR(20)`.

Bounds preserved verbatim from V1; Phase 4g §29 locked.

**R definition:**

```text
R = |entry_price − initial_stop|
```

### Stop trigger domain

Per Phase 4g §24 + Phase 3v §8 binding:

- **Research / backtest:** `trade_price_backtest`. The Phase 4l
  execution phase MUST tag every V2 trade record with
  `stop_trigger_domain = trade_price_backtest`.
- **Future runtime / paper / live (NOT authorized by Phase 4k or
  Phase 4l):** `mark_price_runtime`.
- **Future live-readiness validation step (NOT authorized):**
  `mark_price_backtest_candidate`.
- **`mixed_or_unknown` is invalid and fails closed at any decision
  boundary.**

### Fixed-R take-profit

Per Phase 4g §20 (preserved verbatim):

- For long: `take_profit = entry + N_R × R`.
- For short: `take_profit = entry − N_R × R`.
- `N_R ∈ {2.0, 2.5}` per Phase 4g §29 axis 8.

### Unconditional time-stop

Per Phase 4g §20 (preserved verbatim):

- Time-stop horizon `T_stop ∈ {12, 16}` 30m bars (= 6h, 8h) per Phase
  4g §29 axis 9.
- After `T_stop` 30m bars elapsed since entry, the position exits at
  next 30m bar's open at market regardless of MFE / MAE.

### Stop-precedence

Per Phase 4g §20 (preserved verbatim):

1. If protective stop triggers first → exit at stop.
2. Else if take-profit triggers first → exit at take-profit.
3. Else if time-stop horizon elapses → exit at next 30m open at
   market.

### No break-even rule

Per Phase 4g §21 (preserved verbatim): `break_even_rule = disabled`
for V2's first spec.

### No trailing stop

Per Phase 4g §18 (preserved verbatim): no trailing exit in V2's
first spec.

### No volatility-regime-degradation early exit

Per Phase 4g §18 (preserved verbatim): `stagnation_window_role =
metric_only`; ATR percentile is observed but NOT acted on.

### No discretionary exit

Per Phase 4g §18 / §20 (preserved verbatim): no human-in-the-loop
exit modifications.

### Same-bar exit ambiguity tie-breakers

If a single 30m bar's high/low/close range admits BOTH stop and
take-profit, the future V2 backtest MUST resolve as follows:

- **Conservative tie-break:** stop wins. Justification: the actual
  realized intra-bar path is unknown; assuming stop-first is
  conservative (loss-realizing) and matches V1 / R3 backtest
  conventions.
- This tie-break MUST be predeclared in the Phase 4l brief and applied
  consistently. No alternative tie-break may be chosen post-hoc.

---

## Cost and slippage model

Per Phase 4g §26 + Phase 2f §11.6 (preserved verbatim):

### Cost cells

| Cell | Slippage per side | Round-trip cost (fees + slippage) | Phase 4l report |
|---|---|---|---|
| LOW-slip | 1 bp | 4 + 4 + 1 + 1 = 10 bps | sensitivity cell |
| MEDIUM-slip | 4 bps | 4 + 4 + 4 + 4 = 16 bps | standard reporting cell |
| HIGH-slip | 8 bps | 4 + 4 + 8 + 8 = 24 bps | promotion-gate cell (§11.6) |

The fee rate is taker = 0.04% per side default for USDⓈ-M futures
(≈ 4 bps per side per Phase 4g §26).

### §11.6 cost-sensitivity gate (binding)

- **§11.6 = 8 bps HIGH per side preserved verbatim.**
- V2 candidates that fail the §11.6 HIGH cost-sensitivity gate on
  EITHER BTCUSDT OR ETHUSDT MUST FAIL framework promotion (per R2's
  failure pattern; Phase 2w §16.1).
- §11.6 is non-negotiable in Phase 4k. Any §11.6 amendment requires
  a separately authorized governance memo.

### Funding cost

- Funding cost MUST be included in P&L per
  `docs/04-data/data-requirements.md` funding-history requirement.
- Funding accrual occurs at funding events (8h cadence on BTCUSDT
  USDⓈ-M).
- For each open V2 position spanning a funding event, the position
  is debited / credited per the published funding rate × position
  notional × funding-fraction.
- Funding cost is recorded per-trade and reported in aggregate.

### No maker-rebate assumption

Per Phase 4g §26: V2 entry orders are MARKET orders, paying taker
fees. No maker rebate is assumed.

### No live fee assumption

V2's first backtest is research-only. No live fee waivers, VIP
discounts, BNB-payment discounts, or partner-rebate assumptions
modify the standard taker fee.

### No cost-model relaxation

Phase 4l MUST NOT relax the §11.6 HIGH gate, change the cost cells,
or apply a "favorable" fee assumption.

---

## Position sizing and exposure assumptions

Per Phase 4g §25 + §1.7.3 (preserved verbatim):

| Constraint | Locked value |
|---|---|
| Initial live risk per trade | 0.25% of sizing equity |
| Effective leverage cap | 2× |
| Internal notional cap | mandatory for live; research-mode default per Phase 4l brief |
| Max concurrent positions | 1 |
| Symbol scope | BTCUSDT only for live; ETHUSDT research / comparison only |
| Pyramiding | forbidden |
| Reversal while positioned | forbidden |
| Stop-distance filter | 0.60 × ATR(20) ≤ stop distance ≤ 1.80 × ATR(20) |

For Phase 4l backtest:

- Position sizing uses 0.25% risk on a per-trade basis.
- 2× effective leverage cap enforced.
- Per-trade R is the unit of account in the V2 backtest report.
- Aggregate cumulative R per variant is reported as `total_R`.
- Drawdown is reported in R units (peak-to-trough cumulative R
  decline).

---

## Threshold-grid handling

### Phase 4g §29 grid is binding

Phase 4l MUST NOT extend, restrict, modify, or reorder the Phase 4g
§29 512-variant grid. Each variant is fully specified by the 9
non-fixed axes (per §"V2 hypothesis and locked strategy spec recap"
above).

### Search-space size

512 variants is at the upper bound of what PBO / deflated Sharpe
machinery handles cleanly per Phase 4g §29.

Phase 4g §29 offered the future Phase 4l execution phase two options:

- **Option A — reduce search space at brief time** (e.g., tie
  `V_z_min` to `V_rel_min` via `V_z_min = (V_rel_min − 1) / σ_v` and
  drop `V_z_min` from a free axis, bringing 512 → 256).
- **Option B — apply full PBO / deflated Sharpe / CSCV with 512
  variants fully reported.**

### Phase 4k recommendation: Option B (no further reduction)

**Phase 4k recommends Option B.** The rationale:

1. **Predeclaration purity.** Reducing the grid in Phase 4l after
   Phase 4g committed it would be a post-hoc reduction not approved
   ex ante. Honoring Phase 4g §29's 512-variant grid verbatim
   preserves the predeclaration discipline.
2. **CSCV machinery is well-tractable at 512.** Bailey / Borwein /
   López de Prado / Zhu (2014) deflated-Sharpe correction handles
   N variants with cost ~log(N); CSCV with N split into S
   sub-samples handles N at S × N work. Both are well within
   Python-runtime feasibility for V2's expected per-variant trade
   count (~hundreds to low-thousands at the OOS holdout window).
3. **The reduction in Option A — tying V_z_min to V_rel_min — would
   conflate two participation features.** They are correlated but not
   functionally identical (V_rel is multiplicative; V_z is z-score
   normalized to volatility). Conflating them removes a degree of
   research freedom that Phase 4g committed.
4. **Reporting 512 variants is feasible.** The Phase 4l report MUST
   include a per-variant table of M1 / M2 / M3 / cost-cell results;
   512 rows per symbol per cost cell is roughly 3072 cells, which is
   readable in CSV / Parquet form even if not directly inline in the
   report Markdown.

### Phase 4l brief commitment

The future Phase 4l execution-phase brief MUST commit to Option B
explicitly: 512 variants, deflated-Sharpe correction, CSCV with at
least 16 chronologically-respecting sub-samples (the standard CSCV
S = 16 per Bailey et al.), and PBO reported.

If a future operator decides instead to reduce the search space (e.g.,
to match limited compute budget), the operator MUST authorize a
separate predeclaration memo *before* the Phase 4l execution phase
runs. Phase 4k does NOT itself reduce the grid.

### Outcome-driven threshold selection forbidden

No threshold may be selected from backtest outcomes. The Phase 4l
execution phase reports per-variant outcomes; the choice of "best"
variant must be subject to deflated Sharpe / PBO correction per
Bailey et al., NOT raw in-sample Sharpe.

The Phase 4l report MUST identify:

- the variant with highest in-sample Sharpe on the train window;
- the variant with highest deflated Sharpe on the train window;
- the variants surviving deflated-Sharpe-correction at predeclared
  thresholds;
- their performance on the validation window;
- their performance on the OOS holdout window;
- the train → validation → OOS performance decay (a measure of
  in-sample fitting).

---

## Search-space control

### Single-grid commitment

Phase 4l MUST commit to the Phase 4g §29 512-variant grid. No
on-the-fly grid extension. No "small additional variants" beyond
512. No "warm-up" smaller grid that becomes the published grid.

### No variant-by-variant operator approval

Phase 4l does NOT request per-variant operator authorization. The
512-variant grid is a single commitment. The Phase 4l execution
proceeds across all 512 variants in one run.

### Variant ordering

Phase 4l MUST process variants in a deterministic order
(lexicographic by axis name then axis value) so that any partial-run
re-execution produces identical intermediate state. This is
reproducibility discipline, not statistical methodology.

### No exit early on bad variants

If a variant produces a negative-expectancy backtest on the train
window, Phase 4l MUST NOT exit early or skip its reporting. All 512
variants MUST be reported, including failures, to support PBO /
deflated-Sharpe computation.

---

## PBO / deflated Sharpe / CSCV plan

Per Phase 4g §31 / §34 (preserved verbatim) and Bailey / Borwein /
López de Prado / Zhu (2014):

### Deflated Sharpe correction

For each of the 512 variants, compute the deflated Sharpe ratio
(DSR) per Bailey & López de Prado (2014):

```text
DSR(v) = (SR(v) − E[max(SR_random)]) / sqrt((1 − γ_3·SR(v) + (γ_4 − 1)/4·SR(v)²) / (T − 1))
```

where:

- `SR(v)` is the Sharpe ratio of variant `v` on the train window;
- `E[max(SR_random)]` is the expected maximum of N = 512
  i.i.d. standard-normal Sharpe ratios under the null;
- `γ_3` is the per-trade-return skewness;
- `γ_4` is the per-trade-return kurtosis;
- `T` is the trade count on the train window.

A variant is deflated-Sharpe-significant if DSR > 1.96 (5%
two-sided).

### Probability of Backtest Overfitting (PBO)

Per Bailey / Borwein / López de Prado / Zhu (2014):

1. Split the train window into S = 16 chronologically-respecting
   sub-samples.
2. For each combination of S/2 = 8 chosen sub-samples (J = (16
   choose 8) = 12 870 combinations):
   - Form the in-sample subset (= 8 sub-samples joined).
   - Form the out-of-sample subset (= the other 8 sub-samples
     joined).
   - Identify the variant maximizing in-sample Sharpe.
   - Compute that variant's out-of-sample Sharpe rank within the
     N = 512 variants.
3. PBO = fraction of (in-sample, out-of-sample) splits where the
   in-sample-best variant ranks below median on out-of-sample.

A PBO > 0.5 is a strong signal of overfitting (i.e., the
in-sample-best variant systematically underperforms out-of-sample).

### CSCV sub-sample structure

Per Bailey et al.:

- S = 16 sub-samples.
- Sub-samples MUST be chronologically respecting (no random
  shuffle; no time-leakage).
- The 12 870 combinations per CSCV are well-tractable in Python
  with numpy-vectorized rank computation.

### Reporting

The Phase 4l report MUST include:

| Metric | Required form |
|---|---|
| Per-variant in-sample Sharpe (train window) | full 512-row table per symbol |
| Per-variant deflated Sharpe (train window) | full 512-row table per symbol |
| Variants surviving DSR > 1.96 (train window) | summary table + count |
| Per-variant out-of-sample Sharpe (validation window) | full 512-row table per symbol |
| Per-variant out-of-sample Sharpe (OOS holdout window) | full 512-row table per symbol |
| In-sample-to-OOS Sharpe decay | summary statistics (mean, median, distribution plot) |
| PBO (train → validation) | scalar with confidence interval |
| PBO (train → OOS holdout) | scalar with confidence interval |
| CSCV S = 16 sub-sample sharpe rankings | full table per symbol |

### Minimum trade count requirement

- DSR computation requires `T >= 30` per-variant trade count on the
  train window (statistical-power floor).
- If a variant has < 30 train-window trades, it is reported as
  "trade-count-insufficient" and excluded from DSR / PBO computation.
- Persistent low trade counts (e.g., > 50% of variants insufficient)
  are themselves a catastrophic-floor predicate (see below).

---

## Chronological validation plan

### Date-window split (predeclared)

Phase 4k commits the following exact UTC date-window split BEFORE
any V2 backtest is run:

| Window | Start (UTC) | End (UTC) | Duration |
|---|---|---|---|
| **Training / model-selection** | 2022-01-01 00:00:00 | 2023-06-30 23:30:00 | ~18 months |
| **Validation / selection-confirmation** | 2023-07-01 00:00:00 | 2024-06-30 23:30:00 | ~12 months |
| **Out-of-sample holdout** | 2024-07-01 00:00:00 | 2026-03-31 23:30:00 | ~21 months |

Justifications:

- Total coverage 2022-01-01 .. 2026-03-31 = ~51 months (matches Phase
  4i acquired range).
- 18-month training window provides sufficient regime diversity
  (2022 bear; early 2023 chop) to avoid single-regime-only fit.
- 12-month validation window separates train-selected variants from
  the OOS holdout to avoid double-dipping.
- 21-month OOS holdout is the primary out-of-sample evidence cell,
  containing the longest unseen period. Larger than the validation
  window deliberately — more OOS data is better for OOS judgment.
- Train + validation + OOS = 51 months exact.
- All boundaries are at 30m-bar boundaries.

### No data shuffle

Per Phase 4g §31 (preserved verbatim): no random shuffling of bars.
Chronological order is preserved.

### No leakage

The Phase 4l execution phase MUST verify zero leakage:

- All feature computations use only prior-bar data.
- The CSCV sub-samples are chronologically respecting.
- The validation window is NOT used for variant selection.
- The OOS holdout window is NOT used for variant selection AND NOT
  used for validation-window Sharpe ranking.

### Walk-forward extension (optional secondary)

The Phase 4g §31 specification permits walk-forward / multi-window
OOS splits if feasible. Phase 4k recommends, but does NOT require,
a secondary walk-forward analysis with 4 rolling 12-month OOS
windows over the 2024-07..2026-03 period (4 chronologically-respecting
12-month windows starting at 2024-07, 2024-10, 2025-01, 2025-04 —
overlapping). This is a robustness check, not the primary OOS
evidence.

If walk-forward is omitted, the Phase 4l report MUST justify the
omission and the operator MUST review.

---

## Train / validation / holdout windows

Per the previous section. Restated for explicit binding:

### Train window: 2022-01-01 00:00:00 UTC → 2023-06-30 23:30:00 UTC

Used for:

- per-variant Sharpe computation;
- deflated Sharpe correction;
- CSCV S = 16 sub-sample formation;
- variant selection ("best" variant identification).

### Validation window: 2023-07-01 00:00:00 UTC → 2024-06-30 23:30:00 UTC

Used for:

- selection-confirmation: train-selected variants MUST preserve their
  relative Sharpe ranking.
- variant survival check: variants failing on validation cannot
  proceed to OOS holdout claims.
- NOT used for variant re-selection.

### Out-of-sample holdout window: 2024-07-01 00:00:00 UTC → 2026-03-31 23:30:00 UTC

Used for:

- primary out-of-sample evidence;
- M1 / M2 / M3 mechanism-check evaluation on OOS data;
- catastrophic-floor predicate evaluation;
- promotion / failure / partial-pass verdict.

The OOS holdout window is **the primary V2 evidence cell**. V2
results on the train window are reported but do not constitute
promotion evidence. V2 results on the validation window are reported
as variant-selection-confirmation.

### No window modification post-hoc

If the future Phase 4l execution phase observes that the predeclared
windows produce too few trades (catastrophic-floor predicate trigger),
the appropriate response is **predicate-failure stop**, NOT window
expansion. Window expansion after observing trade count would be
post-hoc data selection (Bailey et al. 2014). The Phase 4l brief
MUST predeclare the window split exactly as above.

---

## BTCUSDT primary and ETHUSDT comparison protocol

Per Phase 4g §10 + §31 (preserved verbatim):

### BTCUSDT is primary

V2's primary evidence is BTCUSDT. ETHUSDT is comparison-only.

### ETHUSDT cannot rescue BTCUSDT failure

Per Phase 4g §31: cross-symbol consistency is required. If BTCUSDT
fails any catastrophic-floor predicate on the OOS holdout window,
V2 fails framework promotion regardless of ETHUSDT outcome. ETHUSDT
results may **support robustness** but NOT **rescue** a BTC failure.

### ETHUSDT may support robustness if directionally consistent

If BTCUSDT and ETHUSDT both pass M1 / M2 / M3 mechanism checks AND
both pass §11.6 HIGH cost on the OOS holdout window, the cross-symbol
robustness is reported as **directionally consistent**.

If BTCUSDT passes but ETHUSDT fails, the robustness is **BTC-only**;
the V2 report MUST flag this as reduced cross-symbol confidence.

### No multi-asset portfolio

V2 is BTCUSDT only for live (per §1.7.3). ETHUSDT is not a portfolio
component.

### No cross-symbol optimization

The Phase 4l execution phase MUST NOT:

- choose different variants per symbol after observing outcomes;
- select the "best of BTC OR ETH" variant;
- cherry-pick cross-symbol-consistent variants from in-sample data;
- apply any cross-symbol weighting that depends on observed outcomes.

The same 512 variants are evaluated independently per symbol. The
Phase 4l report MUST present BTC and ETH per-variant outcomes
side-by-side for transparency, NOT as a basis for cross-symbol
selection.

### BTCUSDT-only variant winner

If a future operator wishes to declare a "winning" V2 variant for
implementation consideration, the variant MUST be selected on BTCUSDT
out-of-sample data alone, with ETHUSDT used for cross-symbol
robustness check only.

The Phase 4l report MUST report:

- BTCUSDT-train-best variant;
- BTCUSDT-validation-confirming variant;
- BTCUSDT-OOS-passing variant;
- ETHUSDT cross-symbol consistency for the BTCUSDT-OOS-passing
  variant (whether it also passes ETH OOS, with what magnitude
  difference).

---

## M1 / M2 / M3 mechanism-check implementation plan

Per Phase 4g §30 (preserved verbatim):

### M1 — Price-structure mechanism

**Question:** under V2's locked entry conditions, do at least half of
the resulting trades reach +0.5R MFE before stop on each of BTCUSDT
and ETHUSDT?

**Computation:**

For each (variant, symbol, cost-cell, window) tuple:

1. For each closed V2 trade in the trade population:
   - Track the maximum favorable excursion (MFE) in R units between
     entry and exit.
   - `mfe_max_R = max((max(high) − entry) / R)` for long;
     `(entry − min(low)) / R` for short. (Computed bar-by-bar across
     the trade lifetime, excluding entry bar's inside-bar fluctuation
     ambiguity per V1 / R3 conventions.)
2. Compute `frac_reached_0_5R = count(mfe_max_R >= 0.5) / total_trade_count`.

**Pass criterion:** `frac_reached_0_5R >= 0.50` on BOTH BTCUSDT and
ETHUSDT, on the OOS holdout window, MEDIUM-slip cell.

**Fail criterion:** `frac_reached_0_5R < 0.50` on either symbol on
the OOS holdout window.

**Interpretation:**

- M1 PASS: directional-trend-continuation mechanism is at least
  minimally present.
- M1 FAIL: trades stop before any meaningful follow-through;
  breakout-from-compression setup is not capturing trend continuation
  at all. M1 FAIL is sufficient for V2 framework rejection
  (analogous to F1's HARD REJECT under Phase 3c §7.3
  catastrophic-floor).

### M2 — Participation mechanism

**Question:** does V2's participation-confirmation layer add at least
+0.10R per-trade expectancy versus a price-only V2 skeleton on each
of BTCUSDT and ETHUSDT?

**Computation:**

For each (variant, symbol, cost-cell, window) tuple:

1. Compute the **full V2 trade population** (all entry conditions
   active).
2. Compute the **participation-relaxed degenerate variant**:
   - Set `V_rel_min = 0.0`.
   - Set `V_z_min = -∞` (effectively `-100`).
   - Set `Q_session = 0` (UTC-hour percentile passes for any volume).
   - Set `T_imb_min = 0` (taker imbalance gate disabled).
   - All other features unchanged.
3. Compute `mean_R(full_V2)` and `mean_R(participation_relaxed)`.
4. Compute `diff_M2 = mean_R(full_V2) − mean_R(participation_relaxed)`.
5. Compute bootstrap-by-trade 95% confidence interval on `diff_M2`
   (resample with replacement; B = 10 000 bootstrap iterations).

**Pass criterion:** `diff_M2 >= +0.10R` on BOTH BTCUSDT and ETHUSDT
on the OOS holdout window, with bootstrap-CI lower bound > 0 (i.e.,
stat-significant).

**Fail criterion:** `diff_M2 < +0.10R` or bootstrap-CI lower bound
< 0 on either symbol.

**Interpretation:**

- M2 PASS: participation confirmation adds value beyond
  price-structure-only skeleton.
- M2 FAIL: participation gates do not contribute; V2 is functionally
  equivalent to a re-parameterized V1; partial rejection (V2 retained
  as research evidence, non-leading, no successor authorized).

### M3 — Derivatives-context mechanism

**Question:** does V2's derivatives-flow-context layer add at least
+0.05R per-trade expectancy versus a derivatives-relaxed V2 skeleton
AND non-degrade §11.6 HIGH cost-resilience on each of BTCUSDT and
ETHUSDT?

**Computation:**

For each (variant, symbol, cost-cell, window) tuple:

1. Compute the **full V2 trade population** (all entry conditions
   active).
2. Compute the **derivatives-relaxed degenerate variant**:
   - Set `OI_dir = pass-through` (entry feature 8 sub-component (a)
     disabled; OI delta direction does not gate).
   - Set funding band = `[0, 100]` (entry feature 8 sub-component
     (b) disabled; funding rate does not gate).
   - All other features unchanged.
3. Compute `mean_R(full_V2)` and `mean_R(derivatives_relaxed)`.
4. Compute `diff_M3 = mean_R(full_V2) − mean_R(derivatives_relaxed)`.
5. Compute §11.6 HIGH cost-resilience: `mean_R(full_V2 @ HIGH-slip)
   − mean_R(derivatives_relaxed @ HIGH-slip)`. The full V2 must NOT
   degrade (i.e., the difference at HIGH cell ≥ the difference at
   MEDIUM cell − ε; ε = 0.05R for predeclaration).

**Pass criterion:** `diff_M3 >= +0.05R` on BOTH symbols on the OOS
holdout window AND §11.6 HIGH cost-resilience non-degraded on BOTH
symbols.

**Fail criterion:** `diff_M3 < +0.05R` on either symbol OR §11.6
HIGH cost-resilience degraded on either symbol.

**Interpretation:**

- M3 PASS: derivatives-flow gating adds risk-aware value.
- M3 FAIL: derivatives-flow gating is not contributing OR is
  cost-fragile; over-conditioning suspected; partial rejection (V2
  retained as research evidence, non-leading, no successor authorized).

### M1 / M2 / M3 reporting

For each (variant, symbol, cost-cell, window) tuple, the Phase 4l
report MUST include:

- trade count;
- win rate;
- average R;
- median R;
- total R;
- max drawdown in R;
- profit factor;
- expectancy after §11.6 HIGH cost;
- catastrophic-floor status (per §"Catastrophic-floor predicates"
  below);
- M1 / M2 / M3 pass / fail status with magnitude and CI lower bound.

### Mechanism-check independence

M1 / M2 / M3 outcomes are interpreted independently of overall
expectancy. An expectancy-positive variant that fails any of M1 /
M2 / M3 is STILL a partial rejection.

The minimum bar for V2 framework acceptance:

```text
M1 PASS + M2 PASS + M3 PASS + §11.6 HIGH cost-survival + cross-symbol consistency + OOS persistence
```

ALL must be satisfied. Any one failure produces V2 partial rejection
or HARD REJECT depending on the failure pattern (per §"Promotion /
failure / partial-pass criteria" below).

---

## Catastrophic-floor predicates

Per Phase 3c §7.3 / Phase 3h §11.2 / Phase 4g §31 (preserved
verbatim and extended for V2):

The Phase 4l execution phase MUST evaluate the following predeclared
catastrophic-floor predicates on the OOS holdout window. Any
single-predicate failure is sufficient to declare V2 HARD REJECT,
regardless of M1 / M2 / M3 results elsewhere.

### CFP-1 — Insufficient trade count

**Predicate:** per-variant OOS trade count `< 30` on the
BTCUSDT-primary symbol.

**Failure response:** the variant is reported as
"trade-count-insufficient" and excluded from DSR / PBO. If `> 50%`
of variants are trade-count-insufficient, V2 framework HARD REJECT
(insufficient statistical power).

### CFP-2 — Negative OOS expectancy under HIGH cost

**Predicate:** per-variant `mean_R(BTCUSDT, OOS, HIGH-slip) < 0`.

**Failure response:** the variant FAILS framework promotion. If the
BTCUSDT-train-best variant fails CFP-2, V2 framework HARD REJECT
(R2's failure pattern; Phase 2w §16.1).

### CFP-3 — Catastrophic drawdown

**Predicate:** per-variant max drawdown on OOS holdout window in
cumulative R `> 10R` (i.e., a 10R drawdown on a per-trade-R unit).

**Or alternatively:** profit factor `< 0.50` (i.e., aggregate losses
> 2× aggregate wins) on the OOS holdout window.

**Failure response:** any variant satisfying CFP-3 is HARD REJECT
on its own (analogous to F1's catastrophic-floor predicate per Phase
3c §7.3). If any predicate fires on the BTCUSDT-train-best variant,
V2 framework HARD REJECT.

### CFP-4 — BTCUSDT failure with ETHUSDT pass

**Predicate:** BTCUSDT fails any of M1 / M2 / M3 / CFP-2 / CFP-3 on
OOS, but ETHUSDT passes all.

**Failure response:** V2 framework HARD REJECT regardless of ETHUSDT
performance (per Phase 4g §10 / §31; ETH cannot rescue BTC).

### CFP-5 — Train-only performance with OOS failure

**Predicate:** the train-best variant has `train Sharpe > 1.0` AND
`OOS Sharpe < 0.0`.

**Failure response:** V2 framework HARD REJECT (overfitting
predicate fires).

### CFP-6 — Excessive PBO

**Predicate:** PBO (train → OOS) `> 0.5`.

**Failure response:** V2 framework HARD REJECT (Bailey et al. 2014;
PBO > 0.5 indicates overfitting dominates the variant landscape).

### CFP-7 — Overconcentration in one regime / month

**Predicate:** any single calendar month contributes `> 50%` of the
variant's total R on the OOS holdout window.

**Failure response:** V2 framework HARD REJECT for that variant
(ergodicity-failure predicate; the strategy depends on a single
unrepeatable regime period).

### CFP-8 — Sensitivity-cell failure under exclude-entire-affected-days

**Predicate:** the variant's main-cell mean_R on OOS holdout `>= 0`
BUT the sensitivity-cell (exclude-entire-affected-days) mean_R on
OOS holdout `< -0.5 × abs(main-cell mean_R)` (i.e., severely degrades
when the exclusion is widened).

**Failure response:** V2 framework HARD REJECT (the strategy depends
on bars adjacent to metrics-invalid windows in a way that suggests
contamination).

### CFP-9 — Excluded-bar fraction materially changing conclusion

**Predicate:** the predeclared excluded-bar fraction (per Phase 4j
§15 estimate, BTC ~1.3% maximum) substantially exceeds the estimate
(empirical exclusion fraction `> 5%` on OOS holdout).

**Failure response:** Phase 4l report MUST flag for operator review;
the V2 backtest stops for operator review BEFORE claiming results.
This is a methodology trigger, not a strategy outcome.

### CFP-10 — Optional ratio-column access detected

**Predicate:** the Phase 4l execution phase's static-analysis check
or runtime introspection detects ANY access to the four optional
metrics ratio columns.

**Failure response:** Phase 4l execution MUST abort and produce a
failure report. The V2 backtest results are NOT valid. This is a
governance violation, not a strategy outcome.

### CFP-11 — Phase 4j §11 per-bar exclusion deviation

**Predicate:** the Phase 4l implementation of the per-bar exclusion
test does NOT match the Phase 4k / Phase 4j §16 predeclared algorithm
exactly.

**Failure response:** Phase 4l execution MUST abort. Same as CFP-10
— governance violation.

### CFP-12 — Forbidden data access

**Predicate:** the Phase 4l execution phase touches any of the
forbidden inputs (mark-price klines; v002 mark-price; aggTrades;
spot; cross-venue; authenticated REST / private endpoints / public
endpoints in code / user stream / WebSocket / listenKey lifecycle).

**Failure response:** Phase 4l execution MUST abort. Same as CFP-10
/ CFP-11 — safety violation.

---

## Promotion / failure / partial-pass criteria

The Phase 4l execution phase MUST classify the V2 framework as
exactly one of:

### Verdict A — V2 framework PASS (NOT a promotion authorization)

All of the following hold on the BTCUSDT-train-best variant on the
OOS holdout window, MEDIUM-slip cell:

1. Trade count `>= 30` (CFP-1 not triggered).
2. M1 PASS (≥ 50% +0.5R MFE on BOTH symbols).
3. M2 PASS (≥ +0.10R uplift on BOTH symbols, stat-sig).
4. M3 PASS (≥ +0.05R uplift on BOTH symbols, §11.6 HIGH non-degraded).
5. §11.6 HIGH cost-survival on BTCUSDT (`mean_R >= 0` at HIGH-slip).
6. Cross-symbol consistency (ETHUSDT also passes M1 / M2 / M3 + §11.6).
7. OOS persistence (deflated Sharpe > 1.96 on OOS; PBO < 0.5).
8. None of CFP-1 through CFP-9 triggered.
9. CFP-10 / CFP-11 / CFP-12 NOT triggered (no governance / safety
   violation).

**Implication:** V2 framework is research-promotable. **This is NOT
an implementation authorization.** Implementation authorization
requires a separate operator decision after the Phase 4l report.

### Verdict B — V2 framework PARTIAL PASS (research evidence only)

One or more of M2 / M3 / cross-symbol consistency fail, but M1 passes
AND no CFP triggers.

**Implication:** V2 retained as research evidence; non-leading; no
successor authorized.

### Verdict C — V2 framework HARD REJECT

Any of the following:

1. M1 fails on either symbol.
2. CFP-2 (negative OOS expectancy under HIGH cost) on
   BTCUSDT-train-best variant.
3. CFP-3 (catastrophic drawdown) on BTCUSDT-train-best variant.
4. CFP-4 (BTC fails with ETH pass).
5. CFP-5 (train-only performance with OOS failure).
6. CFP-6 (excessive PBO).
7. CFP-7 (overconcentration in one regime / month).
8. CFP-8 (sensitivity-cell failure under exclude-entire-affected-days).
9. CFP-9 (excluded-bar fraction anomaly; flagged for operator review;
   if review confirms anomaly is structural, HARD REJECT).
10. Any of CFP-10 / CFP-11 / CFP-12 (governance / safety violation).

**Implication:** V2 framework HARD REJECT analogous to F1 / D1-A.
Retained as research evidence, non-leading, terminal. No V2-prime,
V2-narrow, V2-relaxed, V2-with-different-features, V2 / V1 hybrid,
V2 / D1-A hybrid, or any other rescue authorized. **No further
operator action required to make HARD REJECT terminal.**

### Verdict D — V2 framework INCOMPLETE (methodology stop)

Any of CFP-9 (excluded-bar anomaly; pending operator review),
CFP-10 (optional ratio-column access), CFP-11 (per-bar deviation),
CFP-12 (forbidden data access), or any other Phase 4j §11 binding-rule
violation.

**Implication:** the Phase 4l execution stops; the V2 backtest results
are NOT valid; the Phase 4l report is a failure report. This is NOT
a strategy verdict; it is a methodology / governance failure.

---

## Required reporting tables

The future Phase 4l execution phase report (a Markdown document under
`docs/00-meta/implementation-reports/`) MUST include the following
tables. None may be omitted.

### Table 1 — Run metadata

| Field | Value |
|---|---|
| Phase | 4l |
| Code commit SHA | (recorded by Phase 4l) |
| Phase 4k plan commit SHA | (recorded; matches the Phase 4k merge SHA) |
| Phase 4j §11 governance commit SHA | (recorded; matches the Phase 4j merge SHA) |
| Phase 4i acquisition commit SHA | (recorded; matches the Phase 4i merge SHA) |
| Phase 4g spec commit SHA | (recorded; matches the Phase 4g merge SHA) |
| Backtest run start UTC ms | (recorded) |
| Backtest run end UTC ms | (recorded) |
| Wall-clock duration | (recorded) |

### Table 2 — Dataset manifest references

| Dataset | Version | Manifest path | Manifest SHA256 | research_eligible | feature_use |
|---|---|---|---|---|---|
| BTC 30m | v001 | `data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json` | (recorded) | true | full |
| ETH 30m | v001 | (per Phase 4i) | (recorded) | true | full |
| BTC 4h | v001 | (per Phase 4i) | (recorded) | true | full |
| ETH 4h | v001 | (per Phase 4i) | (recorded) | true | full |
| BTC metrics | v001 | (per Phase 4i) | (recorded) | false | oi_subset_only_per_phase_4j_§11 |
| ETH metrics | v001 | (per Phase 4i) | (recorded) | false | oi_subset_only_per_phase_4j_§11 |
| BTC funding | v002 | (per v002) | (recorded) | true | full |
| ETH funding | v002 | (per v002) | (recorded) | true | full |

### Table 3 — Parameter grid

The 9 non-fixed axes × 2 options = 512 variants enumerated explicitly,
with per-variant identifier (1..512).

### Table 4 — Train / validation / OOS split

The exact UTC date boundaries per §"Train / validation / holdout
windows" above.

### Table 5 — Per-variant trade summary (BTCUSDT, train window, MEDIUM-slip)

| Variant id | trade_count | win_rate | mean_R | median_R | total_R | max_DD_R | profit_factor | sharpe_train | DSR_train | DSR_significant_5pct |
|---|---|---|---|---|---|---|---|---|---|---|

(Full 512-row table.)

### Table 6 — Per-variant trade summary (BTCUSDT, validation window, MEDIUM-slip)

(Same columns as Table 5, validation window.)

### Table 7 — Per-variant trade summary (BTCUSDT, OOS holdout window, MEDIUM-slip)

(Same columns as Table 5, OOS window. **The primary V2 evidence
cell.**)

### Tables 8 / 9 / 10 — ETHUSDT versions

(Same as Tables 5 / 6 / 7 but for ETHUSDT. ETHUSDT is comparison-only;
ETH cannot rescue BTC.)

### Table 11 — BTCUSDT-train-best variant identification

Identifies the BTC-train-best variant (per train-window Sharpe,
respecting DSR > 1.96 filter). Includes:

- variant id;
- variant axis values;
- train Sharpe;
- DSR;
- validation Sharpe;
- OOS holdout Sharpe;
- train-to-OOS Sharpe decay.

### Table 12 — BTCUSDT-train-best variant cost cells

| Cost cell | mean_R | total_R | sharpe | profit_factor | passes_CFP_2 |
|---|---|---|---|---|---|
| LOW-slip | (computed) | (computed) | (computed) | (computed) | (true / false) |
| MEDIUM-slip | (computed) | (computed) | (computed) | (computed) | (true / false) |
| **HIGH-slip (§11.6)** | (computed) | (computed) | (computed) | (computed) | (true / false) |

### Table 13 — M1 / M2 / M3 mechanism-check tables

Per (variant, symbol, OOS holdout window, MEDIUM-slip):

- M1: `frac_reached_0_5R`, M1 pass / fail.
- M2: `mean_R(full)`, `mean_R(participation_relaxed)`, `diff_M2`,
  bootstrap-CI lower bound, M2 pass / fail.
- M3: `mean_R(full)`, `mean_R(derivatives_relaxed)`, `diff_M3`,
  §11.6 HIGH cost-resilience differential, M3 pass / fail.

### Table 14 — Cost sensitivity comparison

Per variant: train / validation / OOS Sharpe and mean_R at LOW /
MEDIUM / HIGH cells.

### Table 15 — PBO computation

PBO (train → validation), PBO (train → OOS), with confidence intervals.

### Table 16 — Deflated Sharpe correction summary

Distribution of DSR across 512 variants on train / validation / OOS;
count of variants surviving DSR > 1.96 per window.

### Table 17 — CSCV S = 16 sub-sample sharpe rankings

For each of the 12 870 CSCV combinations: in-sample-best variant id,
its OOS rank.

### Table 18 — Metrics OI per-bar exclusion table

| symbol | date_utc | bar_open_time_ms | bars_excluded_per_day | bars_excluded_cumulative | exclusion_reason |
|---|---|---|---|---|---|

(Full table, with per-symbol totals and percentage of the symbol's
30m bar count.)

### Table 19 — Main-cell vs. exclude-entire-affected-days sensitivity

Per variant on OOS holdout window:

| variant id | symbol | main_mean_R | sensitivity_mean_R | difference | CFP_8_triggered |
|---|---|---|---|---|---|

### Table 20 — Trade distribution by year / month / regime

Per-variant trade count and total R per calendar year + month +
volatility regime (low / medium / high ATR percentile bucket).
CFP-7 evaluation.

### Table 21 — Verdict declaration

V2 framework verdict (one of A / B / C / D per §"Promotion / failure /
partial-pass criteria"). Includes rationale, predicate-trigger
identifications, and a forbidden-work confirmation.

### Table 22 — Forbidden-work confirmation

Per the Phase 4l brief and Phase 4k forbidden-work list:

- "Optional ratio-column access detection: zero accesses confirmed";
- "Per-bar exclusion algorithm verification: matches Phase 4j §16
  exactly";
- "Forbidden data access detection: zero accesses confirmed";
- "Lookahead detection: zero violations confirmed";
- "Timestamp alignment verification: monotone and on-boundary";
- "Authentication-API access: zero attempts";
- "Production-key request: zero";
- "Network I/O outside data.binance.vision public bulk: zero".

If any of these is non-zero, Verdict D (INCOMPLETE / methodology
stop).

---

## Required plots or diagnostics

The future Phase 4l execution phase report MUST include the following
plot artefacts (PNG output under `data/research/phase4l/plots/`,
referenced from the Markdown report):

| Plot | Purpose |
|---|---|
| Cumulative R curve, BTCUSDT, BTC-train-best variant, train + validation + OOS | Visual OOS persistence check. |
| Cumulative R curve, ETHUSDT, BTC-train-best variant, train + validation + OOS | Cross-symbol consistency. |
| Per-variant Sharpe heatmap (axes: train/val/OOS × variant id) | Variant-by-window stability. |
| DSR distribution histogram, train + validation + OOS | DSR significance distribution. |
| PBO sub-sample rank distribution | PBO interpretation. |
| Drawdown curve, BTC-train-best variant, OOS holdout | CFP-3 evaluation. |
| Trade-distribution histogram (R outcome bins), BTC + ETH, OOS | Trade outcome shape. |
| Monthly-bucketed cumulative R, BTC, OOS | CFP-7 (regime/month overconcentration). |
| Excluded-bar count timeseries | Phase 4j §11 governance evidence. |
| Sensitivity-cell vs. main-cell mean_R per variant | CFP-8 evaluation. |

Plots are diagnostic-only; the verdict is determined by the tables,
not the plots.

---

## Stop conditions

The future Phase 4l execution phase MUST stop and produce a failure
report (NOT a partial-result report, NOT a "best-effort" report) if
any of the following stop conditions trigger:

| Condition | Stop response |
|---|---|
| Required manifest missing | abort; failure report; no V2 results |
| Manifest SHA256 mismatch (modified between load and emit) | abort; failure report |
| Local data file not found at expected Parquet partition | abort; failure report |
| Data file corrupted / unreadable | abort; failure report |
| Optional ratio column accessed (CFP-10) | abort; failure report; flag governance violation |
| Per-bar exclusion algorithm deviation from Phase 4j §16 (CFP-11) | abort; failure report |
| Lookahead detected (any feature reads future-bar data) | abort; failure report |
| Timestamp misalignment (any 30m bar `open_time` not on 30m boundary) | abort; failure report |
| Backtest emits trades on excluded bars | abort; failure report |
| Trade count insufficient on > 50% of variants (CFP-1) | report; HARD REJECT |
| Validation report incomplete (any required table missing) | abort; failure report |
| Any code path attempts authentication / private endpoint / live API access (CFP-12) | abort; failure report; flag safety violation |
| Any code path attempts to read or store credentials | abort; failure report; flag safety violation |
| Any code path attempts network I/O outside `data.binance.vision` public bulk (and the script does not need any network I/O at all because data is local) | abort; failure report; flag safety violation |
| Any code path attempts to write to `data/raw/`, `data/normalized/`, `data/manifests/` (read-only access required for Phase 4l) | abort; failure report; flag governance violation |
| Test count regression in pytest (any tests regressed by Phase 4l implementation) | abort; failure report |
| ruff / mypy violation (Phase 4l implementation must not break whole-repo quality gate) | abort; failure report |

The Phase 4l execution phase MUST fail closed on any of these. The
operator MUST review the failure report before any retry or
remediation phase is authorized.

---

## Reproducibility requirements

Per Phase 4i § "Reproducibility notes" pattern:

### Public unauthenticated source only

V2 backtest data is locally cached from `data.binance.vision`
public unauthenticated bulk archives via Phase 4i acquisition. The
Phase 4l execution phase does NOT re-acquire data, does NOT make any
network call, does NOT consult any authenticated endpoint.

### SHA256 verification

The Phase 4l execution phase MUST verify each manifest's `raw_sha256_index`
against locally stored Parquet partitions before backtest computation.
Any mismatch → abort.

### Deterministic variant ordering

Per §"Search-space control" — lexicographic ordering ensures
deterministic results across re-runs.

### Pinned random seeds

Bootstrap-by-trade and CSCV computations require seeded RNG. The
Phase 4l brief MUST pin the seeds (e.g., `bootstrap_rng_seed =
202604300` — derived from the Phase 4l brief commit date — and
record them in the report).

### Idempotent rerun

If the Phase 4l execution phase is rerun with the same manifests,
same code commit, same RNG seeds, and same input data, the report
MUST produce identical results.

### Manifest SHA pinning in report

The Phase 4l report MUST record the manifest SHA256 of every input
dataset (per Table 2 above). A future re-run that produces different
manifests MUST be flagged as a different run.

### Standalone script

`scripts/phase4l_v2_backtest.py` MUST be a standalone script with no
imports from `prometheus.research.data.*`, `prometheus.runtime.*`,
`prometheus.execution.*`, `prometheus.persistence.*`, or any module
that performs network I/O.

### Test suite preservation

The Phase 4l execution phase MUST NOT modify any test under
`tests/**`. Any new tests for Phase 4l implementation belong in
`tests/research/` (analogous to the Phase 4a `tests/unit/runtime/`
pattern), at most.

### Repository quality gate preservation

The Phase 4l execution phase MUST preserve the post-merge whole-repo
quality gate: `ruff check .` passes; `pytest` 785 (or more, if Phase
4l adds tests) passes; `mypy --strict` 0 issues.

---

## What this does not authorize

Phase 4k explicitly does NOT authorize, propose, or initiate any of
the following:

- **Phase 4l execution.** Phase 4k is the docs-only plan; Phase 4l
  authorization is a separate operator decision.
- **V2 backtest.** Forbidden until Phase 4l is authorized AND the
  Phase 4l brief honors the Phase 4k methodology.
- **V2 implementation.** Forbidden until V2 backtest evidence is in
  AND a separately authorized implementation phase exists.
- **V2 strategy implementation under `src/prometheus/strategy/`.**
  Forbidden.
- **V2 strategy / execution / risk module modification.** Forbidden.
- **Phase 4 (canonical).** Per `docs/12-roadmap/phase-gates.md`.
- **Live exchange-write capability.** Architectural prohibition
  unchanged.
- **Production Binance keys, authenticated APIs, private endpoints,
  user stream, WebSocket, listenKey lifecycle, production alerting,
  Telegram / n8n production routes, MCP, Graphify, `.mcp.json`,
  credentials, exchange-write capability.** None of these is touched,
  enabled, or implied.
- **Strategy implementation, rescue, or new candidate** (other than
  the bounded V2 spec predeclared in Phase 4f / 4g and operationalized
  here).
- **R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A revision.** Preserved
  verbatim.
- **Phase 4f / 4g / 4h / 4i / 4j text modification.** All preserved
  verbatim.
- **Lock change.** §1.7.3 / §11.6 / mark-price stops / v002 verdict
  provenance preserved.
- **Data acquisition / patching / regeneration / modification.**
- **Manifest modification.** All `data/manifests/*.manifest.json`
  preserved verbatim.
- **Diagnostics / Q1–Q7 rerun / backtests.** None run.
- **Phase 3v stop-trigger-domain governance modification.** Preserved.
- **Phase 3w break-even / EMA slope / stagnation governance
  modification.** Preserved.
- **Phase 4j §11 metrics OI-subset partial-eligibility rule
  modification.** Preserved verbatim and incorporated as binding.
- **Reconciliation implementation.** Phase 4e reconciliation-model
  design preserved verbatim, not implemented.
- **Mark-price 30m / 4h acquisition.** Deferred per Phase 4h §20 and
  Phase 4i §"Operator decision menu" Option C.
- **`aggTrades` acquisition.** Deferred per Phase 4h §7.E and Phase
  4i §"Operator decision menu" Option D.
- **v003 dataset creation.** Not authorized.
- **Optional ratio-column activation.** Forbidden by Phase 4j §11.3 /
  §14 / §"Optional ratio-column prohibition" above.
- **OI feature removal.** Forbidden by Phase 4g §6 / §31 / §"Forbidden
  signal additions" above.
- **Phase 4k execution-plan text modification post-merge.** Phase 4k
  is itself predeclared and immutable from the Phase 4k merge forward.
  Any future change to Phase 4k requires a separately authorized
  governance memo amending Phase 4k explicitly.
- **Paper / shadow / live-readiness / deployment.** Not authorized.

---

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4l / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched, or
  commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 data acquisition.**
- **No data acquired.** No `data/` artefact modified. No public
  Binance endpoint consulted in code.
- **No implementation code written.** Phase 4k is text-only.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env`
  modification.
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** Phase 4k performs no network I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.**
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
  Existing `prometheus.strategy` modules untouched.
- **No strategy rescue proposal.** V2 is a new ex-ante hypothesis,
  NOT a re-parameterized successor of any retained-evidence candidate.
- **No 5m strategy / hybrid / retained-evidence successor / new
  variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **`scripts/phase3q_5m_acquisition.py` not run.**
- **`scripts/phase3s_5m_diagnostics.py` not run.**
- **`scripts/phase4i_v2_acquisition.py` not run.**
- **No data acquisition / download / patch / regeneration /
  modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json`
  preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No Phase 4i manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A
  all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4j §11 metrics OI-subset governance modification.**
- **No Phase 4f / 4g / 4h / 4i / 4j text modification.**
- **No Phase 4g V2 strategy-spec modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md`
  substantive change.**
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md`
  substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
  substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md`
  substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive
  change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4k branch.** Per the Phase 4k brief.
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No merge to main.**
- **No successor phase started.**

---

## Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4k
  deliverables exist as branch-only artefacts pending operator review.
- **Phase 4k output:** docs-only V2 backtest-plan memo + closeout
  artefact on the Phase 4k branch.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4k startup).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a executed and merged.
  Phase 4b / 4c cleanups merged. Phase 4d review merged. Phase 4e
  reconciliation-model design memo merged. Phase 4f V2 hypothesis
  predeclaration merged. Phase 4g V2 strategy-spec memo merged.
  Phase 4h V2 data-requirements / feasibility memo merged. Phase 4i
  V2 acquisition + integrity validation merged (partial-pass). Phase
  4j V2 metrics governance memo merged. Phase 4k V2 backtest-plan
  memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Metrics OI-subset partial-eligibility governance:** Phase 4j §11
  (preserved verbatim and incorporated as binding for Phase 4l).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared by Phase 4f as
  *Participation-Confirmed Trend Continuation*; operationalized by
  Phase 4g (strategy spec); data-requirements + feasibility analysis
  by Phase 4h; data acquisition by Phase 4i (partial pass; metrics
  not eligible globally); metrics governance by Phase 4j; **backtest
  methodology by Phase 4k (this memo).** **NOT implemented; NOT
  backtested; NOT validated.**
- **OPEN ambiguity-log items after Phase 4k:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:**
  `phase-4k/v2-backtest-plan-memo` exists locally and (after push)
  on `origin`. NOT merged to main.

---

## Operator decision menu

Phase 4k presents the following operator decision options:

### Option A — Remain paused (PROCEDURALLY ACCEPTABLE)

Take no further action. Phase 4k methodology is recorded; Phase 4l
execution is not authorized.

**Verdict:** procedurally acceptable; preserves predeclaration purity
without committing to V2 backtest execution.

### Option B — Phase 4l: V2 Backtest Execution (docs-and-code) (PRIMARY RECOMMENDATION)

Authorize a separate Phase 4l execution phase that implements the
Phase 4k methodology exactly. Phase 4l would:

1. Implement `scripts/phase4l_v2_backtest.py` standalone.
2. Run the 512-variant V2 backtest on the predeclared train /
   validation / OOS holdout windows.
3. Apply Phase 4j §11 per-bar exclusion exactly.
4. Compute M1 / M2 / M3 + DSR + PBO + CSCV + cost-cell sensitivity.
5. Produce the V2 backtest report with all required tables and plots.
6. Stop. Phase 4l does NOT recommend any successor phase by design.

**Constraints binding on Phase 4l:** Phase 4k methodology MUST be
honored exactly; CFP-10 / CFP-11 / CFP-12 must abort the run; the
Phase 4l report MUST emit a definitive verdict (A / B / C / D).

**Verdict:** PRIMARY RECOMMENDATION. Phase 4l is the natural
continuation of the Phase 4f → 4g → 4h → 4i → 4j → 4k chain; it
produces concrete V2 evidence that the operator can use to make a
post-Phase-4l decision (V2 implementation candidacy, V2 retention as
research evidence only, or V2 HARD REJECT termination).

### Option C — Further Phase 4k methodology refinement (NOT RECOMMENDED)

Authorize a separate Phase 4k-followup memo (e.g., revising window
boundaries, revising CFP thresholds, revising M1 / M2 / M3
mechanism-check thresholds).

**Verdict:** NOT RECOMMENDED. Phase 4k methodology is committed and
should be considered final until Phase 4l execution evidence is in.
Refining methodology after observing data would be post-hoc tuning.

### Option D — Phase 4j §11 amendment (NOT RECOMMENDED unless explicitly authorized)

Authorize a separate governance amendment relaxing Phase 4j §11
(e.g., to permit forward-fill, to activate optional ratio columns,
or to widen the exclusion criteria).

**Verdict:** NOT RECOMMENDED. The Phase 4j §11 binding rule is
exactly the governance discipline V2's first backtest needs. Relaxing
it before the first backtest is run would be premature.

### Option E — V2 strategy-spec amendment (REJECTED)

Modify Phase 4g V2 spec (e.g., remove the OI feature; add a 5m
diagnostic; add a session-exclusion zone; remove the participation
gate).

**Verdict:** REJECTED. Phase 4g spec is committed; modifying it to
fit observed Phase 4i data quality would be parameter rescue.

### Option F — Mark-price 30m / 4h acquisition (NOT RECOMMENDED before Phase 4l)

Authorize a separate Phase 4i-followup phase to acquire mark-price
30m / 4h klines.

**Verdict:** NOT RECOMMENDED. Mark-price 30m / 4h is the future
`mark_price_backtest_candidate` path per Phase 3v §8.5. Acquiring
it before V2's first trade-price backtest evidence would invert the
standard ordering.

### Option G — `aggTrades` acquisition (NOT RECOMMENDED)

Authorize a separate Phase 4i-followup phase to acquire `aggTrades`.

**Verdict:** NOT RECOMMENDED. Phase 4h §7.E and Phase 4i §"Operator
decision menu" Option D both recommend against this; kline
`taker_buy_volume` is sufficient for V2's first backtest.

### Option H — Immediate V2 implementation (REJECTED)

Skip Phase 4l and proceed directly to V2 strategy implementation.

**Verdict:** REJECTED. V2 implementation requires successful backtest
evidence (which does not exist).

### Option I — Paper / shadow / live-readiness / exchange-write (FORBIDDEN)

Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.

**Verdict:** FORBIDDEN.

### Phase 4k recommendation

**Phase 4k recommendation: Option B (Phase 4l V2 Backtest Execution,
docs-and-code) primary; Option A (remain paused) conditional
secondary.** No further options recommended; Options C / D / E / F /
G are not recommended; Option H is rejected; Option I is forbidden.

---

## Next authorization status

**No next phase has been authorized.** Phase 4k's recommendation is
**Option B (Phase 4l V2 Backtest Execution, docs-and-code) as
primary**, with **Option A (remain paused) as conditional secondary**.
Options C / D / E / F / G are not recommended. Option H is rejected.
Option I is forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has been
issued.

The 5m research thread remains operationally complete and closed
(per Phase 3t). The implementation-readiness boundary remains
reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding
governance blockers remain RESOLVED at the governance level (per
Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented
(per Phase 4a). The Phase 4b script-scope quality-gate restoration
is complete (per Phase 4b). The Phase 4c state-package quality-gate
residual cleanup is complete (per Phase 4c). The Phase 4d
post-4a/4b/4c review is complete (per Phase 4d). The Phase 4e
reconciliation-model design memo is complete (per Phase 4e). The
Phase 4f V2 hypothesis predeclaration is complete (per Phase 4f).
The Phase 4g V2 strategy spec is complete (per Phase 4g). The Phase
4h V2 data-requirements / feasibility memo is complete (per Phase
4h). The Phase 4i V2 public data acquisition + integrity validation
is complete (per Phase 4i; partial-pass). The Phase 4j V2 metrics
data governance memo is complete (per Phase 4j; Phase 4j §11 binding).
The Phase 4k V2 backtest-plan memo is complete on this branch (this
phase). **Recommended state remains paused.**
