# Phase 4bn-AG — Data-Reading ML Dataset Builder Authorization Memo

## 1. Purpose

This is a **docs-only** authorization memo. It decides whether the project is
ready to **recommend** a future, separately-authorized phase that **implements
and runs** a real, data-reading pre-v002 ML dataset builder — using the Phase
4bn-AF code-only skeleton as the contract surface — and, if so, records the
exact conditions, gates, proofs, and boundaries that future phase must obey.

The memo answers one question and records a posture:

> Are the Phase 4bn-AC source contract, the Phase 4bn-AD builder-readiness
> decision, the Phase 4bn-AE pre-registration amendment, and the passing Phase
> 4bn-AF code-only skeleton (97 synthetic tests) now sufficient to **recommend**
> authorizing a future data-reading ML dataset builder implementation + single
> run, subject to separate operator authorization — and under exactly what
> constraints?

This phase **is not** the data-reading builder. It reads no local data, creates
no local data, creates no output namespace, adds no source / tests / scripts,
mutates no manifest, sets no manifest field, creates no split file / research
matrix / ML dataset / ML config / manifest / gate report / sidecar, trains no
ML, runs no diagnostics, and authorizes no successor. It records a docs-level
authorization **recommendation** and the binding conditions for a future phase;
it grants nothing by itself.

**Critical re-lettering note (recorded per the authorization prompt).** The
Phase 4bn-AE arc budget (§18 of that memo) tentatively reserved the `Phase
4bn-AG` slot for the *data-reading builder run*. Because this Phase 4bn-AG is now
used as this docs-only authorization memo, the actual future data-reading builder
implementation/run, **if separately authorized**, should be **Phase 4bn-AH** (or
otherwise explicitly re-lettered by the operator), and the remaining arc shifts
by one letter (see §14, §25, §26). This memo must **not** be treated as, or
silently collapsed into, the builder run.

---

## 2. Authority and repository state

- **Phase:** 4bn-AG — Data-Reading ML Dataset Builder Authorization Memo.
- **Authorized by:** the operator, following the Phase 4bn-AF decision
  `RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_AUTHORIZATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Branch:** `phase-4bn-ag/data-reading-builder-authorization-memo`.
- **Base `main` SHA:** `51263952f2673526dccc39f99dc3b08e1124197a`
  (`docs(phase-4bn-af): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == 51263952…` verified.
- **Predecessor chain on `main`:** Phase 4bn-AF SHA-finalization `5126395`,
  merge-closeout `e6151dd`, merge `3ca2234`, branch `77da4be`; Phase 4bn-AE
  finalization `3e0e26e` present.
- **Remote:** `https://github.com/jpedrocY/Prometheus.git`.
- **Gitignored namespaces:** `data/microstructure/` (`.gitignore:85`),
  `data/research/` (`.gitignore:88`).
- **Working-tree:** only the expected untracked transient
  `.claude/scheduled_tasks.lock`.

This phase is branch-complete only by its own work; it is **not merged into
`main`** and is **not project-complete**. It becomes project-complete only when a
separately authorized merge phase records its merge-closeout on `main`.

---

## 3. Phase type and strict scope

- **Phase type:** docs-only / data-read authorization decision / ML dataset
  builder authorization conditions / leakage-proof and budget-preflight binding /
  no-data-read memo.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3, because this phase
  decides whether the project may move from a code-only synthetic skeleton toward
  a future data-reading ML dataset builder path. An error here could authorize
  local data reads, dataset-output creation, leakage-prone builder behaviour,
  budget-unsafe execution, or research-matrix / ML work too early. This phase
  itself reads no local data and creates no local data.

**Strict scope (all enforced).** No source code; no tests; no scripts; no
modification of any source or test module; no data read; no data created; no
inspection of any file under `data/microstructure/` or `data/research/`; no
inspection of raw zip / normalized / feature / label Parquet / manifest / gate
report / sidecar; no v002-terminal read; no sealed-test read; no split file; no
research matrix; no ML dataset; no ML config; no manifest; no gate report; no
sidecar; no future output namespace; no training; no scoring; no prediction; no
diagnostics; no strategy / signals / PnL / backtests; no `research_eligible`
flip; no `eligibility_gate_status` transition; no `chronological_split_policy`
set in any manifest; no invocation or alteration of the Phase 4aw
`flip_research_eligible(...)` always-raises invariant; no successor
authorization from inside this memo.

---

## 4. Evidence base and input boundary

Written from **committed docs + committed source/tests only**. No local artefact
under `data/microstructure/` or `data/research/` was read or inspected. The
README is treated as potentially stale and is **not** used as a current-state
authority.

**Committed docs grounding (read-only):** the process standards
(`phase-workflow-standard`, `merge-closeout-standard`,
`phase-risk-tiering-standard`, `phase-prompt-template`, `operator-report-standard`);
`current-project-state.md`; and the Phase 4bn-Y / Z / AA / AB / AC / AD / AE /
AF implementation reports, merge-closeouts, and closeouts. The Phase 4bn-AF
skeleton report and merge-closeout, and the Phase 4bn-AC / AD / AE governance
memos, are the primary predecessor authority.

**Committed source grounding (read-only, for authorization precision):**

- `src/prometheus/research/microstructure/pre_v002_ml_dataset_contract.py` —
  the Phase 4bn-AF inert contract constants (contract name / amendment id;
  symbol / market / source; segment dates; 275 partition counts; 400,001,695
  rows; the eight expected manifest/config/gate SHA256s; the rejected v002
  `819cfa7a…` / `352bad41…` hashes; the 45 feature allowlist; the 17 lineage
  exclusions; forbidden substrings; primary target/horizon; the amendment-001
  evaluation layer; `OUTPUT_NAMESPACE_PATH` as an inert string).
- `pre_v002_ml_dataset_builder.py` — `PreV002MlDatasetError` + the 12 pure
  fail-closed validators/planners the future builder must import and use.
- `pre_v002_ml_dataset_proof.py` — the proof schema and validators, and the
  `BudgetPreflightPlaceholder` echoing the exact Phase 4bn-L caps
  (`DERIVED_FOOTPRINT_WARN_GIB=75` / `HARD_GIB=125`;
  `TOTAL_DERIVED_STACK_WARN_GIB=250` / `HARD_GIB=300`; `RUNTIME_WARN_HOURS=4` /
  `HARD_HOURS=8`; `TEMP_WARN_GIB=50` / `HARD_GIB=100`;
  `D_DRIVE_MIN_FREE_GIB_BEFORE=500`; `D_DRIVE_FAIL_CLOSED_DURING_GIB=350`).
- `tests/research/microstructure/test_phase4bn_af_pre_v002_ml_dataset_builder_skeleton.py`
  — the 97 offline synthetic tests (existence and pass status carried forward
  from the Phase 4bn-AF report; not re-run here as a code phase).
- `pre_v002_split_policy.py` — the Phase 4bn-AA split authority
  (`SPLIT_POLICY_NAME = "CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO"`;
  214 / 1 / 45 / 1 / 14; pure, no I/O; hard-raises out-of-segment / v002 /
  sealed).
- `features_schema_v002.py` / `features_schema.py` / `labels_schema_v002.py` —
  the 45 causal feature columns, the 17 lineage columns, the 40-column label
  schema, `DIRECTION_THRESHOLD_POLICY_V002`, and the forbidden-substring guards.

**Input boundary (not read).** No local Parquet (raw / normalized / feature /
label); no local raw zip; no local manifest or gate report under
`data/microstructure/`; no v002-terminal window; no sealed-test file; no
`data/research/` output; no v002 terminal / sealed-test files. Every numeric
figure carried forward (275 partitions, 400,001,695 rows, footprints, hashes,
gate verdicts, censor counts) comes from the merged predecessor reports, not from
reading any local artefact.

---

## 5. Current blocker ledger

Carried forward from Phase 4bn-AF §27–§29, Phase 4bn-AC §23–§25, and Phase
4bn-AB §18–§20. Before any pre-v002 **data read** for ML purposes, all of the
following were required:

1. A recorded ML dataset **contract** (Phase 4bn-AC) — **done**.
2. A **builder-readiness** decision, code-only-first (Phase 4bn-AD) — **done**.
3. A pre-registered **evaluation / dependence / success-kill / cost-realism /
   strategy-boundary** layer, amending the contract (Phase 4bn-AE) — **done**.
4. A passing **code-only skeleton** binding the contract, split artefact, passed
   gates/hashes as validators over synthetic inputs, with no-data-I/O and
   no-output-namespace proofs (Phase 4bn-AF; 97 tests, ruff clean, 0 direct mypy
   errors) — **done**.
5. A **code-level, data-reading builder** that imports the skeleton and binds to
   the passed gates (`3452fd9d…` / `db731d1b…` / `ffb5b09…`), the manifests /
   hashes, and the Phase 4bn-AA split artefact — **not yet built**.
6. A **leakage / split-integrity proof** (Phase 4bn-AC §19) and a **Phase 4bn-L
   budget preflight** (Phase 4bn-AC §20) **bound into a data-reading builder** —
   **not yet built** (the skeleton encodes their *schema*; a real proof over real
   data and a real preflight are builder work).
7. **Separate data-read authorization** — `source_admissible_for_data_read` is
   **false** (memo-level governance concept per Phase 4bn-AB §9).
8. **Separate dataset-builder authorization** —
   `source_admissible_for_dataset_builder` is **false** (memo-level concept).

**How this memo handles the ledger.** Items 1–4 are complete on `main`. This
memo finds the project **ready to recommend** a future phase that satisfies items
5 and 6 and is granted items 7 and 8 by **separate operator authorization**. This
memo does **not** satisfy items 5–8 itself: it does not build the builder, does
not create the leakage proof over real data, does not run the budget preflight,
and does not grant data-read / builder authorization. It records the
recommendation and the exact conditions (§14–§23). The two admissibility
concepts remain **false** until the future data-reading builder phase (Phase
4bn-AH) records them under separate operator authorization by the docs-only
convention Phase 4bn-AB established (§13).

---

## 6. Phase 4bn-AC source contract carried forward

Carried verbatim as the binding **source contract**
(`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`), unchanged by this
memo:

- **Source scope (permitted, by reference / future-authorized read only):**
  BTCUSDT / Binance USDⓈ-M futures / aggTrades; pre-v002 only 2024-03-01 ..
  2024-11-30 inclusive UTC (275 dates; 400,001,695 rows by reference).
- **Bound inputs:** Phase 4bn-S features (manifest `4881eb87…9b52`;
  `feature_config_hash 0726b41d…114c`; feature-layer gate `db731d1b…6ab08`
  27/27) + Phase 4bn-W labels (manifest `69746c88…b161`;
  `label_config_hash b3bd5d2b…8970`; label-layer gate `ffb5b092…8984` 40/40) +
  Phase 4bn-O normalized lineage (manifest `0e96ae37…d9fa`; normalized-layer gate
  `3452fd9d…f134` 25/25) by reference.
- **Forbidden source scope:** v002 terminal (2024-12-01 .. 2025-02-28); sealed
  test (2025-02-14 .. 2025-02-28, `test_rows_loaded=0`); full-envelope assembly;
  non-BTCUSDT; spot / mark-price / order-book / kline / liquidation / funding /
  open-interest / cross-venue; newly acquired data; raw zip; any family not in
  the pre-v002 chain (incl. published `819cfa7a…` / `352bad41…`); `data/research`
  priors; external / private / authenticated sources — all fail-closed.
- **Split binding:** import `pre_v002_split_policy.py` as the sole authority
  (`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`; train
  2024-03-01..2024-09-30 = 214; embargo 2024-10-01; validation
  2024-10-02..2024-11-15 = 45; embargo 2024-11-16; internal holdout / dry-run
  2024-11-17..2024-11-30 = 14; assignment by `source_transact_time_ms` UTC date;
  drop embargo; per-horizon earlier-split boundary protection; hard-raise on
  out-of-segment / v002 / sealed dates; no shuffle / random / k-fold / bootstrap
  / resampling).
- **Target / horizon:** family `microstructure_labels_aggtrades_v001 @ v002`;
  primary first-baseline target `forward_direction_15s`, 3-class signed
  `{-1, 0, +1}`, zero class preserved, per `DIRECTION_THRESHOLD_POLICY_V002`;
  1s/5s/60s deferred; secondary descriptive-only `forward_log_return_15s`; no
  binary collapse; no regression reframing; no barrier / stop / MFE / MAE /
  R-multiple / PnL labels.
- **Feature allowlist:** exactly the 45 causal computed `FEATURE_SCHEMA_V002`
  columns; 17 lineage columns excluded; all label / support / split / censor
  columns excluded; forbidden substrings `forward_log_return`,
  `forward_direction`, `horizon_censored_flag`, `label_`, `split_`, `censored_`;
  raw prices excluded absent an explicit future revision.
- **Filtering / alignment / execution order / train-only transforms / leakage
  proof / budget preflight / output namespace / non-authorization boundaries:**
  exactly as Phase 4bn-AC §13–§21, carried into §15–§21 below.

---

## 7. Phase 4bn-AD readiness carried forward

Carried verbatim: the readiness verdict is **contract-ready and skeleton-ready,
NOT data-reading-ready, NOT dataset-ready, NOT ML-ready** — as of Phase 4bn-AD.
Phase 4bn-AD recommended a code-only skeleton first (executed as Phase 4bn-AF),
and established the **precedent-only** boundary for the v002-terminal-bound stack
(`ml_baseline_dataset_v002.py` is a data-reading loader identity-bound to the
v002 terminal — 90 partitions / 155,153,449 rows / `feature_config_hash
819cfa7a…` / `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` — and is
**inadmissible** to pre-v002; `ml_baseline_splits.py` and `ml_baseline_train.py`
do not exist). The future data-reading builder must be a **new pre-v002-specific
data-reading module** that imports the Phase 4bn-AF skeleton validators; it must
not wrap, copy, or reuse the v002-terminal loader. Phase 4bn-AD's data-read /
dataset-builder / ML blockers are the blocker ledger this memo now revisits (§5).

---

## 8. Phase 4bn-AE amendment carried forward

Carried verbatim as **amendment 001** to the source contract. Unchanged by this
memo and binding on the future builder and the future evaluator:

- **Claim scope:** the first baseline may claim only (a) whether the 45 causal
  aggTrades features carry short-horizon directional information, (b) whether the
  v002 small-lift sign reproduces across the pre-v002 regime span, (c) whether
  probability calibration / the high-confidence tail is adequate — and **never**
  tradability / profitability / strategy / execution / PnL / backtest / live.
- **Target interpretation:** `forward_direction_15s` is a non-economic
  information-diagnostic target that may embed bid-ask-bounce artifacts
  (aggTrades-only, no mid-price / book data).
- **Overlapping-label dependence policy (Option 1):** row-level metrics are
  descriptive only; the decision unit is the UTC date/month block; per-row
  significance language is forbidden; decimation stride is `None` /
  `reserved_not_adopted`.
- **Metric registry (21 mandatory metrics), granularities
  (aggregate/utc_month/utc_date), calibration / confidence-tail policy,
  cost-realism descriptive policy (share of 15s moves exceeding the 16 bps
  round-trip lock; descriptive only).**
- **Pre-registered success / continue / kill constants:** accuracy uplift +2.0
  pp over both floors; balanced accuracy +1.0 pp; macro-F1 +0.03;
  majority-of-blocks agreement; holdout-no-sign-reversal; calibration-tail rule.
  These are frozen; they may not be relaxed after a result is seen.
- **Strategy / PnL / backtest hard boundary:** no baseline result authorizes
  strategy / signals / PnL / backtest; any path there requires a future M0-style
  mechanism-admissibility memo clearing cost realism at 8 bps/side · 16 bps
  round-trip (§30).
- **Finite arc budget** (renumbered here per §1, §14): skeleton (Phase 4bn-AF,
  done) → data-reading builder run → descriptive dataset diagnostics → fixed
  baseline run → arc-decision, then close or one bounded follow-up.

---

## 9. Phase 4bn-AF skeleton carried forward

Carried verbatim as the **contract surface** the future builder must import and
bind to. Phase 4bn-AF is merge-complete on `main` at
`51263952f2673526dccc39f99dc3b08e1124197a`. It implemented three new source
modules and one offline test module (97 synthetic tests, all passing; ruff clean;
0 direct mypy errors — 29 pre-existing unrelated sibling errors, identical to the
committed `pre_v002_split_policy.py` set):

- **`pre_v002_ml_dataset_contract.py`** — inert contract constants + 5 frozen
  dataclasses.
- **`pre_v002_ml_dataset_builder.py`** — `PreV002MlDatasetError` + 12 pure
  fail-closed validators/planners: `validate_source_scope`,
  `validate_manifest_hashes` (rejects v002 `819cfa7a…` / `352bad41…`),
  `validate_feature_allowlist` (exactly 45), `scan_forbidden_columns` /
  `find_forbidden_columns` / `assert_no_forbidden_columns`, `filter_targets`
  (drops null/censored/invalid by reason; never imputes), `assert_strict_alignment`
  (no join/reorder/fill/tolerance/dedup), `assign_split` (delegates to
  `pre_v002_split_policy`; hard-raises out-of-segment / v002 / sealed),
  `should_drop_for_split` (embargo only), `validate_no_boundary_crossing`
  (Phase 4bn-AA helper), `plan_train_only_transform` (train-only fit; non-train
  fails closed), `validate_evaluation_schema`, `build_skeleton_plan`.
- **`pre_v002_ml_dataset_proof.py`** — 7 proof dataclasses + `build_dataset_builder_proof`
  / `validate_dataset_builder_proof`; `BudgetPreflightPlaceholder` echoes the
  exact Phase 4bn-L caps and is interface-shape only (`is_placeholder=True`,
  `measured_disk=False`, `wrote_output=False`); `validate_dataset_builder_proof`
  fails closed on wrong split counts (214/1/45/1/14), `test_rows_loaded≠0`,
  v002/sealed access, non-empty forbidden scan, missing metrics/granularities,
  imputed targets, a non-placeholder budget preflight, any True non-authorization
  flag, or a created output namespace.

The skeleton reads no data, creates no output, and never wraps/copies the
v002-terminal loader. It is exactly the validated, contract-bound core a future
data-reading builder must inherit rather than re-derive under data-read pressure.

---

## 10. Authorization question

This memo answers, by reference only and reading no data:

1. **Is the project now ready to authorize a future data-reading builder
   implementation/run?** — **Ready to *recommend* it**, subject to separate
   operator authorization; not to *grant* it here (§11, §12, §33).
2. **Under exactly what constraints?** — §14–§23.
3. **What must the future builder do before reading any data?** — §15.
4. **What must it verify before writing anything?** — §16, §17.
5. **What must it write, if authorized?** — §20.
6. **What must it never write?** — §21.
7. **What budget preflight must pass?** — §17.
8. **What leakage proof must be created?** — §18.
9. **What sidecar / proof policy applies?** — §19.
10. **Does this phase transition `source_admissible_for_data_read` or
    `source_admissible_for_dataset_builder`?** — **No** (§13).
11. **If yes, where recorded?** — n/a; not transitioned here (§13).
12. **If no, what remains blocked?** — §27–§30.
13. **What next phase is recommended?** — Phase 4bn-AH data-reading builder
    implementation + single run, subject to separate operator authorization
    (§26).
14. **What remains unauthorized?** — §31.

---

## 11. Data-read admissibility assessment

**Verdict: RECOMMEND authorizing data reads in a future phase — not granted
here.** The four governance prerequisites for the *first* pre-v002 data read are
now present on `main`: the recorded contract (Phase 4bn-AC), the readiness
decision (Phase 4bn-AD), the pre-registration amendment (Phase 4bn-AE), and a
passing code-only skeleton binding the contract, split artefact, and passed gates
as fail-closed validators with no-data-I/O and no-output-namespace proofs (Phase
4bn-AF). The skeleton demonstrates the contract is precise and enforceable in
code. This is sufficient basis to **recommend** that a future phase read the
pre-v002 feature/label segments **under strict gates** — but the read still
requires two things this memo does not provide: (i) a **data-reading builder**
that carries a real leakage proof and a real Phase 4bn-L budget preflight (§17,
§18), and (ii) **separate operator authorization**. Therefore
`source_admissible_for_data_read` remains **false** (§13) until the future data-
reading builder phase records it under separate authorization.

**Why not a stricter blocker.** No blocker was found that should force additional
skeleton hardening, a separate source-admissibility gate artefact, a budget-
preflight design memo, or remaining paused (§24, §25). The skeleton is complete
and passing; the budget thresholds are already fully specified (Phase 4bn-L, AC
§20, AD §22, and the skeleton's `BudgetPreflightPlaceholder`); the leakage-proof
schema is already defined and validated (Phase 4bn-AF proof module); and Phase
4bn-AB §21(B) already considered and rejected a separate code-level source-
admissibility gate as heavier than needed and conflated with the still-
unimplemented Phase 4aw eligibility gate — the data-reading builder does not flip
`research_eligible`, reads only gitignored local data, and writes only gitignored
local output, so no eligibility gate is on its path.

---

## 12. Dataset-builder admissibility assessment

**Verdict: RECOMMEND authorizing a single data-reading builder run in a future
phase — not granted here.** Per Phase 4bn-AB §9, `source_admissible_for_dataset_builder`
becomes true only via a future separately-authorized phase that binds the
contract + budget preflight + leakage proof. The contract (AC) and its amendment
(AE) are recorded; the budget-preflight thresholds and leakage-proof schema are
specified and encoded in the skeleton (AF); the builder-readiness decision (AD)
is recorded. The one missing element is the builder implementation itself, plus
its separate authorization. This memo finds the project ready to **recommend**
that a future phase implement and run — **exactly once** — a data-reading builder
that (a) imports the Phase 4bn-AF skeleton, (b) binds the AC contract and AE
amendment, (c) runs a real budget preflight and fails closed on breach, and (d)
emits a real leakage/split-integrity proof and Phase 4bb-F sidecar. Until that
phase exists and is separately authorized, `source_admissible_for_dataset_builder`
remains **false** (§13).

---

## 13. Manifest-transition posture

**No manifest is created, read, or mutated by this phase. No manifest field is
set. This memo records a docs-level authorization *posture* only.**

Per Phase 4bn-AB §4 and §9, `source_admissible_for_data_read` and
`source_admissible_for_dataset_builder` are **memo-level governance concepts, not
manifest fields** — a repository term search confirmed `source_admissib*` appears
nowhere in the microstructure source. The Phase 4bn-AB memo established the
docs-only convention for recording such posture: it is a *recorded documentation
conclusion about permitted future use*, never a manifest transition, and it never
implies `research_eligible = true`.

This memo records the following **docs-level posture** (documentation only; not
manifest fields; not eligibility transitions):

| Posture concept | Value recorded by this memo |
|---|---|
| `data_read_authorization_recommended` | **true** (recommendation only; §11) |
| `builder_implementation_run_recommended` | **true** (recommendation only; §12) |
| `source_admissible_for_data_read` | **false** — unchanged; transitions only in the future data-reading builder phase (Phase 4bn-AH) under separate operator authorization, by the Phase 4bn-AB docs-only convention |
| `source_admissible_for_dataset_builder` | **false** — unchanged; same mechanism |
| `ml_authorized` / `diagnostics_authorized` / `strategy_backtest_authorized` | **false** — unchanged |

**Actual manifest fields — all unchanged, byte-identically to before this phase,
at every pre-v002 layer (normalized `0e96ae37…`, feature `4881eb87…`, label
`69746c88…`):** `research_eligible = false` (not flipped);
`eligibility_gate_status = pending` (not transitioned);
`chronological_split_policy = not set` (not transitioned);
`no_successor_authorization = true` (preserved). The Phase 4aw
`flip_research_eligible(...)` always-raises invariant is **preserved and never
invoked** (this memo imports no manifest reader and touches no manifest).

Because the repository's only convention for transitioning these memo concepts is
the Phase 4bn-AB docs-only convention — and that convention reserves the
`*_for_data_read` / `*_for_dataset_builder` transitions to "a future
separately-authorized dataset-builder phase" — this memo keeps both **false** and
records the transition as a **recommendation**, not a mutation. No manifest
mutation is invented.

---

## 14. Future builder implementation/run scope

**Future phase identity (re-lettering).** The future data-reading builder
implementation/run, **if separately authorized**, should be **Phase 4bn-AH** (the
`AG` slot the Phase 4bn-AE arc budget tentatively reserved for it is now consumed
by this authorization memo). The remaining arc shifts by one letter and is
recommended as: **Phase 4bn-AH** — data-reading builder implementation + single
run; **Phase 4bn-AI** — pre-declared descriptive dataset diagnostics (no models);
**Phase 4bn-AJ** — fixed baseline run (majority / persistence / linear, run once,
no selection); **Phase 4bn-AK** — arc-decision memo (close, or authorize exactly
one bounded follow-up per Phase 4bn-AE §16). The operator may re-letter or
compress these steps; the finite, five-step-then-decide shape is preserved. This
memo authorizes none of them.

**Future phase type (recommended).** Code + controlled local data read + local
gitignored output creation, **if separately authorized** — a **single controlled
run**, not an open-ended process (§22).

**The future builder MUST:**

- import and use the Phase 4bn-AF skeleton modules
  (`pre_v002_ml_dataset_contract`, `pre_v002_ml_dataset_builder`,
  `pre_v002_ml_dataset_proof`) as its contract surface;
- use the Phase 4bn-AA split artefact (`pre_v002_split_policy.py`) as the sole
  split authority;
- bind the Phase 4bn-AC source contract and the Phase 4bn-AE amendment-001;
- be a **new pre-v002-specific data-reading module** — not a wrap/copy/reuse of
  the v002-terminal loader `ml_baseline_dataset_v002.py`;
- validate source scope before reading (§15);
- validate the manifest / config / gate-report hashes before reading any
  feature/label data (§16);
- run the Phase 4bn-L budget preflight before **any** write and fail closed on
  breach (§17);
- perform **no writes** before all pre-write checks pass (§16, §17);
- read only the pre-v002 normalized / feature / label sources explicitly bound by
  Phase 4bn-AC; read **no** v002 terminal data; read **no** sealed test data;
  read **no** raw zip contents unless explicitly required and **separately
  authorized**;
- create **exactly one** local gitignored output namespace, if authorized:
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`;
- write only the authorized dataset artefacts / proof / sidecar defined by the
  future phase spec, and nowhere else;
- commit no data outputs;
- produce a machine-checkable leakage/split-integrity proof and a Phase 4bb-F
  canonical sidecar;
- preserve `test_rows_loaded = 0`;
- preserve all non-authorization flags for ML / diagnostics / strategy / signals
  / PnL / backtest / live / exchange-write (all `false`).

**The future builder MUST NOT:** train ML; score ML; generate predictions; run
diagnostics; create strategy signals; compute PnL; run backtests; tune
thresholds; use the internal holdout for model selection; touch the sealed test;
touch the v002 terminal; create a full-envelope dataset; acquire new data;
download archives; call endpoints; use authenticated / private APIs; use MCP /
Graphify / credentials; mutate existing published manifests unless separately
authorized; flip `research_eligible`; or mark anything ML-ready. (Full list §21,
§31.)

---

## 15. Required pre-read checks

Before reading **any** feature/label rows, the future builder must pass (using
the Phase 4bn-AF validators):

1. **Source-scope validation** (`validate_source_scope`): symbol = BTCUSDT;
   market = binance_usdm_futures; source_family = aggTrades; dates 2024-03-01 ..
   2024-11-30; partition counts = 275; row count = 400,001,695; and the danger
   flags (`contains_v002_terminal`, `contains_sealed_test`, `full_envelope`,
   `private_source`, `authenticated_source`, `external_source`) absent or falsey.
   Fail closed on any missing critical key or mismatch.
2. **Manifest / config / gate-report hash binding** (`validate_manifest_hashes`):
   normalized manifest `0e96ae37…` + gate `3452fd9d…` (25/25); feature manifest
   `4881eb87…` + `feature_config_hash 0726b41d…` + gate `db731d1b…` (27/27);
   label manifest `69746c88…` (sidecar `636a4c1a…`) + `label_config_hash
   b3bd5d2b…` + gate `ffb5b092…` (sidecar `68dd5b57…`) (40/40). **Reject** the
   published v002-terminal hashes `819cfa7a…` / `352bad41…` by full value and
   prefix. Fail closed on any mismatch or missing critical hash.
3. **Per-Parquet hash verification against the canonical `.sha256` sidecar and
   the manifest `per_day_outputs` inventory**, before reading any rows.
4. **Partition discovery**: exactly 275 feature partitions and 275 label
   partitions from the manifest references; fail closed on any other count.
5. **Split authority binding**: import `pre_v002_split_policy.py`; confirm
   `SPLIT_POLICY_NAME = CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`
   and record its module path + commit SHA for the proof.

Any forbidden source (v002 terminal, sealed test, full envelope, non-BTCUSDT,
newly acquired, raw zip, external / private / authenticated) must **fail closed**
before any read.

---

## 16. Required pre-write checks

Before writing **anything**, the future builder must pass, in the Phase 4bn-AC
§17 execution order:

1. all §15 pre-read checks (source scope; manifest/hash/gate binding; per-Parquet
   hash verification; 275/275 partitions; split authority);
2. **feature/label pairing by UTC date** and **strict positional alignment**
   (`assert_strict_alignment` over `row_index`, `agg_trade_id`,
   `feature_timestamp_ms`, `source_transact_time_ms`, and `symbol` / `utc_date`
   where present) — no join repair / reorder / fill / tolerance merge / heuristic
   dedup; fail closed on any key mismatch;
3. **split assignment** by `source_transact_time_ms` UTC date via the artefact;
   **drop embargo** dates/rows; apply the **per-horizon earlier-split
   boundary-crossing** exclusion (`validate_no_boundary_crossing`);
4. **target filtering** (`filter_targets`): drop null direction, null log-return
   (where the schema requires), censored (`horizon_censored_flag_15s`), and
   invalid-price rows (`label_invalid_price_flag`); **never impute**; record
   dropped counts by split and reason;
5. **model-matrix construction from exactly the 45 allowed feature columns**
   (`validate_feature_allowlist`), plus a **forbidden-column substring scan**
   (`scan_forbidden_columns` / `assert_no_forbidden_columns`) that must be empty;
6. **train-only transform planning** (`plan_train_only_transform`): fit
   standardization/imputation statistics on the `train` split only; fail closed
   on any non-train fit split;
7. **budget preflight** (§17) must **pass**; the builder must fail closed on any
   breach and perform **no write** if it fails;
8. **assemble the leakage/split-integrity proof** (§18) and validate it
   (`validate_dataset_builder_proof`) before any output is committed to disk.

Only after all of the above pass may the builder write to the single authorized
gitignored namespace (§20).

---

## 17. Required budget preflight

The future builder must run the **Phase 4bn-L** derived-stack storage budget
preflight **before any output write** and **fail closed** on any breach. Exact
thresholds (Phase 4bn-AC §20, Phase 4bn-AD §22, and the Phase 4bn-AF proof
module `BudgetPreflightPlaceholder`, which echoes them verbatim):

- **derived footprint:** warn **75 GiB** / hard **125 GiB**;
- **total derived-stack:** warn **250 GiB** / hard **300 GiB**;
- **runtime:** warn **4 h** / hard **8 h**;
- **temp:** warn **50 GiB** / hard **100 GiB**;
- **`D:` free space ≥ 500 GiB before start**;
- **fail closed below 350 GiB free during execution.**

The builder must **record** the budget-preflight result in its proof / run
manifest. No output may be written without a passing, recorded preflight. In the
future builder these thresholds are **measured against real disk / runtime**
(unlike the skeleton's `BudgetPreflightPlaceholder`, which is interface-shape
only and measures nothing).

---

## 18. Required leakage / split-integrity proof

The future builder must emit a **machine-checkable** leakage / split-integrity
proof (JSON, with a Phase 4bb-F canonical sidecar), covering at least (Phase
4bn-AC §19, Phase 4bn-AD §21, and the Phase 4bn-AF proof schema):

- split-policy name `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`;
- split-policy **module path** and **commit SHA**;
- date-assignment counts **214 / 1 / 45 / 1 / 14**;
- no missing in-segment dates; no duplicate in-segment dates; no multi-assigned
  in-segment dates;
- no `EMBARGO` rows used for train / validation / holdout;
- **zero** out-of-segment dates;
- `v002_terminal_window_read = false`; `sealed_test_split_touched = false`;
  `test_rows_loaded = 0`;
- no random; no shuffle; no k-fold; no bootstrap; deterministic assignment by
  `source_transact_time_ms` UTC date;
- per-horizon **zero** earlier-split boundary-crossing rows;
- strict feature/label **key-alignment counts**;
- target null / censored / invalid **rows dropped, by split and reason**;
- active **45-column feature-list hash** (in canonical order);
- **forbidden-column scan** result (empty);
- **train-only transform provenance** (which split the statistics came from, the
  rule, epsilon `1e-8`, fill value `0.0`, booleans unstandardized);
- **budget-preflight result** (§17);
- **metric registry present** (21 mandatory metrics);
- **date/month block reporting schema present** (aggregate / utc_month / utc_date
  granularities);
- **dependence caveat present** (row-level metrics descriptive-only; per-row
  significance forbidden; decimation stride `None` / `reserved_not_adopted`);
- **calibration schema present** (confidence bins, high-confidence-tail size /
  accuracy, beats-majority booleans);
- **cost descriptive fields present** (8/16 bps locks; share of |15s move| > 16
  bps; descriptive only);
- **success / kill constants present** (+2.0 pp accuracy over both floors; +1.0
  pp balanced accuracy; +0.03 macro-F1; majority-of-blocks; holdout-no-sign-
  reversal; calibration-tail rule);
- **non-authorization flags all `false`** for ML / diagnostics / strategy /
  signals / PnL / backtest / live / exchange-write;
- **output namespace created exactly once** if authorized;
- **no outputs outside the authorized namespace.**

The proof must be validated by `validate_dataset_builder_proof`, which fails
closed on wrong split counts, `test_rows_loaded ≠ 0`, v002/sealed access, a
non-empty forbidden scan, missing metrics/granularities, imputed targets, a
non-placeholder-but-failing budget preflight, any True non-authorization flag, or
a created-but-unexpected output namespace.

---

## 19. Required sidecar / metadata policy

- Every future output artefact must carry a **Phase 4bb-F canonical sidecar** (a
  two-space `.sha256` sidecar) in the same directory as the artefact.
- The leakage/split-integrity proof (§18) is itself an artefact and must carry
  its canonical sidecar.
- A local dataset manifest / metadata file for the dataset may be written **if
  and only if** the future phase spec explicitly defines it; it, too, carries a
  canonical sidecar.
- All sidecars and metadata are **local and gitignored** under `data/research/`;
  none are committed.
- Sidecars/metadata must **not** imply research eligibility, must **not** set
  `chronological_split_policy` in any source manifest, and must **not** transition
  `ml_authorized` / `diagnostics_authorized`.

---

## 20. Authorized future output namespace, if separately authorized

If — and only if — the future builder phase (Phase 4bn-AH) is separately
authorized to create outputs, it may create **exactly one** local gitignored
output namespace:

`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`

Within that namespace it may write, at most:

- the authorized **dataset artefact(s)** defined by the future builder spec;
- the machine-checkable **leakage/split-integrity proof** (§18);
- the **Phase 4bb-F canonical sidecar** for every artefact;
- a **local dataset manifest / metadata** file, **if and only if** the future
  phase spec defines it (§19).

This namespace is **not** created, written, or committed by this memo. It is
gitignored under `.gitignore:88` (`data/research/`). Nothing is written outside
it.

---

## 21. Forbidden future outputs

The future builder must **not** create:

- model files; predictions; diagnostics outputs;
- research matrices beyond the authorized dataset (unless explicitly authorized);
- backtest outputs; strategy outputs; PnL reports;
- a v003 dataset; compacted Parquet; database files (`.duckdb` / `.sqlite`);
- any output under `data/microstructure/` (unless explicitly authorized);
- any **committed** data file;
- any output outside
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`;
- a split file, research matrix, ML config, source-manifest, or gate report that
  mutates or replaces any existing published artefact.

---

## 22. One-time run / rerun posture

The future data-reading builder should be a **single controlled run**, not an
open-ended or scheduled process. If the run fails, a **failure closeout /
recovery memo** is required before any rerun. Any rerun must be **separately
authorized** unless the future phase spec explicitly defines safe, idempotent
rerun behaviour (e.g. deterministic overwrite of the single namespace with a
fresh proof and preflight, no accumulation, no partial-state reuse). The default
is: one run, then stop and report.

---

## 23. Future validation requirements

The future builder phase should run:

- **targeted offline tests** for the new data-reading builder code (including
  synthetic-fixture tests for the new I/O boundary and its fail-closed guards);
- the existing **97 Phase 4bn-AF skeleton tests** (must remain green);
- **ruff**;
- **mypy**, clearly distinguishing any new errors from the pre-existing sibling
  errors (the 29-error set reproduced by `mypy pre_v002_split_policy.py` on a
  committed module);
- the **budget preflight** (real, over real disk/runtime);
- **hash / gate validation** (§15, §16);
- a **no-sealed / no-v002 proof** (`v002_terminal_window_read = false`;
  `sealed_test_split_touched = false`; `test_rows_loaded = 0`);
- a **no-output-outside-namespace proof**;
- `git status` (only the intended tracked code/docs; data outputs untracked);
- `git check-ignore -v data/microstructure/` (`.gitignore:85`) and
  `git check-ignore -v data/research/` (`.gitignore:88`).

---

## 24. Current-state consolidation assessment

`docs/00-meta/current-project-state.md` is large (~2.8 MB) and partially stale (a
tail dated 2026-04-29; phase blocks inserted mid-file), as the Phase 4bn-AE
external review flagged and Phase 4bn-AF §30 / its merge-closeout §16 noted. A
**current-state consolidation memo** — freezing the current doc and publishing a
compact authoritative current-state document — is **strongly recommended** as a
near-term parallel docs-only option.

**Assessment: consolidation is NOT a blocker for the future data-reading builder,
and this memo keeps it non-blocking.** Reasoning: this authorization memo, and
the future builder, both derive their authority and their bindings from
**committed reports and committed source** (the AC/AD/AE/AF reports, the AA split
artefact, the passed layer gates, the manifest/config/gate hashes), **not** from
`current-project-state.md`. The state doc is a navigational summary, not the
binding source of truth for any hash, gate, split window, or non-authorization
flag. Its staleness does not weaken any gate, hash, proof, or budget threshold
the future builder binds to. Consolidation would improve navigability and reduce
append pressure, but it is orthogonal to data-read safety. The memo therefore
does **not** elevate it to a blocker (which would select result state 2), while
recommending it as a parallel next step (§26, §34).

---

## 25. Candidate next phases considered

1. **Phase 4bn-AH — data-reading ML dataset builder implementation + single run**
   (code + controlled local data read + local gitignored output), subject to
   separate operator authorization. **Selected recommendation** (§26): all four
   governance prerequisites are complete on `main`; the skeleton is passing; the
   budget thresholds and leakage-proof schema are specified; the only missing
   elements are the builder implementation and its separate authorization.
2. **Current-state consolidation memo** (docs-only). Strongly recommended
   **parallel** option; not a blocker (§24).
3. **Additional skeleton hardening** (code). **Not required**: the skeleton is
   complete and passing with no-data-I/O and no-output-namespace proofs; the
   remaining work (real proof over real data, real preflight) is *builder* work,
   not skeleton hardening.
4. **Source-admissibility gate artefact** (code). **Not required** (Phase 4bn-AB
   §21(B) rejected it; the builder flips no eligibility and touches only
   gitignored data).
5. **Budget-preflight design memo** (docs-only). **Not required**: the thresholds
   are already fully specified (Phase 4bn-L; AC §20; AD §22; AF proof module).
6. **Full-envelope reference-assembly memo** — only if a future path combines
   pre-v002 + v002; **not required** for the conservative pre-v002-only path.
7. **Holdout-boundary memo** — only if a future scope touches the v002 terminal or
   sealed-test dates; **not required** here.
8. **Close the ML-baseline arc.** Defensible but premature: a clear, low-risk,
   pre-registered next step exists (the single builder run then descriptive
   diagnostics then one fixed baseline run then arc-decision).

---

## 26. Selected next recommendation

**Recommend authorizing a data-reading ML dataset builder implementation + single
run (Phase 4bn-AH), subject to separate operator authorization.** The builder
must import the Phase 4bn-AF skeleton, bind the Phase 4bn-AC contract and Phase
4bn-AE amendment, use the Phase 4bn-AA split artefact, validate source scope and
manifest/config/gate hashes before reading (§15), run the Phase 4bn-L budget
preflight and fail closed before any write (§16, §17), emit a machine-checkable
leakage/split-integrity proof and Phase 4bb-F sidecars (§18, §19), create the
single authorized gitignored namespace (§20), write nothing forbidden (§21),
preserve `test_rows_loaded = 0` and all non-authorization flags, and run exactly
once (§22).

A **current-state consolidation memo** is **also recommended** as a near-term
parallel docs-only phase (§24); either order is acceptable and it is not a
blocker.

**No successor is authorized from inside Phase 4bn-AG.** This memo *recommends*
Phase 4bn-AH; it does not authorize it. Phase 4bn-AH requires a separate,
precisely-scoped operator authorization prompt after this branch is reviewed and
merged.

---

## 27. Remaining blockers before future builder run

Before the future data-reading builder (Phase 4bn-AH) may run:

1. this authorization memo recorded (**this phase**); **and**
2. a **code-level data-reading builder** implemented, importing the Phase 4bn-AF
   skeleton and binding the passed gates (`3452fd9d…` / `db731d1b…` / `ffb5b09…`),
   the manifests/hashes, and the Phase 4bn-AA split artefact; **and**
3. a real **leakage/split-integrity proof** (§18) and a real **Phase 4bn-L budget
   preflight** (§17) bound into the builder and passing; **and**
4. **separate operator authorization** for the builder implementation + single
   run (`source_admissible_for_data_read` and
   `source_admissible_for_dataset_builder` both currently **false**, transitioned
   only in that future phase under separate authorization).

---

## 28. Remaining blockers before ML dataset can be used for diagnostics

Before the produced pre-v002 ML dataset may feed **descriptive diagnostics**
(Phase 4bn-AI, no models):

1. all of §27 (the dataset must exist, built under a passing preflight + proof);
   **and**
2. a **separate diagnostics authorization** (`diagnostics_authorized = false`);
   **and**
3. a pre-declared diagnostics scope (class balance; label-overlap / effective-
   sample statistics; `forward_log_return_15s` distribution vs the 16 bps lock;
   per-month regime slices) that **trains no model, scores nothing, and generates
   no predictions**.

Diagnostics are descriptive only and are separately authorized; the dataset's
existence does not authorize them.

---

## 29. Remaining blockers before ML training

Before any ML training on the pre-v002 path:

1. all of §27 and §28; **and**
2. the per-task target / horizon / filtering locked by contract
   (`forward_direction_15s`, 15s, 3-class signed — done, Phase 4bn-AC) **and the
   evaluation / dependence / success-kill layer pre-registered (Phase 4bn-AE,
   done) and encoded (Phase 4bn-AF, done)**; **and**
3. a committed **end-to-end pre-v002 trainer** (does **not** exist; the only
   committed ML-baseline stack is v002-terminal-bound and inadmissible to
   pre-v002); **and**
4. a **separate ML authorization** (`ml_authorized = false`); training remains a
   later, separately-authorized phase (Phase 4bn-AJ fixed baseline run) even
   after 1–3.

---

## 30. Strategy / PnL / backtest hard boundary

**No result of any pre-v002 baseline, however strong, authorizes** strategy
construction, signal generation, threshold / confidence-gated trading,
backtesting, PnL computation, position sizing, execution logic, live-readiness,
paper / shadow trading, or exchange-write. This boundary (Phase 4bn-AE §19) is
**absolute** and is not softened by any dataset, diagnostic, or baseline metric.
Any path toward those requires a **separate future M0-style
mechanism-admissibility memo** (Phase 4ak M0 twelve-clause gate) clearing at
minimum: **M0.5 cost realism** at the locked **8 bps/side · 16 bps round-trip**;
execution feasibility; slippage / spread assumptions (which aggTrades-only data
cannot currently support — mid-price / book data would be required); **label
economic relevance** (the 15s strict-sign target is explicitly non-economic);
strategy admissibility against the retained rejections (R2 / F1 / D1-A / V2 / G1
/ C1) and the M0 §7.D microstructure-lane `NOT_RECOMMENDED_NOW` posture; and the
Phase 4al no-rescue constraints.

---

## 31. Explicit non-authorizations

Phase 4bn-AG does **not**, and does not authorize anyone to: implement or run a
data-reading builder; read or create any local data; inspect any file under
`data/microstructure/` or `data/research/`; inspect any raw zip / normalized /
feature / label Parquet / manifest / gate report / sidecar; read the v002
terminal window; touch the sealed v002 test split (`test_rows_loaded = 0`); create
the future output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`; create a
split file / research matrix / ML dataset / ML config / manifest / sidecar / gate
report; mutate any manifest / sidecar / gate report / successor-state artefact;
flip `research_eligible`; transition `eligibility_gate_status` /
`chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`;
transition `source_admissible_for_data_read` or
`source_admissible_for_dataset_builder`; invoke or alter the Phase 4aw
`flip_research_eligible(...)` always-raises invariant; train / score / predict;
run diagnostics / strategy / signals / PnL / backtests; acquire data; call any
public / authenticated / private endpoint; download any archive / CHECKSUM; run a
HEAD preflight; rerun any acquisition / raw / normalization / feature / label
execution or any layer gate; create a database / `.duckdb` / `.sqlite`; compact
Parquet; migrate storage; create v003; create or commit any `data/microstructure`
or `data/research` artefact; use credentials / `.env` / `.mcp.json` / MCP /
Graphify; open any WebSocket / user stream; authorize Phase 5, paper / shadow,
live-readiness, deployment, exchange-write, production keys, or any successor
phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread /
V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side; round-trip = 16 bps;
§1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j
§11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause
gate + post-null cooldown; Phase 4al refined no-rescue rule; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F
canonical path + sidecar policy; Phase 4bl-F risk tiers; Phase 4bm-U / 4bm-W v002
split policy; Phase 4bn-J-R1 raw-only cap amendment; Phase 4bn-L derived-stack
storage budget; Phase 4bn-N normalization manifest/versioning; Phase 4bn-R feature
manifest/versioning; Phase 4bn-V label manifest/versioning; Phase 4bn-Y
chronological split/holdout policy; Phase 4bn-Z ML-baseline readiness memo; Phase
4bn-AA pre-v002 split-policy artefact; Phase 4bn-AB source-admissibility posture;
Phase 4bn-AC ML dataset contract; Phase 4bn-AD builder-readiness verdict; Phase
4bn-AE pre-registration amendment; Phase 4bn-AF code-only skeleton) is preserved
verbatim. Phase 4 canonical remains unauthorized.

---

## 32. Result state

`DATA_READING_BUILDER_AUTHORIZATION_MEMO_RECORDED__BUILDER_RUN_RECOMMENDED__NO_DATA_READ__REMAIN_PAUSED`

The data-reading builder authorization memo is recorded; a future data-reading
builder implementation + single run (Phase 4bn-AH) is **recommended** subject to
separate operator authorization; no data was read; no data was created; no output
namespace was created; no manifest field was set;
`source_admissible_for_data_read` and `source_admissible_for_dataset_builder`
remain **false**; `ml_authorized` / `diagnostics_authorized` /
`strategy_backtest_authorized` remain **false**; manifest state is unchanged;
remain paused.

---

## 33. Decision

`RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_IMPLEMENTATION_AND_SINGLE_RUN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`

Rationale: the Phase 4bn-AC contract, the Phase 4bn-AD readiness decision, the
Phase 4bn-AE pre-registration amendment, and the passing Phase 4bn-AF code-only
skeleton (97 synthetic tests) together make the project ready to **recommend** a
future data-reading builder implementation + single run under the strict gates in
§14–§23. No blocker was found that should force current-state consolidation
first, additional skeleton hardening, a separate source-admissibility gate, a
budget-preflight design memo, or remaining paused. This memo does **not**
authorize the successor; Phase 4bn-AH requires separate operator authorization.

---

## 34. Recommended state and successor options

**Recommended state: remain paused. No next phase authorized by this memo.**

Operator options (each subject to separate authorization after the
branch-complete report):

- remain paused;
- request a merge prompt for Phase 4bn-AG;
- separately authorize a **data-reading ML dataset builder implementation + single
  run** (recommended; Phase 4bn-AH);
- separately authorize a **current-state consolidation memo** (recommended
  near-term parallel docs-only option);
- separately authorize **additional skeleton hardening** (not required);
- separately authorize a **source-admissibility gate artefact** (not required);
- separately authorize a **budget-preflight design memo** (not required);
- separately authorize a **full-envelope reference-assembly memo** only if a
  future path combines pre-v002 + v002 data;
- separately authorize a **holdout-boundary memo** only if a future scope touches
  the v002 terminal or sealed-test dates;
- reject further ML-baseline successors and **close the ML arc**.

No data-reading builder implementation/run / ML / diagnostics / strategy / PnL /
backtest / storage-migration / database / Parquet-compaction / v003 / paper /
shadow / live / exchange-write option is valid from this state unless separately
authorized after this branch is merged.

---

## 35. Current-project-state update summary

`docs/00-meta/current-project-state.md` is amended **additively only**: one new
Phase 4bn-AG paragraph appended after the Phase 4bn-AF paragraph, and one new
`Current phase:` block inserted ahead of the Phase 4bn-AF block. All prior content
(Phase 4bn-A … 4bn-AF paragraphs and blocks, every retained verdict and project
lock) is preserved verbatim. No manifest field, eligibility flag, split-policy
field, or admissibility manifest field is set. The update records:
data-reading builder authorization memo recorded; data-read authorization
**recommended** (not granted); dataset-builder implementation + single run
**recommended** (not granted); manifest-transition posture (no mutation;
`source_admissible_for_data_read` / `source_admissible_for_dataset_builder` remain
false; `data_read_authorization_recommended = true` /
`builder_implementation_run_recommended = true` as docs-level posture only);
future builder re-lettered to Phase 4bn-AH with the arc shifted by one letter
(AH builder run → AI diagnostics → AJ baseline run → AK arc-decision, subject to
operator re-lettering); required pre-read / pre-write checks; Phase 4bn-L budget
preflight (75/125 GiB derived; 250/300 GiB total; 4/8 h; 50/100 GiB temp; ≥ 500
GiB before, fail closed < 350 GiB during); leakage / split-integrity proof
requirements; Phase 4bb-F sidecar policy; single authorized output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`; forbidden
outputs; one-time run / rerun-requires-authorization posture; future validation
requirements; current-state consolidation non-blocking but recommended; result
`DATA_READING_BUILDER_AUTHORIZATION_MEMO_RECORDED__BUILDER_RUN_RECOMMENDED__NO_DATA_READ__REMAIN_PAUSED`;
decision
`RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_IMPLEMENTATION_AND_SINGLE_RUN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
remain paused; no successor authorized.
