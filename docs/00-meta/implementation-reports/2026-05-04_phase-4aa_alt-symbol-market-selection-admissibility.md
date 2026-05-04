# Phase 4aa — Alt-Symbol Market-Selection and Strategy-Admissibility Memo

**Authority:** Operator authorization for Phase 4aa (docs-only research-direction memo evaluating whether future strategy research should remain BTCUSDT / ETHUSDT only or consider liquid large-cap Binance USDⓈ-M perpetual alt symbols). Phase 4z (post-rejection research-process redesign memo; merged 6fb0c6c; recommendations remain recommendations only and are NOT adopted governance); Phase 4y (post-C1 consolidation); Phase 4x (C1 backtest execution; Verdict C HARD REJECT — terminal for C1 first-spec); Phase 4w (C1 backtest-plan methodology); Phase 4v (C1 strategy spec); Phase 4u (C1 hypothesis-spec); Phase 4t (post-G1 fresh-hypothesis discovery); Phase 4s (post-G1 consolidation); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal); Phase 4q (G1 backtest-plan); Phase 4p (G1 strategy spec); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery); Phase 4m (post-V2 consolidation; 18-requirement validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal); Phase 4k (V2 backtest-plan); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4h (V2 data-requirements / feasibility memo); Phase 4g (V2 strategy spec); Phase 4f (external strategy research landscape memo); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t §12 (validity gate for any future research); Phase 3k (post-D1-A consolidation); Phase 3e (post-F1 consolidation); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4aa — **Alt-Symbol Market-Selection and Strategy-Admissibility Memo** (docs-only research-direction memo). Frames the question of whether the project's strategy-research substrate should remain BTCUSDT / ETHUSDT only or expand to include liquid large-cap Binance USDⓈ-M perpetual alt symbols (SOLUSDT, XRPUSDT, ADAUSDT primary candidate set; BNBUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT secondary watchlist). Defines a pre-backtest symbol-admissibility framework. Recommends remain-paused as primary (always procedurally valid) and a future docs-only alt-symbol data-requirements / feasibility memo as conditional secondary (only if separately authorized; not started by Phase 4aa). **Phase 4aa is text-only.** No data acquisition. No backtest. No strategy spec. No implementation. No live-readiness. No exchange-write. No retained verdict revised. No project lock changed. No governance file amended. No successor phase authorized.

**Branch:** `phase-4aa/alt-symbol-market-selection-admissibility`. **Memo date:** 2026-05-04 UTC.

---

## 1. Purpose

Phase 4aa evaluates whether future strategy research should remain restricted to BTCUSDT / ETHUSDT (the project's substrate from Phase 2 onward) or whether liquid large-cap Binance USDⓈ-M perpetual alt symbols deserve future data-acquisition and strategy-spec work as a candidate research substrate.

**Phase 4aa is docs-only.**

- **No data acquisition.** No new dataset is downloaded, ingested, normalized, or materialized.
- **No backtest.** No backtest is run, planned, or scoped beyond the conceptual question.
- **No strategy spec.** No new strategy candidate is named, defined, or specified.
- **No implementation.** No code is written, modified, or committed under `src/prometheus/`, tests, or scripts.
- **No live-readiness.** No paper / shadow / live operation is authorized, planned, or implied.
- **No exchange-write.** No production keys, authenticated APIs, private endpoints, user stream, WebSocket, or exchange-write capability is touched.

Phase 4aa records the question, the prior-failure constraints any answer must respect, a candidate symbol universe, a market-type boundary recommendation, a pre-backtest admissibility framework, an analysis of whether prior strategies can be improved on alt symbols, a description of what a future data phase would need, an operator decision menu, and a primary recommendation. Phase 4aa does NOT pretend to know the answer; it frames the question and proposes the next docs-only step *if* the operator chooses to continue research.

## 2. Why This Question Is Now Logical

The question is now logical for the following project-record reasons:

1. **BTC was originally selected for production safety, liquidity, and lower idiosyncratic behavior.** The Phase 2 strategy-research arc selected BTCUSDT as the primary live symbol and ETHUSDT as the first comparison symbol per `docs/03-strategy-research/first-strategy-comparison.md`. The selection prioritized exchange depth, lower headline-driven volatility relative to alt-cap names, longer continuous trading history, and operational suitability for staged tiny-live deployment. These reasons remain valid for *production* selection.
2. **ETH was the first comparison symbol.** The project methodology has consistently used BTC primary / ETH comparison through Phases 2e–2w (V1 breakout arc), Phase 3a–3d-B2 (F1 arc), Phase 3f–3j (D1-A arc), Phase 4f–4l (V2 arc), Phase 4n–4r (G1 arc), and Phase 4t–4x (C1 arc). ETH has acted as a non-rescue cross-symbol consistency check; ETH has never been authorized to rescue BTC.
3. **Repeated BTC/ETH-centered strategy research has not produced a viable live/paper candidate.** Six terminal negative outcomes (R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2 HARD REJECT; G1 HARD REJECT; C1 HARD REJECT) are now on record, all evaluated against BTCUSDT primary on the same Phase 4i / v002 dataset family. R3 (Fixed-R take-profit + unconditional time-stop) is the V1 baseline-of-record but is research evidence only and is not promoted to live readiness; R1a / R1b-narrow are retained-non-leading research evidence.
4. **Manual operator observation.** The operator has reported, during the V2 → G1 → C1 sequence, that BTC often had difficulty finding clean setups and overcoming costs. This is a directional observation, not a quantitative claim; it is recorded here as motivation for the question, not as a substitute for data.
5. **The discovery-process redesign issue.** Phase 4z (merged at 6fb0c6c) proposed (as recommendations only, not adopted governance) a design-family-distance matrix (F-1 mechanical-condition + breakout / F-2 pullback-mean-reversion / F-3 funding-derivatives / F-4 microstructure) and observed that V2 / G1 / C1 all sit in the shared F-1 family. Phase 4aa observes that "design family" and "market substrate" are *separable* axes: a future hypothesis can vary along either axis independently, and the project has so far varied only along the design-family axis (within F-1 + a single F-2 / F-3 entry) while holding the market substrate fixed (BTC + ETH).
6. **Therefore, the next rational question is whether BTC / ETH are the wrong substrate for the current class of rules-based breakout / trend-continuation research.** This is a substrate-selection question, not a strategy-selection question. The question's importance does not depend on having an answer; it depends on the project not having previously asked it. Phase 4aa asks the question.

**Important — no claim about the answer:** Phase 4aa does NOT claim that alt symbols would have produced different outcomes for V2 / G1 / C1. Phase 4aa does NOT claim that BTC / ETH are the wrong substrate. Phase 4aa does NOT propose retroactive evaluation of prior failed strategies on alt symbols (this would be retrospective rescue and is forbidden). Phase 4aa frames the question and proposes only that a future docs-only data-requirements memo *could* be authorized to begin establishing the evidence base; the answer remains genuinely unknown until evidence exists.

## 3. Prior Failure Topology as Negative Constraints

Each of the six rejection events imposes a constraint on any future alt-symbol research. Phase 4aa restates the topology and translates each into a future-research negative constraint.

### R2 — cost-fragility

**Failure:** R2 (pullback-retest entry, V1 family) generated mechanism evidence (M1 ✓, M3 ✓, M2 ✗) but failed §11.6 cost-sensitivity at HIGH = 8 bps per side. Cost was the binding driver.

**Constraint for alt-symbol research:** any alt-symbol candidate must demonstrate **cost-to-volatility viability** before promotion. Specifically, the candidate's expected per-trade R distribution must be theoretically large enough relative to typical entry slippage + taker fee + funding to leave positive expected value after §11.6 = 8 bps HIGH per side. Alt symbols may have higher headline volatility but also wider spreads and higher slippage; the cost-to-volatility ratio is what matters, not raw volatility. **Cost relaxation is forbidden** (Phase 3l "B — conservative but defensible" preserved; §11.6 unchanged). A future alt-symbol candidate that argues "BTC's cost was too high for this strategy, but SOL's volatility is higher so cost survives" must derive that argument from first-principles theoretical content and must commit to §11.6 = 8 bps HIGH per side.

### F1 — catastrophic-floor / bad full-population expectancy

**Failure:** F1 (mean-reversion-after-overextension) generated mechanism evidence (M1 PARTIAL; M2 FAIL/weak; M3 PASS-isolated for the TARGET subset only) but the full population had bad expectancy. Phase 3c §7.3 catastrophic-floor predicate triggered 5× across BTC/ETH × MED/HIGH cells.

**Constraint for alt-symbol research:** **catastrophic-floor checks remain mandatory** for any alt-symbol candidate. CFP-1-equivalent predicates (BTC OOS HIGH `mean_R ≤ −0.40`, BTC OOS HIGH `profit_factor < 0.50`, ETH OOS HIGH `mean_R ≤ −0.40`, ETH OOS HIGH `profit_factor < 0.50`) and any other predeclared CFP must apply at the ALT symbol's primary cell. **Mechanism-isolated PASS (subset profitability) is research evidence, not promotion evidence.** A future alt-symbol candidate that produces a positive isolated subset on SOL but a negative full-population expectancy is HARD REJECT, not PASS. The project's Phase 4m §"Fresh-hypothesis validity gate" requirement #15 ("distinguish mechanism evidence from framework promotion") applies on every symbol independently.

### D1-A — mechanism / framework mismatch

**Failure:** D1-A (funding-Z-score contrarian) had M1 BTC h=32 PASS (mean +0.1748R), M3 PASS-isolated for the TARGET subset, but framework conditions cond_i (BTC MED expR > 0) and cond_iv (BTC HIGH cost-resilience) failed. M2 also failed on both symbols.

**Constraint for alt-symbol research:** **a plausible mechanism is not enough.** A future alt-symbol candidate must demonstrate that a partial-mechanism PASS does not by itself license framework promotion. The Phase 4w binding negative-baseline framework (M1 / M2.a / M2.b / M3 / M4) preserved verbatim in Phase 4aa as an example pattern for any future candidate, with each baseline differential evaluated **per symbol independently**. ETH cannot rescue BTC; symmetrically, no alt symbol can rescue any other alt symbol. Cross-symbol consistency is a *non-rescue* check, not a *promotion* mechanism. A candidate that passes mechanism on SOL but fails framework conditions on SOL is HARD REJECT for SOL; the candidate does not become valid by averaging across the symbol universe.

### V2 — design-stage incompatibility / zero trades

**Failure:** V2 (participation-confirmed trend continuation) failed CFP-1 critical (512/512 variants below 30 BTC OOS HIGH trades; train-best 0 trades). The locked Phase 4g 0.60–1.80 × ATR(20) stop-distance filter (V1-inherited) was structurally incompatible with V2's 20/40-bar Donchian setup geometry.

**Constraint for alt-symbol research:** **opportunity-rate viability must be checked before full strategy specification.** Any future alt-symbol candidate must predeclare an expected joint-event rate (setup AND stop_distance_passes) for each candidate symbol *before* a strategy-spec memo, derived from the candidate's first-principles theoretical content rather than from observed forensic numbers. Different symbols have different ATR distributions; a stop-distance filter calibrated to BTC's ATR distribution may produce zero qualifying trades on a less-volatile or more-volatile alt symbol. Each symbol's setup-geometry / stop-distance compatibility is its own research question. **Stop-distance bounds must NOT be passively inherited from a prior strategy on a prior symbol.** The Phase 4m requirement #4 (entry / stop / target / sizing / cost / timeframe / exit must be co-designed) applies on every symbol.

### G1 — regime-gate-meets-setup intersection sparseness / zero qualifying trades

**Failure:** G1 (regime-first breakout continuation) failed CFP-1 critical (32/32 variants below 30 BTC OOS HIGH G1 trades) and CFP-9 independent (regime active fraction 2.03% < 5% threshold). The Phase 4p locked five-dimension AND classifier was structurally too narrow relative to the 30m breakout trigger.

**Constraint for alt-symbol research:** **opportunity-rate viability must be checked before full strategy specification, with explicit attention to multi-condition AND classifiers.** Any future alt-symbol candidate that proposes multi-condition gating must predeclare the joint-event rate per candidate symbol *and* the per-condition activation rate *before* a strategy-spec memo. CFP-9-equivalent thresholds (active fraction floor; joint event rate floor; per-variant trade-count floor) must be predeclared from theoretical content. **The fact that a multi-condition classifier produces sparse intersections on BTC does not imply it will produce sparse intersections on SOL** — but it also does not imply it will produce richer intersections; the question must be evaluated empirically *if* the candidate is ever authorized. Phase 4aa does NOT authorize that evaluation.

### C1 — fires-and-loses / contraction anti-validation

**Failure:** C1 (volatility-contraction expansion breakout) generated a healthy trade population (149 BTC OOS HIGH trades for the train-best variant; transition rate 3.33 / 480 bars; CFP-1 and CFP-9 explicitly did NOT trigger) and produced strictly-negative differentials against three independent baselines (M1 -0.244R CI [-0.41, -0.08]; M2.a -0.220R CI [-0.39, -0.06]; M2.b -0.293R). Cost was NOT the binding driver; LOW / MEDIUM / HIGH all loss-making.

**Constraint for alt-symbol research:** **"more trades" is not enough; theoretical baseline superiority is required.** Any future alt-symbol candidate must predeclare an expected baseline differential `Δ_R` from first-principles theoretical content with bootstrap-CI-based pass/fail, *before* the backtest. The Phase 4w binding negative-baseline framework (M1 / M2.a / M2.b) must apply per symbol independently. **A future candidate that fires plenty of trades on SOL but is anti-validated against same-geometry baselines on SOL is HARD REJECT for SOL.** Sample-size adequacy is a sample-existence gate; baseline-superiority is a strategy-quality gate. The two must remain separable, and both must pass per symbol.

### Summary of negative constraints

For any future alt-symbol candidate (none of which is authorized by Phase 4aa):

1. **Cost-to-volatility viability** must be predeclared from theory before spec promotion (R2 lesson).
2. **Catastrophic-floor predicates** must apply per symbol independently (F1 lesson).
3. **Mechanism PASS does not imply framework PASS**; each symbol's evidence stands on its own (D1-A lesson).
4. **Opportunity-rate viability** must be predeclared from theory before spec promotion (V2 lesson).
5. **Joint-event rate** for multi-condition designs must be predeclared from theory before spec promotion (G1 lesson).
6. **Theoretical baseline superiority** with predicted Δ_R must be predeclared from theory; fires-and-loses anti-validation is HARD REJECT (C1 lesson).
7. **Stop-distance, setup-geometry, target, sizing, time-stop, and cost cells** must be co-designed per symbol from first principles (V2 + G1 + C1 cumulative lesson).
8. **No retroactive rescue.** Prior failed strategies (R2, F1, D1-A, V2, G1, C1) are NOT to be re-evaluated on alt symbols; that would be retrospective rescue. Future alt-symbol candidates must be genuinely ex-ante under the Phase 4m 18-requirement validity gate.

## 4. Candidate Symbol Universe

Phase 4aa defines a candidate symbol universe for *future* research consideration. **No symbol on this list is authorized for data acquisition or backtest by Phase 4aa.** The universe is recorded so that any future docs-only data-requirements memo can refer to a stable starting set; the operator may modify the set at the time of any future authorization.

### Required primary comparison set

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

This set retains BTC and ETH (continuity with the existing project record; Phase 4i v001 30m / 4h klines and v002 datasets remain available) and adds three liquid large-cap Binance USDⓈ-M perpetual alt symbols (SOL, XRP, ADA) as candidate alt-symbol entries.

### Optional secondary watchlist

```text
BNBUSDT
DOGEUSDT
LINKUSDT
AVAXUSDT
```

Optional secondary symbols are **not required** for any future first alt-symbol data-requirements memo. They are recorded as candidate watchlist entries that could be considered in a future iteration if the primary comparison set produces sufficiently informative evidence to justify expansion. **Phase 4aa does NOT authorize watchlist symbols for any data acquisition.**

### Qualitative tradeoff discussion (per symbol group)

The discussion below is **qualitative only**. Phase 4aa does NOT invent quantitative results. No volume, spread, ATR, slippage, opportunity-rate, or cost-survival number is fabricated. Where future data acquisition would be required to evaluate a tradeoff empirically, the section explicitly says so.

#### BTCUSDT (primary; existing substrate)

- **Liquidity:** highest of any USDⓈ-M perpetual on Binance (existing project record indicates depth at top-of-book is generally deep; tail-of-book conditions in stressed regimes have not been independently measured by the project).
- **Volatility:** moderate among large-cap crypto; lower headline-driven instability than smaller-cap alts.
- **Opportunity rate:** measured indirectly across V1 / V2 / G1 / C1 arcs; varies by strategy timeframe and entry rule.
- **Idiosyncratic risk:** lower than alt-cap names (no single-protocol or single-ecosystem dependency).
- **Funding / derivative-flow instability:** moderate; D1-A arc demonstrated funding-Z-score |Z_F| ≥ 2.0 events occur and are tradable as a directional trigger only if the framework survives, which it did not.
- **Wick risk:** Phase 3s Q2 5m diagnostic established V1-family wick-fraction 0.571–1.000 on adverse stop exits — wick risk is real on BTC; alt symbols may be worse.
- **Spread / slippage risk:** project assumes §11.6 = 8 bps HIGH per side as the binding cost; this is preserved.
- **Delisting / metadata-change risk:** essentially zero.
- **Data availability:** complete; v002 + Phase 4i 30m / 4h klines + v002 funding manifests cover the project's research period.

#### ETHUSDT (existing comparison)

- **Liquidity:** very high; second among USDⓈ-M perpetuals after BTC.
- **Volatility:** higher than BTC under most regimes.
- **Opportunity rate:** has acted as a non-rescue cross-symbol consistency check across V1 / V2 / G1 / C1; never sufficient to rescue BTC.
- **Idiosyncratic risk:** moderate; ecosystem-driven flow events (gas-pricing changes, L2 narratives, validator-set events) can produce idiosyncratic moves.
- **Funding / derivative-flow instability:** similar to BTC; correlated.
- **Wick risk:** generally similar to BTC under normal regimes; widens under high-volatility events.
- **Spread / slippage risk:** §11.6 preserved.
- **Delisting / metadata-change risk:** essentially zero.
- **Data availability:** complete; same coverage as BTC.

#### SOLUSDT (primary alt candidate)

- **Liquidity:** large among non-BTC / non-ETH alts on USDⓈ-M perpetuals; the project has not independently measured top-of-book depth or stressed-tail behavior.
- **Volatility:** higher than BTC / ETH under most regimes; specific magnitude unmeasured by the project.
- **Opportunity rate:** unknown without data acquisition; would require future feasibility evaluation.
- **Idiosyncratic risk:** moderate-to-high; chain-outage history (recorded externally; not measured by the project), ecosystem-driven flows, and protocol-specific events are real risks.
- **Funding / derivative-flow instability:** unknown without data acquisition; alt symbols can have more pronounced funding-rate excursions during stress.
- **Wick risk:** unknown without data acquisition; alt symbols often have larger wicks proportionally.
- **Spread / slippage risk:** Phase 4aa cannot quantify; future feasibility evaluation would estimate this against §11.6 = 8 bps HIGH per side.
- **Delisting / metadata-change risk:** low for SOL specifically, but contract-specification changes (tick size, margin tier) can occur; a future data-requirements memo would need to inspect Binance USDⓈ-M perpetual contract metadata for SOL.
- **Data availability:** Binance public unauthenticated bulk archives generally cover SOL at standard intervals; a future feasibility memo would verify integrity gates.

#### XRPUSDT, ADAUSDT (primary alt candidates)

- **Liquidity:** large among non-BTC / non-ETH alts; project has not independently measured.
- **Volatility:** XRP is often described as having lower normal-regime volatility but periodic high-volatility events tied to legal / regulatory news; ADA has moderate volatility with ecosystem-driven flows. **Quantitative claims unmeasured.**
- **Opportunity rate, wick risk, funding instability, spread / slippage:** all unknown without future data acquisition.
- **Idiosyncratic risk:** XRP carries regulatory-event risk (legal-status changes; SEC / equivalent action history); ADA carries ecosystem-driven event risk. Both should be flagged in any future research as structural risks.
- **Delisting / metadata-change risk:** low for both; XRP has a non-trivial regulatory / venue-listing history (project has not independently audited this).
- **Data availability:** Binance public unauthenticated bulk archives generally cover both at standard intervals; a future feasibility memo would verify.

#### Secondary watchlist (BNB, DOGE, LINK, AVAX)

- **All four:** liquid USDⓈ-M perpetuals on Binance with well-known idiosyncratic risk profiles (BNB exchange-token risk; DOGE social-flow / meme-driven risk; LINK protocol-update / oracle-event risk; AVAX ecosystem-driven flows). **Quantitative claims unmeasured.** All four would require future data acquisition to evaluate empirically. Phase 4aa records them as watchlist entries only.

### Quantitative-claim disclaimer

Phase 4aa makes NO quantitative claim about any symbol's liquidity, volatility, opportunity rate, spread, slippage, wick fraction, funding instability, or cost survival. All such claims would require future data acquisition (which is NOT authorized by Phase 4aa) and a separately authorized feasibility memo. Where the project's existing record contains evidence (BTC and ETH only, per Phase 4i v001 30m / 4h klines + v002 + Phase 3s 5m diagnostics), the memo restates only what the record already shows; it does not generate new quantitative claims.

## 5. Market-Type Boundary

Phase 4aa recommends keeping any future alt-symbol research on the same market and product type as the existing project substrate:

```text
Binance USDⓈ-M perpetuals
```

### Recommended boundary

- **Keep same venue / product type for now.** Future alt-symbol research, if ever authorized, should remain on Binance USDⓈ-M perpetuals.
- **Do not change symbol universe and market type simultaneously.** Adding alt symbols *and* expanding to spot or COIN-M futures or options or other venues in a single step would mix two independent variables and contaminate attribution. The project's discipline is one independent variable per research step.
- **Do not evaluate spot / COIN-M / options / other venues in the same next step.** These are distinct markets with distinct cost models, distinct liquidation mechanics, distinct fee structures, distinct settlement rules, and distinct data-availability constraints. They are out of scope for any first alt-symbol step.
- **Clean attribution.** If future alt-symbol research produces evidence (positive or negative) on Binance USDⓈ-M perpetuals, the attribution is to the symbol-substrate change, not to a venue or product-type change. Mixing axes contaminates evidence.

### Excluded market types (explicitly not authorized)

- **Spot.** Different cost structure; different liquidation behavior (none); different fee schedule; different funding (none); different settlement. Out of scope.
- **COIN-M futures.** Inverse-margined; different P&L mechanics; different liquidation behavior; different funding settlement. Out of scope.
- **Options.** Premium-based; different P&L mechanics; different exposure model; different time-decay behavior. Out of scope.
- **Other venues** (centralized exchanges other than Binance; decentralized perpetual venues such as dYdX / Hyperliquid / GMX; cross-venue arbitrage strategies). Each carries distinct execution, custody, settlement, and data-availability constraints. Out of scope.

The project's §1.7.3 project-level locks (0.25% risk; 2× leverage; one position max; mark-price stops where applicable) are calibrated to Binance USDⓈ-M perpetuals; expanding market type would re-open those calibrations, which Phase 4aa does NOT authorize.

## 6. Symbol-Admissibility Framework

Phase 4aa defines a pre-backtest admissibility framework for any future symbol that might be considered for strategy research. **The framework is a recommendation** for any future docs-only data-requirements memo or strategy-spec memo to apply; it is not adopted governance and Phase 4aa does NOT itself admit any symbol.

A symbol is admissible for *future* strategy research only if it passes ALL of the following gates. **Failing any gate is HARD REJECT for the symbol.**

### A. Listing / continuity gate

- **Continuous trading history.** The symbol must have continuous Binance USDⓈ-M perpetual trading history covering the intended research period (project's chronological train / validation / OOS holdout windows or equivalent).
- **No delisting / relisting events** within the research period that materially compromise the dataset.
- **Stable contract metadata.** Significant contract changes (tick size; minimum quantity; maximum leverage; margin tier; funding settlement frequency) within the research period must be documented and treated as risk; a future data-requirements memo would need to inspect Binance metadata snapshots for the symbol.
- **Listing-driven volatility tail.** First-listing months and post-listing months may carry distinct volatility behavior; a future feasibility memo would consider whether to exclude an early window or treat it as a separate regime.

### B. Public-data availability gate

Future acquisition must be possible through **public unauthenticated** Binance USDⓈ-M data sources where possible (continuing the project's Phase 3q / Phase 4i acquisition pattern: `data.binance.vision` bulk archives; no credentials; no authenticated REST; no private endpoints; no user stream; no WebSocket; no listenKey lifecycle; no `.env`; no MCP / Graphify / `.mcp.json`). Required future datasets *may* include (the exact set is decided by a future data-requirements memo, NOT by Phase 4aa):

- **Standard trade-price klines** for relevant intervals (15m / 30m / 1h / 4h depending on the future research question).
- **Mark-price klines** if stop-trigger-domain or mark-price diagnostics are needed (Phase 3v §8 governance preserved; mark-price acquisition decisions follow Phase 3p §4.7 / Phase 3r §8 strict integrity rules and would require explicit Phase 4aa-equivalent treatment of any partial-pass outcomes).
- **Funding rate history** if a future hypothesis requires funding context.
- **Open-interest / metrics data** only if a future hypothesis requires derivatives-flow context, with strict eligibility rules learned from Phase 4i / Phase 4j §11 (the `metrics` family is globally `research_eligible: false`; the OI subset is partial-eligible per Phase 4j §11; optional ratio columns remain forbidden).
- **Exchange metadata snapshots** where available (contract-specification history; tick size changes; minimum quantity changes; funding settlement schedule changes).

A future data-requirements memo must apply Phase 3p §4.7 strict integrity gates verbatim per dataset and must not silently relax integrity rules.

### C. Cost-to-volatility gate

Before any strategy spec, a future data-requirements / feasibility memo must estimate whether each candidate symbol has enough normal movement to survive:

- **§11.6 = 8 bps HIGH per side** preserved verbatim; not relaxed.
- **Slippage assumptions.** Per-symbol expected slippage at production sizing (must be estimated, not assumed equivalent to BTC).
- **Stop distance.** Per-symbol expected stop distance at the candidate's intended timeframe.
- **Expected breakout range / move size.** Per-symbol distribution of typical R-distance moves.
- **Expected holding horizon.** Per-symbol distribution of move duration relative to the candidate's time-stop.

The cost-to-volatility ratio must be theoretically positive (gross-positive expectancy survives §11.6 HIGH) before any strategy spec is authorized. Phase 4aa does NOT perform this estimation; it is predeclared as a future feasibility requirement.

### D. Opportunity-rate gate

Before a full strategy spec, a future feasibility memo must estimate whether each candidate symbol plausibly produces enough candidate events to satisfy CFP-1 (≥ 30 trades for the train-best variant on the symbol's primary cell) and CFP-9 (per-event arrival rate; joint setup-AND-stop-distance-passes rate; per-variant trade-count pass fraction). This gate exists to avoid V2 / G1-style sparse-intersection failures on alt symbols.

The estimation must be derived from theoretical content (e.g., from the symbol's volatility-regime characterization and the candidate strategy's setup-frequency expectation), NOT from observed forensic numbers from prior failed strategies on prior symbols.

### E. Liquidity / execution-risk gate

**Alt symbols must not be admitted merely because they move more.** Higher headline volatility without proportionally adequate liquidity can produce execution-risk (worse fills, wider stops, hostile slippage on adverse moves). A future feasibility memo must:

- estimate top-of-book depth at production sizing;
- estimate behavior under stressed regimes (e.g., during exchange-wide deleveraging events);
- estimate whether the project's §1.7.3 locks (0.25% risk; 2× leverage; one position max) leave headroom for adverse fills.

Liquidity / execution-risk failure is HARD REJECT for the symbol.

### F. Wick / stop-pathology gate

Alt symbols may have higher headline volatility but proportionally worse wick risk. The Phase 3s Q2 5m diagnostic established that V1-family stop exits had wick-fractions of 0.571–1.000 on BTC; alt symbols may be worse. A future feasibility memo must:

- estimate per-symbol wick-fraction distribution on adverse stop exits;
- distinguish "healthy directional expansion" (move sustained beyond stop) from "stop-hostile noise" (move retraced after stop trigger);
- consider whether `stop_trigger_domain` choices (Phase 3v §8 governance preserved) interact differently with alt-symbol wick patterns than with BTC wick patterns.

Excessive wick / stop-hostility failure is HARD REJECT for the symbol on the candidate strategy's geometry.

### G. Idiosyncratic-risk gate

Alt symbols may be more affected by:

- **News events** (regulatory action; venue-listing changes; legal proceedings).
- **Token unlocks / vesting schedules.**
- **Regulatory events** (jurisdiction-specific actions affecting individual tokens).
- **Chain outages** (e.g., SOL has historical outage events; project has not independently audited).
- **Ecosystem shocks** (protocol exploits; oracle failures; bridge incidents).
- **Social-driven flows** (DOGE-style meme-driven volatility; coordinated retail flows).

A future feasibility memo must explicitly discuss per-symbol idiosyncratic-risk profile as a structural risk. **Idiosyncratic events are NOT to be treated as tradable signal** for any future strategy candidate (this would be event-trading, which is out of v1 scope per `.claude/rules/prometheus-core.md`).

### H. Governance-label compatibility gate

Future symbol research must preserve all four governance label schemes verbatim:

- `stop_trigger_domain` (Phase 3v §8): `trade_price_backtest` | `mark_price_runtime` | `mark_price_backtest_candidate`; `mixed_or_unknown` invalid and fails closed.
- `break_even_rule` (Phase 3w §6): `disabled` | `enabled_plus_1_5R_mfe` | `enabled_plus_2_0R_mfe` | `enabled_<other_predeclared>`; `mixed_or_unknown` invalid and fails closed.
- `ema_slope_method` (Phase 3w §7): `discrete_comparison` | `fitted_slope` | `other_predeclared` | `not_applicable`; `mixed_or_unknown` invalid and fails closed.
- `stagnation_window_role` (Phase 3w §8): `not_active` | `metric_only` | `active_rule_predeclared`; `mixed_or_unknown` invalid and fails closed.

Future symbol research must also preserve:

- Phase 3r §8 mark-price gap governance (per-trade exclusion only for Q6-equivalent diagnostics; no patching, forward-fill, interpolation, or imputation).
- Phase 4j §11 metrics OI-subset partial-eligibility rule (if metrics OI is used; per-bar exclusion algorithm restated verbatim; optional ratio columns forbidden).
- §11.6 = 8 bps HIGH per side; §1.7.3 0.25% / 2× / one-position-max / mark-price stops.

A future symbol candidate that requires governance-label amendment is HARD REJECT.

## 7. Can Prior Strategies Be Improved?

**Direct rescue is not recommended.** Phase 4aa's answer to "can prior strategies be improved on alt symbols?" is carefully delimited:

- **Direct rescue is forbidden.** Re-evaluating R3 / R2 / F1 / D1-A / V2 / G1 / C1 on SOL / XRP / ADA (or any alt symbol) without first establishing a new theoretical case is **retrospective rescue**, which is forbidden by Phase 4m §"Forbidden rescue observations", Phase 4s §"Forbidden cross-strategy rescue", and Phase 4y §"Forbidden cross-strategy rescue interpretations". Phase 4aa preserves these prohibitions.
- **Prior strategies inform negative constraints, not positive starting points.** The six-failure topology (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism / framework mismatch; V2 design-stage incompatibility; G1 regime-gate sparseness; C1 fires-and-loses) is a constraint set for future research, not a template set. Future alt-symbol candidates must avoid the failure modes; they must not be designed to "fix what BTC didn't allow."
- **Prior diagnostic findings (Phase 3s Q1–Q7) may not be converted into post-hoc rules.** The Phase 3o §6 forbidden question forms and Phase 3t §14.2 prohibition on converting Q1–Q7 findings into rule candidates are preserved.
- **Future strategy work must be genuinely ex-ante.** Any future alt-symbol candidate must clear the Phase 4m 18-requirement validity gate verbatim, including requirement #1 (named as new hypothesis, not rescue label), requirement #2 (specified before any data is touched), requirement #3 (new in theory, not parameter tweak), and requirement #9 (NOT choose thresholds from prior failed outcomes).
- **A future alt-symbol candidate must not be "R3 on SOL" or "G1 with looser thresholds for higher-volatility symbols."** Any candidate of this form fails the design-family-distance check (Phase 4z proposed as recommendation; Phase 4aa records the principle): it would be the same design family as a rejected strategy with a parameter tweak (the symbol). This is forbidden.
- **A future alt-symbol candidate must clear an elevated design-family-distance review.** The candidate must declare its design family (F-1 / F-2 / F-3 / F-4 or new), declare its closest rejected strategy in the family, and explain why it is not that strategy in disguise. A new theoretical justification is required; same justification + different symbol is not a new theoretical justification.

**The valid path:** future alt-symbol research means *new* hypotheses that are theoretically distinct from R3 / R2 / F1 / D1-A / V2 / G1 / C1 *and* may benefit from running on a different symbol substrate. The order is: (1) admissibility framework applied to candidate symbols; (2) docs-only data-requirements / feasibility memo; (3) docs-only acquisition phase; (4) docs-only fresh-hypothesis discovery memo on the now-admissible substrate; (5) docs-only hypothesis-spec memo; (6) docs-only strategy-spec memo; (7) docs-only backtest-plan memo; (8) backtest execution. Each step requires separate operator authorization. **Phase 4aa authorizes none of these.**

## 8. What Would a Future Data Phase Need?

If the operator ever separately authorizes a future data phase (NOT authorized by Phase 4aa), it would likely take the form of:

```text
Potential future Phase 4ab — Alt-Symbol Public Data Feasibility / Acquisition Plan
```

(The name `Phase 4ab` is a placeholder; the operator may choose a different name. Phase 4aa does NOT name this phase as authorized; it only frames what such a phase *would* look like if ever authorized.)

### Constraints any future data phase must honor

**Phase 4aa explicitly states:**

- **Not authorized by Phase 4aa.** Phase 4aa only describes what such a phase *would* require; it does not start the phase.
- **Would require separate operator approval.** The operator decides whether and when to authorize a future data phase.
- **Would need predeclared symbol list.** A future authorization brief must lock the symbol list (e.g., from Section 4 above) before the phase begins.
- **Would need predeclared intervals.** A future authorization brief must lock the kline intervals (e.g., 15m / 30m / 1h / 4h) and any non-kline data families (funding / mark-price / metrics) before the phase begins.
- **Would need public unauthenticated data only** unless separately authorized otherwise. Continuing the project's Phase 3q / Phase 4i pattern: `data.binance.vision` bulk archives; no credentials; no authenticated REST; no private endpoints; no user stream; no WebSocket; no listenKey lifecycle; no `.env`; no MCP / Graphify / `.mcp.json`.
- **Would need strict integrity gates.** Phase 3p §4.7 strict integrity rules preserved verbatim per dataset; no forward-fill; no interpolation; no imputation; no patching; no silent omission. Any partial-pass outcome would be subject to the same governance pattern as Phase 4i metrics OI-subset (Phase 4j §11) — i.e., a future docs-only governance memo would be required *after* the acquisition, *before* any strategy spec uses the dataset.
- **Would NOT run backtests.** A future data phase would be docs-and-data only (analogous to Phase 3q for 5m supplemental data and Phase 4i for V2 supplemental data), with the docs-and-data outputs strictly bounded to acquisition + manifests + integrity validation. Backtest execution remains a separately authorized phase.

### Suggested future minimal data scope (NOT authorized)

If a future Phase 4ab were authorized, suggested minimum scope based on the project's prior Phase 4i pattern *might* include:

- **Standard trade-price klines** for selected alt symbols at one or more intervals (e.g., 15m / 30m / 1h / 4h depending on the future research question).
- **Funding rate history** for selected alt symbols.
- **Mark-price klines** if needed for stop-trigger-domain comparison (Phase 3p / Phase 3q precedent: mark-price acquisition has produced known invalid-window outcomes that require Phase 3r §8 governance handling; Phase 4ab would inherit this risk).
- **Metrics / open-interest data** ONLY if needed for a future hypothesis and ONLY with strict eligibility rules learned from Phase 4i / Phase 4j (the `metrics` family is globally `research_eligible: false`; OI subset is per-bar partial-eligible per Phase 4j §11; optional ratio columns remain forbidden). A future Phase 4ab should default to NOT acquiring metrics unless a future hypothesis explicitly requires OI features.

The suggested scope is **a recommendation for what such a phase might consider**, not adopted scope. The operator decides at the time of authorization. Phase 4aa explicitly does NOT lock any future scope.

## 9. Research Decision Menu

Phase 4aa offers the following operator decision menu. Each option represents a possible next step; the operator decides which (if any) to authorize. **Phase 4aa does NOT authorize any of these options; each requires separate operator authorization.**

### Option A — Remain paused

Always procedurally valid. The strongest-evidence position remains unchanged after Phase 4aa: six terminal negative strategy outcomes versus two positive anchors (H0, R3) and two retained-research-only positions (R1a, R1b-narrow). Adding a market-substrate question to the research record does not by itself produce strategy evidence; the operator may choose to remain paused for any duration.

### Option B — Future docs-only alt-symbol data-requirements / feasibility memo

Recommended (as conditional secondary) if Phase 4aa concludes alt-symbol research is worth examining further but needs stricter dataset planning first. This option would be docs-only, would not acquire data, would not name a strategy, and would not authorize a backtest. It would translate Section 6's admissibility framework into a concrete feasibility plan for the Section 4 candidate symbol universe.

### Option C — Future public data acquisition for predeclared alt-symbol set

Acceptable only **after** a Section 4 symbol set and Section 6 admissibility-derived data requirements are docs-only finalized in a separately authorized memo. This option would be docs-and-data (analogous to Phase 3q / Phase 4i) with strict integrity gates preserved. **No backtests.** No strategy spec.

### Option D — Future ex-ante strategy-family discovery memo for admitted symbols

Only after symbol substrate feasibility is clearer (Option B and / or Option C completed). This option would be docs-only and would clear the Phase 4m 18-requirement validity gate verbatim, with elevated design-family-distance review per the Phase 4z proposed pattern. The discovery memo would name candidate hypotheses; it would not name a strategy or a backtest plan.

### Option E — Direct old-strategy improvement / rescue

**Not recommended.** Re-evaluating R3 / R2 / F1 / D1-A / V2 / G1 / C1 on alt symbols is retrospective rescue and is forbidden by accumulated governance. Phase 4aa explicitly does NOT recommend this option.

### Option F — Spot / options / COIN-M / other venue expansion

**Not recommended now.** Per Section 5, expanding market type and symbol substrate simultaneously contaminates attribution. Future market-type expansion (if ever considered) should be a separately scoped research direction with its own governance.

### Option G — Paper / shadow / live-readiness / exchange-write

**Forbidden / not authorized.** No validated strategy candidate exists. `docs/12-roadmap/phase-gates.md` requires strategy evidence before paper / shadow / live readiness; the project does not have it. Production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write all remain unauthorized.

## 10. Recommendation

```text
Primary recommendation:
Proceed next, if operator authorizes, with a docs-only alt-symbol data-requirements
and feasibility memo (Option B).

Do not backtest yet.
Do not acquire data yet unless separately authorized.
Do not rescue prior strategies.
Do not expand market type yet.
Keep research on Binance USDⓈ-M perpetuals for clean attribution.
```

**Phase 4aa primary recommendation: Option B — Future docs-only alt-symbol data-requirements and feasibility memo (only if separately authorized).** This option translates Phase 4aa's admissibility framework (Section 6) into concrete future-feasibility requirements for the candidate symbol universe (Section 4), preserves all retained verdicts and project locks, and does not authorize any data acquisition, backtest, strategy spec, or implementation.

**Phase 4aa secondary acceptable: Option A — Remain paused.** Always procedurally valid. The operator may choose to defer Option B authorization for any duration.

**Phase 4aa NOT recommended:**

- **Option C — direct public data acquisition** — premature; Option B should establish requirements first.
- **Option D — direct ex-ante strategy-family discovery memo** — premature; substrate feasibility (Option B and/or C) should establish whether alt symbols are admissible before strategy work resumes.
- **Option E — direct old-strategy improvement / rescue** — forbidden by accumulated governance.
- **Option F — market-type expansion** — premature; one independent variable per research step.

**Phase 4aa FORBIDDEN:**

- **Option G — paper / shadow / live / exchange-write** — no validated strategy exists; phase-gate requirements not met.

## 11. Preserved Locks and Boundaries

Phase 4aa preserves every retained verdict and project lock verbatim. **No verdict is revised. No project lock is changed. No governance file is amended.**

```text
H0           : FRAMEWORK ANCHOR (preserved)
R3           : BASELINE-OF-RECORD (preserved)
R1a          : RETAINED — NON-LEADING (preserved)
R1b-narrow   : RETAINED — NON-LEADING (preserved)
R2           : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1           : HARD REJECT (preserved)
D1-A         : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
5m thread    : OPERATIONALLY CLOSED (Phase 3t; preserved)
V2           : HARD REJECT — terminal for V2 first-spec
                (Phase 4l — Verdict C; CFP-1 critical;
                preserved)
G1           : HARD REJECT — terminal for G1 first-spec
                (Phase 4r — Verdict C; CFP-1 critical binding;
                CFP-9 independent; preserved)
C1           : HARD REJECT — terminal for C1 first-spec
                (Phase 4x — Verdict C; CFP-2 binding;
                CFP-3 / CFP-6 co-binding; preserved)

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
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x / 4y / 4z
                            : all preserved verbatim
Phase 4z recommendations    : remain recommendations only;
                              NOT adopted as binding governance by
                              Phase 4aa
Phase 4aa                   : Alt-symbol market-selection and strategy-
                              admissibility memo (this phase; new;
                              docs-only; feature-branch only;
                              proposes admissibility framework as
                              recommendation only)
```

## 12. Explicit Non-Authorization Statement

Phase 4aa does NOT authorize:

- **Data acquisition** (no symbol; no interval; no funding history; no mark-price; no metrics; no aggTrades; no spot; no cross-venue; no order book).
- **Data modification** (no patching; no forward-fill; no interpolation; no imputation; no replacement; no regeneration).
- **Manifest creation** (no new manifests under `data/manifests/`).
- **Manifest modification** (existing manifests unchanged).
- **Backtests** (none of any kind).
- **Diagnostics** (no Q1–Q7 rerun; no new diagnostic phase).
- **Strategy specs** (no candidate named; no strategy spec authored).
- **Implementation** (no `src/prometheus/` modification; no test modification; no script modification; no script creation; no runtime code).
- **Old-strategy rescue** (no R3 / R2 / F1 / D1-A / V2 / G1 / C1 rescue; no R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any hybrid).
- **Paper / shadow / live operation.**
- **Live-readiness** (Phase 4 canonical not authorized; phase-gate requirements not met).
- **Deployment.**
- **Production-key creation.**
- **Authenticated APIs.**
- **Private endpoints.**
- **User stream / WebSocket / listenKey lifecycle.**
- **Exchange-write capability.**
- **MCP tooling.**
- **Graphify tooling.**
- **`.mcp.json` creation or modification.**
- **Credentials** (no `.env`; no key storage; no key request).
- **Successor phase** (Phase 4ab / Phase 5 / Phase 4 canonical / any other named successor remains unauthorized).
- **Adoption of Phase 4z recommendations as binding governance** (Phase 4z recommendations remain recommendations only; adoption requires a separately authorized governance-update phase).

**Phase 4aa does NOT modify:**

- source code under `src/prometheus/`;
- tests;
- scripts (no modification of `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, or `scripts/phase4x_c1_backtest.py`; no new script created);
- data under `data/raw/`, `data/normalized/`, or `data/manifests/`;
- existing strategy specifications (`docs/03-strategy-research/v1-breakout-strategy-spec.md` and related are preserved verbatim);
- governance files (`docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, or any specialist governance document — except the narrow `docs/00-meta/current-project-state.md` update required to record Phase 4aa);
- project locks, retained verdicts, or any prior phase's substantive content.

**Phase 4aa output:**

- `docs/00-meta/implementation-reports/2026-05-04_phase-4aa_alt-symbol-market-selection-admissibility.md` (this memo);
- `docs/00-meta/implementation-reports/2026-05-04_phase-4aa_closeout.md` (closeout);
- narrow update to `docs/00-meta/current-project-state.md` recording Phase 4aa (no broad documentation refresh).

**Phase 4aa is preserved on its feature branch unless and until the operator separately instructs a merge.** main remains unchanged at `6fb0c6c8ab0e634684a80e7b339c9c96f3a56b02` after Phase 4aa branch creation.

---

**Phase 4aa is text-only. No source code, tests, scripts, data, manifests, governance files, retained verdicts, or project locks were created or modified. Phase 4aa frames the alt-symbol substrate question and proposes an admissibility framework as a recommendation for any future docs-only data-requirements memo. Phase 4aa does NOT authorize data acquisition, backtest, strategy spec, implementation, paper / shadow / live operation, exchange-write, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, or any successor phase. C1 first-spec remains terminally HARD REJECTED. V2 / G1 / R2 / F1 / D1-A all preserved per accumulated governance. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. R1a / R1b-narrow remain RETAINED — NON-LEADING. Phase 4z recommendations remain recommendations only. Recommended state: remain paused (primary); Option B docs-only alt-symbol data-requirements memo (conditional secondary; not authorized by Phase 4aa). No next phase authorized.**
