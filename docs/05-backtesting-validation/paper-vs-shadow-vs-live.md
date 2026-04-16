# Paper vs Shadow vs Live

## Purpose
Clarify the staged progression from simulation to actual execution.

## Scope
This document covers environment types and their role in promotion.

## Background
Not all “not-live” testing is equivalent. The project should distinguish between simulated fills and live exchange-path validation.

## Definitions
- **Paper trading**: signals produce simulated fills under a modeled execution assumption.
- **Shadow trading**: live signals and order intents are generated, but actual orders are not sent to the matching engine.
- **Live trading**: real orders with real fills and capital at risk.

## Main Framework / Design / Rules
### Paper Trading
Use for:
- logic verification
- behavioral observation
- early live-data sanity checks

### Shadow Trading
Use for:
- exchange adapter validation
- order-shape validation
- timing and reconciliation checks
- operator workflow testing

### Live Trading
Use only after:
- strategy evidence is acceptable,
- execution path is trustworthy,
- restart and mismatch handling are tested,
- risk brakes are active.

## Assumptions
- Promotion should move from paper to shadow to tiny live.

## Risks and Failure Modes
- mistaking paper consistency for live readiness
- skipping shadow stage
- treating tiny live as debugging infrastructure

## Open Questions
- What exact checklist should block progression from shadow to live?

## Decisions
- shadow trading is a distinct and important stage

## Next Steps
- finalize promotion-gate checklists

## References
- `promotion-gates.md`
