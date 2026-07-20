# Phase 4bn-AZ — CF-1 Realized-Volatility Substrate-Test Execution and Verdict

## 1. Phase identity

Phase 4bn-AZ — CF-1 Realized-Volatility Substrate-Test Execution. The first and only
authorized execution of the CF-1 development experiment frozen and merged by Phase 4bn-AY.
Code + tests + bounded local data-reading + local gitignored artefacts + committed report
phase. **Not** a trading-strategy, PnL, backtest, reserve-spend, paper/shadow/live, or
exchange/API phase. Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md`.

Branch: `phase-4bn-az/cf1-realized-volatility-substrate-test-execution`.

## 2. Authorization

Executed under the separate explicit operator authorization that constitutes the Phase
4bn-AY §37(a) precondition. The operator accepted the Phase 4bn-AY M0.3 mapping solely for
the non-strategy mechanism claim *incremental out-of-sample QLIKE skill over the fixed
HAR-style realized-variance baseline*. That acceptance authorized only the frozen
development-level scientific comparison. It cleared no directional strategy through M0, no
profitability, no economic materiality, no PnL, no backtest, no execution feasibility, no
cost realism, and no market-state filter.

Global state is unchanged: `research_eligible = false`; `eligibility_gate_status = pending`;
all authorization flags false; Phase 4aw `flip_research_eligible(...)` remains always-raising
and was never invoked.

## 3. Exact SHAs

| Item | SHA |
|---|---|
| Base `main` (== `origin/main` at branch time and at completion) | `e65feb849c8020b5e157d1c472b1a075244c7d9d` |
| Phase 4bn-AY merge commit | `cd5a3b7128bb7bc8d887fb4c7ea1c1538e5b1305` |
| Phase 4bn-AY final scientific-contract tip | `0fb560656aa9b50cf110602e15be8222b7343623` |
| **AZ implementation commit (evidence-bearing code SHA)** | `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1` |

The implementation commit was created, pushed, and verified equal to
`origin/phase-4bn-az/...` **before** the first market-data byte was opened. All artefacts are
stamped with `code_commit_sha = 05fa63a8bf8c9b1fe386cc4ab67805046ae418b1`. No Phase 4bn-AY
file was modified.

## 4. Preflight result

All pre-data gates **PASSED**; no `PREFLIGHT_FAILURE` occurred.

| Gate | Result |
|---|---|
| Base state `HEAD == main == origin/main == e65feb84…`, only `.claude/scheduled_tasks.lock` untracked | PASS |
| Storage floor (`D:` free ≥ 500 GiB) | PASS — **1154.11 GiB** free |
| Deterministic synthetic timestamp-boundary proof (synthetic rows only) | PASS — 14/14 checks |
| Source-partition presence (244 normalized + 244 feature Parquet + sidecars) | PASS |
| Targeted tests / full microstructure suite / ruff / mypy / full pytest | PASS (§9) |
| Implementation commit exists, pushed, local == origin, no tracked changes | PASS |

## 5. Data scope actually opened

- **Exactly 244 UTC dates**: 2024-03-01 .. 2024-10-31 **excluding 2024-10-01**.
- **Normalized (prices / RV):** `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o`
  — 244 daily Parquet partitions, **340,447,363 rows read**.
- **Features (three 60s snapshots):** `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s`
  — 244 daily Parquet partitions, **340,447,363 rows read**.
- Every opened Parquet was integrity-verified against its committed `.sha256` sidecar before
  reading; any mismatch would have failed closed.
- **Not opened:** 2024-10-01; 2024-11-01..2024-11-15 (`UNUSED_NON_RESERVE_BUFFER`); 2024-11-16;
  2024-11-17..2024-11-30 (consumed holdout); 2024-12-01..2025-02-28 (v002 terminal);
  2025-02-14..2025-02-28 (v002 sealed). No raw labels were read; CF-1 built its own RV target
  from price. No network, API, endpoint, credential, `.env`, MCP, or acquisition was used.

## 6. Implementation summary

Three source modules plus one orchestration script (all scientific logic in `src/`, the
script holds orchestration and the bounded read only):

- `src/prometheus/research/microstructure/cf1_realized_volatility_v001.py` — frozen constants;
  the single canonical operator `P_at(u)` (`source_transact_time_ms ≤ u`, greatest-`row_index`
  tie); the causal completed-interval `(a, b]` RV kernel on the 1-minute UTC grid; covered-minute
  counting under `τ_{k-1} < ts ≤ τ_k`; HAR `(t − L, t]` assembly; origin validity;
  no-forbidden-partition guards; the synthetic boundary proof.
- `src/prometheus/research/microstructure/cf1_evaluation_v001.py` — expanding anchored
  walk-forward (one fit per block), one-day embargo (purge subsumed), train-only log + z-score
  (population std, `ddof = 0`), OLS via `numpy.linalg.lstsq`, the numerical guards, QLIKE,
  `d_{i,t}` / `D_i` / `Δ_equal` / `ρ`, MSE and MZ R², the stratified moving-block bootstrap, and
  P1–P4 verdict routing.
- `src/prometheus/research/microstructure/cf1_artifacts_v001.py` — deterministic JSON, compact
  Parquet, `.sha256` sidecars, inventory, provenance and non-authorization flags, validators.
- `scripts/phase4bn_az_cf1_realized_volatility_execution.py` — preflight, proof, SHA pin,
  access-start sentinel, bounded read, target-layer build, leakage proof, evaluation, artefact
  writes, validation, verdict emission.

For bounded memory the `P_at` operator is applied once per UTC-minute boundary per accessible
segment (≈351k boundaries) rather than per trade; prices are carried as decimal strings and cast
to `Decimal` only at the selected boundaries, then to `float64` only at the `ln` step. Carry-forward
is reset at each accessible-segment start, so no price or feature value is ever stitched across the
2024-10-01 embargo or an outer access edge.

## 7. Proof results

**Deterministic synthetic timestamp-boundary proof — PASSED (before any market data was opened).**
Artefact: `proofs/cf1_timestamp_boundary_proof_v001__v001__1784558563200__05fa63a8bf8c.json`
(sha256 `ecdf0fcbad2e192968c0bb9960c8c9117813fd217e94c4a938f201e8aff77248`), synthetic rows only,
`market_data_opened = false`, `reserve_touched = false`. All 14 checks passed, including:
`(09:00, 10:00]` captures the boundary jump into 110; `(10:00, 11:00]` starts from `G_0 = 110`
and does not re-count it; `RV_target(10:00)` excludes the pre-10:00→10:00 jump (first return
exactly 0); a trade exactly at 11:00 is included in `(10:00, 11:00]`; `RV_h(10:00)` may include
the exactly-10:00 trade; the feature snapshot at 10:00 may include the 10:00 row; the
same-timestamp greatest-`row_index` tie selects 110 over 105; a strict-`<` / left-limit operator
demonstrably omits the boundary jump; `2024-10-31T22:00` valid vs `2024-10-31T23:00` invalid; and
the 2024-11-01 and 2024-10-01 partitions are rejected before open.

**Leakage / split / coverage proof — PASSED**, validated before any metric computation.
Artefact: `proofs/cf1_leakage_split_coverage_proof_v001__v001__1784559571783__05fa63a8bf8c.json`
(sha256 `c398d9ac6e1a4dabb86861d4f6d2a9c2c83f651a0d6cd56f090452646b0fba1e`).
`partitions_opened_count = 244`; `october_1_opened = false`; `november_or_later_opened = false`;
`consumed_holdout_opened = false`; `terminal_opened = false`; `sealed_opened = false`;
`october_31_23_00_retained = false`.

## 8. Source identity

| Family | Identity |
|---|---|
| Symbol | `BTCUSDT` |
| Prices / RV | `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o` (`transact_time_ms`, `price` decimal string, `row_index`) |
| Feature snapshots | `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s` (`feature_timestamp_ms`, `row_index`, the three 60s columns) |

Per-partition sha256 values for all 244 normalized and 244 feature partitions are recorded in
the leakage proof artefact (`normalized_partition_shas`, `feature_partition_shas`).

## 9. Quality gates

| Gate | Result |
|---|---|
| `pytest` targeted CF-1 (4 modules) | 56 passed |
| `pytest tests/research/microstructure` | all passed |
| `pytest` (full suite) | **3342 passed, 2 failed, 1 skipped** in 83.8 s |
| `ruff check` (AZ files) | All checks passed |
| `ruff format --check` (AZ files) | 8 files already formatted |
| `mypy --strict` | **12 errors, 0 of them in AZ code** |

**Pre-existing baseline, exact comparison.** The two `pytest` failures are
`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and
`::test_real_2026_03_ethusdt` (`KeyError: 'trade_count'` in
`src/prometheus/research/data/storage.py:232`), a klines/backtest path AZ never touches. The 12
`mypy --strict` errors are in `labels_manifest_v002.py`, `multiday_feature_gate_checks.py`,
`ml_baseline_models_v002.py`, `ml_baseline_dataset_v002.py`, and `feature_drift_v002.py` — five
files AZ never touches. AZ modified **zero** existing tracked files (its whole diff is added
files), so the tracked tree at gate time was byte-identical to base `main`; both failure sets are
therefore the base-`main` baseline. **AZ introduced 0 new test failures and 0 new type errors**,
and added 56 passing tests. `ruff format --check .` over the whole repo reports 235 pre-existing
non-conforming files; all 8 AZ files are conforming.

## 10. Counts

| Quantity | Value |
|---|---|
| Source partitions opened | 244 (of 244 openable) |
| Rows read — normalized | 340,447,363 |
| Rows read — features | 340,447,363 |
| Candidate hourly origins | 5,854 |
| **Valid paired origins** | **5,516** |
| Invalid — `har_unavailable` | 336 |
| Invalid — `har_coverage_failure` | 2 |
| Zero-RV origins | 0 |
| Elapsed | 1009.2 s |

The 336 `har_unavailable` origins are the deterministic warmup consequence of the frozen 168-hour
HAR-week lookback at each accessible-segment start (the first ~7 days of segment A from
2024-03-01, and of segment B from 2024-10-02); they are not data defects. No origin was manually
removed.

**Per-block valid evaluation origins (all ≥ the frozen minimum of 100) and training origins
(all ≥ the frozen minimum of 70):**

| Block | Dates | Valid eval origins `n_i` | Training origins |
|---|---|---|---|
| B1 | 2024-04-01..2024-04-30 | 720 | 551 |
| B2 | 2024-05-01..2024-05-31 | 744 | 1,271 |
| B3 | 2024-06-01..2024-06-30 | 720 | 2,015 |
| B4 | 2024-07-01..2024-07-31 | 744 | 2,735 |
| B5 | 2024-08-01..2024-08-31 | 744 | 3,479 |
| B6 | 2024-09-01..2024-09-30 | 719 | 4,223 |
| B7 | 2024-10-02..2024-10-31 | 550 | 4,966 |

The block-size and training-size minimums were therefore **met in every block**. The run did not
fail on data sufficiency, coverage, leakage, or split integrity.

## 11. All seven block results

The run **fail-closed at the augmented-model numerical guard in every block**, before any loss was
computed.

| Block | `n_train` | `n_eval` | Baseline condition no. | Baseline rank | Augmented condition no. | Guard outcome |
|---|---|---|---|---|---|---|
| B1 | 551 | 720 | 6.172e+02 | 4 / 4 | **1.038e+16** | `augmented_condition_number_exceeded` |
| B2 | 1,271 | 744 | 4.058e+02 | 4 / 4 | **1.019e+16** | `augmented_condition_number_exceeded` |
| B3 | 2,015 | 720 | 3.807e+02 | 4 / 4 | **1.037e+16** | `augmented_condition_number_exceeded` |
| B4 | 2,735 | 744 | 3.418e+02 | 4 / 4 | **1.035e+16** | `augmented_condition_number_exceeded` |
| B5 | 3,479 | 744 | 3.682e+02 | 4 / 4 | **1.065e+16** | `augmented_condition_number_exceeded` |
| B6 | 4,223 | 719 | 3.442e+02 | 4 / 4 | **1.064e+16** | `augmented_condition_number_exceeded` |
| B7 | 4,966 | 550 | 3.634e+02 | 4 / 4 | **1.087e+16** | `augmented_condition_number_exceeded` |

The frozen threshold is `condition number > 1e10 ⇒ CF1_INVALID_RUN` (contract §19). The **baseline**
HAR design was well conditioned everywhere (3.4e+02 – 6.2e+02, full rank 4). The **augmented**
design exceeded the threshold by roughly six orders of magnitude in all seven blocks.

**No QLIKE, no `d_{i,t}`, no `D_i`, no `Δ_equal`, no `ρ`, no MSE, no MZ R², and no bootstrap were
computed.** The guard is evaluated before fitting and scoring, so the run never reached the loss
stage. Any zero appearing in the aggregate block of the model-run manifest is an
uninitialised default, **not** a measured value, and must not be read as a result.

## 12. Root cause (deterministic, verified)

The three features frozen by the Phase 4bn-AY contract §11 are

- `x1 = rolling_aggtrade_count_60s`,
- `x2 = rolling_quantity_sum_60s`,
- `x3 = rolling_quantity_mean_60s`,

and the contract §13 freezes a natural-logarithm transform on each. But by the committed feature
definition `rolling_quantity_mean_60s` is the arithmetic mean of the same 60-second window whose
sum and count are the other two features, i.e. `x3 = x2 / x1`. Therefore

```
ln(x3) ≡ ln(x2) − ln(x1)
```

holds **identically**, so the three log-features span only a two-dimensional space. With the
intercept and the three HAR log-variance regressors, the augmented design matrix has 7 columns
but rank 6 — an exact structural rank deficiency, which manifests numerically as a condition
number at the float64 noise floor (~1e16).

**Verified arithmetically on the frozen target layer** (no new market data read): across all
5,516 valid origins,

```
max | ln(x3) − ( ln(x2) − ln(x1) ) | = 3.33e-14      (machine precision)
mean| ln(x3) − ( ln(x2) − ln(x1) ) | = 3.51e-15
```

This is a property of the **preregistered design**, not of the data, the implementation, the
split, the timestamp semantics, or the substrate. Standardization does not remove it: an
affine rescaling of exactly collinear columns remains exactly collinear. The frozen contract
simultaneously mandates (a) these three features, (b) the log transform, and (c) the
`condition number > 1e10 ⇒ CF1_INVALID_RUN` guard — and (a) ∧ (b) necessarily trips (c). The
experiment as frozen could not have produced a scientific pass or fail on any data.

## 13. P1 / P2 / P3 / P4

| Criterion | Value | Basis |
|---|---|---|
| P1 (`Δ_equal > 0`) | **not evaluable** (recorded false) | `Δ_equal` never computed |
| P2 (≥ 6 of 7 `D_i > 0`) | **not evaluable** (recorded false) | no `D_i` computed |
| P3 (`LB_95 > 0`) | **not evaluable** (recorded false) | bootstrap never run |
| P4 (run validity) | **FALSE** | augmented numerical guard tripped in all 7 blocks |

P4 fails on its own terms, which routes the run to `CF1_INVALID_RUN` before P1–P3 have any
meaning. P1–P3 are recorded as `false` only because the run carries no computed values for them;
they are **not** negative scientific findings.

## 14. Exact verdict

```
CF1_INVALID_RUN
```

Exact result state:

```
CF1_INVALID_RUN__NO_SCIENTIFIC_CLAIM__NO_RERUN_AUTHORIZED__SEPARATE_CORRECTIVE_PHASE_REQUIRED__RESERVES_UNTOUCHED
```

This is the verdict the frozen decision routing requires: a numerical failure (condition number
`> 1e10`) is a technical invalidation, **not** a fail and **not** a pass (contract §31; checklist
§3–§4).

## 15. Plain-language interpretation

The experiment did not run to a scientific answer, and the reason is a defect in the frozen
experimental design rather than anything about the market data.

Everything upstream of the model worked exactly as preregistered. The 244 authorized days were
opened and integrity-checked, 340.4 million trade rows were reduced to an hourly realized-variance
target layer, 5,516 valid forecast origins were produced with every block comfortably above its
minimum size, and both the timestamp-boundary proof and the leakage/split/coverage proof passed.
The plain HAR baseline fitted cleanly in all seven blocks.

The augmented model could not be fitted, because two of its three microstructure inputs already
determine the third. Mean trade size is total volume divided by trade count, so once the design
takes logarithms, "log mean size" is exactly "log volume minus log count" — a redundant column
carrying no independent information. The augmented regression therefore had no unique solution,
and the preregistration's own numerical safety check correctly refused to proceed rather than
silently return an arbitrary one of infinitely many coefficient vectors.

The honest reading is: **CF-1 as frozen was not a runnable experiment.** It says nothing about
whether aggTrades microstructure carries incremental realized-volatility information. That
question remains open and untested.

## 16. Exact consequence

Per Phase 4bn-AY §33 and the checklist §3:

- **No scientific claim is made.** This is neither a pass nor a fail, and must never be converted
  into one.
- All evidence classifications and project locks are preserved exactly.
- **Stop.** No rerun of this experiment is authorized — not with corrected code, not with a
  different feature set, not with a relaxed guard.
- A **separate corrective phase and a new operator authorization** are required before any further
  CF-1 work. Because the defect is in the merged Phase 4bn-AY scientific contract itself, a
  corrective phase would have to be a **docs-only contract-correction phase** that re-preregisters
  the feature contract (for example, by dropping the redundant third feature, or by replacing it
  with a genuinely independent sign-invariant column) *before* any further execution is proposed.
  This report does **not** authorize that phase, does not choose its design, and does not
  pre-approve any particular remedy.
- The one authorized evidence-bearing run has been consumed. The artefacts are preserved and
  hash-validated.

## 17. Explicit limitations

- This run establishes **nothing** about the CF-1 hypothesis. `H0` was neither rejected nor
  supported.
- It does **not** show that the microstructure features are uninformative. It shows only that,
  as specified, they are mutually redundant and cannot be jointly estimated.
- It does **not** narrow the magnitude lane. The Phase 4bn-AY §32 fail consequence explicitly does
  **not** apply, because there was no valid fail.
- It does **not** establish direction, profitability, ability to clear the locked 8 bps/side ·
  16 bps round trip, tradability, sizing, gating, execution timing, or strategy readiness.
- The baseline condition numbers and the origin/coverage counts are diagnostic facts about the
  run, not scientific results about the substrate.
- No secondary metric exists to report; none was computed, and none could rescue anything.

## 18. No-reserve statement

`No evidence reserve was spent by Phase 4bn-AZ.` The v002 terminal window
(2024-12-01..2025-02-28) and the v002 sealed test (2025-02-14..2025-02-28) remain
`UNTOUCHED_RESERVED` and were never opened. The consumed pre-v002 internal holdout
(2024-11-17..2024-11-30) remains `CONSUMED` and descriptive-only and was never opened. The
`UNUSED_NON_RESERVE_BUFFER` (2024-11-01..2024-11-15) was never opened. Recorded and verified:
`v002_terminal_window_read = false`, `sealed_test_split_touched = false`, `test_rows_loaded = 0`,
`consumed_holdout_opened = false`, `november_buffer_opened = false`.

## 19. No-trading statement

`No target generation for trading, signal generation, strategy, PnL analysis, backtest, paper,
shadow, live, or exchange-write execution was performed or is authorized by Phase 4bn-AZ.`
CF-1 is a non-directional realized-variance magnitude test; it produced no directional object and
no tradable object. `network_used = false`, `data_acquisition_used = false`, and all eight
non-authorization flags (`ml_authorized`, `diagnostics_authorized`, `strategy_authorized`,
`signals_authorized`, `pnl_authorized`, `backtest_authorized`, `live_authorized`,
`exchange_write_authorized`) are `false`.

## 20. Environment

Python 3.12.4; NumPy 2.4.4; PyArrow 23.0.1. Command:
`uv run python scripts/phase4bn_az_cf1_realized_volatility_execution.py --run`.
Run completed 2026-07-20T14:59:32.321546Z (artefact filenames carry the run's Unix-ms stamps).
