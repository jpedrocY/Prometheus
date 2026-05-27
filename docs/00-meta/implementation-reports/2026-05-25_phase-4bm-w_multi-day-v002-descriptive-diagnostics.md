# Phase 4bm-W — Multi-Day V002 Descriptive Diagnostics Execution

**Phase identity:** Phase 4bm-W — Multi-Day V002 Descriptive Diagnostics Execution (code + tests + docs + local gitignored diagnostic outputs; first actual descriptive/structural diagnostics execution phase for the research-use-approved-in-principle multi-day v002 feature/label family).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-w/multi-day-v002-descriptive-diagnostics`.
**Base SHA:** `main` at `348d8a34f45b8d3b5e1caa19ab8e0064a9015474` (Phase 4bm-V SHA-finalization commit `docs(phase-4bm-v): finalize merge closeout shas`; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3. First diagnostics execution for the multi-day v002 family; adjacent to ML / strategy / backtests while explicitly authorizing none of them.
**Phase type:** code + tests + docs + local gitignored diagnostic outputs. Adds three new source modules, one runner script, three test modules, narrowly extends `.gitignore`, adds two tracked docs files, and narrowly updates `docs/00-meta/current-project-state.md`. Writes local gitignored diagnostic outputs under `data/research/microstructure/diagnostics/phase-4bm-w/`. **No** manifest / successor-state / gate-report / parquet / sidecar mutation under `data/microstructure/`.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

**Phase 4bm-W runs descriptive diagnostics only.** **Phase 4bm-W does not run ML.** **Phase 4bm-W does not define or run strategy.** **Phase 4bm-W does not run backtests.** **Phase 4bm-W does not authorize acquisition.** **Phase 4bm-W does not authorize research execution beyond the scoped descriptive diagnostics.** **Phase 4bm-W does not perform feature selection.** **Phase 4bm-W does not perform model selection.** **Phase 4bm-W does not perform threshold tuning.** **Phase 4bm-W does not use the test holdout for tuning or design.** **Phase 4bm-W does not mutate any manifest.** **Phase 4bm-W does not mutate any successor-state artefact.** **Phase 4bm-W does not commit data/microstructure.** **Phase 4bm-X is not authorized by Phase 4bm-W.** **Recommended state remains paused.**

---

## 1. Phase identity

Phase 4bm-W is the separately authorized descriptive / structural diagnostics execution phase recommended (but not authorized) by the Phase 4bm-V readiness/scope memo (`RECOMMEND_AUTHORIZE_DESCRIPTIVE_DIAGNOSTICS_PHASE`). It implements and executes strictly descriptive / structural diagnostics over the multi-day v002 BTCUSDT feature/label family `microstructure_labels_aggtrades_v001 @ v002` (90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; horizons 1s / 5s / 15s / 60s), applying the Phase 4bm-U recorded chronological split policy `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`, and produces local gitignored diagnostic outputs plus tracked source / tests / docs. **Phase 4bm-W runs descriptive diagnostics only.**

## 2. Branch name

`phase-4bm-w/multi-day-v002-descriptive-diagnostics`

## 3. Base SHA

`348d8a34f45b8d3b5e1caa19ab8e0064a9015474` (Phase 4bm-V SHA-finalization commit, `docs(phase-4bm-v): finalize merge closeout shas`; head of `main` at branch time; `main == origin/main` verified). The Phase 4bm-V merge commit `6170cb8087870b8aa47bee5806bb56d2e9b4ed49` and merge-closeout commit `7ba87bb110a9419e531d8872dc0d8f8ef8f6dbed` are present on `main` immediately below this SHA-finalization commit (verified by `git log --oneline -14 --decorate`).

## 4. Predecessor Phase 4bm-V readiness decision

`RECOMMEND_AUTHORIZE_DESCRIPTIVE_DIAGNOSTICS_PHASE` (Phase 4bm-V — Multi-Day V002 Diagnostics Readiness and Scope Memo; docs-only; merge-complete and SHA-finalized on `main`). Phase 4bm-V recommended, but did not itself authorize, a future descriptive diagnostics execution phase, bounding it to the descriptive/structural categories of §10–§13 of that memo. The present Phase 4bm-W is that separately authorized execution.

## 5. Implementation surface

Tracked source / tests / script / config:

| Path | Kind |
| --- | --- |
| `src/prometheus/research/microstructure/diagnostics_split_policy_v002.py` | new module — pure split-policy logic (assignment, embargo, boundary-crossing) |
| `src/prometheus/research/microstructure/descriptive_diagnostics_v002.py` | new module — bounded per-partition descriptive/structural kernel |
| `src/prometheus/research/microstructure/diagnostics_report_v002.py` | new module — aggregation, verdict derivation, gitignored output writing |
| `scripts/phase4bm_w_run_descriptive_diagnostics.py` | new runner script (offline orchestrator) |
| `tests/research/microstructure/test_diagnostics_split_policy_v002.py` | new tests (pure policy) |
| `tests/research/microstructure/test_descriptive_diagnostics_v002.py` | new tests (synthetic parquets) |
| `tests/research/microstructure/test_diagnostics_no_network.py` | new tests (static no-network / no-credential scan) |
| `.gitignore` | narrow addition — `data/research/` (research-output namespace; never committed) |

Tracked docs:

| Path | Kind |
| --- | --- |
| `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-w_multi-day-v002-descriptive-diagnostics.md` | this report |
| `docs/00-meta/implementation-reports/2026-05-25_phase-4bm-w_closeout.md` | closeout |
| `docs/00-meta/current-project-state.md` | narrow current-phase block update |

The diagnostics modules import only the Python standard library, numpy, pyarrow, and sibling inert modules. They never import `requests`, `httpx`, `aiohttp`, `websockets`, `binance`, `dotenv`, `urllib.request`, `socket`, `os.environ`, or `getenv`, never read `.env`, never create `.mcp.json`, and never reference MCP / Graphify (statically verified by `test_diagnostics_no_network.py` and `test_import_boundaries.py`).

## 6. Validation results

| Command | Result |
| --- | --- |
| `pytest tests/research/microstructure/test_descriptive_diagnostics*.py tests/research/microstructure/test_diagnostics*.py` | **45 passed** (12 + 12 + 21 across the three new modules) |
| `pytest tests/research/microstructure/test_import_boundaries.py` | **passed** (auto-scans the three new modules for forbidden imports/tokens) |
| `ruff check src/prometheus/research/microstructure scripts tests/research/microstructure` | **All checks passed** |
| `mypy src/prometheus/research/microstructure/diagnostics_split_policy_v002.py descriptive_diagnostics_v002.py diagnostics_report_v002.py` | **Success: no issues found in 3 source files** |
| `mypy src/prometheus/research/microstructure` (whole package) | 2 errors, both in **pre-existing** files (`labels_manifest_v002.py:370`, `multiday_feature_gate_checks.py:847`); **0** in the three new files |

Known baseline caveats (not introduced by this phase): whole-package mypy carries 2 pre-existing errors in 2 pre-existing files; whole-repo pytest is still affected by the documented httpx/duckdb collection errors and the two pre-existing backtest subprocess failures. None changed by this phase.

## 7. Local diagnostic output paths and SHA256s

All outputs are local gitignored (under `.gitignore` `data/research/`); none committed.

| Output | Path | SHA256 |
| --- | --- | --- |
| Summary JSON | `data/research/microstructure/diagnostics/phase-4bm-w/descriptive_diagnostics_summary.json` | `f4b825af2e81734007be06acac5083e2d4048b54b5650bc407d87a6fc246198a` |
| Summary sidecar | `…/descriptive_diagnostics_summary.json.sha256` | `ff52873c983b55cc74a0639d17ea8b3d128cdbee9c77763cd11d2e71b3820473` |
| Diagnostics manifest JSON | `…/diagnostics_manifest.json` | `ac10061d2f0257002e094d578bcc6149b1a74ca28c604fd0d0a97e5c51c26e45` |
| Diagnostics manifest sidecar | `…/diagnostics_manifest.json.sha256` | `644506e392db46da6d27fa46519cac327136b1a05e350e2d9b231c62fce517eb` |
| Per-day inventory table | `…/descriptive_diagnostics_tables/per_day_inventory.csv` | recorded in diagnostics manifest |
| Per-split horizon summary table | `…/descriptive_diagnostics_tables/per_split_horizon_summary.csv` | recorded in diagnostics manifest |

Sidecars use the canonical Phase 4bb-F format `<sha256_lowercase_hex><two spaces><basename><LF>`. Output JSON is ASCII, LF-only, two-space indent, sorted keys (deterministic except `created_at_unix_ms` and `code_commit_sha`).

## 8. Diagnostic verdict

`DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS`.

Zero blocking structural failures. Four non-blocking caveats: (a) envelope-terminal censoring present (857 total censored, all in the test split; horizon availability asymmetric across splits); (b) the 60-second boundary embargo excludes 538 earlier-split rows (descriptive estimate; per-row masks only, no parquet rewrite); (c) forward-return quantiles are approximate (fixed-width histogram, range ±0.02, bin width 1e-05); exact additive moments (mean / std / min / max) are not approximate; (d) the v002 label manifest records `diagnostics_authorized=false` — a historical flag predating Phase 4bm-W; authorization for this phase derives from the Phase 4bm-W operator prompt, not the manifest, and the manifest is unmutated.

This verdict is descriptive-only. It is **not** an ML-readiness, strategy-readiness, or backtest-readiness signal.

## 9. Diagnostic groups executed

All eight descriptive/structural groups of the authorization scope were executed:

- **A. Dataset/split inventory** — row counts by split and UTC date; partition counts by split; 90/90 label + 90/90 feature parquet/sidecar presence; split-date membership; train/validation/test coverage.
- **B. Label availability and censoring** — per-horizon non-null / null / censored counts; envelope-terminal censoring summary; boundary-embargo exclusion estimates; horizon availability by split.
- **C. Label distribution** — forward-return mean/std/min/max (exact), approximate quantiles, sign balance, threshold-free direction balance, extreme |return| counts, distribution descriptors across train/validation/test (descriptive only).
- **D. Feature/label alignment** — per-day row-count alignment; row_index / agg_trade_id / feature_timestamp_ms / source_transact_time_ms elementwise alignment; `feature_config_hash` (feature side) and `label_config_hash` (label side) consistency; `source_transact_time_ms == feature_timestamp_ms`.
- **E. Per-day and per-split stability** — per-day row counts; per-day censoring; per-split aggregates.
- **F. Boundary-embargo and leakage-guard** — boundary-crossing exclusion estimate per boundary and per horizon; embargo rule applicability; no-shuffle compliance; test-holdout-untouched-for-tuning guarantee.
- **G. Missingness / nullability / value-domain** — null/non-null counts; `forward_direction ∈ {-1,0,+1,null}`; `invalid_price_row_count` confirmation; censored-row null discipline; `label_any_censored_flag == OR(horizon_censored_flag_*)`.
- **H. Report-only QA summaries** — local gitignored summary JSON + CSV tables + diagnostics manifest.

## 10. Split-policy application summary

Phase 4bm-U `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` applied verbatim; rows assigned by `source_transact_time_ms` UTC date.

| Split | UTC dates (inclusive) | Partitions | Rows (observed) |
| --- | --- | --- | --- |
| Train | 2024-12-01 .. 2025-01-14 | 45 | 74,535,688 |
| Validation | 2025-01-15 .. 2025-02-13 | 30 | 56,819,939 |
| Test / final holdout | 2025-02-14 .. 2025-02-28 | 15 | 23,797,822 |
| **Total** | 2024-12-01 .. 2025-02-28 | **90** | **155,153,449** |

Observed total = expected total (155,153,449). Partition / sidecar counts: label 90/90, feature 90/90. `out_of_partition_day = 0` and `split_assignment_mismatch = 0` confirm that every row's `source_transact_time_ms` UTC date equals its partition date (the split assignment is unambiguous).

## 11. Embargo / boundary-crossing summary

Minimum 60-second boundary embargo at `T_TV = 2025-01-15T00:00:00Z` (1736899200000 ms) and `T_VT = 2025-02-14T00:00:00Z` (1739491200000 ms). Boundary-crossing rows (earlier-split rows whose `source_transact_time_ms` falls in `[boundary − 60000, boundary)`) are excluded from the earlier split only, by per-row mask; the 90 v002 label parquets are never rewritten.

| Boundary | Earlier split | Embargo-excluded rows (observed) |
| --- | --- | --- |
| `T_TV` (train/validation) | train | 248 |
| `T_VT` (validation/test) | validation | 290 |
| **Total** | — | **538** |

Test split embargo = 0 (test is never the earlier split at any boundary). Per-horizon boundary-crossing sub-estimates (descriptive) are recorded per split in the summary JSON; the 60s embargo is sized to the maximum declared horizon (60s).

## 12. Label availability / censoring summary

Per-horizon censored counts (observed) exactly match the recorded v002 manifest expectation:

| Horizon | Censored (observed) | Censored (expected) |
| --- | --- | --- |
| 1s | 14 | 14 |
| 5s | 39 | 39 |
| 15s | 170 | 170 |
| 60s | 634 | 634 |
| **Total** | **857** | **857** |

All 857 censored rows fall in the test split (final day 2025-02-28; envelope terminal `1740787199996` ms = 2025-02-28T23:59:59.996Z). Train and validation have zero censored rows. Censored-row null discipline holds: in every split×horizon, the number of null forward-return rows equals the number of censored rows (`censored_row_not_null = 0`), and `label_any_censored_flag == OR(horizon_censored_flag_*)` everywhere (`any_censored_flag_mismatch = 0`). `invalid_price_row_count = 0` (top-level, per-day aggregate, and per-row).

## 13. Label distribution summary

Forward-log-return descriptive statistics (exact additive moments; descriptive only — never used for selection / tuning / design):

| Split | Horizon | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| train | 1s | 1.63e-06 | 2.44e-04 | -0.02496 | 0.02528 |
| train | 60s | 1.47e-05 | 1.58e-03 | -0.06982 | 0.03782 |
| validation | 1s | 2.19e-06 | 2.76e-04 | -0.00922 | 0.01224 |
| validation | 60s | 3.14e-05 | 1.88e-03 | -0.03749 | 0.02701 |
| test | 1s | 9.55e-07 | 2.15e-04 | -0.00388 | 0.00284 |
| test | 60s | 2.01e-05 | 1.51e-03 | -0.01489 | 0.01381 |

Direction balance (`forward_direction ∈ {-1,0,+1,null}`) is recorded per split×horizon; std grows monotonically with horizon within each split; the zero-return mass shrinks with horizon (e.g. train 1s zero = 6,410,923 → train 60s zero = 143,672). All values are descriptive and structural; no distribution descriptor is used to select features, models, thresholds, or strategies. The full per-split×horizon table is in the summary JSON and `per_split_horizon_summary.csv`.

## 14. Feature/label alignment summary

Per-day feature↔label alignment over all 90 days: `row_count_mismatch_days = 0`, `row_index_mismatch = 0`, `agg_trade_id_mismatch = 0`, `feature_timestamp_mismatch = 0`, `source_transact_time_mismatch = 0`, `feature_config_hash_mismatch_days = 0`. The label family is in strict 1:1 row alignment with the v002 feature family (155,153,449 rows each; per-day parity). `source_transact_time_ms == feature_timestamp_ms` for all rows (`src_ne_feature_ts = 0`). Feature `feature_config_hash` is constant at `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`; label `label_config_hash` is constant at `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560`.

## 15. Per-day / per-split stability summary

Per-day row counts vary across the 90 days (no zero-row day); per-day censoring is zero on every non-final day and concentrated entirely on 2025-02-28; missingness (null forward returns) equals censoring everywhere. Per-split aggregates are recorded in §10/§12/§13 and `per_day_inventory.csv` / `per_split_horizon_summary.csv`. No per-day structural anomaly was detected (all structural counters aggregate to 0).

## 16. Missingness / value-domain summary

`forward_direction_H ∈ {-1, 0, +1, null}` on all rows (`direction_domain_violation = 0`); `direction_sign_mismatch_vs_return = 0` (sign of each non-null forward return matches its non-null direction); per-horizon `horizon_censored_flag_H == (source_transact_time_ms + H_ms > envelope_terminal_unix_ms)` on all rows (`censor_rule_mismatch = 0`); `row_index` is a contiguous `0..n-1` per partition (`row_index_violation = 0`); `invalid_price_row_count = 0`; symbol / dataset_version constancy holds (`symbol_violation = 0`, `dataset_version_violation = 0`).

## 17. No-shuffle / holdout-protection confirmation

No random / shuffled / k-fold-over-time / bootstrap / post-hoc temporal resampling split was used; rows are assigned strictly by `source_transact_time_ms` UTC date with the recorded chronological windows. The test / final holdout (2025-02-14 .. 2025-02-28; 15 dates; 23,797,822 rows) was summarised **descriptively only** (row counts, censoring, missingness, distribution descriptors) and was **not** used for feature selection, model selection, hyperparameter selection, threshold tuning, strategy design, diagnostic iteration, or eligibility rescue. No diagnostic finding on the test window was fed into any selection / tuning / design loop. The summary JSON `holdout_protection` block records all of these as `false`/protected. **Phase 4bm-W does not use the test holdout for tuning or design.**

## 18. Confirmation no ML / strategy / backtests

No ML model was trained; no model was selected; no features were ranked or selected; no hyperparameters or thresholds were tuned; no strategy was specified, designed, or signalled; no PnL was simulated; no backtest or walk-forward optimization was run. **Phase 4bm-W does not run ML.** **Phase 4bm-W does not define or run strategy.** **Phase 4bm-W does not run backtests.** **Phase 4bm-W does not perform feature selection.** **Phase 4bm-W does not perform model selection.** **Phase 4bm-W does not perform threshold tuning.**

## 19. Confirmation no acquisition

No data was acquired; no additional days or symbols were added; no public / authenticated / private endpoint was called; no WebSocket / user-stream was opened; no credential / `.env` / `.mcp.json` was read or created; MCP / Graphify was not enabled. **Phase 4bm-W does not authorize acquisition.**

## 20. Confirmation no manifest or successor-state mutation

The v002 label manifest, the v002 feature manifest, the Phase 4bm-S label-family research-use successor-state, the Phase 4bm-U chronological split-policy successor-state, and the Phase 4bm-Q label-family eligibility gate report were all read-only and re-hashed byte-identical pre/post:

| Artefact | SHA256 | Result |
| --- | --- | --- |
| v002 label manifest | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` | IDENTICAL |
| v002 label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` | IDENTICAL |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | IDENTICAL |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | IDENTICAL |
| Phase 4bm-S successor-state JSON | `081730006c11360692db0a99d59a0ed499f762ef4f86d6e29bdf3016550abfe7` | IDENTICAL |
| Phase 4bm-U successor-state JSON | `6834ab11a5ac5d93b4d9f14d9b71ef3acb2a279bd8e3189fd22421598675fc9c` | IDENTICAL |
| Phase 4bm-Q gate report | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | IDENTICAL |

The original manifest `chronological_split_policy` remains `"not_yet_defined"`; the recorded policy continues to live only in the Phase 4bm-U sibling successor-state JSON. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked). **Phase 4bm-W does not mutate any manifest.** **Phase 4bm-W does not mutate any successor-state artefact.**

## 21. Confirmation no data/microstructure commit

`git status --short` shows only `.gitignore` (modified) and the new tracked source / test / script files; it shows **no** `data/microstructure/` entry and **no** `data/research/` entry. The diagnostic outputs under `data/research/microstructure/diagnostics/phase-4bm-w/` are gitignored (`git check-ignore` matches the new `.gitignore` `data/research/` rule) and are not committed. No `data/microstructure/` artefact is staged or committed. **Phase 4bm-W does not commit data/microstructure.**

## 22. Retained verdicts preserved

All preserved verbatim: **H0** FRAMEWORK ANCHOR; **R3** BASELINE-OF-RECORD; **R1a** RETAINED — NON-LEADING; **R1b-narrow** RETAINED — NON-LEADING; **R2** FAILED — §11.6; **F1** HARD REJECT; **D1-A** MECHANISM PASS / FRAMEWORK FAIL; **5m thread** OPERATIONALLY CLOSED; **V2** HARD REJECT; **G1** HARD REJECT; **C1** HARD REJECT. All prior phase results (Phase 4am .. Phase 4bm-V) preserved.

## 23. Project locks preserved

All preserved verbatim: §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% risk / 2× leverage / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6/§7/§8; Phase 4j §11; Phase 4k/4p/4q/4v/4w; Phase 4ak M0 twelve-clause gate; Phase 4al refined no-rescue rule; Phase 4aw `flip_research_eligible` always-raises invariant (never invoked); Phase 4bb-F canonical sidecar/path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard.

## 24. Recommended next state

**Remain paused.** Phase 4bm-W is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1). The descriptive diagnostics verdict is `DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS` (descriptive-only; not ML/strategy/backtest readiness). **Phase 4bm-X is not authorized by Phase 4bm-W.** **Recommended state remains paused.**
