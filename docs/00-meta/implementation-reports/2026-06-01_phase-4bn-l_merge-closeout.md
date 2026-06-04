# Phase 4bn-L — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-L — Derived-Stack Storage-Budget Memo.
- **Type:** Docs-only / storage-governance / derived-stack budgeting /
  stage-boundary memo. **Tier 1 — Full Phase** (per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3; it sets
  storage caps and stage boundaries adjacent to future normalization,
  feature derivation, label derivation, future holdout / split policy,
  future ML-baseline admissibility, and future local disk / runtime
  commitments, while authorizing none of them).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-L branch (the derived-stack
  storage-budget memo + closeout + the narrow `current-project-state.md`
  update) into `main` and record the canonical merge-closeout that makes
  Phase 4bn-L project-complete. Phase 4bn-L produced **no** local data
  artefact; nothing under `data/microstructure/` or `data/research/`
  accompanies this merge.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-l/derived-stack-storage-budget-memo`.

## 2. SHAs

- **`main` SHA before merge:** `d8d3ba845362e2c1d294522a89e3b90be93ba89f`
  (`docs(phase-4bn-k): finalize merge closeout shas`; pre-merge
  `main == origin/main == d8d3ba845362…` verified in sync; Phase 4bn-K
  SHA-finalization `d8d3ba8`, merge-closeout `63a43cc`, merge `19c6661`,
  branch `b00a4f3` all present on `main`).
- **Branch commit SHA (budget memo + closeout + state update):**
  `d56420ce8d29bc9062398ad906932069d6119f73`
  (`docs(phase-4bn-l): budget derived stack storage`; the original budget
  memo commit).
- **Branch-closeout finalization commit (final branch tip used for
  merge):** `20022d2c27e8f289b2614b59a9d2f196aca14f51`
  (`docs(phase-4bn-l): finalize branch closeout`; replaced the four
  placeholder fields `<COMMIT_SHA>` / `<GIT_STATUS>` / `<GIT_LOG>` /
  `<HEAD_SHA>` in the branch closeout with the actual branch-complete
  values before merge).
- **Merge commit SHA:** `5c7b5a944efd20141c388a49adfd3d31ad2bc6ed`
  (`docs(phase-4bn-l): merge derived stack storage budget`).
- **Merge-closeout commit SHA:** `docs(phase-4bn-l): add merge closeout`,
  recorded in `git log` and the final operator report. Per the repo
  convention used for Phase 4bn-K / 4bn-J-R2 / 4bn-J-R1 / 4bn-I and
  earlier, the merge-closeout commit cannot self-reference its own hash
  inside its own diff; the SHA is filled in by the subsequent
  SHA-finalization commit, which can reference the merge-closeout commit
  hash because that hash exists in `git log` before the SHA-finalization
  commit is created.
- **SHA-finalization commit:** `docs(phase-4bn-l): finalize merge closeout
  shas`, recorded in the final operator report and `git log`. The
  SHA-finalization commit likewise cannot self-reference its own hash
  inside its own diff; its SHA is captured in the final operator report
  and `git log`.
- **Final `main` / `origin/main` SHA after push:** after the
  SHA-finalization commit and push, final `main` SHA == final
  `origin/main` SHA == the SHA-finalization commit (recorded in the final
  operator report and `git log`).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message:
  `docs(phase-4bn-l): merge derived stack storage budget`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

**Docs (3 files):**

- `docs/00-meta/implementation-reports/2026-06-01_phase-4bn-l_derived-stack-storage-budget-memo.md`
  (added; the derived-stack storage-budget memo; 21 sections).
- `docs/00-meta/implementation-reports/2026-06-01_phase-4bn-l_closeout.md`
  (added; the branch closeout, with placeholders finalized on-branch).
- `docs/00-meta/current-project-state.md` (modified; narrow: new Phase
  4bn-L narrative paragraph + new `Current phase:` block; +157 lines, 0
  deletions; all prior content preserved verbatim).

**Source / tests / scripts / config:** none.

No `data/microstructure/` file was modified. No `data/research/` file was
modified. No prior governance memo was modified beyond the narrow
`current-project-state.md` paragraph + block addition. No prior source /
test / script was modified. No `.gitignore`, `pyproject.toml`, `README.md`,
or MCP file was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 157 ++++++
 .../2026-06-01_phase-4bn-l_closeout.md             | 180 +++++++
 ...hase-4bn-l_derived-stack-storage-budget-memo.md | 544 +++++++++++++++++++++
 3 files changed, 881 insertions(+)
```

The diff matches the expected change set from the authorization prompt
(add the memo, add the closeout, modify `current-project-state.md`); it is
purely additive (0 deletions).

## 6. Verdict

**MEMO RECORDED.** Phase 4bn-L recorded an explicit, stage-separated,
fail-closed storage-budget contract for the future 12-month BTCUSDT
Binance USDⓈ-M futures aggTrades derived stack: separate normalized,
feature, label, temporary-workspace, and binding total derived-stack caps;
a `D:` free-space floor; preflight and in-execution measurement
requirements; per-stage and global fail-closed stop conditions; and
stage-boundary rules that keep normalization, features, labels, ML,
diagnostics, and strategy each behind separate future authorization. Result
state: `DERIVED_STACK_STORAGE_BUDGET_RECORDED__REMAIN_PAUSED`. Decision:
`RECOMMEND_AUTHORIZE_NORMALIZATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
Phase 4bn-L is **merge-complete on `main`** after this merge. The raw
segment remains non-eligible (`research_eligible: false`,
`eligibility_gate_status: "pending"`); no manifest eligibility transition
occurred; the v002 terminal window was not read; the sealed test split was
not touched. **Recommended state: remain paused. No successor authorized.**

### Complete chosen budget values

- **Raw layer (carried forward, unchanged):** already-measured local raw
  pre-v002 segment 5,140,686,147 bytes / **4.788 GiB**; raw-only
  acquisition cap **10 GiB warning / 25 GiB hard**; no new raw acquisition
  authorized.
- **Normalized layer (future):** **100 GiB warning / 150 GiB hard**
  footprint; **4 h warning / 8 h hard** runtime.
- **Feature layer (future):** **50 GiB warning / 100 GiB hard** footprint;
  **4 h warning / 8 h hard** runtime.
- **Label layer (future):** **75 GiB warning / 125 GiB hard** footprint;
  **4 h warning / 8 h hard** runtime.
- **Temporary workspace (future):** **50 GiB warning / 100 GiB hard**;
  temporary files under an explicit gitignored path; cleaned on success or
  fail-closed stop; pre-cleanup and post-cleanup footprint reported.
- **Total derived-stack (future, binding aggregate):** **250 GiB warning /
  300 GiB hard** additional footprint beyond raw archives; includes
  normalized + feature + label + temporary files while running; preflight
  estimate above 300 GiB → stop and require a new storage memo; actual
  crossing 300 GiB → fail closed.
- **`D:` free-space floor (future):** **≥ 500 GiB free before execution**
  (else fail closed, operator decision); **fail closed if `D:` free space
  falls below 350 GiB during execution**.

**The total derived-stack hard cap of 300 GiB binds the aggregate even if
individual per-stage caps still have headroom** (the per-stage hard caps
sum to 475 GiB; the total governs and is lower).

### Stage-boundary rules (recorded)

1. Normalization must be separately authorized after Phase 4bn-L is merged.
2. Feature derivation must not run until normalization completes and passes
   its own gate.
3. Label derivation must not run until the required normalized / feature
   prerequisites are complete and separately authorized.
4. ML must not run until raw, normalized, feature, and label gates pass and
   a separate chronological-split / holdout policy is authorized.
5. Diagnostics must not run until separately authorized.
6. Strategy / signals / PnL / backtests must not run.
7. No phase may silently exceed its budget to "finish the run."
8. On any cap breach: fail closed, report partial outputs, leave all
   outputs non-eligible.
9. Any future partial outputs must remain gitignored and uncommitted.
10. Future manifests start `research_eligible: false` and
    `eligibility_gate_status: "pending"`; future label manifests
    additionally start `chronological_split_policy: "not_yet_defined"`.
11. No future generation phase may flip eligibility (Phase 4aw
    `flip_research_eligible(...)` always-raises invariant preserved).

### Future preflight measurement requirements (recorded)

Before writing, every future derived stage must: (1) estimate stage output
footprint; (2) estimate stage runtime; (3) estimate total derived-stack
footprint including already-written derived footprint, checked against the
300 GiB total hard cap; (4) check `D:` free space against the 500 GiB
floor; (5) record the per-stage and total caps in the run log. During
execution every stage must: measure footprint at day / month boundaries;
measure elapsed runtime; measure `D:` free space before the next stage /
day / month; measure temporary workspace footprint pre-cleanup and
post-cleanup. A stage that cannot produce a preflight estimate fails
closed.

### Future fail-closed stop conditions (recorded, 20)

(1) Preflight cannot estimate output footprint; (2) preflight exceeds
per-stage hard cap; (3) preflight exceeds total derived-stack hard cap (300
GiB → new storage memo required); (4) `D:` free below 500 GiB before
execution; (5) `D:` free below 350 GiB during execution; (6) temporary
workspace exceeds 100 GiB; (7) stage runtime exceeds 8 hours; (8) any
sealed-test-data read attempt; (9) any `research_eligible` flip attempt;
(10) any `eligibility_gate_status` transition-to-eligible attempt; (11) any
v003 creation; (12) any DuckDB / SQLite / database-file creation; (13) any
Parquet compaction; (14) any write outside approved gitignored data paths;
(15) any `data/microstructure` / `data/research` commit attempt; (16) any
ML / diagnostics / strategy / PnL / backtest attempt; (17) any need for
ETHUSDT / mark-price / spot / cross-venue / order-book / tick / extra-horizon
data; (18) any deviation from BTCUSDT / Binance USDⓈ-M futures / aggTrades /
v002-compatible semantics; (19) any missing prerequisite gate; (20) any
ambiguity about whether a future output is raw / normalized / feature /
label / research.

### Storage posture preserved

Active repo `D:\Prometheus`; active workspace
`D:\ClaudeRuns\prometheus-light`; raw / normalized / feature / label
outputs under existing `data/microstructure/` conventions; research outputs
(if ever authorized later) under `data/research/`; no `data/microstructure`
or `data/research` commits; Parquet canonical for future normalized /
feature / label artefacts; no DuckDB database cache; DuckDB in-place
querying of Parquet allowed only if separately needed and non-invasive; no
`.duckdb`; no SQLite research matrices; no `.sqlite`; no Parquet compaction
unless separately authorized by a storage-architecture phase; no storage
migration; no v003.

## 7. Local gitignored outputs (if any)

**None.** Phase 4bn-L produced no local artefact under
`data/microstructure/` or `data/research/`. No local data was read, hashed,
counted, inspected, created, staged, or committed during the phase or
during merge review.

## 8. Validation results

Docs-only Tier 1 phase; the relevant validation surface is git
status / diff review / `git diff --check` / gitignore confirmation / SHA
checks. Repository tooling (ruff / mypy / pytest) is **not** required and
was **not** run (no code / test / script / config surface). No repo-standard
markdown validator exists (no `.markdownlint*` / `.mdlrc` / markdownlint /
mdformat / remark configuration), so none was run.

- `git diff --check` → clean (exit 0).
- `git status --short` → only the expected untracked transient
  `.claude/scheduled_tasks.lock`; no `data/microstructure/` or
  `data/research/` artefact staged.
- `git diff --name-status main..phase-4bn-l/...` (pre-merge) → `M
  current-project-state.md`, `A` budget memo, `A` closeout.
- `git diff --stat <pre-merge main>..HEAD` → 3 files changed, 881
  insertions(+), 0 deletions.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.

## 9. Upstream immutability evidence (if applicable)

**n/a — phase did not access any local artefact.** Phase 4bn-L read only
committed repository Markdown and committed code / tests; it opened no raw
zip, normalized parquet, feature file, label file, manifest, sidecar, or
gate report, and therefore preserved every prior local artefact trivially
(none were touched).

## 10. Manifest state preservation (if applicable)

No manifest was read or mutated by Phase 4bn-L. All current microstructure
manifests remain at `research_eligible: false`,
`eligibility_gate_status: "pending"`, and (label manifest, when it exists)
`chronological_split_policy: "not_yet_defined"`; no transition occurred.
Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant preserved (never invoked).

## 11. Boundary confirmations

- no source modified; no test modified; no script modified;
- no `.gitignore`, `pyproject.toml`, or `README.md` modified; no MCP file
  modified;
- no `data/microstructure/` write; no `data/microstructure/` artefact
  read, created, staged, or committed;
- no `data/research/` write; no `data/research/` artefact read, created,
  staged, or committed;
- `.claude/scheduled_tasks.lock` remained untracked and was not committed;
- no manifest mutation; no sidecar mutation; no gate-report mutation; no
  successor-state mutation;
- no `research_eligible` flipped; no `eligibility_gate_status`
  transitioned; no `chronological_split_policy` changed; no
  `diagnostics_authorized` / `ml_authorized` set;
- no data acquired; no endpoint / public endpoint / Binance /
  `data.binance.vision` called; no archive or CHECKSUM downloaded; no HEAD
  preflight; no WebSocket / user stream / private / authenticated endpoint;
- no raw zip inspected; no v002 terminal window read; no sealed test split
  read / counted / sampled / hashed / summarized / inspected;
- no normalization; no feature derivation; no label derivation; no feature
  ranking / selection / pruning / engineering; no ML training / scoring /
  prediction; no diagnostics; no strategy / signal / PnL / backtest;
- no storage migration; no database created; no `.duckdb` / `.sqlite`; no
  Parquet compaction; no v003;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment;
  no successor authorized.

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
- Phase 4aw `flip_research_eligible(...)` always-raises invariant
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bn-J-R1 raw-only cap amendment (10 GiB warning / 25 GiB hard)

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bn-L merge does not, and cannot, be construed as authorising:

- normalization, feature derivation, label derivation, or any conversion
  of raw / normalized / feature / label artefacts into research outputs;
- ML model training, model selection, scoring, prediction, feature ranking
  / selection / pruning / engineering, hyperparameter / threshold tuning,
  or calibration fitting;
- strategy hypothesis generation, signal construction, position state,
  entry / exit rules, PnL simulation, or backtest design;
- diagnostics of any kind;
- raw acquisition; endpoint / public endpoint / Binance /
  `data.binance.vision` contact; archive or CHECKSUM download; HEAD
  preflight;
- storage migration, database creation, `.duckdb` / `.sqlite` creation,
  Parquet compaction, or v003 creation;
- ETHUSDT / mark-price / spot / cross-venue / order-book / tick /
  extra-horizon data;
- paper / shadow / live-readiness / deployment / exchange-write / production
  keys;
- Phase 4 canonical or Phase 5 authorisation;
- transitioning any manifest's `research_eligible`,
  `eligibility_gate_status`, or `chronological_split_policy` from this memo
  alone;
- authorising the normalization-readiness or normalization execution plan
  that this memo recommends.

The budget recorded here is a contract that future phases must obey before
execution; recording it spends nothing and authorises nothing executable.

## 15. Successor authorization

**None.**

Not authorized by this merge (candidate successors a future operator might
consider, each requiring separate authorization):

- a normalization-readiness or normalization execution plan (the
  recommended-but-NOT-authorized conditional next; see §16);
- a source-policy documentation memo;
- a process-doc `D:` path-string update (refreshing the Phase 4bm-D-P1
  lightweight-workspace standard's stale `C:` example paths);
- any normalization / feature / label derivation phase;
- any raw / normalized / feature / label eligibility-gate phase;
- any ML implementation / model training / diagnostics phase;
- any strategy / signal / PnL / backtest phase;
- any storage-architecture / storage-migration / Parquet-compaction /
  database-creation / v003 phase;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / ETHUSDT
  acquisition;
- paper / shadow / live-readiness / deployment / exchange-write / production
  keys / authenticated APIs / private endpoints / user stream / MCP /
  Graphify / `.mcp.json` / credentials;
- Phase 4 canonical; Phase 5.

## 16. Recommended state

**Remain paused.**

**Conditional next, NOT authorized:** A separately authorized
normalization-readiness or normalization execution plan is the cleanest
non-paused option. It would, under the budget recorded here, plan (and only
if separately authorized, execute) normalization of the expanded 12-month
BTCUSDT aggTrades envelope into normalized aggTrades artefacts under the
normalized-layer cap (100 GiB warning / 150 GiB hard; 4 h / 8 h), preflight
and measure footprint / runtime / `D:` free space, and fail closed on any
cap breach — while deriving no features, labels, ML, diagnostics, strategy,
or research outputs and flipping no eligibility. It is **not** authorised by
this merge.

---

This merge-closeout preserves all retained verdicts and project locks
verbatim. It does not authorize any successor phase. Phase 4 canonical
remains unauthorized.
