# Phase 4m Merge Closeout

## Summary

Phase 4m has been merged into `main` via a `--no-ff` merge commit at
SHA `d1fbf877e6cdc9739505c8b9d338fc37fab64c67` and pushed to
`origin/main`. The Phase 4m Post-V2 Strategy Research Consolidation
Memo and its closeout artefact are now part of the project record on
`main`.

Phase 4m is a retrospective consolidation of the project's complete
strategy-research arc — H0 framework anchor; R3 baseline-of-record;
R1a / R1b-narrow retained non-leading; R2 FAILED — §11.6 cost-
sensitivity blocks; F1 HARD REJECT (Phase 3d-B2 terminal); D1-A
MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3j terminal); 5m
diagnostic thread operationally complete and closed (Phase 3t); V2
HARD REJECT under Phase 4l (structural CFP-1 critical, terminal for
V2 first-spec) — and consolidates what was learned, what cannot be
salvaged without violating the Phase 3t §12 validity gate, and what
conditions a genuinely new future ex-ante hypothesis must satisfy.

**Phase 4m was docs-only.** **Phase 4m does NOT propose or authorize
a new strategy spec, backtest, implementation, data acquisition, or
parameter amendment.**

**Phase 4m preserved verbatim:** R3 baseline-of-record; H0 framework
anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained research
evidence only; §11.6 = 8 bps HIGH per side; §1.7.3 project-level
locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price
5m manifests `research_eligible: false`; Phase 3r §8 mark-price gap
governance; Phase 3v §8 stop-trigger-domain governance; Phase 3w
§6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase
4a public API and runtime behavior; Phase 4e reconciliation-model
design memo; Phase 4f V2 hypothesis predeclaration; Phase 4g V2
strategy spec; Phase 4h V2 data-requirements / feasibility memo;
Phase 4i V2 acquisition + integrity report; Phase 4i metrics
manifests `research_eligible: false`; Phase 4j §11 metrics OI-subset
partial-eligibility rule; Phase 4k V2 backtest-plan methodology;
Phase 4l V2 backtest execution Verdict C HARD REJECT — all preserved
verbatim.

**Whole-repo quality gates remain clean** at Phase 4m merge: `ruff
check .` passed; pytest 785 passed; mypy strict 0 issues across 82
source files.

**Phase 4 canonical remains unauthorized.** **Phase 4n / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, and exchange-write all remain
unauthorized.**

V2 remains **pre-research only**: not implemented; not validated;
not live-ready; **not a rescue** of R3 / R2 / F1 / D1-A. **V2 first-
spec is terminally HARD REJECTED.**

**Recommended state remains paused. No next phase authorized.**

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4m_post-v2-strategy-research-consolidation.md   (new; from Phase 4m branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4m_closeout.md                                  (new; from Phase 4m branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4m_merge-closeout.md                            (new; this file; introduced by housekeeping commit)
docs/00-meta/current-project-state.md                                                                (modified; narrow Phase 4m sync; introduced by housekeeping commit)
```

No other files modified by Phase 4m, the merge, or the housekeeping
commit. No source code under `src/prometheus/`, no tests under
`tests/`, no scripts, no data under `data/raw/` or `data/normalized/`,
and no manifests under `data/manifests/` were touched.

The transient runtime file `.claude/scheduled_tasks.lock` was NOT
committed. Local gitignored Phase 4l outputs under `data/research/`
were NOT committed.

## Phase 4m commits included

```text
Phase 4m memo commit:        bb8111e58b107c82ceaf6cf7ec1c384211c1560e
Phase 4m closeout commit:    1059eb60e3580f8fa894a7985bdf5764d3be974a
```

Both commits are now in `main`'s history via the merge.

## Merge commit

```text
Merge commit:                d1fbf877e6cdc9739505c8b9d338fc37fab64c67
Merge title:                 Merge Phase 4m (post-V2 strategy research consolidation, docs-only) into main
Merge type:                  --no-ff merge of phase-4m/post-v2-strategy-research-consolidation into main
Branch merged from:          phase-4m/post-v2-strategy-research-consolidation
Branch merged into:          main
```

## Housekeeping commit

To be appended after the housekeeping commit lands on `main`.

## Final git status

To be appended after housekeeping commit and push.

## Final git log --oneline -8

To be appended after housekeeping commit and push.

## Final rev-parse

To be appended after housekeeping commit and push.

## main == origin/main confirmation

To be appended after housekeeping commit and push.

## Consolidation conclusion

- **Phase 4m was docs-only.** No source code, tests, scripts, data,
  manifests, or strategy docs were modified.
- **Phase 4m consolidated all strategy research attempted so far.**
  The consolidated record covers H0 framework anchor; R3 baseline-
  of-record; R1a / R1b-narrow retained non-leading; R2 FAILED — §11.6
  cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS /
  FRAMEWORK FAIL — other; 5m diagnostic thread closed; V2 HARD
  REJECT.
- **Phase 4m does NOT authorize a new strategy spec, backtest,
  implementation, data acquisition, or parameter amendment.** Phase
  4m is consolidation only.
- **No retained verdict is revised.** R3 / H0 / R1a / R1b-narrow /
  R2 / F1 / D1-A / V2 all preserved verbatim.
- **No project lock is changed.** §1.7.3, §11.6, mark-price stops,
  Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 3r §8, Phase 4j §11,
  Phase 4k methodology — all preserved.

## Strategy verdict map

```text
H0          → FRAMEWORK ANCHOR              (locked; preserved by Phase 4m)
R3          → BASELINE-OF-RECORD             (locked; preserved by Phase 4m)
R1a         → RETAINED — NON-LEADING        (locked; preserved by Phase 4m)
R1b-narrow  → RETAINED — NON-LEADING        (locked; preserved by Phase 4m)
R2          → FAILED — §11.6                 (locked; preserved by Phase 4m)
F1          → HARD REJECT                    (locked; preserved by Phase 4m)
D1-A        → MECHANISM PASS / FRAMEWORK FAIL (locked; preserved by Phase 4m)
5m thread   → CLOSED operationally           (locked; preserved by Phase 4m)
V2          → HARD REJECT — structural CFP-1 critical (locked; preserved by Phase 4m)
```

**Phase 4m preserves every verdict above verbatim.**

## Four rejection modes

The project has now systematically explored four orthogonal rejection
modes, each a permanent constraint on future hypotheses:

| Mode | Strategy | Binding gate | Lesson |
|---|---|---|---|
| **Cost-fragility** | R2 | §11.6 HIGH = 8 bps per side | Marginal-expectancy strategies fail under HIGH cost; cost realism mandatory. |
| **Catastrophic-floor** | F1 | Phase 3c §7.3 predicate | TARGET-subset profitability does not rescue framework when STOP-subset dominates trade count. |
| **Mechanism / framing mismatch** | D1-A | Phase 3h §11.2 cond_i / cond_iv | Information presence ≠ tradable framework; framing (trigger vs. context) determines viability. |
| **Design-stage incompatibility** | V2 | Phase 4k CFP-1 critical | Setup geometry, structural stop, target model, and position sizing must be co-designed; piecewise inheritance fails. |

## Central V2 lesson

- **V2 produced zero trades.** All 512 variants × 2 symbols × 3 cost
  cells × 3 windows = 4 608 result cells with `trade_count = 0`.
- **Raw V2 candidates existed before the stop-distance filter.** The
  8-feature AND chain (HTF bias + Donchian breakout + width
  compression + ATR regime band + range-expansion + relative volume
  + volume z-score + UTC-hour + taker imbalance + OI delta + funding
  band) produces ~15 raw long-side setups per variant per symbol over
  the 4-year coverage.
- **All raw candidates were rejected by the V1-inherited 0.60–1.80 ×
  ATR stop-distance filter.** With V2's locked 20/40-bar Donchian
  setup window per Phase 4g §29 axis 1 + Phase 4g §19 / V1 §"Stop-
  distance filter" bounds, raw candidates have stop distances around
  3–5 × ATR(20), exceeding the 1.80 × ATR upper bound.
- **The V2 20/40-bar Donchian setup naturally produced structural
  stops around 3–5 × ATR.** This is geometric: a longer setup
  lookback means setup_low (= lowest low over N1 bars) sits further
  below the breakout-bar close.
- **Setup window, structural stop, target model, and position sizing
  must be co-designed.** Phase 4m §"Stop / target / sizing lessons"
  documents the five-element interdependence: setup window N
  determines structural stop distance, which (combined with N_R)
  determines target absolute movement, which determines achievable
  trade rate, which determines statistical power.
- **This does NOT authorize V2 stop-filter widening, V2 rerun, or
  V2 rescue.** Widening the filter, removing the filter, reducing
  N1, or running V2-prime / V2-narrow / V2-relaxed / V2 hybrid would
  all be post-hoc optimization (Bailey et al. 2014) and are
  forbidden.

## Reusable lessons

15 reusable insights from cumulative research arc:

1. Trend-continuation / breakout remains plausible as a broad
   strategy family in crypto, but plain price breakout is not enough
   on BTCUSDT.
2. R2 shows partial mechanism support (M1 ✓ / M3 ✓) can still fail
   §11.6 HIGH-cost cell.
3. F1 shows profitable subsets (M3 PASS-isolated) do not rescue a
   losing full framework.
4. D1-A shows funding contains information but the contrarian
   directional framing fails framework promotion.
5. V2 shows setup geometry and stop model can invalidate a strategy
   before expectancy is even testable.
6. Cost realism (§11.6 = 8 bps HIGH per side) is necessary and
   non-negotiable.
7. Isolated mechanisms are not tradable frameworks.
8. Old assumptions must be revalidated when strategy geometry
   changes (V2's V1-stop-bound inheritance broke).
9. Setup window N determines structural stop distance, target
   absolute movement, achievable trade rate, and statistical power.
   These five elements must be co-designed.
10. Stop-distance filters can be valid trade-quality gates but must
    be calibrated to the specific setup window, not inherited.
11. Information presence ≠ tradable framework. Funding extremes
    contain information; D1-A framing did not exploit it.
12. Phase 4j §11 / Phase 3r §8 partial-eligibility governance pattern
    is reusable for any dataset family with structural integrity
    imperfections.
13. Multi-layer forbidden-input non-access verification (static scan
    + explicit column list + runtime introspection) is feasible.
14. Predeclaration discipline (Bailey et al. 2014) is binding for
    any future research.
15. Catastrophic-floor predicates (Phase 3c §7.3 / Phase 4k CFP-1
    through CFP-12) catch failures cheaply.

## Forbidden rescue observations

The following are explicitly forbidden by Phase 4m:

- **V2 with max stop-distance widened to 5 × ATR** — forbidden.
- **V2 with N1 changed (e.g., reduced from {20, 40} to a smaller
  value)** — forbidden.
- **V2 with stop-distance filter removed entirely** — forbidden.
- **V2-prime / V2-narrow / V2-relaxed / V2 hybrid** — forbidden.
- **F1 with extra filters (regime, time-of-day, funding,
  volatility); F1-prime** — forbidden.
- **D1-A with extra filters; D1-A-prime / D1-B / V1-D1 hybrid /
  F1-D1 hybrid** — forbidden.
- **R2 with cheaper costs** — forbidden (§11.6 locked).
- **Immediate backtest based on Phase 4l observed root cause** —
  forbidden.
- **Phase 4g / Phase 4j / Phase 4k methodology amendment based on
  Phase 4l result** — forbidden.

## Fresh-hypothesis validity gate

Phase 4m defines an **18-requirement validity gate** any future
ex-ante hypothesis must satisfy:

1. Named as a new hypothesis, not a rescue label.
2. Specified before any data is touched.
3. Explains why it is new in theory, not just a parameter tweak.
4. Defines entry, stop, target, sizing, cost, timeframe, and exit
   together (the Phase 4m co-design constraint).
5. Predeclares data requirements (analogous to Phase 4h).
6. Predeclares mechanism checks (analogous to Phase 4g §30 M1 / M2 /
   M3).
7. Predeclares pass / fail gates including catastrophic-floor
   predicates (analogous to Phase 4k CFP-1 through CFP-12).
8. Predeclares forbidden comparisons and forbidden rescue
   interpretations (analogous to Phase 4m §"Forbidden rescue
   observations").
9. Does NOT choose thresholds from prior failed outcomes.
10. Does NOT use Phase 4l root-cause analysis as a direct
    optimization target.
11. Preserves §11.6 cost sensitivity.
12. Preserves project locks (§1.7.3, mark-price stops, Phase 3v §8,
    Phase 3w §6 / §7 / §8, Phase 3r §8, Phase 4j §11 if metrics used,
    Phase 4k methodology if backtest authorized).
13. Commits to predeclared chronological train / validation / OOS
    holdout windows before any backtest.
14. Commits to deflated Sharpe / PBO / CSCV correction if grid
    search is involved.
15. Distinguishes mechanism evidence from framework promotion.
16. Preserves BTCUSDT-primary / ETHUSDT-comparison protocol unless
    operator explicitly authorizes a different universe.
17. Does NOT propose live-readiness or paper / shadow / Phase 4
    canonical as part of its first phase.
18. Satisfies separate operator authorization as a separately briefed
    phase.

A candidate that fails ANY of these is not a valid fresh hypothesis.

## Candidate future research spaces

Identified by Phase 4m but **NOT authorized**:

- **Structural-R trend continuation:** possible future research
  space, **not authorized**. Allowed if defined from first principles,
  not as V2 with widened stops.
- **Regime-first breakout continuation:** possible future research
  space, **not authorized**. Possible if regime is primary design
  choice, not bolt-on filter; Phase 3m precedent.
- **Funding-context trend filter:** possible future research space,
  **not authorized**. Possible if funding is context, not directional
  trigger; structurally distinct from D1-A.
- **Structural pullback continuation:** possible future research
  space, **not authorized**. Possible if cost model and stop
  geometry designed together; structurally distinct from R2.
- **Mean-reversion:** **de-prioritized**. F1 hard-rejected; future
  use requires materially new thesis.
- **Market-making / HFT:** **rejected for Prometheus now**. Not
  transferable to Prometheus substrate.
- **ML-first black-box forecasting:** **rejected for now**. Project
  remains rules-based per §1.7.3.
- **Paper / shadow / live:** **forbidden**.

**Phase 4m does NOT select any of the above as a Phase 4m output.
Phase 4m does NOT create V3, V4, or any new strategy spec. Phase
4m does NOT authorize fresh-hypothesis research.**

## Recommended next operator choice

- **Option A (PRIMARY): remain paused after consolidation.** Phase
  4m has consolidated the cumulative research arc. The current
  cumulative project state across H0 / R3 / R1a / R1b-narrow / R2 /
  F1 / D1-A / V2 means there is no live-deployable strategy
  candidate, and there is no specific next direction committed.
- **Option B (CONDITIONAL SECONDARY): authorize a separate docs-only
  fresh-hypothesis discovery memo** only if the operator explicitly
  chooses to continue research after consolidation. The discovery
  memo would NOT acquire data, NOT run backtests, NOT implement any
  code, NOT modify any prior phase artefact, and NOT propose paper /
  shadow / live.
- **Phase 4m does NOT authorize Option B.** The operator must
  separately authorize it.
- **No successor phase is started by this merge.**

Options C / D / E (V2 rescue / V2 amendment / V2 implementation) not
recommended. Option F (paper / shadow / live-readiness / deployment /
exchange-write) forbidden.

## Verification evidence

| Check | Result |
|---|---|
| `python --version` | `Python 3.12.4` |
| `ruff check .` (whole repo, Phase 4m start) | `All checks passed!` |
| `pytest` (Phase 4m start) | `785 passed in 13.21s` |
| `ruff check .` (whole repo, Phase 4m final) | `All checks passed!` |
| `pytest` (Phase 4m final) | `785 passed in 13.72s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean** at Phase 4m merge.
No regressions relative to the post-Phase-4l-merge baseline.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4n / successor phase started.**
- **No V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec
  authored.**
- **No V3 or any new strategy spec authored.**
- **No F1 / D1-A / R2 rescue spec authored.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.** Phase 4m is text-only.
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No `.claude/rules/**` modification.**
- **No data acquired.** No public Binance endpoint consulted.
- **No data modified.**
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
- **No `data/research/phase4l/**` outputs committed.** Local
  gitignored only.
- **No `.claude/scheduled_tasks.lock` committed.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A / V2 all preserved.
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
- **No optional ratio-column access in any code.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused**. Phase 4m is now part of `main`.
- **Phase 4m output:** docs-only retrospective consolidation memo +
  Phase 4m closeout + this merge-closeout file + narrow Phase 4m
  sync of `docs/00-meta/current-project-state.md`.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4m).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a through Phase 4m all
  merged.
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
- **Phase 4m post-V2 strategy research consolidation:** complete
  (this merge); cumulative research arc consolidated into project
  record.
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j)
  + backtest-plan binding (Phase 4k) + executed (Phase 4l) →
  **Verdict C HARD REJECT, terminal for V2 first-spec; consolidated
  by Phase 4m**.
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
- **Branch state:**
  `phase-4m/post-v2-strategy-research-consolidation` exists locally
  and on `origin/phase-4m/post-v2-strategy-research-consolidation`.
  The branch is now merged into `main`.

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
