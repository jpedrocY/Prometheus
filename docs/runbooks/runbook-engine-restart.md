# Engine Restart

## Purpose
Provide a controlled restart procedure for the trading engine.

## Trigger / When to Use
- planned engine restart
- crash recovery
- deployment requiring restart
- suspected stale runtime state

## Preconditions
- confirm current trading mode
- confirm whether new order creation is already disabled
- confirm recent state persistence is healthy
- capture current alerts and incident context

## Step-by-Step Procedure
1. Pause or disable new trade initiation if the system is still responsive.
2. Record current known positions, open orders, and strategy state snapshot.
3. Stop the engine cleanly where possible.
4. Restart the engine service.
5. Rehydrate persistent state.
6. Reconnect data and user streams.
7. Run reconciliation against exchange state.
8. Confirm that internal positions and open orders match exchange-reported state.
9. Keep the engine in safe mode until reconciliation is explicitly clean.
10. Resume normal operation only after validation.

## Validation / Expected Outcome
- engine process is healthy
- streams are connected
- no unresolved position or order mismatch remains
- alerts reflect healthy status

## Rollback / Recovery
If reconciliation is not clean:
- keep trading disabled
- escalate to position mismatch procedure
- do not resume normal strategy execution

## Escalation
Escalate if:
- positions do not match,
- open orders are ambiguous,
- data or user stream health is unstable,
- recovery state is uncertain.

## Notes
Reconciliation is mandatory after restart. Do not assume that prior internal state is authoritative.

## Related Documents
- `../08-architecture/system-overview.md`
- `../06-execution-exchange/failure-recovery.md`
