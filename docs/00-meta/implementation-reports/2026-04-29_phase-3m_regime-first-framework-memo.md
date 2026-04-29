# Phase 3m — Regime-First Research Framework Memo (docs-only)

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2p §C.1 (R3 baseline-of-record); Phase 2x family-review memo (V1 breakout family at useful ceiling under current framework); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved); Phase 2w §16.1 (R2 FAILED — §11.6 cost-sensitivity blocks); Phase 3d-B2 (F1 HARD REJECT); Phase 3e post-F1 research consolidation memo (remain-paused recommendation); Phase 3f research-direction discovery memo (D3 regime-first ranked "blocked by complexity / Phase-4-dependent"); Phase 3j (D1-A MECHANISM PASS / FRAMEWORK FAIL — other; Phase 3j terminal for D1-A under current locked spec); Phase 3k post-D1-A research consolidation memo (remain-paused primary recommendation; regime-first memo as conditional tertiary alternative); Phase 3l external execution-cost evidence review (primary assessment B — current cost model conservative but defensible; §11.6 unchanged pending stronger evidence); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3m — Docs-only **regime-first research framework memo.** Evaluates whether the next serious research direction should be a regime-classification framework (rather than another immediate strategy-family spec, timeframe switch, ML experiment, or candidate rescue). Builds on Phase 3k's tertiary acceptable docs-only alternative authorization.

**Branch:** `phase-3m/regime-first-framework-memo`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No prior verdict revised.** R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained research evidence. R2 remains FAILED. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. §11.6 = 8 bps HIGH per side preserved. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3m is deciding

Phase 3m is the docs-only tertiary acceptable alternative authorized by Phase 3k (per Phase 3k §11 + §12). The operator's decision sequence to date has been:

1. Phase 3k recommended **remain paused** as primary (after V1 + F1 + D1-A all framework-failed under unchanged discipline).
2. Phase 3l (operator-selected secondary alternative) confirmed: **cost model conservative but defensible**; §11.6 unchanged pending stronger evidence; no candidate rescued; no threshold revision.
3. Phase 3m (operator-selected tertiary alternative) is now docs-only **regime-first research framework memo**.

The question Phase 3m weighs is:

> Given that V1 / R3 / R1a / R1b-narrow improved within the V1 breakout family but did not produce strong positive aggregate edge; that R2 / F1 / D1-A all showed *some* mechanism support but framework-failed (R2 on §11.6; F1 on catastrophic floor; D1-A on cond_i + cond_iv); and that Phase 3l did not support loosening the cost model — is the right next research-framework move to **stop trying single-regime strategies under blanket framework discipline** and instead **construct a regime-classification layer that conditions WHICH mechanism applies WHEN**?

Phase 3m is **NOT**:

- Authorizing a regime-first execution phase, regime-first spec, or regime-first implementation.
- Authorizing any strategy variant, hybrid, or successor (D1-A-prime, D1-B, V1/D1, F1/D1, target-subset rescue).
- Authorizing 5m timeframe work, ML feasibility memo, formal cost-model revision, or new strategy-family discovery.
- Authorizing any backtest, parameter sweep, threshold revision, project-lock revision, or prior-verdict revision.
- Authorizing paper/shadow planning, Phase 4 runtime / state / persistence work, live-readiness, deployment, production-key creation, or exchange-write capability.
- Defining numeric regime thresholds for use in any subsequent execution phase.
- Choosing a final regime taxonomy.

Phase 3m **IS**:

- A docs-only memo that documents (a) why regime-first is being considered now, (b) what anti-circular-reasoning principles must bound any future regime-first work, (c) what regime axes are candidates with their associated evidence / data / risks, (d) a minimal first-pass illustrative taxonomy (no thresholds), (e) how each retained-evidence candidate maps to a plausible regime story (with strong / weak / speculative tags), (f) data requirements, (g) what a future regime-first validation plan would need to look like, (h) failure modes, (i) the relationship to 5m and ML directions, and (j) a single recommended next operator decision from the menu allowed by the Phase 3m brief.

The output is a consolidated regime-first thinking record + a single forward-looking operator decision recommendation. **Phase 3m produces a memo; the operator decides whether to authorize anything downstream.**

---

## 2. Current project-state restatement

| Item | State |
|------|-------|
| **R3** | V1 breakout baseline-of-record per Phase 2p §C.1; locked sub-parameters preserved. |
| **H0** | V1 breakout framework anchor per Phase 2i §1.7.3. |
| **R1a / R1b-narrow** | Retained research evidence only; non-leading. |
| **R2** | Retained research evidence only; **framework FAILED — §11.6 cost-sensitivity blocks** (BTC HIGH-slip Δexp_H0 −0.014; ETH HIGH-slip Δexp_H0 −0.230). |
| **F1** | Retained research evidence only; **HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal for F1. |
| **D1-A** | Retained research evidence only; **MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2; Phase 3j terminal for D1-A under current locked spec. |
| **Phase 3k consolidation** | Drafted, merged; primary recommendation: **remain paused**. |
| **Phase 3l external cost-evidence review** | Drafted, merged; primary assessment **B — current cost model conservative but defensible**; §11.6 = 8 bps HIGH per side **preserved unchanged pending stronger evidence**. |
| **§1.7.3 project-level locks** | Preserved verbatim. |
| **Phase 2f thresholds (incl. §11.6 = 8 bps HIGH per side)** | Preserved verbatim. |
| **Paper/shadow planning** | Not authorized. |
| **Phase 4 work** | Not authorized. |
| **Live-readiness / deployment / production-key / exchange-write work** | Not authorized. |
| **MCP / Graphify / `.mcp.json` / credentials** | Not activated; not requested; not used. |

The next operator decision is operator-driven only. Phase 3m does not pre-empt that decision; this section records the state on which any future decision must build.

---

## 3. Why regime-first is being considered now

The cumulative empirical pattern across **three complete strategy-research arcs under unchanged framework discipline** is now consistent enough to warrant explicit framework-level reflection.

### 3.1 V1 breakout family (Phases 2e–2w)

- H0 baseline produces aggregate-negative expR on BTC + ETH R-windows (BTC −0.459 / ETH −0.475).
- R3 (Phase 2j memo §D — Fixed-R + 8-bar time-stop) **PROMOTE — broad-based**; reduces BTC R-window expR to −0.240 (PF 0.560) and ETH to −0.351 (PF 0.474). R3 is the strongest single candidate evidence the project has produced; **but** the absolute aggregate edge is still negative ("less negative than H0" not "break-even").
- R1a / R1b-narrow each produce mixed-PROMOTE / formal-PROMOTE outcomes with documented per-symbol asymmetry or near-neutral marginal contribution; non-leading.
- The family responds to disciplined structural redesign in a measurable way, but **no candidate has produced positive aggregate net-of-cost expR** on the R-window. Phase 2x classified the V1 family as "at its useful ceiling under current framework".

### 3.2 R2 entry-axis (Phase 2u – 2w)

- R2's pullback-retest entry topology PROMOTED at MED slippage with M1 + M3 mechanism support per Phase 2w §11.5 / §11.7.
- **§11.6 cost-sensitivity gate FAILED** at HIGH on both symbols: BTC Δexp_H0 −0.014 (sub-threshold); ETH Δexp_H0 −0.230 (catastrophic).
- R2's edge is real but slippage-fragile by construction (small post-pullback R-distance amplifies per-trade cost). Lesson: pullback-retest entries are slippage-fragile.

### 3.3 F1 mean-reversion (Phases 3a – 3d-B2)

- F1's **M3 (TARGET-exit subset) PASS** on both symbols: BTC mean +0.748 R / aggregate +1149 R; ETH mean +0.868 R / aggregate +1398 R. The mean-reversion target IS profitable when isolated.
- F1's M1 (post-entry counter-displacement at h=8) BTC PARTIAL (mean +0.024 R below the +0.10 R threshold; fraction non-neg 55.4% above 50%).
- F1's M2 (chop-regime stop-out fraction reduction) **CONTRADICTS the Phase 3b §2.3 hypothesis on BTC**: F1's BTC low-vol stop-out fraction (55.6%) is *higher* than H0's (46.2%). The chop-regime advantage F1 was designed to capture is **not present on BTC at the F1-as-specified parameter setting**.
- F1 catastrophic absolute-floor violations: BTC MED expR=−0.5227, BTC HIGH expR=−0.7000 / PF=0.2181, ETH HIGH expR=−0.5712 / PF=0.2997. Phase 3d-B2 terminal for F1.
- **The wider strategy fails because (a) trade frequency is ~150× H0 and (b) STOP exits (53–54%) overwhelm the TARGET-exit positive contribution.**

### 3.4 D1-A funding-aware (Phases 3f – 3j)

- D1-A's **M1 BTC h=32 PASS**: mean +0.1748 R AND fraction-non-negative 0.5101. The post-extreme-funding contrarian directional mechanism IS empirically present.
- D1-A's **M3 PASS-isolated** on both symbols: BTC TARGET mean +2.143 R; ETH TARGET mean +2.447 R. Per-trade R magnitudes are BETTER than the Phase 3h §5.6.5 forecast.
- **But** empirical WR ~30% / ~31% vs forecast +51% breakeven (gap ~21 percentage points). 67–68% of D1-A trades exit on STOP at −1.30 / −1.24 R mean.
- **Gate failures:** cond_i (BTC MED expR > 0) FAIL; cond_iv (BTC HIGH cost-resilience) FAIL. Catastrophic-floor predicate NOT triggered. Phase 3j terminal for D1-A under current locked spec.
- **Per-fold heterogeneity is large:** BTC F3 2023H1 +0.62 R (PF 2.03; only profitable BTC fold); BTC F5 2024H1 −0.98 R (PF 0.16; catastrophic-fold). ETH similar pattern. The strategy does not robustly produce positive expR across half-year folds in the R window.

### 3.5 Phase 3l cost-evidence review

- Primary assessment **B — current cost model conservative but defensible**.
- §11.6 = 8 bps HIGH per side preserved unchanged pending stronger evidence.
- No threshold loosening would be supported by the public Binance-fee / trading-rule / exchangeInfo evidence accessible without credentials.
- Therefore, framework-fail outcomes are **NOT** a calibration artifact at the level of evidence currently obtained.

### 3.6 The cumulative pattern

Across three arcs, the recurring shape is:

> **Mechanism shows up empirically (M1 and/or M3) → strategy-as-specified framework-fails because aggregate behavior across regimes overwhelms the favorable subset.**

This pattern is not merely about candidate-specific tuning. It suggests that **the favorable cells in the per-fold breakdowns are real, and the unfavorable cells are also real** — and a single-regime strategy specification pays the cost of being wrong in unfavorable regimes while only collecting the gain in favorable regimes.

A natural framework-level question follows: **what if the next research direction is a regime-classification layer that conditions which mechanism applies in which regime, rather than another single-regime variant?**

This question is **not** an attempt to rescue R2 / F1 / D1-A through regime-conditioning. It is a recognition that the project has now executed its rank-1 (F1) and rank-2 (D1-A) near-term Phase-3a / Phase-3f candidates — both of which framework-failed — and that cost-policy verification did not change the picture. The space of "next disciplined research direction" is correspondingly narrower.

Phase 3m treats the regime-first hypothesis with **strict anti-circular-reasoning discipline** (§4 below). The regime-first hypothesis is interesting AND dangerous; this memo's role is to characterize both.

---

## 4. Anti-circular-reasoning principles

Regime-first work is **structurally vulnerable to circular reasoning** in a way that single-regime strategies are not. The principles below are binding for any future regime-first phase. **Phase 3m affirms them as preconditions for any successor authorization.**

### 4.1 Regimes must be defined from first principles before testing

The regime classifier — its axes, its discrete states, its label-assignment rules — must be **declared in writing** before any per-regime strategy outcome is observed. The classifier definition cannot be modified after observing per-regime per-candidate outcomes. This is the regime-first analogue of Phase 2f §11.3.5 (no post-hoc loosening) and Phase 2j §C.6 (singular committed sub-parameters).

The first-principles requirement means: **regimes derive from observable market microstructure or price-action features that exist independently of strategy outcomes**. Examples of acceptable derivation:
- Volatility-quantile from rolling realized vol (independent of any candidate's per-trade outcome).
- Trend-strength from 1h slope-3 magnitude (independent of any candidate's per-trade outcome).
- Funding-rate level from funding-rate Z-score (independent of any candidate's per-trade outcome — even though D1-A's signal is a funding-rate Z, the regime axis would partition on a *separate* magnitude question, not on D1-A's signal direction).
- Spread / liquidity from depth-weighted bid-ask metrics (independent of any candidate's per-trade outcome).

### 4.2 Do not define regimes from winning folds

This is the most dangerous failure mode. Phase 3j showed BTC F3 2023H1 +0.62 R; BTC F5 2024H1 −0.98 R for D1-A. It is **forbidden** to define a regime as "the conditions in F3 2023H1" or "regimes that look statistically similar to F3 2023H1". That construction collapses regime classification into retrospective subset selection — exactly the post-hoc loosening §11.3.5 forbids.

The failure mode is precisely diagnosable: **if the regime axis was constructed by inspecting per-fold per-candidate outcomes, the regime axis carries information that the strategy-as-evaluated did not have at trade time**. Backtests under such a classifier would be optimistically biased; live performance would systematically underperform.

### 4.3 Do not define regimes to rescue R2, F1, or D1-A

R2 / F1 / D1-A's framework verdicts are **binding outcomes** under the framework discipline that produced them. Per Phase 2y §3.3 / Phase 3e §5.4 / Phase 3k §5.5 / Phase 3l §13: mechanism evidence (M1 / M3 PASS) is research evidence; it is not promotion authority.

A regime-first phase that constructs a "regime where R2 works" or "regime where F1 works" or "regime where D1-A works" by selecting features that retrospectively align with each candidate's profitable cells is a **rescue framing** disguised as framework-level redesign. Phase 3m forbids this.

The disciplined alternative: regime axes are defined first; THEN any strategy mechanism (including but not limited to retained-evidence mechanisms) can be evaluated per-regime. The order of operations matters.

### 4.4 Do not use post-hoc target-subset evidence as regime definition

F1's M3 PASS isolated the TARGET-exit subset (retrospectively, by exit reason). D1-A's M3 PASS isolated the TARGET-exit subset (retrospectively). Both subsets are profitable in isolation.

It is **forbidden** to define a regime as "the conditions under which a TARGET exit happens". TARGET-exit-conditional partitioning is post-hoc selection by definition: the partition can only be evaluated after the trade is over. Such a partition cannot be applied prospectively to entry decisions.

The disciplined alternative: regime axes are defined on **pre-entry observable features**; per-regime backtests then evaluate whether the same single-regime strategy specification produces different-shaped TARGET-exit / STOP-exit / TIME_STOP-exit fractions in different regimes. The TARGET-exit fraction is an *outcome statistic*, not a regime-defining feature.

### 4.5 Regime definitions must be falsifiable and stable

A regime definition is **falsifiable** if a labelled period can be checked against the definition's criteria and either confirms or contradicts. "High-vol" is falsifiable if defined as "rolling 1h realized-vol percentile in top quartile relative to a fixed reference window"; it is not falsifiable if defined as "the periods where mean-reversion seems to work better".

A regime definition is **stable** if its labels do not whipsaw within the timescale relevant to the dispatched strategy. A regime classifier that flips state every 2 bars while the strategy fires once per 8 bars is operationally useless; strategies cannot calibrate to a regime label that changes faster than the strategy can act.

Stability requirements include: minimum-duration rule (hysteresis); explicit transition policy (does the dispatched strategy close on regime exit, hold through, or freeze new entries); and lag-budget acceptance (regime classification on completed bars only — same discipline as Phase 2f §11.3.5 strategy-conformance).

### 4.6 Anti-circular-reasoning discipline summary

| Forbidden pattern | Disciplined alternative |
|-------------------|-------------------------|
| Define regimes from winning folds | Define regimes from pre-entry observable market features |
| Define regimes to rescue R2/F1/D1-A | Define regimes first; evaluate any mechanism (incl. retained evidence) per-regime second |
| Use TARGET-exit subset as regime label | Use pre-entry features; treat exit-mix as outcome statistic |
| Tune regime thresholds on per-regime outcomes | Pre-declare thresholds; freeze before per-regime evaluation |
| Whipsaw or flicker labels | Hysteresis + minimum-duration rules; completed-bar-only labels |
| Regimes that "explain" everything | Small, interpretable taxonomy; reject taxonomies that match outcomes too cleanly |

Any future regime-first phase must explicitly affirm these constraints in its phase brief and gate-evaluation plan.

---

## 5. Candidate regime axes

This section enumerates candidate regime axes for an eventual regime-first taxonomy. **Each axis is a candidate; this memo does not pre-select; this memo does not authorize numeric thresholds; the operator and any successor regime-first spec phase decide the actual taxonomy.**

For each axis: why it might matter, prior strategy evidence pointing to it, data required, leakage / overfitting risk.

### 5.1 Volatility level (low / normal / high)

- **Why it might matter:** Per-trade R-magnitude is anchored to ATR(20) in the locked specs. Realized-vol regime affects (i) the spread between ATR(20) and instantaneous bar range, (ii) the geometry of stop-distance vs target-distance, (iii) cost-amplification (slippage in bps is roughly stable; in R-multiples it depends on the ATR-anchoring). Both F1 and D1-A's per-trade-R magnitudes are best when realized-vol is moderate; at extreme-vol periods the stop tends to fire before the directional drift develops.
- **Prior evidence:** F1 M2 BTC stop-out fraction higher in low-vol than H0 stop-out fraction (the chop-regime advantage hypothesis FAILED on BTC). D1-A per-fold heterogeneity F3 2023H1 vs F5 2024H1 plausibly tracks vol-regime differences (2024H1 had several volatility shocks during BTC-halving / regulatory news cycles). R3's broad-based PROMOTE shows R3's edge persists across vol regimes more robustly than F1's or D1-A's.
- **Data required:** Realized-vol on completed 15m bars (rolling N-bar standard deviation of log returns) or on completed 1h bars. ATR(20) on 15m + 1h. **In v002.**
- **Leakage / overfitting risk:** **Moderate.** Vol-quantile is computable from completed bars only; no future-knowledge issue. The risk is that rolling-window quantile choice (look-back length; quantile cutoff) introduces a hyperparameter that is implicitly tuned on the same R-window. Mitigation: pre-declare the look-back in the regime spec; freeze before per-regime evaluation.

### 5.2 Volatility expansion / compression

- **Why it might matter:** Bollinger-band-style compression-then-expansion is an established price-action pattern; F1's hypothesis was related (overextension as compression breakdown); R1a's hypothesis was related (volatility-percentile X=25 / N=200 setup predicate). The regime axis here is the *change-of-vol-regime*, not the level — i.e., is the market currently expanding or compressing?
- **Prior evidence:** R1a's compression-selection mechanically correct at the entry filter (100% of entries at percentile ≤ 25%) per Phase 2m. F1's overextension threshold 1.75×ATR(20) is structurally a compression-end / expansion-begin signal. D1-A is funding-driven, less directly tied to vol expansion / compression.
- **Data required:** Same as §5.1 plus differences (current vol vs N-bar-prior vol; rolling regression of realized-vol). **In v002.**
- **Leakage / overfitting risk:** **Moderate-to-high.** Expansion / compression definitions are extremely sensitive to look-back / threshold choices. The same R-window contains too few independent compression-expansion cycles to support fitting these parameters and then validating in-sample.

### 5.3 Trend strength

- **Why it might matter:** V1's failure mode #1 (chop with repeated false breaks) is the inverse of strong trend. R3's broad-based PROMOTE shows that under V1's existing 1h binary slope-3 + EMA-stack bias, the residual edge is positive in trend regimes and negative in chop. If trend strength can be measured continuously (not just binary slope-3), per-regime evaluation might separate trend-friendly mechanisms (V1 / R3 / D4-style pullback-continuation) from non-trend-friendly mechanisms (mean-reversion-shape).
- **Prior evidence:** F4 2024H1 worst per-fold cell on V1 (H0 BTC −1.025 R; R3 BTC −0.870 R) hints at chop-regime severity. R3's Phase 2l first-positive-expR BTC folds (F2, F3) plausibly track stronger-trend periods.
- **Data required:** 1h slope, 1h ADX, 1h moving-average separation (EMA(50) vs EMA(200)). All v002.
- **Leakage / overfitting risk:** **Moderate.** Trend metrics are well-known and have published academic conventions (ADX, MACD-divergence, EMA-stack); the risk is choosing thresholds that retrospectively split "good" and "bad" V1 / R3 folds. Mitigation: pre-declare trend metric and thresholds before per-regime evaluation.

### 5.4 Trend direction (up vs down)

- **Why it might matter:** Crypto-asset behavior is asymmetric on the up-down axis (long-bias drift; downside flash crashes). R3's per-fold breakdowns show some directional asymmetry. ETH is generally more directional than BTC.
- **Prior evidence:** D1-A's contrarian-direction is symmetric per the Z-score sign; per-trade R magnitudes reasonably symmetric on D1-A (winners +1.98 / +2.26 R; losers −1.30 / −1.24 R per Phase 3j §9). F1 / R2 / R3 per-direction breakdowns generally reasonably symmetric in V1 family.
- **Data required:** Same as §5.3 plus signed direction.
- **Leakage / overfitting risk:** **Low.** Up-vs-down is a binary axis; little to overfit.

### 5.5 Chop / range conditions

- **Why it might matter:** F1's and D1-A's mean-reversion-shape mechanisms claim to thrive in chop. F1 partially falsified this on BTC; D1-A's contrarian-after-extreme-funding mechanism is mean-reversion-flavored. A regime axis that distinguishes "directional" from "ranging" market microstructure could in principle clarify when each mechanism applies.
- **Prior evidence:** F1's M2 BTC stop-out fraction (55.6%) higher than H0's (46.2%) under the F1-as-specified definition of chop. F1's chop-regime advantage hypothesis empirically falsified on BTC (Phase 3d-B2 §10.3). The fact that F1's chop-regime hypothesis falsified is informative: F1's *operationalization* of chop did not match the regime-conditional behavior — but it does not foreclose that a *different* operationalization might.
- **Data required:** Range-as-fraction-of-ATR; bar-by-bar high-low / ATR ratio; consecutive same-direction-close streak; rolling Hurst exponent or similar mean-reversion-vs-trending indicator. v002 sufficient.
- **Leakage / overfitting risk:** **High.** Chop-vs-trend distinction is the most studied (and most overfit) classification axis in price-action research. The "chop" label has many candidate definitions, and selecting one retrospectively that aligns with F1's F3 2023H1-like favorable cells is exactly the rescue-pattern §4.3 forbids.

### 5.6 Funding stress

- **Why it might matter:** D1-A's signal IS funding-extreme. But D1-A's regime axis is the funding-Z-score *level*; a regime-first axis here would be a separate, more general classification: "is the perpetual-spot basis structure under stress?" Funding stress correlates with crowded-position risk and mark-vs-trade-price divergence.
- **Prior evidence:** D1-A M2 funding-cost benefit empirically small (BTC +0.00234 R; ETH +0.00452 R) suggests that simple per-trade carry accrual is not the lever — but funding-stress-as-regime-label could still gate when other mechanisms apply. Phase 3j §8.6 shows MARK vs TRADE_PRICE differs more for D1-A than for V1, suggesting funding-driven wick exposure.
- **Data required:** Funding-rate level + Z-score (already in v002 funding-rate-events dataset). Optionally: open-interest-change derived from public depth APIs (NOT in v002).
- **Leakage / overfitting risk:** **Moderate.** Funding-Z thresholds are interpretable (D1-A uses |Z| ≥ 2.0); risk is using funding-stress to retrospectively explain D1-A's per-fold heterogeneity.

### 5.7 Spread / slippage stress

- **Why it might matter:** §11.6 cost-sensitivity is the most consistent failure-mode signal in the project (R2, F1, D1-A all failed at HIGH; Phase 3l reaffirmed §11.6 = 8 bps preserved). A regime axis that flags real-time spread-widening would let cost-fragile mechanisms (R2-style entries) freeze during stress.
- **Prior evidence:** Phase 3l confirmed BTCUSDT and ETHUSDT perpetuals are typically liquid; spread widens during high-vol events. Phase 2y §5.1.2 listed spread-distribution as required external evidence not yet gathered.
- **Data required:** **NOT in v002.** v002 contains klines + mark-price + funding + exchange_info; it does NOT contain bid-ask spread, depth, or impact tick data. A spread-stress regime axis requires v003 or external microstructure data.
- **Leakage / overfitting risk:** **Low** *if the data exists*; unimplementable without it. Until external spread / depth data is gathered (which Phase 3l confirmed is operator-driven and outside docs-only scope), a spread-stress axis is descriptive only.

### 5.8 Liquidity / volume regime

- **Why it might matter:** Volume / open-interest level affects fill quality at scaled-live notionals; for current Prometheus research notional ($1K–$15K typical) the impact is small (Phase 3l §8.4). At larger notionals, liquidity regime would matter more.
- **Prior evidence:** None directly relevant to current research scope. Becomes relevant only at scaled-live equity tiers (operator-driven future decision).
- **Data required:** 15m volume (in v002 klines). Open-interest (NOT in v002).
- **Leakage / overfitting risk:** **Low** for volume; **moderate** for open-interest if v003 data is added (more parameters, more overfit potential).

### 5.9 Time-of-day / funding-window proximity

- **Why it might matter:** Crypto markets exhibit time-of-day effects (Asia / Europe / US session boundaries). Funding settlement events at 00:00 / 08:00 / 16:00 UTC create periodic micro-regimes around the boundary. D1-A's entries fire at funding-settlement boundaries by construction.
- **Prior evidence:** D1-A `bars_since_funding_event_at_signal = 0` on every trade per Phase 3j §8.4. The mechanism IS time-of-day-locked. Whether session boundaries (Asia/Europe/US) affect V1 / R3 / R1a / R1b-narrow has not been investigated.
- **Data required:** Pure timestamp features (UTC hour-of-day; bars-since-funding-settlement). No new data; both derivable from v002.
- **Leakage / overfitting risk:** **Low-to-moderate.** Time-of-day is well-known; the risk is constructing fine-grained time-of-day buckets that retrospectively segment good and bad V1 / R3 folds.

### 5.10 BTC / ETH relative behavior

- **Why it might matter:** §1.7.3 BTCUSDT-primary lock means Prometheus deploys BTC-only; ETH is research/comparison only. Per-symbol asymmetry has been persistent across V1 / F1 / D1-A. A regime axis that captures BTC-vs-ETH relative strength could improve research interpretation but cannot affect deployment without lifting §1.7.3.
- **Prior evidence:** BTC vs ETH asymmetry persistent across all three arcs (Phase 3k §6.7). F1 / D1-A's BTC-friendliness plausibility partially falsified (ETH less bad than BTC empirically).
- **Data required:** Both BTC and ETH 15m klines. v002.
- **Leakage / overfitting risk:** **Moderate.** The §1.7.3 lock makes any BTC/ETH regime axis research-only; deployment-relevance requires lock revision (outside Phase 3m scope).

### 5.11 Axis cross-cutting observations

- Most candidate axes (§5.1 volatility level; §5.3 trend strength; §5.5 chop/range; §5.6 funding stress; §5.9 time-of-day; §5.10 BTC/ETH) are **derivable from v002**. Spread-stress (§5.7) and full liquidity (§5.8) require v003 or external microstructure data not currently obtainable.
- Interpretability differs sharply: vol-level / funding-Z / time-of-day are highly interpretable (small parameter spaces; well-studied conventions); chop / volatility expansion-compression / liquidity are easier to overfit and harder to falsify.
- Sample-size per-regime constraints will be acute: the R-window has 36 months × 2 symbols ≈ 144 BTC + 144 ETH 1h-aligned regime-cells per axis (assuming 6 months × 6 folds per 36-month axis cell) — but multiplicative axes (e.g., 2 axes × 3 levels each = 6 regimes) cut sample size to 24-cell-equivalent per regime. **Multiplicative taxonomies must be avoided in any near-term regime-first work** because of sample-size collapse.

---

## 6. Regime taxonomy proposal (illustrative; first-pass; no thresholds)

Phase 3m proposes a **minimal first-pass illustrative regime taxonomy**. This is **NOT authorized** for any execution phase; it is a docs-only first sketch to ground the discussion. **No thresholds are proposed.** Any successor regime-first phase would (a) re-evaluate whether this taxonomy is the right one and (b) define thresholds in writing under §4 anti-circular-reasoning discipline before any backtest.

The proposed first-pass taxonomy uses **at most three small interpretable binary axes**, deliberately low-dimensional to avoid the §5.11 multiplicative sample-size collapse:

### 6.1 Axis A — Trend strength (binary)

- **Trend** vs **Non-trend.**
- Pre-entry observable; computed on completed 1h bars; one of the V1-spec-already-tested 1h slope-3 magnitude / EMA-stack indicators (no new indicator development at the regime taxonomy level).
- Threshold: **NOT proposed in Phase 3m.** A successor regime-first phase would declare a single threshold with an a-priori-justified value (e.g., a published academic convention or a structural reason like "EMA(50)-vs-EMA(200) sign agreement"). The threshold would be **frozen before per-regime evaluation**.

### 6.2 Axis B — Volatility level (binary)

- **High-vol** vs **Normal-vol.**
- Pre-entry observable; rolling realized-vol percentile on completed 15m or 1h bars vs a fixed-length reference window.
- Threshold: **NOT proposed in Phase 3m.** A successor regime-first phase would declare a fixed quantile cutoff (e.g., 80th percentile vs 20th percentile, with the *reference-window length* as the only hyperparameter). Frozen before per-regime evaluation.

### 6.3 Axis C — Funding stress (binary; optional)

- **Funding-stress** vs **Normal-funding.**
- Pre-entry observable; funding-rate-Z-score magnitude on the most recent completed funding event (already in v002).
- Threshold: **NOT proposed in Phase 3m.** A successor regime-first phase could either (i) reuse D1-A's |Z| ≥ 2.0 threshold (preserves Phase 3g binding spec; consistent with project precedent) OR (ii) declare a separate threshold for the regime axis distinct from D1-A's signal threshold. Either choice frozen before per-regime evaluation.

### 6.4 Optional Axis D — Liquidity / spread stress (binary; deferred)

- **Liquidity-stress** vs **Normal-liquidity.**
- Pre-entry observable in principle, but **requires data NOT in v002** (spread / depth / impact). Including this axis would require operator authorization for v003 data work, which is **NOT proposed by Phase 3m**.
- Therefore: defer Axis D until external spread / depth evidence is available.

### 6.5 Taxonomy size rationale

- 2 axes × 2 levels each = 4 regimes.
- With 36-month R-window × 2 symbols and per-symbol fold-level R-window evaluation (6 folds × 2 symbols = 12 fold-symbol cells), each regime has ~3 fold-symbol cells of evidence — **sample size is already strained** at 4 regimes.
- 3 axes × 2 levels each = 8 regimes — sample size collapses to ~1.5 fold-symbol cells per regime — **inadequate** for §11.2 fold-consistency evaluation.
- **Therefore the first-pass taxonomy must be 2-axis at most** (4 regimes); an optional third axis is research-evidence-only, not gate-evaluation-ready.
- Any successor regime-first phase that proposes more than 2 binary axes for gate-evaluation must explicitly justify the sample-size implications.

### 6.6 Why this taxonomy is "minimal first-pass" not "final"

- The proposed taxonomy is **interpretable and falsifiable** (per §4.5).
- It is **NOT** validated for stationarity, regime-stability, or per-regime sample-size adequacy on real R-window data (Phase 3m is docs-only; no backtest run).
- A successor regime-first phase would (a) re-evaluate axes selection, (b) declare thresholds in writing, (c) run sample-size-adequacy analysis on v002 R-window labels, (d) freeze definitions before per-regime evaluation. None of (a)-(d) are authorized by Phase 3m.

---

## 7. Mapping retained strategies to plausible regimes

For each retained-evidence candidate, this section discusses (i) which regime each was implicitly trying to exploit, (ii) which regime likely hurt it, (iii) whether the empirical evidence suggests a regime-dependent mechanism, (iv) whether that evidence is **strong**, **weak**, or **only speculative**.

**Important framing:** This section is **interpretive**, not prescriptive. The mappings below describe a hypothesis structure that *could* be tested in a future regime-first phase under §4 anti-circular-reasoning discipline. **Phase 3m does NOT propose to backtest these hypotheses.** None of these mappings constitute candidate rescue framing; all retained-evidence candidates remain framework-failed under their existing verdicts.

### 7.1 H0 (V1 baseline)

- **Implicit target regime:** Trending markets with breakout-continuation behavior; high-vol expansion phases.
- **Likely hurt by:** Chop / non-trend regime (V1 spec failure mode #1); high-vol with whipsaws.
- **Evidence for regime-dependence:** F4 2024H1 worst per-fold cell consistently across V1 family. R3's Phase 2l F2-F3 first-positive-expR cells plausibly track trend-strong / chop-low periods.
- **Evidence strength:** **Weak-to-moderate.** Per-fold pattern is suggestive but not rigorously regime-decomposed. The H0 spec was not designed with explicit regime classification; the per-fold pattern is consistent with trend-vs-chop regime conditioning but does not prove it (could equally reflect look-back-window edge effects).

### 7.2 R3 (V1 baseline-of-record)

- **Implicit target regime:** Same as H0 (trending breakouts) but with exit-machinery (Fixed-R + 8-bar time-stop) that limits damage in unfavorable regimes.
- **Likely hurt by:** Same as H0; less severely because the time-stop caps stagnation losses.
- **Evidence for regime-dependence:** R3 broad-based PROMOTE across all 6 BTC + ETH regime-symbol cells; cost-robust at HIGH; bit-identical MARK vs TRADE_PRICE. R3's improvement appears regime-robust at the level of "smaller per-trade loss when wrong" but regime-dependent at the level of "positive expR fold occurrence" (only F2-F3 BTC; F1, F4-F5 still negative).
- **Evidence strength:** **Moderate.** R3's robustness is strong evidence that the *exit-machinery improvement* is regime-independent; but the *aggregate-edge sign* is regime-dependent. Regime-first work would likely confirm this — without changing R3's status as the strongest single candidate evidence.

### 7.3 R1a (volatility-percentile setup)

- **Implicit target regime:** Volatility-compression regime (Phase 2j §C explicit hypothesis: low-vol percentile setup).
- **Likely hurt by:** High-vol expansion regime; symbol asymmetry on BTC.
- **Evidence for regime-dependence:** Compression-selection mechanically correct (100% of entries at percentile ≤ 25% per Phase 2m). ETH-favorable / BTC-degrading symbol asymmetry. ETH V-window first-ever positive netPct (+0.69%); BTC degraded vs R3.
- **Evidence strength:** **Moderate-to-strong** for the volatility-compression regime axis (R1a's mechanism explicitly implements a volatility-percentile predicate). The remaining open question is whether the BTC degradation is regime-related (different vol-regime distribution) or symbol-structure-related (different microstructure).

### 7.4 R1b-narrow (bias-strength magnitude)

- **Implicit target regime:** Trend-strong regime (Phase 2r explicit hypothesis: only-take-trades-when-bias-magnitude-is-strong).
- **Likely hurt by:** Sample-size; small-sample noise.
- **Evidence for regime-dependence:** Formal §10.3.a-on-both PROMOTE (first such); R3-anchor near-neutral marginal contribution. 65–70% trade-count drop suggests the trend-strength filter is correctly selective but the residual edge is small.
- **Evidence strength:** **Weak-to-moderate.** R1b-narrow's mechanism explicitly implements a trend-strength predicate; the formal PROMOTE supports the regime-dependence story but the small-sample caveats limit confidence.

### 7.5 R2 (pullback-retest)

- **Implicit target regime:** Trending markets with controlled pullback structure (entry geometry assumes confirmed pullback).
- **Likely hurt by:** Cost regime (§11.6 cost-sensitivity FAILED at HIGH on both symbols); fast / wide-spread / high-vol periods amplify slippage on small-R-distance entries.
- **Evidence for regime-dependence:** R2 cleared §10.3 at MEDIUM with M1 + M3 mechanism support. Failed §11.6 at HIGH. Edge proportional to slippage band — high-vol / wide-spread periods consume the gain.
- **Evidence strength:** **Strong** for the cost-stress regime axis (the §11.6 failure is precisely a cost-regime-dependence finding); **weak** for the trend-strength axis (R2 was not specifically calibrated to trend regimes; the cost-fragility issue dominates).

### 7.6 F1 (mean-reversion-after-overextension)

- **Implicit target regime:** Chop with overextension (Phase 3b §2.3 hypothesis); periods where SMA(8) frozen target is reachable from 1.75×ATR-displaced entry.
- **Likely hurt by:** Sustained trend (overextension continues rather than reverts); high-vol shocks (TARGET unreachable before TIME_STOP). M2 contradicts the chop-regime hypothesis on BTC (F1 stops out *more* in BTC chop than H0 does).
- **Evidence for regime-dependence:** M3 PASS (TARGET subset profitable when isolated) suggests *some* regime captures the mean-reversion behavior. M2 BTC FAIL falsifies F1's specific operationalization of "chop". Per-fold heterogeneity exists (Phase 3d-B2 §8.2) but is not as cleanly regime-tracked as D1-A's.
- **Evidence strength:** **Moderate.** TARGET-subset profitability is real (M3 PASS); the regime that produces TARGET reachability is not the same as F1's spec-level definition of "chop". A correctly-defined chop regime might separate TARGET-friendly from STOP-friendly cells — but constructing that regime from F1's exit mix would be the post-hoc rescue §4.4 forbids.

### 7.7 D1-A (funding-aware contrarian)

- **Implicit target regime:** Post-extreme-funding mean-reversion (|Z_F| ≥ 2.0 trigger); short hold (≤ 32 bars / 8 hours).
- **Likely hurt by:** Periods where extreme funding *continues to extend* rather than reverts (e.g., persistent crowded-position regimes). High-vol shocks where 1.0×ATR stop fires before mean-reversion drift develops. Cost-stress at HIGH (cond_iv FAIL).
- **Evidence for regime-dependence:** **Strong per-fold heterogeneity:** BTC F3 2023H1 +0.62 R (PF 2.03) vs F5 2024H1 −0.98 R (PF 0.16) on the same locked spec. M1 BTC h=32 PASS confirms the directional drift exists; the per-fold heterogeneity confirms it does not exist *every* fold.
- **Evidence strength:** **Strong** for some regime-dependence claim. **Weak** for any *specific* regime axis until §4 anti-circular-reasoning discipline is honored — defining "the regime where D1-A's M1 is strong" by inspecting D1-A's per-fold outcomes is exactly the rescue framing forbidden by §4.3 / §4.4.

### 7.8 Cross-candidate summary

| Candidate | Implicit target regime | Likely-hurt regime | Evidence strength for regime-dependence |
|-----------|------------------------|---------------------|------------------------------------------|
| H0 | Trending / breakout | Chop / whipsaw | Weak-to-moderate |
| R3 | Trending (with damage-control exit) | Chop (less severely than H0) | Moderate (regime-robust at exit-machinery; regime-dependent at aggregate-sign) |
| R1a | Vol-compression | Vol-expansion / BTC-microstructure | Moderate-to-strong (mechanism explicitly implements vol-percentile predicate) |
| R1b-narrow | Trend-strong | Sample-size-noise | Weak-to-moderate |
| R2 | Pullback-in-trend | Cost-stress / wide-spread | **Strong** (§11.6 cost-regime-dependence empirically demonstrated) |
| F1 | Chop with mean-reversion | Sustained trend / high-vol shocks | Moderate (M3 PASS evidence; M2 falsified F1's specific chop operationalization) |
| D1-A | Post-extreme-funding mean-reversion | Persistent crowded-position / vol-shock / cost-stress | **Strong** (per-fold heterogeneity F3 +0.62 vs F5 −0.98 on same spec) |

The aggregate picture: **multiple retained-evidence candidates have plausible regime-dependent mechanisms, and the per-fold heterogeneity is not consistent with "the spec is wrong" alone**. This is suggestive evidence for a regime-first framework being a sensible next research direction — **subject to the §4 anti-circular-reasoning discipline that any regime axes be defined first, in writing, from first principles, before any per-regime evaluation**.

The aggregate picture is **NOT** strong enough to authorize a regime-first execution phase under Phase 3m. The interpretive mappings above are research-evidence quality only.

---

## 8. Data requirements

### 8.1 What v002 already supports

The committed v002 datasets cover all four near-term-relevant regime axes:

- **§5.1 Volatility level** — 15m + 1h klines suffice (rolling realized-vol; ATR(20) already computed in pipeline).
- **§5.3 Trend strength** — 1h klines (slope-3, EMA-stack) suffice.
- **§5.4 Trend direction** — same as §5.3 plus signed.
- **§5.5 Chop / range** — 15m + 1h klines (range / ATR ratio; consecutive same-direction-close streak) suffice.
- **§5.6 Funding stress** — funding-rate-events dataset (already in v002).
- **§5.9 Time-of-day / funding-window proximity** — pure timestamp features; no data needed beyond v002.
- **§5.10 BTC / ETH relative behavior** — both BTC and ETH 15m klines (in v002).

A docs-only regime-first taxonomy memo, sample-size-adequacy analysis on v002 labels, and per-regime decomposition of *existing* retained-evidence candidate trade logs (no re-running of backtests; reading existing trade-log artifacts) **could in principle be produced from v002 alone**. Phase 3m does NOT authorize this work; it confirms feasibility.

### 8.2 What v002 does NOT support

- **§5.7 Spread / slippage stress** — not in v002. Bid-ask spread, depth, impact tick data are not part of v002. Phase 3l confirmed these are operator-driven external evidence outside docs-only scope.
- **§5.8 Liquidity (full)** — volume is in v002; open-interest is not. Open-interest is publicly available via the Binance REST API (`/futures/data/openInterestHist`) but accessing it requires either operator-driven external data work or v003 dataset versioning.

### 8.3 Future implementation requirements (NOT authorized by Phase 3m)

If a future operator-authorized regime-first execution phase eventually proceeds, the following data-layer work would likely be needed (each item is informational; **none is authorized by Phase 3m**):

- **New derived regime labels** as a v002-extension (or v003 if cross-version compatibility is needed). The labels would be deterministic functions of v002 inputs; they would be regenerated if regime definitions change.
- **5m data** — explicitly **NOT recommended** by Phase 3m for regime-first work (see §11 below).
- **Tick / spread / depth data** — required only if §5.7 spread-stress axis is added; would need v003 dataset version.
- **v003 dataset version** — would require operator authorization of a separate data-layer phase. Phase 3m explicitly does NOT authorize v003 work.
- **Stricter timestamp / leakage controls** — regime labels must be computed on completed bars only (per Phase 2f §11.3.5 strategy-conformance discipline). The label-computation timestamp must precede the entry decision; this is a stricter implementation discipline than the existing kline / 1h / mark-price / funding-event timestamp policy but uses the same primitive policy.

### 8.4 Phase 3m data scope

Phase 3m **reads** existing internal documentation (`docs/`) and existing `src/prometheus/research/backtest/` source files. Phase 3m **does NOT**: read, write, or commit any `data/` artifact; download any new dataset; generate any derived regime labels; touch the v002 datasets in any way; access any private or authenticated Binance API. The Phase 3m memo is fully self-contained at the documentation level.

---

## 9. Validation design for any future regime-first phase

The following requirements are binding **preconditions** for any future regime-first execution phase. **Phase 3m does NOT authorize such a phase.** This section documents what discipline would be required if the operator chooses to authorize one.

### 9.1 Predeclared regime definitions

- Regime axes (which features), regime levels (binary / ternary), and regime thresholds (numeric values) all **declared in writing** in a phase-spec memo *before* any per-regime evaluation.
- The spec memo must include the rationale for each threshold (academic convention; structural reason; pre-registered hypothesis). "Threshold tuned to optimize per-regime outcome" is **forbidden**.
- The threshold values must be **frozen** before any per-regime backtest. Phase 2j §C.6 / §11.3.5 single-spec discipline applies in regime-first form.

### 9.2 No post-hoc threshold tuning

- Once regime-first per-regime evaluation begins, **regime thresholds cannot be changed**. The §11.3.5 binding rule applies verbatim.
- If a regime threshold turns out to be poorly calibrated, the correct response is to **document the failure as research evidence**, not to retune.
- Any regime-first variant produced by retuning is a **separate candidate** requiring its own framework gate evaluation, not an iteration of the original.

### 9.3 Fold-level stability

- Per-fold (per Phase 2f §11.2) consistency must be evaluated *per regime*. A regime-first verdict cannot rest on a single regime's single-fold positive expR; it must be regime-stable across folds and (subject to §11.4) across symbols.
- The per-regime sample-size-adequacy threshold should be operator-declared (suggested rule: ≥ 30 trades per regime per symbol in the R-window; rejected if below).

### 9.4 Out-of-sample checks

- Phase 2f §11.3 V-window no-peeking applies verbatim to regime-first evaluation.
- The V-window must be evaluated **only after** R-window per-regime evaluation is complete and the regime-first variant has cleared the R-window gate.
- Per-regime V-window outcomes must satisfy the same §10.3 / §10.4 / §11.4 / §11.6 thresholds as single-regime variants.

### 9.5 Sufficient sample size per regime

- The §6.5 calculation suggests the maximum near-term taxonomy is **2-axis × 2-level = 4 regimes**. A 3-axis taxonomy (8 regimes) collapses sample size below feasibility.
- Even 4 regimes implies ~3 fold-symbol cells per regime in the R-window; this is at the lower bound of §11.2 fold-consistency interpretability. The successor regime-first spec phase must justify that the chosen taxonomy is sample-size-feasible *before* per-regime evaluation begins.

### 9.6 Cost-resilience at §11.6

- §11.6 = 8 bps HIGH per side applies to any regime-first variant. **No cost-policy revision is implied or authorized by Phase 3m.**
- If a regime-first variant fires only in regimes where per-trade R-distance is small (e.g., low-vol regime; range-bound regime), it inherits the R2-style and F1-style cost-fragility risks documented in Phase 2y / Phase 2w / Phase 3d-B2.
- The successor regime-first spec phase must explicitly evaluate per-regime cost-sensitivity (LOW / MED / HIGH at the §11.6 calibrated values).

### 9.7 No retrospective target-subset selection

- Per §4.4: TARGET-exit-conditional partitioning is forbidden as a regime label. Regime axes must be pre-entry observable.
- Outcome statistics (TARGET-exit fraction; STOP-exit fraction; TIME_STOP-exit fraction) per regime are **acceptable diagnostics** in the per-regime gate-evaluation phase, but they cannot be used to define regimes.

### 9.8 No candidate rescue framing

- Per §4.3: regime axes must be defined first; existing retained-evidence candidates can be evaluated under the framework second. Phase 3m affirms that R2 / F1 / D1-A's framework verdicts are NOT contingent on any regime-first re-evaluation; they remain framework-failed under their existing verdicts even if a future regime-first phase produces a candidate that uses similar mechanisms in some regime.
- A regime-first variant that uses (e.g.) "F1's mean-reversion target in the chop-regime only" is a **separate candidate** requiring its own framework gate evaluation, not an F1-prime.

### 9.9 Validation-design summary

| Requirement | Source | Binding rule |
|-------------|--------|--------------|
| Predeclared regime definitions | §4.1 / §9.1 | Yes |
| No post-hoc threshold tuning | §4.5 / Phase 2f §11.3.5 | Yes |
| Fold-level stability | Phase 2f §11.2 / §9.3 | Yes |
| Out-of-sample checks | Phase 2f §11.3 / §9.4 | Yes |
| Sufficient sample size per regime | §6.5 / §9.5 | Yes |
| Cost-resilience at §11.6 | Phase 2y / Phase 3l / §9.6 | Yes |
| No retrospective target-subset selection | §4.4 / §9.7 | Yes |
| No candidate rescue framing | §4.3 / §9.8 | Yes |

A future regime-first phase that does NOT explicitly affirm all eight requirements is not authorized by this memo. Phase 3m does not pre-authorize any successor phase; it documents the discipline that any successor would have to honor.

---

## 10. Failure modes

A regime-first framework introduces specific risks. Phase 3m enumerates them so any future authorization is informed.

### 10.1 Overfitting

- Regime-classifier hyperparameters multiply the strategy parameter space. Even at 2 binary axes (4 regimes), the classifier introduces look-back-window length, threshold value, and possibly hysteresis parameters per axis.
- The R-window is 36 months × 2 symbols. The effective sample size per regime is small (§6.5). Standard ML overfitting metrics (degrees-of-freedom budget; held-out validation; cross-validation under stationarity) all imply that 4-regime frameworks are at the edge of what 36-month data can support, and 8-regime frameworks are over the edge.
- **Mitigation:** §9.1 + §9.2 binding rules. The regime-first spec memo must declare the classifier hyperparameters before per-regime evaluation; any tuning is a separate candidate.

### 10.2 Circular reasoning

- The post-hoc regime definition pattern (§4.2 / §4.3 / §4.4) is the most dangerous failure mode. Phase 3m explicitly forbids it; the binding rules are §4.1, §4.3, §4.4.
- **Mitigation:** §4 anti-circular-reasoning discipline as binding precondition.

### 10.3 Small sample size per regime

- §6.5 calculation: 4 regimes ≈ 3 fold-symbol cells per regime. This is at the edge of §11.2 fold-consistency interpretability.
- Per-regime per-fold outcomes have wide confidence intervals; a regime that "looks profitable in 2 of 3 folds" may not be statistically distinguishable from "a fair coin in a regime that doesn't matter".
- **Mitigation:** §9.5 binding rule. Operator-declared sample-size-adequacy threshold; regimes below threshold rejected.

### 10.4 Unstable regimes

- Regime labels that flicker (whipsaw) within the timescale relevant to the dispatched strategy are operationally useless. A regime classifier that flips state every 2 bars cannot calibrate a strategy that fires once every 8 bars.
- **Mitigation:** §4.5 binding rule. Hysteresis + minimum-duration constraints. Regime-stability metric (e.g., median regime duration) must be reported in the regime-first spec memo.

### 10.5 Cost amplification

- Regime-shift-detection latency adds a systematic cost. Entries / exits at regime boundaries are typically less favorable (regime change is itself a market-microstructure event with elevated spread / impact).
- A regime-first dispatch that triggers strategy-mode-switches introduces transition-cost overhead not present in single-regime strategies.
- **Mitigation:** §9.6 binding rule. Per-regime cost-sensitivity sweep (LOW / MED / HIGH) with §11.6 = 8 bps HIGH preserved.

### 10.6 Regime labels lagging real-time

- Live regime classification on completed bars only (per Phase 2f §11.3.5) means the regime label for the bar being decided is computed from prior-bar features.
- The lag is the bar timeframe (15m or 1h); regime transitions during the latency window are missed.
- **Mitigation:** Acceptable as a structural cost; the lag-budget is similar to the strategy's existing completed-bar-only discipline.

### 10.7 Phase 4 / live-state dependency

- Live regime tracking requires Phase 4 runtime / state / persistence work (regime-classifier state must be persisted across restarts; transition events must be logged; regime-aware position management must respect the safety state model).
- **Phase 4 is currently NOT authorized.** A regime-first execution phase is therefore structurally Phase-4-dependent — even research-only regime-first backtesting can be conducted without Phase 4, but live deployment cannot.
- **Mitigation:** Operator policy. Phase 3m does NOT recommend lifting Phase 4 deferral. A successor regime-first phase that limits itself to research-only backtesting on v002 R-window data is feasible without Phase 4; live deployment is out of scope.

### 10.8 False confidence from pretty segmentation

- Regime-decomposed per-fold tables can look more "explanatory" than aggregate single-strategy results — every per-regime cell has its own narrative. This is **dangerous** because it invites confirmation bias.
- A regime-first framework that "explains" past failures by retrospective segmentation is exactly the post-hoc rescue framing forbidden by §4. Pretty segmentation is not validation.
- **Mitigation:** §9.4 V-window no-peeking; §9.5 sample-size-adequacy gate; §9.7 no retrospective target-subset selection. The disciplined response to "the regime-decomposition looks great" is to demand the V-window outcome and reject if V fails.

### 10.9 Failure-mode summary

| Failure mode | Mitigation source | Binding |
|--------------|--------------------|---------|
| Overfitting | §9.1 + §9.2 | Yes |
| Circular reasoning | §4 | Yes |
| Small sample size per regime | §9.5 | Yes |
| Unstable regimes | §4.5 | Yes |
| Cost amplification | §9.6 | Yes |
| Regime labels lagging | Completed-bar discipline | Yes |
| Phase 4 / live-state dependency | Operator policy | Operator-driven |
| False confidence from pretty segmentation | §9.4 + §9.5 + §9.7 | Yes |

Phase 3m affirms that all binding mitigations apply to any successor regime-first phase. The Phase 4 / live-state dependency remains operator-driven; it is not addressed by Phase 3m and is NOT authorized.

---

## 11. Relationship to 5m timeframe

**Phase 3m does NOT authorize 5m timeframe research as part of regime-first work.** 5m work is a separate operator-driven future direction.

### 11.1 Why 5m should not become a strategy signal yet

- The locked 15m / 1h timeframe decomposition has been the framework for V1 / F1 / D1-A. Switching to 5m for regime-first work would compound two unknowns simultaneously (new framework + new timeframe).
- 5m signal-frequency would amplify cost-aggregation risk (the F1-shape catastrophic-frequency × per-trade-loss aggregation). Any 5m candidate would need to demonstrate cost-resilience at HIGH slippage with 3× the trade frequency — a higher bar than the current 15m setup.
- 5m data is **NOT in v002**; obtaining it requires v003 dataset work (operator-authorized future phase).

### 11.2 Why 5m may be useful later as an execution / timing diagnostic

- 5m could in principle inform sub-bar timing diagnostics: how does a 15m-fired strategy's intra-bar fill quality vary? Is the next-bar-open assumption realistic?
- These diagnostics are **execution-realism** questions, not strategy-signal questions. They would inform paper/shadow / Phase 4 work, not regime classification.
- **Not authorized by Phase 3m.**

### 11.3 Why a separate 5m feasibility memo can be considered later

- A future operator-driven 5m feasibility memo could enumerate what v003 5m data work would require, expected sample-size implications, expected cost-amplification, and whether 5m diagnostic use (NOT signal use) is worth the data-layer cost.
- **Phase 3m does NOT authorize a 5m feasibility memo.** The operator may at any future time authorize one as a separate docs-only phase.

### 11.4 5m relationship summary

| Question | Phase 3m position |
|----------|-------------------|
| Should 5m become a regime-first signal? | NO — confounds two unknowns; raises cost-aggregation risk |
| Should 5m be added to v003? | NOT authorized by Phase 3m; operator-driven decision |
| Is 5m useful for execution-realism diagnostics later? | Possibly; reserved for paper/shadow / Phase 4 framing if ever authorized |
| Should Phase 3m authorize a 5m feasibility memo? | NO |

---

## 12. Relationship to ML

**Phase 3m does NOT authorize ML feasibility work.** ML belongs after regime-first thinking is mature, not as a parallel track.

### 12.1 Why ML is not the next step

- Phase 3k §8.5 / Phase 3l §15.6 already documented ML feasibility risks: leakage; overfitting; small effective sample size; non-stationarity (Phase 3j per-fold heterogeneity is direct evidence); cost-sensitivity (ML signal frequency does not lower fees / slippage); explainability (mechanism-falsifiability discipline not satisfied by default).
- A poorly-disciplined ML attempt could produce a fourth framework-fail in shorter time than V1 / F1 / D1-A took, or worse, could produce an apparent PROMOTE that is actually a leakage artifact.
- ML methods do not fix regime-classification discipline; they implicitly assume regimes are stable enough that learned features generalize. **Regime-first thinking is logically prior to ML feasibility.**

### 12.2 Why regime-first can later inform ML feasibility

- A successor regime-first phase that produces validated, falsifiable, sample-size-adequate, cost-resilient regime axes would provide a structured feature space within which ML methods could later operate.
- The regime-first axes would be interpretable; ML applied within a single regime would have a smaller, more stationary feature space than ML applied across all regimes.
- **This sequencing is informational only**; Phase 3m does NOT authorize either direction.

### 12.3 What ML feasibility would later require

- Strict purged + embargoed cross-validation aligned to R-window structure.
- Effective sample-size analysis (sample-to-feature-count ratio).
- Stationarity testing (per-fold feature-distribution shift; per-regime label-distribution shift).
- Cost-sensitivity integration (any ML signal must demonstrate cost-resilience at HIGH slippage in expectation; not retrospectively).
- Explainability requirements (model-class restrictions; falsifiable mechanism prediction analogues to M1 / M2 / M3).
- **Not authorized by Phase 3m.**

### 12.4 ML relationship summary

| Question | Phase 3m position |
|----------|-------------------|
| Is ML the right next step? | NO |
| Can regime-first thinking inform later ML feasibility? | YES (sequencing-informational only; not authorized) |
| Should Phase 3m authorize an ML feasibility memo? | NO |
| Is ML an immediate escape hatch from V1 / F1 / D1-A failures? | NO (well-documented severe risks remain unaddressed) |

---

## 13. Operator decision menu after Phase 3m

Seven options; Phase 3m recommends exactly one.

### 13.1 Option A — Remain paused

**What it would answer:** What state should the project be in while the operator decides the next strategic move?

**Why it may be useful:**

- Compatible with Phase 3m's interpretive findings: regime-dependence is plausible but not validated; anti-circular-reasoning discipline is high; sample-size constraints are tight.
- Compatible with Phase 3k's primary recommendation; consistent with Phase 3l's affirmation that cost-policy is conservative-but-defensible (no calibration crisis to act on).
- The operator has now explored Phase 3l (cost-policy review) and Phase 3m (regime-first thinking) — both are docs-only and both leave the project's deployment state unchanged. Returning to remain-paused after exploration is operationally natural.

**Why it may be dangerous:**

- Project loses momentum; strategic clarity may degrade. The operator has now had three consecutive opportunities to authorize active research (Phase 3l → Phase 3m → next decision) and has chosen docs-only paths each time.

**Violates current restrictions?** No.

**Should be recommended now?** **YES — primary recommendation.** The disciplined response after a docs-only exploration phase is to consolidate the new thinking and remain paused unless a specific operator-developed hypothesis emerges.

### 13.2 Option B — Formal regime-first spec / planning memo (docs-only)

**What it would answer:** Should the regime-first ideas in Phase 3m be formalized into a binding spec memo (analogous to Phase 3b for F1 or Phase 3g for D1-A), with declared regime axes, declared thresholds, declared validation plan, and declared sample-size-adequacy gate?

**Why it may be useful:**

- A formal regime-first spec memo is the natural successor to Phase 3m if the operator wants to commit to the regime-first direction.
- The spec memo would (a) declare regime axes from §5 candidates, (b) declare thresholds in writing under §4 / §9.1 anti-circular-reasoning discipline, (c) declare the sample-size-adequacy gate, (d) declare the validation plan including V-window no-peeking, (e) freeze all definitions before any per-regime evaluation.
- The spec memo itself is docs-only; it does not authorize backtesting, implementation, or execution.

**Why it may be dangerous:**

- The §4 + §9 + §10 binding rules are demanding. A formal spec memo that does not respect them risks producing an over-confident regime-first framework that framework-fails when executed (worst-case fourth consecutive framework-fail).
- The Phase 4 / live-state dependency (§10.7) remains unresolved. A regime-first execution phase eventually requires Phase 4 work; without operator authorization of Phase 4, the regime-first path is research-only-bounded.
- Treadmill risk: each docs-only memo (Phase 3k → 3l → 3m → 3m-prime) postpones the strategic question without resolving it. The right response to repeatedly elevated treadmill risk is more pause, not more memos.

**Violates current restrictions?** No (a formal spec memo is docs-only; Phase 3m itself is the same shape).

**Should be recommended now?** **NO.** Phase 3m's interpretive findings do not yet reach the threshold of "operator-developed falsifiable hypothesis with frozen-in-writing thresholds" that a Phase 3b- or Phase 3g-style spec memo requires. Recommended only if the operator independently judges that the regime-first thinking has crystallized into a specific operator-developed hypothesis ready for formal commitment.

### 13.3 Option C — 5m timeframe feasibility memo (docs-only)

**What it would answer:** Should a docs-only 5m feasibility memo enumerate what v003 5m data work would require?

**Why it may be useful:** Per §11.

**Why it may be dangerous:** Per §11.

**Violates current restrictions?** **YES — Phase 3m brief explicitly forbids** "Do not authorize ... 5m timeframe work."

**Should be recommended now?** **NO. Forbidden by Phase 3m brief.**

### 13.4 Option D — ML feasibility memo (docs-only)

**Why it may be useful / dangerous:** Per §12.

**Violates current restrictions?** **YES — Phase 3m brief explicitly forbids** "Do not authorize ... ML feasibility ..."

**Should be recommended now?** **NO. Forbidden by Phase 3m brief.**

### 13.5 Option E — New strategy-family discovery (Phase 3a-style)

**Violates current restrictions?** **YES — Phase 3m brief explicitly forbids** "Do not authorize ... new strategy discovery ..."

**Should be recommended now?** **NO. Forbidden by Phase 3m brief.**

### 13.6 Option F — Cost-model revision memo (docs-only)

**Violates current restrictions?** **YES — Phase 3m brief explicitly forbids** "Do not authorize ... formal cost-model revision."

**Should be recommended now?** **NO. Forbidden by Phase 3m brief.**

### 13.7 Option G — Paper/shadow or Phase 4

**Violates current restrictions?** **YES — every brief since Phase 0** explicitly forbids paper/shadow / Phase 4 / live-readiness / deployment work without operator policy lifting that deferral.

**Should be recommended now?** **NO. Forbidden.**

### 13.8 Decision menu summary

| Option | Description | Violates Phase 3m brief? | Recommended now? |
|--------|-------------|:-:|:-:|
| **A** | Remain paused | NO | **YES (primary)** |
| B | Formal regime-first spec / planning memo (docs-only) | NO | NO |
| C | 5m timeframe feasibility memo (docs-only) | YES | NO (forbidden) |
| D | ML feasibility memo (docs-only) | YES | NO (forbidden) |
| E | New strategy-family discovery memo (docs-only) | YES | NO (forbidden) |
| F | Cost-model revision memo (docs-only) | YES | NO (forbidden) |
| G | Paper/shadow or Phase 4 | YES | NO (forbidden) |

### 13.9 Recommended next operator decision

**Phase 3m recommends: REMAIN PAUSED.**

The disciplined response after Phase 3m's docs-only regime-first thinking is to consolidate the framework-level reflection and surrender strategic direction to the operator. Phase 3m's interpretive findings do not yet reach the threshold of an operator-developed falsifiable hypothesis ready for formal Phase 3b- / Phase 3g-style commitment. The operator may at any future time authorize a separate docs-only formal regime-first spec memo (Option B) with operator-developed regime-axis selection, operator-committed thresholds, and operator-explicit anti-circular-reasoning affirmation. Phase 3m does not pre-authorize Option B; Phase 3m's existence does not imply that Option B is the right next step.

The recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 14. Explicit preservation list

Phase 3m is docs-only and explicitly preserves all of the following verbatim:

- **No threshold changes.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side preserved. `DEFAULT_SLIPPAGE_BPS` map (LOW=1.0 / MED=3.0 / HIGH=8.0 per side) preserved. `taker_fee_rate=0.0005` preserved.
- **No strategy-parameter changes.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A spec axes preserved verbatim.
- **No project-lock changes.** §1.7.3 locks preserved verbatim.
- **No prior verdict changes.** R3 baseline-of-record / H0 framework anchor / R1a / R1b-narrow / R2 / F1 / D1-A retained-research-evidence preserved verbatim. R2 FAILED, F1 HARD REJECT, D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **No backtests.** No engine invocation; no candidate-cell run; no control reproduction; no per-regime decomposition computed on existing trade-log artifacts within Phase 3m.
- **No code change.** No file in `src/`, `tests/`, or `scripts/` touched. `cost-modeling.md`, `backtesting-principles.md`, `data-requirements.md`, `dataset-versioning.md`, `phase-gates.md`, `technical-debt-register.md`, `current-project-state.md`, `ai-coding-handoff.md` UNCHANGED.
- **No MCP / Graphify / `.mcp.json` activation.** No MCP server enabled; no Graphify integration; no `.mcp.json` file created or modified.
- **No credentials.** No production / sandbox / testnet API keys requested, created, or used. No `.env` file modified. No secrets in any committed file. No authenticated Binance API calls. No private endpoints accessed.
- **No exchange-write paths.** No exchange-write capability proposed, implemented, or enabled.
- **No `data/` commits.** Phase 3m commits are limited to two new `docs/00-meta/implementation-reports/` files (this memo + closeout report).
- **No next phase started.** Phase 3m is docs-only and terminal-as-of-now. No Phase 3n, no Phase 4, no formal regime-first spec phase, no 5m feasibility phase, no ML feasibility phase, no cost-model revision phase, no new strategy-family discovery phase, no paper/shadow planning, no live-readiness, no deployment authorized.

---

**End of Phase 3m regime-first research framework memo.** Phase 3m documents (a) why regime-first is being considered after the V1 + F1 + D1-A framework-fail pattern, (b) the §4 anti-circular-reasoning principles binding any future regime-first work, (c) candidate regime axes (§5) with associated evidence / data / risks, (d) a minimal first-pass illustrative 2-axis taxonomy (§6) without thresholds, (e) interpretive mappings of retained-evidence candidates to plausible regime stories (§7) with strong / weak / speculative tags, (f) data requirements (§8) confirming v002 sufficiency for the docs-only level, (g) the binding validation-design preconditions (§9) for any future regime-first phase, (h) failure modes (§10) including overfitting / circular reasoning / small sample size / Phase-4-dependency, (i) the relationship to 5m and ML directions (§11 + §12) — neither authorized — and (j) the recommended next operator decision (§13): **remain paused** as primary, with formal regime-first spec/planning memo (docs-only) as a non-recommended secondary alternative if the operator independently develops a falsifiable hypothesis. R3 remains baseline-of-record; H0 remains framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence; §11.6 = 8 bps HIGH preserved; §1.7.3 locks preserved verbatim. **No threshold changes. No strategy-parameter changes. No project-lock changes. No prior verdict revised. No backtest run. No code / tests / scripts / data / paper-shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credential / exchange-write change. No next phase started.** Phase 3m is docs-only; the operator decides whether and when to authorize any subsequent phase. Awaiting operator review.
