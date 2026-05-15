# Phase 4bm-A-P1 — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bm-A-P1 — Claude Code Context Management / Thin
  Prompt Standard.
- **Type:** docs-only process refinement / governance calibration
  (Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md`, because
  Phase 4bm-A-P1 authors a new prospective process standard governing
  how every future authorization prompt, merge prompt, operator
  report, chat handoff, and Claude Code session is shaped).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bm-A-P1 branch onto `main` and
  record the project-complete merge-closeout. Phase 4bm-A-P1 authored
  the new `docs/00-meta/process/claude-code-context-management-standard.md`,
  the Phase 4bm-A-P1 implementation report, the Phase 4bm-A-P1
  closeout, six narrow cross-reference additions in existing process
  docs, and a narrow `current-project-state.md` update (Phase 4bm-A-P1
  narrative paragraph + new "Current phase:" block; prior Phase 4bm-A
  "Current phase:" block preserved verbatim as historical context).
  Without this merge plus this merge-closeout, Phase 4bm-A-P1 is
  branch-complete only and is not project-complete.
- **Target branch:** `main`.
- **Source branch:** `phase-4bm-a-p1/claude-code-context-management-thin-prompt-standard`.

## 2. SHAs

- **`main` SHA before merge:** `e6b510cfb54b0720a19ec1bb52490079e5780ca4`
  (Phase 4bm-A merge-closeout commit on `main`).
- **Branch commit SHAs:**
  - `806a02425e8d885695b7673c0400a0772efbc115` —
    `docs(phase-4bm-a-p1): claude code context management thin prompt standard`
    (the single Phase 4bm-A-P1 branch commit; contained the new
    standard, the Phase 4bm-A-P1 implementation report, the
    Phase 4bm-A-P1 closeout, the six narrow process-doc cross-
    references, and the `current-project-state.md` Phase 4bm-A-P1
    narrative paragraph + new "Current phase:" block).
- **Merge commit SHA:** `e00e1786e199a81a23748b964380606703451bbb`
  (`docs(phase-4bm-a-p1): merge claude code context management thin
  prompt standard`).
- **Merge-closeout commit SHA:** to be filled at commit time of this
  merge-closeout file.
- **Final `main` / `origin/main` SHA after push:** to be filled at
  push time of the merge-closeout commit.

## 3. Merge method

- `git merge --no-ff phase-4bm-a-p1/claude-code-context-management-thin-prompt-standard`
- Strategy: `ort` (the default).
- Merge commit message: `docs(phase-4bm-a-p1): merge claude code
  context management thin prompt standard`.
- Pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing.

## 4. Files brought forward by the merge

Process standard added (1):

- `docs/00-meta/process/claude-code-context-management-standard.md`
  — the new prospective Claude Code context-management / thin-prompt
  standard (~908 lines).

Implementation reports added (2):

- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a-p1_claude-code-context-management-thin-prompt-standard.md`
  — the Phase 4bm-A-P1 implementation report.
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-a-p1_closeout.md`
  — the Phase 4bm-A-P1 closeout.

Process standards modified narrowly (6):

- `docs/00-meta/process/phase-workflow-standard.md` — one bullet
  added to the "Required references for future chats" list citing
  the new standard for thin contractual prompts, mandatory vs
  optional read policy, session management, soft size guidance, and
  default-deny MCP / Graphify posture.
- `docs/00-meta/process/phase-risk-tiering-standard.md` — one bullet
  added to the "Required references for future chats" list citing
  the new standard as the operational layer that sits on top of the
  tier model.
- `docs/00-meta/process/phase-prompt-template.md` — one new top-level
  bullet in the "Prompt design principles" list ("Write thin
  contractual prompts, not vague prompts") with detailed text about
  citing repository by path rather than embedding content and citing
  reusable non-authorization blocks by name.
- `docs/00-meta/process/operator-report-standard.md` — one new "Thin
  contractual prompts" subsection describing how ChatGPT should
  draft thin prompts that cite repository instead of embedding.
- `docs/00-meta/process/merge-closeout-standard.md` — one short
  paragraph added inside the existing "Short-form merge-closeout
  (Tier 4 only)" subsection noting that merge prompts follow the
  thin merge prompt shape.
- `docs/00-meta/process/chat-branching-handoff-standard.md` — one
  new "Thin handoff style" subsection noting that the handoff
  itself is a thin contract.

Docs modified narrowly (1):

- `docs/00-meta/current-project-state.md` — Phase 4bm-A-P1 narrative
  paragraph inserted before the prior Phase 4bm-A paragraph; new
  Phase 4bm-A-P1 "Current phase:" block; prior Phase 4bm-A "Current
  phase:" block preserved verbatim under a new
  "Earlier Phase 4bm-A 'Current phase:' block (preserved here for
  continuity; Phase 4bm-A is no longer the current phase):"
  historical-context section.

Source: not modified.
Tests: not modified.
Scripts: not modified.
Configs (`pyproject.toml`, `README.md`, `.gitignore`,
`.gitattributes`, MCP files): not modified.
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
 docs/00-meta/current-project-state.md              | 313 +++++++
 ...code-context-management-thin-prompt-standard.md | 455 +++++++++++
 .../2026-05-15_phase-4bm-a-p1_closeout.md          | 252 ++++++
 .../process/chat-branching-handoff-standard.md     |  14 +
 .../claude-code-context-management-standard.md     | 908 +++++++++++++++++++++
 docs/00-meta/process/merge-closeout-standard.md    |  11 +
 docs/00-meta/process/operator-report-standard.md   |  19 +
 docs/00-meta/process/phase-prompt-template.md      |  17 +
 .../00-meta/process/phase-risk-tiering-standard.md |   6 +
 docs/00-meta/process/phase-workflow-standard.md    |   4 +
 10 files changed, 1999 insertions(+)
```

The diff matches the expected change set from the Phase 4bm-A-P1
authorization prompt verbatim: 1 new process standard, 2 new
implementation report files under
`docs/00-meta/implementation-reports/`, 6 narrowly modified existing
process docs under `docs/00-meta/process/`, 1 narrowly modified
`docs/00-meta/current-project-state.md`. Pure additions, no
deletions. No source / test / script / config / data files modified.

## 6. Verdict

**STANDARD RECORDED.**

Phase 4bm-A-P1 is now project-complete, having been merged into
`main` and closed out by this merge-closeout. The merge added a new
prospective process standard governing how every future authorization
prompt, merge prompt, operator report, chat handoff, and Claude Code
session is shaped. The standard's core principle is **"Repo docs
carry stable rules. Prompts carry the phase execution contract."** —
stable rules live in repo docs and are read at execution time;
prompts carry only the phase execution contract.

Standard contents (recorded for the project record):

- thin contractual prompt vs embedded prompt definitions;
- mandatory vs optional read policy with a default mandatory list of
  nine files plus the most-recent merge-closeout and implementation
  report;
- 17-field thin execution prompt standard covering identity, tier,
  base, branch name, scope, deliverables, files, write boundary,
  non-authorization blocks by name reference, validation, reporting,
  stop condition, retained verdict preservation, project lock
  preservation, governance integration, M0 / cooldown posture, and
  operator-report format reference;
- 12-field thin merge prompt standard covering identity, base,
  branch, merge target, merge method, files brought forward,
  merge-closeout location, successor authorization, retained verdict
  preservation, project lock preservation, validation, and reporting;
- prompt content rules forbidding embedded project history, repeated
  retained verdict ledgers, repeated rejection topology, repeated
  cooldown lists, repeated nine non-authorization blocks, repeated
  forty-five-check enumerations, repeated R-SIDECAR-CRLF criteria,
  repeated structural-integrity rationale, repeated 16-section
  merge-closeout schema, and repeated 10-item Claude Code report
  format;
- session management rule (each phase runs in its own chat session;
  session ends after the final operator report; merge prompt opens
  a new session referencing the closeout file in the repo);
- soft size guidance (target under 8,000 tokens; split work or move
  detail into a repo memo and reference by path if a prompt risks
  exceeding 16,000 tokens);
- default-deny posture for MCP / Graphify / `.mcp.json` /
  credentials / network access / `.env` reads;
- integration with the Phase 4bl-F four-tier risk model (Tier 1
  prompts permit longer scope but still cite repository rather than
  embed; Tier 2 / 3 / 4 prompts inherit the thin style and the
  standing R-SIDECAR-CRLF rule where applicable);
- operator report integration (the existing 10-item compact format
  is preserved verbatim; ChatGPT drafts thin prompts that cite repo
  by path; Claude Code reads files at execution time);
- thin handoff style for chat-branching handoffs (handoff itself is
  a thin contract; cite by repository path rather than re-embedding
  project history);
- acceptance criteria for any future merge phase and any future
  prompt drafted under the standard.

The narrow cross-references added to the six existing process
standards (`phase-workflow-standard.md`,
`phase-risk-tiering-standard.md`, `phase-prompt-template.md`,
`operator-report-standard.md`, `merge-closeout-standard.md`,
`chat-branching-handoff-standard.md`) consist of single bullets,
single paragraphs, or single subsections that name the new standard
and point readers to it. **No prior standard is rewritten. No
binding rule is amended.** The new standard sits as an operational
layer on top of the four-tier risk model: domain-specific process
files retain authority on their own surface; the new standard
governs how the prompts that drive those phases are shaped.

No retained verdict was revised. No project lock was changed. No
`data/microstructure/` artefact was created or modified. No
`research_eligible` flag was flipped on any actual manifest. No
`eligibility_gate_status` was transitioned on any actual manifest.
No `chronological_split_policy` was changed on any actual manifest.
No gate was rerun. No new gate report was created. No
successor-state artefact was created. No data was acquired. No
normalization was executed. No successor phase is authorized.
**Recommended state: remain paused.**

## 7. Local gitignored outputs (if any)

**None.** Phase 4bm-A-P1 was a docs-only Tier 1 process refinement
phase. No local artefacts were produced under `data/microstructure/`
or anywhere else outside the tracked docs.

## 8. Validation results

- `git status` (pre-merge, on branch
  `phase-4bm-a-p1/claude-code-context-management-thin-prompt-standard`):
  clean except pre-existing untracked `.claude/scheduled_tasks.lock`
  and `data/research/`.
- `git rev-parse main` (pre-merge): `e6b510cfb54b0720a19ec1bb52490079e5780ca4`.
- `git rev-parse origin/main` (pre-merge): `e6b510cfb54b0720a19ec1bb52490079e5780ca4`.
- `main == origin/main` (pre-merge): YES (in sync).
- `git diff --stat main..phase-4bm-a-p1/claude-code-context-management-thin-prompt-standard`:
  10 files changed, 1999 insertions(+), 0 deletions(-).
- `git diff --check main..phase-4bm-a-p1/claude-code-context-management-thin-prompt-standard`:
  clean (no whitespace errors).
- `git merge --no-ff` produced merge commit
  `e00e1786e199a81a23748b964380606703451bbb` with `ort` strategy.
  No conflicts.
- `git status` (post-merge, on `main`): clean except pre-existing
  untracked `.claude/scheduled_tasks.lock` and `data/research/`.
- `git diff --check` (post-merge): clean.
- `git log --oneline -5 --decorate` (post-merge): confirms merge
  commit `e00e178` at HEAD on top of branch commit `806a024` on top
  of Phase 4bm-A merge-closeout commit `e6b510c`.
- `ruff` / `mypy` / `pytest` — **not run.** Per the
  `operator-report-standard.md` and the Phase 4bm-A-P1 authorization
  prompt, no source / test / script / configuration file was modified
  by Phase 4bm-A-P1 or by this merge, so no whole-repo code-quality
  gate was rerun. The latest authoritative whole-repo validation
  remains the Phase 4bb-F-implementation merge baseline (`ruff` PASS,
  `mypy` strict 120 source files PASS, microstructure `pytest` 915
  passed + 1 pre-existing labelled skip, whole-repo `pytest` 1698
  passed + 1 skipped + 2 pre-existing simulation failures).

## 9. Upstream immutability evidence (if applicable)

**n/a — phase did not access any local artefact.** Phase 4bm-A-P1
was a docs-only process refinement memo. It did not access, read,
write, or modify any artefact under `data/microstructure/`. Every
prior local artefact (raw zips, raw manifests including the Phase
4az `__v001` and the Phase 4bl-C `__v002` raw manifest, sidecars,
acquisition logs, normalized parquet, derived manifest, feature
parquet, feature manifest, label parquet, label manifest, every
gate report including the Phase 4bb-D raw `__v001` 45/45 PASS
report, the Phase 4bf derived 55/55 PASS report, the Phase 4bi-B
feature 70/70 PASS report, the Phase 4bj-E label 72/72 PASS report,
the Phase 4bl-D raw multi-day FAIL gate report, the Phase 4bl-D-R
raw multi-day PASS gate report, every successor-state artefact
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
always-raises invariant preserved (never invoked by Phase 4bm-A-P1
or by this merge).

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
- no `.mcp.json` read or created
- no `.env` read or created
- MCP and Graphify not enabled (default-deny posture preserved and
  formally codified by the new standard)
- no prior implementation report or merge-closeout modified
- six existing process standards (`phase-workflow-standard.md`,
  `phase-risk-tiering-standard.md`, `phase-prompt-template.md`,
  `operator-report-standard.md`, `merge-closeout-standard.md`,
  `chat-branching-handoff-standard.md`) modified only by single
  narrow cross-reference additions; no binding rule rewritten
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
- no exchange-write surface touched
- no production-key creation
- no paper / shadow / live-readiness / deployment work
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- Phase 4bb-F canonical path policy preserved (no policy text
  changed)
- Phase 4bl-F R-SIDECAR-CRLF standing rule preserved (no rule text
  changed)
- Phase 4bl-F four-tier risk model preserved (the new standard sits
  as an operational layer on top of, not in place of, the tier
  model)
- Phase 4bl-F nine reusable non-authorization blocks preserved and
  the new standard formalises their usage by name reference
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no Phase 4al refined no-rescue rule, §13 boundary, or §14
  hierarchy amendment
- Phase 4bl-D through Phase 4bm-A history preserved verbatim
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

The Phase 4bm-A-P1 merge does not, and cannot, be construed as
authorising:

- Phase 4bm-B execution (the future Multi-Day Normalization
  Implementation phase that the Phase 4bm-A design memo specifies);
- normalization, derivation, feature computation, label computation,
  or diagnostics;
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
- MCP, Graphify, `.mcp.json`, or credentials work (the new standard
  formally codifies the default-deny posture for these surfaces,
  but does **not** enable them and does not introduce any new
  tooling);
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
  remains a remediation rule only; the new standard does not change
  its scope);
- amending the Phase 4bl-F four-tier risk model or the nine
  reusable non-authorization blocks (the new standard sits as an
  operational layer on top of the tier model and formalises how the
  non-authorization blocks are cited, but does not change their
  text);
- amending Phase 4ak M0, the post-null cooldown rule, the
  cooled-down families list, or the memo template;
- amending Phase 4al refined no-rescue rule, §13 boundary, or §14
  hierarchy;
- amending Phase 4aw `flip_research_eligible(...)` always-raises
  invariant;
- amending any prior process standard's binding rules (the six
  process docs are modified only by single narrow cross-reference
  additions; no binding rule is rewritten);
- pre-authorising any successor phase under any name (Phase 4bm-B,
  Phase 4bm-C, Phase 4bm-D, Phase 4bm-E, Phase 4bm-F, Phase 4bm-*,
  Phase 4bn-*, Phase 4bo-*, Phase 4bp-*, Phase 4bq-*).

## 15. Successor authorization

**None.**

The following candidate successors are explicitly **not** authorized
by this merge:

- Phase 4bm-B — Multi-Day Normalization Implementation (the natural
  conditional successor by direct precedent of Phase 4bd for the
  Phase 4az `__v001` raw family; the Phase 4bm-A design memo
  specifies what Phase 4bm-B must do but neither Phase 4bm-A nor
  Phase 4bm-A-P1 authorizes execution)
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
authorized. That stated intent continues to apply. Phase 4bm-A-P1
does not change that intent; it equips the project to author future
prompts and reports more efficiently when the operator is ready.

**Conditional next, NOT authorized:**

Two non-mutually-exclusive conditional paths exist after this merge,
neither of which is authorized by this merge-closeout:

1. Operator-driven discussion of the broader project direction
   (complexity, phase usefulness, energy-market sibling project)
   may continue. The new standard does not preempt that discussion;
   it lowers the cost of resuming work after it if the operator
   chooses to do so.
2. A future operator-authorized Phase 4bm-B — Multi-Day Normalization
   Implementation (docs-and-code, Tier 1) remains the cleanest
   technical-successor option whenever the operator chooses to
   resume technical work. Phase 4bm-B would be drafted under the
   new thin-prompt standard adopted by Phase 4bm-A-P1; it would
   consume the Phase 4bm-A design memo verbatim, run a future
   `scripts/phase4bm_b_normalize_multiday_aggtrades.py` (or
   equivalent) exactly once against the Phase 4bl-C `__v002`
   90-date BTCUSDT raw archive cited by the Phase 4bl-D-R PASS gate
   report and the Phase 4bl-E successor-state record, and produce
   90 per-day Parquet files plus 90 paired canonical Phase 4bb-F
   sidecars plus one multi-day index manifest, all under the
   65-criterion strict-fail-closed validation contract, with
   `research_eligible=false` and `eligibility_gate_status=pending`
   for the new derived `__v002` manifest. Phase 4bm-B is **not**
   authorized by this merge.
