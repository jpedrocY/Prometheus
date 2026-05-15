# Claude Code Context Management Standard

## Title

Prometheus Claude Code Context Management Standard — thin contractual
prompts, mandatory vs optional reads, fresh-session management, report
compression, reusable non-authorization block usage, and MCP / Graphify
governance for Prometheus phases executed by Claude Code.

## Purpose

Prometheus phases are executed inside Claude Code sessions whose context
window is a finite resource. As the project's repo standards have grown
(`phase-workflow-standard.md`, `phase-risk-tiering-standard.md`,
`phase-prompt-template.md`, `operator-report-standard.md`,
`merge-closeout-standard.md`, `chat-branching-handoff-standard.md`),
Claude Code execution prompts have also grown — frequently restating
the same governance blocks, the same retained verdict ledger, the same
non-authorization lists, and the same mandatory read lists in every
phase. Operator reports have grown in parallel.

That growth has become a workflow risk. Oversized prompts, repeated full
governance blocks, excessive mandatory reading, long operator reports,
and stale session carryover can drive Claude Code into auto-compact
loops, increase token consumption without adding safety, and reduce the
operator's ability to read what Claude Code actually did.

This standard fixes that problem **without weakening governance**. The
solution is not vague prompts. The solution is **thin contractual
prompts backed by repo-owned process standards**. Stable rules live in
repo docs. Prompts carry only the phase execution contract.

This standard is **prospective only**. It does not rewrite prior phase
history. Prior large prompts and prior long reports remain valid
records of prior practice. They were correct under the governance that
existed at the time. Future prompts should be thinner because the
standards now exist in repo docs and can be referenced rather than
restated.

## Authority

This document is **process-only**. It does not revise any retained
verdict, project lock, M0 governance, manifest state, label artefact,
gate protocol, canonical path policy, strategy decision, or successor
authorization. Where this standard conflicts with a specialist domain
document on technical content, the specialist document wins. Where this
standard conflicts with another process file on lifecycle, prompt
design, report shape, merge-closeout structure, or chat handoff
content, the domain-specific process file wins for its own surface
(`phase-workflow-standard.md`, `phase-prompt-template.md`,
`operator-report-standard.md`, `merge-closeout-standard.md`,
`chat-branching-handoff-standard.md`, `phase-risk-tiering-standard.md`).

This standard does not authorize any successor phase. It does not
authorize Phase 4bm-B. It does not authorize multi-day normalization
implementation, features, labels, diagnostics, ML, strategy, backtests,
acquisition, paper / shadow, live-readiness, deployment, exchange-write,
production keys, authenticated APIs, private endpoints, user stream,
MCP, Graphify, `.mcp.json`, or credentials. It does not enable any
new tooling.

## Core principle

**Repo docs carry stable rules. Prompts carry the phase execution
contract.**

A well-formed Claude Code prompt names exactly what this phase must do,
which files it may touch, what is forbidden, what to validate, and
where to read the binding governance from in the repo. It does not
restate the full governance text. Claude Code should read the
authoritative repo docs (per the mandatory read policy in §6) instead
of receiving the full governance text pasted into every prompt.

A separate, equally important principle: **short prompts are safe only
when they are contractual and reference the correct repo standards.
Short vague prompts are not acceptable.** A thin prompt that omits the
allowed surface, the forbidden surfaces, the validation contract, or
the fail-closed conditions is not "thin" — it is incomplete.

## Scope

This standard applies prospectively to:

- branch execution prompts (every authorized phase),
- merge prompts (every separately authorized merge phase),
- operator reports produced by ChatGPT after a phase or merge,
- Claude Code session management across phases,
- chat branching and handoffs,
- MCP / Graphify / external tooling considerations,
- the use of the Phase 4bl-F reusable non-authorization blocks.

It does **not** apply retroactively. Prior phase prompts and prior
phase reports remain valid records of prior practice.

## Thin Execution Prompt Standard

Every future branch execution prompt should include exactly these
fields, in this order, expressed contractually rather than narratively.
The full Phase 4bk-A authorization-prompt structure in
`phase-prompt-template.md` remains the canonical reference. This
section defines what minimum content a thin contractual prompt must
include and what content may be referenced instead of pasted in full.

### Required fields

1. **Project / repo / local path.** "Prometheus, `C:\Prometheus`."
2. **Current task.** One short sentence naming the phase.
3. **Phase name and identifier.** Exact name (e.g. "Phase 4bm-A-P1 —
   Claude Code Context Management / Thin Prompt Standard"). Exact
   identifier (e.g. "Phase 4bm-A-P1").
4. **Phase tier.** Tier 1 / 2 / 3 / 4 per
   `phase-risk-tiering-standard.md` (Phase 4bl-F). State the tier
   explicitly. When in doubt, default to the higher tier.
5. **Branch name.** Exact branch name to create.
6. **Latest project-complete phase.** Exact predecessor phase
   identifier and name, and the merge-closeout SHA or commit
   reference. The prompt should not paste the predecessor merge-
   closeout in full; it should name it.
7. **Objective.** One short paragraph (target: 3–6 sentences)
   describing what the phase must do, without restating the project's
   entire history.
8. **Mandatory read list.** The default set defined in §6 plus any
   immediately relevant predecessor implementation report or
   merge-closeout. Do not list every prior implementation report.
9. **Optional read / search rule.** State that older reports may be
   read only if a SHA, path, policy, gate rule, or precedent is
   missing, and that search / grep should be used before opening many
   full documents.
10. **Allowed tracked files.** Enumerate every tracked file Claude
    Code may create or modify. Anything not listed is forbidden.
11. **Allowed local artefacts, if any.** Enumerate every local
    gitignored path Claude Code may produce, with the "not committed"
    requirement and the `git check-ignore -v` validation requirement.
    If the phase produces none, state "none."
12. **Explicitly forbidden surfaces.** State the forbidden tracked
    surfaces (e.g. "no source / test / script / config changes"),
    the forbidden local surfaces (e.g. "no writes under
    `data/microstructure/` outside the allowed surface"), and the
    forbidden activities that are not covered by referenced blocks.
13. **Standard non-authorization blocks to apply by reference.** Cite
    the relevant Phase 4bl-F reusable blocks by name
    (`N-ACQUISITION`, `N-ENDPOINT`, `N-CREDENTIALS`, `N-MANIFEST`,
    `N-GATE-RERUN`, `N-SUCCESSOR-STATE`, `N-DERIVATION`,
    `N-DIAGNOSTICS-ML-STRATEGY`, `N-PHASE-5`, `N-VERDICT-LOCK`) rather
    than pasting them in full. Treat cited blocks as binding.
14. **Deliverables.** Enumerate every deliverable (tracked files
    added, tracked files modified narrowly, local artefacts, reports).
15. **Validation commands.** Exact commands to run and the expected
    pass criteria. For docs-only Tier 1 / Tier 4 phases this is
    typically `git diff --check` and `git status`. For code phases
    this typically includes `ruff`, `mypy`, scoped `pytest`, and
    gitignore confirmation. Do not require `ruff` / `mypy` / `pytest`
    when no source / test / script / configuration file is touched.
16. **Stop condition.** State explicitly that Claude Code stops after
    branch work, that merge is not part of this phase (unless this
    is a merge prompt), and that no successor is authorized.
17. **Final operator report requirement.** Reference the
    `operator-report-standard.md` 10-item compact format. The prompt
    should not paste the format in full; it should name it.

### Content that should normally be omitted

Future thin prompts should avoid pasting:

- the retained verdict ledger in full, unless the phase touches
  verdicts (Tier 1; rare);
- the full preserved project locks list, unless the phase touches
  any lock (Tier 1; rare);
- the full set of nine reusable non-authorization blocks (cite by
  name);
- long lists of historical reports unless directly needed;
- the entire `phase-prompt-template.md` text (reference it);
- the entire `phase-workflow-standard.md` text (reference it);
- the entire `phase-risk-tiering-standard.md` text (reference it);
- restatements of the operator / ChatGPT / Claude Code role split
  (reference it);
- restatements of the Phase 4aw `flip_research_eligible(...)`
  always-raises invariant, the Phase 4bb-F canonical path policy,
  or the Phase 4al refined no-rescue rule unless the phase touches
  one of those directly (rare; Tier 1 typically).

### Content that must never be omitted

A thin prompt must still include:

- the allowed tracked surface list,
- the allowed local artefact list (or "none"),
- the validation contract,
- the explicit non-scope (either by reference to the reusable blocks
  by name, or by explicit statement for phase-specific prohibitions),
- the stop condition,
- a clear statement that no successor is authorized.

Omitting any of these makes the prompt incomplete, not thin.

### Tone

Thin prompts are contractual. They state what Claude Code must do and
must not do. They do not narrate project history. They do not motivate
decisions in essay form. They assume Claude Code will read the
authoritative repo docs (per §6) for context.

## Thin Merge Prompt Standard

Every future merge prompt should include exactly these fields, in this
order:

1. **Source branch.** Exact branch name.
2. **Target branch.** `main`.
3. **Expected base.** The pre-merge `main` SHA, with instruction to
   verify `git rev-parse main == git rev-parse origin/main`.
4. **Latest project-complete phase.** Exact predecessor merge-closeout
   commit.
5. **Expected tracked files.** Enumerate the tracked files the merge
   should bring forward (typically: the phase's implementation
   report, the phase's closeout, the narrow
   `current-project-state.md` update, any other narrow tracked
   changes named by the original authorization prompt).
6. **Expected local artefacts, if any.** Enumerate local artefacts
   the phase produced that should remain on disk after the merge,
   with their SHA256s. If the phase produced none, state "none."
7. **Merge constraints.** `git merge --no-ff` with `ort` strategy.
   No `--no-verify`. No `--no-gpg-sign`. No force-push. No skip-hooks.
   No modification of branch contents during merge.
8. **Validation commands.** Pre-merge validation (`git status`,
   `git rev-parse`, `git diff --stat`), merge validation
   (`git diff --check`), and any phase-specific validation. Do not
   rerun expensive phase execution commands unless explicitly
   required by the merge prompt.
9. **Merge-closeout filename.** Exact path under
   `docs/00-meta/implementation-reports/`. Per
   `merge-closeout-standard.md`, Tier 1 / 2 / 3 phases use the full
   16-section structure; Tier 4 phases may use the short-form
   structure.
10. **Merge-closeout required facts.** Reference
    `merge-closeout-standard.md` for the structure. Name the specific
    facts the closeout must record (e.g. the four SHAs in §2, the
    diff summary in §5, the local artefact SHAs in §7 if applicable).
    Do not paste the full standard.
11. **Final verification commands.** `git status`,
    `git log --oneline -8 --decorate`, `git rev-parse main`,
    `git rev-parse origin/main`, and any phase-specific verification.
12. **Stop condition.** State explicitly that no successor phase is
    authorized by the merge, that the merge-closeout's "Successor
    authorization" section must read **None**, and that the
    "Recommended state" section should default to **Remain paused**
    unless the operator's separate decision has indicated otherwise.

### Content that should normally be omitted

Future thin merge prompts should avoid:

- pasting the full retained verdict ledger (cite the
  `merge-closeout-standard.md` requirement instead);
- pasting the full preserved project locks list (cite the standard);
- pasting the full no-rescue constraint list (cite the standard;
  customize only for phase-specific items);
- asking Claude Code to reread unrelated old reports unless needed;
- rerunning expensive phase execution commands (the phase already
  ran them on the branch).

### Content that must never be omitted

A thin merge prompt must still include:

- the source branch,
- the expected base SHA,
- the merge method,
- the merge-closeout filename and required-facts reference,
- the validation contract,
- the stop condition.

## Mandatory vs Optional Read Policy

Most phases follow the same lifecycle context. Most phases do not need
to reread every prior report.

### Default mandatory read list

For most phases, Claude Code should read exactly these files before
executing:

- `docs/00-meta/current-project-state.md`
- `docs/00-meta/process/phase-workflow-standard.md`
- `docs/00-meta/process/phase-risk-tiering-standard.md`
- `docs/00-meta/process/claude-code-context-management-standard.md`
  (this file)
- `docs/00-meta/process/phase-prompt-template.md`
- `docs/00-meta/process/operator-report-standard.md`
- `docs/00-meta/process/merge-closeout-standard.md`
- the immediate predecessor implementation report
  (`docs/00-meta/implementation-reports/.../...md`)
- the immediate predecessor closeout or merge-closeout
  (`docs/00-meta/implementation-reports/.../...md`)

This default applies to Tier 1, Tier 2, Tier 3, and Tier 4 phases.
`phase-workflow-standard.md` and `phase-risk-tiering-standard.md`
remain mandatory because they define lifecycle and ceremony. This
standard is mandatory because it defines prompt and session
discipline.

### Optional read / search

Older reports should be read only when:

- a SHA, path, policy, gate rule, or precedent is missing from the
  default mandatory reads,
- a phase-specific predecessor is named in the authorization prompt
  beyond the immediate predecessor,
- a specialist governance memo is directly relevant (e.g.
  Phase 4ak M0 for any phase that touches M0; Phase 4bb-F for any
  phase that touches sidecar formatting; Phase 4al for any phase
  that touches the no-rescue rule),
- a domain-specific implementation detail must be cited verbatim.

**Use search / grep first.** Prefer `Grep` over reading many full
documents. A targeted search for a specific SHA, policy clause,
or precedent is much cheaper in context than reading entire memos.

**Read full reports only when a search match warrants the full
context.** A line match in an old implementation report does not
justify reading the entire report — read the surrounding section.

### Tier-specific guidance

- **Tier 1 (Full Phase).** May require broader reads when new
  semantics or high-risk transitions justify it. Tier 1 phases that
  introduce new data semantics, new gate protocols, or new manifest
  state transitions should read the specialist governance memos that
  own the affected surface (e.g. Phase 4bb-F for any new canonical
  path; Phase 3v §8 for any new stop-trigger-domain handling;
  Phase 4j §11 for any metrics OI handling).
- **Tier 2 (Controlled Remediation).** Read the standing rule that
  authorizes the fix (e.g. R-SIDECAR-CRLF in
  `phase-risk-tiering-standard.md` §5). Do not read unrelated phase
  history.
- **Tier 3 (Batch).** Read the prior Tier 1 phase that introduced
  the operation template. Do not reread every prior batch.
- **Tier 4 (Administrative).** The default mandatory list is
  usually sufficient.

### Anti-pattern

Reading a large historical report "for reassurance" is not a valid
reason. If the prompt does not name the report and the report is not
the immediate predecessor, do not read it unless a specific question
about a SHA / path / policy requires it.

## Session Management Guidance

Claude Code session context is a finite resource. The following
practices reduce context pressure without harming evidence quality.

### Recommended session rhythm

- **Use a fresh Claude Code session for each branch execution
  phase.** Each authorized phase is a complete unit of work. Starting
  fresh prevents carryover from unrelated prior phases.
- **Use a fresh Claude Code session for each merge phase when
  practical.** A merge phase is much smaller than a branch execution
  phase. Starting fresh keeps the merge prompt focused on merge
  verification rather than reusing branch-execution context.
- **Clear after closeout.** When a phase is branch-complete (the
  implementation report and closeout are committed on the branch),
  the active session has done its work. Move to operator review.
- **Avoid carrying many prior phases in active Claude Code
  conversation history.** Long sessions that span many phases pay
  context-management costs without adding safety.

### Context monitoring

When context pressure is high, the operator may observe:

- Claude Code's responses become slower or noticeably more compact,
- the auto-compact behavior triggers more often,
- Claude Code references context-window limits in tool output,
- token consumption per tool call increases visibly.

When any of these appear, the correct response is:

- **Prefer clearing and restarting with a thin handoff** when a task
  boundary (phase complete, merge complete) has been reached.
- **Compact only when the current session must continue** and the
  task boundary has not been reached. Compaction is a
  context-recovery tool, not a routine workflow step.

### Operator-side commands (informational)

The Claude Code CLI provides commands that the operator can use to
manage context. These commands are not part of repo-critical
validation; they are operator guidance. The exact command names and
behaviors may evolve with the Claude Code product:

- the operator may inspect approximate context usage,
- the operator may clear the current session and start fresh,
- the operator may explicitly compact when needed.

Repo standards do not require any particular CLI command behavior.
Repo standards require that the operator can read what Claude Code
did, that prompts remain contractual, and that reports remain
operator-readable.

### When to branch a chat

Branching a chat (per `chat-branching-handoff-standard.md`) is for
context refresh between phases. It is not for routine in-phase work.
Branch when:

- the active chat has accumulated context spanning multiple phases,
- a complex multi-phase arc has just completed a merge-closeout and a
  fresh thread would benefit the next debate,
- a phase changes scope (e.g. moving from a research arc to a
  process arc, or moving from the trading project to a sibling
  energy-market project),
- the operator is onboarding a new ChatGPT thread after time has
  passed.

## Report Compression Standard

Operator reports should focus on what happened, what changed, and what
was preserved. They should not reprint stable governance.

### What a phase-completion operator report should include

A well-formed Claude Code phase-completion report should include:

- **Phase identity.** Phase identifier and name. Phase tier.
- **Branch.** Branch name.
- **Base SHA.** The pre-branch `main` SHA at branch creation.
- **Commit SHAs.** The branch commit SHAs in order.
- **Files changed.** Exact list of tracked files added, modified,
  or deleted. Group by category (docs, source, tests, scripts,
  configs).
- **Local artefacts.** Exact paths, sizes, and SHA256s of any local
  gitignored artefacts produced, with the "not committed" status and
  `git check-ignore -v` confirmation.
- **Validation commands and results.** Exact commands run, exact
  outputs (or relevant snippets), and pass / fail status.
- **Boundary deviations, if any.** If any allowed surface boundary
  was approached or exceeded, state it explicitly. If none, this
  section is "none."
- **Final `git status`.** Exact output.
- **Final `git log --oneline -8 --decorate`.** Exact output.
- **Recommended state.** Default: "remain paused unless operator
  separately authorizes."
- **Explicitly unauthorized successors.** Name the candidate
  successors and state they are not authorized.

This corresponds to the `operator-report-standard.md` 10-item compact
format, augmented with the additional facts that are specific to a
phase report (vs a routine action report).

### What an operator report should normally omit

A well-formed operator report should not:

- reprint every reusable non-authorization block if the relevant
  blocks were applied by reference and no deviation occurred
  (state which blocks applied; cite them by name);
- reprint the full retained verdict ledger if no verdict was
  touched (state "preserved verbatim per merge-closeout standard
  §12");
- reprint the full preserved project locks list if no lock was
  touched (state "preserved verbatim per merge-closeout standard
  §13");
- restate the full project history;
- restate the entire authorization prompt;
- include long narrative justification for routine boundary
  preservation.

### Distinguish fact from claim

- **Facts** are anchored to SHAs, file paths, exact command output,
  and `git status` / `git log` evidence.
- **Claims** are interpretations ("this preserves governance",
  "this is a low-risk fix"). Claims should be supported by facts.
- Reports should mark which is which. ChatGPT's operator-facing
  responses translate facts and claims into plain English.

### Deviation reporting

If a deviation occurred (a boundary was approached but not crossed,
a forbidden activity was implied by the prompt and Claude Code had
to decline, an ambiguity required operator guidance), state it
explicitly under "Boundary deviations." Do not bury deviations
among non-blocking notes.

### Length guidance

A docs-only Tier 4 phase report may be very short (under one screen
of output). A docs-only Tier 1 process-standardization phase report
may be longer (several screens) because new content must be
introduced. A code-and-local-artefact Tier 1 phase report may be
longer still because exact artefact paths, sizes, SHA256s, and
validation results take space. Length should match content, not
ceremony.

## Reusable Non-Authorization Block Usage

`docs/00-meta/process/phase-risk-tiering-standard.md` (Phase 4bl-F) §7
defines nine canonical reusable non-authorization blocks:

- `N-ACQUISITION` — No acquisition.
- `N-ENDPOINT` — No endpoint calls.
- `N-CREDENTIALS` — No credentials, no exchange-write.
- `N-MANIFEST` — No manifest mutation.
- `N-GATE-RERUN` — No gate rerun.
- `N-SUCCESSOR-STATE` — No successor-state.
- `N-DERIVATION` — No normalization, derivation, features, or labels.
- `N-DIAGNOSTICS-ML-STRATEGY` — No diagnostics, ML, strategy, or
  backtest.
- `N-PHASE-5` — No Phase 5, paper / shadow, or live.
- `N-VERDICT-LOCK` — No retained verdict or project lock change.

### Citation rules

- Future prompts **may** cite these blocks by name rather than
  restating them in full. Example: "Non-authorization blocks
  `N-ACQUISITION`, `N-ENDPOINT`, `N-CREDENTIALS`, `N-MANIFEST`,
  `N-GATE-RERUN`, `N-SUCCESSOR-STATE`, `N-DERIVATION`,
  `N-DIAGNOSTICS-ML-STRATEGY`, `N-PHASE-5`, and `N-VERDICT-LOCK`
  apply."
- Claude Code **must** treat cited blocks as binding. Citation is
  not a softening.
- Claude Code **should not** restate cited blocks fully in the
  operator report unless the `operator-report-standard.md` requires
  it (e.g. on deviation) or unless the prompt explicitly requires
  it.

### Custom prohibitions

If a phase needs a prohibition that is not covered by the canonical
blocks, the prompt must state it explicitly. The canonical blocks
are not exhaustive; they are common-case shortcuts.

### Tier interaction

- **Tier 1 (Full Phase).** Should cite the relevant blocks by name
  in the prompt and may expand them fully in the implementation
  report when ceremony justifies it. Per
  `phase-risk-tiering-standard.md` §3, Tier 1 phases should still
  expand the relevant blocks in their full ceremony for clarity, but
  citation by name is acceptable when every cited block applies.
- **Tier 2 (Controlled Remediation).** Cite blocks by name. The
  short-form report (per `phase-risk-tiering-standard.md` §8) need
  not expand them.
- **Tier 3 (Batch).** Cite blocks by name. Per-item reports do not
  need to repeat the blocks.
- **Tier 4 (Administrative).** Cite blocks by name in a minimal
  fashion or omit if the prompt's strict non-scope already covers
  the case.

## Allowed Surface Lists

Every future execution prompt must define allowed surfaces explicitly.

### What "allowed surface" means

The allowed surface is the set of files Claude Code is permitted to
create, modify, or delete during the phase. Everything not in the
allowed surface is forbidden by default.

### Required allowed-surface fields

A prompt must define:

- **allowed tracked files.** Exact paths or path patterns. Anything
  not listed is forbidden.
- **allowed local gitignored output paths, if any.** Exact paths or
  path patterns. If the phase produces no local artefacts, state
  "none."
- **forbidden tracked surfaces.** Surfaces explicitly off-limits
  even if they fall in a permitted directory. Example: "no
  modifications to existing process standards under
  `docs/00-meta/process/` beyond named files."
- **forbidden local artefact surfaces.** Surfaces explicitly
  off-limits. Example: "no writes under `data/microstructure/`."
- **whether source / tests / scripts / configs may be touched.**
  State explicitly yes or no per category. The default is no.
- **whether `data/microstructure/` may be read or written.** State
  explicitly. The default is no for writes; reads may be permitted
  for QA phases.

### Deviation handling

If an operation needs to touch a file outside the allowed surface,
Claude Code must stop or report the deviation before continuing,
unless the prompt explicitly permits justified expansion. The
"justified expansion" language is rare and should be reserved for
phases where the operator anticipates the need.

### Why allowed surface lists matter more than long prose

The allowed surface list is the contract. If the list is exact, a
later reviewer (operator, ChatGPT, or a future audit) can compare
files-changed to the allowed surface and immediately detect scope
drift. Long prose explanations of what the phase "should" do are
much harder to audit.

## Handoff File Guidance

A handoff `.md` file (per `chat-branching-handoff-standard.md`)
should be used when a single execution prompt would otherwise be too
large or when context refresh is needed between sessions.

### When to use a handoff

- **Chat branching.** Continuing the project in a new ChatGPT thread.
- **Very large phase context.** When the phase's prompt would
  otherwise be too long even after applying this standard.
- **Transition between ChatGPT and Claude Code.** When ChatGPT has
  done significant interpretation that Claude Code needs to inherit.
- **Parallel project branches.** When the operator is working on a
  sibling project (e.g. an energy-market project) and needs to
  return to Prometheus context efficiently.
- **When a prompt would otherwise exceed reasonable size.** A
  handoff `.md` lets the prompt itself stay thin while the
  background context lives in a referenced file.

### What a handoff should and should not contain

A handoff should:

- summarize the current state (current `main` SHA, last completed
  phase, last merge-closeout path, current local data assumptions),
- point to repo docs as the binding authority,
- identify the recommended next phase or remain-paused.

A handoff should not:

- duplicate every process standard,
- duplicate the full retained verdict ledger and project locks
  (state "preserved per repo state"),
- become a replacement for repo verification,
- substitute for `git rev-parse main` / `git status` /
  `current-project-state.md` checks.

The "do not rely on handoff alone" rule in
`chat-branching-handoff-standard.md` §13 remains binding.

## Thin Prompt Size Guidance

Prompt size discipline is **guidance**, not a hard validation rule.

### Soft targets

- **Normal thin prompt target.** Short enough for Claude Code to
  keep context under control. The operator can judge this by
  observing whether Claude Code responds promptly and whether
  auto-compact triggers during the phase.
- **Complex Tier 1 phases may be longer** but should still
  reference standards rather than paste them.
- **If the prompt becomes very long because of repeated
  boilerplate**, the correct response is to move that boilerplate
  into a repo process standard (or cite an existing standard) and
  shrink the prompt.
- **Avoid embedding large tables of unchanged historical data**
  unless necessary. If the data is in a repo file, cite the file.

### Why no exact token count is binding

Claude Code's context behavior can change with model versions,
context-window upgrades, and tool definitions. A token count that
is safe today may not be safe later (or may be unnecessarily
restrictive). Repo standards therefore set discipline, not numeric
limits.

### When to consider a thin prompt "too long"

A thin prompt is too long when any of the following are true:

- Claude Code's auto-compact triggers during the phase's first few
  tool calls,
- the prompt includes large blocks that simply restate repo
  standards verbatim,
- the prompt includes historical content that does not affect the
  phase's execution,
- the operator finds the prompt hard to review for scope.

When any of these is true, the operator (with ChatGPT) should
shorten the prompt by replacing pasted content with citations to
repo docs.

## MCP / Graphify / Tooling Governance

This standard records the project's prospective posture on Model
Context Protocol (MCP) servers, the Graphify tool, and any future
external integration. The full applicable governance is in
`docs/00-meta/process/phase-risk-tiering-standard.md` (Phase 4bl-F),
the Phase 4ak M0 admissibility gate, and the Phase 4al refined
no-rescue rule. This section summarizes the posture.

### Current posture

- MCP and Graphify are **not enabled by default**.
- MCP and Graphify are **not** a first-line solution to prompt
  bloat. Prompt bloat is addressed first by thin contractual prompts,
  fresh sessions, canonical repo standards, and limited read lists
  (per §5–§11 of this standard).
- Enabling MCP, Graphify, `.mcp.json`, repo graph indexing,
  external tools, or any credentialed integration requires a
  separately authorized governance phase.
- Any future MCP / Graphify consideration must start **read-only,
  local-only, non-networked, and non-mutating** unless separately
  authorized. The default-deny posture applies.
- No exchange, credential, public endpoint, private endpoint, user
  stream, or live-readiness surface may be introduced through MCP /
  Graphify without a dedicated Tier 1 governance phase that
  specifically scopes the new surface.
- Phase 4bl-F's `N-CREDENTIALS` block applies to MCP / Graphify
  considerations: until a separately authorized governance phase
  changes the posture, MCP / Graphify is forbidden.

### Future evaluation criteria

If the project ever considers MCP / Graphify, the evaluation must
be a Tier 1 governance phase that addresses:

- exact integration scope (read-only? local-only? mutating?),
- exact tool inventory (which MCP servers, which Graphify
  capabilities),
- exact credential surface (none, or scoped non-production
  credentials only),
- exact data exposure (which repo paths, which artefacts),
- exact failure mode (what happens if the MCP server
  misbehaves),
- exact rollback (how to disable without state loss),
- exact audit trail (how MCP-driven changes are recorded).

No such evaluation is authorized by this standard.

### Why this is in this standard

Context-management concerns sometimes motivate "let's enable MCP /
Graphify to help Claude Code." This standard records that the
correct response to context pressure is **thinner prompts and fresh
sessions**, not new tooling. New tooling adds attack surface,
governance surface, and integration risk. The Prometheus project
will not trade governance discipline for context convenience.

## Escalation Rules

A prompt must expand beyond the thin format, or escalate to a fuller
Tier 1 treatment, if any of the following apply (per
`phase-risk-tiering-standard.md` §4):

- new data semantics are introduced,
- a new dataset family or dataset version is created,
- a gate protocol is changed,
- a validator is relaxed,
- a manifest is mutated,
- eligibility or admissibility interpretation changes,
- ML / strategy / backtest surfaces are introduced,
- network access is introduced,
- credentials or exchange surfaces are introduced,
- retained verdicts or project locks are touched,
- there is policy ambiguity.

In these cases, the thin format is insufficient because the prompt
must record new content rather than reference existing content.

### How escalation interacts with this standard

This standard does not weaken Tier 1 / Tier 2 / Tier 3 / Tier 4
rules. Thin prompts are a discipline that applies **after** tier
assignment. A Tier 1 phase may still use thin contractual language;
it simply needs to record the new content in full when new content
is being introduced.

## Relationship to Phase 4bl-F

Phase 4bl-F established the four-tier risk model
(`phase-risk-tiering-standard.md`), the standing R-SIDECAR-CRLF
remediation rule, the nine reusable non-authorization blocks, and
short-form report / batch-phase guidance. Phase 4bl-F is the
governance layer.

Phase 4bm-A-P1 (this standard) is the **operational layer**. It
defines how Claude Code prompts and sessions should operationalize
that governance.

The two standards complement each other:

- Phase 4bl-F says: "ceremony must be proportional to risk."
- Phase 4bm-A-P1 says: "and the prompts and reports that drive that
  ceremony should be thin contracts that reference repo standards
  rather than restate them."

Phase 4bl-F is not amended in substance by this standard. The only
narrow cross-references added to other process docs are pointers to
this file as a required reference.

## Relationship to Prior Prompts and Prior Reports

Prior large prompts and prior long reports remain valid records of
prior practice. They were appropriate while the project lacked
reusable standards. Future prompts should be thinner because the
standards now exist in repo docs.

This is a prospective workflow improvement, not a criticism or
rewrite of prior phases. Phase 4bl-D through Phase 4bm-A history is
preserved verbatim. Every prior merge-closeout stands.

## Non-Authorizations

Phase 4bm-A-P1 (this standard) explicitly does **not** authorize:

- Phase 4bm-B;
- multi-day normalization implementation;
- normalization execution of any kind;
- derived dataset generation;
- features;
- labels;
- diagnostics;
- ML;
- strategy implementation;
- strategy hypothesis generation;
- signal construction;
- backtest design or backtest execution;
- additional data acquisition (additional aggTrades / 5m / 1m /
  tick / mark-price 30m / 4h / order-book / spot / cross-venue /
  funding / open-interest);
- public-endpoint calls in code;
- authenticated APIs;
- private endpoints;
- WebSockets;
- user streams;
- credentials;
- `.env` creation or reading;
- `.mcp.json` creation or reading;
- MCP;
- Graphify;
- exchange-write;
- paper / shadow;
- live-readiness;
- deployment;
- production-key creation;
- manifest mutation (raw, derived, feature, or label);
- `research_eligible` flip on any actual manifest;
- `eligibility_gate_status` transition on any actual manifest;
- `chronological_split_policy` change on any actual manifest;
- changes to retained verdicts (H0, R3, R1a, R1b-narrow, R2, F1,
  D1-A, V2, G1, C1, 5m thread closure);
- changes to project locks (§11.6, round-trip, §1.7.3,
  Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8,
  Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w,
  Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw
  `flip_research_eligible(...)` always-raises invariant,
  Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk
  model + R-SIDECAR-CRLF standing rule + nine reusable
  non-authorization blocks);
- any successor phase whatsoever.

The recommended state after Phase 4bm-A-P1 is **remain paused**.

## Change-control process for this standard

This standard may be updated only by:

- a separately authorized docs-only Tier 1 process phase that names
  this file in its allowed tracked files;
- with a corresponding implementation report and closeout;
- merged into `main` with a merge-closeout per
  `merge-closeout-standard.md`;
- and a narrow `current-project-state.md` paragraph addition.

Updating this standard does not transition any technical state.
Updating it does not authorize any successor phase, does not modify
any manifest, does not enable ML / strategy / backtests, and does
not imply readiness for paper / shadow / live / deployment /
exchange-write.

## Required references for future chats

A future chat that uses this standard must also reference:

- `docs/00-meta/process/phase-workflow-standard.md` — master phase
  lifecycle manual,
- `docs/00-meta/process/phase-risk-tiering-standard.md` — tier
  ceremony, R-SIDECAR-CRLF standing rule, reusable non-authorization
  blocks,
- `docs/00-meta/process/phase-prompt-template.md` — authorization
  prompt structure (long-form),
- `docs/00-meta/process/operator-report-standard.md` — Claude Code
  compact report and ChatGPT operator-facing response shape,
- `docs/00-meta/process/merge-closeout-standard.md` — merge-closeout
  structure,
- `docs/00-meta/process/chat-branching-handoff-standard.md` — chat
  branching handoff structure,
- `docs/00-meta/current-project-state.md` — current project state,
- the most recent merge-closeout under
  `docs/00-meta/implementation-reports/`,
- the most recent phase implementation report.

## Final note

The Prometheus project's evidentiary discipline remains its
competitive advantage. This standard does not relax that discipline.
It shifts the operational cost of governance from prompt size and
session carryover to repo-resident standards, fresh sessions, and
contractual prompts. Stable rules belong in repo docs. Phase prompts
should carry the phase execution contract. Operator reports should
record what changed, what was preserved, and what is still
unauthorized.

This standard is prospective only. Prior phases remain valid as
recorded. Future phases should be thinner because the standards now
exist in repo docs and can be cited rather than restated.
