# Phase 2p — Consolidation at R3 Baseline Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL verdict, preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7.3 project-level locks (H0 anchor; ≤ 2 carry-forward; BTCUSDT primary); Phase 2j memo §C (R1a spec) + §D (R3 spec); Phase 2k Gate 1 plan; Phase 2l comparison report (R3 PROMOTE); Phase 2m comparison report (R1a+R3 formal-but-mixed PROMOTE); Phase 2n strategy-review memo (R3 = research-leading; R1a+R3 = promoted-but-non-leading); Phase 2o asymmetry-review memo (asymmetry diagnosis; F.3 R1a-as-research-evidence framing); Phase 2p operator-approved brief.

**Phase:** 2p — Consolidation at R3 Baseline (Option A; docs-only).
**Branch:** `phase-2p/r3-baseline-consolidation`.
**Memo date:** 2026-04-27 UTC.

**Status:** Consolidation recorded. R3 designated as the formal baseline-of-record. R1a designated as retained-for-future-hypothesis-planning research evidence (not the current default / deployable path). Execution paused. Readiness planning (paper/shadow / Phase 4) remains deferred. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## A. Executive summary

### A.1 What Phase 2p does

Phase 2p is a short docs-only consolidation phase. It formalizes three things on the project record:

1. **R3 is the baseline-of-record for any future family work.** Locked sub-parameters: `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`. Same-bar priority STOP > TAKE_PROFIT > TIME_STOP. Setup predicate `RANGE_BASED` (H0 default; not R1a). All other Phase 2j memo §D invariants preserved.
2. **R1a is retained-for-future-hypothesis-planning research evidence.** Not closed (so the operator may revive it via a future docs-only spec-writing phase if a regime-conditional R1a-prime hypothesis is independently developed). Not the current default / deployable path. The Phase 2m artifacts on disk and the committed comparison report stay as historical evidence under the unchanged framework.
3. **Future-resumption criteria are recorded explicitly.** What would need to happen before another execution phase is justified, before paper/shadow planning is justified later, before Phase 4 becomes appropriate later, and before family abandonment becomes appropriate later — all enumerated so any future decision starts from a clear baseline.

### A.2 Why this is a consolidation phase

Three docs-only phases (2n family-level review; 2o asymmetry diagnosis; 2p this consolidation) follow Phase 2m's mixed-PROMOTE result. Each docs-only phase tightens the strategic interpretation: 2n named R3 the research-leading version and R1a+R3 the promoted-but-non-leading branch; 2o diagnosed the BTC/ETH asymmetry as a fact about market structure (not a fixable rule defect) and recommended pausing execution; 2p makes the consolidation concrete on the project record so future phases (whether planning or operational) start from an unambiguous baseline.

Without this consolidation, future phase entries would either (a) re-litigate R3-vs-R1a+R3 framing every time, (b) silently drift back toward execution momentum, or (c) silently drift toward readiness planning. The consolidation prevents both drifts.

### A.3 Plain-English current-state summary

The locked v1 breakout family has now been tested across one parametric wave (Phase 2g; REJECT ALL) and two structural redesigns (Phase 2l R3, broad PROMOTE; Phase 2m R1a+R3, formal-but-mixed PROMOTE). The framework discipline held throughout.

Where the project stands today:

- **R3 alone is the strongest evidence the project has produced.** Broad-based PROMOTE on R; direction-of-improvement holds on V; all 6 regime-symbol cells improve; 4/5 BTC folds and 3/5 ETH folds beat H0; clean implementation; robust to slippage and stop-trigger sensitivity.
- **R1a+R3 produced unique evidence that R3 alone did not.** ETH V-window first-ever positive netPct (+0.69%); ETH low_vol PF 1.353 (first cell with positive expR AND PF > 1); ETH shorts PF 1.906 (strongest direction-symbol cell ever). But R1a hurts BTC (Δexp_R3 −0.180 R; V-window 0% WR / 4 trades). R1a's compression-selection is mechanically correct (100% of entries at percentile ≤ 25%); the asymmetry is in post-compression follow-through, which differs by symbol.
- **Absolute aggregate edge has not materialized.** Even R3's R-window expR is −0.240 BTC / −0.351 ETH (still negative). The framework has produced two PROMOTEs but no positive-aggregate-expR result outside the small-sample R1a+R3 ETH V cell.
- **The family is alive but not validated.** Two PROMOTEs is structural-redesign-responsiveness; absolute-edge has not been demonstrated.
- **Live-readiness, paper/shadow, and Phase 4 all remain deferred** per operator policy.

Phase 2p closes the active research cycle on this picture by formalizing R3 as the baseline-of-record and R1a as retained research evidence. The next phase, whenever and whatever it is, starts from this baseline.

---

## B. Fixed evidence recap

(All numbers quoted from already-committed reports. No re-derivation. No re-running.)

### B.1 Why H0 remains the formal anchor

Phase 2i §1.7.3 established H0 (the locked Phase 2e baseline) as the **sole** comparison anchor for all §10.3 / §10.4 / §11.3 / §11.4 / §11.6 evaluations. This was not a casual choice — it was a deliberate anti-overfitting guard: every successive structural-redesign candidate must clear thresholds against the same descriptive baseline, never against a previous successful candidate.

The discipline has held through three execution phases:

- Phase 2g Wave-1 (parametric): all four variants tested against H0; REJECT ALL.
- Phase 2l R3 (structural exit): tested against H0; PROMOTE.
- Phase 2m R1a+R3 (structural setup on top of R3): **tested against H0** (per Phase 2m §4); PROMOTE; the R3-anchor view in §5 was explicitly labeled supplemental-only.

Phase 2p preserves H0 as the formal anchor unchanged. Any future execution phase must compare to H0; comparing to R3 (or R1a+R3) is supplemental analysis, not governing.

### B.2 Why R3 is the research-leading baseline

R3 (Phase 2j memo §D — fixed-R take-profit at +2.0 R + unconditional time-stop at 8 bars; protective stop never moved intra-trade) cleared the Phase 2f §10.3 framework cleanly:

| Metric        | BTC                      | ETH                      |
|---------------|--------------------------|--------------------------|
| Trades        | 33 (vs H0 33; same)      | 33 (vs H0 33; same)       |
| WR            | 42.42% (vs H0 30.30%)    | 33.33% (vs H0 21.21%)     |
| expR          | **−0.240** (vs H0 −0.459)| **−0.351** (vs H0 −0.475)|
| PF            | **0.560** (vs H0 0.255)  | **0.474** (vs H0 0.321)  |
| netPct        | −1.77% (vs H0 −3.39%)    | −2.61% (vs H0 −3.53%)    |
| maxDD         | −2.16% (vs H0 −3.67%)    | −3.65% (vs H0 −4.13%)    |

§10.3 verdict: **PROMOTE** on both BTC (§10.3.a + §10.3.c) and ETH (§10.3.a + §10.3.c). |maxDD| ratios 0.588× BTC / 0.882× ETH (well below 1.5× veto). Per-fold (5 rolling, GAP-036): R3 beats H0 in **4/5** BTC folds and **3/5** ETH folds. Per-regime (realized 1h-vol): R3 improves expR in **all 6** regime-symbol cells. V-window confirms direction-of-improvement: H0 BTC −0.313 → R3 BTC −0.287; H0 ETH −0.174 → R3 ETH −0.093 (WR 28.57% → 42.86%).

R3's case is the strongest the project has produced. Phase 2n committed R3 as the **research-leading baseline**; Phase 2o §G.2 explicitly stated the asymmetry **increases** confidence in R3; Phase 2p formalizes R3 as the **baseline-of-record**.

### B.3 Why R1a+R3 is preserved as research evidence but not the current default path

R1a (Phase 2j memo §C — volatility-percentile setup with X = 25 / N = 200) on top of the locked R3 exit baseline cleared the framework formally but with strategically mixed evidence:

| Metric        | BTC R1a+R3               | ETH R1a+R3               |
|---------------|--------------------------|--------------------------|
| Trades        | 22 (vs H0 33; vs R3 33)   | 23 (vs H0 33; vs R3 33)   |
| expR          | −0.420 (vs H0 −0.459 / R3 −0.240) | −0.114 (vs H0 −0.475 / R3 −0.351) |
| PF            | 0.355 (vs H0 0.255 / R3 0.560) | 0.833 (vs H0 0.321 / R3 0.474) |
| netPct        | −2.07%                   | −0.59%                   |
| maxDD         | −2.33%                   | −2.96%                   |

H0-anchor §10.3 verdict: **PROMOTE.** BTC clears §10.3.c **only** (Δexp +0.039 R below §10.3.a's +0.10 threshold). ETH clears §10.3.a + §10.3.c. No §10.3 disqualification floor; no §10.4 (Δn < 0); §11.4 satisfied.

But the R3-anchor view is descriptively asymmetric: BTC Δexp_R3 **−0.180** / ΔPF_R3 **−0.205**; ETH Δexp_R3 **+0.237** / ΔPF_R3 **+0.359**. V-window amplifies: ETH **first positive netPct ever** (+0.69%, expR +0.386, PF 2.222); BTC severely degraded (4 trades, 0% WR, expR −0.990).

R1a's compression-selection is mechanically correct (100% of filled entries at ATR percentile ≤ 25%, exactly per Phase 2j §C.5 spec). The asymmetry is in post-compression follow-through, which differs by symbol — Phase 2o §C diagnosis converged on this being a fact about underlying market structure (symbol-specific + directional-bias interaction), not a fixable R1a defect.

The §1.7.3 BTCUSDT-primary lock makes a deployable variant that hurts BTC ineligible for v1. R1a stays alive as research evidence, not as the current default / deployable path.

### B.4 What the family has demonstrated so far

- **Structural-redesign responsiveness.** Two of three structural-redesign experiments PROMOTED under unchanged thresholds. The family responds to structural work in a measurable, framework-disciplined way.
- **Edge concentration on ETH under R1a+R3.** First positive-netPct V-window result the project has ever produced (R1a+R3 ETH V netPct +0.69%, PF 2.222). Specific to ETH, specific to bottom-quartile compression bars, specific to short side; not yet generalized to BTC.
- **Broad-based improvement under R3 alone.** All 6 regime-symbol cells improve; 4/5 BTC folds beat H0; first-ever positive BTC fold expR (F2 +0.015, F3 +0.100); V-window confirms direction-of-improvement.
- **Implementation cleanliness.** H0 + R3 controls reproduce locked baselines bit-for-bit across phases. Zero TRAILING_BREACH / STAGNATION leakage in any R3-or-R1a+R3 trade log. R1a's 100% in-bottom-quartile diagnostic confirms predicate correctness.
- **Framework discipline holds.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds applied without post-hoc adjustment; H0 anchor preserved; Wave-1 historical evidence preserved.

### B.5 What the family has NOT demonstrated

- **Absolute positive aggregate expR on R.** R3 BTC −0.240 / ETH −0.351; R1a+R3 BTC −0.420 / ETH −0.114. All four cells negative on the 36-month research window.
- **Universal cross-symbol PROMOTE that improves both BTC and ETH against R3.** R3 alone did this vs H0; R1a+R3 did not do this vs R3 (asymmetric — helps ETH, hurts BTC).
- **Out-of-sample positive netPct on BTC.** R3 BTC V −0.51% / R1a+R3 BTC V −0.88%. ETH has produced +0.69% V netPct under R1a+R3, but BTC has not.
- **Regime-conditional or symbol-conditional rule that recovers BTC under R1a's filter.** Phase 2o §F.1 noted this as a hypothesis worth specifying via a future docs-only phase but not yet specified.
- **Live-readiness evidence of any kind.** No paper/shadow runs; no tiny-live evidence; no operational scaffolding (Phase 4 deferred).

### B.6 What is now known and what is not

**Known:**
- R3's structural improvement is broad-based and robust.
- R1a's marginal contribution on top of R3 is symbol-asymmetric.
- The asymmetry is a fact about market-structure × strategy interaction, not an implementation bug.
- The framework is informative on small samples and disciplined enough to distinguish R3's clean PROMOTE from R1a+R3's mixed PROMOTE.

**Not known:**
- Whether a different structural redesign (regime-conditional R1a-prime; R1b regime classifier; R2 pullback entry) would produce a clean cross-symbol improvement.
- Whether the family's absolute-edge gap is closeable from within the breakout-continuation thesis at all.
- Whether the asymmetry would persist on extended out-of-sample data (no V-window successor available without new data, which Phase 2p does not authorize).
- Whether a different cost / fee / slippage assumption space (e.g., professional-grade fee tier) would change the absolute-aggregate picture.

---

## C. Consolidated baseline-of-record

### C.1 R3 is the baseline-of-record for future family work

**R3 alone** — not R1a+R3, not H0 — is now the formal baseline-of-record for any future structural-redesign work or operational-readiness planning the operator authorizes. This means:

- Any future structural-redesign hypothesis is specified as "X on top of R3" (mirroring how R1a was specified on top of R3 in Phase 2j memo §C).
- Any future operational-readiness scaffolding (whenever Phase 4 / paper-shadow restrictions are lifted) targets R3 as the deployable variant.
- Any future H0 control re-run continues to use H0 (locked Phase 2e baseline) as the framework anchor; R3 is the candidate-of-record running alongside H0.

### C.2 Exact locked R3 definition

The R3 baseline-of-record is locked at the exact Phase 2j memo §D + Phase 2l-implemented values:

```yaml
strategy_variant:
  # Setup predicate (H0 default; not R1a):
  setup_predicate_kind:        RANGE_BASED
  # H0 setup-validity rule preserved (range_width <= 1.75 * ATR(20) AND
  # |close[-1] - open[-8]| <= 0.35 * range_width).
  setup_size:                  8

  # Trigger (H0 default):
  expansion_atr_mult:          1.0

  # Bias (H0 default):
  ema_fast:                    50
  ema_slow:                    200

  # Exit philosophy (R3):
  exit_kind:                   FIXED_R_TIME_STOP
  exit_r_target:               2.0     # +2 R take-profit
  exit_time_stop_bars:         8       # unconditional time-stop horizon

  # break_even_r is unused under FIXED_R_TIME_STOP but retained at H0 default
  # for explicitness:
  break_even_r:                1.5

  # R1a sub-parameters retained at default (used only if a future operator-
  # approved phase enables setup_predicate_kind=VOLATILITY_PERCENTILE):
  setup_percentile_threshold:  25
  setup_percentile_lookback:   200
```

In the codebase: `V1BreakoutConfig(exit_kind=ExitKind.FIXED_R_TIME_STOP, exit_r_target=2.0, exit_time_stop_bars=8)` (all other fields at H0 defaults). This is what Phase 2l locked in and Phase 2m carried as the locked exit baseline.

**Same-bar priority:** STOP > TAKE_PROFIT > TIME_STOP. Enforced two-fold:
- STOP > TAKE_PROFIT is structural in the engine: `evaluate_stop_hit` runs before management; if a stop is hit the bar is short-circuited via `continue` and management never observes a take-profit on a stopped bar.
- TAKE_PROFIT > TIME_STOP is enforced inside `TradeManagement._fixed_r_time_stop_decision`: take-profit predicate checked first; only if it does not fire is the time-stop predicate evaluated.

**Other R3 invariants:**
- The protective stop is the initial structural stop computed at entry; **never moved intra-trade**.
- No break-even logic, no trailing logic, no Stage 3 / 4 / 5 transitions.
- All other entry pipeline (setup, bias, trigger, stop-distance filter, sizing, re-entry lockout) at H0 defaults.

### C.3 What this means operationally for future research phases

- **Future structural-redesign hypotheses.** A new candidate is specified as "X on top of R3" — keeping R3's exit machinery locked while changing one structural axis (e.g., regime-conditional R1a-prime; R1b; R2). The candidate is compared to H0 (governing) and to R3 (descriptive supplemental). The Phase 2k Gate 1 / Phase 2j-style spec discipline applies unchanged.
- **Future H0 control re-runs.** Continue to re-run H0 alongside any candidate as a bit-for-bit preservation regression. The H0 R-window numbers (BTC 33 / 30.30% / −0.459 / 0.255 / −3.39% / −3.67%; ETH 33 / 21.21% / −0.475 / 0.321 / −3.53% / −4.13%) are the locked reference.
- **Future R3 control re-runs.** Continue to re-run R3 alongside any candidate. The R3 R-window numbers (BTC 33 / 42.42% / −0.240 / 0.560 / −1.77% / −2.16%; ETH 33 / 33.33% / −0.351 / 0.474 / −2.61% / −3.65%) are the locked reference for descriptive R3-anchor analysis.
- **Future strategy-spec docs.** When the operator authorizes Phase 4 or paper/shadow planning, the deployable variant is R3-as-defined-above. Docs / tests / runtime configs for that planning phase reference this exact spec.

### C.4 What this does NOT mean

- **R3 is not a live-ready strategy.** Its R-window expR is still negative (−0.240 BTC / −0.351 ETH). Baseline-of-record means "the version we operate against in research / planning"; it does not mean "approved for capital exposure".
- **R3 does not promote past Phase 2i §1.7.3 locks.** BTCUSDT remains the v1 live primary; ETHUSDT remains research/comparison only; one-position max; 0.25% risk; 2× leverage; mark-price stops; v002 datasets.
- **R3 is not the framework anchor.** H0 remains the sole §10.3 / §10.4 anchor. R3 is the candidate-of-record; H0 is the baseline-anchor. These are different roles.
- **R3 baseline-of-record does not preclude future R3-replacement.** If a future structural-redesign candidate cleanly improves on R3 across both BTC and ETH (analogous to how R3 cleanly improved on H0), the operator may at that point promote it to a new baseline-of-record. Phase 2p locks R3 as the *current* baseline-of-record; future evidence may move that.

---

## D. Status of R1a

### D.1 R1a is part of the project's research evidence base

The Phase 2j memo §C R1a spec, the Phase 2m comparison report, the Phase 2m run artifacts under `data/derived/backtests/phase-2m-r1a-*/` (git-ignored but on disk), and the Phase 2n / 2o / 2p documentation all preserve R1a as committed historical evidence. The §10.3 PROMOTE verdict on R1a+R3 stands.

### D.2 R1a is not the current default / deployable path

- Phase 2n committed R1a+R3 = **promoted but non-leading branch**.
- Phase 2o committed R1a+R3 = **useful research evidence; not the current deployable / default path**.
- Phase 2p committs R1a as **retained-for-future-hypothesis-planning** (chosen and justified in §D.4 below).

In particular, R1a is not the variant the project would deploy under any future paper/shadow / tiny-live / live planning, because its BTC asymmetric degradation conflicts with the §1.7.3 BTCUSDT-primary lock.

### D.3 What findings from R1a are worth preserving

- **R1a's percentile-predicate implementation works exactly as designed.** 100% of filled R1a entries at ATR percentile ≤ 25%. The Phase 2j §C.5 spec is implementable and the implementation is correct. This is reusable for any future regime-conditional R1a-prime variant.
- **Compression filtering does identify a real signal on ETH.** R1a+R3 ETH V netPct **+0.69%** (8 trades, 62.5% WR, expR +0.386, PF 2.222) — first-ever positive-netPct V-window. R1a+R3 ETH low_vol R-window expR **+0.281** / PF **1.353** — first cell with positive expR AND PF > 1. R1a+R3 ETH shorts +0.387 R / PF 1.906 — strongest direction-symbol cell ever observed. Whatever R1a is doing, it is finding real ETH signal.
- **Compression filtering on BTC selects bars whose post-compression follow-through is muted.** R1a+R3 BTC R-window Δexp_R3 −0.180 R; V-window 4 trades / 0% WR / expR −0.990. The filter is mechanically correct on BTC too, but the bars it selects don't follow through. This is a market-structure observation, not an R1a defect.
- **Phase 2o §C diagnosis converged on symbol-specific market behavior + directional-bias interaction as the most-supported explanations.** The asymmetry is in post-compression follow-through, not in compression definition or selection geometry.
- **The funnel attribution stays interpretable** for both predicates: R1a's predicate fires more setups (~3.75× H0's `valid_setup_windows_detected`), but the same `rejected_no_valid_setup` bucket continues to absorb predicate failures. No bucket explosion.

### D.4 What findings from R1a should NOT be over-generalized

- **The ETH +0.69% V-window result is a small sample.** 8 trades. One single very large MFE trade (max +8.688 R) skews the distribution. Treating this as a deployable-edge claim would be over-generalization.
- **The BTC degradation is also a small sample on V** (4 trades). 0% WR on n = 4 is unambiguous in direction but the magnitude estimate is fragile.
- **The "ETH-favorable specialty filter" framing should not be operationalized.** §1.7.3 keeps ETHUSDT as research/comparison only. Treating R1a as "the variant we'd deploy on ETH" requires an operator-policy change beyond Phase 2p's scope.
- **The "regime-conditional variant might salvage BTC" hypothesis is undeveloped.** Phase 2o §F.1 noted high overfitting risk; any future regime-conditional R1a-prime would need a falsifiable spec with sub-parameters committed singularly per Phase 2j-style discipline.

### D.5 R1a is best thought of as: retained-for-future-hypothesis-planning

The three framings the operator brief enumerates:

| Framing                                       | Compatible with the evidence?                                   | Phase 2p choice |
|-----------------------------------------------|-----------------------------------------------------------------|-----------------|
| **closed**                                    | Permanently abandons R1a; closes the regime-conditional R1a-prime door | NO               |
| **dormant**                                   | Set aside; could be revived but no active planning                  | NEAR-MISS        |
| **retained-for-future-hypothesis-planning**   | R1a stays alive specifically as a candidate axis for future docs-only spec-writing if a regime-conditional R1a-prime hypothesis is independently developed | **CHOSEN**       |

**Justification for the chosen framing.** Phase 2o §F.3 framed R1a abandonment as "R1a as deployable variant is dropped; R1a as research evidence remains" — and §F.1 noted regime-conditional R1a-prime as a hypothesis worth specifying via a future docs-only phase. Phase 2o §H.2 (fallback recommendation) explicitly preserved Phase 2p Option B (docs-only hypothesis-planning) as an open path.

The "closed" framing would prematurely close a research door without an evidence-grounded reason — Phase 2o concluded R1a's contribution is symbol-asymmetric and regime-localized, which is informative; closing the door without specifying whether a regime-conditional variant could capture the ETH benefit while avoiding the BTC penalty is a stronger statement than the evidence supports.

The "dormant" framing is close but slightly weaker: it implies the option is set aside without explicit conditions for revival. The current evidence supports a more specific framing — R1a stays alive specifically for the *regime-conditional R1a-prime hypothesis-planning* case identified in Phase 2o §F.1, not for arbitrary revival.

The "retained-for-future-hypothesis-planning" framing is the precise framing that matches: R1a is alive **for a specific future use** (regime-conditional R1a-prime spec writing, if independently authorized), **not** as an active deployable variant, **not** as a default path, and **not** as something Phase 2p itself plans.

---

## E. Family-level consolidation judgment

### E.1 What the family has earned

- **The right to be treated as actively researched, not abandoned.** Two PROMOTEs is meaningful framework evidence. Phase 2h §11.1 stopping rule (clean negative required) is not met; abandoning the family at this point would discard accumulated evidence without justification.
- **R3 as the locked exit-philosophy baseline.** Phase 2l's broad-based PROMOTE was clean and robust. R3 is the most-validated structural improvement the project has produced.
- **Recognition that compression-precedes-breakout is real on ETH (under R1a+R3).** The first positive-netPct V-window is evidence the family can produce out-of-sample positive equity on at least one symbol under at least one redesign combination. Whether that translates to BTC, or to live deployment, or to extended observation windows, is unknown.

### E.2 What the family still lacks

- **Cross-symbol absolute positive expR.** No cell on R has positive expR for both symbols simultaneously under any candidate.
- **Out-of-sample positive netPct on BTC.** R3 BTC V −0.51%; R1a+R3 BTC V −0.88%. Improvement vs H0 V (−0.56%) is marginal at best on BTC.
- **A clean R3-replacement candidate.** R1a+R3 was the project's attempt at one; it failed to be a clean replacement (asymmetric on BTC).
- **Evidence that the family's absolute-edge gap is closeable.** Even R3 is −0.240 / −0.351 expR on R; closing that gap to positive territory (or accepting that the framework's threshold-based PROMOTEs are sufficient even without absolute positive edge for some specific operational use case) requires operator policy clarity that Phase 2p does not provide.

### E.3 Why immediate further execution is paused

Phase 2o §H.1 articulated the case in detail. Summarizing here:

- The most-supported asymmetry explanations (Phase 2o §C.1 symbol-specific market behavior; §C.5 directional-bias interaction) point to **facts about market structure**, not to fixable rule defects.
- Running a third structural-redesign execution immediately (e.g., R1b, R2, or R1a-prime) without first developing the spec docs-only would risk treadmill behaviour: another mixed result that doesn't move the consolidation question forward.
- Paper/shadow / Phase 4 readiness work is operator-policy-deferred; advancing toward it without operator policy change would violate explicit operator restrictions.
- The R3 baseline is itself a useful research consolidation point — characterized, robust, locked. Future research starts here.

### E.4 Why the project is NOT abandoning the family

- Two of three structural-redesign experiments PROMOTED. Family responds to structural work.
- R3 alone is the strongest result the project has produced. Not "ceiling"; not "dead end".
- R1a+R3 ETH V-window first positive netPct is unprecedented evidence the family hasn't generated before. Real signal exists on at least one symbol-redesign combination.
- The Phase 2i-deferred candidates (R1b regime-conditional bias, R2 pullback entry) have not been tested. Calling the family closed without testing these would be premature.
- The Phase 2h §11.1 stopping rule (paraphrased: "abandon a family only when structural redesign has been honestly tried with a falsifiable hypothesis and produced its own clean negative") is not met. Two PROMOTEs is the opposite of a clean negative.

### E.5 Why the project is also NOT advancing toward readiness yet

- Operator policy explicitly defers paper/shadow planning, tiny-live planning, and Phase 4. Phase 2p does not propose changing that policy.
- Even R3's R-window expR is still negative on aggregate (−0.240 BTC / −0.351 ETH). Operationalizing a strategy with negative aggregate expectancy on the BTC live primary symbol — even at 0.25% risk and 2× leverage caps — would be a meaningful policy decision that requires operator-level deliberation beyond Phase 2p's scope.
- The implementation-correctness work, the dataset-discipline work, the framework-discipline work, and the research-baseline work are all in good shape. The blocker for readiness is **strategy-edge confidence**, not infrastructure or process. Phase 2p does not produce new strategy-edge evidence; it consolidates the evidence that exists.

The right framing: **the project is in research-pause-with-baseline-locked**, not in abandoned-family or in advancing-toward-deployment. Future operator decisions can move it in any direction from this consolidated baseline.

---

## F. Future-resumption criteria

This section defines, explicitly, what would need to happen before each of the four scenarios is justified. These are pre-conditions; meeting them produces eligibility for an operator decision, not automatic phase-start.

### F.1 Pre-conditions for another execution phase

A future execution phase (Phase 2q or later) is justified when **all** of:

1. **A specific falsifiable hypothesis is in hand.** Either the regime-conditional R1a-prime variant noted in Phase 2o §F.1 with a Phase 2j-style §C-equivalent full spec; or the Phase 2i-deferred R1b (regime-conditional bias) or R2 (pullback entry) with renewed evidence-grounded justification; or another candidate not yet enumerated.
2. **The hypothesis is single-axis structural.** Per Phase 2i §1.7.1 binding test: rule-shape change; new input domain; not parameter-tuning under another label.
3. **Sub-parameters are committed singularly** before any execution. Per Phase 2f §11.3.5 binding rule.
4. **Falsifiable hypothesis is recorded** with §10.3 / §10.4 disqualification thresholds preserved unchanged.
5. **Operator authorizes execution Gate 1.** Standard process — separate operator decision after the docs-only spec phase.

If those pre-conditions are met, the execution phase's structure mirrors Phase 2k / 2l / 2m: H0 control re-run, R3 control re-run, candidate run; same v002 datasets; same MEDIUM slippage / MARK_PRICE default + sensitivity passes. The candidate is "X on top of R3" (R3 is the locked exit baseline going forward).

### F.2 Pre-conditions for paper/shadow-readiness planning

Future paper/shadow-readiness planning (deferred per current operator policy) becomes appropriate when **all** of:

1. **Operator independently lifts the paper/shadow restriction.** This is a policy decision, not an evidence question — Phase 2p does not propose lifting it. The operator may choose to lift it based on accumulated R3 evidence, or hold it until additional evidence appears.
2. **The candidate to deploy is clearly identified.** Under current evidence, the only viable candidate is R3 (R1a+R3 conflicts with §1.7.3 due to BTC asymmetry). If a future structural-redesign produces a cleaner R3-replacement, that candidate becomes available.
3. **An honest expectation about what paper/shadow can demonstrate at expR < 0 is recorded.** Paper/shadow on a candidate with negative aggregate expR is observation-only — it cannot demonstrate live readiness; it can only demonstrate operational reliability. Whether that's worth the operational investment is an operator decision.
4. **Paper/shadow scope is defined.** Symbols (BTCUSDT primary; ETHUSDT comparison-only per §1.7.3); duration; success criteria; failure-stop criteria.
5. **The operational scaffolding (Phase 4-equivalent) is at least partially in place** OR the operator accepts that paper/shadow at small operational scale precedes Phase 4 work.

### F.3 Pre-conditions for Phase 4 (runtime / state / persistence)

Phase 4 (deferred per current operator policy) becomes appropriate when **either**:

1. **Operator independently lifts the Phase 4 deferral** based on operational-readiness independence from strategy-edge confirmation. The operator may choose to begin operational scaffolding on the strength of R3 alone, or may continue to defer until additional strategy-edge evidence appears. This is a policy decision.
2. **Strategy-edge evidence reaches a level the operator independently judges sufficient for parallel operational scaffolding.** E.g., a future structural-redesign produces clean cross-symbol R3-replacement evidence with positive aggregate expR.

In either path, Phase 4 starts as a separately-gated phase with its own Gate 1 / Gate 2 / runnable checkpoint structure per `docs/00-meta/ai-coding-handoff.md` Phase 4 spec.

### F.4 Pre-conditions for family abandonment

Family abandonment (shifting to a non-breakout strategy family) becomes appropriate when **either**:

1. **A future structural-redesign attempt produces a clean §10.3 disqualification on BTC.** This would be the third strike in the structural-redesign program (after R3 PROMOTE and R1a+R3 mixed-PROMOTE). A clean negative would meet the Phase 2h §11.1 stopping rule.
2. **Operator independently decides the absolute-edge gap is too large to close from within this family.** Even after R3 + R1a+R3, R-window expR remains negative; the operator may at any point judge the gap too large and authorize family-shift planning (without an executed third-strike).
3. **An evidence-grounded alternative-family hypothesis emerges with a credible mechanism that compatibly tests on the same v002 datasets.** E.g., funding-rate arbitrage; mean-reversion in low-vol regimes; cross-symbol relative-momentum. The hypothesis must be specifiable with §10.3-style pre-committed thresholds.

Family abandonment, like all other transitions, is an operator-authorized phase with its own Gate 1 / Gate 2 / scope.

---

## G. Recommended next-boundary options

Each option assumes Phase 2p closes with operator approval. Phase 2p itself does not start any of these.

### Option A — No immediate new phase; maintain consolidation state

**What it would look like.** The project pauses without authorizing a successor phase. R3 baseline-of-record stands. R1a stays in retained-for-future-hypothesis-planning state. Future operator decisions resume the path when an evidence-grounded reason or a policy change produces one.

**Pros.** Cheapest. Preserves discipline. Keeps every door open. Aligns with Phase 2p's consolidation purpose.

**Cons.** No active research happens. If the family has more to give, this option delays that.

**Wasted-effort risk.** ZERO.

**EVI.** ZERO for new evidence; HIGH for clarity (Phase 2p is itself the clarity-producing step; further deferred phases preserve that clarity).

### Option B — Future docs-only hypothesis-planning for one specific redesign

**What it would look like.** When the operator independently develops a regime-conditional R1a-prime hypothesis (per Phase 2o §F.1), or revives R1b / R2 with new evidence-grounding, a docs-only Phase 2j-style spec-writing phase produces the full spec. Forces explicit Phase 2i §1.7 binding-test decision before any execution.

**Pros.** Keeps the structural-redesign path alive cleanly. Preserves discipline. If the spec passes the binding test, a future execution Gate 1 becomes available; if not, the operator has documented reason to consolidate further.

**Cons.** Adds a planning phase to the path. If the hypothesis fails the binding test, partial-waste risk (though the documented failure is itself information).

**Wasted-effort risk.** LOW. Mitigated by docs-only scope.

**EVI.** MEDIUM-HIGH if the operator wants to keep the structural-redesign path alive.

### Option C — Future immediate execution of a new redesign

**What it would look like.** Skip the docs-only spec-writing phase and directly authorize an execution phase for one of R1b / R2 / R1a-prime. Same Phase 2k / 2l / 2m discipline.

**Pros.** Fastest path to evidence if a strong hypothesis exists.

**Cons.** **Premature without first developing the spec.** Phase 2i originally excluded R1b and R2 for evidence-grounded reasons; reviving them needs evidence-grounded justification. Without that, this option risks producing another mixed result that doesn't move the consolidation question forward. Conflicts with Phase 2p's consolidation purpose.

**Wasted-effort risk.** HIGH if invoked without a specific spec.

**EVI.** LOW unless an external high-EVI hypothesis is in hand.

### Option D — Later paper/shadow-readiness planning for R3 only

**What it would look like.** Operator independently lifts the paper/shadow restriction; a future docs-only phase designs the paper/shadow path for R3 alone. Operational scaffolding required (runtime modes, dry-run adapter, dashboard hooks, alert routing, kill-switch wiring) is identified without starting Phase 4.

**Pros.** Aligns with R3 being the baseline-of-record. Sets up eventual research-to-operations transition.

**Cons.** Operator policy currently defers paper/shadow. Premature given expR is still negative. Should be a separate operator decision, not auto-triggered by Phase 2p.

**Wasted-effort risk.** MEDIUM-HIGH if invoked too early.

**EVI.** LOW for strategy; MEDIUM for operations if and when appropriate.

### Option E — Later new strategy-family planning

**What it would look like.** Operator independently authorizes shift-of-family planning. A docs-only phase surveys candidate non-breakout families (mean-reversion, funding-rate arbitrage, cross-symbol relative momentum) and pre-commits a falsifiable next-family hypothesis.

**Pros.** Frees research capacity. Acknowledges absolute-edge-gap is still real.

**Cons.** **Premature given two PROMOTEs and an unprecedented ETH V-window result under R1a+R3.** Phase 2h §11.1 stopping rule (clean negative required) not met.

**Wasted-effort risk.** HIGH if invoked now.

**EVI.** LOW now.

### G.6 Options summary

| Option | Description                                              | Pros                                            | Cons                                          | Wasted-effort risk | EVI            |
|--------|----------------------------------------------------------|-------------------------------------------------|-----------------------------------------------|--------------------|----------------|
| A      | No immediate new phase; maintain consolidation state      | Cheapest; preserves discipline; keeps doors open | No active research                             | ZERO               | ZERO (new) / HIGH (clarity) |
| B      | Future docs-only hypothesis-planning                      | Keeps structural-redesign path alive cleanly     | Adds planning phase; partial-waste risk if binding test fails | LOW                | MEDIUM-HIGH    |
| C      | Future immediate execution                                | Fast path to evidence if hypothesis exists      | Premature; risk of mixed-result repeat         | HIGH               | LOW            |
| D      | Later paper/shadow planning for R3 only                   | Aligns with R3 being baseline-of-record         | Deferred per operator policy; premature        | MEDIUM-HIGH        | LOW (strategy) |
| E      | Later new strategy-family planning                         | Frees capacity; fresh approach                  | Premature; throws away PROMOTE evidence       | HIGH               | LOW now        |

---

## H. Recommendation

This recommendation is **provisional and evidence-based, not definitive**. The operator decides.

### H.1 Primary recommendation

**Stay paused after Phase 2p. No immediate new phase.** Maintain the consolidation state defined by this memo: R3 baseline-of-record locked; R1a in retained-for-future-hypothesis-planning state; H0 anchor preserved; framework discipline preserved; operational restrictions (paper/shadow, Phase 4, live-readiness) preserved. The next phase is whatever the operator independently chooses based on the §F.1 / F.2 / F.3 / F.4 pre-conditions.

This is **Option A** of §G.

**Rationale.**

- Phase 2p's purpose is consolidation. Authorizing a successor phase as part of Phase 2p closure would be inconsistent with that purpose — it would either prematurely commit to a research direction (Option B / C) or prematurely commit to an operational direction (Option D) without an evidence-grounded reason.
- Phase 2o §H.1 already recommended Phase 2p Option A specifically because the asymmetry analysis pointed to facts about market structure rather than to fixable rule defects. Phase 2p's role is to make that pause concrete and durable, not to immediately authorize a follow-on phase.
- The §F.1 pre-conditions for resuming execution are clear; the operator can re-enter the research path whenever those pre-conditions are independently met.
- The §F.2 / F.3 pre-conditions for resuming readiness work are clear; the operator can re-enter the operational path whenever those pre-conditions are independently met.
- The §F.4 pre-conditions for family abandonment are clear; the operator can authorize family-shift whenever those pre-conditions are met.

### H.2 Fallback recommendation

If the operator judges that maintaining a stay-paused state without any active path is too inert, **Phase 2q Option B** (docs-only hypothesis-planning for one specific next redesign — most likely a regime-conditional R1a-prime per Phase 2o §F.1) becomes the path. This is **not** a successor phase Phase 2p authorizes by itself; the operator must independently develop the hypothesis grounding before authorizing any spec-writing phase. The fallback simply records that this is the disciplined next research move *if* the operator decides to keep an active path.

### H.3 Explicit answers to the operator's required questions

- **Whether the project should stay paused after 2p:** YES (primary recommendation). No immediate new phase. Consolidation state maintained; Phase 2q (whether planning, operations, or family-shift) is a separate operator-authorized decision.
- **Whether the next likely path is hypothesis-planning or operational planning:** **Hypothesis-planning, IF a path is taken at all.** The operator-policy deferrals on paper/shadow / Phase 4 / live work are explicit; advancing toward operations without policy change would violate those deferrals. A docs-only spec-writing phase for regime-conditional R1a-prime (or for R1b / R2 with renewed grounding) is the natural research-side resumption. The fallback path (Phase 2q Option B) targets exactly this case.
- **Whether R3 remains the baseline-of-record going forward:** YES. R3's locked sub-parameters (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`) are committed singularly per Phase 2j memo §D.6 and are now formally the baseline-of-record. Future structural-redesign hypotheses are specified as "X on top of R3"; future operational-readiness scaffolding (when authorized) targets R3.

### H.4 What the recommendation explicitly does NOT recommend

- **Immediate execution (Option C):** premature without spec.
- **Immediate paper/shadow planning (Option D):** operator restriction explicit; not Phase 2p's place to lift.
- **Immediate family abandonment (Option E):** stopping rule not met.
- **Phase 4 work:** deferred per operator policy.
- **R1a closed (vs retained-for-future-hypothesis-planning):** would prematurely close a research door.
- **R1a as deployable / default path:** §1.7.3 conflict.

---

## I. What would change this recommendation

The recommendation is **provisional**. The following kinds of evidence or operator-policy decisions would justify switching paths:

### I.1 Switch from "stay paused" to "future docs-only hypothesis-planning" (A → B)

- Operator independently develops a falsifiable regime-conditional R1a-prime spec (per Phase 2o §F.1) and wants a docs-only spec-writing phase to formalize it.
- Operator independently revives R1b (regime-conditional bias) or R2 (pullback entry) with new evidence-grounding.
- Operator wants a Phase 2j-style spec-writing phase to clarify whether a specific hypothesis can clear Phase 2i §1.7 binding test before any execution Gate 1.

### I.2 Switch from "stay paused" to "future execution phase" (A → execution after spec)

- Same as I.1 plus: the spec passes the binding test, the operator independently authorizes a Gate 1 plan, and the spec phase produces a candidate ready for execution against H0 + R3 controls.

### I.3 Switch from "R1a retained-for-future-hypothesis-planning" to "R1a closed permanently"

- Operator independently decides §1.7.3 makes R1a (and any R1a-prime variants) permanently undeployable, and the research value is now fully captured by the existing Phase 2m artifacts.
- A future regime-conditional R1a-prime spec is attempted in a docs-only phase, fails Phase 2i §1.7 binding test, and the operator chooses to close the R1a path rather than try further variants.
- A future structural-redesign attempt produces a clean §10.3 disqualification on BTC and the operator chooses to close R1a as part of family-shift planning.

### I.4 Switch from "stay paused" to "later paper/shadow planning for R3" (A → D)

- Operator independently lifts the paper/shadow restriction.
- Operator independently judges R3's evidence sufficient for operational scaffolding work, accepting that R-window expR is still negative.

### I.5 Switch from "stay paused" to "later Phase 4" (A → Phase 4)

- Operator independently lifts the Phase 4 deferral, on the strength of R3 as research-leading baseline.

### I.6 Switch from "stay paused" to "family shift" (A → E)

- A future docs-only hypothesis-planning phase produces a regime-conditional R1a-prime / R1b / R2 spec; the spec is then executed; it produces a clean §10.3 disqualification on BTC. **Three-strike** family-shift trigger met.
- Operator independently decides the absolute-edge gap is too large to close from within this family.
- An evidence-grounded alternative-family hypothesis emerges with a credible mechanism that compatibly tests on v002 datasets.

### I.7 Stop point (no further phase ever)

- Operator decides to permanently pause strategy work.
- Discovery of a documentation inconsistency in prior phase records that requires a docs-only correction phase before any further strategy work — but this would itself be a phase, not a permanent stop.

---

## J. Explicit non-proposal list

Phase 2p explicitly does NOT:

- Run new backtests, runs, or variants.
- Add a new redesign candidate beyond H0 / R3 / R1a+R3.
- Change any §10.3 / §10.4 / §11.3 / §11.4 / §11.6 threshold.
- Change any committed R3 sub-parameter value (R-target stays at 2.0; time-stop stays at 8).
- Change any committed R1a sub-parameter value (X stays at 25; N stays at 200).
- Change H0's role as the sole formal §10.3 / §10.4 anchor.
- Quietly reopen execution momentum.
- Quietly advance toward readiness planning.
- Re-rank Phase 2g / 2l / 2m / 2n / 2o results.
- Recommend any execution phase.
- Authorize any successor phase by Phase 2p closure (the operator decides separately).
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
- Push the Phase 2p branch to origin (deferred to operator).

---

**End of Phase 2p consolidation memo.** Sections A–J complete. R3 formalized as the baseline-of-record. R1a designated retained-for-future-hypothesis-planning. H0 anchor preserved. Framework thresholds preserved. Future-resumption pre-conditions enumerated. Recommendation: stay paused after Phase 2p; operator decides any successor phase independently. No code changes, no runs, no new evidence — consolidation only. Awaiting operator/ChatGPT Gate 2 review.
