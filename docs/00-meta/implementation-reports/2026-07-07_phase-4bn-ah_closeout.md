# Phase 4bn-AH — Closeout

## Branch

`phase-4bn-ah/data-reading-ml-dataset-builder-single-run`

## Base SHA

`1f4c89b6649181dc7b82e34bcfa97f4b3b7c87f9`
(`docs(phase-4bn-ag): finalize merge closeout shas`).

## Commit SHA

Recorded at commit time in the final operator report and `git log`. Source +
tests + docs are committed together on the branch (no data output committed).

## Phase type

Code + controlled local data read + local gitignored output creation / single
controlled run. **Tier 1 — Full Phase.**

## Files created

- `src/prometheus/research/microstructure/pre_v002_ml_dataset_run.py`
- `tests/research/microstructure/test_phase4bn_ah_pre_v002_ml_dataset_run.py`
- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ah_data-reading-ml-dataset-builder-single-run.md`
- `docs/00-meta/implementation-reports/2026-07-07_phase-4bn-ah_closeout.md`

## Files modified

- `tests/research/microstructure/test_phase4bn_af_pre_v002_ml_dataset_builder_skeleton.py`
  — two tests (`test_imports_do_not_create_future_namespace`,
  `test_no_output_namespace_created`) changed from asserting the output namespace
  is *absolutely absent* to asserting the **skeleton never creates/removes it**
  (existence unchanged across exercising the skeleton surface), because Phase
  4bn-AH is the authorized phase that legitimately creates it. No other change.

No source module was modified; no manifest / gate report / sidecar / split file /
research matrix / ML config / `data/microstructure` file was created or modified;
no committed data file was created.

## Validation commands run

- `pytest …test_phase4bn_ah… …test_phase4bn_af…` → **123 passed** (26 new + 97
  skeleton).
- `ruff check` (new module + both test files) → **All checks passed**.
- `mypy` (new module) → **0 direct errors**; 2 pre-existing sibling errors
  (`labels_manifest_v002.py:370`, `multiday_feature_gate_checks.py:847`) reproduced
  by the committed skeleton builder, unmodified here.
- `git diff --check` → clean.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `data/research/` → `.gitignore:88`; the dataset artefacts → `.gitignore:88`.
- Real Phase 4bn-L budget preflight → **PASSED** (D: 1166.24 GiB free).
- `validate_builder_run_proof` → **VALIDATED** (before write; re-verified on disk).
- One-run guard → second invocation fails closed.

## Implementation summary

A streaming, bounded-memory, fail-closed data-reading builder that imports the
Phase 4bn-AF skeleton, uses the Phase 4bn-AA split artefact, binds the Phase
4bn-AC contract + Phase 4bn-AE amendment, verifies all source bindings before
reading, streams all 275 partitions once, fits the train-only transform
statistics on the `train` split only, and writes a **compact leakage-proof dataset
specification** (not a budget-breaching 144 GiB re-materialisation) with Phase
4bb-F sidecars to the single authorized gitignored namespace. It is a new
pre-v002-specific module; it never wraps/copies the v002-terminal loader.

## Run summary

Single run, **1152.6 s (~19.2 min)**, **400,001,695** rows streamed. Splits: train
304,816,127 / embargo 3,071,370 / validation 68,578,296 / holdout 23,535,902.
Kept: train 304,816,127 / validation 68,578,296 / holdout 23,535,860. Dropped:
holdout censored 42 (segment-terminal 15s censoring, matching the label
manifest); all other cells 0; no imputation. Per-horizon boundary crossings 0
(1s/5s/15s/60s). `test_rows_loaded=0`; `v002_terminal_window_read=false`;
`sealed_test_split_touched=false`. Budget preflight passed.

## Output namespace path

`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` — created once,
gitignored, uncommitted.

## Data outputs gitignored and not committed

Confirmed: 4 artefacts + 4 `.sha256` sidecars under the namespace; `git
check-ignore` → `.gitignore:88`; `git status` shows no `data/` file.

Artefact SHA256:
`dataset_manifest.json` `36a13213…`; `train_only_transform.json` `85f6ea35…`;
`split_index.json` `d1681acd…`; `leakage_split_integrity_proof.json` `e36c9163…`.

## Pre-read checks

Source scope; manifest SHA256 (full values `0e96ae37…` / `4881eb87…` /
`69746c88…`); config hashes (`0726b41d…` / `b3bd5d2b…`; v002 `819cfa7a…` /
`352bad41…` rejected); gate-report SHA256 (full values `3452fd9d…` / `db731d1b…` /
`ffb5b092…`); per-Parquet SHA256 + sidecar + inventory (550 files); 275/275
partitions; split-authority binding (commit `e12e928e33aa84e530a85a1a58b04d6ac217b1fb`).
All PASS.

## Pre-write checks

Strict pairing + positional alignment (400,001,695 rows, 0 mismatches); split
assignment; embargo drop; per-horizon boundary-crossing exclusion (0); target
filtering (never impute); 45-column allowlist; empty forbidden scan; train-only
transform; budget preflight passed; proof validated. All before write. All PASS.

## Budget preflight requirements

Phase 4bn-L, before any write, fail-closed on breach: derived 75/125 GiB;
total-stack 250/300 GiB; runtime 4/8 h; temp 50/100 GiB; D: ≥ 500 GiB before
(measured 1166.24); fail-closed < 350 GiB during. Result recorded in the proof.

## Leakage / split-integrity proof requirements

Machine-checkable JSON + Phase 4bb-F sidecar covering split policy name / module /
commit; 214/1/45/1/14; no missing/duplicate/multi-assigned dates; no embargo used;
zero out-of-segment; no v002/sealed; test_rows_loaded=0; no random/shuffle/kfold/
bootstrap; deterministic UTC-date assignment; per-horizon zero boundary crossings;
key-alignment counts; drops by split/reason; 45-column feature-list hash; empty
forbidden scan; train-only provenance; budget result; metric registry; date/month
schema; dependence caveat; calibration schema; cost fields; success/kill
constants; non-authorization flags all false; namespace created once; no outputs
outside it. VALIDATED.

## Sidecar / metadata requirements

Every artefact + the proof carry canonical two-space `.sha256` sidecars (verified);
a local dataset manifest was written as defined by this phase; all local,
gitignored, uncommitted; none imply eligibility or set any source-manifest field.

## Future output namespace posture

Created exactly once at the authorized path. One-run guard now prevents overwrite;
rerun requires separate authorization.

## Forbidden outputs

None created: no model / prediction / diagnostics / research matrix beyond the
dataset spec / backtest / strategy / PnL / v003 / compacted Parquet / database /
`data/microstructure` output / committed data file / anything outside the
namespace / any mutation of a published artefact.

## One-time run / rerun posture

Single controlled run executed. Rerun refused by the one-run guard; a rerun
requires separate operator authorization (no safe idempotent overwrite defined).

## Future validation requirements (for a later phase)

The Phase 4bn-AI descriptive-diagnostics phase (if separately authorized) should
run its own targeted tests, ruff, mypy, and read this dataset specification
read-only, computing only descriptive statistics (no models / scoring /
predictions).

## Result / decision

- **Result state:**
  `DATA_READING_ML_DATASET_BUILDER_IMPLEMENTED__SINGLE_RUN_COMPLETE__LEAKAGE_PROOF_VALIDATED__NO_ML__REMAIN_PAUSED`
- **Decision:** remain paused; recommend (not authorize) a future Phase 4bn-AI
  descriptive dataset-diagnostics phase, subject to separate operator
  authorization.

## Remaining blockers before Phase 4bn-AI diagnostics

Separate diagnostics authorization (`diagnostics_authorized=false`); a
pre-declared descriptive-only diagnostics scope (no models/scoring/predictions).

## Remaining blockers before ML training

A committed end-to-end pre-v002 trainer (does not exist); separate ML
authorization (`ml_authorized=false`); a separately-authorized baseline run
applying the Phase 4bn-AE success/kill evaluation.

## Recommended state

**Remain paused.**

## No successor authorized

No successor is authorized from inside Phase 4bn-AH. Phase 4bn-AI (diagnostics),
Phase 4bn-AJ (baseline run), Phase 4bn-AK (arc-decision), ML training, and any
other candidate require separate operator authorization.

## Boundary confirmations

- Local data read (only the authorized pre-v002 normalized-lineage / feature /
  label sources); a compact local gitignored dataset specification created.
- No v002 terminal window read; no sealed test touched (`test_rows_loaded=0`).
- No ML trained / scored / predicted; no diagnostics; no strategy / signals / PnL
  / backtests.
- No research matrix beyond the dataset spec; no model / v003 / compacted Parquet
  / database; no output under `data/microstructure/`; no committed data file; no
  output outside the namespace.
- No acquisition; no endpoint call; no archive download; no HEAD preflight; no
  layer-gate rerun.
- No `research_eligible` flip; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized` /
  `source_admissible_*` transition; no published manifest / gate report / sidecar
  mutated.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never
  invoked).
- No credentials / `.env` / `.mcp.json` / MCP / Graphify used; no paper / shadow /
  live / exchange-write.
- `.claude/scheduled_tasks.lock` untracked and uncommitted; nothing under
  `data/microstructure/` or `data/research/` committed.
- Every retained verdict and project lock preserved verbatim; no M0 amendment; no
  successor authorized.

## Final git status / SHAs

Reproduced in the final operator report (`git status --short`, `git log`, HEAD /
main / origin/main SHAs). This branch is **not merged** and **not pushed** (per
the authorization: do not merge, do not push unless later instructed).
