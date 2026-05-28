# Phase 4bn-B — Closeout

**Phase 4bn-B is the multi-day v002 ML-baseline implementation phase.** **Phase 4bn-B implements exactly the Phase 4bn-A design and nothing beyond it.** **Phase 4bn-B trains and evaluates baselines on train and validation only.** **Phase 4bn-B does not use the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, or reporting metrics.** **Phase 4bn-B does not select any model as "best".** **Phase 4bn-B does not rank or select features.** **Phase 4bn-B does not tune hyperparameters.** **Phase 4bn-B does not tune thresholds.** **Phase 4bn-B does not define or run any strategy.** **Phase 4bn-B does not generate trade signals.** **Phase 4bn-B does not simulate PnL.** **Phase 4bn-B does not run backtests.** **Phase 4bn-B does not authorize acquisition.** **Phase 4bn-B does not call any public, authenticated, or private endpoint.** **Phase 4bn-B does not open any WebSocket or user stream.** **Phase 4bn-B does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.** **Phase 4bn-B does not mutate any manifest.** **Phase 4bn-B does not mutate any successor-state artefact.** **Phase 4bn-B does not commit data/microstructure.** **Phase 4bn-B does not commit data/research.** **Phase 4bn-B does not persist model binaries.** **Phase 4bn-B does not persist row-level predictions.** **Phase 4bn-B does not create reusable split masks.** **Phase 4bn-B does not authorize Phase 4bn-C, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.** **Recommended state remains paused.**

## 1. Phase identity

Phase 4bn-B — Multi-Day V002 ML-Baseline Implementation. **Branch-complete only.** Not merged into `main`; not project-complete. A separately authorized Tier 1 merge phase is required for project completion per `docs/00-meta/process/merge-closeout-standard.md`.

## 2. Lifecycle status

Branch-complete only. **Not project-complete.** No successor phase is authorized.

## 3. Branch name

`phase-4bn-b/multi-day-v002-ml-baseline-implementation`

## 4. Base SHA

`5b938b4ae5986874d0f7c3de6122df180c74790a` (Phase 4bn-A SHA-finalization commit `docs(phase-4bn-a): finalize merge closeout shas`; `main == origin/main` verified at branch time). Predecessor Phase 4bn-A docs (`2026-05-27_phase-4bn-a_ml-baseline-implementation-scoping-design.md`, `2026-05-27_phase-4bn-a_closeout.md`, `2026-05-27_phase-4bn-a_merge-closeout.md`) present on `main` and read in full before any Phase 4bn-B work began.

## 5. Commits created

- Implementation commit: `feat(phase-4bn-b): implement multi-day v002 ml baseline` — captured in the final operator report and `git log`.

## 6. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. This phase implements the first ML-baseline execution over the multi-day v002 feature/label family. Adjacent to ML training, model scoring, prediction generation, feature/model selection, threshold tuning, strategy research, backtests, and test-holdout misuse.

## 7. Files changed

Source (tracked, new):

- `src/prometheus/research/microstructure/ml_baseline_design_v002.py`
- `src/prometheus/research/microstructure/ml_baseline_dataset_v002.py`
- `src/prometheus/research/microstructure/ml_baseline_models_v002.py`
- `src/prometheus/research/microstructure/ml_baseline_metrics_v002.py`
- `src/prometheus/research/microstructure/ml_baseline_report_v002.py`

The package `__init__.py` was deliberately NOT modified.

Script (tracked, new):

- `scripts/phase4bn_b_run_ml_baseline_v002.py`

Tests (tracked, new):

- `tests/research/microstructure/test_ml_baseline_dataset_v002.py`
- `tests/research/microstructure/test_ml_baseline_split_policy_v002.py`
- `tests/research/microstructure/test_ml_baseline_no_leakage_v002.py`
- `tests/research/microstructure/test_ml_baseline_no_network.py`
- `tests/research/microstructure/test_ml_baseline_outputs_v002.py`
- `tests/research/microstructure/test_ml_baseline_models_v002.py`
- `tests/research/microstructure/test_ml_baseline_metrics_v002.py`

Docs (tracked, new):

- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_multi-day-v002-ml-baseline-implementation.md`
- `docs/00-meta/implementation-reports/2026-05-28_phase-4bn-b_closeout.md` (this file)

Docs (tracked, narrow update):

- `docs/00-meta/current-project-state.md` (narrow Phase 4bn-B paragraph + new "Current phase:" block; prior Phase 4bn-A block preserved as historical context)

**Not modified:** `pyproject.toml`, `README.md`, `.gitignore`, MCP files, manifests, sidecars, gate reports, successor-state artefacts, all existing source files, all existing tests, all existing scripts, all `data/microstructure/` parquets and sidecars, and all `data/research/` artefacts produced by prior phases.

## 8. Local artefacts created and confirmed gitignored

Seven local gitignored ML-baseline output artefacts plus their canonical Phase 4bb-F sidecars under `data/research/microstructure/ml-baselines/phase-4bn-b/`:

- `ml_baseline_run_manifest.json` (+ `.sha256`)
- `per_horizon_model_summary.json` (+ `.sha256`)
- `metrics_train_validation.csv` (+ `.sha256`)
- `calibration_summary.csv` (+ `.sha256`)
- `class_balance_summary.csv` (+ `.sha256`)
- `feature_schema_used.json` (+ `.sha256`)
- `transform_metadata.json` (+ `.sha256`)

Each output is paired with its canonical Phase 4bb-F sidecar (`<sha256_lowercase_hex>  <basename>\n`; two ASCII spaces; LF only; no CRLF; no BOM; no extra fields). `git check-ignore -v` confirms `.gitignore:88: data/research/` covers every Phase 4bn-B output file. None is staged or committed.

**Model binaries are NOT persisted.** **Row-level predictions are NOT persisted.** **Reusable split masks are NOT persisted.**

## 9. Validation summary

- `ruff check .` — **all checks passed** on the full repo.
- `mypy src` — Phase 4bn-B's pure-numpy modules add the same `[type-arg]` / `[no-any-return]` numpy / pyarrow stub annotations that the existing v002 modules already exhibit; the error categories are the existing baseline, not new categories.
- `pytest tests/research/microstructure/test_ml_baseline_*.py` — **58 passed**, 0 failed.
- Full repo `pytest` — 2376 passed, 1 skipped, 2 pre-existing failures (`test_engine_d1a_dispatch.py` subprocess tests; verified identical pre-existing failures on `main` immediately before branch creation; unrelated to Phase 4bn-B).
- `git diff --check` — clean.
- `git check-ignore -v` — confirms all local outputs gitignored under `.gitignore:88: data/research/`.

## 10. Preserved governance / non-authorizations

- N-ACQUISITION: no data acquisition.
- N-ENDPOINT: no public / authenticated / private endpoint call; no WebSocket / user stream.
- N-CREDENTIALS: no `.env`, `.mcp.json`, MCP, Graphify, or credential use.
- N-MANIFEST: no manifest mutation (v002 label `5e17074d…`, v002 feature `512a0a54…` byte-identical pre/post).
- N-GATE-RERUN: no gate rerun; no new gate report.
- N-SUCCESSOR-STATE: no successor-state mutation.
- N-DERIVATION: no new features / labels / normalized rows / raw rows derived.
- N-DIAGNOSTICS-ML-STRATEGY: only the Phase 4bn-A-defined ML-baseline implementation was performed; no strategy / signals / PnL / backtest / feature ranking / model selection / threshold tuning / hyperparameter search occurred.
- N-PHASE-5: no Phase 5 / Phase 4 canonical / paper / shadow / live-readiness / deployment / production-key / exchange-write.
- N-VERDICT-LOCK: no retained verdict revised; no project lock loosened.

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## 11. Retained verdicts preserved

H0 — FRAMEWORK ANCHOR; R3 — BASELINE-OF-RECORD; R1a — RETAINED — NON-LEADING; R1b-narrow — RETAINED — NON-LEADING; R2 — FAILED — §11.6; F1 — HARD REJECT; D1-A — MECHANISM PASS / FRAMEWORK FAIL — other; 5m thread — OPERATIONALLY CLOSED (per Phase 3t); V2 — HARD REJECT — terminal for V2 first-spec; G1 — HARD REJECT — terminal for G1 first-spec; C1 — HARD REJECT — terminal for C1 first-spec. All prior phase results (Phase 4am .. Phase 4bn-A) preserved verbatim.

## 12. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant; Phase 4bb-F canonical sidecar / path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard. All preserved verbatim.

## 13. No successor authorization

Phase 4bn-B authorizes **no successor phase**. Phase 4bn-C, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, additional acquisition, additional feature engineering, additional label engineering, additional gate runs, feature ranking, model selection through results, hyperparameter tuning, threshold tuning, strategy / signals / PnL / backtest / walk-forward — **all remain unauthorized**.

## 14. Operator handoff notes

- The Phase 4bn-B branch is complete; the commit is on the branch (not on `main`).
- A separately authorized Tier 1 **merge phase** is required to record the merge into `main` and write the paired `merge-closeout` doc, per `docs/00-meta/process/merge-closeout-standard.md`.
- The seven gitignored output artefacts are present locally and are the authoritative descriptive evidence for the run. They are **not** committed and **must not** be committed.
- The descriptive ML evaluation is a research-eligibility datapoint, **not** an edge / profitability / strategy / tradability / live-readiness signal. Operator review should focus on whether the leakage controls were honoured (yes: train-only fit; sealed test; per-horizon censoring; embargo) and on whether anything in the metrics warrants a separately authorized follow-up (no, with the current settings — no baseline meaningfully separates from the majority-class prior; this is consistent with Phase 4bm-Z's caveats).
- **Recommended state remains paused.**

## 15. Required exact phrases

- Phase 4bn-B is the multi-day v002 ML-baseline implementation phase.
- Phase 4bn-B implements exactly the Phase 4bn-A design and nothing beyond it.
- Phase 4bn-B trains and evaluates baselines on train and validation only.
- Phase 4bn-B does not use the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, or reporting metrics.
- Phase 4bn-B does not select any model as "best".
- Phase 4bn-B does not rank or select features.
- Phase 4bn-B does not tune hyperparameters.
- Phase 4bn-B does not tune thresholds.
- Phase 4bn-B does not define or run any strategy.
- Phase 4bn-B does not generate trade signals.
- Phase 4bn-B does not simulate PnL.
- Phase 4bn-B does not run backtests.
- Phase 4bn-B does not authorize acquisition.
- Phase 4bn-B does not call any public, authenticated, or private endpoint.
- Phase 4bn-B does not open any WebSocket or user stream.
- Phase 4bn-B does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.
- Phase 4bn-B does not mutate any manifest.
- Phase 4bn-B does not mutate any successor-state artefact.
- Phase 4bn-B does not commit data/microstructure.
- Phase 4bn-B does not commit data/research.
- Phase 4bn-B does not persist model binaries.
- Phase 4bn-B does not persist row-level predictions.
- Phase 4bn-B does not create reusable split masks.
- Phase 4bn-B does not authorize Phase 4bn-C, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, or any successor phase.
- Recommended state remains paused.
