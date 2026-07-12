# Phase 4bn-AS — Long-Horizon ML Ambiguity Decision Memo

## 1. Phase name

Phase 4bn-AS — Long-Horizon ML Ambiguity Decision Memo. A docs-only scientific
decision phase that resolves the Phase 4bn-AR `INVESTIGATE_AMBIGUOUS` verdict into
**exactly one** of two recommendations: stop the current aggTrades-only long-horizon
ML arc, or recommend exactly one genuinely new, tightly bounded follow-up
preregistration memo for later **separate** authorization. This phase decides only;
it does **not** run, implement, or authorize any follow-up.

## 2. Branch

`phase-4bn-as/longhorizon-ml-ambiguity-decision-memo`
(created from `main` at the base SHA below).

## 3. Base SHA

`a94e85a1b9bd6faf805dbed6ebf0bf3b475e0dbf`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AR merge
closeout. Verified in sync before branching.)

## 4. Phase type

Docs-only scientific **decision memo**. It reads **no** data, trains **nothing**,
scores **nothing**, reruns **no** builder / diagnostic / baseline, generates **no**
prediction / calibration / threshold, reads **no** local generated AQ/AR output,
creates **no** data or model artefact, mutates **no** namespace / manifest / gate /
sidecar / split / config / authorization flag, and authorizes **no** successor
execution phase. It records exactly one decision against the frozen Phase 4bn-AR
evidence and the frozen Phase 4bn-AP / 4bn-AE contracts.

## 5. Documents inspected

Read-only (committed docs + committed source constants only; `README` treated as
potentially stale and **not** used as current-state authority):

- `docs/00-meta/current-project-state.md` (head + repository-context + ML-arc
  framing paragraphs; navigational summary, not binding authority for this decision).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_ml-baseline-preregistration-contract-amendment.md`
  (§1 purpose / claim-scope framing; the §8 allowed/forbidden claim scope, §16
  frozen success/continue/kill thresholds, §17 ambiguous handling, §18 finite-arc
  budget & stopping rule, §19 absolute strategy/PnL/backtest/live boundary and the
  M0-style mechanism-admissibility gate — as recovered here and cross-checked against
  the AK/AP restatements).
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-ak_ml-arc-decision-memo.md`
  (the prior arc-decision that recorded `CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP` on
  the 15s evidence and **spent the single follow-up** on category 1, the
  longer-horizon label memo — i.e. this very long-horizon arc; the four frozen
  `CONTINUE_FOLLOWUP_CATEGORIES`; the treatment of the macro-F1 caveat, the cost
  finding, and the block-dependence policy).
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ap_longhorizon-ml-baseline-preregistration-contract.md`
  (the frozen long-horizon preregistration: §17 5m-primary / 30m-1h-secondary target
  decision, §21 baseline families + frozen L2 constants, §22 persistence definition,
  §23 metric registry, §24 decision hierarchy, §25 kill/continue criteria and the
  exact `INVESTIGATE_AMBIGUOUS` routing, §27 cost/materiality, §34/§35 claim scope).
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-ar_fixed-longhorizon-baseline-run-verdict.md`
  (the authoritative frozen AR evidence: §28–§39 metrics / block evidence /
  calibration / confidence-tail / verdict; §47–§48 claim scope; §51–§53 result state
  and no-successor statement).
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-ar_closeout.md`
  (AR closeout — evidence summary, boundary confirmations, recommended state).
- The Phase 4bn-AH / AI / AJ implementation reports + closeouts and the AK/AL/AM/AN/AO
  closeout lineage as recovered through the AK and AP restatements (arc reconstruction).
- Process standards under `docs/00-meta/process/` (phase-workflow, merge-closeout,
  operator-report, phase-prompt-template, phase-risk-tiering) — for method only.
- Committed source constants (read for frozen-contract verification only; none
  modified): `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py`
  — `SUCCESS_ACCURACY_UPLIFT_PP = 2.0` (line 249), `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP
  = 1.0` (line 250), `SUCCESS_MACRO_F1_UPLIFT = 0.03` (line 251), `LOCKED_COST_BPS_PER_SIDE
  = 8.0` (line 105), `LOCKED_ROUND_TRIP_COST_BPS = 16.0` (line 106),
  `CONTINUE_FOLLOWUP_CATEGORIES` (line 253), `CLAIM_SCOPE_ALLOWED` (line 264),
  `CLAIM_SCOPE_FORBIDDEN` (line 269).

The Phase 4bb-F canonical sidecar policy and Phase 4bn-L storage/budget policy are
cited here only as they bound the AH/AQ/AR artefact and footprint conventions; both
were recovered through the AH/AP/AR restatements and neither is altered by this memo.

## 6. Confirmation no data or generated output was read

Confirmed. This phase read **no** feature Parquet, **no** label Parquet, **no** raw
archive, **no** v002 terminal window, **no** sealed test split, and **no** local
generated AQ or AR JSON output artefact. All quantitative evidence below is quoted
**verbatim** from the committed Phase 4bn-AR verdict report / closeout (and, for the
15s arc, the committed AJ/AK reports). `test_rows_loaded = 0`. Only `git status` /
`git ls-files` / `git check-ignore` tracked-state checks touched `data/` paths, and
those inspect Git bookkeeping only, not file contents.

## 7. Confirmation no model or workflow was run

Confirmed. No model was trained, scored, calibrated, recalibrated, or used for
prediction / inference. No AR / AQ / AN / AH / AI / AJ builder, diagnostic, or
baseline was rerun. No feature selection, feature engineering, hyperparameter /
threshold search, resampling, cross-validation, second baseline run, or successor
experiment occurred. This memo designs and authorizes **nothing**; it records one
decision.

## 8. Summary of the full ML arc from 15s through long-horizon AR

The aggTrades-only microstructure ML arc has proceeded as a strictly gated,
separately-authorized sequence:

- **15s sub-arc.** Phase 4bn-AH built and leakage-proved a compact pre-v002 ML
  dataset spec over 400,001,695 rows / 275 dates (45 causal aggTrades features ↔
  `forward_direction_15s`), 0 boundary crossings, train-only transform. Phase 4bn-AI
  ran read-only descriptive diagnostics (near-binary target; regime-narrow late-2024
  validation/holdout; block-dependent labels). Phase 4bn-AJ ran the three frozen
  baselines once (majority / persistence / L2 multinomial-logistic): **L2 beat the
  majority floor by +5.03 pp and persistence by +2.96 pp on 15s validation accuracy,
  macro-F1 +0.145 over majority, date- and month-block agreement 1.000, no holdout
  reversal, and a ≥0.8 tail (0.633) that beat the floor** — a clean directional
  information result whose single binding limitation was **economic thinness at 15s**
  (only 2.47 % of validation moves clear the 16 bps round-trip cost). Phase 4bn-AK
  applied the frozen §16 gates and recorded `CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`,
  spending the arc's **single** follow-up on category 1, the **longer-horizon label
  memo** — precisely to test whether the demonstrated directional information persists
  **and** becomes economically material at 5m/30m/1h "where cost could plausibly be
  cleared."

- **Long-horizon sub-arc (the spent follow-up).** Phase 4bn-AL (longer-horizon label
  memo) → 4bn-AM (label contract spec) → 4bn-AN (single long-horizon label build:
  family `microstructure_labels_longhorizon_aggtrades_v001`, 275 dates /
  400,001,695 rows, 0 boundary crossings) → 4bn-AO (read-only long-horizon label
  diagnostics; validation |move| > 16 bps rises to **5m 34.95 % / 30m 64.28 % /
  1h 72.72 %** vs the 15s 2.47 % — the raw-move materiality the follow-up was
  designed to probe) → 4bn-AP (frozen long-horizon baseline preregistration: 5m
  primary, 30m/1h secondary; the three frozen baseline families and L2 constants; the
  §25 kill/continue/investigate criteria adopted verbatim from AE §16) → 4bn-AQ
  (single long-horizon ML dataset build: 45 features ↔ AN long-horizon labels,
  existing chrono split, train-only transform, leakage proof; no models) → **4bn-AR**
  (the single, run-once, no-search fixed baseline run over the AQ dataset).

- **AR outcome.** At the materiality-motivated longer horizons, the directional
  information did **not** persist cleanly. On the 5m primary the L2 model **fails to
  beat the strong majority floor** on accuracy (−0.222 pp validation) — a reversal of
  the 15s picture where it beat majority by +5.03 pp — while beating only the weak
  persistence floor (+2.128 pp). Four of the eight frozen continuation criteria fail;
  no hard-negative holdout reversal occurs; two ambiguous conditions match. AR
  recorded **`INVESTIGATE_AMBIGUOUS`**, which authorizes no further run and routes to
  this docs-only decision memo (Phase 4bn-AS).

## 9. Engineering / methodology successes

The arc's engineering and scientific-process discipline is a genuine success and is
recorded as such:

- **Clean leakage / split hygiene end-to-end.** Strict per-row alignment over
  `row_index, agg_trade_id, feature_timestamp_ms, source_transact_time_ms, utc_date`;
  0 earlier-split boundary crossings at every horizon; deterministic UTC-date chrono
  split with a 1-day boundary embargo excluded from all fitting and scoring; a
  train-only transform fitted on the train split and **applied, never recomputed**.
- **Preregistration honoured.** Every AR threshold, family, constant, target
  hierarchy, and verdict rule was frozen in AP/AE **before** the run and applied
  verbatim; the narrow-miss band could route STOP↔INVESTIGATE but could never
  fabricate CONTINUE, and was not triggered.
- **Two-step build/run separation.** The AH→AJ and AQ→AR pattern isolated any
  data/build error from any model result; the AQ namespace re-verified byte-identical
  after AR.
- **Integrity + budget controls.** Phase 4bb-F sidecars (all AQ/AR artefacts + SHA
  verified pre- and post-run); Phase 4bn-L budget preflights; numerical guards (all
  L2 weights finite); one-run/no-overwrite guards; compact-spec artefacts only (no
  re-materialised wide matrix, no row-level prediction dump).
- **Fail-closed boundary maintenance.** `v002_terminal_window_read = false`,
  `sealed_test_split_touched = false`, `test_rows_loaded = 0`, all non-authorization
  flags false, `flip_research_eligible(...)` never invoked, no data/model artefact
  committed — across the entire arc.

## 10. Predictive successes

The genuinely positive empirical findings, at their exact scope:

- **15s (prior sub-arc):** the frozen 45 causal aggTrades features carry **clean
  short-horizon directional information** about `forward_direction_15s` on the
  pre-v002 segment (majority +5.03 pp, persistence +2.96 pp, macro-F1 +0.145, block
  agreement 1.000, no holdout reversal, floor-beating tail).
- **Long-horizon 5m (this sub-arc):** the same feature set retains **measurable
  directional information over the persistence floor** — +2.128 pp accuracy on 5m
  validation and +2.097 pp on 5m holdout (positive on both, no full reversal), plus
  a small balanced-accuracy edge over the trivial floor (+0.779 pp) and a macro-F1
  edge over majority (+0.1138). This is a real, non-zero signal and is **not**
  dismissed.

These are **information-diagnostic** successes only (Phase 4bn-AE §8 a/b/c). No
success here is a tradability, profitability, or economic-edge finding.

## 11. Predictive failures

The decisive negative findings, at their exact scope:

- **Majority-floor failure at every long horizon.** On 5m validation the L2 model
  does **not** beat the strong majority ("up") floor on accuracy (−0.222 pp), and it
  loses to the majority floor by more at 30m (−1.348 pp) and 1h (−2.868 pp). The
  clean 15s majority-floor win (+5.03 pp) **did not carry to the longer horizons** —
  it inverted.
- **Balanced-accuracy uplift below bar.** +0.779 pp over majority on 5m validation,
  under the frozen +1.0 pp requirement.
- **Month-block non-unanimity.** 5m beats both floors in only 1 of 2 validation
  months.
- **Calibration unusable at 5m.** The ≥0.8 confidence tail (0.49656) does **not**
  beat the majority floor (0.51225); ECE ≈ 0.0583.
- **Secondaries cannot rescue.** 30m/1h are not positive frozen diagnostics (they
  fail the majority-floor accuracy bar) and cannot upgrade the 5m primary.

## 12. Exact AR evidence table

All figures quoted verbatim from the committed Phase 4bn-AR verdict report.

**5m primary — aggregate accuracy / balanced-accuracy / macro-F1:**

| Split | Baseline | Accuracy | Balanced acc | Macro-F1 |
|---|---|---|---|---|
| validation | majority    | 0.51225 | 0.33333 | 0.22582 |
| validation | persistence | 0.48876 | 0.33069 | 0.32796 |
| validation | **L2**      | 0.51004 | 0.34113 | 0.33958 |
| holdout    | majority    | 0.50416 | 0.33333 | 0.22345 |
| holdout    | persistence | 0.48686 | 0.32791 | 0.32627 |
| holdout    | **L2**      | 0.50783 | 0.33904 | 0.33771 |

**5m primary — L2 uplifts:**

| Metric | validation | holdout |
|---|---|---|
| accuracy vs majority | **−0.222 pp** | +0.368 pp |
| accuracy vs persistence | +2.128 pp | +2.097 pp |
| balanced-acc vs majority | +0.779 pp | +0.571 pp |
| macro-F1 vs majority | +0.1138 | +0.1143 |

**5m block / calibration / tail evidence:**

| Item | Value |
|---|---|
| validation dates beating both floors | 23/45 = 0.511 (bare majority) |
| validation months beating both floors | 1/2 (not unanimous) |
| holdout full reversal | false |
| ≥0.8 tail n / fraction | 1,562,179 / ≈0.02278 |
| ≥0.8 tail accuracy | 0.49656 |
| majority floor (5m validation) | 0.51225 |
| tail beats majority | **false** |
| ECE (5m) | ≈0.0583 |
| calibration verdict (5m) | **unusable** |

**Frozen continuation criteria — 5m outcomes (all eight must hold for CONTINUE):**

| # | Criterion | Outcome |
|---|---|---|
| 1 | accuracy uplift vs majority ≥ +2.0 pp | **FAIL** (−0.222) |
| 2 | accuracy uplift vs persistence ≥ +2.0 pp | pass (+2.128) |
| 3 | macro-F1 uplift vs majority ≥ +0.03 | pass (+0.1138) |
| 4 | balanced-acc uplift vs majority ≥ +1.0 pp | **FAIL** (+0.779) |
| 5 | beats both floors in > ½ validation dates | pass narrowly (0.511) |
| 6 | beats both floors in every validation month | **FAIL** (1/2) |
| 7 | no full holdout reversal | pass |
| 8 | ≥0.8 tail beats majority floor | **FAIL** (0.497 < 0.512) |

**Secondary horizons (diagnostic):** 30m/1h beat persistence on some information
metrics but fail the majority-floor accuracy requirement; neither is a positive
frozen secondary diagnostic; neither can upgrade or rescue the 5m primary.

**Exact AR verdict:** `INVESTIGATE_AMBIGUOUS`. **Exact matched ambiguity conditions:**
`mixed_date_and_month_block_evidence`; `information_suggested_but_not_clean`. **Final
AR interpretation:** the frozen 45-feature causal aggTrades set contains measurable
long-horizon directional information relative to the persistence floor, but not clean
enough for continuation.

## 13. Majority-floor interpretation

The majority baseline predicts the modal train class (**+1 / "up"** at all three
horizons) and is a **strong** floor on this near-binary, up-skewed target: 0.51225
(5m), 0.52901 (30m), 0.53516 (1h) on validation. **The L2 model did not beat this
floor on 5m validation accuracy (−0.222 pp), and lost to it by progressively more at
30m and 1h.** This is the arc's **main negative result** and it is **not minimized
here**: the specific question the long-horizon follow-up was authorized to answer —
does the demonstrated directional information persist at longer horizons — is answered
**no** against the decision-relevant floor. Beating a strong majority floor is the
central bar for "clean directional information," and the model fails it precisely
where the 15s model had passed it decisively.

## 14. Persistence-floor interpretation

The L2 model beat the persistence baseline (`sign(rolling_log_return_past_window_60s)`)
by **+2.128 pp on 5m validation and +2.097 pp on 5m holdout** — positive on both, no
full reversal. This is **genuine positive evidence** and is **not ignored**: it is the
`information_suggested_but_not_clean` condition made concrete, and it is why AR did not
record a clean STOP-forcing failure.

But its **weight must be read honestly**, and it is materially weaker than the
majority-floor failure:

- The persistence floor is **weak** at long horizons. A 60s past-return sign is a
  poor predictor of 5m/30m/1h-ahead direction on an up-skewed target; persistence
  accuracy (≈0.487–0.489) sits **below** the trivial base rate. Beating a
  below-base-rate floor is a **low bar**.
- Much of the L2 "win over persistence" is explained by L2 **tracking the base rate**
  (it essentially never predicts the rare flat class; its accuracy ≈ the up-rate ≈
  the majority floor), whereas persistence's roughly balanced sign predictions score
  worse on the imbalanced target. That is largely a class-prior effect, not a
  demonstration of strong minority-class discrimination.
- The one metric that isolates genuine above-trivial skill — **balanced accuracy over
  the majority floor** — is only **+0.779 pp**, below the frozen +1.0 pp bar. So the
  "information over persistence" is real but **thin**, and it fails the very gate
  designed to measure it cleanly.

The persistence-floor improvement therefore establishes that *some* directional
information exists, but not that it is clean, strong, or floor-beating in the sense
required for continuation.

## 15. Macro-F1 and class-imbalance interpretation

The L2 macro-F1 uplift over majority (+0.1138 validation) is **structural, not a clean
predictive win**, and must not be read as one:

- The majority baseline predicts **only** the dominant "up" class, so two of three
  per-class F1 terms are 0 and its macro-F1 is mechanically ≈0.226. **Any** model that
  predicts more than one class raises macro-F1 over that degenerate floor. Persistence
  (which predicts all three classes) already has macro-F1 ≈0.328; L2's 0.340 is only
  **≈+0.012 over persistence** — i.e. once compared to a non-degenerate floor, the
  macro-F1 edge is small. The large "+0.1138 over majority" number is an artefact of
  the majority floor's structural weakness on macro-F1, exactly the wrinkle the AK
  memo already flagged for the 15s arc.
- **Target structure.** The direction labels are strongly tilted toward +1/"up" and
  the flat/zero class is extremely rare (flat-class prevalence ≈0.02–0.06 %). This
  up-skew is what makes constant-"up" a strong **accuracy** floor and a weak
  **macro-F1** floor simultaneously — the two metrics point in opposite directions by
  construction.
- **Conceptual (no new target/model authorized).** The observed pattern — accuracy ≈
  majority, macro-F1 ≫ majority, balanced accuracy only marginally above trivial —
  is most consistent with the L2 model capturing a **small amount** of above-base-rate
  directional signal while otherwise defaulting toward the majority prior, i.e. a
  **metric trade-off dominated by class imbalance** rather than robust minority-class
  discrimination. Whether a different target formulation (e.g. a wider dead-band or a
  magnitude-conditioned direction) would reduce the majority floor and expose cleaner
  discrimination is an **open conceptual question only**; nothing here authorizes a
  new target, model, weighting, resampling, or threshold. The macro-F1 uplift is
  **not** treated as equivalent to a clean overall predictive win.

## 16. Date / month consistency interpretation

The 5m model beats both floors on **23/45 validation dates (0.511)** but only **1 of 2
validation months**. This is **mixed evidence, not clean robustness**:

- 23/45 is a **bare** majority — barely over half of dates, effectively coin-flip-like
  block agreement, versus the 15s arc's date agreement of **1.000**.
- The two validation months **disagree** (one passes, one fails), so the frozen
  every-month unanimity criterion fails. Because validation and holdout both sit in
  the same regime-narrow late-2024 window (per AI/AE), month-block disagreement inside
  that narrow window is a **stronger** warning, not a weaker one: even within a single
  regime the signal is not stable across its two months.
- This is exactly the frozen `mixed_date_and_month_block_evidence` condition: the date
  and month block signals disagree, so the block evidence supports "present but
  unstable," not "robust."

## 17. Holdout interpretation

The 5m holdout did **not** fully reverse: L2 uplift vs persistence stayed positive
(+2.097 pp) and vs majority moved slightly positive (+0.368 pp, still far below the
+2.0 pp bar). This absence of a hard-negative reversal is why AR is
`INVESTIGATE_AMBIGUOUS` rather than a STOP-forcing failure — it is a genuine (weak)
stability point and is credited as such.

The **central scientific constraint** it now imposes: this pre-v002 holdout has
**been evaluated** in AR. It is **no longer an untouched future-confirmation set.**
Any future follow-up **must not** describe this same holdout as unseen confirmation
data; reusing it as "independent confirmation" would be scientifically invalid. This
constraint is load-bearing for the decision in §22–§26.

## 18. Calibration / confidence-tail interpretation

The 5m ≥0.8 confidence tail is an **important failure** and is treated as such. The
tail exists (1,562,179 rows, ≈2.28 % of validation) but its accuracy (**0.49656**) is
**below** the majority floor (**0.51225**); ECE ≈0.0583; calibration verdict
**unusable**. The model's high-confidence predictions are therefore **worse than
predicting "up"**, which forecloses any "trade only when confident" reading. The model
probabilities are **not** actionable and **not** reliable, and are not described as
such anywhere in this memo. (30m/1h tails beat their floors but are overconfident —
diagnostic only, never a signal, and cannot rescue the 5m primary.)

## 19. Secondary-horizon interpretation

30m and 1h beat persistence on some information metrics but **fail the majority-floor
accuracy requirement** — indeed they lose to the majority floor by more than 5m does.
Neither is a positive frozen secondary diagnostic under the AP definition, and per the
frozen §24 hierarchy a secondary result **cannot** upgrade or rescue a failed 5m
primary. They corroborate the "information present but not clean, and degrading with
horizon" reading; they do not provide an independent route to continuation.

## 20. Consumed-holdout constraint

Restated as a standalone constraint because it is decisive: the pre-v002 holdout
(14 dates, late-2024) has now been scored under AR and is **spent** as confirmation
evidence. The arc therefore has **no remaining untouched confirmation set within the
studied pre-v002 segment.** The only genuinely-unseen evidence reserves that still
exist are the **v002 terminal window** and the **sealed test split** — both of which
are (a) explicitly out of scope for this phase, (b) precious one-shot resources, and
(c) not accessible without a separate future authorization and (for new periods) data
acquisition. A follow-up cannot manufacture untouched confirmation from already-scored
data; it would have to reserve genuinely new independent evidence, which raises its
cost and one-shot-consumption risk substantially.

## 21. Post-hoc rescue / multiple-testing risk

Any immediate rerun that changes **seed, epochs, learning rate, L2, batch size,
gradient clip, model family, class weights, sample weights, resampling, feature set,
thresholds, or calibration** would now be chosen **with knowledge of the AR results**
and is therefore **result-informed**. The AR evidence itself points to the tempting
rescue levers — the class imbalance suggests class weighting / a new target /
thresholding; the unusable calibration suggests recalibration; the thin balanced-acc
suggests more capacity — and **every one of these is a post-hoc rescue / garden-of-
forking-paths move**, not a hypothesis test. Trying several and reporting the best
would be textbook multiple-comparison inflation on a signal already shown to be
sub-threshold. The frozen anti-rescue posture (AE §16 "not relaxed after a result is
seen"; the project-wide no-rescue lineage) exists precisely to forbid this. Post-hoc
rescue risk here is **high** and weighs strongly against any same-data model
follow-up.

## 22. Case for stopping

The case for `STOP_LONGHORIZON_ML_ARC` is strong and, per the required decision
precedence, is evaluated first:

1. **The decisive result is a majority-floor failure.** On the 5m primary the model
   does not beat the strong majority floor (−0.222 pp), and loses by more at 30m/1h.
   The clean 15s majority-floor win did not carry to the horizons the follow-up was
   built to test — it inverted. This is the single most decision-relevant fact.
2. **Time consistency and calibration are too weak.** Bare 23/45 date agreement with
   month non-unanimity (mixed block evidence), and an unusable 5m calibration whose
   high-confidence tail is worse than the floor. Neither supports robustness or
   actionability.
3. **The persistence-floor improvement does not justify more model experimentation.**
   It beats only a below-base-rate floor, is largely a class-prior effect, and the
   metric that isolates genuine skill (balanced accuracy) is below its bar. A thin,
   sub-threshold signal is not a mandate for further model work.
4. **The consumed holdout and post-hoc risk make another same-data model study
   scientifically unattractive.** No untouched confirmation remains in-segment; any
   parameter/family/target/threshold change would be result-informed rescue with high
   multiple-testing risk.
5. **Further work would likely become rescue, not hypothesis testing.** The AR
   evidence has already surfaced the failure modes; the natural "next tries" are all
   forbidden rescue levers. The follow-up the 15s arc's single budget was spent on has
   now been run and has answered its question negatively.

Under decision precedence rules 4–5, the fact that the verdict is labelled
"ambiguous" is **not itself** evidence that another run is warranted, and ambiguity
must not be used to justify continuation by default.

## 23. Case for one bounded follow-up

For completeness, the strongest case for
`RECOMMEND_ONE_BOUNDED_FOLLOWUP_PREREGISTRATION_MEMO_NEXT` is stated and tested:

- The persistence-floor improvement (+~2.1 pp accuracy at 5m, holding on holdout) and
  the small positive balanced-accuracy edge, both surviving to holdout without a full
  reversal, could be read as a **scientifically meaningful unresolved question**: is
  there a genuine, if thin, above-trivial directional signal at 5m that a *cleanly
  preregistered, single-run confirmation on genuinely independent data* would either
  confirm or refute?
- The only candidate that could survive the anti-rescue requirements (§24) would be a
  **new-data confirmation study**: re-apply the **frozen** AR contract (same features,
  same model, same constants, same metrics, same verdict rule — **no** tuning, **no**
  new target, **no** threshold selection, **no** recalibration) to a genuinely new,
  never-scored independent evaluation reserve, preregistered before that reserve is
  read.

This case is stated honestly, but it does **not** prevail (see §24–§26).

## 24. Anti-rescue admissibility assessment

Testing each conceptual candidate follow-up class against the anti-rescue
requirements:

- **New independently-justified target formulation** (e.g. wider dead-band /
  magnitude-conditioned direction) — **inadmissible as motivated here.** It would be
  selected **because** the current target's up-skew created a strong majority floor
  the model failed to beat — i.e. changing the target to escape an observed failure.
  That is result rescue, not a new hypothesis, and it also requires a heavy new label
  build.
- **New independently-justified feature-family hypothesis** (e.g. bookTicker/mid-price
  features) — **inadmissible now.** This is the heavier new-data admissibility path
  the AK memo already deferred as premature; it is a new arc, not a bounded one-run
  study, requires new data acquisition, and is not motivated as a *confirmation* of
  the AR finding.
- **Class-structure diagnostic on the AR/AQ data** — **inadmissible as informative.**
  Any diagnostic on the already-scored validation/holdout adds no independent
  evidence (the holdout is consumed) and drifts toward threshold/weighting rescue.
- **New-data confirmation of the frozen contract** — **the only class that formally
  survives** the anti-rescue tests: it poses a genuinely new question (does the thin
  5m signal reproduce out-of-sample on unseen data?), changes nothing about the model,
  can be fully preregistered, and can reserve independent evidence. It clears the
  no-rerun / no-seed-only / no-tuning / no-sweep / no-threshold-selection / no-
  recalibration / reserve-independent-evidence bars.

So a follow-up class that is **not** rescue does exist in principle. The decision
therefore turns on the independent-confirmation feasibility (§25) and the
cost/benefit gate (§26), per decision-precedence step 3.

## 25. Independent-confirmation requirement

For the surviving new-data confirmation class to be legitimate it would need genuinely
**unseen** evidence, and here that requirement bites hard:

- The pre-v002 holdout is **consumed** (§20) and cannot be reused as confirmation.
- The only unseen reserves are the **v002 terminal window** and the **sealed test
  split** — precious one-shot resources, out of scope here, and requiring separate
  authorization; spending either to confirm a **sub-threshold, calibration-unusable,
  majority-floor-failing** signal would be a poor allocation of a scarce confirmation
  asset.
- Fresh data acquisition (a new period/symbol) is likewise unauthorized here and is a
  heavier undertaking than the finding warrants.

A **credible, proportionate** independent-confirmation design therefore does **not**
exist for this finding at this time: the only admissible design would burn a scarce
one-shot reserve (or new acquisition) to confirm a signal that — even if confirmed —
would remain sub-threshold and non-actionable.

## 26. Cost / benefit and expected-information-gain assessment

Even granting that a formally anti-rescue-clean confirmation design *could* be
constructed, its **expected information gain does not justify its cost and
multiple-testing risk**, and this is decisive:

- **Ceiling on the payoff.** The AR primary already **failed** the clean-continuation
  bar. A confirmation could, at best, show the thin persistence-floor / balanced-acc
  signal reproduces out-of-sample. That result would **still** be majority-floor-
  failing, calibration-unusable, and — by Phase 4bn-AE §8/§19 — **information-
  diagnostic only, authorizing no strategy/PnL/backtest/live path**. It unlocks
  nothing.
- **Cost / scarcity.** The only admissible confirmation would consume a precious
  one-shot reserve (v002 terminal / sealed test) or require new acquisition — a high
  price for a result that cannot change the arc's conclusion or open any downstream
  path.
- **Risk.** Keeping the arc open invites the forbidden rescue levers (§21) and extends
  what Phase 4bn-AE §18 explicitly designed as a **finite** arc — the 15s arc's single
  bounded follow-up has already been spent on this long-horizon study, which has now
  answered its question.

Expected information gain is **low**; cost and multiple-testing risk are **high**;
the payoff is capped below any decision-relevant threshold. The cost/benefit gate for
Decision B is **not** met.

## 27. Exact decision

**`STOP_LONGHORIZON_ML_ARC`**

## 28. Exact reasoning mapping

Mapping the decision to the required precedence and to the frozen evidence:

1. **STOP case evaluated first (§22):** the majority-floor failure is the decisive
   result; time consistency (bare 23/45 dates, 1/2 months) and 5m calibration
   (unusable; tail below floor) are too weak; the persistence-floor improvement is
   thin, below-base-rate-floor, and largely a class-prior effect; the consumed holdout
   and high post-hoc rescue risk make another same-data model study unattractive;
   further work would likely become rescue.
2. **Genuinely-new bounded hypothesis tested against anti-rescue (§24):** target /
   feature-family / class-structure candidates are inadmissible (rescue-motivated,
   heavier new arcs, or non-informative on consumed data); only a **frozen-contract
   new-data confirmation** formally survives.
3. **Independent-confirmation feasibility (§25) and cost/benefit (§26):** no credible,
   proportionate independent-confirmation design exists (the only admissible reserves
   are scarce one-shot assets, out of scope), and even a clean confirmation would be
   capped at a sub-threshold, non-actionable, information-diagnostic result that
   unlocks no path — so the cost/benefit gate fails. **Per decision-precedence step 3,
   when no credible independent-confirmation design exists, choose STOP.**
4. **Precedence rules 4–5 honoured:** the "ambiguous" label is not itself treated as
   evidence that another run is warranted; the decision is not defaulted to a
   follow-up merely because the verdict is called ambiguous.
5. **Precedence rules 6–7 honoured:** no third recommendation is invented and the
   decision is not left unresolved.

Therefore the arc is stopped.

## 29. Allowed claims

Capped at Phase 4bn-AE §8 (a)/(b)/(c), unchanged. The arc may claim only:

- (a) the frozen 45 causal aggTrades features contain **directional information** —
  clean at 15s (beats both floors) and, at the long horizons, measurable **over the
  persistence floor** at 5m (+~2.1 pp accuracy, holding on holdout) with a small
  balanced-accuracy edge, but **not** a clean lift over the strong majority floor and
  **degrading with horizon**;
- (b) the directional-sign reproduction of the v002 small-lift result on the earlier
  pre-v002 regime (as established in the 15s sub-arc);
- (c) a calibration / confidence-tail **assessment**: the 5m high-confidence tail is
  **unusable** (below the majority floor); 30m/1h tails beat their floors but are
  overconfident — ranking/diagnostic only, never a signal.

The single summarizing empirical claim: *the frozen causal aggTrades 45-feature set
carries measurable long-horizon directional information over the persistence floor at
5m but does not cleanly beat the strong majority floor, its 5m probabilities are
unusable, and the signal degrades with horizon — information is present but not clean
enough for continuation; the long-horizon ML arc is stopped on this evidence.*

## 30. Forbidden claims

Preserved verbatim (Phase 4bn-AE §8 / §19). Nothing in this memo may be cited as
evidence of tradability, profitability, economic edge, PnL, strategy viability,
signals, execution viability, backtest validity, spread/slippage adequacy, market
impact/depth adequacy, live-readiness, paper/shadow readiness, or production
suitability. The long-horizon raw-move materiality shares (validation |move| > 16 bps:
5m 34.95 % / 30m 64.28 % / 1h 72.72 %; 15s ref 2.47 %) and the locked
**8 bps/side · 16 bps round-trip** cost remain **descriptive context only** and
entered no target, model, loss, threshold, weighting, or verdict. The persistence-
floor improvement is **not** an economic edge. A STOP decision makes **no** trading
claim of any kind.

## 31. Strategy / PnL / backtest / live boundary

Absolute and unchanged. aggTrades-only data cannot express spread, slippage,
executable mid-price, order-book depth, or market impact; it therefore cannot support
any strategy / signals / PnL / backtest / Sharpe / hit-rate / turnover / position
sizing / execution / paper / shadow / live-readiness / deployment / exchange-write
claim. Every such path remains behind the **Phase 4bn-AE §19 M0-style mechanism-
admissibility gate**, which is preserved unsoftened; each capability additionally
requires its own separate authorization. None is authorized here.

## 32. Remaining project locks

Preserved verbatim: the Phase 4aw `flip_research_eligible(...)` always-raises
invariant (never invoked; `research_eligible` unchanged); the Phase 4ak M0
twelve-clause mechanism-admissibility gate and Phase 4al no-rescue constraints; the
Phase 4bb-F canonical sidecar policy; the Phase 4bn-L storage/budget policy; the
Phase 4bn-AE claim scope (§8) and §19 M0 boundary (8 bps/side · 16 bps round-trip);
the Phase 4bn-AP frozen model + verdict contract; the Phase 4bn-AQ dataset identity /
source bindings / transform / split / proof; and the exact Phase 4bn-AR metrics and
`INVESTIGATE_AMBIGUOUS` verdict (unchanged and not reinterpreted as a continuation
success). All prior strategy-arc verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 /
D1-A and the 5m / V2 / G1 / C1 threads) remain as recorded. All published
authorization flags remain `false`.

## 33. Recommended next state

**Remain paused.** The long-horizon aggTrades-only ML arc is recommended **stopped**
on the frozen Phase 4bn-AR evidence. No successor execution phase, no follow-up
preregistration memo, no model run, and no data acquisition is authorized or
recommended. The operator may: remain paused; request a merge prompt for Phase
4bn-AS; or, entirely separately and later, open an unrelated line of work under its
own fresh authorization (which this memo neither designs nor endorses).
`current-project-state.md` is left **unchanged**, matching the Phase 4bn-AH..AR
precedent (the update convention at this arc point is not clear/consistent; per the
operator instruction it is not updated and is recorded here as unchanged).

## 34. Explicit no-successor execution statement

Phase 4bn-AS authorizes **no** successor execution phase and generates **no** successor
or future-preregistration prompt. It does **not**, and does not authorize anyone to:
run, implement, or preregister any follow-up; generate a model-run, data-acquisition,
or preregistration prompt; start any new ML experiment; rerun the AR / AQ / AN / AH /
AI / AJ builders, diagnostics, or baselines; run a second fixed baseline, a fourth
model, tree models, neural networks, or ensembles; train / score / predict / infer;
perform feature selection / feature engineering / model selection / hyperparameter or
threshold search / calibration training / probability recalibration / alternate seeds
/ additional epochs / class or sample weighting / resampling / cross-validation; read
any feature or label Parquet, raw data, v002 terminal window, or sealed test, or load
any test row; inspect or mutate the local AQ or AR output namespaces; change the AR
verdict, metrics, or thresholds, or reinterpret AR as a continuation success; change
any published manifest, gate, split, sidecar, model configuration, or authorization
flag; do strategy / signals / PnL / backtest / Sharpe / hit-rate / turnover / position
sizing / execution / paper / shadow / live-readiness / deployment / exchange-write;
acquire data or call any endpoint; use credentials / `.env` / `.mcp.json` / MCP /
Graphify / WebSocket / user stream; commit anything under `data/microstructure/` or
`data/research/`; or commit `.claude/scheduled_tasks.lock`. A recommendation for a
future preregistration memo is **not** made by this phase; and even if one had been
made, it would not be authorization to execute it. **No successor execution is
authorized.** Do not merge to main and do not push unless explicitly instructed in a
later prompt; do not generate a merge-closeout or a successor prompt unless explicitly
instructed later.

## 35. Exact result state

`LONGHORIZON_ML_AMBIGUITY_DECISION_MEMO_COMPLETE__STOP_LONGHORIZON_ML_ARC_RECOMMENDED__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`
