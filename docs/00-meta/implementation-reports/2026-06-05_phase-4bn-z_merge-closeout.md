# Phase 4bn-Z — Merge Closeout

## 1. Phase identity

- **Phase:** 4bn-Z — ML-Baseline Readiness Memo.
- **Phase type:** docs-only ML-readiness / dataset-contract /
  split-implementation-precondition / source-admissibility / leakage-control
  memo.
- **Merge purpose:** bring the branch-complete Phase 4bn-Z docs (ML-baseline
  readiness memo, closeout, narrow `current-project-state.md` update) onto
  `main`.
- **Source branch:** `phase-4bn-z/ml-baseline-readiness-memo`.
- **Target branch:** `main`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (determines ML
  implementation readiness and the prerequisites/leakage-control contract before
  any ML dataset / training path may be authorized).

---

## 2. SHAs

- **Pre-merge `main` / base SHA:** `896f5fa1aaccaa4ed8504e5d815929eeb50ca398`
  (`docs(phase-4bn-y): finalize merge closeout shas`).
- **Branch / docs commit SHA:** `bce8fb477c0fbcfe21e2309e9389819088a27534`
  (`docs(phase-4bn-z): assess ml baseline readiness`).
- **Merge commit SHA:** `12e50e8c042797359bc9d0274d441b5d9635e61a`
  (`docs(phase-4bn-z): merge ml baseline readiness`).
- **Merge-closeout commit SHA:** `268020a87eadef7cbf719cd265ffe8b662d7e67e`
  (`docs(phase-4bn-z): add merge closeout`).
- **SHA-finalization commit SHA:** this update
  (`docs(phase-4bn-z): finalize merge closeout shas`) — its exact SHA is the
  resulting `main` / `origin/main` tip, reproduced in the final operator report
  and `git log`.
- **Final `main` / `origin/main` SHA after push:** equal to the SHA-finalization
  commit SHA above; reproduced in the final operator report and `git log`.

---

## 3. Merge method

`git checkout main` → `git pull --ff-only origin main` (already up to date at
`896f5fa`) → `git merge --no-ff phase-4bn-z/ml-baseline-readiness-memo -m
"docs(phase-4bn-z): merge ml baseline readiness"`. Merge made by the `ort`
strategy; no conflicts. Push status recorded in §8 / final report.

---

## 4. Files brought forward by the merge

- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-z_ml-baseline-readiness-memo.md`
  (26 sections; 624 insertions).
- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-z_closeout.md`
  (226 insertions).
- **Modified (additive only):** `docs/00-meta/current-project-state.md`
  (133 insertions, 0 deletions; new Phase 4bn-Z paragraph + new `Current phase:`
  block; all prior content preserved verbatim).

**No** code, tests, scripts, config, `.gitignore`, `pyproject.toml`, README, MCP
file, manifest, sidecar, gate report, successor-state artefact, split file,
research matrix, ML config, model output, prediction output, or data file was
added or modified.

---

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 133 +++++
 .../2026-06-05_phase-4bn-z_closeout.md             | 226 ++++++++
 ...06-05_phase-4bn-z_ml-baseline-readiness-memo.md | 624 +++++++++++++++++++++
 3 files changed, 983 insertions(+)
```

983 insertions, 0 deletions.

---

## 6. Result / verdict

**MEMO RECORDED — MERGE COMPLETE.** Phase 4bn-Z is a docs-only ML-baseline
readiness memo. It concluded the project is **policy-ready but not
implementation-ready** for ML on the conservative pre-v002-only path, recorded
the six remaining prerequisites before ML training, settled the future allowed
source / split / label / feature / filtering scope, the future
leakage / split-integrity proof and budget-preflight requirements, and the
existing-tooling boundary, and recommended a narrow code-level pre-v002
split-policy artefact + offline tests as the next separately-authorized step.
With this merge, Phase 4bn-Z is **merge-complete on `main`**.

- **Result state:**
  `ML_BASELINE_READINESS_RECORDED__PRE_V002_PATH_READY_FOR_SPLIT_POLICY_ARTEFACT__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_PRE_V002_SPLIT_POLICY_ARTEFACT__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per the project convention, project completion also requires the
SHA-finalization commit (`docs(phase-4bn-z): finalize merge closeout shas`) that
fills the exact post-merge SHAs in §2; that commit is recorded below.

---

## 7. Readiness verdict (carried onto main)

**Policy-ready but NOT implementation-ready for ML on the conservative
pre-v002-only path.**

- **ML training ready:** **No.**
- **ML dataset creation ready:** **No.**
- **Research matrix creation ready:** **No.**
- **Code-level pre-v002 split-policy artefact required before any dataset
  builder:** **Yes.**
- **Source admissibility unresolved (a blocker for data use):** **Yes.**
- **Full-envelope assembly required for first conservative pre-v002-only path:**
  **No.**
- **Holdout-boundary memo required for first conservative pre-v002-only path:**
  **No.**

**Six remaining prerequisites before ML training:** (1) code-level pre-v002
split-policy artefact + offline tests; (2) explicit source-admissibility
resolution; (3) ML dataset contract / builder; (4) leakage / split-integrity
proof; (5) budget preflight for dataset construction; (6) per-task target /
horizon / filtering decision.

---

## 8. Validation results

- `git status --short` (post-merge) → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check` → clean.
- `git diff --name-status main..branch` (pre-merge) →
  `M current-project-state.md`, `A …_closeout.md`,
  `A …_ml-baseline-readiness-memo.md`.
- `git diff --stat main..branch` → 3 files, 983 insertions, 0 deletions.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- No markdown-lint tooling is repo-standard for these reports; none run (it would
  create / mutate nothing). No acquisition / raw / normalization / feature /
  label / gate / ML / diagnostics / backtest / strategy script was run; no
  endpoint called; no archive downloaded; no HEAD preflight; no local data read.

---

## 9. Local gitignored outputs

**None.** This phase created no `data/microstructure/` or `data/research/`
output and read none. `git check-ignore -v data/microstructure/` →
`.gitignore:85`; `git check-ignore -v data/research/` → `.gitignore:88`. The sole
untracked entry is the expected transient `.claude/scheduled_tasks.lock` (not
committed). No `data/microstructure` or `data/research` artefact was staged or
committed.

---

## 10. Upstream immutability / manifest state preservation

n/a — this phase reads and mutates no manifest, sidecar, gate report,
successor-state, or published dataset. The published `__v002`
raw / normalized / feature / label families remain byte-for-byte immutable and
unread. No manifest field was created, read, or mutated: `research_eligible` not
flipped; `eligibility_gate_status` not transitioned (remains `pending`);
`chronological_split_policy` **not** set in any manifest; `diagnostics_authorized`
/ `ml_authorized` not transitioned. The recorded v002
`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy
(`diagnostics_split_policy_v002.py`) and the Phase 4bn-Y Candidate A policy are
preserved verbatim and unmodified.

---

## 11. Boundary confirmations

- No local data read; no local data created.
- No split file, research matrix, ML dataset, ML config, manifest, gate report,
  sidecar, model, score, or prediction created.
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

## 12. Future-path ledger (carried onto main)

**Future allowed source scope (if ever separately authorized):** BTCUSDT /
Binance USDⓈ-M futures / aggTrades only; pre-v002 only, 2024-03-01 .. 2024-11-30
inclusive UTC (275 dates); Phase 4bn-S features + Phase 4bn-W labels only, after
admissibility is resolved; v002 terminal (2024-12-01 .. 2025-02-28) and sealed
test (2025-02-14 .. 2025-02-28) excluded; any other symbol / market / family /
external source excluded.

**Future split scope:** Phase 4bn-Y Candidate A exactly —
`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`; Train 2024-03-01
.. 2024-09-30 (214), embargo 2024-10-01, Validation 2024-10-02 .. 2024-11-15
(45), embargo 2024-11-16, internal holdout / dry-run 2024-11-17 .. 2024-11-30
(14); 214+1+45+1+14 = 275; assignment by `source_transact_time_ms` UTC date;
chronological-only; no random / shuffle / k-fold-over-time / bootstrap /
post-hoc resampling; 1 full UTC date dropped at each internal boundary plus a
formal ≥ 60 s row-level earlier-split floor.

**Future label / target scope:** family
`microstructure_labels_aggtrades_v001 @ v002`, `label_schema_version v001`;
horizons 1s / 5s / 15s / 60s available; initial framing the locked v002 3-class
signed direction `{-1, 0, +1}` and/or forward-log-return, **as targets only**;
recommend a narrow single horizon for a first baseline (no horizon selection or
training authorized); forbidden: barrier / stop / target-before-stop / MFE /
MAE / R-multiple / PnL / profit / loss / equity / position / strategy / signal /
prediction / score / model labels.

**Future feature scope:** only the 45 causal computed `FEATURE_SCHEMA_V002`
columns, after admissibility and dataset-contract resolution; exclude the 17
lineage columns, all label / support / split / censor columns, raw prices
(unless a future contract explicitly authorizes them), and any future-looking /
post-label column; only the two design quality flags retained inside the
45-column matrix; no extra support / quality field promoted without a future
dataset contract.

**Future censored / invalid filtering:** drop per-horizon null labels; drop
censored rows for the active horizon; reject invalid-price rows; never impute
censored or invalid targets; internal holdout is dry-run only; sealed test
remains `test_rows_loaded = 0`.

**Future leakage / split-integrity proof:** 214 / 1 / 45 / 1 / 14 date
assignment with no unassigned or double-assigned dates; zero earlier-split
boundary-crossing rows per horizon under the ≥ 60 s embargo + 1-day purge;
assignment a pure function of `source_transact_time_ms` UTC date; no RNG affects
split membership; `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`; `test_rows_loaded = 0`; hard raise on any
out-of-segment date; strict per-day positional feature/label alignment;
manifest / config-hash binding — feature manifest
`4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`,
`feature_config_hash
0726b41d48e5f7127728c385b150d90fad91a92b3400c0545649b541e4dd114c`, label manifest
`69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`,
`label_config_hash
b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`, gate reports
`db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08` /
`3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134` /
`ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984`; train-only
transform provenance.

**Future budget preflight (Phase 4bn-L caps; fail-closed before any write):**
derived footprint warn 75 GiB / hard 125 GiB; total derived-stack warn 250 GiB /
hard 300 GiB; runtime warn 4 h / hard 8 h; temp warn 50 GiB / hard 100 GiB; `D:`
≥ 500 GiB before; fail closed below 350 GiB during.

**Existing committed ML-baseline tooling boundary:** the Phase 4bn-B
`ml_baseline_design_v002.py` + `ml_baseline_dataset_v002.py` and Phase 4bm-W
`diagnostics_split_policy_v002.py` are hardcoded to the v002 terminal (90
partitions / 155,153,449 rows / `feature_config_hash 819cfa7a…` /
`label_config_hash 352bad41…` / dates 2024-12-01 .. 2025-02-28 / split
`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`) and are **inadmissible to
the pre-v002 segment**; `ml_baseline_splits.py` and `ml_baseline_train.py` do
not exist (no committed end-to-end trainer). A future pre-v002 path needs a new
segment-scoped split artefact (then dataset / training wrappers) per the Phase
4bn-O/S/W precedent.

**Selected next recommendation:** **Phase 4bn-AA — Pre-V002 Split-Policy
Artefact + Offline Tests** (working name; subject to separate operator
authorization) — pure code/tests, no data I/O, no local data read, no data
artefact creation, no manifest mutation, no eligibility transition, no
`chronological_split_policy` field set, no dataset builder, no research matrix,
no ML training, no diagnostics, no strategy/PnL/backtests; does not require
source admissibility first because it touches no data.

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
Phase 4bn-V label manifest/versioning; Phase 4bn-Y chronological split policy;
Phase 4am .. Phase 4bn-Y results — all preserved verbatim.

---

## 14. No-rescue / strict non-authorizations

This merge authorizes **none** of: a pre-v002 split-policy code artefact; a
source-admissibility memo/gate; an ML dataset contract memo; an ML dataset
builder; a research matrix; ML training; model scoring; predictions;
diagnostics; strategy / signals / PnL / backtests; a full-envelope
reference/assembly memo; a holdout-boundary memo; a source-policy documentation
memo; a process-doc `D:` path-string update; acquisition / endpoint calls /
archive download / HEAD preflight; eligibility flip or gate transition;
`chronological_split_policy` manifest mutation; storage migration; database
creation; Parquet compaction; v003; paper / shadow / live-readiness /
deployment / exchange-write / production-key / credentials / MCP / Graphify; any
Phase 5; any successor.

---

## 15. Successor authorization

**None.** No successor is authorized by this merge. A code-level pre-v002
split-policy artefact + offline tests (Phase 4bn-AA, working name) is
*recommended* but requires separate operator authorization.

---

## 16. Recommended state and final git state

**Recommended state: remain paused.** No next phase authorized.

**Next operator options:** remain paused; separately authorize the pre-v002
split-policy artefact + offline tests; separately authorize a source-admissibility
memo/gate; separately authorize an ML dataset contract memo; separately authorize
a full-envelope reference-assembly memo only if a future path combines pre-v002 +
v002 data; separately authorize a holdout-boundary memo only if a future scope
touches the v002 terminal or sealed-test dates; separately authorize a
source-policy documentation memo; separately authorize a process-doc `D:`
path-string update; or reject further ML-baseline successors and close the ML
arc. No ML / diagnostics / strategy / PnL / backtest / storage-migration / paper
/ shadow / live / exchange-write option is valid from this state unless
separately authorized after this merge.

Final `git status` / `git log` / SHAs are reproduced in the final operator report
so the operator need not run a separate status/SHA check manually.
