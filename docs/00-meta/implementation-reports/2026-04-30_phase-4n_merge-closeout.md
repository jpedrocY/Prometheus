# Phase 4n Merge Closeout

## Summary

Phase 4n has been merged into `main` via a `--no-ff` merge commit at
SHA `d85bad22fc21f2c9e7e31809fe2e790a29a3260c` and pushed to
`origin/main`. The Phase 4n Fresh-Hypothesis Discovery Memo and its
closeout artefact are now part of the project record on `main`.

Phase 4n evaluated the four Phase 4m candidate future research
spaces — A (Structural-R trend continuation), B (Regime-first
breakout continuation), C (Funding-context trend filter), D
(Structural pullback continuation) — against the Phase 4m
18-requirement fresh-hypothesis validity gate; identified per-
candidate rescue-risk traps and avoidance patterns; scored each on
10 dimensions; and recommended ONE candidate family for a future
docs-only strategy-spec phase.

**Phase 4n primary recommendation: Phase 4o — Regime-First Breakout
Hypothesis Spec Memo (Candidate B, docs-only).** Selected on the
basis of strongest theoretical novelty (regime-as-primary
categorically distinct from R1a / R1b-narrow / V2 bolt-on patterns),
moderate rescue-risk (lower than A's V2-adjacent and D's R2-adjacent
traps), strong cost-sensitivity profile (regime gate naturally
avoids HIGH-cost margin trades), strong data-readiness (existing
v002 / Phase 4i datasets sufficient), enriched mechanism-check
framework (negative-test component), and Phase 3m precedent.

**Phase 4n conditional secondary: remain paused.**

**Phase 4n was docs-only.** **Phase 4n does NOT create a strategy
spec, define thresholds, define a complete rule set, run a backtest,
acquire data, or implement anything.** **Phase 4o is NOT authorized
by Phase 4n; authorization is a separate operator decision.**

**Phase 4n preserved verbatim:** R3 baseline-of-record; H0 framework
anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained research
evidence only; §11.6 = 8 bps HIGH per side; §1.7.3 project-level
locks; mark-price stops; v002 verdict provenance; Phase 3q mark-
price 5m manifests `research_eligible: false`; Phase 3r §8 mark-
price gap governance; Phase 3v §8 stop-trigger-domain governance;
Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance;
Phase 4a public API and runtime behavior; Phase 4e reconciliation-
model design memo; Phase 4f V2 hypothesis predeclaration; Phase 4g
V2 strategy spec; Phase 4h V2 data-requirements / feasibility memo;
Phase 4i V2 acquisition + integrity report; Phase 4i metrics
manifests `research_eligible: false`; Phase 4j §11 metrics OI-subset
partial-eligibility rule; Phase 4k V2 backtest-plan methodology;
Phase 4l V2 backtest execution Verdict C HARD REJECT; Phase 4m
18-requirement fresh-hypothesis validity gate — all preserved
verbatim.

**Whole-repo quality gates remain clean** at Phase 4n merge: `ruff
check .` passed; pytest 785 passed; mypy strict 0 issues across 82
source files.

**Phase 4 canonical remains unauthorized.** **Phase 4o / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, and exchange-write all remain
unauthorized.**

**Recommended state remains paused outside the conditional Phase 4o
spec memo. No next phase authorized.**

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4n_fresh-hypothesis-discovery-memo.md   (new; from Phase 4n branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4n_closeout.md                          (new; from Phase 4n branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4n_merge-closeout.md                    (new; this file; introduced by housekeeping commit)
docs/00-meta/current-project-state.md                                                        (modified; narrow Phase 4n sync; introduced by housekeeping commit)
```

No other files modified by Phase 4n, the merge, or the housekeeping
commit. No source code under `src/prometheus/`, no tests under
`tests/`, no scripts, no data under `data/raw/` or `data/normalized/`,
and no manifests under `data/manifests/` were touched.

The transient runtime file `.claude/scheduled_tasks.lock` was NOT
committed. Local gitignored Phase 4l outputs under `data/research/`
were NOT committed.

## Phase 4n commits included

```text
Phase 4n memo commit:        b53d1bbeba03aef1b2ba181eac5ae9f8b3c7a8a0
Phase 4n closeout commit:    96765c40dabfcde72c57431232d191446277d957
```

Both commits are now in `main`'s history via the merge.

## Merge commit

```text
Merge commit:                d85bad22fc21f2c9e7e31809fe2e790a29a3260c
Merge title:                 Merge Phase 4n (fresh-hypothesis discovery memo, docs-only) into main
Merge type:                  --no-ff merge of phase-4n/fresh-hypothesis-discovery-memo into main
Branch merged from:          phase-4n/fresh-hypothesis-discovery-memo
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

## Discovery conclusion

- **Phase 4n was docs-only.** No source code, tests, scripts, data,
  manifests, or strategy docs were modified.
- **Phase 4n evaluated four Phase 4m candidate research spaces**
  against the Phase 4m 18-requirement fresh-hypothesis validity
  gate.
- **Phase 4n does NOT authorize a strategy spec, backtest,
  implementation, data acquisition, or parameter amendment.** Phase
  4n is candidate evaluation only.
- **No retained verdict is revised.** R3 / H0 / R1a / R1b-narrow /
  R2 / F1 / D1-A / V2 all preserved verbatim.
- **No project lock is changed.** §1.7.3, §11.6, mark-price stops,
  Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 3r §8, Phase 4j §11,
  Phase 4k methodology, Phase 4m validity gate — all preserved.

## Candidate pool considered

The four Phase 4m candidate spaces:

- **A: Structural-R trend continuation** — trend-continuation with
  setup window / structural stop / target / sizing co-designed from
  first principles.
- **B: Regime-first breakout continuation** — regime as primary
  design choice; strategy active only inside predeclared regimes.
- **C: Funding-context trend filter** — funding-rate as context
  filter (avoid pathological extremes), not directional trigger.
- **D: Structural pullback continuation** — pullback / retest with
  cost model and stop geometry designed together from first
  principles.

**De-prioritized / rejected spaces** (per Phase 4m, preserved
verbatim by Phase 4n):

- **mean-reversion** — de-prioritized; F1 hard-rejected; future use
  requires materially new thesis;
- **market-making / HFT** — rejected for Prometheus now (not
  transferable to Prometheus substrate);
- **ML-first black-box forecasting** — rejected for now (project
  remains rules-based per §1.7.3);
- **V2-prime / V2-narrow / V2-relaxed / V2 hybrid** — forbidden;
- **F1 rescue** — forbidden;
- **D1-A rescue** — forbidden;
- **R2 rescue** — forbidden;
- **5m-only scalping** — forbidden;
- **paper / shadow / live** — forbidden.

## Candidate scoring matrix

Qualitative ratings on 10 dimensions; **Strong / Moderate / Weak /
High risk / Reject**.

| Dimension | A | B | C | D |
|---|---|---|---|---|
| New-theory strength | Moderate | **Strong** | Moderate | Weak |
| Rescue-risk | High risk | Moderate | Moderate-to-high | High risk |
| Co-design clarity | Strong | Strong | Moderate | Moderate |
| Data feasibility | Strong | Strong | Strong | Moderate |
| Mechanism-check clarity | Strong | **Strong (with negative-test)** | Strong | Strong |
| Cost-risk plausibility | Moderate | **Strong** | Moderate | Weak |
| Expected sample-size feasibility | Moderate | Moderate | Moderate | Moderate |
| Compatibility with project constraints | Strong | Strong | Strong | Strong |
| Research value | Moderate | **Strong** | Moderate | Weak |
| Recommended | Conditionally OK | **Recommended (primary)** | Not recommended now | Not recommended now |

**Summary:**

- **Candidate B** recommended **PRIMARY**.
- **Candidate A** **conditionally OK but not recommended first** due
  to V2-adjacent rescue risk (closest of the four to V2's design
  space; "V2 with widened stops" trap is the most obvious failure
  mode).
- **Candidate C** **not recommended now** due to D1-A / V2-component
  adjacency (funding-as-context was already a V2 component, untested
  due to V2's 0 trades; making it standalone is conceptually closer
  to "V2 component extracted" than to a genuinely new direction).
- **Candidate D** **not recommended now** due to R2-adjacent rescue
  risk and weak theoretical novelty (the novelty is primarily
  methodological — explicit cost modeling — rather than structural;
  R2's failure mode is inherent to pullback geometry on BTCUSDT).

## Rescue-risk analysis

Per-candidate nearest-forbidden-rescue trap:

- **A trap:** "V2 but with a wider stop filter."
- **B trap:** "R1a / R1b-narrow but with another bolt-on regime
  filter."
- **C trap:** "D1-A but with extra filters" / "D1-A-prime".
- **D trap:** "R2 but with lower assumed costs."

**Candidate B avoidance pattern (binding for any future Phase 4o
brief on Candidate B):**

- **Define regime as a top-level state machine** (active /
  inactive). The strategy is in one of `{regime_active,
  regime_inactive}` states; in the inactive state, no signals are
  generated regardless of bar-level conditions.
- **Define regime classifier independently of any per-bar trade
  trigger.** The regime classifier may use features (e.g., HTF
  trend slope, volatility percentile, funding pathology) but it
  produces a binary regime state, not a per-bar gate.
- **Do not use V1's 8-bar setup as a baseline reference.**
  Candidate B's regime-active-window setup geometry must be
  designed from first principles for that specific regime.
- **Do not use 5m diagnostic findings (Q1–Q7) as regime
  indicators.** Phase 3o §6 forbidden question forms preserved.
- **Predeclare regime classifier before any data is touched.**

## Recommended next operator choice

- **Option A (PRIMARY): Phase 4o — Regime-First Breakout Hypothesis
  Spec Memo (Candidate B, docs-only).** Phase 4o would predeclare:
  regime classification framework; strategy-active vs. strategy-
  inactive state machine; inside-regime co-designed entry / stop /
  target / sizing from first principles; cost-sensitivity argument
  at brief-time level; forbidden rescue interpretations; predeclared
  validity gate satisfaction. Phase 4o would NOT acquire data, NOT
  run backtests, NOT implement code, NOT propose paper / shadow /
  live.
- **Option B (CONDITIONAL SECONDARY): remain paused.** If operator
  prefers not to commit to any candidate.
- **Phase 4o is NOT started by this merge.**
- **Immediate strategy spec / V3** is **REJECTED**. Phase 4n is
  candidate evaluation only.
- **V2 / F1 / D1-A / R2 rescue** is **REJECTED / FORBIDDEN** per
  Phase 4m §"Forbidden rescue observations".
- **Paper / shadow / live / exchange-write** is **FORBIDDEN** per
  `docs/12-roadmap/phase-gates.md`.

## Verification evidence

| Check | Result |
|---|---|
| `python --version` | `Python 3.12.4` |
| `ruff check .` (whole repo, Phase 4n start) | `All checks passed!` |
| `pytest` (Phase 4n start) | `785 passed in 12.77s` |
| `ruff check .` (whole repo, after memo authoring) | `All checks passed!` |
| `pytest` (after memo authoring) | `785 passed in 12.78s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean** at Phase 4n merge.
No regressions relative to the post-Phase-4m-merge baseline.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4o / successor phase started.**
- **No V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec
  authored.**
- **No V3 or any new strategy spec authored.**
- **No F1 / D1-A / R2 rescue spec authored.**
- **No threshold grid defined.**
- **No complete entry / exit rule set defined.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.** Phase 4n is text-only.
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
  user-stream / WebSocket calls.** Phase 4n performs no network I/O.
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
- **No Phase 4f / 4g / 4h / 4i / 4j / 4k / 4l / 4m text
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

- **Recommended state:** **paused** outside conditional Phase 4o
  authorization. Phase 4n is now part of `main`.
- **Phase 4n output:** docs-only fresh-hypothesis discovery memo +
  Phase 4n closeout + this merge-closeout file + narrow Phase 4n
  sync of `docs/00-meta/current-project-state.md`.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4n).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a through Phase 4n all
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
  (preserved verbatim); 18-requirement fresh-hypothesis validity gate
  binding.
- **Phase 4n fresh-hypothesis discovery direction:** evaluated;
  **Candidate B (Regime-first breakout continuation) recommended as
  PRIMARY** for a future docs-only Phase 4o strategy-spec memo,
  conditional on separate operator authorization.
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j)
  + backtest-plan binding (Phase 4k) + executed (Phase 4l) →
  **Verdict C HARD REJECT, terminal for V2 first-spec; consolidated
  by Phase 4m**.
- **OPEN ambiguity-log items after Phase 4n:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2
  HARD REJECT (Phase 4l, structural CFP-1 critical, terminal for V2
  first-spec); §11.6 = 8 bps HIGH per side; §1.7.3 project-level
  locks; mark-price stops; v002 verdict provenance; Phase 3q
  mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4n/fresh-hypothesis-discovery-memo` exists
  locally and on `origin/phase-4n/fresh-hypothesis-discovery-memo`.
  The branch is now merged into `main`.

## Next authorization status

**No next phase has been authorized.** Phase 4n's recommendation is
**Option A (Phase 4o on Candidate B — Regime-First Breakout
Hypothesis Spec Memo, docs-only) as primary**, with **Option B
(remain paused) as conditional secondary**. Other options not
recommended / rejected / forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.
