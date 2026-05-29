# Phase 4bn-F — V002 Data-Sufficiency / Representativeness Scoping Memo

**Phase identity:** Phase 4bn-F — V002 Data-Sufficiency / Representativeness
Scoping Memo (docs-only / design-only / scoping-only governance memo; Tier 1
— Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3;
the separately authorized scoping phase that addresses the standing future
data-sufficiency / representativeness concern that Phase 4bn-E recorded as a
non-authorizing note).
**Date:** 2026-05-29.
**Branch:** `phase-4bn-f/v002-data-sufficiency-representativeness-scoping`.
**Base SHA:** `main` at `8fa219c83326c79ffb6406cc1904440fdc63c376` (Phase
4bn-E SHA-finalization commit `docs(phase-4bn-e): finalize merge closeout
shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3. Phase 4bn-F is
adjacent to ML-baseline downstream admissibility, possible future data
acquisition, possible future v003 / longer-history planning, possible future
storage architecture decisions, and possible future regime / outlier
interpretation, while explicitly authorizing none of them.
**Phase type:** docs-only / design-only / scoping-only. Adds two new tracked
docs files under `docs/00-meta/implementation-reports/` (this memo + the
paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`.
**No** source / test / committed-script / configuration / manifest / sidecar
/ gate-report / successor-state mutation. **No** local data artefact created
or mutated. **No** diagnostic rerun. **No** ML rerun. **No** ML artefact.
**No** acquisition. **No** storage migration. **No** database creation. **No**
Parquet compaction. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this
work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bn-F is a docs-only / design-only / scoping-only v002
  data-sufficiency / representativeness scoping memo.**
- **Phase 4bn-F does not acquire data.**
- **Phase 4bn-F does not run diagnostics.**
- **Phase 4bn-F does not run ML.**
- **Phase 4bn-F does not train models.**
- **Phase 4bn-F does not score models.**
- **Phase 4bn-F does not generate predictions.**
- **Phase 4bn-F does not inspect the test holdout.**
- **Phase 4bn-F does not use the sealed test split.**
- **Phase 4bn-F does not rank features.**
- **Phase 4bn-F does not select features.**
- **Phase 4bn-F does not prune features.**
- **Phase 4bn-F does not engineer features.**
- **Phase 4bn-F does not tune hyperparameters.**
- **Phase 4bn-F does not tune thresholds.**
- **Phase 4bn-F does not fit calibrators.**
- **Phase 4bn-F does not run strategy research.**
- **Phase 4bn-F does not define a strategy.**
- **Phase 4bn-F does not generate trade signals.**
- **Phase 4bn-F does not simulate PnL.**
- **Phase 4bn-F does not run backtests.**
- **Phase 4bn-F does not authorize acquisition.**
- **Phase 4bn-F does not authorize storage migration.**
- **Phase 4bn-F does not create a v003 dataset.**
- **Phase 4bn-F does not create a database.**
- **Phase 4bn-F does not compact Parquet.**
- **Phase 4bn-F does not modify dataset layout.**
- **Phase 4bn-F does not call any public, authenticated, or private endpoint.**
- **Phase 4bn-F does not open any WebSocket or user stream.**
- **Phase 4bn-F does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.**
- **Phase 4bn-F does not mutate any manifest.**
- **Phase 4bn-F does not mutate any successor-state artefact.**
- **Phase 4bn-F does not commit `data/microstructure`.**
- **Phase 4bn-F does not commit `data/research`.**
- **Phase 4bn-F does not authorize Phase 4bn-G, Phase 5, paper / shadow,
  live-readiness, deployment, exchange-write, production keys, or any
  successor phase.**
- **Recommended state remains paused.**

---

## 1. Purpose

Phase 4bn-F answers a single governance / scoping question:

> Given that Phase 4bn-A through Phase 4bn-E established the first ML-baseline
> evidence on a 90-day v002 microstructure envelope and recommended that the
> project remain paused, is the current 3-month v002 window sufficient as a
> basis for interpreting that ML-baseline evidence, or should the project
> first define a separate future data-sufficiency / representativeness and
> storage-scaling plan before any further ML expansion, acquisition, or
> storage architecture change?

Phase 4bn-F is **docs-only / design-only / scoping-only**. It reads only
committed repository Markdown reports and committed architecture documents
as its evidence base. It opens no local gitignored `data/research/` outputs.
It opens no local gitignored `data/microstructure/` datasets. It reads no
local parquet, CSV, or JSON output. It calls no endpoint. It uses no
credentials. It mutates no manifest, sidecar, gate report, or successor-state
artefact. It trains nothing, scores nothing, predicts nothing, evaluates
nothing on test data, selects nothing, ranks nothing, tunes nothing, runs
nothing, materializes no artefact, acquires no data, designs no storage
migration, creates no database, compacts no Parquet, and authorizes no
successor implementation. **Phase 4bn-F is the governance-level data-
sufficiency / representativeness scoping memo, not data acquisition.**

This memo:

- carries the Phase 4bn-E descriptive train-vs-validation feature drift
  result forward verbatim as the most recent measurement-frame evidence;
- carries the Phase 4bn-D bounded ML-baseline expansion scoping decision
  forward verbatim as the immediate-predecessor design boundary;
- carries the Phase 4bn-C corrected interpretation of Phase 4bn-B ML-baseline
  evidence forward verbatim as the binding factual frame for any
  data-sufficiency claim;
- enumerates what the current 90-day v002 evidence can support and what it
  cannot;
- defines a representativeness / outlier-risk framework that any future
  separately authorized data-expansion phase would have to satisfy before
  any acquisition;
- enumerates seven candidate future data-expansion options at design level
  only, with per-option what-it-answers / what-it-requires-later /
  what-it-risks / what-it-does-not-authorize-now classification;
- discusses storage-scaling questions at design level only, with explicit
  Parquet / compacted Parquet / DuckDB / database tradeoffs that any future
  separately authorized storage-architecture memo would have to address
  before any acquisition or storage migration;
- records a single scoping decision under the operator-supplied decision
  taxonomy and, if a successor is recommended, frames it as a recommendation
  only requiring separate operator authorization.

## 2. Authority and repository state

- **Repository:** Prometheus (`https://github.com/jpedrocY/Prometheus`).
- **Active machine:** Desktop.
- **Local repo path:** `C:\Prometheus`.
- **Claude Code lightweight workspace:** `C:\ClaudeRuns\prometheus-light`
  (Phase 4bm-D-P1 lightweight workspace standard preserved).
- **Authority documents read for this memo (committed repository Markdown
  only):**
  - `docs/00-meta/current-project-state.md` (current high-level project
    state).
  - `docs/00-meta/process/phase-workflow-standard.md` (eleven-step phase
    lifecycle).
  - `docs/00-meta/process/phase-risk-tiering-standard.md` (Phase 4bl-F
    four-tier risk model, R-SIDECAR-CRLF standing rule, nine reusable
    non-authorization blocks).
  - `docs/00-meta/process/phase-prompt-template.md` (authorization-prompt
    structure standard).
  - `docs/00-meta/process/operator-report-standard.md` (Claude Code compact
    report + ChatGPT operator-facing response standard).
  - `docs/00-meta/process/merge-closeout-standard.md` (merge-closeout
    16-section structure).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-e_merge-closeout.md`
    (Phase 4bn-E merge-closeout;
    `LOCAL ARTEFACT PRODUCED — RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-e_train-validation-feature-drift-diagnostics.md`
    (Phase 4bn-E implementation report).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-e_closeout.md`
    (Phase 4bn-E closeout).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_merge-closeout.md`
    (Phase 4bn-D merge-closeout).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_bounded-ml-baseline-expansion-scoping.md`
    (Phase 4bn-D bounded ML-baseline expansion scoping memo).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_closeout.md`
    (Phase 4bn-D closeout).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_merge-closeout.md`
    (Phase 4bn-C merge-closeout).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_ml-baseline-evidence-interpretation-memo.md`
    (Phase 4bn-C interpretation memo).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_closeout.md`
    (Phase 4bn-C closeout).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_merge-closeout.md`
    (Phase 4bn-B merge-closeout; `RECORD_EVIDENCE_ONLY`).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_multi-day-v002-ml-baseline-implementation.md`
    (Phase 4bn-B implementation report).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_closeout.md`
    (Phase 4bn-B closeout).
  - `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_merge-closeout.md`
    (Phase 4bn-A merge-closeout;
    `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`).
  - `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_ml-baseline-implementation-scoping-design.md`
    (Phase 4bn-A scoping / design memo).
  - `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_closeout.md`
    (Phase 4bn-A closeout).
  - `docs/04-data/data-requirements.md` (high-level data requirements index).
  - `docs/04-data/historical-data-spec.md` (canonical historical-data
    contract).
  - `docs/04-data/timestamp-policy.md` (timestamp-handling rules; read for
    context only; no rule restated).
  - `docs/04-data/dataset-versioning.md` (dataset-versioning policy;
    Parquet-first / DuckDB query-engine; mandatory bump conditions).
  - `docs/08-architecture/database-design.md` (runtime database design
    document; read to surface the explicit historical-vs-runtime separation
    and the runtime-database "safety system" framing).
- **Inputs explicitly NOT used:** local gitignored
  `data/research/microstructure/ml-baselines/phase-4bn-b/` outputs (Phase
  4bn-B local artefacts); local gitignored
  `data/research/microstructure/ml-baselines/phase-4bn-e/` outputs (Phase
  4bn-E local artefacts); local gitignored Phase 4bm-W / Phase 4bm-Q /
  Phase 4bm-S / Phase 4bm-U / Phase 4bm-X artefacts; local
  `data/microstructure/` raw / normalized / feature / label parquets; local
  Phase 4bn-B / Phase 4bn-E descriptive CSV / JSON outputs. Phase 4bn-F
  treats every prior phase's committed Markdown record (implementation
  report, closeout, merge-closeout) as the authoritative summary of those
  phases' evidence; no re-hashing or re-reading of any local data file is
  performed in this docs-only / design-only / scoping-only phase.
- **README:** README may be stale and is **not** used as current-state
  authority. The authority is `docs/00-meta/current-project-state.md` plus
  the most recent merge-closeout, plus the most recent implementation
  reports (per `docs/00-meta/process/phase-workflow-standard.md` "Repo-query
  requirement for new chats").
- **Pre-branch verification:**
  `git rev-parse main == git rev-parse origin/main == 8fa219c83326c79ffb6406cc1904440fdc63c376`.
  Phase 4bn-E merge-closeout commit `0ce98d361c8614c1ebdbfae8f7a9eabf9f4fe07c`,
  Phase 4bn-E merge commit `9a6e9aceffc6ecac06556e7113851ab713cf2829`, and
  Phase 4bn-E branch commit `b1a84d0f4454d1c1aaa33ad442fbd6509138956f`
  present on `main` immediately below the SHA-finalization commit. Phase
  4bn-D SHA-finalization commit `254cdacfdfebf37ab9f56fb9b7c0a79ce9d92f84`
  present below that. Predecessor chain
  (Phase 4bn-A → 4bn-B → 4bn-C → 4bn-D → 4bn-E) is fully merge-complete on
  `main`.

## 3. Phase type and strict scope

Phase 4bn-F is **docs-only / design-only / scoping-only**.

**Allowed surface (tracked files added or modified):**

- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_v002-data-sufficiency-representativeness-scoping.md`
  (this memo; new).
- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_closeout.md`
  (closeout; new).
- `docs/00-meta/current-project-state.md` (narrow current-phase paragraph +
  Current-phase block addition; prior Phase 4bn-A / 4bn-B / 4bn-C / 4bn-D /
  4bn-E history preserved as labelled historical context).

**Forbidden surface (verbatim):**

- No source code modification.
- No test modification.
- No committed-script modification.
- No `pyproject.toml`, `README.md`, `.gitignore`, or MCP file modification.
- No `data/microstructure/` artefact created, modified, or committed.
- No `data/research/` artefact created, modified, or committed.
- No manifest, sidecar, gate-report, or successor-state artefact created,
  modified, or accessed for mutation.
- No ML model trained, scored, evaluated, persisted, or referenced for
  selection.
- No row-level prediction generated or persisted.
- No reusable split mask generated or persisted.
- No feature ranked, selected, pruned, or engineered.
- No hyperparameter or threshold tuned.
- No calibrator fitted.
- No strategy defined, designed, or run.
- No trade signal generated.
- No PnL simulated.
- No backtest run.
- No diagnostics rerun.
- No Phase 4bn-B / 4bn-E rerun.
- No data acquired.
- No v003 dataset created.
- No longer-history dataset created.
- No additional symbols loaded.
- No additional horizons created.
- No mark-price, spot, cross-venue, or order-book data acquired.
- No aggTrades acquired.
- No local parquet reads.
- No local `data/research/` reads.
- No local `data/microstructure/` reads.
- No public, authenticated, or private endpoint called.
- No WebSocket or user stream opened.
- No credential, `.env`, `.mcp.json`, MCP, or Graphify use.
- No storage migration.
- No database creation.
- No Parquet compaction.
- No DuckDB database file creation.
- No SQLite database creation.
- No dataset-layout modification.
- No retained verdict revised.
- No project lock loosened.
- No M0 amendment.
- No `research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`, `diagnostics_authorized`, or `ml_authorized`
  transition on any actual manifest.
- No successor authorized.

The non-authorization wording above subsumes the reusable Phase 4bl-F §7
blocks **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**,
**N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**,
**N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, and **N-VERDICT-LOCK**; each
block applies in full to Phase 4bn-F.

## 4. Evidence base and input boundary

Phase 4bn-F reads, read-only, the committed repository Markdown documents
enumerated in §2. It reads no local gitignored artefact. It re-hashes no
local file. It does not invoke any normalizer, gate runner, label kernel,
feature kernel, ML runner, diagnostic runner, backtest runner, simulator,
or acquisition runner. It does not call any acquisition script, does not
load any parquet or CSV from `data/microstructure/` or `data/research/`,
does not call `ml_baseline_runner.run(...)`, does not call
`run_feature_drift_v002(...)`, and does not call any helper that touches
the local data surface. The Phase 4bn-A through Phase 4bn-E merge-closeouts,
implementation reports, and closeouts are treated as the canonical,
sufficient evidence record for the ML-baseline arc; this is the explicit
guarantee that Phase 4bn-F does not, and cannot, reach for the actual local
artefacts. The data architecture documents (`docs/04-data/*.md`,
`docs/08-architecture/database-design.md`) are read for design context only;
no rule, schema, or policy from those documents is rewritten by this memo.

This boundary is deliberate. It (a) protects the local artefacts from
accidental mutation, (b) keeps Phase 4bn-F fully reviewable from `main`
without any local state assumption, and (c) honours the
`phase-workflow-standard.md` rule that branch-complete reports must record
what was actually read so that audit is anchored to repository state rather
than to working-directory state.

## 5. Phase 4bn-E decision carried forward

The Phase 4bn-E implementation report and merge-closeout are the most
recent ML-arc evidence. Their key conclusions are carried forward verbatim
by Phase 4bn-F:

- **Phase 4bn-E decision (verbatim):**
  `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`.
- **Phase 4bn-E descriptive result (verbatim):** 45 v002 computed features
  analysed; 31 `low_descriptive_drift`, 13 `moderate_descriptive_drift`,
  0 `high_descriptive_drift`, 1 `undefined_due_to_zero_or_missing_train_std`
  (`invalid_window_flag`); highest absolute standardized mean delta observed
  0.330 (`rolling_quantity_mean_60s`; strictly below the fixed 0.50
  high-drift cut); highest absolute missing-rate delta ≈ 6e-06 (effectively
  zero); the 13 moderate-drift features cluster on *count* and *mean-quantity*
  dimensions, signed consistently (count up, mean quantity down) between the
  train window (2024-12-01 – 2025-01-14) and the validation window
  (2025-01-15 – 2025-02-13).
- **Phase 4bn-C H10 (feature-stationarity drift) partially ruled out at the
  measurement-frame level only:** no individual feature crosses the fixed
  0.50 high-drift cut; missing-rate deltas uniformly < 1e-5; *gross*
  feature-distribution drift is partially ruled out as the primary cause of
  the weak baseline-vs-prior separation; subtler distribution effects
  (joint feature drift, regime conditioning, second-moment drift beyond the
  std-ratio summary, drift in the feature-label relationship) are *not*
  addressed by Phase 4bn-E's measurement frame.
- **Phase 4bn-E does not authorize Phase 4bn-F, Phase 5, paper / shadow,
  live-readiness, deployment, exchange-write, or any successor phase.**
  Phase 4bn-F is the *separately authorized* scoping phase that the
  Phase 4bn-E recommendation made conditionally allowable as one of several
  equivalent operator options; the operator's separate authorization of
  Phase 4bn-F is recorded in the authorization prompt that produced this
  memo. The Phase 4bn-F authorization does not retrospectively elevate the
  Phase 4bn-E recommendation into anything more than a recommendation, and
  does not retrospectively transform the descriptive Phase 4bn-E drift
  result into a sufficiency / outlier verdict.

This memo defers to Phase 4bn-E on every factual descriptive interpretation
of the train-vs-validation feature drift result; Phase 4bn-F draws no new
descriptive conclusion about the Phase 4bn-E run and computes no metric.

## 6. Phase 4bn-D / 4bn-C / 4bn-B interpretation carried forward

The Phase 4bn-D bounded ML-baseline expansion scoping decision, the Phase
4bn-C corrected interpretation of Phase 4bn-B ML-baseline evidence, and the
Phase 4bn-B descriptive-only result are the binding factual frame for any
data-sufficiency claim discussed below. They are carried forward verbatim:

- **Phase 4bn-D scoping decision (verbatim):**
  `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-C interpretation decision (verbatim):**
  `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`.
- **Phase 4bn-B decision (verbatim):** `RECORD_EVIDENCE_ONLY`.
- **Phase 4bn-B descriptive evidence (verbatim summary):** the flat class
  is underrepresented at 0.15 – 1.09 % across both included horizons and
  both supervised splits; directional classes near-balanced (down ≈ up ≈
  0.495 ± 0.005); majority accuracy floor ~50 % (0.4938 at 15s; 0.4950 at
  60s); majority macro-F1 floor ~0.22; L2 / L1 linear lift ~+5 pp accuracy
  at 15s, ~+1.5 pp at 60s, ~+14 pp macro-F1 at 15s, ~+11 pp macro-F1 at
  60s; the flat class is never predicted by L2 / L1 (per-class P / R / F1
  = 0 / 0 / 0 on flat in every cell); persistence beats majority on hard
  accuracy (+2.3 pp at 15s, +0.2 pp at 60s) but is catastrophically worse
  on log-loss (~18× majority) and Brier (~2× majority) because it emits
  hard one-hot probabilities; L2 15s is well-calibrated in the dominant
  0.5 – 0.6 confidence bin (~86 % of validation rows; reliability gap
  −0.0047) but severely over-confident in the 0.6 – 1.0 tail (reliability
  gaps −0.061 to −0.392; in the 0.8 – 0.9 bin the empirical accuracy is
  0.4881, *below* the majority floor); §11.6 cost-commensurability fractions
  on validation: 15s 6.2 % > 1× / 1.6 % > 2× / 0.16 % > 5×; 60s 18.3 % > 1×
  / 5.8 % > 2× / 0.93 % > 5×; train-validation deltas small (~0.5 pp on
  hard metrics) — no overfitting at this measurement level; test holdout
  sealed (`test_rows_loaded: 0`).
- **A naive "trade when confidence is high" idea would fail under current
  evidence.** Statistical descriptive lift on a near-50 / 50 binary in a
  regime where 80 – 95 % of validation rows have absolute moves below the
  round-trip cost is not a tradability claim.
- **15s has stronger model signal but worse cost / tradability context; 60s
  has better cost context but weaker model signal.**
- **None of this is edge, profitability, tradability, strategy-readiness,
  or a signal.** **Phase 4bn-F inherits this boundary without softening it.**

## 7. What the current 3-month v002 evidence can support

The current v002 microstructure ML-baseline envelope is, factually:

- **Symbol scope:** BTCUSDT only.
- **Calendar coverage:** 90 contiguous UTC dates 2024-12-01 .. 2025-02-28
  (per Phase 4bn-A §1).
- **Supervised splits used:** 45-day train (2024-12-01 .. 2025-01-14;
  74,535,440 supervised rows per included horizon after the 248-row 60s
  boundary embargo); 30-day validation (2025-01-15 .. 2025-02-13; 56,819,649
  supervised rows per included horizon after the 290-row 60s boundary
  embargo); 15-day sealed test (2025-02-14 .. 2025-02-28; 23,797,822 rows;
  `test_rows_loaded: 0`; never opened).
- **Horizons used in baseline ML:** 15s and 60s. 1s and 5s deferred at
  Phase 4bn-A §10 for latency / tradability sensitivity and
  cost-commensurability risk.
- **Feature surface:** the 45 v002 `computed_feature_column_names` (40
  rolling features × 4 windows; 5 non-windowed columns); frozen from the
  v002 feature manifest; no new feature engineering since Phase 4bn-A; no
  feature selection / ranking / pruning since.
- **Split policy:** the Phase 4bm-U-recorded
  `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. Strictly
  chronological; train precedes validation precedes test; 60s-boundary
  embargo enforced; never relaxed.

Given that envelope, the current evidence can support the following claims
at descriptive level only:

1. **One observed instance of a 45 / 30 / 15 chronological multi-day
   ML-baseline result.** The Phase 4bn-B `RECORD_EVIDENCE_ONLY` outcome is
   a single descriptive evaluation, not a strategy-level conclusion.
2. **A descriptive picture of which class is underrepresented.** Flat-class
   prevalence 0.15 – 1.09 %; near-balanced directional classes; majority
   accuracy ~50 %; majority macro-F1 ~0.22. These prevalence numbers are
   *specific to the 90-day envelope* and would not necessarily generalize
   to a different historical window.
3. **A descriptive picture of which baselines are non-trivial vs degenerate
   on this envelope.** L2 / L1 linear softmax: small but reproducible
   lift on accuracy and macro-F1; persistence: small accuracy lift but
   catastrophic log-loss / Brier because it emits one-hot probabilities;
   majority: never predicts the other two classes. These descriptive shapes
   are *specific to the 90-day envelope*.
4. **A descriptive picture of the calibration shape.** Dominant 0.5 – 0.6
   confidence bin well calibrated (gap −0.0047); high-confidence tail
   severely over-confident (gaps −0.061 to −0.392). This shape is *specific
   to the 90-day envelope*.
5. **A descriptive picture of cost-commensurability under §11.6.** Roughly
   6.2 % of 15s validation rows exceed 1× the 16 bps round-trip cost; 18.3 %
   of 60s validation rows exceed 1× cost. These fractions are *specific to
   the 90-day envelope* and reflect the realized volatility regime during
   2024-12-01 .. 2025-02-13.
6. **One descriptive picture of train-vs-validation feature-distribution
   drift.** Phase 4bn-E: 31 low / 13 moderate / 0 high / 1 undefined
   descriptive drift classification; highest absolute standardized mean
   delta 0.330; gross feature-distribution drift partially ruled out at
   the measurement-frame level only. This snapshot is *specific to the
   90-day envelope* and to the train-vs-validation comparison; it does not
   generalize to a different window.
7. **One descriptive picture of microstructural regime direction between
   train and validation.** Count features positive; mean-quantity features
   negative; consistent with trade frequency rising and per-trade size
   falling between train and validation. This direction is *specific to
   the 90-day envelope*.
8. **Confirmation that the test holdout was not used.** `test_rows_loaded:
   0`; `iter_partitions(split="test", ...)` raise verified by tests; the
   test holdout remains sealed as a single-use terminal evaluation budget
   reserved for a separately authorized future terminal-holdout phase that
   does not exist.

These are all *descriptive* claims. None of them is a sufficiency claim,
a representativeness claim, an outlier claim, a tradability claim, or an
edge claim.

## 8. What the current 3-month v002 evidence cannot support

The 90-day v002 envelope **cannot**, without further work, support any of
the following claims:

1. **It cannot support a sufficiency claim.** 90 calendar days is a single
   window. A single window cannot establish that its descriptive results
   are stable across other windows of the same length, across longer
   windows, or across regimes that did not appear in 2024-12-01 ..
   2025-02-28.
2. **It cannot support an insufficiency claim.** 90 calendar days has not
   been shown to be too short either. The Phase 4bn-B / 4bn-C / 4bn-D /
   4bn-E results do not, in themselves, establish that more data would
   meaningfully change the descriptive picture; that is an *unresolved
   question*, not a known result.
3. **It cannot support a representativeness claim.** The 90-day envelope
   covers December 2024, January 2025, and February 2025. It does not
   cover Q2 / Q3 / Q4 2025, does not cover any pre-2024-12 period, and
   does not cover any other calendar year. Whether the realized volatility
   / trend / funding / flow regimes in those three months are representative
   of long-run BTCUSDT futures microstructure is an *open question*.
4. **It cannot support an outlier claim.** The Phase 4bn-E descriptive
   train-vs-validation drift summary (highest standardized mean delta 0.330;
   highest missing-rate delta ≈ 6e-06; 0 high-drift features) is consistent
   with a *quietly-stable* 90-day envelope at the measurement-frame level;
   it is also consistent with the 90-day envelope being one specific
   manifestation of a wider regime space the project has not measured.
   **The operator-supplied "outlier" framing is preserved as an unresolved
   risk, not as a conclusion.** Phase 4bn-F does *not* call the 90-day
   window an outlier as fact. It also does *not* call it representative as
   fact.
5. **It cannot support edge / profitability / tradability / strategy-
   readiness / signal-readiness claims.** Already established by every
   prior Phase 4bn-* and inherited verbatim: descriptive lift is not edge.
6. **It cannot support paper / shadow / live-readiness claims.** Every
   Phase 4bn-* phase explicitly forbids these.
7. **It cannot support sufficiency-for-ML-architecture claims.** The
   Phase 4bn-A §15 / Phase 4bn-B optional shallow-tree decision (memory
   fail-closed; intentionally not implemented) is *not* re-litigated by the
   current evidence; whether the v002 envelope is enough for a richer
   model family is an open question.
8. **It cannot support sufficiency-for-feature-rework claims.** Whether
   the 45-column v002 feature surface is enough, whether new features
   would help, and whether the feature manifest should change — all open
   questions that the current evidence cannot decide.
9. **It cannot support sufficiency-for-label-rework claims.** Whether the
   strict-sign direction label is the right framing, whether
   cost-commensurate framings should replace it, and whether a different
   target family should be used — all open questions that the current
   evidence cannot decide.
10. **It cannot support sufficiency-for-horizon-rework claims.** Whether
    1s / 5s / longer-than-60s horizons would change the picture is an open
    question.
11. **It cannot support sufficiency-for-additional-symbol claims.** Whether
    ETHUSDT comparison would help is an open question; the v002 envelope
    is BTCUSDT-only.
12. **It cannot support storage-architecture claims.** Whether the current
    partitioned Parquet layout is the right backing for any future
    longer-history dataset is an open question that the current evidence
    does not address.

The contrast between §7 and §8 is the central observation of this memo:
**the 90-day window provides one well-controlled descriptive picture, not
a generalization-ready basis.**

## 9. Representativeness / outlier-risk framework

To answer the operator's standing concern about whether the 90-day envelope
may be insufficient or may represent an outlier regime, any future
separately authorized data-expansion phase would have to surface evidence
along multiple non-orthogonal dimensions. Phase 4bn-F defines this framework
**without executing** any of it. The dimensions below are descriptive
categories a future scoping memo would have to address; they are not a
plan, not a recommendation to acquire, not a recommendation to compute,
and not a recommendation to migrate storage.

1. **Chronological coverage.** Does the v002 90-day envelope sample a long
   enough calendar window? Three months samples three calendar months; it
   does not sample year-on-year seasonality, does not sample multiple
   quarter ends, does not sample multiple funding cycles across regimes,
   and does not sample multiple BTC halving / cycle phases. A future
   scoping memo would have to decide what calendar coverage would be
   *enough* before any acquisition is justified.
2. **Volatility regimes.** Does the v002 envelope sample multiple realized
   volatility regimes (low, medium, high; quiet, expansion, contraction)?
   The §11.6 cost-commensurability fractions (15s 6.2 % > 1× cost; 60s
   18.3 % > 1× cost) are themselves a volatility readout; a longer window
   would carry different fractions, and a meaningfully different fraction
   would change the interpretation of any future ML-baseline result. A
   future scoping memo would have to decide which volatility regimes the
   expansion is intended to sample.
3. **Trend / range regimes.** Does the v002 envelope sample both trending
   and range-bound regimes at the 4h / daily / weekly scales? Phase 4bn-E
   surfaced count-up / mean-quantity-down between train and validation,
   consistent with an evolving microstructural regime; without longer
   windows, the project cannot distinguish a slow drift from an episodic
   regime shift.
4. **Volume / activity regimes.** Does the v002 envelope sample both low
   and high market-activity periods? Phase 4bn-E's 13 moderate-drift
   features cluster on count and mean-quantity dimensions — the same
   dimensions a volume-regime sweep would surface most directly. A future
   memo would have to decide what activity regimes the expansion must
   cover.
5. **Funding / derivatives-flow regimes.** Does the v002 envelope sample
   multiple funding-rate regimes (compressed, neutral, extreme positive,
   extreme negative)? Phase 3i / 3j evidence on D1-A established that
   funding behaviour can dominate strategy economics; the v002 envelope
   does not currently support a multi-regime funding evaluation.
6. **Intraday / weekday effects.** Does the v002 envelope sample the
   intraday / weekday structure (sessions, weekday-vs-weekend, holidays)?
   The Phase 4bn-A §15 linear baseline sees `utc_hour` and `utc_minute` as
   features directly; the descriptive Phase 4bn-B result averaged over
   intraday and weekday patterns within 90 days. A future memo would have
   to decide whether subtler intraday / weekday effects need a longer
   window to surface.
7. **Market-event concentration.** Does the v002 envelope contain or
   exclude major venue / macro / on-chain / regulatory events? Three
   contiguous months can over-represent or under-represent any single
   event. A future memo would have to decide how event concentration is
   evaluated.
8. **BTCUSDT-only limitation.** The v002 envelope is BTCUSDT-only.
   Cross-symbol comparison (ETHUSDT as the locked first secondary research
   symbol) is not in the current ML-baseline evidence. A future memo would
   have to decide whether comparison-symbol coverage is needed, and what
   the cost of providing it would be.
9. **Train / validation / test chronology.** The 45 / 30 / 15 split is
   strictly chronological by Phase 4bm-U policy. A future expansion would
   have to decide how additional history is allocated across train,
   validation, and test, and whether multiple non-overlapping
   train / validation / test windows are produced rather than one extended
   contiguous window. The test holdout remains sealed regardless; no
   future memo can authorize test-set inspection or test-set tuning from
   this state.
10. **Cost-commensurability under §11.6.** The §11.6 round-trip cost lock
    (16 bps) is preserved. Any future data-sufficiency evidence must
    re-read the cost-commensurability fractions across the expansion
    window; a fraction that is materially different from the v002
    envelope changes the interpretation of any ML-baseline lift. The
    cost lock itself remains untouched.
11. **High-confidence calibration failure from Phase 4bn-C.** The high-
    confidence over-confidence tail (reliability gaps −0.061 to −0.392 in
    the 0.6 – 1.0 bins; the 0.8 – 0.9 bin's empirical accuracy 0.4881
    *below* the majority floor) is a *specific* descriptive failure of
    the v002 linear baseline. Whether longer-history acquisition would
    change this calibration failure is an *open question*; a future
    scoping memo would have to decide whether new evidence is plausible.
12. **Multiple non-overlapping windows vs single longer window.** Any
    future expansion has at least two structural options: acquire a
    single contiguous longer history, or acquire multiple separated
    windows that intentionally sample different regimes. The single-window
    option preserves the strictly-chronological split policy and is
    easier to reason about; the multi-window option samples more regimes
    but requires explicit treatment of inter-window gaps and explicit
    treatment of train / validation / test chronology across windows.
13. **Preserve label / feature family vs require a new family.** A future
    expansion has two structural choices on the label and feature surface:
    preserve the existing v002 label and feature manifests so the new
    evidence is comparable to Phase 4bn-B (and ETL re-derivability from
    Binance public sources is preserved), or require a new label / feature
    family (which would trigger the Phase 4bj-* eligibility-gate governance
    arc and a new dataset-version bump per `dataset-versioning.md`). The
    structural cost of a new family is high; the cost of preserving the
    existing family is mostly storage and IO.

**Why the 90-day window may be a useful first controlled envelope but
insufficient for broad claims.** The Phase 4bn-A through Phase 4bn-E arc
was deliberately scoped so that one bounded window could be measured
descriptively without overcommitting the project to a particular
generalization claim. That scoping was correct: it produced clean,
auditable descriptive evidence (`RECORD_EVIDENCE_ONLY` at Phase 4bn-B;
`RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED` at Phase 4bn-E) that
no later phase has to relitigate. The 90-day window is the project's first
microstructure ML-baseline envelope and remains the only one. That bounded
clarity is its strength. Its weakness is, equivalently, that one envelope
cannot answer multi-regime / multi-window / multi-symbol / longer-history
questions, all of which would be the subject of a future separately
authorized data-expansion phase.

## 10. Data-sufficiency dimensions to evaluate before any acquisition

Before any future acquisition is authorized, a future separately authorized
docs-only data-expansion requirements memo would have to evaluate at
minimum the following dimensions and record an explicit per-dimension
decision. Phase 4bn-F does *not* execute this evaluation; it records the
list of dimensions a future memo would have to cover so that the operator
can reason about cost before authorizing any expansion.

1. **Target calendar coverage.** Single contiguous window vs multiple
   separated windows; absolute calendar length; explicit lower bound
   below which expansion is not justified; explicit upper bound beyond
   which expansion no longer pays for itself.
2. **Target volatility-regime coverage.** Which regimes must be sampled;
   how regimes are operationally defined (e.g., realized-volatility
   percentile bins; cost-commensurability fractions); how a future window
   would be assessed as covering each regime.
3. **Target trend-vs-range coverage.** Which trend / range regimes must
   be sampled; how they are operationally defined (e.g., 4h / daily
   trend strength; weekly range vs trend); how coverage is verified.
4. **Target volume / activity coverage.** Which activity regimes must be
   sampled; how they are defined (e.g., per-day aggTrade count buckets;
   per-minute trade frequency); how coverage is verified.
5. **Target funding-regime coverage.** Which funding regimes must be
   sampled; how they are defined (e.g., funding-rate percentile bins;
   Z-score-of-funding bins); how coverage is verified.
6. **Target intraday / weekday coverage.** Which intraday / weekday /
   session patterns must be sampled; how they are defined; how coverage
   is verified.
7. **Target market-event coverage.** Whether the expansion must
   intentionally include or exclude specific market events; how events
   are operationally identified; how event concentration is reasoned
   about.
8. **Symbol scope.** Whether ETHUSDT (the locked first secondary research
   symbol) is included for cross-symbol comparison; whether other symbols
   are included; what the cost is.
9. **Split allocation across expansion.** How additional history is
   allocated across train / validation / test; whether multiple
   non-overlapping splits are produced; whether the sealed test holdout
   from the v002 envelope is preserved as is.
10. **Label / feature family preservation.** Whether the existing v002
    label and feature manifests are preserved or whether a new dataset
    family is required (with full Phase 4bj-* governance implications).
11. **Cost-commensurability re-evaluation.** How the §11.6 fractions are
    re-measured across the expansion; what change in the fractions would
    constitute *new* evidence; what change would constitute *consistent*
    evidence.
12. **High-confidence calibration re-evaluation.** Whether the longer
    history would plausibly change the high-confidence over-confidence
    pattern; what evidence would constitute that change.
13. **Per-window descriptive comparability.** How the expansion window's
    descriptive picture is compared to the v002 envelope; how a "consistent"
    vs "inconsistent" outcome is operationally defined.
14. **Acquisition envelope.** The total raw / normalized / feature / label
    artefact volume implied by the expansion; the IO / disk footprint
    implication; whether the artefacts remain locally derivable from
    Binance public sources.
15. **Storage architecture envelope.** Whether the expansion fits inside
    the current partitioned-Parquet layout, requires compacted Parquet,
    requires DuckDB-as-cache, requires SQLite-for-metadata, or requires
    something else. **This is itself a separate question that any future
    storage-scaling memo would have to address before any acquisition.**
16. **Eligibility-gate envelope.** Whether the expansion triggers a new
    feature-family gate, a new label-family gate, a new normalization
    gate, or a new metrics gate; how the gate evidence is produced; how
    the gate evidence is recorded; how successor-state is recorded.
17. **Reproducibility envelope.** How the expansion remains re-derivable
    from public Binance sources; how manifests and sidecars are produced;
    how the Phase 4bb-F canonical sidecar policy is preserved.
18. **Non-authorization envelope.** What the expansion is *not* allowed to
    authorize (ML training, strategy research, signal generation, backtest
    execution, threshold tuning, paper / shadow / live-readiness,
    deployment, exchange-write, production-key creation, MCP / Graphify,
    credentials) — preserved verbatim from the existing Phase 4bn-* arc.

These dimensions are *what a future memo would have to cover*. They are
not what Phase 4bn-F provides. **Phase 4bn-F does not pre-decide any of
these dimensions; it records the list so the operator can see the
governance cost of any future expansion before authorizing one.**

## 11. Possible future data-expansion options, design-level only

Phase 4bn-F enumerates seven candidate future data-expansion options below
at design level only. Each option records (a) what question it answers,
(b) what it would require later, (c) what it risks, (d) what it does not
authorize now, and (e) whether it is recommended, not recommended, or
deferred. **No option is selected for execution by Phase 4bn-F. No option
is authorized by Phase 4bn-F.** Each future executable phase requires a
separate operator authorization that satisfies
`docs/00-meta/process/phase-prompt-template.md`.

### Option A — Remain with current 90-day v002 envelope; no acquisition

- **What it answers.** Whether the project should treat the existing
  Phase 4bn-A through Phase 4bn-E descriptive evidence as the terminal
  evidence boundary for the v002 ML-baseline family.
- **What it would require later.** Nothing executable. Operator chooses
  pause as the recommended state and accepts that the current evidence is
  the project's recorded ML-baseline interpretation.
- **What it risks.** Permanently leaving open the question of whether the
  90-day window is sufficient or representative. Foreclosing future
  expansion options by inertia rather than by decision. Accepting the
  current high-confidence calibration failure as the standing baseline
  with no further measurement.
- **What it does not authorize now.** Anything executable.
- **Recommended / not recommended / deferred.** **Available** as a valid
  operator choice; not recommended as the only option because Phase 4bn-F
  does not foreclose data-expansion options at governance level.

### Option B — Docs-only data-expansion requirements memo

- **What it answers.** Whether a future docs-only / design-only / scoping-
  only memo can enumerate the §10 dimensions with per-dimension explicit
  decisions before any acquisition is authorized. The memo's job is to
  define what the project would have to know to *decide* whether to
  acquire, not to acquire.
- **What it would require later.** A separately authorized Tier 1 docs-only
  phase whose authorization prompt names the data-expansion requirements
  memo and the closeout as the only allowed tracked files (plus the narrow
  `current-project-state.md` paragraph). No source / test / script /
  manifest / sidecar / gate-report / successor-state mutation. No local
  data artefact created or mutated. No acquisition. No diagnostic rerun.
  No ML rerun. No storage migration. No database creation.
- **What it risks.** Producing a long, governance-only memo that the
  operator never uses to authorize an acquisition; over-engineering future
  acquisition requirements before the operator has decided whether
  acquisition is worth its cost.
- **What it does not authorize now.** Anything executable. Specifically, it
  does not authorize Option C, D, E, F, or G.
- **Recommended / not recommended / deferred.** **Available** as one
  half of a recommended combined memo path (see Option D below combined
  with the storage-scaling memo).

### Option C — Acquire a longer single continuous BTCUSDT aggTrades history, in a future separately authorized phase

- **What it answers.** Whether a single longer contiguous BTCUSDT
  aggTrades history would change the descriptive picture (class prevalence,
  L2 / L1 lift, persistence calibration, calibration tail, §11.6
  cost-commensurability fractions, train-vs-validation drift) and thus the
  Phase 4bn-C interpretation.
- **What it would require later.** A separately authorized Tier 1 phase
  with full eligibility-gate / manifest / sidecar / successor-state
  governance for the expanded raw / normalized / feature / label / metrics
  artefacts, plus a separately authorized storage-architecture decision
  (see §12 / §13) *before* any acquisition. The acquisition would have to
  satisfy the §10 dimensions and the §11 / §13 / §14 stop conditions
  defined by any data-expansion requirements memo.
- **What it risks.** Trading more data acquisition cost (download time,
  disk footprint, derivation time, gate-evidence time) for a result whose
  predictive value is itself unknown (whether more data will change the
  Phase 4bn-C calibration tail or the §11.6 cost-commensurability fractions
  is itself an open question). Locking the project into a single longer
  contiguous history shape that may not sample multiple regimes well.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option D, E, F, or G.
- **Recommended / not recommended / deferred.** **Deferred.** Phase 4bn-F
  does not recommend this option directly; it must be preceded by a
  separately authorized data-expansion requirements memo (Option B / D)
  and a separately authorized storage-scaling architecture memo (Option B
  / D), and only then by a separate acquisition-phase authorization.

### Option D — Acquire multiple separated BTCUSDT windows across regimes, in a future separately authorized phase

- **What it answers.** Whether multiple non-overlapping BTCUSDT windows
  intentionally sampling different volatility / trend / activity /
  funding / event regimes would surface differences from the v002 envelope
  that the v002 envelope alone cannot.
- **What it would require later.** Same as Option C plus an explicit
  policy for inter-window gaps, an explicit policy for train / validation
  / test chronology across windows, and an explicit governance decision
  about whether the sealed test holdout from the v002 envelope is
  preserved as is or whether new test holdouts are constructed.
- **What it risks.** More structural complexity than Option C; more gate
  evidence than Option C; more storage cost than Option C; more split-
  policy governance work than Option C.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option C, E, F, or G.
- **Recommended / not recommended / deferred.** **Deferred.** Phase 4bn-F
  does not recommend this option directly. It is potentially more
  informative than Option C if the question being asked is "what does
  multi-regime BTCUSDT microstructure look like", but it costs strictly
  more.

### Option E — Add ETHUSDT comparison later, in a future separately authorized phase

- **What it answers.** Whether the locked first secondary research symbol
  (ETHUSDT) carries comparable descriptive results to BTCUSDT, or whether
  the v002 picture is BTCUSDT-specific.
- **What it would require later.** A separately authorized Tier 1
  acquisition phase for ETHUSDT raw / normalized / feature / label /
  metrics artefacts, with full Phase 4bj-* / Phase 4bb-F / Phase 4bm-Q
  governance applied to the new symbol scope. Plus a separately authorized
  storage-architecture decision.
- **What it risks.** More acquisition cost than Option C / D (because it
  doubles the symbol scope rather than extending the calendar); does not
  by itself address regime / longer-history questions; may produce a
  cross-symbol descriptive comparison that does not change the Phase 4bn-C
  interpretation.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option C, D, F, or G.
- **Recommended / not recommended / deferred.** **Deferred.** Phase 4bn-F
  does not recommend this option directly; the cross-symbol question is a
  valid open question, but is secondary to the calendar-coverage / regime-
  coverage question on BTCUSDT.

### Option F — Define a new v003 or successor dataset family later, only if justified by a future requirements memo

- **What it answers.** Whether the existing v002 label / feature family
  is the right family for any longer-history or multi-regime expansion,
  or whether a new dataset family (v003 or other) is required to capture
  the descriptive picture the operator wants.
- **What it would require later.** A separately authorized docs-only
  family-design memo that satisfies the `dataset-versioning.md`
  mandatory-bump conditions; a separately authorized eligibility-gate /
  manifest-design / sidecar-design phase for the new family; a separately
  authorized acquisition phase; a separately authorized storage-architecture
  decision.
- **What it risks.** Highest structural cost of any option in this list.
  Triggers a full new Phase 4bj-* / Phase 4bb-F / Phase 4bm-* governance
  arc for a family whose value has not been demonstrated. May produce
  evidence that overlaps with what the v002 family already provides.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option C, D, E, or G.
- **Recommended / not recommended / deferred.** **Not recommended at
  governance level until a future requirements memo demonstrates that the
  v002 family cannot answer the operator's question.** Phase 4bn-F treats
  v003 as a deferred-and-conditional option only.

### Option G — Close the ML-baseline arc

- **What it answers.** Whether the project should record a verdict that
  the v002 ML-baseline family is operationally closed for further bounded
  expansion under current evidence and that the descriptive results
  recorded by Phase 4bn-A through Phase 4bn-E stand as the project's
  ML-baseline evidence record.
- **What it would require later.** A separately authorized docs-only
  closure memo whose authorization prompt names the closure memo and the
  closeout as the only allowed tracked files (plus the narrow
  `current-project-state.md` paragraph), and whose decision records the
  operational closure verdict. No source / test / script / manifest /
  sidecar / gate-report / successor-state mutation. No retained verdict
  revised. No project lock loosened.
- **What it risks.** Recording a closure on the v002 ML-baseline family
  before the operator has decided whether the calibration failure and the
  cost-commensurability context could ever be changed by more data;
  closing prematurely on a question whose data-sufficiency answer is
  unknown.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option B, C, D, E, or F, and it does not authorize
  paper / shadow / live-readiness / deployment / exchange-write /
  production keys / Phase 5 / Phase 4 canonical.
- **Recommended / not recommended / deferred.** **Available** as a valid
  operator choice; not recommended as the default because Phase 4bn-F does
  not have the evidence to close the arc unilaterally.

### Summary table — candidate options

| Option | What it answers | Authorizes now? | Pre-acquisition data memo required? | Pre-acquisition storage memo required? |
| --- | --- | --- | --- | --- |
| A — Remain with 90-day envelope | Treat current evidence as terminal | No | No | No |
| B — Docs-only data-expansion requirements memo | Define §10 dimensions before acquiring | No | n/a (this *is* the memo) | No (separate memo) |
| C — Longer single continuous BTCUSDT history | Whether longer single window changes the picture | No | Yes | Yes |
| D — Multiple separated BTCUSDT windows | Whether multi-regime BTCUSDT changes the picture | No | Yes | Yes |
| E — ETHUSDT comparison later | Whether ETHUSDT matches BTCUSDT | No | Yes | Yes |
| F — New v003 / successor family | Whether v002 family is the wrong frame | No | Yes (plus family-design memo) | Yes |
| G — Close the ML-baseline arc | Record operational closure verdict | No | No | No |

Every entry above is **No** for the "Authorizes now?" column. **Phase 4bn-F
authorizes none of the options.**

## 12. Possible future storage-scaling questions, design-level only

Any future expansion that acquires more data than the existing 90-day v002
envelope would force the project to choose explicitly how the new
artefacts are stored. Phase 4bn-F discusses these questions at design level
only; it does not migrate storage, does not create a database, does not
replace Parquet, does not compact Parquet, does not alter the dataset
layout, does not create a DuckDB database file, does not create a SQLite
database file, and does not modify any retention / cache / sidecar /
manifest / gitignore boundary.

The questions a future separately authorized storage-scaling architecture
memo would have to address include:

1. **Current partitioned Parquet.** The project's current historical-data
   storage is partitioned Parquet under `data/microstructure/...` with
   the locked Phase 4bb-F canonical sidecar / path policy. Per
   `docs/04-data/dataset-versioning.md`, Parquet is the canonical
   historical research storage format and DuckDB is the default local
   query engine; raw payloads have their own versioning model
   (source-faithful + traceable). Any storage decision must preserve this
   existing layout for the v002 envelope unchanged.
2. **Compacted Parquet with explicit compression policy.** Whether the
   per-day partition layout should be compacted into larger files (e.g.,
   per-week, per-month) with an explicit compression codec / dictionary /
   row-group policy. Compaction trades smaller file count + lower IO for
   coarser partitioning and harder per-day reproducibility. A future memo
   must decide whether compaction is justified, and if so, must declare
   the compression codec, dictionary policy, row-group size, and
   partitioning key explicitly.
3. **DuckDB querying Parquet in place.** Whether DuckDB is used as the
   query layer over the existing Parquet without copying data into a
   DuckDB database file. This is the lowest-disruption option: DuckDB
   would only be a query engine, the Parquet files remain authoritative,
   and re-derivability from Binance public sources is preserved.
4. **DuckDB database file as a derived local research cache.** Whether
   DuckDB's columnar `.duckdb` database file is used as a derived local
   research cache that mirrors a subset of the Parquet data for faster
   repeated queries. This option introduces a derived artefact whose
   reproducibility must be governed: the `.duckdb` file is *derived* from
   the canonical Parquet; it is not the source of truth; it is gitignored;
   it has its own sidecar / manifest implications.
5. **SQLite only for runtime / control metadata, not large aggTrade
   research matrices unless separately justified.** Per
   `docs/08-architecture/database-design.md`, the runtime database is a
   safety component for control / exposure / order / position / restart /
   reconciliation. SQLite has been *historically discussed* in that
   document as a candidate runtime engine; it is *not* a research-matrix
   engine. Phase 4bn-F preserves that separation: research matrices stay
   in Parquet / DuckDB; runtime control state stays in whatever the
   runtime database choice ends up being. Conflating the two would create
   a single point of failure and undermines the historical-vs-runtime
   separation `data-requirements.md` requires.
6. **Retention / cache / reproducibility tradeoffs.** Whether older
   derived artefacts are retained, archived, or treated as
   re-derivable-on-demand. The Phase 4bb-F canonical sidecar policy
   constrains how derived artefacts are recorded; any retention rule
   must be compatible with that policy.
7. **Disk footprint.** What the realistic raw + normalized + feature +
   label disk footprint is at the proposed expansion size. The v002
   envelope's footprint is already material; longer histories scale
   roughly linearly per symbol.
8. **Query performance.** Whether the partitioned-Parquet layout meets
   the query patterns of any future descriptive memo. The Phase 4bn-E
   diagnostic took 553.6 s on the 75 train + validation partitions read
   twice; longer histories would scale roughly linearly.
9. **Re-derivability from public Binance sources.** Whether every
   artefact stored remains re-derivable from public Binance endpoints
   under the canonical Binance USDⓈ-M futures source policy
   (`docs/04-data/historical-data-spec.md`). Any storage choice that
   breaks re-derivability is structurally rejected.
10. **Sidecar and manifest implications.** Whether each storage choice
    keeps the Phase 4bb-F canonical sidecar policy intact, whether new
    sidecar fields are required, whether new manifest fields are required,
    and whether new successor-state semantics are required. A future
    storage memo would have to declare this explicitly.
11. **Gitignore and non-commit boundaries.** Whether `.gitignore:85:
    data/microstructure/` and `.gitignore:88: data/research/` continue to
    cover the new artefacts. Any storage choice that requires committing
    a derived artefact to the repository is structurally rejected.

**Parquet is already a compressed columnar format, so a database does not
automatically save space.** A `.duckdb` database file is itself a
columnar format with similar compression characteristics; replacing
Parquet with DuckDB does not magically reduce disk footprint, and may
even *increase* it once DuckDB-internal metadata, indexes, and statistics
are accounted for. Compression policy (codec, dictionary, row-group size)
typically has a larger impact than the storage layer choice within the
columnar family. The right question is rarely "Parquet vs DuckDB" — it is
usually "what compression policy, what partitioning key, what file size
target, and what query engine".

**A storage-scaling memo should be separately authorized before any
acquisition or storage migration.** This is the central storage
recommendation of Phase 4bn-F.

## 13. Parquet / DuckDB / database discussion, non-authorizing

The following points are recorded explicitly so the operator has the
governance constraints in one place when reading any future storage-scaling
memo:

- **Parquet is already compressed.** A storage change is not justified by
  "we want compression"; we already have it.
- **DuckDB does not eliminate Parquet.** DuckDB can query Parquet in place
  (Option in §12.3) or maintain a derived `.duckdb` database file (Option
  in §12.4). The former is lower disruption; the latter introduces a
  derived artefact with its own governance implications.
- **A "database" is not a single thing.** "Database" can mean DuckDB
  in-place, DuckDB as a derived file, SQLite, PostgreSQL, or another
  engine. Each has different reproducibility, sidecar, manifest,
  gitignore, and re-derivability implications. The Phase 4bn-F discussion
  does not pick one; it requires that the future memo pick one explicitly.
- **Historical research storage and runtime persistence are separate
  concerns** (`docs/04-data/data-requirements.md` and
  `docs/08-architecture/database-design.md`). A storage-scaling memo for
  microstructure research artefacts is *not* the runtime database
  decision; those are distinct documents and distinct phases.
- **Phase 4bn-F does not choose or implement a storage migration.**
- **Phase 4bn-F does not create DuckDB, SQLite, or any database file.**
- **Phase 4bn-F does not compact Parquet.**
- **Phase 4bn-F does not modify dataset layout.**

## 14. Decision

**`RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Rationale (anchored to §5 – §13):

1. **The Phase 4bn-E descriptive feature-drift result does not, by itself,
   close the data-sufficiency question.** Phase 4bn-E partially ruled out
   gross feature-distribution drift at the measurement-frame level only.
   It did not address regime / volatility / cost-commensurability /
   calendar-coverage / outlier questions. Whether 90 days is enough or is
   an outlier is *unresolved*.
2. **Phase 4bn-F treats "outlier" as an unresolved risk, not as a
   conclusion.** The 90-day envelope is consistent with a quietly-stable
   window at the descriptive scale measured so far, *and* consistent with
   one specific manifestation of a wider regime space that the project
   has not measured. Both readings are admissible under current evidence.
3. **Closing the ML-baseline arc unilaterally (Option G) would over-claim
   confidence in the negative direction.** No stop-work-level negative
   evidence has been produced; the Phase 4bn-B / 4bn-C / 4bn-E descriptive
   results are non-trivial enough that a future scoping memo on
   data-sufficiency may legitimately change the interpretation.
4. **Remaining with the 90-day envelope unilaterally (Option A) would
   over-claim confidence in the positive direction.** No evidence has
   established that the 90-day window is representative or that
   additional data would not meaningfully change the picture.
5. **Acquiring more data without a requirements memo (direct Option C / D
   / E) is structurally premature.** Acquisition cost is high enough that
   the §10 dimensions deserve an explicit per-dimension decision before
   the operator commits to acquisition.
6. **Acquiring more data without a storage-scaling memo (direct Option C
   / D / E) is structurally premature.** Longer-history microstructure
   acquisition and storage layout are tightly coupled: the IO footprint,
   partitioning policy, compression policy, and DuckDB-vs-Parquet
   question all interact with the realistic disk footprint a longer
   history would create.
7. **The cleanest non-paused option is therefore a combined data-expansion
   requirements + storage-scaling architecture memo (Option B combined
   with the storage-architecture memo from §12).** Such a combined memo
   would (a) enumerate the §10 dimensions and a per-dimension decision
   framework, (b) discuss the §12 storage questions at design level only,
   (c) decide neither whether to acquire nor whether to migrate storage,
   and (d) record an explicit non-authorization for both. Combining them
   into a single memo respects the tight coupling between the two
   questions.
8. **The operator-supplied preferred decision was the combined option,
   subject to Claude Code making the final recommendation based on the
   repository evidence.** The repository evidence supports the combined
   option for the reasons in items 1 – 7 above. The combined option is
   strictly compatible with remaining paused (operator may equivalently
   choose pause), does not foreclose the close-arc option (operator may
   equivalently choose to close the arc), and preserves every retained
   verdict and project lock unchanged.
9. **Phase 4bn-F is recommendation-only.** The successor it identifies is
   a possible future docs-only / design-only / scoping-only combined
   data-expansion + storage-scaling memo, *not* an acquisition phase, *not*
   a storage-migration phase, *not* a database-creation phase, *not* a
   Parquet-compaction phase, *not* a v003-creation phase, *not* a label /
   feature / horizon / symbol rework phase, *not* an ML / strategy / signal
   / PnL / backtest phase, *not* a paper / shadow / live-readiness /
   deployment / exchange-write / production-key phase. **The successor is
   not authorized by Phase 4bn-F.** A separate operator authorization is
   required.

## 15. Recommended state and successor options

**Recommended state: remain paused.**

Phase 4bn-F is **recommendation-only** and does not authorize any
successor. The operator may equivalently choose any of the following:

- **remain paused** (default; no successor authorized; Phase 4bn-F's
  recommendation does not pressure the operator to authorize a successor);
- **request a merge prompt for Phase 4bn-F** so the data-sufficiency /
  representativeness scoping decision becomes project-complete on `main`;
- **reject further ML-baseline successors and close the ML arc**
  (operationally close the v002 ML-baseline family for further bounded
  expansion under current evidence; preserve all Phase 4bn-A / 4bn-B /
  4bn-C / 4bn-D / 4bn-E artefacts as research evidence; preserve every
  retained verdict and project lock; no successor authorized);
- **separately authorize a future docs-only combined data-expansion +
  storage-scaling scoping memo (recommended)** that enumerates the §10
  dimensions and a per-dimension decision framework alongside the §12
  storage questions; must remain docs-only and design-only; must not
  authorize any acquisition; must not authorize any storage migration;
  must not create a database; must not compact Parquet; must not create
  a v003 dataset; must not mutate any manifest, sidecar, gate report, or
  successor-state artefact;
- **separately authorize a future docs-only data-expansion requirements
  memo only** (without the storage discussion); this is a weaker variant
  of the recommended combined option and is provided as an operator
  alternative;
- **separately authorize a future docs-only storage-scaling architecture
  memo only** (without the data-expansion discussion); this is a weaker
  variant of the recommended combined option and is provided as an
  operator alternative.

**No acquisition / paper / shadow / live / exchange-write option is valid
from this state.**

## 16. Explicit non-authorizations

Phase 4bn-F is docs-only / design-only / scoping-only and authorizes
**nothing executable**. It does not, and cannot, authorize:

- any data acquisition (no additional days / symbols / families /
  horizons beyond the locked 90-day v002 envelope; no longer single
  contiguous history; no multiple separated windows; no ETHUSDT or other
  comparison-symbol acquisition; no v003 dataset; no successor dataset
  family; no mark-price / spot / cross-venue / order-book / additional
  aggTrades; no longer-horizon labels; no barrier / target-before-stop /
  MFE / MAE / R-multiple / PnL labels; no new feature engineering; no
  new label engineering);
- any storage migration (no Parquet → DuckDB / SQLite / other database
  migration; no Parquet compaction; no per-day → per-week / per-month
  partition restructuring; no new compression codec / dictionary /
  row-group policy applied to existing artefacts; no derived `.duckdb`
  database file creation; no SQLite database file creation; no other
  database file creation);
- any ML training, model scoring, prediction generation, feature ranking,
  feature selection, feature pruning, model selection through results,
  hyperparameter tuning, threshold tuning, calibrator fitting,
  meta-labeling, ensemble construction, or any other ML execution;
- any strategy research, strategy design, signal generation, trade-signal
  generation, PnL simulation, equity-curve construction, Sharpe / Sortino
  / drawdown / hit-rate / trade-PnL metrics, backtests, or walk-forward
  optimization;
- any use of the test holdout for training, fitting, calibration,
  evaluation, tuning, design, model selection, threshold selection,
  reporting, or inspection;
- any diagnostics rerun, diagnostic artefact creation, ML artefact
  creation, reusable split-mask materialization, row-level prediction
  persistence, or model-binary persistence;
- any public / authenticated / private endpoint call; any WebSocket /
  user stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- any manifest mutation, successor-state mutation, gate-report mutation,
  or change to `research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`, `diagnostics_authorized`, or
  `ml_authorized` on any on-disk manifest;
- any source / test / committed-script / config / `.gitignore` /
  `pyproject.toml` / `README.md` / MCP-file modification;
- any commit under `data/microstructure/` or `data/research/`;
- Phase 4bn-G (or any phase under any name performing the recommended
  combined data-expansion + storage-scaling scoping memo, or the
  separately-recommended data-expansion-only or storage-scaling-only
  memos, or any acquisition phase, or any storage-migration phase, or
  any database-creation phase);
- any further Phase 4bn-* successor / Phase 4bo-* / Phase 4bp-*; Phase 5;
  Phase 4 canonical;
- paper / shadow; live-readiness; deployment; exchange-write;
  production-key creation; authenticated APIs; private endpoints; user
  stream; WebSocket implementation;
- any revision of a retained verdict, any loosening of a project lock, or
  any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F
  / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bn-F is a docs-only / design-only / scoping-only v002
data-sufficiency / representativeness scoping memo.** **Phase 4bn-F does
not acquire data.** **Phase 4bn-F does not run diagnostics.** **Phase 4bn-F
does not run ML.** **Phase 4bn-F does not train models.** **Phase 4bn-F
does not score models.** **Phase 4bn-F does not generate predictions.**
**Phase 4bn-F does not inspect the test holdout.** **Phase 4bn-F does not
use the sealed test split.** **Phase 4bn-F does not rank features.**
**Phase 4bn-F does not select features.** **Phase 4bn-F does not prune
features.** **Phase 4bn-F does not engineer features.** **Phase 4bn-F
does not tune hyperparameters.** **Phase 4bn-F does not tune thresholds.**
**Phase 4bn-F does not fit calibrators.** **Phase 4bn-F does not run
strategy research.** **Phase 4bn-F does not define a strategy.** **Phase
4bn-F does not generate trade signals.** **Phase 4bn-F does not simulate
PnL.** **Phase 4bn-F does not run backtests.** **Phase 4bn-F does not
authorize acquisition.** **Phase 4bn-F does not authorize storage
migration.** **Phase 4bn-F does not create a v003 dataset.** **Phase 4bn-F
does not create a database.** **Phase 4bn-F does not compact Parquet.**
**Phase 4bn-F does not modify dataset layout.** **Phase 4bn-F does not
call any public, authenticated, or private endpoint.** **Phase 4bn-F does
not open any WebSocket or user stream.** **Phase 4bn-F does not use
credentials, `.env`, `.mcp.json`, MCP, or Graphify.** **Phase 4bn-F does
not mutate any manifest.** **Phase 4bn-F does not mutate any
successor-state artefact.** **Phase 4bn-F does not commit
`data/microstructure`.** **Phase 4bn-F does not commit `data/research`.**
**Phase 4bn-F does not authorize Phase 4bn-G, Phase 5, paper / shadow,
live-readiness, deployment, exchange-write, production keys, or any
successor phase.**

## 17. Current-project-state update summary

The narrow `docs/00-meta/current-project-state.md` update made by Phase
4bn-F consists of:

- a new Phase 4bn-F paragraph appended immediately after the Phase 4bn-E
  paragraph;
- a new Current-phase block for Phase 4bn-F inserted immediately after the
  new Phase 4bn-F paragraph and immediately before the existing Phase
  4bn-E Current-phase block;
- preservation of every earlier paragraph (Phase 4a .. Phase 4bn-E) and
  every earlier Current-phase block (Phase 4bn-E, Phase 4bn-D, Phase
  4bn-C, Phase 4bn-B, and older blocks) as labelled historical context;
- recording of Phase 4bn-F as **branch-complete only, not merged, not
  project-complete**;
- recording of the Phase 4bn-F decision
  `RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
- recording of the exact non-authorizations (per §0 / §3 / §16 of this
  memo);
- recording of the recommended state (**remain paused**);
- explicit statement that a Phase 4bn-G successor (or any equivalent under
  any name) is recommended but **not authorized** by Phase 4bn-F.

No other section of `docs/00-meta/current-project-state.md` is modified by
Phase 4bn-F. No retained verdict, project lock, manifest field,
successor-state field, gate-report field, or governance label is changed.
The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked by Phase 4bn-F).

## 18. Retained verdicts preserved

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All prior phase results (Phase 4am .. Phase 4bn-E) preserved verbatim.

## 19. Project locks preserved

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max /
  mark-price stops
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k / 4p / 4q / 4v / 4w methodology + strategy-spec locks
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant (never invoked by Phase 4bn-F)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine
  reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## 20. Recommended next state

**Remain paused.** Phase 4bn-F is branch-complete only by this work. Per
the `phase-workflow-standard.md` rule, it is NOT project-complete until a
separately authorized merge phase records its merge-closeout on `main`
per `merge-closeout-standard.md` (Tier 1). The scoping decision
`RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
is a recommendation only and authorizes nothing. **Phase 4bn-G (or any
equivalent under any name) is not authorized by Phase 4bn-F.** **Any
acquisition phase requires a separately authorized phase.** **Any storage-
migration phase requires a separately authorized phase.** **Any
v003-creation phase requires a separately authorized phase.**
**Recommended state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-G docs-only / design-only
/ scoping-only combined data-expansion requirements + storage-scaling
architecture memo is the cleanest non-paused option. It would, if
separately authorized later, enumerate the §10 dimensions with per-
dimension explicit decisions, discuss the §12 storage questions at design
level only, decide neither whether to acquire nor whether to migrate
storage, and record an explicit non-authorization for both. Phase 4bn-G
is **not authorized** by this memo. The operator may equivalently choose
to remain paused, to reject further successors and close the ML arc, to
separately authorize only a data-expansion requirements memo, or to
separately authorize only a storage-scaling architecture memo; Phase 4bn-F
does not foreclose any of these alternatives.
