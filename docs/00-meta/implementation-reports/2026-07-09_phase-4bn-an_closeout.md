# Phase 4bn-AN — Closeout

## Branch

`phase-4bn-an/longer-horizon-label-build-single-run`

## Base SHA

`ea8c6d9f8bfb116c6cfc45486be2836e77ee4a59`
(`main == origin/main == HEAD` at branch time; tip after the Phase 4bn-AM merge
closeout.)

## Phase type

Code + test + **single controlled data build** — implements the new sibling
longer-horizon label family `microstructure_labels_longhorizon_aggtrades_v001`
(horizons 5m / 30m / 1h) recommended and pre-registered by Phase 4bn-AM, and runs
it exactly once over the admitted pre-v002 aggTrades segment. Reads only admitted
pre-v002 sources; writes only a local/gitignored research namespace; no ML; no
strategy; no successor execution authorized.

## Files created / modified

Committed (source / tests / docs only):

- `src/prometheus/research/microstructure/longhorizon_labels_schema_v001.py`
- `src/prometheus/research/microstructure/longhorizon_labels_compute_v001.py`
- `scripts/phase4bn_an_build_longhorizon_labels.py`
- `tests/research/microstructure/test_phase4bn_an_longhorizon_labels.py`
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-an_longer-horizon-label-build-single-run.md`
- `docs/00-meta/implementation-reports/2026-07-09_phase-4bn-an_closeout.md` (this file)

No frozen module, manifest, gate report, sidecar, split file, or ML config was
modified. `current-project-state.md` left unchanged (report §44). **No** data file
was committed.

## Local output namespace

`data/research/microstructure/labels/microstructure_labels_longhorizon_aggtrades_v001_pre_v002/`
(gitignored via `.gitignore:88`).

## Output artefact inventory

275 per-day label Parquet + 275 `.sha256` sidecars; plus under `_manifest/`:
`manifest.json`, `leakage_split_censoring_proof.json`,
`continuous_return_cost_summary.json`, `build_run_record.json`,
`sidecar_inventory.json` — each with a paired `.sha256`. Total footprint
**11,940,496,483 bytes (~11.12 GiB)**; `label_config_hash`
`edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118`.

## Validation commands

- `pytest tests/research/microstructure/test_phase4bn_an_longhorizon_labels.py` →
  **15 passed**.
- `ruff check` (new modules/orchestrator/test) → **All checks passed**.
- `mypy` (new src modules) → no new errors (only the repo's pre-existing baseline
  errors in unrelated frozen feature modules).
- Frozen regression (`test_labels_schema_v002`, `test_labels_compute_v002`,
  `test_phase4bn_aa_pre_v002_split_policy`) → **108 passed**.
- `git status --short`, `git diff --check`, `git ls-files data/microstructure/`,
  `git ls-files data/research/`, `git check-ignore -v` (both) → data 0 tracked,
  both ignored, clean.
- Independent post-run artefact verification: 5/5 JSON sidecars valid; sampled
  per-day Parquet SHAs + sidecars valid; 275 distinct dates; inventory rows sum =
  400,001,695.

## Concise build outcome

Single controlled run built **275 partitions / 400,001,695 label rows** in
**4,716 s (~78.6 min)**, ~11.12 GiB, all under the Phase 4bn-L caps. Leakage/split/
censoring proof: **per-horizon earlier-model-split boundary-crossing rows = 0**
(train/validation × 5m/30m/1h); split counts train 214 / embargo 2 / validation 45
/ holdout 14; per-horizon envelope-terminal censoring 5m 1,528 / 30m 9,916 / 1h
23,650 (holdout tail only); 0 invalid prices; no NaN/Inf; `v002_terminal_window_read
= false`; `sealed_test_split_touched = false`; `test_rows_loaded = 0`;
`frozen_v002_family_mutated = false`; `data_committed = false`; all eight
non-authorization flags `false`. **Descriptive** materiality (label-diagnostic
only): the raw `|forward_log_return_H|` median grows with horizon (~10–11 bps at 5m,
~24–25 bps at 30m, ~33–34 bps at 1h) and the validation share clearing 16 bps
round-trip is ~35% (5m) / ~64% (30m) / ~73% (1h), vs 2.47% at 15s (Phase 4bn-AJ).
**This is a descriptive property of the raw move distribution only — not tradability,
predictability, edge, or PnL, and aggTrades-only data cannot express spread/slippage.**

## Final AN decision / result state

`LONGER_HORIZON_LABEL_BUILD_COMPLETE__LOCAL_LABEL_ARTEFACTS_WRITTEN__NO_ML__NO_STRATEGY__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## Boundary confirmations

- No data files read outside the admitted pre-v002 segment; no acquisition /
  endpoint / raw zip / credentials. ✅
- No v002 terminal read; sealed test untouched; `test_rows_loaded = 0`. ✅
- No AH ML-dataset / AJ baseline namespace mutation (or read); no AH/AI/AJ rerun; no
  AJ/AI/AH metric revised. ✅
- Frozen v002 short-horizon family (and every frozen module / manifest / gate /
  sidecar / split file / ML config) unmodified; a new sibling family was built. ✅
- No ML / training / scoring / prediction / inference; no feature selection /
  threshold optimization / model selection / hyperparameter search; no cost-aware /
  magnitude / deadband label; no threshold tuning. ✅
- No strategy / signals / PnL / backtest / paper / shadow / live / exchange-write. ✅
- No `research_eligible` flip; no authorization-flag transition;
  `flip_research_eligible(...)` never invoked. ✅
- Output namespace local + gitignored; **no data committed**;
  `.claude/scheduled_tasks.lock` not committed. ✅
- Allowed claim scope (AE §8 a/b/c) and forbidden claim scope (AE §8/§19) preserved;
  locked cost 8 bps/side · 16 bps round-trip preserved; the longer-horizon summaries
  labelled descriptive-only. ✅

## Remaining blockers before any ML / diagnostics over the built labels

Building the label layer is **not** permission to model it. Any ML training,
scoring, prediction, inference, feature selection, threshold optimization, model
selection, hyperparameter search, or diagnostics beyond the descriptive build
summaries requires its **own separate future operator authorization**; all
non-authorization flags remain `false`.

## Remaining blockers before any data read / build (beyond this one)

This phase's single controlled run is complete and one-run-guarded. Any further
build, re-run, additional horizon, per-month/per-date descriptive extension, or new
data read requires separate future operator authorization.

## Remaining blockers before any strategy / PnL / backtest / live path

Absolute (Phase 4bn-AE §19). A separate future **M0-style mechanism-admissibility
memo** clearing M0.5 cost realism at 8 bps/side · 16 bps round-trip, execution
feasibility, slippage/spread (aggTrades-only data cannot support — mid/book required;
the `bookticker_midprice_data_admissibility_memo` remains deferred and unauthorized),
label economic relevance, strategy admissibility vs the retained rejections and the
M0 §7.D microstructure-lane `NOT_RECOMMENDED_NOW` posture, and the Phase 4al
no-rescue constraints — **plus** separate authorization for each of strategy /
signals / PnL / backtest / paper-shadow / live / exchange-write. No AN build result,
however favourable the descriptive materiality looks, softens this boundary.

## Recommended state

**Remain paused.** The longer-horizon label layer exists locally (gitignored) with
verified integrity and descriptive summaries. Nothing downstream is authorized.

## Explicit no-successor execution statement

Phase 4bn-AN authorizes **no** successor execution phase. It does not run or
authorize any ML / diagnostics / strategy / signals / PnL / backtest / paper-shadow
/ live / exchange-write over the built labels; it does not build any further labels
or read any further data; it does not generate the next-phase prompt; and it does
not authorize any Phase 5 / successor phase. Every retained verdict and project lock
(8 bps/side · 16 bps round-trip; the Phase 4aw `flip_research_eligible(...)`
always-raises invariant — never invoked; Phase 4bb-F sidecar policy; the Phase
4bn-AE claim-scope and strategy/PnL/backtest/live boundary; the 4bn-AH..AM results
including the AK single-follow-up selection, the AL label-memo recommendation, and
the AM contract) is preserved verbatim. Do not merge to main and do not push unless
explicitly instructed in a later prompt; do not generate a merge-closeout or the
next-phase prompt unless explicitly instructed later.
