# Phase 4g Closeout

## Summary

Phase 4g (V2 Strategy-Spec Memo: Participation-Confirmed Trend
Continuation) is **complete on the Phase 4g branch and not merged
to main**. Phase 4g operationalized the Phase 4f V2 candidate
hypothesis family into a precise, predeclared, bounded strategy
specification suitable for future data-requirements / backtest planning
phases.

Phase 4g is **docs-only**. No source code, tests, scripts, data,
manifests, specs, thresholds, parameters, project locks, or prior
verdicts were modified. No data was acquired. No backtests were run.

V2 remains **pre-research only**: not implemented; not backtested;
not validated; not live-ready; **not a rescue** of R3 / R2 / F1 /
D1-A.

Phase 4g recommendation: **Phase 4h V2 Data Requirements and
Feasibility Memo (docs-only)** primary; **remain paused** conditional
secondary. **No** immediate data acquisition; **no** immediate
backtest; **no** implementation; **no** paper / shadow / live /
exchange-write.

## Files changed

The Phase 4g branch introduces two new docs-only files relative to
`main`:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4g_v2-participation-confirmed-trend-continuation-spec.md`
  (Phase 4g V2 strategy-spec memo; 39 sections)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4g_closeout.md`
  (this file)

`docs/00-meta/current-project-state.md` is **NOT modified** on the
Phase 4g branch (per the Phase 4g brief). It would be updated only
during the merge housekeeping commit, after a separate operator
authorization.

No source code, tests, scripts, data, manifests, specs, thresholds,
parameters, project locks, or prior verdicts were modified by Phase
4g.

## V2 strategy-spec conclusion

Phase 4g locks the V2 design space at the spec level so that any
future V2 data-requirements / backtest / implementation phase
(separately authorized) MUST operate inside the bounds Phase 4g sets.
This is the same anti-data-snooping discipline the project applied to
the Phase 3o predeclared 5m diagnostic question set: commit the
design *before* any data is acquired or any backtest is run, so
parameters cannot be selected after observing outcomes
(Bailey/Borwein/López de Prado/Zhu 2014).

Phase 4g preserves all prior retained-evidence verdicts verbatim
(R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1
HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other) and
preserves all project-level locks (§1.7.3 BTCUSDT primary; one-symbol
live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops;
§11.6 = 8 bps HIGH per side; v002 verdict provenance; Phase 3q
mark-price 5m manifests `research_eligible: false`; Phase 3v §8
stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even /
EMA slope / stagnation governance; Phase 4a public API and runtime
behavior; Phase 4e reconciliation-model design memo; Phase 4f V2
hypothesis predeclaration).

V2 is structurally distinct from R3 / R2 / F1 / D1-A. Phase 4g §6
records the differences explicitly: V2 uses 30m signal vs. V1's 15m;
4h bias vs. V1's 1h; Donchian-channel-based trend state vs. V1's
EMA(50)/(200) state; longer compression lookback; REQUIRES participation
/ volume confirmation (which V1 does not); REQUIRES non-pathological
derivatives-flow context (which V1 does not). V2 is symmetric long /
short with a trend-continuation directional bias, NOT a contrarian
funding trade like D1-A.

## Selected timeframe matrix

Phase 4g §11 selects exactly one timeframe per role from the Phase 4f
§24 candidate matrix:

| Role | Selected | Phase 4f candidate set |
|---|---|---|
| Signal timeframe | **30m** | 15m / 30m / 1h |
| Higher-timeframe bias | **4h** | 1h / 4h |
| Session / volume bucket | **1h** | 30m / 1h |
| 5m | **diagnostic-only, not primary signal** | 5m diagnostic-only |

Reasoning is grounded in Phase 4f's external evidence (Moskowitz / Ooi
/ Pedersen 2012; Hurst / Ooi / Pedersen 2017; Brock / Lakonishok /
LeBaron 1992; Liu / Tsyvinski 2018 / 2021; Hattori 2024; Eross /
Urquhart / Wolfe 2019), NOT in any internal Phase 3s pattern.

## Selected feature set

Phase 4g §28 selects exactly 8 active V2 entry features and 3 active
V2 exit / regime features, matching the Phase 4f §23 bound exactly:

**Entry features (8):**

1. HTF trend bias state (4h EMA(20)/(50) discrete comparison).
2. Donchian breakout state (signal-timeframe Donchian high(N1) / low(N1)).
3. Donchian width percentile (compression precondition).
4. Range-expansion ratio (breakout-bar TR vs. trailing mean).
5. Relative volume + volume z-score.
6. Volume percentile by UTC hour (controls intraday seasonality).
7. Taker buy/sell imbalance.
8. OI delta direction + funding-rate percentile band.

**Exit / regime features (3):**

1. Time-since-entry counter (drives unconditional time-stop).
2. ATR percentile regime (volatility regime; recorded, not acted on as
   exit).
3. HTF bias state continuity (recorded, not acted on as exit).

**Optional features documented but NOT activated by Phase 4g:**
long/short ratio; mark-price vs. trade-price divergence; breakout
close location; HH/HL structure.

## Threshold-grid summary

Phase 4g §29 predeclares the threshold grid for each chosen feature.
The full grid is recorded in §29 of the spec. Total combinatorial
search-space cardinality:

`2 × 2 × 2 × 2 × 2 × 2 × 2 × 2 × 2 = 2^9 = 512 variants.`

The 9 non-fixed grid axes are: N1 (Donchian breakout lookback);
P_w max (Donchian width percentile cap); V_rel_min (relative volume
min); V_z_min (volume z-score min); T_imb_min (taker-imbalance min);
OI_dir (OI delta direction policy); funding band; N_R (fixed-R
take-profit); T_stop (time-stop horizon).

512 is at the upper bound of what PBO / deflated Sharpe machinery
handles cleanly. Phase 4g §29 flags this and requires the future V2
backtest phase to either reduce the search space further or apply the
full PBO / deflated Sharpe / CSCV machinery per Bailey/Borwein/López
de Prado/Zhu 2014.

**No threshold may be selected from backtest outcomes.** Phase 4g
commits the grid; the backtest phase reports the per-variant outcome;
the choice of "best" variant must be subject to deflated Sharpe /
PBO correction, not raw in-sample Sharpe.

## Governance-label declarations

Phase 4g §22–§24 declare all four governance labels explicitly per
Phase 3v §8 and Phase 3w §6 / §7 / §8:

- `stop_trigger_domain` (research): **`trade_price_backtest`**.
- `stop_trigger_domain` (future runtime / paper / live, if ever
  authorized): **`mark_price_runtime`**.
- `stop_trigger_domain` (future live-readiness validation step, if ever
  authorized): **`mark_price_backtest_candidate`**.
- `stop_trigger_domain` (`mixed_or_unknown`): **invalid / fail-closed
  at any decision boundary** (Phase 3v §8.4).
- `break_even_rule`: **`disabled`** for the first V2 spec.
- `ema_slope_method`: **`discrete_comparison`**.
- `stagnation_window_role`: **`metric_only`** (no active rule;
  observed-but-not-acted-on, to support future regime analysis).
- `mixed_or_unknown` is invalid and fails closed for all four schemes.

Phase 4g does NOT modify Phase 3v or Phase 3w governance.

## Candidate next-slice decision

Phase 4g §38 presents the operator decision menu:

- **Option A — Remain paused.** Procedurally acceptable; Phase 4g
  deliverables exist as branch artefacts. Defers Phase 4h.
- **Option B — Phase 4h V2 Data Requirements and Feasibility Memo
  (docs-only).** **PRIMARY RECOMMENDATION.** Operationalize §12 / §32:
  enumerate exact bulk-archive datasets needed; specify SHA256-verified
  acquisition plan analogous to Phase 3q; specify dataset-versioning
  convention; specify integrity-check rules; predeclare invalid-window
  handling; do NOT acquire data. Phase 4h would itself be docs-only.
- **Option C — Immediate V2 data acquisition.** **NOT RECOMMENDED.**
  Inverts the standard Phase 3p → Phase 3q ordering.
- **Option D — Immediate V2 backtest.** **REJECTED.** Cannot be done
  before data is acquired AND would be data-snooping.
- **Option E — V2 implementation.** **REJECTED.** Requires successful
  backtest evidence (which does not exist) AND a separate authorization
  (which does not exist).
- **Option F — Paper / shadow / live-readiness / exchange-write.**
  **FORBIDDEN.** Per `docs/12-roadmap/phase-gates.md`, none of these
  gates is met.

**Phase 4g recommendation: Option B (Phase 4h V2 Data Requirements and
Feasibility Memo, docs-only) primary; Option A (remain paused)
conditional secondary.** No further options recommended.

## Commands run

The following commands were run during Phase 4g per the Phase 4g brief:

| # | Command | Purpose |
|---|---|---|
| 1 | `git status` | Verify clean tree pre-branch and pre-spec |
| 2 | `git checkout -b phase-4g/v2-participation-confirmed-trend-continuation-spec` | Create Phase 4g branch |
| 3 | `git rev-parse main`, `git rev-parse origin/main` | Verify main == origin/main at 0d0d43f |
| 4 | `.venv/Scripts/python --version` | Confirm Python toolchain |
| 5 | `.venv/Scripts/python -m ruff check .` | Verify whole-repo Ruff clean |
| 6 | `.venv/Scripts/python -m pytest -q` | Verify whole-repo pytest clean |
| 7 | `.venv/Scripts/python -m mypy` | Verify mypy strict clean |
| 8 | `git add ... && git commit -m ...` | Commit Phase 4g report |
| 9 | `git push -u origin phase-4g/...` | Push Phase 4g branch |

The following commands were **NOT** run (per Phase 4g brief
prohibitions):

- No `scripts/phase3q_5m_acquisition.py` execution.
- No `scripts/phase3s_5m_diagnostics.py` execution.
- No backtest execution.
- No diagnostics execution.
- No data acquisition.
- No public Binance endpoint consulted in code.

## Verification results

| Check | Result |
|---|---|
| `.venv/Scripts/python --version` | `Python 3.12.4` |
| `.venv/Scripts/python -m ruff check .` | `All checks passed!` |
| `.venv/Scripts/python -m pytest` | `785 passed in 12.59s` |
| `.venv/Scripts/python -m mypy` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean**: zero ruff errors;
785 / 785 tests passing; zero mypy strict issues across 82 source files.
No regressions relative to the post-Phase-4f-merge baseline.

## Commit

| Role | SHA | Message |
|---|---|---|
| Phase 4g report | `f6265cecfb7120c6459a70862fee69ac26bf5d30` | phase-4g: V2 strategy-spec memo (Participation-Confirmed Trend Continuation, docs-only) |
| Phase 4g closeout | `<recorded in chat closeout block after this file is committed>` | docs(phase-4g): closeout report (Markdown artefact) |

## Final git status

After the closeout commit and push:

```text
On branch phase-4g/v2-participation-confirmed-trend-continuation-spec
Your branch is up to date with 'origin/phase-4g/v2-participation-confirmed-trend-continuation-spec'.

nothing to commit, working tree clean
```

## Final git log --oneline -5

(Captured after the closeout commit; recorded verbatim in the chat
closeout block.)

## Final rev-parse

(Captured after the closeout commit; recorded verbatim in the chat
closeout block: `git rev-parse HEAD` and
`git rev-parse origin/phase-4g/v2-participation-confirmed-trend-continuation-spec`.)

## Branch / main status

- Phase 4g branch:
  `phase-4g/v2-participation-confirmed-trend-continuation-spec` exists
  locally and on `origin`.
- Phase 4g branch is **NOT merged to main**.
- `main` and `origin/main` remain at
  `0d0d43ffe5c54436427e6f435bdd3e73be833c31` (Phase 4f housekeeping).
- A separate operator authorization is required before any merge.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4h / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched, or
  commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 data acquisition.**
- **No data acquired.** No `data/` artefact modified. No public Binance
  endpoint consulted in code.
- **No implementation code written.** Phase 4g is text-only.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env`
  modification.
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.**
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.**
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
  Existing `prometheus.strategy` modules untouched.
- **No strategy rescue proposal.** V2 is a new ex-ante hypothesis.
- **No 5m strategy / hybrid / retained-evidence successor / new
  variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **`scripts/phase3q_5m_acquisition.py` not run.**
- **`scripts/phase3s_5m_diagnostics.py` not run.**
- **No data acquisition / download / patch / regeneration /
  modification.**
- **No data manifest modification.**
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A
  all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 4f text modification.** Phase 4g operationalizes Phase 4f;
  it does not edit the Phase 4f memo.
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md`
  substantive change.**
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md`
  substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
  substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md`
  substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive
  change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4g branch.**
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4g
  deliverables exist as branch-only artefacts pending operator review.
- **Phase 4g output:** docs-only V2 strategy-spec memo + this closeout
  artefact on the Phase 4g branch.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4g).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a executed and merged.
  Phase 4b/4c cleanups merged. Phase 4d review merged. Phase 4e
  reconciliation-model design memo merged. Phase 4f V2 hypothesis
  predeclaration merged. Phase 4g V2 strategy-spec memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved through Phase 4g).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared by Phase 4f as
  *Participation-Confirmed Trend Continuation*; operationalized by
  Phase 4g (this branch) with bounded feature list, bounded timeframe
  matrix (signal 30m, bias 4h, session 1h), 512-variant predeclared
  threshold grid, M1 / M2 / M3 mechanism-check decomposition, and
  four governance-label declarations. **NOT implemented; NOT
  backtested; NOT validated.**
- **OPEN ambiguity-log items after Phase 4g:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:**
  `phase-4g/v2-participation-confirmed-trend-continuation-spec` exists
  locally and on `origin`. NOT merged to main.

## Next authorization status

**No next phase has been authorized.** Phase 4g's recommendation is
**Option B (Phase 4h V2 Data Requirements and Feasibility Memo,
docs-only) as primary**, with **Option A (remain paused) as
conditional secondary**. Options C / D / E are not recommended; Option
F is forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has been
issued.

The 5m research thread remains operationally complete and closed (per
Phase 3t). The implementation-readiness boundary remains reviewed (per
Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers
remain RESOLVED at the governance level (per Phase 3v + Phase 3w).
The Phase 4a safe-slice scope is implemented (per Phase 4a). The
Phase 4b script-scope quality-gate restoration is complete (per Phase
4b). The Phase 4c state-package quality-gate residual cleanup is
complete (per Phase 4c). The Phase 4d post-4a/4b/4c review is complete
(per Phase 4d). The Phase 4e reconciliation-model design memo is
complete (per Phase 4e). The Phase 4f V2 hypothesis predeclaration is
complete (per Phase 4f). The Phase 4g V2 strategy spec is complete on
this branch (this phase). **Recommended state remains paused.**
