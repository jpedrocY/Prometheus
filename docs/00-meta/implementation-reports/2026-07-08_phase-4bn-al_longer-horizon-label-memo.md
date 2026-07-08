# Phase 4bn-AL — Longer-Horizon Label Memo

## 1. Branch

`phase-4bn-al/longer-horizon-label-memo`

## 2. Base SHA

`205cdc90f8ac7aa4cd26f6e9d320ead875c05d3f`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AK merge
closeout. Verified in sync before branching.)

## 3. Phase type and strict scope

Docs-only **longer-horizon label design memo**. It is the selected Phase 4bn-AK
bounded follow-up (`longer_horizon_label_memo`, Phase 4bn-AE §16(a)), authorized by
a separate operator prompt for Phase 4bn-AL only. It reviews the completed Phase
4bn-AH / 4bn-AI / 4bn-AJ / 4bn-AK evidence, evaluates whether a future
longer-horizon (5m / 30m / 1h) label design is a reasonable next research contract,
compares candidate label families at the design level, assesses the
economic-materiality rationale relative to the locked cost, and records a decision.

It reads **no data**, builds **no label**, generates **no data file**, creates **no
namespace**, trains / scores / predicts **nothing**, reruns **no** builder /
diagnostics / baseline, and authorizes **no** successor execution phase. It is a
label-**design** decision only: *should Prometheus define a future longer-horizon
label contract, and if so, what should that contract be allowed to decide?* It does
**not** claim, and may not be cited as claiming, that longer horizons will be
tradable.

## 4. Files created / modified

Created (committed):

- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-al_longer-horizon-label-memo.md`
  (this report).
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-al_closeout.md`.

No source module, test, script, manifest, gate report, sidecar, split file, ML
config, research matrix, or `data/` artefact was created or modified. No dataset or
label namespace was created or mutated. `current-project-state.md` is **unchanged**
(see §29).

## 5. Exact documents / source inspected

Read-only (committed docs + committed source only; README treated as potentially
stale and **not** used as current-state authority):

- `docs/00-meta/current-project-state.md` (head + tail; navigational summary, not
  binding authority — its tracked tail stops at Phase 3k / 2026-04-29 and does not
  track the 4bn ML arc).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_ml-baseline-preregistration-contract-amendment.md`
  (via the frozen contract constants and the AK recovery; §8 claim scope, §9 target
  interpretation, §10 dependence policy, §11–§12 block/regime reporting, §13 metric
  registry, §14 calibration, §15 cost realism, §16 success/continue/kill + follow-up
  categories, §17 ambiguity, §18 arc budget/stopping rule, §19 strategy/PnL/backtest/
  live boundary).
- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ah_data-reading-ml-dataset-builder-single-run.md`
  and its `_closeout.md` / `_merge-closeout.md`.
- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ai_descriptive-dataset-diagnostics-no-models.md`
  and its `_closeout.md` / `_merge-closeout.md`.
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-aj_fixed-pre-v002-baseline-run-verdict.md`
  and its `_closeout.md` / `_merge-closeout.md`.
- `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-ak_ml-arc-decision-memo.md`
  and its `_closeout.md` / `_merge-closeout.md`.
- Process standards under `docs/00-meta/process/`
  (phase-workflow-standard, merge-closeout-standard, phase-risk-tiering-standard,
  operator-report-standard, phase-prompt-template) — for method only.
- Committed source constants (read for constant confirmation only; **none
  modified**):
  `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py`
  (`PRIMARY_TARGET = "forward_direction_15s"`, `PRIMARY_HORIZON_MS = 15000`,
  `TARGET_CLASSES = (-1, 0, 1)`, `LOCKED_COST_BPS_PER_SIDE = 8.0`,
  `LOCKED_ROUND_TRIP_COST_BPS = 16.0`, `CONTINUE_FOLLOWUP_CATEGORIES`,
  `CLAIM_SCOPE_ALLOWED`, `CLAIM_SCOPE_FORBIDDEN`, `CONTRACT_KNOWN_HORIZONS`,
  `FORBIDDEN_RAW_PRICE_COLUMNS`, `NON_AUTHORIZATION_FLAGS` all `False`);
  `src/prometheus/research/microstructure/labels_schema_v002.py`
  (`LABEL_HORIZONS_V002 = ("1s","5s","15s","60s")`,
  `LABEL_HORIZON_MS_V002 = (1000, 5000, 15000, 60000)`,
  `DIRECTION_THRESHOLD_POLICY_V002` = strict-sign / no-deadband / no-bp-threshold /
  no-threshold-optimization / no-cost-based-threshold, `NULL_CENSORING_POLICY_V002`
  = per-horizon independent envelope-terminal censoring);
  `pre_v002_fixed_baseline_run.py`, `ml_baseline_design_v002.py`,
  `ml_baseline_models_v002.py`, `ml_baseline_metrics_v002.py` (baseline family,
  frozen hyperparameters, cost lock, calibration/stability helpers) — read for
  constant confirmation only.

## 6. Confirmation no data files were read

Confirmed. This phase read **no** feature/label Parquet row, **no** v002 terminal
window, **no** sealed test split, **no** raw zip, **no** AH/AJ local result artefact
under `data/research/` or `data/microstructure/`, and called **no** endpoint. All
evidence was recovered from committed Markdown reports and committed source
constants. No file under `data/microstructure/` or `data/research/` was opened,
listed for content, hashed, or otherwise inspected (only `git status` /
`git ls-files` / `git check-ignore` tracked-state checks were run against those
paths).

## 7. Confirmation no AH builder / AI diagnostics / AJ baseline rerun occurred

Confirmed. The Phase 4bn-AH data-reading dataset builder was **not** re-run; its
one-run guard and output namespace were untouched. The Phase 4bn-AI descriptive
diagnostics were **not** re-run. The Phase 4bn-AJ fixed baseline runner (`majority`
/ `persistence` / `L2`) was **not** re-run. No model was trained, scored, or
evaluated; no metric was recomputed, revised, or re-derived. Every figure below is
quoted verbatim from the committed AH / AI / AJ / AK reports.

## 8. AK decision summary (recovered)

Phase 4bn-AK recorded, on the committed AJ evidence and the frozen Phase 4bn-AE §16
gates, the arc decision:

- **Final decision:** `CONTINUE_EXACTLY_ONE_BOUNDED_FOLLOWUP`
  (`CONTINUE_ONE_FOLLOWUP` under §16; the stricter `INVESTIGATE_AMBIGUOUS` reading of
  the macro-F1 caveat routes to the same AK memo under §17/§18 and resolves the same
  way).
- **Selected category (exactly one):** `longer_horizon_label_memo` (§16(a)).
- **Selected horizons:** 5m / 30m / 1h.
- **Other three categories rejected / deferred:**
  `bookticker_midprice_data_admissibility_memo` (premature before longer-horizon
  materiality; heavier new-data path); `code_only_evaluation_framework_extension` /
  block-bootstrap (polish over already-maximal 1.000 block agreement; does not touch
  the economic constraint); `fixed_capacity_model_comparison_memo` (capacity is not
  the evidenced bottleneck; highest model-shopping risk).
- **Follow-up not started by AK.** Selecting it consumes the single-follow-up
  budget; it requires a separate future operator prompt before any work begins. AK
  authorized no successor execution phase and recommended **remain paused**.

This Phase 4bn-AL is that separate operator prompt — but authorized **only** as a
docs-only design memo, not as a label build or data read.

## 9. AJ evidence summary (recovered, verbatim)

Phase 4bn-AJ ran the three pre-registered fixed baselines exactly once each over an
authorized row-level read of the AH-verified pre-v002 sources only (no v002
terminal, no sealed test, no raw zip, `test_rows_loaded = 0`, 0 embargo rows):

- Validation L2 accuracy **0.5453**; majority **0.4950**; persistence **0.5158**.
- **L2 uplift over majority = +5.03 pp; over persistence = +2.96 pp.**
- Validation **date-block agreement 1.000** and **month-block agreement 1.000** (L2
  beats the majority floor in every evaluated validation date and both validation
  months).
- **Holdout: no sign reversal** (holdout L2 0.5417 vs majority 0.5003;
  validation−holdout −0.0036; validation−train +0.0078 → no overfitting).
- **High-confidence tail (proba ≥ 0.8): accuracy 0.633, beats the majority floor
  0.4950** on every split, **but overconfident in level** (usable for
  ranking/diagnostic reading, not as calibrated probabilities).
- **Cost realism (descriptive only): 2.47%** of validation 15s moves have
  `|forward_log_return_15s| > 16 bps` round-trip (11.97% > 8 bps one-way; median
  |return| **2.53 bps**, mean 3.84 bps, p90 9.66 bps, p99 23.0 bps, max 180 bps).
  Holdout > 16 bps = 1.20%. Only ~1 in 40 15s moves even *in principle* clears the
  locked round-trip cost.
- **Recorded verdict: `CONTINUE_ONE_FOLLOWUP`**; `kill_reasons = []`. The target
  **remains information-diagnostic, not economic.**

## 10. AI / AH evidence summary (recovered)

**Phase 4bn-AI (descriptive diagnostics, no models):**

- **Near-binary 15s target.** `forward_direction_15s` flat/zero class is a ~1%
  minority in every split (train 1.18%, validation 1.48%, holdout 0.97%); the ±1
  directional classes are near-balanced (~49–50% each).
- **Block / dependence caveat.** The ~397M kept rows are **not** ~397M independent
  observations (heavy 15s label overlap); the natural decision blocks are **275 UTC
  dates / 9 UTC months**. Validation and holdout both sit in the same late-2024
  regime (regime-narrow window).
- **Continuous forward-return distribution not available from AH artefacts alone.**
  AH carried the categorical `forward_direction_15s` counts and the *past-window*
  return feature stats, but no location/dispersion/tail statistics of the continuous
  *forward* 15s log-return; that was measured only later, under authorization, during
  the AJ row-level baseline read.

**Phase 4bn-AH (data-reading dataset builder, single run):**

- **Leakage / split proof VALIDATED before any write.** Strict positional alignment
  over 4 keys + `utc_date` on all 400,001,695 rows, **0 mismatches**; per-horizon
  earlier-split boundary-crossing rows **= 0** at 1s/5s/15s/60s; deterministic
  UTC-date split; 0 embargo rows used; **45-column** feature allowlist with an empty
  forbidden-column scan; train-only transform fitted on train only.
- **No v002 terminal read** (`v002_terminal_window_read = false`; by-reference), **no
  sealed test** (`sealed_test_split_touched = false`), **`test_rows_loaded = 0`**.
- **Compact leakage-proof dataset specification** (not a re-materialised feature
  matrix — a full 400M×45 float64 matrix ≈ 144 GiB would breach the Phase 4bn-L
  125 GiB derived cap). **No ML / no strategy**: all 8 non-authorization flags
  `false`.

## 11. Recovered Phase 4bn-AE label / cost / claim-scope constraints

Recovered verbatim / by close paraphrase from the frozen
`pre_v002_ml_dataset_contract.py` constants and the committed AE / AK memos:

- **Allowed claim scope (§8 / `CLAIM_SCOPE_ALLOWED`):** only (a) short-horizon
  **directional information**; (b) **v002 small-lift sign reproduction**; (c)
  **calibration / confidence-tail** assessment.
- **Forbidden claim scope (§8 / `CLAIM_SCOPE_FORBIDDEN`):** tradability;
  profitability; strategy viability; execution viability; slippage/spread adequacy;
  live-readiness; paper/shadow readiness; PnL; backtest validity; production
  suitability; economic significance.
- **Locked cost (§11.6):** `LOCKED_COST_BPS_PER_SIDE = 8.0`,
  `LOCKED_ROUND_TRIP_COST_BPS = 16.0`. **Descriptive only.**
- **Cost-realism policy (§15):** report the forward-return distribution and the
  share > 16 bps **descriptively only** — **no trading rule, no cost-aware label, no
  PnL** at the evaluation stage. A very small > 16 bps share forecloses an economic
  reading but does not by itself kill the arc.
- **Dependence policy (§10, Option 1):** row-level metrics descriptive only; unit of
  decision evidence is the UTC **date/month block**; no per-row significance / p-value
  / confidence-interval language until a future dependence-aware method exists;
  decimation reserved-not-adopted.
- **Direction-threshold lock (v002):** `forward_direction_H` derived strictly from
  the sign of `forward_log_return_H` at a **strict zero-log-return threshold**; **no
  deadband, no bp threshold, no threshold optimization, no cost-based threshold** —
  i.e. the target is **non-economic by construction**.
- **Existing label family:** `microstructure_labels_aggtrades_v001` defines horizons
  **1s / 5s / 15s / 60s only** (max 60s). 5m / 30m / 1h are **not** in the existing
  family, so any longer-horizon label is a **new label layer**.
- **§16 follow-up categories** (exactly four; a continue authorizes exactly one).
- **§18 arc budget / stopping rule:** the arc is finite and must close or authorize
  exactly one bounded follow-up; every phase is separately operator-authorized.
- **§19 strategy / PnL / backtest / live boundary (absolute):** no baseline result,
  however strong, authorizes any strategy path; that requires a future **M0-style
  mechanism-admissibility memo** clearing M0.5 cost realism at 8 bps/side · 16 bps
  round-trip, execution feasibility, slippage/spread (which aggTrades-only data
  cannot support — mid/book required), label economic relevance (the 15s strict-sign
  target is non-economic), strategy admissibility vs the retained rejections, and the
  no-rescue constraints — **plus** separate authorization for each of
  strategy/signals/PnL/backtest/paper-shadow/live/exchange-write.

## 12. Problem statement for the 15s label

The existing primary target `forward_direction_15s` has a **demonstrated but
non-economic** character:

- **Short-horizon directional information exists.** The AJ L2 baseline beats both the
  majority (+5.03 pp) and persistence (+2.96 pp) floors, in every validation date and
  both validation months (block agreement 1.000), with no holdout sign reversal — a
  clean, regime-stable-within-window information-diagnostic result under §8(a)/(b).
- **Economic materiality is thin at 15s.** Only **2.47%** of validation 15s moves
  (1.20% holdout) exceed the locked 16 bps round-trip cost; the *median* absolute 15s
  move is **2.53 bps** and the mean 3.84 bps — roughly an order of magnitude below the
  round-trip cost. Even the p90 move (9.66 bps) does not clear 16 bps round-trip.
- **The 15s strict-sign target is not a trade signal.** It is derived by strict sign
  of the forward log-return at a zero threshold, with no deadband and no cost
  threshold; getting the *sign* right on a ~2.5 bps move is economically irrelevant
  once 16 bps of round-trip cost is charged. §8/§19 cap every claim at the
  information-diagnostic level regardless.
- **Residual microstructure limitations.** The labels are computed from **aggTrades
  (last-trade price) only**, so the 15s directional target may partly reflect
  **bid-ask bounce** and cannot be reconciled against a mid-price; aggTrades-only data
  cannot express spread or slippage. This is a limitation of the *data*, orthogonal to
  the choice of horizon.

The binding limitation is therefore **economic thinness / non-economic label
construction at 15s**, not a lack of directional information. That is precisely what a
longer-horizon inquiry targets.

## 13. Rationale for considering 5m / 30m / 1h

Longer horizons are a **conceptually and methodologically admissible** next design
question, for the following reasons — none of which asserts that they *will* be
tradable:

- **Larger raw moves.** Price dispersion grows with horizon. Over 5m / 30m / 1h the
  typical absolute move is materially larger than at 15s, so a larger fraction of
  moves would, in principle, exceed the 16 bps round-trip cost. (Under a diffusive
  null, dispersion scales roughly with the square root of elapsed time; real BTC
  returns are fat-tailed and autocorrelated, so this is only a **qualitative
  intuition**, not a quantitative claim. The actual 5m / 30m / 1h forward-return
  distributions are **unmeasured** and cannot be stated here — see §14 and §26.)
- **More economically interpretable.** A "did the price move by more than round-trip
  cost over the next 5m / 30m / 1h" question is closer to an economically meaningful
  quantity than "the strict sign of the next ~2.5 bps of 15s drift."
- **Reduced microstructure-bounce sensitivity.** Bid-ask bounce is a sub-second,
  ~one-tick artifact; over 5m+ the signal-to-bounce ratio improves, so a
  longer-horizon target is a cleaner directional/materiality quantity even on
  aggTrades-only data (though it still does not provide mid/book realism — §17).

These upsides are counterweighted by **new risks** that a longer-horizon design must
confront (and which are the primary reason a *design memo* — not a build — is the
correct next step):

- **Feature-target staleness / signal decay.** The 45-feature allowlist is built from
  **short-memory microstructure** windows (order-flow imbalance, trade intensity,
  recent past-window returns). Their predictive relationship to the *sign/materiality
  of a 1h-ahead move* is very plausibly **much weaker** than to a 15s-ahead move. The
  AJ-demonstrated information may attenuate or vanish at longer horizons — an open
  question a future build would test, not a foregone conclusion in either direction.
- **Regime drift.** A 1h forward window mixes far more of the price path (and more
  regime content) into a single label; the feature→target map is more likely to be
  non-stationary at longer horizons, and the existing validation/holdout window is
  already regime-narrow (late-2024).
- **Lower sample independence / heavier overlap.** 15s labels already overlap heavily;
  at 1h consecutive rows' forward windows overlap almost entirely, collapsing the
  effective independent-sample count. The §10 date/month block structure (275 dates /
  9 months) becomes even more binding — there are far fewer effectively-independent
  long-horizon observations per block.
- **Censoring near segment / envelope ends.** Per-horizon envelope-terminal censoring
  (`NULL_CENSORING_POLICY_V002`) drops rows whose forward endpoint exceeds the
  segment/envelope terminal. At 60s this drop was negligible (AH holdout censored drop
  = 42); at 1h it is ~60× larger per boundary and grows with H, meaningfully reducing
  usable rows near each segment end and near the pre-v002 `END_DATE` (2024-11-30).

## 14. Candidate label families (design-level)

Evaluated at the design level only; **none is adopted or built here**. The
recommendation in §19 favours the most conservative, most diagnostic option.

1. **Strict sign of forward log-return at 5m / 30m / 1h** (mirror the v002
   `DIRECTION_THRESHOLD_POLICY_V002`). *Pro:* directly comparable to the existing 1s/
   5s/15s/60s family; simplest; preserves the non-economic-by-construction posture and
   the existing leakage machinery. *Con:* still **non-economic** — sign at longer
   horizons says nothing about magnitude vs cost, so it does **not** by itself answer
   the economic-materiality question. Admissible; necessary-but-insufficient on its
   own.

2. **Cost-aware ternary label** using a **fixed, pre-registered** ±16 bps (or ±8 bps
   one-way) threshold: +1 if forward return > +threshold, −1 if < −threshold, 0
   (neutral) otherwise. *Pro:* directly encodes economic materiality. *Con:* §15
   currently forbids a cost-aware **label** at the evaluation stage; it edges toward
   threshold/deadband territory that the v002 lock deliberately excluded, and a moving
   or optimized threshold would be forbidden **threshold optimization**. Admissible
   **only** if the threshold is fixed to the locked cost, pre-registered, never
   optimized, and framed as a **label-design** decision — not smuggled in as a trading
   rule. Recommended to be **evaluated but not adopted-by-default** by the future spec
   memo.

3. **Magnitude-aware / material-move label** (e.g. binary "did `|forward return|`
   exceed a fixed pre-registered threshold over the horizon"). *Pro:* captures
   materiality directly and symmetrically; avoids committing to a direction. *Con:*
   same fixed-threshold discipline as (2); a magnitude label answers "is the horizon
   economically material" but discards direction. Useful as a **diagnostic companion**,
   not necessarily the model target.

4. **Abstain / neutral-band (deadband) design** — moves within ±band labelled
   neutral/do-not-act. *Pro:* natural economic-relevance encoding. *Con:* departs from
   the v002 strict-sign-no-deadband lock; the band is a threshold decision that must be
   fixed, pre-registered, and justified; risks becoming an implicit trading rule.
   Admissible only under the same fixed/pre-registered discipline; **not** a default.

5. **Multi-horizon diagnostic label family** — extend the existing strict-sign family
   pattern to add 5m / 30m / 1h **alongside** 1s/5s/15s/60s, **and** record the
   **continuous forward-return distributions** at each new horizon (location,
   dispersion, tails, and the descriptive share of moves clearing 8 bps / 16 bps).
   *Pro:* most conservative; reuses the proven leakage/censoring machinery; answers the
   economic-materiality question **descriptively** (via the recorded distributions and
   cost-clearing shares) **without baking a cost threshold into the target**; keeps
   full comparability with the existing family. *Con:* strict-sign component remains
   non-economic on its own — but the recorded continuous distributions supply the
   economic-materiality diagnostic that strict-sign lacks. **Recommended default.**

6. **Do-not-adopt alternatives** (violate project boundaries): any label using
   **future-derived features**; any **optimized / tuned / cost-fitted** threshold; any
   label requiring **mid/book data** we do not have; any label that bakes in a
   **trading rule, PnL, position sizing, or execution assumption**; any label defined
   on the **v002 terminal or sealed test** windows.

## 15. Horizon-by-horizon analysis

Analysed separately, using committed evidence and design reasoning only. **No
empirical 5m / 30m / 1h return distribution is invented** — those are unmeasured and
would require a separately-authorized build (§18, §26).

**5m (300s; 5× the existing 60s max):**

- *Materiality:* raw moves are qualitatively larger than at 15s, so a larger share
  should in principle clear 16 bps (magnitude unmeasured).
- *Signal persistence:* closest to the regime where the AJ microstructure features
  demonstrably carry directional information; the feature→target relationship is most
  likely to **retain** some strength here. Best signal-persistence-vs-materiality
  tradeoff.
- *Overlap / censoring:* overlap grows but remains moderate; per-horizon censoring at
  5m is small relative to the pre-v002 span. Lowest-risk of the three.
- **→ Most defensible primary / lead horizon.**

**30m (1800s; 30× the 60s max):**

- *Materiality:* moves larger still — more likely to clear cost by magnitude.
- *Signal persistence:* the microstructure feature→target link is **substantially
  weaker** at 30m; this becomes a "does any residual directional information survive
  well beyond microstructure memory" test.
- *Overlap / censoring:* heavy overlap (effective sample collapse); censoring near
  segment/envelope ends grows materially.
- **→ Secondary / diagnostic horizon.**

**1h (3600s; 60× the 60s max):**

- *Materiality:* largest raw moves — most likely to clear cost by magnitude alone.
- *Signal persistence:* **weakest** feature→target link; "larger moves" and
  "predictable-from-microstructure" pull hardest in opposite directions here. High risk
  the AJ signal does not persist; and even if moves clear cost, that is **magnitude,
  not predictability**.
- *Overlap / censoring:* **heaviest** overlap and largest censoring; 1h forward windows
  mix the most regime content into each label; still comfortably within the existing
  1-day boundary embargo (1h ≪ 1 day), so cross-split leakage remains preventable, but
  effective independence is lowest.
- **→ Secondary / diagnostic horizon; treat any favourable 1h magnitude result with
  particular caution (magnitude ≠ edge, and predictability is most doubtful).**

Design conclusion: a future spec memo should cover **all three at the design level**
for comparison, designate **5m as the primary / lead horizon**, and treat **30m and
1h as secondary diagnostic horizons**.

## 16. Leakage / split / censoring implications for a future contract

Any future longer-horizon label contract must preserve every Phase 4bn-AH leakage
invariant, extended to the new horizons:

- **Completed-event discipline.** The target must be computed strictly from the
  **future horizon endpoint** of a completed event, exactly as `forward_log_return_H`
  is today; no partial / in-progress horizon.
- **No future-derived features.** The 45-feature causal allowlist must remain
  **past-only**; longer horizons must **not** leak any future information into features,
  and the forbidden-column scan (`FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`,
  `FORBIDDEN_RAW_PRICE_COLUMNS`) must remain empty of violations.
- **Split-boundary handling / embargo.** The chrono split
  (`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`) and its **1-day
  boundary embargo** must be preserved. Because 5m / 30m / 1h are all **≪ 1 day**, the
  existing 1-day embargo remains **sufficient** to prevent forward-window leakage
  across the train/validation/holdout boundaries — but any row whose forward endpoint
  crosses an earlier-split boundary must be **censored** (target dropped), exactly as
  the AH proof recorded **0** boundary-crossing rows at 1s/5s/15s/60s.
- **Censoring near segment / envelope ends.** Per-horizon envelope-terminal censoring
  (`NULL_CENSORING_POLICY_V002`) must extend to the new horizons; the **censored
  fraction grows with H** and must be **measured and reported**, not assumed. This is a
  first-class contract obligation for 5m/30m/1h (unlike the near-zero drops at 60s).
- **v002 / sealed-test exclusion.** Longer-horizon labels on the pre-v002 segment must
  still exclude the **v002 terminal** (2024-12-01..2025-02-28) and the **sealed test**
  (2025-02-14..2025-02-28); `test_rows_loaded` must remain **0**;
  `v002_terminal_window_read = false`; `sealed_test_split_touched = false`.
- **Time discipline.** UTC Unix-ms / `open_time` / `source_transact_time_ms`
  discipline and the strict alignment-key set
  (`row_index`, `agg_trade_id`, `feature_timestamp_ms`, `source_transact_time_ms`
  + `utc_date`) must be preserved for the new horizons.
- **Dependence.** §10 remains in force: decision evidence at the UTC date/month block
  level; no per-row significance language. Longer-horizon overlap makes this
  **more** important, not less.

## 17. Storage / budget / build implications

- **New label layer.** 5m / 30m / 1h are absent from `LABEL_HORIZONS_V002`
  (1s/5s/15s/60s only), so this is a **new label layer**, not a config toggle. It adds
  ~2 columns per horizon (`forward_log_return_H`, `forward_direction_H`) plus per-horizon
  censored/support flags, over 400,001,695 rows across 275 partitions.
- **Storage.** Labels are **narrow** (a handful of columns), so a longer-horizon label
  layer is modest — of order single-digit to low-tens of GiB, far below the full
  400M×45 matrix (~144 GiB) that AH deliberately avoided by writing a **compact
  dataset specification** rather than a materialised matrix. Any future build should
  **preserve the AH compact-spec posture** and remain within the Phase 4bn-L 125 GiB
  derived cap; a budget preflight (as in AH) would be required.
- **Compute.** Computing forward endpoints at 300s/1800s/3600s offsets is a full pass
  over the 400M aggTrades rows — comparable in cost to the existing label build;
  bounded and one-run-guarded, but non-trivial.
- **None authorized here.** This memo authorizes **no** build, **no** storage
  allocation, and **no** namespace. Any build/data-read requires its own separate
  authorization beyond even the recommended spec memo (§19–§20).

## 18. Interaction with the bookTicker / mid-price deferred path

- Longer horizons **reduce** bid-ask-bounce sensitivity but do **not** provide
  mid-price or order-book realism. On aggTrades-only data, longer-horizon labels can
  answer *"do raw last-trade-price moves clear 16 bps materially more often at
  5m/30m/1h?"* but **cannot** answer *"can we execute at those prices net of spread and
  slippage?"*
- The `bookticker_midprice_data_admissibility_memo` (Phase 4bn-AE §16(b)) therefore
  **remains the required, still-deferred, still-unauthorized** gate for execution
  realism. Longer-horizon labels are **complementary to**, not a substitute for, that
  path.
- Sequencing rationale (consistent with AK §17): the longer-horizon label question is
  the **cheaper prior gate** — if longer-horizon moves are still rarely material, the
  heavier mid/book admissibility investment is unwarranted; if they are materially
  larger, that would **strengthen** (but not authorize) the future case for the mid/book
  path. Either way, the mid/book path stays behind its own separate authorization.

## 19. Interaction with strategy / PnL / backtest / live boundary

Absolute and unsoftened (Phase 4bn-AE §19):

- **Even a maximally favourable longer-horizon label result authorizes nothing toward
  strategy.** A "larger raw moves clear cost more often at 5m/30m/1h" finding is about
  **label economic-materiality**, not tradability, edge, or PnL.
- Any strategy / signals / threshold-or-confidence-gated trading / backtest / PnL /
  Sharpe / hit-rate / position sizing / execution / paper / shadow / live-readiness /
  exchange-write path remains behind a future **M0-style mechanism-admissibility memo**
  clearing M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution feasibility,
  slippage/spread (which **aggTrades-only data cannot support** — mid/book required),
  label economic relevance, strategy admissibility vs the retained rejections, and the
  no-rescue constraints — **plus** separate authorization for each such capability.
- This memo does not, and cannot, move any part of that boundary.

## 20. Recommended AL decision

**`RECOMMEND_LONGER_HORIZON_LABEL_CONTRACT_MEMO_NEXT`.**

Reasoning (evidence-driven; not overfit to AJ optimism, not biased toward closing):

- The AJ evidence establishes **real, regime-stable-within-window short-horizon
  directional information** whose **single binding limitation is economic thinness at
  15s** (2.47% > 16 bps; median move 2.53 bps). Longer horizons directly target that
  limitation, and Phase 4bn-AH/AE §9 explicitly names them as *"where cost could
  plausibly be cleared."* AK selected exactly this follow-up.
- A **docs-only label-contract / spec memo** commits **nothing** — no data, no build,
  no strategy. It is the **cheapest possible** next step and it forces the real design
  decisions (which horizons; strict-sign vs cost-aware vs magnitude-aware; censoring
  policy; storage; leakage invariants; claim scope) to be made **deliberately and
  pre-registered** rather than improvised at build time.
- **Closing (option B) would be premature.** The principal risk — that microstructure
  features lose predictive power at longer horizons — is **unmeasured**. Closing on
  unmeasured pessimism is as much an error as continuing on unmeasured optimism; and it
  would forfeit the one cleanly-motivated continuation AK already selected, at
  effectively zero further cost for a design memo.
- **Insufficient-evidence (option C) does not apply.** The unmeasured forward-return
  distributions block a *build* recommendation, **not** a *design-memo* recommendation:
  the design-level analysis (§12–§19) is fully decidable from committed evidence. The
  memo's job is a **safe label-design decision**, and that decision is reachable now.

This is **not** a trading, strategy, PnL, backtest, economic, or live-readiness
decision, and it does not claim longer horizons will be tradable. It recommends only
that Prometheus **define a future longer-horizon label contract at the design level**,
tightly bounded.

## 21. Recommended next memo scope (option A)

Recommend **exactly one** next **docs-only** phase: a **longer-horizon label
contract / spec memo** (design + pre-registration only; **no** build, **no** data
read, **no** namespace). Its scope should be:

- **Horizons:** cover **all three (5m / 30m / 1h) at the design level** for
  comparison, but designate **5m as the primary / lead horizon** (best
  signal-persistence-vs-materiality tradeoff) and **30m / 1h as secondary diagnostic
  horizons** (§15).
- **Label family:** adopt the conservative **multi-horizon diagnostic family** default
  (§14 option 5) — extend the existing strict-sign family to the new horizons **and**
  specify recording of the **continuous forward-return distributions** and the
  descriptive share of moves clearing 8 bps / 16 bps at each horizon (economic
  materiality as a **descriptive diagnostic**, not a baked-in target). Evaluate — but
  do **not** adopt-by-default — the cost-aware ternary / magnitude / deadband options
  (§14 options 2–4), and only under a **fixed, pre-registered, never-optimized**
  threshold tied to the locked 16 bps; explicitly exclude the do-not-adopt set (§14
  option 6).
- **Leakage / censoring / storage pre-registration:** carry forward every §16 leakage
  invariant, require per-horizon censored-fraction reporting, preserve the AH
  compact-spec posture and the Phase 4bn-L 125 GiB cap, and preserve v002/sealed-test
  exclusion and the §10 dependence posture.
- **Claim scope:** the memo must keep every claim within §8(a)/(b)/(c) and the §19
  boundary; it must state that longer horizons are evaluated for **information +
  economic-materiality diagnostics only**, never for tradability.
- **Evidence needed before any build:** the spec memo must **pre-register** the exact
  horizon set, label policy, censoring/embargo/storage plan, leakage invariants, and
  success/interpretation scope; and it must state that **any actual longer-horizon
  label build or data read requires its own further separate operator authorization**
  beyond the spec memo. The unmeasured 5m/30m/1h forward-return distributions are the
  key quantity a later authorized build would produce — they must not be assumed or
  invented.

## 22. Explicit no-prompt / no-successor statement for the recommended memo (option A)

This memo **does not generate** the recommended next memo's prompt and **does not
authorize** any successor execution phase. The recommended longer-horizon label
contract / spec memo begins **only** under a **separate future operator prompt**, and
even that memo would be **docs-only**; a build or data read is a further,
separately-authorized step beyond it. Selecting/recommending this memo consumes the
single Phase 4bn-AK follow-up budget — the other three §16 categories remain
deferred and unauthorized.

## 23. If rejecting / closing — N/A

Not applicable; the decision is `RECOMMEND_LONGER_HORIZON_LABEL_CONTRACT_MEMO_NEXT`,
not closure. (Had the evidence and design reasoning shown that longer horizons should
not be pursued — e.g. if committed evidence already foreclosed any plausible
materiality or signal persistence — this memo would have recorded
`RECOMMEND_CLOSE_LONGER_HORIZON_FOLLOWUP_NO_BUILD`, preserved all AK/AJ evidence, and
remained paused.)

## 24. If ambiguous — N/A

Not applicable; a safe design-level recommendation is reachable from committed
evidence (§20). (Had a genuine gap blocked even a design-level recommendation, this
memo would have recorded `RECORD_INSUFFICIENT_EVIDENCE_REMAIN_PAUSED` with the exact
evidence gap.) The unmeasured 5m/30m/1h forward-return distributions are a blocker to
a **build**, not to a **design memo**, and are recorded as such (§20–§21, §26).

## 25. Allowed claims preserved

Preserved verbatim (§8 / `CLAIM_SCOPE_ALLOWED`). The AJ result licenses **only**: (a)
the 45 causal aggTrades features contain **short-horizon directional information**
about `forward_direction_15s` on the pre-v002 segment; (b) the **directional sign** of
the v002 small-lift result **is reproduced** on the larger, earlier pre-v002 regime;
(c) the probability outputs' **calibration / confidence tail** beats the majority floor
on accuracy but is overconfident in level — usable for ranking/diagnostic reading, not
as calibrated probabilities. This AL memo adds **no** new empirical claim beyond
(a)/(b)/(c); its longer-horizon reasoning is **design-level and qualitative**, and it
invents **no** empirical longer-horizon distribution.

## 26. Forbidden claims preserved

Preserved verbatim (§8 / `CLAIM_SCOPE_FORBIDDEN`, §19). Nothing in this memo may be
cited as evidence of: tradability; profitability; strategy viability; execution
viability; slippage/spread adequacy; live-readiness; paper/shadow readiness; PnL;
backtest validity; production suitability; economic significance. The
2.47%-of-moves-clear-cost figure is descriptive context, **not** evidence of edge.
`forward_direction_15s` remains an **information-diagnostic, non-economic** target that
may embed bid-ask bounce (aggTrades-only, no mid/book). **This memo does not claim
longer horizons will be tradable, profitable, or economically material** — it claims
only that a future longer-horizon label **design** is a reasonable next research
contract, and that the actual 5m/30m/1h return distributions are **unmeasured** and
require a separately-authorized build. The locked cost reference remains **8 bps per
side / 16 bps round-trip**. The §19 strategy/PnL/backtest/live boundary is absolute and
unsoftened.

## 27. Exact validation commands and results

Docs-only phase (no source/test/script changed), so no pytest/ruff/mypy required.

- `git rev-parse --abbrev-ref HEAD` (pre-branch) → `main`. ✅
- `git rev-parse main` / `origin/main` / `HEAD` (pre-branch) → all
  `205cdc90f8ac7aa4cd26f6e9d320ead875c05d3f`. ✅
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`. ✅
- `git checkout -b phase-4bn-al/longer-horizon-label-memo` → branch created at base
  SHA `205cdc90…`. ✅
- `git ls-files data/microstructure/` → **0 tracked**. ✅
- `git ls-files data/research/` → **0 tracked**. ✅
- `git check-ignore -v data/microstructure/` → `.gitignore:85`. ✅
- `git check-ignore -v data/research/` → `.gitignore:88`. ✅
- `.claude/scheduled_tasks.lock` → `git check-ignore` returns nothing; left
  **untracked and not committed**. ✅
- `git diff --check` → clean. ✅
- `git diff --name-status main..HEAD` (after commit) → only the two new
  `docs/00-meta/implementation-reports/2026-07-08_phase-4bn-al_*.md` files. ✅
- No data-output tracked-file check → no file under `data/` staged or committed. ✅

(Exact post-commit command outputs are reproduced in the closeout and the final
operator report.)

## 28. Git status

Before commit: the two new Phase 4bn-AL docs untracked, plus the transient
`?? .claude/scheduled_tasks.lock` (not committed). No `data/` file staged. Final
committed SHA and post-commit `git status --short` are reproduced in the closeout and
the final operator report.

## 29. current-project-state.md update note

`current-project-state.md` is **left unchanged** by this phase. The update convention
at this point in the arc is **not clear/consistent**: the docs-only decision memos
Phase 4bn-AE and 4bn-AG each added a `current-project-state.md` paragraph, but the
five most recent phases — Phase 4bn-AH, 4bn-AI, 4bn-AJ, and 4bn-AK — did **not** (no
paragraph exists for any of them; the doc's tracked tail still stops at Phase 3k /
2026-04-29), and the doc is additionally flagged by the Phase 4bn-AE external review
as an oversized/stale single-source-of-truth pending a consolidation memo. Per the
operator instruction ("if there is no clear current-project-state update convention
for this point, do not update it; record that it remains unchanged"), and matching the
immediate AH/AI/AJ/AK precedent, this phase records the memo **only** in this report +
closeout and leaves `current-project-state.md` untouched. Should the operator prefer
an additive paragraph at merge time, that can be added under a later merge prompt.

## 30. Result state and explicit no-successor execution statement

**Result state:**
`LONGER_HORIZON_LABEL_MEMO_RECORDED__LABEL_CONTRACT_MEMO_RECOMMENDED__NO_LABEL_BUILD__NO_DATA_READ__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

**Recommended next state:** **Remain paused.** The longer-horizon label memo is
recorded and recommends exactly one next **docs-only** label contract / spec memo
(5m/30m/1h at design level; 5m primary; conservative multi-horizon diagnostic family
default). The recommended memo is **not started** and requires a **separate future
operator prompt**. No label build, no data read, no strategy/signals/PnL/backtest/
paper-shadow/live/exchange-write path is authorized (all remain behind their own
separate authorizations and, for any trading path, the §19 M0-style gate).

**Explicit no-successor execution statement.** Phase 4bn-AL authorizes **no**
successor execution phase. It does **not**, and does not authorize anyone to:
generate the recommended memo's prompt; write, build, or generate any longer-horizon
label or label layer; create any new label/dataset namespace; read any feature/label
Parquet / v002 terminal / sealed test / raw zip / AH / AJ data artefact; acquire data
or call any endpoint; train / score / predict / infer; run new diagnostics; perform
feature selection / threshold optimization / model selection / hyperparameter search;
rerun the AH builder, AI diagnostics, or AJ baselines; do strategy / signals / PnL /
backtest / Sharpe / hit-rate / position sizing / execution / paper / shadow /
live-readiness / deployment / exchange-write; use credentials / `.env` / `.mcp.json`
/ MCP / Graphify / WebSocket / user stream; or authorize any Phase 5 / successor
phase. Every retained verdict and project lock (H0 / R3 / R1a / R1b-narrow / R2 / F1
/ D1-A / 5m thread / V2 / G1 / C1; §11.6 = 8 bps per side / 16 bps round-trip; the
Phase 4ak M0 twelve-clause gate; Phase 4al no-rescue; the Phase 4aw
`flip_research_eligible(...)` always-raises invariant — never invoked; Phase 4bb-F
sidecar policy; the Phase 4bn-AA split artefact, 4bn-AB source-admissibility posture,
4bn-AC ML dataset contract, 4bn-AE pre-registration amendment claim-scope, and the
4bn-AH..AK results including the AK single-follow-up selection) is preserved verbatim.
Phase 4 canonical remains unauthorized. The recommended label contract / spec memo
begins only under a separate future operator prompt. Do not merge to main and do not
push unless explicitly instructed in a later prompt; do not generate a merge-closeout
or the recommended next prompt unless explicitly instructed later.
