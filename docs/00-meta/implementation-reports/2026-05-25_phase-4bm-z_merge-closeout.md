# Phase 4bm-Z — Merge Closeout

**Phase 4bm-Z is now merge-complete on main.** **Phase 4bm-Z is a docs-only ML-readiness evaluation memo.** **Phase 4bm-Z does not train ML models.** **Phase 4bm-Z does not run ML.** **Phase 4bm-Z does not score models.** **Phase 4bm-Z does not generate predictions.** **Phase 4bm-Z does not select models.** **Phase 4bm-Z does not rank or select features.** **Phase 4bm-Z does not tune hyperparameters.** **Phase 4bm-Z does not tune thresholds.** **Phase 4bm-Z does not define or run strategy.** **Phase 4bm-Z does not generate signals.** **Phase 4bm-Z does not simulate PnL.** **Phase 4bm-Z does not run backtests.** **Phase 4bm-Z does not authorize acquisition.** **Phase 4bm-Z does not authorize research execution.** **Phase 4bm-Z does not create ML artefacts.** **Phase 4bm-Z does not create diagnostic artefacts.** **Phase 4bm-Z does not create split masks.** **Phase 4bm-Z does not use the test holdout for tuning or design.** **Phase 4bm-Z does not mutate any manifest.** **Phase 4bm-Z does not mutate any successor-state artefact.** **Phase 4bm-Z does not commit data/microstructure.** **Phase 4bm-Z does not commit data/research.** **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-A is not authorized by Phase 4bm-Z.** **Recommended state remains paused.**

> **Successor-naming note.** `Z` is the terminal letter of the `4bm-` series; by the repo's established convention (the Phase 4bm-Y / 4bm-X merge-closeouts enumerate `Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*` as unauthorized successors), the next letter-series is `4bn-A`. The required exact phrases therefore name **`Phase 4bn-A`** as the unauthorized successor. No successor is authorized under any name.

## 1. Phase identity

- **Phase:** Phase 4bm-Z — Multi-Day V002 ML-Readiness Evaluation Memo.
- **Type:** docs-only governance / methodology evaluation memo (Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bm-Z ML-readiness evaluation memo + closeout + the narrow `current-project-state.md` current-phase block onto `main`, recording the evaluation decision `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` as project state. The phase evaluates — at memo / governance level only — whether a future ML-baseline implementation scoping/design phase may be proposed; it trains, scores, predicts, selects, ranks, tunes, and runs nothing.
- **Target branch:** `main`.
- **Source branch:** `phase-4bm-z/multi-day-v002-ml-readiness-evaluation-memo`.

## 2. SHAs

- **`main` SHA before merge:** `2463ceb716d31c79ef766e9042fd40a3929f3e5c` (Phase 4bm-Y merge-closeout SHA-finalization commit; `main == origin/main` verified pre-merge).
- **Base SHA:** `2463ceb716d31c79ef766e9042fd40a3929f3e5c`.
- **Branch tip SHA before merge:** `0c84b6921a013c37da32a72063a79a7f68867ad3`.
- **Docs commit SHA:** `0c84b6921a013c37da32a72063a79a7f68867ad3` (`docs(phase-4bm-z): evaluate ml-readiness scope`; the memo + closeout + current-project-state block are a single docs commit, which is also the branch tip).
- **Merge commit SHA:** `5b86ecf496421e86138179f47c8273aa1837dbd1` (`docs(phase-4bm-z): merge ml-readiness evaluation memo`).
- **Merge-closeout commit SHA:** `b8afee7b4e9762e3880d1a782799631d588e78a1` (`docs(phase-4bm-z): add merge closeout`).
- **SHA-finalization commit:** `<recorded in the final operator report and git log as `docs(phase-4bm-z): finalize merge closeout shas`; it is the commit that records these final SHAs into this file>`. After that commit and push, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit. (Per the repo convention used for Phase 4bm-Y / 4bm-X / 4bm-W, the SHA-finalization commit cannot self-reference its own hash inside its own diff; its SHA is captured in the final operator report and git log.)
- **Final `main` / `origin/main` SHA after push:** equals the SHA-finalization commit; recorded in the final operator report.

## 3. Merge method

- `git merge --no-ff` with the `ort` strategy.
- Merge commit message: `docs(phase-4bm-z): merge ml-readiness evaluation memo`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-z_ml-readiness-evaluation-memo.md` (added).
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-z_closeout.md` (added).
- `docs/00-meta/current-project-state.md` (modified — narrow current-phase block addition; prior Phase 4bm-Y paragraph preserved as labelled historical context).

Source: none. Tests: none. Scripts: none. Config: none. **No `data/microstructure/` file was modified.** **No `data/research/` file was modified.** No prior governance memo was modified beyond the narrow `current-project-state.md` paragraph addition. No prior source / test / script was modified.

The merge-closeout file `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-z_merge-closeout.md` (this file) is added by the subsequent merge-closeout commit on `main`, not by the merge commit itself.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |   2 +
 .../2026-05-25_phase-4bm-z_closeout.md             | 160 ++++++++
 ...-25_phase-4bm-z_ml-readiness-evaluation-memo.md | 440 +++++++++++++++++++++
 3 files changed, 602 insertions(+)
```

The diff matches the expected change set from the authorization prompt exactly: two added docs files plus one narrow modification to `current-project-state.md`. No source / test / script / config / data / manifest / sidecar / gate-report / successor-state change.

## 6. Verdict

**MEMO RECORDED — `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING`.**

Phase 4bm-Z is the separately authorized docs-only ML-readiness *evaluation* memo recommended by Phase 4bm-Y. It evaluated, at memo / governance level only, whether current repo evidence, diagnostics, split policy, leakage controls, cost constraints, and horizon-specific constraints support proposing a future ML-baseline implementation phase. All eighteen evaluation criteria A–R PASS, so the memo recommends — and only recommends — that a future, separately authorized, docs-only or design-only ML-baseline implementation *scoping/design* phase *may* be proposed. **Phase 4bm-Z is recommendation-only and authorizes nothing.** It authorizes no ML implementation, no model training, no model scoring, no prediction generation, no feature ranking/selection, no model selection, no hyperparameter tuning, no threshold tuning, no strategy research, no signals, no PnL simulation, no backtests, no walk-forward optimization, no acquisition, and no research execution. The v002 label/feature manifests remain `research_eligible = false` / `eligibility_gate_status = "pending"`; the label manifest `chronological_split_policy` remains `"not_yet_defined"` on disk (the split policy is recorded only in the Phase 4bm-U sibling successor-state JSON). The lifecycle state is **remain paused**.

### 6.1 Evaluation criteria A–R — all PASS

| # | Criterion | Result |
| --- | --- | --- |
| A | Phase 4bm-Y completed and merged the docs-only ML-readiness scoping memo | PASS |
| B | Phase 4bm-Y scope internally complete enough to support a future ML-baseline implementation scoping/design phase | PASS |
| C | Phase 4bm-W diagnostics have 0 blocking structural failures | PASS |
| D | Phase 4bm-W non-blocking caveats carried forward as constraints; do not block implementation scoping | PASS |
| E | Phase 4bm-U split policy sufficient for later ML-baseline design | PASS |
| F | Train/validation/test usage rules explicit and enforceable | PASS |
| G | Test holdout remains protected from tuning/design | PASS |
| H | Leakage controls explicit and enforceable | PASS |
| I | Candidate metrics scoped without computing them now | PASS |
| J | Candidate baseline families scoped without training them now | PASS |
| K | Sample-weighting / imbalance / calibration questions explicitly identified | PASS |
| L | Cost-aware constraints explicit and include §11.6 8 bps per side / 16 bps round trip | PASS |
| M | Horizon-specific constraints explicit (1s/5s latency sensitivity; 60s censoring concentration) | PASS |
| N | No diagnostics rerun | PASS |
| O | No ML / strategy / backtest work authorized or run | PASS |
| P | No manifest or successor-state mutation | PASS |
| Q | No data/microstructure or data/research artefact committed | PASS |
| R | Retained verdicts and project locks unchanged | PASS |

**All evaluation criteria A–R PASS.**

### 6.2 Phase 4bm-Y decision carried forward

`RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` (Phase 4bm-Y). This Phase 4bm-Z is its separately authorized realization. Phase 4bm-Y authorized no ML, training, scoring, prediction, selection, ranking, tuning, strategy, backtests, acquisition, or research execution.

### 6.3 Phase 4bm-W diagnostic verdict carried forward

`DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (Phase 4bm-W): 0 blocking structural failures; 4 non-blocking caveats; descriptive-only — not ML-readiness, not strategy-readiness, not backtest-readiness. Carried forward unchanged; not re-derived, not re-issued, not rerun. The four caveats: (1) envelope-terminal censoring asymmetry — 857 censored rows `{1s:14, 5s:39, 15s:170, 60s:634}` all in the test split; (2) 538 embargo-excluded earlier-split rows (train 248, validation 290, test 0); (3) approximate-quantile method (exact moments not approximate); (4) historical `diagnostics_authorized=false` manifest flag (authorization came from the operator prompt, not manifest mutation).

### 6.4 Supervised-learning task-framing evaluation

Classification vs. regression vs. ordinal; horizon-specific vs. multi-horizon; direction-only vs. magnitude-aware (with explicit treatment of the large short-horizon exact-zero return mass); per-horizon censored-row handling (treated as label-unavailable). Scope complete and admissible; **no framing selected** by Phase 4bm-Z.

### 6.5 Target / horizon admissibility evaluation

1s / 5s / 15s / 60s each discussed separately; **no horizon declared ML-ready; no horizon selected.** 1s / 5s carry explicit latency/tradability caveats; 15s / 60s less latency-sensitive but still not strategy-ready; 60s carries the largest censoring concentration (634 of 857), all in the test split → horizon-availability-by-split is a stated constraint.

### 6.6 Train / validation / test usage evaluation

`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`: train 45d / 74,535,688 rows; validation 30d / 56,819,939 rows; test 15d / 23,797,822 rows; total 90d / 155,153,449 rows. Train/validation usable only in future separately authorized phases; test/final holdout single-use; no test-holdout tuning/design; no shuffle / random / k-fold-over-time / bootstrap / post-hoc resampling; 60s boundary embargo and boundary-crossing exclusion enforced (rows assigned by `source_transact_time_ms` UTC date); split masks not materialized.

### 6.7 Metrics-policy evaluation

Candidate families defined but **not computed**: class balance / prevalence; directional classification; regression error; rank / correlation; calibration; cost-aware descriptive; train/validation stability. No PnL / backtest / strategy metrics. Phase 4bm-Z computes none.

### 6.8 Leakage-controls evaluation

`src_ne_feature_ts = 0` (feature timestamp == label start for every row); no future data in features; no boundary-crossing labels in earlier splits; no test-driven feature/model/threshold decisions; no post-hoc test-based horizon selection; train-only fitting of scalers/imputers/encoders; no validation/test-diagnostic-driven feature engineering unless separately authorized; no manifest mutation as governance substitute (Phase 4aw invariant preserved); censored rows treated as label-unavailable per horizon. Explicit and enforceable.

### 6.9 Baseline-model-family evaluation

Majority / persistence / naive direction; logistic regression; regularized linear; calibrated tree ensembles; shallow gradient boosting; simple probabilistic references. No deep learning unless a later memo justifies it. **No family selected, implemented, or trained.**

### 6.10 Sample-weighting / class-imbalance / calibration evaluation

Sample weighting; class imbalance (incl. exact-zero mass); per-horizon censoring masking; calibration requirement; validation-only calibration; test-holdout calibration-leakage avoidance — all explicitly identified as questions for a future phase; **none answered here.**

### 6.11 Cost-aware evaluation

§11.6 = 8 bps per side / 16 bps round trip restated as a locked, non-loosenable constraint; signal horizon vs. transaction-cost commensurability (esp. 1s / 5s, where dispersion is smallest); latency sensitivity; slippage / spread caveats (no order-book depth in v002). No strategy design, no PnL simulation, no backtests.

### 6.12 Future ML-baseline implementation prerequisites

Future ML-baseline implementation scoping/design phase completed and merged; explicit allowed targets/horizons at design level only; explicit leakage controls accepted and operationalized; explicit metric policy accepted; explicit train/validation/test handling accepted (single-use holdout); explicit cost-aware descriptive policy at the §11.6 lock; explicit non-use of the test holdout for tuning/design; explicit local-output / gitignore storage policy; explicit test-suite and boundary requirements; no unresolved blocking caveat; retained verdicts and project locks preserved.

### 6.13 Future ML-baseline implementation scoping/design boundaries

A future, separately authorized ML-baseline implementation scoping/design phase (provisionally a "Phase 4bn-A"-class phase, **not authorized here**) may evaluate, at design level only: which target framing to implement first; which horizons to include/defer; which train/validation rows are admissible; whether censored rows are excluded per horizon; which baseline families to implement first; which metrics to compute; how train-only transform fitting is enforced; how validation-only evaluation/calibration is handled; how the test holdout remains unused; how cost-aware descriptive evaluation stays non-strategy/non-backtest; how outputs are stored locally and gitignored; what tests are required; what implementation boundaries prevent ML/strategy/backtest drift. It **must not**: train models; score models; generate predictions; select features; rank features; select models through results; tune hyperparameters; tune thresholds; design strategy; generate signals; simulate PnL; run backtests; use the test holdout for tuning/design; materialize reusable split masks unless separately authorized; mutate manifests or successor-state artefacts; or acquire data.

## 7. Local gitignored outputs (if any)

**None produced by Phase 4bm-Z.** Phase 4bm-Z created no local artefact. The pre-existing predecessor local gitignored artefacts were re-hashed read-only and are unchanged (see §9). They remain gitignored and not committed:

- Phase 4bm-W diagnostic outputs under `data/research/microstructure/diagnostics/phase-4bm-w/` — `git check-ignore -v` → `.gitignore:88: data/research/`.
- Phase 4bm-S / Phase 4bm-U successor-state JSONs + sidecars under `data/microstructure/successor-state/labels/` — `.gitignore:85: data/microstructure/`.
- Phase 4bm-Q gate report + sidecar under `data/microstructure/gate-reports/labels/` — `.gitignore:85: data/microstructure/`.

## 8. Validation results

- `git diff --check main..phase-4bm-z/...` → clean (no whitespace errors).
- `git diff --name-status main..phase-4bm-z/...` → `M docs/00-meta/current-project-state.md`; `A …_phase-4bm-z_closeout.md`; `A …_phase-4bm-z_ml-readiness-evaluation-memo.md` (docs only).
- `git diff --stat` for the merge → `3 files changed, 602 insertions(+)`.
- `git status --short` (pre and post merge) → clean working tree; only expected gitignored untracked local outputs (not shown by git).
- `git check-ignore -v data/research/microstructure/diagnostics/phase-4bm-w/descriptive_diagnostics_summary.json` → `.gitignore:88: data/research/`.
- `git check-ignore -v data/research/microstructure/diagnostics/phase-4bm-w/diagnostics_manifest.json` → `.gitignore:88: data/research/`.
- No source / test / script / config changed, so ruff / mypy / pytest were not invoked for this docs-only merge; no source-test/lint/type-check coverage is claimed. No markdown-lint tool is part of the repo standard for these reports; none was invented or run.

## 9. Upstream immutability evidence

Every governed predecessor artefact re-hashed read-only pre-merge and post-merge; all byte-identical (IDENTICAL pre/post):

| Artefact | Expected / pre-merge SHA256 | Post-merge | Result |
| --- | --- | --- | --- |
| `descriptive_diagnostics_summary.json` | `f4b825af2e81734007be06acac5083e2d4048b54b5650bc407d87a6fc246198a` | same | IDENTICAL |
| `descriptive_diagnostics_summary.json.sha256` | `ff52873c983b55cc74a0639d17ea8b3d128cdbee9c77763cd11d2e71b3820473` | same | IDENTICAL |
| `diagnostics_manifest.json` | `ac10061d2f0257002e094d578bcc6149b1a74ca28c604fd0d0a97e5c51c26e45` | same | IDENTICAL |
| `diagnostics_manifest.json.sha256` | `644506e392db46da6d27fa46519cac327136b1a05e350e2d9b231c62fce517eb` | same | IDENTICAL |
| Phase 4bm-U split-policy successor-state JSON | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` | same | IDENTICAL |
| Phase 4bm-U split-policy successor-state sidecar | `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` | same | IDENTICAL |
| Phase 4bm-S research-use successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | same | IDENTICAL |
| Phase 4bm-S research-use successor-state sidecar | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` | same | IDENTICAL |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | same | IDENTICAL |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | same | IDENTICAL |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | IDENTICAL |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | same | IDENTICAL |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | same | IDENTICAL |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | same | IDENTICAL |

## 10. Manifest state preservation

- **v002 label manifest** (`5e17074d…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `chronological_split_policy = "not_yet_defined"`; `label_family_research_use_authorized = false`; `stage_5_label_cleared = false`; `diagnostics_authorized = false` (historical). No transition occurred.
- **v002 feature manifest** (`512a0a54…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false`. No transition occurred.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code modified; no test modified; no committed script modified; no config modified.
- no `.gitignore`, `pyproject.toml`, or `README.md` modified.
- no `data/microstructure/` artefact committed; no `data/research/` artefact committed.
- no manifest mutated; no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no `chronological_split_policy` changed; no `diagnostics_authorized` / `ml_authorized` changed.
- no successor-state artefact mutated (Phase 4bm-S `081730006c…`, Phase 4bm-U `6834ab11…` byte-identical).
- no Phase 4bm-Q gate report mutated (`8a360608…` byte-identical).
- no diagnostics rerun; no diagnostic artefact created.
- no ML model trained; no ML run; no model scored; no predictions generated; no model selected; no features ranked/selected; no hyperparameters tuned; no thresholds tuned.
- no strategy defined or run; no signals generated; no PnL simulated; no backtests run; no walk-forward optimization.
- no split mask created/materialized.
- test holdout not used for tuning or design.
- no data acquired; no public/authenticated/private endpoint called; no Binance API called; no WebSocket / user-stream; no credential / `.env` / `.mcp.json` / MCP / Graphify used.
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

All preserved verbatim. All prior phase results (Phase 4am .. Phase 4bm-Y) preserved verbatim.

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

The Phase 4bm-Z merge does not, and cannot, be construed as authorizing:

- ML implementation, model training, model scoring, prediction generation, feature ranking, feature selection, model selection, hyperparameter tuning, threshold tuning, meta-labeling, or any conversion of labels into signals;
- strategy research, strategy design, signal construction, position state, entry / exit rules, PnL simulation, backtests, or walk-forward optimization;
- diagnostics rerun, diagnostic artefact creation, ML artefact creation, or split-mask materialization;
- use of the test holdout for tuning or design;
- manifest mutation, successor-state mutation, or any `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` transition from this memo alone;
- data acquisition (no additional days / symbols / families beyond the locked 90-day v002 envelope; no mark-price / spot / cross-venue / order-book / additional aggTrades; no 30s / 5m / 30m / 1h / 4h / longer-horizon label generation);
- research execution; paper / shadow / live-readiness / deployment / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSockets / MCP / Graphify / `.mcp.json` / credentials;
- Phase 4 canonical, Phase 5, Phase 4bn-A, any ML-baseline implementation scoping/design phase, or any ML-baseline implementation phase;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m research-thread reopening (Phase 3t closure preserved).

`RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` means only that a future, separately authorized, docs-only or design-only scoping/design phase *may be proposed*. **Any ML-baseline implementation requires a separately authorized implementation phase.**

## 15. Successor authorization

**None.**

Not authorized by this merge:

- Phase 4bn-A — ML-Baseline Implementation Scoping/Design phase (or any phase under any name proposing implementation boundaries)
- any ML-baseline implementation phase
- Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / any further microstructure successor
- Phase 5; Phase 4 canonical
- ML implementation; model training; model scoring; prediction generation; feature ranking/selection; model selection; hyperparameter tuning; threshold tuning
- strategy research / design; signal generation; PnL simulation; backtests; walk-forward optimization
- diagnostics rerun; diagnostic artefact creation; ML artefact creation; split-mask materialization; test-holdout tuning/design
- manifest mutation; successor-state mutation
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot / cross-venue data acquisition
- research execution; paper / shadow; live-readiness; deployment; exchange-write; production keys; authenticated APIs; private endpoints; user stream; WebSockets; MCP; Graphify; `.mcp.json`; credentials

## 16. Recommended state

**Remain paused.**

Phase 4bm-Z is now merge-complete on main and, after the SHA-finalization commit and push, project-complete. The evaluation decision `RECOMMEND_AUTHORIZE_ML_BASELINE_IMPLEMENTATION_SCOPING` authorizes nothing. **Any ML-baseline implementation requires a separately authorized implementation phase.** **Phase 4bn-A is not authorized by Phase 4bm-Z.** **Recommended state remains paused.**

**Conditional next, NOT authorized:** a docs-only or design-only ML-baseline implementation *scoping/design* phase is the cleanest non-paused option. It would propose, at design level only, the exact implementation boundaries for a possible later ML-baseline implementation (target framing, horizon inclusion/deferral, admissible train/validation rows, per-horizon censored-row exclusion, baseline-family ordering, metric set, train-only transform fitting, validation-only calibration, test-holdout protection, cost-aware descriptive policy, local-gitignore storage, test requirements, and anti-drift boundaries) — training, scoring, and predicting nothing. That phase is **not authorized** by this merge.
