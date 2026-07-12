# Phase 4bn-AQ — Long-Horizon ML Dataset Build Implementation + Single Controlled Run

## 1. Branch

`phase-4bn-aq/longhorizon-ml-dataset-build-single-run`

## 2. Base SHA

`75bbfa3a2ec789c112e794494904c7a47a8fd06c`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AP merge
closeout.)

## 3. Files created / modified

Committed (source / tests / docs only):

- `src/prometheus/research/microstructure/longhorizon_ml_dataset_contract_v001.py` (new)
- `src/prometheus/research/microstructure/build_longhorizon_ml_dataset_v001.py` (new)
- `scripts/phase4bn_aq_build_longhorizon_ml_dataset.py` (new)
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_contract.py` (new)
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_build.py` (new)
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_proof.py` (new)
- `docs/00-meta/implementation-reports/2026-07-10_phase-4bn-aq_longhorizon-ml-dataset-build-single-run.md` (this file)
- `docs/00-meta/implementation-reports/2026-07-10_phase-4bn-aq_closeout.md`

No frozen module, manifest, gate report, sidecar, split file, or ML config was
modified. The AH ML-dataset builder/contract/proof/run modules, the AJ baseline
run module, and the AN long-horizon label modules were **read and imported** but
never edited. `current-project-state.md` left unchanged (see §41 note). **No** data
file was committed.

## 4. Exact documents / source inspected

Docs (authority): `current-project-state.md` (targeted), Phase 4bn-AE, -AH
(builder/closeout), -AN (build/closeout), -AO, -AP (contract/closeout)
implementation reports; Phase 4bb-F sidecar policy report; Phase 4bn-L
derived-storage budget memo.

Committed source: `pre_v002_ml_dataset_contract.py`, `pre_v002_ml_dataset_builder.py`,
`pre_v002_ml_dataset_proof.py`, `pre_v002_ml_dataset_run.py`,
`pre_v002_split_policy.py`, `features_schema_v002.py`, `labels_schema_v002.py`,
`longhorizon_labels_schema_v001.py`, `longhorizon_labels_compute_v001.py`,
`scripts/phase4bn_an_build_longhorizon_labels.py`,
`tests/research/microstructure/test_phase4bn_ah_pre_v002_ml_dataset_run.py`.

## 5. Exact source data paths read

Committed feature/normalized source witnesses + inventories:

- `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
- `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json`
- `data/microstructure/gate-reports/features/…_4bn_s__phase-4bn-t__1780674917156__e647435c81d7.json`
- `data/microstructure/gate-reports/normalized/…_4bn_o__phase-4bn-p__1780599605192__3fd795ceac4f.json`
- 275 feature Parquet + 275 `.sha256` sidecars under
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/BTCUSDT/<YYYY>/<MM>/…`

Admitted pre-v002 long-horizon label source (Phase 4bn-AN, research namespace):

- `data/research/microstructure/labels/microstructure_labels_longhorizon_aggtrades_v001_pre_v002/_manifest/microstructure_labels_longhorizon_aggtrades_v001_pre_v002.manifest.json`
- 275 long-horizon label Parquet + 275 `.sha256` sidecars under
  `…/microstructure_labels_longhorizon_aggtrades_v001_pre_v002/BTCUSDT/<YYYY>/<MM>/…`

Feature Parquet columns read: the 45-feature allowlist + `row_index, agg_trade_id,
feature_timestamp_ms, source_transact_time_ms, utc_date` (45-feature matrix read on
**train** partitions only; alignment keys on all partitions). Label Parquet columns
read: the 5 alignment keys + `utc_date`, `label_invalid_price_flag`,
`forward_direction_{5m,30m,1h}`, `horizon_censored_flag_{5m,30m,1h}`,
`reference_timestamp_ms_{5m,30m,1h}`. No return / mid / book / price / lineage
column beyond the alignment keys was read; no AN target return column entered the
model matrix.

## 6. Exact local output namespace

`data/research/microstructure/ml_datasets/longhorizon_pre_v001/`
(gitignored via `.gitignore:88`; distinct from the AH namespace
`…/ml_datasets/pre_v002_contract_v001/`, which was neither read nor written).

## 7. Confirmation allowed read scope

Read only: committed feature/normalized manifests, gate reports, sidecars; the AN
long-horizon label manifest + label Parquet; only BTCUSDT, only 2024-03-01 ..
2024-11-30 (the 275-date pre-v002 segment); only the columns required for the
45-feature allowlist, alignment keys, split assignment, long-horizon direction
targets, and censoring/support/boundary proof. ✅

## 8. Confirmation forbidden read scope not touched

No raw zip; no endpoint / private / authenticated / WebSocket source; no
unrelated `data/research` namespace; no AN return columns unrelated to
targets/support/alignment; no source column outside the read list; no data read
for model training/evaluation. The AH ML-dataset output namespace was **not**
inspected (the source binding was proven entirely from committed feature witnesses
+ the AN label manifest + the per-date `paired_source_feature_parquet_sha256`
cross-check). ✅

## 9. Confirmation no v002 terminal read

`v002_terminal_window_read = false`. Only the pre-v002 segment
(2024-03-01 .. 2024-11-30) was read; the split policy raises on any out-of-segment
date. ✅

## 10. Confirmation sealed test untouched

`sealed_test_split_touched = false`. The sealed test window
(2025-02-14 .. 2025-02-28) was never resolved, opened, or read. ✅

## 11. Confirmation `test_rows_loaded = 0`

`test_rows_loaded = 0`. ✅

## 12. Confirmation no AH / AJ / AN namespace mutation

The AH ML-dataset namespace, the AJ baseline namespace, and the AN long-horizon
label namespace were not written, moved, or altered. `frozen_v002_family_mutated =
false`; `longhorizon_label_family_mutated = false`; `ah_dataset_namespace_mutated =
false`. Exactly one **new** namespace was created. ✅

## 13. Confirmation no AH builder / AI diagnostics / AJ baseline rerun

None were invoked. ✅

## 14. Confirmation no AN label build rerun

`scripts/phase4bn_an_build_longhorizon_labels.py` was neither run nor imported for
execution; the AN label Parquet were read-only. ✅

## 15. AP contract summary

Phase 4bn-AP froze the architecture `LONGHORIZON_ML_DATASET_BUILD_THEN_FIXED_BASELINE_RUN`
(the proven AH→AJ two-step): a data-reading, no-models dataset-build phase, then a
separately-authorized fixed run-once baseline. It fixed the primary target
`forward_direction_5m` (5m the sole decision horizon; 30m/1h secondary diagnostics
that cannot upgrade a failed 5m result), reuse of the AH 45-feature allowlist
unchanged (no selection, no new features; long-horizon labels are targets not
features), the train-only `subtract_train_mean_divide_by_max_train_std_epsilon`
transform (ε = 1e-8, `STANDARDIZE_BOOLEAN_FLAGS = False`, fit on train only), the
`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` split, the Phase
4bn-AE §13 metric registry / dependence posture / success thresholds, and the
strategy/PnL/backtest/live non-authorization boundary. It recommended a future
dataset-build phase binding the AH 45-feature source to the AN long-horizon label
family (`label_config_hash edaeafde…`) preserving the AH compact-spec posture, the
125 GiB cap, budget preflight, and Phase 4bb-F sidecars. Phase 4bn-AQ implements
exactly that dataset-build step — and nothing downstream.

## 16. Dataset identity and contract identity

- Dataset family: `microstructure_ml_dataset_longhorizon_pre_v001`
- Contract name: `microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001` (version `v001`)
- `dataset_contract_hash`: `a310eabf7854ae13ffed1baa2d57a8cf557a3d90dec24337a61e4ca26a9c3873`
- Sibling (never mutated) of the 15s dataset contract
  `microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`.

## 17. Feature source binding summary

Exactly the Phase 4bn-AH 45-feature causal aggTrades allowlist (`FEATURE_NAMES_V002`,
imported unchanged), `feature_count = 45`, feature-list hash
`8e705ba8800421ae0ccc55cdbf115a36dce9f27f8682e552e2b59c4ab83df7b9` (identical to
the AH 15s dataset). Bound witnesses: feature manifest
`4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`; feature config
hash `0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c` (v002-terminal
`819cfa7a…` rejected); feature gate `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`;
normalized manifest `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`;
normalized gate `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`.

## 18. Label source binding summary

Family `microstructure_labels_longhorizon_aggtrades_v001` (Phase 4bn-AN);
`label_config_hash edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`
(matches the AP-recommended value and the AN manifest); AN manifest SHA256
`b1ee9afd8dadc410216516f6fa291aa49a26ba788480eb7d98126fc45919f4c0`; horizons
`5m/30m/1h`; 275 dates / 400,001,695 rows. The AN manifest's
`source_feature_manifest_sha256` equals the verified committed feature manifest
SHA (`4881eb87…`), and each of the 275 AN per-day
`paired_source_feature_parquet_sha256` equals its feature-manifest inventory SHA —
proving the labels were built against exactly this feature source. The rejected v002
`352bad41…` and short-horizon 15s (`b3bd5d2b…`) label identities are excluded by
construction.

## 19. Feature scope and feature count

Exactly 45 causal aggTrades feature/quality columns; no new features; no feature
selection; forbidden-substring scan clean (`forward_log_return`, `forward_direction`,
`horizon_censored_flag`, `label_`, `split_`, `censored_`); no raw-price / mid / book
column; the allowlist is provably disjoint from every long-horizon target / return /
support / censoring column. Long-horizon direction labels and return columns are
targets/metadata only, never features.

## 20. Target horizon scope

Primary: `forward_direction_5m` (300,000 ms) — the sole decision horizon. Secondary
diagnostics: `forward_direction_30m` (1,800,000 ms), `forward_direction_1h`
(3,600,000 ms). Return columns `forward_log_return_{5m,30m,1h}` recorded as
horizon metadata only (never model features). Target classes `(-1, 0, 1)`; zero
class preserved; strict-sign direction (no deadband / threshold optimization).

## 21. Split policy summary

`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` (Phase 4bn-AA;
split-policy commit `e12e928e33aa84e530a85a1a58b04d6ac217b1fb`). Date counts:
train 214 (2024-03-01..09-30) / embargo 2 (2024-10-01, 2024-11-16) / validation 45
(2024-10-02..11-15) / holdout 14 (2024-11-17..11-30) = 275. Deterministic UTC-date
assignment; no random / shuffle / k-fold / bootstrap. AN-recorded per-day split
equals the deterministic policy split for all 275 dates. Decision evidence remains
block-level (UTC date / month) for the future baseline run.

## 22. Row / alignment summary

400,001,695 rows streamed and strictly positionally aligned over
`row_index, agg_trade_id, feature_timestamp_ms, source_transact_time_ms, utc_date`
— **0 alignment mismatches**, no join / reorder / fill / tolerance merge. Per-day
feature-row = label-row counts. Raw split rows: train 304,816,127 / embargo
3,071,370 / validation 68,578,296 / holdout 23,535,902 (sum 400,001,695).

## 23. Per-horizon support / censoring summary

Per split × horizon **valid-target** rows (censored / invalid / null-direction
excluded, no imputation):

| split | 5m | 30m | 1h |
|---|---|---|---|
| train (304,816,127 raw) | 304,816,127 | 304,816,127 | 304,816,127 |
| validation (68,578,296 raw) | 68,578,296 | 68,578,296 | 68,578,296 |
| holdout (23,535,902 raw) | 23,534,374 | 23,525,986 | 23,512,252 |

Envelope-terminal censored rows (holdout tail only; train + validation = 0):
5m = **1,528**, 30m = **9,916**, 1h = **23,650** — identical to the Phase 4bn-AN
label build. Invalid-price rows = 0; non-censored null-direction rows = 0. Embargo
rows (3,071,370) dropped in full from all model-eligible splits. Per-date, per-horizon
support is recorded in `split_index.json`.

## 24. Train-only transform summary

Fit on the `train` split only, over the 304,816,127 rows valid for the primary 5m
target (`fit_row_selection =
train_split_rows_valid_for_primary_target_forward_direction_5m`); validation /
holdout / embargo never inspected for the fit. Rule
`subtract_train_mean_divide_by_max_train_std_epsilon`, ε = 1e-8,
`STANDARDIZE_BOOLEAN_FLAGS = False`, `imputation_rule = fixed_zero_for_null_numeric`
(recorded for the future model matrix; **no target imputed here**). Per-feature
`train_mean`, `train_std`, `max(train_std, ε)` denominator, `train_count`,
`train_null_count` recorded for all 45 features. Total non-finite feature cells
excluded from the fit across the 45 columns = **2,783** (excluded from mean/std,
never imputed into any target). Constant/degenerate columns (e.g.
`invalid_window_flag`, all-zero in the train segment → std 0) are handled
invariant-safely by the `max(std, ε)` denominator — no feature was dropped on
statistics.

## 25. Leakage / split / integrity proof summary

`leakage_split_integrity_proof.json` records: admitted-source scope only; feature
source binding + label source binding bound together by SHA/config/hash; strict
positional alignment over the 5 keys with 0 mismatches; **per-horizon earlier-model-
split boundary-crossing rows = 0** for train/validation × 5m/30m/1h (the one-full-day
embargo, 86,400,000 ms, strictly dominates the 3,600,000 ms max horizon; proven from
each row's `reference_timestamp_ms_H` vs the later-split boundary); deterministic
UTC-date split assignment; 1-day boundary embargo preserved; embargo rows used in
model splits = 0; per-horizon censored targets excluded without imputation;
`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`test_rows_loaded = 0`; `data_committed = false`; `frozen_v002_family_mutated =
false`; `longhorizon_label_family_mutated = false`; `ah_dataset_namespace_mutated =
false`; forbidden-feature scan clean; all eight non-authorization flags `false`; no
model / prediction / baseline / metric artefact. The proof validates through the
frozen Phase 4bn-AF conservative-posture validator before any write.

## 26. Output artefact inventory

Under the namespace (each with a paired canonical Phase 4bb-F `.sha256` sidecar):

| Artefact | SHA256 |
|---|---|
| `train_only_transform.json` | `0f79aab7211ed131c483ff5cd0191fec23465902fe01a2433b4d1c3802db9c80` |
| `split_index.json` | `9a1835f5895d8affa104c9607e2087579fd774b841ead43046483dbfcb0dda42` |
| `source_binding.json` | `411269986ec1175871435e90253d87ef605fa9f0b498f135088022b4c9f8ca42` |
| `leakage_split_integrity_proof.json` | `7915e73f8f321480bc6d4af5a97db0c346c380bbcbd174c2c8792f2e77de21b7` |
| `dataset_manifest.json` | `a6be11a039efb52ca4b50719cd46fe1b1986441078c4870ff9e1ea9492d8fefb` |
| `build_run_record.json` | `0f5191ce41f1fc29519147ee746f79ffda74be6e11455103c2307cafcdcdb9d6` |
| `sidecar_inventory.json` | `4ee6ca40e7fd1949617df88af53aedff5a024d14d3592b192dbad1211b3e8c3a` |

14 files total (7 JSON + 7 sidecars). No Parquet, model, prediction, or baseline
artefact. Compact-spec design: no full `400,001,695 × 45` matrix materialised.

## 27. Sidecar / hash validation summary

Independent post-run verification recomputed every artefact SHA256 and matched it to
its two-space canonical `.sha256` sidecar and basename — **7/7 valid**. Pre-read
verification hash-matched all 550 source Parquet (275 feature + 275 label) against
both their manifest inventory SHAs and their on-disk sidecars, plus the 6 committed
manifest/gate files and the AN manifest.

## 28. Build budget preflight

Real Phase 4bn-L preflight: `D:` free **1,154.69 GiB** ≥ 500 GiB floor → passed
(breaches = none). Caps carried: derived footprint 75/125 GiB, total stack 250/300
GiB, runtime 4/8 h, temp 50/100 GiB; live fail-closed floor 350 GiB re-checked every
25 partitions. The compact-spec artefact (~193 KiB) never approaches any footprint
cap.

## 29. Build runtime summary

Single controlled full run: **1,150.9 s (~19.2 min)** (550-file source hash
verification + streaming 275 partitions + 7 artefact writes). A prior no-write
`--dry-run` (full source-binding verification only) took 416.3 s. Both fail-closed
before any write on any breach.

## 30. Storage footprint

Output namespace total **198,130 bytes (~193 KiB)**, well under the Phase 4bn-L
125 GiB derived-footprint hard cap. `D:` free unchanged materially (1,154.69 GiB).

## 31. Gitignored / local namespace confirmation

`git check-ignore -v data/research/microstructure/ml_datasets/longhorizon_pre_v001/…`
→ `.gitignore:88 data/research/`. The namespace is local and gitignored; it does not
appear in `git status`. ✅

## 32. Confirmation no data committed

`git ls-files data/microstructure/` → empty; `git ls-files data/research/` → empty.
No data file staged or committed; `data_committed = false`. ✅

## 33. Confirmation no ML / training / scoring / prediction / inference

None occurred. The build reads data and computes descriptive counts + train-only
feature statistics only. `no_models = no_predictions = no_metrics = true`;
`ml_authorized = false`. ✅

## 34. Confirmation no baseline run

No majority / persistence / L2-logistic baseline was constructed, run, or scored. ✅

## 35. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search

None. The 45-feature allowlist is used verbatim; the direction targets use the frozen
strict-sign policy; no threshold, capacity, or hyperparameter was tuned or compared. ✅

## 36. Confirmation no strategy / signals / PnL / backtest / live / exchange-write

None. No strategy, signal, PnL, backtest, Sharpe/hit-rate/turnover/position/execution,
paper/shadow, live, or exchange-write path was touched. ✅

## 37. Allowed claims preserved

Phase 4bn-AE §8 allowed claim scope (directional-information diagnostic; v002 small-
lift sign reproduction; calibration/confidence-tail assessment) is preserved and
unexercised here — this phase makes no predictive or performance claim. Long-horizon
materiality (5m/30m/1h) remains **descriptive raw-move-distribution** context only.

## 38. Forbidden claims preserved

Phase 4bn-AE §8 forbidden claim scope (tradability, profitability, strategy/execution
viability, slippage/spread adequacy, live/paper-shadow readiness, PnL, backtest
validity, production suitability, economic significance) is preserved. The locked
cost reference (8 bps/side · 16 bps round-trip) is descriptive only; aggTrades-only
data cannot express spread/slippage/mid-price realism.

## 39. Validation commands and results

- `pytest` (3 new AQ test files) → **51 passed**.
- `pytest` (AQ + `test_import_boundaries` + `test_phase4bn_an_longhorizon_labels` +
  `test_phase4bn_ah_pre_v002_ml_dataset_run` + `test_phase4bn_aa_pre_v002_split_policy`)
  → **241 passed**.
- `ruff check` (new source / script / tests) → **All checks passed**.
- `mypy` (both new src modules) → **no errors** (repo-wide baseline errors exist only
  in unrelated pre-existing numpy-heavy modules; the two new modules are clean).
- `phase4bn_aq_build_longhorizon_ml_dataset.py --dry-run` → 275/275 partitions
  verified, preflight passed, no output written.
- Single controlled full run → 400,001,695 rows, 0 alignment mismatches, 0 boundary
  crossings, 7 artefacts written.
- Post-run: 7/7 artefact sidecars valid; proof/manifest consistent;
  `git ls-files data/microstructure/` and `data/research/` empty;
  `git check-ignore -v` confirms the namespace is ignored; `git diff --check` clean.

## 40. Git status

`git status --short` shows only untracked: the 3 new source/script files, the 3 new
test files, and the transient `.claude/scheduled_tasks.lock` (never staged, never
committed). No data file tracked or staged.

## 41. Result state

`LONGHORIZON_ML_DATASET_BUILD_COMPLETE__LOCAL_DATASET_ARTEFACTS_WRITTEN__NO_MODEL_RUN__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

`current-project-state.md` update convention: this is a paused, no-successor,
local-only dataset-build phase (parallel to Phase 4bn-AH/AN, which did not require a
current-project-state edit at this point). It remains **unchanged**; the phase state
is recorded by this report + closeout.

## 42. Recommended next state

**Remain paused.** The long-horizon ML dataset specification exists locally
(gitignored) with verified integrity, source binding, split/support index, and
train-only transform. The next step (a separately-authorized fixed run-once baseline
over `forward_direction_5m` with 30m/1h diagnostics) is **not** authorized by this
prompt and must be requested explicitly.

## 43. Explicit no-successor execution statement

Phase 4bn-AQ authorizes **no** successor execution phase. It does not run or
authorize the future fixed baseline run, any majority / persistence / L2-logistic
baseline, model training / scoring / prediction / inference / calibration /
confidence-tail selection / evaluation / ML verdict, feature selection, threshold
optimization, model selection, hyperparameter search, capacity comparison, or any
strategy / signals / PnL / backtest / paper-shadow / live / exchange-write path; it
does not decide whether the long-horizon ML arc continues; it does not generate the
next-phase prompt or a merge-closeout. Every retained project lock and verdict is
preserved verbatim: the 8 bps/side · 16 bps round-trip cost lock; the Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked); the Phase
4bb-F sidecar policy; the Phase 4bn-AE claim-scope and strategy/PnL/backtest/live
boundary; the Phase 4bn-AP no-ML/no-successor boundary; the frozen v002 short-horizon
family; the Phase 4bn-AN long-horizon label output; the Phase 4bn-AH ML-dataset and
Phase 4bn-AJ baseline namespaces. Do not merge to main and do not push unless
explicitly instructed later.
