# Phase 2r — Gate 1 Planning Memo (Hypothesis-Selection)

**Phase:** 2r — Docs-only Hypothesis-Planning (single-candidate selection).
**Branch:** `phase-2r/gate-1-planning-memo`.
**Memo date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.

**Authority:** Phase 2q decision memo (review-only; recommended Option A primary, Option B fallback for docs-only hypothesis-planning); Phase 2p consolidation memo (R3 = baseline-of-record; R1a = retained-for-future-hypothesis-planning); Phase 2o asymmetry-review memo (most-supported asymmetry explanations: C.1 symbol-specific market behavior + C.5 directional-bias interaction); Phase 2n strategy-review memo; Phase 2m comparison report (R1a+R3 formal-but-mixed PROMOTE); Phase 2l comparison report (R3 broad-based PROMOTE); Phase 2j memo §C / §D specs; Phase 2i §1.7.3 project-level locks; Phase 2f §§ 8–11 thresholds (preserved unchanged per §11.3.5).

**Status:** Decision memo only. No code changes, no new backtests, no new variants, no parameter changes, no candidate-set widening, no Phase 4 / paper-shadow / live-readiness work. The recommendation is **provisional**; the operator decides whether to authorize a Phase 2r-execution spec-writing follow-on.

---

## 1. Plain-English explanation of what Phase 2r is deciding

Phase 2q recommended remain-paused as primary and docs-only hypothesis-planning as fallback. The operator has authorized Phase 2r as the docs-only hypothesis-planning fallback, with three explicit candidate redesigns plus a "remain paused" option. **This memo is the Gate 1 decision step** — not the spec-writing itself. It evaluates the four options against the accumulated Phase 2l–2q evidence and recommends exactly one path forward.

The recommendation is one of:

- **Path A** — proceed to docs-only spec-writing for **regime-conditional R1a-prime**.
- **Path B** — proceed to docs-only spec-writing for **R1b — bias-strength redesign**.
- **Path C** — proceed to docs-only spec-writing for **R2 — pullback-entry redesign**.
- **Path D** — recommend remaining paused (no spec-writing follow-on); Phase 2r closes here.

Phase 2r does not execute anything. It does not write code. It does not run backtests. If a candidate is selected, the next step (subject to a separate operator approval) is a Phase 2j-style spec-writing phase that produces a falsifiable hypothesis with sub-parameters committed singularly, and that spec phase itself does not authorize execution — execution would require a still-later operator-approved Gate 1 cycle.

## 2. Summary of the R3 / R1a evidence that matters for next-hypothesis choice

### 2.1 R3 evidence (Phase 2l)

R3 (locked exit baseline: `exit_kind=FIXED_R_TIME_STOP`, R-target=2.0, time-stop=8 bars; protective stop never moved) cleared §10.3.a + §10.3.c on **both** BTC and ETH against the H0 anchor:

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|-------:|-------:|--------:|------:|--------:|--------:|
| H0  BTC |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% |
| R3  BTC |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% |
| H0  ETH |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% |
| R3  ETH |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% |

Per-fold (5 rolling, GAP-036): R3 beats H0 in **4/5 BTC folds** and **3/5 ETH folds**. First-ever positive BTC fold expR (F2 +0.015, F3 +0.100). Per-regime: R3 improves expR in **all 6 regime-symbol cells**. V-window confirms direction-of-improvement on both symbols. Implementation clean. Robust to slippage and stop-trigger sensitivity.

**What this means for next-hypothesis choice.** R3 is the locked exit baseline. Any next hypothesis is "X on top of R3" — keeping R3's exit machinery and changing one upstream axis. The R3 R-window and V-window numbers above are the locked control reference for any future evaluation alongside H0.

### 2.2 R1a+R3 evidence (Phase 2m)

R1a (volatility-percentile setup, X = 25 / N = 200) on top of R3 cleared §10.3 formally but with strategically mixed evidence:

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|-------:|-------:|--------:|------:|--------:|--------:|
| R1a+R3 BTC |  22 | 27.27% | **−0.420** | **0.355** |  −2.07% |  −2.33% |
| R1a+R3 ETH |  23 | 34.78% | **−0.114** | **0.833** |  −0.59% |  −2.96% |

H0-anchor deltas (governing): BTC Δexp **+0.039** / ΔPF +0.100; ETH Δexp **+0.362** / ΔPF +0.512. BTC clears §10.3.c only (Δexp below §10.3.a's +0.10 threshold); ETH clears §10.3.a + §10.3.c.

R3-anchor deltas (descriptive only): BTC Δexp **−0.180** / ΔPF **−0.205** (R1a hurts BTC); ETH Δexp **+0.237** / ΔPF **+0.359** (R1a helps ETH).

V-window: ETH **first positive netPct ever** (8 trades / 62.5% WR / expR +0.386 / PF 2.222 / netPct +0.69%). BTC severely degraded (4 trades / 0% WR / expR −0.990).

Per-regime cells of note (Phase 2m §6.1):
- **R1a+R3 ETH low_vol** n=11 expR **+0.281** / PF **1.353** — first regime-symbol cell with positive expR AND PF > 1.
- **R1a+R3 ETH shorts** n=16 expR **+0.387** / PF **1.906** — strongest direction-symbol cell ever observed.
- **R1a+R3 BTC low_vol** n=17 expR **−0.329** (vs R3 BTC low_vol −0.054) — R1a actively hurts BTC's low-vol regime where R3 was strongest.
- **R1a+R3 BTC longs** −0.363 / shorts −0.488 — direction-symmetric, both negative.
- **R1a+R3 ETH longs** −1.259 / shorts +0.387 — direction-asymmetric; ETH-shorts dominate.

R1a is **mechanically correct**: 100% of filled R1a entries at ATR percentile ≤ 25%, exactly per Phase 2j §C.5 spec.

### 2.3 What the asymmetry diagnosis (Phase 2o) concluded

Phase 2o §C evaluated six candidate explanations for the BTC/ETH asymmetry. The two best-supported:

- **C.1 Symbol-specific market behavior.** BTC and ETH have intrinsically different post-compression follow-through on the v002 R-window data. R1a's filter exposes that pre-existing difference.
- **C.5 Directional-bias interaction.** R1a amplifies a pre-existing ETH-favorable directional regime; the breakout-on-bias entry rule interacts with R1a's compression filter differently across symbols. ETH was already direction-asymmetric under R3 alone (longs −0.934 / shorts +0.028 in Phase 2l); R1a amplifies that pattern. BTC was direction-symmetric under R3 (longs −0.252 / shorts −0.230); R1a keeps it direction-symmetric and weakly negative.

Phase 2o §E concluded: R1a is mechanically correct and selects genuine compression on both symbols. **The asymmetry is in post-compression follow-through, not in the compression definition.** The asymmetry is consistent with facts about underlying market structure × strategy interaction rather than with a fixable R1a defect.

### 2.4 Family-level observations for next-hypothesis choice

- **Two PROMOTEs, zero clean negatives.** Phase 2h §11.1 stopping rule (clean negative required) not met; the family is alive.
- **Absolute aggregate expR remains negative on R for both candidates.** R3 BTC −0.240 / ETH −0.351; R1a+R3 BTC −0.420 / ETH −0.114. The framework clears improvements; it has not yet cleared a positive-aggregate-edge result.
- **Wave-1 (Phase 2g) eliminated four parametric paths.** Setup-window length, expansion threshold, EMA pair, break-even threshold all REJECTED. Single-axis parameter changes on those four axes have been exhausted.
- **Phase 2i originally excluded R1b and R2** for stated reasons — R1b for higher overfitting risk in regime classifiers; R2 for new pending-limit-fill backtester logic + lower trade count threatening per-fold consistency.

## 3. Evaluation of each candidate

### 3.1 Regime-conditional R1a-prime

**What problem it tries to solve.** R1a's BTC penalty under R1a+R3. Apply R1a's percentile filter only when an additional regime gate condition is met (e.g., 1h volatility regime, trend strength, or a hybrid of both); the gate would activate R1a where it works (predominantly ETH low_vol) and avoid it where it doesn't (BTC).

**Why it may help BTC specifically.** If BTC's R1a degradation is concentrated in specific regimes (Phase 2m §6.1: BTC low_vol n=17 expR −0.329 is the largest-sample cell of degradation), a gate that excludes BTC low_vol from R1a's filter could flip that regime back to R3-alone behaviour (BTC low_vol −0.054 / 0.890 under R3-only). In principle this could recover R3's broad-based BTC behaviour while preserving R1a's ETH benefit.

**Why it may preserve or harm ETH.** ETH's R1a benefit is concentrated in low_vol (R1a+R3 ETH low_vol +0.281 / PF 1.353). A regime gate that *excludes* low_vol on BTC but *includes* it on ETH would require a symbol-aware rule, conflicting with §1.7.3. A symbol-blind gate (e.g., "apply R1a only when 1h vol is high") would invert the regime mix and almost certainly destroy ETH's signal.

**Overfitting risk.** **HIGH.** Phase 2o §F.1 explicitly flagged this. The temptation to pick a gate condition that "happens to" map to the cells where R1a worked vs didn't is post-hoc by definition — selecting parameters from observed data without an out-of-sample hold-out is exactly what Phase 2f §11.3.5 forbids. Any gate parameter would need to be committed *singularly* and *ex-ante* with no tuning.

**Phase 2i / Phase 2p constraint compliance.** PARTIAL. The single-axis structural-change requirement (Phase 2i §1.7.1 binding test) is at risk: a gate-on-top-of-R1a is **not a single-axis structural change** — it is a multi-axis bundled redesign (R1a's percentile predicate + a new regime gate). Phase 2j discipline forbids bundled candidates without explicit operator authorization.

If the gate is reframed as a *replacement* setup-validity rule (e.g., "compression AND regime is X" as a single new predicate shape), it could be specified single-axis — but the line between "regime-conditional R1a" and "a new bundled predicate with regime + compression terms" is thin and would require careful spec discipline to avoid drift.

**Falsifiability.** YES if specified properly. The hypothesis "R1a-prime with gate condition Y produces a §10.3-passing result on **both** BTC and ETH" is falsifiable. The risk is in *Y*: if Y is fitted to the observed data, the falsifiability is hollow.

**Phase 2r verdict on this candidate.** Plausible mechanism (regime-mix), but high overfitting risk and constraint-compliance fragility. The most-supported asymmetry diagnosis (Phase 2o §C.1 and §C.5) is *not* "R1a's regime mix" — it is "post-compression follow-through differs by symbol regardless of how R1a is gated". A regime gate addresses regime-mix, not follow-through.

### 3.2 R1b — bias-strength redesign

**What problem it tries to solve.** H0's bias rule classifies each 1h bar as LONG / SHORT / NEUTRAL using a binary cascade (EMA(50) > EMA(200) AND close > EMA(50) AND EMA(50) > EMA(50)[3 bars ago] for LONG; symmetric for SHORT). The rule does **not distinguish strong vs weak directional setups**. R1b would condition entries on bias **strength** — e.g., requiring that the slope-3 measurement clear a magnitude threshold, not just have the correct sign.

**Why it may help BTC specifically.** Phase 2o §C.5 most-supported asymmetry explanation: the breakout-on-bias entry rule interacts with R1a's compression filter differently across symbols because of pre-existing directional regime asymmetry. ETH was already direction-asymmetric (shorts +0.028 / longs −0.934 under R3 alone); BTC was direction-symmetric. If H0's bias rule admits weak-directional setups whose post-compression follow-through is unreliable, requiring stronger bias would filter those out. This effect should be most pronounced on BTC, where weak-directional setups are more common (BTC's bias regime in the R window is less directionally concentrated than ETH's).

**Why it may preserve or harm ETH.** ETH's strong directional regime should still produce strong-bias bars; a strength threshold doesn't preferentially exclude ETH's directional setups. The likely effect on ETH is trade-count reduction (fewer weak-bias entries) without a meaningful expR degradation, possibly even modest improvement if some of the weak-bias ETH long entries (which are catastrophic under R1a+R3 ETH longs −1.259) are excluded.

**Overfitting risk.** **MEDIUM.** R1b adds **one new threshold** to the existing slope-3 measurement. The threshold value would need to be committed singularly and ex-ante. The slope-strength rule is a single-axis structural change to the bias-validity predicate, analogous in scope to R1a's single-axis structural change to the setup-validity predicate. If the threshold is selected from a project-convention default (e.g., "bottom-of-research-band 0.10% per 3 bars" ≈ ATR-normalized minimum) rather than tuned, overfitting risk is contained.

**Phase 2i / Phase 2p constraint compliance.** YES. Single-axis structural change to the bias rule. One sub-parameter (threshold value). Falsifiable. Cross-symbol relevant. Does **not** conflict with §1.7.3 (no symbol-conditional logic). Does not require new backtester capability (the slope-3 measurement already exists in `bias.py` and `_update_1h_bias`). Phase 2j-style spec is achievable.

The original Phase 2i §3.2 R1b exclusion was for "regime classifiers have higher DOF / harder cross-symbol robustness". A narrowly-scoped bias-**strength** variant — a single threshold on the existing slope-3 measurement, not a multi-parameter regime classifier — has substantially lower DOF than the regime-classifier framing Phase 2i excluded. The narrow framing addresses the original objection.

**Falsifiability.** YES, clean. The hypothesis is testable in a Phase 2j-style spec phase with a singular committed threshold.

**Phase 2r verdict on this candidate.** Strongest mechanistic fit to Phase 2o §C.5 directional-bias interaction diagnosis. Clean single-axis structural change. Lowest implementation cost (no new backtester capability). Achievable Phase 2j-style spec. Cross-symbol relevant. Overfitting risk is genuine but containable via project-convention default for the threshold.

### 3.3 R2 — pullback-entry redesign

**What problem it tries to solve.** H0's entry timing is "market entry at the close of the breakout bar" (more precisely: market order on the next bar's open after the breakout bar's close). This commits the entry as soon as the breakout signal fires, regardless of whether the move follows through. R2 would replace this with a **pullback entry**: after the breakout bar's close, place a pending limit order at the breakout bar's level (or a fraction toward the setup midpoint) and only fill if the market retraces and confirms the breakout.

**Why it may help BTC specifically.** The Phase 2o §C diagnosis of "asymmetric post-compression follow-through" is *directly* about whether breakouts follow through. BTC's R1a+R3 degradation pattern (Phase 2m §6.1: BTC compression bars selected, but trade outcomes negative) is consistent with "BTC compression bars produce more false breakouts than ETH compression bars". A pullback-entry mechanism by definition only fills when the market gives back some of the breakout move and then re-confirms — filtering out failed breakouts that don't have follow-through. This addresses the *root* mechanism Phase 2o identified, not a regime-mix proxy or a bias-strength proxy.

**Why it may preserve or harm ETH.** Pullback entries have a known fill-rate cost: if ETH's directional regime produces strong follow-through *without* meaningful pullbacks, R2 may fail to fill on bars where H0 / R3 / R1a+R3 successfully entered. Trade count would drop; if the dropped trades were ETH winners (under R1a+R3 ETH the +0.69% V netPct came from a small number of TAKE_PROFIT trades; missing a few of those would substantially erode the V signal), R2 could *harm* ETH.

**Overfitting risk.** **LOW-MEDIUM.** Pullback entry is a well-documented, theoretically-grounded mechanism (mean-reversion confirmation of breakout); it is not a fitted-to-data rule. The single sub-parameter would be the pullback target (e.g., "limit at breakout bar's high - 0.5 × breakout-bar range" or "limit at the setup-window midpoint"); committing this singularly per Phase 2j discipline is straightforward. Less post-hoc risk than R1a-prime.

**Phase 2i / Phase 2p constraint compliance.** PARTIAL. Two material concerns:

1. **New backtester capability required.** H0 / R3 / R1a+R3 all use market entry on next-bar open. R2 needs pending-limit-fill logic: place limit order at bar B's close; check whether bar B+1 (or B+K for some K) trades through the limit price; if yes, fill at the limit price; if not, cancel and miss the trade. This is ~50–150 lines of new code in the backtester engine, plus tests. **Phase 2r is docs-only**; the backtester change would be in a future execution phase. So this is a future-phase implementation cost, not a Phase 2r blocker, but it shapes whether Phase 2r recommends spec-writing.

2. **Lower trade count threatens fold consistency.** Phase 2i §3.2 originally excluded R2 partly for this reason: pullback fill rates of 30–60% would reduce per-fold sample sizes. With R3-only at 33 trades on R, R2 might produce 10–20 trades — close to the threshold below which §10.3 confidence becomes fragile. The GAP-036 5-rolling fold convention with 6m test windows would have ≤ 4 trades per fold for many folds.

**Falsifiability.** YES. The hypothesis is testable. The hypothesis would have to acknowledge that fill-rate is itself an experimental variable.

**Phase 2r verdict on this candidate.** Strongest *mechanism fit* to the Phase 2o asymmetry diagnosis (directly addresses post-compression follow-through). Lowest *post-hoc* overfitting risk among the three structural candidates. But two real concerns: future-phase implementation cost (new backtester capability) and trade-count fragility. Phase 2r is docs-only so the implementation cost is deferred; the trade-count concern is genuine but can be partially mitigated by spec-phase analysis (e.g., simulating expected fill rates from existing trade-log MFE distributions before committing).

### 3.4 Remain paused

**What problem it tries to solve.** Avoids treadmill behaviour. Phase 2q already recommended remain-paused as primary.

**Why it may help BTC.** Doesn't help — but also doesn't risk further mixed-result evidence that complicates the consolidation.

**Why it may preserve or harm ETH.** Doesn't change anything.

**Overfitting risk.** ZERO.

**Phase 2i / Phase 2p constraint compliance.** Trivially YES. Every restriction is honored.

**Falsifiability.** N/A — not a research hypothesis.

**Phase 2r verdict on this candidate.** Always available as the disciplined default. The Phase 2q memo recommended this as primary with Option B (docs-only hypothesis-planning) as fallback. The operator authorized the fallback, opening Phase 2r. If Phase 2r determines that none of the three candidates is sufficiently justified for spec-writing, remain-paused is the appropriate Phase 2r recommendation — Phase 2q's primary stands.

## 4. Recommended path

This recommendation is **provisional and evidence-based, not definitive**. The operator decides.

### 4.1 Recommended path: Path B — proceed to docs-only spec-writing for R1b — bias-strength redesign

**Reasoning.**

1. **Mechanistic fit to the Phase 2o diagnosis.** The two best-supported asymmetry explanations were §C.5 directional-bias interaction and §C.1 symbol-specific market behavior. R1b directly addresses §C.5 — it changes the bias rule, which is the rule that Phase 2o identified as interacting differently across symbols. R1a-prime addresses regime-mix, which is a secondary contributing factor (§C.2) rather than a primary explanation. R2 addresses post-compression follow-through, which is mechanistically the most direct fit but at higher implementation cost. Among the three, R1b has the cleanest mechanism-to-spec ratio.

2. **Single-axis structural change.** R1b adds **one** threshold to the existing slope-3 measurement. The bias-validity predicate's rule shape changes (binary directional cascade → strength-conditional cascade); no new inputs, no new indicators, no new backtester capability. Phase 2j-style spec is straightforward.

3. **Cross-symbol relevance.** R1b is symbol-blind. It affects both BTC and ETH simultaneously. There is no symbol-conditional logic; §1.7.3 BTC-primary lock is preserved. The hypothesis's predicted effect (improve BTC by filtering weak-directional setups; preserve ETH by leaving strong-directional setups) is testable on both symbols without requiring policy lift.

4. **Lower overfitting risk than R1a-prime.** R1a-prime salvages a previously-tested filter; the temptation to fit the gate to where R1a worked is structural. R1b tests an independent mechanism (bias strength) with a single committed threshold from a project-convention default; the post-hoc surface is much smaller.

5. **Lower implementation cost than R2.** R1b reuses existing slope-3 measurement infrastructure; R2 needs new pending-limit-fill backtester logic. While Phase 2r is docs-only and implementation cost is a future-phase issue, the recommendation considers the *full path* — a hypothesis whose execution phase requires substantial backtester development is reasonable to spec only if the mechanism justifies it. R2's mechanism is strong, but R1b's is also strong with no implementation overhead.

6. **R1b-narrow addresses the original Phase 2i §3.2 R1b exclusion.** The original exclusion was for "regime classifiers have higher DOF / harder cross-symbol robustness". A narrowly-scoped bias-**strength** variant (single threshold on existing slope-3) is *not* a regime classifier; it is a single-axis structural change to the bias-validity predicate, analogous to R1a's single-axis change to the setup-validity predicate. The narrow framing addresses the original objection while preserving the mechanism Phase 2o identified.

### 4.2 Why not Path A (R1a-prime)

The most-supported asymmetry diagnosis (Phase 2o §C.1 + §C.5) is *not* "R1a's regime mix is wrong"; it is "post-compression follow-through differs by symbol regardless of how R1a is gated". A regime gate addresses a secondary factor (§C.2 regime-composition) rather than the primary mechanism. Phase 2o §F.1 explicitly flagged R1a-prime's high overfitting risk. The natural-feeling-but-wrong path; the disciplined choice is to address the diagnosed mechanism, not the surface symptom.

### 4.3 Why not Path C (R2)

R2 has the strongest direct mechanism fit (post-compression follow-through is exactly what R2 addresses). But two concerns push the recommendation toward R1b:

- **Future-phase implementation cost.** A future execution phase for R2 would require ~50–150 lines of new pending-limit-fill backtester code plus tests. R1b's execution phase needs only a bias-rule modification.
- **Trade-count fragility.** R2's expected fill rate of 30–60% would reduce R-window trade counts to ~10–20 per symbol, threatening the GAP-036 fold-consistency analysis. R1b's expected effect is trade-count *reduction* (filtering weak-bias setups) but at a much smaller magnitude (probably 10–25%) — preserving fold consistency.

R2 stays alive as a *future* candidate. If R1b execution clears or fails, R2 becomes the natural next-axis structural-redesign candidate at that point.

### 4.4 Why not Path D (remain paused)

R1b is "sufficiently justified" by Phase 2r's bar (clean mechanism fit, single-axis structural, sub-parameter committable singularly, no operator-policy conflict, falsifiable hypothesis formulable now). Phase 2r's role is precisely to evaluate whether *any* candidate clears this bar, and R1b does. Defaulting to remain-paused when a candidate clears the bar would be over-conservative.

That said, the operator may legitimately prefer Path D over Path B if the operator independently judges that:

- The Phase 2q memo's "stay paused" recommendation should hold (overrides this Phase 2r evaluation).
- The cost of one more docs-only spec phase exceeds its EVI given the deferred operational context.
- The Phase 2i §3.2 R1b exclusion stands (the operator may judge that "bias-strength" is too close to "regime classifier" to escape the original objection).

Path D is always available as the operator's judgement call; Phase 2r's structured recommendation is Path B.

## 5. Selected path

**Path B — proceed to docs-only spec-writing for R1b — bias-strength redesign.**

## 6. Proposed hypothesis statement

**If H0's bias rule admits weak-directional setups whose post-compression follow-through is unreliable — and if requiring a stronger directional gradient is a clean structural change that filters those weak setups without symbol-conditional logic — then a bias-strength threshold on the existing 1h slope-3 measurement should improve aggregate expR vs H0 under the unchanged Phase 2f framework, with the improvement most pronounced on BTCUSDT (where the bias regime is more directionally muted than ETHUSDT) and with no §10.3 disqualification floor triggered on either symbol.**

In standard Phase 2j §C-style hypothesis form:

> R1b-narrow hypothesis (pre-committable in spec phase): On R = 2022-01-01 → 2025-01-01 with v002 datasets, an R1b-narrow variant (H0 bias rule + a single bias-strength threshold S on the existing 1h slope-3 measurement; setup, trigger, stop, sizing, R3 exit logic all preserved unchanged) produces a §10.3-passing result vs H0 baseline — i.e., either §10.3.a (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05) or §10.3.b (Δexp ≥ 0 AND trades changes within tolerance) or §10.3.c (strict dominance), with no §10.3 disqualification floor triggered (no worse expR, no worse PF, |maxDD| ≤ 1.5× baseline).
>
> The hypothesis is FALSIFIED if R1b-narrow fails §10.3 on BTC OR triggers §10.3 disqualification on BTC, OR triggers §10.3 disqualification on ETH per §11.4 ETH-as-comparison rule.
>
> The hypothesis is INDETERMINATE if R1b-narrow clears §10.3 on R but fails on V per §11.3 no-peeking discipline.

The threshold value S is **deliberately not committed in this Phase 2r Gate 1 memo**. Phase 2r Gate 1 selects the candidate axis only. The Phase 2r spec-writing follow-on (subject to a separate operator approval) is responsible for committing S singularly per Phase 2j-style discipline, with a project-convention rationale for the chosen value (e.g., "S = 0.10% per 3 bars — bottom of research band, not selected by fitting") rather than tuning S on observed data.

## 7. Definition of the next Phase 2r deliverable if approved

If the operator approves Path B, the next deliverable is a **Phase 2r spec-writing follow-on** — docs-only, single-document Gate 1/2 cycle in the Phase 2j-style:

- **Deliverable:** Phase 2r spec memo at `docs/00-meta/implementation-reports/YYYY-MM-DD_phase-2r_R1b-narrow-spec-memo.md`.
- **Scope:**
  - Full spec for R1b-narrow analogous to Phase 2j §C / §D structure.
  - Exact rule shape: bias-validity predicate with single new bias-strength threshold S.
  - Exact inputs used (existing 1h slope-3 measurement; no new indicators).
  - Exact timeframes (1h bias unchanged; 15m signal unchanged).
  - Mathematical form of the predicate.
  - Boundary cases (NaN handling; warmup; tie behavior).
  - **Committed sub-parameter S** — singular, project-convention default, with documented rationale that the value is not selected by fitting.
  - Relationship to existing trigger / setup / entry / stop / R3-exit logic (all preserved).
  - What H0 rules are replaced (bias-validity predicate only).
  - What H0 rules remain unchanged (everything else).
  - Implementation impact (descriptive only — Phase 2r writes no code).
  - Expected mechanism of improvement.
  - Expected main failure mode.
  - Why R1b-narrow is structural and not parametric (Phase 2i §1.7.1 binding test).
  - GAP dispositions (R1b-narrow does not touch any GAP disposition; carries forward unchanged).
  - Candidate-specific falsifiable hypothesis (above).
  - Candidate-specific mandatory diagnostics (e.g., bias-strength distribution at filled entries; per-regime expR by bias-strength bucket).

- **Constraints:**
  - **No code, no runs, no parameter changes, no candidate-set widening, no Phase 4, no paper/shadow, no live-readiness work.**
  - R3 sub-parameters frozen as the locked exit baseline.
  - R1a sub-parameters frozen if R1a is referenced (informational only — R1a is not part of R1b-narrow).
  - Phase 2f §§ 8–11 thresholds preserved unchanged.
  - Phase 2i §1.7.3 project-level locks preserved unchanged.
  - Phase 2j §C.6 / §D.6 sub-parameter values preserved unchanged.

- **Approval gates:**
  - **Spec Gate 1** — operator approves the spec scope before any drafting begins.
  - **Spec Gate 2** — operator approves the drafted spec memo before any commit.
  - **No execution authorization.** The spec memo, even when committed, does not authorize execution. A separate execution-phase Gate 1 cycle (analogous to Phase 2k → Phase 2l) is required if and when the operator decides to advance.

- **Stop conditions for the spec phase:**
  - If the spec drift toward post-hoc threshold tuning is detected, the spec memo records the failure to clear Phase 2i §1.7 binding test; Phase 2r spec phase closes with a documented "binding-test failure" verdict; project re-defaults to Phase 2q's stay-paused recommendation.
  - If the spec is clean and the operator approves Gate 2, a separate operator-authorized execution phase (Phase 2s or later) becomes available — but is not authorized by Phase 2r.

## 8. GO / NO-GO recommendation for proceeding to Phase 2r spec-writing

| Decision                                                       | Recommendation       |
|----------------------------------------------------------------|----------------------|
| Proceed to Phase 2r spec-writing for R1b-narrow                 | **GO** (recommended) |
| Proceed to Phase 2r spec-writing for R1a-prime                  | **NO-GO**            |
| Proceed to Phase 2r spec-writing for R2                         | **NO-GO** at this time (kept alive as future candidate) |
| Remain paused (Phase 2q's stay-paused recommendation stands)    | **Operator-discretion alternative** to Path B |
| Authorize any execution phase                                    | **NO-GO** — Phase 2r is docs-only by definition |
| Authorize any operational-readiness work                         | **NO-GO** — operator deferrals stand |

**Recommended next operator action:** authorize Phase 2r spec-writing for R1b-narrow. If authorized, the next message to Claude should approve the Phase 2r spec scope (mirroring the Phase 2j Gate 1 brief structure) and the spec phase begins. If not authorized, Phase 2q's stay-paused recommendation reverts to the active default.

---

**End of Phase 2r Gate 1 planning memo.** Single-document review-only deliverable. R1b — bias-strength redesign selected as the recommended docs-only spec-writing target. R3 baseline-of-record preserved. R1a retained-for-future-hypothesis-planning preserved (R1a-prime kept alive as a future fallback candidate). H0 framework anchor preserved. R2 kept alive as a future candidate. Operator deferrals (Phase 4, paper/shadow, tiny-live, live-readiness) preserved. Stop after producing this memo.
