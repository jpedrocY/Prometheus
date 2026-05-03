# Phase 4s Merge Closeout

## Summary

Phase 4s — Post-G1 Strategy Research Consolidation Memo (docs-only) — has been merged into `main` via a no-fast-forward merge commit. Phase 4s is the project's third post-rejection strategy-research consolidation memo (after Phase 3e for F1, Phase 3k for D1-A, Phase 4m for V2). It records the Phase 4r G1 — Regime-First Breakout Continuation backtest outcome (Verdict C HARD REJECT; binding driver CFP-1 critical; independent driver CFP-9; subordinate / mechanical CFP-3 and CFP-4), reaffirms every retained verdict and project lock verbatim, updates the rejection topology with G1's distinct fifth failure mode (regime-gate-meets-setup intersection sparseness), distinguishes that mode from the four prior rejection modes (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism / framework mismatch; V2 design-stage incompatibility), records the categorical distinction that R2 / F1 / D1-A failed *with* mechanism evidence while V2 / G1 failed *before* mechanism evidence was generable, extracts ten reusable insights without authorizing any rescue, comparatively analyzes G1 against V2 and against R2 / F1 / D1-A, reaffirms the Phase 4m 18-requirement fresh-hypothesis validity gate as binding (with the observation that requirement #4 should now be read to include regime-gate / entry-rule / sample-size-viability co-design alongside V2's setup-geometry / stop-filter co-design lesson), and recommends remain-paused as primary with a conditional secondary path for a future docs-only fresh-hypothesis discovery memo (Phase 4t) only if the operator explicitly chooses to continue research. Phase 4s was docs-only.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4s_post-g1-strategy-research-consolidation.md   (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4s_closeout.md                                   (added by merge)
docs/00-meta/implementation-reports/2026-04-30_phase-4s_merge-closeout.md                            (added by housekeeping commit — this file)
docs/00-meta/current-project-state.md                                                                  (modified by housekeeping commit — narrow Phase 4s paragraph + "Current phase" / "Most recent merge" refresh)
```

No other files modified by Phase 4s or by this merge.

## Phase 4s commits included

```text
376a586b8ff24b180bf909e38727ed422f2f5401   phase-4s: post-G1 strategy research consolidation memo (docs-only)
92d51ebba9492eda92e2a0c690995ba06e181154   phase-4s: closeout (post-G1 strategy research consolidation)
```

## Merge commit

```text
7710b11425247babbd3d9044579cbeca70cf7b76   Merge Phase 4s (post-G1 strategy research consolidation, docs-only) into main
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

## Consolidation conclusion

- **Phase 4s was docs-only.**
- Phase 4s consolidated the Phase 4r G1 rejection into the project's strategy-research record.
- Phase 4s does **NOT** authorize Phase 4t.
- Phase 4s does **NOT** create a new strategy candidate.
- Phase 4s does **NOT** authorize backtest, implementation, data acquisition, paper / shadow / live, or exchange-write.
- **No retained verdict is revised.**
- **No project lock is changed.**

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
V2           : HARD REJECT — terminal for V2 first-spec (Phase 4l)
G1           : HARD REJECT — terminal for G1 first-spec (Phase 4r —
                Verdict C; CFP-1 critical binding driver; CFP-9
                independent driver)
```

No verdict revised. No project lock changed.

## G1 rejection mechanism

- G1 did **not** primarily fail because active-regime trades lost money.
- G1 failed because the active-regime trade population was **empty / too sparse**.
- All 32 variants produced **0 BTC OOS HIGH G1 trades**.
- BTC train-best (variant id=0) OOS HIGH `trade_count = 0`.
- BTC train-best OOS HIGH `mean_R = 0`.
- **Always-active baseline produced 124 BTC OOS HIGH trades with mean_R = −0.34** (loss-making at §11.6 = 8 bps), confirming the breakout-and-stop machinery fired.
- **Inactive-population pseudo-trades produced 124 BTC OOS HIGH trades with mean_R = −0.34** (also loss-making; rules out "regime gate filters out the only profitable subset" alternative explanation).
- **ETH G1 produced 0 qualifying trades** for the train-best variant across all windows and cost cells; ETH cannot rescue BTC.
- **CFP-1 triggered and is binding** (32 / 32 variants below the 30-trade threshold on OOS BTC HIGH; train-best produced 0 trades).
- **CFP-9 triggered and is independent** (BTC OOS regime-active fraction = 2.03% < 5% threshold).
- **CFP-3 and CFP-4 triggered as subordinate / mechanical** (PF = 0 under empty arrays; M3 BTC FAIL with degenerate M4 ETH trivial PASS — ETH cannot rescue BTC).
- **CFP-2 / CFP-5 / CFP-6 / CFP-7 / CFP-8 / CFP-10 / CFP-11 / CFP-12 did not trigger.**
- The specific G1 failure mode is **regime-gate-meets-setup intersection sparseness**: the Phase 4p locked five-dimension AND classifier was structurally too narrow relative to the 30m breakout trigger, and `regime_active` windows did not intersect breakout-trigger arrival times with sufficient frequency.

## Updated rejection topology

```text
Strategy   Rejection mode                                  Mechanism evidence layer
---------- ----------------------------------------------- --------------------------------------
R2         cost-fragility                                  failed WITH mechanism evidence
F1         catastrophic-floor / bad full-population        failed WITH mechanism evidence
            expectancy
D1-A       mechanism / framework mismatch                  failed WITH mechanism evidence
V2         design-stage incompatibility                    failed BEFORE mechanism evidence
                                                            was generable
G1         regime-gate-meets-setup intersection sparseness failed BEFORE mechanism evidence
                                                            was generable
```

R2 / F1 / D1-A failed *with* mechanism evidence. V2 / G1 failed *before* mechanism evidence was generable. These are categorically different failure layers; Phase 4s preserves the distinction in the project record so future hypotheses can target either.

## Reusable insights

Ten reusable insights, recorded without authorizing any rescue:

1. **Regime-first is theoretically valid as a research concept**, but G1's first-spec implementation was too narrow at the intersection layer.
2. **Active-regime fraction alone is insufficient.** CFP-9's < 5% threshold is necessary but not sufficient.
3. **Active-regime entry-rule arrival rate matters** — the joint event `(regime_active AND breakout_setup AND stop_distance_passes)` is the binding rate, not the active fraction alone.
4. **Always-active baselines are valuable structural negative controls.** G1's 124-trade always-active baseline at mean_R = −0.34 was the binding diagnostic.
5. **Inactive-population pseudo-trades are useful but methodologically inert when active population is empty.** They are valuable for falsification only when active is non-empty.
6. **HIGH-cost realism still matters even when the primary failure is no-trade.** The always-active negative mean_R under §11.6 = 8 bps reaffirms R2's cost-fragility lesson.
7. **Zero-trade outcomes can make PBO / DSR / CSCV methodologically inert.** This is not a defect of those statistics; it is a defect of the strategy under that data.
8. **CFP-9 (regime active fraction < 5%) is important and worked correctly.** It detected sample-size collapse before any over-interpretation of mechanism evidence.
9. **CFP-1 and CFP-9 are independent drivers in this run** — both triggered, both binding, neither subordinate.
10. **A good hypothesis can still fail at operational geometry.** G1's predeclaration discipline was correct; the failure is real research evidence and is preserved as such.

## Forbidden rescue observations

Phase 4s explicitly forbids (binding for any future phase until and unless a separate explicit operator authorization removes the prohibition):

- **G1 with relaxed classifier thresholds**: forbidden.
- **G1 with E_min lowering** (below 0.30): forbidden.
- **G1 with wider ATR band** (outside the locked {[20, 80], [30, 70]} set): forbidden.
- **G1 with lower V_liq_min** (below 0.80): forbidden.
- **G1 with wider funding band** (outside the locked {[15, 85], [25, 75]} set): forbidden.
- **G1 with K_confirm reduction** (below 2): forbidden.
- **G1 with regime gate removal** (i.e., always-active variant promoted): forbidden.
- **G1 with 30m breakout loosening** (B_atr < 0.10 or N_breakout < 12): forbidden.
- **G1 with stop-distance-bound widening** (outside [0.50, 2.20] × ATR(20)): forbidden.
- **G1 with T_stop / N_R change**: forbidden (these remain reserved as future G1-extension possibilities only, requiring a *separately authorized* governance amendment).
- **G1-prime / G1-narrow / G1-extension / G1 hybrid**: forbidden.
- **Any Phase 4p G1 strategy-spec amendment based on Phase 4r forensic numbers**: forbidden.
- **Any Phase 4q methodology amendment based on Phase 4r forensic numbers**: forbidden.
- **Immediate G1 rerun**: forbidden.
- **Immediate always-active rescue** (the always-active baseline produced mean_R = −0.34 under HIGH cost; not viable): forbidden.
- **Immediate data acquisition to rescue G1** (e.g., acquiring mark-price 30m / 4h / aggTrades to "tighten" the regime classifier): forbidden.
- **Using Phase 4r active-fraction numbers as tuning targets** for any future regime-first hypothesis: forbidden.

These prohibitions mirror Phase 4m's V2-rescue prohibitions and apply with equivalent force.

## Comparison with V2

```text
Layer / question                       V2 (Phase 4l)                          G1 (Phase 4r)
-------------------------------------- -------------------------------------- --------------------------------------
Verdict                                C — HARD REJECT (CFP-1 critical)       C — HARD REJECT (CFP-1 critical AND
                                                                                CFP-9 independent)
Failure layer                          structural first-spec failure          structural first-spec failure
                                        before meaningful expectancy            before meaningful expectancy
                                        evaluation                              evaluation
Did entry rule generate any trades?    NO — every variant 0 trades.           Always-active baseline: 124 trades
                                                                                BTC OOS HIGH (mean_R = -0.34).
Were active-regime trades produced?    n/a (no regime gate in V2)             NO for the train-best variant on OOS
                                                                                HIGH; the regime gate filtered out
                                                                                essentially all entries.
Failure mechanism                      design-stage incompatibility            regime-gate-meets-setup intersection
                                        (setup vs stop filter)                  sparseness
Lesson                                 setup window / stop / target /          regime gate / entry opportunity
                                        sizing must be co-designed              rate / sample-size viability must
                                                                                be co-designed
Authorizes rescue?                     NO                                      NO
```

Both are Verdict C structural first-spec failures before meaningful expectancy evaluation. V2 failed at setup geometry / stop-distance-filter incompatibility. G1 failed at regime-gate / entry-rule / sample-size intersection sparseness. **Neither result authorizes rescue.**

## Comparison with R2 / F1 / D1-A

```text
Strategy   Trade count           Mechanism evidence                Verdict / lesson
---------- --------------------- --------------------------------- -----------------------------------------------
R2         sufficient            yes — M1 ✓, M3 ✓, M2 ✗             FAILED — §11.6 cost-fragility blocked
                                  (partial mechanism)               framework promotion despite partial mechanism
                                                                    evidence. Lesson: cost realism is a hard gate.
F1         sufficient            partial — M1 BTC PARTIAL,         HARD REJECT — Phase 3c §7.3 catastrophic-floor
                                  M3 PASS-isolated but               predicate triggered (5 separate violations).
                                  overwhelmed by 53-54%             Lesson: profitable subsets do not rescue a
                                  STOP exits in wider population.   losing framework expectancy.
D1-A       sufficient            yes — M1 BTC h=32 PASS;           MECHANISM PASS / FRAMEWORK FAIL — other.
                                  M3 PASS-isolated but              Lesson: context (funding) carries information
                                  overwhelmed by 67-68% STOP        at mechanism layer without delivering at
                                  exits at -1.30/-1.24R per         framework / promotion layer.
                                  loser; M2 FAIL on both symbols.
V2         zero                  not evaluable                     HARD REJECT — design-stage incompatibility.
                                                                    Lesson: setup / stop / target / sizing
                                                                    co-design.
G1         zero (regime gate)    not evaluable for active          HARD REJECT — regime-gate-meets-setup
                                  population; always-active          intersection sparseness. Lesson: regime gate /
                                  baseline negative under HIGH       entry-rule arrival / sample-size viability
                                  cost; inactive-population          co-design.
                                  baseline negative.
```

R2 / F1 / D1-A failed *with* mechanism evidence. V2 / G1 failed *before* mechanism evidence was generable. These are categorically different failure layers, and Phase 4s preserves the distinction in the project record so future hypotheses can target either.

## Fresh-hypothesis validity gate reaffirmation

- **The Phase 4m 18-requirement fresh-hypothesis validity gate remains binding** for any future ex-ante hypothesis.
- **Any future hypothesis must be separately authorized** by the operator.
- **Any future hypothesis must NOT be a G1 / V2 / R2 / F1 / D1-A rescue.**
- **Any future hypothesis must NOT use Phase 4r forensic numbers** (the 2.03% active fraction; the 124 always-active baseline trades; the −0.34 mean_R) **as tuning inputs.**
- **Requirement #4** (entry / stop / target / sizing / cost / timeframe / exit must be defined together) **should now be read** to include the **regime-gate / entry-rule / sample-size-viability co-design** lesson alongside the V2 setup-geometry / stop-filter co-design lesson — **as an observation, NOT a governance amendment.** The Phase 4m gate is not amended; it is preserved verbatim.

## Recommended next operator choice

- **Option A — primary recommendation:** remain paused. Rationale: Phase 4r is the project's fifth strategy-rejection event (R2 / F1 / D1-A / V2 / G1); each has produced a distinct lesson; the Phase 4m fresh-hypothesis validity gate is binding; there is no internally-derived new hypothesis ready for predeclaration; the conservative posture is to *pause* and let the rejection topology settle before considering any new candidate.
- **Option B — conditional secondary:** authorize a docs-only fresh-hypothesis discovery memo (Phase 4t), only if the operator explicitly chooses to continue research now. Acceptable shape: a Phase 4t docs-only memo analogous to Phase 4n, evaluating a *new* candidate space against the Phase 4m 18-requirement validity gate and the Phase 4s rejection topology; must NOT propose any G1 / V2 / R2 / F1 / D1-A rescue; must NOT use Phase 4r forensic numbers as input; must predeclare any new candidate's opportunity-rate floor before touching data; must satisfy separate operator authorization.

**Phase 4t is NOT started by this merge.**

NOT recommended:

- G1 rescue — REJECTED.
- Immediate G1 implementation — REJECTED.
- Immediate backtest — REJECTED.
- Data acquisition — REJECTED.
- Paper / shadow / live / exchange-write — FORBIDDEN.
- Phase 4 canonical — FORBIDDEN.
- Production-key creation / authenticated APIs / private endpoints / user stream / WebSocket — FORBIDDEN.
- MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN.
- V2 / F1 / D1-A / R2 rescue — FORBIDDEN.

## Verification evidence

Quality gates verified clean during Phase 4s and across the merge:

```text
ruff check .   : All checks passed!
pytest         : 785 passed (no regressions)
mypy           : Success: no issues found in 82 source files
```

No code, tests, scripts, data, or manifests were modified by Phase 4s; the quality gates simply confirm that the documentation-only changes did not regress the repository.

## Forbidden-work confirmation

Phase 4s and this merge did NOT do any of the following:

- start Phase 4t or any successor phase;
- create any new strategy candidate;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
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
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r
                            : all preserved verbatim
Phase 4s                    : Post-G1 strategy research consolidation memo
                              (this phase; merged)
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
