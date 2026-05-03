# Phase 4o Closeout

## Summary

Phase 4o authored the G1 Regime-First Breakout Hypothesis Spec Memo
(docs-only) at
`docs/00-meta/implementation-reports/2026-04-30_phase-4o_regime-first-breakout-hypothesis-spec.md`
(commit `5dd9d971c5e7a4c904de1be6f7d91b15bad5211e` on branch
`phase-4o/regime-first-breakout-hypothesis-spec`).

Phase 4o defines **G1 — Regime-First Breakout Continuation** as a
genuinely new ex-ante research candidate selected by Phase 4n as
the primary fresh-hypothesis direction. G1 is conceptually distinct
from every prior Prometheus strategy line: regime as a top-level
state machine (not per-bar bolt-on filter); inside-regime entry /
stop / target / sizing co-designed from first principles per Phase
4m §"Stop / target / sizing lessons"; structural bulwark against
Candidate B's rescue trap ("R1a / R1b-narrow but with another
bolt-on regime filter") via the regime-first design principle.

**Phase 4o was hypothesis-spec, not strategy-spec.** Phase 4o defines
the conceptual layer (hypothesis name, design principles, state
machine concept, classifier constraints, candidate dimensions,
mechanism-check framework, catastrophic-floor predicates, forbidden-
rescue list); Phase 4o does NOT define final regime classifier
formula, regime state-machine transition thresholds, signal
timeframe / HTF timeframe choices, inside-regime breakout setup
geometry, stop / target / sizing thresholds, threshold grid, exact
data requirements, exact mechanism-check pass thresholds, or exact
pass / fail gate numerical bounds. Those are deferred to a future
**Phase 4p — G1 Strategy Spec Memo (docs-only)**, which Phase 4o
recommends but does NOT authorize.

**Phase 4o was docs-only.** **Phase 4o does NOT run a backtest, run
diagnostics, acquire data, modify data, modify manifests, write
implementation code, modify `src/prometheus/`, create a runnable
strategy, create V3 implementation, or authorize paper / shadow /
live / exchange-write.**

**Verification:**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed in 12.86s (Phase 4o start) and 12.87s (after
  memo authoring).
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**No retained verdict revised. No project lock changed.** R3
baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 /
D1-A / V2 retained research evidence only; §11.6 = 8 bps HIGH per
side; §1.7.3 project-level locks; mark-price stops; v002 verdict
provenance; Phase 3q mark-price 5m manifests `research_eligible:
false`; Phase 3r §8 mark-price gap governance; Phase 3v §8 stop-
trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA
slope / stagnation governance; Phase 4j §11 metrics OI-subset
partial-eligibility rule; Phase 4k V2 backtest-plan methodology;
Phase 4l V2 backtest execution Verdict C HARD REJECT (terminal for
V2 first-spec); Phase 4m 18-requirement fresh-hypothesis validity
gate; Phase 4n Candidate B avoidance pattern — all preserved
verbatim.

**Phase 4 canonical remains unauthorized.** **Phase 4p / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, and exchange-write all remain
unauthorized.**

**Recommended state remains paused outside conditional Phase 4p
spec memo. No next phase authorized.**

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4o_regime-first-breakout-hypothesis-spec.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4o_closeout.md                                 (new — this file)
```

No other files modified. No source code, tests, scripts, data,
manifests, strategy docs, runtime docs, or governance docs touched.

## Hypothesis-spec conclusion

Phase 4o delivers the conceptual hypothesis-spec layer for G1:

- **Hypothesis name:** G1 — Regime-First Breakout Continuation.
- **Core hypothesis:** breakout continuation may be viable on
  BTCUSDT perpetual futures only when the market is in a
  predeclared favorable regime determined by a top-level state
  machine on prior-completed data; outside the active regime, the
  strategy is completely inactive.
- **Regime-first design principle (binding):** 6 rules ensuring
  classifier is computed before signal evaluation, depends on prior
  data only, is independent of entry trigger, and is not tuned to
  rescue prior failures.
- **Regime state machine:** 4 conceptual states (`regime_inactive`,
  `regime_candidate`, `regime_active`, `regime_cooldown` /
  `regime_suspended`) with transitions defined at the conceptual
  level only; final transition thresholds deferred to Phase 4p.
- **Classifier design constraints:** allowed dimensions (HTF
  trend, volatility, persistence, funding context, optional OI);
  forbidden inputs (5m Q1–Q7, V2 forensic numbers, future bars,
  optional metrics ratio columns, mark-price 30m / 4h, aggTrades,
  spot, cross-venue, authenticated, discretionary); 5 binding
  classifier rules (deterministic, stateful but bounded,
  predeclared, stable, distinguishable).
- **Candidate dimensions evaluated:** trend regime; volatility
  regime; liquidity / volume regime; funding context regime;
  composite regime — qualitative evaluation only, no thresholds.
- **Inside-regime breakout concept:** N (setup window),
  structural stop, target, time-stop, position sizing all deferred
  to Phase 4p; explicit prohibitions on inheriting V1 8-bar setup,
  V2 20/40-bar Donchian setup, V1 0.60–1.80 × ATR stop bounds, V2
  8-feature AND chain.
- **Co-design principles:** five interdependent elements (setup
  window N, structural stop distance, target absolute movement,
  trade rate, sample size) must be co-designed per Phase 4m
  §"Stop / target / sizing lessons".
- **Cost-sensitivity argument:** §11.6 = 8 bps HIGH per side
  preserved verbatim; regime gating provides structural cost
  advantage (zero trades outside regime); CFP-1 binding for
  insufficient sample size.
- **Data-readiness assessment:** existing v002 / Phase 4i / v001-
  of-5m datasets sufficient for plausible G1 designs; Phase 4q
  data-requirements memo NOT required unless Phase 4p chooses
  mark-price 30m / 4h / aggTrades / 1m kline data.
- **Mechanism-check framework:** M1 (regime-validity negative
  test); M2 (regime-gating value-add over always-active baseline);
  M3 (inside-regime co-design validity); M4 (cross-symbol
  robustness). Numeric thresholds deferred to Phase 4p.
- **Negative-test framework:** active vs. inactive comparison;
  always-active baseline; optional random-regime baseline.
- **Pass / fail gate framework:** 10 conceptual gates.
- **Catastrophic-floor predicates:** 12 predicates adapted from
  Phase 4k.
- **Forbidden rescue interpretations:** explicit list of G1 rescue
  forms and forbidden Phase 4o successor actions.

Phase 4o is the conceptual layer; Phase 4p (if authorized) is the
specific layer. Phase 4o recommends Phase 4p as the primary next
operator option.

## Hypothesis name

**G1 — Regime-First Breakout Continuation.**

The "G1" prefix denotes a new strategy generation distinct from the
V-family (V1 / V2). The "1" indicates it is the first regime-first
hypothesis; future regime-first variants would be G2, G3, etc.,
subject to separate operator authorization.

**Forbidden alternative names:** V3 (V2 successor implied);
V2-prime; R3-prime; R1c; R1a-extension; R1b-extension; any name
implying direct rescue of any retained-evidence strategy.

## Regime-first design principle

Six binding rules:

1. **First decide whether the market is in a favorable regime.**
2. **Only inside the active regime can a breakout setup be
   considered.**
3. **Outside the active regime, the strategy is inactive and
   produces no candidate signals.**
4. **Regime classifier must be computed from prior-completed data
   only.**
5. **Regime classifier must not depend on whether a breakout signal
   is present.**
6. **Regime classifier must not be tuned to rescue prior failures.**

These six principles are the structural bulwark against the
Candidate B rescue trap "R1a / R1b-narrow but with another bolt-on
regime filter".

## Regime state machine

Four conceptual states (no thresholds):

- **`regime_inactive`** — strategy dormant; classifier runs;
  no entry signals computed.
- **`regime_candidate`** — early evidence of regime shift but
  unconfirmed; no entry signals computed.
- **`regime_active`** — confirmed favorable regime; entry signals
  may be computed at completed-bar boundaries.
- **`regime_cooldown` / `regime_suspended`** — post-trade or
  post-degradation pause; no new entries; existing position
  management continues.

All transitions use prior-completed bars only. No lookahead. No
mid-bar use. No future-event lookups.

## Regime classifier constraints

**Allowed dimensions:** HTF trend direction / slope; volatility
expansion / compression; trend persistence / directional
efficiency; funding context (NOT directional trigger); optional OI
context (under Phase 4j §11 only).

**Forbidden inputs:** 5m Q1–Q7 diagnostic findings; V2 Phase 4l
observed stop-distance failure numbers; any result from future
backtests; future bars; optional metrics ratio columns; mark-price
30m / 4h; `aggTrades`; spot / cross-venue data; private /
authenticated / WebSocket / user-stream data; discretionary /
manual regime labels.

**Binding classifier rules (5):** deterministic given inputs;
stateful but bounded; predeclared; stable across train / validation
/ OOS windows; distinguishable (produces all four states at
non-trivial fractions).

## Inside-regime co-design principles

The five interdependent elements (Phase 4m §"Stop / target / sizing
lessons" preserved):

1. Setup window N → structural stop distance.
2. Structural stop distance × N_R → target absolute movement.
3. Target absolute movement → achievable trade rate.
4. Trade rate × N years → sample size.
5. Sample size → CFP-1 / DSR / PBO statistical power.

Choosing N forces recalibration of the rest. **Phase 4p must
co-design these five elements from first principles for G1**, not
inherit V1's 8-bar setup or V2's 20/40-bar Donchian setup.

**Position sizing locked:** 0.25% risk per trade; 2× leverage cap;
one position max (§1.7.3).

**Stop-trigger domain locked per Phase 3v §8.**

## Data-readiness assessment

For most plausible G1 designs, existing data appears sufficient:

- v002 15m / 1h trade-price klines.
- v002 funding manifests.
- Phase 4i 30m / 4h trade-price klines.
- Phase 4i metrics OI-subset under Phase 4j §11 (only if Phase 4p
  uses OI dimension in classifier).

**Mark-price 30m / 4h, `aggTrades`, spot, cross-venue, optional
metrics ratio columns** all NOT used by G1's first-principles scope.

**Phase 4q data-requirements memo NOT strictly required** unless
Phase 4p chooses data outside the existing set.

## Mechanism-check framework

- **M1 (regime-validity negative test):** active-regime population's
  expectancy > inactive-regime "would-have-been" population's
  expectancy. **Failure of M1** means the regime classifier
  doesn't sort outcomes meaningfully; the regime hypothesis is
  wrong.
- **M2 (regime-gating value-add over always-active baseline):**
  G1 expectancy at HIGH-cost > always-active baseline expectancy
  at HIGH-cost.
- **M3 (inside-regime co-design validity):** trade count adequate;
  positive expectancy at MEDIUM cost; CFP-1 / CFP-2 / CFP-3 not
  triggered.
- **M4 (cross-symbol robustness):** BTCUSDT primary passes M1 / M2 /
  M3; ETHUSDT comparison shows directional support; ETH cannot
  rescue BTC.

Phase 4p must commit specific numeric thresholds.

## Negative-test framework

The negative-test component of M1 is critical for regime-first.
Without it, an illusory regime classifier can pass undetected.

**Required negative-test components for any future Phase 4p
backtest:**

1. Active vs. inactive comparison (the M1 core test).
2. Always-active baseline comparison (the M2 core test).
3. Optional random-regime baseline (additional safeguard).

**Failure modes:** inactive-regime equally favorable; sample size
collapse from regime gating; train-only success.

## Forbidden rescue interpretations

- **G1 ≠ R1a / R1b-narrow with another regime filter.**
- **G1 ≠ V2 with fewer gates / regime filter / stop-distance
  rescue.**
- **G1 ≠ F1 / D1-A / R2 rescue.**
- **5m Q1–Q7 not regime indicators.**
- **No regime thresholds chosen from V1 / V2 failure observations.**
- **No immediate backtest, data acquisition, or implementation from
  Phase 4o.**
- **No paper / shadow / live from Phase 4o.**

## Recommended next operator choice

- **Option A (PRIMARY): Phase 4p — G1 Strategy Spec Memo (docs-
  only).** Phase 4p would predeclare the specific regime classifier
  formula, regime state machine transitions, signal timeframe / HTF
  timeframe, inside-regime breakout setup geometry, stop / target /
  sizing co-design, threshold grid (if any) with deflated Sharpe /
  PBO / CSCV commitment, exact data requirements, exact M1 / M2 /
  M3 / M4 mechanism-check thresholds, exact CFP-1..CFP-12
  thresholds, exact validation windows, and explicit per-G1-design
  forbidden-rescue interpretations.
- **Option B (CONDITIONAL SECONDARY): remain paused.**
- **Option C (NOT RECOMMENDED unless data-readiness blocker):**
  Phase 4q data-requirements memo first.
- **Option D (REJECTED):** immediate G1 backtest (data-snooping).
- **Option E (REJECTED / FORBIDDEN):** V2 / F1 / D1-A / R2 rescue.
- **Option F (FORBIDDEN):** paper / shadow / live / exchange-write /
  Phase 4 canonical.

**Phase 4o recommendation: Option A primary; Option B conditional
secondary.** No other options recommended.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4o/regime-first-breakout-hypothesis-spec
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m mypy
.venv/Scripts/python -m pytest -q
git add docs/00-meta/implementation-reports/2026-04-30_phase-4o_regime-first-breakout-hypothesis-spec.md
git commit -m "phase-4o: G1 regime-first breakout hypothesis-spec memo (docs-only)"
git rev-parse HEAD
git push -u origin phase-4o/regime-first-breakout-hypothesis-spec
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4o_closeout.md
git commit -m "phase-4o: closeout report"
git push origin phase-4o/regime-first-breakout-hypothesis-spec
```

The following commands were **NOT** run (per Phase 4o brief
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
| `ruff check .` (whole repo, Phase 4o start) | `All checks passed!` |
| `pytest` (Phase 4o start) | `785 passed in 12.86s` |
| `ruff check .` (whole repo, after memo authoring) | `All checks passed!` |
| `pytest` (after memo authoring) | `785 passed in 12.87s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean** at Phase 4o final.
No regressions relative to the post-Phase-4n-merge baseline.

## Commit

```text
Phase 4o memo commit:        5dd9d971c5e7a4c904de1be6f7d91b15bad5211e
```

The closeout commit SHA will be recorded after this file is committed.

## Final git status

To be appended after closeout commit and push.

## Final git log --oneline -5

To be appended after closeout commit and push.

## Final rev-parse

To be appended after closeout commit and push.

## Branch / main status

Phase 4o is on branch
`phase-4o/regime-first-breakout-hypothesis-spec`. The branch is
pushed to `origin/phase-4o/regime-first-breakout-hypothesis-spec`.
**Phase 4o is NOT merged to main.** main remains at
`3f71d5e1c7d7d47504ca8f92b19a11373c4cfd24` (post-Phase-4n-merge
housekeeping commit).

Merge to main is not part of Phase 4o. A separate operator decision
("We are closing out Phase 4o by merging it into main") is required
to merge the branch.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4p / successor phase started.**
- **No V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec
  authored.**
- **No V3 or any new strategy spec authored.**
- **No F1 / D1-A / R2 rescue spec authored.**
- **No threshold grid defined.**
- **No complete entry / exit rule set defined.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.** Phase 4o is text-only.
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
  user-stream / WebSocket calls.** Phase 4o performs no network I/O.
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
- **No Phase 4f / 4g / 4h / 4i / 4j / 4k / 4l / 4m / 4n text
  modification.**
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
  Phase 4o branch.** Per Phase 4o brief.
- **No optional ratio-column access in any code.** Phase 4o is
  text-only.
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused** outside conditional Phase 4p
  authorization. Phase 4o deliverables exist as branch-only
  artefacts pending operator review.
- **Phase 4o output:** docs-only hypothesis-spec memo + this
  closeout artefact.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified at Phase 4o start AND after memo
  authoring).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4n all merged. Phase
  4o hypothesis-spec memo on this branch.
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
  (preserved verbatim); 18-requirement fresh-hypothesis validity
  gate binding.
- **Phase 4n fresh-hypothesis discovery:** complete (preserved
  verbatim); Candidate B selected as primary.
- **G1 — Regime-First Breakout Continuation hypothesis:**
  predeclared by Phase 4o (this phase) as a new ex-ante research
  candidate. Conditional on separate operator authorization, Phase
  4p would proceed to a docs-only G1 strategy-spec memo.
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **OPEN ambiguity-log items after Phase 4o:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2
  HARD REJECT (Phase 4l, structural CFP-1 critical, terminal for V2
  first-spec); §11.6 = 8 bps HIGH per side; §1.7.3 project-level
  locks; mark-price stops; v002 verdict provenance; Phase 3q
  mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4o/regime-first-breakout-hypothesis-spec`
  exists locally and on
  `origin/phase-4o/regime-first-breakout-hypothesis-spec`. **NOT
  merged to main.**

## Next authorization status

**No next phase has been authorized.** Phase 4o's recommendation is
**Option A (Phase 4p — G1 Strategy Spec Memo, docs-only) as
primary**, with **Option B (remain paused) as conditional
secondary**. Other options not recommended / rejected / forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.
