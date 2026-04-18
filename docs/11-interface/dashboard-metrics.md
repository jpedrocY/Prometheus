# Dashboard Metrics

## Purpose

This document defines the dashboard metrics and status fields for the v1 Prometheus operator dashboard.

Its purpose is to define what the dashboard must display so the operator can supervise Prometheus safely from the dedicated local NUC / mini PC monitor.

The dashboard should be visually polished, information-rich, and suitable for always-on display. It may take inspiration from professional exchange dashboards such as Binance or TradingView-style chart views, but it must remain specific to Prometheus:

```text
The dashboard shows bot state, risk state, exchange state, protection state,
orders, alerts, charts, and review information.

It is not a discretionary manual trading terminal.
```

This document is a metrics catalog and display contract. It lists what should be visible, how fields should be grouped, why they matter, and where the data should come from.

## Scope

This document applies to the v1 Prometheus dashboard under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- one-way position mode,
- isolated margin mode,
- one active strategy,
- one live symbol first,
- one open position maximum,
- one active protective stop maximum,
- exchange-side protective stop is mandatory,
- restart begins in safe mode,
- exchange state is authoritative,
- runtime state is persisted locally,
- the operator dashboard is displayed on the dedicated NUC monitor during operation,
- v1 is supervised, not lights-out autonomous.

This document covers dashboard fields for:

- top-level runtime state,
- trading permission,
- deployment stage,
- environment and adapter mode,
- market-data health,
- user-stream health,
- exchange connectivity,
- open position state,
- protective stop state,
- open normal orders,
- open algo/protective stop orders,
- unknown execution outcomes,
- strategy signal state,
- setup and trade chart visualization,
- risk and sizing state,
- daily loss state,
- drawdown state,
- reconciliation state,
- restart/recovery state,
- incidents and alerts,
- audit/operator action state,
- security and credential readiness,
- release/config/version state,
- host/NUC health,
- alert-routing state,
- review support metrics.

This document does **not** define:

- exact frontend layout,
- charting library selection,
- CSS/style design,
- authentication implementation,
- exact API route schemas,
- exact database queries,
- exact alert-routing implementation,
- or manual-control workflows.

Those are covered by related documents.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/11-interface/operator-dashboard-requirements.md`
- `docs/11-interface/manual-control-actions.md`
- `docs/11-interface/approval-workflows.md`
- `docs/11-interface/alerting-ui.md`
- `docs/08-architecture/state-model.md`
- `docs/08-architecture/event-flows.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/runtime-persistence-spec.md`
- `docs/08-architecture/database-design.md`
- `docs/08-architecture/observability-design.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/10-security/audit-logging.md`
- `docs/10-security/host-hardening.md`
- `docs/10-security/disaster-recovery.md`
- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/07-risk/kill-switches.md`
- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`

### Authority hierarchy

If this document conflicts with the state model on runtime state meaning, the state model wins.

If this document conflicts with risk documents on risk thresholds or lockout behavior, the risk documents win.

If this document conflicts with manual-control-actions on allowed controls, manual-control-actions wins.

If this document conflicts with alerting-ui on alert presentation, alerting-ui wins for alert UI behavior.

If this document conflicts with database-design on stored fields, database-design wins for persistence.

---

## Dashboard Philosophy

## 1. Always-on operator visibility

The dashboard should be continuously available on the dedicated NUC monitor during operation.

The operator should be able to glance at the screen and understand:

- is the bot healthy,
- is it allowed to trade,
- is there exposure,
- is exposure protected,
- are streams trusted,
- are open orders expected,
- are incidents active,
- is human action required.

## 2. Safety status first, analytics second

Profit, chart beauty, and performance statistics matter, but the top priority is safety state.

The dashboard must emphasize:

- runtime mode,
- entries allowed/blocked,
- open exposure,
- protection status,
- incidents,
- reconciliation,
- alerts,
- kill switch,
- operator review requirement.

## 3. Binance-like richness without discretionary trading

The dashboard may be stylish, dense, and useful like a professional exchange dashboard.

It may show:

- candle charts,
- trade overlays,
- open orders,
- PnL,
- account/risk stats,
- position information,
- order lifecycle status.

It must not provide arbitrary manual order-entry controls.

## 4. Exchange truth vs local state must be visible

The dashboard should make it clear whether a value comes from:

- exchange REST snapshot,
- user stream,
- local runtime state,
- strategy calculation,
- risk engine calculation,
- operator action,
- audit/event log,
- simulated/paper state.

This matters because local state is not exchange truth.

## 5. Unknown state must be obvious

Unknown or stale state should be visually obvious.

Examples:

- position unknown,
- protection uncertain,
- user stream stale,
- reconciliation required,
- open order status unknown,
- alert route degraded,
- runtime DB unavailable.

The dashboard must not make uncertain state look healthy.

---

## Display Priority Levels

Dashboard fields should be grouped by operator urgency.

## Priority 0 — Critical always-visible status

These fields should be visible at all times:

- runtime mode,
- entries allowed/blocked,
- open position yes/no,
- protection confirmed yes/no,
- kill switch active yes/no,
- incident active yes/no,
- highest active severity,
- operator action required yes/no,
- user-stream health,
- market-data health,
- reconciliation state,
- current deployment stage.

## Priority 1 — Active exposure and order management

Visible whenever trading is active or position/order state matters:

- position side,
- position size,
- average entry price,
- notional,
- mark price,
- unrealized PnL,
- protective stop trigger,
- stop status,
- open normal orders,
- open algo orders,
- unknown outcomes,
- trade lifecycle state,
- current risk stage.

## Priority 2 — Risk and governance

Visible in dashboard panels:

- risk fraction,
- sizing equity,
- notional cap,
- leverage cap,
- daily loss state,
- drawdown state,
- remaining daily risk,
- full-risk losses today,
- risk increase blocked,
- deployment promotion status.

## Priority 3 — Diagnostics and review

Available in expandable panels:

- recent runtime events,
- exchange events,
- audit events,
- reconciliation details,
- incident timeline,
- setup/trade charts,
- strategy rule-check details,
- release/config details,
- host health.

---

## Top-Level Status Summary

This is the most important dashboard area.

## Required fields

| Field | Meaning |
|---|---|
| `runtime_mode` | `SAFE_MODE`, `RUNNING_HEALTHY`, `RECOVERING`, `BLOCKED_AWAITING_OPERATOR`, etc. |
| `entries_allowed` | Whether new strategy entries may currently proceed. |
| `entries_blocked_reason` | Primary reason entries are blocked. |
| `deployment_stage` | Local/dev, validation, dry-run, paper/shadow, tiny live, scaled live. |
| `environment` | Runtime environment name. |
| `adapter_mode` | Fake, simulated/testnet, production read-only, production trade-enabled. |
| `kill_switch_active` | Whether kill switch is active. |
| `paused_by_operator` | Whether operator pause is active. |
| `incident_active` | Whether any incident is active. |
| `highest_active_severity` | Highest active incident/alert severity. |
| `operator_review_required` | Whether human review is required before resumption. |
| `reconciliation_state` | Current reconciliation status. |
| `open_position_present` | Whether exchange/local state indicates open position. |
| `protection_confirmed` | Whether live position protection is confirmed. |
| `action_required_now` | Whether operator must act. |
| `last_critical_event` | Most recent important state/event summary. |
| `last_updated_at` | Dashboard data refresh timestamp. |

## Display rule

If any of the following are true, the top-level summary should use prominent warning/critical styling:

- position exists and protection not confirmed,
- kill switch active,
- unsafe reconciliation mismatch,
- unknown execution outcome,
- user stream stale while exposure exists,
- critical incident active,
- credential/security issue active,
- emergency flatten in progress,
- operator action required.

---

## Trading Permission Panel

The dashboard should explicitly show why the bot can or cannot trade.

## Required fields

| Field | Meaning |
|---|---|
| `entries_allowed` | Final derived permission state. |
| `strategy_evaluation_enabled` | Whether strategy may evaluate signals. |
| `live_order_generation_enabled` | Whether live order creation is allowed. |
| `exchange_write_capability_enabled` | Whether config permits exchange write actions. |
| `operator_pause_block` | Pause blocks entries. |
| `kill_switch_block` | Kill switch blocks entries. |
| `incident_block` | Incident blocks entries. |
| `reconciliation_block` | Reconciliation required or active. |
| `stream_health_block` | Required stream stale/unavailable. |
| `market_data_block` | Market data stale/untrusted. |
| `daily_loss_block` | Daily lockout blocks entries. |
| `drawdown_block` | Drawdown pause/hard review blocks entries. |
| `manual_exposure_block` | Manual/non-bot exposure detected. |
| `unknown_order_block` | Unknown order/execution outcome exists. |
| `config_block` | Config missing/invalid for stage. |
| `credential_block` | Credentials missing/invalid for stage. |

## Display rule

Show blocked reasons as explicit chips/tags.

Example:

```text
ENTRIES BLOCKED:
- SAFE_MODE
- RECONCILIATION_REQUIRED
- KILL_SWITCH_ACTIVE
```

Avoid hiding multiple reasons behind a single boolean.

---

## Runtime Mode Panel

## Required fields

| Field | Meaning |
|---|---|
| `runtime_mode` | Top-level runtime mode. |
| `trade_lifecycle_state` | Current trade attempt/lifecycle state. |
| `protection_state` | Protection state for active position. |
| `reconciliation_state` | Current reconciliation mode/status. |
| `incident_state` | Incident active/contained/resolved status. |
| `control_flags` | Kill switch, pause, entries blocked, review required. |
| `last_mode_transition_at` | Timestamp of last mode change. |
| `last_mode_transition_reason` | Why mode changed. |
| `safe_mode_exit_allowed` | Whether safe-mode exit conditions are satisfied. |
| `safe_mode_exit_blockers` | Blockers to healthy operation. |

## Display rule

The dashboard should never show `RUNNING_HEALTHY` if any hard safety blocker is active.

---

## Market-Data Health Panel

Market data is required for strategy evaluation and chart display.

## Required fields

| Field | Meaning |
|---|---|
| `market_data_health` | Healthy, degraded, stale, unavailable, restoring. |
| `btcusdt_15m_kline_status` | Required signal timeframe feed status. |
| `btcusdt_1h_kline_status` | Required higher-timeframe feed status. |
| `mark_price_stream_status` | Mark price reference feed status. |
| `last_15m_closed_bar_open_time` | Latest completed 15m bar identity. |
| `last_15m_closed_bar_close_time` | Close time of latest completed 15m bar. |
| `last_1h_closed_bar_open_time` | Latest completed 1h bar identity. |
| `last_1h_closed_bar_close_time` | Close time of latest completed 1h bar. |
| `bar_completion_delay_ms` | Delay between expected and processed closed bar. |
| `partial_candle_visible` | Whether current forming candle is displayed. |
| `partial_candle_used_for_strategy` | Must always be false. |
| `last_market_event_time` | Last exchange event time received. |
| `last_market_processed_at` | Last processing time. |
| `market_data_stale_reason` | Reason if stale/degraded. |

## Display rule

Partial candles may be displayed if clearly labeled as forming.

They must not be displayed as strategy-confirmed bars.

---

## User-Stream Health Panel

User stream is primary live private-state source.

## Required fields

| Field | Meaning |
|---|---|
| `user_stream_health` | Healthy, degraded, stale, unavailable, restoring. |
| `listen_key_status` | Active, renewal pending, failed, expired, unknown. |
| `last_keepalive_success_at` | Last keepalive success. |
| `last_private_event_time` | Last private exchange event time. |
| `last_private_event_processed_at` | Last private event processing time. |
| `private_event_lag_ms` | Event-time to processing-time lag. |
| `stream_gap_detected` | Whether a gap/reconnect may have occurred. |
| `reconciliation_required_due_to_stream` | Whether stream state requires reconciliation. |
| `last_order_update_at` | Last `ORDER_TRADE_UPDATE` processed. |
| `last_account_update_at` | Last `ACCOUNT_UPDATE` processed. |
| `last_algo_update_at` | Last `ALGO_UPDATE` processed. |
| `stream_restoring` | Whether recovery is underway. |

## Display rule

If user stream is stale while exposure exists, display as critical.

---

## Exchange Connectivity Panel

## Required fields

| Field | Meaning |
|---|---|
| `exchange_connectivity_health` | Healthy, degraded, unavailable, rate-limited. |
| `rest_connectivity_status` | REST reachability. |
| `websocket_connectivity_status` | WebSocket connectivity. |
| `last_successful_rest_read_at` | Last successful exchange read. |
| `last_successful_order_write_at` | Last successful write action, where applicable. |
| `rate_limit_state` | Normal, caution, limited, impaired. |
| `rate_limit_recent_errors` | Recent throttling/weight errors. |
| `ip_ban_risk` | Whether rate-limit/IP-ban risk exists. |
| `clock_request_error_state` | Signed timestamp/recvWindow-related issues. |
| `exchange_status_notes` | Current exchange adapter notes. |

## Display rule

Rate-limit impairment during recovery should be prominent because it may reduce ability to verify or protect state.

---

## Position and Exposure Panel

This panel should be one of the most prominent areas whenever exposure exists or may exist.

## Required fields

| Field | Meaning |
|---|---|
| `position_present` | Whether exchange shows an open position. |
| `position_ownership` | Strategy-owned, possible strategy, manual/non-bot, unknown. |
| `symbol` | BTCUSDT for v1 live. |
| `position_side` | Long, short, flat, unknown. |
| `position_side_raw` | Raw exchange value where useful, e.g. `BOTH`. |
| `signed_position_size` | Signed exchange size. |
| `absolute_position_size` | Absolute size. |
| `average_entry_price` | Average fill/entry price. |
| `break_even_price` | Exchange or internal break-even. |
| `mark_price` | Current mark price. |
| `last_price` | Last trade/reference price if available. |
| `notional_usdt` | Approximate notional. |
| `effective_leverage` | Notional / sizing equity. |
| `unrealized_pnl_usdt` | Current unrealized PnL. |
| `unrealized_pnl_fraction` | Unrealized PnL vs sizing equity. |
| `realized_pnl_usdt_trade` | Realized PnL for current/last trade. |
| `liquidation_price` | Exchange-provided liquidation reference where available. |
| `margin_type` | Isolated, crossed, unknown. |
| `isolated_margin` | Isolated margin fields where available. |
| `manual_exposure_detected` | Whether non-bot exposure exists. |
| `exposure_block_reason` | Why exposure blocks entries. |

## Display rule

Manual/non-bot exposure or unknown ownership must be clearly visible and should block entries.

---

## Protective Stop Panel

Protection is first-class.

## Required fields

| Field | Meaning |
|---|---|
| `protection_state` | Confirmed, submitted, pending, uncertain, missing, emergency. |
| `protective_stop_present` | Whether a valid protective stop exists. |
| `active_stop_count` | Number of active strategy-owned protective stops. |
| `stop_client_algo_id` | Redacted/truncated client algo ID. |
| `stop_exchange_algo_id` | Exchange algo/order ID where available. |
| `stop_type` | STOP_MARKET for v1. |
| `stop_side` | Side needed to close position. |
| `stop_trigger_price` | Current protective stop trigger. |
| `stop_working_type` | MARK_PRICE for v1. |
| `stop_price_protect` | TRUE/FALSE. |
| `stop_close_position` | TRUE/FALSE. |
| `last_stop_confirmation_at` | Last time stop existence was confirmed. |
| `stop_stage` | Initial, reduced, break-even, trailing, replacement. |
| `stop_replacement_in_progress` | Whether cancel-and-replace is active. |
| `old_stop_cancel_state` | Cancel status for old stop. |
| `new_stop_submit_state` | Submit status for replacement stop. |
| `orphaned_stop_detected` | Stop exists without matching position/trade. |
| `multiple_stop_warning` | Multiple/conflicting stops detected. |
| `protection_emergency` | Position exists without confirmed protection. |

## Display rule

If position exists and protection is not confirmed, the dashboard should show critical emergency state.

---

## Open Normal Orders Panel

The dashboard should show all relevant normal orders for the live symbol.

## Required fields per order

| Field | Meaning |
|---|---|
| `order_role` | Entry, exit, emergency flatten, stale cleanup, unknown external. |
| `order_category` | Normal. |
| `client_order_id` | Redacted/truncated deterministic ID. |
| `exchange_order_id` | Exchange order ID. |
| `symbol` | Symbol. |
| `side` | Buy/sell. |
| `type` | Market, limit, etc. |
| `quantity` | Order quantity. |
| `filled_quantity` | Filled amount. |
| `average_fill_price` | Average fill price if known. |
| `status` | New, filled, canceled, rejected, expired, unknown. |
| `submission_state` | Pending, acknowledged, rejected, unknown outcome. |
| `created_at` | Local creation timestamp. |
| `last_exchange_update_at` | Last exchange event time. |
| `last_checked_at` | Last REST/reconciliation check. |
| `trade_reference` | Related trade if any. |
| `ownership` | Strategy-owned, external, unknown. |
| `unknown_outcome` | Whether outcome is unknown. |

## Display rule

Unknown normal order outcomes should be prominent and should explain why entries are blocked.

---

## Open Algo / Protective Orders Panel

This panel should show conditional/algo orders separately from normal orders.

## Required fields per algo order

| Field | Meaning |
|---|---|
| `algo_role` | Protective stop, replacement stop, stale cleanup, unknown external. |
| `client_algo_id` | Redacted/truncated deterministic ID. |
| `exchange_algo_id` | Exchange algo ID. |
| `symbol` | Symbol. |
| `side` | Side. |
| `type` | STOP_MARKET. |
| `trigger_price` | Trigger price. |
| `working_type` | MARK_PRICE. |
| `price_protect` | TRUE/FALSE. |
| `close_position` | TRUE/FALSE. |
| `status` | Active, triggered, canceled, rejected, unknown. |
| `confirmed_at` | Last confirmation. |
| `trade_reference` | Related trade. |
| `ownership` | Strategy-owned, external, unknown. |
| `orphaned` | Whether algo order is orphaned. |
| `conflicts_with_active_stop` | Whether it conflicts. |

## Display rule

Algo orders should not be mixed into the normal order table without clear labeling.

---

## Unknown Execution Outcomes Panel

Unknown outcomes are safety-critical.

## Required fields

| Field | Meaning |
|---|---|
| `unknown_outcome_present` | Whether any unknown outcome exists. |
| `unknown_outcome_type` | Entry, stop submit, stop cancel, stop replacement, exit, flatten. |
| `related_command_id` | Command reference. |
| `related_order_id` | Order/stop reference. |
| `related_trade_reference` | Trade reference. |
| `detected_at` | Detection timestamp. |
| `last_reconciliation_attempt_at` | Last attempt to resolve. |
| `current_classification` | Pending, resolved clean, unsafe, operator required. |
| `entries_blocked_due_to_unknown` | Whether entries blocked. |
| `next_required_action` | Reconcile, operator review, emergency branch, etc. |

## Display rule

Unknown outcome must not be hidden in logs only.

---

## Strategy Signal and Setup Panel

This panel shows whether the strategy is active and why it is or is not signaling.

## Required fields

| Field | Meaning |
|---|---|
| `strategy_id` | Active strategy identifier. |
| `strategy_version` | Strategy version. |
| `signal_timeframe` | 15m. |
| `higher_timeframe` | 1h. |
| `last_strategy_evaluation_at` | Last evaluation time. |
| `last_completed_signal_bar` | Last completed 15m bar used. |
| `last_completed_bias_bar` | Last completed 1h bar used. |
| `higher_timeframe_bias` | Long, short, neutral. |
| `setup_valid` | Whether setup window valid. |
| `setup_high` | Setup high. |
| `setup_low` | Setup low. |
| `setup_range_width` | Range width. |
| `atr_15m` | ATR reference. |
| `normalized_atr_1h` | 1h normalized ATR. |
| `breakout_detected` | Whether breakout condition met. |
| `breakout_direction` | Long/short. |
| `signal_result` | No action, candidate, rejected. |
| `last_no_trade_reason` | Why no trade occurred. |
| `last_candidate_rejection_reason` | Risk/exposure rejection reason if any. |

## Display rule

Strategy diagnostics should clearly show completed-bar use and must not imply partial candle signals are actionable.

---

## Trade / Setup Chart Visualization

A future dashboard should include TradingView-like chart visualizations for trades and setups.

## Purpose

The purpose is visual rule verification and operator review.

Questions it should help answer:

- Did the bot wait for candle close?
- Was the setup range valid?
- Did the breakout close beyond the required level?
- Was the 1h bias valid?
- Was the stop placed at the documented structural level?
- Was the stop updated according to rules?
- Did the exit match lifecycle state?
- Was the trade rejected correctly?

## Required overlays

For a trade/setup chart, include where available:

| Overlay | Meaning |
|---|---|
| Completed candles | Historical 15m candles used for signal. |
| Forming candle | Clearly labeled as partial/forming if shown. |
| Setup window highlight | Previous 8 completed candles. |
| Setup high/low lines | Breakout boundaries. |
| Breakout bar marker | Confirming candle. |
| Entry marker | Actual/expected entry fill. |
| Entry price line | Fill/entry reference. |
| Initial stop line | Original risk-approved stop. |
| Current stop line | Active protective stop. |
| Stop update markers | Cancel-and-replace stages. |
| Exit marker | Exit/stop/flatten close. |
| Target/R levels | Optional R visualization. |
| PnL/R label | Realized/closed or current trade PnL. |
| HTF bias badge | Long/short/neutral at decision time. |
| Rule checklist panel | Pass/fail for strategy conditions. |

## Forbidden chart behavior

The chart must not allow:

- click-to-buy,
- click-to-sell,
- chart-based order placement,
- drag-to-widen-stop,
- manual reversal,
- manual pyramiding,
- bypassing strategy/risk checks.

## Review value

This feature should eventually support daily/weekly review and debugging when a trade seems suspicious.

---

## Risk and Sizing Panel

## Required fields

| Field | Meaning |
|---|---|
| `sizing_equity_usdt` | Equity used for sizing. |
| `account_equity_usdt` | Exchange/account equity reference. |
| `strategy_allocated_equity_usdt` | Strategy allocation boundary. |
| `risk_fraction` | Current risk per trade. |
| `risk_amount_usdt` | Risk budget. |
| `risk_usage_fraction` | Stop-risk usage fraction. |
| `effective_stop_risk_budget_usdt` | Budget used for pure stop distance. |
| `approved_quantity` | Quantity approved by risk. |
| `approved_notional_usdt` | Approved notional. |
| `effective_leverage` | Notional / sizing equity. |
| `max_effective_leverage` | Configured cap. |
| `max_position_notional_usdt` | Internal notional cap. |
| `stop_distance` | Entry-stop distance. |
| `stop_distance_atr_multiple` | Stop distance / ATR. |
| `quantity_rounding_status` | Rounded down/valid/rejected. |
| `exchange_min_qty_status` | Whether quantity meets minimum. |
| `risk_gate_status` | Approved/rejected/blocked. |
| `last_risk_rejection_reason` | Reason if rejected. |

## Display rule

Risk panel should distinguish approved risk from current unrealized PnL.

---

## Daily Loss Panel

## Required fields

| Field | Meaning |
|---|---|
| `session_date_utc` | Current UTC daily session. |
| `daily_realized_pnl_usdt` | Realized PnL for day. |
| `daily_realized_pnl_fraction` | PnL fraction. |
| `daily_state` | Normal, warning, lockout, hard review. |
| `daily_warning_threshold` | Warning threshold. |
| `daily_lockout_threshold` | Lockout threshold. |
| `hard_review_threshold` | Hard review threshold. |
| `consecutive_losing_trades_today` | Loss streak. |
| `full_risk_losses_today` | Full-risk stopped trades. |
| `daily_risk_consumed_fraction` | Approximate consumed risk. |
| `open_position_remaining_risk_fraction` | Remaining open risk to stop. |
| `entries_blocked_by_daily_loss` | Whether daily rule blocks entries. |
| `daily_reset_at_utc` | Next daily reset. |
| `override_active` | Whether daily override is active. |

## Display rule

Daily reset must not imply incidents/kill switch are cleared.

---

## Drawdown Panel

## Required fields

| Field | Meaning |
|---|---|
| `current_strategy_equity_usdt` | Current strategy equity. |
| `strategy_equity_high_watermark_usdt` | High watermark. |
| `strategy_drawdown_fraction` | Current drawdown. |
| `realized_drawdown_fraction` | Realized drawdown. |
| `mark_to_market_drawdown_fraction` | MTM drawdown. |
| `max_drawdown_since_deployment` | Deployment max drawdown. |
| `current_week_max_drawdown` | Weekly drawdown. |
| `drawdown_state` | Normal, watch, caution, pause, hard review. |
| `entries_blocked_by_drawdown` | Whether drawdown blocks entries. |
| `risk_increase_blocked` | Whether risk increase is blocked. |
| `last_drawdown_state_change_at` | Last transition time. |
| `drawdown_clearance_required` | Whether approval required. |

## Display rule

Drawdown controls should be visible even when no position is open.

---

## Reconciliation Panel

## Required fields

| Field | Meaning |
|---|---|
| `reconciliation_state` | Idle, required, in progress, clean, recoverable mismatch, unsafe mismatch. |
| `reconciliation_reason` | Restart, stream gap, unknown outcome, manual request, etc. |
| `last_successful_reconciliation_at` | Last clean/accepted reconciliation. |
| `reconciliation_started_at` | Current/last start. |
| `reconciliation_completed_at` | Current/last completion. |
| `mismatch_class` | None, recoverable, unsafe. |
| `position_result` | Position comparison result. |
| `normal_order_result` | Normal order comparison result. |
| `algo_order_result` | Algo/protection comparison result. |
| `repair_required` | Whether repair needed. |
| `repair_in_progress` | Whether repair active. |
| `repair_action_taken` | What repair was done. |
| `operator_required` | Whether operator needed. |
| `safe_mode_exit_allowed` | Whether reconciliation supports resumption. |

## Display rule

Unsafe mismatch must be critical and should block healthy display.

---

## Restart and Recovery Panel

## Required fields

| Field | Meaning |
|---|---|
| `last_restart_at` | Last process restart. |
| `restart_reason` | Planned, crash, host reboot, recovery, unknown. |
| `restart_mode` | Clean, unclean, stale-state recovery. |
| `safe_mode_entered_at` | Safe-mode start. |
| `safe_mode_exit_at` | Safe-mode exit if any. |
| `startup_checks_status` | Config, DB, secrets, logs, connectivity. |
| `local_state_loaded` | Whether persisted state loaded. |
| `exchange_state_verified` | Whether exchange state verified. |
| `user_stream_restored` | Whether user stream restored. |
| `market_data_restored` | Whether market data restored. |
| `recovery_approval_required` | Whether approval needed. |
| `last_recovery_outcome` | Clean, repaired, blocked, unsafe. |

## Display rule

Startup/restart should be visible. The bot should not appear to have “always been healthy” after crash.

---

## Incidents Panel

## Required fields

| Field | Meaning |
|---|---|
| `active_incident_count` | Count of active incidents. |
| `highest_active_severity` | Highest severity. |
| `active_incident_id` | Primary incident ID. |
| `incident_class` | User stream, market data, protection, security, etc. |
| `incident_status` | Open, contained, blocked, resolved. |
| `incident_opened_at` | Opening time. |
| `incident_summary` | Human-readable summary. |
| `containment_action` | What was done. |
| `operator_review_required` | Whether review required. |
| `related_trade_reference` | Related trade. |
| `related_order_reference` | Related order. |
| `related_reconciliation_id` | Related reconciliation. |
| `resolution_status` | If resolved, how. |
| `post_incident_review_required` | Review requirement. |

## Display rule

Active incidents should never be hidden behind performance widgets.

---

## Alerts Panel

This document lists alert fields; detailed alert presentation belongs in `alerting-ui.md`.

## Required fields

| Field | Meaning |
|---|---|
| `active_alert_count` | Number of active alerts. |
| `highest_alert_severity` | Info, warning, critical. |
| `critical_alert_present` | Whether critical alert exists. |
| `alert_id` | Alert ID. |
| `alert_class` | Stream, protection, incident, security, risk, host. |
| `alert_title` | Short title. |
| `alert_message` | Human-readable message. |
| `alert_status` | Active, acknowledged, resolved, suppressed. |
| `acknowledged_by` | Operator if acknowledged. |
| `acknowledged_at` | Acknowledgement timestamp. |
| `resolved_at` | Resolution timestamp. |
| `next_required_action` | What operator should do. |
| `alert_route_status` | Dashboard, Telegram, n8n delivery status. |

## Display rule

Acknowledged does not mean resolved.

---

## Audit and Operator Action Panel

## Required fields

| Field | Meaning |
|---|---|
| `last_operator_action` | Most recent operator action. |
| `last_operator_action_at` | Timestamp. |
| `last_operator_action_result` | Success, denied, failed, pending. |
| `pending_approval_count` | Open approval requests. |
| `pending_high_risk_approval_count` | Level 3/4 approvals. |
| `last_approval_decision` | Last approval. |
| `last_audit_event_at` | Last audit event. |
| `audit_logging_health` | Healthy/degraded/unavailable. |
| `audit_export_available` | Whether export path works. |
| `audit_redaction_status` | Whether redaction checks pass. |

## Display rule

Operator actions affecting safety should be visible in recent event timeline.

---

## Security and Credential Panel

This panel should show readiness without exposing secrets.

## Required fields

| Field | Meaning |
|---|---|
| `credential_status` | Missing, loaded, invalid, valid, rotated, compromised. |
| `api_key_permission_summary` | Read-only, trade-enabled, invalid, unknown. |
| `ip_restriction_status` | Configured, missing, exception, unknown. |
| `secret_storage_status` | Healthy, missing, invalid permissions, unknown. |
| `last_secret_validation_at` | Last validation time. |
| `credential_rotation_required` | Whether rotation required. |
| `security_incident_active` | Whether security incident active. |
| `dashboard_auth_status` | Dashboard auth/access status where implemented. |
| `telegram_secret_status` | Redacted readiness for Telegram. |
| `n8n_secret_status` | Redacted readiness for n8n. |
| `host_security_exception_active` | Any accepted host/security exception. |

## Display rule

Do not display API keys, secrets, tokens, full webhook URLs, or listen keys.

---

## Release and Configuration Panel

## Required fields

| Field | Meaning |
|---|---|
| `release_version` | Current release version. |
| `git_commit_hash` | Current commit. |
| `config_version` | Current config version. |
| `config_hash` | Hash of active config. |
| `strategy_version` | Active strategy version. |
| `risk_config_version` | Risk config version/hash. |
| `execution_config_version` | Execution config version/hash. |
| `database_schema_version` | Runtime DB schema/migration version. |
| `docs_version_reference` | Docs reference/commit. |
| `deployment_stage` | Current stage. |
| `last_deploy_at` | Last deployment time. |
| `rollback_available` | Whether rollback target exists. |
| `rollback_blockers` | Current rollback blockers. |
| `uncommitted_local_changes_detected` | Should be false on live host. |

## Display rule

Live operation should not hide unknown config/release state.

---

## Host / NUC Health Panel

The dedicated NUC host is part of the safety boundary.

## Required fields

| Field | Meaning |
|---|---|
| `host_name` | Host identifier. |
| `host_role` | Dedicated NUC, local dev, validation, etc. |
| `host_uptime` | System uptime. |
| `process_uptime` | Prometheus process uptime. |
| `cpu_usage` | Basic CPU usage. |
| `memory_usage` | Basic memory usage. |
| `disk_free_runtime_db` | Free disk for runtime DB path. |
| `disk_free_logs` | Free disk for logs. |
| `disk_free_backups` | Free disk for backups. |
| `time_sync_status` | Healthy/degraded/unknown. |
| `network_status` | Healthy/degraded/unavailable. |
| `public_ip_status` | Stable/changed/unknown where checked. |
| `ups_status` | If available. |
| `service_manager_status` | Running/restarting/failed. |
| `last_host_reboot_at` | Last reboot. |
| `dashboard_display_status` | Visible/local display expected/unknown. |

## Display rule

Host health should not overwhelm trading state, but critical host failures must surface prominently.

---

## Alert Routing Panel

## Required fields

| Field | Meaning |
|---|---|
| `dashboard_alerts_enabled` | Local dashboard alerts enabled. |
| `telegram_enabled` | Telegram route enabled. |
| `telegram_last_success_at` | Last successful test/send. |
| `telegram_last_failure_at` | Last failure. |
| `n8n_enabled` | n8n route enabled. |
| `n8n_last_success_at` | Last successful webhook. |
| `n8n_last_failure_at` | Last failure. |
| `critical_alert_route_tested_at` | Last critical alert test. |
| `alert_route_degraded` | Whether route degraded. |
| `alert_route_secrets_validated` | Redacted validation status. |

## Display rule

Paper/shadow and tiny-live readiness should fail if critical alert routing is not tested.

---

## Review Support Panel

The dashboard should support daily/weekly review.

## Required fields

| Field | Meaning |
|---|---|
| `trades_today` | Count of Prometheus trades today. |
| `winning_trades_today` | Wins today. |
| `losing_trades_today` | Losses today. |
| `average_r_multiple_today` | Average R if available. |
| `max_adverse_excursion` | Trade MAE where available. |
| `max_favorable_excursion` | Trade MFE where available. |
| `stop_out_count_today` | Stop-trigger exits today. |
| `emergency_action_count_today` | Emergency actions today. |
| `incident_count_today` | Incidents today. |
| `manual_action_count_today` | Operator actions today. |
| `rule_violation_count` | Any detected strategy/risk rule violations. |
| `paper_shadow_session_status` | If in paper/shadow. |
| `review_notes_pending` | Whether review notes needed. |

## Display rule

Review support should not distract from active emergency state.

---

## Data Source and Freshness Rules

Each dashboard field should have an explicit data source.

Recommended source categories:

```text
RUNTIME_STATE
RUNTIME_DB
USER_STREAM
REST_RECONCILIATION
MARKET_DATA_STREAM
STRATEGY_ENGINE
RISK_ENGINE
EXECUTION_LAYER
INCIDENT_CONTROL
AUDIT_LOG
HOST_MONITOR
CONFIG
RELEASE_METADATA
ALERT_ROUTER
```

## Freshness display

For important fields, dashboard should show:

- last updated time,
- source,
- freshness status,
- stale/unknown indicator.

## Stale handling

If a field is stale, the dashboard should not silently show old values as current.

Examples:

```text
Position size: stale since 12:30 UTC
Protective stop: last confirmed 18m ago
User stream: unavailable
```

---

## Styling and Visual Priority Guidelines

This document does not define final design, but the dashboard should follow these visual principles.

## Status-first layout

Top area:

- runtime mode,
- entries allowed,
- exposure/protection,
- incidents/alerts,
- action required.

Middle area:

- chart/trade visualization,
- position/protection,
- open orders,
- risk.

Side/bottom panels:

- stream health,
- reconciliation,
- recent events,
- host/alert status.

## Color/status language

Use clear severity language:

```text
HEALTHY
DEGRADED
STALE
BLOCKED
RECOVERING
CRITICAL
UNKNOWN
```

Avoid ambiguous cosmetic-only colors without labels.

## Critical state dominance

Critical state must override decorative/analytics panels.

If there is an unprotected live position, the dashboard should make that impossible to miss.

---

## Dashboard Readiness by Stage

## Local development

Minimum dashboard:

- runtime mode,
- fake adapter state,
- logs,
- unit/dev status.

## Dry-run

Minimum dashboard:

- runtime mode,
- fake order lifecycle,
- DB writes,
- strategy/risk decisions,
- basic chart/status.

## Paper / shadow

Minimum dashboard:

- live market data,
- paper/execution simulation state,
- dashboard alerts,
- Telegram/n8n test status,
- restart/recovery visibility,
- trade/setup review.

## Tiny live

Required dashboard:

- all Priority 0 and Priority 1 fields,
- open orders and stops,
- protection state,
- critical alert routing,
- operator action required,
- emergency controls per manual-control policy,
- audit/operator action visibility.

## Scaled live

Tiny-live dashboard plus stronger review, metrics, and incident visibility.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The following practical tasks should be captured later in:

```text
docs/09-operations/first-run-setup-checklist.md
```

## Dashboard setup

- configure dashboard to display on NUC monitor,
- choose local browser/session model,
- verify dashboard starts after reboot where appropriate,
- verify dashboard does not expose secrets,
- verify dashboard can reach backend,
- verify dashboard shows stale state clearly.

## Metrics verification

- verify position panel with fake/paper position,
- verify open normal orders panel,
- verify algo/protective orders panel,
- verify unknown outcome panel,
- verify strategy setup panel,
- verify chart/trade visualization with sample trade,
- verify risk/daily/drawdown panels,
- verify incidents/alerts panels.

## Alert routing

- verify Telegram route,
- verify n8n route if used,
- verify critical alert test,
- verify alert route failures display on dashboard.

## Launch readiness

- before paper/shadow, verify dashboard on monitor,
- before tiny live, verify all Priority 0/1 fields,
- verify emergency states dominate display,
- verify no arbitrary manual trading controls are present.

---

## Testing Requirements

## Unit tests

Test field derivation for:

- entries allowed/blocked,
- runtime mode display,
- position/protection summary,
- order table mapping,
- stale state labels,
- alert severity aggregation,
- daily/drawdown display,
- risk panel values,
- chart overlay data.

## Integration tests

Test dashboard backend/read models for:

- clean flat state,
- protected position,
- unprotected position emergency,
- unknown entry outcome,
- stop replacement in progress,
- user stream stale while exposed,
- market-data stale while flat,
- reconciliation unsafe mismatch,
- kill switch active,
- daily lockout,
- drawdown pause,
- credential issue,
- alert route failure.

## Visual/state tests

Test that:

- critical conditions appear prominently,
- stale values are labeled,
- acknowledged alerts are not treated as resolved,
- unsafe states do not appear healthy,
- chart visualization is read-only,
- arbitrary manual trading controls are absent.

## Dry-run drills

Before tiny live, verify dashboard behavior for:

- fake trade lifecycle,
- fake protective stop lifecycle,
- fake stop replacement,
- fake emergency unprotected position,
- fake emergency flatten,
- fake user-stream outage,
- fake reconciliation mismatch,
- fake dashboard/alert degradation.

---

## Non-Goals

This document does not define:

- final visual design,
- final CSS/theme,
- final frontend framework,
- exact charting library,
- exact API endpoints,
- exact authentication flow,
- exact database query implementation,
- full alert-routing UX,
- or discretionary trading tools.

It defines what the dashboard must make visible.

---

## Acceptance Criteria

`dashboard-metrics.md` is complete enough for v1 when it makes the following clear:

- the dashboard is an always-on NUC monitor supervision surface,
- the dashboard may be polished, dense, Binance-like, and chart-rich,
- safety status takes priority over analytics,
- open positions, normal orders, algo/protective orders, and unknown outcomes are visible,
- position and protection state are separate and prominent,
- user-stream, market-data, and exchange connectivity health are visible,
- daily loss and drawdown controls are visible,
- reconciliation/restart/recovery state is visible,
- incidents and alerts are visible and cannot be mistaken as resolved by acknowledgement,
- security/credential readiness is visible without exposing secrets,
- host/NUC health and alert routing status are visible,
- setup/trade charts are supported for visual rule verification,
- chart visualization is read-only and not a manual trading interface,
- stale or unknown state is clearly labeled,
- stage-specific dashboard readiness is defined,
- practical dashboard setup steps are deferred to the first-run setup checklist,
- and the dashboard supports supervised operation without weakening the safety model.
