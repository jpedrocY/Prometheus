# Binance Futures Mechanics

## Purpose
Capture the main exchange mechanics that matter for initial system design.

## Scope
This document focuses on system-relevant behavior rather than exhaustive exchange documentation.

## Background
A futures bot is not just “a strategy plus API calls.” Exchange rules, session limits, position modes, user streams, and order behavior shape the architecture.

## Definitions
- **USDⓈ-M futures**: Binance futures contracts margined in stablecoin-like quote assets such as USDT.
- **User data stream**: exchange stream carrying account/order/position events.
- **Listen key**: token used to maintain user data stream sessions.

## Main Framework / Design / Rules

### Current Primary Target
- Binance USDⓈ-M futures

### Mechanics That Matter Early
- position mode affects order semantics
- margin mode affects risk isolation
- leverage interacts with notional brackets
- user data streams are essential for live state
- reconnect and renewal behavior must be part of the runtime design
- order intent and actual exchange state must be reconciled continuously

### Design Implications
- the engine must track authoritative order/position state
- the engine must support reconnect-safe recovery
- REST should not be treated as the only live truth source
- symbol metadata and exchange rules must be cached and refreshed deliberately

## Assumptions
- The first implementation will deliberately constrain features to simplify correctness.

## Risks and Failure Modes
- stale listen key management
- assuming fills from intent
- failing to reflect exchange-specific restrictions in the execution model

## Open Questions
- What exact order-type subset should v1 allow?
- What reconciliation cadence should be used after restarts?

## Decisions
- Binance futures mechanics will shape the initial engine design directly.
- Exchange-specific reality takes priority over generic abstraction elegance.

## Next Steps
- define order lifecycle
- define position state model
- define user stream reconciliation approach

## References
- `futures-vs-spot.md`
- `../06-execution-exchange/binance-usdm-order-model.md`
- `../06-execution-exchange/user-stream-reconciliation.md`
