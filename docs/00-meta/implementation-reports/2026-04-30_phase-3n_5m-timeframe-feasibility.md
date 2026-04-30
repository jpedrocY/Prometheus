# Phase 3n — 5m Timeframe Feasibility / Execution-Timing Memo (docs-only)

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2p §C.1 (R3 baseline-of-record); Phase 2x family-review memo (V1 breakout family at useful ceiling under current framework); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved); Phase 2w §16.1 (R2 FAILED — §11.6 cost-sensitivity blocks); Phase 3d-B2 (F1 HARD REJECT); Phase 3e post-F1 research consolidation memo (remain-paused recommendation); Phase 3j (D1-A MECHANISM PASS / FRAMEWORK FAIL — other; Phase 3j terminal for D1-A under current locked spec); Phase 3k post-D1-A research consolidation memo (remain-paused primary recommendation); Phase 3l external execution-cost evidence review (primary assessment B — current cost model conservative but defensible; §11.6 unchanged pending stronger evidence); Phase 3m regime-first research framework memo (remain-paused primary recommendation); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `docs/04-data/timestamp-policy.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3n — Docs-only **5m timeframe feasibility / execution-timing memo.** Evaluates whether 5m data could help Prometheus learn from prior 15m-strategy failures as an *execution / timing diagnostics* layer, without authorizing 5m strategy signals, 5m data download, v003 dataset creation, implementation, or backtesting.

**Branch:** `phase-3n/5m-timeframe-feasibility`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No prior verdict revised. No data downloaded. No v003 dataset created.** R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained research evidence. R2 remains FAILED. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. §11.6 = 8 bps HIGH per side preserved. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal. **Mindset principle:** *Paused means "pause strategy execution," not "pause learning."* Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3n is deciding

Phase 3n is a docs-only feasibility memo — *not* a strategy memo, *not* a data-acquisition memo, *not* a regime memo, and *not* an implementation memo.

The project has now completed three strategy-research arcs (V1 breakout, F1 mean-reversion, D1-A funding-aware) under disciplined Phase 2f Gate-1 thresholds, and Phase 3l confirmed the cost model is conservative but defensible. Phase 3m recommended "remain paused" as primary while documenting regime-first as a possible (not authorized) future direction. The operator-introduced question in this phase is narrower and more specific:

> Would access to *finer* market-data granularity (5-minute OHLCV) help us **understand WHY 15m strategies failed** — not by inventing a 5m strategy, but by giving the future operator additional *diagnostic visibility* into intrabar trade paths, stop triggers, target touches, fill timing, and cost behavior?

Phase 3n weighs the *potential value* of 5m diagnostics against the *potential harms* (overfitting, false precision, cost amplification, signal-frequency explosion, data complexity, and the temptation to slide from "diagnostics" into "5m strategy variants"). The output is a written assessment of whether and how 5m could be *cautiously* used as a diagnostics layer in a possible future docs-only data/planning phase, plus a single recommended next operator decision.

Phase 3n is **NOT**:

- Authorizing 5m strategy signals or any 5m strategy family.
- Authorizing 5m data download.
- Authorizing v003 dataset creation.
- Authorizing 5m derived-table creation.
- Authorizing rerun of H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A or any controls.
- Authorizing reclassification or rescue of R2, F1, or D1-A.
- Authorizing parameter tuning, threshold revision, project-lock revision, or prior-verdict revision.
- Authorizing regime-first implementation, ML feasibility memo, formal cost-model revision, hybrid spec, or new strategy-family discovery.
- Authorizing paper/shadow planning, Phase 4 runtime / state / persistence work, live-readiness, deployment, production-key creation, or exchange-write capability.
- Enabling MCP, Graphify, `.mcp.json`, credentials, authenticated Binance APIs, or any data/ commits.

Phase 3n **IS**:

- A docs-only memo that documents (a) the four distinct *roles* 5m could play (signal layer / diagnostics layer / regime input / paper-shadow execution-realism tool); (b) for each prior failed candidate, what 5m *might* explain about *why* the failure occurred; (c) a candidate diagnostic question set; (d) the risks of 5m work, especially the slippery slope from diagnostics to signal; (e) data-requirements considerations (v002 vs v003, manifest discipline, immutability); (f) anti-overfitting guardrails any future 5m phase would need to predeclare; (g) the relationship to regime-first and ML; (h) the relationship to paper/shadow and Phase 4; and (i) a single recommended next operator decision.

The output is a consolidated 5m-thinking record + a single forward-looking operator decision recommendation. **Phase 3n produces a memo; the operator decides whether to authorize anything downstream.**

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
| **Phase 3l external cost-evidence review** | Merged; primary assessment **B — current cost model conservative but defensible**; §11.6 = 8 bps HIGH per side **preserved unchanged pending stronger evidence**. |
| **Phase 3m regime-first framework memo** | Merged; primary recommendation: **remain paused**; formal regime-first spec / planning memo *not* started by Phase 3m. |
| **§1.7.3 project-level locks** | Preserved verbatim. |
| **Phase 2f thresholds (incl. §11.6 = 8 bps HIGH per side)** | Preserved verbatim. |
| **v002 datasets** | Locked. 15m + 1h-derived + 15m mark-price + funding-event tables for BTCUSDT and ETHUSDT. **No 5m datasets exist; no v003 created.** |
| **Paper/shadow planning** | Not authorized. |
| **Phase 4 work** | Not authorized. |
| **Live-readiness / deployment / production-key / exchange-write work** | Not authorized. |
| **MCP / Graphify / `.mcp.json` / credentials** | Not activated; not requested; not used. |

The next operator decision is operator-driven only. Phase 3n does not pre-empt that decision; this section records the state on which any future decision must build.

---

## 3. Why 5m is being considered

5m is being considered explicitly **for diagnostic learning, not for strategy invention**. The motivating principle is:

> *Pausing strategy execution does not require pausing learning.*

Three failed candidates (R2, F1, D1-A) all showed *some* mechanism support but failed framework discipline for different reasons. The current 15m-only evidence base does **not** distinguish between several plausible failure narratives:

- **Signal failure.** The setup itself is wrong — there is no edge to extract regardless of execution timing.
- **Execution-timing failure.** The setup might have edge, but completed-15m-bar timing causes us to enter or exit at the wrong intrabar moment.
- **Stop-trigger failure.** Stops might be triggered by short-lived 5m noise rather than sustained invalidation.
- **Target-path failure.** Trades might touch profit targets intrabar before reversing — visible in 5m, invisible in 15m.
- **Decay-window failure.** Effects (such as D1-A's funding-extreme contrarian impulse) might decay on a sub-15m timescale.
- **Cost asymmetry.** Real fills inside a 15m bar might be systematically worse (or better) than the next-bar-open assumption.

15m closes alone *cannot* discriminate between these narratives. 5m data *might*. That is the *only* reason to consider 5m at this point — not to build a 5m strategy.

5m is **not** being considered to:

- Rescue R2, F1, or D1-A. Their verdicts are terminal under current locked spec.
- Bypass §11.6. Cost discipline remains preserved verbatim.
- Bypass the "completed bars only" rule. Any future 5m diagnostics work must still respect strategy-decision discipline; 5m would inform *understanding*, not *signal*.
- Increase data noise we trade on. The relevant question is exactly the opposite: would 5m mostly add overfitting risk, or would it expose specific mechanism evidence we cannot otherwise see?

The honest answer is: **we do not yet know**. Phase 3n is the docs-only artifact that frames the question rigorously enough that a future operator decision can be made on principle, not on impulse.

---

## 4. The four distinct roles 5m could play

5m is not one thing. Conflating its possible roles is the single biggest risk in this conversation. Phase 3n distinguishes four:

### 4.1 5m as strategy signal layer

**Definition:** Use 5m completed bars as the entry/exit timing for new or existing strategy families (e.g. a "5m breakout", a 5m re-entry of D1-A, an F1 variant on 5m).

**Recommendation:** **Dangerous now. Not authorized. Strongly discouraged for the foreseeable future.**

**Why:**

- 3× signal-frequency increase (4 × 5m bars per 15m bar). Without dramatically higher per-trade edge, signal frequency directly amplifies any negative edge — exactly the failure mode F1 demonstrated catastrophically (high frequency × negative edge per trade = catastrophic compound loss).
- §11.6 cost-resilience gate becomes *much* harder to pass at 5m: 4× the trade count at the same fee + slippage assumptions ≈ 4× the cost burden in absolute terms. Phase 3l confirmed the cost model is conservative but defensible *for 15m*; we have no equivalent confidence at 5m.
- Increases overfitting surface. 4× more bars = 4× more potential parameter combinations = sharply reduced statistical power per fold.
- Tempts implicit rescue framing: "F1 failed at 15m but might work at 5m" is exactly the kind of post-hoc loosening Phase 2y §11.3.5 forbids.

### 4.2 5m as execution / timing diagnostics layer

**Definition:** Use 5m bars **only** to *describe what happened inside* a 15m trade after the 15m strategy already decided to enter or exit. Produce read-only diagnostics tables, not new entry signals.

**Recommendation:** **Possible later as a docs-only spec memo, then later as a docs-only data/planning memo, then later (much later) as a non-strategy-affecting analytical artifact.** *Not authorized now.* The pre-conditions are extensive (§9 of this memo); the value is non-zero but bounded.

**Why diagnostics-only might be defensible later:**

- It is *informational*, not *executional*. A diagnostic finding cannot directly cause a trade.
- It can falsify or support specific hypotheses about *why* a 15m strategy failed, which is genuinely useful evidence.
- It does not require trading 5m, holding 5m positions, or building a 5m signal pipeline.
- It can be cleanly version-fenced (v003 supplemental) without contaminating v002-based verdicts.

**Why even diagnostics is dangerous and gated:**

- The slippery slope from "diagnostic evidence" to "candidate signal" is psychologically real and historically well-documented.
- Intrabar visibility creates the *illusion* of post-hoc precision (e.g. "we *would have* hit +1R intrabar before exiting at −1R") that can lead to ad-hoc exit-rule rescues — a forbidden post-hoc loosening pattern.
- Predeclared diagnostic questions are the only defense; without predeclaration, diagnostics becomes data dredging.

### 4.3 5m as regime-classification input

**Definition:** Feed 5m derived statistics (e.g. realized vol on 5m, 5m chop, 5m volume profile) into a regime-classification framework that conditions which 15m strategy applies when.

**Recommendation:** **Possible later, but should NOT be the *first* regime-classifier.** Phase 3m's regime-first caution still applies; *if* a regime-first phase is ever authorized, the *first* candidate axes should be observable on existing v002 data (15m vol, 1h vol, funding stress, BTC-ETH covariance, time-of-day). 5m as regime input is a downstream enhancement, not a prerequisite.

**Why downstream:**

- Adding 5m as the *first* regime axis simultaneously introduces three new degrees of freedom (which regime axis, which threshold, which 5m derived statistic) — too many uncontrolled variables for early regime work.
- 5m-derived regime statistics are noisier than 1h-derived ones at the same lookback, increasing label-instability risk.

### 4.4 5m as future paper/shadow execution-realism tool

**Definition:** Use 5m bars (and intrabar tick or sub-minute data, if eventually obtained) to validate that paper/shadow simulated fills *match* what a real exchange would have done within a 15m bar window — including stop-trigger reality, slippage realism, and partial-fill behavior.

**Recommendation:** **Possible much later — only if/when paper/shadow is ever authorized (Phase 7 territory in `phase-gates.md`). Not relevant to the current paused state.**

**Why later:**

- Paper/shadow is itself unauthorized (Phase 7).
- Execution-realism testing is downstream of strategy evidence; it cannot precede strategy authorization.
- 5m alone is probably insufficient for this role anyway — paper/shadow execution realism likely needs sub-minute or tick data, which is its own discussion.

### 4.5 Summary table

| Role | Recommended now? | Possible later? | Conditional on |
|------|------------------|-----------------|----------------|
| Signal layer | **No (dangerous)** | Strongly discouraged | Would require formal reclassification of project framework discipline |
| Diagnostics layer | **No (not authorized)** | Yes, with strict guardrails | Future docs-only spec memo + data/planning memo + predeclared question set |
| Regime input | **No (premature)** | Yes, as downstream regime axis | Future regime-first authorization first; 5m comes after 15m/1h regime axes |
| Paper/shadow execution realism | **No (out of scope)** | Yes, much later | Phase 7 paper/shadow authorization |

---

## 5. Prior-failure mapping — what 5m diagnostics *might* explain

For each prior failed candidate, this section names the **specific failure-mode hypotheses** that 5m diagnostics might help discriminate. Each hypothesis is tagged **STRONG / MODERATE / WEAK / SPECULATIVE** to indicate prior probability the hypothesis is *worth investigating* if a future 5m diagnostics phase is ever authorized. This is *not* a finding — no diagnostics have been run.

### 5.1 V1 / R3 (V1 breakout, baseline-of-record)

R3 is the strongest candidate the project has produced (Phase 2p §C.1 PROMOTE — broad-based) but still produces aggregate-negative net-of-cost expR on R-windows. 5m diagnostics might help discriminate:

- **MODERATE — Immediate adverse excursion (IAE) in the first 5–15 minutes after a 15m next-bar-open entry.** If R3 trades systematically suffer significant adverse path movement in the *first* 5m bar after entry, this is consistent with breakouts often being "front-run" or buying into the immediate post-breakout pullback. 5m would show this clearly; 15m hides it.
- **MODERATE — Stop-trigger sourced from short 5m noise vs sustained invalidation.** R3 stops are structural+ATR. If many stops are hit by a single 5m wick that is reversed within 5–10 minutes, that is a different failure pattern than a stop being hit by sustained directional invalidation. The two have different remediation implications (and reminder: stop *widening* is forbidden in v1; this is diagnostic, not prescriptive).
- **WEAK — Intrabar +1R / +2R touch before stop.** R3 uses Fixed-R take-profit + 8-bar time-stop. Did some 15m losers actually touch profit thresholds intrabar? If yes, this is *only* useful as evidence about target-path realism, *not* as a rescue mechanism (post-hoc target rescue is forbidden).
- **SPECULATIVE — Next-bar-open assumption quality.** Is the actual 5m fill within the 15m next-open bar materially better or worse than the bar-open print? Phase 3l found the cost model conservative but defensible at 15m granularity; 5m visibility could either confirm or refine that.

### 5.2 R2 (V1 breakout pullback-retest entry)

R2 PROMOTED at MED slippage with M1 + M3 mechanism support but FAILED §11.6 at HIGH slippage (BTC Δexp_H0 −0.014 sub-threshold; ETH Δexp_H0 −0.230 catastrophic). 5m diagnostics might help discriminate:

- **STRONG — Pullback-fill timing within the 15m entry bar.** R2's edge depends on *where in the 15m bar* the pullback fill happens. If the 5m bar containing the fill systematically shows the price already moving away (giving a worse intrabar fill), that explains §11.6 cost-fragility. If the 5m fill is typically "clean" (mid-bar consolidation), the §11.6 fragility is not a fill-timing problem.
- **MODERATE — Stop-trigger sensitivity at HIGH slippage.** R2's structural stops at HIGH slippage become disproportionately sensitive. 5m would show whether HIGH-slippage stop hits are 5m-noise events (briefly violated then reversed) or sustained invalidation events.
- **WEAK — Cost amplification from intrabar partial-fill scenarios.** Is the slippage cost concentrated in *specific* 5m windows of the 15m entry bar? This is about cost-model realism, not strategy rescue.

**Important:** 5m diagnostics about R2 *cannot* unblock R2's §11.6 verdict. R2 remains FAILED. 5m evidence about R2 would only be useful if (a) the operator separately authorized a formal cost-model revision phase *and* (b) 5m diagnostics produced strong falsifying evidence against the §11.6 model. That double-conditional bar is intentionally high.

### 5.3 F1 (mean-reversion-after-overextension)

F1 HARD REJECTED on Phase 3c §7.3 catastrophic-floor predicate (5 violations across BTC/ETH × MED/HIGH). Mean +0.024 R below +0.10 threshold; 53–54% STOP exits at −1.30 / −1.24 R mean. 5m diagnostics might help discriminate:

- **MODERATE — Post-entry path of the 53–54% STOP exits.** Did STOP-exiting F1 trades move *immediately* against entry (within the first 5m), or did they show initial favorable movement that reversed? Different paths suggest different mechanism failures (entry-timing vs holding-period).
- **MODERATE — Intrabar TARGET touches in STOP-exiting trades.** F1's TARGET subset shows mean +1.86 R per trade when isolated. Did *some* STOP exits touch the TARGET intrabar before reversing to STOP? This is similar to the R3 hypothesis — useful as path evidence, *not* as rescue justification. F1 remains HARD REJECT regardless of any intrabar target-touch finding.
- **MODERATE — 8-bar time-stop interaction with 5m volatility regime.** Did F1 8-bar time-stop exits coincide with high or low 5m realized volatility windows? This bears on whether the time-stop is mis-calibrated to the underlying volatility regime — a regime-conditioning question more than a 5m question.
- **WEAK — Cumulative-displacement signal precision at 5m.** Would a 5m-resolution view of the 8-bar cumulative displacement reveal that F1 entries are systematically taken at *late* moments in the displacement (after the impulse already exhausted)? This is the kind of question that *sounds* useful but is the most likely to slip into "5m F1 variant" thinking — it must be predeclared as diagnostic-only or not investigated.

**Important:** F1's HARD REJECT is *terminal*. No 5m diagnostics finding can revive F1 under current locked spec.

### 5.4 D1-A (funding-aware directional / carry-aware contrarian)

D1-A MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3j). M1 BTC PASS; M2 FAIL on both symbols (~21× / ~11× below threshold); M3 PASS-isolated; empirical WR ~30–31% vs forecast +51% breakeven; 67–68% STOP exits at −1.24 / −1.30 R mean. 5m diagnostics might help discriminate:

- **STRONG — Funding-extreme decay window.** The single most informative diagnostic question for D1-A is: *over what timescale does the funding-extreme contrarian impulse decay*? If the decay is sub-15m (e.g. mean-revert mostly within 5–15 minutes of the funding settlement), then D1-A's 32-bar (8-hour) holding-period assumption is fundamentally mismatched to the underlying mechanism. 5m would clearly show this; 15m cannot.
- **STRONG — Path of the 67–68% STOP exits.** Did D1-A losers move against immediately after entry (suggesting bad entry timing or reverse-fading momentum), or did they show initial favorable mean-reversion that reversed within hours (suggesting mean-reversion that didn't compound)? These two paths imply very different failure mechanisms.
- **MODERATE — Stop-distance validity at the 32-bar horizon.** D1-A uses 1.0 × ATR(20) on 15m. At 32 bars (8 hours), the structural-stop distance may or may not be appropriate to the realized volatility *over that horizon*. 5m vs 15m vs 1h ATR comparisons could falsify or support this.
- **MODERATE — TARGET subset path realism.** D1-A TARGET subset BTC mean +2.143 R / ETH +2.447 R when isolated. Did TARGET-exit trades reach +2.0 R quickly (within first few hours) or only at the time-stop? This affects whether D1-A's edge is concentrated in fast or slow mean-reversion.
- **WEAK — Per-funding-event cooldown realism.** Did the cooldown rule allow re-entry at moments where the underlying funding-stress had already partially decayed?

**Important:** D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict is *terminal under current locked spec*. No 5m diagnostics finding can revive D1-A without separate operator authorization for a successor (D1-A-prime or similar), which is *not* contemplated by Phase 3n.

### 5.5 Cross-candidate observation

The single highest-value 5m diagnostic question across all four candidates is the same: **What is the intrabar adverse-excursion path of losing trades within the first 5–15 minutes after entry?** If this is uniformly hostile (immediate-against-entry within first 5m), it suggests a structural entry-timing problem common to all 15m-completed-bar entries — a finding that would *inform* the regime-first conversation but would *not* directly authorize any strategy or rescue.

The single highest *risk* 5m question is: *did losing trades touch profit targets intrabar*? This question is only safe to ask if predeclared as diagnostic-only with explicit prior commitment that no rescue exit-rule will be derived from any answer. Otherwise it becomes the textbook post-hoc loosening pattern.

---

## 6. Candidate diagnostic question set

Any future 5m-diagnostics phase should *predeclare* its question set before generating any data. The following is a candidate question list, *not* a final list, ordered approximately by value/risk ratio (highest value, lowest risk first):

1. **Did losing trades move adversely against entry within the first 5–15 minutes after a 15m next-bar-open entry?** Useful for discriminating "bad entry timing" from "bad signal." (HIGH VALUE, LOW RISK — purely descriptive.)
2. **Were stops triggered by short-lived 5m noise (single-wick events reversed within 5–10 minutes) or by sustained invalidation (price stays beyond stop level for ≥3 consecutive 5m bars)?** Useful for understanding stop-trigger pathology. (HIGH VALUE, LOW RISK — purely descriptive; cannot license stop widening.)
3. **For D1-A specifically: did the funding-extreme effect decay within 5, 10, 15, 30, or 60 minutes after the funding settlement event?** Most informative single diagnostic question available for D1-A. (HIGH VALUE, LOW RISK if D1-A is permanently retired; MEDIUM RISK if D1-A-prime is contemplated.)
4. **For R3 / R2 / F1 / D1-A: did losing trades touch +1R or +2R intrabar before exiting against?** (MEDIUM VALUE, HIGH RISK — must be predeclared as diagnostic-only with explicit no-rescue commitment; otherwise becomes post-hoc loosening.)
5. **Would 5m show that 15m next-bar-open fills are materially optimistic or conservative compared to a probability-weighted 5m fill simulation?** Useful for cost-model realism review. (MEDIUM VALUE, MEDIUM RISK — only relevant if a separate cost-model revision phase is ever authorized.)
6. **Would 5m help distinguish *execution timing failure* from *signal failure* — i.e. would shifting the entry by 1, 2, or 3 5m-bars (in either direction) change the empirical WR materially?** (MEDIUM VALUE, MEDIUM RISK — adjacent to the slippery "5m signal layer" temptation; must be tightly bounded.)
7. **Would 5m mark-price vs trade-price comparison expose stop-trigger sensitivity differently than 15m?** Useful for stop-mechanism understanding. (LOW-MEDIUM VALUE, LOW RISK.)
8. **Does 5m-resolution analysis introduce more false precision than useful evidence?** This is a meta-question that should be revisited *after* any future diagnostics work, not before. (META — assess after the fact.)

A future 5m diagnostics phase, if ever authorized, should predeclare which subset of these questions is in scope and explicitly disclaim any others.

---

## 7. Risks of 5m work

5m work — even purely diagnostic — carries specific risks:

### 7.1 Cost amplification

If 5m work *ever* drifts toward signal generation, the cost burden grows roughly linearly with bar frequency. 4× signal candidates ≈ 4× the per-trade cost incurred. §11.6 = 8 bps HIGH per side becomes significantly harder to pass at 5m than at 15m for the same per-trade edge.

### 7.2 Signal-frequency explosion

Even setting cost aside, 4× more bars means 4× more apparent "candidates" for any setup pattern. This dilutes statistical power per fold and increases false-positive rate at any given pattern-detection threshold.

### 7.3 F1-style high-frequency negative-edge compounding

F1 demonstrated catastrophically that high frequency + negative per-trade edge = compounded loss. Any 5m strategy variant inherits this risk at 4× severity unless per-trade edge is *also* 4× larger — which is empirically unlikely given the F1 / R2 / D1-A pattern.

### 7.4 Lower signal-to-noise ratio

5m bars are noisier than 15m bars at the same observable window. Volatility-percentile, ATR, and chop measures are statistically less stable at 5m granularity. Indicators that work cleanly at 15m may oscillate at 5m, producing more false signals and less stable thresholds.

### 7.5 Overfitting

4× more bars = 4× more potential feature combinations. The risk of identifying "patterns" that are statistical artifacts rises sharply. Walk-forward / fold counts that gave acceptable statistical power at 15m may be insufficient at 5m.

### 7.6 Timestamp / leakage risk

Mixing 5m and 15m data introduces explicit timestamp-alignment risk. A 5m bar's `open_time` does not align cleanly with 15m bar boundaries except every third 5m bar (`open_time` mod 15m = 0). Joining 5m and 15m without careful point-in-time discipline can introduce subtle look-ahead leakage, especially in any feature derived from "current 15m bar" state queried at a 5m timestamp.

### 7.7 Data-volume / storage / runtime cost

5m datasets are roughly 3× the size of 15m datasets for the same date range. v003 supplemental 5m data for BTCUSDT + ETHUSDT (klines + mark-price) over the existing v002 date range would meaningfully increase storage footprint and analytical runtime. Not a blocker, but a cost worth noting.

### 7.8 v003 dataset complexity

Adding 5m to v003 means the version manifest must clearly distinguish 5m-supplemental tables from 15m-canonical tables, with explicit predecessor-linkage to v002, schema versioning per `dataset-versioning.md`, and immutability discipline. This is doable but adds ongoing maintenance overhead.

### 7.9 False confidence from intrabar hindsight

Intrabar visibility creates the *illusion* of post-hoc precision. Once you can see "the trade *would have* hit +1R intrabar before reversing to stop," the temptation to redesign exit rules around that observation is strong. This is exactly the post-hoc-loosening anti-pattern Phase 2y §11.3.5 forbids.

### 7.10 Temptation to create 5m variants

The single largest non-statistical risk. Once 5m data exists for diagnostics, the project will face ongoing temptation to "just try" a 5m version of V1, F1, D1-A, or some hybrid. Each such attempt must be separately authorized; without a hard procedural barrier, scope creep is likely.

### 7.11 Confusion between diagnostics and reclassification

5m findings *cannot* by themselves reclassify R2, F1, or D1-A. Any reclassification would require a separately authorized formal phase with predeclared evidence thresholds. Without that procedural separation, 5m diagnostics findings risk being treated as "evidence to reopen" prior verdicts — another post-hoc loosening risk.

---

## 8. Data requirements

Phase 3n is *not* authorizing data download or v003 creation. This section documents what *would be required* if a future docs-only data/planning phase were ever authorized.

### 8.1 v002 sufficiency for Phase 3n

v002 datasets currently include 15m + 1h-derived + 15m mark-price + funding-event tables for BTCUSDT and ETHUSDT (per `data/manifests/`). **v002 is sufficient for Phase 3n** because Phase 3n produces no analysis — only documentation. v002 would be *insufficient* for any future 5m-diagnostics analysis, since 5m OHLCV is not part of v002.

### 8.2 v003 vs supplemental versioning

A future 5m-diagnostics phase would have two valid versioning options:

- **Option A — Bump to v003.** A coordinated dataset-family bump that includes 5m klines, 5m mark-price, and any newly derived 5m-resolution tables, with v003 manifests linking back to v002 as predecessor.
- **Option B — Supplemental versioning under v002.** Add `binance_usdm_btcusdt_5m__v001` as a new dataset family alongside existing v002 datasets, *without* bumping v002 to v003. v002 remains the canonical strategy/validation dataset; v001-of-5m is supplemental.

Per `dataset-versioning.md` §"When a New Dataset Version Is Required," adding a new interval set is a mandatory version bump for the *5m dataset family*. Whether the existing 15m datasets must also bump from v002 to v003 depends on whether any 15m semantic changes are introduced concurrently. If 15m semantics are unchanged, **Option B (supplemental v001-of-5m + v002 unchanged)** is the cleaner path; it avoids contaminating the existing v002-based verdict trail.

This memo does **not** decide between Option A and Option B. That decision belongs in a future docs-only data/planning memo if ever authorized.

### 8.3 Timestamp policy considerations

Per `timestamp-policy.md`, all canonical timestamps are UTC Unix milliseconds, and bar identity uses `symbol + interval + open_time`. Adding 5m introduces specific concerns:

- 5m `open_time` values must align to UTC 5-minute boundaries (`open_time` mod 300000 = 0 in milliseconds).
- 5m bar end times (`close_time`) must respect `open_time + 5 × 60 × 1000 − 1` convention or equivalent.
- Any join between 5m and 15m must use explicit alignment logic; 15m `open_time` values are a strict subset of 5m `open_time` values (every third 5m boundary).
- "Completed bars only" discipline applies at 5m granularity; partial 5m bars must not be used in any future diagnostic analysis.

### 8.4 Dataset-versioning policy considerations

Per `dataset-versioning.md`, any future 5m datasets must:

- Have explicit version IDs (`__vNNN`).
- Have manifest files describing source endpoint, symbol, interval, schema version, generation timestamp, predecessor-linkage to v002 or another formal ancestor, and quality checks.
- Be immutable once published.
- Be linked to any future diagnostics report by version ID.
- Distinguish raw 5m payloads (source-faithful, separately traceable) from normalized 5m datasets (semantically versioned).

### 8.5 Contamination prevention

5m data and any 5m-derived analysis must not contaminate v002-based verdicts. Specifically:

- 5m data must not be re-used to *retroactively* score H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A. Those verdicts are dataset-version-locked to v002; any 5m-augmented re-analysis would constitute a *new* analysis under a *new* dataset version and a *new* phase authorization, not a reclassification of prior verdicts.
- 5m-derived diagnostics must be reported separately from v002-based aggregate metrics in any future memo.
- Prior validation reports (Phase 2e through Phase 3j) remain locked at their v002 dataset references and must not be edited to reference 5m data.

### 8.6 Phase 3n authorization scope

Phase 3n authorizes **none** of the following:

- 5m data download.
- v003 dataset creation.
- Supplemental v001-of-5m dataset creation.
- 5m manifest generation.
- 5m-derived table creation.
- 5m timestamp-policy revision.
- Any schema change to v002.
- Any predecessor-linkage edit to existing v002 manifests.

---

## 9. Validation and anti-overfitting rules for any future 5m phase

Any future 5m phase — whether docs-only or analytical — should respect the following guardrails. These are guardrails for *any future authorization*, not Phase 3n requirements (Phase 3n is docs-only and produces no analysis).

### 9.1 Predeclare diagnostic questions

The diagnostic question set (e.g. a subset of §6 of this memo) must be written down and committed to git **before** any 5m data analysis begins. Adding diagnostic questions after seeing data is data-dredging.

### 9.2 Do not create 5m entry signals initially

The first 5m phase, if any, must explicitly disclaim 5m signal generation. Diagnostic-only scope must be enforced procedurally.

### 9.3 Do not tune parameters from 5m path data

5m diagnostic findings about path (intrabar adverse-excursion, target touches, decay windows) must not be used to derive new entry/exit/stop parameters for any retained-evidence candidate. This is the post-hoc loosening boundary.

### 9.4 Do not use intrabar target touches as post-hoc exit-rule rescue

If any 5m diagnostic shows that some 15m losers touched +1R or +2R intrabar before reversing, this finding must not be converted into an "improved exit rule" without separately authorized formal reclassification phase with predeclared evidence thresholds. The mere existence of intrabar target touches *does not* prove an improved exit rule would have been profitable in walk-forward cross-validation — it only proves that *some* trades touched the level *some* of the time.

### 9.5 Separate diagnostics from candidate framework evaluation

Diagnostics work answers "what happened inside losing trades?" Framework evaluation answers "does this candidate pass §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds?" These are *different questions*. Diagnostic findings may *inform* future framework evaluations, but cannot directly *constitute* framework evaluation.

### 9.6 Freeze data version before analysis

Any 5m data analysis must be scoped to a specific, immutable, manifest-linked dataset version. Data may not be silently re-fetched, re-aggregated, or re-normalized during analysis.

### 9.7 Preserve §11.6

§11.6 = 8 bps HIGH per side remains preserved verbatim regardless of any 5m findings. A separate formal cost-model revision phase, with predeclared evidence thresholds, would be required to revise §11.6.

### 9.8 No prior verdict revision unless separately authorized

R2's FAILED verdict, F1's HARD REJECT verdict, and D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict are *terminal* under current locked spec. 5m diagnostic findings cannot revise them. If the operator ever authorizes a successor or rescue phase, that phase must be separately scoped, separately authorized, and separately reviewed.

### 9.9 No project-lock revision

The §1.7.3 project-level locks (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) remain preserved verbatim regardless of any 5m findings. A future 5m diagnostics phase does not authorize project-lock revision.

---

## 10. Relationship to regime-first

Phase 3m's regime-first framework memo recommended **remain paused** as primary, with formal regime-first spec / planning as a possible future docs-only option but not started.

5m's relationship to regime-first:

- **5m should NOT be the first regime classifier.** First-pass regime axes should be observable on existing v002 data (15m volatility, 1h volatility, funding stress, BTC-ETH covariance, time-of-day). These are all clearly defined, statistically stable, and falsifiable from existing data.
- **5m may later provide regime *transition* diagnostics.** Once a 15m/1h-based regime taxonomy is candidate-defined, 5m might help observe *when* regime transitions actually happen (e.g. does volatility-regime shift happen at the 15m boundary or somewhere inside a 15m bar?). This is a downstream enhancement.
- **5m may later provide execution-path diagnostics conditional on regime.** Different regimes might have different intrabar adverse-excursion patterns. This is also downstream.
- **Phase 3m's regime-first caution still applies.** Anti-circular-reasoning principles (regimes defined first from first principles; no winning-fold-derived regimes; no rescue framing; no TARGET-exit-conditional labels; falsifiable + stable) apply to any future 5m-conditioned regime work *and more so*, since 5m increases the available degree of freedom.

Phase 3n does **not** authorize regime-first work, regime-first spec, or regime-first implementation. Phase 3n's relationship to regime-first is *informational*: 5m's role as a regime-input is downstream, conditional, and not a current-decision question.

---

## 11. Relationship to ML

ML feasibility was discussed in Phase 3k (option in the decision menu) and Phase 3m (briefly noted as not authorized). It remains not authorized.

5m's relationship to ML:

- **5m does NOT enable ML now.** ML feasibility remains a separate, unauthorized question. Phase 3n does not change that.
- **5m increases ML feature count and leakage risk.** If ML is ever authorized, having 5m data available simultaneously increases (a) the feature surface, (b) the leakage risk (5m features must be point-in-time aligned to 15m strategy decision moments without forward-leakage), and (c) the overfitting risk. ML feasibility memo, if ever authorized, must address these concerns explicitly.
- **5m diagnostics could be a useful ML *training-target labeler* later, but only later.** E.g. labels like "did the trade touch +1R intrabar?" are clean targets — *but* the question of whether such labels lead to profitable ML signals is itself the ML feasibility question, which remains unauthorized.

Phase 3n does **not** authorize ML feasibility, ML training, ML data preparation, or ML implementation. ML remains separate and not authorized.

---

## 12. Relationship to paper/shadow and Phase 4

Paper/shadow (Phase 7) and Phase 4 (runtime / state / persistence) remain unauthorized per `phase-gates.md` and `current-project-state.md`.

5m's relationship to paper/shadow and Phase 4:

- **5m execution-realism diagnostics might eventually matter for paper/shadow.** Validating that simulated fills inside a 15m bar match what a real exchange would have done is a paper/shadow-stage concern (Phase 7). 5m bars (and ideally sub-minute or tick data) would be one input to that validation.
- **No live-readiness implication follows from Phase 3n.** 5m diagnostics work, even if eventually authorized, does not affect live-readiness gates, dashboard requirements, runtime persistence, exchange-write capability, or production-key timing. Phase 8 / Phase 9 gates remain governed by `phase-gates.md`.
- **5m work is not a Phase 4 prerequisite.** Phase 4 (runtime state / persistence / risk runtime) is governed by docs already in place; 5m work neither blocks nor accelerates Phase 4 authorization.

Phase 3n does **not** authorize paper/shadow planning, Phase 4 runtime work, live-readiness work, deployment, production-key creation, or exchange-write capability.

---

## 13. Possible future paths after Phase 3n

The operator now has a docs-only feasibility memo about 5m. The next operator decision is operator-driven only. The following paths are *possible*; Phase 3n recommends exactly one.

### 13.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. The strategy-execution pause continues. Phase 3n joins Phase 3k / 3l / 3m as docs-only research-consolidation evidence. No 5m data acquired. No v003 created. No diagnostics phase started.

**Reasoning:**

- The case for 5m diagnostics is **non-zero but provisional**. The strongest single hypothesis (D1-A funding-extreme decay window) has high information value, but D1-A is already terminal under current spec; the diagnostic finding could only *inform* a possible D1-A-prime / D1-B / hybrid / regime-first phase, not authorize one.
- The procedural overhead of any 5m phase is significant: dataset versioning, predeclared question discipline, anti-overfitting guardrails, separation from prior verdicts. None of this overhead is justified without a strong, specific, operator-driven motivation that Phase 3n does not currently produce.
- The risks (especially §7.10 5m-variant scope creep and §7.9 false-confidence-from-intrabar-hindsight) are real and well-documented.
- The cumulative pattern across Phase 3k / 3l / 3m has been "remain paused" three times. Phase 3n adds another piece of *thinking*, not a piece of *evidence demanding action*.
- Phase 3n's value is in *having documented* the 5m feasibility question — so that future operator decisions can reference this memo and not have to re-derive its conclusions from scratch. That value is realized whether or not any successor phase is authorized.

**What this preserves:** R3 baseline-of-record; H0 anchor; all retained-evidence verdicts; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; v002 dataset version; no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write commitment.

**What this rules out:** No 5m data acquired. No v003 created. No diagnostics produced. No prior verdict revised. No successor authorized.

### 13.2 Option B — 5m data-requirements / v003 planning memo, docs-only (CONDITIONAL secondary alternative)

**Description:** Authorize a future docs-only memo that defines (a) which 5m datasets would be required, (b) Option A vs Option B versioning (v003 bump vs supplemental v001-of-5m), (c) timestamp-policy specifics for 5m, (d) data-quality checks, (e) a written decision about whether to actually proceed with 5m data acquisition. Still no data download, still no v003 created, still no analysis.

**Reasoning if selected:** Phase 3n's §8 outlines the data-requirements space at a sufficient level of abstraction; a deeper docs-only data/planning memo would be the *next-most-conservative* step beyond Phase 3n. It would still produce only documentation, not data, and not analysis.

**Pre-conditions if selected:** Operator commits ex-ante to symmetric-outcome / anti-circular-reasoning discipline. Operator commits ex-ante that the data/planning memo cannot itself authorize 5m data acquisition or analysis — a further phase would be required for that.

**Risks if selected:** Procedural escalation. Each successive docs-only memo creates institutional pressure to "do something with this," even if "remain paused" remains the right answer. Three docs-only memos already exist (3k / 3l / 3m); a fourth on essentially the same theme should be selected only if the operator has a specific motivating question that Phase 3n does not already address.

### 13.3 Option C — 5m diagnostics-spec memo, docs-only (CONDITIONAL tertiary alternative)

**Description:** Authorize a future docs-only memo that *predeclares* the diagnostic question set (e.g. a tightly bounded subset of Phase 3n §6), defines the methodology (without producing any analysis), and writes the anti-overfitting guardrails as enforceable procedural rules. Still no data download, still no v003 created, still no analysis.

**Reasoning if selected:** Predeclaring the question set is exactly the discipline §9.1 requires. Doing so before any analysis is an unambiguous good — it cannot be "post-hoc" if it predates any data work.

**Pre-conditions if selected:** Same as Option B, plus operator commitment that the diagnostics-spec memo cannot itself authorize data acquisition or analysis.

**Risks if selected:** Same as Option B, with the additional risk that predeclaring questions creates institutional pressure to *answer* them. A predeclared question is not a commitment to investigate; this must be made explicit.

### 13.4 Option D — Regime-first formal spec memo, docs-only (LATERAL secondary alternative)

**Description:** Authorize the docs-only formal regime-first spec memo that Phase 3m discussed but did not start.

**Reasoning if selected:** Independent of 5m. Some operators may decide that regime-first is a more promising direction than 5m diagnostics.

**Phase 3n's view:** 5m and regime-first are different research tracks; choosing between them is an operator-strategic question, not a Phase 3n technical question. Phase 3m's recommendation was "remain paused" with regime-first formal spec as a possible future option. Phase 3n does not endorse or oppose this option relative to Option A; it is mentioned for completeness.

### 13.5 Option E — ML feasibility memo, docs-only (CONDITIONAL alternative)

**Description:** Authorize a docs-only memo evaluating whether ML feasibility work is appropriate.

**Reasoning if selected:** Independent of 5m. Phase 3k's decision menu listed ML feasibility as an option; it remains so.

**Phase 3n's view:** ML feasibility is a separate and significantly more complex question than 5m feasibility. Phase 3n does not endorse this option as a near-term direction; it is mentioned for completeness.

### 13.6 Option F — New strategy-family discovery (NOT RECOMMENDED)

**Description:** Authorize a new strategy-family discovery phase analogous to Phase 3a (F1 family) or Phase 3f (D1-A family).

**Phase 3n's view:** Three strategy-research arcs have framework-failed under unchanged discipline. Starting a fourth without addressing *why* the first three failed (which 5m diagnostics or regime-first work might inform) is procedurally premature. Not recommended.

### 13.7 Option G — Paper/shadow planning, Phase 4, live-readiness, deployment, or strategy rescue (NOT RECOMMENDED)

**Description:** Authorize any phase beyond docs-only research consolidation.

**Phase 3n's view:** None of these are appropriate from the current state. R3 remains the strongest evidence the project has produced, but R3 alone does not constitute live-readiness evidence under `phase-gates.md` Phase 8 criteria. Strongly not recommended.

### 13.8 Recommendation

**Phase 3n recommends Option A (remain paused) as primary.**

The case for any 5m work is non-zero but provisional and procedurally heavy. The case for *documenting the 5m feasibility question* is strong; that value has now been realized by this memo itself. The case for *acting on* 5m feasibility (even at the docs-only level of Option B or C) is weak in the absence of a specific operator-driven motivation that Phase 3n does not currently identify.

Phase 3n explicitly does **NOT** recommend:

- Implementation of any kind.
- Backtesting of any kind.
- 5m data acquisition.
- v003 creation.
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

If the operator selects Option A, Phase 3n is closed and the project remains at the post-Phase-3n / consolidated boundary.

If the operator selects Option B (5m data-requirements / v003 planning memo) or Option C (5m diagnostics-spec memo), each is conditional on explicit ex-ante operator commitment to symmetric-outcome / anti-circular-reasoning discipline and explicit ex-ante commitment that the docs-only memo cannot itself authorize data acquisition or analysis. Selecting B or C does not authorize anything beyond the named docs-only memo.

Options D, E, F, and G are not recommended by Phase 3n.

---

## 14. Explicit preservation

This memo preserves the following items unchanged:

- **No threshold changes.** §10.3 (Δexp ≥ +0.10 R), §10.4 (absolute floors expR > −0.50 AND PF > 0.30), §11.3 (V-window no-peeking), §11.4 (ETH non-catastrophic), §11.6 (8 bps HIGH per side cost-resilience) preserved verbatim.
- **No strategy-parameter changes.** R3 sub-parameters preserved. F1 parameters preserved (8-bar cumulative displacement > 1.75 × ATR(20); SMA(8) target; structural stop with 0.10 × ATR buffer; 8-bar time-stop; same-direction cooldown until unwind). D1-A parameters preserved (|Z_F| ≥ 2.0 / 270 events / 1.0 × ATR(20) stop / +2.0 R target / 32-bar (8-hour) time-stop / per-funding-event cooldown / band [0.60, 1.80] × ATR / contrarian / no regime filter).
- **No project-lock changes.** §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) preserved verbatim.
- **No prior verdict changes.** R3 remains V1 breakout baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained research evidence only. R2 remains FAILED — §11.6 cost-sensitivity blocks. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other.
- **No backtests.** No backtest run by Phase 3n.
- **No data download.** No data fetched from any source by Phase 3n.
- **No v003 creation.** v002 datasets remain canonical; no v003 dataset created or staged.
- **No supplemental 5m dataset created.**
- **No derived 5m-resolution tables created.**
- **No timestamp-policy changes.**
- **No dataset-versioning policy changes.**
- **No cost-model revision.** Phase 3l's "B — current cost model conservative but defensible" assessment stands. §11.6 unchanged.
- **No regime-first authorization.** Phase 3m's "remain paused" recommendation stands.
- **No ML feasibility authorization.**
- **No new strategy-family discovery authorization.**
- **No D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid authorization.**
- **No paper/shadow planning authorization.**
- **No Phase 4 runtime / state / persistence authorization.**
- **No live-readiness authorization.**
- **No deployment authorization.**
- **No production-key creation authorization.**
- **No exchange-write capability authorization.**
- **No MCP / Graphify / `.mcp.json` activation.** Project rules `.claude/rules/prometheus-mcp-and-secrets.md` preserved.
- **No credentials requested or used.**
- **No authenticated / private Binance API calls made.**
- **No data/ commits.** v002 manifests untouched. No new data files staged or committed.
- **No next phase started.**

The output of Phase 3n is this memo and the closeout report. No code, no tests, no scripts, no data, no thresholds, no strategy parameters, no project locks, no paper/shadow, no Phase 4, no live-readiness, no deployment, no credentials, no MCP, no Graphify, no `.mcp.json`, and no exchange-write work has changed.

Phase 3n is a docs-only feasibility memo. The operator decides what (if anything) follows.
