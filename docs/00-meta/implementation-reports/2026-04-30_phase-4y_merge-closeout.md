# Phase 4y Merge Closeout

## Summary

Phase 4y (Post-C1 Strategy Research Consolidation Memo, docs-only) was merged into `main` via a `--no-ff` merge commit. Phase 4y is the project's third post-rejection consolidation memo (after Phase 4m for V2 and Phase 4s for G1) and the fifth overall (after Phase 3e for F1 and Phase 3k for D1-A). Phase 4y consolidated the Phase 4x C1 backtest outcome (Verdict C HARD REJECT; binding driver CFP-2; co-binding CFP-3 / CFP-6) into the project's strategy-research record; updated the rejection topology with C1's distinct failure mode (**fires-and-loses / contraction anti-validation**, NEW); preserved every retained verdict and project lock verbatim; extracted twelve reusable insights; explicitly forbade C1 rescue and cross-strategy rescue interpretations; and recommended remain-paused as primary with a docs-only post-rejection research-process redesign memo as conditional secondary (not started by this merge). **Phase 4y was docs-only.** No new strategy candidate was created; no fresh-hypothesis discovery memo was authored; no strategy-spec or backtest-plan memo was authored; no backtest was run; no Phase 4x rerun occurred; `scripts/phase4x_c1_backtest.py` was NOT modified; no implementation code was written; no data was acquired or modified; no manifest was modified; no verdict was revised; no project lock was changed. Whole-repo quality gates remain clean (ruff PASS; pytest 785 PASS; mypy strict 0 issues across 82 source files). **No successor phase authorized.**

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4y_post-c1-strategy-research-consolidation.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4y_closeout.md                                 (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4y_merge-closeout.md                           (new; this file)
docs/00-meta/current-project-state.md                                                               (narrow Phase 4y sync)
```

No source under `src/prometheus/` modified. No tests modified. No scripts modified. No data, manifests, or `.gitignore` modified.

## Phase 4y commits included

```text
e0c4c73  phase-4y: post-C1 strategy research consolidation memo (docs-only)
46c7fe3  phase-4y: closeout (post-C1 consolidation memo)
```

## Merge commit

```text
SHA:    69579c15f4ddc15cf79edbf22a67daa84a43f765
Title:  Merge Phase 4y (post-C1 strategy research consolidation memo, docs-only) into main
Type:   --no-ff merge of phase-4y/post-c1-strategy-research-consolidation into main
```

## Housekeeping commit

The merge-closeout file (this file) and the narrow Phase 4y sync to `docs/00-meta/current-project-state.md` are committed as a single docs-only housekeeping commit on `main` after the merge. The housekeeping commit SHA is recorded below in `Final git log --oneline -8`.

## Final git status

```text
On branch main
Your branch is up to date with 'origin/main'.

Untracked files (gitignored transients only; not committed):
  .claude/scheduled_tasks.lock
  data/research/

nothing added to commit but untracked files present
```

## Final git log --oneline -8

Recorded after the housekeeping commit and push.

## Final rev-parse

Recorded after the housekeeping commit and push.

## main == origin/main confirmation

Confirmed at the housekeeping push step.

## Consolidation conclusion

- **Phase 4y was docs-only.**
- Phase 4y consolidated the Phase 4x C1 hard reject into the project's strategy-research record.
- Phase 4y did NOT create a new strategy.
- Phase 4y did NOT authorize Phase 4z.
- Phase 4y did NOT authorize backtest, implementation, data acquisition, paper / shadow / live, or exchange-write.
- **No retained verdict is revised.**
- **No project lock is changed.**
- **Recommended state remains paused.**

## Relationship to Phase 4x

- Phase 4x executed the first C1 backtest exactly under Phase 4w methodology.
- Phase 4x verdict was **C — C1 framework HARD REJECT.**
- Phase 4x recommendation was: Option A — remain paused (primary); Option B — Phase 4y consolidation memo (conditional secondary).
- The operator separately authorized Phase 4y on the conditional-secondary path.
- Phase 4y does NOT modify Phase 4x evidence or `scripts/phase4x_c1_backtest.py`.

## Full rejection topology after C1

| Strategy | Failure mode | Evidence type | Rescue trap |
| --- | --- | --- | --- |
| **R2** | **Cost-fragility** | Mechanism generated; cost survival failed | Cheaper-cost / relaxed §11.6 |
| **F1** | **Catastrophic-floor / bad full-population expectancy** | Mechanism generated; framework failed | Profitable-subset mining |
| **D1-A** | **Mechanism / framework mismatch** | Partial mechanism PASS; framework FAIL | Funding + extra filters / D1-A-prime |
| **V2** | **Design-stage incompatibility / zero trades** | Non-evidence-generating | Wider stops / V2-prime |
| **G1** | **Regime-gate-meets-setup intersection sparseness / zero qualifying trades** | Non-evidence-generating | Classifier relaxation / G1-prime |
| **C1** | **fires-and-loses / contraction anti-validation** | Plenty of trades; negative expectancy; negative differentials vs three baselines (CI strictly negative on M1 and M2.a) | C1-prime / threshold tuning / contraction-variant mining |

**Six categorically distinct failure modes** in the project's strategy-research record.

## C1 result recap

```text
Verdict: C — C1 framework HARD REJECT
Best variant: id=21 (label B=0.10|C=0.45|N=12|S=0.10|T=2.0)

Binding driver:
  CFP-2: BTC OOS HIGH train-best mean_R = -0.3633 <= 0
Co-binding drivers:
  CFP-3: profit_factor=0.4413 < 0.50; max_dd_R=54.55 > 10R
  CFP-6: DSR=-20.8173 <= 0

CFPs that did NOT trigger:
  CFP-1 (149 trades; 0/32 variants below 30);
  CFP-9 (transition rate 3.33; 100% pass fraction);
  CFP-4 / 5 / 7 / 8 / 10 / 11 / 12 (all clean).

BTCUSDT primary:
  trade_count=149; mean_R=-0.3633; PF=0.4413; sharpe=-0.3721
  All 32 BTC OOS HIGH variants loss-making.
  Loss-making at all OOS cost cells:
    LOW=-0.1701; MEDIUM=-0.2529; HIGH=-0.3633.
  Cost is NOT the binding driver.

ETHUSDT comparison:
  trade_count=109; mean_R=-0.2140; PF=0.6252; sharpe=-0.2148
  All 32 ETH OOS HIGH variants loss-making.
  ETH cannot rescue BTC.
```

## C1 categorical failure mode

```text
Topology label: fires-and-loses / contraction anti-validation
```

- C1 generated enough trades (149 BTC OOS HIGH; transition rate 3.33 per 480 bars; 100% of variants ≥ 30 trades).
- C1 passed opportunity-rate floors (CFP-1 / CFP-9 NOT triggered).
- C1 failed expectancy (BTC OOS HIGH mean_R = -0.3633; CFP-2 binding).
- C1 underperformed non-contraction baseline (-0.244R; CI strictly negative), always-active-same-geometry baseline (-0.220R; CI strictly negative), and delayed-breakout baseline (-0.293R).
- This is **stronger evidence against C1 first-spec than zero-trade failure** because the mechanism actually generated a sample and was empirically anti-validated against three independent baselines.

## Comparison with V2 and G1

- **V2 (Phase 4l):** zero-trade non-evidence-generating failure from stop-distance / setup-geometry incompatibility (CFP-1 critical; 0 BTC OOS HIGH trades).
- **G1 (Phase 4r):** zero-trade non-evidence-generating failure from regime-gate / entry-rule sparse intersection (CFP-1 critical + CFP-9 independent; 0 active-regime qualifying trades).
- **C1 (Phase 4x):** evidence-generating negative result. C1 cannot be rescued by appealing to "avoid zero trades" because **C1 already avoided zero trades**.

## Comparison with R2, F1, and D1-A

- **C1 differs from R2** because cost is not the binding driver — C1 is structurally loss-making before HIGH cost amplification (LOW also negative).
- **C1 resembles F1** in being an evidence-generating expectancy failure (both produced sample populations large enough to be statistically informative and both had negative full-population expectancy).
- **C1 differs from D1-A** because C1's core mechanism checks (M1, M2.a, M2.b, M3, M4) directly failed with strictly negative bootstrap CIs, rather than partially passing mechanism while failing framework conditions.

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

- **C1 rescue:** no C1-prime / extension / narrow / hybrid; no C1 threshold tuning; no post-hoc volume / funding / HTF / ATR gate; no C1 rerun; no C1 implementation; no C1 spec or methodology amendment.
- **Cross-strategy rescue:** no V2 / G1 / R2 / F1 / D1-A rescue.
- **Other forbidden:** no 5m strategy; no immediate ML / HFT; no data acquisition; no paper / shadow / live; no Phase 4 canonical.

## Recommended next operator choice

- **Option A — primary recommendation: remain paused.**
- **Option B — conditional secondary:** docs-only post-rejection research-process redesign / hypothesis-discovery process redesign memo (only if separately authorized; not started by this merge).
- **Option C — conditional tertiary:** docs-only documentation-refresh memo (only if separately authorized).
- **Option D — NOT recommended:** docs-only strategy-agnostic implementation-readiness scoping memo (only if separately authorized).

**Phase 4z is NOT started by this merge.** Immediate new strategy / backtest / implementation / data acquisition is rejected. Paper / shadow / live / exchange-write is forbidden. Phase 4 canonical is forbidden.

## Verification evidence

```text
ruff check .                : All checks passed!
pytest                      : 785 passed (no regressions)
mypy strict                 : Success: no issues in 82 source files
```

## Forbidden-work confirmation

Phase 4y (and this merge) did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`);
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
V2                  : HARD REJECT (Phase 4l terminal; preserved)
G1                  : HARD REJECT (Phase 4r terminal; preserved)
C1                  : HARD REJECT (Phase 4x terminal; preserved by Phase 4y)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price
                       stops (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved;
                              strategy-agnostic)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x
                            : all preserved verbatim
Phase 4y                    : Post-C1 strategy research consolidation
                              memo (this phase; merged to main; docs-only)
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
  readiness scoping memo          : NOT authorized; not recommended
```

The next step is operator-driven: the operator decides whether to remain paused (primary) or authorize a docs-only post-rejection research-process redesign memo (conditional secondary). Until then, the project remains at the post-Phase-4y consolidation boundary on `main`.

---

**Phase 4y is docs-only and has been merged into `main`. No source code, tests, scripts, data, manifests, or successor phases were created or modified. No retained verdict revised. No project lock changed. C1 first-spec remains terminally HARD REJECTED. Recommended state: remain paused. No next phase authorized.**
