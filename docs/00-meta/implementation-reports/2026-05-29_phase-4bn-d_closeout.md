# Phase 4bn-D — Closeout

**Phase 4bn-D is a docs-only / design-only / scoping-only bounded ML-baseline expansion scoping memo.** **Phase 4bn-D does not train ML models.** **Phase 4bn-D does not run ML.** **Phase 4bn-D does not score models.** **Phase 4bn-D does not generate predictions.** **Phase 4bn-D does not generate reusable split masks.** **Phase 4bn-D does not persist model binaries.** **Phase 4bn-D does not persist row-level predictions.** **Phase 4bn-D does not read, inspect, evaluate, or report any test-holdout metric.** **Phase 4bn-D does not use the sealed test split.** **Phase 4bn-D does not select models through results.** **Phase 4bn-D does not rank features.** **Phase 4bn-D does not select features.** **Phase 4bn-D does not tune hyperparameters.** **Phase 4bn-D does not tune thresholds.** **Phase 4bn-D does not run strategy research.** **Phase 4bn-D does not define a strategy.** **Phase 4bn-D does not generate trade signals.** **Phase 4bn-D does not simulate PnL.** **Phase 4bn-D does not run backtests.** **Phase 4bn-D does not run diagnostics.** **Phase 4bn-D does not rerun Phase 4bn-B.** **Phase 4bn-D does not acquire data.** **Phase 4bn-D does not call any public, authenticated, or private endpoint.** **Phase 4bn-D does not open any WebSocket or user stream.** **Phase 4bn-D does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.** **Phase 4bn-D does not mutate any manifest.** **Phase 4bn-D does not mutate any successor-state artefact.** **Phase 4bn-D does not commit `data/microstructure`.** **Phase 4bn-D does not commit `data/research`.** **Phase 4bn-D does not authorize Phase 4bn-E, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, or any successor phase.** **Recommended state remains paused.**

## 1. Phase identity

Phase 4bn-D — Multi-Day V002 Bounded ML-Baseline Expansion Scoping Memo. Docs-only / design-only / scoping-only governance memo. Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. **Branch-complete only.** Not merged into `main`; not project-complete. A separately authorized Tier 1 merge phase is required for project completion per `docs/00-meta/process/merge-closeout-standard.md`.

## 2. Branch name

`phase-4bn-d/bounded-ml-baseline-expansion-scoping`

## 3. Base SHA

`e1dc2fa4570baccfc9e4a866899ca6c98fa03c66` (Phase 4bn-C SHA-finalization commit `docs(phase-4bn-c): finalize merge closeout shas`; `main == origin/main` verified at branch time). Phase 4bn-C merge commit `cf6172f4468d3ae28d91a0b3f016a00ba5d9159a` and merge-closeout commit `7fca0d538418293fe9b556a8aa67c26ad6165f52` present on `main`.

## 4. Commit SHA

- Docs commit: recorded by the single commit that adds this closeout + the scoping memo + the narrow `current-project-state.md` block (`docs(phase-4bn-d): scope bounded ml-baseline expansion`); the commit SHA is captured in the final operator report and `git log`.

## 5. Risk tier

**Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. Phase 4bn-D scopes the design surface for a possible future ML-baseline expansion implementation phase and is adjacent to ML execution, model selection, feature selection, hyperparameter tuning, threshold tuning, strategy research, backtests, label / target rework, and test-holdout misuse while explicitly authorizing none of them.

## 6. Files changed

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_bounded-ml-baseline-expansion-scoping.md` (new — the scoping memo).
- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_closeout.md` (new — this file).
- `docs/00-meta/current-project-state.md` (modified — narrow new Phase 4bn-D paragraph + new Current-phase block inserted immediately before the existing Phase 4bn-C Current-phase block; prior Phase 4bn-A / 4bn-B / 4bn-C paragraphs and prior Current-phase blocks preserved as labelled historical context).

**No source code modified; no test modified; no committed-script modified; no `pyproject.toml` / `README.md` / `.gitignore` / MCP file modified.** **No manifest, sidecar, gate-report, or successor-state artefact created, modified, or committed.** **No local data artefact created or mutated. No ML rerun. No diagnostics rerun. No new local gitignored artefact created. No ML artefact, diagnostic artefact, reusable split mask, model binary, or row-level prediction created or persisted. No acquisition. No endpoint call. No WebSocket / user stream. No credential / `.env` / `.mcp.json` / MCP / Graphify use.**

## 7. Scoping decision result

**`RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

This recommends only that a future, separately authorized Phase 4bn-E (bounded ML-baseline expansion implementation, scoped to *one* of {C-A class weighting, C-D train-vs-validation feature drift diagnostics, C-E calibration-limited evaluation}) may be considered by the operator as the cleanest non-paused option. It does not authorize implementation, model training, model scoring, prediction generation, feature ranking / selection, model selection through results, hyperparameter tuning, threshold tuning, strategy, signals, PnL simulation, backtests, acquisition, manifest mutation, successor-state mutation, paper / shadow / live-readiness, deployment, or exchange-write.

The operator may equivalently choose **remain paused** or **reject the successor and close the ML arc**; Phase 4bn-D does not foreclose either alternative.

## 8. Phase 4bn-C interpretation carried forward

`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` (Phase 4bn-C; merge-complete, SHA-finalized, project-complete on `main`). Phase 4bn-C interpreted the Phase 4bn-B `RECORD_EVIDENCE_ONLY` result, surfaced twelve forensic hypotheses for the weak baseline-vs-prior separation, and evaluated five candidate follow-up paths. Phase 4bn-D is exactly the docs-only / design-only / scoping-only successor that Phase 4bn-C's recommendation made conditionally allowable; the operator's separate authorization of Phase 4bn-D was issued in the authorization prompt that produced this work.

## 9. Phase 4bn-B decision carried forward

`RECORD_EVIDENCE_ONLY` (Phase 4bn-B; merge-complete, SHA-finalized, project-complete on `main`). Phase 4bn-B implemented exactly the Phase 4bn-A §9 – §20 design and produced descriptive ML-baseline evidence on the train and validation splits only. The test holdout is sealed (`test_rows_loaded: 0`). The four fixed-a-priori baseline families (`majority_class_prior`, `persistence_past_return_sign`, `multinomial_logistic_regression_l2`, `multinomial_linear_classifier_l1`) were each run exactly once with locked SGD hyperparameters; no model was selected as "best"; no feature was ranked or selected; no hyperparameter or threshold was tuned; no strategy / signal / PnL / backtest exists. Phase 4bn-D does not rerun, re-inspect, or re-evaluate any Phase 4bn-B local artefact.

## 10. Corrected Phase 4bn-B interpretation summary preserved verbatim

- **The flat class is underrepresented, not dominant** (0.15 – 1.09 % across both included horizons and both supervised splits).
- **The classification problem is effectively near-balanced up / down with a very thin flat class** (down ≈ up ≈ 0.495 ± 0.005).
- **Majority baseline accuracy is roughly 49 – 50 %** (validation floors: 0.4938 at 15s; 0.4950 at 60s).
- **L2 / L1 linear baselines show real but small descriptive lift:** ~+5 pp accuracy at 15s; ~+1.5 pp accuracy at 60s; ~+14 pp macro-F1 at 15s; ~+11 pp macro-F1 at 60s; macro-F1 lift structurally driven by predicting both up and down at all; flat class never predicted by L2 / L1 (per-class P / R / F1 = 0 / 0 / 0 on flat).
- **Persistence slightly beats majority on hard accuracy but is catastrophically worse on log-loss (~18× majority) and Brier (~2× majority)** because it emits hard one-hot probabilities; persistence is **not** a calibrated probabilistic baseline.
- **L2 15s is well-calibrated in the dominant 0.5 – 0.6 confidence bin (~86 % of validation rows; reliability gap −0.0047) but the high-confidence tail is severely over-confident** (gaps −0.061 to −0.392 in the 0.6 – 1.0 bins; the 0.8 – 0.9 bin's empirical accuracy 0.4881 is *below* the majority floor).
- **A naive "trade when confidence is high" idea would fail under current evidence** — the most-confident predictions are no better than chance.
- **15s has stronger model signal but worse cost / tradability context** (only ~6.2 % of validation rows exceed 1× the 16 bps round-trip cost).
- **60s has better cost context but weaker model signal** (~18.3 % of validation rows exceed 1× cost; L2 lift collapses to ~1.5 pp; predictions become strongly down-biased).
- **None of this is edge, profitability, tradability, strategy-readiness, or a signal.** Phase 4bn-D inherits this boundary without softening it.

## 11. Candidate bounded expansion menu evaluated

Six candidate paths evaluated at design level only (per memo §9 – §10):

- **C-A — Class weighting / flat-class handling feasibility.**
- **C-B — Cost-commensurate label framing feasibility.**
- **C-C — Horizon-envelope feasibility.**
- **C-D — Train-vs-validation feature drift diagnostics feasibility.**
- **C-E — Calibration-limited evaluation feasibility.**
- **C-F — Optional shallow non-linear baseline feasibility (only if memory and leakage controls can be bounded).**

For each candidate, the memo records purpose, evidence source from Phase 4bn-B / 4bn-C, allowed future inputs, forbidden future inputs, expected output if separately authorized later, failure / stop condition, and explicit non-strategy / non-signal / non-edge status. **No candidate is selected by Phase 4bn-D for execution.** Each candidate is treated as a discrete, separately evaluable question; the per-candidate evaluation in memo §10 is the sole mechanism by which any one candidate could later be selected for a separately authorized successor.

## 12. Recommended successor (NOT authorized)

**Conditional next, NOT authorized: Phase 4bn-E — a bounded ML-baseline expansion implementation phase, scoped to *one* of {C-A class weighting, C-D train-vs-validation feature drift diagnostics, C-E calibration-limited evaluation}, selected by separate operator authorization.** Phase 4bn-E would, if separately authorized later: be Tier 1 — Full Phase; name exactly one candidate as its scope; inherit every Phase 4bn-D §11 control, every §13 validation gate, and every §14 stop condition; keep the test holdout sealed; persist no model binary, no row-level prediction, no reusable split mask; not mutate any manifest, successor-state artefact, gate report, or governance label; not authorize any further successor by itself.

Alternative scoping-only successors (also NOT authorized by Phase 4bn-D):

- **Phase 4bn-E-B (scoping-only)** — a docs-only / design-only memo enumerating C-B candidate cost-commensurate label framings at design level (no label generation, no acquisition);
- **Phase 4bn-E-C (scoping-only)** — a docs-only / design-only memo enumerating C-C horizon-envelope questions at design level (no kernel rerun, no acquisition);
- **Phase 4bn-E-F-stage-1 (scoping-only)** — a docs-only / design-only memo specifying the C-F shallow-tree bounded-memory profile (no training).

Or the operator may **remain paused** (no successor authorized) or **reject the successor and close the ML arc** (operationally close the v002 ML-baseline family for further bounded expansion under current evidence).

## 13. Boundary confirmations

- no source code modified; no test modified; no committed script modified; no config modified.
- no `.gitignore`, `pyproject.toml`, or `README.md` modified.
- no MCP file modified or read.
- no `data/microstructure/` artefact committed; no `data/research/` artefact committed.
- no `data/microstructure/` artefact created or modified; no `data/research/` artefact created or modified.
- no manifest mutated; no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no `chronological_split_policy` changed; no `diagnostics_authorized` / `ml_authorized` changed.
- no successor-state artefact mutated, created, or accessed.
- no Phase 4bm-Q gate report mutated; no Phase 4bm-W diagnostic outputs mutated; no Phase 4bn-B local outputs mutated; no v002 label or feature manifest mutated.
- no diagnostics rerun; no diagnostic artefact created; no ML rerun; no ML artefact created; no reusable split mask created / materialized; no model binary persisted; no row-level prediction persisted.
- no model training / scoring / prediction generation / feature ranking / feature selection / model selection through results / hyperparameter tuning / threshold tuning.
- no strategy defined or run; no trade signals generated; no PnL simulated; no backtests run; no walk-forward optimization.
- test holdout not used for any reason.
- no data acquired; no public / authenticated / private endpoint called; no Binance API called; no WebSocket / user-stream opened; no credential / `.env` / `.mcp.json` / MCP / Graphify used.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- no retained verdict revised; no project lock loosened; no M0 amendment; no successor authorized.

## 14. Retained verdicts preserved

H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m thread, V2, G1, C1 — all preserved verbatim. All prior phase results (Phase 4am .. Phase 4bn-C) preserved verbatim.

## 15. Project locks preserved

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 (0.25% / 2× / one-position / mark-price stops); Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k / 4p / 4q / 4v / 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar / path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard — all preserved verbatim.

## 16. Recommended state

**Remain paused.** Branch-complete only; not merged; not project-complete. A separately authorized Tier 1 merge phase is required for project completion. The scoping decision `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION` authorizes nothing. **Phase 4bn-E is not authorized by Phase 4bn-D.** **Recommended state remains paused.**

## 17. Required exact phrases (verbatim)

- Phase 4bn-D is a docs-only / design-only / scoping-only bounded ML-baseline expansion scoping memo.
- Phase 4bn-D does not train ML models.
- Phase 4bn-D does not run ML.
- Phase 4bn-D does not score models.
- Phase 4bn-D does not generate predictions.
- Phase 4bn-D does not generate reusable split masks.
- Phase 4bn-D does not persist model binaries.
- Phase 4bn-D does not persist row-level predictions.
- Phase 4bn-D does not read, inspect, evaluate, or report any test-holdout metric.
- Phase 4bn-D does not use the sealed test split.
- Phase 4bn-D does not select models through results.
- Phase 4bn-D does not rank features.
- Phase 4bn-D does not select features.
- Phase 4bn-D does not tune hyperparameters.
- Phase 4bn-D does not tune thresholds.
- Phase 4bn-D does not run strategy research.
- Phase 4bn-D does not define a strategy.
- Phase 4bn-D does not generate trade signals.
- Phase 4bn-D does not simulate PnL.
- Phase 4bn-D does not run backtests.
- Phase 4bn-D does not run diagnostics.
- Phase 4bn-D does not rerun Phase 4bn-B.
- Phase 4bn-D does not acquire data.
- Phase 4bn-D does not call any public, authenticated, or private endpoint.
- Phase 4bn-D does not open any WebSocket or user stream.
- Phase 4bn-D does not use credentials, .env, .mcp.json, MCP, or Graphify.
- Phase 4bn-D does not mutate any manifest.
- Phase 4bn-D does not mutate any successor-state artefact.
- Phase 4bn-D does not commit data/microstructure.
- Phase 4bn-D does not commit data/research.
- Phase 4bn-D does not authorize Phase 4bn-E, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, or any successor phase.
- Recommended state remains paused.
