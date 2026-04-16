# Assumptions

## Purpose
Record working assumptions currently guiding research and design so they remain explicit and reviewable.

## Scope
These are working assumptions, not permanent truths. They may be updated through ADRs or later design reviews.

## Background
Many project failures arise from unstated assumptions. Writing them down early makes revisions cleaner and design tradeoffs easier to understand.

## Definitions
- **Working assumption**: a currently accepted premise used to move the project forward.
- **Design assumption**: an assumption with architectural consequences.

## Main Framework / Design / Rules

### Current Working Assumptions
1. The user already has discretionary crypto trading experience, including Binance, leverage, position sizing, stop losses, and risk/reward framing.
2. The primary current venue candidate is Binance USDⓈ-M futures.
3. Leverage will be used conservatively and always subordinated to hard risk controls.
4. The first live-capable system will be rules-based.
5. The initial signal horizon is likely around 10m–15m bars.
6. A future operator interface is expected but should remain separate from the engine.
7. Markdown is the canonical living documentation and AI context format.
8. The bot is expected to run on a small dedicated machine such as a NUC PC, with later UI visibility possibly on a small desk monitor.
9. AI/ML may be useful later, but not as an uncontrolled live-trading authority in early phases.
10. Spot remains a valid comparison and control path even if futures is the primary design target.

## Assumptions
- These assumptions are strong enough to guide initial structuring but should still be revisited at major phase gates.

## Risks and Failure Modes
- Treating working assumptions as immutable
- Forgetting to revise downstream docs after assumptions change
- Allowing interface ideas to reshape the engine prematurely

## Open Questions
- Final initial timeframe: 10m or 15m?
- Exact v1 symbol set?
- Which strategy family best matches the chosen timeframe and execution constraints?

## Decisions
- Assumptions should be revisited during milestone reviews.
- Any assumption with architecture impact should eventually be backed by an ADR or a dedicated design doc.

## Next Steps
- Promote confirmed assumptions into ADRs where appropriate
- Use these assumptions to guide the first strategy selection framework

## References
- `project-objective.md`
- `../adr/ADR-001-use-markdown-as-canonical-memory.md`
- `../adr/ADR-002-target-binance-usdm-futures-first.md`
