# Cost Modeling

## Purpose
Define how costs should be represented during strategy research and validation.

## Scope
This is a framework doc. Numeric values should be refined per instrument and period.

## Background
A strategy that only works before costs is not a strategy. Cost assumptions must be present early, not bolted on after tuning.

## Definitions
- **Explicit costs**: fees and funding.
- **Implicit costs**: slippage, spread, adverse selection.

## Main Framework / Design / Rules
At minimum, strategy research should model:
- entry fee
- exit fee
- entry slippage
- exit slippage
- funding where applicable

### Policy Principles
- first-pass assumptions should be conservative
- costs should vary with execution style when relevant
- live logs must capture realized costs separately for later comparison

## Assumptions
- The first strategy family will likely be sensitive enough to costs that they must be modeled from the start.

## Risks and Failure Modes
- calibrating costs after selecting parameters
- ignoring volatility-dependent slippage
- treating funding as negligible by default

## Open Questions
- What baseline slippage formula should be used in v1 research?

## Decisions
- all validation is net of cost
- all futures research includes funding

## Next Steps
- define default cost presets for first strategy comparisons

## References
- `backtesting-principles.md`
- `../02-market-structure/fees-funding-slippage.md`
