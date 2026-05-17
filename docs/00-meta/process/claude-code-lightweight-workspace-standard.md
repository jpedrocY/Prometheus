# Claude Code Lightweight Workspace Standard

## Title

Prometheus Claude Code Lightweight Workspace Standard — lightweight
launcher workspace pattern for heavy Prometheus Claude Code execution
sessions; standard launch command; IDE / Antigravity posture; default
agent and memory policy; optional local hooks posture; session slicing;
prompt format under the light workspace; when-to-use guidance; default-
deny MCP / Graphify reaffirmed.

## 1. Purpose

Prometheus phases are executed inside Claude Code sessions whose
context window is a finite resource. Phase 4bm-A-P1 established the
operational layer of context discipline by requiring **thin
contractual prompts** that reference repo-resident standards rather
than restate them. Phase 4bm-D exposed a second, complementary risk
that thin prompts alone cannot solve.

Heavy Prometheus implementation phases — phases that touch source
code, tests, large data artefacts, or multi-day gate / kernel /
validation work — can fail operationally when the Claude Code session
is launched directly from the working directory of the Prometheus
repository. The repository carries large governance documents
(`docs/00-meta/current-project-state.md` has grown past 23,000 lines
as the project record has accumulated), a deep `docs/00-meta/process/`
process layer, a deep `docs/00-meta/implementation-reports/` history,
and large source / test / data trees. When Claude Code is launched
from inside that working directory, the harness auto-loads project
context (project memory, repo-resident `CLAUDE.md`-style content,
workspace metadata, and similar surfaces) before the operator's prompt
runs. On heavy phases this auto-loaded context can dominate the
context window, trigger repeated auto-compact loops, and cause
extreme per-tool-call token consumption that prevents the phase from
completing within the operator's bounded sessions.

Phase 4bm-D recovered from this failure mode operationally by running
Claude Code from a **lightweight launcher workspace** at
`C:\ClaudeRuns\prometheus-light` while accessing the real repository
explicitly at `C:\Prometheus`. The light workspace contains no
governance documents, no source code, no tests, and no data — only
the operator's prompt and local session tooling — so the Claude Code
harness does not auto-load anything heavy at session start. The
operator's prompt, the chat-branching handoff, the explicit `cd
C:\Prometheus && <command>` discipline, and targeted repo reads then
do the work that auto-loaded context would otherwise have done, but
under bounded operator control.

This standard formalises that lightweight workspace pattern as the
recommended default for heavy Prometheus Claude Code execution
sessions. It complements, but does not replace,
`docs/00-meta/process/claude-code-context-management-standard.md`
(Phase 4bm-A-P1). The Phase 4bm-A-P1 standard governs **what goes
into the prompt and what gets read**; this standard governs **where
the Claude Code session is launched from and what auto-context it
inherits**. Together they reduce hidden context pressure without
weakening any repo authority, validation, phase lifecycle, or
non-authorization discipline.

This standard is **prospective only**. It does not rewrite prior
phase history. Prior phases that ran directly from `C:\Prometheus`
remain valid as recorded. Phase 4bm-D's lightweight-workspace
recovery is the precedent that motivates this standard; the
precedent itself is preserved as recorded in the Phase 4bm-D
implementation report and merge-closeout.

## 2. Authority

This document is **process-only**. It does not revise any retained
verdict, project lock, M0 governance, manifest state, label
artefact, gate protocol, canonical path policy, strategy decision,
or successor authorization. Where this standard conflicts with a
specialist domain document on technical content, the specialist
document wins. Where this standard conflicts with another process
file on lifecycle, prompt design, report shape, merge-closeout
structure, or chat handoff content, the domain-specific process
file wins for its own surface
(`phase-workflow-standard.md`, `phase-prompt-template.md`,
`operator-report-standard.md`, `merge-closeout-standard.md`,
`chat-branching-handoff-standard.md`, `phase-risk-tiering-standard.md`,
`claude-code-context-management-standard.md`).

This standard does not authorize any successor phase. It does not
authorize Phase 4bm-E. It does not authorize Phase 4bm-F. It does
not authorize features, labels, diagnostics, ML, strategy,
backtests, acquisition, endpoint calls, paper / shadow,
live-readiness, deployment, exchange-write, production keys,
authenticated APIs, private endpoints, user stream, MCP, Graphify,
`.mcp.json`, or credentials. It does not enable any new tooling.

## 3. Core principle

**Heavy execution sessions should start from a lightweight Claude
Code workspace.**

- The real Prometheus repository remains the authoritative target.
  Every tracked file the phase writes lands in `C:\Prometheus`; every
  validation gate runs against `C:\Prometheus`; every artefact SHA
  is computed against `C:\Prometheus`; every merge happens inside
  `C:\Prometheus`.
- Repo docs remain authoritative. The new standard does not weaken
  the mandatory-read policy in
  `docs/00-meta/process/claude-code-context-management-standard.md`
  §6. Repo docs are still binding; they are simply **read
  explicitly and narrowly** by Claude Code rather than auto-loaded
  in bulk by the harness at session start.
- The light workspace is an **execution shell**, not a replacement
  repository. It carries operator prompts, optional local session
  tooling, and the small amount of state needed to launch Claude
  Code with a clean auto-context surface. It does not host a copy
  of `src/`, `tests/`, `data/`, governance memos, or the
  implementation-report history.
- Thin contractual prompts (Phase 4bm-A-P1) remain mandatory.
  Lightweight workspace launch is a complementary discipline, not a
  substitute for prompt discipline.

A heavy execution session that is launched from the light workspace
but uses an oversized prompt is no safer than one launched directly
from the repo. Both disciplines apply together.

## 4. Standard workspace layout

The standard defines two distinct directories on the operator's
machine:

| Role | Path | Contents |
| ---- | ---- | -------- |
| Lightweight Claude Code workspace | `C:\ClaudeRuns\prometheus-light` | Operator prompts, optional local hook scripts, optional local session tooling. No source, tests, data, or governance memos. |
| Real Prometheus repository | `C:\Prometheus` | The authoritative repository: `src/`, `tests/`, `scripts/`, `docs/`, `data/`, `pyproject.toml`, `.gitignore`, every tracked file, every committed history. |

All repository commands should use:

```text
cd C:\Prometheus && <command>
```

This convention applies to every `git`, `ruff`, `mypy`, `pytest`,
`uv run`, `python`, and similar command issued by Claude Code during
a heavy execution session, regardless of which directory the Claude
Code harness was launched from. The convention exists so that
commands operate on the authoritative repository tree, not on the
light workspace.

Claude Code should be launched from the lightweight workspace
(`C:\ClaudeRuns\prometheus-light`). The real repository should be
provided as an explicitly added directory or accessed by absolute
path. The exact mechanism is recorded under §5; the principle is
that the Claude Code harness sees the light workspace as the
working directory and `C:\Prometheus` as an explicit, opt-in
secondary location.

The light workspace must **not** contain a copy of the Prometheus
source tree, the Prometheus test tree, the Prometheus data tree,
the Prometheus governance memos, the Prometheus implementation-
report history, or the Prometheus agent packs / agent memory.
Copying any of those into the light workspace would defeat the
purpose of the standard: the light workspace would once again
auto-load heavy content at session start.

## 5. Recommended launch command

The recommended operator launch pattern for a heavy Prometheus
execution session is:

```powershell
cd C:\ClaudeRuns\prometheus-light

$env:CLAUDE_CODE_DISABLE_CLAUDE_MDS="1"
$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY="1"

claude --add-dir C:\Prometheus
```

Notes on this pattern:

- The two `$env:` assignments are **session-local** to the current
  PowerShell process. They do not modify the operator's user
  profile, do not modify any global environment, and do not affect
  other Claude Code sessions or other projects launched in
  different shells.
- The two environment variables are intended for heavy Prometheus
  execution sessions. They reduce the Claude Code harness's
  auto-loading of project memory / CLAUDE.md files at session
  start. They do not weaken any repo standard: the operator's
  prompt and the mandatory-read policy in
  `docs/00-meta/process/claude-code-context-management-standard.md`
  §6 still apply.
- `--add-dir C:\Prometheus` exposes the real repository to the
  Claude Code session as an explicitly added directory, so that
  tools (Read, Edit, Grep, Glob, Write, Bash) can target files
  inside `C:\Prometheus` without making it the harness's working
  directory and without inheriting its full auto-context.
- The exact CLI surface and environment variable names may evolve
  with the Claude Code product. The principle — launch from the
  light workspace, expose the real repository explicitly, and
  suppress auto-loading of heavy project context — is what is
  binding. Operators may adapt the exact incantation if the
  product's surface changes, provided the principle is preserved.

## 6. IDE / Antigravity guidance

For heavy Prometheus code / test / data / gate / kernel /
validation phases, the Claude Code agent should not be launched
from an IDE workspace rooted at `C:\Prometheus`.

- If the operator uses Antigravity, VS Code, or another IDE to run
  the Claude Code agent, the IDE workspace should be opened at
  `C:\ClaudeRuns\prometheus-light`. The Claude Code agent then
  inherits the light workspace as its working directory rather
  than the full Prometheus repo.
- The real repository at `C:\Prometheus` is accessed explicitly
  through commands (`cd C:\Prometheus && <command>`) and through
  absolute file paths (`C:\Prometheus\src\...`,
  `C:\Prometheus\tests\...`, `C:\Prometheus\docs\00-meta\...`).
- The IDE may still be used as a normal editor / viewer for files
  under `C:\Prometheus`. The standard does not require the
  operator to give up IDE-side editing of the real repository.
  What the standard discourages is launching the **Claude Code
  agent itself** from an IDE workspace rooted at the heavy repo,
  because the agent then inherits the IDE's auto-context surface.

The principle is the same as in §5: the Claude Code agent's
working-directory context should be light; the real repository
should be reached explicitly.

## 7. Agent and memory policy

By default, **Prometheus agents and project memory should not be
auto-loaded** in a lightweight execution session.

Heavy execution sessions should rely on:

- the operator authorization prompt (per
  `docs/00-meta/process/phase-prompt-template.md` and the thin-
  prompt rules in
  `docs/00-meta/process/claude-code-context-management-standard.md`
  §4);
- the chat-branching handoff (per
  `docs/00-meta/process/chat-branching-handoff-standard.md`), if
  the phase is continuing in a new chat;
- targeted repo doc reads (per the mandatory-read policy in
  `docs/00-meta/process/claude-code-context-management-standard.md`
  §6);
- targeted file reads (`Read`, `Glob`, `Grep`) into
  `C:\Prometheus`;
- explicit validation commands (per
  `docs/00-meta/process/phase-prompt-template.md`'s validation
  command library).

Agents may be considered only through a separately authorized,
bounded process decision. This standard does **not** authorize the
introduction of agent packs into the light workspace, does **not**
authorize copying Prometheus agent memory into
`C:\ClaudeRuns\prometheus-light`, and does **not** authorize any
agent-driven autonomous workflow. Any future change to this
posture would require a separately authorized Tier 1 governance
phase that scopes the change, the agent inventory, the failure
mode, the rollback, and the audit trail.

The reason for the default-off agent posture is the same as the
reason for the light-workspace pattern itself: auto-loaded agent
packs and auto-loaded agent memory consume context at session
start. Heavy Prometheus phases need the context budget for the
operator prompt, the targeted reads, and the validation work.

## 8. Hooks and local guardrails

Optional **local** hooks may be used for:

- compact-recovery behavior (a hook that helps the operator
  recover after a Claude Code auto-compact event);
- pre-compact stop / checkpoint behavior (a hook that allows the
  operator to capture state before a compact, or to stop the
  session in favour of a fresh-session restart);
- read-budget guards (a hook that warns when accumulated reads
  exceed a threshold);
- general local session discipline.

The following rules govern hooks under this standard:

- Hook files and the settings that configure them
  (`settings.json`, `settings.local.json`, `hooks/*.ps1`,
  `hooks/*.sh`, similar) are **local operator tooling** unless a
  separately authorized process phase explicitly authorizes their
  inclusion in the repository. Local hook files may live under the
  light workspace (`C:\ClaudeRuns\prometheus-light\.claude\...`)
  without being committed.
- Local hook files **should not** be committed to `C:\Prometheus`
  unless a separately authorized process phase explicitly
  authorizes project-wide hook standardization. Authorising hooks
  for repo inclusion is not within the scope of this standard.
- The standard does **not** require hooks for normal operation.
  The primary fix is the light workspace itself: launching Claude
  Code from a directory with no auto-loaded heavy content is what
  reduces context pressure. Hooks are an optional second layer of
  local discipline.
- Local hooks must not weaken any repo guarantee. A hook that
  bypasses validation, skips commit hooks, force-pushes, or
  silently mutates `C:\Prometheus` artefacts is out of scope and
  must not be used. The Phase 4bk-A `--no-verify` /
  `--no-gpg-sign` / no-force-push rules in
  `phase-workflow-standard.md` and `merge-closeout-standard.md`
  remain binding regardless of whether a local hook is active.

## 9. Session slicing

Large implementation phases may use **multiple bounded Claude Code
sessions** within the same repo phase.

Each bounded session should have:

- one concrete task (e.g. "implement module X and its unit tests",
  "wire the orchestrator and end-to-end tests", "run the
  authoritative gate against real artefacts", "write the
  implementation report and closeout");
- a short checkpoint / handoff for the next session (per
  `chat-branching-handoff-standard.md` if the next session is in a
  new chat; per an in-chat checkpoint note otherwise);
- a narrow allowed file surface, named explicitly per the allowed-
  surface discipline in
  `docs/00-meta/process/claude-code-context-management-standard.md`
  §8;
- explicit validation appropriate to the slice (e.g. scoped
  `pytest`, `ruff`, `mypy` for an implementation slice; `git diff
  --check` and gitignore confirmation for a docs / artefact-
  recording slice);
- stop / report behavior at the end of the slice (the slice ends
  with a compact report; the operator decides whether to continue
  in the same session, start a fresh session, or stop entirely).

Session slicing does **not** create new repo phases by itself. The
repo phase is a single unit defined by its authorization prompt
and its eventual merge-closeout. Bounded sessions are **execution
hygiene inside the existing phase lifecycle**: they let the
operator move a long phase through several manageable Claude Code
sessions without exceeding any single session's effective context
budget. The implementation report and merge-closeout still record
the phase as one unit per `merge-closeout-standard.md`.

A bounded session that hits a fail-closed condition (per
`phase-workflow-standard.md` "When to fail closed") must still
fail closed. Session slicing does not relax the fail-closed rule;
it merely allows recoverable, well-scoped slices to proceed
without one giant Claude Code session.

## 10. Prompt format under light workspace

Future authorization prompts for heavy phases should include the
following fields explicitly, in addition to the Phase 4bm-A-P1
thin-prompt requirements
(`docs/00-meta/process/claude-code-context-management-standard.md`
§4) and the canonical structure in
`docs/00-meta/process/phase-prompt-template.md`:

- **Claude Code working directory.** State explicitly:
  "`C:\ClaudeRuns\prometheus-light`."
- **Real repository path.** State explicitly:
  "`C:\Prometheus`."
- **Command convention.** State explicitly:
  "For every shell command, use `cd C:\Prometheus && <command>`."
- **Current phase.** Exact phase identifier and name.
- **Branch.** Exact branch name to create or operate on.
- **Latest completed phase.** Exact predecessor phase identifier
  and merge-closeout SHA reference.
- **Allowed files.** Enumerate every tracked file Claude Code may
  create or modify (per
  `claude-code-context-management-standard.md` §8).
- **Forbidden surfaces.** Enumerate forbidden tracked surfaces,
  forbidden local surfaces, and any phase-specific forbidden
  activities not covered by the reusable non-authorization blocks.
- **Mandatory docs.** The default mandatory read list per
  `claude-code-context-management-standard.md` §6, plus any
  immediately relevant predecessor implementation report or
  merge-closeout.
- **Optional read / search rule.** Reaffirm the
  `claude-code-context-management-standard.md` §6 rule: older
  reports are read only when a SHA, path, policy, gate rule, or
  precedent is missing; `Grep` / `Glob` are preferred over reading
  many full documents.
- **Stop condition.** State explicitly that Claude Code stops
  after the named work, that no merge is part of the phase unless
  the prompt is a merge prompt, and that no successor is
  authorized.

The first three fields (working directory, real repo path,
command convention) are the addition introduced by this standard.
They make the light-workspace pattern part of the prompt contract
rather than an unwritten operator habit. They cost very little
prompt size and are highly auditable: a future reviewer can read
the prompt and immediately see which workspace was assumed.

## 11. When to use the light workspace

**Use the light workspace by default for:**

- code-heavy phases (any phase that adds or modifies non-trivial
  source code under `src/`);
- test-heavy phases (any phase that adds or modifies non-trivial
  tests under `tests/`);
- data / gate execution phases (any phase that runs a gate
  kernel, a normalization kernel, a feature kernel, a label
  kernel, or any other batch operation that touches large local
  artefacts under `data/microstructure/`);
- long validation phases (any phase whose validation contract
  includes large `pytest` suites, whole-repo `ruff` / `mypy`, or
  multi-step artefact validation);
- phases with large source / test files in their allowed surface
  (e.g. a phase that ships a 1,000+ line module and its
  corresponding test suite);
- phases that previously triggered auto-compact / context
  warnings on a comparable workload (a phase whose ceremony
  pattern mirrors a phase that needed light-workspace recovery).

**Optional for:**

- small docs-only phases (one or two short tracked files; minimal
  reads);
- short merge phases (the merge phase is a small, well-bounded
  unit; light workspace is helpful but not required);
- very narrow admin / Tier 4 fixes (a typo correction or SHA-
  placeholder fixup).

**Avoid using direct `C:\Prometheus` as the Claude Code workspace
if any of the following appear during launch:**

- startup warns about large memory / docs being loaded;
- auto-compact triggers immediately after the operator prompt is
  submitted;
- Claude Code repeatedly rereads context after compacting;
- the harness auto-loads `docs/00-meta/current-project-state.md`
  or other large governance docs without an operator request;
- per-tool-call token consumption rises sharply at session start.

When any of these symptoms appear, the correct response is to
restart the session from the light workspace per §5 and to keep
the operator prompt thin per
`claude-code-context-management-standard.md` §4. Adding tooling
(MCP, Graphify, new agent packs) is **not** the correct response;
the project's default-deny posture on those tools is preserved
verbatim (see §13).

## 12. Relationship to existing process docs

This standard sits inside the existing Prometheus process layer
and does not amend any prior process document beyond the narrow
cross-references introduced by Phase 4bm-D-P1.

- **Phase 4bm-A-P1
  (`claude-code-context-management-standard.md`)** established
  that repo docs carry stable rules and that prompts carry the
  phase execution contract. Phase 4bm-D-P1 extends that principle
  by defining **where heavy Claude Code execution should be
  launched from**. Phase 4bm-A-P1 governs prompt and read
  discipline; Phase 4bm-D-P1 governs workspace and harness
  auto-context discipline. Both apply together to heavy phases.
- **Phase 4bl-F
  (`phase-risk-tiering-standard.md`)** four-tier risk model
  remains unchanged. Light-workspace launch is independent of
  tier: a Tier 1 multi-day code phase benefits the most; a
  Tier 4 typo fix benefits least.
- **Phase 4bk-A
  (`phase-workflow-standard.md`)** master lifecycle remains
  unchanged. The eleven-step lifecycle, the project-complete
  rule, the merge-closeout requirement, and the fail-closed
  rules are all unaffected by where the Claude Code session is
  launched from.
- **Merge-closeout requirements
  (`merge-closeout-standard.md`)** remain unchanged. The 16
  required sections, the SHA recording standard, the merge
  method, and the successor-authorization standard are all
  preserved verbatim.
- **Operator-report requirements
  (`operator-report-standard.md`)** remain unchanged. Claude
  Code's 10-item compact report format, ChatGPT's plain-English
  response templates, and the role split are preserved verbatim.
- **Chat-branching handoff
  (`chat-branching-handoff-standard.md`)** remains unchanged in
  substance. The handoff structure is unchanged; this standard
  only adds the recommendation that handoff continuation prompts
  for heavy phases include the workspace / repo-path /
  command-convention fields defined in §10.
- **Phase prompt template
  (`phase-prompt-template.md`)** structure is unchanged. The
  cross-reference added by Phase 4bm-D-P1 simply points future
  authors at this standard for heavy execution phases.

This standard preserves every retained verdict and every project
lock verbatim. It does not amend M0, the Phase 4al refined
no-rescue rule, the Phase 4aw `flip_research_eligible(...)`
always-raises invariant, the Phase 4bb-F canonical path policy,
the Phase 4bl-F R-SIDECAR-CRLF standing rule, or any nine of the
reusable non-authorization blocks (`N-ACQUISITION`,
`N-ENDPOINT`, `N-CREDENTIALS`, `N-MANIFEST`, `N-GATE-RERUN`,
`N-SUCCESSOR-STATE`, `N-DERIVATION`,
`N-DIAGNOSTICS-ML-STRATEGY`, `N-PHASE-5`, `N-VERDICT-LOCK`).

## 13. Non-authorizations

Phase 4bm-D-P1 (this standard) explicitly does **NOT** authorize:

- MCP enablement of any kind;
- Graphify enablement of any kind;
- `.mcp.json` creation or reading;
- credentials of any kind;
- exchange-write surfaces;
- paper / shadow / live;
- additional data acquisition (additional aggTrades / 5m / 1m /
  tick / mark-price 30m / 4h / order-book / spot / cross-venue /
  funding / open-interest);
- public-endpoint calls in code;
- authenticated APIs;
- private endpoints;
- WebSockets;
- user streams;
- agents by default;
- copying Prometheus agent packs into the light workspace;
- copying Prometheus agent memory into the light workspace;
- modifications to retained verdicts (H0, R3, R1a, R1b-narrow,
  R2, F1, D1-A, V2, G1, C1, 5m thread closure);
- modifications to project locks (§11.6, round-trip, §1.7.3,
  Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 /
  §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v,
  Phase 4w, Phase 4ak M0 twelve-clause gate + post-null
  cooldown + cooled-down families list + memo template, Phase
  4al refined no-rescue rule + §13 boundary + §14 hierarchy,
  Phase 4aw `flip_research_eligible(...)` always-raises
  invariant, Phase 4bb-F canonical path policy, Phase 4bl-F
  four-tier risk model + R-SIDECAR-CRLF standing rule + nine
  reusable non-authorization blocks);
- modifications to any manifest;
- flipping `research_eligible` on any actual manifest;
- transitioning `eligibility_gate_status` on any actual
  manifest;
- changing `chronological_split_policy` on any actual manifest;
- deployment;
- production-key creation;
- Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility
  Decision Memo);
- Phase 4bm-F (Multi-Day Derived-Family Successor-State
  Recording);
- any other successor phase whatsoever.

The recommended state after Phase 4bm-D-P1 remains **remain
paused**. Phase 4bm-D remains project-complete on `main` and is
not amended by this standard.

## 14. Required references for future chats

A future chat that uses this standard must also reference:

- `docs/00-meta/process/phase-workflow-standard.md` — master
  phase lifecycle manual;
- `docs/00-meta/process/phase-risk-tiering-standard.md` — phase
  risk tiers, R-SIDECAR-CRLF standing rule, reusable non-
  authorization blocks;
- `docs/00-meta/process/claude-code-context-management-standard.md`
  (Phase 4bm-A-P1) — thin contractual Claude Code prompts,
  mandatory vs optional read policy, session management, soft
  size guidance, and default-deny MCP / Graphify posture;
- `docs/00-meta/process/phase-prompt-template.md` —
  authorization prompt structure (long-form);
- `docs/00-meta/process/operator-report-standard.md` — Claude
  Code compact report and ChatGPT operator-facing response
  shape;
- `docs/00-meta/process/merge-closeout-standard.md` — merge-
  closeout structure;
- `docs/00-meta/process/chat-branching-handoff-standard.md` —
  chat-branching handoff structure;
- `docs/00-meta/current-project-state.md` — current project
  state;
- the most recent merge-closeout under
  `docs/00-meta/implementation-reports/`;
- the most recent phase implementation report.

## 15. Change-control process for this standard

This standard may be updated only by:

- a separately authorized docs-only Tier 1 process phase that
  names this file in its allowed tracked files;
- with a corresponding implementation report and closeout;
- merged into `main` with a merge-closeout per
  `merge-closeout-standard.md`;
- and a narrow `current-project-state.md` paragraph addition.

Updating this standard does not transition any technical state.
Updating it does not authorize any successor phase, does not
modify any manifest, does not enable ML / strategy / backtests,
and does not imply readiness for paper / shadow / live /
deployment / exchange-write.

## 16. Final note

The Prometheus project's evidentiary discipline is its competitive
advantage. This standard does not relax that discipline. It moves
the operational cost of governance — the cost of keeping Claude
Code sessions running long enough to complete heavy phases —
from "let the harness auto-load everything" to "launch from a
light workspace and read repo docs explicitly". Repo docs remain
authoritative; thin prompts remain mandatory; tier-appropriate
ceremony remains binding; merge-closeouts remain the only marker
of project-complete; no successor is implied.

Heavy execution sessions should start from `C:\ClaudeRuns\prometheus-light`,
access `C:\Prometheus` explicitly through `cd C:\Prometheus && <command>`,
suppress auto-loading of project memory / CLAUDE.md content, default
agents and memory to off, and rely on the operator prompt plus
targeted repo doc reads for context. Lightweight workspace launch is
the recommended default for heavy Prometheus Claude Code execution
sessions from Phase 4bm-D-P1 forward.
