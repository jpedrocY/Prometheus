# Phase 4m Closeout

## Summary

Phase 4m authored the Post-V2 Strategy Research Consolidation Memo
(docs-only) at
`docs/00-meta/implementation-reports/2026-04-30_phase-4m_post-v2-strategy-research-consolidation.md`
(commit `bb8111e58b107c82ceaf6cf7ec1c384211c1560e` on branch
`phase-4m/post-v2-strategy-research-consolidation`).

The memo is a retrospective consolidation covering all Prometheus
strategy research attempted to date — H0 / R3 baseline-of-record;
R1a / R1b-narrow / R2 retained research evidence; F1 HARD REJECT
(Phase 3d-B2 terminal); D1-A MECHANISM PASS / FRAMEWORK FAIL — other
(Phase 3j terminal); the 5m diagnostic thread (operationally complete
and closed per Phase 3t); and now V2 HARD REJECT under Phase 4l
(structural CFP-1 critical, terminal for V2 first-spec) — and
consolidates what was learned, what cannot be salvaged without
violating the Phase 3t §12 validity gate, and what conditions a
genuinely new future ex-ante hypothesis must satisfy.

**Phase 4m was docs-only.** **Phase 4m does NOT propose or authorize
a new strategy spec, backtest, implementation, data acquisition, or
parameter amendment.**

V2 remains **pre-research only**: not implemented; not validated;
not live-ready; **not a rescue** of R3 / R2 / F1 / D1-A. **V2
first-spec is terminally HARD REJECTED.**

**Verification (run on the post-Phase-4l-merge tree, captured by
Phase 4m):**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed in 13.21s (Phase 4m start) and 13.72s
  (Phase 4m final).
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**No retained verdict revised. No project lock changed.** R3
baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 /
D1-A / V2 retained research evidence only; R2 FAILED — §11.6
cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS /
FRAMEWORK FAIL — other; V2 HARD REJECT (Phase 4l, structural CFP-1
critical, terminal for V2 first-spec); §11.6 = 8 bps HIGH per side;
§1.7.3 project-level locks (including mark-price stops); v002
verdict provenance; Phase 3q mark-price 5m manifests
`research_eligible: false`; Phase 3r §8 mark-price gap governance;
Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8
break-even / EMA slope / stagnation governance; Phase 4a public API
and runtime behavior; Phase 4e reconciliation-model design memo;
Phase 4f V2 hypothesis predeclaration; Phase 4g V2 strategy spec;
Phase 4h V2 data-requirements / feasibility memo; Phase 4i V2
acquisition + integrity report; Phase 4i metrics manifests
`research_eligible: false`; Phase 4j §11 metrics OI-subset
partial-eligibility rule; Phase 4k V2 backtest-plan methodology;
Phase 4l V2 backtest execution Verdict C HARD REJECT — all preserved
verbatim.

**Phase 4 canonical remains unauthorized.** **Phase 4n / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, and exchange-write all remain
unauthorized.**

**Recommended state remains paused. No next phase authorized.**

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4m_post-v2-strategy-research-consolidation.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4m_closeout.md                                  (new — this file)
```

No other files modified. No source code, tests, scripts, data,
manifests, strategy docs, runtime docs, or governance docs touched.

## Consolidation conclusion

Phase 4m delivers a written consolidation of the cumulative
strategy-research arc:

- **Eight retained-evidence strategy lines tested** (H0 / R3 / R1a /
  R1b-narrow / R2 / F1 / D1-A + 5m diagnostic thread + V2). None is
  currently a live-deployable candidate.
- **Four orthogonal rejection modes documented:**
  - Cost-fragility (R2: §11.6 HIGH);
  - Catastrophic-floor (F1: Phase 3c §7.3);
  - Mechanism / framing mismatch (D1-A: Phase 3h §11.2);
  - Design-stage incompatibility (V2: Phase 4k CFP-1 critical).
- **15 reusable insights compiled** spanning trend-continuation,
  mean-reversion, funding-as-context, cost realism, mechanism
  evidence, setup / stop / target / sizing co-design, participation
  features, regime gating, partial-eligibility governance pattern,
  multi-layer non-access verification, predeclaration discipline,
  catastrophic-floor predicates, and 5m diagnostic-only role.
- **Forbidden-rescue list explicit** for V2 / F1 / D1-A / R2 and
  cross-strategy patterns; no rescue interpretation is permitted by
  Phase 4m.
- **Fresh-hypothesis validity gate** (18 binding requirements) defines
  what a future candidate must satisfy to be valid.
- **Candidate future research spaces identified but NOT authorized**
  (structural-R trend continuation; regime-first breakout; funding-
  context filter; structural pullback; mean-reversion de-prioritized;
  market-making / HFT rejected; ML-first rejected; paper / shadow /
  live forbidden).
- **V2 lesson crystallized:** V2 did not lose because trades had bad
  expectancy; V2 produced zero trades because the V1-inherited
  stop-distance filter is structurally incompatible with V2's 20/40-
  bar Donchian setup. The lesson is that setup window, structural
  stop, target model, and position sizing must be co-designed, not
  inherited piecewise. **This does NOT authorize widening the V2
  filter or rerunning V2.**

Phase 4m's central role is to ensure that any future operator
decision is grounded in the cumulative evidence rather than rhetorical
drift toward V2 rescue or hasty fresh-hypothesis commitment.

## Strategy verdict map

```text
H0          → FRAMEWORK ANCHOR              (locked; preserved)
R3          → BASELINE-OF-RECORD             (locked; preserved)
R1a         → RETAINED — NON-LEADING        (locked; preserved)
R1b-narrow  → RETAINED — NON-LEADING        (locked; preserved)
R2          → FAILED — §11.6                 (locked; preserved)
F1          → HARD REJECT                    (locked; preserved)
D1-A        → MECHANISM PASS / FW FAIL       (locked; preserved)
5m thread   → CLOSED operationally           (locked; preserved)
V2          → HARD REJECT (CFP-1 critical)   (locked; preserved)
```

**Phase 4m preserves every verdict above verbatim.**

## Reusable lessons

Distilled from the consolidation memo:

1. Trend-continuation / breakout remains plausible as a broad family,
   but plain price breakout is not enough — R3 / V1 is the cleanest
   local maximum.
2. R2 shows partial mechanism support (M1 / M3) can still fail
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

Explicitly classified as forbidden by Phase 4m:

- **V2 with max stop-distance widened to 5 × ATR.** Forbidden.
- **V2 with N1 changed from {20, 40} to a smaller value.** Forbidden.
- **V2 with stop-distance filter removed entirely.** Forbidden.
- **V2-prime / V2-narrow / V2-relaxed / V2 hybrid.** Forbidden.
- **F1 with extra filters (regime, time-of-day, funding,
  volatility).** Forbidden.
- **F1-prime.** Forbidden.
- **D1-A with extra filters.** Forbidden.
- **D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid.** Forbidden.
- **R2 with cheaper costs.** Forbidden (§11.6 locked).
- **Any immediate backtest based on Phase 4l observed root cause.**
  Forbidden.
- **Any Phase 4g / Phase 4j / Phase 4k methodology amendment based
  on Phase 4l result.** Forbidden.
- **Choosing parameters from Phase 4l forensic numbers** (e.g., "set
  filter to 3.5 × ATR because we saw 3.3 × ATR stops"). Forbidden.
- **Treating Q3 / Q6 / Q1 / Q2 5m diagnostic findings as rule
  candidates.** Forbidden.
- **Reducing the 512-variant grid in V2-derived strategies based on
  Phase 4l outcome.** Forbidden.
- **Relaxing §11.6 HIGH cost cell to make a borderline strategy
  pass.** Forbidden.
- **Skipping OOS holdout window after observing train-best variant
  performance.** Forbidden.

## Fresh-hypothesis validity gate

A future candidate must satisfy 18 binding requirements:

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

Identified but NOT authorized by Phase 4m:

- **Structural-R trend continuation** (allowed if defined from first
  principles, not as V2 with widened stops).
- **Regime-first breakout continuation** (possible if regime is a
  primary design choice, not a bolt-on filter; Phase 3m precedent).
- **Funding-context trend filter** (possible if funding is context,
  not directional trigger; structurally distinct from D1-A).
- **Structural pullback continuation** (possible if cost model and
  stop geometry designed together; structurally distinct from R2).
- **Mean-reversion (de-prioritized).** F1 hard-rejected; future use
  requires materially new thesis.
- **Market-making / HFT (rejected).** Not transferable to Prometheus
  substrate.
- **ML-first black-box forecasting (rejected).** Project remains
  rules-based per §1.7.3.
- **Paper / shadow / live (forbidden).** Per phase-gate model.

**Phase 4m does NOT select any of the above as a Phase 4m output.
Phase 4m does NOT create V3, V4, or any new strategy spec. Phase
4m does NOT authorize fresh-hypothesis research.**

## Recommended next operator choice

- **Option A (PRIMARY): remain paused after consolidation.** Phase
  4m has consolidated the cumulative research arc. The current
  cumulative project state across H0 / R3 / R1a / R1b-narrow / R2 /
  F1 / D1-A / V2 means there is no live-deployable strategy
  candidate, and there is no specific next direction committed.
  Remain paused respects the cumulative evidence.
- **Option B (CONDITIONAL SECONDARY): authorize a separate
  docs-only fresh-hypothesis discovery memo only if the operator
  wants to continue research.** The discovery memo would propose a
  fresh ex-ante hypothesis (or evaluate two or three candidates
  against the Phase 4m §"Fresh-hypothesis validity gate") and select
  ONE for further docs-only specification work. NO data acquisition,
  NO backtest, NO implementation, NO paper / shadow / live.
- **Option C (NOT RECOMMENDED): immediate V2 amendment / V2 rescue.**
- **Option D (NOT RECOMMENDED): V2-prime / V2-narrow / V2-relaxed /
  V2 hybrid spec.**
- **Option E (NOT RECOMMENDED): V2 implementation.**
- **Option F (FORBIDDEN): paper / shadow / live-readiness /
  deployment / exchange-write.**

**Phase 4m recommendation: Option A primary; Option B conditional
secondary (only if operator chooses to continue research).** No
other options recommended.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4m/post-v2-strategy-research-consolidation
git branch --show-current
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4m_post-v2-strategy-research-consolidation.md
git commit -m "phase-4m: post-V2 strategy research consolidation memo (docs-only)"
git rev-parse HEAD
git push -u origin phase-4m/post-v2-strategy-research-consolidation
git add docs/00-meta/implementation-reports/2026-04-30_phase-4m_closeout.md
git commit -m "phase-4m: closeout report"
git push origin phase-4m/post-v2-strategy-research-consolidation
```

The following commands were **NOT** run (per Phase 4m brief
prohibitions):

- No `scripts/phase3q_5m_acquisition.py` execution.
- No `scripts/phase3s_5m_diagnostics.py` execution.
- No `scripts/phase4i_v2_acquisition.py` execution.
- No `scripts/phase4l_v2_backtest.py` execution.
- No data acquisition / download / patch / regeneration.
- No diagnostic / Q1–Q7 question rerun.
- No private / authenticated REST or WebSocket request.
- No git push to main. No merge to main.

## Verification results

| Check | Result |
|---|---|
| `python --version` | `Python 3.12.4` |
| `ruff check .` (whole repo, Phase 4m start) | `All checks passed!` |
| `pytest` (Phase 4m start) | `785 passed in 13.21s` |
| `ruff check .` (whole repo, Phase 4m final) | `All checks passed!` |
| `pytest` (Phase 4m final) | `785 passed in 13.72s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean** at Phase 4m final.
No regressions relative to the post-Phase-4l-merge baseline.

## Commit

```text
Phase 4m memo commit:        bb8111e58b107c82ceaf6cf7ec1c384211c1560e
```

The closeout commit SHA will be recorded after this file is committed.

## Final git status

To be appended after closeout commit and push.

## Final git log --oneline -5

To be appended after closeout commit and push.

## Final rev-parse

To be appended after closeout commit and push.

## Branch / main status

Phase 4m is on branch
`phase-4m/post-v2-strategy-research-consolidation`. The branch is
pushed to `origin/phase-4m/post-v2-strategy-research-consolidation`.
**Phase 4m is NOT merged to main.** main remains at
`74bc2397f4d3f87025f41844f853054acf8d12d0` (post-Phase-4l-merge
housekeeping commit).

Merge to main is not part of Phase 4m. A separate operator decision
("We are closing out Phase 4m by merging it into main") is required
to merge the branch.

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
- **No Phase 4g V2 strategy-spec modification.**
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
- **No optional ratio-column access in any code.** Phase 4m is
  text-only; no code at all.
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused**. Phase 4m deliverables exist as
  branch-only artefacts pending operator review.
- **Phase 4m output:** docs-only retrospective consolidation memo +
  this closeout artefact.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified at Phase 4m start AND final).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4l all merged; Phase
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
- **Branch state:**
  `phase-4m/post-v2-strategy-research-consolidation` exists locally
  and on `origin/phase-4m/post-v2-strategy-research-consolidation`.
  **NOT merged to main.**

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
