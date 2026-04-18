# Position State Model

## Purpose

This document defines the exchange-specific position-state model for the v1 Prometheus trading system.

Its purpose is to make explicit how Binance USDⓈ-M futures position facts are normalized into Prometheus internal position facts, and how those normalized facts map into existing runtime state, exposure, protection, reconciliation, and operator-review behavior.

This document exists because the phrase “position state” is dangerous if it is left informal.

In v1, Prometheus must distinguish clearly between:

- no exchange position,
- a clean flat symbol state,
- a strategy-owned long or short position,
- a position that exists but is not yet confirmed protected,
- manual or non-bot exposure,
- hedge-mode or cross-margin state that violates v1 assumptions,
- and unknown or mismatched position state.

This document replaces the previous TBD placeholder for:

```text
docs/06-execution-exchange/position-state-model.md
```

---

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures
- first live symbol: BTCUSDT perpetual
- first secondary research comparison: ETHUSDT perpetual
- v1 live symbol scope: BTCUSDT only
- position mode: one-way mode
- margin mode: isolated margin
- max live positions: one
- max active protective stop: one
- no pyramiding in v1
- no reversal entry while positioned in v1
- entry order: normal `MARKET` order
- protective stop: algo / conditional `STOP_MARKET` order
- protective stop uses:
  - `closePosition=true`
  - `workingType=MARK_PRICE`
  - `priceProtect=TRUE`
- user stream is the primary live private-state source
- REST is used for placement, cancellation, reconciliation, and recovery
- restart begins in safe mode
- exchange state is authoritative
- v1 is supervised, not lights-out autonomous

This document covers:

- Binance position fact sources,
- REST position snapshots,
- `ACCOUNT_UPDATE` position events,
- one-way position-side semantics,
- margin-mode interpretation,
- signed position-size interpretation,
- normalized Prometheus position facts,
- position ownership classification,
- clean flat classification,
- strategy-position classification,
- external/manual exposure classification,
- position/protection state separation,
- mapping to runtime, exposure, reconciliation, and incident behavior,
- persistence requirements,
- observability requirements,
- and testing requirements.

This document does **not** define:

- the full runtime state machine,
- the full user-stream reconciliation algorithm,
- final Binance API wrapper implementation,
- final database schema,
- order-placement mechanics,
- protective-stop placement mechanics,
- position-sizing formula,
- operator dashboard layout,
- or manual-control workflows.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/binance-usdm-order-model.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/06-execution-exchange/user-stream-reconciliation.md`
- `docs/06-execution-exchange/failure-recovery.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/kill-switches.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/operator-workflow.md`
- `docs/11-interface/operator-dashboard-requirements.md`

### Authority hierarchy

If this document conflicts with the state model on runtime modes, trade lifecycle states, or protection states, the state model wins.

If this document conflicts with user-stream reconciliation on reconciliation sequencing, user-stream reconciliation wins.

If this document conflicts with exposure limits on whether new exposure is allowed, exposure limits win.

If this document conflicts with stop-loss policy on unprotected-position handling, stop-loss policy wins.

If this document conflicts with incident response on severity and escalation, incident response wins.

If this document conflicts with official Binance API behavior, implementation must stop, verify current Binance documentation, and update the affected document before live use.

---

## Core Principles

## 1. Position facts are exchange-derived facts

Prometheus does not invent live position truth from local intent.

A strategy signal, entry command, order submission, or local trade record is not proof that a position exists.

Live position truth must come from exchange-derived evidence such as:

- user-stream `ACCOUNT_UPDATE` events,
- order/fill events interpreted through reconciliation,
- REST position snapshots,
- and restart/recovery reconciliation results.

## 2. Exchange symbol position is not the same as clean flat

A symbol can have zero position size while still being operationally unsafe for new entries.

Examples:

- an entry order is in flight,
- a prior entry outcome is unknown,
- a stale open entry order exists,
- a stale protective stop exists,
- a manual open order exists,
- reconciliation has not completed,
- or local/exchange state mismatch remains unresolved.

Therefore, Prometheus must distinguish:

```text
exchange_symbol_position_flat
```

from:

```text
prometheus_clean_flat
```

## 3. Position existence is separate from protection

A confirmed position is not automatically a safe live trade.

The runtime must separately track:

- whether a position exists,
- whether Prometheus owns or recognizes the position,
- whether protective stop coverage is confirmed,
- and whether the protection matches expected side, symbol, and trade reference.

In v1:

```text
position exists != position protected
```

A live position without confirmed protective stop coverage is an emergency condition.

## 4. One-way mode is mandatory in v1

Prometheus v1 expects one-way position semantics.

The expected Binance position-side representation for v1 is:

```text
positionSide = BOTH
```

If hedge-mode position semantics are detected in a live path, Prometheus must block live trading until the mismatch is resolved.

## 5. Isolated margin is mandatory in v1

Prometheus v1 requires isolated margin for BTCUSDT live operation.

If Binance state indicates cross margin, unknown margin type, or ambiguous margin mode while live trading is being considered, Prometheus must fail closed.

## 6. Signed size determines exchange-side direction

For one-way BTCUSDT position state:

```text
positionAmt > 0  -> long position
positionAmt < 0  -> short position
positionAmt == 0 -> no exchange symbol position
```

Prometheus should retain both signed and absolute size in normalized position facts.

## 7. Manual or non-bot exposure blocks entries

Any open position or open order that cannot be classified as Prometheus-owned must block new entries.

Prometheus is not a discretionary account manager in v1.

It should not silently adopt, average, reverse, hedge, or manage manual exposure as if it were a normal strategy trade.

## 8. Unknown position state fails closed

If Prometheus cannot determine position side, size, ownership, margin mode, or protection state with sufficient confidence, new entries must remain blocked.

---

## Binance Position Fact Sources

Prometheus uses multiple exchange-derived sources to determine position state.

No single source should be treated as sufficient for every situation.

## 1. REST position snapshot

The REST position information endpoint provides a snapshot of current Binance position state.

The implementation must verify the current official endpoint and response fields at coding time.

At the time this document is written, Binance USDⓈ-M futures documents position information through:

```text
GET /fapi/v3/positionRisk
```

The implementation should use symbol-scoped reads where possible.

### Role in Prometheus

REST position snapshots are used for:

- startup reconciliation,
- restart recovery,
- resolving user-stream gaps,
- checking current exposure after unknown execution outcomes,
- confirming flat or positioned state during recovery,
- and verifying position state when stream confidence is degraded.

### Important limitation

A REST snapshot is a point-in-time read.

It should not replace the user stream during normal live operation.

The live private event path remains necessary for timely order/account/protection updates.

## 2. `ACCOUNT_UPDATE` user-stream events

`ACCOUNT_UPDATE` events provide account and position changes through the private user data stream.

### Role in Prometheus

`ACCOUNT_UPDATE` events are used for:

- position-size changes,
- position-side updates,
- balance/margin effects,
- realized/unrealized PnL updates where available,
- and confirming position updates after fills, exits, stop triggers, funding, or margin changes.

### Important limitation

An `ACCOUNT_UPDATE` event is a change event, not necessarily a full account snapshot.

Absence of a symbol from one event must not be interpreted as proof that the symbol is flat.

A REST read is required when the bot needs a full authoritative snapshot after restart, stream gap, or uncertainty.

## 3. `ORDER_TRADE_UPDATE` as position context

`ORDER_TRADE_UPDATE` is not itself the final position model, but it provides fill evidence and order lifecycle context.

Examples:

- entry fill evidence,
- partial fill evidence,
- exit fill evidence,
- emergency flatten fill evidence,
- stop-trigger-related order lifecycle evidence where applicable.

A fill update can suggest that a position may exist or may have changed, but position state should still be confirmed through account/position state.

## 4. `ALGO_UPDATE` and open algo orders as protection context

Algo order state is not the position itself.

However, protection state cannot be classified without knowing whether an appropriate active protective stop exists.

Prometheus therefore evaluates position state together with:

- open normal orders,
- open algo orders,
- user-stream algo updates,
- and locally persisted stop/trade references.

## 5. Local persisted state as provisional context

Local persisted state is not exchange truth.

It is used to answer questions such as:

- what trade did Prometheus believe was active,
- what client order IDs were generated,
- what trade reference was assigned,
- what stop was expected,
- what lifecycle state existed before restart,
- and whether a mismatch is explainable.

During reconciliation, persisted local state is context, not authority.

---

## Required Binance Position Fields

The adapter should normalize position information from Binance into internal fields.

The exact raw field names may differ by endpoint or stream event, but the normalized model should preserve the following concepts where available.

## Required position identity fields

- `exchange`
- `symbol`
- `position_side_raw`
- `position_side_normalized`
- `source`
- `event_time_utc_ms` where available
- `snapshot_time_utc_ms` where applicable
- `processed_at_utc_ms`

## Required size and direction fields

- `signed_position_size`
- `absolute_position_size`
- `position_direction`
- `position_is_flat`

## Required price and PnL fields

- `entry_price`
- `break_even_price` where available
- `mark_price` where available
- `unrealized_pnl_usdt` where available
- `realized_pnl_component_usdt` where available from event context

## Required margin and risk fields

- `margin_type`
- `isolated_margin` where available
- `isolated_wallet` where available
- `notional_usdt` where available or derivable
- `liquidation_price` where available
- `leverage` where available

## Required confidence and ownership fields

- `position_fact_confidence`
- `ownership_classification`
- `matched_trade_reference` where known
- `matched_client_order_id` where known
- `last_reconciled_at_utc_ms` where applicable
- `raw_payload_reference` or sanitized raw event hash where available

---

## Normalized Position Fact Model

Prometheus should normalize raw Binance position data into a stable internal model before state logic consumes it.

Recommended internal model:

```text
NormalizedPositionFact
  exchange
  symbol
  position_side_raw
  position_side_normalized
  margin_type_raw
  margin_type_normalized
  signed_position_size
  absolute_position_size
  position_direction
  position_is_flat
  entry_price
  break_even_price
  mark_price
  notional_usdt
  unrealized_pnl_usdt
  liquidation_price
  leverage
  isolated_margin
  isolated_wallet
  source
  event_time_utc_ms
  snapshot_time_utc_ms
  processed_at_utc_ms
  position_fact_confidence
  ownership_classification
  matched_trade_reference
  matched_order_reference
  notes
```

## Position-side enum

Recommended normalized enum:

```text
POSITION_SIDE_BOTH
POSITION_SIDE_LONG
POSITION_SIDE_SHORT
POSITION_SIDE_UNKNOWN
```

For v1 live operation, acceptable normal state is:

```text
POSITION_SIDE_BOTH
```

The values `POSITION_SIDE_LONG` and `POSITION_SIDE_SHORT` indicate hedge-mode semantics and are not accepted for v1 live trading.

## Position-direction enum

Recommended normalized enum:

```text
FLAT
LONG
SHORT
UNKNOWN
```

Direction is derived from signed size under one-way semantics.

## Margin-type enum

Recommended normalized enum:

```text
ISOLATED
CROSSED
UNKNOWN
```

For v1 live operation, acceptable normal state is:

```text
ISOLATED
```

## Confidence enum

Recommended normalized enum:

```text
HIGH
MEDIUM
LOW
UNKNOWN
```

### `HIGH`

Meaning:

- source is trusted,
- fields are parseable,
- timestamp is acceptable,
- position side is compatible with v1,
- margin mode is known,
- and reconciliation context is acceptable.

### `MEDIUM`

Meaning:

- data is likely usable for diagnostics,
- but a full trading decision should still wait for reconciliation or additional evidence.

### `LOW`

Meaning:

- source is stale, partial, or conflicts with another state source.

### `UNKNOWN`

Meaning:

- position fact cannot safely support decisions.

Trading gates must treat `LOW` or `UNKNOWN` confidence as blocking when position state matters.

---

## Numeric Sign Policy

## Core rule

Prometheus must preserve Binance signed position amount semantics.

For one-way position mode:

```text
positionAmt > 0  -> LONG
positionAmt < 0  -> SHORT
positionAmt == 0 -> FLAT
```

## Signed and absolute quantities

Prometheus should store both:

```text
signed_position_size
absolute_position_size
```

### Why both are required

` signed_position_size ` is useful for:

- exchange parity,
- direction checks,
- mismatch detection,
- and debugging.

` absolute_position_size ` is useful for:

- risk calculations,
- notional checks,
- UI display,
- protection matching,
- and exposure summaries.

## Decimal safety

Position quantities, prices, trigger prices, margin values, and notional values should be parsed using decimal-safe handling in execution/risk/state code.

Floating point may be acceptable for analytical summaries, but it should not be the source of truth for exchange-facing position comparisons.

## Zero threshold

The implementation should define a strict zero policy based on exchange quantity precision and symbol step size.

Recommended rule:

```text
position is flat only when the exchange-reported signed position amount is exactly zero
or has been normalized to zero according to explicit exchange precision rules.
```

The bot must not casually treat a small non-zero amount as flat without a documented dust/precision policy.

---

## Timestamp Policy for Position Facts

Position facts should retain both event time and processing time where possible.

## Event time

Event time is the timestamp supplied by Binance or the source event.

Examples:

- account update event time,
- position update time,
- order update event time.

## Snapshot time

Snapshot time is the time associated with a REST snapshot request/response.

It should represent when Prometheus obtained the snapshot, and where possible the exchange update time carried in the response should also be retained.

## Processing time

Processing time is when Prometheus received, normalized, and stored the fact.

## Required rule

Prometheus must not compare stale position facts against fresh order/protection facts as if they were simultaneous.

Where state matters, reconciliation must use a coherent snapshot or explicit event-ordering logic.

---

## One-Way Mode Model

## Expected v1 behavior

Prometheus v1 is designed for Binance one-way mode.

Expected raw position-side behavior:

```text
positionSide = BOTH
```

## Allowed v1 states

| Raw / normalized condition | V1 live implication |
|---|---|
| `positionSide=BOTH`, `positionAmt=0` | acceptable exchange-symbol flat fact |
| `positionSide=BOTH`, `positionAmt>0` | possible long position |
| `positionSide=BOTH`, `positionAmt<0` | possible short position |
| `positionSide=LONG` | hedge-mode behavior detected; block live trading |
| `positionSide=SHORT` | hedge-mode behavior detected; block live trading |
| missing position-side field where required | unknown; fail closed |

## Hedge-mode detection

If hedge-mode semantics are detected:

```text
entries_blocked = true
operator_review_required = true
reconciliation_required = true
```

The runtime should not attempt to reinterpret hedge-mode positions into one-way v1 behavior.

## Account mode correction

If account or symbol mode is wrong, the operator must correct account configuration outside the normal strategy path.

Prometheus should not automatically switch position mode during active or ambiguous exposure.

---

## Margin Mode Model

## Expected v1 behavior

Prometheus v1 requires isolated margin for BTCUSDT live trading.

Expected normalized margin type:

```text
ISOLATED
```

## Margin-mode behavior

| Margin condition | V1 live implication |
|---|---|
| `ISOLATED` and otherwise clean | acceptable |
| `CROSSED` while flat | block live entries until corrected |
| `CROSSED` while positioned | unsafe mismatch / operator review |
| `UNKNOWN` while live path matters | fail closed |
| margin mode changed unexpectedly | incident/reconciliation required |

## Cross margin detection

If cross margin is detected for BTCUSDT in v1 live context:

```text
entries_blocked = true
operator_review_required = true
```

If a position exists under cross margin:

```text
reconciliation_required = true
incident review required
```

Severity depends on whether protection exists and whether the position is strategy-owned.

---

## Flat / Long / Short Classification

## Exchange-symbol classification

Prometheus should classify the exchange symbol position as:

```text
EXCHANGE_SYMBOL_FLAT
EXCHANGE_SYMBOL_LONG
EXCHANGE_SYMBOL_SHORT
EXCHANGE_SYMBOL_UNKNOWN
```

### `EXCHANGE_SYMBOL_FLAT`

Required facts:

- symbol matches v1 symbol,
- position side is compatible with v1,
- signed position size is zero,
- position fact confidence is sufficient.

This means only that the exchange position amount is flat.

It does **not** by itself mean Prometheus may trade.

### `EXCHANGE_SYMBOL_LONG`

Required facts:

- symbol matches v1 symbol,
- position side is compatible with v1,
- signed position size is greater than zero,
- position fact confidence is sufficient.

### `EXCHANGE_SYMBOL_SHORT`

Required facts:

- symbol matches v1 symbol,
- position side is compatible with v1,
- signed position size is less than zero,
- position fact confidence is sufficient.

### `EXCHANGE_SYMBOL_UNKNOWN`

Use when:

- position amount cannot be parsed,
- position side is incompatible or missing,
- source is stale,
- source conflicts with other state,
- required timestamp confidence is missing,
- or the snapshot/event is otherwise not trustworthy.

## Prometheus operational classification

Prometheus should separately classify operational position state as:

```text
PROMETHEUS_CLEAN_FLAT
PROMETHEUS_STRATEGY_POSITION
PROMETHEUS_POSITION_UNCONFIRMED
PROMETHEUS_EXTERNAL_EXPOSURE
PROMETHEUS_POSITION_MISMATCH
PROMETHEUS_POSITION_UNKNOWN
```

These operational classifications use position facts plus open orders, algo orders, local lineage, reconciliation state, and protection state.

---

## Clean Flat Definition

A clean flat state is stricter than exchange position amount being zero.

## Required conditions for clean flat

Prometheus may classify the symbol as clean flat only when all of the following are true:

- exchange position for BTCUSDT is flat,
- no strategy-owned entry order is in flight,
- no strategy-owned entry order has unknown outcome,
- no open normal order exists that could create or close exposure unexpectedly,
- no open manual or external normal order exists for the symbol,
- no active protective stop remains for a nonexistent position,
- no unknown or orphaned algo order exists for the symbol,
- local active trade state is flat or safely reconciled to flat,
- reconciliation state is clean or acceptable,
- user-stream health is acceptable for normal operation,
- required REST reconciliation has completed when needed,
- no active incident, kill switch, daily lockout, drawdown pause, or operator pause blocks entries.

## Clean flat output

When clean flat is confirmed:

```text
exchange_symbol_position_state = EXCHANGE_SYMBOL_FLAT
operational_position_state = PROMETHEUS_CLEAN_FLAT
protection_state = NO_PROTECTION_REQUIRED
entries_may_be_allowed = depends_on_other_gates
```

Clean flat does not automatically mean a trade must be taken.

It means position state does not block a trade if all other gates approve.

---

## Position Ownership Classification

When a position exists, Prometheus must classify ownership before allowing normal management or resumption.

Recommended ownership classes:

```text
NO_POSITION
STRATEGY_OWNED
POSSIBLE_STRATEGY_OWNED
EXTERNAL_OR_MANUAL
UNKNOWN_OWNERSHIP
```

## `NO_POSITION`

Meaning:

- exchange position size is zero,
- no position ownership decision is required.

This does not by itself imply clean flat.

## `STRATEGY_OWNED`

Meaning:

- position can be matched to a Prometheus trade lifecycle with high confidence.

Acceptable evidence may include:

- matching symbol,
- matching side,
- matching signed or absolute size within approved precision,
- known trade reference,
- deterministic client-order ID lineage,
- known fill event chain,
- persisted active trade record,
- reconciliation result,
- and expected timing relative to entry/exit actions.

## `POSSIBLE_STRATEGY_OWNED`

Meaning:

- position plausibly belongs to Prometheus,
- but one or more required ownership proofs are incomplete.

Behavior:

```text
entries_blocked = true
reconciliation_required = true
normal strategy progression blocked
```

Prometheus may continue safety actions, such as protection verification or emergency containment, but should not treat the state as fully normal.

## `EXTERNAL_OR_MANUAL`

Meaning:

- position exists and cannot be linked to Prometheus,
- or evidence indicates it was created outside Prometheus control.

Examples:

- no matching client order lineage,
- no matching local trade reference,
- size/side conflicts with expected strategy state,
- symbol is not approved live symbol,
- timing is incompatible with Prometheus actions,
- operator manually opened a futures position,
- another bot or tool created exposure.

Behavior:

```text
entries_blocked = true
operator_review_required = true
reconciliation_required = true
```

Prometheus must not open additional strategy exposure.

## `UNKNOWN_OWNERSHIP`

Meaning:

- position ownership cannot be determined from available evidence.

Behavior:

```text
entries_blocked = true
operator_review_required = true
incident or recovery classification required
```

If protection is also uncertain, emergency policy applies.

---

## Strategy-Owned Position Requirements

A live position should be considered strategy-owned only when it satisfies all required ownership checks.

## Required checks

- symbol is `BTCUSDT`,
- position side is one-way-compatible,
- margin mode is isolated,
- position direction matches expected trade direction,
- position size matches expected or reconciled strategy size,
- position lineage maps to deterministic Prometheus client order IDs or recovered trade evidence,
- active trade record is present or recoverable,
- no conflicting open normal orders exist,
- no conflicting external orders exist,
- reconciliation has not classified the state as unsafe.

## Ownership after restart

On restart, ownership must be re-established.

Persisted local state may suggest ownership, but restart must still verify exchange state.

## Ownership after unknown entry status

If an entry submission timed out or returned unknown status, a later detected position may be strategy-owned, but only after reconciliation confirms that it matches the submitted entry attempt.

Until confirmed:

```text
ownership_classification = POSSIBLE_STRATEGY_OWNED or UNKNOWN_OWNERSHIP
```

## Ownership after manual intervention

If the operator manually flattens, adjusts, or otherwise changes the futures account outside approved Prometheus controls, Prometheus must not assume continuity.

The bot must reconcile and may require operator review before resumption.

---

## Mapping to Internal Runtime State

This document does not redefine the full runtime state model.

It defines how normalized position facts should influence existing runtime state.

## Clean flat mapping

Conditions:

- clean flat definition is satisfied.

Implications:

```text
trade_lifecycle_state = FLAT
position_state = NO_POSITION
protection_state = NO_PROTECTION_REQUIRED
```

Runtime may enter or remain in `RUNNING_HEALTHY` only if all other gates also permit.

## Position detected after entry workflow

Conditions:

- position exists,
- ownership likely matches active entry workflow,
- protection not yet confirmed.

Implications:

```text
trade_lifecycle_state = POSITION_CONFIRMED or POSITION_UNCONFIRMED
position_state = STRATEGY_POSITION or POSSIBLE_STRATEGY_POSITION
protection_state = PROTECTION_PENDING or PROTECTION_UNCONFIRMED
entries_blocked = true
```

Normal strategy operation must not treat this as steady safe state until protection is confirmed.

## Strategy-owned protected position

Conditions:

- position exists,
- ownership is strategy-owned,
- exactly one valid matching protective stop exists,
- stop side and trigger are consistent with the position,
- reconciliation state is acceptable.

Implications:

```text
trade_lifecycle_state = POSITION_PROTECTED
position_state = STRATEGY_POSITION
protection_state = CONFIRMED_PROTECTED
entries_blocked = true
```

The bot may manage the existing position according to approved trade-management and safety rules.

## Strategy-owned unprotected position

Conditions:

- position exists,
- ownership is strategy-owned or possible strategy-owned,
- protective stop is missing, rejected, stale, conflicting, or unconfirmed.

Implications:

```text
position_state = STRATEGY_POSITION or POSSIBLE_STRATEGY_POSITION
protection_state = UNPROTECTED or PROTECTION_UNCERTAIN
runtime_mode = SAFE_MODE or RECOVERING
entries_blocked = true
incident_severity = emergency/exposure-risk according to incident policy
```

Emergency stop-restoration or flatten policy applies.

## External/manual exposure

Conditions:

- position exists,
- ownership is external/manual or unknown.

Implications:

```text
position_state = EXTERNAL_EXPOSURE or UNKNOWN_OWNERSHIP
runtime_mode = SAFE_MODE or BLOCKED_AWAITING_OPERATOR
entries_blocked = true
operator_review_required = true
```

Prometheus must not add strategy exposure.

## Hedge-mode or margin-mode violation

Conditions:

- hedge-mode position side is observed,
- or margin mode is not isolated,
- or account mode cannot be verified.

Implications:

```text
runtime_mode = SAFE_MODE or BLOCKED_AWAITING_OPERATOR
entries_blocked = true
operator_review_required = true
reconciliation_required = true
```

If exposure exists, severity depends on protection and mismatch risk.

---

## Position and Protection Mapping

Position state and protection state must be evaluated together.

## Position/protection matrix

| Position fact | Protection fact | Classification | Default behavior |
|---|---|---|---|
| No position | No open orders/stops/mismatch | Clean flat possible | Other gates decide entry eligibility |
| No position | Stale protective stop exists | Stale protection artifact | Reconcile/cleanup; block until resolved |
| No position | Open entry order exists | Possible exposure | Block entries; reconcile |
| Position exists | Matching protective stop confirmed | Protected strategy position if ownership known | Manage existing trade only |
| Position exists | Stop submission pending | Protection pending | Block entries; confirm quickly |
| Position exists | Stop missing | Emergency unprotected | Restore protection or flatten according to policy |
| Position exists | Stop rejected | Emergency unprotected | Restore/flatten/escalate |
| Position exists | Multiple stops | Protection uncertain | Reconcile; avoid unsafe cleanup |
| Position exists | Stop ownership unknown | Protection uncertain | Reconcile; operator review if unresolved |
| Position unknown | Any protection state | State unknown | Fail closed |

## Valid protective stop match

A protective stop should be considered matching only when all required checks pass:

- symbol matches position symbol,
- stop is Prometheus-owned or reconciled as valid protection,
- stop side closes the current position direction,
- stop type matches v1 protective-stop model,
- stop uses expected working type and price-protection settings,
- stop trigger price matches current approved stop within exchange tick rules,
- stop is active/open according to exchange state,
- and there is no conflicting active protective stop.

A submitted stop is not confirmed protection.

---

## Manual / Non-Bot Exposure Policy

## Definition

Manual or non-bot exposure includes any futures position or open order that cannot be classified as Prometheus-owned.

Examples:

- manually opened BTCUSDT futures position,
- manually placed BTCUSDT order,
- another bot’s BTCUSDT order,
- ETHUSDT or other futures exposure in the same account,
- unknown order created without Prometheus client ID lineage,
- unexpected position size or side,
- hedge-mode position not created by v1.

## Default behavior

If manual or non-bot exposure is detected:

```text
entries_blocked = true
operator_review_required = true
reconciliation_required = true
```

Prometheus should raise an operator-visible warning or incident depending on severity.

## No automatic adoption

Prometheus must not automatically adopt manual exposure into a normal strategy trade.

Adoption is forbidden in v1 because:

- the strategy stop may be unknown,
- risk sizing may be invalid,
- entry context may not match strategy rules,
- protective-stop logic may not match approved risk,
- and manual exposure undermines testability and review.

## No discretionary management

The operator dashboard should not become a discretionary trading terminal.

Prometheus may support safety actions through approved workflows, but it must not invite ad hoc manual strategy control.

---

## Position Mismatch Policy

A position mismatch occurs when exchange-derived position facts conflict with local state, expected trade state, or other exchange-derived evidence.

## Common mismatch examples

- local state expects flat, exchange shows position,
- local state expects position, exchange shows flat,
- expected long, exchange shows short,
- expected short, exchange shows long,
- expected size differs materially from exchange size,
- expected isolated margin, exchange shows cross margin,
- expected one-way `BOTH`, exchange shows hedge-mode side,
- position exists but no matching entry lineage exists,
- position exists but protective stop is missing,
- position exists but multiple conflicting protective stops exist.

## Default mismatch behavior

```text
entries_blocked = true
reconciliation_required = true
normal strategy progression blocked
```

Runtime should move to `SAFE_MODE`, `RECOVERING`, or `BLOCKED_AWAITING_OPERATOR` depending on whether the mismatch is automatically recoverable.

## Recoverable mismatch examples

Potentially recoverable mismatches include:

- exchange flat, local stale trade state remains,
- stale protective stop remains after flat,
- local stop identifier missing but exactly one valid matching stop exists,
- position exists after known entry timeout and matches the pending entry attempt,
- user-stream event gap but REST confirms clean protected state.

## Unsafe mismatch examples

Unsafe mismatches include:

- position exists with no confirmed protection,
- position side conflicts with local expected side,
- manual/non-bot exposure exists,
- hedge-mode position semantics are detected,
- cross margin is detected during live exposure,
- multiple stops exist and the correct one is not obvious,
- REST and stream-derived state materially disagree and cannot be resolved.

Unsafe mismatches require incident handling and possibly operator review.

---

## Restart and Reconciliation Implications

## Restart begins with provisional local state

On restart, Prometheus must load local persisted state but treat it as provisional.

The bot must then query exchange state and reconcile.

## Required restart position checks

At minimum, restart reconciliation must determine:

1. Does BTCUSDT have a non-zero position?
2. If yes, is the position long or short under one-way semantics?
3. Is margin mode isolated?
4. Can the position be matched to Prometheus ownership?
5. Does an active matching protective stop exist?
6. Are any open normal orders present?
7. Are any open algo orders present?
8. Are there stale or external orders?
9. Is the account in a supported position mode?
10. Can the bot safely classify the state as clean, recoverable, or unsafe?

## Safe resumption rule

Prometheus may leave restart safe mode only when position state has been classified and all blocking issues have been resolved or explicitly approved according to operations policy.

## Existing protected position on restart

If restart finds a strategy-owned protected position:

- preserve the protective stop,
- update local state to exchange truth,
- resume only the allowed management path,
- keep new entries blocked while the position exists.

## Existing unprotected position on restart

If restart finds a position without confirmed protection:

- enter emergency handling,
- block entries,
- restore protection if deterministic and allowed,
- otherwise flatten or escalate according to emergency policy.

## Flat on restart

If restart finds no position and no relevant open orders/stops/mismatches:

- update local state to flat,
- clear stale active trade continuity only through reconciliation event,
- allow safe-mode exit only if all other gates are clean.

---

## Persistence Requirements

The runtime should persist enough position-related state to support safe restart and reconciliation.

## Active trade record fields

The active trade record should include, where applicable:

- `trade_reference`
- `symbol`
- `expected_position_side`
- `expected_signed_position_size`
- `expected_absolute_position_size`
- `average_fill_price`
- `entry_fill_confirmed_at_utc_ms`
- `position_confirmed_at_utc_ms`
- `position_ownership_classification`
- `position_source`
- `updated_at_utc_ms`

## Position continuity fields

The runtime should persist:

- last known normalized position direction,
- last known signed position size,
- last known margin type,
- last known entry price,
- last known notional,
- last known liquidation price where available,
- last position confirmation timestamp,
- last reconciliation timestamp.

## Protection linkage fields

Because position state and protection state are linked, persistence should also retain:

- active protective stop client ID,
- active protective stop exchange/algo ID where known,
- expected stop trigger price,
- protection state,
- last protection confirmation timestamp,
- stop stage.

## Operator/recovery fields

When position state is blocked or mismatched, persist:

- mismatch class,
- blocking reason,
- ownership classification,
- operator review required flag,
- active incident reference if any,
- recovery attempt reference if any.

## Persistence caveat

Persisted position state is never final truth after restart.

It is continuity context for reconciliation.

---

## Observability Requirements

The operator must be able to answer position-state questions quickly.

## Required position summary fields

Dashboard and structured logs should expose:

- exchange symbol position state,
- operational position state,
- position direction,
- position size,
- average entry price,
- break-even price where available,
- mark price where available,
- unrealized PnL where available,
- notional exposure,
- margin type,
- liquidation price where available,
- ownership classification,
- protection state,
- last position confirmation time,
- last protection confirmation time,
- last successful reconciliation time,
- mismatch class if active,
- operator action required yes/no.

## Required alerts

Alert-worthy conditions include:

- position exists but protection is missing,
- position exists but protection is uncertain,
- position exists but ownership is unknown,
- manual/non-bot exposure detected,
- hedge-mode semantics detected,
- cross margin detected,
- position side mismatch,
- position size mismatch,
- REST/user-stream position conflict,
- stale position state while exposure exists,
- open orders exist while position is supposedly flat,
- active stop exists while position is flat.

## Required events

Recommended structured event types:

```text
position.fact_normalized
position.state_changed
position.ownership_classified
position.clean_flat_confirmed
position.external_exposure_detected
position.mismatch_detected
position.margin_mode_violation_detected
position.hedge_mode_detected
position.reconciliation_required
position.reconciliation_resolved
```

All events should include message IDs, correlation IDs, canonical UTC timestamps, source component, symbol, and sanitized payload references where useful.

---

## Testing Requirements

The implementation should include deterministic tests for position-state normalization and mapping.

## Normalization tests

Required cases:

- `positionSide=BOTH`, `positionAmt=0` normalizes to flat,
- `positionSide=BOTH`, positive amount normalizes to long,
- `positionSide=BOTH`, negative amount normalizes to short,
- `positionSide=LONG` blocks v1 live path,
- `positionSide=SHORT` blocks v1 live path,
- missing or malformed position amount fails closed,
- unknown position side fails closed,
- isolated margin normalizes correctly,
- cross margin blocks live entries,
- unknown margin type fails closed.

## Clean flat tests

Required cases:

- zero position plus no orders/stops/mismatch becomes clean flat,
- zero position plus open entry order is not clean flat,
- zero position plus unknown entry outcome is not clean flat,
- zero position plus stale protective stop is not clean flat,
- zero position plus manual order is not clean flat,
- zero position plus unresolved reconciliation mismatch is not clean flat.

## Ownership tests

Required cases:

- position matches active trade lineage -> strategy-owned,
- position after entry timeout with matching lineage -> possible strategy-owned until reconciled,
- position with no matching client order lineage -> external/manual,
- position side mismatch -> unsafe mismatch,
- position size mismatch -> mismatch classification,
- manual exposure blocks entries.

## Protection mapping tests

Required cases:

- strategy-owned position plus one matching stop -> protected,
- strategy-owned position plus missing stop -> emergency unprotected,
- strategy-owned position plus rejected stop -> emergency unprotected,
- strategy-owned position plus multiple stops -> protection uncertain,
- flat position plus active stop -> stale protection artifact requiring cleanup.

## Restart tests

Required cases:

- restart clean flat,
- restart protected strategy position,
- restart unprotected strategy position,
- restart external/manual position,
- restart hedge-mode state,
- restart cross-margin state,
- restart with stale local state but clean exchange state,
- restart with exchange/local side mismatch.

## Stream/snapshot tests

Required cases:

- `ACCOUNT_UPDATE` updates cached position correctly,
- absence of symbol in one account update does not erase cached position,
- REST snapshot overwrites provisional stale position fact during reconciliation,
- stale user stream while positioned blocks entries and requires reconciliation,
- conflicting REST and stream facts fail closed.

---

## Non-Goals

This document does not attempt to define:

- hedge-mode support,
- cross-margin operation,
- multi-position portfolios,
- multi-symbol live trading,
- discretionary account management,
- automatic adoption of manual positions,
- full liquidation-risk formula,
- final dashboard UI design,
- or final database schema.

These are outside v1 scope unless explicitly approved in a later phase.

---

## Open Questions

The following details should be finalized during implementation or later design passes:

1. Exact zero/dust handling if Binance ever reports a tiny residual position amount.
2. Exact tolerance for expected size versus actual size after partial fills and rounding.
3. Exact persistence schema for normalized position facts versus derived state summaries.
4. Whether liquidation price should be shown as a hard dashboard field in paper/shadow if unavailable in simulation.
5. Whether position facts should be retained as a full event-sourced history or summarized plus structured logs for v1.

These open questions do not block the v1 policy:

```text
unknown position state fails closed
```

---

## Acceptance Criteria

This document is implemented correctly when Prometheus can:

- normalize Binance one-way position facts into flat, long, short, or unknown,
- reject hedge-mode semantics in v1 live operation,
- reject cross-margin live operation in v1,
- distinguish exchange-symbol flat from Prometheus clean flat,
- classify strategy-owned versus manual/non-bot exposure,
- block entries when ownership is unknown,
- map position existence separately from protection state,
- classify unprotected live exposure as emergency behavior,
- reconcile position state after restart before resumption,
- persist enough position context for deterministic recovery,
- expose operator-visible position/protection/mismatch status,
- and test all normal, mismatch, restart, and emergency position-state paths without real Binance credentials.

The central policy is:

```text
Prometheus normalizes Binance position facts into a small internal position model.

In v1, only one-way BOTH position semantics and isolated margin are accepted.

A signed position amount determines long, short, or flat at the exchange-symbol level, but clean flat requires no position, no relevant open orders, no protective stops, no unknown outcomes, and no unresolved mismatch.

A position is not safe merely because it exists; it is operationally acceptable only when ownership is known and protective stop coverage is confirmed.

Manual, non-bot, hedge-mode, cross-margin, or ownership-unknown exposure blocks new entries and requires reconciliation and/or operator review.
```
