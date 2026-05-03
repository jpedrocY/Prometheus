# Phase 4l — V2 Backtest Execution

**Authority:** Operator authorization for Phase 4l (Phase 4k §"Operator
decision menu" Option B primary recommendation: Phase 4l V2 Backtest
Execution, docs-and-code, under the Phase 4k V2 Backtest-Plan Memo
methodology); Phase 4k (V2 Backtest-Plan Memo; binding methodology);
Phase 4j §11 (metrics OI-subset partial-eligibility binding rule);
Phase 4i (V2 public data acquisition + integrity validation; partial
pass); Phase 4h (V2 data requirements / feasibility); Phase 4g (V2
strategy-spec memo); Phase 4f §22 (V2 hypothesis); Phase 3v §8
(stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even /
EMA slope / stagnation governance); Phase 3r §8 (mark-price gap
governance); Phase 3p §4.7 (strict integrity gate semantics); Phase
2i §1.7.3 (project-level locks); Phase 2p §C.1 (R3 baseline-of-record);
Phase 2w §16.1 (R2 §11.6 cost-sensitivity FAIL pattern); Phase 3c
§7.3 (catastrophic-floor predicate);
`docs/03-strategy-research/v1-breakout-strategy-spec.md`;
`docs/05-backtesting-validation/v1-breakout-validation-checklist.md`;
`docs/04-data/data-requirements.md`;
`docs/04-data/timestamp-policy.md`;
`docs/04-data/dataset-versioning.md`;
`docs/07-risk/stop-loss-policy.md`;
`docs/07-risk/position-sizing-framework.md`;
`docs/07-risk/exposure-limits.md`;
`docs/12-roadmap/phase-gates.md`;
`docs/12-roadmap/technical-debt-register.md`;
`.claude/rules/prometheus-core.md`;
`.claude/rules/prometheus-safety.md`;
`.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4l — **V2 Backtest Execution** (docs-and-code).
Implements and runs the Phase 4k predeclared V2 backtest methodology
exactly. **Phase 4l does NOT implement V2 inside `src/prometheus/`.
Phase 4l does NOT modify runtime / execution / persistence / risk /
exchange code. Phase 4l does NOT modify tests. Phase 4l does NOT
modify data, manifests, or scripts beyond the new
`scripts/phase4l_v2_backtest.py`. Phase 4l does NOT acquire or
download data. Phase 4l does NOT use network I/O. Phase 4l does NOT
use credentials. Phase 4l does NOT contact Binance APIs. Phase 4l
does NOT create paper / shadow / live runtime. Phase 4l does NOT
imply live-readiness. Phase 4l does NOT authorize Phase 4m or any
successor phase.**

**Branch:** `phase-4l/v2-backtest-execution`. **Memo date:** 2026-05-02
UTC.

---

## Summary

Phase 4l implemented the standalone V2 backtest script
`scripts/phase4l_v2_backtest.py` per Phase 4k methodology and ran
the full 512-variant grid across BTCUSDT (primary) and ETHUSDT
(comparison) on the predeclared train / validation / OOS holdout
windows under three cost cells (LOW = 1 bp, MEDIUM = 4 bps, HIGH =
8 bps slippage per side; HIGH = §11.6 gate preserved verbatim).

**Final verdict: C — V2 framework HARD REJECT.**

**Catastrophic-floor predicate triggered:**

- **CFP-1 critical:** **512 / 512 variants** produced fewer than the
  CFP-1 threshold of 30 OOS trades on BTCUSDT. The BTC-train-best
  variant (variant_id = 0) produced **0 OOS trades** at MEDIUM-slip
  cost cell. M1 / M2 / M3 mechanism checks are NOT meaningfully
  evaluable.

**Root cause analysis (forensic):** Phase 4l's standalone
implementation matches the Phase 4k methodology exactly. The 8-feature
AND chain (HTF bias + Donchian breakout + Donchian width compression
+ ATR regime band + range-expansion + relative volume + volume z-score
+ UTC-hour participation + taker imbalance + OI delta direction +
funding-rate band) yields ~15-30 raw setup candidates per variant per
symbol over the 4-year coverage. **All such candidates are
subsequently rejected by the V1-inherited stop-distance filter
(0.60 × ATR(20) ≤ stop_distance ≤ 1.80 × ATR(20)).** With V2's locked
20-bar or 40-bar Donchian setup window per Phase 4g §29 axis 1, the
setup_low — defined per Phase 4g §19 as "the lowest low of the
previous N1 30m bars" — typically sits 3-5 × ATR(20) below the
breakout-bar close, which exceeds the 1.80 × ATR upper bound. The
result is a **structural incompatibility** between V2's longer
Donchian setup and the V1-inherited stop-distance bounds (originally
calibrated for V1's much shorter 8-bar setup window). This is
analogous to the F1 catastrophic-floor pattern documented in Phase
3c §7.3 (Phase 3d-B2 terminal): the strategy spec, as predeclared,
fails at the design stage, before any data-dependent evaluation can
occur.

**M1 / M2 / M3 not evaluable.** With 0 OOS trades on the
BTC-train-best variant, fraction-reaching-+0.5R-MFE (M1),
participation-relaxed differential (M2), and derivatives-relaxed
differential (M3) cannot be computed meaningfully. The Phase 4l
script reports M1 / M2 / M3 = FAIL trivially (0/0 fraction defaults
to 0.0 < 0.50 threshold) but the underlying cause is CFP-1 critical,
not an organic mechanism failure. Phase 4l's verdict logic
correctly prioritizes CFP-1 critical over M1 FAIL: Phase 4l reports
the verdict as **CFP-1 critical** rather than as "M1 FAIL" in
order not to misattribute the failure mode.

**Phase 4j §11 metrics OI-subset partial-eligibility rule was
honored exactly.** Per-bar exclusion algorithm matches Phase 4j §16
pseudocode verbatim. Empirical exclusion fraction on BTCUSDT:
**0.044%** (33 bars excluded out of 74 448 30m bars; 30 due to
missing-or-invalid OI subset, 3 due to previous-window OI missing).
Empirical exclusion fraction on ETHUSDT: **0.044%** (identical
33-bar pattern). Both well under the CFP-9 5% threshold. The
Phase 4j §11 governance rule is functionally non-restrictive on the
acquired Phase 4i data — the V2 verdict is not driven by metrics
exclusions.

**Optional ratio-column non-access enforcement: PASSED.** Static
scan of `scripts/phase4l_v2_backtest.py` confirms zero occurrences
of any of the four forbidden ratio column name strings
(`count_toptrader_long_short_ratio`,
`sum_toptrader_long_short_ratio`, `count_long_short_ratio`,
`sum_taker_long_short_vol_ratio`). The metrics loader in
`load_metrics_oi_subset()` uses an explicit
`METRICS_OI_COLUMNS = ["create_time", "symbol", "sum_open_interest",
"sum_open_interest_value"]` parameter to pyarrow's `read(columns=...)`
— the four optional columns are not loaded into memory at any point.
Runtime introspection: optional ratio-column access count = 0; no
optional ratio-column diagnostics computed.

**Forbidden-input non-access: CONFIRMED.** No mark-price 30m / 4h /
5m / 15m klines accessed. No aggTrades accessed. No spot data. No
cross-venue data. No authenticated REST / private endpoint / public
endpoint in code / user stream / WebSocket / listenKey lifecycle. No
credentials. No network I/O of any kind during Phase 4l execution.
No write to `data/raw/`, `data/normalized/`, or `data/manifests/`.

**No retained verdict revised.** R3 baseline-of-record; H0 framework
anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence
only — all preserved verbatim.

**No project lock changed.** §1.7.3 / §11.6 / mark-price stops / v002
verdict provenance — all preserved verbatim. **Phase 4j §11 metrics
OI-subset rule: not modified.** **Phase 4g V2 strategy spec: not
modified.** **Phase 4k methodology: not modified.**

**No V2 implementation.** Phase 4l added only one new file under
`scripts/` (the standalone backtest orchestrator) plus this Markdown
report and the Phase 4l closeout. No `src/prometheus/strategy/` /
`src/prometheus/runtime/` / `src/prometheus/execution/` /
`src/prometheus/persistence/` / `src/prometheus/risk/` modification.

**Verification (run on the post-Phase-4k-merge tree):**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**Recommended next phase:** **Remain paused** as primary. The Phase
4l Verdict C HARD REJECT pattern is terminal for the V2 first-spec
under Phase 4g §29 locked threshold grid + V1-inherited stop-distance
filter (0.60-1.80 × ATR). Any future research direction must be
authorized as a separate operator decision and must satisfy the
Phase 3t §12 validity gate (genuinely new ex-ante hypothesis; not
derived from Phase 4l observed patterns; full written specification
before any data is touched).

V2 remains **pre-research only**: not implemented; not backtested
(in any sense useful for promotion); not validated; not live-ready;
**not a rescue** of R3 / R2 / F1 / D1-A.

**No V2 implementation authorized.** **No paper / shadow / live /
exchange-write authorized.** **No successor phase started.**

---

## Authority and boundary

Phase 4l operates strictly inside the post-Phase-4k-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10;
  Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t
  consolidation; Phase 3u §10 / §11; Phase 3v §8 (stop-trigger-domain
  governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope /
  stagnation governance); Phase 4a–4d boundary; Phase 4e
  reconciliation-model design memo; Phase 4f V2 hypothesis
  predeclaration; Phase 4g V2 strategy spec; Phase 4h V2
  data-requirements / feasibility memo; Phase 4i V2 acquisition +
  integrity validation; Phase 4j §11 metrics OI-subset
  partial-eligibility rule; **Phase 4k V2 Backtest-Plan Memo
  methodology (binding from Phase 4k merge forward; Phase 4l honors
  it exactly).**
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md`
  unchanged.
- **Project-level locks preserved verbatim.** §1.7.3.
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 /
  §11.4 / §11.6 (= 8 bps HIGH per side).
- **Retained-evidence verdicts preserved verbatim.** R3 / H0 / R1a /
  R1b-narrow / R2 / F1 / D1-A.
- **Safety rules preserved verbatim.**
- **MCP and secrets rules preserved verbatim.**
- **Phase 4g V2 strategy-spec selections preserved verbatim.** No
  modification to Phase 4g §28 active feature set, §11 timeframe
  matrix, §29 threshold grid, §30 M1 / M2 / M3 decomposition, or
  §22–§24 governance labels.
- **Phase 4i manifests preserved verbatim.** All six Phase 4i
  manifests unchanged. The two metrics manifests retain
  `research_eligible: false`.
- **Phase 4j §11 binding rule preserved verbatim.** Phase 4l honors
  the per-bar exclusion algorithm exactly per Phase 4j §16
  pseudocode.

Phase 4l adds *only* the standalone research script + this report +
the closeout artefact, without modifying any prior phase memo, any
data, any code under `src/prometheus/`, any rule, any threshold, any
manifest, any verdict, any lock, or any gate.

---

## Starting state

```text
branch:           phase-4l/v2-backtest-execution
parent commit:    b9d30151524508e3fb258e7a92e413171969150b (post-Phase-4k-merge housekeeping)
working tree:     clean before script authoring
main:             b9d30151524508e3fb258e7a92e413171969150b (unchanged)

Phase 4a foundation:                                          merged.
Phase 4b/4c cleanup:                                          merged.
Phase 4d review:                                              merged.
Phase 4e reconciliation-model design memo:                    merged.
Phase 4f V2 hypothesis predeclaration:                        merged.
Phase 4g V2 strategy spec:                                    merged.
Phase 4h V2 data-requirements / feasibility memo:             merged.
Phase 4i V2 public data acquisition + integrity:              merged (partial-pass; metrics not eligible).
Phase 4j V2 metrics data governance memo:                     merged (Phase 4j §11 binding).
Phase 4k V2 backtest-plan memo:                               merged.

Repository quality gate:           fully clean (verified at Phase 4l startup).
research thread (5m):              operationally complete and closed (Phase 3t).
v002 datasets:                     locked; manifests untouched.
v001-of-5m datasets:               trade-price research-eligible; mark-price research_eligible:false (Phase 3r §8 governs).
Phase 4i datasets:                 30m + 4h klines × 2 research-eligible; metrics × 2 NOT research-eligible (Phase 4j §11 governs feature-level OI-subset use).
```

---

## Relationship to Phase 4k

Phase 4k authored the V2 backtest-plan methodology before any V2
backtest existed. Phase 4l implements that methodology exactly:

| Phase 4k specification | Phase 4l implementation |
|---|---|
| 4 research-eligible kline datasets + 2 metrics OI subset + v002 funding | `load_kline_symbol_interval()`, `load_metrics_oi_subset()`, `load_funding()` |
| 8 active entry features + 3 exit / regime features (Phase 4g §28) | `compute_symbol_features()` + `compute_signals()` |
| Phase 4j §11 per-bar OI exclusion algorithm verbatim | `compute_oi_eligibility_and_delta()` |
| OI delta = OI(bar_open + 25min) − OI(bar_open − 5min) per Phase 4j §17 | `compute_oi_eligibility_and_delta()` lines 524–532 |
| 512-variant grid (9 binary axes) | `build_variants()` produces exactly 512 variants in deterministic lexicographic order |
| Train (2022-01-01..2023-06-30 UTC) / val (2023-07-01..2024-06-30 UTC) / OOS (2024-07-01..2026-03-31 UTC) | argparse defaults exactly match |
| BTCUSDT primary; ETHUSDT comparison only | Independent per-symbol simulation; no cross-symbol selection |
| §11.6 = 8 bps HIGH per side | `COST_CELL_HIGH_SLIP_BPS = 8.0` |
| 0.25% risk + 2× leverage cap | `LOCKED_RISK_FRACTION = 0.0025`, `LOCKED_LEVERAGE_CAP = 2.0` |
| Stop-distance filter 0.60-1.80 × ATR(20) | `STOP_DIST_MIN_ATR = 0.60`, `STOP_DIST_MAX_ATR = 1.80` |
| Conservative tie-break: stop wins | Implemented in `simulate_trades()` |
| Fixed-R take-profit `N_R ∈ {2.0, 2.5}` | Variant axis 8 |
| Time-stop `T_stop ∈ {12, 16}` 30m bars | Variant axis 9 |
| Cooldown `C = 8` bars (fixed) | `COOLDOWN_BARS = 8` |
| M1: ≥ 50% trades reach +0.5R MFE on BOTH symbols | Computed on OOS, MEDIUM-slip |
| M2: full V2 vs participation-relaxed; ≥ +0.10R; bootstrap-by-trade B = 10000 95% CI | `compute_signals(relax_participation=True)` + `bootstrap_diff_mean_ci()` |
| M3: full V2 vs derivatives-relaxed; ≥ +0.05R; HIGH-resilience non-degraded ε = 0.05R | `compute_signals(relax_derivatives=True)` |
| Deflated Sharpe per Bailey & López de Prado (2014) | `deflated_sharpe_ratio()` |
| PBO with CSCV S = 16 chronologically-respecting sub-samples | `cscv_pbo()` |
| 12 catastrophic-floor predicates (CFP-1..CFP-12) | All evaluated |
| Verdict A / B / C / D classification | `verdict` and `verdict_reason` derivation |
| Manifest SHA256 pinning | Computed via `sha256_of_file()` |
| Pinned RNG seed 202604300 | argparse default |
| Standalone-script pattern; no `prometheus.runtime/execution/persistence` imports; no network I/O | Verified |

Phase 4l does NOT modify Phase 4k text. Phase 4l does NOT amend the
Phase 4k methodology.

---

## Methodology adherence statement

Phase 4l's standalone implementation matches the Phase 4k methodology
exactly. The single area where the implementation makes a binding
choice that Phase 4k either left as a configurable preference or
explicitly recommended is recorded below:

- **Threshold-grid handling: Option B (full PBO / DSR / CSCV with
  512 variants reported, no further reduction).** This is the Phase
  4k §"Threshold-grid handling" primary recommendation, honored
  exactly: the 512-variant grid is iterated in deterministic
  lexicographic order; no early exit on bad variants; all 512
  variants reported.
- **Stop-distance filter check at signal time:** computed using
  `close[i]` (signal-completed bar's close) as a proxy for the
  next-bar entry price. This matches V1 / R3 backtest convention.
  The actual entry price at `open[i+1]` is used for trade simulation
  and realized R computation.
- **Same-bar stop / take-profit ambiguity resolution:** conservative
  tie-break (stop wins), per Phase 4k §"Exit model implementation
  plan / Same-bar exit ambiguity tie-breakers".
- **OI delta computation rule:** Phase 4j §17 binding rule applied
  verbatim — current OI is the metrics record at
  `bar_open_time + 25 minutes`; previous-window OI is the metrics
  record at `bar_open_time − 5 minutes`; OI delta = current − previous.
  This rule supersedes the Phase 4g §17 N_oi-trailing rule for V2's
  first backtest, as predeclared by Phase 4j §17 / §11.4.
- **Plot artefacts: NOT generated.** The Phase 4l venv does not
  include `matplotlib` (the project `pyproject.toml` declares only
  `pyarrow`, `duckdb`, `pydantic`, `httpx`, `numpy`); installing it
  is outside Phase 4l scope. Per Phase 4l brief: "If any table or
  plot cannot be produced, the report must explicitly state why and
  whether this triggers Verdict D / INCOMPLETE." This omission does
  NOT trigger Verdict D — the underlying CSV tables that would back
  the plots are produced (cumulative R, drawdown, exclusion
  timeseries, etc.). The Phase 4k stop conditions list
  "validation report incomplete" only when required tables are
  missing; plots are diagnostic-only artefacts. **Verdict driver is
  CFP-1 critical, not plot absence.**

---

## Data inputs and manifest SHA pinning

| Dataset | Manifest path | Manifest SHA256 | research_eligible | feature_use |
|---|---|---|---|---|
| `binance_usdm_btcusdt_30m__v001` | `data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json` | `3cdf6fb91ffca8acc2a69ae05a00745a031360c01c585a75f876c64d42230da8` | true | full |
| `binance_usdm_btcusdt_4h__v001` | `data/manifests/binance_usdm_btcusdt_4h__v001.manifest.json` | `b2413e7fbbacfa091f2f42af8220ee83b55ee2511ee2b7be070e936c5761180a` | true | full |
| `binance_usdm_btcusdt_metrics__v001` | `data/manifests/binance_usdm_btcusdt_metrics__v001.manifest.json` | `41d6a8e45a1f992ce813838640c28534dcd1885b4482d01d4ded7809a208baf7` | false | oi_subset_only_per_phase_4j_§11 |
| `binance_usdm_btcusdt_funding__v002` | `data/manifests/binance_usdm_btcusdt_funding__v002.manifest.json` | `da719007f9358d45b38792e50fa16ed0e470c0d983345651e6efae9349706007` | false | full |
| `binance_usdm_ethusdt_30m__v001` | `data/manifests/binance_usdm_ethusdt_30m__v001.manifest.json` | `0a7502c5e09916529e50951bd503e1a2ac95d372e99ba65f4cb3bfb1477e3afd` | true | full |
| `binance_usdm_ethusdt_4h__v001` | `data/manifests/binance_usdm_ethusdt_4h__v001.manifest.json` | `3451959278e786fc44ebd41529cc1e83c999070d175e93e145e569eb815cdd79` | true | full |
| `binance_usdm_ethusdt_metrics__v001` | `data/manifests/binance_usdm_ethusdt_metrics__v001.manifest.json` | `deabe463e98ea4ffeedf525c53fce8a3629c9147ee4ac84e03a80f51db8be2be` | false | oi_subset_only_per_phase_4j_§11 |
| `binance_usdm_ethusdt_funding__v002` | `data/manifests/binance_usdm_ethusdt_funding__v002.manifest.json` | `035125d88f75adc451f5ea799e2c6484a5deb9bdcfbecb749efa4b0ffd88dd11` | false | full |

(Note on funding `research_eligible: false`: the v002 funding family
manifests carry `research_eligible: false` per the historical v002
funding integrity-check decision recorded at v002 lock; Phase 4l
reuses the funding manifests as-is, consistent with Phase 4h §22 /
Phase 4k methodology. Funding-rate is used only for the percentile
band feature, not as a primary research-promotability gate.)

All eight manifests existed at Phase 4l execution start. No manifest
was modified by Phase 4l. SHA256 hashes pinned in
`data/research/phase4l/tables/manifest_references.csv`.

---

## Script implementation summary

`scripts/phase4l_v2_backtest.py` is a standalone research script
(~2 700 lines including comments) implementing the Phase 4k
methodology. Key design choices:

- **Pure stdlib + pyarrow + numpy.** The project venv ships
  `pyarrow`, `duckdb`, `pydantic`, `httpx`, `numpy`, plus dev
  tools. Phase 4l uses pyarrow for parquet reads and numpy for all
  arithmetic. **No pandas. No scipy. No matplotlib. No httpx
  imported (no network I/O possible from this script).** No
  `prometheus.runtime/execution/persistence/risk/exchange` imports.
- **Forbidden imports verified:** `from __future__`,
  `argparse`, `dataclasses`, `hashlib`, `itertools`, `json`,
  `math`, `sys`, `collections.abc`, `dataclasses`, `datetime`,
  `pathlib`, `typing`, `numpy`, `pyarrow.parquet`. Nothing else.
- **Deterministic execution.** Variants iterated in lexicographic
  order; numpy RNG seed 202604300 pinned; CSCV combinations
  generated deterministically via `itertools.combinations`.
- **Fail-closed design.** Custom `StopCondition` exception is
  raised on any required-manifest-missing, local-data-missing,
  manifest-research-eligible-mismatch, etc. condition. The script
  exits with code 2 on stop conditions; exit code 0 only after
  successful run.
- **Pure-function feature pipeline.** EMA, ATR, true range, Donchian
  high/low, rolling mean / std / percentile rank are all pure-numpy
  no-side-effect functions.
- **Vectorized per-bar simulation.** `simulate_trades()` iterates
  bar-by-bar but holds at most one position per (symbol, variant,
  cost_cell). Stop-precedence is conservative-tie-break (stop wins
  on same-bar stop+TP touch). Funding cost is included via
  `funding_cost_R_long()` / `funding_cost_R_short()` summing all
  funding events whose `funding_time` falls in `(entry_ms, exit_ms]`.
- **Static-scan-clean.** No string occurrence of any of the four
  forbidden optional ratio column names anywhere in the script.

---

## Forbidden input verification

- **Mark-price 30m / 4h klines:** NOT ACCESSED. Script does not load
  `data/normalized/mark_price_klines/` or
  `data/manifests/binance_usdm_*_markprice_*` files.
- **Mark-price 5m, 15m:** NOT ACCESSED.
- **aggTrades:** NOT ACCESSED.
- **Spot data, cross-venue data:** NOT ACCESSED.
- **Authenticated REST / private endpoints / public endpoint clients
  in code / user stream / WebSocket / listenKey lifecycle:** NONE.
  Script imports only pyarrow + stdlib + numpy. No `httpx` / `aiohttp`
  / `requests` / `websockets` / `binance` SDK imports. No URL string
  literals other than the data.binance.vision entries documented in
  `scripts/phase4i_v2_acquisition.py` (which is a different script
  and was NOT executed by Phase 4l).
- **Credentials:** NONE. No `.env` read. No `os.environ` access for
  credentials. No keyring/store access.
- **v003 dataset creation:** NONE.
- **Network I/O:** NONE. No `socket`, `urllib`, `http.client`,
  `httpx`, etc. imports. The script's `main()` function executes
  entirely against local Parquet files.

---

## Optional ratio-column non-access verification

**Static scan result:** zero occurrences of any of the four
forbidden ratio column name strings inside
`scripts/phase4l_v2_backtest.py`:

```text
$ python -c "
forbidden = [
    'count_toptrader_long_short_ratio',
    'sum_toptrader_long_short_ratio',
    'count_long_short_ratio',
    'sum_taker_long_short_vol_ratio',
]
src = open('scripts/phase4l_v2_backtest.py', encoding='utf-8').read()
hits = [n for n in forbidden if n in src]
print('Forbidden ratio names in script:', hits)
print('Pass:', len(hits) == 0)"
Forbidden ratio names in script: []
Pass: True
```

**Metrics-loader verification:** `load_metrics_oi_subset()` calls
`pq.ParquetFile(p).read(columns=METRICS_OI_COLUMNS)` where
`METRICS_OI_COLUMNS = ["create_time", "symbol", "sum_open_interest",
"sum_open_interest_value"]`. The four optional columns are NOT in
this list and are NEVER loaded into memory.

**Runtime-introspection verification (recorded in
`data/research/phase4l/tables/forbidden_work_confirmation.csv`):**

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

**No optional ratio-column diagnostic computed.** No filter, label,
sensitivity, or feature derived from optional ratio columns.

---

## Metrics OI exclusion results

| Symbol | Total 30m bars | OI-feature-eligible | Missing/invalid (CauseA) | Prev-window missing | Excluded fraction |
|---|---|---|---|---|---|
| BTCUSDT | 74 448 | 74 415 | 30 | 3 | **0.0443%** |
| ETHUSDT | 74 448 | 74 415 | 30 | 3 | **0.0443%** |

Both symbols show identical 33-bar exclusion patterns (30 missing/invalid
+ 3 prev-window-missing), consistent with the Phase 4i metrics
upstream pattern. The exclusion fraction (~0.04%) is well below the
CFP-9 5% threshold. **CFP-9 not triggered.**

**Sensitivity comparison (main cell vs. exclude-entire-affected-days):**

| scope | trade_count | mean_R |
|---|---|---|
| main_btc_oos_medium | 0 | 0 |
| sensitivity_btc_oos_medium | 0 | 0 |

Both cells produce identical (0-trade) outputs because the
underlying simulation produces no trades on any variant; the
sensitivity comparison is therefore methodologically inert under
the V2 first-spec. **CFP-8 not triggered.**

---

## Backtest configuration

```text
Run command (Windows path-separator preserved):

.venv/Scripts/python scripts/phase4l_v2_backtest.py \
  --start 2022-01-01 \
  --end 2026-03-31 \
  --train-start 2022-01-01 \
  --train-end 2023-06-30 \
  --validation-start 2023-07-01 \
  --validation-end 2024-06-30 \
  --oos-start 2024-07-01 \
  --oos-end 2026-03-31 \
  --symbols BTCUSDT ETHUSDT \
  --primary-symbol BTCUSDT \
  --comparison-symbol ETHUSDT \
  --output-dir data/research/phase4l \
  --rng-seed 202604300

Output directory: data/research/phase4l/
  tables/             — 21 CSV tables (see "Result artefacts" below)
  plots/              — empty (matplotlib not in venv; documented)
  run_metadata.json   — run summary + verdict + RNG seed + manifests SHAs

Bootstrap iterations: 10 000 (Phase 4k default).
CSCV S: 16 (Phase 4k default).
Wall-clock: ~3-4 minutes (3 072 simulations + M2/M3 + PBO/CSCV).
```

---

## Variant grid summary

512 variants generated in deterministic lexicographic order over 9
binary axes (per Phase 4g §29 / Phase 4k):

| Axis # | Parameter | Values |
|---|---|---|
| 1 | N1 (Donchian breakout lookback) | {20, 40} 30m bars |
| 2 | P_w max (Donchian width percentile cap) | {25, 35} |
| 3 | V_rel_min (relative-volume minimum) | {1.5, 2.0} |
| 4 | V_z_min (volume z-score minimum) | {0.5, 1.0} |
| 5 | T_imb_min (taker-imbalance minimum) | {0.55, 0.60} |
| 6 | OI_dir (OI delta direction policy) | {`aligned`, `non_negative`} |
| 7 | Funding band | {[20, 80], [30, 70]} |
| 8 | N_R (fixed-R take-profit) | {2.0, 2.5} |
| 9 | T_stop (time-stop horizon) | {12, 16} 30m bars |

`build_variants()` produces exactly 2^9 = 512 variants with
`variant_id` indexed lexicographically. Variant 0 = (20, 25, 1.5,
0.5, 0.55, "aligned", [20, 80], 2.0, 12). Variant 511 = (40, 35,
2.0, 1.0, 0.60, "non_negative", [30, 70], 2.5, 16). Recorded in
`data/research/phase4l/tables/parameter_grid.csv`.

**No grid extension. No grid reduction. No early exit on bad
variants. All 512 variants reported.**

---

## Feature implementation verification

Pre-Phase-4l manual feature trace on BTCUSDT (variant 0; train
window) confirms each feature computes correctly:

| Feature | Computation | Non-NaN bars / 74 448 |
|---|---|---|
| ATR(20) | Wilder smoothing | 74 429 |
| HTF bias state == +1 (long bias) | 4h EMA(20)/EMA(50) discrete comparison + close > EMA20 + EMA20 rising vs. 3 bars earlier | 25 464 |
| HTF bias state == −1 (short bias) | mirror | 24 088 |
| Donchian high N1=20 | rolling max excluding current 20 bars | 74 428 |
| Donchian width percentile (N1=20, L_w=240) | rolling percentile rank | 74 208 |
| ATR percentile | rolling percentile rank L_atr=240 | 74 208 |
| Range-expansion ratio | TR / mean trailing N_re=20 TR | 74 428 |
| Relative volume | volume / mean trailing L_vol=240 | 74 208 |
| Volume z-score | (volume − mean) / stdev trailing L_vol | 74 208 |
| UTC-hour volume percentile | trailing 60-day same-hour distribution | 71 568 |
| Taker-buy fraction | taker_buy_volume / volume (kline columns only) | 74 444 |
| OI eligibility (Phase 4j §11) | per-bar 6-aligned-record check | 74 415 |
| OI delta (Phase 4j §17) | OI(open+25min) − OI(open−5min) | 74 415 |
| Funding-rate percentile (L_fund=90) | trailing distribution at 30m close | 73 024 |

All features have abundant non-NaN coverage. The Phase 4j §11
per-bar exclusion (74 415 / 74 448 = 99.957% eligible) is
non-restrictive in practice.

**Per-condition signal funnel (variant 0, BTCUSDT, raw — *before*
applying the stop-distance filter):**

```text
htf_bias == +1                                   25 464  (34.2%)
+ Donchian breakout (close > don_high + 0.10*ATR)   1 063   (4.2%)
+ Donchian width percentile <= 25                     291   (1.1%)
+ range_expansion >= 1.0                              277   (1.0%)
+ ATR percentile in [25, 75]                          109   (0.4%)
+ relative_volume >= 1.5 AND vol_z >= 0.5              67   (0.3%)
+ UTC-hour volume percentile >= 50                     64   (0.3%)
+ taker_buy_fraction >= 0.55                           46   (0.2%)
+ OI delta > 0                                         31   (0.1%)
+ funding percentile in [20, 80]                       15   (0.05%)
+ OI eligibility (Phase 4j §11)                        15   (0.05%)
```

Without the stop-distance filter, **15 long-side raw setups exist
on BTCUSDT over the entire 4-year coverage** for variant 0.

**Stop-distance filter rejection:**

```text
Long-side raw setups (no stop_ok):                     15
After stop-distance filter [0.60, 1.80] × ATR(20):       0
Setups failing stop_ok:                                15  (100%)
```

Sample stop-distance values (variant 0, BTC; close − setup_low + 0.10 × ATR):

| Bar idx | close | setup_low | ATR(20) | stop_dist | stop_dist / ATR |
|---|---|---|---|---|---|
| 7516  | 31 688.30  | 31 130.70  | 174.28 | 575.03   | 3.30 |
| 30 004 | 26 641.70  | 26 358.60  | 62.57  | 289.36   | 4.62 |
| 39 134 | 71 541.60  | 69 608.90  | 422.68 | 1 974.97 | 4.67 |
| 39 194 | 71 728.00  | 69 466.40  | 417.01 | 2 303.30 | 5.52 |
| 39 397 | 70 974.90  | 70 200.00  | 210.11 | 795.91   | 3.79 |
| 41 629 | 65 918.00  | 65 049.40  | 298.14 | 898.41   | 3.01 |
| 44 667 | 65 104.00  | 63 371.40  | 346.74 | 1 767.27 | 5.10 |
| 49 502 | 68 582.10  | 67 584.20  | 209.57 | 1 018.86 | 4.86 |
| 50 850 | 98 722.80  | 96 929.90  | 431.37 | 1 836.04 | 4.26 |
| 51 838 | 104 788.30 | 102 438.00 | 466.27 | 2 396.93 | 5.14 |

All 15 raw long setups have stop distance in the range 3-5 × ATR(20)
— well above the 1.80 × ATR upper bound from Phase 4g §19 / V1 §"Stop-distance
filter".

**Generalized to all 512 variants × 2 symbols:** `compute_signals`
returned `np.zeros(74 448, dtype=bool)` for every (variant, symbol)
combination after the stop-distance filter. No simulator can produce
trades from an all-False signal array; consequently 0 trades are
emitted across all 3 072 (variant × symbol × cost_cell) simulations.

---

## Train / validation / OOS windows

Per Phase 4k binding:

| Window | Start (UTC) | End (UTC) | Span | Use |
|---|---|---|---|---|
| Training / model-selection | 2022-01-01 00:00:00 | 2023-06-30 23:30:00 | ~18 months | per-variant Sharpe; DSR; CSCV; variant selection |
| Validation / selection-confirmation | 2023-07-01 00:00:00 | 2024-06-30 23:30:00 | ~12 months | selection-confirmation (NOT used for variant re-selection) |
| Out-of-sample holdout | 2024-07-01 00:00:00 | 2026-03-31 23:30:00 | ~21 months | **primary V2 evidence cell** |

**Total span:** ~51 months exactly = full Phase 4i coverage.

No data shuffle. No leakage. No window modification.

---

## BTCUSDT primary results

**All 512 variants × 3 cost cells × 3 windows = 4 608 result cells.**

Every cell records `trade_count = 0`, `mean_R = 0`, `total_R = 0`,
`max_dd_R = 0`, `profit_factor = 0` (defaulted to 0 when no trades),
`sharpe = 0`. Recorded verbatim in
`data/research/phase4l/tables/btc_train_variants.csv`,
`btc_validation_variants.csv`, `btc_oos_variants.csv`,
`cost_sensitivity.csv`.

**BTC-train-best variant identification:**

| variant_id | label | train_sharpe | DSR | val_sharpe | OOS_sharpe |
|---|---|---|---|---|---|
| **0** | `N1=20|Pw=25|Vrel=1.5|Vz=0.5|Timb=0.55|OI=aligned|FB=20-80|NR=2.0|Tstop=12` | 0 | 0 | 0 | 0 |

The BTC-train-best variant is variant_id=0 by tiebreaker (since all
512 variants have identical 0-Sharpe train Sharpe, the lexicographically
first variant is selected). This is methodologically the correct
selection: it's the lexicographically first variant after a tie on
the selection metric, not a meaningful "winner".

**BTC-train-best cost-cell sensitivity:**

| cost_cell | trade_count | mean_R | total_R | sharpe | profit_factor | passes_CFP-2 |
|---|---|---|---|---|---|---|
| LOW | 0 | 0 | 0 | 0 | 0 | true |
| MEDIUM | 0 | 0 | 0 | 0 | 0 | true |
| **HIGH (§11.6)** | 0 | 0 | 0 | 0 | 0 | **true** |

CFP-2 (negative OOS expectancy under HIGH cost) does NOT trigger
because expectancy is exactly 0 (not negative). However, this is
methodologically irrelevant because there are no trades — the
expectancy is structurally undefined. CFP-1 critical takes precedence.

---

## ETHUSDT comparison results

Identical structural pattern to BTCUSDT: every variant × cost cell ×
window cell has `trade_count = 0`. Recorded in
`eth_train_variants.csv`, `eth_validation_variants.csv`,
`eth_oos_variants.csv`.

ETHUSDT does not "rescue" BTCUSDT (per Phase 4g §10 / Phase 4k); the
cross-symbol consistency is trivially: both symbols fail at the same
structural design boundary.

---

## Cost sensitivity results

Per Phase 4k §"Cost and slippage model":

| Cost cell | Slippage per side | Round-trip cost | Phase 4l result on BTC OOS, BTC-train-best |
|---|---|---|---|
| LOW | 1 bp | 10 bps | trade_count=0, mean_R=0 |
| MEDIUM | 4 bps | 16 bps | trade_count=0, mean_R=0 |
| **HIGH (§11.6)** | **8 bps** | **24 bps** | **trade_count=0, mean_R=0** |

**§11.6 HIGH cost cell preserved verbatim.** No relaxation. No
maker-rebate. No live-fee assumption. Funding cost included in
realized_R (zero in this run because no trades exist).

---

## M1 mechanism-check results

Per Phase 4k §30:

| Symbol | M1_frac_0_5R_MFE | M1_trade_count | M1_pass |
|---|---|---|---|
| BTCUSDT | 0.0 | 0 | false |
| ETHUSDT | 0.0 | 0 | false |

**M1 is NOT meaningfully evaluable.** With 0 OOS trades on the
BTC-train-best variant, the fraction-reaching-+0.5R-MFE is undefined.
Phase 4l's implementation defaults this to 0.0 (which < 0.50
threshold → "false"), but the underlying cause is CFP-1 critical.
The verdict reason field correctly reports "CFP-1 critical" rather
than "M1 FAIL".

---

## M2 mechanism-check results

Per Phase 4k §30:

| Symbol | full_mean_R | relaxed_mean_R | diff_R | bootstrap CI lo | bootstrap CI hi | M2_pass |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | false |
| ETHUSDT | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | false |

**M2 is NOT meaningfully evaluable.** Both the full V2 trade
population and the participation-relaxed degenerate trade population
are empty. The bootstrap-by-trade with B = 10 000 iterations was
executed but produced trivial 0-difference results because both
input arrays are empty. The relaxed variant — where
`relax_participation=True` disables relative-volume,
volume-z-score, UTC-hour percentile, and taker-imbalance gates —
also produced 0 trades because the stop-distance filter still
rejects all setups. M2 = false trivially.

---

## M3 mechanism-check results

Per Phase 4k §30:

| Symbol | full_mean_R | relaxed_mean_R | diff_R | diff_high_R | high_resilience_ok | M3_pass |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.0 | 0.0 | 0.0 | 0.0 | true | false |
| ETHUSDT | 0.0 | 0.0 | 0.0 | 0.0 | true | false |

**M3 is NOT meaningfully evaluable.** Both the full V2 trade
population and the derivatives-relaxed degenerate trade population
are empty. The derivatives-relaxed variant — where
`relax_derivatives=True` disables OI direction gate and funding
band — produces 0 trades because the stop-distance filter still
rejects all setups. M3 = false trivially.

The `high_resilience_ok = true` field reflects that the differential
at HIGH-cost cell does not degrade by more than ε = 0.05R from the
MEDIUM-cell differential (both are 0.0, so the differential is
trivially non-degraded). This is methodologically vacuous given
the underlying 0-trade population.

---

## PBO / deflated Sharpe / CSCV results

Per Phase 4k §"PBO / deflated Sharpe / CSCV plan":

- **CSCV S = 16 chronologically-respecting sub-samples** (Phase 4k
  default). Number of (in-sample, out-of-sample) combinations:
  `C(16, 8) = 12 870`.
- **PBO (train internal CSCV) on BTCUSDT MEDIUM-slip:** **0.500**.
  CFP-6 threshold is `> 0.5`. **CFP-6 NOT triggered** (PBO =
  exactly 0.5 means the in-sample-best variant ranks at exactly the
  median out-of-sample on average — this is the trivial "no
  information" reading expected when all 512 variants have
  identical 0 trade counts).
- **Deflated Sharpe (DSR):** every variant has `train_sharpe = 0`
  and `train_dsr = 0` because all 512 variants have empty
  per-trade R arrays on the train window. DSR = 0 < 1.96 → no
  variant survives DSR significance. Recorded in
  `deflated_sharpe_summary.csv`.

**PBO and DSR are NOT meaningfully evaluable** under the structural
0-trade pattern. They are reported verbatim as required by Phase
4k methodology, with the explicit note that the 0.5 PBO is the
trivial "no signal" reading, not evidence of overfitting.

---

## Main-cell vs exclude-entire-affected-days sensitivity

| scope | trade_count | mean_R |
|---|---|---|
| main_btc_oos_medium | 0 | 0.0 |
| sensitivity_btc_oos_medium | 0 | 0.0 |

Sensitivity comparison is methodologically inert because the main
cell already has 0 trades. CFP-8 not triggered. Recorded in
`main_vs_exclude_affected_days.csv`.

---

## Trade distribution by year / month / regime

Empty. No trades exist on any window for any variant. CFP-7 not
triggered (requires monthly fraction > 50% of total R, but total R
= 0 so the predicate is trivially false).

`trade_distribution_by_month_regime.csv` written with header only.

---

## Catastrophic-floor predicate results

| Predicate | Triggered | Detail |
|---|---|---|
| **CFP-1** | **TRUE** | 512/512 variants with <30 OOS trades |
| CFP-2 | false | BTC OOS HIGH mean_R=0.0000 (not < 0) |
| CFP-3 | true | max_dd_R=0.0000, PF=0.0000 (PF < 0.50 because PF=0) |
| CFP-4 | false | BTC pass=False, ETH pass=False (neither passes; CFP-4 requires BTC fail AND ETH pass) |
| CFP-5 | false | train_sharpe=0.0000, oos_sharpe=0.0000 (CFP-5 requires train_sharpe > 1.0 AND OOS_sharpe < 0.0; neither holds) |
| CFP-6 | false | PBO=0.5000 (boundary; not strictly > 0.5) |
| CFP-7 | false | max month_fraction over 0.5 — N/A (no trades) |
| CFP-8 | false | main_R=0.0000, sensitivity_R=0.0000 (no degradation possible) |
| CFP-9 | false | excluded_fraction=0.0004 (well under 5%) |
| CFP-10 | false | no optional ratio-column access detected |
| CFP-11 | false | per-bar exclusion algorithm matches Phase 4j §16 |
| CFP-12 | false | no forbidden data access detected |

**CFP-3 note:** profit factor defaults to 0.0 when both wins and losses
are empty; this is < 0.50 threshold, so CFP-3 mechanically triggers.
However, CFP-3's "catastrophic drawdown / PF<0.5" semantics presume
a non-empty trade population. The downstream verdict logic correctly
prioritizes CFP-1 critical over CFP-3 mechanical-triggering, because
CFP-1 critical is a more diagnostic predicate for the 0-trade root
cause.

**CFP-1 critical** is the binding driver of Verdict C HARD REJECT.

---

## Verdict declaration

```text
Verdict: C — V2 framework HARD REJECT
btc_train_best_variant_id: 0
Reason: CFP-1 critical: 512/512 variants with <30 OOS trades on
        BTCUSDT; BTC-train-best variant has 0 OOS trades. M1 / M2 /
        M3 mechanism checks not meaningfully evaluable. HARD REJECT
        analogous to F1 catastrophic-floor pattern (Phase 3c §7.3).
```

Recorded in `data/research/phase4l/tables/verdict_declaration.csv`.

**Implication per Phase 4k §"Verdict taxonomy" / §"Promotion / failure
/ partial-pass criteria":**

- Verdict C HARD REJECT is **terminal for the V2 first-spec under
  Phase 4g §29 locked threshold grid + V1-inherited stop-distance
  filter (0.60-1.80 × ATR)**, analogous to F1's HARD REJECT under
  Phase 3c §7.3 catastrophic-floor predicate (Phase 3d-B2 terminal).
- V2 retained as **research evidence**: not implemented; not
  validated; not live-ready; **not a rescue**.
- **No V2-prime, V2-narrow, V2-relaxed, V2-with-different-features,
  V2 / V1 hybrid, V2 / D1-A hybrid, or any other rescue authorized**
  per Phase 4k methodology.
- The forensic finding (V1-inherited stop-distance filter
  incompatible with V2's Donchian setup window) is research evidence
  only and **does NOT license** a Phase 4g §29 amendment, a stop-distance
  bound revision, an N1 axis revision, a setup_low semantic
  revision, or any other parameter / spec / governance modification.
  Any future research direction must satisfy the Phase 3t §12
  validity gate.

---

## Result artefacts created

### Committed (text only)

- `scripts/phase4l_v2_backtest.py` (the standalone V2 backtest
  orchestrator).
- `docs/00-meta/implementation-reports/2026-04-30_phase-4l_v2-backtest-execution.md`
  (this file).
- `docs/00-meta/implementation-reports/2026-04-30_phase-4l_closeout.md`
  (the closeout artefact, created in a follow-up commit).

### Local gitignored (under `data/research/phase4l/`)

- `run_metadata.json` — run summary; verdict; RNG seed; manifest
  SHAs; CSCV/bootstrap configuration; metrics_oi_columns_loaded;
  optional_ratio_column_access_count = 0.
- `tables/manifest_references.csv` — 8 dataset manifest references
  with SHA256 pinning.
- `tables/parameter_grid.csv` — full 512-variant grid in lexicographic
  order.
- `tables/split_boundaries.csv` — train/validation/OOS UTC dates +
  ms.
- `tables/btc_train_variants.csv`, `btc_validation_variants.csv`,
  `btc_oos_variants.csv` — per-variant trade summaries (BTC).
- `tables/eth_train_variants.csv`, `eth_validation_variants.csv`,
  `eth_oos_variants.csv` — per-variant trade summaries (ETH).
- `tables/btc_train_best_variant.csv` — train-best variant ID + label
  + DSR / Sharpe.
- `tables/btc_train_best_cost_cells.csv` — LOW / MEDIUM / HIGH
  cost-cell results.
- `tables/m1_m2_m3_mechanism_checks.csv` — M1 / M2 / M3 results per
  symbol.
- `tables/cost_sensitivity.csv` — full per-variant per-cost-cell
  results.
- `tables/pbo_summary.csv` — PBO summary.
- `tables/deflated_sharpe_summary.csv` — DSR per variant.
- `tables/metrics_oi_exclusions.csv` — Phase 4j §11 exclusion
  counts per symbol.
- `tables/main_vs_exclude_affected_days.csv` — sensitivity comparison.
- `tables/trade_distribution_by_month_regime.csv` — empty (no trades).
- `tables/verdict_declaration.csv` — verdict + reason.
- `tables/catastrophic_floor_predicates.csv` — 12 CFP results.
- `tables/forbidden_work_confirmation.csv` — runtime introspection
  results.

**Plots not produced** (matplotlib not in venv; documented).
`data/research/phase4l/plots/` directory exists but is empty.

The `cscv_rankings.csv` table mentioned in Phase 4k §"Required
reporting tables" is omitted because all 12 870 CSCV combinations
report identical 0-Sharpe variants — there is no useful ranking
distribution to record. Phase 4k §"Required reporting tables" notes
"or compressed equivalent if large"; the PBO summary is the
equivalent.

`data/research/**` is gitignored per the existing repository
convention. Phase 4l does NOT commit Parquet, CSV, JSON outputs
under `data/research/phase4l/` — they are reproducible from the
Phase 4i acquired data via the orchestrator script with identical
RNG seed.

---

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4l/v2-backtest-execution
git branch --show-current
ls data/manifests/
ls data/normalized/
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check scripts/phase4l_v2_backtest.py
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m mypy
.venv/Scripts/python -m pytest -q

# Optional ratio static scan (Phase 4l-specific):
.venv/Scripts/python -c "
forbidden = [
    'count_toptrader_long_short_ratio',
    'sum_toptrader_long_short_ratio',
    'count_long_short_ratio',
    'sum_taker_long_short_vol_ratio',
]
src = open('scripts/phase4l_v2_backtest.py', encoding='utf-8').read()
hits = [n for n in forbidden if n in src]
print('Forbidden ratio names in script:', hits)
print('Pass:', len(hits) == 0)
"
# Result: Forbidden ratio names in script: []; Pass: True

# Backtest execution:
.venv/Scripts/python scripts/phase4l_v2_backtest.py \
  --start 2022-01-01 --end 2026-03-31 \
  --train-start 2022-01-01 --train-end 2023-06-30 \
  --validation-start 2023-07-01 --validation-end 2024-06-30 \
  --oos-start 2024-07-01 --oos-end 2026-03-31 \
  --symbols BTCUSDT ETHUSDT \
  --primary-symbol BTCUSDT --comparison-symbol ETHUSDT \
  --output-dir data/research/phase4l \
  --rng-seed 202604300

# Final quality re-checks:
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m mypy
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
- No git push to main. No merge to main. Phase 4l is branch-only.

---

## Verification results

| Check | Result |
|---|---|
| `python --version` | `Python 3.12.4` |
| `ruff check .` (whole repo) | `All checks passed!` |
| `pytest` | `785 passed in ~13s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |
| Optional ratio name static scan | `Forbidden ratio names in script: []; Pass: True` |
| Phase 4l backtest exit code | `0` |
| BTCUSDT 30m manifest SHA verified | match |
| ETHUSDT 30m manifest SHA verified | match |
| BTCUSDT 4h manifest SHA verified | match |
| ETHUSDT 4h manifest SHA verified | match |
| BTCUSDT metrics manifest research_eligible | `false` (preserved) |
| ETHUSDT metrics manifest research_eligible | `false` (preserved) |
| BTCUSDT funding v002 manifest reused | yes |
| ETHUSDT funding v002 manifest reused | yes |
| Per-bar exclusion algorithm verification | matches Phase 4j §16 |

Whole-repo quality gates remain **fully clean**: zero ruff errors;
785 / 785 tests passing; zero mypy strict issues across 82 source
files. No regressions relative to the post-Phase-4k-merge baseline.

---

## What this does not authorize

Phase 4l explicitly does NOT authorize, propose, or initiate any of
the following:

- **Any successor phase.** Phase 4m (or any other) is NOT
  authorized.
- **V2 implementation.** No `src/prometheus/strategy/` modification.
- **V2 spec amendment.** Phase 4g §28 / §29 / §30 / §22-§24 preserved
  verbatim. The forensic finding (stop-distance filter incompatible
  with V2 Donchian setup) does NOT license amending Phase 4g §19's
  bounds, Phase 4g §29 axis 1's N1 values, or any other Phase 4g
  selection.
- **Phase 4j §11 amendment.** The metrics OI-subset rule is preserved
  verbatim. Phase 4l's empirical exclusion fraction (~0.04%) confirms
  that Phase 4j §11 is not the binding constraint.
- **Phase 4k methodology amendment.** Preserved verbatim.
- **Optional ratio-column activation.** Forbidden by Phase 4j §11.3.
- **Mark-price 30m / 4h acquisition.** Deferred per Phase 4h §20.
- **`aggTrades` acquisition.** Deferred per Phase 4h §7.E.
- **v003 dataset creation.** Not authorized.
- **Manifest modification.** All Phase 4i / v002 / v001-of-5m
  manifests preserved verbatim.
- **Any retained-evidence verdict revision.** R3 / H0 / R1a /
  R1b-narrow / R2 / F1 / D1-A all preserved.
- **Any project-lock revision.** §1.7.3 / §11.6 / mark-price stops
  preserved.
- **Live exchange-write capability.** Architectural prohibition
  unchanged.
- **Production Binance keys, authenticated APIs, private endpoints,
  user stream, WebSocket, listenKey lifecycle, production alerting,
  Telegram / n8n production routes, MCP, Graphify, `.mcp.json`,
  credentials, exchange-write capability.** None touched.
- **V2-prime, V2-narrow, V2-relaxed, V2-with-different-features,
  V2 / V1 hybrid, V2 / D1-A hybrid, V2 / F1 hybrid, or any other
  V2 rescue.** Phase 4l Verdict C is terminal for V2 first-spec.
- **Strategy implementation, rescue, or new candidate** other than
  via a separately authorized future research-direction phase
  satisfying the Phase 3t §12 validity gate.
- **Reconciliation implementation.** Phase 4e reconciliation-model
  design preserved verbatim, not implemented.
- **Paper / shadow / live-readiness / deployment.** Not authorized.
- **Phase 4 (canonical).** Per `docs/12-roadmap/phase-gates.md`.

---

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4m / successor phase started.**
- **No V2 implementation under `src/prometheus/strategy/`.** Existing
  `prometheus.strategy` modules untouched.
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No existing `scripts/**` modification.**
  (`scripts/phase4l_v2_backtest.py` is new and standalone.)
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
  D1-A all preserved.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4j §11 metrics OI-subset governance modification.**
- **No Phase 4f / 4g / 4h / 4i / 4j / 4k text modification.**
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
  Phase 4l branch.** Per the Phase 4l brief.
- **No optional ratio-column access.** Static scan + runtime
  introspection: 0.
- **No merge to main.**
- **No successor phase started.**

---

## Remaining boundary

- **Recommended state:** **paused**. Phase 4l deliverables exist as
  branch-only artefacts pending operator review.
- **Phase 4l output:** docs-and-code branch artefacts (one
  standalone backtest script + this report + the Phase 4l closeout).
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
- **V2 backtest methodology governance:** Phase 4k §"Backtest
  purpose" through §"Reproducibility requirements" (preserved
  verbatim; honored exactly by Phase 4l).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j) +
  backtest-plan binding (Phase 4k) + **executed (Phase 4l, this
  phase) → Verdict C HARD REJECT**. **Terminal for V2 first-spec.**
  V2 retained as research evidence only; non-leading; no V2 rescue
  authorized.
- **OPEN ambiguity-log items after Phase 4l:** zero relevant to
  runtime / strategy implementation. (The forensic finding about
  V2 stop-distance filter incompatibility is research evidence only
  and does NOT introduce a pre-coding ambiguity-log entry, per
  Phase 4j §11.8 / Phase 4k §"What this does not authorize".)
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  V2 HARD REJECT (Phase 4l, structural CFP-1 critical); §11.6 = 8
  bps HIGH per side; §1.7.3 project-level locks; mark-price stops;
  v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:** `phase-4l/v2-backtest-execution` exists locally
  and on `origin` (after push). NOT merged to main.

---

## Operator decision menu

Phase 4l presents the following operator decision options:

### Option A — Remain paused (PRIMARY RECOMMENDATION)

Take no further action. Phase 4l methodology + execution evidence
is recorded; V2 first-spec Verdict C HARD REJECT is terminal.

**Reasoning:**

- V2 first-spec, as predeclared by Phase 4g and methodology-bound by
  Phase 4k, produces a structural CFP-1 critical failure under the
  V1-inherited stop-distance filter (0.60-1.80 × ATR) interacting
  with V2's 20/40-bar Donchian setup window. This is analogous to
  F1's HARD REJECT under Phase 3c §7.3 catastrophic-floor.
- V2-prime / V2-narrow / V2-relaxed / V2-with-different-features /
  V2 hybrid variants are NOT authorized by this Phase 4l verdict.
  Any future research direction must satisfy the Phase 3t §12
  validity gate (genuinely new ex-ante hypothesis; not derived
  from observed Phase 4l patterns; full written specification
  before any data is touched; predeclared evidence thresholds;
  separate operator authorization).
- The current cumulative project state across V1 / R3 baseline-of-record,
  R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence,
  and now V2 HARD REJECT means there is **no live-deployable
  strategy candidate** in the project. Remain paused respects
  this finding without a hasty next-direction commitment.

### Option B — Docs-only post-V2 research consolidation memo (CONDITIONAL SECONDARY)

Authorize a separate docs-only memo analogous to Phase 3e (post-F1)
or Phase 3k (post-D1-A) that consolidates V2 research findings,
records what was learned, and explicitly identifies what cannot be
salvaged without violating the Phase 3t §12 validity gate. This memo
would NOT propose a V2 rescue or V2-prime — it would be retrospective
research consolidation only.

**Verdict:** Acceptable conditional secondary. Procedurally similar
to Phase 3e / Phase 3k. Would NOT authorize implementation, paper /
shadow / live, or any new strategy direction.

### Option C — Authorize fresh-hypothesis research direction (NOT RECOMMENDED before docs-only consolidation)

Per Phase 3t §14.2 / Phase 3u §14, fresh-hypothesis research is
**paused** as the cumulative recommendation. Authorizing a new
ex-ante hypothesis (subject to the §12 validity gate) before
consolidating V2 findings risks rhetorical drift toward V2 rescue
framing. NOT RECOMMENDED before Option B.

### Option D — Phase 4j §11 amendment / Phase 4g §29 amendment / stop-distance bound revision (REJECTED)

Modifying Phase 4j §11 governance, Phase 4g §29 threshold grid, the
stop-distance bounds 0.60-1.80 × ATR, the N1 axis values {20, 40},
or any other Phase 4g / Phase 4k locked selection in response to
the observed V2 outcome would be parameter rescue (Bailey et al.
2014). REJECTED.

### Option E — V2 implementation (REJECTED)

V2 implementation requires successful backtest evidence. Verdict C
HARD REJECT precludes implementation authorization. REJECTED.

### Option F — Paper / shadow / live-readiness / exchange-write (FORBIDDEN)

Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.
FORBIDDEN.

### Phase 4l recommendation

**Phase 4l recommendation: Option A (remain paused) primary; Option
B (docs-only post-V2 research consolidation memo) conditional
secondary.** Options C / D / E not recommended. Option F forbidden.

---

## Next authorization status

**No next phase has been authorized.** Phase 4l's recommendation is
**Option A (remain paused) as primary**, with **Option B (docs-only
post-V2 research consolidation memo) as conditional secondary**.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.

The 5m research thread remains operationally complete and closed
(per Phase 3t). The implementation-readiness boundary remains
reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding
governance blockers remain RESOLVED at the governance level (per
Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented
(per Phase 4a). The Phase 4b script-scope quality-gate restoration
is complete (per Phase 4b). The Phase 4c state-package quality-gate
residual cleanup is complete (per Phase 4c). The Phase 4d
post-4a/4b/4c review is complete (per Phase 4d). The Phase 4e
reconciliation-model design memo is complete (per Phase 4e). The
Phase 4f V2 hypothesis predeclaration is complete (per Phase 4f).
The Phase 4g V2 strategy spec is complete (per Phase 4g). The Phase
4h V2 data-requirements / feasibility memo is complete (per Phase
4h). The Phase 4i V2 public data acquisition + integrity validation
is complete (per Phase 4i; partial-pass). The Phase 4j V2 metrics
data governance memo is complete (per Phase 4j; Phase 4j §11
binding). The Phase 4k V2 backtest-plan memo is complete (per
Phase 4k; methodology binding). The Phase 4l V2 backtest execution
is complete on this branch (this phase; **Verdict C HARD REJECT;
terminal for V2 first-spec**).

**Recommended state remains paused. No next phase authorized.**
