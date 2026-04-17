# Internal Event Contracts

## Purpose

This document defines the internal message contract for the v1 Prometheus trading runtime.

Its purpose is to standardize how internal modules communicate by defining:

- message categories,
- the distinction between commands, events, and queries,
- the shared message envelope,
- which component may emit which kinds of messages,
- what minimum payloads important messages must carry,
- which messages should trigger durable state updates,
- and which communication shortcuts are forbidden.

This document exists because the project already has a modular architecture, a runtime state model, and a state-centric observability design.

Without a clear internal message contract, implementation is likely to drift into:

- ad hoc cross-module calls,
- hidden state mutation,
- ambiguous ownership of facts,
- and inconsistent runtime behavior.

This document is intended to prevent that.

## Scope

This document applies to the live v1 runtime and to internal communication between major components such as:

- market-data ingestion
- user-stream/account event intake
- strategy engine
- risk and sizing layer
- execution layer
- state and reconciliation layer
- safety / incident control
- operator control surface
- observability / event recording path

This document covers:

- message taxonomy,
- shared message envelope,
- emission and consumption boundaries,
- minimum payload expectations,
- durable-write trigger rules,
- and invalid communication patterns.

This document does **not** define:

- external API contracts for users,
- frontend wire protocols,
- database schema,
- the full runtime state model,
- or the final code-level transport implementation.

It defines the internal semantic contract only.

## Background

The project already defines:

- a modular-monolith implementation blueprint,
- a hierarchical runtime state model,
- a state-centric observability design,
- restart and reconciliation workflows,
- and operator-supervised control rules.

Those documents imply many important runtime transitions, but they do not yet standardize the internal protocol by which those transitions are expressed.

The runtime needs a clean distinction between:

- intentions,
- confirmed facts,
- and state reads.

This document standardizes that distinction.

## Contract Philosophy

## 1. Separate commands, events, and queries

Internal communication must distinguish clearly between:

### Commands
Requests asking a component to do something.

A command expresses intended work.

### Events
Facts that something has happened.

An event expresses observed or accepted reality.

### Queries
Requests to read current state.

A query expresses information retrieval, not state change.

This separation is mandatory.

## 2. Facts must not be inferred from intentions alone

The runtime must not treat a command as proof that the requested action succeeded.

Examples:

- a command to place an entry order is not proof that an entry exists
- a command to place a protective stop is not proof that protection exists
- a command to begin reconciliation is not proof that reconciliation succeeded

Confirmed state changes require events and/or exchange-confirmed evidence.

## 3. Module ownership must remain explicit

Each component may emit only the messages that correspond to facts or intents it legitimately owns.

This prevents the strategy layer from pretending to know exchange truth, and prevents the UI/control surface from bypassing backend safety boundaries.

## 4. Messages should be durable, explainable, and traceable

Important messages should be:

- uniquely identifiable,
- correlated to the workflow that caused them,
- timestamped in canonical UTC milliseconds,
- and rich enough to reconstruct what happened later.

## 5. Message contracts should support both runtime control and observability

The internal contract should not be one thing for execution and another unrelated thing for logging.

Important runtime messages should be usable as observability inputs as well, provided secret-redaction rules are respected.

## Message Taxonomy

The runtime should use the following top-level message classes.

## 1. Strategy Commands

Commands generated from completed-bar strategy logic.

Examples:

- evaluate strategy on completed bar
- prepare entry candidate
- prepare stop update candidate
- prepare exit candidate

These are internal intent-shaping commands and must not imply exchange-confirmed reality.

## 2. Risk and Approval Commands

Commands that ask the risk/sizing layer to evaluate whether a strategy intent may proceed.

Examples:

- evaluate trade sizing
- validate stop distance
- validate notional against caps
- approve or reject entry candidate

## 3. Execution Commands

Commands that ask the execution layer to interact with Binance.

Examples:

- submit entry order
- submit protective stop
- cancel protective stop
- replace protective stop
- submit market exit
- perform emergency flatten

## 4. Control Commands

Commands that change runtime control state or trigger operator-approved actions.

Examples:

- enable pause
- clear pause
- enable kill switch
- clear kill switch
- request controlled restart
- approve recovery resumption

## 5. Runtime Events

Internal factual events about runtime state transitions.

Examples:

- runtime mode changed
- trade lifecycle advanced
- protection state changed
- reconciliation state changed
- entries blocked state changed

## 6. Exchange-Derived Events

Events derived from exchange/user-stream/REST truth.

Examples:

- entry acknowledged
- fill confirmed
- position confirmed
- protective stop confirmed
- order rejected
- user stream marked stale
- exchange position mismatch detected

## 7. Incident and Recovery Events

Events related to confidence loss, incident classification, containment, and recovery.

Examples:

- incident opened
- incident severity assigned
- reconciliation required
- reconciliation classified unsafe mismatch
- emergency branch entered
- restart recovery completed

## 8. Queries

Read-only requests for current state.

Examples:

- get runtime summary
- get position/protection summary
- get active incidents
- get current reconciliation status
- get recent important events

## Shared Message Envelope

All important internal commands and events should use a shared semantic envelope.

## Required envelope fields

At minimum, the envelope should support:

- `message_type`
- `message_class`
- `message_id`
- `correlation_id`
- `causation_id`
- `occurred_at_utc_ms`
- `source_component`
- `symbol` where relevant
- `strategy_id` where relevant
- `payload`

## Field meanings

### `message_type`
A specific message name.

Example:
- `execution.entry_submitted`
- `protection.state_changed`
- `incident.opened`

### `message_class`
One of:
- command
- event
- query

### `message_id`
A unique identifier for this message instance.

### `correlation_id`
Groups messages belonging to the same logical workflow.

Examples:
- one trade lifecycle
- one reconciliation attempt
- one restart flow
- one incident

### `causation_id`
References the specific prior message that caused this message, where applicable.

This helps trace chains such as:

signal confirmed  
→ entry command issued  
→ entry submitted event  
→ fill confirmed event  
→ stop placement command

### `occurred_at_utc_ms`
Canonical UTC millisecond timestamp for the message.

### `source_component`
The component that emitted the message.

Examples:
- `strategy_engine`
- `execution_layer`
- `state_reconciliation`
- `incident_control`
- `operator_control`

### `symbol`
Required where the message is symbol-specific.

For v1, usually `BTCUSDT`.

### `strategy_id`
Useful where strategy variant identity matters.

### `payload`
Message-specific data.

## Envelope rules

### Rule 1
Every important runtime event should be traceable through `message_id`, `correlation_id`, and where meaningful `causation_id`.

### Rule 2
Messages should use canonical UTC millisecond timestamps.

### Rule 3
Envelope fields must not contain secret material.

## Component Ownership and Allowed Emissions

Ownership rules are mandatory.

## Market-Data Ingestion Layer

### May emit
- completed bar available
- market-data freshness degraded
- market-data marked stale
- market-data restored

### Must not emit
- position confirmed
- protection confirmed
- reconciliation clean
- incident resolved

## User-Stream / Account Event Layer

### May emit
- order update received
- account update received
- algo update received
- user stream connected/disconnected/stale/restored

### Must not emit
- strategy signal confirmed
- risk approved
- operator recovery approved

## Strategy Engine

### May emit
- strategy signal confirmed
- stop update intent generated
- exit intent generated
- no-trade decision generated

### Must not emit
- entry filled
- position confirmed
- protection confirmed
- reconciliation result
- incident severity set

## Risk and Sizing Layer

### May emit
- entry approved
- entry rejected
- sizing computed
- risk gate blocked

### Must not emit
- fill confirmed
- order submitted
- position protected
- user stream stale

## Execution Layer

### May emit
- entry submission started
- entry submitted
- protective stop submission started
- protective stop submitted
- stop replacement started
- exit submission started
- execution uncertainty detected
- order placement rejected at local/exchange boundary

### Must not emit
- final fill confirmation unless confirmed from exchange/user-stream truth path
- reconciliation classified clean/unsafe
- incident resolved
- strategy signal confirmed

## State and Reconciliation Layer

### May emit
- trade lifecycle state changed
- protection state changed
- reconciliation required
- reconciliation started
- reconciliation classified clean
- reconciliation classified recoverable mismatch
- reconciliation classified unsafe mismatch
- repair action required
- repair action succeeded/failed

### Must not emit
- raw strategy signal confirmed
- kill switch enabled by itself unless acting through approved control flow
- discretionary operator decisions

## Safety / Incident Control Layer

### May emit
- incident opened
- severity assigned
- containment action recorded
- operator review required
- emergency branch entered
- entries blocked state changed

### Must not emit
- exchange fill confirmed
- strategy signal confirmed
- public market-data events as if it owns them

## Operator Control Layer

### May emit
- pause requested
- pause cleared
- kill switch requested
- restart requested
- recovery approval submitted
- emergency flatten requested
- operator action recorded

### Must not emit directly
- exchange truth facts
- reconciliation classified clean
- protection confirmed

These must come from backend-controlled state or exchange-derived paths.

## Command Contracts

The following command families should be standardized.

## Strategy Command Family

### `strategy.evaluate_completed_bar`
Purpose:
- ask the strategy engine to evaluate a newly completed bar

Minimum payload:
- symbol
- timeframe
- completed bar reference
- latest completed higher-timeframe reference
- entries currently allowed yes/no

### `strategy.prepare_stop_update`
Purpose:
- ask the strategy engine whether a managed-trade stop update intent exists

Minimum payload:
- symbol
- trade reference
- current risk stage
- completed bar reference

### `strategy.prepare_exit`
Purpose:
- ask the strategy engine whether a strategy exit intent exists

Minimum payload:
- symbol
- trade reference
- completed bar reference

## Risk Command Family

### `risk.evaluate_entry_candidate`
Purpose:
- ask the risk layer to approve/reject and size an entry candidate

Minimum payload:
- symbol
- signal side
- proposed entry reference
- proposed stop reference
- account equity/risk reference
- strategy version
- config version

### `risk.validate_stop_update`
Purpose:
- confirm proposed stop update remains valid under runtime controls

Minimum payload:
- symbol
- trade reference
- current position reference
- proposed stop reference

## Execution Command Family

### `execution.submit_entry_order`
Purpose:
- instruct execution to place a market entry order

Minimum payload:
- symbol
- side
- quantity
- order role
- correlation_id / trade reference
- approved risk reference

### `execution.submit_protective_stop`
Purpose:
- instruct execution to place initial protective stop

Minimum payload:
- symbol
- stop role
- trigger price
- working type
- closePosition flag
- correlation_id / trade reference

### `execution.replace_protective_stop`
Purpose:
- instruct execution to perform cancel-and-replace stop workflow

Minimum payload:
- symbol
- current stop reference
- replacement stop specification
- trade reference

### `execution.submit_exit_order`
Purpose:
- instruct execution to flatten/exit the current position

Minimum payload:
- symbol
- exit reason
- trade reference
- side / role as needed

### `execution.emergency_flatten`
Purpose:
- instruct execution to flatten exposure under emergency handling

Minimum payload:
- symbol
- emergency reason
- incident reference
- trade reference if known

## Control Command Family

### `control.enable_pause`
Minimum payload:
- operator/action source
- reason

### `control.clear_pause`
Minimum payload:
- operator/action source
- reason

### `control.enable_kill_switch`
Minimum payload:
- operator/action source
- reason

### `control.clear_kill_switch`
Minimum payload:
- operator/action source
- reason

### `control.request_restart`
Minimum payload:
- operator/action source
- reason

### `control.approve_recovery_resumption`
Minimum payload:
- operator/action source
- reason
- recovery/reconciliation reference

## Event Contracts

Important event families should define minimum payload expectations.

## Strategy Event Family

### `strategy.signal_confirmed`
Minimum payload:
- symbol
- signal side
- strategy version
- signal bar open time
- signal bar close time
- setup reference
- higher-timeframe reference

### `strategy.stop_update_intent_generated`
Minimum payload:
- symbol
- trade reference
- intended next risk/protection stage
- proposed stop reference
- reason

### `strategy.exit_intent_generated`
Minimum payload:
- symbol
- trade reference
- exit reason
- completed bar reference

## Risk Event Family

### `risk.entry_approved`
Minimum payload:
- symbol
- trade reference
- approved quantity
- approved stop reference
- effective risk amount
- approval reason

### `risk.entry_rejected`
Minimum payload:
- symbol
- trade reference
- rejection reason
- gating category

## Execution Event Family

### `execution.entry_submitted`
Minimum payload:
- symbol
- trade reference
- client order id
- side
- quantity
- order role

### `execution.entry_acknowledged`
Minimum payload:
- symbol
- trade reference
- client order id
- exchange order id if known
- acknowledgement type

### `execution.protective_stop_submitted`
Minimum payload:
- symbol
- trade reference
- stop client order id
- stop trigger reference
- stop role

### `execution.stop_replacement_started`
Minimum payload:
- symbol
- trade reference
- prior stop reference
- replacement stop reference

### `execution.uncertainty_detected`
Minimum payload:
- symbol
- trade reference if known
- affected action
- uncertainty reason
- exposure ambiguity yes/no

## Exchange-Derived Event Family

### `exchange.fill_confirmed`
Minimum payload:
- symbol
- trade reference
- client order id
- exchange order id
- filled quantity
- average fill price
- event time

### `exchange.position_confirmed`
Minimum payload:
- symbol
- trade reference if known
- side
- size
- average entry price if known
- confirmation source

### `exchange.protective_stop_confirmed`
Minimum payload:
- symbol
- trade reference
- stop client order id
- stop exchange order id if known
- confirmation source
- event time

### `exchange.order_rejected`
Minimum payload:
- symbol
- client order id
- exchange order id if known
- rejection category
- rejection detail

### `exchange.user_stream_stale`
Minimum payload:
- symbol if relevant
- stale reason
- last known healthy timestamp

## Runtime State Event Family

### `runtime.mode_changed`
Minimum payload:
- previous mode
- new mode
- reason
- operator review required yes/no

### `trade.lifecycle_changed`
Minimum payload:
- symbol
- trade reference
- previous state
- new state
- triggering reason

### `protection.state_changed`
Minimum payload:
- symbol
- trade reference
- previous protection state
- new protection state
- related stop reference if any
- reason

### `reconciliation.state_changed`
Minimum payload:
- symbol if relevant
- previous reconciliation state
- new reconciliation state
- reason
- repair required yes/no

## Incident Event Family

### `incident.opened`
Minimum payload:
- incident id
- incident class
- severity
- symbol if relevant
- exposure present yes/no
- protection confirmed yes/no
- triggering reason

### `incident.severity_updated`
Minimum payload:
- incident id
- previous severity
- new severity
- reason

### `incident.operator_review_required`
Minimum payload:
- incident id
- reason
- blocked state required yes/no

### `incident.resolution_changed`
Minimum payload:
- incident id
- previous resolution state
- new resolution state
- reason

## Operator Action Event Family

### `operator.action_recorded`
Minimum payload:
- action type
- operator identity or alias where available
- reason
- affected symbol if relevant
- resulting state change summary

## Query Contracts

Queries are read-only and must not mutate runtime state.

## Required query families

### `query.runtime_summary`
Returns:
- runtime mode
- entries allowed
- incident active
- operator review required
- kill switch state
- pause state

### `query.position_protection_summary`
Returns:
- position present
- side
- size
- trade lifecycle state
- protection state
- protective stop present
- last protection confirmation

### `query.reconciliation_summary`
Returns:
- reconciliation state
- last successful reconciliation
- mismatch summary if present
- recovery active yes/no

### `query.active_incidents`
Returns:
- active incidents
- highest severity
- escalation pending
- containment status

### `query.recent_important_events`
Returns:
- recent mode changes
- execution events
- incident events
- operator actions
- restart/reconciliation events

## Query rules

### Rule 1
Queries must not perform hidden state mutation.

### Rule 2
Queries may return derived summaries, but the underlying authoritative state must still be well-defined elsewhere.

## Durable-Write and Persistence Trigger Rules

Some messages should trigger durable persistence before the runtime proceeds.

## Messages that should normally trigger durable state persistence

### Runtime/control changes
- `runtime.mode_changed`
- pause enabled/cleared
- kill switch enabled/cleared
- operator review required set/cleared
- entries blocked state changed

### Trade lifecycle changes
- `trade.lifecycle_changed`

### Protection changes
- `protection.state_changed`

### Reconciliation changes
- `reconciliation.state_changed`

### Operator actions
- `operator.action_recorded`

### Emergency/incident branch changes
- `incident.opened`
- emergency branch entered
- incident resolution state changed where relevant

## Persistence principle

If losing a message on crash would make restart or recovery meaningfully less safe, that message should be persisted durably before the runtime proceeds past the associated transition.

## Important note

This document defines which message types are persistence-critical.

The exact storage mechanism, write semantics, and atomicity details should be finalized in the runtime persistence specification.

## Invalid Patterns and Forbidden Shortcuts

The following patterns are explicitly forbidden.

## 1. Direct hidden state mutation across modules

A module must not directly mutate another module’s internal state as an implicit shortcut.

State changes must occur through explicit commands/events and controlled state ownership.

## 2. Treating commands as confirmed facts

The runtime must not treat:

- `execution.submit_entry_order`
- `execution.submit_protective_stop`
- `execution.replace_protective_stop`

as equivalent to confirmed exchange truth.

## 3. Strategy claiming exchange truth

The strategy engine must not emit messages such as:

- fill confirmed
- position confirmed
- position protected
- reconciliation clean

Those are outside strategy ownership.

## 4. Frontend/control layer bypassing backend safety boundaries

The operator-facing control surface must not directly emit exchange-truth events or bypass controlled backend action paths.

## 5. Events used as hidden commands

A component must not emit an event that semantically means “please do X” while labeling it as a fact.

Commands and events must remain distinct.

## 6. Query-driven mutation

Queries must not mutate runtime state as a hidden side effect.

## 7. Missing correlation on important workflows

Important workflows such as:

- trade lifecycle
- restart/recovery
- reconciliation
- incident handling

must not proceed through uncorrelated message chains that cannot be reconstructed later.

## 8. Secret material in message payloads

Messages must not include raw secret values, secret-bearing config dumps, or sensitive credential payloads.

## Decisions

The following decisions are accepted for the v1 internal event contract:

- internal runtime communication must distinguish commands, events, and queries
- important messages should use a shared semantic envelope
- module ownership boundaries determine which messages a component may emit
- commands are intentions, not confirmed facts
- exchange-confirmed truth must be represented by exchange-derived events
- important workflows must be traceable through message IDs and correlation IDs
- persistence-critical state transitions should be triggered by explicit messages
- direct hidden cross-module state mutation is forbidden
- queries must be read-only
- the operator/control surface must interact through backend-approved command paths, not by bypassing runtime safety boundaries

## Open Questions

The following remain open for later implementation detail:

1. What exact in-process transport style should implement these contracts in the modular monolith?
2. Which messages should be emitted synchronously versus asynchronously inside the runtime?
3. Which message payload fields should become mandatory in code-level schemas versus optional extensions?
4. Which persistence-critical message transitions require write-before-continue semantics for maximum crash safety?
5. Should some queries be implemented as direct state-store reads while others are materialized summaries?

## Next Steps

After this document, the next recommended files are:

1. `docs/08-architecture/runtime-persistence-spec.md`
2. `docs/08-architecture/codebase-structure.md`
3. `docs/00-meta/ai-coding-handoff.md`
