# Phase 4l Merge Closeout

## Summary

Phase 4l has been merged into `main` via a `--no-ff` merge commit at
SHA `918b10a60df23481c25522cdeb51941abecfd44e` and pushed to
`origin/main`. The Phase 4l V2 backtest standalone research script
`scripts/phase4l_v2_backtest.py`, the Phase 4l V2 backtest execution
report, and the Phase 4l closeout artefact are now part of the
project record on `main`.

Phase 4l implemented and ran the standalone V2 backtest exactly under
the Phase 4k methodology and emitted **Verdict C — V2 framework
HARD REJECT**, driven by the **CFP-1 critical** catastrophic-floor
predicate: 512 / 512 variants produced fewer than the 30-OOS-trade
threshold on BTCUSDT; the BTC-train-best variant produced 0 OOS
trades. Root cause: V2's locked 20/40-bar Donchian setup window per
Phase 4g §29 axis 1 is structurally incompatible with the V1-inherited
0.60–1.80 × ATR(20) stop-distance filter per Phase 4g §19 / V1
§"Stop-distance filter". Raw V2 candidates produce stop distances
around 3–5 × ATR(20), exceeding the upper bound, so all are rejected
before trade generation. Analogous to F1 catastrophic-floor pattern
(Phase 3c §7.3); terminal for V2 first-spec.

**Phase 4l was docs-and-code, narrowly scoped:**

- one new standalone research script
  (`scripts/phase4l_v2_backtest.py`);
- two new Markdown reports under
  `docs/00-meta/implementation-reports/`;
- local gitignored Phase 4l outputs under `data/research/phase4l/`
  (not committed; reproducible from the orchestrator with pinned
  RNG seed 202604300).

**Phase 4l preserved verbatim:** R3 baseline-of-record; H0 framework
anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence
only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT;
D1-A MECHANISM PASS / FRAMEWORK FAIL — other; **V2 HARD REJECT
(Phase 4l, structural CFP-1 critical, terminal for V2 first-spec)**;
§11.6 = 8 bps HIGH per side; §1.7.3 project-level locks (including
mark-price stops); v002 verdict provenance; Phase 3q mark-price 5m
manifests `research_eligible: false`; Phase 3r §8 mark-price gap
governance; Phase 3v §8 stop-trigger-domain governance; Phase 3w
§6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase
4a public API and runtime behavior; Phase 4e reconciliation-model
design memo; Phase 4f V2 hypothesis predeclaration; Phase 4g V2
strategy spec; Phase 4h V2 data-requirements / feasibility memo;
Phase 4i V2 acquisition + integrity report; Phase 4i metrics
manifests `research_eligible: false`; Phase 4j §11 metrics OI-subset
partial-eligibility rule; Phase 4k V2 backtest-plan methodology —
all preserved verbatim.

**Whole-repo quality gates remain clean** at Phase 4l merge:
`ruff check .` passed; pytest 785 passed; mypy strict 0 issues
across 82 source files.

**Phase 4 canonical remains unauthorized.** **Phase 4m / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, and exchange-write all remain
unauthorized.**

V2 remains **pre-research only**: not implemented; not validated;
not live-ready; **not a rescue** of R3 / R2 / F1 / D1-A. **Verdict
C HARD REJECT is terminal for the V2 first-spec.**

**Recommended state remains paused. No next phase authorized.**

## Files changed

```text
scripts/phase4l_v2_backtest.py                                                      (new; from Phase 4l branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4l_v2-backtest-execution.md     (new; from Phase 4l branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4l_closeout.md                  (new; from Phase 4l branch)
docs/00-meta/implementation-reports/2026-04-30_phase-4l_merge-closeout.md            (new; this file; introduced by housekeeping commit)
docs/00-meta/current-project-state.md                                                (modified; narrow Phase 4l sync; introduced by housekeeping commit)
```

No other files modified by Phase 4l, the merge, or the housekeeping
commit. No source code under `src/prometheus/`, no tests under
`tests/`, no existing scripts, no data under `data/raw/` or
`data/normalized/`, and no manifests under `data/manifests/` were
touched.

Local gitignored Phase 4l outputs under `data/research/phase4l/`
were NOT committed (reproducible from the orchestrator script with
pinned RNG seed). The transient runtime file `.claude/scheduled_tasks.lock`
was NOT committed.

## Phase 4l commits included

```text
Phase 4l backtest+report commit:    f795d3f3387a1ea48e8ff2d226f752ea3b7bf76a
Phase 4l closeout commit:           ec3a3c3f6479af0f881111150223c6cee38922ef
```

Both commits are now in `main`'s history via the merge.

## Merge commit

```text
Merge commit:                918b10a60df23481c25522cdeb51941abecfd44e
Merge title:                 Merge Phase 4l (V2 backtest execution, docs-and-code) into main
Merge type:                  --no-ff merge of phase-4l/v2-backtest-execution into main
Branch merged from:          phase-4l/v2-backtest-execution
Branch merged into:          main
```

## Housekeeping commit

To be appended after the housekeeping commit lands on `main`.

## Final git status

To be appended after housekeeping commit and push.

## Final git log --oneline -8

To be appended after housekeeping commit and push.

## Final rev-parse

To be appended after housekeeping commit and push.

## main == origin/main confirmation

To be appended after housekeeping commit and push.

## Backtest execution conclusion

- **Phase 4l was docs-and-code standalone research execution.** Phase
  4l implemented only `scripts/phase4l_v2_backtest.py` as a
  standalone research script.
- **Phase 4l ran the full 512-variant V2 backtest under Phase 4k
  methodology**, with no methodology amendment.
- **Phase 4l did not implement V2 in `src/prometheus/`.** No
  modification to `src/prometheus/strategy/`, `src/prometheus/runtime/`,
  `src/prometheus/execution/`, `src/prometheus/persistence/`,
  `src/prometheus/risk/`, or `src/prometheus/exchange/` (or any
  module).
- **Phase 4l did not modify runtime, execution, persistence, risk,
  exchange, or strategy modules.**
- **Phase 4l did not modify tests.**
- **Phase 4l did not modify existing scripts.**
- **Phase 4l did not acquire, modify, or patch data.**
- **Phase 4l did not modify manifests.**
- **Phase 4l did not start any successor phase.** Phase 4m / any
  successor phase remains unauthorized after this merge.

## Verdict

- **Final Verdict: C — V2 framework HARD REJECT.**
- **Binding driver:** CFP-1 critical: 512 / 512 variants produced
  fewer than 30 OOS trades on BTCUSDT; BTC-train-best variant
  produced 0 OOS trades.
- **V2 first-spec is terminal.** Verdict C HARD REJECT is terminal
  for the V2 first-spec under Phase 4g §29 locked threshold grid +
  V1-inherited stop-distance filter.
- **V2 retained as research evidence only.** Non-leading.
- **No V2 rescue is authorized.** No V2-prime, V2-narrow, V2-relaxed,
  V2 hybrid, stop-distance amendment, N1 amendment, Phase 4g
  amendment, Phase 4j §11 amendment, or Phase 4k methodology
  amendment.

## Root-cause analysis

- **Raw V2 candidates existed before the stop-distance filter.** The
  8-feature AND chain (HTF bias + Donchian breakout + Donchian
  width compression + ATR regime band + range-expansion + relative
  volume + volume z-score + UTC-hour participation + taker
  imbalance + OI delta direction + funding-rate band) produces ~15
  raw long-side setups per variant per symbol over the 4-year
  coverage.
- **All raw candidates were rejected by the V1-inherited stop-distance
  filter.** The filter requires `0.60 × ATR(20) ≤ stop_distance ≤
  1.80 × ATR(20)`.
- **V2's locked 20/40-bar Donchian setup window caused setup stops
  around 3–5 × ATR(20).** With `setup_low = lowest low of the
  previous N1 30m bars` (Phase 4g §19) and N1 ∈ {20, 40} (Phase 4g
  §29 axis 1), the breakout-bar close sits 3–5 × ATR(20) above
  setup_low. All raw candidates fail the filter.
- **The locked stop-distance filter allowed only 0.60–1.80 × ATR(20).**
  Bounds preserved verbatim from V1's 8-bar setup window calibration.
- **This is structural incompatibility, not a metrics-governance
  failure.** Phase 4j §11 metrics OI-subset governance was honored
  exactly; per-bar exclusion fired on only 33 / 74 448 bars per
  symbol (~0.044%), well under CFP-9's 5% threshold.
- **The pattern is analogous to F1 catastrophic-floor failure**
  (Phase 3c §7.3 / Phase 3d-B2 terminal): the strategy spec, as
  predeclared, fails at the design stage before any data-dependent
  evaluation can occur.
- **The forensic result does not authorize threshold/spec amendment.**
  Per Phase 4k §"What this does not authorize" and Phase 4l brief
  forbidden list, no Phase 4g / Phase 4j §11 / Phase 4k methodology
  / stop-distance bound / N1 axis amendment is authorized by this
  Phase 4l verdict. Any future research direction must satisfy the
  Phase 3t §12 validity gate.

## Dataset inputs

- **Four research-eligible Phase 4i kline datasets used:**
  - `binance_usdm_btcusdt_30m__v001`
    (SHA256 `3cdf6fb91ffca8acc2a69ae05a00745a031360c01c585a75f876c64d42230da8`);
  - `binance_usdm_ethusdt_30m__v001`
    (SHA256 `0a7502c5e09916529e50951bd503e1a2ac95d372e99ba65f4cb3bfb1477e3afd`);
  - `binance_usdm_btcusdt_4h__v001`
    (SHA256 `b2413e7fbbacfa091f2f42af8220ee83b55ee2511ee2b7be070e936c5761180a`);
  - `binance_usdm_ethusdt_4h__v001`
    (SHA256 `3451959278e786fc44ebd41529cc1e83c999070d175e93e145e569eb815cdd79`).
- **Two Phase 4i metrics datasets used only through the Phase 4j
  OI subset:**
  - `binance_usdm_btcusdt_metrics__v001`
    (SHA256 `41d6a8e45a1f992ce813838640c28534dcd1885b4482d01d4ded7809a208baf7`;
    research_eligible: false; feature_use:
    oi_subset_only_per_phase_4j_§11);
  - `binance_usdm_ethusdt_metrics__v001`
    (SHA256 `deabe463e98ea4ffeedf525c53fce8a3629c9147ee4ac84e03a80f51db8be2be`;
    research_eligible: false; feature_use:
    oi_subset_only_per_phase_4j_§11).
- **Existing v002 funding manifests reused** (no re-acquisition;
  used only for funding-rate percentile feature):
  - `binance_usdm_btcusdt_funding__v002`;
  - `binance_usdm_ethusdt_funding__v002`.
- **No mark-price 30m / 4h / 5m / 15m used.** Mark-price 30m / 4h
  deferred per Phase 4h §20; Phase 3q v001-of-5m and v002 mark-price
  not consulted.
- **No aggTrades used.** Deferred per Phase 4h §7.E.
- **No spot or cross-venue data used.** Forbidden by §1.7.3.
- **No optional metrics ratio columns used.** Forbidden by Phase 4j
  §11.3 / §14.

## Metrics OI exclusion summary

- **BTCUSDT:** 74 448 total 30m bars; 74 415 OI-feature-eligible;
  30 missing/invalid; 3 previous-window missing; **0.044%** excluded.
- **ETHUSDT:** 74 448 total 30m bars; 74 415 OI-feature-eligible;
  30 missing/invalid; 3 previous-window missing; **0.044%** excluded.
- **CFP-9 not triggered.** Both symbols' exclusion fractions are
  well below the 5% threshold.
- **Phase 4j §11 honored exactly.** Per-bar exclusion algorithm
  matches Phase 4j §16 pseudocode verbatim. Verified in
  `data/research/phase4l/tables/forbidden_work_confirmation.csv`
  (`per_bar_exclusion_algorithm = matches_phase_4j_section_16`).
- **No forward-fill, no interpolation, no imputation, no synthetic
  OI data, no silent omission.** All Phase 4j §11.5 prohibitions
  honored verbatim.

## Optional ratio-column non-access verification

- **Static scan found zero forbidden ratio names.** The four
  optional ratio column name strings do not appear anywhere in
  `scripts/phase4l_v2_backtest.py`.
- **Metrics loader explicitly loaded only:**
  - `create_time`;
  - `symbol`;
  - `sum_open_interest`;
  - `sum_open_interest_value`.
  The pyarrow `read(columns=METRICS_OI_COLUMNS)` call uses an
  explicit four-element column list. The four optional ratio
  columns are NOT in this list and are NEVER loaded into memory.
- **Runtime optional ratio-column access count = 0.**
- **No optional ratio-column diagnostics computed.** No filter,
  label, sensitivity, or feature derived from optional ratio
  columns.

## BTCUSDT primary result summary

- **All 512 variants × 3 cost cells × 3 windows = 4 608 result
  cells produced:**
  - `trade_count = 0`;
  - `mean_R = 0`;
  - `total_R = 0`;
  - `sharpe = 0`;
  - `profit_factor = 0`.
- **BTC-train-best variant is variant_id = 0** by lexicographic
  tiebreaker over identical 0-Sharpe variants. Label:
  `N1=20|Pw=25|Vrel=1.5|Vz=0.5|Timb=0.55|OI=aligned|FB=20-80|NR=2.0|Tstop=12`.

## ETHUSDT comparison result summary

- **Identical 0-trade structural pattern.** All 512 variants × 3
  cost cells × 3 windows = 4 608 result cells with
  `trade_count = 0`, `mean_R = 0`, `total_R = 0`, `sharpe = 0`,
  `profit_factor = 0`.
- **ETH does not rescue BTC.** Cross-symbol consistency: both
  symbols fail at the same structural design boundary. Per Phase 4g
  §10 / Phase 4k, ETH cannot rescue a BTC failure.

## M1 / M2 / M3 summary

- **M1 false / NOT meaningfully evaluable due to 0 trades.** With
  0 OOS trades on the BTC-train-best variant, the
  fraction-reaching-+0.5R-MFE is undefined. Reported `false`
  trivially.
- **M2 false / NOT meaningfully evaluable due to 0 trades in full
  and participation-relaxed cells.** Both the full V2 and
  participation-relaxed degenerate variant trade populations are
  empty. Bootstrap-by-trade B = 10 000 was executed but produced
  trivial 0-difference results because both input arrays are empty.
- **M3 false / NOT meaningfully evaluable due to 0 trades in full
  and derivatives-relaxed cells.** Both the full V2 and
  derivatives-relaxed degenerate variant trade populations are
  empty. M3 = false trivially.
- **Verdict reason correctly prioritizes CFP-1 critical, not
  mechanism failure.** Phase 4l's verdict logic correctly attributes
  the failure to CFP-1 critical (insufficient trade count across
  all variants) rather than to "M1 FAIL" — the underlying cause is
  structural, not an organic mechanism failure.

## PBO / DSR / CSCV summary

- **PBO = 0.500.** CFP-6 threshold is `> 0.5` — not crossed. The
  0.5 PBO is the trivial "no signal" reading expected when all 512
  variants have identical 0-trade behavior.
- **DSR = 0 for all variants.** No variant survives DSR significance
  (`DSR > 1.96`).
- **CSCV S = 16, 12 870 combinations honored.** Per Phase 4k
  predeclared exact computation. Bootstrap-by-trade iterations:
  B = 10 000 per Phase 4k default.
- **These are methodologically inert under the 0-trade population.**
  Reported verbatim as required by Phase 4k methodology, with the
  explicit note that the 0.5 PBO is the trivial "no signal" reading,
  not evidence of overfitting.

## Cost sensitivity summary

| Cost cell | Slippage per side | Round-trip | Phase 4l result |
|---|---|---|---|
| LOW | 1 bp | 10 bps | trade_count=0, mean_R=0 |
| MEDIUM | 4 bps | 16 bps | trade_count=0, mean_R=0 |
| **HIGH (§11.6)** | **8 bps** | **24 bps** | **trade_count=0, mean_R=0** |

- **§11.6 HIGH cost preserved verbatim** at 8 bps slippage per side.
- **No cost-model relaxation.**
- **No maker rebate.** V2 entry orders are MARKET orders, paying
  taker fees.
- **No live-fee assumption.** No VIP discounts, BNB-payment
  discounts, or partner-rebate assumptions.
- **Funding cost included in realized_R** (zero in this run because
  no trades).

## Catastrophic-floor predicate summary

| Predicate | Triggered | Detail |
|---|---|---|
| **CFP-1** | **TRUE (binding)** | 512/512 variants with <30 OOS trades |
| CFP-2 | false | BTC OOS HIGH mean_R=0.0000 (not < 0) |
| CFP-3 | true (subordinate) | max_dd_R=0.0000, PF=0.0000 (PF<0.5 mechanically; subordinate to CFP-1) |
| CFP-4 | false | BTC pass=False, ETH pass=False (CFP-4 requires BTC fail AND ETH pass) |
| CFP-5 | false | train_sharpe=0.0000, oos_sharpe=0.0000 |
| CFP-6 | false | PBO=0.5000 (boundary; not strictly > 0.5) |
| CFP-7 | false | max month_fraction over 0.5 — N/A (no trades) |
| CFP-8 | false | main_R=0.0000, sensitivity_R=0.0000 |
| CFP-9 | false | excluded_fraction=0.0004 (well under 5%) |
| CFP-10 | false | no optional ratio-column access detected |
| CFP-11 | false | per-bar exclusion algorithm matches Phase 4j §16 |
| CFP-12 | false | no forbidden data access detected |

- **CFP-1 TRUE and binding.** 512/512 variants produced fewer than
  the 30-OOS-trade threshold on BTCUSDT.
- **CFP-3 mechanically true but subordinate.** Profit factor defaults
  to 0.0 when both wins and losses are empty (PF < 0.50 mechanically),
  but CFP-3's "catastrophic drawdown / PF<0.5" semantics presume a
  non-empty trade population. Subordinate to CFP-1 critical (which
  is the diagnostic root cause).
- **CFP-9 false.** Metrics OI exclusion fraction (~0.044%) is well
  below the 5% threshold.
- **CFP-10 false.** No optional ratio-column access; verified at
  three layers (static scan + metrics-loader explicit-column-list +
  runtime introspection).
- **CFP-11 false.** Per-bar exclusion algorithm matches Phase 4j §16
  pseudocode verbatim.
- **CFP-12 false.** No forbidden data access; verified at the
  import-list and runtime-introspection layers.
- **All other CFPs false.**
- **Verdict C driven by CFP-1 critical.**

## Verification evidence

| Check | Result |
|---|---|
| `python --version` | `Python 3.12.4` |
| `ruff check .` (whole repo) | `All checks passed!` |
| `pytest` | `785 passed in 14.73s` |
| `mypy --strict src/prometheus` | `Success: no issues found in 82 source files` |
| Optional ratio name static scan | `Forbidden ratio names in script: []; Pass: True` |
| Phase 4l backtest exit code | `0` |

Whole-repo quality gates remain **fully clean** at Phase 4l merge.
No regressions relative to the post-Phase-4k-merge baseline.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4m / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched,
  or commenced.
- **No V2 implementation under `src/prometheus/strategy/`.**
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
- **No data acquired.** No public Binance endpoint consulted in
  code.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage.
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** No network I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
- **No strategy rescue proposal.**
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
- **No `data/research/phase4l/**` outputs committed.** Local
  gitignored only.
- **No `.claude/scheduled_tasks.lock` committed.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A all preserved.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4j §11 metrics OI-subset governance modification.**
- **No Phase 4k V2 backtest-plan methodology modification.**
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
- **No optional ratio-column access.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused**. Phase 4l is now part of `main`.
- **Phase 4l output:** docs-and-code merge artefacts (one standalone
  research script + Phase 4l execution report + Phase 4l closeout +
  this merge-closeout file + narrow Phase 4l sync of
  `docs/00-meta/current-project-state.md`).
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4l).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a through Phase 4l all
  merged. **V2 first-spec terminally HARD REJECTED.**
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Metrics OI-subset partial-eligibility governance:** Phase 4j §11
  (preserved verbatim; honored exactly by Phase 4l).
- **V2 backtest methodology governance:** Phase 4k (preserved
  verbatim; honored exactly by Phase 4l).
- **V2 first-spec terminal verdict:** Phase 4l Verdict C HARD
  REJECT.
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared (Phase 4f) +
  operationalized (Phase 4g) + data-requirements (Phase 4h) + data
  acquired (Phase 4i, partial-pass) + governance binding (Phase 4j) +
  backtest-plan binding (Phase 4k) + executed (Phase 4l) →
  **Verdict C HARD REJECT, terminal for V2 first-spec**. V2 retained
  as research evidence only; non-leading; no V2 rescue authorized.
- **OPEN ambiguity-log items after Phase 4l:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  **V2 HARD REJECT (Phase 4l, structural CFP-1 critical, terminal
  for V2 first-spec)**; §11.6 = 8 bps HIGH per side; §1.7.3
  project-level locks; mark-price stops; v002 verdict provenance;
  Phase 3q mark-price 5m manifests `research_eligible: false`. All
  preserved.
- **Branch state:** `phase-4l/v2-backtest-execution` exists locally
  and on `origin/phase-4l/v2-backtest-execution`. The branch is now
  merged into `main`.

## Operator decision menu

The next operator decision is operator-driven only.

### Option A — Remain paused (PRIMARY RECOMMENDATION)

Take no further action. Phase 4l methodology + execution evidence
is recorded in `main`; V2 first-spec Verdict C HARD REJECT is
terminal. The current cumulative project state across V1 / R3
baseline-of-record, R1a / R1b-narrow / R2 / F1 / D1-A retained
research evidence, and now V2 HARD REJECT means there is no
live-deployable strategy candidate in the project. Remain paused
respects this finding without a hasty next-direction commitment.

### Option B — Docs-only post-V2 research consolidation memo (CONDITIONAL SECONDARY)

Authorize a separate docs-only memo analogous to Phase 3e (post-F1)
or Phase 3k (post-D1-A) that consolidates V2 research findings,
records what was learned, and explicitly identifies what cannot be
salvaged without violating the Phase 3t §12 validity gate. This memo
would NOT propose a V2 rescue or V2-prime — it would be retrospective
research consolidation only.

### Option C — Fresh-hypothesis research direction (NOT RECOMMENDED before consolidation)

Per Phase 3t §14.2 / Phase 3u §14, fresh-hypothesis research is
**paused** as the cumulative recommendation. Authorizing a new
ex-ante hypothesis (subject to the §12 validity gate) before
consolidating V2 findings risks rhetorical drift toward V2 rescue
framing. NOT RECOMMENDED before Option B.

### Option D — Phase 4j / Phase 4g / stop-distance / threshold amendment (REJECTED)

Modifying Phase 4j §11 governance, Phase 4g §29 threshold grid, the
stop-distance bounds 0.60–1.80 × ATR, the N1 axis values {20, 40},
or any other Phase 4g / Phase 4k locked selection in response to
the observed V2 outcome would be parameter rescue (Bailey et al.
2014). REJECTED.

### Option E — V2 implementation (REJECTED)

V2 implementation requires successful backtest evidence. Verdict C
HARD REJECT precludes implementation authorization. REJECTED.

### Option F — Paper / shadow / live-readiness / exchange-write (FORBIDDEN)

Per `docs/12-roadmap/phase-gates.md`, none of these gates is met.
FORBIDDEN.

## Next authorization status

**No next phase has been authorized.** Phase 4l's recommendation is
**Option A (remain paused) as primary**, with **Option B (docs-only
post-V2 research consolidation memo, analogous to Phase 3e / Phase
3k) as conditional secondary**.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.
