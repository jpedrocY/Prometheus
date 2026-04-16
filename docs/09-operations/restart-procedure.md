# Restart Procedure

## Purpose

This document defines the operational restart procedure for the trading engine.

Its purpose is to ensure that after:

- a planned restart,
- an unclean shutdown,
- a crash,
- a host reboot,
- or a stream-confidence failure,

the bot does **not** resume trading blindly.

Instead, the bot must:

- restore its local state,
- verify exchange state,
- reconcile the two,
- confirm position protection,
- and only then allow strategy activity to resume.

## Scope

This document applies to the v1 system with the following assumptions:

- Binance USDⓈ-M futures
- BTCUSDT only
- one-way mode
- isolated margin
- one position maximum
- one active protective stop maximum
- supervised deployment

This document covers:

- startup behavior,
- restart behavior,
- recovery after stale streams,
- reconciliation logic,
- and safe resumption rules.

This document does **not** define:

- full disaster recovery across multiple hosts,
- infrastructure provisioning,
- or generalized deployment automation.

## Background

The v1 system depends on:

- exchange-side order state,
- exchange-side position state,
- exchange-side protective stop state,
- user-stream events,
- and local persisted strategy/execution state.

That means restart behavior is a safety-critical part of the system.

A restarted process must not assume that:

- local state is correct,
- the stream is current,
- the exchange still matches the bot’s last known view,
- or a protective stop still exists.

The restart procedure exists to restore certainty before allowing any new exposure.

## Restart Philosophy

## Core principle

**State verification comes before strategy resumption.**

The bot must never restart directly into normal trading mode without reconciliation.

## Safe-mode principle

Every restart begins in:

- **safe mode**

In safe mode:

- no new entries are allowed
- no new strategy signals may generate live orders
- only recovery, reconciliation, and safety actions are allowed

Safe mode remains active until the restart procedure explicitly exits it.

## Restart Modes

The restart procedure must recognize the following modes.

## 1. Clean restart

A clean restart is a planned restart where:

- the process was intentionally stopped,
- no known exchange inconsistency exists,
- and local shutdown behavior was orderly.

Examples:
- maintenance restart
- planned redeploy
- controlled configuration restart

## 2. Unclean restart

An unclean restart is any restart where the process was interrupted unexpectedly.

Examples:
- application crash
- host reboot
- process kill
- power interruption
- forced container stop
- abrupt network failure

This mode must be treated as higher risk than a clean restart.

## 3. Recovery restart after stale-state condition

This is a controlled recovery where the process may still be alive or recently restarted, but state confidence was lost due to:

- stale user stream,
- missing expected updates,
- reconciliation warning,
- or other state-consistency failure.

This mode uses the same core recovery flow as an unclean restart.

## Preconditions

Before the restart procedure can complete successfully, the following must be available:

- application configuration
- exchange credentials
- local persisted state store
- logging / observability outputs
- network connectivity to Binance
- ability to query exchange state
- ability to restore or recreate user streams

If any of these prerequisites are missing, the procedure must remain in safe mode and raise an alert.

## Restart Sequence

## Step 1 — enter safe mode

Immediately on process start:

- set system state to `SAFE_MODE`
- block new entries
- block strategy-side live order generation
- record restart timestamp
- record restart reason if known

This is mandatory for every restart mode.

## Step 2 — initialize logging and observability

Before exchange actions begin:

- initialize logs
- initialize metrics
- initialize alerting hooks where applicable
- record process start
- record software version / config version if available

The restart procedure must itself be observable.

## Step 3 — load persisted local state

Load the last known persisted local state, including where available:

- strategy symbol
- current strategy stage
- expected position side
- expected position size
- entry order identifiers
- protective stop identifiers
- current stop-management stage
- last known reconciliation timestamp
- last known exception flags
- kill-switch state

### Rule
Local state must be treated as **provisional**, not authoritative.

It is needed for reconciliation, not as proof of truth.

## Step 4 — verify system prerequisites

Before exchange recovery proceeds, verify:

- system clock availability
- configuration load success
- credential availability
- network connectivity
- exchange API reachability

If any of these checks fail:

- remain in safe mode
- log the failure
- raise alert
- do not continue to strategy resumption

## Step 5 — restore or recreate user stream

The system must restore private-stream capability.

This includes:

- obtaining or restoring the user data stream
- confirming stream initialization
- scheduling keepalive maintenance
- marking the stream as not yet trusted for normal operation until reconciliation completes

### Rule
A restored stream is necessary, but **stream restoration alone is not sufficient** to resume trading.

Reconciliation must still complete first.

## Step 6 — fetch exchange position state

Query the current position state for the strategy symbol.

For v1, this means checking:

- BTCUSDT position status
- position size
- entry price if applicable
- unrealized state if applicable

### Purpose
This establishes whether the exchange currently believes the account has exposure on the symbol.

## Step 7 — fetch open normal orders

Query open normal orders for the strategy symbol.

### Purpose
This identifies:

- active entry orders
- stale normal orders
- unexpected outstanding orders
- possible mismatches between local and exchange order state

## Step 8 — fetch open algo orders

Query open algo / conditional orders for the strategy symbol.

### Purpose
This identifies:

- active protective stops
- stale protective orders
- missing stop coverage
- multiple unexpected protective orders

## Step 9 — perform reconciliation

Compare:

- local persisted state
- exchange position state
- open normal orders
- open algo orders

The reconciliation must answer:

1. Does a position exist?
2. If a position exists, does a valid protective stop exist?
3. Do exchange orders match expected strategy state?
4. Are there stale or unexpected orders?
5. Can the mismatch, if any, be repaired deterministically?

## Step 10 — classify reconciliation outcome

The restart procedure must classify the result as one of the following:

- `CLEAN`
- `RECOVERABLE_MISMATCH`
- `UNSAFE_MISMATCH`

This classification determines whether the bot may resume, repair, or escalate.

## Step 11 — resolve or escalate

Depending on the classification:

- resume if clean
- repair then resume if safely recoverable
- stay in safe mode and escalate if unsafe

## Step 12 — only then allow normal operation

Only after all required checks pass may the system:

- exit safe mode
- resume normal strategy evaluation
- allow new entries
- continue regular operation

## Reconciliation Logic

## Reconciliation inputs

The reconciliation engine must use:

- persisted local state
- current exchange position state
- current exchange normal open orders
- current exchange algo open orders

## Core reconciliation questions

### Position question
Does the exchange currently show an open BTCUSDT position?

### Protection question
If the exchange shows a position, does the exchange also show an appropriate protective stop?

### Order-state question
Do exchange open orders match what the bot expects to exist?

### Local-state question
Can local state be updated to match exchange truth without ambiguity?

## Reconciliation Outcomes

## 1. Clean

A restart is `CLEAN` when:

- exchange position matches local expectation
- open normal orders match local expectation
- protective stop state matches expectation
- no unexplained extra orders exist
- no unresolved inconsistencies remain

### Action
- log clean result
- exit safe mode
- resume normal operation

## 2. Recoverable mismatch

A restart is `RECOVERABLE_MISMATCH` when:

- a mismatch exists,
- but it can be resolved deterministically,
- and the system can restore a trustworthy state without dangerous ambiguity.

Examples:
- local stop ID missing but exchange protective stop exists clearly
- local order state stale but exchange state is consistent
- local strategy stage missing but position/stop state is clear
- stale normal order exists and can be safely canceled

### Action
- repair local state and/or exchange state
- log the repair action
- rerun reconciliation if necessary
- exit safe mode only after the repaired state is confirmed

## 3. Unsafe mismatch

A restart is `UNSAFE_MISMATCH` when:

- exchange and local state do not agree in a way that cannot be resolved immediately and safely,
- or the account is exposed without trusted protection,
- or exchange order state is ambiguous enough that automated continuation would be unsafe.

Examples:
- open position exists but no protective stop can be confirmed
- local state says flat but exchange shows exposure
- exchange shows multiple unexpected active orders
- position size differs materially from local expectation
- stream gap plus exchange mismatch prevents confident recovery

### Action
- remain in safe mode
- block new entries
- raise operator-visible alert
- enter exception state
- apply emergency decision logic if required

## Emergency Branch: Position Without Confirmed Protection

## Core rule

A position that exists without a confirmed protective stop is an emergency state.

This is one of the highest-priority restart failure conditions.

## Required response

If restart reconciliation finds:

- an open position
- but no valid protective stop can be confirmed

then the system must **not** resume normal operation.

It must enter an emergency decision branch.

## Allowed emergency actions

Depending on the situation, the recovery logic may do one of the following:

### Option 1 — restore protection immediately
If a new protective stop can be placed safely and confidently:
- place the replacement protective stop
- confirm it exists
- update local state
- continue only after reconciliation succeeds again

### Option 2 — flatten the position
If protection cannot be restored with sufficient confidence:
- flatten the position conservatively
- cancel remaining strategy orders as needed
- remain in safe mode until the account state is confirmed

### Rule
The system must never continue as if this state were normal.

## Unexpected Open Orders

## Core rule

Unexpected open orders discovered during restart must be explained, reconciled, or canceled before normal operation resumes.

## Possible cases

### Stale entry order
An old entry order remains open when it should not.

### Duplicate strategy order
More than one strategy-owned order is open unexpectedly.

### Stale algo stop
A protective stop remains open but no longer matches the current position logic.

### Orphaned order
An order exists on the exchange but is not represented in local state.

## Required response

The restart flow must:

- identify the order
- classify it
- decide whether it should be preserved or canceled
- log the action taken
- rerun reconciliation if needed

## Cancellation rule

For v1, cancellation should remain:

- symbol-scoped
- strategy-aware
- conservative

The bot should not cancel unrelated exchange activity outside the strategy scope.

## User Stream Recovery Policy

## Core rule

User-stream restoration is mandatory before normal operation resumes.

## Required steps

- restore or recreate the user data stream
- confirm stream subscription is active
- start keepalive maintenance
- mark stream health explicitly
- reconcile exchange state before trusting the stream for normal trading

## Stream-confidence rule

A newly restored stream is not sufficient proof of correct account state by itself.

It must be paired with successful reconciliation.

## Stream failure during restart

If user-stream restoration fails:

- remain in safe mode
- block new entries
- raise alert
- allow only controlled recovery actions

## Safe Mode Exit Criteria

The bot may exit safe mode only if all of the following are true:

- configuration and credentials are valid
- local state has been loaded
- exchange API access is working
- user stream has been restored
- exchange position state has been queried
- exchange normal open-order state has been queried
- exchange algo open-order state has been queried
- reconciliation result is `CLEAN` or safely repaired from `RECOVERABLE_MISMATCH`
- if a position exists, a valid protective stop is confirmed
- no blocking exception state remains active
- no kill-switch condition remains active

If any one of these fails, safe mode must remain active.

## Logging Requirements

The restart procedure must log at minimum:

- restart timestamp
- restart mode
- restart reason if known
- software/config version if available
- local-state summary
- exchange position summary
- exchange normal open-order summary
- exchange algo open-order summary
- reconciliation classification
- repair actions performed
- cancellations performed
- emergency actions performed
- safe-mode exit or persistence
- operator alert triggers if raised

## Recommended Restart State Fields

The procedure should maintain or expose the following restart-related state fields:

- `restart_mode`
- `restart_started_at`
- `restart_completed_at`
- `safe_mode_active`
- `user_stream_restored`
- `exchange_position_checked`
- `exchange_open_orders_checked`
- `exchange_open_algo_orders_checked`
- `reconciliation_status`
- `reconciliation_notes`
- `emergency_branch_triggered`
- `operator_alert_sent`

## Failure Modes

The restart procedure is expected to guard primarily against the following failures:

### 1. Bot restarts while position exists
The process may restart while the account is still exposed.

### 2. Position exists but stop is missing
The most dangerous restart condition.

### 3. User stream is stale or absent
The bot may otherwise believe it is operating normally while missing live account updates.

### 4. Local state is stale or incomplete
Restart must not assume local persistence is fully correct.

### 5. Unexpected exchange orders remain open
Old or orphaned orders can create dangerous ambiguity.

### 6. Recovery repair partially succeeds
A restart can fail in the middle of recovery, which means restart actions themselves must be visible and deterministic.

## Restrictions for V1

The restart procedure assumes the following remain true in v1:

- BTCUSDT only
- one active strategy
- one-way mode only
- isolated margin only
- one position maximum
- one protective stop maximum
- no portfolio-level orchestration
- no autonomous multi-symbol recovery logic

These restrictions are intentional and simplify safe recovery.

## Validation / Expected Outcome

A successful restart procedure should produce the following outcome:

- bot starts in safe mode
- local state is loaded
- exchange state is queried
- stream capability is restored
- position and order state are reconciled
- protection is confirmed if exposure exists
- no unexplained mismatches remain
- bot either resumes safely or remains blocked safely

A restart procedure is **not** considered successful if the process merely comes online but state certainty is still missing.

## Rollback / Recovery

If restart recovery fails or reaches an unsafe mismatch:

- remain in safe mode
- block new entries
- preserve logs and reconciliation context
- alert the operator
- optionally flatten exposure if protection cannot be trusted
- rerun restart reconciliation only after the blocking condition is understood or repaired

## Escalation

Immediate escalation is required when any of the following occurs:

- open position exists without confirmed protection
- local state and exchange state disagree materially
- multiple unexpected strategy orders are open
- user stream cannot be restored
- restart recovery repeatedly fails
- emergency flattening is triggered
- kill-switch remains active after restart

## Notes

The restart procedure must be treated as part of the live trading safety system, not as operational afterthought.

A bot that cannot restart safely cannot be trusted to run continuously.

## Decisions

The following decisions are accepted for the restart procedure:

- every restart begins in safe mode
- no new entries are allowed until reconciliation passes
- reconciliation uses:
  - persisted local state
  - exchange position state
  - symbol-scoped normal open orders
  - symbol-scoped algo open orders
- user stream must be restored as part of restart recovery
- a position without confirmed protective stop is an emergency condition
- unexpected stale orders must be reconciled or canceled before normal operation resumes
- restart outcomes are classified as:
  - `CLEAN`
  - `RECOVERABLE_MISMATCH`
  - `UNSAFE_MISMATCH`
- all restart actions must be logged clearly

## Open Questions

The following remain open:

1. What exact timeout should define stream-restoration failure during restart?
2. What exact timeout should define reconciliation failure before escalation?
3. Under which precise scenarios should the bot flatten immediately rather than attempt stop restoration first?
4. What exact operator alert routing should be used for each restart failure class?
5. Should the restart procedure explicitly verify commission-rate and metadata freshness, or is that unnecessary for v1 startup?
6. Should repeated restart failures trigger an automatic hard lockout requiring manual operator clearance?

## Next Steps

After this document, the next recommended files are:

1. `docs/10-security/api-key-policy.md`
2. `docs/09-operations/incident-response.md`
3. `docs/09-operations/operator-workflow.md`

## References

Binance references:

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams

- Binance USDⓈ-M Futures Start User Data Stream  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Start-User-Data-Stream

- Binance USDⓈ-M Futures Position Information V3  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Position-Information-V3

- Binance USDⓈ-M Futures Current All Open Orders  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Current-All-Open-Orders

- Binance USDⓈ-M Futures Current All Algo Open Orders  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Current-All-Algo-Open-Orders

- Binance USDⓈ-M Futures Cancel All Open Orders  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Cancel-All-Open-Orders