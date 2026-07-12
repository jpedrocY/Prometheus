# Phase 4bn-AR — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AR — Fixed Long-Horizon Baseline Run + Preregistered Verdict.
Branch: `phase-4bn-ar/fixed-longhorizon-baseline-run-verdict`.

## 2. Phase type

Fixed, run-once, **no-search** long-horizon baseline evaluation; this document is a
**merge-only review** (no model rerun, no source Parquet read).

## 3. Base SHA

`5a1d2c88a35ffb9e48f5db1c95ee66b27c1885fc`

## 4. Pre-merge AR branch HEAD

`1260c2083f7a7f794ef7b7f36c16b0bfcd9d4670`
(AR source/tests/scripts commit `4f8fbb6`; AR docs commit `1260c20`.)

## 5. Main / origin main before merge

`main == origin/main == 5a1d2c88a35ffb9e48f5db1c95ee66b27c1885fc`.

## 6. AR implementation summary

Phase 4bn-AR executed the phase-2 fixed baseline slot of the Phase 4bn-AP
`LONGHORIZON_ML_DATASET_BUILD_THEN_FIXED_BASELINE_RUN` architecture over the verified
Phase 4bn-AQ dataset specification. It verified the seven AQ artefacts + fourteen
sidecars, applied the AQ train-only transform (never refit), streamed the 275
admitted pre-v002 partitions (embargo excluded), fit three independent frozen L2
softmax models (5m / 30m / 1h) alongside the majority and 60s-persistence baselines,
scored validation and holdout, computed the frozen aggregate / date-block /
month-block / calibration / ≥0.8-confidence-tail diagnostics, and recorded exactly
one Phase 4bn-AP §25 verdict: **`INVESTIGATE_AMBIGUOUS`**. It is an
information-diagnostic run only.

## 7. Files added by AR

- `src/prometheus/research/microstructure/longhorizon_fixed_baseline_run_v001.py`
- `src/prometheus/research/microstructure/longhorizon_baseline_verdict_v001.py`
- `scripts/phase4bn_ar_run_fixed_longhorizon_baselines.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_contract.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_metrics.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_verdict.py`
- `tests/research/microstructure/test_phase4bn_ar_longhorizon_fixed_baseline_run.py`
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-ar_fixed-longhorizon-baseline-run-verdict.md`
- `docs/00-meta/implementation-reports/2026-07-12_phase-4bn-ar_closeout.md`

(This merge-closeout is added as a tenth file on the branch before merge.)

## 8. Confirmation diff is additions-only

`git diff --name-status main..HEAD` shows **only `A` (added)** entries — the nine AR
files above (plus this merge-closeout). No `M` / `D` / `R` entries.

## 9. Confirmation no frozen files changed

No modification to any frozen v002 / AH / AI / AJ / AN / AQ source module, published
manifest, gate report, `.sha256` sidecar, split file, frozen ML config, or existing
report. AR added strictly new sibling modules and docs.

## 10. AQ dataset identity and contract hash

- family `microstructure_ml_dataset_longhorizon_pre_v001`;
- contract `microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001`;
- `dataset_contract_hash =
  a310eabf7854ae13ffed1baa2d57a8cf557a3d90dec24337a61e4ca26a9c3873`.

## 11. Feature and label source bindings

- feature count 45; feature-list hash
  `8e705ba8800421ae0ccc55cdbf115a36dce9f27f8682e552e2b59c4ab83df7b9`; feature manifest
  `4881eb87…4b52`; feature config `0726b41d…d114c`; feature gate `db731d1b…6d8ab08`;
- label family `microstructure_labels_longhorizon_aggtrades_v001`; `label_config_hash
  edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`; AN manifest
  `b1ee9afd…f4a0`.

## 12. AR output namespace

`data/research/microstructure/ml_baselines/longhorizon_pre_v001_fixed_run/` — local,
gitignored (`.gitignore:88`), created by exactly one controlled run, one-run /
no-overwrite guarded, ~217,859 bytes (24 files); not committed; not mutated during
merge review.

## 13. AR artefact inventory

12 compact JSON artefacts + 12 canonical `.sha256` sidecars: `run_manifest.json`,
`frozen_config.json`, `source_binding.json`, `model_parameters.json`,
`aggregate_metrics.json`, `per_date_metrics.json`, `per_month_metrics.json`,
`calibration_summary.json`, `confidence_tail_summary.json`, `verdict.json`,
`run_record.json`, `sidecar_inventory.json`.

## 14. AR sidecar validation

All **12/12** AR artefact SHA-256 digests re-verified equal to their on-disk
`.sha256` sidecar during merge review. No forbidden artefact (no Parquet, model
binary, row-level prediction, or transformed matrix). `verdict.json` records
`INVESTIGATE_AMBIGUOUS`; `run_manifest.json` `dataset_contract_hash` matches the AQ
hash.

## 15. Confirmation AQ namespace remained byte-identical

The seven AQ artefacts + fourteen sidecars re-verified byte-identical during merge
review (all AQ preflight checks pass). AR read AQ read-only and mutated nothing.

## 16. Frozen target hierarchy

Primary decision target `forward_direction_5m`; secondary diagnostics
`forward_direction_30m` / `forward_direction_1h` (reported only; cannot upgrade a
failed 5m to continuation).

## 17. Frozen baseline families

majority; persistence; L2 multinomial-logistic — exactly three, run once each per
horizon. No fourth model; no tree / neural / ensemble.

## 18. Frozen L2 constants

epochs 1; batch size 8192; learning rate 0.1; L2 1e-4; gradient clip 10.0; seed
20260528; class order (−1, 0, +1); standardization = AQ train-only transform
(ε 1e-8; boolean flags not standardized).

## 19. Persistence definition

`sign(rolling_log_return_past_window_60s)` — the longest available past-window
log-return feature; the same signal for all three long horizons (no new feature).

## 20. Training and evaluation row counts

Train (fit): 304,816,127 rows per horizon (37,315 batches each; 111,945 total
gradient steps across the three models). Validation: 68,578,296 per horizon. Holdout:
5m 23,534,374 / 30m 23,525,986 / 1h 23,512,252. Total eval rows: 5m 92,112,670 / 30m
92,104,282 / 1h 92,090,548.

## 21. Runtime and output footprint

Runtime 2,075.6 s (~34.6 min); output ~213 KiB (24 files).

## 22. Numerical guard result

All three L2 weight matrices fully finite (`numerical_guard_all_finite = true`); no
fail-closed numerical condition.

## 23. Validation metrics table

Accuracy / balanced-accuracy / macro-F1:

| Horizon | majority | persistence | L2 |
|---|---|---|---|
| 5m  | 0.51225 / 0.33333 / 0.22582 | 0.48876 / 0.33069 / 0.32796 | 0.51004 / 0.34113 / 0.33958 |
| 30m | 0.52901 / 0.33333 / 0.23065 | 0.48907 / 0.33023 / 0.32679 | 0.51553 / 0.34452 / 0.34369 |
| 1h  | 0.53516 / 0.33333 / 0.23240 | 0.48703 / 0.32790 / 0.32499 | 0.50648 / 0.33877 / 0.33762 |

## 24. Holdout metrics table (accuracy)

| Horizon | majority | persistence | L2 |
|---|---|---|---|
| 5m  | 0.50416 | 0.48686 | 0.50783 |
| 30m | 0.52133 | 0.48427 | 0.50117 |
| 1h  | 0.53761 | 0.48818 | 0.50998 |

## 25. 5m uplift versus majority and persistence

Validation: L2 accuracy **−0.222 pp** vs majority; **+2.128 pp** vs persistence.
Holdout: **+0.368 pp** vs majority; **+2.097 pp** vs persistence.

## 26. Balanced-accuracy and macro-F1 uplift (5m validation)

Balanced-accuracy uplift vs majority **+0.779 pp**; macro-F1 uplift vs majority
**+0.1138**.

## 27. Validation date-block evidence

L2 beats **both** floors in **23 of 45** validation UTC-date blocks (0.511 — bare
majority) at 5m; 14/45 at 30m; 14/45 at 1h.

## 28. Validation month-block evidence

L2 beats **both** floors in **1 of 2** validation UTC-month blocks at 5m (not
unanimous); 0/2 at 30m; 0/2 at 1h.

## 29. Holdout no-reversal assessment

5m validation persistence-floor uplift (+2.128 pp) remains positive on holdout
(+2.097 pp); the majority-floor uplift was negative on validation (never a positive
to reverse) and is slightly positive on holdout. **No full sign reversal**
(`holdout_full_reversal = false`).

## 30. Calibration results

L2 reliability (validation, ECE): 5m 0.0583 → **unusable** (≥0.8 tail fails the
majority floor); 30m 0.1080 → **ranking_only**; 1h 0.1181 → **ranking_only**.

## 31. ≥0.8 confidence-tail results

5m: tail n 1,562,179 (fraction ~0.02278), tail accuracy 0.49656 < majority floor
0.51225 → **does not beat floor**. 30m: n 5,587,433, acc 0.58998 > floor 0.52901 →
beats (overconfident). 1h: n 5,077,526, acc 0.53602 > floor 0.53516 → beats
(overconfident).

## 32. 30m / 1h secondary interpretation

Both beat the persistence floor on some information metrics but fail the majority-floor
accuracy requirement; neither is a **positive frozen secondary diagnostic**
(`secondary_positive_flags = {30m: false, 1h: false}`); neither can upgrade or rescue
the 5m primary result.

## 33. Frozen continuation criteria

CONTINUE_ONE_BOUNDED_FOLLOWUP requires **all** of: (1) acc uplift vs majority ≥ +2.0
pp; (2) acc uplift vs persistence ≥ +2.0 pp; (3) macro-F1 uplift vs majority ≥ +0.03;
(4) balanced-accuracy uplift vs majority ≥ +1.0 pp; (5) beats both floors in > ½
validation date blocks; (6) beats both floors in every validation month; (7) holdout
no full reversal; (8) ≥0.8 confidence tail beats the majority floor.

## 34. Exact criteria passed and failed (5m)

1. acc vs majority ≥ +2.0 pp — **FAILED** (−0.222 pp);
2. acc vs persistence ≥ +2.0 pp — passed (+2.128 pp);
3. macro-F1 vs majority ≥ +0.03 — passed (+0.1138);
4. balanced-accuracy vs majority ≥ +1.0 pp — **FAILED** (+0.779 pp);
5. > ½ validation date blocks — passed narrowly (0.511);
6. every validation month — **FAILED** (1 of 2);
7. holdout no full reversal — passed;
8. ≥0.8 tail beats majority — **FAILED** (0.4966 < 0.5122).

## 35. Exact verdict

**`INVESTIGATE_AMBIGUOUS`.**

## 36. Exact ambiguity conditions

`mixed_date_and_month_block_evidence`; `information_suggested_but_not_clean`.

## 37. Confirmation CONTINUE did not apply

Confirmed. Criteria 1, 4, 6, 8 failed → CONTINUE_ONE_BOUNDED_FOLLOWUP did not apply.

## 38. Confirmation STOP was not forced by a hard-negative reversal

Confirmed. `holdout_full_reversal = false`; no hard-negative holdout reversal forced
`STOP_LONGHORIZON_ML_ARC`. With CONTINUE inapplicable, no reversal, and ≥1 ambiguous
condition matched, the deterministic verdict is `INVESTIGATE_AMBIGUOUS`.

## 39. Allowed empirical claim

The frozen 45-feature causal aggTrades set contains measurable long-horizon
directional information **relative to the persistence floor** (~+2 pp accuracy at 5m,
+~0.11 macro-F1 across horizons, holding on holdout with no reversal), but the
evidence is **not clean enough for continuation** (no majority-floor accuracy lift,
incomplete block agreement, unusable 5m confidence tail). Capped at Phase 4bn-AE §8
(a)/(b)/(c).

## 40. Forbidden claims

No claim of tradability, profitability, economic edge, PnL, strategy viability,
execution viability, backtest validity, spread/slippage adequacy, live-readiness, or
production suitability.

## 41. Cost / materiality interpretation

The long-horizon raw-move materiality shares (validation |move| > 16 bps: 5m 34.95 %
/ 30m 64.28 % / 1h 72.72 %; 15s ref 2.47 %) and the locked 8 bps/side · 16 bps
round-trip cost remain **descriptive context only** and entered no target, model,
loss, threshold, weighting, or verdict. aggTrades-only data cannot express spread /
slippage / executable mid / order-book depth / market impact; the absolute Phase
4bn-AE §19 M0-style mechanism-admissibility gate is unchanged.

## 42. Confirmation thresholds were not changed

Confirmed. The frozen Phase 4bn-AE §16 thresholds were applied verbatim to the 5m
primary and **not** relaxed or reinterpreted after the result was seen. The
pre-registered narrow-miss band was not triggered.

## 43. Confirmation no second run

Confirmed. Exactly one fixed baseline run was executed; no rerun during
implementation or merge review.

## 44. Confirmation no seed / configuration change

Confirmed. Seed 20260528 and the frozen L2 constants / persistence definition /
feature set / transform were unchanged throughout.

## 45. Confirmation no source Parquet read during merge review

Confirmed. Merge review read only the compact AQ / AR JSON artefacts + sidecars and
git metadata; no feature Parquet, label Parquet, or raw zip was read; AR was not
rerun.

## 46. Confirmation no local output mutation during merge review

Confirmed. Neither the AQ input namespace nor the AR output namespace was written,
refreshed, normalized, repaired, or deleted; AQ re-verified byte-identical.

## 47. Confirmation no row-level prediction artefact

Confirmed. `persisted_row_level_predictions = false`; no row-level prediction file
exists in the AR namespace.

## 48. Confirmation no data / model artefact committed

Confirmed. The AR and AQ namespaces are gitignored and untracked; `git ls-files
data/` reports zero tracked files; `data_committed = false`.

## 49. Confirmation no v002 / sealed / test read

Confirmed. `test_rows_loaded = 0`; `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`.

## 50. Confirmation no AH / AJ / AN / AQ namespace mutation

Confirmed. No AH / AJ / AN / AQ namespace was mutated; AQ re-verified byte-identical.

## 51. Confirmation no AH / AI / AJ / AN / AQ rerun

Confirmed. No builder or diagnostic was rerun (AQ / AN / AH builders, AI diagnostics,
AJ baseline); AR reused their read-only helpers by import only.

## 52. Confirmation no feature / model / hyperparameter / threshold search

Confirmed. No model / feature / hyperparameter / threshold / seed / epoch search; no
cross-validation; no calibration training; no probability recalibration; no
confidence-threshold selection; no model selection.

## 53. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write

Confirmed. None occurred and none is authorized.

## 54. Confirmation all authorization flags remain false

Confirmed (`run_record.json`): `ml_authorized`, `diagnostics_authorized`,
`strategy_authorized`, `signals_authorized`, `pnl_authorized`, `backtest_authorized`,
`live_authorized`, `exchange_write_authorized` all `false`; every AQ
non-authorization flag preserved `false`; `authorized_successor_phase = false`.

## 55. Confirmation flip_research_eligible(...) was not invoked

Confirmed. `flip_research_eligible_invoked = false`; the Phase 4aw always-raises
invariant is preserved; `research_eligible` unchanged.

## 56. Validation commands and results

- `git diff --name-status main..AR` → 9 additions only (0 modifications);
- targeted AR tests → **49 passed**;
- combined AR + AJ + AQ + import-boundary tests → **204 passed** (superset of the
  prior report's 123-count AR+AJ+AQ subset; all required scopes included, all pass);
- `ruff check` on AR source / script / tests → clean;
- `mypy --follow-imports=silent` on the two new AR modules → clean (strict
  whole-package residual errors are pre-existing `ndarray` type-param findings in the
  frozen `ml_baseline_models_v002` / `ml_baseline_metrics_v002` modules, unchanged);
- `git diff --check` → clean;
- AQ artefacts re-verified byte-identical; AR 12/12 sidecars verified; no forbidden
  artefact; both namespaces gitignored; 0 tracked data files.

## 57. Git status before merge

Only `?? .claude/scheduled_tasks.lock` untracked (not staged, not committed). No
`data/` file staged.

## 58. Merge method

`git merge --no-ff phase-4bn-ar/fixed-longhorizon-baseline-run-verdict` into `main`
(no squash, no rebase). `.claude/scheduled_tasks.lock` and all local data/model
artefacts excluded.

## 59. Merge-closeout branch commit SHA

`PENDING_MERGE_CLOSEOUT_BRANCH_COMMIT` (this merge-closeout, committed on the AR
branch before merge; finalized below).

## 60. Merge commit SHA

`PENDING_MERGE_COMMIT` (no-fast-forward merge into main; finalized below).

## 61. SHA-finalization commit

`PENDING_SHA_FINALIZATION_COMMIT` (docs: finalize merge closeout SHAs, on main).

## 62. Final main / origin SHA

`PENDING_FINAL_MAIN_SHA` (main == origin/main after push).

## 63. Final result state

`LONGHORIZON_FIXED_BASELINE_RUN_MERGED_TO_MAIN__INVESTIGATE_AMBIGUOUS_RECORDED__NO_STRATEGY__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 64. Recommended state

**Remain paused.**

## 65. Remaining blockers before any follow-up ML work

- a separate operator authorization is required;
- at most a **docs-only** decision memo may be considered (not started here);
- no model rerun is authorized;
- no feature / calibration / threshold work is authorized.

## 66. Remaining blockers before strategy / PnL / backtest / live

- the absolute Phase 4bn-AE §19 M0-style mechanism-admissibility gate;
- spread / slippage / executable-mid / order-book realism unresolved (aggTrades-only);
- a separate authorization is required for every downstream capability.

## 67. Explicit no-successor execution statement

Phase 4bn-AR authorizes **no** successor execution phase, generates no successor
prompt, and starts no docs-only ambiguity decision memo. This merge-closeout performs
merge review + the no-fast-forward merge to main only. No follow-up model run, fourth
model, search, calibration, strategy, signals, PnL, backtest, paper/shadow, live,
deployment, or exchange-write is authorized. Do not merge further, rebase, or start
any successor phase without explicit operator authorization.

## 68. Preserved project locks

- Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked);
- Phase 4bb-F canonical sidecar policy;
- Phase 4bn-AE claim scope and §19 M0 boundary;
- locked 8 bps/side · 16 bps round-trip cost (descriptive only);
- Phase 4bn-AP frozen model and verdict contract;
- Phase 4bn-AQ dataset identity / bindings / transform / split / proof (byte-identical);
- Phase 4bn-AR exact observed metrics and verdict (`INVESTIGATE_AMBIGUOUS`),
  preserved without reinterpretation.
