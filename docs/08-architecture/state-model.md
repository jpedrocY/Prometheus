# State Model

## Purpose

This document defines the live runtime state model for the v1 Prometheus trading system.

Its purpose is to make the system’s operational state explicit by defining:

- top-level runtime modes,
- trade lifecycle states,
- position-protection states,
- reconciliation states,
- control and incident state interactions,
- persisted versus derived runtime state,
- and the event classes that are allowed to drive state transitions.

This document exists because v1 depends on state certainty as a safety boundary.

The bot must not continue normal operation when it is uncertain about:

- whether a position exists,
- whether the position is protected,
- whether exchange state matches local state,
- or whether required streams are fresh and trustworthy.

This document is the live runtime state contract.

It does **not** define:

- the full implementation blueprint,
- the observability schema,
- the operator dashboard layout,
- or full code-level interface definitions.

## Scope

This state model applies to the v1 system assumptions:

- Binance USDⓈ-M futures
- BTCUSDT only in first live-capable scope
- one-way mode
- isolated margin
- one active strategy
- one open position maximum
- one active protective stop maximum
- supervised operation
- restart begins in safe mode
- exchange-side protective stop is mandatory for live positions

This document covers:

- runtime state modeling for live trading,
- state ownership boundaries,
- transition rules,
- invalid state combinations,
- and the interaction between runtime, protection, reconciliation, and incident states.

This document does **not** cover:

- historical backtest state modeling,
- portfolio-level orchestration,
- hedge-mode state handling,
- or multi-symbol coordination.

## Background

The project already defines several critical state-dependent requirements:

- the bot must not treat a trade as operationally safe until protective stop coverage is confirmed
- restart must begin in safe mode and reconcile before resumption
- exchange state is authoritative for position/order/protection truth
- incidents that create meaningful uncertainty must block new exposure
- the operator workflow assumes a clear set of top-level system modes
- and recovery decisions depend on whether mismatches are clean, recoverable, or unsafe

Those rules imply that state must be modeled explicitly rather than being scattered across ad hoc booleans and informal assumptions.

## State-Model Principles

## 1. Hierarchical model, not one giant flat enum

The runtime state model should be hierarchical.

It should consist of:

- a top-level runtime mode model,
- a trade lifecycle model,
- a position-protection model,
- a reconciliation model,
- and control / exception flags layered on top.

This is preferable to one giant flat state enum because the runtime needs to track multiple dimensions of truth at once.

## 2. Exchange truth outranks local assumptions

Exchange state is authoritative for:

- whether a position exists,
- what its side and size are,
- whether an order exists,
- and whether protective stop coverage exists.

Local runtime state exists for:

- orchestration,
- restart continuity,
- recovery,
- internal control flow,
- and operator continuity.

If local and exchange state conflict, the system must resolve the conflict in favor of exchange truth.

## 3. Protection is a first-class state concern

A position is not equivalent to a safely managed live trade.

The runtime must explicitly distinguish between:

- position exists
- and
- position is confirmed protected

This is one of the most important safety principles in the whole state model.

## 4. Normal operation requires state certainty

The system may operate normally only when all of the following are true:

- required runtime mode permits it
- no blocking control flag is active
- reconciliation status is acceptable
- required streams are sufficiently trusted
- and if a position exists, protection is confirmed

## 5. Persist only restart-critical facts

The runtime should persist the facts required for:

- restart safety,
- reconciliation,
- operator continuity,
- and deterministic recovery.

It should not persist large amounts of derived convenience state that can be recomputed safely.

## Top-Level Runtime Modes

The runtime should use a small set of primary modes.

## Primary Modes

### `SAFE_MODE`

Meaning:

- no new entries are allowed
- strategy-side live order generation is blocked
- only safety, verification, reconciliation, recovery, cancellation, protection, or flattening actions are allowed

Typical triggers:

- startup
- restart
- serious uncertainty
- blocking incident
- stale critical state
- pre-recovery state

### `RUNNING_HEALTHY`

Meaning:

- the bot is allowed to evaluate strategy logic normally
- new entries are allowed if other gates also permit them
- state confidence is acceptable
- no blocking uncertainty remains

This is the normal target operating mode.

### `RECOVERING`

Meaning:

- the bot is actively performing restart, reconciliation, repair, or controlled recovery work
- the runtime must not be treated as normal live-trading mode
- new entries are blocked

This mode is narrower than `SAFE_MODE` because it indicates active recovery work rather than generic blocked safety posture.

### `BLOCKED_AWAITING_OPERATOR`

Meaning:

- the bot cannot safely continue without an explicit human decision
- new entries are blocked
- automated continuation is not allowed

Typical triggers:

- post-emergency review required
- unresolved unsafe mismatch
- kill-switch clearance required
- severe incident recovery requires approval
- emergency flattening aftermath

## Control / Exception Flags

These should be modeled as layered flags rather than primary runtime modes.

### `incident_active`

Meaning:
- an incident is currently open and not yet fully resolved

### `kill_switch_active`

Meaning:
- strategy progression and new entries are hard-blocked
- recovery or flattening actions may still be allowed depending on policy

### `paused_by_operator`

Meaning:
- the operator has intentionally paused new activity
- no new entries are allowed until operator clears the pause

### `entries_blocked`

Meaning:
- new entries are blocked for any current reason
- this may be derived from multiple underlying conditions but is still useful as an explicit operational gate

### `operator_review_required`

Meaning:
- the bot may be contained, but resumption still requires explicit human review

## Runtime Mode Rules

## Entering `SAFE_MODE`

The bot should enter `SAFE_MODE` automatically when:

- the process starts
- a restart begins
- a blocking incident occurs
- execution outcome of a critical action is unknown and cannot be confirmed immediately
- user stream is stale while exposure or order-state certainty matters
- reconciliation is required after confidence loss
- protection is uncertain
- required credentials or permissions are invalid for intended live operation

## Entering `RUNNING_HEALTHY`

The bot may enter `RUNNING_HEALTHY` only when:

- startup / recovery prerequisites are satisfied
- reconciliation status is acceptable
- no blocking exception remains active
- required streams are sufficiently trusted
- kill switch is not active
- operator pause is not active
- and if a position exists, protective-stop state is confirmed acceptable

## Entering `RECOVERING`

The bot should enter `RECOVERING` when:

- restart reconciliation is running
- stream recovery is underway after confidence loss
- exchange/local mismatch repair is in progress
- or controlled state repair is happening

## Entering `BLOCKED_AWAITING_OPERATOR`

The bot should enter `BLOCKED_AWAITING_OPERATOR` when:

- automated recovery cannot safely conclude the next step
- explicit operator review is required by policy
- emergency exposure-risk conditions have been contained but not cleared for resumption
- or the bot must remain halted until a human decision is recorded

## Trade Lifecycle State Model

The runtime should separately track the lifecycle of the current or most recent live trade attempt.

## Trade Lifecycle States

### `FLAT`

Meaning:
- no active trade attempt exists
- no exchange position is currently expected locally
- no entry workflow is in progress

This is the normal resting state.

### `SIGNAL_CONFIRMED`

Meaning:
- a completed-bar strategy signal has been confirmed
- entry has not yet been submitted

This state may exist only if the runtime currently allows a new entry path to proceed.

### `ENTRY_SUBMITTED`

Meaning:
- the entry order has been submitted to the exchange
- the final exchange outcome is not yet fully confirmed

### `ENTRY_ACKNOWLEDGED`

Meaning:
- exchange acknowledged the order submission path
- but the runtime still does not assume the position is fully established

### `ENTRY_FILL_CONFIRMED`

Meaning:
- exchange/user-stream evidence confirms an entry fill occurred

This is not yet an acceptable steady operating state unless protection is also handled.

### `POSITION_CONFIRMED`

Meaning:
- exchange truth confirms the expected position exists

### `PROTECTIVE_STOP_SUBMITTED`

Meaning:
- protective stop placement has been submitted
- protection is not yet fully trusted

### `POSITION_PROTECTED`

Meaning:
- the position exists
- protective stop coverage is confirmed acceptable
- and the trade may continue under normal managed-trade rules

This is the first acceptable steady “live trade” state.

### `RISK_STAGE_INITIAL`

Meaning:
- the trade is live and protected
- original risk stage remains active

### `RISK_STAGE_REDUCED`

Meaning:
- first stop-reduction rule has been applied

### `RISK_STAGE_BREAKEVEN`

Meaning:
- stop has been moved to break-even

### `RISK_STAGE_TRAILING`

Meaning:
- trailing management is active

### `EXIT_PENDING`

Meaning:
- an exit path has been initiated
- but final exchange-confirmed closure is not yet established

### `EXIT_CONFIRMED`

Meaning:
- exchange/user-stream evidence confirms the trade has been closed

### `TRADE_CLOSED`

Meaning:
- the runtime has completed the trade lifecycle cleanly and may return toward `FLAT`

### `TRADE_EXCEPTION`

Meaning:
- the trade workflow encountered a significant uncertainty or failure that requires recovery, special handling, or manual review

## Trade Lifecycle Rules

### Rule 1
A trade must not be treated as safely live at `ENTRY_FILL_CONFIRMED` alone.

### Rule 2
The first acceptable steady live-trade state is `POSITION_PROTECTED`.

### Rule 3
Managed risk stages such as `RISK_STAGE_REDUCED`, `RISK_STAGE_BREAKEVEN`, and `RISK_STAGE_TRAILING` should only exist while protective coverage remains acceptable.

### Rule 4
`TRADE_EXCEPTION` should be reachable from any non-terminal trade state if execution or protection certainty is lost.

## Position and Protection State Model

Protection state should be modeled explicitly and separately from trade lifecycle stage.

## Protection States

### `NO_POSITION`

Meaning:
- exchange does not show an open strategy position
- there is no active protection requirement

### `POSITION_UNCONFIRMED`

Meaning:
- the runtime suspects exposure may exist, but exchange truth is not yet adequately confirmed

This is a short-lived uncertainty state and not an acceptable steady state.

### `POSITION_UNPROTECTED`

Meaning:
- exchange position is believed to exist
- but acceptable protective stop coverage has not yet been confirmed

This is a dangerous state and must not be treated as normal.

### `STOP_PENDING_CONFIRMATION`

Meaning:
- protective stop has been submitted or replaced
- confirmation is still pending

### `POSITION_PROTECTED`

Meaning:
- exchange position exists
- and acceptable protective stop coverage is confirmed

### `STOP_REPLACEMENT_IN_PROGRESS`

Meaning:
- a cancel-and-replace protective stop workflow is underway
- protection continuity must be watched explicitly

This state should be tightly controlled and short-lived.

### `PROTECTION_UNCERTAIN`

Meaning:
- the bot cannot currently trust whether the live position is adequately protected

This should force safe handling.

### `EMERGENCY_UNPROTECTED`

Meaning:
- exchange position exists
- acceptable protective stop cannot be confirmed
- and the runtime is in an emergency branch

This is one of the highest-priority failure states.

## Protection-State Rules

### Rule 1
`POSITION_UNPROTECTED` and `PROTECTION_UNCERTAIN` must block new entries.

### Rule 2
`EMERGENCY_UNPROTECTED` must force emergency handling and must never coexist with normal healthy trading posture.

### Rule 3
If protection certainty is lost during stop replacement, the runtime must move into controlled exception handling rather than assuming protection exists.

### Rule 4
A live open position should normally settle only in `POSITION_PROTECTED`, not in transitional protection states.

## Reconciliation State Model

Reconciliation is not only a restart concern.

It may also be required after:

- stream interruption,
- uncertain execution outcomes,
- state divergence,
- or other confidence-loss events.

## Reconciliation States

### `NOT_REQUIRED`

Meaning:
- no current condition requires reconciliation beyond ordinary live processing

### `REQUIRED`

Meaning:
- reconciliation is needed before the runtime may be considered trustworthy for normal continuation

### `IN_PROGRESS`

Meaning:
- reconciliation work is currently running

### `CLEAN`

Meaning:
- reconciliation found no blocking mismatch
- exchange and local state are acceptably aligned

### `RECOVERABLE_MISMATCH`

Meaning:
- mismatch exists
- but it can be resolved deterministically and safely

### `REPAIRED_PENDING_RECHECK`

Meaning:
- repair action has been taken
- but reconciliation must still be rerun or reconfirmed before normal resumption

### `UNSAFE_MISMATCH`

Meaning:
- mismatch is severe enough that automated normal continuation is unsafe

This should force blocked or emergency behavior depending on exposure/protection context.

## Reconciliation Rules

### Rule 1
`UNSAFE_MISMATCH` must prevent `RUNNING_HEALTHY`.

### Rule 2
A runtime with open exposure and reconciliation status worse than `CLEAN` must be treated cautiously and may require `SAFE_MODE` or `RECOVERING`.

### Rule 3
`RECOVERABLE_MISMATCH` is not itself permission to resume normal trading; successful repair and acceptable recheck are still required.

## Incident and Control-State Interaction

Incident state and control state interact with runtime modes, but they should not replace them.

## Incident Severity Interaction

### Severity 1
- may leave runtime mode unchanged
- typically logs and continues if state certainty remains intact

### Severity 2
- may keep runtime out of safe mode if exposure risk is controlled
- may still block new entries if confidence is reduced

### Severity 3
- should usually force `SAFE_MODE` or `RECOVERING`
- operator visibility is required

### Severity 4
- must force `SAFE_MODE`
- may additionally require `BLOCKED_AWAITING_OPERATOR`
- may require emergency flattening or emergency protection restoration path

## Kill-Switch Interaction

If `kill_switch_active` is true:

- no new entries are allowed
- normal strategy progression is blocked
- runtime must not be considered fully healthy for trading purposes
- only controlled containment/recovery actions may proceed

## Operator Pause Interaction

If `paused_by_operator` is true:

- no new entries are allowed
- the system may still display health and current exposure state
- existing protected positions may still require controlled management depending on policy

## Operator Review Interaction

If `operator_review_required` is true:

- automated return to `RUNNING_HEALTHY` must not occur
- explicit review must clear the condition first

## Persisted vs Derived Runtime State

## Persisted Runtime State

The runtime should persist the minimum set of restart-critical operational facts.

### Recommended persisted fields

- current primary runtime mode
- incident-active flag
- kill-switch flag
- pause flag
- operator-review-required flag
- trade lifecycle state
- protection state
- reconciliation state
- current strategy stage
- current signal reference and timestamp if applicable
- expected entry side
- entry client order ID
- entry exchange order ID if known
- entry fill timestamp if known
- average fill price if known
- current position side
- current position size
- protective stop client order ID
- protective stop exchange order ID if known
- stop-management stage
- trailing stage if active
- last successful reconciliation timestamp
- restart context if relevant
- exception flags

## Derived / Recomputable Runtime State

The following should generally be treated as derived or recomputable where practical:

- current operator summary banner text
- UI rollups of warning state
- “healthy/not healthy” convenience summaries derived from the authoritative state dimensions
- some diagnostic counters that are not required for restart correctness
- explanatory labels that can be recomputed from persisted facts and exchange state

## Persistence Principle

Persist facts that are needed to:

- recover safely,
- compare against exchange truth,
- explain the current operational condition,
- and continue deterministically after restart.

Do not persist unnecessary convenience state that risks drift.

## Transition Triggers and Event Classes

State transitions should occur only in response to explicit event classes.

## Allowed event classes

### 1. Strategy events
Examples:
- completed-bar signal confirmed
- strategy exit intent generated
- strategy stop-update intent generated
- trade-stage threshold reached

### 2. Execution submission events
Examples:
- entry submitted
- stop submitted
- stop cancel submitted
- exit submitted

### 3. User-stream order events
Examples:
- normal order accepted
- order filled
- order canceled
- order rejected
- terminal order outcome received

### 4. Account / position events
Examples:
- position opened
- position size changed
- position closed
- account update relevant to live trade state

### 5. Algo-order events
Examples:
- protective stop accepted
- protective stop triggered
- protective stop canceled
- protective stop rejected

### 6. Reconciliation events
Examples:
- reconciliation required
- reconciliation started
- clean result
- recoverable mismatch detected
- unsafe mismatch detected
- repair completed

### 7. Incident events
Examples:
- stream stale detected
- execution outcome uncertain
- protection uncertain
- credential/authorization failure
- emergency condition detected

### 8. Operator actions
Examples:
- pause enabled
- pause cleared
- kill switch enabled
- kill switch cleared
- restart requested
- recovery approved
- emergency flatten requested

### 9. Restart lifecycle events
Examples:
- process start
- safe mode entered
- prerequisites verified
- user stream restored
- recovery finished

## Transition Principle

State transitions must be driven by these explicit events, not by loosely coupled modules mutating arbitrary shared fields without a defined event reason.

## Invalid or Forbidden State Combinations

The following combinations must be treated as invalid, unsafe, or at least non-normal.

## Invalid healthy-operation combinations

- `RUNNING_HEALTHY` with `kill_switch_active=true`
- `RUNNING_HEALTHY` with `paused_by_operator=true`
- `RUNNING_HEALTHY` with reconciliation state `UNSAFE_MISMATCH`
- `RUNNING_HEALTHY` with protection state `EMERGENCY_UNPROTECTED`
- `RUNNING_HEALTHY` with `operator_review_required=true`

## Invalid exposure/protection combinations

- open position with protection state `NO_POSITION`
- open position with local steady state `POSITION_UNPROTECTED` outside a transitional emergency/recovery path
- open position with protection state `PROTECTION_UNCERTAIN` while entries remain enabled
- trade lifecycle in managed risk stage while protection is not acceptably confirmed

## Invalid trade/exchange combinations

- local `TRADE_CLOSED` while exchange still shows open position and reconciliation is not active
- local `FLAT` while exchange shows exposure and reconciliation is not active
- `POSITION_PROTECTED` without exchange-confirmed position
- `EXIT_CONFIRMED` while exchange still shows unresolved position state and no recovery flow is active

## Invalid restart/recovery combinations

- safe mode exited while reconciliation status is worse than acceptable
- recovery marked complete while user-stream restoration or equivalent live-state confidence requirement is still missing
- restart classified clean while position exists but protection cannot be confirmed

## Recommended Transition Rules

## Startup rule

On every process start:

- enter `SAFE_MODE`
- mark reconciliation as at least `REQUIRED`
- do not permit `RUNNING_HEALTHY` until restart recovery criteria are satisfied

## Entry progression rule

The normal entry progression should be:

```text
FLAT
  -> SIGNAL_CONFIRMED
  -> ENTRY_SUBMITTED
  -> ENTRY_ACKNOWLEDGED
  -> ENTRY_FILL_CONFIRMED
  -> POSITION_CONFIRMED
  -> PROTECTIVE_STOP_SUBMITTED
  -> POSITION_PROTECTED
  -> RISK_STAGE_INITIAL
```

### Important note
If any critical uncertainty occurs along this path, the runtime should transition to:

- `TRADE_EXCEPTION`
- `SAFE_MODE`
- `RECOVERING`
- or emergency handling as appropriate

rather than blindly continuing.

## Managed-trade progression rule

Once protected, the normal progression may be:

```text
RISK_STAGE_INITIAL
  -> RISK_STAGE_REDUCED
  -> RISK_STAGE_BREAKEVEN
  -> RISK_STAGE_TRAILING
  -> EXIT_PENDING
  -> EXIT_CONFIRMED
  -> TRADE_CLOSED
  -> FLAT
```

This path should remain conditional on protection staying acceptable.

## Stop-replacement rule

During stop replacement:

```text
POSITION_PROTECTED
  -> STOP_REPLACEMENT_IN_PROGRESS
  -> STOP_PENDING_CONFIRMATION
  -> POSITION_PROTECTED
```

If confirmation fails:

```text
STOP_REPLACEMENT_IN_PROGRESS
  -> PROTECTION_UNCERTAIN
  -> TRADE_EXCEPTION
  -> SAFE_MODE / RECOVERING / emergency path
```

## Reconciliation rule

If state confidence is materially lost:

```text
current mode
  -> SAFE_MODE
  -> reconciliation REQUIRED
  -> reconciliation IN_PROGRESS
  -> CLEAN or RECOVERABLE_MISMATCH or UNSAFE_MISMATCH
```

Then:

- `CLEAN` may allow controlled return toward `RUNNING_HEALTHY`
- `RECOVERABLE_MISMATCH` requires repair and recheck
- `UNSAFE_MISMATCH` requires blocked or emergency handling

## Emergency-unprotected rule

If exchange exposure exists and acceptable protective coverage cannot be confirmed:

```text
protection state
  -> EMERGENCY_UNPROTECTED
runtime mode
  -> SAFE_MODE
control flags
  -> incident_active=true
  -> operator_review_required=true
```

Then the runtime must take an emergency branch:

- restore protection if safely possible
- otherwise flatten exposure conservatively
- remain blocked until state certainty is restored and review requirements are satisfied

## Decisions

The following decisions are accepted for the v1 runtime state model:

- the runtime should use a hierarchical state model rather than one giant flat state enum
- top-level runtime modes are separate from control flags
- trade lifecycle, protection state, and reconciliation state are distinct state dimensions
- a position is not an acceptable steady live state until protective coverage is confirmed
- exchange truth is authoritative for live exposure/order/protection state
- restart always begins in `SAFE_MODE`
- `UNSAFE_MISMATCH` must prevent normal healthy operation
- emergency unprotected exposure is a first-class failure state
- restart-critical operational facts must be persisted explicitly
- state transitions should be driven by explicit event classes, not casual shared-state mutation
- invalid state combinations should be treated as design-time and runtime safety violations

## Open Questions

The following remain open for implementation detail and later architecture documents:

1. What exact persisted storage mechanism should hold runtime operational state in v1?
2. What exact timeout values should trigger transitions such as protection uncertainty or missing fill confirmation?
3. Should some convenience fields such as `entries_blocked` remain fully derived or be persisted for easier operator continuity?
4. What exact internal event format should be used for state transitions?
5. Which transitions should require durable write-before-continue discipline to maximize crash safety?
6. Should some control states such as `paused_by_operator` and `kill_switch_active` be modeled as stronger primary modes instead of flags, or is the layered model sufficient?

## Next Steps

After this document, the next recommended files are:

1. `docs/08-architecture/observability-design.md`
2. `docs/11-interface/operator-dashboard-requirements.md`
3. `docs/09-operations/release-process.md`
