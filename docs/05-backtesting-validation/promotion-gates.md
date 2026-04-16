# Promotion Gates

## Purpose
Define the standards required to move between major project stages.

## Scope
This document covers promotion from research to shadow to live.

## Background
Without gates, system promotion becomes arbitrary and emotionally driven.

## Definitions
- **Promotion gate**: formal threshold required before entering the next operating stage.

## Main Framework / Design / Rules

### Gate A — Research Candidate -> Serious Validation
Requirements:
- explicit rule definition
- cost-aware backtest
- identifiable regime fit
- understandable failure modes

### Gate B — Validation -> Paper/Shadow
Requirements:
- no unresolved logic ambiguity
- stable parameter region
- acceptable drawdown behavior
- trade log and analytics export available

### Gate C — Shadow -> Tiny Live
Requirements:
- exchange-path correctness demonstrated
- restart behavior tested
- no unexplained state mismatches
- risk controls active
- operator workflow ready
- rollback procedure documented

### Gate D — Tiny Live -> Scaled Live
Requirements:
- behavior matches design expectations
- no major execution surprises
- alerts and observability proven
- post-trade review process functioning

## Assumptions
- Promotion gates should be written before the pressure to promote arises.

## Risks and Failure Modes
- moving forward because of excitement or impatience
- turning exceptions into habits
- scaling more than one dimension at once

## Open Questions
- What quantitative thresholds will be used at each gate?

## Decisions
- shadow is mandatory before live
- live scaling should occur one dimension at a time

## Next Steps
- add numeric thresholds after first strategy family is selected

## References
- `paper-vs-shadow-vs-live.md`
- `../01-foundations/system-maturity-model.md`
