# Phase 4v Closeout

## Summary

Phase 4v authored the C1 — Volatility-Contraction Expansion Breakout Strategy Spec Memo (docs-only), translating the Phase 4u hypothesis-spec layer into a complete ex-ante strategy specification with exact thresholds. C1's strategy is locked: 30m signal timeframe; compression-box-based contraction measure with rolling-median width comparator; directional close-beyond-compression-box-with-buffer expansion transition with close-location requirement; structural stop derived from compression-box invalidation; measured-move target; time-stop fixed at `2 × N_comp` 30m bars; 0.25% risk / 2× leverage / 1 position max preserved; §11.6 = 8 bps HIGH per side preserved verbatim; LOW / MEDIUM / HIGH cost cells; 32-variant grid (= 2^5) over five binary axes (`N_comp` ∈ {8, 12}; `C_width` ∈ {0.45, 0.60}; `B_width` ∈ {0.05, 0.10}; `S_buffer` ∈ {0.10, 0.20}; `T_mult` ∈ {1.5, 2.0}); fixed parameters (`W_width = 240`; `L_delay = 1`; close-location 0.70 / 0.30; `T_stop_bars = 2 × N_comp`; no HTF gate; no funding input; no metrics OI; no volume gate); M1 / M2 / M3 / M4 mechanism-check thresholds with M5 diagnostic-only; opportunity-rate viability floors derived from first principles (≥1 candidate transition per 480 30m bars; BTC OOS HIGH trade_count ≥ 30; ≥50% of 32 variants ≥ 30 trades); 12 catastrophic-floor predicates (CFP-1..CFP-12) with C1-specific thresholds (CFP-9 enriched as opportunity-rate / sparse-intersection collapse; CFP-11 enriched as transition-dependency violation); validation windows reused verbatim from Phase 4k; BTCUSDT primary / ETHUSDT comparison; ETH cannot rescue BTC. Phase 4v was docs-only.

## Files changed

```text
docs/00-meta/implementation-reports/2026-04-30_phase-4v_c1-strategy-spec-memo.md   (new)
docs/00-meta/implementation-reports/2026-04-30_phase-4v_closeout.md                 (new — this file)
```

No other files modified by Phase 4v.

## Strategy-spec conclusion

The Phase 4v strategy spec is complete and predeclared at the ex-ante level. Every threshold in C1's first-spec is locked: contraction window, contraction-state predicate, expansion-transition trigger with close-location, structural stop, measured-move target, time-stop horizon, 32-variant grid axes, mechanism-check numeric thresholds, opportunity-rate floors, CFP-1..CFP-12 numeric thresholds, validation windows, cost cells, position sizing, and forbidden inputs. C1 remains **pre-research only**: not backtest-planned; not implemented; not backtested; not validated; not live-ready; **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1**. The next allowable step is a separately-authorized Phase 4w docs-only C1 Backtest-Plan Memo. **Phase 4v does NOT authorize Phase 4w.**

## Relationship to Phase 4u

- Phase 4u created the C1 hypothesis-spec layer only (no strategy spec, no threshold grid, no backtest plan, no backtest, no implementation).
- Phase 4u recommended Phase 4v as primary.
- The operator now authorized Phase 4v.
- Phase 4v remains docs-only.
- Phase 4v honored the Phase 4u binding design principles (contraction is local; entry on the transition itself; no top-level state machine; no multi-dimension AND classifier; no broad regime gate), the Phase 4u central anti-G1 discipline, the Phase 4u opportunity-rate viability principle (predeclared *before* any data is touched; intrinsic to the theory; NOT derived from Phase 4r forensic numbers), and the Phase 4u forbidden-rescue interpretations.
- Phase 4v did NOT modify Phase 4u; Phase 4u's hypothesis-spec is a binding input.
- Phase 4v does NOT run a backtest, acquire data, write code, or authorize Phase 4w.

## Strategy name

```text
C1 — Volatility-Contraction Expansion Breakout
```

Forbidden alternative names (would imply rescue): V3, G2, H2, G1-prime, G1-extension, G1-narrow, G1-hybrid, R1c, R3-prime, V2-prime, V2-narrow, V2-relaxed.

## Data requirements decision

**Existing data is sufficient.** No Phase 4w-prerequisite data-requirements memo required. No data acquisition required. **Phase 4v does NOT authorize acquisition.** C1 first-spec uses only existing trade-price klines (Phase 4i v001 30m / 4h klines; v002 15m / 1h-derived klines as sanity / context only) plus the existing volume column on klines (volume DIAGNOSTIC only; not used in entry / stop / target / time-stop rules). Funding is excluded from C1 first-spec.

## Timeframes

```text
Signal timeframe                    : 30m
Context timeframe (reporting only)  : 1h optional, NOT a rule input;
                                       4h excluded from first-spec rules
Entry execution                     : at next 30m bar's open after the
                                       completed signal bar
Decision time                       : the close_time of the completed
                                       30m signal bar
Bar discipline                      : completed bars only
```

## Contraction measure

```text
compression_box_high[t]    := max(high[t-N_comp..t-1])
compression_box_low[t]     := min(low[t-N_comp..t-1])
compression_box_width[t]   := high - low
rolling_median_width[t]    := median(width[t-W_width..t-1])
contraction_state[t]       := (width <= C_width × rolling_median_width)

W_width = 240 (fixed); N_comp ∈ {8, 12} (axis 1);
C_width ∈ {0.45, 0.60} (axis 2).
```

## Expansion transition

```text
contraction_recently_active[t] := any(contraction_state[t-L_delay..t])

LONG_TRANSITION[t] :=
    contraction_recently_active[t]
    AND close[t] > compression_box_high[t] + B_width × compression_box_width[t]
    AND close_location_long[t] >= 0.70

SHORT_TRANSITION[t] :=
    contraction_recently_active[t]
    AND close[t] < compression_box_low[t] - B_width × compression_box_width[t]
    AND close_location_short[t] <= 0.30

L_delay = 1 (fixed); B_width ∈ {0.05, 0.10} (axis 3);
close-location 0.70 / 0.30 fixed.
```

## Entry / stop / target / sizing model

```text
Entry           : at next 30m bar's open after confirmed signal close.
Long stop       : compression_box_low[t] - S_buffer × compression_box_width[t]
Short stop      : compression_box_high[t] + S_buffer × compression_box_width[t]
                  S_buffer ∈ {0.10, 0.20} (axis 4)
Long target     : entry_price + T_mult × compression_box_width[t]
Short target    : entry_price - T_mult × compression_box_width[t]
                  T_mult ∈ {1.5, 2.0} (axis 5)
Time-stop       : 2 × N_comp 30m bars
                  (16 if N_comp=8; 24 if N_comp=12; structurally tied to N_comp)
Stop-distance   : NO ATR-percentile gate in first-spec.
                  stop_distance_atr reported diagnostically only.
Stop precedence : stop > target > time-stop;
                  same-bar stop/target ambiguity = stop wins.
No break-even.  No trailing stop.  No regime exit (no regime state machine).

Position sizing (preserved from §1.7.3 verbatim):
  risk_fraction = 0.0025; max_leverage = 2.0; max_positions = 1;
  no pyramiding; no reversal while positioned;
  BTCUSDT primary; ETHUSDT comparison only; ETH cannot rescue BTC.
```

## Opportunity-rate floors

Derived from first principles; NOT from Phase 4r forensic numbers:

```text
min_candidate_transition_rate_BTC_OOS_HIGH:
  At least 1 candidate transition per 480 30m bars (~10 trading days at 30m).
  With OOS ~30 672 30m bars, this implies ≥64 candidate transitions
  across the OOS window for the train-best variant.

min_executed_trade_count_BTC_OOS_HIGH:
  BTC OOS HIGH executed trade_count >= 30 (preserved from Phase 4q M3
  numeric).

min_executed_trade_count_train_best:
  BTC train-best variant on OOS HIGH must have trade_count >= 30
  (binding for promotion).

min_variant_floor:
  At least 50% of the 32 variants must produce trade_count >= 30 on
  BTC OOS HIGH (otherwise CFP-1 triggers).

stop_distance_pass_rate:
  N/A in first-spec (no stop-distance gate).

sparse_intersection_collapse:
  CFP-9 enriched: triggers on candidate-transition rate floor failure
  OR train-best trade_count < 30 OR >50% variants below 30 trades.
```

## Threshold grid

**Exactly 32 variants over five binary axes (= 2^5).** Deterministic lexicographic ordering.

```text
Axis 1: N_comp     in {8, 12}
Axis 2: C_width    in {0.45, 0.60}
Axis 3: B_width    in {0.05, 0.10}
Axis 4: S_buffer   in {0.10, 0.20}
Axis 5: T_mult     in {1.5, 2.0}
```

Fixed parameters (cardinality 1; not axes): `W_width = 240`; `L_delay = 1`; close-location `0.70 / 0.30`; `T_stop_bars = 2 × N_comp`; HTF gate NONE; funding input NONE; volume input NONE; metrics OI NONE; `break_even_rule = disabled`; `ema_slope_method = not_applicable`; `stagnation_window_role = not_active`; `stop_trigger_domain = trade_price_backtest` (research); `risk_fraction = 0.0025`; `max_leverage = 2.0`; `max_positions = 1`.

## Mechanism-check thresholds

```text
M1 — Contraction-state validity:
  C1_mean_R - non_contraction_mean_R >= +0.10R on BTC OOS HIGH
  AND bootstrap CI lower (B = 10 000) > 0.

M2 — Expansion-transition value-add:
  C1_mean_R - always_active_same_geometry_mean_R >= +0.05R on
  BTC OOS HIGH AND bootstrap CI lower > 0;
  AND C1_mean_R - delayed_breakout_mean_R >= 0 on BTC OOS HIGH.

M3 — Inside-spec co-design validity:
  BTC OOS HIGH mean_R > 0
  AND BTC OOS HIGH trade_count >= 30
  AND no CFP-1 / CFP-2 / CFP-3 trigger
  AND opportunity-rate floors satisfied.

M4 — Cross-symbol robustness:
  ETH OOS HIGH (G1-vs-baseline) differential non-negative
  AND directional consistency with BTC.
  ETH cannot rescue BTC; CFP-4 enforces.

M5 — Compression-box structural validity (DIAGNOSTIC ONLY in first-spec):
  Stops tied to compression-box invalidation behave better than a
  generic ATR-buffered structural stop on the same setup.
  Phase 4w may upgrade to binding gate if justified.

Promotion-bar:
  M1 PASS AND M2 PASS AND M3 PASS AND M4 PASS AND no CFP triggered.
```

## Negative-test specification

```text
Required (binding):
  non_contraction_breakout_baseline                 (M1)
  always_active_same_geometry_breakout_baseline     (M2)
  delayed_breakout_baseline                         (M2 detail)
  active_opportunity_rate_diagnostic                (M3 / CFP-9)

Optional (diagnostic only by default):
  random_contraction_baseline                       (specificity check;
                                                     Phase 4w may upgrade)
```

## Catastrophic-floor predicates

CFP-1..CFP-12 with C1-specific thresholds (full text in the Phase 4v memo):

- CFP-1 insufficient trade count; CFP-2 negative BTC OOS HIGH expectancy; CFP-3 catastrophic PF / drawdown; CFP-4 BTC failure with ETH pass; CFP-5 train-only success / OOS failure; CFP-6 PBO / DSR failure; CFP-7 overconcentration; CFP-8 sensitivity fragility (predeclared perturbation ranges around the five axes); CFP-9 opportunity-rate / sparse-intersection collapse; CFP-10 forbidden optional ratio access; CFP-11 transition-dependency violation (signal without prior contraction; entry beyond L_delay; lookahead); CFP-12 data governance violation.

**Any single CFP triggered = Verdict C HARD REJECT** in any future Phase 4x backtest.

## Validation windows

Reused verbatim from Phase 4k:

```text
Train       : 2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC  (~18 months)
Validation  : 2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC  (~12 months)
OOS holdout : 2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC  (~21 months)
```

## Recommended next operator choice

- **Option A — primary recommendation:** Phase 4w — C1 Backtest-Plan Memo (docs-only). Phase 4w would translate the Phase 4v C1 strategy spec into a precise, reproducible, fail-closed future Phase 4x backtest methodology, mirroring Phase 4q's discipline (NOT V2 / G1 numeric thresholds).
- **Option B — conditional secondary:** remain paused.

NOT recommended: immediate C1 backtest (REJECTED); immediate C1 implementation (REJECTED); data acquisition (REJECTED; not authorized); paper / shadow / live (FORBIDDEN); Phase 4 canonical (FORBIDDEN); production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials (FORBIDDEN); exchange-write capability (FORBIDDEN); G1 / V2 / R2 / F1 / D1-A rescue (FORBIDDEN).

**Phase 4w is NOT authorized by this memo or this closeout.** Phase 4w execution requires a separate explicit operator authorization brief.

## Commands run

```text
git status
git rev-parse main
git rev-parse origin/main
git checkout -b phase-4v/c1-strategy-spec-memo
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q (-> pytest)
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4v_c1-strategy-spec-memo.md
git commit -F <commit-message-file>
git push -u origin phase-4v/c1-strategy-spec-memo
```

(No acquisition, diagnostics, or backtest scripts were run. No web research was performed for this memo; all analysis is derived from the existing project record and the Phase 4m / Phase 4s / Phase 4t / Phase 4u validity gate frameworks.)

## Verification results

```text
Python version             : 3.12.4
ruff check . (initial)     : All checks passed!
pytest (initial)           : 785 passed
mypy (initial)             : Success: no issues found in 82 source files
git status (initial)       : clean working tree (only gitignored
                              .claude/scheduled_tasks.lock and data/research/
                              untracked; not committed)
git rev-parse main         : 6862dc3708613109f74c04743c60e6cba78993d9
git rev-parse origin/main  : 6862dc3708613109f74c04743c60e6cba78993d9
```

## Commit

```text
Phase 4v memo commit:      5f4202dd7bc9556747cec6e873aad7d0ca76d698
Phase 4v closeout commit:  <recorded after this file is committed>
```

## Final git status

(recorded after closeout commit and push)

## Final git log --oneline -5

(recorded after closeout commit and push)

## Final rev-parse

```text
HEAD                                              : <recorded after closeout commit>
origin/phase-4v/c1-strategy-spec-memo             : <recorded after closeout push>
main                                              : 6862dc3708613109f74c04743c60e6cba78993d9 (unchanged)
origin/main                                       : 6862dc3708613109f74c04743c60e6cba78993d9 (unchanged)
```

## Branch / main status

`main` remains unchanged at `6862dc3708613109f74c04743c60e6cba78993d9`. Phase 4v is authored exclusively on the `phase-4v/c1-strategy-spec-memo` branch. Phase 4v is **not** merged to main by this closeout. Any future merge to main requires a separate explicit operator authorization brief (analogous to prior phase merge closeouts).

## Forbidden-work confirmation

Phase 4v did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script;
- run `scripts/phase4r_g1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create a runnable strategy beyond the conceptual name C1;
- create V3 / H2 / G2 / any runnable candidate;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4w / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : HARD REJECT (Phase 4r — Verdict C; CFP-1 critical
                       binding driver; CFP-9 independent driver;
                       terminal for G1 first-spec)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price stops
                      (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u
                            : all preserved verbatim
Phase 4v                    : C1 strategy-spec memo (this phase; new; docs-only)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              strategy-spec defined in Phase 4v;
                              not backtest-planned;
                              not implemented; not backtested; not validated;
                              not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : Phase 4w conditional primary;
                              remain-paused conditional secondary
```

## Next authorization status

```text
Phase 4w                       : NOT authorized
Phase 4x                       : NOT authorized
Phase 4 (canonical)            : NOT authorized
Paper / shadow                 : NOT authorized
Live-readiness                 : NOT authorized
Deployment                     : NOT authorized
Production-key creation        : NOT authorized
Authenticated REST             : NOT authorized
Private endpoints              : NOT authorized
User stream / WebSocket        : NOT authorized
Exchange-write capability      : NOT authorized
MCP / Graphify                 : NOT authorized
.mcp.json / credentials        : NOT authorized
C1 implementation              : NOT authorized
C1 backtest execution          : NOT authorized
C1 data acquisition            : NOT authorized (none required)
G1 / V2 / R2 / F1 / D1-A rescue: NOT authorized; not proposed
G1-prime / G1-extension axes   : NOT authorized; not proposed
G1-narrow / G1 hybrid          : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                               : NOT authorized; data unavailable.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4w (C1 Backtest-Plan Memo, docs-only) or remain paused. Until then, the project remains at the post-Phase-4v strategy-spec boundary.

---

**Phase 4v was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state: Phase 4w conditional primary; remain-paused conditional secondary. No next phase authorized.**
