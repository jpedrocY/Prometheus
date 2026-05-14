# Merge-Closeout Standard

## Title

Prometheus Merge-Closeout Standard — required shape of merge-closeout
reports written on `main` after a phase is merged.

## Purpose

This document specifies the structure of merge-closeout reports
written under `docs/00-meta/implementation-reports/` after every
phase merge into `main`. A merge-closeout is the canonical record
that a phase is project-complete. Without it, the project record is
incomplete.

A well-formed merge-closeout records what changed, what explicitly did
not change, which SHAs anchor the merge, what local gitignored
artefacts (if any) accompany the merge but were not committed, what
validation produced, what governance is preserved, and what successor
is or is not authorized. A malformed merge-closeout invites scope
drift, silent assumptions, or unsafe successor authorization.

This document is **process-only**. It does not authorize any phase.

## When merge-closeout is required

A merge-closeout is required for every phase that is merged into
`main`. This includes:

- docs-only phases,
- code + docs phases,
- code + docs + local gitignored output phases,
- read-only QA phases,
- process / standardization phases,
- governance / consolidation memos,
- any other phase that touches `main`.

If a phase is branch-complete but not merged, no merge-closeout
exists. The phase is research-evidence on a branch, not project state.

## Short-form merge-closeout (Tier 4 only)

Per `docs/00-meta/process/phase-risk-tiering-standard.md`
(Phase 4bl-F), a **short-form** merge-closeout is permitted **only**
for Tier 4 (Administrative / Docs Correction) phases. A short-form
merge-closeout may compress sections that are trivially preserved
(for example, "no upstream artefacts touched", "no manifest
changes", "no successor authorized") into a single statement, but
must still record phase identity, SHAs, files brought forward,
diff summary, validation results, and explicit non-authorization.
Tier 1 (Full Phase), Tier 2 (Controlled Remediation), and Tier 3
(Batch) phases must use the full 16-section structure below.

## Required merge-closeout sections

Every merge-closeout must contain exactly these 16 sections in order:

1. **Phase identity** — phase identifier, phase name, phase type,
   merge purpose, source branch, target branch.
2. **SHAs** — pre-merge `main` SHA, branch commit SHAs (memo,
   closeout, any other tracked commits), merge commit SHA, final
   `main` / `origin/main` SHA after the merge-closeout commit.
3. **Merge method** — exact merge command, strategy, commit message,
   push status, force / skip-hook / skip-signing status (must be
   "none").
4. **Files brought forward by the merge** — exact list of files
   added or modified by the merge, grouped by category (docs, source,
   tests, scripts, config). State explicitly whether any
   `data/microstructure/` file was modified (it should not be).
5. **Diff summary** — `git diff --stat` output for the merge,
   inserted in a fenced code block.
6. **Result / verdict** — one-paragraph plain-English result of the
   phase. State the lifecycle conclusion (e.g. "STRUCTURAL QA PASS",
   "PROCESS STANDARDIZATION COMPLETE", "HARD REJECT recorded as
   research evidence", "remain paused").
7. **Local gitignored outputs (if any)** — for every local artefact
   produced by the phase: absolute path, size, SHA256, "not
   committed" status, `git check-ignore -v` confirmation. If the
   phase produced none, state "none" explicitly.
8. **Validation results** — exact validation tool outputs: ruff,
   mypy, pytest (scoped and / or whole-repo as applicable),
   `git diff --check`, `git check-ignore -v` for relevant paths.
9. **Upstream immutability evidence (if applicable)** — for every
   prior artefact that this phase must preserve bit-for-bit: pre-merge
   SHA256, post-merge SHA256, identical confirmation. If not
   applicable, state "n/a".
10. **Manifest state preservation (if applicable)** — for every
    manifest in scope: `research_eligible` state, `eligibility_gate_status`
    state, `chronological_split_policy` state, governance label state.
    Confirm that no transition occurred. If not applicable, state
    "n/a".
11. **Boundary confirmations** — enumerated list of every boundary
    that was honoured. Include: no source / test / script
    modification (unless explicitly in scope), no
    `data/microstructure/` commit, no manifest mutation, no
    `research_eligible` flip, no `eligibility_gate_status`
    transition, no `chronological_split_policy` change, no ML / strategy
    / backtest / acquisition / paper / shadow / live / deployment /
    exchange-write / production-key / authenticated-API /
    private-endpoint / user-stream / MCP / Graphify / .mcp.json /
    credentials work, no retained-verdict revision, no project-lock
    revision, no M0 amendment, no successor authorized.
12. **Retained verdict ledger** — full ledger of retained verdicts,
    each preserved verbatim. Include H0, R3, R1a, R1b-narrow, R2,
    F1, D1-A, 5m thread, V2, G1, C1.
13. **Preserved project locks** — full list of preserved locks: §11.6,
    round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8,
    Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
    Phase 4v, Phase 4w, Phase 4ak M0 twelve-clause gate + post-null
    cooldown + cooled-down families list + memo template, Phase 4al
    refined no-rescue rule + §13 boundary + §14 hierarchy, plus all
    prior phase results preserved verbatim.
14. **No-rescue constraints** — explicit list of activities this
    merge does NOT authorize and CANNOT be construed as authorizing.
    Include ML, strategy hypothesis generation, signal construction,
    paper / shadow / live-readiness / deployment / exchange-write,
    Phase 4 canonical, Phase 5, 30s / 5m / 30m / 1h / 4h /
    longer-horizon label generation, barrier / target-before-stop /
    MFE / MAE / R-multiple / PnL labels, mark-price / spot /
    cross-venue / order-book / additional aggTrades acquisition,
    old-strategy alt-symbol rerun, cooled-down-family reopening, 5m
    research-thread reopening, manifest transition from QA evidence
    alone.
15. **Successor authorization** — explicit statement of whether any
    successor is authorized. Default is **None**. List every
    candidate successor that is **not** authorized (named phases that
    a future operator might consider).
16. **Recommended state** — explicit recommendation: "Remain paused",
    "Author Phase {Y}", "Pause and reconsider", or another precise
    next action. The default is "Remain paused".

## SHA recording standard

- Record the pre-merge `main` SHA (the commit `main` pointed at
  before merging the branch).
- Record every commit SHA created on the branch (memo commit,
  closeout commit, any other tracked commits).
- Record the merge commit SHA (the commit created by `git merge --no-ff`).
- Record the final `main` / `origin/main` SHA after the
  merge-closeout commit is committed and pushed. This is the
  canonical "project is now at this SHA" marker.
- Use full 40-char SHAs for the merge commit and the final `main`
  SHA. Short SHAs (7-12 chars) are acceptable for branch commits if
  full SHAs appear elsewhere in the closeout.

## Merge method standard

- Always `git merge --no-ff` (no fast-forward).
- Always `ort` strategy (the default).
- Always a clear merge commit message of the form:
  `docs(phase-{X}): merge {short description}` or
  `feat(phase-{X}): merge {short description}` depending on phase
  content.
- Never `--no-verify`.
- Never `--no-gpg-sign`.
- Never `-c commit.gpgsign=false`.
- Never force-push.
- Record push status explicitly: "Pushed to `origin/main` with no
  force, no skip-hooks, no skip-signing."

## Files brought forward standard

- List every file added, modified, or deleted by the merge.
- Group by category: docs, source, tests, scripts, config.
- State explicitly whether any `data/microstructure/` file was
  modified (it should not be).
- State explicitly whether any prior governance memo was modified
  beyond the narrow `current-project-state.md` paragraph addition
  (it should not be unless the phase explicitly amends a governance
  file).
- State explicitly whether any prior source / test / script was
  modified (it should not be unless the phase explicitly extends a
  source / test surface).

## Diff summary standard

Include `git diff --stat` output for the merge in a fenced code
block. Example:

````text
```text
N files changed, M insertions(+), K deletions(-)
```
````

State explicitly whether the diff matches the expected change set
from the authorization prompt.

## Result / verdict standard

The result section is a one-paragraph plain-English summary of the
phase. State the lifecycle conclusion:

- **STRUCTURAL QA PASS** — for read-only QA phases that confirm
  artefacts conform to a contract.
- **PROCESS STANDARDIZATION COMPLETE** — for process / governance
  / standardization phases.
- **MEMO RECORDED** — for docs-only memos that record decisions or
  consolidations.
- **CODE LANDED** — for code + docs phases that ship runnable code
  without local artefact production.
- **LOCAL ARTEFACT PRODUCED** — for code + docs + local gitignored
  output phases.
- **HARD REJECT recorded as research evidence** — for phases that
  produce a research negative result.
- **GATE PASS** — for eligibility-gate phases that produce a passing
  gate report.
- **GATE FAIL** — for eligibility-gate phases that produce a failing
  gate report.

In all cases, conclude with the lifecycle state and the manifest /
artefact state that is preserved.

## Local gitignored output standard

For every local artefact produced by the phase:

- absolute path,
- size in bytes,
- SHA256 (full 64-char hex),
- `.sha256` sidecar SHA (if applicable),
- "not committed" status,
- `git check-ignore -v` confirmation of gitignore coverage,
- predecessor / source artefact references if this artefact derives
  from earlier work.

If the phase produced no local artefacts, state "none" explicitly.

## Validation results standard

Record exact tool outputs:

- `ruff check .` — `All checks passed` or scoped variant.
- `mypy` (whole repo, strict) — `Success on N source files`.
- `pytest tests/research/microstructure/` — `N passed`.
- `pytest` (whole repo) — `N passed, M failed` (and identify
  whether the failures are pre-existing).
- `git diff --check` — `clean` (no whitespace errors).
- `git check-ignore -v data/microstructure/` — `.gitignore:85`.
- `git check-ignore -v data/microstructure/labels/` — `.gitignore:85`.
- `git check-ignore -v data/microstructure/manifests/` —
  `.gitignore:85`.
- `git check-ignore -v data/microstructure/gate-reports/` —
  `.gitignore:85`.
- `git check-ignore -v data/microstructure/successor-state/` —
  `.gitignore:85`.

If whole-repo pytest reveals failures, classify them as pre-existing
or new. Pre-existing failures (e.g. the `KeyError: 'trade_count'`
simulation failures unchanged since prior phases) must be flagged as
"unchanged from prior phases; not introduced by this merge".

## Upstream immutability evidence standard

For every prior artefact that this phase must preserve bit-for-bit:

- name of the artefact,
- pre-merge SHA256,
- post-merge SHA256,
- IDENTICAL confirmation.

Examples of artefacts that must typically be preserved:

- raw manifest,
- raw zip,
- original derived manifest,
- normalized parquet,
- raw gate report,
- derived gate report,
- successor-state JSONs,
- feature parquet,
- feature manifest,
- label parquet,
- label manifest,
- all sidecars.

If the phase does not need to preserve any artefact bit-for-bit
(e.g. a pure docs-only phase that does not touch
`data/microstructure/`), state "n/a — phase did not access any local
artefact".

## Manifest state preservation standard

For every manifest in scope:

- `research_eligible` state — must be `false` for all current
  manifests unless an explicit Stage-2 / Stage-3 transition has
  occurred via a separately authorized successor-state phase.
- `eligibility_gate_status` state — must be `"pending"` for all
  current manifests unless an explicit transition has occurred.
- `chronological_split_policy` state — must be `"not_yet_defined"`
  for the label manifest unless an explicit policy decision has
  occurred.
- Governance label state — record any change. If unchanged, state
  "unchanged".

State explicitly: "Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant preserved (never invoked)" — for every phase that does not
intentionally invoke that helper.

## Boundary confirmation standard

The boundary confirmation list should enumerate every guarantee the
phase makes. Use bulleted "no X" / "preserved Y" form. Examples:

- no labels modified
- no label manifest modified
- no label parquet modified
- no label sidecars modified
- no `data/microstructure/` write outside the allowed surface
- no `data/microstructure/` artefact committed
- no label-family gate report created
- no label-family successor-state artefact created
- no replacement parquet / manifest / sidecar / gate report /
  successor-state created
- no `research_eligible` flipped on any actual manifest
- no `eligibility_gate_status` transitioned on any actual manifest
- no `chronological_split_policy` changed
- no ML model trained
- no strategy created
- no signal computed
- no backtest run
- no data acquired
- no public endpoint called
- no Binance API called
- no WebSocket opened
- no credential / `.env` / `.mcp.json` / MCP / Graphify used
- no normalizer rerun
- no raw eligibility gate rerun
- no derived-family gate rerun
- no feature kernel rerun
- no feature-family eligibility gate rerun
- no source code modified
- no test modified
- no script modified
- no `.gitignore`, `pyproject.toml`, or `README.md` modified
- no MCP file modified
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

Customize the list for the specific phase. Items that do not apply
should be omitted; items that apply must be stated explicitly.

## Retained verdict ledger standard

List every retained verdict, each preserved verbatim:

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

State explicitly: "All preserved verbatim."

## Preserved project locks standard

List every preserved lock:

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

State explicitly: "all prior phase results preserved verbatim."

## No-rescue constraints standard

State the no-rescue list explicitly. Example for a structural QA
phase:

The {Phase X} merge does not, and cannot, be construed as authorising:

- ML model training, model selection, strategy hypothesis generation,
  or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state, entry
  / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible` or
  `eligibility_gate_status` from this evidence alone.

Customize for the specific phase. Do not soften.

## Successor authorization standard

State explicitly:

**None.**

List every candidate successor that is **not** authorized. Example:

- Phase 4bj-E — Label-Family Eligibility Gate Design + Implementation
  + Execution
- Phase 4bj-F — Label-Family Research / ML-Use Decision
- Phase 4bj-G — Label-Family Successor-State Recording
- Phase 4bj (catch-all)
- Phase 4bb-F — Gate Report Output Path Hygiene
- Phase 4bb-G — Raw Manifest Successor-State Recording
- Phase 5
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book
  data acquisition
- ML implementation
- strategy implementation
- backtest implementation
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- user stream
- MCP / Graphify / `.mcp.json` / credentials

## Recommended state standard

The default recommendation is **Remain paused**. State this verbatim
as the conclusion of the merge-closeout.

If a conditional next phase is identified, state it as **NOT
authorised** and describe what it would do:

**Conditional next, NOT authorized:**

{Phase Y} is the cleanest non-paused option. It would {describe scope
in one paragraph}. Phase {Y} is **not** authorised by this merge.

## Common mistakes to avoid

- Omitting the final `main` / `origin/main` SHA after the
  merge-closeout commit.
- Stating "no successor authorized" but listing a successor as
  "recommended next phase" rather than "conditional next, NOT
  authorized".
- Softening no-rescue language.
- Omitting boundary confirmations.
- Treating a passing QA gate as authorization to flip a manifest
  flag.
- Treating a feature-family gate pass as authorization to acquire
  more data.
- Treating a label QA pass as authorization to design ML or strategy.
- Skipping the upstream immutability evidence section.
- Skipping the manifest state preservation section.
- Conflating branch SHAs with the merge commit SHA.
- Omitting `git check-ignore -v` confirmation for new local
  gitignored paths.
- Using vague "done" language instead of precise lifecycle vocabulary.

## Template

A skeleton merge-closeout in markdown:

````text
# Phase {X} — Merge Closeout

## 1. Phase identity
- **Phase:** {phase identifier} — {phase name}
- **Type:** {phase type}
- **Action:** merge into `main`
- **Merge purpose:** {one paragraph}
- **Target branch:** `main`
- **Source branch:** `{branch}`

## 2. SHAs
- **`main` SHA before merge:** `{short SHA}` ({predecessor name})
- **Branch commit SHAs:** `{memo SHA}`, `{closeout SHA}`, ...
- **Merge commit SHA:** `{full 40-char SHA}`
- **Final `main` / `origin/main` SHA after push:** {recorded after
  merge-closeout commit + push}

## 3. Merge method
- `git merge --no-ff` with `ort` strategy
- Merge commit message: `{message}`
- Pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing.

## 4. Files brought forward by the merge
{enumerated list grouped by category}

## 5. Diff summary
```text
{N files changed, M insertions(+), K deletions(-)}
```

## 6. Verdict
**{LIFECYCLE CONCLUSION}.**

{one-paragraph result}

## 7. Local gitignored outputs (if any)
{none / enumerated paths with size, SHA256, "not committed" status}

## 8. Validation results
{exact tool outputs}

## 9. Upstream immutability evidence (if applicable)
{table of pre/post SHA256 confirmations, or "n/a"}

## 10. Manifest state preservation (if applicable)
{enumerated manifest fields preserved, or "n/a"}

## 11. Boundary confirmations
{enumerated list}

## 12. Retained verdict ledger
{full ledger; preserved verbatim}

## 13. Preserved project locks
{full list; preserved verbatim}

## 14. No-rescue constraints
{enumerated list of what this merge does not authorize}

## 15. Successor authorization
**None.**

{enumerated list of every candidate successor not authorized}

## 16. Recommended state
**Remain paused.**

{conditional next phase, if any, marked NOT authorized}
````

This standard preserves all retained verdicts and project locks
verbatim. It does not authorize any successor phase. It does not
authorize Phase 4bj-E, label-family eligibility gate implementation,
ML, strategy, backtests, acquisition, paper / shadow / live,
deployment, exchange-write, production keys, authenticated APIs,
private endpoints, user stream, MCP, Graphify, `.mcp.json`, or
credentials.
