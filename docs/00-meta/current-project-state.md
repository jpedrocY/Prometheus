# Current Project State

## Purpose

This document defines the current state of the Prometheus trading system project.

Its purpose is to:

- provide a clear snapshot of what has already been designed and decided
- identify what remains before implementation
- define the boundary between research/design and code generation
- ensure continuity across chats, sessions, and tools
- act as the authoritative “project memory checkpoint”

This document should be treated as the **single high-level source of truth** for project status.

---

## Project Objective

The goal of the project is to design and build a:

> **production-oriented, safety-first, operator-supervised trading system**

for:

- Binance USDⓈ-M futures  
- BTCUSDT perpetual (initial scope)

The system is:

- initially **rules-based**
- designed for **robustness, not hype**
- built for **safe live deployment**
- structured to **support future extensions (including AI), but not depend on them**

---

## Strategic Direction (Locked Decisions)

The following decisions are **locked unless explicitly revised**:

### Market & Venue
- Exchange: Binance USDⓈ-M Futures
- Primary symbol: BTCUSDT perpetual
- Secondary (research only): ETHUSDT

### Strategy
- Strategy type: breakout continuation
- Signal timeframe: 15m
- Higher timeframe bias: 1h
- Entry: bar-close confirmation → market order
- Stop: structural invalidation + ATR buffer
- Trade management: staged risk reduction + trailing

### Execution
- One-way mode
- Isolated margin
- One symbol only (v1)
- One position only (v1)
- Exchange-side protective stop mandatory

### Risk
- Initial risk: ~0.25% equity per trade
- Leverage: tool, not target

### Deployment
- Supervised (not autonomous)
- Staged rollout:
  - research → validation → paper → tiny live → scaled live

---

## Architectural Direction (Locked)

### Core principles

- Modular monolith (v1)
- Exchange is the **source of truth**
- User stream = **primary live state source**
- REST = placement, recovery, reconciliation
- Restart = safe mode first
- Strategy and execution are strictly separated
- Persistence is **restart-critical only**
- Observability is **state-centric**

---

## What Has Been Fully Designed

The following areas are now **substantially defined and documented**.

---

### 1. Strategy & Validation

- Strategy selection and comparison
- Breakout strategy specification
- Backtest plan
- Validation checklist

---

### 2. Data Layer

- Historical data specification
- Timestamp policy (UTC ms)
- Dataset versioning

---

### 3. Execution & Exchange Behavior

- Entry model (market after bar close)
- Protective stop model (STOP_MARKET, exchange-side)
- Stop update model (cancel-and-replace)
- User stream as primary truth
- Deterministic order IDs

See:  
:contentReference[oaicite:0]{index=0}

---

### 4. Runtime Architecture

- Modular monolith design
- Component boundaries
- Strategy / risk / execution separation
- Research vs live runtime separation
- Exchange-authority rules

See:  
:contentReference[oaicite:1]{index=1}

---

### 5. State Model

- Runtime modes (SAFE_MODE, RUNNING_HEALTHY, etc.)
- Trade lifecycle states
- Protection states (critical safety dimension)
- Reconciliation states
- Control flags and interaction rules

See:  
:contentReference[oaicite:2]{index=2}

---

### 6. Internal Communication

- Commands vs events vs queries
- Message envelope structure
- Component ownership boundaries
- Event-driven state transitions

See:  
:contentReference[oaicite:3]{index=3}

---

### 7. Runtime Persistence

- What must be persisted vs derived
- Required entities (runtime, trade, protection, reconciliation, incidents)
- Write timing rules
- Crash safety principles
- Restart-read behavior

See:  
:contentReference[oaicite:4]{index=4}

---

### 8. Observability

- Structured event model
- Health dimensions (streams, protection, reconciliation, etc.)
- Alerting philosophy
- Operator-facing summaries
- Audit requirements

See:  
:contentReference[oaicite:5]{index=5}

---

### 9. Restart & Recovery

- Safe-mode-first restart
- Reconciliation sequence
- Clean vs recoverable vs unsafe mismatch
- Emergency branch (unprotected position)

See:  
:contentReference[oaicite:6]{index=6}

---

### 10. Incident Handling

- Severity classification (1–4)
- Containment-first principle
- Safe-mode enforcement
- Emergency handling rules

See:  
:contentReference[oaicite:7]{index=7}

---

### 11. Operator Workflow

- Responsibilities and boundaries
- Allowed manual actions
- Supervision model
- Approval rules

See:  
:contentReference[oaicite:8]{index=8}

---

### 12. Review Process

- Daily operational review
- Weekly review
- Escalation thresholds
- Review artifacts

See:  
:contentReference[oaicite:9]{index=9}

---

### 13. Release & Deployment

- Staged promotion pipeline
- Environment model
- Pre-live checklist
- Rollback rules

See:  
:contentReference[oaicite:10]{index=10}

---

### 14. Security

- API key policy (least privilege, no withdrawals)
- Secrets management rules
- Permission scoping model
- Environment separation

See:  
:contentReference[oaicite:11]{index=11}  
:contentReference[oaicite:12]{index=12}  
:contentReference[oaicite:13]{index=13}  

---

### 15. Operator Interface

- Dashboard requirements
- Required visibility
- Control actions
- Safety-first UI philosophy

See:  
:contentReference[oaicite:14]{index=14}

---

## What Is NOT Yet Defined (Pre-Implementation Gaps)

The following areas are still missing or incomplete and should be finalized **before Claude Code implementation**:

---

### 1. Codebase Structure

- Folder/module layout
- Naming conventions
- Dependency boundaries
- Interface surfaces

---

### 2. AI Coding Handoff Document

- How Claude Code should operate
- What files it can modify
- How to respect architecture constraints
- Testing expectations

---

### 3. First-Run Setup Guide

- Environment setup
- Secrets loading
- Initial configuration
- First startup expectations

---

### 4. Paper / Shadow Runbook

- How to run without real capital
- Expected behaviors
- Validation checklist

---

### 5. Tiny Live Runbook

- First live deployment procedure
- Risk restrictions
- Monitoring expectations
- Abort conditions

---

### 6. Templates

- Daily review template
- Weekly review template
- Incident report template
- Release note template

---

## Current Phase

The project is currently in:

> **Final implementation design phase (pre-code)**

This means:

- Architecture is largely defined  
- Execution behavior is defined  
- Safety systems are defined  
- Operational model is defined  

But:

- Implementation structure is not yet fully specified  
- Code generation has not started  

---

## Next Step (Critical)

The next step is:

> **Define the codebase structure and AI coding handoff**

This is the bridge between:

- design  
and  
- actual implementation  

---

## Handoff Readiness Criteria

The project is ready for Claude Code when:

- [ ] Codebase structure is defined  
- [ ] Runtime modules are mapped to code  
- [ ] Interfaces are clearly scoped  
- [ ] Persistence model is implementable  
- [ ] Event system is implementable  
- [ ] Runbooks exist for first execution  
- [ ] Safety constraints are enforceable in code  

---

## Final Notes

- This system is designed for **robustness, not speed of development**
- Narrow scope is intentional and should be preserved
- Safety and state certainty take priority over optimization
- The goal is not to “get a bot running”  
  → The goal is to build a system that **can be trusted with capital**

---

## Document Status

- Status: ACTIVE
- Last updated: (fill on update)
- Owner: Project operator
- Role: Source-of-truth project state checkpoint