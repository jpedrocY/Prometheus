# Position Mismatch

## Purpose
Handle cases where internal position state differs from exchange-reported state.

## Trigger / When to Use
- internal position differs from exchange
- unexpected open exposure appears
- strategy state assumes flat while exchange shows open position

## Preconditions
- freeze new strategy-driven order creation
- capture logs and current snapshots

## Step-by-Step Procedure
1. Stop new discretionary strategy entries.
2. Query authoritative exchange position and open-order state.
3. Compare internal state, recent fills, and recent order events.
4. Determine whether mismatch is explainable by latency, restart, or missing event.
5. Rebuild internal state if possible.
6. If uncertainty remains, favor exchange-reported truth and move to safe mode.
7. Resume only after mismatch cause is understood or risk is neutralized.

## Validation / Expected Outcome
- internal state matches exchange
- root cause is documented
- residual exposure risk is known

## Rollback / Recovery
If mismatch cannot be resolved confidently:
- keep strategy halted
- flatten manually if policy requires
- document incident

## Escalation
Escalate immediately if mismatch involves live exposure and uncertainty.

## Notes
Position mismatch is a high-severity event.

## Related Documents
- `runbook-kill-switch-activation.md`
