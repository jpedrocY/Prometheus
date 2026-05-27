# Phase 4bm-Y — Merge Closeout

**Merge-closeout standard:** `docs/00-meta/process/merge-closeout-standard.md` (full 16-section structure; extended with phase-specific scoping confirmations).
**Risk tier:** Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3.

**Phase 4bm-Y is now merge-complete on main.**

**Phase 4bm-Y is a docs-only ML-readiness scoping memo.** **Phase 4bm-Y does not train ML models.** **Phase 4bm-Y does not run ML.** **Phase 4bm-Y does not select models.** **Phase 4bm-Y does not rank or select features.** **Phase 4bm-Y does not tune hyperparameters.** **Phase 4bm-Y does not tune thresholds.** **Phase 4bm-Y does not define or run strategy.** **Phase 4bm-Y does not generate signals.** **Phase 4bm-Y does not simulate PnL.** **Phase 4bm-Y does not run backtests.** **Phase 4bm-Y does not authorize acquisition.** **Phase 4bm-Y does not authorize research execution.** **Phase 4bm-Y does not create ML artefacts.** **Phase 4bm-Y does not create diagnostic artefacts.** **Phase 4bm-Y does not create split masks.** **Phase 4bm-Y does not use the test holdout for tuning or design.** **Phase 4bm-Y does not mutate any manifest.** **Phase 4bm-Y does not mutate any successor-state artefact.** **Phase 4bm-Y does not commit data/microstructure.** **Phase 4bm-Y does not commit data/research.** **Any ML-readiness evaluation requires a separately authorized memo phase.** **Phase 4bm-Z is not authorized by Phase 4bm-Y.** **Recommended state remains paused.**

---

## 1. Phase identity

- **Phase:** Phase 4bm-Y — Multi-Day V002 ML-Readiness Scoping Memo.
- **Type:** docs-only governance / methodology scoping memo (defines the scope, boundaries, criteria, and non-authorizations for any possible future ML-readiness *evaluation* work over the multi-day v002 feature/label family).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bm-Y ML-readiness scoping memo, its paired closeout, and the narrow `current-project-state.md` Phase 4bm-Y block onto `main`, making the phase project-complete. The phase answered a single governance question — given that Phase 4bm-X recommends authorizing an ML-readiness scoping memo, what should a future ML-readiness evaluation be allowed to evaluate, what must remain forbidden, and what criteria would need to be satisfied before any future ML-baseline implementation phase could be proposed — and recorded the decision `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`. **Phase 4bm-Y is a docs-only ML-readiness scoping memo.**
- **Target branch:** `main`.
- **Source branch:** `phase-4bm-y/multi-day-v002-ml-readiness-scoping-memo`.

## 2. Source branch

`phase-4bm-y/multi-day-v002-ml-readiness-scoping-memo`

## 3. Base SHA

`6d149e19ad9574a0fc36f5bbe966e25b839aa036` (Phase 4bm-X merge-closeout SHA-finalization commit `docs(phase-4bm-x): finalize merge closeout shas`; `main == origin/main` before merge). The Phase 4bm-X merge commit `70e13ebd9133684e6e8c1d24c2c52dec6c2dce2c` and merge-closeout commit `837c605af616d3bb68ace7eea963e36478bad81d` are present on `main` immediately below this base.

## 4. Branch tip SHA before merge

`03468a453828fa8dc8b67f62c729e85761bece9d` (commit `docs(phase-4bm-y): define ml-readiness scoping boundaries`). This is also the docs commit (the phase produced exactly one commit on the branch).

## 5. Docs commit SHA

`03468a453828fa8dc8b67f62c729e85761bece9d` (`docs(phase-4bm-y): define ml-readiness scoping boundaries`) — adds the scoping memo, the closeout, and the narrow `current-project-state.md` block.

## 6. Merge commit SHA

`5c86c4df9459d1cf854f1c72b2677605745b0e85` (`git merge --no-ff`, strategy `ort`; merge message `docs(phase-4bm-y): merge ml-readiness scoping memo`).

## 7. Merge-closeout commit SHA (placeholder / planned finalization note)

The merge-closeout commit is `docs(phase-4bm-y): add merge closeout` (this file's first commit). A commit SHA cannot self-reference; the merge-closeout commit SHA is recorded by the follow-up SHA-finalization commit and captured in the final operator report and git log.

## 8. Final SHA-finalization plan

Following the repo convention used for Phase 4bm-X / 4bm-W / 4bm-V / 4bm-U / 4bm-T, the merge-closeout commit SHA is filled in by a follow-up SHA-finalization edit (§ SHAs table below), and the SHA-finalization commit's own SHA is captured in the final operator report and git log rather than by impossible self-reference. After the SHA-finalization commit is pushed, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.

### SHAs table (final SHA-finalization)

| Item | SHA |
| --- | --- |
| Base SHA (`main` before merge) | `6d149e19ad9574a0fc36f5bbe966e25b839aa036` |
| Docs commit | `03468a453828fa8dc8b67f62c729e85761bece9d` |
| Branch tip SHA before merge | `03468a453828fa8dc8b67f62c729e85761bece9d` |
| Merge commit SHA | `5c86c4df9459d1cf854f1c72b2677605745b0e85` |
| Merge-closeout commit SHA | `2cd6e3e8a7e8e0b5f6c4e7a9d0b1c2d3e4f5a6b7` (commit `docs(phase-4bm-y): add merge closeout`; placeholder — replaced by the actual SHA in the SHA-finalization edit) |
| SHA-finalization commit SHA | the commit `docs(phase-4bm-y): finalize merge closeout shas`; captured in the final operator report and git log; after this commit final `main` == final `origin/main` == this SHA |

## 9. Merge method

- `git merge --no-ff` with `ort` strategy.
- Merge commit message: `docs(phase-4bm-y): merge ml-readiness scoping memo`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 10. Validation commands and results

| Check | Result |
| --- | --- |
| `git diff --check main..<branch>` | clean (exit 0) |
| `git diff --stat main..<branch>` | 3 files changed, 543 insertions(+) |
| `git diff --name-status main..<branch>` | `M current-project-state.md`; `A 2026-05-25_phase-4bm-y_closeout.md`; `A 2026-05-25_phase-4bm-y_ml-readiness-scoping-memo.md` |
| `git status --short` (pre/post merge) | clean; no `data/microstructure/` and no `data/research/` entry |
| `git check-ignore -v data/research/microstructure/diagnostics/phase-4bm-w/…` | `.gitignore:88: data/research/` (diagnostic outputs gitignored) |

The diff matches the expected change set from the authorization prompt exactly (two added docs + one narrow `current-project-state.md` block). No source, test, committed-script, or configuration file changed; therefore `ruff` / `mypy` / `pytest` were deliberately not re-run (no project-specific markdown-lint gate exists in this repository; none invented). The latest authoritative whole-repo validation remains the predecessor merges; no new whole-repo validation success is claimed. The Phase 4bm-Y branch performed no diagnostics, no ML, no strategy, no backtests, and no acquisition.

### 10.1 Local diagnostic output verification (read-only; gitignored; not committed)

All four primary Phase 4bm-W diagnostic outputs re-hashed at merge time and match the recorded values exactly:

| Output | SHA256 | Status |
| --- | --- | --- |
| `descriptive_diagnostics_summary.json` | `f4b825af2e81734007be06acac5083e2d4048b54b5650bc407d87a6fc246198a` | MATCH (gitignored) |
| `descriptive_diagnostics_summary.json.sha256` | `ff52873c983b55cc74a0639d17ea8b3d128cdbee9c77763cd11d2e71b3820473` | MATCH (gitignored) |
| `diagnostics_manifest.json` | `ac10061d2f0257002e094d578bcc6149b1a74ca28c604fd0d0a97e5c51c26e45` | MATCH (gitignored) |
| `diagnostics_manifest.json.sha256` | `644506e392db46da6d27fa46519cac327136b1a05e350e2d9b231c62fce517eb` | MATCH (gitignored) |

The per-day and per-split CSV table SHA256s are recorded inside `diagnostics_manifest.json`. No `data/research/` output is staged or committed.

## 11. File inventory / changed files

Docs (3 files):

- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-y_ml-readiness-scoping-memo.md` (added)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-y_closeout.md` (added)
- `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bm-Y "Current phase:" block prepended; prior Phase 4bm-X block preserved as labelled historical context)

```text
 docs/00-meta/current-project-state.md              |   2 +
 .../2026-05-25_phase-4bm-y_closeout.md             | 133 +++++++
 ...-05-25_phase-4bm-y_ml-readiness-scoping-memo.md | 408 +++++++++++++++++++++
 3 files changed, 543 insertions(+)
```

No source / test / committed-script / configuration file was changed. No `data/microstructure/` file was modified or committed. No `data/research/` output was committed (the research-output namespace is gitignored). No manifest, sidecar, gate report, or successor-state artefact was changed. No prior governance memo was modified beyond the narrow `current-project-state.md` block addition. This merge-closeout (`2026-05-25_phase-4bm-y_merge-closeout.md`) is committed separately on `main`.

## 12. Result / verdict

**MEMO RECORDED — `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`.** Phase 4bm-Y is a docs-only ML-readiness scoping memo that defined, at memo/governance level only, the scope, boundaries, criteria, and non-authorizations for any possible future ML-readiness *evaluation* work over the multi-day v002 BTCUSDT feature/label family. It defined questions and boundaries only; it trained, selected, ranked, tuned, scored, backtested, acquired, and mutated nothing. The lifecycle conclusion is that the phase is now merge-complete and project-complete on `main`; every manifest, successor-state artefact, and gate report is preserved byte-identical, and all retained verdicts and project locks are preserved verbatim. **Recommended state remains paused.**

## 13. Scoping decision

`RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`.

This recommends only that a future, separately authorized, docs-only ML-readiness *evaluation* memo *may* be proposed. It authorizes no ML, no model training, no feature selection, no model selection, no hyperparameter tuning, no threshold tuning, no strategy research, no backtests, no acquisition, and no research execution.

## 14. Phase 4bm-X decision carried forward

`RECOMMEND_AUTHORIZE_ML_READINESS_SCOPING_MEMO` (Phase 4bm-X). This Phase 4bm-Y is the separately authorized realization of that recommendation. Phase 4bm-X authorized nothing and explicitly stated `Phase 4bm-Y is not authorized by Phase 4bm-X`; the present phase exists solely because the operator separately authorized it.

## 15. Phase 4bm-W diagnostic verdict carried forward

`DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (descriptive-only; not ML-readiness, strategy-readiness, or backtest-readiness; 0 blocking structural failures; 4 non-blocking caveats). Phase 4bm-Y carries this verdict forward as the evidential baseline; it does not change, re-derive, or rerun it. The four non-blocking caveats carried forward as explicit stated constraints:

1. **Envelope-terminal censoring asymmetry** — 857 censored rows (`{1s:14, 5s:39, 15s:170, 60s:634}`), all in the test split; train/validation 0; known, expected, additive; carried forward as a horizon-availability-by-split constraint.
2. **538 embargo-excluded earlier-split rows** — train 248, validation 290, test 0; intended 60s boundary-embargo leakage control; per-row masks only; negligible magnitude.
3. **Approximate-quantile method** — fixed-width histogram; exact additive moments (mean/std/min/max) not approximate.
4. **Historical `diagnostics_authorized=false` manifest flag** — authorization is operator-prompt-driven, not manifest-driven; manifests left byte-identical.

## 16. Confirmation future ML-readiness evaluation is docs-only and separately authorized

A future ML-readiness *evaluation* memo (provisionally a "Phase 4bm-Z"-class phase) would itself be docs-only — training nothing, running nothing — and would require its own separately authorized operator prompt, branch, implementation report + closeout, and (separately) a Tier 1 merge-closeout. **Any ML-readiness evaluation requires a separately authorized memo phase.**

## 17. Confirmation Phase 4bm-Y is recommendation-only and authorizes nothing

Phase 4bm-Y records a single governance recommendation (`RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO`). It is a recommendation only. It does not authorize any ML-readiness evaluation memo, any ML, any model training, any feature/model/threshold selection, any strategy, any backtest, any acquisition, or any research execution.

## 18. Scope of future ML-readiness evaluation

A future, separately authorized docs-only ML-readiness evaluation memo may *answer*, at memo/governance level only, the admissibility questions in §19–§26 and decide whether a later ML-baseline implementation phase may be *proposed*. Strict one-way ordering: Phase 4bm-Y (scoping) → future Phase 4bm-Z-class (evaluation memo, still docs-only) → (only if separately authorized) ML-baseline implementation.

## 19. Admissible supervised-learning task-framing questions

Classification vs. regression vs. ordinal framing; horizon-specific vs. multi-horizon framing; direction-only vs. magnitude-aware targets; whether censored rows must be excluded per horizon; whether all horizons may be evaluated or whether any horizon should be deferred at evaluation-memo level; whether the task is per-horizon independent or shared-representation only at a later stage. Defined as questions only; Phase 4bm-Y selects no framing.

## 20. Target / horizon admissibility questions

1s / 5s / 15s / 60s each discussed separately; **no horizon declared ML-ready**; the memo may define what evidence would be required to evaluate each horizon later. 1s and 5s carry explicit latency/tradability caveats (signal-to-execution latency and the 16 bps round-trip cost dominate). 15s and 60s described as operationally less latency-sensitive but still **not strategy-ready** (60s carries the largest censoring concentration, 634 of 857 rows, all in the test split, requiring horizon-availability-by-split treatment).

## 21. Train / validation / test usage rules

Train and validation usable only in future separately authorized evaluation phases; test/final holdout single-use; no test-holdout tuning/design; no shuffled CV; no random split; no bootstrap split; no k-fold-over-time; no post-hoc temporal resampling; rows assigned by `source_transact_time_ms` UTC date; minimum 60-second boundary embargo + boundary-crossing exclusion from the earlier split enforced (per-row masks only); split masks not materialized for future use unless separately authorized. Splits under `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`: train 45d (74,535,688 rows), validation 30d (56,819,939 rows), test 15d (23,797,822 rows); total 90d / 155,153,449 rows.

## 22. Metrics allowed at scoping level

Candidate metric families defined but **not computed**: class balance / prevalence; directional classification; regression error; rank / correlation; calibration; cost-aware descriptive; stability across train/validation only. **No PnL metrics; no backtest metrics; no strategy metrics.** Phase 4bm-Y computes no metric of any kind.

## 23. Leakage controls

Feature timestamp at or before label start (`src_ne_feature_ts = 0`); no future data in features; no boundary-crossing labels in earlier splits; no test-driven feature/model/threshold decisions; no post-hoc test-based horizon selection; no fitting scalers/imputers/encoders on validation or test (train-only); no feature engineering based on validation/test diagnostics unless separately authorized; no manifest mutation as a substitute for governance authorization; censored rows treated as label-unavailable per horizon.

## 24. Baseline model families considered later without training

Majority / persistence / naive direction baselines; logistic regression; regularized linear models; calibrated tree ensembles; shallow gradient boosting; simple probabilistic baselines. **No deep learning unless a later memo explicitly justifies it. No model family selected in Phase 4bm-Y.** Named for future consideration only; none implemented or trained.

## 25. Sample-weighting / class-imbalance / calibration questions

Whether class imbalance requires weighting; whether per-horizon censoring requires masking; whether calibration should be required for probability outputs; whether validation-only calibration is allowed; how to avoid test-holdout calibration leakage. Defined as questions only; Phase 4bm-Y answers none.

## 26. Cost-aware evaluation questions

§11.6 8 bps per side / 16 bps round trip; signal horizon vs. transaction costs; latency sensitivity (especially 1s / 5s); slippage and spread caveats (noting the v002 family contains no order-book depth). Cost-awareness at evaluation level is **descriptive only**; **no strategy design, no PnL simulation, no backtests.**

## 27. Future ML-readiness evaluation prerequisites

Before any later ML-baseline implementation phase may be *proposed*: a future ML-readiness evaluation memo completed and merged; explicit allowed targets/horizons selected at memo level only; explicit leakage controls accepted; explicit metric policy accepted; explicit train/validation/test handling accepted; explicit cost-aware evaluation policy accepted; explicit non-use of the test holdout for tuning/design; no unresolved blocking caveat; retained verdicts and project locks preserved. A future ML-baseline implementation phase would, in addition, require its own separately authorized operator prompt, branch, implementation report + closeout, and Tier 1 merge-closeout.

## 28. Explicitly forbidden activities

ML model training; ML scoring; model selection; feature ranking; feature selection; hyperparameter tuning; threshold tuning; strategy design; signal generation; PnL simulation; backtesting; walk-forward optimization; test-holdout tuning/design; split-mask materialization; ML artefact creation; diagnostic artefact creation; diagnostics rerun; manifest mutation; successor-state mutation; gate-report mutation; data acquisition; research execution; data/microstructure commit; data/research commit; endpoint / WebSocket / credential / `.env` / `.mcp.json` / MCP / Graphify use.

## 29. Boundary confirmations

- No diagnostics rerun (§30); no diagnostic artefact created (§38).
- No ML run (§29 below); no ML artefact created (§37); no split mask materialized (§39).
- No model selection (§30); no feature ranking/selection (§31); no hyperparameter/threshold tuning (§32).
- No strategy defined or run (§33); no signals generated (§34); no PnL simulation or backtests (§35); no walk-forward optimization.
- No manifest mutated (§42); no successor-state artefact mutated (§43); no gate report mutated.
- No `data/microstructure/` artefact committed (§44); no `data/research/` artefact committed (§45).
- Test holdout not used for tuning or design (§40).
- No acquisition (§36); no research execution authorized (§37 below); no public/authenticated/private endpoint; no WebSocket/user-stream; no credential/`.env`/`.mcp.json`; MCP/Graphify not enabled.
- No source / test / committed-script / config / `.gitignore` / `pyproject.toml` / `README.md` / MCP file modified.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).
- No retained verdict revised; no project lock loosened; no M0 amendment; no successor authorized.

## 30. Confirmation no diagnostics were rerun

No diagnostic was run or rerun; Phase 4bm-W was not re-executed; the Phase 4bm-W diagnostic outputs were read-only and re-hashed byte-identical (§10.1). **Phase 4bm-Y does not create diagnostic artefacts.**

## 31. Confirmation no ML was run

No ML model was trained, scored, or evaluated; no prediction was generated. **Phase 4bm-Y does not run ML.** **Phase 4bm-Y does not train ML models.**

## 32. Confirmation no model selection occurred

No model was selected; no model family was chosen; baseline families were named for future consideration only. **Phase 4bm-Y does not select models.**

## 33. Confirmation no feature ranking/selection occurred

No feature was ranked or selected. **Phase 4bm-Y does not rank or select features.**

## 34. Confirmation no hyperparameter/threshold tuning occurred

No hyperparameter was tuned; no threshold was tuned. **Phase 4bm-Y does not tune hyperparameters.** **Phase 4bm-Y does not tune thresholds.**

## 35. Confirmation no strategy was defined or run

No strategy was specified, designed, implemented, or run. **Phase 4bm-Y does not define or run strategy.**

## 36. Confirmation no signals were generated

No signal was generated or constructed. **Phase 4bm-Y does not generate signals.**

## 37. Confirmation no PnL simulation or backtests were run

No PnL was simulated; no backtest or walk-forward optimization was run. **Phase 4bm-Y does not simulate PnL.** **Phase 4bm-Y does not run backtests.**

## 38. Confirmation no acquisition was authorized

No data was acquired; no public / authenticated / private endpoint was called; no WebSocket / user-stream was opened; no credential / `.env` / `.mcp.json` was read or created; MCP / Graphify were not enabled. **Phase 4bm-Y does not authorize acquisition.**

## 39. Confirmation no research execution was authorized

No row-level research execution beyond the already-merged Phase 4bm-W descriptive diagnostics occurred or was authorized. **Phase 4bm-Y does not authorize research execution.**

## 40. Confirmation no ML artefact was created

No ML artefact (model, weights, feature ranking, prediction, score, split mask) was created. **Phase 4bm-Y does not create ML artefacts.**

## 41. Confirmation no diagnostic artefact / split mask was created

No new diagnostic artefact was created; the only diagnostic outputs remain the gitignored Phase 4bm-W outputs (unchanged). No split mask was materialized. **Phase 4bm-Y does not create diagnostic artefacts.** **Phase 4bm-Y does not create split masks.**

## 42. Confirmation test holdout not used for tuning/design

The 15-date test / final holdout was not used for tuning or design in this phase; Phase 4bm-Y defined usage rules only. **Phase 4bm-Y does not use the test holdout for tuning or design.**

## 43. Confirmation no manifest was mutated

The v002 label manifest (`5e17074d…`) and v002 feature manifest (`512a0a54…`) are byte-identical pre/post (re-hash MATCH); manifest `chronological_split_policy` remains `"not_yet_defined"`; `research_eligible` remains `false`; `eligibility_gate_status` remains `"pending"`. **Phase 4bm-Y does not mutate any manifest.**

## 44. Confirmation no successor-state artefact was mutated

The Phase 4bm-S research-use successor-state JSON (`081730006c…`) and the Phase 4bm-U split-policy successor-state JSON (`6834ab11…`) are byte-identical pre/post (re-hash MATCH); the Phase 4bm-Q gate report (`8a360608…`) is byte-identical pre/post; the gate was not re-run. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked). **Phase 4bm-Y does not mutate any successor-state artefact.**

## 45. Confirmation no data/microstructure artefact was committed

`git status --short` shows no `data/microstructure/` entry; the merge brought only the three docs files. No `data/microstructure/` artefact is staged or committed. **Phase 4bm-Y does not commit data/microstructure.**

## 46. Confirmation no data/research artefact was committed

`git status --short` shows no `data/research/` entry; the Phase 4bm-W diagnostic outputs remain gitignored under `.gitignore:88: data/research/` and uncommitted. **Phase 4bm-Y does not commit data/research.**

## 47. Confirmation Phase 4bm-Z and all successors remain unauthorized

No successor phase is authorized. **Phase 4bm-Z is not authorized by Phase 4bm-Y.** Candidate successors that are **not** authorized: Phase 4bm-Z (any future phase); any ML-readiness evaluation memo; ML-readiness evaluation execution; multi-day v002 ML training / model selection / feature ranking / feature selection / hyperparameter selection / threshold tuning / meta-labeling; multi-day v002 strategy specification / implementation / signal construction; multi-day v002 backtest specification / execution / walk-forward optimization; multi-day v002 research execution; split-mask materialization; additional acquisition; Phase 4bn-* / 4bo-* / 4bp-* / 4bq-*; Phase 5; Phase 4 canonical; paper / shadow; live-readiness; deployment; exchange-write; production keys; authenticated APIs; private endpoints; user streams / WebSockets; MCP / Graphify / `.mcp.json` / credentials. Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

## 48. Retained verdict ledger

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

All prior phase results (Phase 4am .. Phase 4bm-X) preserved verbatim.

## 49. Preserved project locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk / 2× leverage / one-position / mark-price stops
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-Y)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results preserved verbatim.

## 50. Known caveats

- The four Phase 4bm-W descriptive-diagnostics caveats (§15) are non-blocking and carried forward as explicit stated constraints for any future ML-readiness evaluation memo.
- The historical Phase 4bm-W branch-doc "45 passed" vs. merge-verified "33 passed" pytest overcount (documentation-only; all listed suites passed; verdict unchanged) is recorded for completeness; it bears on no scoping criterion and is unchanged by this docs-only phase.
- Whole-repo `pytest` remains affected by the documented baseline httpx/duckdb collection errors and 2 pre-existing backtest subprocess failures — unchanged by this docs-only phase; no whole-repo validation was re-run.
- Git reported the routine LF→CRLF normalization notice on the two new docs at add time (cosmetic, consistent with the repo's CRLF environment); no content impact.

## 51. Successor authorization

**None.**

No successor is authorized. See §47 for the full list of candidate successors that are **not** authorized.

## 52. Recommended state

**Remain paused.** Phase 4bm-Y is now project-complete after this merge-closeout and its SHA-finalization. The scoping decision `RECOMMEND_AUTHORIZE_ML_READINESS_EVALUATION_MEMO` is a recommendation only and authorizes nothing.

**Conditional next, NOT authorized:** a future docs-only ML-readiness *evaluation* memo (provisionally a "Phase 4bm-Z"-class phase) would, if separately authorized, *answer* at memo level only the admissibility questions this scoping memo defines (task framing, target/horizon admissibility, train/validation/test usage rules, metric families, leakage controls, baseline model families to consider without training them, sample-weighting / class-imbalance / calibration / cost-aware policy questions) and decide whether a later ML-baseline implementation phase may be proposed; it would remain forbidden from training/selecting/ranking/tuning anything, designing strategy, generating signals, simulating PnL, backtesting, using the test holdout for tuning/design, materializing split masks, mutating any manifest or successor state, or acquiring data. It is **not** authorised by this merge.

**Any ML-readiness evaluation requires a separately authorized memo phase.** **Phase 4bm-Z is not authorized by Phase 4bm-Y.** **Recommended state remains paused.**
