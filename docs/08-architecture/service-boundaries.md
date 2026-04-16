# Service Boundaries

## Purpose
Define the main boundaries between the trading engine and adjacent components.

## Scope
High-level separation only; detailed APIs are TBD.

## Background
Boundary clarity prevents accidental coupling and reduces the blast radius of changes.

## Definitions
- **Boundary**: a clear ownership line between concerns.
- **Blast radius**: the scope of impact when a component fails or changes.

## Main Framework / Design / Rules

### Trading Engine Owns
- strategy evaluation
- risk checks
- order intent generation
- exchange interaction
- reconciliation
- persistent trading state

### Operator Interface Owns
- visualization
- health/status display
- alerts surface
- limited manual controls
- human review workflows

### Shared Contract Areas
- state read model
- metrics
- alert events
- operator commands with explicit authorization rules

## Assumptions
- The engine should remain operable without the UI.

## Risks and Failure Modes
- UI becoming a hidden dependency for trading operations
- shared mutable state without ownership
- direct DB writes from the UI into core trading state

## Open Questions
- What write actions should the UI be allowed to trigger?

## Decisions
- UI should not directly own live trading logic.

## Next Steps
- define manual-control actions and audit requirements

## References
- `system-overview.md`
- `../11-interface/manual-control-actions.md`
