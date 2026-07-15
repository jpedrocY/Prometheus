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

Future **realized variance** of BTCUSDT last-trade log price over a 1-hour forecast window: 1-minute
UTC-clock grid, causal LOCF grid prices, `RV(t) = Σ_{k=1}^{60} r_k²`, modelled as `y = ln(RV + ε)`
with `ε = 1e-16`, forecast mapped back to variance by exponentiation. Non-directional; no prior
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

Pre-v002 train ∪ validation = 2024-03-01..2024-09-30 (214) + 2024-10-02..2024-11-15 (45) = 259
admissible UTC dates. Excluded: embargo dates 2024-10-01 / 2024-11-16; consumed holdout
2024-11-17..2024-11-30 (descriptive-only, not a confirmation set); v002 terminal 2024-12-01..
2025-02-28; v002 sealed 2025-02-14..2025-02-28. `test_rows_loaded = 0` preserved.

## 15. Exact evaluation design

Chronological expanding-window walk-forward over 7 non-overlapping full-month evaluation blocks
Apr–Oct 2024 (B7 = 2024-10-02..2024-10-31); March = warmup; Nov 1–16 = buffer. Purge = 1h horizon;
embargo = 1 calendar day; preprocessing fit train-only; no random/shuffled split.

## 16. Primary loss

**QLIKE** (`σ²/ĥ − ln(σ²/ĥ) − 1`), lower better, block-mean then equal-weighted across 7 blocks.
Secondary descriptive metrics (≤2, non-authorizing): MSE-on-variance; Mincer–Zarnowitz R².

## 17. Pass rule

`CF1_VALID_PASS` iff all of: (P1) `ΔQLIKE_blockmean > 0`; (P2) augmented strictly better in ≥ 6/7
blocks; (P3) moving-block bootstrap one-sided 95% lower bound of pooled loss differential > 0; (P4)
run validity (no invalid-run condition; all 7 blocks ≥ 100 valid origins). Zero-floor materiality.

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

## 25. Commit SHA self-reference convention

The Phase 4bn-AY phase commit adds exactly the four files in §6 with message
`docs(phase-4bn-ay): preregister CF-1 volatility substrate test`. Its exact SHA cannot be embedded
inside itself; it is recorded in the final operator report and the Git log after commit. No
merge-closeout is created and no SHA-finalization commit is performed by this phase (merge is a
separate, operator-authorized step).

## 26. Local / origin branch equality placeholders

After push, `git rev-parse HEAD` == `git rev-parse phase-4bn-ay/…` ==
`git rev-parse origin/phase-4bn-ay/…` (the phase-branch SHA `<PHASE_COMMIT_SHA>`); recorded exactly in
the final operator report. `main` and `origin/main` remain at
`8b6c8614e37508cd05346f5ed90f8d08d9f68560` (untouched; no merge, no main push).

## 27. Exact final result state

`CF1_REALIZED_VOLATILITY_SUBSTRATE_TEST_PREREGISTERED__TARGET_FEATURE_BASELINE_SPLIT_LOSS_AND_PASS_FAIL_CONTRACT_FROZEN__NO_DATA_OPENED__NO_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

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
