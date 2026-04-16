# Milestones

## Purpose
Define the current milestone ladder for the project.

## Scope
This document is a concise milestone map, not a detailed schedule.

## Background
Milestones create checkpoints for quality and prevent progress from being defined only by code volume.

## Definitions
- **Milestone**: a discrete checkpoint with specific outputs and review criteria.

## Main Framework / Design / Rules

### M0 — Documentation Foundation
Outputs:
- docs structure
- templates
- core meta docs
- first ADRs

### M1 — Strategy Decision
Outputs:
- shortlist comparison
- selected first strategy family
- formalization draft

### M2 — Research Harness
Outputs:
- historical data pipeline
- baseline backtester
- cost-aware analytics

### M3 — Validation Harness
Outputs:
- walk-forward testing
- robustness checks
- promotion-gate drafts

### M4 — Execution Skeleton
Outputs:
- exchange adapter
- user stream handling
- state and reconciliation

### M5 — Risk and Ops Baseline
Outputs:
- sizing policy
- kill switches
- logging and alerting
- restart runbooks

### M6 — Shadow Trading Readiness
Outputs:
- live-path validation
- operator review workflow
- state recovery tests

### M7 — Tiny Live Readiness
Outputs:
- full gate review
- minimal-risk deployment conditions
- rollback plan

## Assumptions
- Milestones may be refined, but the staged ordering should remain mostly stable.

## Risks and Failure Modes
- milestones becoming vague
- skipping milestone reviews
- merging incompatible objectives into one milestone

## Open Questions
- What exact acceptance criteria should be added to M2–M7?

## Decisions
- milestone progression should be explicit and reviewable

## Next Steps
- add acceptance criteria after strategy selection

## References
- `implementation-roadmap.md`
- `phase-gates.md`
