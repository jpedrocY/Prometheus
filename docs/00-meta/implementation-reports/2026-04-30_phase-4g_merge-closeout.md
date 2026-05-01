# Phase 4g Merge Closeout

## Summary

Phase 4g (V2 Strategy-Spec Memo: Participation-Confirmed Trend
Continuation, docs-only) has been merged into `main` via a `--no-ff`
merge commit. Phase 4g operationalized the Phase 4f V2 candidate
hypothesis family into a precise, predeclared, bounded strategy
specification: it selected exactly one signal timeframe (30m), one
higher-timeframe bias (4h), one session / volume bucket (1h); it
selected exactly 8 active entry features and 3 active exit / regime
features (matching the Phase 4f §23 bound); it predeclared the
threshold grid for each chosen feature (512 combinatorial variants
over 9 binary axes); it predeclared the M1 / M2 / M3 mechanism-check
decomposition required for any future V2 backtest; and it declared
all four governance labels (`stop_trigger_domain`, `break_even_rule`,
`ema_slope_method`, `stagnation_window_role`) per Phase 3v §8 and
Phase 3w §6 / §7 / §8.

Phase 4g is docs-only. No source code, tests, scripts, data, or
manifests were modified. No backtests were run. No data was acquired.
No retained verdicts were revised. No project locks changed. No
paper / shadow, live-readiness, deployment, production-key,
exchange-write, MCP, Graphify, `.mcp.json`, or credentials work
occurred.

V2 is **pre-research only**: not implemented, not backtested, not
validated, not live-ready, and **not a rescue** of R3 / R2 / F1 /
D1-A.

Phase 4 canonical remains unauthorized. Phase 4h and any successor
phase remain unauthorized. Recommended state remains **paused**.

## Files changed

The merge introduced two new docs-only files into `main`:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4g_v2-participation-confirmed-trend-continuation-spec.md`
  (Phase 4g V2 strategy-spec memo; 39 sections; 1654 lines)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4g_closeout.md`
  (Phase 4g closeout report; 418 lines)

The housekeeping commit additionally updated:

- `docs/00-meta/current-project-state.md`
  (narrow update: new Phase 4g paragraph; refreshed
  "Current phase" / "Most recent merge" code blocks)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4g_merge-closeout.md`
  (this file)

No source code, tests, scripts, data files, manifests, specs,
thresholds, parameters, project locks, or prior verdict records were
modified.

## Phase 4g commits included

| Role | SHA | Message |
| --- | --- | --- |
| Phase 4g report | `f6265cecfb7120c6459a70862fee69ac26bf5d30` | phase-4g: V2 strategy-spec memo (Participation-Confirmed Trend Continuation, docs-only) |
| Phase 4g closeout | `194075070961fa883523c49baa775469c05e8e96` | docs(phase-4g): closeout report (Markdown artefact) |

## Merge commit

| Field | Value |
| --- | --- |
| Merge SHA | `ce9659f61f5ec145e3cadd59305bd923bac73061` |
| Merge style | `--no-ff` |
| Source branch | `phase-4g/v2-participation-confirmed-trend-continuation-spec` |
| Target branch | `main` |
| Pre-merge `main` SHA | `0d0d43ffe5c54436427e6f435bdd3e73be833c31` |

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

## V2 strategy-spec conclusion

- **Phase 4g was docs-only.** No source code, tests, scripts, data,
  or manifests were modified.
- **Phase 4g turns Phase 4f's V2 research direction into a precise
  predeclared strategy spec.** Phase 4f §22 named the V2 hypothesis
  family (*Participation-Confirmed Trend Continuation*) and listed
  candidate features, candidate timeframes, exclusion rules, and
  validation requirements; Phase 4g operationalized those candidates
  into specific selections (timeframes, features, thresholds,
  mechanism-checks, governance labels).
- **V2 is still not implemented, not backtested, not validated, not
  live-ready, and not a rescue.** Phase 4g does not advance V2 toward
  any of those states; it locks the design space so future authorized
  phases (Phase 4h data-requirements / feasibility memo as primary
  recommendation; later authorized backtest phase) operate inside
  predeclared bounds.
- **V2 is structurally distinct from R3 / R2 / F1 / D1-A.** Phase 4g
  §6 records the differences: V2 uses 30m signal vs. V1's 15m; 4h
  bias vs. V1's 1h; Donchian-channel-based trend state vs. V1's
  EMA(50)/(200) state; longer compression lookback; REQUIRES
  participation / volume confirmation (which V1 does not); REQUIRES
  non-pathological derivatives-flow context (which V1 does not). V2 is
  symmetric long / short with a trend-continuation directional bias,
  NOT a contrarian funding trade like D1-A.
- **No prior verdicts are revised.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A
  MECHANISM PASS / FRAMEWORK FAIL — other — all preserved verbatim.
- **No project locks are changed.** §1.7.3 / §11.6 / mark-price stops
  preserved. Phase 3v §8 stop-trigger-domain governance preserved.
  Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
  preserved. Phase 4a public API and runtime behavior preserved.
  Phase 4e reconciliation-model design memo preserved. Phase 4f V2
  hypothesis predeclaration preserved.

## Selected timeframe matrix

Phase 4g §11 selects exactly one timeframe per role from the Phase 4f
§24 candidate matrix:

| Role | Selected | Phase 4f candidate set |
|---|---|---|
| Signal timeframe | **30m** | 15m / 30m / 1h |
| Higher-timeframe bias | **4h** | 1h / 4h |
| Session / volume bucket | **1h** | 30m / 1h |
| 5m | **diagnostic-only, NOT primary signal** | 5m diagnostic-only |

Reasoning is grounded in Phase 4f's external evidence (Moskowitz / Ooi
/ Pedersen 2012; Hurst / Ooi / Pedersen 2017; Brock / Lakonishok /
LeBaron 1992; Liu / Tsyvinski 2018 / 2021; Hattori 2024; Eross /
Urquhart / Wolfe 2019), NOT in any internal Phase 3s pattern.

## Selected feature set

**Active V2 entry features (8, matching Phase 4f §23 bound):**

1. **HTF trend bias state** (4h EMA(20)/(50) discrete comparison).
2. **Donchian breakout state** (signal-timeframe Donchian high(N1) /
   low(N1)).
3. **Donchian width percentile** (compression precondition).
4. **Range-expansion ratio** (breakout-bar TR vs. trailing mean).
5. **Relative volume + volume z-score**.
6. **Volume percentile by UTC hour** (controls intraday seasonality).
7. **Taker buy/sell imbalance**.
8. **OI delta direction + funding-rate percentile band**.

**Active V2 exit / regime features (3, matching Phase 4f §23 bound):**

1. **Time-since-entry counter** (drives unconditional time-stop).
2. **ATR percentile regime** (volatility regime; recorded, not acted
   on as exit).
3. **HTF bias state continuity** (recorded, not acted on as exit).

**Optional features documented but NOT activated by Phase 4g:**
long/short ratio; mark-price vs. trade-price divergence; breakout
close location; HH/HL structure.

## Threshold-grid summary

Phase 4g §29 predeclares the threshold grid for each chosen feature.

**Total combinatorial cardinality: 512 variants** (= 2^9 over 9
non-fixed binary grid axes).

**Grid axes (9 non-fixed):**

| # | Axis | Cardinality |
|---|---|---|
| 1 | N1 (Donchian breakout lookback) | 2 |
| 2 | P_w max (Donchian width percentile cap) | 2 |
| 3 | V_rel_min (relative volume min) | 2 |
| 4 | V_z_min (volume z-score min) | 2 |
| 5 | T_imb_min (taker-imbalance min) | 2 |
| 6 | OI_dir (OI delta direction policy) | 2 |
| 7 | Funding band ([P_fund_low, P_fund_high]) | 2 |
| 8 | N_R (fixed-R take-profit) | 2 |
| 9 | T_stop (time-stop horizon) | 2 |

Total: 2 × 2 × 2 × 2 × 2 × 2 × 2 × 2 × 2 = **512 variants**.

**No threshold may be selected from backtest outcome inspection.**
Phase 4g commits the grid; the backtest phase reports the per-variant
outcome; the choice of "best" variant must be subject to deflated
Sharpe / PBO correction, not raw in-sample Sharpe.

**512 is at the upper bound of what PBO / deflated Sharpe machinery
handles cleanly in a single backtest phase.** Phase 4g §29 flags this
and requires the future V2 backtest phase to either:

- (a) **reduce the search space further** at the backtest-phase brief
  (e.g., tying V_z_min to V_rel_min via the relationship
  V_z_min = (V_rel_min − 1) / σ_v; this would drop V_z_min from a free
  axis and bring 512 → 256), OR
- (b) **apply the full PBO / deflated Sharpe / combinatorially symmetric
  cross-validation (CSCV) machinery** per Bailey / Borwein / López de
  Prado / Zhu 2014 with the 512 variant count fully reported.

The future backtest phase MUST commit to one of (a) or (b) at brief
time, before any V2 data is acquired or any V2 backtest is run.

## Governance-label declarations

Phase 4g §22–§24 declare all four governance labels explicitly per
Phase 3v §8 and Phase 3w §6 / §7 / §8:

- **`stop_trigger_domain` (research):** `trade_price_backtest`.
- **`stop_trigger_domain` (future runtime / paper / live, if ever
  authorized):** `mark_price_runtime`.
- **`stop_trigger_domain` (future mark-price validation, if ever
  authorized):** `mark_price_backtest_candidate`.
- **`break_even_rule`:** `disabled` for the first V2 spec.
- **`ema_slope_method`:** `discrete_comparison`.
- **`stagnation_window_role`:** `metric_only` (no active rule;
  observed-but-not-acted-on, to support future regime analysis).
- **`mixed_or_unknown`** is invalid and fails closed at any decision
  boundary for all four schemes.

**Phase 4g does NOT modify Phase 3v or Phase 3w governance.** Phase
3v §8 stop-trigger-domain governance and Phase 3w §6 / §7 / §8
break-even / EMA slope / stagnation governance are preserved verbatim;
Phase 4g only declares the V2 spec's chosen values within those
governance schemes.

## Candidate next-slice decision

Phase 4g §38 presents the operator decision menu:

- **Phase 4h V2 Data Requirements and Feasibility Memo (docs-only)** —
  **PRIMARY RECOMMENDATION.** Operationalize Phase 4g §12 / §32:
  enumerate exact bulk-archive datasets needed; specify SHA256-verified
  acquisition plan analogous to Phase 3q; specify dataset-versioning
  convention; specify integrity-check rules; predeclare invalid-window
  handling; do NOT acquire data. Phase 4h would itself be docs-only.
- **Remain paused** — **CONDITIONAL SECONDARY.** Procedurally
  acceptable; defers Phase 4h.
- **Immediate V2 data acquisition** — **NOT RECOMMENDED.** Inverts the
  standard Phase 3p → Phase 3q ordering and risks parameter-tuning to
  observed coverage gaps.
- **Immediate V2 backtest** — **REJECTED.** Cannot be done before data
  is acquired AND would be data-snooping per Bailey/Borwein/López de
  Prado/Zhu 2014.
- **V2 implementation** — **REJECTED.** Requires successful backtest
  evidence (which does not exist) AND a separate authorization (which
  does not exist).
- **Paper / shadow / live-readiness / exchange-write** — **FORBIDDEN.**
  Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.

## Verification evidence

The Phase 4g branch was verified clean before merge:

- `ruff check .` passed (`All checks passed!`).
- `pytest` passed (**785 passed**).
- `mypy --strict src/prometheus` passed (`Success: no issues found in
  82 source files`).

Verification was performed against the Phase 4g branch tip
(`194075070961fa883523c49baa775469c05e8e96`) before the merge.
Phase 4g introduced docs-only changes; the verification baseline is
identical to the Phase 4f merge baseline.

## Forbidden-work confirmation

The following did **not** occur in Phase 4g or in this merge closeout:

- no successor phase started (no Phase 4h; no V2 data-requirements /
  feasibility memo; no V2 implementation; no V2 backtest; no V2 data
  acquisition; no successor authorization);
- no implementation code changed;
- no `src/prometheus/` modification;
- no test modification;
- no script modification;
- no data acquisition / patching / regeneration / modification;
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
- no Phase 3v `stop_trigger_domain` governance change;
- no Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance change;
- no Phase 4f text modification;
- no spec / backtest-plan / validation-checklist / stop-loss-policy /
  runtime-doc / phase-gates / technical-debt-register / ai-coding-handoff
  / first-run-setup-checklist substantive edit;
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
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.
- Phase 4a public API and runtime behavior.
- Phase 4e reconciliation-model design memo (governance defined; not
  implemented).
- Phase 4f V2 hypothesis predeclaration.
- **Phase 4g V2 strategy spec (this merge)**: V2 timeframe matrix,
  feature set (8 entry + 3 exit/regime), 512-variant threshold grid,
  M1 / M2 / M3 mechanism-check decomposition, four governance-label
  declarations.

All preserved verbatim. No project locks changed.

## Next authorization status

- **Phase 4 canonical:** unauthorized.
- **Phase 4h / any successor phase:** unauthorized.
- **V2 data-requirements / feasibility memo (docs-only):** Phase 4g's
  primary recommendation. Requires explicit operator authorization
  before starting; this merge does not start it.
- **V2 backtest:** unauthorized.
- **V2 data acquisition:** unauthorized.
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
