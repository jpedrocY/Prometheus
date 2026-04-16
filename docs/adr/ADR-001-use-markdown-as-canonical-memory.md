# ADR ID: 001

## Title
Use Markdown as Canonical Project Memory

## Status
Accepted

## Date
2026-04-16

## Context
The project needs a durable, version-friendly documentation system that can serve both humans and AI tools across long research and implementation phases.

## Decision
Markdown files inside the repository will be the canonical living documentation and memory layer for the project.

## Consequences
### Positive
- easy version control and diffing
- AI-friendly context format
- incremental editing is simple
- low tooling friction

### Negative
- presentation quality is lower than polished publishing formats
- documentation discipline must be maintained manually

## Alternatives Considered
- ad hoc chat history only
- wiki-first documentation
- LaTeX-first documentation
- proprietary note tools as primary memory

## Open Questions
- Which docs should later be promoted into polished report form?

## Related Documents
- `../README.md`
- `../00-meta/project-objective.md`
