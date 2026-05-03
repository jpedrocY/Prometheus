# Phase 4l Closeout

## Summary

Phase 4l implemented the standalone V2 backtest script
`scripts/phase4l_v2_backtest.py` per Phase 4k methodology, ran the
full 512-variant grid across BTCUSDT (primary) and ETHUSDT
(comparison) on the predeclared chronological train / validation /
OOS holdout windows under three cost cells (LOW = 1 bp, MEDIUM =
4 bps, HIGH = 8 bps slippage per side; HIGH = §11.6 gate), and
emitted a Verdict C HARD REJECT. The Phase 4l backtest execution
report at
`docs/00-meta/implementation-reports/2026-04-30_phase-4l_v2-backtest-execution.md`
records all required tables, methodology adherence, forensic
analysis, and forbidden-work confirmation.

**Phase 4l deliverables:** one new standalone research script
(`scripts/phase4l_v2_backtest.py`), one new Markdown backtest report
(2026-04-30_phase-4l_v2-backtest-execution.md), and this closeout.
Local gitignored research outputs under `data/research/phase4l/` are
reproducible from the orchestrator script with the pinned RNG seed
(202604300).

**Final verdict: C — V2 framework HARD REJECT.**

**Catastrophic-floor predicate triggered:** CFP-1 critical (512 / 512
variants produced fewer than the 30-OOS-trade threshold; BTC-train-best
variant produced 0 OOS trades). M1 / M2 / M3 mechanism checks NOT
meaningfully evaluable. Verdict logic correctly prioritizes CFP-1
critical over M1 FAIL — the underlying cause is structural, not an
organic mechanism failure.

**Root cause (forensic):** Phase 4l's standalone implementation
matches the Phase 4k methodology exactly. The 8-feature AND chain
(without stop-distance filter) yields ~15 raw long-side setups per
variant per symbol over the 4-year coverage. **All such setups are
subsequently rejected by the V1-inherited stop-distance filter
(0.60 × ATR(20) ≤ stop_distance ≤ 1.80 × ATR(20)).** With V2's locked
20-bar / 40-bar Donchian setup window per Phase 4g §29 axis 1, the
setup_low — defined per Phase 4g §19 as "the lowest low of the
previous N1 30m bars" — sits 3-5 × ATR(20) below the breakout-bar
close, exceeding the 1.80 × ATR upper bound. This is a **structural
incompatibility** between V2's longer Donchian setup and the V1
stop-distance bounds (originally calibrated for V1's 8-bar setup
window). Analogous to F1's HARD REJECT under Phase 3c §7.3
catastrophic-floor.

**Phase 4l was docs-and-code, narrowly scoped:**

- one new standalone research script (`scripts/phase4l_v2_backtest.py`);
- two new Markdown reports under `docs/00-meta/implementation-reports/`;
- local gitignored outputs under `data/research/phase4l/` (not
  committed; reproducible from orchestrator);
- no `src/prometheus/`, `tests/`, existing `scripts/`, `data/raw/`,
  `data/normalized/`, `data/manifests/` modification;
- no V2 implementation;
- no Phase 4g spec / Phase 4j §11 / Phase 4k methodology / project
  lock / threshold change;
- no retained-evidence verdict revision;
- no merge to main from Phase 4l.

**Verification (run on the post-Phase-4k-merge tree):**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.
- Optional ratio-column non-access static scan: zero forbidden names
  in the script.
- Phase 4j §11 per-bar exclusion algorithm: matches §16 pseudocode
  verbatim.
- No forbidden data access; no network I/O; no credential request;
  no authenticated API access; no production-key request; no
  mark-price/aggTrades/spot/cross-venue acquisition; no v003
  creation.

R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
F1 / D1-A retained research evidence only; R2 FAILED — §11.6
cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS /
FRAMEWORK FAIL — other; **V2 HARD REJECT (Phase 4l, structural
CFP-1 critical)**; §11.6 = 8 bps HIGH per side; §1.7.3 project-level
locks (including mark-price stops); v002 verdict provenance; Phase
3q mark-price 5m manifests `research_eligible: false`; Phase 3r §8
mark-price gap governance; Phase 3v §8 stop-trigger-domain
governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
governance; Phase 4a public API and runtime behavior; Phase 4e
reconciliation-model design memo; Phase 4f V2 hypothesis
predeclaration; Phase 4g V2 strategy spec; Phase 4h V2
data-requirements / feasibility memo; Phase 4i V2 acquisition +
integrity report (partial-pass); Phase 4i metrics manifests
`research_eligible: false`; Phase 4j §11 metrics OI-subset
partial-eligibility rule; Phase 4k V2 backtest-plan methodology —
all preserved verbatim.

V2 remains **pre-research only**: not implemented; not validated;
not live-ready; **not a rescue** of R3 / R2 / F1 / D1-A. **Verdict C
HARD REJECT is terminal for the V2 first-spec.**

**Phase 4 canonical remains unauthorized.** **Phase 4m / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, and exchange-write all remain unauthorized.**

**Recommended state remains paused. No next phase authorized.**

## Files changed

```text
scripts/phase4l_v2_backtest.py                                                 (new; standalone research script)
docs/00-meta/implementation-reports/2026-04-30_phase-4l_v2-backtest-execution.md  (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4l_closeout.md             (new — this file)
```

Local gitignored Phase 4l research outputs under
`data/research/phase4l/` (NOT committed):

```text
data/research/phase4l/run_metadata.json
data/research/phase4l/tables/manifest_references.csv
data/research/phase4l/tables/parameter_grid.csv
data/research/phase4l/tables/split_boundaries.csv
data/research/phase4l/tables/btc_train_variants.csv
data/research/phase4l/tables/btc_validation_variants.csv
data/research/phase4l/tables/btc_oos_variants.csv
data/research/phase4l/tables/eth_train_variants.csv
data/research/phase4l/tables/eth_validation_variants.csv
data/research/phase4l/tables/eth_oos_variants.csv
data/research/phase4l/tables/btc_train_best_variant.csv
data/research/phase4l/tables/btc_train_best_cost_cells.csv
data/research/phase4l/tables/m1_m2_m3_mechanism_checks.csv
data/research/phase4l/tables/cost_sensitivity.csv
data/research/phase4l/tables/pbo_summary.csv
data/research/phase4l/tables/deflated_sharpe_summary.csv
data/research/phase4l/tables/metrics_oi_exclusions.csv
data/research/phase4l/tables/main_vs_exclude_affected_days.csv
data/research/phase4l/tables/trade_distribution_by_month_regime.csv
data/research/phase4l/tables/verdict_declaration.csv
data/research/phase4l/tables/catastrophic_floor_predicates.csv
data/research/phase4l/tables/forbidden_work_confirmation.csv
```

(Plots directory `data/research/phase4l/plots/` exists but is empty
because matplotlib is not in the project venv; documented in the
report. The omission does NOT trigger Verdict D since underlying
CSV tables that would back the plots are produced.)

No source code under `src/prometheus/`, no tests under `tests/`, no
existing scripts, no data under `data/raw/` / `data/normalized/`,
and no manifests under `data/manifests/` were modified by Phase 4l.

## Backtest execution conclusion

- **Phase 4l ran the V2 backtest exactly per Phase 4k methodology.**
  All 512 variants × 2 symbols × 3 cost cells × 3 windows = 4 608
  result cells reported.
- **Per-bar OI eligibility on Phase 4i metrics datasets:** 99.957%
  (74 415 / 74 448) on each symbol; 0.044% excluded fraction (well
  under CFP-9 5% threshold).
- **No trades produced across all 512 variants on either symbol.**
  The 8-feature AND chain produces ~15 raw long-side setups per
  variant per symbol; all are rejected by the V1-inherited
  stop-distance filter (0.60-1.80 × ATR(20)) because V2's locked
  20/40-bar Donchian setup window produces stop distances of
  3-5 × ATR(20).
- **M1 / M2 / M3 mechanism checks not meaningfully evaluable** under
  the 0-trade root cause. Computed and reported as trivial
  false / 0-difference results.
- **PBO (train internal CSCV, S = 16) = 0.500** — the trivial "no
  signal" reading expected when all 512 variants have identical
  0-trade behavior.
- **Deflated Sharpe = 0** for every variant — same trivial reason.
- **§11.6 HIGH cost-sensitivity:** trivially passes (mean_R = 0,
  not negative); but methodologically irrelevant under 0-trade
  population.
- **CFP-1 critical** is the binding driver of Verdict C.

## Verdict

**Verdict C — V2 framework HARD REJECT.**

**Reason:** CFP-1 critical: 512 / 512 variants with <30 OOS trades on
BTCUSDT; BTC-train-best variant has 0 OOS trades. M1 / M2 / M3
mechanism checks not meaningfully evaluable. HARD REJECT analogous to
F1 catastrophic-floor pattern (Phase 3c §7.3). Terminal for V2
first-spec under Phase 4g §29 locked threshold grid + V1-inherited
stop-distance filter (0.60-1.80 × ATR).

## Dataset inputs

| Dataset | Manifest SHA256 | research_eligible | feature_use |
|---|---|---|---|
| `binance_usdm_btcusdt_30m__v001` | `3cdf6fb91ffca8acc2a69ae05a00745a031360c01c585a75f876c64d42230da8` | true | full |
| `binance_usdm_btcusdt_4h__v001` | `b2413e7fbbacfa091f2f42af8220ee83b55ee2511ee2b7be070e936c5761180a` | true | full |
| `binance_usdm_btcusdt_metrics__v001` | `41d6a8e45a1f992ce813838640c28534dcd1885b4482d01d4ded7809a208baf7` | false | oi_subset_only_per_phase_4j_§11 |
| `binance_usdm_btcusdt_funding__v002` | `da719007f9358d45b38792e50fa16ed0e470c0d983345651e6efae9349706007` | (v002 lock) | full |
| `binance_usdm_ethusdt_30m__v001` | `0a7502c5e09916529e50951bd503e1a2ac95d372e99ba65f4cb3bfb1477e3afd` | true | full |
| `binance_usdm_ethusdt_4h__v001` | `3451959278e786fc44ebd41529cc1e83c999070d175e93e145e569eb815cdd79` | true | full |
| `binance_usdm_ethusdt_metrics__v001` | `deabe463e98ea4ffeedf525c53fce8a3629c9147ee4ac84e03a80f51db8be2be` | false | oi_subset_only_per_phase_4j_§11 |
| `binance_usdm_ethusdt_funding__v002` | `035125d88f75adc451f5ea799e2c6484a5deb9bdcfbecb749efa4b0ffd88dd11` | (v002 lock) | full |

No mark-price 30m / 4h / 5m / 15m, no aggTrades, no spot data, no
cross-venue data, no optional ratio columns accessed.

## Local result artefacts

22 CSV tables under `data/research/phase4l/tables/` (gitignored;
reproducible from `scripts/phase4l_v2_backtest.py` with RNG seed
202604300):

- run metadata + verdict;
- manifest references with SHA pinning;
- 512-variant parameter grid;
- chronological window boundaries;
- per-variant trade summaries (BTC + ETH × train/validation/OOS,
  MEDIUM-slip);
- BTC-train-best variant identification;
- BTC-train-best cost-cell sensitivity;
- M1 / M2 / M3 mechanism-check results;
- cost sensitivity (per-variant per-cost-cell);
- PBO summary;
- deflated Sharpe summary (per variant);
- metrics OI exclusion counts (per symbol);
- main-cell vs. exclude-entire-affected-days sensitivity;
- trade distribution by month (empty);
- verdict declaration;
- catastrophic-floor predicate results (12 predicates);
- forbidden-work confirmation (runtime introspection).

## Metrics OI exclusion summary

| Symbol | Total 30m bars | OI-feature-eligible | Missing/invalid | Prev-window missing | Excluded fraction |
|---|---|---|---|---|---|
| BTCUSDT | 74 448 | 74 415 | 30 | 3 | 0.044% |
| ETHUSDT | 74 448 | 74 415 | 30 | 3 | 0.044% |

Phase 4j §11 per-bar exclusion rule honored exactly per Phase 4j §16
pseudocode. No forward-fill. No interpolation. No imputation. No
synthetic OI data. No silent omission.

Sensitivity comparison (main cell vs. exclude-entire-affected-days):
both cells produce 0-trade outputs because the underlying simulation
produces 0 trades; sensitivity comparison is methodologically inert
under V2 first-spec. CFP-8 not triggered.

## Optional ratio-column non-access verification

**Static scan result:**

```text
Forbidden ratio names in script: []
Pass: True
```

**Metrics-loader verification:** the metrics loader uses an explicit
`METRICS_OI_COLUMNS = ["create_time", "symbol", "sum_open_interest",
"sum_open_interest_value"]` parameter to pyarrow's `read(columns=...)`.
The four optional ratio columns are NOT in this list and are NEVER
loaded into memory.

**Runtime introspection** (recorded in
`forbidden_work_confirmation.csv`):

| check | result |
|---|---|
| optional_ratio_column_access | 0 |
| per_bar_exclusion_algorithm | matches_phase_4j_section_16 |
| forbidden_data_access | 0 |
| network_io | 0 |
| authenticated_api_access | 0 |
| credential_request | 0 |
| mark_price_30m_4h_acquisition | 0 |
| aggtrades_acquisition | 0 |
| spot_data_acquisition | 0 |
| v003_creation | 0 |

## BTCUSDT primary result summary

- All 512 variants × 3 cost cells × 3 windows = 4 608 result cells
  with `trade_count = 0`, `mean_R = 0`, `total_R = 0`, `sharpe = 0`,
  `profit_factor = 0`.
- BTC-train-best variant: variant_id = 0 (lexicographic tiebreaker
  over identical 0-Sharpe). Label: `N1=20|Pw=25|Vrel=1.5|Vz=0.5|
  Timb=0.55|OI=aligned|FB=20-80|NR=2.0|Tstop=12`. Train Sharpe = 0;
  DSR = 0; validation Sharpe = 0; OOS Sharpe = 0.
- §11.6 HIGH cost-sensitivity (BTC OOS, BTC-train-best variant):
  mean_R = 0; total_R = 0; sharpe = 0; profit_factor = 0; passes_CFP-2
  = true (mean_R not negative).

## ETHUSDT comparison result summary

Identical structural pattern: all 512 variants × 3 cost cells × 3
windows = 4 608 result cells with `trade_count = 0`. ETHUSDT does
NOT rescue BTCUSDT; cross-symbol consistency is trivially: both
symbols fail at the same structural design boundary.

## M1 / M2 / M3 summary

| Symbol | M1 (≥50% reach +0.5R MFE) | M2 (≥+0.10R uplift, bootstrap-CI lo > 0) | M3 (≥+0.05R uplift, HIGH non-degraded) |
|---|---|---|---|
| BTCUSDT | false (0 trades; not evaluable) | false (0 trades both cells) | false (0 trades both cells) |
| ETHUSDT | false (0 trades; not evaluable) | false (0 trades both cells) | false (0 trades both cells) |

M1 / M2 / M3 are all "false" trivially because the underlying trade
populations are empty. The verdict reason field correctly attributes
the failure to CFP-1 critical, not to M1 / M2 / M3 mechanism failure.

## PBO / DSR / CSCV summary

- **PBO (train internal CSCV, S = 16):** 0.500. CFP-6 threshold > 0.5
  not crossed. The 0.5 PBO is the trivial "no signal" reading
  expected when all 512 variants have identical 0-trade behavior.
- **CSCV combinations evaluated:** 12 870 (= C(16, 8); Phase 4k
  predeclared exact computation honored).
- **Bootstrap iterations for M2 / M3:** B = 10 000 per Phase 4k
  default.
- **Deflated Sharpe:** all 512 variants have DSR = 0 < DSR_significance_z
  (1.96). No variant survives DSR significance. CFP-1 critical /
  0-trade root cause.

## Cost sensitivity summary

| Cost cell | Slippage per side | Round-trip | BTC OOS BTC-train-best mean_R |
|---|---|---|---|
| LOW | 1 bp | 10 bps | 0.0 |
| MEDIUM | 4 bps | 16 bps | 0.0 |
| **HIGH (§11.6)** | **8 bps** | **24 bps** | **0.0** |

§11.6 HIGH preserved verbatim. No relaxation. No maker-rebate. No
live-fee assumption. Funding cost included in realized_R (zero in
this run because no trades).

## Catastrophic-floor predicate summary

| Predicate | Triggered | Detail |
|---|---|---|
| **CFP-1** | **TRUE** | **512/512 variants with <30 OOS trades** |
| CFP-2 | false | BTC OOS HIGH mean_R=0.0000 (not < 0) |
| CFP-3 | true | max_dd_R=0.0000, PF=0.0000 (PF<0.5 mechanically; subordinate to CFP-1) |
| CFP-4 | false | BTC pass=False, ETH pass=False (CFP-4 requires BTC fail AND ETH pass) |
| CFP-5 | false | train_sharpe=0.0000, oos_sharpe=0.0000 (CFP-5 requires train>1.0 AND OOS<0.0) |
| CFP-6 | false | PBO=0.5000 (boundary; not strictly > 0.5) |
| CFP-7 | false | max month_fraction over 0.5 — N/A (no trades) |
| CFP-8 | false | main_R=0.0000, sensitivity_R=0.0000 |
| CFP-9 | false | excluded_fraction=0.0004 (well under 5%) |
| CFP-10 | false | no optional ratio-column access detected |
| CFP-11 | false | per-bar exclusion algorithm matches Phase 4j §16 |
| CFP-12 | false | no forbidden data access detected |

CFP-1 critical is the binding verdict driver. CFP-3's "PF<0.5"
trigger is mechanically true under empty arrays but methodologically
subordinate to CFP-1 (which is the diagnostic root cause).

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4l/v2-backtest-execution
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check scripts/phase4l_v2_backtest.py
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m mypy
.venv/Scripts/python -m pytest -q
# Optional ratio static scan (zero forbidden names confirmed)
.venv/Scripts/python -c "
forbidden = ['count_toptrader_long_short_ratio',
'sum_toptrader_long_short_ratio',
'count_long_short_ratio',
'sum_taker_long_short_vol_ratio']
src = open('scripts/phase4l_v2_backtest.py', encoding='utf-8').read()
hits = [n for n in forbidden if n in src]
print('Forbidden ratio names in script:', hits)
print('Pass:', len(hits) == 0)"
.venv/Scripts/python scripts/phase4l_v2_backtest.py \
  --start 2022-01-01 --end 2026-03-31 \
  --train-start 2022-01-01 --train-end 2023-06-30 \
  --validation-start 2023-07-01 --validation-end 2024-06-30 \
  --oos-start 2024-07-01 --oos-end 2026-03-31 \
  --symbols BTCUSDT ETHUSDT \
  --primary-symbol BTCUSDT --comparison-symbol ETHUSDT \
  --output-dir data/research/phase4l \
  --rng-seed 202604300
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
git add scripts/phase4l_v2_backtest.py docs/.../2026-04-30_phase-4l_v2-backtest-execution.md
git commit -m "phase-4l: V2 backtest execution (docs-and-code)"
git push -u origin phase-4l/v2-backtest-execution
git add docs/.../2026-04-30_phase-4l_closeout.md
git commit -m "phase-4l: closeout report"
git push origin phase-4l/v2-backtest-execution
```

The following commands were **NOT** run (per Phase 4l brief
prohibitions):

- No `scripts/phase3q_5m_acquisition.py` execution.
- No `scripts/phase3s_5m_diagnostics.py` execution.
- No `scripts/phase4i_v2_acquisition.py` execution.
- No data acquisition / download / patch / regeneration.
- No mark-price 30m / 4h acquisition.
- No `aggTrades` acquisition.
- No private / authenticated REST or WebSocket request.
- No git push to main. No merge to main.

## Verification results

| Check | Result |
|---|---|
| `python --version` | `Python 3.12.4` |
| `ruff check .` (whole repo) | `All checks passed!` |
| `pytest` | `785 passed in 14.73s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |
| Optional ratio name static scan | `[]; Pass: True` |
| Phase 4l backtest exit code | `0` |
| Per-bar exclusion algorithm verification | matches Phase 4j §16 |

Whole-repo quality gates remain **fully clean** at Phase 4l final.

## Commit

```text
Phase 4l backtest+report commit:  f795d3f3387a1ea48e8ff2d226f752ea3b7bf76a
```

The closeout commit SHA will be recorded after this file is committed.

## Final git status

To be appended after closeout commit and push.

## Final git log --oneline -5

To be appended after closeout commit and push.

## Final rev-parse

To be appended after closeout commit and push.

## Branch / main status

Phase 4l is on branch `phase-4l/v2-backtest-execution`. The branch
is pushed to `origin/phase-4l/v2-backtest-execution`. **Phase 4l is
NOT merged to main.** main remains at
`b9d30151524508e3fb258e7a92e413171969150b` (post-Phase-4k-merge
housekeeping commit).

Merge to main is not part of Phase 4l. A separate operator decision
("We are closing out Phase 4l by merging it into main") is required
to merge the branch.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4m / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched,
  or commenced.
- **No V2 implementation under `src/prometheus/strategy/`.** Existing
  `prometheus.strategy` modules untouched.
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No existing `scripts/**` modification.** Phase 4l adds only
  `scripts/phase4l_v2_backtest.py` (standalone).
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No `.claude/rules/**` modification.**
- **No data acquired.** No public Binance endpoint consulted in code.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage.
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** Phase 4l performs no network I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
- **No strategy rescue proposal.** V2 is a new ex-ante hypothesis;
  Verdict C is terminal for V2 first-spec.
- **No 5m strategy / hybrid / retained-evidence successor / new
  variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No `scripts/phase4i_v2_acquisition.py` execution.**
- **No data acquisition / download / patch / regeneration /
  modification.** No `data/raw/` or `data/normalized/` modification.
- **No data manifest modification.** All
  `data/manifests/*.manifest.json` preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No Phase 4i manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4j §11 metrics OI-subset governance modification.**
- **No Phase 4f / 4g / 4h / 4i / 4j / 4k text modification.**
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
  Phase 4l branch.** Per Phase 4l brief.
- **No optional ratio-column access.** Static scan + runtime
  introspection: 0.
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused**. Phase 4l deliverables exist as
  branch-only artefacts pending operator review.
- **Phase 4l output:** docs-and-code branch artefacts (one
  standalone backtest script + this Markdown closeout + the Phase
  4l V2 backtest execution report).
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified at Phase 4l final).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4k all merged. Phase
  4l V2 backtest execution on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 +
  enforced in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 +
  enforced in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Metrics OI-subset partial-eligibility governance:** Phase 4j §11
  (preserved verbatim; honored exactly by Phase 4l).
- **V2 backtest methodology governance:** Phase 4k (preserved
  verbatim; honored exactly by Phase 4l).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j)
  + backtest-plan binding (Phase 4k) + executed (Phase 4l, this
  phase) → **Verdict C HARD REJECT, terminal for V2 first-spec**.
  V2 retained as research evidence only; non-leading; no V2 rescue
  authorized.
- **OPEN ambiguity-log items after Phase 4l:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  **V2 HARD REJECT (Phase 4l, structural CFP-1 critical)**;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:** `phase-4l/v2-backtest-execution` exists locally
  and on `origin/phase-4l/v2-backtest-execution`. **NOT merged to
  main.**

## Next authorization status

**No next phase has been authorized.** Phase 4l's recommendation is
**Option A (remain paused) as primary**, with **Option B (docs-only
post-V2 research consolidation memo, analogous to Phase 3e / Phase
3k) as conditional secondary**.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.
