# Current Project State

## Purpose

This document is the top-level state snapshot for the Prometheus project.

Its purpose is to make the current project status easy to understand at a glance by recording:

- the current phase,
- the major locked decisions,
- the most important open questions,
- the current source-of-truth documents,
- the immediate next implementation-planning steps,
- and the required working method.

This file is a coordination document, not a replacement for topic-specific specifications.

If this file ever conflicts with a more specific topic document, the topic document is authoritative.

## Current Phase

The project is currently in:

- **implementation architecture and execution-planning**

### Meaning of this phase

This means:

- the first strategy family has already been selected,
- the v1 strategy specification has already been written,
- the historical-data, validation, execution, operations, and security directions are already substantially defined,
- and the next priority is to build the bridge from research/specification into implementation-ready architecture.

This is **not** the phase for jumping directly into broad coding without structure.

The next priority is to define:

- implementation blueprint,
- runtime state model,
- observability design,
- operator dashboard requirements,
- and release / deployment process.

## Project Summary

Prometheus is being developed as a production-oriented, AI-assisted but initially rules-based trading system.

The project is intentionally **not** starting as a self-learning autonomous AI trading bot.

The current design direction is:

- narrow scope first,
- supervised deployment first,
- one symbol first,
- one position first,
- strong operational safety,
- realistic backtesting,
- explicit reconciliation and restart behavior,
- and disciplined documentation before implementation.

## Locked Decisions

The following decisions are already accepted and should not be changed casually.

## Strategy and Market

- venue: **Binance USDⓈ-M futures**
- primary symbol: **BTCUSDT perpetual**
- first secondary comparison symbol: **ETHUSDT perpetual**
- strategy family: **breakout continuation with higher-timeframe trend filter**
- signal timeframe: **15m**
- higher-timeframe bias timeframe: **1h**
- execution style: **bar-close confirmation, then market entry**
- baseline backtest fill assumption: **next-bar open after confirmed signal close**

## Risk and Trade Management

- stop model: **structural stop + ATR buffer + exchange-side protection**
- initial live deployment risk: **0.25% equity risk per trade**
- leverage is treated as a **tool to reach valid position size**, not a target
- initial live scope remains **one symbol, one position, supervised rollout**
- preferred live exit philosophy is **staged risk reduction, then trailing**, not a pure fixed take-profit

## Research and Data

- official Binance USDⓈ-M endpoints are the canonical historical source
- historical research storage is **Parquet**
- the default local research query engine is **DuckDB**
- canonical timezone is **UTC**
- canonical timestamp format is **Unix milliseconds**
- canonical bar identity uses **open_time**
- strategy logic may use **completed bars only**
- normalized and derived datasets used for formal research must be versioned explicitly

## Execution and Operations

- v1 uses **one-way mode**
- v1 uses **isolated margin**
- v1 runs **BTCUSDT only** in the first live-capable form
- user-stream events are the **primary live source of truth**
- REST is used for placement, cancellation, reconciliation, and recovery
- protective stop uses:
  - `STOP_MARKET`
  - `closePosition=true`
  - `MARK_PRICE`
  - `priceProtect=TRUE`
- restart always begins in **safe mode**
- no new entries are allowed until restart reconciliation succeeds
- incident handling is **severity-based**
- v1 is **operator-supervised**, not lights-out autonomous

## Security

- API keys must follow **least privilege**
- withdrawal permission must remain **disabled**
- production keys must use **IP restriction**
- secrets must never live in:
  - code
  - git
  - docs
  - screenshots
  - chats
  - or normal logs
- startup must fail closed if required secrets or permissions are missing or invalid

## Most Important Open Questions

The following remain open and should be resolved through research, validation, or architecture work rather than assumption.

## Strategy Validation

- Which exit model is most robust after realistic fees, funding, and slippage?
- Does BTCUSDT clearly outperform ETHUSDT for this strategy, or are both similarly viable?
- Is EMA 50 / 200 materially more robust than EMA 20 / 100?
- Which setup-window length is most robust across folds?
- Which breakout and stop buffers are robust rather than merely attractive in one period?
- How sensitive are results to slippage assumptions?
- Does mark-price-based stop sensitivity materially change conclusions?

## Runtime and Execution Architecture

- What exact runtime state model should be used?
- What exact client order ID format should be standardized?
- What exact thresholds should define stale market-data and user-data streams?
- What exact timeout should define missing entry confirmation?
- What exact timeout should define missing stop confirmation?
- Under which failure scenarios should the bot flatten immediately versus preserve protection and wait for review?

## Observability and Operations

- What exact health signals, metrics, and alerts should be mandatory in v1?
- Which alerts require immediate operator escalation versus passive review?
- What exact release / promotion path should be used from development to paper / shadow to tiny live?
- What exact daily and weekly review templates should become standard?

## Security and Deployment

- Should v1 production use one key or split trading and monitoring keys from the start?
- What exact runtime secret-loading method should be used on the first production host?
- What exact permission scoping should be defined for each operational role?
- Where should key and secret inventory metadata live operationally?

## Source-of-Truth Documents

The following documents are currently authoritative in their areas.

## Strategy Research

- `docs/03-strategy-research/first-strategy-comparison.md`
- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`

## Data

- `docs/04-data/historical-data-spec.md`
- `docs/04-data/timestamp-policy.md`
- `docs/04-data/dataset-versioning.md`

## Validation

- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`

## Execution / Exchange

- `docs/06-execution-exchange/btcusdt-v1-order-handling-notes.md`

## Operations

- `docs/09-operations/restart-procedure.md`
- `docs/09-operations/incident-response.md`
- `docs/09-operations/operator-workflow.md`
- `docs/09-operations/daily-weekly-review-process.md`

## Security

- `docs/10-security/api-key-policy.md`
- `docs/10-security/secrets-management.md`

## Authority Rule

If any older summary, earlier chat, or high-level overview conflicts with one of the topic documents above, the topic document wins.

## Known Document Notes

The project should remain alert to documentation drift.

Current notes:

- the historical data specification required cleanup due to formatting / copy-paste corruption and should now be treated as the corrected version
- high-level project summaries can drift behind the more detailed topic documents
- this file exists partly to reduce future drift by making the current phase and next steps explicit

## Immediate Next Steps

The next recommended documents / planning steps are:

1. `docs/08-architecture/implementation-blueprint.md`
2. `docs/08-architecture/state-model.md`
3. `docs/08-architecture/observability-design.md`
4. `docs/11-interface/operator-dashboard-requirements.md`
5. `docs/09-operations/release-process.md`

## Why these are next

These are the highest-value bridge documents between the current specification-heavy phase and the first serious coding phase.

The project already has strong strategy, data, execution, operations, and security policies.

What it still needs most is:

- implementation structure,
- state ownership and transitions,
- observability requirements,
- operator interface requirements,
- and release discipline.

## Required Working Method

This workflow is mandatory for project work:

1. research, analyze, compare, and think through the decision space carefully
2. present reasoning, tradeoffs, conclusions, and recommendations clearly
3. wait for agreement, disagreement, or adjustments
4. only after approval write or rewrite the Markdown file

Do not skip straight to file generation unless explicitly asked.

## Out of Scope Right Now

The following are intentionally out of scope for the current phase unless explicitly revisited:

- a self-learning live AI bot as the initial production system
- lights-out autonomous deployment
- hedge mode
- multi-symbol portfolio orchestration
- portfolio-level backtesting as the first implementation target
- machine-learning overlays in v1
- alternative data as a default input
- excessive strategy complexity before baseline validation
- premature coding without architecture/state-model clarity

## Current Success Condition

The project should consider the current phase successful when:

- the implementation blueprint is clear,
- the runtime state model is explicit,
- the observability design is defined,
- the operator dashboard requirements are documented,
- the release / promotion process is documented,
- and the project is ready to begin coding from a stable architecture rather than from scattered assumptions.