# Phase 2n — Operator / Strategy Review Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL verdict, preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7.3 project-level locks (H0 anchor; ≤ 2 carry-forward; BTCUSDT primary); Phase 2j memo §C (R1a spec) + §D (R3 spec); Phase 2k Gate 1 plan; Phase 2l comparison report (R3 PROMOTE); Phase 2m comparison report (R1a+R3 PROMOTE — formal but mixed); Phase 2n operator-approved brief.

**Phase:** 2n — Operator / Strategy Review (docs-only).
**Branch:** `phase-2n/operator-strategy-review`.
**Memo date:** 2026-04-27 UTC.

**Status:** Recommendation produced. No code changes, no new backtests, no new variants, no parameter changes, no threshold changes, no candidate-set widening. The recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## A. Executive summary

### A.1 What Phase 2n does

Phase 2n is a docs-only review phase. It synthesizes the evidence accumulated through Phase 2g (Wave-1 REJECT ALL), Phase 2l (R3 PROMOTE), and Phase 2m (R1a+R3 formal PROMOTE with strategically mixed BTC/ETH evidence) and recommends what the highest-value next research step is. It produces a recommendation, not a decision; the operator decides.

It does not run new backtests. It does not change source code. It does not change the §10.3 / §10.4 / §11.3 / §11.4 / §11.6 framework or any committed sub-parameter value. It does not re-rank prior phases or quietly replace H0 as the formal framework anchor. It does not propose paper/shadow planning, tiny-live planning, or any operational-readiness work.

### A.2 Why review rather than another execution phase

The Phase 2m operator Gate 2 approval explicitly framed the next step:

> Phase 2n should be a docs-only operator / strategy review phase.
> Do not start another execution phase yet.
> Do not start Phase 4.
> Do not start paper/shadow planning yet.

The strategic reason: Phase 2m's PROMOTE is **formal under the unchanged framework but mixed in interpretation**. A naïve "next variant in line" execution after Phase 2m risks (a) cementing R1a+R3 as the new universal baseline when its BTC behaviour does not justify that, (b) treadmill behaviour through more structural redesigns without first deciding what the family-level evidence now means, or (c) accidentally moving toward operational readiness on a candidate the operator has not yet endorsed for that path. Stepping back is the disciplined response.

### A.3 Plain-English summary of the current family state

The locked v1 breakout family has now been tested under three discipline regimes:

1. **Parametric tweaks (Phase 2g Wave-1).** Four single-axis parameter changes — H-A1 (setup-window length), H-B2 (trigger expansion), H-C1 (HTF EMA pair), H-D3 (break-even threshold). All four REJECTED on BTC under §10.3 disqualification. Verdict: parameter-level fixes don't move the needle on the four tested axes. Wave-1 is preserved as historical evidence; no comparison-baseline shifting.

2. **Exit-philosophy structural redesign (Phase 2l R3).** Replace H0's seven-stage staged-trailing exit machinery with R3's two-rule terminal exit (fixed-R take-profit at +2 R + unconditional time-stop at 8 bars; protective stop never moved). PROMOTED on R via §10.3.a + §10.3.c on **both** BTC and ETH. R3 produced the project's first-ever positive-expR per-fold results on BTC (F2 +0.015, F3 +0.100). V-window confirmed direction-of-improvement out-of-sample. R3 improves expR in **all 6** regime-symbol cells. R3 is broad-based, robust to slippage and stop-trigger sensitivity, and clean (zero TRAILING_BREACH/STAGNATION leakage).

3. **Setup-validity structural redesign on top of R3 (Phase 2m R1a+R3).** Replace H0's range_width/drift two-clause setup predicate with R1a's percentile-based ranking (volatility ≤ 25th percentile of trailing 200 bars). PROMOTED on R via §10.3.c (BTC) + §10.3.a + §10.3.c (ETH) — but **the BTC clearance is on §10.3.c only, with Δexp +0.039 R below the §10.3.a +0.10 threshold**. R3-anchor view shows R1a hurts BTC (Δexp_R3 −0.180) and helps ETH (Δexp_R3 +0.237). V-window confirms the asymmetry: ETH first-ever positive-netPct validation result (+0.69%, expR +0.386, PF 2.222); BTC severely degraded (4 trades, 0% WR, expR −0.990).

The breakout family is responding to structural-redesign work — both R3 and R1a+R3 PROMOTE cleanly under the unchanged framework. But absolute performance remains negative in aggregate on R, and R1a's contribution is symbol-asymmetric. The family has not been disproven, but it has not been demonstrated to be live-ready. The decision in front of the operator is what to do with this nuanced picture.

---

## B. Fixed evidence recap

(All numbers quoted from already-committed reports. No re-derivation. No re-running of any variant.)

### B.1 H0 baseline facts that still matter

The locked Phase 2e baseline (FULL window 51 months; v002 datasets):

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|-------:|-------:|--------:|------:|--------:|--------:|
| BTCUSDT |     41 | 29.27% |  −0.43  | 0.32  |  −3.95% |  −4.23% |
| ETHUSDT |     47 | 23.40% |  −0.39  | 0.42  |  −4.07% |  −4.89% |

R-window (36 months, Phase 2g/2l/2m H0 control):

| Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|-------:|-------:|--------:|------:|--------:|--------:|
| BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% |
| ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% |

Signal-funnel dominant rejections under H0: `no valid setup` ~58%, `neutral bias` ~37%, `no close-break` ~5%. R3 keeps these untouched (H0 setup predicate). R1a+R3 changes the setup predicate; the funnel attribution stays in `rejected_no_valid_setup` for both predicates.

H0 is descriptive baseline only. It is **not** a promotion candidate. It serves as the **sole comparison anchor** for §10.3 / §10.4 evaluation per Phase 2i §1.7.3.

### B.2 Phase 2g Wave-1 result (committed, preserved as historical evidence)

| Variant | Axis tested                              | BTC §10.3 verdict                            |
|---------|------------------------------------------|----------------------------------------------|
| H-A1    | setup_size 8 → 10                        | DISQUALIFY (worse expR + worse PF)            |
| H-B2    | expansion_atr_mult 1.0 → 0.75            | DISQUALIFY (|maxDD| ratio 1.505× > 1.5×)      |
| H-C1    | ema_fast/ema_slow 50/200 → 20/100        | DISQUALIFY (worse expR + worse PF)            |
| H-D3    | break_even_r 1.5 → 2.0                   | DISQUALIFY (worse expR)                       |

Wave-1 verdict: REJECT ALL. Single-axis parameter changes on the four tested axes do not pass the framework. H-B2 was the closest case (cleared §10.3.a but vetoed by the |maxDD| > 1.5× baseline floor).

Wave-1 evidence is **historical only**. It is not a comparison baseline for any subsequent candidate; H0 is the anchor. Wave-1 numbers may be cited diagnostically (e.g., "H-A1 already eliminated the window-length-tweak alternative") but never as a target for promotion comparison.

### B.3 Phase 2l R3 PROMOTE result

R-window (36 months, MEDIUM slippage, MARK_PRICE):

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|
| H0      | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% |
| H0      | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% |
| R3      | BTCUSDT |     33 | 42.42% |  **−0.240** | **0.560** |  **−1.77%** |  **−2.16%** |
| R3      | ETHUSDT |     33 | 33.33% |  **−0.351** | **0.474** |  **−2.61%** |  **−3.65%** |

Deltas vs H0: BTC Δexp **+0.219** / ΔPF **+0.305** / Δ|dd| **−1.515 pp**; ETH Δexp **+0.124** / ΔPF **+0.153** / Δ|dd| **−0.487 pp**.

**Verdict: PROMOTE on both symbols via §10.3.a + §10.3.c.** No §10.3 disqualification floor; |maxDD| ratios 0.588× BTC / 0.882× ETH (well below 1.5×). §10.4 hard reject does not apply (Δn = 0).

Per-fold (5 rolling, GAP-036): R3 beats H0 in **4/5** BTC folds and **3/5** ETH folds. F2 +0.015 and F3 +0.100 are the project's first-ever positive-expR BTC folds. F1 ties exactly; F4-F5 BTC also improve modestly.

V-window: H0 BTC −0.313 / R3 BTC −0.287 (improvement); H0 ETH −0.174 / R3 ETH −0.093 (improvement); WR ETH 28.57% → 42.86%. Direction-of-improvement holds out-of-sample.

Mandatory diagnostics: realized 1h-vol regime expR — R3 improves expR in **all 6** regime-symbol cells (after the operator-required corrected diagnostic in Phase 2l). MFE distribution mostly unchanged (R3 doesn't alter excursion measurement up to the take-profit point). Long/short asymmetry: R3 narrows BTC long/short asymmetry; ETH shorts under R3 +0.028 R / PF 1.07 (first-ever positive direction-symbol cell). TAKE_PROFIT mean R 1.64 (BTC) / 1.52 (ETH) — fees + slippage + next-bar-open fill mechanic; expected. TIME_STOP bias near zero — symmetric. Implementation-bug check clean. Slippage sensitivity monotone. TRADE_PRICE bit-identical.

### B.4 Phase 2m R1a+R3 PROMOTE result (formal but mixed)

R-window (36 months, MEDIUM slippage, MARK_PRICE):

| Variant | Symbol  | Trades | WR     | expR    | PF    | netPct  | maxDD   |
|---------|---------|-------:|-------:|--------:|------:|--------:|--------:|
| H0      | BTCUSDT |     33 | 30.30% |  −0.459 | 0.255 |  −3.39% |  −3.67% |
| R3      | BTCUSDT |     33 | 42.42% |  −0.240 | 0.560 |  −1.77% |  −2.16% |
| R1a+R3  | BTCUSDT |     22 | 27.27% |  **−0.420** | **0.355** |  −2.07% |  −2.33% |
| H0      | ETHUSDT |     33 | 21.21% |  −0.475 | 0.321 |  −3.53% |  −4.13% |
| R3      | ETHUSDT |     33 | 33.33% |  −0.351 | 0.474 |  −2.61% |  −3.65% |
| R1a+R3  | ETHUSDT |     23 | 34.78% |  **−0.114** | **0.833** |  −0.59% |  −2.96% |

H0-anchor deltas (governing): BTC Δexp **+0.039** / ΔPF **+0.100** / Δ|dd| −1.341 pp / Δn **−33.3%**; ETH Δexp **+0.362** / ΔPF **+0.512** / Δ|dd| −1.171 pp / Δn **−30.3%**.

**Formal verdict: PROMOTE.** BTC clears §10.3.c **only** (Δexp +0.039 < §10.3.a's +0.10 threshold); ETH clears §10.3.a + §10.3.c. No §10.3 disqualification floor; no §10.4 (Δn < 0); §11.4 ETH-as-comparison rule satisfied.

R3-anchor deltas (descriptive only): BTC Δexp **−0.180** / ΔPF **−0.205**; ETH Δexp **+0.237** / ΔPF **+0.359**.

V-window: R1a+R3 ETH **first positive netPct ever** (8 trades / 62.5% WR / expR **+0.386** / PF **2.222** / netPct **+0.69%** / maxDD only 0.51%). R1a+R3 BTC severely degraded (4 trades / 0% WR / expR **−0.990** / netPct **−0.88%**).

Per-fold: R1a+R3 beats H0 in 2/5 BTC folds (F3 +1.215, F4 +0.789) and 4/5 ETH folds. R1a+R3 beats R3 in 2/5 BTC folds and 2/5 ETH folds — much weaker than R3 vs H0.

R1a-specific diagnostic: **100%** of filled R1a entries at ATR percentile ≤ 25% (predicate working as designed; admitting only bottom-quartile compression bars). Funnel attribution stays interpretable in `rejected_no_valid_setup`.

Per-regime expR (realized 1h vol): R1a+R3 ETH low_vol n=11 expR **+0.281 R / PF 1.353** — first regime-symbol cell with **positive expR AND PF > 1** in any phase. R1a+R3 ETH shorts n=16 expR **+0.387 / PF 1.906** — strongest direction-symbol cell ever observed.

R1a+R3 BTC under R: low_vol degrades vs R3 (−0.329 vs −0.054); high_vol degrades vs R3 (−0.942 vs −0.472). R1a's filter is correctly identifying compression — but BTC compression bars do not consistently translate into post-breakout follow-through.

Implementation-bug check clean. Slippage sensitivity monotone. TRADE_PRICE bit-identical.

### B.5 What is now known technically

After three structural-redesign experiments and one parametric one:

- The **research stack** (data layer, backtester, variant config, diagnostic funnel, multi-symbol runner, manifests, GAP-036 fold convention) is mature and reusable.
- The **§10.3 / §10.4 / §11.3 / §11.4 / §11.6 framework** is robust enough to produce informative verdicts on small samples (33 trades on R) and to distinguish a clean broad-based promotion (R3) from a mixed symbol-asymmetric promotion (R1a+R3) without post-hoc threshold adjustment.
- The **H0 baseline is preserved bit-for-bit through Phase 2g, 2l, and 2m** controls, confirming that successive optional fields and dispatch logic do not silently regress the locked Phase 2e behaviour.
- **Same-bar STOP > TAKE_PROFIT > TIME_STOP priority** is enforced both structurally (engine pre-check) and within management (helper dispatch).
- **The volatility-percentile predicate works as designed** on this data: 100% of R1a entries at percentile ≤ 25%; the predicate is admitting compression bars as intended.
- **The mark-price stop-trigger semantic is consistent with TRADE_PRICE on this data**: zero gap-through stops across R3 and R1a+R3.
- **Wave-1 disqualification logic** correctly fired on tail-risk (H-B2) and on edge worsening (H-A1, H-C1, H-D3).

### B.6 What remains unresolved strategically

Phase 2n's job is to address these:

1. **Is R3 alone the research-leading baseline going forward?** R3's promotion is broad-based; R1a+R3's is asymmetric. Strategically, R3 has earned the "leading" label; R1a+R3 has earned a "promoted but conditional" label. But these are framings, not committed project policies — the operator decides.
2. **What is the right framing for R1a+R3?** "Universal winner" is not supported by the BTC evidence. "ETH-specialty candidate" is closer but the operator brief deliberately keeps the project at one-symbol-live (BTCUSDT) per Phase 2i §1.7.3. "Promoted but non-leading branch" is the framing that matches the evidence and the project-level locks.
3. **Has the family earned more research investment?** Two of three structural redesigns have PROMOTED; the family is not a dead end. But absolute performance is still negative in aggregate; the family is not a clear winner either.
4. **Where is the next-highest-EVI step?** Five plausible options enumerated in §F below; recommendation in §G; switch conditions in §H.

---

## C. Candidate hierarchy analysis

### C.1 H0 status

**H0 is the framework anchor and remains the sole comparison anchor for §10.3 / §10.4 evaluation per Phase 2i §1.7.3.** It is not a promotion candidate; it is descriptive baseline. It will continue to be re-run as the control in any future execution phase to enforce bit-for-bit preservation regression.

### C.2 R3 status

**R3 is the research-leading baseline.** It is the locked exit-philosophy baseline that any future structural-redesign work should sit on top of (Phase 2m's R1a was specifically built on top of R3's locked exit machinery, not on top of H0's). R3:

- Promoted broadly on R (both BTC and ETH; both §10.3.a and §10.3.c).
- Confirmed direction-of-improvement out-of-sample on V (both BTC and ETH).
- Improved expR in all 6 regime-symbol cells.
- Beat H0 in 4/5 BTC folds and 3/5 ETH folds (first-ever positive BTC fold expR results).
- Robust to slippage sensitivity and stop-trigger sensitivity.
- Implementation clean (zero TRAILING_BREACH/STAGNATION leakage).
- Sub-parameters (R-target = 2.0, time-stop bars = 8) anchored to existing project conventions, not selected by fitting.

R3's case is the strongest the project has ever produced. Treating R3 as the research-leading baseline is the disciplined reading of the evidence.

### C.3 R1a+R3 status

**R1a+R3 is a promoted but non-leading branch.** It cleared the unchanged §10.3 framework, so it is a formal PROMOTE. But:

- The BTC clearance is **weak** — only §10.3.c strict-dominance fires (Δexp +0.039 R is below §10.3.a's +0.10 threshold; near the noise scale at 22-trade samples).
- The R3-anchor view shows R1a **hurts** BTC (Δexp_R3 −0.180 R, ΔPF_R3 −0.205) and **helps** ETH (Δexp_R3 +0.237 R, ΔPF_R3 +0.359).
- V-window evidence amplifies the asymmetry: ETH first-ever positive netPct (+0.69%); BTC severe (4 trades / 0% WR / expR −0.990).
- Per-fold view: 2/5 BTC, 4/5 ETH vs H0; 2/5 / 2/5 vs R3 — R1a contributes mixed value.
- R1a's predicate is **mechanically correct** (100% of entries at percentile ≤ 25%), so the asymmetry is not an implementation bug. It is a regime-selection asymmetry: R1a's compression filter selects bars that on ETH genuinely precede follow-through and on BTC do not. This is a fact about the data + strategy interaction, not about R1a's correctness.

### C.4 The framing decision for R1a+R3

The three options the operator brief enumerates:

| Framing                                     | Compatible with the evidence? | Compatible with project locks (§1.7.3)?       |
|---------------------------------------------|-------------------------------|-----------------------------------------------|
| New primary candidate                       | NO — BTC degradation vs R3 is real | NO — BTCUSDT is the live primary; an ETH-helping/BTC-hurting candidate is not a primary |
| Symbol-asymmetric specialty candidate       | YES — matches the evidence    | NO at v1 live (one-symbol live; ETH research/comparison only) — but valid at research level |
| Promoted but non-leading branch             | YES — matches the evidence    | YES — preserves H0 anchor + project-level locks; defers operational implications |

**Recommended framing: promoted but non-leading branch.** This is the framing the operator's Phase 2m Gate 2 approval explicitly anchored ("R1a+R3 is a promoted but strategically mixed candidate that requires a review phase before further execution or any deployment-readiness planning"). It is the framing that preserves both the formal §10.3 verdict and the project-level locks.

The "symbol-asymmetric specialty" framing is informationally true (R1a helps ETH dramatically, hurts BTC) but should not be operationalized at v1 — Phase 2i §1.7.3 keeps BTCUSDT as the live primary and ETHUSDT as research/comparison only. A future symbol-specific deployment is not on the v1 roadmap.

### C.5 Summary candidate hierarchy

```
H0           — framework anchor (descriptive baseline only, never a candidate)
R3           — research-leading baseline (broad-based PROMOTE; preserved as exit baseline for any future redesign)
R1a+R3       — promoted but non-leading branch (formal PROMOTE; symbol-asymmetric; not the new universal winner)
Wave-1       — historical evidence only (REJECT ALL; never a comparison baseline)
```

---

## D. Interpretation of the mixed Phase 2m result

### D.1 Why the H0-anchor PROMOTE is valid

The §10.3 framework was designed pre-Wave-1 with three explicit promotion paths (a / b / c) and a disqualification floor; thresholds were committed before any candidate was tested (§11.3.5 binding rule). R1a+R3 satisfies §10.3.c on BTC and §10.3.a + §10.3.c on ETH; the disqualification floor does not fire; §10.4 does not apply (Δn < 0); §11.4 ETH-as-comparison rule is satisfied. **The verdict is what it is.** Refusing to call it PROMOTE would amount to post-hoc threshold tightening — exactly what §11.3.5 forbids.

The framework was deliberately designed to admit small-margin promotions on §10.3.c when the magnitude path (§10.3.a) doesn't fire, because strict-dominance is itself meaningful evidence (everything moved the right direction; nothing got worse). The §10.3.c clearance on BTC is genuine framework evidence.

### D.2 Why the R3-anchor view still matters strategically

Two reasons:

- **R3 is the locked exit baseline for any future redesign.** The Phase 2m brief explicitly framed R1a as "on top of R3" — the candidate is R1a+R3, not R1a-on-H0. So the question "does R1a contribute value on top of R3?" is the natural strategic question, even though it is not the §10.3 governing question.
- **The R3-anchor view reveals that R1a's marginal contribution is asymmetric.** That asymmetry is not visible in the H0-anchor view because R3's exit-machinery improvements absorb part of R1a's BTC degradation. Without the R3-anchor view, the operator would be making decisions about R1a's value without knowing what R1a alone is contributing.

The R3-anchor view does not replace H0 as the formal anchor. It is supplemental, descriptive, and exists to inform strategic interpretation. The Phase 2m comparison report explicitly labeled it that way (§5 of that report); Phase 2n preserves the labeling.

### D.3 Why Phase 2m is not a clean replacement result

A clean replacement result would have Δexp ≥ 0 vs R3 on both symbols, ideally with §10.3.a-magnitude improvements on both. Phase 2m has Δexp_R3 −0.180 BTC and Δexp_R3 +0.237 ETH — opposite-signed, with the BTC degradation amplified out-of-sample on V (R1a+R3 BTC V is the project's worst V cell ever). A clean replacement would be unambiguous evidence that R1a+R3 is universally better than R3. The evidence does not support that.

### D.4 How BTC and ETH asymmetry should affect decision-making

The decision principle the project has committed to (Phase 2i §1.7.3) is:

- BTCUSDT is the live primary.
- ETHUSDT is research/comparison only.
- BTC must clear; ETH must not catastrophically fail (§11.4).

Under that principle:

- R1a+R3 PROMOTES because BTC clears (weakly via §10.3.c) and ETH does not catastrophically fail.
- But the asymmetry — R1a hurts BTC vs R3 — is a strategic warning sign for any future operational-readiness planning. Deploying R1a+R3 in any future paper/shadow on the BTC live primary would be deploying a candidate whose marginal contribution on the live symbol is negative.
- The asymmetry **does** mean: if (and only if) the project ever lifts the one-symbol-live restriction, R1a+R3 might be the right candidate for ETH-specific research deployment. That decision is not in scope for Phase 2n.
- Within Phase 2n's scope: the asymmetry means **R3 alone is the better candidate for any future BTC-focused operational work**, and R1a+R3 should be retained as a research artifact informing future ETH-focused or symbol-aware research.

### D.5 What the evidence pattern now implies

The project has accumulated a coherent picture across three structural-redesign axes (one parametric Wave-1, two structural):

1. **Parameter-level fixes don't help (Wave-1).**
2. **Exit-philosophy redesign helps universally (R3).**
3. **Setup-validity redesign on top of R3 helps ETH and hurts BTC (R1a+R3).**

The most likely interpretations, ordered by support strength:

1. **R3's exit-philosophy improvement is real and broad-based.** HIGH confidence — supported by per-symbol R + V + slippage + stop-trigger + per-fold + per-regime evidence.
2. **R1a's setup-validity improvement is real on ETH.** MEDIUM-HIGH confidence — supported by R-window expR, V-window first-positive-netPct, per-regime ETH-low_vol PF > 1, per-direction ETH-shorts strongest cell ever. But: 23 trades on R + 8 on V is small.
3. **R1a's setup-validity improvement is symbol-asymmetric and hurts BTC.** MEDIUM confidence — supported by R3-anchor BTC Δexp −0.180 + V-window BTC 0% WR. But: 22 trades on R + 4 on V is small.
4. **The breakout family has genuine structural-edge potential but absolute live-readiness is still distant.** MEDIUM confidence — even R3's R-window expR is −0.240 R / −0.351 R; V-window is similar. The strategy still loses money on average.

The framework is not yet showing evidence of a strong absolute-edge result. It is showing evidence of structural-redesign-responsiveness. Continued research is justified; declaration of victory is not.

### D.6 Symbol-specific edge / regime-specific edge / fragile conditional edge?

The operator brief asks whether the project has evidence of:

- Symbol-specific edge,
- Regime-specific edge,
- Or still only fragile conditional edge.

Evidence-based answer:

- **Regime-specific edge: YES (under R3 alone, modestly).** R3's per-regime view shows expR improves in all 6 cells; the strongest absolute cell is R3 ETH low_vol −0.177 / 0.747. R1a+R3 reveals stronger regime-specific edge: ETH low_vol with R1a+R3 is +0.281 / 1.353 — first cell with positive expR AND PF > 1. This is regime-conditional edge, materializing in the bottom-quartile-volatility regime on ETH.
- **Symbol-specific edge: YES (under R1a+R3, on ETH).** R1a+R3 ETH V-window +0.69% netPct is the project's first positive-netPct out-of-sample result. ETH shorts under R1a+R3 are +0.387 R / 1.906 PF. This is symbol-specific edge at the ETH-research level. Under Phase 2i §1.7.3 it is **not** symbol-specific edge at the v1-live level (BTC primary).
- **Fragile conditional edge: also YES.** Even the strongest cells are small samples (n = 8–16) and the absolute aggregate is still negative on R for both R3 and R1a+R3. The framework discipline is holding, but the absolute-edge case has not been made.

So the project has accumulated **all three kinds of evidence**, with the strongest being regime-conditional and symbol-conditional, and the absolute-aggregate case still weak. This is normal for early-stage structural-redesign research; it is not a green-light for live deployment.

---

## E. Family-level judgement

### E.1 Has the breakout family shown enough evidence to justify continued research?

**Yes, modestly.** Two of three structural-redesign experiments have PROMOTED under the unchanged framework. The framework discipline has held throughout. Per-regime + per-direction + per-fold diagnostics have surfaced regime-conditional and symbol-conditional positive cells. The family responds to structural work.

But the case is qualified:

- Absolute aggregate expR is still negative on R for both promoted candidates (R3: BTC −0.240 / ETH −0.351; R1a+R3: BTC −0.420 / ETH −0.114).
- Wave-1's REJECT ALL means parameter-level fixes are exhausted on the four tested axes.
- R1a+R3's mixed promotion limits the value of stacking further structural redesigns without first deciding what direction to push.

The family is **alive** but **not validated**.

### E.2 Is R3 enough of an improvement to keep this family alive?

**Yes.** R3 alone clears every threshold the project has committed to:

- §10.3.a + §10.3.c on both BTC and ETH (broad-based).
- §10.3 disqualification floor not triggered (|maxDD| ratios well below 1.5×).
- V-window confirms direction-of-improvement on both symbols.
- All 6 regime-symbol cells improve.
- 4/5 BTC folds, 3/5 ETH folds beat H0.
- Implementation clean.
- Robust to slippage and stop-trigger sensitivity.

R3 is the project's first PROMOTE verdict and remains the strongest result the project has ever produced. It is, by itself, sufficient to justify keeping the family alive.

### E.3 Does R1a strengthen the family overall, or only selectively?

**Selectively.** R1a's contribution on top of R3 is asymmetric: helps ETH, hurts BTC. The ETH improvement is substantial and robust; the BTC degradation is real and amplified out-of-sample on V. R1a does not strengthen the family in a universally-applicable sense.

R1a does, however, **strengthen the project's understanding** of where edge lives:

- On ETH, R1a's compression filter unlocks something genuinely valuable (first positive-netPct V-window).
- On BTC, R1a's compression filter selects bars that don't follow through — telling us something about BTC's regime structure under v002 R-window data.
- This is genuine information about the strategy / data interaction.

So R1a strengthens the family **diagnostically** but not **deployment-readiness-wise**.

### E.4 Should the project continue optimizing inside this family, or should it stop soon unless a stronger result appears?

**The disciplined answer: continue cautiously, with clear stopping criteria.**

Continue cautiously means:

- Treat R3 alone as the research-leading baseline going forward.
- Do not run another structural-redesign execution phase without first deciding what next-axis hypothesis is genuinely worth testing.
- Use the existing two-promotion evidence base to inform the next decision, not to drive automatic momentum.

Clear stopping criteria means:

- If a third structural redesign (e.g., R1b regime-conditional bias, R2 pullback entry) is run and produces a REJECT or another mixed promotion, the family should be set aside in favour of operational infrastructure work (Phase 4) or new-family research.
- If the operator's analysis decides the asymmetric R1a evidence is not informative enough, the family stays alive at R3-alone and operational infrastructure planning becomes the higher-EVI path.

The recommendation is **not** "continue execution immediately". It is "review first, decide second, execute only if the next hypothesis is genuinely high-EVI".

---

## F. Decision options analysis

The operator brief enumerates five options. Each is evaluated below on pros / cons / wasted-effort risk / expected-value-of-information / justification threshold.

### Option A — Keep R3 as the research-leading version and stop further immediate redesign execution

**What it would look like.** Recognize R3 as the research-leading baseline. R1a+R3 is retained as a promoted-but-non-leading research branch. No new execution phase is started; the project pauses to consolidate before deciding the next direction. Future work focuses on either operational-infrastructure scaffolding (Phase 4-equivalent, deferred), targeted analysis on existing data, or a deliberate re-think of where edge would come from next.

**Pros.** Preserves the cleanest result the project has produced. Stops treadmill behaviour. Keeps R1a+R3 alive as a research artifact without operationalizing it. Aligns with the Phase 2m operator framing of "promoted but mixed; review before next step". Low-cost.

**Cons.** Doesn't proactively pursue the R1a+R3 ETH signal. If the family is genuinely improvable with one more structural axis, this option delays that.

**Wasted-effort risk.** LOW. R3 is committed; pause does not invalidate it.

**EVI.** MEDIUM. The information value comes from the operator's strategic decision rather than from new evidence.

**Justification threshold.** Operator agrees that the family-level case is "alive but not validated" and wants to consolidate before further execution. This is the disciplined interpretation of the Phase 2m mixed result.

### Option B — Continue with a targeted next redesign / analysis phase focused on the asymmetry revealed by R1a

**What it would look like.** A docs-only or analysis-only phase that examines the BTC/ETH R1a asymmetry in depth. Possible angles: (a) per-trade walkthrough of R1a's BTC F2 degradation (R3 BTC F2 +0.015 → R1a+R3 BTC F2 −0.792), (b) regime decomposition of R1a's BTC entries that produce 0% V-window WR, (c) hypothesis generation for whether a regime-conditional version of R1a (e.g., apply R1a only when 1h volatility regime is in a specific band) would salvage BTC. Could be docs-only or could escalate to a future R1c / R1a-prime execution phase if the diagnostic is informative.

**Pros.** Directly attacks the most-informative anomaly the project has surfaced. Could yield a third structural redesign with cleaner BTC behaviour. Inside the existing family.

**Cons.** Extends the family-research treadmill. The asymmetry might be a fact about BTC's R-window regime structure, not a fixable strategy issue — in which case the analysis would not produce an actionable next-redesign hypothesis. Would still need its own Gate 1 / Gate 2 cycle.

**Wasted-effort risk.** MEDIUM. The analysis is informative regardless, but the next-redesign hypothesis it produces (if any) might fail in execution.

**EVI.** MEDIUM-HIGH if the operator wants to deepen understanding before deciding the family's fate. LOWER if the operator's reading is "the asymmetry is a feature of the data, not a fixable spec issue".

**Justification threshold.** Operator wants to invest one more research cycle inside the family before deciding whether to consolidate (Option A) or continue execution (next-redesign).

### Option C — Begin paper/shadow-readiness planning later for R3 only (not in this phase)

**What it would look like.** Phase 2n recommends that a future phase begin paper/shadow-readiness planning for R3 alone, with R1a+R3 explicitly excluded from operational paths. The actual planning happens in a separate phase; Phase 2n only frames the option.

**Pros.** Aligns with R3 being the broad-based, robust, research-leading version. Preserves Phase 2i §1.7.3 BTC-primary discipline. Sets up the eventual transition from research to paper/shadow on the strongest candidate.

**Cons.** Premature given that even R3's R-window expR is −0.240 R (still negative absolute). Paper/shadow at expR < 0 is observation-only and doesn't generate live-readiness value beyond what backtests already show. Operator brief explicitly says "do not start paper/shadow planning yet"; this option only frames it as a later possibility.

**Wasted-effort risk.** MEDIUM-HIGH if invoked too early. Paper/shadow infrastructure investment that is reshaped by a later structural-redesign decision is real cost.

**EVI.** LOW for the strategy question; MEDIUM for the operational-readiness question.

**Justification threshold.** Operator decides the family is sufficiently characterized at R3 and wants the next research delivery to be operational rather than another redesign.

### Option D — Begin paper/shadow-readiness planning later for R1a+R3 despite the asymmetry

**What it would look like.** A future phase begins paper/shadow-readiness planning for R1a+R3 specifically — not because R1a+R3 is universally better than R3, but because the ETH signal is the strongest absolute-edge result the project has ever produced and the operator wants to preserve the option to operationalize it later if the v1 one-symbol-live restriction is ever lifted.

**Pros.** Preserves the ETH +0.69% V-window signal as a deployable artifact. Acknowledges that R1a+R3 has produced unique evidence (first positive-netPct V-window) not present in R3 alone.

**Cons.** Operationalizing R1a+R3 on BTC under v1's BTC-primary policy would deploy a candidate whose marginal contribution on the live symbol is negative. The Phase 2i §1.7.3 lock makes this option effectively unavailable at v1. Operator brief explicitly says "do not start paper/shadow planning yet".

**Wasted-effort risk.** HIGH if invoked at v1. The operational-readiness investment would be on a candidate that the project's own framework says is not the BTC primary's best representative.

**EVI.** LOW within v1's BTC-primary policy. HIGHER only if the operator independently decides to relax §1.7.3 and admit ETH-research-deployment.

**Justification threshold.** Operator independently decides to relax §1.7.3 (a policy change beyond Phase 2n's scope). Without that, this option is dominated by Option C.

### Option E — Stop this family and shift to a different strategy family later

**What it would look like.** Phase 2n recommends that future research not extend the breakout family further; instead pursue a different family (e.g., mean-reversion in low-vol regimes, funding-rate arbitrage, cross-symbol relative momentum). Phase 2n itself does not start the new family — it only frames the deferral / shift.

**Pros.** Acknowledges that the absolute-aggregate case for the breakout family is still weak even after two PROMOTEs. Frees research capacity for a fresh approach. May produce a stronger absolute-edge result.

**Cons.** **Premature given the evidence.** The family has shown structural-redesign responsiveness; abandoning it now wastes the structural-redesign progress. R3's broad-based PROMOTE is the strongest result the project has produced. Throwing that away to start fresh is not justified by current evidence. The Phase 2h decision memo §13 explicitly stated that family abandonment is justified only when "structural redesign has been honestly tried with a falsifiable hypothesis and produced its own clean negative". R3 + R1a+R3 are both PROMOTEs, not negatives.

**Wasted-effort risk.** HIGH. Throws away two PROMOTE verdicts and the supporting research stack.

**EVI.** LOW now. Higher only after a third structural redesign produces a clean negative inside the family.

**Justification threshold.** A third structural-redesign attempt produces a §10.3 disqualification, OR the operator independently decides the absolute-edge gap is too large to close from within this family. Neither condition is currently met.

### F.6 Options summary table

| Option | Description                                                  | Pros                                          | Cons                                          | Wasted-effort risk | EVI       | Justification threshold met now? |
|--------|--------------------------------------------------------------|-----------------------------------------------|-----------------------------------------------|--------------------|-----------|---------------------------------|
| A      | R3 as research-leading; stop further immediate execution     | Preserves cleanest result; matches operator framing; low-cost | Doesn't proactively pursue R1a+R3 ETH signal | LOW                | MEDIUM    | YES                              |
| B      | Targeted asymmetry-review / analysis phase                   | Attacks most-informative anomaly; informative either way | Treadmill risk; might not yield actionable hypothesis | MEDIUM             | MEDIUM-HIGH | Operator-discretion              |
| C      | Later paper/shadow planning for R3 only                       | Aligns with R3 being leading; preserves locks | Premature at expR < 0; deferred per operator restriction | MEDIUM-HIGH        | LOW (strategy) / MEDIUM (operations) | NO at this time             |
| D      | Later paper/shadow planning for R1a+R3                        | Preserves ETH signal                          | Conflicts with §1.7.3 BTC-primary; deferred per operator restriction | HIGH               | LOW within v1 | NO at this time             |
| E      | Stop family, shift to different strategy family               | Frees capacity; fresh approach                | Premature; throws away two PROMOTEs           | HIGH               | LOW now   | NO                              |

---

## G. Recommendation

This recommendation is **provisional and evidence-based, not definitive**. The operator decides.

### G.1 Primary recommendation: Option A — R3 as the research-leading version; stop further immediate redesign execution

**R3 is now the research-leading baseline.** R1a+R3 remains alive as a promoted but non-leading research branch. No new execution phase is justified immediately.

**Rationale.** The Phase 2m PROMOTE is formal under the framework but mixed in interpretation. Running a third structural-redesign execution immediately after Phase 2m risks treadmill behaviour without first deciding what direction is genuinely high-EVI. R3 alone is the broad-based winner; cementing it as the research-leading baseline preserves the cleanest result the project has produced and aligns with the Phase 2m operator-approved framing of "promoted but mixed; review before next step". The Phase 2i §1.7.3 BTC-primary locks make R1a+R3 a non-candidate for v1 operational paths regardless of its ETH signal.

This is consistent with the Phase 2h §11.1 stopping rule (paraphrased): a family is abandoned only after structural redesign has been honestly tried and produced a clean negative. The breakout family has not produced a clean negative — R3 is a broad PROMOTE, R1a+R3 is a mixed PROMOTE. The disciplined path is **consolidate, don't accelerate**.

**Concrete implications:**

- Treat R3 (`exit_kind=FIXED_R_TIME_STOP`, R-target=2.0, time-stop=8) as the baseline-of-record for any future structural-redesign work or operational-readiness planning.
- Treat R1a+R3 as a research artifact — the project's evidence for what setup-validity redesign costs and gains on this data, useful for future hypothesis generation but not the deployable variant.
- Do not start Phase 2o execution unless and until a specific high-EVI hypothesis for the next axis is independently developed (e.g., from the Phase 2i-deferred candidates R1b or R2, or from a targeted asymmetry review).
- Phase 4 stays deferred per operator policy.
- Paper/shadow planning stays deferred per operator policy.

### G.2 Fallback: Option B — Targeted asymmetry review / analysis phase

If the operator judges that more diagnostic insight on the R1a BTC/ETH asymmetry is worth one more research cycle before consolidating, **Phase 2o would be a docs-only / analysis-only review of the asymmetry**: per-trade walkthroughs, regime decomposition of BTC R1a entries, hypothesis generation for whether a regime-conditional R1a-variant might salvage BTC. Could escalate to an execution phase later if the diagnostic produces an actionable hypothesis; could close out as docs-only if it does not.

Option B's risk is treadmill — extending the family's research without a clear stopping rule. Its value is that it directly attacks the most-informative anomaly the project has surfaced. It is the disciplined "one more analysis cycle before consolidating" path.

### G.3 What is explicitly NOT recommended

- **Option C (later paper/shadow for R3 only):** premature given expR remains negative; operator brief defers paper/shadow planning.
- **Option D (later paper/shadow for R1a+R3):** conflicts with §1.7.3 BTC-primary lock; operator brief defers paper/shadow planning.
- **Option E (stop family, shift to new family):** premature given two PROMOTE verdicts; abandons the strongest evidence base the project has accumulated.
- **Phase 4 work:** deferred per operator policy.
- **Live-readiness planning of any kind:** deferred per operator policy.

### G.4 Explicit framework / lock preservation

The recommendation enforces:

- **R3 is the research-leading baseline; R1a+R3 is a promoted but non-leading branch.** Both PROMOTE verdicts stand.
- **H0 remains the sole formal §10.3 / §10.4 anchor.** The R3-anchor view in Phase 2m is supplemental.
- **Phase 2i §1.7.3 project-level locks are unchanged.**
- **Wave-1 REJECT ALL is preserved as historical evidence only.**
- **No paper/shadow / tiny-live readiness claim is implied by either PROMOTE verdict.**

---

## H. What would change this recommendation

The recommendation is **provisional**. The following kinds of evidence or operator-policy decisions would justify switching paths:

### H.1 Switch from Option A (primary) to Option B (fallback as primary)

- Operator wants one more analysis cycle on the R1a BTC/ETH asymmetry before consolidating.
- Operator believes the asymmetry might be addressable by a regime-conditional variant (R1a-prime) and wants docs-only diagnostic work to test that hypothesis.
- Operator wants to delay the decision between consolidation (Option A) and further execution until more diagnostic insight is in hand.

### H.2 Switch from Option A to a future structural-redesign execution (R1b, R2, or R1a-prime)

- A specific high-EVI hypothesis for the next axis is developed (independently of Phase 2n) — e.g., a regime-conditional R1a variant motivated by Phase 2m's regime-decomposition evidence; an R1b regime-classifier-driven bias rule; or R2 pullback-entry logic with a falsifiable hypothesis.
- The operator decides one more execution cycle is worth the framework-discipline investment.
- The hypothesis is single-axis, sub-parameters committed singularly per Phase 2j-style pre-commitment, and does not violate Phase 2i §1.7.3 locks.

### H.3 Switch from Option A to Option C / D (later paper/shadow planning)

- Operator independently lifts the "do not start paper/shadow planning yet" restriction.
- For C (R3-only): operator decides R3's evidence is sufficient to begin operational scaffolding, accepting that absolute expR is still negative.
- For D (R1a+R3): operator independently relaxes §1.7.3 to admit ETH-specific research deployment.

### H.4 Switch from Option A to Option E (stop family, new family)

- A future structural-redesign attempt produces a clean §10.3 disqualification on BTC (a third-strike rule, even though the framework has no formal three-strike rule).
- Operator independently decides the absolute-edge gap (expR remains negative even after R3 and R1a+R3) is too large to close from within this family.
- An evidence-grounded alternative-family hypothesis is developed (e.g., funding-rate arbitrage with a credible edge mechanism) that compatibly tests on the same v002 datasets.

### H.5 Switch to Phase 4 (operational infrastructure) ahead of any 2o strategy work

- Operator independently lifts the Phase 4 deferral.
- Decision is that operational scaffolding is independently valuable regardless of which strategy candidate eventually deploys.

### H.6 Stop point (no further phase)

- Operator decides to pause strategy work entirely (e.g., for a different operational concern, security review, or external timing constraint).
- Discovery of a documentation inconsistency in prior phase records that requires a docs-only correction phase before any further strategy work.

---

## I. Next-phase options (Phase 2o variants)

Each option assumes Phase 2n closes with operator approval. Phase 2n itself does not start any of these.

### Option A — Phase 2o: docs-only targeted asymmetry review / analysis planning

**What it would look like.** Mirrors Phase 2n structure: docs-only, no code, no runs. Examines the R1a BTC/ETH asymmetry in depth using Phase 2m's already-committed run artifacts. Outputs a written analysis memo (BTC R1a F2 / F4 walkthrough; per-regime BTC degradation root cause; hypothesis generation for a regime-conditional R1a-prime variant if one is justifiable). Could escalate to a future execution phase if the diagnostic surfaces an actionable hypothesis; could close out as docs-only if not.

**Pros.** Directly attacks the most-informative anomaly. Cheap. Preserves discipline. Could yield a high-EVI next-axis hypothesis without any execution-phase commitment.

**Cons.** Treadmill risk. Might produce no actionable hypothesis. Adds another phase to the path before any operational readiness.

**Wasted-effort risk.** MEDIUM-LOW (informative regardless).

**EVI.** MEDIUM-HIGH if operator wants to deepen the family's diagnosis before consolidating or shifting.

### Option B — Phase 2o: new structural execution phase

**What it would look like.** Skip the analysis review and directly execute one of the Phase 2i-deferred candidates: R1b (regime-conditional bias) or R2 (pullback entry). Same Phase 2j / 2k / 2l / 2m discipline: single-axis structural change, sub-parameters committed singularly, H0 anchor + R3 locked exit baseline (per Phase 2m's R1a-on-R3 precedent).

**Pros.** If a high-EVI hypothesis exists, this is the fastest path to evidence. Preserves the framework discipline.

**Cons.** Phase 2i explicitly excluded R1b (higher overfitting risk; harder cross-symbol robustness) and R2 (needs new pending-limit-fill backtester logic; lower trade count makes per-fold consistency harder). The reasons that justified excluding them haven't changed. **Premature without first reviewing the Phase 2m asymmetry.** Risk of a third PROMOTE-but-mixed result that doesn't move the consolidation question forward.

**Wasted-effort risk.** MEDIUM-HIGH if invoked without a strong hypothesis.

**EVI.** LOWER than Option A unless an external high-EVI hypothesis is in hand.

### Option C — Phase 2o: later paper/shadow-readiness planning for R3 only

**What it would look like.** A docs-only planning phase that designs the eventual paper/shadow path for R3 alone. Identifies the operational scaffolding required (runtime-mode handling, dry-run adapter, dashboard hooks, alert routing, kill-switch wiring) without starting Phase 4. Frames the gates that paper/shadow would need to clear before any tiny-live work.

**Pros.** Aligns with R3 being the research-leading version. Sets up the eventual research-to-operations transition. Inside the operator's stated v1 BTC-primary scope.

**Cons.** Operator brief explicitly says "do not start paper/shadow planning yet". Premature given expR is still negative. Should be a separate operator decision, not auto-triggered by Phase 2n.

**Wasted-effort risk.** MEDIUM-HIGH if invoked too early.

**EVI.** LOW for strategy question; MEDIUM for operational-readiness if and when paper/shadow becomes appropriate.

### Option D — Phase 2o: later paper/shadow-readiness planning for R1a+R3

**What it would look like.** Same as Option C but for R1a+R3.

**Pros.** Preserves ETH +0.69% V-window signal as deployable.

**Cons.** Conflicts with §1.7.3 BTC-primary lock. R1a+R3 BTC degradation makes this an inappropriate candidate for operational readiness on the live primary. **Effectively unavailable at v1 unless §1.7.3 is independently relaxed.**

**Wasted-effort risk.** HIGH at v1.

**EVI.** LOW within v1's policies.

### Option E — Phase 2o: new strategy-family research planning

**What it would look like.** A docs-only planning phase that surveys candidate non-breakout strategy families and pre-commits a falsifiable next-family hypothesis (e.g., mean-reversion in low-vol regimes, funding-rate arbitrage, cross-symbol relative momentum). Phase 2o itself does not start the new family — it plans the eventual transition.

**Pros.** Acknowledges that absolute-aggregate edge is still weak. Frees research capacity for a fresh approach if the operator decides the family has been adequately characterized.

**Cons.** **Premature given the family has produced two PROMOTEs.** The Phase 2h §11.1 stopping rule (clean negative required) is not met. Throws away the structural-redesign research stack.

**Wasted-effort risk.** HIGH if invoked now.

**EVI.** LOW now; HIGHER only after a third structural-redesign attempt produces a clean negative.

### I.6 Next-phase options summary

| Option | Description                                           | Pros                              | Cons                                    | Wasted-effort risk | EVI         |
|--------|-------------------------------------------------------|-----------------------------------|-----------------------------------------|--------------------|-------------|
| A      | Phase 2o: docs-only asymmetry review / analysis       | Targets most-informative anomaly  | Treadmill risk; might not yield hypothesis | MEDIUM-LOW         | MEDIUM-HIGH |
| B      | Phase 2o: new structural execution (R1b, R2, R1a-prime) | Fast path to evidence if hypothesis exists | Premature; risk of mixed-result repeat | MEDIUM-HIGH        | LOWER       |
| C      | Phase 2o: paper/shadow planning for R3 only           | Aligns with R3 being leading       | Premature; deferred per restriction      | MEDIUM-HIGH        | LOW (strategy) |
| D      | Phase 2o: paper/shadow planning for R1a+R3            | Preserves ETH signal               | Conflicts with §1.7.3; deferred           | HIGH               | LOW          |
| E      | Phase 2o: new strategy-family research planning        | Frees capacity                    | Premature; throws away PROMOTE evidence  | HIGH               | LOW now      |

**Recommended Phase 2o:** Option A (docs-only asymmetry review / analysis planning) is the natural next step under the primary recommendation. If the operator chooses Phase 2n's Option A primary recommendation, Phase 2o Option A is the disciplined "deepen-before-deciding" continuation. If the operator chooses a different Phase 2n direction (e.g., immediate execution), Phase 2o Option B becomes available; the others remain effectively unavailable at v1 unless an independent operator-policy change occurs.

---

## J. Explicit non-proposal list

Phase 2n explicitly does NOT:

- Run new backtests, runs, or variants.
- Add a new redesign candidate beyond H0 / R3 / R1a+R3.
- Change any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold.
- Re-rank Phase 2g / 2l / 2m results.
- Change any committed R3 sub-parameter value (R-target stays at 2.0; time-stop stays at 8).
- Change any committed R1a sub-parameter value (X stays at 25; N stays at 200).
- Quietly replace H0 as the formal framework anchor.
- Quietly declare R1a+R3 the new universal winner.
- Start Phase 4 (runtime / state / persistence).
- Start paper/shadow-readiness planning.
- Start tiny-live-readiness planning.
- Declare any candidate live-ready.
- Edit `docs/12-roadmap/technical-debt-register.md` (operator restriction).
- Edit the implementation-ambiguity log.
- Touch any source file, test file, script, dataset, or manifest.
- Enable MCP, create `.mcp.json`, or enable Graphify.
- Request, create, or use any production Binance credentials.
- Add exchange-write capability of any kind.
- Download new market data.
- Call Binance APIs (authenticated or public).
- Push the Phase 2n branch to origin (deferred to operator).

---

**End of Phase 2n strategy-review memo.** Sections A–J complete. Threshold preservation enforced. H0 anchor preserved. Phase 2m mixed-promote framing preserved. R3 designated as research-leading; R1a+R3 designated as promoted-but-non-leading branch. No code changes, no runs, no new evidence — judgement and planning only. Awaiting operator/ChatGPT Gate 2 review.
