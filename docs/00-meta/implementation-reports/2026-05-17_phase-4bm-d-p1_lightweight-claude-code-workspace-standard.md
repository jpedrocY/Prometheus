# Phase 4bm-D-P1 — Lightweight Claude Code Workspace Execution Standard

**Phase identity:** Phase 4bm-D-P1 — Lightweight Claude Code Workspace Execution Standard.
**Type:** docs-only Tier 1 process / workflow standardization phase.
**Date:** 2026-05-17.
**Branch:** `phase-4bm-d-p1/lightweight-claude-workspace-standard`.
**Status:** branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Phase identity

Phase 4bm-D-P1 formalises the **lightweight Claude Code workspace** pattern as the recommended default for heavy Prometheus Claude Code execution sessions. The phase is docs-only and prospective: it adds one new process standard under `docs/00-meta/process/`, adds narrow cross-references in five existing process standards, adds the standard pair of implementation report + closeout under `docs/00-meta/implementation-reports/`, and narrowly updates `docs/00-meta/current-project-state.md`. It does not modify any source code, test, script, configuration, README, pyproject, `.gitignore`, `.gitattributes`, MCP file, `.claude/` operator-side tooling, manifest, sidecar, gate report, successor-state artefact, normalized parquet, derived parquet, feature parquet, label parquet, or any other `data/microstructure/` artefact.

The phase is the operational complement to Phase 4bm-A-P1 (`docs/00-meta/process/claude-code-context-management-standard.md`). Phase 4bm-A-P1 established that repo docs carry stable rules and prompts carry the phase execution contract — a discipline that governs **what goes into the prompt and what gets read**. Phase 4bm-D-P1 extends that discipline by governing **where the Claude Code session is launched from and what auto-context the harness inherits at session start**. Both disciplines apply together to heavy execution sessions.

Per the Phase 4bk-A workflow standard (`docs/00-meta/process/phase-workflow-standard.md`), Phase 4bm-D-P1 is **branch-complete only** and is **not project-complete** until a separately authorized merge phase records its merge-closeout on `main`.

---

## 2. Branch and base SHA

| Item | Value |
| ---- | ----- |
| Branch | `phase-4bm-d-p1/lightweight-claude-workspace-standard` |
| `main` HEAD before Phase 4bm-D-P1 branch | `59e3e6cdca4996289e26e12b4b68d96615728702` (Phase 4bm-D merge-closeout commit) |
| Pre-branch sync state | `main` == `origin/main` == `59e3e6c…` (in sync) |
| Predecessor on `main` | Phase 4bm-D (Multi-Day Derived-Family Eligibility Gate, project-complete on `main`) |

---

## 3. Phase tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md`. The phase introduces a new repo-resident process standard (`claude-code-lightweight-workspace-standard.md`) that future phases will cite by name. New process content of this kind warrants the full ceremony — single phase named, allowed tracked files enumerated, strict non-scope enumerated, validation commands specified, fail-closed conditions specified, full implementation report, full closeout, separate merge phase, full 16-section merge-closeout, narrow `current-project-state.md` update — even though the phase is docs-only and changes no scientific meaning. This matches the precedent set by Phase 4bk-A (the workflow standard), Phase 4bl-F (the risk-tiering standard), and Phase 4bm-A-P1 (the context-management standard).

---

## 4. Motivation

Phase 4bm-D (Multi-Day Derived-Family Eligibility Gate) exposed a major Claude Code workflow issue. Running heavy Prometheus code / test / data phases directly from `C:\Prometheus` as the Claude Code working directory caused the Claude Code harness to load excessive workspace / project context at session start, including the very large `docs/00-meta/current-project-state.md` (>23,000 lines), the deep `docs/00-meta/process/` standards layer, the deep `docs/00-meta/implementation-reports/` history, and similar surfaces. On the Phase 4bm-D heavy workload, this auto-loaded context dominated the context window, triggered repeated auto-compact loops, and caused extreme per-tool-call token consumption that prevented the phase from completing within bounded operator sessions.

The successful operational recovery — recorded in the Phase 4bm-D implementation report and merge-closeout `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-d_merge-closeout.md` — was to run Claude Code from a **lightweight launcher workspace** at `C:\ClaudeRuns\prometheus-light` while accessing the real Prometheus repository explicitly at `C:\Prometheus`. The light workspace contained no governance memos, no source code, no tests, and no data, so the Claude Code harness did not auto-load anything heavy at session start. The operator's prompt, the chat-branching handoff, the `cd C:\Prometheus && <command>` discipline, and targeted repo reads then carried the work that auto-loaded context would otherwise have done — but under bounded operator control.

Phase 4bm-D-P1 formalises that workflow as a repo-resident process standard so future heavy phases inherit the discipline by default rather than rediscovering it under context pressure.

---

## 5. Goals and non-goals

### Goals

- Formalise the lightweight Claude Code workspace pattern as the recommended default for heavy Prometheus Claude Code execution sessions.
- State the workspace layout precisely: light workspace at `C:\ClaudeRuns\prometheus-light`; real repository at `C:\Prometheus`; every shell command uses `cd C:\Prometheus && <command>`.
- Record the recommended launch command, including the session-local environment variable assignments that reduce auto-loading of project memory / CLAUDE.md content.
- State the IDE / Antigravity posture for the Claude Code agent (open the light workspace; access the real repo explicitly through commands and absolute paths).
- State the default agent / memory policy (off by default; agent packs and agent memory not copied into the light workspace).
- Record the optional local-hooks posture (local-only operator tooling; not committed unless a separate phase authorizes repo inclusion; not required for normal operation).
- Define session slicing so that long implementation phases can move through multiple bounded Claude Code sessions inside one repo phase.
- Define the prompt format under the light workspace (working directory, real repo path, command convention added to the standard thin-prompt fields).
- State when to use the light workspace (heavy phases by default; optional for small docs-only / short merge / Tier 4 admin phases).
- Add narrow cross-references in five existing process standards so future authors are pointed at the new standard from the documents they will already be reading.
- Reaffirm the default-deny MCP / Graphify posture verbatim.
- Reaffirm the no-successor-authorization rule verbatim.

### Non-goals

- This standard does **not** modify any source code, test, script, configuration, README, pyproject, `.gitignore`, `.gitattributes`, MCP file, or `.claude/` operator-side tooling.
- This standard does **not** copy Prometheus source / tests / data / governance memos / implementation-report history / agent packs / agent memory into the light workspace. The light workspace remains an execution shell, not a replacement repository.
- This standard does **not** rewrite prior phase history. Prior phases that ran directly from `C:\Prometheus` remain valid as recorded. Phase 4bm-D's operational recovery is the precedent that motivates this standard; the precedent itself is preserved as recorded.
- This standard does **not** authorize MCP, Graphify, `.mcp.json`, credentials, exchange-write, paper / shadow / live, deployment, production-key creation, authenticated APIs, private endpoints, user stream, agents-by-default, additional data acquisition, endpoint calls, manifest mutation, `research_eligible` flip, `eligibility_gate_status` transition, `chronological_split_policy` change, retained-verdict revision, project-lock revision, M0 amendment, or any successor phase (including Phase 4bm-E and Phase 4bm-F).

---

## 6. Files changed by this phase

Tracked files added (3):

- `docs/00-meta/process/claude-code-lightweight-workspace-standard.md` — the new process standard (Phase 4bm-D-P1).
- `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-d-p1_lightweight-claude-code-workspace-standard.md` — this implementation report.
- `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-d-p1_closeout.md` — the Phase 4bm-D-P1 closeout (companion to this report).

Tracked files modified narrowly (6):

- `docs/00-meta/process/claude-code-context-management-standard.md` — added a single bullet to the "Required references for future chats" section pointing at the new standard; no other change.
- `docs/00-meta/process/phase-prompt-template.md` — added a single bullet to the "Prompt design principles" list directing heavy-execution prompts to include the lightweight workspace fields per §10 of the new standard; no other change.
- `docs/00-meta/process/chat-branching-handoff-standard.md` — appended a single paragraph to the "Thin handoff style" section explaining that handoffs whose next phase is heavy execution should carry the workspace / repo-path / command-convention fields; no other change.
- `docs/00-meta/process/operator-report-standard.md` — appended a single paragraph to the "Thin contractual prompts" section explaining that heavy-execution prompts drafted by ChatGPT should carry the workspace / repo-path / command-convention fields; no other change.
- `docs/00-meta/process/phase-workflow-standard.md` — added a single bullet to the "Required references for future chats" section pointing at the new standard; no other change.
- `docs/00-meta/current-project-state.md` — narrow Phase 4bm-D-P1 narrative paragraph plus the new "Current phase:" block; prior Phase 4bm-D "Current phase:" block preserved as labelled historical context.

No other tracked file modified.

---

## 7. Files NOT modified

- No source under `src/` modified.
- No tests under `tests/` modified.
- No scripts under `scripts/` modified.
- `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes` — unchanged.
- No MCP file modified or created (no `.mcp.json`).
- No `.claude/settings.json` / `.claude/settings.local.json` / `.claude/hooks/` / `.claude/agents/` file modified or created in `C:\Prometheus`. (Local operator-side hook tooling lives under `C:\ClaudeRuns\prometheus-light\.claude\...` and is not part of this commit.)
- No `data/microstructure/` file modified, added, or deleted.
- No `data/research/` file committed (the pre-existing untracked `data/research/` entry remains untracked).
- No manifest, sidecar, gate report, successor-state JSON, normalized parquet, derived parquet, feature parquet, or label parquet modified.
- No prior implementation report, closeout, or merge-closeout modified.
- No prior process standard modified beyond the narrow cross-reference edits listed in §6.
- No prior governance memo modified beyond the narrow `current-project-state.md` paragraph addition listed in §6.

---

## 8. What the new standard contains

The new standard (`docs/00-meta/process/claude-code-lightweight-workspace-standard.md`) contains 16 sections:

1. **Purpose** — heavy implementation phases can fail operationally if Claude Code is launched from `C:\Prometheus` and auto-loads excessive project context; the lightweight workspace pattern reduces hidden context load while preserving repo authority; complements Phase 4bm-A-P1; prospective-only.
2. **Authority** — process-only; does not revise any retained verdict, project lock, M0 governance, manifest state, label artefact, gate protocol, canonical path policy, strategy decision, or successor authorization; specialist documents and domain-specific process files win their own surfaces.
3. **Core principle** — heavy execution sessions should start from a lightweight Claude Code workspace; the real Prometheus repository remains the authoritative target; repo docs remain authoritative but read explicitly and narrowly; the light workspace is an execution shell, not a replacement repository.
4. **Standard workspace layout** — light workspace at `C:\ClaudeRuns\prometheus-light`; real repository at `C:\Prometheus`; all repo commands use `cd C:\Prometheus && <command>`; Claude Code launched from the light workspace; the real repo provided as an added directory or accessed by absolute path; the light workspace must not contain a copy of the source / tests / data / governance memos / agent packs.
5. **Recommended launch command** — `cd C:\ClaudeRuns\prometheus-light; $env:CLAUDE_CODE_DISABLE_CLAUDE_MDS="1"; $env:CLAUDE_CODE_DISABLE_AUTO_MEMORY="1"; claude --add-dir C:\Prometheus`; environment variables are session-local; the CLI surface may evolve but the principle is binding.
6. **IDE / Antigravity guidance** — for heavy Prometheus phases, do not launch the Claude Code agent from an IDE workspace rooted at `C:\Prometheus`; open `C:\ClaudeRuns\prometheus-light` as the workspace; access `C:\Prometheus` explicitly through commands and absolute paths; IDE may still be used as a normal editor / viewer for the real repo.
7. **Agent and memory policy** — Prometheus agents and project memory not auto-loaded by default; heavy execution sessions rely on the operator prompt, the chat-branching handoff, targeted repo doc reads, targeted file reads, and explicit validation commands; agents may be considered only through a separately authorized, bounded process decision; agent packs and agent memory are not copied into the light workspace by default.
8. **Hooks and local guardrails** — optional local hooks may be used for compact recovery, pre-compact stop / checkpoint, read-budget guards, local session discipline; hook files and settings are local operator tooling unless separately authorized for repo inclusion; local hooks should not be committed unless a separate process phase authorizes project-wide hook standardization; the standard does not require hooks for normal operation; local hooks must not weaken any repo guarantee (the `--no-verify` / `--no-gpg-sign` / no-force-push rules remain binding).
9. **Session slicing** — large implementation phases may use multiple bounded Claude Code sessions within the same repo phase; each bounded session has one concrete task, a short checkpoint / handoff, a narrow allowed file surface, explicit validation, and stop / report behavior; session slicing does not create new repo phases; it is execution hygiene inside the existing phase lifecycle.
10. **Prompt format under light workspace** — future heavy-phase authorization prompts include the Claude Code working directory, the real repository path, the `cd C:\Prometheus && <command>` command convention, the current phase, the branch, the latest completed phase, the allowed files, the forbidden surfaces, the mandatory docs, the optional-read / search rule, and the stop condition; the first three fields are the addition introduced by this standard.
11. **When to use the light workspace** — use by default for code-heavy, test-heavy, data / gate execution, long-validation, large-source / large-test phases, and any phase whose pattern previously triggered auto-compact / context warnings; optional for small docs-only, short merge, narrow Tier 4 admin phases; avoid direct `C:\Prometheus` Claude workspace if the symptoms listed appear at startup.
12. **Relationship to existing process docs** — extends Phase 4bm-A-P1; preserves Phase 4bl-F risk-tiering, Phase 4bk-A workflow lifecycle, merge-closeout requirements, operator-report requirements, chat-branching handoff structure, and phase-prompt-template structure unchanged in substance; preserves M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical path policy, Phase 4bl-F R-SIDECAR-CRLF, and all nine reusable non-authorization blocks verbatim.
13. **Non-authorizations** — explicit list of activities the standard does not authorize (MCP, Graphify, `.mcp.json`, credentials, exchange-write, paper / shadow / live, additional acquisition, endpoint calls, agents by default, copying agent memory into the light workspace, manifest mutation, retained-verdict revision, project-lock revision, Phase 4bm-E, Phase 4bm-F, any other successor).
14. **Required references for future chats** — the standard cross-references the seven existing process docs plus `current-project-state.md` plus the most recent merge-closeout plus the most recent implementation report.
15. **Change-control process for this standard** — updates require a separately authorized docs-only Tier 1 process phase that names this file in its allowed tracked files, with an implementation report, closeout, merge into `main`, merge-closeout, and a narrow `current-project-state.md` paragraph addition.
16. **Final note** — heavy execution sessions should start from `C:\ClaudeRuns\prometheus-light`, access `C:\Prometheus` explicitly through `cd C:\Prometheus && <command>`, suppress auto-loading of project memory / CLAUDE.md content, default agents and memory to off, and rely on the operator prompt plus targeted repo doc reads for context.

---

## 9. Narrow cross-reference edits

Five existing process standards received a single narrow edit each. None of the edits rewrites the underlying standard; each is either a new bullet in an existing list or a single appended paragraph in an existing section.

| File | Section touched | Nature of edit |
| ---- | --------------- | -------------- |
| `docs/00-meta/process/claude-code-context-management-standard.md` | "Required references for future chats" | Added one bullet pointing at the new standard and stating that it complements this standard by governing where the Claude Code session is launched from. |
| `docs/00-meta/process/phase-prompt-template.md` | "Prompt design principles" | Added one bullet stating that heavy-execution phase prompts should include the lightweight workspace fields (working directory, real repo path, command convention) per §10 of the new standard. |
| `docs/00-meta/process/chat-branching-handoff-standard.md` | "Thin handoff style" | Appended one paragraph stating that handoffs whose next phase is heavy execution should include the lightweight workspace fields per §10 of the new standard. |
| `docs/00-meta/process/operator-report-standard.md` | "Thin contractual prompts" | Appended one paragraph stating that ChatGPT-drafted heavy-execution prompts should include the lightweight workspace fields per §10 of the new standard. |
| `docs/00-meta/process/phase-workflow-standard.md` | "Required references for future chats" | Added one bullet pointing at the new standard with a one-sentence summary. |

No other text in these files was modified. The 16-section structure of `merge-closeout-standard.md` was deliberately not touched, since this standard explicitly does not modify merge-closeout requirements.

---

## 10. Current-project-state update

`docs/00-meta/current-project-state.md` was updated narrowly:

- A new Phase 4bm-D-P1 narrative paragraph was added at the top of the existing chronological narrative chain, immediately ahead of the Phase 4bm-D paragraph. The paragraph records: phase identity (docs-only Tier 1 process / workflow standardization phase); branch; base SHA; tracked files added (3); tracked files modified narrowly (6); the recommended launch command; the seven new-standard content blocks; the default-off agent / memory posture; the optional-local-hooks posture; the session-slicing definition; the prompt-format addition; the when-to-use rules; the verbatim retained-verdict ledger; the verbatim preserved-project-locks list; the verbatim non-authorizations list; the branch-complete-only lifecycle status; and the no-successor-authorized recommendation.
- The previous "Current phase:" block (Phase 4bm-D) is preserved verbatim as a labelled "Earlier 'Current phase:' block (preserved here for continuity; Phase 4bm-D is no longer the current phase)" historical block.
- A new "Current phase:" block records Phase 4bm-D-P1 as the current branch-complete state, naming the branch, the base SHA, the new standard, and the recommended pause.

No other section of `current-project-state.md` is modified.

---

## 11. Validation summary

Phase 4bm-D-P1 is docs-only. No source, tests, scripts, or configuration is modified. The validation contract is correspondingly narrow per `docs/00-meta/process/phase-risk-tiering-standard.md` §8 short-form / docs-only guidance and `docs/00-meta/process/claude-code-context-management-standard.md` §4 (Required validation fields):

| Tool | Scope | Expected result |
| ---- | ----- | --------------- |
| `git diff --check` | working tree on `phase-4bm-d-p1/...` | clean (no whitespace errors; no unresolved merge markers) |
| `git status --short` | working tree on `phase-4bm-d-p1/...` | only the tracked Phase 4bm-D-P1 files (3 added + 6 modified) plus the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`) |
| `git diff --name-status main..HEAD` | branch vs `main` | exactly 9 tracked files (`A` for the 3 added; `M` for the 6 modified) matching §6 |
| `git diff --stat main..HEAD` | branch vs `main` | insertion / deletion totals match the actual content added |

`ruff`, `mypy`, and `pytest` are not part of this validation contract because no source code, test, script, or configuration file is modified by this phase. Per the operator authorization: "Do not run ruff, mypy, or pytest unless source/tests/scripts/config files are unexpectedly modified. Do not claim they were run unless actually run." Those tools were therefore not invoked. The pre-existing whole-repo `pytest` baseline (`1156 passed, 1 skipped`; two pre-existing `KeyError: 'trade_count'` simulation failures on `tests/simulation/test_backtest_real_2026_03.py` unchanged from prior phases) remains the authoritative baseline; Phase 4bm-D-P1 does not modify any source or test and therefore cannot have introduced any new regression against it.

The closeout records the actual `git diff --check`, `git status --short`, `git diff --name-status main..HEAD`, and `git diff --stat main..HEAD` outputs at the time of the docs commit.

---

## 12. Boundary confirmations

This phase honours every relevant non-authorization. Citing the canonical reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 by name:

- **N-ACQUISITION** applies — no acquisition; no download; no new artefact from any remote source; no extension of any existing dataset; no creation or modification of raw data files.
- **N-ENDPOINT** applies — no Binance endpoint called (public, authenticated, or private); no other exchange / data-vendor endpoint called; no `data.binance.vision` contact; no WebSocket opened.
- **N-CREDENTIALS** applies — no credential used, read, created, or referenced; `.env` not read or created; `.mcp.json` not read or created; MCP / Graphify not enabled; no order placed; no position modified; no exchange-write surface contacted.
- **N-MANIFEST** applies — no actual manifest file modified; no `research_eligible` flip on any actual manifest; no `eligibility_gate_status` transition on any actual manifest; no `chronological_split_policy` change on any actual manifest; Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- **N-GATE-RERUN** applies — no raw / derived / feature / label / metrics gate rerun; no new gate report generated.
- **N-SUCCESSOR-STATE** applies — no successor-state artefact created or modified.
- **N-DERIVATION** applies — no normalization, derivation, feature computation, or label computation; no feature kernel run; no label kernel run; no derived / feature / label parquet file produced.
- **N-DIAGNOSTICS-ML-STRATEGY** applies — no diagnostics run; no ML trained; no ML architecture designed; no features ranked; no meta-labeling created; no strategy created; no signals computed; no backtest run; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output computed.
- **N-PHASE-5** applies — Phase 5 not authorized; Phase 4 canonical not authorized; paper / shadow not authorized; live-readiness not authorized; deployment not authorized; exchange-write not authorized; production-key creation not authorized; authenticated APIs not authorized; private endpoints not authorized; user stream not authorized; live WebSocket implementation not authorized.
- **N-VERDICT-LOCK** applies — no retained verdict revised (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1, C1, 5m thread closure all preserved verbatim); no project lock changed (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks all preserved verbatim).

Additional phase-specific boundary confirmations:

- No `.claude/settings.json`, `.claude/settings.local.json`, `.claude/hooks/`, or `.claude/agents/` file in `C:\Prometheus` modified or created.
- No `.mcp.json` created or modified.
- Local operator-side hook tooling (under `C:\ClaudeRuns\prometheus-light\.claude\...`) remains local and is not part of this commit; the standard's §8 records that authorising repo inclusion of hook files would require a separate process phase.
- No agent pack file or agent memory copied from `C:\Prometheus` into `C:\ClaudeRuns\prometheus-light`; the standard's §7 records that copying agent memory into the light workspace is not authorized by default.
- No `data/microstructure/` file modified, added, or deleted.
- No prior phase implementation report, closeout, or merge-closeout modified.
- No prior process standard modified beyond the five narrow cross-reference edits listed in §9.
- Phase 4bm-D project-complete status on `main` preserved verbatim.

---

## 13. Lifecycle and successor authorization

Phase 4bm-D-P1 is **branch-complete only** by this work. Per `docs/00-meta/process/phase-workflow-standard.md` it is **not project-complete** until a separately authorized merge phase records its merge-closeout on `main`.

Phase 4bm-D-P1 does **not** authorize:

- Phase 4bm-D-P1 merge phase (the merge itself requires a separately authorized merge prompt);
- Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision Memo);
- Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording);
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / any other Phase 4 successor;
- Phase 5 / Phase 4 canonical;
- features, labels, diagnostics, ML, strategy, backtests;
- additional data acquisition (additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book / spot / cross-venue / funding / open-interest);
- endpoint calls (public, authenticated, or private);
- WebSockets;
- user streams;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- credentials;
- `.env` creation or reading;
- `.mcp.json` creation or reading;
- MCP enablement;
- Graphify enablement;
- agents by default;
- copying Prometheus agent packs into the light workspace;
- copying Prometheus agent memory into the light workspace;
- modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual on-disk manifest;
- creation of any successor-state JSON;
- revision of any retained verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1, C1, 5m thread closure);
- modification of any project lock (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks);
- amendment of M0;
- amendment of Phase 4al refined no-rescue rule;
- amendment of Phase 4aw `flip_research_eligible(...)` always-raises invariant;
- amendment of Phase 4bb-F canonical path policy;
- amendment of Phase 4bl-F four-tier risk model or its R-SIDECAR-CRLF standing rule or its nine reusable non-authorization blocks;
- amendment of Phase 4bm-A-P1 thin-prompt context-management standard.

The recommended state after Phase 4bm-D-P1 is **remain paused**.

---

## 14. Recommended next step

**Operator review of the Phase 4bm-D-P1 new standard, the implementation report, and the closeout. After review — if accepted — a separately authorized Phase 4bm-D-P1 merge phase per the established `docs/00-meta/process/phase-workflow-standard.md` and `docs/00-meta/process/merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).**

After merge, the recommended state remains **remain paused** pending operator decision on the conditional Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision Memo) → Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording) ladder. Neither is authorized by Phase 4bm-D-P1.

---

## 15. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim by Phase 4bm-D-P1.

---

## 16. Preserved project locks (preserved verbatim)

- §11.6 = 8 bps per side
- Round-trip = 16 bps
- §1.7.3 = 0.25% risk / 2× leverage / one-position / mark-price stops
- Phase 3p §4.7 (strict integrity gate)
- Phase 3r §8 (mark-price gap governance)
- Phase 3v §8 (stop-trigger-domain governance)
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance)
- Phase 4j §11 (metrics OI-subset partial-eligibility rule)
- Phase 4k (V2 backtest-plan methodology)
- Phase 4p (G1 strategy spec)
- Phase 4q (G1 backtest-plan methodology)
- Phase 4v (C1 strategy spec)
- Phase 4w (C1 backtest-plan methodology)
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; never invoked)
- Phase 4bb-F canonical path policy
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; not invoked)
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard (cited; complemented by this phase, not amended)
- Phase 4am .. Phase 4bm-D results — all preserved verbatim.

All preserved verbatim by Phase 4bm-D-P1.

— end of Phase 4bm-D-P1 implementation report —