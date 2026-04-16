# System Maturity Model

## Purpose
Define the staged maturity path for the project.

## Scope
This document covers progression from research to production operation.

## Background
The project should grow through controlled stages rather than trying to jump directly to full automation.

## Definitions
- **Promotion gate**: a required threshold before moving to the next stage.
- **Shadow trading**: live decision generation without live matching-engine execution.

## Main Framework / Design / Rules

### Stage 0 — Concept and Documentation
- establish project objective
- define assumptions
- map system domains
- create documentation structure

### Stage 1 — Strategy Research
- formalize candidate setups
- backtest with cost assumptions
- reject weak ideas quickly

### Stage 2 — Validation
- walk-forward evaluation
- robustness testing
- parameter sensitivity review

### Stage 3 — Live Simulation
- paper trading
- shadow trading
- execution-path verification
- state reconciliation tests

### Stage 4 — Tiny Live
- minimal size
- strict risk caps
- active supervision
- strong rollback readiness

### Stage 5 — Operational Hardening
- better observability
- runbooks
- deployment discipline
- operator workflows

### Stage 6 — Controlled Expansion
- more symbols
- more notional
- possibly more strategies
- possible ML additions where justified

## Assumptions
- Skipping stages increases hidden risk dramatically.

## Risks and Failure Modes
- using live capital to discover basic engineering flaws
- increasing scope and size simultaneously
- promoting strategies on weak evidence

## Open Questions
- What exact quantitative gates should separate Stage 3 from Stage 4?

## Decisions
- The project follows staged promotion, not direct deployment.

## Next Steps
- Expand `promotion-gates.md`
- Tie future milestones to this maturity model

## References
- `../05-backtesting-validation/promotion-gates.md`
- `../12-roadmap/milestones.md`
