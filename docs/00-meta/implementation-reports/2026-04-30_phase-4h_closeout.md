# Phase 4h Closeout

## Summary

Phase 4h (V2 Data Requirements and Feasibility Memo) is **complete on
the Phase 4h branch and not merged to main**. Phase 4h translated the
Phase 4g locked V2 strategy spec into an exact data-requirements and
feasibility plan covering required dataset families, public-source
availability, dataset-versioning convention, directory layout,
manifest schema, integrity-check rules, `research_eligible` rules,
invalid-window handling, alignment / timestamp policy, and a future
Phase 4i acquisition execution plan preview.

Phase 4h is **docs-only**. No source code, tests, scripts, data,
manifests, specs, thresholds, parameters, project locks, or prior
verdicts were modified. No data was acquired or downloaded. No
backtests were run.

V2 remains **pre-research only**: not implemented, not backtested,
not validated, not live-ready, **not a rescue** of R3 / R2 / F1 /
D1-A.

Phase 4h recommendation: **Phase 4i — V2 Public Data Acquisition and
Integrity Validation (docs-and-data, public bulk archives only, no
credentials)** primary; **remain paused** conditional secondary.
**No** immediate backtest; **no** implementation; **no** paper /
shadow / live / exchange-write.

## Files changed

The Phase 4h branch introduces two new docs-only files relative to
`main`:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4h_v2-data-requirements-and-feasibility.md`
  (Phase 4h V2 data-requirements / feasibility memo; 38 sections;
  1676 lines)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4h_closeout.md`
  (this file)

`docs/00-meta/current-project-state.md` is **NOT modified** on the
Phase 4h branch (per the Phase 4h brief). It would be updated only
during the merge housekeeping commit, after a separate operator
authorization.

No source code, tests, scripts, data, manifests, specs, thresholds,
parameters, project locks, or prior verdicts were modified by Phase
4h.

## Data-requirements conclusion

Phase 4h translates Phase 4g's V2 spec into an exact, predeclared
data plan that any future V2 acquisition / backtest phase MUST
operate inside. This is the same anti-data-snooping discipline the
project applied to the Phase 3o predeclared 5m diagnostic question
set and the Phase 3p predeclared per-question outcome-interpretation
rules: commit the rules before acquiring or operating on data.

Phase 4h preserves verbatim:

- Phase 4g V2 strategy-spec selections (signal 30m, bias 4h, session/
  volume bucket 1h, 8 entry features + 3 exit/regime features,
  512-variant threshold grid, M1/M2/M3 mechanism-check decomposition,
  four governance label declarations);
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance;
- Phase 3r §8 mark-price gap governance;
- Phase 3p §4.7 strict integrity-gate semantics;
- Phase 3q v001-of-5m manifests;
- v002 dataset and manifests;
- §1.7.3 / §11.6 project-level locks;
- All retained-evidence verdicts (R3 baseline-of-record; H0 framework
  anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence
  only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS /
  FRAMEWORK FAIL — other).

## Required dataset families

For V2's first backtest (`trade_price_backtest` provenance per Phase
4g §24), Phase 4h identifies the following minimum required
acquisition set:

| Family | Symbols | Granularity | Source family | Required for V2 first backtest? | Already in repo? |
|---|---|---|---|---|---|
| Trade-price klines | BTC, ETH | 30m | `data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/30m/` | **YES** | NO |
| Trade-price klines | BTC, ETH | 4h | `data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/4h/` | **YES** | NO |
| `metrics` (OI + taker imbalance + long/short ratio) | BTC, ETH | 5-minute records inside daily archive | `data.binance.vision/data/futures/um/daily/metrics/<SYMBOL>/` | **YES** (OI + taker imbalance cross-check) | NO |
| Funding-rate history | BTC, ETH | per-event 8h | (existing v002 `__v002` REST source) | **YES** (reuses v002, no new acquisition) | YES (`__v002` research-eligible) |

**Total minimum acquisition set for V2 first backtest: 6 new dataset
families** (30m klines × 2 + 4h klines × 2 + `metrics` × 2).

Deferred / optional families:

| Family | Symbols | Granularity | Status |
|---|---|---|---|
| Mark-price klines | BTC, ETH | 30m, 4h | DEFERRED — only required for future `mark_price_backtest_candidate` validation pass; not first V2 backtest. Phase 3r §8 governance applies verbatim. |
| `aggTrades` (tick-level) | BTC, ETH | tick | OPTIONAL / DEFERRED — fallback only if klines `taker_buy_volume` column is shown to be insufficient (Phase 4h does NOT expect this). |

## Feature-to-dataset mapping

**Entry features:**

| # | Feature | Required dataset(s) | Phase 4i required? |
|---|---|---|---|
| 1 | HTF trend bias state (4h EMA(20)/(50) discrete comparison) | BTC + ETH 4h klines | YES (4h klines acquisition) |
| 2 | Donchian breakout state (signal-timeframe Donchian) | BTC + ETH 30m klines | YES (30m klines acquisition) |
| 3 | Donchian width percentile (compression precondition) | (covered by #2) | covered by #2 |
| 4 | Range-expansion ratio (breakout-bar TR vs. trailing mean) | (covered by #2) | covered by #2 |
| 5 | Relative volume + volume z-score | (covered by #2; uses `volume` column) | covered by #2 |
| 6 | Volume percentile by UTC hour | (covered by #2 + UTC hour derivation) | covered by #2 |
| 7 | Taker buy/sell imbalance | (covered by #2; uses `taker_buy_volume` column). `metrics` `sum_taker_long_short_vol_ratio` cross-check | covered by #2 |
| 8 | OI delta direction + funding-rate percentile band | BTC + ETH `metrics` archive (OI sub-component); v002 funding manifests (funding sub-component) | YES (`metrics` acquisition; funding reuses v002) |

**Exit / regime features:**

| # | Feature | Required dataset(s) | Phase 4i required? |
|---|---|---|---|
| 1 | Time-since-entry counter | none (clock + entry timestamp only) | NO |
| 2 | ATR percentile regime (recorded; not acted on as exit) | (covered by entry feature #2) | covered by entry #2 |
| 3 | HTF bias state continuity (recorded; not acted on as exit) | (covered by entry feature #1) | covered by entry #1 |

## Feasibility verdict

**POSITIVE under defined boundary.**

All Phase 4g V2 features can be derived from public unauthenticated
Binance bulk archives (`klines`, `markPriceKlines`, `fundingRate` REST
event archive, `metrics` daily archive, optionally `aggTrades` monthly
archive) using the same Phase 3q acquisition pattern.

**No private / authenticated / spot / order-book / user-stream data is
required.** No credentials. No `.env`. No MCP. No `.mcp.json`. No
production keys. No exchange-write capability.

Two dataset family categories that do not yet exist in the repository
— `metrics` (5-minute granularity, contains open interest + taker
buy/sell ratio + long/short ratio in one daily file) and (optionally)
`aggTrades` (tick-level taker classifier) — would need to be acquired
in a future Phase 4i. The `metrics` family is the only NEW family
required (not just NEW interval). 30m and 4h klines are NEW intervals
of an EXISTING family (`klines`); the same applies to potential 30m /
4h `markPriceKlines` (DEFERRED).

**No feasibility blocker identified.** Phase 4h does NOT recommend
revising the Phase 4g V2 strategy spec.

## research_eligible rules

Phase 4h §18 predeclares strict `research_eligible` rules consistent
with Phase 3p §4.7 and Phase 3r §8:

1. Core trade-price kline data (30m / 4h): any unhandled gap FAILS
   `research_eligible`. No forward-fill, no silent patching, no
   relaxation. Strict gate.
2. Required taker-flow data (kline `taker_buy_volume` column): any
   null / missing for a 30m signal bar excludes the bar from V2
   candidate setups (treated as data-stale per `live-data-spec.md`
   freshness gate).
3. Required OI / `metrics` data: any gap in 5-minute coverage at
   the 30m signal bar boundary excludes the bar; the dataset itself
   FAILS `research_eligible` if any day has gaps.
4. Required funding-rate data: any V2 30m signal bar that has no
   completed funding event with `funding_time ≤ t AND t -
   funding_time ≤ 8h` excludes the bar.
5. Mark-price gaps: Phase 3r §8 governance applies verbatim. Mark
   price datasets remain `research_eligible: false` if any gap is
   detected.
6. Forward-fill / interpolation / imputation: FORBIDDEN across any
   missing core observation. Phase 4h does NOT predeclare any
   deviation.
7. Unknown source coverage: dataset FAILS `research_eligible` until
   coverage is proven. Fail-closed.
8. Private / authenticated-source dependency: FAILS at design time.
   Phase 4h FORBIDS adding any feature that requires private data.

## Candidate next-slice decision

Phase 4h §37 presents the operator decision menu:

- **Phase 4i — V2 Public Data Acquisition and Integrity Validation
  (docs-and-data, public bulk archives only, no credentials)** —
  **PRIMARY RECOMMENDATION.** Implement the §33 acquisition execution
  plan: acquire 30m klines × 2 symbols, 4h klines × 2 symbols,
  `metrics` × 2 symbols from public bulk archives; SHA256-verify;
  normalize to Parquet; generate manifests per §16 schema; run
  integrity checks per §17; produce a Phase 4i acquisition + integrity
  report analogous to Phase 3q. Mark-price 30m / 4h and aggTrades
  acquisition deferred unless separately scoped.
- **Remain paused** — **CONDITIONAL SECONDARY.** Procedurally
  acceptable; defers Phase 4i.
- **Revise V2 spec** — **NOT RECOMMENDED.** No feasibility blocker
  identified.
- **Immediate V2 backtest** — **REJECTED.** Cannot be done before
  data is acquired AND would be data-snooping.
- **V2 implementation** — **REJECTED.** Requires successful backtest
  evidence (which does not exist) AND a separate authorization (which
  does not exist).
- **Paper / shadow / live-readiness / exchange-write** — **FORBIDDEN.**
  Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.

## Commands run

The following commands were run during Phase 4h per the Phase 4h
brief:

| # | Command | Purpose |
|---|---|---|
| 1 | `git status` | Verify clean tree pre-branch |
| 2 | `git checkout -b phase-4h/v2-data-requirements-and-feasibility` | Create Phase 4h branch |
| 3 | `git rev-parse main`, `git rev-parse origin/main` | Verify main == origin/main at 9291ea7 |
| 4 | `WebSearch ...` (×2) | Verify public Binance bulk archive `metrics` and `aggTrades` endpoint availability |
| 5 | `.venv/Scripts/python --version` | Confirm Python toolchain |
| 6 | `.venv/Scripts/python -m ruff check .` | Verify whole-repo Ruff clean |
| 7 | `.venv/Scripts/python -m pytest` | Verify whole-repo pytest clean |
| 8 | `.venv/Scripts/python -m mypy` | Verify mypy strict clean |
| 9 | `git add ... && git commit -m ...` | Commit Phase 4h memo |
| 10 | `git push -u origin phase-4h/...` | Push Phase 4h branch |

The following commands were **NOT** run (per Phase 4h brief
prohibitions):

- No `scripts/phase3q_5m_acquisition.py` execution.
- No `scripts/phase3s_5m_diagnostics.py` execution.
- No backtest execution.
- No diagnostics execution.
- No data acquisition.
- No data download.
- No public Binance endpoint consulted *in code*. Web research used
  the `WebSearch` tool only against public documentation pages.
- No Binance API call from project code.
- No new script added.
- No new API client added.

## Verification results

| Check | Result |
|---|---|
| `.venv/Scripts/python --version` | `Python 3.12.4` |
| `.venv/Scripts/python -m ruff check .` | `All checks passed!` |
| `.venv/Scripts/python -m pytest` | `785 passed in 12.87s` |
| `.venv/Scripts/python -m mypy` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean**: zero ruff errors;
785 / 785 tests passing; zero mypy strict issues across 82 source
files. No regressions relative to the post-Phase-4g-merge baseline.

## Commit

| Role | SHA | Message |
|---|---|---|
| Phase 4h memo | `6ad42080bf91e82eef3113ab9166c15f86ccdd3f` | phase-4h: V2 data requirements and feasibility memo (docs-only) |
| Phase 4h closeout | `<recorded in chat closeout block after this file is committed>` | docs(phase-4h): closeout report (Markdown artefact) |

## Final git status

After the closeout commit and push:

```text
On branch phase-4h/v2-data-requirements-and-feasibility
Your branch is up to date with 'origin/phase-4h/v2-data-requirements-and-feasibility'.

nothing to commit, working tree clean
```

## Final git log --oneline -5

(Captured after the closeout commit; recorded verbatim in the chat
closeout block.)

## Final rev-parse

(Captured after the closeout commit; recorded verbatim in the chat
closeout block: `git rev-parse HEAD` and
`git rev-parse origin/phase-4h/v2-data-requirements-and-feasibility`.)

## Branch / main status

- Phase 4h branch: `phase-4h/v2-data-requirements-and-feasibility`
  exists locally and on `origin`.
- Phase 4h branch is **NOT merged to main**.
- `main` and `origin/main` remain at
  `9291ea732e25d78f1ced2013064539cc3d9ac808` (Phase 4g housekeeping).
- A separate operator authorization is required before any merge.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4i / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched, or
  commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 data acquisition.**
- **No data acquired.** No `data/` artefact modified. No public Binance
  endpoint consulted *in code*.
- **No data downloaded.** No archive fetched.
- **No implementation code written.** Phase 4h is text-only.
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
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4f text modification.**
- **No Phase 4g text modification.** Phase 4h does NOT modify Phase
  4g's selections; Phase 4h operationalizes Phase 4g's data needs.
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md`
  substantive change.**
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md`
  substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
  substantive change.**
- **No `docs/04-data/data-requirements.md` substantive change.**
- **No `docs/04-data/live-data-spec.md` substantive change.**
- **No `docs/04-data/timestamp-policy.md` substantive change.**
- **No `docs/04-data/dataset-versioning.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md`
  substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive
  change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive
  change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4h branch.**
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

- **Recommended state:** **paused** for any successor phase. Phase
  4h deliverables exist as branch-only artefacts pending operator
  review.
- **Phase 4h output:** docs-only V2 data-requirements / feasibility
  memo + this closeout artefact on the Phase 4h branch.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4h).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase
  4 (canonical) remains not authorized. Phase 4a–4g all merged.
  Phase 4h V2 data-requirements / feasibility memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved through Phase 4h).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared by Phase 4f as
  *Participation-Confirmed Trend Continuation*; operationalized by
  Phase 4g (strategy spec) and Phase 4h (data requirements). NOT
  implemented; NOT backtested; NOT validated; NOT live-ready.
- **OPEN ambiguity-log items after Phase 4h:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:**
  `phase-4h/v2-data-requirements-and-feasibility` exists locally and
  on `origin`. NOT merged to main.

## Next authorization status

**No next phase has been authorized.** Phase 4h's recommendation is
**Option B (Phase 4i V2 Public Data Acquisition and Integrity
Validation) as primary**, with **Option A (remain paused) as
conditional secondary**. Options C / D / E are not recommended;
Option F is forbidden.

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
complete (per Phase 4f). The Phase 4g V2 strategy spec is complete
(per Phase 4g). The Phase 4h V2 data-requirements / feasibility memo
is complete on this branch (this phase). **Recommended state remains
paused.**
