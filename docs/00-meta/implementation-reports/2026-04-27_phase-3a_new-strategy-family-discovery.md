# Phase 3a — New Strategy-Family Discovery Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-position max; one-symbol-only; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2p consolidation memo §§ C.1 / D / F.4 (R3 baseline-of-record; future-resumption pre-conditions; family-shift framing); Phase 2x family-review memo (V1 breakout family likely at useful ceiling under current framework; Option D — new strategy-family planning — appropriate after Option C clarity OR operator-independent family-ceiling confirmation); Phase 2y slippage / cost-policy review memo (Option (a) — §11.6 = 8 bps HIGH stays unchanged; Phase 2x Option C now closed; framework-calibration question resolved without threshold revision); `docs/03-strategy-research/v1-breakout-strategy-spec.md` (decisions: rules-based, supervised); `docs/05-backtesting-validation/backtesting-principles.md` (no leakage; chronological integrity; cost realism mandatory); `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` (Gate 1 data integrity; Gate 5 robustness; Gate 6 exit-model comparison); `docs/04-data/data-requirements.md` (v002 dataset coverage: BTCUSDT/ETHUSDT 15m + derived 1h + mark-price + funding + exchangeInfo); `docs/04-data/dataset-versioning.md` (any new feature dataset requires a versioned manifest); `docs/05-backtesting-validation/cost-modeling.md` (all validation net of cost; futures research includes funding); `.claude/rules/prometheus-core.md` (v1 rules-based, not self-learning, supervised, BTCUSDT-only live).

**Phase:** 3a — Docs-only **discovery review** to identify and rank possible non-breakout strategy families for any potential next research arc. **Family-selection only**, not strategy execution, not backtesting, not parameter search, not live-readiness.

**Branch:** `phase-3a/new-strategy-family-discovery`. **Memo date:** 2026-04-27 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal.** R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 remain retained research evidence per Phase 2p §D / Phase 2s §13 / Phase 2w §16.3. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3a is deciding

Phase 3a is **family-selection-only**, not candidate-execution and not even candidate-spec-writing. It is the natural successor to the Phase 2x family-level review memo, which framed five next-decision options at the post-Phase-2w boundary:

- Option A — remain paused (Phase 2x primary recommendation),
- Option B — one more narrowly-justified breakout-family research phase,
- Option C — independent slippage / cost-policy review,
- Option D — new strategy-family planning,
- Option E — paper/shadow or Phase 4 (forbidden by current operator policy).

Phase 2y executed Option C and recommended Option (a) — keep §11.6 = 8 bps HIGH unchanged. With Option C closed, the Phase 2x §7.4 precondition for Option D ("becomes the right move if (a) the operator independently confirms the family-ceiling assessment, and (b) Option C confirms §11.6 is correctly calibrated") is satisfied: Option C confirmed §11.6 is correctly calibrated, and the operator's authorization of Phase 3a is the family-ceiling-confirmation precedent. Phase 3a is therefore the executed Option D-style discovery survey.

What Phase 3a is asking:

> Given that the V1 breakout-continuation family has likely reached its useful ceiling under the current framework (Phase 2x §5), and given that Phase 2y has confirmed the framework's cost-policy calibration is preserved, **which non-breakout strategy families are credible candidates for any potential next research arc, and what is the right next docs-only phase (if any)?**

What Phase 3a is **not** asking:

- Not asking whether to deploy R3 or to begin paper/shadow (forbidden by operator policy).
- Not asking whether to begin Phase 4 (runtime / state / persistence) work (forbidden).
- Not asking whether to lift any §1.7.3 project-level lock.
- Not asking whether to revise any Phase 2f threshold (Phase 2y closed this).
- Not asking which non-breakout strategy to **build** next — only which family is the strongest **candidate** for any future operator-authorized spec-writing phase.

The output is a candidate-family enumeration with falsifiable-mechanism hypotheses, classified by near-term suitability under unchanged operator policy, plus a single recommended next docs-only phase (which may legitimately be "remain paused" if no candidate is justified). Phase 3a does **not** authorize any execution. Phase 3a does **not** authorize any spec-writing. Phase 3a produces a memo; the operator decides whether to authorize a downstream phase.

---

## 2. Why a new strategy family is justified now

### 2.1 V1 breakout-family research is paused / completed, not closed

Per Phase 2x §5 family-level diagnosis, the V1 breakout-continuation family has tested all four structural axes under unchanged framework discipline and the carry-forward set is exhausted:

- **Exit axis (R3)** — clean broad-based PROMOTE; baseline-of-record per Phase 2p §C.1; cost-robust at HIGH slippage on both symbols.
- **Setup-validity axis (R1a)** — symbol-asymmetric mixed-PROMOTE; ETH-favorable / BTC-degrading; retained research evidence per Phase 2p §D; BTC-degradation makes it ineligible under §1.7.3 BTCUSDT-primary lock without a lock revision.
- **Bias-validity axis (R1b-narrow)** — formal-strongest §10.3.a-on-both PROMOTE but with R3-anchor near-neutral marginal contribution and 65–70% trade-count drop; retained research evidence per Phase 2s §13.
- **Entry-lifecycle axis (R2)** — MED-slip §10.3 PROMOTE with M1 + M3 mechanism support but **§11.6 cost-sensitivity gate FAILS** at HIGH slippage on both symbols (BTC Δexp_H0 −0.014; ETH Δexp_H0 −0.230); retained research evidence per Phase 2w §16.3; framework verdict FAILED — slippage-fragile.

The pattern across post-R3 candidates is **diminishing absolute-edge return**: each post-R3 axis produced narrower formal PROMOTE (or framework FAIL) while the absolute-edge gap (BTC R-window aggregate expR ≈ −0.24 R per trade under R3) refused to close. Phase 2x §5's four-axis enumeration concludes the family ceiling is "likely reached" under the current framework.

The status is **paused/completed**, not abandoned:

- R3 stays usable as a deployable variant if and when operator policy authorizes paper/shadow / Phase 4.
- R1a / R1b-narrow / R2 stay as research evidence; their findings feed any future hypothesis-development phase.
- A regime-conditional R1a-prime hypothesis (Phase 2o §F.1, Phase 2p §F.1) remains available as un-specified hypothesis territory if the operator independently develops a falsifiable spec.

### 2.2 Why further breakout-family tuning is not the recommended next move

Three reasons, all preserved verbatim from Phase 2x §7.2 / §8.4:

1. **Treadmill risk is now elevated.** Three structural-redesign candidates post-R3 produced PROMOTE-with-caveats or framework-FAIL. Authorizing a fourth breakout-family candidate without a specific operator-developed hypothesis risks producing another mixed result that doesn't move the family-ceiling question forward.
2. **No specific candidate is currently specified.** The Phase 2o §F.1 regime-conditional R1a-prime is undeveloped; the Phase 2i §3.2 R1b-broad with regime-conditional bias was excluded for higher overfitting risk; an R2-prime under operator-policy-revised §11.6 is now blocked because Phase 2y closed Option C with "no threshold revision".
3. **Phase 2j §C.6 / §11.3.5 binding rule applies.** Each new candidate requires explicit per-symbol-regime predicate and singular sub-parameters; specifying one purely from Phase 3a review without an independently-developed hypothesis is exactly the "operator-policy decision under research framing" Phase 2p §H.4 explicitly does not authorize.

### 2.3 Why family-shift discovery is the right next move

Phase 2y closing Option C with "keep §11.6 unchanged" removes the calibration confound that Phase 2x §7.4 flagged: the family-ceiling assessment is no longer partially-confounded by an open cost-policy question. The Phase 2x §6 / §7.4 conditional becomes unconditional: Option D becomes appropriate.

Doing the family-discovery as a **docs-only survey** (this memo), not as a candidate-spec-writing phase, is the disciplined entry path. It mirrors the pre-Phase-2j structure: enumerate candidates → evaluate each against project locks and current evidence → recommend the strongest candidate (or none) → operator decides whether to authorize a downstream spec-writing phase. The survey itself produces no irreversible commitment.

### 2.4 What stays preserved during the discovery

- **R3** as baseline-of-record per Phase 2p §C.1.
- **H0** as framework anchor per Phase 2i §1.7.3.
- **R1a / R1b-narrow / R2** as retained research evidence per Phase 2p §D / Phase 2s §13 / Phase 2w §16.3.
- **§1.7.3 project-level locks** verbatim: BTCUSDT primary live, ETHUSDT research/comparison only, one-symbol-only live, one-position max, 0.25% risk per trade, 2× leverage cap, mark-price stops, v002 datasets.
- **No threshold change.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds preserved per Phase 2f §11.3.5 / Phase 2y closeout.
- **No paper/shadow planning, no Phase 4, no live-readiness, no deployment, no production-key work, no exchange-write capability, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits.**

---

## 3. Candidate family menu

Eight candidate families enumerated per the Phase 3a operator brief. Each is evaluated against twelve attributes (§4) before classification (§5) and ranking (§6).

| # | Family name | One-line mechanism hypothesis |
|---|-------------|--------------------------------|
| F1 | Mean reversion after overextension | After short-horizon directional overextension, prices revert toward a recent mean; trade the reversion. |
| F2 | Volatility contraction / expansion redesigned from first principles | After a low-volatility compression regime ends with a volatility expansion shock, position with the directional bias of the shock — but specified independently of breakout-family setup logic. |
| F3 | Trend pullback / continuation | In an established trend, after a counter-trend retracement, position with the trend; entry on retracement-completion confirmation, not on breakout. |
| F4 | Range-bound regime strategy | When the market is in a confirmed range, fade extremes (sell tops, buy bottoms within range); exit on range-edge violation or mean-revert target. |
| F5 | BTC / ETH relative strength / spread / rotation | Trade the relative-strength relationship between BTC and ETH; position long the leader and (operationally) flat the laggard, or trade the spread directly. |
| F6 | Funding-aware directional or carry-aware | Use Binance USDⓈ-M funding-rate extremes as either a contrarian directional signal or a cost-discount filter for an existing directional thesis. |
| F7 | Regime-first strategy framework | Build a regime classifier (low-vol / med-vol / high-vol; trending / range-bound; risk-on / risk-off) and dispatch to family-specific sub-strategies; family-of-families rather than a single strategy. |
| F8 | ML-assisted forecasting layer (future-only) | Use a learned model to forecast directional bias / volatility / regime as a strategy input; rules-based execution layer downstream. |

---

## 4. Per-family attribute evaluation

Each family is evaluated against twelve attributes per the Phase 3a operator brief: (a) core market hypothesis; (b) what failure mode of V1 breakout it avoids; (c) required data inputs; (d) v002 dataset sufficiency; (e) v003 dataset need; (f) expected trade frequency; (g) expected cost sensitivity; (h) expected BTC/ETH behavior; (i) overfitting risk; (j) implementation complexity; (k) validation difficulty; (l) safety / live-readiness implications.

### 4.1 F1 — Mean reversion after overextension

| Attribute | Detail |
|-----------|--------|
| **(a) Core market hypothesis** | After a short-horizon directional overextension (e.g., N consecutive 15m bars of one-sided drift, or a single-bar move > k × ATR), reversion to a recent rolling mean is more likely than continuation — particularly in chop / range-bound regimes where breakout-family is structurally hostile. |
| **(b) Breakout failure mode avoided** | **Chop with repeated false breaks** (V1 spec §"Failure Modes" #1). V1's main expected loss pattern is exactly the regime mean-reversion targets. Phase 2g/2h/2l/2m/2s/2w showed F4 2024H1 was the worst fold for both H0 and R3 on both symbols — a regime-incompatibility R3 reduced but did not solve. Mean-reversion is structurally complementary. |
| **(c) Required data inputs** | 15m + 1h OHLCV (BTC/ETH); volatility features (ATR, realized vol); short-window directional-strength features (consecutive-bar count, displacement-vs-ATR ratio); rolling-mean references (EMA/SMA over short windows). All derivable from existing v002 datasets. |
| **(d) v002 dataset sufficiency** | **Sufficient.** No new raw data required. New derived features needed (overextension predicates, rolling-mean references). Per Phase 2e v002 framing + dataset-versioning policy, derived features create a new versioned feature dataset (e.g., `mean_reversion_features_btcusdt_15m__v001`) without a v003 raw-data bump. |
| **(e) v003 dataset need** | **Not required** for initial spec-writing or first execution. Funding-rate enrichment (already in v002) is enough for cost realism. |
| **(f) Expected trade frequency** | **Higher than V1 breakout.** Mean-reversion candidates fire whenever overextension predicate hits — typically 2–4× the V1 breakout-trade frequency at comparable thresholds. R-window expected sample size: ≥80–120 trades per symbol (vs. 33 for H0/R3). Improves §10.3 statistical strength materially. |
| **(g) Expected cost sensitivity** | **Moderate-to-high.** Mean-reversion typically operates with tight stops (often inside the overextension range) and tight targets (mean-reversion target). Per-trade R-multiples are smaller than breakout, so per-trade cost is a larger fraction. Round-trip slippage at 16 bps HIGH could materially erode edge. **Direct evidence relevance:** R2's §11.6 failure was the slippage-fragility precedent for entry-axis improvements; mean-reversion shares the small-R-distance geometry. |
| **(h) Expected BTC/ETH behavior** | **Likely BTC-friendly.** ETH's higher noise / wider spread profile (Phase 2x §4.6 / Phase 2y §5.1.8) is more hostile to mean-reversion's tight-stop geometry. R1a's ETH-favorable / BTC-degrading asymmetry inverts here: mean-reversion plausibly favors BTC structurally. Helps §1.7.3 BTCUSDT-primary alignment. |
| **(i) Overfitting risk** | **Moderate.** Multiple thresholds (overextension definition, stop-distance, target-distance, cooldown). Mitigatable via Phase 2j §11.3.5-style singular-sub-parameter commitment + Phase 2f §11.2 fold-consistency discipline. Larger trade samples reduce small-window fragility relative to V1 breakout. |
| **(j) Implementation complexity** | **Medium.** Comparable to R1a's spec-writing cost (overextension predicate is structurally similar to volatility-percentile predicate). New strategy module; new feature dataset; new exit-machinery (mean-reversion-specific take-profit and stop-out). Estimate: 1500–2500 lines including tests, in line with Phase 2t R2 budget. |
| **(k) Validation difficulty** | **Moderate.** Standard Phase 2j-style spec → Phase 2k-style execution → Phase 2l-style comparison fits cleanly. Cross-symbol §11.4 evaluation applies. Cost-sensitivity sweep (LOW / MED / HIGH) and §11.6 evaluation apply. Larger trade count makes per-fold §11.2 evaluation more informative. |
| **(l) Safety / live-readiness implications** | **Compatible with v1 locks.** One-position max preserved (mean-reversion is one-position). No reversal while positioned (each mean-reversion trade is independent; same direction allowed only on new overextension). Tight stops are acceptable — the v1 stop-distance filter `[0.60, 1.80] × ATR(20)` already constrains tightness. Mark-price stops apply unchanged. **No §1.7.3 lock change required** for BTC-primary live deployment. |

### 4.2 F2 — Volatility contraction / expansion redesigned from first principles

| Attribute | Detail |
|-----------|--------|
| **(a) Core market hypothesis** | Volatility regime transitions (compression-end → expansion-onset) are predictable signals; trade the expansion direction with rule-set independent of V1 breakout's range-and-bar-close-confirmation logic. Could be Bollinger-band squeeze release, ATR-percentile transition, or volatility-of-volatility shock. |
| **(b) Breakout failure mode avoided** | **Breakout exhaustion** (V1 spec failure mode #3): some breakouts mark the END of a move, not the beginning. A first-principles volatility-regime redesign could position based on regime-transition direction rather than bar-close-confirmation, sidestepping the exhaustion pattern. |
| **(c) Required data inputs** | 15m + 1h OHLCV; ATR(N) for multiple N; Bollinger / Keltner-style envelopes; volatility-percentile features. All derivable from v002. |
| **(d) v002 dataset sufficiency** | **Sufficient** with new derived features. |
| **(e) v003 dataset need** | Not required initially. |
| **(f) Expected trade frequency** | **Comparable to V1 breakout** (volatility-regime transitions are structurally similar in frequency to compression-then-breakout). 30–50 trades per symbol per R-window. |
| **(g) Expected cost sensitivity** | **Moderate.** Could be more cost-robust than F1 if entries are placed at expansion-onset (similar to R3's structural exit-machinery improvement) rather than at compressed pullback levels. |
| **(h) Expected BTC/ETH behavior** | **Uncertain.** Volatility-regime transitions are universal but their predictability differs by symbol. Possibly inherits some of breakout-family's BTC/ETH asymmetry. |
| **(i) Overfitting risk** | **Higher than F1.** Many parameters (compression-window length, expansion threshold, regime-classifier choice, multiple ATR horizons). Phase 2i §3.2 logic that excluded R1b-broad with regime-conditional bias for high overfitting risk applies symmetrically here. |
| **(j) Implementation complexity** | **High.** Multi-feature regime classifier + execution rules. Estimate: 2500–3500 lines including tests. Higher than F1. |
| **(k) Validation difficulty** | **High.** Multiple parameters increase the §11.3.5 single-sub-parameter-commitment burden; risk of accidentally specifying a candidate too close to the V1 breakout family (since both sit on the volatility axis). Family-shift cleanliness is questionable. |
| **(l) Safety / live-readiness implications** | **Compatible with v1 locks** if specified carefully. But: family-shift cleanliness is the concern — a volatility-redesign that ends up being "V1 breakout with different setup-window logic" is not really a family shift; it's another setup-axis variant in the breakout family. Phase 2i §1.7 binding-test (rule-shape change vs parameter-tuning under another label) would require careful application. |

### 4.3 F3 — Trend pullback / continuation

| Attribute | Detail |
|-----------|--------|
| **(a) Core market hypothesis** | In an established trend (defined by a higher-timeframe filter similar to V1's 1h EMA structure), after a counter-trend retracement of definite depth (e.g., touch of a fast EMA, or N% retracement from recent extreme), trend resumption is more likely than reversal. Position with the trend on retracement-completion. |
| **(b) Breakout failure mode avoided** | **Lagging bias filter during reversals** (V1 spec failure mode #2) — partial avoidance. Trend-pullback still uses a higher-timeframe trend filter, so it shares some of the same lagging-filter-during-reversal exposure. But it avoids breakout-exhaustion (failure mode #3) because entry is on retracement-completion, not on breakout. |
| **(c) Required data inputs** | 15m + 1h OHLCV; EMA/SMA stack; retracement / Fibonacci-style measurements; ATR for sizing. All derivable from v002. |
| **(d) v002 dataset sufficiency** | **Sufficient** with new derived features (retracement detection, fast/slow EMA stack). |
| **(e) v003 dataset need** | Not required initially. |
| **(f) Expected trade frequency** | **Comparable to or lower than V1 breakout** (fewer pullbacks than breakouts in a given trend). 20–35 trades per symbol per R-window. **Sample-size concern** — same magnitude as V1 breakout, which already strained per-fold §11.2 evaluation. |
| **(g) Expected cost sensitivity** | **High.** Pullback entries place the entry close to a structural support/resistance, producing tight stops by geometry (same as R2's mechanism). **Direct evidence relevance:** R2's §11.6 failure is the precedent — pullback-entry geometry produced cost-fragility. Trend-pullback inherits this risk. |
| **(h) Expected BTC/ETH behavior** | **Possibly BTC-friendly under R3's exit machinery** (the M1 +0.123 R BTC intersection-trade gain in Phase 2w R2 was direction-symmetric; trend-pullback in established trend shares the geometry). But the §11.6 failure is also a direct precedent. |
| **(i) Overfitting risk** | **Moderate.** Multiple parameters (retracement depth, trend-filter thresholds, confirmation rule). Lower than F2 because the trend filter can mirror V1's documented EMA(50)/EMA(200) structure (familiar baseline). |
| **(j) Implementation complexity** | **Medium-High.** Retracement-detection logic is non-trivial; trend-filter logic re-uses V1 patterns. Estimate: 1800–2800 lines including tests. |
| **(k) Validation difficulty** | **Moderate.** Standard Phase 2j-style cycle. The §11.6 cost-sensitivity gate is the binding concern given inherited geometry; expect cost-fragility and need for explicit slippage-sweep. |
| **(l) Safety / live-readiness implications** | **Compatible with v1 locks.** No reversal while positioned, one-position max preserved. The R2 entry-lifecycle topology evidence (M1 +0.123 R / §11.6 FAIL) is directly informative — would need cost-realism evidence-collection (a future Phase 2z-equivalent) before realistic deployment expectations. |

### 4.4 F4 — Range-bound regime strategy

| Attribute | Detail |
|-----------|--------|
| **(a) Core market hypothesis** | When the market is in a confirmed range (defined by N consecutive bars within a bounded width relative to ATR), fade range extremes — sell tops, buy bottoms — with target at midpoint or opposite extreme, exit on range-edge violation. |
| **(b) Breakout failure mode avoided** | **Chop with repeated false breaks** (failure mode #1) — strongest avoidance. Range-trading is structurally inverse to breakout-trading: where breakout fails (chop / range), range-trading thrives. |
| **(c) Required data inputs** | 15m + 1h OHLCV; range-detection features (rolling high/low, range-width-vs-ATR ratio, range-violation detection). All derivable from v002. |
| **(d) v002 dataset sufficiency** | **Sufficient.** |
| **(e) v003 dataset need** | Not required initially. |
| **(f) Expected trade frequency** | **Variable** — depends entirely on regime mix. Could be 0–2 trades per fold during trending periods (range-trading inactive), 5–10 trades per fold during ranging periods. Aggregate could be 25–50 trades per symbol per R-window. |
| **(g) Expected cost sensitivity** | **Very high.** Range-trading typically uses tight stops just outside range edges and targets at range midpoints — small absolute price moves. Per-trade R-multiples are small. Per-trade cost is a substantial fraction of edge. **Among all candidates, F4 has the highest expected cost-sensitivity.** |
| **(h) Expected BTC/ETH behavior** | **Potentially symmetric.** Both BTC and ETH exhibit range-bound regimes; the regime-mix differs more than the within-regime profitability. ETH's wider spreads / shallower depth (Phase 2y §5.1.8) makes ETH execution less attractive — could disadvantage ETH side. |
| **(i) Overfitting risk** | **Moderate-to-high.** Range-detection itself is sensitive to lookback window, width threshold, and regime-end detection. Single-sub-parameter commitment per Phase 2j §C.6 / §11.3.5 helps, but the parameter space is larger than R1a. |
| **(j) Implementation complexity** | **High.** Range-detection logic + entry-at-extreme + range-violation exit + range-end / regime-shift detection. Estimate: 2500–3500 lines including tests. |
| **(k) Validation difficulty** | **High.** Cost-sensitivity sweep (LOW / MED / HIGH) and §11.6 gate are the binding constraints. Per-fold sample sizes will be very uneven (zero trades in trending folds, larger samples in ranging folds), complicating §11.2 fold-consistency evaluation. |
| **(l) Safety / live-readiness implications** | **Compatible with v1 locks** mechanically. The regime-shift / range-violation exit must trigger cleanly to avoid a position-stuck-in-failed-range scenario. Mark-price stops apply unchanged. The "no reversal while positioned" rule is preserved per-trade (range-trading is one direction at a time). |

### 4.5 F5 — BTC / ETH relative strength / spread / rotation

| Attribute | Detail |
|-----------|--------|
| **(a) Core market hypothesis** | BTC/ETH relative strength is mean-reverting or trending at predictable horizons. Trade the relationship: long the leader and short the laggard (spread trade), or rotate single-leg long-only between the two based on relative-strength signal. |
| **(b) Breakout failure mode avoided** | **Volatility shock conditions** (failure mode #4) — partial avoidance. Spread-trades are more market-neutral than directional trades; idiosyncratic volatility shocks affect both legs and partially cancel. |
| **(c) Required data inputs** | 15m + 1h OHLCV for both BTC and ETH; relative-strength index (price ratio, return-correlation); spread-construction primitives. All derivable from v002. |
| **(d) v002 dataset sufficiency** | **Sufficient** for research. ETH-specific microstructure data (depth, spread distribution) is not in v002 but is needed for live-realism assessment per Phase 2y §5.1.2. |
| **(e) v003 dataset need** | **Possibly required** for execution-realism — a v003 with ETH spread/depth features would be needed before live deployment, but not for initial research. |
| **(f) Expected trade frequency** | **Lower** — relative-strength trades have longer hold periods and fewer setups. 10–20 trades per R-window combined. **Sample-size concern is acute.** |
| **(g) Expected cost sensitivity** | **High** — two-leg trades double the cost-stack (entry + exit on each leg = 4 fee + 4 slippage events vs 2 + 2 for single-leg). ETH leg's wider spread (per Phase 2y §5.1.8) compounds. |
| **(h) Expected BTC/ETH behavior** | **Both symbols required by construction.** This is the only family on the menu that requires BTC AND ETH simultaneously. |
| **(i) Overfitting risk** | **High.** Multi-asset families have larger parameter spaces (signal definition, hedge ratio, leg-correlation requirement, cooldowns). |
| **(j) Implementation complexity** | **High.** Two-leg execution, dual-symbol order management, spread reconciliation logic. Significant runtime infrastructure beyond v1's one-position-one-symbol architecture. |
| **(k) Validation difficulty** | **High.** Sample-size, parameter-space, and execution-realism all compound. |
| **(l) Safety / live-readiness implications** | **BLOCKED by §1.7.3 BTCUSDT-primary lock and one-symbol-only live scope.** F5 cannot be deployed live without lifting two project-level locks (BTCUSDT-primary AND one-symbol-only). The locks were established in Phase 2i and are explicitly preserved through Phase 2y. F5 is research-only under unchanged operator policy. Phase 4 (runtime / state / persistence) would also require multi-symbol-aware redesign, which is not the current scope (Phase 2x §3.5 / Phase 2y §8.4). |

### 4.6 F6 — Funding-aware directional or carry-aware

| Attribute | Detail |
|-----------|--------|
| **(a) Core market hypothesis** | Two sub-hypotheses, each falsifiable independently: (a) **funding-rate extremes are contrarian directional signals** — when longs pay shorts heavily (positive extreme funding), short positions have a positive carry tailwind that compensates for adverse selection; (b) **funding-aware filtering of an existing directional thesis** — only take long signals when funding is neutral-or-negative; only take short signals when funding is neutral-or-positive — using funding as a cost-discount filter rather than a primary signal. |
| **(b) Breakout failure mode avoided** | **Volatility shock conditions** (failure mode #4) — moderate avoidance. Funding extremes often precede volatility-regime changes; using funding as a filter or signal could position with or away from regime shifts. |
| **(c) Required data inputs** | 15m + 1h OHLCV; **funding-rate history (already in v002)**; mark-price (for carry-cost calculations). All in v002. |
| **(d) v002 dataset sufficiency** | **Sufficient.** Uniquely among the candidates, F6 leverages a v002 dataset feature (funding rates) that the V1 breakout family did not exploit as a primary signal. |
| **(e) v003 dataset need** | Not required. |
| **(f) Expected trade frequency** | **Lower-to-moderate.** Funding extremes are episodic — Binance funds every 8 hours; meaningful extremes occur perhaps 5–15× per month in volatile regimes, fewer in quiet regimes. Variant (a) has lower frequency than variant (b). |
| **(g) Expected cost sensitivity** | **Lower than F1, F3, F4.** Funding is a known carry component already in the cost stack; if the strategy actively harvests funding, the carry cost becomes a carry benefit. Sub-variant (b) (funding as filter) is cost-neutral relative to base directional thesis. |
| **(h) Expected BTC/ETH behavior** | **Could be BTC-favorable.** BTC funding is more liquid / larger volume / more reliable than ETH funding. ETH funding rates can be more erratic. §1.7.3 BTCUSDT-primary alignment is natural. |
| **(i) Overfitting risk** | **Moderate.** Funding-extreme threshold, hold-period, position-direction logic. Smaller parameter space than F2 / F4 / F5. |
| **(j) Implementation complexity** | **Medium.** New funding-feature dataset; signal logic; standard execution layer. Estimate: 1500–2500 lines including tests. Comparable to F1. |
| **(k) Validation difficulty** | **Moderate.** Sample-size is the concern (funding extremes are episodic; per-fold counts could be fragile). Cost-sensitivity and §11.6 are evaluable cleanly. |
| **(l) Safety / live-readiness implications** | **Compatible with v1 locks.** Single-symbol single-position. Funding awareness is information-only at signal time — does not alter execution semantics. Mark-price stops apply unchanged. **Note:** funding as a signal also has plausible interaction with R3's exit machinery (time-stop near funding-event times could be considered) — but Phase 3a does not specify; it identifies. |

### 4.7 F7 — Regime-first strategy framework

| Attribute | Detail |
|-----------|--------|
| **(a) Core market hypothesis** | A meta-strategy that classifies the current regime (trending / range-bound / shock; low-vol / med-vol / high-vol; risk-on / risk-off) and dispatches to family-specific sub-strategies. The hypothesis is that the right strategy depends on regime, and a regime-aware framework outperforms any single regime-blind strategy. |
| **(b) Breakout failure mode avoided** | **All four V1 breakout failure modes potentially**: chop is handled by F1 / F4 sub-strategies; reversal-lag is handled by switching off trend-filter sub-strategies; exhaustion is handled by mean-reversion sub-strategies; volatility shocks are handled by regime-shift detection itself. |
| **(c) Required data inputs** | All inputs from F1–F6 combined. |
| **(d) v002 dataset sufficiency** | **Sufficient.** |
| **(e) v003 dataset need** | Not required. |
| **(f) Expected trade frequency** | **Moderate** (aggregate across sub-strategies). |
| **(g) Expected cost sensitivity** | **High** — inherits the worst-case cost-sensitivity of the constituent sub-strategies. Regime-shift detection latency adds a systematic cost (entries/exits at regime boundaries are typically less favorable). |
| **(h) Expected BTC/ETH behavior** | Inherits the BTC/ETH asymmetry profile of each sub-strategy. |
| **(i) Overfitting risk** | **Very high.** Regime-classifier hyperparameters + sub-strategy hyperparameters compound multiplicatively. Phase 2i §3.2's exclusion logic for R1b-broad applies here in extreme form. |
| **(j) Implementation complexity** | **Very high.** Regime-classifier module + multiple sub-strategy modules + dispatch logic + transition handling + regime-confidence reporting. Estimate: 8000+ lines including tests. Significantly larger than any single Phase 2 candidate. |
| **(k) Validation difficulty** | **Very high.** Phase 2f §11.2 fold-consistency and §11.6 cost-sensitivity become harder to reason about when the strategy itself shifts behavior across folds. The §10.3 framework's threshold mechanics were calibrated on single-strategy candidates. |
| **(l) Safety / live-readiness implications** | **Compatible with v1 locks** mechanically (one-position-at-a-time enforced at the dispatcher level). But: the runtime complexity introduces a substantial Phase 4 burden — regime classifier + dispatch logic + sub-strategy state machines × N. **Premature relative to current operator policy** (Phase 2y reaffirmed Phase 4 is not authorized). F7 is a long-horizon family-of-families ambition, not a near-term Phase 3b candidate. |

### 4.8 F8 — ML-assisted forecasting layer (future-only)

| Attribute | Detail |
|-----------|--------|
| **(a) Core market hypothesis** | Use a learned model (logistic regression, gradient-boosted trees, sequence model) to forecast directional bias / volatility / regime at the strategy decision time. Strategy execution remains rules-based; the ML output is one signal input among many. |
| **(b) Breakout failure mode avoided** | Variable — depends on what the model is trained to predict. |
| **(c) Required data inputs** | All v002 features + engineered feature set + train/validation/test splits per `v1-breakout-validation-checklist.md` Gate 4. |
| **(d) v002 dataset sufficiency** | **Sufficient for research training data.** New feature-engineering datasets needed. |
| **(e) v003 dataset need** | Not required for research; could be required for operational feature-pipeline reproducibility. |
| **(f) Expected trade frequency** | **Variable** — depends on the model's confidence threshold and the underlying strategy. |
| **(g) Expected cost sensitivity** | Inherits underlying strategy's cost profile. |
| **(h) Expected BTC/ETH behavior** | Highly model-dependent. |
| **(i) Overfitting risk** | **Maximum.** ML forecasting on financial time series is the textbook example of overfitting risk. Bailey et al. (cited in `v1-breakout-validation-checklist.md`) "The Probability of Backtest Overfitting" applies most directly here. |
| **(j) Implementation complexity** | **Very high.** Feature pipeline, training pipeline, model serving, model versioning, model rollback, drift monitoring — significant infrastructure beyond a single rules-based strategy. |
| **(k) Validation difficulty** | **Highest.** ML adds hyperparameter selection, train/test split design, lookahead avoidance in feature engineering, and drift / non-stationarity handling — orthogonal to and on top of the existing Phase 2f framework. |
| **(l) Safety / live-readiness implications** | **BLOCKED by `.claude/rules/prometheus-core.md` "v1 not self-learning" lock and the Prometheus locked decision per `current-project-state.md` "initially rules-based, not self-learning in v1, designed to support future AI-assisted research or automation, but not dependent on a self-learning live AI component for v1".** F8 is explicitly out of v1 scope per project-level documentation. F8 is **future-only / not immediate** per the Phase 3a operator brief. |

---

## 5. Family classification

Each family classified per the Phase 3a operator brief into one of:

- **Near-term candidate** — could be the basis for a Phase 3b spec-writing phase under unchanged operator policy.
- **Research-only later** — credible family but blocked by current locks; could be revisited if locks change.
- **Blocked by data requirements** — needs new raw-data ingestion (v003-equivalent) before research can begin.
- **Blocked by complexity** — implementation / validation cost too high for the next phase boundary.
- **Not recommended** — fundamentally misaligned with v1 scope or current evidence.

| # | Family | Classification | Primary blocker / driver |
|---|--------|----------------|--------------------------|
| F1 | Mean reversion after overextension | **Near-term candidate** | Strongest §1.7.3 alignment + v002 sufficient + structurally inverts main V1 breakout failure mode. Cost-sensitivity is the watchpoint. |
| F2 | Volatility contraction / expansion redesigned | **Research-only later** | Family-shift cleanliness uncertain; risk of accidentally specifying another setup-axis variant in the breakout family rather than a true family shift. Phase 2i §1.7 binding-test would be hard to satisfy. |
| F3 | Trend pullback / continuation | **Near-term candidate (with caveats)** | v002 sufficient; §1.7.3 compatible; but inherits R2's §11.6 cost-fragility precedent (M1 +0.123 R BTC gain consumed at HIGH slippage). Would be a useful candidate **only after** the §5.1.x-style external slippage evidence (per Phase 2y §5.3) is gathered or the operator accepts the cost-fragility risk explicitly. |
| F4 | Range-bound regime strategy | **Research-only later** | High cost-sensitivity (smallest expected per-trade R-multiples among candidates) is a near-deal-breaker under unchanged §11.6 = 8 bps HIGH. Could become near-term if Phase 2y's §5.3 external-evidence path is ever pursued and HIGH is materially lower. |
| F5 | BTC / ETH relative strength / spread | **Research-only later (lock-blocked for live)** | §1.7.3 BTCUSDT-primary AND one-symbol-only live scope must both be lifted to deploy. Research-only feasibility is real (v002 sufficient for backtest), but the live-readiness path is far. |
| F6 | Funding-aware directional or carry-aware | **Near-term candidate** | v002 sufficient (uniquely leverages v002's funding-rate dataset that V1 breakout did not exploit as primary signal); §1.7.3 compatible; lower cost-sensitivity than F1 / F3 / F4. Sample-size concern (funding extremes are episodic) is the main watchpoint. |
| F7 | Regime-first strategy framework | **Blocked by complexity** | Implementation budget (~8000+ lines) and Phase 4 dependence (regime-aware runtime infrastructure) make F7 premature relative to current operator policy. F7 is a long-horizon meta-framework, not a near-term Phase 3b candidate. |
| F8 | ML-assisted forecasting layer | **Not recommended (future-only per project policy)** | Explicitly out of v1 scope per project-level documentation (`current-project-state.md` "not self-learning in v1"; `.claude/rules/prometheus-core.md`). Future-only. |

### 5.1 Near-term candidate ranking

Three families classified as near-term candidates (F1, F3, F6). Ranked by net suitability:

**Rank 1 — F1 (Mean reversion after overextension).** Strongest case:

- Structurally inverts the V1 breakout family's #1 failure mode (chop with false breaks). Phase 2g/2h/2l/2m/2s/2w consistently showed F4 2024H1 was the worst fold for both H0 and R3 on both symbols; mean-reversion is regime-complementary.
- v002 sufficient; no v003 needed.
- §1.7.3 BTCUSDT-primary aligned (mean-reversion plausibly favors BTC's tighter-spread profile).
- Higher trade-count expectation (≥80–120 per R-window per symbol) materially improves §10.3 / §11.2 / §11.6 statistical strength.
- Implementation budget moderate (~1500–2500 lines).
- Established crypto-microstructure research basis (Wen et al. 2022 "Intraday return predictability in the cryptocurrency markets" cited in `v1-breakout-strategy-spec.md`).
- Cost-sensitivity is the watchpoint — but Phase 2y closeout means we evaluate against unchanged §11.6 = 8 bps HIGH and see.

**Rank 2 — F6 (Funding-aware).** Distinct positives:

- Uniquely leverages a v002 dataset feature (funding rates) the V1 breakout family did not exploit as primary signal.
- Lowest cost-sensitivity among the near-term candidates.
- Implementation budget moderate (~1500–2500 lines).
- Two falsifiable sub-hypotheses (contrarian directional vs. cost-discount filter) provide a built-in A/B comparison.
- Sample-size concern is the main watchpoint — funding extremes are episodic; per-R-window expected sample counts (5–15 per month × 36 months) could yield 25–60 trades per symbol, comparable to V1 breakout's tight per-fold behavior.

**Rank 3 — F3 (Trend pullback / continuation).** Useful but cautious:

- Direct relevance to existing R2 evidence (M1 + M3 mechanism findings inform spec).
- §1.7.3 compatible; v002 sufficient.
- **But:** inherits R2's §11.6 cost-fragility geometry. Without §5.3-style external slippage evidence (Phase 2y closed Option C with no threshold change), F3 is at high risk of producing another §11.6-failed mechanism-partially-supported result — the pattern Phase 2x §5.2 identified as the diminishing-returns curve.

---

## 6. Recommended next docs-only phase

This recommendation is **provisional and evidence-based, not definitive**. The operator decides.

### 6.1 Primary recommendation

**Authorize Phase 3b — F1 (mean-reversion-after-overextension) family spec-writing memo.**

Phase 3b would be a Phase 2j-style docs-only spec-writing phase that produces:

1. A market-hypothesis statement with falsifiable mechanism predictions (M1 / M2 / M3 equivalents).
2. Singular committed sub-parameters per Phase 2j §C.6 / §11.3.5 discipline (overextension predicate definition; stop-distance; target-distance; cooldown).
3. Explicit fold-consistency expectations per Phase 2f §11.2.
4. Explicit cost-sensitivity expectations per Phase 2f §11.6 (acknowledging cost-sensitivity is the family's structural risk).
5. Explicit BTC/ETH behavior expectations and §11.4 compliance plan.
6. Implementation surface estimate per Phase 2t §J.6 framing.
7. A pre-declared GO / NO-GO Gate 1 plan for an eventual Phase 3c execution phase.

Phase 3b is **docs-only**; produces a memo; does not authorize execution. The execution phase (Phase 3c, if and when authorized) would require its own operator-policy gate.

### 6.2 Why F1 over F6 over F3

The §6.1 ranking section gave the technical case. The recommendation summary:

- **F1 vs F6:** F1's structural inversion of the V1 breakout family's #1 failure mode is a cleaner family-shift than F6's data-feature exploitation. F6 is a strong second; if the operator prefers a candidate with lower cost-sensitivity exposure, F6 becomes primary. The two are nearly co-equal.
- **F1 vs F3:** F3 inherits R2's §11.6 cost-fragility risk. Phase 2y closed Option C without threshold change, so F3's cost-fragility risk is unchanged from R2's. Phase 2x §5.2 family-ceiling diagnosis applies: another §11.6-fragile candidate would extend the diminishing-returns pattern rather than break it.

### 6.3 Why not "remain paused" or "data-requirements phase"

- **Remain paused** — could be the operator's choice. Phase 3a does not authorize Phase 3b; Phase 3b only happens if the operator authorizes it. Phase 2x's Option A (remain paused) remains a legitimate post-Phase-3a position. The Phase 3a recommendation reflects "if any active path is desired, here is the strongest candidate"; "stay paused" is a valid alternative the operator selects independently.
- **Data-requirements phase** — not recommended. F1 / F6 / F3 all use v002 datasets directly; no v003 is needed for spec-writing. A separate data-requirements phase would be redundant. (F5 might warrant a v003 ETH-microstructure dataset before live deployment, but F5 is not a near-term candidate.)

### 6.4 What Phase 3b would NOT do

- Phase 3b would NOT recommend implementation. Phase 3b is a spec-writing memo only. Implementation requires a separately-authorized Phase 3c execution phase.
- Phase 3b would NOT change any threshold. Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 apply unchanged.
- Phase 3b would NOT change any §1.7.3 project-level lock.
- Phase 3b would NOT propose paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write work.
- Phase 3b would NOT alter R3's baseline-of-record status, H0's framework-anchor status, or R1a / R1b-narrow / R2's retained-research-evidence status.
- Phase 3b would NOT propose any MCP / Graphify / `.mcp.json` / credentials / `data/` commits.

---

## 7. Explicit project-state preservation statement

Phase 3a explicitly preserves the following:

- **R3 remains baseline-of-record** per Phase 2p §C.1. Locked sub-parameters: `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`. Same-bar priority STOP > TAKE_PROFIT > TIME_STOP. Phase 2j §D.6 invariants preserved.
- **H0 remains the formal framework anchor** per Phase 2i §1.7.3.
- **R1a remains research evidence only** per Phase 2p §D. Retained-for-future-hypothesis-planning. Not deployable; not the current default.
- **R1b-narrow remains research evidence only** per Phase 2s §13.
- **R2 remains research evidence only** per Phase 2w §16.3. Framework verdict FAILED — §11.6 cost-sensitivity blocks. Mechanism evidence (M1 + M3 PASS; M2 FAIL) preserved as descriptive.
- **No threshold change.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / **§11.6 = 8 bps HIGH** preserved verbatim per Phase 2f §11.3.5 / Phase 2y closeout. `src/prometheus/research/backtest/config.py:55-59` unchanged.
- **No project-level lock change.** §1.7.3 BTCUSDT primary, ETHUSDT research/comparison only, one-symbol-only live, one-position max, 0.25% risk per trade, 2× leverage cap, mark-price stops, v002 datasets — all preserved verbatim.
- **No paper/shadow planning is authorized.** Phase 2p §F.2 / post-Phase-2w consolidation / Phase 2x §6 / Phase 2y §8.4 deferrals stand.
- **No Phase 4 (runtime / state / persistence) is authorized.** Phase 2p §F.3 / post-Phase-2w / Phase 2x §6 / Phase 2y §8.4 deferrals stand.
- **No live-readiness work is authorized.** No deployment, no exchange-write capability, no production keys, no MCP / Graphify / `.mcp.json` activation, no credentials.
- **No `data/` commits.**
- **No code change.** No file in `src/`, `tests/`, or `scripts/` is touched by Phase 3a.
- **No spec change.** `v1-breakout-strategy-spec.md`, `v1-breakout-validation-checklist.md`, `cost-modeling.md`, `backtesting-principles.md`, `phase-gates.md`, `technical-debt-register.md`, `data-requirements.md`, `dataset-versioning.md` all preserved.

---

## 8. What would change this recommendation

- **Operator selects F6 (funding-aware) over F1.** Switch primary → F6. Phase 3a treats F1 and F6 as nearly co-equal; F6 has lower cost-sensitivity exposure but smaller expected trade samples.
- **Operator chooses to remain paused.** Phase 2x Option A remains a legitimate post-Phase-3a outcome. Phase 3a's recommendation is conditional on "if any active path is desired"; "stay paused" is the valid alternative.
- **Operator independently authorizes Phase 2z external-evidence-gathering** (per Phase 2y §8.5) before Phase 3b. F3's cost-fragility risk could be re-evaluated under any future revised §11.6, potentially elevating F3 from rank-3 to rank-1 or rank-2.
- **Operator authorizes lifting §1.7.3 single-symbol-only or BTCUSDT-primary lock** (a meaningful policy decision outside Phase 3a scope). F5 (BTC/ETH relative strength) could become a near-term candidate.
- **Operator independently develops a falsifiable regime-conditional R1a-prime hypothesis** (per Phase 2o §F.1 / Phase 2p §F.1). Phase 2x Option B (one more breakout-family research phase) could become primary, deferring family-shift.
- **Discovery of an implementation issue or documentation inconsistency in prior phase records** that requires a docs-only correction phase before any further strategy work.

---

## 9. GO / NO-GO recommendation for the next docs-only phase

**GO (provisional)** for **Phase 3b — F1 (mean-reversion-after-overextension) family spec-writing memo** as the recommended next docs-only phase. Rank 1 of three near-term candidates. Phase 3b would be Phase 2j-style: docs-only; falsifiable mechanism predictions; singular sub-parameters; pre-declared §10.3 / §10.4 / §11.3 / §11.4 / §11.6 evaluation plan; estimated implementation surface for any eventual Phase 3c execution phase. **Phase 3b does not authorize execution.** A separately-authorized Phase 3c would be required for implementation, and a still-later phase for paper/shadow / Phase 4 / live-readiness work — none of which are authorized now or by Phase 3a.

**GO (provisional, alternative)** for **Phase 3b-alt — F6 (funding-aware) family spec-writing memo** as the second-strongest near-term candidate, recommended if the operator prefers lower cost-sensitivity exposure over higher expected trade-count.

**NO-GO** for any **Phase 3c-equivalent execution phase** of any family. Phase 3a does not authorize execution; the spec-writing must precede any execution.

**NO-GO** for **F2 / F4 / F5 / F7** as near-term Phase 3b candidates (research-only-later or blocked-by-complexity per §5).

**NO-GO** for **F8 (ML-assisted forecasting)** under any timeline — explicitly out of v1 scope per project-level documentation. Future research only.

**NO-GO** for **paper/shadow planning, Phase 4 (runtime / state / persistence), live-readiness, deployment, exchange-write capability, production keys, MCP / Graphify activation, credentials, and `data/` commits.** All Phase 2x / Phase 2y / post-Phase-2w restrictions stand.

**NO-GO** for any **threshold change, §1.7.3 project-level lock change, or operator-policy revision.** Phase 3a is family-discovery only; policy changes are outside scope.

The recommended next operator decision is one of:

1. **Authorize Phase 3b — F1 spec-writing.** Recommended primary.
2. **Authorize Phase 3b-alt — F6 spec-writing.** Recommended alternative.
3. **Remain paused.** Phase 2x Option A continues to be valid; Phase 3a does not require an active path.
4. **Authorize Phase 2z external-evidence-gathering before any Phase 3b.** Phase 2y §8.5 conditional.
5. **Authorize a different family or different scope.** Operator-driven; Phase 3a recommends F1 / F6 but the operator may legitimately choose differently.

Phase 3a explicitly does **not** authorize execution of any kind. The next docs-only phase, whichever it is, becomes a separate operator decision.

---

**End of Phase 3a new-strategy-family discovery memo.** Sections 1–9 complete per the operator brief's required structure. The V1 breakout-continuation family research is paused/completed for now under the Phase 2x family-ceiling assessment + Phase 2y framework-calibration consolidation. A new strategy family is justified now under unchanged operator policy. Eight candidate families enumerated; three classified as near-term candidates (F1 mean-reversion, F6 funding-aware, F3 trend-pullback); F1 ranked rank-1 by structural inversion of V1 breakout's #1 failure mode (chop), v002 dataset sufficiency, §1.7.3 alignment, higher expected trade-count, and moderate implementation budget. Recommended next docs-only phase: **Phase 3b — F1 (mean-reversion-after-overextension) family spec-writing memo**, Phase 2j-style; alternative: Phase 3b-alt — F6 (funding-aware). NO-GO for any execution / paper-shadow / Phase 4 / live-readiness / deployment / threshold-change / project-lock change. R3 baseline-of-record / H0 framework-anchor / R1a-R1b-narrow-R2 retained-research-evidence preserved. Awaiting operator review.
