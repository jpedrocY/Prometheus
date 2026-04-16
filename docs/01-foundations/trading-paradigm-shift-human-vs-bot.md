# Trading Paradigm Shift: Human vs Bot

## Purpose
Capture the conceptual shift required when moving from discretionary personal trading to building an automated system.

## Scope
This document addresses mindset and system implications, not specific strategy rules.

## Background
A human trader can tolerate ambiguity, visual interpretation, context switching, and occasional inconsistency. A bot cannot. A bot needs explicit rules, defined state, predictable behavior, and recoverable failure handling.

## Definitions
- **Discretionary trading**: decisions made with flexible human judgment.
- **Systematic trading**: decisions made according to codified rules.
- **Formalization**: converting human concepts into machine-executable logic.

## Main Framework / Design / Rules

### What Humans Do Well
- contextual interpretation
- ambiguity tolerance
- visual pattern recognition
- adapting to unusual conditions without explicit preprogramming

### What Bots Do Well
- rule consistency
- fast repeated evaluation
- state tracking
- auditability
- disciplined enforcement of risk and process

### What Changes in the Bot Paradigm
A setup is no longer “obvious because it looks good.”  
It must be expressed as:
- a precise definition,
- measurable inputs,
- explicit entry and exit rules,
- explicit invalidation rules,
- explicit risk behavior.

## Assumptions
- Existing discretionary knowledge is valuable, but it must be translated, not copied directly.

## Risks and Failure Modes
- hiding discretion inside vague rule descriptions
- coding visual concepts that are not actually well defined
- overestimating how much human intuition can be mimicked cheaply

## Open Questions
- Which current discretionary concepts can survive honest formalization?

## Decisions
- Formalization quality is more important than preserving every discretionary nuance.

## Next Steps
- Build the first strategy formalization framework
- Score candidate concepts by testability

## References
- `failure-modes-overview.md`
- `../03-strategy-research/price-action-concepts-formalization.md`
