# Prometheus

Prometheus is a long-term research, systems-design, and implementation-planning project for a production-oriented trading system.

The project is currently focused on designing a robust, testable, operator-supervised trading bot for **Binance USDⓈ-M futures**, starting with a narrow rules-based v1 before any future AI-assisted or adaptive extensions are considered.

> Prometheus is not intended to start as a self-learning live AI trader. The first implementation is deliberately rules-based, tightly scoped, heavily documented, and safety-first.

---

## Current Project Status

**Phase:** final implementation-design phase, pre-code.

The repository is still primarily a documentation and architecture repository. The current work is to finish the implementation handoff documents before source-code generation begins.

The current focus is on:

- preserving the locked v1 trading scope,
- translating architecture into a concrete codebase structure,
- preparing the AI coding handoff for Claude Code,
- defining first-run and paper/shadow procedures,
- and keeping live-capital safety constraints explicit before implementation.

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
- Exchange-side protective stop mandatory
- User stream is the primary live state source
- REST is used for placement, cancellation, reconciliation, and recovery

### Risk

- Initial live risk target: approximately 0.25% account equity per trade
- Leverage is a sizing tool, not a target
- Capital preservation takes priority over return optimization

### Deployment

The release path is staged:

```text
research -> validation -> paper/shadow -> tiny live -> scaled live
```

No stage should be skipped.

---

## Core Architecture Principles

Prometheus v1 is designed as a **modular monolith**.

That means one primary deployable runtime with strong internal module boundaries, not a premature distributed microservice system.

Core principles:

- Strategy and execution remain strictly separated.
- Exchange state is authoritative for live position, order, and stop truth.
- Local runtime state exists for orchestration, restart, reconciliation, persistence, and operator continuity.
- Restart always begins in safe mode.
- Live trading may resume only after reconciliation restores state confidence.
- Runtime persistence stores restart-critical facts, not arbitrary convenience state.
- Observability is state-centric: exposure, protection, stream health, reconciliation, incidents, and operator action requirements matter most.
- The operator interface is part of the v1 safety boundary.

---

## Repository Structure

Current documentation structure:

```text
docs/
  00-meta/                  project objective, scope, current state, handoff context
  01-foundations/           foundational concepts and project framing
  02-market-structure/      futures mechanics, fees, funding, leverage, liquidation
  03-strategy-research/     strategy selection and v1 breakout strategy design
  04-data/                  historical data, timestamps, dataset versioning
  05-backtesting-validation/ backtesting principles and validation gates
  06-execution-exchange/    exchange/order handling and reconciliation concepts
  07-risk/                  risk philosophy and risk controls
  08-architecture/          implementation architecture and runtime design
  09-operations/            restart, incident, operator, review, release processes
  10-security/              API keys, secrets, permission scoping, security policies
  11-interface/             dashboard and operator-control requirements
  12-roadmap/               future roadmap and sequencing
  adr/                      architecture decision records
  glossary/                 shared definitions
  runbooks/                 operational procedures
  templates/                reusable documentation templates
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

## Most Important Current Documents

For current project context, start with:

```text
docs/00-meta/current-project-state.md
```

Then review the implementation-critical documents:

```text
docs/03-strategy-research/first-strategy-comparison.md
docs/03-strategy-research/v1-breakout-strategy-spec.md
docs/03-strategy-research/v1-breakout-backtest-plan.md

docs/04-data/historical-data-spec.md
docs/04-data/timestamp-policy.md
docs/04-data/dataset-versioning.md

docs/05-backtesting-validation/v1-breakout-validation-checklist.md

docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md

docs/08-architecture/implementation-blueprint.md
docs/08-architecture/state-model.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/observability-design.md
docs/08-architecture/codebase-structure.md

docs/09-operations/restart-procedure.md
docs/09-operations/incident-response.md
docs/09-operations/operator-workflow.md
docs/09-operations/daily-weekly-review-process.md
docs/09-operations/release-process.md

docs/10-security/api-key-policy.md
docs/10-security/secrets-management.md
docs/10-security/permission-scoping.md

docs/11-interface/operator-dashboard-requirements.md
```

---

## Source of Truth Policy

Markdown documents in this repository are the project’s primary source of truth.

If there is a conflict between older chat context and repository documentation:

1. detailed current Markdown docs win,
2. then `docs/00-meta/current-project-state.md`,
3. then older project chat memory,
4. then informal summaries.

Do not silently change locked decisions. Surface conflicts first.

---

## Implementation Handoff Status

The project is not yet ready for unrestricted code generation.

Before Claude Code implementation starts, the remaining high-value pre-code documents are:

- `docs/00-meta/ai-coding-handoff.md`
- first-run setup guide
- paper/shadow runbook
- tiny-live runbook
- review, incident, and release templates

The recently defined `codebase-structure.md` is the first bridge from architecture to implementation. The next major step is the AI coding handoff document.

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
- or premature distributed infrastructure.

The goal is not to get a bot trading as quickly as possible.

The goal is to build a system that can eventually be trusted with real capital under strict supervision.

---

## Safety and Security Rules

Hard project rules:

- Never commit secrets.
- Never place API keys or secrets in docs, code, logs, screenshots, or chats.
- Production API keys must have no withdrawal permission.
- Production API keys must use IP restriction.
- Development, paper/shadow, and production credentials must remain separate.
- If credentials are missing, invalid, or unauthorized, the bot must fail closed.
- If exchange/local state is uncertain, the bot must block new entries.
- If a position exists without confirmed protective stop coverage, the system is in an emergency state.

---

## Disclaimer

This repository is for research, architecture, and software-system design.

Nothing in this repository is financial advice. Trading leveraged crypto futures is high risk and can result in rapid loss of capital. The project explicitly prioritizes risk control, validation, and operational safety because profitability is uncertain and must never be assumed from design alone.

---

## Document Status

- Status: active
- Project phase: final implementation design, pre-code
- Initial live scope: BTCUSDT perpetual on Binance USDⓈ-M futures
- Last updated: 2026-04-17
