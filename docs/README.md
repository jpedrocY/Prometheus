# Documentation Map

## Purpose
This `docs/` directory is the canonical living memory of the project.

It is designed to serve four roles at the same time:
1. long-term technical memory for the project,
2. implementation context for future AI-assisted coding,
3. decision history and rationale tracking,
4. a structured knowledge base for human review.

Markdown is intentionally the primary format because it is:
- easy to version,
- easy to diff,
- easy to feed into AI tools,
- easy to refine incrementally.

Later, selected material may be converted into more polished human-readable reports or LaTeX/PDF outputs. Those polished outputs are not the source of truth; these Markdown files are.

## Folder Guide
- `00-meta/` project mission, scope, assumptions, decision logic
- `01-foundations/` conceptual foundations and system framing
- `02-market-structure/` market-specific mechanics, especially futures
- `03-strategy-research/` strategy families and formalization work
- `04-data/` data requirements, normalization, versioning
- `05-backtesting-validation/` evidence standards and promotion gates
- `06-execution-exchange/` exchange adapter and execution mechanics
- `07-risk/` risk philosophy and trading constraints
- `08-architecture/` system design and component boundaries
- `09-operations/` operator workflows and incident handling
- `10-security/` key handling, permissions, auditability, host protection
- `11-interface/` future dashboard/operator console requirements
- `12-roadmap/` milestones, phase gates, implementation sequencing
- `adr/` architecture decision records
- `runbooks/` operational procedures for known incident classes
- `glossary/` shared definitions
- `templates/` standard Markdown templates for future docs

## ADR Usage
Important architectural and project-level decisions should be recorded as ADRs.  
An ADR should answer:
- what decision was made,
- why it was made,
- what alternatives were considered,
- what consequences follow from it.

## Review Order
Recommended first review:
1. `00-meta/project-objective.md`
2. `00-meta/scope-and-non-goals.md`
3. `00-meta/decision-framework.md`
4. `07-risk/risk-philosophy.md`
5. `08-architecture/system-overview.md`
6. `adr/ADR-001-use-markdown-as-canonical-memory.md`
7. `adr/ADR-002-target-binance-usdm-futures-first.md`
8. `adr/ADR-003-separate-trading-engine-from-ui.md`

## Compact Structure
```text
docs/
  00-meta/
  01-foundations/
  02-market-structure/
  03-strategy-research/
  04-data/
  05-backtesting-validation/
  06-execution-exchange/
  07-risk/
  08-architecture/
  09-operations/
  10-security/
  11-interface/
  12-roadmap/
  adr/
  runbooks/
  glossary/
  templates/
```
