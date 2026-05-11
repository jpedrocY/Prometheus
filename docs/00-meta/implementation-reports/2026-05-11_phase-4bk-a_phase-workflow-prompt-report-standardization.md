# Phase 4bk-A — Phase Workflow / Prompt / Report Standardization

## Phase header

- **Phase:** Phase 4bk-A — Phase Workflow / Prompt / Report
  Standardization
- **Type:** docs-only / process standardization
- **Branch:** `phase-4bk-a/phase-workflow-prompt-report-standardization`
- **Base:** `main` at the post-Phase-4bj-D merge-closeout state
- **Predecessor merge:** Phase 4bj-D merge commit
  `11e25acbf7d33b30f5149b93919594c3ccab9fe2` (confirmed ancestor of
  `main`)

## Why this phase exists

The project has accumulated a deep, well-disciplined phase ledger
across the V2 microstructure → aggTrades acquisition → eligibility
gate → normalization → derived gate → derived successor-state → feature
kernel → feature QA → feature gate → feature research-use → feature
successor-state → label boundary → label schema → label
implementation → label structural QA arc. Across that arc, a stable
pattern has emerged: docs-only recommendation / debate → authorization
prompt → branch execution → implementation report + closeout → operator
review in ChatGPT → merge prompt → merge into `main` → merge-closeout
report on `main` → operator post-merge explanation → recommended next
phase or pause → chat branching handoff when context requires.

The pattern works. But the pattern lives in chat memory, not in the
repository. A new chat may absorb the project's technical content
quickly and still miss critical lifecycle nuance: that branch-complete
work is not project-complete until merge-closeout is recorded; that a
QA pass is not authorization to flip a manifest flag; that a feature-
family gate pass is not authorization to acquire more data; that
ChatGPT's role is interpreter, not executor; that Claude Code's role is
executor, not interpreter; that no successor phase is ever automatic.

Phase 4bk-A makes the lifecycle authoritative inside the repository.

## Problem observed

A new chat may understand project content but miss that branch-complete
work requires review, merge prompt, merge, and merge-closeout before
the next phase can even be recommended. A new chat that recommends a
successor phase based on chat-memory summaries alone, without anchoring
to current `main` SHA and the latest merge-closeout, is unsafe.

The specific failure modes Phase 4bk-A addresses:

- treating branch-complete as merged,
- recommending a successor before the predecessor's merge-closeout
  exists,
- skipping the merge-closeout and moving to the next authorization
  prompt,
- treating a passing QA gate as authorization to flip
  `research_eligible`,
- treating a label QA pass as authorization to design ML or strategy,
- treating a feature-family gate pass as authorization to acquire more
  data,
- authorizing the next phase from a chat handoff alone, without
  confirming `main` SHA and the latest merge-closeout,
- ChatGPT over-claiming readiness or profitability in plain-English
  summaries,
- Claude Code editorializing about strategy / edge / readiness in
  compact reports.

## Current project state

At the start of Phase 4bk-A:

- `main` SHA: `244e619d2956b7715a861d691e8a78fc6b36f663`
- `origin/main` SHA: `244e619d2956b7715a861d691e8a78fc6b36f663` (in
  sync)
- Last completed phase: Phase 4bj-D — Label Artefact Structural QA
  Memo, merge-closeout recorded at
  `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-d_merge-closeout.md`.
- Label family: Stage-0, `research_eligible = false`,
  `eligibility_gate_status = "pending"`,
  `chronological_split_policy = "not_yet_defined"`.
- Phase 4bj-E (label-family eligibility gate) is the cleanest
  non-paused conditional next phase, NOT authorized.
- `data/microstructure/` is gitignored under `.gitignore:85`.

## Inputs reviewed

Phase 4bk-A inspected (read-only) prior process / report style:

- `docs/00-meta/current-project-state.md` (to match the verbose
  narrative style of the "Current phase" block);
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-d_merge-closeout.md`
  (most recent merge-closeout, used as the canonical
  merge-closeout style reference);
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-c_merge-closeout.md`
  (prior merge-closeout for style continuity);
- recent phase implementation reports (Phase 4bj-D, Phase 4bj-C,
  Phase 4bj-B) for tone consistency.

No file under `docs/00-meta/process/` existed prior to Phase 4bk-A.

## Scope

Phase 4bk-A is docs-only / process standardization. The scope is:

- create five process documents under `docs/00-meta/process/` that
  codify the phase lifecycle, prompt design, operator / Claude Code
  reporting standard, merge-closeout standard, and chat-branching
  handoff standard;
- create a phase implementation report and a phase closeout under
  `docs/00-meta/implementation-reports/`;
- update `docs/00-meta/current-project-state.md` narrowly to add a
  Phase 4bk-A narrative paragraph and a new "Current phase" block,
  preserving the prior Phase 4bj-D block as historical context.

Nothing else.

## Non-scope

Phase 4bk-A does NOT:

- modify any source, test, script, `.gitignore`, `pyproject.toml`,
  `README.md`, or MCP file;
- modify or commit anything under `data/microstructure/`;
- modify any label artefact, label manifest, label parquet, or
  label sidecar;
- create any label-family gate report or label successor-state
  artefact;
- change `research_eligible`, `eligibility_gate_status`, or
  `chronological_split_policy` on any manifest;
- acquire data, train ML, run strategy, run backtests, call APIs,
  open WebSockets, use credentials, create `.env` or `.mcp.json`,
  enable MCP or Graphify;
- revise any retained verdict or project lock;
- amend M0 governance;
- authorize Phase 4bj-E or any other successor phase;
- merge into `main`.

## Process files created

Phase 4bk-A created five process documents under
`docs/00-meta/process/`:

1. `phase-workflow-standard.md` — master phase lifecycle manual.
2. `phase-prompt-template.md` — required structure of authorization
   prompts and merge prompts.
3. `operator-report-standard.md` — required shape of Claude Code
   compact reports and ChatGPT operator-facing responses.
4. `merge-closeout-standard.md` — required shape of merge-closeout
   reports.
5. `chat-branching-handoff-standard.md` — required shape of the
   handoff that anchors a new chat to current repo state.

## Phase workflow standard summary

`docs/00-meta/process/phase-workflow-standard.md` codifies:

- the eleven-step phase lifecycle (recommendation → authorization
  prompt → branch execution → implementation report + closeout →
  operator review → merge prompt → merge → merge-closeout → operator
  post-merge explanation → next-phase recommendation or pause → chat
  branching handoff);
- the nine phase states (Proposed, Authorized, Branch-complete,
  Reviewed, Merge-ready, Merged, Merge-closeout recorded, Paused,
  Fail-closed / stopped);
- the binding rule: **A phase is not project-complete until it is
  merged into main and its merge-closeout is recorded.**;
- the mandatory merge-closeout requirement after every merge;
- the successor-authorization rule (default: no successor authorized);
- the local gitignored artefact rule (record paths / SHA256 / "not
  committed" status; preserve bit-for-bit; never commit
  `data/microstructure/` outputs);
- the manifest mutation rule (no transitions without explicit
  authorization; Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved);
- the repo-query requirement for new chats;
- the operator / ChatGPT / Claude Code role split;
- examples of correct lifecycle sequencing;
- examples of forbidden lifecycle collapse;
- preserved project governance (full retained verdict ledger, full
  project locks);
- a change-control process for the standard itself.

## Phase prompt template summary

`docs/00-meta/process/phase-prompt-template.md` codifies:

- prompt design principles (one phase per prompt; exact allowed files;
  exact forbidden activities; distinguish tracked from local
  gitignored; forbid successor authorization; include validation
  commands; include fail-closed conditions; require compact final
  response);
- 21 required prompt sections (repository, local path, phase identity,
  phase type, branch name, known state, predecessor dependency,
  purpose, critical boundary, strict non-scope, allowed tracked files,
  allowed local gitignored outputs, required outputs, required
  evidence, initial verification, validation commands, expected
  validation behavior, commit instructions, do-not-merge / merge
  instructions, fail-closed conditions, final Claude response format);
- prompt templates for docs-only, code + docs, code + docs + local
  gitignored output, read-only QA, and merge phase types;
- the 10-item final Claude response format (Status, Branch, Commit
  SHAs, Merge SHA if applicable, Files changed, Validation summary,
  Final git status, Final git log --oneline -8, Local/origin sync,
  Notes / blockers);
- libraries for fail-closed conditions, validation commands, commit
  instructions, non-scope wording, local artefact wording, and
  successor authorization wording;
- skeleton examples for authorization prompts and merge prompts.

## Operator report standard summary

`docs/00-meta/process/operator-report-standard.md` codifies:

- the three-way role split (Claude Code = executor and recorder;
  ChatGPT = interpreter, reviewer, teacher, phase navigator,
  operator-facing explainer; repo docs = authority that keeps both
  consistent);
- the Claude Code 10-item compact report format;
- the ChatGPT four-question response rule (what happened, what does
  it mean in simple terms, what is still blocked / not authorized,
  what should happen next);
- five ChatGPT response templates:
  - **phase review** (`## Phase X review`, `## What happened`,
    `## What this means in simple terms`, `## Evidence that matters`,
    `## What is still not allowed`, `## Issues or corrections`,
    `## Next lifecycle action`),
  - **post-merge confirmation** (`## Current result`, `## What
    changed`, `## What this means`, `## Still blocked`, `## Next
    correct phase`),
  - **prompt-generation** (`## Recommended prompt for Phase X`,
    `## Prompt`, `## Why this scope`, `## What this prompt does NOT
    authorize`, `## How to issue this prompt`),
  - **concept-explanation** (`## Plain English`, `## Project-specific
    meaning`, `## What it is not`, `## Why it matters next`),
  - **ambiguity / correction** (`## Concern`, `## Why it matters`,
    `## Options`, `## Recommended option`, `## What this means for
    the current phase`);
- plain-English explanation rules (avoid jargon, use project-specific
  language consistently, distinguish facts from interpretation,
  translate not embellish, be explicit about lifecycle state and
  non-authorizations);
- blocker vs non-blocker classification;
- "still blocked / not authorized" language standard (with verbatim
  phrases for ML, strategy, backtests, acquisition, paper / shadow /
  live, deployment, exchange-write, production keys, MCP, Graphify,
  manifest transition, successor phases);
- next-action recommendation standard (remain paused; author Phase
  Y; pause and reconsider; stop and correct; branch chat);
- evidence and citation standard;
- tone and style standard;
- anti-patterns to avoid.

## Merge-closeout standard summary

`docs/00-meta/process/merge-closeout-standard.md` codifies:

- when merge-closeout is required (every phase merged into `main`);
- the 16 required sections (phase identity, SHAs, merge method, files
  brought forward, diff summary, result / verdict, local gitignored
  outputs, validation results, upstream immutability evidence,
  manifest state preservation, boundary confirmations, retained
  verdict ledger, preserved project locks, no-rescue constraints,
  successor authorization, recommended state);
- the SHA recording standard (pre-merge `main` SHA, branch commit
  SHAs, merge commit SHA, final `main` / `origin/main` SHA after
  merge-closeout commit + push; full 40-char SHAs for merge commit
  and final `main` SHA);
- the merge method standard (`git merge --no-ff` with `ort` strategy;
  no `--no-verify`; no `--no-gpg-sign`; no force-push; explicit push
  status);
- the files-brought-forward standard (grouped by category; explicit
  statement about `data/microstructure/` files);
- the diff summary standard;
- the result / verdict standard (with eight standard lifecycle
  conclusion labels: STRUCTURAL QA PASS, PROCESS STANDARDIZATION
  COMPLETE, MEMO RECORDED, CODE LANDED, LOCAL ARTEFACT PRODUCED,
  HARD REJECT recorded as research evidence, GATE PASS, GATE FAIL);
- the local gitignored output standard (paths, sizes, SHA256s,
  "not committed" status, gitignore confirmation);
- the validation results standard (exact tool outputs);
- the upstream immutability evidence standard (pre/post SHA256
  IDENTICAL confirmation);
- the manifest state preservation standard;
- the boundary confirmation standard;
- the retained verdict ledger and preserved project locks standards;
- the no-rescue constraints standard;
- the successor authorization standard (default: None);
- the recommended state standard (default: Remain paused);
- a skeleton template.

## Chat branching handoff standard summary

`docs/00-meta/process/chat-branching-handoff-standard.md` codifies:

- when to branch chat (context accumulation; post-merge-closeout
  fresh chat; arc focus change; operator preference);
- 15 required handoff sections (project identity, repository and
  local path, current `main` / `origin/main` SHA, last completed
  phase, last merge-closeout path, current local data assumptions,
  current artefacts and SHAs, current arc summary, phases completed
  in current arc, retained verdicts, project locks, current
  non-authorizations, known validation caveats, recommended next
  phase or paused state, ready-to-paste continuation prompt);
- the 11 required continuation prompt sections;
- the repo-query requirement for new chats (read
  `current-project-state.md`, read latest merge-closeout, read
  latest implementation report, confirm `main == origin/main`,
  confirm lifecycle state, confirm local data assumptions, confirm
  retained verdicts and project locks);
- four verification checklists (current-state, latest-phase,
  merge-state, local-data, artefact SHA, retained verdict /
  project-lock);
- the "do not rely on handoff alone" rule;
- a skeleton template.

## Required lifecycle behavior

Going forward, every phase must obey:

1. branch-complete is not project-complete;
2. merge-closeout is mandatory after every merge;
3. no successor is authorized unless operator explicitly authorizes;
4. local gitignored outputs are recorded but never committed;
5. `data/microstructure/` outputs must not be committed;
6. manifests do not transition without explicit authorization;
7. the Phase 4aw
   `MicrostructureManifest.flip_research_eligible(...)` always-raises
   invariant is preserved;
8. `current-project-state.md` is high-level state, not a replacement
   for phase reports or merge-closeouts.

## Required ChatGPT response behavior

ChatGPT responses about phases must answer four questions:

1. What happened?
2. What does it mean in simple terms?
3. What is still blocked / not authorized?
4. What should happen next?

ChatGPT must use the response templates in
`operator-report-standard.md` and the verbatim "still blocked / not
authorized" phrases. ChatGPT must distinguish lifecycle state from
project state. ChatGPT must cite documents and SHAs where available.

## Required Claude Code response behavior

Claude Code must end every phase response with the 10-item compact
final response format. Claude Code must not editorialize about
strategy, edge, profitability, or readiness. Claude Code must
distinguish `COMPLETED`, `FAIL_CLOSED`, and `STOPPED` precisely.

## Required merge behavior

Every merge must follow `phase-prompt-template.md` merge prompt
template and produce a merge-closeout report matching
`merge-closeout-standard.md`. The final `main` / `origin/main` SHA
must be recorded in the merge-closeout after the merge-closeout
commit is pushed.

## Required handoff behavior

Every chat-branching handoff must follow
`chat-branching-handoff-standard.md` and include the ready-to-paste
continuation prompt with the repo-query requirement.

## What this phase proves

Phase 4bk-A proves that the project's lifecycle, prompt design,
report shape, merge-closeout structure, and chat handoff content are
now authoritative inside the repository. Future chats anchored to
these documents will produce safer, more consistent, more
operator-readable outputs.

## What this phase does NOT prove

Phase 4bk-A does NOT prove:

- that the label family is research-eligible;
- that any manifest transition is authorized;
- that ML / strategy / backtests / acquisition / paper / shadow /
  live / deployment / exchange-write are authorized;
- that Phase 4bj-E is authorized;
- that any project lock has been loosened;
- that any retained verdict has been revised;
- that profitability, edge, or readiness has been demonstrated.

Phase 4bk-A improves process consistency only. The technical state of
the label family is unchanged.

## Preserved boundaries

This phase preserves:

- the full retained verdict ledger (H0, R3, R1a, R1b-narrow, R2, F1,
  D1-A, 5m thread, V2, G1, C1),
- all project locks (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase
  3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k,
  Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0, Phase 4al
  refined no-rescue rule),
- the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant,
- the Phase 3t 5m research-thread closure,
- the Phase 3v §8 stop-trigger-domain governance,
- the Phase 4j §11 metrics OI-subset partial-eligibility rule
  (preserved; unused),
- every prior phase's results verbatim.

## Recommended future options

**Remain paused (default).**

The Phase 4bk-A merge — when issued separately — will record process
standardization. The label family will remain Stage-0. No technical
state will move.

**Conditional next, NOT authorized by Phase 4bk-A:**

- Phase 4bj-E — Label-Family Eligibility Gate Design + Implementation
  + Execution. This remains the cleanest non-paused option for the
  current arc. It is **not** authorized by Phase 4bk-A.
- Phase 4bk-B — any further process refinement (not currently scoped).
- Phase 4bj-F — Label-Family Research / ML-Use Decision (not
  authorized; would require Phase 4bj-E to have produced a passing
  gate report first).

## Closeout / lock preservation

This phase does not modify any source, test, script, config, data,
manifest, sidecar, or gate report. This phase does not authorize any
successor. This phase does not enable any forbidden activity. This
phase does not loosen any project lock. This phase does not amend
M0. This phase does not revise any retained verdict.

**Recommended state: Remain paused.**
