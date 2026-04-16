# ADR ID: 005

## Title
Use Isolated Margin for V1

## Status
Accepted

## Date
2026-04-16

## Context
The first live-capable version should prioritize localized containment and clearer reasoning about position risk.

## Decision
V1 should use isolated margin rather than cross margin.

## Consequences
### Positive
- clearer per-position containment
- simpler risk interpretation
- safer first-live operating posture

### Negative
- less flexible margin utilization
- can be less capital-efficient than cross

## Alternatives Considered
- cross margin from the start
- delaying the margin-mode decision

## Open Questions
- What future conditions would justify moving selected strategies to cross margin?

## Related Documents
- `../02-market-structure/leverage-liquidation-margin-modes.md`
- `../07-risk/risk-philosophy.md`
