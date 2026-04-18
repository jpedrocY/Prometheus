# Exchange Adapter Design

## Purpose

This document defines the exchange-adapter design for the v1 Prometheus trading system.

Its purpose is to create a strict implementation boundary between Prometheus internal logic and Binance USDⓈ-M futures APIs.

The exchange adapter exists so that:

- strategy code does not call Binance directly,
- risk code does not place orders,
- execution code uses a controlled interface,
- user-stream events are normalized before entering runtime state,
- REST responses are normalized before reconciliation,
- exchange-specific mechanics do not leak through the entire codebase,
- credentials and signatures remain isolated,
- rate limits and request discipline are centralized,
- and live trading behavior remains testable through fake adapters.

This document replaces the previous TBD placeholder for:

```text
docs/06-execution-exchange/exchange-adapter-design.md
```

## Scope

This design applies to v1 with the following assumptions:

- exchange venue: Binance USDⓈ-M futures
- initial live symbol: BTCUSDT perpetual
- first research comparison symbol: ETHUSDT perpetual
- live v1 symbol scope: BTCUSDT only
- one-way mode
- isolated margin
- one active strategy
- one open position maximum
- one active protective stop maximum
- supervised deployment
- strategy entry: market order after completed 15m signal bar
- protective stop: exchange-side STOP_MARKET algo order
- protective stop settings:
  - `closePosition=true`
  - `workingType=MARK_PRICE`
  - `priceProtect=TRUE`
- user-stream events are the primary live state source
- REST is used for placement, cancellation, startup reconciliation, recovery, and exception handling

This document covers:

- adapter responsibilities,
- adapter non-responsibilities,
- module boundaries,
- REST client boundaries,
- WebSocket / stream boundaries,
- signed request policy,
- response normalization,
- command-to-exchange mapping,
- exchange-derived events,
- idempotency and client IDs,
- error and uncertainty handling,
- rate-limit handling,
- test/fake adapter requirements,
- security boundaries,
- and implementation constraints.

This document does **not** define:

- final Python class implementations,
- final library selection,
- final infrastructure deployment,
- final operator dashboard UI,
- final database schema,
- or final Binance credential setup.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/08-architecture/implementation-blueprint.md`
- `docs/08-architecture/codebase-structure.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/observability-design.md`
- `docs/04-data/live-data-spec.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/10-security/api-key-policy.md`
- `docs/10-security/secrets-management.md`
- `docs/10-security/permission-scoping.md`

### Authority hierarchy

If this document conflicts with security policy, security policy wins.

If this document conflicts with the state model on runtime truth or protection states, the state model wins.

If this document conflicts with order-handling notes on accepted v1 order behavior, the order-handling notes win.

If Binance official API documentation changes, the implementation must be reviewed and this document updated before live use.

---

## Core Design Principles

## 1. The adapter is a boundary, not business logic

The exchange adapter translates between Prometheus internal commands/events and Binance-specific API mechanics.

It should not decide:

- whether the strategy has a signal,
- how much risk is allowed,
- whether a trade is desirable,
- whether an incident is cleared,
- or whether operator approval is granted.

Those decisions belong to strategy, risk, safety, state, and operator-control layers.

## 2. Strategy must not know Binance

The strategy engine must not import Binance clients, REST endpoint wrappers, WebSocket clients, or exchange-specific request models.

The strategy should only produce internal strategy decisions or intents.

## 3. Risk must not place orders

The risk layer may approve, reject, and size a candidate trade.

It must not own credentials, submit orders, cancel stops, or query private account endpoints directly.

## 4. Execution uses the adapter, not raw HTTP

The execution layer may request exchange actions through an adapter interface.

It should not scatter raw endpoint calls, signing logic, or response parsing across the codebase.

## 5. Exchange truth must be normalized

Exchange responses and user-stream events must be converted into internal typed models before state/reconciliation logic consumes them.

The runtime should not depend on raw Binance payload shapes throughout the system.

## 6. Submission is not confirmation

An adapter method returning “submitted” or “acknowledged” is not proof that:

- an entry filled,
- a position exists,
- or a protective stop exists.

Final truth must come from exchange-confirmed state paths such as user-stream events and reconciliation reads.

## 7. The adapter must be replaceable in tests

The codebase must support fake adapters and deterministic fixtures.

No unit test should require real Binance credentials or live network access.

## 8. Secrets stay inside the narrowest boundary

API keys, secrets, signatures, and signed payloads must remain inside the secure request/authentication boundary.

They must not leak into logs, events, test snapshots, exception messages, docs, or prompts.

---

## Adapter Position in the Architecture

The exchange adapter sits between Prometheus execution/user-stream/market-data components and Binance external APIs.

```text
strategy_engine
  -> risk_layer
    -> execution_layer
      -> exchange_adapter
        -> Binance REST / WebSocket APIs

Binance user data stream
  -> exchange_adapter stream client
    -> normalized exchange-derived events
      -> state_and_reconciliation_layer
        -> runtime state / persistence / observability
```

## Component interaction summary

| Component | May use exchange adapter? | Notes |
|---|---:|---|
| Strategy engine | No | Strategy produces intent only. |
| Risk and sizing | No direct private adapter use | May use symbol metadata through approved internal models, not raw Binance clients. |
| Execution layer | Yes | Uses adapter for order placement/cancellation/stop actions. |
| Market-data layer | Yes, public market-data side only | Through market-data stream/fetch interfaces. |
| User-stream/account layer | Yes | Uses adapter stream interfaces to normalize private events. |
| Reconciliation layer | Yes | Uses read-only state queries through controlled adapter interfaces. |
| Safety/incident layer | Indirect only | Requests actions through execution/reconciliation paths. |
| Operator interface | No direct exchange access | Must use backend-controlled commands/read models. |

---

## Recommended Code Location

The codebase structure should place exchange-specific code under:

```text
src/prometheus/exchange/
```

Recommended v1 package layout:

```text
src/prometheus/exchange/
  __init__.py
  interfaces.py
  models.py
  errors.py
  fake.py

  binance_usdm/
    __init__.py
    rest_client.py
    rest_models.py
    request_signing.py
    rate_limits.py
    error_mapping.py
    metadata.py
    orders.py
    algo_orders.py
    account.py
    user_stream.py
    market_stream.py
    normalizers.py
    websocket_routing.py
```

### Module intent

| Module | Responsibility |
|---|---|
| `interfaces.py` | Exchange-agnostic adapter protocols/interfaces. |
| `models.py` | Internal exchange-domain models used across modules. |
| `errors.py` | Internal exchange error categories. |
| `fake.py` | Fake adapter for tests and simulations. |
| `binance_usdm/rest_client.py` | Low-level HTTP wrapper, signing, request dispatch integration. |
| `binance_usdm/request_signing.py` | Isolated request signing and timestamp handling. |
| `binance_usdm/rate_limits.py` | Rate-limit tracking and backoff decisions. |
| `binance_usdm/error_mapping.py` | Binance error/HTTP response to internal error categories. |
| `binance_usdm/metadata.py` | Exchange info, leverage bracket, commission, symbol metadata. |
| `binance_usdm/orders.py` | Normal order endpoint wrappers. |
| `binance_usdm/algo_orders.py` | Algo/conditional order endpoint wrappers. |
| `binance_usdm/account.py` | Position and account read endpoint wrappers. |
| `binance_usdm/user_stream.py` | Private user-stream lifecycle and event intake. |
| `binance_usdm/market_stream.py` | Public market-data stream intake. |
| `binance_usdm/normalizers.py` | Raw payload to internal model conversion. |
| `binance_usdm/websocket_routing.py` | WebSocket base URL/category routing. |

This is a recommended structure, not a requirement to create every file in Phase 0.

Claude Code should create files incrementally as implementation phases require them.

---

## Public Interface Families

The exchange adapter should expose a small set of interface families.

## 1. Market Data Interface

Used by the market-data layer.

Responsibilities:

- subscribe to public kline streams,
- subscribe to mark-price streams,
- fetch recent standard klines by REST,
- fetch recent mark-price klines by REST where needed,
- normalize public market-data payloads,
- surface stream health and connection events.

Must not:

- place orders,
- read private account state,
- infer position/protection truth,
- or emit strategy signals.

## 2. Trading REST Interface

Used by the execution layer.

Responsibilities:

- submit normal entry orders,
- submit market exit orders,
- submit protective algo stop orders,
- cancel protective algo orders,
- cancel strategy-owned open orders where approved,
- query order status where needed,
- return normalized submission results,
- classify uncertain outcomes.

Must not:

- decide if a trade should be taken,
- decide position size,
- clear incidents,
- or mutate runtime state directly.

## 3. Account / Reconciliation Read Interface

Used by reconciliation and state-confidence flows.

Responsibilities:

- fetch current symbol position state,
- fetch open normal orders for symbol,
- fetch open algo orders for symbol,
- fetch relevant order details where needed,
- fetch exchange metadata snapshots,
- support startup and recovery reconciliation.

Must not:

- generate strategy decisions,
- place new exposure,
- or update local state without going through the state/reconciliation layer.

## 4. User Stream Interface

Used by the user-stream/account event layer.

Responsibilities:

- create or restore listen key / private stream capability,
- keep private stream alive,
- reconnect after interruption,
- consume private order/account/algo events,
- normalize private events,
- expose stream-health transitions.

Must not:

- classify reconciliation outcome by itself,
- decide that state is clean,
- or perform operator approval actions.

## 5. Metadata Interface

Used by risk/execution/research setup through controlled models.

Responsibilities:

- exchange info,
- symbol filters,
- precision rules,
- order type availability,
- leverage bracket information,
- commission rate information where available.

Must not:

- bypass risk controls,
- assume metadata is permanently static,
- or silently ignore symbol-rule changes.

---

## Binance USDⓈ-M REST Endpoint Scope

The adapter should support only endpoints needed by v1.

Implementation must verify exact endpoint paths and parameters against official Binance docs at coding time.

## Normal order endpoints

Initial v1 needs normal order support for:

- market entry order,
- market exit order if flattening or normal exit is required,
- order status query where needed,
- symbol-scoped open order queries,
- symbol-scoped cancellation where approved.

The official Binance USDⓈ-M docs currently describe new normal order submission through:

```text
POST /fapi/v1/order
```

V1 uses this for market entry and market exit orders.

## Algo order endpoints

Initial v1 needs algo order support for:

- protective STOP_MARKET order,
- protective stop cancellation,
- current open algo order query,
- possibly algo order detail query.

The official Binance USDⓈ-M docs currently describe new algo order submission through:

```text
POST /fapi/v1/algoOrder
```

The v1 protective stop design should use this algo-order path where supported.

## Account / position endpoints

Initial v1 needs:

- current position information,
- open normal orders,
- open algo orders,
- possibly account/trade/fill reads for reconciliation.

The adapter should keep these reads symbol-scoped where possible.

## Metadata endpoints

Initial v1 needs:

- exchange information,
- leverage brackets,
- commission rate information where available,
- symbol status and filters.

## Test order endpoint

The adapter may support test-order behavior for validation where Binance provides it.

However:

- test-order success is not proof that live order lifecycle is safe,
- test-order does not replace fake adapter tests,
- test-order must never use production keys casually in development.

---

## Binance WebSocket / Stream Scope

The adapter should distinguish stream categories.

## Market streams

Used for:

- BTCUSDT 15m kline updates,
- BTCUSDT 1h kline updates,
- BTCUSDT mark-price updates,
- stream connection/freshness state.

## User data streams

Used for:

- normal order lifecycle events,
- fills and partial fills,
- account/position updates,
- algo/protective stop lifecycle events.

## WebSocket routing sensitivity

Binance announced WebSocket URL architecture changes in 2026 that separate traffic by data category such as public, market, and private.

Therefore the implementation must:

- verify current WebSocket base URLs,
- route stream types to the correct endpoint category,
- avoid hardcoding legacy URLs without review,
- and include endpoint routing configuration in one adapter-owned location.

The adapter must not scatter WebSocket base URLs throughout the codebase.

---

## Request Signing Policy

## Signed request boundary

All Binance signed request behavior must be isolated inside the adapter’s request-signing boundary.

## Required fields / concepts

The adapter should handle:

- API key header placement,
- timestamp generation in UTC Unix milliseconds,
- query/body canonicalization,
- HMAC signature creation where required,
- explicit `recvWindow` policy where used,
- response status handling,
- and redaction of signed request material.

## Timestamp rule

Signed request timestamps must use canonical UTC milliseconds.

The implementation should use the project time utility rather than local timezone logic.

## recvWindow rule

If `recvWindow` is used, it must be:

- explicit,
- configurable,
- conservative,
- and documented.

## Redaction rule

The following must never appear in logs, events, exceptions, or test snapshots:

- API secret,
- raw signature,
- full live API key,
- full signed query string if it contains sensitive material,
- raw secret-bearing config,
- environment dump with secrets.

---

## Authentication and Permission Model

The adapter must respect the project’s least-privilege model.

## Runtime roles

The adapter should support logical separation between:

- trading runtime role,
- monitoring/read role,
- research/data role where applicable.

V1 may physically use fewer credentials at first, but the code should not make future separation impossible.

## Required startup validation

At startup or live enablement, the adapter/config layer should validate:

- credentials are present where required,
- environment is explicit,
- credential role matches intended runtime role,
- API authorization succeeds where safe to verify,
- no withdrawal permission is enabled for bot keys,
- production keys are IP-restricted where production live is intended,
- required trade permissions are present only for trading runtime paths.

## Failure behavior

Credential or permission failure must fail closed:

- block live trading,
- enter or remain in safe mode,
- raise operator-visible error,
- and avoid continuing in best-effort live mode.

---

## Request Discipline and Rate Limits

The adapter must centralize request discipline.

## Required behavior

The adapter should:

- track relevant Binance response headers,
- classify 429 rate-limit responses,
- back off on 429,
- treat repeated 429 failures as operational incidents,
- avoid request storms during recovery,
- avoid broad account polling when symbol-scoped queries are sufficient,
- preserve request budget for safety-critical actions.

Binance’s official general info states that 429 is returned when rate limits are violated, APIs must back off, repeated violations can lead to HTTP 418 automated IP bans, and IP rate limits are based on IPs rather than API keys.

## WebSocket rate concerns

The adapter should also respect WebSocket connection and ping/pong rate limits.

WebSocket reconnection loops must include backoff and should not hammer endpoints.

## Recovery request discipline

During restart/reconciliation, the adapter should prefer the minimum required symbol-scoped reads:

1. current BTCUSDT position,
2. current BTCUSDT open normal orders,
3. current BTCUSDT open algo orders,
4. specific order/algo-order details only if needed.

---

## Internal Models

The adapter should normalize raw exchange data into internal models.

## Suggested internal model categories

```text
ExchangeOrder
ExchangeAlgoOrder
ExchangePosition
ExchangeFill
ExchangeAccountSnapshot
ExchangeSymbolMetadata
ExchangeRateLimitState
ExchangeSubmissionResult
ExchangeError
ExchangeStreamEvent
```

## Model requirements

Internal models should include:

- source exchange,
- symbol,
- event/update timestamp where available,
- processed timestamp,
- raw exchange identifier where needed,
- client order ID / client algo ID where relevant,
- side,
- order type,
- order status,
- execution type where relevant,
- quantity fields,
- price fields,
- stop/trigger fields,
- working type where relevant,
- reduce-only / close-position flags where relevant,
- raw payload reference or redacted raw snapshot where safe.

## Raw payload retention

For debugging, it may be useful to retain raw payloads internally.

However:

- raw payloads must be redacted before logs,
- raw payloads must not contain secret material,
- raw payloads must not be treated as long-term schema contract,
- internal normalized models remain the runtime-facing interface.

---

## Order Identifier Policy

The adapter must support deterministic client identifiers.

## Normal orders

Normal order submissions should include deterministic:

```text
newClientOrderId
```

unless an approved exception exists.

## Algo orders

Algo order submissions should include deterministic:

```text
clientAlgoId
```

where supported.

## Format constraints

The adapter must validate client IDs against Binance constraints before sending.

The official Binance docs currently specify client order/algo IDs must be unique among open orders and match a constrained pattern with maximum length 36.

## Recommended ID properties

Client IDs should encode or reference:

- project/bot prefix,
- environment where safe,
- strategy identifier,
- symbol,
- order role,
- trade reference or correlation reference,
- sequence or short unique suffix.

## Do not include

Client IDs must not include:

- secrets,
- full account identifiers,
- personally sensitive data,
- overly long free-text reasons,
- or raw timestamps if they cause length issues.

## Idempotency use

Deterministic IDs support:

- detecting duplicate submissions,
- matching exchange state to local intent,
- safe recovery after unknown responses,
- and auditability.

They are not a substitute for reconciliation.

---

## Normal Entry Order Mapping

For a v1 long entry, execution should request a normal market order through the adapter.

Conceptual internal command:

```text
execution.submit_entry_order
```

Adapter-level normal order fields should map to Binance-compatible fields such as:

- `symbol=BTCUSDT`
- `side=BUY` for long entry, `SELL` for short entry
- `type=MARKET`
- `quantity`
- deterministic `newClientOrderId`
- one-way-mode position behavior, default position side where appropriate
- `newOrderRespType` policy as configured

## One-way mode

V1 assumes one-way mode.

The adapter must not introduce hedge-mode behavior unless the project explicitly approves hedge-mode support later.

## Response handling

The adapter should return a normalized submission result.

A successful HTTP response should be treated as:

- order submission accepted or acknowledged according to response,
- not final fill confirmation,
- not final position confirmation.

---

## Protective Stop Algo Order Mapping

For v1, the protective stop should be expressed as a Binance USDⓈ-M algo order where supported.

Conceptual internal command:

```text
execution.submit_protective_stop
```

Adapter-level algo fields should map to Binance-compatible fields such as:

- `algoType=CONDITIONAL`
- `symbol=BTCUSDT`
- `side=SELL` to protect a long position
- `side=BUY` to protect a short position
- `type=STOP_MARKET`
- `triggerPrice`
- `workingType=MARK_PRICE`
- `priceProtect=TRUE`
- `closePosition=true`
- deterministic `clientAlgoId`

## Quantity rule

When using `closePosition=true`, the adapter must not also send `quantity` if Binance rules forbid that combination.

## reduceOnly rule

When using `closePosition=true`, the adapter must not send `reduceOnly` if Binance rules forbid that combination.

## Position-side rule

V1 is one-way mode, so the adapter should not send hedge-mode-only position-side behavior.

## Confirmation rule

A successful protective stop submission response is not enough to declare protection confirmed.

Protection is confirmed only after exchange-state evidence supports it through:

- user-stream algo update,
- open algo order query,
- or reconciliation path defined elsewhere.

---

## Stop Replacement Mapping

V1 stop updates use cancel-and-replace.

Conceptual command:

```text
execution.replace_protective_stop
```

Recommended sequence:

1. Verify current position still exists through state/reconciliation context.
2. Identify current active protective stop.
3. Cancel current protective stop through adapter.
4. Confirm cancellation through exchange-derived state or query.
5. Submit replacement protective stop.
6. Confirm replacement exists.
7. Emit normalized events and allow state layer to update.

## Adapter responsibility

The adapter may expose cancel and submit operations.

It should not unilaterally decide that the replacement workflow is safe to continue if confirmation is missing.

## Safety rule

If cancel succeeds but replacement cannot be confirmed, the runtime must treat protection as uncertain or emergency depending on context.

The adapter should surface uncertainty clearly.

---

## Exit and Emergency Flatten Mapping

The adapter may support market exit orders.

Conceptual commands:

```text
execution.submit_exit_order
execution.emergency_flatten
```

For v1, emergency flattening must be routed through controlled execution/safety paths.

The adapter should provide the technical ability to submit a flattening order, but it must not decide when flattening is required.

## Flattening caution

Flattening should account for:

- current exchange-confirmed position side,
- current position quantity,
- one-way mode,
- existing protective stops,
- possible stale local state,
- and unknown order outcomes.

If position quantity or side cannot be trusted, the reconciliation/safety layer must determine the safest next step before the adapter sends a flattening order.

---

## User Stream Adapter Design

The user-stream adapter handles Binance private event intake.

## Responsibilities

- obtain or restore listen key / private stream setup where required,
- maintain keepalive,
- connect to correct private WebSocket endpoint,
- reconnect on interruption,
- classify stream health,
- normalize private events,
- emit internal exchange-derived events.

## Required normalized event categories

The adapter should support normalized equivalents of:

- order update received,
- account update received,
- algo update received,
- user stream connected,
- user stream disconnected,
- user stream stale,
- user stream restored,
- listen key keepalive succeeded,
- listen key keepalive failed.

## Event types relevant to v1

The order-handling notes identify these key private event types:

- `ORDER_TRADE_UPDATE`
- `ACCOUNT_UPDATE`
- `ALGO_UPDATE`

The adapter should normalize these into internal models before state/reconciliation consumes them.

## User stream is primary live source

During normal operation, user-stream events are the primary live source for order, position, and account changes.

However, stream events still pass through state/reconciliation logic; the adapter itself does not declare the whole runtime clean.

---

## Market Stream Adapter Design

Market stream adapter behavior is primarily defined in the live data spec.

The exchange adapter should provide Binance-specific market stream connectivity and payload normalization.

## Responsibilities

- connect to kline streams,
- connect to mark-price stream,
- normalize public stream messages,
- expose connection health,
- route payloads to market-data layer.

## Boundary rule

Market stream adapter must not:

- place orders,
- confirm positions,
- confirm protective stops,
- or emit execution truth.

---

## Exchange Metadata Adapter Design

The metadata adapter should provide normalized symbol and account/exchange metadata.

## Required metadata

For v1 research/runtime alignment:

- exchange info,
- symbol filters,
- price precision,
- quantity precision,
- minimum quantity,
- notional constraints where available,
- trigger protection thresholds where available,
- allowed order types,
- leverage brackets,
- commission rates where available.

## Metadata usage

Risk and execution layers use metadata for:

- tradability checks,
- quantity rounding,
- trigger price validation,
- leverage cap validation,
- notional and filter compliance.

## Snapshot policy

Metadata used for research or validation should be snapshot/version-aware.

Runtime metadata should be refreshed under controlled rules and should not silently alter behavior mid-trade without logging.

---

## Error and Exception Model

The adapter must map external errors into internal categories.

## Suggested error categories

```text
ExchangeErrorCategory:
  AUTHENTICATION_FAILED
  PERMISSION_DENIED
  IP_RESTRICTED
  RATE_LIMITED
  IP_BANNED
  INVALID_REQUEST
  SYMBOL_RULE_VIOLATION
  INSUFFICIENT_MARGIN
  ORDER_REJECTED
  ORDER_NOT_FOUND
  UNKNOWN_ORDER_STATE
  NETWORK_TIMEOUT
  NETWORK_UNAVAILABLE
  SERVICE_UNAVAILABLE
  RESPONSE_PARSE_ERROR
  STREAM_DISCONNECTED
  STREAM_STALE
  LISTEN_KEY_EXPIRED
  UNKNOWN
```

## Unknown execution status

Unknown execution status is safety-critical.

It may occur when:

- request times out after reaching exchange,
- response is malformed,
- network breaks after submission,
- exchange returns ambiguous error,
- stream confirmation is delayed,
- or order query cannot determine outcome.

When unknown status affects exposure or protection, the adapter must surface:

```text
execution_uncertainty_detected
```

or equivalent internal event/return state.

The runtime should then enter safe/recovery behavior according to incident and restart procedures.

## Retry policy

The adapter must not blindly retry trade-affecting requests when outcome is unknown.

Before retrying an order or cancellation, the system should query exchange state using deterministic client IDs and reconciliation rules.

## Safe retry examples

Potentially safe retries may include:

- idempotent read requests,
- stream reconnects with backoff,
- REST metadata fetch retry,
- account/order queries after timeout.

Potentially unsafe retries include:

- re-submitting entry orders after unknown status,
- re-submitting protective stop without checking existing stop,
- repeated cancel/replace without state confirmation.

---

## Acknowledgement and Confirmation Semantics

The adapter must preserve the distinction between:

| Term | Meaning |
|---|---|
| Submitted | Local request was sent or attempted. |
| Acknowledged | Exchange returned a response indicating request acceptance/acknowledgement. |
| Filled | Exchange/user-stream evidence confirms execution. |
| Position confirmed | Exchange state confirms position exists. |
| Stop submitted | Protective stop request was sent or acknowledged. |
| Stop confirmed | Exchange state confirms protective stop exists. |
| Reconciled clean | State/reconciliation layer confirms local and exchange state alignment. |

## Critical rules

- Submitted entry does not mean filled.
- Acknowledged entry does not mean position exists.
- Submitted stop does not mean position is protected.
- Acknowledged stop does not mean protection is confirmed.
- Adapter success does not mean runtime can resume from safe mode.
- Only state/reconciliation can classify clean/recoverable/unsafe state.

---

## Observability Requirements

The adapter must emit or support structured observability for exchange interactions.

## Required exchange events

Recommended event categories:

- `exchange.rest_request_started`
- `exchange.rest_request_completed`
- `exchange.rest_request_failed`
- `exchange.rate_limit_state_updated`
- `exchange.order_submission_started`
- `exchange.order_submission_acknowledged`
- `exchange.algo_submission_acknowledged`
- `exchange.order_rejected`
- `exchange.unknown_execution_status`
- `exchange.user_stream_connected`
- `exchange.user_stream_disconnected`
- `exchange.user_stream_stale`
- `exchange.user_stream_restored`
- `exchange.private_event_received`
- `exchange.payload_normalization_failed`

## Required event fields

Where relevant:

- exchange name,
- endpoint role,
- symbol,
- request role,
- client order ID,
- client algo ID,
- exchange order ID,
- exchange algo ID,
- HTTP status,
- error category,
- rate-limit header summary,
- event time,
- processing time,
- correlation ID,
- causation ID,
- redaction status.

## Forbidden event fields

Events must not include:

- API secret,
- full live API key,
- raw signature,
- unredacted signed payload,
- full secret-bearing config,
- sensitive environment dump.

---

## Adapter State

The adapter may maintain limited operational state.

## Allowed adapter-local state

- current REST base URL,
- current WebSocket endpoint routing,
- current rate-limit counters,
- stream connection status,
- listen key metadata,
- recent request IDs,
- health state,
- circuit breaker / backoff state.

## Not adapter-owned state

The adapter must not own final authoritative business state such as:

- current trade lifecycle,
- risk stage,
- protection state,
- reconciliation result,
- incident lifecycle,
- operator approval state,
- current account truth beyond normalized latest reads.

Those belong to state, reconciliation, safety, and persistence layers.

---

## Configuration Requirements

The adapter should be configured through typed configuration.

## Required config categories

- environment: dev / validation / paper / shadow / production
- Binance REST base URL
- Binance market WebSocket base URL
- Binance private WebSocket base URL
- request timeout
- recvWindow if used
- retry/backoff policy
- rate-limit policy
- allowed symbol list
- live trading enabled flag
- testnet/paper mode flag where applicable
- credential role references
- redaction policy enabled flag

## Live trading enablement

The adapter must not enable live trade actions merely because credentials exist.

Live trade actions require explicit runtime/live enablement gates outside the adapter as well.

## Environment safety

Default configuration should be safe.

Development defaults must not point to live production trading with real credentials.

---

## Library Selection Policy

The project may use:

- direct HTTP/WebSocket implementation,
- an official Binance connector,
- or a thin wrapper around a selected library,

but the selected approach must still preserve the Prometheus adapter boundary.

## If using an external library

The implementation must:

- wrap it behind Prometheus interfaces,
- avoid leaking library-specific models into strategy/risk/state code,
- centralize signing and redaction review,
- test normalization,
- and pin/version dependencies deliberately.

## If using direct HTTP/WebSocket

The implementation must:

- implement request signing carefully,
- implement rate-limit handling,
- implement reconnect/backoff discipline,
- test error mapping,
- and keep endpoint paths centralized.

## Recommendation

For v1, prefer clarity and testability over clever abstraction.

A thin internal adapter over a well-understood client is acceptable if it does not compromise boundary rules.

---

## Fake Adapter Requirements

A fake adapter is mandatory for testing.

## Fake adapter should support

- successful market entry submission,
- rejected market entry submission,
- unknown entry submission status,
- protective stop submission success,
- protective stop rejection,
- stop cancellation success,
- stop cancellation failure,
- stop replacement partial failure,
- position exists / no position reads,
- open normal order reads,
- open algo order reads,
- user-stream order update fixtures,
- account update fixtures,
- algo update fixtures,
- rate-limit simulation,
- stream disconnect/stale simulation.

## Fake adapter must not

- require real credentials,
- call live Binance endpoints,
- hide nondeterministic behavior,
- or return raw Binance payloads without normalization tests.

---

## Testing Requirements

## Unit tests

Required for:

- request signing redaction,
- client order ID validation,
- response normalization,
- error mapping,
- rate-limit state update,
- symbol metadata parsing,
- endpoint routing config.

## Contract tests

Required for:

- adapter interface behavior,
- fake adapter parity with real adapter models,
- command-to-adapter mapping,
- normalized event schemas.

## Integration tests with fake adapter

Required for:

- entry command to order submission event,
- protective stop command to algo submission event,
- cancel-and-replace workflow,
- unknown execution status recovery trigger,
- user-stream event to normalized exchange-derived event,
- reconciliation reads from fake exchange state.

## Live/sandbox tests

Optional and later-stage only.

Must require explicit opt-in and must never run by default in CI.

## No real credentials in tests

No test fixture may contain real API keys, secrets, signatures, account IDs, or live order IDs that expose sensitive account context.

---

## Implementation Phasing

## Phase A — Interfaces and fake adapter

Create:

- exchange interfaces,
- internal exchange models,
- fake adapter,
- error categories,
- tests.

No live Binance access yet.

## Phase B — Public market-data adapter skeleton

Create:

- market stream wrappers,
- kline/mark-price normalization,
- REST kline fetch wrappers,
- endpoint routing config,
- tests with fixtures.

No live orders.

## Phase C — Metadata/read-only REST adapter

Create:

- exchange info fetch,
- leverage bracket fetch,
- commission rate fetch where approved,
- position read interface,
- open order read interface,
- open algo order read interface,
- tests with fixtures.

No live orders by default.

## Phase D — User-stream adapter

Create:

- listen key lifecycle,
- private stream connection,
- keepalive,
- event normalization,
- stream health,
- tests with fixtures.

Still no automatic live trading.

## Phase E — Trade action adapter

Create:

- normal order submission wrapper,
- algo stop order submission wrapper,
- cancellation wrappers,
- response normalization,
- unknown status classification,
- tests with fake adapter and static payloads.

Requires safety foundations to already exist.

## Phase F — Paper/shadow/live gate integration

Only after prior phases are tested:

- integrate with execution layer,
- enforce live enablement gates,
- verify operator visibility,
- validate restart/reconciliation behavior,
- rehearse in paper/shadow before real capital.

---

## V1 Non-Goals

The v1 exchange adapter should not implement:

- multi-venue routing,
- hedge-mode trading,
- portfolio-margin logic,
- multi-symbol live orchestration,
- options or coin-margined futures,
- smart order routing,
- iceberg/slicing execution,
- latency-sensitive market making,
- full order book execution optimization,
- autonomous exchange failover,
- discretionary manual trading terminal behavior,
- native exchange trailing stop as the primary strategy trailing logic,
- WebSocket API trading as the primary order path unless explicitly approved.

---

## Open Questions

The following should be resolved before live-capable order placement is enabled.

## 1. Exact client order ID format

The adapter requires deterministic IDs, but the exact compact format should be standardized.

## 2. ACK versus RESULT response policy

Binance supports different response types for orders.

V1 should decide whether to use `ACK` or `RESULT` for normal and algo orders, while preserving the rule that user-stream/reconciliation remains authoritative.

## 3. Missing confirmation timeout

The project needs concrete timeouts for:

- missing entry confirmation,
- missing position confirmation,
- missing protective stop confirmation,
- missing cancel confirmation,
- missing replacement stop confirmation.

## 4. Official connector versus direct HTTP

The implementation should decide whether to use an official connector or direct HTTP/WebSocket wrappers.

## 5. Testnet versus dry-run design

Paper/shadow mode should define whether it uses Binance testnet, fake adapter, dry-run simulation, or multiple modes.

## 6. Exact rate-limit/circuit-breaker thresholds

The adapter must back off and protect recovery budget, but exact thresholds need implementation tuning.

## 7. WebSocket endpoint migration handling

Current Binance WebSocket architecture has recent migration considerations.

The implementation must verify current endpoint routing before live use.

---

## Acceptance Criteria

This exchange-adapter design is satisfied when the implementation can demonstrate:

- strategy code does not import Binance clients,
- risk code does not place orders,
- execution uses adapter interfaces,
- REST signing and credentials are isolated,
- secrets and signatures are redacted,
- normal and algo order paths are separated,
- protective stop mapping supports `STOP_MARKET`, `closePosition=true`, `MARK_PRICE`, and `priceProtect=TRUE`,
- order submission is distinct from fill/position confirmation,
- stop submission is distinct from stop/protection confirmation,
- user-stream events are normalized before entering state/reconciliation,
- REST reconciliation reads are symbol-scoped where practical,
- unknown execution status is surfaced explicitly,
- rate-limit responses trigger backoff rather than request spam,
- fake adapter tests can exercise success, rejection, and unknown-status paths,
- no live credentials are required for unit tests,
- and live order placement cannot occur without explicit live enablement and runtime safety gates.

---

## References

Official Binance references to verify during implementation:

- Binance USDⓈ-M Futures General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info

- Binance USDⓈ-M Futures New Order REST API  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api

- Binance USDⓈ-M Futures New Algo Order REST API  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/New-Algo-Order

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams

- Binance USDⓈ-M Futures WebSocket API General Info  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-api-general-info

- Binance Derivatives Change Log  
  https://developers.binance.com/docs/derivatives/change-log

Implementation must verify these references at coding time because exchange APIs and endpoint routing may change.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Exchange adapter implementation boundary
