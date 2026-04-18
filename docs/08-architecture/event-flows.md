# Event Flows

## Purpose

This document defines the core event and command flows for the v1 Prometheus trading system.

Its purpose is to make implementation behavior explicit enough that the runtime can be built without accidentally violating the project’s most important safety rules:

- commands are not facts,
- REST acknowledgements are not final truth,
- a filled entry is not yet a protected trade,
- a submitted stop is not yet confirmed protection,
- unknown execution outcomes fail closed,
- restart begins in safe mode,
- exchange state is authoritative,
- and live operation may continue only when state certainty is acceptable.

This document replaces the previous TBD placeholder for:

```text
docs/08-architecture/event-flows.md
```

The document is intentionally sequence-oriented. It is designed to help implementation tools and human reviewers understand what should happen, in what order, which component owns each step, and which branches must block or escalate.

---

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures
- first live symbol: BTCUSDT perpetual
- first secondary research comparison: ETHUSDT perpetual
- v1 live scope: BTCUSDT only
- strategy family: breakout continuation with higher-timeframe trend filter
- signal timeframe: 15m
- higher-timeframe bias: 1h
- entry method: market entry after completed-bar confirmation
- position mode: one-way mode
- margin mode: isolated margin
- max live positions: one
- max active protective stop: one
- no pyramiding
- no reversal entry while positioned
- protective stop: exchange-side algo `STOP_MARKET`
- protective stop settings:
  - `closePosition=true`
  - `workingType=MARK_PRICE`
  - `priceProtect=TRUE`
- user stream is the primary live private-state source
- REST is used for placement, cancellation, reconciliation, and recovery
- restart always begins in safe mode
- exchange state is authoritative
- deployment is staged and operator-supervised

This document covers:

- flow notation,
- shared module boundaries,
- shared command/event rules,
- durable-write markers,
- normal trading flows,
- trade-management flows,
- restart and recovery flows,
- failure and emergency flows,
- risk-control flows,
- kill-switch flows,
- cross-flow invariants,
- persistence expectations,
- observability expectations,
- and testing requirements.

This document does **not** define:

- final code-level classes,
- database tables,
- exchange endpoint wrappers,
- frontend layout,
- deployment topology,
- full incident runbooks,
- or final implementation schedule.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/04-data/live-data-spec.md`
- `docs/04-data/timestamp-policy.md`
- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/binance-usdm-order-model.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/06-execution-exchange/user-stream-reconciliation.md`
- `docs/06-execution-exchange/failure-recovery.md`
- `docs/06-execution-exchange/position-state-model.md`
- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/07-risk/kill-switches.md`
- `docs/08-architecture/implementation-blueprint.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/operator-workflow.md`
- `docs/09-operations/daily-weekly-review-process.md`
- `docs/11-interface/operator-dashboard-requirements.md`

### Authority hierarchy

If this document conflicts with the state model on runtime modes, trade lifecycle states, protection states, or reconciliation states, the state model wins.

If this document conflicts with execution/exchange documents on Binance order behavior, the execution/exchange documents win.

If this document conflicts with stop-loss policy on protective-stop emergency behavior, the stop-loss policy wins.

If this document conflicts with incident response on severity and escalation, incident response wins.

If this document conflicts with runtime persistence on durable-write requirements, runtime persistence wins.

If this document conflicts with the timestamp policy on completed-bar or UTC timestamp handling, timestamp policy wins.

---

## Core Principles

## 1. Flows must preserve command/event separation

A command asks a component to do something.

An event records that something happened.

A query reads state.

No implementation flow may treat a command as proof that the requested action succeeded.

Examples:

```text
execution.submit_entry_order command
  != entry filled
  != position exists
  != trade protected
```

```text
execution.submit_protective_stop command
  != stop exists
  != position protected
```

## 2. Exchange-derived facts drive execution truth

Exchange-derived events and reconciliation reads determine:

- whether an entry order exists,
- whether an entry filled,
- whether a position exists,
- whether a protective stop exists,
- whether a position is flat,
- and whether local state matches exchange state.

Local state is useful for continuity, but it does not outrank exchange truth.

## 3. New exposure is blocked during uncertainty

If the runtime cannot confidently answer whether there is:

- an entry in flight,
- an open position,
- an active protective stop,
- unknown execution status,
- manual exposure,
- stale critical stream state,
- or unresolved reconciliation mismatch,

then new entries must remain blocked.

## 4. Protection is a separate flow stage

A live trade does not become operationally acceptable when the entry fills.

A live trade becomes operationally acceptable only after:

1. position existence is confirmed,
2. ownership is classified,
3. protective stop is submitted,
4. protective stop existence is confirmed,
5. and reconciliation/protection state is acceptable.

## 5. Failure branches are part of the flow

Every implementation flow must include uncertainty and failure paths.

The happy path alone is insufficient for a live futures trading system.

## 6. Persistence occurs at safety boundaries

If losing a transition during a crash would make restart behavior less safe, the transition must be persisted before continuing.

This document marks those points as:

```text
[PERSIST BEFORE CONTINUE]
```

## 7. Observability follows the same event model

Important commands, events, state changes, and operator actions should leave structured event records.

Observability is not separate from runtime truth. It is the reviewable trail of runtime truth, uncertainty, repair, and operator decisions.

---

## Flow Notation

This document uses text sequence flows.

### Component line format

```text
ComponentA
  -> ComponentB: message.name
```

### State update format

```text
RuntimeState
  -> RuntimeState: runtime_mode = SAFE_MODE
```

### Durable write marker

```text
[PERSIST BEFORE CONTINUE]
```

This means the implementation should durably write the associated state transition or continuity record before proceeding to the next safety-relevant step.

### Blocking marker

```text
[BLOCK ENTRIES]
```

This means no new strategy-generated live entry may be submitted while the condition remains active.

### Reconciliation marker

```text
[RECONCILE]
```

This means the state/reconciliation layer must compare local continuity state with exchange state before normal progression may continue.

### Escalation marker

```text
[ESCALATE]
```

This means incident or operator-review policy applies.

### Emergency marker

```text
[EMERGENCY]
```

This means the runtime has entered a high-severity exposure-risk branch, typically involving unprotected or uncertain live exposure.

### Example

```text
ExecutionLayer
  -> ExchangeAdapter: execution.submit_entry_order
ExchangeAdapter
  -> ExecutionLayer: execution.entry_submitted
RuntimeState
  -> RuntimeState: trade_lifecycle_state = ENTRY_SUBMITTED
[PERSIST BEFORE CONTINUE]
UserStream
  -> StateReconciliation: exchange.entry_fill_confirmed
```

---

## Shared Components

The flows use the following logical components.

## MarketDataLayer

Owns:

- public market-data stream intake,
- completed-bar publication,
- market-data freshness state,
- mark-price reference intake,
- REST bar backfill for market-data recovery.

Must not own:

- position truth,
- order truth,
- protection truth,
- risk approval,
- or operator clearance.

## StrategyEngine

Owns:

- completed-bar strategy evaluation,
- higher-timeframe bias logic,
- setup and trigger logic,
- strategy-side stop update intent,
- strategy-side exit intent.

Must not own:

- sizing approval,
- order placement,
- fill confirmation,
- position confirmation,
- or stop confirmation.

## RiskLayer

Owns:

- stop validation,
- sizing calculation,
- exposure gates,
- notional/leverage gates,
- daily loss and drawdown gates where relevant,
- entry approval or rejection.

Must not own:

- strategy signal generation,
- exchange order submission,
- user-stream event truth,
- or operator emergency actions.

## ExecutionLayer

Owns:

- expression of approved actions as exchange commands,
- entry order submission,
- protective stop submission,
- stop cancel-and-replace workflow,
- market exit submission,
- emergency flatten submission when requested by safety policy,
- deterministic client ID usage.

Must not own:

- strategy desirability,
- final exchange truth,
- incident clearance,
- or operator approval.

## ExchangeAdapter

Owns:

- Binance-specific REST/WebSocket boundary,
- signing and credentials boundary,
- request dispatch,
- rate-limit discipline,
- response normalization,
- error/uncertainty classification.

Must not own:

- runtime state transitions,
- risk decisions,
- incident severity decisions,
- or operator approval decisions.

## UserStreamLayer

Owns:

- private user-stream lifecycle,
- listen-key upkeep,
- private event intake,
- private event normalization,
- private stream health classification.

Must not own:

- reconciliation outcome classification,
- clean-flat decisions,
- or operator clearance.

## StateReconciliationLayer

Owns:

- local-versus-exchange state comparison,
- order/position/protection truth classification,
- clean/recoverable/unsafe mismatch classification,
- position ownership classification,
- trade lifecycle state transition recommendations,
- recovery state transitions.

Must not own:

- discretionary trading decisions,
- Binance request signing,
- or UI-only presentation logic.

## SafetyIncidentLayer

Owns:

- incident classification,
- emergency branch activation,
- kill-switch activation policy,
- operator review requirements,
- containment decisions,
- recovery clearance prerequisites.

Must not own:

- raw exchange request execution,
- strategy signal generation,
- or hidden state mutation.

## OperatorControlSurface

Owns:

- operator commands,
- acknowledgements,
- pause/kill switch request surfaces,
- recovery approval/denial inputs,
- emergency action confirmation where required.

Must not own:

- direct exchange credentials,
- direct order submission,
- bypassing backend safety gates,
- or discretionary manual trading workflows.

## RuntimeState

Owns:

- current top-level runtime mode,
- control flags,
- trade lifecycle state,
- protection state,
- reconciliation state,
- active incident continuity,
- entries-blocked state.

All mutation must happen through explicit state-owned transitions driven by valid commands/events.

## PersistenceLayer

Owns:

- durable writes of restart-critical records,
- active trade continuity records,
- protection continuity records,
- reconciliation records,
- control state records,
- operator action records,
- incident continuity records.

Must not own:

- interpretation of exchange truth,
- risk approval,
- or strategy decisions.

## ObservabilityLayer

Owns:

- structured event recording,
- health indicators,
- alert emission,
- review-support records,
- redacted logs.

Must not become a hidden state authority.

---

## Shared Event and Command Rules

## Message envelope

Important commands and events should carry at least:

```text
message_type
message_class
message_id
correlation_id
causation_id
occurred_at_utc_ms
source_component
symbol where relevant
strategy_id where relevant
payload
```

## Correlation rule

All messages in a trade attempt should share a trade-level correlation reference.

Examples:

```text
signal confirmed
  -> risk approval
  -> entry submission
  -> fill confirmation
  -> protective stop submission
  -> stop confirmation
```

should be traceable as one workflow.

## Causation rule

Each downstream command/event should reference the message that caused it when practical.

Example:

```text
strategy.signal_confirmed
  causes risk.evaluate_entry_candidate
```

```text
risk.entry_approved
  causes execution.submit_entry_order
```

## Timestamp rule

All canonical timestamps must use UTC Unix milliseconds.

Human-readable timestamps may be displayed, but they must derive from canonical timestamps.

## Secret rule

No internal message, event payload, persistence record, log line, or dashboard summary may contain API secrets, request signatures, private keys, or unredacted credential material.

---

## Shared Runtime Gates

Before any live entry path reaches order submission, all of the following must be true:

```text
runtime_mode permits live entry
entries_blocked = false
kill_switch_active = false
paused_by_operator = false
operator_review_required = false
incident_active does not block entry
reconciliation_state is acceptable
market_data_health is acceptable
user_stream_health is acceptable for entry path
symbol is allowed for live v1
account mode is one-way
position side model is one-way/BOTH
margin mode is isolated
no position exists
no entry order is in flight
no unknown execution outcome exists
no manual/non-bot exposure exists
no stale strategy-owned order exists
no active protective stop exists while flat unless cleanup is in progress
risk approval is current
exchange metadata is current enough for order validation
```

If any required gate fails:

```text
RiskLayer / RuntimeState
  -> StrategyEngine: entry blocked / no live order path
```

The strategy may still evaluate signals for diagnostics or paper/shadow analysis if explicitly configured, but it must not produce a live exchange command while live gates are blocked.

---

## Durable Write Markers

The following transitions normally require durable persistence before continuation:

### Runtime/control transitions

- runtime mode changed,
- entries blocked changed,
- operator pause enabled or cleared,
- kill switch enabled or cleared,
- operator review required set or cleared.

### Trade lifecycle transitions

- signal confirmed,
- entry submitted,
- entry acknowledged if tracked,
- entry fill confirmed,
- position confirmed,
- exit submitted,
- exit confirmed,
- trade closed.

### Protection transitions

- protective stop submission started,
- protective stop submitted,
- protective stop confirmed,
- stop replacement started,
- old stop cancel requested,
- old stop cancel confirmed,
- replacement stop submitted,
- replacement stop confirmed,
- protection uncertainty entered,
- emergency unprotected state entered.

### Reconciliation/recovery transitions

- reconciliation required,
- reconciliation started,
- reconciliation classified clean,
- reconciliation classified recoverable mismatch,
- reconciliation classified unsafe mismatch,
- repair action started,
- repair action completed,
- restart context initialized,
- recovery completed.

### Incident/operator transitions

- incident opened,
- incident severity escalated,
- emergency branch entered,
- emergency flatten requested,
- operator action recorded,
- operator approval recorded,
- incident resolution state changed.

---

# Core Trading Flows

## Flow 1 — Completed-Bar Signal Evaluation

## Purpose

This flow converts a strategy-ready completed 15m bar into either:

- no action,
- a diagnostic no-trade reason,
- or a candidate entry signal.

It must preserve the completed-bar-only policy.

## Preconditions

- Market-data layer is connected or recently recovered.
- A BTCUSDT 15m bar is confirmed closed.
- Higher-timeframe 1h context is available from a completed 1h bar.
- Partial candles are not used for strategy decisions.
- Runtime is allowed to evaluate strategy logic for the current environment.

## Normal sequence

```text
MarketDataLayer
  -> MarketDataLayer: receive kline update
MarketDataLayer
  -> MarketDataLayer: verify kline is closed
MarketDataLayer
  -> MarketDataLayer: verify completed-bar continuity
MarketDataLayer
  -> MarketDataLayer: update market-data freshness state
MarketDataLayer
  -> StrategyEngine: market.completed_bar_available
StrategyEngine
  -> StrategyEngine: load latest completed 15m history
StrategyEngine
  -> StrategyEngine: load latest completed 1h bias context
StrategyEngine
  -> StrategyEngine: evaluate v1 breakout rules
```

If no signal exists:

```text
StrategyEngine
  -> ObservabilityLayer: strategy.no_trade_decision_recorded
```

If a candidate signal exists:

```text
StrategyEngine
  -> RuntimeState: trade_lifecycle_state = SIGNAL_CONFIRMED
[PERSIST BEFORE CONTINUE]
StrategyEngine
  -> RiskLayer: risk.evaluate_entry_candidate
```

## Required candidate signal payload

At minimum:

```text
symbol
strategy_id
strategy_version
config_version
signal_time_utc_ms
signal_bar_open_time_utc_ms
signal_bar_close_time_utc_ms
side
setup_reference
higher_timeframe_bias_reference
proposed_entry_reference
initial_strategy_stop
atr_reference
no_trade_filters_passed
correlation_id
```

## Failure / block branches

### Partial candle received

```text
MarketDataLayer
  -> MarketDataLayer: classify as partial candle
MarketDataLayer
  -> ObservabilityLayer: market.partial_candle_observed
```

No strategy evaluation may occur from this update.

### Market data stale

```text
MarketDataLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
MarketDataLayer
  -> ObservabilityLayer: market_data.marked_stale
```

If no exposure exists, the runtime may remain in a degraded non-emergency state.

If exposure exists and trade management depends on the stale feed, incident policy applies.

### Higher-timeframe context missing or not completed

```text
StrategyEngine
  -> ObservabilityLayer: strategy.no_trade_missing_completed_1h_context
```

No live signal may be produced.

## Required outcome

A completed-bar signal flow ends in exactly one of:

```text
NO_ACTION
NO_TRADE_FILTERED
CANDIDATE_SIGNAL_CREATED
EVALUATION_BLOCKED_DUE_TO_DATA_UNCERTAINTY
```

---

## Flow 2 — Signal to Risk Approval

## Purpose

This flow converts a candidate strategy signal into either:

- approved executable trade parameters,
- or a clear risk rejection.

## Preconditions

- Candidate signal exists from completed-bar strategy logic.
- Initial strategy stop exists.
- Runtime entry gates are checked before submission.
- Required account/equity/metadata state is available.

## Normal sequence

```text
StrategyEngine
  -> RiskLayer: risk.evaluate_entry_candidate
RiskLayer
  -> RuntimeState: query current runtime gates
RiskLayer
  -> StateReconciliationLayer: query current exposure/protection summary
RiskLayer
  -> RiskLayer: validate symbol is BTCUSDT live-approved
RiskLayer
  -> RiskLayer: validate no position / no in-flight entry / no unknown exposure
RiskLayer
  -> RiskLayer: validate stop exists and side is correct
RiskLayer
  -> RiskLayer: validate stop distance and ATR filters
RiskLayer
  -> RiskLayer: validate sizing equity and risk fraction
RiskLayer
  -> RiskLayer: calculate risk-based quantity
RiskLayer
  -> RiskLayer: apply risk-usage buffer
RiskLayer
  -> RiskLayer: apply exchange quantity/price rules
RiskLayer
  -> RiskLayer: apply leverage cap and notional cap
RiskLayer
  -> RiskLayer: apply daily loss and drawdown gates
```

If approved:

```text
RiskLayer
  -> ObservabilityLayer: risk.entry_approved
RiskLayer
  -> ExecutionLayer: execution.submit_entry_order
```

If rejected:

```text
RiskLayer
  -> ObservabilityLayer: risk.entry_rejected
RiskLayer
  -> RuntimeState: trade_lifecycle_state = FLAT or blocked candidate state
[PERSIST BEFORE CONTINUE if lifecycle changed]
```

## Required approval payload

At minimum:

```text
symbol
side
approved_quantity
proposed_entry_reference
approved_initial_stop
risk_amount_usdt
risk_fraction
risk_usage_fraction
sizing_equity_usdt
estimated_notional_usdt
estimated_effective_leverage
metadata_snapshot_reference
strategy_signal_reference
config_version
correlation_id
```

## Rejection examples

Reject if any of the following apply:

- stop missing,
- stop invalid for side,
- stop distance outside allowed ATR range,
- quantity below minimum after rounding down,
- notional cap exceeded,
- leverage cap exceeded,
- margin mode not isolated,
- position mode not one-way,
- live symbol not approved,
- entry already in flight,
- existing position exists,
- manual/non-bot exposure exists,
- protective stop uncertainty exists,
- unknown execution outcome exists,
- daily lockout active,
- drawdown pause active,
- kill switch active,
- operator pause active,
- unresolved incident active,
- exchange metadata missing or stale.

## Failure / block branches

### Missing risk state

```text
RiskLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
RiskLayer
  -> ObservabilityLayer: risk.entry_rejected_missing_state
```

### Existing or possible exposure

```text
RiskLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
RiskLayer
  -> ObservabilityLayer: risk.entry_rejected_existing_or_possible_exposure
```

### Manual/non-bot exposure detected

```text
RiskLayer
  -> SafetyIncidentLayer: incident.open_external_exposure_warning_or_block
SafetyIncidentLayer
  -> RuntimeState: operator_review_required = true
[PERSIST BEFORE CONTINUE]
```

## Required outcome

Risk evaluation ends in exactly one of:

```text
ENTRY_APPROVED
ENTRY_REJECTED
ENTRY_BLOCKED_UNCERTAIN_STATE
OPERATOR_REVIEW_REQUIRED
```

---

## Flow 3 — Entry to Position Confirmation

## Purpose

This flow submits the approved market entry and confirms whether a position actually exists.

It must not treat REST acknowledgement as final truth.

## Preconditions

- Risk approval is current.
- No position exists.
- No in-flight entry exists.
- No unknown exposure exists.
- Required live gates are open.
- User stream is healthy enough for live entry path or recovery policy explicitly allows placement with immediate reconciliation safeguards.

## Normal sequence

```text
RiskLayer
  -> ExecutionLayer: execution.submit_entry_order
ExecutionLayer
  -> RuntimeState: trade_lifecycle_state = ENTRY_SUBMITTED
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: submit normal MARKET order
ExchangeAdapter
  -> ExecutionLayer: execution.entry_submission_acknowledged
ExecutionLayer
  -> RuntimeState: trade_lifecycle_state = ENTRY_ACKNOWLEDGED
[PERSIST BEFORE CONTINUE]
UserStreamLayer
  -> StateReconciliationLayer: exchange.order_trade_update_received
StateReconciliationLayer
  -> StateReconciliationLayer: classify entry fill evidence
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = ENTRY_FILL_CONFIRMED
[PERSIST BEFORE CONTINUE]
UserStreamLayer / ExchangeAdapter REST
  -> StateReconciliationLayer: exchange.position_fact_received
StateReconciliationLayer
  -> StateReconciliationLayer: normalize Binance position fact
StateReconciliationLayer
  -> StateReconciliationLayer: classify position ownership
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = POSITION_CONFIRMED
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ExecutionLayer: execution.submit_protective_stop
```

## Required entry submission payload

At minimum:

```text
symbol
side
quantity
order_role = ENTRY
client_order_id
strategy_id
config_version
risk_approval_reference
correlation_id
```

## Required fill confirmation evidence

At least one exchange-derived source should support fill confirmation:

- valid `ORDER_TRADE_UPDATE` fill event,
- or REST order query result classified as filled during recovery,
- plus position confirmation through `ACCOUNT_UPDATE` or REST position query where needed.

## Failure / uncertainty branches

### REST timeout after submit

```text
ExchangeAdapter
  -> ExecutionLayer: execution.submission_unknown
ExecutionLayer
  -> RuntimeState: runtime_mode = SAFE_MODE or RECOVERING
ExecutionLayer
  -> RuntimeState: entries_blocked = true
ExecutionLayer
  -> RuntimeState: trade_lifecycle_state = ENTRY_SUBMITTED or UNKNOWN_EXECUTION_OUTCOME
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> StateReconciliationLayer: reconciliation.required
[RECONCILE]
```

No blind retry is allowed.

### Exchange rejection before exposure

```text
ExchangeAdapter
  -> ExecutionLayer: execution.entry_rejected
ExecutionLayer
  -> StateReconciliationLayer: verify no position exists if needed
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = FLAT
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ObservabilityLayer: execution.entry_rejected
```

If the rejection reason suggests account, permission, margin, symbol, or mode inconsistency, block entries until reviewed.

### Partial fill

```text
UserStreamLayer
  -> StateReconciliationLayer: exchange.partial_fill_detected
StateReconciliationLayer
  -> RuntimeState: entries_blocked = true
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = ENTRY_FILL_CONFIRMED
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> StateReconciliationLayer: confirm current position size
StateReconciliationLayer
  -> ExecutionLayer: execution.submit_protective_stop if exposure exists and deterministic
```

Partial exposure must not be ignored.

### Fill evidence but position not confirmed

```text
StateReconciliationLayer
  -> RuntimeState: runtime_mode = RECOVERING
StateReconciliationLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ExchangeAdapter: query position state
```

Do not proceed to normal trade management until position state is confirmed.

## Required outcome

Entry flow ends in exactly one of:

```text
POSITION_CONFIRMED_AND_STOP_FLOW_STARTED
ENTRY_REJECTED_FLAT_CONFIRMED
UNKNOWN_EXECUTION_OUTCOME_RECONCILIATION_REQUIRED
PARTIAL_EXPOSURE_PROTECTION_REQUIRED
UNSAFE_MISMATCH_OPERATOR_REVIEW_REQUIRED
```

---

## Flow 4 — Position to Protective Stop Confirmation

## Purpose

This flow converts a confirmed position into a confirmed protected position.

It is one of the most safety-critical flows in the system.

## Preconditions

- Position exists.
- Position side and size are known enough to determine the closing side.
- Position ownership is strategy-owned or safely recoverable strategy-owned.
- Risk-approved stop is available.
- Stop price is exchange-valid or can be adjusted within approved risk tolerance.
- No conflicting active protective stop exists.

## Normal sequence

```text
StateReconciliationLayer
  -> ExecutionLayer: execution.submit_protective_stop
ExecutionLayer
  -> RuntimeState: protection_state = STOP_SUBMISSION_STARTED
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: submit algo STOP_MARKET protective stop
ExchangeAdapter
  -> ExecutionLayer: execution.protective_stop_submitted
ExecutionLayer
  -> RuntimeState: protection_state = STOP_SUBMITTED_UNCONFIRMED
[PERSIST BEFORE CONTINUE]
UserStreamLayer / ExchangeAdapter REST
  -> StateReconciliationLayer: exchange.algo_update_or_open_algo_order_received
StateReconciliationLayer
  -> StateReconciliationLayer: validate protective stop matches position
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_CONFIRMED
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = POSITION_PROTECTED
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ObservabilityLayer: protection.confirmed
```

## Required protective stop fields

At minimum:

```text
symbol
side opposite current position
order_role = PROTECTIVE_STOP
client_algo_id
stop_trigger_price
workingType = MARK_PRICE
closePosition = true
priceProtect = TRUE
trade_reference
correlation_id
config_version
```

## Valid protective stop match

A protective stop is valid only if:

- it belongs to the current strategy trade lineage,
- it is on the expected symbol,
- its side closes the current position,
- its trigger price matches the risk-approved stop after allowed tick adjustment,
- it uses required v1 settings,
- it is active/open according to exchange state,
- and there are no conflicting protective stops.

## Failure / uncertainty branches

### Stop submission rejected

```text
ExchangeAdapter
  -> ExecutionLayer: execution.protective_stop_rejected
ExecutionLayer
  -> RuntimeState: protection_state = PROTECTION_UNCERTAIN or UNPROTECTED
ExecutionLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> SafetyIncidentLayer: incident.open_stop_submission_failure
[EMERGENCY if position exists]
```

### Stop confirmation timeout

```text
ExecutionLayer
  -> RuntimeState: protection_state = STOP_SUBMITTED_UNCONFIRMED
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> StateReconciliationLayer: verify open algo orders
[RECONCILE]
```

If reconciliation confirms valid stop:

```text
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_CONFIRMED
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = POSITION_PROTECTED
[PERSIST BEFORE CONTINUE]
```

If no stop exists:

```text
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_unprotected_position
[EMERGENCY]
```

### Multiple stops detected

```text
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_UNCERTAIN
StateReconciliationLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_conflicting_protective_stops
[ESCALATE]
```

## Required outcome

Protection flow ends in exactly one of:

```text
POSITION_PROTECTED
PROTECTION_CONFIRMED_BY_RECONCILIATION
UNPROTECTED_POSITION_EMERGENCY
PROTECTION_UNCERTAIN_OPERATOR_REVIEW_REQUIRED
```

---

## Flow 5 — Full Signal-to-Protected-Position Flow

## Purpose

This is the full golden path from completed 15m bar to protected live position.

It combines Flows 1 through 4.

## Golden path sequence

```text
MarketDataLayer
  -> StrategyEngine: market.completed_bar_available
StrategyEngine
  -> StrategyEngine: evaluate completed-bar breakout setup
StrategyEngine
  -> RuntimeState: trade_lifecycle_state = SIGNAL_CONFIRMED
[PERSIST BEFORE CONTINUE]
StrategyEngine
  -> RiskLayer: risk.evaluate_entry_candidate
RiskLayer
  -> RiskLayer: validate stop, sizing, exposure, daily/drawdown gates
RiskLayer
  -> ExecutionLayer: execution.submit_entry_order
ExecutionLayer
  -> RuntimeState: trade_lifecycle_state = ENTRY_SUBMITTED
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: submit MARKET entry
ExchangeAdapter
  -> ExecutionLayer: execution.entry_submission_acknowledged
ExecutionLayer
  -> RuntimeState: trade_lifecycle_state = ENTRY_ACKNOWLEDGED
[PERSIST BEFORE CONTINUE]
UserStreamLayer
  -> StateReconciliationLayer: exchange.entry_fill_confirmed
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = ENTRY_FILL_CONFIRMED
[PERSIST BEFORE CONTINUE]
UserStreamLayer / REST
  -> StateReconciliationLayer: exchange.position_confirmed
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = POSITION_CONFIRMED
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ExecutionLayer: execution.submit_protective_stop
ExecutionLayer
  -> RuntimeState: protection_state = STOP_SUBMITTED_UNCONFIRMED
[PERSIST BEFORE CONTINUE]
UserStreamLayer / REST
  -> StateReconciliationLayer: exchange.protective_stop_confirmed
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_CONFIRMED
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = POSITION_PROTECTED
[PERSIST BEFORE CONTINUE]
RuntimeState
  -> ObservabilityLayer: trade.position_protected
```

## Forbidden shortcuts

The implementation must not skip from:

```text
ENTRY_SUBMITTED -> POSITION_PROTECTED
```

or:

```text
ENTRY_ACKNOWLEDGED -> POSITION_PROTECTED
```

or:

```text
PROTECTIVE_STOP_SUBMITTED -> POSITION_PROTECTED
```

without exchange-derived confirmation or reconciliation evidence.

## Required final steady state

For a live trade to be considered in acceptable steady operation:

```text
runtime_mode = RUNNING_HEALTHY or managed-position mode permitted by state model
trade_lifecycle_state = POSITION_PROTECTED or later protected risk-stage state
protection_state = PROTECTION_CONFIRMED
entries_blocked = true for new entries because one position exists
position_ownership = STRATEGY_OWNED
user_stream_health acceptable
market_data_health acceptable for management
reconciliation_state acceptable
```

One open protected position still means no new entries in v1.

---

# Trade Management Flows

## Flow 6 — Strategy-Managed Stop Replacement

## Purpose

This flow handles strategy-managed stop updates such as risk reduction, break-even transition, or trailing-stop movement.

V1 uses cancel-and-replace, not in-place modification.

## Preconditions

- Strategy-owned position exists.
- Current protective stop is confirmed.
- Proposed new stop is risk-reducing or equal-risk according to v1 policy.
- Stop widening is not allowed.
- No stop replacement is already in progress.
- User stream and REST recovery paths are available enough to verify replacement.

## Normal sequence

```text
MarketDataLayer
  -> StrategyEngine: market.completed_bar_available
StrategyEngine
  -> StrategyEngine: evaluate trade-management stage
StrategyEngine
  -> RiskLayer: risk.validate_stop_update_candidate
RiskLayer
  -> RiskLayer: confirm stop update does not increase risk
RiskLayer
  -> ExecutionLayer: execution.replace_protective_stop
ExecutionLayer
  -> RuntimeState: protection_state = STOP_REPLACEMENT_STARTED
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: cancel current protective stop
ExchangeAdapter
  -> ExecutionLayer: execution.protective_stop_cancel_submitted
UserStreamLayer / REST
  -> StateReconciliationLayer: exchange.old_stop_cancel_confirmed
StateReconciliationLayer
  -> RuntimeState: protection_state = OLD_STOP_CANCEL_CONFIRMED
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: submit replacement protective stop
ExchangeAdapter
  -> ExecutionLayer: execution.replacement_stop_submitted
ExecutionLayer
  -> RuntimeState: protection_state = REPLACEMENT_STOP_SUBMITTED_UNCONFIRMED
[PERSIST BEFORE CONTINUE]
UserStreamLayer / REST
  -> StateReconciliationLayer: exchange.replacement_stop_confirmed
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_CONFIRMED
StateReconciliationLayer
  -> RuntimeState: update risk_stage / stop_stage
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ObservabilityLayer: protection.stop_replacement_confirmed
```

## Failure / uncertainty branches

### Cancel request unknown

```text
ExchangeAdapter
  -> ExecutionLayer: execution.stop_cancel_unknown
ExecutionLayer
  -> RuntimeState: protection_state = PROTECTION_UNCERTAIN
ExecutionLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> StateReconciliationLayer: reconciliation.required
[RECONCILE]
```

Do not submit another stop until the old stop state is known, unless emergency policy specifically chooses a controlled repair action.

### Old stop canceled, new stop submission failed

```text
ExchangeAdapter
  -> ExecutionLayer: execution.replacement_stop_failed
ExecutionLayer
  -> RuntimeState: protection_state = UNPROTECTED_OR_PROTECTION_UNCERTAIN
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> SafetyIncidentLayer: incident.open_stop_replacement_failure
[EMERGENCY]
```

Allowed paths:

1. deterministic restore-protection attempt if state is clear,
2. emergency flatten if protection cannot be restored safely,
3. blocked awaiting operator if automated choice is unsafe.

### Both old and new stops active

```text
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_UNCERTAIN
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_conflicting_stops
[ESCALATE]
```

The system must not treat duplicate stop state as healthy.

### Proposed stop widens risk

```text
RiskLayer
  -> StrategyEngine: stop_update_rejected_would_increase_risk
RiskLayer
  -> ObservabilityLayer: risk.stop_update_rejected
```

No exchange action should occur.

## Required outcome

Stop replacement ends in exactly one of:

```text
STOP_REPLACEMENT_CONFIRMED
STOP_UPDATE_REJECTED_NO_EXCHANGE_ACTION
PROTECTION_UNCERTAIN_RECONCILIATION_REQUIRED
UNPROTECTED_POSITION_EMERGENCY
CONFLICTING_STOPS_OPERATOR_REVIEW_REQUIRED
```

---

## Flow 7 — Normal Strategy Exit

## Purpose

This flow handles normal strategy exits that are not protective-stop triggers or emergency flattening.

## Preconditions

- Strategy-owned position exists.
- Position ownership is known.
- Protective stop status is known or emergency policy explicitly allows exit during uncertainty.
- Exit intent is generated by approved strategy/risk logic.
- No other exit/flatten order is already in flight.

## Normal sequence

```text
StrategyEngine
  -> RiskLayer: risk.validate_exit_candidate
RiskLayer
  -> ExecutionLayer: execution.submit_market_exit
ExecutionLayer
  -> RuntimeState: trade_lifecycle_state = EXIT_PENDING
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: submit normal MARKET exit order
ExchangeAdapter
  -> ExecutionLayer: execution.exit_order_acknowledged
UserStreamLayer
  -> StateReconciliationLayer: exchange.exit_fill_confirmed
StateReconciliationLayer
  -> ExchangeAdapter: query position state if needed
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = EXIT_CONFIRMED
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> StateReconciliationLayer: verify position is flat
StateReconciliationLayer
  -> StateReconciliationLayer: check open algo orders
```

If protective stop remains open after flat:

```text
StateReconciliationLayer
  -> ExecutionLayer: execution.cancel_stale_protective_stop
ExecutionLayer
  -> RuntimeState: cleanup_state = STALE_STOP_CLEANUP_PENDING
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: cancel stale protective stop
UserStreamLayer / REST
  -> StateReconciliationLayer: exchange.stale_stop_cancel_confirmed
StateReconciliationLayer
  -> RuntimeState: operational_position_state = PROMETHEUS_CLEAN_FLAT
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ObservabilityLayer: trade.closed_clean_flat
```

If no stale stop remains:

```text
StateReconciliationLayer
  -> RuntimeState: operational_position_state = PROMETHEUS_CLEAN_FLAT
[PERSIST BEFORE CONTINUE]
```

## Failure / uncertainty branches

### Exit submission unknown

```text
ExchangeAdapter
  -> ExecutionLayer: execution.exit_submission_unknown
ExecutionLayer
  -> RuntimeState: runtime_mode = RECOVERING
ExecutionLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> StateReconciliationLayer: reconciliation.required
[RECONCILE]
```

No duplicate exit order may be blindly submitted.

### Exit partially filled

```text
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = EXIT_PENDING_PARTIAL
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> StateReconciliationLayer: confirm remaining position size
StateReconciliationLayer
  -> SafetyIncidentLayer: classify partial exit handling requirement
```

### Flat confirmed but stale protective stop cancel unknown

```text
ExecutionLayer
  -> RuntimeState: operational_position_state = FLAT_WITH_STALE_ORDER_UNCERTAINTY
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> StateReconciliationLayer: reconciliation.required
```

New entries remain blocked until clean flat is confirmed.

## Required clean flat conditions

A normal exit may end in clean flat only when:

```text
exchange position amount = 0
no open normal entry/exit orders remain
no open protective stop remains
no unknown order outcome remains
no unresolved mismatch remains
no manual/non-bot exposure exists
```

---

## Flow 8 — Protective Stop Triggered

## Purpose

This flow handles the exchange-side protective stop triggering and closing or reducing the position.

## Preconditions

- Strategy-owned position exists.
- Protective stop exists and is confirmed.
- User stream or reconciliation detects algo trigger/order update/account update.

## Normal sequence

```text
UserStreamLayer
  -> StateReconciliationLayer: exchange.algo_update_stop_triggered
UserStreamLayer
  -> StateReconciliationLayer: exchange.order_trade_update_stop_execution
UserStreamLayer
  -> StateReconciliationLayer: exchange.account_update_position_change
StateReconciliationLayer
  -> StateReconciliationLayer: confirm position reduced or flat
```

If position flat:

```text
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = STOP_EXIT_CONFIRMED
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_CONSUMED_OR_CLOSED
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> RiskLayer: risk.update_daily_loss_and_drawdown
RiskLayer
  -> RuntimeState: update daily/drawdown state if thresholds crossed
[PERSIST BEFORE CONTINUE if thresholds changed]
StateReconciliationLayer
  -> ObservabilityLayer: trade.stopped_out_recorded
```

If position reduced but not flat:

```text
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = POSITION_SIZE_CHANGED_UNEXPECTEDLY
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_UNCERTAIN
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_position_size_mismatch
[ESCALATE]
```

## Failure / uncertainty branches

### Stop trigger event but position not flat and no valid protection remains

```text
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_unprotected_residual_position
[EMERGENCY]
```

### Conflicting event sequence

Example:

```text
ALGO_UPDATE says triggered
ACCOUNT_UPDATE delayed or missing
position REST query inconclusive
```

Required behavior:

```text
StateReconciliationLayer
  -> RuntimeState: runtime_mode = RECOVERING
StateReconciliationLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ExchangeAdapter: query position, open orders, open algo orders
[RECONCILE]
```

## Required outcome

Protective stop trigger flow ends in one of:

```text
POSITION_FLAT_STOP_EXIT_CONFIRMED
RESIDUAL_POSITION_PROTECTION_REQUIRED
UNKNOWN_STOP_OUTCOME_RECONCILIATION_REQUIRED
UNSAFE_MISMATCH_OPERATOR_REVIEW_REQUIRED
```

---

# Restart, Recovery, and Failure Flows

## Flow 9 — Restart Reconciliation

## Purpose

This flow ensures the bot never restarts directly into normal trading.

## Triggers

- process start,
- clean planned restart,
- unclean crash restart,
- host reboot,
- controlled redeploy,
- stale-state recovery restart,
- operator-requested restart.

## Normal sequence

```text
Process
  -> RuntimeState: runtime_mode = SAFE_MODE
Process
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
Process
  -> ObservabilityLayer: restart.started
Process
  -> PersistenceLayer: load runtime control record
Process
  -> PersistenceLayer: load active trade/protection/reconciliation records
Process
  -> RuntimeState: local state loaded as provisional
Process
  -> ExchangeAdapter: verify credentials/config/connectivity prerequisites
Process
  -> UserStreamLayer: restore or recreate user stream
UserStreamLayer
  -> RuntimeState: user_stream_health = RESTORING
Process
  -> ExchangeAdapter: query BTCUSDT position state
Process
  -> ExchangeAdapter: query BTCUSDT open normal orders
Process
  -> ExchangeAdapter: query BTCUSDT open algo orders
Process
  -> StateReconciliationLayer: reconcile local state vs exchange state
StateReconciliationLayer
  -> RuntimeState: reconciliation_state = RECONCILIATION_IN_PROGRESS
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> StateReconciliationLayer: classify outcome CLEAN / RECOVERABLE_MISMATCH / UNSAFE_MISMATCH
```

### Clean outcome

```text
StateReconciliationLayer
  -> RuntimeState: reconciliation_state = CLEAN
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> RuntimeState: runtime_mode = RUNNING_HEALTHY if all other gates permit
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ObservabilityLayer: restart.completed_clean
```

### Recoverable mismatch outcome

```text
StateReconciliationLayer
  -> RuntimeState: reconciliation_state = RECOVERABLE_MISMATCH
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ExecutionLayer: perform approved deterministic repair
ExecutionLayer
  -> ExchangeAdapter: repair action
UserStreamLayer / REST
  -> StateReconciliationLayer: repair confirmation
StateReconciliationLayer
  -> RuntimeState: reconciliation_state = CLEAN_AFTER_REPAIR
[PERSIST BEFORE CONTINUE]
```

Only after repair is confirmed may safe-mode exit be considered.

### Unsafe mismatch outcome

```text
StateReconciliationLayer
  -> RuntimeState: reconciliation_state = UNSAFE_MISMATCH
StateReconciliationLayer
  -> RuntimeState: runtime_mode = BLOCKED_AWAITING_OPERATOR
StateReconciliationLayer
  -> RuntimeState: operator_review_required = true
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_reconciliation_unsafe_mismatch
[ESCALATE]
```

## Required checks before safe-mode exit

Safe-mode exit requires:

```text
reconciliation acceptable
no unresolved unknown execution outcome
no unresolved manual/non-bot exposure
no stale critical stream state
if position exists, ownership known
if position exists, protection confirmed
kill switch not active
operator pause not active
operator review not required
blocking incident not active
configuration and credentials valid
```

## Forbidden behavior

The bot must never:

- start directly in `RUNNING_HEALTHY`,
- submit a new entry before startup reconciliation,
- treat persisted local state as exchange truth,
- ignore stale protective stops while flat,
- ignore unprotected positions found at startup,
- clear kill switch automatically on restart.

---

## Flow 10 — User-Stream Gap While Flat

## Purpose

This flow handles private user-stream degradation when the bot is flat and no order outcome is in flight.

## Preconditions

- No exchange position exists according to last trusted state.
- No entry/exit/stop order is in flight.
- No unknown execution outcome exists.

## Sequence

```text
UserStreamLayer
  -> UserStreamLayer: detect disconnect / listen-key issue / stale event cadence
UserStreamLayer
  -> RuntimeState: user_stream_health = STALE or UNAVAILABLE
UserStreamLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
UserStreamLayer
  -> ObservabilityLayer: user_stream.marked_stale
UserStreamLayer
  -> UserStreamLayer: reconnect or recreate listen key
UserStreamLayer
  -> RuntimeState: user_stream_health = RESTORING
UserStreamLayer
  -> StateReconciliationLayer: reconciliation.required_after_stream_gap
StateReconciliationLayer
  -> ExchangeAdapter: query position state
StateReconciliationLayer
  -> ExchangeAdapter: query open normal orders
StateReconciliationLayer
  -> ExchangeAdapter: query open algo orders
StateReconciliationLayer
  -> StateReconciliationLayer: classify clean/recoverable/unsafe
```

If clean:

```text
StateReconciliationLayer
  -> RuntimeState: user_stream_health = HEALTHY
StateReconciliationLayer
  -> RuntimeState: entries_blocked = false only if all other gates permit
[PERSIST BEFORE CONTINUE]
```

If mismatch:

```text
StateReconciliationLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
[ESCALATE if unsafe]
```

## Required outcome

A flat user-stream gap ends in one of:

```text
STREAM_RESTORED_CLEAN
STREAM_RESTORED_RECOVERABLE_REPAIR_REQUIRED
STREAM_GAP_UNSAFE_OPERATOR_REVIEW_REQUIRED
```

---

## Flow 11 — User-Stream Gap While Exposed

## Purpose

This flow handles private stream staleness while a position exists or while order/protection state matters.

This is more severe than a stream gap while flat.

## Triggers

- user stream disconnected while position exists,
- keepalive fails while position exists,
- listen key expires while position exists,
- expected fill/position/stop event does not arrive,
- event sequence appears inconsistent,
- private stream health cannot be trusted during exposure.

## Sequence

```text
UserStreamLayer
  -> RuntimeState: user_stream_health = STALE or UNAVAILABLE
UserStreamLayer
  -> RuntimeState: runtime_mode = SAFE_MODE or RECOVERING
UserStreamLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
UserStreamLayer
  -> SafetyIncidentLayer: incident.open_user_stream_stale_while_exposed
UserStreamLayer
  -> StateReconciliationLayer: reconciliation.required
StateReconciliationLayer
  -> ExchangeAdapter: query current position state
StateReconciliationLayer
  -> ExchangeAdapter: query open normal orders
StateReconciliationLayer
  -> ExchangeAdapter: query open algo orders
StateReconciliationLayer
  -> StateReconciliationLayer: classify position/protection state
```

If position exists and valid stop exists:

```text
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_CONFIRMED_BY_REST
StateReconciliationLayer
  -> RuntimeState: runtime_mode = RECOVERING until stream restored
[PERSIST BEFORE CONTINUE]
UserStreamLayer
  -> UserStreamLayer: restore private stream
StateReconciliationLayer
  -> RuntimeState: runtime_mode = RUNNING_HEALTHY or managed blocked state if all gates pass
[PERSIST BEFORE CONTINUE]
```

If position exists and stop is missing or uncertain:

```text
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_unprotected_or_uncertain_position
[EMERGENCY]
```

If exchange state cannot be queried:

```text
StateReconciliationLayer
  -> RuntimeState: runtime_mode = BLOCKED_AWAITING_OPERATOR or RECOVERING
StateReconciliationLayer
  -> RuntimeState: operator_review_required = true
[PERSIST BEFORE CONTINUE]
[ESCALATE]
```

## Required outcome

A user-stream gap while exposed ends in one of:

```text
EXPOSURE_CONFIRMED_PROTECTED_STREAM_RESTORED
EXPOSURE_CONFIRMED_PROTECTED_STREAM_STILL_DEGRADED_ENTRIES_BLOCKED
UNPROTECTED_POSITION_EMERGENCY
UNKNOWN_EXPOSURE_OPERATOR_REVIEW_REQUIRED
```

---

## Flow 12 — Emergency Unprotected Position

## Purpose

This flow handles one of the most dangerous v1 states:

```text
position exists + protective stop not confirmed
```

## Triggers

- position confirmed after entry but stop submission failed,
- stop rejected,
- stop confirmation timeout and reconciliation finds no valid stop,
- stop replacement canceled old stop and new stop failed,
- restart finds position without valid protective stop,
- user-stream gap/reconciliation cannot confirm stop while position exists,
- multiple/conflicting stops make protection uncertain.

## Sequence

```text
StateReconciliationLayer
  -> RuntimeState: protection_state = UNPROTECTED or PROTECTION_UNCERTAIN
StateReconciliationLayer
  -> RuntimeState: runtime_mode = SAFE_MODE or BLOCKED_AWAITING_OPERATOR
StateReconciliationLayer
  -> RuntimeState: entries_blocked = true
StateReconciliationLayer
  -> RuntimeState: operator_review_required = true where required
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_severity_4_unprotected_position
SafetyIncidentLayer
  -> ObservabilityLayer: alert.critical_unprotected_position
```

## Deterministic restore-protection branch

Allowed only if all are true:

```text
position side known
position ownership known or safely recoverable strategy-owned
position size/side not ambiguous
risk-approved stop known
stop price still valid and risk-approved
no conflicting active stop exists
exchange connectivity available
adapter can submit required STOP_MARKET
```

Sequence:

```text
SafetyIncidentLayer
  -> ExecutionLayer: execution.restore_protective_stop_once
ExecutionLayer
  -> RuntimeState: protection_state = RESTORE_PROTECTION_ATTEMPTED
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: submit protective STOP_MARKET
UserStreamLayer / REST
  -> StateReconciliationLayer: exchange.protective_stop_confirmed
StateReconciliationLayer
  -> RuntimeState: protection_state = PROTECTION_CONFIRMED
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.contained_pending_review
```

Even after restore succeeds, operator review may still be required depending on incident severity.

## Emergency flatten branch

If deterministic restore is not safe or fails:

```text
SafetyIncidentLayer
  -> ExecutionLayer: execution.submit_emergency_flatten
ExecutionLayer
  -> RuntimeState: trade_lifecycle_state = EMERGENCY_FLATTEN_PENDING
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: submit MARKET flatten order
UserStreamLayer / REST
  -> StateReconciliationLayer: exchange.position_flat_confirmed
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = EMERGENCY_FLATTEN_CONFIRMED
StateReconciliationLayer
  -> RuntimeState: runtime_mode = BLOCKED_AWAITING_OPERATOR
[PERSIST BEFORE CONTINUE]
```

## If emergency flatten outcome is unknown

```text
ExecutionLayer
  -> RuntimeState: runtime_mode = BLOCKED_AWAITING_OPERATOR or RECOVERING
ExecutionLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> StateReconciliationLayer: reconciliation.required
[ESCALATE]
```

No blind flatten retry is allowed if the first flatten request may have reached the exchange.

## Required outcome

Emergency unprotected position flow ends in one of:

```text
PROTECTION_RESTORED_INCIDENT_CONTAINED
POSITION_FLATTENED_INCIDENT_CONTAINED
UNKNOWN_FLATTEN_OUTCOME_RECONCILIATION_REQUIRED
BLOCKED_AWAITING_OPERATOR
```

---

## Flow 13 — Unknown Execution Outcome

## Purpose

This flow handles any exposure-changing request whose final outcome is unknown.

## Examples

- REST timeout after entry submit,
- REST timeout after exit submit,
- REST timeout after emergency flatten submit,
- stop submission unknown,
- stop cancel unknown,
- stop replacement unknown,
- exchange returns ambiguous response,
- adapter cannot classify request outcome.

## Sequence

```text
ExchangeAdapter
  -> ExecutionLayer: execution.outcome_unknown
ExecutionLayer
  -> RuntimeState: entries_blocked = true
ExecutionLayer
  -> RuntimeState: runtime_mode = SAFE_MODE or RECOVERING
ExecutionLayer
  -> RuntimeState: execution_uncertainty_active = true
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ObservabilityLayer: execution.unknown_outcome_detected
ExecutionLayer
  -> StateReconciliationLayer: reconciliation.required
StateReconciliationLayer
  -> ExchangeAdapter: query relevant order by client ID / order ID where available
StateReconciliationLayer
  -> ExchangeAdapter: query open normal orders
StateReconciliationLayer
  -> ExchangeAdapter: query open algo orders if protection-related
StateReconciliationLayer
  -> ExchangeAdapter: query position state
StateReconciliationLayer
  -> StateReconciliationLayer: classify outcome
```

## Classification outcomes

### No exposure and no order exists

```text
StateReconciliationLayer
  -> RuntimeState: execution_uncertainty_active = false
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = FLAT if applicable
[PERSIST BEFORE CONTINUE]
```

### Order filled and position exists

```text
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = POSITION_CONFIRMED
[PERSIST BEFORE CONTINUE]
StateReconciliationLayer
  -> ExecutionLayer: execution.submit_protective_stop if protection missing
```

### Position exists and protection uncertain

```text
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_unprotected_or_uncertain_position
[EMERGENCY]
```

### Cannot classify

```text
StateReconciliationLayer
  -> RuntimeState: runtime_mode = BLOCKED_AWAITING_OPERATOR
StateReconciliationLayer
  -> RuntimeState: operator_review_required = true
[PERSIST BEFORE CONTINUE]
[ESCALATE]
```

## Forbidden behavior

The runtime must not:

- blindly retry exposure-changing commands,
- assume timeout means failure,
- assume timeout means success,
- submit a second market entry before reconciliation,
- submit another flatten before knowing the first flatten outcome,
- cancel/replace stops repeatedly without knowing current stop state.

---

## Flow 14 — Rate-Limit / IP-Ban Recovery Impairment

## Purpose

This flow handles REST rate-limit or IP-ban risk, especially during recovery.

Rate-limit stress can become a safety issue if it prevents the bot from verifying position or protection state.

## Triggers

- HTTP 429-like throttling responses,
- IP-ban or ban-warning responses,
- adapter rate-limit budget near exhaustion,
- repeated request failures caused by pacing,
- exchange refusing recovery reads due to rate pressure.

## Sequence

```text
ExchangeAdapter
  -> ExecutionLayer / StateReconciliationLayer: exchange.rate_limit_warning
ExchangeAdapter
  -> RuntimeState: exchange_connectivity_state = DEGRADED
ExchangeAdapter
  -> RuntimeState: entries_blocked = true if live safety may be affected
[PERSIST BEFORE CONTINUE if entries_blocked changes]
ExchangeAdapter
  -> ObservabilityLayer: exchange.rate_limit_warning_recorded
```

## Recovery priority order

When request budget is constrained, prioritize:

1. position state reads,
2. active protective stop / open algo order reads,
3. open normal order reads relevant to unknown exposure,
4. cancel or repair actions only after required reads,
5. non-critical metadata refresh,
6. dashboard convenience reads,
7. historical or analytics reads.

## If flat and no order uncertainty exists

```text
RuntimeState
  -> RuntimeState: entries_blocked = true until rate-limit condition clears
[PERSIST BEFORE CONTINUE]
```

No emergency is required solely because flat-state noncritical reads are rate-limited.

## If exposed and recovery reads are impaired

```text
StateReconciliationLayer
  -> SafetyIncidentLayer: incident.open_rate_limit_recovery_impaired
SafetyIncidentLayer
  -> RuntimeState: runtime_mode = SAFE_MODE or BLOCKED_AWAITING_OPERATOR
SafetyIncidentLayer
  -> RuntimeState: operator_review_required = true
[PERSIST BEFORE CONTINUE]
[ESCALATE]
```

## Forbidden behavior

The runtime must not:

- spam REST during uncertainty,
- retry every failed request aggressively,
- exhaust request budget on non-critical dashboard updates,
- continue live entries while recovery capacity is impaired,
- ignore IP-ban risk because no order failed yet.

---

# Risk Control Flows

## Flow 15 — Daily Loss Lockout

## Purpose

This flow updates daily loss state after trade closure or realized PnL change and blocks new entries if daily loss limits are reached.

## Triggers

- normal exit confirmed,
- protective stop exit confirmed,
- emergency flatten confirmed,
- realized PnL update received,
- funding/fee event relevant to daily realized PnL,
- daily UTC boundary reset.

## Normal sequence after realized update

```text
StateReconciliationLayer
  -> RiskLayer: risk.update_daily_loss_state
RiskLayer
  -> RiskLayer: calculate daily realized PnL fraction
RiskLayer
  -> RiskLayer: calculate full-risk losses today
RiskLayer
  -> RiskLayer: classify daily state
```

If warning threshold crossed:

```text
RiskLayer
  -> ObservabilityLayer: alert.daily_loss_warning
```

If daily entry lockout threshold crossed:

```text
RiskLayer
  -> RuntimeState: entries_blocked = true
RiskLayer
  -> RuntimeState: daily_loss_lockout_active = true
[PERSIST BEFORE CONTINUE]
RiskLayer
  -> ObservabilityLayer: alert.daily_entry_lockout
```

If hard review threshold crossed:

```text
RiskLayer
  -> SafetyIncidentLayer: review.daily_hard_review_required
SafetyIncidentLayer
  -> RuntimeState: operator_review_required = true
SafetyIncidentLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
```

## Existing protected position behavior

If daily lockout activates while a protected position is already open:

```text
daily lockout blocks new entries
existing protected position may continue safety management
profit-optimizing behavior should remain within approved strategy rules
emergency/protection actions remain allowed
```

## UTC daily reset behavior

At UTC day boundary:

```text
RiskLayer
  -> RiskLayer: reset daily counters if no unresolved dependency blocks reset
RiskLayer
  -> RuntimeState: daily_loss_lockout_active = false only for daily-lockout reason
[PERSIST BEFORE CONTINUE]
```

Daily reset must not clear:

- active kill switch,
- unresolved incident,
- operator review requirement,
- drawdown pause,
- reconciliation requirement,
- unprotected position state,
- unknown execution outcome.

---

## Flow 16 — Drawdown Pause / Hard Review

## Purpose

This flow updates longer-term drawdown state and blocks risk increases or entries when drawdown controls require it.

## Triggers

- trade closed,
- realized PnL update,
- mark-to-market drawdown update if configured,
- daily/weekly review update,
- deployment-stage equity high watermark update,
- operator-approved capital allocation change.

## Normal sequence

```text
RiskLayer
  -> RiskLayer: update strategy equity
RiskLayer
  -> RiskLayer: update high watermark if applicable
RiskLayer
  -> RiskLayer: calculate drawdown fraction
RiskLayer
  -> RiskLayer: classify drawdown state
```

If drawdown watch:

```text
RiskLayer
  -> ObservabilityLayer: alert.drawdown_watch
```

If drawdown caution:

```text
RiskLayer
  -> RuntimeState: risk_increase_blocked = true
[PERSIST BEFORE CONTINUE]
RiskLayer
  -> ObservabilityLayer: alert.drawdown_caution
```

If drawdown pause:

```text
RiskLayer
  -> RuntimeState: entries_blocked = true
RiskLayer
  -> RuntimeState: drawdown_pause_active = true
RiskLayer
  -> RuntimeState: operator_review_required = true
[PERSIST BEFORE CONTINUE]
RiskLayer
  -> ObservabilityLayer: alert.drawdown_pause
```

If hard review:

```text
RiskLayer
  -> RuntimeState: entries_blocked = true
RiskLayer
  -> RuntimeState: operator_review_required = true
RiskLayer
  -> SafetyIncidentLayer: review.drawdown_hard_review_required
[PERSIST BEFORE CONTINUE]
```

## Abnormal drawdown branch

If drawdown is tied to:

- unprotected exposure,
- unknown execution outcome,
- duplicate entry,
- manual/non-bot exposure,
- stop failure,
- reconciliation failure,
- suspected credential issue,

then incident/kill-switch policy may override normal drawdown handling.

```text
RiskLayer
  -> SafetyIncidentLayer: incident.open_abnormal_drawdown
[ESCALATE]
```

---

## Flow 17 — Kill-Switch Activation

## Purpose

This flow activates a hard trust-boundary halt.

## Triggers

- operator activates kill switch,
- position exists without confirmed protection,
- repeated unsafe reconciliation mismatches,
- repeated unknown execution outcomes,
- suspected credential compromise,
- critical stream failure while exposed,
- emergency flatten path triggered,
- severe incident requires hard halt.

## Operator activation sequence

```text
OperatorControlSurface
  -> SafetyIncidentLayer: control.activate_kill_switch
SafetyIncidentLayer
  -> RuntimeState: kill_switch_active = true
SafetyIncidentLayer
  -> RuntimeState: entries_blocked = true
SafetyIncidentLayer
  -> RuntimeState: operator_review_required = true
SafetyIncidentLayer
  -> RuntimeState: runtime_mode = SAFE_MODE or BLOCKED_AWAITING_OPERATOR
[PERSIST BEFORE CONTINUE]
SafetyIncidentLayer
  -> ObservabilityLayer: control.kill_switch_activated
```

## Automatic activation sequence

```text
SafetyIncidentLayer
  -> RuntimeState: kill_switch_active = true
SafetyIncidentLayer
  -> RuntimeState: entries_blocked = true
SafetyIncidentLayer
  -> RuntimeState: operator_review_required = true
[PERSIST BEFORE CONTINUE]
SafetyIncidentLayer
  -> ObservabilityLayer: control.kill_switch_auto_activated
```

## Allowed actions while active

Kill switch blocks:

- new entries,
- normal strategy progression toward new exposure,
- automatic return to `RUNNING_HEALTHY`,
- risk increase,
- leverage increase,
- stop widening,
- parameter changes intended to bypass halt.

Kill switch may still allow controlled safety actions:

- exchange state reads,
- reconciliation,
- stream restoration,
- stale order cancellation,
- protective stop restoration,
- risk-reducing stop repair,
- emergency flattening,
- incident logging,
- operator review workflows.

## Existing protected position behavior

If a protected position exists when kill switch activates:

```text
RuntimeState
  -> RuntimeState: normal strategy progression blocked
RuntimeState
  -> RuntimeState: entries_blocked = true
SafetyIncidentLayer
  -> StateReconciliationLayer: verify position/protection state
```

The bot may preserve or reduce risk. It must not continue profit-optimizing behavior as if healthy unless explicitly allowed by policy as safety-preserving.

---

## Flow 18 — Kill-Switch Clearance

## Purpose

This flow clears a kill switch only after explicit operator action and required safety checks.

Kill switch must never auto-clear.

## Preconditions

- Operator requests clearance.
- Required review notes or approvals are recorded where policy requires.
- Exchange state can be queried.
- Reconciliation can run.
- No unresolved emergency condition remains.

## Sequence

```text
OperatorControlSurface
  -> SafetyIncidentLayer: control.request_kill_switch_clearance
SafetyIncidentLayer
  -> PersistenceLayer: record operator action
[PERSIST BEFORE CONTINUE]
SafetyIncidentLayer
  -> StateReconciliationLayer: reconciliation.required_for_kill_switch_clearance
StateReconciliationLayer
  -> ExchangeAdapter: query position state
StateReconciliationLayer
  -> ExchangeAdapter: query open normal orders
StateReconciliationLayer
  -> ExchangeAdapter: query open algo orders
StateReconciliationLayer
  -> StateReconciliationLayer: classify reconciliation state
```

If all checks pass:

```text
SafetyIncidentLayer
  -> RuntimeState: kill_switch_active = false
SafetyIncidentLayer
  -> RuntimeState: operator_review_required = false only if no other reason remains
SafetyIncidentLayer
  -> RuntimeState: entries_blocked = false only if all gates permit
[PERSIST BEFORE CONTINUE]
SafetyIncidentLayer
  -> ObservabilityLayer: control.kill_switch_cleared
```

If checks fail:

```text
SafetyIncidentLayer
  -> RuntimeState: kill_switch_active = true
SafetyIncidentLayer
  -> RuntimeState: operator_review_required = true
SafetyIncidentLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
SafetyIncidentLayer
  -> ObservabilityLayer: control.kill_switch_clearance_denied
```

## Clearance checks

At minimum:

```text
no unprotected position
no unknown execution outcome
no unsafe reconciliation mismatch
no unresolved severe incident
no credential/security concern unresolved
no manual/non-bot exposure unless explicitly handled
user stream restored or acceptable for selected mode
market data restored or acceptable for selected mode
runtime persistence healthy
operator approval recorded
```

## Forbidden behavior

The implementation must not:

- auto-clear kill switch after timeout,
- clear kill switch solely because the process restarted,
- clear kill switch without reconciliation,
- clear kill switch while position/protection state is unknown,
- clear kill switch by changing configuration alone.

---

# Operator and Manual Control Flows

## Flow 19 — Operator Pause Activation and Clearance

## Purpose

This flow handles normal operator pause, which is weaker than a kill switch but still blocks new entries.

## Activation sequence

```text
OperatorControlSurface
  -> RuntimeState: paused_by_operator = true
OperatorControlSurface
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
OperatorControlSurface
  -> ObservabilityLayer: operator.pause_enabled
```

## Effects

Pause blocks:

- new live entries,
- strategy-generated live exposure,
- automatic risk increase while paused.

Pause does not block:

- exchange state reads,
- reconciliation,
- protective stop maintenance,
- safety exits,
- emergency flattening,
- incident handling.

## Clearance sequence

```text
OperatorControlSurface
  -> RuntimeState: paused_by_operator = false
OperatorControlSurface
  -> RuntimeState: entries_blocked = false only if all other gates permit
[PERSIST BEFORE CONTINUE]
OperatorControlSurface
  -> ObservabilityLayer: operator.pause_cleared
```

If another blocking condition remains, `entries_blocked` must remain true.

---

## Flow 20 — Manual Emergency Flatten Request

## Purpose

This flow handles operator-requested emergency flattening through backend safety controls.

The dashboard is not a discretionary trading terminal. Emergency flatten exists to reduce or remove risk.

## Preconditions

- Operator is authenticated/authorized according to current operational policy.
- Confirmation requirement is satisfied.
- Backend validates that flatten is risk-reducing.
- Current exchange state is queried or recent enough for emergency path.

## Sequence

```text
OperatorControlSurface
  -> SafetyIncidentLayer: operator.request_emergency_flatten
SafetyIncidentLayer
  -> PersistenceLayer: record operator action
[PERSIST BEFORE CONTINUE]
SafetyIncidentLayer
  -> StateReconciliationLayer: verify current exposure if possible
SafetyIncidentLayer
  -> ExecutionLayer: execution.submit_emergency_flatten
ExecutionLayer
  -> RuntimeState: trade_lifecycle_state = EMERGENCY_FLATTEN_PENDING
ExecutionLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> ExchangeAdapter: submit MARKET flatten order
UserStreamLayer / REST
  -> StateReconciliationLayer: exchange.position_flat_confirmed
StateReconciliationLayer
  -> RuntimeState: trade_lifecycle_state = EMERGENCY_FLATTEN_CONFIRMED
StateReconciliationLayer
  -> RuntimeState: runtime_mode = BLOCKED_AWAITING_OPERATOR
[PERSIST BEFORE CONTINUE]
```

## Unknown flatten outcome branch

```text
ExchangeAdapter
  -> ExecutionLayer: execution.emergency_flatten_unknown
ExecutionLayer
  -> RuntimeState: runtime_mode = RECOVERING or BLOCKED_AWAITING_OPERATOR
ExecutionLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
ExecutionLayer
  -> StateReconciliationLayer: reconciliation.required
```

No blind second flatten order may be submitted until state is known.

---

# Data and Stream Recovery Flows

## Flow 21 — Market-Data Gap Recovery

## Purpose

This flow handles missing or stale public market data needed for completed-bar strategy evaluation.

## Sequence

```text
MarketDataLayer
  -> RuntimeState: market_data_health = STALE or DEGRADED
MarketDataLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE if entries_blocked changes]
MarketDataLayer
  -> ObservabilityLayer: market_data.gap_detected
MarketDataLayer
  -> ExchangeAdapter: fetch recent klines by REST
MarketDataLayer
  -> MarketDataLayer: validate bar continuity and completed-bar state
```

If recovered:

```text
MarketDataLayer
  -> RuntimeState: market_data_health = HEALTHY
MarketDataLayer
  -> RuntimeState: entries_blocked = false only if all other gates permit
[PERSIST BEFORE CONTINUE if entries_blocked changes]
MarketDataLayer
  -> ObservabilityLayer: market_data.restored
```

If not recovered:

```text
MarketDataLayer
  -> RuntimeState: entries_blocked = true
[PERSIST BEFORE CONTINUE]
MarketDataLayer
  -> ObservabilityLayer: alert.market_data_unavailable
```

## Position-management note

If an existing position is protected, market-data gaps do not remove the exchange-side stop. However, strategy-managed trailing or exit logic may be blocked if required completed-bar data is unavailable.

---

## Flow 22 — Metadata Refresh Failure

## Purpose

This flow handles stale or missing exchange metadata needed for sizing, validation, or order formatting.

## Sequence

```text
ExchangeAdapter
  -> RiskLayer / ExecutionLayer: metadata.refresh_failed
RiskLayer
  -> RuntimeState: entries_blocked = true if metadata needed for live entry
[PERSIST BEFORE CONTINUE if entries_blocked changes]
RiskLayer
  -> ObservabilityLayer: metadata.refresh_failed_recorded
```

## Effects

New entries must be blocked if metadata needed for:

- symbol status,
- price precision,
- quantity precision,
- step size,
- tick size,
- minimum quantity,
- notional rules,
- leverage bracket,
- supported order/trigger settings,
- isolated/position mode validation,

is missing or stale.

Existing protected positions may continue safety management if required state is still valid and no unsafe condition exists.

---

# Cross-Flow Invariants

The following invariants apply across all flows.

## Invariant 1 — No live entry without clean eligibility

A live entry may be submitted only when all required runtime, risk, exposure, state, stream, and control gates permit it.

## Invariant 2 — One position maximum

If any strategy-owned position exists, no new entry may be opened.

## Invariant 3 — Unknown exposure counts as possible exposure

Unknown order status, unknown fill status, unknown position state, or stale exchange state blocks new entries until resolved.

## Invariant 4 — Manual/non-bot exposure blocks entries

If the bot detects exposure or open orders it cannot classify as strategy-owned, it must block new entries and require review.

## Invariant 5 — Filled entry is not protected trade

The transition from fill to protected trade requires position confirmation and protective stop confirmation.

## Invariant 6 — Submitted stop is not confirmed protection

A protective stop submission response is not enough. Exchange-derived evidence or reconciliation must confirm stop existence.

## Invariant 7 — Position without confirmed protection is emergency

Any live position without confirmed protective stop coverage enters emergency handling unless a deterministic immediate restore path is safely available.

## Invariant 8 — Stop updates cannot increase risk

V1 stop updates may preserve or reduce risk. Stop widening is not allowed.

## Invariant 9 — Cancel-and-replace must model uncertainty

Stop replacement has transitional risk. The runtime must explicitly model cancellation pending, cancel unknown, replacement submitted, replacement confirmed, and protection uncertainty states.

## Invariant 10 — Restart never resumes blindly

Every restart begins in safe mode and requires reconciliation before normal operation.

## Invariant 11 — Kill switch never auto-clears

Kill-switch clearance requires explicit operator action and required safety checks.

## Invariant 12 — Daily reset does not clear safety problems

A new UTC day may reset daily counters, but it must not clear kill switch, incidents, operator review requirement, reconciliation requirement, unprotected exposure, unknown execution status, or drawdown pause.

## Invariant 13 — Exchange state outranks persisted local state

Persisted state supports recovery but does not prove exchange truth.

## Invariant 14 — Observability must not leak secrets

Events, logs, audit records, and dashboard fields must never expose credentials, request signatures, or secrets.

---

# Persistence Expectations

## Required persisted continuity records

The event flows assume the runtime can persist at least:

- runtime control record,
- active trade record,
- protection record,
- reconciliation record,
- incident continuity record,
- operator action record,
- important event log records.

## Persistence must support restart answers

After restart, the system must be able to answer:

- what runtime mode was last known,
- whether kill switch was active,
- whether operator pause was active,
- whether operator review was required,
- whether entries were blocked,
- whether an active trade workflow existed,
- what entry/stop identifiers were known,
- whether protection was believed confirmed,
- whether reconciliation had failed,
- whether emergency branch was active,
- what major operator actions had been taken.

## Persistence is not exchange truth

Persisted local state must always be treated as provisional at startup or after confidence loss.

Exchange state and reconciliation classify operational truth.

---

# Observability Expectations

Each flow should emit structured events sufficient to reconstruct:

- what triggered the flow,
- which component acted,
- what command was issued,
- what exchange-derived facts were observed,
- what runtime state changed,
- what was persisted,
- what failure branch occurred,
- whether operator action was required,
- and whether the flow ended safely.

## Required event families

The flows should use the existing event families:

- system/runtime events,
- market-data events,
- user-stream/account events,
- execution events,
- reconciliation/restart events,
- incident events,
- operator action events,
- review-support events.

## High-priority alerts

The following must be operator-visible:

- unprotected live position,
- protection uncertainty while positioned,
- unknown execution outcome involving possible exposure,
- user stream stale while exposed,
- REST recovery impaired while exposed,
- unsafe reconciliation mismatch,
- emergency flatten requested or ambiguous,
- kill switch active,
- kill switch clearance denied,
- manual/non-bot exposure detected,
- daily lockout,
- drawdown pause/hard review.

## Dashboard state fields implied by flows

The dashboard should be able to show:

```text
runtime_mode
entries_allowed
entries_blocked_reasons
kill_switch_active
paused_by_operator
operator_review_required
incident_active
highest_active_severity
market_data_health
user_stream_health
exchange_connectivity_state
reconciliation_state
last_successful_reconciliation_at
position_present
position_side
position_size
position_ownership
protection_state
protective_stop_present
last_protection_confirmation_at
trade_lifecycle_state
daily_loss_state
drawdown_state
last_important_event
```

---

# Testing Requirements

Implementation must include deterministic tests for the flows below.

## Completed-bar and signal tests

- partial candle does not trigger strategy evaluation,
- completed 15m candle triggers evaluation once,
- current forming 1h candle is not used for bias,
- missing higher-timeframe context blocks signal,
- stale market data blocks live entry.

## Signal-to-risk tests

- missing stop rejects trade,
- invalid stop side rejects trade,
- stop outside ATR distance filter rejects trade,
- quantity below minimum rejects trade,
- notional cap rejects trade,
- leverage cap rejects trade,
- daily lockout rejects trade,
- drawdown pause rejects trade,
- kill switch rejects trade,
- manual exposure rejects trade.

## Entry flow tests

- ACK does not mark position confirmed,
- fill event marks fill confirmed but not protected,
- position confirmation required before stop submission,
- REST timeout after entry enters unknown outcome and reconciliation,
- entry rejection remains flat after verification,
- partial fill creates exposure/protection path.

## Protection flow tests

- stop submission response does not mark protection confirmed,
- `ALGO_UPDATE` or REST open algo query confirms protection,
- stop rejection while positioned enters emergency,
- stop confirmation timeout triggers reconciliation,
- missing stop while positioned triggers severity-4 emergency,
- multiple stops triggers protection uncertainty.

## Stop replacement tests

- valid risk-reducing replacement reaches confirmed protection,
- stop widening is rejected before exchange action,
- cancel unknown triggers reconciliation,
- old stop canceled and new stop failed enters emergency,
- duplicate old/new stops triggers protection uncertainty.

## Exit and stop-trigger tests

- normal exit confirmation requires position flat evidence,
- stale protective stop after flat must be cleaned before clean-flat state,
- exit timeout enters unknown outcome and reconciliation,
- stop trigger updates daily loss and trade closure,
- residual position after stop trigger escalates.

## Restart tests

- restart always enters safe mode,
- local state is loaded as provisional,
- clean flat restart exits safe mode only after reconciliation,
- position with valid stop restores protected-position state,
- position without stop enters emergency,
- unexpected order causes mismatch classification,
- active kill switch survives restart.

## User-stream tests

- flat stream gap blocks entries until reconnection/reconciliation,
- exposed stream gap verifies position and stop by REST,
- exposed stream gap with missing stop enters emergency,
- listen-key failure while exposed opens incident.

## Unknown outcome tests

- entry timeout does not retry blindly,
- stop cancel timeout does not assume canceled,
- emergency flatten timeout does not retry blindly,
- reconciliation can classify no-order/no-position clean outcome,
- unclassifiable outcome blocks awaiting operator.

## Risk-control tests

- daily warning threshold emits alert,
- daily lockout blocks entries,
- UTC daily reset does not clear incident/kill switch,
- drawdown caution blocks risk increase,
- drawdown pause blocks entries,
- abnormal drawdown escalates incident path.

## Kill-switch tests

- operator activation persists and blocks entries,
- automatic activation persists and blocks entries,
- safety actions remain allowed while active,
- kill switch never auto-clears,
- clearance requires reconciliation,
- clearance denied if state remains unsafe.

---

# Non-Goals

This document does not attempt to define:

- final Python class names,
- full database schema,
- exact dashboard layout,
- all Binance endpoint paths and parameters,
- cloud deployment architecture,
- multi-symbol orchestration,
- hedge-mode behavior,
- portfolio-level risk routing,
- discretionary manual trading behavior,
- or machine-learning/autonomous strategy switching.

Those are out of scope for this flow document.

---

# Open Questions

The following should be resolved during implementation design or later docs:

1. Exact enum names for every runtime, trade, protection, reconciliation, and incident state.
2. Exact persistence transaction boundaries for multi-record updates.
3. Exact timeout thresholds for entry confirmation, stop confirmation, stream staleness, and REST recovery.
4. Exact dashboard wording for each blocked state and required operator action.
5. Exact emergency flatten confirmation UX and approval wording.
6. Exact strategy-managed trailing behavior while kill switch is active but position remains protected.
7. Exact policy for paper/shadow mode events that mimic live flows without placing real orders.

None of these open questions should weaken the locked safety principles.

---

# Acceptance Criteria

This document is complete enough for v1 implementation planning when:

- the completed-bar signal flow is explicit,
- signal-to-risk approval is explicit,
- market entry flow does not treat ACK as truth,
- position confirmation is separate from fill confirmation,
- protective stop confirmation is separate from stop submission,
- signal-to-protected-position golden path is clear,
- stop replacement failure branches are explicit,
- normal exit and stale stop cleanup are explicit,
- protective stop trigger handling is explicit,
- restart reconciliation is explicit,
- user-stream gap behavior differs between flat and exposed states,
- emergency unprotected position behavior is explicit,
- unknown execution outcome behavior forbids blind retry,
- rate-limit recovery impairment is explicit,
- daily loss and drawdown control flows are explicit,
- kill-switch activation and clearance flows are explicit,
- durable-write points are marked,
- observability expectations are clear,
- test requirements cover normal, failure, restart, and emergency branches,
- and the document does not duplicate database, deployment, or UI-specific responsibilities.

