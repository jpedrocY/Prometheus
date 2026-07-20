# Phase 4bn-AZ — Merge Closeout

## 1. Phase identity

Phase 4bn-AZ — CF-1 Realized-Volatility Substrate-Test Execution. The first and only authorized
execution of the CF-1 development experiment frozen and merged by Phase 4bn-AY. Branch:
`phase-4bn-az/cf1-realized-volatility-substrate-test-execution`.

## 2. Phase type and merge action

Code + tests + bounded local data-reading + local gitignored artefacts + committed reports. The
merge action brings eleven Phase 4bn-AZ files — plus this merge-closeout — onto `main` via an
explicit no-fast-forward merge commit, followed by one narrow SHA-finalization update of this file.

**This merge is a recordkeeping and reproducibility action only.** It changes no data, no manifest,
no eligibility state, no verdict, no reserve, and no lock. It authorizes no execution.

`Merging Phase 4bn-AZ records the implementation, artefacts, proof results, and invalid-run evidence; it is not a scientific endorsement and does not convert the invalid run into a pass or fail.`

## 3. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — the phase executed
the one authorized evidence-bearing run of the currently-selected research arc, so it carries the
highest ceremony tier even though it mutates no eligibility, manifest, verdict, reserve, or lock.

## 4. Source and target branches

- **Source:** `phase-4bn-az/cf1-realized-volatility-substrate-test-execution`
- **Target:** `main`

## 5. Pre-merge `main` / base SHA

`e65feb849c8020b5e157d1c472b1a075244c7d9d` (`HEAD == main == origin/main` at merge time; the tip
after the Phase 4bn-AY merge-closeout SHA-finalization commit). Verified in sync before any
mutation. The only untracked item was the transient `.claude/scheduled_tasks.lock`, which was not
staged, modified, deleted, cleaned, or committed.

## 6. Complete Phase 4bn-AZ source-branch commit history

Three commits on the source branch after the base, preserved exactly — not squashed, reordered,
rebased, amended, or rewritten:

| # | SHA | Commit message | Role |
|---|---|---|---|
| 1 | `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1` | `feat(phase-4bn-az): implement CF-1 substrate execution` | **Frozen evidence-bearing implementation.** Created, pushed, and verified equal to origin **before** the first market-data byte was opened; stamped into every AZ artefact as `code_commit_sha`. |
| 2 | `00dfefdd82e8a31f86ff7ca6393ed76350d906d6` | `research(phase-4bn-az): record CF-1 execution verdict` | Adds the execution-and-verdict report and the artefact/leakage/split-validation report. |
| 3 | `a493b46b081534a7acaee2a6c0ba92a7a8b98d07` | `docs(phase-4bn-az): add closeout` | Adds the Phase 4bn-AZ closeout; final branch tip before merge-closeout creation. |

This merge-closeout is the **fourth** commit on the source branch.

## 7. Final pre-merge scientific branch-tip SHA

`a493b46b081534a7acaee2a6c0ba92a7a8b98d07` — the approved Phase 4bn-AZ evidence state at merge time.

## 8. Merge-closeout branch commit SHA

`eb7298012c8e30f00a25f45eef3da2c0095163be` — the commit on the AZ branch that adds this
merge-closeout file (`docs(phase-4bn-az): add merge closeout`). This is the **fourth** commit on the
source branch.

## 9. No-fast-forward merge commit SHA

`8e82e185a0def318acd2ec42fcb73337edc67b51` — the no-fast-forward merge commit created on `main`
(`research(phase-4bn-az): merge CF-1 invalid-run evidence`), made by the `ort` strategy with 12
added files and 5,135 insertions.

## 10. SHA-finalization commit statement

SHA-finalization commit SHA:
this update (`docs(phase-4bn-az): finalize merge closeout shas`);
its exact SHA equals the resulting final `main` / `origin/main` tip and is
recorded in the final operator report and Git log. Its own SHA is not embedded inside the
commit that creates it.

## 11. Final `main` / `origin/main` statement

After the SHA-finalization commit is pushed, final `main` and `origin/main` will both equal the
SHA-finalization commit SHA (§10). `HEAD == main == origin/main` at completion.

## 12. Merge method

`git merge --no-ff` with the default `ort` strategy and an explicit merge commit. No fast-forward,
no squash, no rebase, no amend, no history rewrite, no hook skipping, no signing disablement, no
force push. Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 13. Files brought forward

Eleven Phase 4bn-AZ files, all additions:

**Source (3)**
1. `src/prometheus/research/microstructure/cf1_realized_volatility_v001.py`
2. `src/prometheus/research/microstructure/cf1_evaluation_v001.py`
3. `src/prometheus/research/microstructure/cf1_artifacts_v001.py`

**Script (1)**
4. `scripts/phase4bn_az_cf1_realized_volatility_execution.py`

**Tests (4)**
5. `tests/research/microstructure/test_cf1_realized_volatility_v001.py`
6. `tests/research/microstructure/test_cf1_evaluation_v001.py`
7. `tests/research/microstructure/test_cf1_artifacts_v001.py`
8. `tests/research/microstructure/test_cf1_no_network_v001.py`

**Documents (3)**
9. `docs/00-meta/implementation-reports/2026-07-17_phase-4bn-az_cf1-execution-and-verdict.md`
10. `docs/00-meta/implementation-reports/2026-07-17_phase-4bn-az_cf1-artefact-leakage-and-split-validation.md`
11. `docs/00-meta/implementation-reports/2026-07-17_phase-4bn-az_closeout.md`

This merge-closeout file is added on the AZ branch before the merge, so the merged base-to-final
diff carries **twelve** added files in total. **No `data/microstructure/` file and no
`data/research/` file was modified, added, or committed.**

## 14. Additions-only confirmation

Confirmed additions-only. `git diff --name-status main..AZ` shows exactly **eleven `A` entries and
no `M` / `D` / `R` entries**. No existing file was modified, renamed, or deleted by the AZ branch or
by the merge. No pre-existing source, test, script, config, schema, manifest, gate report, sidecar,
split file, prior report, README, `current-project-state.md`, M0 memo, evidence-ledger, phase-gate,
technical-debt-register, or process standard changed. `pyproject.toml` and `uv.lock` are unchanged.

## 15. Diff summary

Pre-merge branch diff (`main..AZ`), `git diff --stat`:

```text
 11 files changed, 4548 insertions(+)
```

`git diff --check main..AZ` → clean (no whitespace errors). The merged base-to-final diff adds the
same eleven files plus this merge-closeout (twelve added files), then one later modification of this
merge-closeout solely to finalize the exact SHAs. The diff matches the expected change set from the
authorization prompt exactly.

## 16. Phase 4bn-AY contract lineage

Phase 4bn-AY froze and merged the entire CF-1 development experiment before any market data was
opened: the causal completed-interval `(a, b]` convention with the single operator `P_at(u)`
(`source_transact_time_ms ≤ u`, greatest-`row_index` tie); the 60-minute horizon at top-of-UTC-hour
non-overlapping origins; `y = ln(RV + 1e-16)`; the HAR-style OLS baseline on `RV_h` / `RV_d` /
`RV_w`; the nested augmented OLS adding exactly three sign-invariant 60s microstructure features;
QLIKE with the `v = RV + ε` / `h = max(exp(ŷ), ε)` safeguard; seven monthly evaluation blocks;
`Δ_equal`; the stratified-by-block moving-block bootstrap (`B = 10,000`, seed `20260715`); the
6-of-7 block-consistency rule; and the numerical guards including
`condition number > 1e10 ⇒ CF1_INVALID_RUN`.

- Phase 4bn-AY merge commit: `cd5a3b7128bb7bc8d887fb4c7ea1c1538e5b1305`
- Phase 4bn-AY final scientific-contract tip: `0fb560656aa9b50cf110602e15be8222b7343623`

**No Phase 4bn-AY file was modified by Phase 4bn-AZ or by this merge**
(`git diff main..AZ -- <the five AY documents>` is empty).

## 17. Execution authorization boundary

Phase 4bn-AZ ran under the separate explicit operator authorization that satisfied the Phase 4bn-AY
§37(a) precondition. The operator accepted the Phase 4bn-AY M0.3 mapping **solely** for the
non-strategy mechanism claim *incremental out-of-sample QLIKE skill over the fixed HAR-style
realized-variance baseline*. That acceptance authorized only the frozen development-level scientific
comparison. It cleared no directional strategy through M0, no profitability, no economic
materiality, no PnL, no backtest, no execution feasibility, no cost realism, and no market-state
filter. Global state is unchanged: `research_eligible = false`; `eligibility_gate_status = pending`;
all authorization flags false; Phase 4aw `flip_research_eligible(...)` always-raising and never
invoked.

## 18. Exact data scope

**Authorized and opened: exactly 244 UTC dates**, 2024-03-01 through 2024-10-31, **excluding
2024-10-01**.

| Source family | Role | Rows read |
|---|---|---|
| `microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o` | prices / RV | **340,447,363** |
| `microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s` | feature snapshots | **340,447,363** |

Every opened Parquet was verified against its committed `.sha256` sidecar **before** its rows were
read; a mismatch would have failed closed. Partition selection used an explicit 244-date allowlist
plus a fail-closed guard on every path construction, so no glob or broad scan could reach a
forbidden partition.

**Not opened:** 2024-10-01; 2024-11-01 through 2024-11-15; 2024-11-16; 2024-11-17 through
2024-11-30; 2024-12-01 onward; the v002 terminal window; the v002 sealed test; prior labels; any
unrelated symbol; any order-book / top-of-book source; funding; open interest; liquidation; and
mark/index-price data. No acquisition, no network, no API, no credentials.

## 19. Exact proof results

**Synthetic timestamp-boundary proof — PASSED before any market-data file was opened.** Synthetic
rows only; `market_data_opened = false`; `feature_data_opened = false`; `reserve_touched = false`;
**14 of 14 checks passed**; `timestamp_boundary_proof_passed = true`. Artefact
`proofs/cf1_timestamp_boundary_proof_v001__v001__1784558563200__05fa63a8bf8c.json`, SHA256
`ecdf0fcbad2e192968c0bb9960c8c9117813fd217e94c4a938f201e8aff77248`.

**Leakage / split / coverage proof — PASSED before model fitting or metric computation.**
`leakage_split_coverage_proof_passed = true`; `partitions_opened_count = 244`;
`october_1_opened = false`; `november_or_later_opened = false`; `consumed_holdout_opened = false`;
`terminal_opened = false`; `sealed_opened = false`; `october_31_23_00_retained = false`. The final
live covered-minute predicate was `τ_{k-1} < ts ≤ τ_k` with threshold 30 of 60. Artefact
`proofs/cf1_leakage_split_coverage_proof_v001__v001__1784559571783__05fa63a8bf8c.json`, SHA256
`c398d9ac6e1a4dabb86861d4f6d2a9c2c83f651a0d6cd56f090452646b0fba1e`.

## 20. Exact origin counts

| Quantity | Value |
|---|---|
| Candidate hourly origins | 5,854 |
| **Valid paired origins** | **5,516** |
| Invalid — `har_unavailable` | 336 |
| Invalid — `har_coverage_failure` | 2 |
| Zero-RV origins | 0 |

Per-block evaluation and training origin counts:

| Block | Dates | Valid eval origins | Training origins |
|---|---|---|---|
| B1 | 2024-04-01..2024-04-30 | 720 | 551 |
| B2 | 2024-05-01..2024-05-31 | 744 | 1,271 |
| B3 | 2024-06-01..2024-06-30 | 720 | 2,015 |
| B4 | 2024-07-01..2024-07-31 | 744 | 2,735 |
| B5 | 2024-08-01..2024-08-31 | 744 | 3,479 |
| B6 | 2024-09-01..2024-09-30 | 719 | 4,223 |
| B7 | 2024-10-02..2024-10-31 | 550 | 4,966 |

**Every evaluation block exceeded the frozen minimum of 100. Every training set exceeded the frozen
minimum of 70.** The 336 `har_unavailable` origins are the deterministic 168-hour HAR-week warmup at
each accessible-segment start, not data defects; no origin was manually removed.

The run did **not** invalidate on data sufficiency, split integrity, timestamp semantics, coverage,
source integrity, reserve access, or leakage.

## 21. Exact numerical guard result

The **baseline** HAR design was full rank (`4 / 4`) and well conditioned in all seven blocks. The
**augmented** design invalidated in every block at the frozen condition-number guard.

| Block | Baseline condition number | Baseline rank | Augmented condition number |
|---|---|---|---|
| B1 | `6.172e+02` | 4 / 4 | `1.038e+16` |
| B2 | `4.058e+02` | 4 / 4 | `1.019e+16` |
| B3 | `3.807e+02` | 4 / 4 | `1.037e+16` |
| B4 | `3.418e+02` | 4 / 4 | `1.035e+16` |
| B5 | `3.682e+02` | 4 / 4 | `1.065e+16` |
| B6 | `3.442e+02` | 4 / 4 | `1.064e+16` |
| B7 | `3.634e+02` | 4 / 4 | `1.087e+16` |

Frozen guard: `condition number > 1e10 ⇒ CF1_INVALID_RUN`.

**No augmented model was fitted. No paired forecasts were produced. No
`cf1_paired_model_predictions_v001` artefact was written.**

## 22. Exact algebraic root cause

The Phase 4bn-AY contract froze `x1 = rolling_aggtrade_count_60s`,
`x2 = rolling_quantity_sum_60s`, and `x3 = rolling_quantity_mean_60s`, and required a natural
logarithm on each. By the committed feature definition `x3 = x2 / x1`, therefore
`ln(x3) ≡ ln(x2) − ln(x1)`. The three transformed features span only two dimensions. With the
intercept, three HAR regressors, and three transformed microstructure regressors, the augmented
matrix has seven columns but **structural rank six**.

Verified on the frozen target layer across all 5,516 valid origins:

```
max  |ln(x3) − (ln(x2) − ln(x1))| = 3.33e-14
mean |ln(x3) − (ln(x2) − ln(x1))| = 3.51e-15
```

`The identity ln(rolling_quantity_mean_60s) = ln(rolling_quantity_sum_60s) − ln(rolling_aggtrade_count_60s) made the augmented design non-identifiable under the frozen feature contract.`

This is an **algebraic defect in the frozen Phase 4bn-AY design**. It is **not** a data defect, a
timestamp defect, a split defect, a leakage defect, a substrate finding, or an implementation
defect. Standardization cannot remove exact linear dependence: an affine rescaling of exactly
collinear columns remains exactly collinear.

## 23. Exact metrics-not-computed statement

`No QLIKE, d_{i,t}, D_i, Δ_equal, ρ, MSE, Mincer–Zarnowitz R², bootstrap distribution, or LB_95 was computed.`

The guard is evaluated before fitting and scoring, so the run never reached the loss stage. No
per-origin losses exist.

`P1, P2, and P3 were not evaluable; any false or zero placeholder is not a negative scientific finding.`

P4 is false because the augmented numerical guard invalidated. Any zero appearing in the aggregate
block of the model-run manifest is an uninitialised default, not a measured value.

## 24. Exact verdict

```
CF1_INVALID_RUN
```

`Phase 4bn-AZ produced CF1_INVALID_RUN, not CF1_VALID_FAIL and not CF1_VALID_PASS.`

## 25. Exact Phase 4bn-AZ result state

```
CF1_INVALID_RUN__NO_SCIENTIFIC_CLAIM__NO_RERUN_AUTHORIZED__SEPARATE_CORRECTIVE_PHASE_REQUIRED__RESERVES_UNTOUCHED
```

## 26. Correct no-scientific-claim interpretation

`The run produced no scientific test of the CF-1 hypothesis because the preregistered transformed feature set was structurally rank deficient.`

The correct interpretation is: **the preregistered augmented model was structurally non-identifiable
because the transformed feature set contained an algebraic redundancy; the run produced no
scientific test of the CF-1 hypothesis.**

An invalid run is not interpretable scientifically — neither a pass nor a fail — and must never be
converted into one. `H0` was neither rejected nor supported. The result does **not** show that the
aggTrades microstructure features are uninformative about future realized-volatility magnitude; it
shows only that, as frozen, they are mutually redundant and cannot be jointly estimated. The
substrate remains scientifically untested under a valid estimable specification.

`The Phase 4bn-AY valid-fail consequence does not apply, and the aggTrades magnitude lane was not narrowed by Phase 4bn-AZ.`

No scientific neighboring variant is authorized by the invalid run.

## 27. One-run / no-rerun posture

`The one authorized evidence-bearing run is consumed, and no rerun is authorized.`

No code was changed after the access-start record was written. No patch-and-rerun occurred. No guard
was relaxed. No feature was removed. No second seed was used. No alternate model was fitted. No
adverse date or block was removed. No second scientific implementation was run to confirm the
answer. Only artefact hashes were recomputed, plus one permitted lightweight arithmetic validation
of the already-frozen target layer using identical formulas and no new market data.

An initial shell redirection attempt failed **before** the Python process started (the redirect
target directory did not yet exist). It opened no data, wrote no artefact, and did not consume the
authorized run. The one actual Python evidence-bearing run is the only scientific run.

## 28. Local artefact root and hashes

Local root: `data/research/cf1_realized_volatility_substrate_test_v001/` — **gitignored and
uncommitted**, confirmed by `git check-ignore -v` → `.gitignore:88:data/research/`. `git ls-files`
reports **zero** tracked files under the AZ output root and zero under `data/research/`.

Six artefacts, each with a valid paired `.sha256` sidecar; all re-verified during merge review:

| # | Relative path | Bytes | SHA256 |
|---|---|---|---|
| 1 | `proofs/cf1_timestamp_boundary_proof_v001__v001__1784558563200__05fa63a8bf8c.json` | 8,556 | `ecdf0fcbad2e192968c0bb9960c8c9117813fd217e94c4a938f201e8aff77248` |
| 2 | `runs/cf1_execution_access_start_v001__v001__1784558563266__05fa63a8bf8c.json` | 11,715 | `66c807976dc43e1d74e697336b91a15a39f54814485197103c4a9878d43c2ed2` |
| 3 | `targets/cf1_realized_variance_target_layer_v001__v001__1784558563266__05fa63a8bf8c.parquet` | 478,424 | `9a7f1a922a02391ac997244e196e12446f56db6deb696ba66d5b8dffcc245010` |
| 4 | `proofs/cf1_leakage_split_coverage_proof_v001__v001__1784559571783__05fa63a8bf8c.json` | 54,262 | `c398d9ac6e1a4dabb86861d4f6d2a9c2c83f651a0d6cd56f090452646b0fba1e` |
| 5 | `manifests/cf1_model_run_manifest_v001__v001__1784558563266__05fa63a8bf8c.json` | 13,905 | `794480596f9623117f576d205f6fc5926769bf33e61f4494ffc023ad7027ebd9` |
| 6 | `manifests/cf1_execution_artifact_inventory_v001__v001__1784559572363__05fa63a8bf8c.json` | 8,251 | `fefc5b51e45b203283ff24f32f793fee6a23580adc142fa52514c626872bc1df` |

`ALL_SIDECARS_VALID = true`. The artefact root was not written, refreshed, repaired, normalized, or
deleted during merge review.

## 29. No predictions artefact — explanation

The `cf1_paired_model_predictions_v001` family was **deliberately not written**. No block produced a
fitted augmented model, so there are zero paired forecasts and zero per-origin losses. Writing an
empty or partial predictions artefact would have implied a scoring stage that never occurred. Its
absence is expected behaviour of the fail-closed path, not a missing artefact.

## 30. Quality-gate results with baseline nuance

| Gate | Result |
|---|---|
| Targeted AZ tests (4 modules) | **56 passed** |
| `pytest tests/research/microstructure` | all passed |
| Full `pytest` | **3342 passed, 2 failed, 1 skipped** (83.8 s) |
| `ruff check` (8 AZ files) | All checks passed |
| `ruff format --check` (8 AZ files) | 8 files already formatted |
| `mypy --strict` | 12 errors, **none in AZ code** |
| `git diff --check main..AZ` | clean |

**Baseline nuance — this merge-closeout does not claim the repository is globally clean.** The
repository retains **2 pre-existing pytest failures** and **12 pre-existing mypy errors**:

- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and
  `::test_real_2026_03_ethusdt`, both failing with `KeyError: 'trade_count'` in
  `src/prometheus/research/data/storage.py:232` — a klines/backtest path AZ never touches.
- 12 `mypy --strict` errors in `labels_manifest_v002.py`, `multiday_feature_gate_checks.py`,
  `ml_baseline_models_v002.py`, `ml_baseline_dataset_v002.py`, and `feature_drift_v002.py` — five
  files AZ never touches.

Phase 4bn-AZ modified **zero** existing tracked files (its entire diff is added files), so the
tracked tree at gate time was byte-identical to base `main`; both failure sets are therefore the
verified base-`main` baseline and are unchanged from prior phases, not introduced by this phase or
this merge. **Phase 4bn-AZ passed relative to the verified base-main baseline and introduced zero
new failures and zero new type errors**, while adding 56 passing tests. Repo-wide
`ruff format --check .` reports 235 pre-existing non-conforming files; none is an AZ file.

No test, lint, type check, AZ run, synthetic proof, target generation, model fit, QLIKE, bootstrap,
diagnostic, backtest, or data workflow was rerun during this merge.

## 31. No-November / no-holdout / no-terminal / no-sealed proof

| Range | Classification | Opened |
|---|---|---|
| 2024-10-01 | committed `1D_BOUNDARY_EMBARGO` | **false** |
| 2024-11-01 .. 2024-11-15 | `UNUSED_NON_RESERVE_BUFFER` | **false** |
| 2024-11-16 | committed embargo exclusion | **false** |
| 2024-11-17 .. 2024-11-30 | `PRE_V002_INTERNAL_HOLDOUT = CONSUMED` | **false** |
| 2024-12-01 .. 2025-02-28 | `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED` | **false** |
| 2025-02-14 .. 2025-02-28 | `V002_SEALED_TEST = UNTOUCHED_RESERVED` | **false** |

The frozen target layer's maximum origin is `2024-10-31T22:00:00Z` and maximum target endpoint is
`2024-10-31T23:00:00Z`; **no 2024-11 timestamp appears anywhere** in the target layer, and no
prediction rows exist. `test_rows_loaded = 0`; `v002_terminal_window_read = false`;
`sealed_test_split_touched = false`.

`The v002 terminal window and v002 sealed test remain untouched and excluded.`

`The consumed pre-v002 internal holdout and the 2024-11-01 through 2024-11-15 buffer were not opened.`

`No evidence reserve was spent by Phase 4bn-AZ or by its merge.`

## 32. No network / no acquisition

No network, web search, API, Binance endpoint, WebSocket, credential, `.env`, `.mcp.json`, MCP,
Graphify, or external reviewer was used by Phase 4bn-AZ or by this merge. No data was acquired or
downloaded. `network_used = false`; `data_acquisition_used = false`. This is statically asserted by
`test_cf1_no_network_v001.py` over all four AZ code files.

## 33. No PnL / backtest / trading

`No PnL analysis, backtest, signal generation, strategy, paper, shadow, live, or exchange-write execution was performed or is authorized.`

CF-1 is a non-directional realized-variance magnitude test; it produced no directional object and no
tradable object. No plot, notebook, or exploratory output exists. All eight non-authorization flags
(`ml_authorized`, `diagnostics_authorized`, `strategy_authorized`, `signals_authorized`,
`pnl_authorized`, `backtest_authorized`, `live_authorized`, `exchange_write_authorized`) are
`false`.

## 34. Manifest state preservation

No manifest was read for mutation, written, or transitioned. `research_eligible = false`;
`eligibility_gate_status = pending`; `chronological_split_policy` unchanged; governance labels
unchanged. **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant
preserved (never invoked).**

## 35. Upstream immutability evidence

No prior local artefact was mutated. The Phase 4bn-AZ artefact root was created by exactly one
controlled run and re-verified byte-identical during merge review (all six sidecars valid). No
Phase 4bn-AQ / AR / AN / AJ / AH namespace was read, written, or mutated by AZ or by this merge. No
`data/microstructure/` file was modified; the 244 opened source Parquets were read strictly
read-only and verified against their committed sidecars.

## 36. Boundary confirmations

- no Phase 4bn-AY file modified;
- no pre-existing source, test, script, or config modified;
- no `data/microstructure/` file modified or committed;
- no `data/research/` artefact staged or committed;
- no manifest mutated; no `research_eligible` flip; no `eligibility_gate_status` transition; no
  `chronological_split_policy` change;
- no forbidden partition opened (2024-10-01, November buffer, 2024-11-16, consumed holdout,
  terminal, sealed);
- no reserve spend;
- no acquisition; no network; no endpoint; no credential; no MCP / Graphify / `.mcp.json`;
- no ML model trained beyond the frozen preregistered baseline fit; no strategy; no signal; no PnL;
  no backtest; no paper / shadow / live / deployment / exchange-write;
- no rerun of AZ, the synthetic proof, target generation, model fitting, QLIKE, or the bootstrap;
- no retained verdict revised; no project lock loosened; no M0 amendment;
- `.claude/scheduled_tasks.lock` never staged, modified, deleted, cleaned, or committed;
- no successor authorized.

## 37. Retained verdict ledger

All preserved verbatim: **H0** — FRAMEWORK ANCHOR; **R3** — BASELINE-OF-RECORD; **R1a** — RETAINED —
NON-LEADING; **R1b-narrow** — RETAINED — NON-LEADING; **R2** — FAILED — §11.6; **F1** — HARD REJECT;
**D1-A** — MECHANISM PASS / FRAMEWORK FAIL; **5m thread** — OPERATIONALLY CLOSED; **V2** — HARD
REJECT — terminal for V2 first-spec; **G1** — HARD REJECT — terminal for G1 first-spec; **C1** —
HARD REJECT — terminal for C1 first-spec.

Phase 4bn-AR's `INVESTIGATE_AMBIGUOUS` and every other prior phase result are preserved verbatim and
unreinterpreted. Phase 4bn-AZ adds exactly one new record: `CF1_INVALID_RUN`, which is not a
scientific verdict and does not enter the retained verdict ledger as a pass or fail.

## 38. Preserved project locks

Unchanged and preserved exactly:

- `STOP_LONGHORIZON_ML_ARC` and `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` — **distinct**; not
  merged, softened, reinterpreted, rescued, reopened, or continued;
- `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
- `PRE_V002_INTERNAL_HOLDOUT = CONSUMED`;
- `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
- `V002_SEALED_TEST = UNTOUCHED_RESERVED`;
- `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`;
- `test_rows_loaded = 0`; `research_eligible = false`; `eligibility_gate_status = pending`; all
  published authorization flags false;
- Phase 4aw `flip_research_eligible(...)` always-raising, never invoked;
- Phase 4bn-AE §19 absolute M0 boundary; the Phase 4ak twelve-clause M0 gate with §6 cooldown and §7
  cooled-down families; M0 cooldown and cooled-down-family rules;
- §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops;
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p;
  Phase 4q; Phase 4v; Phase 4w; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy;
- all dataset identities and hashes; all split, holdout, sidecar, storage, and evidence-ledger
  policies (Phase 4bn-Y / L / AA / 4bb-F / AV);
- the human operator as sole final authority.

All prior phase results preserved verbatim. `docs/00-meta/current-project-state.md` and the README
are left unchanged by this merge, matching the recent docs-only and code-and-evidence precedent.

## 39. No-rescue constraints

The Phase 4bn-AZ merge does not, and cannot, be construed as authorising:

- converting `CF1_INVALID_RUN` into a pass or a fail;
- endorsing the frozen Phase 4bn-AY design;
- rerunning Phase 4bn-AZ, in whole or in part;
- correcting, relaxing, or reinterpreting the frozen feature contract, the log transform, or the
  `1e10` condition-number guard;
- selecting or pre-approving any replacement feature or remedy;
- creating a new preregistration or starting a successor phase;
- generating QLIKE, bootstrap, or any other CF-1 metric;
- opening any market data, the November buffer, the consumed holdout, the v002 terminal window, or
  the v002 sealed test;
- spending any evidence reserve;
- ML model training beyond the frozen preregistered baseline, model selection, strategy hypothesis
  generation, or converting any output into signals;
- strategy signal construction, position state, entry / exit rules, or backtest design;
- PnL analysis, paper / shadow, live-readiness, deployment, or exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; barrier / target-before-stop / MFE /
  MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m research-thread reopening;
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`, or
  `chronological_split_policy` from this evidence alone.

## 40. Explicit statement that no remedy is chosen or authorized

**No remedy is chosen, selected, designed, or authorized by this merge-closeout.** The Phase 4bn-AZ
execution report identified the algebraic redundancy and mentioned, purely illustratively, that a
future contract correction might drop the redundant third feature or replace it with a genuinely
independent sign-invariant column. That mention is **not** an authorization, **not** a
recommendation, and **not** a pre-approval. Dropping `rolling_quantity_mean_60s` is explicitly
**not** authorized. Any remedy must be chosen inside a separately authorized docs-only
contract-correction phase, not here.

`If CF-1 is pursued further, the next admissible step is a separately authorized docs-only correction of the merged Phase 4bn-AY contract, with a new anti-duplication audit and no pre-approved remedy.`

Because the defect lives in the merged Phase 4bn-AY scientific contract, correcting it is a
preregistration change and must not be performed inside an execution phase or inside this merge.

## 41. Exact post-merge result state

```
CF1_INVALID_RUN_RECORDED_ON_MAIN__NO_SCIENTIFIC_CLAIM__NO_RERUN_AUTHORIZED__SEPARATE_DOCS_ONLY_CONTRACT_CORRECTION_REQUIRED_IF_CONTINUING__RESERVES_UNTOUCHED
```

## 42. Required post-merge operator posture and recommended next action

The project remains **paused with respect to execution**. The CF-1 development experiment has been
executed once under the frozen contract; the run is invalid, produced no scientific test, and
consumed the single authorized evidence-bearing run. No data may be opened, no target or feature
generated, no model fitted, no QLIKE or bootstrap computed, no diagnostic or backtest run, no
acquisition made, and no evidence reserve spent.

`Remaining paused is a valid operator choice.`

**Recommended next operator action:** return this merge-closeout and the final operator report to
ChatGPT for review; then decide separately whether to remain paused or to authorize a docs-only
Phase 4bn-AY contract-correction phase. **Recommended state: remain paused.**

**Conditional next, NOT authorized:** a docs-only correction of the merged Phase 4bn-AY feature
contract would re-preregister an estimable feature set, carry a new mechanism justification and an
explicit anti-duplication audit, and be frozen before any new execution is proposed. It is **not**
authorised by this merge, chooses no remedy, and requires its own operator authorization and a new
Claude Code prompt.

## 43. Successor authorization

**None.**

No successor phase is authorized by this merge. Explicitly **not** authorized:

- any Phase 4bn-AZ rerun or partial re-execution;
- a Phase 4bn-AY contract-correction phase (docs-only or otherwise);
- a corrected CF-1 preregistration or a CF-1 re-execution phase;
- any neighbouring CF-1 feature / horizon / loss / baseline / model / threshold / split variant;
- a market-state or volatility-regime filter assessment or implementation;
- reopening `STOP_LONGHORIZON_ML_ARC` or `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`;
- terminal-window, sealed-test, or consumed-holdout access;
- Phase 4 canonical; Phase 5;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book data acquisition;
- ML implementation; strategy implementation; backtest implementation; signal generation;
- paper / shadow; live-readiness; deployment; exchange-write; production keys; authenticated APIs;
  private endpoints; user stream; MCP / Graphify / `.mcp.json` / credentials;
- any manifest transition from this evidence alone.

`Phase 4bn-BA or any other successor requires separate operator authorization and a new Claude Code
prompt.`
