# Phase 4bn-D — Multi-Day V002 Bounded ML-Baseline Expansion Scoping Memo

**Phase identity:** Phase 4bn-D — Multi-Day V002 Bounded ML-Baseline Expansion Scoping Memo (docs-only / design-only / scoping-only governance memo; Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3; the separately authorized scoping phase that follows the Phase 4bn-C interpretation decision `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`).
**Date:** 2026-05-29.
**Branch:** `phase-4bn-d/bounded-ml-baseline-expansion-scoping`.
**Base SHA:** `main` at `e1dc2fa4570baccfc9e4a866899ca6c98fa03c66` (Phase 4bn-C SHA-finalization commit `docs(phase-4bn-c): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. Phase 4bn-D scopes the design surface for a possible future ML-baseline expansion implementation phase and is adjacent to ML execution, model selection, feature selection, hyperparameter tuning, threshold tuning, strategy research, backtests, label / target rework, and test-holdout misuse while explicitly authorizing none of them.
**Phase type:** docs-only / design-only / scoping-only. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` (this memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created or mutated. **No** diagnostic rerun. **No** ML rerun. **No** ML artefact. **No** acquisition. **No** successor authorization.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 0. Required exact phrases

- **Phase 4bn-D is a docs-only / design-only / scoping-only bounded ML-baseline expansion scoping memo.**
- **Phase 4bn-D does not train ML models.**
- **Phase 4bn-D does not run ML.**
- **Phase 4bn-D does not score models.**
- **Phase 4bn-D does not generate predictions.**
- **Phase 4bn-D does not generate reusable split masks.**
- **Phase 4bn-D does not persist model binaries.**
- **Phase 4bn-D does not persist row-level predictions.**
- **Phase 4bn-D does not read, inspect, evaluate, or report any test-holdout metric.**
- **Phase 4bn-D does not use the sealed test split.**
- **Phase 4bn-D does not select models through results.**
- **Phase 4bn-D does not rank features.**
- **Phase 4bn-D does not select features.**
- **Phase 4bn-D does not tune hyperparameters.**
- **Phase 4bn-D does not tune thresholds.**
- **Phase 4bn-D does not run strategy research.**
- **Phase 4bn-D does not define a strategy.**
- **Phase 4bn-D does not generate trade signals.**
- **Phase 4bn-D does not simulate PnL.**
- **Phase 4bn-D does not run backtests.**
- **Phase 4bn-D does not run diagnostics.**
- **Phase 4bn-D does not rerun Phase 4bn-B.**
- **Phase 4bn-D does not acquire data.**
- **Phase 4bn-D does not call any public, authenticated, or private endpoint.**
- **Phase 4bn-D does not open any WebSocket or user stream.**
- **Phase 4bn-D does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.**
- **Phase 4bn-D does not mutate any manifest.**
- **Phase 4bn-D does not mutate any successor-state artefact.**
- **Phase 4bn-D does not commit `data/microstructure`.**
- **Phase 4bn-D does not commit `data/research`.**
- **Phase 4bn-D does not authorize Phase 4bn-E, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, or any successor phase.**
- **Recommended state remains paused.**

---

## 1. Purpose

Phase 4bn-D answers a single governance / scoping question:

> Given Phase 4bn-C interpreted the Phase 4bn-B ML-baseline evidence and recommended only `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` — what, at design level only and without running anything, would a tightly bounded follow-up ML-baseline expansion phase be permitted to evaluate, under what predeclared constraints, and is any such future phase recommended (subject to separate operator authorization) or should the project remain paused?

Phase 4bn-D is **docs-only / design-only / scoping-only**. It reads only committed repository Markdown reports as the evidence base. It does not open or depend on local gitignored `data/research/` ML outputs. It trains nothing, scores nothing, predicts nothing, evaluates nothing on test data, selects nothing, ranks nothing, tunes nothing, runs nothing, materializes no artefact, mutates no manifest or successor-state artefact, acquires no data, and authorizes no successor implementation. **Phase 4bn-D is a docs-only / design-only / scoping-only bounded ML-baseline expansion scoping memo.** **This is the design / scoping step of the ML arc, not ML execution.**

This memo:

- carries the Phase 4bn-C interpretation forward verbatim as the current authoritative reading of the first ML-baseline evidence;
- preserves the corrected interpretation of Phase 4bn-B evidence (flat-class underrepresented, near-balanced binary in practice, small but reproducible linear lift at 15s, well-calibrated dominant bin with over-confident tail, persistence uncalibrated on log-loss / Brier, cost-commensurability fractions per horizon);
- enumerates a bounded candidate menu of expansion paths that a possible future implementation phase could be allowed to evaluate, each classified by purpose, evidence basis, allowed inputs, forbidden inputs, expected output, failure / stop condition, and explicit non-strategy / non-signal / non-edge status;
- records a single scoping decision and, if a successor is recommended, frames it as a recommendation only requiring separate operator authorization.

## 2. Authority and repository state

- **Repository:** Prometheus.
- **Active machine:** Desktop.
- **Local repo path:** `C:\Prometheus`.
- **Claude Code lightweight workspace:** `C:\ClaudeRuns\prometheus-light` (Phase 4bm-D-P1 lightweight workspace standard preserved).
- **Authority documents read for this memo (committed repository Markdown only):**
  - `docs/00-meta/current-project-state.md` (current high-level project state).
  - `docs/00-meta/process/phase-workflow-standard.md` (eleven-step phase lifecycle).
  - `docs/00-meta/process/phase-risk-tiering-standard.md` (Phase 4bl-F four-tier risk model, R-SIDECAR-CRLF standing rule, nine reusable non-authorization blocks).
  - `docs/00-meta/process/phase-prompt-template.md` (authorization-prompt structure standard).
  - `docs/00-meta/process/operator-report-standard.md` (Claude Code compact report + ChatGPT operator-facing response standard).
  - `docs/00-meta/process/merge-closeout-standard.md` (merge-closeout 16-section structure).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_merge-closeout.md` (Phase 4bn-C merge-closeout; `MEMO RECORDED — RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_ml-baseline-evidence-interpretation-memo.md` (Phase 4bn-C interpretation memo; corrected reading of Phase 4bn-B evidence; twelve forensic hypotheses; five candidate paths evaluated).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_closeout.md` (Phase 4bn-C closeout).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_merge-closeout.md` (Phase 4bn-B merge-closeout; `RECORD_EVIDENCE_ONLY`).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_multi-day-v002-ml-baseline-implementation.md` (Phase 4bn-B implementation report).
  - `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_closeout.md` (Phase 4bn-B closeout).
  - `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_merge-closeout.md` (Phase 4bn-A merge-closeout; `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION`).
  - `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_ml-baseline-implementation-scoping-design.md` (Phase 4bn-A scoping / design memo).
  - `docs/00-meta/implementation-reports/2026-05-27_phase-4bn-a_closeout.md` (Phase 4bn-A closeout).
- **Inputs explicitly NOT used:** local gitignored `data/research/microstructure/ml-baselines/phase-4bn-b/` outputs (Phase 4bn-B local artefacts); local gitignored Phase 4bm-W / Phase 4bm-Q / Phase 4bm-S / Phase 4bm-U / Phase 4bm-X artefacts. Phase 4bn-D treats Phase 4bn-C's committed Markdown record as the authoritative summary of Phase 4bn-B evidence; no re-hashing or re-reading of any local data file is performed in this docs-only / design-only / scoping-only phase.
- **README:** README may be stale and is **not** used as current-state authority. The authority is `docs/00-meta/current-project-state.md` plus the most recent merge-closeout, plus the most recent implementation reports (per `docs/00-meta/process/phase-workflow-standard.md` "Repo-query requirement for new chats").
- **Pre-branch verification:** `git rev-parse main == git rev-parse origin/main == e1dc2fa4570baccfc9e4a866899ca6c98fa03c66`. Phase 4bn-C merge commit `cf6172f4468d3ae28d91a0b3f016a00ba5d9159a` and merge-closeout commit `7fca0d538418293fe9b556a8aa67c26ad6165f52` present on `main` immediately below the SHA-finalization commit. Predecessor chain (Phase 4bn-A → Phase 4bn-B → Phase 4bn-C) is fully merge-complete on `main`.

## 3. Phase type and strict scope

Phase 4bn-D is **docs-only / design-only / scoping-only**.

**Allowed surface (tracked files added or modified):**

- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_bounded-ml-baseline-expansion-scoping.md` (this memo; new).
- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_closeout.md` (closeout; new).
- `docs/00-meta/current-project-state.md` (narrow current-phase paragraph + Current-phase block addition; prior Phase 4bn-A / 4bn-B / 4bn-C history preserved as labelled historical context).

**Forbidden surface (verbatim):**

- No source code modification.
- No test modification.
- No committed-script modification.
- No `pyproject.toml`, `README.md`, `.gitignore`, or MCP file modification.
- No `data/microstructure/` artefact created, modified, or committed.
- No `data/research/` artefact created, modified, or committed.
- No manifest, sidecar, gate-report, or successor-state artefact created, modified, or accessed for mutation.
- No ML model trained, scored, evaluated, persisted, or referenced for selection.
- No row-level prediction generated or persisted.
- No reusable split mask generated or persisted.
- No feature ranked or selected.
- No hyperparameter or threshold tuned.
- No strategy defined, designed, or run.
- No trade signal generated.
- No PnL simulated.
- No backtest run.
- No diagnostics rerun.
- No Phase 4bn-B rerun.
- No data acquired.
- No public, authenticated, or private endpoint called.
- No WebSocket or user stream opened.
- No credential, `.env`, `.mcp.json`, MCP, or Graphify use.
- No retained verdict revised.
- No project lock loosened.
- No M0 amendment.
- No `research_eligible`, `eligibility_gate_status`, `chronological_split_policy`, `diagnostics_authorized`, or `ml_authorized` transition on any actual manifest.
- No successor authorized.

The non-authorization wording above subsumes the reusable Phase 4bl-F §7 blocks **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, and **N-VERDICT-LOCK**; each block applies in full to Phase 4bn-D.

## 4. Evidence base read for this memo

Phase 4bn-D reads, read-only, the committed repository Markdown documents enumerated in §2. It reads no local gitignored artefact. It re-hashes no local file. It does not invoke any normalizer, gate runner, label kernel, feature kernel, ML runner, diagnostic runner, backtest runner, simulator, or acquisition runner. It does not call `ml_baseline_runner.run(...)` or any equivalent. It does not load any parquet or CSV from `data/microstructure/` or `data/research/`. The Phase 4bn-C merge-closeout, interpretation memo, and closeout are treated as the canonical, sufficient evidence record for the Phase 4bn-B ML-baseline run; this is the explicit guarantee that Phase 4bn-D does not, and cannot, reach for the actual local artefacts.

This boundary is deliberate. It (a) protects the local artefacts from accidental mutation, (b) keeps Phase 4bn-D fully reviewable from `main` without any local state assumption, and (c) honours the Phase 4bk-A `phase-workflow-standard.md` rule that branch-complete reports must record what was actually read so that audit is anchored to repository state rather than to working-directory state.

## 5. Phase 4bn-C interpretation carried forward

The Phase 4bn-C interpretation memo (`docs/00-meta/implementation-reports/2026-05-28_phase-4bn-c_ml-baseline-evidence-interpretation-memo.md`) is the current authoritative interpretation of the first ML-baseline evidence. Its key conclusions are carried forward verbatim by Phase 4bn-D:

- **Phase 4bn-C interpretation decision (verbatim):** `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`.
- **Phase 4bn-B decision carried forward (verbatim):** `RECORD_EVIDENCE_ONLY` (Phase 4bn-B implemented exactly the Phase 4bn-A §9 – §20 design and produced descriptive ML-baseline evidence on the train and validation splits only; the test holdout is sealed with `test_rows_loaded: 0`).
- **Phase 4bn-C does not authorize Phase 4bn-D, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.** Phase 4bn-D is the *separately authorized* scoping phase that the Phase 4bn-C recommendation made conditionally allowable; the operator's separate authorization of Phase 4bn-D is recorded in the authorization prompt that produced this memo. The Phase 4bn-D authorization does not retrospectively elevate the Phase 4bn-C recommendation into anything more than a recommendation.
- The Phase 4bn-C closeout records twelve non-mutually-exclusive forensic hypotheses for the weak baseline-vs-prior separation (H1 label-imbalance / flat-class collapse; H2 target bluntness; H3 horizon-vs-cost mismatch; H4 v002 feature-surface limitations; H5 linear-model simplicity; H6 class-weighting absence by design; H7 shallow-tree memory fail-closed; H8 regime heterogeneity; H9 time-of-day effects; H10 feature-stationarity drift; H11 labels capturing common no-move behavior more than exploitable directional edge; H12 the market may not contain a simple exploitable edge under this family). **None is ranked, weighted, resolved, or converted into a design or strategy proposal by Phase 4bn-D either.** Phase 4bn-D draws on these hypotheses only as a candidate menu of *questions a future implementation phase could be allowed to evaluate*, never as a strategy recommendation.
- The Phase 4bn-C closeout evaluated five candidate follow-up paths and chose option 2 (`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`). Phase 4bn-D is *that* scoping memo. Phase 4bn-D does not revisit options 1, 3, 4, or 5 of Phase 4bn-C as alternative paths; the operator separately authorized Phase 4bn-D specifically to scope the bounded expansion menu.

This memo defers to Phase 4bn-C on every factual interpretation; Phase 4bn-D draws no new descriptive conclusion about the Phase 4bn-B run and computes no metric.

## 6. Corrected interpretation of Phase 4bn-B evidence

The following corrected interpretation, drawn from the Phase 4bn-C interpretation memo (§9 – §13 of that memo) and the Phase 4bn-C merge-closeout (§6.3 – §6.7), is carried forward verbatim by Phase 4bn-D and is treated as the binding factual frame for any candidate path discussed in §9 – §10. Phase 4bn-D adds no new evidence; it surfaces what Phase 4bn-C established so the design-level discussion that follows is anchored to it.

- **The flat class is underrepresented, not dominant.** Class prevalence on supervised splits (read by Phase 4bn-C from `class_balance_summary.csv` / `per_horizon_model_summary.json`):
  - train × 15s: down 0.4957 / flat 0.0109 / up 0.4934.
  - train × 60s: down 0.5016 / flat 0.0019 / up 0.4965.
  - validation × 15s: down 0.4938 / flat 0.0082 / up 0.4980.
  - validation × 60s: down 0.4950 / flat 0.0015 / up 0.5036.
- **The classification problem is effectively near-balanced up / down with a very thin flat class.** Down ≈ up ≈ 0.495 ± 0.005 on both included horizons in both supervised splits; flat is 0.15 – 1.09 % of supervised rows.
- **Majority baseline accuracy is roughly 49 – 50 %.** Validation majority accuracy floors: 0.4938 (15s) / 0.4950 (60s). Validation majority macro-F1 floors: 0.2204 (15s) / 0.2207 (60s) — much lower than the accuracy floor because the majority baseline predicts only one class.
- **L2 / L1 linear baselines show real but small descriptive lift:**
  - about **+5 pp accuracy at 15s** over majority (validation L2 accuracy 0.5435 vs majority 0.4938).
  - about **+1.5 pp accuracy at 60s** over majority (validation L2 accuracy 0.5095 vs majority 0.4950).
  - about **+14 pp macro-F1 at 15s** (validation L2 macro-F1 0.3638 vs majority 0.2204).
  - about **+11 pp macro-F1 at 60s** (validation L2 macro-F1 0.3291 vs majority 0.2207).
  - the macro-F1 lift is structurally driven by the linear models predicting both up and down at all, while the majority baseline predicts only one of the three classes; the flat class is never predicted by L2 / L1 (per-class P / R / F1 = 0 / 0 / 0 on flat in every cell).
  - L1 and L2 differ in the fourth significant figure on every metric (consistent with weak `1e-4` penalties).
  - train-validation deltas (validation minus train) are small and approximately matched in sign across L1 / L2 (~−0.005 / −0.005 on accuracy / balanced-accuracy / macro-F1 at 15s; ~−0.003 / −0.0004 / −0.008 at 60s) — the models are not overfitting at this level of descriptive measurement.
- **Persistence slightly beats majority on hard accuracy but is catastrophically worse on log-loss and Brier because it emits hard one-hot probabilities.** Persistence-vs-majority on validation: accuracy +2.3 pp (15s) / +0.2 pp (60s); log-loss ~18× the majority floor; Brier ~2× the majority floor. The catastrophic gap is structural (every miss costs −log(ε) ≈ 27.6 nats per row when probabilities are 1.0 on one class). Persistence is **not** a calibrated probabilistic baseline.
- **L2 15s is well-calibrated in the dominant 0.5 – 0.6 confidence bin, but the high-confidence tail is severely over-confident.** The 0.5 – 0.6 bin holds ~86 % of validation rows (mean max p̂ 0.5478 / empirical accuracy 0.5432 / reliability gap −0.0047); the 0.6 – 0.7 bin gap is −0.0610; the 0.7 – 0.8 gap −0.2041; the 0.8 – 0.9 gap −0.3535 (empirical accuracy 0.4881 — *below the majority floor*); the 0.9 – 1.0 gap −0.3916.
- **A naive "trade when confidence is high" idea would fail under current evidence.** The most-confident L2-15s predictions are *no better than chance*; the obvious threshold-tune-for-confidence follow-up would actively make things worse rather than better.
- **15s has stronger model signal but worse cost / tradability context.** At 15s validation, only ~6.2 % of `|forward_log_return|` rows exceed 1× the §11.6 round-trip cost (16 bps); 1.57 % > 2×; 0.16 % > 5×.
- **60s has better cost context but weaker model signal.** At 60s validation, 18.3 % exceed 1×; 5.78 % exceed 2×; 0.93 % exceed 5×; but the L2 accuracy lift over majority is only ~1.5 pp and the model becomes strongly down-biased (38.8 M `pred_down` vs 18.0 M `pred_up` on validation; per-class precision / recall down 0.504 / 0.695 vs up 0.522 / 0.328).
- **None of this is edge, profitability, tradability, strategy-readiness, or a signal.** Statistical descriptive lift on a near-50 / 50 binary in a regime where 80 – 95 % of validation rows have absolute moves below the round-trip cost is not a tradability claim. **Phase 4bn-D inherits this boundary without softening it.**

## 7. Non-goals and non-authorizations

Phase 4bn-D is **not** a model-selection memo, **not** a feature-ranking memo, **not** a hyperparameter-tuning memo, **not** a threshold-tuning memo, **not** a strategy / signal / PnL / backtest memo, **not** an acquisition memo, **not** a manifest-mutation memo, **not** a successor-state-mutation memo, **not** a diagnostics-rerun memo, **not** an ML-rerun memo, **not** a calibration-fit memo, **not** a regime-segmentation execution memo, **not** a label-regeneration memo, **not** an `ml_authorized` / `diagnostics_authorized` transition memo, **not** an authorization for Phase 4bn-E (or any phase under any name performing bounded ML-baseline expansion implementation, label / target rework implementation, class-imbalance / regime-conditioning implementation, calibration-only-analysis implementation, or any successor to the Phase 4bn-* arc), **not** an authorization for Phase 5 / Phase 4 canonical, **not** an authorization for paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / user stream / WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

Phase 4bn-D explicitly does **not** authorize:

- training ML models;
- running ML;
- scoring models;
- generating predictions;
- generating reusable split masks;
- persisting model binaries;
- persisting row-level predictions;
- reading, inspecting, evaluating, or reporting any test-holdout metric;
- using the sealed test split;
- selecting models through results;
- ranking features;
- selecting features;
- tuning hyperparameters;
- tuning thresholds;
- running strategy research;
- defining a strategy;
- generating trade signals;
- simulating PnL;
- running backtests;
- running diagnostics;
- rerunning Phase 4bn-B;
- acquiring data;
- calling public endpoints;
- calling authenticated or private endpoints;
- opening WebSockets or user streams;
- using credentials;
- using `.env`;
- using `.mcp.json`;
- using MCP;
- using Graphify;
- mutating manifests;
- mutating successor-state artefacts;
- committing `data/microstructure`;
- committing `data/research`;
- authorizing Phase 4bn-E;
- authorizing Phase 5;
- authorizing paper / shadow;
- authorizing live-readiness;
- authorizing deployment;
- authorizing exchange-write;
- authorizing production keys.

## 8. Test-holdout seal

The Phase 4bn-A / Phase 4bn-B / Phase 4bn-C test-holdout protection is preserved verbatim by Phase 4bn-D. The 15-day test split (2025-02-14 .. 2025-02-28; 15 partitions; 23,797,822 rows) is **sealed**. The Phase 4bn-B run manifest records `test_holdout_sealed: true`, `test_rows_loaded: 0`, `test_n_partitions_unused: 15` (read only via the Phase 4bn-C carry-forward; Phase 4bn-D opens no JSON). The Phase 4bn-B dataset module's `iter_partitions(split="test", ...)` raises `MlBaselineDatasetError` because `test ∉ SUPERVISED_SPLITS`; the existing test `test_ml_baseline_split_policy_v002.test_test_holdout_iteration_is_forbidden_by_design` enforces this invariant. **Phase 4bn-D inspects no test data, references no test metrics, designs no test-time evaluation, and proposes no per-test threshold, cut, or hyperparameter.** Any candidate path discussed in §9 – §10 below must keep the test holdout sealed; this rule appears as a per-candidate constraint and as a global stop condition (§14).

The Phase 4bm-W envelope-terminal censoring asymmetry (857 rows: 1s 14 / 5s 39 / 15s 170 / 60s 634, all concentrated on 2025-02-28 inside the sealed test split) is carried forward as a non-blocking caveat for any future test-holdout evaluation phase (not authorized by Phase 4bn-D).

## 9. Candidate bounded expansion paths

The Phase 4bn-D authorization prompt enumerates a bounded candidate menu of expansion paths. Each candidate below is described at design level only; for each, §10 records purpose, evidence source, allowed future inputs, forbidden future inputs, expected output if separately authorized later, failure / stop condition, and why it is not a strategy, signal, or trading edge.

The six candidates considered are:

- **C-A — Class weighting / flat-class handling feasibility.** Whether a future implementation phase could be permitted to evaluate inverse-prevalence (or other a-priori, predeclared) class weights in the multinomial softmax loss for the L2 / L1 linear baselines, without selecting weights through validation results and without converting any reweighted output into a trade signal.
- **C-B — Cost-commensurate label framing feasibility.** Whether a future docs-only scoping memo could be permitted to *describe* candidate cost-commensurate label framings (e.g., direction-of-move conditional on `|forward_log_return|` exceeding a multiple of the §11.6 lock, or magnitude-aware ordinal bins, or residual-magnitude labels). This candidate is design-level only at every step — no label generation, no label regeneration, no manifest transition, no successor-state JSON, no acquisition, no strategy framing.
- **C-C — Horizon-envelope feasibility.** Whether a future docs-only scoping memo could be permitted to *describe* candidate horizon-envelope changes (e.g., whether 1s / 5s should remain deferred or be partially included for descriptive parity; whether the 15s / 60s envelope should be widened to one additional horizon strictly for descriptive context). This candidate is design-level only — no kernel rerun, no new horizon labels generated, no acquisition.
- **C-D — Train-vs-validation feature drift diagnostics feasibility.** Whether a future descriptive-only diagnostic could be permitted to evaluate train-vs-validation drift in the v002 feature distributions (Phase 4bm-W diagnostics did not compute this), using train-only fit statistics from `transform_metadata.json` as the reference and the validation split as the comparison surface. Test split remains sealed. No new feature engineering, no feature ranking / selection, no kernel rerun.
- **C-E — Calibration-limited evaluation feasibility.** Whether a future descriptive-only calibration memo could be permitted to extend the Phase 4bn-B 10-bin reliability summary into a per-class and per-horizon calibration table on validation only, without fitting any calibrator, without tuning any threshold, without converting any probability into a trade signal, and without touching the test split.
- **C-F — Optional shallow non-linear baseline feasibility (only if memory and leakage controls can be bounded).** Whether a future docs-only / design-only memo could be permitted to *specify* a memory-bounded, depth-limited shallow tree baseline with predeclared `max_depth`, predeclared chunked / sampled training that fail-closes on memory rather than implicitly downsampling, and explicit leakage-control verification — without actually training it. (Phase 4bn-A §15 authorized this only "if complexity and leakage controls are explicitly bounded"; Phase 4bn-B fail-closed on memory and intentionally did not implement it. This candidate revisits whether the controls could be bounded enough to make a future implementation phase safe, *not* whether to run it.)

**Phase 4bn-D adds no candidate beyond these six.** Each candidate is treated as a discrete, separately evaluable question; the §10 evaluation table is the sole mechanism by which any one candidate could later be selected for a separately authorized successor.

## 10. Candidate path evaluation table

The following per-candidate evaluation enumerates, for each candidate path C-A through C-F, the purpose, evidence source from Phase 4bn-B / 4bn-C, allowed future inputs, forbidden future inputs, expected output if separately authorized later, failure / stop condition, and explicit non-strategy / non-signal / non-edge status. Every cell below is a design-level description only; nothing in this section authorizes any execution.

---

### C-A — Class weighting / flat-class handling feasibility

- **Purpose.** Scope, at design level only, whether a future ML-baseline implementation phase could be permitted to evaluate inverse-prevalence (or another fixed, a-priori, predeclared) class-weight scheme in the multinomial softmax loss for L2 / L1, in order to assess whether the structural non-prediction of the flat class by the un-weighted softmax can be relaxed without converting outputs into trade signals.
- **Evidence source from Phase 4bn-B / 4bn-C.** Phase 4bn-C §9 (flat class underrepresented at 0.15 – 1.09 %; L2 / L1 per-class P / R / F1 = 0 / 0 / 0 on flat; macro-F1 lift structurally driven by predicting both up and down at all). Phase 4bn-C §11 (60s strongly down-biased: 38.8 M `pred_down` vs 18.0 M `pred_up`; per-class P / R asymmetry). Phase 4bn-C §15 H1 / H6 (flat-class collapse; class weighting absent by design).
- **Allowed future inputs (if separately authorized later).** The same train + validation supervised splits used by Phase 4bn-B; train-only fit of any standardization statistic (mirroring Phase 4bn-B `transform_metadata.json`); class-weight values that are predeclared a priori (e.g., inverse prevalence using train-side priors only); the same v002 feature surface (45 `computed_feature_column_names`); the same locked SGD hyperparameter set as Phase 4bn-A §15 (penalty, lr, batch size, epochs, strength, grad clip, RNG seed) extended only by the weighting term; the same exclusion list (17 v002 lineage columns; all label columns; all label-derived fields; any split-flag column; `FORBIDDEN_MODEL_MATRIX_SUBSTRINGS`).
- **Forbidden future inputs.** The sealed test split; any test row; any validation-derived weight (no weight selected through validation results); any new feature; any feature ranking; any feature selection; any hyperparameter selected through validation; any threshold; any probability-to-signal conversion; any reusable split mask; any model binary persistence; any row-level prediction persistence; any acquisition; any endpoint call; any credential; any `.env`; any `.mcp.json`; any MCP / Graphify use; any manifest mutation; any successor-state mutation; any strategy / signal / PnL / backtest; any retained verdict revision; any project lock change.
- **Expected output if separately authorized later.** A descriptive-only local gitignored artefact set (under `data/research/...`, never committed) containing per-class precision / recall / F1, macro-F1, balanced accuracy, mean log-loss, mean Brier, and confusion matrices on train and validation only for the weighted variant, alongside the un-weighted variant for reference; a `class_weight_scheme` block in the run manifest recording the predeclared weighting policy, the train-side priors used to derive it, and the explicit non-use of validation rows in weight selection; canonical Phase 4bb-F sidecars for every output file. **No** strategy artefact, **no** signal artefact, **no** PnL artefact, **no** backtest artefact, **no** test-set artefact, **no** threshold artefact, **no** model binary, **no** row-level prediction, **no** reusable split mask, **no** ranked feature list, **no** chosen feature list, **no** tuned hyperparameter list, **no** tuned threshold list, **no** acquisition artefact.
- **Failure / stop condition.** Any of: (i) the weighting policy would require validation-row inspection to derive; (ii) the implementation would persist a model binary or row-level prediction; (iii) the implementation would touch any test row; (iv) the implementation would propose a threshold or a probability-to-signal conversion; (v) the implementation cannot fit train within the same memory and runtime envelope as Phase 4bn-B; (vi) the implementation introduces any new feature, new column, new label, new horizon, new manifest field, new successor-state field, or any successor authorization. If any of (i) – (vi) holds, Phase 4bn-E (or whatever name) must fail-closed.
- **Why C-A is not a strategy, signal, or trading edge.** C-A would only ask whether a weighted-softmax baseline produces *descriptively* different per-class scores on supervised splits. It would not propose any trade rule, threshold, entry / exit, position, or signal. A weighted-softmax that achieves nominally higher macro-F1 is not a tradability claim; the calibration evidence (Phase 4bn-C §12) still shows that high-confidence predictions are no better than chance, and the cost-commensurability evidence (Phase 4bn-C §13) still shows that 80 – 95 % of validation rows have absolute moves below the round-trip cost. C-A is a descriptive question about the un-weighted baseline's structural flat-class collapse, not a strategy proposal.

---

### C-B — Cost-commensurate label framing feasibility

- **Purpose.** Scope, at design level only, whether a future docs-only scoping memo could be permitted to *describe* candidate cost-commensurate label framings (e.g., direction-of-move conditional on `|forward_log_return|` exceeding a multiple of the §11.6 lock; magnitude-aware ordinal bins; residual-magnitude labels) without generating new labels, without regenerating any v002 artefact, and without touching strategy, signals, PnL, or backtests.
- **Evidence source from Phase 4bn-B / 4bn-C.** Phase 4bn-C §10 / §11 (the strict-sign label collapses magnitude information; a 0.0001 bp move and a 100 bp move contribute the same gradient). Phase 4bn-C §13 (§11.6 cost-commensurability: 6.2 % > 1× at 15s, 18.3 % > 1× at 60s; descriptive context). Phase 4bn-C §15 H2 / H11 (target bluntness; labels capturing common no-move behavior more than exploitable directional edge).
- **Allowed future inputs (if separately authorized later).** The committed Markdown record of Phase 4bn-B and Phase 4bn-C (no local data file opened); the §11.6 cost lock (8 bps per side, 16 bps round trip); the v002 label manifest's `forward_direction_{horizon}` definition (referenced for description only; no field altered); Phase 4bm-W diagnostic summary (referenced for description only; no rerun). The candidate scoping memo would describe what a future *separately authorized* label-design memo *might* be allowed to evaluate; it would not itself generate labels or design any successor.
- **Forbidden future inputs.** Any local data file (no parquet, no CSV); any label generation; any label regeneration; any v002 label-manifest field change; any v002 feature-manifest field change; any new horizon; any new symbol; any new family; any acquisition (no additional aggTrades, no mark-price, no spot, no cross-venue, no order-book); any test-split inspection; any threshold; any strategy; any signal; any PnL; any backtest; any model training; any model scoring; any prediction; any reusable split mask; any model binary; any row-level prediction; any manifest mutation; any successor-state mutation; any endpoint call; any credential; any `.env` / `.mcp.json` / MCP / Graphify.
- **Expected output if separately authorized later.** A docs-only candidate-framing memo enumerating, at design level, a small bounded menu of cost-commensurate label-shape candidates (direction-conditional-on-magnitude; magnitude-bin ordinal; residual-magnitude) with per-candidate purpose, evidence basis, allowed future inputs, forbidden future inputs, expected later artefact shape, failure / stop condition, and explicit non-strategy status. **No** label artefact, **no** label manifest, **no** label sidecar, **no** label gate report, **no** label successor-state, **no** acquisition artefact, **no** strategy artefact, **no** signal artefact, **no** PnL artefact, **no** backtest artefact, **no** test-split artefact.
- **Failure / stop condition.** Any of: (i) the future scoping memo would require recomputing any label statistic from local data; (ii) the future scoping memo would name an actual label-regeneration phase as recommended; (iii) the future scoping memo would propose a cost-commensurate label that requires acquisition beyond the locked 90-day v002 envelope; (iv) the future scoping memo would imply strategy / signal / PnL / backtest / threshold work; (v) the future scoping memo would propose a label change that requires a `chronological_split_policy` transition; (vi) the future scoping memo would propose a label change without first satisfying Phase 4bj-* eligibility-gate governance. If any of (i) – (vi) holds, the would-be successor must fail-closed.
- **Why C-B is not a strategy, signal, or trading edge.** C-B describes what a future label-design memo *might* be allowed to scope. It does not propose to trade on any threshold, magnitude bin, or residual-magnitude class. It explicitly preserves the project's no-rescue boundary: a cost-commensurate label is still a label, not a signal; converting any future label scheme into a tradable rule would require a separate strategy phase, a separate backtest phase, and separate operator authorization — none of which Phase 4bn-D authorizes.

---

### C-C — Horizon-envelope feasibility

- **Purpose.** Scope, at design level only, whether a future docs-only scoping memo could be permitted to *describe* whether 1s / 5s should remain deferred or be partially included for descriptive parity, or whether the 15s / 60s envelope should be widened by one additional horizon strictly for descriptive context — without generating new horizon labels, without acquisition, and without revising any retained verdict or project lock.
- **Evidence source from Phase 4bn-B / 4bn-C.** Phase 4bn-A §9 – §20 (1s / 5s deferred; latency / tradability sensitivity acknowledged). Phase 4bn-B implementation report (only 15s / 60s implemented). Phase 4bn-C §11 (15s lift is real; 60s lift collapses to ~1.5 pp). Phase 4bn-C §15 H3 (horizon-vs-cost mismatch). Phase 4bn-C §13 (cost-commensurability fractions per horizon: 6.2 % at 15s, 18.3 % at 60s; both descriptive context only). Phase 4bm-W diagnostic summary's envelope-terminal censoring asymmetry per horizon (1s 14 / 5s 39 / 15s 170 / 60s 634, all concentrated on the final envelope day inside the sealed test split).
- **Allowed future inputs (if separately authorized later).** The committed Markdown record of Phase 4bn-A / 4bn-B / 4bm-W / 4bn-C (no local data file opened); the v002 label manifest's horizon enumeration (referenced for description only; no field altered). The candidate scoping memo would describe a horizon-envelope question only at design level.
- **Forbidden future inputs.** Any local parquet or CSV; any new label generation; any new horizon kernel rerun; any new horizon manifest field; any acquisition (no new days, no new symbols, no new families, no longer-horizon labels, no barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels); any test-split inspection; any threshold; any strategy; any signal; any PnL; any backtest; any model training; any model scoring; any prediction; any reusable split mask; any model binary; any row-level prediction; any manifest mutation; any successor-state mutation; any endpoint call; any credential; any `.env` / `.mcp.json` / MCP / Graphify.
- **Expected output if separately authorized later.** A docs-only memo recording (at design level only) which horizon-envelope adjustments could be safely scoped, under what predeclared constraints, and with what stop conditions. **No** new horizon artefact, **no** new horizon label, **no** new horizon kernel, **no** strategy artefact, **no** signal artefact, **no** PnL artefact, **no** backtest artefact, **no** test-split artefact.
- **Failure / stop condition.** Any of: (i) the future scoping memo would require recomputing any horizon-conditional label statistic from local data; (ii) the future scoping memo would propose acquisition beyond the locked 90-day v002 envelope; (iii) the future scoping memo would propose a horizon change that requires a label kernel rerun; (iv) the future scoping memo would propose any horizon-conditional threshold or signal; (v) the future scoping memo would propose any horizon change that requires test-split inspection. If any of (i) – (v) holds, the would-be successor must fail-closed.
- **Why C-C is not a strategy, signal, or trading edge.** A horizon-envelope question is a *measurement-frame* question. Including more horizons descriptively does not constitute a trade rule. The fact that 60s carries better cost-commensurability than 15s but weaker model signal (Phase 4bn-C §13) is itself evidence that horizon choice is not the simple optimization a strategy memo would treat it as.

---

### C-D — Train-vs-validation feature drift diagnostics feasibility

- **Purpose.** Scope, at design level only, whether a future descriptive-only diagnostic memo could be permitted to evaluate train-vs-validation drift in the v002 feature distributions, in order to surface whether the train-only standardization fit (`transform_metadata.json`) is mis-applied to validation due to distributional shift. This addresses Phase 4bn-C §15 H10 (feature-stationarity drift) at design level only.
- **Evidence source from Phase 4bn-B / 4bn-C.** Phase 4bn-B implementation report (train-only mean / std fit; validation transform; Phase 4bm-W did not compute this drift). Phase 4bn-C §15 H10 (feature-stationarity drift). Phase 4bn-C §9 – §11 (the ~5 pp 15s lift and ~1.5 pp 60s lift could plausibly under-perform under unmeasured drift).
- **Allowed future inputs (if separately authorized later).** The same train + validation supervised splits used by Phase 4bn-B (no test); train-side fit statistics from `transform_metadata.json` (descriptive reference only); the same v002 feature surface; the same exclusion list; descriptive-only summary statistics (per-feature mean, std, quantile bands on train and validation; per-feature train-vs-validation delta and absolute delta; per-feature train-vs-validation distance metric chosen a priori, predeclared, not selected through results).
- **Forbidden future inputs.** The sealed test split; any test row; any new feature; any feature ranking; any feature selection; any feature pruning; any hyperparameter selection; any threshold; any probability-to-signal conversion; any model training; any model scoring; any reusable split mask; any model binary; any row-level prediction; any manifest mutation; any successor-state mutation; any acquisition; any endpoint call; any credential; any `.env` / `.mcp.json` / MCP / Graphify; any strategy / signal / PnL / backtest; any retained verdict revision; any project lock change.
- **Expected output if separately authorized later.** A descriptive-only local gitignored artefact set under `data/research/...` (never committed) containing per-feature train-vs-validation summary tables, a single per-feature drift metric (predeclared a priori), and a per-feature drift-vs-baseline table for the included features; canonical Phase 4bb-F sidecars for every output file. **No** feature ranked, **no** feature selected, **no** feature pruned, **no** feature engineered, **no** threshold tuned, **no** strategy artefact, **no** signal artefact, **no** PnL artefact, **no** backtest artefact, **no** test-split artefact, **no** model binary, **no** row-level prediction, **no** reusable split mask.
- **Failure / stop condition.** Any of: (i) the diagnostic would require inspecting test rows; (ii) the diagnostic would rank or select features; (iii) the diagnostic would propose a kernel rerun or any feature regeneration; (iv) the diagnostic would tune a threshold or convert a feature-drift score into a trade rule; (v) the diagnostic would mutate any manifest; (vi) the diagnostic would persist a model binary or row-level prediction. If any of (i) – (vi) holds, the would-be successor must fail-closed.
- **Why C-D is not a strategy, signal, or trading edge.** C-D would surface, at a measurement-frame level only, whether the v002 features are stationary enough between train and validation that the existing standardization is meaningful. It is a *quality assurance* descriptive question, not a strategy proposal. Even a large measured drift would not translate into a trade signal; it would only inform whether the H10 hypothesis can be ruled in or out as one of the candidate explanations for the weak baseline-vs-prior separation.

---

### C-E — Calibration-limited evaluation feasibility

- **Purpose.** Scope, at design level only, whether a future descriptive-only calibration memo could be permitted to extend the Phase 4bn-B 10-bin reliability summary into a per-class and per-horizon calibration table on validation only, without fitting any calibrator, without tuning any threshold, without converting any probability into a trade signal, and without touching the test split.
- **Evidence source from Phase 4bn-B / 4bn-C.** Phase 4bn-B `calibration_summary.csv` (10-bin reliability on max predicted probability). Phase 4bn-C §12 (dominant 0.5 – 0.6 bin well-calibrated; high-confidence tail severely over-confident with reliability gaps −0.061 to −0.392 in the 0.6 – 1.0 bins; persistence calibration degenerate by construction).
- **Allowed future inputs (if separately authorized later).** The validation supervised split used by Phase 4bn-B (no test); the existing L2 / L1 / majority / persistence predicted-probability outputs for validation only (the same outputs Phase 4bn-B already produced; no rerun); a fixed, predeclared bin scheme (the same 10-bin scheme Phase 4bn-B used, optionally with a per-class and per-horizon split applied descriptively); descriptive reliability gaps per bin per class per horizon on validation only; persistence's degenerate one-hot bucket called out explicitly as uncalibrated by construction.
- **Forbidden future inputs.** The sealed test split; any test row; any calibrator fit (no isotonic, no Platt, no histogram binning, no spline, no neural calibrator); any threshold; any probability-to-signal conversion; any cut-off, confidence band, or decision rule; any new feature; any feature ranking; any feature selection; any hyperparameter selection; any model training; any model scoring; any model binary persistence; any row-level prediction persistence; any reusable split mask; any manifest mutation; any successor-state mutation; any acquisition; any endpoint call; any credential; any `.env` / `.mcp.json` / MCP / Graphify; any strategy / signal / PnL / backtest; any retained verdict revision; any project lock change.
- **Expected output if separately authorized later.** A descriptive-only local gitignored artefact set under `data/research/...` (never committed) containing per-class per-horizon reliability tables on validation only, per-bin row counts, per-bin mean predicted probability, per-bin empirical accuracy, per-bin reliability gap, and a per-baseline summary; canonical Phase 4bb-F sidecars. **No** calibrator fitted, **no** threshold tuned, **no** strategy artefact, **no** signal artefact, **no** PnL artefact, **no** backtest artefact, **no** test-split artefact, **no** model binary, **no** row-level prediction, **no** reusable split mask.
- **Failure / stop condition.** Any of: (i) the memo would fit a calibrator; (ii) the memo would tune a threshold; (iii) the memo would convert any probability into a trade signal; (iv) the memo would inspect any test row; (v) the memo would propose a confidence cut; (vi) the memo would propose any decision rule. If any of (i) – (vi) holds, the would-be successor must fail-closed.
- **Why C-E is not a strategy, signal, or trading edge.** C-E would only extend an existing descriptive table. The Phase 4bn-C calibration evidence already establishes that high-confidence predictions are no better than chance, which means even a more granular calibration table would *not* be used to trade on confidence. C-E is a refinement of measurement, not a strategy proposal.

---

### C-F — Optional shallow non-linear baseline feasibility (only if memory and leakage controls can be bounded)

- **Purpose.** Scope, at design level only, whether a future docs-only / design-only memo could be permitted to *specify* a memory-bounded, depth-limited shallow tree baseline that would respect the Phase 4bn-A §15 boundary ("Optionally one shallow tree baseline only if complexity and leakage controls are explicitly bounded") and a streaming-safe memory profile, *without* actually training it. Phase 4bn-B intentionally fail-closed on memory and did not implement this baseline; C-F revisits whether the controls could be bounded enough to make a future *separately authorized* implementation phase safe.
- **Evidence source from Phase 4bn-B / 4bn-C.** Phase 4bn-A §15 (optional shallow tree authorized only if complexity and leakage controls are explicitly bounded; `BASELINE_SHALLOW_TREE_INCLUDED = False`). Phase 4bn-B implementation report (memory fail-closed; intentional non-implementation; recorded verbatim in the Phase 4bn-B merge-closeout). Phase 4bn-C §15 H5 / H7 (linear / logistic may be too simple; shallow tree excluded by memory fail-closed).
- **Allowed future inputs (if separately authorized later).** Predeclared fixed `max_depth` (e.g., a single value declared a priori, not chosen through validation results); predeclared chunked-or-sampled training shape that fail-closes on memory rather than implicitly downsampling for headline metrics; the same train + validation supervised splits used by Phase 4bn-B; the same v002 feature surface; the same exclusion list; the same train-only standardization (if applicable to the chosen tree implementation); the same locked split policy (`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`); the same canonical Phase 4bb-F sidecar policy for any descriptive output. The candidate memo would describe what a *separately authorized* implementation phase would be required to demonstrate in advance (fail-closed memory; predeclared depth; no leakage; no test access; no model selection through results).
- **Forbidden future inputs.** The sealed test split; any test row; any new feature; any feature ranking; any feature selection; any hyperparameter selection through validation; any depth chosen through validation; any threshold; any probability-to-signal conversion; any reusable split mask; any model binary persistence; any row-level prediction persistence; any manifest mutation; any successor-state mutation; any acquisition; any endpoint call; any credential; any `.env` / `.mcp.json` / MCP / Graphify; any strategy / signal / PnL / backtest; any retained verdict revision; any project lock change. **The future implementation must fail-closed on memory in the same way Phase 4bn-B did, rather than silently downsampling for headline metrics.**
- **Expected output if separately authorized later (two stages).** Stage 1 (docs-only design memo): a single specification document recording the predeclared `max_depth`, chunked / sampled training shape, fail-closed memory rule, leakage-control proof obligations, expected descriptive outputs, allowed inputs, forbidden inputs, failure / stop conditions, and explicit non-strategy status. **No** training. **No** scoring. **No** prediction. **No** test access. Stage 2 (separately authorized implementation phase, *not* implied by Stage 1): a descriptive-only local gitignored artefact set under `data/research/...` containing per-class precision / recall / F1, macro-F1, balanced accuracy, mean log-loss, mean Brier, and confusion matrices for the shallow tree variant on train and validation only; canonical Phase 4bb-F sidecars; a memory-trace recording that fail-closes if exceeded. **No** model binary persisted. **No** row-level prediction persisted. **No** reusable split mask persisted. **No** test row touched. **No** threshold tuned. **No** feature ranked or selected. **No** strategy artefact, **no** signal artefact, **no** PnL artefact, **no** backtest artefact. The two stages are explicitly separate authorizations; Stage 1 does not authorize Stage 2.
- **Failure / stop condition.** Any of: (i) the bounded-memory profile cannot be specified up-front (e.g., the tree implementation chosen requires loading all rows in memory); (ii) the depth would have to be selected through validation results; (iii) the implementation would persist a model binary or row-level prediction; (iv) the implementation would touch any test row; (v) the implementation would propose a threshold or a probability-to-signal conversion; (vi) the leakage-control proof cannot be made explicit (e.g., the chosen tree implementation cannot guarantee that no label-derived information leaks into the feature matrix); (vii) the implementation cannot fit within the same compute envelope as Phase 4bn-B without silently downsampling for headline metrics. If any of (i) – (vii) holds, the would-be successor must fail-closed at the design stage and may not advance to an implementation stage.
- **Why C-F is not a strategy, signal, or trading edge.** Even a successful shallow-tree baseline would still face the same calibration evidence (Phase 4bn-C §12) and the same cost-commensurability context (Phase 4bn-C §13). The most-confident predictions of a more flexible model could still be no better than chance; the 80 – 95 % of validation rows with sub-cost absolute moves would still dominate; and the test holdout would still be sealed. C-F is a *measurement* question about whether linearity is the binding constraint on the existing un-weighted multinomial softmax baseline, not a strategy proposal.

---

### Summary table — candidate-level non-authorizations

| Candidate | Trains a model? | Scores a model? | Generates predictions? | Touches test? | Mutates a manifest? | Persists a model binary or row-level prediction? | Authorizes a successor? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-A — Class weighting | No | No | No | No | No | No | No |
| C-B — Cost-commensurate label framing | No | No | No | No | No | No | No |
| C-C — Horizon-envelope | No | No | No | No | No | No | No |
| C-D — Train-vs-validation feature drift diagnostics | No | No | No | No | No | No | No |
| C-E — Calibration-limited evaluation | No | No | No | No | No | No | No |
| C-F — Optional shallow non-linear baseline | No | No | No | No | No | No | No |

Every entry above is **No** for Phase 4bn-D itself. Each candidate is described at design level only by this memo; nothing in §10 authorizes any execution. A future implementation phase that would actually execute any of C-A / C-D / C-E / C-F (or the design stage of C-B / C-C / C-F-Stage-1) requires a **separately authorized** Tier 1 phase with its own authorization prompt, branch, implementation report, closeout, separate merge phase, and merge-closeout. **Phase 4bn-D authorizes none of them.**

## 11. Required controls for any future expansion

Any future ML-baseline expansion phase, if separately authorized, must honour every control below. Phase 4bn-D records these as prospective controls only; it does not authorize any phase to invoke them.

1. **Test holdout sealed.** No test row may be loaded into any supervised stream. The Phase 4bn-B `iter_partitions(split="test", ...)` raise must remain in force, and the corresponding test must continue to pass.
2. **No model selection through results.** Any hyperparameter, weight, depth, or threshold must be predeclared a priori in the authorization prompt and the implementation report; validation results may not be used to choose among candidate values.
3. **No feature ranking or selection.** The v002 feature surface is the input; no feature may be ranked, pruned, engineered, or selected by validation results.
4. **No threshold tuning, no probability-to-signal conversion.** The Phase 4bn-C calibration evidence (over-confident high-confidence tail) explicitly forbids the obvious "trade only when confident" follow-up; the same forbiddance applies to every future ML-baseline expansion successor.
5. **No model binary persistence, no row-level prediction persistence, no reusable split mask persistence.** Only descriptive summary artefacts may be produced. Predictions used to compute calibration tables must be aggregated in flight; row-level predictions may not be persisted to disk.
6. **Memory and leakage controls must be predeclared, not discovered.** Any candidate that cannot specify a fail-closed memory profile up front must not progress beyond the design stage. Any candidate whose leakage controls cannot be proven up front must not progress beyond the design stage.
7. **Strict gitignore coverage.** All ML-baseline expansion outputs must live under `data/research/microstructure/ml-baselines/...` (gitignored under `.gitignore:88: data/research/`); none may be committed.
8. **Canonical Phase 4bb-F sidecar policy.** Every descriptive output file must be paired with a canonical Phase 4bb-F sidecar (two-space separator between SHA and basename; LF line ending; no BOM; no extra tokens).
9. **No manifest transition.** The v002 label manifest's `research_eligible = false`, `eligibility_gate_status = "pending"`, `chronological_split_policy = "not_yet_defined"`, `label_family_research_use_authorized = false`, `stage_5_label_cleared = false`, `diagnostics_authorized = false`, and equivalent flags on the v002 feature manifest, must remain unchanged.
10. **No successor-state mutation.** The Phase 4bm-S, Phase 4bm-U, Phase 4bm-Q artefacts and any future ML-arc successor-state artefact must be byte-identical before and after any expansion run.
11. **No retained verdict revision, no project lock change.** §11.6 = 8 bps per side / 16 bps round trip; §1.7.3 risk / leverage / position / stop rules; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k / 4p / 4q / 4v / 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant; Phase 4bb-F canonical sidecar / path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard — all preserved verbatim under every future ML-baseline expansion.
12. **No acquisition.** The locked 90-day v002 envelope is the binding data surface; no additional days / symbols / families / horizons / mark-price / spot / cross-venue / order-book / longer-horizon / barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels may be acquired or generated.
13. **No endpoint or credential.** No public, authenticated, or private endpoint call; no WebSocket or user stream; no credential, `.env`, `.mcp.json`, MCP, or Graphify use under any expansion phase.
14. **Per-candidate strict non-scope.** Every future expansion phase must enumerate, in its authorization prompt, the per-candidate forbidden inputs from §10 verbatim; any silent broadening of scope is a fail-closed condition.

These controls are prospective only; they bind any *future* phase. Phase 4bn-D itself trains nothing, scores nothing, runs nothing, and authorizes nothing.

## 12. Future artefact boundary, if separately authorized

If a future bounded ML-baseline expansion implementation phase is separately authorized later, every output it produces must live under `data/research/microstructure/ml-baselines/phase-{successor-name}/` and be paired with a canonical Phase 4bb-F sidecar. No output may be committed. No output may be tracked. `git check-ignore -v` must confirm gitignore coverage at `.gitignore:88: data/research/` for every output path.

Specifically, a future expansion implementation phase must NOT produce, or be construed to produce:

- a committed parquet, CSV, or JSON under `data/research/microstructure/`;
- a committed manifest, sidecar, gate report, or successor-state file under `data/microstructure/`;
- a model binary anywhere on disk;
- a row-level prediction file anywhere on disk;
- a reusable split mask file anywhere on disk;
- a tracked or local file that records test-split metrics;
- a tracked or local file that records a tuned threshold or a probability-to-signal conversion;
- a tracked or local file that records a feature ranking or feature selection;
- a tracked or local file that records strategy / signal / PnL / backtest output;
- a tracked or local file that mutates any manifest field, successor-state field, gate-report field, or governance label.

Any future expansion implementation phase may produce only descriptive-summary CSV / JSON artefacts (such as per-class P / R / F1, macro-F1, balanced accuracy, mean log-loss, mean Brier, confusion matrices, calibration tables, drift summaries, cost-commensurability fractions) on supervised splits only, with the test split sealed. Every artefact must be re-derivable from the locked v002 inputs without any new acquisition.

## 13. Future validation boundary, if separately authorized

If a future bounded ML-baseline expansion implementation phase is separately authorized later, its validation must satisfy:

- `ruff check .` clean (or scoped to the new surface and explicitly justified if not full-repo).
- Scoped pytest pass for any new test surface (e.g., `pytest tests/research/microstructure/test_ml_baseline_expansion_*.py`).
- Whole-repo pytest: pre-existing failures classified explicitly and not introduced by the expansion.
- `mypy src` baseline preserved or improved (with explicit categorization of any new errors against the existing baseline; no claim of full strict mypy clean is required, consistent with Phase 4bn-B's reporting).
- `git diff --check` clean.
- `git check-ignore -v` confirmation for every new local output path under `data/research/...`.
- Re-hash of every Phase 4bn-A / Phase 4bn-B / Phase 4bm-* governed artefact pre/post implementation: all IDENTICAL.
- Re-hash of the v002 label and feature manifests pre/post: IDENTICAL.
- `iter_partitions(split="test", ...)` raise test continues to pass.
- Explicit non-authorization block (per §3 / §7 / §11 of this memo) in the implementation report and closeout.

Phase 4bn-D records these prospective controls as the validation envelope a future expansion implementation phase would have to satisfy. Phase 4bn-D itself runs none of them as code; the validation Phase 4bn-D runs is the docs-only validation enumerated in the authorization prompt.

## 14. Stop conditions

A future bounded ML-baseline expansion implementation phase, if separately authorized later, must fail-closed (return `FAIL_CLOSED` per the operator-report standard) if any of the following hold:

- the predecessor merge-closeout (this Phase 4bn-D, or whichever predecessor is named) is absent from `main` or its SHA does not match the authorization-prompt expectation;
- `git rev-parse main != git rev-parse origin/main`;
- the Phase 4bn-A / Phase 4bn-B / Phase 4bn-C SHAs are not ancestors of `main`;
- any v002 label or feature manifest sidecar fails canonical Phase 4bb-F verification (CRLF, BOM, extra fields, embedded-SHA mismatch);
- the test split would be loaded into any supervised stream;
- a hyperparameter, weight, depth, or threshold cannot be predeclared up-front;
- a model binary or row-level prediction would be persisted;
- a reusable split mask would be persisted;
- a feature would be ranked, selected, or engineered through validation results;
- a threshold or probability-to-signal conversion would be introduced;
- any manifest field, successor-state field, gate-report field, or governance label would be mutated;
- any acquisition would be attempted (additional days / symbols / families / horizons / mark-price / spot / cross-venue / order-book / barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels);
- any public, authenticated, or private endpoint call would be made;
- any credential, `.env`, `.mcp.json`, MCP, or Graphify would be used;
- the implementation cannot specify its memory profile up-front and fail-closes only after silent downsampling;
- any retained verdict (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1, C1, 5m thread) would be revised;
- any project lock (§11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k / 4p / 4q / 4v / 4w, Phase 4ak M0, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)` always-raises invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + standing CRLF rule + reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard) would be loosened;
- ambiguity in scope prevents safe execution and the prompt does not allow pausing.

A failure of any of the above means the would-be successor must stop, record the failure, and not advance to commit or merge. Phase 4bn-D records these stop conditions as the safety envelope that any successor must inherit.

## 15. Decision

**`RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Rationale (anchored to §5 – §13).

1. **Phase 4bn-C's `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` is the immediate predecessor recommendation, and Phase 4bn-D is exactly the docs-only / design-only / scoping-only successor that recommendation made conditionally allowable.** Phase 4bn-D's purpose is to *evaluate* whether a bounded successor expansion phase can be safely scoped, not to authorize it. The Phase 4bn-D scoping work demonstrates that at least three candidate paths (C-A class weighting, C-D feature-drift diagnostics, C-E calibration-limited evaluation) are amenable to a strictly bounded, descriptive-only, test-sealed implementation that would not require any change to retained verdicts, project locks, manifest state, successor-state artefacts, gate reports, or acquisition envelope, and that would not require strategy / signals / PnL / backtests.
2. **A subset of the candidate menu is design-stage only.** C-B (cost-commensurate label framing) and C-C (horizon-envelope) are scoping-stage questions only; they require no execution, no kernel rerun, no acquisition. C-F (optional shallow non-linear baseline) is a two-stage candidate where Stage 1 is a design-level specification memo and Stage 2 (if separately authorized later) would be an implementation phase under bounded memory / leakage controls. Phase 4bn-D does not authorize Stage 2 of C-F.
3. **The Phase 4bn-C calibration evidence (over-confident high-confidence tail) explicitly forecloses the obvious "threshold-tune for confidence" follow-up; any successor must honour this.** Section 10 records the explicit forbiddance per candidate; section 11 records the forbiddance as a global control; section 14 records it as a stop condition.
4. **The §11.6 cost-commensurability evidence (80 – 95 % of validation rows below the round-trip cost) explicitly forecloses any framing of these candidates as strategy proposals.** Every candidate above is descriptive measurement, not edge.
5. **Recommending "remain paused" (Phase 4bn-C option 1) would over-claim confidence in the negative direction.** The Phase 4bn-C interpretation explicitly noted that the 15s lift is reproducible with controlled stability deltas, and the bounded candidate menu in §10 is amenable to descriptive-only follow-up without crossing any of the project's safety boundaries.
6. **Recommending a stop-work verdict on the v002 family (Phase 4bn-C option 5) would also over-claim confidence in the negative direction.** No stop-work-level negative evidence has been produced.
7. **Phase 4bn-D is recommendation-only.** The successor it identifies is a possible future docs-only / design-only / scoping-only or descriptive-only implementation phase, *not* a strategy phase, *not* a model-selection phase, *not* a threshold-tuning phase, *not* an acquisition phase, *not* a manifest-mutation phase, *not* a paper / shadow / live-readiness / deployment / exchange-write / production-key phase. **The successor is not authorized by Phase 4bn-D.** A separate operator authorization is required.

## 16. Successor recommendation, if any

**Conditional next, NOT authorized: Phase 4bn-E — a bounded ML-baseline expansion implementation phase, scoped to *one* of the §10 candidates (C-A class weighting, C-D train-vs-validation feature drift diagnostics, or C-E calibration-limited evaluation), selected by separate operator authorization.**

Phase 4bn-E (provisional name; *not* authorized by Phase 4bn-D) would, if separately authorized later:

- be Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (because it touches ML and is adjacent to downstream admissibility decisions);
- name exactly one of {C-A, C-D, C-E} as its scope and explicitly defer the other two until separately authorized;
- inherit every §11 control, every §13 validation gate, and every §14 stop condition verbatim;
- run no model whose result is used to select among candidate hyperparameters, weights, depths, thresholds, or features;
- keep the test holdout sealed;
- persist no model binary, no row-level prediction, no reusable split mask;
- not mutate any manifest, successor-state artefact, gate report, or governance label;
- not authorize any further successor by itself.

Alternatively (also *not* authorized by Phase 4bn-D), the operator may choose:

- **Phase 4bn-E-B (scoping-only)** — a docs-only / design-only memo enumerating C-B candidate cost-commensurate label framings at design level (no label generation, no acquisition);
- **Phase 4bn-E-C (scoping-only)** — a docs-only / design-only memo enumerating C-C horizon-envelope questions at design level (no kernel rerun, no acquisition);
- **Phase 4bn-E-F-stage-1 (scoping-only)** — a docs-only / design-only memo specifying the C-F shallow-tree bounded-memory profile (no training).

Or:

- **remain paused** — no successor authorized; the ML arc is recorded as having reached an evidence boundary; later operator decisions remain open.

Or:

- **reject the successor and close the ML arc** — record a verdict that the v002 ML-baseline family is operationally closed for further bounded expansion under current evidence; preserve all Phase 4bn-A / 4bn-B / 4bn-C artefacts as research evidence; preserve every retained verdict and project lock; no successor authorized.

**Phase 4bn-D's recommendation is the conditional Phase 4bn-E option above** (a bounded implementation phase, scoped to one candidate from {C-A, C-D, C-E}, subject to separate operator authorization). The "remain paused" and "reject successor" options remain valid operator choices; Phase 4bn-D does not foreclose them.

## 17. Explicit non-authorizations

Phase 4bn-D is docs-only / design-only / scoping-only and authorizes **nothing executable**. It does not, and cannot, authorize:

- any ML training, model scoring, prediction generation, feature ranking, feature selection, feature pruning, model selection through results, hyperparameter tuning, threshold tuning, meta-labeling, ensemble construction, or calibrator fitting;
- any strategy research, strategy design, signal generation, trade-signal generation, PnL simulation, equity-curve construction, Sharpe / Sortino / drawdown / hit-rate / trade-PnL metrics, backtests, or walk-forward optimization;
- any use of the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, threshold selection, reporting, or inspection;
- any diagnostics rerun, diagnostic artefact creation, ML artefact creation, reusable split-mask materialization, row-level prediction persistence, or model-binary persistence;
- any data acquisition (no additional days / symbols / families beyond the locked 90-day v002 envelope; no mark-price / spot / cross-venue / order-book / additional aggTrades; no longer-horizon labels; no barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels);
- any public / authenticated / private endpoint call; any WebSocket / user stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- any manifest mutation, successor-state mutation, gate-report mutation, or change to `research_eligible`, `eligibility_gate_status`, `chronological_split_policy`, `diagnostics_authorized`, or `ml_authorized` on any on-disk manifest;
- any source / test / committed-script / config / `.gitignore` / `pyproject.toml` / `README.md` / MCP-file modification;
- any commit under `data/microstructure/` or `data/research/`;
- Phase 4bn-E or any successor phase (under any name) performing bounded ML-baseline expansion implementation, label / target rework implementation, class-imbalance / regime-conditioning implementation, calibration-only-analysis implementation, or any other Phase 4bn-* / Phase 4bo-* / Phase 4bp-* successor;
- Phase 5; Phase 4 canonical; paper / shadow; live-readiness; deployment; exchange-write; production-key creation;
- any revision of a retained verdict, any loosening of a project lock, or any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bn-D is a docs-only / design-only / scoping-only bounded ML-baseline expansion scoping memo.** **Phase 4bn-D does not train ML models.** **Phase 4bn-D does not run ML.** **Phase 4bn-D does not score models.** **Phase 4bn-D does not generate predictions.** **Phase 4bn-D does not generate reusable split masks.** **Phase 4bn-D does not persist model binaries.** **Phase 4bn-D does not persist row-level predictions.** **Phase 4bn-D does not read, inspect, evaluate, or report any test-holdout metric.** **Phase 4bn-D does not use the sealed test split.** **Phase 4bn-D does not select models through results.** **Phase 4bn-D does not rank features.** **Phase 4bn-D does not select features.** **Phase 4bn-D does not tune hyperparameters.** **Phase 4bn-D does not tune thresholds.** **Phase 4bn-D does not run strategy research.** **Phase 4bn-D does not define a strategy.** **Phase 4bn-D does not generate trade signals.** **Phase 4bn-D does not simulate PnL.** **Phase 4bn-D does not run backtests.** **Phase 4bn-D does not run diagnostics.** **Phase 4bn-D does not rerun Phase 4bn-B.** **Phase 4bn-D does not acquire data.** **Phase 4bn-D does not call any public, authenticated, or private endpoint.** **Phase 4bn-D does not open any WebSocket or user stream.** **Phase 4bn-D does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.** **Phase 4bn-D does not mutate any manifest.** **Phase 4bn-D does not mutate any successor-state artefact.** **Phase 4bn-D does not commit `data/microstructure`.** **Phase 4bn-D does not commit `data/research`.** **Phase 4bn-D does not authorize Phase 4bn-E, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, or any successor phase.**

## 18. Current-project-state update summary

The narrow `docs/00-meta/current-project-state.md` update made by Phase 4bn-D consists of:

- a new Phase 4bn-D paragraph appended immediately after the Phase 4bn-C paragraph;
- a new Current-phase block for Phase 4bn-D inserted immediately after the new Phase 4bn-D paragraph and immediately before the existing Phase 4bn-C Current-phase block;
- preservation of every earlier paragraph (Phase 4a .. Phase 4bn-C) and every earlier Current-phase block (Phase 4bn-C, Phase 4bn-B, and older blocks) as labelled historical context;
- recording of Phase 4bn-D as **branch-complete only, not merged, not project-complete**;
- recording of the Phase 4bn-D decision `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
- recording of the exact non-authorizations (per §0 / §3 / §7 / §17 of this memo);
- recording of the recommended state (**remain paused**);
- explicit statement that a Phase 4bn-E successor is recommended but **not authorized** by Phase 4bn-D.

No other section of `docs/00-meta/current-project-state.md` is modified by Phase 4bn-D. No retained verdict, project lock, manifest field, successor-state field, gate-report field, or governance label is changed. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked by Phase 4bn-D).

## 19. Retained verdicts preserved

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

All prior phase results (Phase 4am .. Phase 4bn-C) preserved verbatim.

## 20. Project locks preserved

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max / mark-price stops
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k / 4p / 4q / 4v / 4w methodology + strategy-spec locks
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bn-D)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

## 21. Recommended next state

**Remain paused.** Phase 4bn-D is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The scoping decision `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION` is a recommendation only and authorizes nothing. **Phase 4bn-E is not authorized by Phase 4bn-D.** **Any bounded ML-baseline expansion implementation phase requires a separately authorized phase.** **Recommended state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-E bounded ML-baseline expansion implementation phase scoped to one of {C-A class weighting, C-D train-vs-validation feature drift diagnostics, C-E calibration-limited evaluation} is the cleanest non-paused option. It would respect every §11 control, every §13 validation gate, and every §14 stop condition, and would keep the test holdout sealed. Phase 4bn-E is **not authorized** by this memo. The operator may equivalently choose to remain paused or to reject the successor and close the ML arc; Phase 4bn-D does not foreclose either alternative.
