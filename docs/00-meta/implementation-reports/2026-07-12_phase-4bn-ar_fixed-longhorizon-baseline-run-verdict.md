# Phase 4bn-AR — Fixed Long-Horizon Baseline Run + Preregistered Verdict

## 1. Branch

`phase-4bn-ar/fixed-longhorizon-baseline-run-verdict`

## 2. Base SHA

`5a1d2c88a35ffb9e48f5db1c95ee66b27c1885fc`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AQ merge
closeout. Verified in sync before branching.)

## 3. Phase type and strict scope

A single, run-once, **no-search** long-horizon fixed baseline evaluation — phase 2
of the Phase 4bn-AP `LONGHORIZON_ML_DATASET_BUILD_THEN_FIXED_BASELINE_RUN`
architecture — executed over the verified Phase 4bn-AQ dataset specification. It
trains the three frozen baseline families once each per authorized horizon, scores
validation and holdout under the frozen split, computes the pre-registered
aggregate / date-block / month-block / calibration / confidence-tail diagnostics,
and records **exactly one** Phase 4bn-AP §25 verdict. It is an information-diagnostic
baseline run only; it establishes nothing about tradability / profitability / edge /
PnL / strategy / execution / live-readiness (Phase 4bn-AE §8/§19).

## 4. Files created / modified

Created — committed (source / tests / scripts / docs only):

- `src/prometheus/research/microstructure/longhorizon_fixed_baseline_run_v001.py`
  (the fixed-baseline runner: AQ artefact verification, train-only standardizer,
  streaming per-horizon read, three-horizon lockstep L2 fit, evaluation registry,
  orchestration, artefact assembly).
- `src/prometheus/research/microstructure/longhorizon_baseline_verdict_v001.py`
  (pure, deterministic Phase 4bn-AP §24/§25 verdict hierarchy + calibration
  classification).
- `scripts/phase4bn_ar_run_fixed_longhorizon_baselines.py` (thin CLI orchestrator;
  `--dry-run` preflight / full run).
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_contract.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_metrics.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_verdict.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_run.py`
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-ar_fixed-longhorizon-baseline-run-verdict.md`
  (this report).
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-ar_closeout.md`.

No frozen v002 / AH / AJ / AN / AQ module, manifest, gate report, sidecar, split
file, or ML config was modified. `current-project-state.md` **unchanged** (§52).
**No data / model artefact committed** — the model-run outputs are local /
gitignored only.

## 5. Exact documents / source inspected

Read-only (committed docs + committed source; README not treated as authority): the
Phase 4bn-AE preregistration contract amendment; the Phase 4bn-AH / AI / AJ / AK /
AL / AM / AN / AO / AP / AQ reports + closeouts + merge-closeouts; the Phase 4bb-F
sidecar policy and Phase 4bn-L derived-storage memo (as cited by AH/AQ);
`docs/00-meta/process/`. Committed source: `ml_baseline_design_v002.py`,
`ml_baseline_models_v002.py`, `ml_baseline_metrics_v002.py`,
`pre_v002_fixed_baseline_run.py` (AJ), `features_schema_v002.py`,
`longhorizon_ml_dataset_contract_v001.py`, `build_longhorizon_ml_dataset_v001.py`
(AQ), `pre_v002_ml_dataset_contract.py`, `pre_v002_split_policy.py`,
`scripts/phase4bn_aq_build_longhorizon_ml_dataset.py`, and the AJ / AQ test suites.

## 6. AQ artefacts inspected and sidecar results

All **seven** AQ artefacts and their **fourteen** Phase 4bb-F sidecars under
`data/research/microstructure/ml_datasets/longhorizon_pre_v001/` were verified
read-only (both pre-implementation via a standalone check and, again, at run time by
`load_and_verify_aq_artefacts`): `dataset_manifest.json`, `split_index.json`,
`train_only_transform.json`, `leakage_split_integrity_proof.json`,
`source_binding.json`, `sidecar_inventory.json`, `build_run_record.json`. Every
sidecar basename + SHA matched the on-disk file. Cross-artefact agreement confirmed:
`dataset_contract_hash` identical across manifest / source_binding / proof;
feature_count 45; feature_list == the frozen allowlist; feature_list_hash bound;
label family / config hash / AN manifest SHA bound; split raw rows and per-horizon
support counts bound; `alignment_mismatches = 0`; per-horizon
`boundary_crossing_rows = 0`; `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`; `test_rows_loaded = 0`; `data_committed =
false`; all eight non-authorization flags `false`; transform `fit_split = train`,
`train_primary_valid_rows = 304,816,127`, per_feature count 45. **After the run the
AQ namespace re-verified byte-identical** (read-only; not mutated).

## 7. Source data paths read

Only the AQ-bound admitted pre-v002 sources: BTCUSDT, 2024-03-01 … 2024-11-30, the
275 feature Parquet partitions (`microstructure_features_aggtrades_v001` / Phase
4bn-S) and the 275 Phase 4bn-AN long-horizon label Parquet partitions
(`microstructure_labels_longhorizon_aggtrades_v001`), resolved from the AQ
`source_binding` / manifest inventories, every per-parquet `.sha256` re-verified.
Feature columns read: the frozen 45-feature allowlist + the five alignment keys.
Label columns read: the five alignment keys, `label_invalid_price_flag`,
`forward_direction_{5m,30m,1h}`, `horizon_censored_flag_{5m,30m,1h}`. **No** forward
return, reference-price, raw-price, book/mid, reference-timestamp, or unrelated
column was read; **no** descriptive cost statistic was recomputed (AN/AO materiality
context used only). The v002 terminal window and the sealed test were never
resolved or read.

## 8. Exact output namespace

`data/research/microstructure/ml_baselines/longhorizon_pre_v001_fixed_run/` — one
new local / gitignored namespace (`.gitignore:88`), previously nonexistent; a
one-run / no-overwrite guard refuses to overwrite a completed run.

## 9. Preflight results

Budget preflight (Phase 4bn-L): `D:` free **1,154.24 GiB ≥ 500 GiB** floor →
passed (breaches = none); live fail-closed floor 350 GiB re-checked every 25
partitions. A prior no-write `--dry-run` (full source-binding + 550-sidecar
verification, no rows read, no write) verified 7 AQ artefacts + 275 partitions,
confirmed the dataset-contract-hash and AN label-manifest SHA, and reported the
output namespace absent. Output namespace confirmed empty / gitignored before any
write.

## 10. Dataset identity and contract hash

- family `microstructure_ml_dataset_longhorizon_pre_v001`;
- contract `microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001`;
- `dataset_contract_hash =
  a310eabf7854ae13ffed1baa2d57a8cf557a3d90dec24337a61e4ca26a9c3873`
  (recomputed at run time and matched).

## 11. Feature-source identity and hashes

- feature count **45**; feature-list hash
  `8e705ba8800421ae0ccc55cdbf115a36dce9f27f8682e552e2b59c4ab83df7b9`;
- feature manifest SHA
  `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`;
- feature config hash
  `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`;
- feature gate SHA
  `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`.

## 12. Label-source identity and hashes

- family `microstructure_labels_longhorizon_aggtrades_v001`;
- `label_config_hash
  edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`;
- AN manifest SHA
  `b1ee9afd8dadc410216516f6fa291aa49a26ba788480eb7d98126fc45919f4c0`.

## 13. Split / transform binding

Split `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`: train 214 /
embargo 2 / validation 45 / holdout 14 dates; 1-day boundary embargo; no random /
shuffled split; embargo excluded from all fitting and scoring. Transform
`subtract_train_mean_divide_by_max_train_std_epsilon`, ε = 1e-8,
`STANDARDIZE_BOOLEAN_FLAGS = false`, `imputation_rule = fixed_zero_for_null_numeric`
(fill 0.0), fit on the train split only (over the 304,816,127 primary-5m-valid train
rows). The AQ-fitted statistics were **applied, never recomputed**; the future
model-matrix non-finite convention (impute non-finite numeric → fixed 0.0 before
standardization; boolean flags pass through) matches the committed Phase 4bn-AJ
`TrainOnlyStandardizer` verbatim.

## 14. Confirmation no AQ input artefact mutation

Confirmed. The seven AQ artefacts + fourteen sidecars re-verify byte-identical after
the run; nothing under the AQ namespace was written, refreshed, or re-hashed.

## 15. Confirmation no AH / AJ / AN namespace mutation

Confirmed. The Phase 4bn-AH ML-dataset, 4bn-AJ 15s-baseline, and 4bn-AN
long-horizon-label namespaces were read-only inputs / not touched; none mutated.

## 16. Confirmation no AH / AI / AJ / AN / AQ rerun

Confirmed. No builder or diagnostic was rerun: not the AQ dataset builder, not the
AN label builder, not the AH dataset builder, not the AI diagnostics, not the AJ 15s
baseline. AR reused their committed read-only verification / model / metric helpers
by import only.

## 17. Confirmation no v002 terminal / sealed test / test rows

Confirmed. `test_rows_loaded = 0`; `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`. No v002-terminal or sealed-test path was
resolved or read.

## 18. Baseline families

Exactly three, run once each per horizon: (1) **majority** (modal train class per
horizon); (2) **persistence** = `sign(rolling_log_return_past_window_60s)` (the same
signal for all three long horizons); (3) **L2 multinomial-logistic** (one independent
3-class softmax model per horizon). No fourth model; no tree / neural / ensemble; no
model-family comparison beyond the three.

## 19. Frozen L2 constants

epochs 1; batch size 8192; learning rate 0.1; L2 1e-4; gradient clip 10.0; seed
20260528; standardization = AQ train-only transform (ε 1e-8; boolean flags not
standardized); no early stopping; no schedule; no class/sample/cost weighting; no
CV; no calibration training; no retrain after validation/holdout. Each horizon's
trainer owns its RNG, so the single-read three-trainer dispatch is exactly
equivalent to three independent chronological passes.

## 20. Persistence definition

`sign(rolling_log_return_past_window_60s)` — the longest available past-window
log-return feature (one of the frozen 45). Class mapping {−1, 0, +1}; existing
non-finite handling preserved (non-finite → 0.0 → sign 0). **No** horizon-matched
5m/30m/1h past-window feature was created.

## 21. Training-row counts per horizon

train (fit): **5m 304,816,127 / 30m 304,816,127 / 1h 304,816,127** (identical; train
censoring 0 across horizons). Re-derived counts and per-horizon class counts
cross-checked equal to the AQ manifest (fail-closed on drift); L2 batches processed
**37,315 per horizon**.

## 22. Validation / holdout support counts

validation: **68,578,296** each horizon. holdout: **5m 23,534,374 / 30m 23,525,986 /
1h 23,512,252** (per-horizon envelope-terminal censoring excluded without
imputation). Total eval rows scored: 5m 92,112,670 / 30m 92,104,282 / 1h 92,090,548.

## 23. Batches processed

37,315 mini-batches per horizon model (1 epoch, batch 8192, over 214 train
partitions). Total gradient steps across the three L2 models = 111,945.

## 24. Runtime

Single controlled full run **2,075.6 s (~34.6 min)** (550-file source-hash
verification + fit pass over 214 train partitions × 3 models + eval pass over 59
validation/holdout partitions × 3 baselines × 3 horizons + 12 artefact writes). The
prior no-write `--dry-run` verification took ~416 s. Both fail-closed before any
write on any breach.

## 25. Storage footprint

Output namespace total **217,859 bytes (~213 KiB)** across **24 files** (12 compact
JSON artefacts + 12 canonical `.sha256` sidecars) — far under the Phase 4bn-L 125
GiB derived-footprint cap. `D:` free materially unchanged. No row-level prediction
file, no transformed matrix, no model binary.

## 26. Numerical guard summary

All three L2 weight matrices fully finite (`numerical_guard_all_finite = true`); no
non-finite logits / probabilities; softmax numerically stabilised (row-max
subtraction); gradient-norm clip 10.0 applied deterministically. No fail-closed
numerical condition arose.

## 27. Majority-class result per horizon

Modal train class = **+1 ("up")** for all three horizons (5m / 30m / 1h),
determined from that horizon's valid train targets only and frozen for
validation / holdout.

## 28. Validation aggregate metrics (all three baselines, per horizon)

Accuracy / balanced-accuracy / macro-F1:

| Horizon | Baseline | Accuracy | Balanced acc | Macro-F1 |
|---|---|---|---|---|
| 5m  | majority    | 0.51225 | 0.33333 | 0.22582 |
| 5m  | persistence | 0.48876 | 0.33069 | 0.32796 |
| 5m  | **L2**      | 0.51004 | 0.34113 | 0.33958 |
| 30m | majority    | 0.52901 | 0.33333 | 0.23065 |
| 30m | persistence | 0.48907 | 0.33023 | 0.32679 |
| 30m | **L2**      | 0.51553 | 0.34452 | 0.34369 |
| 1h  | majority    | 0.53516 | 0.33333 | 0.23240 |
| 1h  | persistence | 0.48703 | 0.32790 | 0.32499 |
| 1h  | **L2**      | 0.50648 | 0.33877 | 0.33762 |

(Full per-class precision/recall/F1, confusion matrices, predicted-class
distributions, predicted-zero rate, and zero-class prevalence are in
`aggregate_metrics.json`. Predicted-zero rate is ~0 for majority/L2 and ~0.003 for
persistence; the flat-class prevalence is ~0.02–0.06 % — the label is near-binary.)

## 29. Holdout aggregate metrics (all three baselines, per horizon)

| Horizon | Baseline | Accuracy | Balanced acc | Macro-F1 |
|---|---|---|---|---|
| 5m  | majority    | 0.50416 | 0.33333 | 0.22345 |
| 5m  | persistence | 0.48686 | 0.32791 | 0.32627 |
| 5m  | **L2**      | 0.50783 | 0.33904 | 0.33771 |
| 30m | majority    | 0.52133 | 0.33333 | 0.22845 |
| 30m | persistence | 0.48427 | 0.32544 | 0.32352 |
| 30m | **L2**      | 0.50117 | 0.33388 | 0.33381 |
| 1h  | majority    | 0.53761 | 0.33333 | 0.23309 |
| 1h  | persistence | 0.48818 | 0.32979 | 0.32600 |
| 1h  | **L2**      | 0.50998 | 0.34084 | 0.33984 |

## 30. L2 uplift vs majority and persistence; balanced-accuracy and macro-F1 uplift

Percentage-point uplifts (accuracy / balanced-accuracy) and macro-F1 uplift, L2 over
each floor:

| Horizon / split | acc vs majority | acc vs persistence | balacc vs majority | macro-F1 vs majority |
|---|---|---|---|---|
| 5m / validation  | **−0.222 pp** | **+2.128 pp** | +0.779 pp | +0.1138 |
| 5m / holdout     | +0.368 pp | +2.097 pp | +0.571 pp | +0.1143 |
| 30m / validation | −1.348 pp | +2.646 pp | +1.118 pp | +0.1130 |
| 30m / holdout    | −2.016 pp | +1.690 pp | +0.055 pp | +0.1054 |
| 1h / validation  | −2.868 pp | +1.945 pp | +0.543 pp | +0.1052 |
| 1h / holdout     | −2.763 pp | +2.180 pp | +0.751 pp | +0.1068 |

Interpretation: L2 **beats the persistence floor** on accuracy by ~+2 pp at 5m (and
on macro-F1 by ~+0.11 across all horizons — persistence and L2 predict all three
classes, while the majority floor predicts only "up" and so has a structurally low
macro-F1 of ~0.226). L2 **does not beat the strong majority floor** on accuracy at
5m (−0.22 pp validation) and loses to it by more at 30m/1h — the near-binary,
up-skewed label makes constant-"up" a hard accuracy floor. Balanced-accuracy uplift
is small (+0.78 pp at 5m validation, below the +1.0 pp bar).

## 31. Per-date block evidence

Fraction of the 45 validation UTC-date blocks where L2 beats **both** floors: **5m
23/45 = 0.511** (a bare majority); 30m 14/45 = 0.311; 1h 14/45 = 0.311. (Per-date
metrics for all families/splits are in `per_date_metrics.json`.)

## 32. Per-month block evidence

Validation spans two UTC-month blocks. L2 beats **both** floors in: **5m 1 of 2
months** (not unanimous); 30m 0 of 2; 1h 0 of 2. (Per-month metrics + the
beats-both-floors summary are in `per_month_metrics.json`.)

## 33. Holdout no-reversal assessment (5m primary)

Validation 5m L2 uplift: vs majority −0.222 pp, vs persistence +2.128 pp. Holdout 5m
L2 uplift: vs majority +0.368 pp, vs persistence +2.097 pp. A full reversal requires
a positive validation uplift to become negative on holdout against a required floor.
Against persistence, the positive validation uplift **remains positive** on holdout
(no reversal). Against majority, the validation uplift was already negative (never a
positive to reverse) and is slightly positive on holdout. **No full sign reversal**
(`holdout_full_reversal = false`).

## 34. Calibration results

L2 reliability (validation), Phase 4bn-B decile binning, ECE = Σ (n_b/N)·|emp−mean|:

| Horizon | ECE | calibration verdict |
|---|---|---|
| 5m  | 0.0583 | **unusable** (≥0.8 tail does not beat the majority floor) |
| 30m | 0.1080 | **ranking_only** (tail beats floor but overconfident) |
| 1h  | 0.1181 | **ranking_only** (tail beats floor but overconfident) |

## 35. ≥0.8 confidence-tail results

| Horizon | tail n | tail fraction | tail acc | majority floor | beats floor |
|---|---|---|---|---|---|
| 5m  | 1,562,179 | 0.02278 | 0.49656 | 0.51225 | **False** |
| 30m | 5,587,433 | 0.08148 | 0.58998 | 0.52901 | True |
| 1h  | 5,077,526 | 0.07404 | 0.53602 | 0.53516 | True |

The 5m high-confidence tail exists but its accuracy (49.7 %) does **not** beat the
majority floor (51.2 %); the 30m/1h tails beat their floors but are overconfident
(diagnostic only — never a trading signal).

## 36. 5m primary verdict evaluation

Against the frozen clean-continuation requirements (all must hold):

1. acc uplift vs majority ≥ +2.0 pp → **−0.222 pp — FAIL**;
2. acc uplift vs persistence ≥ +2.0 pp → +2.128 pp — pass;
3. macro-F1 uplift vs majority ≥ +0.03 → +0.1138 — pass;
4. balanced-accuracy uplift vs majority ≥ +1.0 pp → +0.779 pp — **FAIL**;
5. beats both floors in > ½ validation date blocks → 0.511 — pass (bare);
6. beats both floors in every validation month → 1 of 2 — **FAIL**;
7. holdout does not reverse the sign → no full reversal — pass;
8. ≥0.8 tail beats the majority floor → tail acc 0.497 < 0.512 — **FAIL**.

CONTINUE requires **all** → CONTINUE does not apply. There is **no hard-negative
holdout reversal** (STOP-forcing condition absent).

## 37. 30m / 1h secondary diagnostic interpretation

30m and 1h show the same qualitative pattern: L2 beats persistence but not the
(stronger) majority floor on accuracy, positive macro-F1 uplift, and overconfident
but floor-beating high-confidence tails. Neither is a **positive frozen diagnostic**
under the AP definition (beats **both** floors by +2.0 pp accuracy **and** +0.03
macro-F1 with no holdout reversal): both fail the accuracy-vs-majority bar
(`secondary_positive_flags = {30m: false, 1h: false}`). They therefore neither
upgrade nor rescue the 5m result; they corroborate the "information present but not
clean" reading.

## 38. Exact final verdict

**`INVESTIGATE_AMBIGUOUS`.**

## 39. Exact mapping from observed evidence to the frozen verdict criteria

Precedence applied: (1) CONTINUE evaluated first — fails (criteria 1, 4, 6, 8 above
fail). (2) Hard-negative holdout reversal — absent (`holdout_full_reversal =
false`), so STOP is not forced. (3) Explicit Phase 4bn-AP ambiguous conditions
evaluated — **two matched**:

- `mixed_date_and_month_block_evidence` — the 5m validation date-block majority is
  met (0.511 > 0.5) while the month-block unanimity is not (1 of 2), i.e. the date
  and month block signals disagree;
- `information_suggested_but_not_clean` — at least one frozen sub-threshold is met on
  5m (beats persistence by ≥ +2.0 pp accuracy; macro-F1 uplift ≥ +0.03; date-block
  majority), so genuine directional information over the persistence floor is
  present, but not cleanly enough for continuation.

No secondary-positive condition applied (both secondaries fail the majority-floor
accuracy bar). Since CONTINUE does not hold, there is no full reversal, and ≥1
ambiguous condition applies, the deterministic verdict is `INVESTIGATE_AMBIGUOUS`.
This authorizes **no** further run — at most a future docs-only decision memo under
separate authorization.

## 40. Confirmation thresholds were not changed

Confirmed. The frozen Phase 4bn-AE §16 thresholds (accuracy ≥ +2.0 pp over both
floors; balanced-accuracy ≥ +1.0 pp over majority; macro-F1 ≥ +0.03 over majority;
> ½ date blocks; every month block; no holdout reversal; ≥0.8 tail beats majority)
were adopted verbatim and applied to the 5m primary **before** the run and **not**
relaxed or reinterpreted after the result was seen. The narrow-miss interpretation
band (`NARROW_MISS_FLOOR_PP = 1.0`, which only routes STOP↔INVESTIGATE and can never
fabricate CONTINUE) was fixed in code before the run and was **not** triggered here.

## 41. Output artefact inventory

Under the AR namespace (each with a paired canonical Phase 4bb-F `.sha256` sidecar):
`run_manifest.json`, `frozen_config.json`, `source_binding.json`,
`model_parameters.json`, `aggregate_metrics.json`, `per_date_metrics.json`,
`per_month_metrics.json`, `calibration_summary.json`,
`confidence_tail_summary.json`, `verdict.json`, `run_record.json`,
`sidecar_inventory.json` (12 artefacts + 12 sidecars = 24 files).

## 42. Sidecar verification

All 12 artefact SHA-256 digests re-verified equal to their on-disk file and to the
`sidecar_inventory.json` record; the inventory's own sidecar re-verified. All pass.

## 43. Confirmation no row-level predictions written

Confirmed. No row-level prediction file, no transformed feature matrix, no per-row
probability dump; `persisted_row_level_predictions = false`. The
`model_parameters.json` records only the compact per-horizon weight matrix,
intercept, class ordering, parameter hash, batch/row counts, and numerical-guard
status.

## 44. Confirmation no data / model artefacts committed

Confirmed. The AR output namespace is gitignored (`.gitignore:88`) and untracked;
`git ls-files data/` reports zero tracked files under both data roots;
`data_committed = false`.

## 45. Confirmation all published authorization flags remain false

Confirmed (recorded on `run_record.json`): `ml_authorized`,
`diagnostics_authorized`, `strategy_authorized`, `signals_authorized`,
`pnl_authorized`, `backtest_authorized`, `live_authorized`,
`exchange_write_authorized` all `false`; every AQ non-authorization flag preserved
`false`; `authorized_successor_phase = false`.

## 46. Confirmation flip_research_eligible(...) not invoked

Confirmed. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is
preserved; it was **never** invoked (`flip_research_eligible_invoked = false`).
`research_eligible` unchanged.

## 47. Allowed claims

Capped at Phase 4bn-AE §8 (a)/(b)/(c): (a) a short-/long-horizon **directional
information** diagnostic; (b) v002 small-lift sign reproduction; (c)
calibration / confidence-tail assessment. The single allowed empirical claim from
this run: *the frozen causal aggTrades 45-feature set contains measurable directional
information for the long-horizon direction labels over the **persistence** floor
(+~2 pp accuracy at 5m and +~0.11 macro-F1 across horizons, holding on holdout), but
does not cleanly beat the strong majority ("up") floor and its high-confidence tail
is not usable at 5m — information is present but not clean enough for continuation.*

## 48. Forbidden claims

No claim of tradability, profitability, economic edge, PnL, strategy viability,
execution viability, backtest validity, spread/slippage adequacy, live-readiness,
paper/shadow readiness, or production suitability. The long-horizon raw-move
materiality shares (validation |move| > 16 bps: 5m 34.95 % / 30m 64.28 % / 1h
72.72 %; 15s ref 2.47 %) and the 8 bps/side · 16 bps round-trip cost remain
**descriptive context only** and did not enter any target, model, loss, threshold,
weighting, or verdict. aggTrades-only data cannot express spread / slippage /
executable mid / depth / impact; any strategy/PnL/backtest/live path remains behind
the absolute Phase 4bn-AE §19 M0-style mechanism-admissibility gate.

## 49. Validation commands / results

- targeted Phase 4bn-AR tests (contract / metrics / verdict / run) → **49 passed**;
- AJ baseline + AQ dataset (contract / build / proof) tests → **all passed** (with
  the AR suites, 123 passed in the combined run);
- import-boundary tests → **passed**;
- `ruff check` on the AR source / tests / script → **All checks passed**;
- `mypy --follow-imports=silent` on the two new AR modules → **Success: no issues**
  (the strict whole-package run's remaining errors are pre-existing `ndarray`
  type-parameter findings in the frozen `ml_baseline_models_v002` /
  `ml_baseline_metrics_v002` modules, unchanged by this phase);
- `git diff --check` → clean;
- AQ artefact sidecar verification (pre- and post-run) → all match; AQ namespace
  byte-identical after the run;
- AR output sidecar verification → all 12 artefacts + sidecars match;
- `git ls-files data/microstructure/` / `data/research/` → 0 tracked;
- `git check-ignore` → AR output `.gitignore:88`, data roots `.gitignore:85/88`.

## 50. Git status

Working tree: the four new Phase 4bn-AR source/test modules, the runner + verdict
source, the CLI script, and the two Phase 4bn-AR docs untracked (to be committed),
plus the transient `?? .claude/scheduled_tasks.lock` (**not** committed). No `data/`
file staged. The ~11 GiB AN label layer and the AQ dataset spec under
`data/research/…` and the AR output namespace remain gitignored, untracked, and
(for AQ) unmutated.

## 51. Phase result state

`LONGHORIZON_FIXED_BASELINE_RUN_COMPLETE__INVESTIGATE_AMBIGUOUS_RECORDED__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## 52. Recommended state

**Remain paused.** The single fixed long-horizon baseline run is complete and its
verdict is frozen: `INVESTIGATE_AMBIGUOUS`. This authorizes no further model run; at
most it recommends a future **docs-only** decision memo (under a separate
authorization) to weigh whether the persistence-floor-only directional information —
absent a clean majority-floor lift, clean block agreement, or usable 5m calibration —
warrants any bounded follow-up. `current-project-state.md` is left **unchanged**,
matching the entire Phase 4bn-AH..AQ precedent (the update convention at this arc
point is not clear/consistent; per the operator instruction it is not updated and is
recorded here as unchanged). No ML, strategy, signals, PnL, backtest, paper/shadow,
live, or exchange-write path is authorized; each requires its own separate
authorization, and any trading path remains behind the §19 M0 gate.

## 53. Explicit no-successor execution statement

Phase 4bn-AR authorizes **no** successor execution phase. It does **not**, and does
not authorize anyone to: run a second full baseline or a rerun with any changed seed
/ epochs / constants / persistence definition / feature set; add any fourth model /
tree / neural / ensemble; search models / features / hyperparameters / thresholds /
seeds / epochs; perform cross-validation / calibration training / probability
recalibration / confidence-threshold selection / selective-prediction optimization;
write row-level predictions; rerun the AQ / AN / AH builders, AI diagnostics, or AJ
baseline; do strategy / signals / PnL / backtest / Sharpe / hit-rate / turnover /
position sizing / holding-period / execution / paper / shadow / live-readiness /
deployment / exchange-write; acquire data or call any endpoint / read raw archives;
use credentials / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user stream;
mutate any AH / AJ / AN / AQ namespace, the frozen v002 family, or any published
manifest / gate / sidecar / split / ML config; commit any data / model artefact or
`.claude/scheduled_tasks.lock`; or authorize any Phase 5 / successor phase. Every
retained project lock and verdict is preserved verbatim, including the Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked), the Phase
4bb-F canonical sidecar policy, the Phase 4bn-AE claim scope and §19 M0 boundary
(8 bps/side · 16 bps round-trip), the Phase 4bn-AP frozen model + verdict contract,
and the Phase 4bn-AQ dataset identity / source bindings / transform / split / proof.
Do not merge to main and do not push unless explicitly instructed in a later prompt;
do not generate a merge-closeout or a successor prompt unless explicitly instructed
later.
