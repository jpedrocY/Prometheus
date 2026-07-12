# Phase 4bn-AQ — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AQ — Long-Horizon ML Dataset Build Implementation + Single Controlled Run.
Branch: `phase-4bn-aq/longhorizon-ml-dataset-build-single-run`.

## 2. Phase type

Code + tests + one controlled data-reading dataset build; **merge-only review**;
no models. During merge review: no Parquet read; no build rerun; no output-namespace
mutation; no ML; no strategy; no successor execution authorized.

## 3. Base SHA

`75bbfa3a2ec789c112e794494904c7a47a8fd06c`
(pre-AQ `main` tip; the `docs(phase-4bn-ap): finalize merge closeout shas` commit.)

## 4. Pre-merge AQ branch HEAD

`765c36f4189c850acbbe340d355385efa445c3b6`
(`feat(phase-4bn-aq): build long-horizon ml dataset artefacts`).

## 5. Main / origin main before merge

`main == origin/main == 75bbfa3a2ec789c112e794494904c7a47a8fd06c` (verified in sync
before merge).

## 6. AQ implementation summary

Phase 4bn-AQ implemented the Phase 4bn-AP-pre-registered long-horizon ML
dataset-build step: it bound the frozen Phase 4bn-AH 45-feature causal aggTrades
source to the Phase 4bn-AN long-horizon label family
(`microstructure_labels_longhorizon_aggtrades_v001`; horizons 5m/30m/1h;
`label_config_hash edaeafde…`) under one new dataset contract, and ran the single
controlled full build once over the admitted pre-v002 segment (BTCUSDT,
2024-03-01 .. 2024-11-30, 275 partitions / 400,001,695 rows). It produced a compact,
leakage-proof dataset **specification** (7 JSON + 7 sidecars, ~193 KiB) in one
local/gitignored namespace — no wide matrix, no model, no prediction, no baseline,
no metric. It ran no model, evaluated no predictive performance, and did not decide
whether the long-horizon ML arc continues.

## 7. Files added by AQ

- `src/prometheus/research/microstructure/longhorizon_ml_dataset_contract_v001.py`
- `src/prometheus/research/microstructure/build_longhorizon_ml_dataset_v001.py`
- `scripts/phase4bn_aq_build_longhorizon_ml_dataset.py`
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_contract.py`
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_build.py`
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_proof.py`
- `docs/00-meta/implementation-reports/2026-07-10_phase-4bn-aq_longhorizon-ml-dataset-build-single-run.md`
- `docs/00-meta/implementation-reports/2026-07-10_phase-4bn-aq_closeout.md`
- `docs/00-meta/implementation-reports/2026-07-10_phase-4bn-aq_merge-closeout.md` (this file)

`git diff --name-status main..<AQ branch>` shows only `A` (added) entries.

## 8. Confirmation no frozen files were modified

No existing frozen source module, no AH / AN / AJ module, no published manifest, no
gate report, no sidecar, no split file, no frozen ML configuration, and no existing
report were modified or deleted. The diff is additions-only. ✅

## 9. Local output namespace

`data/research/microstructure/ml_datasets/longhorizon_pre_v001/`.

## 10. Confirmation output namespace is local and gitignored

Local and gitignored via `.gitignore:88` (`data/research/`); distinct from the AH
dataset namespace `…/ml_datasets/pre_v002_contract_v001/`; not committed; not tracked. ✅

## 11. Output artefact inventory

7 JSON + 7 canonical Phase 4bb-F `.sha256` sidecars (14 files, 198,130 bytes / ~193 KiB):

| Artefact | SHA256 |
|---|---|
| `dataset_manifest.json` | `a6be11a039efb52ca4b50719cd46fe1b1986441078c4870ff9e1ea9492d8fefb` |
| `split_index.json` | `9a1835f5895d8affa104c9607e2087579fd774b841ead43046483dbfcb0dda42` |
| `train_only_transform.json` | `0f79aab7211ed131c483ff5cd0191fec23465902fe01a2433b4d1c3802db9c80` |
| `leakage_split_integrity_proof.json` | `7915e73f8f321480bc6d4af5a97db0c346c380bbcbd174c2c8792f2e77de21b7` |
| `source_binding.json` | `411269986ec1175871435e90253d87ef605fa9f0b498f135088022b4c9f8ca42` |
| `sidecar_inventory.json` | `4ee6ca40e7fd1949617df88af53aedff5a024d14d3592b192dbad1211b3e8c3a` |
| `build_run_record.json` | `0f5191ce41f1fc29519147ee746f79ffda74be6e11455103c2307cafcdcdb9d6` |

## 12. Confirmation 7/7 sidecars valid

Independent merge-review recompute matched all 7 artefact SHA256s to their two-space
canonical `.sha256` sidecar bodies and basenames — **7/7 valid**. ✅

## 13. Confirmation no Parquet / model / prediction / baseline artefact was written

The namespace holds only the 7 JSON specs + 7 sidecars — no Parquet, model,
prediction, baseline, or performance-metric file. ✅

## 14. Dataset family and contract identity

Family `microstructure_ml_dataset_longhorizon_pre_v001`; contract
`microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001` (version
`v001`); sibling of (never mutating) the 15s dataset contract
`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`.

## 15. Dataset contract hash

`a310eabf7854ae13ffed1baa2d57a8cf557a3d90dec24337a61e4ca26a9c3873` (consistent across
`dataset_manifest.json`, `leakage_split_integrity_proof.json`, `source_binding.json`).

## 16. Feature family, count, and allowlist hash

Family `microstructure_features_aggtrades_v001`; `feature_count = 45` (the frozen AH
allowlist, imported unchanged); feature-list hash
`8e705ba8800421ae0ccc55cdbf115a36dce9f27f8682e552e2b59c4ab83df7b9` (identical to the
AH 15s dataset). Feature manifest `4881eb87…`; feature config hash `0726b41d…`
(v002-terminal `819cfa7a…` rejected); feature gate `db731d1b…`; normalized manifest
`0e96ae37…`; normalized gate `3452fd9d…`.

## 17. Label family and label_config_hash

Family `microstructure_labels_longhorizon_aggtrades_v001`; `label_config_hash
edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`; AN manifest SHA
`b1ee9afd8dadc410216516f6fa291aa49a26ba788480eb7d98126fc45919f4c0`.

## 18. Feature / label source-binding summary

The AN manifest's `source_feature_manifest_sha256` equals the verified committed
feature manifest SHA (`4881eb87…`), and each of the 275 AN per-day
`paired_source_feature_parquet_sha256` equals its feature-manifest inventory SHA —
proving the labels were built against exactly this feature source. Rejected v002
(`352bad41…`) and 15s short-horizon (`b3bd5d2b…`) label identities excluded by
construction.

## 19. Target horizon roles

Primary: `forward_direction_5m` (300,000 ms) — sole decision horizon. Secondary
diagnostics: `forward_direction_30m` (1,800,000 ms), `forward_direction_1h`
(3,600,000 ms) — cannot upgrade a failed 5m result. Return columns
`forward_log_return_{5m,30m,1h}` are horizon metadata only; labels are targets only,
never features.

## 20. Split policy and date counts

`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` (Phase 4bn-AA;
split-policy commit `e12e928e33aa84e530a85a1a58b04d6ac217b1fb`). Date counts: train
214 / embargo 2 / validation 45 / holdout 14 = 275. Deterministic UTC-date
assignment; AN-recorded per-day split equals the deterministic policy split for all
275 dates.

## 21. Raw split row counts

Train 304,816,127 / embargo 3,071,370 / validation 68,578,296 / holdout 23,535,902
(sum 400,001,695).

## 22. Strict alignment keys and mismatch count

Keys `row_index, agg_trade_id, feature_timestamp_ms, source_transact_time_ms,
utc_date`; **0 mismatches** over all 400,001,695 rows; no join / reorder / fill /
tolerance merge.

## 23. Per-horizon support counts

| split | 5m | 30m | 1h |
|---|---|---|---|
| train | 304,816,127 | 304,816,127 | 304,816,127 |
| validation | 68,578,296 | 68,578,296 | 68,578,296 |
| holdout | 23,534,374 | 23,525,986 | 23,512,252 |

## 24. Per-horizon censoring counts

Holdout tail only: 5m = 1,528; 30m = 9,916; 1h = 23,650. Train censoring = 0;
validation censoring = 0; invalid-price rows = 0; non-censored null-direction rows = 0.

## 25. Confirmation censored targets excluded without imputation

Per-horizon censored / invalid / null-direction rows are excluded from that horizon's
valid-target support with **no imputation** (`targets_imputed = false`). ✅

## 26. Train-only transform policy

`subtract_train_mean_divide_by_max_train_std_epsilon`, ε = 1e-8,
`STANDARDIZE_BOOLEAN_FLAGS = false`, `imputation_rule = fixed_zero_for_null_numeric`
(recorded for the future model matrix; no target imputed here); fit on the `train`
split only over primary-5m-valid rows; validation / holdout / embargo never inspected
for the fit.

## 27. Train fit-row count

304,816,127 train rows valid for the primary 5m target.

## 28. Non-finite feature-cell accounting

2,783 non-finite feature cells excluded from the mean/std fit across the 45 columns —
excluded from the statistic only, never imputed into any target.

## 29. Confirmation no feature dropped

No feature was dropped on statistics; constant/degenerate columns (e.g.
`invalid_window_flag`, all-zero in the train segment → std 0) are handled
invariant-safely by the `max(train_std, ε)` denominator. All 45 features retained. ✅

## 30. Leakage / split / integrity proof summary

`leakage_split_integrity_proof.json`: admitted-source scope only; feature ↔ label
source binding by SHA/config/hash; strict positional alignment over the 5 keys with 0
mismatches; per-horizon earlier-model-split boundary-crossing rows = 0; deterministic
UTC-date split; 1-day boundary embargo preserved; embargo rows used in model splits =
0; per-horizon censored targets excluded without imputation; forbidden-feature scan
clean; all eight non-authorization flags `false`; no model / prediction / baseline /
metric artefact. Validates through the frozen Phase 4bn-AF conservative-posture
validator.

## 31. Boundary-crossing count

Per-horizon earlier-model-split boundary crossings = **0** for train/validation ×
5m/30m/1h (the one-full-day embargo, 86,400,000 ms, strictly dominates the 3,600,000
ms max horizon; proven from each row's `reference_timestamp_ms_H` vs the later-split
boundary).

## 32. v002 / sealed / test exclusion summary

`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`test_rows_loaded = 0`. Only the pre-v002 segment (2024-03-01 .. 2024-11-30) was read;
the split policy raises on any out-of-segment date.

## 33. Budget preflight and storage footprint

Real Phase 4bn-L preflight: `D:` free 1,154.69 GiB ≥ 500 GiB floor → passed (no
breaches); live 350 GiB fail-closed floor re-checked every 25 partitions. Output
footprint 198,130 bytes (~193 KiB), far under the 125 GiB derived-footprint hard cap.

## 34. Build runtime

Single controlled full run: **1,150.9 s (~19.2 min)** (550-file source hash
verification + streaming 275 partitions + 7 artefact writes). A separate prior
no-write `--dry-run` took 416.3 s.

## 35. Confirmation exactly one full controlled run occurred

Exactly one full controlled build run occurred (one-run guarded: `run()` refuses to
overwrite an existing `dataset_manifest.json`). ✅

## 36. Confirmation no build rerun occurred during merge review

No AQ / AN / AH / AI / AJ builder or workflow was run during merge review. ✅

## 37. Confirmation no source Parquet was read during merge review

Merge review read only committed source (git objects, docs) and the 7 compact AQ JSON
artefacts + sidecars. No feature Parquet, no label Parquet, no raw zip was read. ✅

## 38. Confirmation no local output mutation occurred during merge review

The AQ output namespace was read-only during merge review — not rewritten, refreshed,
normalized, repaired, deleted, or otherwise mutated. All 7 artefact SHAs are unchanged
from the build. ✅

## 39. Test results

- AQ targeted tests (3 files) → **51 passed**.
- Combined AQ + `test_import_boundaries` + `test_phase4bn_an_longhorizon_labels` +
  `test_phase4bn_ah_pre_v002_ml_dataset_run` + `test_phase4bn_aa_pre_v002_split_policy`
  → **241 passed**.

## 40. Ruff result

`ruff check` (AQ source / script / tests) → **All checks passed**.

## 41. Mypy result

`mypy` (both new AQ src modules) → **no errors** (repo-wide baseline errors exist only
in unrelated pre-existing numpy-heavy modules).

## 42. Git diff and tracked-data checks

`git diff --name-status main..<AQ branch>` → 8 `A` entries only; `git diff --check`
clean; `git ls-tree -r --name-only <AQ branch> -- data/microstructure/` and
`data/research/` → empty; `git ls-files data/microstructure/` and `data/research/` →
empty; `git check-ignore -v` → both roots ignored.

## 43. Confirmation no data committed

No file under `data/` is tracked or staged; `data_committed = false`. ✅

## 44. Confirmation no AH / AJ / AN namespace mutation

The AH ML-dataset namespace, the AJ baseline namespace, and the AN long-horizon label
namespace were not written or altered (the AH dataset namespace was not even inspected).
`ah_dataset_namespace_mutated = false`; `longhorizon_label_family_mutated = false`;
`frozen_v002_family_mutated = false`. ✅

## 45. Confirmation no AH / AI / AJ / AN rerun

None were run or imported for execution. ✅

## 46. Confirmation no ML / training / scoring / prediction / inference

None occurred. `no_models = no_predictions = no_metrics = true`; `ml_authorized =
false`. ✅

## 47. Confirmation no baseline run

No majority / persistence / L2-logistic baseline was constructed, run, or scored. ✅

## 48. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search

None. The 45-feature allowlist is used verbatim; the strict-sign direction targets
are frozen; no threshold / capacity / hyperparameter tuned or compared. ✅

## 49. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write

None touched. ✅

## 50. Confirmation all eight non-authorization flags remain false

`ml_authorized`, `diagnostics_authorized`, `strategy_authorized`, `signals_authorized`,
`pnl_authorized`, `backtest_authorized`, `live_authorized`, `exchange_write_authorized`
— all `false`. ✅

## 51. Confirmation flip_research_eligible(...) was not invoked

The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved;
it was never invoked. ✅

## 52. Allowed claims preserved

Phase 4bn-AE §8 allowed claim scope (directional-information diagnostic; v002 small-lift
sign reproduction; calibration/confidence-tail assessment) is preserved and unexercised
— AQ makes no predictive or performance claim. ✅

## 53. Forbidden claims preserved

Phase 4bn-AE §8/§19 forbidden claim scope (tradability, profitability, strategy/execution
viability, slippage/spread adequacy, live/paper-shadow readiness, PnL, backtest validity,
production suitability, economic significance) is preserved. Long-horizon materiality
remains descriptive raw-move-distribution context only; aggTrades-only data cannot
express spread/slippage/mid-price realism. ✅

## 54. Locked 8 bps/side and 16 bps round-trip cost preserved

The locked cost reference (8 bps/side · 16 bps round-trip) is preserved and descriptive
only; it never entered any target. ✅

## 55. Phase 4bn-AE §19 M0 boundary preserved

The absolute Phase 4bn-AE §19 M0 mechanism-admissibility gate is preserved; AQ does not
approach it. ✅

## 56. Future fixed baseline run remains not started

The future fixed long-horizon baseline run was neither started nor prompted. ✅

## 57. Future fixed baseline run requires separate operator authorization

It requires its own separate explicit operator authorization; this phase does not
provide it. ✅

## 58. No successor execution is authorized

No successor execution phase is authorized by AQ or by this merge. ✅

## 59. Validation commands and results

- `git status --short` → only `.claude/scheduled_tasks.lock` untracked.
- `git diff --check` → clean.
- `git diff --name-status main..<AQ branch>` → 8 additions only.
- `git ls-tree -r --name-only <AQ branch> -- data/microstructure/` / `-- data/research/`
  → empty.
- `git ls-files data/microstructure/` / `data/research/` → empty.
- `git check-ignore -v data/microstructure/` / `data/research/` → both ignored.
- `pytest` → 51 (AQ) and 241 (combined) passed.
- `ruff check` → clean; `mypy` (2 new modules) → clean.
- Artefact verification → 7/7 JSON sidecars valid; manifest/proof/source_binding
  contract-hash + bindings + alignment + boundary crossings consistent; no
  Parquet/model/prediction/baseline artefact; namespace gitignored.

## 60. Git status before merge

`git status --short` shows only untracked `.claude/scheduled_tasks.lock` (never staged,
never committed). No data file tracked or staged.

## 61. Merge method

`git merge --no-ff phase-4bn-aq/longhorizon-ml-dataset-build-single-run` (no squash, no
rebase). `.claude/scheduled_tasks.lock` and every local data artefact excluded.

## 62. Merge-closeout branch commit SHA

`96e2c92cdb72ec0f95e185707267f3c10d32da6f` — the `docs(phase-4bn-aq): add merge
closeout` commit on the AQ branch.

## 63. Merge commit SHA

`40350ac09aa0dac8208bfaf40d92d0d0d59446ae` — the `feat(phase-4bn-aq): merge
long-horizon ml dataset build` no-fast-forward merge commit on `main`.

## 64. SHA-finalization commit

This commit — `docs(phase-4bn-aq): finalize merge closeout shas` on `main` (its own SHA
is reproduced in the final operator report; a commit cannot embed its own SHA).

## 65. Final main / origin main SHA

Equal to this SHA-finalization commit after `git push origin main` (reproduced in the
final operator report; a commit cannot embed its own SHA).

### Post-merge validation (recorded at finalization)

- Merge method: `git merge --no-ff` → merge commit `40350ac0…` (9 files added, 3,739
  insertions; additions-only).
- `git status --short` → only `.claude/scheduled_tasks.lock` untracked.
- `git log --oneline -12` → merge commit, merge-closeout `96e2c92`, and implementation
  commit `765c36f` on top of `75bbfa3` (pre-AQ main tip).
- `git diff --check` → clean.
- `git ls-files data/microstructure/` / `data/research/` → empty; `git check-ignore -v`
  → both roots ignored.
- AQ output namespace intact (14 files, ~193 KiB), gitignored, unmutated. No AQ builder
  rerun, no source Parquet read, no baseline/model run during merge/finalization.

## 66. Final result state

`LONGHORIZON_ML_DATASET_BUILD_MERGED_TO_MAIN__LOCAL_DATASET_ARTEFACTS_PRESERVED__NO_MODEL_RUN__NO_STRATEGY__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 67. Recommended state

**Remain paused.**

## 68. Remaining blockers before fixed baseline run

- AQ must be merged successfully (this closeout);
- the dataset artefacts must remain available and valid locally (7/7 verified);
- a separate explicit operator authorization is required;
- the frozen Phase 4bn-AP baseline configuration and kill/continue verdict criteria
  must be preserved.

## 69. Remaining blockers before any strategy / PnL / backtest / live path

- an absolute Phase 4bn-AE §19 M0-style mechanism-admissibility memo (M0.5 cost realism
  at 8 bps/side · 16 bps round-trip, execution feasibility, label economic relevance,
  strategy admissibility vs the retained rejections);
- spread/slippage/mid/book realism remains unresolved (aggTrades-only data cannot supply
  it; the `bookticker_midprice_data_admissibility_memo` remains deferred and unauthorized);
- separate authorization for every downstream capability (strategy / signals / PnL /
  backtest / paper-shadow / live / exchange-write).

## 70. Explicit no-successor execution statement

Phase 4bn-AQ and this merge authorize **no** successor execution phase. They do not
start or authorize the fixed baseline run, any baseline / model / prediction / inference
/ calibration / confidence-tail / evaluation / ML verdict, feature selection, threshold
optimization, model selection, hyperparameter search, or any strategy / signals / PnL /
backtest / paper-shadow / live / exchange-write path; they do not generate the
fixed-baseline-run prompt or any next-phase prompt. Every retained project lock and
verdict is preserved verbatim: the 8 bps/side · 16 bps round-trip cost lock; the Phase
4aw `flip_research_eligible(...)` always-raises invariant (never invoked); the Phase
4bb-F canonical sidecar policy; the Phase 4bn-AE claim-scope and §19 M0 boundary; the
Phase 4bn-AP preregistration contract; the frozen v002 short-horizon family; the Phase
4bn-AN long-horizon label output; the Phase 4bn-AH ML-dataset and Phase 4bn-AJ baseline
namespaces.
