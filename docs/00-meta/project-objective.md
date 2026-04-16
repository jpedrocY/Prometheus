# Project Objective

## Purpose
Define the primary objective of the project and anchor all future decisions to that objective.

## Scope
This document covers the project mission at a high level. It does not define implementation details, strategy rules, or deployment thresholds.

## Background
The project aims to build a production-oriented crypto trading system that is AI-assisted in selected roles, but not prematurely dependent on AI for live decision-making. The near-term focus is disciplined research, system design, and validation.

## Definitions
- **AI-assisted**: AI is used where it improves research, coding, analysis, monitoring, or later model operations, without granting uncontrolled authority over live risk.
- **Production-oriented**: Designed for realistic deployment concerns such as exchange behavior, uptime, state recovery, auditability, and operator control.
- **Rules-based**: Deterministic logic that can be inspected, tested, and reproduced.

## Main Framework / Design / Rules
The project objective is to design, validate, and eventually deploy a robust crypto trading bot that can:
- generate and execute rule-based trading decisions,
- interact correctly with exchange infrastructure,
- manage risk under explicit policy constraints,
- produce auditable logs and state,
- support staged rollout from research to live trading,
- later incorporate ML/AI only where justified by evidence and operational controls.

The initial target is not a self-learning autonomous trader. The initial target is a controlled, testable, futures-capable system with strong architecture and risk foundations.

## Assumptions
- The primary market candidate is Binance USDⓈ-M futures.
- The first live-capable version should be rules-based.
- Futures capability is a deliberate design choice, not an afterthought.
- A future operator UI is expected, but it should remain separate from the trading engine.

## Risks and Failure Modes
- Chasing novelty over reliability
- Expanding scope too early
- Treating AI as a substitute for validation
- Collapsing research, execution, and UI concerns into one codebase
- Confusing a profitable backtest with production readiness

## Open Questions
- Which strategy family should be implemented first?
- What exact symbol set should v1 target?
- What exact promotion criteria will be required for tiny live deployment?

## Decisions
- The project is documentation-first.
- The first system is rules-based.
- AI/ML is deferred to later, constrained roles unless evidence supports earlier use.

## Next Steps
- Finalize the first strategy-family selection framework
- Expand risk policy documents
- Define the execution and reconciliation architecture in more detail

## References
- `scope-and-non-goals.md`
- `decision-framework.md`
- `../07-risk/risk-philosophy.md`
- `../08-architecture/system-overview.md`
