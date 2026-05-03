# Phase 4t Closeout

## Summary

Phase 4t authored the project's second fresh-hypothesis discovery memo (after Phase 4n, which led to G1's eventual Verdict C HARD REJECT). Phase 4t evaluated eight candidate spaces (A — Structural-R trend continuation revisited; B — Funding-context trend/risk filter revisited; C — Structural pullback continuation revisited; D — Volatility-contraction expansion breakout; E — Event-risk / funding-stress avoidance overlay; F — Market microstructure / liquidity-timing research; G — Cross-timeframe continuation without hard regime gate; H — No new candidate / remain paused) against the Phase 4m 18-requirement validity gate, the Phase 4s rejection topology (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism / framework mismatch; V2 design-stage incompatibility; G1 regime-gate-meets-setup intersection sparseness), and the Phase 4s reusable insights and forbidden-rescue observations. Phase 4t recommends **Option A — remain paused as primary** because no candidate among A–G clearly dominates the validity gate. Phase 4t records **Option B — conditional secondary** as a future docs-only Phase 4u Volatility-Contraction Expansion Breakout Hypothesis Spec Memo on Candidate D, only if separately authorized and only with elevated discipline (predeclared opportunity-rate viability; explicit anti-G1-AND-classifier design; explicit avoidance of R1a / V2-prime / D1-A / F1 / R2 traps; preserved §11.6 / §1.7.3). Phase 4t was docs-only; no source code, tests, scripts, data, or manifests modified.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4t_post-g1-fresh-hypothesis-discovery.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4t_closeout.md                              (new — this file)
```

No other files modified by Phase 4t.

## Discovery conclusion

After five strategy-rejection events (R2 / F1 / D1-A / V2 / G1) and one prior fresh-hypothesis discovery cycle (Phase 4n) that itself produced a rejected hypothesis (G1), the most disciplined posture is to *pause* unless a candidate clearly dominates the validity gate. **No candidate among A–G clearly dominates.** Candidate D (Volatility-contraction expansion breakout) is the strongest among the new spaces but its rescue-risk distance from G1 / R1a / V2-prime is "Moderate", not "Strong". Phase 4t's primary recommendation is Option A remain paused, with Option B Phase 4u (Candidate D, docs-only, separately authorized) as a conditional secondary. Phase 4t does NOT authorize Phase 4u, does NOT create a strategy spec, does NOT name a runnable strategy, does NOT change any retained verdict or project lock.

## Relationship to Phase 4s

- Phase 4s recommended remain-paused as primary and Phase 4t (docs-only fresh-hypothesis discovery memo) as conditional secondary, contingent on explicit operator authorization.
- The operator chose Option B; Phase 4t was authorized as docs-only.
- Phase 4t operates under the Phase 4m 18-requirement validity gate, the Phase 4s rejection topology, and the Phase 4s forbidden-rescue observations.
- Phase 4t does NOT modify Phase 4s. Phase 4s's verdict-preservation, rejection-topology, and forbidden-rescue observations are binding inputs.
- Phase 4t does NOT create a strategy spec, run a backtest, acquire data, or implement code.

## Candidate pool considered

Eight candidates (A–H). Detailed evaluation in the Phase 4t memo. Compact recap:

```text
A — Structural-R trend continuation revisited           (Phase 4n A)
B — Funding-context trend/risk filter revisited         (Phase 4n C; reframed)
C — Structural pullback continuation revisited          (Phase 4n D)
D — Volatility-contraction expansion breakout           (NEW)
E — Event-risk / funding-stress avoidance overlay       (NEW; risk overlay)
F — Market microstructure / liquidity-timing research   (NEW; data-unavailable)
G — Cross-timeframe continuation without hard regime    (NEW)
H — No new candidate / remain paused                    (real outcome)
```

## Candidate scoring matrix

Qualitative ratings only. **Strong / Moderate / Weak / High risk / Reject.** No numeric optimization.

```text
Dimension                                   A          B          C          D          E          F          G          H
------------------------------------------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ----------
D1: New-theory strength                     Moderate   Moderate   Weak       Strong     Weak       Moderate   Moderate   n/a
D2: Distance from forbidden rescue          Moderate   Moderate   Weak       Moderate   Weak       Strong     Moderate   n/a
D3: Opportunity-rate viability              Moderate   Moderate   Moderate   Strong     n/a        Moderate   Moderate   n/a
D4: Co-design clarity (V2+G1 lessons)       Moderate   Moderate   Moderate   Strong     Weak       Moderate   Moderate   n/a
D5: Data feasibility (existing only)        Strong     Strong     Strong     Strong     Strong     Reject     Strong     Strong
D6: Cost-survival plausibility (§11.6)      Moderate   Moderate   Weak       Moderate   n/a        Moderate   Moderate   Strong
D7: Mechanism-check designability           Strong     Moderate   Strong     Strong     Weak       Moderate   Moderate   n/a
D8: Governance compatibility                Strong     Strong     Strong     Strong     Strong     Reject     Strong     Strong
D9: Implementation complexity later         Moderate   Moderate   Moderate   Moderate   Weak       High risk  Moderate   n/a
D10: Research value                         Moderate   Moderate   Weak       Strong     Weak       Moderate   Moderate   Strong
Recommendation                              not now    not now    not now    conditional not now    rejected   not now    primary
                                                                              secondary  (overlay)  at this              (Option A)
                                                                              (Option B)            boundary
```

Candidate D is the strongest research candidate; Candidate H is the primary recommendation because no candidate clearly dominates the validity gate.

## Rescue-risk analysis

- **A:** trap "V2 with wider stop filter"; avoidance credibility Moderate.
- **B:** trap "D1-A with extra filters / D1-A-prime"; avoidance credibility Strong as overlay-only, but weak strategic value as primary.
- **C:** trap "R2 with cheaper costs"; avoidance credibility Weak.
- **D:** primary trap "G1 with one-dimension volatility-only regime gate"; secondary "R1a rescue"; tertiary "V2-prime"; avoidance credibility Moderate; requires elevated design discipline.
- **E:** trap "D1-A as overlay rather than directional rule"; risk overlay only, not primary candidate.
- **F:** trap "if I had finer-resolution data, the strategy would work" (acquisition temptation); rejected at this boundary because data unavailable.
- **G:** trap "G1 with HTF demoted from gate to input but otherwise similar"; avoidance credibility Moderate; predeclaring continuous shaping rules without sliding into AND-gates is delicate.
- **H:** strongest governance option after five rejection events; preserves possibility of genuinely new theoretical insight without predeclaration → rejection pattern repeating mechanically.

## Opportunity-rate viability analysis

Required for every candidate after G1. Phase 4t restated this as observations only (NOT adopted thresholds; NOT derived from Phase 4r forensic numbers):

- **A:** intrinsic candidate-arrival rate from structural-R derivation; predeclare before any backtest.
- **B:** as overlay, opportunity-rate is bounded by primary thesis; not a primary candidate.
- **C:** pullback-arrival rate × HIGH-cost survival is a tight combination on BTCUSDT 15m / 30m.
- **D:** intrinsic transition-detection rate plus joint (transition AND setup AND stop_distance_passes) rate; explicit "intersection rate" diagnostic similar to G1's CFP-9 must be predeclared in Phase 4u.
- **E:** as overlay, residual trade count post-overlay; not primary.
- **F:** rejected at this boundary.
- **G:** HTF inputs as continuous shaping parameters do not filter trade opportunities; opportunity-rate determined by entry rule.
- **H:** n/a.

## Data-readiness implications

```text
Candidate   Data classification
----------- ----------------------------------------------------------------------
A           existing-data feasible (v002 + Phase 4i klines + v002 funding)
B           existing-data feasible (v002 funding only; no metrics OI)
C           existing-data feasible (v002 + Phase 4i klines + v002 funding)
D           existing-data feasible (Phase 4i 30m / 4h klines; v002 1h-derived;
            v002 funding optional as sizing modulator)
E           existing-data feasible as overlay; rejected as primary
F           UNAVAILABLE-DATA DEPENDENT (rejected at this boundary)
G           existing-data feasible (Phase 4i 30m / 4h klines; v002 1h-derived;
            v002 funding optional as shaping input)
H           n/a
```

No candidate among A–G except F requires new acquisition. F is rejected at this boundary.

## Final recommendation

**Primary recommendation: Option A — remain paused.**

**Conditional secondary: Option B — authorize Phase 4u — Volatility-Contraction Expansion Breakout Hypothesis Spec Memo (docs-only) on Candidate D**, only if the operator explicitly chooses to continue research now and accepts elevated discipline burden. Phase 4u, if ever authorized, must follow the Phase 4o → 4p → 4q → 4r template's discipline (not its V2 / G1 numeric thresholds), predeclare opportunity-rate viability before any data is touched, design Candidate D's contraction-state as a local precondition (NOT a top-level state machine), and explicitly forbid all G1-AND-classifier / R1a-bolt-on / V2-prime / D1-A / F1 / R2 rescue patterns. **Phase 4t does NOT authorize Phase 4u.**

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4t/post-g1-fresh-hypothesis-discovery
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q (-> pytest)
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4t_post-g1-fresh-hypothesis-discovery.md
git commit -m "phase-4t: post-G1 fresh-hypothesis discovery memo (docs-only)"
git push -u origin phase-4t/post-g1-fresh-hypothesis-discovery
```

(No acquisition, diagnostics, or backtest scripts were run. No web research was performed for this memo; all analysis is derived from the existing project record and the Phase 4m / Phase 4s validity gate framework.)

## Verification results

```text
Python version             : 3.12.4
ruff check . (initial)     : All checks passed!
pytest (initial)           : 785 passed
mypy (initial)             : Success: no issues found in 82 source files
git status (initial)       : clean working tree (only gitignored
                              .claude/scheduled_tasks.lock and data/research/
                              untracked; not committed)
git rev-parse main         : 1b2a2643540a6f3eb50fea740743528b462c8492
git rev-parse origin/main  : 1b2a2643540a6f3eb50fea740743528b462c8492
```

## Commit

```text
Phase 4t memo commit:      c6d9b30bbd76c5f0fb30a63ba1fc0276a11a89c3
Phase 4t closeout commit:  <recorded after this file is committed>
```

## Final git status

(recorded after closeout commit and push)

## Final git log --oneline -5

(recorded after closeout commit and push)

## Final rev-parse

```text
HEAD                                                            : <recorded after closeout commit>
origin/phase-4t/post-g1-fresh-hypothesis-discovery              : <recorded after closeout push>
main                                                            : 1b2a2643540a6f3eb50fea740743528b462c8492 (unchanged)
origin/main                                                     : 1b2a2643540a6f3eb50fea740743528b462c8492 (unchanged)
```

## Branch / main status

`main` remains unchanged at `1b2a2643540a6f3eb50fea740743528b462c8492`. Phase 4t is authored exclusively on the `phase-4t/post-g1-fresh-hypothesis-discovery` branch. Phase 4t is **not** merged to main by this closeout. Any future merge to main requires a separate explicit operator authorization brief (analogous to prior phase merge closeouts).

## Forbidden-work confirmation

Phase 4t did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script;
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
```

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

**Phase 4t was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state remains paused (Option A primary). No next phase authorized.**
