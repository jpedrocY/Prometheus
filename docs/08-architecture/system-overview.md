# System Overview

## Purpose
Describe the intended high-level system architecture and the primary component boundaries.

## Scope
This document covers the high-level design, not detailed implementation specifics.

## Background
The project is expected to evolve toward a live-capable trading system with a later operator interface. To avoid unnecessary coupling and risk, the engine and UI should remain separate.

## Definitions
- **Trading engine**: the service responsible for strategy evaluation, risk checks, execution, and reconciliation.
- **Operator interface**: dashboard or control layer for visibility and limited manual actions.
- **Reconciliation**: alignment of internal intended state with exchange-reported actual state.

## Main Framework / Design / Rules

### Core Architectural Principle
The trading engine and the future operator interface must remain separate layers or services.

### High-Level Components
1. Data ingestion layer  
   market data, user streams, metadata

2. Strategy/signal layer  
   deterministic rule evaluation producing intents

3. Risk layer  
   sizing, limits, brakes, veto logic

4. Execution layer  
   exchange adapter, order placement, cancel/replace, fill handling

5. State layer  
   positions, orders, fills, strategy state, audit events

6. Observability layer  
   logs, metrics, traces, alerts

7. Operator interface layer  
   dashboard, status, controls, review tools

### Runtime Assumption
A likely future deployment target is a small dedicated machine such as a NUC PC. The operator interface may later be displayed on a small desk monitor, but that interface should not reshape the core engine architecture prematurely.

### Future UI Note
A future UI may use Tailwind, Stitch AI, Laravel, or another stack. This is a later-phase concern and should consume engine outputs through defined boundaries rather than embedding live trading logic directly into the UI layer.

## Assumptions
- Engine correctness and recovery matter more than initial UI convenience.
- Service separation can be logical first and physical later if needed.

## Risks and Failure Modes
- embedding engine logic in a web application runtime too early
- weak state boundaries between execution and UI
- designing around future dashboard ideas instead of live-trading requirements

## Open Questions
- What interface should mediate between engine and UI: DB, API, event bus, or hybrid?
- What should be the minimum manual control surface exposed to the operator?

## Decisions
- engine and UI should remain separate
- NUC-style local deployment is a plausible later operational target
- UI stack is explicitly undecided and non-blocking for core engine work

## Next Steps
- define service boundaries in more detail
- define state model and observability design

## References
- `service-boundaries.md`
- `state-model.md`
- `observability-design.md`
- `../adr/ADR-003-separate-trading-engine-from-ui.md`
