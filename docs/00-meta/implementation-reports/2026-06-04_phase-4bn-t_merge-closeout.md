# Phase 4bn-T — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-T — Feature-Layer Eligibility Gate for the Pre-V002
  BTCUSDT aggTrades Feature Segment.
- **Type:** feature-layer eligibility gate / local gitignored feature artefact
  validation / code + tests + docs + local gate-report.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-T bounded read-only feature-layer gate
  runner (`scripts/phase4bn_t_validate_feature_pre_v002_gate.py`), its offline
  test module, the implementation report, the branch closeout, and the narrow
  `current-project-state.md` update onto `main` as project state. The phase ran
  a read-only feature-layer eligibility gate over the Phase 4bn-S local,
  gitignored, non-eligible pre-v002 BTCUSDT Binance USDⓈ-M futures aggTrades
  feature segment (2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates;
  400,001,695 feature rows) and emitted one local gitignored gate report +
  canonical sidecar. The gate **PASSED** (27 / 27 checks); it flipped no
  eligibility and authorized no successor.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-t/feature-layer-eligibility-gate`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section
  merge-closeout required).

## 2. SHAs

- **`main` SHA before merge:** `e647435c81d784f610b9cf8b5e2f2dc8ee0e914e`
  (`docs(phase-4bn-s): finalize merge closeout shas`).
- **Branch commit SHA (code + tests + docs):**
  `b9843bd78bba8554c80de443ceda0aa3401fcf75`
  (`data(phase-4bn-t): gate feature pre-v002 segment`).
- **Merge commit SHA:** `8149750801fdf8bad219f1baba1614d9c36e068b`
  (`data(phase-4bn-t): merge feature-layer eligibility gate`).
- **Merge-closeout commit SHA:** this commit
  (`docs(phase-4bn-t): add merge closeout`) — recorded in the final operator
  report.
- **SHA-finalization commit SHA:** the subsequent
  `docs(phase-4bn-t): finalize merge closeout shas` commit — its own hash becomes
  the new `main` tip; recorded verbatim in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization commit;
  `main == origin/main` after push (recorded in the final operator report).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `data(phase-4bn-t): merge feature-layer eligibility gate`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
  (recorded at the final operator report after the SHA-finalization commit).

## 4. Files brought forward by the merge

- **Docs (3):**
  - `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-T
    paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-S
    paragraphs and blocks preserved verbatim as labelled historical context;
    92 insertions, 0 deletions — insertion-only);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-t_feature-layer-eligibility-gate.md`
    (added — the implementation report, 25 sections);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-t_closeout.md`
    (added — branch closeout).
- **Scripts (1):** `scripts/phase4bn_t_validate_feature_pre_v002_gate.py` (added
  — the bounded read-only feature-layer gate runner; reuses the locked generic
  SHA / sidecar / path primitives and the locked `FEATURE_SCHEMA_V002` constants
  unchanged).
- **Tests (1):**
  `tests/research/microstructure/test_phase4bn_t_feature_layer_gate.py` (added —
  31 offline tests).
- **Source / config:** none.
- **`data/microstructure/` files:** **none modified or committed.** No
  `data/research/` file. No published manifest, sidecar, prior gate report,
  successor-state artefact, `.gitignore`, `pyproject.toml`, `README.md`, or MCP
  file was modified. No locked prior-phase script and no source module was
  modified.

The diff matches the expected change set from the merge authorization prompt
exactly (add 4 files, modify 1 doc).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |   92 ++
 .../2026-06-04_phase-4bn-t_closeout.md             |  115 +++
 ...4_phase-4bn-t_feature-layer-eligibility-gate.md |  386 ++++++++
 .../phase4bn_t_validate_feature_pre_v002_gate.py   | 1009 ++++++++++++++++++++
 .../test_phase4bn_t_feature_layer_gate.py          |  702 ++++++++++++++
 5 files changed, 2304 insertions(+)
```

The diff matches the expected change set (insertion-only; code + tests + docs;
no data).

## 6. Result / verdict

**GATE PASS — LOCAL FEATURE SEGMENT NON-ELIGIBLE — REMAIN PAUSED.** Phase 4bn-T
ran a bounded, read-only feature-layer eligibility gate over the Phase 4bn-S
local feature pre-v002 segment and emitted result state
`FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`
with **27 / 27 checks PASS** in 348.9 s. The gate streamed the SHA256 of every
one of the 275 feature Parquet (each matched its canonical two-space `.sha256`
sidecar and the manifest `per_file_inventory`), validated 275 contiguous
in-segment dates (2024-03-01 .. 2024-11-30; no date ≥ 2024-12-01; no
sealed-test date), the exact segment path layout +
`BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet` basename, the feature segment
manifest SHA256 (`4881eb87…4599b52`) + sidecar (`f2ca2f48…92e5`), the Phase
4bn-R required-field contract and forbidden-field absence, the locked 62-column
`FEATURE_SCHEMA_V002` (17 lineage + 45 feature/quality; metadata for all 275 +
identity-column deep checks on a 10-date sample), the causal kernel policy
(`leakage_policy=causal_only_no_future_lookahead`,
`cross_day_lookback_policy=causal_cross_day_lookback`,
`cross_day_tail_buffer_ms=60000`; sampled `feature_timestamp_ms ==
source_transact_time_ms`), adjacent-date non-overlap for all 274 pairs,
recomputed total rows = **400,001,695** (exact) and footprint (parquet + sidecar
bytes) = **54,254,406,538 B** (exact), and predecessor integrity (Phase 4bn-O
normalized segment manifest `0e96ae37…d9fa` + sidecar `5d7dcbef…6402`; Phase
4bn-P normalized-layer gate report `3452fd9d…f134`, verdict
`NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`,
25 / 25 PASS). Result state
`FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
decision
`RECOMMEND_AUTHORIZE_LABEL_DERIVATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
The merge lands the gate runner + tests + report + closeout + narrow state
update on `main`; the project remains paused; the segment remains non-eligible. A
passing feature-layer gate does **not** make the dataset research-eligible.

## 7. Local gitignored outputs (produced by the phase; NOT committed)

One gate report + canonical sidecar, produced by the real gate run; local,
gitignored (`.gitignore:85`, `data/microstructure/`), uncommitted, and confirmed
not staged. `git check-ignore -v data/microstructure/` → `.gitignore:85`.

- **Gate report**
  `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s__phase-4bn-t__1780674917156__e647435c81d7.json`
  — SHA256 `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`;
  not committed.
- **Gate report sidecar**
  `…__phase-4bn-t__1780674917156__e647435c81d7.json.sha256`
  — SHA256 `12d2e437f444f8445306f6c3eebbf77821d59428d23dc621f3e39a541bd986ea`;
  canonical two-space body, LF, no BOM; not committed.
- **Gate result:** 27 / 27 checks PASS; **runtime:** 348.9 s.
- **Recorded in the report:** `phase = phase-4bn-t`; `base_commit_sha =
  e647435c81d784f610b9cf8b5e2f2dc8ee0e914e`; `segment_non_eligible = true`;
  `research_eligible_after = false`; `eligibility_gate_status_after = pending`;
  `no_successor_authorization = true`; `feature_execution_rerun = false`;
  `v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
  `published_v002_mutated = false`; `data_committed = false`.
- **Source artefacts referenced by the report (read-only):** Phase 4bn-S feature
  segment manifest SHA256 `4881eb87…4599b52`; Phase 4bn-O normalized segment
  manifest SHA256 `0e96ae37…d9fa`; Phase 4bn-P normalized-layer gate report
  SHA256 `3452fd9d…f134`.

The pre-existing Phase 4bn-S feature outputs (275 Parquets + 275 sidecars + the
feature segment manifest + sidecar), the Phase 4bn-O normalized outputs, and the
Phase 4bn-P normalized-layer gate report remain local, gitignored, and
uncommitted.

## 8. Validation results

Merge-review validation (no real feature-layer gate rerun; no gate / feature
execution / normalization / acquisition run):

- `git diff --check` → clean (no whitespace errors).
- `git diff --name-status main..branch` (pre-merge) → exactly the 5 expected
  files (M `current-project-state.md`; A closeout; A implementation report; A
  script; A test).
- `git diff --stat main..branch` (pre-merge) → `5 files changed, 2304
  insertions(+)`.
- `ruff check scripts/phase4bn_t_validate_feature_pre_v002_gate.py
  tests/research/microstructure/test_phase4bn_t_feature_layer_gate.py` → All
  checks passed.
- `pytest tests/research/microstructure/test_phase4bn_t_feature_layer_gate.py`
  → 31 passed.
- `pytest` (predecessor set: Phase 4bn-S feature + 4bn-P normalized-layer gate +
  4bn-O normalization) → **88 passed**.
- `mypy src/prometheus` (repo-standard gate; `files = ["src/prometheus"]`) →
  **96 errors in 12 files (checked 149 source files)**, **identical to `main`**:
  Phase 4bn-T added no file under `src/prometheus` and modified no source module,
  so the mypy surface is unchanged and **zero** new errors were introduced. The
  new gate runner lives under `scripts/`, which is out of mypy scope by repo
  convention; no mypy gate applies to it.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only `.claude/scheduled_tasks.lock` untracked; no
  `data/microstructure/` or `data/research/` artefact staged or committed; the
  merge commit committed exactly the 5 tracked files (no `data/` file).
- The real feature-layer gate was run once on the branch (not rerun at merge):
  27 / 27 checks PASS; runtime 348.9 s; one gitignored gate report + canonical
  sidecar written; no feature execution rerun; no `.duckdb` / `.sqlite`; no v003
  path; no `data/research` output; published feature `__v002` neither read nor
  mutated; v002 terminal raw/normalized window and sealed-test split untouched.

## 9. Upstream immutability evidence

The Phase 4bn-T gate is read-only on all data artefacts; it opened the Phase
4bn-S feature artefacts, the Phase 4bn-O normalized segment manifest + sidecar,
and the Phase 4bn-P normalized-layer gate report for hashing only and wrote
nothing back to them. SHA pins verified during the gate run (read-only):

- Phase 4bn-S feature segment manifest
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  — SHA256 `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`
  (matched expected; not mutated).
- Phase 4bn-O normalized segment manifest
  — SHA256 `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa`
  (+ sidecar `5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402`;
  matched expected; not mutated).
- Phase 4bn-P normalized-layer gate report
  — SHA256 `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`
  (matched expected; verdict + 25/25 PASS confirmed; not mutated).
- All 275 feature Parquet files — each SHA256 matched its canonical sidecar and
  the segment manifest inventory (read-only verification).

The published normalized `__v002` family, the published feature `__v002`
manifest
(`data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`)
and Parquet family, the v002 terminal raw/normalized window, and the sealed-test
split were neither read nor mutated. The merge modified no `data/microstructure/`
file.

## 10. Manifest state preservation

- **Source Phase 4bn-O normalized segment manifest:** `research_eligible:
  false`, `eligibility_gate_status: "pending"`; unchanged — no transition.
- **Gated Phase 4bn-S feature segment manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`, `no_successor_authorization: true`,
  `source_eligibility_posture: "non_eligible_gate_passed_pending"`; 18-key
  boundary confirmations all true; 8-flag non-authorization set all false; no
  `chronological_split_policy` field; governance labels mark
  labels/ml/diagnostics/strategy/backtest = forbidden, acquisition =
  unauthorized. **The gate did not mutate this manifest** and recorded no
  transition.
- **Published normalized / feature `__v002` manifests:** untouched; no
  transition.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no locked prior-phase script modified; no test
  outside the new module modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no published manifest / sidecar / prior gate report / successor-state artefact
  modified;
- no `data/microstructure/` or `data/research/` artefact staged or committed;
- no feature execution rerun; no feature artefact mutation; no normalization
  rerun; no raw-gate rerun; no normalized-layer-gate rerun;
- no published feature `__v002` read or mutation; no published normalized
  `__v002` read or mutation;
- no v002 terminal normalized window read; no v002 terminal raw window read; no
  sealed-test read;
- no labels / targets / future returns; no ML / model scoring / predictions; no
  diagnostics; no strategy / signal / PnL / backtest; no feature ranking /
  selection / pruning / hyperparameter / threshold / calibration tuning; no
  research-matrix output;
- no acquisition; no endpoint / public / Binance / `data.binance.vision` call;
  no archive / CHECKSUM download; no HEAD preflight;
- no `research_eligible` flip; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transition;
- no database / `.duckdb` / `.sqlite`; no Parquet compaction; no storage
  migration; no v003;
- no ETHUSDT / mark-price / spot / cross-venue / order-book / tick /
  extra-horizon data;
- no credential / `.env` / `.mcp.json` / MCP / Graphify / WebSocket / user
  stream / private / authenticated endpoint used;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment; no
  successor authorized.

## 12. Retained verdict ledger

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `flip_research_eligible(...)` always-raises invariant (never
  invoked)
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bn-J-R1 raw-only cap amendment
- Phase 4bn-L derived-stack storage budget
- Phase 4bn-N normalization manifest/versioning convention
- Phase 4bn-R feature manifest/versioning convention + non-eligible-source
  precondition (validated by this gate)

All prior phase results preserved verbatim. Phase 4 canonical remains
unauthorized.

## 14. No-rescue constraints

The Phase 4bn-T merge does not, and cannot, be construed as authorising:

- a label-derivation readiness / execution-plan phase or any successor
  (recommended only, NOT authorized);
- label derivation / label gate; targets; future returns; barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels; 30s / 5m / 30m /
  1h / 4h / longer-horizon label generation;
- ML model training / selection / scoring, predictions, strategy hypothesis
  generation, signal construction, position state, entry/exit rules,
  diagnostics, or backtest design;
- feature ranking / selection / pruning / engineering / hyperparameter /
  threshold / calibration tuning;
- a chronological-split / holdout policy decision or transition;
- paper / shadow / live-readiness / deployment / exchange-write / production-key
  work; Phase 4 canonical or Phase 5 authorisation;
- mark-price / spot / cross-venue / order-book / tick / additional aggTrades /
  ETHUSDT acquisition; extra horizons; v003 creation;
- reading the v002 terminal raw/normalized window or sealed-test split;
  mutating the published normalized or feature `__v002` family;
- database creation / DuckDB / SQLite / Parquet compaction / storage migration;
- transitioning any manifest's `research_eligible` or `eligibility_gate_status`
  from this passing feature-layer gate alone;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening.

## 15. Successor authorization

**None.**

Not authorized (candidates a future operator might consider):

- a label-derivation readiness or execution-plan phase (Phase 4bn-T's
  recommendation — requires separate operator authorization; must run no ML /
  diagnostics / strategy / PnL / backtests, flip no eligibility, and use no
  sealed test split unless separately governed);
- a docs-only holdout-boundary memo (only if a future scope reads the v002
  terminal raw/normalized window or sealed-test dates);
- a source-policy documentation memo; a process-doc `D:` path-string update;
- label derivation + label gate; a chronological-split / holdout policy memo;
- ML implementation; strategy implementation; backtest implementation;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot /
  cross-venue / ETHUSDT acquisition; v003 creation; storage migration; database
  creation;
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials;
- Phase 5; Phase 4 canonical.

## 16. Recommended state

**Remain paused.**

Phase 4bn-T is now **merge-complete on `main`** as of merge commit
`8149750801fdf8bad219f1baba1614d9c36e068b` and the subsequent merge-closeout +
SHA-finalization commits. Project completion of this phase requires the
SHA-finalization commit (`docs(phase-4bn-t): finalize merge closeout shas`) per
the repository's merge-closeout convention. The local feature segment remains
**non-eligible** (`research_eligible: false`, `eligibility_gate_status:
"pending"`, `no_successor_authorization: true`); no manifest eligibility
transition occurred. v003 remains forbidden and absent; the published feature
`__v002` family remains immutable; the v002 terminal raw/normalized window
remains by-reference only and unread; the sealed-test split remains untouched.
The **conditional next, NOT authorized** option is a separately-authorized
**label-derivation readiness or execution-plan phase**. It is **not** authorized
by this merge.

### Feature segment gated (preserved)

- **Exact feature segment:** 2024-03-01 .. 2024-11-30 inclusive UTC (Phase
  4bn-S pre-v002 feature segment; 275 dates).
- **Exact feature manifest path:**
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json`
  (SHA256 `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52`).
- **Exact feature output directory:**
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s/`
  (path-disjoint from the published `__v002/` feature dir; not the generic
  `microstructure_features_aggtrades_v001/` dir; not v003).
- **275 feature Parquet files validated; 275 feature sidecars validated; total
  feature footprint 54,254,406,538 bytes (≈50.53 GiB); total feature rows
  400,001,695; schema exactly `FEATURE_SCHEMA_V002`, 62 columns (17 lineage + 45
  feature/quality).**
- **Manifest required-field contract passed; manifest forbidden-field contract
  passed; leakage / causal-policy validation passed; predecessor integrity
  passed; published feature `__v002` remained by-reference / immutable; v002
  terminal raw/normalized windows remained unread; sealed-test split remained
  untouched.**
- **Gate report:**
  `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s__phase-4bn-t__1780674917156__e647435c81d7.json`
  (SHA256 `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`);
  **27 / 27 checks PASS; runtime 348.9 s.**

### Explicit confirmations

- Phase 4bn-T is merge-complete on `main` after this merge.
- Project completion requires the SHA-finalization commit
  (`docs(phase-4bn-t): finalize merge closeout shas`).
- Label-derivation readiness / execution-plan / any successor is **NOT
  authorized**.
- `research_eligible` remains `false`; `eligibility_gate_status` remains
  `pending`; no manifest eligibility transition occurred.
- v003 remains forbidden and absent; the published feature `__v002`
  manifest/family remained immutable; the v002 terminal raw/normalized window
  remained by-reference only and unread; the sealed-test split remained
  untouched.
- Local feature outputs and the Phase 4bn-T gate report are gitignored and
  uncommitted; the pre-existing gitignored Phase 4bn-S feature outputs, Phase
  4bn-O normalized outputs, and Phase 4bn-P normalized-layer gate report remain
  local and uncommitted.
- No acquisition was run, no endpoints were called, no archives were downloaded,
  no HEAD preflight was run, no raw gate was rerun, no normalization was rerun,
  no normalized-layer gate was rerun, no feature execution was rerun, no labels
  were derived, no targets were created, no future returns were computed, no ML
  was trained, no model scoring was performed, no predictions were generated, no
  diagnostics were run, no backtests were run, no strategy/signal/PnL work was
  performed, no storage migration occurred, no database was created, no Parquet
  was compacted, no v003 dataset was created, no v002 terminal raw/normalized
  window was read, no test holdout was touched, no manifest eligibility
  transition occurred, no `data/research` artefacts were created or committed, no
  `data/microstructure` artefacts were committed, and no
  paper/shadow/live/exchange-write/credentials/MCP/Graphify work was authorized.

### Final git status (at SHA-finalization)

Recorded in the final operator report: working tree clean except the expected
untracked transient `.claude/scheduled_tasks.lock` plus the expected gitignored
local `data/microstructure/` and `data/research/` namespaces; `main ==
origin/main` after push.
