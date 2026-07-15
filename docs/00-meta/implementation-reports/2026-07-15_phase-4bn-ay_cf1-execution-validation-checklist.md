# Phase 4bn-AY — CF-1 Execution-Validation Checklist (for a later, separately-authorized phase)

This checklist gates a **future** CF-1 execution phase (proposed title
`Phase 4bn-AZ`, not authorized here). **No execution is performed in Phase 4bn-AY.** The checklist
is the fail-closed preflight and verdict-routing contract for whoever later runs CF-1 under the
Phase 4bn-AY frozen contract
(`2026-07-15_phase-4bn-ay_cf1-target-feature-baseline-and-evaluation-contract.md`). Every gate below
must pass **before** any market data is opened or any metric is interpreted. Any gate failure routes
per §3–§4; a preflight or technical-invalidation failure is **not** a scientific result.

All references to "the contract" are to the Phase 4bn-AY implementation-grade contract; section
numbers (§) are its sections.

---

## 1. Preflight gates (all must PASS before any data read)

Each gate is `PASS` / `FAIL`; any `FAIL` ⇒ **preflight failure** (§3), stop, no data opened.

### 1.1 Authorization & repository state
- [ ] A separate explicit **operator authorization** and a new Claude Code prompt exist for the CF-1
      execution phase (this checklist and the preregistration are not authorization).
- [ ] **Exact base / preregistration SHA:** the execution phase is branched from and pins the Phase
      4bn-AY preregistration commit SHA; `HEAD == main == origin/main` at that SHA (or a later main
      that still contains the four Phase 4bn-AY files unmodified); only `.claude/scheduled_tasks.lock`
      untracked.
- [ ] **No preregistration-file modification:** all four Phase 4bn-AY files
      (preregistration memo, contract, this checklist, closeout) are byte-for-byte unmodified in the
      execution branch (`git diff <prereg-sha> -- <the four files>` is empty).

### 1.2 Data identity & boundaries (stated from committed metadata; verified without reserve reads)
- [ ] **Exact data identity:** substrate = BTCUSDT USDⓈ-M pre-v002 aggTrades; families per contract
      §1; on-disk under `data/microstructure/…` (gitignored). No other source.
- [ ] **Exact development date boundary:** development window = 2024-03-01..2024-09-30 ∪
      2024-10-02..2024-11-15 (259 dates); embargo dates 2024-10-01 and 2024-11-16 excluded (§21).
- [ ] **Terminal exclusion:** v002 terminal 2024-12-01..2025-02-28 excluded;
      `v002_terminal_window_read = false`.
- [ ] **Sealed exclusion:** v002 sealed test 2025-02-14..2025-02-28 excluded;
      `sealed_test_split_touched = false`; `test_rows_loaded = 0`.
- [ ] **Consumed-holdout exclusion from confirmation:** 2024-11-17..2024-11-30 not used as a CF-1
      evaluation or confirmation set; not relabeled into a fresh holdout; descriptive-only (§36).

### 1.3 Frozen target / horizon / cadence
- [ ] **Target formula** matches §3 exactly (1-minute UTC grid, causal LOCF prices, `RV = Σ r_k²`,
      `y = ln(RV+ε)`, `ε = 1e-16`, no annualization).
- [ ] **Horizon = 60 min** (`M = 60`); exactly one; no sensitivity horizon (§4).
- [ ] **Cadence = top-of-UTC-hour, non-overlapping** windows (§5).
- [ ] Interval closure, missing-grid coverage (`≥30/60`), partial-window, and day-boundary rules per
      §6–§10.

### 1.4 Frozen features
- [ ] **Feature names** exactly `{rolling_aggtrade_count_60s, rolling_quantity_sum_60s,
      rolling_quantity_mean_60s}`; max feature count 3; single 60s window; causal snapshot at origin
      (§11–§12).
- [ ] **Feature transformations** = natural log then train-only z-score (`ε_std = 1e-8`); no
      clipping/winsorization; HAR regressors unstandardized (§13–§14).
- [ ] **Directional exclusions** honored: no flow-ratio, imbalance, buy/sell quantities/counts,
      signed returns, funding, calendar, OI, book, forced-flow/liquidation (§16).
- [ ] **No dispersion feature invented** (none exists in the committed schema).

### 1.5 Frozen baseline & augmented models
- [ ] **Baseline implementation** = HAR-style OLS in log space on `RV_h, RV_d, RV_w` + intercept;
      forecast `exp(ŷ)`; exactly one baseline (§17).
- [ ] **Augmented implementation** = nested OLS adding only the 3 standardized log microstructure
      features; identical target/window/estimator/origins/preprocessing (§18).
- [ ] Estimation = plain **OLS**, no regularization, no tunable hyperparameter (§19); positivity by
      construction (§20).

### 1.6 Frozen split / leakage controls
- [ ] **Split boundaries:** 7 monthly evaluation blocks Apr–Oct 2024 (B7 = 2024-10-02..2024-10-31);
      March warmup; Nov 1–16 buffer (§22).
- [ ] **Expanding-window training** rule; `≥ 70` training origins per fit (§23).
- [ ] **Purge** = horizon (1h); **embargo** = 1 calendar day at each train/eval boundary (§24).
- [ ] **Preprocessing scope:** all fitted on training origins only; no global stats; no eval block
      influences its own preprocessing (§25).

### 1.7 Frozen loss / uncertainty / decision
- [ ] **Primary loss** = QLIKE per §26; block-mean then equal-weighted across 7 blocks; secondary
      metrics limited to MSE-on-variance and MZ-R² (descriptive only).
- [ ] **Uncertainty method** = moving-block bootstrap per §29 (`ℓ=⌈n^(1/3)⌉`, `B=10,000`, one-sided
      95%, null `E[d]=0`, lower-bound>0 rule).
- [ ] **Pass / fail / invalid pseudocode** implemented exactly per §31; block-consistency `≥6/7`
      (§30); zero-floor materiality (§28).
- [ ] **Random seeds:** OLS deterministic; bootstrap `RNG_SEED = 20260715` fixed (§32).

### 1.8 Frozen outputs / provenance / environment
- [ ] **Output paths** local/gitignored under `data/research/…`; no data file committed (§33).
- [ ] **Sidecar fields** per Phase 4bb-F: `.sha256` sidecars + inventory; `created_at_unix_ms`,
      `created_at_utc`, `code_commit_sha`, `base_main_commit_sha`; non-authorization flags all
      `false` (§34).
- [ ] **No network** / web / API / Binance endpoint / credential / WebSocket / MCP / Graphify /
      `.mcp.json` used.
- [ ] **No acquisition** of any new data; substrate is the already-on-disk pre-v002 aggTrades only.
- [ ] **No reserve read:** terminal, sealed, and consumed-holdout not opened for scoring/confirmation.

### 1.9 Frozen anti-switching preflight
- [ ] **No metric switching**, **no model switching**, **no feature switching**, **no manual date
      exclusion**, **no horizon/cadence/window/threshold change**, **no loss change** vs the contract.
- [ ] **No exploratory plots before the primary result is frozen**; **no PnL or directional
      analysis** at any point; **no interpretation before artefact hashes and the leakage/split proof
      validate**.

## 2. Execution-order gates (fail-closed, in order)

1. [ ] Build the RV target + HAR lookbacks + microstructure snapshots on development data only;
       emit the **leakage / split / coverage proof** and validate it **before** any metric
       computation (boundaries, embargo/purge, `≥30/60` coverage, per-block valid-origin counts,
       reserve-untouched flags).
2. [ ] Fit baseline and augmented per block (expanding window); record numerical-guard results
       (condition number, rank, training-origin counts).
3. [ ] Compute per-origin QLIKE, per-block means, `ΔQLIKE_block,i`, `ΔQLIKE_blockmean`, `ρ`, the two
       secondary metrics, and the moving-block bootstrap CI.
4. [ ] Freeze the primary result, then (only then) route to the verdict in §3–§4.

## 3. Outcome classification (four mutually distinct results)

The execution phase must record **exactly one**:

| Outcome | Meaning | Consequence |
|---|---|---|
| **PREFLIGHT_FAILURE** | any §1 gate failed **before** data read | stop; fix and re-authorize; **no** data opened; **not** a scientific result |
| **CF1_INVALID_RUN** (technical invalidation) | a §1.x/§2 control broke **during** execution — leakage, reserve access, preprocessing leak, timestamp misalignment, missing/undersized block, numerical failure, or any unauthorized switch (contract §31) | make **no** scientific claim; preserve all locks; stop; separate corrective phase + new operator authorization |
| **CF1_VALID_FAIL** | valid run; not all of P1/P2/P3 met (contract §31) | fail consequence (prereg §32): materially narrow the magnitude lane; no neighboring variants; return to paused |
| **CF1_VALID_PASS** | valid run; P1 ∧ P2 ∧ P3 ∧ P4 all met | pass consequence (prereg §31): substrate informative on magnitude axis; authorize **only** a separate docs-only market-state-filter assessment; no direction/PnL/reserve |

- **PREFLIGHT_FAILURE** and **CF1_INVALID_RUN** are **not** scientific results and never become a
  pass or a fail.
- **CF1_VALID_FAIL** and **CF1_VALID_PASS** are the only scientific outcomes; both are legitimate and
  neither authorizes trading, direction, reserve spend, or reopening a stopped arc.

## 4. Distinguishing the four (decision routing)

```text
if any §1 preflight gate FAILED before opening data:            → PREFLIGHT_FAILURE (stop; no data read)
elif any control broke during the run (contract §31 invalid):  → CF1_INVALID_RUN   (corrective phase)
elif P1 and P2 and P3 and run-valid:                           → CF1_VALID_PASS
else (valid run, pass rule not fully met):                     → CF1_VALID_FAIL
```

- A numerical failure (singular matrix, zero-variance regressor, condition number `> 1e10`,
  non-finite loss, `< 70` training origins, a block with `< 100` valid origins) is a
  **CF1_INVALID_RUN**, not a fail and not a pass.
- Ambiguity, a missing contract element, invalid temporal ordering, or a contaminated split **cannot**
  be converted into a scientific pass; when in doubt, fail closed to `CF1_INVALID_RUN`.

## 5. Non-authorization

This checklist authorizes nothing. It does not permit reading any data, building any target/feature,
fitting any model, running any diagnostic/backtest, spending any reserve, or beginning any successor
phase. The CF-1 execution phase begins only under a separate explicit operator authorization and a
new Claude Code prompt. No market data, feature row, label row, model output, or evidence reserve was
opened or read by Phase 4bn-AY to write this checklist.
