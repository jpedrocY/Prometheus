# Backtesting Principles

## Purpose
Define the minimum standards for a credible backtest in this project.

## Scope
This document establishes principles, not a specific backtesting engine implementation.

## Background
Backtests are useful only when they help reject weak ideas and estimate live behavior honestly. They become dangerous when used as persuasion tools.

## Definitions
- **Leakage**: use of future information directly or indirectly in a backtest.
- **Overfitting**: optimizing to historical noise rather than durable structure.
- **Net performance**: results after all modeled costs.

## Main Framework / Design / Rules
A backtest should:
- use explicit, reproducible rules,
- respect chronological order,
- include realistic cost assumptions,
- separate exploratory tuning from final evaluation,
- export trade-level detail,
- support robustness review.

### Minimum Standards
- no look-ahead logic
- no hidden discretionary filtering
- no gross-only performance claims
- no cherry-picked windows without explanation
- no parameter optimization without sensitivity review

## Assumptions
- The first backtests will be simpler than the final execution model but must still be honest.

## Risks and Failure Modes
- appealing equity curves masking weak methodology
- repeated parameter tuning until something works
- ignoring tails and drawdowns

## Open Questions
- What first-pass robustness checks should be mandatory for every strategy candidate?

## Decisions
- Chronological integrity is mandatory.
- Cost modeling is mandatory.

## Next Steps
- expand walk-forward and promotion-gate docs

## References
- `walk-forward-validation.md`
- `cost-modeling.md`
- `promotion-gates.md`
