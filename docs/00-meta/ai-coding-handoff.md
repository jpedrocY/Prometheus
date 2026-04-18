# AI Coding Handoff

## Purpose

This document is the implementation handoff for AI-assisted coding of the Prometheus trading-system repository.

Its purpose is to tell Claude Code, or any other implementation agent, how to approach the repository safely, in what order to read the documentation, what decisions are already locked, what must not be changed casually, how to implement the system phase by phase, and what evidence must be produced before moving closer to real exchange connectivity or real capital exposure.

This is not a casual prompt.

This is an implementation control document.

Prometheus v1 is a safety-first, rules-based, operator-supervised trading system for Binance USDⓈ-M futures. It must be built in phases, with runnable checkpoints, reviewable outputs, and explicit operator approval before promotion.

---

## Scope

This handoff applies to initial code implementation, local development setup, dry-run runtime construction, paper/shadow preparation, tiny-live preparation, and future scaled-live preparation.

It applies to:

- repository intake,
- documentation review,
- codebase setup,
- dependency installation,
- local development,
- data layer implementation,
- backtesting implementation,
- strategy implementation,
- risk implementation,
- runtime state implementation,
- persistence implementation,
- dashboard and alerting implementation,
- fake exchange / dry-run implementation,
- paper/shadow preparation,
- tiny-live preparation,
- and staged handoff reports.

It does not authorize:

- one-shot implementation of the entire trading system,
- production exchange-write capability during early phases,
- creation of production Binance trade-capable API keys during local development,
- bypassing documented phase gates,
- bypassing operator approval,
- replacing safety-first design with convenience behavior,
- discretionary manual trading features,
- or live autonomous operation without supervision.

---

## Authority Hierarchy

Implementation must follow this authority hierarchy:

1. Repository Markdown files are the primary source of truth.
2. Specialist documents win for their own domain.
3. This handoff controls implementation method, sequencing, and reporting.
4. `docs/00-meta/current-project-state.md` controls high-level project status.
5. `docs/12-roadmap/phase-gates.md` controls phase promotion and gating.
6. `docs/12-roadmap/technical-debt-register.md` controls known debt, deferrals, and blocking status.
7. Chat history and external memory are secondary and must not override repository documentation.
8. If Binance official documentation conflicts with repository assumptions, implementation must stop, record the conflict, and request review before live-capable behavior is implemented.

Specialist ownership examples:

- Strategy rules: `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- Validation gates: `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
- Data requirements: `docs/04-data/data-requirements.md`
- Timestamp rules: `docs/04-data/timestamp-policy.md`
- Live data behavior: `docs/04-data/live-data-spec.md`
- Exchange adapter boundaries: `docs/06-execution-exchange/exchange-adapter-design.md`
- Binance order model: `docs/06-execution-exchange/binance-usdm-order-model.md`
- User-stream reconciliation: `docs/06-execution-exchange/user-stream-reconciliation.md`
- Failure recovery: `docs/06-execution-exchange/failure-recovery.md`
- Position state: `docs/06-execution-exchange/position-state-model.md`
- Sizing: `docs/07-risk/position-sizing-framework.md`
- Exposure gates: `docs/07-risk/exposure-limits.md`
- Stops: `docs/07-risk/stop-loss-policy.md`
- Kill switches: `docs/07-risk/kill-switches.md`
- Runtime state: `docs/08-architecture/state-model.md`
- Persistence: `docs/08-architecture/runtime-persistence-spec.md`
- Database design: `docs/08-architecture/database-design.md`
- Event contracts: `docs/08-architecture/internal-event-contracts.md`
- Event flows: `docs/08-architecture/event-flows.md`
- Deployment: `docs/08-architecture/deployment-model.md`
- Host hardening: `docs/10-security/host-hardening.md`
- First-run setup: `docs/09-operations/first-run-setup-checklist.md`

---

## Repository and Operator Context

Repository:

```text
https://github.com/jpedrocY/Prometheus
```

At the time of this handoff, the operator already has:

- repository cloned locally at:

```text
C:\Prometheus
```

- repository tracked with GitHub Desktop,
- repository folder open in AntiGravity IDE,
- Claude Code extension installed,
- Claude Code logged into a Max plan account,
- ChatGPT project workspace available for external review, setup guidance, debugging, documentation continuity, screenshot interpretation, and operational planning.

Claude Code should not waste setup effort on creating the GitHub repository or cloning it from scratch unless the local checkout is missing or corrupt.

Claude Code must still verify:

- current repository contents,
- current branch,
- working tree status,
- existing code layout,
- existing package/tooling files,
- available tests,
- documentation map freshness,
- and whether implementation conventions already exist.

Do not assume:

- dependencies are installed,
- Python/tooling choices are final unless present in repo files,
- tests already pass,
- runtime directories exist,
- dashboard code exists,
- Binance credentials exist,
- exchange-write capability is allowed,
- or the current machine is the final live NUC.

---

## Current Implementation Status

The project is leaving documentation/pre-implementation planning and preparing for phased implementation.

The expected near-term status is:

- high-value architecture and safety docs exist,
- first-run setup checklist exists,
- this AI coding handoff exists,
- current project state is updated,
- implementation has not yet been completed,
- execution layer must be built late,
- dry-run and paper/shadow stages must happen before tiny live,
- production Binance trade-capable keys must not be requested or created during early coding phases.

Prometheus v1 is:

- rules-based,
- safety-first,
- operator-supervised,
- not self-learning live AI,
- not lights-out autonomous,
- staged from research to validation to dry-run to paper/shadow to tiny live.

---

## Locked V1 Decisions

### Market and venue

- Venue: Binance USDⓈ-M futures.
- Initial live symbol: BTCUSDT perpetual.
- ETHUSDT perpetual is research/comparison only.
- V1 live scope: one live symbol.
- V1 live symbol: BTCUSDT only unless separately approved in future documentation.
- One-way mode.
- Isolated margin.

### Strategy

- Strategy family: breakout continuation with higher-timeframe trend filter.
- Signal timeframe: 15m.
- Higher-timeframe bias: 1h.
- Completed bars only.
- Entry style: completed 15m bar confirmation, then market entry.
- Higher-timeframe bias must use completed 1h bars only.
- Baseline backtest fill assumption: next-bar open after confirmed signal close.
- Initial stop: structural stop plus ATR buffer.
- Trade management: staged risk reduction and strategy-managed trailing.
- No intrabar signal confirmation in v1.

### Live execution scope

- One symbol.
- One position maximum.
- One active protective stop maximum.
- No pyramiding.
- No reversal entry while positioned.
- No hedge-mode behavior.
- No multi-symbol live orchestration.
- No portfolio routing.
- No discretionary chart trading.

### Orders and protection

- Entry order: normal MARKET order.
- Protective stop: exchange-side STOP_MARKET algo/conditional order.
- Protective stop required settings:
  - `closePosition=true`
  - `workingType=MARK_PRICE`
  - `priceProtect=TRUE`
- Stop updates: cancel-and-replace.
- A filled entry is not yet a protected trade.
- A submitted stop is not yet confirmed protection.
- A position without confirmed protective stop coverage is an emergency.

### State and reconciliation

- User stream is the primary private live-state source.
- REST is used for placement, cancellation, reconciliation, and recovery.
- Exchange state is authoritative.
- Commands are not facts.
- REST acknowledgements are not final truth.
- Unknown execution outcomes fail closed.
- No blind retry for exposure-changing actions.
- Restart always begins in SAFE_MODE.
- Reconciliation is required before normal resumption after startup or confidence loss.

### Risk

- Initial live risk per trade: 0.25% of sizing equity.
- Initial effective leverage cap: 2x.
- Internal notional cap is mandatory before live operation.
- Leverage is a tool to express approved risk size, not a target.
- Future risk increases require evidence and explicit operator approval.
- Future leverage increases require evidence and explicit operator approval.

### Deployment

- V1 is supervised.
- Default tiny-live host: dedicated local NUC / mini PC used only for Prometheus.
- NUC has an attached desk monitor.
- Operator dashboard should be visible whenever the monitor is on during operation.
- Telegram and/or n8n may be used for alerts.
- Telegram/n8n must not initially approve high-risk actions.
- Production Binance keys must not be created until the correct phase gate.

---

## Non-Negotiable Safety Constraints

Claude Code must preserve these constraints at all times:

1. No production exchange-write capability before the approved phase gate.
2. No production Binance trade-capable API key creation during local development, validation, or early dry-run.
3. No real order placement until documentation, tests, dry-run, paper/shadow, security, host, and operator-readiness gates have passed.
4. No blind retry for any action that may change exposure or protection.
5. No strategy code directly importing Binance clients.
6. No risk code placing orders.
7. No UI or dashboard bypassing backend safety gates.
8. No hidden manual discretionary trading terminal.
9. No manual buy/sell buttons in v1.
10. No stop widening in v1.
11. No pyramiding in v1.
12. No reversal entry while positioned in v1.
13. No hedge-mode behavior in v1.
14. No multi-symbol live trading in v1.
15. No treating local state as exchange truth.
16. No treating REST acknowledgement as final truth.
17. No treating submitted stop as confirmed protection.
18. No running normal live operation with uncertain position/protection state.
19. No automatic clearing of kill switch.
20. No secrets in git, logs, docs, prompts, screenshots, database rows, test snapshots, or generated reports.

If a requested implementation step would violate any of these constraints, Claude Code must stop and report the conflict.

---

## What Claude Code Must Not Do

Claude Code must not:

- implement the entire project in one broad generation,
- skip repository audit,
- silently change locked v1 assumptions,
- remove safety gates for convenience,
- invent undocumented trading rules,
- optimize strategy parameters without recording variants,
- add self-learning live behavior,
- add autonomous live strategy switching,
- implement discretionary manual trading,
- request production Binance keys in early phases,
- hardcode secrets or credentials,
- log secrets or signed payloads,
- create unreviewed live-write paths,
- treat fake adapter success as live readiness,
- treat backtest profitability as live readiness,
- treat paper/shadow success as automatic tiny-live approval,
- treat tiny-live success as automatic scaled-live approval,
- or proceed through phase gates without explicit operator review.

---

## Required Reading Order

Before implementation, Claude Code must inspect the repository Markdown files in this order.

### 1. Project state and governance

```text
docs/00-meta/current-project-state.md
docs/00-meta/ai-coding-handoff.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
docs/README.md
```

### 2. Setup and deployment

```text
docs/09-operations/first-run-setup-checklist.md
docs/08-architecture/deployment-model.md
docs/10-security/host-hardening.md
docs/10-security/secrets-management.md
docs/10-security/api-key-policy.md
docs/10-security/permission-scoping.md
docs/10-security/disaster-recovery.md
```

### 3. Strategy, data, and validation

```text
docs/03-strategy-research/v1-breakout-strategy-spec.md
docs/03-strategy-research/v1-breakout-backtest-plan.md
docs/04-data/data-requirements.md
docs/04-data/historical-data-spec.md
docs/04-data/live-data-spec.md
docs/04-data/timestamp-policy.md
docs/04-data/dataset-versioning.md
docs/05-backtesting-validation/v1-breakout-validation-checklist.md
```

### 4. Execution and exchange

```text
docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md
docs/06-execution-exchange/failure-recovery.md
docs/06-execution-exchange/position-state-model.md
```

### 5. Risk

```text
docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/daily-loss-rules.md
docs/07-risk/drawdown-controls.md
docs/07-risk/kill-switches.md
```

### 6. Architecture

```text
docs/08-architecture/implementation-blueprint.md
docs/08-architecture/codebase-structure.md
docs/08-architecture/state-model.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/database-design.md
docs/08-architecture/event-flows.md
docs/08-architecture/observability-design.md
```

### 7. Operations and interface

```text
docs/09-operations/restart-procedure.md
docs/09-operations/incident-response.md
docs/09-operations/operator-workflow.md
docs/09-operations/release-process.md
docs/09-operations/rollback-procedure.md
docs/09-operations/daily-weekly-review-process.md
docs/11-interface/operator-dashboard-requirements.md
docs/11-interface/dashboard-metrics.md
docs/11-interface/alerting-ui.md
docs/11-interface/manual-control-actions.md
docs/11-interface/approval-workflows.md
```

If a file listed here is missing, renamed, or stale, Claude Code must record that in the repo-audit report instead of guessing.

---

## Implementation Philosophy

Prometheus must be implemented as a phased, testable, reviewable system.

The correct build direction is:

```text
repository audit
→ local development foundation
→ data layer
→ validation/backtesting
→ strategy conformance
→ risk and sizing
→ runtime state and persistence
→ observability/dashboard/alerts
→ fake exchange and dry-run
→ paper/shadow
→ tiny live
→ scaled live
```

Execution comes late.

Real exchange-write capability comes very late.

Every phase must end with:

- runnable checkpoint,
- commands run,
- outputs captured,
- tests/checks reported,
- changed files listed,
- known gaps documented,
- safety constraints checked,
- and next phase proposed.

Claude Code must prefer small, reviewable increments over large opaque changes.

---

## Dual-AI Implementation Workflow

This project uses a deliberate three-way workflow:

```text
Claude Code = implementation executor inside the repository
ChatGPT = setup/review/debugging/documentation guide
Operator = approval authority and physical/system operator
```

Claude Code should:

- implement code and repo changes,
- run local commands where appropriate,
- install project/phase dependencies where safe,
- produce checkpoint reports,
- stop on unclear installation, system, security, or phase-gate issues,
- and provide copy-paste escalation prompts for ChatGPT when needed.

ChatGPT will:

- help the operator interpret errors, logs, screenshots, photos, IDE state, GitHub Desktop state, terminal output, dashboard output, alert-route output, and setup status,
- guide manual installations or external-account steps where Claude Code cannot proceed,
- help review phase reports,
- help refine prompts back to Claude Code,
- and preserve continuity of the project decisions.

The operator will:

- approve phase starts,
- approve phase promotions,
- perform external/account/system actions when required,
- provide screenshots/logs/output to ChatGPT when needed,
- and decide when to return to Claude Code.

Claude Code should produce clear outputs that the operator can paste into ChatGPT for independent review.

---

## Claude Code Installation Authority

Claude Code may perform installation and setup actions that are necessary for the currently approved phase, provided they are local, project-relevant, and not safety-sensitive.

Allowed examples:

- create or activate a Python virtual environment,
- install Python project dependencies from repo-defined files,
- add or update dependency files when part of the active phase,
- install development tooling required by the repo,
- initialize local test tooling,
- initialize local runtime database files for fake/dry-run stages,
- create local non-secret config templates,
- create local directories for logs, reports, data, and runtime state,
- run migrations in local development or dry-run contexts,
- run linting, formatting, type checks, and tests,
- run local fake-adapter runtime checks,
- run local dashboard prototypes without live exchange-write capability.

Claude Code must stop and request operator/ChatGPT guidance before:

- broad system-level package installation outside the project context,
- administrative shell changes that affect the host globally,
- firewall changes,
- SSH/security changes,
- Windows service or Linux systemd installation,
- NUC host-hardening actions,
- external account setup,
- Binance account/API setup,
- Telegram bot creation,
- n8n deployment or credential setup,
- production secrets management,
- real exchange connectivity with write capability,
- or any action that could affect real funds.

---

## Installation Safety Boundaries

Installation must preserve these boundaries:

1. Local development and validation must not require production trade-capable keys.
2. Dry-run must not send real exchange orders.
3. Paper/shadow must not place production orders unless a later documented mode explicitly permits tightly scoped behavior.
4. Tiny-live requires explicit gate approval before production write keys or real capital exposure.
5. Secrets must remain outside git.
6. Generated `.env` or config templates must be examples only unless explicitly ignored and local.
7. Claude Code must never paste real secrets into files, logs, prompts, comments, tests, or reports.
8. If an installer requests broad permissions or unclear system changes, stop and escalate.
9. If a dependency or package looks suspicious, abandoned, or unrelated to the repo plan, stop and ask.
10. If installation fails repeatedly, stop and provide an escalation prompt rather than improvising risky fixes.

---

## ChatGPT Setup Escalation Protocol

When Claude Code cannot safely complete an installation, configuration, environment, account, permission, system, or tooling step, it must stop and give the operator a copy-paste prompt for ChatGPT.

Use this format:

```md
## ChatGPT Setup Escalation Prompt

I am implementing Prometheus in Claude Code.

Current phase:
Current goal:
Machine/OS:
Repo path:
Current branch:
Working tree status:
Command attempted:
Full error/output:
What Claude Code thinks is missing:
What installation or configuration appears needed:
Why Claude Code stopped:
Safety constraints to preserve:
Files changed so far:
Commands already run:
Question for ChatGPT:
```

The operator will bring that prompt to ChatGPT.

After ChatGPT guides the operator through the issue, the operator should return to Claude Code with a confirmation such as:

```text
The required setup step has been completed and reviewed with ChatGPT.
Continue from the previous checkpoint.
Do not skip the phase acceptance criteria.
Report any new errors with full command output.
```

Claude Code must then resume from the prior phase checkpoint, not skip ahead.

---

## Runnable Checkpoint Review Protocol

At the end of every phase, Claude Code must produce a checkpoint report.

Use this format:

```md
## Phase Checkpoint Report

Phase:
Goal:
Summary:
Files changed:
Files created:
Files deleted:
Commands run:
Installations performed:
Configuration created or changed:
Tests/checks passed:
Tests/checks failed:
Runtime output:
Screenshots or artifacts to capture:
Known gaps:
Spec ambiguities found:
Technical-debt updates needed:
Safety constraints verified:
Current runtime capability:
Exchange connectivity status:
Exchange-write capability status:
Recommended next step:
Question for ChatGPT/operator, if any:
```

The operator may paste this report into ChatGPT for independent review before approving the next phase.

Claude Code must not treat the checkpoint as automatically approved.

---

## Ambiguity and Spec-Gap Protocol

Claude Code must not guess silently.

If implementation finds a missing requirement, contradiction, ambiguity, stale doc reference, missing command, unclear dependency, unclear API behavior, or unsafe assumption, it must record it.

Preferred handling:

1. Pause the affected implementation area.
2. Write a concise ambiguity entry.
3. Propose safe options.
4. Recommend one option.
5. Ask for operator approval before proceeding if the issue affects safety, exchange behavior, state truth, risk, persistence, deployment, or phase gates.

During implementation, create and maintain:

```text
docs/00-meta/implementation-ambiguity-log.md
```

unless the operator explicitly chooses to track all items only inside:

```text
docs/12-roadmap/technical-debt-register.md
```

Minimum ambiguity-log entry format:

```md
## GAP-YYYYMMDD-NNN — Title

Status:
Phase discovered:
Area:
Blocking phase:
Risk level:
Related docs:
Description:
Why it matters:
Options:
Recommended resolution:
Operator decision:
Resolution evidence:
```

Safety-relevant gaps must also be reflected in the technical-debt register if they remain open.

---

## Expected Claude Code Reporting Style

Claude Code should report clearly and concretely.

Each implementation response should include:

- what was done,
- why it was done,
- files changed,
- commands run,
- test results,
- unresolved issues,
- whether the phase remains within allowed capability,
- and what should happen next.

Avoid vague claims such as:

```text
Everything is done.
```

Prefer evidence:

```text
pytest passed: 84 tests
ruff passed
mypy passed
dry-run startup begins in SAFE_MODE
fake adapter rejects live-write mode
```

When a command fails, include the exact command and full relevant output.

---

# Implementation Phases

## Phase 0 — Handoff Intake and Repo Audit

### Purpose

Inspect the repository, confirm current state, verify documentation, identify existing code/tooling, and propose Phase 1 implementation only.

### Claude Code may

- read repository files,
- inspect git status,
- inspect docs,
- inspect existing code,
- inspect package/tooling files,
- identify stale references,
- identify missing files,
- prepare a repo-audit report,
- propose Phase 1.

### Claude Code must not

- implement broad application code,
- create exchange-write logic,
- request credentials,
- change strategy rules,
- skip docs,
- or proceed directly to full implementation.

### Required checks

- Confirm repository path.
- Confirm current branch.
- Confirm working tree status.
- Identify top-level layout.
- Identify existing source code.
- Identify existing tests.
- Identify dependency manager, if any.
- Identify Python version constraints, if any.
- Identify documentation files present/missing.
- Identify stale README/doc-map references.
- Identify immediate blockers to Phase 1.

### Runnable checkpoint

At the end of Phase 0, produce a repo-audit report.

### Acceptance criteria

- Required reading order was followed or missing files were reported.
- Current implementation status is clearly summarized.
- Existing tooling state is documented.
- No broad code generation occurred.
- Phase 1 plan is proposed for approval.

---

## Phase 1 — Local Development Foundation

### Purpose

Create a safe local development foundation that can run tests, linting, formatting, and basic project commands without live exchange capability.

### Build only what is needed for

- package structure,
- dependency management,
- test framework,
- formatting/lint/type-check framework,
- basic configuration model,
- safe local config templates,
- fake/no-op runtime foundation,
- local directories for logs/reports/runtime state,
- developer documentation updates.

### Claude Code may install

- project Python dependencies,
- test tools,
- formatting/lint tools,
- type-check tools,
- local development dependencies,
- only if they are relevant and recorded.

### Claude Code must not

- require production Binance credentials,
- implement real exchange write behavior,
- store secrets in repo,
- install unrelated global software without escalation,
- or create live-running services.

### Runnable checkpoint

A local command set should run successfully, such as:

```text
install dependencies
run tests
run lint/format check
run type check where configured
run a minimal safe CLI or package import check
```

Exact commands depend on repo tooling.

### Acceptance criteria

- Project can be installed locally.
- Tests can run.
- Lint/format/type-check path exists or is explicitly deferred.
- No production credentials are required.
- No exchange-write capability exists.
- Local config examples are safe and non-secret.
- Any setup commands are documented.
- First ambiguity log may be created if needed.

---

## Phase 2 — Historical Data and Validation Foundation

### Purpose

Implement the historical data foundation needed for reproducible research and validation.

### Build only what is needed for

- historical data directory conventions,
- dataset manifests,
- Binance USDⓈ-M historical kline ingestion design,
- normalized data models,
- UTC millisecond timestamp handling,
- open-time bar identity,
- Parquet/DuckDB support where selected,
- dataset versioning,
- validation data checks,
- sample fixtures,
- data-quality tests.

### Claude Code may install

- data-processing dependencies,
- DuckDB/Parquet libraries,
- validation/reporting dependencies,
- only if phase-relevant and recorded.

### Claude Code must not

- mix research storage with runtime database,
- silently overwrite validated dataset versions,
- forward-fill missing bars without explicit invalid-window logging,
- use local timezone as canonical time,
- or request production exchange credentials.

### Runnable checkpoint

A small sample dataset or fixture should be ingested/validated with tests proving:

- UTC millisecond handling,
- `symbol + interval + open_time` bar identity,
- completed-bar-only assumptions,
- basic data-quality checks,
- and dataset manifest behavior.

### Acceptance criteria

- Historical data path is reproducible.
- Timestamp policy is enforced in tests.
- Data integrity checks exist.
- Dataset versioning is represented.
- BTCUSDT and ETHUSDT research requirements are supported in design.
- No live runtime state is mixed into research storage.

---

## Phase 3 — Backtesting and Strategy Conformance

### Purpose

Implement backtesting and strategy logic according to the v1 breakout specification.

### Build only what is needed for

- v1 breakout strategy calculations,
- 15m signal timeframe logic,
- 1h completed-bar bias alignment,
- setup/consolidation rules,
- breakout trigger rules,
- initial structural stop calculation,
- no-trade filters,
- next-bar-open baseline fill model,
- fees/slippage/funding hooks,
- validation reports,
- strategy conformance tests.

### Claude Code must not

- add hidden discretionary filters,
- use partial candles for strategy decisions,
- use current forming 1h candles for 1h bias,
- optimize parameters without recording variants,
- use unrealistic fill-at-signal-close as baseline,
- or promote backtest results as live readiness.

### Runnable checkpoint

Backtest/strategy conformance suite runs on fixtures or sample data and proves:

- completed-bar-only signal evaluation,
- point-in-time-valid 1h alignment,
- setup-window logic,
- breakout trigger logic,
- stop calculation,
- next-bar-open fill assumption,
- and no look-ahead behavior.

### Acceptance criteria

- Strategy implementation matches spec.
- Tests cover long, short, and neutral/no-trade cases.
- Tests cover missing/incomplete higher-timeframe context.
- Validation checklist mapping exists.
- Results are reproducible.
- Strategy remains rules-based.

---

## Phase 4 — Risk, State, and Persistence Runtime

### Purpose

Implement the runtime safety core before real execution.

### Build only what is needed for

- risk sizing,
- stop validation,
- exposure gates,
- notional caps,
- leverage caps,
- runtime modes,
- trade lifecycle states,
- protection states,
- reconciliation states,
- kill-switch state,
- persistent runtime control records,
- active trade/protection continuity records,
- incidents and operator actions,
- SQLite runtime database with migrations if selected,
- local startup into SAFE_MODE.

### Claude Code must not

- place real orders,
- implement live exchange writes,
- skip persistence for safety-critical transitions,
- treat local DB as exchange truth,
- auto-clear kill switch,
- or allow normal operation with unknown state.

### Runnable checkpoint

A local fake/no-exchange runtime should demonstrate:

- startup enters SAFE_MODE,
- runtime control state persists,
- kill switch persists across restart,
- entries are blocked under unsafe flags,
- active trade/protection records can be stored,
- unknown execution outcome state blocks entries,
- database migrations/tests pass.

### Acceptance criteria

- Runtime state model is implemented or scaffolded.
- Persistence follows durability expectations.
- State transitions are explicit and testable.
- Commands are not treated as facts.
- No exchange-write behavior exists.
- Restart-safety behavior is tested.

---

## Phase 5 — Dashboard, Observability, and Alerts

### Purpose

Build operator visibility before live-like execution.

### Build only what is needed for

- local dashboard/status surface,
- runtime mode display,
- entries allowed/blocked display,
- position/protection/order summary models,
- stream health placeholders,
- reconciliation state display,
- incident display,
- recent event display,
- host health placeholders,
- alert-route configuration,
- Telegram/n8n alert test hooks,
- structured logs/events.

### Claude Code may install

- dashboard/frontend dependencies,
- backend API dependencies,
- alert integration dependencies,
- only if phase-relevant and recorded.

### Claude Code must not

- add manual discretionary trading controls,
- add arbitrary buy/sell buttons,
- expose secrets in UI/logs,
- make Telegram/n8n approve high-risk actions,
- or bypass backend safety gates.

### Runnable checkpoint

A local dashboard/status command should start and display fake or local runtime state.

Alert route test should be possible with non-production/test credentials or documented placeholders.

### Acceptance criteria

- Dashboard can show safety state.
- Dashboard can show risk/protection/incident summaries.
- Dashboard is not a manual trading terminal.
- Alerts can be tested safely or are explicitly deferred.
- Logs are structured and redacted.
- Operator can capture screenshots without exposing secrets.

---

## Phase 6 — Dry-Run Exchange Simulation

### Purpose

Exercise live-like runtime behavior without real exchange order placement.

### Build only what is needed for

- fake exchange adapter,
- fake user-stream events,
- fake market data/completed bars,
- fake order lifecycle,
- fake fill lifecycle,
- fake protective stop lifecycle,
- fake stop cancel-and-replace,
- reconciliation simulation,
- failure injection,
- unknown outcome handling,
- emergency unprotected-position simulation,
- dry-run dashboard integration.

### Claude Code must not

- enable production exchange-write capability,
- require production credentials,
- use fake success as proof of live readiness,
- skip unknown-outcome branches,
- or allow dry-run to bypass safety state.

### Runnable checkpoint

A dry-run scenario should demonstrate:

```text
completed bar
→ strategy signal
→ risk approval
→ fake entry submission
→ fake fill confirmation
→ fake position confirmation
→ fake protective stop submission
→ fake stop confirmation
→ protected position state
→ fake exit/stop event
→ clean flat or recovery state
```

Failure scenarios should demonstrate blocked entries and reconciliation requirement.

### Acceptance criteria

- Happy path works in fake runtime.
- Unknown submission outcome blocks entries.
- Missing protection creates emergency branch.
- User-stream stale simulation blocks entries.
- Restart begins in SAFE_MODE.
- Reconciliation simulation can classify clean/recoverable/unsafe states.
- Dashboard reflects dry-run state.

---

## Phase 7 — Paper / Shadow Operation

### Purpose

Prepare and run live-like observation without real capital exposure.

Paper/shadow should validate:

- live market-data behavior,
- completed-bar publication,
- dashboard visibility,
- alert routing,
- runtime persistence,
- restart behavior,
- reconciliation behavior,
- operator workflow,
- and reporting discipline.

### Claude Code must not

- request production trade-capable keys unless phase-gate and operator explicitly approve a narrowly scoped reason,
- place real production orders,
- treat paper/shadow as tiny-live approval,
- or skip operator review.

### Runnable checkpoint

Paper/shadow runtime should run for an approved observation window and produce:

- completed-bar event logs,
- strategy signal/no-trade logs,
- simulated/paper trade lifecycle,
- dashboard state,
- alert tests,
- restart/recovery test evidence,
- phase report.

### Acceptance criteria

- Live-like data feed is reliable enough for observation.
- Completed-bar-only behavior is verified.
- Paper/shadow trade lifecycle works without capital exposure.
- Dashboard and alerts are usable.
- Restart/reconciliation behavior is tested.
- No real exposure exists.
- Operator review is recorded.

---

## Phase 8 — Tiny Live Preparation

### Purpose

Prepare for first real-capital tiny-live operation after evidence and approval.

This phase prepares but does not automatically begin tiny live.

### Build or verify

- dedicated NUC readiness,
- host hardening,
- runtime service management,
- local dashboard on attached monitor,
- alert route reliability,
- runtime DB/log/audit paths,
- backup and restore,
- secrets storage,
- IP restriction readiness,
- Binance account mode checks,
- one-way mode verification,
- isolated margin verification,
- internal notional cap,
- tiny-live config,
- emergency access,
- rollback path,
- operator checklist.

### Production Binance keys

Production trade-capable Binance API keys may only be created when the correct phase gate explicitly allows it and the operator approves.

Even then:

- permissions must be scoped,
- IP restrictions should be used where practical,
- secrets must not enter git/docs/prompts/logs,
- exchange-write capability must require explicit environment/config permission,
- and first runtime start still begins in SAFE_MODE.

### Runnable checkpoint

Before tiny live, the system should demonstrate on the NUC:

- repo cloned from GitHub,
- dependencies installed from lockfiles,
- tests pass,
- runtime DB initialized,
- dashboard visible on monitor,
- alerts tested,
- restart enters SAFE_MODE,
- reconciliation behavior verified in allowed mode,
- kill switch tested,
- backup/restore tested,
- exchange-write remains disabled until final approval.

### Acceptance criteria

- Phase-gate evidence exists.
- Host readiness evidence exists.
- Security readiness evidence exists.
- Operator readiness evidence exists.
- Internal notional cap exists.
- Risk is 0.25%.
- Effective leverage cap is 2x.
- Exchange-write capability is explicitly gated.
- Tiny live has not started without final approval.

---

## Phase 9 — Scaled Live Preparation

### Purpose

Prepare future scaled live only after tiny-live evidence.

This is not part of initial implementation.

### Requirements

Before scaled live, the project must have:

- stable tiny-live evidence,
- no unresolved severe incidents,
- reviewed slippage/fee behavior,
- reviewed drawdown behavior,
- reviewed stop/protection reliability,
- reviewed reconciliation performance,
- reviewed alerting reliability,
- reviewed host reliability,
- explicit risk increase approval,
- explicit leverage increase approval if applicable,
- updated documentation,
- and operator sign-off.

### Claude Code must not

- auto-promote to scaled live,
- increase risk automatically,
- increase leverage automatically,
- add symbols automatically,
- or remove supervision requirements.

---

## Cross-Phase Acceptance Rules

A phase is not complete unless:

- the runnable checkpoint works,
- commands and outputs are recorded,
- tests/checks are reported,
- changed files are listed,
- safety constraints are reviewed,
- unresolved gaps are documented,
- technical debt is updated if needed,
- and the operator approves moving forward.

A phase must fail or pause if:

- safety constraints are violated,
- production credentials are requested too early,
- exchange-write capability appears too early,
- tests cannot run and no justified deferral exists,
- unknown state is treated as safe,
- strategy uses partial bars,
- runtime does not start in SAFE_MODE where required,
- secrets appear in repo/logs/prompts/screenshots,
- or Claude Code cannot explain what changed.

---

## Required Evidence After Each Phase

At minimum, each phase should produce:

- checkpoint report,
- command list,
- test output,
- changed-file list,
- known gaps,
- unresolved questions,
- install actions performed,
- safety constraints checked,
- and next-step recommendation.

Where applicable, also save:

- generated reports,
- database migration output,
- dry-run logs,
- dashboard screenshots without secrets,
- alert test confirmation,
- backup/restore proof,
- reconciliation proof,
- incident simulation output,
- phase-gate approval notes.

---

## Local Development First, NUC Later

Initial implementation can and should happen on the operator's laptop/desktop.

The expected path is:

```text
Laptop/desktop development
→ local tests
→ data/backtest work
→ fake adapter dry-run
→ dashboard prototype
→ GitHub commits
→ NUC preparation
→ clone repo on NUC
→ install from lockfiles
→ run tests on NUC
→ run dry-run on NUC
→ dashboard on NUC monitor
→ paper/shadow
→ tiny live only after approval
```

Do not start with tiny-live NUC deployment before the codebase, tests, dry-run, dashboard, alerting, and setup process are ready.

The NUC should be prepared when the project approaches paper/shadow and tiny-live readiness.

---

## Migration-to-NUC Expectations

When moving from laptop/desktop implementation to the NUC:

1. Commit and push code through GitHub.
2. Prepare the NUC OS/security baseline.
3. Clone the repository onto the NUC.
4. Install dependencies from repo-defined lockfiles.
5. Create NUC-specific local config outside git.
6. Create NUC-specific secrets outside git.
7. Initialize runtime DB/log/audit/backup folders.
8. Run tests on the NUC.
9. Run dry-run on the NUC.
10. Verify dashboard on attached monitor.
11. Verify alert routes.
12. Verify restart into SAFE_MODE.
13. Verify kill switch persistence.
14. Verify backup/restore.
15. Keep exchange-write disabled until final tiny-live approval.

Do not migrate by copying an untracked random working folder as the primary deployment method.

Use the repository, lockfiles, config templates, and documented setup steps.

---

## Configuration and Secrets Rules

Claude Code may create templates such as:

```text
.env.example
config/example.local.yaml
config/example.dry-run.yaml
config/example.paper.yaml
config/example.tiny-live.yaml
```

Templates must not contain real secrets.

Local secret/config files must be ignored by git.

Claude Code must ensure `.gitignore` covers likely local secret files and runtime artifacts.

Production secrets must not be created, requested, stored, or used before the correct phase gate.

---

## Required Initial Claude Code Prompt

The operator should start Claude Code with this prompt after this file is committed to the repository:

```text
We are starting implementation of the Prometheus trading-bot repository.

Repository path on this machine:
C:\Prometheus

Before writing broad code, read:

1. docs/00-meta/current-project-state.md
2. docs/00-meta/ai-coding-handoff.md
3. docs/12-roadmap/phase-gates.md
4. docs/12-roadmap/technical-debt-register.md
5. docs/09-operations/first-run-setup-checklist.md
6. docs/README.md

Then follow the required reading order in ai-coding-handoff.md.

Important constraints:
- Prometheus v1 is rules-based, safety-first, and operator-supervised.
- Do not implement this as a self-learning live AI.
- Do not implement the whole project in one shot.
- Do not request or create production Binance trade-capable API keys.
- Do not enable production exchange-write capability.
- Build in phases.
- Each phase must end with a runnable checkpoint and a checkpoint report.
- Execution layer comes late.
- Dry-run and paper/shadow come before tiny live.
- Unknown execution outcomes fail closed.
- Restart begins in SAFE_MODE.
- Exchange state is authoritative.
- Strategy uses completed bars only.

Your first task is Phase 0 only:
perform a repository audit.

Report:
- current branch,
- working tree status,
- existing source layout,
- existing docs status,
- existing package/tooling state,
- existing tests,
- missing or stale files,
- immediate blockers,
- proposed Phase 1 plan.

Do not make broad code changes during Phase 0.
Do not proceed to Phase 1 until I approve.
If you find an installation or setup issue you cannot safely resolve, produce the ChatGPT Setup Escalation Prompt from the handoff.
```

---

## Standard Prompt Back to Claude Code After ChatGPT Setup Help

When the operator returns from ChatGPT after resolving an installation/setup issue, use:

```text
The setup issue was reviewed with ChatGPT.

Resolution summary:
[operator fills in what was done]

Current status:
[operator fills in verification result]

Continue from the previous checkpoint.
Do not skip the phase acceptance criteria.
Run the relevant command/check again and report the output.
If a new issue appears, stop and provide the full command output.
```

---

## Standard Prompt to Ask Claude Code for a Checkpoint Report

Use this when the operator wants a reviewable checkpoint:

```text
Stop at the current phase boundary and produce the Phase Checkpoint Report using the exact format from docs/00-meta/ai-coding-handoff.md.

Include:
- files changed,
- commands run,
- installations performed,
- tests/checks passed,
- tests/checks failed,
- runtime output,
- known gaps,
- spec ambiguities,
- safety constraints verified,
- and recommended next step.

Do not proceed to the next phase until I approve.
```

---

## Related Documents

This handoff should be read together with:

```text
docs/00-meta/current-project-state.md
docs/09-operations/first-run-setup-checklist.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
docs/08-architecture/implementation-blueprint.md
docs/08-architecture/state-model.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/database-design.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/event-flows.md
docs/08-architecture/deployment-model.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md
docs/06-execution-exchange/failure-recovery.md
docs/06-execution-exchange/position-state-model.md
docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/kill-switches.md
docs/10-security/host-hardening.md
docs/11-interface/operator-dashboard-requirements.md
```

---

## Final Rule

When in doubt:

```text
stop
preserve safety
record the ambiguity
recommend options
ask for review
```

Prometheus should move slowly where mistakes could create real exposure, unprotected positions, credential risk, or false confidence.

Fast coding is acceptable only when the phase is local, testable, reversible, and safely isolated from real exchange-write capability.
