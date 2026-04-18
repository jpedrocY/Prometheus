# Drawdown Controls

## Purpose

This document defines the drawdown-control framework for the v1 Prometheus trading system.

Its purpose is to define when longer-term equity deterioration requires increased caution, new-entry pause, formal review, or incident escalation.

Daily loss rules answer:

> Has today already taken too much damage?

Drawdown controls answer:

> Has the strategy/system lost enough from a recent or deployment high watermark that the bot should reduce activity, pause, review, or block scaling?

This document replaces the previous TBD placeholder for:

```text
docs/07-risk/drawdown-controls.md
```

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures
- first live symbol: BTCUSDT perpetual
- first research comparison symbol: ETHUSDT perpetual
- v1 live scope: one symbol
- v1 live position limit: one position
- position mode: one-way mode
- margin mode: isolated margin
- initial live risk per trade: 0.25% of sizing equity
- first future live-risk target: up to 1.00% only after staged validation
- initial effective leverage cap: 2x
- future leverage caps such as 5x or 10x may be researched later
- deployment model: supervised staged rollout
- runtime begins in safe mode after restart
- exchange state is authoritative
- all canonical timestamps are UTC Unix milliseconds

This document covers:

- drawdown definitions,
- high-watermark tracking,
- drawdown state categories,
- tiny-live drawdown thresholds,
- future risk-scaling implications,
- interaction with daily loss rules,
- interaction with kill switch and incidents,
- drawdown pause behavior,
- clearing and review requirements,
- persistence requirements,
- observability requirements,
- event expectations,
- testing requirements,
- and non-goals.

This document does **not** define:

- per-trade position-sizing formula,
- daily loss lockout thresholds,
- stop-loss mechanics,
- kill-switch mechanics,
- exchange order behavior,
- full portfolio-level risk,
- tax/accounting reporting,
- final production scaling limits,
- or final live runbook procedures.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/kill-switches.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/operator-workflow.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/daily-weekly-review-process.md`
- `docs/09-operations/release-process.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`

### Authority hierarchy

If this document conflicts with incident response on severity and emergency escalation, incident response wins.

If this document conflicts with the state model on runtime mode behavior, the state model wins.

If this document conflicts with daily-loss rules for same-day lockout behavior, daily-loss rules win for same-day limits.

If this document conflicts with position sizing, the position-sizing framework wins for per-trade sizing.

---

## Core Principles

## 1. Drawdown controls are longer-term discipline controls

Drawdown controls exist to prevent slow or repeated losses from becoming normalized.

They are not intended to prevent every losing streak.

They are intended to force review when strategy equity declines enough to challenge current operating assumptions.

## 2. Drawdown is separate from daily loss

Daily loss rules focus on one UTC daily session.

Drawdown controls focus on peak-to-current deterioration across days, weeks, or deployment stages.

Both can block new entries.

## 3. Normal drawdown is not automatically a system failure

A strategy can experience drawdown even when:

- signals are valid,
- stops are working,
- execution is clean,
- reconciliation is clean,
- and the system is behaving as designed.

In that case, the correct response may be caution or pause, not an emergency kill switch.

## 4. Abnormal drawdown is different

Drawdown caused by abnormal execution, unprotected exposure, unknown order state, or reconciliation failure must escalate through incident and kill-switch policy.

## 5. Risk increases are forbidden during active drawdown controls

The bot must not increase risk while in drawdown caution, drawdown pause, or hard review.

Increasing risk after losses without review is not allowed.

## 6. Missing drawdown state fails closed

If the bot cannot determine drawdown state during live operation, it must block new entries until state confidence is restored.

## 7. Drawdown controls must survive restart

Drawdown state affects trading permission and must be persisted.

A restart must not erase drawdown pause or hard review state.

---

## Key Definitions

## Strategy equity

The equity value assigned to Prometheus strategy performance tracking.

This should be based on the strategy-allocated equity model rather than blindly using the full Binance futures account.

## Strategy allocated equity

The amount of capital allocated to the Prometheus strategy.

This is also used by position sizing as the strategy risk boundary.

## Strategy equity high watermark

The highest recorded strategy equity since the relevant tracking period began.

Recommended field:

```text
strategy_equity_high_watermark_usdt
```

## Current strategy equity

The current strategy equity after realized and, where applicable, mark-to-market changes.

Recommended field:

```text
current_strategy_equity_usdt
```

## Drawdown fraction

Recommended formula:

```text
drawdown_fraction =
  (current_strategy_equity_usdt - strategy_equity_high_watermark_usdt)
  / strategy_equity_high_watermark_usdt
```

This value is negative during drawdown.

## Realized drawdown

Drawdown calculated from closed-trade realized PnL only.

## Mark-to-market drawdown

Drawdown including open unrealized PnL.

## Deployment drawdown

Drawdown measured since a specific deployment stage began, such as paper/shadow or tiny live.

## Weekly drawdown

Drawdown measured within the current active review week.

---

## Drawdown Measures to Track

The system should track multiple drawdown measures.

## 1. Strategy equity drawdown

Primary governance measure.

```text
strategy_drawdown_fraction
```

This should use strategy equity and strategy equity high watermark.

## 2. Realized drawdown

Useful for clean closed-trade analysis.

```text
realized_drawdown_fraction
```

## 3. Mark-to-market drawdown

Useful during open positions.

```text
mark_to_market_drawdown_fraction
```

## 4. Max drawdown since deployment

Useful for evaluating the current release or rollout stage.

```text
max_drawdown_fraction_since_deployment
```

## 5. Current week max drawdown

Useful for weekly review.

```text
max_drawdown_fraction_current_week
```

## 6. Peak-to-valley trade drawdown

Useful for comparing live pain profile against backtest expectations.

```text
peak_to_valley_trade_drawdown_fraction
```

---

## High-Watermark Policy

## Updating the high watermark

The high watermark updates only when strategy equity reaches a new high.

```text
if current_strategy_equity > strategy_equity_high_watermark:
    strategy_equity_high_watermark = current_strategy_equity
```

## Manual reset

The high watermark must not be manually reset casually.

Manual reset may be allowed only for:

- new strategy deployment stage,
- formal capital allocation change,
- strategy version reset,
- operator-approved accounting correction,
- or documented release/governance decision.

## Capital deposits and withdrawals

Deposits, withdrawals, and allocation changes must be handled carefully so drawdown is not distorted.

If strategy allocated equity changes, the system should record:

- old allocation,
- new allocation,
- reason,
- operator,
- timestamp,
- whether high watermark was adjusted,
- and adjustment method.

## New deployment

Starting a new deployment stage may create a new deployment-specific high watermark.

This does not erase historical performance records.

---

## Drawdown State Categories

Recommended drawdown states:

```text
DRAWDOWN_NORMAL
DRAWDOWN_WATCH
DRAWDOWN_CAUTION
DRAWDOWN_PAUSE
DRAWDOWN_HARD_REVIEW
DRAWDOWN_ESCALATED_TO_INCIDENT
```

## `DRAWDOWN_NORMAL`

Meaning:

- no drawdown threshold is active,
- normal entry eligibility may proceed if all other gates pass.

## `DRAWDOWN_WATCH`

Meaning:

- drawdown has become noticeable,
- operator should be alerted,
- no automatic entry block is required by default.

## `DRAWDOWN_CAUTION`

Meaning:

- drawdown is significant enough to block risk increases,
- tighter supervision is required,
- new entries may continue only if configured and all other gates pass.

## `DRAWDOWN_PAUSE`

Meaning:

- new entries are blocked pending review,
- existing protected positions may continue safety management,
- operator review is required before resumption.

## `DRAWDOWN_HARD_REVIEW`

Meaning:

- live operation remains blocked until formal review,
- reset or resumption requires stronger evidence and explicit operator decision.

## `DRAWDOWN_ESCALATED_TO_INCIDENT`

Meaning:

- drawdown is tied to abnormal behavior, state uncertainty, protection failure, or security concern,
- incident and possibly kill-switch policy applies.

---

## Tiny-Live Drawdown Policy

Tiny live starts with:

```text
risk_fraction = 0.0025
```

Equivalent:

```text
0.25% of sizing equity per trade
```

## Tiny-live thresholds

Approved tiny-live thresholds:

| Drawdown state | Threshold from strategy equity high watermark | Default action |
|---|---:|---|
| `DRAWDOWN_WATCH` | `-1.0%` | Alert and review trend |
| `DRAWDOWN_CAUTION` | `-1.5%` | Block risk increases; tighten supervision |
| `DRAWDOWN_PAUSE` | `-2.0%` | Pause new entries pending review |
| `DRAWDOWN_HARD_REVIEW` | `-3.0%` | Block live operation until formal review |

## Why these thresholds

At 0.25% risk per trade:

```text
-1.0% ≈ 4 full-risk losses
-1.5% ≈ 6 full-risk losses
-2.0% ≈ 8 full-risk losses
-3.0% ≈ 12 full-risk losses
```

This gives the strategy room for normal loss clustering while still preventing a persistent equity bleed from becoming normalized.

## Emergency escalation

Any drawdown level may escalate to incident or kill switch if drawdown is associated with abnormal behavior.

Examples:

- missing protective stop,
- stop rejected,
- unknown execution outcome,
- duplicate entry,
- unrecognized exposure,
- reconciliation failure,
- severe slippage outside expected assumptions,
- credential or security concern.

---

## Future Risk-Scaling Framework

The project may work toward 1% live risk in the future.

Drawdown controls must scale deliberately and must be reviewed with every risk increase.

## Example future framework

| Stage | Risk per trade | Watch | Caution | Pause | Hard review |
|---|---:|---:|---:|---:|---:|
| Tiny live | 0.25% | -1.0% | -1.5% | -2.0% | -3.0% |
| Early scaled | 0.50% | -2.0% | -3.0% | -4.0% | -6.0% |
| Mature reviewed | 0.75% | -3.0% | -4.5% | -6.0% | -9.0% |
| Max reviewed target | 1.00% | -4.0% | -6.0% | -8.0% | -12.0% |

These future levels are not automatic approval.

They are a planning framework for later review.

## Risk increase restriction

Risk may not be increased if current drawdown state is:

```text
DRAWDOWN_CAUTION
DRAWDOWN_PAUSE
DRAWDOWN_HARD_REVIEW
DRAWDOWN_ESCALATED_TO_INCIDENT
```

Risk may be increased only after:

- drawdown review,
- stable recovery evidence,
- weekly review,
- no unresolved incidents,
- clean reconciliation,
- operator approval,
- release/config version update.

## Higher leverage interaction

Future leverage increases, such as 5x or 10x effective leverage caps, must also consider drawdown behavior.

Higher leverage may increase notional, fee sensitivity, liquidation sensitivity, and operational stress.

A leverage cap increase must not be approved while drawdown controls are active.

---

## Drawdown Watch Behavior

When drawdown watch triggers:

```text
drawdown_state = DRAWDOWN_WATCH
```

Default behavior:

- alert operator,
- record state change,
- include in daily/weekly review,
- continue trading only if all other gates permit,
- do not increase risk.

Drawdown watch is a visibility state, not necessarily a trading halt.

---

## Drawdown Caution Behavior

When drawdown caution triggers:

```text
drawdown_state = DRAWDOWN_CAUTION
```

Default behavior:

- block risk increases,
- block leverage cap increases,
- block notional cap increases,
- require closer supervision,
- include in weekly review,
- continue new entries only if current stage/config permits.

Recommended tiny-live behavior:

- entries may continue only if daily loss rules and all runtime gates are clean,
- operator should monitor next run closely,
- no scaling or parameter loosening is allowed.

---

## Drawdown Pause Behavior

When drawdown pause triggers:

```text
drawdown_state = DRAWDOWN_PAUSE
entries_blocked = true
drawdown_pause_active = true
operator_review_required = true
```

Default behavior:

- no new entries,
- existing protected position may continue safety management,
- risk-reducing stop actions may continue,
- approved exits may continue,
- reconciliation and recovery may continue,
- operator review required before resumption.

## Existing protected position

Do not automatically flatten solely because drawdown pause triggered if the open position is valid and protected.

The position may continue under safety-preserving management.

## Existing unprotected position

If position is unprotected:

- incident policy takes over,
- kill switch may activate,
- stop restoration or flattening may be required.

---

## Drawdown Hard Review Behavior

When hard review triggers:

```text
drawdown_state = DRAWDOWN_HARD_REVIEW
entries_blocked = true
operator_review_required = true
```

Default behavior:

- block live entries,
- require formal review,
- require review of recent trades,
- require review of execution and stop behavior,
- require review of live results versus backtest expectations,
- block risk increases,
- block live scaling,
- possibly freeze release promotion.

Hard review may persist beyond daily reset.

---

## Drawdown Escalation to Incident

Drawdown should escalate to incident if it is tied to abnormal behavior.

## Escalation triggers

Examples:

- position without confirmed protective stop,
- stop submission failure causing excess loss,
- unknown execution status causing duplicate or uncontrolled exposure,
- repeated unsafe mismatches,
- user-stream stale while exposed,
- market-data stale affecting management,
- manual/non-bot exposure,
- security/credential issue,
- extreme slippage outside expected assumptions,
- emergency flattening event.

## Effects

If escalated:

```text
drawdown_state = DRAWDOWN_ESCALATED_TO_INCIDENT
```

Then incident and kill-switch policy determine:

- runtime mode,
- operator review requirements,
- emergency response,
- recovery,
- resumption.

---

## Drawdown Recovery and Resumption

## Clearing drawdown pause

To clear drawdown pause, require:

- operator review,
- clean reconciliation,
- no active severe incident,
- no active kill switch,
- no unprotected position,
- no unknown execution status,
- review of recent trades,
- review of execution/protection behavior,
- explicit next-run decision.

## Clearing hard review

Hard review requires stronger process:

- formal review note,
- review of recent losing sequence,
- comparison to expected backtest drawdown profile,
- review of daily/weekly operational records,
- review of incident/stale stream/mismatch history,
- decision whether to continue, reduce risk, pause, or return to research.

## Recovery is not one winning trade

One winning trade does not by itself clear drawdown concern or approve risk increase.

Risk increase after drawdown requires sustained evidence and review.

## New equity high

When strategy equity reaches a new high watermark, drawdown state may return to normal if no other blocking conditions remain.

However, incident/kill-switch states must still be cleared through their own policies.

---

## Drawdown and Weekly Review

Weekly review should include:

- current drawdown,
- max drawdown this week,
- max drawdown since deployment,
- realized drawdown versus mark-to-market drawdown,
- drawdown compared to backtest expectation,
- number of losing trades,
- worst losing streak,
- daily lockouts,
- incidents during drawdown,
- execution/protection anomalies,
- recommendation for next week.

## Weekly review outcomes

Possible outcomes:

```text
continue normally
continue with caution
pause pending review
reduce risk
remain paused
return to research
escalate incident/release review
```

Risk increases should not be considered unless weekly review supports stability.

---

## Drawdown and Release Process

Drawdown controls interact with release promotion.

## Promotion blocked if

- drawdown pause active,
- hard review active,
- unresolved drawdown incident,
- drawdown exceeds validation expectation materially,
- drawdown is tied to execution/protection defects,
- daily/weekly review recommends pause.

## Rollback review may be required if

- drawdown begins after a release,
- execution behavior changes after release,
- incident frequency increases after release,
- stop/protection behavior degrades,
- live results diverge sharply from expected behavior.

Rollback is not automatic solely because of drawdown, but drawdown may trigger release review.

---

## Missing or Stale Drawdown State

If drawdown state is unavailable, corrupt, stale, or cannot be computed:

```text
block new entries
raise operator-visible warning
require state repair or reconciliation
```

## Examples

- equity store unavailable,
- high watermark missing,
- recent trade PnL missing,
- open position PnL unavailable,
- realized/unrealized data inconsistent,
- restart could not load drawdown state,
- account allocation changed without update.

## Fail-closed rule

Live trading must not continue if the system cannot determine whether drawdown controls are active.

---

## Persistence Requirements

Drawdown state must be persisted.

Minimum persisted drawdown record:

```text
strategy_id
strategy_version
deployment_stage
strategy_equity_high_watermark_usdt
current_strategy_equity_usdt
current_realized_equity_usdt
current_mark_to_market_equity_usdt
current_drawdown_fraction
realized_drawdown_fraction
mark_to_market_drawdown_fraction
max_drawdown_fraction_since_deployment
max_drawdown_fraction_current_week
drawdown_state
drawdown_state_reason
drawdown_watch_active
drawdown_caution_active
drawdown_pause_active
drawdown_hard_review_required
last_equity_update_utc_ms
last_high_watermark_update_utc_ms
last_drawdown_state_change_utc_ms
updated_at_utc_ms
```

## Operator review records

If drawdown pause or hard review is cleared, persist:

```text
operator_identity_or_alias
action_type
reason
review_summary_reference
occurred_at_utc_ms
resulting_state
```

## Restart behavior

On restart, drawdown state must be loaded before new entries are allowed.

If unavailable:

```text
block entries
```

---

## Event Contract Expectations

Recommended events:

```text
drawdown.equity_updated
drawdown.high_watermark_updated
drawdown.watch_triggered
drawdown.caution_triggered
drawdown.pause_triggered
drawdown.hard_review_triggered
drawdown.escalated_to_incident
drawdown.pause_clearance_requested
drawdown.pause_cleared
drawdown.pause_clearance_blocked
drawdown.state_unavailable
```

## Equity update event payload

Minimum payload:

```text
strategy_id
strategy_version
current_strategy_equity_usdt
strategy_equity_high_watermark_usdt
current_drawdown_fraction
realized_drawdown_fraction
mark_to_market_drawdown_fraction
occurred_at_utc_ms
```

## Drawdown state change event payload

Minimum payload:

```text
previous_drawdown_state
new_drawdown_state
trigger_threshold
current_drawdown_fraction
state_change_reason
entries_blocked
operator_review_required
occurred_at_utc_ms
```

## Clearance event payload

Minimum payload:

```text
drawdown_state
requested_by
clearance_result
clearance_reason
blocked_reasons if any
occurred_at_utc_ms
```

---

## Operator Visibility Requirements

The operator dashboard should show:

```text
current strategy equity
strategy equity high watermark
current drawdown %
realized drawdown %
mark-to-market drawdown %
max drawdown since deployment
max drawdown current week
drawdown state
drawdown pause active yes/no
drawdown hard review required yes/no
entries blocked by drawdown yes/no
risk increase blocked yes/no
last high watermark time
last drawdown state change time
clearance requirements
```

## Required alerts

Alerts should occur when:

- drawdown watch triggers,
- drawdown caution triggers,
- drawdown pause triggers,
- hard review triggers,
- drawdown state unavailable,
- drawdown escalates to incident,
- risk increase is attempted while drawdown control active,
- drawdown clearance is blocked.

---

## Implementation Boundaries

## Risk layer owns

- checking drawdown gate before entry approval,
- rejecting entries when drawdown pause/hard review is active,
- blocking risk increases when drawdown caution or worse is active.

## Persistence layer owns

- storing drawdown state,
- restoring state on restart,
- storing review/clearance records.

## Observability layer owns

- drawdown events,
- alerts,
- dashboard summaries.

## Operator layer owns

- drawdown review workflow,
- clearance request path,
- reason capture.

## Strategy layer does not own

- drawdown clearance,
- risk increase approval,
- drawdown reset.

## Execution layer does not own

- drawdown thresholds,
- drawdown state transitions,
- drawdown pause clearance.

---

## Rejection Categories

Recommended rejection categories:

```text
DRAWDOWN_PAUSE_ACTIVE
DRAWDOWN_HARD_REVIEW_REQUIRED
DRAWDOWN_STATE_UNAVAILABLE
DRAWDOWN_COUNTER_STALE
DRAWDOWN_RISK_INCREASE_BLOCKED
DRAWDOWN_ESCALATED_TO_INCIDENT
DRAWDOWN_CLEARANCE_REQUIRED
```

A drawdown watch alone does not necessarily reject entries.

A drawdown caution blocks risk increases, but may not block entries unless configured.

Drawdown pause and hard review must block new entries.

---

## Testing Requirements

Implementation must include tests for the following.

## High-watermark tests

- new equity high updates high watermark,
- lower equity does not reset high watermark,
- manual reset requires explicit reason,
- allocation changes are recorded.

## Drawdown calculation tests

- current drawdown calculation,
- realized drawdown calculation,
- mark-to-market drawdown calculation,
- max drawdown since deployment,
- weekly max drawdown.

## Threshold tests

- tiny-live watch at -1.0%,
- tiny-live caution at -1.5%,
- tiny-live pause at -2.0%,
- tiny-live hard review at -3.0%,
- watch does not necessarily block entries,
- caution blocks risk increases,
- pause blocks entries,
- hard review blocks entries.

## Runtime tests

- drawdown pause does not auto-flatten protected position,
- unprotected position during drawdown escalates incident,
- active kill switch blocks drawdown clearance,
- reconciliation required blocks drawdown clearance,
- missing drawdown state blocks entries.

## Restart tests

- drawdown state restored on restart,
- drawdown pause persists after restart,
- hard review persists after restart,
- missing state fails closed.

## Scaling tests

- risk increase rejected during drawdown caution,
- risk increase rejected during drawdown pause,
- risk increase rejected during hard review,
- risk increase allowed only after review state clean.

## Operator tests

- clearance requires reason,
- clearance blocked under unsafe state,
- clearance event persisted,
- dashboard summary reflects drawdown state.

---

## V1 Non-Goals

The drawdown-control framework does not include:

- portfolio-level drawdown allocation,
- multi-symbol capital rebalancing,
- automatic strategy switching after drawdown,
- automatic risk increase after recovery,
- martingale recovery behavior,
- discretionary override to “make it back,”
- tax/accounting reporting,
- investor reporting,
- fund-level drawdown waterfalls,
- machine-learning drawdown prediction.

These may be researched later, but they are not v1 behavior.

---

## Open Questions

The following should be resolved before paper/shadow or tiny live.

## 1. Exact strategy equity source

The project should define whether current strategy equity comes from:

- exchange account equity,
- internal allocated equity ledger,
- realized PnL ledger,
- mark-to-market calculation,
- or a combination.

## 2. Allocation change handling

Need exact rule for how deposits, withdrawals, or allocation changes affect high watermark.

## 3. Mark-to-market timing

Need exact update cadence for mark-to-market drawdown during open positions.

## 4. Hard review persistence

Recommended: hard review persists until operator review, even if equity recovers.

Implementation should confirm.

## 5. Future threshold approval

Future 0.50%, 0.75%, and 1.00% risk thresholds require validation and approval.

The framework does not approve them automatically.

---

## Acceptance Criteria

This drawdown-control policy is satisfied when implementation can demonstrate:

- drawdown is calculated from strategy equity high watermark,
- tiny-live watch triggers at -1.0%,
- tiny-live caution triggers at -1.5%,
- tiny-live pause triggers at -2.0%,
- tiny-live hard review triggers at -3.0%,
- drawdown pause blocks new entries,
- drawdown caution blocks risk increases,
- drawdown hard review requires formal review,
- drawdown pause does not automatically flatten a valid protected position,
- abnormal drawdown escalates to incident/kill-switch policy,
- missing drawdown state fails closed,
- drawdown state persists across restart,
- daily reset does not clear drawdown hard review,
- operator dashboard shows drawdown state clearly,
- and future risk/leverage increases are blocked while drawdown controls are active.

---

## Document Status

- Status: ACTIVE
- Created: 2026-04-18
- Owner: Project operator
- Role: Risk drawdown-control policy
