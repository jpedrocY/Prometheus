# Phase 4bn-AC — Closeout

## 1. Phase identity

- **Phase:** 4bn-AC — ML Dataset Contract Memo.
- **Phase type:** docs-only / ML dataset contract / pre-v002 source-binding /
  target-feature-filtering / leakage-proof / budget-preflight / no-data-read
  memo.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
- **Branch-complete only:** not merged into `main`; not project-complete.
  Becomes project-complete only when a separately authorized merge phase records
  its merge-closeout on `main`.

---

## 2. SHAs

- **Branch:** `phase-4bn-ac/ml-dataset-contract-memo`.
- **Base `main` SHA:** `46bcdd3862c2b82b268d668f1e2d0180243f0dce`
  (`docs(phase-4bn-ab): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 46bcdd38…` verified.
- **Predecessors present on `main`:** Phase 4bn-AB `46bcdd3` / `1d032a4` /
  `d200a8b` / `80e032c`; Phase 4bn-AA `e749598`.
- **Branch commit SHA:** recorded in the final operator report (this closeout is
  committed in the same single commit
  `docs(phase-4bn-ac): record ml dataset contract`).

---

## 3. Files created / modified

**Created (2):**

- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ac_ml-dataset-contract-memo.md`
  (32 sections).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ac_closeout.md` (this
  file).

**Modified narrowly (1):**

- `docs/00-meta/current-project-state.md` — additive only: one new Phase 4bn-AC
  paragraph + one new `Current phase:` block; all prior content preserved
  verbatim.

**No** code, tests, scripts, config, manifests, gate reports, sidecars, split
files, research matrices, ML configs, successor-state artefacts, or data files
were created or modified. No existing source or test was modified.

---

## 4. Code / tooling added or modified

**None.** Docs-only phase. No code, tests, or scripts were added or modified.

---

## 5. Tests added or modified

**None.**

---

## 6. Validation commands run

- `git status --short` → only the three tracked Phase 4bn-AC docs files plus the
  expected untracked `.claude/scheduled_tasks.lock`.
- `git diff --check` → clean (no whitespace / conflict markers).
- `git diff -- docs/00-meta/current-project-state.md <memo> <closeout>` →
  intended changes only.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- No repo-standard markdown lint tooling exists, so none was run; ruff / mypy /
  pytest omitted for a docs-only Tier 1 memo with no code surface.

Exact command outputs are reproduced in the final operator report.

---

## 7. Dataset contract verdict

The pre-v002 normalized / feature / label stack is **source-admissible for a
docs-only ML dataset contract only**. This memo records that contract by
reference. It does **not** make the stack admissible for data reads, a dataset
builder, or ML — those remain blocked and separately authorizable only.

---

## 8. Contract name

`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001` (docs-level contract
name only; no dataset / config / manifest created or set).

---

## 9. Source scope

- **Permitted (by reference, future-authorized read only):** BTCUSDT / Binance
  USDⓈ-M futures / aggTrades; pre-v002 only (2024-03-01..2024-11-30; 275 dates);
  Phase 4bn-S features (`4881eb87…` / `feature_config_hash 0726b41d…`) + Phase
  4bn-W labels (`69746c88…` / `label_config_hash b3bd5d2b…`); Phase 4bn-O
  normalized lineage (`0e96ae37…`) by reference.
- **Forbidden:** v002 terminal (2024-12-01..2025-02-28); sealed test
  (2025-02-14..2025-02-28); full-envelope assembly; non-BTCUSDT; spot /
  mark-price / order-book / kline / liquidation / funding / open-interest /
  cross-venue; newly acquired data; raw zip; any family not in the pre-v002
  chain (incl. published `819cfa7a…` / `352bad41…`); `data/research` priors;
  external / private / authenticated sources.

---

## 10. Target / horizon choice

- Family `microstructure_labels_aggtrades_v001 @ v002`.
- Primary first-baseline target **`forward_direction_15s`** — 3-class signed
  `{-1, 0, +1}`, zero class preserved.
- Horizon **15s** chosen over 60s on committed terminal-censor evidence (1s=3 /
  5s=20 / 15s=42 / 60s=216; 60s drops ~5× more terminal rows) and noise
  structure — a contract choice, **not** a performance claim.
- Secondary descriptive (not a model target): `forward_log_return_15s` for
  cost-context reporting only.
- `1s` / `5s` / `60s` contract-known but multi-horizon use deferred.

---

## 11. Feature scope

Exactly the **45** causal computed `FEATURE_SCHEMA_V002` columns (40 windowed +
3 time-context + 2 quality flags). No additions, no selection / ranking /
pruning, no PCA / embeddings, no raw prices unless a future revision explicitly
authorizes them.

---

## 12. Forbidden column policy

Exclude the **17 lineage columns**; exclude all label / support / split / censor
columns. Forbidden model-matrix substrings: `forward_log_return`,
`forward_direction`, `horizon_censored_flag`, `label_`, `split_`, `censored_`. A
forbidden-column substring scan over the assembled matrix must **fail closed**.

---

## 13. Filtering policy

For the active horizon (15s): drop null direction; drop null log-return where
required; drop `horizon_censored_flag_15s = true`; reject
`label_invalid_price_flag = true` (0 present by reference); never impute targets;
censored/invalid rows never enter any split; internal holdout dry-run only;
sealed test `test_rows_loaded = 0`. Record drop counts by split and reason.

---

## 14. Split binding

Import `pre_v002_split_policy.py`
(`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`); train 214 /
embargo 2024-10-01 / validation 45 / embargo 2024-11-16 / holdout 14 = 275;
assignment by `source_transact_time_ms` UTC date via `split_for_timestamp_ms`;
drop embargo; per-horizon earlier-split boundary protection; hard-raise on
out-of-segment / v002 / sealed dates; no shuffle / random / k-fold / bootstrap /
resampling.

---

## 15. Leakage / split-integrity proof obligations

Machine-checkable proof (with Phase 4bb-F sidecar): policy name; split module
path + commit SHA; 214/1/45/1/14 counts; no missing/duplicate/multi-assigned
dates; no embargo used; zero out-of-segment; `v002_terminal_window_read=false`;
`sealed_test_split_touched=false`; `test_rows_loaded=0`; no random/shuffle/
k-fold/bootstrap; per-horizon zero boundary-crossing rows; strict feature/label
key-alignment counts; null/censor/invalid drops by split; feature-column list
hash; forbidden-column scan empty; train-only transform provenance;
budget-preflight result; non-authorization flags all false.

---

## 16. Budget preflight obligations

Phase 4bn-L caps, fail-closed, recorded before any write: derived footprint warn
75 GiB / hard 125 GiB; total derived-stack warn 250 GiB / hard 300 GiB; runtime
warn 4 h / hard 8 h; temp warn 50 GiB / hard 100 GiB; `D:` ≥ 500 GiB before /
fail closed below 350 GiB during.

---

## 17. Output namespace posture

Future outputs (if separately authorized) local + gitignored only under
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`, each with a
Phase 4bb-F canonical sidecar. Not created / written / committed by this phase.
No research-eligibility implication; no `chronological_split_policy` set; no
`ml_authorized` / `diagnostics_authorized` transition.

---

## 18. Data read / created / blocked status

- **Any local data read?** **No.**
- **Any local data created?** **No.**
- **Data reads remain blocked?** **Yes** (`source_admissible_for_data_read =
  false`).
- **Dataset builder remains blocked?** **Yes**
  (`source_admissible_for_dataset_builder = false`).
- **ML remains blocked?** **Yes** (`ml_authorized = false`).

---

## 19. Result / decision

- **Result state:**
  `ML_DATASET_CONTRACT_RECORDED__PRE_V002_CONTRACT_ONLY__NO_DATA_READ__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_ML_DATASET_BUILDER_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Recommended state:** remain paused.
- **Alternative decision (if contract precise enough for code-only work but not
  data reads):**
  `RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

---

## 20. Boundary confirmations (non-authorizations)

- No acquisition, endpoint call, archive / CHECKSUM download, or HEAD preflight.
- No raw / normalization / feature / label execution or any layer-gate re-run.
- No local raw zip, normalized / feature / label Parquet, manifest, gate report,
  or sidecar read or inspected.
- No v002-terminal window read; no sealed-test read or touch
  (`test_rows_loaded = 0`).
- No storage migration; no database / `.duckdb` / `.sqlite`; no Parquet
  compaction; no v003.
- No manifest mutation; no `chronological_split_policy` set; no
  `research_eligible` flip; no `eligibility_gate_status` /
  `diagnostics_authorized` / `ml_authorized` transition.
- No `data/research` or `data/microstructure` artefact created or committed.
- No code, tests, scripts, or data files added; no existing source/test
  modified.
- No ML trained; no ML dataset created; no research matrix created; no model
  scored; no prediction generated; no diagnostics run; no strategy / signals /
  PnL / backtests.
- No successor authorized.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).
- Recorded v002 `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`, the Phase
  4bn-Y Candidate A policy, the Phase 4bn-AA split artefact, and the Phase
  4bn-AB source-admissibility posture preserved verbatim.

---

## 21. Successor authorization

**None.** Not authorized by this phase: any merge phase; an ML dataset builder
readiness memo; a code-only ML dataset builder skeleton; a source-admissibility
gate artefact; an ML dataset builder; a research matrix; any model / scoring /
prediction; any diagnostics; any strategy / signals / PnL / backtest; a
full-envelope reference / assembly memo; a holdout-boundary memo; a source-policy
documentation memo; a process-doc path update; any acquisition; any paper /
shadow / live / exchange-write / production-key; any Phase 5; any other
successor.

---

## 22. Recommended state

**Remain paused.** No next phase authorized.

---

## 23. Final git state

Reproduced in the final operator report (`git status --short`,
`git log --oneline -8 --decorate`, `git rev-parse HEAD`, `git rev-parse main`,
`git rev-parse origin/main`) so the operator need not run a separate status / SHA
check manually.
