# Scope and Non-Goals

## Purpose
Define what the project is trying to accomplish in the near term and what it is explicitly not trying to accomplish yet.

## Scope
This document applies to the current research and v1 system-design horizon.

## Background
A common failure pattern in trading-system projects is trying to solve too many layers at once: strategy discovery, ML, portfolio scaling, live automation, dashboards, and infrastructure hardening. This project intentionally narrows scope to build a strong foundation.

## Definitions
- **Near-term scope**: current design and first implementation horizon.
- **Non-goal**: something that may be useful later but is intentionally excluded for now.

## Main Framework / Design / Rules

### In Scope
- production-oriented research and design
- rules-based strategy development
- futures-capable architecture
- realistic validation standards
- exchange execution correctness
- explicit risk controls
- observability and operator visibility
- staged deployment from research to shadow to tiny live

### Out of Scope for Now
- autonomous self-learning live trading
- RL-first architecture
- HFT / ultra-low-latency systems
- multi-exchange routing and abstraction complexity
- large multi-strategy portfolio platform in v1
- deeply integrated UI-first development
- broad alternative-data pipelines before core execution is trustworthy

## Assumptions
- The first meaningful milestone is a trustworthy single-strategy system, not a feature-rich platform.
- Futures are the preferred target, but the design should preserve a spot reference path where helpful.

## Risks and Failure Modes
- Scope creep disguised as ambition
- Premature optimization
- Using architecture abstractions to solve hypothetical future needs
- Building a polished UI before engine correctness is proven

## Open Questions
- Should the first live-capable version remain single-symbol through the first live cycle?
- Which operational tooling belongs in v1 versus v1.5?

## Decisions
- Self-learning automation is a non-goal for the initial phases.
- UI integration is a later-phase concern, not a precondition for core engine design.

## Next Steps
- Lock first-strategy candidate set
- Define promotion gates in detail
- Expand scope controls through milestone documents

## References
- `project-objective.md`
- `decision-framework.md`
