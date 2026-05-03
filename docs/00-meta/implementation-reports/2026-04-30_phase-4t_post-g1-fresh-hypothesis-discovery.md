# Phase 4t — Post-G1 Fresh-Hypothesis Discovery Memo

**Authority:** Operator authorization for Phase 4t (Phase 4s §"Operator decision menu" Option B conditional secondary alternative — docs-only fresh-hypothesis discovery memo, conditional on operator explicitly choosing to continue research after consolidation; operator has so chosen). Phase 4s (post-G1 strategy research consolidation memo); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal for G1 first-spec); Phase 4q (G1 backtest-plan methodology binding); Phase 4p (G1 strategy spec locked); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery memo; Candidate B selection); Phase 4m (post-V2 consolidation; 18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4f (external strategy research landscape memo + V2 candidates); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t §12 (validity gate); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4t — **Post-G1 Fresh-Hypothesis Discovery Memo** (docs-only). Evaluates genuinely new future research spaces under the Phase 4m 18-requirement fresh-hypothesis validity gate and the Phase 4s rejection topology, identifies rescue-risk traps, and recommends at most one candidate space (or remain-paused) for a future docs-only hypothesis-spec memo. **Phase 4t does NOT create a strategy spec, name a runnable strategy, define exact thresholds, define a backtest plan, run a backtest, run diagnostics, acquire data, modify data, modify manifests, write code, modify `src/prometheus/`, modify tests, modify scripts, authorize Phase 4u, or authorize paper / shadow / live / exchange-write.** **Phase 4t is text-only.**

**Branch:** `phase-4t/post-g1-fresh-hypothesis-discovery`. **Memo date:** 2026-05-03 UTC.

---

## Summary

Phase 4t is the project's second fresh-hypothesis discovery memo (after Phase 4n, which was the post-V2 discovery memo and led to Phase 4o → Phase 4p → Phase 4q → Phase 4r → Phase 4s — i.e., the G1 research arc that ended in Verdict C HARD REJECT). Phase 4t evaluates eight candidate spaces (A — Structural-R trend continuation revisited; B — Funding-context trend/risk filter revisited; C — Structural pullback continuation revisited; D — Volatility-contraction expansion breakout; E — Event-risk / funding-stress avoidance overlay; F — Market microstructure / liquidity-timing research; G — Cross-timeframe continuation without hard regime gate; H — No new candidate / remain paused) against the Phase 4m 18-requirement validity gate, the Phase 4s rejection topology (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism / framework mismatch; V2 design-stage incompatibility; G1 regime-gate-meets-setup intersection sparseness), the Phase 4s reusable insights, and the Phase 4s forbidden-rescue observations. **Phase 4t recommends Option A — remain paused as primary.** Five strategy-rejection events with five categorically distinct failure modes is enough evidence to question whether the project has yet assembled a research-discovery process strong enough to clear the validity gate; Phase 4t identifies no candidate that *clearly dominates* under the validity gate. **Phase 4t records Option B — conditional secondary** as a future docs-only hypothesis-spec memo on **Candidate D — Volatility-contraction expansion breakout**, on the strict condition that the operator explicitly authorizes a future Phase 4u and accepts that Candidate D's predeclaration discipline must be unusually rigorous — particularly its opportunity-rate floor and its avoidance of becoming "G1 with a one-dimension volatility-only regime gate". Candidate D is the strongest among A–G under the validity gate, but its rescue-risk distance from R1a (volatility-percentile-as-bolt-on filter to R3) and from G1 (regime-gate-meets-setup intersection sparseness) is moderate, not strong. Phase 4t does NOT authorize Phase 4u. Phase 4t does NOT create a strategy spec. Phase 4t does NOT name a runnable strategy. Phase 4t does NOT change any retained verdict or project lock.

## Authority and boundary

- **Authority granted:** create the Phase 4t docs-only discovery memo; create the Phase 4t closeout; evaluate broad strategy-family spaces against the Phase 4m validity gate and Phase 4s rejection topology; reject hidden G1 / V2 / R2 / F1 / D1-A rescues; recommend at most one candidate space for a future docs-only hypothesis-spec memo or recommend remain-paused.
- **Authority NOT granted:** create a full strategy spec (forbidden); create a new named runnable strategy (forbidden); name V3 / H2 / G2 / any successor implementation name (forbidden); create G1-prime / G1-narrow / G1-extension / G1 hybrid (forbidden); create V2-prime / V2-narrow / V2-relaxed / V2 hybrid (forbidden); create F1 / D1-A / R2 rescue (forbidden); define exact thresholds (forbidden); define a backtest plan (forbidden); run a backtest (forbidden); run diagnostics (forbidden); acquire / modify / patch / regenerate / replace data (forbidden); modify manifests (forbidden); create v003 (forbidden); modify `src/prometheus/`, tests, or existing scripts (forbidden); authorize Phase 4u or any successor phase (forbidden); authorize paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials (forbidden).
- **Hard rule:** Phase 4t is text-only. No code is written. No data is touched. No backtest is run. No new strategy candidate is named or specified beyond conceptual discussion.

## Starting state

```text
Branch (Phase 4t):   phase-4t/post-g1-fresh-hypothesis-discovery
main / origin/main:  1b2a2643540a6f3eb50fea740743528b462c8492 (unchanged)
Phase 4s merge:      7710b11425247babbd3d9044579cbeca70cf7b76 (merged)
Phase 4s housekeeping: 1b2a2643540a6f3eb50fea740743528b462c8492 (merged)
Working-tree state:  clean (no tracked modifications); only gitignored
                     transients .claude/scheduled_tasks.lock and
                     data/research/ are untracked and will not be committed.
Quality gates (verified at memo creation):
  ruff check . PASS
  pytest 785 PASS
  mypy strict 0 issues across 82 source files
```

## Why this memo exists

The project has now completed five strategy-rejection events (R2 cost-fragility, F1 catastrophic-floor, D1-A mechanism / framework mismatch, V2 design-stage incompatibility, G1 regime-gate-meets-setup intersection sparseness) and three post-rejection consolidation memos (Phase 3e for F1, Phase 3k for D1-A, Phase 4m for V2; Phase 4s adds the G1 consolidation; the post-D1-A external-cost-evidence review (Phase 3l) and post-D1-A regime-first framework memo (Phase 3m) are also in the record but are not strategy-rejection memos). After consolidation, the operator has an explicit choice: pause indefinitely, or attempt another fresh-hypothesis discovery cycle.

Phase 4t exists because the operator chose the second option for the second time. Phase 4n (post-V2) was the first such cycle and produced Candidate B Regime-First Breakout — which became G1 — which terminated at Verdict C HARD REJECT. The pattern of "predeclaration discipline → first-spec rejection" is now a real risk; Phase 4t must take that risk seriously and not produce another candidate "by default" simply because the operator authorized discovery.

Phase 4t accordingly weights *remain paused* heavily in the discovery framework. A candidate must *clearly dominate* under the validity gate; otherwise Phase 4t recommends remain paused.

## Relationship to Phase 4s

- Phase 4s recommended remain-paused as primary and Phase 4t (docs-only fresh-hypothesis discovery memo) as conditional secondary, contingent on explicit operator authorization.
- The operator has now chosen Option B; Phase 4t is authorized as docs-only.
- Phase 4t **must operate under** the Phase 4m 18-requirement fresh-hypothesis validity gate, the Phase 4s rejection topology, and the Phase 4s forbidden-rescue observations.
- **Phase 4t does NOT modify Phase 4s.** Phase 4s's verdict-preservation, rejection-topology, and forbidden-rescue observations are binding inputs, not subject to revision.
- **Phase 4t must NOT create a strategy spec, run a backtest, acquire data, or implement code.** Phase 4t recommends; the operator decides whether to authorize a future Phase 4u (hypothesis-spec memo, docs-only) or remain paused.

## Full rejection topology recap

```text
Strategy   Rejection mode                                  Mechanism evidence layer    Rescue trap
---------- ----------------------------------------------- --------------------------- -----------------------------------------
R2         cost-fragility                                  failed WITH evidence        cheaper costs / cost relaxation
F1         catastrophic-floor / bad full-population        failed WITH evidence        profitable subset mining
            expectancy
D1-A       mechanism / framework mismatch                  failed WITH evidence        funding with extra filters
V2         design-stage incompatibility                    failed BEFORE evidence       wider stops / stop-filter removal /
                                                            was generable               V2-prime
G1         regime-gate-meets-setup intersection sparseness failed BEFORE evidence       classifier relaxation / G1-prime / using
                                                            was generable               Phase 4r active-fraction numbers as
                                                                                        tuning targets
```

R2 / F1 / D1-A failed *with* mechanism evidence. V2 / G1 failed *before* mechanism evidence was generable. Five rejection modes are categorically distinct; they share only the discipline of having been predeclared and tested under §11.6 cost realism with bootstrap / DSR / PBO / CSCV correction.

## Phase 4m validity gate recap

```text
1.  Must be named as a new hypothesis (not a rescue label).
2.  Must be specified before any data is touched.
3.  Must explain why it is new in theory.
4.  Must define entry / stop / target / sizing / cost / timeframe / exit
    together (the V2 / G1 co-design lesson — see below).
5.  Must predeclare data requirements.
6.  Must predeclare mechanism checks.
7.  Must predeclare pass / fail gates including catastrophic-floor predicates.
8.  Must predeclare forbidden comparisons and forbidden rescue interpretations.
9.  Must NOT choose thresholds from prior failed outcomes.
10. Must NOT use Phase 4l V2 root-cause analysis as direct optimization
    target.  (Phase 4s extends this to: must NOT use Phase 4r G1 active-
    fraction or 124-trade baseline numbers as direct optimization target.)
11. Must preserve §11.6 cost sensitivity.
12. Must preserve project locks and governance.
13. Must commit to predeclared chronological train / validation / OOS
    holdout windows before backtest.
14. Must commit to deflated Sharpe / PBO / CSCV correction if grid search.
15. Must distinguish mechanism evidence from framework promotion.
16. Must preserve BTCUSDT-primary / ETHUSDT-comparison protocol.
17. Must NOT propose live-readiness / paper / shadow / Phase 4 canonical
    as part of first phase.
18. Must satisfy separate operator authorization.
```

**Requirement #4 reading (post-V2 + post-G1):** entry / stop / target / sizing / cost / timeframe / exit must be defined together, AND the **regime-gate / entry-rule / sample-size-viability** co-design lesson (G1) must be honored alongside the **setup-geometry / stop-filter** co-design lesson (V2). This is the Phase 4s observation, not a governance amendment; the requirement text is unchanged but the reading is enriched.

**Requirement #9 / #10 reading (post-V2 + post-G1) — explicit forbidden-input list for any future hypothesis:**

- **V2 forensic numbers** forbidden as tuning inputs: V2's 20/40-bar Donchian setup, V2's 0.60–1.80 × ATR(20) stop-distance filter, V2's 8-feature AND chain shape, V2's 512-variant grid shape, any specific V2 threshold from the Phase 4g spec, the Phase 4l observed "raw V2 candidates produce ~3–5 × ATR stops" forensic number, the Phase 4l zero-trade outcome.
- **G1 forensic numbers** forbidden as tuning inputs: G1's five-dimension AND classifier shape, G1's specific binary-axis values (E_min ∈ {0.30, 0.40}; ATR band ∈ {[20, 80], [30, 70]}; V_liq_min ∈ {0.80, 1.00}; funding band ∈ {[15, 85], [25, 75]}; K_confirm ∈ {2, 3}), the Phase 4r 2.03% active-fraction observation, the 124 always-active baseline trades, the −0.34 mean_R always-active outcome, the 0.500 PBO_cscv outcome under empty-array conditions, the all-zero DSR outcome, the zero-trade G1 population.
- **5m Q1–Q7 forensic findings** forbidden as rule candidates (Phase 3o §6 / Phase 3t §14.2 preserved verbatim).

## Phase 4s additional design-discipline observations

Phase 4s recorded ten reusable insights (recapped concisely):

1. Regime-first is theoretically valid; G1 first-spec was too narrow.
2. Active-regime fraction alone is insufficient (CFP-9 < 5% is necessary, not sufficient).
3. **Active-regime entry-rule arrival rate matters** — joint rate `(regime_active AND setup AND stop_distance_passes)` is the binding rate.
4. Always-active baselines are valuable structural negative controls.
5. Inactive-population pseudo-trades are useful but methodologically inert when active is empty.
6. HIGH-cost realism still binds even when primary failure is no-trade.
7. Zero-trade outcomes neutralize PBO / DSR / CSCV.
8. CFP-9 worked correctly.
9. CFP-1 and CFP-9 are independent drivers.
10. A good hypothesis can fail at operational geometry.

These are the design-discipline observations Phase 4t imports as binding evaluation context for every candidate.

## Discovery method

Phase 4t evaluates each candidate space against ten dimensions:

- **D1: New-theory strength** — does the candidate's core thesis exist independently of any prior rejected family, and can it be stated in first-principles terms?
- **D2: Distance from forbidden rescue** — how close is the candidate to a hidden V2-prime / G1-prime / R2-cheaper-cost / F1-subset-mining / D1-A-extra-filter? "Strong" = clearly distinct; "Moderate" = adjacent and risky; "High risk" = adjacent enough to require structural avoidance pattern; "Reject" = direct rescue.
- **D3: Opportunity-rate viability** — does the candidate intrinsically support a non-trivial opportunity-rate floor, or does it risk another G1-style sparse-intersection failure?
- **D4: Co-design clarity** — does the candidate make it natural to define entry / stop / target / sizing / cost / timeframe / exit *together* (V2 lesson) AND regime-gate / entry-rule / sample-size-viability *together* (G1 lesson)?
- **D5: Data feasibility** — does the candidate operate on data already available (v002 + Phase 4i + v002 funding) or does it require new acquisition (mark-price 30m / 4h, aggTrades, spot, cross-venue, order book)? Phase 4t cannot authorize acquisition.
- **D6: Cost-survival plausibility** — is there a first-principles reason to expect §11.6 = 8 bps HIGH cost survival? Or is the candidate's edge fragile in the same way R2 was?
- **D7: Mechanism-check designability** — can clean, predeclared M1 / M2 / M3 / M4 mechanism checks be designed for the candidate, with always-active and inactive-population baselines as appropriate?
- **D8: Governance compatibility** — does the candidate naturally honor §11.6 / §1.7.3 / Phase 3v / Phase 3w / Phase 4j §11 / Phase 4k governance, or does it pressure governance?
- **D9: Implementation complexity later** — if Phase 4u → 4v (hypothesis-spec → strategy-spec → backtest-plan → backtest-execution) ever proceeds, how complex would the standalone-script implementation be relative to Phase 4l (V2; ~3 000 lines) and Phase 4r (G1; ~3 000 lines)?
- **D10: Research value** — even if the candidate fails (which any fresh hypothesis is more likely to do than not, given the rejection record), would the rejection produce a *new* lesson that does not duplicate R2 / F1 / D1-A / V2 / G1?

Each dimension uses qualitative ratings only: **Strong / Moderate / Weak / High risk / Reject**. **No numeric optimization. No data-derived scores. No use of Phase 4r forensic values as thresholds.** The recommendation is the conjunction across dimensions; a candidate that scores "High risk" on D2 (rescue-trap distance) cannot be primary.

## Candidate pool considered

Phase 4t evaluates eight candidates. A through G are research candidates; H is the explicit "no new candidate / remain paused" outcome treated as a real candidate with its own dimensions.

## Candidate A — Structural-R trend continuation revisited

**Origin:** Phase 4n Candidate A. Carried forward by name; not modified by G1's outcome.

**Core thesis:** trend continuation in BTCUSDT perpetual futures may be tradable on a structurally-derived R-multiple basis (e.g., entry on confirmed continuation; structural stop derived from the consolidation that precedes the entry; target as a multiple of the structural R), without inheriting V1's specific 8-bar setup or V2's 20/40-bar Donchian-plus-AND-chain shape.

**Rescue-risk profile:**

- Phase 4n labeled the rescue trap "V2 but with a wider stop filter".
- After G1, the trap analysis is *unchanged*: V2 failed at setup-geometry / stop-filter incompatibility; Candidate A's natural avoidance is to redesign setup geometry and stop-filter together from first principles, *not* to widen V2's stop-distance bound.
- **Critical:** Candidate A must NOT use Phase 4l V2 forensic numbers (the "3–5 × ATR" observation; the locked Phase 4g 0.60–1.80 × ATR bound) as tuning inputs.
- Candidate A is not a G1-prime concern; it does not propose a regime gate.

**Risk note:** The fact that *G1 also failed* — even after explicitly avoiding V2's stop-filter trap — should make Candidate A more cautious, not less. R1a / R1b-narrow are retained-but-non-leading; Candidate A risks becoming *another* incremental variation on V1 / R3 with subtle redesign.

## Candidate B — Funding-context trend/risk filter revisited

**Origin:** Phase 4n Candidate C. Reframed (not directional trigger; risk-context only).

**Core thesis:** funding rate, funding history percentile, and funding-stress windows may carry information about *risk regimes* (when to be smaller; when to avoid entries; when to widen time-stops), without becoming a directional trigger as D1-A used.

**Rescue-risk profile:**

- Phase 4n labeled the rescue trap "D1-A but with extra filters / D1-A-prime".
- Funding-as-direction (D1-A) is HARD REJECT under MECHANISM PASS / FRAMEWORK FAIL.
- Candidate B's avoidance pattern: funding is a *risk-context* signal that modulates sizing or activation, NEVER produces a directional entry by itself.
- **Critical question:** is funding-as-risk-context strong enough as a *strategy hypothesis*, or is it merely a risk overlay on top of a separate directional thesis? If the latter, Candidate B is not a strategy candidate; it is a risk module.

**Risk note:** A funding-as-risk-context overlay on top of Candidate A or Candidate D risks compound complexity; strapping risk-overlays onto an unproven directional thesis is exactly the kind of "more conditions = better" pattern that G1 demonstrated to be unsafe.

## Candidate C — Structural pullback continuation revisited

**Origin:** Phase 4n Candidate D. Carried forward by name; not modified by G1's outcome.

**Core thesis:** pullback-after-trend-confirmation entries (rather than breakout-on-continuation) may carry different cost profiles and different sample sizes than R2's specific pullback-retest entry.

**Rescue-risk profile:**

- Phase 4n labeled the rescue trap "R2 but with lower assumed costs".
- Cost-relaxation rescue is forbidden by Phase 4m and Phase 4s.
- Candidate C must preserve §11.6 = 8 bps HIGH per side.
- The candidate's burden is to demonstrate a *materially new pullback thesis* — not "R2 except cheaper" — under HIGH cost.

**Risk note:** Pullback-continuation under HIGH cost realism is a long-running cost-sensitivity research question; R2 already explored this and failed at §11.6. Candidate C's distance from R2-rescue is moderate at best.

## Candidate D — Volatility-contraction expansion breakout

**Origin:** New candidate space introduced by Phase 4t.

**Core thesis:** markets alternate between volatility *contraction* (low ATR-percentile, compressed range) and volatility *expansion* (high ATR-percentile, range expansion). A breakout from a confirmed contraction phase may be more meaningful than a breakout in a "broad regime" sense, because contraction-to-expansion is a localized state transition that occurs more frequently than a five-dimension AND classifier (G1) and is more selective than a per-bar ATR-percentile filter (R1a). The thesis is that *the contraction-state precondition itself* — measured locally and recently — is a sufficient regime context, replacing G1's heavy AND-classifier with a single contraction-expansion state.

**Distinction from G1:** No top-level hard regime gate that suppresses signal evaluation for most bars. Contraction-state is a *precondition for the setup* (similar to a Donchian-width compression check), not a multi-dimension AND classifier. The setup itself fires only when contraction transitions to expansion *with* directional confirmation; the candidate's design intent is that the joint event (contraction-state AND breakout) should occur at a non-trivial rate.

**Distinction from R1a:** R1a was a volatility-percentile bolt-on filter applied per-bar to R3's existing setup. Candidate D is structurally different: contraction is a *precondition*, not a filter; the breakout-rule is redesigned to depend on the contraction-to-expansion transition, not bolted onto an existing R3-style breakout.

**Rescue-risk profile:**

- Closest forbidden trap: G1 with a one-dimension volatility-only regime gate. Avoidance pattern: the candidate must NOT use a top-level state machine that gates entry evaluation across most bars; the contraction-state must be a *local* precondition with high frequency, and the entry rule must be designed to fire on the transition itself, not despite the state.
- Second closest trap: R1a-rescue. Avoidance: contraction is a setup component, not a per-bar filter on a different setup.
- Third closest trap: V2-prime. Avoidance: the candidate's setup geometry must be designed from first principles for contraction-to-expansion transition; it must NOT inherit V2's 20/40-bar Donchian setup or V2's stop-distance filter.

**Risk note:** Candidate D is the strongest among the new spaces but its "Moderate" rescue-risk distance from G1 is real. A future Phase 4u memo, if ever authorized, would have to rigorously design out the G1-like AND-classifier shape and predeclare an opportunity-rate floor.

## Candidate E — Event-risk / funding-stress avoidance overlay

**Origin:** New candidate space introduced by Phase 4t.

**Core thesis:** rather than using funding as a directional trigger (D1-A) or as a regime band (G1), use funding-stress avoidance to *downweight or block* entries during identified stress windows (extreme funding values; known event days). The candidate is an *avoidance overlay*, not a primary signal.

**Rescue-risk profile:**

- Phase 4t observation: Candidate E is structurally similar to D1-A in its use of funding signals; its avoidance pattern is to be exclusively a *risk overlay* (block / size-down), never a directional trigger.
- Critical question: is Candidate E a *strategy hypothesis* or *just a risk module*? If the latter, it is not a strategy candidate; it cannot be the primary recommendation; it could only ever be a sub-component of a separate primary hypothesis.

**Phase 4t evaluation:** Candidate E is most likely a risk overlay, not a strategy hypothesis. Phase 4t does NOT recommend Candidate E as a primary candidate.

## Candidate F — Market microstructure / liquidity-timing research

**Origin:** New candidate space introduced by Phase 4t.

**Core thesis:** entry-execution quality may depend on intra-bar liquidity state, spread, taker imbalance, and execution-window selection. A candidate could explore whether entry timing within the next-bar-open window improves R-multiples after costs.

**Rescue-risk profile:**

- Direct rescue traps: not applicable; the candidate is structurally orthogonal to R2 / F1 / D1-A / V2 / G1.
- New rescue trap: "if I had finer-resolution data, the strategy would work" — i.e., the temptation to acquire mark-price 30m / 4h / aggTrades / order-book snapshots / spot data to evaluate microstructure. **Phase 4t does NOT authorize acquisition.**

**Data feasibility:** Likely **unavailable-data dependent**. Order-book / aggTrades / spread data is not currently acquired. Phase 4i did NOT acquire aggTrades by Phase 4h §7.E (deferred). Mark-price 30m / 4h is not acquired. Spot data is not acquired. Phase 4t cannot authorize acquisition.

**Phase 4t evaluation:** Candidate F is **rejected** at this boundary because it would require new data acquisition before any evaluation, and Phase 4t cannot authorize acquisition. It is recorded as a *future* possibility only if a separately authorized data-requirements memo proves feasibility on existing data.

## Candidate G — Cross-timeframe continuation without hard regime gate

**Origin:** New candidate space introduced by Phase 4t.

**Core thesis:** use HTF context (4h or 1h trend / volatility / structure) to *shape* entry geometry — specifically, the structural stop, the target, and the sizing — *without* using the HTF context as a hard regime gate that suppresses signal evaluation. The candidate's design intent is that HTF context modulates *trade quality* without filtering trade *opportunity*.

**Distinction from G1:** No top-level state machine suppressing entry evaluation. HTF context shapes the entry's stop / target / sizing, not its existence.

**Distinction from R1a / R1b-narrow:** Not a per-bar bolt-on filter to R3's existing setup. The entry rule is redesigned to read HTF context as a parameter (e.g., HTF-volatility-scaled stop distance; HTF-trend-scaled target multiplier), not to gate on an HTF condition.

**Rescue-risk profile:**

- Closest forbidden trap: G1 with HTF context demoted from "gate" to "input" but otherwise similar. Avoidance pattern: the candidate must NOT use the same five-dimension AND classifier shape; HTF inputs must enter the entry rule as continuous shaping parameters, not boolean gates.
- Second closest trap: R1a / R1b-narrow per-bar filter pattern. Avoidance: HTF context shapes entry parameters, does not filter setup arrival.
- Third closest trap: D1-A directional rule. Avoidance: HTF inputs do not produce direction; direction comes from the entry rule, HTF inputs shape stop / target / sizing only.

**Risk note:** Candidate G is conceptually attractive and structurally distinct from G1, but the same risk applies: predeclaring exact "shaping" rules without G1-style AND-classifier shapes is delicate. The candidate's burden is to predeclare opportunity-rate viability *before* HTF shaping is added.

## Candidate H — No new candidate / remain paused

**Origin:** explicit "remain paused" outcome treated as a real candidate.

**Core thesis:** five strategy-rejection events (R2 / F1 / D1-A / V2 / G1), three post-rejection consolidation memos, and one fresh-hypothesis discovery cycle that itself produced a new rejection event (Phase 4n → G1) is enough evidence to question whether the project has yet assembled a research-discovery process strong enough to clear the validity gate. The conservative posture is to *pause indefinitely* until either (a) a genuinely new theoretical insight emerges (not derivable from Phase 4f / 4n's candidate space), (b) external evidence shifts the cost / data assumptions (e.g., a new Phase 3l-style cost-evidence review with stronger evidence than "B — conservative but defensible"), or (c) the project's research-discovery process itself improves (e.g., a methodology-level memo that strengthens the validity gate or adds an opportunity-rate-viability gate as a binding pre-spec requirement).

**Phase 4t evaluation:** Candidate H is a serious option. It is the *primary* recommendation under "candidate must clearly dominate or pause". Among A–G, no candidate dominates clearly enough to displace H.

## Rejected / forbidden spaces

Phase 4t explicitly rejects (NOT subject to consideration as candidates):

- **G1-prime / G1-narrow / G1-extension / G1 hybrid** — any G1 rescue (Phase 4s forbidden-rescue list).
- **V2-prime / V2-narrow / V2-relaxed / V2 hybrid** — any V2 rescue (Phase 4m forbidden-rescue list).
- **R2 cheaper-cost rescue** — §11.6 cost-relaxation forbidden (Phase 4m).
- **F1 profitable-subset rescue** — Phase 3c §7.3 catastrophic-floor predicate.
- **D1-A extra-filter rescue** — Phase 3k forbidden.
- **Always-active G1 promotion** — the always-active baseline produced mean_R = −0.34 under HIGH cost; not viable.
- **Immediate 5m strategy** — Phase 3o §6 / Phase 3t §14.2 closure preserved.
- **Mean-reversion immediate revival** — F1 HARD REJECT preserved.
- **ML-first black-box forecasting** — project remains rules-based per §1.7.3.
- **Market-making / HFT** — not transferable to Prometheus substrate.
- **Paper / shadow / live** — Phase 4 canonical preconditions not met.
- **Phase 4 canonical** — preconditions not met.
- **Any data acquisition as the next step** — Phase 4t does not authorize acquisition.
- **Any immediate backtest** — data-snooping risk per Bailey / Borwein / López de Prado / Zhu 2014.

## Candidate scoring matrix

Qualitative ratings only. **Strong / Moderate / Weak / High risk / Reject.** No numeric optimization. No data-derived scores. No Phase 4r forensic values used.

```text
Dimension                                   A          B          C          D          E          F          G          H
------------------------------------------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------
D1: New-theory strength                     Moderate   Moderate   Weak       Strong     Weak       Moderate   Moderate   n/a
D2: Distance from forbidden rescue          Moderate   Moderate   Weak       Moderate   Weak       Strong     Moderate   n/a
D3: Opportunity-rate viability              Moderate   Moderate   Moderate   Strong     n/a (overlay) Moderate Moderate   n/a
D4: Co-design clarity (V2+G1 lessons)       Moderate   Moderate   Moderate   Strong     Weak       Moderate   Moderate   n/a
D5: Data feasibility (existing only)        Strong     Strong     Strong     Strong     Strong     Reject     Strong     Strong
D6: Cost-survival plausibility (§11.6)      Moderate   Moderate   Weak       Moderate   n/a (overlay) Moderate Moderate   Strong (n/a)
D7: Mechanism-check designability           Strong     Moderate   Strong     Strong     Weak       Moderate   Moderate   n/a
D8: Governance compatibility                Strong     Strong     Strong     Strong     Strong     Reject     Strong     Strong
D9: Implementation complexity later         Moderate   Moderate   Moderate   Moderate   Weak       High risk  Moderate   n/a
D10: Research value                         Moderate   Moderate   Weak       Strong     Weak       Moderate   Moderate   Strong
Recommendation                              not now    not now    not now    conditional not now    rejected   not now    primary
                                                                              secondary  (overlay)  at this              (Option A)
                                                                              (Option B)            boundary
```

**Reading the matrix:**

- **Candidate D — Volatility-contraction expansion breakout** is the strongest among A–G, scoring "Strong" on six dimensions (D1, D3, D4, D5, D7, D8, D10) and "Moderate" on four (D2, D6, D9). Its critical risk is D2 (Moderate distance from G1-rescue / R1a-rescue / V2-prime); avoidance requires rigorous design discipline.
- **Candidate F — Market microstructure** is **rejected** at this boundary because D5 (data feasibility) is "Reject" — Phase 4t cannot authorize acquisition, and Candidate F requires unavailable data.
- **Candidate E — Event-risk / funding-stress avoidance overlay** is **rejected as a primary candidate** because it is most plausibly a risk overlay, not a strategy hypothesis (D1, D3, D4, D6, D7 weak / n/a).
- **Candidates A / B / C / G** score "Moderate" across most dimensions; none clearly dominates. A and C carry V2 / R2 rescue risk that is not novel after V2 / G1; B is most useful as a risk overlay rather than a primary candidate; G is closer to a generalization of "use HTF context without G1-style gating" than a sharp first-principles thesis.
- **Candidate H — Remain paused** is the **primary recommendation** because no candidate clearly dominates the validity gate.

## Rescue-risk analysis

**Candidate A — Structural-R trend continuation revisited.** Nearest trap: *V2 with wider stop filter*. Why dangerous: V2 failed at setup-geometry / stop-filter incompatibility; Candidate A's natural temptation is to widen the stop filter or remove it. Avoidance: redesign setup-geometry and stop-filter together from first principles; do NOT use V2's specific 20/40-bar Donchian shape; do NOT use V2's 0.60–1.80 × ATR bound; do NOT use Phase 4l forensic numbers. Avoidance credibility: Moderate — the discipline is well-known after Phase 4m, but avoiding hidden importation of V1-derived mental templates is hard.

**Candidate B — Funding-context trend/risk filter revisited.** Nearest trap: *D1-A with extra filters / D1-A-prime*. Why dangerous: D1-A failed at MECHANISM PASS / FRAMEWORK FAIL; using funding for direction is a known dead end. Avoidance: funding is a *risk-context* signal only (block / size-down), never a directional trigger. Avoidance credibility: Strong (the discipline is sharp), but the strategic value of an avoidance overlay is weak as a *primary* candidate.

**Candidate C — Structural pullback continuation revisited.** Nearest trap: *R2 with cheaper costs*. Why dangerous: R2 FAILED — §11.6; the temptation to argue "but realistic costs are lower" is forbidden by Phase 4m. Avoidance: preserve §11.6 = 8 bps HIGH per side; demonstrate a materially new pullback thesis. Avoidance credibility: Weak — most plausible pullback theses on BTCUSDT 15m / 30m have been explored in some form; demonstrating "materially new" is a high bar.

**Candidate D — Volatility-contraction expansion breakout.** Nearest trap: *G1 with a one-dimension volatility-only regime gate*. Why dangerous: G1 failed at regime-gate-meets-setup intersection sparseness; reducing G1's five-dimension AND classifier to one volatility dimension might *seem* to fix it but would be the same failure mode at a different point on the AND chain. Avoidance: the contraction-state must be a *local* precondition with high frequency; the entry rule must be designed to fire on the *transition* itself; opportunity-rate viability must be predeclared *before* data is touched, derived from first principles, not from Phase 4r's 2.03% forensic number. Avoidance credibility: Moderate — the discipline is sharp but the operational failure mode for Candidate D is structurally adjacent to G1's. Second-nearest trap: R1a rescue (volatility percentile as bolt-on filter to R3). Avoidance: contraction is a setup component, not a filter; the entry rule is redesigned, not augmented. Third-nearest trap: V2-prime. Avoidance: setup geometry is designed from first principles for contraction-to-expansion transition; do NOT inherit V2's 20/40-bar Donchian or V2's stop-distance filter.

**Candidate E — Event-risk / funding-stress avoidance overlay.** Not a primary candidate. As a sub-component of a future hypothesis, the rescue trap is *D1-A as overlay rather than directional rule*. Avoidance: stays purely as block / size-down; never produces direction; never selects entries.

**Candidate F — Market microstructure / liquidity-timing research.** Rejected at this boundary because of D5 (data feasibility = Reject). Distinct rescue trap: "if I had finer-resolution data, the strategy would work" — temptation to authorize acquisition. Avoidance: Phase 4t does NOT authorize acquisition.

**Candidate G — Cross-timeframe continuation without hard regime gate.** Nearest trap: *G1 with HTF demoted from gate to input but otherwise similar*. Why dangerous: G1 failed because the AND-classifier shape was too narrow; if Candidate G uses HTF as a continuous-valued input but ends up with an effective AND-gate (multiple HTF inputs that must all be in some range), it is structurally G1. Avoidance: HTF inputs enter the entry rule as continuous shaping parameters (modulating stop distance / target multiplier / position size), NOT as boolean gates. Avoidance credibility: Moderate — predeclaring continuous shaping rules without sliding into AND-gates is delicate.

**Candidate H — Remain paused.** Why this may be the strongest governance option after five rejection events: predeclaration discipline has worked (Phases 4f → 4l for V2; Phases 4n → 4r for G1) — every rejection was clean and no governance leakage occurred — but each new fresh-hypothesis cycle has produced another rejection. The marginal value of another cycle is unclear; the marginal cost (operator time; cumulative project drift; risk that yet another rejection erodes the discipline of pausing) is real. Remaining paused is *not* a defeat; it is a deliberate posture that preserves the possibility of a genuinely new theoretical insight without the predeclaration → rejection pattern repeating mechanically.

## Opportunity-rate viability analysis

After G1, every candidate must include an explicit opportunity-rate viability story. Phase 4t restates this requirement for each candidate (these are *observations* about future hypothesis-spec design discipline; they are NOT adopted thresholds and they MUST NOT be derived from Phase 4r forensic numbers).

**Candidate A — Structural-R trend continuation revisited.** Likely opportunity-rate bottleneck: the structural-R derivation (entry / stop / target derived from a consolidation pattern). A future hypothesis-spec memo would predeclare a *minimum candidate arrival rate* before any backtest. Opportunity-rate floor must be intrinsic (derived from the pattern's expected frequency on BTCUSDT 30m / 1h klines) — not a post-G1 patch derived from Phase 4r's 2.03%. Negative control: an always-active baseline run on the same setup geometry, to confirm the entry-rule fires at non-trivial rate.

**Candidate B — Funding-context trend/risk filter revisited.** As a primary strategy candidate: opportunity-rate floor is determined by the underlying directional thesis B sits on top of. As an overlay-only: opportunity-rate is unbounded by B itself but is bounded by the primary thesis. Phase 4t observation: B is most plausibly an overlay; its opportunity-rate viability question is "does the overlay reduce trade count below a viable floor?", which is a different question from a primary candidate.

**Candidate C — Structural pullback continuation revisited.** Likely opportunity-rate bottleneck: pullback patterns have lower arrival rates than breakout patterns on most timeframes. A future hypothesis-spec memo must predeclare a minimum pullback-arrival rate before any backtest. Risk: pullback-arrival rate × HIGH-cost survival threshold is a tight combination on BTCUSDT 15m / 30m.

**Candidate D — Volatility-contraction expansion breakout.** Likely opportunity-rate bottleneck: contraction-to-expansion transitions arrive at moderate frequency (more frequent than five-dimension AND classifier; less frequent than per-bar setups). A future hypothesis-spec memo must predeclare a minimum transition-detection rate AND a minimum joint (transition AND setup AND stop_distance_passes) rate. The opportunity-rate floor must be derived from the contraction-state's expected duration and transition frequency on BTCUSDT 30m, *not* from Phase 4r's 2.03% number. Negative control: always-active breakout baseline on the same setup geometry, to confirm rate before contraction-state filter.

**Candidate E — Event-risk / funding-stress avoidance overlay.** As an overlay: opportunity-rate is bounded by the primary thesis; the overlay's design discipline is to ensure block-rate is small enough to leave a non-trivial residual trade population.

**Candidate F — Market microstructure / liquidity-timing research.** Rejected at this boundary; opportunity-rate analysis deferred.

**Candidate G — Cross-timeframe continuation without hard regime gate.** Likely opportunity-rate bottleneck: HTF-context-shaped parameters (continuous) do not filter trade opportunities; the opportunity-rate is determined by the entry rule itself. The G-design discipline is to ensure HTF inputs enter as continuous shaping parameters, not as filtering AND-gates.

**Candidate H — Remain paused.** Not applicable.

## Data-readiness implications

```text
Candidate   Data classification
----------- ----------------------------------------------------------------------
A           existing-data feasible (v002 + Phase 4i klines + v002 funding)
B           existing-data feasible (v002 funding only; no metrics OI by default)
C           existing-data feasible (v002 + Phase 4i klines + v002 funding)
D           existing-data feasible (Phase 4i 30m / 4h klines for ATR-percentile;
            v002 1h-derived for HTF context; v002 funding optional as sizing
            modulator only)
E           existing-data feasible as overlay (v002 funding); rejected as primary
F           UNAVAILABLE-DATA DEPENDENT
            (would require aggTrades, mark-price, spread, order book, or spot
             data — none of which Phase 4t can authorize)
G           existing-data feasible (Phase 4i 30m / 4h klines; v002 1h-derived;
            v002 funding optional as shaping input)
H           n/a
```

**No candidate among A–G except F requires new acquisition.** This is a deliberate Phase 4t outcome: any candidate that requires acquisition is automatically deprioritized at this boundary because Phase 4t cannot authorize acquisition. F is rejected at this boundary.

**Phase 4j §11 metrics OI-subset partial-eligibility rule** is preserved but should NOT be used by any future hypothesis on Phase 4t's recommended path (Candidate D). The metrics OI subset is a Phase 4i artefact tied to the V2 thesis; using it for a regime-flavored Candidate D would risk hidden V2-rescue.

## Cost-sensitivity implications

§11.6 = 8 bps HIGH per side preserved verbatim. After G1, the cost record now includes:

- R2 FAILED — §11.6 (Phase 2w).
- Always-active baseline on G1's setup at HIGH cost = mean_R −0.34 (Phase 4r forensic).
- Phase 3l "B — conservative but defensible" cost-model assessment.

For Candidates A–G, the cost-survival burden under §11.6 is unchanged: any future hypothesis must demonstrate HIGH-cost survival; no cost-model relaxation is authorized.

## Mechanism-check designability

For each candidate, Phase 4t notes high-level mechanism-check shapes only (no exact thresholds; no exact bootstrap iteration counts; no exact pass/fail R values).

**Candidate A — Structural-R trend continuation revisited.** M1 active-vs-inactive (if any state filter is added), M2 candidate-vs-always-active baseline (always-active = same setup without any Phase 4t-introduced refinement), M3 BTC OOS HIGH primary expectancy + minimum trade count, M4 ETH cross-symbol consistency.

**Candidate B — Funding-context trend/risk filter revisited (overlay framing).** M1 with-overlay-vs-without-overlay, M2 against the underlying directional thesis baseline, M3 BTC OOS HIGH primary expectancy + minimum trade count post-overlay, M4 ETH consistency.

**Candidate C — Structural pullback continuation revisited.** M1 against R3 baseline (pullback-vs-breakout on same instrument), M2 against always-active baseline (same setup at all bars), M3 BTC OOS HIGH primary expectancy + minimum trade count, M4 ETH consistency.

**Candidate D — Volatility-contraction expansion breakout.** M1 contraction-state-vs-expansion-state baseline (does the contraction-state precondition add positive expectancy over its complement?), M2 candidate-vs-always-active breakout baseline (does the contraction-state add value over no-precondition?), M3 BTC OOS HIGH primary expectancy + minimum trade count + opportunity-rate floor predeclared, M4 ETH consistency. **Also required:** an explicit "intersection rate" diagnostic similar to G1's CFP-9 — predeclared *before* any data is touched — to detect a G1-style sparse-intersection failure early.

**Candidate E — Event-risk / funding-stress avoidance overlay.** As overlay: M1 with-overlay-vs-without-overlay on the underlying thesis; M2 against always-active baseline; opportunity-rate floor must measure residual trade count post-overlay.

**Candidate F — Market microstructure / liquidity-timing research.** Rejected at this boundary; mechanism-check design deferred.

**Candidate G — Cross-timeframe continuation without hard regime gate.** M1 HTF-shaped-vs-fixed-parameter baseline (does HTF shaping add positive expectancy over fixed parameters?), M2 against always-active baseline, M3 BTC OOS HIGH primary expectancy + minimum trade count (HTF shaping should NOT reduce trade count materially), M4 ETH consistency.

**BTCUSDT-primary / ETHUSDT-comparison protocol preserved for all candidates.** ETH cannot rescue BTC.

## Governance and forbidden-input implications

All Phase 4t candidates must honor:

- §11.6 = 8 bps HIGH per side preserved verbatim.
- §1.7.3 0.25% risk / 2× leverage / one-position max preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance preserved.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 4j §11 metrics OI-subset partial-eligibility binding rule preserved (Phase 4t recommends NOT using it for any candidate on the recommended path).
- Phase 4k V2 backtest-plan methodology preserved as governance template (any future Phase 4u → 4v → 4w hypothesis-spec → backtest-plan → backtest-execution arc would mirror this template's discipline, not its specific V2 / G1 numeric thresholds).
- Phase 4m 18-requirement fresh-hypothesis validity gate preserved.
- Phase 4s forbidden-rescue observations preserved.

Forbidden input list (binding for any Phase 4u → 4v → 4w arc on the recommended path):

- mark-price 30m / 4h, mark-price 5m, mark-price 15m;
- aggTrades;
- spot data;
- cross-venue data;
- Phase 4i metrics OI subset (preserved governance; not used by recommended candidate);
- optional metrics ratio columns (Phase 4j §11.3 forbidden);
- v003;
- modified Phase 4i / v002 / v001-of-5m manifests;
- authenticated REST / private endpoints / public endpoints in code / user stream / WebSocket / listenKey lifecycle;
- 5m Q1–Q7 diagnostic outputs as features or regime indicators;
- V2 Phase 4l observed stop-distance failure numbers;
- G1 Phase 4r active-fraction / 124-trade / −0.34 mean_R numbers as tuning targets;
- credentials / `.env`.

## Final discovery recommendation

**Primary recommendation: Option A — remain paused.**

Rationale:

1. The project has now completed five strategy-rejection events (R2 / F1 / D1-A / V2 / G1) and one fresh-hypothesis discovery cycle (Phase 4n) that itself produced a rejected hypothesis. The pattern of "predeclaration discipline → first-spec rejection" is a real and growing risk; immediately authorizing another fresh-hypothesis discovery → spec → backtest cycle continues the pattern mechanically.
2. No candidate among A–G *clearly dominates* under the Phase 4m 18-requirement validity gate. Candidate D is the strongest, but its rescue-risk distance from G1 / R1a / V2-prime is "Moderate", not "Strong".
3. The conservative posture preserved by remaining paused is not a defeat. It allows time for genuinely new theoretical insight to emerge, for external evidence to shift cost / data assumptions (Phase 3l-style review), or for the project's research-discovery process itself to improve (e.g., a methodology-level memo strengthening the validity gate with an opportunity-rate-viability gate as a binding pre-spec requirement).
4. Phase 4 canonical preconditions are not met under any candidate; remain-paused does not obstruct any work that is currently authorized.

**Conditional secondary: Option B — authorize Phase 4u — Volatility-Contraction Expansion Breakout Hypothesis Spec Memo (docs-only) on Candidate D**, only if the operator explicitly chooses to continue research now. Acceptable shape if chosen:

- Phase 4u memo MUST follow the Phase 4o → Phase 4p → Phase 4q → Phase 4r template's *discipline*, not its V2 / G1 numeric thresholds.
- Phase 4u memo MUST predeclare an explicit **opportunity-rate viability story** before any data is touched (intrinsic to Candidate D's contraction-to-expansion theory; not derived from Phase 4r forensic numbers).
- Phase 4u memo MUST design Candidate D's contraction-state as a *local precondition with high frequency*, NOT as a top-level state machine that gates entry evaluation.
- Phase 4u memo MUST design the entry rule to fire on the *transition* itself, not despite the state.
- Phase 4u memo MUST explicitly forbid: G1-style five-dimension AND classifier; R1a-style per-bar volatility-percentile bolt-on filter; V2's 20/40-bar Donchian setup or 0.60–1.80 × ATR stop-distance bound; D1-A-style funding-Z-score directional rule; F1-style mean-reversion logic; R2-style pullback-retest entry; cost-model relaxation; mark-price / aggTrades / spot / cross-venue / metrics OI / 5m diagnostic outputs as features.
- Phase 4u memo MUST be docs-only; MUST NOT acquire data; MUST NOT define exact thresholds beyond the Phase 4u layer (the threshold grid layer would be Phase 4v if ever authorized); MUST NOT name a runnable strategy beyond the conceptual name.
- **Phase 4t does NOT authorize Phase 4u.** Phase 4u execution requires a separate explicit operator authorization brief.
- The conditional-secondary path is *acceptable* but not *recommended over remain-paused*. The operator should choose remain-paused unless there is an additional reason to proceed (e.g., a specific theoretical insight not derivable from the Phase 4n / Phase 4t candidate space).

NOT recommended (any option):

- G1 rescue — REJECTED.
- V2 / F1 / D1-A / R2 rescue — REJECTED.
- Immediate hypothesis-spec memo on Candidates A / B / C / E / G — NOT recommended at this boundary; none clearly dominates D.
- Candidate F — REJECTED at this boundary (data unavailable).
- Immediate backtest of any kind — REJECTED.
- Data acquisition of any kind — NOT authorized.
- Paper / shadow / live-readiness — FORBIDDEN.
- Phase 4 canonical — FORBIDDEN.
- Production-key creation / authenticated APIs / private endpoints / user stream / WebSocket — FORBIDDEN.
- MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN.
- Exchange-write capability — FORBIDDEN.

## What this does not authorize

Phase 4t does NOT authorize:

- creation of a strategy spec;
- creation of V3 / H2 / G2 / any runnable candidate name;
- creation of G1-prime / G1-narrow / G1-extension / G1 hybrid;
- creation of V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- creation of F1 / D1-A / R2 rescue;
- definition of exact thresholds for any candidate;
- definition of a backtest plan;
- a backtest run;
- diagnostics rerun;
- data acquisition of any kind;
- modification of `data/raw/`, `data/normalized/`, or `data/manifests/`;
- creation of new manifests or v003;
- modification of `src/prometheus/`, tests, or existing scripts;
- start of Phase 4u or any successor phase;
- paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- start of Phase 4 canonical;
- amendment of any project lock (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- amendment of any governance rule (Phase 3r / 3v / 3w / 4j §11 / 4k);
- amendment of any retained verdict (R3 / R2 / R1a / R1b-narrow / F1 / D1-A / V2 / G1 / H0).

## Forbidden-work confirmation

Phase 4t did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- run `scripts/phase4r_g1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create any new strategy candidate beyond conceptual discussion;
- name a runnable strategy;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4u / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : HARD REJECT (Phase 4r — Verdict C; CFP-1 critical
                       binding driver; CFP-9 independent driver;
                       terminal for G1 first-spec)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price stops
                      (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s
                            : all preserved verbatim
Phase 4t                    : Post-G1 fresh-hypothesis discovery memo
                              (this phase; new; docs-only)
Recommended state           : paused (Option A primary)
Conditional secondary       : Phase 4u Volatility-Contraction Expansion
                              Breakout Hypothesis Spec Memo (docs-only) on
                              Candidate D, only if separately authorized.
```

## Operator decision menu

- **Option A — primary recommendation:** remain paused.
- **Option B — conditional secondary:** authorize Phase 4u (Volatility-Contraction Expansion Breakout Hypothesis Spec Memo, docs-only, on Candidate D). Acceptable only if the operator explicitly chooses to continue research now and accepts the elevated discipline burden (predeclared opportunity-rate viability story; explicit anti-G1-AND-classifier design pattern; explicit avoidance of R1a / V2-prime / D1-A / F1 / R2 rescue traps; preserved §11.6 cost realism; preserved §1.7.3 locks; docs-only).

NOT recommended:

- any G1 / V2 / F1 / D1-A / R2 rescue — REJECTED.
- immediate hypothesis-spec on Candidates A / B / C / E / G — NOT recommended at this boundary.
- Candidate F (microstructure) — REJECTED at this boundary (data unavailable).
- immediate G1 / V2 / R2 / F1 / D1-A rerun — REJECTED.
- immediate backtest — REJECTED.
- data acquisition — NOT authorized.
- paper / shadow / live-readiness — FORBIDDEN.
- Phase 4 canonical — FORBIDDEN.
- production-key creation / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN.
- exchange-write capability — FORBIDDEN.

**Phase 4u is NOT authorized by this Phase 4t memo.** Phase 4u execution would require a separate explicit operator authorization brief.

## Next authorization status

```text
Phase 4u                       : NOT authorized
Phase 4 (canonical)            : NOT authorized
Paper / shadow                 : NOT authorized
Live-readiness                 : NOT authorized
Deployment                     : NOT authorized
Production-key creation        : NOT authorized
Authenticated REST             : NOT authorized
Private endpoints              : NOT authorized
User stream / WebSocket        : NOT authorized
Exchange-write capability      : NOT authorized
MCP / Graphify                 : NOT authorized
.mcp.json / credentials        : NOT authorized
G1 implementation              : NOT authorized
G1-prime / G1-extension axes   : NOT authorized; not proposed
G1-narrow / G1 hybrid          : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
Candidate F (microstructure)   : NOT authorized; data unavailable;
                                  rejected at this boundary.
Candidate D (volatility-       : Phase 4t conditional secondary; Phase 4u
contraction expansion             docs-only memo NOT authorized;
breakout)                         requires separate explicit operator
                                  authorization.
Candidates A / B / C / E / G   : NOT authorized; not recommended at this
                                  boundary.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4u (Candidate D hypothesis-spec memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4t discovery boundary.

---

**Phase 4t is docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state remains paused (Option A primary). No next phase authorized.**
