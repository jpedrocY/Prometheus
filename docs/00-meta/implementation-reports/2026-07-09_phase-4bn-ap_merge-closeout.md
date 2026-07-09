# Phase 4bn-AP — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AP — Long-Horizon ML Baseline Preregistration / Evaluation Contract Memo.
Branch: `phase-4bn-ap/longhorizon-ml-baseline-preregistration-contract`.

## 2. Phase type

Docs-only long-horizon ML baseline preregistration / evaluation-contract memo;
**merge-only review**. No Parquet read; no AN JSON re-read; no output-namespace
mutation; no build rerun; no ML; no strategy; no successor execution authorized.

## 3. Base SHA

`4633a5ff5ddc9f418694b99990ffde8b2eacd161`
(pre-AP `main` tip; the `docs(phase-4bn-ao): finalize merge closeout shas` commit).

## 4. Pre-merge branch HEAD

`251dee47f0ff91bc41f1b7a991ba57100f2b31ec`
(`docs(phase-4bn-ap): record long-horizon ml baseline preregistration`).

## 5. Main / origin main before merge

`main == origin/main == 4633a5ff5ddc9f418694b99990ffde8b2eacd161` (verified in sync
before merge).

## 6. Summary of Phase 4bn-AP preregistration

Phase 4bn-AP pre-registered, at the design level only, a future, separately authorized
long-horizon baseline evaluation over the Phase 4bn-AN long-horizon labels: its
architecture (AH→AJ two-step), target horizons (5m primary; 30m/1h secondary
diagnostic), feature scope (the frozen 45-feature AH allowlist; labels are targets),
split/censoring/leakage treatment, frozen baseline families + constants, metric
registry, decision hierarchy, kill/continue criteria, dependence policy,
cost/materiality interpretation, future artefact requirements, and claim-scope
boundaries. It executed nothing (no row-level read, no Parquet, no model, no
evaluation) and recommended exactly one future long-horizon ML dataset-build
authorization phase.

## 7. Confirmation AP was docs-only

Confirmed. The branch adds exactly two Markdown files under
`docs/00-meta/implementation-reports/` (the preregistration memo and its closeout) and
nothing else. No source / test / script / config / manifest / gate report / sidecar /
split file / ML config / `data/` artefact was created or modified.

## 8. Confirmation no Parquet files were read

Confirmed. No built long-horizon label Parquet, no source feature/normalized Parquet,
no raw zip — during Phase 4bn-AP or this merge review.

## 9. Confirmation no AN JSON artefacts were re-read

Confirmed. No committed-report inconsistency required it; all AN facts were recovered
from the committed AN/AO reports.

## 10. Confirmation no output namespace mutation

Confirmed. The Phase 4bn-AN output namespace was not created, overwritten, deleted,
refreshed, or re-hashed; it was not touched at all.

## 11. Confirmation no build rerun

Confirmed. `scripts/phase4bn_an_build_longhorizon_labels.py` was not executed.

## 12. Confirmation no ML / training / scoring / prediction / inference

Confirmed. None occurred.

## 13. Final AP evaluation architecture

`LONGHORIZON_ML_DATASET_BUILD_THEN_FIXED_BASELINE_RUN` (AH→AJ two-step): future phase 1
= data-reading long-horizon ML dataset build (no models); future phase 2 = fixed
run-once baseline (only after phase 1, separately authorized).

## 14. Final AP target horizon decision

Primary decision target `forward_direction_5m`; secondary diagnostic targets
`forward_direction_30m` and `forward_direction_1h` (cannot upgrade a failed 5m result
unless a later separate decision memo revisits the hierarchy).

## 15. Feature scope

The existing Phase 4bn-AH 45 causal aggTrades feature allowlist only; no new features;
no feature selection; no mid/book features; no raw/price/future-derived forbidden
columns; **no long-horizon label / support / reference / censoring columns as
features** (labels are targets only).

## 16. Baseline families

Majority; persistence; L2 multinomial-logistic. Exactly three, fixed, run-once; no
model / family / hyperparameter search; no calibration training; no threshold tuning.

## 17. Persistence definition

`sign(rolling_log_return_past_window_60s)`. Horizon-matched persistence (a 5m/30m/1h
past-window return) is **rejected** because no 5m/30m/1h past-window feature exists in
the frozen 45-feature allowlist (windows asserted `1s/5s/15s/60s`) and no new feature
may be created; 60s is the longest available past-window return (closest to the long
horizons) and provides a "recent-trend-continues" floor. The exact-AJ-feature
alternative (`rolling_log_return_past_window_15s`) is recorded but not selected; the
choice is frozen and revisable only by a later separate decision memo, never after
results.

## 18. L2 frozen constants

epochs 1; batch size 8192; learning rate 0.1; L2 1e-4; gradient clip 10; seed
20260528; train-only standardization
(`subtract_train_mean_divide_by_max_train_std_epsilon`); standardization epsilon 1e-8;
`STANDARDIZE_BOOLEAN_FLAGS = False`. Confirmed verbatim from
`ml_baseline_design_v002.py`. Frozen by the AP memo; the future run must use them
verbatim.

## 19. Metric registry

The Phase 4bn-AE §13 registry per horizon (aggregate + per-month + per-date): accuracy;
balanced accuracy; macro-F1; per-class precision/recall/F1; confusion matrix; predicted
class distribution; predicted-zero rate; majority floor and persistence floor
comparisons; per-date and per-month block agreement; holdout non-reversal; log-loss;
Brier score; calibration reliability; high-confidence tail size + accuracy at ≥ 0.8;
descriptive cost-realism context only. **Forbidden:** PnL; trade count; Sharpe; trading
hit-rate; turnover; position/holding metric; any strategy metric.

## 20. Kill / continue criteria

Frozen AE §16 thresholds on the **5m primary** target (not relaxed after results):

- **`CONTINUE_ONE_BOUNDED_FOLLOWUP`** — only if all hold: L2 beats **both** the majority
  and persistence floors on validation accuracy by **≥ +2.0 pp**; macro-F1 **≥ +0.03**
  over the majority floor; balanced accuracy **≥ +1.0 pp** over the majority floor (or at
  minimum non-degraded, the nuance the AP memo records); improvement in a **majority** of
  validation date blocks **and** both validation months; holdout **does not reverse**;
  the ≥ 0.8 confidence tail beats the majority floor (diagnostic only).
- **`INVESTIGATE_AMBIGUOUS`** — mixed evidence (incl. 5m-fails-but-30m/1h-positive);
  routes to a separate docs-only decision memo; must not silently become a continue.
- **`STOP_LONGHORIZON_ML_ARC`** — failed 5m primary criteria, block concentration,
  holdout reversal, or failed information diagnostic.

## 21. Dependence policy

Block-level evidence (275 dates / 9 months); no per-row significance; no p-value over
row counts; block bootstrap **reserved-not-adopted** for the first fixed baseline
evaluation. Long-horizon overlap is heavier than 15s, so effective independence is far
below the row count.

## 22. Cost / materiality interpretation

8 bps/side · 16 bps round-trip locked cost remains **descriptive context only**. The
AN materiality shares (validation > 16 bps: 5m 34.95% / 30m 64.28% / 1h 72.72% vs 15s
2.47%) show label materiality, **not** predictive edge. No cost thresholding of the
target; no trade simulation; no PnL. A future positive baseline would remain
information-diagnostic and non-economic; aggTrades-only data cannot resolve
spread/slippage/mid-price realism; any strategy path remains behind the Phase 4bn-AE
§19 M0-style mechanism-admissibility memo.

## 23. Future artefact requirements

**Future dataset build (phase 1):** dataset manifest; per-date split index; train-only
transform stats; leakage/split/integrity proof (strict alignment, 0 boundary crossings,
0 embargo rows used); feature ↔ label source binding (AH feature SHAs + AN
`label_config_hash`); `v002_terminal_window_read = false` / `sealed_test_split_touched
= false` / `test_rows_loaded = 0` proof fields; per-Parquet `.sha256` sidecars +
inventory (Phase 4bb-F); **no model output**. **Future baseline run (phase 2):** run
manifest; frozen config; §19 metrics; per-date/per-month summaries; calibration/tail
summaries; holdout confirmation; the §20 verdict; **no strategy/PnL/backtest artefact**.
All local/gitignored; no data committed.

## 24. Final AP decision

**`RECOMMEND_LONGHORIZON_ML_DATASET_BUILD_AUTHORIZATION_MEMO_NEXT`** (option A).

## 25. Recommended future authorization

Exactly one future **long-horizon ML dataset-build authorization phase**: data-reading;
no models; bind the AH 45-feature pre-v002 source to the AN long-horizon label family
`microstructure_labels_longhorizon_aggtrades_v001` (`label_config_hash` `edaeafde…`)
over the admitted pre-v002 segment (275 dates / 400,001,695 rows); produce a compact
leakage-proof dataset spec + split index + train-only transform + source binding +
sidecars/inventory; preserve the AH compact-spec posture, the Phase 4bb-F sidecar
policy, and the Phase 4bn-L 125 GiB cap (budget preflight); v002/sealed/test excluded;
all non-authorization flags false; local/gitignored; no data committed; no model run.
The fixed baseline run remains a **further separate** authorization after this build.

## 26. Confirmation recommended dataset-build phase is not started

Confirmed. No work on it has begun; no prompt for it was generated.

## 27. Confirmation recommended dataset-build phase requires separate future operator authorization

Confirmed. It begins only under a separate future operator prompt; row-level reads
happen only under that prompt.

## 28. Confirmation fixed baseline run requires further separate authorization after the dataset build

Confirmed. Phase 2 (fixed baseline run) is a further separate authorization beyond the
dataset-build phase; the dataset-build phase authorizes no model run.

## 29. Confirmation no successor execution is authorized

Confirmed. Phase 4bn-AP and this merge authorize no successor execution phase.

## 30. Files added by AP

- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ap_longhorizon-ml-baseline-preregistration-contract.md`
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ap_closeout.md`

(This merge-closeout adds a third docs file on the branch before merge.)

## 31. Confirmation no data files were committed

Confirmed. No file under `data/microstructure/` or `data/research/` was staged or
committed; `.claude/scheduled_tasks.lock` was not committed.

## 32. Confirmation local output namespaces remain gitignored

Confirmed. `git check-ignore -v` → `.gitignore:85` (`data/microstructure/`) /
`.gitignore:88` (`data/research/`); `git ls-files data/…` → 0 tracked.

## 33. Confirmation no data files were read during merge review

Confirmed. Only `git` tracked-state checks and re-reading the committed Phase 4bn-AP
report + closeout. No source or built data Parquet, and no AN JSON, was read.

## 34. Confirmation no Parquet read during merge review

Confirmed.

## 35. Confirmation no build rerun during merge review

Confirmed.

## 36. Confirmation no output namespace mutation during merge review

Confirmed.

## 37. Confirmation no v002 terminal / sealed test / test rows

Confirmed (no data window read at all; the contract itself keeps
`test_rows_loaded = 0`, v002/sealed excluded).

## 38. Confirmation no AH/AJ/AN namespace mutation

Confirmed.

## 39. Confirmation no AH builder / AI diagnostics / AJ baseline rerun

Confirmed.

## 40. Confirmation no AJ/AI/AH/AO metrics revised or recomputed

Confirmed. All prior-phase figures quoted verbatim.

## 41. Confirmation no ML / training / scoring / prediction / inference

Confirmed.

## 42. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search

Confirmed.

## 43. Confirmation no cost-aware / magnitude / deadband label adopted

Confirmed.

## 44. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write

Confirmed.

## 45. Confirmation no eligibility / authorization / manifest / gate / sidecar flag transition

Confirmed. No `research_eligible` flip; no `ml_authorized` / `diagnostics_authorized` /
strategy / backtest / live authorization transition; no published manifest / gate
report / sidecar / split file mutation. The Phase 4aw `flip_research_eligible(...)`
always-raises invariant was preserved and never invoked.

## 46. Validation commands and results from merge review

- `git rev-parse main` / `origin/main` → both
  `4633a5ff5ddc9f418694b99990ffde8b2eacd161`.
- `git rev-parse phase-4bn-ap/…` → `251dee47f0ff91bc41f1b7a991ba57100f2b31ec`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`; `git diff --name-only`
  (tracked) → empty (no working-tree modifications).
- `git diff --check` → clean.
- `git diff --name-status main..branch` → two added AP docs; no modifications to any
  existing tracked file; no source/test/script/manifest/gate/split/ML-config change.
- `git ls-tree -r --name-only branch -- data/microstructure/` and `-- data/research/`
  → empty.
- `git ls-files data/microstructure/` / `data/research/` → 0 tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/` →
  `.gitignore:88`.
- No Parquet read; no AN JSON re-read; no build rerun; no namespace mutation; no
  pytest/ruff/mypy required (docs-only).

(These reflect the pre-merge review; the merge-closeout commit adds this docs file.
Post-merge and post-finalization command outputs are reproduced in the final operator
report.)

## 47. Git status before merge

Only `?? .claude/scheduled_tasks.lock` untracked; no `data/` file staged; branch tip
`251dee47…` (+ the merge-closeout commit added on the branch before merge). The
~11.12 GiB AN label layer under `data/research/…` remains gitignored, untracked, and
unmutated.

## 48. Merge method to be used

Non-fast-forward merge (`git merge --no-ff`) of
`phase-4bn-ap/longhorizon-ml-baseline-preregistration-contract` into `main`. No squash;
no rebase; no `.claude/scheduled_tasks.lock`; no data outputs.

## 49. Final merge commit SHA

`<PENDING_MERGE_COMMIT_SHA>` — to be resolved by the post-merge
`docs(phase-4bn-ap): finalize merge closeout shas` commit on `main`
(`docs(phase-4bn-ap): merge long-horizon ml baseline preregistration`; `--no-ff`, 3
docs files added: the two AP docs + this merge-closeout).

## 50. Final main / origin main SHA

`<PENDING_FINAL_MAIN_SHA>` — equal to the SHA-finalization commit
(`docs(phase-4bn-ap): finalize merge closeout shas`), the resulting `main` /
`origin/main` tip after push; resolved in the finalize commit and reproduced in the
final operator report.

## 51. Result state

`LONGHORIZON_ML_BASELINE_PREREGISTRATION_MERGED_TO_MAIN__DATASET_BUILD_AUTHORIZATION_MEMO_RECOMMENDED__NO_ML__NO_PARQUET_READ__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 52. Recommended state

**Remain paused.**

## 53. Explicit no-successor execution statement

The recommended dataset-build phase, any row-level read, any dataset build, any ML /
baseline run, any evaluation / diagnostics over the built labels, any further label
build / read / rerun, any strategy / signals / PnL / backtest / paper / shadow / live /
exchange-write, and any other successor phase require **separate future operator
authorization**. Phase 4bn-AP and this merge generate **no** successor prompt and
authorize **no** successor execution phase.

## 54. Remaining blockers before row-level read / dataset build

A separate future operator authorization for the long-horizon ML dataset-build phase; a
budget preflight; data-reading boundaries (admitted pre-v002 sources only; v002/sealed/
test excluded); **no model run** in that phase.

## 55. Remaining blockers before ML / baseline run

A successful dataset-build phase first; then a **further** separate authorization for
the fixed baseline run; the frozen AP §18 constants and §20 verdict criteria preserved
verbatim. All non-authorization flags remain false.

## 56. Remaining blockers before strategy / PnL / backtest / live

Absolute (Phase 4bn-AE §19). A separate future **M0-style mechanism-admissibility memo**
clearing M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution feasibility, and
slippage/spread — which aggTrades-only data cannot support: mid/book/spread/slippage
realism remains **unresolved** (the `bookticker_midprice_data_admissibility_memo`
remains deferred/unauthorized) — plus label economic relevance, strategy admissibility
vs the retained rejections and the M0 §7.D microstructure-lane `NOT_RECOMMENDED_NOW`
posture, the Phase 4al no-rescue constraints, and separate authorization for each of
strategy / signals / PnL / backtest / paper-shadow / live / exchange-write.

## 57. Preserved project locks and verdicts

Preserved verbatim: 8 bps per side / 16 bps round-trip; the Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F
canonical sidecar policy; Phase 4bn-AE claim-scope and strategy/PnL/backtest/live
boundary; Phase 4bn-AH proof and dataset namespace posture; Phase 4bn-AI descriptive
no-model boundary; Phase 4bn-AJ fixed baseline verdict and no-strategy boundary; Phase
4bn-AK single-follow-up selection; Phase 4bn-AL label-memo recommendation and
no-build/no-data-read boundary; Phase 4bn-AM label-contract/spec recommendation and
no-build/no-data-read boundary; Phase 4bn-AN build result and
no-ML/no-strategy/no-successor boundary; Phase 4bn-AO diagnostics result and
no-ML/no-Parquet/no-successor boundary; Phase 4bn-AP preregistration result and
no-ML/no-Parquet/no-successor boundary. Plus the retained strategy-research locks (H0 /
R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1) and the Phase 4ak M0
twelve-clause gate. Phase 4 canonical remains unauthorized.

## 58. Manifest / eligibility state preservation

- No `research_eligible` flip.
- No `ml_authorized` transition.
- No `diagnostics_authorized` transition.
- No strategy / backtest / live authorization transition.
- No published manifest / gate report / sidecar / split file mutation.
