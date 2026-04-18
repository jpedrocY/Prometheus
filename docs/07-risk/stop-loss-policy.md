# Stop-Loss Policy

## Purpose

This document defines the stop-loss policy for the v1 Prometheus trading system.

Its purpose is to make the risk-side stop policy explicit across:

- strategy stop generation,
- risk validation,
- position sizing,
- exchange-side protective stop placement,
- stop updates,
- stop confirmation,
- stop-related incidents,
- restart/reconciliation,
- and operator visibility.

The strategy specification defines the initial structural stop formula and trade-management stages.

The execution documents define how protective stops are expressed on Binance.

The state and incident documents define what happens when protection is uncertain.

This document ties those decisions together into one risk-control policy:

> No valid stop means no trade.  
> No confirmed protection means no normal live operation.  
> A position without confirmed protection is an emergency condition.

This document replaces the previous TBD placeholder for:

```text
docs/07-risk/stop-loss-policy.md
```

## Scope

This policy applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures
- first live symbol: BTCUSDT perpetual
- first research comparison symbol: ETHUSDT perpetual
- v1 live symbol scope: BTCUSDT only
- strategy family: breakout continuation
- signal timeframe: 15m
- higher-timeframe bias: 1h
- entry method: market entry after completed-bar confirmation
- stop model: structural invalidation plus ATR buffer
- position mode: one-way mode
- margin mode: isolated margin
- max live positions: one
- protective stop: exchange-side STOP_MARKET
- deployment model: supervised staged rollout

This document covers:

- stop policy principles,
- strategy stop versus risk-approved stop versus exchange-side stop,
- initial stop validation,
- protective stop placement timing,
- stop confirmation rules,
- stop update rules,
- stop-widening policy,
- cancel-and-replace behavior,
- stop precision and metadata validation,
- unprotected-position emergency handling,
- stop-related rejection categories,
- persistence requirements,
- observability requirements,
- testing requirements,
- and future expansion constraints.

This document does **not** define:

- full strategy entry logic,
- full position-sizing formula,
- Binance endpoint implementation details,
- daily loss lockout thresholds,
- drawdown lockout thresholds,
- final dashboard design,
- or final production deployment procedure.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/kill-switches.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/operator-workflow.md`

### Authority hierarchy

If this document conflicts with the v1 strategy specification on initial stop formula or trade-management thresholds, the strategy specification wins.

If this document conflicts with the order-handling notes on exchange stop mechanics, the order-handling notes win.

If this document conflicts with the state model on protection states, the state model wins.

If this document conflicts with incident response on emergency severity, incident response wins.

---

## Core Principles

## 1. No stop, no trade

A trade candidate cannot be approved unless it has a valid initial stop.

The stop is required for:

- risk sizing,
- exposure approval,
- liquidation-safety review,
- protective order placement,
- and post-trade review.

## 2. Initial stop is structural

The v1 stop is based on strategy invalidation, not an arbitrary fixed percentage.

It uses setup/breakout structure plus an ATR buffer.

## 3. Risk-approved stop must match execution stop

The stop used for position sizing must be the same stop intended for exchange-side protection, except for documented tick-size adjustments.

If the stop changes after sizing, risk must be recomputed or the trade rejected.

## 4. Every live position must have exchange-side protection

After entry fill and position confirmation, the system must place an exchange-side protective stop.

The bot must not intentionally remain exposed without protective stop coverage.

## 5. Stop submission is not stop confirmation

A REST acknowledgement that a stop was submitted is not enough.

Protection is confirmed only when exchange state confirms the protective stop exists.

## 6. Stop uncertainty blocks normal operation

If the system cannot trust protective stop state, it must block new entries and enter recovery, incident, or emergency logic.

## 7. Stops may reduce risk, not increase it

After a trade is live, the protective stop may stay the same or move in a risk-reducing direction.

Discretionary stop widening is not allowed in v1.

## 8. Cancel-and-replace is safety-critical

V1 stop updates use cancel-and-replace.

This creates a temporary window where protection may be uncertain.

The runtime must model that state explicitly.

## 9. Unprotected exposure is an emergency

A live position without confirmed protective stop coverage is a high-severity exposure-risk condition.

The system must restore protection deterministically if possible, or flatten/block according to emergency policy.

---

## Stop Layers

The system should distinguish three stop layers.

## Layer 1 — Strategy Stop

The strategy stop is the conceptual invalidation level.

It is calculated by the strategy engine from completed-bar market structure.

For a long:

```text
initial_stop = min(setup_low, breakout_bar_low) - 0.10 * ATR(20)
```

For a short:

```text
initial_stop = max(setup_high, breakout_bar_high) + 0.10 * ATR(20)
```

The strategy layer owns this conceptual stop calculation.

## Layer 2 — Risk-Approved Stop

The risk layer validates the strategy stop.

It checks:

- stop exists,
- stop side is valid,
- stop distance is positive,
- stop distance passes ATR filter,
- stop price can be made exchange-valid,
- stop does not violate risk caps,
- stop supports valid position sizing,
- liquidation safety is acceptable,
- metadata needed for validation is available.

The risk-approved stop is the stop used for sizing.

## Layer 3 — Exchange-Side Protective Stop

The execution layer expresses the risk-approved stop as an exchange-side protective stop.

For v1, this means:

```text
STOP_MARKET
closePosition=true
workingType=MARK_PRICE
priceProtect=TRUE
```

The exchange-side protective stop is the disaster protection that should remain active while the position exists.

---

## Initial Stop Validation

A trade candidate must be rejected if any required stop input is invalid.

## Required inputs

- symbol,
- side,
- proposed entry price,
- initial stop price,
- ATR reference,
- strategy version,
- config version,
- exchange symbol metadata,
- stop trigger metadata where applicable.

## Long stop validity

For a long:

```text
initial_stop_price < proposed_entry_price
```

Reject if:

```text
initial_stop_price >= proposed_entry_price
```

## Short stop validity

For a short:

```text
initial_stop_price > proposed_entry_price
```

Reject if:

```text
initial_stop_price <= proposed_entry_price
```

## Stop distance

For a long:

```text
stop_distance = proposed_entry_price - initial_stop_price
```

For a short:

```text
stop_distance = initial_stop_price - proposed_entry_price
```

Reject if:

```text
stop_distance <= 0
```

## ATR stop-distance filter

The v1 strategy uses:

```text
0.60 * ATR <= stop_distance <= 1.80 * ATR
```

Reject if:

```text
stop_distance < 0.60 * ATR
```

Reject if:

```text
stop_distance > 1.80 * ATR
```

## Metadata validation

Reject if required metadata is missing or stale:

- price precision,
- tick size,
- trigger order support,
- working type support,
- price protection support,
- symbol trading status,
- relevant trigger constraints.

## Stop is required before sizing

Position sizing must not proceed without a validated stop.

---

## Stop and Position Sizing Link

The same stop must be used for:

- risk sizing,
- exposure approval,
- protective stop submission,
- and trade-management state.

## Stop changed after sizing

If stop price changes after sizing, one of the following must happen:

1. risk is recomputed with the new stop,
2. quantity is reduced to preserve approved risk,
3. or the trade is rejected.

## Tick-size adjustment

A small tick-size adjustment may be acceptable if:

- it is required for exchange validity,
- it does not materially increase approved risk,
- it is logged,
- and actual risk remains within configured limits.

If rounding or adjustment increases risk beyond tolerance:

```text
reject trade or recompute size
```

---

## Exchange-Side Protective Stop Policy

## Required stop type

For v1, the exchange-side protective stop uses:

```text
STOP_MARKET
```

## Required close behavior

```text
closePosition=true
```

## Required working type

```text
workingType=MARK_PRICE
```

## Required price protection

```text
priceProtect=TRUE
```

## Why this is selected

This design:

- keeps disaster protection on exchange,
- can protect the position if the bot process fails,
- avoids fragile quantity tracking in v1,
- reduces last-trade distortion sensitivity by using mark price,
- and aligns with the strategy’s structural stop model.

## Quantity rule

If using `closePosition=true`, the execution layer must follow Binance rules for whether quantity should be omitted.

The adapter must reject invalid combinations before sending orders where possible.

## reduceOnly rule

If using `closePosition=true`, do not include `reduceOnly` where Binance rules forbid that combination.

## Side rule

For a long position, protective stop side should close the long.

For a short position, protective stop side should close the short.

In one-way mode, implementation must follow Binance’s one-way order semantics.

---

## Protective Stop Timing

## Sequence

The standard live sequence is:

```text
signal_confirmed
entry_submitted
entry_acknowledged
entry_fill_confirmed
position_confirmed
protective_stop_submitted
protective_stop_confirmed
position_protected
```

## Placement timing

The protective stop must be submitted immediately after entry fill and position confirmation.

The system must not intentionally wait for a better price, a later candle, or operator comfort before placing the protective stop.

## Why not before position confirmation

For v1, the protective stop uses `closePosition=true`.

The system should not rely on that stop being valid before the exchange position exists.

The correct approach is to submit the stop as soon as the position is confirmed.

## If entry fill confirmation is delayed

If entry outcome is uncertain:

- block new entries,
- query/reconcile exchange state,
- determine whether position exists,
- submit protective stop if position exists and state is clear enough,
- escalate if state remains uncertain.

---

## Stop Confirmation Policy

## Confirmation sources

A protective stop may be confirmed through:

- user-stream algo update,
- open algo order query,
- reconciliation result using exchange state.

## Not sufficient

The following are not sufficient alone:

- local intent,
- command issued,
- HTTP request attempted,
- REST acknowledgement,
- local database write,
- dashboard optimistic state.

## Pending confirmation state

After submission but before confirmation:

```text
protection_state = STOP_PENDING_CONFIRMATION
```

## Confirmation timeout

The implementation must define a configurable stop-confirmation timeout.

If stop is not confirmed before timeout:

```text
protection_state = PROTECTION_UNCERTAIN
```

If position exists and no valid stop can be confirmed:

```text
protection_state = EMERGENCY_UNPROTECTED
```

## Reconciliation after confirmation

Even after stop confirmation, reconciliation should be able to verify the stop still exists after restart, disconnect, or mismatch.

---

## Stop Update Policy

V1 stop updates use cancel-and-replace.

## Approved reasons to update stop

A stop may be updated when:

- strategy risk stage advances,
- break-even stage activates,
- trailing stage activates,
- trailing level improves,
- exchange metadata correction is required,
- recovery repair is required,
- emergency restore protection is required.

## Not approved reasons

A stop must not be updated because:

- operator wants to “give the trade more room,”
- price moved against the trade,
- volatility expanded after entry,
- the trader feels the stop is too close,
- the strategy generated a discretionary override,
- a future AI component suggests widening risk without approved policy.

## Direction rule

For a long, a stop update must not lower the stop below the currently approved stop.

For a short, a stop update must not raise the stop above the currently approved stop.

In simple terms:

```text
stop may stay same or reduce risk
stop may not widen risk
```

## Exception: technical correction

A narrow technical correction may be allowed if:

- the original stop cannot be accepted by exchange due to precision/trigger constraints,
- the correction is required for validity,
- the corrected stop does not materially increase approved risk,
- risk remains within allowed limit,
- and the correction is logged.

If the correction would materially increase risk:

```text
recompute size or reject
```

---

## Strategy Stop Management Stages

The v1 strategy uses staged stop management.

## Stage 1 — Initial protection

After entry, the original structural stop remains active.

## Stage 2 — No early stop reduction

Before the trade reaches at least:

```text
+1.0R maximum favorable excursion
```

the stop is not moved, except under operational safety conditions.

## Stage 3 — First risk reduction

When the trade reaches:

```text
+1.0R MFE
```

research default:

```text
move stop from full initial risk to -0.25R
```

This reduces risk without forcing immediate break-even.

## Stage 4 — Break-even transition

When the trade reaches:

```text
+1.5R MFE
```

move stop to:

```text
break-even
```

## Stage 5 — Trailing mode

When the trade reaches:

```text
+2.0R MFE
```

activate trailing mode.

For a long:

```text
trail_level = highest_high_since_entry - 2.5 * ATR(20)
```

For a short:

```text
trail_level = lowest_low_since_entry + 2.5 * ATR(20)
```

Trailing remains strategy-managed in v1.

## Native exchange trailing stop

Native Binance trailing stop is not the default v1 trailing mechanism.

Any future use of exchange-native trailing stops requires separate testing and approval.

---

## Cancel-and-Replace Procedure

Stop replacement must be modeled as a controlled workflow.

## Required sequence

```text
1. Verify current position still exists.
2. Identify the currently active protective stop.
3. Calculate replacement stop.
4. Validate replacement stop does not increase risk.
5. Validate replacement stop is exchange-compatible.
6. Persist replacement workflow state.
7. Cancel current protective stop.
8. Confirm cancellation.
9. Submit replacement protective stop.
10. Confirm replacement stop exists.
11. Persist updated protection state.
12. Emit observability events.
```

## Replacement state

During replacement:

```text
protection_state = STOP_REPLACEMENT_IN_PROGRESS
```

## Replacement failure

If replacement cannot be confirmed:

```text
protection_state = PROTECTION_UNCERTAIN
```

If a position exists and no valid protective stop exists:

```text
protection_state = EMERGENCY_UNPROTECTED
```

## No silent continuation

The system must not continue as if the position is protected when stop replacement outcome is unknown.

---

## Emergency Unprotected Policy

## Definition

Emergency unprotected state exists when:

```text
position exists
and
valid protective stop cannot be confirmed
```

This is one of the most severe operational states in v1.

## Required response

If emergency unprotected state is detected:

```text
block all new entries
raise critical alert
enter emergency branch
attempt deterministic protection restore if possible
flatten if protection cannot be restored with high confidence
require operator review before resumption
```

## Controlled restore attempt

The bot may attempt one controlled protection-restore action before flattening if all conditions are true:

```text
position side is known
position size is known or closePosition=true can safely apply
intended stop price is known
no conflicting open orders exist
exchange connectivity is usable
protective stop submission path is available
the system can confirm the result
```

## Restore sequence

If deterministic restore is allowed:

```text
1. remain in safe/emergency mode
2. submit replacement protective stop
3. confirm stop exists
4. rerun reconciliation
5. update persistence
6. require operator-visible review if severity policy requires it
```

## If restore fails

If restore fails, confirmation cannot be obtained, or state is ambiguous:

```text
flatten exposure conservatively
or block awaiting operator if automated flatten is unsafe
```

The incident policy determines whether flattening is automatic or operator-mediated in the specific case.

## After emergency

After emergency unprotected state:

- normal trading must not resume automatically,
- operator review is required,
- incident record must be created or updated,
- reconciliation must be clean before resumption,
- daily/weekly review should include the event.

---

## Restart and Reconciliation Stop Policy

## Startup behavior

On startup, the bot begins in safe mode.

If persisted local state indicates a recent or active trade, restart reconciliation must verify:

- whether exchange position exists,
- whether open protective stop exists,
- whether protective stop matches expected role,
- whether unexpected protective stops exist,
- whether local state can be repaired.

## Position exists, stop confirmed

If position exists and exactly one valid protective stop is confirmed:

- repair local state if needed,
- classify mismatch as clean or recoverable where appropriate,
- resume only after full restart procedure passes.

## Position exists, stop missing

If position exists and no valid stop is confirmed:

```text
emergency unprotected state
```

Use emergency policy.

## No position, stop exists

If no position exists but protective stop exists:

```text
orphaned protective stop
```

Required response:

- block new entries,
- classify order,
- cancel if safe,
- reconcile again.

## Multiple stops

If multiple protective stops exist:

- block new entries,
- classify mismatch,
- resolve duplicates if deterministic,
- require operator review if ambiguous.

---

## Stop Precision and Exchange Constraints

## Required validation

Before stop submission, execution/risk must validate:

- symbol status,
- tick size,
- trigger price precision,
- stop order support,
- STOP_MARKET support,
- `MARK_PRICE` working type support,
- `priceProtect` support,
- `closePosition=true` support,
- trigger direction validity,
- current price relation to trigger.

## Stop price rounding

Stop price rounding must preserve exchange validity and risk integrity.

## Long stop rounding

For long stops below market, rounding must not create a stop that violates trigger rules or materially increases risk.

## Short stop rounding

For short stops above market, rounding must not create a stop that violates trigger rules or materially increases risk.

## If rounding changes risk

If stop rounding changes stop distance:

- recompute actual risk,
- confirm risk remains within allowed tolerance,
- or recompute quantity,
- or reject trade.

## Metadata unavailable

If required metadata is unavailable:

```text
reject trade or block stop update
```

If already in a live position and metadata is unavailable during protection repair, incident policy should guide emergency handling.

---

## Stop-Related Rejection Categories

Recommended categories:

```text
MISSING_INITIAL_STOP
INVALID_STOP_SIDE
INVALID_STOP_DISTANCE
STOP_TOO_TIGHT
STOP_TOO_WIDE
STOP_PRICE_PRECISION_INVALID
STOP_TRIGGER_INVALID
STOP_WOULD_INCREASE_RISK_AFTER_ROUNDING
STOP_METADATA_UNAVAILABLE
STOP_ORDER_TYPE_UNSUPPORTED
STOP_WORKING_TYPE_UNSUPPORTED
PRICE_PROTECT_UNSUPPORTED
CLOSE_POSITION_UNSUPPORTED
PROTECTIVE_STOP_SUBMISSION_FAILED
PROTECTIVE_STOP_CONFIRMATION_TIMEOUT
PROTECTIVE_STOP_REJECTED
PROTECTIVE_STOP_MISSING
MULTIPLE_PROTECTIVE_STOPS
ORPHANED_PROTECTIVE_STOP
STOP_REPLACEMENT_FAILED
STOP_REPLACEMENT_UNCONFIRMED
STOP_WIDENING_NOT_ALLOWED
POSITION_UNPROTECTED
PROTECTION_UNCERTAIN
EMERGENCY_UNPROTECTED
```

Each rejection or incident should include a human-readable reason.

---

## Persistence Requirements

Stop-related state is restart-critical.

The runtime should persist at minimum:

```text
trade_reference
symbol
protection_state
protective_stop_client_order_id
protective_stop_exchange_order_id
stop_trigger_price
stop_stage
risk_stage
trailing_stage
last_protection_confirmation_at_utc_ms
stop_replacement_in_progress
emergency_unprotected
updated_at_utc_ms
```

## Write timing

Durable writes should occur when:

- initial stop is accepted by risk,
- protective stop submission starts,
- protective stop is submitted,
- protective stop is confirmed,
- stop replacement starts,
- stop cancellation is confirmed,
- replacement stop is submitted,
- replacement stop is confirmed,
- protection uncertainty is entered,
- emergency unprotected state is entered,
- trade closes and protection requirement ends.

## Local state is not truth

Persisted stop state is local continuity state.

Exchange state remains authoritative after restart or uncertainty.

---

## Observability Requirements

Stop protection must be highly visible.

## Required operator-visible fields

The operator should be able to see:

```text
position present yes/no
position side
position size
current stop price
stop stage
risk stage
trailing stage
protective stop confirmed yes/no
last stop confirmation time
stop replacement in progress yes/no
protection uncertainty yes/no
emergency unprotected yes/no
orphaned stop yes/no
multiple stops yes/no
```

## Required alerts

Critical alerts:

- position exists but stop missing,
- protective stop rejected,
- protective stop confirmation timeout,
- stop replacement failed,
- protection uncertain,
- emergency unprotected,
- multiple protective stops,
- orphaned stop after position close.

Warnings:

- stop rounding changed risk,
- stop update delayed,
- stop metadata stale,
- mark-price stream degraded while protected position exists.

## Required event families

Stop-related events should include:

```text
protection.stop_submission_started
protection.stop_submitted
protection.stop_confirmed
protection.stop_confirmation_timeout
protection.stop_replacement_started
protection.stop_cancel_confirmed
protection.stop_replacement_submitted
protection.stop_replacement_confirmed
protection.stop_replacement_failed
protection.protection_uncertain
protection.emergency_unprotected_entered
protection.orphaned_stop_detected
protection.multiple_stops_detected
```

---

## Operator Control Boundaries

## Manual stop movement

The operator must not casually move stops manually on exchange while the bot is active.

Manual stop changes outside bot awareness create reconciliation risk.

## Dashboard stop controls

The v1 dashboard should not provide discretionary stop-widening controls.

Allowed stop-related operator actions may include:

- pause new entries,
- request controlled restart/reconciliation,
- activate kill switch,
- approve recovery resumption,
- request emergency flatten,
- approve emergency recovery action where required.

## Emergency manual intervention

If the operator manually changes or cancels a stop during an emergency:

- the action must be logged,
- the bot must reconcile afterward,
- normal operation must remain blocked until state is clean.

---

## Implementation Boundaries

## Strategy layer owns

- initial conceptual stop formula,
- MFE/R stage logic,
- trailing stop candidate calculation,
- stop update intent.

## Risk layer owns

- validating stop distance,
- validating stop side,
- validating stop risk,
- rejecting invalid stops,
- approving stop update risk direction.

## Execution layer owns

- submitting protective stop,
- canceling protective stop,
- replacing protective stop,
- handling exchange responses,
- emitting execution uncertainty.

## Exchange adapter owns

- mapping stop requests to Binance order fields,
- validating exchange parameter support,
- signing/submitting requests,
- normalizing responses.

## State/reconciliation owns

- confirming whether stop exists,
- comparing local and exchange stop state,
- classifying mismatches,
- deciding clean/recoverable/unsafe outcomes.

## Safety/incident owns

- emergency classification,
- safe-mode enforcement,
- operator-review requirements,
- kill-switch interaction.

---

## Testing Requirements

The implementation must include tests for the following.

## Initial stop tests

- long stop below entry passes,
- long stop above entry rejects,
- short stop above entry passes,
- short stop below entry rejects,
- stop distance <= 0 rejects,
- stop too tight rejects,
- stop too wide rejects.

## Sizing link tests

- sizing stop equals execution stop,
- stop adjustment after sizing triggers recompute/reject,
- tick-size adjustment does not exceed risk tolerance,
- risk increase after rounding rejects.

## Protective stop tests

- protective stop submitted after position confirmation,
- submission acknowledgement does not equal confirmed protection,
- stop confirmation from user-stream/query updates protection state,
- confirmation timeout enters protection uncertainty.

## Stop update tests

- risk-reducing long stop update passes,
- risk-widening long stop update rejects,
- risk-reducing short stop update passes,
- risk-widening short stop update rejects,
- cancel-and-replace enters replacement state,
- replacement success confirms new stop,
- replacement failure enters protection uncertainty.

## Emergency tests

- position without stop enters emergency unprotected,
- deterministic restore attempt succeeds and reconciles,
- restore failure triggers flatten/block path,
- no conflicting orders requirement enforced,
- operator review required after emergency.

## Restart/reconciliation tests

- position and stop clean after restart,
- position without stop after restart emergency,
- no position with orphaned stop cleanup,
- multiple stops create mismatch,
- local stop state differing from exchange state reconciles.

## Boundary tests

- strategy cannot confirm stop existence,
- risk cannot place stop order,
- execution cannot mark position protected without exchange evidence,
- dashboard cannot widen stop.

---

## V1 Non-Goals

The stop-loss policy does not include:

- partial take-profit stop logic,
- discretionary stop movement,
- manual trailing from dashboard,
- exchange-native trailing stop as primary method,
- portfolio-level stop coordination,
- multi-symbol stop netting,
- AI-generated dynamic stop widening,
- volatility-adaptive stop expansion after entry,
- averaging down stop movement,
- breakeven movement before approved threshold,
- removing the stop because the bot is watching the position.

These are not v1 behavior.

---

## Open Questions

The following should be resolved before paper/shadow or tiny live.

## 1. Exact stop confirmation timeout

The policy requires a timeout, but the exact value should be defined during implementation/testing.

## 2. Exact stop rounding tolerance

The policy requires no material risk increase, but the tolerance should be defined in code/config.

## 3. Emergency flatten automation threshold

Incident policy should define when flattening is automatic versus blocked awaiting operator.

## 4. Mark-price diagnostic display

Dashboard requirements should define how mark-price context is shown around stop behavior.

## 5. Native trailing stop future research

Native Binance trailing stops may be researched later, but v1 uses strategy-managed cancel-and-replace.

---

## Acceptance Criteria

This stop-loss policy is satisfied when implementation can demonstrate:

- no trade is approved without a valid initial stop,
- stop distance is validated against ATR filter,
- stop used for sizing matches stop used for protection,
- protective stop is submitted after position confirmation,
- stop submission acknowledgement is not treated as confirmation,
- stop confirmation requires exchange-state evidence,
- stop updates are risk-reducing only,
- stop widening is rejected,
- cancel-and-replace is modeled as transitional protection state,
- replacement failure enters protection uncertainty,
- position without confirmed stop enters emergency state,
- deterministic restore-protection attempt is allowed only when safe,
- failed restore leads to flatten/block emergency path,
- stop-related state is persisted,
- stop-related events are observable,
- operator cannot casually widen stops,
- and normal trading cannot continue under protection uncertainty.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Risk stop-loss and protection policy
