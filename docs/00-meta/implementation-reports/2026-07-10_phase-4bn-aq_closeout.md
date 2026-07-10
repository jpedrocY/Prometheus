# Phase 4bn-AQ — Closeout

## Branch

`phase-4bn-aq/longhorizon-ml-dataset-build-single-run`

## Base SHA

`75bbfa3a2ec789c112e794494904c7a47a8fd06c`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AP merge
closeout.)

## Phase type

Code + tests + **single controlled data-reading dataset build, no models**.
Implements the long-horizon ML dataset-build step pre-registered by Phase 4bn-AP:
binds the Phase 4bn-AH 45-feature causal aggTrades source to the Phase 4bn-AN
long-horizon label family (`microstructure_labels_longhorizon_aggtrades_v001`;
horizons 5m/30m/1h; `label_config_hash edaeafde…`) and materialises a compact,
leakage-proof dataset **specification** once over the admitted pre-v002 segment.
Reads only admitted pre-v002 sources; writes only a local/gitignored namespace; no
ML; no baseline; no strategy; no successor execution authorized.

## Files created / modified

Committed (source / tests / docs only):

- `src/prometheus/research/microstructure/longhorizon_ml_dataset_contract_v001.py`
- `src/prometheus/research/microstructure/build_longhorizon_ml_dataset_v001.py`
- `scripts/phase4bn_aq_build_longhorizon_ml_dataset.py`
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_contract.py`
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_build.py`
- `tests/research/microstructure/test_phase4bn_aq_longhorizon_ml_dataset_proof.py`
- `docs/00-meta/implementation-reports/2026-07-10_phase-4bn-aq_longhorizon-ml-dataset-build-single-run.md`
- `docs/00-meta/implementation-reports/2026-07-10_phase-4bn-aq_closeout.md` (this file)

No frozen module, manifest, gate report, sidecar, split file, or ML config modified.
`current-project-state.md` left unchanged (report §41). **No** data file committed.

## Local output namespace

`data/research/microstructure/ml_datasets/longhorizon_pre_v001/`
(gitignored via `.gitignore:88`; distinct from the AH namespace, which was neither
read nor written).

## Output artefact inventory

7 compact JSON artefacts + 7 canonical Phase 4bb-F `.sha256` sidecars (14 files,
~193 KiB total): `dataset_manifest.json`, `split_index.json`,
`train_only_transform.json`, `leakage_split_integrity_proof.json`,
`source_binding.json`, `sidecar_inventory.json`, `build_run_record.json`. No Parquet,
model, prediction, or baseline artefact. `dataset_contract_hash a310eabf7854ae13…`;
feature-list hash `8e705ba8…`; `label_config_hash edaeafde…`.

## Validation commands

- `pytest` (3 new AQ files) → **51 passed**; (AQ + import-boundaries + AN labels + AH
  run + AA split policy) → **241 passed**.
- `ruff check` (new source/script/tests) → **All checks passed**.
- `mypy` (both new src modules) → **no errors** (only the repo's pre-existing baseline
  errors in unrelated frozen numpy modules).
- `--dry-run` → 275/275 partitions verified, preflight passed, no output written.
- Single controlled run → 400,001,695 rows, 0 alignment mismatches, 0 boundary
  crossings, 7 artefacts written.
- `git status --short`, `git diff --check`, `git ls-files data/microstructure/`,
  `git ls-files data/research/`, `git check-ignore -v` → 0 data tracked, both ignored,
  clean.
- Post-run artefact verification: 7/7 JSON sidecars valid; proof/manifest consistent.

## Concise dataset-build outcome

Single controlled run built the compact long-horizon ML dataset spec over
**275 partitions / 400,001,695 rows** in **1,150.9 s (~19.2 min)**, ~193 KiB, far
under the Phase 4bn-L 125 GiB cap. Strict positional alignment over
`row_index, agg_trade_id, feature_timestamp_ms, source_transact_time_ms, utc_date` —
**0 mismatches**. Split counts train 214 / embargo 2 / validation 45 / holdout 14;
raw split rows train 304,816,127 / embargo 3,071,370 / validation 68,578,296 /
holdout 23,535,902. **Per-horizon earlier-model-split boundary crossings = 0**
(train/validation × 5m/30m/1h). Per-horizon valid-target support: train & validation
full at all horizons; holdout 5m 23,534,374 / 30m 23,525,986 / 1h 23,512,252 with
envelope-terminal censoring 1,528 / 9,916 / 23,650 (holdout tail only; train +
validation = 0), matching Phase 4bn-AN exactly; 0 invalid prices; 0 non-censored null
directions; censored targets excluded **without imputation**. Train-only transform
fit on the 304,816,127 train rows valid for the primary 5m target
(`subtract_train_mean_divide_by_max_train_std_epsilon`, ε = 1e-8,
`STANDARDIZE_BOOLEAN_FLAGS = False`); 2,783 non-finite feature cells excluded from the
fit across 45 features (never imputed into targets); constant columns handled by the
`max(std, ε)` denominator (no feature dropped). `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`; `test_rows_loaded = 0`; `data_committed = false`;
`frozen_v002_family_mutated = false`; `longhorizon_label_family_mutated = false`;
`ah_dataset_namespace_mutated = false`; all eight non-authorization flags `false`.

## Final AQ result state

`LONGHORIZON_ML_DATASET_BUILD_COMPLETE__LOCAL_DATASET_ARTEFACTS_WRITTEN__NO_MODEL_RUN__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## Boundary confirmations

- Read only admitted pre-v002 sources (BTCUSDT, 2024-03-01..2024-11-30) and only the
  required columns; no acquisition / endpoint / raw zip / credentials / WebSocket /
  MCP. ✅
- No v002 terminal read; sealed test untouched; `test_rows_loaded = 0`. ✅
- No AH ML-dataset / AJ baseline / AN label namespace mutation; the AH dataset output
  namespace was not even inspected (binding proven from committed feature witnesses +
  the AN manifest + per-date paired-feature-SHA cross-check). ✅
- No AH builder / AI diagnostics / AJ baseline rerun; no AN label build rerun. ✅
- Frozen v002 short-horizon family and every frozen module / manifest / gate / sidecar
  / split file / ML config unmodified; exactly one new dataset namespace created. ✅
- No ML / training / scoring / prediction / inference / calibration / confidence-tail
  / evaluation / ML verdict; no feature selection / threshold optimization / model
  selection / hyperparameter search / capacity comparison; no baseline run. ✅
- No strategy / signals / PnL / backtest / Sharpe / hit-rate / turnover / position /
  execution / paper / shadow / live / exchange-write. ✅
- No `research_eligible` flip; `flip_research_eligible(...)` never invoked. ✅
- Output namespace local + gitignored; **no data committed**;
  `.claude/scheduled_tasks.lock` not committed. ✅
- Allowed claim scope (AE §8 a/b/c) preserved and unexercised; forbidden claim scope
  (AE §8/§19) preserved; locked cost 8 bps/side · 16 bps round-trip preserved;
  long-horizon materiality remains descriptive-only. ✅

## Remaining blockers before the fixed baseline run

Building the dataset spec is **not** permission to model it. The future fixed
run-once baseline (majority / persistence / L2-logistic over `forward_direction_5m`,
with 30m/1h diagnostics), and any model scoring / prediction / calibration /
confidence-tail selection / evaluation / ML verdict, require their **own separate
future operator authorization**. All non-authorization flags remain `false`. This
phase does not decide whether the long-horizon ML arc continues.

## Remaining blockers before any strategy / PnL / backtest / live path

Absolute (Phase 4bn-AE §19). A separate future M0-style mechanism-admissibility memo
clearing M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution feasibility,
slippage/spread (aggTrades-only data cannot support — mid/book required; the
`bookticker_midprice_data_admissibility_memo` remains deferred and unauthorized),
label economic relevance, and strategy admissibility vs the retained rejections —
**plus** separate authorization for each of strategy / signals / PnL / backtest /
paper-shadow / live / exchange-write. No dataset-build result softens this boundary.

## Recommended state

**Remain paused.** The long-horizon ML dataset specification exists locally
(gitignored) with verified integrity, source binding, split/support index, and
train-only transform. Nothing downstream is authorized.

## Explicit no-successor execution statement

Phase 4bn-AQ authorizes **no** successor execution phase. It does not run or authorize
the fixed baseline run, any baseline / model / prediction / inference / calibration /
evaluation / ML verdict, feature selection, threshold optimization, model selection,
hyperparameter search, or any strategy / signals / PnL / backtest / paper-shadow /
live / exchange-write path; it does not generate the next-phase prompt or a
merge-closeout. Every retained verdict and project lock (8 bps/side · 16 bps
round-trip; the Phase 4aw `flip_research_eligible(...)` always-raises invariant —
never invoked; Phase 4bb-F sidecar policy; the Phase 4bn-AE claim-scope and
strategy/PnL/backtest/live boundary; the Phase 4bn-AP no-ML/no-successor boundary; the
AH..AP results) is preserved verbatim. Do not merge to main and do not push unless
explicitly instructed in a later prompt; do not generate a merge-closeout or the
next-phase prompt unless explicitly instructed later.
