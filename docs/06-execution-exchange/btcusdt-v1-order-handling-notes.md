# BTCUSDT V1 Order Handling Notes

## Purpose

This document defines the order-handling design for the v1 BTCUSDT breakout strategy on Binance USDⓈ-M futures.

Its purpose is to translate the strategy and risk rules into exchange-safe operational behavior.

This document focuses on:

- order placement,
- protective stop placement,
- state tracking,
- reconciliation,
- stop updates,
- and failure handling.

## Scope

This document applies to the first live-capable version of the system with the following assumptions:

- Binance USDⓈ-M futures
- BTCUSDT perpetual
- one-way mode
- isolated margin
- one symbol only
- one position only
- supervised deployment
- bar-close market entry
- exchange-side protective stop

This document does **not** define the full implementation code, UI behavior, or multi-symbol orchestration.

## Background

The v1 strategy uses:

- 15m signal logic,
- 1h higher-timeframe bias,
- breakout continuation entries,
- market entry after confirmed bar close,
- structural stop with ATR buffer,
- staged stop reduction,
- and trailing management after trade confirmation.

Because this system trades futures rather than a spot instrument, the execution layer must manage:

- order state,
- fill state,
- position state,
- protective stop state,
- and recovery state

in a way that is robust to disconnects, restart events, and exchange/API edge cases.

Binance’s current USDⓈ-M futures model separates:

- **normal orders**
- and **conditional / algo orders**

so the order-handling design must reflect that distinction explicitly.

## Core Operational Principles

### 1. Strategy and execution must remain separate

The strategy decides **what should happen**.

The execution layer decides **how to safely express that decision on the exchange**.

### 2. Exchange state is authoritative

Local state is necessary for tracking and orchestration, but the exchange remains the ultimate source of truth.

### 3. User-stream events are the primary live state source

For normal live operation:

- user-stream events are the primary source of truth for order, position, and account changes.

REST queries are used for:

- placement,
- cancellation,
- startup reconciliation,
- recovery after disconnects,
- and exception handling.

### 4. Symbol-scoped behavior is preferred

All order and reconciliation logic should be scoped to the active strategy symbol whenever possible.

For v1, that means BTCUSDT-specific order and position queries rather than broad account-wide polling unless a recovery condition explicitly requires it.

### 5. Deterministic client order IDs are mandatory

Every order placed by the strategy should have a deterministic, strategy-tagged client order ID.

This is required for:

- reconciliation,
- debugging,
- safe idempotency patterns,
- and traceability.

## Definitions

### Normal order
A standard futures order submitted through the normal trade endpoint.

Examples:
- `MARKET`
- `LIMIT`

### Algo order
A conditional / trigger-style order submitted through the algo-order path.

Examples:
- `STOP_MARKET`
- `TAKE_PROFIT_MARKET`
- `TRAILING_STOP_MARKET`

### Protective stop
The exchange-side hard fail-safe stop intended to close the open position if price reaches the invalidation level.

### Local state
The bot’s internal persisted view of:

- intended orders,
- known exchange order IDs,
- fills,
- position state,
- and stop-management stage.

### Reconciliation
The process of comparing local state with exchange state and resolving mismatches.

## Exchange State Sources

## Primary live sources

### User data stream events
The following are the key live private event types for v1:

- `ORDER_TRADE_UPDATE`
- `ACCOUNT_UPDATE`
- `ALGO_UPDATE`

These events are the primary real-time state feed during normal operation.

### Meaning of each

#### `ORDER_TRADE_UPDATE`
Used to track:
- normal order acceptance,
- fills,
- partial fills,
- cancellations,
- rejections,
- and terminal order outcomes.

#### `ACCOUNT_UPDATE`
Used to track:
- balance changes,
- position changes,
- realized PnL effects,
- and account-side updates relevant to risk and reconciliation.

#### `ALGO_UPDATE`
Used to track:
- protective stop status,
- trigger-order lifecycle,
- and algo-order state transitions.

## REST sources

REST should be used for:

- order placement
- order cancellation
- startup reconciliation
- exception recovery
- state confirmation when stream consistency is in doubt

For v1, the key REST queries are:

- new normal order
- new algo order
- open orders for symbol
- position information
- cancel all open orders for symbol

## Entry Order Design

## Strategy-side assumption

A long or short entry signal becomes valid only after the 15m breakout bar has fully closed.

## Execution-side entry method

### Selected method
- submit a **normal `MARKET` order**
- immediately after the confirming 15m signal bar closes

### Why this is selected
This is the cleanest first implementation because:

- the strategy is based on bar-close confirmation,
- BTCUSDT is highly liquid,
- and market entry avoids the extra state complexity of resting breakout-stop entry logic in v1.

## Entry order fields

For v1, entry orders should include the appropriate fields for:

- `symbol=BTCUSDT`
- `side=BUY` or `SELL`
- `type=MARKET`
- deterministic `newClientOrderId`
- one-way-mode assumptions

### Position side
Because v1 uses **one-way mode**, the execution design assumes the default one-way position behavior rather than hedge-mode logic.

## Entry acknowledgement policy

### Recommended policy
- submit the entry order
- accept exchange acknowledgement
- do **not** treat the position as established until live user-stream updates confirm the result

### Why this policy is selected
This keeps the user stream as the primary authoritative state path instead of over-trusting the immediate placement response.

The placement response is useful, but the strategy should not advance its internal state to “live position confirmed” until fill/position updates are received and reconciled.

## Entry state transitions

Recommended local state progression:

1. `signal_confirmed`
2. `entry_submitted`
3. `entry_acknowledged`
4. `entry_fill_confirmed`
5. `position_confirmed`
6. `protective_stop_submitted`
7. `protective_stop_confirmed`

The bot should not treat the trade as operationally protected until the protective stop has also been confirmed.

## Protective Stop Design

## Core rule

Every live position must have an exchange-side protective stop.

This is a hard rule.

## Selected protective stop model

After entry is confirmed, the system should place an algo stop with:

- order type: `STOP_MARKET`
- `closePosition=true`
- `workingType=MARK_PRICE`
- `priceProtect=TRUE`

## Why this is selected

This design gives the v1 bot a strong fail-safe because:

- the stop exists on the exchange,
- the stop can still protect the position even if the bot crashes,
- `MARK_PRICE` reduces sensitivity to last-trade distortions,
- and `closePosition=true` simplifies quantity handling for a one-position v1 design.

## Protective stop timing

The protective stop must be submitted **immediately after entry confirmation**.

The system must not intentionally remain exposed without protective stop coverage.

## Protective stop price source

The protective stop level is derived from the strategy’s structural invalidation logic:

- setup invalidation,
- breakout-bar invalidation,
- plus ATR buffer

The exact stop price comes from the strategy layer, but the execution layer is responsible for correctly expressing it as a valid algo order.

## Protective stop confirmation

The bot must confirm that the protective stop exists through exchange state, preferably via:

- `ALGO_UPDATE`
- and/or direct recovery queries if needed

Local assumption alone is not sufficient.

## Stop Update Policy

## Core rule

For v1, stop updates should use **cancel-and-replace**, not in-place modification.

## Why this is selected

The first version should prefer clarity over cleverness.

A cancel-and-replace approach is easier to reason about for:

- break-even transition,
- reduced-risk transition,
- and trailing-stop updates.

## Stop update triggers

The strategy layer may instruct stop updates at stages such as:

- first risk reduction after +1R,
- break-even transition after follow-through,
- trailing management after +2R,
- tighter management at later profit stages if enabled.

The execution layer should not invent these transitions. It should only apply them when instructed by the strategy state machine.

## Stop update sequence

Recommended sequence:

1. verify current position still exists
2. identify active protective stop
3. cancel current protective stop
4. confirm cancellation
5. submit replacement protective stop
6. confirm replacement exists
7. update local state only after confirmation

## Important safety rule

At no point should the system intentionally lose track of whether the position is protected.

If a replacement stop cannot be confirmed, the bot must enter an exception state and prevent new strategy actions until resolved.

## Trailing Stop Policy

For v1, trailing behavior should remain **strategy-managed**, not fully delegated to exchange-native trailing order logic unless explicitly tested and approved later.

This means:

- the strategy decides when the stop should move,
- the execution layer expresses that move using the cancel-and-replace protective-stop workflow.

This is simpler to audit and keeps the trailing logic aligned with the same staged management rules used in research and backtesting.

## Local State Requirements

The execution system must persist enough local state to survive restart and recovery.

Minimum local state should include:

- strategy symbol
- active strategy variant
- current strategy stage
- current signal timestamp
- expected entry side
- entry client order ID
- entry exchange order ID if known
- entry fill timestamp
- average fill price
- current position side
- current position size
- current protective stop client order ID
- current protective stop exchange order ID if known
- current stop stage
- current trailing stage if active
- last successful reconciliation time
- exception flags
- kill-switch state

## Startup and Recovery Reconciliation

## When reconciliation is required

Reconciliation must run:

- on bot startup
- after restart
- after stream interruption
- after detected state inconsistency
- after any exception that could affect order or position certainty

## Recovery sequence

Recommended recovery sequence for v1:

1. load persisted local state
2. fetch current BTCUSDT position information
3. fetch current BTCUSDT open orders
4. compare exchange position with local position state
5. compare exchange open orders with local tracked orders
6. identify whether a protective stop exists
7. resolve mismatches
8. only resume strategy actions after reconciliation succeeds

## Reconciliation outcomes

### Clean state
No mismatch between local and exchange state.

Result:
- normal operation may resume

### Recoverable mismatch
Mismatch exists but can be resolved safely.

Examples:
- missing local order ID but exchange order clearly identifiable
- position exists but local stop reference missing
- order canceled on exchange but local state not updated

Result:
- repair local state and continue only after explicit resolution

### Unsafe mismatch
State cannot be trusted immediately.

Examples:
- exchange position exists but stop protection cannot be confirmed
- conflicting open orders exist
- position quantity does not match assumptions
- stream gap occurred and exchange state is unclear

Result:
- block new entries
- raise alert
- enter safe recovery state

## User Stream Lifecycle

## Listen key behavior

The v1 bot must treat user-stream maintenance as mandatory operational logic.

The stream lifecycle includes:

- obtaining the listen key
- keeping it alive on schedule
- detecting disconnects
- reconnecting cleanly
- and reconciling after interruption when necessary

## Event routing

The bot should explicitly route the following event classes to state handlers:

- normal-order updates
- algo-order updates
- account/position updates

Each event handler should be idempotent where practical.

## Stream failure handling

If the stream disconnects, expires, or appears stale:

1. block new entries
2. keep local exception state visible
3. reconnect / refresh the stream
4. reconcile position and open orders
5. only resume after reconciliation succeeds

## REST Query Discipline

## Allowed use of REST

REST is appropriate for:

- placing orders
- canceling orders
- startup reconciliation
- exception handling
- spot-check confirmation of live state

## Discouraged use of REST

REST should **not** be used as the primary constant live-state loop during normal operation.

The system should not rely on repeated broad polling as its normal control mechanism.

## Symbol scoping

Whenever possible, REST recovery queries should be scoped to:

- `symbol=BTCUSDT`

This reduces noise, cost, and ambiguity.

## Client Order ID Policy

Every order created by the bot should use a deterministic client order ID pattern.

### Design goals
The ID should encode enough information to help with:

- tracing
- reconciliation
- distinguishing entry vs stop
- linking orders to strategy stages
- debugging after restart

### Suggested components
A client order ID scheme may include:

- strategy prefix
- symbol
- order role
- side
- timestamp or monotonic unique token
- optional stage code

### Example roles
- `ENTRY`
- `STOP`
- `STOP_REPL`
- `EXIT`
- `EMERGENCY`

The exact string format can be finalized later, but the policy must be deterministic and documented.

## Kill Switch and Emergency Handling

## Kill-switch behavior

When the kill switch is activated:

1. block all new strategy entries
2. stop any strategy-side order generation
3. assess current open orders
4. cancel open orders associated with the strategy symbol where appropriate
5. determine whether the current position should be flattened immediately or kept with protective stop depending on the scenario
6. raise an operator-visible alert

## Emergency flattening

Flattening should be considered when:

- local and exchange state cannot be reconciled safely
- protective stop status cannot be trusted
- execution logic is degraded
- or operator intervention rules require immediate de-risking

The exact flattening rule should remain conservative and explicit.

## Safe-mode principle

If the engine is uncertain about position protection or state correctness, it should prefer:

- blocking new exposure
- preserving or restoring protection
- and escalating visibly

rather than continuing normally under uncertainty.

## Failure Modes

The order-handling layer is expected to fail primarily in these ways:

### 1. Entry acknowledged but position not yet confirmed
The system must not assume fill completion too early.

### 2. Position exists but protective stop is missing
This is one of the most serious operational failure states.

### 3. Stream disconnect or expiration
State can become stale if live private events stop arriving.

### 4. Local state diverges from exchange state
This can happen after restart, network issues, or partial event loss.

### 5. Cancel-and-replace sequence breaks midway
The system must detect and handle this rather than assuming protection exists.

### 6. Multiple open orders exist unexpectedly
This should trigger reconciliation and exception handling immediately in v1.

## Operational Restrictions for V1

The order-handling design assumes the following restrictions remain active:

- BTCUSDT only
- one strategy only
- one-way mode only
- isolated margin only
- one open position at a time
- one active protective stop at a time
- no hedge-mode logic
- no multi-leg order choreography
- no portfolio-level routing

These restrictions are intentional.

## Decisions

The following decisions are accepted for the v1 order-handling design:

- user-stream events are the primary live source of truth
- REST is used for placement, cancellation, recovery, and reconciliation
- entry orders use the normal futures order endpoint
- entry type remains market-on-confirmed-bar-close
- entry state is not considered final until stream-confirmed
- protective stops use conditional/algo orders
- protective stop type is `STOP_MARKET`
- protective stops use `closePosition=true`
- protective stop trigger uses `MARK_PRICE`
- protective stops use `priceProtect=TRUE`
- stop updates use cancel-and-replace in v1
- startup recovery uses position and open-order reconciliation
- all bot-created orders require deterministic client order IDs
- one-way mode assumptions apply throughout the order-handling design

## Open Questions

The following remain open:

1. What exact client order ID format should be standardized?
2. Should entry orders use `ACK` or `RESULT` response handling in the first implementation, even if stream confirmation remains authoritative?
3. What exact timeout should define a missing entry confirmation before recovery logic begins?
4. What exact timeout should define a missing stop-confirmation event before exception handling begins?
5. Under which failure scenarios should the bot flatten immediately versus preserve the current protective stop and wait for operator review?
6. Should exchange-native trailing-stop orders be tested later against the strategy-managed cancel-and-replace trailing model?
7. What exact alert routing should be triggered for each execution failure class?

## Next Steps

After this document, the next recommended files are:

1. `docs/04-data/timestamp-policy.md`
2. `docs/04-data/dataset-versioning.md`
3. `docs/09-operations/restart-procedure.md`

## References

Binance references:

- Binance USDⓈ-M Futures General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info

- Binance USDⓈ-M Futures New Order REST API  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

- Binance USDⓈ-M Futures New Algo Order  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Algo-Order

- Binance USDⓈ-M Futures Position Information V3  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Position-Information-V3

- Binance USDⓈ-M Futures Current All Open Orders  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Current-All-Open-Orders

- Binance USDⓈ-M Futures Cancel All Open Orders  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Cancel-All-Open-Orders

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams

- Binance USDⓈ-M Futures Event: Order Update  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Order-Update

- Binance USDⓈ-M Futures Event: Account Update  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Balance-and-Position-Update

- Binance USDⓈ-M Futures Event: Algo Orders Update  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Conditional-Order-Trigger-Reject

- Binance Derivatives Change Log  
  https://developers.binance.com/docs/derivatives/change-log