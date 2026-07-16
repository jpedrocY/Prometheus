# Phase 4bn-AY — Closeout

## 1. Phase name

Phase 4bn-AY — CF-1 Realized-Volatility Magnitude-Forecasting Substrate-Test Preregistration
(docs-only, low-researcher-freedom).

## 2. Branch

`phase-4bn-ay/cf1-realized-volatility-substrate-test-preregistration`.

## 3. Base SHA

`8b6c8614e37508cd05346f5ed90f8d08d9f68560` (`HEAD == main == origin/main` at branch time; tip after
the Phase 4bn-AX merge-closeout SHA-finalization commit). Verified in sync before branching; the only
untracked item was the transient `.claude/scheduled_tasks.lock`, which was not staged, modified,
deleted, cleaned, or committed.

## 4. Phase type

Docs-only, low-researcher-freedom **preregistration** phase (contract-freeze only). Not data
execution, target/feature generation, model fitting, hyperparameter tuning, diagnostics, backtesting,
PnL analysis, a reserve-spend proposal, terminal/sealed use, a strategy authorization, a
market-state-filter implementation, or a paper/shadow/live/exchange-write phase.

## 5. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` (scientific design of
the selected arc), though it mutates no eligibility, manifest, verdict, reserve, or lock and freezes a
contract only.

## 6. Files added

Exactly four, all additions:

1. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_cf1-realized-volatility-substrate-test-preregistration.md` — main preregistration memo.
2. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_cf1-target-feature-baseline-and-evaluation-contract.md` — implementation-grade frozen contract.
3. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_cf1-execution-validation-checklist.md` — execution-validation checklist for a later phase.
4. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_closeout.md` — this closeout.

The four files were subsequently amended **in place** by **three pre-merge contract corrections**
(§33.A–§33.C), followed by **this closeout-history-only correction** (§33.D), which modifies **only
this closeout file**. The base-to-final branch diff relative to `main` remains **exactly these four
added files** — no fifth file, no modification/deletion/rename of any pre-existing file.

## 7. Confirmation no existing file modified

Confirmed. No existing file was modified, renamed, or deleted. The tracked diff is exactly four added
files. The evidence ledger, `current-project-state.md`, README, M0 gate, process standards, phase
gates, technical-debt register, source, tests, scripts, manifests, sidecars, splits, and all prior
reports are untouched.

## 8. Areas inspected

Committed, read-only: Phase 4bn-AX main decision memo, forced-flow/M0 audit, and closeout; Phase
4bn-AW screening; Phase 4bn-AK/AS/AT stopped-arc lineage; Phase 4bn-AV evidence ledger and
spending-authority standard; Phase 4bn-AE §19 M0 boundary and Phase 4ak twelve-clause M0 gate; Phase
4bn-Y split/holdout policy and the committed `pre_v002_split_policy.py` / `diagnostics_split_policy_
v002.py` constants; Phase 4bn-L storage/budget; Phase 4bb-F sidecar policy; `docs/04-data/timestamp-
policy.md`; Phase 4bn-AP/AM contract precedents; and committed source
(`features_schema.py`, `features_schema_v002.py`, `labels_compute_v002.py`,
`longhorizon_labels_schema_v001.py`) for feature/target/timestamp capability confirmation only. Git
history/metadata for base-state verification. README and `current-project-state.md` treated as
potentially stale and navigational only.

## 9. Exact selected target

Future **realized variance** of BTCUSDT last-trade log price over a 1-hour **causal completed**
target interval `(t, t + H]`: 1-minute UTC-clock grid, single canonical operator
`P_at(u)` = last canonical aggTrade with `source_transact_time_ms ≤ u` (greatest `row_index` tie
rule), `τ_k = t + k·60,000 ms` for `k = 0…60`, `G_k = P_at(τ_k)`, `r_k = ln(G_k / G_{k-1})`,
`RV(t) = RV(t, t + H] = Σ_{k=1}^{60} r_k²`, modelled as `y = ln(RV + ε)` with `ε = 1e-16`, forecast
mapped back to variance by exponentiation. A boundary trade is assigned exactly once, to the interval
**ending** at its timestamp; `G_0 = P_at(t)` is already-known origin information, so no boundary jump
is omitted and no already-observed origin-time jump enters the target. Non-directional; no prior
committed RV definition existed, so authored fresh.

## 10. Exact horizon

**H = 60 minutes (3,600,000 ms). Exactly one.** Top-of-UTC-hour, non-overlapping origins.

## 11. Exact baseline

One HAR-style realized-variance baseline: OLS in log-variance space on `RV_h` (prev 1h), `RV_d` (mean
of prev 24 hourly RVs), `RV_w` (mean of prev 168 hourly RVs) + intercept; forecast `exp(ŷ)`.

## 12. Exact augmented model

Nested OLS adding only the three standardized log microstructure features to the baseline; identical
target, training window, estimator, forecast origins, and preprocessing; isolates incremental
microstructure information, not model class.

## 13. Exact feature count / families

Exactly **3** sign-invariant committed features at the 60s window: `rolling_aggtrade_count_60s`
(trade-arrival intensity), `rolling_quantity_sum_60s` (unsigned volume intensity),
`rolling_quantity_mean_60s` (mean trade size). No dispersion feature (none exists in the committed
schema; none invented).

## 14. Exact development boundary

**Committed non-reserve eligibility envelope:** pre-v002 train ∪ validation = 2024-03-01..2024-09-30
(214) + 2024-10-02..2024-11-15 (45) = 259 admissible UTC dates. **Frozen CF-1 primary
execution-access boundary:** `2024-03-01 through 2024-10-31 UTC, excluding 2024-10-01` = 244 dates —
the only dates the primary experiment may open or use. **`2024-11-01..2024-11-15 =
UNUSED_NON_RESERVE_BUFFER`** — non-reserve-eligible but unopened and unused (not training, not
evaluation, not bootstrap, not confirmation, not preprocessing, not diagnostics). Excluded: embargo
dates 2024-10-01 / 2024-11-16; consumed holdout 2024-11-17..2024-11-30 (descriptive-only, not a
confirmation set, not opened for CF-1 confirmation); v002 terminal 2024-12-01..2025-02-28; v002
sealed 2025-02-14..2025-02-28. `test_rows_loaded = 0` preserved.

## 15. Exact evaluation design

Chronological expanding-window walk-forward over 7 non-overlapping full-month evaluation blocks
Apr–Oct 2024 (B7 = 2024-10-02..2024-10-31); March = warmup; `2024-11-01..2024-11-15 =
UNUSED_NON_RESERVE_BUFFER` (never opened); 2024-11-16 = committed embargo exclusion. No evaluation
block, training set, or bootstrap uses any date on or after 2024-11-01. An origin is assigned to a
block by its own UTC date/time but is valid only if its entire completed target `(t, t+H]` — right
endpoint included — lies inside execution access; the `2024-10-31T23:00` origin is therefore invalid
and B7's last potentially valid origin is `2024-10-31T22:00`. Purge = 1h horizon; embargo = 1 calendar
day; preprocessing fit train-only; no random/shuffled split.

## 16. Primary loss

**QLIKE** (`v/h − ln(v/h) − 1`) with the fixed zero-RV safeguard `v = RV + ε`,
`h_m = max(exp(ŷ_m), ε)`, `ε = 1e-16` for both models — always finite, zero-RV origins retained, no
post-hoc clipping. Lower better; block-mean then equal-weighted across the 7 blocks (the `Δ_equal`
estimand). Secondary descriptive metrics (≤2, non-authorizing): MSE-on-variance; Mincer–Zarnowitz R².

## 17. Pass rule

`CF1_VALID_PASS` iff all of: (P1) `Δ_equal > 0`, where `d_{i,t} = QLIKE_base(i,t) − QLIKE_aug(i,t)`,
`D_i = (1/n_i) Σ_t d_{i,t}`, `Δ_equal = (1/7) Σ_{i=1}^{7} D_i`; (P2) augmented strictly better
(`D_i > 0`) in ≥ 6/7 blocks; (P3) the stratified-by-block moving-block bootstrap of the **same**
`Δ_equal` estimand gives `LB_95 = quantile({Δ_equal^(b)}, 0.05) > 0` (block-specific
`ℓ_i = ceil(n_i^(1/3))`, within-block resampling only, `B = 10,000`, seed `20260715`); (P4) run
validity (no invalid-run condition; all 7 blocks ≥ 100 valid origins). Zero-floor materiality. P2 and
P3 are independent; neither replaces the other.

## 18. Fail rule

`CF1_VALID_FAIL`: any valid run not meeting all of P1–P3. No borderline / weak / partial / secondary-
metric / post-hoc-subset pass.

## 19. Invalid-run rule

`CF1_INVALID_RUN`: target/feature/split/leakage/reserve/preprocessing/timestamp violation; missing or
undersized block; material implementation mismatch; numerical failure preventing the preregistered
comparison; or any unauthorized model/metric/horizon/threshold/feature/window/loss change. Not
scientifically interpretable; requires a separate corrective phase and new operator authorization.

## 20. Anti-rescue posture

A valid fail closes the CF-1 development family under this target/horizon/baseline/feature/evaluation
design and authorizes no neighboring variant; any later materially-different variant needs a new
mechanism justification, a new docs-only phase, an anti-duplication audit, and operator
authorization. A valid pass does not reopen `STOP_LONGHORIZON_ML_ARC` or
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`. Reinforces M0.10/M0.12, Phase 4bn-AS anti-rescue, and
Phase 4bn-AV §16.

## 21. Terminal / sealed exclusion

The v002 terminal window (2024-12-01..2025-02-28) and v002 sealed test (2025-02-14..2025-02-28)
remain `UNTOUCHED_RESERVED` and are excluded from the preregistered development experiment; no
reserve spend authorized; `test_rows_loaded = 0` preserved.

## 22. Consumed-holdout posture

The consumed pre-v002 internal holdout (2024-11-17..2024-11-30) is not reusable as independent
confirmation and is not designated as the CF-1 evaluation set; descriptive-only; no new holdout
created by relabeling it.

## 23. Checks run

- `git fetch origin`; `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- `git branch --show-current`; `git rev-parse HEAD` / `main` / `origin/main` → all
  `8b6c8614e37508cd05346f5ed90f8d08d9f68560` pre-branch.
- `git log --oneline -10 --decorate` → confirmed tip at the AX SHA-finalization commit.
- `git switch -c phase-4bn-ay/cf1-realized-volatility-substrate-test-preregistration` → branch
  created; working tree clean apart from the transient lock.
- Post-write validation (`git status --short`; `git diff --check`; `git diff --name-status`;
  `git diff --stat`) → exactly four added files, no modifications/deletions/renames, no whitespace
  errors; reproduced in the final operator report.

## 24. Tests / scripts / data / network not run

Because this is docs-only, the following were **not run**: pytest, Ruff, mypy, any project script,
builder, target/label generation, feature pipeline, diagnostic, model, hyperparameter search,
backtest, replay, or runtime process; no data workflow or acquisition workflow; no network, web
search, API, Binance endpoint, credential, WebSocket, exchange-write function, MCP, Graphify, or
`.mcp.json`; no Fable or external reviewer. No executable surface changed, so none applies.

## 25. Commit history and SHA self-reference convention

The Phase 4bn-AY branch comprises the following commits, in order:

| # | SHA | Commit message | Role |
|---|---|---|---|
| 1 | `c46cc6001d602d43c672aa94c069a34b5dc5d753` | `docs(phase-4bn-ay): preregister CF-1 volatility substrate test` | Original Phase 4bn-AY preregistration; **added** exactly the four files in §6. |
| 2 | `752d7ab27a81a2d4c42c89290d62a3d90a562d98` | `docs(phase-4bn-ay): tighten CF-1 preregistration contract` | First contract-tightening amendment (§33.A) — equal-weighted bootstrap estimand, zero-RV QLIKE safeguard, November buffer. Modified the same four files in place. |
| 3 | `ead199856beb1a440b4c432d1c0e571ec39a9eb3` | `docs(phase-4bn-ay): clarify half-open timestamp semantics` | Half-open timestamp-semantics amendment (§33.B). **Historical and `SUPERSEDED_BEFORE_MERGE_BY_THE_CAUSAL_COMPLETED_INTERVAL_CORRECTION`** — its `[a, b)` construction is **not** a live implementation rule anywhere. |
| 4 | `eeedab67c40a209c6ba85dcd3350752d735edc48` | `docs(phase-4bn-ay): correct causal RV boundary semantics` | **Final scientific-contract correction** (§33.C) — the causal completed-interval convention `(a, b]` with the single operator `P_at(u)` (`≤ u`). This is the approved scientific/mathematical contract. |
| 5 | *this commit* | `docs(phase-4bn-ay): correct closeout commit history` | **Closeout-history-only correction** (§33.D). Modifies **only this closeout file**; changes **no** scientific contract. Its SHA is recorded in the final operator report because a commit cannot embed its own SHA. |

Explicitly:

- Commit 3 (`ead19985…`) is **historical and superseded**; it is retained only as the labeled
  §33.B record and states its own supersession.
- Commit 4 (`eeedab67…`) is the **final scientific-contract correction** and remains the approved
  contract state.
- **This commit (5) changes no scientific, statistical, timestamp, target, feature, model, loss,
  bootstrap, split, verdict, consequence, evidence, or authorization rule** — it corrects closeout
  commit history only, and modifies no file other than this closeout.
- **No merge-closeout is created in this task**, and no SHA-finalization commit is performed by this
  phase. **Merge remains separately authorized** and is a distinct, operator-authorized step.

## 26. Local / origin branch equality placeholders

After push, `git rev-parse HEAD` == `git rev-parse phase-4bn-ay/…` ==
`git rev-parse origin/phase-4bn-ay/…` (the phase-branch SHA `<PHASE_COMMIT_SHA>`); recorded exactly in
the final operator report. `main` and `origin/main` remain at
`8b6c8614e37508cd05346f5ed90f8d08d9f68560` (untouched; no merge, no main push).

## 27. Exact final result state

`CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_PREREGISTERED__TARGET_FEATURE_BASELINE_SPLIT_LOSS_AND_PASS_FAIL_CONTRACT_FROZEN__BOOTSTRAP_ESTIMAND_ZERO_RV_EXECUTION_BOUNDARY_AND_CAUSAL_COMPLETED_INTERVAL_SEMANTICS_CLARIFIED__NO_DATA_OPENED__NO_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

## 28. No-execution statement

`No target generation, feature generation, model fitting, diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-AY.`

`No market data, feature row, label row, model output, diagnostic output, or evidence reserve was opened or read by Phase 4bn-AY.`

`The Phase 4bn-AY preregistration freezes the CF-1 development experiment contract but does not authorize that experiment to run.`

## 29. No-reserve-spend statement

`No evidence reserve is authorized for spending by Phase 4bn-AY.` The v002 terminal window and v002
sealed test remain `UNTOUCHED_RESERVED`; the consumed pre-v002 internal holdout remains descriptive-
only and is not a confirmation set.

## 30. Successor-authorization statement

`Phase 4bn-AZ or any other successor requires separate operator authorization and a new Claude Code
prompt.` The proposed successor title — `Phase 4bn-AZ — CF-1 Realized-Volatility Substrate-Test
Execution` — is proposed only and is not authorized by this phase.

## 31. Merge note

Merging Phase 4bn-AY into `main` requires a **separate operator prompt**. This phase does not merge,
does not create a merge-closeout, does not push `main`, and does not perform a SHA-finalization
commit. Recommended next operator action: return the four AY files and the final operator report to
ChatGPT for compliance review and a separate merge decision.

## 32. Preserved project locks

Unchanged: `STOP_LONGHORIZON_ML_ARC` and `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct; not
merged/softened/reinterpreted/rescued/reopened); the Phase 4bn-AX forced-flow rejection
`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`; the human operator as sole final authority;
Phase 4aw `flip_research_eligible(...)` always-raising, never invoked; `research_eligible = false`;
`eligibility_gate_status = pending`; all published authorization flags false; the Phase 4bn-AE §19 M0
boundary; the Phase 4ak twelve-clause M0 gate with §6 cooldown and §7 cooled-down families; the
locked 8 bps/side · 16 bps round-trip cost; the Phase 4bn-AV evidence ledger, spending-authority
standard, and late-inadmissibility protocol; all dataset identities and hashes;
split/holdout/sidecar/storage policies (Phase 4bn-Y / L / AA / 4bb-F); every prior verdict and
retained-evidence classification; and every completed implementation report.
`docs/00-meta/current-project-state.md` is left unchanged by this phase.

## 33. Post-review contract-verification amendments (pre-merge)

Three narrow, docs-only, pre-merge **contract** corrections were made on this Phase 4bn-AY branch
after the original preregistration commit, followed by one **closeout-history-only** correction. None
is a new scientific phase, a redesign of CF-1, the merge phase, execution authorization, or data
authorization. (Full commit table: §25.)

- **Original Phase 4bn-AY preregistration commit:** `c46cc6001d602d43c672aa94c069a34b5dc5d753`.
- **First contract-tightening amendment:** `752d7ab27a81a2d4c42c89290d62a3d90a562d98` (§33.A).
- **Half-open endpoint-semantics amendment:** `ead199856beb1a440b4c432d1c0e571ec39a9eb3` (§33.B) —
  **`SUPERSEDED_BEFORE_MERGE_BY_THE_CAUSAL_COMPLETED_INTERVAL_CORRECTION`**.
- **Final causal completed-interval correction (the approved scientific contract):**
  `eeedab67c40a209c6ba85dcd3350752d735edc48` (§33.C).
- **Closeout commit-history correction (this commit; closeout file only):** §33.D; its SHA is
  recorded in the final operator report.

### 33.A First amendment — bootstrap estimand, zero-RV QLIKE, November buffer

- **What happened:** after the original commit, a repository-grounded compliance review found the design
  substantially well constrained but identified three execution-bearing points needing to be made
  fully explicit and internally consistent **before merge**. A **narrow, docs-only contract-
  verification amendment** was made on the same Phase 4bn-AY branch. It is not a new scientific
  phase, not the merge phase, and not execution authorization.
- **The three clarified areas (and nothing else):**
  1. **Equal-weighted bootstrap estimand.** The uncertainty procedure now estimates the **same**
     equal-weighted seven-block estimand as the primary point estimate: `d_{i,t}`, `D_i`, and
     `Δ_equal = (1/7) Σ_{i=1}^{7} D_i` are defined exactly; the bootstrap is **stratified by
     evaluation block** with block-specific `ℓ_i = ceil(n_i^(1/3))`, within-block resampling only,
     equal-weighted recombination, `B = 10,000`, seed `20260715`, and `P3 iff LB_95 =
     quantile({Δ_equal^(b)}, 0.05) > 0`. The earlier "pooled per-origin `d̄`" phrasing — which could
     have implied origin-count weighting or cross-block pooling — is removed from every decision path.
  2. **Zero-RV QLIKE safeguard.** The loss is frozen as `v = RV + ε`, `h_m = max(exp(ŷ_m), ε)`,
     `ratio_m = v/h_m`, `QLIKE_m = ratio_m − ln(ratio_m) − 1`, with the same `ε = 1e-16` already used
     by the target and applied identically to both models; `exp(ŷ)` is clarified to forecast the
     positive `RV + ε`. Zero-RV observations are **retained**, never dropped; any non-finite actual,
     forecast, ratio, logarithm, or QLIKE is a technical invalidation; no alternative floor and no
     post-hoc clipping of ratio or loss is permitted.
  3. **Unused November 1–15 buffer.** The **committed non-reserve eligibility envelope** (through
     2024-11-15, 259 dates) is now explicitly distinguished from the **frozen CF-1 primary
     execution-access boundary** (`2024-03-01 through 2024-10-31 UTC, excluding 2024-10-01`; 244
     dates). `2024-11-01..2024-11-15` is frozen as `UNUSED_NON_RESERVE_BUFFER` — unopened and unused:
     not training, evaluation, bootstrap, confirmation, holdout, fallback, preprocessing, threshold
     choice, or diagnostics; never plotted or interpreted. Eligibility is not access. The execution
     checklist now **fails preflight** if any 2024-11-01..2024-11-15 row is proposed to be opened or
     used. 2024-11-16 remains a committed embargo exclusion; 2024-11-17..2024-11-30 remains the
     consumed internal holdout; 2024-12-01 onward remains terminal/sealed reserve territory.
- **Nothing scientific changed.** The amendment changed **no** scientific hypothesis, target family,
  horizon (60 min), forecast cadence, feature set (the same three sign-invariant 60s features), model
  (HAR-style OLS baseline; nested augmented OLS), primary loss (QLIKE), secondary metrics, number of
  evaluation blocks (7), block-consistency threshold (6 of 7), materiality floor (zero), bootstrap
  replicate count (10,000), confidence level (one-sided 95%), seed (`20260715`), verdict vocabulary
  (`CF1_VALID_PASS` / `CF1_VALID_FAIL` / `CF1_INVALID_RUN`), or any pass/fail/invalid project
  consequence. All anti-tuning, anti-switching, anti-rescue, evidence-reserve, and non-authorization
  boundaries are preserved exactly.
- **No data or reserve opened.** The amendment read only committed documentation and Git metadata. No
  market data, feature row, label row, model output, diagnostic output, or evidence reserve was
  opened or read. No QLIKE, bootstrap, target, feature, model, diagnostic, or backtest was computed.
- **Diff shape preserved.** Only the four Phase 4bn-AY files were modified in place; no fifth file was
  added; nothing was deleted or renamed; the base-to-final branch diff versus
  `8b6c8614e37508cd05346f5ed90f8d08d9f68560` remains **exactly four added files**.
- **Amendment SHA.** `752d7ab27a81a2d4c42c89290d62a3d90a562d98`.
- **Still not authorized:** merge into `main`, a merge-closeout, Phase 4bn-AZ, any execution, any data
  read, or any evidence-reserve spend. Merge remains a separate operator decision.

### 33.B Half-open timestamp-endpoint amendment — `SUPERSEDED_BEFORE_MERGE_BY_THE_CAUSAL_COMPLETED_INTERVAL_CORRECTION`

**This entire subsection is a historical amendment record only.** The half-open `[a, b)` construction
it describes is **superseded before merge** by §33.C and is **not** a live implementation rule
anywhere in the Phase 4bn-AY contract, memo, or checklist.

- **What happened:** a final contract review identified one remaining execution-bearing ambiguity.
  The target interval was declared right-open `[t, t + H)`, but the grid notation defined a single
  operator `P(τ)` using `source_transact_time_ms ≤ τ` for **every** grid instant — which could be read
  as admitting a trade timestamped exactly at the right endpoint `t + H`, even though that endpoint
  lies outside the declared interval. Related HAR notation alternated between `(t − L, t]` (prose) and
  `[t − L, t)` (formula). This amendment resolves **only** that endpoint/tie ambiguity.
- **Exact clarification (frozen):**
  - **Right-open target and HAR intervals.** Every CF-1 realized-variance interval — target and HAR
    lookback alike — is half-open `[a, b)`: it includes information available at the left endpoint `a`
    and excludes every trade whose event timestamp is exactly the right endpoint `b`. There is no
    right-closed realized-variance interval anywhere in the contract; the conflicting `(t − L, t]` /
    "right-closed HAR lookback" notation is removed.
  - **Left endpoint uses `≤`.** `P_start(a)` = price of the canonical last aggTrade with
    `source_transact_time_ms ≤ a`, ties broken by greatest canonical `row_index` (the committed
    `row_index_le_R` rule).
  - **Interior and terminal right boundaries use `<`.** `P_minus(u)` = price of the canonical last
    aggTrade with `source_transact_time_ms < u`, applied at **every** grid boundary strictly after the
    interval start, **including the terminal boundary**. Frozen formula: `τ_k = a + k×60,000 ms`,
    `G_0 = P_start(a)`, `G_k = P_minus(τ_k)`, `r_k = ln(G_k/G_{k-1})`, `RV[a,b) = Σ_{k=1}^{60} r_k²`.
    `≤ τ_k` is prohibited for `k ≥ 1`. A boundary trade is assigned exactly once, to the interval
    **beginning** at its timestamp. Consequently no HAR regressor at origin `t` uses a trade
    timestamped exactly `t` — the intended meaning of "strictly past-only".
  - **Feature snapshot at the origin remains `≤`.** The three microstructure features are snapshotted
    from the last committed feature row with `feature_timestamp_ms ≤ t`; a row timestamped exactly `t`
    is available and may be used. This asymmetry is intentional and is **not** leakage: information at
    the origin is available at the origin, the future target begins after it, and every event is
    assigned consistently under the half-open convention.
  - **Final October target opens no November row.** The terminal price of
    `[2024-10-31T23:00:00.000Z, 2024-11-01T00:00:00.000Z)` is `P_minus(2024-11-01T00:00:00.000Z)`,
    formed only from `source_transact_time_ms < 2024-11-01T00:00:00.000Z` — a causal **left-limit**
    price, not ordinary LOCF using `≤`. 2024-11-01..2024-11-15 remains unopened and unused.
  - **Coverage made consistent, threshold unchanged.** `[τ_{k-1}, τ_k)` is covered iff ≥ 1 actual
    aggTrade satisfies `τ_{k-1} ≤ source_transact_time_ms < τ_k`; the ≥ 30-of-60 threshold, causal
    carry-forward, no-look-ahead, no-stitching, and zero-RV-retention rules are unchanged.
  - **Invalid-run and checklist.** Endpoint-convention violations now route explicitly to
    `CF1_INVALID_RUN`, and the checklist adds seven preflight gates plus a required **deterministic
    timestamp-boundary proof** over **synthetic timestamp cases only** (no market data, no reserve),
    to be emitted and validated by the later execution code before any metric is computed. **That
    proof was not run during this docs-only amendment.**
- **Nothing scientific or statistical changed.** No change to the hypothesis, target family, source,
  1-minute UTC grid, causal construction, horizon (60 min), cadence (top-of-UTC-hour), non-overlapping
  intervals, `RV = Σ r_k²`, `y = ln(RV + 1e-16)`, no-annualization, the HAR-style log-RV OLS baseline
  or its 1h/24h/168h lengths and averaging, the nested augmented OLS, the three sign-invariant
  features, log + train-only z-score, seven evaluation blocks, the execution-access boundary ending
  2024-10-31, the `UNUSED_NON_RESERVE_BUFFER`, purge/embargo, QLIKE, the QLIKE epsilon, the
  equal-weighted seven-block estimand, the stratified-by-block moving-block bootstrap, 10,000
  replicates, one-sided 95%, seed `20260715`, 6-of-7 block consistency, the pass/fail/invalid rules, or
  any project consequence. All anti-tuning, anti-switching, anti-rescue, evidence, reserve, and
  non-authorization boundaries are preserved exactly.
- **No data or reserve opened.** Only committed documentation and Git metadata were read. No market
  data, feature row, label row, model output, diagnostic output, or evidence reserve was opened. No
  boundary proof, QLIKE, bootstrap, target, feature, model, diagnostic, or backtest was computed.
- **Diff shape preserved.** Only the four Phase 4bn-AY files were modified in place; no fifth file
  added; nothing deleted or renamed; the base-to-final branch diff versus
  `8b6c8614e37508cd05346f5ed90f8d08d9f68560` remains **exactly four added files**.
- **Amendment SHA.** `ead199856beb1a440b4c432d1c0e571ec39a9eb3`.
- **Still not authorized:** merge into `main`, a merge-closeout, Phase 4bn-AZ, any execution, any data
  read, the timestamp-boundary proof, or any evidence-reserve spend. Merge remains a separate operator
  decision.

### 33.C Final amendment — causal completed-interval correction

- **Why the half-open specification (§33.B) was superseded — boundary-jump omission.** That
  specification paired `G_0 = P_start(a)` (trades `≤ a`) with `G_k = P_minus(τ_k)` (trades `< τ_k`).
  For a trade occurring exactly at a shared boundary `a`: the **preceding** interval excluded it at
  its right endpoint, while the **following** interval already contained its price in `G_0`. The
  price jump from the last pre-`a` trade to the trade at `a` therefore appeared in **neither**
  interval's return sequence. That contradicted the "assigned exactly once" rule and could
  **understate realized variance at exact clock boundaries** — a mathematical defect, not a wording
  issue.
- **Why `P_minus(a)` at the target start was not adopted instead.** Replacing `G_0` with `P_minus(a)`
  would have captured the boundary jump in the following interval, but under the existing information
  set the feature snapshot at origin `t` may use a trade timestamped exactly `t`; the future target
  would then contain a price jump that was **already observed at the origin**. That is a causality
  defect, so it was rejected.
- **Exact final solution (frozen).**
  - **Convention:** every CF-1 realized-variance interval is a **causal completed interval `(a, b]`** —
    target, previous-hour RV, each hourly RV in the 24h and 168h HAR means, and the coverage minutes.
    A trade at exactly `a` is **not** in `(a, b]`; a trade at exactly `b` **is**. Adjacent `(a,b]` and
    `(b,c]` assign a trade at exactly `b` to the interval **ending** at `b`. Every boundary event is
    assigned **exactly once**. No live `[a, b)` RV interval remains.
  - **Single operator:** `P_at(u)` = price of the canonical last aggTrade with
    `source_transact_time_ms ≤ u`, ties by greatest canonical `row_index` (committed `row_index_le_R`).
    `P_start`, `P_minus`, strict `<` at an RV boundary, mixed operators, and left-limit terminal prices
    are removed as live concepts.
  - **Formula:** `τ_k = a + k·60,000 ms` (`k = 0…60`), `G_k = P_at(τ_k)`, `r_k = ln(G_k/G_{k-1})`
    (`k = 1…60`), `RV(a,b] = Σ r_k²`. No boundary jump omitted; no boundary trade double-counted.
  - **Target:** `(t, t + H]`, `RV_target(t) = RV(t, t+H]`. `G_0 = P_at(t)` is already-known origin
    information, so the target contains no already-observed origin-time jump; a trade at exactly `t+H`
    belongs to this target; the next target `(t+H, t+2H]` starts from `P_at(t+H)` without re-counting.
    Adjacent target intervals remain non-overlapping.
  - **Feature snapshot:** unchanged at `feature_timestamp_ms ≤ t`; a row at exactly `t` may be used.
    It now reads the **same** origin information set as `G_0 = P_at(t)` and the HAR terminal price, so
    the earlier "intentional asymmetry" framing no longer applies and was removed.
  - **HAR:** `RV_h(t) = RV(t − 1h, t]`; daily mean over the 24 completed hourly intervals
    `(t−24h, t−23h] … (t−1h, t]`; weekly mean over the 168 completed hourly intervals tiling
    `(t−168h, t]`. A trade at exactly `t` is known at the origin and **may** enter `RV_h(t)`; it is not
    in the target because it is already in `G_0`. Causal, no future look-ahead. Lengths, averaging, and
    OLS unchanged.
  - **Coverage:** `(τ_{k-1}, τ_k]` covered iff ≥ 1 aggTrade with `τ_{k-1} < ts ≤ τ_k`; threshold
    unchanged at ≥ 30 of 60; causal carry-forward, no look-ahead, no stitching, no zero-RV drop.
  - **Final October origin:** because `P_at(b)` uses `≤ b`, an origin is valid only if its **entire**
    completed target `(t, t+H]` — right endpoint included — lies inside execution access. The
    `2024-10-31T23:00` origin is therefore **invalid** (endpoint `2024-11-01T00:00:00.000Z`), and the
    **last potentially valid October origin is `2024-10-31T22:00`** (target ends
    `2024-10-31T23:00:00.000Z`). The dropped hour is removed identically from both models. **No
    2024-11-01 row — including one at exactly midnight — is opened**, and no excluded endpoint is
    loaded merely to form `P_at(endpoint)`. The superseded left-limit example retaining the 23:00
    origin is withdrawn; this may reduce B7's possible origin count by **one** relative to it.
  - **Invalid-run / checklist:** completed-interval violations route to `CF1_INVALID_RUN`, and the
    checklist carries ten explicit gates plus a **deterministic timestamp-boundary proof** over
    **synthetic timestamp cases only** (price 100 at `09:59:59.999`, 110 at exactly `10:00:00.000`),
    to be emitted and validated by the later execution code **before any market data is opened**.
    **That proof was not run during this docs-only amendment.**
- **Preserved unchanged.** B7's date identity, the seven-block structure, the ≥ 100 valid-paired-origin
  minimum, equal block weighting; and every prior correction: the equal-weighted `Δ_equal` statistic
  and P1; the stratified-by-block moving-block bootstrap (`ℓ_i = ceil(n_i^(1/3))`, within-block only,
  `B = 10,000`, seed `20260715`, `LB_95 = quantile(·, 0.05)`, P3 iff `LB_95 > 0`, no pooled
  origin-count weighting); the QLIKE safeguard (`v = RV + 1e-16`, `h_m = max(exp(ŷ_m), 1e-16)`,
  zero-RV origins retained, all values finite, no alternative floor, no post-hoc loss clipping); and
  `2024-11-01..2024-11-15 = UNUSED_NON_RESERVE_BUFFER`, unopened and unused.
- **Nothing scientific or statistical changed.** No change to the hypothesis, target family, source,
  1-minute UTC grid, horizon (60 min), forecast cadence, `RV = Σ r_k²`, `y = ln(RV + 1e-16)`,
  no-annualization, the HAR-style log-RV OLS baseline, the nested augmented OLS, the three
  sign-invariant features, log + train-only z-score, seven evaluation blocks, the committed eligibility
  envelope, the execution-access boundary, purge/embargo, QLIKE, the QLIKE epsilon, the
  equal-weighted seven-block estimand, the bootstrap, 10,000 replicates, one-sided 95%, seed
  `20260715`, 6-of-7 block consistency, the pass rule, the pass/fail/invalid consequences, or any
  evidence classification. Only the RV interval-closure convention and its directly dependent
  checklist / invalid-run wording changed.
- **No data or reserve opened.** Only committed documentation and Git metadata were read. No boundary
  proof, QLIKE, bootstrap, target, feature, model, diagnostic, or backtest was computed.
- **Diff shape preserved.** Only the four Phase 4bn-AY files were modified in place; no fifth file
  added; nothing deleted or renamed; the base-to-final branch diff versus
  `8b6c8614e37508cd05346f5ed90f8d08d9f68560` remains **exactly four added files**.
- **Amendment SHA.** `eeedab67c40a209c6ba85dcd3350752d735edc48` — the **final scientific-contract
  correction** and the approved contract state.
- **Still not authorized:** merge into `main`, a merge-closeout, Phase 4bn-AZ, any execution, any data
  read, the deterministic boundary proof, or any evidence-reserve spend. Merge remains a separate
  operator decision.

### 33.D Final closeout commit-history correction

- **What happened.** After the scientific contract was **approved** (final contract state
  `eeedab67c40a209c6ba85dcd3350752d735edc48`, §33.C), a final review found **one documentation defect
  only**: the closeout's commit-history section (§25) still described the **superseded** half-open
  timestamp amendment (`ead19985…`) as the *final* amendment, even though the later causal
  completed-interval correction had become the final branch state. This correction fixes that record.
- **Only the closeout file changed.** This correction modifies exactly
  `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_closeout.md` and **no other file**. The
  main preregistration memo, the implementation-grade contract, and the execution-validation checklist
  are **untouched**.
- **What was corrected.**
  1. **§25 stale history →** replaced with an accurate, ordered commit table naming all four prior
     commits plus this one, marking `ead19985…` historical/superseded and `eeedab67…` the final
     scientific-contract correction.
  2. **§6 singular/plural wording →** now states the four files were amended in place by **three**
     pre-merge contract corrections, followed by this closeout-history-only correction (which touches
     only the closeout).
  3. **§33 intro →** minimal consistency edit so it aligns with the corrected §25 and distinguishes
     the original preregistration, the first amendment, the superseded half-open amendment, the final
     causal completed-interval correction, and this closeout-history-only correction. The scientific
     explanation in §33.C is preserved unchanged.
- **The commit sequence is now accurate** (§25).
- **No scientific, statistical, timestamp, target, feature, model, loss, bootstrap, split, verdict,
  consequence, evidence, or authorization rule changed.** The live contract remains exactly as
  approved: RV intervals `(a, b]`; the single canonical operator `P_at(u)` using
  `source_transact_time_ms ≤ u`; `G_k = P_at(τ_k)`, `r_k = ln(G_k/G_{k-1})`, `RV(a,b] = Σ r_k²`;
  target `(t, t+H]` with `H = 60 min` at top-of-UTC-hour origins; HAR `(t−L, t]` (1h / 24 completed
  hourly / 168 completed hourly); feature snapshot `feature_timestamp_ms ≤ t`; the three
  sign-invariant features; HAR-style OLS baseline and nested augmented OLS; QLIKE with
  `v = RV + 1e-16` and `h = max(exp(ŷ), 1e-16)`; zero-RV retention; seven evaluation blocks;
  `Δ_equal = (1/7) Σ_i D_i`; the block-specific stratified moving-block bootstrap, 10,000 replicates,
  seed `20260715`, P3 iff `LB_95 > 0`; 6-of-7 block consistency; last potentially valid October origin
  `2024-10-31T22:00:00.000Z` and invalid `2024-10-31T23:00:00.000Z`; `2024-11-01..2024-11-15 =
  UNUSED_NON_RESERVE_BUFFER` with no November row opened; and all pass/fail/invalid routing,
  anti-tuning, anti-switching, anti-rescue, terminal/sealed/consumed-holdout exclusions, stopped arcs,
  and governance locks.
- **No data or reserve was opened.** Only committed documentation and Git metadata were read.
- **No execution ran.** No boundary proof, QLIKE, bootstrap, target, feature, model, diagnostic, or
  backtest was computed.
- **Diff shape preserved.** The base-to-final branch diff versus
  `8b6c8614e37508cd05346f5ed90f8d08d9f68560` remains **exactly four added AY documents**; this commit
  contributes exactly one `M` entry (the closeout) relative to `eeedab67…`.
- **Correction SHA.** This correction commit's exact SHA cannot be embedded inside itself; it is
  recorded in the final operator report and in the Git log after commit.
- **Merge remains unauthorized** until a separate merge prompt. No merge-closeout is created here.
