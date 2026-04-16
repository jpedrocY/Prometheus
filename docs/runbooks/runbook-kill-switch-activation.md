# Kill Switch Activation

## Purpose
Describe when and how to halt trading activity rapidly and safely.

## Trigger / When to Use
- severe position mismatch
- repeated exchange-state uncertainty
- risk limit breach
- uncontrolled order behavior
- major data integrity failure

## Preconditions
- identify whether existing exposure must be actively managed
- capture incident context

## Step-by-Step Procedure
1. Disable new trade initiation immediately.
2. Cancel non-protective pending orders where appropriate.
3. Assess current live exposure.
4. Determine whether positions should be reduced, flattened, or held under supervision.
5. Preserve logs, alerts, and state snapshots.
6. Do not re-enable automated trading until cause analysis is complete.

## Validation / Expected Outcome
- no new automated risk is being added
- current exposure is understood
- incident is contained

## Rollback / Recovery
Recovery requires:
- root cause assessment
- state verification
- explicit approval to re-enable automation

## Escalation
Always escalate kill-switch events for review.

## Notes
A kill switch should be treated as a designed safety response, not as a failure of discipline.

## Related Documents
- `../07-risk/kill-switches.md`
