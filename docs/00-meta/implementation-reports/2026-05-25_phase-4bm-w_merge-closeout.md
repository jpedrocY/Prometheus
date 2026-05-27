# Phase 4bm-W — Merge Closeout

**Merge-closeout standard:** `docs/00-meta/process/merge-closeout-standard.md` (full 16-section structure).
**Risk tier:** Tier 1 — Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` §3.

**Phase 4bm-W is now merge-complete on main.**

**Phase 4bm-W runs descriptive diagnostics only.** **Phase 4bm-W does not run ML.** **Phase 4bm-W does not define or run strategy.** **Phase 4bm-W does not run backtests.** **Phase 4bm-W does not authorize acquisition.** **Phase 4bm-W does not authorize research execution beyond the scoped descriptive diagnostics.** **Phase 4bm-W does not perform feature selection.** **Phase 4bm-W does not perform model selection.** **Phase 4bm-W does not perform threshold tuning.** **Phase 4bm-W does not use the test holdout for tuning or design.** **Phase 4bm-W does not mutate any manifest.** **Phase 4bm-W does not mutate any successor-state artefact.** **Phase 4bm-W does not commit data/microstructure.** **Phase 4bm-X is not authorized by Phase 4bm-W.** **Recommended state remains paused.**

---

## 1. Phase identity

- **Phase:** Phase 4bm-W — Multi-Day V002 Descriptive Diagnostics Execution.
- **Type:** code + tests + docs + local gitignored diagnostic outputs (the first actual descriptive/structural diagnostics execution for the research-use-approved-in-principle multi-day v002 feature/label family).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bm-W descriptive diagnostics implementation (three new source modules, one runner script, three test modules), the narrow `.gitignore` `data/research/` addition, the implementation report, the closeout, and the narrow `current-project-state.md` Phase 4bm-W block onto `main`, making the phase project-complete. The phase implemented and executed strictly descriptive / structural diagnostics over the 90-day v002 BTCUSDT feature/label family, applying the Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` split policy, and produced local gitignored diagnostic outputs only. **Phase 4bm-W runs descriptive diagnostics only.**
- **Target branch:** `main`.
- **Source branch:** `phase-4bm-w/multi-day-v002-descriptive-diagnostics`.

## 2. SHAs

- **`main` SHA before merge:** `348d8a34f45b8d3b5e1caa19ab8e0064a9015474` (Phase 4bm-V SHA-finalization commit; `main == origin/main` before merge).
- **Branch tip SHA before merge:** `440b149aac010be8fdb254613683301f27c19be7` (commit `docs(phase-4bm-w): record descriptive diagnostics results`).
- **Code / tests / script / `.gitignore` commit SHA:** `7101357de4f2bf760e2f40c65f36e2ad9f79b59b` (commit `feat(phase-4bm-w): add multi-day v002 descriptive diagnostics`).
- **Docs commit SHA:** `440b149aac010be8fdb254613683301f27c19be7` (commit `docs(phase-4bm-w): record descriptive diagnostics results`).
- **Merge commit SHA:** `cd8913a273c030dd5a2e6e5e5eeab142fd1ffda4` (`git merge --no-ff`, strategy `ort`).
- **Merge-closeout commit SHA:** the commit `docs(phase-4bm-w): add merge closeout` (this file's first commit). The closeout commit SHA cannot self-reference; it is recorded by the follow-up SHA-finalization commit and captured in the final operator report and git log.
- **SHA-finalization commit SHA:** the commit `docs(phase-4bm-w): finalize merge closeout shas` (the finalization edit); captured in the final operator report and in git log rather than by impossible self-reference. After this commit is pushed, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.

### SHAs section (final SHA-finalization plan)

| Item | SHA |
| --- | --- |
| Base SHA (`main` before merge) | `348d8a34f45b8d3b5e1caa19ab8e0064a9015474` |
| Branch tip SHA before merge | `440b149aac010be8fdb254613683301f27c19be7` |
| Code / tests / script / `.gitignore` commit | `7101357de4f2bf760e2f40c65f36e2ad9f79b59b` |
| Docs commit | `440b149aac010be8fdb254613683301f27c19be7` |
| Merge commit SHA | `cd8913a273c030dd5a2e6e5e5eeab142fd1ffda4` |
| Merge-closeout commit SHA | `da76f8e07f2cfe6f74816cbc3892ee100bc7b94f` (commit `docs(phase-4bm-w): add merge closeout`) |
| SHA-finalization commit SHA | the commit `docs(phase-4bm-w): finalize merge closeout shas`; captured in the final operator report and git log; after this commit final `main` == final `origin/main` == this SHA |

**SHA-finalization plan:** following the repo convention used for Phase 4bm-V / 4bm-U / 4bm-T, the merge-closeout commit SHA is filled in by a follow-up SHA-finalization edit (this section), and the SHA-finalization commit's own SHA is captured in the final operator report and git log rather than by impossible self-reference. After the SHA-finalization commit is pushed, final `main` SHA == final `origin/main` SHA == the SHA-finalization commit.

## 3. Merge method

- `git merge --no-ff phase-4bm-w/multi-day-v002-descriptive-diagnostics` with `ort` strategy (default).
- Merge commit message: `feat(phase-4bm-w): merge descriptive diagnostics`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No force-push.
- Push status: Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Source (3 files, added):

- `src/prometheus/research/microstructure/diagnostics_split_policy_v002.py`
- `src/prometheus/research/microstructure/descriptive_diagnostics_v002.py`
- `src/prometheus/research/microstructure/diagnostics_report_v002.py`

Scripts (1 file, added):

- `scripts/phase4bm_w_run_descriptive_diagnostics.py`

Tests (3 files, added):

- `tests/research/microstructure/test_diagnostics_split_policy_v002.py`
- `tests/research/microstructure/test_descriptive_diagnostics_v002.py`
- `tests/research/microstructure/test_diagnostics_no_network.py`

Config (1 file, modified):

- `.gitignore` (narrow addition of `data/research/` only — the gitignored research-output namespace)

Docs (3 files):

- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-w_multi-day-v002-descriptive-diagnostics.md` (added)
- `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-w_closeout.md` (added)
- `docs/00-meta/current-project-state.md` (modified — narrow Phase 4bm-W "Current phase:" block prepended; prior Phase 4bm-V block preserved as labelled historical context)

No `data/microstructure/` file was modified by the merge. No `data/research/` output was committed by the merge (the research-output namespace is gitignored). No prior governance memo was modified beyond the narrow `current-project-state.md` block addition. No prior source / test / script was modified. This merge-closeout (`2026-05-25_phase-4bm-w_merge-closeout.md`) is committed separately on `main`.

## 5. Diff summary

```text
 .gitignore                                         |   3 +
 docs/00-meta/current-project-state.md              |   2 +
 .../2026-05-25_phase-4bm-w_closeout.md             | 114 ++++
 ...4bm-w_multi-day-v002-descriptive-diagnostics.md | 212 +++++++
 scripts/phase4bm_w_run_descriptive_diagnostics.py  | 166 +++++
 .../microstructure/descriptive_diagnostics_v002.py | 679 +++++++++++++++++++++
 .../microstructure/diagnostics_report_v002.py      | 644 +++++++++++++++++++
 .../diagnostics_split_policy_v002.py               | 298 +++++++++
 .../test_descriptive_diagnostics_v002.py           | 345 +++++++++++
 .../microstructure/test_diagnostics_no_network.py  | 112 ++++
 .../test_diagnostics_split_policy_v002.py          | 133 ++++
 11 files changed, 2708 insertions(+)
```

The diff matches the expected change set from the authorization prompt exactly: 9 added files (3 source modules, 1 script, 3 tests, 2 docs) and 2 modifications (`.gitignore` narrow `data/research/` addition; `current-project-state.md` narrow block). `git diff --check main..<branch>` clean (exit 0).

## 6. Verdict

**LOCAL ARTEFACT PRODUCED — DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS (descriptive-only).**

Phase 4bm-W implemented and executed strictly descriptive / structural diagnostics over the multi-day v002 BTCUSDT feature/label family (`microstructure_labels_aggtrades_v001 @ v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; horizons 1s / 5s / 15s / 60s), applying the Phase 4bm-U recorded chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`. The diagnostic verdict is `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`: **0 blocking structural failures** and **4 non-blocking caveats**. The verdict is descriptive-only and is **not** an ML-readiness, strategy-readiness, or backtest-readiness signal. Lifecycle state: Phase 4bm-W is now merge-complete and project-complete on `main` after this merge-closeout and its SHA-finalization. The v002 label manifest's `chronological_split_policy` remains `"not_yet_defined"` (the recorded policy lives only in the Phase 4bm-U sibling successor-state JSON); all manifest / successor-state / gate-report artefacts are preserved byte-identically; all diagnostic outputs are local gitignored and uncommitted. **Recommended state remains paused.**

### 6.1 Diagnostic groups executed

A dataset/split inventory; B label availability and censoring; C label distribution (descriptive only); D feature/label alignment; E per-day and per-split stability; F boundary-embargo and leakage-guard; G missingness / nullability / value-domain; H report-only QA summaries.

### 6.2 Split-policy / embargo summary

Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` applied verbatim; rows assigned by `source_transact_time_ms` UTC date. Train 2024-12-01..2025-01-14 (45 dates; 74,535,688 rows); Validation 2025-01-15..2025-02-13 (30 dates; 56,819,939 rows); Test/final holdout 2025-02-14..2025-02-28 (15 dates; 23,797,822 rows); observed total 155,153,449 (= expected); label 90/90 + feature 90/90 parquet/sidecar counts. Minimum 60s boundary embargo at `T_TV = 2025-01-15T00:00:00Z` (1736899200000 ms; train embargo 248) and `T_VT = 2025-02-14T00:00:00Z` (1739491200000 ms; validation embargo 290); total **538** embargo-excluded earlier-split rows (test 0). Boundary-crossing rows excluded from the earlier split only (per-row masks; no parquet rewrite). No shuffle / random / bootstrap / k-fold-over-time / post-hoc resampling. `out_of_partition_day = 0` and `split_assignment_mismatch = 0`.

### 6.3 Label availability / censoring summary

Per-horizon censored counts observed `{1s:14, 5s:39, 15s:170, 60s:634}` exactly match the recorded v002 manifest expectation; total 857, **all in the test split** (envelope terminal `1740787199996` ms = 2025-02-28T23:59:59.996Z; train/validation 0). Censored-row null discipline holds (null forward-return count equals censored count per split×horizon; `censored_row_not_null = 0`); `label_any_censored_flag == OR(horizon_censored_flag_*)` everywhere (`any_censored_flag_mismatch = 0`); `invalid_price_row_count = 0`.

### 6.4 Label distribution summary

Forward-log-return exact additive moments (mean/std/min/max) and direction balance recorded per split×horizon (descriptive only; never used for selection/tuning/design). std grows monotonically with horizon within each split; zero-return mass shrinks with horizon. Quantiles are approximate (fixed-width histogram). Full per-split×horizon table in the summary JSON and `per_split_horizon_summary.csv`.

### 6.5 Feature/label alignment summary

Over all 90 days: `row_count_mismatch_days = 0`, `row_index_mismatch = 0`, `agg_trade_id_mismatch = 0`, `feature_timestamp_mismatch = 0`, `source_transact_time_mismatch = 0`, `feature_config_hash_mismatch_days = 0`. Strict 1:1 row alignment (155,153,449 each; per-day parity); `source_transact_time_ms == feature_timestamp_ms` for all rows; feature `feature_config_hash` constant (`819cfa7a…`); label `label_config_hash` constant (`352bad41…`).

### 6.6 Per-day / per-split stability summary

Per-day row counts vary (no zero-row day); per-day censoring zero on every non-final day and concentrated entirely on 2025-02-28; missingness equals censoring. All structural counters aggregate to 0.

### 6.7 Missingness / value-domain summary

`forward_direction_H ∈ {-1,0,+1,null}` on all rows (`direction_domain_violation = 0`); `direction_sign_mismatch_vs_return = 0`; `horizon_censored_flag_H == (source_transact_time_ms + H_ms > envelope_terminal_unix_ms)` on all rows (`censor_rule_mismatch = 0`); contiguous `row_index 0..n-1` (`row_index_violation = 0`); symbol / dataset_version / label_config_hash constancy holds.

## 7. Local gitignored outputs

Produced by Phase 4bm-W under `data/research/microstructure/diagnostics/phase-4bm-w/` (gitignored via `.gitignore:88: data/research/`; **not committed**):

| Output | SHA256 | Status |
| --- | --- | --- |
| `descriptive_diagnostics_summary.json` | `f4b825af2e81734007be06acac5083e2d4048b54b5650bc407d87a6fc246198a` | gitignored; not committed |
| `descriptive_diagnostics_summary.json.sha256` | `ff52873c983b55cc74a0639d17ea8b3d128cdbee9c77763cd11d2e71b3820473` | gitignored; not committed |
| `diagnostics_manifest.json` | `ac10061d2f0257002e094d578bcc6149b1a74ca28c604fd0d0a97e5c51c26e45` | gitignored; not committed |
| `diagnostics_manifest.json.sha256` | `644506e392db46da6d27fa46519cac327136b1a05e350e2d9b231c62fce517eb` | gitignored; not committed |
| `descriptive_diagnostics_tables/per_day_inventory.csv` | (recorded inside `diagnostics_manifest.json`) | gitignored; not committed |
| `descriptive_diagnostics_tables/per_split_horizon_summary.csv` | (recorded inside `diagnostics_manifest.json`) | gitignored; not committed |

`git check-ignore -v data/research/microstructure/diagnostics/phase-4bm-w/descriptive_diagnostics_summary.json` → `.gitignore:88: data/research/`. `git check-ignore -v …/diagnostics_manifest.json` → `.gitignore:88: data/research/`. All four primary output SHA256s re-verified at merge time and match the Phase 4bm-W closeout exactly. The two CSV table SHA256s are recorded inside `diagnostics_manifest.json`. No `data/research/` output is staged or committed.

## 8. Validation results

| Check | Result |
| --- | --- |
| `pytest test_descriptive_diagnostics_v002.py + test_diagnostics_split_policy_v002.py + test_diagnostics_no_network.py` | **33 passed** |
| `pytest test_import_boundaries.py` | **63 passed** (auto-scans the three new modules; no forbidden imports/tokens) |
| `ruff check src/prometheus/research/microstructure scripts tests/research/microstructure` | **All checks passed** |
| `mypy` on the three new modules | **Success: no issues found in 3 source files** |
| `mypy src/prometheus/research/microstructure` (whole package) | 2 errors, both in **pre-existing** files (`labels_manifest_v002.py:370`, `multiday_feature_gate_checks.py:847`); **0** in the three new files |
| `git diff --check main..<branch>` | clean (exit 0) |
| `git status --short` (post-merge) | clean (no `data/microstructure/` and no `data/research/` entry; `data/research/` ignored via merged `.gitignore:88`) |
| `git check-ignore -v data/research/microstructure/diagnostics/phase-4bm-w/…` | `.gitignore:88: data/research/` |

**Documentation discrepancy (non-blocking; count only):** the Phase 4bm-W implementation report and closeout state "45 passed" for the three new pytest suites. The accurate re-verified count at merge time is **33 passed** — a documentation overcount in the branch docs, **not** a test failure; every listed suite passes (33/33). This merge-closeout records the accurate count (33). No code, no test outcome, and no diagnostic result is affected; the diagnostic verdict is unchanged.

Whole-repo pytest was not re-run at merge time; it remains affected by the documented baseline httpx/duckdb collection errors and the 2 pre-existing backtest subprocess failures — unchanged from prior phases and not introduced by this merge. No whole-repo pytest success is claimed.

## 9. Upstream immutability evidence

All re-hashed read-only pre-merge and confirmed byte-identical (gate not re-run; no manifest / successor-state / gate-report written):

| Artefact | Pre/Post SHA256 | Status |
| --- | --- | --- |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | IDENTICAL |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | IDENTICAL |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | IDENTICAL |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | IDENTICAL |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | IDENTICAL |
| Phase 4bm-Q gate report sidecar | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | IDENTICAL |
| Phase 4bm-S research-use successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | IDENTICAL |
| Phase 4bm-S research-use successor-state sidecar | `05597fe4d568f5644ad9acc914f8a3b429bc7984cf7df3a2ac3f8c7935e02551` | IDENTICAL |
| Phase 4bm-U split-policy successor-state JSON | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` | IDENTICAL |
| Phase 4bm-U split-policy successor-state sidecar | `fa9ae709add4541111e70cfc03d9126ac40f136ea2ce1aa1abe299d3412ac0b6` | IDENTICAL |

The 90 v002 per-day label Parquets + 90 sidecars and the 90 v002 per-day feature Parquets + 90 sidecars are byte-identical pre/post (Phase 4bm-W reads them read-only and writes nothing under `data/microstructure/`). Parquet/sidecar counts verified at label 90/90 and feature 90/90.

## 10. Manifest state preservation

v002 label manifest (`microstructure_labels_aggtrades_v001__v002.json`, SHA `5e17074d…`): `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_5_label_cleared = false`; `label_family_research_use_authorized = false`; `chronological_split_policy = "not_yet_defined"` — all unchanged. v002 feature manifest (SHA `512a0a54…`): `research_eligible = false`; `diagnostics_authorized = false`; `ml_authorized = false` — all unchanged. No transition occurred. The recorded chronological split policy lives only in the Phase 4bm-U sibling successor-state JSON, never on the manifest. The manifests' historical `diagnostics_authorized=false` flag predates this phase; authorization for Phase 4bm-W derived from the operator prompt, not from manifest mutation. Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- no prior source code modified; no prior test modified; no prior committed script modified; no `pyproject.toml` / `README.md` / MCP file modified; `.gitignore` modified only by the narrow `data/research/` addition
- no `data/microstructure/` write; no `data/microstructure/` artefact committed
- no `data/research/` output committed (research-output namespace gitignored)
- no manifest mutated; no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no `chronological_split_policy` changed
- no successor-state JSON or sidecar created or mutated (Phase 4bm-S and Phase 4bm-U artefacts byte-identical)
- no gate report created or mutated; no gate rerun
- no ML model trained; no model selection / feature ranking / feature selection / hyperparameter selection / threshold tuning; no strategy created or signal computed; no PnL simulation / backtest / walk-forward run
- test holdout summarised descriptively only; not used for feature/model/hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, or eligibility rescue
- no split-mask materialization for later research use (only in-memory per-row diagnostic masks; no parquet rewrite)
- no data acquired; no public / authenticated / private endpoint called; no Binance API called; no WebSocket / user-stream opened
- no credential / `.env` / `.mcp.json` / MCP / Graphify used
- no normalizer rerun; no raw / derived / feature / label eligibility gate rerun; no kernel rerun
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked)
- no retained verdict revised; no project lock loosened; no M0 amendment
- no successor authorized. **Phase 4bm-X is not authorized by Phase 4bm-W.**

**Phase 4bm-W runs descriptive diagnostics only.** **Phase 4bm-W does not run ML.** **Phase 4bm-W does not define or run strategy.** **Phase 4bm-W does not run backtests.** **Phase 4bm-W does not authorize acquisition.** **Phase 4bm-W does not authorize research execution beyond the scoped descriptive diagnostics.** **Phase 4bm-W does not perform feature selection.** **Phase 4bm-W does not perform model selection.** **Phase 4bm-W does not perform threshold tuning.** **Phase 4bm-W does not use the test holdout for tuning or design.** **Phase 4bm-W does not mutate any manifest.** **Phase 4bm-W does not mutate any successor-state artefact.** **Phase 4bm-W does not commit data/microstructure.**

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

All preserved verbatim.

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (never invoked by Phase 4bm-W)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results (Phase 4am .. Phase 4bm-V) preserved verbatim.

## 14. No-rescue constraints

The Phase 4bm-W merge does not, and cannot, be construed as authorising:

- any further diagnostics execution beyond the scoped descriptive diagnostics already run; diagnostic iteration on the test holdout; split-mask materialization for later research use;
- ML model training, model selection, feature ranking, feature selection, hyperparameter selection, threshold tuning, meta-labeling, or any conversion of labels into signals;
- strategy design, strategy signal generation / signal construction, strategy logic, position state, entry / exit rules, PnL simulation, backtest design / execution, or walk-forward optimization;
- any use of the test window for tuning or design, or eligibility rescue;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening; 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` from this diagnostics evidence alone.

The diagnostic verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` is descriptive-only and is **not** ML-readiness, strategy-readiness, or backtest-readiness. **Any further research execution requires a separately authorized phase.**

## 15. Successor authorization

**None.**

Candidate successors that are **not** authorized:

- Phase 4bm-X (any future phase — explicitly not authorized)
- multi-day v002 ML training / model selection / feature ranking / feature selection / hyperparameter selection / threshold tuning / meta-labeling
- multi-day v002 strategy specification / implementation / signal construction
- multi-day v002 backtest specification / plan / execution / walk-forward optimization
- multi-day v002 research execution beyond the scoped descriptive diagnostics already run
- split-mask materialization for later research use
- additional acquisition (additional days / symbols / data families beyond the locked 90-day v002 envelope; mark-price / order-book / funding / OI / liquidation / cross-venue / aggTrades)
- Phase 4bn-* / 4bo-* / 4bp-* / 4bq-*
- Phase 5
- Phase 4 canonical
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- user streams / WebSockets
- MCP / Graphify / `.mcp.json` / credentials

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

## 16. Recommended state

**Remain paused.** Phase 4bm-W is now project-complete after this merge-closeout and its SHA-finalization. The diagnostic verdict `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` is descriptive-only and authorizes nothing.

**Conditional next, NOT authorized:** any future research execution on the multi-day v002 family (ML feasibility, model selection, strategy design, backtests) would require its own separately authorized operator prompt and must honour the Phase 4bm-U split policy, the single-use test-holdout protection, and all retained verdicts and project locks. It is **not** authorised by this merge.

**Phase 4bm-X is not authorized by Phase 4bm-W.** **Recommended state remains paused.**
