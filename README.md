# Prometheus

Prometheus is a long-term research, systems-design, and implementation-planning project for a production-oriented trading system.

The project is focused on designing and implementing a robust, testable, operator-supervised trading bot for **Binance USDⓈ-M futures**, starting with a narrow rules-based v1 before any future AI-assisted or adaptive extensions are considered.

> Prometheus is not intended to start as a self-learning live AI trader. The first implementation is deliberately rules-based, tightly scoped, heavily documented, and safety-first.

---

## Current Project Status

**Phase:** Claude Code handoff readiness / Phase 0 implementation intake.

The repository is still primarily a documentation and architecture repository, but the core pre-implementation handoff layer is now in place.

The current focus is on:

- preserving the locked v1 trading scope,
- using the repository Markdown files as the source of truth,
- handing Claude Code a strict phased implementation contract,
- starting with a repo audit before broad code generation,
- guiding installations and setup through Claude Code + ChatGPT + operator review,
- and keeping live-capital safety constraints explicit before implementation.

The next implementation step is:

```text
Claude Code Phase 0 — Handoff Intake and Repo Audit
```

Broad code generation should not begin until Phase 0 is completed and reviewed.

---

## Project Objective

Design and eventually build a:

> **production-oriented, safety-first, operator-supervised trading system**

for:

- **Venue:** Binance USDⓈ-M futures
- **Initial symbol:** BTCUSDT perpetual
- **Secondary research comparison:** ETHUSDT perpetual

The system is designed to be:

- initially **rules-based**,
- narrow before broad,
- robust before clever,
- supervised before autonomous,
- and extensible only after the baseline system proves trustworthy.

---

## Locked V1 Direction

The following decisions are currently locked unless a later document explicitly revises them.

### Market and venue

- Binance USDⓈ-M futures
- BTCUSDT perpetual as the first live-capable symbol
- ETHUSDT perpetual as the first secondary research comparison
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
- Exchange-side protective stop mandatory
- Protective stop uses `STOP_MARKET`, `closePosition=true`, `workingType=MARK_PRICE`, `priceProtect=TRUE`
- User stream is the primary live private-state source
- REST is used for placement, cancellation, reconciliation, and recovery
- Exchange state is authoritative

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

Current documentation structure:

```text
docs/
  00-meta/                   project objective, scope, current state, AI handoff
  01-foundations/            foundational concepts and project framing
  02-market-structure/       futures mechanics, fees, funding, leverage, liquidation
  03-strategy-research/      strategy selection and v1 breakout strategy design
  04-data/                   historical data, live data, timestamps, dataset versioning
  05-backtesting-validation/ backtesting principles and validation gates
  06-execution-exchange/     exchange/order handling and reconciliation concepts
  07-risk/                   risk philosophy and risk controls
  08-architecture/           implementation architecture and runtime design
  09-operations/             setup, restart, incident, operator, review, release processes
  10-security/               API keys, secrets, permission scoping, security policies
  11-interface/              dashboard and operator-control requirements
  12-roadmap/                phase gates, technical debt, sequencing
  adr/                       architecture decision records
  glossary/                  shared definitions
  runbooks/                  operational procedures
  templates/                 reusable documentation templates
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

1. detailed current Markdown docs win,
2. then `docs/00-meta/current-project-state.md`,
3. then older project chat memory,
4. then informal summaries.

Do not silently change locked decisions.

Surface conflicts first.

---

## Recommended Reading Order

For a human reviewer or AI implementation agent, start here:

```text
docs/00-meta/current-project-state.md
docs/00-meta/ai-coding-handoff.md
docs/09-operations/first-run-setup-checklist.md
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

## AI Coding Handoff

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

The operator already has the repo cloned locally at:

```text
C:\Prometheus
```

and is using:

- GitHub Desktop for repository tracking,
- AntiGravity IDE,
- Claude Code extension logged into a Max plan account,
- ChatGPT for guided setup review, screenshots, logs, errors, and checkpoint interpretation.

Claude Code may install project/phase-required dependencies when safe.

If installation or setup requires unclear system-level action, admin privileges, external account setup, security-sensitive configuration, Binance credentials, Telegram/n8n setup, NUC host changes, or anything outside the approved phase, Claude Code must stop and produce the ChatGPT setup escalation prompt defined in the handoff.

---

## Implementation Handoff Status

The project is ready for Claude Code Phase 0 repository audit.

Created handoff/setup documents:

```text
docs/00-meta/ai-coding-handoff.md
docs/09-operations/first-run-setup-checklist.md
```

Implementation must be phased.

The expected high-level implementation order is:

```text
1. repo audit and Phase 1 plan
2. local development foundation
3. historical data and validation foundation
4. backtesting and strategy conformance
5. risk, state, and persistence runtime
6. dashboard, observability, and alerts
7. dry-run exchange simulation
8. paper/shadow operation
9. tiny-live preparation
10. scaled-live preparation
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
- Never place API keys or secrets in docs, code, logs, screenshots, or chats.
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

## Disclaimer

This repository is for research, architecture, and software-system design.

Nothing in this repository is financial advice. Trading leveraged crypto futures is high risk and can result in rapid loss of capital. The project explicitly prioritizes risk control, validation, and operational safety because profitability is uncertain and must never be assumed from design alone.

---

## Document Status

- Status: active
- Project phase: Claude Code handoff readiness / Phase 0 implementation intake
- Initial live scope: BTCUSDT perpetual on Binance USDⓈ-M futures
- Last updated: 2026-04-18
