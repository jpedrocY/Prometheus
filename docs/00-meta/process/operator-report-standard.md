# Operator Report Standard

## Title

Prometheus Operator Report Standard — required shape of Claude Code
compact reports and ChatGPT operator-facing responses.

## Purpose

This document specifies the shape of reports and responses in the
Prometheus phase lifecycle. It exists to make outputs precise,
consistent, and operator-readable across chats, across implementation
agents, and across phases. A well-formed report distinguishes facts
from interpretation, lifecycle state from project state, and
blockers from notes. A malformed report invites scope drift, silent
assumptions, or over-claimed readiness.

This document is **process-only**. It does not authorize any phase.

## Role split

Three distinct roles produce different kinds of output:

- **Claude Code** is the executor and recorder inside the repo. Its
  responses are compact, evidence-anchored, and use the 10-item final
  response format. Claude Code records what happened, what changed,
  what validation produced, and any blockers. Claude Code does not
  interpret in plain English. Claude Code does not authorize phases.
- **ChatGPT** is the interpreter, reviewer, teacher, phase
  navigator, and operator-facing explainer. Its responses are
  plain-English summaries that translate Claude Code's compact
  evidence into operator-readable explanations. ChatGPT identifies
  blockers, confirms scope honoured, recommends merge or pause,
  recommends next phase or remain-paused, and prepares chat handoffs.
  ChatGPT does **not** modify the repo. ChatGPT does not authorize
  phases on its own.
- **Repo docs** are the authority that keeps both consistent across
  chats. Implementation reports, closeouts, merge-closeouts, and
  `current-project-state.md` are the canonical record. Chat outputs
  are derived from repo docs, never the other way around.

These roles are deliberately separated. ChatGPT sees plain English and
intent. Claude Code sees scope and execution. Operator sees both and
decides.

## Claude Code compact report standard

Every Claude Code response that closes a phase action must end with
exactly this 10-item format:

```text
1. Status: COMPLETED / FAIL_CLOSED / STOPPED
2. Branch:
3. Commit SHA(s):
4. Merge SHA, if applicable:
5. Files changed:
6. Validation summary:
7. Final git status:
8. Final git log --oneline -8:
9. Local/origin sync:
10. Notes / blockers:
```

Required fields:

- **Status** — one of `COMPLETED`, `FAIL_CLOSED`, `STOPPED`. Use
  `COMPLETED` only when every step of the authorized prompt was
  executed successfully. Use `FAIL_CLOSED` when a precondition,
  validation, or scope check failed. Use `STOPPED` when the operator
  asked Claude Code to stop mid-phase.
- **Branch** — the exact branch name. If on `main`, say `main`.
- **Commit SHA(s)** — short SHAs of every commit created in this
  phase action, in order.
- **Merge SHA, if applicable** — merge commit SHA if this is a merge
  phase. Otherwise `n/a`.
- **Files changed** — exact list of files touched (created,
  modified, deleted) in this phase action.
- **Validation summary** — one line per validation gate: ruff status,
  mypy status, pytest status, gitignore confirmation, diff --check
  status. Use exact tool output where short.
- **Final git status** — output of `git status` after the last
  commit.
- **Final git log --oneline -8** — output of `git log --oneline -8`
  after the last commit.
- **Local/origin sync** — whether the local branch is in sync with
  `origin`. State explicitly whether the branch was pushed.
- **Notes / blockers** — any blocker, ambiguity, scope question, or
  follow-up that the operator should know.

Claude Code reports must not:

- editorialize about strategy, edge, profitability, or readiness;
- claim a phase is project-complete when only branch-complete;
- imply a successor is authorized;
- skip blockers because they are minor;
- bury blockers among non-blocking notes;
- speak in plain English where compact evidence is required.

## ChatGPT operator-facing response standard

ChatGPT responses translate Claude Code's compact evidence into
operator-readable plain English. Every phase-related ChatGPT response
must answer four questions:

1. **What happened?** — what Claude Code did, in plain English,
   anchored to the compact report's evidence.
2. **What does it mean in simple terms?** — translation into project
   context: which arc, which boundary, which artefact, which
   manifest.
3. **What is still blocked / not authorized?** — enumeration of
   activities that this phase did not authorize, with explicit
   language.
4. **What should happen next?** — either a recommended next phase
   with precise scope, or remain-paused.

ChatGPT responses must cite documents and SHAs where available. ChatGPT
responses must distinguish lifecycle state (branch-complete vs
merge-closeout recorded) from project state (what is on `main`).

## Phase review response template

When operator brings a branch-complete phase to ChatGPT for review:

```text
## Phase {X} review

{One-paragraph summary anchored to Claude Code's compact report.
Include phase identifier, phase type, branch name, branch commit SHAs,
and lifecycle state (branch-complete).}

## What happened

{Plain-English account of what Claude Code did. Describe the tracked
files produced, the local gitignored artefacts produced (if any), the
validation gates that passed, and the boundaries that were honoured.}

## What this means in simple terms

{Translation into project context. Which arc does this belong to?
Which boundary did the phase cross? Which manifest state is preserved?
What evidence is now in the repo?}

## Evidence that matters

{Enumerate the most important evidence: implementation report path,
closeout path, key SHA256s, validation results.}

## What is still not allowed

{Enumerate forbidden activities verbatim. Use "still" / "remains" /
"not authorized" language. Include common items: ML, strategy,
backtests, acquisition, paper / shadow / live, MCP, Graphify,
credentials, manifest transition, successor phases.}

## Issues or corrections

{Identify blockers, scope concerns, or corrections needed before
merge. If none, say "none identified."}

## Next lifecycle action

{One of: "Proceed to merge prompt", "Pause and remain paused",
"Author a corrective phase before merge", "Stop and reconsider".}
```

## Post-merge confirmation template

When Claude Code reports a successful merge-closeout, ChatGPT confirms
to the operator:

```text
## Current result

{One-paragraph summary anchored to the merge-closeout. Include the
final `main` / `origin/main` SHA, the merge commit SHA, and the
project-complete lifecycle state.}

## What changed

{Enumerate the files brought forward by the merge. Distinguish docs
from source / tests / scripts. State explicitly whether any
`data/microstructure/` file was modified (it should not be).}

## What this means

{Translation into project context. What is now on `main` that was not
before? Which arc moved forward, if any? Which manifest state is
preserved? Which retained verdict / project lock / governance contract
remains binding?}

## Still blocked

{Enumerate forbidden activities verbatim. Use "still" / "remains" /
"not authorized" language. Reference the merge-closeout's successor
authorization section.}

## Next correct phase

{One of: "Remain paused", "Author Phase {Y}", "Pause and reconsider
arc direction". If recommending a next phase, give precise scope.}
```

## Prompt-generation response template

When operator asks ChatGPT to draft an authorization prompt or merge
prompt for Claude Code:

```text
## Recommended prompt for Phase {X}

{One-paragraph rationale anchored to current `main` state and
predecessor merge-closeout. Cite SHAs.}

## Prompt

{Full prompt body in a fenced code block, following
`phase-prompt-template.md`. Include all required sections.}

## Why this scope

{Plain-English explanation of why the scope is what it is. Explain
what is included, what is excluded, and why.}

## What this prompt does NOT authorize

{Enumerate forbidden activities verbatim. Include successor phases.}

## How to issue this prompt

{Instructions to the operator on copying the prompt to Claude Code
and what to expect in the compact report.}
```

## Concept-explanation response template

When operator asks ChatGPT to explain a concept (a manifest, a gate,
a label, a verdict, a project lock, a forbidden activity):

```text
## Plain English

{Two- to four-sentence plain-English explanation of the concept.
Avoid jargon.}

## Project-specific meaning

{What the concept means in the Prometheus repository. Reference
specific files, manifests, or governance contracts. Cite SHAs where
relevant.}

## What it is not

{Common misunderstandings. Examples: "labels are not signals", "QA
pass is not authorization", "research-eligible flag does not mean ML
is authorized".}

## Why it matters next

{Connect the concept to the current lifecycle state. Why does the
operator need to understand this now?}
```

## Ambiguity / correction response template

When ChatGPT identifies a scope concern, ambiguity, or correction
needed:

```text
## Concern

{One-paragraph description of the concern. Be precise. Cite the
specific report, file, or SHA where the concern was observed.}

## Why it matters

{Connect to the project's safety / governance rules. Reference
specific project locks, M0 clauses, or no-rescue constraints.}

## Options

{Enumerate concrete options. For each option, state what would have
to be done.}

## Recommended option

{Recommend exactly one option. Explain why.}

## What this means for the current phase

{Lifecycle implication: pause, draft a corrective phase, fail closed,
proceed with adjustment, etc.}
```

## Chat handoff response expectations

When operator branches to a new chat, ChatGPT prepares the handoff per
`chat-branching-handoff-standard.md`. The handoff response must
include:

- the current `main` / `origin/main` SHA,
- the last completed phase,
- the last merge-closeout path,
- the current local data assumptions,
- the current artefacts and SHA256s,
- the retained verdict ledger,
- the project locks,
- the current non-authorizations,
- the recommended next phase or paused state,
- a ready-to-paste continuation prompt for the new chat,
- explicit instructions for the new chat to query the repo before
  recommending or executing anything.

## Plain-English explanation rules

When ChatGPT translates Claude Code's compact evidence into plain
English:

- **Avoid jargon where plain words suffice.** Say "a passing test
  suite" instead of "scoped pytest PASS".
- **Use project-specific language consistently.** "Label artefact",
  "feature parquet", "raw manifest", "successor-state JSON",
  "research_eligible flag" — use the exact terms.
- **Distinguish facts from interpretation.** Anchor facts to SHAs and
  file paths. Mark interpretation as such.
- **Translate, do not embellish.** Do not over-claim profitability,
  edge, readiness, or value.
- **Be explicit about lifecycle state.** Say "branch-complete" or
  "merge-closeout recorded", not "done".
- **Be explicit about non-authorizations.** Use the verbatim list
  from the merge-closeout.

## Blocker vs non-blocker classification

A **blocker** is anything that prevents the current lifecycle step
from completing safely. Examples:

- failed precondition verification,
- scope violation,
- failed validation gate,
- missing required artefact,
- gitignore coverage missing where required,
- ambiguity that cannot be resolved without operator decision,
- a forbidden activity that the prompt would require.

A **non-blocker** is anything that does not prevent the current
lifecycle step but should be tracked. Examples:

- a minor documentation typo that does not affect content,
- a future enhancement that is out of scope but worth noting,
- a deferred follow-up that the operator should decide on later.

ChatGPT must classify clearly. Blockers must be surfaced explicitly.
Non-blockers must be labelled as such.

## "Still blocked / not authorized" language standard

Standard phrases for forbidden activities:

- "ML training remains unauthorized."
- "Strategy implementation remains unauthorized."
- "Backtest execution remains unauthorized."
- "Data acquisition (additional aggTrades / 5m / 1m / tick /
  mark-price / order-book) remains unauthorized."
- "Paper / shadow remains unauthorized."
- "Live-readiness remains unauthorized."
- "Deployment remains unauthorized."
- "Exchange-write remains unauthorized."
- "Production keys remain unauthorized."
- "Authenticated APIs remain unauthorized."
- "Private endpoints remain unauthorized."
- "User stream remains unauthorized."
- "MCP / Graphify / .mcp.json / credentials remain unauthorized."
- "Manifest transition (`research_eligible`,
  `eligibility_gate_status`, `chronological_split_policy`) remains
  unauthorized."
- "Phase {Y} remains unauthorized."
- "No successor is authorized by this merge."

Use these verbatim. Do not soften.

## Next-action recommendation standard

Every phase-related ChatGPT response ends with an explicit
next-action recommendation:

- **Remain paused.** The default. Recommended after every
  merge-closeout. Recommended when the next sensible step is
  operator-driven.
- **Author Phase {Y}.** Specify scope, predecessor, allowed surface,
  and reason. Include the precise rationale.
- **Pause and reconsider.** Use when the current arc has reached an
  evidence boundary and the next step requires governance design
  rather than execution.
- **Stop and correct.** Use when a blocker requires a corrective
  phase before continuing.
- **Branch chat.** Use when context has accumulated and the next
  phase deserves a fresh chat with a clean handoff.

## Evidence and citation standard

When ChatGPT cites evidence:

- **Cite repo file paths in backticks.** Example:
  ``docs/00-meta/implementation-reports/2026-05-11_phase-4bj-d_merge-closeout.md``
- **Cite SHAs as short SHAs (first 7-12 chars) where space matters.**
  Cite full SHAs when discussing artefacts.
- **Cite line ranges with `:N` or `:N-M` syntax** when discussing a
  specific section of a file.
- **Distinguish artefact SHA256s from git commit SHAs.** Artefact
  SHA256s are 64-char hex; git commit SHAs are 40-char hex.
- **Anchor every claim to evidence.** If you cannot cite, do not
  claim.

## Tone and style standard

- **Be plain.** Use clear, direct language.
- **Be specific.** Use exact file paths, exact SHAs, exact tool
  output.
- **Be honest about uncertainty.** Say "I cannot confirm without
  reading the repo" when applicable.
- **Be respectful of operator authority.** ChatGPT recommends;
  operator decides.
- **Be respectful of Claude Code's execution role.** ChatGPT
  interprets; Claude Code executes.

## Anti-patterns to avoid

ChatGPT and Claude Code must avoid:

- saying "done" without specifying lifecycle state,
- treating branch-complete as merged,
- implying a successor is authorized,
- turning labels into signals or treating descriptive evidence as
  strategy evidence,
- turning a QA pass into authorization for ML / strategy / backtests,
- turning a feature-family gate pass into authorization to acquire
  more data,
- over-claiming edge / profitability / readiness,
- skipping citations when documents are available,
- hiding blockers among non-blocking notes,
- softening forbidden-activity language,
- using vague verbs ("done", "finished", "ready") where precise
  lifecycle language is required,
- mixing fact and interpretation without distinction.

This standard preserves all retained verdicts and project locks
verbatim. It does not authorize any successor phase. It does not
authorize Phase 4bj-E, label-family eligibility gate implementation,
ML, strategy, backtests, acquisition, paper / shadow / live,
deployment, exchange-write, production keys, authenticated APIs,
private endpoints, user stream, MCP, Graphify, `.mcp.json`, or
credentials.
