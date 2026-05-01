# Phase 4i Merge Closeout

## Summary

Phase 4i (V2 Public Data Acquisition and Integrity Validation,
docs-and-data) has been merged into `main` via a `--no-ff` merge
commit. Phase 4i acquired the six Phase 4h-predeclared minimum
dataset families for V2's first-backtest data plan from public
unauthenticated `data.binance.vision` bulk archives, normalized them
to Parquet under the existing repository partition convention,
generated six new manifests, and ran the Phase 4h §17 strict
integrity-check evidence specification on each dataset.

Phase 4i is **docs-and-data**. No source code, tests, existing
scripts, existing data, existing manifests, specs, thresholds,
parameters, project locks, or prior verdicts were modified. The
acquisition used only public unauthenticated bulk archives. No
credentials, no private endpoints, no WebSocket, no user-stream, no
listenKey, no order-placement, no exchange-write capability touched.

**Verdict — partial pass:** 4 of 6 datasets are research-eligible
(all four kline datasets: 30m × 2 and 4h × 2). 2 of 6 metrics
datasets FAIL the Phase 4h §17.4 strict gate due to upstream
`data.binance.vision` characteristics: intra-day 5-minute missing
observations + NaN values in optional ratio columns concentrated in
early-2022 data. The required `sum_open_interest` and
`sum_open_interest_value` columns are fully populated for both
symbols.

Phase 4i did NOT relax the strict gate, did NOT silently patch
gaps, did NOT forward-fill, did NOT interpolate, and did NOT silently
omit data. Phase 4i stops here for operator review per the brief
failure-path.

V2 remains **pre-research only**: not implemented, not backtested,
not validated, not live-ready, **not a rescue** of R3 / R2 / F1 /
D1-A.

Phase 4 canonical remains unauthorized. Phase 4j and any successor
phase remain unauthorized. Recommended state remains **paused**.

## Files changed

The merge introduced the following files into `main`:

- `scripts/phase4i_v2_acquisition.py` (new, standalone acquisition
  orchestrator)
- `data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json` (new)
- `data/manifests/binance_usdm_ethusdt_30m__v001.manifest.json` (new)
- `data/manifests/binance_usdm_btcusdt_4h__v001.manifest.json` (new)
- `data/manifests/binance_usdm_ethusdt_4h__v001.manifest.json` (new)
- `data/manifests/binance_usdm_btcusdt_metrics__v001.manifest.json`
  (new; `research_eligible: false`)
- `data/manifests/binance_usdm_ethusdt_metrics__v001.manifest.json`
  (new; `research_eligible: false`)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4i_v2-public-data-acquisition-and-integrity-validation.md`
  (Phase 4i acquisition + integrity report; 934 lines)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4i_closeout.md`
  (Phase 4i closeout report; 403 lines)

The housekeeping commit additionally adds:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4i_merge-closeout.md`
  (this file)
- `docs/00-meta/current-project-state.md`
  (narrow update: new Phase 4i paragraph; refreshed
  "Current phase" / "Most recent merge" code blocks)

`data/raw/**` and `data/normalized/**` artefacts are NOT committed
(gitignored per existing convention). They are local research
evidence reproducible from the public bulk archive via
`scripts/phase4i_v2_acquisition.py`.

No source code under `src/prometheus/`, no tests, and no existing
scripts were modified.

## Phase 4i commits included

| Role | SHA | Message |
| --- | --- | --- |
| Phase 4i acquisition + report | `6913d29ff70c683e2f10b61c873241adaffecfcf` | phase-4i: V2 public data acquisition and integrity validation (docs-and-data) |
| Phase 4i closeout | `408301f1eb5b16cfac35f73936738bd973b42caa` | docs(phase-4i): closeout report (Markdown artefact) |

## Merge commit

| Field | Value |
| --- | --- |
| Merge SHA | `a2c414e8cf7e36235db4c97905f9cc890a848e70` |
| Merge style | `--no-ff` |
| Source branch | `phase-4i/v2-public-data-acquisition-and-integrity-validation` |
| Target branch | `main` |
| Pre-merge `main` SHA | `4a0edf980c01a1c3c9336ad89dd142685a53a445` |

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

## Dataset families acquired

Phase 4i acquired exactly the six Phase 4h-predeclared minimum V2
dataset families from public unauthenticated `data.binance.vision`
bulk archives, for the date range 2022-01-01 through 2026-03-31 UTC:

1. **BTCUSDT 30m trade-price klines** —
   `binance_usdm_btcusdt_30m__v001` (51 monthly archives; 74 448
   bars).
2. **ETHUSDT 30m trade-price klines** —
   `binance_usdm_ethusdt_30m__v001` (51 monthly archives; 74 448
   bars).
3. **BTCUSDT 4h trade-price klines** —
   `binance_usdm_btcusdt_4h__v001` (51 monthly archives; 9 306
   bars).
4. **ETHUSDT 4h trade-price klines** —
   `binance_usdm_ethusdt_4h__v001` (51 monthly archives; 9 306
   bars).
5. **BTCUSDT metrics** — `binance_usdm_btcusdt_metrics__v001` (1551
   daily archives; 446 555 / 446 688 expected 5-minute records).
6. **ETHUSDT metrics** — `binance_usdm_ethusdt_metrics__v001` (1551
   daily archives; 446 555 / 446 688 expected 5-minute records).

**Total archives acquired: 3 306** (204 monthly klines + 3 102 daily
metrics) at 8 parallel workers, ~11 minutes wall-clock, with
SHA256-verification of every raw archive against its paired
`.CHECKSUM` companion file.

**Phase 4i did NOT acquire mark-price 30m / 4h** (DEFERRED to a future
`mark_price_backtest_candidate` validation pass per Phase 4h §20).

**Phase 4i did NOT acquire aggTrades** (OPTIONAL / DEFERRED per Phase
4h §7.E; klines `taker_buy_volume` column is sufficient for V2's
predeclared taker-imbalance feature).

**Phase 4i did NOT re-acquire funding-rate history.** v002 funding
manifests (`binance_usdm_btcusdt_funding__v002` and
`binance_usdm_ethusdt_funding__v002`) remain reused per Phase 4h §22.

**Phase 4i added the standalone script** `scripts/phase4i_v2_acquisition.py`.
It does not modify any existing `prometheus.research.data.*` module,
does not extend the `Interval` enum, does not modify any existing
script, does not require credentials, does not read `.env`, and does
not add API-key support.

## Integrity verdict

- **Phase 4i verdict: PARTIAL PASS.**
- **Four kline datasets PASS strict gate.** All four kline datasets
  satisfy every Phase 4h §17.1 integrity check: zero gaps, monotone
  timestamps, zero duplicate timestamps, zero boundary alignment
  violations, zero close-time consistency violations, zero OHLC
  sanity violations, zero volume sanity violations,
  `taker_buy_volume` present and bounded by `volume`, zero symbol /
  interval consistency violations, full date-range coverage from
  2022-01-01 00:00:00 UTC to coverage-required-last per interval.
- **Two metrics datasets FAIL Phase 4h §17.4 strict gate.** Both
  metrics datasets satisfy monotone timestamps, zero duplicate
  timestamps, zero boundary alignment violations, zero symbol
  consistency violations, zero non-negative OI violations, zero
  non-negative ratio violations, and date-range coverage true. They
  fail on `missing_observations` (intra-day 5-minute gaps) and
  `nonfinite_violations` (NaN values in optional ratio columns).
- **No strict gate was relaxed.** Phase 4h §17.4 remains the binding
  research_eligible criterion for metrics. Phase 4i does NOT modify
  the strict gate.
- **No data was patched, forward-filled, interpolated, or silently
  omitted.** All gaps are recorded verbatim in
  `quality_checks.gap_locations` and `invalid_windows` (capped at
  200 entries per manifest per Phase 3q-style reporting cap).
- **Phase 4i stops for operator review** per the brief failure-path.

## research_eligible verdicts

```text
binance_usdm_btcusdt_30m__v001:        research_eligible: true
binance_usdm_ethusdt_30m__v001:        research_eligible: true
binance_usdm_btcusdt_4h__v001:         research_eligible: true
binance_usdm_ethusdt_4h__v001:         research_eligible: true
binance_usdm_btcusdt_metrics__v001:    research_eligible: false
binance_usdm_ethusdt_metrics__v001:    research_eligible: false
```

## Metrics failure details

- **BTCUSDT metrics**: 446 555 / 446 688 records (133 short =
  ~0.03 % of expected 4-year coverage); 5 699 missing 5-minute
  observations across the 4-year coverage; 91 840 rows with at least
  one NaN in optional ratio columns
  (`count_toptrader_long_short_ratio`,
  `sum_toptrader_long_short_ratio`, `count_long_short_ratio`,
  `sum_taker_long_short_vol_ratio`); 0 missing daily archives.
- **ETHUSDT metrics**: 446 555 / 446 688 records (133 short =
  ~0.03 % of expected 4-year coverage); 3 631 missing 5-minute
  observations across the 4-year coverage; 91 841 rows with at
  least one NaN in optional ratio columns; 0 missing daily archives.
- **The required `sum_open_interest` and `sum_open_interest_value`
  columns are FULLY POPULATED** (zero NaN) for both symbols across
  the entire 4-year coverage.
- **NaN values are concentrated in optional ratio columns,
  especially early 2022.** Sample distribution:
  - BTCUSDT 2022-01: ~97 % NaN in `count/sum_toptrader_long_short_ratio`
    and `sum_taker_long_short_vol_ratio`; ~60 % NaN in
    `count_long_short_ratio`.
  - BTCUSDT 2026-03: 0 % NaN in all ratio columns.
  - ETHUSDT shows the same pattern.
- **This observation does NOT authorize relaxation or backtesting.**
  Phase 4i preserves Phase 4h §17.4 verbatim. The metrics datasets
  remain `research_eligible: false`. A future operator-authorized
  docs-only governance memo (analogous to Phase 3r §8 for
  mark-price) is the only path that could permit partial-eligibility
  use of the OI subset; Phase 4i does NOT propose or initiate such a
  memo.

## Verification evidence

The Phase 4i branch was verified clean before merge:

- `ruff check .` passed (`All checks passed!`).
- `pytest` passed (**785 passed**).
- `mypy --strict src/prometheus` passed (`Success: no issues found
  in 82 source files`).

Verification was performed against the Phase 4i branch tip
(`408301f1eb5b16cfac35f73936738bd973b42caa`) before the merge.

## Forbidden-work confirmation

The following did **not** occur in Phase 4i or in this merge closeout:

- no successor phase started (no Phase 4j; no V2 backtest; no V2
  implementation; no successor authorization);
- no V2 backtest run;
- no V2 implementation;
- no diagnostics run;
- no Q1–Q7 rerun;
- no `scripts/phase3q_5m_acquisition.py` execution;
- no `scripts/phase3s_5m_diagnostics.py` execution;
- no mark-price 30m / 4h acquisition;
- no `aggTrades` acquisition;
- no spot data acquisition;
- no cross-venue data acquisition;
- no funding-rate re-acquisition (v002 reused);
- no v002 dataset / manifest modification;
- no v001-of-5m dataset / manifest modification;
- no v003 dataset created;
- no Phase 3p §4.7 amendment;
- no Phase 3r §8 mark-price gap governance modification;
- no Phase 3v `stop_trigger_domain` governance modification;
- no Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance modification;
- no Phase 4f text modification;
- no Phase 4g V2 strategy-spec modification;
- no Phase 4h text modification;
- no `src/prometheus/**` modification;
- no `tests/**` modification;
- no existing `scripts/**` modification (`scripts/phase4i_v2_acquisition.py`
  is new and standalone);
- no `prometheus.research.data.*` extension;
- no `Interval` enum extension;
- no `pyproject.toml` modification;
- no `.gitignore` modification;
- no `.mcp.json` modification;
- no `uv.lock` modification;
- no `.env` file creation;
- no credential storage / request / use;
- no authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls;
- no production alerting / Telegram / n8n production routes;
- no MCP enabling / Graphify enabling;
- no deployment artefact created;
- no paper / shadow runtime created;
- no live-readiness implication;
- no order placement / cancellation;
- no real exchange adapter implementation;
- no exchange-write capability;
- no reconciliation implementation;
- no retained-evidence verdict revision;
- no project-lock revision;
- no threshold / parameter modification;
- no §11.6 / §1.7.3 governance change;
- no `docs/00-meta/implementation-ambiguity-log.md` modification.

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
- Phase 4g V2 strategy spec.
- Phase 4h V2 data-requirements / feasibility memo.
- **Phase 4i V2 public data acquisition + integrity validation (this
  merge):** 4 of 6 datasets research-eligible (klines: 30m × 2 +
  4h × 2); 2 of 6 metrics datasets `research_eligible: false`; new
  standalone acquisition script; six new manifests; partial-pass
  verdict; stops for operator review.

All preserved verbatim. No project locks changed.

## Operator decision menu

- **Option A — Remain paused, accept partial-pass evidence.**
  **PRIMARY RECOMMENDATION.** Phase 4i deliverables (script + 6
  manifests + report + closeout) exist on `main`. Trade-price 30m
  and 4h klines are research-eligible. Metrics datasets are NOT
  research-eligible under the strict gate. No backtest is run. No
  successor phase authorized.
- **Option B — Future docs-only metrics governance memo analogous
  to Phase 3r §8.** **CONDITIONAL SECONDARY.** A future docs-only
  memo could propose either (a) a `metrics_ineligibility_governance`
  rule analogous to Phase 3r §8 (record gaps in `invalid_windows`,
  exclude affected V2 setups per-bar), or (b) a partial-eligibility
  scheme permitting V2 entry feature 8 OI sub-component to use only
  the OI subset (`sum_open_interest`, `sum_open_interest_value`
  fully-populated columns) without requiring the optional ratio
  columns to be finite at the alignment timestamp. Phase 4i does
  NOT propose either of these as a recommendation; an operator
  decision is required to authorize a separate memo. **This merge
  does NOT start that memo.**
- **Option C — Mark-price 30m / 4h acquisition.** **NOT RECOMMENDED
  NOW.** Mark-price 30m / 4h was deferred by Phase 4h §20 because it
  is not required for V2's first backtest (`trade_price_backtest`
  provenance per Phase 4g §24). Acquiring it before V2's first
  backtest evidence inverts the standard ordering.
- **Option D — `aggTrades` acquisition.** **NOT RECOMMENDED NOW.**
  `aggTrades` is OPTIONAL / DEFERRED per Phase 4h §7.E. Phase 4i
  confirms that klines `taker_buy_volume` is fully populated for V2
  entry feature 7. `aggTrades` adds complexity without clear V2
  benefit at this boundary.
- **Option E — Immediate V2 backtest.** **REJECTED.** The brief
  forbids it: *"If any family is not research_eligible, Phase 4i
  must stop for operator review and must not proceed to any backtest
  or successor phase."*
- **Option F — V2 implementation.** **REJECTED.** Requires
  successful backtest evidence (which does not exist).
- **Option G — Paper / shadow / live-readiness / exchange-write.**
  **FORBIDDEN.** Per `docs/12-roadmap/phase-gates.md`, none of these
  gates is met.

## Next authorization status

- **Phase 4 canonical:** unauthorized.
- **Phase 4j / any successor phase:** unauthorized.
- **V2 metrics governance memo (docs-only, future):** Phase 4i's
  conditional secondary recommendation. Requires explicit operator
  authorization before starting; this merge does not start it.
- **V2 backtest:** unauthorized.
- **V2 implementation:** unauthorized.
- **Mark-price 30m / 4h acquisition:** unauthorized.
- **`aggTrades` acquisition:** unauthorized.
- **Paper / shadow:** unauthorized.
- **Live-readiness:** unauthorized.
- **Deployment:** unauthorized.
- **Production keys:** unauthorized.
- **Authenticated APIs:** unauthorized.
- **Private endpoints / user stream / WebSocket:** unauthorized.
- **MCP / Graphify / `.mcp.json` / credentials:** unauthorized.
- **Exchange-write:** unauthorized.

**Recommended state remains paused. No next phase authorized.**
