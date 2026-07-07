# Phase 4bn-AH — Merge Closeout

## 1. Phase name and branch

- **Phase:** 4bn-AH — Data-Reading ML Dataset Builder Implementation + Single Run.
- **Phase type:** code + controlled local data read + local gitignored output
  creation / single controlled run.
- **Action:** merge into `main`.
- **Source branch:** `phase-4bn-ah/data-reading-ml-dataset-builder-single-run`.
- **Target branch:** `main`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (it performed the first
  authorized local data read of the pre-v002 feature/label segments and created
  the first local ML dataset artefact; the full 16-section structure is used).

## 2. Base SHA

`1f4c89b6649181dc7b82e34bcfa97f4b3b7c87f9`
(`docs(phase-4bn-ag): finalize merge closeout shas`).

## 3. Pre-merge branch HEAD

`9f353a177593297a0adedc23e79be81f817363f1`
(`docs(phase-4bn-ah): add data-reading builder closeout`).

Branch commits:

- `5327bcf` — `code(phase-4bn-ah): implement data-reading ml dataset builder single run`
  (source + tests).
- `9f353a1` — `docs(phase-4bn-ah): add data-reading builder closeout`
  (implementation report + closeout).

## 4. Main / origin main before merge

`main == origin/main == 1f4c89b6649181dc7b82e34bcfa97f4b3b7c87f9` (verified in
sync before the merge).

## 5. Summary of AH implementation

Phase 4bn-AH added `pre_v002_ml_dataset_run.py` — a streaming, bounded-memory,
fail-closed **data-reading** builder that imports and reuses the Phase 4bn-AF
skeleton (`pre_v002_ml_dataset_contract` / `_builder` / `_proof`), uses the Phase
4bn-AA split artefact (`pre_v002_split_policy`), and binds the Phase 4bn-AC
contract + Phase 4bn-AE amendment. It is a new pre-v002-specific module and never
wraps, copies, or reuses the v002-terminal loader `ml_baseline_dataset_v002`. It
verifies all source bindings before reading (manifest/config/gate SHA256s at full
value; per-Parquet SHA256 + Phase 4bb-F sidecar + manifest inventory for 550
files; 275/275 partition discovery; split-authority binding), runs a real Phase
4bn-L budget preflight before any write (fail-closed on breach), streams all 275
partitions once, fits the train-only transform statistics on the `train` split
only, and — because a full `~144 GiB` model matrix would breach the `125 GiB`
derived-footprint hard cap — writes a **compact leakage-proof dataset
specification** (train-only transform stats + per-date split/filter index +
per-month/class summaries + leakage proof + dataset manifest; ~97 KB) with Phase
4bb-F sidecars to the single authorized gitignored namespace. A one-run guard
prevents overwrite (rerun requires separate authorization). Tests: 26 new offline
tests added; the 97 Phase 4bn-AF skeleton tests still pass (two behaviourally
adjusted from asserting the namespace is *absolutely absent* to asserting the
*skeleton never creates/removes it*, since Phase 4bn-AH is the authorized phase
that creates it).

## 6. Summary of AH single controlled run

One controlled run, ~19.2 min, streaming all **400,001,695** rows. Splits: train
`304,816,127` / embargo `3,071,370` / validation `68,578,296` / holdout
`23,535,902`. Kept (filtered): train `304,816,127` / validation `68,578,296` /
holdout `23,535,860`. Dropped: holdout `censored = 42` (segment-terminal 15s
censoring, exactly matching the label manifest's 15s count); every other cell 0;
`invalid_price = 0`; **no targets imputed**. Per-horizon earlier-split
boundary-crossing rows `0` (1s/5s/15s/60s). Strict alignment: 400,001,695 rows,
`0` mismatches. Budget preflight **passed** (D: 1166.24 GiB free). The
leakage/split-integrity proof was assembled and **validated before any write**.

## 7. Output namespace

`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` — created
exactly once by Phase 4bn-AH (4 artefacts + 4 Phase 4bb-F `.sha256` sidecars).

## 8. Output namespace gitignored and uncommitted

Confirmed. `git check-ignore -v data/research/microstructure/ml_datasets/pre_v002_contract_v001/`
→ `.gitignore:88`. `git ls-files data/research/microstructure/ml_datasets/pre_v002_contract_v001/`
→ **0 tracked files**. The namespace is local, gitignored, and uncommitted. The
merge did **not** touch, overwrite, refresh, or mutate it (a read-only `ls`
confirmed the 8 files remain intact).

## 9. No data files committed

Confirmed. The branch tracks **0 files** under `data/microstructure/` and **0**
under `data/research/`. The merge brings forward only source, tests, and docs (§5
/ §13). No data output is staged or committed.

## 10. No builder rerun occurred during merge

Confirmed. The Phase 4bn-AH data-reading builder was **not** re-invoked during
this merge review. No command created, overwrote, deleted, mutated, or refreshed
the output namespace. Validation used the offline test suite only; the one-run
guard remains active.

## 11. No diagnostics / ML / model / scoring / prediction / strategy / signals / PnL / backtest during merge

Confirmed. None were run. The merge review ran only `pytest` (offline synthetic
tests), `ruff`, `mypy`, and git state checks.

## 12. No v002 terminal read, no sealed test touch, test_rows_loaded = 0 (as recorded by AH)

Confirmed as recorded in the AH leakage proof and reports:
`v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
`test_rows_loaded = 0`. The merge changes none of this.

## 13. Validation commands and results (this merge review)

- `pytest …test_phase4bn_ah… …test_phase4bn_af…` → **123 passed** (26 AH + 97
  AF skeleton).
- `ruff check` (AH module + both test files) → **All checks passed**.
- `mypy src/…/pre_v002_ml_dataset_run.py` → **0 direct errors in the new AH
  module**; **2 pre-existing sibling errors** surface transitively (see §14).
- `git diff --check` → clean.
- `git diff --name-status main..branch` → `A` closeout, `A` implementation report,
  `A` `pre_v002_ml_dataset_run.py`, `M` `test_phase4bn_af…skeleton.py`, `A`
  `test_phase4bn_ah…run.py` (5 files; 2067 insertions, 3 deletions) — matches the
  expected change set.
- `git ls-tree -r --name-only branch -- data/microstructure/` → **0**;
  `… -- data/research/` → **0**.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `… data/research/` → `.gitignore:88`;
  `… data/research/microstructure/ml_datasets/pre_v002_contract_v001/` →
  `.gitignore:88`.
- `git ls-files …/pre_v002_contract_v001/` → **0 tracked files**.

## 14. mypy caveat (direct vs pre-existing)

The new AH module `pre_v002_ml_dataset_run.py` introduces **0 direct mypy
errors**. Running mypy with it as the entry point surfaces **2 pre-existing
errors in committed sibling modules** — `labels_manifest_v002.py:370`
(`Incompatible types in assignment`) and `multiday_feature_gate_checks.py:847`
(`Function is missing a type annotation`) — both reproduced by mypy on the
committed Phase 4bn-AF skeleton builder module and **unmodified by this phase**.
**Whole-repo mypy is therefore not clean**; these two errors are pre-existing and
are not introduced by Phase 4bn-AH.

## 15. Git status before merge

```text
?? .claude/scheduled_tasks.lock
```

Only the expected transient untracked `.claude/scheduled_tasks.lock` (not
committed). Working tree otherwise clean on the branch tip.

## 16. Merge method

`git checkout main` → confirm `main == 1f4c89b` → `git merge --no-ff
phase-4bn-ah/data-reading-ml-dataset-builder-single-run -m "code(phase-4bn-ah):
merge data-reading ml dataset builder single run"`. `ort` strategy; no squash; no
rebase; no `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
force-push. `.claude/scheduled_tasks.lock` and all data outputs excluded. Pushed
to `origin/main` with no force, no skip-hooks, no skip-signing.

## 17. Final merge commit SHA

Recorded by the SHA-finalization commit below (`docs(phase-4bn-ah): finalize
merge closeout shas`) after the merge is created.

## 18. Final main / origin main SHA

Recorded by the SHA-finalization commit below; equals the SHA-finalization commit
SHA (the resulting `main` / `origin/main` tip); reproduced in the final operator
report and `git log`.

## 19. Result state

`DATA_READING_ML_DATASET_BUILDER_MERGED_TO_MAIN__SINGLE_RUN_PROOF_PRESERVED__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED`

## 20. Recommended state

**Remain paused.**

## 21. Explicit no-successor authorization

**None.** No successor is authorized by this merge. Phase 4bn-AI (descriptive
dataset diagnostics), Phase 4bn-AJ (fixed baseline run), Phase 4bn-AK
(arc-decision), ML training, model scoring, predictions, diagnostics, strategy,
signals, PnL, backtests, additional data reads, a Phase 4bn-AH builder rerun, a
new dataset namespace, v003, compacted Parquet, database outputs, paper / shadow,
live-readiness, deployment, exchange-write, production keys, authenticated APIs,
private endpoints, user stream, MCP / Graphify / `.mcp.json` / credentials, and
all other candidates each require **separate operator authorization**.

## 22. Retained verdict ledger

All preserved verbatim: H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1,
C1.

## 23. Preserved project locks

All preserved verbatim: §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3;
Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11;
Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al refined
no-rescue rule; Phase 4aw `flip_research_eligible(...)` always-raises invariant
(never invoked); Phase 4bb-F canonical path + sidecar policy; Phase 4bl-F risk
tiers; Phase 4bm-U / 4bm-W v002 split policy; Phase 4bn-L derived-stack storage
budget; Phase 4bn-N/R/V manifest-versioning; Phase 4bn-Y chronological split;
Phase 4bn-Z / AA / AB / AC / AD / AE / AF / AG results. All prior phase results
preserved verbatim.

## 24. Manifest state preservation

No published manifest / gate report / sidecar / successor-state artefact was
created, read for mutation, or mutated. At every pre-v002 layer:
`research_eligible = false`; `eligibility_gate_status = pending`;
`chronological_split_policy = not set`; `diagnostics_authorized` /
`ml_authorized` = false; `source_admissible_for_data_read` /
`source_admissible_for_dataset_builder` remain false (memo-level concepts).
The Phase 4aw `flip_research_eligible(...)` always-raises invariant was never
invoked. The AH builder read the published feature/label Parquet **read-only** to
build a separate local gitignored dataset specification; it wrote nothing back to
`data/microstructure/`.
