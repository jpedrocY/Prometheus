# Phase 4bn-G — Combined Data-Expansion Requirements + Storage-Scaling Architecture Scoping Memo

**Phase identity:** Phase 4bn-G — Combined Data-Expansion Requirements +
Storage-Scaling Architecture Scoping Memo (docs-only / design-only /
scoping-only governance memo; Tier 1 — Full Phase per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3; the separately
authorized scoping phase that follows the Phase 4bn-F recommendation
`RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`).
**Date:** 2026-05-29.
**Branch:** `phase-4bn-g/combined-data-expansion-storage-scaling-scoping`.
**Base SHA:** `main` at `c9a2df0eb3e76a91b72c3687f3767b931b458fe2` (Phase
4bn-F SHA-finalization commit `docs(phase-4bn-f): finalize merge closeout
shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3. Phase 4bn-G is
adjacent to possible future data acquisition, possible future v003 /
longer-history dataset planning, possible future storage architecture
decisions, possible future ML-baseline downstream admissibility, and
possible future regime / outlier interpretation, while explicitly
authorizing none of them.
**Phase type:** docs-only / design-only / scoping-only. Adds two new tracked
docs files under `docs/00-meta/implementation-reports/` (this memo + the
paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`.
**No** source / test / committed-script / configuration / manifest / sidecar
/ gate-report / successor-state mutation. **No** local data artefact created
or mutated. **No** diagnostic rerun. **No** ML rerun. **No** ML artefact.
**No** acquisition. **No** storage migration. **No** database creation. **No**
Parquet compaction. **No** v003 dataset creation. **No** successor
authorization.
**Status:** drafted; pending operator review. Branch-complete only by this
work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bn-G is a docs-only / design-only / scoping-only combined
  data-expansion requirements + storage-scaling architecture scoping memo.**
- **Phase 4bn-G does not acquire data.**
- **Phase 4bn-G does not run diagnostics.**
- **Phase 4bn-G does not run ML.**
- **Phase 4bn-G does not train models.**
- **Phase 4bn-G does not score models.**
- **Phase 4bn-G does not generate predictions.**
- **Phase 4bn-G does not inspect the test holdout.**
- **Phase 4bn-G does not use the sealed test split.**
- **Phase 4bn-G does not rank features.**
- **Phase 4bn-G does not select features.**
- **Phase 4bn-G does not prune features.**
- **Phase 4bn-G does not engineer features.**
- **Phase 4bn-G does not tune hyperparameters.**
- **Phase 4bn-G does not tune thresholds.**
- **Phase 4bn-G does not fit calibrators.**
- **Phase 4bn-G does not run strategy research.**
- **Phase 4bn-G does not define a strategy.**
- **Phase 4bn-G does not generate trade signals.**
- **Phase 4bn-G does not simulate PnL.**
- **Phase 4bn-G does not run backtests.**
- **Phase 4bn-G does not authorize acquisition.**
- **Phase 4bn-G does not authorize storage migration.**
- **Phase 4bn-G does not create a v003 dataset.**
- **Phase 4bn-G does not create a database.**
- **Phase 4bn-G does not compact Parquet.**
- **Phase 4bn-G does not modify dataset layout.**
- **Phase 4bn-G does not call any public, authenticated, or private endpoint.**
- **Phase 4bn-G does not open any WebSocket or user stream.**
- **Phase 4bn-G does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.**
- **Phase 4bn-G does not mutate any manifest.**
- **Phase 4bn-G does not mutate any successor-state artefact.**
- **Phase 4bn-G does not commit `data/microstructure`.**
- **Phase 4bn-G does not commit `data/research`.**
- **Phase 4bn-G does not authorize Phase 4bn-H, Phase 5, paper / shadow,
  live-readiness, deployment, exchange-write, production keys, or any
  successor phase.**
- **Recommended state remains paused.**

---

## 1. Purpose

Phase 4bn-G answers a single governance / scoping question:

> Given that Phase 4bn-F recommended a future docs-only / design-only /
> scoping-only combined data-expansion requirements + storage-scaling
> architecture memo as the cleanest non-paused option after the 90-day v002
> ML-baseline arc, what *exact* requirements would any future data
> acquisition have to satisfy, what *exact* storage architecture options
> would be admissible, how do those questions couple, and what successor (if
> any) should the project consider, subject to separate operator
> authorization?

Phase 4bn-G is **docs-only / design-only / scoping-only**. It reads only
committed repository Markdown reports and committed architecture documents
as its evidence base. It opens no local gitignored `data/research/` outputs.
It opens no local gitignored `data/microstructure/` datasets. It reads no
local parquet, CSV, or JSON output. It calls no endpoint. It uses no
credentials. It mutates no manifest, sidecar, gate report, or successor-state
artefact. It trains nothing, scores nothing, predicts nothing, evaluates
nothing on test data, selects nothing, ranks nothing, tunes nothing, runs
nothing, materialises no artefact, acquires no data, migrates no storage,
creates no database, compacts no Parquet, modifies no dataset layout,
creates no v003 dataset, and authorizes no successor implementation. **Phase
4bn-G is the governance-level combined data-expansion + storage-scaling
scoping memo, not data acquisition and not storage migration.**

This memo:

- carries the Phase 4bn-F recommendation forward verbatim as the
  immediate-predecessor authorising boundary;
- carries the Phase 4bn-E descriptive train-vs-validation feature drift
  result forward verbatim as the most recent ML-arc measurement-frame
  evidence;
- carries the Phase 4bn-D bounded ML-baseline expansion scoping decision
  forward verbatim as the design boundary for the C-A / C-B / C-C / C-D /
  C-E / C-F candidate menu;
- carries the Phase 4bn-C corrected interpretation of Phase 4bn-B ML-baseline
  evidence forward verbatim as the binding factual frame for any
  data-sufficiency claim;
- carries the Phase 4bn-B `RECORD_EVIDENCE_ONLY` decision forward verbatim;
- defines a concrete data-expansion **requirements framework** any future
  separately authorized acquisition-readiness memo would have to satisfy
  before any acquisition is authorized;
- enumerates seven candidate **expansion shapes** at design level only with
  per-option what-it-answers / what-it-requires-later / expected storage
  impact / expected governance cost / expected reproducibility implications /
  what-it-risks / what-it-does-not-authorize-now / recommended-or-deferred
  classification;
- enumerates six candidate **storage architectures** at design level only
  with per-option what-it-solves / what-it-does-not-solve / disk-footprint
  implications / query-performance implications / reproducibility
  implications / sidecar / manifest implications / gitignore / non-commit
  implications / migration risk / recommended-or-deferred classification;
- crosses the expansion shapes with the storage architectures in a coupled
  decision matrix that classifies each combination as compatible, compatible
  but deferred, not recommended, or structurally rejected — without
  authorizing any combination;
- defines required **pre-acquisition gates** any future acquisition would
  have to satisfy before any execution;
- defines required **pre-storage-migration gates** any future storage change
  would have to satisfy before any execution;
- defines the required **non-authorization envelope** any future docs-only
  successor must honour;
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
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_merge-closeout.md`
    (Phase 4bn-F merge-closeout;
    `MEMO RECORDED — RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_v002-data-sufficiency-representativeness-scoping.md`
    (Phase 4bn-F scoping memo).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-f_closeout.md`
    (Phase 4bn-F closeout).
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
  - `docs/04-data/data-requirements.md` (high-level data requirements index;
    historical-vs-runtime storage separation; Parquet + DuckDB + explicit
    dataset versioning research stack; runtime DB is operational storage).
  - `docs/04-data/historical-data-spec.md` (canonical historical-data
    contract; Binance USDⓈ-M futures source policy).
  - `docs/04-data/timestamp-policy.md` (timestamp-handling rules; read for
    context only; no rule restated).
  - `docs/04-data/dataset-versioning.md` (dataset-versioning policy;
    Parquet-first / DuckDB query-engine; mandatory bump conditions;
    `__vNNN` naming pattern; immutability; manifest requirements;
    `data/microstructure/` and `data/research/` reproducibility).
  - `docs/08-architecture/database-design.md` (runtime database design
    document; SQLite with WAL recommended for runtime control state; the
    runtime database is a safety component, not an analytical store;
    historical research storage is a *separate* domain).
- **Inputs explicitly NOT used:** local gitignored
  `data/research/microstructure/ml-baselines/phase-4bn-b/` outputs (Phase
  4bn-B local artefacts); local gitignored
  `data/research/microstructure/ml-baselines/phase-4bn-e/` outputs (Phase
  4bn-E local artefacts); local gitignored Phase 4bm-W / Phase 4bm-Q /
  Phase 4bm-S / Phase 4bm-U / Phase 4bm-X artefacts; local
  `data/microstructure/` raw / normalized / feature / label parquets; local
  Phase 4bn-B / Phase 4bn-E descriptive CSV / JSON outputs. Phase 4bn-G
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
  `git rev-parse main == git rev-parse origin/main == c9a2df0eb3e76a91b72c3687f3767b931b458fe2`.
  Phase 4bn-F SHA-finalization commit `c9a2df0eb3e76a91b72c3687f3767b931b458fe2`
  is the tip; Phase 4bn-F merge-closeout commit
  `76c4f8befe9fd9f41470d1836f181796f45197a6`, Phase 4bn-F merge commit
  `615c172de55aac2b7c8b127625b2f22bb14fe591`, and Phase 4bn-F branch commit
  `85a74a535ec4532c45415fa2f6ddc416d58d04da` are present on `main`
  immediately below the SHA-finalization commit. Phase 4bn-E SHA-finalization
  commit `8fa219c83326c79ffb6406cc1904440fdc63c376` is below that.
  Predecessor chain (Phase 4bn-A → 4bn-B → 4bn-C → 4bn-D → 4bn-E → 4bn-F) is
  fully merge-complete on `main`.

## 3. Phase type and strict scope

Phase 4bn-G is **docs-only / design-only / scoping-only**.

**Allowed surface (tracked files added or modified):**

- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_combined-data-expansion-storage-scaling-scoping.md`
  (this memo; new).
- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_closeout.md`
  (closeout; new).
- `docs/00-meta/current-project-state.md` (narrow current-phase paragraph +
  Current-phase block addition; prior Phase 4bn-A / 4bn-B / 4bn-C / 4bn-D /
  4bn-E / 4bn-F history preserved as labelled historical context).

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
block applies in full to Phase 4bn-G.

## 4. Evidence base and input boundary

Phase 4bn-G reads, read-only, the committed repository Markdown documents
enumerated in §2. It reads no local gitignored artefact. It re-hashes no
local file. It does not invoke any normalizer, gate runner, label kernel,
feature kernel, ML runner, diagnostic runner, backtest runner, simulator,
or acquisition runner. It does not call any acquisition script, does not
load any parquet or CSV from `data/microstructure/` or `data/research/`,
does not call `ml_baseline_runner.run(...)`, does not call
`run_feature_drift_v002(...)`, and does not call any helper that touches
the local data surface. The Phase 4bn-A through Phase 4bn-F merge-closeouts,
implementation reports, and closeouts are treated as the canonical,
sufficient evidence record for the ML-baseline arc; this is the explicit
guarantee that Phase 4bn-G does not, and cannot, reach for the actual local
artefacts. The data architecture documents (`docs/04-data/*.md`,
`docs/08-architecture/database-design.md`) are read for design context only;
no rule, schema, or policy from those documents is rewritten by this memo.

This boundary is deliberate. It (a) protects the local artefacts from
accidental mutation, (b) keeps Phase 4bn-G fully reviewable from `main`
without any local state assumption, and (c) honours the
`phase-workflow-standard.md` rule that branch-complete reports must record
what was actually read so that audit is anchored to repository state rather
than to working-directory state.

## 5. Phase 4bn-F decision carried forward

The Phase 4bn-F merge-closeout, implementation report, and closeout are the
immediate predecessor and the explicit authorising boundary for Phase
4bn-G. Their key conclusions are carried forward verbatim by Phase 4bn-G:

- **Phase 4bn-F decision (verbatim):**
  `RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-F type (verbatim):** docs-only / design-only / scoping-only
  governance memo (Tier 1 — Full Phase).
- **Phase 4bn-F is project-complete on `main`** (merge commit
  `615c172de55aac2b7c8b127625b2f22bb14fe591`; merge-closeout commit
  `76c4f8befe9fd9f41470d1836f181796f45197a6`; final-`main` SHA
  `c9a2df0eb3e76a91b72c3687f3767b931b458fe2`).
- **Phase 4bn-F is recommendation-only.** It authorizes nothing executable;
  it explicitly does not authorize Phase 4bn-G, any successor, any
  acquisition, any storage migration, any database creation, any Parquet
  compaction, any v003 dataset, any ML, any strategy, any signal, any PnL,
  any backtest, any paper / shadow / live-readiness / deployment /
  exchange-write / production-key work. The operator's separate authorization
  of Phase 4bn-G is recorded in the authorization prompt that produced this
  memo. Phase 4bn-F's recommendation does not retrospectively authorize
  Phase 4bn-G to authorize a downstream successor; Phase 4bn-G is itself
  docs-only / design-only / scoping-only and authorizes nothing.
- **Phase 4bn-F equivalent operator alternatives (verbatim):** remain paused;
  request a merge prompt for Phase 4bn-F (already chosen and executed);
  reject further ML-baseline successors and close the ML arc; separately
  authorize only a docs-only data-expansion requirements memo; separately
  authorize only a docs-only storage-scaling architecture memo. The
  operator chose the combined-memo option; Phase 4bn-G is the chosen
  combined-memo execution.

This memo defers to Phase 4bn-F on every factual scoping interpretation of
the 90-day v002 ML-baseline arc and the storage-scaling open questions;
Phase 4bn-G draws no new descriptive conclusion about the ML-baseline arc
and computes no metric.

## 6. Phase 4bn-E / 4bn-D / 4bn-C / 4bn-B interpretation carried forward

The Phase 4bn-E descriptive feature drift result, the Phase 4bn-D bounded
ML-baseline expansion scoping decision, the Phase 4bn-C corrected
interpretation of Phase 4bn-B ML-baseline evidence, and the Phase 4bn-B
descriptive-only result are the binding factual frame for any
data-sufficiency or storage-scaling claim discussed below. They are carried
forward verbatim:

- **Phase 4bn-E decision (verbatim):**
  `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`. Phase 4bn-E executed
  the bounded descriptive C-D candidate (train-vs-validation feature drift
  diagnostics) and produced descriptive feature-drift evidence (45 v002
  computed features analysed; 31 `low_descriptive_drift`, 13
  `moderate_descriptive_drift`, 0 `high_descriptive_drift`, 1
  `undefined_due_to_zero_or_missing_train_std`; highest absolute
  standardized mean delta 0.330; highest absolute missing-rate delta
  ≈ 6e-06; the 13 moderate-drift features cluster on count and
  mean-quantity dimensions, signed consistently between train and
  validation). Phase 4bn-E partially ruled out gross feature-distribution
  drift at the measurement-frame level only; it did not address regime /
  volatility / cost-commensurability / calendar-coverage / outlier
  questions.
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
  0.4881, *below* the majority floor); §11.6 cost-commensurability
  fractions on validation: 15s 6.2 % > 1× / 1.6 % > 2× / 0.16 % > 5×;
  60s 18.3 % > 1× / 5.8 % > 2× / 0.93 % > 5×; train-validation deltas
  small (~0.5 pp on hard metrics) — no overfitting at this measurement
  level; test holdout sealed (`test_rows_loaded: 0`).
- **A naive "trade when confidence is high" idea would fail under current
  evidence.** Statistical descriptive lift on a near-50 / 50 binary in a
  regime where 80 – 95 % of validation rows have absolute moves below the
  round-trip cost is not a tradability claim.
- **15s has stronger model signal but worse cost / tradability context; 60s
  has better cost context but weaker model signal.**
- **None of this is edge, profitability, tradability, strategy-readiness,
  or a signal.** **Phase 4bn-G inherits this boundary without softening it.**

## 7. Current 90-day v002 evidence boundary

The current v002 microstructure ML-baseline envelope is, factually:

- **Symbol scope:** BTCUSDT only.
- **Calendar coverage:** 90 contiguous UTC dates 2024-12-01 .. 2025-02-28
  (per Phase 4bn-A §1).
- **Supervised splits used:** 45-day train (2024-12-01 .. 2025-01-14;
  74,535,440 supervised rows per included horizon after the 248-row 60s
  boundary embargo); 30-day validation (2025-01-15 .. 2025-02-13;
  56,819,649 supervised rows per included horizon after the 290-row 60s
  boundary embargo); 15-day sealed test (2025-02-14 .. 2025-02-28;
  23,797,822 rows; `test_rows_loaded: 0`; never opened).
- **The sealed test split remains sealed and is not inspected.** Phase
  4bn-G does not read it, evaluate against it, design with it, peek at it,
  hash it, or unseal it under any pretext. `iter_partitions(split="test",
  ...)` raises by construction in the Phase 4bn-B implementation and that
  invariant is unchanged.
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

The 90-day v002 envelope is the project's first microstructure ML-baseline
envelope and remains the only one. It provides **one well-controlled
descriptive picture**, not a generalisation-ready basis. The Phase 4bn-F
memo §7 / §8 contrast is preserved verbatim by Phase 4bn-G:

- The current v002 microstructure ML-baseline window is **90 calendar
  days**.
- The split structure is **45 train days, 30 validation days, and 15
  sealed test days**.
- The sealed test split remains sealed and is not inspected.
- Phase 4bn-B produced descriptive ML-baseline evidence only.
- Phase 4bn-C interpreted that evidence as small descriptive lift, not
  edge.
- Phase 4bn-D scoped bounded expansion options but authorized nothing.
- Phase 4bn-E partially ruled out gross train-vs-validation
  feature-distribution drift at the measurement-frame level only.
- Phase 4bn-F concluded the 90-day window is useful but **not enough to
  prove broad sufficiency, insufficiency, representativeness, or outlier
  status**.
- None of the Phase 4bn-A through Phase 4bn-G evidence establishes edge,
  profitability, tradability, strategy-readiness, signal-readiness, paper
  / shadow readiness, or live-readiness.
- Parquet is already a compressed columnar format, so moving to a database
  does not automatically save space.
- Future data expansion and storage architecture are tightly coupled.

## 8. Data-expansion requirements framework

A future separately authorized acquisition-readiness memo would have to
satisfy the following requirements framework before any acquisition is
authorized. Phase 4bn-G **defines** this framework. It **does not execute
it**. It **does not pre-decide** any requirement. It **does not authorize**
acquisition. The framework exists so the operator can see the governance
cost of any future acquisition before authorizing one and so any future
acquisition-readiness memo has a binding contract to satisfy.

### 8.1 Target calendar coverage

Any future acquisition-readiness memo must declare:

- the absolute lower bound below which expansion is not justified (and
  why);
- the absolute upper bound beyond which expansion no longer pays for
  itself (and why);
- whether the target is a single contiguous window, multiple separated
  windows, or both;
- the calendar-coverage rationale: why the chosen length and shape sample
  the regime questions the project actually wants to answer;
- the failure condition: what would constitute *insufficient* calendar
  coverage and would force the memo to recommend a different shape.

### 8.2 Single continuous window vs multiple separated windows

The memo must declare explicitly:

- which structural option is chosen (single contiguous, multiple
  separated, or both, with explicit rationale);
- if multiple separated windows: how inter-window gaps are treated, how
  train / validation / test chronology is enforced across windows, how
  each window's individual descriptive picture is recorded, and how the
  cross-window comparison is reported;
- if single contiguous: how the realized regime balance is documented and
  how the cost of a regime-monotonic window is reasoned about.

### 8.3 Volatility regimes

The memo must declare:

- which volatility regimes (low / medium / high; quiet / expansion /
  contraction) the acquisition is intended to sample;
- the operational definition of each regime (e.g., realized-volatility
  percentile bins; cost-commensurability fractions; conditional
  volatility from a published model);
- how the chosen target window is assessed as covering each regime;
- the failure condition: what would constitute a missed regime and what
  consequence that has.

### 8.4 Trend / range regimes

The memo must declare:

- whether trending and range-bound regimes at the 4h / daily / weekly
  scales must both be sampled;
- the operational definition of trend vs range (e.g., 4h / daily trend
  strength; weekly range vs trend);
- how trend / range coverage is verified;
- the failure condition.

### 8.5 Volume / activity regimes

The memo must declare:

- which activity regimes (per-day aggTrade count buckets; per-minute trade
  frequency) must be sampled;
- how the chosen target window covers them;
- how the Phase 4bn-E count-up / mean-quantity-down direction informs the
  required activity-coverage envelope;
- the failure condition.

### 8.6 Funding / derivatives-flow regimes

The memo must declare:

- which funding regimes (compressed, neutral, extreme positive, extreme
  negative) the target window samples;
- the operational definition (e.g., funding-rate percentile bins; Z-score
  of funding);
- the cross-link to D1-A and the project's funding evidence;
- the failure condition.

### 8.7 Intraday / weekday effects

The memo must declare:

- whether subtler intraday / weekday / session effects need a longer or
  multi-window envelope to surface;
- the operational definition;
- the failure condition.

### 8.8 Market-event concentration

The memo must declare:

- whether the target window must intentionally include or exclude specific
  market / macro / venue / on-chain / regulatory events;
- how events are operationally identified;
- how event concentration is reasoned about;
- the failure condition.

### 8.9 BTCUSDT-only limitation

The memo must declare:

- whether the acquisition remains BTCUSDT-only (the Phase 4bn-F default)
  or extends to ETHUSDT;
- if BTCUSDT-only: how the cross-symbol question is acknowledged but
  deferred;
- if extending to ETHUSDT: how the symbol scope is justified (the locked
  first secondary research symbol per `data-requirements.md`).

### 8.10 ETHUSDT comparison option

If ETHUSDT is added, the memo must declare:

- the per-symbol acquisition cost;
- the per-symbol governance cost (Phase 4bj-* / Phase 4bb-F / Phase 4bm-Q
  governance applied to the new symbol scope);
- the per-symbol storage cost;
- the cross-symbol reporting requirement.

### 8.11 Symbol scope

A combined statement covering §8.9 and §8.10: the final symbol scope, the
justification, and the explicit acknowledgement that symbols beyond
BTCUSDT and ETHUSDT are out of scope unless separately authorized.

### 8.12 Horizon scope

The memo must declare:

- whether the existing 15s and 60s horizons are preserved or extended;
- if extended: how 1s / 5s / longer-than-60s horizons are justified
  against the Phase 4bn-A §10 deferral reasoning (latency / tradability /
  cost-commensurability);
- whether any new horizon would trigger label / feature regeneration and,
  if so, what governance arc that requires.

### 8.13 Split allocation

The memo must declare:

- how additional history is allocated across train, validation, and test;
- whether multiple non-overlapping train / validation / test windows are
  produced or whether a single extended contiguous train / validation /
  test split is used;
- the rationale for the chosen allocation against the existing 45 / 30 /
  15 day split;
- explicit confirmation that the existing v002 sealed test holdout
  remains sealed (see §8.14).

### 8.14 Test-holdout preservation

The memo must declare verbatim:

- the existing v002 sealed test holdout (15 days; 2025-02-14 .. 2025-02-28;
  23,797,822 rows; `test_rows_loaded: 0`) **remains sealed**;
- no future acquisition phase, no future storage phase, and no future
  acquisition-readiness or storage-decision memo may read, inspect,
  evaluate, hash, design with, or unseal the existing v002 sealed test
  holdout;
- if any new test holdout is constructed, it follows the same
  single-use-terminal-evaluation policy and the new holdout is sealed by
  construction; opening either holdout requires a separately authorized
  terminal-holdout phase that does not exist and is not authorized.

### 8.15 Whether the existing v002 sealed test set remains untouched

Restated as a standalone binding requirement: **yes, the existing v002
sealed test set remains untouched** in every option discussed in this
memo. Any successor memo, any successor acquisition phase, and any
successor storage phase must record this preservation verbatim.

### 8.16 Label / feature family preservation vs v003 / successor family

The memo must declare:

- whether the existing v002 label and feature manifests are preserved
  (and therefore the new evidence is comparable to Phase 4bn-B and ETL
  re-derivability from Binance public sources is preserved) or whether a
  new label / feature family is required;
- if a new family is required: explicit acknowledgement that this
  triggers the Phase 4bj-* eligibility-gate governance arc, a new
  dataset-version bump per `dataset-versioning.md`, a new manifest
  design, a new sidecar design, a new feature kernel arc, and a new
  label kernel arc — all of which are *separately authorized* phases
  that do not exist;
- if preserved: explicit acknowledgement that the v002 feature surface (45
  computed features × split policy) and the v002 label family
  (strict-sign direction at 15s / 60s) are unchanged in semantics, and
  that any new data is generated under the same kernel.

### 8.17 Cost-commensurability under §11.6

The memo must declare:

- how the §11.6 fractions (15s 6.2 % > 1× / 1.6 % > 2× / 0.16 % > 5×; 60s
  18.3 % > 1× / 5.8 % > 2× / 0.93 % > 5×) are re-measured across the
  expansion window;
- what change in the fractions would constitute *new* evidence (vs
  consistent);
- explicit confirmation that the §11.6 round-trip cost lock (16 bps)
  remains untouched.

### 8.18 High-confidence calibration failure from Phase 4bn-C

The memo must declare:

- whether the longer-history acquisition could plausibly change the
  high-confidence over-confidence pattern (reliability gaps −0.061 to
  −0.392 in the 0.6 – 1.0 bins; the 0.8 – 0.9 bin's empirical accuracy
  0.4881 *below* the majority floor);
- what evidence would constitute that change;
- explicit acknowledgement that the calibration failure is a *specific*
  descriptive failure of the v002 linear baseline and that any
  recalibration / threshold-tuning / signal-conversion remains forbidden
  outside a separately authorized future phase.

### 8.19 Reproducibility from public Binance sources

The memo must declare:

- how every acquired artefact remains re-derivable from public Binance
  endpoints under the canonical Binance USDⓈ-M futures source policy
  (`docs/04-data/historical-data-spec.md`);
- how source-faithful raw storage is preserved alongside normalized /
  derived artefacts;
- explicit rejection of any acquisition shape that breaks
  re-derivability.

### 8.20 Sidecar / manifest implications

The memo must declare:

- whether each acquired artefact carries a canonical Phase 4bb-F sidecar
  (two-space separator between SHA and basename; refuse-overwrite;
  immutability);
- whether the manifest schema requires any new field (and, if so, how
  that field is governed);
- whether the manifest follows the existing `__vNNN` naming pattern
  (`dataset-versioning.md`);
- whether each manifest's `research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`, `diagnostics_authorized`, and
  `ml_authorized` invariants are preserved.

### 8.21 Disk footprint

The memo must declare:

- the realistic raw + normalized + feature + label disk footprint
  implied by the proposed expansion size at the proposed symbol scope;
- the scaling rule used (per-day cost × number of days × number of
  symbols, with adjustments for the relevant compression / partitioning
  policy);
- the comparison to the current v002 footprint;
- the implication for storage architecture (cross-link to §10).

### 8.22 Expected derivation time

The memo must declare:

- the realistic normalisation / feature / label derivation time on the
  proposed acquisition envelope;
- the Phase 4bn-E diagnostic runtime (553.6 s on 75 partitions, two
  passes) as the baseline scaling unit;
- the implication for query / IO patterns.

### 8.23 Expected query load

The memo must declare:

- the expected query patterns of any future descriptive memo, ML rerun,
  or backtest;
- whether the partitioned-Parquet layout meets those query patterns;
- the implication for whether DuckDB / compaction / database-cache
  options become more attractive at scale (cross-link to §10).

### 8.24 Exact stop conditions

The memo must declare:

- the exact conditions under which the acquisition stops (e.g., manifest
  validation fail; sidecar drift; Phase 4bb-F refuse-overwrite trigger;
  source-endpoint policy change; cost cap exceeded; disk-footprint
  cap exceeded; reproducibility check fail; gate failure on any acquired
  partition);
- the exact rollback policy if the acquisition stops mid-stream
  (immutability of partial acquisitions; sidecar policy; manifest
  policy);
- explicit acknowledgement that fail-closed is the default.

## 9. Candidate expansion shapes

Phase 4bn-G enumerates seven candidate expansion shapes below at design
level only. Each shape records (a) what question it answers, (b) what it
would require later, (c) expected storage impact, (d) expected governance
cost, (e) expected reproducibility implications, (f) what it risks, (g) what
it does not authorize now, and (h) whether it is recommended, not
recommended, or deferred. **No shape is selected for execution by Phase
4bn-G. No shape is authorized by Phase 4bn-G.** Each future executable
phase requires a separate operator authorization that satisfies
`docs/00-meta/process/phase-prompt-template.md`.

### Option A — Remain with current 90-day v002 envelope; no acquisition

- **What it answers.** Whether the project should treat the existing
  Phase 4bn-A through Phase 4bn-F descriptive evidence as the terminal
  evidence boundary for the v002 ML-baseline family.
- **What it would require later.** Nothing executable. Operator chooses
  pause as the recommended state and accepts that the current evidence is
  the project's recorded ML-baseline interpretation.
- **Expected storage impact.** None. The v002 envelope's footprint is
  already material; no marginal increase.
- **Expected governance cost.** None beyond the existing reports.
- **Expected reproducibility implications.** None; all v002 artefacts
  remain re-derivable from Binance public sources unchanged.
- **What it risks.** Permanently leaving open the question of whether the
  90-day window is sufficient or representative. Foreclosing future
  expansion options by inertia rather than by decision. Accepting the
  current high-confidence calibration failure as the standing baseline
  with no further measurement.
- **What it does not authorize now.** Anything executable.
- **Recommended / not recommended / deferred.** **Available** as a valid
  operator choice; Phase 4bn-G does not foreclose data-expansion options
  at governance level.

### Option B — Longer single continuous BTCUSDT aggTrades history

- **What it answers.** Whether a single longer contiguous BTCUSDT
  aggTrades history would change the descriptive picture (class
  prevalence, L2 / L1 lift, persistence calibration, calibration tail,
  §11.6 cost-commensurability fractions, train-vs-validation drift) and
  thus the Phase 4bn-C interpretation.
- **What it would require later.** A separately authorized docs-only
  acquisition-readiness memo per §8 that fully satisfies the
  requirements framework, followed by a separately authorized storage
  architecture decision per §10 that pre-decides the storage layer,
  followed by a separately authorized Tier 1 acquisition phase with full
  eligibility-gate / manifest / sidecar / successor-state governance for
  the expanded raw / normalized / feature / label / metrics artefacts.
  The acquisition would have to satisfy the §8 dimensions and the §10
  storage decision before any execution.
- **Expected storage impact.** Roughly linear in days × symbols. A
  doubling of calendar coverage doubles the raw, normalized, feature, and
  label per-day footprint at the current per-day cost. The acquisition
  envelope cap declared in the §8.21 memo would govern the absolute
  ceiling.
- **Expected governance cost.** A separately authorized
  acquisition-readiness memo (Tier 1, docs-only), a separately authorized
  storage-architecture memo (Tier 1, docs-only), a separately authorized
  acquisition phase (Tier 1, code + docs + local gitignored output), a
  separately authorized raw eligibility gate execution (Tier 3 batch if
  the existing Phase 4bb-C gate protocol covers it; Tier 1 if any new
  semantics), a separately authorized derived eligibility gate execution,
  a separately authorized feature kernel rerun, a separately authorized
  label kernel rerun, a separately authorized feature-family gate
  execution, a separately authorized label-family gate execution, a
  separately authorized successor-state recording phase per family. Each
  phase requires its own merge-closeout and narrow
  `current-project-state.md` update.
- **Expected reproducibility implications.** Preserved if the existing
  Binance USDⓈ-M futures source policy
  (`docs/04-data/historical-data-spec.md`) covers the longer window
  unchanged. If the source endpoint set changes (e.g., archive vs live)
  the acquisition-readiness memo must record the change and the
  per-`dataset-versioning.md` mandatory bump applies.
- **What it risks.** Trading more data acquisition cost (download time,
  disk footprint, derivation time, gate-evidence time) for a result whose
  predictive value is itself unknown (whether more data will change the
  Phase 4bn-C calibration tail or the §11.6 cost-commensurability
  fractions is itself an open question). Locking the project into a
  single longer contiguous history shape that may not sample multiple
  regimes well.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option C, D, E, F, or G.
- **Recommended / not recommended / deferred.** **Deferred.** Phase 4bn-G
  does not recommend this option directly; it must be preceded by a
  separately authorized acquisition-readiness memo and a separately
  authorized storage-architecture memo (or by the recommended combined
  successor; see §12).

### Option C — Multiple separated BTCUSDT regime windows

- **What it answers.** Whether multiple non-overlapping BTCUSDT windows
  intentionally sampling different volatility / trend / activity /
  funding / event regimes would surface differences from the v002
  envelope that the v002 envelope alone cannot.
- **What it would require later.** Same as Option B plus an explicit
  policy for inter-window gaps, an explicit policy for train / validation
  / test chronology across windows, and an explicit governance decision
  about whether the sealed test holdout from the v002 envelope is
  preserved as is (yes, per §8.14 / §8.15) or whether new test holdouts
  are constructed (each new holdout sealed by construction).
- **Expected storage impact.** Approximately the sum of per-window
  footprints; more total bytes than Option B at equal total calendar
  length because per-window manifests, per-window sidecars, per-window
  gate reports, and per-window successor-state add overhead. Storage
  layout (per-day partitioning preserved) does not change semantics, but
  it does multiply file count.
- **Expected governance cost.** Higher than Option B by one
  inter-window-policy decision plus per-window per-family gate evidence.
- **Expected reproducibility implications.** Preserved if every window's
  source endpoint set and acquisition protocol are unchanged. Per-window
  manifests must each record the locked source, schema, and
  transformation version.
- **What it risks.** More structural complexity than Option B; more
  governance evidence than Option B; more storage cost than Option B;
  more split-policy governance work than Option B.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option B, D, E, F, or G.
- **Recommended / not recommended / deferred.** **Deferred.** Phase 4bn-G
  does not recommend this option directly. It is potentially more
  informative than Option B if the question being asked is "what does
  multi-regime BTCUSDT microstructure look like", but it costs strictly
  more.

### Option D — BTCUSDT longer continuous history plus later ETHUSDT comparison

- **What it answers.** Whether the longer-history BTCUSDT picture
  (Option B) generalises to the locked first secondary research symbol
  (ETHUSDT), and how cross-symbol descriptive differences read against
  BTCUSDT.
- **What it would require later.** Option B plus a separately authorized
  acquisition-readiness memo for ETHUSDT, a separately authorized
  acquisition phase for ETHUSDT raw / normalized / feature / label /
  metrics artefacts under the same Phase 4bj-* / Phase 4bb-F / Phase
  4bm-Q governance, a separately authorized cross-symbol descriptive
  comparison memo. ETHUSDT acquisition follows Option B's full governance
  chain.
- **Expected storage impact.** Roughly the sum of Option B's per-symbol
  cost and ETHUSDT's per-symbol cost.
- **Expected governance cost.** Higher than Option B; effectively Option
  B's governance chain run twice (once per symbol) plus an additional
  cross-symbol descriptive comparison memo.
- **Expected reproducibility implications.** Preserved if both symbols
  remain under the Binance USDⓈ-M futures source policy.
- **What it risks.** More acquisition cost than Option B (because it
  doubles the symbol scope rather than only extending the calendar);
  cross-symbol descriptive comparison may not change the Phase 4bn-C
  interpretation if both symbols share the same regime; may overcommit
  to ETHUSDT before BTCUSDT longer history has shown whether longer
  history changes the picture at all.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option B, C, E, F, or G.
- **Recommended / not recommended / deferred.** **Deferred.** Phase 4bn-G
  does not recommend this option directly; the cross-symbol question is
  a valid open question, but is secondary to the calendar-coverage /
  regime-coverage question on BTCUSDT.

### Option E — Multiple BTCUSDT regime windows plus later ETHUSDT comparison

- **What it answers.** A combination of Option C (multi-regime BTCUSDT)
  and Option D's ETHUSDT comparison.
- **What it would require later.** Option C's full governance chain plus
  Option D's ETHUSDT addition.
- **Expected storage impact.** Highest of the BTCUSDT-extension family;
  approximately the sum of Option C's storage cost and an ETHUSDT
  equivalent.
- **Expected governance cost.** Highest of the BTCUSDT-extension family.
- **Expected reproducibility implications.** Preserved if every window
  and every symbol remain under the Binance USDⓈ-M futures source
  policy.
- **What it risks.** Highest total acquisition cost; highest governance
  cost; not necessarily proportionally more informative than Option C
  alone or Option D alone; may overcommit before the simpler shapes
  (Option B, Option C, Option D) have established the marginal-evidence
  return rate.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option B, C, D, F, or G.
- **Recommended / not recommended / deferred.** **Deferred.** Phase 4bn-G
  does not recommend this option directly; structurally rejected as a
  *first* expansion shape because the simpler shapes have not been tried
  first.

### Option F — Define a new v003 or successor dataset family later

- **What it answers.** Whether the existing v002 label / feature family
  is the right family for any longer-history or multi-regime expansion,
  or whether a new dataset family (v003 or other) is required to capture
  the descriptive picture the operator wants.
- **What it would require later.** A separately authorized docs-only
  family-design memo that satisfies the `dataset-versioning.md`
  mandatory-bump conditions; a separately authorized eligibility-gate /
  manifest-design / sidecar-design phase for the new family; a separately
  authorized acquisition phase; a separately authorized storage-
  architecture decision; full Phase 4bj-* governance for the new label
  family; full Phase 4bb-F sidecar / path discipline.
- **Expected storage impact.** Equivalent to Option B (single window)
  through Option E (multi-window multi-symbol) depending on the chosen
  envelope, plus the v003 family overhead. Because v003 introduces new
  schemas, sidecars, and manifests, the per-day storage footprint may
  differ slightly from v002.
- **Expected governance cost.** Highest of all shapes. Triggers a full
  new Phase 4bj-* / Phase 4bb-F / Phase 4bm-* governance arc for a family
  whose value has not been demonstrated.
- **Expected reproducibility implications.** Each new family must declare
  its source endpoint set, normalization logic, schema, partitioning, and
  manifest; the existing v002 family remains immutable.
- **What it risks.** Highest structural cost of any option in this list.
  May produce evidence that overlaps with what the v002 family already
  provides. Locks the project into v003 governance overhead before the
  v003 value is established.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option B, C, D, E, or G.
- **Recommended / not recommended / deferred.** **Not recommended at
  governance level until a future requirements memo demonstrates that
  the v002 family cannot answer the operator's question.** Phase 4bn-G
  treats v003 as a deferred-and-conditional option only.

### Option G — Close the ML-baseline arc

- **What it answers.** Whether the project should record a verdict that
  the v002 ML-baseline family is operationally closed for further bounded
  expansion under current evidence and that the descriptive results
  recorded by Phase 4bn-A through Phase 4bn-F stand as the project's
  ML-baseline evidence record. Closing the arc means **no further v002
  ML-baseline follow-up under this arc unless reopened by a separately
  authorized future phase**; it **does not delete evidence** and **does
  not close Prometheus**.
- **What it would require later.** A separately authorized docs-only
  closure memo whose authorization prompt names the closure memo and the
  closeout as the only allowed tracked files (plus the narrow
  `current-project-state.md` paragraph), and whose decision records the
  operational closure verdict. No source / test / script / manifest /
  sidecar / gate-report / successor-state mutation. No retained verdict
  revised. No project lock loosened. No M0 amendment.
- **Expected storage impact.** None.
- **Expected governance cost.** Low (one closure memo + closeout).
- **Expected reproducibility implications.** None; all existing v002
  artefacts remain immutable.
- **What it risks.** Recording a closure on the v002 ML-baseline family
  before the operator has decided whether the calibration failure and
  the cost-commensurability context could ever be changed by more data;
  closing prematurely on a question whose data-sufficiency answer is
  unknown.
- **What it does not authorize now.** Anything executable. Specifically,
  it does not authorize Option A, B, C, D, E, or F, and it does not
  authorize paper / shadow / live-readiness / deployment / exchange-write
  / production keys / Phase 5 / Phase 4 canonical.
- **Recommended / not recommended / deferred.** **Available** as a valid
  operator choice; not recommended as the default because Phase 4bn-G
  does not have the evidence to close the arc unilaterally.

### Summary table — candidate expansion shapes

| Option | What it answers | Authorizes now? | Storage impact | Governance cost | Reproducibility | Recommended? |
| --- | --- | --- | --- | --- | --- | --- |
| A — Remain with 90-day envelope | Treat current evidence as terminal | No | None | None | None | Available |
| B — Longer single continuous BTCUSDT | Whether longer single window changes the picture | No | ~Linear in days | High (full governance chain) | Preserved | Deferred |
| C — Multiple separated BTCUSDT windows | Whether multi-regime BTCUSDT changes the picture | No | Higher (per-window overhead) | Higher than B | Preserved | Deferred |
| D — BTCUSDT longer + ETHUSDT comparison later | Whether longer history generalises across symbols | No | ~2× Option B | ~2× Option B + comparison memo | Preserved | Deferred |
| E — Multi-regime BTCUSDT + ETHUSDT later | Combined multi-regime + cross-symbol | No | Highest of family | Highest of family | Preserved | Deferred (structurally rejected as a first shape) |
| F — New v003 / successor family | Whether v002 family is the wrong frame | No | Variable + v003 overhead | Highest | New family must declare reproducibility | Not recommended at governance level |
| G — Close the ML-baseline arc | Record operational closure verdict | No | None | Low | None | Available |

Every entry above is **No** for the "Authorizes now?" column. **Phase
4bn-G authorizes none of the options.**

## 10. Candidate storage architectures

Any future acquisition that exceeds the existing 90-day v002 envelope
would force the project to choose explicitly how the new artefacts are
stored. Phase 4bn-G enumerates six candidate storage architectures below
at design level only. Each architecture records (a) what it solves, (b)
what it does not solve, (c) disk-footprint implications, (d)
query-performance implications, (e) reproducibility implications, (f)
sidecar / manifest implications, (g) gitignore / non-commit implications,
(h) migration risk, and (i) whether it is recommended, not recommended,
or deferred. **No architecture is selected for execution by Phase 4bn-G.
No architecture is authorized by Phase 4bn-G.**

### Storage A — Current partitioned Parquet remains canonical

- **What it solves.** Reproducibility (re-derivable from Binance public
  sources unchanged), immutability (Phase 4bb-F sidecar / path policy
  preserved), compression (Parquet is already a compressed columnar
  format), and analytical query performance through DuckDB on Parquet.
- **What it does not solve.** Per-day partition file count can grow
  large at multi-year scale; some query patterns (full-history scans,
  multi-window joins) may benefit from a query layer or cache.
- **Disk-footprint implications.** None beyond what the acquisition
  envelope itself implies. Parquet is already compressed.
- **Query-performance implications.** Already good for the workloads
  Phase 4bn-B / 4bn-E exercised (per-day partition read; two-pass scan).
  Scales linearly with total partitions read; the Phase 4bn-E 553.6 s
  baseline on 75 partitions × 2 passes is the empirical scaling unit.
- **Reproducibility implications.** Preserved verbatim.
- **Sidecar / manifest implications.** Preserved verbatim (Phase 4bb-F
  canonical sidecar / path policy).
- **Gitignore / non-commit implications.** Preserved verbatim
  (`.gitignore:85: data/microstructure/`; `.gitignore:88: data/research/`).
- **Migration risk.** Zero (no migration).
- **Recommended / not recommended / deferred.** **Recommended as the
  baseline.** Any storage decision must preserve the current partitioned
  Parquet layout for the v002 envelope unchanged. Storage A is the
  default; the other storage options are evaluated *against* it.

### Storage B — Compacted Parquet with explicit compression / row-group / partition policy

- **What it solves.** Reduces file count per acquisition (per-week or
  per-month files instead of per-day); reduces metadata overhead on
  scans; may improve cold-cache scan performance on full-history
  queries; lets the project declare a single compression codec /
  dictionary policy / row-group size for the family.
- **What it does not solve.** Adds compaction-policy governance overhead
  (which codec, which dictionary, which row-group size, which
  partitioning key, which compaction trigger); makes per-day
  reproducibility harder if compaction loses the per-day boundary;
  changes some query patterns (per-day reads become per-window reads
  with row-group filtering).
- **Disk-footprint implications.** Modest reduction at best; Parquet is
  already compressed. The biggest savings come from declared dictionary
  / row-group / compression policy, not from file-count reduction
  alone.
- **Query-performance implications.** Mixed. Full-history scans may
  improve; targeted per-day reads may slow down depending on
  partitioning key.
- **Reproducibility implications.** Preserved only if the compaction is
  deterministic and the per-day source data is preserved alongside the
  compacted file (or trivially re-derivable from the raw zips). If
  compaction discards per-day boundaries entirely, re-derivability from
  Binance public sources becomes a multi-step process rather than a
  one-step one.
- **Sidecar / manifest implications.** Each compacted artefact requires
  its own canonical Phase 4bb-F sidecar; the per-day sidecars for the
  un-compacted source must remain unless the source is itself archived
  with explicit policy.
- **Gitignore / non-commit implications.** Preserved verbatim if the
  compacted artefacts live under `data/microstructure/` /
  `data/research/`.
- **Migration risk.** Material if existing artefacts are rewritten.
  Recommended only as a forward-looking acquisition policy, not as a
  retroactive rewrite of the v002 envelope.
- **Recommended / not recommended / deferred.** **Deferred.** Phase
  4bn-G does not recommend compaction directly; it must be preceded by
  a separately authorized storage-architecture memo that declares the
  exact compaction policy.

### Storage C — DuckDB querying Parquet in place

- **What it solves.** Provides a higher-level analytical query layer over
  the existing Parquet without copying data into a DuckDB database file.
  Lets the project write SQL queries that join across partitions and
  symbols without changing the source-of-truth Parquet layout.
- **What it does not solve.** Does not reduce disk footprint (the
  Parquet files remain canonical); does not change per-day reproducibility
  (Parquet remains the source); does not by itself improve cold-cache
  performance much beyond DuckDB's existing scan optimisations.
- **Disk-footprint implications.** Zero (no duplicate storage).
- **Query-performance implications.** Improved for SQL-shaped queries
  that benefit from DuckDB's optimiser; modest improvement for the
  per-partition scan workloads Phase 4bn-B / 4bn-E exercised; meaningful
  improvement for multi-partition joins, aggregations, and ad-hoc
  exploration.
- **Reproducibility implications.** Fully preserved. DuckDB is a query
  engine; Parquet remains the source of truth.
- **Sidecar / manifest implications.** None new. The sidecar / manifest
  policy applies to Parquet, not to the query engine.
- **Gitignore / non-commit implications.** None new (DuckDB does not
  require a database file when querying Parquet in place; any local
  `.duckdb` file would itself be gitignored under the same data
  namespace).
- **Migration risk.** Very low. DuckDB-in-place is the lowest-disruption
  storage option because it does not require any change to the existing
  Parquet layout, the manifests, or the sidecars.
- **Recommended / not recommended / deferred.** **Recommended as the
  preferred non-invasive query layer** if any future memo decides a
  query layer is needed. Storage C is fully compatible with Storage A
  (the current partitioned Parquet) and does not require migration.

### Storage D — DuckDB database file as a derived local research cache

- **What it solves.** Caches a subset of the Parquet data into a
  `.duckdb` database file for faster repeated queries; may speed up
  research iteration if the same Parquet partitions are scanned
  repeatedly.
- **What it does not solve.** Introduces a derived artefact whose
  reproducibility must be governed (the `.duckdb` file is *derived* from
  the canonical Parquet; it is not the source of truth; it is gitignored;
  it has its own sidecar / manifest implications); duplicates storage
  for cached data (and may *increase* total disk footprint, not reduce
  it); requires a cache-invalidation policy if the source Parquet
  changes.
- **Disk-footprint implications.** **Increases** total local disk
  footprint by the size of the cached subset. Parquet is already a
  compressed columnar format; a `.duckdb` database file is itself a
  columnar format with similar compression characteristics, so caching
  does not reduce storage — it duplicates it.
- **Query-performance implications.** Improved for repeated queries
  against the cached subset; uncached queries fall back to Storage A /
  C.
- **Reproducibility implications.** Preserved only if the cache is
  treated as derived (the source Parquet is authoritative; the cache
  must be re-derivable from the source). The cache must not become a
  silent source of truth.
- **Sidecar / manifest implications.** Each `.duckdb` cache file should
  carry a canonical Phase 4bb-F sidecar plus a manifest that records the
  source Parquet partitions, the source SHAs, the cache generation
  timestamp, and the cache schema.
- **Gitignore / non-commit implications.** Cache files must remain under
  `data/microstructure/` or `data/research/` with gitignore coverage; no
  cache file is ever committed.
- **Migration risk.** Material if any process treats the cache as the
  source of truth. Cache-invalidation bugs would silently corrupt
  research evidence.
- **Recommended / not recommended / deferred.** **Deferred.** Phase
  4bn-G does not recommend Storage D directly. A cache makes sense only
  after an acquisition envelope and query workload are defined that
  show repeated queries against the same partitions are the bottleneck;
  in the absence of that workload, Storage D risks duplicating storage
  for no gain. If ever recommended, it must be by a separately
  authorized storage-architecture memo that pre-declares the cache
  governance, invalidation policy, and reproducibility envelope.

### Storage E — SQLite only for runtime / control metadata, not large aggTrade research matrices unless separately justified

- **What it solves.** Provides a transactional, restart-safe local
  database for runtime control state, active trade state, order /
  protective-stop continuity, reconciliation runs, incidents, operator
  actions, daily loss state, drawdown state, and config / release
  references. This is the runtime-database role defined by
  `docs/08-architecture/database-design.md` (SQLite with WAL recommended
  for v1 runtime). SQLite is part of the safety system; it is not an
  analytical store.
- **What it does not solve.** SQLite is *not* a research-matrix engine
  and *not* an analytical query engine for large aggTrade matrices. Per
  the runtime-vs-research separation in `data-requirements.md` (Core
  Principle 7: "Research storage and runtime database are separate") and
  in `database-design.md` ("The live runtime database must not become
  the canonical historical kline store"), the runtime database must
  *not* be used to hold the v002 aggTrade matrices, the longer-history
  matrices, or any feature / label parquet. Conflating runtime and
  research storage creates a single point of failure and breaks the
  Phase 4aw / Phase 4bb-F invariants.
- **Disk-footprint implications.** Negligible for the runtime role;
  catastrophic if misused for research matrices (SQLite is not
  optimised for large columnar analytical workloads at the scale of
  aggTrade matrices).
- **Query-performance implications.** Excellent for the runtime role;
  poor for analytical workloads.
- **Reproducibility implications.** Different domain. The runtime DB is
  operational state, not research evidence. Research evidence remains in
  Parquet / DuckDB.
- **Sidecar / manifest implications.** Different domain. Runtime
  schema changes follow `docs/08-architecture/database-design.md`'s
  migration policy.
- **Gitignore / non-commit implications.** The runtime SQLite file is
  not part of `data/microstructure/` or `data/research/`; it follows the
  runtime-persistence policy.
- **Migration risk.** Zero for the runtime role (already the documented
  default); high if anyone proposes using SQLite for research matrices
  (would require explicit separate justification and would likely be
  rejected at governance review).
- **Recommended / not recommended / deferred.** **Preserved verbatim
  for the runtime role**; **structurally rejected for the research
  role** unless a future storage-architecture memo justifies the
  unification with an explicit per-`data-requirements.md` Core
  Principle 7 / `database-design.md` separation override (which it
  almost certainly should not).

### Storage F — Defer storage migration; keep current layout until a concrete acquisition plan exists

- **What it solves.** Keeps the project at its current zero-risk,
  zero-migration storage posture until a concrete acquisition plan
  defines the storage workload. Recognises that storage decisions are
  workload-driven and that absent a defined acquisition envelope, the
  storage choice is premature.
- **What it does not solve.** Does not pre-decide storage; the future
  storage decision still has to be made before any acquisition is
  executed.
- **Disk-footprint implications.** None (current footprint preserved).
- **Query-performance implications.** None (current performance
  preserved).
- **Reproducibility implications.** Fully preserved.
- **Sidecar / manifest implications.** Fully preserved.
- **Gitignore / non-commit implications.** Fully preserved.
- **Migration risk.** Zero (no migration).
- **Recommended / not recommended / deferred.** **Recommended as the
  default.** Storage F is the prudent posture in the absence of a
  concrete acquisition workload; it is fully compatible with Storage A
  and Storage C (the recommended baseline + non-invasive query layer)
  and with deferring Storage B (compaction) and Storage D (DuckDB cache)
  to a separately authorized future storage-architecture memo.

### Summary table — candidate storage architectures

| Storage | What it solves | Disk impact | Query impact | Reproducibility | Migration risk | Recommended? |
| --- | --- | --- | --- | --- | --- | --- |
| A — Current partitioned Parquet | Reproducibility, immutability, compression | None new | Existing baseline | Preserved | Zero | Recommended as baseline |
| B — Compacted Parquet | File count reduction, codec / row-group policy | Modest reduction at best | Mixed | Preserved if deterministic | Material (if rewriting existing) | Deferred |
| C — DuckDB querying Parquet in place | Higher-level SQL query layer | None | Improved for SQL shapes | Preserved | Very low | Recommended as preferred non-invasive query layer |
| D — DuckDB database file as derived local research cache | Repeated-query acceleration | **Increases** total | Improved for cached subset | Preserved only if cache is treated as derived | Material (cache-invalidation bugs) | Deferred |
| E — SQLite for runtime / control metadata | Runtime safety system | Negligible (runtime); catastrophic (research) | Excellent (runtime); poor (research) | Different domain | Zero (runtime); high (research) | Preserved verbatim for runtime; structurally rejected for research |
| F — Defer migration; keep current layout | Workload-driven posture | None | None | Preserved | Zero | Recommended as default |

## 11. Coupled data-and-storage decision matrix

The seven candidate expansion shapes (§9) cross with the six candidate
storage architectures (§10) into the matrix below. Each cell classifies
the combination as **compatible** (the two options can coexist without
authorization issues), **compatible but deferred** (the combination is
admissible at design level but must be preceded by a separately authorized
acquisition-readiness or storage-architecture memo), **not recommended**
(the combination is technically possible but structurally weak), or
**structurally rejected** (the combination violates a project lock or a
governance invariant).

**This matrix is decision-support only. It does not authorize any
combination. No row / column / cell of this matrix authorizes any
execution.**

| Expansion ↓ \\ Storage → | A (Parquet canonical) | B (Compacted Parquet) | C (DuckDB on Parquet in place) | D (DuckDB cache file) | E (SQLite for runtime only) | F (Defer migration) |
| --- | --- | --- | --- | --- | --- | --- |
| **A — Remain with 90-day v002** | Compatible | Not recommended (no workload to justify) | Compatible (low-disruption query layer) | Not recommended (no workload to justify) | Compatible (runtime role only) | Compatible (preferred) |
| **B — Longer continuous BTCUSDT** | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible (runtime role only) | Compatible but deferred |
| **C — Multiple separated BTCUSDT** | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible (runtime role only) | Compatible but deferred |
| **D — BTCUSDT longer + ETHUSDT** | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible (runtime role only) | Compatible but deferred |
| **E — Multi-regime BTCUSDT + ETHUSDT** | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible (runtime role only) | Compatible but deferred |
| **F — New v003 / successor family** | Compatible but deferred (and not recommended at governance level until v002 inadequacy is shown) | Compatible but deferred | Compatible but deferred | Compatible but deferred | Compatible (runtime role only) | Compatible but deferred |
| **G — Close the ML-baseline arc** | Compatible | Not applicable (no new workload) | Compatible | Not applicable (no new workload) | Compatible (runtime role only) | Compatible (preferred) |

**Structurally rejected combinations (cross-cutting):**

- Any combination that places research matrices in Storage E (SQLite
  research role) is **structurally rejected** per `data-requirements.md`
  Core Principle 7 and `database-design.md` ("The live runtime database
  must not become the canonical historical kline store"). The Storage E
  column above lists "runtime role only"; using SQLite for research
  matrices requires a separately authorized storage-architecture memo
  that defends the unification against the existing separation, and that
  defence would almost certainly fail at governance review.
- Any combination that modifies the v002 envelope's existing partitioned
  Parquet layout retroactively (e.g., re-compacting the existing v002
  artefacts in place) is **structurally rejected** because the v002
  envelope is the project's only ML-baseline evidence and is
  immutability-locked under Phase 4bb-F.
- Any combination that breaks re-derivability from Binance public sources
  is **structurally rejected** per the §8.19 requirement and per
  `historical-data-spec.md`.
- Any combination that requires `data/microstructure/` or `data/research/`
  artefacts to be committed to the repository is **structurally rejected**
  per `.gitignore:85: data/microstructure/` and `.gitignore:88:
  data/research/`.

**Preferred combinations under Phase 4bn-G's design-level read:**

- **A (Parquet canonical) + F (defer migration) + C (DuckDB in place as
  query layer if needed)** is the lowest-disruption baseline and is
  compatible with every expansion shape. It is the default posture.
- For Option A (remain with 90-day v002), the preferred storage is
  **A + F**, with **C** available as a query convenience.
- For Options B – F (any expansion shape), the preferred storage is
  **A (canonical) + C (query layer)** plus a separately authorized
  storage-architecture memo that decides whether B (compaction) or D
  (cache file) is justified by the acquisition envelope's specific
  workload. **No combination is authorized.**

## 12. Recommended future expansion / storage path, if any

### 12.1 What the repository evidence supports

The repository evidence supports the following design-level reading:

1. **The Phase 4bn-F recommendation is correct as stated.** The Phase
   4bn-E descriptive feature-drift result does not, by itself, close the
   data-sufficiency question. The Phase 4bn-C calibration failure does
   not, by itself, close the sufficiency question in either direction.
   The Phase 4bn-B descriptive evidence is non-trivial but is not edge.
   Whether 90 days is enough or is an outlier is *unresolved*.
2. **Acquiring more data without a requirements memo is structurally
   premature.** Acquisition cost is high enough that the §8 dimensions
   deserve an explicit per-dimension decision before the operator commits
   to acquisition.
3. **Migrating storage without an acquisition envelope is structurally
   premature.** Storage decisions are workload-driven; absent a defined
   acquisition envelope, the storage workload is unknown, and the
   storage choice (compaction codec, row-group size, partitioning key,
   query engine, cache policy) cannot be made on real evidence.
4. **Parquet is already a compressed columnar format.** A `.duckdb`
   database file is itself a columnar format with similar compression
   characteristics. Replacing Parquet with DuckDB does not reduce disk
   footprint and may *increase* it. Compression policy (codec,
   dictionary, row-group size) typically has a larger impact than the
   storage-layer choice within the columnar family. The right question
   is rarely "Parquet vs DuckDB" — it is usually "what compression
   policy, what partitioning key, what file size target, and what query
   engine".
5. **DuckDB querying Parquet in place (Storage C) is the lowest-risk
   query-layer upgrade.** It does not duplicate storage. It does not
   require migration. It preserves reproducibility. It is fully
   compatible with the existing Phase 4bb-F sidecar / path policy and
   with the existing `__vNNN` dataset-versioning naming.
6. **A derived DuckDB database cache (Storage D) may *duplicate*
   storage** rather than reduce it. Deferring Storage D until the
   acquisition envelope and query workload are defined is prudent.
7. **Compacted Parquet (Storage B) may help query performance and
   file-count overhead at scale**, but the codec / dictionary / row-group
   / partitioning decisions should not be made until the acquisition
   envelope and query workload are defined. Compaction is a forward-only
   policy for any future acquisition; retroactively rewriting existing
   v002 artefacts is structurally rejected.
8. **The runtime vs research separation is binding.** SQLite for runtime
   control state is correct; SQLite for research matrices is rejected.
   This separation is preserved verbatim.
9. **Closing the ML-baseline arc (Option G) is a valid operator choice
   but is not what the evidence forces.** No stop-work-level negative
   evidence has been produced; the descriptive results are non-trivial
   enough that a future scoping memo on data-sufficiency may legitimately
   change the interpretation.
10. **Remaining paused (Option A) is a valid operator choice but does not
    address the data-sufficiency question that the operator originally
    raised.** Phase 4bn-F's recommendation that the question deserves a
    combined memo is supported by the repository evidence.

### 12.2 Recommended path

Phase 4bn-G's recommendation, based on the repository evidence read
above:

**Recommend a future docs-only acquisition-readiness memo that keeps
Parquet as canonical (Storage A) and evaluates DuckDB querying Parquet
in place (Storage C) as the preferred non-invasive query layer, while
deferring any DuckDB database-cache (Storage D) or Parquet-compaction
(Storage B) decision until there is a concrete acquisition envelope.**

This recommendation crystallises the §11 preferred combination
**A + F + C** as the design-level baseline and selects a docs-only
acquisition-readiness memo as the cleanest next docs-only / design-only
/ scoping-only successor path, subject to separate operator
authorization.

Rationale (anchored to §5 – §11):

1. Parquet remains canonical and reproducible.
2. DuckDB in-place querying is low-disruption.
3. A derived DuckDB database cache may duplicate storage rather than
   reduce it.
4. Parquet compaction may help query performance and file-count overhead,
   but should not be decided until the acquisition envelope and query
   workload are defined.
5. Acquisition itself is still not authorized.
6. The recommended acquisition-readiness memo is itself docs-only /
   design-only / scoping-only; it would not acquire data, would not
   migrate storage, would not create a database, would not compact
   Parquet, would not create a v003 dataset, and would not authorize any
   downstream execution.
7. The operator may equivalently remain paused, request a merge prompt
   for Phase 4bn-G, reject further successors and close the ML arc,
   separately authorize only a future docs-only storage-architecture
   decision memo (Storage B / C / D only), or separately authorize a
   future docs-only combined acquisition-readiness + storage-decision
   memo (the same scope as Phase 4bn-G but one level lower in
   abstraction, focused on a specific acquisition shape).
8. Phase 4bn-G does not foreclose any of these alternatives.

### 12.3 Why this is the recommendation and not Option G (close the arc)

The Phase 4bn-F evidence is consistent with two contradictory readings:
the 90-day envelope is a stable quietly-uneventful window (in which case
more data could change the picture) **and** the 90-day envelope is
representative of long-run BTCUSDT futures microstructure (in which case
more data would converge on the same descriptive shape). Closing the arc
under Option G would resolve this ambiguity by *recording the closure as
the project's verdict* — which over-claims confidence in the negative
direction. The recommended path defers the resolution to a future
docs-only acquisition-readiness memo that, in turn, would not authorize
acquisition by itself; the operator retains the option to remain paused
or to close the arc at any later point.

### 12.4 Why this is the recommendation and not Option B / C / D / E / F (direct acquisition)

Direct acquisition would require both the acquisition-readiness
requirements decision and the storage-architecture decision to be made
inside the acquisition phase, which would conflate three things
(acquisition design, storage design, acquisition execution) into one
phase. The Phase 4bn-F memo specifically recommended decoupling
acquisition design from acquisition execution; Phase 4bn-G preserves
that decoupling by recommending only the docs-only acquisition-readiness
memo, with the storage-architecture memo provided as an equally valid
operator alternative.

## 13. Required pre-acquisition gates

Before any future acquisition is authorized, the following gates must be
in place. Phase 4bn-G **records** these gates; it **does not pre-decide**
them.

1. **Acquisition-readiness memo present in `main`.** Either Phase 4bn-G
   plus a separately authorized acquisition-readiness memo (the
   recommended successor), or Phase 4bn-G plus a separately authorized
   combined acquisition-readiness + storage-decision memo. The memo must
   satisfy §8 in full and must declare an exact acquisition envelope.
2. **Storage-architecture decision present in `main`.** Either the
   separately authorized storage-architecture memo or the combined memo.
   The decision must satisfy §10 in full and must declare the exact
   storage layer.
3. **Source-policy preservation.** The Binance USDⓈ-M futures source
   policy (`historical-data-spec.md`) must apply to the acquisition
   target unchanged, or any divergence must be governed by a separately
   authorized source-policy memo.
4. **`__vNNN` naming policy.** The new acquisition must follow
   `dataset-versioning.md` (`__vNNN` pattern; manifests; immutability;
   experiment linkage).
5. **Phase 4bb-F canonical sidecar / path policy.** The acquisition must
   produce canonical sidecars (`<sha>  <basename>\n` two-space separator;
   refuse-overwrite) and canonical paths
   (`data/microstructure/<family-subdir>/...`).
6. **Phase 4aw `flip_research_eligible(...)` always-raises invariant.**
   No acquisition phase may invoke `flip_research_eligible`; the
   invariant must remain (never invoked).
7. **Eligibility-gate envelope.** A separately authorized raw eligibility
   gate execution per acquired symbol / family / version. If the
   existing Phase 4bb-C gate protocol covers it, the execution may be a
   Tier 3 batch; if any new semantics, a Tier 1 phase.
8. **Manifest invariants.** Every acquired family's manifest must start
   at `research_eligible: false`, `eligibility_gate_status: "pending"`,
   `chronological_split_policy: "not_yet_defined"`,
   `diagnostics_authorized: false`, `ml_authorized: false`. No
   transition of any of these is authorized by the acquisition phase
   itself.
9. **Successor-state recording.** A separately authorized successor-state
   recording phase per family.
10. **Test-holdout preservation.** The existing v002 sealed test holdout
    remains sealed. Any new test holdout is sealed by construction. No
    acquisition phase reads any sealed test partition.
11. **Reproducibility check.** Every acquired artefact must be
    re-derivable from public Binance sources at the source-policy lock
    in §13.3.
12. **Disk-footprint cap.** The acquisition-readiness memo's declared
    disk-footprint cap must be honoured; if exceeded, the acquisition
    stops.
13. **Cost cap.** The acquisition-readiness memo's declared cost cap
    (acquisition time, derivation time, gate-evidence time) must be
    honoured; if exceeded, the acquisition stops.
14. **Fail-closed default.** Any acquisition error fails closed; no
    partial artefact is treated as canonical without explicit
    eligibility-gate evidence.

## 14. Required pre-storage-migration gates

Before any future storage migration is authorized, the following gates
must be in place. Phase 4bn-G **records** these gates; it **does not
pre-decide** them.

1. **Storage-architecture memo present in `main`.** Either a separately
   authorized storage-architecture memo or the combined acquisition-
   readiness + storage-decision memo. The memo must satisfy §10 in full
   and must declare exactly which Storage A / B / C / D / E / F option
   is chosen and the exact migration protocol.
2. **Acquisition workload defined.** No storage migration may be
   authorized in the absence of a defined acquisition workload. Storage
   decisions are workload-driven.
3. **Reproducibility preservation.** Every migrated artefact must remain
   re-derivable from Binance public sources unchanged; any storage
   choice that breaks re-derivability is structurally rejected.
4. **Sidecar / manifest preservation.** Every migrated artefact must
   carry a canonical Phase 4bb-F sidecar (including a fresh sidecar for
   each new file) and an appropriately versioned manifest.
5. **Immutability of existing v002 envelope.** No migration may rewrite
   existing v002 artefacts in place. The v002 envelope is
   immutability-locked under Phase 4bb-F and the Phase 4bn-A through
   Phase 4bn-F evidence chain.
6. **Gitignore coverage.** Every migrated artefact must remain under
   `data/microstructure/` or `data/research/` with gitignore coverage
   (`.gitignore:85`, `.gitignore:88`). No artefact is ever committed.
7. **Cache-invalidation policy (if Storage D).** Any DuckDB cache must
   declare its cache-invalidation policy, its source-of-truth reference
   (canonical Parquet), and its sidecar / manifest policy.
8. **Runtime / research separation (if Storage E).** SQLite is preserved
   verbatim for the runtime role only; using SQLite for research
   matrices requires explicit override against `data-requirements.md`
   Core Principle 7 and `database-design.md`, which Phase 4bn-G
   structurally rejects.
9. **Migration rollback.** Every migration phase must declare its
   rollback policy (how to restore the pre-migration state if the
   migration fails or produces unexpected behaviour).
10. **No silent rewrite.** Every migration must be auditable; every
    rewritten artefact must record its pre-migration SHA, post-migration
    SHA, and an explicit re-derivability proof.

## 15. Required non-authorization envelope for any successor

Any future successor recommended by Phase 4bn-G (the docs-only
acquisition-readiness memo per §12, or any equivalent under any name)
must honour the following non-authorization envelope verbatim:

1. **Docs-only / design-only / scoping-only.** The successor must not
   acquire data, must not migrate storage, must not create a database,
   must not compact Parquet, must not create a v003 dataset, must not
   modify dataset layout, must not run ML, must not train models, must
   not score models, must not generate predictions, must not run
   diagnostics, must not run backtests, must not generate signals, and
   must not simulate PnL.
2. **No source / test / committed-script / configuration / manifest /
   sidecar / gate-report / successor-state mutation.**
3. **No local data artefact creation or mutation.**
4. **No test-holdout access** for training, fitting, calibration,
   evaluation, tuning, design, model selection, threshold selection,
   reporting, or inspection.
5. **No public, authenticated, or private endpoint calls.**
6. **No WebSocket or user stream.**
7. **No credentials, `.env`, `.mcp.json`, MCP, or Graphify.**
8. **No `research_eligible` flip, `eligibility_gate_status` transition,
   `chronological_split_policy` change, `diagnostics_authorized`
   transition, or `ml_authorized` transition** on any actual manifest.
9. **No retained verdict revision.**
10. **No project lock loosening.**
11. **No M0 amendment.**
12. **No authorization of any further successor.** Each successor memo
    must explicitly recommend a remain-paused default and may only
    recommend (not authorize) a downstream phase, which itself requires
    separate operator authorization.
13. **No commit under `data/microstructure/` or `data/research/`.**

## 16. Decision

**`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Rationale (anchored to §5 – §15):

1. The Phase 4bn-F recommendation to combine the data-expansion
   requirements and storage-scaling architecture questions is honoured
   by this memo; Phase 4bn-G *is* the combined scoping memo.
2. The combined scoping (this memo) has now been recorded; the next
   docs-only / design-only / scoping-only successor is a more concrete
   acquisition-readiness memo focused on a specific expansion shape
   (most plausibly Option B — longer continuous BTCUSDT, with Option A
   and Option G as equally valid operator alternatives at that later
   stage). The recommended successor is **docs-only / design-only /
   scoping-only** and authorizes nothing executable.
3. The recommended path keeps Parquet canonical (Storage A) and DuckDB
   in place (Storage C) as the preferred non-invasive query layer,
   deferring any compaction or cache decision; this design-level
   recommendation is recorded inside this memo without authorising any
   migration.
4. The operator may equivalently choose any of: remain paused; request
   a merge prompt for Phase 4bn-G; reject further ML-baseline successors
   and close the ML arc; separately authorize only a future docs-only
   storage-architecture decision memo (without the acquisition-readiness
   memo); separately authorize a future docs-only combined acquisition-
   readiness + storage-decision memo (the same recommendation pattern
   one level lower in abstraction); separately authorize the
   recommended docs-only acquisition-readiness memo. Phase 4bn-G does
   not foreclose any of these alternatives.
5. Phase 4bn-G is recommendation-only. **The successor is not authorized
   by Phase 4bn-G.** A separate operator authorization is required for
   any executable follow-up.

## 17. Recommended state and successor options

**Recommended state: remain paused.**

Phase 4bn-G is **recommendation-only** and does not authorize any
successor. The operator may equivalently choose any of the following:

- **remain paused** (default; no successor authorized; Phase 4bn-G's
  recommendation does not pressure the operator to authorize a
  successor);
- **request a merge prompt for Phase 4bn-G** so the combined
  data-expansion + storage-scaling scoping decision becomes
  project-complete on `main`;
- **reject further ML-baseline successors and close the ML arc**
  (operationally close the v002 ML-baseline family for further bounded
  expansion under current evidence; preserve all Phase 4bn-A / 4bn-B /
  4bn-C / 4bn-D / 4bn-E / 4bn-F artefacts as research evidence; preserve
  every retained verdict and project lock; no further v002 ML-baseline
  follow-up under this arc unless reopened by a separately authorized
  future phase; does not delete evidence; does not close Prometheus);
- **separately authorize a future docs-only acquisition-readiness memo
  (recommended)** that pre-declares the §8 requirements framework for a
  specific expansion shape (most plausibly Option B); must remain
  docs-only and design-only; must not authorize any acquisition; must
  not authorize any storage migration; must not create a database;
  must not compact Parquet; must not create a v003 dataset; must not
  mutate any manifest, sidecar, gate report, or successor-state
  artefact;
- **separately authorize a future docs-only storage-architecture
  decision memo only** (without the acquisition-readiness memo); this
  is a weaker variant of the recommended path and is provided as an
  operator alternative; must remain docs-only and must not authorize
  any storage migration;
- **separately authorize a future docs-only combined acquisition-
  readiness + storage-decision memo** (one level lower in abstraction
  than Phase 4bn-G; same recommendation pattern; same docs-only
  constraints).

**No acquisition / paper / shadow / live / exchange-write option is
valid from this state.**

## 18. Explicit non-authorizations

Phase 4bn-G is docs-only / design-only / scoping-only and authorizes
**nothing executable**. It does not, and cannot, authorize:

- any data acquisition (no additional days / symbols / families /
  horizons beyond the locked 90-day v002 envelope; no longer single
  contiguous history; no multiple separated windows; no ETHUSDT or
  other comparison-symbol acquisition; no v003 dataset; no successor
  dataset family; no mark-price / spot / cross-venue / order-book /
  additional aggTrades; no longer-horizon labels; no barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels; no new
  feature engineering; no new label engineering);
- any storage migration (no Parquet → DuckDB / SQLite / other database
  migration; no Parquet compaction; no per-day → per-week / per-month
  partition restructuring; no new compression codec / dictionary /
  row-group policy applied to existing artefacts; no derived `.duckdb`
  database file creation; no SQLite database file creation; no other
  database file creation);
- any ML training, model scoring, prediction generation, feature
  ranking, feature selection, feature pruning, model selection through
  results, hyperparameter tuning, threshold tuning, calibrator fitting,
  meta-labeling, ensemble construction, or any other ML execution;
- any strategy research, strategy design, signal generation,
  trade-signal generation, PnL simulation, equity-curve construction,
  Sharpe / Sortino / drawdown / hit-rate / trade-PnL metrics, backtests,
  or walk-forward optimization;
- any use of the test holdout for training, fitting, calibration,
  evaluation, tuning, design, model selection, threshold selection,
  reporting, or inspection;
- any diagnostics rerun, diagnostic artefact creation, ML artefact
  creation, reusable split-mask materialization, row-level prediction
  persistence, or model-binary persistence;
- any public / authenticated / private endpoint call; any WebSocket /
  user stream; any credential / `.env` / `.mcp.json` / MCP / Graphify
  use;
- any manifest mutation, successor-state mutation, gate-report
  mutation, or change to `research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`, `diagnostics_authorized`, or
  `ml_authorized` on any on-disk manifest;
- any source / test / committed-script / config / `.gitignore` /
  `pyproject.toml` / `README.md` / MCP-file modification;
- any commit under `data/microstructure/` or `data/research/`;
- Phase 4bn-H (or any phase under any name performing the recommended
  docs-only acquisition-readiness memo, or any docs-only
  storage-architecture decision memo, or any docs-only combined
  acquisition-readiness + storage-decision memo, or any acquisition
  phase, or any storage-migration phase, or any database-creation
  phase, or any v003-creation phase);
- any further Phase 4bn-* successor / Phase 4bo-* / Phase 4bp-*;
  Phase 5; Phase 4 canonical;
- paper / shadow; live-readiness; deployment; exchange-write;
  production-key creation; authenticated APIs; private endpoints; user
  stream; WebSocket implementation;
- any revision of a retained verdict, any loosening of a project lock,
  or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F /
  Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bn-G is a docs-only / design-only / scoping-only combined
data-expansion requirements + storage-scaling architecture scoping
memo.** **Phase 4bn-G does not acquire data.** **Phase 4bn-G does not
run diagnostics.** **Phase 4bn-G does not run ML.** **Phase 4bn-G does
not train models.** **Phase 4bn-G does not score models.** **Phase 4bn-G
does not generate predictions.** **Phase 4bn-G does not inspect the test
holdout.** **Phase 4bn-G does not use the sealed test split.** **Phase
4bn-G does not rank features.** **Phase 4bn-G does not select
features.** **Phase 4bn-G does not prune features.** **Phase 4bn-G does
not engineer features.** **Phase 4bn-G does not tune hyperparameters.**
**Phase 4bn-G does not tune thresholds.** **Phase 4bn-G does not fit
calibrators.** **Phase 4bn-G does not run strategy research.** **Phase
4bn-G does not define a strategy.** **Phase 4bn-G does not generate
trade signals.** **Phase 4bn-G does not simulate PnL.** **Phase 4bn-G
does not run backtests.** **Phase 4bn-G does not authorize
acquisition.** **Phase 4bn-G does not authorize storage migration.**
**Phase 4bn-G does not create a v003 dataset.** **Phase 4bn-G does not
create a database.** **Phase 4bn-G does not compact Parquet.** **Phase
4bn-G does not modify dataset layout.** **Phase 4bn-G does not call any
public, authenticated, or private endpoint.** **Phase 4bn-G does not
open any WebSocket or user stream.** **Phase 4bn-G does not use
credentials, `.env`, `.mcp.json`, MCP, or Graphify.** **Phase 4bn-G does
not mutate any manifest.** **Phase 4bn-G does not mutate any
successor-state artefact.** **Phase 4bn-G does not commit
`data/microstructure`.** **Phase 4bn-G does not commit `data/research`.**
**Phase 4bn-G does not authorize Phase 4bn-H, Phase 5, paper / shadow,
live-readiness, deployment, exchange-write, production keys, or any
successor phase.**

## 19. Current-project-state update summary

The narrow `docs/00-meta/current-project-state.md` update made by Phase
4bn-G consists of:

- a new Phase 4bn-G paragraph appended immediately after the Phase 4bn-F
  paragraph;
- a new Current-phase block for Phase 4bn-G inserted immediately after
  the new Phase 4bn-G paragraph and immediately before the existing
  Phase 4bn-F Current-phase block;
- preservation of every earlier paragraph (Phase 4a .. Phase 4bn-F) and
  every earlier Current-phase block (Phase 4bn-F, Phase 4bn-E, Phase
  4bn-D, Phase 4bn-C, Phase 4bn-B, and older blocks) as labelled
  historical context;
- recording of Phase 4bn-G as **branch-complete only, not merged, not
  project-complete**;
- recording of the Phase 4bn-G decision
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
- recording of the exact non-authorizations (per §0 / §3 / §18 of this
  memo);
- recording of the recommended state (**remain paused**);
- explicit statement that a Phase 4bn-H successor (or any equivalent
  under any name) is recommended but **not authorized** by Phase 4bn-G.

No other section of `docs/00-meta/current-project-state.md` is modified
by Phase 4bn-G. No retained verdict, project lock, manifest field,
successor-state field, gate-report field, or governance label is
changed. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked by Phase 4bn-G).

---

## Appendix A — Retained verdicts preserved

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

All prior phase results (Phase 4am .. Phase 4bn-F) preserved verbatim.

## Appendix B — Project locks preserved

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
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant (never invoked by Phase 4bn-G)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule +
  nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## Appendix C — Recommended next state

**Remain paused.** Phase 4bn-G is branch-complete only by this work. Per
the `phase-workflow-standard.md` rule, it is NOT project-complete until
a separately authorized merge phase records its merge-closeout on
`main` per `merge-closeout-standard.md` (Tier 1). The scoping decision
`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
is a recommendation only and authorizes nothing. **Phase 4bn-H (or any
equivalent under any name) is not authorized by Phase 4bn-G.** **Any
acquisition phase requires a separately authorized phase.** **Any
storage-migration phase requires a separately authorized phase.** **Any
v003-creation phase requires a separately authorized phase.** **Any
database-creation phase requires a separately authorized phase.** **Any
Parquet-compaction phase requires a separately authorized phase.**
**Recommended state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-H docs-only /
design-only / scoping-only acquisition-readiness memo (focused on a
specific expansion shape, most plausibly Option B — longer continuous
BTCUSDT, keeping Parquet canonical and DuckDB in place as the preferred
non-invasive query layer) is the cleanest non-paused option. It would,
if separately authorized later, pre-declare the §8 requirements
framework for the chosen expansion shape, declare an exact acquisition
envelope, and record an explicit non-authorization for both acquisition
and storage migration. Phase 4bn-H is **not authorized** by this memo.
The operator may equivalently choose to remain paused, to reject further
successors and close the ML arc, to separately authorize only a
docs-only storage-architecture decision memo, or to separately
authorize a docs-only combined acquisition-readiness + storage-decision
memo; Phase 4bn-G does not foreclose any of these alternatives.
