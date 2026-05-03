# Phase 4m — Post-V2 Strategy Research Consolidation Memo

**Authority:** Operator authorization for Phase 4m (Phase 4l §"Operator
decision menu" Option B conditional secondary alternative: docs-only
post-V2 research consolidation memo, analogous to Phase 3e (post-F1)
or Phase 3k (post-D1-A) precedents); Phase 4l (V2 backtest execution
verdict C HARD REJECT); Phase 4k (V2 backtest-plan methodology); Phase
4j §11 (metrics OI-subset partial-eligibility binding rule); Phase 4i
(V2 acquisition + integrity validation); Phase 4h (V2 data-requirements
/ feasibility); Phase 4g (V2 strategy spec); Phase 4f (V2 hypothesis
predeclaration); Phase 4e (reconciliation-model design memo); Phase 4d
(post-4a/4b/4c review); Phase 4a (local safe runtime foundation);
Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8
(break-even / EMA slope / stagnation governance); Phase 3r §8
(mark-price gap governance); Phase 3t (5m research thread closure);
Phase 3u (implementation-readiness boundary review); Phase 3p §4.7
(strict integrity gate semantics); Phase 3o §6 / §10 (predeclared
question forms; analysis boundary); Phase 3k (post-D1-A consolidation
memo); Phase 3l (external execution-cost evidence review); Phase 3j
(D1-A first execution + framework verdict); Phase 3h §11.2 (D1-A
MECHANISM PASS / FRAMEWORK FAIL — other); Phase 3e (post-F1
consolidation memo); Phase 3d-B2 (F1 first execution + HARD REJECT);
Phase 3c §7.3 (catastrophic-floor predicate); Phase 2w §16.1 (R2 §11.6
cost-sensitivity FAIL); Phase 2p §C.1 (R3 baseline-of-record); Phase
2i §1.7.3 (project-level locks);
`docs/03-strategy-research/v1-breakout-strategy-spec.md`;
`docs/03-strategy-research/v1-breakout-backtest-plan.md`;
`docs/05-backtesting-validation/v1-breakout-validation-checklist.md`;
`docs/04-data/data-requirements.md`;
`docs/04-data/timestamp-policy.md`;
`docs/04-data/dataset-versioning.md`;
`docs/07-risk/stop-loss-policy.md`;
`docs/07-risk/position-sizing-framework.md`;
`docs/07-risk/exposure-limits.md`;
`docs/12-roadmap/phase-gates.md`;
`docs/12-roadmap/technical-debt-register.md`;
`docs/00-meta/ai-coding-handoff.md`;
`docs/00-meta/implementation-ambiguity-log.md`;
`.claude/rules/prometheus-core.md`;
`.claude/rules/prometheus-safety.md`;
`.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4m — **Post-V2 Strategy Research Consolidation Memo**
(docs-only). Reviews all Prometheus strategy research attempted so
far, consolidates why each strategy / spec failed or was retained,
distinguishes reusable lessons from forbidden post-hoc rescue
observations, and defines what a genuinely new future hypothesis
must satisfy. **Phase 4m does NOT propose or authorize a new strategy
spec, backtest, implementation, data acquisition, or parameter
amendment. Phase 4m is text-only.**

**Branch:** `phase-4m/post-v2-strategy-research-consolidation`. **Memo
date:** 2026-05-02 UTC.

---

## Summary

Phase 4m is a retrospective research consolidation. It surveys the
project's complete strategy-research arc — H0 / R3 baseline-of-record,
R1a / R1b-narrow / R2 retained research evidence, F1 HARD REJECT, D1-A
MECHANISM PASS / FRAMEWORK FAIL — other, the 5m diagnostic thread,
and now V2 HARD REJECT under Phase 4l — and consolidates what was
learned, what cannot be salvaged without violating the Phase 3t §12
validity gate, and what conditions a genuinely new future ex-ante
hypothesis must satisfy.

**Key consolidation findings:**

- **Eight retained-evidence strategy lines have been tested.** None
  is currently a live-deployable candidate. R3 remains baseline-of-
  record; H0 remains framework anchor; R1a, R1b-narrow, R2, F1, D1-A
  are retained research evidence only; V2 first-spec is HARD REJECT.
- **Each rejection had a different mechanism:** R2 failed §11.6
  cost-sensitivity (Phase 2w §16.1); F1 hard-rejected on Phase 3c
  §7.3 catastrophic-floor (negative expectancy + cost-overwhelmed
  TARGET subset, Phase 3d-B2); D1-A framework-failed despite
  mechanism-pass (cond_i BTC MED expR > 0 FAILED + cond_iv BTC HIGH
  cost-resilience FAILED, Phase 3h §11.2 / Phase 3j); V2 hard-rejected
  on a structural CFP-1 critical (V1-inherited 0.60–1.80 × ATR
  stop-distance filter incompatible with V2's 20/40-bar Donchian
  setup; 0 trades produced, Phase 4l).
- **Cost realism is non-negotiable.** §11.6 = 8 bps HIGH per side
  (preserved verbatim from Phase 2w §16.1) blocked R2; subordinated
  D1-A; cannot be relaxed.
- **Mechanism evidence is necessary but not sufficient for framework
  promotion.** F1 had M3 PASS-isolated (TARGET subset profitable);
  D1-A had M1 PASS, M3 PASS-isolated; V2 produced too few trades to
  evaluate M1/M2/M3. None of these mechanism findings rescued the
  framework — each strategy still failed at the framework level.
- **Setup geometry interacts non-trivially with stop / target /
  sizing.** V2's structural CFP-1 critical exposes a co-design
  failure: a longer setup window naturally produces wider structural
  stops, which interact with the V1-inherited stop-distance filter
  to reject all candidates. **The lesson is that setup window,
  structural stop, target model, and position sizing must be
  co-designed; they cannot be inherited piecewise from a different
  strategy.**

**Phase 4m does NOT:**

- propose or authorize a new strategy spec (no V3, no
  V2-prime / -narrow / -relaxed, no V1/D1 hybrid, no F1/D1 hybrid);
- propose or authorize a Phase 4g / Phase 4j §11 / Phase 4k
  methodology amendment;
- propose or authorize stop-distance bound revision, N1 axis
  revision, threshold-grid revision, or any other Phase 4l-result-
  driven optimization;
- run or authorize any backtest, diagnostic, or data acquisition;
- modify any retained-evidence verdict;
- modify any project lock, threshold, or governance rule;
- authorize fresh-hypothesis research (an explicit future operator
  decision is required);
- authorize Phase 4 canonical, paper / shadow, live-readiness, or
  exchange-write.

**Phase 4m IS:** a written record of what the project has learned
and what conditions must be satisfied before the project ever again
considers strategy research, so that any future authorization is
grounded in the cumulative evidence rather than rhetorical drift
toward the most recent failure mode's inverse.

**Recommended next operator choice:** **Option A (remain paused)
primary**; **Option B (authorize a separate docs-only fresh-hypothesis
discovery memo)** conditional secondary, only if the operator
explicitly chooses to continue research after consolidation. No
further options recommended.

**Verification (run on the post-Phase-4l-merge tree, captured by
Phase 4m):**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**No project lock changed.** §1.7.3 / §11.6 / mark-price stops / v002
verdict provenance — all preserved verbatim. **Phase 4j §11 metrics
OI-subset rule: not modified.** **Phase 4k methodology: not modified.**
**Phase 4g V2 strategy spec: not modified.** **R3 baseline-of-record;
H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained
research evidence: all preserved verbatim.**

**Recommended state remains paused. No next phase authorized.**

---

## Authority and boundary

Phase 4m operates strictly inside the post-Phase-4l-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10;
  Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t
  consolidation; Phase 3u §10 / §11; Phase 3v §8; Phase 3w §6 / §7 /
  §8; Phase 4a's anti-live-readiness statement; Phase 4d review;
  Phase 4e reconciliation-model design memo; Phase 4f V2 hypothesis
  predeclaration; Phase 4g V2 strategy spec; Phase 4h V2
  data-requirements / feasibility memo; Phase 4i V2 acquisition +
  integrity validation; Phase 4j §11 metrics OI-subset
  partial-eligibility rule; Phase 4k V2 backtest-plan methodology;
  Phase 4l V2 backtest execution.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md`
  unchanged.
- **Project-level locks preserved verbatim.** §1.7.3.
- **Phase 2f thresholds preserved verbatim.** §11.6 = 8 bps HIGH per
  side.
- **Retained-evidence verdicts preserved verbatim.** R3 / H0 / R1a /
  R1b-narrow / R2 / F1 / D1-A; **V2 HARD REJECT (Phase 4l, terminal
  for V2 first-spec)**.
- **Safety rules preserved verbatim.**
- **MCP and secrets rules preserved verbatim.**

Phase 4m adds *only* a docs-only retrospective consolidation memo,
without modifying any prior phase memo, any data, any code under
`src/prometheus/`, any rule, any threshold, any manifest, any verdict,
any lock, or any gate.

---

## Starting state

```text
branch:           phase-4m/post-v2-strategy-research-consolidation
parent commit:    74bc2397f4d3f87025f41844f853054acf8d12d0 (post-Phase-4l-merge housekeeping)
working tree:     clean before memo authoring (transient .claude/scheduled_tasks.lock + gitignored data/research/ excluded)
main:             74bc2397f4d3f87025f41844f853054acf8d12d0 (unchanged)

Phase 4a foundation:                                          merged.
Phase 4b/4c cleanup:                                          merged.
Phase 4d review:                                              merged.
Phase 4e reconciliation-model design memo:                    merged.
Phase 4f V2 hypothesis predeclaration:                        merged.
Phase 4g V2 strategy spec:                                    merged.
Phase 4h V2 data-requirements / feasibility memo:             merged.
Phase 4i V2 public data acquisition + integrity:              merged (partial-pass; metrics not eligible).
Phase 4j V2 metrics data governance memo:                     merged (Phase 4j §11 binding).
Phase 4k V2 backtest-plan memo:                               merged.
Phase 4l V2 backtest execution:                               merged (Verdict C HARD REJECT, terminal for V2 first-spec).

Repository quality gate:           fully clean.
research thread (5m):              operationally complete and closed (Phase 3t).
v002 datasets:                     locked; manifests untouched.
v001-of-5m datasets:               trade-price research-eligible; mark-price research_eligible:false.
Phase 4i datasets:                 30m + 4h klines × 2 research-eligible; metrics × 2 NOT research-eligible.
```

---

## Why this memo exists

Phase 4l Verdict C HARD REJECT for V2 first-spec is the seventh major
strategy-research rejection in Prometheus's history (counting the V1
arc terminal at R3 as a partial pass with R1a / R1b-narrow / R2 as
retained evidence; F1 as one rejection; D1-A as one rejection; the 5m
diagnostic thread as descriptive-only; and V2 as the most recent).
The cumulative pattern matters more than any single rejection in
isolation:

- **Each new strategy was a deliberate ex-ante hypothesis.** F1, D1-A,
  and V2 each predeclared their hypotheses (Phase 3a, Phase 3f, Phase
  4f) with bounded feature sets, threshold grids, and validation
  methodology before any data was touched. This discipline came from
  Bailey / Borwein / López de Prado / Zhu (2014) data-snooping
  literature and from the project's own Phase 3o predeclared 5m
  diagnostic question set.
- **Each rejection illuminates a different boundary of the strategy
  space.** R2 — costs at HIGH-slip kill marginal expectancy. F1 —
  isolated profitable subsets do not rescue a losing whole. D1-A —
  funding-as-trigger fails even when funding-as-context contains
  information. V2 — setup geometry and stop model can invalidate a
  strategy at the design stage, before expectancy is even testable.
- **The cumulative evidence is not "we keep failing for the same
  reason"; it is "we have systematically explored four orthogonal
  rejection modes."** Each mode, once recognized, becomes a
  constraint on any future hypothesis.

Without consolidation, the project risks rhetorical drift in two
directions:

- **Toward V2 rescue.** "V2 had raw candidates! Just widen the
  stop-distance filter and rerun!" — this is exactly the Phase 4k
  / Phase 4l forbidden-rescue pattern. Widening a stop-distance
  filter in response to an observed 0-trade outcome is post-hoc
  optimization (Bailey et al. 2014).
- **Toward fresh-hypothesis pressure.** "We've spent so much effort;
  surely there's something we can deploy." — this risks committing
  to a new direction before the cumulative evidence is properly
  understood.

Phase 4m exists to close the loop: write down what the project has
learned, what cannot be salvaged, and what conditions a future
hypothesis must satisfy. Without this memo, every future operator
decision risks being driven by the most recent failure mode's
opposite rather than by the cumulative evidence.

This is the same retrospective discipline applied at Phase 3e
(post-F1) and Phase 3k (post-D1-A) — each phase consolidated lessons
before moving to the next research direction.

---

## Relationship to Phase 4l

Phase 4l (merged at `918b10a6...` with housekeeping at `74bc2397...`)
delivered three artefacts:

1. The standalone V2 backtest script
   `scripts/phase4l_v2_backtest.py`.
2. The Phase 4l V2 backtest execution report.
3. The Phase 4l closeout artefact.

Phase 4l ran the predeclared 512-variant V2 backtest exactly under
Phase 4k methodology and emitted Verdict C HARD REJECT, with **CFP-1
critical** as the binding driver: 512 / 512 variants produced fewer
than 30 OOS trades on BTCUSDT; the BTC-train-best variant produced
0 OOS trades.

Phase 4l identified the structural root cause: V2's locked 20/40-bar
Donchian setup window per Phase 4g §29 axis 1 produces stop distances
of 3–5 × ATR(20), which exceed the V1-inherited 0.60–1.80 × ATR(20)
stop-distance filter per Phase 4g §19 / V1 §"Stop-distance filter".
Raw V2 candidates exist (~15 per variant per symbol over the 4-year
coverage from the 8-feature AND chain), but ALL are rejected by the
stop-distance filter before trade generation.

Phase 4l correctly classified this as analogous to F1's HARD REJECT
under Phase 3c §7.3 catastrophic-floor predicate.

Phase 4m does NOT modify Phase 4l. Phase 4l text remains verbatim.
Phase 4m consolidates Phase 4l's evidence into the cumulative
research-arc record without amending Phase 4l, Phase 4k, Phase 4j,
Phase 4g, or any other prior memo.

Phase 4m's central observation about V2:

- **V2 did not lose because trades had bad expectancy.**
- **V2 produced zero trades.**
- **The failure was at the design stage, not the data stage.**
- **The Phase 4l forensic finding is a methodology design lesson, not
  an authorization to rerun V2 with a relaxed filter.**

---

## Strategy research inventory

The project's complete strategy-research arc to date:

### Inventory table

| Strategy | Family | Core hypothesis | Tested timeframe / data basis | Final verdict | Main reason for rejection or retention | Mechanism evidence? | Cost-sensitivity blocker? | Stop / exit a driver? | Reusable as insight? | Direct continuation forbidden? |
|---|---|---|---|---|---|---|---|---|---|---|
| **H0** | V1 breakout (15m / 1h, EMA(50)/(200) bias, 8-bar setup, fixed-R + trailing) | Trend-continuation breakout from consolidation | BTCUSDT 15m / 1h v002 | **Framework anchor** (Phase 2i §1.7.3) | Reference framework for all V1 work | n/a (framework anchor) | n/a | n/a | yes (anchor) | n/a |
| **R3** | V1 breakout (fixed 2R take-profit + unconditional time-stop) | Simpler exit family beats staged management | BTCUSDT 15m / 1h v002 | **Baseline-of-record** (Phase 2p §C.1) | Cleanly promoted; survived all V1 validation gates | yes (M1 + M2 / M3) | passed §11.6 HIGH | yes (fixed-R + time-stop is the locked exit family) | yes (canonical exit framework) | n/a (R3 IS the live candidate, but no live deployment authorized) |
| **R1a** | V1 breakout + volatility-percentile setup predicate | Volatility regime gating improves breakout quality | BTCUSDT 15m / 1h v002 | **Retained research evidence** (non-leading) | Framework promotion did not improve over R3; non-leading | partial | partial | no (mostly entry-side) | yes (regime-gating insight) | yes (R1a as direct continuation forbidden) |
| **R1b-narrow** | V1 breakout + bias-strength magnitude threshold | Strong-trend filter improves entries | BTCUSDT 15m / 1h v002 | **Retained research evidence** (non-leading) | Same — framework non-leading | partial | partial | no | yes (bias-strength insight) | yes |
| **R2** | V1 breakout + pullback-retest entry | Pullback entry improves trade quality vs. breakout-bar entry | BTCUSDT 15m / 1h v002 | **FAILED — §11.6 cost-sensitivity blocks** (Phase 2w §16.1) | M1 ✓, M3 ✓, M2 ✗; slippage-fragile under HIGH cost | yes (M1 + M3 partial) | YES (binding) | yes (entry-style change shifted slippage exposure) | yes (cost lesson + entry-quality lesson) | yes (R2 with cheaper costs forbidden) |
| **F1** | Mean-reversion-after-overextension (15m, 8-bar cumulative displacement > 1.75 × ATR, SMA(8) target) | Overextension followed by mean reversion | BTCUSDT 15m v002 | **HARD REJECT** (Phase 3c §7.3 catastrophic-floor; Phase 3d-B2 terminal) | 5 separate violations across BTC/ETH × MED/HIGH; M1 BTC PARTIAL; M2 BTC FAIL / ETH weak-PASS; M3 PASS-isolated but TARGET subset overwhelmed by 53–54% STOP exits at −1R | yes (M3 PASS-isolated) | yes (HIGH-cell PF=0.22) | yes (stop-vs-target ratio insufficient for ~25–35% true win rate) | yes (mean-reversion family lesson) | yes (F1 with extra filters / F1-prime forbidden) |
| **D1-A** | Funding-aware contrarian directional (15m, 90-day funding-rate Z\|Z_F\|≥2.0, contrarian +2R fixed) | Extreme funding signals contrarian opportunity | BTCUSDT 15m v002 + funding | **MECHANISM PASS / FRAMEWORK FAIL — other** (Phase 3h §11.2; Phase 3j terminal) | M1 BTC h=32 PASS (mean +0.1748R); M2 FAIL on both symbols (~21× / ~11× below threshold); M3 PASS-isolated; cond_i BTC MED expR > 0 FAILED; cond_iv BTC HIGH cost-resilience FAILED | yes (M1 + M3 partial) | yes (BTC HIGH expR=−0.4755) | yes (1R stop + +2R fixed; ~30% empirical WR vs. ~51% breakeven) | yes (funding-as-trigger lesson) | yes (D1-A with extra filters / D1-A-prime / D1-B forbidden) |
| **5m diagnostics thread** | Diagnostic-only (Q1–Q7 predeclared) | Surface what 15m-bar dynamics hide | v001-of-5m supplemental | **Operationally complete and closed** (Phase 3t) | Q1 / Q2 / Q3 (+1R) / Q6 (D1-A) / Q7 INFORMATIVE; Q4 / Q5 NON-INFORMATIVE; Q3 ambiguous (+2R) | yes (descriptive-only) | n/a | n/a | yes (entry-path adverse bias; V1-vs-F1/D1A stop-pathology differentiation) | yes (Phase 3o §6 forbidden question forms; cannot become rules) |
| **V2** | Participation-confirmed trend continuation (30m signal, 4h bias, 1h session, 8 entry features + 3 exit / regime, 512-variant grid) | Trend-continuation under simultaneous price + volatility + participation + derivatives-flow alignment | BTCUSDT 30m / 4h / metrics OI subset / funding | **HARD REJECT** (Phase 4l, structural CFP-1 critical, terminal for V2 first-spec) | 0 trades produced; setup-vs-stop-distance-filter incompatibility; 8-feature AND chain produces ~15 raw candidates per variant per symbol but all rejected by V1-inherited 0.60–1.80 × ATR filter | n/a (0 trades; M1/M2/M3 not evaluable) | n/a (no trades to test) | YES (binding root cause) | yes (setup-stop-target co-design lesson) | yes (V2-prime / -narrow / -relaxed forbidden) |

### Inventory observations

- **Eight retained-evidence strategy lines.** None is currently a
  live-deployable candidate.
- **Verdict distribution:** 1 framework anchor (H0); 1
  baseline-of-record (R3); 2 retained non-leading (R1a, R1b-narrow);
  1 cost-failed retained (R2); 2 hard-rejected (F1, V2); 1 framework-
  failed (D1-A); 1 diagnostic-only closed (5m thread).
- **Symbol coverage:** all primary work on BTCUSDT; ETHUSDT used as
  cross-symbol comparison only (per §1.7.3).
- **Timeframe coverage:** 15m signal (V1 family + F1 + D1-A); 5m
  diagnostic-only; 30m signal (V2). 1m / sub-minute / tick not
  authorized.
- **Cost cells tested:** LOW (1 bp), MEDIUM (4 bps), HIGH (8 bps =
  §11.6 gate) for every strategy.
- **All strategy SHA-pinned to v002 datasets** (R3 / R1a / R1b-narrow /
  R2 / F1 / D1-A) or v001 30m+4h datasets (V2). Manifest immutability
  preserved.

---

## Consolidated verdict table

```text
┌──────────────┬────────────────────────────┬──────────────┬─────────────────────────────────────────────────────────┐
│ Strategy     │ Verdict                    │ Status       │ Cumulative role                                          │
├──────────────┼────────────────────────────┼──────────────┼─────────────────────────────────────────────────────────┤
│ H0           │ FRAMEWORK ANCHOR           │ locked        │ V1 reference; not deployed                              │
│ R3           │ BASELINE-OF-RECORD         │ locked        │ V1 canonical exit family; not deployed                  │
│ R1a          │ RETAINED — NON-LEADING     │ locked        │ regime-gating insight                                   │
│ R1b-narrow   │ RETAINED — NON-LEADING     │ locked        │ bias-strength insight                                   │
│ R2           │ FAILED — §11.6             │ locked        │ cost-sensitivity warning + entry-style insight          │
│ F1           │ HARD REJECT                │ locked        │ mean-reversion family lesson                            │
│ D1-A         │ MECHANISM PASS / FW FAIL   │ locked        │ funding-as-trigger lesson                               │
│ 5m thread    │ CLOSED (operationally)     │ locked        │ entry-path / stop-pathology / OI lag descriptive only   │
│ V2           │ HARD REJECT (CFP-1 crit)   │ locked        │ setup-stop-target co-design lesson                      │
└──────────────┴────────────────────────────┴──────────────┴─────────────────────────────────────────────────────────┘
```

**Phase 4m preserves every verdict above verbatim. No row above is
revised by Phase 4m.**

---

## H0 / R3 baseline recap

**H0** is the V1 breakout framework anchor (Phase 2e). It is the
reference design for the V1 family: 15m signal, 1h higher-timeframe
bias (EMA(50) / EMA(200), discrete comparison, EMA(50) rising vs. 3
1h bars earlier), 8-bar setup window with consolidation criterion,
breakout-bar entry, structural stop with 0.10 × ATR(20) buffer,
0.60 × ATR ≤ stop_distance ≤ 1.80 × ATR filter, and staged-management
exit family. H0 was used as the reference against which R1a, R1b-narrow,
R2, R3 were compared.

**R3** (Phase 2p §C.1) was Phase 2's cleanest framework promotion: a
fixed-R take-profit at 2R + unconditional 16-bar time-stop replaced
H0's staged-management exit. R3 survived all V1 validation gates
(Phase 2 §G), including §11.6 = 8 bps HIGH per side cost-sensitivity.
**R3 became the V1 breakout baseline-of-record.** No live deployment
was authorized then or now.

**R3 baseline-of-record is preserved verbatim by Phase 4m.** R3
remains the canonical reference for V1 framework completion. The
fact that V1 (R3) was promoted but never deployed reflects the
project's deliberate phase-gate discipline (Phase 4 canonical
unauthorized).

**H0 framework anchor is preserved verbatim by Phase 4m.** H0
remains the V1 framework reference. No H0 amendment is contemplated
or authorized.

**No live deployment of H0 or R3 is authorized.** This is unchanged
by Phase 4m.

---

## R1a / R1b-narrow recap

**R1a** is the V1 breakout framework with an additional
volatility-percentile setup predicate (Phase 2 §B): the breakout-bar's
ATR percentile must fall within a predeclared band. R1a was tested
against H0 / R3 and showed partial improvement on some sub-windows
but failed to consistently dominate R3 on the full validation set.
**R1a was retained as research evidence, non-leading.**

**R1b-narrow** is the V1 breakout framework with a bias-strength
magnitude threshold: the 1h EMA(50) trend strength (e.g., percentage
above EMA(200)) must exceed a predeclared minimum. R1b-narrow showed
similar partial improvement patterns but did not consistently dominate
R3. **R1b-narrow was retained as research evidence, non-leading.**

**R1a / R1b-narrow lessons:**

- **Setup-side regime gates can have signal information.** Both
  variants showed partial-window improvement, suggesting the
  underlying regime-gating ideas have some merit.
- **But neither beat R3 on the full validation set.** The regime
  gates reduced trade count without proportionally improving
  expectancy.
- **Cost sensitivity stayed within R3's band.** Neither failed
  §11.6 outright; they simply did not improve on R3.
- **Both are retained as research evidence only. Direct
  continuation (R1a-prime, R1b-prime, R1a hybrid) is forbidden.**

**Reusable insight:** regime gating may have value in a future
strategy that is *designed around* regime detection from the start,
rather than bolted onto an existing framework. This is NOT a license
for V2 / D1-A / F1 rescue with "added regime gates".

---

## R2 recap

**R2** is the V1 breakout framework with **pullback-retest entry**
instead of breakout-bar-close entry: after a confirmed breakout,
wait for a pullback to the broken level and enter on the
confirmation that the pullback held. R2 was tested against R3 across
the v002 multi-year coverage with §11.6 cost cells.

**Verdict (Phase 2w §16.1):** **R2 FAILED — §11.6 cost-sensitivity
blocks.**

- **M1 ✓**: pullback-retest entries exhibited the expected
  directional follow-through pattern.
- **M3 ✓**: regime decomposition showed retests in trending
  conditions outperformed breakout-bar entries.
- **M2 ✗**: but mechanism vs. degenerate variant — R2 minus the
  pullback-confirmation gate — did not show stat-significant
  expectancy uplift, and **most critically, R2 was slippage-fragile
  under HIGH-slip (8 bps per side per §11.6).**

R2's slippage fragility came from the entry-style change: pullback
entries occur at less liquid intra-trade-cycle moments, where realized
slippage tends to be higher, and the marginal expectancy is too thin
to absorb the higher cost.

**R2 is retained as research evidence only.** Phase 2w §16.1 verdict
is preserved verbatim by Phase 4m.

**R2 lessons:**

- **Mechanism evidence (M1 ✓ / M3 ✓) does NOT compensate for cost
  failure.** A strategy that "works" at LOW-slip and fails at HIGH-slip
  is structurally fragile to liquidity conditions that may worsen
  over time or in adverse regimes.
- **Entry style affects realized cost.** Different entry triggers
  (breakout-bar close vs. pullback-retest) interact with execution
  microstructure differently. Cost models must capture this.
- **§11.6 cost-sensitivity gate is necessary.** It blocked R2 from
  framework promotion; it would have blocked any future framework
  with similar marginal-expectancy / high-cost-fragility profile.
- **R2 with cheaper costs is forbidden as rescue.** The §11.6 = 8 bps
  HIGH per side bound is locked (Phase 2w §16.1 / preserved by every
  subsequent phase). Relaxing cost assumptions to make R2 pass would
  be a rescue interpretation forbidden by the validity gate.

**Reusable insight:** any new strategy that uses pullback / retest
geometry must explicitly model the slippage interaction at signal
time, not assume V1 / R3 cost assumptions transfer. This is NOT a
license to rerun R2 at lower cost; it is a constraint on future
hypotheses.

---

## F1 recap

**F1** (Phase 3a–3d-B2) is the mean-reversion-after-overextension
strategy on BTCUSDT 15m: when the 8-bar cumulative absolute
displacement exceeds 1.75 × ATR(20) and the price has stretched away
from the 8-bar SMA, enter contrarian (long after a sharp downward
move; short after a sharp upward move) with a structural stop and an
8-bar unconditional time-stop, targeting reversion to the SMA.

**Verdict (Phase 3d-B2):** **HARD REJECT** (Phase 3c §7.3
catastrophic-floor predicate; **Phase 3d-B2 terminal**).

- **5 separate violations** across BTC / ETH × MED / HIGH cost cells.
- **BTC MED expR = −0.5227.** **BTC HIGH expR = −0.7000 / PF = 0.2181.**
  **ETH HIGH expR = −0.5712 / PF = 0.2997.**
- **M1 BTC PARTIAL** (mean +0.024R below the +0.10 threshold;
  fraction-non-negative 55.4%).
- **M2 BTC FAIL / ETH weak-PASS.**
- **M3 PASS-isolated on both symbols.** TARGET subset (the trades
  that actually reverted to the SMA target) was profitable in
  isolation, but **overwhelmed by 53–54% STOP exits at −1R mean per
  loser** in the full trade population.

F1 was the project's first hard rejection. Phase 3c §7.3 predeclared
the catastrophic-floor predicate and Phase 3d-B2 evaluated it
exactly: any strategy producing negative expectancy at HIGH-slip
across both symbols, plus PF < 0.50, plus M1 below threshold, is
HARD REJECT.

**F1 is retained as research evidence only.** Phase 3d-B2 / Phase 3e
verdict preserved verbatim by Phase 4m.

**F1 lessons:**

- **Mechanism PASS-isolated is insufficient.** A strategy where
  TARGET-subset trades are profitable in isolation can still fail at
  the framework level if the STOP-subset trades dominate by trade
  count and lose enough per loser. Math: TARGET-subset mean R times
  TARGET-subset count must outweigh STOP-subset mean R times
  STOP-subset count, after costs. F1 had ~46–47% TARGET share, not
  enough.
- **Stop-vs-target ratio matters as much as expectancy.** F1's 1R
  stop + variable target produced ~25–35% empirical win rate vs.
  ~50% breakeven required by the ratio.
- **Mean-reversion at this geometry is not promotable.** F1 with
  extra filters (regime, time-of-day, funding, etc.) is forbidden as
  rescue. F1-prime is explicitly not authorized.
- **Hard-rejection at first execution validates the predeclared
  catastrophic-floor framework.** Phase 3c §7.3 caught a structural
  failure before the project committed implementation effort.

**Reusable insight:** any future mean-reversion strategy must
predeclare a stop-vs-target geometry compatible with the empirically-
observed win rate. F1's ~30% win rate × ~1.5R variable target is
sub-breakeven before costs.

---

## D1-A recap

**D1-A** (Phase 3f–3j) is the funding-aware directional contrarian
strategy on BTCUSDT 15m: at completed funding-settlement time, if
the trailing-90-day funding-rate Z-score |Z_F| ≥ 2.0, enter contrarian
at the next 15m bar's open (long when funding is extreme-negative,
short when extreme-positive), 1.0 × ATR(20) stop, +2R fixed take-
profit, 32-bar (8-hour) unconditional time-stop, per-funding-event
cooldown.

**Verdict (Phase 3j):** **MECHANISM PASS / FRAMEWORK FAIL — other**
(Phase 3h §11.2; **Phase 3j terminal under current locked spec**).

- **Catastrophic-floor predicate NOT triggered.**
- **cond_i BTC MED expR > 0 FAILED** (BTC R MED expR = −0.3217).
- **cond_iv BTC HIGH cost-resilience FAILED** (BTC R HIGH expR =
  −0.4755 / PF = 0.5145).
- **M1 BTC h=32 PASS** (mean +0.1748R AND fraction-non-negative
  0.5101).
- **M2 FAIL on both symbols** (BTC funding benefit +0.00234R ~21×
  below the +0.05R threshold; ETH +0.00452R ~11× below).
- **M3 PASS-isolated on both symbols** (TARGET subset BTC mean
  +2.143R / aggregate +111.46R; ETH mean +2.447R / aggregate
  +119.89R — overwhelmed by 67–68% STOP exits at −1.30 / −1.24R
  mean per loser).
- **Empirical WR ~30% / ~31% vs. forecast +51% breakeven.**

D1-A's distinctive failure pattern: the funding signal **does** carry
information (M1 PASS, M3 PASS-isolated showing TARGET subset
profitability), but the directional contrarian framing does not
translate into framework-level expectancy. Funding extremes correlate
with eventual reversion, but the time-to-reversion is too long for
the 32-bar time-stop, and the stop-vs-target ratio interacts
adversely with the empirical ~30% win rate.

**D1-A is retained as research evidence only.** Phase 3j / Phase 3k
verdict preserved verbatim by Phase 4m.

**D1-A lessons:**

- **Information presence ≠ tradable framework.** Funding extremes
  contain information about future price direction (M1 PASS, M3
  PASS-isolated). But the D1-A *framing* — direct contrarian
  directional entry with fixed time-stop and fixed-R target — does
  not translate that information into framework-level expectancy.
- **Stop / target / time-stop interacts with mechanism timescale.**
  The 32-bar time-stop is too short for the multi-day reversion
  pattern that funding extremes signal. A different exit family
  might capture the information differently — but that is a NEW
  hypothesis, not D1-A rescue.
- **Funding-as-trigger ≠ funding-as-context.** D1-A used funding as
  the directional trigger. A future strategy that uses funding only
  as a context filter (e.g., avoid trading when funding is in
  pathological extremes) is conceptually distinct from D1-A.
- **Cost sensitivity remains binding.** BTC HIGH expR = −0.4755 with
  PF = 0.5145 confirms §11.6's blocking power.
- **D1-A with extra filters / D1-A-prime / D1-B / V1/D1 hybrid /
  F1/D1 hybrid all forbidden as rescue.** Phase 3j explicitly
  forbids these continuations.

**Reusable insight:** funding may be useful as **context** for a
trend-continuation strategy (avoid trading at pathological extremes)
or as one of several confirmation lenses. It is NOT useful as a
direct directional trigger under D1-A's framing. Any future
funding-using strategy must structurally distinguish itself from
D1-A.

---

## 5m diagnostics recap

**5m diagnostic thread** (Phase 3o predeclaration → Phase 3p data-
requirements memo → Phase 3q v001-of-5m supplemental acquisition →
Phase 3r §8 mark-price gap governance → Phase 3s diagnostic
execution → Phase 3t closure consolidation) was a **diagnostic-only**
research thread, not a strategy.

**Phase 3o** predeclared seven question forms (Q1–Q7) with strict
analysis-boundary rules: each question had to surface a property of
the v002-locked retained-evidence trade populations (R3, R2, F1,
D1-A; 10 031 trades total), with predeclared informative /
non-informative classification rules, **before any 5m data existed
in the repository**. Phase 3o §6 explicitly forbade rescue-shaped
question forms (e.g., "what filter makes F1 profitable?").

**Phase 3s execution (run exactly once):**

- **Q1, Q2, Q3 (+1R), Q6 (D1-A only), Q7 meta** classified
  **INFORMATIVE** under Phase 3p §8 outcome-interpretation rules.
- **Q4, Q5** classified **NON-INFORMATIVE**.
- **Q3** ambiguous for +2R.
- Phase 3r §8 mark-price gap governance applied with **zero trades
  excluded empirically** (retained-evidence trade lifetimes ≤ 8h are
  too short to straddle the four mark-price gap windows).

**Headline informative findings:**

- **Q1** — IAE > IFE in 7 of 8 candidate × symbol cells (universal
  entry-path adverse bias; F1 most pronounced at ~0.5R consumed in
  first 5 min).
- **Q2** — V1-family wick-dominated stop pathology (R3 / R2 wick-
  fraction 0.571–1.000) vs. F1 / D1-A sustained-dominated (0.269–
  0.347), the cleanest cross-family mechanism finding.
- **Q3 (+1R)** — intrabar-touch fraction ≥ 25% in 6 of 8 cells.
- **Q6** — D1-A mark-stop lag ~1.3–1.8 5m bars (mark triggers later
  than trade).

**Phase 3t closure consolidation:**

- **5m research thread is operationally complete and closed.**
- **Useful timing information exists inside 15m bars, descriptively
  only.**
- **No 5m strategy was authorized** then or since. **5m remains
  diagnostic-only.**
- **Phase 3o §6 forbidden question forms preserved.**
- **Phase 3o §10 analysis boundary preserved:** informative findings
  cannot license verdict revision, parameter change, strategy rescue,
  5m strategy / hybrid / variant, paper / shadow, Phase 4, live-
  readiness, deployment, or any successor authorization.

**5m diagnostics lessons:**

- **Sub-15m timing information is real.** Q1 / Q2 / Q6 surface
  measurable patterns in entry-path and stop-pathology that 15m bars
  hide.
- **But sub-15m information is not directly tradable in v1.** The
  bar-completion-time discipline (Phase 4g §13 / R3 / V1) prevents
  using mid-bar 5m information as a primary signal source. Any
  attempt to do so would require an entirely new execution model.
- **Phase 3o §6 forbidden question forms are binding.** Q1–Q7 cannot
  be converted into rules. Q3 / Q6 cannot become "the +1R early-
  touch rule" or "the mark-stop lag adjustment". Q3 ambiguous for
  +2R is not a license to assume a +2R early-touch effect.

**Reusable insight:** future strategies that use sub-15m information
must do so as **diagnostics applied to executed trades**, not as
primary signal triggers. The 5m thread is a permanent reference for
this discipline.

---

## V2 recap

**V2** (Phase 4f predeclaration → Phase 4g spec → Phase 4h data-
requirements → Phase 4i acquisition → Phase 4j §11 metrics governance
→ Phase 4k methodology → Phase 4l execution) was the project's most
ambitious ex-ante hypothesis: **Participation-Confirmed Trend
Continuation**.

**Phase 4f predeclaration:** trade trend-continuation / breakout
events on BTCUSDT perpetual only when **price structure** (Donchian
breakout from compression with HTF trend bias), **volatility regime**
(post-compression / expansion-friendly), **participation / volume**
(relative volume + volume z-score + UTC-hour percentile + taker
imbalance), and **derivatives-flow context** (OI delta + funding
percentile band) align simultaneously.

**Phase 4g operationalized:** signal 30m, bias 4h, session bucket 1h,
8 active entry features + 3 active exit / regime features, 512-
variant predeclared threshold grid (= 2^9), M1 / M2 / M3 mechanism-
check decomposition, four governance labels.

**Phase 4i acquired** the four 30m+4h kline datasets (research-
eligible) plus two metrics datasets (NOT research-eligible globally;
~0.03% intra-day 5m gaps + NaN concentration in optional ratio
columns). **Phase 4j §11** adopted the binding metrics OI-subset
partial-eligibility rule (mirrors Phase 3r §8 pattern). **Phase 4k**
predeclared the complete backtest methodology.

**Phase 4l executed** the 512-variant V2 backtest exactly under
Phase 4k methodology and emitted **Verdict C — V2 framework HARD
REJECT** driven by **CFP-1 critical**.

**The forensic finding:**

- **V2 did not lose because trades had bad expectancy.**
- **V2 produced zero trades.**
- The 8-feature AND chain produces ~15 raw long-side setups per
  variant per symbol over the 4-year coverage.
- **All raw setups are subsequently rejected by the V1-inherited
  stop-distance filter (0.60 × ATR ≤ stop_distance ≤ 1.80 × ATR).**
- V2's locked 20/40-bar Donchian setup window per Phase 4g §29 axis
  1 produces **structural stop distances of 3–5 × ATR(20)**.
- The V1 stop-distance filter was originally calibrated for V1's
  8-bar setup window, where setup_low typically sits ~0.5–1.0 × ATR
  below the breakout-bar close. With V2's 20–40 bar Donchian setup,
  setup_low can sit far further below.
- **This is structural incompatibility between V2's setup geometry
  and V1's inherited stop-distance gating.**

**Phase 4l correctly classified this as analogous to F1's HARD
REJECT under Phase 3c §7.3 catastrophic-floor**: the strategy spec,
as predeclared, fails at the design stage before any data-dependent
evaluation can occur.

**V2 is retained as research evidence only. V2 first-spec is
terminal.**

**V2 lessons (the critical content of Phase 4m):**

The V2 lesson is **not**:

- "the stop-distance filter is too strict";
- "let's widen the filter and rerun";
- "let's drop the filter and rerun";
- "let's reduce N1 to 8 and rerun";
- "V2 just needs a parameter tweak".

The V2 lesson **is**:

- **Setup window geometry directly determines structural stop
  geometry.** A longer setup window (20–40 bars) naturally produces
  wider structural stops (since the lowest-low / highest-high over
  20–40 bars sits further from the current bar's close than over
  8 bars).
- **Stop-distance trade-quality filters cannot be inherited
  piecewise from a different strategy.** The V1 0.60–1.80 × ATR
  bounds were calibrated for V1's 8-bar setup. V2 inherited the
  bounds without recalibrating; the geometric mismatch produced 0
  trades.
- **Stop / target / sizing are co-design constraints.** A wider stop
  is risk-controllable by reducing position size (sizing maintains
  fixed risk fraction). But a wider stop changes trade geometry
  because fixed-R targets require larger absolute price moves to
  reach take-profit. A 3× ATR stop with +2R take-profit requires a
  6× ATR move; this is achievable far less often than a 1× ATR stop
  with +2R take-profit (= 2× ATR move). Trade frequency and sample
  size collapse as stop widens.
- **A stop-distance filter can be a valid trade-quality gate,** but
  it must be calibrated to the setup window from first principles —
  not blindly inherited.
- **Future strategies must justify stop-distance bounds from the
  setup itself, not from V1.**

This V2 lesson is the most important addition to the project's
research-arc record from Phase 4l. Phase 4m's job is to write it
down clearly so that no future operator decision drifts into
"just widen the V2 filter".

---

## Strategy-family failure taxonomy

Categorizing the rejection modes:

### 1. Cost-fragility rejection (R2)

- **Pattern:** mechanism evidence partially present (M1 / M3); but
  HIGH-slip cost cell breaks marginal expectancy.
- **§11.6 = 8 bps HIGH per side is the binding gate.**
- **Implication:** any future strategy with marginal expectancy in
  MED-slip will likely fail HIGH-slip; cost realism must be designed
  in, not bolted on.

### 2. Catastrophic-floor rejection (F1)

- **Pattern:** negative expectancy at HIGH-slip on both symbols;
  PF < 0.50; mechanism support PASS-isolated but not framework-
  level.
- **Phase 3c §7.3 predicate is the binding gate.**
- **Implication:** TARGET-subset profitability does not rescue a
  losing whole population. Stop-vs-target geometry must be
  compatible with empirical win rate.

### 3. Mechanism-pass / framework-fail (D1-A)

- **Pattern:** information signal present (M1 PASS, M3 PASS-isolated);
  but framing as direct directional trigger does not produce
  framework-level expectancy at HIGH-slip.
- **cond_i / cond_iv (Phase 3h §11.2) are the binding gates.**
- **Implication:** information presence ≠ tradable framework.
  Different framings of the same information may differ in
  framework-level performance.

### 4. Structural / design-stage rejection (V2)

- **Pattern:** strategy produces zero or near-zero trades because
  setup geometry is incompatible with another locked design element
  (stop-distance filter, target ratio, time-stop, etc.).
- **CFP-1 critical (Phase 4k) is the binding predicate.**
- **Implication:** setup geometry, structural stop, target model,
  and position sizing must be co-designed. Inheriting individual
  pieces from a different strategy is risky.

### Summary: four orthogonal rejection modes

The project has now systematically explored four orthogonal rejection
modes:

| Mode | Strategy | Binding gate | Lesson |
|---|---|---|---|
| Cost-fragility | R2 | §11.6 HIGH | cost realism is mandatory |
| Catastrophic-floor | F1 | Phase 3c §7.3 | TARGET-subset doesn't rescue framework |
| Information / framing mismatch | D1-A | Phase 3h §11.2 | information ≠ tradable framework |
| Design-stage incompatibility | V2 | Phase 4k CFP-1 | setup / stop / target must co-design |

**Each mode is a permanent constraint on future hypotheses.**

---

## Cost-sensitivity lessons

- **§11.6 = 8 bps HIGH per side is preserved verbatim.** It blocked
  R2 outright (Phase 2w §16.1) and subordinated D1-A (Phase 3j
  cond_iv FAIL).
- **§11.6 is not a target to game.** A strategy that "barely" passes
  §11.6 is structurally fragile to any cost-environment change.
- **Phase 3l external execution-cost evidence review** found §11.6
  is "B — current cost model conservative but defensible". Phase 3l
  did NOT recommend revision. **Phase 4m preserves §11.6 verbatim.**
- **Funding cost is included in P&L.** Phase 4l confirmed this works
  correctly (zero in V2's run because no trades; in non-zero-trade
  strategies, funding accrues at 8h cadence).
- **No maker rebate, no live-fee, no VIP-discount assumptions.** All
  prior strategies (R3 / R2 / F1 / D1-A / V2) were tested at taker
  fee = 0.04% per side default for USDⓈ-M futures. Phase 4m preserves
  this.

**Reusable insight:** any future strategy must be designed to survive
HIGH-slip from the start, not engineered to barely pass it. Marginal-
expectancy strategies are structurally weak.

---

## Stop / target / sizing lessons

The V2 forensic finding crystallizes the most important lesson of
Phase 4m. Phase 4m distinguishes:

### Position sizing by fixed risk percentage

- **Locked at 0.25% risk per trade** (§1.7.3).
- **Effective leverage cap: 2×** (§1.7.3).
- Position size = (equity × 0.25%) / stop_distance, rounded down to
  lot size.
- **Wider stops do NOT increase risk;** position size adjusts down
  proportionally.
- **But wider stops reduce position size in absolute terms,** which
  affects:
  - notional cap headroom (§1.7.3);
  - sub-minimum-quantity rejection rate;
  - target-distance absolute price move;
  - market-impact / slippage realized on the (now smaller) position.

### Stop-distance trade-quality filter

- **Distinct from sizing.** A trade-quality filter rejects trades
  whose stop distance falls outside a band; sizing handles approved
  trades.
- **V1 / R3 / V2 all use 0.60–1.80 × ATR(20).** V1 calibrated for
  8-bar setup; V2 inherited the same band for 20/40-bar setup. V2
  rejected 100% of raw candidates because its setup geometry
  produces stop distances outside the band.
- **A stop-distance filter is valid IF AND ONLY IF it is compatible
  with the setup window.** Not every strategy needs the V1 band.

### Structural invalidation point

- **The price level that, if breached, invalidates the trade
  hypothesis.** For V1 / R3 / V2: setup_low (long) = lowest low
  over the prior N bars of the setup window.
- **N determines structural stop distance.** N=8 (V1) gives close
  stops; N=20 / 40 (V2) gives far-out stops.
- **The stop is BELOW setup_low − ATR_buffer** to absorb noise.

### Target distance in R

- **R = |entry_price − initial_stop|** (R3 / V2 convention).
- **Fixed-R take-profit (e.g., 2R, 2.5R) is a relative target.** A
  wider stop means a wider absolute target.
- **Win rate required to break even** depends on the R-multiple of
  the target plus costs. At fixed 2R + 16 bps round-trip cost,
  breakeven win rate ≈ 35%; at fixed 2.5R, breakeven ≈ 31%.

### Absolute price movement required to reach target

- **For long with R=stop_distance, target=N_R × R:** absolute price
  move required = N_R × stop_distance.
- **V1 example:** 8-bar setup, stop ≈ 0.7 × ATR; with N_R=2, target
  ≈ 1.4 × ATR move. Plausible within 12–16 30m bars.
- **V2 example:** 20-bar setup, stop ≈ 4 × ATR; with N_R=2, target
  ≈ 8 × ATR move. Far less plausible within 12–16 30m bars.
- **The same N_R produces qualitatively different trade frequencies
  depending on setup window.**

### Cost / slippage impact

- **Cost is a fixed bps fraction of entry / exit price.** Round-trip
  ≈ (taker fee + slippage) × 2 = 8–24 bps depending on cell.
- **In R units: cost = round_trip_bps × entry_price / R / 10000.**
- **Wider R reduces relative cost in R units.** A 3 × ATR stop at
  HIGH-slip has cost-in-R ≈ half of a 1.5 × ATR stop at HIGH-slip,
  for a given R.
- **But trade frequency collapses with wider R.** Per-trade cost
  reduction does not compensate for sample-size loss.

### Trade frequency / sample-size impact

- **A wider stop-distance filter combined with a longer setup window
  reduces trade count.** V2 ran into the extreme: 0 trades.
- **Sample size enters into DSR computation** (Bailey & López de
  Prado 2014). DSR requires T ≥ 30 train-window trades per variant.
  V2 had T = 0.
- **A strategy with too few trades per year fails CFP-1** even
  before mechanism evaluation.

### Co-design conclusion

**The lesson:**

- **Setup window N determines structural stop distance.**
- **Structural stop distance × N_R determines target absolute
  movement.**
- **Target absolute movement determines achievable trade rate.**
- **Trade rate × N years of data determines sample size.**
- **Sample size determines CFP-1 / DSR / PBO statistical power.**

These five elements are linked. Choosing N=20 forces a recalibration
of the stop-distance filter, which forces a recalibration of N_R,
which forces a recalibration of T_stop, which determines whether the
strategy produces enough trades to test.

**A future strategy must co-design these five elements from first
principles.** Inheriting V1's stop-distance bounds for a non-V1 setup
window is the V2 failure mode.

**Phase 4m does NOT propose specific bounds for any future strategy.**
It records the constraint.

---

## Timeframe and setup-window lessons

| Timeframe | Strategies tested | Outcome | Insight |
|---|---|---|---|
| 15m signal / 1h bias | H0, R3, R1a, R1b-narrow, R2, F1, D1-A | 1 baseline + 4 retained + 1 cost-fail + 1 hard-reject + 1 framework-fail | 15m has been thoroughly explored; orthogonal failure modes documented |
| 5m | diagnostics-only (Q1–Q7) | operationally complete and closed | sub-15m information exists but is not directly tradable in v1 |
| 30m signal / 4h bias / 1h session | V2 | structural CFP-1 critical; 0 trades; HARD REJECT | longer setup windows require recalibrated stop / target / sizing |
| 1h, 4h, daily | not tested as standalone signal timeframes | — | possible future research space; trade-frequency and sample-size constraints become severe |
| 1m / sub-minute / tick | not authorized | — | execution model constraints; v1 forbids |

**Setup-window lessons:**

- **N=8 (V1)** is calibrated and battle-tested across H0 / R3 / R1a /
  R1b-narrow / R2 / F1 / D1-A.
- **N=20 / 40 (V2)** produced 0 trades under V1 stop bounds.
- **Mid-range N (10–15)** has not been tested.
- **A future strategy at N≠8 must justify the choice and
  co-recalibrate the stop / target / sizing.**

**Reusable insight:** if a future strategy moves the signal timeframe
from 15m, the setup-window N value cannot be assumed; it must be
designed from first principles.

---

## Volume / participation lessons

V2 was the project's first strategy to use volume / participation
features as primary entry confirmation. The Phase 4l forensic finding
shows:

- **The 8-feature AND chain produces ~15 raw setups per variant per
  symbol over 4 years.** Most of the funnel collapse happens at the
  participation gates (relative volume, volume z-score, taker
  imbalance, UTC-hour percentile).
- **The participation gates are restrictive but not unreasonable.**
  Each gate individually passes ~50% of bars; the AND combination
  reduces to ~0.05% — multiplicative effect of restrictive
  thresholds.
- **The V1 family (H0 / R3 / R1a / R1b-narrow / R2) does NOT use
  participation gates.** V1 treats volume as a context observable
  but not as a primary entry trigger.
- **F1 / D1-A also do NOT use participation gates.**

**Participation lesson:** participation confirmation is a strong
filter that produces few candidate trades over years of coverage. A
future strategy that uses participation gates must:

- expect low candidate count (~tens per symbol per year);
- design stop / target / sizing such that ~tens of trades per year
  is sufficient for DSR / PBO / CSCV;
- predeclare participation thresholds before testing (Phase 4g pattern
  is correct);
- not increase participation thresholds after observing too many
  trades (rescue) or decrease them after observing too few (rescue).

**Reusable insight:** participation features are valuable but
restrictive. A future strategy that uses them must design around the
low-trade-count constraint.

---

## Funding / derivatives-context lessons

Funding-rate has been used in two distinct framings:

### As directional trigger (D1-A)

- **Tested in Phase 3f–3j.** Verdict: MECHANISM PASS / FRAMEWORK
  FAIL — other.
- **The funding signal carries information** (M1 PASS, M3 PASS-
  isolated).
- **But the contrarian directional framing does not translate into
  framework-level expectancy.**

### As context / filter band (V2)

- **Tested in Phase 4l as part of V2's 8-feature AND chain.**
- **V2 used funding-rate percentile as a non-pathological band
  filter:** [20, 80] or [30, 70] percentile.
- **V2 produced 0 trades, so the funding-as-context contribution
  cannot be evaluated empirically.**
- **The framing (band filter, not directional trigger) is
  conceptually distinct from D1-A.**

**Funding lessons:**

- **Funding contains information.** Phase 3f–3j proved this at the
  M1 level.
- **But "funding-as-trigger" is a failed framework.** D1-A is HARD
  CLOSED; D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid all
  forbidden.
- **"Funding-as-context-band-filter" is a different framing.** It
  could be tested in a new ex-ante hypothesis if (and only if) that
  hypothesis is genuinely new and not D1-A rescue. **V2 used this
  framing but didn't produce enough data to evaluate it.**

**Reusable insight:** funding can serve as context for a different
strategy, but any future use must structurally distinguish itself
from D1-A and must predeclare its framing before testing.

---

## Regime-filter lessons

Regime-filter approaches have appeared in:

- **R1a (volatility-percentile setup predicate).** Retained non-
  leading; partial improvement only.
- **R1b-narrow (bias-strength magnitude threshold).** Retained non-
  leading; partial improvement only.
- **V2 (multiple regime gates: ATR percentile, Donchian width
  percentile, UTC-hour percentile, funding band).** All bolted into
  the AND chain.

**Regime lessons:**

- **Regime gates have signal information** (R1a / R1b-narrow showed
  partial improvement).
- **But no Prometheus strategy has been designed regime-first.** All
  tested strategies start with a primary entry trigger (V1 breakout,
  F1 mean-reversion, D1-A funding) and add regime gates secondarily.
- **Phase 3m predeclared the docs-only regime-first research framework
  memo** as a possible future direction. **Phase 3m recommended remain
  paused.** No regime-first work has been authorized since.
- **A regime-first strategy is conceptually distinct from any current
  Prometheus strategy.** It would be a genuinely new hypothesis
  family if predeclared properly.

**Reusable insight:** regime detection done as a first-class design
choice (not as a bolt-on) is a candidate research space. **Phase 4m
does NOT authorize this.** Any such direction would need a separate
operator decision.

---

## Data and governance lessons

Phase 4i / 4j / 4l introduced new data-governance patterns:

### Phase 4i partial-pass acquisition

- 4 of 6 datasets research-eligible at strict gate; 2 metrics
  datasets failed.
- **Phase 4i did NOT relax the strict gate** (Phase 4h §17.4
  preserved). **Phase 4i stopped for operator review** per its
  brief.
- **This is a valid integrity-preserving outcome.** A backtest could
  not begin without operator deciding metrics governance.

### Phase 4j §11 metrics OI-subset partial-eligibility rule

- **Mirrors Phase 3r §8 mark-price gap governance** (transposed
  per-trade → per-bar).
- **Manifests remain globally `research_eligible: false`.**
- **Per-bar OI-feature-eligibility check** required all six aligned
  5-minute records present + non-NaN.
- **Optional ratio columns categorically forbidden.**
- **No forward-fill, interpolation, imputation.**

**Lesson:** when a dataset family has structural integrity
imperfections, the right response is a feature-level governance rule,
not a manifest-level relaxation.

### Phase 4l forbidden-input non-access

- **Optional ratio-column non-access enforced at three layers:**
  static scan + metrics-loader explicit-column-list + runtime
  introspection. Zero access confirmed.
- **No mark-price 30m / 4h / 5m / 15m, no aggTrades, no spot, no
  cross-venue, no authenticated APIs, no network I/O.**

**Lesson:** forbidden-input non-access verification can be implemented
at multiple layers without slowing down execution. This pattern is
reusable for any future research code.

### Empirical exclusion fraction

- **Phase 4l empirical metrics OI exclusion: ~0.044% on each symbol.**
- **CFP-9 threshold is 5%.** Well below.
- **Phase 4j §11 governance was non-restrictive in practice.**

**Lesson:** the Phase 4j §11 binding rule turned out to have
negligible practical impact on V2's outcome. The V2 verdict was
driven by the stop-distance filter, not by metrics exclusion. This
is research evidence, not authorization to relax Phase 4j §11.

**Reusable insights:**

- **Predeclared per-bar / per-trade exclusion governance is the
  correct response to dataset partial-eligibility.**
- **Multi-layer non-access verification is feasible and valuable.**
- **Empirically-verified exclusion fractions strengthen confidence
  in the governance rule.**

---

## Reusable insights

Compiled from the above sections:

1. **Trend-continuation / breakout** remains a plausible broad
   strategy family in crypto, but plain price breakout is not
   sufficient on BTCUSDT. R3 / V1 represents the cleanest local
   maximum; further work has not demonstrably improved on it.

2. **Mean-reversion-after-overextension at the F1 geometry is
   structurally not promotable.** Future mean-reversion ideas would
   need a materially different geometry.

3. **Funding contains information** but **funding-as-trigger fails
   at D1-A's framing.** Funding-as-context-band-filter is a different
   framing that has not been independently evaluated.

4. **Cost realism (§11.6 = 8 bps HIGH per side) is mandatory.**
   Marginal-expectancy strategies fail under HIGH cost; any future
   strategy must be designed to survive HIGH cost from the start.

5. **§11.6 cost gate is non-negotiable.** Phase 3l confirmed it is
   "conservative but defensible".

6. **Mechanism evidence (M1 / M2 / M3) is necessary but not
   sufficient.** PASS-isolated subsets do not rescue losing
   frameworks (F1 / D1-A both demonstrate this).

7. **Setup window, structural stop, target model, position sizing,
   and trade frequency are interdependent.** Choosing N forces
   recalibration of the others.

8. **Stop-distance filters are valid trade-quality gates** but must
   be calibrated to the specific setup window — not inherited from
   a different strategy.

9. **Volume / participation features produce restrictive AND chains.**
   Strategies using them yield few candidates per year; design
   accordingly.

10. **Regime gates have partial signal information** but the project
    has not yet tested regime-first as a primary design choice.

11. **Phase 4j §11 / Phase 3r §8 partial-eligibility governance
    pattern is reusable.** When a dataset family has structural
    integrity imperfections, define a feature-level rule rather than
    relaxing the manifest gate.

12. **Multi-layer forbidden-input non-access verification is
    feasible.** Phase 4l demonstrates static scan + explicit column
    list + runtime introspection.

13. **Predeclaration discipline (Bailey et al. 2014) is binding.**
    Hypothesis, features, threshold grid, validation methodology,
    pass/fail thresholds, and forbidden rescue interpretations must
    all be committed before data is touched.

14. **Catastrophic-floor predicates (Phase 3c §7.3 / Phase 4k CFP-1
    through CFP-12) catch failures cheaply.** They are reusable as a
    default predicate set for any future research.

15. **5m sub-bar information is real but diagnostic-only in v1.**
    Phase 3o §6 forbidden question forms preserved.

---

## Forbidden rescue observations

The following observations would be rescue interpretations and are
**FORBIDDEN by Phase 4m**:

### V2 rescue forms (forbidden)

- **V2 with max stop-distance widened to 5 × ATR.** Forbidden.
  Widening the filter to admit V2's structurally-wide stops would be
  post-hoc optimization.
- **V2 with max stop-distance set to "the smallest value that admits
  any V2 trades".** Forbidden. This would be selecting a parameter
  from the failure outcome.
- **V2 but N1 changed from {20, 40} to a smaller value.** Forbidden.
  Phase 4g §29 axis 1 is locked. Changing N1 in response to Phase 4l
  outcome is parameter rescue.
- **V2 but stop-distance filter removed entirely.** Forbidden. The
  filter is a Phase 4g §19 / V1 inheritance; removing it for V2
  while keeping it for V1 / R3 would be inconsistent and post-hoc.
- **V2-prime / V2-narrow / V2-relaxed / V2 hybrid.** Explicitly
  forbidden by Phase 4l verdict and Phase 4m.
- **Any immediate backtest based on the Phase 4l observed root
  cause.** Forbidden.
- **Any Phase 4g / Phase 4j / Phase 4k methodology amendment based
  on Phase 4l result.** Forbidden.

### F1 rescue forms (forbidden)

- **F1 with extra filters (regime, time-of-day, funding, volatility).**
  Forbidden. Phase 3d-B2 is terminal for F1.
- **F1 with relaxed stop / target / time-stop.** Forbidden.
- **F1-prime.** Explicitly forbidden by Phase 3e / Phase 3k.

### D1-A rescue forms (forbidden)

- **D1-A with extra filters.** Forbidden. Phase 3j is terminal.
- **D1-A-prime / D1-B.** Explicitly forbidden by Phase 3k.
- **V1/D1 hybrid / F1/D1 hybrid.** Explicitly forbidden by Phase 3k.

### R2 rescue forms (forbidden)

- **R2 with cheaper costs.** Forbidden. §11.6 is locked.
- **R2 with HIGH cost relaxed to MED-only.** Forbidden.

### Cross-strategy rescue forms (forbidden)

- **Choosing parameters from Phase 4l forensic numbers.** E.g., "V2
  candidates have stop ≈ 3.3 × ATR; let's set the filter to 3.5 × ATR
  for the next backtest." Forbidden.
- **Selecting subsequent strategy thresholds based on Phase 3s 5m
  diagnostic findings.** Phase 3o §6 forbidden question forms apply.
- **Treating Q3 / Q6 / Q1 / Q2 informative findings as rule
  candidates.** Forbidden.

### Methodological rescue forms (forbidden)

- **Reducing the 512-variant grid in V2-derived strategies to make
  PBO / DSR computation cheaper, choosing reduction based on Phase 4l
  outcome.** Forbidden if it amounts to selecting variants that
  "would have produced trades".
- **Relaxing the §11.6 HIGH cost cell to make a borderline strategy
  pass.** Forbidden.
- **Skipping the OOS holdout window after observing train-best
  variant performance.** Forbidden.

**Phase 4m records these as the explicit forbidden-rescue list.**

---

## Fresh-hypothesis validity gate

A future candidate must satisfy ALL of the following to be a valid
ex-ante hypothesis (Phase 3t §12 + Phase 4m extensions):

1. **Must be named as a new hypothesis, not a rescue label.** Names
   like "V2.1", "V2-prime", "V2-modified" are forbidden. The
   hypothesis must have a distinct name and a distinct conceptual
   foundation.

2. **Must be specified before any data is touched.** No exploratory
   plotting / aggregating / backtest runs of the new direction
   before predeclaration.

3. **Must explain why it is new in theory, not just a parameter
   tweak.** The conceptual basis must distinguish it from R3 / R2 /
   R1a / R1b-narrow / F1 / D1-A / V2. "It uses a different N1" is
   not new in theory.

4. **Must define entry, stop, target, sizing, cost, timeframe, and
   exit together.** The five-element co-design (Phase 4m §"Stop /
   target / sizing lessons") must be done from first principles.

5. **Must predeclare data requirements** (analogous to Phase 4h).

6. **Must predeclare mechanism checks** (analogous to Phase 4g §30
   M1 / M2 / M3 framework, but tailored to the new hypothesis).

7. **Must predeclare pass / fail gates** including catastrophic-floor
   predicates (analogous to Phase 4k CFP-1 through CFP-12 set,
   tailored).

8. **Must predeclare forbidden comparisons and forbidden rescue
   interpretations** (analogous to Phase 4m §"Forbidden rescue
   observations" but specific to the new hypothesis).

9. **Must NOT choose thresholds from prior failed outcomes.**
   Bailey et al. 2014 anti-data-snooping discipline.

10. **Must NOT use Phase 4l root-cause analysis as a direct
    optimization target.** I.e., must not say "we want stop_distance
    to be in [X, Y] because we saw V2 had 3-5×ATR stops". The new
    bounds must be derived from the new strategy's own first-
    principles design.

11. **Must preserve §11.6 cost sensitivity.** No relaxation.

12. **Must preserve project locks and governance.** §1.7.3, mark-
    price stops (Phase 3v §8), break-even / EMA slope / stagnation
    (Phase 3w §6 / §7 / §8), Phase 3r §8 mark-price gap governance,
    Phase 4j §11 metrics OI-subset rule (if metrics used), Phase 4k
    methodology (if backtest authorized).

13. **Must commit to predeclared chronological train / validation /
    OOS holdout windows** before any backtest.

14. **Must commit to deflated Sharpe / PBO / CSCV correction** if
    grid search is involved.

15. **Must distinguish between mechanism evidence and framework
    promotion.** PASS-isolated mechanism is research evidence, NOT
    promotion.

16. **Must preserve the BTCUSDT-primary / ETHUSDT-comparison
    protocol** unless the operator explicitly authorizes a different
    universe (which would itself require a separate predeclaration).

17. **Must NOT propose live-readiness or paper / shadow / Phase 4
    canonical** as part of its first phase.

18. **Must satisfy operator authorization** as a separately briefed
    phase.

A candidate that fails ANY of these is not a valid fresh hypothesis.

---

## Candidate future research spaces

This section identifies broad research directions WITHOUT authorizing
any. Each is a candidate, not a commitment.

### Structural-R trend continuation

- **Idea:** trend-continuation strategy where R is defined by setup
  geometry from first principles, with stop / target / sizing co-
  designed.
- **Distinguishing feature:** unlike V2, the stop-distance bounds
  are derived from the setup window, not inherited from V1.
- **Status:** ALLOWED as a future research space. **NOT authorized.**
- **Forbidden interpretation:** if specified as "V2 with adaptive
  stop bounds derived from N1", it is V2 rescue. The hypothesis
  must be conceptually distinct.

### Regime-first breakout continuation

- **Idea:** regime detection (volatility regime, trend regime,
  funding regime) is the primary design choice; entry trigger comes
  second.
- **Distinguishing feature:** unlike R1a / R1b-narrow / V2, regime
  is not a bolt-on filter; it determines whether the strategy is
  active at all.
- **Status:** ALLOWED as a future research space. **NOT authorized.**
- **Phase 3m precedent:** Phase 3m recommended remain paused on this.

### Funding-context trend filter

- **Idea:** funding-rate as a context filter (avoid trading in
  pathological extremes), not as a directional trigger.
- **Distinguishing feature:** unlike D1-A, funding does not
  determine direction; it determines whether to trade at all.
- **Status:** ALLOWED as a future research space. **NOT authorized.**
- **Forbidden interpretation:** if specified as "D1-A but with
  funding as filter instead of trigger", it is D1-A rescue. The
  hypothesis must be conceptually distinct.

### Structural pullback continuation

- **Idea:** pullback / retest entry but with cost model and stop
  geometry designed together from first principles.
- **Distinguishing feature:** unlike R2, the cost model and stop
  geometry are not inherited from V1 / R3.
- **Status:** ALLOWED as a future research space. **NOT authorized.**
- **Forbidden interpretation:** if specified as "R2 with relaxed
  cost", it is R2 rescue.

### Mean-reversion (de-prioritized)

- **Idea:** any new mean-reversion approach.
- **Status:** **DE-PRIORITIZED.** F1 hard-rejected. Future use
  requires a materially new thesis (geometry, holding period,
  trigger definition all distinct from F1).
- **Forbidden interpretation:** F1 with extra filters.

### Market-making / HFT (rejected)

- **Idea:** liquidity-provision strategies.
- **Status:** **REJECTED for Prometheus now.** Phase 4f §"transferable
  vs. non-transferable institutional families" classified HFT /
  liquidity-provision as non-transferable to Prometheus's substrate.

### ML-first black-box forecasting (rejected)

- **Idea:** neural networks, gradient-boosted trees, opaque feature
  embeddings as primary signal source.
- **Status:** **REJECTED for now.** Phase 4f §"V2 non-goals"
  excluded ML-first; project remains rules-based per §1.7.3.

### Paper / shadow / live (forbidden)

- **Status:** **FORBIDDEN.** Per `docs/12-roadmap/phase-gates.md`.
  Phase 4 canonical not authorized; paper / shadow not authorized;
  live-readiness not authorized; deployment not authorized;
  production keys not authorized; exchange-write not authorized.

**Phase 4m does NOT select any of the above as a Phase 4m output.
Phase 4m does NOT create V3, V4, or any new strategy spec. Phase 4m
does NOT authorize fresh-hypothesis research.**

---

## Explicitly rejected next moves

The following are explicitly REJECTED as Phase 4m next-step
recommendations:

- **Immediate V2 backtest with relaxed stop filter.** Rejected (V2
  rescue).
- **V2 spec amendment.** Rejected.
- **Phase 4g / Phase 4j / Phase 4k methodology amendment.** Rejected.
- **F1-prime, F1 with extra filters, F1 hybrid.** Rejected.
- **D1-A-prime, D1-A with extra filters, D1-A hybrid.** Rejected.
- **R2 at lower cost.** Rejected.
- **R1a-prime, R1b-prime, V1/R1a hybrid.** Rejected.
- **5m as primary signal.** Rejected.
- **Paper / shadow / live / exchange-write / Phase 4 canonical.**
  FORBIDDEN.
- **Production Binance keys / authenticated APIs / private endpoints
  / user stream / WebSocket / listenKey / MCP / Graphify / `.mcp.json`
  / credentials.** FORBIDDEN.
- **V3, V4, or any new strategy spec authored by Phase 4m.**
  Rejected (Phase 4m is consolidation only, not strategy design).
- **Selecting parameters from Phase 4l forensic numbers for any
  future hypothesis.** Rejected (Bailey et al. 2014).

---

## Recommended next operator choice

### Option A — Remain paused (PRIMARY RECOMMENDATION)

Take no further action. Phase 4m has consolidated the cumulative
research arc. The current cumulative project state across H0 / R3 /
R1a / R1b-narrow / R2 / F1 / D1-A / V2 means there is no live-
deployable strategy candidate in the project, and the project has
not committed to any specific next research direction.

**Reasoning:**

- The project has explored four orthogonal rejection modes (cost-
  fragility, catastrophic-floor, mechanism / framing mismatch,
  design-stage incompatibility). Each is now a permanent constraint
  on future hypotheses.
- Without a specific operator decision to commit research effort to
  a particular direction (regime-first, structural-R, funding-context,
  structural pullback), there is no benefit to authorizing any
  research phase.
- Remain paused respects the cumulative evidence and avoids hasty
  commitment to a new direction post-V2.

### Option B — Docs-only fresh-hypothesis discovery memo (CONDITIONAL SECONDARY)

Authorize a separate **docs-only** phase that proposes a fresh ex-ante
hypothesis (or evaluates two or three candidates against the Phase
4m §"Fresh-hypothesis validity gate") and selects ONE for further
docs-only specification work. The fresh-hypothesis discovery memo
would NOT acquire data, NOT run backtests, NOT implement any code,
NOT modify any prior phase artefact, and NOT propose paper / shadow /
live.

**Conditional:** only if the operator explicitly chooses to continue
research after consolidation. The memo's first task would be to
satisfy Phase 4m §"Fresh-hypothesis validity gate" requirement #3
("explain why it is new in theory") for the proposed candidate(s).

**Phase 4m does NOT authorize Option B. The operator must
separately authorize it.**

### Options C–F (NOT RECOMMENDED / REJECTED / FORBIDDEN)

- **Option C — Immediate V2 amendment / V2 rescue.** REJECTED.
- **Option D — V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec.**
  REJECTED.
- **Option E — V2 implementation under `src/prometheus/strategy/`.**
  REJECTED.
- **Option F — Paper / shadow / live-readiness / deployment /
  exchange-write.** FORBIDDEN.

### Phase 4m recommendation

**Phase 4m recommendation: Option A (remain paused) primary; Option
B (docs-only fresh-hypothesis discovery memo) conditional secondary
only if operator chooses to continue research.** Options C / D / E
not recommended. Option F forbidden.

---

## What this does not authorize

Phase 4m explicitly does NOT authorize, propose, or initiate any of
the following:

- **Any successor phase.** Phase 4n / Phase 4 canonical / any
  research / implementation / deployment phase NOT authorized.
- **V3 or any new strategy spec.** Phase 4m is consolidation only;
  it does not create a new strategy.
- **V2 rescue in any form.** V2-prime / V2-narrow / V2-relaxed / V2
  hybrid all forbidden.
- **F1 / D1-A / R2 rescue in any form.** All forbidden.
- **Phase 4g V2 strategy-spec amendment.** Preserved verbatim.
- **Phase 4j §11 metrics OI-subset rule amendment.** Preserved
  verbatim.
- **Phase 4k V2 backtest-plan methodology amendment.** Preserved
  verbatim.
- **Stop-distance bound revision, N1 axis revision, or threshold-
  grid revision based on Phase 4l outcome.** Forbidden.
- **§11.6 / §1.7.3 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r
  §8 modification.** All preserved verbatim.
- **R3 baseline-of-record revision.** Preserved.
- **H0 framework anchor revision.** Preserved.
- **V1 strategy spec revision.** Preserved.
- **5m research thread reopening.** Phase 3t closure preserved.
- **Phase 3o §6 forbidden question form revision.** Preserved.
- **Q1–Q7 conversion to rules.** Forbidden.
- **Mark-price 30m / 4h acquisition.** Deferred per Phase 4h §20.
- **`aggTrades` acquisition.** Deferred per Phase 4h §7.E.
- **v003 dataset creation.** Not authorized.
- **Manifest modification.** All Phase 4i / v002 / v001-of-5m
  manifests preserved verbatim.
- **Live exchange-write capability, production Binance keys,
  authenticated APIs, private endpoints, user stream, WebSocket,
  listenKey lifecycle, production alerting, Telegram / n8n
  production routes, MCP, Graphify, `.mcp.json`, credentials.** None
  touched.
- **Reconciliation implementation.** Phase 4e design preserved
  verbatim, not implemented.
- **Paper / shadow / live-readiness / deployment.** Not authorized.
- **Phase 4 (canonical).** Per `docs/12-roadmap/phase-gates.md`.

---

## Forbidden-work confirmation

- **No Phase 4n / Phase 4 canonical / successor phase started.**
- **No V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec
  authored.**
- **No V3 or any new strategy spec authored.**
- **No F1 / D1-A / R2 rescue spec authored.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No `.claude/rules/**` modification.**
- **No data acquired.**
- **No data modified.**
- **No public Binance endpoint consulted in code.**
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** Phase 4m performs no network I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No diagnostics run.**
- **No Phase 3o / 3p Q1–Q7 question rerun.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No `scripts/phase4i_v2_acquisition.py` execution.**
- **No `scripts/phase4l_v2_backtest.py` execution.**
- **No data acquisition / download / patch / regeneration /
  modification.**
- **No data manifest modification.** All
  `data/manifests/*.manifest.json` preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No Phase 4i manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A / V2 all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4j §11 metrics OI-subset governance modification.**
- **No Phase 4k V2 backtest-plan methodology modification.**
- **No Phase 4f / 4g / 4h / 4i / 4j / 4k / 4l text modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md`
  substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
  substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive
  change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4m branch.** Per Phase 4m brief.
- **No optional ratio-column access in any code.** (Phase 4m is
  text-only; no code at all.)
- **No merge to main.**
- **No successor phase started.**

---

## Remaining boundary

- **Recommended state:** **paused**. Phase 4m deliverables exist as
  branch-only artefacts pending operator review.
- **Phase 4m output:** docs-only retrospective consolidation memo +
  Phase 4m closeout artefact.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified at Phase 4m start).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4l all merged. Phase
  4m post-V2 consolidation memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Metrics OI-subset partial-eligibility governance:** Phase 4j §11
  (preserved verbatim).
- **V2 backtest methodology governance:** Phase 4k (preserved
  verbatim).
- **V2 first-spec terminal verdict:** Phase 4l Verdict C HARD REJECT
  (preserved verbatim).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j)
  + backtest-plan binding (Phase 4k) + executed (Phase 4l) →
  **Verdict C HARD REJECT, terminal for V2 first-spec; consolidated
  into project record by Phase 4m**.
- **OPEN ambiguity-log items after Phase 4m:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2
  HARD REJECT (Phase 4l, structural CFP-1 critical, terminal for V2
  first-spec); §11.6 = 8 bps HIGH per side; §1.7.3 project-level
  locks; mark-price stops; v002 verdict provenance; Phase 3q
  mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4m/post-v2-strategy-research-consolidation`
  exists locally and (after push) on `origin`. NOT merged to main.

---

## Next authorization status

**No next phase has been authorized.** Phase 4m's recommendation is
**Option A (remain paused) as primary**, with **Option B (docs-only
fresh-hypothesis discovery memo)** as **conditional secondary** —
acceptable only if the operator explicitly chooses to continue
research after consolidation. Options C / D / E not recommended.
Option F forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.

The 5m research thread remains operationally complete and closed
(per Phase 3t). The implementation-readiness boundary remains
reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance
blockers remain RESOLVED at the governance level (per Phase 3v +
Phase 3w). The Phase 4a safe-slice scope is implemented (per Phase
4a). The Phase 4b script-scope quality-gate restoration is complete
(per Phase 4b). The Phase 4c state-package quality-gate residual
cleanup is complete (per Phase 4c). The Phase 4d post-4a/4b/4c
review is complete (per Phase 4d). The Phase 4e reconciliation-model
design memo is complete (per Phase 4e). The Phase 4f V2 hypothesis
predeclaration is complete (per Phase 4f). The Phase 4g V2 strategy
spec is complete (per Phase 4g). The Phase 4h V2 data-requirements /
feasibility memo is complete (per Phase 4h). The Phase 4i V2 public
data acquisition + integrity validation is complete (per Phase 4i;
partial-pass). The Phase 4j V2 metrics data governance memo is
complete (per Phase 4j; Phase 4j §11 binding). The Phase 4k V2
backtest-plan memo is complete (per Phase 4k; methodology binding).
The Phase 4l V2 backtest execution is complete (per Phase 4l;
**Verdict C HARD REJECT terminal for V2 first-spec**). The Phase 4m
post-V2 strategy research consolidation memo is complete on this
branch (this phase).

**Recommended state remains paused. No next phase authorized.**
