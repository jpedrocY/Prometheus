# Phase 4bn-AO — Closeout

## Branch

`phase-4bn-ao/longhorizon-label-descriptive-diagnostics-no-models`

## Base SHA

`7e70b13a6753f7f77f60051182f259831a78b69e`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AN merge
closeout.)

## Phase type

Docs + **local-JSON-artefact-only** descriptive diagnostics memo (no models). Reads
only the five Phase 4bn-AN `_manifest/*.json` artefacts (+ sidecars); no Parquet read;
no output-namespace mutation; no build rerun; no ML; no strategy; no successor
execution authorized.

## Files created / modified

Created (committed — docs only):

- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ao_longhorizon-label-descriptive-diagnostics-no-models.md`
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-ao_closeout.md` (this file)

No source / test / script / config / manifest / gate / sidecar / split / ML-config /
`data/` artefact created or modified. `current-project-state.md` left unchanged
(report §31).

## Local JSON artefacts inspected

Under
`data/research/microstructure/labels/microstructure_labels_longhorizon_aggtrades_v001_pre_v002/_manifest/`:
`manifest.json`, `leakage_split_censoring_proof.json`,
`continuous_return_cost_summary.json`, `build_run_record.json`,
`sidecar_inventory.json` — plus their five `.sha256` sidecars (all verified).

## Validation commands

- `git rev-parse main`/`origin/main`/`HEAD` (pre-branch) → all
  `7e70b13a6753f7f77f60051182f259831a78b69e`.
- `git status --short` (pre-branch) → only `?? .claude/scheduled_tasks.lock`.
- Verified the 5 AN JSON sidecars (body SHA256 == `.sha256`): all OK.
- `git ls-files data/microstructure/` / `data/research/` → 0 tracked.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `data/research/` →
  `.gitignore:88`.
- `git diff --check` → clean; `git diff --name-status main..HEAD` (after commit) → only
  the two Phase 4bn-AO docs.
- No Parquet read; no namespace mutation; no build rerun; no pytest/ruff/mypy required
  (docs-only).

## Concise diagnostics outcome

The Phase 4bn-AN long-horizon label layer is **integrity-clean and complete**: family
`microstructure_labels_longhorizon_aggtrades_v001`, `label_config_hash` `edaeafde…`,
275/275 distinct dates, `Σ row_count = 400,001,695`, 275 sidecar-inventory entries, all
five JSON sidecars verify, all non-authorization flags `false`, `data_committed =
false`, `frozen_v002_family_mutated = false`. Leakage-safe: per-horizon earlier-model-
split boundary crossings **0**; `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`; `test_rows_loaded = 0`; `max_horizon (1h)` < 1-day
embargo. (Minor benign reconciliation: AN inventory holdout = 23,535,902 rows — labels
keep all feature rows — vs the AH ML-dataset kept-count 23,535,860 cited in AN §26, a
42-row citation nuance; the AN totals sum exactly to 400,001,695.)

**Descriptive materiality (label-diagnostic only, not predictability):** validation
share `|move| > 16 bps` = **5m 34.95% / 30m 64.28% / 1h 72.72%** vs **15s 2.47%** (AJ);
median move rises 15s ~2.5 bps → 5m ~10–11 → 30m ~24–25 → 1h ~33–34 bps; stable across
train/validation/holdout; near-binary direction with a shrinking flat class and a mild
horizon-growing up-skew (majority floor modestly above 50%). Longer horizons resolve the
15s economic-thinness limitation **at the label-materiality level only** — larger raw
moves are not predictive edge and aggTrades-only data cannot express spread/slippage/mid.

## Final AO decision

**`RECOMMEND_LONGHORIZON_ML_BASELINE_PREREGISTRATION_MEMO_NEXT`.**

The labels are a sound substrate and the now-well-posed open question — does directional
*information* survive at the horizons where cost is materially clearable? — warrants a
fixed, pre-registered, no-strategy baseline **evaluation contract** (mirroring Phase
4bn-AE for the 15s AJ baseline). Closing (no-ML) would be premature on unmeasured
pessimism; insufficient-evidence does not apply (artefacts complete/valid).

## Recommended future preregistration / evaluation contract (if any)

Exactly one future **docs-only** ML baseline preregistration/evaluation-contract memo,
deciding: target horizon(s) (5m primary; 30m/1h secondary diagnostic); fixed run-once
baseline families (majority / persistence / L2-logistic, frozen hyperparameters);
train/validation/holdout treatment on the existing chrono split + 1-day embargo;
block-level dependence evidence (275 dates / 9 months; no per-row significance); the
Phase 4bn-AE §13 metric registry (accuracy/balanced-acc/macro-F1 vs both floors,
calibration/confidence-tail, descriptive cost realism); pre-registered kill/continue
criteria (not relaxed after results); and the absolute no-strategy/PnL/backtest/live
boundary. It must record that the evaluation itself (row-level label+feature reads or a
long-horizon ML dataset build) is a **further separately-authorized** step beyond the
memo (AH→AJ pattern). **No prompt generated; no ML authorized.**

## Explicit boundary confirmations

- No Parquet read (no built labels, no source feature/normalized, no raw zip). ✅
- No output-namespace mutation; no build rerun. ✅
- No v002 terminal / sealed test / test rows. ✅
- No AH/AJ namespace mutation; no AH builder / AI diagnostics / AJ baseline rerun; no
  AJ/AI/AH metric revised. ✅
- No ML / training / scoring / prediction / inference; no feature selection / threshold
  optimization / model selection / hyperparameter search / calibration training /
  confidence-tail selection. ✅
- No cost-aware / magnitude / deadband label adopted; no threshold picked. ✅
- No strategy / signals / PnL / backtest / paper / shadow / live / exchange-write. ✅
- No eligibility / authorization / manifest / gate / sidecar flag transition;
  `flip_research_eligible(...)` never invoked; frozen v002 family unmutated. ✅
- Nothing committed under `data/`; `.claude/scheduled_tasks.lock` not committed. ✅
- Allowed claim scope (AE §8 a/b/c) and forbidden claim scope (AE §8/§19) preserved;
  locked cost 8 bps/side · 16 bps round-trip preserved; the large 30m/1h shares labelled
  descriptive-only. ✅

## Remaining blockers before any ML / diagnostics over the built labels

A separate future operator authorization; the recommended docs-only preregistration/
evaluation-contract memo (itself separately prompted); and, beyond that memo, a further
separate authorization for the actual evaluation (row-level label+feature reads or a
long-horizon ML dataset build). No threshold/model/feature selection until then; all
non-authorization flags remain `false`.

## Remaining blockers before any strategy / PnL / backtest / live path

Absolute (Phase 4bn-AE §19). A separate future **M0-style mechanism-admissibility memo**
clearing M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution feasibility, and
slippage/spread — which aggTrades-only data cannot support (mid/book required; the
`bookticker_midprice_data_admissibility_memo` remains deferred/unauthorized) — plus label
economic relevance, strategy admissibility vs the retained rejections and the M0 §7.D
microstructure-lane `NOT_RECOMMENDED_NOW` posture, the Phase 4al no-rescue constraints,
and separate authorization for each capability. No AO/AN result softens this boundary.

## Recommended state

**Remain paused.** Diagnostics recorded; one docs-only preregistration/evaluation-contract
memo recommended but **not started** and awaiting a separate future operator prompt.

## Result state

`LONGHORIZON_LABEL_DIAGNOSTICS_RECORDED__ML_BASELINE_PREREGISTRATION_MEMO_RECOMMENDED__NO_ML__NO_PARQUET_READ__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## Explicit no-successor execution statement

Phase 4bn-AO authorizes **no** successor execution phase. It does not generate the
recommended memo's prompt; run any ML / scoring / prediction / inference; read any
Parquet for row-level analysis; build any ML/dataset/label namespace; do feature
selection / threshold optimization / model selection / hyperparameter search; rerun the
AN build / AH builder / AI diagnostics / AJ baselines; do strategy / signals / PnL /
backtest / paper-shadow / live / exchange-write; or authorize any Phase 5 / successor
phase. Every retained verdict and project lock is preserved verbatim (8 bps/side · 16 bps
round-trip; the Phase 4aw always-raises invariant — never invoked; Phase 4bb-F sidecar
policy; the Phase 4bn-AE claim-scope and §19 boundary; the 4bn-AH..AN results including
the AK single-follow-up selection, the AL/AM recommendations, and the AN build). Do not
merge to main and do not push unless explicitly instructed in a later prompt; do not
generate a merge-closeout or the recommended next prompt unless explicitly instructed
later.
