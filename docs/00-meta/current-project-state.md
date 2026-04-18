# Current Project State

## Purpose

This document defines the current state of the Prometheus trading system project.

Its purpose is to:

- provide a clear snapshot of what has already been designed and decided,
- identify what remains before implementation,
- define the boundary between research/design and code generation,
- ensure continuity across chats, sessions, repository updates, and AI coding tools,
- and act as the authoritative high-level project memory checkpoint.

This document should be treated as the single high-level source of truth for project status.

If this document conflicts with a detailed specialist document, the specialist document wins for its domain.

If older chat memory conflicts with repository Markdown files, the repository Markdown files win.

---

## Project Objective

Prometheus is a long-term project to design and build a:

> production-oriented, safety-first, operator-supervised trading system

for:

- Binance USDⓈ-M futures,
- BTCUSDT perpetual as the initial live symbol.

The system is:

- initially rules-based,
- designed for robustness rather than novelty,
- built for staged and supervised deployment,
- structured to support future AI-assisted research or automation,
- but not dependent on a self-learning live AI component for v1.

The project is intentionally **not** starting with a self-learning, autonomous, always-on AI trading agent.

The project is building a staged trading system first.

---

## Current Phase

The project is currently in:

```text
implementation architecture and pre-Claude-Code planning
```

The current objective is to finish the remaining implementation-constraint documents before producing the final AI coding handoff.

The final AI coding handoff should not be created until the remaining important TBD placeholder documents are either:

- written as full documents,
- converted into bridge/superseded documents,
- explicitly deferred,
- or removed as no longer useful.

---

## Repository Context

The repository is expected to remain available at:

```text
https://github.com/jpedrocY/Prometheus
```

The repository Markdown files are the primary source of truth.

Project-uploaded files in ChatGPT are a limited continuity cache because the project file limit is 25 files.

The next assistant should inspect the repository directly when possible and use uploaded files only as a high-priority context subset.

---

## Strategic Direction — Locked Decisions

The following decisions are locked unless a conflict is surfaced and explicitly approved.

### Market and Venue

- Venue: Binance USDⓈ-M futures
- Initial live symbol: BTCUSDT perpetual
- First secondary research/comparison symbol: ETHUSDT perpetual
- V1 live scope: BTCUSDT only

### Strategy

- Strategy family: breakout continuation with higher-timeframe trend filter
- Signal timeframe: 15m
- Higher-timeframe bias: 1h
- Entry style: completed-bar confirmation, then market entry
- Baseline backtest fill assumption: next-bar open after confirmed signal close
- Initial stop: structural stop plus ATR buffer
- Trade management: staged risk reduction and strategy-managed trailing

### Execution

- Runtime account mode: one-way mode
- Margin mode: isolated margin
- One symbol first
- One position maximum
- No pyramiding in v1
- No reversal entry while positioned in v1
- No hedge-mode behavior in v1
- Entry order: normal MARKET order
- Protective stop: exchange-side algo/conditional STOP_MARKET
- Protective stop settings:
  - closePosition=true
  - workingType=MARK_PRICE
  - priceProtect=TRUE
- Stop updates: cancel-and-replace
- User stream: primary live private-state source
- REST: placement, cancellation, reconciliation, and recovery
- Exchange state is authoritative

### Risk

- Initial live risk per trade: 0.25% of sizing equity
- Initial effective leverage cap: 2x
- Leverage is a tool to reach valid risk-based position size, not a target
- Future risk path may work toward 1.00% only after staged validation and review
- Future leverage caps such as 5x or 10x may be researched later, but are not initial live defaults
- Internal notional cap is mandatory for live operation
- Missing risk state, metadata, or exchange-state confidence fails closed

### Deployment

- Deployment is supervised and staged
- V1 is not lights-out autonomous
- Standard rollout path:
  - research
  - validation
  - paper/shadow
  - tiny live
  - scaled live
- Restart always begins in safe mode
- Reconciliation is required before normal resumption
- Incidents are severity-classified
- Kill switch is persistent and never auto-clears

---

## Architectural Direction — Locked

### Core Architecture

- Modular monolith for v1
- Strict strategy/risk/execution separation
- Research and live runtime remain separate concerns
- Exchange state outranks local state
- Local persistence exists for restart safety and operational continuity
- Observability is state-centric, not vanity-metric-centric
- Operator interface is a supervision and control surface, not a discretionary trading terminal

### Core Runtime Principles

- Commands are not facts
- REST acknowledgements are not final truth
- User-stream and reconciliation paths confirm state
- A filled entry is not yet a protected trade
- A submitted stop is not yet confirmed protection
- A position without confirmed protection is an emergency state
- Unknown execution outcomes fail closed
- Manual/non-bot exposure blocks new bot entries

---

## Completed / Substantially Defined Documentation

The following areas are substantially defined and should be treated as current context.

---

## 1. Strategy and Research

Important documents:

```text
docs/03-strategy-research/first-strategy-comparison.md
docs/03-strategy-research/v1-breakout-strategy-spec.md
docs/03-strategy-research/v1-breakout-backtest-plan.md
```

Defined:

- v1 strategy family selection,
- BTCUSDT primary symbol,
- ETHUSDT comparison symbol,
- 15m/1h timeframe structure,
- breakout setup and trigger logic,
- completed-bar-only strategy logic,
- initial structural stop logic,
- staged stop management,
- backtest assumptions,
- anti-overfitting principles,
- validation methodology.

---

## 2. Data Layer

Important documents:

```text
docs/04-data/historical-data-spec.md
docs/04-data/timestamp-policy.md
docs/04-data/dataset-versioning.md
docs/04-data/live-data-spec.md
```

Defined:

- official Binance USDⓈ-M futures data as canonical v1 historical source,
- Parquet + DuckDB research data stack,
- UTC Unix milliseconds as canonical timestamps,
- completed-bar-only strategy policy,
- dataset versioning and manifests,
- live market-data stream behavior,
- partial-candle restrictions,
- live 15m/1h alignment,
- mark-price context,
- stale market-data gating.

Remaining data doc:

```text
docs/04-data/data-requirements.md
```

This should become a concise requirements/index bridge tying together historical data, live data, timestamp, dataset versioning, and validation data needs.

---

## 3. Backtesting and Validation

Important document:

```text
docs/05-backtesting-validation/v1-breakout-validation-checklist.md
```

Defined:

- promotion gates,
- data integrity checks,
- strategy conformity checks,
- simulation realism checks,
- robustness checks,
- exit model comparison,
- risk profile review,
- execution readiness review,
- paper/shadow and tiny-live candidate requirements.

---

## 4. Execution and Exchange

Important documents:

```text
docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md
```

Defined:

- market entry after completed 15m signal close,
- normal MARKET entry order model,
- algo/conditional STOP_MARKET protective stop model,
- deterministic client IDs,
- normal order IDs versus algo order IDs,
- ACK preferred for initial market entry response,
- REST acknowledgement not final truth,
- user stream as live private-state source,
- ORDER_TRADE_UPDATE / ACCOUNT_UPDATE / ALGO_UPDATE responsibilities,
- stream staleness and reconciliation behavior,
- clean flat state,
- clean protected-position state,
- unknown execution outcome handling,
- orphaned/multiple stop handling,
- manual/non-bot exposure handling,
- exchange adapter boundaries.

Remaining execution docs:

```text
docs/06-execution-exchange/failure-recovery.md
docs/06-execution-exchange/position-state-model.md
```

`user-stream-reconciliation.md` is now completed and should not be treated as remaining.

---

## 5. Risk

Important documents:

```text
docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/kill-switches.md
docs/07-risk/daily-loss-rules.md
docs/07-risk/drawdown-controls.md
```

Defined:

### Position sizing

- sizing from stop distance and equity risk,
- sizing equity should use strategy allocation boundary,
- initial live risk 0.25%,
- future path toward 1% risk only after staged review,
- initial risk-usage buffer 90%,
- quantity rounded down,
- below-minimum quantity rejects,
- leverage cap and notional cap enforcement,
- missing metadata/equity/bracket/state fails closed.

### Exposure limits

- BTCUSDT only live,
- ETHUSDT research-only,
- one position maximum,
- no pyramiding,
- no reversal entry while positioned,
- pending entry/unknown status counts as exposure,
- manual/non-bot exposure blocks new entries,
- internal notional cap mandatory.

### Stop-loss policy

- no stop, no trade,
- sizing stop must match protection stop,
- stop submission is not stop confirmation,
- stop widening forbidden in v1,
- cancel-and-replace stop updates,
- unprotected live position is emergency,
- one deterministic restore-protection attempt is allowed only if state is clear,
- otherwise flatten or block awaiting operator under emergency policy.

### Kill switch

- distinct from pause,
- blocks entries and normal strategy progression,
- suspends normal trailing/profit optimization,
- allows deterministic safety actions,
- persists across restart,
- never auto-clears,
- requires operator action and clean safety conditions to clear.

### Daily loss

- UTC daily session,
- tiny-live warning around -0.50%,
- tiny-live lockout at -0.75% or 3 full-risk losses,
- hard review around -1.00% or abnormal loss behavior,
- normal loss lockout is not automatically kill switch,
- daily reset does not clear incidents/kill switch/reconciliation problems.

### Drawdown

- measured from strategy equity high watermark,
- tiny-live watch -1.0%,
- caution -1.5%,
- pause -2.0%,
- hard review -3.0%,
- caution blocks risk increases,
- pause blocks new entries,
- abnormal drawdown escalates to incident/kill-switch policy.

---

## 6. Runtime Architecture

Important documents:

```text
docs/08-architecture/implementation-blueprint.md
docs/08-architecture/codebase-structure.md
docs/08-architecture/state-model.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/observability-design.md
```

Defined:

- modular monolith architecture,
- component ownership boundaries,
- strategy/risk/execution separation,
- runtime modes,
- trade lifecycle states,
- protection states,
- reconciliation states,
- control flags,
- commands/events/queries,
- message envelope,
- durable persistence requirements,
- restart-critical entities,
- state-centric observability,
- health dimensions,
- alert philosophy.

Remaining architecture docs:

```text
docs/08-architecture/database-design.md
docs/08-architecture/deployment-model.md
docs/08-architecture/event-flows.md
```

---

## 7. Operations

Important documents:

```text
docs/09-operations/restart-procedure.md
docs/09-operations/incident-response.md
docs/09-operations/operator-workflow.md
docs/09-operations/daily-weekly-review-process.md
docs/09-operations/release-process.md
```

Defined:

- safe-mode-first restart,
- reconciliation before resumption,
- clean/recoverable/unsafe mismatch classification,
- incident severity model,
- containment-first incident response,
- operator responsibilities,
- allowed manual actions,
- daily/weekly review cadence,
- release stages and promotion gates.

Remaining operations doc:

```text
docs/09-operations/rollback-procedure.md
```

---

## 8. Security

Important documents:

```text
docs/10-security/api-key-policy.md
docs/10-security/secrets-management.md
docs/10-security/permission-scoping.md
```

Defined:

- least privilege,
- no withdrawal permission,
- production IP restriction,
- environment separation,
- role-based credential thinking,
- secrets never in code/git/docs/screenshots/chats/logs,
- fail-closed credential behavior,
- key rotation/revocation principles.

Remaining security docs:

```text
docs/10-security/audit-logging.md
docs/10-security/disaster-recovery.md
docs/10-security/host-hardening.md
```

---

## 9. Operator Interface

Important document:

```text
docs/11-interface/operator-dashboard-requirements.md
```

Defined:

- dashboard is supervision/control surface,
- top-level runtime status,
- connectivity/stream health,
- position/protection panel,
- reconciliation/restart panel,
- incidents and alerts,
- recent important events,
- limited manual controls,
- confirmation/guardrail expectations.

Remaining interface docs:

```text
docs/11-interface/alerting-ui.md
docs/11-interface/approval-workflows.md
docs/11-interface/dashboard-metrics.md
docs/11-interface/manual-control-actions.md
```

These should mostly refine or split the existing dashboard requirements rather than contradict them.

---

## 10. Roadmap / Governance

Remaining roadmap docs:

```text
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
```

These should be completed before the AI coding handoff.

---

## AI Coding Handoff Status

The AI coding handoff has **not** been created yet.

Planned path:

1. Finish remaining high-value TBD docs.
2. Convert low-value duplicate TBDs into bridge/superseded docs or remove them.
3. Update this current-project-state document again if needed.
4. Create:

```text
docs/00-meta/ai-coding-handoff.md
```

The AI coding handoff should include:

- repository reading order,
- authoritative docs list,
- coding phase plan,
- hard safety constraints,
- module-by-module implementation sequence,
- what Claude Code must not change,
- required tests before live-like operation,
- explicit instruction not to wire real trading before dry-run/paper gates,
- and final pre-implementation checklist.

---

## Remaining TBD Document Plan

The following plan should guide the next chat.

### `docs/04-data/data-requirements.md`

Recommended treatment: bridge / concise requirements index.

Purpose:

- summarize required historical and live data,
- link historical data spec, live data spec, timestamp policy, dataset versioning, and validation checklist,
- avoid duplicating all detailed schemas,
- define must-have data before backtesting, paper/shadow, and tiny live.

### `docs/06-execution-exchange/failure-recovery.md`

Recommended treatment: full document.

Purpose:

- define execution-specific failure modes and recovery behavior,
- cover REST timeout after submit, unknown order status, stop submission failure, stop replacement failure, cancel ambiguity, stale stream during active exposure, rate-limit/IP-ban risk,
- connect order model, user-stream reconciliation, incident response, stop policy, and restart procedure,
- emphasize no blind retry for exposure-changing actions.

### `docs/06-execution-exchange/position-state-model.md`

Recommended treatment: bridge / exchange-specific state document.

Purpose:

- define Binance position facts that Prometheus normalizes,
- map exchange position state to internal runtime position/protection state,
- clarify one-way mode, isolated margin, flat/long/short states, position size signs, position-side assumptions, manual/non-bot exposure,
- avoid duplicating the full architecture state model.

### `docs/08-architecture/database-design.md`

Recommended treatment: full implementation-support document.

Purpose:

- define v1 database/storage design,
- separate runtime DB from historical Parquet/DuckDB research storage,
- define entities for runtime control, active trade, protection, reconciliation, incidents, operator actions, daily loss, drawdown, event log,
- include migration/versioning principles,
- avoid overengineering distributed database architecture.

### `docs/08-architecture/deployment-model.md`

Recommended treatment: full document.

Purpose:

- define local/dev, validation, paper/shadow, tiny-live, scaled-live deployment models,
- define process boundaries, configuration loading, secrets boundaries, host assumptions, restart behavior, log paths, operator access,
- connect release process, permission scoping, host hardening, and disaster recovery.

### `docs/08-architecture/event-flows.md`

Recommended treatment: full diagram-like document.

Purpose:

- define text sequence flows for:
  - completed bar to signal,
  - signal to risk approval,
  - entry to position confirmation,
  - position to protective stop confirmation,
  - stop replacement,
  - normal exit,
  - restart reconciliation,
  - user-stream gap,
  - emergency unprotected position,
  - daily/drawdown lockout,
  - kill-switch activation and clearance.
- This will be very useful for Claude Code.

### `docs/09-operations/rollback-procedure.md`

Recommended treatment: full document.

Purpose:

- define rollback for code, configuration, strategy parameters, risk settings, deployment environment, and documentation,
- clarify that rollback does not bypass reconciliation,
- define when rollback is blocked by live exposure,
- require safe mode/reconciliation/operator review before and after rollback,
- connect release process and incident response.

### `docs/10-security/audit-logging.md`

Recommended treatment: full / medium security-observability bridge.

Purpose:

- define audit log requirements for operator actions, credential events, config changes, release changes, kill-switch actions, overrides, recovery approvals, emergency flattening,
- define immutability expectations, retention, redaction, and reviewability,
- connect observability and security docs.

### `docs/10-security/disaster-recovery.md`

Recommended treatment: full document.

Purpose:

- define recovery from host loss, database corruption, credential compromise, lost logs, exchange/API disruption, repo/config corruption, and operator machine loss,
- define backups, restore testing, key revocation/rotation, safe-mode-first rebuild,
- connect restart procedure, secrets, host hardening, incident response.

### `docs/10-security/host-hardening.md`

Recommended treatment: full document.

Purpose:

- define production host security baseline,
- OS updates, firewall, least privilege, process user, SSH hygiene, outbound IP stability, logging permissions, time sync, dependency update policy, secret file permissions,
- connect API key IP restriction and deployment model.

### `docs/11-interface/alerting-ui.md`

Recommended treatment: bridge / interface supplement.

Purpose:

- define how alerts appear to operator,
- severity display, acknowledgement, escalation, grouping, quieting rules, and alert history,
- avoid duplicating observability design.

### `docs/11-interface/approval-workflows.md`

Recommended treatment: full interface/operations document.

Purpose:

- define operator approvals for:
  - live enablement,
  - recovery resumption,
  - kill-switch clearance,
  - daily lockout override,
  - drawdown pause clearance,
  - risk increase,
  - leverage/notional cap increase,
  - release promotion,
  - emergency flatten confirmation where applicable.
- This should connect operator workflow, release process, risk docs, and dashboard requirements.

### `docs/11-interface/dashboard-metrics.md`

Recommended treatment: bridge / metrics catalog.

Purpose:

- enumerate dashboard metrics and status fields,
- group by runtime, stream, position/protection, risk, daily loss, drawdown, reconciliation, incidents, security, release,
- avoid full UI design.

### `docs/11-interface/manual-control-actions.md`

Recommended treatment: full safety-control document.

Purpose:

- define exact allowed manual controls,
- confirmation requirements,
- disabled states,
- backend command generated,
- audit requirements,
- forbidden controls,
- guardrails against discretionary manual trading.

### `docs/12-roadmap/phase-gates.md`

Recommended treatment: full governance document.

Purpose:

- define stage gates from research to validation to paper/shadow to tiny live to scaled live,
- define entry/exit criteria per phase,
- define evidence required for risk increase toward 1%,
- define evidence required for leverage increase,
- define documents/tests required before Claude Code and before live.

### `docs/12-roadmap/technical-debt-register.md`

Recommended treatment: living register / medium document.

Purpose:

- record accepted deferrals and known future work,
- classify by risk, owner, phase, and blocking status,
- prevent forgotten TODOs from becoming hidden assumptions,
- distinguish pre-Claude blockers from post-MVP improvements.

### `docs/00-meta/ai-coding-handoff.md`

Recommended treatment: final meta document after remaining docs.

Purpose:

- create the final Claude Code handoff,
- define repo reading order,
- summarize locked decisions,
- specify coding phases,
- forbid unsafe shortcuts,
- define implementation/test expectations,
- define what not to build yet,
- make dry-run/paper-first execution mandatory.

---

## Remaining Document Priority Order

Recommended next order:

1. `docs/06-execution-exchange/failure-recovery.md`
2. `docs/06-execution-exchange/position-state-model.md`
3. `docs/08-architecture/event-flows.md`
4. `docs/08-architecture/database-design.md`
5. `docs/08-architecture/deployment-model.md`
6. `docs/09-operations/rollback-procedure.md`
7. `docs/10-security/audit-logging.md`
8. `docs/10-security/host-hardening.md`
9. `docs/10-security/disaster-recovery.md`
10. `docs/11-interface/manual-control-actions.md`
11. `docs/11-interface/approval-workflows.md`
12. `docs/11-interface/dashboard-metrics.md`
13. `docs/11-interface/alerting-ui.md`
14. `docs/04-data/data-requirements.md`
15. `docs/12-roadmap/phase-gates.md`
16. `docs/12-roadmap/technical-debt-register.md`
17. `docs/00-meta/ai-coding-handoff.md`

Reasoning:

- failure recovery and position state are closest to live trading safety,
- event flows are highly useful before coding,
- database/deployment/rollback/security/interface docs turn architecture into implementation constraints,
- data requirements can be a concise bridge because stronger data docs already exist,
- phase gates and technical debt should be finalized right before the AI coding handoff.

---

## Current 25-File ChatGPT Project Upload Recommendation

Because ChatGPT project files are limited to 25, the project files should act as a compact continuity cache, not the entire source of truth.

The repository should remain public and should still be inspected by the next chat.

Recommended 25 project files:

```text
docs/00-meta/current-project-state.md

docs/03-strategy-research/v1-breakout-strategy-spec.md
docs/05-backtesting-validation/v1-breakout-validation-checklist.md

docs/04-data/historical-data-spec.md
docs/04-data/live-data-spec.md
docs/04-data/timestamp-policy.md
docs/04-data/dataset-versioning.md

docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md

docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/kill-switches.md
docs/07-risk/daily-loss-rules.md
docs/07-risk/drawdown-controls.md

docs/08-architecture/implementation-blueprint.md
docs/08-architecture/state-model.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/observability-design.md

docs/09-operations/restart-procedure.md
docs/09-operations/incident-response.md

docs/11-interface/operator-dashboard-requirements.md
```

If working specifically on security docs, temporarily swap in:

```text
docs/10-security/api-key-policy.md
docs/10-security/secrets-management.md
docs/10-security/permission-scoping.md
```

by temporarily removing less relevant strategy/data docs, because the repository remains the full source of truth.

---

## Implementation Readiness Status

The project is **not ready yet** for Claude Code to start full implementation.

It is close, but the remaining TBD files should be triaged and completed first.

Current readiness:

```text
Strategy/research: strong
Historical/live data design: strong
Risk model: strong
Execution model: strong but missing failure-recovery and position-state bridge
Runtime architecture: strong but missing event-flows/database/deployment detail
Operations: strong but missing rollback procedure
Security: strong base but missing audit/host/disaster docs
Interface: strong base but missing detailed controls/metrics/approval/alert supplements
Roadmap/governance: missing phase gates and technical debt register
AI coding handoff: pending
```

---

## Immediate Next Task

The next chat should:

1. Inspect the repository.
2. Confirm remaining TBD placeholder files.
3. Use this current-project-state document as the high-level checkpoint.
4. Continue with the same method:
   - discuss decision space,
   - recommend final policy,
   - wait for approval,
   - then write the Markdown file.
5. Start with:

```text
docs/06-execution-exchange/failure-recovery.md
```

unless repository inspection reveals a more urgent blocker.

---

## Document Status

- Status: ACTIVE
- Updated: 2026-04-18
- Owner: Project operator
- Role: High-level project memory checkpoint
