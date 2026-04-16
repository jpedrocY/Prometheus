# Walk-Forward Validation

## Purpose
Document the preferred time-aware validation approach for the project.

## Scope
This document applies to both rules-based strategy research and any later ML components.

## Background
Time series must be validated chronologically. Random train/test splits create misleading confidence by violating the temporal structure of market data.

## Definitions
- **Walk-forward validation**: repeated train/validate/test progression across time windows.
- **Expanding window**: training set grows over time.
- **Rolling window**: training window moves with fixed or limited size.

## Main Framework / Design / Rules
The project should prefer validation approaches that:
- preserve time order,
- isolate tuning from final evaluation,
- test across multiple market regimes,
- estimate stability rather than only peak performance.

### Initial Preferred Approach
- exploratory stage: broad historical sweeps
- validation stage: rolling or expanding walk-forward windows
- promotion stage: final holdout plus shadow/live simulation evidence

## Assumptions
- Strategy quality must survive more than one market phase.

## Risks and Failure Modes
- training or tuning on the effective future
- treating a single long backtest as enough evidence
- using only one regime to judge robustness

## Open Questions
- What exact window scheme best fits the chosen strategy horizon?

## Decisions
- Time-aware validation is mandatory.
- Final promotion should not rely on a single historical split.

## Next Steps
- define a standard validation template for all strategy candidates

## References
- `backtesting-principles.md`
- `promotion-gates.md`
