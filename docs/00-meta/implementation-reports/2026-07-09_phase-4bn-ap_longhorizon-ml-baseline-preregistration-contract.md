# Phase 4bn-AP — Long-Horizon ML Baseline Preregistration / Evaluation Contract Memo

## 1. Branch

`phase-4bn-ap/longhorizon-ml-baseline-preregistration-contract`

## 2. Base SHA

`4633a5ff5ddc9f418694b99990ffde8b2eacd161`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AO merge
closeout. Verified in sync before branching.)

## 3. Phase type and strict scope

Docs-only **long-horizon ML baseline preregistration / evaluation-contract memo** — the
memo recommended by Phase 4bn-AO. It **pre-registers, at the design level only**, a
future, separately authorized long-horizon baseline evaluation: its architecture,
target horizons, feature scope, split/censoring/leakage treatment, frozen baseline
families + constants, metric registry, decision hierarchy, kill/continue criteria,
dependence policy, cost/materiality interpretation, future artefact requirements, and
claim-scope boundaries. It **executes nothing**: no row-level data read, no Parquet
read, no model trained/scored, no prediction, no evaluation, no ML artefact, no
namespace mutation, no successor execution phase authorized.

## 4. Files created / modified

Created (committed — docs only):

- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ap_longhorizon-ml-baseline-preregistration-contract.md`
  (this report).
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ap_closeout.md`.

No source, test, script, manifest, gate report, sidecar, split file, ML config, or
`data/` artefact created or modified. `current-project-state.md` **unchanged** (§39
note). No data file committed.

## 5. Exact documents / source inspected

Read-only (committed docs + committed source; README not treated as authority): the
Phase 4bn-AE preregistration; the Phase 4bn-AH / AI / AJ / AK / AL / AM / AN / AO
reports + closeouts + merge-closeouts; `docs/00-meta/process/`; and committed source
`pre_v002_ml_dataset_contract.py`, `labels_schema_v002.py`,
`longhorizon_labels_schema_v001.py`, `longhorizon_labels_compute_v001.py`,
`pre_v002_fixed_baseline_run.py`, `ml_baseline_design_v002.py`,
`ml_baseline_models_v002.py`, `ml_baseline_metrics_v002.py`, `features_schema_v002.py`,
`scripts/phase4bn_an_build_longhorizon_labels.py`.

## 6. Confirmation no local data artefacts were read (except git tracked-state checks)

Confirmed. No AN JSON artefact was re-read (no committed-report inconsistency required
it); all AN facts were recovered from the committed AN/AO reports. Only `git status` /
`git ls-files` / `git check-ignore` tracked-state checks touched `data/` paths.

## 7. Confirmation no Parquet files were read

Confirmed. No built long-horizon label Parquet, no source feature/normalized Parquet,
no raw zip was read.

## 8. Confirmation no output namespace mutation occurred

Confirmed. The Phase 4bn-AN output namespace was not created, overwritten, deleted,
refreshed, or re-hashed; it was not touched at all this phase.

## 9. Confirmation no ML / training / scoring / prediction / inference

Confirmed. None occurred. This memo designs a future contract; it runs no model.

## 10. Confirmation no v002 terminal / sealed test / test rows

Confirmed. No data window was read at all. The pre-registered contract itself forbids
v002-terminal / sealed-test / test-row reads (`test_rows_loaded = 0`).

## 11. Confirmation no AH/AJ/AN namespace mutation

Confirmed. The Phase 4bn-AH ML-dataset, 4bn-AJ baseline, and 4bn-AN long-horizon label
namespaces were not read, mutated, refreshed, created, or deleted.

## 12. AO recommendation summary (recovered)

Phase 4bn-AO recorded `RECOMMEND_LONGHORIZON_ML_BASELINE_PREREGISTRATION_MEMO_NEXT`: the
AN long-horizon label layer is integrity-clean and complete and descriptively far more
cost-relevant than 15s, so a fixed, pre-registered, no-strategy baseline evaluation is
warranted — but only via a docs-only preregistration memo (this Phase 4bn-AP) followed
by a **separately authorized** evaluation. Posture: 5m primary; 30m/1h secondary
diagnostic; majority/persistence/L2-logistic fixed baselines; existing chrono split +
1-day embargo; block-level dependence evidence (275 dates / 9 months; no per-row
significance); AE §13 metric registry vs both floors; pre-registered kill/continue
criteria; absolute no-strategy/PnL/backtest/live boundary; evaluation itself requires a
further separate authorization.

## 13. AN build and artefact-integrity summary (recovered)

Family `microstructure_labels_longhorizon_aggtrades_v001`; `label_config_hash`
`edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`; **275** dates /
**400,001,695** rows; local/gitignored label artefacts only. Leakage/scope: per-horizon
earlier-model-split boundary crossings **0**; `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`; `test_rows_loaded = 0`; all eight
non-authorization flags `false`; `frozen_v002_family_mutated = false`;
`data_committed = false`. Split totals (AN inventory): train 304,816,127 (214 dates) /
embargo 3,071,370 (2 dates) / validation 68,578,296 (45 dates) / holdout 23,535,902 (14
dates). Per-horizon envelope-terminal censoring (holdout tail only): 5m 1,528 / 30m
9,916 / 1h 23,650; invalid prices 0. No ML / no strategy / no successor.

## 14. Long-horizon materiality summary (recovered, descriptive only)

Validation share `|move| > 16 bps`: **5m 34.95% / 30m 64.28% / 1h 72.72%** vs the Phase
4bn-AJ 15s reference **2.47%**. Median absolute move: 15s ~2.5 bps → 5m ~10–11 → 30m
~24–25 → 1h ~33–34 bps. Near-binary direction with a shrinking flat class and a mild
horizon-growing up-skew. **Descriptive raw-move label-materiality only — not predictive
edge, not tradability.**

## 15. AJ 15s baseline reference summary (recovered)

Majority accuracy 0.4950; persistence 0.5158; L2 0.5453; L2 uplift over majority
**+5.03 pp**, over persistence **+2.96 pp**; validation date/month block agreement
**1.000**; holdout no sign reversal; high-confidence tail (≥0.8) 0.633, beats the floor
but overconfident; 15s validation > 16 bps share 2.47%. Target remains
information-diagnostic, non-economic.

## 16. AE preregistration framework summary (recovered)

- **Allowed claim scope (§8):** (a) short-horizon directional information; (b) v002
  small-lift sign reproduction; (c) calibration/confidence-tail assessment.
- **Forbidden claim scope (§8/§19):** tradability; profitability; strategy viability;
  execution viability; slippage/spread adequacy; live-readiness; paper/shadow readiness;
  PnL; backtest validity; production suitability; economic significance.
- **Locked cost:** 8 bps/side · 16 bps round-trip (descriptive only).
- **§13 metric registry** (mandatory metrics; aggregate + per-month + per-date
  granularities).
- **§16 frozen success thresholds:** `SUCCESS_ACCURACY_UPLIFT_PP = 2.0` over **both**
  the majority and persistence floors; `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP = 1.0` over
  the **majority** floor; `SUCCESS_MACRO_F1_UPLIFT = 0.03` over the **majority** floor;
  thresholds pre-registered and **not relaxed after a result is seen**.
- **§10 dependence policy (Option 1):** row-level metrics descriptive only; decision by
  UTC date/month block; no per-row significance; decimation reserved-not-adopted.
- **§19 absolute strategy/PnL/backtest/live boundary** behind a future **M0-style
  mechanism-admissibility memo** (aggTrades-only cannot support spread/slippage/mid).

## 17. Target horizon decision

**Primary decision target: `forward_direction_5m`.** Secondary diagnostic targets:
`forward_direction_30m` and `forward_direction_1h`.

Rationale: 5m best balances **materiality** (validation ~35% of moves clear 16 bps, vs
2.47% at 15s) against **plausible feature-target signal persistence** — it is the
closest long horizon to the microstructure-memory regime where the AJ 15s directional
lift was demonstrated. 30m and 1h have larger raw materiality (~64% / ~73% clear 16 bps)
but the weakest plausible predictability (short-memory features vs a 30–60-minute-ahead
direction) and the heaviest label overlap / lowest effective independence. All three may
be **prepared** in the future dataset (the AN labels already exist for all three), but
the **continuation decision is keyed to 5m only** (see §24); 30m/1h are reported as
secondary diagnostics and cannot, by themselves, upgrade a failed 5m result.

## 18. Evaluation architecture decision

**`LONGHORIZON_ML_DATASET_BUILD_THEN_FIXED_BASELINE_RUN`** (option A — the AH→AJ
two-step pattern).

- **Future phase 1 (separately authorized):** a data-reading **long-horizon ML dataset
  build / preparation** phase — bind the AH-verified 45-feature source to the AN
  long-horizon label source, assign the existing pre-v002 chrono split, fit a train-only
  transform, and emit a compact dataset spec + split index + leakage/split/integrity
  proof + source binding. **No model** runs in this phase.
- **Future phase 2 (separately authorized, after phase 1):** a **fixed run-once
  baseline** phase — majority / persistence / L2-logistic with frozen constants over the
  phase-1 dataset, emitting the §23 metrics + verdict. **No model/family search.**

Justification for A over B (direct baseline run): it preserves the proven AH→AJ safety
separation — the dataset layer is built, leakage-proved, and gated **before** any model
touches it, so a data/build error cannot be conflated with a model result. The existing
AH ML-dataset was built for the **15s** label; the long-horizon targets require a **new**
dataset join (45 features ↔ AN long-horizon labels), so a genuine build/verify step
exists and should be isolated. No committed evidence supports skipping the checkpoint;
B (direct run) is not adopted. C/D (no evaluation / blocker) do not apply — the labels
are integrity-clean and the evaluation is warranted.

## 19. Feature scope

- **Reuse the existing Phase 4bn-AH 45 causal aggTrades feature allowlist**
  (`FEATURE_NAMES_V002`) **unchanged**. No new features; **no feature selection**; no
  mid/book features; no raw/price/future-derived forbidden columns; no
  threshold-optimized features.
- **Long-horizon labels are targets, not features.** The AN label / support / reference /
  censoring columns (`forward_log_return_H`, `forward_direction_H`,
  `reference_row_index_H`, `reference_timestamp_ms_H`, `horizon_censored_flag_H`,
  `label_invalid_price_flag`, `label_any_censored_flag`) are **never** model inputs; the
  forbidden model-matrix substring scan (`forward_log_return`, `forward_direction`,
  `horizon_censored_flag`, `label_`, `split_`, `censored_`) and forbidden raw-price scan
  remain empty.
- The 45-feature past-window returns exist only at windows **1s/5s/15s/60s** (asserted
  `FEATURE_WINDOWS_MS_V002 == (1000,5000,15000,60000)`) — this fact drives the persistence
  definition (§22).

## 20. Split / censoring / leakage scope

- **Existing pre-v002 chrono split** (`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_
  BOUNDARY_EMBARGO`): train (214 dates) / embargo (2) / validation (45) / holdout (14);
  1-day boundary embargo preserved; **no random split; no shuffled CV**.
- **v002 terminal excluded**; **sealed test excluded**; **`test_rows_loaded = 0`**;
  `v002_terminal_window_read = false`; `sealed_test_split_touched = false`.
- **Per-horizon censoring:** exclude censored labels from that horizon's target
  evaluation; **do not impute** censored targets; per-horizon support counts reported.
- **Leakage:** retain strict per-row alignment proof over `row_index, agg_trade_id,
  feature_timestamp_ms, source_transact_time_ms, utc_date`; no target leakage from
  reference/support columns; no future-derived features; earlier-model-split
  boundary-crossing rows must be **0** (as AN already proved); train-only transform
  fitted on the train split only. Preserve the AH and AN proofs.

## 21. Baseline families and frozen constants

Exactly three fixed, run-once baselines (no fourth model; **no** tree / neural / capacity
comparison; **no** hyperparameter search; **no** calibration training; **no** threshold
tuning):

1. **Majority** — predict the train-majority class (per horizon).
2. **Persistence** — `sign(rolling_log_return_past_window_60s)` (see §22).
3. **L2 multinomial-logistic** — softmax over 3 classes, mini-batch SGD, with the
   **frozen Phase 4bn-B/AJ constants** (confirmed from `ml_baseline_design_v002.py`):
   - `SGD_EPOCHS = 1`
   - `SGD_BATCH_SIZE = 8192`
   - `SGD_LEARNING_RATE = 0.1`
   - `SGD_L2_REGULARIZATION_STRENGTH = 1e-4`
   - `SGD_GRADIENT_CLIP_NORM = 10.0`
   - `RNG_SEED = 20260528`
   - standardization `subtract_train_mean_divide_by_max_train_std_epsilon`,
     `STANDARDIZATION_EPSILON = 1e-8`, `STANDARDIZE_BOOLEAN_FLAGS = False`
     (train-only fit).

These constants are **frozen by this memo**; the future baseline run must use them
verbatim and may not tune them.

## 22. Persistence baseline definition

**Pre-registered: persistence = `sign(rolling_log_return_past_window_60s)`** for each
long-horizon target (predicted class = the sign of the 60s past-window log-return; the
existing per-row `persistence_signs` channel).

Rationale and the horizon-match rejection: the AJ convention is "sign of the past-window
return at the window matched to the forward horizon" — for 15s it used
`rolling_log_return_past_window_15s`. The 45-feature allowlist contains past-window
returns only at **1s/5s/15s/60s**; **no 5m/30m/1h past-window return feature exists**. A
horizon-matched persistence for 5m/30m/1h would therefore require **creating a new
feature**, which is explicitly **rejected** (no new feature creation). Per the AO/AP
posture, persistence keeps the AJ convention using an **existing** window; the **60s**
window is pre-registered as the persistence signal for all three long horizons because
it is the **longest available** past-window return (closest to the long horizons) and
provides a genuine "recent-trend-continues" floor. (The exact-AJ-feature alternative
`rolling_log_return_past_window_15s` is recorded as the sole alternative; the choice is
frozen here and may be revisited **only** by a later separate decision memo, **never**
after seeing results.)

## 23. Metric registry

The Phase 4bn-AE §13 mandatory registry, per horizon and at aggregate / per-month /
per-date granularities:

- accuracy; balanced accuracy; macro-F1; per-class precision/recall/F1; confusion
  matrix; predicted-class distribution; predicted-zero rate; zero-class prevalence;
- **majority floor** (accuracy / balanced-accuracy / macro-F1) and **persistence floor**
  comparisons;
- per-date and per-month **block agreement** (fraction of blocks where L2 beats the
  majority floor) and **holdout non-reversal**;
- log-loss; Brier score; calibration reliability table; high-confidence tail size +
  accuracy at the pre-registered ≥ 0.8 threshold; beats-majority booleans; a
  usable/ranking-only/unusable calibration verdict;
- filtered-row date counts; dropped-rows-by-reason; per-horizon support/censored counts;
- **descriptive cost-realism context only:** the AN 8 bps / 16 bps cost-clearing shares
  from the label distributions.

**Forbidden metrics:** no PnL; no trade count; no Sharpe; no hit-rate framed as trading;
no turnover; no position/holding metric; no strategy metric of any kind.

## 24. Decision hierarchy and primary target

- **Primary target: `forward_direction_5m`.** The continuation decision is keyed to 5m.
- **Primary comparison:** L2 must beat **both** the majority and persistence floors on
  5m **validation accuracy** by the frozen §16 margin, **and** macro-F1 by the frozen
  margin (majority-referenced), **and** balanced accuracy must not collapse.
- **Block evidence:** improvement in a **majority** of validation date-blocks **and**
  both validation months; **holdout must not reverse** the sign of the uplift.
- **Calibration/confidence-tail:** diagnostic only (usable / ranking-only / unusable);
  never a trading gate.
- **30m / 1h are secondary diagnostics only.** A positive 30m/1h result **cannot**
  override a failed 5m primary result, and cannot by itself trigger continuation, unless
  a **later separate decision memo** explicitly revisits the hierarchy. A negative 5m with
  positive 30m/1h routes to `INVESTIGATE_AMBIGUOUS` (§25), not to continuation.

## 25. Kill / continue criteria (frozen)

Adopt the Phase 4bn-AE §16 frozen thresholds **verbatim** (they are pre-registered and
horizon-independent as design thresholds), applied to the **5m primary** target, and
**not relaxed after any result is seen**. The future fixed baseline run must record
exactly one of:

- **`CONTINUE_ONE_BOUNDED_FOLLOWUP`** — only if **all** hold on 5m validation: L2 beats
  **both** the majority and persistence floors on accuracy by **≥ +2.0 pp**
  (`SUCCESS_ACCURACY_UPLIFT_PP`); L2 beats the majority floor on macro-F1 by **≥ +0.03**
  (`SUCCESS_MACRO_F1_UPLIFT`); balanced accuracy does not degrade materially (≥ +1.0 pp
  over the majority floor, `SUCCESS_BALANCED_ACCURACY_UPLIFT_PP`, or at minimum
  non-degraded); improvement in a **majority** of validation date-blocks **and** both
  months; holdout **does not reverse**; the ≥ 0.8 confidence tail beats the majority
  floor (diagnostic, not overclaimed).
- **`INVESTIGATE_AMBIGUOUS`** — mixed block evidence; validation-improves-but-holdout-
  does-not (without full reversal); classification-improves-but-calibration-fails;
  5m-fails-but-30m/1h-positive; or information-suggested-but-not-clean. Routes to a
  separate docs-only decision memo (default posture: remain paused); must **not** silently
  become a continue.
- **`STOP_LONGHORIZON_ML_ARC`** — 5m L2 fails to beat both floors by ≥ +2.0 pp
  accuracy; **or** fails +1.0 pp balanced-acc over majority **and** +0.03 macro-F1 (both
  fail); **or** improvement concentrated in a single month / minority of blocks; **or**
  holdout **reverses** the sign; **or** calibration unusable **and** the classification
  margins also fail; **or** the descriptive cost stats plus a failed information
  diagnostic jointly show no non-economic value.

These are frozen at the design level here; the future baseline-run implementation prompt
must adopt them **verbatim** (exact numeric thresholds already given) and may not
introduce new or relaxed thresholds.

## 26. Dependence / block-evidence policy

- Rows are **not** independent; long-horizon label overlap is **heavier** than 15s
  (consecutive 5m/30m/1h forward windows overlap almost entirely), so the effective
  independent-sample count is far below the row count.
- **Decision evidence at the UTC date/month block level** (275 dates / 9 months); **no
  per-row significance**; **no p-value over row counts**; rely on block-agreement and
  holdout non-reversal.
- **Block bootstrap: reserved-not-adopted** for the first fixed baseline evaluation
  (matching the AE §10 posture); it may be adopted only by a later separate framework
  phase if a dependence-aware uncertainty statement is later required.

## 27. Cost / materiality interpretation

- The locked **8 bps / 16 bps** cost remains **descriptive context only**; the AN
  long-horizon cost-clearing shares show label **materiality**, not edge. **No** cost
  thresholding of the target, **no** trade simulation, **no** PnL.
- **Even a positive predictive result at 5m/30m/1h would not authorize strategy.** A
  directional lift over floors is an information-diagnostic claim (§8 a/b/c), not
  tradability. aggTrades-only data cannot resolve spread/slippage/mid-price realism; any
  strategy/PnL/backtest/live path remains behind the Phase 4bn-AE §19 **M0-style
  mechanism-admissibility memo** and its per-capability separate authorizations.

## 28. Future artefact requirements

**Future phase 1 (long-horizon ML dataset build, no models)** should produce: a dataset
manifest; a per-date **split index**; the **train-only transform** stats (fitted on
train only); a **leakage/split/integrity proof** (strict alignment, 0 boundary
crossings, embargo rows used = 0); **feature ↔ label source binding** (AH feature
segment SHAs + AN `label_config_hash` `edaeafde…`); explicit `v002_terminal_window_read
= false` / `sealed_test_split_touched = false` / `test_rows_loaded = 0` proof fields;
per-Parquet `.sha256` sidecars + inventory (Phase 4bb-F policy); **no model output**.
Compact-spec posture; all non-authorization flags `false`.

**Future phase 2 (fixed baseline run)** should produce: a model-run manifest; the frozen
config (§21 constants); the §23 baseline metrics; per-date / per-month summaries;
calibration / confidence-tail summaries; holdout confirmation; the §25 verdict. **No**
strategy / PnL / backtest artefact.

All data/model outputs **local / gitignored** unless later explicitly authorized;
**no** data file committed.

## 29. Final AP decision

**`RECOMMEND_LONGHORIZON_ML_DATASET_BUILD_AUTHORIZATION_MEMO_NEXT`** (option A).

Reasoning: the AN labels are integrity-clean and the evaluation is warranted (Phase
4bn-AO), and the safest, evidence-consistent path is the proven **AH→AJ two-step**
structure — build and leakage-prove the long-horizon ML dataset **first** (no models),
then run fixed baselines under a **separate later** prompt. This isolates any
data/build error from any model result and keeps each step separately gated. Option B
(direct baseline run) is not adopted (no evidence supports skipping the dataset
checkpoint); options C/D do not apply (labels sound, evaluation warranted, no blocker).

## 30. Exact high-level future build scope (option A, phase 1)

Recommend **exactly one** future **long-horizon ML dataset-build authorization phase**
(data-reading, no models), scoped at a high level as:

- **Bind** the AH-verified 45-feature pre-v002 source to the AN long-horizon label
  family `microstructure_labels_longhorizon_aggtrades_v001` (`label_config_hash`
  `edaeafde…`) over the admitted pre-v002 segment (275 dates / 400,001,695 rows).
- **Produce** a compact leakage-proof dataset specification: per-date split index (train
  214 / embargo 2 / validation 45 / holdout 14), train-only transform stats, per-horizon
  support/censored accounting, strict-alignment + 0-boundary-crossing proof, feature↔label
  source binding, sidecars + inventory — **no re-materialised wide matrix** (preserve the
  AH compact-spec posture and the Phase 4bn-L 125 GiB cap with a budget preflight).
- **Exclude** v002 terminal + sealed test; keep `test_rows_loaded = 0`; all
  non-authorization flags `false`; local/gitignored namespace; no data committed.
- **Explicitly excluded from that build:** any model / scoring / prediction / inference;
  any feature selection / threshold optimization / model selection / hyperparameter
  search / calibration training; any strategy / signals / PnL / backtest; any data
  acquisition / endpoint / raw-zip read; any new-feature creation.

The **fixed baseline run (phase 2)** is a **further, separate** authorization **after**
phase 1 and is **not** authorized by phase 1.

## 31. If recommending direct fixed baseline run — N/A

Not applicable; the decision is option A (dataset-build-first), not option B.

## 32. If no evaluation / blocker — N/A

Not applicable; a safe evaluation contract is fully definable and the evaluation is
warranted. (Had a blocker existed, this memo would have recorded
`RECORD_PREREGISTRATION_BLOCKER_REMAIN_PAUSED` with the exact gap.)

## 33. No prompt generated / no evaluation authorized

This memo **does not generate** the recommended dataset-build phase's prompt and **does
not authorize** any row-level read, dataset build, model run, or successor execution
phase. The recommended dataset-build phase begins **only** under a separate future
operator prompt; row-level reads happen **only** under that later prompt; and **no model
run is authorized by that future dataset-build phase** — the fixed baseline run is a
further separate authorization beyond it.

## 34. Allowed claims preserved

Preserved verbatim (Phase 4bn-AE §8): (a) short-horizon directional information; (b)
v002 small-lift sign reproduction; (c) calibration/confidence-tail assessment. This memo
adds no new empirical claim; it pre-registers a future evaluation whose claims will be
capped at §8(a)/(b)/(c).

## 35. Forbidden claims preserved

Preserved verbatim (Phase 4bn-AE §8 / §19). Nothing here may be cited as evidence of
tradability, profitability, strategy viability, execution viability, slippage/spread
adequacy, live-readiness, paper/shadow readiness, PnL, backtest validity, production
suitability, or economic significance. The AN long-horizon cost-clearing shares are
descriptive materiality context only — **not** predictive edge and **not** tradability.
A future positive baseline result would remain information-diagnostic and non-economic.
The locked cost reference remains 8 bps/side · 16 bps round-trip; the §19 M0 gate is
unsoftened.

## 36. Validation commands and results

Docs-only phase (no source/test changed), so no pytest/ruff/mypy required.

- `git rev-parse main`/`origin/main`/`HEAD` (pre-branch) → all
  `4633a5ff5ddc9f418694b99990ffde8b2eacd161`. ✅
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`;
  `git diff --name-only` (tracked) → empty (no working-tree modifications). ✅
- `git checkout -b phase-4bn-ap/longhorizon-ml-baseline-preregistration-contract` at base
  SHA. ✅
- `git ls-files data/microstructure/` / `data/research/` → **0 tracked**. ✅
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/` →
  `.gitignore:88`. ✅
- Confirmed no Parquet read; no AN JSON re-read; no namespace mutation. ✅
- `git diff --check` → clean. ✅
- `git diff --name-status main..HEAD` (after commit) → only the two Phase 4bn-AP docs. ✅
- No data-output tracked-file check → no file under `data/` staged or committed. ✅

## 37. Git status

Before commit: the two new Phase 4bn-AP docs untracked, plus the transient
`?? .claude/scheduled_tasks.lock` (not committed). No `data/` file staged. The ~11.12 GiB
AN label layer under `data/research/…` remains gitignored, untracked, and unmutated.
Final committed SHA and post-commit `git status --short` are reproduced in the closeout
and the final operator report.

## 38. Result state

`LONGHORIZON_ML_BASELINE_PREREGISTRATION_RECORDED__DATASET_BUILD_AUTHORIZATION_MEMO_RECOMMENDED__NO_ML__NO_PARQUET_READ__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## 39. Recommended next state

**Remain paused.** The long-horizon baseline evaluation contract is pre-registered.
Recommended next step: exactly one **docs-only-authorized, data-reading** long-horizon
**ML dataset-build** phase (no models), **not started**, requiring a **separate future
operator prompt**; the fixed baseline run is a further separate authorization after
that. No ML, no row-level read, no strategy/PnL/backtest/live path is authorized (each
requires its own separate authorization; any trading path remains behind the §19 M0
gate). `current-project-state.md` is left unchanged, matching the immediate Phase
4bn-AH..AO precedent (the update convention at this arc point is not clear/consistent;
per the operator instruction it is not updated and is recorded here as unchanged).

## 40. Explicit no-successor execution statement

Phase 4bn-AP authorizes **no** successor execution phase. It does **not**, and does not
authorize anyone to: generate the recommended dataset-build phase's prompt; read any
built long-horizon label Parquet or source feature/normalized Parquet for row-level
analysis; build any ML/dataset/label namespace; train / score / predict / infer; perform
feature selection / threshold optimization / model selection / hyperparameter search /
calibration training / confidence-tail selection; rerun the AN build / AH builder / AI
diagnostics / AJ baselines; do strategy / signals / PnL / backtest / Sharpe / hit-rate /
position sizing / execution / paper / shadow / live-readiness / deployment /
exchange-write; acquire data or call any endpoint; use credentials / `.env` /
`.mcp.json` / MCP / Graphify / WebSocket / user stream; mutate the frozen v002 family or
the AN output namespace or any published manifest / gate / sidecar / split / ML config;
or authorize any Phase 5 / successor phase. Every retained verdict and project lock (H0 /
R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1; 8 bps/side · 16 bps
round-trip; the Phase 4ak M0 twelve-clause gate; Phase 4al no-rescue; the Phase 4aw
`flip_research_eligible(...)` always-raises invariant — never invoked; Phase 4bb-F
sidecar policy; the Phase 4bn-AA split artefact, 4bn-AC ML dataset contract, 4bn-AE
preregistration claim-scope, and the 4bn-AH..AO results including the AK single-follow-up
selection, the AL/AM recommendations, the AN build, and the AO diagnostics) is preserved
verbatim. Phase 4 canonical remains unauthorized. Do not merge to main and do not push
unless explicitly instructed in a later prompt; do not generate a merge-closeout or the
recommended next prompt unless explicitly instructed later.
