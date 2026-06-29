# Phase 4bn-AA — Merge Closeout

## 1. Phase identity

- **Phase:** 4bn-AA — Pre-V002 Split-Policy Artefact + Offline Tests.
- **Phase type:** pure-source split-policy artefact + offline unit tests + docs.
- **Merge purpose:** bring the branch-complete Phase 4bn-AA work (the pure
  pre-v002 split-policy source module, its offline test module, the
  implementation report, the closeout, and the narrow additive
  `current-project-state.md` update) onto `main`.
- **Source branch:** `phase-4bn-aa/pre-v002-split-policy-artefact`.
- **Target branch:** `main`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (operationalises an
  admissibility boundary — the split / holdout / embargo contract that any future
  ML-baseline work must obey; an error could silently corrupt downstream
  scientific meaning, even though the module performs no data I/O).

---

## 2. SHAs

- **Pre-merge `main` / base SHA:** `d9e699ea07d41a8d5492efdab8f6a1f74aae54e2`
  (`docs(phase-4bn-z): finalize merge closeout shas`).
- **Branch / code+docs commit SHA:** `e12e928e33aa84e530a85a1a58b04d6ac217b1fb`
  (`code(phase-4bn-aa): add pre-v002 split policy artefact`).
- **Merge commit SHA:** `451a51e9bd8c5711a147b095c6ec37989f725f66`
  (`code(phase-4bn-aa): merge pre-v002 split policy artefact`).
- **Merge-closeout commit SHA:** `6cfbf68783011ea67fbb752d27b3b49773a479c9`
  (`docs(phase-4bn-aa): add merge closeout`).
- **SHA-finalization commit SHA:** this update
  (`docs(phase-4bn-aa): finalize merge closeout shas`) — its exact SHA is the
  resulting `main` / `origin/main` tip, reproduced in the final operator report
  and `git log`.
- **Final `main` / `origin/main` SHA after push:** equal to the SHA-finalization
  commit SHA above; reproduced in the final operator report and `git log`.

---

## 3. Merge method

`git checkout main` → `git pull --ff-only origin main` (already up to date at
`d9e699e`) → `git merge --no-ff phase-4bn-aa/pre-v002-split-policy-artefact -m
"code(phase-4bn-aa): merge pre-v002 split policy artefact"`. Merge made by the
`ort` strategy; no conflicts. Push status recorded in the final operator report.

---

## 4. Files merged (brought forward by the merge)

- **Added:** `src/prometheus/research/microstructure/pre_v002_split_policy.py`
  (pure pre-v002 split-policy source module; 626 insertions).
- **Added:**
  `tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py`
  (offline unit-test module, 70 tests; 547 insertions).
- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-aa_pre-v002-split-policy-artefact.md`
  (22 sections; 452 insertions).
- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-aa_closeout.md`
  (206 insertions).
- **Modified (additive only):** `docs/00-meta/current-project-state.md`
  (97 insertions, 0 deletions; new Phase 4bn-AA paragraph + new `Current phase:`
  block; all prior content preserved verbatim).

**No** existing source or test was modified; no scripts, config, `.gitignore`,
`pyproject.toml`, README, MCP file, manifest, sidecar, gate report,
successor-state artefact, split file, research matrix, ML config, model output,
prediction output, or data file was added or modified.
`src/prometheus/research/microstructure/diagnostics_split_policy_v002.py` is
preserved verbatim (absent from the branch diff).

---

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  97 ++++
 .../2026-06-05_phase-4bn-aa_closeout.md            | 206 +++++++
 ..._phase-4bn-aa_pre-v002-split-policy-artefact.md | 452 +++++++++++++++
 .../microstructure/pre_v002_split_policy.py        | 626 +++++++++++++++++++++
 .../test_phase4bn_aa_pre_v002_split_policy.py      | 547 ++++++++++++++++++
 5 files changed, 1928 insertions(+)
```

1928 insertions, 0 deletions.

---

## 6. Result / verdict

**ARTEFACT IMPLEMENTED — NO DATA I/O — MERGE COMPLETE.** Phase 4bn-AA is a
pure-source split-policy artefact + offline tests + docs phase. It
operationalised the Phase 4bn-Y **Candidate A** chronological split / holdout
policy exactly as pure date / window arithmetic, added one pure source module
(import-only `datetime`), added one offline test module (70 tests), and made a
narrow additive `current-project-state.md` update. It read no local data, created
no local data, performed no data I/O, modified no existing source / test, and
authorized no successor. With this merge, Phase 4bn-AA is **merge-complete on
`main`**.

- **Result state:**
  `PRE_V002_SPLIT_POLICY_ARTEFACT_IMPLEMENTED__NO_DATA_IO__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_SOURCE_ADMISSIBILITY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per the project convention, project completion also requires the
SHA-finalization commit (`docs(phase-4bn-aa): finalize merge closeout shas`) that
fills the exact post-merge SHAs in §2; that commit is recorded below and in the
final operator report.

---

## 7. Module / API / policy summary (carried onto main)

- **Module path:** `src/prometheus/research/microstructure/pre_v002_split_policy.py`.
- **Test path:** `tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py`.
- **Policy name:** `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`.
- **Public API added:** `PreV002SplitPolicyError`; split labels `TRAIN` /
  `VALIDATION` / `HOLDOUT` / `EMBARGO`; policy / date / boundary / embargo /
  horizon constants; `split_for_date`, `split_for_timestamp_ms`, `is_train_date`,
  `is_validation_date`, `is_holdout_date`, `is_embargo_date`,
  `is_model_eligible_split`, `policy_date_inventory`, `validate_horizon_ms`,
  `earlier_split_embargo_window_ms`, `is_embargoed`,
  `is_earlier_split_boundary_crossing`, `boundary_crossing_window_ms`,
  `validate_policy_arithmetic`, `build_split_policy_contract`; stable `__all__`.

**Encoded split:**

| Split | UTC date range (inclusive) | Dates |
|---|---|---|
| Train | 2024-03-01 .. 2024-09-30 | 214 |
| Embargo | 2024-10-01 | 1 (dropped) |
| Validation | 2024-10-02 .. 2024-11-15 | 45 |
| Embargo | 2024-11-16 | 1 (dropped) |
| Internal holdout / dry-run | 2024-11-17 .. 2024-11-30 | 14 |
| **Total** | 2024-03-01 .. 2024-11-30 | **275** |

214 + 1 + 45 + 1 + 14 = 275 = full gated pre-v002 segment.

- **Assignment rule:** by `source_transact_time_ms` UTC date; chronological-only;
  no shuffle / random / k-fold-over-time / bootstrap / post-hoc temporal
  resampling; no RNG.
- **Embargo rule:** one full UTC date dropped at each internal boundary
  (2024-10-01, 2024-11-16) over a formal ≥ 60 s row-level earlier-split floor
  (`MIN_BOUNDARY_EMBARGO_MS = 60000`; `MAX_LABEL_HORIZON_MS = 60000`; one-day
  purge 86,400 s strictly dominates the 60 s max horizon); embargo applies to the
  earlier split only; HOLDOUT (latest split) never embargoes itself.
- **Boundary timestamps:** `BOUNDARY_TRAIN_VALIDATION_MS = 1727827200000`
  (2024-10-02T00:00:00Z); `BOUNDARY_VALIDATION_HOLDOUT_MS = 1731801600000`
  (2024-11-17T00:00:00Z).
- **Boundary-crossing helper:** for row timestamp `T` and horizon `H` — TRAIN
  crosses iff `T + H ≥ 1727827200000`; VALIDATION crosses iff
  `T + H ≥ 1731801600000`; HOLDOUT never crosses (no later pre-v002 split);
  EMBARGO rows raise; out-of-segment timestamps raise; horizon ∉ {1000, 5000,
  15000, 60000} raises. No real earlier-split row can cross because the 1-day
  purge dominates the 60 s max horizon.
- **v002 terminal exclusion:** every date 2024-12-01 .. 2025-02-28 raises
  `PreV002SplitPolicyError`; assigned to no split; unread.
- **Sealed-test exclusion:** every date 2025-02-14 .. 2025-02-28 raises
  `PreV002SplitPolicyError`; `test_rows_loaded = 0`; untouched; internal holdout
  recorded as `holdout_is_sealed_test = False`.

---

## 8. No-data-I/O confirmation

The module imports only `datetime` (plus `from __future__ import annotations`).
It performs no file I/O, opens no path, uses no network, uses no RNG, and imports
no pandas / pyarrow / polars / numpy. It declares no `data/microstructure` or
`data/research` path token. `build_split_policy_contract()` returns an in-memory
dict and writes nothing. A source-token hygiene test asserts the absence of all
forbidden imports / path tokens, so the no-I/O, no-RNG, no-data-path posture is
itself test-enforced.

---

## 9. Validation results

- `ruff check src/prometheus/research/microstructure/pre_v002_split_policy.py tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py`
  → **All checks passed** (re-run at merge review).
- `python -m pytest tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py -q`
  → **70 passed** (re-run at merge review).
- `python -m mypy src/prometheus/research/microstructure/pre_v002_split_policy.py`
  → **0 direct errors in the new module.** mypy surfaced **29 pre-existing,
  unrelated** errors transitively from sibling committed modules
  (`labels_compute.py`, `features_compute.py`, `features_compute_v002.py`,
  `labels_manifest_v002.py`, `multiday_feature_gate_checks.py`); checking
  `labels_compute.py` alone reproduces the same 29, confirming they pre-date this
  phase. **The new module introduced none.**
- `git diff --check` → clean.
- `git diff --name-status main..branch` (pre-merge) → `M current-project-state.md`,
  `A …_closeout.md`, `A …_pre-v002-split-policy-artefact.md`,
  `A pre_v002_split_policy.py`, `A test_phase4bn_aa_pre_v002_split_policy.py`.
- `git diff --stat main..branch` → 5 files, 1928 insertions, 0 deletions.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` (post-merge) → only `?? .claude/scheduled_tasks.lock`.
- No acquisition / raw / normalization / feature / label / gate / ML /
  diagnostics / backtest / strategy script was run; no endpoint called; no
  archive downloaded; no HEAD preflight; no local data read.

---

## 10. Local gitignored outputs

**None.** This phase created no `data/microstructure/` or `data/research/` output
and read none. `git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. The sole untracked entry
is the expected transient `.claude/scheduled_tasks.lock` (not committed). No
`data/microstructure` or `data/research` artefact was staged or committed.

---

## 11. Upstream immutability / manifest state preservation

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

## 12. Boundary confirmations

- No local data read; no local data created.
- No split file, research matrix, ML dataset, ML config, manifest, gate report,
  sidecar, model, score, or prediction created.
- No existing source / test / script / config modified; no new scripts or data
  files added.
- No local raw zip, normalized / feature / label Parquet, manifest, gate report,
  or sidecar under `data/microstructure/` read or inspected.
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

## 13. Future-path ledger (carried onto main)

Phase 4bn-AA satisfies the first of the six Phase 4bn-Z ML-training
prerequisites (the code-level pre-v002 split-policy artefact + offline tests).
**Remaining blockers before any ML dataset creation** (each requiring separate
operator authorization): (1) **source admissibility** resolved (segment remains
`research_eligible=false` / `eligibility_gate_status=pending` at every layer);
(2) an **ML dataset contract / builder** with its **leakage / split-integrity
proof**; (3) a **budget preflight** within the Phase 4bn-L caps; (4) a **per-task
target / horizon / filtering decision**. A committed end-to-end trainer still
does not exist and would be a later, separately-authorized phase even after
(1)–(4). The recommended next blocker is **source admissibility**.

The future allowed source scope remains: BTCUSDT / Binance USDⓈ-M futures /
aggTrades only; pre-v002 only (2024-03-01 .. 2024-11-30; 275 dates); Phase 4bn-S
features + Phase 4bn-W labels only, after admissibility is resolved; v002 terminal
(2024-12-01 .. 2025-02-28) and sealed test (2025-02-14 .. 2025-02-28) excluded.

---

## 14. Retained verdict ledger and preserved project locks

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
Phase 4bn-Z ML-baseline readiness memo; Phase 4am .. Phase 4bn-Z results — all
preserved verbatim.

---

## 15. No-rescue / strict non-authorizations

This merge authorizes **none** of: a source-admissibility memo/gate; an ML
dataset contract memo; an ML dataset builder readiness memo; an ML dataset
builder; a research matrix; ML training; model scoring; predictions; diagnostics;
strategy / signals / PnL / backtests; a full-envelope reference/assembly memo; a
holdout-boundary memo; a source-policy documentation memo; a process-doc `D:`
path-string update; acquisition / endpoint calls / archive download / HEAD
preflight; eligibility flip or gate transition; `chronological_split_policy`
manifest mutation; storage migration; database creation; Parquet compaction;
v003; paper / shadow / live-readiness / deployment / exchange-write /
production-key / credentials / MCP / Graphify; any Phase 5; any successor.

---

## 16. Successor authorization

**None.** No successor is authorized by this merge. A docs-only
**source-admissibility memo/gate** is *recommended* as the next blocker but
requires separate operator authorization.

---

## 17. Recommended state and final git state

**Recommended state: remain paused.** No next phase authorized.

**Next operator options:** remain paused; separately authorize a
source-admissibility memo/gate (recommended); separately authorize an ML dataset
contract memo; separately authorize an ML dataset builder readiness memo;
separately authorize a full-envelope reference-assembly memo only if a future
path combines pre-v002 + v002 data; separately authorize a holdout-boundary memo
only if a future scope touches the v002 terminal or sealed-test dates; separately
authorize a source-policy documentation memo; separately authorize a process-doc
`D:` path-string update; or reject further ML-baseline successors and close the
ML arc. No ML / diagnostics / strategy / PnL / backtest / storage-migration /
paper / shadow / live / exchange-write option is valid from this state unless
separately authorized after this merge.

Final `git status` / `git log` / SHAs are reproduced in the final operator report
so the operator need not run a separate status/SHA check manually.
