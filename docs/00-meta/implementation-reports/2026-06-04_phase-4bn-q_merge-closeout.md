# Phase 4bn-Q — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-Q — Docs-Only Feature-Derivation Readiness / Execution
  Plan.
- **Type:** docs-only / feature-derivation readiness / feature execution
  planning / feature manifest and gate boundary-contract.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-Q feature-derivation readiness /
  execution-plan memo, its closeout, and the narrow `current-project-state.md`
  update onto `main` as project state. The phase produced **no** code, tests,
  scripts, data, or local artefacts; it is a docs-only boundary-contract memo.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-q/feature-derivation-readiness-execution-plan`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section
  merge-closeout required).

## 2. SHAs

- **`main` SHA before merge:** `b2b46de6a27311318b2e9d58f5de28e5137b28dd`
  (`docs(phase-4bn-p): finalize merge closeout shas`).
- **Branch commit SHA (docs):** `b7f8f2cd1c23f34969db659fa7c36c07ff990b40`
  (`docs(phase-4bn-q): plan feature derivation readiness`).
- **Merge commit SHA:** `7ac685b307cfd7a8454e3758f7c059135bf8b29d`
  (`docs(phase-4bn-q): merge feature derivation readiness plan`).
- **Merge-closeout commit SHA:** `51a20a2d3c7cc64160dc56ebf4713f5bbbcf0f0f`
  (`docs(phase-4bn-q): add merge closeout`).
- **SHA-finalization commit SHA:** this commit
  (`docs(phase-4bn-q): finalize merge closeout shas`) — its own hash is the new
  `main` tip; recorded verbatim in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization commit;
  `main == origin/main` after push (recorded in the final operator report).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `docs(phase-4bn-q): merge feature derivation readiness
  plan`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
  (recorded at the final operator report after the SHA-finalization commit).

## 4. Files brought forward by the merge

- **Docs (3):**
  - `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-Q
    paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-P
    paragraphs and blocks preserved verbatim as labelled historical context);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-q_feature-derivation-readiness-execution-plan.md`
    (added — the readiness/execution-plan memo, 21 sections);
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-q_closeout.md`
    (added — branch closeout).
- **Source / tests / scripts / config:** none.
- **`data/microstructure/` files:** **none modified or committed.** No
  `data/research/` file. No published manifest, sidecar, gate report,
  successor-state artefact, `.gitignore`, `pyproject.toml`, `README.md`, or MCP
  file was modified.

The diff matches the expected change set from the merge authorization prompt
exactly (add 2 files, modify 1 doc).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 111 +++++
 .../2026-06-04_phase-4bn-q_closeout.md             | 158 ++++++
 ..._feature-derivation-readiness-execution-plan.md | 536 +++++++++++++++++++++
 3 files changed, 805 insertions(+)
```

## 6. Verdict

**MEMO RECORDED.** Phase 4bn-Q determined, from committed docs and committed
tooling only, whether a future feature-only execution phase can be safely
authorized over the Phase 4bn-O / 4bn-P pre-v002 normalized BTCUSDT Binance
USDⓈ-M futures aggTrades segment. Findings: the v002 feature **primitives** are
safe and directly reusable; the feature **compute orchestrator** and **feature
gate** are NOT directly reusable (hardcoded 90-day v002 terminal window +
published `__v002` manifest + Phase 4bm-F Stage-3 research-eligible
successor-state precondition + no Phase 4bn-L caps) and need bounded new
wrappers; the feature **manifest/versioning** shape is ambiguous (the existing
tooling's research-eligible-source precondition conflicts with the non-eligible
pre-v002 segment, and the pre-v002 feature segment manifest/versioning is not
codified); the sealed-test / v002-terminal boundary is **clear** for the
conservative causal-only pre-v002 scope (no holdout-boundary memo required). The
decision is
`RECOMMEND_AUTHORIZE_DOCS_ONLY_FEATURE_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`,
mirroring how Phase 4bn-N settled the normalized layer before Phase 4bn-O
executed. The merge lands the memo + closeout + narrow state update on `main`;
the project remains paused.

## 7. Local gitignored outputs (if any)

**None.** Phase 4bn-Q is docs-only: it created no local artefact under
`data/microstructure/` or `data/research/`, read no local data, hashed no local
data, and counted no local data. The pre-existing Phase 4bn-O normalized
outputs and Phase 4bn-P normalized-layer gate report remain local, gitignored
(`.gitignore:85`), and uncommitted; this phase did not touch them.

## 8. Validation results

Docs-only validation (no code/test/script/config surface; no real gate /
normalization / feature run):

- `git diff --check` → clean (no whitespace errors).
- `git diff --name-status main..branch` → exactly the 3 expected docs files
  (M `current-project-state.md`; A memo; A closeout).
- `git status --short` → only `.claude/scheduled_tasks.lock` untracked; no
  `data/microstructure/` or `data/research/` artefact staged.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- **ruff / pytest / mypy:** not required — Phase 4bn-Q adds no code/test/script
  surface. The relevant validation surface for a docs-only phase is git status,
  diff review, `git diff --check`, gitignore confirmation, and SHA checks.
- **Markdown validator:** no repo-standard markdown lint tooling is configured;
  none was run (running an ad-hoc one is unnecessary and could create outputs).

## 9. Upstream immutability evidence

**n/a — phase did not access any local artefact.** Phase 4bn-Q read only
committed repository Markdown and committed code/tests; it opened no local
normalized/raw/feature/label/manifest/sidecar/gate-report/successor-state or
`data/research` artefact. The merge modified no `data/microstructure/` file.
The published normalized `__v002` family, the Phase 4bn-O pre-v002 normalized
segment, and the Phase 4bn-P gate report were untouched.

## 10. Manifest state preservation

- No manifest was read, created, or mutated by this phase. The Phase 4bn-O
  normalized segment manifest and all prior manifests remain unchanged:
  `research_eligible: false`, `eligibility_gate_status: "pending"`; no
  transition occurred.
- `chronological_split_policy` unchanged/absent.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no test modified; no script modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no published manifest / sidecar / gate report / successor-state artefact
  modified;
- no `data/microstructure/` or `data/research/` artefact read, created,
  staged, or committed;
- no feature derivation; no feature artefact; no feature manifest creation or
  mutation; no label derivation;
- no normalization rerun; no raw-gate rerun; no normalized-layer-gate rerun; no
  feature-gate run; no acquisition; no endpoint / public / Binance /
  `data.binance.vision` call; no archive / CHECKSUM download; no HEAD preflight;
- no local raw zip / normalized Parquet / feature / label read; no v002
  terminal-window read; no sealed-test read; no local manifest / gate-report
  read under `data/microstructure`;
- no diagnostics; no ML; no scoring; no predictions; no feature ranking /
  selection / pruning / tuning / calibration; no strategy / signal / PnL /
  backtest;
- no `research_eligible` flip; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transition;
- no database / `.duckdb` / `.sqlite`; no Parquet compaction; no storage
  migration; no v003;
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

All prior phase results preserved verbatim. Phase 4 canonical remains
unauthorized.

## 14. No-rescue constraints

The Phase 4bn-Q merge does not, and cannot, be construed as authorising:

- a feature manifest/versioning memo, a feature-only execution phase, a
  feature-layer eligibility gate, or any successor (recommended only, NOT
  authorized);
- feature derivation, label derivation, or research outputs;
- ML model training / selection, strategy hypothesis generation, signal
  construction, position state, entry/exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / tick / additional aggTrades /
  ETHUSDT acquisition; v003 creation;
- reading the v002 terminal raw/normalized window or sealed-test split;
  mutating the published `__v002` family;
- database creation / DuckDB / SQLite / Parquet compaction / storage migration;
- transitioning any manifest's `research_eligible` or `eligibility_gate_status`
  from this memo alone;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening.

## 15. Successor authorization

**None.**

Not authorized (candidates a future operator might consider):

- a docs-only feature manifest/versioning memo (Phase 4bn-Q's recommendation —
  requires separate operator authorization);
- a feature-only execution phase + bounded wrapper + offline tests;
- a feature-layer eligibility gate;
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

Phase 4bn-Q is now **merge-complete on `main`** as of merge commit
`7ac685b307cfd7a8454e3758f7c059135bf8b29d` and the subsequent merge-closeout +
SHA-finalization commits. The normalized segment and any future feature output
remain **non-eligible** (`research_eligible: false`, `eligibility_gate_status:
"pending"`); no manifest eligibility transition occurred. The **conditional
next, NOT authorized** option is a separately-authorized **docs-only feature
manifest/versioning memo** (settling the pre-v002 feature segment manifest
shape, the version-suffixed segment directory, the non-eligible-source
precondition, and the by-reference linkage to the published `__v002` feature
family), to be followed only later — and only if separately authorized — by a
bounded feature-only execution wrapper and a feature-layer eligibility gate. It
is **not** authorized by this merge.

### Readiness findings (preserved)

- Feature **primitives** (`features_schema_v002`, `features_compute_v002`,
  `features_io_v002`, `features_manifest_v002`, `features_schema`): **safe and
  directly reusable** (causal-only; no labels/targets/future returns;
  forbidden-substring guard; canonical sidecars; atomic refuse-overwrite;
  network-free; offline tests present).
- Feature **compute orchestrator** (`scripts/phase4bm_h_compute_multiday_features.py`):
  **NOT directly reusable — needs a bounded new wrapper** (hardcoded 90-day v002
  terminal window 2024-12-01..2025-02-28, count 90, 155,153,449 events; expects
  published `__v002` normalized manifest; requires Phase 4bm-F Stage-3
  research-eligible successor-state; no Phase 4bn-L caps).
- Feature **gate** (`multiday_feature_gate*`, Phase 4bm-J): **NOT directly
  reusable — needs a bounded new wrapper** (same 90-day v002 hardcoding +
  Stage-3 successor precondition).
- Feature **manifest/versioning + non-eligible-source precondition**:
  **ambiguous; requires a docs-only memo.**
- Sealed-test / v002 terminal boundary: **clear** for the conservative
  causal-only pre-v002 feature scope; **holdout-boundary memo not required**.

### Future feature scope recommended (preserved)

- BTCUSDT only; Binance USDⓈ-M futures only; aggTrades only.
- Input: the Phase 4bn-O pre-v002 normalized segment only, 2024-03-01 ..
  2024-11-30 inclusive UTC; existing v002 terminal normalized family by
  reference only; no v002 terminal normalized reads; no sealed-test reads.
- Output: feature artefacts only — no labels / targets / future returns / ML
  outputs / diagnostics / research matrices / `data/research` outputs; under
  `data/microstructure/features/`; Parquet canonical; canonical `.sha256`
  sidecars; a single non-eligible feature segment manifest + sidecar; no
  database; no Parquet compaction; no v003.
- **Candidate future conventions (subject to the feature manifest/versioning
  memo):** output dir
  `data/microstructure/features/microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet`;
  manifest
  `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002_pre_v002_segment_<feature-phase-id>.json`.

### Phase 4bn-L budget carried forward (preserved)

- Feature footprint warn **50 GiB** / hard **100 GiB**; runtime warn **4 h** /
  hard **8 h**.
- Temporary workspace warn **50 GiB** / hard **100 GiB**.
- Total derived-stack warn **250 GiB** / hard **300 GiB**.
- `D:` free-space floor **≥ 500 GiB** before execution; **fail closed below 350
  GiB** during execution. Stop before writing if feature output est. > 100 GiB,
  total stack > 300 GiB, runtime > 8 h, or `D:` free < 500 GiB.

### Future fail-closed stop conditions (preserved)

The 35 fail-closed stop conditions for a future feature phase are recorded in
§16 of the Phase 4bn-Q memo and carried forward verbatim (missing/ mismatched
normalized prerequisites; date/scope violations; sealed-test or v002-terminal
ambiguity; forward-looking / label / future-return features; budget / `D:`
breaches; output-path / data-research / label / ML / database / Parquet-compaction
/ v003 / eligibility-flip / commit violations; ETHUSDT / mark-price / spot /
cross-venue / order-book / tick / extra-horizon needs; manifest/versioning
ambiguity; sidecar/tooling-unsafe conditions; forbidden feature column names;
cross-boundary leakage; sealed-split dependence).

### Explicit confirmations

- Phase 4bn-Q is merge-complete on `main` after this merge.
- Project completion of this phase requires the SHA-finalization commit
  (`docs(phase-4bn-q): finalize merge closeout shas`) per the repository's
  merge-closeout convention.
- Feature manifest/versioning memo / feature-only execution / any successor is
  **NOT authorized**.
- `research_eligible` remains `false`; `eligibility_gate_status` remains
  `pending`; no manifest eligibility transition occurred.
- No local data was read, created, or committed; the pre-existing gitignored
  Phase 4bn-O / 4bn-P artefacts remain local and uncommitted.
- No acquisition was run, no endpoints were called, no archives were downloaded,
  no HEAD preflight was run, no raw gate was rerun, no normalization was rerun,
  no normalized-layer gate was rerun, no local raw zip contents were inspected,
  no local normalized Parquet files were read, no v002 terminal window was read,
  no test holdout was touched, no features were derived, no labels were derived,
  no ML was trained, no diagnostics were run, no backtests were run, no
  strategy/signal/PnL work was performed, no storage migration occurred, no
  database was created, no Parquet was compacted, no v003 dataset was created,
  no manifest eligibility transition occurred, no `data/research` artefacts were
  created or committed, no `data/microstructure` artefacts were created or
  committed, and no paper/shadow/live/exchange-write/credentials/MCP/Graphify
  work was authorized.

### Final git status (at SHA-finalization)

Recorded in the final operator report: working tree clean except the expected
untracked transient `.claude/scheduled_tasks.lock` plus the expected gitignored
local `data/microstructure/` and `data/research/` namespaces; `main ==
origin/main` after push.
