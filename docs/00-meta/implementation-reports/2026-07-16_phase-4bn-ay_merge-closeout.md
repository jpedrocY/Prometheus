# Phase 4bn-AY — Merge Closeout

## 1. Phase identity

Phase 4bn-AY — CF-1 Realized-Volatility Magnitude-Forecasting Substrate-Test Preregistration
(docs-only, low-researcher-freedom). Branch:
`phase-4bn-ay/cf1-realized-volatility-substrate-test-preregistration`.

## 2. Phase type and merge action

Docs-only **preregistration** phase (contract freeze only). The merge action brings four Phase
4bn-AY documentation files — plus this merge-closeout — onto `main` via an explicit
no-fast-forward merge commit, followed by one narrow SHA-finalization update of this file. The merge
changes no executable surface, no data, no manifest, no eligibility state, no verdict, no reserve,
and no lock. It authorizes no execution.

## 3. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — it governs the
scientific design of the one currently-selected research arc, so it is treated at the highest
ceremony tier even though it mutates no eligibility, manifest, verdict, reserve, or lock and freezes
a contract only.

## 4. Source and target branches

- **Source:** `phase-4bn-ay/cf1-realized-volatility-substrate-test-preregistration`.
- **Target:** `main`.

## 5. Pre-merge `main` / base SHA

`8b6c8614e37508cd05346f5ed90f8d08d9f68560` (`HEAD == main == origin/main` at merge time; tip after
the Phase 4bn-AX merge-closeout SHA-finalization commit). Verified in sync before any mutation. The
only untracked item was the transient `.claude/scheduled_tasks.lock`, which was not staged,
modified, deleted, cleaned, or committed.

## 6. Complete Phase 4bn-AY source-branch commit history

Six commits on the source branch after the base, preserved exactly — not squashed, reordered,
rebased, amended, or rewritten:

| # | SHA | Commit message | Role |
|---|---|---|---|
| 1 | `c46cc6001d602d43c672aa94c069a34b5dc5d753` | `docs(phase-4bn-ay): preregister CF-1 volatility substrate test` | Original Phase 4bn-AY preregistration; added the four AY documents. |
| 2 | `752d7ab27a81a2d4c42c89290d62a3d90a562d98` | `docs(phase-4bn-ay): tighten CF-1 preregistration contract` | Bootstrap-estimand / zero-RV QLIKE / November-buffer tightening. |
| 3 | `ead199856beb1a440b4c432d1c0e571ec39a9eb3` | `docs(phase-4bn-ay): clarify half-open timestamp semantics` | **Historical half-open amendment — `SUPERSEDED_BEFORE_MERGE_BY_THE_CAUSAL_COMPLETED_INTERVAL_CORRECTION`.** Its half-open `[a, b)` specification is **not** a live contract rule. |
| 4 | `eeedab67c40a209c6ba85dcd3350752d735edc48` | `docs(phase-4bn-ay): correct causal RV boundary semantics` | **Final causal completed-interval scientific-contract correction** — the approved `(a, b]` / `P_at(u)` convention. |
| 5 | `918ef91baa4c658d9191853bcd7065f36b3b7397` | `docs(phase-4bn-ay): correct closeout commit history` | Closeout-history-only correction (no scientific change). |
| 6 | `0fb560656aa9b50cf110602e15be8222b7343623` | `docs(phase-4bn-ay): correct coverage proof predicate` | Final live coverage-proof-predicate correction (one predicate in the §33 proof requirement). |

The Phase 4bn-AY closeout (`2026-07-15_phase-4bn-ay_closeout.md`) intentionally does **not** embed
commit 6's SHA, because that commit post-dates it; it was not modified recursively. This
merge-closeout is the authoritative record of the complete six-commit history.

## 7. Final pre-merge scientific-contract branch-tip SHA

`0fb560656aa9b50cf110602e15be8222b7343623` — the approved Phase 4bn-AY scientific-contract state at
merge time.

## 8. Merge-closeout branch commit SHA

`TO_BE_FILLED_AFTER_COMMIT` — the commit on the AY branch that adds this merge-closeout file
(`docs(phase-4bn-ay): add merge closeout`). This becomes the **seventh** commit on the source branch.

## 9. No-fast-forward merge commit SHA

`TO_BE_FILLED_AFTER_MERGE` — the no-fast-forward merge commit created on `main`
(`docs(phase-4bn-ay): merge CF-1 volatility substrate preregistration`).

## 10. SHA-finalization commit statement

SHA-finalization commit SHA:
this update (`docs(phase-4bn-ay): finalize merge closeout shas`);
its exact SHA equals the resulting final `main` / `origin/main` tip and is
recorded in the final operator report and Git log. Its own SHA is not embedded inside the
commit that creates it.

## 11. Final `main` / `origin/main` statement

After the SHA-finalization commit is pushed, final `main` and `origin/main` will both equal the
SHA-finalization commit SHA (§10). `HEAD == main == origin/main` at completion.

## 12. Merge method

`git merge --no-ff` with an explicit merge commit. No fast-forward, no squash, no rebase, no amend,
no history rewrite, no hook skipping, no signing disablement, no force push.

## 13. Files brought forward

Exactly four AY documentation files, all additions:

1. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_cf1-realized-volatility-substrate-test-preregistration.md` — AY main preregistration memo.
2. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_cf1-target-feature-baseline-and-evaluation-contract.md` — AY implementation-grade frozen contract.
3. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_cf1-execution-validation-checklist.md` — AY execution-validation checklist for a later phase.
4. `docs/00-meta/implementation-reports/2026-07-15_phase-4bn-ay_closeout.md` — AY phase closeout.

This merge-closeout file (`2026-07-16_phase-4bn-ay_merge-closeout.md`) is added on the AY branch
before the merge, so the merged base-to-final diff carries **five** added documents in total.

## 14. Additions-only confirmation

Confirmed additions-only. No existing file was modified, renamed, or deleted by the AY branch or by
the merge. The base-to-final diff contains only added AY documents plus one later narrow
modification of this merge-closeout file solely for SHA finalization.

## 15. Diff summary

- **Pre-merge branch diff (`main..AY`):** exactly the four added AY files, `2,081` insertions, no
  modifications / deletions / renames, no whitespace errors (`git diff --check` clean).
- **Merged base-to-final diff (`8b6c8614..HEAD`):** five added AY documents (the four above plus this
  merge-closeout), then one later modification of this merge-closeout solely to finalize the exact
  SHAs. No source, test, script, config, data, manifest, gate, sidecar, split, prior report, README,
  current-project-state, M0, evidence-ledger, phase-gate, technical-debt-register, or
  existing-process-standard file changed.

## 16. AX selection lineage and AY purpose

Phase 4bn-AX selected exactly `SELECT_CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_FOR_LATER_
PREREGISTRATION`, rejected the forced-flow family
(`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`), and proposed — without authorizing — a
docs-only Phase 4bn-AY. CF-1 was selected **only** as a realized-volatility magnitude-forecasting
substrate test, never as a trading strategy, directional hypothesis, profitability claim,
data-execution authorization, or reserve-spend authorization. Phase 4bn-AY operationalizes that
selection at the design level only: it freezes the entire CF-1 development experiment **before** any
market data is opened and before any target, feature, model, metric, diagnostic, or backtest is run,
eliminating researcher freedom prior to execution.

## 17. Scientific hypothesis

Can predeclared, **non-directional** aggTrades microstructure variables improve future
realized-volatility **magnitude** forecasts beyond a simple, predeclared realized-volatility
persistence / HAR-style baseline? Null (`H0`): the augmented model achieves no strictly positive,
block-consistent, uncertainty-supported QLIKE improvement over the HAR-style baseline
(`E[d_{i,t}] ≤ 0`). Alternative (`H1`): it does, under the frozen block-consistency and uncertainty
criteria. Mechanism: realized variance clusters and exhibits long memory (ARCH/HAR stylized fact); a
hour/day/week cascade of past RV captures most of that persistence, and the claim is that recent
order-flow intensity and traded-volume/size carry **incremental information-arrival** signal about
near-future realized variance beyond past RV alone. The mechanism is non-directional by construction
and uses only sign-invariant inputs.

## 18. Exact target and horizon

- **Target family:** future **realized variance** of the BTCUSDT last-trade log price. No direction,
  sign, return-classification, continuation, reversion, liquidation, or forced-flow target.
- **Horizon:** exactly one — **`H = 60 minutes`** (3,600,000 ms).
- **Cadence:** one forecast origin at the **top of every UTC hour** (`HH:00:00.000`);
  **non-overlapping** target intervals.
- **Transform:** `y = ln(RV + 1e-16)`; forecasts exponentiated back to a positive variance.
- **No annualization.**

## 19. Exact timestamp and boundary convention

- **Every CF-1 realized-variance interval is a causal completed interval `(a, b]`** — target and HAR
  lookback alike. There is **no live half-open `[a, b)` RV interval** anywhere in the contract.
- **Target intervals:** `(t, t + H]`.
- **Canonical grid-price operator (the only one):**
  `P_at(u)` = price of the canonical last aggTrade with `source_transact_time_ms ≤ u`.
- **Same-timestamp tie:** greatest canonical `row_index`, consistent with the committed
  `row_index_le_R` rule.
- **Minute grid:** `τ_k = a + k × 60,000 ms`, `k = 0…60`; `G_k = P_at(τ_k)`;
  `r_k = ln(G_k / G_{k-1})`; `RV(a, b] = Σ_{k=1}^{60} r_k²`.
- **Boundary assignment:** a trade at exactly the left endpoint is **not** part of `(a, b]`; a trade
  at exactly the right endpoint **is**. A boundary trade belongs **exactly once**, to the interval
  **ending** at its timestamp. The origin-time trade is reflected in `G_0 = P_at(t)` and does not
  enter the future return. **No exact-boundary price jump is omitted or double-counted.**
- `P_start`, `P_minus`, strict `<` at an RV grid boundary, mixed `≤`/`<` operators inside one RV
  interval, and left-limit terminal prices are **prohibited as live execution concepts**; any
  surviving mention is only a prohibition, an invalid-run condition, or a clearly labeled superseded
  historical record.

## 20. Exact HAR baseline

- `RV_h(t) = RV(t − 1h, t]`.
- `RV_d(t)` = mean of the **24** completed hourly RV intervals ending at `t`.
- `RV_w(t)` = mean of the **168** completed hourly RV intervals ending at `t`.
- HAR-style **OLS in log-variance space**, **intercept included**, forecasts exponentiated to
  guarantee positive variance.
- **Exactly one baseline. No baseline shopping.** No tuning; no lag search; no alternate cascade.
- Every HAR interval uses the same `P_at(·)` operator and minute-return formula as the target; a
  trade timestamped exactly `t` is known at the origin and **may** enter `RV_h(t)`, while it is not
  part of the future target because it is already contained in `G_0 = P_at(t)`. This is causal and
  contains no future look-ahead.

## 21. Exact augmented model and feature contract

Nested OLS adding **exactly three** committed, sign-invariant 60s features:

- `rolling_aggtrade_count_60s` (trade-arrival intensity);
- `rolling_quantity_sum_60s` (unsigned traded-volume intensity);
- `rolling_quantity_mean_60s` (mean trade size).

- **Feature snapshot:** the last committed feature row with `feature_timestamp_ms ≤ t`, committed
  greatest-`row_index` tie rule; a row timestamped exactly `t` is available and may be used.
- **Transforms:** natural logarithm, then **train-only z-score** with
  `STANDARDIZATION_EPSILON = 1e-8`. No clipping, no winsorization, no interactions, no polynomial
  expansion, no other feature or window.
- **Nesting:** the baseline is exactly the augmented model with the three microstructure coefficients
  set to zero — identical target, training window, estimator, forecast origins, and preprocessing —
  so the comparison isolates **incremental microstructure information**, not model-class superiority.
- **No directional, signed-flow, funding, calendar, open-interest, order-book, forced-flow, or
  liquidation feature is authorized.** No sign-invariant dispersion feature is used because none
  exists in the committed 45-column schema; none was invented.

## 22. Exact development-access boundary

- **Committed non-reserve eligibility envelope:** 2024-03-01..2024-09-30 ∪ 2024-10-02..2024-11-15 =
  **259 dates**.
- **Frozen CF-1 primary execution-access boundary:** **2024-03-01 through 2024-10-31 UTC, excluding
  2024-10-01 = 244 dates** — the only dates a future execution may open or use. Eligibility is **not**
  access.
- **`2024-11-01 through 2024-11-15 = UNUSED_NON_RESERVE_BUFFER`** — unopened and unused: not
  training, not evaluation, not bootstrap, not confirmation, not a holdout, not a fallback, not
  preprocessing, not threshold choice, not diagnostics; never plotted or interpreted.
- 2024-11-16 remains a committed embargo exclusion.

## 23. Exact October/November boundary

Because `P_at(b)` uses `≤ b`, an origin is valid only if its **entire** completed target `(t, t+H]` —
**right endpoint included** — lies inside the execution-access boundary. Therefore:

- the origin **`2024-10-31T23:00:00.000Z` is INVALID** (its target endpoint is
  `2024-11-01T00:00:00.000Z`, outside execution access and inside the unopened buffer date);
- the **last potentially valid October forecast origin is `2024-10-31T22:00:00.000Z`**, whose target
  `(22:00, 23:00]` ends at `2024-10-31T23:00:00.000Z`;
- the final unavailable clock hour is a partial / out-of-boundary target, **dropped identically from
  both models**;
- **no 2024-11-01 row — including one timestamped exactly at midnight — may be opened**, and no
  excluded endpoint may be loaded merely to form `P_at(endpoint)`.

## 24. Exact covered-minute rule and QLIKE safeguard

**Covered-minute rule (live):** `(τ_{k-1}, τ_k]` is covered iff at least one actual aggTrade
satisfies `τ_{k-1} < source_transact_time_ms ≤ τ_k`. Short-form proof predicate:
`τ_{k-1} < ts ≤ τ_k`. Coverage threshold: **`≥ 30 of 60`**. The superseded predicate
`τ_{k-1} ≤ ts < τ_k` does **not** appear as a live rule anywhere. Causal carry-forward; no future
look-ahead; no stitching across embargo, unused-buffer, holdout, terminal, or sealed boundaries.

**QLIKE safeguard (live), for model `m ∈ {B, A}`:**

```
v         = RV + 1e-16
h_m       = max( exp(ŷ_m), 1e-16 )
ratio_m   = v / h_m
QLIKE_m   = ratio_m − ln(ratio_m) − 1
```

Zero-RV observations are **retained**, never dropped for being zero; all actuals, forecasts, ratios,
logarithms, and losses must be finite; **no alternative floor**; **no post-hoc clipping** of the ratio
or loss.

## 25. Exact primary equal-weighted estimand

For evaluation block `i ∈ {1…7}` and valid origin `t`:

```
d_{i,t} = QLIKE_base(i,t) − QLIKE_aug(i,t)
D_i     = (1 / n_i) · Σ_t d_{i,t}
Δ_equal = (1 / 7) · Σ_{i=1}^{7} D_i
```

**P1 iff `Δ_equal > 0`.** There is **no origin-count-weighted pooled decision statistic** and no
cross-block pooling at any decision stage.

## 26. Exact bootstrap

**Stratified-by-evaluation-block moving-block bootstrap** of the **same** `Δ_equal` estimand:

- the seven evaluation blocks remain **separate**;
- **within-block** moving-block resampling only, chronological order preserved;
- block-specific `ℓ_i = ceil(n_i^(1/3))`; resample to exactly `n_i` (final block truncated);
- `D_i^(b) = mean(d_{i,*}^{(b)})`; `Δ_equal^(b) = (1/7) · Σ_i D_i^(b)`;
- exactly **`B = 10,000`** replicates; **seed `20260715`**;
- one-sided **95%** percentile lower bound `LB_95 = quantile({Δ_equal^(b)}, 0.05)`;
- **P3 iff `LB_95 > 0`**;
- **no resampling across evaluation-block boundaries**; no pooled origin-count weighting; **no
  alternate uncertainty method may replace the preregistered method** after execution.

## 27. Evaluation design

Seven chronological blocks, April–October 2024 (B7 = 2024-10-02..2024-10-31); March 2024 train-only
warmup. Expanding-window walk-forward, **one fit per block**; **purge = 1 hour**; **embargo = 1
calendar day**; preprocessing fit on **training origins only**; **minimum 70** augmented-model
training origins; **minimum 100** paired valid origins per evaluation block. No random split, no
shuffled CV, no resampling across time.

## 28. Pass rule

`CF1_VALID_PASS` iff **all** hold simultaneously:

- **P1:** `Δ_equal > 0` (strict; zero-floor materiality);
- **P2:** at least **6 of 7** observed `D_i > 0` (block consistency);
- **P3:** `LB_95 > 0`;
- **P4:** run valid and all block minimums met.

P2 and P3 are independent; neither replaces the other.

## 29. Fail rule

`CF1_VALID_FAIL`: any scientifically valid run not meeting all of P1–P3. **No borderline, promising,
weak, or partial pass**; no pass on a secondary metric; no pass on a post-hoc subset.

## 30. Invalid-run rule

`CF1_INVALID_RUN`: any contract, timestamp, boundary, split, leakage, reserve, preprocessing,
numerical, model, metric, feature, horizon, cadence, threshold, or implementation violation —
including a live `[a, b)` RV interval, `P_minus` / strict `<` at an RV boundary, mixed operators, the
origin-time jump inside the future target, an omitted boundary jump, a boundary trade double-assigned
or unassigned, HAR built as `[t−L, t)`, opening a 2024-11-01 row to score the `2024-10-31T23:00`
origin, retaining an origin whose target endpoint lies outside execution access, or a failed/absent
deterministic timestamp-boundary proof. An invalid run is **not** scientifically interpretable.

## 31. Anti-tuning and anti-rescue rules

Prohibited: horizon shopping; forecast-cadence shopping; metric/loss switching; baseline switching;
model switching; feature addition/removal after results; lookback-window search; threshold search;
block-boundary adjustment after results; post-hoc exclusion of adverse dates/blocks; reclassifying
invalid runs as fails or passes; treating secondary metrics as primary; subgroup or regime mining;
calendar/funding covariate insertion; signed-flow insertion; forced-flow / liquidation-proxy
insertion; hyperparameter search; ensembling; changing the target transform or RV estimator; using
terminal or sealed data to resolve ambiguity; using the consumed holdout as fresh confirmation; and
any immediate neighboring CF-1 variant after a valid fail. Every experiment parameter is frozen;
none is `TBD`.

## 32. Pass consequence

A valid pass establishes **only** that the admissible aggTrades substrate carries incremental
**development-level** information about future realized-volatility magnitude beyond the fixed
HAR-style baseline under the frozen contract. It does **not** establish direction, profitability,
ability to clear 16 bps, tradability, position sizing, trade gating, execution timing, strategy
readiness, paper/shadow/live readiness, or reserve-confirmed evidence. A pass permits **only** a
later, separately authorized **docs-only** assessment of whether the forecast could support a
bounded, non-directional market-state / volatility-regime filter. It does **not** reopen
`STOP_LONGHORIZON_ML_ARC`.

## 33. Fail consequence

A valid fail **materially closes or narrows** the admissible BTCUSDT aggTrades research lane on the
**magnitude axis** under this target / horizon / baseline / feature / evaluation design. It
authorizes **no** neighboring feature, horizon, loss, model, threshold, or split variant, and no
terminal or sealed evidence. Return to a paused posture unless a genuinely new family is separately
proposed. This is the high-negative-value outcome.

## 34. Invalid-run consequence

Make **no** scientific claim. Preserve all evidence classifications and locks. **Stop**, and require
a separate corrective phase and new operator authorization. An invalid run is never converted into a
pass or a fail.

## 35. Explicit non-directional / non-trading boundary

CF-1 is a **non-directional realized-variance magnitude** test. A `CF1_VALID_PASS` would establish no
directional edge, no profitability, no ability to clear the locked 8 bps/side · 16 bps round-trip
cost, and no permission to reopen the stopped long-horizon ML arc or any directional program. The
Phase 4bn-AE §19 absolute strategy/PnL/backtest/live boundary is unsoftened: any trading path would
require its own separate M0-style mechanism-admissibility clearance and its own separate
authorization. CF-1 maps onto M0 via the M0.3 "equivalent baseline differential for non-strategy
mechanism claims" route; this preregistration does not itself clear M0.

## 36. Terminal and sealed exclusion

The **v002 terminal window** (2024-12-01..2025-02-28) and the **v002 sealed test**
(2025-02-14..2025-02-28) remain `UNTOUCHED_RESERVED` and are **excluded** from the preregistered
development experiment. No terminal or sealed evidence is designated for this development run;
`test_rows_loaded = 0` is preserved. Any future confirmation against the terminal reserve would
require the full Phase 4bn-AV pre-spend sequence and separate operator authorization.

## 37. Consumed-holdout posture

The consumed pre-v002 internal holdout (2024-11-17..2024-11-30) remains `CONSUMED`, is **not**
reusable as independent confirmation, and is **not** designated as the CF-1 evaluation set. It may be
cited descriptively only. No new independent holdout was created by relabeling it. The CF-1
development verdict is a **development-evidence** verdict only.

## 38. Confirmation no data or reserve was opened

Confirmed. No market data, feature row, label row, normalized or raw row, model output, diagnostic
output, backtest output, v002 terminal window, v002 sealed test, or consumed holdout was opened,
read, listed for content, hashed, sampled, or scored by Phase 4bn-AY or by this merge. Nothing under
`data/microstructure/` or `data/research/` was opened. No evidence reserve was spent. No network,
endpoint, credential, WebSocket, MCP, Graphify, `.mcp.json`, or external reviewer was used.

## 39. Confirmation no executable surface changed

Confirmed. The merge adds documentation only. No source, test, script, config, schema, manifest,
gate report, sidecar, split file, ML config, or data artefact was created, modified, renamed, or
deleted.

## 40. Validation results

- `git fetch origin`; `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- Pre-merge `rev-parse` → `main == origin/main == 8b6c8614e37508cd05346f5ed90f8d08d9f68560`; local
  AY == origin AY == `0fb560656aa9b50cf110602e15be8222b7343623`.
- `git log --oneline 8b6c8614..AY` → the six commits in §6, in order.
- `git diff --check main..AY` → clean; `git diff --name-status main..AY` → exactly four `A` entries,
  no `M`/`D`/`R`; `git diff --stat` → 2,081 insertions.
- Contract consistency audit → target `(t, t+H]`; all RV intervals `(a, b]`; `P_at(u)` uses `≤ u`;
  HAR `(t−L, t]`; feature snapshot `≤ t`; covered minutes `(τ_{k-1}, τ_k]`; live predicate
  `τ_{k-1} < ts ≤ τ_k`; **zero** live occurrences of `τ_{k-1} ≤ ts < τ_k` in the contract, memo, or
  checklist; every `[a, b)` / `P_minus` / `P_start` / left-limit mention is a prohibition, an
  invalid-run condition, or a labeled superseded historical record; `2024-10-31T23:00` invalid; no
  November row opened.
- Statistical consistency audit → exact three-feature set; fixed HAR-style OLS baseline; fixed nested
  augmented OLS; QLIKE `1e-16` safeguard; zero-RV retention; equal-weighted seven-block `Δ_equal`;
  stratified-by-block bootstrap of the same estimand; 10,000 replicates; seed `20260715`; P2 = ≥ 6 of
  7; P3 = `LB_95 > 0`; no pooled origin-count weighting; no alternate decision metric.
- Post-merge → `git diff --check 8b6c8614..HEAD` clean; `git diff --name-status 8b6c8614..HEAD` →
  five added AY documents, no `M`/`D`/`R`; final `HEAD == main == origin/main`.
- **Not run** (docs-only; no executable surface changed and execution is outside merge scope):
  pytest, Ruff, mypy, any project script, builder, the deterministic timestamp-boundary proof, target
  or feature generation, model fitting, QLIKE computation, the bootstrap, diagnostics, backtests,
  replays, runtime processes, data workflows, and acquisition workflows.

## 41. Manifest, eligibility, M0, split, sidecar, storage, evidence-ledger, and stopped-arc preservation

Unchanged and preserved exactly: `STOP_LONGHORIZON_ML_ARC` and
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct; not merged, softened, reinterpreted, rescued,
reopened, or continued); the Phase 4bn-AX forced-flow rejection
`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`; the human operator as sole final authority;
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
`V002_SEALED_TEST = UNTOUCHED_RESERVED`; `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`;
`test_rows_loaded = 0`; `research_eligible = false`; `eligibility_gate_status = pending`; all
published authorization flags false; Phase 4aw `flip_research_eligible(...)` always-raising and never
invoked; the Phase 4bn-AE §19 absolute M0 boundary; the Phase 4ak twelve-clause M0 gate with §6
cooldown and §7 cooled-down families; M0 cooldown and cooled-down-family rules; the locked cost
8 bps/side · 16 bps round trip; all dataset identities and hashes; all split, holdout, sidecar,
storage, and evidence-ledger policies (Phase 4bn-Y / L / AA / 4bb-F / AV); every prior verdict and
retained-evidence classification; and every completed implementation report.
`docs/00-meta/current-project-state.md` is left unchanged by this merge, matching the AH..AX
docs-only precedent.

## 42. Exact post-merge result state

`CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_PREREGISTRATION_MERGED_TO_MAIN__TARGET_FEATURE_BASELINE_SPLIT_LOSS_AND_PASS_FAIL_CONTRACT_FROZEN__BOOTSTRAP_ESTIMAND_ZERO_RV_EXECUTION_BOUNDARY_AND_CAUSAL_COMPLETED_INTERVAL_SEMANTICS_CLARIFIED__NO_DATA_OPENED__NO_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

Exact statements:

`Phase 4bn-AY freezes the CF-1 development experiment contract but does not authorize that experiment to run.`

`The final live covered-minute predicate is τ_{k-1} < ts ≤ τ_k.`

`A CF1_VALID_PASS would not establish directional edge, profitability, ability to clear 16 bps, tradability, or permission to reopen the stopped long-horizon ML arc.`

`A CF1_VALID_FAIL closes or materially narrows the preregistered CF-1 magnitude lane under the frozen target, horizon, baseline, feature, and evaluation design and authorizes no neighboring rescue variant.`

`No target generation, feature generation, model fitting, QLIKE computation, bootstrap execution, diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write execution is authorized by the Phase 4bn-AY merge.`

`No market data, feature row, label row, model output, diagnostic output, or evidence reserve was opened or read by Phase 4bn-AY or by its merge.`

`The v002 terminal window and v002 sealed test remain untouched and excluded.`

`The consumed pre-v002 internal holdout is not reusable as independent confirmation and is not designated as the CF-1 evaluation set.`

`No evidence reserve is authorized for spending by the Phase 4bn-AY merge.`

`Phase 4bn-AZ or any other successor requires separate operator authorization and a new Claude Code prompt.`

## 43. Required post-merge operator posture

The project remains **paused with respect to execution**. The CF-1 development experiment contract is
frozen and merged, but is **not** authorized to run: no data may be opened, no target or feature
generated, no model fitted, no QLIKE or bootstrap computed, no diagnostic or backtest run, no
acquisition made, and no evidence reserve spent. The v002 terminal window and sealed test remain
untouched reserves; the consumed holdout remains descriptive-only. Recommended next operator action:
return this merge-closeout and the final operator report to ChatGPT for review before deciding
whether to authorize the CF-1 execution phase.

## 44. Phase 4bn-AZ non-authorization

`Phase 4bn-AZ or any other successor requires separate operator authorization and a new Claude Code
prompt.` The proposed successor title — `Phase 4bn-AZ — CF-1 Realized-Volatility Substrate-Test
Execution` — is **proposed only** and is **not** authorized by this merge, by Phase 4bn-AY, or by
Phase 4bn-AX. No successor execution, deterministic boundary proof, data read, acquisition, or
reserve spend is begun or authorized here.
