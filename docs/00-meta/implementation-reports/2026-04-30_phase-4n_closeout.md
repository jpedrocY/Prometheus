# Phase 4n Closeout

## Summary

Phase 4n authored the Fresh-Hypothesis Discovery Memo (docs-only) at
`docs/00-meta/implementation-reports/2026-04-30_phase-4n_fresh-hypothesis-discovery-memo.md`
(commit `b53d1bbeba03aef1b2ba181eac5ae9f8b3c7a8a0` on branch
`phase-4n/fresh-hypothesis-discovery-memo`).

Phase 4n evaluates the four Phase 4m candidate future research
spaces — A (Structural-R trend continuation), B (Regime-first
breakout continuation), C (Funding-context trend filter), D
(Structural pullback continuation) — against the Phase 4m
18-requirement fresh-hypothesis validity gate; identifies per-
candidate rescue-risk traps and avoidance patterns; scores each on
10 dimensions; and recommends ONE candidate family for a future
docs-only strategy-spec phase.

**Phase 4n primary recommendation: Phase 4o — Regime-First Breakout
Hypothesis Spec Memo (Candidate B), docs-only.** Selected on the
basis of strongest theoretical novelty (regime-as-primary is
categorically distinct from R1a / R1b-narrow / V2 bolt-on patterns),
moderate rescue-risk (lower than A's V2-adjacent and D's R2-adjacent
traps), strong cost-sensitivity profile (regime gate naturally
avoids HIGH-cost margin trades), strong data-readiness (existing
v002 / Phase 4i datasets sufficient), enriched mechanism-check
framework (negative-test component), and Phase 3m precedent.

**Phase 4n conditional secondary: remain paused.**

**Phase 4n was docs-only.** **Phase 4n does NOT create a strategy
spec, define thresholds, define a complete rule set, run a backtest,
acquire data, or implement anything.**

**Phase 4o is NOT authorized by Phase 4n.** Authorization for Phase
4o is a separate operator decision.

**Verification:**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed in 12.77s (Phase 4n start) and 12.78s (after
  memo authoring).
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**No retained verdict revised. No project lock changed.** R3
baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 /
D1-A / V2 retained research evidence only; R2 FAILED — §11.6 cost-
sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK
FAIL — other; V2 HARD REJECT (Phase 4l, structural CFP-1 critical,
terminal for V2 first-spec); §11.6 = 8 bps HIGH per side; §1.7.3
project-level locks; mark-price stops; v002 verdict provenance;
Phase 3q mark-price 5m manifests `research_eligible: false`; Phase
3r §8 mark-price gap governance; Phase 3v §8 stop-trigger-domain
governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
governance; Phase 4j §11 metrics OI-subset partial-eligibility rule;
Phase 4k V2 backtest-plan methodology; Phase 4l Verdict C HARD
REJECT; Phase 4m 18-requirement fresh-hypothesis validity gate — all
preserved verbatim.

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
docs/00-meta/implementation-reports/2026-04-30_phase-4n_fresh-hypothesis-discovery-memo.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4n_closeout.md                          (new — this file)
```

No other files modified. No source code, tests, scripts, data,
manifests, strategy docs, runtime docs, or governance docs touched.

## Discovery conclusion

Phase 4n delivers a written candidate evaluation:

- **Four candidates evaluated** against the Phase 4m 18-requirement
  validity gate.
- **Per-candidate rescue-risk traps identified** with explicit
  avoidance patterns:
  - A trap: "V2 but with a wider stop filter";
  - B trap: "R1a / R1b-narrow but with another bolt-on regime
    filter";
  - C trap: "D1-A but with extra filters" / "D1-A-prime";
  - D trap: "R2 but with lower assumed costs".
- **Qualitative scoring matrix on 10 dimensions:** new-theory
  strength, rescue-risk, co-design clarity, data feasibility,
  mechanism-check clarity, cost-risk plausibility, expected
  sample-size feasibility, compatibility with project constraints,
  research value, recommended.
- **Primary recommendation: Phase 4o on Candidate B (Regime-First
  Breakout Hypothesis Spec Memo).** Strongest theoretical novelty
  (regime-as-primary categorically distinct from R1a / R1b-narrow /
  V2 bolt-on); moderate rescue-risk; strong cost-sensitivity
  profile (regime gate avoids HIGH-cost margin trades); strong
  data-readiness (existing v002 / Phase 4i datasets sufficient);
  enriched mechanism-check framework (negative-test component);
  Phase 3m precedent.
- **Conditional secondary: remain paused** if operator prefers not
  to commit to any candidate.

## Candidate pool considered

Exactly the four Phase 4m candidate spaces:

- **A: Structural-R trend continuation** — trend-continuation with
  setup window / structural stop / target / sizing co-designed from
  first principles. Phase 4m one-liner: "allowed if defined from
  first principles, not as V2 with widened stops".
- **B: Regime-first breakout continuation** — regime as primary
  design choice; strategy active only inside predeclared regimes.
  Phase 4m one-liner: "possible if regime is primary design choice,
  not bolt-on filter; Phase 3m precedent".
- **C: Funding-context trend filter** — funding-rate as context
  filter (avoid pathological extremes), not directional trigger.
  Phase 4m one-liner: "possible if funding is context, not
  directional trigger; structurally distinct from D1-A".
- **D: Structural pullback continuation** — pullback / retest with
  cost model and stop geometry designed together from first
  principles. Phase 4m one-liner: "possible if cost model and stop
  geometry designed together; structurally distinct from R2".

De-prioritized / rejected spaces (per Phase 4m): mean-reversion
(de-prioritized; F1 hard-rejected); market-making / HFT (rejected);
ML-first black-box forecasting (rejected); V2-prime / V2-narrow /
V2-relaxed / V2 hybrid (forbidden); F1 / D1-A / R2 rescue
(forbidden); 5m-only scalping (forbidden); paper / shadow / live
(forbidden).

## Candidate scoring matrix

Qualitative ratings: **Strong**, **Moderate**, **Weak**, **High
risk**, **Reject**.

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

## Rescue-risk analysis

Per-candidate nearest-forbidden-rescue trap and avoidance pattern:

- **A:** Trap "V2 but with a wider stop filter". Avoid by not
  starting from V2's Donchian setup; not using Phase 4l forensic
  numbers as design inputs; designing from first principles using
  trend-persistence literature (Moskowitz et al. 2012; Hurst et al.
  2017); predeclaring bounds before any data is touched.
- **B:** Trap "R1a / R1b-narrow but with another bolt-on regime
  filter". Avoid by defining regime as a top-level state machine
  (active / inactive); defining regime classifier independently of
  any per-bar trade trigger; not using V1's 8-bar setup as a
  baseline; not using 5m diagnostic findings (Q1–Q7) as regime
  indicators (Phase 3o §6 forbidden); predeclaring regime classifier
  before any data is touched.
- **C:** Trap "D1-A but with extra filters" / "D1-A-prime". Avoid by
  not using D1-A's |Z_F| ≥ 2.0 directional rule; not entering at
  funding-settlement time; not framing as contrarian signal; not
  importing V2's funding percentile bands; predeclaring funding-
  context bounds from first principles.
- **D:** Trap "R2 but with lower assumed costs". Avoid by preserving
  §11.6 HIGH = 8 bps per side verbatim; modeling entry-time slippage
  explicitly; designing pullback-confirmation geometry such that
  entry-time microstructure differs from R2's; not starting from R2's
  pullback-retest signal.

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
- **Option C: Phase 4o on Candidate A (Structural-R trend
  continuation).** NOT RECOMMENDED FIRST due to rescue-risk too
  close to V2.
- **Option D: Phase 4o on Candidate C (Funding-context trend
  filter).** NOT RECOMMENDED NOW due to V2-component / D1-A
  adjacency.
- **Option E: Phase 4o on Candidate D (Structural pullback
  continuation).** NOT RECOMMENDED NOW due to R2-adjacency and
  primarily methodological novelty.
- **Option F: Immediate strategy spec / V3.** REJECTED.
- **Option G: V2 / F1 / D1-A / R2 rescue.** REJECTED / FORBIDDEN.
- **Option H: Paper / shadow / live / exchange-write / Phase 4
  canonical.** FORBIDDEN.

**Phase 4n recommendation: Option A primary; Option B conditional
secondary.** No other options recommended.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4n/fresh-hypothesis-discovery-memo
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m mypy
.venv/Scripts/python -m pytest -q
git add docs/00-meta/implementation-reports/2026-04-30_phase-4n_fresh-hypothesis-discovery-memo.md
git commit -m "phase-4n: fresh-hypothesis discovery memo (docs-only)"
git rev-parse HEAD
git push -u origin phase-4n/fresh-hypothesis-discovery-memo
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4n_closeout.md
git commit -m "phase-4n: closeout report"
git push origin phase-4n/fresh-hypothesis-discovery-memo
```

The following commands were **NOT** run (per Phase 4n brief
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
| `ruff check .` (whole repo, Phase 4n start) | `All checks passed!` |
| `pytest` (Phase 4n start) | `785 passed in 12.77s` |
| `ruff check .` (whole repo, after memo authoring) | `All checks passed!` |
| `pytest` (after memo authoring) | `785 passed in 12.78s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean** at Phase 4n final.
No regressions relative to the post-Phase-4m-merge baseline.

## Commit

```text
Phase 4n memo commit:        b53d1bbeba03aef1b2ba181eac5ae9f8b3c7a8a0
```

The closeout commit SHA will be recorded after this file is committed.

## Final git status

To be appended after closeout commit and push.

## Final git log --oneline -5

To be appended after closeout commit and push.

## Final rev-parse

To be appended after closeout commit and push.

## Branch / main status

Phase 4n is on branch `phase-4n/fresh-hypothesis-discovery-memo`.
The branch is pushed to
`origin/phase-4n/fresh-hypothesis-discovery-memo`. **Phase 4n is NOT
merged to main.** main remains at
`40a29e1fce8f7b8828d208fe5ed8f1ead94f7eb9` (post-Phase-4m-merge
housekeeping commit).

Merge to main is not part of Phase 4n. A separate operator decision
("We are closing out Phase 4n by merging it into main") is required
to merge the branch.

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
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A / V2 all preserved verbatim.
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
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4n branch.** Per Phase 4n brief.
- **No optional ratio-column access in any code.** Phase 4n is
  text-only; no code at all.
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused** outside conditional Phase 4o
  authorization. Phase 4n deliverables exist as branch-only
  artefacts pending operator review.
- **Phase 4n output:** docs-only fresh-hypothesis discovery memo +
  this closeout artefact.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified at Phase 4n start AND after
  memo authoring).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4m all merged. Phase
  4n discovery memo on this branch.
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
  (preserved verbatim).
- **Phase 4n fresh-hypothesis discovery direction:** evaluated
  (this phase); **Candidate B (Regime-first breakout continuation)
  recommended as PRIMARY** for a future docs-only Phase 4o
  strategy-spec memo, conditional on separate operator authorization.
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
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
  **NOT merged to main.**

## Next authorization status

**No next phase has been authorized.** Phase 4n's recommendation is
**Option A (Phase 4o on Candidate B — Regime-First Breakout
Hypothesis Spec Memo, docs-only) as primary**, with **Option B
(remain paused) as conditional secondary**. Other options not
recommended / rejected / forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.
