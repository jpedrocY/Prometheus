# Fees, Funding, and Slippage

## Purpose
Define the core trading frictions that must be modeled before a strategy is considered credible.

## Scope
This is a policy and validation framing document. Exact numeric assumptions remain strategy- and period-specific.

## Background
Many weak strategies appear viable only because frictions are modeled poorly or ignored entirely.

## Definitions
- **Fees**: explicit exchange costs per trade.
- **Funding**: periodic transfer mechanism in perpetual futures.
- **Slippage**: difference between expected price and realized fill price.

## Main Framework / Design / Rules
Any strategy evaluation must include:
- entry and exit fees,
- slippage assumptions for both entry and exit,
- funding effects where relevant,
- differences between maker-like and taker-like behavior if the strategy depends on them.

### Design Principles
- Assume worse-than-ideal fills unless evidence supports tighter assumptions.
- Model costs before tuning parameters.
- Consider that short-horizon systems are more friction-sensitive.
- The live engine must record realized costs separately from research assumptions.

## Assumptions
- 10m–15m systems can still be materially affected by costs, especially if they trade frequently.

## Risks and Failure Modes
- using zero-slippage assumptions
- underestimating costs during high-volatility moves
- evaluating strategies on gross returns rather than net behavior

## Open Questions
- What default slippage framework should be used for first-pass strategy research?
- Should funding be modeled continuously or event-based in backtests?

## Decisions
- All strategy research must be net-of-cost.
- Funding is not optional in futures research.

## Next Steps
- expand cost-modeling docs
- define first-pass slippage assumptions for candidate strategy families

## References
- `../05-backtesting-validation/cost-modeling.md`
