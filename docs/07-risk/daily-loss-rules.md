# Daily Loss Rules

## Purpose

This document defines the daily loss rules for the v1 Prometheus trading system.

Its purpose is to define when the bot must stop opening new trades for the current daily session because realized losses, loss clustering, or abnormal loss behavior has crossed a safety boundary.

The position-sizing framework controls:

> How much risk is allowed on one trade?

The exposure-limits framework controls:

> Is the system allowed to hold or add exposure?

This daily-loss-rules document controls:

> Has the current daily session already taken enough damage that the bot must stop opening new trades?

This document replaces the previous TBD placeholder for:

```text
docs/07-risk/daily-loss-rules.md
```

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures
- first live symbol: BTCUSDT perpetual
- v1 live scope: one symbol
- v1 live position limit: one position
- position mode: one-way mode
- margin mode: isolated margin
- initial live risk per trade: 0.25% of sizing equity
- first future risk target: up to 1.00% only after staged validation
- deployment model: supervised staged rollout
- runtime begins in safe mode after restart
- exchange state is authoritative
- all canonical timestamps are UTC Unix milliseconds

This document covers:

- daily session definition,
- daily realized PnL tracking,
- loss-streak tracking,
- daily warning thresholds,
- daily entry lockout thresholds,
- hard review thresholds,
- reset behavior,
- override behavior,
- interaction with open positions,
- interaction with kill switch and incidents,
- observability requirements,
- event expectations,
- testing requirements,
- and future risk-scaling behavior.

This document does **not** define:

- position-sizing formula,
- maximum exposure formula,
- stop-loss mechanics,
- kill-switch mechanics,
- longer-term drawdown controls,
- release rollback procedure,
- final dashboard design,
- or final paper/tiny-live runbook steps.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/kill-switches.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/operator-workflow.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/daily-weekly-review-process.md`
- `docs/09-operations/release-process.md`

### Authority hierarchy

If this document conflicts with the state model on runtime mode behavior, the state model wins.

If this document conflicts with incident response on severity and emergency escalation, incident response wins.

If this document conflicts with kill-switch clearance rules, the kill-switch document wins.

If this document conflicts with position sizing, the position-sizing framework wins for per-trade sizing.

---

## Core Principles

## 1. Daily loss rules are discipline controls

Daily loss rules exist to prevent repeated losses in one daily session from becoming uncontrolled behavior.

They are not intended to optimize the strategy.

They are intended to enforce a stop-trading boundary.

## 2. Normal losing trades are not system failures

A strategy can take consecutive losses even when everything is working correctly.

Daily loss lockout should not automatically imply the bot is broken.

If losses occurred through normal valid trades and stops, the correct response may be a daily entry lockout rather than a kill switch.

## 3. Abnormal losses are different

If losses are connected to:

- missing protective stop,
- duplicate entry,
- unknown execution status,
- excessive slippage,
- reconciliation failure,
- manual/non-bot exposure,
- credential/security issue,
- or protection uncertainty,

then the system should escalate through incident and possibly kill-switch policy.

## 4. Daily reset does not clear safety problems

A new UTC day may reset daily counters.

It must not clear:

- active kill switch,
- unresolved incident,
- reconciliation requirement,
- operator pause,
- unprotected position,
- or blocked-awaiting-operator state.

## 5. Missing loss state fails closed

If the bot cannot determine the current daily loss state during live operation, it must block new entries until state confidence is restored.

## 6. Loss limits are stage-specific

Tiny live uses conservative limits.

Future risk increases toward 1% per trade require revisiting daily loss thresholds at the same time.

---

## Daily Session Definition

## Canonical daily window

The daily loss window is the UTC calendar day.

```text
daily_session_start = 00:00:00 UTC
daily_session_end = 23:59:59.999 UTC
```

## Why UTC

The project uses UTC Unix milliseconds as canonical time.

Using UTC avoids:

- local timezone ambiguity,
- daylight-saving issues,
- inconsistent backtest/live alignment,
- and operator-location dependency.

## Local display

The dashboard may show local time for operator convenience, but canonical daily loss logic must use UTC.

---

## What Counts Toward Daily Loss

## Included in daily realized PnL

Daily realized PnL should include:

- realized trade PnL from closed Prometheus trades,
- entry fees,
- exit fees,
- funding payments/receipts once realized,
- realized emergency-flatten losses,
- realized losses from bot-related recovery actions,
- known slippage and execution friction where captured.

## Tracked separately

The system should track separately:

- open unrealized PnL,
- current trade unrealized loss,
- worst-case remaining loss to stop,
- fees accrued on currently open position,
- expected but unrealized funding impact,
- abnormal execution loss notes.

## Excluded from bot daily loss

The following should not be included in Prometheus daily loss counters:

- unrelated manual trades,
- unrelated deposits,
- withdrawals,
- transfers,
- exchange bonuses,
- account adjustments not tied to strategy activity.

However, unrelated manual exposure should block new bot entries under exposure-limit policy.

## Emergency/manual actions

If the operator performs a bot-related emergency action, such as emergency flattening, its realized PnL impact should be included in the daily review and preferably in the bot-related daily loss record.

---

## Daily Loss Measures

The system should track multiple daily loss measures.

## 1. Realized daily PnL

Closed-trade PnL after known costs.

Recommended field:

```text
daily_realized_pnl_usdt
```

## 2. Realized daily PnL fraction

Realized daily PnL as a fraction of sizing equity or configured daily reference equity.

Recommended field:

```text
daily_realized_pnl_fraction
```

## 3. Consecutive losing trades today

Number of consecutive closed losing Prometheus trades in the current UTC day.

Recommended field:

```text
consecutive_losing_trades_today
```

## 4. Full-risk stopped trades today

Number of trades that realized approximately one full planned risk loss.

Recommended field:

```text
full_risk_losses_today
```

## 5. Daily risk consumed

Approximate amount of planned risk consumed by closed losses.

Recommended field:

```text
daily_risk_consumed_fraction
```

## 6. Worst open-risk state

If a position is open, track current remaining worst-case stop risk.

Recommended field:

```text
open_position_remaining_risk_fraction
```

---

## Tiny-Live Daily Loss Policy

The initial live stage is tiny live.

Starting risk per trade:

```text
risk_fraction = 0.0025
```

Equivalent:

```text
0.25% of sizing equity
```

## Daily warning threshold

Tiny-live warning threshold:

```text
daily_realized_pnl_fraction <= -0.0050
```

Equivalent:

```text
-0.50%
```

Meaning:

- alert operator,
- continue only if other gates allow,
- increase supervision,
- record warning in daily review.

## Daily entry lockout threshold

Tiny-live daily entry lockout triggers when either condition is met:

```text
daily_realized_pnl_fraction <= -0.0075
```

Equivalent:

```text
-0.75%
```

or:

```text
full_risk_losses_today >= 3
```

Meaning:

- no new entries for the rest of the UTC daily session,
- existing protected position may continue safety management,
- operator-visible status must show daily lockout,
- daily review must include the event.

## Hard daily review threshold

Tiny-live hard review threshold:

```text
daily_realized_pnl_fraction <= -0.0100
```

Equivalent:

```text
-1.00%
```

Hard review should also trigger if losses involve abnormal behavior, even if the numeric loss is smaller.

Examples:

- stop missing,
- stop rejected,
- duplicate entry,
- unexpected manual exposure,
- unknown execution status,
- excessive slippage,
- reconciliation mismatch,
- stream/state failure while exposed.

## Why three full-risk losses

Two consecutive losing trades can easily happen in normal trading.

Three full-risk losses gives the strategy more realistic breathing room while still preventing an undisciplined loss spiral.

At 0.25% initial risk, three full-risk losses is approximately:

```text
3 * 0.25% = 0.75%
```

This aligns the full-risk loss count with the daily entry lockout threshold.

---

## Future Risk-Scaling Policy

The project may work toward 1% live risk over time.

Daily loss rules must be reviewed alongside any risk increase.

## Suggested future stage framework

| Stage | Risk per trade | Daily warning | Daily entry lockout | Hard review |
|---|---:|---:|---:|---:|
| Tiny live | 0.25% | -0.50% | -0.75% or 3 full-risk losses | -1.00% |
| Early scaled | 0.50% | -1.00% | -1.50% or 3 full-risk losses | -2.00% |
| Mature reviewed | 0.75% | -1.50% | -2.25% or 3 full-risk losses | -3.00% |
| Max reviewed target | 1.00% | -2.00% | -3.00% or 3 full-risk losses | -4.00% |

## Important note

These future thresholds are not live approval.

They are a framework for future review.

Increasing risk per trade requires:

- validation evidence,
- paper/shadow review,
- tiny-live stability,
- release approval,
- daily loss threshold review,
- operator approval,
- config version change.

## Do not increase risk automatically

Daily loss rules must not include automatic risk increases after wins or reductions after losses unless a future risk policy explicitly approves it.

For v1:

```text
no automatic risk escalation
no revenge sizing
no martingale behavior
```

---

## Daily Lockout Behavior

## Entry lockout effects

When daily entry lockout activates:

```text
daily_loss_lockout_active = true
entries_blocked = true
```

The runtime should:

- block new entries,
- preserve existing protective stops,
- allow controlled exits,
- allow risk-reducing stop updates if approved,
- allow reconciliation and recovery,
- record the lockout event,
- show operator-visible reason.

## Runtime mode

A normal daily entry lockout does not necessarily require kill switch.

If all trades were valid and system state is clean, the runtime may remain in a controlled blocked state rather than emergency mode.

Recommended state behavior:

```text
entries_blocked = true
operator_review_required = stage-dependent
runtime_mode may remain SAFE_MODE or controlled blocked state depending on implementation
```

## Existing protected position

Daily lockout should not automatically flatten an existing valid protected position.

The position may continue to be managed for safety and approved exits.

## Existing unprotected position

If daily loss lockout occurs while a position is unprotected:

- incident policy takes over,
- kill-switch/emergency policy may activate,
- stop restoration or flattening should be considered.

## New entries

No new entry may be submitted while daily lockout is active.

---

## Daily Warning Behavior

When daily warning threshold is reached:

```text
daily_loss_warning_active = true
```

The system should:

- alert operator,
- record warning event,
- increase visibility,
- continue only if all other gates permit.

Daily warning does not necessarily block new entries.

However, paper/tiny-live configuration may choose to block entries at warning if the operator wants stricter behavior.

---

## Hard Review Behavior

Hard review activates when:

- daily loss exceeds hard review threshold,
- abnormal loss condition occurs,
- loss occurs with execution/protection uncertainty,
- or repeated daily lockouts occur within a review period.

Effects:

```text
daily_hard_review_required = true
entries_blocked = true
operator_review_required = true
```

Hard review should not automatically clear at UTC reset unless configured and reviewed.

If hard review is caused by abnormal behavior, incident/kill-switch policy may apply.

---

## Escalation to Incident or Kill Switch

## Normal loss lockout

A normal sequence of valid losing trades should generally cause:

```text
DAILY_ENTRY_LOCKOUT
```

not necessarily kill switch.

## Escalate if abnormal

Escalate to incident and possibly kill switch if daily loss involves:

- missing protective stop,
- unknown execution outcome,
- duplicate entry,
- unrecognized position,
- unrecognized order,
- stop replacement failure,
- excessive slippage outside expected assumptions,
- reconciliation mismatch,
- stale user stream while exposed,
- security/credential anomaly,
- manual intervention outside policy.

## Severity guidance

- Normal valid losses: operational lockout / review.
- Loss with degraded but contained behavior: severity 2 or 3 depending on context.
- Loss with unprotected exposure or unknown execution: severity 4.

---

## Daily Reset Policy

## Reset time

Daily counters reset at:

```text
00:00 UTC
```

## Counters that reset

At reset, the system may reset:

- daily realized PnL,
- daily trade count,
- consecutive losing trades today,
- full-risk losses today,
- daily warning flag,
- daily entry lockout flag if allowed by config.

## Conditions required for clean reset

Daily reset must not resume trading if any of the following remain active:

- kill switch,
- active blocking incident,
- operator pause,
- reconciliation required,
- unsafe mismatch,
- unprotected position,
- unknown execution status,
- hard review that requires manual clearance.

## Reset is not forgiveness

A new UTC day does not make an unsafe system safe.

It only resets daily counters if other safety states are clean.

---

## Operator Override Policy

## Core rule

Daily lockout should not be casually overridden.

## Tiny-live rule

During tiny live:

```text
daily entry lockout should not be cleared intraday except for configuration/test error or explicitly reviewed exceptional case
```

## Override requirements

If operator override is allowed by stage/config, it requires:

- explicit operator action,
- reason/note,
- no active kill switch,
- no unprotected position,
- clean reconciliation,
- no unknown execution status,
- no unresolved severe incident,
- visible current daily loss state,
- event logged and persisted.

## Discouraged behavior

The operator should not clear a daily lockout simply because:

- the next setup looks good,
- the market feels favorable,
- losses feel recoverable,
- the operator wants to “make it back.”

That would undermine the purpose of the rule.

---

## Missing or Stale Daily Loss State

If daily loss state is missing, corrupt, stale, or cannot be computed:

```text
block new entries
raise operator-visible warning
require state repair or reconciliation
```

## Examples

- daily PnL store unavailable,
- trade history incomplete,
- fill/fee data missing,
- unknown position closure,
- reconciliation mismatch affects realized PnL,
- funding/fee data unavailable for closed trade.

## Fail-closed rule

Live trading must not continue when the system cannot know whether daily loss limits have already been breached.

---

## Persistence Requirements

Daily loss state should be persisted because it affects trading permission.

Minimum persisted daily loss record:

```text
session_date_utc
session_start_utc_ms
session_end_utc_ms
daily_realized_pnl_usdt
daily_realized_pnl_fraction
daily_trade_count
daily_losing_trade_count
consecutive_losing_trades_today
full_risk_losses_today
daily_risk_consumed_fraction
daily_warning_active
daily_loss_lockout_active
daily_hard_review_required
lockout_reason
hard_review_reason
updated_at_utc_ms
```

## Operator action record

If daily lockout is overridden or manually reviewed, persist:

```text
operator_identity_or_alias
action_type
reason
occurred_at_utc_ms
resulting_state
```

## Restart behavior

On restart, the bot must reload current UTC day loss state before allowing new entries.

If unavailable:

```text
block entries
```

---

## Event Contract Expectations

Recommended events:

```text
daily_loss.session_started
daily_loss.trade_recorded
daily_loss.warning_triggered
daily_loss.lockout_triggered
daily_loss.hard_review_triggered
daily_loss.reset_completed
daily_loss.reset_blocked
daily_loss.override_requested
daily_loss.override_approved
daily_loss.override_rejected
daily_loss.state_unavailable
```

## Warning event payload

Minimum payload:

```text
session_date_utc
daily_realized_pnl_usdt
daily_realized_pnl_fraction
threshold
trade_count
full_risk_losses_today
occurred_at_utc_ms
```

## Lockout event payload

Minimum payload:

```text
session_date_utc
lockout_reason
daily_realized_pnl_usdt
daily_realized_pnl_fraction
full_risk_losses_today
threshold
entries_blocked
operator_review_required
occurred_at_utc_ms
```

## Reset event payload

Minimum payload:

```text
previous_session_date_utc
new_session_date_utc
reset_allowed
blocked_reason if any
occurred_at_utc_ms
```

---

## Operator Visibility Requirements

The operator dashboard should show:

```text
current UTC daily session
daily realized PnL
daily realized PnL %
daily warning active yes/no
daily lockout active yes/no
daily hard review required yes/no
daily trade count
daily losing trade count
consecutive losses today
full-risk losses today
daily reset time
entries blocked by daily loss yes/no
lockout reason
override allowed yes/no
override blocked reason
```

## Required alerts

Alerts should occur when:

- daily warning threshold reached,
- daily lockout threshold reached,
- hard review threshold reached,
- daily loss state unavailable,
- lockout reset blocked,
- override requested,
- override approved/rejected.

---

## Implementation Boundaries

## Risk layer owns

- checking daily loss gate before entry approval,
- rejecting entries when lockout is active,
- producing rejection categories.

## Persistence layer owns

- storing daily loss state,
- restoring it on restart,
- preserving operator actions.

## Observability layer owns

- daily loss events,
- alerts,
- dashboard summaries.

## Execution layer does not own

- daily loss thresholds,
- daily lockout clearance,
- override approval.

## Strategy layer does not own

- daily loss lockout,
- daily loss override,
- risk reset behavior.

## Operator layer owns

- review/override request path,
- reason capture,
- visible control flow.

---

## Rejection Categories

Recommended rejection categories:

```text
DAILY_LOSS_WARNING_ACTIVE
DAILY_LOSS_LOCKOUT_ACTIVE
DAILY_MAX_FULL_RISK_LOSSES_REACHED
DAILY_HARD_REVIEW_REQUIRED
DAILY_LOSS_STATE_UNAVAILABLE
DAILY_LOSS_COUNTER_STALE
DAILY_RESET_BLOCKED
DAILY_OVERRIDE_REQUIRED
```

A warning alone does not necessarily reject entries unless configured to do so.

Lockout and hard review must reject entries.

---

## Testing Requirements

Implementation must include tests for the following.

## Session tests

- UTC daily session boundary,
- reset at 00:00 UTC,
- local timezone does not affect logic,
- reset blocked by active kill switch,
- reset blocked by unresolved incident.

## PnL tests

- realized trade loss updates daily PnL,
- fees included,
- funding included once realized,
- open unrealized PnL tracked separately,
- unrelated manual trade excluded from bot PnL.

## Threshold tests

- tiny-live warning at -0.50%,
- tiny-live lockout at -0.75%,
- tiny-live lockout at 3 full-risk losses,
- hard review at -1.00%,
- warning does not necessarily block,
- lockout blocks entries,
- hard review blocks entries.

## Override tests

- lockout does not auto-clear intraday,
- override requires operator reason,
- override blocked with active kill switch,
- override blocked with unprotected position,
- override blocked with reconciliation required,
- override event persisted.

## Restart tests

- daily loss state restored on restart,
- missing state blocks entries,
- stale state blocks entries,
- reset state does not clear kill switch.

## Escalation tests

- normal losing trades create lockout only,
- missing stop loss escalates incident,
- unknown execution loss escalates incident,
- manual exposure loss escalates/blocking behavior.

---

## V1 Non-Goals

The daily loss rules do not include:

- automatic risk reduction after losses,
- automatic risk increase after wins,
- martingale recovery,
- revenge-trade mode,
- discretionary “one more trade” behavior,
- portfolio-level daily VaR,
- multi-symbol daily allocation,
- account-wide discretionary PnL management,
- tax/accounting reporting.

These may be considered later but are not v1 behavior.

---

## Open Questions

The following should be resolved before paper/shadow or tiny live.

## 1. Exact sizing equity reference for daily percentage

The daily percentage should likely use the same sizing equity reference as risk sizing, but implementation must define this exactly.

## 2. How to classify partial losses

A “full-risk loss” threshold needs a tolerance.

Example:

```text
loss >= 0.80R may count as full-risk loss
```

Exact value should be configured.

## 3. Daily hard review persistence

Decide whether hard review persists beyond UTC reset by default.

Recommended: yes during tiny live if caused by abnormal behavior.

## 4. Operator override permissions

Define which operator role may override daily lockout, if any.

## 5. Future scaled-live thresholds

The framework suggests thresholds but final numbers require validation and operator approval.

---

## Acceptance Criteria

This daily-loss-rules policy is satisfied when implementation can demonstrate:

- daily session uses UTC calendar day,
- tiny-live warning triggers around -0.50%,
- tiny-live entry lockout triggers around -0.75%,
- tiny-live entry lockout also triggers after 3 full-risk losses,
- hard review triggers around -1.00% or abnormal loss behavior,
- daily lockout blocks new entries,
- daily lockout does not automatically flatten valid protected positions,
- abnormal loss escalates to incident/kill-switch policy,
- daily reset does not clear kill switch or unresolved incidents,
- operator override is discouraged and controlled,
- missing/stale daily loss state blocks entries,
- daily loss state persists across restart,
- and operator dashboard shows daily loss status clearly.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Risk daily loss lockout policy
