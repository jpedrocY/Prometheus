# Phase 4bn-Z — ML-Baseline Readiness Memo

## 1. Purpose

This is a **docs-only** ML-baseline readiness memo for the conservative
pre-v002-only research path defined by the Phase 4bn-Y chronological split /
holdout policy. It answers one question:

> Is the project ready to implement a pre-v002 ML-baseline path now, and if
> not, what exact prerequisites remain before any ML dataset builder, research
> matrix, model training, scoring, prediction, diagnostics, strategy, PnL, or
> backtest may be authorized?

The memo **settles readiness and records prerequisites**. It authorizes none of
the downstream actions it discusses. It implements nothing in code, reads no
local data, creates no artefact, flips no eligibility flag, and authorizes no
successor. Its conclusions are determined from committed documentation and
committed source read read-only; the figures it carries forward come from the
predecessor implementation reports already merged to `main`.

---

## 2. Authority and repository state

- **Phase:** 4bn-Z — ML-Baseline Readiness Memo.
- **Authorization:** separately authorized by the operator following the Phase
  4bn-Y decision `RECOMMEND_AUTHORIZE_ML_BASELINE_READINESS_MEMO`.
- **Branch:** `phase-4bn-z/ml-baseline-readiness-memo`.
- **Base `main` SHA:** `896f5fa1aaccaa4ed8504e5d815929eeb50ca398`
  (`docs(phase-4bn-y): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 896f5fa1…` verified.
- **Predecessors present on `main`:** Phase 4bn-Y SHA-finalization `896f5fa`,
  merge-closeout `e55e5a8`, merge `69005a4`, branch `f4d4b5d`; Phase 4bn-X
  finalization `5d69e67` present as predecessor.
- **Remote:** `https://github.com/jpedrocY/Prometheus.git`.
- **Gitignored data namespaces:** `data/microstructure/` (`.gitignore:85`) and
  `data/research/` (`.gitignore:88`) — both confirmed; both remain uncommitted.

This phase is branch-complete only by its own work; it is **not merged into
`main`** and is **not project-complete**. It becomes project-complete only when
a separately authorized merge phase records its merge-closeout on `main`.

---

## 3. Phase type and strict scope

**Phase type:** docs-only / ML-readiness / dataset-contract /
split-implementation-precondition / source-admissibility / leakage-control memo.

**Tier:** Tier 1 — Full Phase per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3, because the phase
determines whether the locally produced and gated pre-v002 raw → normalized →
feature → label stack, plus the Phase 4bn-Y split policy, is ready for a future
ML-baseline implementation path, and settles what remains required before any ML
dataset builder, research matrix, model training, scoring, diagnostics,
strategy, PnL, backtest, or downstream use may be authorized.

**Strictly out of scope (this phase does none of these):** implement the split
policy in code; create an ML dataset builder; create a research matrix; create a
model, scores, or predictions; run diagnostics; run strategy / signals / PnL /
backtests; add code, tests, or scripts; create any local artefact; read any
local data; flip any eligibility flag; transition `eligibility_gate_status`; set
`chronological_split_policy` in any manifest; or authorize any successor.

---

## 4. Evidence base and input boundary

**Admissible evidence (read-only) used for this memo:**

- Committed process standards (`merge-closeout-standard`,
  `phase-risk-tiering-standard`, `phase-workflow-standard`,
  `phase-prompt-template`, `operator-report-standard`) and
  `current-project-state.md`.
- Committed Phase 4bn-O … 4bn-Y implementation reports, merge-closeouts, and
  closeouts (the source of every figure carried forward in §5 – §6).
- Committed data / architecture docs (`data-requirements`,
  `historical-data-spec`, `timestamp-policy`, `dataset-versioning`,
  `database-design`).
- Committed source, read-only, for readiness grounding:
  `diagnostics_split_policy_v002.py`, `ml_baseline_design_v002.py`,
  `ml_baseline_dataset_v002.py`, `labels_schema_v002.py`,
  `labels_compute_v002.py`, `labels_validation.py`, `features_schema_v002.py`,
  `scripts/phase4bn_x_validate_label_pre_v002_gate.py`,
  `scripts/phase4bn_w_compute_pre_v002_labels.py`, and the committed test tree.

**Input boundary (not read):** no local Parquet (raw / normalized / feature /
label); no local raw zip; no local manifest or gate report under
`data/microstructure/`; no v002 terminal raw / normalized / feature / label
window; no sealed-test file; no `data/research/` output. `README` is treated as
potentially stale and is **not** used as a current-state authority.

The two committed ML-baseline source files named in the authorization
(`ml_baseline_splits.py`, `ml_baseline_train.py`) **do not exist** in the
repository; this absence is itself evidence (see §8).

---

## 5. Phase 4bn-Y split policy carried forward

The Phase 4bn-Y memo recorded, for the first conservative pre-v002-only path,
**Candidate A** — working name
`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` (not implemented in
code):

- **Train:** 2024-03-01 .. 2024-09-30 — 214 UTC dates.
- **Embargo date (dropped):** 2024-10-01.
- **Validation:** 2024-10-02 .. 2024-11-15 — 45 UTC dates.
- **Embargo date (dropped):** 2024-11-16.
- **Internal holdout / dry-run (NOT the sealed test):** 2024-11-17 .. 2024-11-30
  — 14 UTC dates.
- **Total:** 214 + 1 + 45 + 1 + 14 = **275** = full gated pre-v002 segment.
- **Assignment:** by `source_transact_time_ms` UTC date; chronological-only; no
  shuffle / random / k-fold-over-time / bootstrap.
- **Embargo:** 1 full UTC date dropped at each internal boundary (operational
  rule), over a formal ≥ 60 s row-level earlier-split floor (subsumes the locked
  v002 `MIN_BOUNDARY_EMBARGO_SECONDS = 60`; 86,400 s ≫ 60 s).
- **v002 terminal (2024-12-01 .. 2025-02-28):** by reference only / unread;
  governed by the recorded v002
  `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`; inadmissible to the first
  ML-baseline path.
- **Published v002 labels:** by reference only; byte-for-byte immutable; unread.
- **Sealed test (2025-02-14 .. 2025-02-28):** fully sealed; `test_rows_loaded=0`;
  untouched; single-use, future-authorization only; the pre-v002 internal
  holdout is **not** the sealed test.
- **Result state:** `RECORD_CHRONOLOGICAL_SPLIT_POLICY__REMAIN_PAUSED`;
  **decision:** `RECOMMEND_AUTHORIZE_ML_BASELINE_READINESS_MEMO`.

This memo treats Candidate A as the **policy contract** for the first path and
does not alter it.

---

## 6. Local gated pre-v002 stack carried forward

All figures below are quoted from the merged Phase 4bn-O … 4bn-X reports; no
local artefact was read to obtain them.

| Layer | Phase | Files | Rows | Footprint (B) | Manifest / config SHA | Gate verdict |
|---|---|---|---|---|---|---|
| Normalized | 4bn-O / 4bn-P | 275 | 400,001,695 | 3,954,532,918 | manifest `0e96ae37…d9fa` | `NORMALIZED_LAYER_GATE_PASSED…` 25/25; report `3452fd9d…f134` |
| Feature | 4bn-S / 4bn-T | 275 | 400,001,695 | 54,254,406,538 | manifest `4881eb87…9b52`; `feature_config_hash 0726b41d…114c` | `FEATURE_LAYER_GATE_PASSED…` 27/27; report `db731d1b…6ab08` |
| Label | 4bn-W / 4bn-X | 275 (+275 sidecars) | 400,001,695 | 15,654,082,679 | manifest `69746c88…b161`; `label_config_hash b3bd5d2b…8970` | `LABEL_LAYER_GATE_PASSED…` 40/40; report `ffb5b09…8984` |

Segment span: **2024-03-01 .. 2024-11-30 inclusive UTC (275 dates)**.
Label envelope terminal: `envelope_terminal_unix_ms = 1733011199331`
(`envelope_terminal_utc_date 2024-11-30`). Per-horizon censored counts:
1s = 3 / 5s = 20 / 15s = 42 / 60s = 216; invalid-price rows = 0. Every layer is
`research_eligible = false`, `eligibility_gate_status = pending`,
`no_successor_authorization = true`.

All three layers passed their read-only eligibility gates **without** becoming
research-eligible. A passing gate proves byte-integrity, schema conformance,
lineage binding, and boundary/censoring correctness; it does **not** confer
admissibility for ML use.

---

## 7. Current source eligibility posture

The pre-v002 segment is **non-eligible at every layer**:
`research_eligible = false` and `eligibility_gate_status = pending`, with no
Stage-5 / research-use successor-state. This is the project's governing posture
and the central reason no data may yet feed any ML path.

The Phase 4aw `flip_research_eligible(...)` **always-raises invariant** is
preserved and was never invoked by this phase. Eligibility cannot be flipped by
a memo, by a gate pass, or by the existence of a split policy; it is governed by
the project's eligibility governance and remains an explicit, separate,
currently-unauthorized action. This memo **identifies** source admissibility as
a blocker (§12); it does not and may not solve it.

---

## 8. Existing committed ML-baseline tooling boundary

The committed ML-baseline tooling is the **Phase 4bn-B** stack, bound to the
**published v002 terminal** family, plus its Phase 4bm-W split helper:

- `diagnostics_split_policy_v002.py` (Phase 4bm-W) — encodes **only** the v002
  split `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`: train
  2024-12-01..2025-01-14 (45) / validation 2025-01-15..2025-02-13 (30) / test
  2025-02-14..2025-02-28 (15); boundaries `1736899200000` / `1739491200000`;
  `MIN_BOUNDARY_EMBARGO_SECONDS = 60`. `split_for_date()` **raises
  `SplitPolicyError`** for any date outside the 90-day v002 envelope — i.e. for
  **every** pre-v002 date.
- `ml_baseline_design_v002.py` (Phase 4bn-B) — declarative design constants
  hardcoded to the v002 terminal: `EXPECTED_PARTITION_COUNT = 90`,
  `EXPECTED_TOTAL_ROW_COUNT = 155,153,449`,
  `EXPECTED_FEATURE_CONFIG_HASH = 819cfa7a…`,
  `EXPECTED_LABEL_CONFIG_HASH = 352bad41…`, dates = `policy.TRAIN_START_DATE` ..
  `policy.TEST_END_DATE`. It also encodes the reusable **leakage controls**:
  the frozen 45-column computed feature matrix, the 17 lineage columns excluded,
  the `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS` guard, train-only standardization /
  imputation, 3-class signed direction framing, fixed-a-priori baselines (no
  search / no model selection), and the full `NON_AUTHORIZATION_FLAGS` block.
- `ml_baseline_dataset_v002.py` (Phase 4bn-B) — bounded-memory streaming loader.
  Its `discover_partition_refs()` hard-fails (`MlBaselineDatasetError`) unless
  the manifests carry the v002 family/version and `feature_config_hash =
  819cfa7a…`, expects exactly 90 partitions, and assigns splits via the v002
  `policy.split_for_date()`. It would reject the pre-v002 segment on the first
  guard (`feature_config_hash 0726b41d…` ≠ `819cfa7a…`; 275 ≠ 90 partitions).
- **`ml_baseline_splits.py` and `ml_baseline_train.py` do not exist.** There is
  **no committed end-to-end trainer**; the committed ML-baseline arc is design
  constants + a v002-bound dataset loader only.

**Boundary conclusion.** The existing tooling is **inadmissible to the pre-v002
segment** and cannot be reused directly — the same conclusion Phase 4bn-O /
4bn-S / 4bn-W / 4bn-X / 4bn-T / 4bn-P reached for normalization, feature, label,
and gate tooling. A future pre-v002 ML path would require a **new
segment-scoped** split-policy artefact (and, later, dataset and training
wrappers) that reuse the locked design constants and leakage controls but
re-bind the family, hashes, partition count, dates, and split windows to the
pre-v002 segment. None of that is built or authorized here.

---

## 9. Readiness question and verdict

**Verdict: the project is policy-ready but NOT implementation-ready for ML on
the pre-v002 path.**

| Readiness question | Verdict |
|---|---|
| 1. Is ML training ready now? | **No.** |
| 2. Is ML dataset creation ready now? | **No.** |
| 3. Is research matrix creation ready now? | **No.** |
| 4. Next step: implementation or docs phase? | A **narrow implementation** phase (code-level split-policy artefact + offline tests) — not training. |
| 5. Must the 4bn-Y split be a code-level artefact before any dataset builder? | **Yes.** |
| 6. Should that artefact be the next recommended phase? | **Yes.** |
| 7. Does source admissibility need separate resolution before data are used for ML? | **Yes** (before any dataset construction; not before the pure-code split artefact). |
| 8. May a dataset builder be built while sources stay non-eligible? | **No** — a dataset builder reads data; deferred until admissibility is resolved. |
| 9. Horizon-specific, multi-horizon, or defer? | **Defer** final task selection; recommend a narrow single-horizon first baseline when training is later authorized. |
| 10. Which label columns initially admissible? | Per-horizon `forward_log_return_*` / `forward_direction_*` as **targets only**; see §13. |
| 11. Which feature columns initially admissible? | Only the 45 causal computed `FEATURE_SCHEMA_V002` columns; see §14. |
| 12. Which columns excluded from model features? | 17 lineage + label + support + quality/forbidden; see §14. |
| 13. How to filter censored / invalid labels? | Drop per-horizon nulls; reject invalid-price rows; never impute targets; see §15. |
| 14. What leakage proof must a dataset builder emit? | See §16. |
| 15. What checks must offline tests cover? | See §17 – §18. |
| 16. What budget preflight before any dataset? | Phase 4bn-L caps + D: thresholds; see §19. |
| 17. What stays forbidden until after readiness + separate authorization? | See §20, §23. |

**Reason ML training is not authorized.** (a) The 4bn-Y split exists only as a
policy contract — no code encodes the 214/45/14 windows, the 2024-10-01 /
2024-11-16 embargo dates, or the pre-v002 exclusions; the only committed split
code raises on pre-v002 dates (§8). (b) Source admissibility is unresolved —
every source layer is `research_eligible=false` / `eligibility_gate_status=pending`
(§7). (c) No leakage / split-integrity proof exists for the pre-v002 split. (d)
No budget preflight has been run for any pre-v002 dataset construction. (e) No
committed trainer exists (§8). Any one of (a) – (d) is independently
disqualifying.

---

## 10. First conservative pre-v002 ML path scope

If — after the prerequisites in §20 are each separately satisfied and
authorized — a first ML-baseline path is ever built, its permitted scope is:

- **Instrument / source:** BTCUSDT / Binance USDⓈ-M futures / aggTrades **only**.
- **Dates:** pre-v002 **only**, 2024-03-01 .. 2024-11-30 inclusive UTC (275
  dates).
- **Inputs:** only the Phase 4bn-S feature segment (manifest `4881eb87…`,
  `feature_config_hash 0726b41d…`) and the Phase 4bn-W label segment (manifest
  `69746c88…`, `label_config_hash b3bd5d2b…`), each only after source
  admissibility is explicitly resolved.
- **Excluded:** the v002 terminal (2024-12-01 .. 2025-02-28) and the sealed test
  (2025-02-14 .. 2025-02-28) — both remain by reference only and untouched.
- **Full-envelope assembly:** **not required** for this conservative
  pre-v002-only path; required only before a future pre-v002 + v002 combined
  path; deferred and unauthorized.

---

## 11. Split-policy operationalization requirement

The Phase 4bn-Y Candidate A split is **sufficient as a policy contract but is
not operationalized**. A future code-level **pre-v002 split-policy artefact**
must encode it exactly:

- The 214 / (embargo 2024-10-01) / 45 / (embargo 2024-11-16) / 14 windows over
  2024-03-01 .. 2024-11-30, totalling 275 dates.
- Assignment by `source_transact_time_ms` UTC date; chronological-only.
- The 1-full-UTC-date boundary purge **and** the formal ≥ 60 s row-level
  earlier-split embargo floor (`exclude_from_earlier_split`), mirroring the v002
  `earlier_split_embargo_window_ms()` semantics but on the pre-v002 boundaries.
- Hard refusal of any shuffle / random / k-fold-over-time / bootstrap.
- Hard refusal to assign, load, or reference any v002 terminal or sealed-test
  date (the pre-v002 artefact must raise on any out-of-segment date, exactly as
  the v002 helper raises on pre-v002 dates today).
- A horizon-boundary protection proof: for every horizon H ∈ {1s, 5s, 15s, 60s},
  no earlier-split row whose forward target crosses an internal boundary may
  remain in the earlier split.

**This artefact is pure date / window arithmetic with no data I/O.** It can
therefore be authored and tested **before** source admissibility is resolved,
because it neither reads data nor confers eligibility. It is the recommended
next phase (§22).

---

## 12. Source admissibility requirement

Source admissibility is the **gating blocker for any data use**, distinct from
split operationalization:

- The pre-v002 segment remains `research_eligible = false` /
  `eligibility_gate_status = pending` at every layer.
- Resolving admissibility is an explicit eligibility-governance action that this
  memo neither performs nor authorizes, and that must respect the Phase 4aw
  `flip_research_eligible(...)` always-raises invariant — i.e. admissibility is
  **not** "flip the flag"; it is whatever the project's eligibility governance
  defines as the admissibility decision, recorded through the proper channel.
- A future ML **dataset builder** (which reads the feature/label Parquet) is
  **blocked** until admissibility is explicitly resolved.
- The pure-code **split-policy artefact** (§11) is **not** blocked by
  admissibility because it uses no data.

This memo's position: identify admissibility as the blocker; do not solve it. A
dedicated source-admissibility memo / gate is a valid (and likely necessary)
future phase, but the safest *immediate* step is the split-policy artefact,
which makes progress without touching the admissibility question.

---

## 13. Label / target readiness policy

For the first pre-v002 path (when later authorized):

- **Label family:** `microstructure_labels_aggtrades_v001 @ v002`,
  `label_schema_version = v001` (the Phase 4bn-W pre-v002 segment).
- **Available horizons:** 1s, 5s, 15s, 60s (1000 / 5000 / 15000 / 60000 ms).
- **Target framing:** the locked v002 framing — 3-class signed direction
  `{-1, 0, +1}` with the zero class preserved (and/or `forward_log_return_*` for
  descriptive cost-commensurability). No regression-only reframing, no binary
  collapse, no ordinal/meta-labeling beyond the locked framing.
- **Target columns admissible (per active horizon only):**
  `forward_direction_<H>` and/or `forward_log_return_<H>` plus the alignment keys
  (`row_index`, `agg_trade_id`, `feature_timestamp_ms`,
  `source_transact_time_ms`) and `horizon_censored_flag_<H>` for filtering.
- **First-baseline recommendation:** start narrow — a **single horizon** (e.g.
  one of 15s / 60s, consistent with the v002 design's included horizons) — to
  bound cost and leakage surface. This memo **recommends** but does **not
  authorize** any horizon or any training.
- **Forbidden label families (never derived or used):** barrier / target-before-
  stop / MFE / MAE / R-multiple / PnL / profit / loss / equity / position /
  alpha / edge / prediction / model / score / decision / strategy / entry /
  exit / signal / target — enforced by
  `FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002` (`pnl`, `mfe`, `mae`, `barrier`,
  `stop`, …).

---

## 14. Feature readiness policy

- **Admissible model features:** only the **45 causal computed feature/quality
  columns** of `FEATURE_SCHEMA_V002` (4 windows × 10 per-window + 3 time-context
  + 2 quality), under the locked causal policy
  (`leakage_policy = causal_only_no_future_lookahead`,
  `cross_day_lookback_policy = causal_cross_day_lookback`). These are exactly the
  `COMPUTED_FEATURE_COLUMN_NAMES` (`len == 45`) of `ml_baseline_design_v002`.
- **Excluded from the model matrix (always):**
  - the **17 lineage columns** (`EXCLUDED_LINEAGE_COLUMN_NAMES`: dataset/family/
    version identifiers, `symbol`, `utc_date`, `agg_trade_id`, `row_index`,
    `feature_timestamp_ms`, `source_transact_time_ms`, the source SHA lineage
    columns, `feature_config_hash`);
  - all **label / support / split / censor** columns, caught by the
    `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS` guard
    (`forward_log_return`, `forward_direction`, `horizon_censored_flag`,
    `label_`, `split_`, `censored_`);
  - any future-looking or post-label column.
- **Raw prices as features:** **forbidden** unless a future dataset contract
  explicitly authorizes them (the normalized trade price is a label input, not a
  model feature, in the first path).
- **Quality flags** (`invalid_window_flag`, `rolling_missing_window_flag`) are
  retained inside the 45-column matrix as the v002 design specifies (they encode
  missingness; they are not standardized). No additional support/quality column
  may be promoted into the matrix without an explicit future dataset contract.

---

## 15. Censored / invalid target filtering policy

- **Censored labels:** never imputed. For each active horizon, **drop** rows
  where `horizon_censored_flag_<H>` is set or where the per-horizon
  `forward_direction_<H>` / `forward_log_return_<H>` is null. (The pre-v002
  segment carries 1s = 3 / 5s = 20 / 15s = 42 / 60s = 216 censored rows at the
  2024-11-30 envelope terminal.)
- **Invalid-price labels:** the segment has **0** invalid-price rows; the future
  policy must nonetheless **reject/filter** any such row and **never impute** it.
- **Supervised mask (per horizon):** included iff *not censored* **and** *not
  embargoed* **and** *direction non-null* **and** *log-return non-null* — exactly
  the `load_partition_matrices` mask semantics of the committed v002 dataset
  loader, re-bound to the pre-v002 split.
- **Internal holdout (2024-11-17 .. 2024-11-30):** usable only as a dry-run; it
  must **not** be used for model selection, hyperparameter selection, threshold
  tuning, or any final / strategy / production claim. The sealed test stays at
  `test_rows_loaded = 0`.

---

## 16. Leakage and split-integrity proof requirements

A future pre-v002 dataset builder / split artefact must emit a machine-checkable
leakage / split-integrity proof recording, at minimum:

1. **Partition / split assignment** — each of the 275 dates assigned to exactly
   one of {train, embargo-dropped, validation, embargo-dropped, holdout}; counts
   214 / 1 / 45 / 1 / 14; no date unassigned or double-assigned.
2. **No boundary crossing** — for every horizon H, zero earlier-split rows whose
   `source_transact_time_ms + H_ms` crosses an internal boundary remain in the
   earlier split; the ≥ 60 s embargo (and the 1-day purge) verified empty of
   leakage.
3. **No shuffle** — assignment is a pure function of `source_transact_time_ms`
   UTC date; no RNG influences split membership.
4. **No v002 / sealed access** — `v002_terminal_window_read = false`,
   `sealed_test_split_touched = false`, `test_rows_loaded = 0`; the artefact
   raises on any out-of-segment date.
5. **Strict feature/label alignment** — per day, identical
   `(row_index, agg_trade_id, feature_timestamp_ms, source_transact_time_ms)` in
   identical order (positional pairing, no join).
6. **Manifest / config SHA binding** — feature manifest `4881eb87…` +
   `feature_config_hash 0726b41d…`; label manifest `69746c88…` +
   `label_config_hash b3bd5d2b…`; predecessor gate reports `db731d1b…` /
   `3452fd9d…` / `ffb5b09…` re-verified.
7. **Train-only transform provenance** — standardization / imputation statistics
   fit on the train split only (see §18).

---

## 17. Future ML dataset contract requirements

If an ML dataset builder is ever authorized, its contract must (mirroring the
Phase 4bn-O/S/W segment-wrapper precedent):

- Re-bind to the pre-v002 family/hashes/partition count (275, not 90) and the
  pre-v002 split windows; never reuse the v002 `feature_config_hash 819cfa7a…` /
  `label_config_hash 352bad41…` / 90-partition guards.
- Stream bounded memory (≤ one feature + one label partition materialised at a
  time); never load the full segment into memory.
- Never load any v002 terminal or sealed-test partition into any train /
  validation / holdout stream.
- Apply the §14 feature scope, §13 target scope, and §15 filtering exactly.
- Write outputs **local and gitignored only** (under
  `data/research/microstructure/…` per the v002 output-namespace precedent),
  each with a canonical Phase 4bb-F sidecar; commit **nothing**; flip no
  eligibility; create no reusable split mask that could be mistaken for an
  eligibility transition.
- Carry the full `NON_AUTHORIZATION_FLAGS` evidence block (all `False`).

No such builder is authorized here.

---

## 18. Future transform-fitting and model-selection rules

- **Train-only transform fitting:** mean/std (and any imputation statistic) are
  accumulated over the **train** split only and applied unchanged to validation
  / holdout; never refit on validation, holdout, or test. The committed
  `StreamingStandardizer` enforces this (`fit_partition` raises unless
  `split == TRAIN`); a pre-v002 artefact must preserve the same rule.
- **Imputation:** fixed-zero for null numeric features (fit-free, declared
  a-priori); booleans never imputed.
- **Model selection:** **none through results** — fixed-a-priori baselines only,
  run once each; no hyperparameter / grid / random / Bayesian / CV search; no
  feature ranking / selection / pruning; no ensemble/stacking/voting; forbidden
  families per `FORBIDDEN_BASELINE_FAMILIES` (deep learning, GBM, XGBoost,
  random forest, etc.). The holdout/dry-run is descriptive only and must not
  drive selection.

---

## 19. Future budget and storage preflight requirements

Any future dataset-construction or ML phase must run a Phase 4bn-L preflight
**before** writing and fail closed if any cap would be exceeded:

- Derived-artefact footprint: warn 75 GiB / hard cap 125 GiB (per layer);
  total derived-stack warn 250 GiB / hard cap 300 GiB.
- Runtime: warn 4 h / hard cap 8 h.
- Temp: warn 50 GiB / hard cap 100 GiB.
- `D:` free space: ≥ 500 GiB required before start; fail closed below 350 GiB
  during.

Headroom context (informational): the gated pre-v002 derived stack already sums
to ≈ 73 GiB (normalized 3.95 GB + feature 54.25 GB + label 15.65 GB), well under
the 250 GiB total-derived warn; a dataset build adds to this and must be
preflighted against the same caps.

---

## 20. Explicit blockers before ML training

ML training on the pre-v002 path is blocked until **all** of the following are
each separately satisfied and authorized:

1. This ML-baseline readiness memo recorded (**done by this phase**).
2. A **code-level pre-v002 split-policy artefact + offline tests** (§11) — not
   built here.
3. **Source admissibility resolved** (§7, §12) — segment currently
   `research_eligible=false` / `eligibility_gate_status=pending`.
4. An **ML dataset contract / builder** (§17) with its **leakage / split-
   integrity proof** (§16).
5. A **budget preflight** (§19) for dataset construction.
6. A **per-task target / horizon / filtering decision** (§13, §15).

A committed end-to-end **trainer does not exist** (§8) and would itself be a
later, separately-authorized phase even after 1 – 6.

---

## 21. Candidate next phases considered

- **(A) Pre-V002 split-policy artefact + offline tests** — pure code/tests,
  no data I/O, not blocked by admissibility, directly operationalizes the only
  unbuilt half of the 4bn-Y contract. **Lowest risk; highest leverage.**
- **(B) Source-admissibility memo / gate** — necessary eventually, but it
  neither builds nor unblocks the split artefact, and resolving admissibility is
  the heaviest governance action; sequencing it first delays safe progress.
- **(C) ML dataset contract memo** — useful, but premature while the split is
  not operationalized and admissibility is unresolved; the contract leans on
  both.
- **(D) Full-envelope reference-assembly memo** — only relevant to a future
  pre-v002 + v002 combined path; explicitly **not required** for the
  conservative pre-v002-only path; would expand scope toward the v002 terminal,
  against the conservative direction.
- **(E) Holdout-boundary memo** — only required if a future scope touches the
  v002 terminal or sealed-test dates; the conservative path touches neither, so
  **not required**.
- **(F) Remain paused / close the ML arc** — valid operator options, but the arc
  has a clear, low-risk next step, so closing is not recommended.

---

## 22. Selected next recommendation

**Recommend a narrow Phase 4bn-AA — Pre-V002 Split-Policy Artefact + Offline
Tests** (working name; subject to separate operator authorization):

- Implement Candidate A exactly (§11): 214 / 45 / 14 windows, 2024-10-01 /
  2024-11-16 embargo dates, ≥ 60 s row-level floor + 1-day purge, no shuffle,
  hard v002/sealed exclusion, horizon-boundary protection.
- Pure date/window arithmetic; **no data I/O**; offline tests only; no manifest
  write; no eligibility transition; no `chronological_split_policy` field set.
- It does **not** require source admissibility to be resolved first (it touches
  no data), while leaving actual dataset construction blocked until admissibility
  is explicitly resolved (§12).

This is the safest technical step that makes real progress without reading data,
flipping eligibility, or approaching the v002 terminal / sealed test. Dataset
construction, leakage-proof emission over real data, budget preflight, and
training each remain later, separately-authorized phases.

---

## 23. Explicit non-authorizations

This phase authorizes **none** of: any merge phase for 4bn-Z; the pre-v002
split-policy code artefact; a source-admissibility memo/gate; an ML dataset
contract memo; an ML dataset builder; a research matrix; a model; scores or
predictions; diagnostics; strategy / signals / PnL / backtests; full-envelope
reference assembly; a holdout-boundary memo; a source-policy documentation memo;
a process-doc `D:` path-string update; any eligibility flip or
`eligibility_gate_status` transition; any `chronological_split_policy` manifest
field; any storage migration / database / Parquet compaction / v003; any
acquisition / endpoint call / archive download / HEAD preflight; any paper /
shadow / live / exchange-write / production-key / credentials / MCP / Graphify
work; any Phase 5; or any other successor.

---

## 24. Decision

- **Result state:**
  `ML_BASELINE_READINESS_RECORDED__PRE_V002_PATH_READY_FOR_SPLIT_POLICY_ARTEFACT__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_PRE_V002_SPLIT_POLICY_ARTEFACT__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Rationale: the project is policy-ready (gated source stack + recorded split
policy) but not implementation-ready; the next safe step is to operationalize
the 4bn-Y split in code/tests, which is pure code with no data use, no
eligibility change, and no v002/sealed contact. ML training, dataset creation,
and research-matrix creation are each **not ready** and remain blocked behind the
§20 prerequisites.

---

## 25. Recommended state and successor options

**Recommended state: remain paused. No next phase authorized by this memo.**

Acceptable operator options after this branch's branch-complete report:

- remain paused;
- request a merge prompt for Phase 4bn-Z;
- separately authorize the **pre-v002 split-policy artefact + offline tests**
  (the recommendation);
- separately authorize a **source-admissibility memo** (if preferred to sequence
  admissibility first);
- separately authorize an **ML dataset contract memo** (if preferred to clarify
  the dataset contract before the split artefact);
- separately authorize a **full-envelope reference-assembly memo** only if a
  future path combines pre-v002 + v002 data;
- separately authorize a **holdout-boundary memo** only if a future scope
  touches the v002 terminal or sealed-test dates;
- separately authorize a **source-policy documentation memo** or a **process-doc
  `D:` path-string update**;
- reject further ML-baseline successors and **close the ML arc**.

No ML / diagnostics / strategy / PnL / backtest / storage-migration / paper /
shadow / live / exchange-write option is valid from this state unless separately
authorized after this branch is merged.

---

## 26. Current-project-state update summary

`docs/00-meta/current-project-state.md` is amended **additively only**: one new
Phase 4bn-Z paragraph (recording phase type, tier, branch, base SHA, the
readiness verdict, the result state / decision, and the full non-authorization
posture) plus one new `Current phase:` block at the top of the
`Current phase:` history. All prior Phase 4bn-A … 4bn-Y paragraphs and blocks,
every retained verdict, and every project lock are preserved verbatim. No other
section is modified.
