# Phase 4bn-M — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-M — Normalization Readiness / Execution Plan.
- **Type:** docs-only / normalization-readiness / execution-planning /
  boundary-contract phase. **Risk tier: Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-M normalization-readiness /
  execution-plan memo, its closeout, and the narrow `current-project-state.md`
  update onto `main` so the predeclared future normalization-only execution
  contract for the expanded 12-month BTCUSDT Binance USDⓈ-M futures aggTrades
  envelope becomes project state. The phase authorizes nothing executable and
  no successor; it records a readiness plan and a decision and remains paused.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-m/normalization-readiness-execution-plan`.

## 2. SHAs

- **`main` SHA before merge:** `b7767a636a864bcb2eeca6a613c8f7c602a85c5b`
  (`docs(phase-4bn-l): finalize merge closeout shas`).
- **Branch commit SHA (memo + closeout + state update):**
  `844bc5fba69f08ed0a4a090b65279c2e572d557f`
  (`docs(phase-4bn-m): plan normalization readiness`).
- **Merge commit SHA:** `3dad0cb476573a10e358525eaf5b8bd8023399ea`
  (`docs(phase-4bn-m): merge normalization readiness plan`).
- **Merge-closeout commit SHA:** `6d8f9d3613702a41cc03b23860c00adb4f9c75d9`
  (`docs(phase-4bn-m): add merge closeout`).
- **SHA-finalization commit:** `docs(phase-4bn-m): finalize merge closeout
  shas` — this commit (the published `main` tip after push); its exact
  40-char SHA is recorded in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization
  commit above; exact 40-char SHA recorded in the final operator report
  after push (`main == origin/main` at that SHA).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message:
  `docs(phase-4bn-m): merge normalization readiness plan`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- **Push status:** pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing, after the SHA-finalization commit
  `docs(phase-4bn-m): finalize merge closeout shas`.

## 4. Files brought forward by the merge

- **Docs (3 files):**
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-m_normalization-readiness-execution-plan.md`
    (added; the 20-section readiness / execution-plan memo).
  - `docs/00-meta/implementation-reports/2026-06-04_phase-4bn-m_closeout.md`
    (added; the branch closeout).
  - `docs/00-meta/current-project-state.md` (modified; new Phase 4bn-M
    prose paragraph + new `Current phase:` block; prior Phase 4bn-A …
    4bn-L paragraphs and blocks preserved as labelled historical context).
- **Source:** none.
- **Tests:** none.
- **Scripts:** none.
- **Config / `.gitignore` / `pyproject.toml` / `README.md` / MCP:** none.
- **No `data/microstructure/` file was modified.** No prior governance memo
  was modified beyond the narrow `current-project-state.md` paragraph + block
  addition. No prior source / test / script was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 193 +++++++
 .../2026-06-04_phase-4bn-m_closeout.md             | 187 +++++++
 ...4bn-m_normalization-readiness-execution-plan.md | 607 +++++++++++++++++++++
 3 files changed, 987 insertions(+)
```

The diff matches the expected change set from the authorization prompt
exactly: add the memo, add the closeout, modify `current-project-state.md`.
No deletions; no other files touched.

## 6. Verdict

**MEMO RECORDED — `RECORD_NORMALIZATION_READINESS_PLAN__REMAIN_PAUSED`.**
Phase 4bn-M recorded, from committed docs and committed tooling only, a
predeclared future normalization-only execution contract for the expanded
12-month BTCUSDT Binance USDⓈ-M futures aggTrades envelope: scope, inputs,
outputs, manifest/versioning posture, the carried-forward Phase 4bn-L
budget, preflight requirements, 30 fail-closed stop conditions, required
offline tests for any future bounded tooling, and required successor
validation/gate phases. It ran no normalization, read no local data, and
created no local data. The decision is
`RECOMMEND_AUTHORIZE_DOCS_ONLY_NORMALIZATION_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
With this merge, **Phase 4bn-M is merge-complete on `main`.** The raw segment
remains non-eligible (`research_eligible: false`,
`eligibility_gate_status: "pending"`); no manifest eligibility transition
occurred. **Recommended state: remain paused.**

## 7. Local gitignored outputs (if any)

**None.** Phase 4bn-M produced no local artefact under `data/microstructure/`
or `data/research/`. It read no local data and created no local data. The
only untracked working-tree entry is the known scheduler transient
`.claude/scheduled_tasks.lock` (not committed).

## 8. Validation results

Docs-only Tier 1 phase with no code/test/script/config surface; the relevant
validation surface is git status, diff review, `git diff --check`, gitignore
confirmation, and SHA checks.

- `git diff --check` → clean (no whitespace errors).
- `git diff --name-status main..phase-4bn-m/normalization-readiness-execution-plan`
  (pre-merge) →
  `M docs/00-meta/current-project-state.md`,
  `A docs/00-meta/implementation-reports/2026-06-04_phase-4bn-m_closeout.md`,
  `A docs/00-meta/implementation-reports/2026-06-04_phase-4bn-m_normalization-readiness-execution-plan.md`.
- `git diff --stat` (merge) → `3 files changed, 987 insertions(+)`.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`; no
  `data/microstructure/` or `data/research/` artefact staged or committed.
- **ruff / mypy / pytest:** not required and not run — Phase 4bn-M creates no
  code/test/script/config surface (no source change to lint or type-check, no
  test to run). **No repo-standard markdown validator exists** (no
  `.markdownlint*`, `.mdlrc`, or markdownlint / mdformat / remark dependency),
  so none was run.

## 9. Upstream immutability evidence (if applicable)

**n/a — phase did not access any local artefact.** Phase 4bn-M did not open,
hash, read, or mutate any raw manifest, raw zip, normalized parquet, feature
parquet, label parquet, gate report, successor-state JSON, or sidecar under
`data/microstructure/`, and created nothing under `data/research/`.

## 10. Manifest state preservation (if applicable)

No manifest was read or mutated by this phase. State carried forward
unchanged for all microstructure manifests in the project:

- `research_eligible` — **false** (unchanged; no transition).
- `eligibility_gate_status` — **"pending"** (unchanged; no transition).
- `chronological_split_policy` — **"not_yet_defined"** for the label manifest
  (unchanged; no transition).
- Governance labels — **unchanged**.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant **preserved (never invoked).**

## 11. Boundary confirmations

- no source code modified;
- no test modified;
- no script modified;
- no `.gitignore`, `pyproject.toml`, or `README.md` modified;
- no MCP file modified;
- no manifest mutated;
- no sidecar mutated;
- no gate report mutated;
- no successor-state artefact mutated;
- no `data/microstructure/` write or commit;
- no `data/research/` write or commit;
- no `research_eligible` flipped on any manifest;
- no `eligibility_gate_status` transitioned on any manifest;
- no `chronological_split_policy` changed;
- no `diagnostics_authorized` / `ml_authorized` transition;
- no normalization run; no normalizer rerun;
- no raw eligibility gate rerun; no derived/feature/label gate rerun;
- no feature / label kernel run;
- no ML model trained; no model scoring; no predictions;
- no diagnostics run;
- no strategy created; no signal computed; no PnL; no backtest run;
- no data acquired; no public / Binance / `data.binance.vision` endpoint
  called; no archive or CHECKSUM downloaded; no HEAD preflight; no WebSocket
  / user stream opened;
- no local raw zip contents inspected; no v002 terminal raw window read; no
  sealed test split read / counted / sampled / hashed / inspected;
- no storage migration; no DuckDB / SQLite / `.duckdb` / `.sqlite` / database
  created; no Parquet compaction; no v003 created;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment;
- no successor authorized.

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

**All preserved verbatim.**

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bn-J-R1 raw-only cap amendment (10 GiB warning / 25 GiB hard)
- Phase 4bn-L derived-stack storage budget

**All prior phase results preserved verbatim.**

## 14. No-rescue constraints

The Phase 4bn-M merge does not, and cannot, be construed as authorising:

- normalization execution, normalized-artefact generation, or a bounded
  normalization runner;
- feature derivation, label derivation, or any research-matrix construction;
- ML model training, model selection, model scoring, predictions, feature
  ranking / selection / pruning / engineering, hyperparameter tuning,
  threshold tuning, or calibration fitting;
- strategy hypothesis generation, signal construction, position state, entry
  / exit rules, PnL simulation, or backtest design / execution;
- raw acquisition; public / Binance / `data.binance.vision` endpoint calls;
  archive or CHECKSUM downloads; HEAD preflight; WebSocket / user stream;
- reading the v002 terminal raw window or touching the sealed test split for
  any ML / diagnostics / statistics / strategy / research use;
- storage migration; DuckDB / SQLite / database creation; Parquet compaction;
  v003 dataset creation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / tick / ETHUSDT /
  extra-horizon / additional aggTrades acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- paper / shadow / live-readiness / deployment / exchange-write / production
  keys / authenticated APIs / private endpoints / credentials / MCP /
  Graphify / `.mcp.json`;
- Phase 4 canonical or Phase 5 authorisation;
- transitioning any manifest's `research_eligible` or
  `eligibility_gate_status` from this readiness plan alone;
- authorizing the recommended docs-only normalization manifest/versioning
  memo — it is recommended only, **subject to separate operator
  authorization.**

## 15. Successor authorization

**None.**

Candidate successors that are **NOT** authorized by this merge:

- docs-only normalization manifest/versioning memo (the Phase 4bn-M
  recommendation — recommended only, not authorized);
- normalization-only execution phase (bounded new runner over the pre-v002
  segment);
- docs-only holdout-boundary memo (only relevant if a future phase reads the
  v002 terminal raw window);
- source-policy documentation memo;
- process-doc `D:` path-string update (Phase 4bm-D-P1 lightweight-workspace
  standard still carries old `C:` example paths);
- normalized-layer eligibility gate; feature derivation + feature gate;
  label derivation + label gate; chronological-split / holdout policy memo;
- ML implementation; strategy implementation; backtest implementation;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / ETHUSDT
  data acquisition;
- paper / shadow; live-readiness; deployment; exchange-write; production
  keys; authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials;
- Phase 5; Phase 4 canonical.

## 16. Recommended state

**Remain paused.**

**Conditional next, NOT authorized:** a docs-only normalization
manifest/versioning memo is the cleanest non-paused option. It would settle —
at design level only — the manifest/versioning shape for a pre-v002
normalized aggTrades segment (segment manifest vs predecessor-linked
extension; how the eventual full 12-month normalized envelope is identified;
keeping v003 forbidden), thereby unblocking a subsequent normalization-only
execution phase. It is **not** authorized by this merge.

---

### Readiness findings carried onto `main`

1. **Normalization tooling primitives are SAFE and directly reusable** —
   `normalize_aggtrades.py` (19-column `NORMALIZED_SCHEMA_V001` + CSV
   iterator), `normalize_io.py` (path discipline, atomic zstd Parquet,
   canonical two-space `.sha256` sidecars, refuse-overwrite),
   `normalize_manifest.py`, `normalize_validation.py`, `canonical_paths.py`,
   the `derived_gate*` / `multiday_derived_gate*` modules, and the offline
   normalization test suite; network-free, credential-free, path-disciplined.
2. **The existing runner requires a bounded new wrapper** —
   `scripts/phase4bm_b_normalize_multiday_aggtrades.py` is hardcoded to the
   90-day v002 window and locked v002 precondition SHAs, reads the published
   v002 raw manifest (not the pre-v002 segment manifest), enforces a v002
   identity cross-check, and has no Phase 4bn-L preflight/budget caps, so it
   cannot be repointed safely at the pre-v002 segment. A bounded new runner
   reusing the locked primitives and adding segment-date guards, the segment
   manifest as source, and the Phase 4bn-L caps is required — assessed safe
   and bounded, not unsafe.
3. **Manifest/versioning is ambiguous and requires a memo** — the pre-v002
   raw segment used a phase-scoped segment manifest while
   `dataset-versioning.md` codifies only monotonic `__vNNN` + predecessor
   linkage and does not settle the normalized segment-manifest /
   backward-extension / full-envelope identity; v003 is forbidden; this
   ambiguity is the binding reason for the Phase 4bn-M decision.
4. **Sealed-test / v002 terminal boundary is clear for the conservative
   pre-v002-only scope** — the new pre-v002 segment 2024-03-01 .. 2024-11-30
   contains no sealed-test dates; the existing v002 terminal window
   2024-12-01 .. 2025-02-28 is already normalized in the `__v002` family;
   raw-to-normalized over sealed dates was already performed by Phase 4bm-B
   and is not test-use by itself; a separate holdout-boundary memo is required
   only if a future phase proposes to read the v002 terminal raw window; the
   sealed test split remains protected from ML, diagnostics, statistics,
   strategy, and research use regardless of normalization scope.

### Future normalization scope recommended (design level only; not authorized)

- BTCUSDT only; Binance USDⓈ-M futures only; aggTrades only; normalized
  aggTrades output only.
- Conservative first execution: **pre-v002 segment 2024-03-01 .. 2024-11-30
  only.**
- Existing v002 terminal window treated **by reference**; full 12-month
  envelope assembled **by manifest/reference** rather than re-reading the
  terminal window.
- Parquet canonical; canonical sidecars; non-eligible manifest; no database;
  no Parquet compaction; no v003; no features / labels / research outputs.

### Phase 4bn-L budget carried forward

- Normalized layer: **100 GiB warning / 150 GiB hard** footprint.
- Normalized runtime: **4 h warning / 8 h hard**.
- Temporary workspace: **50 GiB warning / 100 GiB hard**.
- Total derived-stack (binding aggregate): **250 GiB warning / 300 GiB hard**.
- `D:` free-space floor: **≥ 500 GiB before execution**; **fail closed below
  350 GiB during execution**.
- Stop before writing if the normalized output estimate exceeds 150 GiB, the
  total derived-stack estimate exceeds 300 GiB, the runtime estimate exceeds
  8 h, or `D:` free space is below 500 GiB.

### Future fail-closed stop conditions (carried forward)

Missing raw archive / sidecar prerequisite; raw archive hash mismatch; raw
archive path outside approved BTCUSDT aggTrades conventions; any date outside
the authorized range; any ambiguity about reading v002 terminal / sealed-test
raw dates; any attempt to use sealed-test data for ML / diagnostics /
statistics / strategy / research; preflight cannot estimate normalized
footprint; normalized estimate > 150 GiB; total derived-stack estimate
> 300 GiB; `D:` free < 500 GiB before execution; `D:` free < 350 GiB during
execution; temporary workspace > 100 GiB; runtime > 8 h; output path outside
approved gitignored `data/microstructure/normalized/`; any attempt to create
`data/research` output / features / labels; any attempt to run ML /
diagnostics / strategy / PnL / backtests; any attempt to create DuckDB /
SQLite / database files; any Parquet compaction; any v003 creation; any
`research_eligible` flip; any `eligibility_gate_status` transition to
eligible; any `data/microstructure` or `data/research` commit; any need for
ETHUSDT / mark-price / spot / cross-venue / order-book / tick / extra-horizon
data; any deviation from BTCUSDT / Binance USDⓈ-M futures / aggTrades /
v002-compatible semantics; any missing or ambiguous manifest/versioning
convention; any inability to create canonical sidecars; any validator /
tooling unsafe condition.

### Execution-review confirmation

During this merge review, **no acquisition was run, no endpoints were called,
no archives were downloaded, no HEAD preflight was run, no raw gate was run,
no normalization was run, no raw zip contents were inspected, no local
manifest or gate report under `data/microstructure` was read, no v002
terminal window was read, no test holdout was touched, no features were
derived, no labels were derived, no ML was trained, no model scoring was
performed, no predictions were generated, no diagnostics were run, no
backtests were run, no strategy / signal / PnL work was performed, no storage
migration occurred, no database was created, no Parquet was compacted, no
v003 dataset was created, no manifest eligibility transition occurred, no
`data/research` artefacts were created or committed, no `data/microstructure`
artefacts were created or committed, and no paper / shadow / live-readiness /
deployment / exchange-write / production-key / credentials / MCP / Graphify
work was authorized.**

### Lifecycle note

With this merge and merge-closeout, **Phase 4bn-M is merge-complete on
`main`** per `merge-closeout-standard.md` (Tier 1, full 16-section
structure). Per the project's current convention, project completion is
finalized by a separate **SHA-finalization** commit
(`docs(phase-4bn-m): finalize merge closeout shas`) that records the
merge-closeout commit SHA and the final `main` / `origin/main` SHA, which are
not knowable before the merge-closeout commit exists.
