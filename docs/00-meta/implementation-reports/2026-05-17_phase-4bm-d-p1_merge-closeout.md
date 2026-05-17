# Phase 4bm-D-P1 Merge Closeout

## §1 Phase Identity

- **Phase**: Phase 4bm-D-P1 — Lightweight Claude Code Workspace Execution Standard
- **Tier**: Tier 1 (docs-only Full Phase; process / workflow standardization)
- **Type**: docs-only process standardization — adds one new repo-resident process standard, narrow cross-references in five existing process standards, the standard pair of implementation report + closeout, and a narrow `current-project-state.md` update
- **Action**: merge into `main`
- **Merge purpose**: record Phase 4bm-D-P1 as project-complete on `main` after a clean docs-only branch that formalises the lightweight Claude Code workspace pattern as the recommended default for heavy Prometheus Claude Code execution sessions, preserving every retained verdict, every project lock, every on-disk manifest, and every prior governance artefact byte-for-byte
- **Branch merged**: `phase-4bm-d-p1/lightweight-claude-workspace-standard`
- **Target branch**: `main`
- **Base**: `main` at `59e3e6cdca4996289e26e12b4b68d96615728702` (Phase 4bm-D merge-closeout commit)
- **Predecessor**: Phase 4bm-D (Multi-Day Derived-Family Eligibility Gate, project-complete on `main`)

Per `docs/00-meta/process/phase-workflow-standard.md`, **Phase 4bm-D-P1 is project-complete only after this merge + merge-closeout commit on `main`**.

## §2 SHAs

- **Pre-merge `main` SHA**: `59e3e6cdca4996289e26e12b4b68d96615728702`
- **Pre-merge `origin/main` SHA**: `59e3e6cdca4996289e26e12b4b68d96615728702` (in sync)
- **Phase 4bm-D-P1 branch docs commit SHA**: `055a6709e40130421dc3577454a2d0ff78344195` (`docs(phase-4bm-d-p1): add lightweight claude workspace standard`; 9 files / +1,474 / -0; single commit on branch)
- **Phase 4bm-D-P1 branch tip SHA pre-merge**: `055a6709e40130421dc3577454a2d0ff78344195`
- **Merge commit SHA**: `3ddad0288fcaf0391a5f73c34872a89d8c1e51ee`
- **Merge commit message**: `docs(phase-4bm-d-p1): merge lightweight claude workspace standard`
- **Merge-closeout commit SHA**: recorded by the commit's `git log` entry; final post-commit `git rev-parse HEAD` is the canonical value (this closeout commit is the next commit on `main`).
- **Post-merge `main` / `origin/main` SHA after merge-closeout commit + push**: recorded by §17 of the final operator report (final `git rev-parse main` / `git rev-parse origin/main` values).

## §3 Merge Method

- **Command**: `git merge --no-ff phase-4bm-d-p1/lightweight-claude-workspace-standard -m "docs(phase-4bm-d-p1): merge lightweight claude workspace standard"`
- **Strategy**: `ort` (git default; reported by git as `Merge made by the 'ort' strategy.`)
- **Conflicts**: none
- **Hooks**: not skipped (no `--no-verify`)
- **Signing**: not skipped (no `--no-gpg-sign`)
- **Force**: not used
- **Push status**: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing (recorded in §17 of the final operator report).

## §4 Files Brought Forward by the Merge

Nine tracked files brought forward from the Phase 4bm-D-P1 branch into `main`, all from the single source-branch commit (`055a670`).

**Tracked files added (3):**

1. `docs/00-meta/process/claude-code-lightweight-workspace-standard.md` (NEW, +611; 16-section process standard formalising the lightweight Claude Code workspace pattern)
2. `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-d-p1_lightweight-claude-code-workspace-standard.md` (NEW, +305; 16-section implementation report)
3. `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-d-p1_closeout.md` (NEW, +162; 14-section closeout)

**Tracked files modified narrowly (6):**

4. `docs/00-meta/process/claude-code-context-management-standard.md` (MODIFIED, +8; one bullet added in "Required references for future chats" pointing at the new standard)
5. `docs/00-meta/process/phase-prompt-template.md` (MODIFIED, +14; one bullet added in "Prompt design principles" directing heavy-execution prompts to include the lightweight workspace fields)
6. `docs/00-meta/process/chat-branching-handoff-standard.md` (MODIFIED, +14; one paragraph appended to "Thin handoff style" for heavy-execution-continuation handoffs)
7. `docs/00-meta/process/operator-report-standard.md` (MODIFIED, +15; one paragraph appended to "Thin contractual prompts" for ChatGPT-drafted heavy-execution prompts)
8. `docs/00-meta/process/phase-workflow-standard.md` (MODIFIED, +9; one bullet added in "Required references for future chats")
9. `docs/00-meta/current-project-state.md` (MODIFIED, +336 / -0; Phase 4bm-D-P1 narrative paragraph + new "Current phase:" block; prior Phase 4bm-D "Current phase:" block preserved verbatim as labelled historical context)

**This merge-closeout commit — 1 additional tracked file (allowed by the operator authorization for the merge phase):**

10. `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-d-p1_merge-closeout.md` (NEW; this file)

**Explicit non-changes:** No `data/microstructure/` file was modified, added, or deleted. No `data/research/` file was committed. No prior `src/prometheus/` module was modified. No prior `tests/` file was modified. No `scripts/` script was modified. No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, MCP file (`.mcp.json` absent before and after), or `.claude/settings.json` / `.claude/settings.local.json` / `.claude/hooks/` / `.claude/agents/` file in `C:\Prometheus` was modified or created. No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph addition. No prior implementation report, closeout, or merge-closeout was modified. No prior process standard was modified beyond the five narrow cross-reference edits listed in §4 above.

## §5 Diff Summary

```text
 docs/00-meta/current-project-state.md              | 336 +++++++++++
 .../2026-05-17_phase-4bm-d-p1_closeout.md          | 162 ++++++
 ...1_lightweight-claude-code-workspace-standard.md | 305 ++++++++++
 .../process/chat-branching-handoff-standard.md     |  14 +
 .../claude-code-context-management-standard.md     |   8 +
 .../claude-code-lightweight-workspace-standard.md  | 611 +++++++++++++++++++++
 docs/00-meta/process/operator-report-standard.md   |  15 +
 docs/00-meta/process/phase-prompt-template.md      |  14 +
 docs/00-meta/process/phase-workflow-standard.md    |   9 +
 9 files changed, 1474 insertions(+)
```

- 9 files changed
- 1,474 insertions
- 0 deletions
- The merge diff exactly matches the expected change set from the authorization prompt (3 added + 6 modified = 9 tracked files; no `data/microstructure/` files).
- `git diff --check` clean (no whitespace errors; no unresolved merge markers).

## §6 Result / Verdict

**PROCESS STANDARDIZATION COMPLETE — Phase 4bm-D-P1 lightweight Claude Code workspace standard recorded on `main`; Phase 4bm-D-P1 is project-complete on `main`.**

Phase 4bm-D-P1 formalises the lightweight Claude Code workspace pattern as the recommended default for heavy Prometheus Claude Code execution sessions: launch Claude Code from a lightweight workspace at `C:\ClaudeRuns\prometheus-light` while accessing the real repository explicitly at `C:\Prometheus`, with every shell command using the `cd C:\Prometheus && <command>` convention. The new standard at `docs/00-meta/process/claude-code-lightweight-workspace-standard.md` is 16 sections covering: purpose, authority, core principle, standard workspace layout, recommended launch command (including session-local `$env:CLAUDE_CODE_DISABLE_CLAUDE_MDS="1"` and `$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY="1"` plus `claude --add-dir C:\Prometheus`), IDE / Antigravity guidance, default-off agent and memory policy, optional local-hooks posture, session slicing, prompt format under the light workspace, when-to-use rules, relationship to existing process docs, comprehensive non-authorizations, required references for future chats, change-control process, and final note. The standard complements, but does not replace, Phase 4bm-A-P1 (`claude-code-context-management-standard.md`): Phase 4bm-A-P1 governs **what goes into the prompt and what gets read**; Phase 4bm-D-P1 governs **where the Claude Code session is launched from and what auto-context the harness inherits at session start**. Both disciplines apply together to heavy execution sessions. Phase 4bm-D-P1 is now project-complete on `main`. **Phase 4bm-D-P1 does not authorize Phase 4bm-E, Phase 4bm-F, any other successor, MCP, Graphify, agents-by-default, copying Prometheus agent packs or agent memory into the light workspace, or any change to any on-disk manifest.**

## §7 Local Gitignored Outputs

**None.** Phase 4bm-D-P1 is docs-only and produced no local gitignored artefacts. No file under `data/microstructure/`, `data/research/`, or any other local gitignored namespace was created, modified, or deleted by the source branch or by this merge-closeout commit. Local operator-side hook tooling under `C:\ClaudeRuns\prometheus-light\.claude\...` remains local to the lightweight workspace and is not part of `C:\Prometheus`; the new standard's §8 explicitly classifies hook files as local operator tooling that must not be committed unless a separately authorized process phase authorizes repo inclusion.

## §8 Validation Results

### Pre-merge (on Phase 4bm-D-P1 branch tip `055a670`)

- `git status --short`: clean (only the pre-existing untracked `.claude/scheduled_tasks.lock` and `data/research/`).
- `git diff --check`: clean.
- `git rev-parse main`: `59e3e6cdca4996289e26e12b4b68d96615728702`.
- `git rev-parse origin/main`: `59e3e6cdca4996289e26e12b4b68d96615728702` (`main == origin/main` in sync).
- `git rev-parse phase-4bm-d-p1/lightweight-claude-workspace-standard`: `055a6709e40130421dc3577454a2d0ff78344195`.
- `git rev-parse --verify origin/phase-4bm-d-p1/lightweight-claude-workspace-standard`: NO_ORIGIN_BRANCH (source branch was not pushed to origin; this is expected and does not invalidate the merge).
- `git diff --name-status main...phase-4bm-d-p1/lightweight-claude-workspace-standard`: 9 files (3 `A` + 6 `M`) matching §4.
- `git diff --stat main...phase-4bm-d-p1/lightweight-claude-workspace-standard`: 9 files / +1,474 insertions / 0 deletions (matches expected).

### Checkout main + pull

- `git checkout main`: Switched to branch 'main'.
- `git pull --ff-only`: Already up to date.
- `git status --short` on main pre-merge: only the two pre-existing untracked entries.

### Merge command output

- `git merge --no-ff phase-4bm-d-p1/lightweight-claude-workspace-standard -m "docs(phase-4bm-d-p1): merge lightweight claude workspace standard"`: `Merge made by the 'ort' strategy.`
- Files: 9 files changed, 1,474 insertions(+), 0 deletions(-).
- Conflicts: none.
- Merge commit SHA: `3ddad0288fcaf0391a5f73c34872a89d8c1e51ee`.

### Post-merge (on `main` after the merge commit)

- `git diff --check` (post-merge): clean — exit code 0 (no whitespace errors, no unresolved markers).
- `git status --short` (post-merge, pre-closeout-commit): only the two pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`).
- `git log --oneline -5 --decorate` (post-merge, pre-closeout-commit):
  ```text
  3ddad02 (HEAD -> main) docs(phase-4bm-d-p1): merge lightweight claude workspace standard
  055a670 (phase-4bm-d-p1/lightweight-claude-workspace-standard) docs(phase-4bm-d-p1): add lightweight claude workspace standard
  59e3e6c (origin/main, origin/HEAD) docs(phase-4bm-d): add merge closeout
  a80b8a0 docs(phase-4bm-d): merge multi-day derived family eligibility gate
  71ec483 (origin/phase-4bm-d/multi-day-derived-family-eligibility-gate, phase-4bm-d/multi-day-derived-family-eligibility-gate) docs(phase-4bm-d): add gate report and closeout
  ```

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by this merge phase. Per the operator authorization: "Do not run ruff, mypy, or pytest unless source/tests/scripts/config files were unexpectedly modified." No source / test / script / configuration file is modified by the source branch or by this merge-closeout commit, so the rule applies. The most recent authoritative whole-repo `pytest` baseline remains the Phase 4bm-B merge baseline (`1156 passed, 1 skipped`; two pre-existing `KeyError: 'trade_count'` simulation failures on `tests/simulation/test_backtest_real_2026_03.py` in `src/prometheus/research/data/storage.py:232` are unrelated to Phase 4bm-D-P1 and are preserved as the baseline). Phase 4bm-D-P1 introduces zero new regressions vs that baseline because no source / test is modified.

### Gitignore policy verification

- `git check-ignore -v data/microstructure/`: `.gitignore:85: data/microstructure/` (pre-existing rule, unchanged).
- No new gitignored paths were introduced by Phase 4bm-D-P1.

## §9 Upstream Immutability Evidence

Phase 4bm-D-P1 is a docs-only process-standardization phase. It does not read, hash, or write any `data/microstructure/` artefact. Every prior local artefact under `data/microstructure/` (the 90 v002 raw zips and sidecars, the v002 raw manifest and sidecar, the v002 acquisition log and sidecar, the Phase 4bl-D-R gate report and sidecar, the Phase 4bl-E successor-state record and sidecar, the Phase 4bm-B v002 derived multi-day index manifest and sidecar, the 90 Phase 4bm-B v002 per-day Parquets and 90 sidecars, the Phase 4bm-D authoritative gate report and sidecar, the Phase 4bd v001 derived parquet and manifest, the Phase 4bf v001 derived gate report, the Phase 4bg-B successor-state, the Phase 4bh feature parquet and manifest, the Phase 4bj-C label parquet and manifest, every prior gate report and successor-state artefact) is byte-identical pre- and post-Phase-4bm-D-P1 by construction: no file under `data/microstructure/` is read, hashed, written, deleted, or otherwise touched by the source branch or by this merge-closeout commit. Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved end-to-end (never invoked).

## §10 Manifest State Preservation

- **v002 derived multi-day index manifest** (`microstructure_normalized_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged.
- **v002 raw manifest** (`microstructure_raw_aggtrades_v001__v002.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged.
- **Phase 4bd v001 derived manifest** (`microstructure_normalized_aggtrades_v001__v001.json`): `research_eligible = false`; `eligibility_gate_status = "pending"`. Unchanged.
- **Every other manifest** under `data/microstructure/manifests/` and `data/manifests/`: unchanged.

No `research_eligible` flip occurred. No `eligibility_gate_status` transition occurred on any actual on-disk manifest. No `chronological_split_policy` change occurred on any actual manifest. No path exists in this phase to mutate any manifest: Phase 4bm-D-P1 is docs-only and writes no code that touches manifests.

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## §11 Boundary Confirmations

The Phase 4bm-D-P1 merge honours every relevant boundary. Citing the canonical reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 by name, plus phase-specific additions:

- **N-ACQUISITION** applies — no acquisition; no download; no extension of any existing dataset; no creation or modification of raw data files.
- **N-ENDPOINT** applies — no Binance / public / authenticated / private endpoint called; no `data.binance.vision` contact; no WebSocket opened.
- **N-CREDENTIALS** applies — no credential used, read, created, or referenced; `.env` not read or created; `.mcp.json` not read or created; MCP / Graphify not enabled; no order placed; no exchange-write surface contacted.
- **N-MANIFEST** applies — no actual manifest file modified; no `research_eligible` flip; no `eligibility_gate_status` transition; no `chronological_split_policy` change; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- **N-GATE-RERUN** applies — no raw / derived / feature / label / metrics gate rerun; no new gate report generated.
- **N-SUCCESSOR-STATE** applies — no successor-state artefact created or modified.
- **N-DERIVATION** applies — no normalization, derivation, feature, or label computation; no kernel run; no derived / feature / label parquet produced.
- **N-DIAGNOSTICS-ML-STRATEGY** applies — no diagnostics, ML, strategy, signal construction, or backtest; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit output.
- **N-PHASE-5** applies — no Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.
- **N-VERDICT-LOCK** applies — no retained verdict revised (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1, C1, 5m thread closure all preserved verbatim); no project lock changed (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks all preserved verbatim).

Additional merge-level confirmations:

- no `data/microstructure/` file committed by either the source-branch commit or this merge-closeout commit
- no prior source / test / script modified by either commit
- no `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or MCP file modified
- no `.mcp.json` created
- no `.claude/settings.json` / `.claude/settings.local.json` / `.claude/hooks/` / `.claude/agents/` file in `C:\Prometheus` modified or created (local operator-side hook tooling lives under `C:\ClaudeRuns\prometheus-light\.claude\...` and is not part of this commit; the new standard's §8 records that authorising repo inclusion of hook files would require a separate process phase)
- no prior governance memo modified beyond the narrow `current-project-state.md` paragraph addition
- no prior phase implementation report, closeout, or merge-closeout modified
- no prior process standard modified beyond the five narrow cross-reference edits listed in §4
- no gate rerun (no gate kernel invoked)
- no acquisition; no endpoint contacted; no WebSocket opened; no credential used; no `.env` / `.mcp.json` read or created; MCP / Graphify not enabled
- no features / labels / signals / proxies / ML / strategy / backtest output computed
- no successor-state JSON created
- agents and project memory remain default-off for heavy light-workspace execution sessions (per the new standard's §7)
- local hooks remain local operator tooling unless separately authorized (per the new standard's §8); no agent pack or agent memory copied from `C:\Prometheus` into `C:\ClaudeRuns\prometheus-light`
- no retained verdict revised; no project lock loosened; no M0 amendment; no Phase 4al rule amended; no Phase 4aw invariant amended; no Phase 4bb-F canonical path policy amended; no Phase 4bl-F rule amended; no Phase 4bm-A-P1 standard amended (complemented, not amended, by Phase 4bm-D-P1)
- no successor authorized (Phase 4bm-E / Phase 4bm-F / Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / Phase 5 / Phase 4 canonical all remain unauthorized)
- merge command was a clean `git merge --no-ff` with `ort` strategy, no conflicts, no `--no-verify`, no `--no-gpg-sign`, no force-push

## §12 Retained Verdict Ledger

All preserved verbatim:

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

All preserved verbatim by Phase 4bm-D-P1 and by this merge.

## §13 Preserved Project Locks

All preserved verbatim:

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
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; not invoked — Phase 4bm-D-P1 introduces no new sidecars)
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard (cited; complemented by Phase 4bm-D-P1, not amended)
- Phase 4am .. Phase 4bm-D results — all preserved verbatim

## §14 No-Rescue Constraints

The Phase 4bm-D-P1 merge records a docs-only process / workflow standardization that formalises the lightweight Claude Code workspace pattern. The standard is operational discipline for Claude Code execution sessions. It does NOT, and CANNOT, be construed as authorising:

- ML model training, model selection, strategy hypothesis generation, signal construction, or any conversion of evidence into trading signals
- strategy logic, position state, entry / exit rules, or backtest design
- paper / shadow / live-readiness / deployment / exchange-write work
- Phase 4 canonical or Phase 5 authorisation
- transitioning any manifest's `research_eligible` flag from `false` to `true` from this evidence alone
- transitioning any manifest's `eligibility_gate_status` from `"pending"` to anything else on disk
- transitioning any manifest's `chronological_split_policy`
- creating any successor-state JSON (Phase 4bm-F would require a separately authorized phase)
- creating a Phase 4bm-E research-eligibility decision memo (requires a separately authorized phase)
- features, labels, diagnostics, ML, strategy, or backtests
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- old-strategy alt-symbol rerun or cooled-down-family reopening
- 5m research-thread reopening (Phase 3t closure preserved)
- revising or weakening any retained verdict (R2 / F1 / D1-A / V2 / G1 / C1 first-specs remain terminally rejected as recorded; H0 framework anchor, R3 baseline-of-record, and R1a / R1b-narrow retained-non-leading status all preserved)
- cross-strategy hybrids (V1-D1, F1-D1, V2-G1, G1-C1, or any other combination)
- -prime, -narrow, -extension, or -hybrid variants of any historical candidate
- §11.6 cost-realism relaxation, §1.7.3 risk / leverage / one-position / mark-price stop amendment, or any other lock loosening
- M0 amendment, post-null cooldown weakening, cooled-down families list shortening, or memo template alteration
- use of Phase 4l V2 forensic numbers, Phase 4r G1 forensic numbers, or Phase 4x C1 forensic numbers as parameter-selection inputs
- use of 5m Q1–Q7 diagnostic outputs as rule-input candidates
- MCP / Graphify / `.mcp.json` / credential enablement
- copying Prometheus agent packs or agent memory into the lightweight workspace at `C:\ClaudeRuns\prometheus-light`
- enabling agents-by-default for heavy execution sessions
- committing local hook files from the lightweight workspace into `C:\Prometheus` without a separately authorized process phase
- amending the Phase 4bm-A-P1 thin-prompt Claude Code context-management standard (Phase 4bm-D-P1 complements it; does not amend it)
- public-endpoint code calls, user-stream implementation, live WebSocket implementation, or any authenticated-API / private-endpoint access

The lightweight Claude Code workspace standard is necessary operational discipline for heavy Claude Code execution sessions; it is not sufficient evidence for any of the above. Each future technical phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight workspace standard, and the merge-closeout standard.

## §15 Successor Authorization

**None.**

This merge-closeout records that Phase 4bm-D-P1 is project-complete on `main`. It does **not** authorize:

- Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo
- Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / any other Phase 4 successor
- Phase 5 / Phase 4 canonical
- Paper / shadow / live-readiness / deployment / exchange-write
- Production-key creation / authenticated APIs / private endpoints
- User-stream / live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credential work
- Any additional aggTrades / 5m / 1m / tick / mark-price / order-book / cross-venue data acquisition beyond the 90 locked BTCUSDT UTC dates 2024-12-01 .. 2025-02-28
- ML implementation, model selection, feature ranking, meta-labeling
- Strategy implementation, signal construction, backtest implementation
- Any modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual on-disk manifest
- Any successor-state JSON creation
- Agents-by-default for heavy Claude Code execution sessions
- Copying Prometheus agent packs or agent memory into `C:\ClaudeRuns\prometheus-light`
- Committing local hook files from the lightweight workspace into `C:\Prometheus`

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.

## §16 Recommended State

**Remain paused.**

Phase 4bm-D-P1 is now project-complete on `main` (this merge-closeout records the lifecycle anchor). The lightweight Claude Code workspace pattern is now the recommended default for heavy Prometheus Claude Code execution sessions. The operator's broader pause decision continues to apply.

**Conditional next, NOT authorized:**

Future operator-authorized **Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo** would be the natural next step in the v002 lifecycle ladder by precedent of Phase 4bg-A (research-eligibility decision for the Phase 4bd v001 derived family). Phase 4bm-E would evaluate whether the v002 derived family is admissible in principle for a future Stage-3 research-eligibility transition given the completed Stage-0 (Phase 4bm-B), report-level Stage-1 / Stage-2 (Phase 4bm-C structural QA PASS + Phase 4bm-D `DERIVED_GATE_PASS`) evidence, and emit a docs-only decision memo. Phase 4bm-E is **not** authorised by this merge-closeout.

After any Phase 4bm-E merge, the recommended state would remain **remain paused** pending operator decision on the further conditional **Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording** ladder step (by precedent of Phase 4bg-B for the v001 derived family). Phase 4bm-F is **not** authorised by this merge-closeout.

— end of Phase 4bm-D-P1 merge-closeout —
