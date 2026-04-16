# Failure Modes Overview

## Purpose
List the major failure classes that commonly break trading systems.

## Scope
This is a high-level failure map. Detailed handling belongs in later domain-specific docs and runbooks.

## Background
Trading bot failure is rarely caused by one dramatic mistake. More often it is caused by ordinary failures that were not made explicit early enough.

## Definitions
- **Silent failure**: a failure that does not immediately surface through alerts or visible symptoms.
- **Operational failure**: a failure caused by infrastructure, process, or runtime issues rather than strategy logic.

## Main Framework / Design / Rules

### Primary Failure Classes
1. Research failure  
   False edges, overfitting, unrealistic backtests.

2. Data failure  
   Missing data, bad timestamps, leakage, schema drift.

3. Execution failure  
   Rejected orders, partial fills, stale state, bad reconciliation.

4. Risk failure  
   Oversizing, correlated exposure, missing brakes, flawed stop logic.

5. Operational failure  
   Restart issues, stale connections, no alerting, no runbooks.

6. Security failure  
   Poor key handling, excessive permissions, no audit trail.

7. Governance failure  
   Strategy changes without clear evidence or approval criteria.

## Assumptions
- Most live failures can be prevented or softened through documentation and design discipline.

## Risks and Failure Modes
- focusing only on strategy quality
- underdocumenting operational risks
- ignoring “boring” failure classes because they seem solvable later

## Open Questions
- Which failure classes deserve hard blockers before paper trading?

## Decisions
- Failure mapping is a first-class design activity, not an afterthought.

## Next Steps
- Expand risk, execution, and operations docs
- Create runbooks for the first incident classes

## References
- `system-maturity-model.md`
- `../05-backtesting-validation/backtesting-principles.md`
