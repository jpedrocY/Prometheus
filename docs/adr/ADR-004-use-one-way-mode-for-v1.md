# ADR ID: 004

## Title
Use One-Way Mode for V1

## Status
Accepted

## Date
2026-04-16

## Context
Hedge mode increases expressiveness but also introduces more state and execution complexity. The first live-capable version should reduce ambiguity where possible.

## Decision
V1 should use one-way mode rather than hedge mode.

## Consequences
### Positive
- simpler position semantics
- simpler reconciliation
- easier risk reasoning

### Negative
- reduced flexibility for advanced position handling
- some future strategy patterns may require reconsideration

## Alternatives Considered
- hedge mode from the start
- deferring the position-mode decision

## Open Questions
- Under what later conditions would hedge mode become worth the added complexity?

## Related Documents
- `../02-market-structure/leverage-liquidation-margin-modes.md`
