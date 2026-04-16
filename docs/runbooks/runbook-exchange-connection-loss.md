# Exchange Connection Loss

## Purpose
Respond safely to loss of exchange connectivity or stream health.

## Trigger / When to Use
- market-data stream disconnect
- user-data stream disconnect
- repeated heartbeat failure
- order request failures caused by connectivity degradation

## Preconditions
- determine whether market stream, user stream, or both are affected
- determine whether the engine can still query exchange state safely

## Step-by-Step Procedure
1. Mark the system degraded.
2. Stop initiating new trades unless policy explicitly permits otherwise.
3. Attempt controlled reconnect according to retry policy.
4. Renew any required session or listen-key state.
5. Reconcile positions and open orders after reconnect.
6. Resume normal operation only if state and stream health are clean.

## Validation / Expected Outcome
- streams restored
- state reconciled
- no stale uncertainty remains

## Rollback / Recovery
If reconnect remains unstable:
- keep new trading disabled
- consider kill switch or manual supervision mode

## Escalation
Escalate after repeated reconnect failure or if live state certainty is lost.

## Notes
Loss of connectivity is a risk event, not just a networking nuisance.

## Related Documents
- `runbook-engine-restart.md`
