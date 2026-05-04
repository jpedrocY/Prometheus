# Phase 4y — Post-C1 Strategy Research Consolidation Memo

**Authority:** Operator authorization for Phase 4y (Phase 4x §"Operator decision menu" Option B conditional secondary alternative — docs-only post-C1 strategy research consolidation memo, only if separately authorized; operator has so chosen). Phase 4x (C1 backtest execution; Verdict C HARD REJECT — terminal for C1 first-spec); Phase 4w (C1 backtest-plan methodology); Phase 4v (C1 strategy spec); Phase 4u (C1 hypothesis-spec); Phase 4t (post-G1 fresh-hypothesis discovery memo); Phase 4s (post-G1 strategy research consolidation memo); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal for G1 first-spec); Phase 4q (G1 backtest-plan methodology); Phase 4p (G1 strategy spec); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery memo); Phase 4m (post-V2 consolidation memo; 18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4f (external strategy research landscape memo); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t (post-5m-diagnostics consolidation memo); Phase 3k (post-D1-A consolidation memo); Phase 3e (post-F1 consolidation memo); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks).

**Phase:** 4y — **Post-C1 Strategy Research Consolidation Memo** (docs-only). Consolidates the full post-C1 strategy-research state, updates the rejection topology with C1's distinct failure mode ("fires-and-loses" / contraction anti-validation), preserves every retained verdict and project lock, extracts reusable lessons from the Phase 4x C1 result, explicitly forbids rescue interpretations, and recommends the next operator boundary. **Phase 4y is text-only.** No new strategy is created; no new candidate is named; no fresh-hypothesis discovery memo is created; no strategy-spec or backtest-plan memo is created; no backtest is run; no Phase 4x rerun is permitted; no `scripts/phase4x_c1_backtest.py` modification is permitted; no implementation code is written; no data is acquired or modified; no manifest is modified; no verdict is revised; no project lock is changed; no successor phase is authorized.

**Branch:** `phase-4y/post-c1-strategy-research-consolidation`. **Memo date:** 2026-05-04 UTC.

---

## Summary

Phase 4x ran the predeclared C1 — Volatility-Contraction Expansion Breakout backtest exactly under the Phase 4w methodology and produced **Verdict C — C1 framework HARD REJECT.** Binding catastrophic-floor driver: CFP-2 (BTC OOS HIGH train-best mean_R = -0.3633 ≤ 0). Co-binding / independent drivers: CFP-3 (profit_factor = 0.4413 < 0.50; max_drawdown_R = 54.55 > 10R); CFP-6 (DSR = -20.8173 ≤ 0). **CFP-1 and CFP-9 explicitly did NOT trigger** — train-best variant 21 produced 149 BTC OOS HIGH trades; transition rate was 3.33 per 480 bars; 100% of variants produced ≥ 30 trades. C1 solved the V2 / G1 zero-trade collapse problem but still failed: the C1 transition trades produced mean_R = -0.3633 vs. non-contraction baseline mean_R = -0.1192 (a -0.2440R differential with bootstrap 95% CI [-0.4101, -0.0810] strictly negative). C1 also underperformed always-active-same-geometry baseline (-0.2201R; CI strictly negative) and delayed-breakout baseline (-0.2930R). All 32 BTC OOS HIGH variants and all 32 ETH OOS HIGH variants are loss-making. Cost is NOT the binding driver; LOW / MEDIUM / HIGH all loss-making. ETH cannot rescue BTC.

**C1 represents a categorically new failure mode** in the project's strategy-research record: **"fires-and-loses" / contraction anti-validation.** This is structurally distinct from V2 (Phase 4l, design-stage incompatibility, zero trades) and G1 (Phase 4r, regime-gate-meets-setup intersection sparseness, zero trades), and structurally similar to F1 (Phase 3d-B2, catastrophic-floor / bad full-population expectancy) and R2 (Phase 2w, cost-fragility) in that it generated a population large enough to evaluate. It differs from F1 in that the failure is not catastrophic-floor-driver heavy but is rather an empirical anti-validation against multiple non-hypothesis baselines. It differs from R2 in that costs were not the binding driver — C1 is structurally loss-making before HIGH cost amplification.

**C1 first-spec is terminally HARD REJECTED as retained research evidence only.** Every retained verdict and project lock from Phase 2 / 3 / 4 is preserved verbatim. **No C1 rescue is authorized:** no C1-prime / C1-narrow / C1-extension / C1 hybrid; no threshold tuning from Phase 4x forensic numbers; no post-hoc volume / funding / HTF / ATR-stop-distance gate addition; no C1 rerun; no C1 implementation; no Phase 4v / Phase 4w amendment based on Phase 4x forensic results. **No cross-strategy rescue is authorized:** no V2-prime / G1-prime / R2 cheaper-cost / F1 profitable-subset / D1-A extra-filter / D1-B / V1-D1 / F1-D1 hybrid; no immediate ML / market-making / paper / shadow / live / Phase 4 canonical. **Recommended next operator choice: remain paused (primary).** Conditional secondary: docs-only "post-rejection research map / hypothesis-discovery process redesign" memo, only if separately authorized.

## Authority and boundary

- **Authority granted:** create the Phase 4y docs-only consolidation memo; create the Phase 4y closeout; consolidate the post-C1 strategy-research state into the project record; update the rejection topology with C1's failure mode; reaffirm every retained verdict and project lock verbatim; extract reusable insights; document forbidden rescue interpretations; identify what C1 did and did not teach; recommend the next operator boundary (remain paused as primary; docs-only research-process redesign memo as conditional secondary).
- **Authority NOT granted:** create C1-prime / C1-narrow / C1-extension / C1 hybrid (forbidden); create any new named strategy candidate (forbidden); create a fresh-hypothesis discovery memo (forbidden — would require separate operator authorization analogous to Phase 4n / 4t); create a strategy-spec memo (forbidden); create a backtest-plan memo (forbidden); run any backtest (forbidden); rerun Phase 4x (forbidden); modify `scripts/phase4x_c1_backtest.py` (forbidden); write implementation code (forbidden); acquire / download / modify / patch data (forbidden); modify manifests (forbidden); revise any retained verdict (forbidden); change any project lock (forbidden); authorize Phase 4z or any successor phase (forbidden); authorize paper / shadow / live / exchange-write (forbidden).
- **Hard rule:** Phase 4y is text-only. No code is written. No data is touched. No backtest is run.

## Starting state

```text
Branch (Phase 4y):      phase-4y/post-c1-strategy-research-consolidation
main / origin/main:     a24ee9298f52e4289e1c56b23fc9b762a850ca4b (unchanged)
Phase 4x merge:         e28e34a2878d9a6b602e0f2e26eafdf787cfbb59 (merged)
Phase 4x housekeep:     a24ee9298f52e4289e1c56b23fc9b762a850ca4b (merged)
Working-tree state:     clean (no tracked modifications); only gitignored
                        transients .claude/scheduled_tasks.lock and
                        data/research/ are untracked and will not be
                        committed.
Quality gates (verified at memo creation):
  ruff check . PASS
  pytest 785 PASS
  mypy strict 0 issues across 82 source files
```

## Why this memo exists

The Phase 4x C1 backtest produced a third Verdict C HARD REJECT in the project's strategy-research record (after Phase 4l V2 HARD REJECT and Phase 4r G1 HARD REJECT) and the sixth terminal strategy verdict overall (R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2 HARD REJECT; G1 HARD REJECT; C1 HARD REJECT). The project precedent for handling these outcomes is a docs-only consolidation memo:

- Phase 3e — post-F1 consolidation memo;
- Phase 3k — post-D1-A consolidation memo;
- Phase 4m — post-V2 consolidation memo (introduced the 18-requirement fresh-hypothesis validity gate);
- Phase 4s — post-G1 consolidation memo;
- **Phase 4y — post-C1 consolidation memo (this phase).**

A consolidation memo serves five purposes:

1. record the Phase 4x outcome canonically into the project's research-state ledger;
2. preserve every retained verdict and project lock verbatim;
3. update the rejection topology with the new failure mode;
4. extract reusable insights without authorizing rescue;
5. recommend a forward boundary that respects accumulated negative evidence and avoids drift toward strategy-rescue work.

Phase 4y does NOT introduce a new candidate, new strategy spec, new backtest plan, or new methodology. Each of those steps requires its own separate operator authorization; Phase 4n (post-V2 fresh-hypothesis discovery) and Phase 4t (post-G1 fresh-hypothesis discovery) precedents demonstrate the pattern.

## Relationship to Phase 4x

- Phase 4x executed the first C1 backtest under Phase 4w. Phase 4x emitted Verdict C — C1 framework HARD REJECT.
- Phase 4x recommendation was: Option A — remain paused (primary); Option B — Phase 4y post-C1 consolidation memo (conditional secondary).
- The operator has now explicitly authorized Phase 4y as a docs-only consolidation memo on the conditional-secondary path (analogous to the post-G1 Phase 4s authorization after Phase 4r).
- Phase 4y does NOT authorize Phase 4z or any successor phase.
- Phase 4y does NOT amend Phase 4v C1 strategy spec, Phase 4w C1 backtest-plan methodology, or any prior governance.
- Phase 4y does NOT modify `scripts/phase4x_c1_backtest.py` or rerun the backtest.
- Phase 4y does NOT use Phase 4x forensic numbers as a tuning input for any future hypothesis or rescue.

## Full retained-verdict ledger

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
                (Phase 4l — Verdict C; CFP-1 critical; CFP-3 mechanical;
                preserved)
G1           : HARD REJECT — terminal for G1 first-spec
                (Phase 4r — Verdict C; CFP-1 critical binding;
                CFP-9 independent; CFP-3/4 mechanical/subordinate;
                preserved)
C1           : HARD REJECT — terminal for C1 first-spec
                (Phase 4x — Verdict C; CFP-2 binding;
                CFP-3 / CFP-6 co-binding;
                CFP-1 / CFP-9 explicitly did NOT trigger;
                NEW failure mode: fires-and-loses /
                contraction anti-validation;
                preserved by this memo)

§11.6        : 8 bps HIGH per side (preserved verbatim)
§1.7.3       : 0.25% risk / 2× leverage / 1 position / mark-price stops
                (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation
                              governance (preserved)
Phase 4a runtime            : public API and behavior (preserved;
                              strategy-agnostic)
Phase 4e                    : reconciliation-model design memo
                              (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x
                            : all preserved verbatim
Phase 4y                    : Post-C1 strategy research consolidation
                              memo (this phase; new; docs-only)
```

**No verdict is revised by Phase 4y. No project lock is changed by Phase 4y.**

## Full rejection topology after C1

| Strategy | Failure mode | Evidence type | Rescue trap |
| --- | --- | --- | --- |
| **R2** (pullback-retest entry) | Cost-fragility | Mechanism generated; cost survival failed (§11.6 HIGH blocks) | Cheaper-cost / relaxed §11.6 rescue |
| **F1** (mean-reversion-after-overextension) | Catastrophic-floor / bad full-population expectancy | Mechanism generated; full framework failed (Phase 3c §7.3 catastrophic-floor predicate triggered 5×; M1 PARTIAL; M2 FAIL/weak; M3 PASS-isolated only) | Profitable-subset mining; "TARGET-isolation" rescue |
| **D1-A** (funding-Z-score contrarian) | Mechanism / framework mismatch | Mechanism partially passed (M1 BTC h=32 PASS); framework conditions failed (cond_i / cond_iv) | Funding + extra filters / D1-A-prime / D1-B; V1/D1 hybrid; F1/D1 hybrid |
| **V2** (participation-confirmed trend continuation) | Design-stage incompatibility | Zero trades; no mechanism evidence (CFP-1 critical: 512/512 variants below 30 OOS trades; train-best 0 OOS trades) | Wider stops / stop-distance-filter removal / V2-prime / V2-narrow |
| **G1** (regime-first breakout continuation) | Regime-gate-meets-setup intersection sparseness | Zero qualifying trades; no active-regime mechanism evidence (CFP-1 critical; CFP-9 independent; regime active fraction 2.03%) | Classifier relaxation / K_confirm reduction / ATR-band widening / V_liq lowering / funding-band widening / G1-prime |
| **C1** (volatility-contraction expansion breakout) | **fires-and-loses / contraction anti-validation** | Plenty of trades (149 BTC OOS HIGH; transition rate 3.33 per 480 bars); negative expectancy (mean_R = -0.3633); negative differentials vs all three baselines (M1 -0.244R; M2.a -0.220R; M2.b -0.293R); CI strictly negative for M1 and M2.a | C1-prime / threshold amendment / contraction-variant mining; volume / funding / HTF gate added post hoc; ATR stop-distance gate added post hoc |

C1 occupies a new column in the topology: **evidence-generating negative result that directly anti-validates the hypothesis against non-hypothesis baselines**. Unlike V2 / G1's zero-trade non-evidence-generating failures, C1 produced a sufficiently large trade population to be statistically informative — and the information is empirically negative.

## C1 result recap

```text
Verdict: C — C1 framework HARD REJECT
Best variant: id=21, label=B=0.10|C=0.45|N=12|S=0.10|T=2.0
              (B_width=0.10, C_width=0.45, N_comp=12,
               S_buffer=0.10, T_mult=2.0, T_stop_bars=24)

Binding catastrophic-floor driver:
  CFP-2: BTC OOS HIGH train-best mean_R = -0.3633 <= 0

Co-binding / independent drivers:
  CFP-3: profit_factor = 0.4413 < 0.50
         max_drawdown_R = 54.55 > 10R
  CFP-6: DSR = -20.8173 <= 0

CFPs that did NOT trigger:
  CFP-1: 149 trades on BTC OOS HIGH; 0/32 variants below 30
  CFP-4: BTC fail AND ETH fail; no rescue scenario
  CFP-5: train HIGH mean_R already negative (no train-only success)
  CFP-7: max-month fraction 7.4% (well below 50%)
  CFP-8: worst sensitivity degrade 0.155R (below 0.20R threshold)
  CFP-9: transition_rate_per_480 = 3.33 (>= 1.0);
         100% of variants produce >= 30 trades
  CFP-10: optional-ratio access count = 0
  CFP-11: no future-bar / partial-bar / signal-without-contraction /
          entry-beyond-L_delay / degenerate-double-transition
  CFP-12: all forbidden-input audit counters = 0

BTCUSDT primary (train-best variant 21):
  BTC OOS HIGH:
    trade_count   : 149
    mean_R        : -0.3633
    total_R       : -54.1258
    max_dd_R      :  54.55
    profit_factor :   0.4413
    sharpe        :  -0.3721
  All 32 BTC OOS HIGH variants loss-making (mean_R range -0.10 to -0.44).
  Loss-making at all OOS cost cells:
    LOW    (1bp)  : mean_R = -0.1701
    MEDIUM (4bps) : mean_R = -0.2529
    HIGH   (8bps) : mean_R = -0.3633
  Cost is NOT the binding driver.

ETHUSDT comparison (same train-best variant 21):
  ETH OOS HIGH:
    trade_count   : 109
    mean_R        : -0.2140
    profit_factor :   0.6252
    sharpe        :  -0.2148
  All 32 ETH OOS HIGH variants loss-making (mean_R range -0.10 to -0.24).
  ETH cannot rescue BTC.

Mechanism checks:
  M1 FAIL: diff = -0.2440R; CI = [-0.4101, -0.0810] strictly negative
  M2 FAIL:
    M2.a diff = -0.2201R; CI = [-0.3859, -0.0556] strictly negative
    M2.b diff = -0.2930R
  M3 FAIL: BTC OOS HIGH mean_R < 0; CFP-2/3 trigger;
           opportunity-rate floors PASS
  M4 FAIL: ETH differential = -0.1589; directional consistency YES;
           ETH cannot rescue BTC
  M5 DIAGNOSTIC_ONLY: skipped per Phase 4w optional handling

Search-space control:
  PBO_train_validation : 0.375  (below 0.50)
  PBO_train_oos        : 0.219  (below 0.50)
  PBO_cscv             : 0.094  (below 0.50)
  DSR (train-best, N=32) : -20.8173 (<= 0; CFP-6 triggers via DSR)

Opportunity-rate:
  total_30m_bars                       : 30 672
  oos_total_transitions (long+short)   : 213
  transition_rate_per_480_bars         : 3.33  (>= 1.0)
  train-best OOS HIGH executed trades  : 149   (>= 30)
  variants with >= 30 BTC OOS HIGH trades : 32 / 32 (100.0%)
  CFP-1 NOT triggered.
  CFP-9 NOT triggered.
```

## What C1 taught

1. **C1 solved the V2 / G1 zero-trade problem but still failed.** The local-precondition design successfully generated 149 BTC OOS HIGH trades and 213 candidate transitions across the 21-month OOS window. The C1 design pattern — local precondition (compression-state) coupled with a transition trigger (close-beyond-buffer) — is empirically capable of producing healthy opportunity rates without the regime-gate sparsity that doomed G1 or the stop-distance-filter incompatibility that doomed V2.
2. **Opportunity-rate viability is necessary but not sufficient.** Phase 4u predeclared opportunity-rate viability as intrinsic to the contraction-to-expansion theory, and Phase 4v / Phase 4w made it a binding gate via CFP-9. The Phase 4x result confirms that the framework is implementable and the gate is meaningful — but passing the gate does NOT imply the strategy has an edge.
3. **The local contraction precondition produced enough trades, but the trades were bad.** This is a sample-size adequate negative result, not a sample-size collapse failure.
4. **Contraction-tied transitions underperformed non-contraction baselines.** C1 mean_R = -0.3633 vs. non-contraction baseline mean_R = -0.1192 (-0.244R differential; bootstrap 95% CI strictly negative). The contraction precondition makes the strategy *worse*, not better, on this dataset under this implementation.
5. **Transition timing did not add value; it degraded value.** Delayed-breakout baseline (entries fired more than `L_delay` bars after the contraction state ended) produced mean_R = -0.0702 vs. C1 mean_R = -0.3633 (a -0.293R differential). Firing immediately after compression release was *worse* than firing later.
6. **Always-active same-geometry baseline was better than C1.** mean_R = -0.1431 vs. C1 mean_R = -0.3633 (-0.220R differential; CI strictly negative). The same close-beyond-compression-box-with-buffer rule, fired without the contraction precondition, performed substantially better. **The contraction precondition is empirically anti-predictive in this implementation.**
7. **The theory "compression release into directional movement" was not supported under the locked C1 implementation.** Three independent baselines (non-contraction, always-active, delayed) all outperformed C1. This is multi-baseline negative agreement.
8. **Cost realism still matters, but cost was NOT the binding failure here.** All three cost cells (LOW, MEDIUM, HIGH) produced negative mean_R for the train-best variant. The §11.6 = 8 bps HIGH cost only amplified an already-negative gross expectancy.
9. **Negative baselines were crucial.** Without M1 / M2.a / M2.b structurally requiring negative-baseline comparisons, the project would only see "C1 produced 149 trades, mean_R = -0.36." With baselines, the project can distinguish "noisy strategy" from "anti-validated strategy." Phase 4w's binding negative-test framework is now validated as an essential discipline.
10. **All 32 variants failing reduces variant-grid overfitting risk to nil.** PBO across all three horizons (train→val 0.375; train→OOS 0.219; CSCV 0.094) is below 0.50. There is no "lucky" subset that PBO mistakenly identifies as edge — the strategy is broadly negative.
11. **DSR can show "anti-overfit" while still confirming "no edge."** Train-best DSR = -20.8173 magnifies the negative train-best raw Sharpe (-0.363) under N=32 deflation. CFP-6 triggers via DSR, not via PBO. This is a useful new pattern: a strategy can be both not-overfit AND not-good.
12. **All 32 variants are loss-making across all three windows.** Train HIGH mean_R for the train-best is already -0.4778; validation HIGH is -0.6126; OOS HIGH is -0.3633. The strategy was negative on the training set itself; the OOS result is consistent with the train.

## What C1 did not teach

- **C1 does not prove all volatility-contraction ideas are impossible.** It proves this specific compression-box-width-vs-rolling-median-with-close-beyond-buffer-with-close-location implementation, on BTCUSDT 30m bars over 2024-07-01..2026-03-31 OOS, under HIGH = 8 bps cost, is empirically negative.
- **C1 does not justify C1-prime.** Picking different N_comp / C_width / B_width / S_buffer / T_mult values from the Phase 4x grid output is forbidden — this is exactly the data-snooping pattern Phase 4m's 18-requirement validity gate forbids.
- **C1 does not justify tuning thresholds from Phase 4x results.** Phase 4w explicitly forbade this; Phase 4x explicitly forbade this; Phase 4y explicitly forbids this.
- **C1 does not justify a new contraction measure selected from Phase 4x failures.** Choosing a different compression measure, rolling-median window, close-location form, or stop / target / time-stop derivation that "happens to fix" Phase 4x's negative result is forbidden post-hoc tuning.
- **C1 does not justify adding volume / funding / HTF / ATR-stop-distance gates post hoc.** Phase 4v explicitly excluded these; adding them after observing the Phase 4x negative result is forbidden.
- **C1 does not revise V2 / G1 / R2 / F1 / D1-A verdicts.** Each prior verdict stands on its own evidence base.
- **C1 does not justify paper / shadow / live operation.** The strategy is loss-making; any live exposure would be expected-loss.
- **C1 does not justify Phase 4 canonical (paper / shadow / live-readiness gates).** No strategy candidate exists for Phase 4 canonical to validate.
- **C1 does not justify data acquisition.** No additional data was needed for Phase 4x; no additional data is justified by the result.
- **C1 does not invalidate the Phase 4u opportunity-rate viability principle.** It confirms the principle is meaningful (the C1 framework satisfies it) and adds the corollary that opportunity-rate viability ≠ edge.

## C1 categorical failure mode

```text
Topology label: fires-and-loses / contraction anti-validation
```

Definition:

- C1 did NOT fail because no trades were generated (149 BTC OOS HIGH train-best trades; 213 candidate transitions; 100% of variants ≥ 30 trades).
- C1 did NOT fail because the opportunity-rate floor was too strict (transition rate 3.33 per 480 bars >> 1.0 floor; train-best 149 trades >> 30 floor; 100% pass fraction >> 50% floor).
- C1 did NOT fail because HIGH cost alone killed an otherwise viable low-cost edge (LOW, MEDIUM, HIGH all produce negative mean_R for the train-best variant).
- C1 did NOT fail because the variant grid was overfit to a "lucky" subset (PBO low across all three horizons; CSCV PBO 0.094).
- C1 did NOT fail at the methodology layer (CFP-10 / CFP-11 / CFP-12 all clean; no lookahead; no transition-dependency violation; no forbidden-input access).
- **C1 failed because the core contraction-tied transition claim performed worse than relevant baselines and had negative BTC OOS HIGH expectancy.**

This is *stronger* evidence against the C1 first-spec than V2 / G1 zero-trade failure because the mechanism actually generated a sample and was empirically negative against three independent baselines.

## Comparison with V2 and G1

| Dimension | V2 (Phase 4l) | G1 (Phase 4r) | **C1 (Phase 4x)** |
| --- | --- | --- | --- |
| Trade count | 0 BTC OOS HIGH | 0 BTC OOS HIGH G1 | **149 BTC OOS HIGH** |
| Binding CFP | CFP-1 critical (zero trades) | CFP-1 critical + CFP-9 independent | **CFP-2 binding (negative expectancy); CFP-3 / CFP-6 co-binding** |
| Mechanism evidence | Not generable | Not generable | **Generable; empirically negative** |
| Opportunity-rate gate | N/A (CFP-1 first-binding) | N/A (CFP-9 independent) | **PASSED (rate 3.33; 100% variants pass)** |
| Failure layer | Design-stage incompatibility (stop-distance filter) | Regime-gate-meets-setup sparseness (joint event) | **Edge layer (contraction anti-predictive)** |
| Baseline differentials | Not measurable | Not measurable | **All three baselines outperform C1; CI strictly negative on M1 and M2.a** |
| Cost binding? | Mechanically negative under cost (CFP-3 mechanical via empty arrays) | Mechanically negative under cost (CFP-3 mechanical via empty arrays) | **NOT cost-binding — loss-making at LOW cost** |
| PBO | Methodologically inert (zero trades) | Methodologically inert (zero trades) | **All PBO < 0.50; not overfit but not edge** |
| DSR | All zero (zero trades) | All zero (zero trades) | **-20.82 ≤ 0 (CFP-6 binding via DSR)** |

**V2 and G1 were structural non-evidence-generating failures.** C1 is **an evidence-generating negative result**. Therefore C1 cannot be rescued by appealing to the V2 / G1 lesson "avoid zero trades" — C1 already avoided zero trades, and the resulting evidence is *more* damning than zero trades, not less. A zero-trade result leaves the hypothesis undetermined; an anti-validated result rejects the hypothesis on this dataset.

## Comparison with R2, F1, and D1-A

| Dimension | R2 (Phase 2w) | F1 (Phase 3d-B2) | D1-A (Phase 3j) | **C1 (Phase 4x)** |
| --- | --- | --- | --- | --- |
| Trade-count adequacy | OK | OK | OK | **OK (149 / 109)** |
| Mechanism check status | M1 ✓; M3 ✓; M2 ✗ | M1 PARTIAL; M2 FAIL / weak; M3 PASS-isolated | M1 PASS (h=32); M2 FAIL; M3 PASS-isolated | **All M1 / M2 / M3 / M4 FAIL** |
| Cost-survival | FAIL (HIGH blocks) | Mostly negative | BTC HIGH negative | **Negative at LOW / MEDIUM / HIGH** |
| Catastrophic-floor predicates | None binding (cost is binding) | CFP-1-equivalent triggered 5× | None binding by predicate; cond_i / cond_iv conditions fail | **CFP-2 binding; CFP-3 / CFP-6 co-binding** |
| Final verdict | FAILED — §11.6 | HARD REJECT | MECHANISM PASS / FRAMEWORK FAIL — other | **HARD REJECT** |
| Baseline differential check | Not formally required at the 2w bar | Mechanism subset diagnostic only | Mechanism subset diagnostic only | **Three formal binding negative tests; all three FAIL with CI strictly negative for M1 / M2.a** |
| Distinct lesson | cost-realism is binding | catastrophic-floor predicates are essential | mechanism PASS does not imply framework PASS | **opportunity-rate PASS does not imply edge PASS; baseline differentials can be strictly negative** |

C1 resembles **F1** more than V2 / G1 in that it generated enough trades and failed expectancy. C1 differs from **R2** because cost is not the binding driver — C1 is structurally loss-making before HIGH cost amplification. C1 differs from **D1-A** because its core mechanism checks failed *directly* and *unambiguously* with strictly negative bootstrap CIs, rather than failing framework conditions while passing partial mechanism checks.

The combined topology now contains **six categorically distinct failure modes** in the project's strategy-research record:

1. **R2** — cost-fragility;
2. **F1** — catastrophic-floor / bad full-population expectancy;
3. **D1-A** — mechanism / framework mismatch;
4. **V2** — design-stage incompatibility (zero trades);
5. **G1** — regime-gate-meets-setup intersection sparseness (zero trades);
6. **C1** — fires-and-loses / contraction anti-validation (NEW).

## Updated strategy-research topology

```text
                            POSITIVE                       NEGATIVE
                            --------                       --------
H0  framework anchor        baseline-of-existence
R3  V1 baseline             BASELINE-OF-RECORD
R1a volatility filter       retained as research
R1b-narrow                  retained as research

R2  pullback-retest                                        FAILED — §11.6
F1  mean-reversion                                         HARD REJECT (catastrophic-floor)
D1-A funding contrarian                                    MECHANISM PASS / FRAMEWORK FAIL
V2  participation breakout                                 HARD REJECT (zero-trade design)
G1  regime-first breakout                                  HARD REJECT (zero-trade gate)
C1  contraction-expansion                                  HARD REJECT (fires-and-loses)
```

**Six terminal negative outcomes** versus **two positive anchors (H0, R3)** and **two retained-research-only positions (R1a, R1b-narrow)**. The accumulated negative evidence is substantial and is itself a project-record asset; it constrains what kinds of future hypotheses can be plausibly differentiated from already-tested designs.

## Reusable insights after C1

1. **Opportunity-rate viability must remain a pre-backtest gate, but it is not an edge test.** A strategy can satisfy CFP-1 / CFP-9 (sample-size adequacy) and still be empirically anti-predictive. The Phase 4u opportunity-rate viability principle is preserved; CFP-9 enrichment is preserved; the project must continue to use it as a fail-closed pre-condition AND must add explicit baseline-differential checks for any future hypothesis.
2. **Negative baselines are mandatory for any future hypothesis.** C1's M1 / M2.a / M2.b multi-baseline framework is the right pattern. Any future fresh hypothesis must define its closest non-hypothesis baseline before any data is touched. A future spec that omits negative baselines must be rejected at spec-review time.
3. **A local precondition can avoid G1-style sparsity while still being anti-predictive.** Avoiding zero trades is a necessary but insufficient discipline. The C1 design solved the joint-event problem and still failed.
4. **Sample viability and edge viability are distinct.** Project methodology must explicitly separate "is the population large enough to be statistically informative?" from "does the population have positive expectancy after costs?" Conflating them produces false confidence.
5. **"Not zero trades" is not success.** A future hypothesis must not be evaluated against the criterion "did it fire enough trades?" alone. Firing is necessary; the evidence after firing is what determines edge.
6. **HIGH-cost survival cannot rescue negative gross structure.** §11.6 is a one-way gate (passing it is necessary; it does not validate edge). C1 already failed at LOW cost; HIGH only amplified the failure. Future hypotheses must establish gross-positive expectancy before any cost-sensitivity claim is evaluated.
7. **Every future hypothesis must explain why its primary condition should outperform an unconditioned baseline.** Phase 4y adds this requirement to the Phase 4m 18-requirement validity gate as observation #19 (informally; the gate itself is preserved verbatim and is not amended). The minimum acceptable theoretical content is "this condition is positively predictive against an unconditioned same-geometry baseline because [stated mechanism]."
8. **Every future hypothesis must define the closest non-hypothesis baseline before any data is touched.** This is the precondition-removed-while-everything-else-fixed baseline. C1's always-active-same-geometry baseline played this role.
9. **Baseline differentials may be more important than raw mean_R.** A strategy with mean_R = +0.1R could still fail M1 / M2 if its non-conditioned baseline produces +0.3R. A strategy with mean_R = -0.1R could still fail M1 / M2 if its baseline produces -0.4R (Phase 4y note: this would still trigger CFP-2 on absolute negativity; the differential check is necessary in addition to absolute checks, not in place of them).
10. **DSR / PBO / CSCV can show "not overfit" while still confirming no edge.** Phase 4x's PBO_cscv = 0.094 demonstrates that low PBO is not equivalent to "the strategy has edge." DSR magnifying a negative raw Sharpe via CFP-6 is a useful complementary signal: when PBO is low and DSR is strongly negative, the diagnosis is "consistently bad," not "overfit."
11. **First-spec hard rejections should not be mined for second-spec thresholds.** This is a discipline already established by Phase 4m (post-V2) and Phase 4s (post-G1); Phase 4y reaffirms it for C1. The Phase 4x parameter grid result is NOT an input to any future tuning.
12. **Remain-paused gains more weight after multiple independent failure modes.** With six terminal negative outcomes across categorically distinct failure modes, the operator has stronger evidence that "no obvious next strategy candidate exists" is itself an informative finding rather than a temporary state. This does not preclude future research; it constrains the form of future research.

## Forbidden C1 rescue interpretations

Phase 4y explicitly forbids:

- **C1-prime** (any C1 variant with modified thresholds based on Phase 4x forensic numbers);
- **C1-extension** (any C1 variant that adds an axis, dimension, or filter);
- **C1-narrow** (any C1 variant that restricts an existing axis to a "better-performing" subset chosen from Phase 4x);
- **C1 hybrid** (any blend of C1 with R3 / R1a / R1b-narrow / V2 / G1 / R2 / F1 / D1-A);
- **C1 with tuned thresholds from Phase 4x.** Choosing N_comp ∈ {6, 10, 14}, C_width ∈ {0.40, 0.65}, B_width ∈ {0.025, 0.15}, S_buffer ∈ {0.05, 0.30}, or T_mult ∈ {1.0, 2.5} based on which Phase 4x sensitivity-cell results looked "least bad" is forbidden post-hoc tuning.
- **C1 with different N_comp chosen from Phase 4x outputs** — forbidden.
- **C1 with different C_width chosen from Phase 4x outputs** — forbidden.
- **C1 with different B_width chosen from Phase 4x outputs** — forbidden.
- **C1 with different S_buffer chosen from Phase 4x outputs** — forbidden.
- **C1 with different T_mult chosen from Phase 4x outputs** — forbidden.
- **C1 with volume added post hoc.** Phase 4v excluded volume; adding it after observing Phase 4x is forbidden post-hoc design adjustment.
- **C1 with funding added post hoc.** Phase 4v excluded funding; adding it post-hoc is forbidden.
- **C1 with HTF gate added post hoc.** Phase 4v excluded HTF gate; adding it post-hoc is forbidden.
- **C1 with ATR stop-distance gate added post hoc.** Phase 4v explicitly forbade this gate (in the C1 first-spec); adding it post-hoc is forbidden double-violation (post-hoc design adjustment AND inheriting V2 forensic numbers).
- **C1 with mark-price / aggTrades / spot / cross-venue / order-book rescue.** Phase 4u / 4v / 4w excluded these inputs; adding any of them post-hoc is forbidden.
- **C1 using any Phase 4x forensic result as tuning input** — forbidden.
- **C1 rerun** — forbidden. Phase 4x is terminal for the C1 first-spec.
- **C1 implementation in `src/prometheus/`** — forbidden. C1 is research evidence only.
- **Phase 4v amendment based on Phase 4x forensic numbers** — forbidden.
- **Phase 4w methodology amendment based on Phase 4x forensic numbers** — forbidden.

## Forbidden cross-strategy rescue interpretations

Phase 4y reaffirms forbidden:

- **V2-prime / V2-narrow / V2-relaxed / V2 hybrid** — terminal V2 first-spec rejection from Phase 4l;
- **G1-prime / G1-narrow / G1-extension / G1 hybrid** — terminal G1 first-spec rejection from Phase 4r;
- **R2 cheaper-cost / relaxed-§11.6 rescue** — §11.6 = 8 bps HIGH per side preserved verbatim;
- **F1 profitable-subset rescue** — Phase 3e and Phase 3d-B2 explicitly rejected this;
- **D1-A extra-filter / D1-A-prime / D1-B / V1-D1 / F1-D1 hybrid** — Phase 3k explicitly rejected these;
- **5m strategy from Q1–Q7 diagnostic findings** — Phase 3t explicitly closed this thread; Phase 3o §6 forbidden question forms preserved;
- **Immediate ML-first black-box forecasting** — project remains rules-based per §1.7.3; no ML feasibility memo is authorized;
- **Immediate market-making / HFT** — Phase 4f confirmed non-transferable to Prometheus substrate;
- **Paper / shadow / live operation** — no validated strategy exists; FORBIDDEN per `docs/12-roadmap/phase-gates.md`;
- **Phase 4 canonical** — assumes strategy evidence which the project does not have; FORBIDDEN;
- **Data acquisition as next step** — no acquisition is justified by Phase 4x; mark-price / aggTrades / spot / cross-venue / order-book remain forbidden;
- **C1-prime / V2-prime / G1-prime** as the "obvious next step after Phase 4y" — Phase 4y explicitly does not authorize any of them.

## Implications for future fresh-hypothesis discovery

If a future docs-only fresh-hypothesis discovery memo is ever separately authorized (analogous to Phase 4n after Phase 4m, or Phase 4t after Phase 4s — neither is authorized by Phase 4y):

- **Any future hypothesis must be more theoretically distinct than C1 was from G1 / R1a / V2.** Phase 4y observes that C1 was already designed to be theoretically distinct from G1 (no top-level state machine; no multi-dimension AND classifier) and from V2 (no Donchian setup; no V1-inherited stop-distance filter) and from R1a (no per-bar volatility-percentile bolt-on filter). Despite this distinctness, C1 still failed on BTCUSDT 30m. A future hypothesis must clear an even higher bar: it must be theoretically distinct from C1 *as well as* from G1 / R1a / V2 / R3 / R1b-narrow.
- **Any future hypothesis must define its negative baseline before any data touch.** The closest non-hypothesis baseline must be specified ex-ante (analogous to C1's always-active-same-geometry baseline).
- **Any future hypothesis must define both opportunity-rate viability AND expected baseline superiority.** Phase 4u predeclared the former; Phase 4y observes that the latter must be explicit ("we expect the conditioned strategy to outperform the unconditioned baseline by ≥ Δ_R with bootstrap CI lower > 0").
- **Any future hypothesis must avoid "mechanical condition + breakout" unless it explains why the condition is positively predictive against a same-geometry baseline.** C1 was a mechanical-condition + breakout design and the mechanical condition turned out to be anti-predictive. Future mechanical-condition designs must include a theoretical case for why their condition is *positively* predictive — not merely "it is a condition that can be measured."
- **Any future discovery memo must treat remain-paused as a serious primary outcome.** With six terminal negative outcomes, the burden of proof for a new candidate is higher, not lower.
- **No future candidate should be named directly by Phase 4y.** Any naming would constitute a new candidate and is forbidden by the Phase 4y scope. A future docs-only research-process redesign or hypothesis-discovery memo would be the appropriate venue, and would itself require separate operator authorization.
- The Phase 4m 18-requirement fresh-hypothesis validity gate remains binding verbatim. Phase 4y observes that requirement #4 (entry / stop / target / sizing / cost / timeframe / exit must be defined together) and requirement #6 (predeclared mechanism checks) should be read together with the C1 lesson that **mechanism-check predeclaration must include negative-baseline differentials with bootstrap CI**, not merely raw mean_R thresholds. This is an observation, not a governance amendment; the gate itself is preserved verbatim.

## Implications for implementation-readiness work

- The runtime foundation from Phase 4a (state package, persistence layer, governance labels, risk skeleton, exposure-gate skeleton, stop-validation skeleton, fake-exchange adapter, operator state view, test harness) **still exists and remains strategy-agnostic**. Phase 4x did not modify any of it.
- Phase 4x did NOT create an implementation candidate. C1 was research-only and remains research-only after the HARD REJECT.
- Implementation-readiness work *may* still be useful in the future if explicitly scoped as **strategy-agnostic safety infrastructure** (e.g., the Phase 4d Option D reconciliation-model design memo authorized in Phase 4e; the Phase 4e Option B richer fake-exchange test harness; the Phase 4d Option B structured runtime logging slice). None of these is authorized by Phase 4y; each requires its own separate operator decision.
- **No C1 runtime implementation should occur.** C1 first-spec is terminally HARD REJECTED.
- **No paper / shadow / live step is justified** because no strategy candidate is positively validated.

## Implications for Phase 4 canonical / paper / shadow / live

- **Phase 4 canonical remains unauthorized.** `docs/12-roadmap/phase-gates.md` requires that Phase 4 canonical assume strategy evidence which the project does not possess. With the addition of C1 to the rejection ledger, the project's strategy-evidence position has not improved.
- **Paper / shadow / live remain FORBIDDEN.**
- **Production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials / exchange-write all remain unauthorized.**
- The `docs/12-roadmap/phase-gates.md` Production API Key Readiness Gate explicitly requires tiny-live phase to be near, host hardening complete, and validated strategy candidate present. The latter remains absent.

## Remaining valid project directions

Phase 4y identifies the following valid project directions (NOT authorizations — each requires separate operator authorization):

1. **Remain paused.** Always valid; primary recommendation.
2. **Docs-only post-rejection research-process redesign memo.** Could examine the cumulative lessons from R2 / F1 / D1-A / V2 / G1 / C1 and propose redesigns to the Phase 4m 18-requirement fresh-hypothesis validity gate, the negative-baseline framework, the opportunity-rate / edge-rate separation, or the variant-grid / DSR / PBO / CSCV conventions. This would be docs-only and would not authorize any new strategy candidate. **Conditional secondary** under the Phase 4y operator decision menu.
3. **Docs-only documentation-refresh memo.** Update `docs/00-meta/current-project-state.md`, `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, or `docs/00-meta/ai-coding-handoff.md` to reflect the post-C1 boundary. Conditional tertiary under the Phase 4y operator decision menu.
4. **Docs-only strategy-agnostic implementation-readiness scoping memo.** Could scope a future Phase 4d Option B (structured runtime logging) or Phase 4e Option B (richer fake-exchange test harness) without authorizing implementation. Conditional quaternary; not preferred over the research-process redesign because the project's binding constraint is strategy evidence, not infrastructure.

The following directions are **NOT valid** at this boundary (each is FORBIDDEN by accumulated governance / Phase 4y reaffirmation):

- C1 / V2 / G1 / R2 / F1 / D1-A rescue;
- new named strategy candidate;
- fresh-hypothesis discovery memo (would require separate operator authorization analogous to Phase 4n / 4t precedents);
- backtest of any kind;
- implementation in `src/prometheus/`;
- data acquisition;
- paper / shadow / live;
- Phase 4 canonical;
- production keys / credentials / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / exchange-write.

## Recommended next operator choice

- **Option A — primary recommendation: remain paused.** With six terminal negative strategy outcomes (R2 / F1 / D1-A / V2 / G1 / C1) and one preserved baseline-of-record (R3) plus one framework anchor (H0) and two retained-research-only positions (R1a / R1b-narrow), the project's strategy-evidence position has not improved during the Phase 4f → Phase 4x arc. The accumulated negative evidence itself is informative and should be preserved before the project commits to any further forward motion.
- **Option B — conditional secondary: docs-only post-rejection research-process redesign / hypothesis-discovery process redesign memo (only if separately authorized).** Phase 4y does NOT itself authorize this option. If the operator separately authorizes it later, the memo would be docs-only, would not name a new candidate, would not amend Phase 4m / Phase 4u / Phase 4v / Phase 4w governance, and would explicitly preserve every retained verdict and project lock. The memo's purpose would be to examine whether the Phase 4m 18-requirement validity gate, the Phase 4u opportunity-rate principle, the Phase 4w negative-baseline framework, and the variant-grid / DSR / PBO / CSCV conventions should be tightened given the cumulative six-failure-mode evidence. Such a memo would itself be docs-only and would explicitly not authorize any successor strategy phase.

NOT recommended:

- **C1 rescue** — REJECTED;
- **Immediate new strategy spec** — REJECTED (would require fresh-hypothesis discovery memo authorization first, analogous to Phase 4n / 4t);
- **Immediate backtest** — REJECTED;
- **Data acquisition** — REJECTED;
- **Implementation in `src/prometheus/`** — REJECTED;
- **Paper / shadow / live** — FORBIDDEN;
- **Phase 4 canonical** — FORBIDDEN.

## What this does not authorize

Phase 4y does NOT authorize:

- **Phase 4z** or any successor phase;
- creation of any new strategy candidate;
- creation of **C1-prime / C1-extension / C1-narrow / C1 hybrid**;
- any **C1 rerun**;
- any amendment of **Phase 4v C1 strategy spec** or **Phase 4w C1 backtest-plan methodology**;
- any amendment of **Phase 4m 18-requirement validity gate**, **Phase 4j §11 metrics OI-subset partial-eligibility rule**, **Phase 4k V2 backtest-plan methodology**, **Phase 3v §8 stop-trigger-domain governance**, **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance**, **Phase 3r §8 mark-price gap governance**;
- **implementation** in `src/prometheus/`;
- **data acquisition**;
- **paper / shadow / live / exchange-write**;
- any revision of **retained verdicts** (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1);
- any change to **project locks** (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- creation of a **fresh-hypothesis discovery memo** (would require separate operator authorization analogous to Phase 4n / 4t);
- creation of a **strategy-spec memo** or **backtest-plan memo** (would require separate operator authorization analogous to Phase 4o / 4p / 4u / 4v or Phase 4q / 4w);
- modification of **`scripts/phase4x_c1_backtest.py`** or any other existing script.

## Forbidden-work confirmation

Phase 4y did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`);
- run `scripts/phase4x_c1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create a new strategy candidate or named successor;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4z / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values;
- use Phase 4x C1 forensic numbers as tuning input for any future hypothesis or rescue.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : HARD REJECT (Phase 4r — Verdict C; CFP-1 critical
                       binding; CFP-9 independent; terminal for G1 first-spec;
                       preserved)
C1                  : HARD REJECT (Phase 4x — Verdict C; CFP-2 binding;
                       CFP-3 / CFP-6 co-binding; CFP-1 / CFP-9 NOT
                       triggered; terminal for C1 first-spec; preserved
                       by this memo)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price
                       stops (preserved)
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
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x
                            : all preserved verbatim
Phase 4y                    : Post-C1 strategy research consolidation
                              memo (this phase; new; docs-only)
Recommended state           : remain paused (primary);
                              docs-only post-rejection research-process
                              redesign memo (conditional secondary; not
                              authorized by Phase 4y)
```

## Operator decision menu

- **Option A — primary recommendation: remain paused.** This is the strongest-evidence position given the cumulative six-failure-mode rejection ledger.
- **Option B — conditional secondary: docs-only post-rejection research-process redesign / hypothesis-discovery process redesign memo (only if separately authorized; not started by this merge; would itself be docs-only and would explicitly not authorize any successor strategy phase).** This option is procedurally well-grounded but is NOT preferred over remain-paused because the binding constraint at this boundary is strategy evidence, and no docs-only memo can produce strategy evidence.
- **Option C — conditional tertiary: docs-only documentation-refresh memo (only if separately authorized; would update `docs/00-meta/current-project-state.md`, `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, or `docs/00-meta/ai-coding-handoff.md` to reflect the post-C1 boundary).** Acceptable but lower-value than Option B because the relevant docs are already largely synchronized.
- **Option D — NOT recommended: docs-only strategy-agnostic implementation-readiness scoping memo (only if separately authorized; would scope future Phase 4d Option B / Option C work).** Acceptable in principle but not preferred at this boundary because the project's binding constraint is strategy evidence, not infrastructure.
- **Option E — NOT recommended: fresh-hypothesis discovery memo.** Would require separate operator authorization analogous to Phase 4n / 4t. Phase 4y does NOT recommend this immediately because remain-paused has stronger evidence after six terminal failure modes.
- **Option F — REJECTED: any C1 / V2 / G1 / R2 / F1 / D1-A rescue.** All forbidden by Phase 4y.
- **Option G — REJECTED: immediate new strategy spec / backtest / implementation / data acquisition.** All rejected.
- **Option H — FORBIDDEN: paper / shadow / live / exchange-write / Phase 4 canonical / production keys / MCP / Graphify / `.mcp.json` / credentials.** All forbidden.

**Phase 4z and any successor phase are NOT authorized by Phase 4y.** Each future authorization is operator-driven and would be separately approved.

## Next authorization status

```text
Phase 4z (any successor)         : NOT authorized
Phase 4 (canonical)              : NOT authorized
Paper / shadow                   : NOT authorized
Live-readiness                   : NOT authorized
Deployment                       : NOT authorized
Production-key creation          : NOT authorized
Authenticated REST               : NOT authorized
Private endpoints                : NOT authorized
User stream / WebSocket          : NOT authorized
Exchange-write capability        : NOT authorized
MCP / Graphify                   : NOT authorized
.mcp.json / credentials          : NOT authorized
C1 implementation                : NOT authorized; terminal-rejected
C1 rerun                         : NOT authorized; terminal-rejected
C1 spec amendment                : NOT authorized; FORBIDDEN
Phase 4w methodology amendment   : NOT authorized; FORBIDDEN
G1 / V2 / R2 / F1 / D1-A rescue  : NOT authorized; FORBIDDEN
G1-prime / G1-extension axes     : NOT authorized; FORBIDDEN
V2-prime / V2-variant            : NOT authorized; FORBIDDEN
C1-prime / C1-extension          : NOT authorized; FORBIDDEN
Retained-evidence rescue         : NOT authorized; FORBIDDEN
5m strategy / hybrid             : NOT authorized; not proposed
ML feasibility                   : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                                 : NOT authorized; data unavailable
Mark-price / aggTrades / spot / cross-venue acquisition
                                 : NOT authorized; FORBIDDEN
Fresh-hypothesis discovery memo  : NOT authorized; would require
                                   separate operator authorization
Research-process redesign memo   : NOT authorized; conditional secondary
                                   in operator decision menu
Documentation-refresh memo       : NOT authorized; conditional tertiary
Strategy-agnostic implementation-
  readiness scoping memo          : NOT authorized; conditional quaternary
```

The next step is operator-driven: the operator decides whether to remain paused (primary) or authorize a docs-only post-rejection research-process redesign memo (conditional secondary, not started by this Phase 4y merge). Until then, the project remains at the post-Phase-4y consolidation boundary.

---

**Phase 4y is text-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. No retained verdict revised. No project lock changed. C1 first-spec remains terminally HARD REJECTED. Recommended state: remain paused. No next phase authorized.**
