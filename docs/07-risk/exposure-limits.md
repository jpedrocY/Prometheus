# Exposure Limits

## Purpose

This document defines the exposure-limit framework for the v1 Prometheus trading system.

Its purpose is to define the hard boundaries around whether the system is allowed to add, maintain, or continue exposure.

The position-sizing framework answers:

> Given a valid trade candidate, what quantity is allowed?

This exposure-limits document answers:

> Is the system allowed to have this exposure at all?

The exposure-limit framework exists to ensure that:

- the bot trades only approved symbols,
- v1 remains one-position and one-symbol,
- pending or unknown order states are treated conservatively,
- manual or non-bot exposure blocks new entries,
- notional and leverage caps are enforced as hard gates,
- unprotected exposure is treated as an emergency,
- and exposure expansion happens only through staged review.

This document replaces the previous TBD placeholder for:

```text
docs/07-risk/exposure-limits.md
```

## Scope

This document applies to v1 Prometheus with the following assumptions:

- venue: Binance USDⓈ-M futures
- first live symbol: BTCUSDT perpetual
- first secondary research comparison: ETHUSDT perpetual
- v1 live symbol scope: BTCUSDT only
- strategy family: breakout continuation
- signal timeframe: 15m
- higher-timeframe bias: 1h
- position mode: one-way mode
- margin mode: isolated margin
- max live positions: one
- max active protective stop: one
- deployment model: supervised staged rollout

This document covers:

- symbol exposure limits,
- position exposure limits,
- pending-order exposure limits,
- protective-order exposure expectations,
- notional exposure limits,
- leverage exposure limits,
- manual/non-bot exposure behavior,
- environment-specific exposure policy,
- exposure gate checks,
- approval/rejection output models,
- testing requirements,
- and future expansion constraints.

This document does **not** define:

- full position-sizing formula,
- daily loss lockout thresholds,
- drawdown control thresholds,
- kill-switch mechanics,
- stop-loss placement formula,
- exchange order field mapping,
- exact database schema,
- or final live deployment runbooks.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/07-risk/kill-switches.md`
- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`
- `docs/06-execution-exchange/exchange-adapter-design.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/operator-workflow.md`

### Authority hierarchy

If this document conflicts with the state model on position/protection truth, the state model wins.

If this document conflicts with incident response on emergency handling, incident response wins.

If this document conflicts with the position-sizing framework on calculation formula, the position-sizing framework wins.

If this document conflicts with exchange-order behavior, the execution/exchange documents win.

---

## Core Principles

## 1. Exposure limits are hard gates

Exposure limits are not suggestions.

If an exposure gate fails, the system must not open new exposure.

## 2. Unknown exposure is treated as possible exposure

If the system cannot prove whether an order or position exists, it must assume exposure may exist until reconciliation proves otherwise.

## 3. V1 is one-symbol and one-position

V1 live operation is intentionally narrow:

```text
BTCUSDT only
one position maximum
one active strategy
one active protective stop maximum
```

This narrowness is a safety feature.

## 4. Manual or non-bot exposure blocks new entries

If the bot detects an open futures position or open order that it cannot classify as strategy-owned, it must block new entries and require operator review.

The production futures account should remain exposure-clean during v1 operation.

## 5. Existing exposure changes the system objective

When no position exists, the system may evaluate entries if all gates pass.

When a position exists, the system objective changes to:

- maintain protection,
- manage exits,
- reconcile state,
- prevent duplicate exposure,
- and preserve capital.

## 6. Position without confirmed protection is an emergency

An open position without confirmed protective stop coverage is not merely a risk-limit violation.

It is an emergency or severity-4 exposure condition under the incident framework.

## 7. Exposure expansion is staged

Future increases toward:

```text
1% live risk
5x or 10x leverage caps
larger notional caps
```

are possible, but only through validation, release, and operator approval.

---

## Exposure Categories

The system should distinguish five exposure categories.

## 1. Position exposure

A confirmed open position on Binance USDⓈ-M futures.

For v1:

```text
max_open_positions = 1
max_open_positions_per_symbol = 1
allowed_live_symbols = ["BTCUSDT"]
```

If a strategy-owned BTCUSDT position exists:

```text
block new entries
manage existing position only
```

## 2. Pending order exposure

An order that may create or modify exposure but has not reached a terminal known state.

Examples:

- market entry submitted but not confirmed filled/rejected,
- entry order acknowledged but final outcome not known,
- partially filled entry order,
- timeout after order submission,
- order status unknown,
- stale open strategy-owned entry order,
- retry ambiguity.

Rule:

```text
if entry_order_in_flight:
    block new entries
```

Rule:

```text
if unknown execution status exists:
    block new entries
    require reconciliation
```

## 3. Protective order state

Protective orders are not new exposure, but they are safety-critical.

If a position exists:

```text
exactly one valid active protective stop should exist
```

If no position exists:

```text
no active protective stop should remain unless cleanup/recovery is in progress
```

Unexpected protective orders must trigger reconciliation.

## 4. Notional exposure

The USD value of the current or proposed position.

Approximate for linear BTCUSDT:

```text
notional_usdt = quantity * price
```

The system must enforce an internal notional cap independent of what Binance technically allows.

## 5. Account-level exposure

Exposure elsewhere in the same futures account that may not belong to Prometheus.

Examples:

- manual BTCUSDT position,
- manual ETHUSDT futures position,
- open manual order,
- another bot’s position,
- unexpected strategy-unclassified order.

For v1:

```text
non-bot exposure blocks new entries
operator review required
```

---

## What Counts as Exposure

## Counts as exposure

The following must count as current or possible exposure:

- confirmed open strategy position,
- entry order submitted and not terminal,
- unknown-status entry attempt,
- stale open entry order,
- partially filled entry order,
- unconfirmed position after fill evidence,
- open manual futures position,
- open non-strategy order,
- unexpected open strategy-owned order,
- exchange/local position mismatch,
- protective stop uncertainty while position exists.

## Does not count as new exposure

The following do not count as new exposure by themselves:

- confirmed protective stop for an existing position,
- canceled order confirmed terminal,
- rejected order confirmed terminal,
- flat position confirmed by exchange,
- read-only metadata fetch,
- market-data stream,
- user-stream event intake,
- reconciliation query,
- REST account-state read.

## Ambiguous cases

Ambiguous cases must be treated as possible exposure.

Example:

```text
order submission timed out after request may have reached exchange
```

Safe interpretation:

```text
exposure may exist
block new entries
reconcile
```

---

## Locked V1 Exposure Rules

## Rule 1 — BTCUSDT only

Live v1 may trade only:

```text
BTCUSDT perpetual on Binance USDⓈ-M futures
```

Reject live entries for:

- ETHUSDT,
- altcoin perpetuals,
- spot symbols,
- coin-margined futures,
- options,
- other venues.

ETHUSDT remains research/comparison only until explicitly promoted.

## Rule 2 — One position maximum

V1 allows:

```text
max_total_strategy_positions = 1
```

If any strategy-owned position exists:

```text
block new entries
```

## Rule 3 — No pyramiding

If an existing BTCUSDT position is already open in the same direction:

```text
reject same-direction entry
```

No adding to winners.

No scaling in.

No averaging into a position.

## Rule 4 — No reversal entry while position exists

If BTCUSDT long exists and a short signal appears:

```text
do not open short
```

If BTCUSDT short exists and a long signal appears:

```text
do not open long
```

The strategy may generate an exit intent if rules allow, but same-bar reversal execution is not v1 behavior.

## Rule 5 — Hedge mode not supported

If account or symbol behavior indicates hedge mode or ambiguous position-side behavior:

```text
reject live entry
block trading until corrected
```

V1 assumes one-way mode.

## Rule 6 — Isolated margin required

If BTCUSDT margin mode is not isolated:

```text
reject live entry
```

Do not silently trade under cross margin.

## Rule 7 — Entry in flight blocks new exposure

If an entry order was submitted and final status is not known:

```text
block new entries
```

This remains true even if the strategy generates a new valid signal.

## Rule 8 — Unknown order status blocks new exposure

If any strategy-owned order has unknown status:

```text
block new entries
require reconciliation
```

## Rule 9 — Missing protection blocks all new entries

If a position exists and protective stop is not confirmed:

```text
block all new entries
enter incident/emergency path
```

## Rule 10 — Internal notional cap is mandatory

For any live environment:

```text
max_position_notional_usdt must be explicitly configured
```

If missing:

```text
reject live entry
```

## Rule 11 — Manual exposure blocks bot entries

If the bot detects exposure or open orders it cannot classify as strategy-owned:

```text
block new entries
raise operator-visible warning
require operator review
```

## Rule 12 — Account should be clean for v1 runtime

For v1 production/tiny-live operation, the Binance futures account should not contain unrelated live positions or open orders.

Mixed-use account operation is not supported in v1.

---

## Symbol Exposure Policy

## Live symbol allowlist

Initial live allowlist:

```text
["BTCUSDT"]
```

## Research symbol list

Research may include:

```text
["BTCUSDT", "ETHUSDT"]
```

## Symbol promotion

A research symbol may become live-eligible only after:

- strategy validation,
- execution-readiness review,
- risk review,
- exposure-limit update,
- operator approval,
- release process,
- updated runbooks,
- and explicit configuration change.

## Symbol mismatch

If a live order candidate symbol is not in the live allowlist:

```text
reject exposure
```

## Symbol metadata requirement

Allowed symbol status and trading filters must be available and fresh before live approval.

---

## Position Count Policy

## V1 maximum

```text
max_total_open_positions = 1
max_open_positions_per_symbol = 1
```

## Strategy-owned position

A position is strategy-owned only if it can be matched to Prometheus state through:

- symbol,
- known trade reference,
- known client order ID lineage,
- known user-stream events,
- persisted state,
- and reconciliation.

If ownership cannot be established:

```text
treat as non-bot exposure
block new entries
require operator review
```

## Existing flat state

The system is considered flat only when exchange truth confirms:

- no BTCUSDT position,
- no unexpected position on relevant account scope,
- no open strategy entry orders,
- no unknown execution status,
- no unresolved mismatch.

---

## Pending Order Exposure Policy

## Entry orders

Any non-terminal strategy entry order blocks new entries.

Examples:

- submitted,
- acknowledged,
- partially filled,
- pending query,
- status unknown,
- cancel pending.

## Market orders

Even market orders must pass through status confirmation.

A market order is not considered terminal merely because a REST submission response exists.

## Duplicate prevention

The exposure layer must prevent:

- duplicate entry after timeout,
- duplicate entry after delayed user-stream event,
- duplicate entry after restart,
- duplicate entry caused by retry logic.

## Unknown status

Unknown status must force:

```text
SAFE_MODE or RECOVERING
reconciliation required
new entries blocked
```

---

## Protective Order Exposure Policy

## Position exists

If position exists, expected protective stop count:

```text
1 valid active protective stop
```

## No position exists

If no position exists, expected protective stop count:

```text
0 active protective stops
```

Unless cleanup/recovery is explicitly in progress.

## Multiple protective stops

If multiple protective stops exist:

```text
block new entries
reconcile
classify mismatch
operator review if unsafe
```

## Missing protective stop

If position exists and no valid protective stop is confirmed:

```text
Severity 4 exposure-risk condition
emergency branch
restore protection or flatten
```

## Stale protective stop

If a protective stop exists but no longer matches the active position or current stop-management stage:

```text
block new entries
reconcile
repair if deterministic
```

---

## Notional Exposure Policy

## Internal hard cap

Each live environment must define:

```text
max_position_notional_usdt
```

## Proposed position notional

For linear USDT futures:

```text
proposed_notional_usdt = approved_quantity * proposed_entry_price
```

## Projected total notional

For v1, because no existing position is allowed when opening new exposure:

```text
projected_total_strategy_notional_usdt = proposed_notional_usdt
```

If future versions allow multiple positions, this formula must be updated.

## Notional cap rule

Reject if:

```text
projected_total_strategy_notional_usdt > max_position_notional_usdt
```

## Missing cap

Reject live entry if:

```text
max_position_notional_usdt is missing
```

## Cap increases

Increasing `max_position_notional_usdt` requires:

- config version change,
- risk review,
- operator approval,
- release note,
- and stage-appropriate validation.

---

## Effective Leverage Exposure Policy

## Initial live cap

Initial live effective leverage cap:

```text
max_effective_leverage = 2.0
```

## Effective leverage formula

```text
effective_leverage = position_notional_usdt / sizing_equity_usdt
```

## Rule

Reject if:

```text
effective_leverage > max_effective_leverage
```

## Future caps

Future researched caps may include:

```text
3x
5x
10x
```

but these are not approved for initial live.

## Requirements before leverage cap increase

Before increasing beyond 2x, require:

- execution reliability evidence,
- stop placement/replacement reliability,
- reconciliation reliability,
- cost sensitivity review,
- liquidation-safety review,
- operator approval,
- release note,
- and updated configuration.

## Higher leverage note

Higher leverage may help reach desired risk size, but it creates larger notional exposure, higher fee impact, and potentially tighter liquidation constraints.

---

## Environment-Specific Exposure Policy

## Development

Development environment must not create real exposure.

Recommended:

```text
live_trading_enabled = false
max_live_notional_usdt = 0
```

Allowed:

- fake adapter,
- local tests,
- static fixtures,
- dry-run simulation.

Forbidden:

- production credentials,
- real Binance live orders,
- real capital exposure.

## Validation / Research

Validation is simulated and dataset-driven.

Allowed:

- backtests,
- parameter sweeps,
- walk-forward tests,
- simulated notional/risk.

Forbidden:

- live order placement,
- production trade credentials,
- treating research exposure as live approval.

## Paper / Shadow

Paper/shadow may use:

- fake adapter,
- dry-run mode,
- testnet where approved,
- live market data without real orders,
- simulated execution tracking.

Real capital exposure:

```text
false
```

## Tiny Live

Tiny live is first real-capital exposure.

Recommended starting policy:

```text
allowed_live_symbols = ["BTCUSDT"]
max_open_positions = 1
risk_fraction = 0.0025
max_effective_leverage = 2.0
max_position_notional_usdt = explicit small cap
manual_exposure_allowed = false
```

The exact notional cap must be explicitly configured before tiny live.

## Early Scaled Live

Early scaled live may increase:

- risk fraction,
- notional cap,
- possibly leverage cap.

But only after review.

One-symbol and one-position restrictions should remain unless explicitly changed.

## Mature Live

Mature live may consider broader exposure only after a separate architecture and risk review.

Multi-symbol or portfolio exposure is not v1 behavior.

---

## Manual and Non-Bot Exposure Policy

## Core rule

Manual or non-bot exposure in the same Binance futures account blocks new bot entries.

## Detection examples

The bot may detect:

- open position with no Prometheus trade reference,
- open order with no recognized client order ID prefix,
- protective or algo order not linked to active trade,
- position on a non-approved symbol,
- order from another tool or manual session.

## Required response

When detected:

```text
block new entries
raise operator-visible alert
require reconciliation
require operator review
```

## Operator behavior

The operator should not place manual Binance futures trades in the same account while Prometheus is active.

If manual intervention is required, it should occur through approved recovery/emergency workflows where possible.

## Mixed-use accounts

Mixed-use futures accounts are not supported for v1 live operation.

Future support would require a separate account-scoping and reconciliation design.

---

## Exposure Gate Checks

Before a new entry can proceed, exposure control must check the following.

| Gate | Reject if |
|---|---|
| Symbol gate | Symbol is not in live allowlist |
| Venue gate | Venue is not approved Binance USDⓈ-M futures |
| Position gate | Existing position exists |
| Pending order gate | Entry order is in flight |
| Unknown state gate | Unknown order/position/protection status exists |
| Notional gate | Proposed notional exceeds internal cap |
| Leverage gate | Proposed effective leverage exceeds cap |
| Account mode gate | Account is not one-way mode |
| Margin mode gate | Symbol is not isolated margin |
| Protection gate | Existing position lacks confirmed protection |
| Runtime gate | Safe mode, pause, kill switch, or blocking incident active |
| Reconciliation gate | Reconciliation required or unsafe mismatch exists |
| Manual exposure gate | Non-bot exposure or unclassified order exists |
| Config gate | Required exposure config missing |
| Metadata gate | Required symbol/account metadata unavailable |

---

## Exposure Approval Output

A successful exposure check should produce a structured approval object.

Recommended fields:

```text
ExposureApproval:
  approved: true
  symbol
  side
  requested_quantity
  requested_notional_usdt
  projected_total_strategy_notional_usdt
  projected_effective_leverage
  max_position_notional_usdt
  max_effective_leverage
  max_total_open_positions
  max_open_positions_per_symbol
  existing_position_count
  pending_entry_count
  unknown_order_count
  non_strategy_exposure_present
  account_mode
  margin_mode
  config_version
  strategy_version
  approved_at_utc_ms
```

## Exposure Rejection Output

A rejected exposure check should produce a structured rejection object.

Recommended fields:

```text
ExposureRejection:
  approved: false
  symbol
  side
  rejection_category
  rejection_reason
  failed_gate
  requested_quantity if available
  requested_notional_usdt if available
  current_position_summary
  current_open_order_summary
  current_runtime_mode
  reconciliation_state
  protection_state
  config_version
  strategy_version
  rejected_at_utc_ms
```

---

## Rejection Categories

Recommended rejection categories:

```text
SYMBOL_NOT_ALLOWED
VENUE_NOT_ALLOWED
EXISTING_POSITION
MAX_POSITIONS_REACHED
PYRAMIDING_NOT_ALLOWED
REVERSAL_NOT_ALLOWED
ENTRY_IN_FLIGHT
UNKNOWN_EXECUTION_STATUS
UNEXPECTED_OPEN_ORDER
UNEXPECTED_POSITION
NON_STRATEGY_EXPOSURE
NOTIONAL_CAP_EXCEEDED
LEVERAGE_CAP_EXCEEDED
ACCOUNT_MODE_INVALID
MARGIN_MODE_INVALID
PROTECTION_UNCERTAIN
POSITION_UNPROTECTED
RECONCILIATION_REQUIRED
UNSAFE_MISMATCH
SAFE_MODE_ACTIVE
KILL_SWITCH_ACTIVE
OPERATOR_PAUSE_ACTIVE
INCIDENT_BLOCK_ACTIVE
CONFIG_MISSING_EXPOSURE_CAP
METADATA_UNAVAILABLE
UNKNOWN_EXPOSURE_ERROR
```

Each rejection must include a human-readable explanation.

---

## Event Contract Expectations

Exposure checks should communicate through internal command/event contracts.

## Input

Exposure layer may consume:

- approved risk sizing result,
- runtime state summary,
- reconciliation state,
- current exchange position summary,
- current open order summary,
- protection state,
- config version,
- symbol metadata reference.

## Approval event

Recommended:

```text
risk.exposure_approved
```

Minimum payload:

- symbol,
- side,
- approved quantity,
- projected notional,
- projected effective leverage,
- max caps,
- config version.

## Rejection event

Recommended:

```text
risk.exposure_rejected
```

Minimum payload:

- rejection category,
- rejection reason,
- failed gate,
- current exposure summary,
- config version.

---

## Runtime State Interaction

Exposure limits must respect runtime state.

## Block new entries if runtime mode is

- `SAFE_MODE`
- `RECOVERING`
- `BLOCKED_AWAITING_OPERATOR`

## Block new entries if flags include

- `incident_active` with blocking severity,
- `kill_switch_active`,
- `paused_by_operator`,
- `operator_review_required`,
- `entries_blocked`.

## Reconciliation state

Block new entries if reconciliation state is:

- `REQUIRED`
- `IN_PROGRESS`
- `RECOVERABLE_MISMATCH` not yet repaired/rechecked
- `REPAIRED_PENDING_RECHECK`
- `UNSAFE_MISMATCH`

## Protection state

Block new entries if protection state is:

- `POSITION_UNCONFIRMED`
- `POSITION_UNPROTECTED`
- `STOP_PENDING_CONFIRMATION`
- `STOP_REPLACEMENT_IN_PROGRESS`
- `PROTECTION_UNCERTAIN`
- `EMERGENCY_UNPROTECTED`

If no position exists and protection state is `NO_POSITION`, exposure may proceed only if other gates pass.

---

## Existing Position Behavior

If a strategy-owned position exists and is protected:

- do not open new entry,
- continue position management,
- allow approved stop updates,
- allow approved exit actions,
- monitor protection state,
- block unrelated new exposure.

If a strategy-owned position exists and is not protected:

- block all new entries,
- enter incident/emergency path,
- restore protection or flatten according to incident policy.

If a non-strategy position exists:

- block all new entries,
- require operator review,
- do not attempt to manage it as if strategy-owned unless emergency policy explicitly says so.

---

## Open Order Behavior

## Expected open orders when flat

When flat, expected strategy-owned open orders:

```text
0
```

If open strategy orders exist while flat:

```text
block new entries
reconcile or cancel if safe
```

## Expected open orders when position exists

When a strategy-owned position exists, expected open orders:

```text
1 active protective stop
0 active entry orders
```

Other order types may exist only if an approved exit or stop-replacement workflow is in progress.

## Unexpected open orders

Unexpected open orders require:

- classification,
- reconciliation,
- cancellation if safe,
- operator review if ambiguous.

---

## Configuration Requirements

Recommended exposure configuration:

```yaml
allowed_live_symbols:
  - BTCUSDT

max_total_open_positions: 1
max_open_positions_per_symbol: 1
allow_pyramiding: false
allow_reversal_entry: false
allow_hedge_mode: false
require_isolated_margin: true
manual_exposure_allowed: false

max_position_notional_usdt: null  # must be set before live
max_effective_leverage: 2.0

block_on_unknown_order_status: true
block_on_non_strategy_exposure: true
block_on_unexpected_open_order: true
block_on_reconciliation_required: true
```

Live startup must reject or block trading if required live exposure settings are missing.

---

## Observability Requirements

Exposure-limit state must be visible to the operator.

Required status fields:

- allowed live symbols,
- current symbol exposure,
- current position count,
- current pending entry count,
- current open strategy order count,
- current non-strategy exposure flag,
- max notional cap,
- current/projected notional,
- max effective leverage,
- current/projected effective leverage,
- entries blocked by exposure yes/no,
- exposure rejection reason if applicable,
- last exposure check time.

Required alerts:

- existing position blocks entry,
- pending order blocks entry,
- unknown order status,
- unexpected open order,
- unexpected position,
- non-strategy exposure,
- notional cap exceeded,
- leverage cap exceeded,
- missing protective stop,
- manual exposure detected.

---

## Testing Requirements

Implementation must include tests for the following.

## Symbol tests

- BTCUSDT live candidate passes symbol gate,
- ETHUSDT live candidate rejects,
- unknown symbol rejects,
- research-only symbol cannot live-trade.

## Position tests

- flat state permits entry if other gates pass,
- existing BTCUSDT position blocks new entry,
- same-direction entry rejects,
- opposite-direction entry rejects,
- non-strategy position blocks entry.

## Pending order tests

- entry submitted blocks new entry,
- unknown execution status blocks new entry,
- stale open entry order blocks new entry,
- partially filled entry order blocks new entry.

## Protective state tests

- protected existing position still blocks new entry,
- unprotected position triggers emergency/block,
- multiple protective stops block and require reconciliation,
- orphaned protective stop while flat blocks/requires cleanup.

## Notional/leverage tests

- proposed notional under cap passes,
- proposed notional over cap rejects,
- missing cap rejects live entry,
- effective leverage over cap rejects,
- future cap config is visible and tested.

## Manual exposure tests

- manual open position blocks,
- manual open order blocks,
- unrecognized client ID blocks,
- mixed-use account rejects under v1 policy.

## Runtime state tests

- safe mode blocks,
- kill switch blocks,
- pause blocks,
- reconciliation required blocks,
- unsafe mismatch blocks,
- operator review required blocks.

---

## V1 Non-Goals

The exposure-limit framework does not support:

- multi-symbol live portfolios,
- simultaneous BTCUSDT and ETHUSDT live positions,
- pyramiding,
- grid exposure,
- martingale exposure expansion,
- hedge-mode long/short coexistence,
- manual trade coexistence in same futures account,
- account-wide portfolio margin optimization,
- automatic risk escalation after wins,
- automatic leverage increases,
- discretionary manual exposure overrides.

These may be researched later but are not v1 behavior.

---

## Open Questions

The following should be resolved before paper/shadow or tiny live.

## 1. Exact tiny-live notional cap

The cap must be set before live.

This document requires the cap but does not choose the numeric amount.

## 2. Account dedication policy

The recommendation is a clean futures account for v1 operation.

If the account is shared with manual trading or other bots later, a new account-scoping design is required.

## 3. Non-strategy exposure handling

The default is block and operator review.

Future policy may define whether the bot should ever flatten non-strategy exposure in emergencies.

## 4. Future multi-symbol exposure model

Not v1.

If ETHUSDT becomes live later, exposure limits must be redesigned for portfolio and correlation control.

## 5. Future leverage cap increases

The framework allows future research toward 5x or 10x caps, but approval criteria should be linked to phase gates.

---

## Acceptance Criteria

This exposure-limit framework is satisfied when implementation can demonstrate:

- BTCUSDT is the only live-allowed v1 symbol,
- ETHUSDT is research-only,
- max live positions is one,
- pyramiding is rejected,
- reversal entries while positioned are rejected,
- hedge-mode behavior is rejected,
- isolated margin is required,
- pending entry orders block new entries,
- unknown order status blocks new entries,
- manual/non-bot exposure blocks new entries,
- missing protective stop triggers emergency/blocking behavior,
- internal notional cap is mandatory for live,
- effective leverage cap is enforced,
- missing exposure configuration rejects live trading,
- exposure approvals/rejections are structured,
- and exposure state is visible to the operator.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Risk exposure-limit contract
