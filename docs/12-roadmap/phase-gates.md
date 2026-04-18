# Phase Gates

## Purpose

This document defines the phase-gate governance model for the v1 Prometheus trading system.

Its purpose is to define when the project may move from one stage to the next:

```text
research
→ validation
→ dry-run implementation
→ paper/shadow
→ tiny live
→ scaled live
```

Prometheus is a safety-first, operator-supervised trading system. Phase gates exist because the system should not move closer to real capital exposure merely because code exists, tests pass, or a short run looks profitable.

Each phase must produce evidence.

Each promotion must be deliberate.

Each live risk increase must be reviewed.

The core rule is:

```text
No phase promotion, live enablement, risk increase, leverage increase, or scaled deployment
is allowed without documented evidence, clean safety state, and explicit operator approval.
```

## Scope

This document applies to v1 Prometheus under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- first secondary research comparison: ETHUSDT perpetual,
- strategy family: breakout continuation with higher-timeframe trend filter,
- signal timeframe: 15m,
- higher-timeframe bias: 1h,
- completed-bar confirmation,
- market entry after confirmed signal close,
- one-way position mode,
- isolated margin mode,
- one live symbol first,
- one position maximum,
- one active protective stop maximum,
- no pyramiding in v1,
- no reversal entry while positioned in v1,
- initial live risk: 0.25% of sizing equity,
- initial effective leverage cap: 2x,
- default tiny-live host: dedicated local NUC / mini PC with attached dashboard monitor,
- v1 is supervised, not lights-out autonomous.

This document covers:

- phase definitions,
- entry criteria,
- exit criteria,
- promotion evidence,
- demotion triggers,
- Claude Code readiness,
- first-run setup readiness,
- production key readiness,
- paper/shadow readiness,
- tiny-live readiness,
- scaled-live readiness,
- risk increase governance,
- leverage increase governance,
- technical-debt gating,
- and final acceptance criteria.

This document does **not** define:

- exact setup commands,
- exact implementation tasks,
- exact backtest code,
- exact dashboard design,
- exact Binance API key creation steps,
- exact operator checklist steps,
- or exact release commands.

Those belong in implementation documents and the future first-run setup checklist.

---

## Relationship to Other Documents

This document should be read together with:

- `docs/00-meta/current-project-state.md`
- `docs/00-meta/ai-coding-handoff.md`
- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`
- `docs/04-data/data-requirements.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
- `docs/06-execution-exchange/failure-recovery.md`
- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/exposure-limits.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/daily-loss-rules.md`
- `docs/07-risk/drawdown-controls.md`
- `docs/07-risk/kill-switches.md`
- `docs/08-architecture/deployment-model.md`
- `docs/08-architecture/database-design.md`
- `docs/08-architecture/event-flows.md`
- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/rollback-procedure.md`
- `docs/10-security/host-hardening.md`
- `docs/10-security/disaster-recovery.md`
- `docs/11-interface/manual-control-actions.md`
- `docs/11-interface/approval-workflows.md`
- `docs/11-interface/dashboard-metrics.md`
- `docs/11-interface/alerting-ui.md`
- `docs/12-roadmap/technical-debt-register.md`

### Authority hierarchy

If this document conflicts with a specialist document on a technical rule, the specialist document wins.

If this document conflicts with approval-workflows on how approval is recorded, approval-workflows wins.

If this document conflicts with risk documents on risk thresholds, the risk documents win.

If this document conflicts with incident response on emergency behavior, incident response wins.

If this document conflicts with current-project-state on project status, current-project-state should be updated to resolve the mismatch.

---

## Core Principles

## 1. Promotion requires evidence, not optimism

A phase may not be promoted because the project “feels ready.”

Promotion requires evidence from tests, validation, runs, reviews, and operator readiness checks.

## 2. Real-capital stages require operational proof

A good backtest does not prove live readiness.

Before live exposure, Prometheus must prove:

- data handling,
- strategy conformity,
- runtime state handling,
- persistence,
- dashboard visibility,
- alerting,
- restart behavior,
- reconciliation,
- failure recovery,
- emergency controls,
- and operator readiness.

## 3. Execution comes late

The execution layer is the only layer that can lose money.

Implementation should build toward execution gradually:

```text
data → storage → features → backtest → strategy → risk → runtime state
→ observability/dashboard → dry-run execution → paper/shadow → tiny live
```

Real exchange write capability must be introduced late and only after gates pass.

## 4. A runnable checkpoint ends every implementation phase

Each coding phase should end with something runnable and verifiable.

Examples:

- data layer ingests a known sample,
- backtest reproduces expected signals,
- fake exchange adapter simulates entry/stop lifecycle,
- dashboard displays runtime state,
- restart/reconciliation test passes,
- dry-run emergency flatten simulation works.

## 5. Ambiguity must be logged

If implementation finds gaps or contradictions in the specification, Claude Code or the implementer must record them in an ambiguity/spec-gap log.

The correct response is not to guess silently.

## 6. Phase gates can demote as well as promote

If evidence degrades or incidents occur, the system should move backward.

Examples:

- tiny live may demote to paper/shadow,
- scaled live may demote to tiny live,
- live operation may be paused or blocked pending review.

## 7. Risk increases are separate approvals

Moving from tiny live to scaled live does not automatically approve higher risk, higher notional, or higher leverage.

Risk, notional, and leverage increases each require their own evidence and approval.

## 8. Production keys are created only at the correct phase

Production trade-capable keys should not be created during early design or coding.

Key creation belongs near the approved paper/shadow-to-tiny-live transition, after host/security/secrets/IP-readiness checks pass.

---

## Phase Overview

Recommended phase sequence:

```text
PHASE 0 — Documentation and implementation planning
PHASE 1 — Local development foundation
PHASE 2 — Historical data and validation foundation
PHASE 3 — Backtesting and strategy conformance
PHASE 4 — Risk, state, and persistence runtime
PHASE 5 — Dashboard, observability, and alerts
PHASE 6 — Dry-run exchange simulation
PHASE 7 — Paper/shadow operation
PHASE 8 — Tiny live
PHASE 9 — Scaled live
```

The phases are sequential by default.

Some coding work may happen in parallel, but promotion gates must remain sequential.

---

## Phase 0 — Documentation and Implementation Planning

## Purpose

Finish the documentation required before Claude Code begins implementation.

## Entry criteria

- Repository exists.
- Core strategy/risk/execution/data decisions are documented.
- Working method is agreed.
- Project remains rules-based and supervised for v1.

## Exit criteria

Before leaving Phase 0:

- remaining high-value TBD docs are completed, bridged, deferred, or removed,
- first-run setup checklist exists,
- AI coding handoff exists,
- current-project-state is updated,
- technical-debt register exists,
- phase gates exist,
- repository docs are synchronized,
- project files/context cache plan is defined.

## Required evidence

- final `docs/00-meta/current-project-state.md`,
- final `docs/00-meta/ai-coding-handoff.md`,
- `docs/09-operations/first-run-setup-checklist.md`,
- `docs/12-roadmap/phase-gates.md`,
- `docs/12-roadmap/technical-debt-register.md`.

## Blockers

Phase 0 is blocked if:

- AI coding handoff is missing,
- first-run setup checklist is missing,
- unresolved pre-Claude blockers exist in technical-debt register,
- repository docs are stale versus intended source of truth,
- any high-safety placeholder remains unexplained.

---

## Phase 1 — Local Development Foundation

## Purpose

Create the codebase foundation without live exchange write capability.

## Entry criteria

- Phase 0 complete.
- Claude Code handoff approved.
- Repository is available.
- No production keys are required.
- Local development environment can be prepared.

## Required build outputs

- Python project structure,
- dependency manager setup,
- test runner,
- lint/type-check tooling,
- configuration loader,
- logging foundation,
- basic CLI or runtime entrypoint,
- fake/simulated config,
- local development docs,
- initial CI or local quality command where practical.

## Required tests

- unit test command runs,
- lint/type-check command runs,
- config loading tests,
- no production secret required,
- fake environment boots without exchange write capability.

## Exit criteria

- local codebase can be installed and tested,
- configuration separation exists,
- secrets are not required for local tests,
- code structure matches architecture direction,
- no live exchange order path is enabled.

---

## Phase 2 — Historical Data and Validation Foundation

## Purpose

Build the historical data ingestion, storage, versioning, and validation foundation.

## Entry criteria

- Phase 1 complete.
- Historical data requirements understood.
- Data folders/config paths defined.

## Required build outputs

- historical data ingestion/downloader or loader,
- Parquet storage conventions,
- DuckDB query setup,
- dataset manifest generation,
- normalized kline dataset,
- derived 1h bar generation,
- data integrity checks,
- dataset version linkage.

## Required tests/evidence

- BTCUSDT 15m data sample loads,
- ETHUSDT comparison data sample loads,
- duplicate/missing bar checks work,
- UTC Unix millisecond timestamp checks pass,
- 15m/1h alignment tests pass,
- dataset manifest created,
- validation cannot proceed without dataset version reference.

## Exit criteria

- data layer can produce versioned, validated research datasets,
- known sample periods can be queried reproducibly,
- no look-ahead timestamp issues detected,
- data layer acceptance criteria pass.

---

## Phase 3 — Backtesting and Strategy Conformance

## Purpose

Implement v1 strategy logic and backtesting enough to prove rule conformance.

## Entry criteria

- Phase 2 complete.
- Versioned datasets available.
- Strategy specification is stable.

## Required build outputs

- v1 breakout setup detection,
- completed-bar-only signal generation,
- 1h bias alignment,
- initial stop calculation,
- no-trade filters,
- baseline next-bar-open fill model,
- fee/slippage/funding modeling hooks,
- trade record output,
- validation report generation.

## Required tests/evidence

- hand-checkable examples pass,
- completed-bar-only behavior verified,
- forming candles not used,
- 1h bias uses latest completed bar only,
- stop formula matches spec,
- no look-ahead tests pass,
- BTCUSDT validation report produced,
- ETHUSDT comparison report produced.

## Exit criteria

- strategy logic can be trusted enough for paper/dry-run simulation,
- validation checklist data/strategy gates pass,
- known limitations are recorded.

---

## Phase 4 — Risk, State, and Persistence Runtime

## Purpose

Implement the live-runtime safety foundation before live execution.

## Entry criteria

- Phase 3 complete.
- Risk docs stable.
- Runtime architecture docs stable.

## Required build outputs

- risk sizing engine,
- exposure gate engine,
- stop validation,
- daily loss state,
- drawdown state,
- runtime state model,
- internal event/message contracts,
- runtime database schema,
- migrations,
- audit/runtime event storage,
- restart-critical persistence,
- safe-mode startup.

## Required tests/evidence

- risk sizing tests pass,
- below-minimum quantity rejects,
- leverage/notional cap tests pass,
- missing metadata fails closed,
- one-position/no-pyramiding/no-reversal gates pass,
- kill switch persists across restart,
- runtime starts in safe mode,
- runtime DB backup/restore smoke test passes,
- state transition and event log transaction tests pass.

## Exit criteria

- runtime can represent safe/blocked/recovery states,
- persistence supports restart safety,
- risk gates fail closed,
- no exchange write capability required.

---

## Phase 5 — Dashboard, Observability, and Alerts

## Purpose

Build operator visibility and control surface before any live-capable execution.

## Entry criteria

- Phase 4 complete.
- Dashboard requirements stable.
- Dedicated NUC display model documented.

## Required build outputs

- dashboard backend/read model,
- always-on local dashboard view,
- top-level runtime status,
- position/protection panels,
- open orders/protective stops panels,
- alerts panel,
- incident/reconciliation panels,
- risk/daily/drawdown panels,
- host/NUC health panel,
- audit/operator action panel,
- Telegram route if selected,
- n8n route if selected,
- alert history,
- manual controls disabled-state logic.

## Required tests/evidence

- dashboard displays fake clean-flat state,
- dashboard displays fake protected position,
- dashboard displays fake unprotected emergency,
- stale state is visibly labeled,
- alert acknowledgement does not resolve condition,
- Telegram/n8n messages are redacted,
- no arbitrary manual trading controls exist,
- chart/trade visualization is read-only if implemented.

## Exit criteria

- operator can supervise state from dashboard,
- critical alerts are visible,
- alert routes tested where configured,
- dashboard does not weaken safety model.

---

## Phase 6 — Dry-Run Exchange Simulation

## Purpose

Run Prometheus as a full live-like system without real order-writing.

## Entry criteria

- Phase 5 complete.
- Fake exchange adapter available.
- Runtime DB and dashboard working.
- Alerts working.
- No production trade keys required.

## Required build outputs

- fake exchange adapter,
- simulated order lifecycle,
- simulated user-stream events,
- simulated fills,
- simulated protective stop lifecycle,
- simulated stop replacement,
- simulated unknown outcomes,
- simulated stream gaps,
- dry-run emergency flatten flow,
- dry-run reconciliation.

## Required tests/evidence

- signal-to-protected-position dry-run flow passes,
- entry unknown outcome blocks entries,
- stop submission failure triggers emergency path,
- stop replacement ambiguity reconciles,
- restart/reconciliation dry-run passes,
- dashboard displays all states,
- alerts fire for critical simulated failures,
- audit records are produced.

## Exit criteria

- full event flows run end-to-end in fake/simulated mode,
- no real exchange order write capability is present,
- dry-run runbook is repeatable.

---

## Phase 7 — Paper / Shadow Operation

## Purpose

Observe Prometheus under live market conditions without real capital exposure.

## Entry criteria

- Phase 6 complete.
- Paper/shadow configuration approved.
- NUC/dashboard setup ready.
- Alerts tested.
- No production trade-capable keys required unless separately approved for read-only behavior.

## Required evidence

- sustained paper/shadow run,
- completed-bar timing correct,
- strategy signals occur only on completed bars,
- risk decisions logged,
- fake/paper orders tracked,
- protective stop simulation works,
- dashboard remains available,
- alerts work,
- restart test performed,
- reconciliation simulation performed,
- daily/weekly review notes produced.

## Exit criteria

- paper/shadow behavior matches expectations,
- no unresolved state-machine issues,
- no unresolved dashboard/alert blockers,
- no unresolved serious incidents,
- operator is comfortable supervising the system,
- tiny-live checklist can be prepared.

---

## Phase 8 — Tiny Live

## Purpose

First real-capital operation with deliberately conservative risk.

## Entry criteria

Before tiny live:

- Phase 7 complete,
- phase-gate approval recorded,
- dedicated NUC host-hardening complete,
- dashboard visible on monitor,
- alert routing tested,
- backup/restore tested,
- production key readiness approved,
- API permissions scoped,
- IP restriction configured or exception approved,
- secrets stored safely,
- rollback procedure understood,
- disaster-recovery checklist reviewed,
- emergency access tested,
- kill switch tested,
- emergency flatten tested in dry-run,
- risk set to 0.25% of sizing equity,
- effective leverage cap set to 2x,
- internal notional cap explicitly configured.

## Tiny-live operating constraints

- BTCUSDT only,
- one position maximum,
- no pyramiding,
- no reversal entry while positioned,
- supervised operation,
- no lights-out operation,
- no risk increases,
- no leverage increases,
- no scaled notional,
- no new strategy variants.

## Required evidence during tiny live

- every trade has confirmed stop protection,
- user-stream/reconciliation behavior clean,
- stop placement/replacement reliable,
- restart behavior tested while flat and/or safely controlled,
- dashboard/alerts reliable,
- incidents reviewed,
- daily/weekly review completed,
- slippage/fees reviewed,
- drawdown behavior reviewed,
- operator notes maintained.

## Exit criteria

Tiny live may continue or later promote only if:

- no unresolved severe incidents,
- no unresolved protection failures,
- no repeated unknown execution outcomes,
- no unresolved credential/security issues,
- daily/drawdown behavior acceptable,
- operator supervision is stable,
- evidence supports next stage.

---

## Phase 9 — Scaled Live

## Purpose

Operate with larger approved risk/notional/leverage only after evidence.

## Entry criteria

- tiny-live review passed,
- stage promotion approved,
- risk increase approved separately if applicable,
- notional increase approved separately if applicable,
- leverage increase approved separately if applicable,
- no unresolved high-severity incidents,
- no unresolved technical debt blocking scaled live,
- backup/restore and alert reliability reviewed,
- dashboard and operator workflow stable.

## Scaled-live constraints

Scaled live remains supervised unless future documents explicitly change that.

Scaling must be gradual.

Risk should progress only through approved steps such as:

```text
0.25% → 0.50% → 0.75% → 1.00%
```

Leverage cap should not jump directly to high values.

Recommended leverage evaluation progression, if ever justified:

```text
2x → 3x → 5x → 10x
```

## Exit criteria

Scaled live remains allowed only while:

- operational safety remains stable,
- strategy behavior remains within expected profile,
- risk/drawdown controls are respected,
- incidents are reviewed,
- operator continues active supervision,
- and no unresolved safety blockers exist.

---

## Claude Code Readiness Gate

Before asking Claude Code to implement the system:

## Required docs

The following must exist and be current:

- current project state,
- AI coding handoff,
- strategy spec,
- validation checklist,
- data requirements,
- execution docs,
- risk docs,
- architecture docs,
- operations docs,
- security docs,
- interface docs,
- phase gates,
- technical-debt register,
- first-run setup checklist.

## Required handoff content

The AI coding handoff must instruct Claude Code to:

- read the repo docs first,
- treat repo Markdown as authoritative,
- implement in phases,
- keep exchange-write capability disabled until approved,
- maintain an ambiguity/spec-gap log,
- stop when contradictions are found,
- write tests per phase,
- create runnable checkpoints,
- avoid one-shot full-system generation,
- not create production API keys,
- not enable real trading before phase gates,
- not bypass safety docs.

## Required implementation phase order

The handoff should prefer:

```text
1. project scaffold / tooling
2. data ingestion and validation
3. backtesting
4. strategy conformance
5. risk engine
6. runtime state/persistence
7. observability/dashboard read models
8. fake exchange adapter
9. dry-run event flows
10. paper/shadow environment
11. live execution integration only after approval
```

## Blockers

Claude Code readiness is blocked if:

- first-run setup checklist is missing,
- AI coding handoff is missing,
- technical-debt register contains pre-Claude blockers,
- docs contain unresolved contradictions,
- repo and current-project-state disagree materially,
- no phased acceptance criteria are defined.

---

## First-Run Setup Readiness Gate

Before actual setup begins:

- first-run setup checklist must exist,
- NUC assumptions must be documented,
- Python/dependency setup must be defined,
- local environment bootstrap must be defined,
- runtime DB initialization must be defined,
- research data folders must be defined,
- dashboard local display setup must be defined,
- Telegram/n8n setup path must be defined if used,
- Binance key creation timing must be clear,
- host hardening checklist must be clear,
- backup/restore setup must be clear,
- paper/shadow launch checklist must be clear,
- tiny-live launch checklist must be clear.

The first-run setup checklist should be practical and step-oriented.

The AI coding handoff should reference it, not duplicate it fully.

---

## Production API Key Readiness Gate

Production trade-capable keys must not be created until:

- tiny-live phase is near,
- host is prepared,
- secret storage path is prepared,
- API permissions policy is clear,
- IP restriction plan is clear,
- alert/dashboard readiness is tested,
- backup/restore readiness is tested,
- operator understands key revocation/rotation,
- production key readiness approval is recorded.

No production API keys should be created during documentation, early coding, or historical backtesting phases.

---

## Risk Increase Gate

Risk increase above 0.25% requires:

- tiny-live or paper/shadow evidence depending on stage,
- no unresolved severe incidents,
- no unresolved stop/protection failures,
- no repeated unknown execution outcomes,
- daily loss behavior acceptable,
- drawdown behavior acceptable,
- slippage/fee behavior reviewed,
- operator review completed,
- config version change,
- approval workflow completed,
- release note recorded.

Risk increase is blocked during:

- active drawdown caution/pause/hard review,
- active daily lockout,
- active kill switch,
- unresolved incident,
- unresolved credential issue,
- unresolved state mismatch.

---

## Leverage Increase Gate

Leverage cap increase above 2x requires:

- risk model review,
- liquidation-distance review,
- stop-distance behavior review,
- fee/slippage review,
- stable execution history,
- stable stop placement/replacement history,
- stable reconciliation history,
- no unresolved incidents,
- approval workflow,
- config/release update.

Leverage increase must never be approved merely because exchange maximum leverage is higher.

---

## Notional Cap Increase Gate

Notional cap increase requires:

- liquidity/slippage review,
- account allocation review,
- position sizing review,
- leverage/bracket review,
- risk cap consistency,
- tiny-live evidence if live,
- operator approval,
- config/release update.

The internal notional cap must remain explicit.

---

## Demotion and Pause Triggers

The system should demote, pause, or block advancement when:

- unprotected position occurs,
- repeated stop failures occur,
- unknown execution outcomes repeat,
- user stream reliability unacceptable,
- restart/reconciliation unreliable,
- dashboard unavailable in live stage,
- alert routing unreliable in live stage,
- daily loss/drawdown hard review triggered,
- credential/security concern appears,
- host/NUC reliability unacceptable,
- operator cannot supervise,
- technical-debt item becomes blocking,
- strategy validation assumptions no longer hold.

Demotion options include:

```text
scaled_live → tiny_live
tiny_live → paper_shadow
paper_shadow → dry_run
any live stage → safe_mode / blocked awaiting operator
```

---

## Evidence Artifacts

Phase-gate decisions should reference evidence artifacts.

Examples:

- dataset manifests,
- validation reports,
- backtest reports,
- paper/shadow logs,
- dry-run event-flow reports,
- dashboard screenshots without secrets,
- alert test records,
- restart/reconciliation logs,
- incident reports,
- daily/weekly review notes,
- release notes,
- config diffs,
- audit records,
- host-hardening checklist,
- backup/restore test record.

Evidence must be redacted where necessary.

---

## Phase-Gate Decision Record

Each promotion or major gate decision should record:

```text
gate_id
gate_type
from_phase
to_phase
decision
decided_by
decided_at_utc_ms
release_version
config_version
dataset_version_references
evidence_references
known_limitations
technical_debt_references
risk_changes
operator_notes
approval_reference
```

Implementation may store this as markdown initially, then later in runtime/audit records if needed.

---

## Setup and Runbook Topics Deferred to First-Run Checklist

The first-run setup checklist should translate phase gates into practical steps for:

- installing local tools,
- cloning repository,
- setting Python/dependency environment,
- running tests,
- initializing runtime DB,
- preparing historical data folders,
- configuring dry-run,
- setting up dashboard display on NUC,
- configuring Telegram/n8n routes,
- preparing host hardening,
- creating production keys only at approved phase,
- launching paper/shadow,
- launching tiny live,
- verifying emergency access.

---

## Forbidden Phase-Gate Patterns

The following are not allowed:

- coding the entire system in one monolithic Claude Code step,
- enabling live exchange writes before dry-run/paper evidence,
- creating production trade keys during early development,
- promoting because backtest alone looks profitable,
- increasing risk because recent live trades won,
- increasing leverage because Binance allows it,
- skipping dashboard/alert readiness before tiny live,
- skipping backup/restore testing before tiny live,
- skipping reconciliation testing,
- ignoring technical debt blockers,
- treating paper/shadow as equivalent to live proof,
- treating alert acknowledgement as incident resolution,
- treating operator excitement as approval evidence,
- moving to scaled live with unresolved safety incidents.

---

## Testing Requirements

## Phase-gate tests

The implementation should support tests or checklist validations for:

- data gate,
- backtest gate,
- strategy conformance gate,
- risk gate,
- runtime state gate,
- persistence/restart gate,
- reconciliation gate,
- dashboard/alert gate,
- dry-run exchange gate,
- paper/shadow gate,
- tiny-live readiness gate.

## Governance tests

Test that:

- risk increase is blocked without approval,
- leverage increase is blocked without approval,
- production trade mode cannot be enabled in local/dev config,
- live enablement requires proper stage/config,
- kill switch blocks promotion,
- unresolved incident blocks promotion,
- technical-debt blockers block handoff/promotions.

---

## Non-Goals

This document does not define:

- exact implementation commands,
- exact shell setup,
- exact backtest metrics thresholds,
- exact statistical acceptance thresholds beyond existing validation docs,
- exact front-end UI,
- exact CI/CD system,
- exact legal/compliance requirements,
- or exact production operations rota.

It defines governance gates.

---

## Acceptance Criteria

`phase-gates.md` is complete enough for v1 when it makes the following clear:

- implementation and deployment are staged,
- Claude Code implementation must be phased with runnable checkpoints,
- each phase has entry and exit criteria,
- paper/shadow and tiny live require operational evidence, not just code,
- first-run setup checklist is required before setup work,
- production keys are created only at the correct phase,
- tiny live requires NUC/host/dashboard/alerts/secrets/backups readiness,
- risk increases require separate approval,
- leverage increases require separate approval,
- scaled live requires tiny-live evidence and explicit approval,
- demotion/pause triggers are defined,
- ambiguity/spec-gap logging is required,
- and no phase gate may bypass exchange reconciliation, protective-stop requirements, incidents, kill switch, daily/drawdown controls, or security requirements.
