# Prometheus

Prometheus is a long-term research, systems-design, and implementation project for a production-oriented trading system.

The project is focused on building a robust, testable, operator-supervised trading bot for **Binance USDⓈ-M futures**, starting with a narrow rules-based v1 before any future AI-assisted or adaptive extensions are considered.

> Prometheus is not intended to start as a self-learning live AI trader. The first implementation is deliberately rules-based, tightly scoped, heavily documented, safety-first, and operator-supervised.

---

## Current Project Status

**Phase:** Claude Code Phase 0 readiness — repository audit and implementation-readiness review.

The repository has completed the main pre-implementation documentation and handoff layer.

Completed readiness items:

- core strategy, data, validation, execution, risk, architecture, operations, security, interface, and governance documentation,
- `docs/09-operations/first-run-setup-checklist.md`,
- `docs/00-meta/ai-coding-handoff.md`,
- `docs/00-meta/current-project-state.md`,
- Prometheus-specific Claude Code agent pack,
- root `CLAUDE.md`,
- `.claude/agents/` with the nine Prometheus project agents,
- `.claude/rules/` with Prometheus project rules,
- `.mcp.example.json` as an inert MCP template,
- `.mcp.graphify.template.json` as an inert Graphify placeholder.

The next implementation step is:

```text
Claude Code Phase 0 — Handoff Intake and Repo Audit
```

Phase 0 is an audit and readiness step. It is **not** broad implementation.

Claude Code must inspect the repository, read the required handoff documents, verify the current source/tooling/test/doc state, and produce a Phase 0 repository-audit report before Phase 1 is approved.

---

## Project Objective

Design and build a:

> **production-oriented, safety-first, operator-supervised trading system**

for:

- **Venue:** Binance USDⓈ-M futures
- **Initial live symbol:** BTCUSDT perpetual
- **Secondary research/comparison symbol:** ETHUSDT perpetual

The system is designed to be:

- initially **rules-based**,
- narrow before broad,
- robust before clever,
- supervised before autonomous,
- staged before live,
- and extensible only after the baseline system proves trustworthy.

---

## Locked V1 Direction

The following decisions are currently locked unless a later repository document explicitly revises them.

### Market and venue

- Binance USDⓈ-M futures
- BTCUSDT perpetual as the first live-capable symbol
- ETHUSDT perpetual as the first secondary research/comparison symbol
- BTCUSDT-only live scope for v1

### Strategy

- Strategy family: breakout continuation with higher-timeframe trend filter
- Signal timeframe: 15m
- Higher-timeframe bias: 1h
- Signal style: completed-bar confirmation only
- Entry style: market entry after confirmed signal bar close
- Baseline backtest fill assumption: next-bar open after confirmed signal close
- Stop model: structural stop + ATR buffer
- Trade management: staged risk reduction + trailing management

### Execution

- One-way mode
- Isolated margin
- One symbol first
- One position maximum in v1
- One active protective stop maximum in v1
- No pyramiding
- No reversal entry while positioned
- No hedge-mode behavior
- Exchange-side protective stop mandatory
- Protective stop uses:
  - `STOP_MARKET`
  - `closePosition=true`
  - `workingType=MARK_PRICE`
  - `priceProtect=TRUE`
- User stream is the primary live private-state source
- REST is used for placement, cancellation, reconciliation, and recovery
- Exchange state is authoritative
- Unknown execution outcomes fail closed
- No blind retry for exposure-changing actions

### Risk

- Initial live risk target: 0.25% of sizing equity per trade
- Initial effective leverage cap: 2x
- Internal notional cap is mandatory before live operation
- Leverage is a sizing tool, not a target
- Capital preservation takes priority over return optimization
- Future risk/leverage increases require evidence and explicit operator approval

### Deployment

The release path is staged:

```text
research -> validation -> dry-run -> paper/shadow -> tiny live -> scaled live
```

No stage should be skipped.

Tiny live is intended to run on a dedicated local NUC / mini PC with an attached monitor showing the operator dashboard during operation.

Production Binance trade-capable keys must not be created until the correct approved phase gate.

---

## Core Architecture Principles

Prometheus v1 is designed as a **modular monolith**.

That means one primary deployable runtime with strong internal module boundaries, not a premature distributed microservice system.

Core principles:

- Strategy and execution remain strictly separated.
- Strategy does not directly call Binance.
- Risk does not place orders.
- UI/dashboard does not bypass backend safety gates.
- Exchange state is authoritative for live position, order, and stop truth.
- Local runtime state exists for orchestration, restart, reconciliation, persistence, and operator continuity.
- Restart always begins in safe mode.
- Live trading may resume only after reconciliation restores state confidence.
- Runtime persistence stores restart-critical facts, not arbitrary convenience state.
- Observability is state-centric: exposure, protection, stream health, reconciliation, incidents, and operator action requirements matter most.
- The operator interface is part of the v1 safety boundary.
- The dashboard is a supervision/control surface, not a discretionary trading terminal.

---

## Repository Structure

Current documentation and support structure:

```text
docs/
  00-meta/                    current state, AI coding handoff, Claude agent pack
  01-foundations/             foundational concepts and project framing
  02-market-structure/        futures mechanics, fees, funding, leverage, liquidation
  03-strategy-research/       strategy selection and v1 breakout strategy design
  04-data/                    historical data, live data, timestamps, dataset versioning
  05-backtesting-validation/  backtesting principles and validation gates
  06-execution-exchange/      exchange/order handling and reconciliation concepts
  07-risk/                    risk philosophy and risk controls
  08-architecture/            implementation architecture and runtime design
  09-operations/              setup, restart, incident, operator, review, release processes
  10-security/                API keys, secrets, permission scoping, security policies
  11-interface/               dashboard and operator-control requirements
  12-roadmap/                 phase gates, technical debt, sequencing
  adr/                        architecture decision records
  glossary/                   shared definitions
  runbooks/                   operational procedures
  templates/                  reusable documentation templates

.claude/
  agents/                     Prometheus-specific Claude Code project agents
  rules/                      Prometheus-specific Claude Code rule imports
  settings.json               shared safe Claude Code settings
  settings.local.example.json local-only settings template

CLAUDE.md                     root Claude Code project memory/instructions
.mcp.example.json             inert MCP example template
.mcp.graphify.template.json   inert Graphify MCP placeholder
```

The planned implementation source tree is defined separately in:

```text
docs/08-architecture/codebase-structure.md
```

The expected future source layout starts with:

```text
src/prometheus/
```

and keeps live runtime, research/backtesting, exchange access, persistence, safety, and operator controls in separate modules.

---

## Source of Truth Policy

Markdown documents in this repository are the project’s primary source of truth.

If there is a conflict between older chat context and repository documentation:

1. detailed current Markdown docs win for their specialist domain,
2. `docs/00-meta/current-project-state.md` wins for high-level project status,
3. `docs/00-meta/ai-coding-handoff.md` wins for implementation method and Claude Code workflow,
4. `docs/12-roadmap/phase-gates.md` wins for promotion gates,
5. older chat memory and informal summaries are secondary.

Do not silently change locked decisions.

Surface conflicts first.

---

## Recommended Reading Order

For a human reviewer or AI implementation agent, start here:

```text
CLAUDE.md
docs/00-meta/current-project-state.md
docs/00-meta/ai-coding-handoff.md
docs/09-operations/first-run-setup-checklist.md
docs/00-meta/claude-agent-pack.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
```

Then review the implementation-critical documents:

```text
docs/03-strategy-research/first-strategy-comparison.md
docs/03-strategy-research/v1-breakout-strategy-spec.md
docs/03-strategy-research/v1-breakout-backtest-plan.md

docs/04-data/data-requirements.md
docs/04-data/historical-data-spec.md
docs/04-data/live-data-spec.md
docs/04-data/timestamp-policy.md
docs/04-data/dataset-versioning.md

docs/05-backtesting-validation/v1-breakout-validation-checklist.md

docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md
docs/06-execution-exchange/failure-recovery.md
docs/06-execution-exchange/position-state-model.md

docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/daily-loss-rules.md
docs/07-risk/drawdown-controls.md
docs/07-risk/kill-switches.md

docs/08-architecture/implementation-blueprint.md
docs/08-architecture/codebase-structure.md
docs/08-architecture/state-model.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/database-design.md
docs/08-architecture/observability-design.md
docs/08-architecture/event-flows.md
docs/08-architecture/deployment-model.md

docs/09-operations/restart-procedure.md
docs/09-operations/incident-response.md
docs/09-operations/operator-workflow.md
docs/09-operations/daily-weekly-review-process.md
docs/09-operations/release-process.md
docs/09-operations/rollback-procedure.md

docs/10-security/api-key-policy.md
docs/10-security/secrets-management.md
docs/10-security/permission-scoping.md
docs/10-security/audit-logging.md
docs/10-security/host-hardening.md
docs/10-security/disaster-recovery.md

docs/11-interface/operator-dashboard-requirements.md
docs/11-interface/manual-control-actions.md
docs/11-interface/approval-workflows.md
docs/11-interface/dashboard-metrics.md
docs/11-interface/alerting-ui.md
```

---

## Claude Code Handoff

Claude Code implementation must begin with:

```text
docs/00-meta/ai-coding-handoff.md
```

That document defines:

- repository reading order,
- authority hierarchy,
- locked v1 decisions,
- non-negotiable safety constraints,
- forbidden implementation actions,
- phased implementation plan,
- runnable checkpoints,
- acceptance criteria per phase,
- installation authority,
- ChatGPT escalation protocol,
- checkpoint reporting protocol,
- ambiguity/spec-gap protocol,
- local development first / NUC later approach,
- migration-to-NUC expectations,
- and the initial Claude Code prompt.

Claude Code must start with:

```text
Phase 0 — Handoff Intake and Repo Audit
```

Phase 0 is an audit/review step, not broad implementation.

---

## Claude Agent Pack

Prometheus includes a project-specific Claude Code agent pack.

The pack is documented in:

```text
docs/00-meta/claude-agent-pack.md
```

Project agents live in:

```text
.claude/agents/
```

Current Prometheus agents:

```text
prometheus-orchestrator
prometheus-safety-guardian
prometheus-spec-architect
prometheus-data-validation-engineer
prometheus-strategy-backtest-engineer
prometheus-risk-state-engineer
prometheus-execution-simulation-engineer
prometheus-dashboard-alerts-engineer
prometheus-test-verification-engineer
```

Recommended first agents:

```text
prometheus-orchestrator
prometheus-safety-guardian
prometheus-spec-architect
prometheus-test-verification-engineer
```

The agent pack strengthens Claude Code during phased implementation. It does not replace the AI coding handoff, phase gates, specialist docs, or operator approval.

---

## MCP and Graphify Status

Prometheus includes MCP templates only:

```text
.mcp.example.json
.mcp.graphify.template.json
```

Current intended status:

- `.mcp.example.json` is a tracked inert template.
- `.mcp.graphify.template.json` is a tracked inert placeholder.
- `.mcp.json` should remain local-only and gitignored if created later.
- MCP servers are not required before Phase 0.
- Graphify is optional and should not be enabled until installation and secret-exclusion rules are verified.

Recommended early MCP candidates, when approved:

- `filesystem-prometheus`, scoped only to `C:/Prometheus`,
- `context7`, for library documentation,
- `playwright`, later for dashboard testing.

Do not configure:

- ERP/JAF MCP servers,
- company MySQL/MariaDB MCP servers,
- Laravel MCP servers,
- Phoenix theme MCP servers,
- Figma tokens,
- plaintext credentials,
- Binance production write tools.

---

## Setup and Operator Workflow

The practical setup path is defined in:

```text
docs/09-operations/first-run-setup-checklist.md
```

The intended workflow is:

```text
Claude Code = implementation executor inside repo
ChatGPT = setup/review/debugging/documentation guide
Operator = approval authority and physical/system operator
```

Current operator environment:

```text
Local repo path: C:\Prometheus
GitHub Desktop: repository tracking
AntiGravity IDE: repository open
Claude Code extension: installed and logged in
ChatGPT: setup/debug/checkpoint review partner
```

Claude Code may install project/phase-required dependencies when safe.

If installation or setup requires unclear system-level action, admin privileges, external account setup, security-sensitive configuration, Binance credentials, Telegram/n8n setup, NUC host changes, or anything outside the approved phase, Claude Code must stop and produce the ChatGPT setup escalation prompt defined in the handoff.

---

## Implementation Order

Implementation must be phased.

Expected high-level order:

```text
0. repo audit and Phase 1 plan
1. local development foundation
2. historical data and validation foundation
3. backtesting and strategy conformance
4. risk, state, and persistence runtime
5. dashboard, observability, and alerts
6. dry-run exchange simulation
7. paper/shadow operation
8. tiny-live preparation
9. scaled-live preparation
```

Execution-layer and real exchange-write capability come late.

No production exchange-write capability should exist before dry-run, paper/shadow, security, host, and phase-gate evidence justify it.

---

## Non-Goals for V1

The first live-capable version should not include:

- autonomous self-learning live trading,
- machine-learning-driven live decisions,
- multi-symbol portfolio execution,
- hedge mode,
- multi-venue routing,
- order-book or tick-level execution optimization,
- fully unattended lights-out operation,
- large indicator stacks,
- discretionary pattern interpretation,
- arbitrary manual buy/sell buttons,
- click-to-trade behavior,
- manual pyramiding,
- manual reversal,
- manual stop widening,
- or premature distributed infrastructure.

The goal is not to get a bot trading as quickly as possible.

The goal is to build a system that can eventually be trusted with real capital under strict supervision.

---

## Safety and Security Rules

Hard project rules:

- Never commit secrets.
- Never place API keys or secrets in docs, code, logs, screenshots, prompts, chats, database rows, or test snapshots.
- Production API keys must have no withdrawal permission.
- Production API keys must use IP restriction where practical.
- Development, paper/shadow, and production credentials must remain separate.
- If credentials are missing, invalid, or unauthorized, the bot must fail closed.
- If exchange/local state is uncertain, the bot must block new entries.
- If a position exists without confirmed protective stop coverage, the system is in an emergency state.
- Kill switch state must persist across restart.
- Kill switch must never auto-clear.
- Unknown execution outcomes fail closed.
- No blind retry for exposure-changing actions.

---

## Local Development and NUC Path

Initial development can happen on the laptop/desktop.

The expected path is:

```text
Laptop/desktop development
→ local tests
→ data/backtest work
→ fake adapter dry-run
→ dashboard prototype
→ GitHub commits
→ NUC preparation
→ clone repo on NUC
→ install from lockfiles
→ run tests on NUC
→ run dry-run on NUC
→ dashboard on NUC monitor
→ paper/shadow
→ tiny live only after approval
```

Tiny live should run on the dedicated local NUC / mini PC after host hardening, dashboard, alerts, runtime persistence, backup/restore, secrets, emergency access, safe-mode restart, and phase-gate requirements are satisfied.

---

## Current Next Step

Run Claude Code Phase 0 only:

```text
Phase 0 — Handoff Intake and Repo Audit
```

Claude Code should produce a report covering:

- current branch,
- working tree status,
- repository layout,
- documentation status,
- source-code status,
- package/tooling status,
- test status,
- existing configuration status,
- agent-pack status,
- MCP status,
- missing or stale files,
- immediate blockers,
- safety concerns,
- proposed Phase 1 plan,
- recommended commands for Phase 1,
- questions for operator/ChatGPT.

Claude Code must stop after the Phase 0 report and wait for operator approval.

---

## Disclaimer

This repository is for research, architecture, and software-system design.

Nothing in this repository is financial advice. Trading leveraged crypto futures is high risk and can result in rapid loss of capital. The project explicitly prioritizes risk control, validation, and operational safety because profitability is uncertain and must never be assumed from design alone.

---

## Document Status

- Status: active
- Project phase: Claude Code Phase 0 readiness
- Initial live scope: BTCUSDT perpetual on Binance USDⓈ-M futures
- Last updated: 2026-04-19
