# Phase 2o — Targeted Asymmetry Review / Analysis Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL verdict, preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7.3 project-level locks (H0 anchor; ≤ 2 carry-forward; BTCUSDT primary); Phase 2j memo §C (R1a spec) + §D (R3 spec); Phase 2k Gate 1 plan; Phase 2l comparison report (R3 PROMOTE, designated research-leading baseline in Phase 2n); Phase 2m comparison report (R1a+R3 formal-but-mixed PROMOTE, designated promoted-but-non-leading branch in Phase 2n); Phase 2n strategy-review memo; Phase 2o operator-approved brief.

**Phase:** 2o — Targeted Asymmetry Review / Analysis (docs-only).
**Branch:** `phase-2o/asymmetry-review`.
**Memo date:** 2026-04-27 UTC.

**Status:** Recommendation produced. No new backtests, no new variants, no parameter changes, no threshold changes, no candidate-set widening, no Phase 4 / paper-shadow / live-readiness work. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## A. Executive summary

### A.1 What Phase 2o does

Phase 2o is a docs-only targeted asymmetry review. It examines the BTC/ETH asymmetry that Phase 2m surfaced — R1a (volatility-percentile setup, X = 25 / N = 200) materially helps ETH and materially hurts BTC relative to the locked R3 exit baseline — and judges whether that asymmetry points to (a) a fixable next hypothesis, (b) a symbol-specific limitation, (c) a regime-specific effect, or (d) a reason to stop further immediate execution.

It does not run new backtests. It does not re-derive any statistic that constitutes new evidence. All numbers are quoted from already-committed reports (Phase 2l comparison report; Phase 2m comparison report; Phase 2n strategy-review memo). No source-file changes, no parameter changes, no threshold changes, no candidate-set widening.

### A.2 Why analysis-only

Phase 2n's Gate 2 approval established the operator-approved framing: R3 = research-leading baseline; R1a+R3 = promoted but strategically mixed / non-leading branch; no further immediate execution is justified yet. Phase 2o is the disciplined diagnostic-deepening that should happen *before* deciding whether to authorize a third structural-redesign execution, before authorizing any operational-readiness work, or before deciding to consolidate the family at R3 alone.

Running another execution phase immediately would be premature treadmill behaviour. Pausing without diagnostic effort would leave the most-informative anomaly the project has surfaced un-examined. The disciplined middle path is one more docs-only diagnostic cycle.

### A.3 Plain-English BTC/ETH asymmetry summary

R1a's filter selects 15-minute bars whose 15m ATR(20) is in the bottom 25% of the trailing 200-bar distribution (per Phase 2j memo §C.6). The Phase 2m run confirmed the filter works exactly as designed: 100% of filled R1a entries have ATR percentile ≤ 25%. So R1a is mechanically correct.

But the *outcomes* of the trades it admits differ sharply between BTC and ETH:

- **ETH under R1a+R3** is the project's strongest result: V-window first-ever positive netPct (+0.69%, expR +0.386, PF 2.222, WR 62.5%); R-window per-regime ETH low_vol PF 1.353 (first-ever cell with positive expR AND PF > 1); ETH shorts +0.387 R / PF 1.906 (strongest direction-symbol cell ever).
- **BTC under R1a+R3** is materially worse than under R3 alone: Δexp_R3 −0.180, ΔPF_R3 −0.205 on R; V-window 4 trades / 0% WR / expR −0.990 (severely degraded out-of-sample).

The compression filter is selecting genuine bottom-quartile compression on both symbols. The follow-through after compression diverges by symbol.

This is the question Phase 2o examines.

---

## B. Fixed evidence recap

(All numbers quoted from already-committed reports. No re-derivation. No re-running.)

### B.1 R3 evidence that made it the research-leading baseline

R-window (Phase 2l comparison report; reproduced in Phase 2m as a control):

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|
| H0      | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% |
| R3      | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% |
| H0      | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% |
| R3      | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% |

R3 vs H0: BTC Δexp +0.219 / ΔPF +0.305 / Δ|dd| −1.515 pp; ETH Δexp +0.124 / ΔPF +0.153 / Δ|dd| −0.487 pp. **§10.3.a + §10.3.c clear on both symbols.** No §10.3 disqualification floor; |maxDD| ratios 0.588× BTC / 0.882× ETH (well below 1.5×).

Per-fold (5 rolling, GAP-036): R3 beats H0 in **4/5** BTC folds and **3/5** ETH folds. F2 +0.015 and F3 +0.100 are the project's first-ever positive-expR BTC folds.

V-window: H0 BTC −0.313 → R3 BTC −0.287 (improvement); H0 ETH −0.174 → R3 ETH −0.093 (improvement); WR ETH 28.57% → 42.86%.

Per-regime (realized 1h-vol, terciles 33/67): R3 improves expR in **all 6** regime-symbol cells. Implementation-bug check clean. Slippage sensitivity monotone. TRADE_PRICE bit-identical.

R3 sub-parameters (R-target = 2.0, time-stop bars = 8) anchored to existing project conventions (STAGE_5_MFE_R = 2.0; STAGNATION_BARS = 8 in `management.py`); not selected by fitting.

### B.2 R1a+R3 evidence that made it a formal but mixed PROMOTE

R-window:

| Variant  | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|----------|---------|-------:|-------:|--------:|------:|--------:|--------:|
| R1a+R3   | BTCUSDT |     22 | 27.27% |  −0.420 | 0.355 |  −2.07% |  −2.33% |
| R1a+R3   | ETHUSDT |     23 | 34.78% |  −0.114 | 0.833 |  −0.59% |  −2.96% |

H0-anchor deltas (governing): BTC Δexp **+0.039** / ΔPF **+0.100** / Δ|dd| −1.341 pp / Δn **−33.3%**; ETH Δexp **+0.362** / ΔPF **+0.512** / Δ|dd| −1.171 pp / Δn **−30.3%**.

**Formal verdict: PROMOTE.** BTC clears §10.3.c **only** (Δexp +0.039 < §10.3.a's +0.10 threshold). ETH clears §10.3.a + §10.3.c. No §10.3 disqualification floor; no §10.4 (Δn < 0); §11.4 satisfied.

R3-anchor deltas (descriptive only): BTC Δexp **−0.180** / ΔPF **−0.205**; ETH Δexp **+0.237** / ΔPF **+0.359**.

V-window: R1a+R3 ETH **first positive netPct** (8 trades / 62.5% WR / expR **+0.386** / PF **2.222** / netPct **+0.69%**). R1a+R3 BTC severely degraded (4 trades / 0% WR / expR **−0.990**).

Per-fold: R1a+R3 vs H0 — 2/5 BTC, 4/5 ETH. R1a+R3 vs R3 — 2/5 BTC, 2/5 ETH.

Per-regime: R1a+R3 ETH low_vol n=11 expR **+0.281 / PF 1.353** — first cell with positive expR AND PF > 1 ever observed. R1a+R3 BTC low_vol n=17 expR −0.329 (worse than R3's −0.054). R1a+R3 BTC high_vol n=4 expR −0.942 (worse than R3's −0.472).

Long/short asymmetry: R1a+R3 ETH shorts n=16 expR **+0.387 / PF 1.906** — strongest direction-symbol cell ever. R1a+R3 ETH longs catastrophic (n=7, expR −1.259 / PF 0). R1a+R3 BTC roughly symmetric (longs −0.363 / shorts −0.488).

R1a-specific diagnostic: **100%** of filled R1a entries at ATR percentile ≤ 25% (BTC mean 10.55%, median 9.50%; ETH mean 7.98%, median 5.00%). The predicate is admitting only bottom-quartile compression bars exactly per Phase 2j §C.5 spec.

Funnel attribution: R1a+R3's `valid_setup_windows_detected` is ~3.75× H0's (predicate admits more candidate setups; downstream trigger filtering ends with fewer entry intents). Same `rejected_no_valid_setup` bucket — funnel attribution stays interpretable.

Slippage sensitivity monotone. TRADE_PRICE bit-identical. Implementation-bug check clean (zero TRAILING_BREACH/STAGNATION leakage).

### B.3 The exact BTC-vs-ETH asymmetry (Phase 2n preserved)

Phase 2n committed:

- R3 = **research-leading baseline** (broad-based PROMOTE; project's strongest result).
- R1a+R3 = **promoted but non-leading branch** (formal PROMOTE under unchanged §10.3 with H0 anchor; strategically mixed — helps ETH, hurts BTC relative to R3).
- H0 = framework anchor only (preserved as sole §10.3 / §10.4 comparison anchor per §1.7.3).
- Wave-1 = historical evidence only.

The strategically-mixed framing is the operator-approved interpretation, reproduced verbatim from the Phase 2m Gate 2 approval. It preserves the formal PROMOTE while denying the "universal winner" framing.

### B.4 What is now known

- **R1a is mechanically correct.** 100% of filled R1a entries at percentile ≤ 25%. The selection geometry is exactly what Phase 2j §C.5 specified.
- **R1a's selection differs in volume by symbol but not in selectivity.** BTC valid_setup_windows 30,260 vs ETH 28,751 — comparable. BTC entries 22 vs ETH 23 — comparable. The downstream trigger filtering is what reduces both pools to similar sizes.
- **The post-compression follow-through differs by symbol.** This is the empirical fact that Phase 2o investigates.
- **The framework discipline holds.** Both R3 and R1a+R3 PROMOTEs were earned under unchanged thresholds with H0 as the sole anchor; no post-hoc tuning.
- **R3 alone is robust.** 4/5 BTC folds, 3/5 ETH folds beat H0; all 6 regime-symbol cells improve; V-window confirms.
- **R1a+R3 alone is asymmetric.** 2/5 BTC, 4/5 ETH vs H0; mixed regime evidence; V-window divergent.

### B.5 What is not known

- **Why** BTC compression bars under R1a's selection don't follow through with the same frequency / magnitude that ETH compression bars do.
- **Whether** a regime-conditional or symbol-conditional variant of R1a would salvage BTC.
- **Whether** the asymmetry is specific to v002 R-window data or would persist on out-of-sample V data with a larger trade pool.
- **Whether** the project's edge thesis ("breakout continuation after compression") is genuinely symbol-asymmetric or only appears asymmetric due to small samples.

These are diagnostic open questions. Phase 2o examines them via the §C diagnosis framework but does not produce decisive answers — that would require new backtests, which Phase 2o does not authorize.

---

## C. Asymmetry diagnosis framework

The operator brief enumerates six candidate explanations. Each is evaluated below on plausibility, supporting evidence, weakening evidence, and whether it points to a fixable next hypothesis.

### C.1 Symbol-specific market-behavior explanation

**Statement.** BTC and ETH have intrinsically different post-compression behaviour on the v002 R-window data; R1a's filter exposes that pre-existing difference rather than creating it.

**Plausibility.** HIGH. BTC and ETH are different markets — different liquidity profiles, different funding-rate dynamics, different correlated-asset exposure (ETH carries beta to broader L1/DeFi flows that BTC does not). Different post-compression follow-through across these two assets is an a-priori reasonable expectation; many trading-research papers document symbol-specific compression-then-expansion characteristics on similar instruments.

**Supporting evidence (committed):**
- The Phase 2g Wave-1 H-A1 result (setup window 8 → 10) showed setup-window length is not the binding parameter; trade count collapsed without recovering edge. That hint is consistent with "the issue is what happens *after* a setup, not the setup definition itself".
- R3's per-regime view shows ETH low_vol with R3 alone is already the strongest cell (−0.177 / 0.747 vs BTC's R3 low_vol −0.054 / 0.890 — actually BTC R3 low_vol is also strong, but ETH-low-vol is the cell where R1a then *amplifies* the gain to +0.281 / 1.353).
- Long/short asymmetry: under R3 alone, BTC is roughly direction-symmetric (longs −0.252 / shorts −0.230) and ETH is direction-asymmetric (longs −0.934 / shorts +0.028). R1a+R3 amplifies ETH's direction asymmetry (longs −1.259 / shorts +0.387) but does not introduce BTC asymmetry (BTC longs −0.363 / shorts −0.488 — still direction-symmetric, just both worse).
- The H0 baseline already shows BTC and ETH respond to the same strategy spec differently (H0 BTC PF 0.255 vs ETH PF 0.321; H0 BTC WR 30.3% vs ETH WR 21.2%).

**Weakening evidence (committed):**
- R3 alone produced broad-based improvement on both symbols (4/5 BTC folds, 3/5 ETH folds; all 6 regime cells improve). If symbols were intrinsically incompatible with the family, R3 alone wouldn't have worked on both.
- R1a+R3's 100% bottom-quartile percentile entry distribution is identical across symbols — the compression-selection mechanism is symbol-independent.

**Pointers to a fixable hypothesis?** PARTIAL. If the explanation is "BTC and ETH genuinely behave differently after compression", the natural next hypothesis is symbol-conditional R1a — apply R1a only on ETH. But this conflicts with Phase 2i §1.7.3 BTC-primary lock (BTCUSDT is the v1 live primary; an ETH-only filter does not deploy on the live symbol). So the hypothesis is technically generable but operationally constrained by project locks.

**Verdict on this explanation.** Plausible and partially supported. The fixable-hypothesis space it opens is constrained by §1.7.3.

### C.2 Regime-composition explanation

**Statement.** R1a's bottom-quartile filter selects regimes that are well-distributed for one symbol but skewed against the other; the asymmetry is regime-mix-driven.

**Plausibility.** MEDIUM-HIGH. The percentile filter is locally adaptive (trailing 200 bars), so by construction it always selects "the bottom 25%" — but the *kind* of bars in that bottom 25% depends on the local volatility regime. If BTC's R-window data has a regime mix that skews R1a toward bars that don't follow through, while ETH's mix skews R1a toward bars that do, the asymmetry is a regime-composition artifact.

**Supporting evidence (committed):**
- Phase 2m §6.1 per-regime expR: under R1a+R3, BTC is concentrated in `low_vol` (17/22 = **77%**) while ETH is more balanced (`low_vol` 11/23 = **48%**, `med_vol` 7/23, `high_vol` 5/23). R1a's filter is pulling more of BTC's entries into the low-vol regime — and BTC's low-vol regime under R1a+R3 has expR −0.329 (worse than R3's BTC low_vol of −0.054).
- R1a+R3 BTC high_vol (n=4) expR −0.942 — but that's a tiny sample; the more meaningful BTC degradation is in low_vol where the sample is larger.
- The Phase 2l per-regime analysis (R3 alone) had BTC's regime distribution at 13 / 7 / 13 (low / med / high). R1a's filter in Phase 2m shifts it to 17 / 1 / 4. The shift toward low_vol is dramatic on BTC; on ETH it's much more modest (12/8/13 → 11/7/5).
- Per-fold (Phase 2m §6.1): R1a+R3 BTC F2 expR −0.792 (was R3 BTC F2 +0.015 — first positive BTC fold ever, destroyed by R1a). R1a+R3 BTC F5 expR −1.320 (was R3 BTC F5 −0.448 — significantly worse). F2 corresponds to 2023H1, F5 to 2024H2 — different regime-composition periods.

**Weakening evidence (committed):**
- The percentile filter is locally adaptive *by design*; Phase 2j §C.11 explicitly justifies the design by saying "in low-volatility regimes the absolute ATR is small, so H0's `range_width ≤ 1.75 × ATR20` admits many setups; in high-volatility regimes the absolute ATR is large, so H0's predicate rejects most bars; R1a's percentile rule normalizes this." The local-adaptation is the *feature*, so any asymmetry arising from it is a feature-of-design effect, not a bug.
- The 100% in-bottom-quartile distribution is symbol-independent; R1a is functionally doing "the same thing" on both symbols.

**Pointers to a fixable hypothesis?** YES, but with strong overfitting risk. A regime-conditional R1a (apply only when 1h volatility is in a specified band, perhaps avoiding the cells where BTC degrades) would be a natural next hypothesis. But:

- It introduces additional parameters (which regimes; which bands) — multi-axis change risks Phase 2i §1.7 binding-test failure if the spec drifts toward parametric.
- Tuning the regime band on observed data without an out-of-sample hold-out is a textbook overfitting move. Phase 2i §1.7 + Phase 2f §11.3.5 would forbid post-hoc threshold setting.
- A genuinely structural regime-conditional rule (e.g., "apply R1a only when 1h vol ≤ 50th-percentile of trailing 200 1h-bars" — symmetric structural shape, single new parameter committed pre-execution) might be specifiable, but would need a falsifiable hypothesis and full Phase 2j-style spec.

**Verdict on this explanation.** Plausible and supported. The fixable-hypothesis space is real but overfitting-fraught.

### C.3 Trade-count / sample-fragility explanation

**Statement.** 22 BTC / 23 ETH trades on R, 4 BTC / 8 ETH on V; the asymmetry might be statistical noise within the small sample.

**Plausibility.** MEDIUM. Sample sizes are small. Per-fold sub-counts are smaller still (R-window BTC F3 = 2 trades; F4 = 2; F5 = 1).

**Supporting evidence (committed):**
- 22 BTC trades on R; 4 BTC trades on V. Phase 2m §10 explicitly flags the small-sample concern: "the BTC margin (Δexp +0.039 R) is approximately the noise scale".
- The framework's §10.3 thresholds (Δexp ≥ +0.10 for §10.3.a; PF +0.05 for §10.3.a) were chosen pre-Wave-1 to be informative on small samples, but they are not statistical-confidence thresholds in any formal sense.
- One-trade flips can change ETH F3 fold sign (Phase 2m: "the single ETH fold-3 regression at sample-noise scale of −0.006").
- The Phase 2m comparison report §10 already records this as a caveat.

**Weakening evidence (committed):**
- The asymmetry is consistent across multiple independent measurements: R-window expR, V-window expR, per-fold expR, per-regime expR, long/short expR, R3-anchor deltas. Six independent views all show the same direction (ETH improvement, BTC degradation). Multiple-evidence-coherence reduces the noise-only hypothesis.
- The R3 result on the same R-window with the same data (33 trades each) is broad-based and robust across all the same diagnostic cuts. If 22-23 trades were too few to be meaningful, R3's 33 would also be problematic — but R3 evidence is internally consistent. The asymmetry is unlikely to be purely sample-size-driven.
- The R1a-specific "100% percentile ≤ 25%" diagnostic is independent of sample size — the predicate's mechanical correctness does not depend on how many trades fired.

**Pointers to a fixable hypothesis?** PARTIAL. If the asymmetry is sample noise, the right response is "wait for more data" — i.e., paper/shadow on R3 alone for an extended period before deciding. But that requires the operator to lift the paper/shadow restriction, which is currently deferred. As a research-phase fixable hypothesis, sample-size explanations point to "extend the data window" or "synthetic-bootstrap analysis on existing trades", neither of which is in scope for Phase 2o.

**Verdict on this explanation.** Plausible but only partially supported. Multiple-evidence-coherence weakens the pure-noise reading. The asymmetry is probably real; the magnitude estimate is fragile.

### C.4 Setup-selection-shape explanation

**Statement.** R1a's percentile predicate has a different selection geometry from H0's range-based predicate; the asymmetry is a selection-bias artifact of the new predicate's shape.

**Plausibility.** MEDIUM. Percentile-based selection has known properties: it is locally adaptive (responds to recent regime), it ranks rather than thresholds, and it tends to amplify whatever the underlying distribution's structural skew is.

**Supporting evidence (committed):**
- R1a admits ~3.75× more candidate setups than H0 (BTC valid_setup_windows 30,260 vs H0's 8,064). The candidate pool is much larger; the downstream trigger filtering is what reduces it. This means R1a is a much wider gate at the predicate stage; the asymmetric impact comes from how the wider gate interacts with downstream filters.
- ETH H0 funnel: 84,731 rejected_no_valid_setup → 47 entry intents. ETH R1a+R3: 63,817 rejected_no_valid_setup → 31 entry intents. Even though R1a admits more setups, the entry-intent count drops. The downstream filtering (close-broke-level, TR, close-location, ATR-regime, stop-distance) removes more candidates from R1a's pool than from H0's. **R1a's pool composition is different — and the downstream filters affect it differently.**
- BTC: same pattern. H0 BTC: 85,480 → 41 entries. R1a BTC: 63,284 → 27 entries. Same magnitude of pool widening (~3.75×) and same magnitude of trade-count reduction (33 → 22).

**Weakening evidence (committed):**
- The percentile predicate is symbol-independent. Both symbols see the same selection geometry. If the geometry alone were responsible, both would respond the same way.
- The 100% in-bottom-quartile diagnostic confirms R1a is selecting compression as designed; the "selection bias" framing would have to be at a more subtle level (e.g., selection bias *within* the bottom quartile that differs by symbol).

**Pointers to a fixable hypothesis?** PARTIAL. A different setup-side rule shape (e.g., volatility-contraction-by-time, structural-pattern-based) might have different selection geometry and avoid R1a's BTC penalty. But the hypothesis space is wide and unfocused without more analysis. Phase 2i originally excluded R1b (regime classifier) and R2 (pullback entry) for separate reasons; reviving either of those is a separate operator decision.

**Verdict on this explanation.** Plausible at the second-order level (selection-bias *within* bottom-quartile differs by symbol). Direct evidence is thin; would need new analysis to support.

### C.5 Directional-bias interaction explanation

**Statement.** The breakout-on-bias entry rule interacts with R1a's compression filter differently across symbols. The strongest evidence: R1a+R3 ETH shorts +0.387 / PF 1.906 (best direction-symbol cell ever); R1a+R3 ETH longs −1.259 / PF 0 (catastrophic). BTC is roughly direction-symmetric (longs −0.363 / shorts −0.488).

**Plausibility.** HIGH. The breakout strategy enters in the direction of the 1h bias. The R-window had a regime mix where ETH spent more time in bearish bias regimes (consistent with the broader 2022-2024 ETH price action that included multiple sustained downtrends); ETH shorts under those conditions had genuine post-compression downside follow-through. ETH longs in the same window had less follow-through (the bullish-bias regimes were shorter / less directional). R1a's filter selects compression bars in both directions; the directional asymmetry of the underlying regime then translates to the directional asymmetry of trade outcomes.

**Supporting evidence (committed):**
- Phase 2m §7.3 long/short asymmetry: R1a+R3 ETH shorts n=16 expR +0.387 / PF 1.906; ETH longs n=7 expR −1.259 / PF 0. The cells are concentrated: 16 shorts vs 7 longs (more than 2:1 short bias under R1a+R3 ETH; H0 was 13/20 long/short, so R1a is amplifying the short bias).
- R3 alone ETH shorts +0.028 / PF 1.07 — already directionally positive on R3 (the first-ever positive direction-symbol cell, in Phase 2l). R1a+R3 amplifies this signal substantially (+0.359 PF on top of R3's already-positive ETH-shorts).
- R3 alone BTC: longs −0.252 / shorts −0.230 — direction-symmetric. R1a+R3 BTC: longs −0.363 / shorts −0.488 — still direction-symmetric, just both worse.

**Weakening evidence (committed):**
- The direction-asymmetry on ETH was already present under R3 alone (longs −0.934 / shorts +0.028 in Phase 2l). R1a amplifies it but doesn't create it. So the directional-bias interaction is more about ETH's underlying directional regime than about R1a specifically.
- The BTC direction-symmetry under R3 means R1a's compression filter, if applied symmetrically, should produce direction-symmetric effects on BTC too — and it does (longs −0.363 / shorts −0.488 are close). The asymmetry is *between symbols*, not *between directions within BTC*.

**Pointers to a fixable hypothesis?** PARTIAL. If the explanation is "R1a is amplifying a pre-existing ETH directional regime", then:

- A direction-conditional R1a (apply only on bearish bias) would be operationally meaningful only if §1.7.3 is relaxed to admit symbol-aware research deployment.
- A symbol-conditional R1a (apply only on ETH) similarly conflicts with §1.7.3.
- An ETH-research-only paper/shadow study (extended observation of R1a+R3's ETH performance in real time) would be the natural next operational step — but paper/shadow planning is currently deferred per operator policy.

**Verdict on this explanation.** Plausible and well-supported by the cross-symbol direction view. Points to an ETH-favorable specialty effect more than a fixable BTC remediation.

### C.6 Family-limitation explanation

**Statement.** The breakout family is approaching its useful-edge ceiling on the v002 R-window data; R1a's asymmetry is a sign that further structural redesign inside the family won't move the needle.

**Plausibility.** MEDIUM. Two of three structural-redesign experiments have PROMOTED. R3 was broad and clean; R1a+R3 was asymmetric and mixed. The marginal improvement R1a contributes on top of R3 is small in expR magnitude even on ETH (Δexp_R3 +0.237 R; expR remains negative −0.114 R on R; +0.386 R on V from a tiny 8-trade sample). The absolute aggregate edge has not materialized at any point in the family's research history.

**Supporting evidence (committed):**
- Even R3's R-window expR is −0.240 / −0.351 — still negative on aggregate.
- Even R1a+R3's strongest cells (ETH low_vol +0.281, ETH shorts +0.387, ETH V +0.386) have small samples (n = 11, 16, 8 respectively).
- Wave-1's REJECT ALL eliminated four parametric paths.
- The Phase 2h decision memo §11.1 stopping rule (paraphrased: "abandon a family only when structural redesign has been honestly tried with a falsifiable hypothesis and produced its own clean negative") has not been met yet — neither R3 nor R1a+R3 produced a clean negative — but the clean *positive* aggregate has also not materialized.

**Weakening evidence (committed):**
- R3 produced first-ever positive BTC fold expR (F2, F3) and improved all 6 regime-symbol cells. The family is *responding* to structural work, not flatlining.
- R1a+R3 ETH V-window first positive netPct (+0.69%) is unprecedented — the family has never produced an out-of-sample positive equity result before. This is genuine new evidence, not noise.
- The Phase 2i deferred candidates (R1b regime-conditional bias, R2 pullback entry) have not been tested. Calling the family at-ceiling without testing them is premature.

**Pointers to a fixable hypothesis?** NEGATIVE. If the explanation is "family at ceiling", the implication is to stop pushing — not to chase a fix. The "fix" is to consolidate at R3 and either accept the family's level or shift to a different family. Both are operator-policy decisions outside Phase 2o's scope.

**Verdict on this explanation.** Plausible but premature. Two PROMOTEs is not "ceiling" evidence. The explanation should stay alive as a future cross-check after one more honest structural attempt fails (or after operator independently decides to stop).

### C.7 Summary of explanations

| # | Explanation                                          | Plausibility | Supporting strength | Points to fixable hypothesis? |
|---|------------------------------------------------------|--------------|---------------------|--------------------------------|
| 1 | Symbol-specific market behavior                       | HIGH         | MEDIUM-HIGH         | PARTIAL (constrained by §1.7.3) |
| 2 | Regime-composition                                    | MEDIUM-HIGH  | MEDIUM-HIGH         | YES, but high overfitting risk  |
| 3 | Trade-count / sample fragility                        | MEDIUM       | LOW                 | PARTIAL (longer observation)    |
| 4 | Setup-selection shape                                  | MEDIUM       | LOW (needs new analysis) | PARTIAL (different setup-side)  |
| 5 | Directional-bias interaction                          | HIGH         | HIGH (multi-evidence) | PARTIAL (ETH-favorable framing) |
| 6 | Family-limitation                                      | MEDIUM       | MEDIUM (premature)  | NEGATIVE (stop, don't fix)      |

**The most-supported explanations are #1 (symbol-specific market behavior) and #5 (directional-bias interaction).** Both converge on the same operational implication: R1a is acting like an ETH-favorable specialty filter, picking up structural directional signal that exists on ETH and is muted on BTC. **Explanation #2 (regime-composition) is the most fixable in principle, but the most overfitting-fraught in practice.**

---

## D. BTC-vs-ETH evidence synthesis

### D.1 R-window differences

| Measure                       | BTC                                          | ETH                                          | Asymmetry direction        |
|-------------------------------|----------------------------------------------|----------------------------------------------|----------------------------|
| Trades                        | 22 (vs H0 33; vs R3 33)                      | 23 (vs H0 33; vs R3 33)                      | symmetric (both ↓ ~30%)     |
| WR                            | 27.27% (H0 30.30%, R3 42.42%)                | 34.78% (H0 21.21%, R3 33.33%)                | ETH ↑ vs both anchors; BTC ↓ vs R3 |
| expR                          | −0.420 (vs H0 −0.459 / R3 −0.240)            | −0.114 (vs H0 −0.475 / R3 −0.351)            | ETH ↑ vs both; BTC ↑ vs H0 (small) / ↓ vs R3 |
| PF                            | 0.355 (vs H0 0.255 / R3 0.560)               | 0.833 (vs H0 0.321 / R3 0.474)               | same pattern                |
| netPct                        | −2.07% (vs H0 −3.39% / R3 −1.77%)            | −0.59% (vs H0 −3.53% / R3 −2.61%)            | ETH dramatically ↑; BTC slightly ↓ vs R3 |
| maxDD                         | −2.33% (vs H0 −3.67% / R3 −2.16%)            | −2.96% (vs H0 −4.13% / R3 −3.65%)            | ETH ↑ vs both; BTC ↑ vs H0 / ≈ R3 |

### D.2 V-window differences

| Measure                       | BTC                                          | ETH                                          | Asymmetry direction        |
|-------------------------------|----------------------------------------------|----------------------------------------------|----------------------------|
| Trades                        | 4 (vs H0 8 / R3 8)                            | 8 (vs H0 14 / R3 14)                          | both ↓ ~50%                 |
| WR                            | **0.00%** (vs H0 25%, R3 25%)                 | **62.50%** (vs H0 28.57%, R3 42.86%)          | extreme divergence          |
| expR                          | **−0.990** (vs H0 −0.313 / R3 −0.287)         | **+0.386** (vs H0 −0.174 / R3 −0.093)         | **opposite signs**          |
| PF                            | **0.000** (vs H0 0.541 / R3 0.580)            | **2.222** (vs H0 0.695 / R3 0.824)            | extreme divergence          |
| netPct                        | **−0.88%** (vs H0 −0.56% / R3 −0.51%)         | **+0.69%** (vs H0 −0.55% / R3 −0.29%)         | **opposite signs**          |

V-window amplifies the asymmetry. ETH V-window is the project's first positive-netPct out-of-sample result; BTC V-window is the project's worst V cell ever. Sample sizes are small (n = 4 BTC; n = 8 ETH) so the magnitude estimates are fragile, but the direction is unambiguous.

### D.3 Per-fold differences

R1a+R3 vs H0 per-fold expR delta:

| Fold     | BTC Δexp                        | ETH Δexp                        |
|----------|---------------------------------|---------------------------------|
| F1 2022H2| −0.347                          | +0.138                          |
| F2 2023H1| −0.554 (worst BTC fold)         | −0.680                          |
| F3 2023H2| **+1.215** (best BTC fold)       | +0.126                          |
| F4 2024H1| **+0.789**                       | +0.519                          |
| F5 2024H2| −0.627                          | +0.017 (tie)                     |

R1a+R3 vs R3 per-fold expR delta:

| Fold     | BTC Δexp                        | ETH Δexp                        |
|----------|---------------------------------|---------------------------------|
| F1 2022H2| −0.347                          | −0.094                          |
| F2 2023H1| **−0.807** (R3 destroyed)        | **−0.972**                       |
| F3 2023H2| +0.592                          | +0.133                          |
| F4 2024H1| +0.634                          | +0.519                          |
| F5 2024H2| −0.873                          | −0.214                          |

Both anchors show R1a+R3 strongest at F3-F4 (mid-2023 → 2024H1) and weakest at F2 (2023H1) and F5 (2024H2). **The F2 BTC degradation is the most material**: R3's first positive BTC fold (F2 +0.015) is replaced with R1a+R3 −0.792. Whatever R1a is doing on BTC F2, it is undoing the structural improvement R3 delivered.

### D.4 Per-regime differences (realized 1h-vol; trailing 1000 1h-bar window; terciles)

| Regime    | Variant | BTC expR / PF / WR        | ETH expR / PF / WR        |
|-----------|---------|---------------------------|---------------------------|
| low_vol   | H0      | −0.372 / 0.377 / 30.77%   | −0.184 / 0.729 / 33.33%   |
| low_vol   | R3      | −0.054 / 0.890 / 38.46%   | −0.177 / 0.747 / 41.67%   |
| low_vol   | R1a+R3  | **−0.329** / 0.460 / 23.53% | **+0.281** / **1.353** / 36.36% |
| med_vol   | H0      | −0.195 / 0.571 / 57.14%   | −0.970 / 0.000 / 0.00%    |
| med_vol   | R3      | −0.157 / 0.656 / 57.14%   | −0.766 / 0.103 / 25.00%   |
| med_vol   | R1a+R3  | +0.120 / inf / 100% (n=1) | −0.665 / 0.127 / 28.57%   |
| high_vol  | H0      | −0.688 / 0.047 / 15.38%   | −0.439 / 0.204 / 23.08%   |
| high_vol  | R3      | −0.472 / 0.278 / 38.46%   | −0.257 / 0.509 / 30.77%   |
| high_vol  | R1a+R3  | **−0.942** / 0.051 / 25.00% | −0.209 / 0.331 / 40.00%   |

**Where R1a hurts BTC vs R3:** low_vol (Δ −0.275) and high_vol (Δ −0.470). The low_vol degradation is the larger sample (17 trades vs R3's 13) and the more material effect. **Where R1a helps ETH vs R3:** low_vol (Δ +0.458) — and that's the cell that drives the V-window first-ever positive netPct.

The asymmetry is **regime-localized**: R1a does well on ETH-low-vol; R1a does poorly on BTC-low-vol. The other regimes are smaller-sample and noisier.

### D.5 Long/short asymmetry differences

| Variant | BTC L/S expR / PF                          | ETH L/S expR / PF                          |
|---------|-------------------------------------------|-------------------------------------------|
| H0      | longs 16: −0.560 / 0.216  shorts 17: −0.364 / 0.305 | longs 13: −1.005 / 0.067  shorts 20: −0.131 / 0.712 |
| R3      | longs 16: −0.252 / 0.578  shorts 17: −0.230 / 0.540 | longs 13: −0.934 / 0.133  shorts 20: +0.028 / 1.070 |
| R1a+R3  | longs 12: −0.363 / 0.430  shorts 10: −0.488 / 0.269 | longs 7: −1.259 / 0.000  shorts 16: **+0.387** / **1.906** |

**R1a+R3 ETH shorts is the strongest direction-symbol cell ever observed** in the project. Sixteen trades, +0.387 R expectancy, profit factor **1.906**. The signal is concentrated on the short side — ETH longs under R1a+R3 are catastrophic. **BTC under R1a+R3 has no comparable directional signal** — both sides are weakly negative.

### D.6 Trade-frequency and funnel differences

| Variant | Symbol  | valid_setup_windows | rejected_no_valid_setup | entry_intents | trades_filled | trades_closed | warmup_15m_excluded |
|---------|---------|--------------------:|------------------------:|--------------:|--------------:|--------------:|--------------------:|
| H0      | BTCUSDT |               8,064 |                  85,480 |            41 |            41 |            41 |                  29 |
| H0      | ETHUSDT |               7,837 |                  84,731 |            47 |            47 |            47 |                  29 |
| R3      | BTCUSDT |               8,064 |                  85,480 |            41 |            41 |            41 |                  29 |
| R3      | ETHUSDT |               7,837 |                  84,731 |            47 |            47 |            47 |                  29 |
| R1a+R3  | BTCUSDT |              30,260 |                  63,284 |            27 |            27 |            27 |                 220 |
| R1a+R3  | ETHUSDT |              28,751 |                  63,817 |            31 |            31 |            31 |                 220 |

R1a's predicate produces ~3.75× the valid-setup count of H0's predicate. The downstream trigger filtering then cuts more aggressively. End-result: 27 BTC entry intents (vs H0's 41) and 31 ETH entry intents (vs H0's 47). **The end-trade pool is approximately the same shape across symbols** (27 vs 31 entry intents — comparable). The asymmetry is not in the funnel volume but in the *outcomes* of the trades that pass.

The warmup-floor lift from 29 to 220 (R1a's lookback warmup: 200 bars + ATR seed 21 = 221) is symmetric across symbols.

### D.7 Synthesis

The BTC/ETH asymmetry under R1a+R3 is **multi-faceted and converges on a coherent picture**:

- R1a's compression filter is **mechanically correct on both symbols** (100% percentile ≤ 25%; 3.75× pool widening matched across symbols).
- The trade pool that survives the downstream trigger is **comparable in size** across symbols (27 vs 31 entry intents).
- The **outcomes** of those trades diverge: ETH outcomes improve substantially, BTC outcomes degrade modestly. The divergence is concentrated in the low-vol regime (ETH +0.458 vs R3; BTC −0.275 vs R3) and in the directional split (ETH shorts +0.387 PF 1.906; BTC roughly direction-symmetric and weakly negative).
- **V-window amplifies the asymmetry**. ETH first-ever positive netPct; BTC severe degradation.
- **The asymmetry is consistent across multiple independent measurements** (R-window expR, V-window expR, per-fold expR, per-regime expR, long/short expR, R3-anchor deltas) — six independent views, same direction.

The most parsimonious interpretation: **R1a's compression filter is interacting with a pre-existing ETH-favorable directional regime in the v002 R-window data; on BTC the same filter selects bars that don't have the same post-compression directional follow-through.** This is consistent with explanations C.1 (symbol-specific) and C.5 (directional-bias) being the dominant drivers; C.2 (regime-composition) is a secondary contributing factor; C.3 (sample fragility) and C.4 (selection-shape) are weak; C.6 (family-limitation) is premature.

---

## E. Interpretation of the R1a mechanism

### E.1 Is R1a correctly implemented?

**Yes.** The Phase 2m R1a-specific diagnostic confirmed:

- 100% of filled R1a entries have ATR percentile ≤ 25% (BTC mean 10.55%, median 9.50%; ETH mean 7.98%, median 5.00%).
- The funnel attribution stays in the existing `rejected_no_valid_setup` bucket — no leakage to the wrong bucket.
- The implementation-bug check is clean: zero TRAILING_BREACH and zero STAGNATION exits on either symbol (R3's exit logic is preserved bit-for-bit; R1a does not touch exits).
- H0 and R3 controls reproduce Phase 2l baselines bit-for-bit (the new optional fields and dispatch logic do not silently regress prior behaviour).
- 13 unit tests (Phase 2m commit 1) enforce the predicate invariants.

R1a's mechanical correctness is not in doubt.

### E.2 Is R1a actually selecting genuine compression?

**Yes, by definition.** R1a's percentile-based predicate selects 15m bars whose 15m ATR(20) is in the bottom 25% of the trailing 200-bar distribution. By construction, those bars are in a locally-low-volatility regime — that is the textbook definition of "compression". The 100% in-bottom-quartile observed result confirms the predicate is doing exactly what it claims.

The deeper question is whether "compression" *as defined this way* corresponds to the kind of compression that historically precedes breakouts. Phase 2j memo §C.11 anticipated this: "The percentile-based predicate is regime-aware: it ranks the current ATR against the recent distribution rather than against an absolute threshold." But the v002 R-window evidence shows the percentile-defined compression does not consistently precede follow-through breakouts on BTC — even though it does on ETH.

So R1a is selecting "compression" by a defensible definition, but "compression" by that definition does not always predict breakout follow-through.

### E.3 Whose problem is it — the compression concept itself, or how BTC responds after compression?

This is the core diagnostic question. The evidence:

- The compression predicate is symbol-agnostic.
- The selection volume is comparable across symbols.
- The downstream outcome diverges sharply.

This points to **post-compression follow-through being the asymmetric variable**, not the compression definition itself. The compression filter is doing a fine job of identifying compression on both symbols; what differs is what each symbol does after compression.

This is consistent with the symbol-specific market-behaviour explanation (C.1) and the directional-bias interaction explanation (C.5). Both say: the asymmetry is in the markets, not in R1a.

### E.4 What does R1a look like, in framing terms?

Three candidate framings:

| Framing                          | Compatible with evidence?                                              | Compatible with project locks (§1.7.3)?           |
|----------------------------------|----------------------------------------------------------------------|---------------------------------------------------|
| ETH-favorable specialty filter   | YES — ETH R-window, V-window, regime, direction all support           | NO at v1 live (one-symbol live; ETH research only) — but valid as research finding |
| Regime-dependent filter          | YES — low_vol cells dominate the asymmetry direction                  | YES if specified pre-execution as a structural rule with no post-hoc tuning |
| Unstable filter that should not be extended | PARTIAL — V-window BTC at 4 trades / 0% WR is suggestive but small-sample | YES — points to consolidation at R3 alone         |

**Recommended framing:** R1a is best characterized as **an ETH-favorable specialty filter with a regime-localized signal**. It is not "unstable" in the implementation sense — it works exactly as designed — but it is unstable in the deployment sense — its outcomes depend on which symbol it is applied to, and on which regime the symbol is in.

This framing aligns with Phase 2n's "promoted but non-leading branch" framing. R1a stays alive as a research artifact (it has produced unique evidence that the project did not have before — first positive-netPct V-window). It does not become a deployable v1 candidate (the §1.7.3 locks make it ineligible).

---

## F. Fixability analysis

The operator brief enumerates four future-direction hypotheses to evaluate **as hypotheses, not as execution approvals**.

### F.1 Regime-conditional R1a application

**Statement.** Apply R1a's percentile filter only in specified regimes. Possible specifications: (a) only when 1h volatility is in the bottom 33% of trailing 1000 1h-bars; (b) only when 1h ATR(20) is below a fixed threshold normalized by close; (c) only when bar close is within a defined range of EMA(50) (proxy for trend strength).

**Potential upside.** If the asymmetry is regime-localized (per §D.4), a regime-conditional version might capture the ETH-low-vol benefit without the BTC-low-vol penalty. The Phase 2m §6.1 evidence shows R1a's biggest BTC degradation is in low_vol (where its biggest ETH improvement also is) — so a regime-conditional rule that activates R1a *only when 1h vol is high* would invert the regime-mix and might salvage BTC. But that would also discard ETH's strongest cell.

**Overfitting risk.** **HIGH.** Regime-conditional rules introduce additional parameters (which regime; which threshold; which window). Tuning those parameters on observed data without an out-of-sample hold-out is exactly what Phase 2f §11.3.5 forbids.

**Policy / project-lock conflict risk.** MEDIUM. A genuinely structural regime-conditional rule (single new parameter committed pre-execution; falsifiable hypothesis; full Phase 2j-style spec) is technically eligible under Phase 2i §1.7.1 binding test. But the operator framework would need to be confident that the regime-condition is rule-shape change, not parameter-tuning under another label.

**Expected value of information.** MEDIUM. If a clean regime-conditional spec can be pre-committed before any new run, the EVI is real. If the spec drifts toward post-hoc tuning, EVI collapses.

**Should it stay alive?** YES, but only as a hypothesis to be carefully specified in a future docs-only planning phase before any execution. **Not** approved for execution by Phase 2o.

### F.2 Symbol-conditional use of R1a (apply only on ETH)

**Statement.** Use R1a only on ETH; leave BTC under R3 alone.

**Potential upside.** Captures the full ETH benefit (V-window +0.69%, ETH-shorts PF 1.906) while preserving R3's broad-based BTC behaviour. Mechanically clean.

**Overfitting risk.** LOW at the rule level (no new parameters), but conceptually the choice is post-hoc data-driven (we know R1a hurts BTC and helps ETH only because we ran the Phase 2m experiment).

**Policy / project-lock conflict risk.** **HIGH.** Phase 2i §1.7.3 establishes BTCUSDT as the v1 live primary with ETHUSDT as research/comparison only. A symbol-conditional rule that applies different setup logic to BTC and ETH:

- Implicitly elevates ETH from research-only to research-with-distinct-rules — a partial relaxation of §1.7.3.
- Creates two different strategies in one runtime, doubling the operational complexity.
- Conflicts with the v1 spec's "one symbol live, one position max" simplicity goal.

**Expected value of information.** LOW within v1's BTC-primary policy. If the operator independently relaxes §1.7.3 to admit symbol-aware research deployment, EVI rises substantially. Without that policy change, this option is dominated by Option F.3 (R1a abandonment).

**Should it stay alive?** **NO** at v1, by §1.7.3. Stays alive only as a future possibility contingent on operator policy change.

### F.3 R1a abandonment while keeping R3

**Statement.** Drop R1a entirely; treat R3 alone as the locked baseline for any future structural-redesign work or operational-readiness planning.

**Potential upside.** Aligns with R3's broad-based PROMOTE evidence. Avoids the BTC degradation R1a introduces. Preserves R3 as a clean, well-characterized candidate. Simplifies the strategy spec going forward (one structural redesign instead of two).

**Overfitting risk.** ZERO. Abandoning a candidate is the opposite of overfitting.

**Policy / project-lock conflict risk.** ZERO. R3 alone is fully consistent with §1.7.3 and the entire Phase 2j discipline.

**Expected value of information.** **HIGH** — for clarity. Consolidating at R3 alone eliminates the strategically-mixed framing and makes the next research / operational decision cleaner.

**Should it stay alive?** YES. This is the strongest fixability option in terms of clarity and discipline. Does NOT mean R1a's evidence is discarded — the Phase 2m research artifacts remain on disk and the comparison report is committed history. R1a as a *deployable variant* is dropped; R1a as *research evidence* remains.

### F.4 A different setup-side redesign altogether

**Statement.** Abandon R1a's percentile-based shape; consider a different setup-validity rule shape (e.g., volatility-contraction-by-time, structural-pattern-based, Bollinger-band-squeeze, breakout-retest pattern).

**Potential upside.** A different rule shape might capture compression-precedes-breakout structure differently and avoid the BTC asymmetry R1a produces. Phase 2i §3.2 originally surveyed several alternatives; only R1a was selected for execution.

**Overfitting risk.** MEDIUM. A new rule shape needs its own falsifiable hypothesis, single-axis structural change, sub-parameters committed singularly per Phase 2j-style discipline. Phase 2i §1.7 binding test must be satisfied.

**Policy / project-lock conflict risk.** LOW if specified properly within the existing framework.

**Expected value of information.** LOW-MEDIUM. The hypothesis space is wide and unfocused; without a specific proposed rule shape grounded in concrete evidence about why it would behave differently from R1a, EVI is speculative. Phase 2i originally chose R1a precisely because it was the highest-EVI Family-S candidate at that time.

**Should it stay alive?** PARTIAL. As a docs-only future-planning option, yes — but only after a more focused diagnostic surfaces a specific rule shape worth proposing. The current evidence does not point to any one alternative as obviously higher-EVI than R1a was.

### F.5 Fixability summary

| Option | Description                                  | Upside       | Overfitting risk | Policy conflict | EVI            | Stay alive? |
|--------|----------------------------------------------|--------------|------------------|-----------------|----------------|-------------|
| F.1    | Regime-conditional R1a application            | MEDIUM       | HIGH             | MEDIUM          | MEDIUM         | YES (planning-only) |
| F.2    | Symbol-conditional use of R1a (ETH-only)      | HIGH on ETH  | LOW (rule)       | HIGH (§1.7.3)   | LOW within v1  | NO at v1    |
| F.3    | R1a abandonment while keeping R3              | HIGH (clarity) | ZERO            | ZERO             | HIGH (clarity) | YES         |
| F.4    | Different setup-side redesign altogether      | UNFOCUSED    | MEDIUM           | LOW             | LOW-MEDIUM     | PARTIAL     |

**The disciplined reading:** F.3 is the cleanest immediate path; F.1 is the highest-EVI execution path **if** specified properly; F.4 is an open future option contingent on more diagnostic work; F.2 is unavailable at v1.

---

## G. Family-level implication

### G.1 What does this asymmetry imply about the breakout family?

The asymmetry implies that **the breakout-continuation-after-compression thesis has a real but symbol-asymmetric edge structure on the v002 R-window data**. The thesis is not falsified — R3 alone clears the framework on both symbols, and R1a+R3 finds genuine ETH-side edge that R3 alone does not. But the thesis is also not universal — R1a's compression filter does not improve BTC outcomes when added to R3.

The most coherent reading: the family has **modest broad-based edge under R3 alone** and **stronger but symbol-localized edge under R1a+R3 on ETH**. The family does not have a **strong universal edge** that lifts both symbols toward live-readiness.

### G.2 Does the asymmetry increase confidence in R3?

**YES.** The fact that R3 alone produces broad-based improvement on both symbols across all 6 regime cells, all 5 folds (mostly), and out-of-sample on V — and that R1a's setup-side change does not universally improve on R3 — increases confidence that R3's exit-philosophy improvement is the genuine, structural source of edge in this family. R3 is not contingent on a particular symbol-regime alignment; it works on the structure of the strategy itself.

R3 should be treated as **the most-validated structural improvement the project has produced**.

### G.3 Does the asymmetry reduce confidence in setup-side redesigns generally, or only in this specific R1a form?

**Only in this specific R1a form.** The Phase 2j memo §C originally identified R1a as one of several Family-S candidates. R1a was chosen for execution because it had the best evidence-grounded case at that time. The asymmetry observed in Phase 2m is specific to R1a's percentile-based shape; it does not generalize to "all setup-side redesigns are doomed".

A different setup-side rule shape (per Option F.4) might behave very differently. But the asymmetry is also a warning: **setup-side redesigns are sensitive to symbol-specific market structure** in a way that exit-side redesigns (R3) are not. Future setup-side proposals should be scrutinized for symbol-asymmetric implications before execution.

### G.4 Does this suggest one more redesign cycle later, or that execution should pause longer?

**Pause longer.** Two arguments:

1. **The most-supported explanations (C.1 symbol-specific, C.5 directional-bias) point to facts about the underlying markets, not to fixable rule-shape issues.** Running another structural-redesign execution to "fix" something that may not be fixable risks treadmill behaviour with diminishing returns.
2. **R3 alone is already the strongest result the project has produced.** Operating on R3 (in extended observation, paper/shadow if eventually authorized, or ongoing research) generates more value than rushing to R1b / R2 / R1a-prime execution without first determining whether the asymmetry has changed the operator's view of the family.

The longer pause does NOT mean "stop forever". It means: **next research cycle is a planning cycle, not an execution cycle.** Either (a) Phase 2p is another docs-only planning phase (regime-conditional R1a hypothesis development; or the Phase 2i-deferred R1b / R2 spec review), or (b) the operator chooses to pause strategy work entirely while operational-infrastructure gates are reviewed.

---

## H. Recommendation

This recommendation is **provisional and evidence-based, not definitive**. The operator decides.

### H.1 Primary recommendation

**Phase 2o effectively closes the question of further structural-redesign execution for now.** R3 remains the research-leading baseline. R1a stays alive as a research branch (the Phase 2m artifacts on disk and the committed comparison report are not invalidated). No further immediate execution phase is justified.

The recommended next step is **Phase 2p — pause strategy execution; operate on R3 evidence; defer further redesign work** (per the Phase 2p Option A described in §J below). Phase 2p itself is docs-only / minimal: a brief operator-strategy review consolidating the R3 baseline, deferring further redesign work, and (critically) NOT yet starting paper/shadow-readiness planning, NOT yet starting Phase 4, and NOT yet starting any new strategy family.

**Concretely:**

- **R3** is the research-leading baseline and remains the locked exit-philosophy baseline for any future structural-redesign work. Sub-parameters R-target = 2.0 / time-stop = 8 frozen.
- **R1a** stays alive as a promoted-but-non-leading research branch. The Phase 2m comparison report is preserved as committed evidence. R1a's sub-parameters X = 25 / N = 200 frozen. The Phase 2j §C spec is preserved.
- **No future execution phase** is justified at this time. If the operator independently develops a high-EVI hypothesis (regime-conditional R1a-prime; or Phase 2i-deferred R1b / R2 with newer evidence-grounding), that hypothesis must clear its own Gate 1 before any execution.
- **Phase 4 stays deferred** per operator policy.
- **Paper/shadow-readiness planning stays deferred** per operator policy.
- **Live-readiness claims** stay forbidden.

### H.2 Fallback recommendation

If the operator judges that one more docs-only planning cycle is worth doing — specifically to develop a falsifiable regime-conditional R1a-prime spec (per Option F.1) — then **Phase 2p Option B** (docs-only hypothesis-planning for one specific next redesign) becomes the path. This is not an execution phase; it's a Phase 2j-style spec-writing phase that produces a falsifiable hypothesis with pre-committed sub-parameters before any future Gate 1 / Gate 2 / execution cycle.

Phase 2p Option B's value is that it forces the operator and Claude to decide whether a regime-conditional R1a-prime can be specified cleanly enough to satisfy Phase 2i §1.7 binding test. If yes, a future execution phase becomes available. If no (the spec drifts toward post-hoc tuning), the operator has a documented reason to consolidate at R3.

### H.3 Explicit answers to the operator's required questions

- **Whether R3 remains the research-leading baseline:** YES. R3's Phase 2l PROMOTE evidence is the strongest result the project has produced; the Phase 2o asymmetry analysis increases confidence in R3.
- **Whether R1a should stay alive as a research branch:** YES. R1a's Phase 2m PROMOTE is formal and the ETH evidence is genuinely informative (first positive-netPct V-window). R1a's deployable status is constrained by §1.7.3, but the research value is preserved.
- **Whether a future execution phase is justified at all:** NOT IMMEDIATELY. If a high-EVI hypothesis (regime-conditional R1a-prime, R1b, or R2) can be specified cleanly via a future Phase 2j-style spec-writing phase, then a future Gate 1 / Gate 2 / execution cycle becomes available. Phase 2o does not authorize execution; the next phase should be docs-only.
- **Whether Phase 2o should effectively close the question for now:** YES. Phase 2o's recommendation is consolidation at R3 with R1a preserved as research-only. The asymmetry is most likely a fact about market structure, not a fixable rule issue. Closing the question for now means: the operator has the diagnostic evidence to make a clear next-direction decision; that decision can be "pause and operate on R3 evidence" or "one more spec-writing cycle for R1a-prime".

### H.4 What the recommendation explicitly does NOT recommend

- **Symbol-conditional R1a (Option F.2):** unavailable at v1 by §1.7.3.
- **Different setup-side redesign (Option F.4) as immediate execution:** hypothesis-space is unfocused; needs more diagnostic work first.
- **Paper/shadow planning for R3 (operator brief Option D) or R1a+R3 (operator brief Option E):** deferred per operator policy.
- **New strategy-family research planning (operator brief Option F):** premature; family has produced two PROMOTEs and one of them is ETH-positive on V.
- **Phase 4 work:** deferred per operator policy.

---

## I. What would change this recommendation

The recommendation is **provisional**. The following kinds of evidence or operator-policy decisions would justify switching paths:

### I.1 Switch from "consolidate at R3" to "execute another structural redesign"

- Operator independently develops a falsifiable regime-conditional R1a-prime spec (via Phase 2p Option B docs-only planning) that satisfies Phase 2i §1.7 binding test (genuine rule-shape change, single-axis, sub-parameters committed singularly, no post-hoc tuning).
- Operator independently revives the Phase 2i-deferred R1b (regime-conditional bias) or R2 (pullback entry) candidates with evidence-grounded justification for testing them now.
- Operator's reading of the asymmetry analysis is that one more execution cycle is worth the framework-discipline investment.

### I.2 Switch from "R1a stays alive" to "R1a abandoned permanently"

- A future execution attempt produces additional evidence that R1a's BTC degradation is robust across more data (extended out-of-sample window, more trades, different regime mixes).
- Operator independently decides the §1.7.3 constraints make R1a permanently undeployable and the research value is now fully captured by the existing Phase 2m artifacts.
- The accumulated R3 + R1a+R3 evidence is enough; R1a as a candidate is closed.

### I.3 Switch from "R1a promoted-but-non-leading" to "R1a as ETH-only research evidence"

- Operator independently relaxes §1.7.3 to admit ETH-research-deployment paths (e.g., for paper/shadow on ETH separately from BTC).
- A future Phase 2p / 2q produces a docs-only planning frame that would deploy R1a+R3 on ETH for extended out-of-sample observation while leaving R3 alone on BTC.
- This is a policy change, not an evidence change. Phase 2o does not propose it.

### I.4 Switch to "stop family / new family"

- A future structural-redesign attempt (regime-conditional R1a-prime, or R1b, or R2) produces a clean §10.3 disqualification on BTC.
- Operator independently decides the absolute-edge gap (expR remains negative across all candidates and all per-fold cells) is too large to close from within this family.
- Evidence-grounded alternative-family hypothesis (e.g., funding-rate arbitrage with credible mechanism) is developed.

### I.5 Switch to Phase 4 (operational infrastructure) ahead of any 2p strategy work

- Operator independently lifts the Phase 4 deferral.
- Operational scaffolding becomes the higher-priority track regardless of strategy candidate.

### I.6 Stop point (no further phase)

- Operator pauses strategy work entirely.
- Discovery of a documentation inconsistency in prior phase records that requires a docs-only correction phase before any further strategy work.

---

## J. Next-phase options (Phase 2p variants)

Each option assumes Phase 2o closes with operator approval. Phase 2o itself does not start any of these.

### Option A — Phase 2p: pause further execution; keep R3 baseline; no immediate new redesign

**What it would look like.** A short docs-only operator-strategy review phase that consolidates the R3 baseline, formally records that R1a stays alive as research-only / non-leading, and defers further redesign work. Could be as short as a Gate 1 plan + closing memo + Gate 2 review + checkpoint, mirroring Phase 2n's structure.

**Pros.** Aligns with the §H.1 primary recommendation. Cheapest. Preserves discipline. No new evidence required.

**Cons.** Does not proactively pursue any next research direction. If the family has more to give, this option delays that.

**Wasted-effort risk.** LOW.

**EVI.** LOW for new evidence; HIGH for consolidation clarity.

### Option B — Phase 2p: docs-only hypothesis-planning for one specific next redesign

**What it would look like.** A Phase 2j-style spec-writing phase that develops a falsifiable hypothesis for one of: regime-conditional R1a-prime (per Option F.1); R1b (regime-conditional bias, Phase 2i-deferred); R2 (pullback entry, Phase 2i-deferred). Outputs: full §C-style spec, sub-parameters pre-committed singularly, falsifiable hypothesis, GAP dispositions, mandatory diagnostics list.

**Pros.** Forces explicit decision on whether the hypothesis can clear Phase 2i §1.7 binding test. If yes, a future execution Gate 1 becomes available. If no, the operator has documented reason to consolidate.

**Cons.** Adds another planning phase to the path. If the hypothesis fails the binding test, the planning effort is partially "wasted" (though the documented failure is itself information).

**Wasted-effort risk.** MEDIUM. Mitigated by docs-only scope and Phase 2j-style discipline.

**EVI.** MEDIUM-HIGH if the operator wants to keep the structural-redesign path alive.

### Option C — Phase 2p: immediate new structural execution phase

**What it would look like.** Skip the docs-only spec-writing phase and directly execute one of R1b / R2 / R1a-prime. Same Phase 2j / 2k / 2l / 2m discipline.

**Pros.** Fastest path to evidence if a strong hypothesis exists.

**Cons.** **Premature without first developing the spec.** Phase 2i originally excluded R1b and R2 for evidence-grounded reasons; reviving them needs evidence-grounded justification. Without that, this option risks producing another mixed result that doesn't move the consolidation question forward.

**Wasted-effort risk.** HIGH.

**EVI.** LOW unless an external high-EVI hypothesis is in hand.

### Option D — Later paper/shadow-readiness planning for R3 only

**What it would look like.** A future docs-only phase that designs the eventual paper/shadow path for R3 alone. Operator brief explicitly defers paper/shadow planning; this option remains deferred.

**Pros.** Aligns with R3 being research-leading. Sets up eventual operations transition.

**Cons.** Operator brief defers paper/shadow planning. Premature given expR is still negative.

**Wasted-effort risk.** MEDIUM-HIGH if invoked too early.

**EVI.** LOW for strategy; MEDIUM for operations if/when appropriate.

### Option E — Later new strategy-family research planning

**What it would look like.** Survey candidate non-breakout strategy families (mean-reversion, funding-rate arbitrage, cross-symbol relative momentum) and pre-commit a falsifiable next-family hypothesis.

**Pros.** Frees research capacity for fresh approach.

**Cons.** Premature given two PROMOTEs. Phase 2h §11.1 stopping rule (clean negative required) not met.

**Wasted-effort risk.** HIGH if invoked now.

**EVI.** LOW now.

### J.6 Next-phase summary

| Option | Description                                            | Pros                                          | Cons                                          | Wasted-effort risk | EVI         |
|--------|--------------------------------------------------------|-----------------------------------------------|-----------------------------------------------|--------------------|-------------|
| A      | Phase 2p: pause; keep R3 baseline; no new redesign      | Aligns with primary recommendation; cheap; preserves discipline | Does not pursue further direction proactively | LOW                | LOW (new) / HIGH (clarity) |
| B      | Phase 2p: docs-only hypothesis-planning                 | Forces explicit binding-test decision; preserves family path | Adds planning phase; partial-waste risk if binding test fails | MEDIUM             | MEDIUM-HIGH |
| C      | Phase 2p: immediate new structural execution            | Fast path to evidence if hypothesis exists    | Premature; risk of mixed-result repeat         | HIGH               | LOW         |
| D      | Later paper/shadow planning for R3 only                 | Aligns with R3 being research-leading         | Deferred per operator policy; premature        | MEDIUM-HIGH        | LOW (strategy) |
| E      | Later new strategy-family planning                       | Frees capacity; fresh approach                | Premature; throws away PROMOTE evidence       | HIGH               | LOW now     |

**Recommended Phase 2p:** **Option A** (pause; keep R3 baseline; no immediate new redesign) is the natural continuation under Phase 2o's primary recommendation. **Option B** is the disciplined alternative if the operator wants to keep the structural-redesign path alive via spec-writing first. The others remain effectively deferred at v1.

---

## K. Explicit non-proposal list

Phase 2o explicitly does NOT:

- Run new backtests, runs, or variants.
- Add a new redesign candidate beyond H0 / R3 / R1a+R3.
- Change any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold.
- Re-rank Phase 2g / 2l / 2m / 2n results.
- Change any committed R3 sub-parameter value (R-target stays at 2.0; time-stop stays at 8).
- Change any committed R1a sub-parameter value (X stays at 25; N stays at 200).
- Change H0's role as the sole formal §10.3 / §10.4 anchor.
- Quietly convert R1a's ETH-specific strength into a universal recommendation.
- Quietly declare R1a+R3 the new universal winner.
- Recommend any execution phase without explicit evidence-grounded justification.
- Start Phase 4 (runtime / state / persistence).
- Start paper/shadow-readiness planning.
- Start tiny-live-readiness planning.
- Declare any candidate live-ready.
- Edit `docs/12-roadmap/technical-debt-register.md` (operator restriction).
- Edit the implementation-ambiguity log (none surfaced; operator restriction).
- Touch any source file, test file, script, dataset, or manifest.
- Enable MCP, create `.mcp.json`, or enable Graphify.
- Request, create, or use any production Binance credentials.
- Add exchange-write capability of any kind.
- Download new market data.
- Call Binance APIs (authenticated or public).
- Push the Phase 2o branch to origin (deferred to operator).

---

**End of Phase 2o asymmetry-review memo.** Sections A–K complete. Threshold preservation enforced. H0 anchor preserved. R3 research-leading framing preserved. R1a+R3 promoted-but-non-leading framing preserved. ETH-specific strength NOT converted into universal recommendation. No execution phase recommended. No code changes, no runs, no new evidence — judgement and analysis only. Awaiting operator/ChatGPT Gate 2 review.
