# ADR ID: 003

## Title
Separate Trading Engine from Future Operator Interface

## Status
Accepted

## Date
2026-04-16

## Context
A future dashboard or operator console is expected, possibly running on a small desk display and potentially built with a web stack. Mixing that concern directly into the engine would increase coupling and risk.

## Decision
The trading engine and future operator interface must remain separate layers or services with explicit boundaries.

## Consequences
### Positive
- safer failure boundaries
- easier testing and replacement of the UI
- cleaner deployment model
- easier long-term maintenance

### Negative
- requires a defined contract between engine and interface
- may introduce some additional integration work later

## Alternatives Considered
- embedding engine logic directly in a web application
- UI-first architecture
- delaying boundary definition until implementation

## Open Questions
- What should be the first interface contract: API, DB read model, event stream, or hybrid?

## Related Documents
- `../08-architecture/system-overview.md`
- `../08-architecture/service-boundaries.md`
