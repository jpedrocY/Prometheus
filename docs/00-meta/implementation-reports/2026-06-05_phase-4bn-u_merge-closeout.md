# Phase 4bn-U — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-U — Label-Derivation Readiness / Execution Plan.
- **Type:** docs-only / label-derivation readiness / label execution planning /
  label manifest and gate boundary-contract memo.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-U readiness/execution-plan memo, its
  branch closeout, and the narrow `current-project-state.md` update onto `main`
  as project state. Phase 4bn-U determined — from committed repository Markdown
  and committed code/tests only, reading no local data — whether the project can
  safely authorize a future label-only execution phase for the Phase 4bn-S /
  4bn-T pre-v002 BTCUSDT Binance USDⓈ-M futures aggTrades feature segment
  (2024-03-01 .. 2024-11-30 inclusive UTC). The phase decided
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_LABEL_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
  it authorizes no label derivation, no label artefact, no manifest mutation, no
  ML, no diagnostics, no strategy, and no successor.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-u/label-derivation-readiness-execution-plan`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (full 16-section
  merge-closeout required).

## 2. SHAs

- **`main` SHA before merge:** `28e1683646499a910186efdf48d4a5d01a23e630`
  (`docs(phase-4bn-t): finalize merge closeout shas`).
- **Branch commit SHA (memo + closeout + narrow state update):**
  `ced0a79a3dfe098383c9905a94cce41518268ff8`
  (`docs(phase-4bn-u): plan label derivation readiness`).
- **Merge commit SHA:** `4f0bc5b48bab4d62657e791ce33b09d2afac63cc`
  (`docs(phase-4bn-u): merge label derivation readiness plan`).
- **Merge-closeout commit SHA:** `062b8f094faffafbded0afcc825d8075b796cf51`
  (`docs(phase-4bn-u): add merge closeout`).
- **SHA-finalization commit SHA:** this commit
  (`docs(phase-4bn-u): finalize merge closeout shas`) — its own hash becomes the
  new `main` tip; recorded verbatim in the final operator report after push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization commit;
  `main == origin/main` after push (recorded in the final operator report).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message: `docs(phase-4bn-u): merge label derivation readiness plan`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
  (recorded at the final operator report after the SHA-finalization commit).

## 4. Files brought forward by the merge

- **Docs (3):**
  - `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-U
    compact-ledger paragraph + new `Current phase:` block ahead of the Phase
    4bn-T block; prior Phase 4bn-A … 4bn-T paragraphs and blocks preserved
    verbatim as labelled historical context; 103 insertions, 0 deletions —
    insertion-only);
  - `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-u_label-derivation-readiness-execution-plan.md`
    (added — the implementation report, 21 sections);
  - `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-u_closeout.md`
    (added — branch closeout).
- **Source / tests / scripts / config:** none.
- **`data/microstructure/` files:** **none modified or committed.** No
  `data/research/` file. No manifest, sidecar, gate report, successor-state
  artefact, `.gitignore`, `pyproject.toml`, `README.md`, or MCP file was
  modified. No source module, test, or script was created or modified.

The diff matches the expected change set from the merge authorization prompt
exactly (add 2 files, modify 1 doc).

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 103 +++
 .../2026-06-05_phase-4bn-u_closeout.md             | 135 ++++
 ...-u_label-derivation-readiness-execution-plan.md | 692 +++++++++++++++++++++
 3 files changed, 930 insertions(+)
```

The diff matches the expected change set (insertion-only; docs only; no data,
no code, no tests, no scripts, no config).

## 6. Result / verdict

**MEMO RECORDED — REMAIN PAUSED.** Phase 4bn-U is a docs-only label-derivation
readiness / execution-plan memo. From committed docs and committed tooling only
(no local data read), it established three findings. (1) **Existing label
tooling is reusable only through a bounded new wrapper:** the label kernel
`compute_aggtrade_labels_v002_for_day`, schema (`labels_schema_v002.py`,
`LABEL_SCHEMA_V002`, 40 columns), validation, IO, and gate-check modules are
reusable, but the multiday orchestrator
`scripts/phase4bm_o_compute_multiday_labels.py` is hardcoded to the published
v002 family (15 locked precondition SHAs incl. the Phase 4bm-L Stage-5
research-use successor-state, `EXPECTED_FEATURE_CONFIG_HASH=819cfa7a…`, the v002
90-day window constants 2024-12-01 .. 2025-02-28, and the single `__v002`
manifest basename / output dir), and the `multiday_label_gate` input contract is
v002-lineage-shaped and requires a Stage-5 successor-state the non-eligible
pre-v002 segment does not have — so a future label phase must add a bounded
`phase4bn_*` wrapper + segment-scoped gate + segment-scoped path/manifest
helpers + new offline tests, exactly as Phase 4bn-O/4bn-S did. (2) **Label
manifest/versioning requires a docs-only memo:** the v002 `label_config_hash`
and lineage model bind a Stage-5 feature successor-state and Phase 4bm-J/L/F/D
lineage absent for the pre-v002 segment; the pre-v002 feature_config_hash
(`0726b41d…`) differs from the v002 lock (`819cfa7a…`); the envelope terminal
must be re-locked to the pre-v002 terminal; and segment naming must be settled —
none of which the Phase 4bn-R *feature* manifest memo resolved for *labels*. (3)
**Sealed-test / v002-terminal boundary is clear and safe for a conservative
pre-v002-only label run** with `envelope_terminal_unix_ms` set to the pre-v002
segment terminal (2024-11-30); the 1s/5s/15s/60s forward horizons censor at the
boundary and never read 2024-12-01+ (v002 terminal) or 2025-02-14..28
(sealed-test) data, so a holdout-boundary memo is **not** required for the
conservative scope. Label-only execution is feasible in principle but premature
until the manifest/versioning shape is settled. Decision:
`RECOMMEND_AUTHORIZE_DOCS_ONLY_LABEL_MANIFEST_VERSIONING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
The merge lands the memo + closeout + narrow state update on `main`; the project
remains paused; the pre-v002 feature/normalized segments remain **non-eligible**
(`research_eligible: false`, `eligibility_gate_status: "pending"`); no manifest
eligibility transition occurred.

## 7. Local gitignored outputs (if any)

**None.** Phase 4bn-U is docs-only: it produced no local artefact, read no local
data, and created nothing under `data/microstructure/` or `data/research/`.
`git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88` (the pre-existing local
gitignored Phase 4bn-O/4bn-S/4bn-T artefacts remain local, uncommitted, and were
not accessed by this phase).

## 8. Validation results

Docs-only merge-review validation (no code/test/script/config surface; no
acquisition, gate, normalization, feature, label, ML, diagnostics, strategy, or
backtest run):

- `git diff --check` → clean (no whitespace errors / conflict markers).
- `git diff --name-status main..branch` (pre-merge) → exactly the 3 expected
  files (M `current-project-state.md`; A closeout; A implementation report).
- `git diff --stat main..branch` (pre-merge) and the merge diff → `3 files
  changed, 930 insertions(+)` (insertion-only).
- `ruff` / `mypy` / `pytest` → **not run; not required.** Phase 4bn-U adds no
  code, tests, scripts, or config surface; the validation surface for a docs-only
  phase is git status, diff review, `git diff --check`, gitignore confirmation,
  and SHA checks. No repo-standard Markdown validator that runs without producing
  outputs / mutating artefacts is configured; none was run.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only `.claude/scheduled_tasks.lock` untracked; no
  `data/microstructure/` or `data/research/` artefact staged or committed; the
  merge committed exactly the 3 tracked docs files (no `data/` file).

## 9. Upstream immutability evidence

**n/a — phase did not access any local artefact.** Phase 4bn-U read no local
Parquet, manifest, sidecar, gate report, or zip; it referenced upstream
artefacts only by their committed-document SHAs (Phase 4bn-S feature segment
manifest `4881eb87…b52` / feature_config_hash `0726b41d…`; Phase 4bn-O
normalized segment manifest `0e96ae37…d9fa`; Phase 4bn-P normalized-layer gate
report `3452fd9d…f134`; the published-v002 label tooling lock `819cfa7a…`) cited
from committed reports, not by hashing local data. No `data/microstructure/`
file was read or modified by the phase or the merge.

## 10. Manifest state preservation

- **Phase 4bn-S feature segment manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; unchanged — no transition (referenced by
  document SHA only; not read or mutated).
- **Phase 4bn-O normalized segment manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; unchanged — no transition.
- **Published normalized / feature / label `__v002` manifests:** untouched; no
  transition.
- No `chronological_split_policy`, `diagnostics_authorized`, or `ml_authorized`
  transition occurred.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
  invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code created or modified; no test created or modified; no script
  created or modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no manifest / sidecar / gate report / successor-state artefact created or
  modified;
- no `data/microstructure/` or `data/research/` artefact opened, hashed,
  counted, inspected, created, staged, or committed;
- no local raw zip / normalized Parquet / feature Parquet / label file / gate
  report / manifest read under `data/microstructure`;
- no v002 terminal raw window read; no v002 terminal normalized window read; no
  sealed-test split read;
- no label derivation; no label artefact / manifest creation or mutation; no
  targets / future returns; no barrier / target-before-stop / MFE / MAE /
  R-multiple / PnL labels;
- no feature execution rerun; no feature-layer gate rerun; no normalization
  rerun; no raw-gate rerun; no normalized-layer-gate rerun;
- no ML / model scoring / predictions; no diagnostics; no strategy / signal /
  PnL / backtest; no feature ranking / selection / pruning; no label
  optimization / threshold / hyperparameter / calibration tuning;
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
- Phase 4bl-F four-tier risk model
- Phase 4bn-J-R1 raw-only cap amendment
- Phase 4bn-L derived-stack storage budget (carried forward by this memo)
- Phase 4bn-N normalization manifest/versioning convention
- Phase 4bn-R feature manifest/versioning convention + non-eligible-source
  precondition

All prior phase results preserved verbatim. Phase 4 canonical remains
unauthorized.

## 14. No-rescue constraints

The Phase 4bn-U merge does not, and cannot, be construed as authorising:

- the docs-only label manifest/versioning memo it recommends (recommended only,
  NOT authorized), a holdout-boundary memo, a source-policy memo, or a
  process-doc path update;
- label-only execution; label derivation / label gate; targets; future returns;
  barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels; 30s / 5m /
  30m / 1h / 4h / longer-horizon label generation; extra horizons beyond the
  committed 1s/5s/15s/60s label policy;
- ML model training / selection / scoring, predictions, strategy hypothesis
  generation, signal construction, position state, entry/exit rules,
  diagnostics, or backtest design;
- feature ranking / selection / pruning / engineering / hyperparameter /
  threshold / calibration tuning;
- a chronological-split / holdout policy decision or transition;
- paper / shadow / live-readiness / deployment / exchange-write / production-key
  work; Phase 4 canonical or Phase 5 authorisation;
- mark-price / spot / cross-venue / order-book / tick / additional aggTrades /
  ETHUSDT acquisition; v003 creation;
- reading the v002 terminal raw/normalized/feature window or sealed-test split;
  mutating the published normalized / feature / label `__v002` family;
- database creation / DuckDB / SQLite / Parquet compaction / storage migration;
- transitioning any manifest's `research_eligible` or `eligibility_gate_status`
  from this docs-only readiness plan alone;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening.

## 15. Successor authorization

**None.**

Not authorized (candidates a future operator might consider):

- a docs-only label manifest/versioning memo (Phase 4bn-U's recommendation —
  requires separate operator authorization);
- a label-only execution phase (preferred follow-on, but only after the
  manifest/versioning shape is settled, or with deliberate acceptance of
  manifest/versioning resolution inside that execution phase);
- a docs-only holdout-boundary memo (only if a future scope reads the v002
  terminal raw/normalized/feature window or sealed-test dates);
- a source-policy documentation memo; a process-doc `D:` path-string update;
- a label-layer eligibility gate; a chronological-split / holdout policy memo;
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

Phase 4bn-U is now **merge-complete on `main`** as of merge commit
`4f0bc5b48bab4d62657e791ce33b09d2afac63cc` and the subsequent merge-closeout +
SHA-finalization commits. Project completion of this phase requires the
SHA-finalization commit (`docs(phase-4bn-u): finalize merge closeout shas`) per
the repository's merge-closeout convention. The pre-v002 feature and normalized
segments remain **non-eligible** (`research_eligible: false`,
`eligibility_gate_status: "pending"`); no manifest eligibility transition
occurred. v003 remains forbidden and absent; the published `__v002`
normalized/feature/label families remain immutable; the v002 terminal
raw/normalized window remains by-reference only and unread; the sealed-test
split remains untouched.

**Conditional next, NOT authorized:** a separately-authorized **docs-only label
manifest/versioning memo** is the cleanest non-paused option. It would settle the
segment label family naming (analogous to `…__v002_pre_v002_segment_4bn_s`), the
`label_config_hash` field set and re-mapped lineage columns for a non-eligible,
successor-state-free segment, and the pre-v002 envelope terminal — before any
label execution. It is **not** authorized by this merge.

### Readiness findings (preserved)

- **Existing label tooling: reusable only through a bounded new wrapper.** Kernel
  / schema / validation / IO / gate-check modules reusable; orchestrator and
  multiday label gate hardcoded to the published v002 family (15 locked SHAs;
  `EXPECTED_FEATURE_CONFIG_HASH=819cfa7a…`; v002 90-day window;
  `__v002` manifest basename; Phase 4bm-L Stage-5 successor-state dependency).
- **Label manifest/versioning: requires a docs-only memo.** v002
  `label_config_hash` + lineage bind a Stage-5 successor-state and Phase
  4bm-J/L/F/D lineage the pre-v002 segment lacks; pre-v002 feature_config_hash
  `0726b41d…` ≠ v002 lock `819cfa7a…`; envelope terminal + segment naming
  unsettled; Phase 4bn-R settled the feature manifest, not the label manifest.
- **Sealed-test / v002-terminal boundary: clear and safe** for a conservative
  pre-v002-only label run (envelope terminal = pre-v002 segment terminal at
  2024-11-30; 1s/5s/15s/60s horizons censor at the boundary; v002 terminal
  2024-12-01+ and sealed-test 2025-02-14..28 by reference only / unread).
- **Holdout-boundary memo not required** for the conservative pre-v002-only
  scope; required only if a future design proposes reading v002-terminal or
  sealed-test dates.
- **Label-only execution feasible in principle but premature** until the label
  manifest/versioning shape is settled.

### Future label scope recommended (preserved)

- Symbol BTCUSDT only; market Binance USDⓈ-M futures only; family aggTrades only.
- Input feature layer: Phase 4bn-S pre-v002 feature segment only, 2024-03-01 ..
  2024-11-30 inclusive UTC.
- Input normalized layer: Phase 4bn-O pre-v002 normalized segment only, for
  anchor/reference prices.
- Existing v002 terminal raw/normalized/feature families **by reference only**;
  no v002 terminal reads; no sealed-test reads.
- Output: 275 per-day non-eligible label Parquet + 275 canonical sidecars + 1
  segment-scoped non-eligible label manifest + 1 manifest sidecar, under
  `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_<label-phase-id>/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY-MM-DD>.parquet`.
- Label artefacts only; no ML outputs / diagnostics / strategy / PnL / backtests
  / research outputs; no database; no Parquet compaction; no v003; nothing
  committed under `data/microstructure` or `data/research`.

### Label semantics (preserved)

- Existing label family `microstructure_labels_aggtrades_v001 @ v002`; schema
  exactly `LABEL_SCHEMA_V002`, 40 columns (17 lineage + `label_config_hash` + 8
  label + 14 support).
- Horizons 1s / 5s / 15s / 60s; 8 labels
  `forward_log_return_{1s,5s,15s,60s}` + `forward_direction_{1s,5s,15s,60s}`;
  14 support columns (per-horizon `reference_row_index`,
  `reference_timestamp_ms`, `horizon_censored_flag`, plus
  `label_invalid_price_flag`, `label_any_censored_flag`).
- Causal forward-return / forward-direction only; **no barrier / no
  target-before-stop / no stop / no MFE / no MAE / no R-multiple**; no strategy /
  signal / PnL semantics (enforced by the forbidden-substring guard).

### Phase 4bn-L budget carried forward (preserved)

- Label footprint warning 75 GiB / hard cap 125 GiB.
- Label runtime warning 4 h / hard cap 8 h.
- Temporary workspace warning 50 GiB / hard cap 100 GiB.
- Total derived-stack warning 250 GiB / hard cap 300 GiB.
- D: free-space floor ≥ 500 GiB before execution; fail closed below 350 GiB
  during execution.
- Stop before writing if a label preflight estimates label output > 125 GiB,
  total derived-stack > 300 GiB, runtime > 8 h, or D: free space < 500 GiB.

### Future fail-closed stop conditions (preserved by reference)

The future label phase must fail closed on at least: missing feature/sidecar
prerequisite; feature Parquet hash mismatch; feature path outside approved
conventions; missing Phase 4bn-T gate PASS predecessor; source not
`research_eligible=false` / `eligibility_gate_status=pending`; any date outside
2024-03-01 .. 2024-11-30; any ambiguity about reading v002-terminal /
sealed-test dates; any sealed-test use for ML/diagnostics/strategy/research/
tuning/split; any horizon crossing into sealed-test or v002-terminal without a
separately authorized holdout-boundary memo; missing source data; preflight
cannot estimate footprint; output > 125 GiB; total stack > 300 GiB; D: < 500 GiB
before / < 350 GiB during; temp > 100 GiB; runtime > 8 h; output path outside
the approved gitignored labels convention; any `data/research` output; any ML /
diagnostics / strategy / PnL / backtest; any DuckDB/SQLite/database; any Parquet
compaction; any v003; any `research_eligible` flip or `eligibility_gate_status`
transition; any `data/microstructure` or `data/research` commit; any need for
ETHUSDT / mark-price / spot / cross-venue / order-book / tick / extra-horizon
data; any deviation from BTCUSDT / Binance USDⓈ-M futures / aggTrades /
v002-compatible semantics; missing or ambiguous label manifest/versioning
convention; inability to create canonical sidecars; any validator/tooling unsafe
condition; any forbidden-substring column name; any leakage beyond the
authorized horizon/context boundary; any requirement for the sealed test split.

### Explicit confirmations

- Phase 4bn-U is merge-complete on `main` after this merge.
- Project completion requires the SHA-finalization commit
  (`docs(phase-4bn-u): finalize merge closeout shas`).
- The docs-only label manifest/versioning memo / label-only execution / any
  successor is **NOT authorized**.
- `research_eligible` remains `false`; `eligibility_gate_status` remains
  `pending`; no manifest eligibility transition occurred.
- v003 remains forbidden and absent; the published `__v002`
  normalized/feature/label families remained immutable; the v002 terminal
  raw/normalized window remained by-reference only and unread; the sealed-test
  split remained untouched.
- No local data was read; no local data was created; no local
  `data/microstructure` or `data/research` artefact was opened, hashed, counted,
  inspected, created, staged, or committed.
- No acquisition was run, no endpoints were called, no archives were downloaded,
  no HEAD preflight was run, no raw gate was rerun, no normalization was rerun,
  no normalized-layer gate was rerun, no feature execution was rerun, no
  feature-layer gate was rerun, no local raw zip contents were inspected, no
  local normalized Parquet files were read, no local feature Parquet files were
  read, no v002 terminal window was read, no test holdout was touched, no labels
  were derived, no ML was trained, no model scoring was performed, no predictions
  were generated, no diagnostics were run, no backtests were run, no
  strategy/signal/PnL work was performed, no storage migration occurred, no
  database was created, no Parquet was compacted, no v003 dataset was created, no
  manifest eligibility transition occurred, no `data/research` artefacts were
  created or committed, no `data/microstructure` artefacts were created or
  committed, and no paper/shadow/live/exchange-write/credentials/MCP/Graphify
  work was authorized.

### Final git status (at SHA-finalization)

Recorded in the final operator report: working tree clean except the expected
untracked transient `.claude/scheduled_tasks.lock` plus the expected gitignored
local `data/microstructure/` and `data/research/` namespaces; `main ==
origin/main` after push.
