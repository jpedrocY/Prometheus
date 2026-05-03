# Phase 4t Merge Closeout

## Summary

Phase 4t — Post-G1 Fresh-Hypothesis Discovery Memo (docs-only) — has been merged into `main` via a no-fast-forward merge commit. Phase 4t is the project's second fresh-hypothesis discovery memo (after Phase 4n, which led to the G1 research arc that ended in Verdict C HARD REJECT). Phase 4t evaluated eight candidate spaces (A — Structural-R trend continuation revisited; B — Funding-context trend/risk filter revisited; C — Structural pullback continuation revisited; D — Volatility-contraction expansion breakout; E — Event-risk / funding-stress avoidance overlay; F — Market microstructure / liquidity-timing research; G — Cross-timeframe continuation without hard regime gate; H — No new candidate / remain paused) under the Phase 4m 18-requirement fresh-hypothesis validity gate, the Phase 4s rejection topology (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism / framework mismatch; V2 design-stage incompatibility; G1 regime-gate-meets-setup intersection sparseness), the Phase 4s reusable insights, and the Phase 4s forbidden-rescue observations. **Phase 4t recommends Option A — remain paused as primary.** Phase 4t records **Option B — conditional secondary** as a future docs-only Phase 4u Volatility-Contraction Expansion Breakout Hypothesis Spec Memo on Candidate D, only if separately authorized and only with elevated discipline. Phase 4t was docs-only.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4t_post-g1-fresh-hypothesis-discovery.md   (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4t_closeout.md                              (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4t_merge-closeout.md                       (added by housekeeping commit — this file)
docs/00-meta/current-project-state.md                                                            (modified by housekeeping commit — narrow Phase 4t paragraph + "Current phase" / "Most recent merge" refresh)
```

No other files modified by Phase 4t or by this merge.

## Phase 4t commits included

```text
c6d9b30bbd76c5f0fb30a63ba1fc0276a11a89c3   phase-4t: post-G1 fresh-hypothesis discovery memo (docs-only)
d377d0882667f752d17b6b3e44a431f1af556bc8   phase-4t: closeout (post-G1 fresh-hypothesis discovery)
```

## Merge commit

```text
5e831d2a1f0e881f963a44d1cf8b1a7fb6b83b5b   Merge Phase 4t (post-G1 fresh-hypothesis discovery, docs-only) into main
```

## Housekeeping commit

```text
<recorded after this file is committed>
```

## Final git status

(recorded after housekeeping commit and push)

## Final git log --oneline -8

(recorded after housekeeping commit and push)

## Final rev-parse

```text
main          : <recorded after housekeeping push>
origin/main   : <recorded after housekeeping push>
```

## main == origin/main confirmation

(verified after housekeeping push; reported in chat)

## Discovery conclusion

- **Phase 4t was docs-only.**
- Phase 4t evaluated eight candidate spaces after the G1 hard reject.
- Phase 4t does **NOT** authorize Phase 4u.
- Phase 4t does **NOT** create a strategy spec.
- Phase 4t does **NOT** name a runnable strategy.
- Phase 4t does **NOT** authorize backtest, implementation, data acquisition, paper / shadow / live, or exchange-write.
- **No retained verdict is revised.**
- **No project lock is changed.**

## Relationship to Phase 4s

- Phase 4s recommended remain-paused as primary and Phase 4t (docs-only fresh-hypothesis discovery memo) as conditional secondary, contingent on explicit operator authorization.
- The operator chose Option B; Phase 4t was authorized as docs-only.
- Phase 4t operated under the Phase 4m 18-requirement validity gate, the Phase 4s rejection topology, and the Phase 4s forbidden-rescue observations.
- Phase 4t did NOT modify Phase 4s. Phase 4s's verdict-preservation, rejection-topology, and forbidden-rescue observations are binding inputs.

## Candidate pool considered

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

Candidate D is the strongest research candidate. Candidate H (remain paused) is the primary recommendation because no candidate clearly dominates the validity gate.

## Rescue-risk analysis

- **A (Structural-R trend continuation):** trap "V2 with wider stop filter"; avoidance credibility Moderate.
- **B (Funding-context risk filter):** trap "D1-A with extra filters / D1-A-prime"; avoidance credibility Strong as overlay-only, but weak strategic value as primary.
- **C (Structural pullback):** trap "R2 with cheaper costs"; avoidance credibility Weak.
- **D (Volatility-contraction expansion breakout):** primary trap "G1 with one-dimension volatility-only regime gate"; secondary "R1a rescue"; tertiary "V2-prime"; avoidance credibility Moderate; requires elevated design discipline (predeclared opportunity-rate viability; contraction-state as local precondition; entry rule fires on transition itself; explicit anti-rescue patterns).
- **E (Event-risk avoidance overlay):** trap "D1-A as overlay rather than directional rule"; risk overlay only, not primary candidate.
- **F (Microstructure / liquidity-timing):** trap "if I had finer-resolution data, the strategy would work" (acquisition temptation); rejected at this boundary because data unavailable; Phase 4t cannot authorize acquisition.
- **G (Cross-timeframe shaping without regime gate):** trap "G1 with HTF demoted from gate to input but otherwise similar"; avoidance credibility Moderate; predeclaring continuous shaping rules without sliding into AND-gates is delicate.
- **H (Remain paused):** strongest governance option after five rejection events; preserves possibility of genuinely new theoretical insight without predeclaration → rejection pattern repeating mechanically.

## Opportunity-rate viability analysis

After G1, every candidate must include an explicit opportunity-rate viability story. Phase 4t recorded these as observations only (NOT adopted thresholds; NOT derived from Phase 4r forensic numbers):

- **A:** intrinsic candidate-arrival rate from structural-R derivation; predeclare before any backtest.
- **B:** as overlay, opportunity-rate is bounded by primary thesis; not a primary candidate.
- **C:** pullback-arrival rate × HIGH-cost survival is a tight combination on BTCUSDT 15m / 30m.
- **D:** intrinsic transition-detection rate plus joint (transition AND setup AND stop_distance_passes) rate; explicit "intersection rate" diagnostic similar to G1's CFP-9 must be predeclared in any future Phase 4u memo *before* data is touched.
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

No candidate among A–G except F requires new acquisition. F is rejected at this boundary. **Phase 4j §11 metrics OI-subset partial-eligibility rule** is preserved but should NOT be used by any future hypothesis on Phase 4t's recommended path (Candidate D).

## Final recommendation

- **Option A — primary recommendation:** remain paused.
- **Option B — conditional secondary:** authorize Phase 4u — Volatility-Contraction Expansion Breakout Hypothesis Spec Memo (docs-only) on Candidate D, only if the operator explicitly chooses to continue research now. Acceptable shape:
  - Phase 4u memo MUST follow the Phase 4o → 4p → 4q → 4r template's *discipline*, not its V2 / G1 numeric thresholds.
  - Phase 4u memo MUST predeclare an explicit **opportunity-rate viability story** before any data is touched.
  - Phase 4u memo MUST design Candidate D's contraction-state as a *local precondition with high frequency*, NOT as a top-level state machine.
  - Phase 4u memo MUST design the entry rule to fire on the *transition* itself, not despite the state.
  - Phase 4u memo MUST explicitly forbid: G1-style five-dimension AND classifier; R1a-style per-bar volatility-percentile bolt-on filter; V2's 20/40-bar Donchian setup or 0.60–1.80 × ATR stop-distance bound; D1-A-style funding-Z-score directional rule; F1-style mean-reversion logic; R2-style pullback-retest entry; cost-model relaxation; mark-price / aggTrades / spot / cross-venue / metrics OI / 5m diagnostic outputs as features.
  - Phase 4u memo MUST be docs-only; MUST NOT acquire data; MUST NOT define exact thresholds beyond the Phase 4u layer; MUST NOT name a runnable strategy beyond the conceptual name.

**Phase 4u is NOT started by this merge.** Phase 4u execution requires a separate explicit operator authorization brief.

**Candidate D is strongest among A–G but does NOT clearly dominate enough to displace remain-paused as the primary recommendation.** Candidate D has Moderate rescue-risk distance from G1 / R1a / V2-prime; the elevated discipline burden in any future Phase 4u memo is the safeguard.

NOT recommended:

- immediate strategy spec is rejected unless Phase 4u is separately authorized;
- immediate backtest is rejected;
- data acquisition is rejected;
- paper / shadow / live / exchange-write is forbidden;
- Phase 4 canonical is forbidden;
- G1 / V2 / R2 / F1 / D1-A rescue is forbidden;
- Candidate F (microstructure) rejected at this boundary;
- Candidates A / B / C / E / G not recommended at this boundary.

## Verification evidence

Quality gates verified clean during Phase 4t and across the merge:

```text
ruff check .   : All checks passed!
pytest         : 785 passed (no regressions)
mypy           : Success: no issues found in 82 source files
```

No code, tests, scripts, data, or manifests were modified by Phase 4t; the quality gates simply confirm that the documentation-only changes did not regress the repository.

## Forbidden-work confirmation

Phase 4t and this merge did NOT do any of the following:

- start Phase 4u or any successor phase;
- create any new strategy spec;
- create a runnable strategy;
- create V3 / H2 / G2 / any runnable candidate;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- define exact thresholds;
- define a backtest plan;
- run a backtest;
- run diagnostics;
- run acquisition scripts;
- modify `src/prometheus/` code;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- modify `data/raw/` / `data/normalized/` / `data/manifests/`;
- commit `data/research/` outputs;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- create v003;
- use metrics OI as a new hypothesis input;
- use optional metrics ratio columns;
- use 5m Q1–Q7 findings as rule candidates;
- use V2 Phase 4l stop-distance failure numbers to choose thresholds;
- use Phase 4r G1 active-fraction numbers to choose thresholds;
- use the G1 always-active 124-trade / −0.34 mean_R result as a candidate-tuning target;
- modify Phase 4p G1 strategy-spec selections;
- modify Phase 4q methodology;
- modify Phase 4j §11 governance;
- modify Phase 4k methodology;
- revise retained verdicts;
- revise project locks, thresholds, parameters, or governance rules;
- change §11.6 / §1.7.3 / Phase 3r governance / Phase 3v governance / Phase 3w governance / Phase 4j governance / Phase 4k methodology;
- start Phase 4 canonical;
- implement reconciliation;
- implement a real exchange adapter;
- implement exchange-write capability;
- place or cancel orders;
- use / request / store credentials;
- add authenticated REST / private endpoints / public endpoint clients / user stream / WebSocket / listenKey lifecycle;
- enable MCP / Graphify or modify `.mcp.json`;
- create `.env` files;
- deploy anything;
- create paper / shadow runtime;
- imply live-readiness.

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
                              (this phase; merged)
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
