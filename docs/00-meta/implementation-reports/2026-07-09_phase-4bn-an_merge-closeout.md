# Phase 4bn-AN — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AN — Longer-Horizon Label Build Implementation + Single Controlled Run.
Branch: `phase-4bn-an/longer-horizon-label-build-single-run`.

## 2. Phase type

Code + tests + **single controlled data build**; **merge-only review**. The build
was **not** rerun during this review; the local output namespace was **not**
mutated; no ML / diagnostics / strategy; no successor execution authorized.

## 3. Base SHA

`ea8c6d9f8bfb116c6cfc45486be2836e77ee4a59`
(pre-AN `main` tip; the `docs(phase-4bn-am): finalize merge closeout shas` commit).

## 4. Pre-merge branch HEAD

`0be4f65da2648fc241347532b0eb5cc989cc3818`. The branch carries two commits: the
Phase 4bn-AN implementation `f14f2c6398f79309cd74b843151e59f3d940c56e`
(`feat(phase-4bn-an): build long-horizon label artefacts`) and a merge-review
tidy `0be4f65…` (`chore(phase-4bn-an): make sibling-family assert mypy-clean` — a
one-line change replacing a static-literal `!=` assert with a `str(...)`-based
runtime tripwire so mypy reports **0** errors on the new modules; **no** behavioral
or artefact change, the built labels and `label_config_hash` are unaffected). The
branch-vs-main diff remains exactly the six intended files.

## 5. Main / origin main before merge

`main == origin/main == ea8c6d9f8bfb116c6cfc45486be2836e77ee4a59` (verified in sync
before merge).

## 6. Summary of Phase 4bn-AN implementation

Phase 4bn-AN implemented the Phase 4bn-AM-recommended **new sibling** longer-horizon
label family `microstructure_labels_longhorizon_aggtrades_v001` (horizons 5m / 30m /
1h) as three new modules — a schema module, a per-day kernel (a faithful
transcription of the frozen v002 label kernel to the new horizon set, reusing the
frozen `load_normalized_day_ref`), and a build orchestrator that **reuses the frozen
Phase 4bn-W source-verification + preflight verbatim** — plus a 15-test suite. It
then ran the build **exactly once** over the admitted pre-v002 aggTrades segment,
writing a local/gitignored research namespace and the AM-required descriptive
continuous-return / cost-clearing summaries. The frozen v002 short-horizon family
was not touched.

## 7. Summary of Phase 4bn-AN local build output

275 per-day label Parquet + 275 `.sha256` sidecars + 5 JSON artefacts (manifest,
leakage/split/censoring proof, continuous-return/cost summary, build run record,
sidecar inventory), each JSON with a paired `.sha256`. ~11.12 GiB. All under the
gitignored `data/research/…` namespace; **nothing committed**.

## 8. Confirmation AN implemented a new sibling family

Confirmed. `microstructure_labels_longhorizon_aggtrades_v001` — a new sibling of the
frozen `microstructure_labels_aggtrades_v001`.

## 9. Confirmation frozen v002 family was not mutated

Confirmed. No frozen module (`labels_schema_v002.py`, `labels_compute_v002.py`,
`labels_io.py`, `pre_v002_split_policy.py`, the W orchestrator) and no published
manifest / gate report / sidecar / split file / ML config was modified. The branch
diff is six **added** files only (`git diff --name-status`); the frozen v002 horizon
set stays asserted `1s/5s/15s/60s`.

## 10. Output namespace

`data/research/microstructure/labels/microstructure_labels_longhorizon_aggtrades_v001_pre_v002/`
(gitignored via `.gitignore:88`).

## 11. Output artefact inventory

275 Parquet; 275 Parquet `.sha256` sidecars; 5 JSON artefacts; 5 JSON `.sha256`
sidecars.

## 12. Label config hash

`edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`.

## 13. Build row / partition counts

275 partitions (2024-03-01..2024-11-30); 400,001,695 rows.

## 14. Split counts

train 304,816,127 (214 dates); validation 68,578,296 (45 dates); holdout
23,535,860 (14 dates); embargo 2 dates.

## 15. Censoring summary

Per-horizon envelope-terminal censored rows: 5m = 1,528; 30m = 9,916; 1h = 23,650
(holdout tail only; train + validation have 0 censoring). Invalid prices = 0. No
NaN/Inf in non-null numeric outputs.

## 16. Leakage / split proof summary

Per-horizon earlier-model-split boundary-crossing rows = **0** for every
(train, validation) × (5m, 30m, 1h). `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`; `test_rows_loaded = 0`;
`frozen_v002_family_mutated = false`; `data_committed = false`; all eight
non-authorization flags `false`; forbidden-substring scan clean; embargo rows used
in model splits = 0; `max_horizon_ms` (3,600,000) < `one_day_purge_ms`
(86,400,000).

## 17. Descriptive cost-clearing summary

Validation share clearing 16 bps round-trip: 5m ≈ 34.95%; 30m ≈ 64.28%; 1h ≈
72.72%. Phase 4bn-AJ 15s reference = 2.47%. (Median absolute move ≈ 10–11 bps at
5m, 24–25 bps at 30m, 33–34 bps at 1h.)

## 18. Binding interpretation

These figures are **descriptive raw last-trade-price move-distribution
label-materiality diagnostics only**. They are **not** evidence of tradability;
profitability; economic edge; PnL; strategy viability; backtest validity; or
execution viability. aggTrades-only data cannot express spread/slippage or
mid-price execution realism. Larger raw moves at longer horizons are a property of
the return distribution, **not** a demonstration that any move is predictable or
capturable. The locked cost reference remains 8 bps/side · 16 bps round-trip.

## 19. Files added by AN

- `src/prometheus/research/microstructure/longhorizon_labels_schema_v001.py`
- `src/prometheus/research/microstructure/longhorizon_labels_compute_v001.py`
- `scripts/phase4bn_an_build_longhorizon_labels.py`
- `tests/research/microstructure/test_phase4bn_an_longhorizon_labels.py`
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-an_longer-horizon-label-build-single-run.md`
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-an_closeout.md`

(This merge-closeout adds a seventh docs file on the branch before merge.)

## 20. Confirmation no data files were committed

Confirmed. No file under `data/microstructure/` or `data/research/` was staged or
committed; `.claude/scheduled_tasks.lock` was not committed.

## 21. Confirmation local output namespace is gitignored

Confirmed. `git check-ignore -v` → `.gitignore:88` for the AN output namespace;
`git ls-files data/research/` → 0 tracked.

## 22. Confirmation no data files were read during merge review

Confirmed. The merge review used only `git status` / `git diff` / `git ls-tree` /
`git ls-files` / `git check-ignore` tracked-state checks and re-read the committed
Phase 4bn-AN report + closeout. No built Parquet label output was read for new
analysis; no source data Parquet was read.

## 23. Confirmation the build was not rerun during merge review

Confirmed. `scripts/phase4bn_an_build_longhorizon_labels.py` was **not** executed
during this review.

## 24. Confirmation local output namespace was not mutated during merge review

Confirmed. No file under the AN output namespace was created, overwritten, deleted,
refreshed, or rehashed en masse; the review preserved the build.

## 25. Confirmation no v002 terminal / sealed test / test rows

Confirmed. No v002 terminal window, sealed-test date, or test row was read;
`test_rows_loaded = 0`.

## 26. Confirmation no AH/AJ namespace mutation

Confirmed. The Phase 4bn-AH ML-dataset namespace and Phase 4bn-AJ baseline namespace
were not read, mutated, refreshed, created, or deleted.

## 27. Confirmation no AH builder / AI diagnostics / AJ baseline rerun

Confirmed. None was executed.

## 28. Confirmation no AJ/AI/AH metrics revised or recomputed

Confirmed. All prior-phase figures are quoted verbatim; none recomputed.

## 29. Confirmation no ML / training / scoring / prediction / inference

Confirmed. None occurred.

## 30. Confirmation no extra diagnostics beyond build-required descriptive summaries

Confirmed. Only the AM-required descriptive continuous-return / cost-clearing /
class-balance summaries were produced.

## 31. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search

Confirmed. None occurred.

## 32. Confirmation no cost-aware / magnitude / deadband label adopted

Confirmed. Strict-sign zero-threshold direction only; no deadband / bp / cost /
learned / optimised / magnitude / neutral-band label.

## 33. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write

Confirmed. None occurred.

## 34. Confirmation no eligibility / authorization / manifest / gate / sidecar flag transition

Confirmed. No `research_eligible` flip; no `ml_authorized` / `diagnostics_authorized`
/ strategy / backtest / live authorization transition; no published manifest / gate
report / sidecar / split file mutation. The Phase 4aw `flip_research_eligible(...)`
always-raises invariant was preserved and never invoked.

## 35. Validation commands and results from merge review

- `git rev-parse main` / `origin/main` → both
  `ea8c6d9f8bfb116c6cfc45486be2836e77ee4a59`.
- `git rev-parse phase-4bn-an/…` → `0be4f65…` (impl `f14f2c6…` + mypy tidy).
- `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check` → clean.
- `git diff --name-status main..branch` → six added files (2 src, 1 script, 1 test,
  2 docs); no modifications to any existing tracked file.
- `git ls-tree -r --name-only branch -- data/microstructure/` and `-- data/research/`
  → empty.
- `git ls-files data/microstructure/` / `data/research/` → 0 tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/` →
  `.gitignore:88`.
- `pytest test_phase4bn_an_longhorizon_labels.py` → **15 passed**.
- `pytest test_labels_schema_v002 + test_labels_compute_v002 +
  test_phase4bn_aa_pre_v002_split_policy` → **108 passed** (no regression).
- `ruff check` (2 new src modules + orchestrator + test) → **All checks passed**.
- `mypy` (2 new src modules) → **0** errors attributed to the new modules (repo's
  pre-existing baseline errors remain only in unrelated frozen feature modules).
- The build was **not** run; the AN output namespace was **not** mutated.

(These reflect the pre-merge review; the merge-closeout commit adds this docs file.
Post-merge and post-finalization command outputs are reproduced in the final
operator report.)

## 36. Git status before merge

Only `?? .claude/scheduled_tasks.lock` untracked; no `data/` file staged; branch tip
`0be4f65…` (+ the merge-closeout commit added on the branch before merge). The
~11.12 GiB built label layer under `data/research/…` remains gitignored and
untracked.

## 37. Merge method to be used

Non-fast-forward merge (`git merge --no-ff`) of
`phase-4bn-an/longer-horizon-label-build-single-run` into `main`. No squash; no
rebase; no `.claude/scheduled_tasks.lock`; no data outputs.

## 38. Final merge commit SHA

`2cd9dddda4e1b382180f10459264e5da918739e0`
(`feat(phase-4bn-an): merge long-horizon label build`; `--no-ff`, 7 docs/code/test
files added net vs base: the six AN files + this merge-closeout).

## 39. Final main / origin main SHA

Equal to this SHA-finalization commit (`docs(phase-4bn-an): finalize merge closeout
shas`), the resulting `main` / `origin/main` tip after push; the literal value is
reproduced in the final operator report (a commit cannot embed its own SHA).

## 40. Result state

`LONGER_HORIZON_LABEL_BUILD_MERGED_TO_MAIN__LOCAL_LABEL_ARTEFACTS_PRESERVED__NO_ML__NO_STRATEGY__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 41. Recommended state

**Remain paused.**

## 42. Explicit no-successor execution statement

Any ML / diagnostics over the built labels, any further label build / read / rerun,
any strategy / signals / PnL / backtest / paper / shadow / live / exchange-write, and
any other successor phase require **separate future operator authorization**. Phase
4bn-AN and this merge authorize **no** successor execution phase and do **not**
generate any successor prompt.

## 43. Remaining blockers before ML / diagnostics over the built labels

A separate future operator authorization; a specific evaluation contract; no
threshold / model / feature selection unless separately authorized. All
non-authorization flags remain `false`.

## 44. Remaining blockers before strategy / PnL / backtest / live

Absolute (Phase 4bn-AE §19). A separate future **M0-style mechanism-admissibility
memo** clearing M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution
feasibility, and slippage/spread — which aggTrades-only data cannot support:
mid/book/spread/slippage realism is **unresolved** (the
`bookticker_midprice_data_admissibility_memo` remains deferred and unauthorized) —
plus label economic relevance, strategy admissibility vs the retained rejections and
the M0 §7.D microstructure-lane `NOT_RECOMMENDED_NOW` posture, the Phase 4al
no-rescue constraints, and separate authorization for each of strategy / signals /
PnL / backtest / paper-shadow / live / exchange-write.

## 45. Preserved project locks and verdicts

Preserved verbatim: 8 bps per side / 16 bps round-trip; the Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F
canonical sidecar policy; Phase 4bn-AE claim-scope and strategy/PnL/backtest/live
boundary; Phase 4bn-AH proof and dataset namespace posture; Phase 4bn-AI descriptive
no-model boundary; Phase 4bn-AJ fixed baseline verdict and no-strategy boundary;
Phase 4bn-AK single-follow-up selection; Phase 4bn-AL label-memo recommendation and
no-build/no-data-read boundary; Phase 4bn-AM label-contract/spec recommendation and
no-build/no-data-read boundary; Phase 4bn-AN build result and
no-ML/no-strategy/no-successor boundary. Plus the retained strategy-research locks
(H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1) and the
Phase 4ak M0 twelve-clause gate. Phase 4 canonical remains unauthorized.

## 46. Manifest / eligibility state preservation

- No `research_eligible` flip.
- No `ml_authorized` transition.
- No `diagnostics_authorized` transition.
- No strategy / backtest / live authorization transition.
- No published manifest / gate report / sidecar / split file mutation.
