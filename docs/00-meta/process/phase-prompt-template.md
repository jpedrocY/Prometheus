# Phase Prompt Template

## Title

Prometheus Phase Prompt Template — standard structure for authorization
prompts that operator (with ChatGPT) issues to Claude Code.

## Purpose

This document specifies the standard shape of authorization prompts and
merge prompts for Prometheus phases. It exists to make prompts precise,
boundary-safe, validation-anchored, and consistent across chats so that
Claude Code's executor role can be performed without ambiguity.

A well-formed prompt names exactly one phase, the allowed tracked
files, the allowed local gitignored outputs (if any), the strict
non-scope, the validation commands, and the fail-closed conditions. A
malformed prompt invites scope drift, silent assumptions, or unsafe
execution.

This document is **process-only**. It does not authorize any phase.

## Prompt design principles

- **Declare the phase risk tier.** Every authorization prompt should
  declare the phase's risk tier per
  `docs/00-meta/process/phase-risk-tiering-standard.md`
  (Phase 4bl-F): Tier 1 (Full Phase), Tier 2 (Controlled
  Remediation), Tier 3 (Batch), or Tier 4 (Administrative / Docs
  Correction). When in doubt, default to the higher tier. The tier
  declaration determines whether a short-form report or short-form
  merge-closeout is permissible, whether a standing remediation
  rule applies, and which reusable non-authorization blocks may be
  referenced rather than expanded in full.
- **Write thin contractual prompts, not vague prompts.** Per
  `docs/00-meta/process/claude-code-context-management-standard.md`
  (Phase 4bm-A-P1), a phase prompt should be a thin execution
  contract: the phase identifier, tier, scope, allowed surface,
  validation, fail-closed conditions, and explicit non-scope.
  Repository docs carry the stable rules; the prompt carries the
  phase execution contract. Avoid embedding large extracts of prior
  phase reports, retained verdict ledgers, or governance text inside
  the prompt — cite them by repo path instead. Cite the relevant
  non-authorization blocks from
  `docs/00-meta/process/phase-risk-tiering-standard.md` §7 by name
  (N-ACQUISITION, N-ENDPOINT, N-CREDENTIALS, N-MANIFEST,
  N-GATE-RERUN, N-SUCCESSOR-STATE, N-DERIVATION,
  N-DIAGNOSTICS-ML-STRATEGY, N-PHASE-5, N-VERDICT-LOCK) rather than
  restating each prohibition in full, unless a phase-specific
  variation is required. A thin prompt is shorter, less likely to
  exhaust Claude Code's context window, and more auditable.
- **For heavy execution phases, include the lightweight Claude
  Code workspace fields.** Per
  `docs/00-meta/process/claude-code-lightweight-workspace-standard.md`
  (Phase 4bm-D-P1), heavy code / test / data / gate / kernel /
  long-validation phase prompts should state the Claude Code
  working directory (`C:\ClaudeRuns\prometheus-light`), the real
  Prometheus repository path (`C:\Prometheus`), and the command
  convention (`cd C:\Prometheus && <command>`) explicitly. These
  three fields are low-cost in prompt size, make the workspace
  assumption auditable, and pair with the thin-prompt discipline
  above to reduce hidden context pressure without weakening any
  repo authority. Small docs-only and short merge prompts may
  omit the fields; the standard's §11 "When to use the light
  workspace" rules govern.
- **Name exactly one phase.** Never bundle two phases. Never imply a
  successor.
- **Name exact allowed files.** List every tracked file Claude Code
  may create or modify. Anything not listed is forbidden.
- **Name exact forbidden activities.** ML, strategy, backtests,
  acquisition, paper / shadow / live, MCP, Graphify, credentials,
  manifest transitions, `.env` / `.mcp.json` creation, and any
  domain-specific forbidden activity should be enumerated.
- **Distinguish tracked from local gitignored.** If a phase produces
  local artefacts under `data/microstructure/`, list them explicitly
  as local gitignored outputs with the "not committed" requirement.
- **Forbid successor authorization.** Unless explicitly asked,
  Claude Code must not authorize the next phase. Prompts should state
  "no successor authorized."
- **Include validation commands.** Every prompt should specify the
  exact validation commands and the expected behaviour.
- **Include fail-closed conditions.** Every prompt should specify
  when Claude Code should stop and return `FAIL_CLOSED`.
- **Require a compact final response.** Use the 10-item final
  response format below.

## Required prompt sections

Every authorization prompt should include these sections in order:

1. **Repository** — name of the repo (Prometheus).
2. **Local path** — absolute local path (`C:\Prometheus`).
3. **Current task / authorized phase** — phase identifier and name.
4. **Phase type** — docs-only, code + docs, code + docs + local
   gitignored output, read-only QA, merge.
5. **Branch name** — exact branch name to create.
6. **Current known state** — `main` SHA, predecessor merge SHA,
   relevant artefacts that must exist or be preserved.
7. **Predecessor dependency** — explicit reference to the predecessor
   phase's merge-closeout that must be present in `main`.
8. **Purpose** — one paragraph describing what the phase does.
9. **Critical boundary** — one paragraph describing what the phase is
   not allowed to do.
10. **Strict non-scope** — enumerated list of forbidden activities.
11. **Allowed tracked files** — enumerated list of files Claude Code
    may create or modify.
12. **Allowed local gitignored outputs (if any)** — enumerated list of
    local paths Claude Code may produce, with the "not committed"
    requirement.
13. **Required outputs** — enumerated list of artefacts that must be
    produced for the phase to be branch-complete.
14. **Required evidence** — what evidence must appear in the report
    and closeout.
15. **Initial verification** — exact commands to run before any work,
    with explicit pass criteria.
16. **Validation commands** — exact commands to run after
    implementation, with explicit pass criteria.
17. **Expected validation behavior** — exact expected outputs.
18. **Commit instructions** — explicit `git add` paths (no `git add
    -A`), commit message format, HEREDOC trailer.
19. **Do-not-merge / merge instructions** — explicit instruction not
    to merge (for authorization prompts) or explicit merge method
    (for merge prompts).
20. **Fail-closed conditions** — enumerated conditions under which
    Claude Code must stop.
21. **Final Claude response format** — the 10-item format below.

## Docs-only phase template

```text
Execute **Phase {X} — {Phase Name}** for the Prometheus project at
`C:\Prometheus`.

This is docs-only / process standardization. No source/test/script/data
changes. No merge.

# Branch
`phase-{X}/{slug}` — create from current `main`.

# Hard rules (FAIL_CLOSED if violated)
- Do NOT modify source, tests, scripts, pyproject.toml, README.md,
  .gitignore, MCP files.
- Do NOT modify or commit anything under `data/microstructure/`.
- Do NOT modify label artefacts/manifest/sidecars.
- Do NOT create label gate report or successor-state.
- Do NOT change `research_eligible` / `eligibility_gate_status` /
  `chronological_split_policy`.
- Do NOT acquire data, train ML, run strategy, run backtests, call
  APIs, open WebSockets, use credentials, create `.env` / `.mcp.json`,
  enable MCP / Graphify.
- Do NOT revise retained verdicts or project locks; do NOT amend M0.
- Do NOT authorize any successor — process docs must explicitly state
  no successor is authorized.
- Do NOT merge in this phase.
- Do NOT use `git add -A`; always explicit paths.
- Do NOT use `--no-verify`. Do NOT push.

# Step 1 — Verification
{exact verification commands and pass criteria}

# Step 2 — Inspect prior style
{Read tool usage for style consistency}

# Step 3 — Write the N docs
{exact file paths and required sections}

# Step 4 — Narrow current-project-state update
{narrative paragraph addition + Current phase block update}

# Step 5 — Validation
{exact validation commands}

# Step 6 — Commit (single commit)
{exact `git add` paths, HEREDOC commit message with Co-Authored-By
trailer}

# Step 7 — Final response
{10-item final response format}
```

## Code + docs phase template

```text
Execute **Phase {X} — {Phase Name}** for the Prometheus project at
`C:\Prometheus`.

This is code + docs. Source/test additions allowed under the named
surface. No local data writes. No merge.

# Branch
`phase-{X}/{slug}` — create from current `main`.

# Hard rules (FAIL_CLOSED if violated)
- Allowed tracked source paths: {exact list}.
- Allowed tracked test paths: {exact list}.
- Allowed tracked doc paths: implementation report, closeout,
  current-project-state.md narrow update.
- Do NOT modify any other source / test / script.
- Do NOT modify or commit anything under `data/microstructure/`.
- Do NOT modify any prior manifest.
- Do NOT change `research_eligible` / `eligibility_gate_status` /
  `chronological_split_policy`.
- Do NOT acquire data, train ML, run strategy, run backtests, call
  APIs, open WebSockets, use credentials, create `.env` / `.mcp.json`,
  enable MCP / Graphify.
- Do NOT revise retained verdicts or project locks; do NOT amend M0.
- Do NOT authorize any successor.
- Do NOT merge.
- Do NOT use `git add -A`. Do NOT use `--no-verify`. Do NOT push.

# Step 1 — Verification
{verification commands}

# Step 2 — Implementation
{exact code surface and contract}

# Step 3 — Tests
{exact test surface}

# Step 4 — Reports
{implementation report and closeout}

# Step 5 — Narrow current-project-state update

# Step 6 — Validation
{ruff, mypy, scoped pytest, gitignore confirmation, git diff --check}

# Step 7 — Commit

# Step 8 — Final response
```

## Code + docs + local gitignored output phase template

```text
Execute **Phase {X} — {Phase Name}** for the Prometheus project at
`C:\Prometheus`.

This is code + docs + local gitignored output. Source/test/code under
the named surface; one local kernel run that produces gitignored
artefacts under `data/microstructure/...`. No merge.

# Branch
`phase-{X}/{slug}` — create from current `main`.

# Hard rules (FAIL_CLOSED if violated)
- Allowed tracked surface: {exact list of source / test / docs}.
- Allowed local gitignored outputs: {exact paths under
  data/microstructure/...}. These files must NOT be committed.
  `git check-ignore -v` must confirm gitignore coverage.
- Do NOT modify or commit anything under `data/microstructure/`
  beyond the allowed local outputs (and even those must remain
  gitignored).
- Do NOT modify any prior manifest or sidecar.
- Do NOT change `research_eligible` / `eligibility_gate_status` /
  `chronological_split_policy`.
- Do NOT create a label gate report or label successor-state unless
  explicitly authorized.
- Do NOT acquire data from any network source.
- Do NOT train ML, run strategy, run backtests.
- Do NOT call APIs, open WebSockets, use credentials, create `.env` /
  `.mcp.json`, enable MCP / Graphify.
- Do NOT revise retained verdicts or project locks; do NOT amend M0.
- Do NOT authorize any successor.
- Do NOT merge.
- Do NOT use `git add -A`. Do NOT use `--no-verify`. Do NOT push.

# Step 1 — Verification

# Step 2 — Implementation

# Step 3 — One-shot kernel run that produces local gitignored output

# Step 4 — Record local artefact paths, sizes, SHA256s in
implementation report; record "not committed" status

# Step 5 — Tests

# Step 6 — Reports

# Step 7 — Narrow current-project-state update

# Step 8 — Validation (must include `git check-ignore -v` confirmation
for every local output path)

# Step 9 — Commit (tracked files only)

# Step 10 — Final response
```

## Read-only QA phase template

```text
Execute **Phase {X} — {Phase Name}** for the Prometheus project at
`C:\Prometheus`.

This is read-only QA + docs. No source/test/script/data changes. No
merge.

# Branch
`phase-{X}/{slug}` — create from current `main`.

# Hard rules (FAIL_CLOSED if violated)
- Do NOT modify any source / test / script / config / data / manifest.
- Do NOT modify or commit anything under `data/microstructure/`.
- Do NOT modify any sidecar.
- Do NOT change `research_eligible` / `eligibility_gate_status` /
  `chronological_split_policy`.
- Do NOT create any gate report or successor-state.
- Do NOT acquire data, train ML, run strategy, run backtests, call
  APIs, open WebSockets, use credentials, create `.env` / `.mcp.json`,
  enable MCP / Graphify.
- Do NOT revise retained verdicts or project locks; do NOT amend M0.
- Do NOT authorize any successor.
- Do NOT merge.
- Do NOT use `git add -A`. Do NOT use `--no-verify`. Do NOT push.

# Step 1 — Verification

# Step 2 — Read artefacts (read-only)

# Step 3 — Record evidence in implementation report (paths, sizes,
SHA256s)

# Step 4 — Confirm pre/post SHA preservation (no mutation)

# Step 5 — Reports (implementation report + closeout)

# Step 6 — Narrow current-project-state update

# Step 7 — Validation

# Step 8 — Commit (docs only)

# Step 9 — Final response
```

## Merge prompt template

```text
Merge **Phase {X} — {Phase Name}** into `main` for the Prometheus
project at `C:\Prometheus`.

# Source branch
`phase-{X}/{slug}`

# Target branch
`main`

# Merge method
`git merge --no-ff` with `ort` strategy.

Merge commit message:
`docs(phase-{X}): merge {short description}`

# Hard rules (FAIL_CLOSED if violated)
- Do NOT skip hooks (--no-verify).
- Do NOT skip signing.
- Do NOT force-push.
- Do NOT modify the branch contents during merge.
- Do NOT authorize any successor in the merge-closeout.

# Step 1 — Verification
- `git rev-parse main == git rev-parse origin/main`
- branch is reviewed
- branch has implementation report and closeout
- no `data/microstructure/` files are staged

# Step 2 — Merge

# Step 3 — Write merge-closeout per `merge-closeout-standard.md`

# Step 4 — Commit merge-closeout on `main`

# Step 5 — Push to `origin/main`

# Step 6 — Record final `main` / `origin/main` SHA in merge-closeout

# Step 7 — Final response
```

## Fail-closed conditions library

Common fail-closed conditions to include in prompts:

- `git rev-parse main != git rev-parse origin/main`.
- predecessor merge commit not an ancestor of `main`.
- predecessor merge-closeout file missing.
- required local artefact missing or SHA256 mismatch.
- gitignore coverage missing for a required local path.
- a `data/microstructure/` file appears in `git status` as staged or
  modified outside the allowed surface.
- a forbidden tracked file appears in `git status`.
- ruff fails.
- mypy fails.
- scoped pytest fails.
- a forbidden activity is implied by the prompt and cannot be
  declined.
- ambiguity in scope and the prompt does not allow pausing.

## Validation command library

Common validation commands and expected behaviour:

- `git diff --stat` — should match expected file change set.
- `git diff --name-only` — exact list of changed files.
- `ruff check .` — should pass (or scoped variant).
- `mypy src` — should pass (or scoped variant).
- `pytest tests/research/microstructure/` — should pass (744 passed
  post-Phase 4bj-D).
- `git diff --check` — clean (no whitespace errors).
- `git check-ignore -v data/microstructure/` — `.gitignore:85`.
- `git check-ignore -v data/microstructure/labels/` —
  `.gitignore:85`.
- `git check-ignore -v data/microstructure/manifests/` —
  `.gitignore:85`.
- `git status` — only expected staged / changed files.
- `git log --oneline -8` — recent history.

## Commit instruction library

- **Always use explicit `git add` paths.** Never `git add -A`,
  `git add .`, `git add -u`.
- **Always use HEREDOC for commit messages.** Include the
  `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` trailer.
- **Never use `--no-verify`.** Never use `--no-gpg-sign`. Never use
  `-c commit.gpgsign=false`.
- **Never amend** unless explicitly asked. If a hook fails, fix the
  issue, re-stage, and create a NEW commit.
- **Never force-push.** Never push to `main` outside the merge-prompt
  flow.

## Final Claude response format

Every Claude Code phase response must end with exactly this 10-item
format:

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

## Non-scope wording library

Standard non-scope phrases to include in prompts:

- "Do NOT modify any source / test / script / config."
- "Do NOT modify or commit anything under `data/microstructure/`."
- "Do NOT modify any manifest or sidecar."
- "Do NOT change `research_eligible` / `eligibility_gate_status` /
  `chronological_split_policy`."
- "Do NOT create any gate report or successor-state."
- "Do NOT acquire data, train ML, run strategy, run backtests."
- "Do NOT call APIs, open WebSockets, use credentials."
- "Do NOT create `.env` or `.mcp.json`."
- "Do NOT enable MCP or Graphify."
- "Do NOT revise retained verdicts or project locks."
- "Do NOT amend M0."
- "Do NOT authorize any successor."
- "Do NOT merge in this phase."

## Local artefact wording library

For phases that produce local gitignored outputs:

- "Allowed local gitignored outputs: {exact paths}."
- "These files must NOT be committed."
- "`git check-ignore -v` must confirm gitignore coverage for every
  path."
- "Record paths, sizes, and SHA256s in the implementation report."
- "Record paths, sizes, and SHA256s in the closeout."
- "Record the 'not committed' status explicitly."
- "Preserve all prior local artefacts bit-for-bit (record pre/post
  SHA256 if applicable)."

## Successor authorization wording

For every phase prompt:

- "This phase does NOT authorize any successor."
- "The implementation report and closeout must explicitly state
  that no successor is authorized."
- "Recommended state at end of phase: remain paused unless operator
  separately authorizes."

For merge prompts:

- "The merge-closeout must explicitly state no successor is
  authorized."
- "The merge-closeout must list every phase that is **not**
  authorized."

## Examples / skeletons

A skeleton authorization prompt for a hypothetical docs-only memo:

```text
Execute **Phase 4bk-B — {hypothetical}** for the Prometheus project at
`C:\Prometheus`.

This is docs-only. No source/test/script/data changes. No merge.

Branch: `phase-4bk-b/{slug}` — create from current `main`.

Hard rules: {non-scope library entries}.

Step 1 — Verification: ...
Step 2 — Inspect prior style: ...
Step 3 — Write the memo: ...
Step 4 — Narrow current-project-state update: ...
Step 5 — Validation: ...
Step 6 — Commit (single commit): ...
Step 7 — Final response: {10-item format}.
```

A skeleton merge prompt:

```text
Merge **Phase 4bk-A — Phase Workflow / Prompt / Report
Standardization** into `main` for the Prometheus project at
`C:\Prometheus`.

Source: `phase-4bk-a/phase-workflow-prompt-report-standardization`.
Target: `main`.
Method: `git merge --no-ff`.
Commit message: `docs(phase-4bk-a): merge phase workflow standards`.
Hard rules: {merge-prompt non-scope entries}.

Step 1 — Verification: ...
Step 2 — Merge: ...
Step 3 — Write merge-closeout per
`merge-closeout-standard.md`: ...
Step 4 — Commit merge-closeout on `main`: ...
Step 5 — Push to `origin/main`: ...
Step 6 — Record final `main` / `origin/main` SHA: ...
Step 7 — Final response: {10-item format}.
```

This template is process-only. It does not authorize any phase. It
does not authorize Phase 4bj-E. It does not authorize label-family
eligibility gate implementation, ML, strategy, backtests, acquisition,
paper / shadow / live, MCP, Graphify, credentials, exchange-write, or
production keys.
