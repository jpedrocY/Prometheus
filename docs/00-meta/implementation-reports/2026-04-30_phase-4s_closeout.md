# Phase 4s Closeout

## Summary

Phase 4s authored the project's third post-rejection strategy-research consolidation memo (after Phase 3e for F1, Phase 3k for D1-A, Phase 4m for V2). The memo records the Phase 4r G1 — Regime-First Breakout Continuation backtest outcome (Verdict C HARD REJECT; binding driver CFP-1 critical; independent driver CFP-9; subordinate / mechanical CFP-3 and CFP-4), reaffirms every retained verdict and project lock, updates the rejection topology with G1's distinct failure mode (regime-gate-meets-setup intersection sparseness), distinguishes that mode from the four prior rejection modes, extracts ten reusable insights without authorizing any rescue, comparatively analyzes G1 against V2 and against R2 / F1 / D1-A, reaffirms the Phase 4m 18-requirement fresh-hypothesis validity gate as binding, and recommends remain-paused as primary with a conditional secondary path for a future docs-only fresh-hypothesis discovery memo (Phase 4t) only if the operator explicitly chooses to continue research. Phase 4s was docs-only.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4s_post-g1-strategy-research-consolidation.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4s_closeout.md                                   (new — this file)
```

No other files modified by Phase 4s.

## Consolidation conclusion

Phase 4s is the methodologically-disciplined post-mortem of the Phase 4r G1 backtest. It records the binding outcome (Verdict C HARD REJECT) and the *specific* G1 lesson — that **regime gates can destroy sample size and prevent expectancy evaluation entirely** — as a structurally distinct fifth failure mode in the project's rejection topology, alongside R2 cost-fragility, F1 catastrophic-floor, D1-A mechanism / framework mismatch, and V2 design-stage incompatibility. Phase 4s does NOT amend any Phase 4p / 4q decision, does NOT propose any G1 rescue, does NOT name any new candidate, and does NOT authorize any successor phase. The project boundary after Phase 4s remains paused; G1 first-spec is terminally HARD REJECTED as retained research evidence only.

## Updated strategy verdict map

```text
H0           : FRAMEWORK ANCHOR (Phase 2i §1.7.3)
R3           : BASELINE-OF-RECORD (Phase 2p §C.1 — V1 breakout)
R1a          : RETAINED — NON-LEADING (research evidence only)
R1b-narrow   : RETAINED — NON-LEADING (research evidence only)
R2           : FAILED — §11.6 cost-sensitivity gate blocks
F1           : HARD REJECT (Phase 3c §7.3 catastrophic-floor predicate;
                Phase 3d-B2 terminal)
D1-A         : MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3h §11.2;
                Phase 3j terminal)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
V2           : HARD REJECT — structural CFP-1 critical (Phase 4l;
                terminal for V2 first-spec)
G1           : HARD REJECT — CFP-1 critical AND CFP-9 (Phase 4r;
                terminal for G1 first-spec)
```

No verdict revised. No project lock changed.

## G1 rejection mechanism

G1 did **not** primarily fail because active-regime trades lost money. G1 failed because the active-regime trade population was empty (zero trades on BTC OOS HIGH for the train-best variant; zero across all 32 variants). The Phase 4p locked five-dimension AND classifier (HTF trend AND DE_4h ≥ E_min AND ATR percentile in band AND relative-volume ≥ V_liq_min AND funding percentile in band) was structurally too narrow relative to the 30m Donchian breakout setup. Active-regime windows and breakout-trigger arrival times did not intersect with sufficient frequency. The always-active baseline (124 trades; mean_R = −0.34 under HIGH cost) confirms the breakout-and-stop machinery fired and was loss-making at §11.6 = 8 bps. G1 failed at the intersection of regime gate sparsity, breakout setup arrival timing, sample-size / trade-count floor, and HIGH-cost realism.

## Updated rejection topology

```text
Strategy   Rejection mode                                  Lesson
---------- ----------------------------------------------- ---------------------------------------------------------
R2         cost-fragility                                  Partial mechanism evidence (M1 ✓, M3 ✓) can fail §11.6
                                                            HIGH-cost survival; slippage realism is a hard gate.
F1         catastrophic-floor / bad full-population         Profitable subsets do not rescue a losing framework;
            expectancy                                       the catastrophic-floor predicate enforces this.
D1-A       mechanism / framework mismatch                  Context (here funding) may carry information at the
            ("MECHANISM PASS / FRAMEWORK FAIL — other")     mechanism layer (M1 PASS) without delivering at the
                                                            framework / promotion layer (M2 ✗ in the form required
                                                            for promotion).
V2         design-stage incompatibility                    Setup window / structural stop / target / position sizing
                                                            must be co-designed; importing one element (e.g. stop-
                                                            distance bounds) from a different design produces
                                                            structural rejection at the pre-trade gate.
G1         regime-gate-meets-setup intersection sparseness Regime filters can destroy sample size and prevent
                                                            expectancy evaluation entirely. A regime hypothesis must
                                                            be validated for both selectivity AND opportunity-rate
                                                            preservation, not selectivity alone.
```

R2 / F1 / D1-A failed *with mechanism evidence*. V2 / G1 failed *before mechanism evidence was generable*. These are categorically different failure layers; Phase 4s preserves the distinction in the project record so future hypotheses can target either.

## Reusable insights

Ten reusable insights, recorded without authorizing any rescue:

1. Regime-first is theoretically valid as a research concept; G1's first-spec implementation was too narrow at the intersection layer. Future regime-first hypotheses must validate not just classifier selectivity but classifier-AND-entry-rule arrival rate.
2. Active-regime fraction alone is not enough; active-regime entry-rule arrival rate matters. CFP-9's < 5% threshold is necessary but not sufficient.
3. Always-active baselines are valuable structural negative controls; G1's 124-trade always-active baseline at mean_R = −0.34 was the binding diagnostic.
4. Inactive-population pseudo-trades are valuable but methodologically inert when active population is empty.
5. HIGH-cost realism still matters even when the primary failure is no-trade.
6. Zero-trade outcomes can make PBO / DSR / CSCV methodologically inert; the statistics correctly carry no signal in that regime.
7. CFP-9 (regime active fraction < 5%) is important and worked correctly; it detected sample-size collapse before any over-interpretation of mechanism evidence.
8. CFP-1 (insufficient trade count) and CFP-9 (active-fraction collapse) are **independent drivers** in this run.
9. M1 / M2 negative tests are valuable but degenerate if active population is empty; the Phase 4q implementation correctly reported FAIL rather than spuriously passing.
10. A good hypothesis can still fail at operational geometry. G1's predeclaration discipline was correct; the failure is real research evidence and is preserved as such.

## Forbidden rescue observations

Phase 4s explicitly forbids (binding for any future phase until and unless a separate explicit operator authorization removes the prohibition):

- G1 with relaxed classifier thresholds; G1 with E_min lowered; G1 with wider ATR band; G1 with lower V_liq_min; G1 with wider funding band; G1 with K_confirm reduced; G1 with regime gate removed; G1 with 30m breakout loosened; G1 with stop-distance bounds widened; G1 with T_stop / N_R changed.
- G1-prime / G1-narrow / G1-extension / G1 hybrid.
- Any Phase 4p G1 strategy-spec amendment based on Phase 4r forensic numbers (the 2.03% active fraction; the 124 always-active baseline trades; the −0.34 mean_R).
- Any Phase 4q methodology amendment based on Phase 4r forensic numbers.
- Immediate G1 rerun.
- Immediate always-active rescue (the always-active baseline produced mean_R = −0.34 under §11.6 = 8 bps; not viable).
- Immediate data acquisition to rescue G1.
- Using Phase 4r active-fraction numbers as tuning targets for any future regime-first hypothesis.

These prohibitions mirror Phase 4m's V2-rescue prohibitions and apply with equivalent force.

## Recommended next operator choice

- **Option A — primary recommendation:** remain paused. Rationale: Phase 4r is the project's fifth strategy-rejection event (R2 / F1 / D1-A / V2 / G1); each has produced a distinct lesson; the Phase 4m fresh-hypothesis validity gate is binding; there is no internally-derived new hypothesis ready for predeclaration; immediate authorization of another fresh-hypothesis discovery memo risks the same predeclaration → first-spec rejection pattern without time to consolidate the regime-gate-meets-setup intersection lesson into design-discipline practice.
- **Option B — conditional secondary:** authorize a docs-only fresh-hypothesis discovery memo (Phase 4t), only if the operator explicitly chooses to continue research now. Acceptable shape if chosen: a Phase 4t docs-only memo analogous to Phase 4n, evaluating a *new* candidate space against the Phase 4m 18-requirement validity gate and the Phase 4s rejection topology; must NOT propose any G1 / V2 / R2 / F1 / D1-A rescue; must NOT use Phase 4r forensic numbers as input; must predeclare any new candidate's opportunity-rate floor before touching data; must satisfy separate operator authorization. **Phase 4s does NOT authorize Phase 4t.**

NOT recommended: G1 rescue (REJECTED); immediate G1 implementation (REJECTED); immediate backtest (REJECTED); data acquisition (REJECTED); paper / shadow / live (FORBIDDEN); Phase 4 canonical (FORBIDDEN); production-key creation / authenticated APIs / private endpoints / user stream / WebSocket (FORBIDDEN); MCP / Graphify / `.mcp.json` / credentials (FORBIDDEN); exchange-write capability (FORBIDDEN); V2 / F1 / D1-A / R2 rescue (FORBIDDEN).

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4s/post-g1-strategy-research-consolidation
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q (-> pytest)
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4s_post-g1-strategy-research-consolidation.md
git commit -m "phase-4s: post-G1 strategy research consolidation memo (docs-only)"
git push -u origin phase-4s/post-g1-strategy-research-consolidation
```

(No acquisition, diagnostics, or backtest scripts were run.)

## Verification results

```text
Python version             : 3.12.4
ruff check . (initial)     : All checks passed!
pytest (initial)           : 785 passed
mypy (initial)             : Success: no issues found in 82 source files
git status (initial)       : clean working tree (only gitignored
                              .claude/scheduled_tasks.lock and data/research/
                              untracked; not committed)
git rev-parse main         : 03a626ff260aaf8608d9ee5f9fc2451a14361bfb
git rev-parse origin/main  : 03a626ff260aaf8608d9ee5f9fc2451a14361bfb
```

## Commit

```text
Phase 4s memo commit:      376a586b8ff24b180bf909e38727ed422f2f5401
Phase 4s closeout commit:  <recorded after this file is committed>
```

## Final git status

(recorded after closeout commit and push)

## Final git log --oneline -5

(recorded after closeout commit and push)

## Final rev-parse

```text
HEAD                                                             : <recorded after closeout commit>
origin/phase-4s/post-g1-strategy-research-consolidation          : <recorded after closeout push>
main                                                             : 03a626ff260aaf8608d9ee5f9fc2451a14361bfb (unchanged)
origin/main                                                      : 03a626ff260aaf8608d9ee5f9fc2451a14361bfb (unchanged)
```

## Branch / main status

`main` remains unchanged at `03a626ff260aaf8608d9ee5f9fc2451a14361bfb`. Phase 4s is authored exclusively on the `phase-4s/post-g1-strategy-research-consolidation` branch. Phase 4s is **not** merged to main by this closeout. Any future merge to main requires a separate explicit operator authorization brief (analogous to prior phase merge closeouts).

## Forbidden-work confirmation

Phase 4s did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script (no `scripts/...py` added);
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
- create any new strategy candidate;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4t / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret.

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
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r
                            : all preserved verbatim
Phase 4s                    : Post-G1 strategy research consolidation memo
                              (this phase; new; docs-only)
Recommended state           : paused
```

## Next authorization status

```text
Phase 4t                       : NOT authorized
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
New family research            : NOT authorized at this boundary; would
                                  require a separately authorized
                                  fresh-hypothesis discovery memo (Phase 4t)
                                  under the Phase 4m 18-requirement validity
                                  gate.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4t (fresh-hypothesis discovery memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4s consolidation boundary.

---

**Phase 4s was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state remains paused. No next phase authorized.**
