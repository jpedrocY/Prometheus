# User Stream Reconciliation

## Purpose

This document defines the user-stream reconciliation policy for the v1 Prometheus trading system.

Its purpose is to define how Prometheus uses Binance USDⓈ-M futures private user-stream events and REST reads to maintain confidence in:

- entry order lifecycle,
- fill confirmation,
- position state,
- protective stop state,
- algo order state,
- restart recovery,
- unknown execution outcomes,
- and local-versus-exchange consistency.

The system must not rely on local intent alone.

This document replaces the previous TBD placeholder for:

```text
docs/06-execution-exchange/user-stream-reconciliation.md
```

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
- entry order: normal MARKET order
- protective stop: algo STOP_MARKET order
- protective stop uses:
  - closePosition=true
  - workingType=MARK_PRICE
  - priceProtect=TRUE
- user stream is the primary live source of private order/account/protection events
- REST is used for placement, cancellation, reconciliation, and recovery
- restart begins in safe mode
- exchange state is authoritative

This document covers:

- user-stream responsibilities,
- REST reconciliation responsibilities,
- event families,
- listen-key lifecycle,
- stream freshness and staleness,
- order update handling,
- account update handling,
- algo update handling,
- state transition expectations,
- reconciliation triggers,
- reconciliation sequence,
- clean/recoverable/unsafe classifications,
- unknown execution outcomes,
- missing protective stop handling,
- restart behavior,
- persistence and observability requirements,
- testing requirements,
- and implementation boundaries.

This document does **not** define:

- final Binance API wrapper implementation,
- order endpoint mapping,
- position-sizing formula,
- stop-loss risk policy,
- incident severity matrix,
- final database schema,
- dashboard design,
- or production deployment steps.

Those are defined in related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/binance-usdm-order-model.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/06-execution-exchange/failure-recovery.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/kill-switches.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/operator-workflow.md`

### Authority hierarchy

If this document conflicts with the state model on runtime modes or protection states, the state model wins.

If this document conflicts with the order model on Binance event/identifier distinctions, the order model wins.

If this document conflicts with stop-loss policy on protective stop emergency behavior, stop-loss policy wins.

If this document conflicts with restart procedure on startup sequencing, restart procedure wins.

---

## Core Principles

## 1. User stream is primary live private-event source

During normal live operation, user-stream events are the primary source for:

- normal order lifecycle updates,
- fills and partial fills,
- account and position updates,
- algo/protective stop lifecycle updates.

## 2. REST is reconciliation and recovery support

REST is required for:

- startup state reconstruction,
- recovery after stream interruption,
- resolving unknown order outcomes,
- checking open normal orders,
- checking open algo orders,
- checking position state,
- and verifying state after confidence loss.

REST snapshots do not eliminate the need for user-stream processing.

## 3. Exchange truth outranks local state

Local state is for orchestration, persistence, and continuity.

Exchange state is authoritative for:

- whether a position exists,
- whether a normal order exists,
- whether an algo order exists,
- whether a protective stop exists.

## 4. Commands are not facts

An execution command is intent.

A submitted request is not proof of fill.

A stop-placement request is not proof of protection.

State changes require exchange-derived evidence and/or reconciliation.

## 5. Stream staleness is a safety condition

If the private stream becomes stale or unavailable while order or position certainty matters, the system must block new entries and reconcile.

## 6. Unknown states fail closed

If the bot cannot confidently determine order, position, or stop state, it must enter safe/recovery behavior.

## 7. Protection is first-class

A position is not operationally safe unless protective stop coverage is confirmed.

---

## Private Event Types Required for V1

Prometheus v1 must support at least three Binance user-stream event types.

## `ORDER_TRADE_UPDATE`

Used for normal order lifecycle events.

Relevant to:

- entry order creation,
- entry order acknowledgement,
- partial fills,
- final fills,
- cancellations,
- rejections,
- expirations,
- market exit order lifecycle,
- emergency flatten order lifecycle.

## `ACCOUNT_UPDATE`

Used for account and position state changes.

Relevant to:

- position size changes,
- balance changes,
- realized PnL changes,
- funding fee effects,
- margin-type or position changes where present.

## `ALGO_UPDATE`

Used for algo/conditional order lifecycle events.

Relevant to:

- protective stop creation,
- protective stop active state,
- protective stop cancellation,
- protective stop trigger,
- protective stop rejection,
- replacement stop lifecycle.

---

## User Stream Lifecycle

## Listen-key lifecycle

Binance USDⓈ-M user data streams require a listen-key / private stream lifecycle.

The implementation must:

- create or restore a listen key where required,
- keep it alive before expiry,
- recreate it if invalid,
- reconnect after disconnection,
- classify stream health,
- and persist/emit stream lifecycle events where useful.

## Connection duration

User-stream connections may have maximum lifetimes and expected disconnect behavior.

The implementation must expect planned reconnects and should not treat every disconnect as a catastrophic event.

However, while exposure exists, any stream gap can affect state confidence.

## Keepalive behavior

The user-stream layer must maintain keepalive according to current Binance rules.

If keepalive fails:

- mark user stream degraded or stale,
- block new entries if state certainty matters,
- reconnect/recreate listen key,
- reconcile if gap may have occurred.

## Event ordering

The stream should process events by exchange event time and processing time.

Where Binance provides ordering guidance, implementation should follow it.

The system should still tolerate duplicate, delayed, or out-of-order events.

---

## User Stream Health States

Recommended user-stream health states:

```text
HEALTHY
DEGRADED
STALE
UNAVAILABLE
RESTORING
```

## `HEALTHY`

Meaning:

- stream connected,
- keepalive working,
- recent events/heartbeat behavior acceptable,
- no known gap requiring reconciliation.

## `DEGRADED`

Meaning:

- stream connected but weaker than normal,
- event delay, reconnect, keepalive warning, or uncertain cadence detected,
- new entries may be blocked depending on exposure context.

## `STALE`

Meaning:

- stream has not been trustworthy within required tolerance,
- event gap may exist,
- new entries must be blocked,
- reconciliation required if order/position state matters.

## `UNAVAILABLE`

Meaning:

- stream is disconnected or unusable,
- new entries blocked,
- recovery/reconnect required.

## `RESTORING`

Meaning:

- reconnect/recreate/backfill/reconciliation is in progress,
- new entries blocked until restored and reconciled.

---

## Stream Staleness Policy

## Staleness triggers

User stream should be marked stale or unsafe when:

- connection is lost unexpectedly,
- keepalive fails,
- listen key expires,
- stream reconnects after a gap,
- message delay exceeds configured threshold,
- event parsing fails repeatedly,
- expected event confirmation does not arrive,
- private event sequence appears inconsistent,
- or stream health cannot be determined.

## State effect

When user stream is stale:

```text
entries_blocked = true
reconciliation_required = true
```

If exposure exists:

```text
runtime_mode = SAFE_MODE or RECOVERING
```

depending on current recovery action.

## Existing position while stream stale

If a protected position exists and user stream becomes stale:

- preserve existing protective stop,
- block new entries,
- query exchange state,
- verify position and stop,
- repair/reconcile if needed,
- continue only after confidence is restored.

If position is unprotected or protection cannot be confirmed:

- emergency policy applies.

---

## Event Normalization

Raw Binance payloads must be normalized before entering runtime state logic.

## Normalized event requirements

Every normalized private event should include:

```text
event_type
exchange
symbol where applicable
event_time_utc_ms
processed_at_utc_ms
source_stream
raw_event_id or hash where practical
correlation_id if known
causation_id if known
normalized_payload
redaction_status
```

## Raw payload policy

Raw payloads may be retained internally for debugging if safe.

They must not contain secrets.

They must be redacted before logging.

They must not become the stable internal runtime API.

## Unknown fields

Unknown new fields from Binance should not crash the runtime.

Unknown critical enum values should trigger safe handling.

---

## ORDER_TRADE_UPDATE Handling

## Purpose

`ORDER_TRADE_UPDATE` drives normal order lifecycle handling.

## Relevant order roles

Prometheus should map events to roles such as:

```text
ENTRY
EXIT
EMERGENCY_FLATTEN
STALE_CLEANUP
UNKNOWN_EXTERNAL
```

## Required matching fields

To match a normal order update to local state, use:

- symbol,
- client order ID,
- exchange order ID,
- order side,
- order type,
- order status,
- execution type,
- quantity/fill information,
- trade/correlation reference where encoded or mapped.

## Expected state transitions

A normal entry order may progress through:

```text
ENTRY_SUBMITTED
ENTRY_ACKNOWLEDGED
ENTRY_FILL_CONFIRMED
POSITION_CONFIRMED
```

However:

```text
entry fill confirmed != position protected
```

## Fill confirmation

A fill may be confirmed by a valid `ORDER_TRADE_UPDATE` with trade/fill evidence.

Position must still be confirmed through `ACCOUNT_UPDATE`, REST position query, or reconciliation.

## Partial fill handling

If partial fill occurs:

- block new entries,
- track partial exposure,
- confirm current position size,
- ensure protection policy is applied if exposure exists,
- classify state carefully.

For v1 market entries, partial fill may be short-lived but must not be ignored.

## Rejection handling

If order is rejected:

- record rejection,
- keep flat if no exposure exists,
- verify no position exists if ambiguity remains,
- block entries if rejection reason is operationally significant.

## Unknown normal order update

If order update cannot be classified:

```text
block new entries
classify as UNKNOWN_EXTERNAL or UNKNOWN_ORDER_STATE
reconcile
operator review if unresolved
```

---

## ACCOUNT_UPDATE Handling

## Purpose

`ACCOUNT_UPDATE` supports position and balance state updates.

It is critical for confirming whether exposure exists after order events.

## Position confirmation

After entry fill evidence, Prometheus should confirm position through:

- account update position fields,
- REST position query,
- or reconciliation.

## Position fields

The normalized account update should capture:

```text
symbol
position_side
position_size
entry_price
unrealized_pnl where available
margin_type where available
event_reason where available
event_time_utc_ms
processed_at_utc_ms
```

## Balance/PnL fields

Account updates may also support:

- realized PnL tracking,
- fee/funding effects,
- daily loss calculations,
- drawdown calculations.

## Account update limitations

An account update may not include every symbol every time.

The implementation must not assume absence from one account update means no position exists unless Binance semantics and reconciliation logic support that conclusion.

## Funding updates

Funding-related account updates should feed PnL/account tracking, not strategy signal logic.

---

## ALGO_UPDATE Handling

## Purpose

`ALGO_UPDATE` drives algo/protective stop lifecycle handling.

## Relevant order roles

Prometheus should map algo events to:

```text
PROTECTIVE_STOP
REPLACEMENT_PROTECTIVE_STOP
STALE_CLEANUP
UNKNOWN_EXTERNAL
```

## Required matching fields

To match an algo update to local protection state, use:

- symbol,
- clientAlgoId,
- algoId,
- side,
- type,
- trigger price,
- working type,
- close-position setting,
- status,
- trade reference where encoded/mapped.

## Protective stop confirmation

A protective stop can be considered confirmed only if exchange state shows:

- correct symbol,
- correct active stop role,
- expected side,
- expected trigger price within approved tolerance,
- expected `closePosition=true`,
- expected `workingType=MARK_PRICE`,
- expected `priceProtect=TRUE`,
- active/open state,
- matches current active trade.

## Stop triggered

If protective stop triggers:

- confirm position closure through account/position state,
- cancel/clean orphaned state if needed,
- record stop execution,
- transition trade toward exit confirmed / trade closed if exchange confirms flat.

## Stop canceled

If stop cancellation is expected during replacement:

- continue replacement workflow,
- confirm replacement submission.

If stop cancellation is unexpected while position exists:

```text
PROTECTION_UNCERTAIN or EMERGENCY_UNPROTECTED
```

## Unknown algo update

If algo update cannot be classified:

```text
block new entries
reconcile open algo orders
operator review if unresolved
```

---

## REST Reconciliation Inputs

REST reconciliation should be able to query the minimum exchange truth needed for v1.

## Required REST reads

At minimum:

```text
current BTCUSDT position
open normal orders for BTCUSDT
open algo orders for BTCUSDT
specific normal order by client/order ID where needed
specific algo order by clientAlgoId/algoId where needed
recent fills/trades where needed
account balance/equity where needed
```

## Symbol scope

Use BTCUSDT-scoped reads where possible.

Avoid broad account scanning unless necessary for detecting non-bot exposure or account-level safety issues.

## Metadata reads

Reconciliation may also require:

- exchange symbol metadata,
- current account mode,
- margin mode,
- leverage/bracket state.

---

## Reconciliation Triggers

Reconciliation is required when:

- process starts or restarts,
- user stream reconnects after possible gap,
- listen key expires or is recreated,
- private stream becomes stale,
- normal order status is unknown,
- algo order status is unknown,
- REST request outcome is ambiguous,
- order submission times out,
- stop submission confirmation times out,
- stop replacement is interrupted,
- local position and exchange position disagree,
- local stop state and exchange open algo orders disagree,
- orphaned protective stop is detected,
- multiple protective stops are detected,
- non-strategy/manual exposure is detected,
- operator requests controlled restart,
- incident policy requires confidence restoration.

---

## Startup Reconciliation Sequence

On startup, the runtime begins in safe mode.

Recommended sequence:

```text
1. Load persisted runtime state.
2. Restore kill-switch/pause/operator-review flags.
3. Mark entries blocked.
4. Establish exchange connectivity.
5. Establish or restore user stream.
6. Query current BTCUSDT position.
7. Query open normal orders for BTCUSDT.
8. Query open algo orders for BTCUSDT.
9. Match exchange state to persisted local state.
10. Classify result as clean, recoverable mismatch, or unsafe mismatch.
11. Repair deterministic mismatches if allowed.
12. Recheck after repair.
13. Allow safe-mode exit only if all gates pass.
```

## Startup rule

Do not enter `RUNNING_HEALTHY` directly on process start.

Even if no position is expected, startup must prove enough exchange state to resume.

---

## Reconciliation Classification

The reconciliation layer should classify outcomes.

## `CLEAN`

Meaning:

- local and exchange state are acceptably aligned,
- no unexpected position,
- no unexpected open order,
- no missing protective stop,
- no unknown execution state,
- no blocking mismatch.

## `RECOVERABLE_MISMATCH`

Meaning:

- mismatch exists,
- deterministic safe repair exists,
- no immediate uncontrolled exposure remains after repair,
- recheck is required before normal resumption.

Examples:

- local flat but exchange has known stale strategy order that can be safely canceled,
- local stop ID missing but exchange has exactly one matching protective stop,
- persisted state stale but exchange state clearly confirms flat.

## `REPAIRED_PENDING_RECHECK`

Meaning:

- repair action was taken,
- system must query exchange again before resumption.

## `UNSAFE_MISMATCH`

Meaning:

- automated continuation is unsafe,
- operator review or emergency action is required.

Examples:

- position exists with no confirmed protective stop,
- position size differs materially from local state,
- unknown external position exists,
- multiple conflicting protective stops,
- order status unknown after possible submission,
- stop cancellation occurred unexpectedly while position exists.

---

## Clean Flat State Criteria

The system can be considered clean/flat only if exchange truth confirms:

```text
no BTCUSDT strategy position
no unexpected BTCUSDT position
no open Prometheus entry order
no unknown entry outcome
no open protective stop
no unknown algo outcome
no blocking user-stream gap
no active reconciliation mismatch
```

If account-scope checks detect non-bot exposure, clean flat is false for v1 live operation.

---

## Clean Protected Position Criteria

A live position can be considered clean/protected only if:

```text
BTCUSDT position exists
position side and size are known
position matches active trade context
exactly one valid protective stop exists
protective stop matches expected role and side
protective stop uses expected closePosition/workingType/priceProtect behavior
no unknown entry/exit order state exists
no conflicting open orders exist
user stream is healthy or REST reconciliation is clean
```

This is the only acceptable steady open-position state.

---

## Recoverable Mismatch Examples

Recoverable mismatches may include:

## Missing local stop ID but exchange stop exists

If exchange shows exactly one valid matching protective stop and local state lacks its ID:

- repair local state,
- persist stop ID,
- recheck.

## Local active trade but exchange flat

If exchange confirms no position and no open orders:

- close local trade lifecycle,
- mark trade closed/reconciled,
- recheck.

## Orphaned known strategy order while flat

If known strategy-owned order exists while flat and can be safely canceled:

- cancel,
- confirm cancellation,
- recheck.

## User stream gap but REST state clean

If user stream had gap but REST confirms clean flat or protected position:

- mark recovered,
- restore stream,
- recheck,
- clear recovery if all gates pass.

---

## Unsafe Mismatch Examples

Unsafe mismatches include:

## Position without stop

If position exists and no valid protective stop exists:

```text
EMERGENCY_UNPROTECTED
```

## Position size mismatch

If exchange position size differs materially from local active trade size:

- block entries,
- classify unsafe unless deterministic explanation exists,
- require operator review or repair.

## Unknown entry outcome

If an entry request may have reached exchange and outcome cannot be determined:

- block entries,
- query by client order ID,
- inspect position,
- classify unsafe if unresolved.

## Multiple protective stops

If multiple protective stops exist and correct one cannot be determined confidently:

- block entries,
- classify unsafe or recoverable only if deterministic cleanup is safe.

## Non-strategy exposure

If manual/non-bot position or order exists:

- block entries,
- require operator review.

## Security anomaly

If exchange state suggests unauthorized trading:

- security kill switch,
- incident response,
- credential review.

---

## Unknown Execution Outcome Handling

Unknown execution outcome is safety-critical.

## Examples

- REST timeout after order submission,
- connection dropped after signed order request,
- malformed response after submission,
- exchange returned ambiguous error,
- user stream did not confirm,
- order query temporarily unavailable.

## Required behavior

```text
block new entries
enter SAFE_MODE or RECOVERING
query order by deterministic client ID
query position state
query open normal orders
query open algo orders if relevant
classify reconciliation result
```

## No blind retry

Do not blindly retry exposure-changing requests after unknown outcome.

This applies to:

- entry orders,
- protective stop submissions,
- stop cancellations,
- stop replacements,
- flattening orders.

State must be checked first.

---

## Protective Stop Reconciliation

Protective stop reconciliation must verify:

```text
stop exists
stop is active/open
stop belongs to current trade
symbol matches
side matches expected close direction
trigger price matches approved stop within tolerance
closePosition=true
workingType=MARK_PRICE
priceProtect=TRUE
no duplicate protective stop exists
```

If any critical field fails:

```text
PROTECTION_UNCERTAIN
```

If position exists and no valid stop exists:

```text
EMERGENCY_UNPROTECTED
```

## Stop trigger while stream unavailable

If stop may have triggered while stream was unavailable:

- query current position,
- query order/algo history if needed,
- reconcile trade closure,
- update realized PnL/daily loss/drawdown,
- do not assume position remains open or closed without exchange evidence.

---

## Orphaned Stop Reconciliation

An orphaned stop exists when:

```text
no position exists
but active protective stop exists
```

Required behavior:

- block new entries,
- identify whether stop is strategy-owned,
- cancel if deterministic and safe,
- confirm cancellation,
- recheck exchange state,
- record event.

If ownership is unknown:

- operator review required,
- do not silently cancel external orders unless emergency policy allows.

---

## Multiple Stop Reconciliation

Multiple protective stops are unsafe unless deterministic cleanup is obvious.

Required behavior:

- block new entries,
- identify active trade,
- identify all open stops,
- classify known strategy-owned versus unknown external,
- preserve or restore one valid protective stop,
- cancel duplicates only if deterministic and safe,
- recheck state.

If ambiguity remains:

```text
UNSAFE_MISMATCH
operator review required
```

---

## Manual / Non-Bot Exposure Reconciliation

For v1, manual or non-bot exposure in the same futures account blocks new entries.

Detection examples:

- position without Prometheus trade reference,
- open normal order without known client ID prefix,
- open algo order without known clientAlgoId prefix,
- position on symbol outside live allowlist,
- position created while bot was offline and no persisted workflow exists.

Required behavior:

```text
block new entries
classify as non-strategy exposure
raise operator-visible alert
require operator review
```

The bot should not automatically manage non-strategy exposure as if it owns it.

---

## Stream Recovery Procedure

When user stream is degraded/stale/unavailable:

```text
1. Mark user-stream health degraded/stale.
2. Block new entries.
3. Attempt reconnect or listen-key recreation.
4. Query current exchange state through REST.
5. Compare exchange state to persisted local state.
6. Classify reconciliation result.
7. Repair deterministic mismatch if allowed.
8. Recheck exchange state.
9. Mark stream restored only after connection and state confidence are both acceptable.
10. Resume only if all runtime gates pass.
```

## Stream restored is not enough

A WebSocket reconnect by itself does not prove state is clean.

State must be reconciled after any meaningful gap.

---

## Reconciliation and Runtime Modes

## SAFE_MODE

Used when normal strategy operation is blocked but safety actions remain allowed.

## RECOVERING

Used while reconciliation/repair is actively running.

## BLOCKED_AWAITING_OPERATOR

Used when automated recovery cannot safely decide the next action.

## RUNNING_HEALTHY

Allowed only when:

- reconciliation is clean or not required,
- user stream health is acceptable,
- no active blocking incident exists,
- no kill switch is active,
- no operator pause is active,
- no unprotected position exists,
- if position exists, protection is confirmed.

---

## Reconciliation Write Timing

Reconciliation state is restart-critical and must be persisted.

Durable writes should occur when:

- reconciliation is required,
- reconciliation starts,
- exchange position is read,
- open normal orders are read,
- open algo orders are read,
- mismatch is classified,
- repair action starts,
- repair action succeeds/fails,
- emergency branch is entered,
- reconciliation becomes clean,
- safe-mode exit is allowed or blocked.

---

## Persistence Requirements

Minimum reconciliation persistence fields:

```text
reconciliation_state
reconciliation_reason
last_successful_reconciliation_at_utc_ms
reconciliation_started_at_utc_ms
mismatch_class
repair_required
repair_in_progress
latest_exchange_position_reference
latest_open_order_reference
latest_open_algo_order_reference
related_incident_id
updated_at_utc_ms
```

Minimum user-stream continuity fields:

```text
user_stream_health_state
listen_key_alias_or_metadata
last_user_stream_event_time_utc_ms
last_user_stream_processed_at_utc_ms
last_keepalive_success_at_utc_ms
last_reconnect_at_utc_ms
stream_gap_detected
stream_gap_reason
updated_at_utc_ms
```

Do not persist raw secrets or listen keys in ordinary runtime state if avoidable.

---

## Observability Requirements

The operator must be able to see:

```text
user stream health
last private event time
last private event processing time
last keepalive success
current reconciliation state
last successful reconciliation time
position present yes/no
position side and size
protection confirmed yes/no
open normal order count
open algo order count
unknown order count
non-strategy exposure present yes/no
mismatch class
repair in progress yes/no
operator action required yes/no
```

## Required alerts

Alerts should occur for:

- user stream stale,
- listen key keepalive failure,
- user stream reconnect after active exposure,
- unknown execution status,
- position without stop,
- missing protective stop,
- orphaned protective stop,
- multiple protective stops,
- non-strategy exposure,
- unsafe mismatch,
- reconciliation failed,
- safe-mode exit blocked.

---

## Event Contract Expectations

Recommended events:

```text
user_stream.connected
user_stream.disconnected
user_stream.keepalive_succeeded
user_stream.keepalive_failed
user_stream.marked_stale
user_stream.restored
user_stream.event_received
user_stream.event_normalized
user_stream.normalization_failed

reconciliation.required
reconciliation.started
reconciliation.exchange_position_queried
reconciliation.open_orders_queried
reconciliation.open_algo_orders_queried
reconciliation.classified_clean
reconciliation.classified_recoverable_mismatch
reconciliation.classified_unsafe_mismatch
reconciliation.repair_started
reconciliation.repair_succeeded
reconciliation.repair_failed
reconciliation.recheck_required
reconciliation.completed
reconciliation.safe_mode_exit_blocked
reconciliation.safe_mode_exit_allowed
```

## Event payload basics

Important events should include:

```text
symbol
runtime_mode
reconciliation_state
protection_state where relevant
trade_lifecycle_state where relevant
user_stream_health_state
correlation_id
causation_id
event_time_utc_ms
processed_at_utc_ms
source_component
```

---

## Implementation Boundaries

## User-stream layer owns

- listen-key lifecycle,
- WebSocket connection,
- keepalive,
- raw private event intake,
- stream health classification,
- event normalization.

## Reconciliation layer owns

- comparing exchange state to local state,
- mismatch classification,
- repair/recheck workflow,
- clean/recoverable/unsafe result.

## State layer owns

- runtime state transitions,
- trade lifecycle state,
- protection state,
- reconciliation state.

## Execution layer owns

- submitting/canceling orders,
- stop replacement actions,
- flatten actions when approved,
- surfacing unknown execution status.

## Safety/incident layer owns

- emergency branching,
- kill-switch interaction,
- operator review required state,
- severity classification.

## Operator layer owns

- operator approval/rejection,
- manual restart/recovery request,
- status display.

---

## Testing Requirements

Implementation must include tests for the following.

## User-stream lifecycle tests

- listen key created/refreshed,
- keepalive success updates health,
- keepalive failure marks degraded/stale,
- disconnect marks unavailable/stale,
- reconnect triggers reconciliation,
- stream restored only after state confidence restored.

## Event normalization tests

- `ORDER_TRADE_UPDATE` normalized,
- `ACCOUNT_UPDATE` normalized,
- `ALGO_UPDATE` normalized,
- unknown event type handled safely,
- unknown enum value fails closed,
- duplicate event does not corrupt state,
- delayed event handled by event/processing time.

## Entry lifecycle tests

- entry update confirms order lifecycle,
- fill update does not mark position protected,
- account update confirms position,
- unknown entry status triggers reconciliation,
- duplicate entry prevention after timeout.

## Protective stop tests

- algo update confirms protective stop,
- stop submit ack alone does not confirm protection,
- missing stop enters emergency state,
- stop canceled unexpectedly enters protection uncertainty,
- orphaned stop detected,
- multiple stops detected.

## Reconciliation classification tests

- clean flat state,
- clean protected position,
- recoverable stale local state,
- recoverable orphaned known order,
- unsafe position without stop,
- unsafe manual position,
- unsafe unknown execution outcome,
- repaired pending recheck.

## Restart tests

- startup begins safe,
- persisted flat reconciles clean,
- persisted active trade with exchange position/stop reconciles clean,
- persisted active trade but exchange flat resolves recoverably,
- exchange position without stop triggers emergency,
- active kill switch remains active.

## Boundary tests

- user-stream layer does not clear incidents,
- execution layer does not mark reconciliation clean,
- strategy layer does not consume raw Binance private events,
- dashboard cannot emit exchange-truth events directly.

---

## V1 Non-Goals

The user-stream reconciliation design does not include:

- multi-symbol live reconciliation,
- portfolio-level reconciliation,
- hedge-mode long/short leg reconciliation,
- multi-account reconciliation,
- cross-exchange reconciliation,
- automated management of manual external positions,
- high-frequency trade-stream optimization,
- WebSocket trading API as primary execution path,
- reconciliation-free operation.

These may be considered later, but they are not v1 behavior.

---

## Open Questions

The following should be resolved before paper/shadow or tiny live.

## 1. Exact stream freshness thresholds

Define how long without private events/keepalive success marks degraded or stale.

## 2. Exact confirmation timeouts

Define timeouts for entry fill, position confirmation, stop confirmation, cancel confirmation, replacement confirmation.

## 3. Exact repair permissions

Define which recoverable mismatches may be repaired automatically and which require operator approval.

## 4. Exact non-strategy exposure procedure

V1 blocks new entries on non-strategy exposure, but emergency handling for external exposure should be clarified if needed.

## 5. Exact event deduplication key

Define deterministic event deduplication across reconnects and repeated payloads.

## 6. Listen-key storage policy

Define whether listen-key metadata is persisted, and how to avoid secret-like leakage.

---

## Acceptance Criteria

This user-stream reconciliation policy is satisfied when implementation can demonstrate:

- user stream lifecycle is modeled explicitly,
- `ORDER_TRADE_UPDATE` drives normal order updates,
- `ACCOUNT_UPDATE` supports position/account updates,
- `ALGO_UPDATE` supports protective stop lifecycle,
- user-stream stale state blocks new entries,
- reconnect after gap requires reconciliation,
- startup always reconciles before normal operation,
- clean flat state can be proven,
- clean protected position can be proven,
- recoverable mismatches are repaired and rechecked,
- unsafe mismatches block normal operation,
- unknown execution outcomes fail closed,
- position without stop enters emergency path,
- orphaned and multiple stops are detected,
- manual/non-bot exposure blocks entries,
- reconciliation state persists across restart,
- operator dashboard shows user-stream and reconciliation state,
- and no component treats local command intent as exchange truth.

---

## References

Official Binance references to verify during implementation:

- Binance USDⓈ-M Futures User Data Streams  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams

- Binance USDⓈ-M Futures Event: Order Update  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Order-Update

- Binance USDⓈ-M Futures Event: Balance and Position Update  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Balance-and-Position-Update

- Binance USDⓈ-M Futures Event: Algo Order Update  
  https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Algo-Order-Update

- Binance Derivatives Change Log  
  https://developers.binance.com/docs/derivatives/change-log

Implementation must verify these references at coding time because Binance derivatives APIs and WebSocket routing may change.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: User-stream and reconciliation behavior specification
