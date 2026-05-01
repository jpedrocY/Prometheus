# Phase 4h Merge Closeout

## Summary

Phase 4h (V2 Data Requirements and Feasibility Memo, docs-only) has
been merged into `main` via a `--no-ff` merge commit. Phase 4h
translated the locked Phase 4g V2 strategy spec into an exact
data-requirements and feasibility plan: required dataset families,
public-source availability, dataset-versioning convention, directory
layout, manifest schema, integrity-check rules, `research_eligible`
rules, invalid-window handling, alignment / timestamp policy, and a
future Phase 4i acquisition execution plan preview.

Phase 4h is docs-only. No source code, tests, scripts, data,
manifests, specs, thresholds, parameters, project locks, or prior
verdicts were modified. No data was acquired or downloaded. No
backtests were run. No paper / shadow, live-readiness, deployment,
production-key, exchange-write, MCP, Graphify, `.mcp.json`, or
credentials work occurred.

V2 remains **pre-research only**: not implemented, not backtested,
not validated, not live-ready, **not a rescue** of R3 / R2 / F1 /
D1-A.

Phase 4 canonical remains unauthorized. Phase 4i and any successor
phase remain unauthorized. Recommended state remains **paused**.

## Files changed

The merge introduced two new docs-only files into `main`:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4h_v2-data-requirements-and-feasibility.md`
  (Phase 4h V2 data-requirements / feasibility memo; 38 sections;
  1676 lines)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4h_closeout.md`
  (Phase 4h closeout report; 438 lines)

The housekeeping commit additionally updated:

- `docs/00-meta/current-project-state.md`
  (narrow update: new Phase 4h paragraph; refreshed
  "Current phase" / "Most recent merge" code blocks)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4h_merge-closeout.md`
  (this file)

No source code, tests, scripts, data files, manifests, specs,
thresholds, parameters, project locks, or prior verdict records were
modified.

## Phase 4h commits included

| Role | SHA | Message |
| --- | --- | --- |
| Phase 4h memo | `6ad42080bf91e82eef3113ab9166c15f86ccdd3f` | phase-4h: V2 data requirements and feasibility memo (docs-only) |
| Phase 4h closeout | `a27ebdd671446b2be563d84adcce27878894c73b` | docs(phase-4h): closeout report (Markdown artefact) |

## Merge commit

| Field | Value |
| --- | --- |
| Merge SHA | `99aacbc80760405a49ea19ff848642ebb0960cba` |
| Merge style | `--no-ff` |
| Source branch | `phase-4h/v2-data-requirements-and-feasibility` |
| Target branch | `main` |
| Pre-merge `main` SHA | `9291ea732e25d78f1ced2013064539cc3d9ac808` |

## Housekeeping commit

The housekeeping commit (recorded in the chat closeout block after
this file is committed) updates `docs/00-meta/current-project-state.md`
and adds this merge-closeout file. It is docs-only and post-merge.

## Final git status

After merge + housekeeping:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## Final git log --oneline -8

(Captured after the housekeeping commit and final push; recorded
verbatim in the chat closeout block.)

## Final rev-parse

(Captured after the housekeeping commit and final push; recorded
verbatim in the chat closeout block: `git rev-parse main` and
`git rev-parse origin/main`.)

## main == origin/main confirmation

After the housekeeping commit is pushed, `git rev-parse main` and
`git rev-parse origin/main` both resolve to the same SHA. Local and
remote are in sync.

## Data-requirements conclusion

- **Phase 4h was docs-only.** No source code, tests, scripts, data,
  or manifests were modified.
- **Phase 4h translated the locked Phase 4g V2 strategy spec into
  exact data requirements and feasibility rules** consistent with the
  Phase 3p / Phase 3q / Phase 3r data-requirements / acquisition /
  governance precedents.
- **Phase 4h preserves verbatim:** Phase 4g V2 strategy-spec
  selections; Phase 3v §8 stop-trigger-domain governance; Phase 3w
  §6 / §7 / §8 break-even / EMA slope / stagnation governance;
  Phase 3r §8 mark-price gap governance; Phase 3p §4.7 strict
  integrity-gate semantics; Phase 3q v001-of-5m manifests; v002
  dataset and manifests; §1.7.3 / §11.6 project-level locks; all
  retained-evidence verdicts.
- **Phase 4h does NOT acquire any data** and does NOT authorize
  acquisition. Phase 4i (the recommended next phase) would be a
  separate, explicit operator authorization.

## Required dataset families

Phase 4h identifies the minimum future Phase 4i acquisition set for
V2's first backtest (`trade_price_backtest` provenance per Phase 4g
§24):

- **BTCUSDT 30m trade-price klines.** New `__v001` dataset version.
- **ETHUSDT 30m trade-price klines.** New `__v001` dataset version.
- **BTCUSDT 4h trade-price klines.** New `__v001` dataset version.
- **ETHUSDT 4h trade-price klines.** New `__v001` dataset version.
- **BTCUSDT `metrics`.** New `__v001` dataset version (5-minute
  granularity OI + taker buy/sell ratio + long/short ratio in one
  daily archive from
  `data.binance.vision/data/futures/um/daily/metrics/`).
- **ETHUSDT `metrics`.** New `__v001` dataset version.

**Total minimum acquisition set: 6 new dataset families.**

**Funding-rate history reuses existing v002 funding manifests**
(`binance_usdm_btcusdt_funding__v002` and
`binance_usdm_ethusdt_funding__v002`); no new funding acquisition
required for V2's first backtest.

**Mark-price 30m / 4h is DEFERRED to a future
`mark_price_backtest_candidate` path** per Phase 3v §8.5 (only
required for live-readiness validation step; not first V2 backtest).
Phase 3r §8 mark-price gap governance applies verbatim to any
future mark-price acquisition.

**`aggTrades` is OPTIONAL / DEFERRED fallback only** (klines
`taker_buy_volume` column is sufficient for V2's predeclared
taker-imbalance feature; Phase 4h does NOT recommend `aggTrades`
acquisition).

**No data was acquired by Phase 4h.** No `data/` artefact modified.
No public Binance endpoint consulted in code.

## Feature-to-dataset mapping

**Entry features (Phase 4g §28):**

| # | Feature | Required dataset(s) | Phase 4i required? |
|---|---|---|---|
| 1 | HTF trend bias state (4h EMA(20)/(50) discrete comparison) | BTC + ETH 4h klines | YES (4h klines acquisition) |
| 2 | Donchian breakout state (signal-timeframe Donchian) | BTC + ETH 30m klines | YES (30m klines acquisition) |
| 3 | Donchian width percentile (compression precondition) | (covered by #2) | covered by #2 |
| 4 | Range-expansion ratio (breakout-bar TR vs. trailing mean) | (covered by #2) | covered by #2 |
| 5 | Relative volume + volume z-score | (covered by #2; uses kline `volume` column) | covered by #2 |
| 6 | Volume percentile by UTC hour | (covered by #2 + UTC hour derivation) | covered by #2 |
| 7 | Taker buy/sell imbalance | (covered by #2; uses kline `taker_buy_volume` column). `metrics` `sum_taker_long_short_vol_ratio` cross-check | covered by #2 |
| 8 | OI delta direction + funding-rate percentile band | BTC + ETH `metrics` archive (OI sub-component); v002 funding manifests (funding sub-component) | YES (`metrics` acquisition; funding reuses v002) |

**Exit / regime features (Phase 4g §28):**

| # | Feature | Required dataset(s) | Phase 4i required? |
|---|---|---|---|
| 1 | Time-since-entry counter | none (clock + entry timestamp only) | NO |
| 2 | ATR percentile regime (recorded; not acted on as exit) | (covered by entry feature #2) | covered by entry #2 |
| 3 | HTF bias state continuity (recorded; not acted on as exit) | (covered by entry feature #1) | covered by entry #1 |

## Feasibility verdict

- **Feasibility verdict is POSITIVE under defined boundary.**
- **All Phase 4g V2 features can be supported by public
  unauthenticated Binance bulk / public data under the Phase 4h
  rules.** Trade-price klines, mark-price klines, funding-rate REST
  event archive, `metrics` daily archive, and (optionally)
  `aggTrades` monthly archive are all available from
  `data.binance.vision` with paired `.CHECKSUM` files (per Phase 3q
  acquisition pattern).
- **No private / authenticated / user-stream / order-book data is
  required.** No `aggTrades` reliance (klines `taker_buy_volume`
  column is sufficient for V2's predeclared taker-imbalance feature).
  No spot leg. No cross-venue.
- **No credentials are required.** No API keys. No `.env` files.
  No signed requests. No MCP. No `.mcp.json`. No production keys.
  No exchange-write capability.
- **No feasibility blocker was identified.** All 8 Phase 4g entry
  features and all 3 exit / regime features can be derived from the
  6-family minimum acquisition set + reused v002 funding manifests.
- **Phase 4h does NOT recommend revising Phase 4g.** No spec change
  is required to make V2 implementable from public data.

## research_eligible rules

Phase 4h §18 predeclares strict `research_eligible` rules consistent
with Phase 3p §4.7 and Phase 3r §8:

1. **Core trade-price kline data (30m / 4h):** any unhandled gap
   (`gaps_detected != 0`) FAILS `research_eligible`. No forward-fill,
   no silent patching, no relaxation. Strict gate.
2. **Required taker-flow data (kline `taker_buy_volume`):** any
   null / missing for a 30m signal bar excludes the bar from V2
   candidate setups (treated as data-stale per `live-data-spec.md`
   freshness gate).
3. **Required OI / `metrics` data:** any gap in 5-minute coverage at
   the 30m signal bar boundary excludes the bar; the dataset itself
   FAILS `research_eligible` if any day has gaps.
4. **Required funding-rate data:** any V2 30m signal bar that has no
   completed funding event with `funding_time ≤ t AND t -
   funding_time ≤ 8h` excludes the bar.
5. **Mark-price gaps:** Phase 3r §8 governance applies verbatim.
   Mark-price datasets remain `research_eligible: false` if any gap
   is detected.
6. **Forward-fill / interpolation / imputation:** FORBIDDEN across
   any missing core observation. Phase 4h does NOT predeclare any
   deviation.
7. **Unknown source coverage:** dataset FAILS `research_eligible`
   until coverage is proven. Fail-closed.
8. **Private / authenticated-source dependency:** FAILS at design
   time. Phase 4h FORBIDS adding any feature that requires private
   data.

## Candidate next-slice decision

- **Phase 4i — V2 Public Data Acquisition and Integrity Validation
  (docs-and-data, public bulk archives only, no credentials)** —
  **PRIMARY RECOMMENDATION.** Implement the §33 acquisition execution
  plan: acquire 30m klines × 2 symbols, 4h klines × 2 symbols,
  `metrics` × 2 symbols from public bulk archives; SHA256-verify;
  normalize to Parquet; generate manifests per §16 schema; run
  integrity checks per §17; produce a Phase 4i acquisition + integrity
  report analogous to Phase 3q. Mark-price 30m / 4h and `aggTrades`
  acquisition deferred unless separately scoped.
- **Remain paused** — **CONDITIONAL SECONDARY.** Procedurally
  acceptable; defers Phase 4i.
- **Revise V2 spec** — **NOT RECOMMENDED.** No feasibility blocker
  identified.
- **Immediate V2 backtest** — **REJECTED.** Cannot be done before
  data is acquired AND would be data-snooping per Bailey/Borwein/
  López de Prado/Zhu 2014.
- **V2 implementation** — **REJECTED.** Requires successful backtest
  evidence (which does not exist) AND a separate authorization (which
  does not exist).
- **Paper / shadow / live-readiness / exchange-write** — **FORBIDDEN.**
  Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.

## Verification evidence

The Phase 4h branch was verified clean before merge:

- `ruff check .` passed (`All checks passed!`).
- `pytest` passed (**785 passed**).
- `mypy --strict src/prometheus` passed (`Success: no issues found
  in 82 source files`).

Verification was performed against the Phase 4h branch tip
(`a27ebdd671446b2be563d84adcce27878894c73b`) before the merge.
Phase 4h introduced docs-only changes; the verification baseline is
identical to the Phase 4g merge baseline.

## Forbidden-work confirmation

The following did **not** occur in Phase 4h or in this merge closeout:

- no successor phase started (no Phase 4i; no V2 acquisition; no V2
  implementation; no V2 backtest; no successor authorization);
- no implementation code changed;
- no `src/prometheus/` modification;
- no test modification;
- no script modification;
- no data acquisition / patching / regeneration / modification;
- no data download;
- no `data/manifests/*.manifest.json` modification;
- no Phase 3q v001-of-5m manifest modification;
- no v003 dataset created;
- no Q1–Q7 rerun;
- no diagnostics rerun;
- no backtests run;
- no `scripts/phase3q_5m_acquisition.py` execution;
- no `scripts/phase3s_5m_diagnostics.py` execution;
- no V2 implementation;
- no V1 / R3 / R2 / F1 / D1-A implementation or rescue;
- no retained verdict revision;
- no project-lock revision;
- no §11.6 change;
- no §1.7.3 change;
- no Phase 3r §8 mark-price gap governance change;
- no Phase 3v `stop_trigger_domain` governance change;
- no Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance change;
- no Phase 4f text modification;
- no Phase 4g V2 strategy-spec selection modification;
- no spec / backtest-plan / validation-checklist / stop-loss-policy /
  runtime-doc / phase-gates / technical-debt-register / ai-coding-handoff
  / first-run-setup-checklist / data-requirements / live-data-spec /
  timestamp-policy / dataset-versioning substantive edit;
- no `docs/00-meta/implementation-ambiguity-log.md` modification (all
  four pre-coding governance blockers remain RESOLVED per Phase 3v /
  Phase 3w);
- no Phase 4 canonical authorization;
- no reconciliation implementation;
- no real-exchange adapter implementation;
- no exchange-write capability;
- no order placement / cancellation;
- no credential storage / request / use;
- no authenticated REST / private endpoints / public endpoints in code /
  user stream / WebSocket / listenKey lifecycle;
- no MCP / Graphify enablement;
- no `.mcp.json` modification;
- no `.env` files created;
- no deployment;
- no paper / shadow runtime;
- no live-readiness implication;
- no v002 dataset / manifest modification;
- no Phase 3p §4.7 amendment.

## Remaining boundary

- R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
  F1 / D1-A retained research evidence only.
- R2 FAILED — §11.6 cost-sensitivity blocks.
- F1 HARD REJECT.
- D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- §11.6 = 8 bps HIGH per side.
- §1.7.3 project-level locks (including mark-price stops).
- v002 verdict provenance.
- Phase 3q mark-price 5m manifests `research_eligible: false`.
- Phase 3r §8 mark-price gap governance.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance.
- Phase 4a public API and runtime behavior.
- Phase 4e reconciliation-model design memo (governance defined; not
  implemented).
- Phase 4f V2 hypothesis predeclaration.
- Phase 4g V2 strategy spec (timeframe matrix, feature set,
  threshold grid, M1/M2/M3 mechanism-checks, governance labels).
- **Phase 4h V2 data-requirements / feasibility memo (this merge):**
  required dataset families; feature-to-dataset mapping;
  feasibility verdict POSITIVE under defined boundary;
  dataset-versioning convention; directory layout; manifest schema;
  integrity-check rules; `research_eligible` rules; invalid-window
  handling; alignment / timestamp policy; future Phase 4i acquisition
  execution plan preview.

All preserved verbatim. No project locks changed.

## Next authorization status

- **Phase 4 canonical:** unauthorized.
- **Phase 4i / any successor phase:** unauthorized.
- **V2 data acquisition:** unauthorized.
- **V2 backtest:** unauthorized.
- **V2 implementation:** unauthorized.
- **Paper / shadow:** unauthorized.
- **Live-readiness:** unauthorized.
- **Deployment:** unauthorized.
- **Production keys:** unauthorized.
- **Authenticated APIs:** unauthorized.
- **Private endpoints / user stream / WebSocket:** unauthorized.
- **MCP / Graphify / `.mcp.json` / credentials:** unauthorized.
- **Exchange-write:** unauthorized.

**Recommended state remains paused. No next phase authorized.**
