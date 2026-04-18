# Binance USDⓈ-M Order Model

## Purpose

This document defines the Binance USDⓈ-M futures order model as used by the v1 Prometheus trading system.

Its purpose is to provide an exchange-specific order vocabulary and mechanics reference so that implementation does not confuse:

- normal orders,
- algo / conditional orders,
- order acknowledgements,
- fills,
- position confirmation,
- protective stop confirmation,
- user-stream events,
- REST reconciliation reads,
- and local runtime state.

This document supports the existing v1 order-handling notes.

It does not replace them.

The order-handling notes define Prometheus-specific execution policy. This document defines the Binance-specific order concepts and how Prometheus should normalize them internally.

This document replaces the previous TBD placeholder for:

```text
docs/06-execution-exchange/binance-usdm-order-model.md
```

## Scope

This document applies to the v1 Prometheus implementation under the following assumptions:

- venue: Binance USDⓈ-M futures
- initial live symbol: BTCUSDT perpetual
- first secondary research comparison: ETHUSDT perpetual
- v1 live symbol scope: BTCUSDT only
- position mode: one-way mode
- margin mode: isolated margin
- entry order: normal MARKET order
- entry timing: after completed 15m signal candle confirmation
- protective stop: algo / conditional STOP_MARKET order
- protective stop behavior:
  - closePosition=true
  - workingType=MARK_PRICE
  - priceProtect=TRUE
- stop update method: cancel-and-replace
- user stream: primary live source of order/account/protection updates
- REST: placement, cancellation, reconciliation, recovery
- exchange state is authoritative

This document covers:

- Binance order categories,
- Prometheus order role mapping,
- normal order model,
- algo order model,
- client ID model,
- one-way mode assumptions,
- response type policy,
- order status normalization,
- user-stream event mapping,
- position/protection truth boundaries,
- unknown status handling,
- reconciliation identifiers,
- persistence-relevant fields,
- and implementation/testing requirements.

This document does **not** define:

- final adapter class implementation,
- final client order ID string format,
- complete Binance API wrapper,
- position-sizing formula,
- stop-loss risk policy,
- restart procedure,
- incident response,
- dashboard layout,
- or final production deployment.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/06-execution-exchange/user-stream-reconciliation.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/exposure-limits.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`

### Authority hierarchy

If this document conflicts with official Binance API documentation, implementation must stop and review the conflict.

If this document conflicts with Prometheus order-handling notes on v1 execution policy, the order-handling notes win.

If this document conflicts with the state model on runtime truth, the state model wins.

If this document conflicts with stop-loss policy on protective stop risk behavior, the stop-loss policy wins.

---

## Core Principles

## 1. Order model is not truth model

An order being accepted does not prove a position exists.

A stop order being accepted does not prove a position is protected.

Order-level information must be reconciled into runtime state before the bot can trust it.

## 2. Normal orders and algo orders are distinct

Prometheus must model normal orders and algo / conditional orders separately.

Normal orders and algo orders use different endpoint families, identifiers, event types, and query paths.

## 3. REST acknowledgement is not final runtime truth

REST placement responses are useful, but they do not replace user-stream and reconciliation-based confirmation.

## 4. User stream is primary live truth path

Normal order lifecycle and account changes should be driven primarily from user-stream events during live operation.

Algo/protective stop lifecycle should also be tracked through private stream events where available.

## 5. Unknown or ambiguous order state fails closed

If Prometheus cannot classify an order outcome safely, it must block new entries and reconcile before continuing.

## 6. One-way mode is assumed

V1 assumes one-way mode.

Hedge-mode behavior is not supported in v1.

If hedge mode or ambiguous position-side behavior is detected, live trading must be blocked until corrected.

## 7. Deterministic client identifiers are required

Prometheus must use deterministic, strategy-tagged client identifiers for both normal orders and algo orders.

These identifiers are central to reconciliation and duplicate-prevention.

---

## Binance Order Categories

For v1, Prometheus should distinguish two Binance order categories.

## 1. Normal Orders

Normal futures orders are used for direct order actions such as market entry and market exit.

Prometheus v1 uses normal orders for:

```text
entry market order
market exit order
emergency flatten order
```

Relevant normal order type for v1:

```text
MARKET
```

Other normal order types may exist on Binance, but they are not active v1 behavior unless explicitly approved later.

## 2. Algo / Conditional Orders

Algo orders are used for conditional trigger-based order behavior.

Prometheus v1 uses algo orders for:

```text
initial protective stop
replacement protective stop
```

Relevant algo order type for v1:

```text
STOP_MARKET
```

Other conditional order types may exist, including:

```text
STOP
TAKE_PROFIT
TAKE_PROFIT_MARKET
TRAILING_STOP_MARKET
```

These are not v1 active order types unless separately approved.

---

## Prometheus Order Roles

Every Prometheus-managed order should have an internal order role.

Recommended order roles:

```text
ENTRY
EXIT
EMERGENCY_FLATTEN
PROTECTIVE_STOP
REPLACEMENT_PROTECTIVE_STOP
STALE_CLEANUP
UNKNOWN_EXTERNAL
```

## Role meanings

### `ENTRY`

Normal market order used to enter a strategy-approved position.

### `EXIT`

Normal market order used to exit a strategy-owned position under approved exit logic.

### `EMERGENCY_FLATTEN`

Normal market order used to flatten exposure during emergency handling.

### `PROTECTIVE_STOP`

Exchange-side algo STOP_MARKET order used as the active protective stop for a live position.

### `REPLACEMENT_PROTECTIVE_STOP`

Exchange-side algo STOP_MARKET order submitted during stop replacement.

### `STALE_CLEANUP`

Cancellation or cleanup operation for stale/unexpected orders.

### `UNKNOWN_EXTERNAL`

Order or position detected on exchange that cannot be classified as Prometheus-owned.

This should block new entries and require reconciliation/operator review.

---

## Normal Order Model

## V1 entry order

The v1 entry order is:

```text
normal MARKET order
```

Expected internal action:

```text
execution.submit_entry_order
```

Expected Binance-side concept:

```text
POST /fapi/v1/order
```

Implementation must verify the exact current endpoint and parameters against official Binance documentation at coding time.

## Required Prometheus fields for entry

Minimum internal fields:

```text
symbol
side
quantity
order_role
client_order_id
correlation_id
approved_risk_reference
strategy_id
config_version
```

## Expected Binance fields for entry

Conceptual mapping:

```text
symbol=BTCUSDT
side=BUY or SELL
type=MARKET
quantity=approved_quantity
newClientOrderId=deterministic client order ID
newOrderRespType=ACK for initial v1 preference
```

## One-way mode position side

V1 assumes one-way mode.

If Binance expects position side behavior, it should default to one-way semantics such as `BOTH` where appropriate.

The implementation must not send hedge-mode `LONG` or `SHORT` position-side behavior in v1 unless account mode is explicitly changed in a future version.

## Normal market exit

Market exit and emergency flatten actions also use normal order mechanics.

They must be routed through approved execution/safety paths.

They are not discretionary manual trade controls.

---

## Algo Order Model

## V1 protective stop

The v1 protective stop is:

```text
algo / conditional STOP_MARKET order
```

Expected internal action:

```text
execution.submit_protective_stop
```

Expected Binance-side concept:

```text
POST /fapi/v1/algoOrder
```

Implementation must verify the exact current endpoint and parameters against official Binance documentation at coding time.

## Required Prometheus fields for protective stop

Minimum internal fields:

```text
symbol
side
stop_trigger_price
order_role
client_algo_id
trade_reference
correlation_id
working_type
close_position
price_protect
strategy_id
config_version
```

## Expected Binance fields for protective stop

Conceptual mapping:

```text
symbol=BTCUSDT
algoType=CONDITIONAL
side=opposite side required to close current position
type=STOP_MARKET
triggerPrice=approved stop trigger
workingType=MARK_PRICE
closePosition=true
priceProtect=TRUE
clientAlgoId=deterministic protective stop ID
```

## Quantity rule

When using `closePosition=true`, implementation must not send quantity if Binance rules forbid the combination.

## Reduce-only rule

When using `closePosition=true`, implementation must not send `reduceOnly` if Binance rules forbid the combination.

## Stop acknowledgement rule

A successful algo order REST response means:

```text
protective stop submitted or acknowledged
```

It does not mean:

```text
position protected
```

Protection is confirmed only through exchange-state evidence such as:

- `ALGO_UPDATE`,
- open algo order query,
- reconciliation result.

---

## Response Type Policy

## Initial v1 preference

Initial v1 should prefer:

```text
newOrderRespType=ACK
```

for normal market entry orders.

## Why ACK is preferred initially

ACK supports the project’s state-authority design by reducing the temptation to treat the REST response as final truth.

The system should progress based on user-stream and reconciliation evidence.

## RESULT may be evaluated later

Binance supports `RESULT` behavior for some order types, including returning final `FILLED` result for market orders where applicable.

Prometheus may evaluate `RESULT` later if useful.

However:

```text
RESULT must not change the truth model.
```

Even if REST returns filled details, Prometheus must still preserve user-stream/reconciliation-based authority for final runtime state.

## Algo order response type

Algo order response type should be selected conservatively and tested.

Whatever response type is used, it must not be treated as final protection confirmation.

---

## Client Identifier Model

Prometheus must use deterministic client identifiers.

## Normal order client ID

Normal orders use:

```text
newClientOrderId
```

Prometheus should persist:

```text
normal_client_order_id
normal_exchange_order_id
```

## Algo order client ID

Algo orders use:

```text
clientAlgoId
```

Prometheus should persist:

```text
protective_stop_client_algo_id
protective_stop_exchange_algo_id
```

## Important distinction

Do not mix normal order IDs and algo order IDs.

A protective stop's `clientAlgoId` is not the same field as a normal order's `newClientOrderId`.

A normal order's `orderId` is not the same thing as an algo order's `algoId`.

## Client ID requirements

Client IDs should:

- be deterministic,
- be unique among relevant open orders,
- include or map to order role,
- include or map to trade reference,
- support restart/reconciliation,
- fit Binance length/pattern constraints,
- avoid secrets or sensitive data.

## Recommended encoded information

A compact client ID may reference:

```text
bot prefix
environment short code
strategy ID
symbol short code
order role
trade/correlation reference
sequence or short unique suffix
```

## Forbidden client ID contents

Client IDs must not contain:

- API keys,
- secrets,
- account identifiers,
- personal information,
- long free-text reasons,
- unbounded timestamps that exceed length constraints.

---

## One-Way Mode Model

V1 assumes:

```text
one-way mode
```

## Practical meaning

- one net position per symbol,
- no simultaneous LONG and SHORT legs,
- position side should be default/BOTH where Binance expects one-way behavior,
- hedge mode is not supported.

## Hedge mode detection

If hedge mode is detected:

```text
block live trading
raise operator-visible error
require correction before resumption
```

## Position-side confusion

If an order or stream event contains position-side behavior inconsistent with one-way mode:

```text
enter safe mode or block entries
reconcile
require operator review if unresolved
```

---

## Margin Mode Model

V1 assumes:

```text
isolated margin
```

## Practical meaning

The bot should verify BTCUSDT margin mode before live operation.

If margin mode is not isolated:

```text
reject live entry
block live trading until corrected
```

Do not silently trade in cross margin.

---

## Order Lifecycle Vocabulary

Prometheus should normalize exchange order statuses into internal lifecycle states.

## Normal order statuses

Expected statuses may include:

```text
NEW
PARTIALLY_FILLED
FILLED
CANCELED
EXPIRED
REJECTED
EXPIRED_IN_MATCH
```

Implementation must map any unknown value to an unknown/unsafe category.

## Execution types

Expected execution types may include:

```text
NEW
TRADE
CANCELED
EXPIRED
CALCULATED
AMENDMENT
```

Implementation must handle unknown execution types safely.

## Internal normal order lifecycle

Recommended internal lifecycle:

```text
SUBMISSION_REQUESTED
SUBMITTED
ACKNOWLEDGED
PARTIALLY_FILLED
FILLED
CANCELED
REJECTED
EXPIRED
UNKNOWN
```

## Terminal states

Terminal normal order states include:

```text
FILLED
CANCELED
REJECTED
EXPIRED
EXPIRED_IN_MATCH
```

However, terminal order state does not by itself prove complete trade lifecycle safety.

Example:

```text
entry FILLED
```

still requires:

```text
position confirmed
protective stop submitted
protective stop confirmed
```

---

## Algo Order Lifecycle Vocabulary

Prometheus should normalize algo order state separately from normal order state.

## Expected algo states

Expected algo statuses may include values such as:

```text
NEW
CANCELED
TRIGGERED
FINISHED
EXPIRED
REJECTED
```

Implementation must verify current Binance values at coding time.

Unknown algo statuses must map to:

```text
UNKNOWN_ALGO_STATE
```

## Internal algo lifecycle

Recommended internal lifecycle:

```text
ALGO_SUBMISSION_REQUESTED
ALGO_SUBMITTED
ALGO_ACKNOWLEDGED
ALGO_ACTIVE
ALGO_TRIGGERED
ALGO_CANCELED
ALGO_REJECTED
ALGO_EXPIRED
ALGO_FINISHED
ALGO_UNKNOWN
```

## Protective stop state distinction

An algo order being active supports protection, but Prometheus must still connect it to:

- correct symbol,
- correct trade reference,
- correct side,
- correct trigger price,
- correct close-position behavior,
- and current position state.

---

## User Data Stream Events

The private user stream is the primary live source of order/account/protection events.

## Required event types for v1

Prometheus should support at minimum:

```text
ORDER_TRADE_UPDATE
ACCOUNT_UPDATE
ALGO_UPDATE
```

## `ORDER_TRADE_UPDATE`

Used for normal order lifecycle.

Relevant for:

- entry order created,
- entry acknowledged,
- entry partially filled,
- entry filled,
- entry canceled,
- entry rejected,
- market exit filled,
- emergency flatten filled.

## `ACCOUNT_UPDATE`

Used for account and position state.

Relevant for:

- position size changes,
- balance updates,
- realized PnL,
- margin changes,
- position confirmation after fill.

## `ALGO_UPDATE`

Used for algo/protective stop lifecycle.

Relevant for:

- protective stop created,
- protective stop active,
- protective stop canceled,
- protective stop triggered,
- protective stop rejected,
- replacement stop lifecycle.

## User stream event limitations

User-stream events can be delayed, disconnected, or missed.

If private stream confidence is lost:

- block new entries,
- reconcile using REST,
- do not assume state is still clean.

---

## REST Query and Reconciliation Model

REST queries are used for:

- order placement,
- cancellation,
- querying current order status,
- querying current algo order status,
- querying open normal orders,
- querying open algo orders,
- querying current position state,
- startup reconciliation,
- recovery after uncertainty.

## Symbol-scoped reads

Where possible, v1 should use symbol-scoped reads for BTCUSDT.

This reduces ambiguity and request load.

## Required reconciliation reads

At startup or confidence loss, the system should be able to query:

```text
current BTCUSDT position
open normal orders for BTCUSDT
open algo orders for BTCUSDT
specific normal order by client/order ID
specific algo order by clientAlgoId/algoId
```

## REST query limitations

A REST query gives a snapshot.

It must be interpreted in reconciliation context.

It does not replace user-stream event history or persisted state.

---

## Entry Truth Model

## What confirms entry submission

Entry submission may be recognized from:

- execution command accepted locally,
- REST request sent,
- REST response received,
- user-stream order event.

## What confirms entry fill

Entry fill should be confirmed through:

- user-stream `ORDER_TRADE_UPDATE` with trade/fill evidence,
- order query showing filled status,
- reconciliation result.

## What confirms position

Position should be confirmed through:

- user-stream account update,
- position REST query,
- reconciliation result.

## Important distinction

```text
entry filled != position protected
```

A filled entry still requires protective stop submission and confirmation.

---

## Protective Stop Truth Model

## What confirms stop submission

Stop submission may be recognized from:

- execution command,
- REST request,
- REST response,
- algo update.

## What confirms stop protection

Protection is confirmed only when exchange state shows a valid stop exists and matches the expected trade.

Acceptable sources:

- `ALGO_UPDATE`,
- open algo order query,
- reconciliation result.

## Protection matching criteria

A protective stop must match:

- symbol,
- expected side,
- expected order role,
- clientAlgoId lineage,
- active status,
- trigger price within approved tolerance,
- `closePosition=true`,
- `workingType=MARK_PRICE`,
- `priceProtect=TRUE`,
- current active trade reference.

If any critical field does not match:

```text
protection uncertain
```

---

## Unknown and Ambiguous State Handling

Unknown order state must fail closed.

## Examples

- REST timeout after submit request,
- malformed REST response,
- missing user-stream confirmation,
- unknown order status value,
- unknown algo status value,
- open algo order query unavailable,
- order exists without recognized client ID,
- position exists without known entry lineage,
- duplicate client ID ambiguity,
- user-stream gap during active position,
- cancel response unknown,
- replacement stop response unknown.

## Required response

When state is unknown:

```text
block new entries
enter SAFE_MODE or RECOVERING
reconcile exchange state
raise operator-visible warning or incident
do not blindly retry exposure-changing request
```

## Retry policy

Do not blindly retry:

- entry submission,
- protective stop submission,
- stop cancellation,
- stop replacement,
- flattening order,

when outcome is unknown.

Query state first.

---

## Normalized Internal Models

Prometheus should normalize raw Binance payloads into internal models.

Recommended models:

```text
NormalizedNormalOrder
NormalizedAlgoOrder
NormalizedOrderUpdate
NormalizedAlgoUpdate
NormalizedAccountUpdate
NormalizedPositionSnapshot
NormalizedOpenOrdersSnapshot
NormalizedOpenAlgoOrdersSnapshot
OrderRole
NormalOrderLifecycleStatus
AlgoOrderLifecycleStatus
ExecutionUncertainty
```

## `NormalizedNormalOrder`

Minimum fields:

```text
exchange
symbol
order_role
client_order_id
exchange_order_id
side
order_type
status
execution_type if from stream
quantity
filled_quantity
average_price if available
last_fill_price if available
event_time_utc_ms
processed_at_utc_ms
correlation_id
raw_payload_reference if safe
```

## `NormalizedAlgoOrder`

Minimum fields:

```text
exchange
symbol
order_role
client_algo_id
exchange_algo_id
side
algo_type
order_type
algo_status
trigger_price
working_type
close_position
price_protect
event_time_utc_ms
processed_at_utc_ms
correlation_id
raw_payload_reference if safe
```

## `NormalizedPositionSnapshot`

Minimum fields:

```text
exchange
symbol
position_side
position_size
entry_price
mark_price if available
unrealized_pnl if available
margin_mode
event_time_utc_ms if available
processed_at_utc_ms
source
```

## Raw payload policy

Raw payloads may be retained internally for debugging if safe.

They must be redacted before logging and must not contain secrets.

---

## Persistence-Relevant Fields

The runtime should persist identifiers needed for restart and reconciliation.

## Entry order fields

```text
trade_reference
symbol
entry_client_order_id
entry_exchange_order_id
entry_side
entry_quantity
entry_order_status
entry_submitted_at_utc_ms
entry_fill_confirmed_at_utc_ms
```

## Protective stop fields

```text
trade_reference
symbol
protective_stop_client_algo_id
protective_stop_exchange_algo_id
protective_stop_side
protective_stop_trigger_price
protective_stop_status
protective_stop_submitted_at_utc_ms
protective_stop_confirmed_at_utc_ms
```

## Uncertainty fields

```text
unknown_execution_status
unknown_order_reference
unknown_algo_reference
uncertainty_detected_at_utc_ms
reconciliation_required
```

---

## Reconciliation-Relevant Matching

## Strategy-owned normal order matching

A normal order may be considered Prometheus-owned if it matches:

- known client order ID prefix/format,
- persisted trade reference,
- expected symbol,
- expected role,
- expected side,
- expected quantity,
- known correlation ID lineage where available.

If it cannot be classified:

```text
UNKNOWN_EXTERNAL
```

## Strategy-owned algo order matching

An algo order may be considered Prometheus-owned if it matches:

- known clientAlgoId prefix/format,
- persisted trade reference,
- expected symbol,
- protective stop role,
- expected side,
- expected stop trigger,
- expected close-position behavior.

If it cannot be classified:

```text
UNKNOWN_EXTERNAL
```

## Manual/non-bot order

Any order that cannot be classified as Prometheus-owned should trigger exposure-limit behavior:

```text
block new entries
require operator review
```

---

## Stop Replacement Order Model

V1 stop replacement uses cancel-and-replace.

## Replacement sequence

```text
identify active protective stop
cancel current algo stop
confirm cancellation
submit replacement algo stop
confirm replacement active
```

## Important states

During replacement:

```text
STOP_REPLACEMENT_IN_PROGRESS
```

If replacement status is unknown:

```text
PROTECTION_UNCERTAIN
```

If position exists and no valid stop exists:

```text
EMERGENCY_UNPROTECTED
```

## Replacement ID model

Replacement protective stop should receive a new deterministic `clientAlgoId`.

Old and new stop IDs should be linked in persistence and observability.

---

## Orphaned and Unexpected Orders

## Orphaned protective stop

If no position exists but protective stop exists:

```text
orphaned protective stop
```

Response:

- block entries,
- classify order,
- cancel if deterministic and safe,
- reconcile again.

## Multiple protective stops

If more than one active protective stop exists for the same strategy position:

```text
multiple protective stops
```

Response:

- block entries,
- classify mismatch,
- cancel duplicate if deterministic,
- require operator review if ambiguous.

## Unexpected normal order

If an unexpected normal order exists:

- block entries,
- classify ownership,
- cancel if safe and strategy-owned,
- require operator review if external/unknown.

---

## Observability Requirements

Order model events must be visible and traceable.

## Required fields in order events

Where relevant:

```text
order_role
symbol
client_order_id
exchange_order_id
client_algo_id
exchange_algo_id
order_type
algo_type
side
status
execution_type
quantity
filled_quantity
trigger_price
working_type
close_position
price_protect
event_time_utc_ms
processed_at_utc_ms
correlation_id
causation_id
```

## Required alerts

Alerts should be generated for:

- unknown order status,
- unknown algo status,
- entry status unknown,
- stop status unknown,
- stop rejected,
- stop missing,
- orphaned stop,
- multiple stops,
- external/unclassified order,
- user-stream gap involving active order,
- REST query failure during reconciliation.

---

## Testing Requirements

Implementation must include tests for the following.

## Normal order tests

- market entry command maps to normal order model,
- `newClientOrderId` is required,
- ACK response does not mark filled,
- filled user-stream update confirms fill,
- position confirmation remains separate from fill confirmation,
- unknown status maps to safe failure.

## Algo order tests

- protective stop command maps to algo order model,
- `clientAlgoId` is required,
- `STOP_MARKET` is used,
- `closePosition=true` is represented,
- `workingType=MARK_PRICE` is represented,
- `priceProtect=TRUE` is represented,
- algo REST acknowledgement does not mark protection confirmed,
- `ALGO_UPDATE` or open algo query can confirm protection,
- unknown algo state maps to safe failure.

## ID tests

- normal and algo IDs are not mixed,
- strategy-owned normal order classification works,
- strategy-owned algo order classification works,
- unknown external order classification blocks entries,
- duplicate ID ambiguity triggers reconciliation.

## One-way mode tests

- one-way mode uses expected position-side behavior,
- hedge-mode data blocks live operation,
- unexpected position-side values trigger safe handling.

## Reconciliation tests

- open normal order matched to local trade,
- open algo order matched to protective stop,
- orphaned stop detected,
- multiple protective stops detected,
- position exists without stop detected.

---

## V1 Non-Goals

The Binance USDⓈ-M order model for v1 does not include:

- hedge-mode support,
- multi-symbol live orchestration,
- native exchange trailing stop as default,
- take-profit orders,
- limit entry orders,
- grid orders,
- scale-in orders,
- partial take-profit ladders,
- portfolio margin behavior,
- options or coin-margined futures,
- discretionary manual trading terminal behavior,
- WebSocket API trading as primary order path.

These may be researched later, but they are not v1 behavior.

---

## Open Questions

The following should be resolved during implementation or before paper/shadow.

## 1. Exact client ID format

The format must satisfy Binance constraints while carrying enough role/correlation information.

## 2. ACK versus RESULT later-stage policy

Initial v1 prefers ACK.

RESULT may be evaluated later if it improves diagnostics without weakening truth-model discipline.

## 3. Exact confirmation timeouts

Entry fill, position confirmation, stop confirmation, cancel confirmation, and replacement confirmation require configurable timeouts.

## 4. Exact unknown-status escalation thresholds

Unknown status should fail closed, but implementation needs concrete thresholds for incident severity and retry/reconciliation cadence.

## 5. Exact algo status vocabulary

Implementation must verify current Binance algo status values and keep normalizers updated.

---

## Acceptance Criteria

This Binance USDⓈ-M order model is satisfied when implementation can demonstrate:

- normal orders and algo orders are modeled separately,
- v1 entry uses normal MARKET order,
- v1 protective stop uses algo STOP_MARKET order,
- normal order IDs and algo order IDs are not mixed,
- initial v1 prefers ACK for normal market entry response,
- REST acknowledgements are not treated as final truth,
- fills are distinct from position confirmation,
- stop submission is distinct from protection confirmation,
- one-way mode is required,
- hedge-mode behavior blocks live operation,
- user-stream `ORDER_TRADE_UPDATE` is normalized for normal order lifecycle,
- user-stream `ACCOUNT_UPDATE` is normalized for position/account state,
- user-stream `ALGO_UPDATE` is normalized for protective stop lifecycle,
- unknown statuses fail closed,
- unclassified orders block entries,
- reconciliation can match exchange orders to local trade references,
- and operator-visible alerts exist for unknown, orphaned, or conflicting order states.

---

## References

Official Binance references to verify during implementation:

- Binance USDⓈ-M Futures New Order REST API  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

- Binance USDⓈ-M Futures New Algo Order REST API  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Algo-Order

- Binance USDⓈ-M Futures Order Update User Stream Event  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Order-Update

- Binance USDⓈ-M Futures Algo Order Update User Stream Event  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Algo-Order-Update

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams

- Binance Derivatives Change Log  
  https://developers.binance.com/docs/derivatives/change-log

Implementation must verify these references at coding time because Binance derivatives APIs may change.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Binance USDⓈ-M futures order-model reference
