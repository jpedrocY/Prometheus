# Phase 4bn-Y — Merge Closeout

## 1. Phase identity

- **Phase:** 4bn-Y — Chronological Split / Holdout Policy Memo.
- **Phase type:** docs-only split-policy / holdout-boundary /
  ML-admissibility-precondition / leakage-control memo.
- **Merge purpose:** bring the branch-complete Phase 4bn-Y docs (split/holdout
  policy memo, closeout, narrow `current-project-state.md` update) onto `main`.
- **Source branch:** `phase-4bn-y/chronological-split-holdout-policy-memo`.
- **Target branch:** `main`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (defines an
  ML-admissibility / leakage-control boundary contract).

---

## 2. SHAs

- **Pre-merge `main` / base SHA:** `5d69e679b00783c1a2b37e4d6a80c64c2dd3782a`
  (`docs(phase-4bn-x): finalize merge closeout shas`).
- **Branch / docs commit SHA:** `f4d4b5dd3df44c78087d2214790b8542da6c74ba`
  (`docs(phase-4bn-y): define chronological split holdout policy`).
- **Merge commit SHA:** `69005a46a46addf703bbe470e3382f72cbf3dabb`
  (`docs(phase-4bn-y): merge chronological split holdout policy`).
- **Merge-closeout commit SHA:** `e55e5a84b57d312f4e5f6e10a29ff69a276532e1`
  (`docs(phase-4bn-y): add merge closeout`).
- **SHA-finalization commit SHA:** this commit
  (`docs(phase-4bn-y): finalize merge closeout shas`) — its exact SHA is the
  resulting `main` / `origin/main` tip, reproduced in the final operator report
  and `git log`.
- **Final `main` / `origin/main` SHA after push:** equal to the SHA-finalization
  commit SHA above; reproduced in the final operator report and `git log`.

---

## 3. Merge method

`git checkout main` → `git pull --ff-only origin main` (already up to date at
`5d69e67`) → `git merge --no-ff phase-4bn-y/chronological-split-holdout-policy-memo
-m "docs(phase-4bn-y): merge chronological split holdout policy"`. Merge made by
the `ort` strategy; no conflicts. Push status recorded in §8 / final report.

---

## 4. Files brought forward by the merge

- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-y_chronological-split-holdout-policy.md`
  (23 sections; 596 insertions).
- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-y_closeout.md`
  (189 insertions).
- **Modified (additive only):** `docs/00-meta/current-project-state.md`
  (128 insertions, 0 deletions; new Phase 4bn-Y paragraph + new `Current phase:`
  block; all prior content preserved verbatim).

**No** code, tests, scripts, config, `.gitignore`, `pyproject.toml`, README, MCP
file, manifest, sidecar, gate report, successor-state artefact, split file,
research matrix, ML config, or data file was added or modified.

---

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 128 +++++
 ...ase-4bn-y_chronological-split-holdout-policy.md | 596 +++++++++++++++++++++
 .../2026-06-05_phase-4bn-y_closeout.md             | 189 +++++++
 3 files changed, 913 insertions(+)
```

913 insertions, 0 deletions.

---

## 6. Result / verdict

**MEMO RECORDED — MERGE COMPLETE.** Phase 4bn-Y is a docs-only chronological
split / holdout policy memo. It selected **Candidate A** (conservative
pre-v002-only chronological split with internal dry-run holdout), recorded the
purge/embargo, sealed-test, v002-terminal, published-v002-label, full-envelope,
censored-label, and invalid-label handling rules, and the future ML-readiness
prerequisites. With this merge, Phase 4bn-Y is **merge-complete on `main`**.

- **Result state:** `RECORD_CHRONOLOGICAL_SPLIT_POLICY__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_ML_BASELINE_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per the project convention, project completion also requires the
SHA-finalization commit (`docs(phase-4bn-y): finalize merge closeout shas`) that
fills the exact post-merge SHAs in §2; that commit is recorded below.

---

## 7. Local gitignored outputs

**None.** This phase created no `data/microstructure/` or `data/research/`
output and read none. `git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. The sole untracked entry
is the expected transient `.claude/scheduled_tasks.lock` (not committed).

---

## 8. Validation results

- `git status --short` (post-merge) → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check` → clean.
- `git diff --name-status main..branch` (pre-merge) → `M current-project-state.md`,
  `A …_chronological-split-holdout-policy.md`, `A …_closeout.md`.
- `git diff --stat main..branch` → 3 files, 913 insertions, 0 deletions.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- No markdown-lint tooling is repo-standard for these reports; none run (it would
  create / mutate nothing). No acquisition / raw / normalization / feature /
  label / gate / ML / diagnostics / backtest / strategy script was run; no
  endpoint called; no archive downloaded; no HEAD preflight.

---

## 9. Upstream immutability evidence

n/a — this phase reads and mutates no manifest, sidecar, gate report,
successor-state, or published dataset. The published `__v002`
raw / normalized / feature / label families remain byte-for-byte immutable and
unread.

---

## 10. Manifest state preservation

n/a — no manifest field was created, read, or mutated. In particular:
`research_eligible` not flipped; `eligibility_gate_status` not transitioned
(remains `pending`); `chronological_split_policy` **not** set in any manifest;
`diagnostics_authorized` / `ml_authorized` not transitioned. The recorded v002
`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy
(`diagnostics_split_policy_v002.py`) is preserved verbatim and unmodified.

---

## 11. Boundary confirmations

- No local data read; no local data created.
- No split file, research matrix, ML config, manifest, gate report, or sidecar
  created.
- No code / tests / scripts / config added.
- No local raw zip, normalized / feature / label Parquet, manifest, gate report,
  or sidecar under `data/microstructure/` read.
- No v002 terminal window read; no sealed-test read or touch
  (`test_rows_loaded = 0`).
- No ML / diagnostics / strategy / signals / PnL / backtests.
- No acquisition, endpoint call, archive download, or HEAD preflight.
- No storage migration; no database; no Parquet compaction; no v003.
- No `data/microstructure` or `data/research` artefact staged or committed.
- `.claude/scheduled_tasks.lock` remains untracked and uncommitted.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).

---

## 12. Selected policy ledger (carried onto main)

- **Selected split policy:** Candidate A — conservative pre-v002-only
  chronological split with internal dry-run holdout (working name
  `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`; recorded as a
  future code-level artefact name — **not implemented in code** by Phase 4bn-Y).
- **Train:** 2024-03-01 .. 2024-09-30 inclusive UTC (214 dates).
- **Embargo / purge date:** 2024-10-01 (dropped).
- **Validation:** 2024-10-02 .. 2024-11-15 inclusive UTC (45 dates).
- **Embargo / purge date:** 2024-11-16 (dropped).
- **Internal holdout / dry-run (NOT the sealed test):** 2024-11-17 .. 2024-11-30
  inclusive UTC (14 dates).
- **Total arithmetic:** 214 + 1 + 45 + 1 + 14 = **275** = full gated pre-v002
  segment (2024-03-01 .. 2024-11-30).
- **Assignment clock:** `source_transact_time_ms` UTC date.
- **Split mode:** chronological-only; no random / shuffle / k-fold-over-time /
  bootstrap / post-hoc temporal resampling.
- **Purge / embargo:** 1 full UTC date dropped at each internal boundary
  (2024-10-01, 2024-11-16); formal floor ≥ 60 s row-level earlier-split embargo
  (max label horizon = 60 s). Rationale: 1 day = 86,400 s ≫ 60 s, strictly more
  conservative than the horizon and trivially enforceable with daily partitions;
  consistent with and stronger than the recorded v002
  `MIN_BOUNDARY_EMBARGO_SECONDS = 60`. Future sub-day tooling must still enforce
  the ≥ 60 s row-level floor.
- **v002 terminal (2024-12-01 .. 2025-02-28):** by reference only; unread;
  governed by the recorded v002 policy; inadmissible to the first ML-baseline
  path.
- **Published v002 labels:** by reference only; byte-for-byte immutable; unread.
- **Sealed test (2025-02-14 .. 2025-02-28):** fully sealed; `test_rows_loaded=0`;
  untouched; excluded from all training / validation / model selection /
  hyperparameter / threshold tuning / feature selection / strategy design /
  diagnostic iteration / eligibility rescue; future single-use authorization
  only. The pre-v002 internal holdout is **not** the sealed test.
- **Full-envelope reference / assembly:** not required for the conservative
  pre-v002-only path; required later only for any pre-v002 + v002 combined path
  (or any v002-terminal row admission); deferred and unauthorized.
- **Censored labels:** no silent imputation; retain rows with null per-horizon
  labels; future ML dataset drops per-horizon null targets; exact per-task
  filtering deferred to a future ML-baseline readiness memo.
- **Invalid-price labels:** 0 present; future policy must explicitly
  reject / filter; never impute.
- **Future ML-readiness prerequisites:** (1) docs-only ML-baseline readiness
  memo; (2) code-level pre-v002 split-policy artefact + offline tests; (3) source
  admissibility resolved (segment `research_eligible=false` /
  `eligibility_gate_status=pending`; separate unauthorized eligibility action);
  (4) leakage / split-integrity proof; (5) budget preflight within Phase 4bn-L
  caps.
- **Selected conclusions:** no full-envelope reference/assembly is required
  before the first conservative pre-v002-only readiness path; no holdout-boundary
  memo is required for this pre-v002-only split (it touches no v002-terminal or
  sealed-test scope); a docs-only ML-baseline readiness memo is the recommended
  next separately authorized step.

---

## 13. Retained verdict ledger and preserved project locks

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread /
V2 / G1 / C1) and every project lock is preserved verbatim: §11.6 = 8 bps per
side / round-trip 16 bps; §1.7.3 0.25% / 2× / one-position / mark-price stops;
Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11;
Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 + post-null
cooldown; Phase 4al refined no-rescue + §13 boundary + §14 hierarchy; Phase 4aw
always-raises invariant; Phase 4bb-F canonical path policy; Phase 4bl-F risk
tiers; Phase 4bm-U / 4bm-W v002 split policy; Phase 4bn-L budgets; Phase 4bn-N
normalization manifest/versioning; Phase 4bn-R feature manifest/versioning;
Phase 4bn-V label manifest/versioning; Phase 4am .. Phase 4bn-X results — all
preserved verbatim.

---

## 14. No-rescue / strict non-authorizations

This merge authorizes **none** of: ML-baseline readiness memo; ML training; ML
dataset creation; research matrix creation; diagnostics; strategy / signals /
PnL / backtests; any pre-v002 split-policy code artefact; full-envelope
reference/assembly memo; holdout-boundary memo; source-policy documentation memo;
process-doc path update; acquisition / endpoint calls / archive download / HEAD
preflight; eligibility flip or gate transition; `chronological_split_policy`
manifest mutation; storage migration; database creation; Parquet compaction;
v003; paper / shadow / live-readiness / deployment / exchange-write /
production-key / credentials / MCP / Graphify; any Phase 5; any successor.

---

## 15. Successor authorization

**None.** No successor is authorized by this merge. A docs-only ML-baseline
readiness memo is *recommended* but requires separate operator authorization.

---

## 16. Recommended state and final git state

**Recommended state: remain paused.** No next phase authorized.

Final `git status` / `git log` / SHAs are reproduced in the final operator report
so the operator need not run a separate status/SHA check manually.
