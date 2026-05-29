# Phase 4bn-D — Merge Closeout

**Phase 4bn-D is now merge-complete on main.** **Phase 4bn-D is a docs-only / design-only / scoping-only bounded ML-baseline expansion scoping memo.** **Phase 4bn-D does not train ML models.** **Phase 4bn-D does not run ML.** **Phase 4bn-D does not score models.** **Phase 4bn-D does not generate predictions.** **Phase 4bn-D does not generate reusable split masks.** **Phase 4bn-D does not persist model binaries.** **Phase 4bn-D does not persist row-level predictions.** **Phase 4bn-D does not read, inspect, evaluate, or report any test-holdout metric.** **Phase 4bn-D does not use the sealed test split.** **Phase 4bn-D does not select models through results.** **Phase 4bn-D does not rank features.** **Phase 4bn-D does not select features.** **Phase 4bn-D does not tune hyperparameters.** **Phase 4bn-D does not tune thresholds.** **Phase 4bn-D does not run strategy research.** **Phase 4bn-D does not define a strategy.** **Phase 4bn-D does not generate trade signals.** **Phase 4bn-D does not simulate PnL.** **Phase 4bn-D does not run backtests.** **Phase 4bn-D does not run diagnostics.** **Phase 4bn-D does not rerun Phase 4bn-B.** **Phase 4bn-D does not acquire data.** **Phase 4bn-D does not call any public, authenticated, or private endpoint.** **Phase 4bn-D does not open any WebSocket or user stream.** **Phase 4bn-D does not use credentials, `.env`, `.mcp.json`, MCP, or Graphify.** **Phase 4bn-D does not mutate any manifest.** **Phase 4bn-D does not mutate any successor-state artefact.** **Phase 4bn-D does not commit `data/microstructure`.** **Phase 4bn-D does not commit `data/research`.** **Phase 4bn-D does not authorize Phase 4bn-E, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, or any successor phase.** **Recommended state remains paused.**

## 1. Phase identity

- **Phase:** Phase 4bn-D — Multi-Day V002 Bounded ML-Baseline Expansion Scoping Memo.
- **Type:** docs-only / design-only / scoping-only governance memo (Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3). The separately authorized scoping phase that follows the Phase 4bn-C interpretation decision `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-D bounded ML-baseline expansion scoping memo + closeout + the narrow `current-project-state.md` paragraph + Current-phase block onto `main`, recording the scoping decision `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION` as project state. The phase reads only committed repository Markdown reports as the evidence base; it opens no local gitignored `data/research/` ML output; it creates no data artefact; it mutates no manifest, sidecar, gate report, or successor-state file. It evaluates six candidate bounded expansion paths (C-A class weighting; C-B cost-commensurate label framing; C-C horizon-envelope; C-D train-vs-validation feature drift diagnostics; C-E calibration-limited evaluation; C-F optional shallow non-linear baseline) at design level only, records per-candidate purpose / evidence-source / allowed inputs / forbidden inputs / expected output / failure-stop / non-strategy status, and records a single scoping recommendation. It trains, scores, predicts, selects, ranks, tunes, and runs nothing.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-d/bounded-ml-baseline-expansion-scoping`.

## 2. SHAs

- **`main` SHA before merge:** `e1dc2fa4570baccfc9e4a866899ca6c98fa03c66` (Phase 4bn-C SHA-finalization commit `docs(phase-4bn-c): finalize merge closeout shas`; `main == origin/main` verified pre-merge).
- **Base SHA:** `e1dc2fa4570baccfc9e4a866899ca6c98fa03c66`.
- **Branch tip SHA before merge:** `2cd9b47667c800dc0a300047126c07d6ff67cf97`.
- **Docs commit SHA:** `2cd9b47667c800dc0a300047126c07d6ff67cf97` (`docs(phase-4bn-d): scope bounded ml-baseline expansion`; the memo + closeout + current-project-state block are a single docs commit, which is also the branch tip).
- **Merge commit SHA:** `6b8cc6a8f3d0333bc84db189bf470d074b14f088` (`docs(phase-4bn-d): merge bounded ml-baseline expansion scoping`).
- **Merge-closeout commit SHA:** `c8ad067eb4f81bbd1613aeb9a59d9e0973e1fca6` (`docs(phase-4bn-d): add merge closeout`).
- **SHA-finalization commit:** recorded in the final operator report and `git log` as `docs(phase-4bn-d): finalize merge closeout shas`. Per the repo convention used for Phase 4bn-C / 4bn-B / 4bn-A / 4bm-Z / 4bm-Y / 4bm-X, the SHA-finalization commit cannot self-reference its own hash inside its own diff; its SHA is captured in the final operator report and `git log`. After that commit and push, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.
- **Final `main` / `origin/main` SHA after push:** equals the SHA-finalization commit; recorded in the final operator report and updated into this merge-closeout by the SHA-finalization commit.

## 3. Merge method

- `git merge --no-ff` with the `ort` strategy.
- Merge commit message: `docs(phase-4bn-d): merge bounded ml-baseline expansion scoping`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_bounded-ml-baseline-expansion-scoping.md` (added).
- `docs/00-meta/implementation-reports/2026-05-29_phase-4bn-d_closeout.md` (added).
- `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bn-D paragraph + new Current-phase block inserted immediately after the Phase 4bn-C paragraph and immediately before the existing Phase 4bn-C Current-phase block; prior Phase 4bn-A / 4bn-B / 4bn-C paragraphs and prior Current-phase blocks preserved as labelled historical context).

Source: none. Tests: none. Scripts: none. Config: none. **No `pyproject.toml`, `README.md`, `.gitignore`, MCP file, manifest, sidecar, gate report, successor-state artefact, existing source / test / script file, or any `data/microstructure/` artefact was modified.** No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph addition. **No `data/research/` artefact was committed** (the seven Phase 4bn-B local outputs + their canonical Phase 4bb-F sidecars remain local-only and gitignored under `.gitignore:88: data/research/`; the four Phase 4bm-W diagnostic outputs + sidecars remain local-only and gitignored under the same rule; Phase 4bn-D did not access or re-read any of them). The merge-closeout file (this file) is added by the subsequent merge-closeout commit on `main`, not by the merge commit itself.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 157 ++++++
 ...-4bn-d_bounded-ml-baseline-expansion-scoping.md | 541 +++++++++++++++++++++
 .../2026-05-29_phase-4bn-d_closeout.md             | 152 ++++++
 3 files changed, 850 insertions(+)
```

The diff matches the expected change set from the authorization prompt exactly: two added docs files plus one narrow modification to `current-project-state.md`. No source / test / script / config / data / manifest / sidecar / gate-report / successor-state change.

## 6. Verdict

**MEMO RECORDED — `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Phase 4bn-D is the separately authorized docs-only / design-only / scoping-only governance memo that scopes a possible future bounded ML-baseline expansion implementation phase, evaluates six candidate paths at design level only, and records a single recommendation. It carries the Phase 4bn-C interpretation decision forward verbatim (`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`), carries the Phase 4bn-B decision forward verbatim (`RECORD_EVIDENCE_ONLY`), and preserves the Phase 4bn-C corrected interpretation of the Phase 4bn-B evidence verbatim. It reads no local gitignored artefact, mutates no manifest or successor-state artefact, and authorizes no execution. **Phase 4bn-D is recommendation-only and authorizes nothing.** It authorizes no implementation, no ML training, no model scoring, no prediction generation, no feature ranking / selection, no model selection through results, no hyperparameter / threshold tuning, no strategy / signal / PnL / backtest, no acquisition, no manifest mutation, no successor-state mutation, no paper / shadow / live-readiness / deployment / exchange-write. The v002 label and feature manifests remain `research_eligible = false` / `eligibility_gate_status = "pending"`; the label manifest's `chronological_split_policy` remains `"not_yet_defined"` on disk (recorded only in the Phase 4bm-U sibling successor-state JSON). The lifecycle state is **remain paused**.

After this merge commit, the merge-closeout commit, and the SHA-finalization commit are pushed, Phase 4bn-D is project-complete on `main`. **Project completion still requires the SHA-finalization commit below per the repo's current Phase 4bn-C / 4bn-B / 4bn-A SHA-finalization convention.**

### 6.1 Phase 4bn-C interpretation carried forward

`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` (Phase 4bn-C; merge-complete, SHA-finalized, project-complete on `main`). Phase 4bn-C interpreted the Phase 4bn-B `RECORD_EVIDENCE_ONLY` result, surfaced twelve forensic hypotheses for the weak baseline-vs-prior separation, and evaluated five candidate follow-up paths. Phase 4bn-D is exactly the docs-only / design-only / scoping-only successor that Phase 4bn-C's recommendation made conditionally allowable; the operator's separate authorization of Phase 4bn-D was issued in the authorization prompt that produced this work.

### 6.2 Phase 4bn-B decision carried forward

`RECORD_EVIDENCE_ONLY` (Phase 4bn-B; merge-complete, SHA-finalized, project-complete on `main`). Phase 4bn-B implemented exactly the Phase 4bn-A §9 – §20 design and produced descriptive ML-baseline evidence on the train and validation splits only. The test holdout is sealed (`test_rows_loaded: 0`). The four fixed-a-priori baseline families (`majority_class_prior`, `persistence_past_return_sign`, `multinomial_logistic_regression_l2`, `multinomial_linear_classifier_l1`) were each run exactly once with locked SGD hyperparameters; no model was selected as best; no feature was ranked or selected; no hyperparameter or threshold was tuned; no strategy / signal / PnL / backtest exists.

### 6.3 Phase 4bn-D is docs-only / design-only / scoping-only and authorizes nothing

Phase 4bn-D is a docs-only / design-only / scoping-only governance memo. It adds two new tracked docs files under `docs/00-meta/implementation-reports/` (the scoping memo + the paired closeout) and narrowly updates `docs/00-meta/current-project-state.md`. **No** source / test / committed-script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** local data artefact created or mutated. **No** ML rerun. **No** diagnostics rerun. **No** ML artefact, diagnostic artefact, reusable split mask, model binary, or row-level prediction created or persisted. **No** acquisition, endpoint call, WebSocket / user stream, or credential / `.mcp.json` / MCP / Graphify use. **No** successor authorization.

### 6.4 Corrected Phase 4bn-B evidence preserved verbatim

- **The flat class is underrepresented, not dominant** (0.15 – 1.09 % across both included horizons and both supervised splits).
- **The classification problem is effectively near-balanced up / down with a very thin flat class** (down ≈ up ≈ 0.495 ± 0.005).
- **Majority baseline accuracy is roughly 49 – 50 %** (validation floors: 0.4938 at 15s; 0.4950 at 60s).
- **L2 / L1 linear baselines show real but small descriptive lift:** ~+5 pp accuracy at 15s; ~+1.5 pp accuracy at 60s; ~+14 pp macro-F1 at 15s; ~+11 pp macro-F1 at 60s.
- **Persistence slightly beats majority on hard accuracy but is catastrophically worse on log-loss (~18× majority) and Brier (~2× majority)** because it emits hard one-hot probabilities; persistence is **not** a calibrated probabilistic baseline.
- **L2 15s is well-calibrated in the dominant 0.5 – 0.6 confidence bin (~86 % of validation rows; reliability gap −0.0047) but the high-confidence tail is severely over-confident** (reliability gaps −0.061 to −0.392 in the 0.6 – 1.0 bins; the 0.8 – 0.9 bin's empirical accuracy 0.4881 is *below* the majority floor).
- **A naive "trade when confidence is high" idea would fail under current evidence** — the most-confident predictions are no better than chance.
- **15s has stronger model signal but worse cost / tradability context** (only ~6.2 % of validation rows exceed 1× the 16 bps round-trip cost).
- **60s has better cost context but weaker model signal** (~18.3 % of validation rows exceed 1× cost; L2 lift collapses to ~1.5 pp; predictions become strongly down-biased).
- **None of this is edge, profitability, tradability, strategy-readiness, or a signal.** Phase 4bn-D inherits this boundary without softening it.

### 6.5 Six candidate bounded expansion paths evaluated at design level only

- **C-A — Class weighting / flat-class handling feasibility.**
- **C-B — Cost-commensurate label framing feasibility.**
- **C-C — Horizon-envelope feasibility.**
- **C-D — Train-vs-validation feature drift diagnostics feasibility.**
- **C-E — Calibration-limited evaluation feasibility.**
- **C-F — Optional shallow non-linear baseline feasibility (only if memory and leakage controls can be bounded).**

For each candidate, the memo records purpose, evidence source from Phase 4bn-B / 4bn-C, allowed future inputs, forbidden future inputs (including the sealed test split, any new feature, any feature ranking / selection, any hyperparameter / threshold tuning through validation, any probability-to-signal conversion, any model binary or row-level prediction persistence, any reusable split mask, any manifest mutation, any successor-state mutation, any acquisition, any endpoint call, any credential / `.env` / `.mcp.json` / MCP / Graphify use, any strategy / signal / PnL / backtest), expected output if separately authorized later, failure / stop condition, and explicit non-strategy / non-signal / non-edge status. **No candidate is selected by Phase 4bn-D for execution.**

### 6.6 Recommended successor (NOT authorized)

**Conditional next, NOT authorized: Phase 4bn-E — a bounded ML-baseline expansion implementation phase, scoped to *one* of {C-A class weighting, C-D train-vs-validation feature drift diagnostics, C-E calibration-limited evaluation}, selected by separate operator authorization.** Phase 4bn-E would, if separately authorized later: be Tier 1 — Full Phase; name exactly one candidate as its scope; inherit every Phase 4bn-D §11 control, every §13 validation gate, and every §14 stop condition; keep the test holdout sealed; persist no model binary, no row-level prediction, no reusable split mask; not mutate any manifest, successor-state artefact, gate report, or governance label; not authorize any further successor by itself.

Alternative scoping-only successors (also NOT authorized by this merge):

- **Phase 4bn-E-B (scoping-only)** — a docs-only / design-only memo enumerating C-B candidate cost-commensurate label framings at design level (no label generation, no acquisition).
- **Phase 4bn-E-C (scoping-only)** — a docs-only / design-only memo enumerating C-C horizon-envelope questions at design level (no kernel rerun, no acquisition).
- **Phase 4bn-E-F-stage-1 (scoping-only)** — a docs-only / design-only memo specifying the C-F shallow-tree bounded-memory profile (no training).

The operator may equivalently **remain paused** (no successor authorized) or **reject the successor and close the ML arc** (operationally close the v002 ML-baseline family for further bounded expansion under current evidence). Phase 4bn-D does not foreclose either alternative.

## 7. Local gitignored outputs

**None produced by Phase 4bn-D.** Phase 4bn-D created no local artefact. The pre-existing predecessor local gitignored artefacts were not accessed by Phase 4bn-D (the scoping memo reads only committed repository Markdown reports as the evidence base; it does not re-hash, re-open, or re-evaluate any local file). They remain gitignored and not committed:

- Phase 4bn-B ML-baseline outputs under `data/research/microstructure/ml-baselines/phase-4bn-b/` — `git check-ignore -v` → `.gitignore:88: data/research/`.
- Phase 4bm-W diagnostic outputs under `data/research/microstructure/diagnostics/phase-4bm-w/` — `.gitignore:88: data/research/`.
- Phase 4bm-S / Phase 4bm-U successor-state JSONs + sidecars under `data/microstructure/successor-state/labels/` — `.gitignore:85: data/microstructure/`.
- Phase 4bm-Q gate report + sidecar under `data/microstructure/gate-reports/labels/` — `.gitignore:85: data/microstructure/`.

## 8. Validation results

- `git diff --check main..phase-4bn-d/bounded-ml-baseline-expansion-scoping` → clean (no whitespace errors).
- `git diff --name-status main..phase-4bn-d/bounded-ml-baseline-expansion-scoping` (pre-merge): `M docs/00-meta/current-project-state.md`; `A …_phase-4bn-d_bounded-ml-baseline-expansion-scoping.md`; `A …_phase-4bn-d_closeout.md` (docs only).
- `git diff --stat main..phase-4bn-d/bounded-ml-baseline-expansion-scoping` (pre-merge): `3 files changed, 850 insertions(+)`.
- `git status --short` (pre and post merge) → clean working tree; only expected gitignored untracked entries (`.claude/scheduled_tasks.lock`, and the pre-existing gitignored `data/research/` and `data/microstructure/` local outputs).
- `git check-ignore -v` for `data/research/` → `.gitignore:88:data/research/`.
- `git check-ignore -v` for `data/microstructure/` → `.gitignore:85:data/microstructure/`.
- `git log --oneline -5 --decorate` post-merge confirmed: `6b8cc6a (HEAD -> main) docs(phase-4bn-d): merge bounded ml-baseline expansion scoping` above `2cd9b47 (phase-4bn-d/...) docs(phase-4bn-d): scope bounded ml-baseline expansion` above `e1dc2fa (origin/main, origin/HEAD) docs(phase-4bn-c): finalize merge closeout shas`.
- No source / test / script / config changed, so ruff / mypy / pytest were not invoked for this docs-only merge; no source-test / lint / type-check coverage is claimed for Phase 4bn-D itself. No markdown-lint tool is part of the repo standard for these implementation reports (consistent with Phase 4bn-C's `2026-05-28_phase-4bn-c_merge-closeout.md` §8: "No markdown-lint tool is part of the repo standard for these reports; none was invented or run."); none was invented or run here.
- Encoding / line-ending preservation: `docs/00-meta/current-project-state.md` remains UTF-8 without BOM, CRLF line endings; the two new docs files were authored as UTF-8 without BOM, CRLF (matching the existing Phase 4bn-C closeout convention). The § / – / × / ≈ / ± / − characters used in the Phase 4bn-D paragraph and Current-phase block are valid UTF-8.

## 9. Upstream immutability evidence

Phase 4bn-D explicitly did not read or modify any local gitignored artefact (the scoping memo reads only committed repository Markdown reports as the evidence base; it does not re-hash any local data file). The Phase 4bn-D merge brings forward zero changes to any prior governed artefact:

| Artefact | Pre-merge SHA256 | Post-merge | Result |
| --- | --- | --- | --- |
| `ml_baseline_run_manifest.json` (Phase 4bn-B) | `cd436e3823d7c8e5e07431a9b11ebcf72e35e997db9a76ca865ff1885b3cfa13` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `ml_baseline_run_manifest.json.sha256` (Phase 4bn-B) | `b13dbedf70f02891df50d9080f904b6327f0569687c257f3840256ec9e02f293` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `per_horizon_model_summary.json` (Phase 4bn-B) | `d94f8d72781afd4c229ee7b525e8cd79f2a13a56e5a1d68e42e74724d4c396b0` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `per_horizon_model_summary.json.sha256` (Phase 4bn-B) | `23f91cc02a6a272b25b57cd46953f139e58beca7073351dbfa6fae4f150c03cf` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `metrics_train_validation.csv` (Phase 4bn-B) | `40cde4a01dde14e4152c4d53b70f57bc330f20d3f2ef6248b9bb18e1c190a7a8` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `metrics_train_validation.csv.sha256` (Phase 4bn-B) | `5b3a04fae93df8b73830b83e92addd80a498d9d0061e2e0dd9cdf9fc9b202a34` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `calibration_summary.csv` (Phase 4bn-B) | `a0f469d27c90958b2fc308b54753d97bd78830321d5954e7d30649bff4e00138` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `calibration_summary.csv.sha256` (Phase 4bn-B) | `1b43de79ae210b5c082c087b17eb5ca9a96c7e6990d04cd82b9e329f16ba6df9` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `class_balance_summary.csv` (Phase 4bn-B) | `6e6338bff25bae253d5442763fb960339a31f936e51e58ae2199af5e844df40f` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `class_balance_summary.csv.sha256` (Phase 4bn-B) | `41ca08d604e597aaceff0964f720742367801e6c43538539a4265933932294e6` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `feature_schema_used.json` (Phase 4bn-B) | `5f3d84b45fe8cc538c39c8ddc093625cfe6f8040a862c2e97ad970114415fac6` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `feature_schema_used.json.sha256` (Phase 4bn-B) | `2f99379a21a0bd6937be59b8cd6c7a048f94cba4b20028ea0c7149feca399a42` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `transform_metadata.json` (Phase 4bn-B) | `73b455af6698ab6b43536a0f1e3941bdd9d4078b619ce0287cbdc634313286b0` | same | IDENTICAL (not touched by Phase 4bn-D) |
| `transform_metadata.json.sha256` (Phase 4bn-B) | `d3b91fb201b047a5e36b669ba0aac63fe225261dfe4283e524146ffecae792dd` | same | IDENTICAL (not touched by Phase 4bn-D) |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | same | IDENTICAL (not touched by Phase 4bn-D) |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | same | IDENTICAL (not touched by Phase 4bn-D) |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | IDENTICAL (not touched by Phase 4bn-D) |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | same | IDENTICAL (not touched by Phase 4bn-D) |

Per-prompt evidence carry-forward (recorded in Phase 4bn-C merge-closeout §9 and unchanged by this docs-only Phase 4bn-D merge because Phase 4bn-D did not read any local artefact): Phase 4bm-U split-policy successor-state JSON `6834ab11…` + sidecar `fa9ae709…`; Phase 4bm-S research-use successor-state JSON `081730006c…` + sidecar `05597fe4…`; Phase 4bm-Q gate report `8a360608…` + sidecar `3913a510…`; Phase 4bm-W summary `f4b825af…` + sidecar `ff52873c…`; Phase 4bm-W manifest `ac10061d…` + sidecar `644506e3…` — all known IDENTICAL through the prior Phase 4bn-C merge and unchanged by this docs-only Phase 4bn-D merge.

## 10. Manifest state preservation

- **v002 label manifest** (`5e17074d…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `chronological_split_policy = "not_yet_defined"`; `label_family_research_use_authorized = false`; `stage_5_label_cleared = false`; `diagnostics_authorized = false` (historical). **No transition occurred.**
- **v002 feature manifest** (`512a0a54…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false`. **No transition occurred.**
- Phase 4bm-S, Phase 4bm-U, and Phase 4bm-Q sibling successor-state / gate-report artefacts: not accessed; byte-identical (see §9). No transition occurred.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no test modified; no committed script modified; no config modified.
- no `.gitignore`, `pyproject.toml`, or `README.md` modified.
- no MCP file created, read, or modified; no `.mcp.json` created or read; no Graphify use.
- no `data/microstructure/` artefact committed; no `data/research/` artefact committed.
- no `data/microstructure/` artefact created or modified; no `data/research/` artefact created or modified; no local gitignored artefact opened, re-hashed, or re-evaluated.
- no manifest mutated; no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no `chronological_split_policy` changed; no `diagnostics_authorized` / `ml_authorized` changed.
- no successor-state artefact mutated, created, or accessed (Phase 4bm-S `081730006c…`, Phase 4bm-U `6834ab11…` byte-identical).
- no Phase 4bm-Q gate report mutated (`8a360608…` byte-identical).
- no Phase 4bm-W diagnostic output mutated (all four SHAs byte-identical).
- no Phase 4bn-B local output mutated (all 14 SHAs byte-identical; not even read).
- no diagnostics rerun; no new diagnostic artefact created.
- no ML rerun; no ML artefact created.
- no reusable split mask created / materialized; no model binary persisted; no row-level prediction persisted.
- no model training / scoring / prediction generation / feature ranking / feature selection / model selection through results / hyperparameter tuning / threshold tuning.
- no strategy defined or run; no trade signals generated; no PnL simulated; no backtests run; no walk-forward optimization.
- test holdout not used for any reason; Phase 4bn-B `test_rows_loaded: 0` preserved.
- no data acquired; no public / authenticated / private endpoint called; no Binance API called; no WebSocket / user stream opened; no credential / `.env` / `.mcp.json` / MCP / Graphify used.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- no retained verdict revised; no project lock loosened; no M0 amendment; no successor authorized.

## 12. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim. All prior phase results (Phase 4am .. Phase 4bn-C) preserved verbatim.

## 13. Preserved project locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k / 4p / 4q / 4v / 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bn-D merge does not, and cannot, be construed as authorizing:

- any ML rerun; any further ML-baseline expansion; any model training; any model scoring; any prediction generation; any feature ranking; any feature selection; any feature pruning; any model selection through results; any hyperparameter tuning; any threshold tuning; any meta-labeling; any ensemble construction; any calibrator fitting;
- any strategy research; any strategy design; any signal generation; any trade-signal generation; any PnL simulation; any equity-curve construction; any Sharpe / Sortino / drawdown / hit-rate / trade-PnL metrics; any backtests; any walk-forward optimization;
- any use of the test holdout for training, fitting, calibration, evaluation, tuning, design, model selection, threshold selection, reporting, or inspection;
- any diagnostics rerun; any diagnostic artefact creation; any ML artefact creation; any reusable split-mask materialization; any row-level prediction persistence; any model binary persistence;
- any data acquisition (no additional days / symbols / families beyond the locked 90-day v002 envelope; no mark-price / spot / cross-venue / order-book / additional aggTrades; no 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; no barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels);
- any manifest mutation; any successor-state mutation; any `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized` transition from this memo alone;
- any public / authenticated / private endpoint call; any WebSocket / user stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4 canonical; Phase 5; Phase 4bn-E; any future bounded ML-baseline expansion implementation phase; Phase 4bn-* further successors; Phase 4bo-* / Phase 4bp-*;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m research-thread reopening (Phase 3t closure preserved).

`RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION` means only that a future, separately authorized Phase 4bn-E bounded ML-baseline expansion implementation phase, scoped to *one* of {C-A class weighting, C-D train-vs-validation feature drift diagnostics, C-E calibration-limited evaluation}, may be considered by the operator. **Any bounded ML-baseline expansion implementation phase requires a separately authorized phase.**

## 15. Successor authorization

**None.**

Not authorized by this merge:

- Phase 4bn-E — Multi-Day V002 Bounded ML-Baseline Expansion Implementation (or any phase under any name performing bounded ML-baseline expansion implementation, class-weighted-softmax implementation, train-vs-validation feature-drift diagnostic implementation, calibration-limited-evaluation implementation, label / target rework implementation, class-imbalance / regime-conditioning implementation, or any successor to the Phase 4bn-* arc);
- Phase 4bn-E-B / Phase 4bn-E-C / Phase 4bn-E-F-stage-1 (alternative scoping-only successors enumerated in the memo);
- any ML implementation execution; ML model training; model scoring; prediction generation; feature ranking / selection; model selection through results; hyperparameter tuning; threshold tuning;
- strategy research / design; signal generation; trade-signal generation; PnL simulation; backtests; walk-forward optimization;
- diagnostics rerun; diagnostic artefact creation; ML artefact creation; reusable split-mask materialization; row-level prediction persistence; model binary persistence; test-holdout tuning / design / evaluation / inspection;
- manifest mutation; successor-state mutation;
- Phase 4bn-* further successors / Phase 4bo-* / Phase 4bp-* / Phase 5 / Phase 4 canonical;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot / cross-venue data acquisition;
- research execution; paper / shadow; live-readiness; deployment; exchange-write; production keys; authenticated APIs; private endpoints; user stream; WebSockets; MCP; Graphify; `.mcp.json`; credentials.

## 16. Recommended state

**Remain paused.**

Phase 4bn-D is now merge-complete on main and, after the SHA-finalization commit and push, project-complete. The scoping decision `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION` authorizes nothing. **Any bounded ML-baseline expansion implementation phase requires a separately authorized phase.** **Phase 4bn-E is not authorized by Phase 4bn-D.** **Recommended state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-E bounded ML-baseline expansion implementation phase, scoped to *one* of {C-A class weighting, C-D train-vs-validation feature drift diagnostics, C-E calibration-limited evaluation}, is the cleanest non-paused option. It would respect every Phase 4bn-D memo §11 control, every §13 validation gate, and every §14 stop condition, and would keep the test holdout sealed. Phase 4bn-E is **not authorized** by this merge.

The operator may equivalently choose:

- **remain paused** (no successor authorized);
- **reject Phase 4bn-E and close the ML arc** (operationally close the v002 ML-baseline family for further bounded expansion under current evidence);
- **separately authorize a Phase 4bn-E prompt** scoped to exactly one of C-A, C-D, or C-E (requires a separate authorization prompt that satisfies `docs/00-meta/process/phase-prompt-template.md`).

**No paper / shadow / live / exchange-write / production-key / credentials / MCP / Graphify option is valid from this state.**

## 17. Known caveats

- Phase 4bn-D's scoping decision is a *recommendation*; nothing in this merge transitions the ML arc into execution. The operator's decision to authorize, defer, or reject Phase 4bn-E remains entirely open.
- The Phase 4bn-C calibration evidence (high-confidence tail severely over-confident) and the §11.6 cost-commensurability context (80 – 95 % of validation rows below the round-trip cost) explicitly foreclose threshold-tuning, probability-to-signal conversion, and any strategy framing for every future expansion phase; Phase 4bn-D §11 and §14 record these as binding controls and stop conditions for any successor.
- The Phase 4bn-B / Phase 4bn-A non-implementation of the optional shallow tree baseline (`BASELINE_SHALLOW_TREE_INCLUDED = False`) is preserved verbatim; Phase 4bn-D's C-F candidate revisits the question only at design level (whether bounded memory / leakage controls could be specified up front) and explicitly does not authorize implementation.
- The Phase 4bm-W envelope-terminal censoring asymmetry (857 rows: 1s 14 / 5s 39 / 15s 170 / 60s 634, all concentrated on 2025-02-28 inside the sealed test split) remains a non-blocking caveat for any future test-holdout evaluation phase; Phase 4bn-D does not authorize any test-holdout work.
- The lightweight Claude Code workspace standard (Phase 4bm-D-P1) and the thin-prompt context-management standard (Phase 4bm-A-P1) were used to author Phase 4bn-D; both standards are preserved verbatim.
