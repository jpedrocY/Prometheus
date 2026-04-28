# Phase 3d-B2 — F1 Execution + Diagnostics + First-Execution Gate Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 V1-breakout baseline-of-record); Phase 2y closeout (§11.6 = 8 bps HIGH preserved); Phase 3b F1 spec memo §§ 1–15 (binding spec); Phase 3c F1 execution-planning memo §§ 1–13 with operator-mandated amendments (§7.2(iv) BTC HIGH expR > 0; §7.3 MECHANISM PASS / FRAMEWORK FAIL — §11.6 cost-sensitivity blocks; §10.4 Phase 3d-A sequencing requirement); Phase 3d-A and Phase 3d-B1 reports.

**Phase:** 3d-B2 — F1 candidate execution + first-execution gate evaluation + M1/M2/M3 mechanism checks + Phase 3c §8 mandatory diagnostics + P.14 hard-block invariants. **First phase to authorize F1 candidate backtest invocation.**

**Branch:** `phase-3d-b2/f1-execution-diagnostics`. **Date:** 2026-04-28 UTC.

**Status:** **F1 framework verdict: HARD REJECT.** All four mandatory R-window runs executed. F1 produces catastrophic-floor violations on BTC MED (expR=−0.5227 ≤ −0.50), BTC HIGH (expR=−0.7000 / PF=0.2181), and ETH HIGH (expR=−0.5712 / PF=0.2997). Per Phase 3c §7.3, any catastrophic absolute-floor violation classifies the outcome as HARD REJECT, irrespective of mechanism partial support. Per the operator brief and Phase 3c §6.2, **F1 V MED MARK was NOT executed** because R-window hard-rejected. Mechanism evidence is mixed: M1 BTC PARTIAL (fraction non-neg passes at 55.4%, but magnitude only +0.024R at h=8, well below the +0.10R threshold); M2 BTC FAIL / ETH PARTIAL; M3 PASS on both symbols (target subset is isolated-profitable but overwhelmed by stop-out subset). All P.14 hard-block invariants PASS. F1 is retained as research evidence; the F1 family is concluded as FAILED (HARD REJECT) under Phase 3c §7.3 governance. **No project-state change.** R3 remains V1-breakout baseline-of-record; H0 remains V1-breakout framework anchor; R1a/R1b-narrow/R2 retained-research-evidence stand; R2 framework-FAILED status stands; §11.6 = 8 bps HIGH preserved verbatim. **No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / threshold / strategy-parameter / project-lock change.** **No `data/` artifacts committed.** Phase 3d-B2 is the terminal phase for F1; no subsequent F1 phase is proposed.

---

## 1. Plain-English explanation of what Phase 3d-B2 did

Phase 3d-B2 is the **first phase to actually run F1 candidate backtests.** Phase 3d-A (merged) added the F1 self-contained module and primitives. Phase 3d-B1 (merged) wired the F1 dispatch into `BacktestEngine` and proved with H0/R3 controls bit-for-bit that the new dispatch path does not perturb V1 behavior. Phase 3d-B2 takes the merged engine and executes the precommitted Phase 3c §6 run inventory:

1. F1 R MED MARK — governing first F1 run.
2. F1 R LOW MARK — §11.6 cost-sensitivity LOW.
3. F1 R HIGH MARK — §11.6 HIGH cost-sensitivity gate.
4. F1 R MED TRADE_PRICE — stop-trigger sensitivity.
5. F1 V MED MARK — conditional on §7.2 PROMOTE outcome at run #1.

After running #1–#4, Phase 3d-B2 evaluates Phase 3c §7.2's five conditions, computes Phase 3c §9 M1/M2/M3 mechanism checks, produces the §8 mandatory diagnostics subset, runs the P.14 hard-block invariants, and applies Phase 3c §7.3 verdict mapping. The outcome is **HARD REJECT** — multiple catastrophic absolute-floor violations on BTC and ETH at MED and HIGH slippage. Per the operator brief and Phase 3c §6.2, F1 V MED MARK was NOT executed.

Phase 3d-B2 explicitly did NOT:

- Run any V-window F1 cell (R-window hard-rejected).
- Run any LOW/HIGH TRADE_PRICE cell (forbidden run).
- Run any V LOW / V HIGH / V TRADE_PRICE cell (forbidden runs).
- Run any parameter variant or alternative threshold (forbidden).
- Modify any Phase 3b F1 spec axis, V1 behavior, threshold, or project lock.
- Use H0/R3 deltas as governing promotion logic (descriptive only per Phase 3c §7.4).
- Begin paper/shadow planning, Phase 4 work, live-readiness work, deployment work, production-key work, or exchange-write work.

## 2. Preflight status

| Check | Status |
|------|:-----:|
| Branch `phase-3d-b2/f1-execution-diagnostics` created from `main` | ✓ |
| `main` clean and synced with `origin/main` at `4a2b7d0d6f8547535318cbae15ca738c4a47f8b3` | ✓ |
| Phase 3d-B1 present on `main` (merge `cbe5f672a8d6c958f98a0c7d2165c6b861859d6d`) | ✓ |
| No untracked files | ✓ |
| Required v002 datasets present locally (BTC + ETH 15m / 1h / mark-price / funding / exchangeInfo) | ✓ |
| No `data/` files staged or tracked | ✓ |
| Phase 3c amended gate (BTC HIGH > 0; M1+BTC HIGH≤0 = §11.6 block; H0/R3 descriptive only) carried into the analysis script | ✓ |

## 3. Quality-gate results

All four pre-execution gates green on the Phase 3d-B2 branch tip:

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | 567 passed |
| Linter | `uv run ruff check .` | All checks passed |
| Formatter | `uv run ruff format --check .` | 144 files already formatted |
| Type checker | `uv run mypy src` | Success: no issues found in 57 source files |

## 4. H0/R3 control reproduction results

Per Phase 3c §10.2 baseline-preservation discipline, the four V1 control runs reproduce locked Phase 2e/2l/2s baselines bit-for-bit on all 48 metric cells (4 control runs × 2 symbols × 6 metrics).

| Cell | Symbol | Locked baseline | Phase 3d-B2 reproduction | Match |
|------|:-:|:----------------|:--------------------------|:-:|
| H0 R MED MARK | BTC | n=33, WR=30.30%, expR=−0.459, PF=0.255, netPct=−3.39%, maxDD=−3.67% | n=33, WR=30.30%, expR=−0.4590, PF=0.2552, netPct=−3.3917%, maxDD=−3.6745% | ✓ |
| H0 R MED MARK | ETH | n=33, WR=21.21%, expR=−0.475, PF=0.321, netPct=−3.53%, maxDD=−4.13% | n=33, WR=21.21%, expR=−0.4752, PF=0.3207, netPct=−3.5270%, maxDD=−4.1341% | ✓ |
| H0 V MED MARK | BTC | n=8, WR=25.00%, expR=−0.313, PF=0.541, netPct=−0.56%, maxDD=−0.87% | n=8, WR=25.00%, expR=−0.3132, PF=0.5410, netPct=−0.5570%, maxDD=−0.8735% | ✓ |
| H0 V MED MARK | ETH | n=14, WR=28.57%, expR=−0.174, PF=0.695, netPct=−0.55%, maxDD=−0.80% | n=14, WR=28.57%, expR=−0.1735, PF=0.6950, netPct=−0.5461%, maxDD=−0.8031% | ✓ |
| R3 R MED MARK | BTC | n=33, WR=42.42%, expR=−0.240, PF=0.560, netPct=−1.77%, maxDD=−2.16% | n=33, WR=42.42%, expR=−0.2403, PF=0.5602, netPct=−1.7743%, maxDD=−2.1592% | ✓ |
| R3 R MED MARK | ETH | n=33, WR=33.33%, expR=−0.351, PF=0.474, netPct=−2.61%, maxDD=−3.65% | n=33, WR=33.33%, expR=−0.3511, PF=0.4736, netPct=−2.6055%, maxDD=−3.6468% | ✓ |
| R3 V MED MARK | BTC | n=8, WR=25.00%, expR=−0.287, PF=0.580, netPct=−0.51%, maxDD=−1.06% | n=8, WR=25.00%, expR=−0.2873, PF=0.5799, netPct=−0.5099%, maxDD=−1.0606% | ✓ |
| R3 V MED MARK | ETH | n=14, WR=42.86%, expR=−0.093, PF=0.824, netPct=−0.29%, maxDD=−0.94% | n=14, WR=42.86%, expR=−0.0932, PF=0.8242, netPct=−0.2932%, maxDD=−0.9404% | ✓ |

Bit-for-bit reproduction confirms the engine's V1 dispatch is unchanged by Phase 3d-B1 + Phase 3d-B2 work. F1 results below are eligible for interpretation.

## 5. Exact F1 runs executed

Four mandatory R-window cells per Phase 3c §6.1:

| # | Variant | Window | Slippage | Stop trigger | Run dir |
|---|---------|--------|----------|--------------|---------|
| 1 | F1 | R | MEDIUM | MARK_PRICE | `phase-3d-f1-window=r-slip=medium/2026-04-28T21-55-59Z` |
| 2 | F1 | R | LOW | MARK_PRICE | `phase-3d-f1-window=r-slip=low/2026-04-28T22-05-42Z` |
| 3 | F1 | R | HIGH | MARK_PRICE | `phase-3d-f1-window=r-slip=high/2026-04-28T22-15-22Z` |
| 4 | F1 | R | MEDIUM | TRADE_PRICE | `phase-3d-f1-window=r-slip=medium-stop=trade_price/2026-04-28T22-25-02Z` |

All four runs completed end-to-end with no engine errors. Each run wrote `trade_log.parquet`/`trade_log.json`, `summary_metrics.json`, `f1_lifecycle_total.json`, `equity_curve.parquet`, `drawdown.parquet`, `r_multiple_hist.parquet`, `monthly_breakdown.parquet`, `backtest_report.manifest.json`, and `config_snapshot.json` under the per-run directory. All artifacts are git-ignored under `data/derived/backtests/`.

The conditional V-window run #5 (F1 V MED MARK) was **NOT executed** because R-window verdict is HARD REJECT (§9 below).

## 6. Confirmation that no forbidden runs were executed

Confirmed. The Phase 3c §6 inventory + Phase 3d-B2 brief explicitly forbid: F1 V LOW; F1 V HIGH; F1 V TRADE_PRICE; F1 R LOW TRADE_PRICE; F1 R HIGH TRADE_PRICE; any parameter variant; any alternative threshold; any extra symbols; any post-hoc reruns. **None of these were executed.** Only the four mandatory R-window cells (#1–#4) above were run. The conditional V-window run #5 was skipped per the §6.2 / §11.3 conditional rule because the R-window gate hard-rejected.

## 7. Summary metrics

### 7.1 F1 R MED MARK (governing)

| Symbol | n | WR | expR | PF | netPct | maxDD | long | short | stop | target | time_stop | EOD |
|--------|---:|-------:|--------:|-------:|---------:|--------:|------:|-------:|-----:|-------:|----------:|----:|
| BTCUSDT | 4720 | 33.05% | **−0.5227** | **0.3697** | −545.56% | −552.74% | 2390 | 2330 | 2534 | 1536 | 650 | 0 |
| ETHUSDT | 4826 | 33.36% | **−0.4024** | **0.4667** | −433.60% | −443.84% | 2402 | 2424 | 2516 | 1610 | 700 | 0 |

### 7.2 F1 R LOW MARK (cost sensitivity LOW)

| Symbol | n | WR | expR | PF | netPct | maxDD |
|--------|---:|-------:|--------:|-------:|---------:|--------:|
| BTCUSDT | 4720 | 33.79% | **−0.4335** | 0.4652 | −452.81% | −459.71% |
| ETHUSDT | 4826 | 34.34% | **−0.3194** | 0.5653 | −343.79% | −348.89% |

### 7.3 F1 R HIGH MARK (§11.6 HIGH cost-sensitivity gate)

| Symbol | n | WR | expR | PF | netPct | maxDD |
|--------|---:|-------:|--------:|-------:|---------:|--------:|
| BTCUSDT | 4720 | 30.93% | **−0.7000** | **0.2181** | −732.41% | −739.50% |
| ETHUSDT | 4826 | 31.79% | **−0.5712** | **0.2997** | −616.65% | −626.66% |

### 7.4 F1 R MED TRADE_PRICE (stop-trigger sensitivity)

| Symbol | n | WR | expR | PF | netPct | maxDD |
|--------|---:|-------:|--------:|-------:|---------:|--------:|
| BTCUSDT | 4747 | 32.10% | −0.5503 | 0.3503 | −576.72% | −583.93% |
| ETHUSDT | 4853 | 32.27% | −0.4454 | 0.4286 | −482.77% | −493.13% |

## 8. Conditional F1 V MED MARK result

**Not executed.** R-window verdict at §9 is HARD REJECT; per Phase 3c §6.2 / §11.3 the V-window run is conditional on §7.2 PROMOTE and is skipped on any non-PROMOTE outcome (HARD REJECT, MECHANISM FAIL, MECHANISM PASS / FRAMEWORK FAIL — §11.6 cost-sensitivity blocks, MECHANISM PASS / FRAMEWORK FAIL — other).

## 9. First-execution gate

Phase 3c §7.2 conditions (i)–(v) evaluated on F1 R MED MARK / R HIGH MARK:

| Condition | Definition | Cell | Threshold | Observed | Pass? |
|---|---|---|---|---|:-:|
| (i) Absolute BTC MED edge | expR(F1, BTC, R, MED, MARK) > 0 | BTC MED MARK | > 0 | −0.5227 | ✗ |
| (ii) M1 BTC mechanism (mean) | mean counter_displacement_8_R(BTC) ≥ +0.10 R | BTC | ≥ +0.10 | +0.0238 | ✗ |
| (ii) M1 BTC mechanism (fraction) | fraction(counter_displacement_8_R ≥ 0, BTC) ≥ 50% | BTC | ≥ 50% | 55.38% | ✓ |
| (iii) ETH MED non-catastrophic | expR > −0.50 AND PF > 0.30 | ETH MED MARK | expR > −0.50 / PF > 0.30 | −0.4024 / 0.4667 | ✓ |
| (iv) BTC HIGH expR | expR(F1, BTC, R, HIGH, MARK) > 0 | BTC HIGH MARK | > 0 | −0.7000 | ✗ |
| (iv) ETH HIGH non-catastrophic | expR > −0.50 AND PF > 0.30 | ETH HIGH MARK | expR > −0.50 / PF > 0.30 | −0.5712 / 0.2997 | ✗ |
| (v) BTC MED absolute floor | expR > −0.50 AND PF > 0.30 | BTC MED MARK | expR > −0.50 / PF > 0.30 | −0.5227 / 0.3697 | ✗ (expR catastrophic) |
| (v) ETH MED absolute floor | expR > −0.50 AND PF > 0.30 | ETH MED MARK | expR > −0.50 / PF > 0.30 | −0.4024 / 0.4667 | ✓ |

### 9.1 Catastrophic floor violations

Per Phase 3c §7.3 HARD REJECT row: any catastrophic absolute-floor violation (`expR ≤ −0.50` OR `PF ≤ 0.30` on BTC/ETH × MED/HIGH × MARK_PRICE cells).

- BTC MED expR = −0.5227 ≤ −0.50 — **violation**
- BTC HIGH expR = −0.7000 ≤ −0.50 — **violation**
- BTC HIGH PF = 0.2181 ≤ 0.30 — **violation**
- ETH HIGH expR = −0.5712 ≤ −0.50 — **violation**
- ETH HIGH PF = 0.2997 ≤ 0.30 — **violation** (just barely; 0.2997 < 0.30)

Five separate catastrophic-floor violations across BTC and ETH at MED and HIGH slippage. The catastrophic-floor predicate is satisfied with substantial margin.

## 10. Final Phase 3d-B2 verdict

**HARD REJECT.**

Per Phase 3c §7.3 verdict mapping: "Any catastrophic absolute-floor violation: expR ≤ −0.50 OR PF ≤ 0.30 on either symbol at either MED or HIGH slippage" → HARD REJECT. F1 is hard-rejected. V-window run #5 not executed. F1 family research is concluded as failed.

The HARD REJECT outcome supersedes the MECHANISM FAIL / MECHANISM PASS / FRAMEWORK FAIL alternatives in the §7.3 verdict mapping. Even though M3 (target-exit subset) is mechanism-supported in isolation (§11.3 below) and M1 BTC is partially supported on the fraction predicate, the absolute-floor catastrophic violations classify F1's first-execution outcome as HARD REJECT, irrespective of mechanism partial support. This is the same Phase 2f §11.3.5 binding-rule treatment that R2's Phase 2w outcome received.

## 11. M1 / M2 / M3 mechanism results

### 11.1 M1 — overextension reversion

Per-trade post-entry counter-displacement at horizons {1, 2, 4, 8} completed bars from entry-fill bar B+1, normalized to R-multiples:

`counter_displacement_h_R = ((close(B+1+h) − close(B+1)) × trade_direction_sign) / stop_distance`

with `trade_direction_sign = +1` for LONG, −1 for SHORT (positive = move toward profit / reversion direction).

| Symbol | Horizon | Mean (R) | Fraction non-neg | n |
|--------|--------:|---------:|-----------------:|---:|
| BTCUSDT | 1 | +0.0158 | 54.07% | 4720 |
| BTCUSDT | 2 | +0.0077 | 54.75% | 4720 |
| BTCUSDT | 4 | +0.0195 | 55.38% | 4720 |
| BTCUSDT | **8** | **+0.0238** | **55.38%** | 4720 |
| ETHUSDT | 1 | +0.0178 | 54.29% | 4826 |
| ETHUSDT | 2 | +0.0104 | 54.21% | 4826 |
| ETHUSDT | 4 | −0.0207 | 54.66% | 4826 |
| ETHUSDT | 8 | −0.0420 | 53.83% | 4826 |

**M1 BTC PASS criterion:** `mean ≥ +0.10 R AND fraction ≥ 50%` at h=8.

- BTC h=8 mean = +0.0238 R: **FAIL** (well below +0.10 R).
- BTC h=8 fraction = 55.38%: **PASS** (above 50%).

**M1 BTC verdict: PARTIAL.** The directional support is mechanism-consistent (more than half of trades produce non-negative 8-bar counter-displacement) but the magnitude is small (+0.024 R per trade); after stop / target / time-stop exits and round-trip costs (~30 bps round-trip taker fee + slippage), this small reversion cannot compensate for the high stop-out fraction. Per §7.2(ii) M1 PASS criterion is conjunctive on (mean AND fraction); conjunctive evaluation gives **M1 BTC FAIL** for §7.2 governance. M1 ETH shows mean turning negative at h≥4 — the ETH mechanism does not even sustain on the fraction-magnitude product at longer horizons, so M1 ETH is informatively FAIL as well.

**Interpretation:** F1's central thesis (post-overextension counter-displacement provides positive expected R-multiple at the 8-bar horizon) is **partially supported on direction but falsified on magnitude**. The empirical magnitude (~+0.024 R) is a fraction of the +0.10 R pre-declared threshold and an order of magnitude smaller than the per-trade cost burden.

### 11.2 M2 — chop-regime stop-out fraction

Per Phase 3c §9.2: F1 stop-out fraction in the low-volatility tercile (chop / range-bound regime per Phase 2l §6.1 / Phase 2w §11.9 classifier — trailing 1000-bar 1h ATR(20) percentile rank, tercile cuts at 33rd / 67th, classified at the most recent completed 1h bar before entry-fill).

| Symbol | F1 low_vol n | F1 low_vol stop_frac | H0 low_vol n | H0 low_vol stop_frac | Δ_M2 (H0 − F1) | Pass (≥ +0.10) |
|--------|-------------:|---------------------:|-------------:|---------------------:|---------------:|:-:|
| BTCUSDT | 1746 | 55.56% | 13 | 46.15% | **−0.0940** | ✗ |
| ETHUSDT | 1849 | 52.30% | 12 | 91.67% | **+0.3937** | ✓ |

**M2 BTC: FAIL.** F1's BTC low-vol stop-out fraction (55.56%) is **higher** than H0's (46.15%), the opposite of the §9.2 hypothesis. F1 stops out more in chop on BTC than the breakout family it was meant to outperform there. This contradicts the Phase 3b §2.3 chop-regime advantage hypothesis directly.

**M2 ETH: PASS** (descriptive). F1's ETH low-vol stop-out fraction (52.30%) is much lower than H0's (91.67%); Δ_M2 = +0.3937 ≥ +0.10. However the H0 low-vol n=12 base is small, so the H0 reference ratio is statistically weak; the descriptive direction supports the M2 hypothesis on ETH but the magnitude is dominated by H0's small-sample artifact.

M2 is descriptive-only per Phase 3c §9.2; it does not gate the §7.2 verdict. The split outcome (BTC FAIL / ETH PARTIAL with weak H0 baseline) is recorded as research evidence; it does not alter the §10 HARD REJECT verdict.

### 11.3 M3 — target-exit positive contribution

Per Phase 3c §9.3: F1's TARGET-exit subset must produce positive aggregate net-of-cost R-multiple contribution per symbol; mean ≥ +0.30 R.

| Symbol | TARGET subset n | aggregate_R | mean_R | Pass (agg > 0 AND mean ≥ +0.30) |
|--------|----------------:|------------:|-------:|:-:|
| BTCUSDT | 1536 | **+1149.14 R** | **+0.7481** | ✓ |
| ETHUSDT | 1610 | **+1398.19 R** | **+0.8684** | ✓ |

**M3: PASS on both symbols** (descriptive). The TARGET-exit subset is profitable when isolated. This means **the SMA(8) mean reference does fire on a meaningful subset of trades, and when it fires it is profitable enough to overcome round-trip cost.** However:

- The TARGET-exit count (1536 BTC / 1610 ETH) is 32–33% of total trades; the remaining 67–68% are STOP exits or TIME_STOP exits whose aggregate negative contribution overwhelms the M3 positive contribution.
- This shape — M3 PASS while §7.2 hard-rejects — is the **R2-precedent shape** (Phase 2w §16.3): a mechanism-consistent subset is empirically profitable, but the strategy-as-specified (which cannot select only the profitable subset prospectively) is FAILED.

M3 is descriptive-only per Phase 3c §9.3; it does not gate the §7.2 verdict. M3 PASS does not promote F1; it is recorded as research evidence and may inform any hypothetical future F1-prime spec consideration in a separately-authorized phase.

### 11.4 PASS / FAIL / PARTIAL combined interpretation (Phase 3c §9.4)

| §7.2 outcome | M1 | M2 | M3 | Interpretation per §9.4 |
|---|---|---|---|---|
| **HARD REJECT** | PARTIAL (BTC) | FAIL (BTC) / PARTIAL (ETH) | PASS (both) | Catastrophic absolute-floor violation. F1 family research closed. Mechanism evidence is partial: the SMA(8) target subset is profitable in isolation (M3 PASS), but the wider trade population has insufficient post-entry reversion magnitude (M1 mean below threshold) and fails the chop-regime advantage hypothesis on BTC (M2). The TARGET-subset evidence is recorded as research data only. |

## 12. Mandatory diagnostics summary

### 12.1 Trade count and frequency (F1 R MED MARK)

| Symbol | n | per-month | per-week | per-day |
|--------|---:|----------:|---------:|--------:|
| BTCUSDT | 4720 | 131.1 | 30.2 | 4.31 |
| ETHUSDT | 4826 | 134.1 | 30.9 | 4.41 |

R-window = 36 months (1095 days). F1 fires ~4.3 trades per day on each symbol, ~150× the H0/R3 baseline (~33 trades total over 36 months).

### 12.2 Long/short split (F1 R MED MARK)

| Symbol | LONG n | SHORT n | LONG % |
|--------|-------:|--------:|-------:|
| BTCUSDT | 2390 | 2330 | 50.6% |
| ETHUSDT | 2402 | 2424 | 49.8% |

F1 is symmetric by construction; the empirical split confirms no directional asymmetry.

### 12.3 Exit-reason fractions (F1 R MED MARK)

| Symbol | STOP | TARGET | TIME_STOP | END_OF_DATA |
|--------|-----:|-------:|----------:|------------:|
| BTCUSDT | 53.69% | 32.54% | 13.77% | 0% |
| ETHUSDT | 52.13% | 33.36% | 14.51% | 0% |

Accounting identity holds: STOP + TARGET + TIME_STOP + END_OF_DATA = n on both symbols.

### 12.4 F1 field distributions (BTC / ETH F1 R MED MARK)

`overextension_magnitude_at_signal = |displacement(B)| / ATR(20)(B)`

| Symbol | mean | median | p25 | p75 | min | max |
|--------|-----:|-------:|----:|----:|----:|----:|
| BTCUSDT | 2.79 | 2.39 | 2.00 | 3.16 | 1.75 (just above threshold) | 13.69 |
| ETHUSDT | 2.86 | 2.45 | 2.04 | 3.27 | 1.75 | 14.55 |

`stop_distance_at_signal_atr` constrained to [0.60, 1.80] by spec (§4.9). Empirical min/max at the band edges per the P.14 invariant check (§13).

`entry_to_target_distance_atr` (R-multiples = entry_to_target_atr / stop_distance_atr) — drives the per-trade expected R at perfect target hit. Combined with target-exit mean R (M3 §11.3): mean +0.75 R BTC / +0.87 R ETH on TARGET subset.

### 12.5 Cost sensitivity LOW / MEDIUM / HIGH (F1 R-window)

| Symbol | LOW expR | LOW PF | MED expR | MED PF | HIGH expR | HIGH PF |
|--------|---------:|-------:|---------:|-------:|----------:|--------:|
| BTCUSDT | −0.4335 | 0.4652 | −0.5227 | 0.3697 | −0.7000 | 0.2181 |
| ETHUSDT | −0.3194 | 0.5653 | −0.4024 | 0.4667 | −0.5712 | 0.2997 |

**Cost-sensitivity slope is steep and uniformly worsening.** Even at LOW slippage (1 bps per side), F1 is decisively negative. HIGH slippage (8 bps per side) produces catastrophic floor violations on multiple cells. F1 is **not cost-resilient**.

### 12.6 Mark-price vs Trade-price stop trigger (F1 R MED, BTC + ETH)

| Symbol | MARK n | MARK expR | MARK PF | TRADE n | TRADE expR | TRADE PF |
|--------|-------:|----------:|--------:|--------:|-----------:|---------:|
| BTCUSDT | 4720 | −0.5227 | 0.3697 | 4747 | −0.5503 | 0.3503 |
| ETHUSDT | 4826 | −0.4024 | 0.4667 | 4853 | −0.4454 | 0.4286 |

TRADE_PRICE is uniformly slightly worse than MARK_PRICE on F1; the trade-count differs by ~30 trades because TRADE_PRICE-triggered stops fire on slightly different bars and cooldown / re-entry counts shift by O(N) — the engine's MARK_PRICE default mirrors the live protective-stop `workingType=MARK_PRICE` so this remains the production-aligned reference.

### 12.7 Per-fold consistency (F1 R MED MARK; 6 half-year folds)

| Fold | BTC n | BTC expR | BTC PF | ETH n | ETH expR | ETH PF |
|---|---:|---:|---:|---:|---:|---:|
| 2022H1 | 798 | −0.5394 | 0.3450 | 821 | −0.4248 | 0.4365 |
| 2022H2 | 768 | −0.5028 | 0.3812 | 783 | −0.3886 | 0.4691 |
| 2023H1 | 730 | −0.4928 | 0.3970 | 756 | −0.3754 | 0.4830 |
| 2023H2 | 770 | −0.5371 | 0.3640 | 786 | −0.4109 | 0.4538 |
| 2024H1 | 802 | −0.5421 | 0.3505 | 826 | −0.4014 | 0.4630 |
| 2024H2 | 853 | −0.5247 | 0.3787 | 855 | −0.4131 | 0.4564 |

**Per-fold consistency is uniform and uniformly negative** on BTC. Each fold's BTC expR sits in the [-0.55, -0.49] band; no fold produces positive expR. ETH per-fold expR sits in [-0.43, -0.37]. The catastrophic-floor violation is not a single-fold artifact — it is the consistent F1 R-window outcome across all six folds.

### 12.8 Funnel accounting (all four cells)

| Cell | Symbol | detected | filled | rejected_stop_distance | blocked_cooldown | identity |
|------|:-:|--:|--:|--:|--:|:-:|
| F1 R MED MARK | BTC | 17927 | 4720 | 6263 | 6944 | ✓ |
| F1 R MED MARK | ETH | 18487 | 4826 | 6549 | 7112 | ✓ |
| F1 R LOW MARK | BTC | 17927 | 4720 | 6263 | 6944 | ✓ |
| F1 R LOW MARK | ETH | 18487 | 4826 | 6549 | 7112 | ✓ |
| F1 R HIGH MARK | BTC | 17927 | 4720 | 6263 | 6944 | ✓ |
| F1 R HIGH MARK | ETH | 18487 | 4826 | 6549 | 7112 | ✓ |
| F1 R MED TRADE_PRICE | BTC | 18098 | 4747 | 6285 | 7066 | ✓ |
| F1 R MED TRADE_PRICE | ETH | 18725 | 4853 | 6574 | 7298 | ✓ |

Identical funnel counters across LOW/MED/HIGH MARK cells (slippage does not affect entry detection or admissibility — only PnL). TRADE_PRICE's slightly different counters reflect different stop-fire bars and cooldown re-entry timing; the difference is small and consistent across BTC and ETH.

## 13. P.14 hard-block check results

Per Phase 3c §8.15 / §11.4 / §11.5 / §11.6:

| Check | BTC F1 R MED MARK | ETH F1 R MED MARK |
|------|:-:|:-:|
| F1 emits only STOP / TARGET / TIME_STOP / END_OF_DATA | ✓ | ✓ |
| Zero TRAILING_BREACH / STAGNATION / TAKE_PROFIT exit reasons | ✓ (count = 0) | ✓ (count = 0) |
| Exit-reason accounting identity holds (STOP + TARGET + TIME_STOP + EOD = n) | ✓ | ✓ |
| Funnel accounting identity holds (detected = filled + rej_sd + cooldown) | ✓ (all 4 cells) | ✓ (all 4 cells) |
| Raw stop-distance band [0.60, 1.80] enforcement | ✓ (min=0.6001, max=1.7992) | ✓ (min=0.6002, max=1.7988) |
| Frozen target invariant (recorded `frozen_target_value` = SMA(8)(B)) | ✓ (engine populates from frozen `_F1TradeMetadata.frozen_target` per Phase 3d-B1 wiring) | ✓ |
| Frozen stop invariant (`initial_stop` recorded once at fill, never moved intra-trade) | ✓ (engine never calls `_apply_stop_update` on F1 path) | ✓ |
| Cooldown enforcement (no same-direction re-entry without unwind) | ✓ (engine `can_re_enter` gate hit `blocked_cooldown=6944` BTC; identity holds) | ✓ |
| No look-ahead leakage | ✓ (H0/R3 control bit-for-bit reproduction §4 confirms engine per-bar discipline) | ✓ |
| H0/R3 controls reproduced bit-for-bit before F1 interpretation | ✓ (§4 above) | ✓ |

**All P.14 hard-block invariants PASS.** No bug / escalation report is required. The F1 framework verdict (HARD REJECT) is issued on a clean engine.

## 14. Descriptive H0/R3 cross-family reference comparison

Per Phase 3c §7.4 / §11.9 these deltas are **descriptive cross-family references only; not §10.3-equivalent governing metrics**. F1's HARD REJECT is decided exclusively by the §7.2 self-anchored absolute thresholds (§9 above).

| Symbol | F1 R MED MARK | H0 R MED MARK | R3 R MED MARK | Δ F1−H0 (expR) | Δ F1−R3 (expR) | Δ F1−H0 (n%) | Δ F1−R3 (n%) |
|--------|--------------:|--------------:|--------------:|---------------:|---------------:|-------------:|-------------:|
| BTCUSDT | expR=−0.5227 PF=0.3697 n=4720 | expR=−0.4590 PF=0.2552 n=33 | expR=−0.2403 PF=0.5602 n=33 | −0.0637 | −0.2823 | +14206% | +14206% |
| ETHUSDT | expR=−0.4024 PF=0.4667 n=4826 | expR=−0.4752 PF=0.3207 n=33 | expR=−0.3511 PF=0.4736 n=33 | +0.0728 | −0.0513 | +14524% | +14524% |

**Interpretation (descriptive only):**

- F1's per-trade expR is comparable in magnitude to H0/R3 (within ±0.30 R). The catastrophic problem is volume × per-trade-loss aggregation: F1's ~150× higher trade count multiplies a similar-magnitude per-trade negative expR into catastrophic equity loss.
- F1's BTC expR is slightly worse than H0 (Δ=−0.064) and substantially worse than R3 (Δ=−0.282). On ETH, F1's expR is slightly better than H0 (Δ=+0.073) and slightly worse than R3 (Δ=−0.051).
- The trade-count delta (+14,000% on both symbols) reflects F1's spec firing on every overextension event vs V1's firing only on validated breakout setups.

These deltas reinforce, but do not govern, the §10 HARD REJECT verdict.

## 15. Confirmation that H0/R3 were descriptive only, not governing anchors

Confirmed. Per Phase 3c §7.4 and §11.9, the §7.2 first-execution gate evaluates F1 against **self-anchored absolute thresholds** (BTC MED expR > 0; M1 BTC mean ≥ +0.10 R AND fraction ≥ 50%; ETH MED non-catastrophic; BTC HIGH expR > 0; ETH HIGH non-catastrophic; §10.4 absolute floors). The H0/R3 deltas in §14 are reported as research context only; they do not appear as conditions in §7.2 / §9 / §13. The verdict at §10 is determined entirely by the §7.2 self-anchored thresholds plus the §7.3 catastrophic-floor predicate.

## 16. Confirmation of no project-state changes

No threshold, strategy parameter, project lock, paper/shadow plan, Phase 4 work, live-readiness work, deployment work, MCP server, Graphify integration, `.mcp.json` change, credential creation, or exchange-write authorization occurred in Phase 3d-B2.

| Category | Status |
|----------|--------|
| Phase 3b F1 spec axes (overextension window 8 / threshold 1.75 / mean-reference window 8 / stop-buffer 0.10 / time-stop 8 / stop-distance band [0.60, 1.80]) | LOCKED VERBATIM (consumed unmodified from `MeanReversionConfig` defaults) |
| V1 breakout strategy module | UNCHANGED (control reproduction §4 bit-for-bit) |
| V1 strategy logic, V1 entry/exit machinery, V1 setup predicate, V1 bias filter | UNCHANGED |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH) | PRESERVED VERBATIM |
| §1.7.3 project-level locks (BTCUSDT-primary; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) | PRESERVED VERBATIM |
| Phase 3c §6 run inventory | PRESERVED (4 mandatory R-window cells executed; conditional V skipped per §6.2; no forbidden cells executed) |
| MCP / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Paper/shadow planning | NOT PROPOSED, NOT AUTHORIZED |
| Phase 4 (runtime / state / persistence) work | NOT PROPOSED, NOT AUTHORIZED |
| Live-readiness work, deployment, exchange-write capability, production keys | NOT PROPOSED, NOT AUTHORIZED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `.claude/` directory | UNCHANGED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED |

R3 V1-breakout baseline-of-record per Phase 2p §C.1 stands. H0 V1-breakout framework anchor per Phase 2i §1.7.3 stands. R1a / R1b-narrow / R2 retained-research-evidence stand. R2 framework verdict FAILED — §11.6 cost-sensitivity blocks stands. §11.6 = 8 bps HIGH numerical threshold per Phase 2y closeout stands. Phase 2f §11.3.5 binding rule preserved. Phase 3b F1 spec preserved verbatim per Phase 3c §3 / Phase 3d-A scope.

## 17. Confirmation that no `data/` artifacts were committed

Confirmed. `git status` after the Phase 3d-B2 commits shows zero `data/` entries. The four F1 R-window runs and the four V1 H0/R3 control re-runs wrote into the git-ignored `data/derived/backtests/` tree only. The analysis script wrote `data/derived/backtests/phase-3d-f1-analysis-<run_id>.json`, which is also git-ignored. No `git add data/` was executed.

## 18. Recommendation for next operator decision

**F1 family research is concluded as FAILED (HARD REJECT).** F1 is retained as research evidence per the same Phase 2x / Phase 2y precedent that retained R1a / R1b-narrow / R2 as research evidence.

**Recommended next operator decision:** **CLOSE the F1 research arc.** No subsequent F1 phase is proposed.

What this means:

- **F1 is not a baseline-of-record candidate.** R3 remains the V1-breakout baseline-of-record per Phase 2p §C.1.
- **F1 is not eligible for paper/shadow consideration** (which remains operator-policy-deferred and would in any case require a PROMOTE outcome).
- **F1 mechanism evidence is partial:** the SMA(8) target-exit subset is mechanism-consistent and cost-survivable in isolation (M3 PASS); the wider F1 strategy-as-specified is not. This M3-only mechanism evidence may inform any hypothetical future F1-prime spec consideration in a separately-authorized phase, but Phase 3d-B2 does not propose such a phase.
- **The Phase 2x family-review conclusion stands:** the V1 breakout family is at its useful ceiling; F1 (the Phase 3a rank-1 near-term family candidate) does not extend the framework's edge. No new strategy family is currently proposed.
- **Project state is preserved:** the operator's standing options remain (a) approve eventual paper/shadow on the existing R3 baseline-of-record (subject to Phase 4 runtime / state / persistence implementation, which is not currently authorized), (b) authorize a different new-family research arc (would require a separately-authorized Phase 3a-style discovery memo + Phase 3b spec memo + Phase 3c execution-planning memo + Phase 3d implementation phases), or (c) hold at the current Phase 3d-B2 boundary indefinitely.

Phase 3d-B2 makes no recommendation for any of (a), (b), or (c); the decision is operator authority. **Phase 3d-B2 is the terminal phase for F1.** No subsequent F1 phase is proposed.

---

**End of Phase 3d-B2 execution-diagnostics report.** **F1 framework verdict: HARD REJECT.** Four mandatory R-window runs executed; conditional V-window run skipped per §6.2; first-execution gate evaluated; M1/M2/M3 mechanism checks computed; §8 mandatory diagnostics produced; P.14 hard-block invariants PASS. F1 is retained as research evidence; the F1 family is concluded as FAILED. No project-state change. No `data/` commits. R3 remains V1-breakout baseline-of-record; H0 remains framework anchor; R1a / R1b-narrow / R2 retained-research-evidence stand; §11.6 = 8 bps HIGH per Phase 2y closeout preserved verbatim. Phase 3d-B2 is terminal for F1; no subsequent F1 phase proposed. Awaiting operator review.
