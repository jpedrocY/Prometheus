# Failure Recovery

## Purpose

This document defines the execution-specific failure-recovery policy for the v1 Prometheus trading system.

Its purpose is to make failure behavior explicit enough that the bot does not improvise when exchange interaction, order status, position state, or protective-stop state becomes uncertain.

The central purpose of this document is to define what Prometheus must do when an execution action may have changed exchange state but the bot does not yet know the final result.

In v1, the correct response to uncertainty is not to retry harder. The correct response is to contain, reconcile, and only then continue.

This document replaces the previous TBD placeholder for:

```text
docs/06-execution-exchange/failure-recovery.md
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
- entry order: normal `MARKET` order
- protective stop: algo / conditional `STOP_MARKET` order
- protective stop uses:
  - `closePosition=true`
  - `workingType=MARK_PRICE`
  - `priceProtect=TRUE`
- stop updates use cancel-and-replace
- user stream is the primary live private-state source
- REST is used for placement, cancellation, reconciliation, and recovery
- restart begins in safe mode
- exchange state is authoritative
- v1 is supervised, not lights-out autonomous

This document covers:

- failure-classification principles,
- no-blind-retry rules,
- REST timeout after submit,
- unknown order status,
- entry rejection,
- partial-fill ambiguity,
- protective-stop submission failure,
- protective-stop confirmation timeout,
- stop replacement failure,
- cancel ambiguity,
- stale user stream during exposure,
- REST reconciliation failure,
- rate-limit / IP-ban risk,
- exchange unavailability during exposure,
- allowed automatic repairs,
- operator escalation rules,
- persistence requirements,
- observability requirements,
- and testing requirements.

This document does **not** define:

- final Binance API wrapper implementation,
- final timeout values,
- final database schema,
- full incident-response policy,
- full restart procedure,
- full operator dashboard behavior,
- final deployment infrastructure,
- or final manual-control workflow.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/binance-usdm-order-model.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/06-execution-exchange/user-stream-reconciliation.md`
- `docs/06-execution-exchange/position-state-model.md`
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

If this document conflicts with the order-handling notes on v1 execution policy, the order-handling notes win.

If this document conflicts with the Binance order model on normal/algo order distinction, the Binance order model wins.

If this document conflicts with stop-loss policy on protective-stop emergency handling, stop-loss policy wins.

If this document conflicts with incident response on severity or escalation, incident response wins.

If this document conflicts with restart procedure on startup sequencing, restart procedure wins.

If this document conflicts with official Binance API behavior, implementation must stop, verify current Binance documentation, and update the affected document before live use.

---

## Core Principles

## 1. No blind retry for exposure-changing actions

Prometheus must not blindly retry any action that may have reached the exchange and may have changed exposure or protection state.

This applies especially to:

- market entry submission,
- market exit submission,
- emergency flatten submission,
- protective stop submission,
- protective stop cancellation,
- protective stop replacement,
- stale order cleanup where outcome affects protection.

If the request may have reached Binance, the system must treat the outcome as unknown until exchange state is checked.

### Rule

```text
request outcome unknown
  -> block new entries
  -> mark reconciliation required
  -> inspect exchange state
  -> continue only after classification
```

## 2. Unknown execution outcome is a safety state

An unknown execution outcome is not a normal transient API error.

It means the bot may not know whether:

- an order exists,
- an order filled,
- a position exists,
- a stop exists,
- a stop was canceled,
- or exposure changed.

Unknown execution outcome must be modeled explicitly and must block normal strategy progression.

## 3. Exchange state is authoritative

Local intent, local commands, REST acknowledgement, and local persisted state are not final truth.

Exchange-derived evidence is required for:

- current position state,
- normal order state,
- algo order state,
- protective-stop state,
- fill confirmation,
- closure confirmation.

Exchange state may be established from user-stream events, REST reconciliation reads, or both.

## 4. User stream is primary during normal operation, REST is recovery support

During healthy live operation, private user-stream events are the primary source of live order/account/algo updates.

REST is required for:

- placement,
- cancellation,
- startup reconciliation,
- recovery after missed events,
- resolving ambiguous order states,
- and verifying position/protection state when confidence is lost.

REST should be used deliberately and symbol-scoped where possible.

## 5. A submitted entry is not a position

After an entry request is submitted, the bot must not assume a position exists until exchange-derived evidence confirms the entry fill and position state.

## 6. A filled entry is not a protected trade

A filled entry or confirmed position is not yet an acceptable steady live state.

A live trade becomes operationally acceptable only after protective-stop coverage is confirmed.

## 7. A submitted stop is not confirmed protection

A REST acknowledgement that a protective stop was submitted does not prove the position is protected.

Protection requires exchange-state evidence such as:

- valid `ALGO_UPDATE`,
- open algo order query,
- successful reconciliation classification,
- or another approved exchange-confirmed path.

## 8. Stop replacement is a dangerous transitional workflow

Cancel-and-replace creates a temporary interval where protection may be uncertain.

The runtime must represent this explicitly and must not assume the old stop or the new stop is active unless exchange state proves it.

## 9. If exposure exists and protection is not confirmed, emergency policy applies

A live position without confirmed protective-stop coverage is an emergency exposure-risk condition.

The system may attempt deterministic protection restoration only when state is clear enough to do so safely.

If protection cannot be restored safely, the emergency flatten/block path applies.

## 10. Recovery must preserve REST request budget

During failure recovery, the bot must avoid REST spam.

Repeated uncontrolled polling can make recovery worse by increasing rate-limit or IP-ban risk.

The system should use bounded, symbol-scoped, prioritized recovery reads and should preserve request capacity for safety-critical actions.

---

## Failure Classification Model

Failure recovery should classify failures by the type of uncertainty they introduce.

Recommended failure classes:

```text
SUBMISSION_UNKNOWN
ORDER_REJECTED
ORDER_STATUS_UNKNOWN
FILL_UNKNOWN
POSITION_UNKNOWN
PARTIAL_FILL_AMBIGUITY
STOP_SUBMISSION_FAILED
STOP_STATUS_UNKNOWN
STOP_CONFIRMATION_TIMEOUT
STOP_CANCEL_UNKNOWN
STOP_REPLACEMENT_FAILED
ORPHANED_STOP_DETECTED
MULTIPLE_STOPS_DETECTED
USER_STREAM_STALE_DURING_EXPOSURE
REST_RECONCILIATION_FAILED
RATE_LIMIT_RECOVERY_IMPAIRED
EXCHANGE_UNAVAILABLE_DURING_EXPOSURE
AUTHORIZATION_FAILURE_DURING_RECOVERY
```

## Classification fields

Every failure classification should capture at least:

```text
failure_class
symbol
trade_reference if known
correlation_id
causation_id if known
runtime_mode_before_failure
trade_lifecycle_state_before_failure
protection_state_before_failure
position_known yes/no
position_present yes/no/unknown
protective_stop_known yes/no
protective_stop_present yes/no/unknown
normal_order_status known/unknown
algo_order_status known/unknown
user_stream_health
market_data_health where relevant
rest_health
incident_severity if opened
reconciliation_required yes/no
operator_review_required yes/no
created_at_utc_ms
```

## Severity mapping

Failure severity should follow the incident-response framework.

| Failure condition | Default severity | Required response |
|---|---:|---|
| Recoverable API warning while flat | Severity 1-2 | Log, monitor, possibly block entries until healthy |
| User stream stale while flat | Severity 2 | Block entries if state confidence degraded, restore, reconcile if needed |
| Entry submission outcome unknown | Severity 3 by default | Safe mode or recovering, block entries, reconcile |
| Entry outcome unknown and exposure may exist | Severity 3-4 | Safe mode, urgent reconciliation |
| Position exists but stop uncertain | Severity 4 | Emergency unprotected policy |
| Stop submission rejected after position confirmed | Severity 4 | Restore if deterministic, otherwise flatten/block |
| Stop replacement ambiguity with live position | Severity 3-4 | Reconcile stop state, restore or emergency path |
| Local/exchange position mismatch | Severity 3-4 | Safe mode, reconcile, operator review if material |
| REST reconciliation unavailable while exposed | Severity 3-4 | Preserve protection if known, escalate if protection unknown |
| Suspected credential compromise | Severity 4 | Security kill switch / revoke / verify account |

---

## Runtime Effects of Failure States

When execution failure affects order, exposure, or protection certainty, the runtime must set or preserve:

```text
entries_blocked = true
reconciliation_required = true
```

Depending on severity and current exposure, runtime mode should move to one of:

```text
SAFE_MODE
RECOVERING
BLOCKED_AWAITING_OPERATOR
```

## Minimum runtime effects

For any non-trivial execution uncertainty:

- block new entries,
- stop normal strategy progression,
- prevent additional exposure-changing commands,
- persist the failure classification,
- emit an observable event,
- reconcile before resumption.

## Position-specific effects

If no position exists and no order is in flight:

- failure may be contained as a degraded/blocked flat state,
- new entries remain blocked until recovery confirms clean state.

If an entry order is in flight:

- exposure must be treated as possible,
- no new entry may be submitted,
- reconciliation must determine whether the order exists, filled, failed, or remains open.

If a position exists:

- protective-stop state becomes the highest priority,
- stop state must be confirmed,
- if protection is missing or uncertain, emergency policy applies.

If protection exists but stream confidence is degraded:

- preserve the stop,
- block new entries,
- reconcile via REST,
- resume only after confidence returns.

---

## Recovery Authority Rules

## State/reconciliation layer owns truth classification

The state/reconciliation layer owns classification of:

- clean state,
- recoverable mismatch,
- unsafe mismatch,
- emergency unprotected state.

The execution layer may detect uncertainty, but it must not unilaterally declare final recovery success.

## Execution layer owns exchange action attempts

The execution layer owns:

- order submission attempts,
- stop submission attempts,
- stop cancellation attempts,
- stop replacement attempts,
- flatten order submission attempts,
- reporting execution uncertainty.

## Exchange adapter owns request/response classification

The exchange adapter owns:

- mapping HTTP errors and exchange errors into internal categories,
- identifying timeout/unknown outcomes,
- enforcing bounded retry policy for safe read-only requests,
- surfacing rate-limit conditions,
- normalizing exchange responses.

## Safety/incident layer owns emergency escalation

The safety/incident layer owns:

- severity assignment,
- safe-mode enforcement,
- kill-switch interaction,
- emergency branch activation,
- operator-review requirement.

## Operator owns ambiguous risk decisions

The operator must be involved when:

- automated recovery cannot restore state certainty,
- flatten-versus-preserve is ambiguous,
- Severity 4 exposure-risk condition occurred,
- emergency flattening was triggered,
- security compromise is suspected,
- kill switch clearance is required.

---

## Read-Only Retry Policy

Read-only recovery actions may be retried under bounded rules.

Examples:

- query current position,
- query open normal orders,
- query open algo orders,
- query specific normal order,
- query specific algo order,
- query recent trades/fills where needed.

### Required constraints

Read-only retries must be:

- bounded by configured maximum attempts,
- backoff-controlled,
- symbol-scoped where possible,
- observable,
- rate-limit aware,
- interrupted if a higher-severity emergency action is required.

### Forbidden behavior

The bot must not enter an infinite query loop.

The bot must not query broad account-wide endpoints repeatedly when symbol-scoped reads are sufficient.

The bot must not consume REST budget on non-critical diagnostics while safety-critical reconciliation is pending.

---

## Write / Exposure-Changing Retry Policy

Write actions that may change exposure or protection must not be retried blindly.

Examples:

- submit entry,
- submit market exit,
- submit emergency flatten,
- submit protective stop,
- cancel protective stop,
- replace protective stop,
- cancel stale order that may be protective,
- cancel all open orders.

### Rule

If the final outcome of a write request is unknown:

```text
write outcome unknown
  -> do not resend same write immediately
  -> mark outcome unknown
  -> block new entries
  -> reconcile relevant exchange state
  -> decide next action from exchange truth
```

### Exception: deterministic idempotency support

If implementation later proves a specific action is safely idempotent through deterministic client IDs and exchange behavior, the action may be retried only under an explicitly documented idempotency policy.

For v1, this document assumes conservative behavior:

```text
unknown write outcome requires reconciliation before another exposure-changing write
```

---

# Scenario Policies

---

## Scenario 1 — REST Timeout After Entry Submit

## Description

The bot submits a normal market entry order and the REST request times out or returns an ambiguous transport failure.

The bot does not know whether Binance received the request.

## Risk

The order may have:

- never reached Binance,
- been accepted but not filled,
- filled immediately,
- partially filled,
- been rejected after acceptance,
- or generated user-stream events the bot has not yet processed.

Blind retry may create duplicate exposure.

## Required response

Immediately:

```text
trade_lifecycle_state = TRADE_EXCEPTION or ENTRY_SUBMITTED_UNKNOWN
runtime_mode = SAFE_MODE or RECOVERING
entries_blocked = true
reconciliation_required = true
```

Then:

1. Check user-stream events already received for the client order ID.
2. Query normal order status by deterministic client order ID where possible.
3. Query open normal orders for BTCUSDT.
4. Query BTCUSDT position state.
5. Query recent fills/trades if order state remains ambiguous.
6. Classify outcome.

## Allowed classifications

### Case A — No order and no position

If exchange evidence shows:

```text
entry order not found or confirmed absent
position flat
no relevant fills
no open normal order
```

Then:

- classify as failed entry with no exposure,
- return to flat blocked state,
- allow resumption only after reconciliation is clean.

### Case B — Order exists but not terminal

If an entry order exists and may still affect exposure:

- keep entries blocked,
- track as pending order exposure,
- wait for terminal state or cancel only if cancellation is safe and approved,
- reconcile again after terminal outcome.

### Case C — Fill occurred / position exists

If fill or position is confirmed:

- update trade lifecycle from exchange truth,
- move to position confirmation path,
- immediately proceed to protective stop submission path,
- do not resume normal strategy behavior until protection is confirmed.

### Case D — State remains ambiguous

If the bot cannot determine whether exposure exists:

- remain in safe mode,
- open or update incident,
- escalate to operator if ambiguity persists beyond configured threshold.

## Forbidden behavior

- Do not submit a second market entry before reconciliation.
- Do not assume timeout means failure.
- Do not assume timeout means success.
- Do not continue evaluating new signals.

---

## Scenario 2 — Unknown Entry Order Status

## Description

An entry order was acknowledged or submitted, but final status cannot be confirmed in the expected window.

Examples:

- missing `ORDER_TRADE_UPDATE`,
- delayed user stream,
- query order returns inconclusive result,
- order ID/client ID mismatch,
- exchange returns temporary error during status check.

## Required response

- block new entries,
- mark order status unknown,
- start reconciliation,
- preserve deterministic identifiers,
- do not submit another entry.

## Reconciliation order

Preferred sequence:

1. Process buffered user-stream events.
2. Query specific order by client order ID or exchange order ID.
3. Query open normal orders for BTCUSDT.
4. Query current position state.
5. Query recent account trades if needed.

## Outcome rules

If filled:

- confirm position,
- proceed to protection.

If rejected/canceled/expired and no position exists:

- record terminal non-entry,
- reconcile flat,
- allow future entries only after all gates are clean.

If partially filled:

- treat as exposure,
- confirm current position size,
- protect or flatten according to emergency/risk policy.

If still unknown:

- remain blocked,
- escalate based on severity and exposure possibility.

---

## Scenario 3 — Entry Rejected

## Description

The exchange rejects the entry order or the adapter detects a local validation failure before submission.

## Local validation failure

If the entry is rejected before reaching the exchange:

- record rejection reason,
- keep flat,
- do not enter recovery unless state is otherwise uncertain.

Examples:

- invalid quantity,
- metadata stale,
- notional cap violation,
- margin mode invalid,
- hedge mode detected,
- missing account permissions.

## Exchange rejection

If Binance rejects an entry request with a known terminal rejection and there is no evidence of fill or position:

- record exchange rejection,
- keep or return to flat state,
- block future entries if rejection indicates a systemic problem.

## Required escalation

Escalate or remain blocked when rejection suggests:

- account mode mismatch,
- permission failure,
- symbol status problem,
- margin or leverage configuration problem,
- repeated parameter-format bugs,
- possible credential issue,
- repeated exchange-side validation failures.

## Forbidden behavior

- Do not adjust risk or quantity ad hoc after rejection unless the full risk approval path is rerun.
- Do not bypass symbol metadata checks.
- Do not resubmit with modified parameters outside the approved strategy/risk/execution path.

---

## Scenario 4 — Partial Fill / Position Ambiguity

## Description

A market entry appears partially filled, or fill and position evidence disagree temporarily.

Although BTCUSDT market entries are expected to fill quickly under normal conditions, v1 must not ignore partial-fill states.

## Required response

If any partial exposure may exist:

- block new entries,
- treat exposure as present,
- query current position,
- determine actual filled size,
- determine whether an entry order remains open or terminal,
- protect the actual position if protection can be submitted safely,
- otherwise flatten/block under incident policy.

## Position-size rule

Protection and emergency actions must use exchange-confirmed position state, not intended order quantity, when the two differ.

## Risk rule

If actual position size is smaller than approved size:

- protect actual size or use `closePosition=true` stop where valid,
- do not scale up to intended size automatically.

If actual position size is larger than approved size:

- classify as serious risk mismatch,
- enter safe mode,
- reduce/flatten according to incident policy.

## Forbidden behavior

- Do not submit a second entry to “complete” the partial fill in v1.
- Do not ignore a partial fill because market orders usually fill.
- Do not consider the trade safe until position and protection are confirmed.

---

## Scenario 5 — Protective Stop Submission Failure

## Description

A position is confirmed, and the bot attempts to submit the required exchange-side protective stop, but the stop submission fails.

Failures include:

- local parameter validation failure,
- exchange rejection,
- REST timeout,
- ambiguous submit result,
- missing confirmation after acknowledgement,
- adapter error before final classification.

## Risk

This is one of the highest-risk execution failures because the bot may now have live exposure without confirmed exchange-side protection.

## Required response

If a position exists and no protective stop is confirmed:

```text
protection_state = POSITION_UNPROTECTED or PROTECTION_UNCERTAIN
runtime_mode = SAFE_MODE or RECOVERING
entries_blocked = true
incident_active = true
```

If protection cannot be confirmed promptly:

```text
protection_state = EMERGENCY_UNPROTECTED
operator_review_required = true
```

## Recovery sequence

1. Verify current position state.
2. Query open algo orders for BTCUSDT.
3. Check whether the intended protective stop exists under deterministic client algo ID.
4. Check for conflicting or stale stops.
5. If no stop exists and state is clear, attempt one deterministic restore-protection action.
6. Reconcile again.
7. If restore succeeds, keep incident/review state as required and decide whether managed trade may continue.
8. If restore fails or state is not clear, enter emergency flatten/block path.

## Deterministic restore requirements

A restore-protection attempt is allowed only when all of the following are true:

- exactly one current BTCUSDT position exists,
- position side is known,
- position mode is one-way,
- margin mode is acceptable,
- no conflicting active protective stop exists,
- intended stop trigger price is known and valid,
- stop is risk-reducing / protective,
- exchange metadata needed for stop expression is available,
- adapter can generate a deterministic client algo ID,
- REST and authentication paths are usable.

## Flatten/block path

If safe restoration is not possible:

- preserve any valid existing protection if present,
- otherwise submit emergency flatten only if policy permits and state is clear enough,
- if flattening also cannot be safely attempted, remain blocked awaiting operator,
- escalate as Severity 4.

## Forbidden behavior

- Do not continue normal trade management while stop is unconfirmed.
- Do not submit multiple competing protective stops blindly.
- Do not widen stop to make submission easier.
- Do not ignore stop rejection because the bot is still online.

---

## Scenario 6 — Protective Stop Confirmation Timeout

## Description

The protective stop submission returned acknowledgement or apparent success, but the system does not receive confirmation that the stop exists within the configured timeout.

## Required response

- move protection state to `STOP_PENDING_CONFIRMATION` while within timeout,
- block new entries,
- if timeout expires, move to `PROTECTION_UNCERTAIN`,
- reconcile via open algo order query and user-stream review,
- classify clean/recoverable/unsafe.

## Outcome rules

If stop exists and matches requirements:

- mark protection confirmed,
- update protection record,
- resume only if all other gates are clean.

If no stop exists and position exists:

- emergency unprotected policy applies.

If multiple stops exist:

- classify as mismatch,
- determine which, if any, is valid protection,
- cancel stale/conflicting stops only when safe,
- operator review may be required.

If status remains unknown:

- remain in safe mode,
- escalate according to exposure risk.

---

## Scenario 7 — Stop Replacement Failure

## Description

The strategy/risk layer approved a risk-reducing stop update, and execution begins cancel-and-replace. The workflow then fails or becomes ambiguous.

Possible failure points:

- old stop cancel request rejected,
- old stop cancel request timed out,
- old stop cancel confirmed but new stop submission failed,
- new stop submitted but not confirmed,
- both old and new stops appear active,
- neither old nor new stop appears active,
- user stream goes stale during replacement.

## Required state handling

During replacement:

```text
protection_state = STOP_REPLACEMENT_IN_PROGRESS
entries_blocked = true
```

If new stop confirmation is pending:

```text
protection_state = STOP_PENDING_CONFIRMATION
```

If certainty is lost:

```text
protection_state = PROTECTION_UNCERTAIN
runtime_mode = SAFE_MODE or RECOVERING
reconciliation_required = true
```

If position exists and no valid protective stop can be confirmed:

```text
protection_state = EMERGENCY_UNPROTECTED
incident severity = Severity 4
```

## Recovery sequence

1. Query current position.
2. Query open algo orders for BTCUSDT.
3. Match stop orders against expected trade reference and client algo IDs.
4. Determine whether old stop, new stop, both, or neither are active.
5. Classify protection state.
6. If exactly one valid protective stop exists, update local state to exchange truth.
7. If no valid stop exists and state is clear, attempt deterministic restore.
8. If multiple/conflicting stops exist, cancel only those that are clearly stale and safe to cancel.
9. If ambiguity remains, escalate.

## Old stop still active

If replacement failed but the old stop is still confirmed active and valid:

- maintain old stop as protection,
- classify replacement failure as recoverable or degraded,
- do not force emergency flatten solely because the improvement failed,
- keep entries blocked until state is clean.

## Old stop canceled, new stop failed

If old stop was canceled and new stop failed:

- classify as unprotected or protection uncertain,
- attempt deterministic restore if safe,
- otherwise emergency path.

## Both stops active

If old and new stops are both active:

- classify as mismatch,
- evaluate whether either could cause harmful behavior,
- prefer preserving protection over aggressive cleanup,
- cancel stale stop only when the active desired stop is confirmed and cancellation is safe,
- log all actions.

## Forbidden behavior

- Do not assume cancel success from timeout.
- Do not assume replacement success from submission acknowledgement.
- Do not continue trailing updates while previous replacement is unresolved.
- Do not widen the stop during recovery.

---

## Scenario 8 — Cancel Ambiguity

## Description

The bot sends a cancel request for a normal order or algo order, but the result is unknown.

This matters especially for protective-stop cancellation during replacement.

## Required response

If cancel outcome is unknown:

- do not assume canceled,
- do not assume active,
- reconcile relevant order set,
- block follow-up actions that depend on the cancel result.

## Normal order cancel ambiguity

If cancel ambiguity affects an entry order:

- treat possible exposure as present,
- query order status,
- query open normal orders,
- query position,
- inspect fills.

If order may still fill:

- keep entries blocked,
- wait for terminal state or take approved safe action.

## Protective stop cancel ambiguity

If cancel ambiguity affects a protective stop:

- query open algo orders,
- preserve any confirmed valid protection,
- do not submit replacement stop until the current protection state is known unless an approved emergency restore policy applies.

## Cancel-all caution

Broad cancel-all actions can remove protection.

In v1, cancel-all behavior must not be used casually during recovery.

If cancel-all is ever used:

- it must be explicitly safety-approved,
- the system must immediately re-check position and stop state,
- if a position remains, protection must be restored or emergency path must activate.

---

## Scenario 9 — User Stream Stale During Exposure

## Description

The private user stream becomes stale, disconnected, expired, delayed, or otherwise untrusted while order or position certainty matters.

## Severity rule

- If flat and no order is in flight: usually Severity 2.
- If entry is in flight: Severity 3 by default.
- If position exists: Severity 3 by default.
- If position exists and protection cannot be verified: Severity 4.

## Required response if flat

If no position exists and no order is in flight:

- block new entries,
- restore/recreate user stream,
- verify no open orders or exposure if required by policy,
- resume only after stream health and reconciliation are acceptable.

## Required response if entry in flight

If an entry is in flight:

- enter safe mode or recovering,
- query order/position state,
- inspect buffered stream events after reconnect,
- do not submit new entries.

## Required response if position exists

If a position exists:

- preserve any confirmed exchange-side stop,
- block new entries,
- restore/recreate user stream,
- query current position,
- query open algo orders,
- verify protection,
- reconcile before resuming.

## Required response if protection uncertain

If protection cannot be confirmed:

- emergency unprotected policy applies,
- deterministic restore or flatten/block path must be considered.

---

## Scenario 10 — REST Reconciliation Failure

## Description

The bot needs REST reconciliation, but REST reads fail, time out, return errors, or become rate-limited.

## Risk

The bot may be unable to verify:

- position state,
- open normal orders,
- open algo orders,
- stop state,
- fill state.

## Required response

If flat and no uncertainty exists:

- block new entries,
- retry bounded read-only reconciliation,
- resume only after successful checks.

If position exists and protection was previously confirmed:

- preserve the known protective stop,
- do not cancel or replace unless required and state is clear,
- raise warning/incident,
- continue attempting bounded recovery.

If position exists and protection is unknown:

- classify high severity,
- attempt to restore visibility,
- escalate to operator,
- consider emergency action only when state is clear enough to avoid worsening risk.

## Forbidden behavior

- Do not resume normal strategy operation without reconciliation.
- Do not spam REST endpoints.
- Do not cancel existing stops merely because queries are failing.
- Do not flatten blindly if position side/size cannot be determined.

---

## Scenario 11 — Rate Limit / IP-Ban Risk

## Description

The exchange adapter detects request-rate warnings, throttling, repeated HTTP 429-like behavior, IP-ban risk, or related rate-limit degradation.

## Risk

Overuse of REST can prevent the bot from performing the state reads or safety actions needed for recovery.

## Required response

- classify rate-limit condition,
- reduce non-critical REST calls,
- preserve request budget for safety-critical reconciliation,
- prefer user-stream-derived state where still trusted,
- block new entries if recovery capacity is degraded,
- escalate if live exposure exists and protection cannot be verified.

## Recovery priority order

When REST budget is constrained, prioritize:

1. position state read,
2. open protective/algo order read,
3. open normal order read,
4. specific order status read,
5. recent fills/trades read,
6. non-critical metadata refresh,
7. diagnostics and dashboard enrichment.

## Forbidden behavior

- Do not poll all account orders repeatedly when symbol-scoped reads are enough.
- Do not allow dashboard refreshes to consume safety-critical request budget.
- Do not allow repeated failed cleanup attempts to create IP-ban risk.

---

## Scenario 12 — Exchange Unavailable During Exposure

## Description

Binance REST or relevant exchange paths become unavailable or unreliable while Prometheus has or may have live exposure.

## Required response

If no exposure and no pending order exists:

- block entries,
- wait for exchange access restoration,
- verify clean state before resuming.

If position exists and protective stop is already confirmed:

- preserve stop,
- block new entries,
- suspend non-essential stop updates,
- avoid actions that could remove protection,
- alert operator.

If position exists and protection is not confirmed:

- classify as emergency risk,
- attempt to restore exchange connectivity,
- use any approved alternate confirmation path if available,
- operator escalation required.

## Stop-management rule during exchange degradation

Normal profit-optimizing trailing is suspended during exchange uncertainty.

Only safety-preserving or risk-reducing actions may be considered, and only when their outcome can be verified or failure behavior is acceptable.

---

## Scenario 13 — Emergency Flatten Failure or Ambiguity

## Description

The bot submits an emergency flatten order, but the result is rejected, times out, or cannot be confirmed.

## Risk

Emergency flatten is itself exposure-changing. If its outcome is unknown, the bot may not know whether the position is still open, partially closed, or fully closed.

## Required response

- do not submit repeated flatten orders blindly,
- query current position,
- query flatten order status where possible,
- inspect user-stream updates,
- query recent fills if needed,
- preserve or restore protection if position remains and stop policy allows,
- escalate to operator.

## Outcome rules

If flat confirmed:

- cancel stale protective orders if safe,
- reconcile flat,
- remain blocked pending review.

If position remains:

- verify protection,
- if unprotected, restore or attempt another emergency action only under controlled policy,
- remain in emergency incident state.

If unknown:

- remain blocked,
- operator review required,
- do not resume normal trading.

---

## Scenario 14 — Authorization Failure During Recovery

## Description

The bot receives authorization, permission, IP restriction, timestamp, or credential-related failures while trying to place, cancel, or reconcile orders.

## Required response

- fail closed,
- block entries,
- classify incident,
- preserve any existing valid protection,
- avoid repeated signed-request spam,
- alert operator,
- escalate to security workflow if compromise or permission drift is suspected.

## Exposure-specific behavior

If flat:

- remain blocked until credential issue is fixed and reconciliation confirms clean state.

If position exists and stop is confirmed:

- preserve stop,
- do not attempt non-essential changes,
- resolve credential access before normal resumption.

If position exists and stop is not confirmed:

- Severity 4 emergency condition,
- operator intervention likely required,
- credential restoration/revocation/rotation path must not ignore live exposure.

---

# Recovery Decision Matrix

| Condition | Runtime mode | Entries | Reconciliation | Automatic repair | Operator review |
|---|---|---:|---:|---:|---:|
| Flat, transient read warning | RUNNING_HEALTHY or SAFE_MODE depending confidence | Maybe blocked | Optional | No | No |
| Flat, user stream stale | SAFE_MODE / RECOVERING | Blocked | Required before live resume | Restore stream | If unresolved |
| Entry submit timeout | SAFE_MODE / RECOVERING | Blocked | Required | Read-only reconciliation | If unresolved |
| Entry rejected locally | Existing mode unless systemic | Blocked for that signal | Not needed unless submitted | No | Usually no |
| Entry exchange rejected, no exposure | SAFE_MODE if systemic, else flat blocked | Blocked until clean | Usually yes | No | If systemic |
| Partial fill | SAFE_MODE / RECOVERING | Blocked | Required | Protect/flatten if safe | Likely |
| Position confirmed, stop pending | SAFE_MODE / RECOVERING until stop confirmed | Blocked | Required if timeout | Submit stop | If timeout/fail |
| Position confirmed, stop rejected | SAFE_MODE / emergency | Blocked | Required | One deterministic restore if safe | Yes |
| Stop replacement failed, old stop active | SAFE_MODE / RECOVERING | Blocked | Required | Keep old stop, repair local state | Maybe |
| Stop replacement failed, no stop | SAFE_MODE / emergency | Blocked | Required | Restore or flatten if safe | Yes |
| Multiple stops | SAFE_MODE / RECOVERING | Blocked | Required | Cleanup only if safe | Usually |
| REST unavailable, flat | SAFE_MODE | Blocked | Deferred until available | No | If prolonged |
| REST unavailable, exposed, stop confirmed | SAFE_MODE | Blocked | Required when available | Preserve stop | Yes if prolonged |
| REST unavailable, exposed, stop unknown | SAFE_MODE / emergency | Blocked | Required but impaired | Only if safe | Yes |
| Credential failure, flat | SAFE_MODE | Blocked | Required after fix | No | Yes if live env |
| Credential failure, exposed | SAFE_MODE / emergency | Blocked | Required | Preserve protection | Yes |

---

# Allowed Automatic Repairs

Automatic repairs are permitted only when they reduce uncertainty or reduce risk without creating uncontrolled exposure.

## Allowed repair categories

### 1. Restore private stream

Allowed when:

- listen key expired or stream disconnected,
- no unsafe write action is required,
- reconnect is observable,
- reconciliation follows if a gap may have occurred.

### 2. Read-only reconciliation

Allowed when:

- endpoint access is available,
- rate-limit budget is acceptable,
- queries are bounded and symbol-scoped where possible.

### 3. Adopt exchange truth into local state

Allowed when:

- exchange state is clear,
- no harmful mismatch remains,
- state transition is logged,
- reconciliation class is `CLEAN` or repaired/rechecked.

### 4. Deterministic protection restoration

Allowed when:

- exactly one position exists,
- side and symbol are known,
- no conflicting active stop exists,
- stop level is known and valid,
- the stop would reduce/protect risk,
- request path is available,
- result can be confirmed.

### 5. Stale order cleanup

Allowed when:

- order is clearly stale,
- cancellation cannot remove required protection,
- cancellation target is identified by deterministic client ID or exchange ID,
- post-cancel reconciliation is required.

### 6. Emergency flatten

Allowed only under emergency policy when:

- position side and size are clear enough,
- flatten action is risk-reducing,
- protective restoration is impossible or not trusted,
- operator approval requirements are satisfied where configured,
- outcome will be reconciled.

---

# Forbidden Recovery Actions

The following are forbidden in v1:

- blind retry of market entry after timeout,
- blind retry of emergency flatten after timeout,
- blind retry of protective stop submission without checking existing stops,
- stop widening to bypass exchange validation,
- scaling into a partial fill to reach intended size,
- same-bar reversal after recovery,
- placing a new entry while any prior entry status is unknown,
- treating REST acknowledgement as final truth,
- treating stop submission as confirmed protection,
- canceling all orders without understanding whether a protective stop will be removed,
- continuing normal trailing while protection is uncertain,
- auto-clearing kill switch or operator-review requirement,
- resuming from safe mode without reconciliation when reconciliation is required,
- using broad account-wide REST polling as a substitute for disciplined state reconciliation,
- ignoring manual/non-bot exposure discovered during recovery.

---

# Persistence Requirements

Failure recovery depends on durable state.

The system must persist enough information to recover safely after a crash during any execution workflow.

## Required persisted facts

At minimum, persistence must capture:

```text
runtime_mode
entries_blocked
reconciliation_required
operator_review_required
kill_switch_active
incident_active
trade_reference
trade_lifecycle_state
protection_state
expected_entry_side
signal_reference
entry_client_order_id
entry_exchange_order_id if known
protective_stop_client_algo_id
protective_stop_exchange_algo_id if known
last_known_position_side
last_known_position_size
last_known_stop_trigger_price
stop_stage
reconciliation_state
last_failure_class
last_failure_reason
last_failure_correlation_id
updated_at_utc_ms
```

## Write-before-continue rule

Before sending exposure-changing requests, the bot should durably record the intent where practical.

After detecting uncertainty, the bot must durably record the uncertainty before attempting complex recovery.

This is required so a crash during recovery does not erase the fact that reconciliation is required.

## Recovery after crash during failure handling

On restart, if persisted state indicates:

- execution uncertainty,
- entry in flight,
- stop pending confirmation,
- stop replacement in progress,
- protection uncertain,
- emergency branch active,
- reconciliation required,

then restart must remain in safe mode and run reconciliation before any normal strategy activity.

---

# Observability and Audit Requirements

Every failure-recovery path must emit structured events.

## Required event families

Failure recovery should emit events such as:

```text
execution.failure_detected
execution.outcome_unknown
execution.entry_status_unknown
execution.stop_submission_failed
execution.stop_confirmation_timeout
execution.stop_cancel_unknown
execution.stop_replacement_failed
reconciliation.required
reconciliation.started
reconciliation.classified_clean
reconciliation.classified_recoverable_mismatch
reconciliation.classified_unsafe_mismatch
protection.state_changed
incident.opened
incident.escalated
recovery.automatic_repair_started
recovery.automatic_repair_succeeded
recovery.automatic_repair_failed
operator_review.required
```

## Required event fields

Each important recovery event should include:

```text
message_id
correlation_id
causation_id
symbol
trade_reference if known
failure_class if relevant
runtime_mode
trade_lifecycle_state
protection_state
reconciliation_state
position_present yes/no/unknown
protective_stop_present yes/no/unknown
normal_order_ids if safe
algo_order_ids if safe
client_order_id if safe
client_algo_id if safe
incident_id if relevant
severity if relevant
occurred_at_utc_ms
processed_at_utc_ms
source_component
```

## Dashboard visibility

The operator dashboard should clearly show:

- current runtime mode,
- whether entries are blocked,
- whether reconciliation is required,
- active failure class,
- active incident severity,
- whether a position exists,
- whether protection is confirmed,
- whether operator action is required,
- last recovery attempt,
- last successful reconciliation time.

## Audit requirements

Any recovery action that changes exchange state must be auditable.

This includes:

- protective stop restoration,
- stop cancellation,
- stale order cleanup,
- emergency flatten,
- kill switch activation,
- operator recovery approval,
- operator denial of recovery,
- manual intervention around stop or position state.

---

# Testing Requirements

The implementation must include tests for failure-recovery behavior before live-like operation.

## Entry failure tests

- REST timeout after entry submit enters safe/recovering state.
- Entry timeout does not blind retry.
- Entry timeout with no order/no position reconciles flat.
- Entry timeout with filled order proceeds to protection.
- Entry timeout with ambiguous status remains blocked.
- Entry rejection with no exposure records rejection and does not trade.
- Partial fill is treated as exposure.

## Stop failure tests

- Stop submission acknowledgement does not confirm protection.
- Stop confirmation timeout enters protection uncertainty.
- Stop rejected while positioned triggers emergency policy.
- Deterministic restore succeeds when state is clear.
- Restore attempt is blocked when conflicting stop exists.
- Restore failure leads to flatten/block emergency path.

## Stop replacement tests

- Replacement enters explicit replacement state.
- Cancel timeout does not assume cancel success.
- Old stop active + new stop failed preserves old protection.
- Old stop canceled + new stop failed enters emergency/unprotected path.
- Both stops active triggers mismatch and safe cleanup logic.
- Neither stop active triggers emergency path.

## Stream failure tests

- User stream stale while flat blocks entries until restored.
- User stream stale while entry in flight triggers reconciliation.
- User stream stale while positioned verifies position and stop.
- User stream stale while protection uncertain escalates emergency.

## REST/rate-limit tests

- Reconciliation uses bounded retries.
- Symbol-scoped reads are preferred.
- Rate-limit condition blocks non-critical polling.
- Rate-limit during exposure escalates if protection cannot be verified.
- REST unavailable while flat blocks entries.
- REST unavailable while exposed and unprotected escalates.

## Persistence/restart tests

- Crash after entry submit but before confirmation restarts in safe mode.
- Crash after position confirmation but before stop confirmation restarts in emergency/protection recovery path.
- Crash during stop replacement restarts with reconciliation required.
- Persisted kill switch remains active after restart.
- Persisted reconciliation-required state blocks normal resumption.

## Operator/escalation tests

- Severity 4 requires operator review.
- Emergency flatten result ambiguity remains blocked.
- Kill switch cannot auto-clear.
- Operator recovery approval is logged.
- Operator denial keeps system blocked.

## Boundary tests

- Strategy cannot bypass recovery state.
- Risk cannot submit recovery orders directly.
- Dashboard cannot force new entry during recovery.
- Execution cannot mark protection confirmed without exchange evidence.
- Adapter cannot hide unknown outcomes as ordinary failures.

---

# Implementation Notes

## Timeout values

This document intentionally does not define exact timeout values.

Implementation should define configurable timeouts for:

- missing entry acknowledgement,
- missing entry fill confirmation,
- missing position confirmation,
- missing protective stop confirmation,
- missing stop cancel confirmation,
- missing replacement stop confirmation,
- stale user stream,
- REST reconciliation read failure,
- emergency recovery escalation.

These values should start conservatively in paper/shadow and tiny-live stages, then be adjusted based on observed exchange behavior.

## Client identifiers

Recovery depends heavily on deterministic client identifiers.

The implementation should ensure that:

- entry orders use deterministic strategy-tagged client order IDs,
- protective stops use deterministic strategy-tagged client algo IDs,
- replacement stops encode enough identity to match trade and stage,
- IDs are compact enough for exchange limits,
- IDs are persisted before or immediately after submission intent.

## Idempotency caution

Deterministic IDs help reconciliation and duplicate detection.

They do not automatically make retries safe.

Any idempotency behavior must be proven against current Binance behavior before being used as a reason to retry writes.

## Fake adapter requirements

The fake exchange adapter must support failure simulation for:

- timeout after accepted entry,
- timeout before accepted entry,
- delayed fill,
- partial fill,
- missing user-stream event,
- stop rejection,
- stop acknowledgement without confirmation,
- cancel ambiguity,
- duplicate stop state,
- REST rate-limit responses,
- exchange unavailable states.

---

# Non-Goals

This document does not add support for:

- multi-symbol recovery choreography,
- hedge-mode position recovery,
- portfolio-margin recovery,
- autonomous exchange failover,
- smart order routing,
- scaling into partial fills,
- discretionary manual trading from the dashboard,
- automatic strategy parameter mutation after failures,
- self-learning recovery policies,
- lights-out live operation,
- unmanaged manual account repair outside audit trail.

These are not v1 behavior.

---

# Open Questions

The following should be resolved before paper/shadow or tiny live.

## 1. Exact timeout values

The project needs specific timeout thresholds for missing confirmations and stale streams.

## 2. Exact client ID format

The project needs a compact deterministic format for normal order IDs and algo order IDs.

## 3. Emergency flatten automation threshold

The project should define exactly when flattening is automatic versus blocked awaiting operator approval.

## 4. Restore-protection retry count

This document allows one deterministic restore attempt when state is clear.

Implementation should decide whether any environment permits more than one attempt. Initial live should remain conservative.

## 5. Rate-limit thresholds

The adapter must define concrete request-rate warning and circuit-breaker thresholds.

## 6. Testnet / dry-run behavior

Paper/shadow design should decide which recovery scenarios use fake adapter simulation, Binance testnet, dry-run mode, or all three.

## 7. Operator UI details

Interface docs should define exactly how recovery states, emergency states, and operator approvals appear on the dashboard.

---

# Acceptance Criteria

This failure-recovery policy is satisfied when the implementation can demonstrate:

- exposure-changing actions are never retried blindly after unknown outcomes,
- entry submit timeout blocks entries and triggers reconciliation,
- unknown order status is represented explicitly,
- partial fills are treated as exposure,
- a filled entry is not treated as safe until protection is confirmed,
- stop submission acknowledgement is not treated as protection,
- stop confirmation timeout enters protection uncertainty,
- stop rejection while positioned triggers emergency policy,
- stop replacement is modeled as a transitional protection state,
- cancel ambiguity is reconciled before dependent actions continue,
- stale user stream during exposure blocks entries and requires reconciliation,
- REST recovery uses bounded, symbol-scoped, rate-limit-aware reads,
- rate-limit/IP-ban risk preserves safety-critical request budget,
- exchange unavailable while exposed is handled conservatively,
- deterministic protection restoration is allowed only when state is clear,
- emergency flatten ambiguity does not cause blind repeated flattening,
- recovery state is persisted across restart,
- incidents and operator-review requirements survive restart,
- every recovery action is observable and auditable,
- fake adapter tests cover success, rejection, timeout, ambiguity, and mismatch paths,
- normal strategy operation cannot resume until reconciliation and safety gates allow it.

---

# Decisions

The following decisions are accepted for v1 failure recovery:

- no blind retry for exposure-changing actions,
- unknown execution outcome fails closed,
- exchange state is authoritative,
- user stream is primary for normal private-state updates,
- REST is required for reconciliation and recovery,
- entry timeout requires reconciliation before any new entry,
- protective-stop uncertainty while positioned is an emergency condition,
- one deterministic restore-protection attempt is allowed only when state is clear,
- stop replacement must explicitly model transitional protection uncertainty,
- cancel ambiguity must be reconciled before dependent actions continue,
- stale user stream during exposure blocks new entries and triggers verification,
- rate-limit/IP-ban risk is a recovery-safety issue, not just a performance issue,
- Severity 4 exposure-risk incidents require operator review before normal resumption.

---

# Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Execution failure-recovery policy
