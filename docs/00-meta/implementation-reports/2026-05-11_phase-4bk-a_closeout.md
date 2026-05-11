# Phase 4bk-A — Closeout

## Phase name

Phase 4bk-A — Phase Workflow / Prompt / Report Standardization.

## Branch name

`phase-4bk-a/phase-workflow-prompt-report-standardization`.

## Base SHA

`main` at `244e619d2956b7715a861d691e8a78fc6b36f663` (Phase 4bj-D
merge-closeout state). Phase 4bj-D merge commit
`11e25acbf7d33b30f5149b93919594c3ccab9fe2` confirmed as ancestor of
`main`.

## Files changed

Tracked files added (7):

- `docs/00-meta/process/phase-workflow-standard.md`
- `docs/00-meta/process/phase-prompt-template.md`
- `docs/00-meta/process/operator-report-standard.md`
- `docs/00-meta/process/merge-closeout-standard.md`
- `docs/00-meta/process/chat-branching-handoff-standard.md`
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bk-a_phase-workflow-prompt-report-standardization.md`
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bk-a_closeout.md`

Tracked files modified narrowly (1):

- `docs/00-meta/current-project-state.md` (Phase 4bk-A narrative
  paragraph + new "Current phase" block; prior Phase 4bj-D "Current
  phase" block demoted to historical context).

No other tracked file modified.

No file under `data/microstructure/` modified, created, or committed.

No source / test / script / `pyproject.toml` / `README.md` /
`.gitignore` / MCP file modified.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git merge-base --is-ancestor 11e25acbf7d33b30f5149b93919594c3ccab9fe2 main
ls docs/00-meta/implementation-reports/2026-05-11_phase-4bj-d_merge-closeout.md
git check-ignore -v data/microstructure/
git check-ignore -v data/microstructure/labels/
git check-ignore -v data/microstructure/manifests/
git switch -c phase-4bk-a/phase-workflow-prompt-report-standardization
mkdir -p docs/00-meta/process
git diff --stat
git diff --name-only
ruff check .
mypy src
pytest tests/research/microstructure/
git diff --check
git status
git log --oneline -8
git add docs/00-meta/process/phase-workflow-standard.md
git add docs/00-meta/process/phase-prompt-template.md
git add docs/00-meta/process/operator-report-standard.md
git add docs/00-meta/process/merge-closeout-standard.md
git add docs/00-meta/process/chat-branching-handoff-standard.md
git add docs/00-meta/implementation-reports/2026-05-11_phase-4bk-a_phase-workflow-prompt-report-standardization.md
git add docs/00-meta/implementation-reports/2026-05-11_phase-4bk-a_closeout.md
git add docs/00-meta/current-project-state.md
git commit (HEREDOC commit message with Co-Authored-By trailer)
```

## Validation summary

- `ruff check .` (whole repo): **All checks passed**
- `mypy src` (strict): **Success on 115 source files** (unchanged
  from Phase 4bj-D baseline)
- `pytest tests/research/microstructure/`: **744 passed** (unchanged
  from Phase 4bj-D baseline)
- `git diff --check`: clean
- `git check-ignore -v data/microstructure/`: `.gitignore:85` confirms
  coverage
- `git check-ignore -v data/microstructure/labels/`: `.gitignore:85`
  confirms coverage
- `git check-ignore -v data/microstructure/manifests/`: `.gitignore:85`
  confirms coverage
- Whole-repo pytest: optional; if run, the two pre-existing
  `KeyError: 'trade_count'` simulation failures in
  `tests/simulation/test_backtest_real_2026_03.py` remain unchanged
  from prior phases and are not introduced by Phase 4bk-A.

## Process standards created

Five process documents now exist under `docs/00-meta/process/`:

1. **`phase-workflow-standard.md`** — master phase lifecycle manual.
   Codifies the eleven-step lifecycle, nine phase states, the binding
   rule "A phase is not project-complete until it is merged into main
   and its merge-closeout is recorded", the merge-closeout mandate,
   the successor-authorization rule (default: none), the local
   gitignored artefact rule, the manifest mutation rule, the repo-query
   requirement for new chats, and the operator / ChatGPT / Claude Code
   role split.
2. **`phase-prompt-template.md`** — required structure of
   authorization prompts and merge prompts. Codifies 21 required
   prompt sections, templates for docs-only / code + docs / code +
   docs + local gitignored output / read-only QA / merge phase types,
   the 10-item final Claude response format, and libraries for
   fail-closed conditions, validation commands, commit instructions,
   non-scope wording, local artefact wording, and successor
   authorization wording.
3. **`operator-report-standard.md`** — required shape of Claude Code
   compact reports and ChatGPT operator-facing responses. Codifies
   the three-way role split, the Claude Code 10-item compact report
   format, the ChatGPT four-question response rule, five ChatGPT
   response templates (phase review; post-merge confirmation;
   prompt-generation; concept-explanation; ambiguity / correction),
   plain-English explanation rules, blocker vs non-blocker
   classification, "still blocked / not authorized" language
   standard, next-action recommendation standard, evidence /
   citation standard, tone / style standard, and anti-patterns to
   avoid.
4. **`merge-closeout-standard.md`** — required shape of
   merge-closeout reports. Codifies the 16 required sections, SHA
   recording standard, merge method standard, files-brought-forward
   standard, diff summary standard, result / verdict standard (with
   eight lifecycle conclusion labels), local gitignored output
   standard, validation results standard, upstream immutability
   evidence standard, manifest state preservation standard, boundary
   confirmation standard, retained verdict ledger and preserved
   project locks standards, no-rescue constraints standard, successor
   authorization standard (default: None), recommended state
   standard (default: Remain paused), and a skeleton template.
5. **`chat-branching-handoff-standard.md`** — required shape of the
   handoff that anchors a new chat to current repo state. Codifies
   when to branch chat, 15 required handoff sections, 11 required
   continuation prompt sections, the repo-query requirement for new
   chats, six verification checklists (current-state, latest-phase,
   merge-state, local-data, artefact SHA, retained verdict /
   project-lock), the "do not rely on handoff alone" rule, and a
   skeleton template.

## Boundary confirmations

- no source / test / script modified
- no `.gitignore`, `pyproject.toml`, `README.md` modified
- no MCP file modified
- no `data/microstructure/` artefact modified, created, or committed
- no label artefact modified
- no label manifest modified
- no label parquet modified
- no label sidecars modified
- no feature artefact modified
- no feature manifest modified
- no feature parquet modified
- no feature sidecars modified
- no derived manifest modified
- no normalized parquet modified
- no raw manifest modified
- no raw zip modified
- no any prior gate report modified
- no any prior successor-state JSON modified
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
- no label kernel rerun
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized
- not merged into `main`

## Retained verdict ledger

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

## Preserved project locks

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
- all prior phase results (Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A
  / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A
  / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C
  / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D) preserved verbatim

## Successor authorization status

**None.**

Phase 4bk-A does not authorize any successor phase. Specifically not
authorized by this phase:

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

## Recommended state

**Remain paused.**

Phase 4bk-A improves process consistency only. The technical state of
the label family is unchanged: Stage-0, `research_eligible = false`,
`eligibility_gate_status = "pending"`,
`chronological_split_policy = "not_yet_defined"`. No forward motion
is implied.

This phase is branch-complete after the commit. The phase becomes
project-complete only after a separately issued merge prompt is
followed by `git merge --no-ff` into `main`, a merge-closeout per
`docs/00-meta/process/merge-closeout-standard.md` is committed on
`main`, and the final `main` / `origin/main` SHA is recorded in that
merge-closeout.
