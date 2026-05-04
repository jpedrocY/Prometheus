# Phase 4y Closeout

## Summary

Phase 4y authored the **Post-C1 Strategy Research Consolidation Memo** (docs-only) on branch `phase-4y/post-c1-strategy-research-consolidation`. Phase 4y consolidated the Phase 4x C1 backtest outcome (Verdict C HARD REJECT; binding driver CFP-2; co-binding CFP-3 / CFP-6) into the project's strategy-research record; updated the rejection topology with C1's distinct failure mode (**fires-and-loses / contraction anti-validation**, NEW); preserved every retained verdict and project lock verbatim; extracted twelve reusable insights; explicitly forbade C1 rescue and cross-strategy rescue interpretations; and recommended remain-paused as primary with a docs-only post-rejection research-process redesign memo as conditional secondary (not started by this merge). **Phase 4y is text-only.** No new strategy candidate was created; no fresh-hypothesis discovery memo was authored; no strategy-spec or backtest-plan memo was authored; no backtest was run; no Phase 4x rerun occurred; `scripts/phase4x_c1_backtest.py` was NOT modified; no implementation code was written; no data was acquired or modified; no manifest was modified; no verdict was revised; no project lock was changed. Whole-repo quality gates remain clean (ruff PASS; pytest 785 PASS; mypy strict 0 issues across 82 source files). **No successor phase authorized.**

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4y_post-c1-strategy-research-consolidation.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4y_closeout.md                                 (new; this file)
```

No source under `src/prometheus/` modified. No tests modified. No scripts modified. No data, manifests, or `.gitignore` modified. `current-project-state.md` will be updated at merge time per the operator's standard merge-housekeeping pattern.

## Consolidation conclusion

The Phase 4x C1 backtest produced Verdict C — C1 framework HARD REJECT, with binding catastrophic-floor driver CFP-2 (BTC OOS HIGH train-best mean_R = -0.3633 ≤ 0) and co-binding drivers CFP-3 (PF=0.4413 < 0.50; max_dd_R=54.55 > 10R) and CFP-6 (DSR=-20.8173 ≤ 0). CFP-1 and CFP-9 explicitly did NOT trigger — C1 fired 149 BTC OOS HIGH trades for the train-best variant; transition rate 3.33 per 480 bars; 100% of variants produced ≥ 30 trades. C1 solved V2 / G1's zero-trade problem and still failed: contraction-tied transitions performed 0.244R worse than non-contraction baseline (bootstrap 95% CI [-0.4101, -0.0810] strictly negative); 0.220R worse than always-active-same-geometry baseline (CI strictly negative); 0.293R worse than delayed-breakout baseline. C1's failure mode is categorically new: **fires-and-loses / contraction anti-validation**, structurally distinct from V2 / G1's design-stage zero-trade collapses and structurally similar to F1's evidence-generating expectancy failure (but cost-binding-distinct from R2). The combined topology now contains six terminal negative outcomes versus two positive anchors (H0, R3) and two retained-research-only positions (R1a, R1b-narrow). Phase 4y reaffirms remain-paused as primary recommendation with stronger evidence than at any previous post-rejection consolidation boundary.

## Relationship to Phase 4x

- Phase 4x executed the first C1 backtest exactly under Phase 4w methodology and emitted Verdict C — C1 framework HARD REJECT.
- Phase 4x recommendation: Option A — remain paused (primary); Option B — Phase 4y post-C1 consolidation memo (conditional secondary).
- The operator authorized Phase 4y on the conditional-secondary path.
- Phase 4y is docs-only.
- Phase 4y does NOT amend Phase 4v C1 strategy spec, Phase 4w C1 backtest-plan methodology, Phase 4j §11 governance, Phase 4k V2 backtest-plan methodology, Phase 3v §8 stop-trigger-domain governance, Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance, Phase 3r §8 mark-price gap governance, or any other prior governance.
- Phase 4y does NOT modify `scripts/phase4x_c1_backtest.py` or rerun the backtest.
- Phase 4y does NOT use Phase 4x forensic numbers as tuning input.
- Phase 4y does NOT authorize Phase 4z or any successor phase.

## Full rejection topology after C1

| Strategy | Failure mode | Evidence type | Rescue trap |
| --- | --- | --- | --- |
| **R2** | Cost-fragility | Mechanism generated; cost survival failed | Cheaper-cost / relaxed §11.6 |
| **F1** | Catastrophic-floor / bad full-population expectancy | Mechanism generated; framework failed | Profitable-subset mining |
| **D1-A** | Mechanism / framework mismatch | Partial mechanism PASS; framework FAIL | Funding + extra filters / D1-A-prime |
| **V2** | Design-stage incompatibility | Zero trades; non-evidence-generating | Wider stops / V2-prime |
| **G1** | Regime-gate-meets-setup intersection sparseness | Zero qualifying trades; non-evidence-generating | Classifier relaxation / G1-prime |
| **C1** | **fires-and-loses / contraction anti-validation** | **Plenty of trades; negative expectancy; negative differentials vs three baselines (CI strictly negative)** | **C1-prime / threshold amendment / contraction-variant mining** |

**Six categorically distinct failure modes** in the project's strategy-research record. C1 is the project's first **evidence-generating negative result with multi-baseline anti-validation** — stronger evidence against the hypothesis than zero-trade non-evidence-generating failures.

## C1 result recap

```text
Verdict: C — C1 framework HARD REJECT
Best variant: id=21, label=B=0.10|C=0.45|N=12|S=0.10|T=2.0
Binding driver:
  CFP-2: BTC OOS HIGH train-best mean_R = -0.3633 <= 0
Co-binding drivers:
  CFP-3: profit_factor = 0.4413 < 0.50; max_drawdown_R = 54.55 > 10R
  CFP-6: DSR = -20.8173 <= 0
CFPs that did NOT trigger:
  CFP-1 (149 trades; 0/32 variants below 30);
  CFP-4 (BTC fail AND ETH fail; no rescue);
  CFP-5 (train HIGH already negative);
  CFP-7 (max-month fraction 7.4%);
  CFP-8 (worst sensitivity degrade 0.155R);
  CFP-9 (transition rate 3.33; 100% pass fraction);
  CFP-10 / CFP-11 / CFP-12 (all forbidden-input audit counters 0).

BTCUSDT primary (train-best variant 21):
  BTC OOS HIGH: n=149; mean_R=-0.3633; total_R=-54.1258;
                max_dd_R=54.55; PF=0.4413; sharpe=-0.3721
  All 32 BTC OOS HIGH variants loss-making.
  Loss-making at all OOS cost cells:
    LOW=-0.1701; MEDIUM=-0.2529; HIGH=-0.3633.
  Cost is NOT the binding driver.

ETHUSDT comparison (same train-best variant 21):
  ETH OOS HIGH: n=109; mean_R=-0.2140; PF=0.6252; sharpe=-0.2148
  All 32 ETH OOS HIGH variants loss-making.
  ETH cannot rescue BTC.

Mechanism checks:
  M1 FAIL: diff=-0.2440R; CI=[-0.4101, -0.0810] strictly negative
  M2.a FAIL: diff=-0.2201R; CI=[-0.3859, -0.0556] strictly negative
  M2.b FAIL: diff=-0.2930R
  M3 FAIL: BTC OOS HIGH mean_R<0; CFP-2/3 trigger;
           opportunity-rate floors PASS
  M4 FAIL: ETH differential=-0.1589; ETH cannot rescue BTC
  M5 DIAGNOSTIC_ONLY: skipped per Phase 4w optional

Search-space control:
  PBO_train_validation = 0.375 (below 0.50)
  PBO_train_oos = 0.219 (below 0.50)
  PBO_cscv = 0.094 (below 0.50)
  DSR (train-best, N=32) = -20.8173 (CFP-6 triggers via DSR)

Opportunity-rate:
  total_30m_bars = 30,672
  oos_total_transitions = 213
  transition_rate_per_480_bars = 3.33
  train-best OOS HIGH executed trades = 149
  variants with >= 30 BTC OOS HIGH trades = 32 / 32 (100.0%)
  CFP-1 NOT triggered. CFP-9 NOT triggered.
```

## C1 categorical failure mode

```text
Topology label: fires-and-loses / contraction anti-validation
```

C1 did NOT fail at the trade-count layer (149 trades), the opportunity-rate layer (rate 3.33 / 480 bars), the cost layer (LOW also negative), the variant-grid layer (PBO < 0.50 across all three horizons), or the methodology layer (CFPs 10-12 clean). **C1 failed at the edge layer**: the core contraction-tied transition claim performed worse than three independent baselines (non-contraction, always-active-same-geometry, delayed-breakout) with bootstrap CI strictly negative on M1 and M2.a. This is **stronger** evidence against the first-spec than V2 / G1 zero-trade non-evidence-generating failures because the mechanism actually generated a sample and was empirically anti-validated.

## Comparison with V2 and G1

- **V2 (Phase 4l):** failed before trades due to stop-distance / setup-geometry incompatibility (CFP-1 critical; 0 BTC OOS HIGH trades).
- **G1 (Phase 4r):** failed before trades due to regime-gate / entry-rule sparse intersection (CFP-1 critical + CFP-9 independent; 0 active-regime qualifying trades).
- **C1 (Phase 4x):** generated trades, passed opportunity-rate floors, and still lost (149 trades; mean_R = -0.3633; multi-baseline anti-validation).

V2 and G1 were structural non-evidence-generating failures. C1 is an evidence-generating negative result. Therefore **C1 cannot be rescued by appealing to the V2 / G1 lesson "avoid zero trades"** — C1 already avoided zero trades, and the resulting evidence is *more* damning.

## Comparison with R2, F1, and D1-A

- **R2:** cost-survival FAIL (§11.6 HIGH blocks). C1 differs because cost is not the binding driver (LOW also negative).
- **F1:** catastrophic-floor / bad full-population expectancy (CFP-1-equivalent triggered 5×; M2 FAIL/weak; M3 PASS-isolated). C1 resembles F1 in generating a population large enough to evaluate, but C1's failure is multi-baseline anti-validation rather than catastrophic-floor predicates dominating.
- **D1-A:** mechanism / framework mismatch (M1 BTC h=32 PASS; cond_i / cond_iv FAIL). C1 differs because its core mechanism checks failed *directly* with strictly negative bootstrap CIs, rather than passing partial mechanism checks while failing framework conditions.

## Reusable insights

Phase 4y compiled twelve reusable insights:

1. Opportunity-rate viability is necessary but not sufficient.
2. Negative baselines are mandatory for any future hypothesis.
3. A local precondition can avoid G1-style sparsity while still being anti-predictive.
4. Sample viability and edge viability are distinct.
5. "Not zero trades" is not success.
6. HIGH-cost survival cannot rescue negative gross structure.
7. Every future hypothesis must explain why its primary condition should outperform an unconditioned baseline.
8. Every future hypothesis must define the closest non-hypothesis baseline before any data is touched.
9. Baseline differentials may be more important than raw mean_R.
10. DSR / PBO / CSCV can show "not overfit" while still confirming "no edge."
11. First-spec hard rejections should not be mined for second-spec thresholds.
12. Remain-paused gains more weight after multiple independent failure modes.

## Forbidden rescue interpretations

**C1 rescue:** no C1-prime / C1-extension / C1-narrow / C1 hybrid; no C1 with tuned thresholds from Phase 4x; no different N_comp / C_width / B_width / S_buffer / T_mult chosen from Phase 4x outputs; no volume / funding / HTF / ATR-stop-distance gate added post hoc; no mark-price / aggTrades / spot / cross-venue / order-book rescue; no using Phase 4x forensic results as tuning input; no C1 rerun; no C1 implementation in `src/prometheus/`; no Phase 4v amendment; no Phase 4w methodology amendment.

**Cross-strategy rescue:** no V2-prime / V2-narrow / V2-relaxed / V2 hybrid; no G1-prime / G1-narrow / G1-extension / G1 hybrid; no R2 cheaper-cost rescue; no F1 profitable-subset rescue; no D1-A extra-filter / D1-A-prime / D1-B / V1-D1 / F1-D1 hybrid; no 5m strategy from Q1–Q7 findings; no immediate ML / market-making / HFT; no paper / shadow / live; no Phase 4 canonical; no data acquisition as next step.

## Recommended next operator choice

- **Option A — primary recommendation: remain paused.** Strongest-evidence position given six terminal negative outcomes.
- **Option B — conditional secondary: docs-only post-rejection research-process redesign / hypothesis-discovery process redesign memo (only if separately authorized; not started by this merge).**
- **Option C — conditional tertiary: docs-only documentation-refresh memo (only if separately authorized).**
- Option D — strategy-agnostic implementation-readiness scoping memo NOT recommended (binding constraint is strategy evidence, not infrastructure).
- Option E — fresh-hypothesis discovery memo NOT recommended now.
- Option F — REJECTED: any C1 / V2 / G1 / R2 / F1 / D1-A rescue.
- Option G — REJECTED: immediate new strategy spec / backtest / implementation / data acquisition.
- Option H — FORBIDDEN: paper / shadow / live / exchange-write / Phase 4 canonical / production keys / MCP / Graphify / `.mcp.json` / credentials.

**Phase 4z and any successor phase are NOT authorized by Phase 4y.**

## Commands run

```text
git status                                          (clean except gitignored)
git rev-parse main                                  a24ee9298f52e4289e1c56b23fc9b762a850ca4b
git rev-parse origin/main                           a24ee9298f52e4289e1c56b23fc9b762a850ca4b
git checkout -b phase-4y/post-c1-strategy-research-consolidation
                                                    Switched to new branch
.venv/Scripts/python --version                      Python 3.12.4
.venv/Scripts/python -m ruff check .                All checks passed!
.venv/Scripts/python -m pytest -q                   785 passed in 16.06s
.venv/Scripts/python -m mypy                        Success: no issues in 82 source files
git add docs/00-meta/implementation-reports/2026-04-30_phase-4y_post-c1-strategy-research-consolidation.md
git commit -F .git/PHASE_4Y_COMMIT_MSG              Phase 4y memo committed (e0c4c73)
git push -u origin phase-4y/post-c1-strategy-research-consolidation
                                                    Branch pushed; tracking origin
```

## Verification results

```text
ruff check .                : All checks passed!
pytest                      : 785 passed in 16.06s (no regressions)
mypy strict                 : Success: no issues in 82 source files

Phase 4y memo line count    : 586 lines (single new file)

No source code modified.
No tests modified.
No scripts modified.
No data acquired or modified.
No manifests modified.
No v003 created.
No retained verdicts revised.
No project locks changed.
```

## Commit

```text
Phase 4y memo commit:
  SHA: e0c4c73
  Title: phase-4y: post-C1 strategy research consolidation memo (docs-only)
  Files: docs/00-meta/implementation-reports/2026-04-30_phase-4y_post-c1-strategy-research-consolidation.md (new; 586 lines)

Phase 4y closeout commit:
  SHA: <recorded after this file is committed>
```

## Final git status

```text
On branch phase-4y/post-c1-strategy-research-consolidation
Untracked files (gitignored transients only):
  .claude/scheduled_tasks.lock
  data/research/
nothing added to commit but untracked files present
```

## Final git log --oneline -5

Recorded after the closeout commit and push.

## Final rev-parse

```text
HEAD                                                              <recorded after closeout commit>
origin/phase-4y/post-c1-strategy-research-consolidation           <recorded after closeout push>
main                                                              a24ee9298f52e4289e1c56b23fc9b762a850ca4b (unchanged)
origin/main                                                       a24ee9298f52e4289e1c56b23fc9b762a850ca4b (unchanged)
```

## Branch / main status

- Phase 4y branch: `phase-4y/post-c1-strategy-research-consolidation` (created from main; pushed to origin).
- main / origin/main: `a24ee9298f52e4289e1c56b23fc9b762a850ca4b` (unchanged; Phase 4y has not been merged).
- No merge to main is performed by Phase 4y (per authorization brief).

## Forbidden-work confirmation

Phase 4y did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`);
- run `scripts/phase4x_c1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create a new strategy candidate or named successor;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4z / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values;
- use Phase 4x C1 forensic numbers as tuning input.

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
                       binding; CFP-9 independent; terminal for G1 first-spec;
                       preserved)
C1                  : HARD REJECT (Phase 4x — Verdict C; CFP-2 binding;
                       CFP-3 / CFP-6 co-binding; CFP-1 / CFP-9 NOT
                       triggered; terminal for C1 first-spec; preserved
                       by Phase 4y consolidation)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price
                       stops (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved;
                              strategy-agnostic)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x
                            : all preserved verbatim
Phase 4y                    : Post-C1 strategy research consolidation memo
                              (this phase; new; docs-only; not merged)
Recommended state           : remain paused (primary);
                              docs-only post-rejection research-process
                              redesign memo (conditional secondary;
                              not authorized by Phase 4y)
```

## Next authorization status

```text
Phase 4z (any successor)         : NOT authorized
Phase 4 (canonical)              : NOT authorized
Paper / shadow                   : NOT authorized
Live-readiness                   : NOT authorized
Deployment                       : NOT authorized
Production-key creation          : NOT authorized
Authenticated REST               : NOT authorized
Private endpoints                : NOT authorized
User stream / WebSocket          : NOT authorized
Exchange-write capability        : NOT authorized
MCP / Graphify                   : NOT authorized
.mcp.json / credentials          : NOT authorized
C1 implementation                : NOT authorized; terminal-rejected
C1 rerun                         : NOT authorized; terminal-rejected
C1 spec amendment                : NOT authorized; FORBIDDEN
Phase 4w methodology amendment   : NOT authorized; FORBIDDEN
G1 / V2 / R2 / F1 / D1-A rescue  : NOT authorized; FORBIDDEN
G1-prime / G1-extension axes     : NOT authorized; FORBIDDEN
V2-prime / V2-variant            : NOT authorized; FORBIDDEN
C1-prime / C1-extension          : NOT authorized; FORBIDDEN
Retained-evidence rescue         : NOT authorized; FORBIDDEN
5m strategy / hybrid             : NOT authorized; not proposed
ML feasibility                   : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                                 : NOT authorized; data unavailable
Mark-price / aggTrades / spot / cross-venue acquisition
                                 : NOT authorized; FORBIDDEN
Fresh-hypothesis discovery memo  : NOT authorized
Research-process redesign memo   : NOT authorized; conditional secondary
                                   in operator decision menu
Documentation-refresh memo       : NOT authorized; conditional tertiary
Strategy-agnostic implementation-
  readiness scoping memo          : NOT authorized; conditional quaternary
```

The next step is operator-driven: the operator decides whether to remain paused (primary) or authorize a docs-only post-rejection research-process redesign memo (conditional secondary). Until then, the project remains at the post-Phase-4y consolidation boundary on the Phase 4y branch (not merged to main).

---

**Phase 4y is text-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. main remains unchanged at a24ee92. C1 first-spec remains terminally HARD REJECTED. Recommended state: remain paused. No next phase authorized.**
