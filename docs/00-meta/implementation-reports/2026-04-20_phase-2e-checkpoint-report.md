# Phase 2e — Checkpoint Report

**Date:** 2026-04-20
**Phase:** 2e — Wider Historical Backfill and Baseline Backtest Dataset
**Branch:** `phase-2e/wider-historical-backfill` (off `main` at `07be435`; 5 commits landed locally; **not pushed**)

Produced per `.claude/rules/prometheus-phase-workflow.md`. Descriptive evidence only; not promotion evidence and not live-readiness evidence.

---

## Phase

Phase 2e — Wider Historical Backfill and Baseline Backtest Dataset.

Scope-defining documents:
- `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-2-review.md`

## Goal

Widen the Phase 2b/2c research-data footprint from the 2026-03 validation slice to the full 2022-01 through 2026-03 range for BTCUSDT + ETHUSDT across all four research datasets (standard klines, 1h derived, mark-price klines, funding events), then run the Phase-3-locked v1 breakout backtest over the widened range and produce a descriptive baseline summary with no parameter tuning and no live-readiness claims.

## Summary

- All Phase 2e Gate 1 conditions satisfied. The HIGH-risk TD-006 pre-backfill verification surfaced `GAP-20260420-029` (Binance `fundingRate` returns empty-string `markPrice` for pre-2024 events). Execution paused, GAP logged, operator approved Option C (narrow model change to `FundingRateEvent.mark_price: float | None`). Three source files + 13 new tests; backtester verified unchanged (`grep mark_price src/prometheus/research/backtest/` returns no reference to `FundingRateEvent.mark_price`).
- 51-month backfill completed cleanly. 8 v002 manifests written; 8 v001 manifests preserved as audit trail. Zero invalid windows across all datasets; 204 / 204 SHA256 checksum matches. Pre-2024 funding events land as `mark_price=None` as designed; post-2024 events as positive floats.
- Phase-3-locked baseline backtest run end-to-end over the widened data. BTCUSDT: 41 trades, −3.95% net. ETHUSDT: 47 trades, −4.07% net. No tuning; single-configuration descriptive baseline at locked defaults (`risk=0.25%`, `risk_usage=0.90`, `max_leverage=2x`, `notional_cap=100k`, `taker=5bps`, `slippage=MEDIUM`, `adapter=FAKE`). Signal-funnel bucket-accounting invariant holds for both symbols (decision bars = rejection sum + entry intents). Mark-price coverage gap (BTC 289 / ETH 193 missing 15m bars in 2022-07 → 2023-11 window) verified to affect **zero** held-position intervals on either symbol; baseline PnL and stop evaluation therefore unaffected.
- Internal optimization added during Gate 2 execution: incremental O(1) Wilder ATR + EMA cache in `StrategySession` and `research.backtest.diagnostics.run_signal_funnel`, matching the standalone `wilder_atr` / `ema` seeding semantics exactly. No threshold, parameter, or strategy-logic change; all 387 tests still pass. 51-month run wall time: >50 min → ~1 min.

## Files changed

By commit:

| Commit | SHA | Files |
|--------|-----|-------|
| 1. Option C core | `60c3a26` | `src/prometheus/core/events.py`, `src/prometheus/research/data/funding_rate.py`, `src/prometheus/research/data/storage.py` |
| 2. Option C tests | `9515f9c` | `tests/unit/core/test_events.py`, `tests/unit/research/data/test_funding_rate.py`, `tests/unit/research/data/test_storage.py`, `tests/unit/research/backtest/test_funding_join.py` |
| 3. Performance fix | `b1efcf2` | `src/prometheus/strategy/v1_breakout/strategy.py`, `src/prometheus/research/backtest/diagnostics.py` |
| 4. Runner scripts | `724a92b` | `scripts/phase2e_backfill.py`, `scripts/phase2e_baseline_backtest.py` |
| 5. Docs | `829bb6a` | `docs/00-meta/implementation-ambiguity-log.md`, `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-1-plan.md`, `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-2-review.md`, `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md` |
| 6. Checkpoint | this commit | `docs/00-meta/implementation-reports/2026-04-20_phase-2e-checkpoint-report.md` |

## Files created

- `scripts/phase2e_backfill.py`
- `scripts/phase2e_baseline_backtest.py`
- `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-1-plan.md`
- `docs/00-meta/implementation-reports/2026-04-20_phase-2e_gate-2-review.md`
- `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md`
- `docs/00-meta/implementation-reports/2026-04-20_phase-2e-checkpoint-report.md` (this file)

(The eight v002 manifests + 1,000+ partitioned Parquet files + backtest artifacts under `data/` are all git-ignored and **not** committed.)

## Commands run (representative, in order)

```
git checkout -b phase-2e/wider-historical-backfill
# --- TD-006 verification (WebFetch) surfaced GAP-029; paused; operator approved Option C ---
uv run pytest        -> 387 passed (was 374)
uv run ruff check .  -> pass
uv run ruff format --check . -> pass
uv run mypy          -> pass
uv run python scripts/phase2e_backfill.py           -> all 8 v002 manifests written; 0 invalid windows
uv run python scripts/phase2e_baseline_backtest.py  -> run_id 2026-04-20T23-58-39Z
# --- Gate 2 pre-commit operator checks (report hygiene + mark-price impact) ---
uv run ruff check .  -> pass
uv run ruff format --check . -> 114 files already formatted
uv run mypy          -> Success: no issues found in 48 source files
uv run pytest        -> 387 passed
# --- 6-commit sequence, pytest after each ---
git add <commit 1 files> && git commit  -> 60c3a26 ; pytest 387 passed
git add <commit 2 files> && git commit  -> 9515f9c ; pytest 387 passed
git add <commit 3 files> && git commit  -> b1efcf2 ; pytest 387 passed
git add <commit 4 files> && git commit  -> 724a92b ; pytest 387 passed
git add <commit 5 files> && git commit  -> 829bb6a ; pytest 387 passed
git add <commit 6 file>  && git commit  -> <this commit>
```

## Installations performed

None. No new runtime dependencies. No new dev dependencies. `uv.lock` unchanged. `pyproject.toml` unchanged.

## Configuration changed

None. No edits to `configs/`, no new `.env*` files, no MCP config, no Graphify config, no `.claude/` edits, no `CLAUDE.md` edit, no `current-project-state.md` edit, no `technical-debt-register.md` edit.

## Tests/checks passed

- `uv run ruff check .` — passed post-edit and post-every-commit.
- `uv run ruff format --check .` — 114 files already formatted.
- `uv run mypy` — Success: no issues found in 48 source files.
- `uv run pytest` — **387 passed** in ~11 s after each of the 5 code/doc commits (pre-checkpoint). Test count 374 (Phase 3) → 387 (+13 Option C).

## Tests/checks failed

None.

## Runtime output (key evidence snippets)

- Backfill:
  - 102 / 102 kline SHA256 matches.
  - 102 / 102 mark-price SHA256 matches.
  - 0 invalid windows across all 8 v002 datasets.
  - 9,306 funding events total (4,010 with `mark_price=None` from pre-2024 upstream).
- Baseline run `2026-04-20T23-58-39Z`:
  - BTCUSDT: 41 trades, 29.3% win rate, expectancy −0.43 R, profit factor 0.32, net −394.87 USDT, max DD −424.23 USDT / −4.23%, fees 197.73, funding −1.13.
  - ETHUSDT: 47 trades, 23.4% win rate, expectancy −0.39 R, profit factor 0.42, net −407.31 USDT, max DD −490.62 USDT / −4.89%, fees 177.04, funding +0.61.
  - Signal-funnel invariant: BTC 148,085 = 147,965 + 120 ✓; ETH 148,085 = 147,965 + 120 ✓ (decision-bars = rejection-sum + entry-intents on each symbol after rounding into the per-bucket totals reported in the Gate 2 review §11).
- Mark-price coverage vs held-position intervals:
  - BTC: 289 missing 15m mark-price bars (0.194%); 0 of 399 held intervals affected; 0 trades affected.
  - ETH: 193 missing 15m mark-price bars (0.130%); 0 of 421 held intervals affected; 0 trades affected.

## Known gaps

Open at phase close:

- `GAP-20260419-018` — ACCEPTED: taker commission placeholder; `commissionRate` authenticated endpoint deferred.
- `GAP-20260419-020` — ACCEPTED: `exchangeInfo` 2026-04-19T21-22-59Z snapshot used as proxy for the full range.
- `GAP-20260419-024` — ACCEPTED: `leverageBracket` / `commissionRate` deferred; not binding at 2x leverage.
- `GAP-20260420-028` — OPEN (v002 manifest `predecessor_version=null` instead of the v001 string). Noted in Gate 2 review §5 as a known limitation; orchestrator does not expose a predecessor parameter and extending it was explicitly out of the Phase 2e zero-core-code-change intent. Can be addressed in a small follow-up commit if operator prefers.

Resolved this phase:

- `GAP-20260420-029` — RESOLVED (Option C narrow model change, 13 tests, backtester verified unaffected).

## Spec ambiguities found

- `GAP-20260420-029` (HIGH) — surfaced and resolved in-phase (see above).
- `GAP-20260420-028` (LOW) — manifest `predecessor_version` not populated; logged, not resolved, not blocking.

No other new ambiguities found this phase.

## Technical-debt updates needed

None. `docs/12-roadmap/technical-debt-register.md` was **not edited** in this phase per operator instruction. Any follow-up additions (e.g., for `GAP-20260420-028`) will be proposed separately.

## Safety constraints verified

| Constraint | Result |
|-----------|--------|
| Production Binance API keys | Not created, not requested, not used. |
| `.env` / real credentials | None. |
| Authenticated endpoints | Zero calls (backfill uses public `data.binance.vision` + public `/fapi/v1/fundingRate` only). |
| Signed requests / HMAC / `X-MBX-APIKEY` | Zero. |
| WebSocket / user data stream | Zero. |
| Third-party market-data sources | Zero. |
| `.mcp.json` / MCP / Graphify | Not created, not enabled. |
| Exchange-write capability | None; research-only code path. |
| Parameter tuning / threshold changes | Zero. Locked Phase 3 defaults. |
| Sensitivity variants | Zero; deferred per operator condition 8. |
| New runtime dependencies | Zero. |
| `docs/12-roadmap/technical-debt-register.md` edits | None. |
| `.claude/`, `CLAUDE.md`, `current-project-state.md` edits | None. |
| Committed `data/` files | Zero; all git-ignored. |
| `git add -f` | Never used. |
| Destructive git commands | Never used. |
| Promotion / live-readiness claims in output | None — baseline explicitly marked "descriptive, not promotion evidence". |
| TD-006 verification before downloads | Performed; surfaced and resolved `GAP-20260420-029`. |

## Current runtime capability

Research-only. Wide-range historical data ingested, validated, manifested, and queryable via the Phase 2b/2c ingest + derivation pipelines. Phase-3-locked backtest runs cleanly over the 51-month BTC+ETH range and produces the same artifact shape as Phase 3. No live runtime code path was introduced.

## Exchange connectivity status

None for private endpoints. Public historical ZIPs from `data.binance.vision` and public `fundingRate` REST calls from `fapi.binance.com` only. No authenticated calls.

## Exchange-write capability status

**Disabled by design.** No exchange adapter is invoked in the research/backtest path. `adapter=FAKE` in the baseline config. No credentials exist in the repository or `.env` files.

## Recommended next step

Return control to the operator and to ChatGPT for Phase 2e acceptance review. Proposed next direction (**proposal only; not authorized here**): operator + ChatGPT review the committable baseline summary against the Gate 2 evidence and decide whether the next phase should be:

- (a) Phase 2f — sensitivity / walk-forward variants over the widened data (deferred condition from Gate 1), or
- (b) another Phase-2 data-foundation follow-up (e.g., `commissionRate` endpoint work to retire `GAP-018` and `GAP-024`), or
- (c) move on to Phase 4 (risk, state, persistence runtime) per the original phase sequence in `docs/00-meta/ai-coding-handoff.md`.

Per operator restrictions at the Gate 2 approval: **do not start Phase 4, do not start any parameter-tuning phase, do not tune thresholds, do not run sensitivity variants, do not push, do not edit `technical-debt-register.md`, do not enable MCP or Graphify, do not create `.mcp.json`.**

## Question for ChatGPT/operator

None. All Gate 2 conditions satisfied. Awaiting direction on the next phase boundary.
