# Phase 4bn-Z — Closeout

## 1. Phase identity

- **Phase:** 4bn-Z — ML-Baseline Readiness Memo.
- **Phase type:** docs-only / ML-readiness / dataset-contract /
  split-implementation-precondition / source-admissibility / leakage-control
  memo.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
- **Branch-complete only:** not merged into `main`; not project-complete.
  Becomes project-complete only when a separately authorized merge phase records
  its merge-closeout on `main`.

---

## 2. SHAs

- **Branch:** `phase-4bn-z/ml-baseline-readiness-memo`.
- **Base `main` SHA:** `896f5fa1aaccaa4ed8504e5d815929eeb50ca398`
  (`docs(phase-4bn-y): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 896f5fa1…` verified.
- **Predecessors present on `main`:** Phase 4bn-Y `896f5fa` / `e55e5a8` /
  `69005a4` / `f4d4b5d`; Phase 4bn-X `5d69e67`.
- **Branch commit SHA:** recorded in the final operator report (this closeout is
  committed in the same single commit
  `docs(phase-4bn-z): assess ml baseline readiness`).

---

## 3. Files created / modified

**Created (2):**

- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-z_ml-baseline-readiness-memo.md`
  (26 sections).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-z_closeout.md` (this
  file).

**Modified narrowly (1):**

- `docs/00-meta/current-project-state.md` — additive only: one new Phase 4bn-Z
  paragraph + one new `Current phase:` block; all prior content preserved
  verbatim.

**No** code, tests, scripts, config, manifests, gate reports, sidecars, split
files, research matrices, ML configs, or data files were created or modified.

---

## 4. Validation commands run

- `git status --short` → only the three tracked Phase 4bn-Z docs files plus the
  pre-existing untracked `.claude/scheduled_tasks.lock`.
- `git diff --check` → clean (no whitespace errors).
- `git diff -- docs/00-meta/current-project-state.md docs/00-meta/implementation-reports/2026-06-05_phase-4bn-z_ml-baseline-readiness-memo.md docs/00-meta/implementation-reports/2026-06-05_phase-4bn-z_closeout.md`
  → only additive docs changes.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.

No markdown-lint tooling is repo-standard for these reports (predecessor memos
are not lint-gated); none was run, and none would have created or mutated any
artefact. Exact command outputs are reproduced in the final operator report.

---

## 5. Local gitignored outputs

**None.** This phase created no `data/microstructure/` or `data/research/`
output and read none. The pre-v002 local artefacts (Phase 4bn-O/P/S/T/W/X)
remain uncommitted and unread.

---

## 6. Readiness verdict

**Policy-ready but NOT implementation-ready for ML on the pre-v002 path.** The
project has produced and locally gated the normalized / feature / label source
layers and recorded the Phase 4bn-Y split policy, but still lacks: a code-level
pre-v002 split-policy artefact + offline tests; explicit source-admissibility
resolution; an ML dataset contract / builder; a leakage / split-integrity proof;
a budget preflight for dataset construction; and a per-task target / horizon /
filtering decision.

- **ML training ready now:** **No.**
- **ML dataset creation ready now:** **No.**
- **Research matrix creation ready now:** **No.**
- **Code-level split-policy artefact required before any dataset builder:**
  **Yes.**
- **Split-policy artefact should be the next recommended phase:** **Yes.**
- **Source admissibility unresolved (a blocker for data use):** **Yes.**
- **Full-envelope assembly required for first conservative pre-v002-only path:**
  **No.**
- **Holdout-boundary memo required for first conservative pre-v002-only path:**
  **No.**

---

## 7. Existing committed ML-baseline tooling boundary

- Committed tooling = Phase 4bn-B `ml_baseline_design_v002.py` +
  `ml_baseline_dataset_v002.py`, plus the Phase 4bm-W
  `diagnostics_split_policy_v002.py` split helper.
- All three are hardcoded to the **v002 terminal** (90 partitions /
  155,153,449 rows / `feature_config_hash 819cfa7a…` / `label_config_hash
  352bad41…` / dates 2024-12-01..2025-02-28 / split
  `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`) and are **inadmissible to
  the pre-v002 segment** (the dataset loader rejects the pre-v002 hashes /
  partition count; `split_for_date()` raises on every pre-v002 date).
- `ml_baseline_splits.py` and `ml_baseline_train.py` **do not exist**; there is
  **no committed end-to-end trainer**.
- A future pre-v002 path needs a new segment-scoped split artefact (and later
  dataset/training wrappers) reusing the locked design constants and leakage
  controls — exactly the Phase 4bn-O/S/W segment-wrapper precedent.

---

## 8. Future allowed scope (if ever separately authorized)

- **Source scope:** BTCUSDT / Binance USDⓈ-M futures / aggTrades; pre-v002 only,
  2024-03-01 .. 2024-11-30 (275 dates); Phase 4bn-S features + Phase 4bn-W
  labels only, after admissibility is resolved; v002 terminal and sealed test
  excluded.
- **Split scope:** Phase 4bn-Y Candidate A exactly (214 / embargo 2024-10-01 /
  45 / embargo 2024-11-16 / 14; chronological-only; ≥ 60 s floor + 1-day purge;
  no shuffle; v002/sealed excluded).
- **Label / target scope:** family `microstructure_labels_aggtrades_v001 @ v002`
  (`label_schema_version v001`); horizons 1s/5s/15s/60s available; 3-class signed
  direction `{-1,0,+1}` (and/or forward-log-return); recommend a narrow single
  horizon for a first baseline; no barrier / stop / MFE / MAE / R-multiple / PnL
  labels.
- **Feature scope:** only the 45 causal computed `FEATURE_SCHEMA_V002` columns;
  exclude the 17 lineage columns, all label / support / split / censor columns
  (`FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`), quality flags beyond the two design
  flags, raw prices, and any future-looking / post-label column.
- **Censored / invalid filtering:** drop per-horizon nulls and censored rows;
  reject invalid-price rows; never impute targets; internal holdout is dry-run
  only (no selection / tuning); sealed test stays `test_rows_loaded = 0`.

---

## 9. Future leakage / split-integrity proof requirements

A future pre-v002 dataset builder / split artefact must emit a checkable proof:
214 / 1 / 45 / 1 / 14 date assignment with none unassigned or double-assigned;
zero earlier-split boundary-crossing rows per horizon under the ≥ 60 s embargo +
1-day purge; assignment a pure function of `source_transact_time_ms` UTC date
(no RNG); `v002_terminal_window_read = false` / `sealed_test_split_touched =
false` / `test_rows_loaded = 0` with hard raise on any out-of-segment date;
strict per-day positional feature/label alignment; manifest / config-hash
binding (`4881eb87…` / `0726b41d…` / `69746c88…` / `b3bd5d2b…` and gate reports
`db731d1b…` / `3452fd9d…` / `ffb5b09…`); and train-only transform provenance.

---

## 10. Future budget preflight requirements

Phase 4bn-L caps, fail-closed before any write: derived footprint warn 75 GiB /
hard 125 GiB; total derived-stack warn 250 GiB / hard 300 GiB; runtime warn 4 h /
hard 8 h; temp warn 50 GiB / hard 100 GiB; `D:` ≥ 500 GiB before / fail closed
below 350 GiB during.

---

## 11. Result / decision

- **Result state:**
  `ML_BASELINE_READINESS_RECORDED__PRE_V002_PATH_READY_FOR_SPLIT_POLICY_ARTEFACT__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_PRE_V002_SPLIT_POLICY_ARTEFACT__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Selected next recommendation:** Phase 4bn-AA — Pre-V002 Split-Policy Artefact
  + Offline Tests (pure code/tests, no data I/O; not blocked by admissibility).
- **Recommended state:** remain paused.
- **MEMO RECORDED.**

---

## 12. Boundary confirmations

- No local data read; no local data created.
- No ML trained; no ML dataset created; no research matrix created; no scoring;
  no predictions; no diagnostics; no strategy / signals / PnL / backtests.
- No acquisition, endpoint call, archive download, or HEAD preflight.
- No raw / normalization / feature / label execution or any layer gate re-run.
- No local raw zip, normalized / feature / label Parquet, manifest, gate report,
  or sidecar read.
- No v002 terminal window read; no sealed-test read or touch
  (`test_rows_loaded = 0`).
- No storage migration; no database; no Parquet compaction; no v003.
- No manifest mutation; no `chronological_split_policy` set; no
  `research_eligible` flip; no `eligibility_gate_status` transition.
- No `data/research` or `data/microstructure` artefact created or committed.
- No code / tests / scripts added.
- No successor authorized.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).
- Recorded v002 `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` and Phase
  4bn-Y Candidate A policy preserved verbatim.

---

## 13. Successor authorization

**None.** Not authorized by this phase: any merge phase; the pre-v002
split-policy code artefact; a source-admissibility memo/gate; an ML dataset
contract memo; an ML dataset builder; a research matrix; any model / scoring /
prediction; any diagnostics; any strategy / signals / PnL / backtest; a
full-envelope reference/assembly memo; a holdout-boundary memo; a source-policy
documentation memo; a process-doc path update; any acquisition; any paper /
shadow / live / exchange-write / production-key; any Phase 5; any other
successor.

---

## 14. Recommended state

**Remain paused.** No next phase authorized.

---

## 15. Final git state

Reproduced in the final operator report (`git status --short`,
`git log --oneline -8 --decorate`, `git rev-parse HEAD`, `git rev-parse main`,
`git rev-parse origin/main`) so the operator need not run a separate status / SHA
check manually.
