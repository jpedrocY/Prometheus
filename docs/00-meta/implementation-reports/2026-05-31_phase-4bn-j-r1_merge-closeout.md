# Phase 4bn-J-R1 — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-J-R1 — Workspace Relocation + Raw-Only Acquisition
  Cap Amendment.
- **Type:** docs-only / governance-only / amendment-only phase.
- **Risk tier:** **Tier 1 — Full Phase** (per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3): it amends the
  acquisition execution contract adjacent to public historical data
  acquisition, local disk / runtime caps, data / microstructure artefact
  generation, future eligibility gates, and future ML-baseline
  admissibility, while authorizing no acquisition and no downstream use.
  Full 16-section merge-closeout used (no short-form).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-J-R1 amendment memo, closeout,
  preserved Phase 4bn-J stop report, and the narrow
  `current-project-state.md` update onto `main` so the workspace
  relocation and the raw-only acquisition cap amendment become
  project-complete; authorize nothing executable.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-j-r1/workspace-relocation-raw-cap-amendment`.

## 2. SHAs

- **`main` SHA before merge:** `27dbc5723f3f068c34663ec57cd85a0e6b42f501`
  (`docs(phase-4bn-i): finalize merge closeout shas`).
- **Branch / docs commit SHA:** `3f792a6257271ae63d1ead4e77c8d30101f478e8`
  (`docs(phase-4bn-j-r1): amend workspace path and raw cap`).
- **Merge commit SHA:** `f63ded86bbc3d010f3f329f40ef2e3bb9df091f6`
  (`docs(phase-4bn-j-r1): merge workspace relocation raw cap amendment`).
- **Merge-closeout commit SHA:** `<to be filled at SHA-finalization>`
  (`docs(phase-4bn-j-r1): add merge closeout`).
- **SHA-finalization commit SHA:** `<to be filled at SHA-finalization>`
  (`docs(phase-4bn-j-r1): finalize merge closeout shas`).
- **Final `main` / `origin/main` SHA after push:**
  `<to be filled at SHA-finalization>`
  (`main == origin/main` verified in sync after push).

## 3. Merge method

- `git merge --no-ff` with `ort` strategy (no fast-forward).
- Merge commit message:
  `docs(phase-4bn-j-r1): merge workspace relocation raw cap amendment`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

**Docs (4 files):**

- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j_acquisition-stop-report.md`
  (added; the Phase 4bn-J **stop report**, previously untracked, now
  committed byte-for-byte as **tracked documentation — a stop report, not
  a closeout**).
- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j-r1_workspace-relocation-raw-cap-amendment.md`
  (added; the amendment memo; 17 sections).
- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j-r1_closeout.md`
  (added; the phase closeout).
- `docs/00-meta/current-project-state.md`
  (modified; narrow, purely additive: 308 insertions, 0 deletions — new
  Phase 4bn-J-R1 prose paragraph + new `Current phase:` block; all prior
  paragraphs / blocks preserved as labelled historical context).

**Source:** none. **Tests:** none. **Scripts:** none. **Config:** none.

No `data/microstructure/` file was modified. No `data/research/` file was
modified. No manifest, sidecar, gate report, or successor-state artefact
was modified. No prior finalized Phase 4bn-I file was modified; no Phase
4bn-I history was rewritten; no Phase 4bn-I merge-closeout was edited. The
process standard
`docs/00-meta/process/claude-code-lightweight-workspace-standard.md` was
**not** modified (deliberately deferred to a separate §15-compliant phase;
see §11 and §16). `pyproject.toml`, `README.md`, `.gitignore`, and MCP
files were left byte-identical.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 308 ++++++++++
 .../2026-05-31_phase-4bn-j-r1_closeout.md          | 285 ++++++++++
 ...-j-r1_workspace-relocation-raw-cap-amendment.md | 623 +++++++++++++++++++++
 ...26-05-31_phase-4bn-j_acquisition-stop-report.md | 340 +++++++++++
 4 files changed, 1556 insertions(+)
```

This matches the expected change set from the merge authorization prompt
exactly: add the stop report, add the amendment memo, add the closeout,
modify `current-project-state.md` — no source / test / script / config /
manifest / sidecar / gate-report / successor-state / data change.

## 6. Verdict

**MEMO RECORDED — workspace relocation + raw-only acquisition cap
amendment is now project-complete on `main`.**

Phase 4bn-J-R1 records the relocation of the active local repository from
`C:\Prometheus` to `D:\Prometheus` and of the Claude Code lightweight
workspace from `C:\ClaudeRuns\prometheus-light` to
`D:\ClaudeRuns\prometheus-light`; preserves the Phase 4bn-J stop report as
tracked documentation (a stop report, not a closeout); and amends the
Phase 4bn-I disk-footprint cap as **raw-only** (10 GiB warning / 25 GiB
hard) **for the acquisition-only retry only**, leaving the runtime cap
(2 h / 4 h) and every other Phase 4bn-I boundary intact. The decision is
`RECOMMEND_AUTHORIZE_REVISED_ACQUISITION_ONLY_RETRY__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
Lifecycle state after this merge-closeout: **merge-closeout recorded
(project-complete on `main`)**. Recommended state: **remain paused**. No
successor authorized; manifest / artefact state unchanged.

## 7. Local gitignored outputs (if any)

**None.** Phase 4bn-J-R1 produced no local artefact under
`data/microstructure/` or `data/research/`. No CSV, JSON, parquet,
manifest, sidecar, gate report, successor-state file, `.duckdb`, or
`.sqlite` file was created. No diagnostic, ML, simulation, backtest, or
acquisition kernel was invoked. The only untracked transient,
`.claude/scheduled_tasks.lock`, is a Claude Code scheduler artefact and
was not committed.

## 8. Validation results

Phase 4bn-J-R1 is a docs-only Tier 1 merge phase that adds / modifies no
code surface. The relevant validation surface is git status, diff review,
`git diff --check`, `git remote -v`, and SHA checks (the Phase 4bn-I /
4bn-H / 4bn-G precedents recorded the same omission rationale for ruff /
mypy / pytest on docs-only phases).

- `git status --short` (post-merge, pre-finalization) — only the expected
  untracked `.claude/scheduled_tasks.lock`; no tracked modifications; no
  `data/research/` or `data/microstructure/` artefact staged.
- `git diff --check` — clean (no whitespace errors).
- `git diff --name-status main..branch` (pre-merge) — exactly:
  `M  docs/00-meta/current-project-state.md`,
  `A  .../2026-05-31_phase-4bn-j-r1_closeout.md`,
  `A  .../2026-05-31_phase-4bn-j-r1_workspace-relocation-raw-cap-amendment.md`,
  `A  .../2026-05-31_phase-4bn-j_acquisition-stop-report.md`.
- `git diff --stat main..branch` (pre-merge) — `4 files changed, 1556
  insertions(+)`; `current-project-state.md` change is additive
  (308 insertions, 0 deletions).
- `git remote -v` — `origin` →
  `https://github.com/jpedrocY/Prometheus.git` (fetch + push), intact and
  not re-pointed.
- SHA checks — recorded in §2.
- ruff / mypy / pytest — not run; docs-only phase with no code surface;
  rationale above.
- No acquisition script, ML script, diagnostics script, or backtest
  script was run during merge review; no endpoint was called; no local
  data was inspected; no test-holdout data was touched.

## 9. Upstream immutability evidence (if applicable)

**n/a — phase did not access any local artefact.** Phase 4bn-J-R1
created, read, hashed, and mutated no `data/microstructure/` or
`data/research/` artefact, no manifest, no sidecar, no gate report, and no
successor-state file. No prior local artefact required bit-for-bit
preservation by this docs-only amendment. The preserved Phase 4bn-J stop
report was committed byte-for-byte as written by the stopped attempt.

## 10. Manifest state preservation (if applicable)

**n/a for mutation — no manifest was touched.** No manifest file under
`data/microstructure/manifests/` or `data/manifests/` was created, read,
or modified. No `research_eligible` flip; no `eligibility_gate_status`
transition; no `chronological_split_policy` change; no
`diagnostics_authorized` / `ml_authorized` change. All existing manifests
remain `research_eligible: false`, `eligibility_gate_status: "pending"`,
label manifest `chronological_split_policy: "not_yet_defined"` as before.
Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked). Any future
acquisition-retry manifest must start non-eligible.

## 11. Boundary confirmations

- no source code modified;
- no test modified;
- no committed script modified (no script modification was required to
  preserve the stop report as docs);
- no config / `.gitignore` / `pyproject.toml` / `README.md` / MCP file
  modified;
- no `docs/00-meta/process/claude-code-lightweight-workspace-standard.md`
  modification (deliberately deferred: it was not named in the phase's
  allowed tracked files and its own §15 change-control requires a phase
  that names it; its principle is preserved and its `C:` path strings are
  superseded by this amendment + `current-project-state.md` for the active
  convention, pending a separate §15-compliant update phase);
- no prior finalized Phase 4bn-I file modified; no Phase 4bn-I history
  rewritten; no Phase 4bn-I merge-closeout edited;
- no `data/microstructure/` artefact committed; no `data/research/`
  artefact committed;
- no `data/microstructure/` or `data/research/` artefact created,
  modified, moved, read, or hashed;
- no local parquet / CSV / JSON output read or inspected;
- no manifest mutated; no `research_eligible` flipped; no
  `eligibility_gate_status` transitioned; no `chronological_split_policy`
  changed;
- no successor-state artefact mutated, created, moved, or accessed;
- no prior gate report mutated;
- no archive downloaded; no data acquired; no public / Binance /
  authenticated / private endpoint called; no `data.binance.vision`
  contacted; no WebSocket / user stream opened;
- no acquisition code written; no new acquisition script created;
- no ML model trained / scored; no prediction generated; no feature
  ranked / selected / pruned / engineered; no hyperparameter or threshold
  tuned; no calibrator fitted; no strategy defined / run; no signal
  generated; no PnL simulated; no backtest run;
- test holdout not used for any reason; sealed v002 split
  2025-02-14..2025-02-28 untouched; Phase 4bn-B `test_rows_loaded: 0` and
  the `iter_partitions(split="test", ...)` always-raise pattern preserved;
- no v003 dataset created; no new dataset family; no new label / feature /
  horizon / symbol acquisition; no mark-price / spot / cross-venue /
  order-book / tick acquisition;
- no storage migration; no database created; no Parquet compaction; no
  `.duckdb` / `.sqlite` file created; no partitioning / compression /
  dataset-layout change;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used;
- the stopped Phase 4bn-J branch
  (`phase-4bn-j/acquisition-only-btcusdt-aggtrades-12m`) was **not**
  merged, **not** treated as branch-complete, and **not** deleted;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment;
  no successor authorized.

## 12. Retained verdict ledger

All preserved verbatim:

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

All preserved verbatim. None of Phase 4bn-A through Phase 4bn-J-R1
establishes edge, profitability, tradability, strategy-readiness,
signal-readiness, paper / shadow readiness, or live-readiness.

## 13. Preserved project locks

All preserved verbatim:

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
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `flip_research_eligible(...)` always-raises invariant (never
  invoked)
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable
  non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard — **principle
  preserved**; its `C:` example path strings superseded by this amendment
  for the active convention pending a separate §15-compliant update phase

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bn-J-R1 merge does not, and cannot, be construed as
authorizing:

- any acquisition; any archive download; any endpoint call (public,
  Binance, authenticated, or private); any WebSocket or user stream;
- any acquisition code; any script modification;
- any credentials; any `.env`; any `.mcp.json`; any MCP; any Graphify;
- any local parquet / data/research / data/microstructure read;
- any diagnostics; any ML training; any model scoring; any predictions;
  any feature ranking / selection / pruning / engineering; any
  hyperparameter tuning; any threshold tuning; any calibration fitting;
- any strategy research; any signal generation; any PnL simulation; any
  backtests; any test-holdout access;
- any manifest mutation; any successor-state mutation; any gate-report
  mutation;
- any data/research or data/microstructure artefact creation or commit;
- any storage migration; any database creation; any Parquet compaction;
  any v003; any extra symbol / horizon / mark-price / spot / cross-venue /
  order-book / tick data;
- the derived normalized / feature / label cap expansion (the raw-only
  cap amendment does **not** extend to the derived stack, which requires a
  separate future derived-stack disk budget — planning warning only:
  ~150–250 GiB plausible, ~300 GiB comfortable; exact cap set in the
  future derivation / gate phase, not here);
- any paper / shadow; any live-readiness; any deployment; any
  exchange-write; any production keys;
- the revised acquisition-only retry itself (recommended only; not
  authorized);
- any Phase 4bn-J-R2; any Phase 5; any Phase 4 canonical; any successor
  phase whatsoever.

## 15. Successor authorization

**None.**

The following candidate successors are explicitly **not** authorized by
this merge:

- the revised acquisition-only retry (Phase 4bn-J-R1's recommendation;
  subject to separate operator authorization; bounded exactly by the
  amendment memo §7–§14);
- Phase 4bn-J (the stopped attempt) — not resumed, not authorized;
- Phase 4bn-J-R2 — not authorized;
- a docs-only source-policy documentation memo (backfill
  `historical-data-spec.md` with the aggTrades-archive convention);
- a docs-only derived-stack storage-budget memo;
- a docs-only process-doc update phase that names
  `docs/00-meta/process/claude-code-lightweight-workspace-standard.md` in
  its allowed tracked files to refresh its `C:` path strings to `D:`;
- any acquisition phase; any storage-migration phase; any
  database-creation phase; any v003-creation phase; any Parquet-compaction
  phase;
- any ML implementation / model training / model scoring / feature
  ranking / feature selection;
- any strategy / signals / PnL / backtest;
- Phase 5; Phase 4 canonical;
- paper / shadow; live-readiness; deployment; exchange-write; production
  keys; authenticated APIs; private endpoints; user stream; MCP; Graphify;
  `.mcp.json`; credentials.

A successor becomes authorized only by a separate operator decision with
its own authorization prompt, after this merge-closeout exists on `main`.

## 16. Recommended state

**Remain paused.**

Phase 4bn-J-R1 is now **merge-closeout recorded (project-complete on
`main`)**. The default and recommended state is to remain paused. The
operator may, as separate decisions:

- remain paused (default);
- separately authorize the revised acquisition-only retry after this merge
  (bounded exactly by the amendment memo §7–§14; raw-only 10 GiB / 25 GiB
  cap; 2 h / 4 h runtime cap; BTCUSDT aggTrades 2024-03-01..2024-11-30;
  v002 terminal window and sealed split untouched; Parquet canonical; no
  v003 / ETHUSDT / mark-price / spot / cross-venue / order-book / tick;
  must remain acquisition-only);
- separately authorize a docs-only source-policy documentation memo;
- separately authorize a docs-only derived-stack storage-budget memo;
- separately authorize a docs-only process-doc update phase for the
  lightweight-workspace standard's `D:` path strings;
- reject further ML-baseline successors and close the ML arc.

**Conditional next, NOT authorized.** The revised acquisition-only retry
is the cleanest non-paused option. It would, under a separate operator
authorization, acquire only the 275 new pre-v002 raw aggTrades days
(2024-03-01..2024-11-30) for BTCUSDT Binance USDⓈ-M futures under the
amended raw-only 10 GiB / 25 GiB cap and the preserved 2 h / 4 h runtime
cap, preserving the v002 terminal window and sealed test split untouched,
keeping Parquet canonical and manifests non-eligible, and committing no
data. It is **not** authorized by this merge.

**No acquisition / ML / diagnostics / strategy / PnL / backtest /
storage-migration / database-creation / Parquet-compaction / v003 /
paper / shadow / live / exchange-write option is valid from this state
unless separately authorized after this merge.**
