# Phase 4j Merge Closeout

## Summary

Phase 4j (V2 Metrics Data Governance Memo, docs-only) has been
merged into `main` via a `--no-ff` merge commit. Phase 4j adopted
the **Phase 4j §11 metrics OI-subset partial-eligibility rule** as
the binding governance for the Phase 4i metrics partial-pass
evidence. The rule mirrors Phase 3r §8 mark-price gap governance —
keep manifests globally `research_eligible: false`, permit feature-
level partial-use under strict per-record exclusion, no patching,
no forward-fill, no synthetic data — transposed from per-trade
exclusion (Q6 mark-price) to per-bar exclusion (V2 candidate setup
metrics OI).

Phase 4j is docs-only. No source code, tests, existing scripts,
existing data, existing manifests, specs, thresholds, parameters,
project locks, or prior verdicts were modified. No data was
acquired. No data was downloaded. No backtests were run. No mark-
price 30m / 4h or aggTrades were acquired. No funding-rate was
re-acquired. No paper / shadow, live-readiness, deployment,
production-key, exchange-write, MCP, Graphify, `.mcp.json`, or
credentials work occurred.

V2 remains **pre-research only**: not implemented, not backtested,
not validated, not live-ready, **not a rescue** of R3 / R2 / F1 /
D1-A.

Phase 4 canonical remains unauthorized. Phase 4k and any successor
phase remain unauthorized. Recommended state remains **paused**.

## Files changed

The merge introduced two new docs-only files into `main`:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4j_v2-metrics-data-governance.md`
  (Phase 4j governance memo; 26 sections; 1397 lines)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4j_closeout.md`
  (Phase 4j closeout report; 436 lines)

The housekeeping commit additionally adds:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4j_merge-closeout.md`
  (this file)
- `docs/00-meta/current-project-state.md`
  (narrow update: new Phase 4j paragraph; refreshed
  "Current phase" / "Most recent merge" code blocks)

No source code under `src/prometheus/`, no tests, no existing
scripts, no existing data, and no existing manifests were modified.

## Phase 4j commits included

| Role | SHA | Message |
| --- | --- | --- |
| Phase 4j memo | `6fa92766da5b47ef1d5ebf2b7f7c8334e15b317e` | phase-4j: V2 metrics data governance memo (docs-only) |
| Phase 4j closeout | `1b2d4c8f57bd4356e67b8a35a255fbf8d5d9ce5e` | docs(phase-4j): closeout report (Markdown artefact) |

## Merge commit

| Field | Value |
| --- | --- |
| Merge SHA | `ea948017c77f4a028427f9c8515e973cd274abad` |
| Merge style | `--no-ff` |
| Source branch | `phase-4j/v2-metrics-data-governance` |
| Target branch | `main` |
| Pre-merge `main` SHA | `17ebb755ce32ccc5d605329d9972df2e4ce2f140` |

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

## Governance conclusion

- **Phase 4j was docs-only.** No source code, tests, scripts, data,
  or manifests were modified.
- **Phase 4j adopts Phase 4j §11 as binding metrics OI-subset
  partial-eligibility governance.** The rule is immutable from
  operator approval forward; future amendments require a separately
  authorized governance memo.
- **Metrics manifests remain globally `research_eligible: false`.**
  Phase 4i `binance_usdm_btcusdt_metrics__v001.manifest.json` and
  `binance_usdm_ethusdt_metrics__v001.manifest.json` are preserved
  byte-for-byte verbatim.
- **Feature-level partial-eligibility is permitted only for the
  OI subset.** The four columns `create_time`, `symbol`,
  `sum_open_interest`, `sum_open_interest_value` may be used by V2's
  first backtest under per-bar exclusion; the four optional ratio
  columns may NOT be used.
- **Optional ratio columns remain forbidden for V2's first backtest.**
  `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`,
  `count_long_short_ratio`, `sum_taker_long_short_vol_ratio`.
- **No data or manifests are modified.**
- **No V2 backtest is authorized.** Phase 4j defines what a future
  V2 backtest must do *if* it is ever authorized; it does NOT
  authorize one.

## Metrics evidence recap

Per Phase 4i §"research_eligible verdicts":

```text
binance_usdm_btcusdt_30m__v001:        research_eligible: true
binance_usdm_ethusdt_30m__v001:        research_eligible: true
binance_usdm_btcusdt_4h__v001:         research_eligible: true
binance_usdm_ethusdt_4h__v001:         research_eligible: true
binance_usdm_btcusdt_metrics__v001:    research_eligible: false
binance_usdm_ethusdt_metrics__v001:    research_eligible: false
```

Metrics failure breakdown (Phase 4i §"Metrics integrity results"):

- BTCUSDT metrics: 446 555 / 446 688 records; 5 699 missing 5-minute
  observations; 91 840 rows with ≥ 1 NaN in optional ratio columns;
  0 missing daily archives; required `sum_open_interest` and
  `sum_open_interest_value` FULLY POPULATED (zero NaN).
- ETHUSDT metrics: 446 555 / 446 688 records; 3 631 missing 5-minute
  observations; 91 841 rows with ≥ 1 NaN in optional ratio columns;
  0 missing daily archives; required `sum_open_interest` and
  `sum_open_interest_value` FULLY POPULATED (zero NaN).
- NaN values are concentrated in optional ratio columns, especially
  early-2022 data (~97 % NaN in 2022-01 ratio columns; ~0 % NaN by
  2026-03).

## Binding metrics governance rule

**Phase 4j §11 metrics OI-subset partial-eligibility rule** —
binding from operator approval (this merge) forward; immutable
absent a separately authorized governance amendment.

### Manifest scope

- **Metrics manifests remain globally `research_eligible: false`.**
  Both Phase 4i metrics manifests preserved verbatim. No corrected
  manifest. No `__v002` metrics manifest. No v003.

### OI subset (permitted for feature-level use)

- `create_time`
- `symbol`
- `sum_open_interest`
- `sum_open_interest_value`

### Optional ratio columns (forbidden for V2 first backtest)

- `count_toptrader_long_short_ratio`
- `sum_toptrader_long_short_ratio`
- `count_long_short_ratio`
- `sum_taker_long_short_vol_ratio`

These columns MUST NOT be read by the V2 feature pipeline, used for
any filter, label, diagnostic, post-hoc interpretation, or sensitivity
analysis variant that V2 reports as primary, or used to derive any
V2 entry / exit / regime feature in V2's first backtest.

### Per-bar exclusion test

- Any 30m V2 signal bar is **OI-feature-eligible** if and only if all
  six aligned 5-minute metrics records (at offsets 0, 5, 10, 15, 20,
  25 minutes from the bar's open_time, all UTC) are present AND each
  has non-NaN `sum_open_interest` AND non-NaN
  `sum_open_interest_value`.
- Any 30m signal bar that fails this check is **excluded from V2
  candidate setup generation entirely** (the bar produces zero V2
  candidate setups regardless of other features' values).

### Forbidden patterns

- **No forward-fill.**
- **No interpolation.**
- **No imputation.**
- **No replacement.**
- **No synthetic OI data.**
- **No silent omission.**

### Reporting requirements (binding on any future V2 backtest)

- **Exclusion counts must be reported** (per-symbol, per-day,
  per-30m-bar with reason `metrics_oi_missing_or_invalid`,
  cumulative).
- **Sensitivity analysis must compare main-cell vs.
  exclude-entire-affected-days** — i.e., a sensitivity-cell variant
  that ALSO excludes any 30m bar whose date contains ANY metrics
  `invalid_window`, regardless of whether the bar's specific 30m
  window is OI-feature-eligible. Material divergence between the
  two cells must be reported and stop the backtest for operator
  review before claiming results.

### OI delta computation rule

- For each 30m signal bar at `bar_open_time_ms` that passes the
  per-bar exclusion test:
  - `oi_at_bar_close` = the metrics record with `create_time =
    bar_open_time_ms + 25 * 60 * 1000` (last 5-minute record in
    the current 30m window).
  - `oi_at_prev_window_close` = the metrics record with
    `create_time = bar_open_time_ms - 5 * 60 * 1000` (last
    5-minute record in the previous 30m window).
  - `oi_delta = oi_at_bar_close - oi_at_prev_window_close`.
- Variant rules (mean-OI-over-window, exponentially-smoothed-OI,
  etc.) are NOT permitted in V2's first backtest. Variants require
  a separately authorized strategy-spec amendment.

### Immutability

- **The rule is immutable absent a separately authorized governance
  amendment.** Future amendments require a docs-only memo
  explicitly amending Phase 4j §11.

## Backtest preconditions

A future V2 backtest remains BLOCKED until ALL of the following are
satisfied (per Phase 4j §20):

1. **Phase 4j must be merged to `main`.** ✓ Achieved by this merge.
2. **`docs/00-meta/current-project-state.md` must record the rule.**
   Updated by this merge's housekeeping commit.
3. **A separate V2 backtest-plan phase must be authorized.** A
   future operator-authorized docs-only Phase 4k memo would
   operationalize the per-bar exclusion algorithm, predeclare the
   backtest implementation plan, and predeclare evidence thresholds.
4. **The plan must predeclare:**
   - the per-bar exclusion algorithm implementation matching Phase
     4j §16 verbatim;
   - exclusion-counts reporting matching Phase 4j §11.6;
   - sensitivity analysis matching Phase 4j §11.7;
   - PBO / deflated Sharpe / CSCV machinery per Phase 4g §29 / §31
     and Phase 4f §28;
   - chronological holdout and OOS window definitions per Phase 4g
     §31;
   - full M1 / M2 / M3 mechanism-check decomposition implementation
     per Phase 4g §30;
   - explicit confirmation that no optional ratio column is used.
5. **No V2 backtest is authorized by Phase 4j.** Phase 4j is the
   governance rule; the backtest-plan and backtest-execution phases
   are separate operator decisions.

## Verification evidence

The Phase 4j branch was verified clean before merge:

- `ruff check .` passed (`All checks passed!`).
- `pytest` passed (**785 passed**).
- `mypy --strict src/prometheus` passed (`Success: no issues found
  in 82 source files`).

Verification was performed against the Phase 4j branch tip
(`1b2d4c8f57bd4356e67b8a35a255fbf8d5d9ce5e`) before the merge.
Phase 4j introduced docs-only changes; the verification baseline
is identical to the Phase 4i merge baseline.

## Forbidden-work confirmation

The following did **not** occur in Phase 4j or in this merge closeout:

- no successor phase started (no Phase 4k; no V2 backtest-plan memo;
  no V2 backtest; no V2 implementation; no successor authorization);
- no V2 backtest run;
- no V2 implementation;
- no diagnostics run;
- no Q1–Q7 rerun;
- no `scripts/phase3q_5m_acquisition.py` execution;
- no `scripts/phase3s_5m_diagnostics.py` execution;
- no `scripts/phase4i_v2_acquisition.py` execution;
- no data acquisition / patching / regeneration / modification;
- no data download;
- no `data/manifests/*.manifest.json` modification (all Phase 4i
  manifests, v002 manifests, and v001-of-5m manifests preserved
  verbatim);
- no corrected manifest created;
- no `__v002` metrics manifest created;
- no v003 dataset family created;
- no mark-price 30m / 4h acquisition;
- no `aggTrades` acquisition;
- no spot data acquisition;
- no cross-venue data acquisition;
- no funding-rate re-acquisition;
- no silent OI patching;
- no forward-fill;
- no interpolation;
- no imputation;
- no silent omission;
- no optional ratio-column activation;
- no OI feature removal from V2;
- no Phase 4f text modification;
- no Phase 4g V2 strategy-spec modification;
- no Phase 4h text modification;
- no Phase 4i text modification;
- no Phase 4i acquisition script modification;
- no Phase 3r §8 mark-price gap governance modification;
- no Phase 3v `stop_trigger_domain` governance modification;
- no Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance modification;
- no retained verdict revision (R3 / H0 / R1a / R1b-narrow / R2 /
  F1 / D1-A all preserved verbatim);
- no project-lock revision;
- no §11.6 / §1.7.3 governance change;
- no `src/prometheus/**` modification;
- no `tests/**` modification;
- no existing `scripts/**` modification;
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
- Phase 4i V2 public data acquisition + integrity validation
  (partial-pass; klines × 4 research-eligible; metrics × 2
  `research_eligible: false`).
- **Phase 4j V2 metrics OI-subset partial-eligibility governance
  (this merge):** binding rule for any future V2 backtest;
  manifests preserved verbatim; OI subset feature-eligible under
  per-bar exclusion; optional ratios forbidden; no patching.

All preserved verbatim. No project locks changed.

## Operator decision menu

- **Option A — Adopt §11 and remain paused.** **PRIMARY
  RECOMMENDATION.** The Phase 4j §11 rule is now in effect on
  `main` from this merge forward. Strategy execution remains paused.
  No V2 backtest runs.
- **Option B — Adopt §11 and authorize future docs-only V2
  backtest-plan phase (Phase 4k).** **CONDITIONAL SECONDARY.**
  The operator approves §11 (achieved by this merge) AND authorizes
  a follow-on docs-only memo that operationalizes the per-bar
  exclusion algorithm, predeclares the backtest implementation
  plan, predeclares evidence thresholds, and predeclares variant
  comparison rules. The plan phase would itself be docs-only. **This
  merge does NOT start that phase.**
- **Option C — Reject §11 and keep V2 backtesting blocked.** **NOT
  RECOMMENDED.** Equivalent to the post-Phase-4i boundary; stalls
  V2 even though V2-required `sum_open_interest` is fully populated.
- **Option D — Remove OI feature from V2.** **NOT RECOMMENDED /
  REQUIRES SEPARATE AMENDMENT.** Modifies Phase 4g §28; the Phase 4j
  brief explicitly forbade Phase 4j from doing this.
- **Option E — Permit patching / forward-fill / interpolation.**
  **REJECTED.** Forbidden by Phase 3r §8 / Phase 3p §4.7 / Phase
  4h §17–§19 / Phase 4i §17 / Phase 4j §11.5.
- **Option F — Immediate V2 backtest.** **REJECTED.** Phase 4i and
  Phase 4j both block this until a separately authorized
  backtest-plan phase is in place.
- **Option G — Paper / shadow / live-readiness / exchange-write.**
  **FORBIDDEN.** Per `docs/12-roadmap/phase-gates.md`, none of
  these gates is met.

## Next authorization status

- **Phase 4 canonical:** unauthorized.
- **Phase 4k / any successor phase:** unauthorized.
- **V2 backtest-plan memo (docs-only, future Phase 4k):** Phase 4j's
  conditional secondary recommendation. Requires explicit operator
  authorization before starting; this merge does not start it.
- **V2 backtest:** unauthorized.
- **V2 implementation:** unauthorized.
- **Optional ratio-column activation:** unauthorized.
- **OI feature removal from V2:** unauthorized.
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
