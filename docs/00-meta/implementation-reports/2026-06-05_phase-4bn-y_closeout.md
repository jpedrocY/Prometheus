# Phase 4bn-Y — Closeout

## 1. Phase identity

- **Phase:** 4bn-Y — Chronological Split / Holdout Policy Memo.
- **Phase type:** docs-only split-policy / holdout-boundary /
  ML-admissibility-precondition / leakage-control memo.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
- **Branch-complete only:** not merged into `main`; not project-complete. Becomes
  project-complete only when a separately authorized merge phase records its
  merge-closeout on `main`.

---

## 2. SHAs

- **Branch:** `phase-4bn-y/chronological-split-holdout-policy-memo`.
- **Base `main` SHA:** `5d69e679b00783c1a2b37e4d6a80c64c2dd3782a`
  (`docs(phase-4bn-x): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 5d69e679…` verified.
- **Predecessors present on `main`:** Phase 4bn-X `5d69e67` / `af6387d` /
  `daee3df` / `d272dcd`; Phase 4bn-W `5bcae53`.
- **Branch commit SHA:** recorded in the final operator report (this closeout is
  committed in the same single commit `docs(phase-4bn-y): define chronological
  split holdout policy`).

---

## 3. Files created / modified

**Created (2):**

- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-y_chronological-split-holdout-policy.md`
  (23 sections).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-y_closeout.md` (this
  file).

**Modified narrowly (1):**

- `docs/00-meta/current-project-state.md` — additive only: one new Phase 4bn-Y
  paragraph + one new `Current phase:` block; all prior content preserved
  verbatim.

**No** code, tests, scripts, config, manifests, gate reports, sidecars, split
files, research matrices, ML configs, or data files were created or modified.

---

## 4. Validation commands run

- `git status --short` → only the three tracked Phase 4bn-Y docs files plus the
  pre-existing untracked `.claude/scheduled_tasks.lock`.
- `git diff --check` → clean (no whitespace errors).
- `git diff -- docs/00-meta/current-project-state.md docs/00-meta/implementation-reports/2026-06-05_phase-4bn-y_chronological-split-holdout-policy.md docs/00-meta/implementation-reports/2026-06-05_phase-4bn-y_closeout.md`
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

## 6. Selected split policy and boundaries

- **Selected policy:** Candidate A — conservative pre-v002-only chronological
  split with internal dry-run holdout (working name
  `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`; **not**
  implemented in code by this phase).
- **Train:** 2024-03-01 .. 2024-09-30 (214 UTC dates).
- **Embargo date:** 2024-10-01 (dropped).
- **Validation:** 2024-10-02 .. 2024-11-15 (45 UTC dates).
- **Embargo date:** 2024-11-16 (dropped).
- **Internal holdout / dry-run (not sealed test):** 2024-11-17 .. 2024-11-30
  (14 UTC dates).
- **Total:** 214 + 1 + 45 + 1 + 14 = **275** = full gated pre-v002 segment.
- **Assignment:** by `source_transact_time_ms` UTC date; chronological-only; no
  shuffle / random / k-fold / bootstrap.

---

## 7. Purge / embargo interval

- **Primary operational rule:** 1 full UTC date dropped at each internal boundary
  (2024-10-01, 2024-11-16), enforceable with daily partitions.
- **Formal floor:** ≥ 60 s row-level earlier-split embargo
  (`exclude_from_earlier_split`), matching/subsuming the locked v002
  `MIN_BOUNDARY_EMBARGO_SECONDS = 60`. The 1-day purge is explicitly more
  conservative than the 60 s label horizon (86,400 s ≫ 60 s).

---

## 8. Handling rules

- **v002 terminal (2024-12-01 .. 2025-02-28):** by reference only; unread;
  governed by the recorded `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`
  policy (preserved verbatim); inadmissible to the first ML-baseline path.
- **Published v002 labels:** by reference only; byte-for-byte immutable; unread.
- **Sealed test (2025-02-14 .. 2025-02-28):** fully sealed; `test_rows_loaded=0`;
  untouched; excluded from all training / validation / selection / tuning /
  design / rescue; single-use, future-authorization only.
- **Full-envelope reference / assembly:** not required for the conservative
  pre-v002-only path; required only before any future pre-v002 + v002 combined
  path; deferred and unauthorized here.
- **Censored labels:** no silent imputation; retain rows with null per-horizon
  labels; per-task drop of per-horizon nulls; exact filtering deferred to the ML
  readiness memo.
- **Invalid-price labels:** 0 present; future policy must explicitly
  reject/filter; never impute.

---

## 9. Future ML-readiness prerequisites

1. Docs-only ML-baseline readiness memo (per-task dataset construction).
2. Code-level pre-v002 split-policy artefact + offline tests (not created here).
3. Source admissibility resolved (segment currently `research_eligible=false` /
   `eligibility_gate_status=pending`; separate, unauthorized eligibility action).
4. Leakage / split-integrity proof (no boundary crossing; no shuffle; no
   v002/sealed access).
5. Budget preflight within Phase 4bn-L caps.

---

## 10. Result / decision

- **Result state:** `RECORD_CHRONOLOGICAL_SPLIT_POLICY__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_ML_BASELINE_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Recommended state:** remain paused.
- **MEMO RECORDED.**

---

## 11. Boundary confirmations

- No local data read; no local data created.
- No ML / diagnostics / strategy / signals / PnL / backtests.
- No acquisition, endpoint calls, archive download, or HEAD preflight.
- No raw / normalization / feature / label execution or any layer gate re-run.
- No local raw zip, normalized / feature / label Parquet, manifest, gate report,
  or sidecar read.
- No v002 terminal window read; no sealed-test read or touch.
- No storage migration; no database; no Parquet compaction; no v003.
- No manifest mutation; no `chronological_split_policy` set; no
  `research_eligible` flip; no `eligibility_gate_status` transition.
- No `data/research` or `data/microstructure` artefact created or committed.
- No code / tests / scripts added.
- No successor authorized.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).
- Recorded v002 `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` preserved
  verbatim.

---

## 12. Successor authorization

**None.** Not authorized by this phase: any merge phase; ML-baseline readiness
memo; full-envelope reference/assembly memo; holdout-boundary memo; source-policy
documentation memo; process-doc path update; any pre-v002 split-policy code
artefact; any ML implementation / model training / scoring / prediction; any
strategy / signals / PnL / backtest; any acquisition; any paper / shadow / live /
exchange-write / production-key; any Phase 5; any other successor.

---

## 13. Recommended state

**Remain paused.** No next phase authorized.

---

## 14. Final git state

Reproduced in the final operator report (`git status --short`,
`git log --oneline -8 --decorate`, `git rev-parse HEAD`, `git rev-parse main`,
`git rev-parse origin/main`) so the operator need not run a separate status / SHA
check manually.
