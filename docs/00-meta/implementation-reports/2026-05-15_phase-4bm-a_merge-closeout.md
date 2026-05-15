# Phase 4bm-A — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bm-A — Multi-Day Normalization Design Memo
- **Type:** docs-only design memo (Tier 1 — Full Phase under
  `docs/00-meta/process/phase-risk-tiering-standard.md`, because
  Phase 4bm-A defines the future v002 multi-day derived dataset
  family identity, schema contract, partitioning, manifest shape,
  and 65-criterion strict-fail-closed validation contract that any
  future Phase 4bm-B implementation must follow verbatim).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bm-A branch onto `main` and
  record the project-complete merge-closeout. Phase 4bm-A authored
  the v002 multi-day normalization design memo, the Phase 4bm-A
  closeout, and a narrow `current-project-state.md` update
  (Phase 4bm-A narrative paragraph + new "Current phase:" block;
  prior Phase 4bl-F "Current phase:" block preserved verbatim as
  historical context). Without this merge plus this merge-closeout,
  Phase 4bm-A is branch-complete only and is not project-complete.
- **Target branch:** `main`.
- **Source branch:** `phase-4bm-a/multi-day-normalization-design-memo`.

## 2. SHAs

- **`main` SHA before merge:** `ac3475acd332978bfe0037a24e5004cec5e84efc`
  (Phase 4bl-F merge-closeout commit on `main`).
- **Branch commit SHAs:**
  - `fba78ef008b78240b5624c6457b1f12caa207044` —
    `docs(phase-4bm-a): design multi-day aggtrades normalization`
    (the single Phase 4bm-A branch commit; contained the design memo,
    the Phase 4bm-A closeout, and the `current-project-state.md`
    Phase 4bm-A narrative paragraph + new "Current phase:" block).
- **Merge commit SHA:** `af97285f1c3a594a23d1da4adaff281e1de30d84`
  (`docs(phase-4bm-a): merge multi-day normalization design memo`).
- **Merge-closeout commit SHA:** to be filled at commit time of this
  merge-closeout file.
- **Final `main` / `origin/main` SHA after push:** to be filled at
  push time of the merge-closeout commit.

## 3. Merge method

- `git merge --no-ff phase-4bm-a/multi-day-normalization-design-memo`
- Strategy: `ort` (the default).
- Merge commit message: `docs(phase-4bm-a): merge multi-day
  normalization design memo`.
- Pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing.

## 4. Files brought forward by the merge

Docs added (2):

- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_multi-day-normalization-design-memo.md`
  — the 13-section Phase 4bm-A design memo.
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_closeout.md`
  — the Phase 4bm-A closeout.

Docs modified narrowly (1):

- `docs/00-meta/current-project-state.md` — Phase 4bm-A narrative
  paragraph inserted before the prior Phase 4bl-F paragraph; new
  Phase 4bm-A "Current phase:" block; prior Phase 4bl-F "Current
  phase:" block preserved verbatim under a new
  "Earlier Phase 4bl-F 'Current phase:' block (preserved here for
  continuity; Phase 4bl-F is no longer the current phase):"
  historical-context section.

Source: not modified.
Tests: not modified.
Scripts: not modified.
Configs (`pyproject.toml`, `README.md`, `.gitignore`,
`.gitattributes`, MCP files): not modified.
Process standards (`docs/00-meta/process/...`): not modified.
Prior implementation reports / merge-closeouts: not modified.
`data/microstructure/`: not modified — every existing artefact
(raw zips, raw manifests including v001 + v002, sidecars, acquisition
logs, normalized parquet, derived manifest, feature parquet, feature
manifest, label parquet, label manifest, every gate report including
Phase 4bb-D / Phase 4bf / Phase 4bi-B / Phase 4bj-E / Phase 4bl-D /
Phase 4bl-D-R, every successor-state artefact including Phase 4bb-G /
Phase 4bg-B / Phase 4bi-D / Phase 4bj-G / Phase 4bj-J / Phase 4bl-E,
every canonicalization report including Phase 4bl-D-S2) is
byte-identical pre/post.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 364 ++++++++
 .../2026-05-15_phase-4bm-a_closeout.md             | 285 +++++++
 ...se-4bm-a_multi-day-normalization-design-memo.md | 935 +++++++++++++++++++++
 3 files changed, 1584 insertions(+)
```

The diff matches the expected change set from the Phase 4bm-A
authorization prompt verbatim: 2 new docs files under
`docs/00-meta/implementation-reports/`, 1 narrowly modified docs
file (`docs/00-meta/current-project-state.md`), no source / test /
script / config / data files modified.

## 6. Verdict

**MEMO RECORDED.**

Phase 4bm-A is now project-complete, having been merged into `main`
and closed out by this merge-closeout. The merge added the v002
multi-day normalization design memo and recorded the Phase 4bm-A
closeout. The design memo translates the Phase 4bc v001 single-day
normalization design pattern (originally written for the Phase 4az
BTCUSDT 2025-01-15 raw archive) onto the Phase 4bl-C v002 multi-day
raw aggTrades family (90 contiguous UTC dates 2024-12-01 through
2025-02-28; BTCUSDT only; 155,153,449 rows; 1,943,823,208 bytes).
Locked design decisions: (1) family name reuse —
`microstructure_normalized_aggtrades_v001` is preserved unchanged
because the schema is byte-identical, while `dataset_version` bumps
from `v001` to `v002` mirroring the raw family pattern; (2) the
19-column `NORMALIZED_SCHEMA_V001` contract is preserved verbatim
with `schema_version="v001"`, Decimal-as-string for `price` and
`quantity`, and float storage forbidden; (3) per-day Parquet partition
layout under `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/`
producing 90 Parquet files + 90 paired canonical Phase 4bb-F sidecars,
~20.6 GiB estimated; (4) one multi-day index manifest at
`data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`
with 90-entry `per_file_inventory` mirroring the v002 raw manifest
shape; (5) 65-criterion strict-fail-closed normalization-time
validation contract across six groups; (6) Phase 4ba 5-stage
eligibility ladder applied prospectively to the v002 derived family
with the Phase 4aw `flip_research_eligible(...)` always-raises
invariant preserved at every stage transition; (7) source-data
lineage cited verbatim including the Phase 4bl-D-R PASS gate report
SHA and the Phase 4bl-E successor-state SHA. Phase 4bm-A also
invokes the nine Phase 4bl-F reusable non-authorization blocks
(N-ACQUISITION, N-ENDPOINT, N-CREDENTIALS, N-MANIFEST, N-GATE-RERUN,
N-SUCCESSOR-STATE, N-DERIVATION, N-DIAGNOSTICS-ML-STRATEGY,
N-PHASE-5, N-VERDICT-LOCK) verbatim. No retained verdict was
revised. No project lock was changed. No `data/microstructure/`
artefact was created or modified. No `research_eligible` flag was
flipped on any actual manifest. No `eligibility_gate_status` was
transitioned on any actual manifest. No `chronological_split_policy`
was changed on any actual manifest. No gate was rerun. No new gate
report was created. No successor-state artefact was created. No
data was acquired. No normalization was executed. No successor
phase is authorized. **Recommended state: remain paused.**

## 7. Local gitignored outputs (if any)

**None.** Phase 4bm-A was a docs-only Tier 1 design phase. No local
artefacts were produced under `data/microstructure/` or anywhere
else outside the tracked docs.

## 8. Validation results

- `git status` (pre-merge, on branch `phase-4bm-a/multi-day-normalization-design-memo`):
  clean except pre-existing untracked `.claude/scheduled_tasks.lock`
  and `data/research/`.
- `git rev-parse main` (pre-merge): `ac3475acd332978bfe0037a24e5004cec5e84efc`.
- `git rev-parse origin/main` (pre-merge): `ac3475acd332978bfe0037a24e5004cec5e84efc`.
- `main == origin/main` (pre-merge): YES (in sync).
- `git diff --stat main..phase-4bm-a/multi-day-normalization-design-memo`:
  3 files changed, 1584 insertions(+), 0 deletions(-).
- `git diff --name-status main..phase-4bm-a/multi-day-normalization-design-memo`:
  `M docs/00-meta/current-project-state.md`,
  `A docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_closeout.md`,
  `A docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_multi-day-normalization-design-memo.md`.
- `git diff --check main..phase-4bm-a/multi-day-normalization-design-memo`:
  clean (no whitespace errors).
- `git merge --no-ff` produced merge commit
  `af97285f1c3a594a23d1da4adaff281e1de30d84` with `ort` strategy.
  No conflicts.
- `git status` (post-merge, on `main`): clean except pre-existing
  untracked `.claude/scheduled_tasks.lock` and `data/research/`.
- `git log --oneline -5 --decorate` (post-merge): confirms merge
  commit `af97285` at HEAD on top of branch commit `fba78ef` on top
  of Phase 4bl-F merge-closeout commit `ac3475a`.
- `ruff` / `mypy` / `pytest` — **not run.** Per the
  `operator-report-standard.md` and the Phase 4bm-A authorization
  prompt, no source / test / script / configuration file was modified
  by Phase 4bm-A or by this merge, so no whole-repo code-quality
  gate was rerun. The latest authoritative whole-repo validation
  remains the Phase 4bb-F-implementation merge baseline (`ruff` PASS,
  `mypy` strict 120 source files PASS, microstructure `pytest` 915
  passed + 1 pre-existing labelled skip, whole-repo `pytest` 1698
  passed + 1 skipped + 2 pre-existing simulation failures).

## 9. Upstream immutability evidence (if applicable)

**n/a — phase did not access any local artefact.** Phase 4bm-A was
a docs-only design memo. It did not access, read, write, or modify
any artefact under `data/microstructure/`. Every prior local artefact
(raw zips, raw manifests including the Phase 4az `__v001` and the
Phase 4bl-C `__v002` raw manifest, sidecars, acquisition logs,
normalized parquet, derived manifest, feature parquet, feature
manifest, label parquet, label manifest, every gate report
including the Phase 4bb-D raw `__v001` 45/45 PASS report, the
Phase 4bf derived 55/55 PASS report, the Phase 4bi-B feature
70/70 PASS report, the Phase 4bj-E label 72/72 PASS report, the
Phase 4bl-D raw multi-day FAIL gate report, the Phase 4bl-D-R raw
multi-day PASS gate report, every successor-state artefact
including Phase 4bb-G raw `__v001`, Phase 4bg-B derived,
Phase 4bi-D feature, Phase 4bj-G label, Phase 4bj-J no-split
determination, Phase 4bl-E raw `__v002`, every canonicalization
report including the Phase 4bl-D-S2 sidecar canonicalization report)
is byte-identical pre/post by virtue of not having been touched.

## 10. Manifest state preservation (if applicable)

**n/a — phase did not touch any manifest.** No manifest field was
read for write purposes, no manifest was modified, no manifest was
created, no manifest was deleted. Every actual on-disk manifest
retains the state recorded by its last authoring phase:

- raw `__v001` manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"` (Phase 4az / 4bb-G).
- raw `__v002` multi-day manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"` (Phase 4bl-C / 4bl-E
  successor-state JSON sibling).
- derived `__v001` manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"` (Phase 4bd / 4bg-B
  successor-state JSON sibling).
- feature `__v001` manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"` (Phase 4bh / 4bi-D
  successor-state JSON sibling).
- label `__v001` manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"`,
  `chronological_split_policy = "not_yet_defined"` (Phase 4bj-C /
  4bj-G successor-state JSON sibling / 4bj-J no-split determination
  JSON sibling).

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked by Phase 4bm-A or
by this merge).

The future derived `__v002` multi-day manifest (proposed by
Phase 4bm-A and only producible by a separately authorized future
Phase 4bm-B) does not yet exist.

## 11. Boundary confirmations

- no source code modified
- no test modified
- no script modified
- no `.gitignore`, `.gitattributes`, `pyproject.toml`, or
  `README.md` modified
- no MCP file modified
- no process standard modified (`docs/00-meta/process/...` untouched)
- no prior implementation report or merge-closeout modified
- no `data/microstructure/` write of any kind
- no `data/microstructure/` artefact committed
- no manifest mutation (raw, derived, feature, or label)
- no `research_eligible` flipped on any actual manifest
- no `eligibility_gate_status` transitioned on any actual manifest
- no `chronological_split_policy` changed on any actual manifest
- no gate rerun (raw `__v001`, raw `__v002`, derived, feature, label)
- no new gate report created
- no successor-state artefact created
- no canonicalization report created
- no normalization run
- no derivation, features, labels, diagnostics, ML, strategy,
  signals, or backtests run
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge
  / prediction / model-score / decision-score / entry-exit / strategy
  output computed
- no data acquired, downloaded, or fetched
- no Binance / public / private endpoint contacted
- no public-endpoint call in code added
- no WebSocket opened
- no user stream opened
- no listenKey lifecycle invoked
- no credential used or referenced
- no `.env` read or created
- no `.mcp.json` read or created
- MCP and Graphify not enabled
- no exchange-write surface touched
- no production-key creation
- no paper / shadow / live-readiness / deployment work
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- Phase 4bb-F canonical path policy preserved (no policy text changed;
  the design memo specifies that any future Phase 4bm-B forward
  writes must conform to canonical Phase 4bb-F format)
- Phase 4bl-F R-SIDECAR-CRLF rule preserved (the design memo
  explicitly notes R-SIDECAR-CRLF is a remediation rule for
  pre-existing non-canonical sidecars and does not apply to forward
  writes by Phase 4bm-B)
- Phase 4bl-F four-tier risk model preserved
- Phase 4bl-F nine reusable non-authorization blocks preserved and
  invoked verbatim by the design memo
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no Phase 4al refined no-rescue rule, §13 boundary, or §14
  hierarchy amendment
- Phase 4bl-D through Phase 4bl-F history preserved verbatim
- no successor authorized

## 12. Retained verdict ledger

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7 (strict integrity gate)
- Phase 3r §8 (mark-price gap governance)
- Phase 3v §8 (stop-trigger-domain governance)
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation
  governance)
- Phase 4j §11 (metrics OI-subset partial-eligibility rule)
- Phase 4k (V2 backtest-plan methodology)
- Phase 4p (G1 strategy-spec)
- Phase 4q (G1 backtest-plan methodology)
- Phase 4v (C1 strategy-spec)
- Phase 4w (C1 backtest-plan methodology)
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant
- Phase 4bb-F canonical path policy
- Phase 4bl-F four-tier risk model + nine reusable non-authorization
  blocks + R-SIDECAR-CRLF standing rule

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bm-A merge does not, and cannot, be construed as
authorising:

- Phase 4bm-B execution (the future Multi-Day Normalization
  Implementation phase that this design memo specifies);
- normalization, derivation, feature computation, label
  computation, or diagnostics;
- creation of any normalized parquet under
  `data/microstructure/normalized/`;
- creation of any derived `__v002` multi-day manifest;
- creation of any new sidecar, gate report, or successor-state
  artefact under `data/microstructure/`;
- ML model training, model selection, strategy hypothesis
  generation, or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write
  work;
- production-key creation, authenticated APIs, private endpoints,
  public-endpoint calls in code, user stream, or live WebSocket
  implementation;
- MCP, Graphify, `.mcp.json`, or credentials work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL
  labels;
- mark-price / spot / cross-venue / order-book / additional
  aggTrades acquisition (beyond the 90 locked BTCUSDT UTC dates
  already acquired by Phase 4bl-C);
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible` or
  `eligibility_gate_status` from this evidence alone;
- changing any manifest's `chronological_split_policy` from this
  evidence alone;
- rescuing R2, F1, D1-A, V2, G1, C1, or any cooled-down family;
- amending the Phase 4bb-F canonical path policy;
- amending the Phase 4bl-F R-SIDECAR-CRLF rule (R-SIDECAR-CRLF
  remains a remediation rule only; it does not apply to forward
  writes by Phase 4bm-B);
- amending the Phase 4bl-F four-tier risk model or nine reusable
  non-authorization blocks;
- amending Phase 4ak M0, the post-null cooldown rule, the
  cooled-down families list, or the memo template;
- amending Phase 4al refined no-rescue rule, §13 boundary, or §14
  hierarchy;
- amending Phase 4aw `flip_research_eligible(...)` always-raises
  invariant;
- pre-authorising any successor phase under any name (Phase 4bm-B,
  Phase 4bm-C, Phase 4bm-D, Phase 4bm-E, Phase 4bm-F, Phase 4bm-*,
  Phase 4bn-*, Phase 4bo-*, Phase 4bp-*, Phase 4bq-*).

## 15. Successor authorization

**None.**

The following candidate successors are explicitly **not** authorized
by this merge:

- Phase 4bm-B — Multi-Day Normalization Implementation (the natural
  conditional successor by direct precedent of Phase 4bd for the
  Phase 4az `__v001` raw family; the design memo specifies what
  Phase 4bm-B must do but does not authorize execution)
- Phase 4bm-C — Multi-Day Normalized Structural QA Memo
- Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate
- Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility
  Decision Memo
- Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording
- Phase 4bm-* (any further multi-day normalization / derived arc)
- Phase 4bn-* (any multi-day feature arc)
- Phase 4bo-* (any multi-day label arc)
- Phase 4bp-* (any multi-day diagnostic arc)
- Phase 4bq-* (any multi-day chronological-split arc)
- Phase 5
- Phase 4 canonical
- normalization (any kind, including v002 multi-day execution)
- derivation
- feature computation
- label computation
- label diagnostics
- ML training / model selection / meta-labeling
- strategy implementation / strategy spec / strategy hypothesis
- signal construction
- backtest design / backtest execution
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production-key creation
- authenticated APIs
- private endpoints
- public-endpoint calls in code
- user stream
- live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h /
  order-book / spot / cross-venue / funding / open-interest data
  acquisition (beyond the 90 locked BTCUSDT UTC dates already
  acquired by Phase 4bl-C)
- any execution under R-SIDECAR-CRLF (R-SIDECAR-CRLF requires a
  separately authorized Tier 2 controlled remediation phase)
- any operator-driven discussion outcome that would unilaterally
  promote any of the above without a separately authorized
  authorization prompt

## 16. Recommended state

**Remain paused.**

The operator has signalled an intent to pause for a broader project
discussion (project complexity, phase usefulness, possible
energy-market sibling project) before any technical successor is
authorized. That stated intent continues to apply.

**Conditional next, NOT authorized:**

Phase 4bm-B — Multi-Day Normalization Implementation (docs-and-code,
Tier 1) is the cleanest non-paused option. It would consume this
Phase 4bm-A design memo verbatim, run a future
`scripts/phase4bm_b_normalize_multiday_aggtrades.py` (or equivalent)
exactly once against the Phase 4bl-C `__v002` 90-date BTCUSDT raw
archive cited by the Phase 4bl-D-R PASS gate report and the
Phase 4bl-E successor-state record, and produce 90 per-day Parquet
files (~20.6 GiB total) plus 90 paired canonical Phase 4bb-F
sidecars plus one multi-day index manifest at
`data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`,
all under the 65-criterion strict-fail-closed validation contract,
with `research_eligible=false` and `eligibility_gate_status=pending`
for the new derived `__v002` manifest. Phase 4bm-B is **not**
authorised by this merge. Operator-driven discussion of project
direction (complexity, phase usefulness, energy-market sibling
project) may also intervene before any future Phase 4bm-B
authorization prompt is issued.
