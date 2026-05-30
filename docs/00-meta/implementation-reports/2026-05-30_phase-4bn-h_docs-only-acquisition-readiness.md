# Phase 4bn-H — Docs-Only Acquisition-Readiness Memo

**Phase identity:** Phase 4bn-H — Docs-Only Acquisition-Readiness Memo (docs-only
/ design-only / scoping-only governance memo; Tier 1 — Full Phase per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3; the separately
authorized scoping phase that follows the Phase 4bn-G recommendation
`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`).
**Date:** 2026-05-30.
**Branch:** `phase-4bn-h/docs-only-acquisition-readiness`.
**Base SHA:** `main` at `1ab9ebea5b959764c9cfc6821245103ceb301ffa` (Phase 4bn-G
SHA-finalization commit `docs(phase-4bn-g): finalize merge closeout shas`;
pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3. Phase 4bn-H is
adjacent to possible future data acquisition, longer-history microstructure
planning, possible storage workload definition, possible future ML-baseline
downstream admissibility, and possible future regime / outlier interpretation,
while explicitly authorizing none of them.
**Phase type:** docs-only / design-only / scoping-only. Adds two new tracked
docs files under `docs/00-meta/implementation-reports/` (this memo + the
paired closeout) and narrowly updates
`docs/00-meta/current-project-state.md`. **No** source / test /
committed-script / configuration / manifest / sidecar / gate-report /
successor-state mutation. **No** local data artefact created or mutated.
**No** diagnostic rerun. **No** ML rerun. **No** ML artefact. **No**
acquisition. **No** storage migration. **No** database creation. **No**
Parquet compaction. **No** v003 dataset creation. **No** successor
authorization.
**Status:** drafted; pending operator review. Branch-complete only by this
work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bn-H is a docs-only / design-only / scoping-only
  acquisition-readiness memo.**
- **Phase 4bn-H does not acquire data.**
- **Phase 4bn-H does not migrate storage.**
- **Phase 4bn-H does not create any database.**
- **Phase 4bn-H does not compact Parquet.**
- **Phase 4bn-H does not create v003.**
- **Phase 4bn-H does not authorize acquisition.**
- **Phase 4bn-H does not authorize any successor.**
- **Phase 4bn-H does not run diagnostics.**
- **Phase 4bn-H does not run ML.**
- **Phase 4bn-H does not train models.**
- **Phase 4bn-H does not score models.**
- **Phase 4bn-H does not generate predictions.**
- **Phase 4bn-H does not inspect the test holdout.**
- **Phase 4bn-H does not use the sealed test split.**
- **Phase 4bn-H does not rank features.**
- **Phase 4bn-H does not select features.**
- **Phase 4bn-H does not prune features.**
- **Phase 4bn-H does not engineer features.**
- **Phase 4bn-H does not tune hyperparameters.**
- **Phase 4bn-H does not tune thresholds.**
- **Phase 4bn-H does not fit calibrators.**
- **Phase 4bn-H does not run strategy research.**
- **Phase 4bn-H does not define a strategy.**
- **Phase 4bn-H does not generate trade signals.**
- **Phase 4bn-H does not simulate PnL.**
- **Phase 4bn-H does not run backtests.**
- **Phase 4bn-H does not modify dataset layout.**
- **Phase 4bn-H does not call any public, authenticated, or private endpoint.**
- **Phase 4bn-H does not open any WebSocket or user stream.**
- **Phase 4bn-H does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.**
- **Phase 4bn-H does not mutate any manifest.**
- **Phase 4bn-H does not mutate any successor-state artefact.**
- **Phase 4bn-H does not commit `data/microstructure`.**
- **Phase 4bn-H does not commit `data/research`.**
- **Phase 4bn-H does not authorize Phase 4bn-I, Phase 5, paper / shadow,
  live-readiness, deployment, exchange-write, production keys, or any
  successor phase.**
- **The current v002 microstructure ML-baseline window is 90 calendar days.**
- **The split structure is 45 train days, 30 validation days, and 15 sealed
  test days.**
- **The sealed test split remains sealed and is not inspected.**
- **Phase 4bn-B produced descriptive ML-baseline evidence only.**
- **Phase 4bn-C interpreted that evidence as small descriptive lift, not edge.**
- **Phase 4bn-D scoped bounded expansion options but authorized nothing.**
- **Phase 4bn-E partially ruled out gross train-vs-validation
  feature-distribution drift at the measurement-frame level only.**
- **Phase 4bn-F concluded the 90-day window is useful but not enough to
  prove broad sufficiency, insufficiency, representativeness, or outlier
  status.**
- **Phase 4bn-G defined a concrete data-expansion requirements framework
  and storage-scaling comparison, then recommended this acquisition-readiness
  memo.**
- **None of the Phase 4bn-A through Phase 4bn-H evidence establishes edge,
  profitability, tradability, strategy-readiness, signal-readiness, paper /
  shadow readiness, or live-readiness.**
- **Recommended state remains paused.**

---

## 1. Purpose

Phase 4bn-H answers a single governance / scoping question:

> Given that Phase 4bn-G recorded a combined data-expansion requirements +
> storage-scaling architecture scoping decision and recommended a future
> docs-only acquisition-readiness memo focused on a specific expansion shape
> (most plausibly Option B — longer single continuous BTCUSDT aggTrades
> history, keeping Parquet canonical and DuckDB querying Parquet in place
> as the preferred non-invasive query layer) as the cleanest non-paused
> option, is the project ready to consider a future separately authorized
> acquisition phase, and if so, what exact future acquisition envelope,
> what exact calendar coverage, what exact storage posture, what exact
> pre-acquisition gates, and what exact stop conditions would be admissible
> at design level only?

Phase 4bn-H is **docs-only / design-only / scoping-only**. It reads only
committed repository Markdown reports and committed architecture documents
as its evidence base. It opens no local gitignored `data/research/` outputs.
It opens no local gitignored `data/microstructure/` datasets. It reads no
local parquet, CSV, or JSON output. It calls no endpoint. It uses no
credentials. It mutates no manifest, sidecar, gate report, or successor-state
artefact. It trains nothing, scores nothing, predicts nothing, evaluates
nothing on test data, selects nothing, ranks nothing, tunes nothing, runs
nothing, materialises no artefact, acquires no data, migrates no storage,
creates no database, compacts no Parquet, modifies no dataset layout,
creates no v003 dataset, and authorizes no successor implementation.
**Phase 4bn-H is the governance-level acquisition-readiness memo, not data
acquisition, not storage migration, and not v003 creation.**

This memo:

- carries the Phase 4bn-G recommendation forward verbatim as the
  immediate-predecessor authorising boundary;
- carries the Phase 4bn-F data-sufficiency / representativeness scoping
  decision forward verbatim as the most recent representativeness-frame
  evidence;
- carries the Phase 4bn-E descriptive train-vs-validation feature drift
  result forward verbatim as the most recent ML-arc measurement-frame
  evidence;
- carries the Phase 4bn-D bounded ML-baseline expansion scoping decision
  forward verbatim as the design boundary for the C-A / C-B / C-C / C-D /
  C-E / C-F candidate menu;
- carries the Phase 4bn-C corrected interpretation of Phase 4bn-B
  ML-baseline evidence forward verbatim as the binding factual frame;
- carries the Phase 4bn-B `RECORD_EVIDENCE_ONLY` decision forward verbatim;
- defines a single acquisition-readiness framework for a longer
  continuous BTCUSDT aggTrades expansion (Option B from Phase 4bn-G §9)
  at design level only;
- defines a proposed future acquisition envelope at design level only
  (no execution; no execution authorization);
- compares calendar-coverage options A / B / C / D / E at design level
  only;
- defines required future data families at design level only;
- defines a storage posture for any future acquisition at design level
  only, preserving the Phase 4bn-G `A + F + C` baseline recommendation
  (Parquet canonical; defer migration; DuckDB querying Parquet in place
  as the preferred non-invasive query layer);
- defines required pre-acquisition gates and stop conditions at design
  level only;
- records a single scoping decision under the operator-supplied decision
  taxonomy and frames any recommended successor as a recommendation only
  requiring separate operator authorization.

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
  - `docs/00-meta/process/operator-report-standard.md` (Claude Code
    compact report + ChatGPT operator-facing response standard).
  - `docs/00-meta/process/merge-closeout-standard.md` (merge-closeout
    16-section structure).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_merge-closeout.md`
    (Phase 4bn-G merge-closeout;
    `MEMO RECORDED — RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_combined-data-expansion-storage-scaling-scoping.md`
    (Phase 4bn-G scoping memo; 19 sections + 3 appendices).
  - `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-g_closeout.md`
    (Phase 4bn-G closeout).
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
  - `docs/04-data/data-requirements.md` (high-level data requirements
    index; historical-vs-runtime storage separation; Parquet + DuckDB +
    explicit dataset versioning research stack).
  - `docs/04-data/historical-data-spec.md` (canonical historical-data
    contract; Binance USDⓈ-M futures source policy; raw / normalized /
    derived three-layer model).
  - `docs/04-data/timestamp-policy.md` (UTC Unix milliseconds canonical
    timestamp standard; completed-bar policy; point-in-time and
    higher-timeframe alignment rules; read for context only, no rule
    restated).
  - `docs/04-data/dataset-versioning.md` (dataset-versioning policy;
    `__vNNN` naming pattern; mandatory bump conditions; immutability;
    manifest requirements; experiment linkage).
  - `docs/08-architecture/database-design.md` (runtime database design
    document; SQLite with WAL recommended for v1 runtime; the runtime
    database is a safety component, not an analytical store; historical
    research storage is a separate domain).
- **Inputs explicitly NOT used:** local gitignored
  `data/research/microstructure/ml-baselines/phase-4bn-b/` outputs (Phase
  4bn-B local artefacts); local gitignored
  `data/research/microstructure/ml-baselines/phase-4bn-e/` outputs (Phase
  4bn-E local artefacts); local gitignored Phase 4bm-W / Phase 4bm-Q /
  Phase 4bm-S / Phase 4bm-U / Phase 4bm-X artefacts; local
  `data/microstructure/` raw / normalized / feature / label parquets;
  local descriptive CSV / JSON outputs from prior phases. Phase 4bn-H
  treats every prior phase's committed Markdown record (implementation
  report, closeout, merge-closeout) as the authoritative summary of those
  phases' evidence; no re-hashing or re-reading of any local data file is
  performed in this docs-only / design-only / scoping-only phase.
- **README:** README may be stale and is **not** used as current-state
  authority. The authority is `docs/00-meta/current-project-state.md`
  plus the most recent merge-closeout, plus the most recent implementation
  reports (per `docs/00-meta/process/phase-workflow-standard.md`
  "Repo-query requirement for new chats").
- **Pre-branch verification:**
  `git rev-parse main == git rev-parse origin/main == 1ab9ebea5b959764c9cfc6821245103ceb301ffa`.
  Phase 4bn-G SHA-finalization commit
  `1ab9ebea5b959764c9cfc6821245103ceb301ffa` is the tip; Phase 4bn-G
  merge-closeout commit `6073a7e70e19756b6d968ac482c20236d3be256e`, Phase
  4bn-G merge commit `f46c70545825817c528a3c2d61bdbdbb2622e5ca`, and
  Phase 4bn-G branch commit `90c8dba527a11c24f6c15d3368ae1c3d8b85f87c`
  are present on `main` immediately below the SHA-finalization commit.
  Phase 4bn-F SHA-finalization commit
  `c9a2df0eb3e76a91b72c3687f3767b931b458fe2` is present below that.
  Predecessor chain (Phase 4bn-A → 4bn-B → 4bn-C → 4bn-D → 4bn-E → 4bn-F
  → 4bn-G) is fully merge-complete on `main`.

## 3. Phase type and strict scope

Phase 4bn-H is **docs-only / design-only / scoping-only**.

**Allowed surface (tracked files added or modified):**

- `docs/00-meta/implementation-reports/2026-05-30_phase-4bn-h_docs-only-acquisition-readiness.md`
  (this memo; new).
- `docs/00-meta/implementation-reports/2026-05-30_phase-4bn-h_closeout.md`
  (closeout; new).
- `docs/00-meta/current-project-state.md` (narrow current-phase paragraph
  + Current-phase block addition; prior Phase 4bn-A / 4bn-B / 4bn-C /
  4bn-D / 4bn-E / 4bn-F / 4bn-G history preserved as labelled historical
  context).

**Forbidden surface (verbatim):**

- No source code modification.
- No test modification.
- No committed-script modification.
- No `pyproject.toml`, `README.md`, `.gitignore`, or MCP file
  modification.
- No `data/microstructure/` artefact created, modified, or committed.
- No `data/research/` artefact created, modified, or committed.
- No manifest, sidecar, gate-report, or successor-state artefact
  created, modified, or accessed for mutation.
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
  `chronological_split_policy`, `diagnostics_authorized`, or
  `ml_authorized` transition on any actual manifest.
- No successor authorized.

The non-authorization wording above subsumes the reusable Phase 4bl-F §7
blocks **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**,
**N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**,
**N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, and **N-VERDICT-LOCK**;
each block applies in full to Phase 4bn-H.

## 4. Evidence base and input boundary

Phase 4bn-H reads, read-only, the committed repository Markdown documents
enumerated in §2. It reads no local gitignored artefact. It re-hashes no
local file. It does not invoke any normalizer, gate runner, label kernel,
feature kernel, ML runner, diagnostic runner, backtest runner, simulator,
or acquisition runner. It does not call any acquisition script, does not
load any parquet or CSV from `data/microstructure/` or `data/research/`,
does not call `ml_baseline_runner.run(...)`, does not call
`run_feature_drift_v002(...)`, and does not call any helper that touches
the local data surface. The Phase 4bn-A through Phase 4bn-G
merge-closeouts, implementation reports, and closeouts are treated as the
canonical, sufficient evidence record for the ML-baseline arc and the
data-expansion + storage-scaling scoping arc; this is the explicit
guarantee that Phase 4bn-H does not, and cannot, reach for the actual
local artefacts. The data architecture documents
(`docs/04-data/*.md`, `docs/08-architecture/database-design.md`) are read
for design context only; no rule, schema, or policy from those documents
is rewritten by this memo.

This boundary is deliberate. It (a) protects the local artefacts from
accidental mutation, (b) keeps Phase 4bn-H fully reviewable from `main`
without any local state assumption, and (c) honours the
`phase-workflow-standard.md` rule that branch-complete reports must
record what was actually read so that audit is anchored to repository
state rather than to working-directory state.

## 5. Phase 4bn-G decision carried forward

The Phase 4bn-G merge-closeout, implementation report, and closeout are
the immediate predecessor and the explicit authorising boundary for
Phase 4bn-H. Their key conclusions are carried forward verbatim:

- **Phase 4bn-G decision (verbatim):**
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-G type (verbatim):** docs-only / design-only / scoping-only
  governance memo (Tier 1 — Full Phase).
- **Phase 4bn-G is project-complete on `main`** (merge commit
  `f46c70545825817c528a3c2d61bdbdbb2622e5ca`; merge-closeout commit
  `6073a7e70e19756b6d968ac482c20236d3be256e`; final-`main` SHA
  `1ab9ebea5b959764c9cfc6821245103ceb301ffa`).
- **Phase 4bn-G is recommendation-only.** It authorizes nothing
  executable; it explicitly does not authorize Phase 4bn-H, any
  successor, any acquisition, any storage migration, any database
  creation, any Parquet compaction, any v003 dataset, any ML, any
  strategy, any signal, any PnL, any backtest, any paper / shadow /
  live-readiness / deployment / exchange-write / production-key work.
  The operator's separate authorization of Phase 4bn-H is recorded in
  the authorization prompt that produced this memo. Phase 4bn-G's
  recommendation does not retrospectively authorize Phase 4bn-H to
  authorize a downstream successor; Phase 4bn-H is itself docs-only /
  design-only / scoping-only and authorizes nothing.
- **Phase 4bn-G data-expansion requirements framework (verbatim from
  Phase 4bn-G §8, 24 requirements):** target calendar coverage; single
  continuous window vs multiple separated windows; volatility regimes;
  trend / range regimes; volume / activity regimes; funding /
  derivatives-flow regimes; intraday / weekday effects; market-event
  concentration; BTCUSDT-only limitation; ETHUSDT comparison option;
  symbol scope; horizon scope; split allocation; test-holdout
  preservation; explicit confirmation that the existing v002 sealed test
  set remains untouched; label / feature family preservation vs v003 /
  successor family; cost-commensurability under §11.6; high-confidence
  calibration failure from Phase 4bn-C; reproducibility from public
  Binance sources; sidecar / manifest implications; disk footprint;
  expected derivation time; expected query load; exact stop conditions.
- **Phase 4bn-G seven candidate expansion shapes (verbatim from Phase
  4bn-G §9):** Option A (remain with current 90-day v002 envelope; no
  acquisition) — available; Option B (longer single continuous BTCUSDT
  aggTrades history) — deferred; Option C (multiple separated BTCUSDT
  regime windows) — deferred; Option D (BTCUSDT longer continuous
  history plus later ETHUSDT comparison) — deferred; Option E (multiple
  BTCUSDT regime windows plus later ETHUSDT comparison) — deferred,
  structurally rejected as a first shape; Option F (define a new v003
  or successor dataset family later) — not recommended at governance
  level; Option G (close the ML-baseline arc) — available.
- **Phase 4bn-G six candidate storage architectures (verbatim from Phase
  4bn-G §10):** Storage A (current partitioned Parquet remains canonical)
  — recommended as baseline; Storage B (compacted Parquet with explicit
  compression / row-group / partition policy) — deferred; Storage C
  (DuckDB querying Parquet in place) — recommended as preferred
  non-invasive query layer; Storage D (DuckDB database file as a derived
  local research cache) — deferred (may duplicate storage rather than
  reduce it); Storage E (SQLite only for runtime / control metadata) —
  preserved verbatim for runtime; structurally rejected for research;
  Storage F (defer storage migration; keep current layout until a
  concrete acquisition plan exists) — recommended as default.
- **Phase 4bn-G recommended path (verbatim from Phase 4bn-G §12):**
  recommend a future docs-only acquisition-readiness memo that keeps
  Parquet as canonical (Storage A) and evaluates DuckDB querying Parquet
  in place (Storage C) as the preferred non-invasive query layer, while
  deferring any DuckDB database-cache (Storage D) or Parquet-compaction
  (Storage B) decision until there is a concrete acquisition envelope.
- **Phase 4bn-G pre-acquisition gates (verbatim from Phase 4bn-G §13, 14
  gates):** acquisition-readiness memo present in main;
  storage-architecture decision present in main; source-policy
  preservation; `__vNNN` naming policy; Phase 4bb-F canonical sidecar /
  path policy; Phase 4aw `flip_research_eligible(...)` always-raises
  invariant; eligibility-gate envelope; manifest invariants (start at
  `research_eligible: false`, `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"`); successor-state
  recording; test-holdout preservation; reproducibility check;
  disk-footprint cap; cost cap; fail-closed default.
- **Phase 4bn-G non-authorization envelope (verbatim from Phase 4bn-G
  §15, 13 constraints):** docs-only / design-only / scoping-only; no
  source / test / script / config / manifest / sidecar / gate-report /
  successor-state mutation; no local data artefact creation or mutation;
  no test-holdout access; no endpoint calls; no WebSocket / user stream;
  no credentials / `.env` / `.mcp.json` / MCP / Graphify; no manifest
  transitions; no retained verdict revision; no project lock loosening;
  no M0 amendment; no authorization of any further successor; no commit
  under `data/microstructure/` or `data/research/`.
- **Phase 4bn-G equivalent operator alternatives (verbatim):** remain
  paused; request a merge prompt for Phase 4bn-G (already chosen and
  executed); reject further ML-baseline successors and close the ML
  arc; separately authorize only a future docs-only
  storage-architecture decision memo; separately authorize a future
  docs-only combined acquisition-readiness + storage-decision memo;
  separately authorize the recommended docs-only acquisition-readiness
  memo (the option the operator chose, producing this Phase 4bn-H memo).

This memo defers to Phase 4bn-G on every factual scoping interpretation
of the combined data-expansion + storage-scaling questions; Phase 4bn-H
does not re-derive the 24-requirement framework, the 7-shape expansion
menu, the 6-architecture storage menu, the 7 × 6 decision matrix, the
14 pre-acquisition gates, the 10 pre-storage-migration gates, or the 13
non-authorization constraints. Phase 4bn-H applies that framework to
one chosen expansion shape (Option B) at design level only.

## 6. Phase 4bn-F / 4bn-E / 4bn-D / 4bn-C / 4bn-B interpretation carried forward

The Phase 4bn-F data-sufficiency / representativeness scoping decision,
the Phase 4bn-E descriptive feature drift result, the Phase 4bn-D
bounded ML-baseline expansion scoping decision, the Phase 4bn-C
corrected interpretation of Phase 4bn-B ML-baseline evidence, and the
Phase 4bn-B descriptive-only result are the binding factual frame for
any data-sufficiency or storage-scaling claim discussed below. They are
carried forward verbatim:

- **Phase 4bn-F decision (verbatim):**
  `RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
  Phase 4bn-F concluded the 90-day window is useful but not enough to
  prove broad sufficiency, insufficiency, representativeness, or outlier
  status; it treated "outlier" as an unresolved risk, not a conclusion.
- **Phase 4bn-E decision (verbatim):**
  `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`. Phase 4bn-E
  executed the bounded descriptive C-D candidate (train-vs-validation
  feature drift diagnostics) and produced descriptive feature-drift
  evidence (45 v002 computed features analysed; 31 `low_descriptive_drift`,
  13 `moderate_descriptive_drift`, 0 `high_descriptive_drift`, 1
  `undefined_due_to_zero_or_missing_train_std`; highest absolute
  standardized mean delta 0.330; highest absolute missing-rate delta
  ≈ 6e-06; the 13 moderate-drift features cluster on count and
  mean-quantity dimensions, signed consistently count-up /
  mean-quantity-down between train and validation). Phase 4bn-E
  partially ruled out gross feature-distribution drift at the
  measurement-frame level only; it did not address regime / volatility /
  cost-commensurability / calendar-coverage / outlier questions.
- **Phase 4bn-D scoping decision (verbatim):**
  `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Phase 4bn-C interpretation decision (verbatim):**
  `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`.
- **Phase 4bn-B decision (verbatim):** `RECORD_EVIDENCE_ONLY`.
- **Phase 4bn-B descriptive evidence (verbatim summary):** the flat
  class is underrepresented at 0.15 – 1.09 % across both included
  horizons and both supervised splits; directional classes near-balanced
  (down ≈ up ≈ 0.495 ± 0.005); majority accuracy floor ~50 % (0.4938
  at 15s; 0.4950 at 60s); majority macro-F1 floor ~0.22; L2 / L1 linear
  lift ~+5 pp accuracy at 15s, ~+1.5 pp at 60s, ~+14 pp macro-F1 at 15s,
  ~+11 pp macro-F1 at 60s; the flat class is never predicted by L2 / L1
  (per-class P / R / F1 = 0 / 0 / 0 on flat in every cell); persistence
  beats majority on hard accuracy (+2.3 pp at 15s, +0.2 pp at 60s) but
  is catastrophically worse on log-loss (~18× majority) and Brier (~2×
  majority) because it emits hard one-hot probabilities; L2 15s is
  well-calibrated in the dominant 0.5 – 0.6 confidence bin (~86 % of
  validation rows; reliability gap −0.0047) but severely over-confident
  in the 0.6 – 1.0 tail (reliability gaps −0.061 to −0.392; in the 0.8
  – 0.9 bin the empirical accuracy is 0.4881, *below* the majority
  floor); §11.6 cost-commensurability fractions on validation: 15s
  6.2 % > 1× / 1.6 % > 2× / 0.16 % > 5×; 60s 18.3 % > 1× / 5.8 % > 2× /
  0.93 % > 5×; train-validation deltas small (~0.5 pp on hard metrics)
  — no overfitting at this measurement level; test holdout sealed
  (`test_rows_loaded: 0`).
- **A naive "trade when confidence is high" idea would fail under
  current evidence.**
- **15s has stronger model signal but worse cost / tradability
  context; 60s has better cost context but weaker model signal.**
- **None of this is edge, profitability, tradability,
  strategy-readiness, or a signal.** **Phase 4bn-H inherits this
  boundary without softening it.**

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
  4bn-H does not read it, evaluate against it, design with it, peek at
  it, hash it, or unseal it under any pretext. `iter_partitions(split="test",
  ...)` raises by construction in the Phase 4bn-B implementation and that
  invariant is unchanged.
- **Horizons used in baseline ML:** 15s and 60s. 1s and 5s deferred at
  Phase 4bn-A §10 for latency / tradability sensitivity and
  cost-commensurability risk.
- **Feature surface:** the 45 v002 `computed_feature_column_names` (40
  rolling features × 4 windows; 5 non-windowed columns); frozen from
  the v002 feature manifest; no new feature engineering since Phase
  4bn-A; no feature selection / ranking / pruning since.
- **Label surface:** strict-sign direction classification (3-class
  `{-1, 0, +1}` per horizon) from the v002 label family; flat class
  preserved explicitly.
- **Split policy:** the Phase 4bm-U-recorded
  `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. Strictly
  chronological; train precedes validation precedes test; 60s-boundary
  embargo enforced; never relaxed.

**The current v002 microstructure ML-baseline window is 90 calendar
days. The split structure is 45 train days, 30 validation days, and 15
sealed test days. The sealed test split remains sealed and is not
inspected.**

The 90-day v002 envelope is the project's first microstructure
ML-baseline envelope and remains the only one. It provides **one
well-controlled descriptive picture**, not a generalisation-ready basis.
Phase 4bn-F / 4bn-G concluded the window is useful but not enough to
prove broad sufficiency, insufficiency, representativeness, or outlier
status. Phase 4bn-H preserves that conclusion verbatim and does not
soften it.

## 8. Candidate acquisition question

Phase 4bn-H defines the exact future acquisition question that any
future separately authorized acquisition phase would have to answer
before any operator commitment. Phase 4bn-G recommended that this memo
focus on a specific expansion shape (most plausibly Option B — longer
single continuous BTCUSDT aggTrades history). Phase 4bn-H adopts Option
B as the candidate shape and frames the candidate acquisition question
as follows.

**The exact future acquisition question (verbatim):**

> Would a longer single continuous BTCUSDT aggTrades history, preserving
> the v002 feature/label family and keeping the existing v002 sealed
> test split untouched, provide a materially better basis for
> interpreting the Phase 4bn-B / 4bn-C descriptive ML-baseline evidence
> across calendar, volatility, activity, funding, and cost-commensurability
> regimes?

**What the question is not (verbatim, to prevent rephrasing drift):**

- It is **not** "Will more data make ML work?"
- It is **not** "Can we find edge with more data?"
- It is **not** "Can we rescue the model?"
- It is **not** "Can we tune until performance improves?"
- It is **not** "Can we get a tradable signal?"
- It is **not** "Will additional data prove the v002 family is correct?"
- It is **not** "Will additional data refute the v002 family?"

**Why this question is the right one to ask, given current evidence:**

1. Phase 4bn-B / 4bn-C / 4bn-E showed that the v002 family produces a
   small but reproducible descriptive lift over the majority floor at
   15s and a weaker lift at 60s, with a severe high-confidence
   calibration tail and §11.6 cost-commensurability fractions consistent
   with 80 – 95 % of validation rows being below the round-trip cost.
2. Phase 4bn-F concluded the 90-day window is useful but not enough to
   prove broad sufficiency, insufficiency, representativeness, or
   outlier status; whether 90 days is enough remains unresolved.
3. Phase 4bn-E partially ruled out gross feature-distribution drift at
   the measurement-frame level only; subtler regime / volatility /
   cost-commensurability / calendar-coverage / outlier questions remain
   open.
4. Phase 4bn-G recommended the project consider a future docs-only
   acquisition-readiness memo focused on Option B; that recommendation
   is bounded by the 24-requirement framework in Phase 4bn-G §8.
5. The candidate question above is therefore a *descriptive*
   interpretability question, not a *predictive performance* question;
   it asks whether the existing descriptive picture is robust to
   longer-history sampling across regimes, not whether longer history
   would *change* the model's predictive quality.

**Phase 4bn-H does not pre-decide the answer to the question.** Phase
4bn-H records only that the question is a legitimate, bounded, and
specific scoping target, and that any future separately authorized
acquisition execution plan would have to answer it under the
24-requirement framework in Phase 4bn-G §8 before any acquisition is
authorized.

## 9. Proposed future acquisition envelope, design-level only

Phase 4bn-H proposes a future acquisition envelope at design level only,
without executing it. **The envelope is not authorized.** The envelope
exists so the operator can see, at one level lower of abstraction than
Phase 4bn-G's seven-option menu, what a future separately authorized
acquisition execution plan for Option B would have to look like at
design level.

**Default preferred envelope (Phase 4bn-G Option B, design-level only):**

- **Symbol:** BTCUSDT only.
- **Data family:** Binance USDⓈ-M futures aggTrades only.
- **Shape:** longer single continuous history (one contiguous calendar
  window; no multiple separated windows in this first expansion).
- **Preserve v002 feature and label family semantics initially.** The
  acquisition execution plan would reuse the v002 feature kernel, the
  v002 label kernel, the v002 manifest semantics, and the v002 split
  policy without modification.
- **Preserve horizons 15s and 60s initially.** No new horizons. The
  Phase 4bn-A §10 1s / 5s deferral remains in force. Any horizon
  extension would trigger a separate phase that must satisfy the Phase
  4bn-A horizon deferral rationale.
- **Keep existing v002 sealed test set untouched.** Per Phase 4bn-G §8.14
  / §8.15 (preserved verbatim). The existing 15-day sealed test split
  (2025-02-14 .. 2025-02-28; 23,797,822 rows; `test_rows_loaded: 0`)
  remains sealed and is never inspected.
- **Keep Parquet canonical** (Storage A from Phase 4bn-G §10).
- **Permit DuckDB querying Parquet in place** as a non-invasive query
  layer (Storage C from Phase 4bn-G §10) if any future descriptive
  workload requires SQL-shaped joins. The existing Parquet remains the
  source of truth.
- **Do not create DuckDB database cache** (Storage D deferred).
- **Do not compact Parquet** (Storage B deferred).
- **Do not add ETHUSDT yet** (Option D / Option E deferred).
- **Do not create v003 yet** (Option F not recommended at governance
  level until v002 inadequacy is shown).
- **Do not change the manifest invariants** (`research_eligible: false`,
  `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"` start state preserved
  on the new manifests; any transition requires a separately authorized
  successor-state recording phase).
- **Do not authorize ML, models, tuning, strategy, signals, PnL, or
  backtests** on the expanded envelope. Any future ML execution on the
  expanded envelope would require its own separately authorized Tier 1
  ML-baseline implementation phase that satisfies the Phase 4bn-A §9 –
  §20 design boundary (or a separately authorized successor design
  memo).

**Envelope cost framing (design-level only; no acquisition):**

The acquisition execution plan would have to record, at design level,
the realistic raw + normalized + feature + label disk footprint implied
by the proposed expansion size at the proposed symbol scope (per Phase
4bn-G §8.21), the realistic normalisation / feature / label derivation
time (per Phase 4bn-G §8.22), and the expected query load (per Phase
4bn-G §8.23). Phase 4bn-H does **not** compute these numbers; the
acquisition execution plan would. Phase 4bn-H only enforces that the
plan must declare them with explicit caps before any acquisition is
authorized.

**Envelope structurally rejected combinations (cross-link to Phase
4bn-G §11):**

- Any combination that places research matrices in SQLite (Storage E
  research role) — structurally rejected.
- Any retroactive rewrite of the existing v002 envelope — structurally
  rejected.
- Any combination that breaks re-derivability from Binance public
  sources — structurally rejected.
- Any combination that requires `data/microstructure/` or `data/research/`
  artefacts to be committed — structurally rejected.

## 10. Calendar coverage options and selected readiness recommendation

Phase 4bn-H enumerates candidate calendar coverage options at design
level only. Each option records (a) what it answers, (b) expected
governance cost, (c) expected storage impact, (d) expected
derivation/query burden, (e) representativeness benefit, (f) risk, and
(g) whether it is recommended, deferred, not recommended, or available.
**No option is selected for execution by Phase 4bn-H. No option is
authorized by Phase 4bn-H.**

The options compared below are deliberately narrower than Phase 4bn-G
§9's seven-shape menu: Phase 4bn-G enumerated structurally distinct
expansion *shapes* (single contiguous BTCUSDT vs multi-regime BTCUSDT vs
add ETHUSDT vs new family vs close arc); Phase 4bn-H narrows to the
recommended shape (Option B — single contiguous BTCUSDT) and varies
*calendar length* within it, while preserving Phase 4bn-G Option A (no
acquisition) and Phase 4bn-G Option G (close the arc) as the two
non-acquisition alternatives at the endpoints.

### Option A — No acquisition; remain with 90-day v002

- **What it answers.** Whether the project should treat the existing
  Phase 4bn-A through Phase 4bn-G descriptive evidence as the terminal
  evidence boundary for the v002 ML-baseline family.
- **Expected governance cost.** None beyond the existing reports.
- **Expected storage impact.** None. The v002 envelope's footprint is
  already material; no marginal increase.
- **Expected derivation / query burden.** None.
- **Representativeness benefit.** None. The 90-day window remains the
  only descriptive picture and remains of unresolved representativeness
  per Phase 4bn-F.
- **Risk.** Permanently leaving open the question of whether 90 days
  is sufficient or representative. Foreclosing future expansion options
  by inertia rather than by decision. Accepting the current
  high-confidence calibration failure as the standing baseline with no
  further measurement.
- **Recommended / deferred / not recommended / available.** **Available**
  as a valid operator choice. Phase 4bn-H does not foreclose Option A.

### Option B — Extend to 6 months continuous BTCUSDT

- **What it answers.** Whether doubling the calendar window of the
  existing v002 envelope (approximately) materially changes the
  descriptive picture across volatility, activity, funding, and event
  regimes.
- **Expected governance cost.** Moderate. A separately authorized
  docs-only acquisition execution plan (Tier 1), then a separately
  authorized acquisition phase (Tier 1, code + docs + local gitignored
  output) under the existing Phase 4bb-* / Phase 4bj-* / Phase 4bm-Q
  governance, then a separately authorized raw eligibility-gate
  execution (Tier 3 batch if the Phase 4bb-C gate protocol covers it;
  Tier 1 if any new semantics), then a separately authorized derived
  eligibility-gate execution, then feature/label kernel reruns under
  the v002 kernels, then a separately authorized feature-family gate
  execution and label-family gate execution, then per-family
  successor-state recording.
- **Expected storage impact.** Roughly twice the current v002 per-day
  raw + normalized + feature + label footprint. Per Phase 4bn-G §10
  Storage A (Parquet canonical), the per-day Parquet footprint is the
  same as v002; the absolute increase depends on the chosen window cap.
- **Expected derivation / query burden.** Roughly twice the Phase 4bn-E
  diagnostic scaling unit (Phase 4bn-E ran 75 partitions × 2 passes in
  553.6 s on the 90-day envelope; 6 months at roughly the same per-day
  unit cost implies ~1.8× that runtime as a first-order estimate; the
  actual cost depends on the per-day partition size at the chosen
  window dates).
- **Representativeness benefit.** Modest. Doubles the calendar window
  but is still inside one realized macro regime. May not change the
  §11.6 cost-commensurability picture qualitatively if the chosen
  window is monotonically similar to the existing 90 days. May
  surface modest changes in count / mean-quantity drift dimensions
  observed in Phase 4bn-E.
- **Risk.** 6 months may still be too narrow for broad regime
  representativeness (the central concern Phase 4bn-F surfaced).
  Commits acquisition governance cost without necessarily resolving
  the unresolved sufficiency question. May force a second acquisition
  later if 6 months proves insufficient.
- **Recommended / deferred / not recommended / available.** **Available
  but not preferred.** Phase 4bn-H does not foreclose Option B as a
  bounded first expansion, but the marginal sufficiency gain may not
  justify the governance cost given that 6 months remains inside one
  macro regime.

### Option C — Extend to 12 months continuous BTCUSDT

- **What it answers.** Whether a calendar window of approximately one
  year materially changes the descriptive picture across multiple
  volatility, activity, funding, intraday, weekday, and event regimes;
  whether the existing 90-day descriptive picture survives across a
  meaningfully wider macro envelope; and whether the Phase 4bn-E
  count-up / mean-quantity-down drift direction generalises across a
  year.
- **Expected governance cost.** Higher than Option B by the factor
  needed to acquire, normalize, feature-derive, label-derive, and
  gate-evidence the additional months; same governance phase chain as
  Option B (acquisition execution plan, acquisition, raw gate, derived
  gate, feature kernel rerun, label kernel rerun, feature-family gate,
  label-family gate, per-family successor-state).
- **Expected storage impact.** Roughly four times the current v002
  per-day raw + normalized + feature + label footprint (12 months ≈
  365 days vs 90 days). Per Phase 4bn-G §10 Storage A (Parquet
  canonical), the per-day Parquet footprint is the same; the absolute
  increase scales linearly. The disk-footprint cap declared in the
  future acquisition execution plan would govern the absolute ceiling.
- **Expected derivation / query burden.** Roughly four times the Phase
  4bn-E baseline diagnostic scaling unit (~2 200 s = ~37 minutes for an
  equivalent two-pass diagnostic over 12 months at the same per-day
  unit cost). The actual cost depends on the per-day partition size at
  the chosen window. The Phase 4bn-G §10 Storage C (DuckDB querying
  Parquet in place) becomes more attractive at this scale for SQL-shaped
  ad-hoc exploration but does not change the per-pass scan cost
  materially.
- **Representativeness benefit.** Material. A 12-month window samples
  multiple volatility regimes, multiple trend / range regimes, multiple
  funding regimes, intraday and weekday cycles at scale, and at least
  one or two macro / venue / on-chain / regulatory events. Whether the
  90-day descriptive picture survives across a 12-month envelope is
  itself a meaningful answer regardless of direction (consistent picture
  → 90 days is more representative than expected; divergent picture →
  the 90-day window's representativeness was overestimated).
- **Risk.** Acquisition cost is non-trivial; if the resulting
  descriptive picture is largely consistent with the v002 picture, the
  marginal-evidence return rate per acquisition cost may not feel
  worthwhile in hindsight (although a consistent picture is itself
  informative). Disk-footprint and runtime caps must be declared
  conservatively to avoid governance-cost overruns.
- **Recommended / deferred / not recommended / available.**
  **Recommended at design level only** as the cleanest first-expansion
  calendar coverage subject to separate operator authorization of a
  docs-only acquisition execution plan that satisfies the Phase 4bn-G
  §8 24-requirement framework, declares an explicit disk-footprint cap
  and cost cap, and preserves the existing v002 sealed test holdout
  untouched. **Phase 4bn-H does not authorize execution.**

### Option D — Extend to 24 months continuous BTCUSDT

- **What it answers.** Whether a calendar window of approximately two
  years materially changes the descriptive picture across an even
  broader regime envelope, including multiple bull / bear / range
  macro cycles, multiple funding-regime shifts, and a higher likelihood
  of capturing high-impact venue / regulatory / on-chain events.
- **Expected governance cost.** Higher than Option C by the factor
  needed to acquire, normalize, feature-derive, label-derive, and
  gate-evidence the additional twelve months.
- **Expected storage impact.** Roughly eight times the current v002
  per-day raw + normalized + feature + label footprint (24 months ≈
  730 days vs 90 days). The disk-footprint cap declared in the future
  acquisition execution plan would govern the absolute ceiling; this is
  the option at which the Phase 4bn-G §10 Storage B (compacted Parquet)
  and Storage D (DuckDB cache) deferred decisions become more pressing
  as second-order optimisations, but compaction and cache remain
  deferred under Phase 4bn-H's storage posture (§12).
- **Expected derivation / query burden.** Roughly eight times the Phase
  4bn-E baseline diagnostic scaling unit (~4 400 s = ~73 minutes for an
  equivalent two-pass diagnostic over 24 months at the same per-day
  unit cost). At this scale, file-count overhead per Phase 4bn-G §10
  Storage A becomes a more significant factor; the per-day partitioning
  preserved by Storage A continues to work but bumps into the deferred
  compaction question.
- **Representativeness benefit.** Higher than Option C. A 24-month
  window samples nearly all common volatility / trend / activity /
  funding regimes at meaningful scale.
- **Risk.** Largest acquisition cost of the contiguous-window family.
  Highest disk-footprint and runtime burden. May be too large for the
  *first* expansion before the disk-footprint and derivation-time cap
  estimates are precisely measured against real Option C numbers.
  Commits more governance cost than Option C without proportional
  marginal-evidence return rate guaranteed.
- **Recommended / deferred / not recommended / available.** **Deferred.**
  Phase 4bn-H does not recommend Option D as the first expansion shape;
  the Option C recommendation above is bounded specifically so that the
  first expansion measures the actual per-day cost in practice before
  committing to a larger envelope. Option D remains available as a
  follow-up expansion shape if Option C's actual cost evidence supports
  it.

### Option E — Close the ML-baseline arc

- **What it answers.** Whether the project should record a verdict that
  the v002 ML-baseline family is operationally closed for further
  bounded expansion under current evidence and that the descriptive
  results recorded by Phase 4bn-A through Phase 4bn-G stand as the
  project's ML-baseline evidence record. Closing the arc means **no
  further v002 ML-baseline follow-up under this arc unless reopened by
  a separately authorized future phase**; it **does not delete
  evidence** and **does not close Prometheus**.
- **Expected governance cost.** Low (one closure memo + closeout +
  narrow current-project-state.md update; separately authorized Tier 1).
- **Expected storage impact.** None.
- **Expected derivation / query burden.** None.
- **Representativeness benefit.** None. Records closure without
  acquiring further representativeness evidence.
- **Risk.** Records a closure on the v002 ML-baseline family before
  the operator has decided whether the calibration failure and the
  cost-commensurability context could ever be changed by more data;
  closing prematurely on a question whose data-sufficiency answer is
  unknown.
- **Recommended / deferred / not recommended / available.** **Available**
  as a valid operator choice; not recommended as the default because
  Phase 4bn-H does not have evidence to close the arc unilaterally
  (consistent with Phase 4bn-G §12.3).

### Summary table — calendar coverage options

| Option | What it answers | Governance cost | Storage impact (vs 90-day) | Derivation / query burden | Representativeness benefit | Risk | Recommended? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A — No acquisition; remain 90-day v002 | Treat current evidence as terminal | None | None | None | None | Forecloses by inertia | Available |
| B — 6 months continuous BTCUSDT | Modest calendar doubling | Moderate | ~2× | ~2× Phase 4bn-E unit | Modest | May still be too narrow | Available but not preferred |
| C — 12 months continuous BTCUSDT | Materially broader regime envelope | Higher | ~4× | ~4× Phase 4bn-E unit | Material | Acquisition cost; representativeness vs cost tradeoff | **Recommended at design level only** |
| D — 24 months continuous BTCUSDT | Even broader regime envelope | Higher than C | ~8× | ~8× Phase 4bn-E unit | Higher | Largest acquisition / disk / runtime burden | Deferred |
| E — Close the ML-baseline arc | Record operational closure verdict | Low | None | None | None | Closes prematurely | Available |

Every entry above is "design level only" for the "Authorizes now?"
column (which is omitted from the table because the column is uniformly
**No**). **Phase 4bn-H authorizes none of the options.**

### Selected readiness recommendation

Phase 4bn-H's design-level reading of the repository evidence supports
the following recommendation:

**Recommend a future separately authorized docs-only acquisition
execution plan for a 12-month continuous BTCUSDT aggTrades expansion,
preserving v002 semantics, Parquet canonical storage, DuckDB-in-place
query posture, and no ETHUSDT / v003 / compaction / cache in the first
expansion. Acquisition itself remains unauthorized.**

Rationale (anchored to §5 – §10):

1. **6 months may still be too narrow for regime representativeness**
   (Option B). The Phase 4bn-F unresolved sufficiency question is more
   likely answerable across a 12-month window than a 6-month window
   because the macro regime is more likely to vary at 12 months.
2. **12 months gives materially better calendar / volatility / funding
   / activity coverage while staying bounded** (Option C). The
   acquisition cost is non-trivial but bounded; the disk-footprint and
   derivation-time caps remain explicit at design level. A 12-month
   window samples multiple regimes without committing to the highest
   total cost.
3. **24 months may be too large for the first expansion before
   disk / runtime burden is precisely measured** (Option D). The Phase
   4bn-G §8.21 / §8.22 / §8.23 dimensions become harder to predict at
   24 months without empirical evidence from a smaller expansion first.
   Doing Option C first lets the project measure the real per-day cost
   before committing to Option D.
4. **BTCUSDT-only keeps the first expansion simpler.** ETHUSDT
   (Option D / Option E in Phase 4bn-G §9) requires per-symbol
   acquisition governance; deferring cross-symbol expansion to a later
   phase preserves the comparability of the first expansion to the
   existing Phase 4bn-B descriptive picture.
5. **Preserving v002 semantics keeps comparability to Phase 4bn-B.**
   The Phase 4bn-G §8.16 label / feature family preservation requirement
   is satisfied. The 45 computed feature columns and the 3-class
   strict-sign label family are unchanged. No v003 family is created in
   this first expansion.
6. **Parquet canonical + DuckDB-in-place avoids premature storage
   migration.** The Phase 4bn-G §10 / §12 recommendation
   `A + F + C` is preserved verbatim. Storage B (compaction) and Storage
   D (DuckDB database cache) remain deferred until the actual workload
   measured against Option C's real expansion shows whether they are
   justified.
7. **Phase 4bn-G's 24-requirement framework remains the binding
   contract.** The future acquisition execution plan would have to
   satisfy Phase 4bn-G §8 in full, declare an explicit disk-footprint
   cap (Phase 4bn-G §8.21), declare an explicit cost cap (Phase 4bn-G
   §8.22 / §8.23), declare exact stop conditions (Phase 4bn-G §8.24),
   preserve the existing v002 sealed test holdout untouched (Phase
   4bn-G §8.14 / §8.15), and preserve every retained verdict and
   project lock.
8. **The recommended docs-only acquisition execution plan is itself
   docs-only / design-only / scoping-only and authorizes nothing
   executable.** The acquisition phase itself would remain a separate,
   separately authorized Tier 1 phase that the execution plan does not
   trigger.

**Phase 4bn-H does not foreclose Option A (remain paused / no
acquisition) or Option E (close the ML-baseline arc).** The operator
may equivalently choose either of these without contradicting Phase
4bn-H's design-level reading; the recommendation above is the cleanest
non-paused, non-arc-closing option, subject to separate operator
authorization. If the operator prefers a narrower variant, Option B
(6 months) remains structurally available; if the operator prefers a
larger first expansion, Option D (24 months) remains structurally
available subject to the disk-footprint / cost-cap concerns raised
above.

## 11. Required future data families, design-level only

Any future acquisition phase, if separately authorized later, would
require the following data artefact families. Phase 4bn-H **defines**
which families would be needed; it **does not create** them.

### 11.1 Raw aggTrades archives

- **What.** Public Binance USDⓈ-M aggTrades archives covering the
  chosen 12-month expansion window (or whatever calendar coverage the
  separately authorized acquisition execution plan ultimately
  declares).
- **Source policy.** `docs/04-data/historical-data-spec.md` canonical
  Binance USDⓈ-M futures endpoints. Any divergence must be governed
  by a separately authorized source-policy memo.
- **Storage.** Under `data/microstructure/raw/` per the Phase 4bb-F
  canonical path policy; gitignored under `.gitignore:85: data/microstructure/`;
  never committed.
- **Sidecar / manifest.** Each archive must carry a canonical Phase
  4bb-F sidecar (`<sha>  <basename>\n` two-space separator; LF only;
  no CRLF; no BOM; no extra fields; refuse-overwrite).
- **Governance.** A separately authorized raw eligibility-gate
  execution under the Phase 4bb-C protocol (Tier 3 batch if the
  protocol covers the new partitions unchanged; Tier 1 if any new
  semantics are introduced).
- **Phase 4bn-H does not acquire raw archives; does not invoke any
  acquisition runner; does not call any endpoint.**

### 11.2 Normalized aggTrades

- **What.** Normalized aggTrade tables under the existing v002
  normalization logic (the Phase 4bd implementation; the Phase 4be
  structural QA result preserved verbatim).
- **Storage.** Under `data/microstructure/normalized/` per the Phase
  4bb-F canonical path policy; gitignored; never committed.
- **Sidecar / manifest.** Canonical Phase 4bb-F sidecars; manifests
  follow the existing `__vNNN` naming pattern with appropriate version
  bump if normalization semantics change (per
  `docs/04-data/dataset-versioning.md`); the v002 normalization logic
  is preserved unchanged in this first expansion.
- **Governance.** A separately authorized derived eligibility-gate
  execution under the Phase 4bf-A / 4bf protocol.
- **Phase 4bn-H does not normalize aggTrades; does not invoke any
  normalization kernel; does not modify any normalized artefact.**

### 11.3 v002-compatible feature outputs

- **What.** Feature parquets derived under the existing v002 feature
  kernel (the Phase 4bk-* implementation; the 45 `computed_feature_column_names`
  preserved); per Phase 4bn-G §8.16 the v002 feature surface is
  preserved as the first expansion's feature surface.
- **Storage.** Under `data/microstructure/features/` per the Phase
  4bb-F canonical path policy; gitignored; never committed.
- **Sidecar / manifest.** Canonical Phase 4bb-F sidecars; the v002
  feature manifest's `research_eligible: false`,
  `eligibility_gate_status: "pending"`, and `stage_4_feature_cleared: false`
  start state preserved on the new manifests; no transition authorized
  by acquisition alone.
- **Governance.** A separately authorized feature-family
  eligibility-gate execution under the Phase 4bi-B / 4bi protocol.
- **Phase 4bn-H does not derive features; does not invoke any feature
  kernel; does not modify any feature artefact.**

### 11.4 v002-compatible label outputs

- **What.** Label parquets derived under the existing v002 label kernel
  (strict-sign direction at 15s and 60s; flat class preserved
  explicitly); per Phase 4bn-G §8.16 the v002 label family is
  preserved as the first expansion's label family.
- **Storage.** Under `data/microstructure/labels/` per the Phase 4bb-F
  canonical path policy; gitignored; never committed.
- **Sidecar / manifest.** Canonical Phase 4bb-F sidecars; the v002
  label manifest's `research_eligible: false`,
  `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"`, and
  `label_family_research_use_authorized: false` start state preserved
  on the new manifests; no transition authorized by acquisition alone.
- **Governance.** A separately authorized label-family
  eligibility-gate execution under the Phase 4bj-E / 4bj-F / 4bj-G
  protocol (each Tier 1 unless the protocol explicitly covers the new
  partitions as a Tier 3 batch).
- **Phase 4bn-H does not derive labels; does not invoke any label
  kernel; does not modify any label artefact.**

### 11.5 Manifests and sidecars

- **What.** Per-family manifests (raw, normalized, feature, label)
  recording phase identity, base SHA, source manifest SHAs, split
  policy snapshot, source endpoint set, fetch timestamps, transform /
  pipeline version, schema version, partitioning rules, primary key
  definition, generation timestamp, quality checks, known issues,
  predecessor versions, and the canonical Phase 4bb-F sidecar policy.
- **Storage.** Under the appropriate `data/microstructure/manifests/`
  / per-family manifest directory per the Phase 4bb-F canonical path
  policy; gitignored; never committed.
- **Sidecar.** Canonical Phase 4bb-F format.
- **Governance.** Manifests follow the existing `dataset-versioning.md`
  policy. The v002 `__vNNN` naming pattern is preserved. Any breaking
  schema change would trigger a new dataset version per
  `dataset-versioning.md`.
- **Phase 4bn-H does not write any manifest; does not mutate any
  manifest; does not invoke any manifest writer.**

### 11.6 Future descriptive ML-baseline outputs (only if separately authorized later)

- **What.** Future descriptive ML-baseline outputs analogous to the
  Phase 4bn-B local artefacts (`ml_baseline_run_manifest.json`,
  `per_horizon_model_summary.json`, `metrics_train_validation.csv`,
  `calibration_summary.csv`, `class_balance_summary.csv`,
  `feature_schema_used.json`, `transform_metadata.json` + canonical
  Phase 4bb-F sidecars) derived over the expanded envelope.
- **Storage.** Local gitignored under
  `data/research/microstructure/ml-baselines/phase-4bn-{X}/` for some
  future phase identifier X; never committed.
- **Governance.** A separately authorized Tier 1 ML-baseline
  implementation phase that satisfies the Phase 4bn-A §9 – §20 design
  boundary (or a separately authorized successor design memo). The
  acquisition phase itself does not authorize any ML execution.
- **Phase 4bn-H does not run ML; does not authorize any future
  ML-baseline implementation; does not pre-decide any ML scope on the
  expanded envelope.**

### 11.7 Future diagnostics outputs (only if separately authorized later)

- **What.** Future descriptive diagnostic outputs analogous to the
  Phase 4bn-E local artefacts (`feature_drift_summary.csv`,
  `feature_drift_overview.json`, `feature_drift_manifest.json` +
  canonical Phase 4bb-F sidecars) derived over the expanded envelope.
- **Storage.** Local gitignored under
  `data/research/microstructure/ml-baselines/phase-4bn-{X}/` for some
  future phase identifier X; never committed.
- **Governance.** A separately authorized Tier 1 diagnostic
  implementation phase that satisfies the Phase 4bn-E measurement-frame
  boundary (or a separately authorized successor design memo). The
  acquisition phase itself does not authorize any diagnostic execution.
- **Phase 4bn-H does not run diagnostics; does not authorize any
  future diagnostic implementation; does not pre-decide any diagnostic
  scope on the expanded envelope.**

## 12. Storage posture for any future acquisition

Phase 4bn-H preserves the Phase 4bn-G storage posture verbatim. The
storage posture for any future separately authorized acquisition is
the Phase 4bn-G §12 `A + F + C` baseline:

- **Parquet remains canonical.** Storage A from Phase 4bn-G §10.
  Per-day partitioned Parquet under `data/microstructure/` per the
  Phase 4bb-F canonical path policy; gitignored under
  `.gitignore:85: data/microstructure/`; never committed; immutable
  per `dataset-versioning.md`.
- **DuckDB querying Parquet in place is the preferred non-invasive
  query layer if needed.** Storage C from Phase 4bn-G §10. SQL-shaped
  joins and ad-hoc analytical queries can use DuckDB on top of the
  canonical Parquet without copying data; the Parquet remains the
  source of truth. No `.duckdb` database file is created.
- **DuckDB database cache is deferred.** Storage D from Phase 4bn-G
  §10. A derived `.duckdb` database cache may duplicate storage
  rather than reduce it. Deferred until the actual workload measured
  against an Option C expansion shows whether the cache is justified.
  Any future cache decision requires a separately authorized
  storage-architecture decision memo.
- **Parquet compaction is deferred.** Storage B from Phase 4bn-G §10.
  Codec / dictionary / row-group / partitioning policy decisions
  should not be made until the acquisition envelope and query workload
  are defined. Compaction is a forward-only policy for any future
  acquisition; retroactive rewrite of existing v002 artefacts is
  structurally rejected (Phase 4bn-G §11).
- **SQLite remains runtime / control metadata only, not research
  matrices.** Storage E from Phase 4bn-G §10 preserved verbatim.
  Runtime / research separation per `data-requirements.md` Core
  Principle 7 and `docs/08-architecture/database-design.md` is
  binding. Storage E in the research role is structurally rejected.
- **No storage migration is authorized.** Phase 4bn-H does not migrate
  any storage; does not change any partitioning policy; does not change
  any compression policy; does not change any dataset layout. The
  storage posture above applies to any *future* separately authorized
  acquisition; it does not authorize any storage change in Phase 4bn-H
  itself.
- **No database is created.** Phase 4bn-H does not create any DuckDB,
  SQLite, or other database file.
- **No Parquet is compacted.** Phase 4bn-H does not compact any
  Parquet partition; does not rewrite any sidecar; does not change any
  per-day layout.

The storage posture above is binding on any future separately
authorized acquisition execution plan and on any future separately
authorized acquisition phase. Any deviation requires a separately
authorized storage-architecture decision memo per the Phase 4bn-G §14
ten pre-storage-migration gates.

## 13. Pre-acquisition gates

Phase 4bn-H records the gates that must be passed before any future
acquisition phase could be authorized. Phase 4bn-H **records** these
gates; it **does not pre-decide** them. The gates extend the Phase
4bn-G §13 14-gate framework by narrowing it to the chosen Option B
shape and 12-month default recommendation; the Phase 4bn-G gates remain
binding verbatim, and Phase 4bn-H adds no looser gate.

1. **Acquisition execution plan must be separately authorized and
   merged into `main`.** A separately authorized Tier 1 docs-only
   acquisition execution plan must be present on `main` (per Phase
   4bn-G §13.1 acquisition-readiness memo gate plus a more concrete
   execution plan). Phase 4bn-H is the acquisition-readiness memo;
   the execution plan would be a separately authorized later phase.
2. **Exact calendar range must be fixed before acquisition.** The
   acquisition execution plan must declare the exact UTC date range
   to be acquired (e.g., 2024-04-01 .. 2025-03-31 for a 12-month
   recommended envelope; the operator may choose any specific 12-month
   window that satisfies Phase 4bn-G §8.1 calendar coverage). Once
   fixed, the range cannot drift; any change requires a new execution
   plan.
3. **Disk-footprint estimate must be recorded before acquisition.**
   The execution plan must declare a realistic raw + normalized +
   feature + label disk footprint estimate, the scaling rule used
   (per-day cost × number of days × number of symbols), the comparison
   to the current v002 footprint (per Phase 4bn-G §8.21), and an
   explicit disk-footprint cap that triggers fail-closed if exceeded.
4. **Derivation-time estimate must be recorded before acquisition.**
   The execution plan must declare a realistic normalisation / feature
   / label derivation time estimate using the Phase 4bn-E diagnostic
   runtime (553.6 s on 75 partitions × 2 passes) as the baseline
   scaling unit (per Phase 4bn-G §8.22), and an explicit cost cap that
   triggers fail-closed if exceeded.
5. **Source endpoint policy must be confirmed.** The execution plan
   must confirm from committed docs (per
   `docs/04-data/historical-data-spec.md` canonical Binance USDⓈ-M
   futures source policy) or via a separately authorized source-policy
   memo that the chosen window is covered by the existing source
   endpoint set without change. Any source-endpoint divergence
   requires a separately authorized source-policy memo before
   acquisition.
6. **Canonical path layout must be predeclared.** The execution plan
   must predeclare the exact `data/microstructure/raw/`,
   `data/microstructure/normalized/`, `data/microstructure/features/`,
   `data/microstructure/labels/`, and `data/microstructure/manifests/`
   path layout for the new artefacts under the Phase 4bb-F canonical
   path policy; no path drift permitted.
7. **Phase 4bb-F sidecar policy must be preserved.** Every acquired
   raw, normalized, feature, label, and manifest artefact must carry
   a canonical Phase 4bb-F sidecar (`<sha>  <basename>\n` two-space
   separator; LF only; no CRLF; no BOM; no extra fields;
   refuse-overwrite). No sidecar drift permitted.
8. **Manifest schema impact must be predeclared.** The execution plan
   must predeclare whether the new manifests preserve the existing
   v002 schema exactly (no `__vNNN` bump), whether they require an
   additive change (which still triggers a new dataset version per
   `dataset-versioning.md`), or whether they require a breaking change
   (which triggers a new version with explicit predecessor reference).
   Under the recommended Option B / 12-month / v002-semantics-preserved
   envelope, the expectation is that the v002 schema is preserved
   exactly and no schema-driven version bump is required for the
   feature / label families (the schema bump applies to any new raw
   manifest produced by a per-day acquisition that conforms to the
   existing raw schema).
9. **Existing v002 sealed test split must remain sealed.** The
   execution plan must record verbatim that the existing 15-day sealed
   test split (2025-02-14 .. 2025-02-28; 23,797,822 rows;
   `test_rows_loaded: 0`) remains sealed and is not inspected. The
   `iter_partitions(split="test", ...)` raise pattern in the existing
   Phase 4bn-B implementation is unchanged.
10. **New holdout policy, if any, must be predeclared and sealed.**
    If the execution plan introduces a new test holdout for the
    expanded envelope (for example, a new 15-day or larger sealed
    terminal window inside the expansion), the holdout must be sealed
    by construction; opening it requires a separately authorized
    terminal-holdout phase that does not exist and is not authorized
    by Phase 4bn-H.
11. **Fail-closed stop conditions must be defined.** The execution
    plan must declare the exact conditions under which acquisition
    fails closed (see §14 below).
12. **No `research_eligible` or manifest eligibility transitions from
    acquisition alone.** Per Phase 4bn-G §13.8, every acquired
    family's manifest must start at `research_eligible: false`,
    `eligibility_gate_status: "pending"`,
    `chronological_split_policy: "not_yet_defined"`,
    `diagnostics_authorized: false`, `ml_authorized: false`. No
    transition is authorized by the acquisition phase itself. Phase
    4aw `flip_research_eligible(...)` always-raises invariant
    preserved (never invoked by acquisition).
13. **No ML execution from acquisition alone.** Any ML execution on
    the expanded envelope requires a separately authorized Tier 1
    ML-baseline implementation phase. The acquisition phase produces
    raw / normalized / feature / label artefacts; it does not produce
    ML artefacts.
14. **No strategy / backtest execution from acquisition alone.** Any
    strategy research, signal generation, PnL simulation, or backtest
    on the expanded envelope requires a separately authorized phase.
    The acquisition phase does not authorize any of these.

The 14 gates above extend Phase 4bn-G §13 by narrowing it to the
Option B shape; the Phase 4bn-G gates remain binding verbatim. Phase
4bn-H softens none of them.

## 14. Stop conditions and fail-closed rules

Phase 4bn-H records the exact stop conditions that any future
separately authorized acquisition execution plan must declare. Phase
4bn-H **defines** these stop conditions; it **does not execute** any
acquisition.

1. **Endpoint / source-policy mismatch.** If the chosen window is not
   covered by the canonical Binance USDⓈ-M futures source policy
   without change, acquisition fails closed until a separately
   authorized source-policy memo records the divergence and re-authorises
   the execution plan.
2. **Unexpected schema.** If any acquired raw archive's schema
   differs from the v002 expected schema (per `historical-data-spec.md`
   §"Standard futures kline schema" / aggTrades equivalent), the
   per-day acquisition fails closed; the archive is preserved on disk
   under `data/microstructure/raw/` with its sidecar; no normalization,
   feature derivation, or label derivation proceeds on that day until
   the schema divergence is governed by a separately authorized
   schema-change memo.
3. **Timestamp monotonicity or gap issue.** If any acquired raw
   archive exhibits a timestamp monotonicity violation, an unexpected
   gap, an unexpected duplicate, or any other data-integrity failure
   per `historical-data-spec.md` §"Data Quality Policy", the per-day
   acquisition fails closed; the archive is preserved with its sidecar
   for diagnostic review; no downstream derivation proceeds on that
   day.
4. **Sidecar mismatch.** If any sidecar fails the canonical Phase
   4bb-F format check (`<sha>  <basename>\n` two-space separator; LF
   only; no CRLF; no BOM; no extra fields), the acquisition fails
   closed until the sidecar is canonicalised per the Phase 4bl-F
   R-SIDECAR-CRLF standing rule (Tier 2 controlled remediation) or
   until a separately authorized memo governs the divergence.
5. **Hash mismatch.** If any acquired raw archive's recomputed SHA256
   differs from the embedded sidecar SHA256, the per-day acquisition
   fails closed; the archive is treated as suspect; no downstream
   derivation proceeds.
6. **Disk-footprint cap exceeded.** If the cumulative disk footprint
   exceeds the cap declared in the execution plan (per §13.3 above),
   the acquisition fails closed at the next per-day boundary; no
   further per-day acquisition proceeds without a separately
   authorized cap update.
7. **Derivation-time cap exceeded.** If the cumulative derivation
   time exceeds the cap declared in the execution plan (per §13.4
   above), the acquisition fails closed at the next per-day boundary;
   no further per-day derivation proceeds without a separately
   authorized cap update.
8. **Missing archive.** If any expected per-day raw archive is missing
   from the source endpoint (e.g., a gap day), the per-day acquisition
   fails closed for that day; the gap is recorded in the manifest's
   `known_issues` field; no silent gap repair is permitted.
9. **Duplicate archive.** If a per-day raw archive is fetched a
   second time, the existing archive must not be overwritten (Phase
   4bb-F refuse-overwrite policy); the duplicate fetch fails closed
   and is logged for diagnostic review.
10. **Manifest validation failure.** If any acquired manifest fails
    the existing `dataset-versioning.md` validation (missing required
    field, schema-version mismatch, predecessor reference missing,
    primary-key inconsistency), the per-family acquisition fails
    closed; no downstream derivation proceeds.
11. **Any accidental test-holdout access.** Any attempt to read,
    inspect, hash, evaluate, or unseal the existing v002 sealed test
    split (2025-02-14 .. 2025-02-28) or any new test holdout that the
    execution plan introduces is a fail-closed event; the
    `iter_partitions(split="test", ...)` raise pattern in the Phase
    4bn-B implementation is the canonical enforcement; any new
    derivation kernel must implement an equivalent invariant.
12. **Any attempt to commit data artefacts.** Any attempt to
    `git add` a file under `data/microstructure/` or `data/research/`
    is a fail-closed event; the `.gitignore` rules
    (`.gitignore:85: data/microstructure/`,
    `.gitignore:88: data/research/`) plus the per-phase
    `git check-ignore -v` verification gate make accidental commits
    detectable; the per-phase fail-closed rule then aborts the commit.
13. **Any credential / private-endpoint usage.** Any attempt to use
    credentials, `.env`, `.mcp.json`, MCP, Graphify, or any
    authenticated / private / user-stream endpoint is a fail-closed
    event. The acquisition is restricted to public Binance USDⓈ-M
    futures endpoints per `historical-data-spec.md`. Phase 4bl-F §7
    N-CREDENTIALS and N-ENDPOINT blocks apply verbatim.

The stop conditions above are binding on any future separately
authorized acquisition execution plan and on any future separately
authorized acquisition phase. They subsume Phase 4bn-G §8.24's "exact
stop conditions" requirement at one level lower of abstraction. Phase
4bn-H softens none of them.

## 15. What this would and would not answer

If the operator separately authorizes the recommended Option C
(12-month continuous BTCUSDT) execution plan, and the execution plan is
itself separately authorized and merged, and a separately authorized
acquisition phase actually acquires the data, and the acquired data
passes its raw / derived / feature / label eligibility gates, and a
separately authorized successor descriptive ML-baseline phase analogous
to Phase 4bn-B is run on the expanded envelope, then **the result would
answer**:

- whether the small descriptive lift observed at 15s in Phase 4bn-B is
  reproducible across a 12-month window;
- whether the §11.6 cost-commensurability fractions (15s 6.2 % > 1× /
  1.6 % > 2× / 0.16 % > 5×; 60s 18.3 % > 1× / 5.8 % > 2× / 0.93 % > 5×)
  are stable across a 12-month window or vary materially with regime;
- whether the severe high-confidence calibration tail at 15s (reliability
  gaps −0.061 to −0.392 in the 0.6 – 1.0 bins; 0.8 – 0.9 bin's empirical
  accuracy 0.4881 below the majority floor) is stable across a 12-month
  window or improves / worsens at scale;
- whether the Phase 4bn-E count-up / mean-quantity-down feature drift
  direction generalises across a 12-month window or reverses at scale;
- whether the broad sufficiency / representativeness / outlier-status
  question Phase 4bn-F surfaced as unresolved gains usable evidence
  across a 12-month window;
- whether the descriptive picture is *broadly* consistent with the
  existing 90-day picture (in which case the 90-day window's
  representativeness is more credible than feared) or *broadly*
  inconsistent (in which case the 90-day window's representativeness
  was overestimated and the project gains structurally important
  information regardless of direction).

And the result would **not answer**:

- whether the v002 family has predictive edge;
- whether the v002 family is tradable;
- whether the v002 family is profitable;
- whether the v002 family supports any specific trade signal;
- whether the v002 family supports any specific strategy;
- whether the v002 family is paper-/shadow-/live-ready;
- whether high-confidence predictions become tradable through threshold
  tuning, recalibration, or any other rescue;
- whether 1s or 5s horizons (deferred at Phase 4bn-A §10) become
  viable;
- whether ETHUSDT shows similar patterns (deferred to a separately
  authorized future cross-symbol comparison phase);
- whether a v003 family is needed (deferred to a separately authorized
  future family-design memo only if v002 inadequacy is shown);
- whether any compaction (Storage B) or DuckDB cache (Storage D) is
  justified (deferred to a separately authorized future
  storage-architecture decision memo).

The candidate acquisition would therefore be an *interpretability
expansion*, not an *edge search*. Phase 4bn-H records this distinction
verbatim and rejects any framing that treats acquisition as a path to
edge.

## 16. Decision

**`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Rationale (anchored to §5 – §15):

1. The Phase 4bn-G recommendation to author a docs-only
   acquisition-readiness memo is honoured by this memo; Phase 4bn-H
   *is* the acquisition-readiness memo.
2. The acquisition-readiness framework has now been recorded at one
   level lower of abstraction than Phase 4bn-G §8 – §15: Phase 4bn-H
   names a specific candidate expansion shape (Option B — longer
   single continuous BTCUSDT aggTrades history), a specific calendar
   coverage (12 months as the recommended first expansion among A / B
   / C / D / E), a specific data-family contract (v002 semantics
   preserved), a specific storage posture (`A + F + C` baseline
   preserved verbatim), specific pre-acquisition gates (14 gates
   extending Phase 4bn-G §13), and specific stop conditions (13
   conditions extending Phase 4bn-G §8.24).
3. The recommended next docs-only / design-only / scoping-only
   successor is therefore a docs-only acquisition execution plan
   (provisional Phase 4bn-I; *not* authorized) that pre-declares the
   exact UTC date range, the exact disk-footprint cap, the exact
   derivation-time cap, the exact canonical path layout, the exact
   sidecar / manifest policy, the exact source-endpoint policy
   confirmation, the exact test-holdout preservation language, the
   exact new-holdout policy (if any), and the exact fail-closed stop
   conditions. The acquisition execution plan is itself **docs-only /
   design-only / scoping-only** and authorizes nothing executable.
4. The operator may equivalently choose any of: remain paused; request
   a merge prompt for Phase 4bn-H; reject further ML-baseline
   successors and close the ML arc; separately authorize only a
   future docs-only storage-architecture decision memo (without the
   acquisition execution plan); separately authorize a future
   docs-only combined acquisition execution plan + storage-architecture
   decision memo; separately authorize the recommended docs-only
   acquisition execution plan. Phase 4bn-H does not foreclose any of
   these alternatives.
5. Phase 4bn-H is **recommendation-only**. The successor is not
   authorized by Phase 4bn-H. A separate operator authorization is
   required for any executable follow-up. No acquisition is
   authorized. No storage migration is authorized. No database is
   created. No Parquet is compacted. No v003 dataset is created. No
   manifest is mutated. No ML execution is authorized. No strategy /
   signal / PnL / backtest is authorized.

## 17. Recommended state and successor options

**Recommended state: remain paused.**

Phase 4bn-H is **recommendation-only** and does not authorize any
successor. The operator may equivalently choose any of the following:

- **remain paused** (default; no successor authorized; Phase 4bn-H's
  recommendation does not pressure the operator to authorize a
  successor);
- **request a merge prompt for Phase 4bn-H** so the acquisition-readiness
  scoping decision becomes project-complete on `main`;
- **reject further ML-baseline successors and close the ML arc**
  (operationally close the v002 ML-baseline family for further bounded
  expansion under current evidence; preserve all Phase 4bn-A / 4bn-B /
  4bn-C / 4bn-D / 4bn-E / 4bn-F / 4bn-G artefacts as research evidence;
  preserve every retained verdict and project lock; no further v002
  ML-baseline follow-up under this arc unless reopened by a separately
  authorized future phase; does not delete evidence; does not close
  Prometheus);
- **separately authorize the recommended docs-only acquisition
  execution plan (recommended)** that pre-declares the exact UTC date
  range, disk-footprint cap, derivation-time cap, canonical path
  layout, sidecar / manifest policy, source-endpoint policy
  confirmation, test-holdout preservation language, new-holdout
  policy (if any), and fail-closed stop conditions for the chosen
  Option C (12-month continuous BTCUSDT) expansion shape; must remain
  docs-only and design-only; must not authorize any acquisition; must
  not authorize any storage migration; must not create a database;
  must not compact Parquet; must not create a v003 dataset; must not
  mutate any manifest, sidecar, gate report, or successor-state
  artefact;
- **separately authorize a future docs-only storage-architecture
  decision memo only** (without the acquisition execution plan); this
  is a weaker variant of the recommended path and is provided as an
  operator alternative; must remain docs-only and must not authorize
  any storage migration;
- **separately authorize a future docs-only combined acquisition
  execution plan + storage-architecture decision memo** (one level
  lower in abstraction than Phase 4bn-H; same recommendation pattern;
  same docs-only constraints).

**No acquisition / paper / shadow / live / exchange-write option is
valid from this state.**

## 18. Explicit non-authorizations

Phase 4bn-H is docs-only / design-only / scoping-only and authorizes
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
  row-group policy applied to existing artefacts; no derived
  `.duckdb` database file creation; no SQLite database file creation;
  no other database file creation);
- any ML training, model scoring, prediction generation, feature
  ranking, feature selection, feature pruning, model selection through
  results, hyperparameter tuning, threshold tuning, calibrator
  fitting, meta-labeling, ensemble construction, or any other ML
  execution;
- any strategy research, strategy design, signal generation,
  trade-signal generation, PnL simulation, equity-curve construction,
  Sharpe / Sortino / drawdown / hit-rate / trade-PnL metrics,
  backtests, or walk-forward optimization;
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
- Phase 4bn-I (or any phase under any name performing the recommended
  docs-only acquisition execution plan, or any docs-only
  storage-architecture decision memo, or any docs-only combined
  acquisition execution plan + storage-decision memo, or any
  acquisition phase, or any storage-migration phase, or any
  database-creation phase, or any v003-creation phase);
- any further Phase 4bn-* successor / Phase 4bo-* / Phase 4bp-*;
  Phase 5; Phase 4 canonical;
- paper / shadow; live-readiness; deployment; exchange-write;
  production-key creation; authenticated APIs; private endpoints;
  user stream; WebSocket implementation;
- any revision of a retained verdict, any loosening of a project lock,
  or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F /
  Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bn-H is a docs-only / design-only / scoping-only
acquisition-readiness memo.** **Phase 4bn-H does not acquire data.**
**Phase 4bn-H does not migrate storage.** **Phase 4bn-H does not create
any database.** **Phase 4bn-H does not compact Parquet.** **Phase 4bn-H
does not create v003.** **Phase 4bn-H does not authorize acquisition.**
**Phase 4bn-H does not authorize any successor.** **Phase 4bn-H does
not run diagnostics.** **Phase 4bn-H does not run ML.** **Phase 4bn-H
does not train models.** **Phase 4bn-H does not score models.** **Phase
4bn-H does not generate predictions.** **Phase 4bn-H does not inspect
the test holdout.** **Phase 4bn-H does not use the sealed test split.**
**Phase 4bn-H does not rank features.** **Phase 4bn-H does not select
features.** **Phase 4bn-H does not prune features.** **Phase 4bn-H does
not engineer features.** **Phase 4bn-H does not tune hyperparameters.**
**Phase 4bn-H does not tune thresholds.** **Phase 4bn-H does not fit
calibrators.** **Phase 4bn-H does not run strategy research.** **Phase
4bn-H does not define a strategy.** **Phase 4bn-H does not generate
trade signals.** **Phase 4bn-H does not simulate PnL.** **Phase 4bn-H
does not run backtests.** **Phase 4bn-H does not modify dataset
layout.** **Phase 4bn-H does not call any public, authenticated, or
private endpoint.** **Phase 4bn-H does not open any WebSocket or user
stream.** **Phase 4bn-H does not use credentials, `.env`, `.mcp.json`,
MCP, or Graphify.** **Phase 4bn-H does not mutate any manifest.**
**Phase 4bn-H does not mutate any successor-state artefact.** **Phase
4bn-H does not commit `data/microstructure`.** **Phase 4bn-H does not
commit `data/research`.** **Phase 4bn-H does not authorize Phase 4bn-I,
Phase 5, paper / shadow, live-readiness, deployment, exchange-write,
production keys, or any successor phase.**

## 19. Current-project-state update summary

The narrow `docs/00-meta/current-project-state.md` update made by Phase
4bn-H consists of:

- a new Phase 4bn-H paragraph appended immediately after the Phase
  4bn-G paragraph;
- a new Current-phase block for Phase 4bn-H inserted immediately after
  the new Phase 4bn-H paragraph and immediately before the existing
  Phase 4bn-G Current-phase block;
- preservation of every earlier paragraph (Phase 4a .. Phase 4bn-G)
  and every earlier Current-phase block (Phase 4bn-G, Phase 4bn-F,
  Phase 4bn-E, Phase 4bn-D, Phase 4bn-C, Phase 4bn-B, and older
  blocks) as labelled historical context;
- recording of Phase 4bn-H as **branch-complete only, not merged, not
  project-complete**;
- recording of the Phase 4bn-H decision
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
- recording of the exact non-authorizations (per §0 / §3 / §18 of this
  memo);
- recording of the recommended state (**remain paused**);
- explicit statement that a Phase 4bn-I successor (or any equivalent
  under any name) is recommended but **not authorized** by Phase
  4bn-H.

No other section of `docs/00-meta/current-project-state.md` is modified
by Phase 4bn-H. No retained verdict, project lock, manifest field,
successor-state field, gate-report field, or governance label is
changed. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked by Phase 4bn-H).

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

All prior phase results (Phase 4am .. Phase 4bn-G) preserved verbatim.

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
  always-raises invariant (never invoked by Phase 4bn-H)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule +
  nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## Appendix C — Recommended next state

**Remain paused.** Phase 4bn-H is branch-complete only by this work.
Per the `phase-workflow-standard.md` rule, it is NOT project-complete
until a separately authorized merge phase records its merge-closeout
on `main` per `merge-closeout-standard.md` (Tier 1). The scoping
decision
`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
is a recommendation only and authorizes nothing. **Phase 4bn-I (or any
equivalent under any name) is not authorized by Phase 4bn-H.** **Any
acquisition phase requires a separately authorized phase.** **Any
storage-migration phase requires a separately authorized phase.**
**Any v003-creation phase requires a separately authorized phase.**
**Any database-creation phase requires a separately authorized phase.**
**Any Parquet-compaction phase requires a separately authorized
phase.** **Recommended state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-I docs-only /
design-only / scoping-only acquisition execution plan (focused on the
recommended Option C — 12-month continuous BTCUSDT aggTrades history,
preserving v002 semantics, Parquet canonical storage, DuckDB-in-place
query posture, and no ETHUSDT / v003 / compaction / cache in the first
expansion) is the cleanest non-paused option. It would, if separately
authorized later, pre-declare the exact UTC date range, the exact
disk-footprint cap, the exact derivation-time cap, the exact canonical
path layout, the exact sidecar / manifest policy, the exact
source-endpoint policy confirmation, the exact test-holdout
preservation language, the exact new-holdout policy (if any), and the
exact fail-closed stop conditions; and record an explicit
non-authorization for both acquisition and storage migration. Phase
4bn-I is **not authorized** by this memo. The operator may equivalently
choose to remain paused, to reject further successors and close the
ML arc, to separately authorize only a docs-only storage-architecture
decision memo, or to separately authorize a docs-only combined
acquisition execution plan + storage-decision memo; Phase 4bn-H does
not foreclose any of these alternatives.
