# Technical Debt Register

## Purpose

This document is the technical-debt and deferral register for the v1 Prometheus trading system.

Its purpose is to prevent known gaps, accepted limitations, deferred features, unresolved ambiguities, and future improvements from becoming hidden assumptions.

A trading system can fail not only because code is wrong, but because a known limitation was forgotten.

This register exists so that the project can clearly distinguish between:

```text
pre-Claude blockers
pre-paper blockers
pre-tiny-live blockers
pre-scaled-live blockers
post-MVP improvements
future research ideas
```

The register should be updated whenever a decision is deferred, a TODO is accepted, or implementation discovers a specification gap.

## Scope

This register applies to:

- documentation gaps,
- implementation gaps,
- testing gaps,
- operational readiness gaps,
- exchange/API uncertainty,
- security hardening gaps,
- dashboard/interface gaps,
- setup/runbook gaps,
- future feature ideas,
- and known limitations accepted for v1.

This document does **not** replace:

- issue tracker,
- release notes,
- incident reports,
- validation reports,
- phase gates,
- or the AI coding handoff.

It is a governance index for known debt and deferrals.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/12-roadmap/phase-gates.md`
- `docs/00-meta/current-project-state.md`
- `docs/00-meta/ai-coding-handoff.md`
- `docs/09-operations/release-process.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/rollback-procedure.md`
- `docs/10-security/audit-logging.md`
- `docs/10-security/disaster-recovery.md`
- `docs/08-architecture/deployment-model.md`
- `docs/08-architecture/database-design.md`
- all specialist docs that own the relevant domain.

### Authority hierarchy

If this register says an item is deferred but a specialist safety document says it is required before live operation, the specialist safety document wins.

If this register conflicts with phase gates on blocking status, phase gates win.

If implementation discovers a gap not listed here, this register should be updated rather than relying on memory.

---

## Core Principles

## 1. Known debt must be explicit

Do not leave important TODOs hidden in chat memory or code comments only.

## 2. Blocking status must be clear

Every register item should say whether it blocks:

- Claude Code handoff,
- coding start,
- dry-run,
- paper/shadow,
- tiny live,
- scaled live,
- or future improvement only.

## 3. Safety debt is different from convenience debt

A missing chart animation is not the same kind of debt as unknown stop-state recovery behavior.

Debt should be categorized by risk.

## 4. Accepted deferrals must have a phase

If something is deferred, the register should say until when.

## 5. The register is living

This document should be updated during implementation when:

- Claude Code finds ambiguity,
- Binance API behavior differs from spec,
- tests reveal missing edge cases,
- setup reveals host/network issues,
- dashboard/alerting gaps are found,
- paper/shadow exposes runtime mismatch.

---

## Classification Model

Each item should use this structure:

```text
ID:
Title:
Category:
Owner area:
Status:
Blocking phase:
Risk level:
Description:
Why deferred / why it exists:
Required resolution:
Evidence required to close:
Related docs:
```

## Category values

Recommended categories:

```text
DOCUMENTATION
IMPLEMENTATION
TESTING
DATA
STRATEGY
RISK
EXECUTION
EXCHANGE_API
ARCHITECTURE
DATABASE
DEPLOYMENT
OPERATIONS
SECURITY
INTERFACE
DASHBOARD
ALERTING
SETUP
ROADMAP
RESEARCH
```

## Status values

```text
OPEN
IN_PROGRESS
RESOLVED
DEFERRED
ACCEPTED_LIMITATION
SUPERSEDED
```

## Blocking phase values

```text
PRE_CLAUDE_HANDOFF
PRE_CODING_START
PRE_DRY_RUN
PRE_PAPER_SHADOW
PRE_TINY_LIVE
PRE_SCALED_LIVE
POST_MVP
FUTURE_RESEARCH
NON_BLOCKING
```

## Risk levels

```text
LOW
MEDIUM
HIGH
CRITICAL
```

---

## Current Register Summary

As of this document version, most high-value placeholder docs have been completed.

Remaining near-term items are:

1. first-run setup checklist,
2. AI coding handoff,
3. final current-project-state update,
4. repository documentation map/index review,
5. implementation ambiguity/spec-gap log creation during coding.

These are not optional before serious coding handoff/setup work.

---

## Open Items

## TD-001 — First-run setup checklist not yet created

**Category:** SETUP / OPERATIONS  
**Owner area:** Operations / setup  
**Status:** OPEN  
**Blocking phase:** PRE_CLAUDE_HANDOFF  
**Risk level:** HIGH

### Description

The project needs a practical setup/runbook document:

```text
docs/09-operations/first-run-setup-checklist.md
```

This document should guide the operator through:

- local development setup,
- Python/dependency setup,
- repository clone,
- test/lint/type-check execution,
- runtime DB initialization,
- historical data folders,
- DuckDB/Parquet setup,
- dry-run configuration,
- dashboard local monitor setup,
- Telegram/n8n alert setup,
- dedicated NUC preparation,
- host hardening checks,
- backup/restore verification,
- Binance account/key timing,
- paper/shadow launch,
- tiny-live launch,
- emergency access.

### Why it exists

Architecture/security/interface docs define requirements, but the operator needs a guided setup path.

### Required resolution

Create `docs/09-operations/first-run-setup-checklist.md`.

### Evidence required to close

- checklist file exists,
- it references deployment/host/security/data/dashboard/phase-gate docs,
- it clearly says not to create production keys before the approved phase,
- it includes paper/shadow and tiny-live readiness checklists.

### Related docs

- `docs/08-architecture/deployment-model.md`
- `docs/10-security/host-hardening.md`
- `docs/10-security/disaster-recovery.md`
- `docs/11-interface/dashboard-metrics.md`
- `docs/11-interface/alerting-ui.md`
- `docs/12-roadmap/phase-gates.md`

---

## TD-002 — AI coding handoff not yet created

**Category:** DOCUMENTATION / IMPLEMENTATION  
**Owner area:** Meta / coding handoff  
**Status:** OPEN  
**Blocking phase:** PRE_CODING_START  
**Risk level:** HIGH

### Description

The final Claude Code handoff has not yet been created:

```text
docs/00-meta/ai-coding-handoff.md
```

### Why it exists

The handoff should be created only after remaining docs are complete and setup requirements are captured.

### Required resolution

Create the AI coding handoff after:

- first-run setup checklist,
- final current-project-state update,
- phase gates,
- technical debt register,
- and any remaining repository doc index updates.

### Required handoff content

Must include:

- repository reading order,
- authoritative docs list,
- locked v1 decisions,
- phased implementation plan,
- runnable checkpoints,
- acceptance criteria per phase,
- ambiguity/spec-gap log requirement,
- hard safety constraints,
- no real trading before dry-run/paper gates,
- execution layer late in implementation,
- dry-run and paper/shadow first,
- human approval for live promotion.

### Related docs

- `docs/12-roadmap/phase-gates.md`
- `docs/00-meta/current-project-state.md`
- all implementation docs.

---

## TD-003 — Final current-project-state update required before branch/handoff

**Category:** DOCUMENTATION  
**Owner area:** Meta  
**Status:** OPEN  
**Blocking phase:** PRE_CLAUDE_HANDOFF  
**Risk level:** MEDIUM

### Description

`docs/00-meta/current-project-state.md` must be updated after roadmap docs are created and before branching to the final setup/handoff chat.

### Required resolution

Update current-project-state to show:

- completed docs,
- remaining setup/handoff tasks,
- correct 25-file project upload recommendation,
- dedicated NUC/dashboard/Telegram/n8n assumptions,
- next chat instructions.

### Evidence required to close

- updated file exists,
- no outdated remaining-TBD plan remains,
- branch prompt/list is available.

---

## TD-004 — Documentation map may need index update

**Category:** DOCUMENTATION  
**Owner area:** Docs map  
**Status:** OPEN  
**Blocking phase:** PRE_CODING_START  
**Risk level:** LOW

### Description

The repository documentation map may need an update to include newly created docs and the later first-run setup checklist.

### Required resolution

Review and update `docs/README.md` if needed.

### Evidence required to close

- docs map links or lists key directories/files correctly,
- no important completed doc remains hidden from the map.

---

## TD-005 — Claude Code ambiguity/spec-gap log must be created during implementation

**Category:** IMPLEMENTATION / DOCUMENTATION  
**Owner area:** Claude Code handoff / implementation process  
**Status:** RESOLVED  
**Blocking phase:** PRE_CODING_START  
**Risk level:** HIGH

### Description

During implementation, Claude Code must maintain an ambiguity/spec-gap log.

Proposed future file:

```text
docs/00-meta/implementation-ambiguity-log.md
```

or another location agreed in the AI coding handoff.

### Why it exists

A large specification set can still underdetermine details.

The model must not silently guess important behavior when specs conflict or are incomplete.

### Required resolution

AI coding handoff should instruct Claude Code to create/update this log whenever it finds:

- contradictory docs,
- Binance API uncertainty,
- missing rounding rule,
- unclear state transition,
- unclear config behavior,
- unclear test expectation,
- unclear dashboard/control behavior.

### Blocking status

Not a blocker to writing handoff, but the handoff must require it before implementation proceeds deeply.

### Resolution evidence

- `docs/00-meta/implementation-ambiguity-log.md` now exists and contains the required entry-format header plus the initial Phase 1 ambiguity/spec-gap entries:
  - `GAP-20260419-001` — filename mismatch `first_strategy-comparison.md` vs `first-strategy-comparison.md` (RESOLVED by `git mv`).
  - `GAP-20260419-002` — Phase 1 tooling decisions (uv, Python `>=3.11,<3.13`, `[dependency-groups]`, deferred pre-commit/CI, feature-branch workflow) (RESOLVED).
  - `GAP-20260419-003` — `.python-version` git-ignore conflict; narrow `.gitignore` edit authorized (RESOLVED).
- Ambiguity log committed in Phase 1 Commit 3 on branch `phase-1/local-dev-foundation`.
- Phase 1 checkpoint report at `docs/00-meta/implementation-reports/2026-04-19_phase-1-checkpoint-report.md` records the ambiguity-log discipline as the process to carry into Phase 2 and onward.

---

## TD-006 — Exact Binance endpoint behavior must be verified at coding time

**Category:** EXCHANGE_API  
**Owner area:** Exchange adapter  
**Status:** OPEN  
**Blocking phase:** PRE_DRY_RUN / PRE_PAPER_SHADOW  
**Risk level:** HIGH

### Description

Docs define conceptual Binance USDⓈ-M behavior, but implementation must verify exact current endpoint paths, parameters, enums, response fields, error codes, rate limits, and user-stream behavior against official Binance documentation at coding time.

### Why it exists

Exchange APIs can change or have edge behavior not captured in design docs.

### Required resolution

During exchange adapter implementation:

- verify official docs,
- write endpoint mapping tests/fakes,
- record any mismatch in ambiguity log,
- update docs if needed.

### Evidence required to close

- exchange adapter endpoint mapping exists,
- tests/fakes exist,
- no unreviewed doc/API mismatch remains before paper/shadow.

---

## TD-007 — Binance testnet vs pure dry-run decision remains implementation-time choice

**Category:** DEPLOYMENT / EXCHANGE_API  
**Owner area:** Dry-run / paper-shadow  
**Status:** DEFERRED  
**Blocking phase:** PRE_PAPER_SHADOW  
**Risk level:** MEDIUM

### Description

The project allows dry-run, fake adapter, paper/shadow, and possibly Binance testnet usage, but does not yet force a single exact staging method.

### Why deferred

The implementation should first build a fake adapter and dry-run harness. Testnet usefulness can be assessed later.

### Required resolution

Before paper/shadow:

- decide whether Binance testnet is useful,
- document testnet limitations,
- keep production trading disabled,
- ensure paper/shadow evidence is clear.

---

## TD-008 — TradingView-like chart implementation deferred

**Category:** DASHBOARD / INTERFACE  
**Owner area:** Dashboard  
**Status:** DEFERRED  
**Blocking phase:** POST_MVP or PRE_TINY_LIVE depending on operator preference  
**Risk level:** LOW/MEDIUM

### Description

The dashboard should eventually include TradingView-like candle/setup/trade visualization for rule verification.

### Why deferred

It is useful, but not required before foundational data, runtime, risk, execution simulation, and dashboard safety status are implemented.

### Required resolution

Implement read-only setup/trade charts when dashboard foundation is stable.

### Must preserve

- no chart trading,
- no click-to-buy/sell,
- no drag-to-widen-stop,
- no discretionary manual trading controls.

---

## TD-009 — Remote approvals through Telegram/n8n deferred

**Category:** ALERTING / APPROVALS / SECURITY  
**Owner area:** Alerting / interface  
**Status:** DEFERRED  
**Blocking phase:** POST_MVP  
**Risk level:** MEDIUM/HIGH

### Description

Telegram/n8n may notify the operator, but high-risk approvals should initially remain on the controlled dashboard.

### Why deferred

Remote approvals create authentication, replay, authorization, accidental-click, and audit risks.

### Required resolution

Future remote approvals require:

- authentication design,
- confirmation design,
- replay protection,
- audit logging,
- explicit approval from security/interface docs.

---

## TD-010 — Multi-symbol and portfolio support deferred

**Category:** STRATEGY / RISK / EXECUTION  
**Owner area:** Future roadmap  
**Status:** DEFERRED  
**Blocking phase:** POST_MVP  
**Risk level:** HIGH if attempted early

### Description

V1 live scope is BTCUSDT only.

ETHUSDT is research/comparison only.

### Why deferred

Multi-symbol support increases:

- exposure complexity,
- reconciliation complexity,
- dashboard complexity,
- risk allocation complexity,
- exchange-order state ambiguity.

### Required resolution

Future multi-symbol support requires new strategy/risk/execution/portfolio docs and phase gates.

---

## TD-011 — Hedge mode support deferred

**Category:** EXECUTION / RISK  
**Owner area:** Future exchange support  
**Status:** DEFERRED  
**Blocking phase:** POST_MVP  
**Risk level:** HIGH if attempted early

### Description

V1 assumes one-way mode.

Hedge mode is explicitly unsupported.

### Required resolution

If future hedge mode is considered, create separate design docs and tests for:

- positionSide behavior,
- long/short simultaneous positions,
- stop/protection mapping,
- exposure limits,
- UI display.

---

## TD-012 — Automated strategy learning / self-learning bot deferred

**Category:** STRATEGY / RESEARCH  
**Owner area:** Future research  
**Status:** DEFERRED  
**Blocking phase:** FUTURE_RESEARCH  
**Risk level:** HIGH if attempted early

### Description

The project goal may eventually include AI-assisted research or automation, but v1 is rules-based.

### Required resolution

Any self-learning/live-adaptive system requires separate research, validation, risk, and governance docs.

---

## TD-013 — Full remote production operations model deferred

**Category:** DEPLOYMENT / OPERATIONS  
**Owner area:** Deployment  
**Status:** DEFERRED  
**Blocking phase:** POST_MVP  
**Risk level:** MEDIUM

### Description

The default v1 live host is a dedicated local NUC with monitor.

A VPS/cloud deployment may be considered later.

### Required resolution

If VPS/cloud becomes desired, create an alternative deployment model covering:

- remote access,
- network security,
- monitoring,
- backup,
- secrets,
- dashboard access,
- disaster recovery.

---

## TD-014 — External immutable audit sink deferred

**Category:** SECURITY / AUDIT  
**Owner area:** Audit logging  
**Status:** DEFERRED  
**Blocking phase:** POST_MVP  
**Risk level:** MEDIUM

### Description

V1 can use local runtime DB audit tables, structured logs, and backups.

A future external immutable log sink may improve tamper resistance.

### Required resolution

Evaluate after tiny-live if audit/log needs justify it.

---

## TD-015 — Advanced operator authentication and role model deferred

**Category:** SECURITY / INTERFACE  
**Owner area:** Dashboard/security  
**Status:** DEFERRED  
**Blocking phase:** PRE_SCALED_LIVE or POST_MVP  
**Risk level:** MEDIUM

### Description

V1 likely has a single primary operator.

A multi-user role model is not required immediately, but the system should avoid designs that make it impossible later.

### Required resolution

Before multiple operators or remote approvals:

- define user roles,
- authentication,
- authorization,
- audit identity,
- session handling.

---

## TD-016 — Exact statistical live-performance thresholds require future evidence

**Category:** RESEARCH / RISK  
**Owner area:** Validation / phase gates  
**Status:** ACCEPTED_LIMITATION  
**Blocking phase:** PRE_RISK_INCREASE  
**Risk level:** MEDIUM

### Description

Docs define operational and validation gates, but exact statistical thresholds for long-term strategy quality will require evidence from backtests, paper/shadow, and tiny live.

### Required resolution

Before risk increase:

- compare live/paper performance to backtest expectations,
- review drawdown,
- review win/loss distribution,
- review slippage/fees,
- update phase gate criteria if needed.

---

## TD-017 — Exact public-IP solution for local NUC must be resolved before production keys

**Category:** SECURITY / DEPLOYMENT  
**Owner area:** Host/API key readiness  
**Status:** OPEN  
**Blocking phase:** PRE_TINY_LIVE  
**Risk level:** HIGH

### Description

The dedicated NUC may be behind a home/office ISP with changing public IP.

Production Binance API keys should use IP restriction where possible.

### Required resolution

Before production trade-capable keys:

- determine public IP stability,
- choose static IP/VPN/egress solution if needed,
- document exception if IP restriction cannot be used,
- approve exception if required.

---

## TD-018 — First live notional cap value must be finalized before tiny live

**Category:** RISK  
**Owner area:** Risk/config  
**Status:** OPEN  
**Blocking phase:** PRE_TINY_LIVE  
**Risk level:** HIGH

### Description

Risk docs require an explicit internal notional cap for live operation, but the final numeric tiny-live cap must be set in config.

### Required resolution

Before tiny live:

- choose tiny-live notional cap,
- record config version,
- verify with sizing equity,
- include in approval workflow.

---

## TD-019 — Exact production alert route selection must be finalized before tiny live

**Category:** ALERTING / SETUP  
**Owner area:** Alerting UI / setup  
**Status:** OPEN  
**Blocking phase:** PRE_TINY_LIVE  
**Risk level:** MEDIUM/HIGH

### Description

Docs allow Telegram and/or n8n alert routing.

The actual production route must be chosen and tested before tiny live.

### Required resolution

Before tiny live:

- decide Telegram only, n8n only, both, or other,
- configure secrets safely,
- test warning/critical alerts,
- verify route degradation appears on dashboard.

---

## TD-020 — Exact backup schedule and retention must be finalized before tiny live

**Category:** OPERATIONS / DISASTER_RECOVERY  
**Owner area:** Backup/restore  
**Status:** OPEN  
**Blocking phase:** PRE_TINY_LIVE  
**Risk level:** HIGH

### Description

Docs require runtime DB backup and restore testing, but final frequency and retention must be chosen.

### Required resolution

Before tiny live:

- define backup frequency,
- define retention,
- define location,
- test restore,
- document in setup checklist.

---

## Deferred Future Enhancements

The following are accepted future work and do not block v1:

- multi-symbol strategy support,
- ETHUSDT live promotion,
- portfolio-level risk allocation,
- advanced performance analytics,
- remote mobile dashboard,
- remote high-risk approvals,
- external immutable audit sink,
- advanced distributed deployment,
- automated model-based strategy selection,
- ML/self-learning live strategy adaptation,
- sophisticated order types beyond v1,
- in-place stop modification if later justified,
- multi-venue support,
- hedge-mode support.

Each future enhancement requires its own phase gate and design review before implementation.

---

## Pre-Claude Blocker Checklist

Before Claude Code implementation handoff, the following must be resolved:

- [ ] `docs/09-operations/first-run-setup-checklist.md` created.
- [ ] `docs/00-meta/ai-coding-handoff.md` created.
- [ ] `docs/00-meta/current-project-state.md` updated.
- [ ] unresolved documentation placeholders reviewed.
- [ ] repository docs synchronized.
- [ ] current 25-file project upload list updated.
- [ ] implementation ambiguity/spec-gap log requirement included in handoff.

---

## Pre-Tiny-Live Blocker Checklist

Before tiny live, at minimum:

- [ ] production NUC host baseline complete.
- [ ] dashboard visible on monitor.
- [ ] alert route selected and tested.
- [ ] backup/restore tested.
- [ ] production API key readiness approved.
- [ ] public IP/IP-restriction plan resolved.
- [ ] explicit notional cap configured.
- [ ] emergency controls tested in dry-run.
- [ ] paper/shadow evidence reviewed.
- [ ] no unresolved severe technical debt.
- [ ] no unresolved severe incident.
- [ ] operator approval recorded.

---

## Register Maintenance Rules

## When to add an item

Add an item when:

- a design decision is deferred,
- implementation finds ambiguity,
- test coverage is knowingly missing,
- a future feature is intentionally excluded,
- paper/shadow reveals a weakness,
- a live incident exposes missing design,
- setup discovers a practical gap.

## When to close an item

Close an item only when:

- the required document/code/test/setup exists,
- evidence is available,
- related docs are updated if needed,
- closure does not hide a safety limitation.

## When to escalate an item

Escalate if:

- a non-blocking item becomes safety-relevant,
- a future enhancement is about to be implemented,
- a deferred issue blocks phase promotion,
- a live incident connects to the item.

---

## Forbidden Patterns

The following are not allowed:

- leaving known safety gaps only in chat memory,
- treating TODOs as resolved because they are inconvenient,
- starting live setup while pre-tiny-live blockers remain open,
- asking Claude Code to guess around unresolved spec gaps,
- moving debt from blocker to non-blocker without reason,
- hiding exchange/API uncertainty,
- treating future enhancements as silently approved,
- forgetting deferred risk/leverage decisions,
- removing debt items without evidence.

---

## Acceptance Criteria

`technical-debt-register.md` is complete enough for v1 when it makes the following clear:

- known deferrals are explicit,
- blocking phase is recorded,
- safety debt is distinguished from convenience debt,
- first-run setup checklist is a pre-handoff blocker,
- AI coding handoff is a pre-coding blocker,
- implementation ambiguity/spec-gap logging is required,
- Binance API details must be verified at coding time,
- local NUC public-IP/IP restriction remains a pre-tiny-live item,
- notional cap, alert route, and backup schedule require finalization before tiny live,
- future enhancements are not silently approved,
- and the register should be maintained during implementation and operations.
