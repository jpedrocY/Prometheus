# Phase 4am — Exit Architecture Backtest-Logic Audit

## 1. Purpose and Non-Authorization

Phase 4am is the **narrow audit-only successor** contemplated by
Phase 4al §11.A and Phase 4al Decision Menu Option D. Phase 4am
performs a docs-only inspection of the backtest scripts and reports
already in the repository against the §11.A audit subjects defined
by Phase 4al.

Phase 4am explicitly does **NOT**:

- run any strategy backtest,
- compute full retained-population MFE / MAE / time-to-MFE /
  time-to-stop forensic distributions (Phase 4al §11.B and Option C
  scope; not authorized),
- tune or optimize any TP / SL / break-even / trailing /
  partial-exit / time-exit parameter,
- rescue any prior strategy candidate,
- revise any historical verdict,
- modify any source module under `src/prometheus/`,
- modify any existing backtest script,
- modify any test,
- modify any data file,
- modify any manifest,
- create `v003` or any other dataset version,
- acquire 5m / 1m / aggTrades / tick data,
- call `data.binance.vision`, exchange APIs, public endpoints in
  code, private endpoints, user streams, WebSockets, MCP, Graphify,
  `.mcp.json`, credentials, or production keys,
- prepare paper / shadow / live-readiness / deployment / exchange-
  write / production-key work,
- authorize Phase 4an or any successor phase.

## 2. Authority and Inputs Reviewed

### 2.A Governance and methodology documents (read verbatim)

- `docs/00-meta/m0-mechanism-admissibility-gate.md` (Phase 4ak
  binding M0 gate; cooled-down families list; post-null cooldown
  rule; M0 memo template).
- `docs/00-meta/implementation-reports/
  2026-05-06_phase-4al_exit-architecture-trade-management-m0-
  admissibility.md` (Phase 4al §11.A in-scope subjects; §11.B
  exclusions; §13 future Phase 4am boundary).
- `docs/00-meta/implementation-reports/
  2026-04-30_phase-4k_v2-backtest-plan-memo.md` (Phase 4k V2
  cost / funding model; cost cells; §11.6 promotion gate).
- `docs/00-meta/implementation-reports/
  2026-04-30_phase-4q_g1-backtest-plan-memo.md` (Phase 4q G1
  cost / funding implementation plan; sizing / exposure plan;
  governance labels).
- `docs/00-meta/implementation-reports/
  2026-04-30_phase-4w_c1-backtest-plan-memo.md` (Phase 4w C1
  cost model implementation plan; funding excluded from C1 first-
  spec; governance labels).
- `docs/00-meta/implementation-reports/
  2026-04-30_phase-3v_gap-20260424-032-stop-trigger-domain-
  resolution.md` (Phase 3v §8 stop-trigger-domain governance; the
  four valid label values; `mixed_or_unknown` fail-closed rule).
- `docs/00-meta/implementation-reports/
  2026-04-30_phase-3w_remaining-ambiguity-log-resolution.md`
  (Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation
  governance; per-candidate historical provenance).
- `docs/00-meta/implementation-reports/
  2026-04-30_phase-4l_v2-backtest-execution.md` (Phase 4l V2 report;
  Verdict C HARD REJECT context).
- `docs/00-meta/implementation-reports/
  2026-04-30_phase-4r_g1-backtest-execution.md` (Phase 4r G1 report;
  Verdict C HARD REJECT context).
- `docs/00-meta/implementation-reports/
  2026-04-30_phase-4x_c1-backtest-execution.md` (Phase 4x C1 report;
  Verdict C HARD REJECT context).

### 2.B Backtest scripts inspected

- `scripts/phase4l_v2_backtest.py` (V2; 2 449 lines).
- `scripts/phase4r_g1_backtest.py` (G1; 2 997 lines).
- `scripts/phase4x_c1_backtest.py` (C1; 3 338 lines).

### 2.C Phase 4al §11.A scope (in-scope subjects; verbatim)

The audit covers the eleven §11.A subjects:

```text
§11.A.1   Fee handling
§11.A.2   Slippage handling
§11.A.3   Funding handling
§11.A.4   Stop / TP sequencing
§11.A.5   Stop-trigger-domain governance
§11.A.6   Partial-exit logic
§11.A.7   Break-even logic
§11.A.8   Trailing-exit logic
§11.A.9   Time-exit logic
§11.A.10  Realized-R-after-costs accounting
§11.A.11  Intrabar ambiguity
```

### 2.D Phase 4al §11.B exclusions (out of scope; verbatim)

```text
§11.B.1   Modify the existing backtest scripts
§11.B.2   Modify any project lock or rule
§11.B.3   Revise any verdict on the basis of audit findings
§11.B.4   Optimize any parameter
§11.B.5   Run a new backtest
§11.B.6   Touch credentials, MCP, Graphify, .mcp.json, exchange-
          write paths, paper / shadow runtime, live-readiness
          scaffolding
```

## 3. Audit Method

### 3.A Method per item

For each §11.A subject:

1. **Expected rule.** Read verbatim from the relevant Phase 4k /
   4q / 4w plan memo (and Phase 3v / 3w governance documents where
   applicable). Cross-reference Phase 4g / 4p / 4v strategy specs
   when the plan memo refers to them.
2. **Code inspection.** Locate the relevant section of the
   corresponding backtest script via `Grep` and `Read`. Quote line
   ranges; do not paraphrase critical formulas.
3. **Cross-script consistency.** Compare V2 / G1 / C1 implementation
   for the same subject. Where the three scripts diverge, report
   the divergence and assess materiality.
4. **Synthetic micro-cases.** None were required for this audit.
   No helper script was created. All findings are derivable from
   direct code / spec inspection.
5. **Result.** Classify per §6 of this memo.

### 3.B No backtest re-execution

This audit operates only on the **already-merged** scripts and
reports. No backtest was re-executed. No script was modified. No
test was modified. No new analysis output was produced.

## 4. Scope Exclusions

This audit explicitly excludes:

- **Full retained-population MFE / MAE forensics.** Phase 4al
  Option C / §11.A.10 path-distribution analysis is not part of
  Phase 4am. Trade ledgers were not opened or aggregated.
- **Lower-timeframe data acquisition.** Phase 4al §14 records
  5m as the recommended first path-resolution layer if such work
  is ever authorized. Phase 4am does not acquire 5m / 1m /
  aggTrades / tick data and does not authorize their acquisition.
- **Strategy rescue and parameter optimization.** Phase 4al §9.A
  forbidden activities are honored in full.
- **Verdict revision.** Phase 4al §9.A.4 prohibition is honored.
- **Lock revision.** §11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p,
  Phase 4q, Phase 4v, Phase 4w, M0 governance all preserved
  unchanged.

## 5. Audit Matrix

The audit matrix below applies to each §11.A subject. File
references use the form `scripts/<file>.py:<line>`.

### 5.A.1 Fee handling

**Expected rule (Phase 4k §"Cost cells" / Phase 4q §"Cost and
funding model implementation plan" / Phase 4w §"Cost model
implementation plan").** Taker fee = 4 bps per side for USDⓈ-M
futures; no maker rebates; no live-fee assumption; fees applied
to entry and exit legs.

**Evidence.**

- All three scripts declare `TAKER_FEE_PER_SIDE_BPS = 4.0` as a
  module-level constant.
  - V2: `scripts/phase4l_v2_backtest.py:84`.
  - G1: `scripts/phase4r_g1_backtest.py:83`.
  - C1: `scripts/phase4x_c1_backtest.py:82`.
- G1 and C1 apply fees as part of `(slip_bps + TAKER_FEE_PER_SIDE_BPS) / 10_000`
  in `_apply_costs_long` / `_apply_costs_short`, applied to both
  entry and exit legs symmetrically:
  - G1: `scripts/phase4r_g1_backtest.py:913-921`.
  - C1: `scripts/phase4x_c1_backtest.py:687-698`.
- V2 sums fee + slip into `fee_bps_per_side` and computes round-
  trip cost, applied as `fee_round_trip_frac × entry_price /
  initial_R`:
  - V2: `scripts/phase4l_v2_backtest.py:1078-1079, 1142-1158`.
- No maker rebate is assumed in any script (no maker code path
  exists).

**Result.** **PASS** for taker-fee value; **PASS** for absence of
maker rebate; **PASS** for absence of live-fee assumption; **PASS
WITH LIMITATION** for the V2 round-trip approximation versus the
G1 / C1 executed-price-shifting formula (see §5.A.10 below for the
materiality assessment).

**Future action.** None required at the audit layer; documented
in §5.A.10 as a non-material V2/G1/C1 cost-application formula
divergence.

### 5.A.2 Slippage handling

**Expected rule (Phase 4k / Phase 4q / Phase 4w cost model).**
Cost cells per side:
- LOW = 1 bp;
- MEDIUM = 4 bps;
- HIGH = 8 bps (§11.6 promotion gate).
Round-trip cost = 2 × (taker_fee + slippage) per side. HIGH = 8
bps per side; round-trip = 24 bps including fees (4 + 4 + 8 + 8).
Slippage applied per side, in the adverse direction (entry slips
up for long; entry slips down for short; exit mirror).

**Evidence.**

- All three scripts declare:
  ```python
  COST_CELL_LOW_SLIP_BPS    = 1.0
  COST_CELL_MEDIUM_SLIP_BPS = 4.0
  COST_CELL_HIGH_SLIP_BPS   = 8.0
  ```
  - V2: `scripts/phase4l_v2_backtest.py:85-87`.
  - G1: `scripts/phase4r_g1_backtest.py:85-87`.
  - C1: `scripts/phase4x_c1_backtest.py:85-87`.
- G1 and C1 apply slippage adversely per side via the executed-
  price formula (entry inflated for long; exit deflated for long;
  short mirror). G1: `scripts/phase4r_g1_backtest.py:913-921`. C1:
  `scripts/phase4x_c1_backtest.py:687-698`.
- V2 absorbs slippage into the round-trip cost via
  `fee_bps_per_side = TAKER_FEE_PER_SIDE_BPS + cost_cell_slip_bps`
  and `fee_round_trip_frac = 2 × fee_bps_per_side / 10000`. The
  HIGH cell yields `fee_bps_per_side = 12` and
  `fee_round_trip_frac = 0.0024 = 24 bps`, matching the spec's
  round-trip total. V2: `scripts/phase4l_v2_backtest.py:1078-1079`.

**Result.** **PASS** for all three scripts on per-side bps values
and round-trip totals. **PASS** for adverse-direction application
in G1 / C1 (explicit). **PASS WITH LIMITATION** for V2's flat-
`entry_price` approximation (see §5.A.10).

**Future action.** None required at the audit layer.

### 5.A.3 Funding handling

**Expected rule.**

- **V2 (Phase 4k §"Funding cost").** Funding cost MUST be
  included in P&L. Funding accrual occurs at funding events (8 h
  cadence on Binance USDⓈ-M). For each open V2 position spanning
  a funding event, the position is debited / credited per published
  funding rate × position notional × funding fraction. Funding
  recorded per-trade and reported in aggregate.
- **G1 (Phase 4q §"Cost and funding model implementation plan").**
  Funding cost included; applied at every completed funding event
  the position spans, not at trade-close-only. Spec formula:
  `funding_cost_per_event(side, fr, notional) = +fr × notional`
  for LONG and `-fr × notional` for SHORT. Spec sign convention:
  positive funding rate ⇒ longs pay shorts. Funding events
  strictly between entry_open_time and exit_realized_time.
- **C1 (Phase 4w §"Cost model implementation plan").** Funding
  **excluded** from C1 first-spec trade R. (Spec note: positions
  are short enough that funding-rate impact is small relative to
  slippage + fees.)

**Evidence.**

- **V2 funding inclusion.** V2 includes funding via two helpers
  `funding_cost_R_long` / `funding_cost_R_short`:
  `scripts/phase4l_v2_backtest.py:1190-1213`. Sign convention:
  long pays funding when sum_rates > 0 (cost > 0 reduces realized
  R via `realized = r_gross - cost_R - f_cost_R`). Short receives
  when sum_rates > 0 (`f_cost_R = -sum_rates × ep / R` is
  negative, so `realized = r_gross - cost_R - negative` adds the
  credit). ✓ matches spec sign convention.

  - **Sub-finding.** V2 funding-event boundary uses
    `searchsorted(..., entry_ms, side="right")` to
    `searchsorted(..., exit_ms, side="right")`, which yields the
    half-open interval `(entry_ms, exit_ms]`. Phase 4k spec wording
    is "funding events spanning the position" without strict-
    versus-inclusive specification; Phase 4q spec for G1 uses
    *strictly between* `(entry_ms, exit_ms)`. V2 is therefore
    inclusive on the right boundary while G1 is strict. Funding
    events occur at 00:00 / 08:00 / 16:00 UTC; 30m bars open at
    HH:00 / HH:30, so the right boundary is occasionally hit
    exactly. Affected fraction is a small subset of trade exits.

- **G1 funding inclusion.** G1 implements the per-event accrual
  exactly per spec: `_funding_cost_R` selects events strictly
  inside `(entry_time_ms, exit_time_ms)`:
  `scripts/phase4r_g1_backtest.py:878-910`. Sign convention via
  `sign = +1.0 if side == "long" else -1.0` and
  `cost_R = -cost_per_event / (position_size_units × R_per_unit)`
  yields the correct economic direction (verified by walking the
  long-pays-positive-rate case).

- **C1 funding exclusion.** C1 has **no funding code path** in
  `simulate_trades_for_signal_array`:
  `scripts/phase4x_c1_backtest.py:706-865`. Funding is not loaded;
  the funding loader is documented as "NOT INVOKED by Phase 4x"
  in the Phase 4w spec. Realized R is `raw_R` from
  `_apply_costs_*` only; no `+ fc_R` term. ✓ matches Phase 4w.

**Result.**

- V2 funding inclusion: **PASS** for inclusion and sign
  convention; **DEFECT_NON_MATERIAL** for the right-boundary
  inclusivity divergence from G1's strict-between convention.
  Phase 4k spec did not specify boundary handling explicitly, so
  this is closer to a **DOCUMENTATION_LIMITATION** than an
  implementation defect. Materiality is bounded by the funding
  rate magnitude per event (typically a few bps annualized) times
  the small fraction of trades where exit timestamps coincide
  exactly with a funding-event timestamp.
- G1 funding inclusion: **PASS** for boundary handling, sign
  convention, and per-event accrual.
- C1 funding exclusion: **PASS** — matches Phase 4w spec
  verbatim. Documented limitation, not a defect.

**Future action.** None required at the audit layer for V2 / G1.
The V2 boundary divergence is recorded as a documentation
limitation; future memos may want to harmonize the convention if
funding-sensitive analysis is ever undertaken.

### 5.A.4 Stop / TP sequencing

**Expected rule (Phase 4k / 4q / 4w).** Precedence: stop > TP >
time-stop. Same-bar stop / TP ambiguity: stop wins (conservative
tie-break).

**Evidence.**

- **V2.** `scripts/phase4l_v2_backtest.py:1227-1248`:
  ```python
  # Conservative tie-break: stop wins
  ...
  if stop_hit:
      close_position(i, stop_price, "stop")
  elif tp_hit:
      close_position(i, tp_price, "take_profit")
  elif bars_since_entry >= variant.t_stop:
      close_position(i + 1, ..., "time_stop")
  ```
  ✓ stop > TP > time-stop precedence; stop-first tie-break.
- **G1.** `scripts/phase4r_g1_backtest.py:974-989`:
  ```python
  exit_kind: str | None = None
  if stop_touched:
      exit_kind = "stop"
      exit_p = stop_price
  elif tp_touched:
      exit_kind = "take_profit"
      exit_p = tp_price
  elif time_due:
      exit_kind = "time_stop"
      ...
  ```
  ✓ same precedence and tie-break.
- **C1.** `scripts/phase4x_c1_backtest.py:760-775`: identical
  pattern (`stop > target > time-stop`). C1 docstring at
  `scripts/phase4x_c1_backtest.py:721-722` states this verbatim.
  ✓ same precedence and tie-break.

**Result.** **PASS** in all three scripts.

**Future action.** None.

### 5.A.5 Stop-trigger-domain governance

**Expected rule (Phase 3v §8).** Future evidence and runtime
artifacts must carry an explicit `stop_trigger_domain` label with
valid values:

```text
trade_price_backtest | mark_price_runtime | mark_price_backtest_candidate
```

`mixed_or_unknown` is invalid and fails closed. For Phase 4k / 4q /
4w research backtests, the label must be `trade_price_backtest`.

**Evidence.**

- **Behavioural conformance.** All three scripts use kline
  `low <= stop_price` (long) / `high >= stop_price` (short) for
  stop-hit detection — i.e., trade-price domain. None reads a
  mark-price series. None applies a `mark_price_runtime` or
  `mark_price_backtest_candidate` label.
  - V2: `scripts/phase4l_v2_backtest.py:1230-1239`.
  - G1: `scripts/phase4r_g1_backtest.py:967-970`.
  - C1: `scripts/phase4x_c1_backtest.py:748-756`.
- **Label recording.** Only **C1** writes the four governance
  labels into `run_metadata.json` artefacts:
  `scripts/phase4x_c1_backtest.py:2495-2498`:
  ```python
  "stop_trigger_domain": "trade_price_backtest",
  "break_even_rule": "disabled",
  "ema_slope_method": "not_applicable",
  "stagnation_window_role": "not_active",
  ```
  V2 and G1 **do not** record any of these four labels in their
  `run_metadata.json` (verified by `grep` across the two scripts;
  zero matches for `stop_trigger_domain`, `break_even_rule`,
  `ema_slope_method`, `stagnation_window_role`).
- **`mixed_or_unknown`.** No script accepts `mixed_or_unknown`;
  no decision branch reads any label at runtime.

**Result.**

- Behavioural conformance: **PASS** in all three scripts (all
  operate in the trade-price domain).
- Label recording in artefacts: **DOCUMENTATION_LIMITATION** in
  V2 and G1 (the four governance labels are documented in the
  Phase 4k / 4q / 4w plan memos but not surfaced as machine-
  readable artefact fields). C1 sets the better pattern.
- `mixed_or_unknown` enforcement: **PASS** — there is no decision
  path that could even read the label, so structural fail-closed is
  trivially satisfied.

**Future action.** None at the audit layer. A future docs-only
correction phase could choose to write the four labels into V2
and G1 `run_metadata.json` for parity with C1 if desired; this
would not change any historical verdict.

### 5.A.6 Partial-exit logic

**Expected rule.** Phase 4g / 4p / 4v strategy specs do **not**
authorize partial exits; Phase 4k / 4q / 4w plan memos confirm
this.

**Evidence.** `Grep` for `partial` across the three scripts
returned only documentation-string mentions and a Phase 4j §11
metrics-OI partial-eligibility reference — no partial-exit code
path. Each `simulate_trades*` function exits the entire position
in a single `close_position` / record append call.

**Result.** **PASS** — partial exits are absent in all three
scripts, consistent with the documented absence in spec.

**Future action.** None.

### 5.A.7 Break-even logic

**Expected rule (Phase 3w §6).** Per-candidate historical
provenance:
- H0 / R1a / R1b-narrow / R2: `break_even_rule = enabled_plus_1_5R_mfe`;
- R3 (baseline-of-record): `break_even_rule = disabled`;
- F1 / D1-A: `break_even_rule = disabled`;
- V2 (Phase 4g): `break_even_rule = disabled`;
- G1 (Phase 4p): `break_even_rule = disabled`;
- C1 (Phase 4v): `break_even_rule = disabled`.

**Evidence.** `Grep` for `break_even` / `breakeven` across the
three Phase 4 scripts returned no implementation. C1 records
`"break_even_rule": "disabled"` in `run_metadata.json`
(`scripts/phase4x_c1_backtest.py:2496`); V2 and G1 do not record
the label but have no implementation either. The behavioural
state is "no break-even movement" in all three.

**Result.** **PASS** behavioural conformance for all three
(`disabled` matches V2 / G1 / C1 specs). **DOCUMENTATION_LIMITATION**
on V2 / G1 label recording (see §5.A.5).

**Future action.** None.

### 5.A.8 Trailing-exit logic

**Expected rule.** Phase 4g / 4p / 4v specs do not authorize
trailing exits. Phase 4k / 4q / 4w plan memos confirm this.

**Evidence.** `Grep` for `trail` across the three scripts returned
only references to "trailing distribution / lookback" in
percentile-window code (not exit-management trailing). No
trailing-stop-update code path exists. C1 docstring at
`scripts/phase4x_c1_backtest.py:724` states "No break-even. No
trailing. No regime exit." explicitly.

**Result.** **PASS** — trailing exits are absent in all three
scripts.

**Future action.** None.

### 5.A.9 Time-exit logic

**Expected rule (Phase 4k / 4q / 4w).**
- V2: `T_stop ∈ {12, 16}` 30m bars, axis 9 of grid.
- G1: `T_stop = 16` 30m bars (fixed).
- C1: `T_stop_bars = 2 × N_comp` 30m bars (structurally tied).
- All three: time-stop exits at next 30m bar's open, or at current
  bar's close at end-of-data.
- Precedence: stop > TP > time-stop.

**Evidence.**

- **V2.** `scripts/phase4l_v2_backtest.py:1244-1248`:
  ```python
  elif bars_since_entry >= variant.t_stop:
      if i + 1 < n:
          close_position(i + 1, float(open_p[i + 1]), "time_stop")
      else:
          close_position(i, float(f.close_30m[i]), "time_stop")
  ```
  ✓ next-bar-open exit; close-of-current at end-of-data;
  precedence respected.
- **G1.** `scripts/phase4r_g1_backtest.py:982-989`:
  ```python
  elif time_due:
      if i + 1 < n_30m:
          exit_kind = "time_stop"
          exit_p = f.open_30m[i + 1]
      else:
          exit_kind = "time_stop"
          exit_p = f.close_30m[i]
  ```
  ✓ same.
- **C1.** `scripts/phase4x_c1_backtest.py:769-775`: identical
  pattern. ✓ same.
- Bar-count semantics: all three define `bars_in_trade = i -
  entry_idx` and trigger when `>= T_stop`. With `entry_idx = i+1`
  set at signal bar, the time-stop fires after exactly `T_stop`
  bars in trade, consistent across all three scripts.

**Result.** **PASS** in all three scripts for time-stop bar count,
exit price, and precedence.

**Future action.** None.

### 5.A.10 Realized-R-after-costs accounting

**Expected rule (Phase 4w §"Cost model implementation plan",
generalizing).** For LONG:
```text
long_entry_executed = entry_price × (1 + cost_factor)
long_exit_executed  = exit_price  × (1 - cost_factor)
R_after_costs       = (long_exit_executed - long_entry_executed)
                      / (entry_price - stop_price)
```
For SHORT: mirror. Initial R denominator uses the **original
(pre-cost) stop distance**, preserving R as a normalized stop-
distance multiple. Funding cost included for V2 / G1; excluded
for C1.

**Evidence.**

- **G1 implementation (matches Phase 4q spec verbatim).**
  `scripts/phase4r_g1_backtest.py:913-921, 994-1008`:
  ```python
  def _apply_costs_long(entry, exit_p, slip_bps):
      cost = (slip_bps + TAKER_FEE_PER_SIDE_BPS) / 10_000.0
      return entry * (1.0 + cost), exit_p * (1.0 - cost)
  ...
  eep, exp_ = _apply_costs_long(entry_price, exit_p, slip_bps)
  raw_R = (exp_ - eep) / R_per_unit       # uses pre-cost R
  ...
  realized_R = float(raw_R + fc_R)        # add funding term
  ```
  `R_per_unit = ep - sp` is computed before any cost is applied.
  ✓ matches Phase 4q.

- **C1 implementation (matches Phase 4w spec verbatim).**
  `scripts/phase4x_c1_backtest.py:687-698, 778-808`. Same formula
  as G1; no `+ fc_R` (funding excluded).
  ```python
  R_unit = ep - sp                        # pre-cost R
  ...
  eep, exp_ = _apply_costs_long(entry_price, exit_p, slip_bps)
  raw_R = (exp_ - eep) / R_per_unit
  ...
  realized_R=float(raw_R)                 # no funding term
  ```
  ✓ matches Phase 4w.

- **V2 implementation (uses a flat-`entry_price` approximation).**
  `scripts/phase4l_v2_backtest.py:1078-1079, 1136-1158`:
  ```python
  fee_bps_per_side    = TAKER_FEE_PER_SIDE_BPS + cost_cell_slip_bps
  fee_round_trip_frac = 2.0 * fee_bps_per_side / 10000.0
  ...
  cost_R = fee_round_trip_frac * entry_price / initial_R
  realized = r_gross - cost_R - f_cost_R
  ```
  This computes the round-trip cost as `2 × per-side-bps × entry_price`
  and converts to R units via `/ initial_R`. By comparison, the
  exact executed-price formula computes
  `(entry_price + exit_price) × per-side-bps / initial_R`.
  V2's approximation uses `2 × entry_price` instead of
  `entry_price + exit_price`, so it overcharges the exit leg by
  `(entry_price − exit_price) × per-side-bps / initial_R` for stops
  (where exit < entry for long) and undercharges by
  `(exit_price − entry_price) × per-side-bps / initial_R` for TPs
  (where exit > entry for long). Magnitude bound, per trade, in
  units of R:
  ```text
  |error| <= 2 × N_R × per_side_bps / 10000
  ```
  For HIGH (12 bps per side) and N_R = 2.0 (V2 axis), the bound
  per TP-hit trade is ≈ 0.0048 R = 0.48% of R. For stop-hit trades
  it is ≈ 0.0024 R = 0.24% of R. Population-averaged, the error
  partially cancels (over- and under-charges on opposite-direction
  exits).

  **Materiality assessment.** Phase 4l V2 verdict (Verdict C HARD
  REJECT) was driven by CFP-1 critical (zero qualifying trades on
  any of 512 variants). The cost-application formula choice does
  not affect a 0-trade verdict. Therefore the formula divergence
  is **non-material to the V2 verdict**.

  **Spec conformance.** Phase 4k did **not** specify the
  executed-price-shifting formula explicitly (it only specified
  per-side bps and round-trip totals). V2's approximation is
  consistent with Phase 4k's stated round-trip cost level (24 bps
  HIGH = 4 + 4 + 8 + 8) at the population-average level. The
  formula divergence is therefore an **implementation choice**
  permitted by the Phase 4k spec wording, not a defect against
  the spec. The G1 / C1 executed-price formula is more precise per-
  trade but the project did not specify the precision level
  required.

- **R denominator in all three scripts** uses the pre-cost stop
  distance (`initial_R = entry_price - stop_price` for long;
  mirror for short), preserving R as a normalized stop-distance
  multiple. ✓ matches Phase 4w spec for all three scripts.

- **Sign handling for long vs short** is correct in all three
  scripts:
  - V2 long: `gross = exit_price - entry_price`; short: `gross =
    entry_price - exit_price`. ✓.
  - G1 long: `raw_R = (exp_ - eep) / R_per_unit`; short: `raw_R =
    (eep - exp_) / R_per_unit`. ✓.
  - C1 same as G1. ✓.

**Result.**

- G1 / C1 realized-R-after-costs accounting: **PASS** — matches
  Phase 4q / 4w spec verbatim.
- V2 realized-R-after-costs accounting: **PASS_WITH_LIMITATION**
  — V2 uses a flat-`entry_price` round-trip approximation that
  diverges from G1 / C1's executed-price-shifting formula. The
  divergence is bounded at `≤ 2 × N_R × per_side_bps / 10000`
  per trade (≤ 0.48% of R per TP at HIGH N_R = 2.0), is not a
  defect against the Phase 4k spec wording (which specified per-
  side bps and round-trip totals but not the executed-price
  formula), and is **non-material to the Phase 4l V2 verdict
  (Verdict C HARD REJECT, CFP-1 critical, zero qualifying trades).**

**Future action.** None at the audit layer. A future docs-only
methodology-harmonization memo could choose to specify the
executed-price-shifting formula prospectively for any future
Phase 4-style backtest, mirroring Phase 4q / 4w. Phase 4am does
not propose this.

### 5.A.11 Intrabar ambiguity

**Expected rule (Phase 4k / 4q / 4w).** Same-bar stop / TP cases
resolved as **stop-first conservative**.

**Evidence.**

- All three scripts check `stop_touched`/`stop_hit` first via an
  `if stop_*: ... elif tp_*: ...` branch. When both flags are
  true (intrabar straddle), only the stop branch fires.
  - V2: `scripts/phase4l_v2_backtest.py:1240-1243`.
  - G1: `scripts/phase4r_g1_backtest.py:976-981`.
  - C1: `scripts/phase4x_c1_backtest.py:762-768` (with explicit
    code comment "Same-bar stop+target ambiguity: stop wins
    (conservative).").

**Sub-finding — entry-bar exit handling divergence (V2 vs G1 / C1).**

- **V2** guards exit evaluation with `if i > entry_idx:`
  (`scripts/phase4l_v2_backtest.py:1218`). With
  `entry_idx = i + 1` set at the signal bar, the exit loop skips
  exit checking on the entry bar itself (when the loop index
  reaches the entry bar, the guard is `entry_idx + 0 > entry_idx`,
  which is false). V2 therefore **cannot exit on the entry bar**.
- **G1** does not have this guard (`scripts/phase4r_g1_backtest.py:964-989`).
  When the loop reaches `i = entry_idx`, `bars_in_trade = 0` and
  the high / low of the entry bar are evaluated for stop / TP
  hits. G1 **can exit on the entry bar**.
- **C1** does not have this guard either (`scripts/phase4x_c1_backtest.py:745-775`).
  Same behaviour as G1: **can exit on the entry bar**.

The relevant plan memos (Phase 4k / 4q / 4w) do not explicitly
specify whether intrabar exits on the entry bar itself are
allowed. Both behaviours are defensible; V2 is more conservative
(it cannot capture an entry-bar TP nor be hit by an entry-bar
stop), G1 / C1 are symmetric (they can capture either).

**Materiality assessment.**

- V2 verdict (Verdict C HARD REJECT) was driven by zero qualifying
  trades; entry-bar handling cannot affect a 0-trade outcome.
- G1 verdict (Verdict C HARD REJECT) was driven by zero G1 trades
  (regime-gate × setup sparseness); same.
- C1 verdict (Verdict C HARD REJECT, mean_R = −0.36 BTC OOS HIGH)
  was driven by negative expectancy across 149 trades; if entry-
  bar exits had been excluded, the trade count would have been
  approximately the same (most exits do not occur on the entry
  bar). The C1 verdict's mean_R = −0.36 R is large enough that
  any small fraction of entry-bar exits could not flip the
  verdict.

The divergence is therefore **non-material to all three reported
verdicts**.

**Result.**

- Same-bar stop / TP tie-break: **PASS** in all three scripts.
- Entry-bar exit handling: **DEFECT_NON_MATERIAL** — V2 and G1 / C1
  diverge on whether exits may fire on the entry bar. The
  divergence is not a defect against any plan-memo specification
  (because none specifies the behaviour), but it is a structural
  inconsistency across the three scripts. Non-material to the
  three reported verdicts.

**Future action.** None at the audit layer. A future docs-only
methodology-harmonization memo could choose to specify entry-bar
exit handling prospectively for any future Phase 4-style backtest.
Phase 4am does not propose this.

## 6. Defect Classification Model

Findings are classified per Phase 4al's instruction:

```text
CLEAN_BILL                          no defects
DOCUMENTATION_LIMITATION            documented spec gap or missing
                                    artefact field; no behavioural
                                    defect
IMPLEMENTATION_DEFECT_NON_MATERIAL  behavioural divergence from spec
                                    bounded in magnitude and shown
                                    not to affect the corresponding
                                    verdict
IMPLEMENTATION_DEFECT_MATERIAL      behavioural divergence from spec
                                    that could affect the corresponding
                                    verdict; requires future governance
                                    decision before any verdict review
GOVERNANCE_BLOCKED                  finding cannot be assessed without
                                    relaxing a binding governance
                                    constraint
NOT_AUDITABLE_FROM_REPO_STATE       script or artifact not present;
                                    inspection not possible
```

## 7. Audit Findings

### 7.A Aggregate finding

```text
AUDIT RESULT: DOCUMENTATION_LIMITATION

Sub-findings:
- Two DOCUMENTATION_LIMITATION items;
- Two IMPLEMENTATION_DEFECT_NON_MATERIAL items;
- Seven §11.A subjects: PASS (clean) across all three scripts.

No IMPLEMENTATION_DEFECT_MATERIAL findings.
No GOVERNANCE_BLOCKED findings.
No NOT_AUDITABLE_FROM_REPO_STATE findings.
```

### 7.B Per-subject summary table

| §11.A item | V2 (Phase 4l) | G1 (Phase 4r) | C1 (Phase 4x) |
|---|---|---|---|
| .1  Fee handling | PASS | PASS | PASS |
| .2  Slippage handling | PASS | PASS | PASS |
| .3  Funding handling | DEFECT_NON_MATERIAL (right-boundary inclusivity) | PASS | PASS (excluded per spec) |
| .4  Stop / TP sequencing | PASS | PASS | PASS |
| .5  Stop-trigger-domain governance | PASS behaviour; DOCUMENTATION_LIMITATION on label recording | PASS behaviour; DOCUMENTATION_LIMITATION on label recording | PASS |
| .6  Partial-exit logic | PASS (absent) | PASS (absent) | PASS (absent) |
| .7  Break-even logic | PASS behaviour; DOCUMENTATION_LIMITATION on label recording | PASS behaviour; DOCUMENTATION_LIMITATION on label recording | PASS |
| .8  Trailing-exit logic | PASS (absent) | PASS (absent) | PASS (absent) |
| .9  Time-exit logic | PASS | PASS | PASS |
| .10 Realized-R-after-costs accounting | PASS_WITH_LIMITATION (flat-`entry_price` approximation) | PASS | PASS |
| .11 Intrabar ambiguity (tie-break) | PASS | PASS | PASS |
| .11 Intrabar ambiguity (entry-bar exit handling) | DEFECT_NON_MATERIAL (V2 excludes; G1 / C1 include) | DEFECT_NON_MATERIAL | DEFECT_NON_MATERIAL |

### 7.C Per-finding detail

#### Finding F-1 — V2 funding-event right-boundary inclusivity

- **Affected file / function.** `scripts/phase4l_v2_backtest.py`,
  helpers `funding_cost_R_long` (lines 1190-1201) and
  `funding_cost_R_short` (lines 1203-1213).
- **Expected behaviour.** Phase 4q (G1) / Phase 4w (C1; funding
  excluded) specify *strictly between* `(entry_ms, exit_ms)`.
  Phase 4k (V2) does not specify the boundary explicitly.
- **Observed behaviour.** V2 uses `searchsorted(..., side="right")`
  for both endpoints, which yields the half-open interval
  `(entry_ms, exit_ms]`. A funding event at exactly `exit_ms` is
  included.
- **Why it matters.** Funding events occur at 00:00 / 08:00 /
  16:00 UTC; 30m bars open at HH:00 / HH:30, so a time-stop at
  exactly 16:00 (when 8 h of trade has elapsed since an 08:00
  entry) lines up with a funding event timestamp. V2 charges that
  funding event; G1's convention would not.
- **Could it affect realized R?** Yes, by at most one funding
  event per affected trade; per-event funding rate magnitude on
  BTCUSDT USDⓈ-M is typically `≤ 0.01%` (1 bp), giving an R
  impact of `≤ 0.0001 × entry_price / R_per_unit`. For a typical
  V2 stop distance of `~ 1.0 × ATR(20)`, R impact is `≤ 0.0001 ×
  entry_price / (1.0 × ATR(20))`. The scale of `entry_price /
  ATR(20)` for BTCUSDT 30m is in the few-hundreds range, so the
  per-affected-trade R impact is `≤ 0.05R` worst-case, with
  affected trades a small fraction of the population.
- **Material?** **No.** The Phase 4l verdict (Verdict C HARD
  REJECT, CFP-1 critical, zero qualifying trades on all 512
  variants) is unaffected by funding accounting because no
  trades survived the entry filter to be aggregated. Even if V2
  had produced trades, the boundary-inclusivity divergence affects
  only a small fraction of trades by at most a small fraction of R
  per affected trade.
- **Future action.** None required. A future docs-only
  methodology-harmonization memo could harmonize the boundary
  convention prospectively if funding-sensitive analysis is ever
  contemplated.

#### Finding F-2 — V2 cost-application formula approximation

- **Affected file / function.** `scripts/phase4l_v2_backtest.py`,
  `simulate_trades.close_position` (lines 1136-1158, particularly
  1146 / 1154).
- **Expected behaviour.** Phase 4k spec defines the cost cells
  per side and the round-trip totals (4 + 4 + 8 + 8 = 24 bps for
  HIGH) but does not specify the executed-price-shifting formula.
  Phase 4q (G1) and Phase 4w (C1) **do** specify the executed-
  price-shifting formula:
  ```text
  long_entry_executed = entry_price × (1 + cost_factor)
  long_exit_executed  = exit_price  × (1 - cost_factor)
  raw_R               = (long_exit_executed - long_entry_executed)
                        / (entry_price - stop_price)
  ```
  Both Phase 4q (later in time) and Phase 4w follow Phase 4k
  conceptually but pin down the per-trade formula.
- **Observed behaviour.** V2 uses
  `cost_R = fee_round_trip_frac × entry_price / initial_R`,
  treating both legs as if executed at `entry_price`. This is
  equivalent to the executed-price formula only if
  `exit_price ≈ entry_price`. Per-trade error bound (in R units):
  `≤ |exit_price − entry_price| × per_side_bps / 10000 / initial_R`.
  For TP at +N_R · R: error `≤ N_R × per_side_bps / 10000 ≈
  0.0024R` at HIGH per-side bps and N_R = 2. For stop at −1R:
  error `≈ 0.0012R`.
- **Could it affect realized R?** Yes, per-trade by a bounded
  small fraction of R, with sign depending on exit type.
- **Material?** **No.** Phase 4l verdict is CFP-1 critical (zero
  trades). Even at a hypothetical positive trade count, population-
  averaged the bias is small and partially cancelling.
- **Spec conformance.** Phase 4k did not require the executed-
  price formula. V2's flat approximation is consistent with the
  Phase 4k specification at the round-trip-total level. **This is
  better classified as `DOCUMENTATION_LIMITATION` than as a
  defect**, but the audit notes it as `PASS_WITH_LIMITATION`
  because the formula is observably less precise than the G1 / C1
  formulation that was adopted later.
- **Future action.** None required.

#### Finding F-3 — V2 / G1 missing governance-label artefacts

- **Affected files.** `scripts/phase4l_v2_backtest.py`
  (`run_metadata.json` writer, region around lines 2400-2440),
  `scripts/phase4r_g1_backtest.py:2440-2473` (`_write_run_metadata`).
- **Expected behaviour.** Phase 3v §8 + Phase 3w §6 / §7 / §8
  define four governance labels (`stop_trigger_domain`,
  `break_even_rule`, `ema_slope_method`, `stagnation_window_role`)
  whose values must be recorded for any future evidence and
  runtime artefacts. Phase 4q and Phase 4w spec memos declare the
  expected values for G1 and C1 respectively. C1 records all four
  in `run_metadata.json` (`scripts/phase4x_c1_backtest.py:2495-2498`).
- **Observed behaviour.** V2 and G1 do not record the four
  labels in their `run_metadata.json` artefacts (verified via
  `grep` returning zero matches across the two scripts).
- **Why it matters.** Behavioural conformance is intact (no
  break-even code; no trailing code; trade-price stop trigger; no
  partial exits; etc.), and the spec memos document the expected
  label values, so the governance is documented at the project
  level. The artefact gap is a machine-readable-audit-trail
  limitation rather than a behavioural defect.
- **Material?** **No.** No verdict depends on the artefact field
  presence.
- **Future action.** None required at the audit layer. A future
  docs-only correction phase could add the labels to V2 and G1
  `run_metadata.json` for parity with C1; this would not change
  any historical verdict.

#### Finding F-4 — Entry-bar exit handling divergence

- **Affected files.** `scripts/phase4l_v2_backtest.py:1218` (V2
  guard `if i > entry_idx:`); `scripts/phase4r_g1_backtest.py:964-989`
  (no guard); `scripts/phase4x_c1_backtest.py:745-775` (no guard).
- **Expected behaviour.** Plan memos do not specify entry-bar
  exit handling explicitly.
- **Observed behaviour.** V2 cannot exit on the entry bar; G1
  and C1 can (intrabar stop or TP on the entry bar's high / low
  triggers an immediate exit at the spot price = stop_price or
  tp_price).
- **Why it matters.** The three scripts use different
  conventions. If a future Phase 4am-style forensic phase wanted
  to compute MFE / MAE distributions starting from the entry
  bar, the V2 vs G1 / C1 difference would matter for the entry-
  bar slice of the distribution (V2 cannot record an entry-bar
  exit; G1 / C1 can).
- **Could it affect realized R?** Marginal at population level.
  For symmetric-payoff strategies (stops and TPs equally likely
  on the entry bar), the bias is small. For asymmetric (e.g.,
  breakouts where the entry bar tends to extend favourably), V2
  would systematically under-record TP-on-entry-bar trades and
  also under-record stop-on-entry-bar trades; the net direction
  depends on the distribution of entry-bar paths.
- **Material?** **No** to all three reported verdicts:
  - V2 / G1 zero-trade outcomes are unaffected (no exits to
    register on any bar).
  - C1's mean_R = −0.36 across 149 trades is too large to be
    flipped by the entry-bar slice.
- **Future action.** None at the audit layer. A future docs-only
  methodology-harmonization memo could specify entry-bar exit
  handling prospectively for any future Phase 4-style backtest.
  Phase 4am does not propose this.

## 8. Verdict Impact

Phase 4am explicitly does **NOT** revise any historical verdict.
All retained verdicts are preserved verbatim:

```text
H0:           FRAMEWORK ANCHOR
R3:           BASELINE-OF-RECORD
R1a:          RETAINED — NON-LEADING
R1b-narrow:   RETAINED — NON-LEADING
R2:           FAILED — §11.6
F1:           HARD REJECT
D1-A:         MECHANISM PASS / FRAMEWORK FAIL — other
5m thread:    OPERATIONALLY CLOSED per Phase 3t
V2:           HARD REJECT — terminal for V2 first-spec
G1:           HARD REJECT — terminal for G1 first-spec
C1:           HARD REJECT — terminal for C1 first-spec
```

None of the four findings (F-1 V2 funding boundary; F-2 V2 cost-
application approximation; F-3 V2 / G1 missing governance-label
artefacts; F-4 entry-bar exit handling divergence) are **material**
to any historical verdict. All were assessed against each affected
verdict; in every case the verdict driver (zero-trade outcome for
V2 / G1; large negative mean_R for C1) is too dominant for the
finding to flip.

No future governance decision is required *before* any verdict
could be reviewed: each finding is bounded in magnitude and is
non-material on its face. If a future operator chooses to
authorize a verdict-revision phase (separately authorized; not
contemplated by Phase 4am), the four findings here are recorded
inputs but do not, individually or in combination, suggest that a
verdict review would change any verdict.

**No verdict is revised by Phase 4am.**

## 9. Locks Impact

Phase 4am explicitly does **NOT** change any project lock. All
binding locks remain unchanged:

```text
§11.6:           8 bps per side; round-trip 16 bps slippage; +
                 4 bps per side taker fee; HIGH cell round-trip
                 24 bps total; HIGH cell is the promotion gate
§1.7.3:          0.25% risk per trade; 2× leverage cap;
                 one position max; mark-price stops where applicable
Phase 3r §8:     mark-price gap governance
Phase 3v §8:     stop-trigger-domain governance (four valid label
                 values; mixed_or_unknown invalid; fail-closed)
Phase 3w §6/§7/§8:
                 break-even / EMA-slope / stagnation governance;
                 per-candidate historical provenance preserved
Phase 4j §11:    metrics OI-subset partial-eligibility rule
Phase 4k:        V2 backtest-plan methodology
Phase 4p:        G1 strategy-spec discipline
Phase 4q:        G1 backtest-plan methodology
Phase 4v:        C1 strategy-spec discipline
Phase 4w:        C1 backtest-plan methodology
M0 (Phase 4ak):  twelve-clause gate + post-null cooldown +
                 cooled-down families list + memo template
```

## 10. Recommendation

```text
Recommendation: REMAIN PAUSED with documented non-material
findings logged.
```

The cumulative audit result is `DOCUMENTATION_LIMITATION` (with
two `IMPLEMENTATION_DEFECT_NON_MATERIAL` sub-findings). No
material defects exist. The recommended posture is:

- **Primary.** Remain paused. The audit foundation is acceptable.
  No verdict review is implied or recommended.
- **Conditional secondary.** A future docs-only methodology-
  harmonization memo could optionally:
  - specify the executed-price-shifting cost formula
    prospectively for any future Phase 4-style backtest
    (mirroring Phase 4q / 4w),
  - specify entry-bar exit handling prospectively (V2 convention
    versus G1 / C1 convention),
  - specify funding-event boundary handling prospectively
    (strictly between vs half-open),
  - add the four governance labels to V2 / G1 `run_metadata.json`
    for parity with C1.

  This is **not authorized** by Phase 4am. It is recorded as a
  conditional secondary option only.

- **Conditional tertiary.** If the operator separately authorizes
  a future Phase 4-style backtest under the new harmonized
  conventions, Phase 4am's findings provide the input list for
  that harmonization. Phase 4am does not propose such a phase.

- **Not recommended.** Full Phase 4al-Option-C exit-path forensic
  analysis is not motivated by Phase 4am's findings (the audit
  foundation is clean enough that forensic analysis would
  describe what already happened under documented rules; it is
  acceptable but not preferred over remain-paused).

- **Forbidden.** Verdict revision; lock revision; parameter
  optimization; rescue of any historical candidate; paper /
  shadow / live-readiness / deployment / exchange-write.

## 11. Explicit Non-Authorization

Phase 4am does **NOT** authorize:

- Phase 4an or any successor phase;
- full exit-path forensic analysis (Phase 4al §11.A.10 forensic
  scope; Option C);
- new strategy specs;
- new backtest plans;
- new backtests;
- data acquisition;
- 5m / 1m / aggTrades / tick data work (Phase 4al §14
  recommendation only);
- code changes to `src/prometheus/` modules;
- modifications to existing backtest scripts;
- modifications to manifests;
- creation of `v003` or any other dataset version;
- verdict revision (R3 / R2 / F1 / D1-A / V2 / G1 / C1 / R1a /
  R1b-narrow / H0 all preserved verbatim);
- lock revision (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p,
  Phase 4q, Phase 4v, Phase 4w, M0 all preserved verbatim);
- paper / shadow operation;
- live-readiness preparation;
- deployment;
- exchange-write capability;
- credential creation, request, inspection, or storage;
- MCP, Graphify, `.mcp.json`;
- production Binance keys.

The recommended state remains **paused**. No next phase is
authorized.

## 12. Final Status

```text
Phase 4am type:                    narrow audit-only successor
                                   (Phase 4al Option D / §11.A scope)
Aggregate audit result:            DOCUMENTATION_LIMITATION
Material defects:                  zero
Non-material defects:              two (F-1 V2 funding right-boundary
                                   inclusivity; F-4 entry-bar exit
                                   handling divergence between V2 and
                                   G1 / C1)
Documentation limitations:         two (F-2 V2 cost-application
                                   formula approximation;
                                   F-3 V2 / G1 missing governance-label
                                   artefact fields)
Verdicts revised:                  none
Locks changed:                     none
Successor phase authorized:        none
Recommended project state:         remain paused
```
