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
- [ ] **Committed non-reserve eligibility envelope (context only):** 2024-03-01..2024-09-30 ∪
      2024-10-02..2024-11-15 (259 dates); embargo dates 2024-10-01 and 2024-11-16 excluded (§21).
      Eligibility is **not** access.
- [ ] **Exact primary execution-access boundary:** the execution phase may open and use **only**
      `2024-03-01 through 2024-10-31 UTC, excluding 2024-10-01` (244 dates) (§21). March = warmup /
      initial training history; April–October = the seven evaluation blocks; 2024-10-01 = the fixed
      one-day embargo before the October block, which begins 2024-10-02.
- [ ] **November buffer not opened (FAIL PREFLIGHT if violated):** `2024-11-01 .. 2024-11-15 =
      UNUSED_NON_RESERVE_BUFFER`. **Preflight FAILS if the execution prompt, the implementation, any
      config, or any query proposes to open, load, read, train on, evaluate on, bootstrap over,
      preprocess with, threshold on, plot, or interpret any 2024-11-01..2024-11-15 row.** That
      committed split metadata classifies these dates as non-reserve development-eligible does **not**
      authorize their use in the frozen CF-1 primary experiment.
- [ ] **2024-11-16 exclusion:** remains excluded under committed split/embargo metadata; outside the
      primary experiment.
- [ ] **Terminal exclusion:** v002 terminal 2024-12-01..2025-02-28 excluded;
      `v002_terminal_window_read = false`.
- [ ] **Sealed exclusion:** v002 sealed test 2025-02-14..2025-02-28 excluded;
      `sealed_test_split_touched = false`; `test_rows_loaded = 0`.
- [ ] **Consumed-holdout exclusion from confirmation:** 2024-11-17..2024-11-30 not used as a CF-1
      evaluation or confirmation set; not relabeled into a fresh holdout; descriptive-only (§36).

### 1.3 Frozen target / horizon / cadence
- [ ] **Target formula** matches §3 exactly (1-minute UTC grid, `τ_k = a + k·60,000 ms` for
      `k = 0…60`, `G_k = P_at(τ_k)`, `r_k = ln(G_k/G_{k-1})`, `RV(a,b] = Σ_{k=1}^{60} r_k²`,
      `y = ln(RV+ε)`, `ε = 1e-16`, no annualization); `exp(ŷ)` forecasts the positive quantity
      `RV + ε`, consistent with the log target.

**Causal completed-interval gates (all must PASS; any violation ⇒ `CF1_INVALID_RUN`, §31):**

- [ ] **(1) Every RV target/HAR interval uses `(a, b]`** — a causal completed interval. Confirm **no
      live `[a, b)` RV interval** anywhere (§3, §6).
- [ ] **(2) `P_at(u)` uses `≤ u` at every grid boundary** — the single canonical operator; ties by
      greatest canonical `row_index` (`row_index_le_R`). Confirm `P_start`, `P_minus`, strict `<` at
      an RV boundary, mixed `≤`/`<` inside one interval, and left-limit terminal prices are **absent**.
- [ ] **(3) Future target is `(t, t + H]`** — `G_0 = P_at(t)`, `G_k = P_at(t + k·60,000)` for
      `k = 1…60`; a trade timestamped exactly `t + H` **is** included in the target for origin `t`.
- [ ] **(4) Feature snapshot is `≤ t`** — last committed feature row with `feature_timestamp_ms ≤ t`,
      committed tie rule; a row timestamped exactly `t` may be used (§11).
- [ ] **(5) Origin-time trade information is present in `G_0` and not counted as a future return** —
      the first target return is `ln(P_at(t + 1min) / P_at(t))`; the already-known pre-`t`→`t` jump
      does **not** appear in the target.
- [ ] **(6) HAR intervals ending at `t` may use trades timestamped exactly `t`** — `RV_h(t) =
      RV(t − 1h, t]` with terminal `P_at(t)`; causal, no future look-ahead (§17).
- [ ] **(7) Boundary trades are assigned exactly once, to the interval ENDING at their timestamp** —
      never to both adjacent RV intervals, never to neither; **no boundary jump omitted**. Tie rules
      **identical** between target and HAR construction.
- [ ] **(8) Covered minutes use `(τ_{k-1}, τ_k]`** — covered iff ≥ 1 actual aggTrade satisfies
      `τ_{k-1} < source_transact_time_ms ≤ τ_k` (§7).
- [ ] **(9) The final October `2024-10-31T23:00` origin is INVALID** — its target endpoint
      `2024-11-01T00:00:00.000Z` lies outside execution access. B7's last potentially valid origin is
      `2024-10-31T22:00:00.000Z` (target ends `2024-10-31T23:00:00.000Z`). The dropped hour is removed
      identically from both models (§8, §21).
- [ ] **(10) No November row is opened** — including a row timestamped exactly at midnight, and
      including any attempt to load an excluded endpoint merely to form `P_at(endpoint)` (§21).
- [ ] **Deterministic timestamp-boundary proof emitted and PASSING before ANY market data is opened**
      (§33), over **synthetic timestamp cases only** (reads no market data, no reserve). With price
      `100` at `09:59:59.999` and `110` at exactly `10:00:00.000`, verify: `(09:00,10:00]` **captures**
      the boundary jump; `(10:00,11:00]` **starts from `110`** and does **not** re-count it; the
      feature snapshot at `10:00` **may** include the `10:00` trade; `RV_h(10:00)` **may** include the
      `10:00` trade; `RV_target(10:00)` does **not** count the pre-`10:00`→`10:00` jump; a trade
      exactly at `11:00` **is included** in target `(10:00,11:00]`; the final October `23:00` origin is
      **rejected without opening November data**. A failed or absent proof ⇒ `CF1_INVALID_RUN`.
- [ ] **Zero-RV safeguard wired in:** the loss uses `v = RV + ε` and `h_m = max(exp(ŷ_m), ε)` with the
      **same** `ε = 1e-16` for **both** models (§3, §20, §26); zero-RV origins are **retained**, never
      dropped for being zero; no alternative floor; no post-hoc clipping of ratio or loss.
- [ ] **Horizon = 60 min** (`M = 60`); exactly one; no sensitivity horizon (§4).
- [ ] **Cadence = top-of-UTC-hour, non-overlapping** windows (§5).
- [ ] Interval closure, partial-window/block-assignment, and day-boundary rules per §6–§10 — an
      origin is assigned to a block by its own UTC date/time but is valid only if its **entire**
      completed target `(t, t+H]`, **right endpoint included**, lies inside execution access and
      crosses no embargo / buffer / holdout / terminal / sealed boundary. An ordinary UTC-day or month
      crossing (e.g. `2024-04-30T23:00Z → 2024-05-01T00:00Z`, assigned to B1) is permitted.
- [ ] **Covered-minute predicate:** `(τ_{k-1}, τ_k]` is covered iff ≥ 1 actual aggTrade satisfies
      `τ_{k-1} < source_transact_time_ms ≤ τ_k` — a trade exactly at the sub-interval **start**
      belongs to the **preceding** completed minute; a trade exactly at `τ_k` belongs to the
      **current** completed minute; every boundary trade counted in exactly one minute (§7). Coverage
      threshold unchanged at **≥ 30 of 60**; causal carry-forward; no future look-ahead; no stitching
      across embargo / buffer / holdout / terminal / sealed boundaries; no zero-RV drop.

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
- [ ] Estimation = plain **OLS**, no regularization, no tunable hyperparameter (§19); forecast
      positivity by construction plus the `ε` loss-floor safeguard (§20).

### 1.6 Frozen split / leakage controls
- [ ] **Split boundaries:** 7 monthly evaluation blocks Apr–Oct 2024 (B7 = 2024-10-02..2024-10-31);
      March warmup; `2024-11-01..2024-11-15 = UNUSED_NON_RESERVE_BUFFER` (never opened); 2024-11-16 =
      committed embargo exclusion. No evaluation block, training set, or bootstrap uses any date on or
      after 2024-11-01 (§22).
- [ ] **Expanding-window training** rule; `≥ 70` training origins per fit (§23).
- [ ] **Purge** = horizon (1h); **embargo** = 1 calendar day at each train/eval boundary (§24).
- [ ] **Preprocessing scope:** all fitted on training origins only; no global stats; no eval block
      influences its own preprocessing (§25).

### 1.7 Frozen loss / uncertainty / decision
- [ ] **Primary loss** = QLIKE per §26 (with the `v`/`h` `ε`-safeguard); secondary metrics limited to
      MSE-on-variance and MZ-R² (descriptive only, never decision-bearing).
- [ ] **Observed primary estimand computed exactly as §27:** `d_{i,t} = QLIKE_base(i,t) −
      QLIKE_aug(i,t)`; `D_i = (1/n_i) Σ_t d_{i,t}`; `Δ_equal = (1/7) Σ_{i=1}^{7} D_i`. **P1 iff
      `Δ_equal > 0`.** Verify **no** origin-count weighting and **no** cross-block pooling anywhere in
      the decision path.
- [ ] **Bootstrap estimates the SAME `Δ_equal` estimand (§29):** stratified by evaluation block;
      chronological order preserved within each block; block-specific `ℓ_i = ceil(n_i^(1/3))`;
      within-block moving-block resampling to exactly `n_i` (final block truncated); `D_i^(b) =
      mean(d_{i,*}^{(b)})`; `Δ_equal^(b) = (1/7) Σ_i D_i^(b)`; exactly `B = 10,000` replicates; seed
      `20260715`; `LB_95 = quantile({Δ_equal^(b)}, 0.05)`. **P3 iff `LB_95 > 0`.**
- [ ] **Bootstrap prohibitions honored:** no pooling of all per-origin observations into one sequence;
      no weighting of months by valid-origin count; no resampling across evaluation-block boundaries;
      no alternate bootstrap / analytical SE / IID test / DM variant / residual diagnostic substituted
      after execution.
- [ ] **P2 and P3 independent:** at least 6 of 7 observed `D_i` strictly positive (§30); the bootstrap
      may not replace the 6-of-7 rule and the 6-of-7 rule may not replace the bootstrap.
- [ ] **Pass / fail / invalid pseudocode** implemented exactly per §31; zero-floor materiality (§28).
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

0. [ ] Emit and validate the **deterministic timestamp-boundary proof** (§33; synthetic timestamp
       cases only, no market data, no reserve). It must PASS **before any market data is opened**.
1. [ ] Build the RV target + HAR lookbacks + microstructure snapshots **within the primary
       execution-access boundary only** (2024-03-01..2024-10-31 excl. 2024-10-01), using `(a, b]`
       intervals and `P_at(u)` (`≤ u`) at **every** grid boundary, dropping any origin whose target
       endpoint falls outside execution access (incl. the `2024-10-31T23:00` origin); emit the
       **leakage / split / coverage proof** and validate it **before** any metric computation
       (boundaries, embargo/purge, `≥30/60` coverage, per-block valid-origin counts `n_i`,
       no-November-buffer-row proof, reserve-untouched flags).
2. [ ] Fit baseline and augmented per block (expanding window); record numerical-guard results
       (condition number, rank, training-origin counts).
3. [ ] Compute per-origin `QLIKE_m(t)` under the `ε`-safeguard (verifying every actual, forecast,
       ratio, logarithm, and loss is finite, and that zero-RV origins are retained), then `d_{i,t}`,
       `D_i`, `Δ_equal`, `ρ`, the two secondary metrics, and the stratified moving-block bootstrap
       `LB_95`.
4. [ ] Freeze the primary result, then (only then) route to the verdict in §3–§4.

## 3. Outcome classification (four mutually distinct results)

The execution phase must record **exactly one**:

| Outcome | Meaning | Consequence |
|---|---|---|
| **PREFLIGHT_FAILURE** | any §1 gate failed **before** data read | stop; fix and re-authorize; **no** data opened; **not** a scientific result |
| **CF1_INVALID_RUN** (technical invalidation) | a §1.x/§2 control broke **during** execution — leakage, reserve access, any 2024-11-01..2024-11-15 buffer row opened or used, **any completed-interval violation (a live `[a,b)` RV interval; `P_minus` or strict `<` at an RV boundary; mixed operators; the origin-time jump inside the future target; a boundary jump omitted; a boundary trade double-assigned or unassigned; HAR built as `[t−L,t)`; a November row opened to score the `2024-10-31T23:00` origin; an origin retained whose target endpoint lies outside execution access; a failed/absent timestamp-boundary proof)**, preprocessing leak, timestamp misalignment, missing/undersized block, numerical failure, or any unauthorized switch (contract §31) | make **no** scientific claim; preserve all locks; stop; separate corrective phase + new operator authorization |
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

- A numerical failure (singular matrix, zero-variance regressor, condition number `> 1e10`, a
  non-finite actual / forecast / ratio / logarithm / QLIKE / coefficient value, `< 70` training
  origins, a block with `< 100` valid origins) is a **CF1_INVALID_RUN**, not a fail and not a pass.
  Note `RV(t) = 0` is **not** a numerical failure and **not** a drop reason — the `ε` floor keeps its
  QLIKE well-defined (contract §26).
- Ambiguity, a missing contract element, invalid temporal ordering, or a contaminated split **cannot**
  be converted into a scientific pass; when in doubt, fail closed to `CF1_INVALID_RUN`.

## 5. Non-authorization

This checklist authorizes nothing. It does not permit reading any data, building any target/feature,
fitting any model, running any diagnostic/backtest, spending any reserve, or beginning any successor
phase. The CF-1 execution phase begins only under a separate explicit operator authorization and a
new Claude Code prompt. No market data, feature row, label row, model output, or evidence reserve was
opened or read by Phase 4bn-AY to write this checklist.
