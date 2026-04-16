# Leverage, Liquidation, and Margin Modes

## Purpose
Document the core mechanical realities of leveraged futures trading that must be reflected in the bot design.

## Scope
This is a design and risk framing document, not a full liquidation-engine tutorial.

## Background
Leverage does not simply amplify returns; it tightens failure tolerance. A futures bot must treat leverage as a risk and implementation concern, not only a capital-efficiency feature.

## Definitions
- **Leverage**: borrowed exposure relative to allocated margin.
- **Liquidation**: forced closure when maintenance requirements are breached.
- **Isolated margin**: margin assigned per position.
- **Cross margin**: margin shared across positions and account balance.
- **One-way mode**: a single net position per symbol.
- **Hedge mode**: simultaneous long and short positions on the same symbol.

## Main Framework / Design / Rules

### Leverage Principles
- leverage should be constrained by risk policy, not by exchange maximums
- stop distance and position size should be sized together
- liquidation distance must never be ignored even if stop logic exists
- leverage settings should be bracket-aware

### Margin Mode Principles
#### Isolated Margin
Pros:
- clearer per-position risk containment
- simpler operational reasoning
- safer first live configuration

Cons:
- less flexible balance utilization

#### Cross Margin
Pros:
- balance sharing can reduce premature isolated position stress

Cons:
- failures can contaminate the broader account
- harder to reason about localized risk

### Position Mode Principles
#### One-Way Mode
Pros:
- simpler state
- simpler reconciliation
- cleaner v1 logic

#### Hedge Mode
Pros:
- more expressive position handling

Cons:
- more complex intent, state, and reduce-only behavior

## Assumptions
- V1 should favor simplicity and controllability over expressiveness.

## Risks and Failure Modes
- sizing from desired leverage rather than defined risk
- stops placed without awareness of liquidation proximity
- using cross margin too early
- using hedge mode before the execution model is mature

## Open Questions
- What minimum liquidation buffer should be required by policy?

## Decisions
- isolated margin is preferred for v1
- one-way mode is preferred for v1
- leverage must be secondary to explicit risk sizing

## Next Steps
- reflect these principles in risk policy docs
- ensure position-sizing docs account for liquidation constraints

## References
- `futures-vs-spot.md`
- `../07-risk/position-sizing-framework.md`
- `../adr/ADR-004-use-one-way-mode-for-v1.md`
- `../adr/ADR-005-use-isolated-margin-for-v1.md`
