# Current Project State

## Purpose

This document defines the current high-level state of the Prometheus trading-system project.

Its purpose is to:

- provide a clear project checkpoint before Claude Code implementation begins,
- summarize what has already been designed,
- identify the current implementation-readiness status,
- define the boundary between documentation/setup/handoff and coding,
- preserve locked decisions across chats and repository updates,
- and act as the high-level project memory checkpoint.

This document should be treated as the single high-level source of truth for project status.

If this document conflicts with a detailed specialist document, the specialist document wins for its domain.

If older chat memory conflicts with repository Markdown files, the repository Markdown files win.

---

## Repository Context

Repository:

```text
https://github.com/jpedrocY/Prometheus
```

The repository Markdown files are the primary source of truth.

ChatGPT project-uploaded files are only a limited continuity cache because of the project-file limit.

Claude Code or any other implementation agent must inspect the repository directly and use uploaded files as a compact high-priority cache, not as the complete project source.

---

## Project Objective

Prometheus is a long-term project to design and build a:

```text
production-oriented, safety-first, operator-supervised trading system
for Binance USDⓈ-M futures
```

Initial live market:

```text
BTCUSDT perpetual
```

The system is:

- initially rules-based,
- not self-learning in v1,
- designed for robustness rather than novelty,
- built for staged and supervised deployment,
- designed to support future AI-assisted research or automation,
- but not dependent on a self-learning live AI component for v1.

Prometheus v1 is not intended to be a lights-out autonomous AI trading agent.

---

## Current Phase

Phase 0 (repo audit), Phase 1 (local development foundation), the Phase 2 historical-data foundation, and **three complete strategy-research arcs** are all complete:

1. The **V1 breakout-continuation arc** (Phases 2e through 2w) producing one locked baseline (H0), one cleanly-promoted structural redesign (R3 — baseline-of-record), and three post-R3 structural redesigns (R1a, R1b-narrow, R2 — retained research evidence).
2. The **F1 mean-reversion-after-overextension arc** (Phases 3a through 3d-B2) producing one new strategy family (F1) which **HARD REJECTED** at first execution per Phase 3c §7.3 catastrophic-floor predicate. Phase 3e is the docs-only post-F1 research consolidation memo with remain-paused recommendation.
3. The **D1-A funding-aware directional / carry-aware arc** (Phases 3f through 3j) producing one new strategy family (D1-A) which **FRAMEWORK FAILED** at first execution per Phase 3h §11.2 (verdict: MECHANISM PASS / FRAMEWORK FAIL — other; catastrophic-floor predicate NOT triggered; cond_i BTC MED expR > 0 FAILED; cond_iv BTC HIGH cost-resilience FAILED).

Phase 3k is the docs-only post-D1-A research consolidation memo with operator decision menu; primary recommendation is **remain paused** with external-cost-evidence review or regime-first framework memo as acceptable secondary / tertiary alternatives.

Current phase:

```text
Phase 3j merged. Phase 3k docs-only consolidation drafted.
No next phase authorized.
```

Most recent merge:

```text
main HEAD: a7f653123fce822e67fefb62b05bcd152e167267
Merge title:  Merge Phase 3j (D1-A first execution + diagnostics + first-execution-gate eval) into main
              + docs(phase-3j): merge report (5d18408)
              + docs(phase-3j): record merge-report commit hash in section 3 (a7f6531)
Phase 3j merge commit:        5c8537bde462d328985b5c917729c663deaabc04
Phase 3j merge-report commit: 5d18408daaed08ab30be47236f06c9d38c468f99
```

## Strategy Research Arc Outcomes

The two complete strategy-research arcs produced these outcomes:

### V1 breakout arc (Phase 2e through Phase 2w)

- **H0** — locked Phase 2e baseline; remains the **framework anchor**.
- **R3** (Fixed-R take-profit + unconditional time-stop, Phase 2p §C.1) — **baseline-of-record**.
- **R1a** (volatility-percentile setup predicate) — retained as **research evidence**; **non-leading**.
- **R1b-narrow** (bias-strength magnitude threshold) — retained as **research evidence**; **non-leading**.
- **R2** (pullback-retest entry) — final verdict **FAILED — §11.6 cost-sensitivity gate blocks**. M1 ✓, M3 ✓, M2 ✗ (mechanism partially supported); slippage-fragile. Retained as **research evidence** per Phase 2p §D framing.

### F1 mean-reversion arc (Phase 3a through Phase 3d-B2)

- **F1** (mean-reversion-after-overextension; 8-bar cumulative displacement > 1.75 × ATR(20) → SMA(8) frozen target; structural stop with 0.10 × ATR buffer; 8-bar unconditional time-stop; same-direction cooldown until unwind). Phase 3a discovery rank-1 near-term family candidate; Phase 3b spec; Phase 3c execution-planning; Phase 3d-A implementation (deliberately non-runnable); Phase 3d-B1 engine wiring (runnable but guarded); Phase 3d-B2 first execution + first-execution-gate evaluation. **Final verdict: HARD REJECT** (Phase 3c §7.3 catastrophic-floor predicate; 5 separate violations across BTC/ETH × MED/HIGH cells: BTC MED expR=−0.5227, BTC HIGH expR=−0.7000 / PF=0.2181, ETH HIGH expR=−0.5712 / PF=0.2997). M1 BTC PARTIAL (mean +0.024 R below +0.10 threshold; fraction 55.4%); M2 BTC FAIL / ETH weak-PASS; M3 PASS-isolated on both symbols (TARGET subset profitable when isolated, but overwhelmed by 53–54% STOP exits in the wider trade population). **Phase 3d-B2 is terminal for F1.** F1 retained as **research evidence**; **non-leading**; no F1-prime authorized.

### D1-A funding-aware arc (Phase 3f through Phase 3j)

- **D1-A** (funding-aware directional / carry-aware contrarian; trailing-90-day funding-rate Z-score |Z_F| ≥ 2.0 at completed funding-settlement time → enter contrarian at next 15m bar's open; stop = 1.0 × ATR(20); fixed +2.0R target; 32-bar (8-hour) unconditional time-stop; per-funding-event cooldown; band [0.60, 1.80] × ATR(20); contrarian direction; no regime filter). Phase 3f research-direction discovery (post-F1 rank-1 active-path candidate); Phase 3g spec memo + methodology audit; Phase 3h execution-planning memo with timing-clarification amendments; Phase 3i-A implementation-controls (deliberately non-runnable); Phase 3i-B1 engine-wiring (runnable but guarded); Phase 3j first execution + first-execution-gate evaluation. **Final verdict: MECHANISM PASS / FRAMEWORK FAIL — other** (Phase 3h §11.2; catastrophic-floor predicate NOT triggered; cond_i BTC MED expR > 0 FAILED with BTC R MED expR=−0.3217; cond_iv BTC HIGH cost-resilience FAILED with BTC R HIGH expR=−0.4755 / PF=0.5145). M1 BTC h=32 PASS (mean +0.1748 R AND fraction-non-negative 0.5101 — both above thresholds); M2 FAIL on both symbols (BTC funding benefit +0.00234 R ~21× below +0.05 R threshold; ETH +0.00452 R ~11× below); M3 PASS-isolated on both symbols (TARGET subset BTC mean +2.143 R / aggregate +111.46 R; ETH mean +2.447 R / aggregate +119.89 R — overwhelmed by 67–68% STOP exits at −1.30 / −1.24 R mean per loser). Empirical WR ~30% / ~31% vs forecast +51% breakeven. **Phase 3j is terminal for D1-A under the current locked spec.** D1-A retained as **research evidence**; **non-leading**; **no D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid authorized**.

No next strategy phase is authorized.

No paper/shadow planning is authorized.

No Phase 4 (risk/state/persistence runtime) work is authorized.

No live-readiness, deployment, exchange-write, or production-key work is authorized.

The next step is operator-driven only: the operator decides whether and when any subsequent phase is authorized. Until then, the project remains at the post-Phase-3j / Phase-3k consolidation boundary.

---

## Recently Completed Pre-Handoff Documents

The following formerly pending documents have now been created:

```text
docs/09-operations/first-run-setup-checklist.md
docs/00-meta/ai-coding-handoff.md
```

These files complete the practical setup and AI implementation handoff layer.

## First-Run Setup Checklist Status

`docs/09-operations/first-run-setup-checklist.md` now defines the guided setup path for:

- current local environment assumptions,
- repository setup at `C:\Prometheus`,
- GitHub Desktop tracking,
- AntiGravity IDE usage,
- Claude Code extension usage,
- ChatGPT-guided setup support,
- local development setup,
- Python/tooling setup,
- configuration skeletons,
- historical data and research storage,
- runtime database/log/state preparation,
- dry-run runtime setup,
- dashboard and monitor setup,
- Telegram/n8n alert-route setup,
- dedicated NUC preparation,
- host hardening checks,
- backup/restore verification,
- paper/shadow readiness,
- production Binance key timing,
- tiny-live readiness,
- emergency access and recovery readiness.

It explicitly preserves the rule:

```text
Do not create production Binance trade-capable API keys until the correct approved phase gate.
```

## AI Coding Handoff Status

`docs/00-meta/ai-coding-handoff.md` now defines the implementation contract for Claude Code.

It includes:

- repository reading order,
- authority hierarchy,
- locked v1 decisions,
- non-negotiable safety constraints,
- forbidden actions,
- phased implementation plan,
- runnable checkpoints,
- acceptance criteria per phase,
- dual-AI workflow with ChatGPT,
- Claude Code installation authority,
- installation escalation protocol,
- checkpoint reporting protocol,
- ambiguity/spec-gap protocol,
- local development first / NUC later plan,
- migration-to-NUC expectations,
- and copy-paste prompts for Claude Code.

The handoff explicitly requires:

```text
phased implementation
not one-shot generation
runnable checkpoint after every phase
no production exchange-write capability before approved gates
no production Binance keys during early coding
dry-run and paper/shadow before tiny live
operator approval before promotion
```

---

## Locked V1 Decisions

## Market and venue

- Venue: Binance USDⓈ-M futures.
- Initial live symbol: BTCUSDT perpetual.
- First secondary research/comparison symbol: ETHUSDT perpetual.
- V1 live scope: BTCUSDT only.
- ETHUSDT remains research/comparison only until separately approved.

## Strategy

- Strategy family: breakout continuation with higher-timeframe trend filter.
- Signal timeframe: 15m.
- Higher-timeframe bias: 1h.
- Entry style: completed-bar confirmation, then market entry.
- Baseline backtest fill assumption: next-bar open after confirmed signal close.
- Initial stop: structural stop plus ATR buffer.
- Trade management: staged risk reduction and strategy-managed trailing.
- Strategy uses completed bars only.

## Execution

- Runtime account mode: one-way mode.
- Margin mode: isolated margin.
- One symbol first.
- One position maximum.
- No pyramiding in v1.
- No reversal entry while positioned in v1.
- No hedge-mode behavior in v1.
- Entry order: normal MARKET order.
- Protective stop: exchange-side algo/conditional STOP_MARKET.
- Protective stop settings:
  - `closePosition=true`
  - `workingType=MARK_PRICE`
  - `priceProtect=TRUE`
- Stop updates: cancel-and-replace.
- User stream: primary live private-state source.
- REST: placement, cancellation, reconciliation, and recovery.
- Exchange state is authoritative.
- No blind retry for exposure-changing actions.

## Risk

- Initial live risk per trade: 0.25% of sizing equity.
- Initial effective leverage cap: 2x.
- Leverage is a tool to reach valid risk-based position size, not a target.
- Future risk path may work toward 1.00% only after staged validation and review.
- Future leverage caps such as 5x or 10x may be researched later, but are not initial live defaults.
- Internal notional cap is mandatory for live operation.
- Missing risk state, metadata, or exchange-state confidence fails closed.

## Deployment

- Deployment is supervised and staged.
- V1 is not lights-out autonomous.
- Standard rollout path:
  - research,
  - validation,
  - dry-run,
  - paper/shadow,
  - tiny live,
  - scaled live.
- Restart always begins in safe mode.
- Reconciliation is required before normal resumption.
- Incidents are severity-classified.
- Kill switch is persistent and never auto-clears.
- Tiny-live default host: dedicated local NUC / mini PC used only for Prometheus.
- The NUC has an attached desk monitor showing the operator dashboard during operation.
- Dashboard should be always available when the monitor is on.
- Telegram and/or n8n may be used for alert routing, but not as high-risk approval surfaces in v1.
- Production Binance trade-capable keys must not be created until the correct approved phase gate.

---

## Locked Architecture Direction

## Core architecture

- Modular monolith for v1.
- Strict strategy/risk/execution separation.
- Research and live runtime remain separate concerns.
- Exchange state outranks local state.
- Local persistence exists for restart safety and operational continuity.
- Observability is state-centric, not vanity-metric-centric.
- Operator dashboard is a supervision and control surface, not a discretionary trading terminal.
- Manual controls are for safety, recovery, governance, and audit.

## Core runtime principles

- Commands are not facts.
- REST acknowledgements are not final truth.
- User-stream and reconciliation paths confirm state.
- A filled entry is not yet a protected trade.
- A submitted stop is not yet confirmed protection.
- A position without confirmed protection is an emergency state.
- Unknown execution outcomes fail closed.
- Manual/non-bot exposure blocks new bot entries.
- Rollback does not clear safety state.
- Backup restore does not prove exchange truth.
- Approval cannot make unknown state known.

---

## Dashboard / NUC / Alerting Direction

The live operator environment is explicitly centered on:

```text
dedicated local NUC / mini PC
+ attached desk monitor
+ always-on Prometheus dashboard
```

The dashboard should be:

- polished,
- information-rich,
- Binance-like in density where useful,
- focused on Prometheus-specific safety and execution state,
- always visible during operation where practical.

Dashboard should show:

- runtime mode,
- entries allowed/blocked,
- open positions,
- open normal orders,
- open algo/protective orders,
- protective stop state,
- unknown execution outcomes,
- stream health,
- reconciliation state,
- incidents,
- alerts,
- daily loss,
- drawdown,
- risk state,
- host/NUC health,
- release/config state,
- Telegram/n8n route state.

A future TradingView-like candle/setup/trade visualization is allowed and desirable for rule verification.

It should remain read-only and must not become chart trading.

Forbidden in v1:

- arbitrary manual buy/sell,
- click-to-trade,
- manual pyramiding,
- manual reversal,
- manual stop widening,
- casual risk/leverage sliders,
- bypassing reconciliation,
- bypassing kill switch,
- bypassing incidents or approvals.

---

## Completed / Substantially Defined Documentation

The following documentation areas are substantially defined.

## 1. Meta, Setup, and Handoff

```text
docs/00-meta/current-project-state.md
docs/00-meta/ai-coding-handoff.md
docs/09-operations/first-run-setup-checklist.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
```

Defined:

- current high-level project memory checkpoint,
- Claude Code implementation handoff,
- repository reading order,
- phased implementation method,
- dual-AI workflow,
- installation escalation protocol,
- first-run setup path,
- phase gates,
- technical-debt tracking,
- implementation ambiguity/spec-gap log requirement.

## 2. Strategy and Research

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

## 3. Data Layer

```text
docs/04-data/historical-data-spec.md
docs/04-data/timestamp-policy.md
docs/04-data/dataset-versioning.md
docs/04-data/live-data-spec.md
docs/04-data/data-requirements.md
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
- stale market-data gating,
- research storage vs runtime DB separation,
- data setup/runbook requirements connected through the first-run setup checklist.

## 4. Backtesting and Validation

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

## 5. Execution and Exchange

```text
docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md
docs/06-execution-exchange/failure-recovery.md
docs/06-execution-exchange/position-state-model.md
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
- `ORDER_TRADE_UPDATE` / `ACCOUNT_UPDATE` / `ALGO_UPDATE` responsibilities,
- stream staleness and reconciliation behavior,
- clean flat state,
- clean protected-position state,
- unknown execution outcome handling,
- orphaned/multiple stop handling,
- manual/non-bot exposure handling,
- exchange adapter boundaries,
- no blind retry for exposure-changing actions,
- position state normalization,
- one-way `BOTH` semantics,
- `positionAmt` sign interpretation.

## 6. Risk

```text
docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/kill-switches.md
docs/07-risk/daily-loss-rules.md
docs/07-risk/drawdown-controls.md
```

Defined:

- sizing from stop distance and equity risk,
- sizing equity uses strategy allocation boundary,
- initial live risk 0.25%,
- future path toward 1% risk only after staged review,
- initial risk-usage buffer 90%,
- quantity rounded down,
- below-minimum quantity rejects,
- leverage cap and notional cap enforcement,
- BTCUSDT-only live scope,
- one position maximum,
- no pyramiding,
- no reversal while positioned,
- manual exposure blocks entries,
- no stop/no trade,
- stop widening forbidden,
- unprotected live position emergency,
- kill switch behavior,
- daily loss lockouts,
- drawdown controls.

## 7. Runtime Architecture

```text
docs/08-architecture/implementation-blueprint.md
docs/08-architecture/codebase-structure.md
docs/08-architecture/state-model.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/observability-design.md
docs/08-architecture/event-flows.md
docs/08-architecture/database-design.md
docs/08-architecture/deployment-model.md
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
- runtime database design,
- state transition/event log transaction rules,
- event flows,
- deployment stages,
- NUC deployment model,
- alert/dashboard hooks,
- state-centric observability.

## 8. Operations

```text
docs/09-operations/first-run-setup-checklist.md
docs/09-operations/restart-procedure.md
docs/09-operations/incident-response.md
docs/09-operations/operator-workflow.md
docs/09-operations/daily-weekly-review-process.md
docs/09-operations/release-process.md
docs/09-operations/rollback-procedure.md
```

Defined:

- practical first-run setup path,
- safe-mode-first restart,
- reconciliation before resumption,
- clean/recoverable/unsafe mismatch classification,
- incident severity model,
- containment-first incident response,
- operator responsibilities,
- allowed manual actions,
- daily/weekly review cadence,
- release stages and promotion gates,
- rollback for code/config/risk/database/deployment/docs,
- rollback does not bypass reconciliation or clear safety flags.

## 9. Security

```text
docs/10-security/api-key-policy.md
docs/10-security/secrets-management.md
docs/10-security/permission-scoping.md
docs/10-security/audit-logging.md
docs/10-security/host-hardening.md
docs/10-security/disaster-recovery.md
```

Defined:

- least privilege,
- no withdrawal permission,
- production IP restriction,
- environment separation,
- secrets never in code/git/docs/screenshots/chats/logs,
- fail-closed credential behavior,
- key rotation/revocation principles,
- audit logging for safety/security actions,
- dedicated NUC host baseline,
- monitor/dashboard model,
- physical security,
- power/internet/outbound-IP readiness,
- disaster recovery,
- backup/restore,
- credential compromise handling.

## 10. Operator Interface

```text
docs/11-interface/operator-dashboard-requirements.md
docs/11-interface/manual-control-actions.md
docs/11-interface/approval-workflows.md
docs/11-interface/dashboard-metrics.md
docs/11-interface/alerting-ui.md
```

Defined:

- dashboard is supervision/control surface,
- dashboard is always-on on the dedicated NUC monitor where practical,
- top-level runtime status,
- connectivity/stream health,
- position/protection panel,
- open normal orders,
- open algo/protective orders,
- reconciliation/restart panel,
- incidents and alerts,
- recent important events,
- limited manual controls,
- forbidden discretionary manual trading controls,
- approval workflows,
- dashboard metrics catalog,
- Telegram/n8n alerting behavior,
- alert acknowledgement vs resolution,
- TradingView-like read-only chart/review concept.

## 11. Roadmap / Governance

```text
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
```

Defined:

- staged development and deployment gates,
- Claude Code readiness gate,
- first-run setup readiness gate,
- production key readiness gate,
- risk increase gate,
- leverage increase gate,
- notional cap increase gate,
- demotion/pause triggers,
- evidence artifacts,
- technical-debt categories,
- pre-Claude blockers,
- pre-tiny-live blockers,
- implementation ambiguity/spec-gap log requirement.

---

## Immediate Next Tasks

No new strategy phase, paper/shadow planning, Phase 4 runtime implementation, live-readiness, or deployment work is currently authorized.

The next step is operator-driven:

1. Operator reviews Phase 3j final outputs:
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3j_D1A_execution-diagnostics.md`
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3j_closeout-report.md`
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3j_merge-report.md`
2. Operator reviews Phase 3k consolidation memo and decision menu:
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3k_post-D1A-research-consolidation.md`
   - `docs/00-meta/implementation-reports/2026-04-29_phase-3k_closeout-report.md`
3. Operator decides whether and when to authorize any subsequent phase. Phase 3k primary recommendation is **remain paused**; acceptable secondary / tertiary alternatives are **external execution-cost evidence review (docs-only)** or **regime-first research framework memo (docs-only)**, each conditional on explicit ex-ante operator commitment to symmetric-outcome / anti-circular-reasoning discipline. Implementation, backtesting, paper/shadow, Phase 4, live-readiness, deployment, D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, and ML-feasibility authorizations are **NOT** recommended by Phase 3k.
4. Until that authorization, the project remains at the post-Phase-3j / Phase-3k consolidation boundary.

Implementation/code work that proceeds without explicit operator authorization for a specific phase is forbidden.

---

## Claude Code Start Instruction

Phase 0 (repo audit), Phase 1 (local development foundation), the Phase 2 strategy/backtesting research arc (through Phase 2w), the Phase 3 F1 mean-reversion research arc (Phase 3a through Phase 3d-B2 + Phase 3e consolidation), and the Phase 3 D1-A funding-aware research arc (Phase 3f through Phase 3j) are complete and merged to `main`. Phase 3k is the docs-only post-D1-A research consolidation memo with operator decision menu.

Claude Code must not begin any subsequent strategy phase, paper/shadow planning, Phase 4 runtime implementation, live-readiness, or deployment work without explicit operator authorization for that specific phase. Phase 3k's recommended next operator decision is **remain paused** with **external execution-cost evidence review (docs-only)** or **regime-first research framework memo (docs-only)** as acceptable secondary / tertiary alternatives. Any subsequent phase requires explicit operator authorization beyond Phase 3k. **No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, or ML-training authorization flows from Phase 3k.**

The AI coding handoff at `docs/00-meta/ai-coding-handoff.md` remains the authoritative reference for phased implementation method, safety constraints, and reporting protocol. Phase-gate governance at `docs/12-roadmap/phase-gates.md` and the technical-debt register at `docs/12-roadmap/technical-debt-register.md` continue to bound any future phase.

---

## Current 25-File Project Upload Recommendation

For a future ChatGPT project-file continuity cache, use these 25 files.

The repo remains authoritative and should still be inspected directly.

```text
docs/00-meta/current-project-state.md
docs/00-meta/ai-coding-handoff.md
docs/09-operations/first-run-setup-checklist.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
docs/03-strategy-research/v1-breakout-strategy-spec.md
docs/05-backtesting-validation/v1-breakout-validation-checklist.md
docs/04-data/data-requirements.md
docs/04-data/live-data-spec.md
docs/04-data/timestamp-policy.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/binance-usdm-order-model.md
docs/06-execution-exchange/user-stream-reconciliation.md
docs/06-execution-exchange/failure-recovery.md
docs/06-execution-exchange/position-state-model.md
docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/kill-switches.md
docs/08-architecture/implementation-blueprint.md
docs/08-architecture/state-model.md
docs/08-architecture/internal-event-contracts.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/database-design.md
docs/08-architecture/deployment-model.md
```

If a future chat focuses heavily on setup/dashboard/alerts rather than coding handoff, temporarily swap in:

```text
docs/08-architecture/event-flows.md
docs/10-security/host-hardening.md
docs/10-security/disaster-recovery.md
docs/11-interface/dashboard-metrics.md
docs/11-interface/alerting-ui.md
docs/11-interface/manual-control-actions.md
docs/11-interface/approval-workflows.md
```

by removing less immediately needed strategy/data/risk documents, because the repository remains the full source of truth.

---

## Implementation Readiness Status

Current readiness:

```text
Strategy/research (V1 breakout):  Phase 2 research arc complete
                                  H0 anchor; R3 baseline-of-record;
                                  R1a, R1b-narrow, R2 retained as research evidence
Strategy/research (F1 mean-rev):  Phase 3 research arc complete
                                  F1 HARD REJECT (Phase 3d-B2 first execution);
                                  retained as research evidence; non-leading;
                                  Phase 3d-B2 terminal for F1
Strategy/research (D1-A funding): Phase 3 research arc complete
                                  D1-A MECHANISM PASS / FRAMEWORK FAIL - other
                                  (Phase 3j first execution);
                                  retained as research evidence; non-leading;
                                  Phase 3j terminal for D1-A under current locked spec
Historical/live data design:      docs strong; Phase 2e v002 datasets locked
Validation plan:                  implemented through Phase 3j
Risk model:                       docs strong; runtime not yet implemented
Execution model:                  docs strong; runtime not yet implemented
Runtime architecture:             docs strong; runtime not yet implemented
Operations:                       docs strong; runtime not yet implemented
Security:                         docs strong; runtime not yet implemented
Interface/dashboard/alerts:       docs strong; not yet implemented
Roadmap/governance:               strong
AI coding handoff:                created
First-run setup checklist:        created
Claude Code Phase 0 readiness:    completed
Phase 1 local-dev foundation:     completed
Phase 2 data foundation:          completed
Phase 2 strategy research arc:    completed (Phase 2w merged)
Phase 3 F1 research arc:          completed (Phase 3d-B2 merged + Phase 3e consolidation)
Phase 3 D1-A research arc:        completed (Phase 3j merged at 5c8537b;
                                  merge-report 5d18408 / 5d18408+a7f6531)
Phase 3k consolidation memo:      drafted (docs-only; remain-paused primary
                                  recommendation; external-cost-evidence or
                                  regime-first memo as acceptable secondary /
                                  tertiary alternatives)
Phase 4 runtime implementation:   NOT authorized
Paper/shadow planning:            NOT authorized
Live-readiness / deployment:      NOT authorized
Production-key work:              NOT authorized
Exchange-write capability:        NOT authorized
F1-prime / target-subset spec:    NOT authorized; not proposed
D1-A-prime / D1-B / hybrid spec:  NOT authorized; not proposed
ML feasibility memo:              NOT authorized; not proposed
New family research:              NOT authorized; not proposed
```

The project has completed three strategy/backtesting research arcs (V1 breakout through Phase 2w; F1 mean-reversion through Phase 3d-B2; D1-A funding-aware through Phase 3j). Phase 3k is the docs-only post-D1-A consolidation memo with operator decision menu; recommended next operator decision is **remain paused** with external-cost-evidence review or regime-first framework memo as acceptable secondary / tertiary alternatives.

It is not ready for Phase 4 runtime implementation, paper/shadow operation, exchange-write capability, production Binance keys, or live trading. No subsequent phase has been authorized; the next step requires explicit operator authorization for that specific phase.

---

## Document Status

- Status: ACTIVE
- Updated: 2026-04-29
- Owner: Project operator
- Role: High-level project memory checkpoint after Phase 3j + Phase 3k consolidation
