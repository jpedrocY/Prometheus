# Implementation Roadmap

## Purpose
Provide the current staged build order for the project.

## Scope
This is a planning document for the early and middle phases of the project.

## Background
The project should build from clarity and correctness outward, not from feature count backward.

## Definitions
- **Build order**: the recommended sequence of implementation work.
- **Milestone**: a meaningful project stage with reviewable outputs.

## Main Framework / Design / Rules

### Phase 1 — Documentation and Decision Spine
- create docs structure
- lock initial ADRs
- define assumptions and scope
- establish strategy-selection framework

### Phase 2 — Strategy Formalization
- compare initial candidate families
- translate selected concepts into objective rules
- define required data inputs

### Phase 3 — Research and Validation Harness
- historical data handling
- backtest framework
- cost model
- walk-forward validation
- promotion checklist drafts

### Phase 4 — Live Execution Skeleton
- exchange adapter
- order lifecycle handling
- user stream processing
- reconciliation logic
- state persistence

### Phase 5 — Risk and Operations Hardening
- sizing policy implementation
- daily loss rules
- kill switches
- logging/metrics/alerts
- restart and incident runbooks

### Phase 6 — Shadow and Tiny Live
- shadow workflow
- operator review cycle
- tiny live rollout under hard caps

### Phase 7 — Controlled Expansion
- more symbols
- improved tooling
- possible ML additions in constrained roles
- future UI/dashboard integration

## Assumptions
- Strategy selection must happen before deep implementation of the trading engine.
- Core engine reliability precedes polished UI work.

## Risks and Failure Modes
- building execution before knowing what the strategy actually requires
- overdesigning future integrations
- scaling before the system has survived routine failures

## Open Questions
- What is the earliest point at which a minimal operator dashboard becomes useful?

## Decisions
- roadmap is staged and validation-driven

## Next Steps
- create milestone detail docs
- perform the first strategy family comparison

## References
- `milestones.md`
- `phase-gates.md`
- `../01-foundations/system-maturity-model.md`
