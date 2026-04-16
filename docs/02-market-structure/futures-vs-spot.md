# Futures vs Spot

## Purpose
Compare spot and futures as initial deployment targets and explain why futures is currently the primary candidate.

## Scope
This document covers strategic and implementation implications, not exchange-specific API details.

## Background
Spot is operationally simpler, but futures provides both long and short exposure and more flexible capital use. That makes futures attractive, especially in 24/7 crypto markets, but the added mechanics materially increase system complexity.

## Definitions
- **Spot**: direct ownership or sale of the asset.
- **Perpetual futures**: derivative contracts that track an underlying asset without expiry, usually with funding.
- **Isolated margin**: margin allocated per position.
- **Cross margin**: margin shared across positions.

## Main Framework / Design / Rules

### Spot Advantages
- simpler position semantics
- no liquidation mechanics
- fewer exchange-state edge cases
- easier early execution model

### Futures Advantages
- ability to trade both directions
- capital efficiency
- broader opportunity set in both trends and drawdowns
- more direct alignment with the user’s prior trading experience

### Futures Disadvantages
- liquidation risk
- leverage and bracket constraints
- funding effects
- more complex order and position behavior
- greater reconciliation and risk-engine burden

### Current Project Position
- **Primary candidate**: Binance USDⓈ-M futures
- **Reference/baseline path**: spot remains useful for comparison and simplification
- **Preferred initial constraints**: one-way mode, isolated margin, conservative leverage

## Assumptions
- The project can handle futures complexity if scope is kept narrow at first.

## Risks and Failure Modes
- underestimating futures state complexity
- oversizing because leverage makes notional cheap
- confusing “can short” with “should take more setups”

## Open Questions
- Should v1 remain single-symbol for the entire first live cycle?
- Is 10m or 15m the better initial compromise for the first strategy family?

## Decisions
- Futures is the primary target, spot is a valid control path.
- Isolated margin and one-way mode are preferred starting choices.

## Next Steps
- Expand leverage, liquidation, and margin-mode docs
- Align execution design with futures position semantics

## References
- `binance-futures-mechanics.md`
- `leverage-liquidation-margin-modes.md`
