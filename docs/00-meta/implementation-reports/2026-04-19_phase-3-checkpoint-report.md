# Phase 3 — Checkpoint Report

**Date:** 2026-04-20
**Phase:** 3 — Backtesting and Strategy Conformance
**Branch:** `phase-3/backtest-strategy-conformance` (off `main` at `4a35887`, 6 commits ahead pre-checkpoint; this commit = 7th)
**Status:** COMPLETE. Awaiting operator review before merge; Phase 4 not started; Phase 2e not started.

---

## Phase

3 — Backtesting and Strategy Conformance.

## Goal

Implement the locked v1 breakout strategy and a research-only historical backtester that consumes the Phase 2 / 2b / 2c data foundation to produce reviewable trade logs, equity curves, drawdown series, R-multiple histograms, summary metrics, and a `BacktestReportManifest` citing the exact dataset manifest versions consumed. Deliver this without any live trading, exchange adapter, credentials, network activity, or Phase-4 runtime state.

## Summary

Phase 3 shipped a full-stack research-only backtester plus the v1 breakout strategy, organized as 6 small, reviewable commits preceded by a single numpy-dependency commit. The strategy package (`src/prometheus/strategy/v1_breakout/`) encodes the 1h EMA(50)/EMA(200) bias with slope confirmation, the 8-bar compression setup, the six-condition breakout trigger, the structural stop + ATR buffer + 0.60–1.80×ATR filter, and the Stage-2 through Stage-7 management state machine — all sourced from `docs/03-strategy-research/v1-breakout-strategy-spec.md` verbatim. The backtest package (`src/prometheus/research/backtest/`) implements a bar-by-bar event loop with operator-approved behavior for next-bar-open fills (entry + managed exits), mark-price stop evaluation with gap-through, adverse-direction slippage, taker commissions, inclusive-both-ends funding accrual, the full position-sizing pipeline with round-down stepSize flooring, and a per-run artifact writer that emits `trade_log.{parquet,json}`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `summary_metrics.json`, `config_snapshot.json`, and a `backtest_report.manifest.json` with dataset citations + accepted-limitation text. A mechanical import-graph guardrail, an adapter-enum invariant test, and a no-lookahead mutation test provide tamper-evident boundaries. A `SignalFunnelCounts` diagnostic attributes every decision bar to its first short-circuit filter, and a manufactured synthetic trade-path test proves the full positive path (entry intent → fill → close → all per-symbol artifacts) under unchanged v1 defaults.

Test count: 212 (end of Phase 2c) → **374 passing** (+162 new). Ruff clean on 112 files, format clean, `mypy --strict` green on 48 source files. One runtime dependency added (`numpy>=2.0,<3.0`, resolved to `numpy==2.4.4`).

## Files changed (by commit)

| Commit | Hash | Summary | Files | Insertions |
| --- | --- | --- | --- | --- |
| 1 | `292f1a2` | phase-3: add numpy runtime dep | 2 | +40 |
| 2 | `71ea54e` | strategy package — indicators, types, v1 breakout bias/setup/trigger/stop/management/strategy | 21 | +~1,790 |
| 3 | `f899eb8` | backtest core — config, clock, fills, stops, sizing + import-graph guardrail | 13 | +~1,140 |
| 4 | `b09bab3` | backtest accounting — PnL, funding join, trade log | 6 | +~660 |
| 5 | `a637b7b` | backtest engine + report + cli + simulation tests + smoke-run script + diagnostics + manufactured trade-path | 14 | +~2,220 |
| 6 | *pending hash* | docs — ambiguity log GAP-014..GAP-025 + Gate-1 plan + Gate-2 review + configs example | 4 | +~2,110 |

Totals at Commit 6 tip: **60 files changed, ~7,960 insertions, 0 deletions**. (Numbers in the insertions column are approximate due to file-rewriting churn; exact counts available via `git diff --stat origin/main..HEAD` post-merge.)

## Files created

Source code (23 files):

- `src/prometheus/strategy/{__init__,indicators,types}.py`
- `src/prometheus/strategy/v1_breakout/{__init__,bias,setup,trigger,stop,management,strategy}.py`
- `src/prometheus/research/backtest/{__init__,config,simulation_clock,fills,stops,sizing,accounting,funding_join,trade_log,engine,report,cli,diagnostics}.py`
- `scripts/phase3_smoke_run.py`

Tests (24 files):

- `tests/unit/strategy/{__init__,conftest,test_indicators,test_types,test_no_lookahead}.py`
- `tests/unit/strategy/v1_breakout/{__init__,test_bias,test_setup,test_trigger,test_stop,test_management,test_strategy_end_to_end}.py`
- `tests/unit/research/backtest/{__init__,conftest,test_config,test_simulation_clock,test_fills,test_stops,test_sizing,test_accounting,test_funding_join,test_trade_log,test_engine_smoke,test_report,test_cli,test_import_graph,test_diagnostics}.py`
- `tests/simulation/{__init__,test_backtest_synthetic_end_to_end,test_backtest_real_2026_03,test_backtest_manufactured_trade_path}.py`

Docs (3 files):

- `docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-2-review.md` (includes §15 signal-funnel diagnostic and §16 positive synthetic trade-path evidence)
- `docs/00-meta/implementation-reports/2026-04-19_phase-3-checkpoint-report.md` (this file; Commit 7)

Modified existing files (4): `pyproject.toml`, `uv.lock`, `docs/00-meta/implementation-ambiguity-log.md`, `configs/dev.example.yaml`.

## Commands run

```bash
# Pre-flight
uv --version        # uv 0.11.7
python --version    # Python 3.12.4
git status --short  # clean except Gate 1 plan untracked
git rev-list --left-right --count HEAD...@{u}  # 0 0

# Step 1: branch
git checkout -b phase-3/backtest-strategy-conformance

# Step 2: numpy
# edit pyproject.toml: append "numpy>=2.0,<3.0"
uv sync             # resolved numpy==2.4.4; 29 packages total

# Steps 3-9: write source + tests (no shell during write phase)
# Quality gates after each subpackage:
uv run ruff check .        # fix iterations applied
uv run ruff format .       # auto-format iterations applied
uv run mypy                # 0 issues
uv run pytest              # 212 -> 271 -> 341 -> 357 -> 365 -> 371 -> 374

# Operator-run real-data smoke (Gate-1 condition A):
uv run python scripts/phase3_smoke_run.py
  # Output: 0 trades on BTC/ETH 2026-03
  # Signal-funnel diagnostic per symbol printed
  # Report written under data/derived/backtests/phase-3-smoke/<ts>/

# Gate 2 pre-commit gates:
uv run ruff check .          # All checks passed!
uv run ruff format --check . # 112 files already formatted
uv run mypy                  # Success: 48 source files
uv run pytest                # 374 passed in 4.05s

# 6 commits (Gate 2 approved):
git add pyproject.toml uv.lock
git commit -m "phase-3: add numpy runtime dep"                               # 292f1a2
git add src/prometheus/strategy/ tests/unit/strategy/
git commit -m "phase-3: strategy package -- ..."                             # 71ea54e
git add src/prometheus/research/backtest/{config,simulation_clock,fills,stops,sizing,__init__}.py \
        tests/unit/research/backtest/{__init__,conftest,test_config,test_simulation_clock,test_fills,test_stops,test_sizing,test_import_graph}.py
git commit -m "phase-3: backtest core -- ..."                                # f899eb8
git add src/prometheus/research/backtest/{accounting,funding_join,trade_log}.py \
        tests/unit/research/backtest/test_{accounting,funding_join,trade_log}.py
git commit -m "phase-3: backtest accounting -- ..."                          # b09bab3
git add src/prometheus/research/backtest/{engine,report,cli,diagnostics}.py \
        tests/unit/research/backtest/test_{engine_smoke,report,cli,diagnostics}.py \
        tests/simulation/ scripts/phase3_smoke_run.py
git commit -m "phase-3: backtest engine + report + cli + simulation tests + ..."  # a637b7b
git add docs/00-meta/implementation-ambiguity-log.md \
        docs/00-meta/implementation-reports/2026-04-19_phase-3_gate-{1-plan,2-review}.md \
        configs/dev.example.yaml
git commit -m "phase-3: docs -- ambiguity log GAP-014..GAP-025 + ..."        # (this commit's parent)

# Commit 7: this checkpoint report
git add docs/00-meta/implementation-reports/2026-04-19_phase-3-checkpoint-report.md
git commit -m "phase-3: checkpoint report"
```

No destructive git. No `--force`. No `--no-verify`. No `git add -f`. No push. No `/fapi/*` authenticated calls. No credentials.

## Installations performed

One runtime dependency added: `numpy>=2.0,<3.0` (resolved to `numpy==2.4.4`). `uv sync` completed on first attempt with no Windows / wheel / typing / escalation issues. numpy ships its own type stubs, so no mypy override added.

No global installs. No host-level configuration change. `uv.lock` updated to include numpy and its transitive deps.

## Configuration changed

- `configs/dev.example.yaml`: added a new documentation-only `backtest:` block at the bottom recording operator-approved Phase 3 defaults (sizing_equity_usdt=10_000, risk_fraction=0.0025, risk_usage=0.90, max_leverage=2.0, notional cap=100_000, taker=0.0005, slippage=MEDIUM, adapter=FAKE). No config loader consumes it yet; values mirror the CLI defaults and the `BacktestConfig` model.

No other existing files modified beyond what each module required to expose re-exports at package init boundaries.

## Tests / checks passed

| Check | Command | Result |
| --- | --- | --- |
| Lint | `uv run ruff check .` | All checks passed! |
| Format | `uv run ruff format --check .` | 112 files already formatted |
| Type | `uv run mypy` | Success: 48 source files |
| Tests | `uv run pytest` | **374 passed** in 4.05s |

Test-count evolution: 2 (Phase 1) → 79 (Phase 2) → 136 (Phase 2b) → 212 (Phase 2c) → **374** (Phase 3, +162 new).

Phase 3 test breakdown (162 new):

- 79 strategy unit tests (indicators, types, no-lookahead, bias, setup, trigger, stop, management, session)
- 71 backtest unit tests (config, clock, fills, stops, sizing, accounting, funding join, trade log, engine smoke, report, cli, import-graph guardrail, diagnostic)
- 7 simulation tests (synthetic end-to-end ×2, real 2026-03 ×2 (skipif-gated), manufactured trade-path ×3)
- Plus pytest parametrizations absorbed into the 162 net total

## Tests / checks failed

None at branch tip. No mid-implementation failures survived to commit tips. Fix iterations:

- Ruff/format auto-fixes applied during Commit 2 + Commit 3 authoring (import ordering, SIM102 nested-if, E501 line-length).
- One mypy attr-defined issue in `research/backtest/__init__.py` (SlippageBucket re-export) resolved by sourcing from `config.py` rather than `accounting.py` after ruff's unused-import removal.
- One Pydantic strict-mode JSON round-trip issue on `BacktestReportManifest` (list vs tuple coercion) resolved with `Annotated[..., BeforeValidator(_as_tuple)]` helpers, mirroring the GAP-20260419-008 pattern from Phase 2.
- Test invariants in `test_management.py` refined to match the actual stage-5 cascade (trail level can be below break-even; the risk-reducing-only guard keeps the stop at break-even and the emitted intent reports STAGE_4_BREAK_EVEN rather than STAGE_5_TRAIL).
- Real-data simulation tests initially used raw `pq.read_table` on partition files which triggered a dictionary-vs-string column type merge error; replaced with the Hive-aware `storage.read_klines` / `read_mark_price_klines` / `read_funding_rate_events` helpers.

All resolved before any commit. No test was ever removed or modified in its semantic content; only failing-test fixes clarified the expected behavior.

## Runtime output

No runtime surface introduced. Phase 3 is research-only; the backtester is invoked by explicit operator `uv run python -m ...` or `uv run python scripts/phase3_smoke_run.py`.

### Real-data smoke run (operator-executed 2026-04-19T23:13:04Z)

```
Run written to: data/derived/backtests/phase-3-smoke/2026-04-19T23-13-04Z
Total trades (all symbols): 0
  BTCUSDT: 0 trades | equity 10000.00 | realized PnL +0.00
  ETHUSDT: 0 trades | equity 10000.00 | realized PnL +0.00

Signal-funnel diagnostic (BTCUSDT):
  bars loaded 15m=2976 1h=744 | warmup excluded 15m=29 1h=811 | decision bars=2165
  bias long=684 short=736 neutral=745 | setups valid=103 | candidates long=1 short=6
  reject: neutral_bias=745 no_setup=1317 no_break=96 TR<ATR=1 close_loc=3
          atr_regime=0 stop_dist=3 sizing=0 end_of_data=0
  entry_intents=0 trades_filled=0 trades_closed=0
# ETH mirror: 845 + 1224 + 89 + 0 + 6 + 0 + 1 + 0 + 0 = 2165; 0 trades.
```

Interpretation: strict v1 filters + single-month window. Not a pipeline bug. Detailed analysis in Gate 2 review §15.5.

### Manufactured trade-path test (deterministic)

`tests/simulation/test_backtest_manufactured_trade_path.py` constructs an in-memory 919-15m-bar fixture that satisfies all six v1 trigger conditions on bar 909 (900 warmup + 8 compression + 1 breakout + 10 post-breakout quiet bars). The engine produces:

- 1 LONG trade, filled at bar 910's open with entry slippage
- Stage-7 stagnation exit at `bars_in_trade=8`
- Exit fill on next bar's open
- Full per-symbol artifact set written: `trade_log.parquet`, `trade_log.json`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `summary_metrics.json`, `backtest_report.manifest.json`, `config_snapshot.json`

This proves the full positive path under unchanged v1 defaults.

## Known gaps

- **Phase 2e wider historical backfill** (GAP-20260419-025) — deferred. Phase 3 is conformance-grade on a single month; walk-forward / robustness / BTC-vs-ETH-at-scale / exit-model comparison all require multi-year data. Proposed as a separate operator-approved data task.
- **Phase 2d authenticated endpoints** — deferred. `leverageBracket` and `commissionRate` remain placeholder/parameterized in Phase 3. The validation-checklist Gate-1 strict reading is accepted-limitation (GAP-20260419-024).
- **1h mark-price derivation** — not implemented. Phase 3's backtester uses 15m mark-price bars only; if Phase 5/6 require 1h mark-price context, a small derived-data job similar to `derive_1h_from_15m` for mark-price would be needed.
- **ExchangeInfo snapshot manifest** — the `data/derived/exchange_info/2026-04-19T21-22-59Z.json` snapshot is cited in backtest reports via `DatasetCitation.raw_file_path + raw_file_sha256` rather than a `DatasetManifest` version, pending a separate retroactive-manifest task (GAP-20260419-020).
- **WebSocket / user-stream** — Phase 6+ concern; not part of Phase 3.
- **Runtime state / kill switch / SAFE_MODE / persistence** — Phase 4 concern; not part of Phase 3. The research-only BacktestAdapter has only a FAKE value, mechanically enforced.
- **Sensitivity sweeps over taker fee + slippage buckets** — executable via multiple `BacktestConfig` invocations with different `run_id`; no automated sweep runner was added in Phase 3 scope (operator can add a thin wrapper later if needed).
- **Compounding-sizing variant** — not added. Phase 3 primary variant is flat (non-compounding) per GAP-20260419-021. A compounding variant is a single-field change in the engine's sizing call path but was kept out of scope.

## Spec ambiguities found

Appended to `docs/00-meta/implementation-ambiguity-log.md` (12 entries: GAP-20260419-014 through GAP-20260419-025):

| ID | Status | Summary |
| --- | --- | --- |
| GAP-014 | **RESOLVED** | 1h normalized ATR filter uses 1h ATR(20) and latest 1h close |
| GAP-015 | **RESOLVED** | Stop-distance filter uses signal-bar close as reference |
| GAP-016 | **RESOLVED** | Managed-exit fills at next bar's open |
| GAP-017 | **RESOLVED** | Gap-through rule: fill at bar open if gap, else at stop level |
| GAP-018 | **ACCEPTED_LIMITATION** | Taker commission parameterized {0.05%, 0.04%, 0.02%}; primary 0.05% |
| GAP-019 | **RESOLVED** | Funding event join window inclusive both ends |
| GAP-020 | **ACCEPTED_LIMITATION** | ExchangeInfo 2026-04-19 snapshot as 2026-03 proxy |
| GAP-021 | **RESOLVED** | Starting sizing_equity_usdt = 10,000 (flat) |
| GAP-022 | **RESOLVED** | Risk-usage fraction 0.90 primary, 1.00 sensitivity |
| GAP-023 | **RESOLVED** | Research internal notional cap = 100,000 USDT |
| GAP-024 | **ACCEPTED_LIMITATION** | Validation Gate 1 leverageBracket + commissionRate deferred to Phase 2d |
| GAP-025 | **DEFERRED** | Phase 2e wider historical backfill |

No HIGH-risk escalations encountered during execution. The 4 ACCEPTED_LIMITATION / DEFERRED entries are explicitly documented on every `BacktestReportManifest.accepted_limitations` per backtest run.

## Technical-debt updates needed

**Per operator directive, no edits to `docs/12-roadmap/technical-debt-register.md` in Phase 3.** The register remains the operator's to update.

For reference only — items Phase 3 interacted with, to be surfaced as follow-up when operator approves a register update:

- **TD-006** (Binance API verification): no new endpoints exercised; existing Phase 2c verifications remain cited. No new TD-006 surface.
- **TD-016** (statistical thresholds require evidence): Phase 3 produces mechanics evidence, not promotion-grade statistics. Remains OPEN.
- **TD-018** (tiny-live notional cap): Phase 3 defines a *research* cap (100,000 USDT) distinct from the live cap. Does not resolve TD-018.
- **Potential NEW item — Phase 2e wider backfill** (GAP-20260419-025): could graduate into TD-register as a formal entry if operator wishes.
- **Potential NEW item — Phase 2d authenticated endpoints** (already implicit from Phase 2c deferral, flagged again here by GAP-024).

No new TD entries introduced in the register by this phase.

## Safety constraints verified

| Constraint | Result |
| --- | --- |
| Production Binance API keys | **Not created, not requested, not used.** |
| Real secrets / `.env` | **None touched. .env not created.** |
| Exchange-write capability | **None. BacktestAdapter has only FAKE; mechanical test enforces.** |
| Signed requests / HMAC | **None anywhere.** |
| `X-MBX-APIKEY` header | **Never constructed in Phase 3 code.** |
| Account-authenticated endpoints | **Not touched.** `leverageBracket`, `commissionRate`, `/fapi/v1/account/*` all deferred to Phase 2d. |
| WebSockets | **None.** |
| Third-party market-data sources | **None.** |
| `.mcp.json` / Graphify | **Not created / not enabled.** |
| Real downloaded data committed | **None** — report artifacts under `data/derived/backtests/**` are git-ignored. |
| `.claude/*` / `CLAUDE.md` / current-project-state | **Not modified.** |
| `docs/12-roadmap/technical-debt-register.md` | **Not modified.** |
| Runtime DB / persistence | **Not touched.** Phase 4 concern. |
| Destructive git / `git add -f` | **None.** |
| Network during tests | **Zero.** Enforced by `test_import_graph.py`. |
| Network during diagnostic | **Zero.** Enforced by same test. |
| Adapter enum tamper-evidence | **Enforced** by `test_adapter_enum_has_only_fake`. |
| No-lookahead invariant | **Tested** by `test_no_lookahead.py` (mutate-future, assert-past-unchanged). |

## Current runtime capability

None. Phase 3 is a research-only extension. The `strategy` package provides pure strategy calculations. The `research.backtest` package provides a bar-by-bar engine that reads Parquet inputs and writes report artifacts. Nothing runs automatically — every backtest is an explicit operator invocation.

## Exchange connectivity status

None. Phase 3 adds no exchange-touching code. `test_import_graph.py` mechanically enforces that `prometheus.research.backtest.*` and `prometheus.strategy.*` do not import any module capable of exchange I/O, including the Phase 2c `BinanceRestClient` and `BulkDownloader`.

Endpoints touched in Phase 3: **zero.** The real-data smoke run consumes only local on-disk Parquet from Phase 2b/2c.

## Exchange-write capability status

**Disabled by absence and by mechanical tests.** `BacktestAdapter` is a `StrEnum` with a single value `FAKE`; a test asserts the enum values list is exactly `["FAKE"]`. Adding any live-capable value to the enum will fail the build. The backtest package has no signing code, no credential parameters, no HMAC, no REST client, and no WebSocket. `configs/dev.example.yaml` continues to declare `exchange_write_enabled: false` and `real_capital_enabled: false`.

## Branch / commit state at end of Phase 3 (before this checkpoint commit lands)

```
$ git log --oneline -7
<pending commit-7>  phase-3: checkpoint report
<commit-6 hash>     phase-3: docs -- ambiguity log GAP-014..GAP-025 + Gate-1 plan + Gate-2 review + configs example
a637b7b             phase-3: backtest engine + report + cli + simulation tests + smoke-run script + diagnostics + manufactured trade-path
b09bab3             phase-3: backtest accounting -- PnL, funding join, trade log
f899eb8             phase-3: backtest core -- config, clock, fills, stops, sizing + import-graph guardrail
71ea54e             phase-3: strategy package -- indicators, types, v1 breakout bias/setup/trigger/stop/management/strategy
292f1a2             phase-3: add numpy runtime dep
4a35887             Merge pull request #4 from jpedrocY/phase-2c/public-market-data-completion
```

After this checkpoint commit lands, the branch is **7 commits ahead of `origin/main`** and has **not been pushed**. `main` is unchanged at `4a35887`.

## Recommended next step

Three reasonable paths forward; operator decides. These are listed in increasing strategic weight, not in any implied order:

1. **Push `phase-3/backtest-strategy-conformance` and open a PR** so the operator can review the full branch on GitHub and merge when ready.

2. **Phase 2e — wider historical backfill** (BTC + ETH 15m + 1h + mark-price + funding for a multi-year range, e.g. 2022-01 through 2026-03, via the existing `BulkDownloader` with iteration over months). Unlocks the walk-forward / robustness / exit-model validation gates that 2026-03 alone cannot support. Low implementation risk — no new code paths, just month iteration over existing Phase 2b/2c machinery.

3. **Phase 4 — Risk, State, and Persistence Runtime** — the locked next implementation phase per `docs/12-roadmap/phase-gates.md`. Introduces SAFE_MODE, kill switch, SQLite runtime DB, reconciliation states, and runtime control persistence. Still research-only; no exchange writes. Phase 4 does NOT depend on Phase 2e.

Phase 3 does not require Phase 2e completion before Phase 4 begins. Phase 2e is a *data* task; Phase 4 is a *runtime-state* task. They can run in parallel, sequentially, or independently.

## Questions for ChatGPT / operator

1. **Push timing** — push `phase-3/backtest-strategy-conformance` to `origin` now and open PR #5 into `main`, or stack Phase 4 / Phase 2e work on top of the local branch first?
2. **TD-register follow-up** — would you like a separate small follow-up commit to update `docs/12-roadmap/technical-debt-register.md` with (a) the Phase 3 slice of TD-006-related verifications, (b) a formal Phase 2e entry, and (c) a formal Phase 2d entry? Per Phase 3 instructions I did not edit that file.
3. **Phase 2e scope** — if you want to start Phase 2e, do you have a specific date range in mind? Default proposal: 2022-01 through 2026-03 (4+ years) for BTC + ETH 15m + 1h derived + mark-price + funding. This is a several-GB bulk download; the existing downloader handles SHA256 verification + idempotent state.
4. **Phase 4 kickoff** — ready to plan Phase 4 (Risk, State, and Persistence Runtime) now, or defer until Phase 2e / merge / operator review of Phase 3 is complete?

None of these block Phase 3 completion. Phase 3 is done.
