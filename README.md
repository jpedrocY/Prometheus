# Prometheus

Prometheus is a **production-oriented, safety-first, operator-supervised trading system** for **Binance USDⓈ-M futures**.

The v1 project is intentionally **rules-based**, **not self-learning**, and designed to be built in **phases with review gates**, runnable checkpoints, and explicit human approval before any move toward real exchange-write capability.

## Current status

**Project state:** post-Phase 2p consolidation.

What that means right now:

- **H0** remains the formal validation anchor.
- **R3** is the formal **baseline-of-record** for future family work.
- **R1a** is preserved as **research evidence only** and retained for future hypothesis planning, not as the current default path.
- The project is **intentionally paused** on new strategy execution until a future phase is explicitly authorized.
- **Paper/shadow planning, Phase 4 runtime work, and any live-readiness path remain deferred.**
- The current pytest baseline is **417 passing tests**.

## What Prometheus is trying to become

Prometheus is not meant to be a one-shot backtest script.

The target is a staged trading system with:

- research-quality historical data handling,
- reproducible backtesting and validation,
- strict risk and governance controls,
- safe runtime-state handling and reconciliation,
- dry-run and paper/shadow stages before any live exposure,
- operator supervision throughout v1.

## Current research conclusion

The project has tested the breakout family in multiple structured phases.

The key conclusion at the end of Phase 2p is:

- **R3** is the strongest result so far and is the version future work should start from.
- **R1a** taught the project something useful about conditional edge, especially on ETH, but it did **not** become the new universal default.
- The project has **not** demonstrated live readiness or strong enough absolute edge to justify moving toward deployment yet.

## Locked baseline-of-record

The current baseline-of-record is **R3**, which keeps the original entry side mostly intact while replacing the old staged exit machinery with a simpler exit philosophy:

- `exit_kind = FIXED_R_TIME_STOP`
- `exit_r_target = 2.0`
- `exit_time_stop_bars = 8`
- same-bar priority: `STOP > TAKE_PROFIT > TIME_STOP`
- initial protective stop is never moved intra-trade

This is the version future research should treat as the reference candidate unless later evidence clearly replaces it.

## What the project has **not** done yet

Prometheus is still in a research / pre-runtime stage.

The repo has **not** started:

- Phase 4 runtime/state/persistence implementation,
- paper/shadow operation,
- tiny-live preparation,
- scaled-live preparation,
- production Binance key creation,
- live exchange-write capability.

## Safety principles

Prometheus is deliberately conservative.

Important assumptions that still hold:

- no production trade-capable Binance keys should exist yet,
- credentials alone must never enable trading,
- dry-run and paper/shadow must come before tiny live,
- unknown state must fail closed,
- restart must begin in `SAFE_MODE`,
- operator approval is required across major phase boundaries.

## Repository layout

```text
Prometheus/
├─ docs/                     # canonical project memory and specifications
├─ src/                      # implementation code
├─ tests/                    # unit/integration validation
├─ scripts/                  # phase runners and research helpers
├─ data/                     # local research/runtime artifacts (git-ignored where appropriate)
└─ README.md                 # this file
```

For the full documentation map, read:

- `docs/README.md`

## Most important documents

Start here if you want to understand the repo quickly:

- `docs/00-meta/current-project-state.md`
- `docs/00-meta/ai-coding-handoff.md`
- `docs/09-operations/first-run-setup-checklist.md`
- `docs/12-roadmap/phase-gates.md`
- `docs/12-roadmap/technical-debt-register.md`
- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`

For the research state that led to the current consolidation:

- `docs/00-meta/implementation-reports/2026-04-26_phase-2l_R3_variant-comparison.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2n_strategy-review-memo.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2o_asymmetry-review-memo.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2p_consolidation-memo.md`

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

Do not treat successful local tests as authorization for live trading. They only confirm the current research/code state.

## Working method

The project has been developed with a dual-review workflow:

- **Claude Code** performs repo work inside the local checkout.
- **ChatGPT** reviews plans, reports, checkpoint outputs, errors, and phase-gate decisions.
- The **operator** is the approval authority.

That workflow is intentional and should be preserved for future phases.

## Phase model

Prometheus is governed by staged phase gates.

High-level phase sequence:

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

Research sub-phases and review phases may exist inside or around those boundaries, but promotion is always evidence-based and never automatic.

## Current recommendation

If you are reopening this repo later, the correct default assumption is:

- start from **R3 as the baseline-of-record**,
- treat **R1a as preserved research evidence**,
- do **not** restart execution momentum automatically,
- do **not** start readiness planning automatically,
- use the most recent implementation reports to decide whether a new docs-only planning phase is justified.

## License / usage

Add the project license here if and when one is selected.
