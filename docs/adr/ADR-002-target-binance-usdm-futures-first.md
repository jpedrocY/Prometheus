# ADR ID: 002

## Title
Target Binance USDⓈ-M Futures First

## Status
Accepted

## Date
2026-04-16

## Context
The user has prior Binance and leveraged crypto trading experience, and the project values both long and short opportunity capture in a 24/7 market. Futures aligns well with that goal, but increases complexity.

## Decision
The primary initial venue target is Binance USDⓈ-M futures. Spot remains a valid baseline and reference path for comparison and simplification.

## Consequences
### Positive
- aligned with project goals and user background
- supports short exposure
- realistic and meaningful operational target

### Negative
- more complex execution and risk model
- added liquidation, funding, and margin considerations
- more demanding reconciliation requirements

## Alternatives Considered
- spot-only first
- exchange-agnostic design before venue specialization
- COIN-M futures first

## Open Questions
- Should v1 remain single-symbol through the entire first live cycle?

## Related Documents
- `../02-market-structure/futures-vs-spot.md`
- `../02-market-structure/binance-futures-mechanics.md`
