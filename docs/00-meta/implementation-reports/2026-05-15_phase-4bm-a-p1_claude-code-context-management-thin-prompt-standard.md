# Phase 4bm-A-P1 — Claude Code Context Management / Thin Prompt Standard

## 1. Phase identity

- **Phase:** Phase 4bm-A-P1 — Claude Code Context Management / Thin
  Prompt Standard.
- **Tier:** Tier 1 (Full Phase) per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3. Process /
  governance standardization. New prospective standard governing
  Claude Code prompt design and session management.
- **Type:** Docs-only.
- **Branch:** `phase-4bm-a-p1/claude-code-context-management-thin-prompt-standard`.
- **Base `main` SHA at branch creation:**
  `e6b510cfb54b0720a19ec1bb52490079e5780ca4` (Phase 4bm-A merge-closeout
  commit; the canonical Phase 4bm-A project-complete anchor).
- **Predecessor phase on `main`:** Phase 4bm-A — Multi-Day Normalization
  Design Memo (docs-only design memo). Phase 4bm-A is project-complete;
  see `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a_merge-closeout.md`.

## 2. Pre-state

Phase 4bm-A is project-complete on `main`. `git rev-parse main ==
git rev-parse origin/main` at branch creation: both equal
`e6b510cfb54b0720a19ec1bb52490079e5780ca4`. The repository contains
the four pre-existing process standards (`phase-workflow-standard.md`,
`phase-risk-tiering-standard.md`, `phase-prompt-template.md`,
`operator-report-standard.md`, `merge-closeout-standard.md`,
`chat-branching-handoff-standard.md`) plus the most recent merge-
closeout for Phase 4bm-A. No prior Claude Code context management or
thin-prompt standard exists in the repository.

The pre-existing standards collectively cover: phase lifecycle
(`phase-workflow-standard.md`); ceremony per risk tier and reusable
non-authorization blocks (`phase-risk-tiering-standard.md`);
authorization-prompt structure (`phase-prompt-template.md`); compact
Claude Code report and operator-facing ChatGPT response shape
(`operator-report-standard.md`); 16-section merge-closeout structure
(`merge-closeout-standard.md`); and chat-branching handoff structure
(`chat-branching-handoff-standard.md`). What they do not yet cover is
the operational reality that Claude Code authorization prompts have
been growing long enough to risk exhausting Claude Code's context
window and triggering auto-compact loops mid-phase.

The Phase 4bm-A authorization prompt itself is the immediate evidence
of this problem. Phase 4bm-A was a docs-only design memo, the kind of
phase that should have a thin contractual prompt, yet the authorization
prompt was large enough that Claude Code reported context pressure
during execution. Phase 4bm-A succeeded, but the cost-of-execution
signal is clear: future Tier 1 phases of similar shape will compound
the problem unless prompt discipline changes.

## 3. Problem statement

**Claude Code's context window is a finite resource, and prompt size
directly competes with the room Claude Code needs to read the repo,
inspect existing artefacts, write the authorized files, and run
validation.**

The two failure modes that motivate this standard:

- **Context-window exhaustion mid-phase.** When the authorization
  prompt is very long, Claude Code can run out of headroom while
  performing the authorized work, particularly during phases that
  require reading several existing files and writing several new
  ones. The result is degraded output quality, missed steps, and in
  the worst case, auto-compacted summarization loops that lose
  precision.
- **Auto-compact summarization loops.** When the conversation grows
  past Claude Code's context budget, the runtime compacts prior
  turns into a summary and re-feeds that summary. Each round of
  compaction loses fidelity. A prompt that embedded large extracts of
  prior phase reports, retained verdict ledgers, or governance text
  is the worst-case input for this loop: the most important rules
  end up summarized, paraphrased, or dropped, while the surrounding
  history is preserved.

The root cause is not Claude Code's context window. The root cause is
that authorization prompts have been treating themselves as substitute
documentation — embedding the binding rules instead of citing them.
That conflates two roles. The repository holds stable rules. The
prompt holds the phase execution contract. When the prompt re-embeds
stable rules, every phase pays for the embedding, even though the
rules are already in `main` where Claude Code can read them.

The fix is structural: thin contractual prompts that cite the
repository instead of embedding it.

## 4. Solution and core principle

**Repo docs carry stable rules. Prompts carry the phase execution
contract.**

The new standard at `docs/00-meta/process/claude-code-context-management-standard.md`
codifies this principle and translates it into operational guidance:

- a **thin execution prompt standard** that lists the 17 fields a
  Tier 1 authorization prompt must include, the content to omit
  (large extracts of prior phase reports, retained verdict ledgers,
  governance text, prior memo full text, prior closeout full text,
  policy memos in full), and the content that must never be omitted
  even in thin form (phase identifier and tier, scope, allowed
  surface, validation, fail-closed conditions, explicit non-scope);
- a **thin merge prompt standard** that lists the 12 fields a merge
  prompt must include and the rule that the merge-closeout structure
  itself is cited by path rather than re-embedded;
- a **mandatory vs optional read policy** that defines the default
  read list of nine files plus the immediate predecessor implementation
  report and immediate predecessor closeout / merge-closeout, with
  tier-specific guidance for what may be optional, and an explicit
  anti-pattern list (reading every prior phase report, reading every
  prior merge-closeout, reading deep specialist files when not in
  scope);
- a **session management standard** that recommends a fresh Claude
  Code session per phase by default, with explicit context-pressure
  signals to watch for and a session-branch protocol if context
  pressure does appear mid-phase;
- a **report compression standard** that defines short-form report
  permissibility (Tier 2 and Tier 4 only), references the full
  implementation report template for Tier 1 and Tier 3, and forbids
  short-form reports from omitting facts required for audit;
- a **reusable non-authorization block usage standard** that codifies
  citation by name (N-ACQUISITION, N-ENDPOINT, N-CREDENTIALS,
  N-MANIFEST, N-GATE-RERUN, N-SUCCESSOR-STATE, N-DERIVATION,
  N-DIAGNOSTICS-ML-STRATEGY, N-PHASE-5, N-VERDICT-LOCK) from
  `docs/00-meta/process/phase-risk-tiering-standard.md` §7 rather
  than restating each prohibition in full, with rules for
  phase-specific custom prohibitions and tier-interaction;
- an **allowed surface list standard** that requires every prompt
  to enumerate tracked files allowed for creation or modification,
  local gitignored outputs allowed (if any) with "not committed"
  status, and an explicit "anything else is forbidden" closing
  clause;
- a **handoff file guidance section** that connects this standard to
  `chat-branching-handoff-standard.md`: the handoff itself is a thin
  contract, not a vehicle for re-embedding project history; the
  continuation prompt's first responsibility is to instruct the new
  chat to read the repo;
- a **thin prompt size guidance** section with soft targets (typical
  Tier 1 prompt under ~3000 lines of guidance content; Tier 2 / Tier
  4 prompts substantially shorter) and an explicit rule that there
  is no hard token count — the goal is contract density, not byte
  count;
- an **MCP / Graphify / tooling governance** section codifying the
  default-deny posture: MCP, Graphify, `.mcp.json`, and credentialed
  tooling are not enabled by default; any future evaluation requires
  a separately authorized Tier 1 governance phase whose scope is
  precisely the evaluation, not the activation;
- **escalation rules** that cross-reference Phase 4bl-F §4: if any
  proposed thin-prompt change touches data semantics, manifest
  state, successor authorization, governance, or any item in
  Phase 4bl-F §4, the phase escalates to a full Tier 1 phase with
  the appropriate standard amendment, not a prompt-level fix;
- a **relationship-to-Phase-4bl-F** section stating that Phase 4bl-F
  defines the **governance** layer (which ceremony applies per
  tier; what non-authorization blocks may be referenced); this
  standard defines the **operational** layer (how a Claude Code
  prompt is shaped so that the governance layer's discipline is
  delivered to Claude Code in a context-window-safe way);
- a **relationship-to-prior-prompts** section that explicitly does
  not retroactively criticize or rewrite any prior phase prompt;
  prospective only;
- a **comprehensive non-authorization list** preserving every
  retained verdict, project lock, and non-rescue constraint;
- a **change-control process** matching the pattern used by every
  prior process standard (Tier 1 process phase, implementation
  report, closeout, merge with merge-closeout, narrow
  `current-project-state.md` update); and
- a **required references for future chats** section that lists this
  standard alongside the five existing process standards plus
  `current-project-state.md`, the most recent merge-closeout, and
  the most recent phase implementation report.

The new standard is prospective only. It does not rewrite any prior
phase prompt, any prior phase implementation report, any prior phase
closeout, any prior merge-closeout, or any prior governance memo.
Existing prompts and their resulting phases remain valid as recorded.

## 5. Files added

Phase 4bm-A-P1 adds two new tracked files:

- `docs/00-meta/process/claude-code-context-management-standard.md`
  (the new process standard).
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a-p1_claude-code-context-management-thin-prompt-standard.md`
  (this report).

A third tracked file is added by this branch:

- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a-p1_closeout.md`
  (the Phase 4bm-A-P1 closeout).

## 6. Files modified narrowly

Phase 4bm-A-P1 makes only narrow cross-reference additions to six
existing process documents. The pre-existing prose, structure, and
binding rules of each file are preserved. The new standard is added
to each file's "Required references for future chats" list or to the
nearest equivalent section, and each file gains exactly one short
clarifying paragraph that points to the new standard for the
operational concern it addresses.

- `docs/00-meta/process/phase-workflow-standard.md` — one bullet
  added to the "Required references for future chats" list, citing
  the new standard for thin contractual prompts, mandatory vs
  optional read policy, session management, soft size guidance, and
  the default-deny MCP / Graphify posture.
- `docs/00-meta/process/phase-risk-tiering-standard.md` — one bullet
  added to the "Required references for future chats" list, citing
  the new standard as the operational layer that sits on top of the
  tier model defined in Phase 4bl-F.
- `docs/00-meta/process/phase-prompt-template.md` — one bullet
  added to the top of the "Prompt design principles" list, naming
  thin contractual prompts as a design principle and citing the new
  standard. The existing principles, prompt templates, fail-closed
  condition library, validation command library, commit instruction
  library, final response format, and non-scope wording library are
  preserved.
- `docs/00-meta/process/operator-report-standard.md` — one new
  "Thin contractual prompts" subsection added near the existing
  "Risk-tier acknowledgement" subsection, describing how ChatGPT
  should draft thin prompts when assisting the operator. The
  existing role split, Claude Code compact report standard, ChatGPT
  operator-facing response standard, phase review template, post-
  merge confirmation template, prompt-generation response template,
  concept-explanation response template, ambiguity / correction
  response template, chat handoff response expectations, plain-
  English explanation rules, blocker vs non-blocker classification,
  still-blocked language standard, next-action recommendation
  standard, evidence and citation standard, tone and style standard,
  and anti-patterns list are preserved.
- `docs/00-meta/process/merge-closeout-standard.md` — one short
  paragraph added inside the existing "Short-form merge-closeout
  (Tier 4 only)" subsection, noting that the merge prompt that
  produces the merge-closeout should follow the thin merge prompt
  shape defined in the new standard. The 16-section structure, the
  SHA recording standard, the merge method standard, the files
  brought forward standard, the diff summary standard, the result
  / verdict standard, the local gitignored output standard, the
  validation results standard, the upstream immutability evidence
  standard, the manifest state preservation standard, the boundary
  confirmation standard, the retained verdict ledger standard, the
  preserved project locks standard, the no-rescue constraints
  standard, the successor authorization standard, the recommended
  state standard, the common-mistakes list, and the template are
  preserved.
- `docs/00-meta/process/chat-branching-handoff-standard.md` — one
  new "Thin handoff style" subsection added after the "'Do not rely
  on handoff alone' rule" section, noting that the handoff itself
  should be a thin contract rather than a vehicle for re-embedding
  project history. The 15 required handoff sections, 11 required
  continuation prompt sections, repo-query requirement, current-
  state / latest-phase / merge-state / local-data assumptions /
  artefact SHA / retained-verdict / project-lock checklists,
  current-arc summary, recommended next action, and the handoff
  template are preserved.

None of these edits rewrites any binding rule. Each edit adds a
cross-reference to the new standard. The diff for each modified file
is small and surgical.

## 7. Summary of new standard

The new standard at `docs/00-meta/process/claude-code-context-management-standard.md`
is structured for citation. It is intended to be referenced from a
thin authorization prompt by path, not embedded. Its core deliverables:

- a default mandatory read list of nine files for new chats and new
  Claude Code sessions: `docs/00-meta/current-project-state.md`,
  `docs/00-meta/process/phase-workflow-standard.md`,
  `docs/00-meta/process/phase-risk-tiering-standard.md`,
  `docs/00-meta/process/claude-code-context-management-standard.md`,
  `docs/00-meta/process/phase-prompt-template.md`,
  `docs/00-meta/process/operator-report-standard.md`,
  `docs/00-meta/process/merge-closeout-standard.md`, the immediate
  predecessor implementation report, and the immediate predecessor
  closeout or merge-closeout. Reading these nine files is sufficient
  for most phases. Reading more is permitted but must be justified
  by phase scope.
- a thin authorization prompt template with 17 required fields and
  explicit lists of content to omit, content to compress, and content
  that must never be omitted regardless of how thin the prompt
  becomes.
- a thin merge prompt template with 12 required fields and the rule
  that the merge-closeout structure is cited by path, not embedded.
- a fresh-session-per-phase recommendation, with context-pressure
  signals (Claude Code reports compaction; turn latency rises;
  response specificity drops; tool-call density falls) and a
  session-branch protocol for mid-phase context pressure (stop at
  the next safe checkpoint, summarize state to a fresh session,
  resume).
- soft size targets and an explicit refusal to set a hard token
  budget: density, not length, is the metric.
- a default-deny MCP / Graphify posture with the rule that any
  future evaluation is its own separately authorized Tier 1 phase.

The standard preserves every retained verdict and every project lock
verbatim. It does not authorize any successor phase. It does not
modify any manifest, gate report, successor-state artefact, label
artefact, feature artefact, raw artefact, or any other technical
state.

## 8. Boundary confirmations

Phase 4bm-A-P1 honors the following boundaries:

- no source code modified;
- no test modified;
- no script modified;
- no configuration modified (`pyproject.toml`, `README.md`,
  `.gitignore`, `.gitattributes` all unchanged);
- no MCP file modified;
- no data file modified;
- no `data/microstructure/` write of any kind;
- no manifest modified (no actual manifest's `research_eligible`
  flipped; no actual manifest's `eligibility_gate_status`
  transitioned; no actual manifest's `chronological_split_policy`
  changed);
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- Phase 4bb-F canonical sidecar policy preserved;
- Phase 4bl-F four-tier risk model and nine reusable non-authorization
  blocks preserved (this standard cites them; it does not amend
  them);
- Phase 4bl-F R-SIDECAR-CRLF standing remediation rule preserved
  verbatim (this standard does not invoke or modify it);
- Phase 4ak M0 twelve-clause gate, post-null cooldown rule, cooled-
  down families list, and memo template all preserved verbatim;
- Phase 4al refined no-rescue rule, §13 boundary, and §14 hierarchy
  preserved verbatim;
- no gate rerun;
- no normalization rerun;
- no derivation rerun;
- no diagnostics run;
- no ML, strategy, signal, or backtest output produced;
- no PnL, MFE, MAE, R-multiple, equity, position, alpha, edge,
  prediction, model-score, decision-score, entry-exit, or strategy
  output computed;
- no acquisition;
- no Binance / public / private endpoint contacted;
- no WebSocket opened;
- no credential used;
- no `.env` read or created;
- no `.mcp.json` read or created;
- MCP and Graphify not enabled;
- no successor authorized;
- no retained verdict revised (H0 / R3 / R1a / R1b-narrow / R2 / F1
  / D1-A / 5m thread / V2 / G1 / C1 preserved verbatim);
- no project lock changed (§11.6 = 8 bps per side, round-trip = 16
  bps, §1.7.3 = 0.25% / 2× / one-position / mark-price stops,
  Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8,
  Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w
  all preserved verbatim);
- no prior phase result modified;
- no prior governance memo modified beyond the narrow cross-
  reference additions enumerated in §6.

## 9. Validation

This phase is docs-only. The validation surface is narrow:

- `git diff --check`: clean.
- `git status --short`: shows only the tracked Phase 4bm-A-P1 files
  (new standard, narrow updates to six existing process docs,
  implementation report, closeout, narrow `current-project-state.md`
  update) plus the pre-existing untracked entries
  (`.claude/scheduled_tasks.lock`, `data/research/`).

`ruff` / `mypy` / `pytest` were **not** rerun for this phase. No
source code, test, script, or configuration file was modified. The
latest authoritative whole-repo validation remains the Phase 4bb-F-
implementation merge baseline (`ruff check .` PASS; `mypy` strict
PASS on 120 source files; microstructure `pytest` 915 passed + 1
pre-existing labelled skip; whole-repo `pytest` 1698 passed + 1
skipped + 2 pre-existing simulation failures). This standard's
prescriptive content does not change behavior of any source / test /
script and therefore does not need the test suite to be rerun. Per
the operator-report standard, this report does not claim those gates
were exercised in this phase.

## 10. Retained verdicts and project locks preserved

Retained verdicts (each preserved verbatim):

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED per Phase 3t
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

Project locks (each preserved verbatim):

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
- Phase 4aw `flip_research_eligible(...)` always-raises invariant
- Phase 4bb-F canonical path policy
- Phase 4bl-F four-tier risk model + nine reusable non-authorization
  blocks + R-SIDECAR-CRLF standing rule

All prior phase results preserved verbatim. No phase result is
modified by Phase 4bm-A-P1.

## 11. Successor authorization

**None.**

Phase 4bm-A-P1 does not authorize any successor phase. It does not
authorize Phase 4bm-A-P1 merge phase, Phase 4bm-B, Phase 4bm-C,
Phase 4bm-D, Phase 4bm-E, Phase 4bm-F, Phase 5, Phase 4 canonical,
paper / shadow, live-readiness, deployment, exchange-write, MCP,
Graphify, `.mcp.json`, credentials, or any other phase or activity.

## 12. Recommended state

**Remain paused.**

Phase 4bm-A-P1 is **branch-complete only** by this work. Per the
Phase 4bk-A workflow standard, Phase 4bm-A-P1 is **not project-
complete** until a separately authorized merge phase records its
merge-closeout on `main`. The operator should review this report,
the new standard, and the narrow cross-reference updates with
ChatGPT before deciding whether to authorize a merge prompt.

The conditional next step, **not authorized** by this phase: a
future operator-authorized Phase 4bm-A-P1 merge phase that merges
this branch into `main` and records a Phase 4bm-A-P1 merge-closeout
per `docs/00-meta/process/merge-closeout-standard.md`. Tier 1
ceremony (full 16-section merge-closeout). No further phase is
authorized after merge.

The operator's stated intent to pause for a broader project
discussion (complexity, phase usefulness, possible energy-market
sibling project) before any technical successor is authorized
continues to apply. This phase is part of that pause: it improves
the operational discipline that any future technical successor
will rely on, without authorizing any technical successor itself.
