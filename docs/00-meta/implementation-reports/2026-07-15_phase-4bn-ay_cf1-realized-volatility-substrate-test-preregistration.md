# Phase 4bn-AY — CF-1 Realized-Volatility Magnitude-Forecasting Substrate-Test Preregistration (Main Memo)

## 1. Phase identity

Phase 4bn-AY — CF-1 Realized-Volatility Magnitude-Forecasting Substrate-Test Preregistration
(docs-only, low-researcher-freedom). This memo preregisters the **entire** CF-1 development
experiment before any market data is opened or any code, builder, model, diagnostic, or backtest is
run. Its implementation-grade companion
(`2026-07-15_phase-4bn-ay_cf1-target-feature-baseline-and-evaluation-contract.md`) freezes every
execution-bearing field; its execution-validation checklist
(`2026-07-15_phase-4bn-ay_cf1-execution-validation-checklist.md`) gates a later execution phase; its
closeout (`2026-07-15_phase-4bn-ay_closeout.md`) records branch/merge posture.

## 2. Branch

`phase-4bn-ay/cf1-realized-volatility-substrate-test-preregistration`.

## 3. Base SHA

`8b6c8614e37508cd05346f5ed90f8d08d9f68560` (`HEAD == main == origin/main` at branch time; the tip
after the Phase 4bn-AX merge-closeout SHA-finalization commit). Verified in sync before branching;
the only untracked item was the transient `.claude/scheduled_tasks.lock`, which was not staged,
modified, deleted, cleaned, or committed.

## 4. Phase type

Docs-only, **low-researcher-freedom preregistration** phase. It reads committed documentation,
committed source, committed tests, and Git metadata read-only, and creates exactly four new
documentation files. It is **not**: data execution; target generation; feature generation; model
fitting; hyperparameter tuning; diagnostic analysis; backtesting; PnL analysis; a reserve-spend
proposal; terminal-window use; sealed-test use; a strategy authorization; a market-state-filter
implementation; or a paper/shadow/live/exchange-write phase. It authorizes nothing beyond the
creation of documentation, and does **not** authorize the experiment it preregisters to run.

## 5. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — it governs the
scientific design of the one currently-selected research arc, so it is treated at the highest
ceremony tier even though it mutates no eligibility, manifest, verdict, reserve, or lock and freezes
a contract only.

## 6. Exact authorization boundary

**Authorized:** read committed docs / source / tests / Git metadata; author exactly four new files
(this memo, the contract, the checklist, a closeout); commit and push the dedicated phase branch.
**Not authorized:** to open, read, inspect, list-for-content, hash, sample, load, score, or
summarize any market-data / feature / label / normalized / raw row, the v002 terminal window, the
v002 sealed test, the consumed pre-v002 holdout for new analysis, anything under
`data/microstructure/` or `data/research/`, or any generated research/model/diagnostic/backtest
output; to run pytest / Ruff / mypy / any project script / builder / target or label generation /
feature pipeline / diagnostic / model / hyperparameter search / backtest / replay / runtime /
acquisition workflow; to use network / web search / any API / Binance endpoints / credentials /
WebSockets / exchange-write functions / MCP / Graphify / `.mcp.json` / Fable or any external
reviewer; to modify any existing file; to spend any evidence reserve; or to authorize any successor
phase. This phase used committed repository evidence only.

## 7. Areas inspected

Committed, read-only (README and `docs/00-meta/current-project-state.md` treated as potentially
stale and navigational only; recent implementation reports, merge-closeouts, source, and tests
outrank stale summaries):

- **AX selection lineage:** the Phase 4bn-AX main decision memo, forced-flow overlap/M0 audit, and
  closeout (CF-1 selected only as a substrate test; forced-flow rejected).
- **AW screening:** the Phase 4bn-AW candidate-family screening (CF-1 mechanism/prediction/
  falsification/negative-result value; M0.3 mapping).
- **Stopped-arc lineage:** Phase 4bn-AK ML arc-decision; Phase 4bn-AS (`STOP_LONGHORIZON_ML_ARC`);
  Phase 4bn-AT (`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`); the AJ 15s result (2.47% clear 16 bps)
  and the AR long-horizon inversion as restated through AK/AS.
- **Governance:** the Phase 4ak twelve-clause M0 gate (M0.3 non-strategy differential; §6 cooldown;
  §7.A/§7.C/§7.D/§7.E); the Phase 4bn-AE §19 absolute strategy/PnL/backtest/live boundary; the Phase
  4bn-AV evidence ledger and spending-authority standard.
- **Contract precedents:** Phase 4bn-AP long-horizon baseline preregistration; Phase 4bn-AM
  long-horizon label contract (alignment keys, timestamp discipline, censoring, split/embargo).
- **Split / storage / provenance:** Phase 4bn-Y split/holdout policy and the committed
  `pre_v002_split_policy.py` / `diagnostics_split_policy_v002.py` constants; Phase 4bn-L storage/
  budget; Phase 4bb-F sidecar policy; `docs/04-data/timestamp-policy.md`.
- **Committed source / schema (capability confirmation only; none modified):**
  `features_schema.py` / `features_schema_v002.py` (the 45-column feature contract, windows,
  forbidden substrings, causal window rule), `labels_compute_v002.py` /
  `longhorizon_labels_schema_v001.py` (forward-return formula, horizons, alignment),
  `pre_v002_split_policy.py` (exact split dates and boundary constants).

## 8. Confirmation no data or reserve was opened

Confirmed. No feature/label/normalized/raw row, no v002 terminal window, no v002 sealed test, no
generated local research/model/diagnostic/backtest artefact, and nothing under
`data/microstructure/` or `data/research/` was opened, read, listed for content, hashed, sampled, or
scored. The Phase 4bn-AV evidence ledger is preserved exactly:
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED` (descriptive-only), `V002_TERMINAL_WINDOW =
UNTOUCHED_RESERVED`, `V002_SEALED_TEST = UNTOUCHED_RESERVED`,
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`, `test_rows_loaded = 0`. No evidence
reserve was spent. No network, endpoint, credential, or external reviewer was used.

## 9. AX selection and CF-1 boundary

Phase 4bn-AX selected exactly `SELECT_CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_FOR_LATER_
PREREGISTRATION`. CF-1 was selected **only** as a realized-volatility magnitude-forecasting
substrate test — **not** as a trading strategy, a directional hypothesis, a profitability claim, a
data-execution authorization, or a reserve-spend authorization. The trading claim remains explicitly
false: a positive CF-1 result would **not** establish price direction, profitability, ability to
clear the locked 16 bps round-trip, or permission to reopen the stopped directional ML arc. This
preregistration operationalizes that selection at the design level only and preserves every stop and
lock.

## 10. Scientific hypothesis

Can predeclared, **non-directional** aggTrades microstructure variables improve future
realized-volatility **magnitude** forecasts beyond a simple, predeclared realized-volatility
persistence / HAR-style baseline? Concretely: three fixed, sign-invariant aggTrades microstructure
features (trade-arrival intensity `rolling_aggtrade_count_60s`, unsigned traded-volume intensity
`rolling_quantity_sum_60s`, mean trade size `rolling_quantity_mean_60s`), snapshotted causally at
each hourly forecast origin, improve out-of-sample forecasts of the next hour's realized variance of
BTCUSDT last-trade log price versus a fixed HAR-style realized-variance baseline, measured by lower
QLIKE, block-consistently across the chronological development evaluation blocks.

## 11. Null hypothesis

`H0`: the augmented model does **not** achieve strictly positive, block-consistent,
uncertainty-supported QLIKE improvement over the HAR-style baseline — i.e. the three sign-invariant
microstructure features carry **no** incremental out-of-sample realized-variance information beyond
the RV-based baseline. Formally, `E[ L_base(t) − L_aug(t) ] ≤ 0`.

## 12. Alternative hypothesis

`H1`: the augmented model achieves strictly lower QLIKE than the baseline, in a supermajority
(≥ 6/7) of chronological blocks, with the one-sided 95% **stratified-by-block** moving-block-bootstrap
lower bound of the **equal-weighted seven-block** QLIKE loss-differential estimand `Δ_equal` (`LB_95`)
`> 0`. Formally, `E[ d_{i,t} ] > 0` (where `d_{i,t} = QLIKE_base(i,t) − QLIKE_aug(i,t)`) with the
frozen block-consistency and uncertainty criteria met.

## 13. Mechanism

Realized variance exhibits **clustering and long memory** (the ARCH/HAR stylized fact); a
heterogeneous cascade of past realized variance (hour / day / week) captures most of that
persistence. The CF-1 claim is that **order-flow intensity and traded-volume/size** in the
seconds preceding a forecast origin carry **incremental information-arrival** signal about
near-future realized variance beyond past RV alone. This is a **magnitude / variance** mechanism,
orthogonal to price direction: a realized-variance forecast contains no sign and yields no
directional decision. The mechanism is non-directional by construction and uses only sign-invariant
inputs.

## 14. Target summary

Future **realized variance** of the BTCUSDT last-trade log price over a 1-hour forecast window,
computed as the sum of 60 squared 1-minute log returns on a fixed UTC clock grid (causal LOCF grid
prices), modelled in log space (`y = ln(RV + ε)`, `ε = 1e-16`) and mapped back to a positive
variance forecast by exponentiation. The QLIKE loss uses the actual variance `v = RV + ε` and floors
each forecast at `ε` (`h = max(exp(ŷ), ε)`) with the same `ε = 1e-16`, so the loss stays finite even
when `RV = 0` and no zero-RV observation is dropped (contract §3, §26). No direction, sign,
return-classification, continuation, reversion, or liquidation target. Full formula and validity
rules: contract §3, §7–§10. The project has **no** prior committed realized-variance definition;
CF-1's is authored fresh and duplicates nothing.

## 15. Exact selected horizon

**H = 60 minutes (3,600,000 ms). Exactly one horizon.** Supported by the committed `1h` forward
window semantics; no sensitivity horizon; no executable-horizon menu. Alternatives 5m / 15m / 30m /
daily were considered and rejected (contract §4): shorter horizons give too few / too noisy
intra-window returns for a stable RV proxy; daily gives far too few block-level observations. The
horizon is fixed here, before any data is opened, and may never be changed after seeing data.

## 16. Exact forecast cadence

One forecast origin at the **top of each UTC hour** (`HH:00:00.000`), **non-overlapping** windows
`[HH:00, HH+1:00)`. The target series carries no construction-induced overlap dependence.

## 17. Baseline summary

Exactly one **HAR-style realized-variance baseline** (heterogeneous autoregressive cascade at the
hour / day / week timescales available in the 244-date primary execution-access window), estimated by
**OLS in log-variance space** on three strictly-past-only realized-variance lookbacks (`RV_h` =
previous 1h; `RV_d` = mean of previous 24 hourly RVs; `RV_w` = mean of previous 168 hourly RVs), with
an intercept; forecasts exponentiated to guarantee positive variance. No baseline shopping; no
alternate baseline promoted after execution; no tuning. Full spec: contract §17.

## 18. Augmented-model summary

A **nested, low-complexity** OLS extension of the baseline that adds **only** the three §10
sign-invariant microstructure features (log-transformed, train-only standardized), with identical
target, training window, estimator, forecast origins, and preprocessing scope. The baseline is
exactly the augmented model with the three microstructure coefficients set to zero, so the
comparison isolates **incremental microstructure information**, not model-class superiority. No
trees, neural nets, ensembles, ML searches, regularization searches, feature selection, or
hyperparameter sweeps. Full spec: contract §18–§19.

## 19. Feature-family summary

**Exactly three** committed, sign-invariant feature columns at the **60s** window, snapshotted
causally at the origin: `rolling_aggtrade_count_60s` (trade-arrival intensity),
`rolling_quantity_sum_60s` (unsigned traded-volume intensity), `rolling_quantity_mean_60s` (mean
trade size). All are magnitude/count quantities with no directional content. **No sign-invariant
dispersion/standard-deviation feature is used because none exists in the committed 45-column
schema** — and, per the Phase 4bn-AY mandate, none is invented here; the smaller three-feature
contract supported by existing columns is used instead. Excluded as directional: aggressive
flow-ratio, aggressive quantity-imbalance, aggressive buy/sell quantities and counts, and signed
past returns. Full contract: contract §11–§16.

## 20. Development-evidence boundary

Two boundaries are distinguished (contract §21). **(a) Committed non-reserve eligibility envelope** =
pre-v002 train ∪ validation = **259 admissible UTC dates: 2024-03-01 .. 2024-09-30 (214) + 2024-10-02
.. 2024-11-15 (45)** (committed `pre_v002_split_policy.py`). **(b) Frozen CF-1 primary
execution-access boundary** (what the primary experiment may open and use) = **2024-03-01 through
2024-10-31 UTC, excluding 2024-10-01 = 244 dates**. **`2024-11-01 through 2024-11-15 =
UNUSED_NON_RESERVE_BUFFER`** — non-reserve-eligible but **unopened and unused** (not training, not
evaluation, not bootstrap, not confirmation, not preprocessing, not diagnostics). Excluded: the
embargo dates 2024-10-01 and 2024-11-16; the **consumed** pre-v002 internal holdout 2024-11-17 ..
2024-11-30 (never a CF-1 evaluation/confirmation set; descriptive-only); the **v002 terminal window**
2024-12-01 .. 2025-02-28 (`UNTOUCHED_RESERVED`); the **v002 sealed test** 2025-02-14 .. 2025-02-28
(`UNTOUCHED_RESERVED`, highest protection). `test_rows_loaded = 0` is preserved. The CF-1 development
verdict is a **development-evidence** verdict only; genuine independent confirmation would require the
untouched terminal reserve under a separate authorized spend, which this phase does **not** authorize.

## 21. Split / evaluation summary

Chronological, **expanding-window walk-forward** over **7 contiguous, non-overlapping full UTC
calendar-month evaluation blocks**: April–October 2024 (B7 = October starting 2024-10-02 to respect
the committed 2024-10-01 embargo date). March 2024 is train-only warmup; **2024-11-01..2024-11-15 is
the `UNUSED_NON_RESERVE_BUFFER` (never opened)** and 2024-11-16 is a committed embargo exclusion — no
evaluation block, training set, or bootstrap uses any date on or after 2024-11-01. Each block is
evaluated with a model trained on all in-access development origins strictly before it, minus a 1-day
embargo. No random split, no shuffled CV, no resampling across time. Full spec: contract §21–§25.

## 22. Primary loss

**QLIKE** (quasi-likelihood), `QLIKE(t) = v/h − ln(v/h) − 1` with the fixed zero-RV safeguard
`v = RV + ε` and `h = max(exp(ŷ), ε)`, `ε = 1e-16` (so the loss is always finite and no zero-RV
observation is dropped); lower better; block-mean then equal-weighted across the 7 blocks (the
`Δ_equal` estimand). It is robust to a noisy volatility proxy and to the heavy right tail / scale
variation of realized variance (Patton 2011), and is a proper score for variance forecasts —
matching the magnitude question. It is the sole primary loss; secondary metrics cannot rescue a
primary failure. Fable's illustrative 3–5% QLIKE margin is **not** adopted. Full spec:
contract §26–§28.

## 23. Secondary descriptive metrics

Exactly two, descriptive and **non-authorizing**:
1. **MSE on realized variance** — the other Patton-robust loss, reported as a cross-check.
2. **Mincer–Zarnowitz R²** of realized log-variance on forecast log-variance — forecast
   informativeness.
Neither can rescue a QLIKE primary failure, upgrade a fail to a pass, or serve as the decision
statistic.

## 24. Pass rule

`CF1_VALID_PASS` iff **all** hold simultaneously (contract §31): **(P1)** `Δ_equal > 0` — strict
positive equal-weighted seven-block-mean QLIKE improvement (`Δ_equal = (1/7) Σ_i D_i`, zero-floor per
§28); **(P2)** block consistency — augmented strictly better (`D_i > 0`) in **≥ 6 of 7** blocks;
**(P3)** uncertainty — the one-sided 95% **stratified-by-block** moving-block-bootstrap lower bound of
the **same** `Δ_equal` estimand (`LB_95`) `> 0`; **(P4)** run validity — no `CF1_INVALID_RUN`
condition, no contaminated block, no unauthorized switching, all 7 blocks valid (each ≥ 100 valid
paired origins). P2 and P3 are independent and neither replaces the other.

## 25. Fail rule

`CF1_VALID_FAIL`: every scientifically valid run (P4 holds) that does **not** satisfy all of
P1–P3 — e.g. `Δ_equal ≤ 0`, or fewer than 6/7 blocks with `D_i > 0`, or `LB_95 ≤ 0`. There is **no**
borderline / promising / weak / partial pass, **no** pass on a secondary metric, and **no** pass on
a post-hoc subset.

## 26. Invalid-run rule

`CF1_INVALID_RUN`: any target-contract violation; feature-contract violation; split leakage; reserve
access (terminal / sealed / consumed-holdout-as-confirmation); preprocessing leakage; timestamp
misalignment; missing required block or a block with `< 100` valid origins; material implementation
mismatch; numerical failure (singular matrix, zero-variance regressor, condition number `> 1e10`,
non-finite loss/coefficient, `< 70` training origins) preventing the preregistered comparison; or
any unauthorized change of model / metric / horizon / cadence / threshold / feature / window / loss.
An invalid run is **not** interpretable scientifically (neither pass nor fail) and requires a
separate corrective phase and a new operator authorization.

## 27. Uncertainty method

**Stratified-by-evaluation-block moving-block bootstrap** (contract §29) that estimates uncertainty
for the **same** equal-weighted seven-block `Δ_equal` estimand as the primary point estimate —
compatible with serially-dependent chronological forecast errors. Within each block `i`, preserve
chronological order, use a **block-specific** length `ℓ_i = ceil(n_i^(1/3))`, and resample moving
blocks **within that block only** to `n_i` observations; per replicate compute `D_i^(b)` then
`Δ_equal^(b) = (1/7) Σ_i D_i^(b)`; `B = 10,000` replicates, `RNG_SEED = 20260715`; `LB_95 =
quantile({Δ_equal^(b)}, 0.05)`; **P3 passes iff `LB_95 > 0`**. No pooling of origins across blocks, no
origin-count weighting, no resampling across block boundaries. Exactly one uncertainty test; no IID
assumption; no multiple-testing selection; no alternate bootstrap / analytical SE / IID test /
Diebold–Mariano variant may replace it after execution (a DM/Newey–West figure may be reported
descriptively only). The uncertainty criterion supports but does **not** replace block consistency,
and block consistency does **not** replace it.

## 28. Block-consistency rule

Augmented strictly lower block-mean QLIKE than baseline (`D_i > 0`) in **≥ 6 of the 7** evaluation
blocks; all 7 block differentials `D_i` recorded. Required and independent; not replaceable by the
stratified moving-block bootstrap (§27), and the bootstrap is not replaceable by it.

## 29. Anti-tuning and anti-switching rules

Prohibited (any occurrence ⇒ `CF1_INVALID_RUN`): horizon shopping; forecast-cadence shopping;
loss-function switching; baseline switching; model switching; feature addition/removal after
results; lookback-window search; threshold search; block-boundary adjustment after results;
post-hoc exclusion of adverse dates/blocks; reclassifying invalid runs as fails/passes; treating
secondary metrics as primary; subgroup or regime mining; calendar/funding covariate insertion;
signed-flow insertion; forced-flow / liquidation-proxy insertion; hyperparameter search; ensembling;
changing the target transform; changing the realized-volatility estimator; using terminal or sealed
data to resolve ambiguity; using the consumed holdout as fresh confirmation. Every experiment
parameter is frozen in the contract; none is `TBD`.

## 30. Anti-rescue rule

A `CF1_VALID_FAIL` **closes** the preregistered CF-1 development family under this target, horizon,
baseline, feature contract, and evaluation design. It does **not** authorize immediate neighboring
variants. Any later materially-different CF-1 variant requires a **new mechanism justification**, a
**new docs-only phase**, an explicit **anti-duplication audit**, and **operator authorization**. A
`CF1_VALID_PASS` does **not** reopen `STOP_LONGHORIZON_ML_ARC` or `STOP_TOB_MECHANISM_ARC_DATA_
INADMISSIBLE`, and does not soften, merge, or reinterpret either. This reinforces M0.10 / M0.12, the
Phase 4bn-AS §21/§24 anti-rescue, and Phase 4bn-AV §16.

## 31. Pass consequence

On `CF1_VALID_PASS`: record that the admissible aggTrades substrate is **scientifically informative
on the magnitude axis** under the frozen contract. Authorize **nothing automatically**; permit
**only** a separately-authorized docs-only decision phase assessing whether the forecast could
support a **bounded, non-directional market-state / volatility-regime filter**. Do **not** infer
direction, infer profitability, claim ability to clear 16 bps, or authorize position sizing, trade
gating, execution timing, PnL analysis, paper/shadow/live trading, terminal evidence, or sealed
evidence. Do **not** reopen `STOP_LONGHORIZON_ML_ARC`. A development-level pass is **not** reserve-
confirmed evidence.

## 32. Fail consequence

On `CF1_VALID_FAIL`: **materially close or narrow** the admissible BTCUSDT aggTrades research lane on
the **magnitude axis**; record that the substrate has not shown incremental realized-volatility
predictability beyond the preregistered price-based baseline under the frozen contract. Do **not**
authorize neighboring feature / horizon / loss / baseline / model variants; do **not** authorize
terminal or sealed evidence; return to a paused posture unless a genuinely new family is separately
proposed. This is the high-negative-value outcome: combined with the stopped directional arc, it
lets the project retire the trade-tape substrate on the magnitude axis at near-zero reserve cost.

## 33. Invalid-run consequence

On `CF1_INVALID_RUN`: make **no** scientific claim; preserve all evidence classifications and locks;
**stop**; require a separate corrective phase and a new operator authorization. An invalid run is
never converted into a pass or a fail.

## 34. Explicit non-directional / non-trading boundary

CF-1 is a **non-directional realized-variance magnitude** test. A `CF1_VALID_PASS` would establish
**no** directional edge, **no** profitability, **no** ability to clear the locked 8 bps/side · 16
bps round-trip cost, and **no** permission to reopen the stopped long-horizon ML arc or any
directional program. The Phase 4bn-AE §19 absolute strategy/PnL/backtest/live boundary is unsoftened:
any trading path would require its own separate M0-style mechanism-admissibility clearance (M0.5
cost realism, execution feasibility, slippage/spread — which aggTrades-only data cannot support) and
its own separate authorization. CF-1 selection and any CF-1 result leave that boundary exactly where
it is. (M0 mapping: CF-1 uses the M0.3 "equivalent baseline differential for non-strategy mechanism
claims" route — predicted incremental QLIKE skill over HAR-RV, not a Δ_R; it escapes the §7.A
price-only directional depletion by being non-directional; and it addresses the §7.D microstructure
caution because its data is already on disk (M0.8 PASS) and its object is magnitude, not
short-horizon direction. This preregistration does **not** itself clear M0; M0 clearance for any
execution remains a separate operator-authorized step.)

## 35. Terminal and sealed reserve exclusion

The v002 terminal window (2024-12-01 .. 2025-02-28) and the v002 sealed test (2025-02-14 ..
2025-02-28) remain `UNTOUCHED_RESERVED` and are **excluded** from the preregistered development
experiment. No terminal or sealed evidence is designated for this development run; no reserve spend
is authorized; `test_rows_loaded = 0` is preserved. Any future confirmation against the terminal
reserve would require the full Phase 4bn-AV pre-spend sequence and a separate operator authorization.

## 36. Consumed-holdout treatment

The consumed pre-v002 internal holdout (2024-11-17 .. 2024-11-30) is **not reusable as independent
confirmation** and is **not** designated as the CF-1 evaluation set. It may be cited **descriptively
only**. No new independent holdout is created by relabeling it. The CF-1 development evaluation uses
the pre-v002 train ∪ validation window only.

## 37. Exact execution preconditions

Before any later CF-1 execution phase may run (all enforced by the execution-validation checklist):
(a) a separate explicit **operator authorization** and a new Claude Code prompt; (b) the execution
phase pinned to this preregistration commit SHA with **no** modification of any of the four Phase
4bn-AY files; (c) base state `HEAD == main == origin/main` with only the transient lock untracked;
(d) acceptance of CF-1's M0 mapping (§34) or a separate M0-style clearance memo; (e) storage
preflight (`D:` free ≥ 500 GiB; Phase 4bn-L caps); (f) reserves untouched (`v002_terminal_window_read
= false`, `sealed_test_split_touched = false`, `test_rows_loaded = 0`); (g) all non-authorization
flags `false`; (h) the leakage/split/coverage proof validated **before** any metric is computed.
Absent any precondition, execution does not begin.

## 38. Proposed later execution phase title (explicitly not authorized)

`Phase 4bn-AZ — CF-1 Realized-Volatility Substrate-Test Execution (data-reading target/feature build
+ fixed baseline-vs-augmented QLIKE evaluation under the Phase 4bn-AY frozen contract)`. **Proposed
only.** It is not authorized by this phase, by AX, by AW, or by the operator's authorization of Phase
4bn-AY. It requires separate operator authorization and a new Claude Code prompt before any work
begins.

## 39. Recommended next operator action

Return the four Phase 4bn-AY files and the final operator report to ChatGPT for compliance review and
a separate merge decision. Do **not** run Fable; do **not** merge from inside this phase; do **not**
begin Phase 4bn-AZ, generate targets/features, fit a model, run diagnostics/backtests, read data, or
propose/authorize acquisition or a reserve spend. If, after review, the operator wishes to proceed,
the next possible step is to separately authorize the docs-only-preregistered Phase 4bn-AZ execution
(§38) via a new Claude Code prompt — but the project otherwise remains paused, and remaining paused
is a valid operator choice.

## 40. Exact final result state

`CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_PREREGISTERED__TARGET_FEATURE_BASELINE_SPLIT_LOSS_AND_PASS_FAIL_CONTRACT_FROZEN__NO_DATA_OPENED__NO_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

Exact statements:

`No market data, feature row, label row, model output, diagnostic output, or evidence reserve was opened or read by Phase 4bn-AY.`

`No target generation, feature generation, model fitting, diagnostic, backtest, PnL analysis, data acquisition, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-AY.`

`The Phase 4bn-AY preregistration freezes the CF-1 development experiment contract but does not authorize that experiment to run.`

`The v002 terminal window and v002 sealed test remain untouched and are excluded from the preregistered development experiment.`

`The consumed pre-v002 internal holdout is not reusable as independent confirmation and is not designated as the CF-1 evaluation set.`

`A CF1_VALID_PASS would not establish directional edge, profitability, ability to clear 16 bps, or permission to reopen the stopped long-horizon ML arc.`

`Phase 4bn-AZ or any other successor requires separate operator authorization and a new Claude Code prompt.`

## 41. Preserved project locks

Unchanged and preserved exactly: `STOP_LONGHORIZON_ML_ARC` and `STOP_TOB_MECHANISM_ARC_DATA_
INADMISSIBLE` (distinct; not merged, softened, reinterpreted, rescued, reopened, or continued); the
Phase 4bn-AX forced-flow rejection `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`; the human
operator as sole final authority; Phase 4aw `flip_research_eligible(...)` always-raising, never
invoked; `research_eligible = false`; `eligibility_gate_status = pending`; all published
authorization flags false; the Phase 4bn-AE §19 M0 boundary; the Phase 4ak twelve-clause M0 gate with
§6 cooldown and §7 cooled-down families; M0 cooldown and cooled-down-family rules; the locked 8
bps/side · 16 bps round-trip cost; all dataset identities and hashes; split, holdout, sidecar, and
storage policies (Phase 4bn-Y / L / AA / 4bb-F); every prior verdict and retained-evidence
classification; the Phase 4bn-AV evidence ledger, spending-authority standard, and late-
inadmissibility protocol. `docs/00-meta/current-project-state.md` is left unchanged by this phase
(matching the AH..AX docs-only precedent; any additive paragraph would be a separate merge-time
decision).
