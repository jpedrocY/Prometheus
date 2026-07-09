# Phase 4bn-AO — Merge Closeout

## 1. Phase name and branch

Phase 4bn-AO — Longer-Horizon Label Descriptive Diagnostics, No Models.
Branch: `phase-4bn-ao/longhorizon-label-descriptive-diagnostics-no-models`.

## 2. Phase type

Docs + **local-JSON-artefact-only** descriptive diagnostics; **merge-only review**.
No Parquet read; no build rerun; no output-namespace mutation; no ML; no strategy; no
successor execution authorized.

## 3. Base SHA

`7e70b13a6753f7f77f60051182f259831a78b69e`
(pre-AO `main` tip; the `docs(phase-4bn-an): finalize merge closeout shas` commit).

## 4. Pre-merge branch HEAD

`916f6c18be65abdf14fab57a9d5021ebc092ffad`
(`docs(phase-4bn-ao): record long-horizon label diagnostics`).

## 5. Main / origin main before merge

`main == origin/main == 7e70b13a6753f7f77f60051182f259831a78b69e` (verified in sync
before merge).

## 6. Summary of Phase 4bn-AO diagnostics

Phase 4bn-AO inspected the five Phase 4bn-AN `_manifest/*.json` artefacts (+ their
`.sha256` sidecars) and produced a no-model descriptive diagnostics + readiness memo:
it confirmed the built long-horizon label layer is integrity-clean and complete,
summarized its leakage/scope invariants and its descriptive materiality (longer-horizon
raw moves clear the locked cost far more often than 15s), assessed longer-horizon
risks, and recommended exactly one **future, separately authorized** docs-only ML
baseline preregistration/evaluation-contract memo. It read no Parquet, ran no model,
mutated nothing, and authorized no successor.

## 7. Confirmation AO inspected only the five AN JSON artefacts and sidecars

Confirmed. Only `manifest.json`, `leakage_split_censoring_proof.json`,
`continuous_return_cost_summary.json`, `build_run_record.json`, and
`sidecar_inventory.json` (+ their five `.sha256` sidecars) under the AN `_manifest/`
were opened, plus committed docs/source and `git` tracked-state checks.

## 8. Confirmation no Parquet files were read

Confirmed. No built per-day label Parquet, no source feature/normalized Parquet, no
raw zip was read — during Phase 4bn-AO or this merge review.

## 9. Confirmation all five JSON sidecars verified

Confirmed. Each of the five AN JSON artefacts' body SHA256 matches its `.sha256`
sidecar (re-verified in this merge review).

## 10. Confirmation no AN build rerun

Confirmed. `scripts/phase4bn_an_build_longhorizon_labels.py` was not executed.

## 11. Confirmation no AN output namespace mutation

Confirmed. Nothing under the AN output namespace was created, overwritten, deleted,
refreshed, or re-hashed en masse; the JSON artefacts were opened read-only. The
namespace remains intact (275 Parquet + 275 sidecars + 5 JSON artefacts + 5 sidecars).

## 12. Artefact-integrity summary

- Family `microstructure_labels_longhorizon_aggtrades_v001`; sibling of the frozen
  `microstructure_labels_aggtrades_v001`.
- `label_config_hash` `edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`.
- 275 distinct dates; 400,001,695 total rows; 275 sidecar-inventory entries.
- All eight non-authorization flags `false`; `data_committed = false`;
  `frozen_v002_family_mutated = false`; all five JSON sidecars valid.

## 13. Benign row-count reconciliation

AN per-day inventory holdout = **23,535,902** rows (labels keep all feature rows); AN
§26 cited **23,535,860** — the Phase 4bn-AH ML-dataset holdout *kept*-count (42 fewer,
AH's own dataset-build drop). A 42-row citation nuance only; the AN totals (train
304,816,127 + embargo 3,071,370 + validation 68,578,296 + holdout 23,535,902) sum
**exactly to 400,001,695**. No build defect.

## 14. Leakage / scope summary

Per-horizon earlier-model-split boundary crossings **0** (train/validation × 5m/30m/1h);
`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`test_rows_loaded = 0`; 1-day embargo (86,400 s) > 1h max horizon (3,600 s); invalid
prices 0; no NaN/Inf; no AH/AJ/source mutation.

## 15. Descriptive materiality summary

Validation share `|move| > 16 bps`: 5m **34.95%**; 30m **64.28%**; 1h **72.72%**.
Phase 4bn-AJ 15s reference: **2.47%**. Median absolute move: 15s ~2.5 bps → 5m ~10–11
bps → 30m ~24–25 bps → 1h ~33–34 bps. Monotone in horizon and stable across
train/validation/holdout blocks.

## 16. Direction / class-balance summary

Near-binary `forward_direction_H`; the exactly-flat (0) class shrinks with horizon;
a mild horizon-growing up-skew (validation +1 class ~51%→~53.5%). A future baseline's
majority floor is modestly above 50% and must be accounted for (majority + persistence
floors).

## 17. Longer-horizon risk summary

Materiality does not imply predictability; likely feature-target signal decay at longer
horizons (short-memory features); heavier overlap / lower effective independence;
regime narrowness (late-2024 validation/holdout); 30m/1h materially large but least
obviously predictable; aggTrades-only limitation (no spread/slippage/mid realism);
up-skew requires majority/persistence floors; censoring small but horizon-growing.

## 18. Binding interpretation

The materiality figures are **descriptive raw last-trade-price move-distribution
label-materiality diagnostics only**. They are **not** predictive edge; not
tradability; not profitability; not PnL; not strategy viability; not backtest validity;
not execution viability. aggTrades-only data cannot express spread/slippage or
mid-price execution realism. The locked cost reference remains 8 bps/side · 16 bps
round-trip; the §19 M0 gate is unsoftened.

## 19. Final AO decision

**`RECOMMEND_LONGHORIZON_ML_BASELINE_PREREGISTRATION_MEMO_NEXT`.**

## 20. Recommended future preregistration / evaluation-contract memo

Exactly one future **docs-only** memo, deciding: target horizons (**5m primary**;
**30m/1h secondary diagnostic**); fixed run-once baselines (**majority / persistence /
L2-logistic with frozen hyperparameters**); the existing chrono split + 1-day embargo;
block-level dependence evidence (275 dates / 9 months; no per-row significance); the
Phase 4bn-AE §13 metric registry (accuracy / balanced-accuracy / macro-F1;
calibration/confidence-tail; comparison vs **both** majority and persistence floors);
pre-registered kill/continue criteria; and the absolute no-strategy/PnL/backtest/live
boundary. The evaluation itself (row-level label+feature reads or a long-horizon ML
dataset build) requires a **further separate authorization** after the memo.

## 21. Confirmation the recommended future memo is not started

Confirmed. No work on the recommended preregistration memo has begun; no prompt for it
was generated.

## 22. Confirmation the recommended future memo requires separate future operator authorization

Confirmed. It is docs-only and begins only under a separate future operator prompt.

## 23. Confirmation any evaluation / row-level read / dataset build / ML / diagnostics requires separate future authorization beyond the memo

Confirmed. The preregistration memo does not authorize evaluation; any row-level read
of the built labels/features, any long-horizon ML dataset build, and any ML /
diagnostics require their **own further** separate operator authorization (AH→AJ
pattern).

## 24. Files added by AO

- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ao_longhorizon-label-descriptive-diagnostics-no-models.md`
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ao_closeout.md`

(This merge-closeout adds a third docs file on the branch before merge.)

## 25. Confirmation no data files were committed

Confirmed. No file under `data/microstructure/` or `data/research/` was staged or
committed; `.claude/scheduled_tasks.lock` was not committed.

## 26. Confirmation local output namespace remains gitignored

Confirmed. `git check-ignore -v` → `.gitignore:88` for the AN output namespace;
`git ls-files data/research/` → 0 tracked.

## 27. Confirmation no data files were read during merge review

Confirmed. The merge review used only `git` tracked-state checks, re-read the committed
Phase 4bn-AO report + closeout, and re-verified the five AN JSON artefact sidecars. No
source or built data Parquet was read.

## 28. Confirmation no Parquet read during merge review

Confirmed.

## 29. Confirmation no build rerun during merge review

Confirmed.

## 30. Confirmation no output namespace mutation during merge review

Confirmed.

## 31. Confirmation no v002 terminal / sealed test / test rows

Confirmed (`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`test_rows_loaded = 0`; the review read no data window at all).

## 32. Confirmation no AH/AJ namespace mutation

Confirmed.

## 33. Confirmation no AH builder / AI diagnostics / AJ baseline rerun

Confirmed.

## 34. Confirmation no AJ/AI/AH metrics revised or recomputed

Confirmed. All prior-phase figures quoted verbatim.

## 35. Confirmation no ML / training / scoring / prediction / inference

Confirmed.

## 36. Confirmation no feature selection / threshold optimization / model selection / hyperparameter search

Confirmed.

## 37. Confirmation no cost-aware / magnitude / deadband label adopted

Confirmed.

## 38. Confirmation no strategy / signals / PnL / backtest / paper / shadow / live / exchange-write

Confirmed.

## 39. Confirmation no eligibility / authorization / manifest / gate / sidecar flag transition

Confirmed. No `research_eligible` flip; no `ml_authorized` / `diagnostics_authorized`
/ strategy / backtest / live authorization transition; no published manifest / gate
report / sidecar / split file mutation. The Phase 4aw `flip_research_eligible(...)`
always-raises invariant was preserved and never invoked.

## 40. Validation commands and results from merge review

- `git rev-parse main` / `origin/main` → both
  `7e70b13a6753f7f77f60051182f259831a78b69e`.
- `git rev-parse phase-4bn-ao/…` → `916f6c18be65abdf14fab57a9d5021ebc092ffad`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`; `git diff --name-only`
  (tracked) → empty (no working-tree modifications).
- `git diff --check` → clean.
- `git diff --name-status main..branch` → two added AO docs; no modifications to any
  existing tracked file; no source/test/script/manifest/gate/split change.
- `git ls-tree -r --name-only branch -- data/microstructure/` and `-- data/research/`
  → empty.
- `git ls-files data/microstructure/` / `data/research/` → 0 tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/` →
  `.gitignore:88`.
- Re-verified the five AN JSON artefact sidecars (body SHA256 == `.sha256`): all OK.
- No Parquet read; no build rerun; no namespace mutation; no pytest/ruff/mypy required
  (docs-only).

(These reflect the pre-merge review; the merge-closeout commit adds this docs file.
Post-merge and post-finalization command outputs are reproduced in the final operator
report.)

## 41. Git status before merge

Only `?? .claude/scheduled_tasks.lock` untracked; no `data/` file staged; branch tip
`916f6c18…` (+ the merge-closeout commit added on the branch before merge). The
~11.12 GiB AN label layer under `data/research/…` remains gitignored, untracked, and
unmutated.

## 42. Merge method to be used

Non-fast-forward merge (`git merge --no-ff`) of
`phase-4bn-ao/longhorizon-label-descriptive-diagnostics-no-models` into `main`. No
squash; no rebase; no `.claude/scheduled_tasks.lock`; no data outputs.

## 43. Final merge commit SHA

`<PENDING_MERGE_COMMIT_SHA>` — to be resolved by the post-merge
`docs(phase-4bn-ao): finalize merge closeout shas` commit on `main`
(`docs(phase-4bn-ao): merge long-horizon label diagnostics`; `--no-ff`, 3 docs files
added: the two AO docs + this merge-closeout).

## 44. Final main / origin main SHA

`<PENDING_FINAL_MAIN_SHA>` — equal to the SHA-finalization commit
(`docs(phase-4bn-ao): finalize merge closeout shas`), the resulting `main` /
`origin/main` tip after push; resolved in the finalize commit and reproduced in the
final operator report.

## 45. Result state

`LONGHORIZON_LABEL_DIAGNOSTICS_MERGED_TO_MAIN__ML_BASELINE_PREREGISTRATION_MEMO_RECOMMENDED__NO_ML__NO_PARQUET_READ__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 46. Recommended state

**Remain paused.**

## 47. Explicit no-successor execution statement

The recommended preregistration memo, any evaluation, any row-level read, any ML /
diagnostics over the built labels, any further label build / read / rerun, any strategy
/ signals / PnL / backtest / paper / shadow / live / exchange-write, and any other
successor phase require **separate future operator authorization**. Phase 4bn-AO and
this merge authorize **no** successor execution phase and generate **no** successor
prompt.

## 48. Remaining blockers before ML / diagnostics over the built labels

A separate future operator authorization; the recommended docs-only preregistration /
evaluation-contract memo (itself separately prompted); and, beyond that memo, a further
separate authorization for the actual row-level evaluation. All non-authorization flags
remain `false`.

## 49. Remaining blockers before strategy / PnL / backtest / live

Absolute (Phase 4bn-AE §19). A separate future **M0-style mechanism-admissibility memo**
clearing M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution feasibility, and
slippage/spread — which aggTrades-only data cannot support: mid/book/spread/slippage
realism remains **unresolved** (the `bookticker_midprice_data_admissibility_memo`
remains deferred/unauthorized) — plus label economic relevance, strategy admissibility
vs the retained rejections and the M0 §7.D microstructure-lane `NOT_RECOMMENDED_NOW`
posture, the Phase 4al no-rescue constraints, and separate authorization for each of
strategy / signals / PnL / backtest / paper-shadow / live / exchange-write.

## 50. Preserved project locks and verdicts

Preserved verbatim: 8 bps per side / 16 bps round-trip; the Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F
canonical sidecar policy; Phase 4bn-AE claim-scope and strategy/PnL/backtest/live
boundary; Phase 4bn-AH proof and dataset namespace posture; Phase 4bn-AI descriptive
no-model boundary; Phase 4bn-AJ fixed baseline verdict and no-strategy boundary; Phase
4bn-AK single-follow-up selection; Phase 4bn-AL label-memo recommendation and
no-build/no-data-read boundary; Phase 4bn-AM label-contract/spec recommendation and
no-build/no-data-read boundary; Phase 4bn-AN build result and
no-ML/no-strategy/no-successor boundary; Phase 4bn-AO diagnostics result and
no-ML/no-Parquet/no-successor boundary. Plus the retained strategy-research locks (H0 /
R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1) and the Phase 4ak M0
twelve-clause gate. Phase 4 canonical remains unauthorized.

## 51. Manifest / eligibility state preservation

- No `research_eligible` flip.
- No `ml_authorized` transition.
- No `diagnostics_authorized` transition.
- No strategy / backtest / live authorization transition.
- No published manifest / gate report / sidecar / split file mutation.
