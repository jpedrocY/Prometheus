# Phase Workflow Standard

## Title

Prometheus Phase Workflow Standard — master phase lifecycle manual.

## Purpose

This document is the authoritative in-repo description of how a Prometheus
phase moves from a recommendation to a merged, recorded change in `main`.
Its purpose is to keep the project safe, ordered, and auditable across
chats, across implementation agents, and across time.

A new chat may understand the project's content but miss that a
branch-complete phase still requires operator review, a merge prompt, a
merge into `main`, and a merge-closeout report before the next phase can
even be recommended. This standard makes that lifecycle authoritative
inside the repository so it does not depend on chat memory.

## Authority

This document is **process-only**. It does not revise any retained
verdict, project lock, M0 governance, manifest state, label artefact, or
strategy decision. Where this standard conflicts with a specialist
domain document on technical content, the specialist document wins.
Where another process file conflicts on lifecycle, prompt design, report
shape, merge-closeout structure, or chat handoff content, the
domain-specific process file wins for its own surface
(`phase-prompt-template.md`, `operator-report-standard.md`,
`merge-closeout-standard.md`, `chat-branching-handoff-standard.md`).

This standard does not authorize any successor phase. It does not
authorize Phase 4bj-E. It does not authorize label-family eligibility
gate implementation. It does not authorize ML, strategy, backtests,
acquisition, paper / shadow, live-readiness, deployment, exchange-write,
production keys, authenticated APIs, private endpoints, user stream,
MCP, Graphify, `.mcp.json`, or credentials.

## Core principle: repo is authoritative, not chat memory

The repository is the source of truth.

A new chat must not rely on summaries, scratchpads, or prior chat
context. A new chat must consult the repo:

- `docs/00-meta/current-project-state.md` for the high-level project
  state and the current phase block,
- the latest merge-closeout under `docs/00-meta/implementation-reports/`
  to confirm what was actually merged into `main`,
- the relevant phase implementation report to confirm what was actually
  done on a branch,
- any specialist governance file that owns the affected surface,
- `git rev-parse main` and `git rev-parse origin/main` to confirm
  current SHAs and remote sync state.

A phase recommendation that is not anchored to current repo state is
unsafe.

## Phase lifecycle overview

A Prometheus phase moves through eleven ordered lifecycle steps:

1. **Recommendation / debate.** A docs-only or in-chat conversation
   identifies a candidate next phase, scopes it, and surfaces
   constraints. Operator and ChatGPT debate the option set.
2. **Authorization prompt.** Operator (with ChatGPT's help) drafts a
   precise authorization prompt for Claude Code. The prompt names
   exactly one phase, the allowed tracked files, the allowed local
   gitignored outputs (if any), the strict non-scope, the validation
   commands, and the fail-closed conditions.
3. **Branch execution.** Claude Code creates a branch, performs the
   authorized work, runs validation, and produces tracked commits and
   (if applicable) local gitignored artefacts.
4. **Implementation report + closeout.** Claude Code records a phase
   implementation report and a phase closeout under
   `docs/00-meta/implementation-reports/`, both committed on the
   branch.
5. **Operator review in ChatGPT.** Operator brings the branch report,
   closeout, and validation evidence to ChatGPT for plain-English
   review, blocker identification, and verification that scope was
   honoured.
6. **Merge prompt.** If review passes, operator (with ChatGPT) drafts
   a merge prompt for Claude Code. The merge prompt names the source
   branch, target branch, merge method, the merge-closeout file to
   create, and any required pre-merge validation.
7. **Merge into `main`.** Claude Code merges the branch into `main`
   using the standard merge method, pushes if instructed, and records
   the merge SHA.
8. **Merge-closeout.** Claude Code writes the merge-closeout report
   under `docs/00-meta/implementation-reports/` per
   `merge-closeout-standard.md`, commits it on `main`, and records
   final `main` / `origin/main` SHAs.
9. **Operator post-merge explanation.** Operator returns to ChatGPT
   for a post-merge plain-English summary that confirms what changed,
   what is still blocked, and what is not authorized.
10. **Next-phase recommendation or pause.** ChatGPT either recommends
    a precisely scoped next phase or recommends remain-paused, with
    explicit acknowledgement that no successor is authorized until
    operator decides.
11. **Chat branching handoff.** If continuation is in a new chat,
    operator (with ChatGPT) prepares a handoff per
    `chat-branching-handoff-standard.md` that anchors the new chat to
    repo state.

A phase that stops at step 3 or 4 is **branch-complete**, not
**project-complete**. A phase is project-complete only after step 8.

## Phase states

A phase carries one of the following states at any moment:

- **Proposed** — appears in conversation as a candidate, not yet
  authorized.
- **Authorized** — operator has issued an authorization prompt to
  Claude Code naming exactly this phase.
- **Branch-complete** — Claude Code has executed and committed on a
  branch with implementation report and closeout, but the branch is
  not yet merged.
- **Reviewed** — operator (with ChatGPT) has reviewed the branch and
  found no blockers, but the branch is not yet merged.
- **Merge-ready** — operator has issued a merge prompt to Claude Code.
- **Merged** — branch has been merged into `main` and (if instructed)
  pushed to `origin/main`, but merge-closeout is not yet recorded.
- **Merge-closeout recorded** — merge-closeout report has been
  committed on `main`. This is the only state at which the phase is
  project-complete.
- **Paused** — phase is intentionally not progressing further; this is
  a recommended terminal state for a project arc that should remain at
  the current evidence boundary.
- **Fail-closed / stopped** — Claude Code (or operator) detected a
  precondition violation, scope violation, validation failure, or
  ambiguity, and stopped without further action.

## Branch-complete vs project-complete

**A phase is not project-complete until it is merged into main and its merge-closeout is recorded.**

This rule is binding. It applies to every phase, including docs-only
phases, code phases, code+local-output phases, and read-only QA phases.

Branch-complete work that is reviewed but not merged is **not** the
project's current state — `main` is. The retained verdict ledger,
project locks, manifest states, governance contracts, and the
`current-project-state.md` "Current phase" block reflect what is on
`main`. Branch-complete work that is never merged is research-evidence
that did not enter the project record.

## Mandatory merge-closeout rule

Every phase that is merged into `main` must produce a merge-closeout
report under `docs/00-meta/implementation-reports/` matching the
structure in `merge-closeout-standard.md`. The merge-closeout records:

- phase identity,
- pre-merge `main` SHA,
- branch commit SHAs,
- merge commit SHA,
- final `main` / `origin/main` SHA after merge-closeout commit,
- merge method,
- files brought forward,
- diff summary,
- result / verdict,
- local gitignored outputs (if any),
- validation results,
- upstream immutability evidence (if applicable),
- manifest state preservation (if applicable),
- boundary confirmations,
- retained verdict ledger,
- preserved project locks,
- no-rescue constraints,
- successor authorization status,
- recommended state.

Without this report, the project record is incomplete.

## Successor authorization rule

A merge-closeout must explicitly state whether any successor phase is
authorized. The default is **no successor authorized**. A successor
phase becomes authorized only when:

1. operator explicitly chooses to proceed,
2. the next phase is named, scoped, and given an authorization prompt
   that satisfies `phase-prompt-template.md`,
3. the precondition phases (the predecessor merge-closeout, the
   relevant governance memos, the relevant evidence artefacts) are all
   present in `main`.

Claude Code must not invent a successor. ChatGPT must not imply a
successor is automatic. Operator decisions are explicit.

## Local gitignored artefact rule

Some phases produce local artefacts that are intentionally
gitignored — for example, label parquet files and label manifests
under `data/microstructure/`, gate reports under
`data/microstructure/gate-reports/`, and successor-state files under
`data/microstructure/successor-state/`. These artefacts must be:

- recorded in the implementation report and merge-closeout with
  absolute paths, sizes, SHA256s, and the explicit "not committed"
  status,
- preserved bit-for-bit across phases that do not modify them,
- never committed (`git check-ignore -v` must confirm gitignore
  coverage),
- never assumed to exist by a phase that does not produce them — if a
  later phase needs them, the prerequisite must be satisfied (the
  artefact must be present locally or be explicitly out of scope).

`data/microstructure/` outputs must not be committed under any
circumstance.

## Manifest mutation rule

Manifest state transitions are governed by phase-specific rules. By
default:

- `research_eligible` flips from `false` to `true` only via an
  explicit, separately authorized eligibility-gate or successor-state
  phase whose authorization prompt names the manifest.
- `eligibility_gate_status` transitions from `"pending"` only via an
  explicit, separately authorized phase.
- `chronological_split_policy` is changed only via an explicit,
  separately authorized phase.

A QA, inspection, or descriptive-evidence phase must not transition
any of these. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant must be preserved across every phase.

## Repo-query requirement for new chats

A new chat must, before recommending or executing any phase:

1. Read `docs/00-meta/current-project-state.md` and identify the
   current phase block.
2. Read the most recent merge-closeout under
   `docs/00-meta/implementation-reports/`.
3. Read the most recent phase implementation report.
4. Confirm `git rev-parse main == git rev-parse origin/main`.
5. Confirm whether the latest phase is **branch-complete** (no
   merge-closeout) or **merge-closeout recorded** (project-complete).
6. Confirm any local data assumptions that the candidate next phase
   will rely on (for example, presence and SHA256 of a label parquet
   under `data/microstructure/labels/`).
7. Confirm retained verdicts and project locks have not silently
   shifted between summaries.

A new chat that skips this step is unsafe and must be corrected.

## Operator / ChatGPT / Claude Code role split

- **Operator** — the human authority. Approves authorization prompts,
  reviews branch reports, decides whether to merge, decides whether to
  pause, decides whether to authorize the next phase. Owns
  high-stakes choices: live-readiness, key creation, capital exposure.
- **ChatGPT** — the interpreter, reviewer, teacher, phase navigator,
  and operator-facing explainer. Helps draft authorization prompts,
  reviews branch reports in plain English, identifies blockers,
  confirms scope honoured, recommends merge or pause, recommends next
  phase or remain-paused, prepares chat handoffs. Does **not**
  modify the repo. Does not authorize phases on its own.
- **Claude Code** — the executor and recorder inside the repo. Reads
  authorization prompts, performs precisely the authorized work,
  produces compact reports, fails closed on scope violation,
  preconditions failure, validation failure, or ambiguity. Does not
  invent scope. Does not authorize successors.

These roles are deliberately separated. ChatGPT sees plain English and
intent. Claude Code sees scope and execution. Operator sees both and
decides.

## Standard lifecycle checklist

Before executing a phase, operator confirms:

- [ ] Authorization prompt names exactly one phase.
- [ ] Authorization prompt lists allowed tracked files.
- [ ] Authorization prompt lists allowed local gitignored outputs (if
      any).
- [ ] Authorization prompt lists strict non-scope.
- [ ] Authorization prompt lists validation commands.
- [ ] Authorization prompt lists fail-closed conditions.
- [ ] Authorization prompt forbids modification of any
      `data/microstructure/` file unless explicitly allowed.
- [ ] Authorization prompt forbids transitioning
      `research_eligible`, `eligibility_gate_status`, or
      `chronological_split_policy` unless explicitly allowed.
- [ ] Authorization prompt forbids authorizing successor phases.

Before reviewing a branch, operator confirms:

- [ ] Implementation report exists and is committed on the branch.
- [ ] Closeout exists and is committed on the branch.
- [ ] Validation results are recorded.
- [ ] Scope was honoured.
- [ ] No `data/microstructure/` write outside the allowed surface.

Before merging, operator confirms:

- [ ] Branch is reviewed.
- [ ] No blockers were identified.
- [ ] Merge prompt names source branch, target branch, merge method,
      merge-closeout file.

After merging, operator confirms:

- [ ] Merge-closeout is committed on `main`.
- [ ] Final `main` / `origin/main` SHA is recorded in the
      merge-closeout.
- [ ] `current-project-state.md` reflects the merged phase.

## When to pause

The default recommendation after every merge-closeout is
**remain paused**. Pausing is a deliberate state, not a failure.
Pause when:

- the current arc has reached an evidence boundary and proceeding
  would require new authorization,
- the next sensible step is operator-driven (for example, deciding
  whether to authorize a label-family eligibility gate),
- there is no precondition-satisfied next phase that is both safe and
  high-value,
- the current phase produced descriptive evidence and the next move
  requires governance design rather than execution.

Pausing is the correct state most of the time.

## When to fail closed

Claude Code must fail closed (return `FAIL_CLOSED` or `STOPPED`) when:

- precondition verification fails (wrong SHA, missing predecessor
  merge-closeout, missing required artefact, gitignore coverage
  missing where required),
- scope violation would be required to satisfy the prompt,
- validation fails on a strict gate (ruff, mypy, pytest scoped to the
  surface),
- ambiguity prevents safe execution and the prompt does not allow
  pausing,
- a forbidden activity is implied (data acquisition, manifest
  transition, ML, strategy, backtest, paper / shadow / live, MCP,
  Graphify, credentials).

Failing closed is preferred over guessing.

## Required references for future chats

A future chat must reference:

- this standard,
- `docs/00-meta/process/phase-prompt-template.md`,
- `docs/00-meta/process/operator-report-standard.md`,
- `docs/00-meta/process/merge-closeout-standard.md`,
- `docs/00-meta/process/chat-branching-handoff-standard.md`,
- `docs/00-meta/current-project-state.md`,
- the most recent merge-closeout,
- the most recent phase implementation report.

## Examples of correct lifecycle sequencing

**Example A — docs-only phase that pauses after merge.**

1. Operator and ChatGPT debate whether to author a docs-only memo.
2. Operator drafts authorization prompt for Phase X (docs-only).
3. Claude Code creates branch `phase-X/...`, writes the memo and
   closeout, runs validation, commits.
4. Operator brings branch to ChatGPT for review.
5. Review passes; operator drafts merge prompt.
6. Claude Code merges and writes merge-closeout on `main`.
7. ChatGPT post-merge summary confirms what changed, what is still
   blocked, what is not authorized.
8. Recommendation: remain paused.

**Example B — code + local gitignored output phase.**

1. Operator authorizes Phase Y (code + docs + local gitignored
   output) with explicit scope.
2. Claude Code creates branch, implements code, runs the kernel
   exactly once, produces local artefacts under
   `data/microstructure/...`, commits tracked code + reports.
3. Local artefacts are recorded with paths and SHA256 in the
   implementation report.
4. Operator review, merge prompt, merge, merge-closeout.
5. Merge-closeout records local artefact SHA256s and "not committed"
   status.
6. Recommendation: remain paused.

**Example C — read-only QA phase.**

1. Operator authorizes Phase Z (read-only QA) with explicit
   "no-mutation" scope.
2. Claude Code reads the artefacts, computes evidence, writes a memo
   that records what was read and confirms nothing was changed.
3. Operator review, merge prompt, merge, merge-closeout.
4. Merge-closeout records SHA-preservation evidence.
5. Recommendation: remain paused.

## Examples of forbidden lifecycle collapse

- Treating a branch-complete phase as if it were on `main`.
- Recommending a successor phase before the predecessor's
  merge-closeout exists.
- Skipping the merge-closeout and moving to the next authorization
  prompt.
- Treating ChatGPT review as a substitute for the merge.
- Treating a passing pytest run as authorization to flip
  `research_eligible`.
- Treating a label QA pass as authorization to design ML or strategy.
- Treating a feature-family gate pass as authorization to acquire
  more data.
- Authorizing the next phase from a chat handoff alone, without
  confirming `main` SHA and the latest merge-closeout.

## Preserved project governance

This standard preserves verbatim:

- §11.6 = 8 bps per side,
- round-trip = 16 bps,
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops,
- Phase 3p §4.7,
- Phase 3r §8,
- Phase 3v §8,
- Phase 3w §6 / §7 / §8,
- Phase 4j §11,
- Phase 4k,
- Phase 4p,
- Phase 4q,
- Phase 4v,
- Phase 4w,
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template,
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy,
- the full retained verdict ledger (H0, R3, R1a, R1b-narrow, R2, F1,
  D1-A, 5m thread, V2, G1, C1).

## Change-control process for this standard

This standard may be updated only by:

- a separately authorized docs-only process phase that names this file
  in its allowed tracked files,
- with a corresponding implementation report and closeout,
- merged into `main` with a merge-closeout that records the change,
- and a narrow `current-project-state.md` paragraph addition.

This standard does not transition any technical state. Updating it
does not authorize any successor phase, does not modify any
manifest, does not enable ML / strategy / backtests, and does not
imply readiness for paper / shadow / live / deployment / exchange-write.
