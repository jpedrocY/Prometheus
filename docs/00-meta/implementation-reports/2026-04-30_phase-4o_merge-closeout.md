# Phase 4o Merge Closeout

## Summary

Phase 4o has been merged into `main` via a `--no-ff` merge commit at
SHA `a60ec81242d2ab5b88d9bd0a0b9e57f8dceb4778` and pushed to
`origin/main`. The Phase 4o G1 Regime-First Breakout Hypothesis Spec
Memo and its closeout artefact are now part of the project record on
`main`.

Phase 4o defined **G1 — Regime-First Breakout Continuation** as a
genuinely new ex-ante research candidate, selected by Phase 4n as
the primary fresh-hypothesis direction after Phase 4l's V2 HARD
REJECT and Phase 4m's consolidation. G1 is conceptually distinct
from every prior Prometheus strategy line: regime as a top-level
state machine (not per-bar bolt-on filter); inside-regime entry /
stop / target / sizing co-designed from first principles per Phase
4m §"Stop / target / sizing lessons"; six binding regime-first
principles forming the structural bulwark against Candidate B's
rescue trap "R1a / R1b-narrow but with another bolt-on regime
filter".

**Phase 4o was hypothesis-spec, not strategy-spec.** Phase 4o
defined the conceptual layer (hypothesis name; design principles;
state machine concept; classifier constraints; candidate dimensions;
mechanism-check framework; catastrophic-floor predicates;
forbidden-rescue list); Phase 4o did NOT define final regime
classifier formula, regime state-machine transition thresholds,
signal timeframe / HTF timeframe choices, inside-regime breakout
setup geometry, stop / target / sizing thresholds, threshold grid,
exact data requirements, exact mechanism-check pass thresholds, or
exact pass / fail gate numerical bounds. Those are deferred to a
future **Phase 4p — G1 Strategy Spec Memo (docs-only)**, which
Phase 4o recommends but does NOT authorize.

**Phase 4o was docs-only.** **Phase 4o does NOT run a backtest, run
diagnostics, acquire data, modify data, modify manifests, write
implementation code, modify `src/prometheus/`, create a runnable
strategy, create V3 implementation, or authorize paper / shadow /
live / exchange-write.**

**Phase 4o preserved verbatim:** R3 baseline-of-record; H0 framework
anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained research
evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD
REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2 HARD
REJECT (Phase 4l, structural CFP-1 critical, terminal for V2
first-spec); §11.6 = 8 bps HIGH per side; §1.7.3 project-level
locks; mark-price stops; v002 verdict provenance; Phase 3q mark-
price 5m manifests `research_eligible: false`; Phase 3r §8 mark-
price gap governance; Phase 3v §8 stop-trigger-domain governance;
Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
governance; Phase 4a public API and runtime behavior; Phase 4e
reconciliation-model design memo; Phase 4f V2 hypothesis
predeclaration; Phase 4g V2 strategy spec; Phase 4h V2 data-
requirements / feasibility memo; Phase 4i V2 acquisition + integrity
report; Phase 4i metrics manifests `research_eligible: false`; Phase
4j §11 metrics OI-subset partial-eligibility rule; Phase 4k V2
backtest-plan methodology; Phase 4l V2 backtest execution Verdict C
HARD REJECT; Phase 4m 18-requirement fresh-hypothesis validity gate;
Phase 4n Candidate B avoidance pattern — all preserved verbatim.

**Whole-repo quality gates remain clean** at Phase 4o merge: `ruff
check .` passed; pytest 785 passed; mypy strict 0 issues across 82
source files.

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
docs/00-meta/implementation-reports/2026-04-30_phase-4o_regime-first-breakout-hypothesis-spec.md   (new; from Phase 4o branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4o_closeout.md                                (new; from Phase 4o branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4o_merge-closeout.md                          (new; this file; introduced by housekeeping commit)
docs/00-meta/current-project-state.md                                                              (modified; narrow Phase 4o sync; introduced by housekeeping commit)
```

No other files modified by Phase 4o, the merge, or the housekeeping
commit. No source code under `src/prometheus/`, no tests under
`tests/`, no scripts, no data under `data/raw/` or `data/normalized/`,
and no manifests under `data/manifests/` were touched.

The transient runtime file `.claude/scheduled_tasks.lock` was NOT
committed. Local gitignored Phase 4l outputs under `data/research/`
were NOT committed.

## Phase 4o commits included

```text
Phase 4o memo commit:        5dd9d971c5e7a4c904de1be6f7d91b15bad5211e
Phase 4o closeout commit:    17bd410b193dadfac3e534945377c11a12c9edb7
```

Both commits are now in `main`'s history via the merge.

## Merge commit

```text
Merge commit:                a60ec81242d2ab5b88d9bd0a0b9e57f8dceb4778
Merge title:                 Merge Phase 4o (G1 regime-first breakout hypothesis-spec memo, docs-only) into main
Merge type:                  --no-ff merge of phase-4o/regime-first-breakout-hypothesis-spec into main
Branch merged from:          phase-4o/regime-first-breakout-hypothesis-spec
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

## Hypothesis-spec conclusion

- **Phase 4o was docs-only.** No source code, tests, scripts, data,
  manifests, or strategy docs were modified.
- **Phase 4o defines G1 — Regime-First Breakout Continuation as a
  new ex-ante research candidate.**
- **Phase 4o is hypothesis-spec only, not strategy-spec.** Phase 4o
  defines the conceptual layer; specific thresholds / classifier
  formula / state-machine transitions / inside-regime entry rules /
  stop-target-sizing / threshold grid / data requirements / pass-
  fail gates are deferred to a future Phase 4p strategy-spec memo.
- **Phase 4o does NOT authorize Phase 4p.** Authorization for Phase
  4p is a separate operator decision.
- **Phase 4o does NOT authorize backtest, implementation, data
  acquisition, paper / shadow / live, or exchange-write.**
- **No retained verdict is revised.** R3 / H0 / R1a / R1b-narrow /
  R2 / F1 / D1-A / V2 all preserved verbatim.
- **No project lock is changed.** §1.7.3, §11.6, mark-price stops,
  Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 3r §8, Phase 4j §11,
  Phase 4k methodology, Phase 4m 18-requirement validity gate,
  Phase 4n Candidate B avoidance pattern — all preserved.

## Hypothesis name

**G1 — Regime-First Breakout Continuation.**

The "G1" prefix denotes a new strategy generation distinct from the
V-family (V1 / V2). The "1" indicates it is the first regime-first
hypothesis; future regime-first variants would be G2, G3, etc.,
subject to separate operator authorization.

**Forbidden alternative names:** V3 (V2 successor implied);
V2-prime; R3-prime; R1c; R1a-extension; R1b-extension; or any name
implying direct rescue.

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

Four conceptual states (no thresholds; transition criteria deferred
to Phase 4p):

- **`regime_inactive`** — strategy dormant; classifier runs;
  no entry signals computed.
- **`regime_candidate`** — early evidence of regime shift but
  unconfirmed; no entry signals computed.
- **`regime_active`** — confirmed favorable regime; entry signals
  may be computed at completed-bar boundaries.
- **`regime_cooldown` / `regime_suspended`** — post-trade or
  post-degradation pause; no new entries; existing position
  management continues.

**All transitions use prior-completed bars only.** No lookahead. **No
entry signals are computed outside `regime_active`.**

## Regime classifier constraints

**Allowed dimensions:**

- HTF trend direction / slope;
- volatility expansion / compression;
- trend persistence / directional efficiency;
- funding context as risk-context only, not directional trigger;
- optional OI context only if Phase 4j §11 is preserved.

**Forbidden inputs:**

- 5m Q1–Q7 diagnostic findings;
- V2 Phase 4l observed stop-distance failure numbers;
- future bars;
- optional metrics ratio columns;
- mark-price 30m / 4h unless separately authorized;
- aggTrades unless separately authorized;
- spot / cross-venue data;
- private / authenticated / WebSocket / user-stream data;
- discretionary / manual labels.

**Five binding classifier rules:** deterministic given inputs;
stateful but bounded; predeclared; stable across train / validation /
OOS windows; distinguishable (produces all four states at non-trivial
fractions).

## Inside-regime co-design principles

Per Phase 4m §"Stop / target / sizing lessons" preserved:

- **Setup window N, structural stop, target absolute movement,
  trade rate, and sample size must be co-designed.** Choosing N
  forces recalibration of the others.
- **Position sizing remains fixed-risk:**
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max.
- **Stop-distance bounds, if any, must be justified from active-
  regime structure** — NOT inherited from V1 / V2 / R1a / R1b /
  R2 / F1 / D1-A.

**Phase 4o forbids default inheritance of:**

- V1 8-bar setup;
- V2 20/40-bar Donchian;
- V1 0.60–1.80 × ATR stop-distance filter;
- V2 8-feature AND chain.

R2 pullback-retest entry, F1 mean-reversion logic, and D1-A
funding-Z-score directional rule are also forbidden as defaults.

## Data-readiness assessment

- **Existing v002 / Phase 4i / v001-of-5m datasets appear sufficient
  for plausible G1 designs:**
  - v002 15m / 1h trade-price klines;
  - v002 funding manifests;
  - Phase 4i 30m / 4h trade-price klines;
  - Phase 4i metrics OI-subset under Phase 4j §11 (only if needed).
- **Phase 4q data-requirements memo NOT strictly required** unless
  Phase 4p chooses unavailable data (mark-price 30m / 4h,
  aggTrades, or 1m kline data).
- **No acquisition authorized** by Phase 4o. Phase 4p must reuse
  existing data, OR a separate Phase 4q must be authorized before
  any acquisition.

## Mechanism-check framework

Phase 4o defines four mechanism checks at the conceptual level
(numeric thresholds deferred to Phase 4p):

- **M1 — Regime-validity negative test.** Active-regime population's
  expectancy > inactive-regime "would-have-been" population's
  expectancy. Failure of M1 means the regime classifier doesn't
  sort outcomes meaningfully; the regime hypothesis is wrong.
- **M2 — Regime-gating value-add over always-active baseline.** G1
  expectancy at HIGH-cost > always-active baseline expectancy at
  HIGH-cost.
- **M3 — Inside-regime co-design validity.** Trade count adequate;
  positive expectancy at MEDIUM cost; CFP-1 / CFP-2 / CFP-3 not
  triggered.
- **M4 — Cross-symbol robustness.** BTCUSDT primary passes M1 / M2 /
  M3; ETHUSDT comparison shows directional support; ETH cannot
  rescue BTC.

**Numeric thresholds deferred to Phase 4p.**

## Negative-test framework

The negative-test component of M1 is critical for regime-first.
Without it, an illusory regime classifier can pass undetected.

**Required negative-test components for any future Phase 4p / Phase
4t-equivalent backtest:**

1. **Active-vs-inactive comparison** (the M1 core test).
2. **Always-active baseline comparison** (the M2 core test).
3. **Optional random-regime baseline** (additional safeguard).

**Failure modes:**

- **Inactive regime equally favorable** (or better): regime
  hypothesis fails.
- **Sample-size collapse from regime gating**: CFP-1-analogous
  triggers; hypothesis fails.

## Forbidden rescue interpretations

- **G1 is not R1a / R1b-narrow with another filter.** R1a / R1b are
  per-bar bolt-on filters; G1 is regime-first state-machine gating.
- **G1 is not V2 with fewer gates.** V2's 8-feature AND chain is
  explicitly excluded.
- **G1 is not V2 with a regime filter.** Same.
- **G1 is not V2 stop-distance rescue.** G1's stop bounds are
  derived from active-regime volatility, not from V2's Phase 4l
  forensic numbers.
- **G1 is not F1 / D1-A / R2 rescue.** G1 is trend-continuation; F1
  / D1-A / R2 are different families.
- **5m Q1–Q7 cannot be used as regime indicators.** Phase 3o §6
  forbidden question forms preserved.
- **No regime thresholds chosen from prior failed outcomes.**
  Bailey et al. 2014 / Phase 4m anti-data-snooping discipline.
- **No immediate backtest, data acquisition, implementation, paper /
  shadow / live** from Phase 4o.

## Recommended next operator choice

- **Option A (PRIMARY): Phase 4p — G1 Strategy Spec Memo (docs-
  only).** Phase 4p would predeclare the specific regime classifier
  formula, regime state machine transitions, signal / HTF timeframe,
  inside-regime breakout setup geometry, stop / target / sizing
  co-design, threshold grid (if any) with deflated Sharpe / PBO /
  CSCV commitment, exact data requirements, exact M1 / M2 / M3 /
  M4 mechanism-check thresholds, exact CFP-1..CFP-12 thresholds,
  exact validation windows, and explicit per-G1-design forbidden-
  rescue interpretations.
- **Option B (CONDITIONAL SECONDARY): remain paused.**
- **Phase 4p is NOT started by this merge.**
- **Immediate backtest is REJECTED.**
- **Data acquisition is REJECTED** unless a future Phase 4p finds a
  data-readiness blocker AND a separate Phase 4q is authorized.
- **V2 / F1 / D1-A / R2 rescue is REJECTED / FORBIDDEN** per
  Phase 4m §"Forbidden rescue observations".
- **Paper / shadow / live / exchange-write is FORBIDDEN** per
  `docs/12-roadmap/phase-gates.md`.

## Verification evidence

| Check | Result |
|---|---|
| `python --version` | `Python 3.12.4` |
| `ruff check .` (whole repo, Phase 4o start) | `All checks passed!` |
| `pytest` (Phase 4o start) | `785 passed in 12.86s` |
| `ruff check .` (whole repo, after memo authoring) | `All checks passed!` |
| `pytest` (after memo authoring) | `785 passed in 12.87s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean** at Phase 4o merge.
No regressions relative to the post-Phase-4n-merge baseline.

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
- **No `scripts/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No `.claude/rules/**` modification.**
- **No data acquired.**
- **No data modified.**
- **No public Binance endpoint consulted.**
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
- **No `data/research/phase4l/**` outputs committed.**
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
- **No optional ratio-column access in any code.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused** outside conditional Phase 4p
  authorization. Phase 4o is now part of `main`.
- **Phase 4o output:** docs-only hypothesis-spec memo + Phase 4o
  closeout + this merge-closeout file + narrow Phase 4o sync of
  `docs/00-meta/current-project-state.md`.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4o).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a through Phase 4o all
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
  (preserved verbatim); 18-requirement fresh-hypothesis validity
  gate binding.
- **Phase 4n fresh-hypothesis discovery:** complete (preserved
  verbatim); Candidate B selected as primary.
- **G1 — Regime-First Breakout Continuation hypothesis:**
  predeclared by Phase 4o (this merge) as a new ex-ante research
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
- **Branch state:**
  `phase-4o/regime-first-breakout-hypothesis-spec` exists locally
  and on `origin/phase-4o/regime-first-breakout-hypothesis-spec`.
  The branch is now merged into `main`.

## Next authorization status

**No next phase has been authorized.** Phase 4o's recommendation is
**Option A (Phase 4p — G1 Strategy Spec Memo, docs-only) as
primary**, with **Option B (remain paused) as conditional
secondary**. Other options not recommended / rejected / forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.
