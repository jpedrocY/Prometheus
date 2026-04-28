# Phase 3f — Next Research-Direction Discovery Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2p consolidation memo (R3 baseline-of-record; future-resumption pre-conditions); Phase 2x family-review memo (V1 breakout family at useful ceiling); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved; framework-calibration question closed without threshold revision); Phase 3a new-strategy-family discovery memo (8-family menu; F1 ranked rank-1 near-term); Phase 3b F1 spec memo §§ 1–15; Phase 3c F1 execution-planning memo §§ 1–13 with operator-mandated amendments; Phase 3d-A / 3d-B1 / 3d-B2 reports; Phase 3d-B2 merge report; Phase 3e post-F1 research consolidation memo + closeout + merge; `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3f — Docs-only **next research-direction discovery memo.** Identifies what kind of research, if any, is most justified after the V1 breakout family reached its useful ceiling, R2 failed under §11.6 cost sensitivity, F1 hard-rejected, and Phase 3e recommended remain paused. **Research-direction-only**, not strategy-execution, not strategy-spec, not backtesting, not parameter search, not paper/shadow planning, not Phase 4 work, not live-readiness, not deployment.

**Branch:** `phase-3f/research-direction-discovery`. **Memo date:** 2026-04-28 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal.** R3 remains V1-breakout baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 remain retained research evidence. F1 framework verdict HARD REJECT. Phase 3d-B2 terminal for F1. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 project-level locks preserved verbatim. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3f is deciding

Phase 3f is a docs-only research-direction discovery phase. It is the natural successor to Phase 3e's "remain paused" recommendation — but with the operator now explicitly authorizing a discovery survey. Phase 3f does **not** override Phase 3e's pause; it asks one further question while remaining within the pause posture:

> Given that the V1 breakout family is at its useful ceiling (Phase 2x), R2 failed §11.6 cost-sensitivity, F1 hard-rejected at first execution, Phase 3d-B2 is terminal for F1, and Phase 3e recommended remain paused, **what kind of research, if any, is most justified as the next docs-only phase?**

Phase 3f is **research-direction-only**, not candidate-execution and not even candidate-spec-writing. It is one level above Phase 3a (which surveyed a family menu and proposed F1 spec-writing as the next downstream phase): Phase 3f surveys at the level of *research kind* — strategy spec memo vs data-requirements memo vs cost-evidence review vs continued pause — and recommends one disciplined next move (which legitimately may remain "remain paused").

What Phase 3f is NOT deciding:

- Not deciding whether to deploy R3 or to begin paper/shadow (forbidden by operator policy).
- Not deciding whether to begin Phase 4 runtime / state / persistence work (forbidden).
- Not deciding whether to lift any §1.7.3 project-level lock.
- Not deciding whether to revise any Phase 2f threshold (Phase 2y closed this; Phase 3e Option E re-affirmed no fresh external trigger).
- Not authorizing any next execution phase, any next implementation phase, any backtest, or any code change.
- Not commencing F1-prime, F1-target-subset, or any F1-derived hypothesis development (forbidden by Phase 3e §8.6 + the explicit Phase 3f operator brief).
- Not commencing R1a-prime, R1b-prime, R2-prime, or any retroactive V1-breakout-family rescue.
- Not authorizing implementation of any chosen direction.
- Not recommending immediate execution.

The output is a candidate research-direction enumeration with disciplined evaluation against the constraints below, plus a single recommended next docs-only phase (or pause). Phase 3f produces a memo; the operator decides whether to authorize anything downstream.

---

## 2. Current canonical project baseline

| Item | State |
|------|-------|
| **R3 (Phase 2j memo §D — Fixed-R + 8-bar time-stop, no trailing)** | **V1 breakout baseline-of-record** per Phase 2p §C.1; locked sub-parameters `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`; same-bar priority STOP > TAKE_PROFIT > TIME_STOP; protective stop never moved intra-trade. |
| **H0 (Phase 2e locked baseline)** | **V1 breakout framework anchor** per Phase 2i §1.7.3; sole §10.3 / §10.4 / §11.3 / §11.4 / §11.6 comparison anchor for all V1-family candidates. |
| **R1a (Phase 2j memo §C — volatility-percentile setup)** | Retained as **research evidence only** per Phase 2p §D; non-leading; symbol-asymmetric mixed-PROMOTE (ETH-favorable / BTC-degrading); ineligible under §1.7.3 BTCUSDT-primary lock without lock revision. |
| **R1b-narrow (Phase 2r — bias-strength magnitude S=0.0020)** | Retained as **research evidence only** per Phase 2s §13; non-leading; formal §10.3.a-on-both PROMOTE but R3-anchor near-neutral marginal contribution; small-sample caveats (BTC n=10 / ETH n=12 R-window). |
| **R2 (Phase 2u — pullback-retest entry topology on top of R3)** | Retained as **research evidence only** per Phase 2w §16.3; **framework FAILED — §11.6 cost-sensitivity blocks** (BTC HIGH-slip Δexp_H0 −0.014; ETH HIGH-slip Δexp_H0 −0.230). M1 + M3 mechanism support but slippage-fragile. |
| **F1 (Phase 3b §4 — mean-reversion-after-overextension)** | Retained as **research evidence only**; **framework verdict HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate (5 separate violations across BTC/ETH × MED/HIGH cells). M1 BTC PARTIAL (mean +0.024 R below +0.10 threshold; fraction non-neg 55.4%); M2 BTC FAIL / ETH weak-PASS; M3 PASS-isolated on both symbols. **Phase 3d-B2 is terminal for F1.** |
| **§1.7.3 project-level locks** | **Preserved verbatim:** BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode. |
| **Phase 2f thresholds** | **Preserved verbatim:** §10.3.a Δexp ≥ +0.10 R; §10.3.c |maxDD| ratio < 1.5×; §10.4 absolute floors expR > −0.50 AND PF > 0.30; §11.3 V-window no-peeking; §11.4 ETH non-catastrophic; **§11.6 = 8 bps HIGH per side** (Phase 2y closeout). |
| **Paper/shadow planning** | **Not authorized.** Operator policy continues to defer paper/shadow indefinitely. |
| **Phase 4 (runtime / state / persistence) work** | **Not authorized.** No runtime / state / persistence implementation has been started. |
| **Live-readiness work, deployment, exchange-write capability, production keys** | **Not authorized.** |
| **MCP / Graphify / `.mcp.json`** | **Not activated, not touched.** |
| **Credentials / `.env` / API keys** | **Not requested, not created, not used.** |

The Phase 3e recommendation (remain paused) governs the project's posture. Phase 3f operates *within* that pause to evaluate whether any disciplined next docs-only phase is more useful than indefinite inertia.

---

## 3. Why research may continue despite Phase 3e's pause recommendation

Phase 3e §7 recommended **remain paused** as the disciplined response to the two-arc evidence pattern. Phase 3f does not contradict that recommendation; Phase 3f operates within it.

Three reasons Phase 3f is consistent with Phase 3e's pause:

1. **The operator explicitly asked for research-direction discovery.** Phase 3e §8 operator decision menu listed seven options; Option A (remain paused) was the primary recommendation; Option B (new Phase 3a-style discovery memo) was listed as not-recommended-now. The operator has now elected, with full Phase 3e context, to authorize a docs-only research-direction discovery — which is structurally a refined Phase 3e Option B. Phase 3e's recommendation was provisional and evidence-based, not definitive; the operator is the decision authority.
2. **Phase 3f is docs-only.** No implementation, no execution, no backtesting, no variant creation, no parameter tuning, no threshold change, no project-lock change. The discovery itself produces no irreversible commitment. Phase 3e's restrictions are preserved verbatim. The pause posture (no paper/shadow, no Phase 4, no live-readiness, no deployment) is unchanged.
3. **No implementation or execution is being authorized.** Phase 3f recommends one next docs-only phase (or no next phase); it does not authorize a Phase 3b / 3c / 3d / 3e / 3f / Phase-4 / deployment phase. Any subsequent docs-only phase would require its own separate operator decision. The chain "discovery memo → spec memo → execution-planning memo → implementation phase → execution phase" has multiple operator-decision gates, none of which Phase 3f short-circuits.

What Phase 3f does NOT do:

- Phase 3f does **not** implicitly lift the Phase 3e remain-paused recommendation for any non-discovery work.
- Phase 3f does **not** authorize paper/shadow planning, Phase 4, live-readiness, deployment, threshold changes, project-lock changes, F1-prime hypothesis development, R3-deployment-readiness work, or any candidate-execution authorization.
- Phase 3f does **not** signal that the project is exiting the post-Phase-3d-B2 / Phase-3e consolidation boundary — only that one further docs-only direction-discovery is being performed at that boundary.

---

## 4. Lessons from failed and retained evidence

The two-arc evidence (V1 breakout Phase 2e–2w; F1 mean-reversion Phase 3a–3d-B2) produced five categorized findings that constrain any next research direction:

### 4.1 R3 — exit redesign helped but did not create positive aggregate edge

**Mechanism:** Replaced H0's staged-trailing topology with a two-rule terminal exit (fixed +2.0 R take-profit + unconditional 8-bar time-stop; protective stop never moved intra-trade).

**What it proved:** Exit-machinery improvements are **cost-robust and broadly improving**: R3 improves expR in all 6 regime-symbol cells; cost-robust at HIGH slippage on both symbols; bit-identical between MARK_PRICE and TRADE_PRICE stop-triggers; first positive ETH-shorts direction-symbol cell (+0.028 R / PF 1.07).

**What it did not prove:** Aggregate R-window expR remains negative on both symbols (BTC −0.240 / ETH −0.351). PF below 1 on both symbols. R3 is "less negative than H0", not break-even.

**Lesson for any next family:** A clean exit-machinery improvement can produce broadly-improving evidence without flipping the absolute-edge sign. Future families should not assume that fixing one structural axis (exit, entry, setup, bias) is sufficient to produce positive aggregate net-of-cost expR; the framework's binding question is the absolute edge, not the marginal improvement vs anchor.

### 4.2 R2 — entry timing helped but failed cost robustness

**Mechanism:** Replaced H0's market-on-next-bar-open entry with conditional-pending pullback-retest entry. Signal at bar B → register PendingCandidate → wait up to 8 bars for low ≤ setup_high (LONG) AND close > structural_stop → fill at next-bar open after confirmation.

**What it proved:** Per-trade expectancy on intersection trades improved (M1 PASS on BTC, +0.123 R per trade direction-symmetric). M3 PASS on both symbols (mechanical R-distance reduction; ratios 0.844 BTC / 0.815 ETH).

**What it did not prove:** §11.6 cost-sensitivity gate FAILS at HIGH on both symbols (BTC Δexp_H0 −0.014; ETH Δexp_H0 −0.230). The first §11.6 failure in the family arc. R2's edge is **slippage-fragile** — at HIGH slippage (8 bps per side), the cost increase ≈ M1's per-trade gain.

**Lesson for any next family:** Pullback-retest geometry produces slippage-fragile edges. Any candidate that places entries close to structural support/resistance (small post-pullback R-distance) shares this geometry and inherits the cost-sensitivity risk. Phase 2y closed the cost-policy review with §11.6 = 8 bps HIGH preserved; future candidates must demonstrate cost-resilience at HIGH slippage, not at LOW or MED only.

### 4.3 F1 — target subset worked but full strategy hard-rejected

**Mechanism:** 8-bar cumulative displacement > 1.75 × ATR(20) → market-fill at next-bar open; SMA(8) frozen target; structural stop with 0.10 × ATR buffer; unconditional 8-bar time-stop; same-direction cooldown until unwind.

**What it proved:** M3 (TARGET-exit subset) PASS on both symbols. The SMA(8) mean-reversion target is profitable when isolated: BTC TARGET subset n=1536 mean +0.7481 R / aggregate +1149.14 R; ETH TARGET subset n=1610 mean +0.8684 R / aggregate +1398.19 R. The mean-reversion target *exists* at the SMA(8) horizon on Binance USDⓈ-M BTCUSDT/ETHUSDT 15m data, in a way that survives round-trip taker fee + MEDIUM slippage + funding cost on the trades that reach it.

**What it did not prove:** The wider F1 strategy-as-specified is catastrophically negative. Three structural failure modes simultaneously: (a) **trade frequency × per-trade negative expR multiplies into catastrophic equity loss** — F1 fires ~150× more trades than H0/R3 (4720+ BTC / 4826 ETH vs 33 baseline) producing R-window total return −546% on BTC at MED slip; (b) **cost-sensitivity slope is steep and uniformly worsening** — even at LOW slippage (1 bps per side) F1 BTC expR=−0.4335; HIGH slippage produces BTC expR=−0.7000 / PF=0.2181; (c) **M2 chop-regime advantage hypothesis falsified on BTC** — F1's BTC low-vol stop-out fraction (55.56%) is *higher* than H0's (46.15%), the opposite of the Phase 3b §2.3 claim.

**Lesson for any next family:** High-frequency strategies amplify per-trade negative expR catastrophically. A profitable target subset (M3 PASS in isolation) does not imply a viable full strategy — selecting the profitable subset *prospectively* requires a separate predicate that does not exist as part of the original spec. Constructing such a predicate post-hoc is forbidden by Phase 2f §11.3.5 (no post-hoc loosening). The R2 → F1 → F1-prime treadmill is exactly what Phase 2x §7.2 / Phase 2p §H.4 / Phase 3e §5.4 explicitly disallow.

### 4.4 R1a / R1b-narrow — filters can improve selected cells but have symbol/asymmetry/sample-size issues

**R1a mechanism:** Volatility-percentile setup-validity predicate (15m ATR(20) at close of bar B−1 in bottom X=25% of trailing N=200-bar ATR distribution).

**What it proved:** ETH improvement substantial and clear (Δexp_H0 +0.362 R / ΔPF +0.512); first positive V-window netPct in project history (+0.69%); first cell with positive expR AND PF > 1 (ETH low-vol +0.281 / 1.353).

**What it did not prove:** **Symbol-asymmetric.** BTC degrades vs R3 (Δexp_R3 −0.180 R; V-window catastrophic at n=4, 0% WR). Ineligible under §1.7.3 BTCUSDT-primary lock without lock revision.

**R1b-narrow mechanism:** Slope-strength magnitude predicate at threshold S=0.0020.

**What it proved:** First candidate to clear §10.3.a-on-both simultaneously at the magnitude threshold (BTC Δexp +0.196 / ETH Δexp +0.251). Cost-monotone; PROMOTES at HIGH slippage.

**What it did not prove:** Trade-count drops 65–70% (BTC 33→10; ETH 33→12). R3-anchor view: roughly neutral marginal contribution on BTC. The §10.3.a clearance is dominated by R3's exit-machinery contribution + filter's trade-count concentration, not by genuine per-trade-expectancy gain on top of R3.

**Lesson for any next family:** Setup/bias filters can improve selected cells while degrading others; symbol-asymmetric variants are ineligible under §1.7.3 BTCUSDT-primary lock without explicit lock revision; trade-count concentration can clear comparison metrics without genuine per-trade-expectancy gain. Future families must avoid the filtering-through-concentration pattern (a §10.3.a clearance via reduced sample isn't a real edge improvement).

### 4.5 The cumulative pattern

Five candidates × five different structural axes (exit, setup, bias, entry, family-shift) under unchanged framework discipline produced:

| Candidate | Axis | Verdict | Binding gate |
|-----------|------|---------|--------------|
| R3 | Exit | PROMOTE — baseline-of-record | None (clean PROMOTE) |
| R1a | Setup | mixed-PROMOTE; non-leading | §1.7.3 BTCUSDT lock (BTC degrades) |
| R1b-narrow | Bias | PROMOTE-with-caveats; non-leading | Sample-fragility + R3-anchor neutrality |
| R2 | Entry | FAILED | §11.6 cost-sensitivity at HIGH |
| F1 | Family-shift | HARD REJECT | §10.4 catastrophic floor (5 violations) |

The framework's binding gates have shifted: early candidates were filtered by symbol-asymmetry (§1.7.3) or sample-fragility; the most recent two candidates were filtered by cost-sensitivity (§11.6) and absolute-edge floor (§10.4 catastrophic). **Cost-sensitivity is now the most consistent binding-gate signal in the project.** Future candidates must structurally avoid cost-fragility geometry (small per-trade R-distance amplified by per-trade cost, or high frequency × negative per-trade expR aggregation), not merely pass it incidentally.

---

## 5. Research constraints for any next family

Per the Phase 3f operator brief, any next research direction must satisfy the following constraints. These are the binding pre-execution discipline requirements derived from §4 lessons:

### 5.1 Frequency-vs-edge constraint

**Must avoid high-frequency cost load unless per-trade edge is large.** F1's catastrophic outcome demonstrates: a strategy with ~4700 trades per 36-month R-window per symbol cannot tolerate per-trade negative expR similar to V1 baseline (~−0.46 R) — the aggregation produces total return ≤ −440%. Future families must either (a) keep trade frequency in the 30–150 trades per R-window per symbol band where per-trade negative expR aggregates to bounded equity loss, OR (b) demonstrate per-trade positive expR substantially above the cost-stack (round-trip taker fee + slippage + funding) before frequency × expR aggregation.

**Implication:** A high-frequency family proposal must produce per-trade expR > 0 plausibly; a low-frequency proposal can tolerate per-trade expR closer to neutral, but still must demonstrate cost-resilience.

### 5.2 Cost-resilience constraint

**Must survive HIGH slippage (§11.6 = 8 bps per side).** R2 demonstrated that pullback-retest geometry produces slippage-fragile edges — the per-trade gain is consumed by HIGH-slip cost. F1 demonstrated that high-frequency mean-reversion-style geometry produces catastrophic-floor violations at HIGH slip. Future families must demonstrate, by construction (not by accidental empirical luck), that the per-trade R-distance and per-trade R-multiple potential are large enough that 8 bps round-trip slippage does not consume the edge.

**Implication:** Any candidate whose entry is placed close to a structural support/resistance level, or whose target is geometrically close to entry (small R-multiple potential), inherits the slippage-fragility risk and must be specifically justified against §11.6.

### 5.3 No retrospective target-subset selection

**Must not rely on retrospective target-subset selection.** F1's M3 PASS demonstrates the SMA(8) target subset is profitable in isolation; constructing a *prospective* selection predicate (one that fires before entry, distinguishing target-eligible from non-target-eligible setups) requires a separate falsifiable hypothesis that does not exist in the F1 spec. Phase 2f §11.3.5 forbids post-hoc loosening; Phase 3e §5.4 + §8.6 forbid F1-prime / target-subset rescue. Future families must not be disguised target-subset rescues of F1, R2, R1a, or any other failed/retained candidate.

**Implication:** Any candidate that selectively activates only on bars/conditions where a known-failed candidate would have produced its profitable subset is forbidden as a disguised post-hoc rescue. The mechanism predicate must be developed independently and must be falsifiable before any execution.

### 5.4 BTCUSDT-primary plausibility

**Must have BTCUSDT-primary plausibility.** §1.7.3 designates BTCUSDT as the v1 live primary symbol; ETHUSDT is research/comparison only. R1a's symbol-asymmetric mixed-PROMOTE (ETH-favorable / BTC-degrading) is the precedent for what is *not* eligible — a candidate that improves ETH while degrading BTC under unchanged §1.7.3 is non-leading. Future families must produce, by hypothesis at minimum and ideally by mechanism reasoning, a credible BTC-friendly thesis. ETH evidence is informative but cannot be the primary edge case.

**Implication:** Family proposals where the underlying mechanism is structurally ETH-favorable (e.g., higher-noise-leveraging strategies) cannot be promoted on ETH evidence alone. F5 (BTC/ETH relative-strength) is BLOCKED by §1.7.3 + one-symbol-only live scope without a separate operator-policy revision.

### 5.5 v002 dataset sufficiency

**Must use v002 data unless a separate data-requirements phase is justified.** Phase 2e v002 datasets are locked: BTCUSDT/ETHUSDT 15m + derived 1h + mark-price + funding + exchangeInfo. Any new feature dataset (e.g., overextension predicates, retracement features) is a *derived* dataset on top of v002 and creates a versioned feature dataset (per Phase 2e v002 framing + dataset-versioning policy) without a v003 raw-data bump. A new raw-data dataset (v003) requires a separate operator-authorized data-requirements phase.

**Implication:** Family proposals that require ETH spread/depth microstructure data, off-chain data, on-chain data, social/sentiment data, alternative venues, or other non-v002 raw inputs trigger a v003 data-requirements precondition — which itself is a docs-only phase but is *not* a strategy-discovery phase.

### 5.6 Falsifiable mechanism before implementation

**Must be falsifiable before implementation.** Phase 3b's M1/M2/M3 falsifiable mechanism predictions for F1 are the discipline standard. Future family proposals must, at the spec stage, define falsifiable mechanism predictions that are testable independently of the §10.3-style comparison metrics — so that "mechanism PASS / framework FAIL" outcomes are separable and informative regardless of the framework verdict.

**Implication:** A family proposed without falsifiable mechanism predictions is not a research candidate; it is a parameter sweep awaiting a hypothesis. Phase 2j §C.6 / §11.3.5 binding rule applies.

### 5.7 No disguised V1-breakout / F1-target-subset rescue

**Must not be another disguised V1 breakout or F1 target-subset rescue.** A candidate that is structurally another V1-breakout setup-axis variant (e.g., a different volatility-compression predicate while still using the V1 breakout's range-and-bar-close-confirmation logic) is not a family shift — it is another R1a-shaped variant inside the V1 family. Phase 2x §5 family-ceiling assessment applies. A candidate that selectively activates F1-style overextension setups while filtering for "TARGET-eligible" subsets (without an independently-developed predicate) is a disguised F1-prime rescue forbidden by Phase 3e §5.4 + §8.6.

**Implication:** Family-shift cleanliness is a discipline question. Phase 2i §1.7 binding test (rule-shape change vs parameter-tuning under another label) applies. The Phase 3a §5 classifications ("research-only later" for F2 volatility-redesigned because of family-shift cleanliness uncertainty) apply with renewed force after F1's HARD REJECT — the project should not accept another F1-shape risk lightly.

---

## 6. Candidate research directions to evaluate

Per the Phase 3f operator brief, the eight candidate research directions are enumerated below. Each is named with a one-line core hypothesis. §7 evaluates each against the §5 constraints; §8 ranks; §9 recommends.

| # | Direction | One-line core hypothesis |
|---|-----------|---------------------------|
| **D1** | Funding-aware directional / carry-aware strategy | Use Binance USDⓈ-M funding-rate extremes as either a contrarian directional signal or a cost-discount filter for an existing directional thesis. |
| **D2** | Volatility contraction / expansion redesigned from first principles | After a low-volatility compression regime ends with a volatility expansion shock, position with the directional bias of the shock — but specified independently of breakout-family setup logic. |
| **D3** | Regime-first framework | Build a regime classifier and dispatch to family-specific sub-strategies; family-of-families rather than a single strategy. |
| **D4** | Trend pullback / continuation, explicitly avoiding R2-style slippage fragility | In an established trend, after a counter-trend retracement, position with the trend on retracement-completion confirmation — but with entry geometry designed *ex-ante* to avoid R2's small-R-distance slippage-fragility precedent. |
| **D5** | BTC / ETH relative strength / spread or rotation strategy | Trade the relative-strength relationship between BTC and ETH; long the leader and short the laggard, or rotate single-leg between them based on relative-strength signal. |
| **D6** | Range-bound regime strategy | When the market is in a confirmed range, fade extremes (sell tops, buy bottoms within range); exit on range-edge violation or mean-revert target. |
| **D7** | External execution-cost evidence review | Audit the §11.6 = 8 bps HIGH per side calibration against current Binance USDⓈ-M live-execution slippage / fee evidence; not a strategy redesign; framework-calibration-only. |
| **D8** | Pause / no further active research | Hold the post-Phase-3e consolidation state indefinitely; no next research-direction phase authorized. |

D1, D2, D4, D6 map roughly to Phase 3a F6, F2, F3, F4 respectively (with §5 constraints applied with renewed strictness post-F1 HARD REJECT). D3 maps to Phase 3a F7. D5 maps to Phase 3a F5. D7 is the Phase 3e §8.5 Option E (also called the Phase 2y §8.5 / Phase 2x §6 Option C path). D8 is the Phase 3e §7 + §8.1 primary recommendation.

Note on absent candidates: Phase 3a F8 (ML-assisted forecasting) is explicitly not enumerated here per the Phase 3f operator brief framing and per project-level documentation (`current-project-state.md`: "not self-learning in v1"; `.claude/rules/prometheus-core.md`). F1-prime / F1-target-subset rescue is explicitly not enumerated per the Phase 3f operator brief ("Do not authorize implementation [of] F1-prime"). R3-deployment / paper-shadow / Phase-4-readiness directions are explicitly not enumerated per operator policy.

---

## 7. Per-candidate evaluation

Each direction is evaluated against twelve attributes derived from the Phase 3f operator brief: (a) core hypothesis; (b) which prior failure mode it addresses; (c) which prior failure mode it risks repeating; (d) required data; (e) v002 sufficient?; (f) expected trade frequency; (g) expected cost sensitivity; (h) BTCUSDT-primary plausibility; (i) implementation complexity; (j) overfitting risk; (k) validation difficulty; (l) whether it should proceed now.

### 7.1 D1 — Funding-aware directional / carry-aware strategy

| Attribute | Detail |
|-----------|--------|
| **(a) Core hypothesis** | Two falsifiable sub-hypotheses: (1) **funding-rate extremes are contrarian directional signals** — when longs pay shorts heavily (positive extreme funding), short positions have a positive carry tailwind that compensates for adverse selection; (2) **funding-aware filtering of an existing directional thesis** — only take long signals when funding is neutral-or-negative; only take short signals when funding is neutral-or-positive — using funding as a cost-discount filter rather than primary signal. |
| **(b) Failure mode addressed** | F1's high-frequency cost-load failure (D1 fires only on funding extremes which are episodic, ~5–15 events per month). R2's slippage-fragility (D1's per-trade R-distance is not constrained to be small; entry can be at next-bar open with structural stop similar to V1 baseline). V1 breakout's regime-incompatibility (volatility-shock conditions; failure mode #4) — funding extremes often precede regime shifts. |
| **(c) Failure mode risked** | Sample-size fragility: funding extremes are episodic (Binance funds every 8 hours; meaningful extremes occur 5–15× per month in volatile regimes, fewer in quiet regimes). Per-fold sample counts could be 10–25 trades per symbol per 6-month fold, comparable to or smaller than V1 breakout's tight per-fold counts. R1b-narrow's sample-fragility precedent applies. **Smaller risk:** could empirically not beat the §10.4 absolute floor without trade-count concentration artifacts. |
| **(d) Required data** | 15m + 1h OHLCV (BTC); funding-rate history; mark-price (for carry-cost calculations). All in v002. |
| **(e) v002 sufficient?** | **YES.** D1 uniquely leverages a v002 dataset feature (funding rates) that V1 breakout did not exploit as primary signal and F1 used only as cost-component. |
| **(f) Expected trade frequency** | **Low-to-moderate.** Variant (1) ~5–15 trades per month per symbol; variant (2) inherits underlying directional-thesis frequency reduced by funding-filter pass-through rate. Both substantially lower than F1; likely lower than V1 breakout. |
| **(g) Expected cost sensitivity** | **Lower than F1, R2, D2, D4, D6.** Funding is a known carry component already in the cost stack; if the strategy actively harvests funding, the carry cost becomes a carry benefit. Sub-variant (2) (funding as filter) is cost-neutral relative to base directional thesis. **Among all candidates, D1 has the lowest expected cost-sensitivity profile.** |
| **(h) BTCUSDT-primary plausibility** | **High.** BTC funding is more liquid / larger volume / more reliable than ETH funding (Phase 3a §4.6). ETH funding rates can be more erratic; BTC's tighter funding-extreme distribution favors a contrarian-funding thesis. §1.7.3 BTCUSDT-primary alignment is natural. |
| **(i) Implementation complexity** | **Medium.** New funding-feature dataset (derived); signal logic; standard execution layer. Estimate: 1500–2500 lines including tests. Comparable to F1. |
| **(j) Overfitting risk** | **Moderate.** Funding-extreme threshold, hold-period, position-direction logic. Smaller parameter space than D2 / D3 / D6. Phase 2j §C.6 / §11.3.5 single-sub-parameter commitment applies cleanly. |
| **(k) Validation difficulty** | **Moderate.** Sample-size is the watchpoint (funding extremes are episodic; per-fold counts could be fragile). Cost-sensitivity sweep (LOW / MED / HIGH) and §11.6 evaluation apply cleanly. Standard Phase 2j → 2k → 2l-style cycle fits. |
| **(l) Should proceed now?** | **PROVISIONAL YES** as the highest-ranked active path, conditional on operator preference for an active path. Cleanest §5-constraint compliance among active candidates. The lowest-cost-sensitivity active candidate after F1's HARD REJECT made cost-sensitivity the binding gate. |

### 7.2 D2 — Volatility contraction / expansion redesigned from first principles

| Attribute | Detail |
|-----------|--------|
| **(a) Core hypothesis** | Volatility regime transitions (compression-end → expansion-onset) are predictable signals; trade the expansion direction with rule-set independent of V1 breakout's range-and-bar-close-confirmation logic. Could be Bollinger-band squeeze release, ATR-percentile transition, or volatility-of-volatility shock. |
| **(b) Failure mode addressed** | V1 breakout's exhaustion failure mode (#3) — D2 positions on regime-transition direction rather than on bar-close-confirmation, sidestepping the exhaustion pattern. |
| **(c) Failure mode risked** | **Family-shift cleanliness uncertain (Phase 3a §4.2 + §5 already classified D2 as research-only-later for this reason).** Risk of accidentally specifying a candidate too close to the V1 breakout family — a "volatility-redesign" that ends up being V1 breakout with different setup-window logic is not a family shift; it's another setup-axis variant inside the breakout family. Phase 2i §1.7 binding-test (rule-shape change vs parameter-tuning) would require careful application. **R2-style slippage fragility risk:** if entries are placed at expansion-onset close to a volatility-band level, the R-distance geometry could inherit R2's cost-fragility. |
| **(d) Required data** | 15m + 1h OHLCV; ATR(N) for multiple N; Bollinger / Keltner-style envelopes; volatility-percentile features. v002. |
| **(e) v002 sufficient?** | **YES** with new derived features. |
| **(f) Expected trade frequency** | **Comparable to V1 breakout** (volatility-regime transitions are structurally similar in frequency to compression-then-breakout). 30–50 trades per symbol per R-window. |
| **(g) Expected cost sensitivity** | **Moderate.** Could be more cost-robust than F1 if entries are at expansion-onset (similar to R3's structural exit-machinery improvement); could be less cost-robust if entries are at compressed pullback levels (R2 geometry inheritance). Specification-dependent. |
| **(h) BTCUSDT-primary plausibility** | **Uncertain.** Volatility-regime transitions are universal but their predictability differs by symbol; possibly inherits some of breakout-family's BTC/ETH asymmetry. |
| **(i) Implementation complexity** | **High.** Multi-feature regime classifier + execution rules. Estimate: 2500–3500 lines including tests. Higher than D1. |
| **(j) Overfitting risk** | **Higher than D1.** Many parameters (compression-window length, expansion threshold, regime-classifier choice, multiple ATR horizons). Phase 2i §3.2 logic that excluded R1b-broad applies symmetrically. |
| **(k) Validation difficulty** | **High.** Multiple parameters increase the §11.3.5 single-sub-parameter-commitment burden; risk of accidentally specifying a candidate too close to V1 breakout. |
| **(l) Should proceed now?** | **NO.** Family-shift cleanliness uncertainty + R2-style slippage-fragility risk + higher overfitting risk than D1. Phase 3a §5 classification "research-only later" applies with renewed strictness post-F1 HARD REJECT. Could be revisited if the operator independently develops a clean regime-transition mechanism that demonstrably differs from V1 breakout setup logic. |

### 7.3 D3 — Regime-first framework

| Attribute | Detail |
|-----------|--------|
| **(a) Core hypothesis** | A meta-strategy that classifies the current regime (trending / range-bound / shock; low-vol / med-vol / high-vol; risk-on / risk-off) and dispatches to family-specific sub-strategies. The hypothesis is that the right strategy depends on regime, and a regime-aware framework outperforms any single regime-blind strategy. |
| **(b) Failure mode addressed** | Potentially all four V1 breakout failure modes (chop is handled by mean-reversion sub-strategy; reversal-lag by switching off trend-filter sub-strategies; exhaustion by mean-reversion sub-strategies; volatility shocks by regime-shift detection). F1's chop-regime advantage hypothesis (which falsified on BTC) could in principle be rehabilitated as a *conditional* hypothesis rather than a strategy-wide hypothesis. |
| **(c) Failure mode risked** | **Implementation complexity is the binding blocker.** Regime-classifier hyperparameters + sub-strategy hyperparameters compound multiplicatively. Phase 2i §3.2's exclusion logic for R1b-broad applies in extreme form. Regime-shift detection latency adds a systematic cost (entries/exits at regime boundaries are typically less favorable). Phase 3a §4.7 / §5 classified F7 as "blocked by complexity" for these reasons. |
| **(d) Required data** | All inputs from D1, D2, D4, D6 combined. |
| **(e) v002 sufficient?** | **YES** for research; v003 not required initially. |
| **(f) Expected trade frequency** | **Moderate** (aggregate across sub-strategies). |
| **(g) Expected cost sensitivity** | **High** — inherits the worst-case cost-sensitivity of the constituent sub-strategies. Regime-shift detection latency adds a systematic cost. |
| **(h) BTCUSDT-primary plausibility** | Inherits the BTC/ETH asymmetry profile of each sub-strategy. |
| **(i) Implementation complexity** | **Very high.** Regime-classifier module + multiple sub-strategy modules + dispatch logic + transition handling + regime-confidence reporting. Estimate: 8000+ lines including tests. Significantly larger than any single Phase 2 / Phase 3 candidate. |
| **(j) Overfitting risk** | **Very high.** Multiplicative parameter space. |
| **(k) Validation difficulty** | **Very high.** Phase 2f §11.2 fold-consistency and §11.6 cost-sensitivity become harder to reason about when the strategy itself shifts behavior across folds. The §10.3 framework's threshold mechanics were calibrated on single-strategy candidates. |
| **(l) Should proceed now?** | **NO.** Blocked by complexity (Phase 3a §5 classification "blocked by complexity" stands; renewed force post-F1 HARD REJECT). Premature relative to current operator policy (Phase 4 runtime infrastructure not authorized; D3 is structurally Phase-4-dependent). D3 is a long-horizon family-of-families ambition, not a near-term Phase 3g-equivalent candidate. |

### 7.4 D4 — Trend pullback / continuation, explicitly avoiding R2-style slippage fragility

| Attribute | Detail |
|-----------|--------|
| **(a) Core hypothesis** | In an established trend (defined by a higher-timeframe filter similar to V1's 1h EMA structure), after a counter-trend retracement of definite depth, trend resumption is more likely than reversal. **Crucially:** entry geometry must be designed *ex-ante* to avoid R2's small-R-distance slippage-fragility precedent — e.g., entry on retracement-completion *with confirmation bar* placing entry far enough from the structural stop that 8 bps round-trip slippage does not consume per-trade edge. |
| **(b) Failure mode addressed** | V1 breakout's lagging-bias-during-reversals failure mode (#2) — partial avoidance. V1's exhaustion failure mode (#3) — entry on retracement-completion sidesteps breakout-exhaustion. F1's high-frequency cost-load failure — D4 fires less frequently than F1 (one trade per pullback per trend, not per overextension event). |
| **(c) Failure mode risked** | **R2 slippage-fragility precedent is the central risk.** R2's M1 + M3 mechanism PASSED in Phase 2w; R2's §11.6 gate FAILED at HIGH on both symbols. Trend-pullback families share R2's pullback-retest geometry by construction. The operator brief explicitly says "avoiding R2-style slippage fragility" — but without a specific structural redesign of entry geometry that demonstrably differs from R2's, the proposal inherits R2's risk. **Phase 2y closed Option C with §11.6 = 8 bps unchanged**, so the cost-sensitivity question is not relaxed for D4. |
| **(d) Required data** | 15m + 1h OHLCV; EMA/SMA stack; retracement / Fibonacci-style measurements; ATR. All in v002. |
| **(e) v002 sufficient?** | **YES** with new derived features (retracement detection, fast/slow EMA stack). |
| **(f) Expected trade frequency** | **Comparable to or lower than V1 breakout** (fewer pullbacks than breakouts in a given trend). 20–35 trades per symbol per R-window. **Sample-size concern** — same magnitude as V1 breakout, which already strained per-fold §11.2 evaluation. |
| **(g) Expected cost sensitivity** | **High by structural inheritance from R2.** Pullback entries place entry close to a structural support/resistance, producing tight stops by geometry — same as R2's mechanism. The "explicitly avoiding R2-style slippage fragility" clause requires a specific entry-geometry redesign that demonstrably increases R-distance — but no such redesign is currently developed. |
| **(h) BTCUSDT-primary plausibility** | **Possibly BTC-friendly under R3's exit machinery** (the M1 +0.123 R BTC intersection-trade gain in Phase 2w R2 was direction-symmetric). But the §11.6 failure on R2 BTC was also at HIGH — the BTC-friendliness was undone by HIGH slippage. |
| **(i) Implementation complexity** | **Medium-High.** Retracement-detection logic non-trivial; trend-filter logic re-uses V1 patterns. Estimate: 1800–2800 lines including tests. |
| **(j) Overfitting risk** | **Moderate.** Multiple parameters (retracement depth, trend-filter thresholds, confirmation rule). Lower than D2 / D6 because the trend filter can mirror V1's documented EMA(50)/EMA(200) structure (familiar baseline). |
| **(k) Validation difficulty** | **Moderate** for §10.3 / §11.2 / §11.4; **high** for §11.6 — expect cost-fragility and need for explicit slippage-sweep + geometry-redesign justification. |
| **(l) Should proceed now?** | **NO.** Without an independently-developed redesign of entry geometry that demonstrably differs from R2's pullback-retest, D4 inherits R2's §11.6 fragility risk. The operator brief's "explicitly avoiding R2-style slippage fragility" qualifier requires a specific mechanism that does not yet exist; D4 should not be authorized as a docs-only spec phase until such a mechanism is operator-developed. Phase 3a §5 classified F3 as "near-term candidate (with caveats)" but renewed Phase 3d-B2 evidence (cost-sensitivity is now the most consistent binding-gate signal) elevates the caveat into a blocker. |

### 7.5 D5 — BTC / ETH relative strength / spread or rotation strategy

| Attribute | Detail |
|-----------|--------|
| **(a) Core hypothesis** | BTC/ETH relative strength is mean-reverting or trending at predictable horizons. Trade the relationship: long the leader and short the laggard (spread trade), or rotate single-leg long-only between the two based on relative-strength signal. |
| **(b) Failure mode addressed** | V1 breakout's volatility-shock failure mode (#4) — partial avoidance via market-neutrality of spread trades. |
| **(c) Failure mode risked** | **BLOCKED by §1.7.3 BTCUSDT-primary lock and one-symbol-only live scope.** D5 cannot be deployed live without lifting two project-level locks (BTCUSDT-primary AND one-symbol-only). The locks were established in Phase 2i and are explicitly preserved through Phase 2y / Phase 3e. D5 is research-only under unchanged operator policy. Phase 4 runtime / state / persistence would also require multi-symbol-aware redesign, which is not the current scope. |
| **(d) Required data** | 15m + 1h OHLCV for both BTC and ETH; relative-strength index (price ratio, return-correlation); spread-construction primitives. v002 sufficient for research; ETH-specific microstructure data (depth, spread distribution) is not in v002 but is needed for live-realism assessment per Phase 2y §5.1.2. |
| **(e) v002 sufficient?** | **YES for research backtest;** v003 ETH-microstructure dataset would be needed before live deployment. |
| **(f) Expected trade frequency** | **Lower** — relative-strength trades have longer hold periods and fewer setups. 10–20 trades per R-window combined. **Sample-size concern is acute.** |
| **(g) Expected cost sensitivity** | **High** — two-leg trades double the cost-stack (entry + exit on each leg = 4 fee + 4 slippage events vs 2 + 2 for single-leg). ETH leg's wider spread (per Phase 2y §5.1.8) compounds. |
| **(h) BTCUSDT-primary plausibility** | **Both symbols required by construction.** This is the only direction on the menu that requires BTC AND ETH simultaneously. |
| **(i) Implementation complexity** | **High.** Two-leg execution, dual-symbol order management, spread reconciliation logic. Significant runtime infrastructure beyond v1's one-position-one-symbol architecture. |
| **(j) Overfitting risk** | **High.** Multi-asset families have larger parameter spaces (signal definition, hedge ratio, leg-correlation requirement, cooldowns). |
| **(k) Validation difficulty** | **High.** Sample-size, parameter-space, and execution-realism all compound. |
| **(l) Should proceed now?** | **NO. Blocked by §1.7.3 lock.** Cannot proceed without an explicit operator-policy revision lifting BTCUSDT-primary AND one-symbol-only live locks — which is outside Phase 3f scope. D5 is research-only-later per Phase 3a §5; renewed force post-F1 HARD REJECT. |

### 7.6 D6 — Range-bound regime strategy

| Attribute | Detail |
|-----------|--------|
| **(a) Core hypothesis** | When the market is in a confirmed range (defined by N consecutive bars within a bounded width relative to ATR), fade range extremes — sell tops, buy bottoms — with target at midpoint or opposite extreme, exit on range-edge violation. |
| **(b) Failure mode addressed** | V1 breakout's chop-with-false-breaks failure mode (#1) — strongest avoidance among candidates. F1 attempted to address the same failure mode and HARD REJECTED; D6 is structurally similar to F1 but with different setup discipline. |
| **(c) Failure mode risked** | **F1-shape risk: D6 has the highest expected cost-sensitivity among candidates (Phase 3a §4.4 / §5 / 5.1 evaluation).** Range-trading uses tight stops just outside range edges and targets at range midpoints — small absolute price moves. Per-trade R-multiples are small. Per-trade cost is a substantial fraction of edge. **Renewed force post-F1 HARD REJECT:** F1 already demonstrated that small-R-multiple mean-reversion-like candidates fail catastrophically at HIGH slippage on BTC. D6 inherits F1's structural fragility. |
| **(d) Required data** | 15m + 1h OHLCV; range-detection features (rolling high/low, range-width-vs-ATR ratio, range-violation detection). v002. |
| **(e) v002 sufficient?** | **YES.** |
| **(f) Expected trade frequency** | **Variable** — depends entirely on regime mix. Could be 0–2 trades per fold during trending periods (range-trading inactive), 5–10 trades per fold during ranging periods. Aggregate could be 25–50 trades per symbol per R-window. |
| **(g) Expected cost sensitivity** | **Very high.** Phase 3a §4.4 classified F4 as "highest expected cost-sensitivity" among the original 8-family menu. F1's HARD REJECT on similar small-R-multiple geometry confirms the risk empirically. |
| **(h) BTCUSDT-primary plausibility** | **Potentially symmetric.** Both BTC and ETH exhibit range-bound regimes; the regime-mix differs more than within-regime profitability. ETH's wider spreads / shallower depth (Phase 2y §5.1.8) makes ETH execution less attractive. |
| **(i) Implementation complexity** | **High.** Range-detection logic + entry-at-extreme + range-violation exit + range-end / regime-shift detection. Estimate: 2500–3500 lines including tests. |
| **(j) Overfitting risk** | **Moderate-to-high.** Range-detection itself is sensitive to lookback window, width threshold, and regime-end detection. |
| **(k) Validation difficulty** | **High.** Cost-sensitivity sweep and §11.6 gate are the binding constraints. Per-fold sample sizes will be very uneven (zero trades in trending folds, larger samples in ranging folds), complicating §11.2 fold-consistency evaluation. |
| **(l) Should proceed now?** | **NO.** F1-shape cost-sensitivity risk is confirmed empirically by F1 HARD REJECT. D6's small-R-multiple geometry is structurally fragile under §11.6 = 8 bps HIGH. Phase 3a §5 classified F4 as "research-only later"; renewed strictness post-F1 HARD REJECT. Could be revisited only if external execution-cost evidence (D7) materially revises §11.6 calibration — which is itself not currently authorized. |

### 7.7 D7 — External execution-cost evidence review

| Attribute | Detail |
|-----------|--------|
| **(a) Core hypothesis** | Audit the §11.6 = 8 bps HIGH per side calibration against current Binance USDⓈ-M live-execution slippage / fee evidence. **Not a strategy redesign.** Framework-calibration only. Output: confirmation that 8 bps is correctly calibrated, OR documented evidence that revision is justified, OR documented evidence that the current threshold is too loose. |
| **(b) Failure mode addressed** | None directly. Indirectly: if §11.6 is over-conservative, D4 / D6 / future entry-axis candidates could be re-evaluated under revised threshold; if §11.6 is under-conservative, future candidates are filtered more strictly. |
| **(c) Failure mode risked** | **Post-hoc-loosening trap (Phase 2f §11.3.5; Phase 3e §8.5).** D7 must be invoked as an *audit*, not as a way to retroactively rehabilitate R2 or F1 without independent external evidence. Phase 2y closed the same review path with "no threshold revision; preserve §11.6 = 8 bps". Phase 3e §8.5 said "no fresh external evidence is currently asserted; revisiting cost-policy without external trigger risks the post-hoc-loosening trap." |
| **(d) Required data** | External: Binance USDⓈ-M BTCUSDT futures live slippage / depth / spread / fee evidence (operator-gathered or third-party). No internal data. |
| **(e) v002 sufficient?** | N/A (D7 is framework-calibration, not strategy research). |
| **(f) Expected trade frequency** | N/A. |
| **(g) Expected cost sensitivity** | N/A. |
| **(h) BTCUSDT-primary plausibility** | N/A — D7 is symbol-agnostic by design. |
| **(i) Implementation complexity** | **Low.** Docs-only review; no code change; outputs a markdown memo. |
| **(j) Overfitting risk** | **Low** if D7 follows the discipline framework: the audit must be independent of any specific candidate's framework outcome. **High** if D7 is invoked specifically to rescue R2 or F1 — that would be exactly the post-hoc-loosening trap. |
| **(k) Validation difficulty** | **Moderate.** Output is a documented evidence-and-reasoning memo; the discipline check is "would the operator have produced the same conclusion without knowing R2's or F1's framework verdicts?" |
| **(l) Should proceed now?** | **CONDITIONAL — second-best active path if D1 is not preferred.** D7 is genuinely informative regardless of outcome (confirmation OR revision both clarify the framework-calibration question). Disciplined invocation requires the operator to commit *ex-ante* to "outcome could go either way; threshold revision is not the goal". F1's HARD REJECT at HIGH (BTC expR=−0.7000 / PF=0.2181) is fresh empirical evidence that strengthens the case for *checking* §11.6 against external data — not for revising it. The Phase 2y §5.3 / Phase 3e §8.5 prior of "no fresh external evidence is asserted" is now arguable: F1's catastrophic-floor at HIGH is itself empirical evidence that warrants verification against live-trading cost realism. **Disciplined GO** if the operator wants an active path that does not commit to a new strategy direction. |

### 7.8 D8 — Pause / no further active research

| Attribute | Detail |
|-----------|--------|
| **(a) Core hypothesis** | The post-Phase-3e consolidation state is the right place to be. No next research-direction phase is authorized; the project remains paused awaiting operator strategic choice. |
| **(b) Failure mode addressed** | Treadmill risk. Phase 2x §7.2 / Phase 3e §7 framing applies: authorizing another active phase without a strong independently-developed hypothesis risks producing another mixed/failed result that does not advance the strategic question. |
| **(c) Failure mode risked** | Project momentum loss; strategic clarity may degrade if pause is indefinite. |
| **(d) Required data** | None. |
| **(e) v002 sufficient?** | N/A. |
| **(f) Expected trade frequency** | N/A. |
| **(g) Expected cost sensitivity** | N/A. |
| **(h) BTCUSDT-primary plausibility** | N/A. |
| **(i) Implementation complexity** | **None.** No phase authorized. |
| **(j) Overfitting risk** | None. |
| **(k) Validation difficulty** | None. |
| **(l) Should proceed now?** | **DEFAULT PRIMARY (per Phase 3e §7 + §8.1 + §9).** Phase 3f does not contradict Phase 3e's pause recommendation. D8 is the disciplined default; D1 / D7 are the disciplined active alternatives if the operator prefers an active path within the pause posture. |

---

## 8. Ranking

Per the Phase 3f operator brief, the eight candidates are classified into:

- **Near-term docs-only candidate** — could be authorized as next docs-only phase under unchanged operator policy.
- **Later research candidate** — credible direction but not next; could be revisited if specific preconditions are met.
- **Blocked by data** — needs new raw-data ingestion (v003-equivalent) before research can begin.
- **Blocked by complexity** — implementation / validation cost too high for the next phase boundary.
- **Not recommended** — fundamentally misaligned with v1 scope, current evidence, or §5 constraints.

| # | Direction | Classification | Primary blocker / driver |
|---|-----------|----------------|--------------------------|
| **D1** | Funding-aware directional / carry-aware | **Near-term docs-only candidate (rank 1)** | Strongest §5-constraint compliance. Lowest expected cost-sensitivity. v002 sufficient. BTC-friendly. Episodic frequency avoids F1's failure mode. Falsifiable two-sub-hypothesis structure. |
| **D7** | External execution-cost evidence review | **Near-term docs-only candidate (rank 2)** | Framework-calibration question is binding (cost-sensitivity is now most consistent failure-mode signal). F1 HARD REJECT at HIGH provides arguable fresh empirical trigger. Disciplined invocation possible; post-hoc-loosening trap avoidable with explicit operator commitment. |
| **D8** | Pause / no further active research | **Default primary (consistent with Phase 3e §9)** | Disciplined default if no active path is operator-preferred. Phase 3e recommendation already endorses this; Phase 3f does not contradict. |
| **D2** | Volatility contraction / expansion redesigned | **Later research candidate** | Family-shift cleanliness uncertain (Phase 3a §4.2). R2-style slippage-fragility risk unresolved. Higher overfitting risk than D1. Could be revisited if operator independently develops a clean regime-transition mechanism that demonstrably differs from V1 breakout setup logic. |
| **D4** | Trend pullback / continuation, avoiding R2-style fragility | **Later research candidate** | The "avoiding R2-style slippage fragility" qualifier requires a specific entry-geometry redesign that demonstrably differs from R2's pullback-retest. No such redesign currently developed. Could be revisited after operator-developed redesign or D7 outcome materially revises §11.6. |
| **D6** | Range-bound regime strategy | **Later research candidate (downgraded post-F1)** | F1-shape cost-sensitivity risk confirmed empirically. Small-R-multiple geometry is structurally fragile under §11.6 = 8 bps HIGH. Phase 3a §5 "research-only later" classification now strengthened to "downgraded post-F1". |
| **D5** | BTC / ETH relative strength / spread | **Blocked by §1.7.3 lock** | Cannot proceed without explicit operator-policy revision lifting BTCUSDT-primary AND one-symbol-only locks — outside Phase 3f scope. v003 ETH-microstructure data also blocking for live deployment. |
| **D3** | Regime-first framework | **Blocked by complexity** | Implementation budget (~8000+ lines) and Phase 4 runtime infrastructure dependence make D3 premature. Phase 4 not authorized. Long-horizon meta-framework, not a near-term direction. |

### 8.1 Near-term docs-only candidate ranking

Two near-term active candidates (D1, D7) plus one default-primary (D8). Ranked:

**Rank 1 (active path) — D1 (Funding-aware directional / carry-aware).** Strongest case:

- Cleanest §5-constraint compliance among active candidates: lowest expected cost-sensitivity (addresses §5.2); episodic frequency (addresses §5.1); v002 sufficient (addresses §5.5); BTC-friendly mechanism (addresses §5.4); two falsifiable sub-hypotheses (addresses §5.6); not a disguised V1-breakout or F1-target-subset rescue (addresses §5.7).
- Phase 3a §5 classified F6 as "near-term candidate" (rank 2 after F1); F1's HARD REJECT now elevates the rank-2 candidate to rank-1 active path.
- v002 funding-rate dataset is the unique v002 feature not yet exploited by V1 breakout (used only as cost-component) or F1 (used only as cost-component).
- Two falsifiable sub-hypotheses (contrarian directional vs cost-discount filter) provide a built-in A/B comparison structure, similar to Phase 2j §C / §D's R1a-vs-R3 structure.

**Rank 2 (active path) — D7 (External execution-cost evidence review).** Useful but conditional:

- F1's HARD REJECT at HIGH (BTC expR=−0.7000 / PF=0.2181) is fresh empirical evidence that the cost-sensitivity gate is binding for at least one mean-reversion-like family. Verifying §11.6 calibration against live-trading cost realism is now arguably triggered.
- Disciplined invocation requires the operator to commit *ex-ante* to "outcome could go either way; revision is not the goal". The Phase 2y precedent + Phase 3e §8.5 caution applies.
- Genuinely informative regardless of outcome: confirmation strengthens the F1 HARD REJECT and R2 FAILED verdicts; revision could re-open D4 / D6 evaluation under revised threshold; tightening would filter future candidates more strictly.

**Default primary (no active path) — D8 (Pause).** Phase 3e §7 + §8.1 + §9 recommendation. Phase 3f does not contradict this. If the operator does not prefer either D1 or D7, D8 remains the disciplined default.

### 8.2 Why D1 over D7 over D8 (if active path is preferred)

- **D1 vs D7:** D1 is a strategy-direction discovery; D7 is a framework-calibration audit. D1 directly progresses toward potentially testing a new family that addresses F1's structural failure modes; D7 informs *all* future candidates equally without committing to any. If the operator prefers progress on a strategy direction, D1 is primary; if the operator prefers confirming the framework before any new strategy work, D7 is primary. They are not mutually exclusive — D7 could precede D1 — but Phase 3f recommends D1 as primary because the §5 lessons already show cost-sensitivity is binding (D7 would likely confirm 8 bps HIGH rather than revise it; D1 is informative regardless of D7 outcome).
- **D1 vs D8:** D8 is the disciplined default; D1 is the disciplined active alternative within the pause posture. D1 produces a docs-only spec memo (a separate operator-decision phase); no implementation, execution, or paper/shadow authorization is implied. The operator may legitimately prefer D8 if the project should remain in indefinite pause until a fundamentally different framework or hypothesis emerges.

### 8.3 Why D2 / D4 / D6 / D5 / D3 are not recommended now

- **D2 (Volatility contraction redesigned):** Family-shift cleanliness uncertainty + R2-style slippage-fragility risk + higher overfitting risk than D1. Renewed Phase 3a §5 "research-only later".
- **D4 (Trend pullback avoiding R2 fragility):** No specific redesign of entry geometry currently developed. Operator brief's "explicitly avoiding" qualifier requires a mechanism that does not yet exist.
- **D6 (Range-bound):** F1-shape cost-sensitivity risk confirmed empirically. Small-R-multiple geometry structurally fragile under §11.6.
- **D5 (BTC/ETH relative strength):** Blocked by §1.7.3 lock without explicit operator-policy revision (outside Phase 3f scope).
- **D3 (Regime-first framework):** Blocked by complexity and Phase 4 dependence.

---

## 9. Recommended next operator decision

Per the Phase 3f operator brief constraint (acceptable: remain paused; spec memo for one direction; data-requirements memo; external-cost-evidence review), Phase 3f recommends one of these.

**Primary recommendation: authorize a docs-only spec memo for D1 — funding-aware directional / carry-aware strategy.**

This recommendation reflects:

- The operator's stated preference for active research-direction discovery (Phase 3f authorization itself);
- The strongest §5-constraint compliance among active candidates (D1 cleanly satisfies §5.1 frequency, §5.2 cost-resilience, §5.4 BTC-primary, §5.5 v002, §5.6 falsifiability, §5.7 not-disguised-rescue);
- F1's HARD REJECT making cost-sensitivity the binding gate (D1's lowest-cost-sensitivity profile addresses this most directly);
- v002 sufficiency (no v003 raw-data dependency);
- Disciplined progression analogous to Phase 2j-style spec-writing for V1-family or Phase 3b-style for F1.

**Alternative active recommendation (operator preference for framework-calibration over strategy-direction):** authorize **D7 — external execution-cost evidence review.**

**Default recommendation (operator preference for indefinite pause):** **remain paused** per Phase 3e §9.

**Phase 3f does NOT recommend:**

- Authorizing implementation, backtesting, paper/shadow, Phase 4, live-readiness, or deployment work (forbidden by Phase 3f operator brief).
- Authorizing D2 / D3 / D4 / D5 / D6 (per §8.3).
- Authorizing F1-prime, F1-target-subset, R1a-prime, R1b-prime, R2-prime, or any retroactive V1-breakout-family rescue (forbidden).
- Authorizing a separate data-requirements memo as primary (no near-term candidate requires v003 raw-data; D5 would but D5 is §1.7.3-blocked anyway).

The recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 10. Proposed next docs-only phase (if D1 is authorized)

If the operator selects D1 as the next docs-only phase, the proposal is:

### 10.1 Proposed phase name

**Phase 3g — Funding-aware directional / carry-aware strategy spec memo (Phase 3b-style).**

### 10.2 Purpose

Produce a docs-only spec memo for the D1 funding-aware family that:

1. States the market-hypothesis with falsifiable mechanism predictions (M1 / M2 / M3 equivalents — e.g., M1: post-extreme-funding-event mean-reversion at horizon h; M2: regime-conditional hold-period behavior; M3: cost-discount-filter pass-through rate × per-trade R for the filter sub-variant).
2. Selects between the two D1 sub-hypotheses (contrarian directional vs cost-discount filter) or specifies both for comparison.
3. Locks singular committed sub-parameters per Phase 2j §C.6 / §11.3.5 discipline (funding-extreme threshold; hold-period; position-direction logic; entry timing; exit logic; cooldown rule; stop-distance band).
4. Specifies the Phase 3a §4.6 BTC/ETH expected behavior with §11.4 ETH-comparison plan.
5. Specifies cost-sensitivity expectations for LOW / MED / HIGH per Phase 2f §11.6 (acknowledging D1's structural lower-cost-sensitivity claim must be empirically demonstrable).
6. Specifies sample-size expectations and per-fold §11.2 plan (D1's episodic frequency may produce 10–25 trades per symbol per 6-month fold — sample-size is the watchpoint).
7. Specifies implementation surface estimate per Phase 2t §J.6 framing.
8. Specifies a pre-declared Phase 3c-equivalent execution-planning gate for any eventual execution phase.

### 10.3 Strict scope

Phase 3g is **docs-only**. Produces a memo under `docs/00-meta/implementation-reports/`. Does NOT:

- Authorize execution.
- Authorize implementation.
- Authorize backtesting.
- Authorize parameter tuning.
- Change any threshold, strategy parameter, or project-level lock.
- Change any V1 / F1 / control behavior.
- Touch any source code, test, or script.
- Touch `data/`.
- Touch MCP / Graphify / `.mcp.json` / credentials / exchange-write paths.
- Authorize paper/shadow, Phase 4, live-readiness, or deployment work.
- Propose F1-prime, F1-target-subset, R1a-prime, R1b-prime, R2-prime, or any retroactive rescue.

### 10.4 Why it is justified

- D1 is the highest-ranked active candidate per §8.1.
- Cost-sensitivity is the binding gate post-F1 HARD REJECT; D1 has the lowest expected cost-sensitivity profile among candidates.
- D1 uniquely leverages v002 funding-rate data not yet exploited as primary signal.
- D1 is BTC-friendly per Phase 3a §4.6, aligning with §1.7.3 BTCUSDT-primary lock.
- D1 has falsifiable sub-hypotheses (contrarian vs filter), enabling A/B comparison structure.
- D1's episodic frequency avoids F1's catastrophic-frequency × per-trade-loss aggregation.
- D1 is not a disguised V1-breakout or F1-target-subset rescue.
- A spec memo is the standard disciplined Phase 3b-style entry point; producing one does not commit to execution.

### 10.5 Why it does not violate Phase 3e's paused state

- Phase 3e is docs-only; Phase 3g would also be docs-only.
- Phase 3e does not authorize paper/shadow, Phase 4, live-readiness, deployment, threshold change, project-lock change; Phase 3g preserves all of those.
- Phase 3e §8.2 considered Option B (Phase 3a-style discovery memo) as not-recommended-now without operator hypothesis development; the Phase 3f operator brief's authorization of Phase 3f (research-direction discovery) plus the Phase 3f §9 recommendation of D1 specifically constitutes operator-driven hypothesis selection.
- Phase 3g does not begin implementation. Each subsequent phase (Phase 3h-equivalent execution-planning; Phase 3i-equivalent implementation; Phase 3j-equivalent execution) requires its own separate operator-decision gate.
- Phase 3g respects Phase 3e's recommendation that the project should "pause and let the operator strategically choose, not keep pushing variants through framework discipline" — by limiting itself to spec memo (not parameter sweep, not execution).

### 10.6 NO-GO conditions

Phase 3g must NOT proceed if:

- The operator chooses D7 or D8 as the next decision instead of D1.
- The operator chooses to develop an F1-prime, F1-target-subset, or other retroactive rescue (forbidden; Phase 3e §8.6 + Phase 3f §5.7).
- The operator chooses to revise §11.6 = 8 bps HIGH without external evidence (Phase 2f §11.3.5 forbidden post-hoc loosening).
- The operator chooses to lift §1.7.3 BTCUSDT-primary or one-symbol-only locks (outside Phase 3f scope).
- An implementation issue or documentation inconsistency in prior phase records emerges that requires a docs-only correction phase before any further strategy work.

Phase 3g, if authorized, terminates at the spec memo. No execution, implementation, or parameter sweep is implied. An eventual Phase 3h (execution-planning) or Phase 3i (implementation) would require fresh operator authorization and would be subject to all current restrictions plus any restrictions defined in the Phase 3g spec memo itself.

---

## 11. Explicit preservation list

Phase 3f is docs-only and explicitly preserves all of the following verbatim:

- **No threshold changes.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / **§11.6 = 8 bps HIGH per side** preserved verbatim per Phase 2f §11.3.5 / Phase 2y closeout / Phase 3e §11.
- **No strategy-parameter changes.** R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`); H0 baseline (range-based setup, 1h binary slope-3 bias + EMA(50)/EMA(200), 0.10 × ATR breakout buffer, staged-trailing exit, 0.10 × ATR structural-stop buffer); R1a sub-parameters (volatility-percentile X=25 / N=200); R1b-narrow sub-parameter (slope-strength magnitude S=0.0020); R2 sub-parameters (pullback-retest with 8-bar validity window; 5-step precedence; fill-time stop-distance re-check); F1 spec axes (overextension window 8; threshold 1.75 × ATR(20); mean-reference window 8; stop buffer 0.10 × ATR(20); time-stop 8 bars; stop-distance band [0.60, 1.80] × ATR(20); cooldown rule; no regime filter; market entry at next-bar open). All preserved verbatim.
- **No project-lock changes.** §1.7.3 locks (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; one active protective stop max; 0.25% risk per trade; 2× leverage cap; mark-price stops; v002 datasets; one-way mode; isolated margin; no pyramiding; no reversal while positioned; no hedge mode) preserved verbatim.
- **No paper/shadow planning is authorized.** Phase 3e §11 deferral stands.
- **No Phase 4 (runtime / state / persistence) work is authorized.** Phase 3e §11 deferral stands.
- **No live-readiness work is authorized.** No deployment, no exchange-write capability, no production keys. Phase 3e §11 deferral stands.
- **No deployment work is authorized.**
- **No credentials.** No production / sandbox / testnet API keys requested, created, or used. No `.env` file modified. No secrets in any committed file.
- **No MCP / Graphify / `.mcp.json` activation.** No MCP server enabled; no Graphify integration; no `.mcp.json` file created or modified.
- **No exchange-write paths.** No exchange-write capability proposed, implemented, or enabled. `BacktestAdapter.FAKE` remains the only adapter type in the engine.
- **No `data/` commits.** Phase 3f commits are limited to two `docs/00-meta/implementation-reports/` files.
- **No code change.** No file in `src/`, `tests/`, `scripts/`, or `.claude/` is touched by Phase 3f.
- **No existing-spec change.** `v1-breakout-strategy-spec.md`, `v1-breakout-validation-checklist.md`, `cost-modeling.md`, `backtesting-principles.md`, `phase-gates.md`, `technical-debt-register.md`, `data-requirements.md`, `dataset-versioning.md`, `current-project-state.md`, `ai-coding-handoff.md` all preserved.
- **R3 remains V1 breakout baseline-of-record** per Phase 2p §C.1.
- **H0 remains V1 breakout framework anchor** per Phase 2i §1.7.3.
- **R1a / R1b-narrow / R2 / F1 remain retained as research evidence only.** R2 framework verdict FAILED — §11.6 cost-sensitivity blocks. F1 framework verdict HARD REJECT. Phase 3d-B2 terminal for F1.

---

**End of Phase 3f next research-direction discovery memo.** Phase 3f operates within Phase 3e's pause posture to evaluate one further docs-only direction-discovery question at the post-Phase-3d-B2 / Phase-3e consolidation boundary. Eight candidate research directions enumerated (D1 funding-aware; D2 volatility-redesigned; D3 regime-first; D4 trend-pullback-avoiding-R2; D5 BTC/ETH relative strength; D6 range-bound; D7 external cost evidence; D8 pause). Two near-term active candidates (D1 rank-1; D7 rank-2); one default primary (D8 consistent with Phase 3e); five later/blocked (D2 / D3 / D4 / D5 / D6). Recommended next operator decision: **authorize a docs-only spec memo for D1 (funding-aware directional / carry-aware strategy)** as the disciplined active alternative to D8 pause. Alternative active recommendation: D7 external execution-cost evidence review. Default recommendation: remain paused per Phase 3e §9. R3 baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved. §11.6 = 8 bps HIGH preserved verbatim. §1.7.3 locks preserved verbatim. No paper/shadow, no Phase 4, no live-readiness, no deployment, no implementation, no execution, no backtest, no parameter tuning, no threshold change, no project-lock change, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits, no code change. Awaiting operator review.
