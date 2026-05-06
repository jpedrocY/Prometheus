# Prometheus

Prometheus is a **production-oriented, safety-first, operator-supervised trading system** for **Binance USDⓈ-M futures**.

The v1 project is intentionally **rules-based**, **not self-learning**, and built in **phases with review gates**, runnable checkpoints, and explicit human approval before any move toward real exchange-write capability.

## Current status

**Project state:** post-Phase 4ak (M0 governance adoption merged to `main`).

What that means right now:

- The project is **intentionally paused**. No new strategy candidate, fresh-hypothesis discovery, market research, backtest, paper / shadow, live-readiness, deployment, exchange-write, production-key, MCP, Graphify, `.mcp.json`, or credential work is authorized.
- Six terminal strategy rejections are on the project record (see "Strategy research arc outcomes" below).
- **R3** remains the **baseline-of-record**; **H0** remains the framework anchor; **R1a** and **R1b-narrow** remain retained research evidence (non-leading).
- The **M0 mechanism-admissibility gate** is now **binding prospective governance** for any future research lane (durable artifact: [docs/00-meta/m0-mechanism-admissibility-gate.md](docs/00-meta/m0-mechanism-admissibility-gate.md)).
- The **Phase 4a–4c local safe runtime foundation** is implemented and behind quality gates, but is strategy-agnostic and not authorized to place orders.
- Pytest baseline: **785 passing tests**; full-repo `ruff check .` clean; `mypy --strict` clean across 82 source files.

## Strategy research arc outcomes

The project has produced three complete strategy-research arcs and one alt-symbol substrate arc, all of which terminated without producing a validated strategy.

| Strategy | Family signature                          | Verdict                                            |
| -------- | ----------------------------------------- | -------------------------------------------------- |
| H0       | V1 breakout framework anchor              | FRAMEWORK ANCHOR (preserved)                       |
| R3       | Fixed-R take-profit + unconditional time-stop | BASELINE-OF-RECORD                              |
| R1a      | Volatility-percentile setup predicate     | Retained research evidence — non-leading           |
| R1b-narrow | Bias-strength magnitude threshold       | Retained research evidence — non-leading           |
| R2       | V1 pullback-retest variant                | FAILED — §11.6 cost-sensitivity blocks             |
| F1       | Mean-reversion after overextension        | HARD REJECT (Phase 3d-B2 catastrophic-floor)       |
| D1-A     | Funding-aware contrarian directional rule | MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3j) |
| V2       | Participation-confirmed breakout          | HARD REJECT (Phase 4l — design-stage; zero trades) |
| G1       | Regime-first breakout continuation        | HARD REJECT (Phase 4r — gate × setup sparseness)   |
| C1       | Volatility-contraction expansion breakout | HARD REJECT (Phase 4x — fires-and-loses)           |

The 5m diagnostic thread (Phases 3o → 3p → 3q → 3r → 3s → 3t) is operationally closed.

The alt-symbol substrate arc (Phases 4aa → 4ai) on BTCUSDT / ETHUSDT / SOLUSDT / XRPUSDT / ADAUSDT produced descriptive cost-cushion / regime-continuity / cross-sectional ranking evidence, with the Phase 4ai cross-sectional ranking feasibility lane returning `NOT_SUPPORTED`. No strategy was promoted from substrate work.

After Phase 4y (post-C1 consolidation) and Phase 4z (post-rejection research-process redesign), the project pivoted to docs-only governance work: Phase 4ag mechanism-source triage; Phase 4ah / 4ai cross-sectional feasibility; Phase 4aj M0 governance reconciliation; Phase 4ak M0 governance adoption.

## What the project has not done yet

Prometheus has **not** started:

- paper / shadow operation,
- tiny-live preparation,
- scaled-live preparation,
- production Binance trade-capable key creation,
- live exchange-write capability,
- authenticated REST / private endpoints / user stream / WebSocket / listenKey integration in code,
- MCP / Graphify / `.mcp.json` / credentials work.

Phase 4 canonical (paper / shadow / live-readiness gates) remains unauthorized. The Phase 4a–4c runtime foundation that is implemented is local-only, fake-exchange, exchange-write-free, and strategy-agnostic per the Phase 3x scoping memo and Phase 4a authorization brief.

## Project locks (preserved verbatim across every phase)

- **§11.6** HIGH cost = 8 bps per side (round-trip = 16 bps).
- **§1.7.3** project-level locks: 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation governance.
- Phase 4j §11 metrics OI-subset partial-eligibility rule.
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy-spec discipline; Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy-spec discipline; Phase 4w C1 backtest-plan methodology.
- **M0 mechanism-admissibility gate** and **post-null cooldown rule** (binding prospective; adopted Phase 4ak).

## Safety principles

Prometheus is deliberately conservative.

- No production trade-capable Binance keys exist or are authorized.
- Credentials alone must never enable trading; live exchange-write capability requires explicit environment / config / phase-gate approval.
- Dry-run, fake-adapter, and paper / shadow stages must come before any tiny-live operation.
- Unknown state must fail closed; restart must begin in `SAFE_MODE`.
- Operator approval is required across major phase boundaries.
- Every future research lane must clear the **M0 admissibility gate** before discovery, hypothesis spec, strategy spec, or backtest work.

## Repository layout

```text
Prometheus/
├─ docs/                     # canonical project memory, specifications, governance, implementation reports
├─ src/prometheus/           # Phase 4a–4c local safe runtime foundation (state, persistence, events, governance,
│                            #   risk sizing/exposure/stop-validation, fake_adapter, operator, cli)
├─ tests/                    # 785 passing pytest tests
├─ scripts/                  # standalone phase research scripts (no runtime imports; no network I/O)
├─ data/                     # local research/runtime artifacts (most paths git-ignored)
└─ README.md                 # this file
```

For the full documentation map, read [docs/README.md](docs/README.md).

## Most important documents

Start here if you want to understand the repo quickly:

- [docs/00-meta/current-project-state.md](docs/00-meta/current-project-state.md) — high-level project memory checkpoint
- [docs/00-meta/m0-mechanism-admissibility-gate.md](docs/00-meta/m0-mechanism-admissibility-gate.md) — binding prospective governance for any future research lane
- [docs/00-meta/ai-coding-handoff.md](docs/00-meta/ai-coding-handoff.md)
- [docs/09-operations/first-run-setup-checklist.md](docs/09-operations/first-run-setup-checklist.md)
- [docs/12-roadmap/phase-gates.md](docs/12-roadmap/phase-gates.md)
- [docs/12-roadmap/technical-debt-register.md](docs/12-roadmap/technical-debt-register.md)
- [docs/03-strategy-research/v1-breakout-strategy-spec.md](docs/03-strategy-research/v1-breakout-strategy-spec.md)
- [docs/05-backtesting-validation/v1-breakout-validation-checklist.md](docs/05-backtesting-validation/v1-breakout-validation-checklist.md)

Representative recent implementation reports (full set under `docs/00-meta/implementation-reports/`):

- Phase 2p consolidation memo (R3 baseline-of-record locked)
- Phase 2w consolidation (R2 FAILED — §11.6)
- Phase 3d-B2 (F1 HARD REJECT)
- Phase 3j (D1-A MECHANISM PASS / FRAMEWORK FAIL)
- Phase 3t (5m diagnostic thread closure)
- Phase 4a (local safe runtime foundation)
- Phase 4l (V2 backtest execution — Verdict C HARD REJECT)
- Phase 4m (post-V2 strategy-research consolidation; 18-requirement validity gate)
- Phase 4r (G1 backtest execution — Verdict C HARD REJECT)
- Phase 4s (post-G1 consolidation)
- Phase 4t (post-G1 fresh-hypothesis discovery)
- Phase 4x (C1 backtest execution — Verdict C HARD REJECT)
- Phase 4y (post-C1 consolidation)
- Phase 4z (post-rejection research-process redesign)
- Phase 4ag (research-program pivot / mechanism-source triage)
- Phase 4ai (cross-sectional trend feasibility — `NOT_SUPPORTED`)
- Phase 4aj (M0 governance reconciliation)
- Phase 4ak (M0 governance adoption)

## Local development

The project uses **uv** for environment and command execution.

Typical local commands:

```powershell
cd C:\Prometheus
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Do not treat successful local tests as authorization for live trading. They confirm the current research / runtime-foundation code state only.

## Working method

The project is developed with a dual-review workflow:

- **Claude Code** performs repo work inside the local checkout.
- **ChatGPT** reviews plans, reports, checkpoint outputs, errors, and phase-gate decisions.
- The **operator** is the approval authority.

That workflow is intentional and is preserved for future phases.

## Phase model

Prometheus is governed by staged phase gates.

High-level phase sequence:

```text
PHASE 0 — Documentation and implementation planning
PHASE 1 — Local development foundation
PHASE 2 — Historical data, validation foundation, and V1 strategy research arc
PHASE 3 — F1 / D1-A research arcs and 5m diagnostic thread
PHASE 4 — Local safe runtime foundation, V2 / G1 / C1 research arcs, alt-symbol substrate arc, governance adoption
PHASE 5 — Dashboard, observability, and alerts (not started; not authorized)
PHASE 6 — Dry-run exchange simulation (not started; not authorized)
PHASE 7 — Paper / shadow operation (not authorized)
PHASE 8 — Tiny live (not authorized)
PHASE 9 — Scaled live (not authorized)
```

Phases 4a–4c (runtime foundation) are merged but strategy-agnostic; Phase 4 canonical (the live-readiness gate) is **not** authorized. Research sub-phases live inside Phase 4 (e.g., 4f → 4l for V2; 4n → 4r for G1; 4u → 4x for C1; 4aa → 4ai for alt-symbol substrate).

## Current recommendation

If you are reopening this repo later, the correct default assumption is:

- start from **R3 as the baseline-of-record**;
- treat **R1a / R1b-narrow** as preserved research evidence (non-leading);
- do **not** restart strategy execution momentum automatically;
- do **not** start readiness or live-path planning automatically;
- any future research lane must clear the **M0 admissibility gate** ([docs/00-meta/m0-mechanism-admissibility-gate.md](docs/00-meta/m0-mechanism-admissibility-gate.md)) before discovery / spec / backtest;
- read the most recent implementation reports under `docs/00-meta/implementation-reports/` to decide whether a new docs-only phase is justified.

## License / usage

Add the project license here if and when one is selected.
