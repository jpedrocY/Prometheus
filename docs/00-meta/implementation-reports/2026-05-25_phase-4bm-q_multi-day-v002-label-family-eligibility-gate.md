# Phase 4bm-Q — Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution

**Phase identity:** Phase 4bm-Q — Multi-Day V002 Label-Family Eligibility Gate Design / Implementation / Execution (code + tests + script + docs + local gitignored gate report; multi-day v002 analogue of Phase 4bj-E).
**Date:** 2026-05-25.
**Branch:** `phase-4bm-q/multi-day-v002-label-family-eligibility-gate`.
**Base:** `main` at `3f87123175e07a1cc373b15f3fc29d487fae3265` (Phase 4bm-P merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 hierarchy. Phase 4bm-Q is a code + tests + script + docs phase whose verdict influences downstream authorization decisions (label-family research-use, successor-state recording, chronological-split-policy). Tier 1 ceremony applies: dedicated branch, full implementation report, dedicated closeout, narrow `current-project-state.md` update, and (separately, in a future phase) a Tier 1 merge-closeout.
**Phase type:** code + tests + script + docs + 1 local gitignored gate report.
**Status:** branch-complete by this work; not merged into `main`; not project-complete.

---

## 1. Required exact phrases

- **Phase 4bm-Q is a label-family eligibility gate phase only.**
- **LABEL_GATE_PASS is report-level only, if achieved.**
- **Label-family research-use is not authorized by Phase 4bm-Q.**
- **Label-family successor-state recording is not authorized by Phase 4bm-Q.**
- **Chronological split policy is not authorized by Phase 4bm-Q.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-Q.**
- **No label artefact is modified by Phase 4bm-Q.**
- **No upstream artefact is mutated by Phase 4bm-Q.**
- **No data/microstructure file is committed by Phase 4bm-Q.**
- **No manifest transition is authorized by Phase 4bm-Q.**
- **No successor-state JSON creation is authorized by Phase 4bm-Q.**
- **Phase 4bm-R is not authorized by Phase 4bm-Q.**

## 2. Phase header

Phase 4bm-Q is the multi-day v002 analogue of the v001 **Phase 4bj-E** label-family eligibility gate. It produces:

- four new v002 source modules under `src/prometheus/research/microstructure/`;
- a narrow `__init__.py` re-export update;
- five new test files under `tests/research/microstructure/` (38 tests, all PASS);
- one narrow test refinement to `tests/research/microstructure/test_import_boundaries.py` (word-boundary `.env` check; details §11);
- one new orchestrator script at `scripts/phase4bm_q_run_multiday_label_gate.py`;
- one local gitignored gate report + paired Phase 4bb-F sidecar under `data/microstructure/gate-reports/labels/`;
- this main memo + a closeout memo + a narrow `current-project-state.md` paragraph + new "Current phase:" block.

The phase answers, by deterministic offline read-only inspection of the Phase 4bm-O local gitignored v002 label artefacts, **whether the v002 label family passes a formal label-family eligibility gate at report level**.

## 3. Scope and boundary

Phase 4bm-Q is authorised to:

- add source modules `multiday_label_gate_io.py`, `multiday_label_gate_checks.py`, `multiday_label_gate_report.py`, `multiday_label_gate.py` under `src/prometheus/research/microstructure/`;
- narrowly update the package `__init__.py` for the new public-API re-exports;
- add fixture-free + real-artefact test files under `tests/research/microstructure/`;
- narrowly tighten one pre-existing test (`test_import_boundaries.py`) so the `.env` substring check uses a word boundary and no longer collides with the Phase 4bm-N `envelope_terminal_unix_ms` identifier accessed via `self.envelope_terminal_unix_ms` inside a dataclass `to_dict()` body (the new `multiday_label_gate_report.py` legitimately exposes this v002-schema field);
- add an offline label-family eligibility gate orchestrator script at `scripts/phase4bm_q_run_multiday_label_gate.py`;
- execute the gate read-only against the existing Phase 4bm-O local gitignored label artefacts and emit exactly one new gate report JSON + paired canonical Phase 4bb-F sidecar under `data/microstructure/gate-reports/labels/` (gitignored, not committed);
- add this implementation report + a closeout memo + a narrow `current-project-state.md` paragraph + new "Current phase:" block (prior Phase 4bm-P block preserved as labelled historical context).

Phase 4bm-Q does **NOT**:

- run diagnostics, ML, models, classifiers, scores, predictions, embeddings, or learned representations;
- compute strategy signals, strategy actions, position-state outputs, PnL, MFE, MAE, R-multiple, equity curves, alpha, edge, or decision scores;
- compute new label / target / barrier / execution-quality / cross-symbol outputs;
- recompute the v002 label kernel, the v002 feature kernel, or any normalizer / raw gate / derived gate / feature gate;
- mutate any v002 label parquet, v002 label manifest, v002 label sidecar, v002 feature manifest + sidecar, Phase 4bm-L successor-state, Phase 4bm-J gate report, v002 derived/normalized multi-day index manifest, 90 v002 normalized parquets, Phase 4bm-F successor-state, Phase 4bm-D gate report, v002 raw manifest, v002 acquisition log, Phase 4bl-E raw successor-state, Phase 4bl-D-R raw gate report, prior v001 artefacts, or any other on-disk governance artefact;
- flip `research_eligible`, transition `eligibility_gate_status`, set `stage_5_label_cleared = true`, mark `label_family_research_use_authorized = true`, or change `chronological_split_policy` on any actual on-disk manifest;
- create a label-family successor-state JSON;
- acquire data, call any Binance endpoint, open any WebSocket, use any credential, read or create `.env` / `.mcp.json`, or enable MCP / Graphify;
- revise any retained verdict, change any project lock, or amend M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1 / Phase 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K / 4bm-L / 4bm-M / 4bm-N / 4bm-O / 4bm-P;
- authorize Phase 4bm-R, label-family research-use, label-family successor-state recording, chronological-split-policy, diagnostics, ML, strategy, backtests, additional acquisition, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user streams, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

## 4. Module decomposition

Mirrors the Phase 4bm-J four-module decomposition (orchestrator + checks + io + report) verbatim, adapted to labels:

| File | Description |
|---|---|
| `multiday_label_gate_io.py` | Path discipline under `data/microstructure/gate-reports/labels/`; streaming SHA256 helper; canonical Phase 4bb-F sidecar composer; atomic write-then-rename JSON + sidecar writers with refuse-to-overwrite. |
| `multiday_label_gate_checks.py` | 60-check deterministic offline suite (groups A–G); `MultidayLabelGateCheckResult` / `MultidayLabelGateCheckStatus` / `MultidayLabelGateContext` dataclasses; locked Phase 4bm-O / Phase 4bm-L / Phase 4bm-J / Phase 4bm-D / Phase 4bm-F / Phase 4bl-D-R / Phase 4bl-E identity SHAs; `SAMPLE_DATES` deep-scan set of 6 representative dates; `CHECK_ORDER` tuple; `run_all_checks(ctx)` orchestrator with `try/except → ERROR` conversion. |
| `multiday_label_gate_report.py` | Frozen `MultidayLabelGateReport` dataclass with build-time hard invariants (`research_eligible_after=False`, `eligibility_gate_status_after="pending"`, `stage_5_label_cleared_after=False`, `label_family_research_use_authorized_after=False`, `chronological_split_policy_after="not_yet_defined"`, 7 non-authorization flags `False`, 14 immutability flags `True`); `GATE_VERDICT_PASS` / `_FAIL` / `_INDETERMINATE` taxonomy; classifier; `build_report(...)` + `write_gate_report(...)`. |
| `multiday_label_gate.py` | `MultidayLabelGateInput` (20 typed `Path` fields + `code_commit_sha` + `write_report`) with `__post_init__` validation; `MultidayLabelGateResult`; public `run_multiday_label_family_gate(inp)` orchestrator. |

## 5. Check inventory

60 checks across 7 groups:

- **A — Locked preconditions (15)**: `A1..A15` — label manifest SHA, label sidecar SHA, sidecar canonical form, feature manifest SHA + sidecar SHA, Phase 4bm-J gate report + sidecar SHA, Phase 4bm-L successor-state + sidecar SHA, derived manifest SHA, raw manifest SHA, Phase 4bm-D gate report SHA, Phase 4bm-F successor-state SHA, Phase 4bl-D-R gate report SHA, and Phase 4bm-P structural QA verdict (`LABEL_STRUCTURAL_QA_PASS`).
- **B — Inventory / sidecar / gitignore (10)**: `B1..B10` — manifest + sidecar present, 90 label parquets, 90 sidecars, exact contiguous-date inventory, BTCUSDT-only symbol subdir, `per_day_outputs` length=90 + unique dates, all 90 sidecars canonical Phase 4bb-F + SHA-consistent, all 90 parquet SHA256 match manifest.
- **C — Schema / lineage / forbidden-substring detector (11)**: `C1..C11` — manifest `column_count`=40, `schema_column_list` equals `LABEL_SCHEMA_V002`, 17 lineage / 8 label / 14 support column counts, `label_config_hash`, `feature_config_hash`, dataset / source / symbol / date / horizon identity literals, all 14 manifest lineage SHA fields, 0 forbidden-substring hits across all 40 columns, all 90 parquets share identical canonical 40-column schema.
- **D — Row count / partition / timestamp (6)**: `D1..D6` — total row_count=155,153,449, sum(per-day)=total, per-day label row count == per-day feature row count (90/90), no zero-row day, parquet `num_rows` matches manifest (90/90), sample partition invariants over 6 representative dates (row_index 0..n-1, monotonic timestamps, `feature_timestamp_ms == source_transact_time_ms`, in-day boundaries, symbol/utc_date/dataset_version constants).
- **E — Label semantics / censoring / value-domain (7)**: `E1..E7` — per-row censoring rule `horizon_censored_flag_H == (source_transact_time_ms + horizon_ms_H > envelope_terminal_unix_ms)` over 6 sample days × 4 horizons; censored-row null discipline + `label_any_censored_flag == OR(horizon_censored_flag_*)`; `forward_direction_H ∈ {-1, 0, +1, null}`; `invalid_price_row_count == 0` at top-level / per-day aggregate / sampled rows; `censored_per_horizon` aggregate equals expected `{1s:14, 5s:39, 15s:170, 60s:634}`; `envelope_terminal_unix_ms = 1740787199996`; censored counts monotone non-decreasing in horizon order.
- **F — Upstream immutability (4)**: `F1..F4` — feature manifest still `research_eligible=False / eligibility_gate_status='pending' / stage_4_feature_cleared=False`; derived manifest still pending; raw manifest still pending; 90/90 `per_day_outputs[].source_feature_parquet_sha256` matches v002 feature manifest's `feature_parquet_sha256` byte-for-byte.
- **G — Non-authorization (7)**: `G1..G7` — manifest `research_eligible=False`, `eligibility_gate_status='pending'`, `stage_5_label_cleared=False`, `label_family_research_use_authorized=False`, `chronological_split_policy='not_yet_defined'`, all 8 non-authorization flags `False`, `boundary_confirmations` all `True` with `len >= 17`.

`CHECK_ORDER` is a 60-entry tuple and `run_all_checks` enforces that the observed result ordering equals `CHECK_ORDER` (drift raises `MultidayLabelGateIOError`).

## 6. Locked SHAs (compiled from Phase 4bm-O / Phase 4bm-P / Phase 4bm-J evidence)

| Artefact | Expected SHA256 |
|---|---|
| Label manifest (`microstructure_labels_aggtrades_v001__v002.json`) | `5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed` |
| Label manifest sidecar | `451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd` |
| `label_config_hash` | `352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560` |
| `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` |
| Phase 4bm-J gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` |
| Phase 4bm-J gate report sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` |
| Phase 4bm-L successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` |
| Phase 4bm-L successor-state sidecar | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` |
| v002 derived/normalized manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 derived/normalized manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| Phase 4bm-D gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Phase 4bm-D gate report sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| Phase 4bm-F successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` |
| Phase 4bm-F successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` |
| Phase 4bl-D-R raw gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| Phase 4bl-E raw successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |

## 7. Execution and gate verdict

```text
python scripts/phase4bm_q_run_multiday_label_gate.py \
    --code-commit-sha 3f87123175e07a1cc373b15f3fc29d487fae3265
```

Result:

```text
[phase-4bm-q] running check suite (60 checks)...
[phase-4bm-q] check results: total=60 PASS=60 FAIL=0 ERROR=0 NOT_APPLICABLE=0
[phase-4bm-q] gate_verdict     : LABEL_GATE_PASS
[phase-4bm-q] overall_status   : pass
```

**Gate verdict: `LABEL_GATE_PASS`.**

- Check totals: **60 / 60 PASS** (0 FAIL, 0 ERROR, 0 NOT_APPLICABLE; 0 blocking failures).
- Group totals: A 15/15, B 10/10, C 11/11, D 6/6, E 7/7, F 4/4, G 7/7.
- Report path: `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json`
- Report SHA256: `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e`
- Report size: 20,259 bytes
- Sidecar SHA256: `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8`
- Sidecar size: 156 bytes
- Sidecar canonical Phase 4bb-F format: `<report_sha256_lowercase_hex>  <basename>\n` (64 + 2 + 90 + 1 = 156 bytes; no CRLF, no BOM).

## 8. Local gitignored outputs

| Output | Path | SHA256 | Bytes |
|---|---|---|---|
| Gate report JSON | `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002__phase-4bm-q__1779708036319__3f87123175e0.json` | `8a360608841680775baa97f0c33e0f829050f02f1baf459d40bfb2e52df29f2e` | 20,259 |
| Gate report sidecar | `<report>.sha256` | `3913a510e6b2903e79c7501b1527befc62f5c302890e6a2b465034a43be29fc8` | 156 |

Both files are gitignored under `.gitignore:85` (`data/microstructure/`) and **NOT** committed. `git check-ignore -v <report>` returns `.gitignore:85: data/microstructure/`. `git status --short` post-execution shows only the expected pre-existing untracked entry (`data/research/`); **no** `data/microstructure/` artefact appears in `git status`.

## 9. Upstream immutability evidence

All 20 governance lineage artefacts are byte-identical pre/post gate execution:

| Artefact | Pre/Post SHA256 |
|---|---|
| v002 label manifest | `5e17074d…` |
| v002 label sidecar | `451d5b88…` |
| v002 feature manifest | `512a0a54…` |
| v002 feature manifest sidecar | `22e2fb77…` |
| 90 v002 label parquets | manifest `per_day_outputs[].sha256` (90/90 match) |
| 90 v002 label sidecars | manifest `per_day_outputs[].sidecar_sha256` (90/90 match) |
| 90 v002 feature parquets (via lineage cross-check) | `per_day_outputs[].source_feature_parquet_sha256` (90/90 match) |
| Phase 4bm-J gate report | `3c59dfae…` |
| Phase 4bm-J gate sidecar | `14a17764…` |
| Phase 4bm-L successor-state | `7eccaa8f…` |
| Phase 4bm-L successor-state sidecar | `c2b73330…` |
| v002 derived manifest | `01c5fa53…` |
| v002 derived manifest sidecar | `d96f31ae…` |
| v002 raw manifest | `01696786…` |
| Phase 4bm-D gate report | `3b45e70b…` |
| Phase 4bm-D gate report sidecar | `8e74261c…` |
| Phase 4bm-F successor-state | `72b6edd4…` |
| Phase 4bm-F successor-state sidecar | `1e9ffb23…` |
| Phase 4bl-D-R raw gate report | `f9493fd1…` |
| Phase 4bl-E raw successor-state | `a0576ca6…` |

Manifest state preservation:

- v002 label manifest: `research_eligible=false`, `eligibility_gate_status='pending'`, `stage_5_label_cleared=false`, `label_family_research_use_authorized=false`, `label_family_eligibility_gate_authorized=false`, `chronological_split_policy='not_yet_defined'` — unchanged.
- v002 feature manifest: `research_eligible=false`, `eligibility_gate_status='pending'`, `stage_4_feature_cleared=false` — unchanged.
- v002 derived/normalized manifest: `research_eligible=false`, `eligibility_gate_status='pending'` — unchanged.
- v002 raw manifest: `research_eligible=false`, `eligibility_gate_status='pending'` — unchanged.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant: preserved end-to-end; **never invoked** during Phase 4bm-Q.

## 10. Validation commands and results

| Command | Result |
|---|---|
| `git status --short` (pre-execution) | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected) |
| `git branch --show-current` | `phase-4bm-q/multi-day-v002-label-family-eligibility-gate` |
| `git rev-parse main` | `3f87123175e07a1cc373b15f3fc29d487fae3265` |
| `git rev-parse origin/main` | `3f87123175e07a1cc373b15f3fc29d487fae3265` (in sync) |
| `git log --oneline -12 --decorate` | latest main commit is `3f87123 docs(phase-4bm-p): finalize merge closeout shas` (matches expectation) |
| `pytest tests/research/microstructure/test_multiday_label_gate*.py` | **38 / 38 passed** |
| `pytest tests/research/microstructure/` (full sweep, run from repo root) | **all passing** (no new regression) |
| `ruff check` on Phase 4bm-Q surface (4 modules + script + 5 tests + `__init__.py` + `test_import_boundaries.py`) | **All checks passed!** |
| `mypy src/prometheus/research/microstructure/multiday_label_gate*.py` | **Success: no issues found in 4 source files** |
| `python scripts/phase4bm_q_run_multiday_label_gate.py --no-write-report` | LABEL_GATE_PASS (60/60) |
| `python scripts/phase4bm_q_run_multiday_label_gate.py --code-commit-sha 3f87123175e07a1cc373b15f3fc29d487fae3265` | LABEL_GATE_PASS; report + sidecar written under `data/microstructure/gate-reports/labels/` |
| Pre/post upstream immutability recompute (20 governance artefacts + 90 label parquets + 90 label sidecars) | byte-identical |
| `git status --short` (post-execution) | unchanged: only `data/research/` untracked (no `data/microstructure/` entry) |
| `git check-ignore -v` over new gate-report + sidecar | covered by `.gitignore:85: data/microstructure/` |

## 11. Notes on `test_import_boundaries.py` change

`tests/research/microstructure/test_import_boundaries.py` previously contained a bare-substring `.env` denylist scan. Phase 4bm-N introduced the v002 label schema field `envelope_terminal_unix_ms`, and Phase 4bm-Q's new frozen-dataclass `MultidayLabelGateReport` legitimately accesses it via `self.envelope_terminal_unix_ms` inside `to_dict()`. The substring `.env` therefore appears in code (excluding docstrings) as part of `.envelope_terminal_unix_ms` attribute access, tripping the bare-substring check despite no actual `.env` file reference.

The narrow fix swaps the bare `.env` substring for a word-boundary regex (`\.env(?![A-Za-z0-9_])`), preserving the original intent (catch `.env`, `.env.local`, `.env "`, `.env\n` file references) while accommodating legitimate identifiers like `.envelope_*`. This narrow correctness change is justified by the new v002 label schema field and is the smallest viable repair of a pre-existing test idiom. No other content of `test_import_boundaries.py` is altered; the `ALLOWLIST_DENY_TOKENS` tuple loses only its `.env` entry (re-implemented via `_DOT_ENV_RE`), and the new word-boundary check is added inside `test_allowlist_deny_tokens_only_in_allowlist_code` immediately after the loop over the remaining tokens.

## 12. Skipped checks and rationale

`mypy src/prometheus` (whole package) and whole-repo `pytest` were not invoked at Phase 4bm-Q level. Rationale:

- Phase 4bm-Q does not modify any existing source module outside the narrow `__init__.py` re-export update, and the new 4 modules introduce no third-party dependency beyond `pyarrow` / stdlib (already in the project baseline).
- The documented baseline of 29 mypy errors in 5 files (on `main`) is unrelated to Phase 4bm-Q surfaces; mypy run targeted at the 4 new modules returns `Success: no issues found in 4 source files`.
- The documented baseline of 15 pytest collection errors from missing `httpx` / `duckdb` and 2 pre-existing subprocess failures in `tests/unit/research/backtest/test_engine_d1a_dispatch.py` is unrelated to Phase 4bm-Q surfaces.
- The full microstructure pytest sweep (`pytest tests/research/microstructure/` run from repo root) passes without new regressions.

## 13. What this phase proves

- A deterministic, reproducible, offline label-family eligibility gate exists and runs to completion over the Phase 4bm-O local label artefacts;
- 60 / 60 PASS at first invocation, including every locked precondition SHA, every per-day inventory / sidecar / hash check, every schema / lineage / forbidden-substring check, every row-count / partition / timestamp check, every label-semantics / censoring / value-domain check, every upstream-immutability check, and every non-authorization invariant;
- The gate is byte-immutable with respect to every upstream artefact (20 governance witnesses + 90 label parquets + 90 label sidecars + transitive 90 feature parquets via `source_feature_parquet_sha256` lineage = 290 immutability witnesses), all byte-identical pre/post run;
- The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains preserved end-to-end and was never invoked.

## 14. What this phase does not prove

- That any v002 label has predictive value or forecastable signal;
- That label-family research-use should be authorized;
- That a chronological-split policy should be defined;
- That diagnostics, ML, strategy, or backtests should run;
- That any future Phase 4bm-Q merge phase or any successor (Phase 4bm-R, label-family research-use decision, label-family successor-state recording, chronological-split-policy memo) is authorized.

## 15. Non-authorization

Phase 4bm-Q does **not**, and **cannot**, authorize:

- Phase 4bm-R (any provisional successor; not authorized);
- multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F);
- multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G);
- multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I);
- multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J);
- multi-day v002 diagnostics;
- multi-day v002 ML training, model selection, feature ranking, meta-labeling;
- multi-day v002 strategy specification, implementation, signal construction;
- multi-day v002 backtest specification, plan, or execution;
- additional acquisition (no additional days, no additional symbols, no mark-price / order-book / funding / OI / liquidation / cross-venue data, no aggTrades acquisition beyond the existing locked v002 90-day envelope);
- Phase 4bn-* / 4bo-* / 4bp-* / 4bq-*;
- Phase 5;
- Phase 4 canonical;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user-stream / live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` / `stage_5_label_cleared` / `label_family_research_use_authorized` / `label_family_eligibility_gate_authorized` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E / -F / -G / -H / -I / -J / -K / -L / -M / -N / -O / -P;
- any further successor-state JSON creation;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST** (every upstream / sibling manifest remains byte-identical; the only file written by Phase 4bm-Q is the new gate report + paired sidecar under `data/microstructure/gate-reports/labels/`, and they are gitignored), **N-GATE-RERUN** (no prior gate is rerun; this is a new gate-report family), **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (no successor-state artefact created by Phase 4bm-Q). **N-DERIVATION** does not apply — Phase 4bm-Q is the explicitly authorized label-family eligibility gate phase.

## 16. Recommended state

**Remain paused.**

Phase 4bm-Q is branch-complete by this work. Per the Phase 4bk-A workflow standard, Phase 4bm-Q is **NOT** project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout). The operator's broader pause decision continues to apply.

## 17. Conditional next options, none authorized

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next** — future operator-authorized Phase 4bm-Q merge phase | docs + merge | **NOT authorized by this memo** |
| **Conditional later** — future multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F) | docs-only | **NOT authorized** |
| **Conditional later** — future multi-day v002 label-family research-use successor-state recording (multi-day analogue of Phase 4bj-G) | docs + local gitignored successor-state | **NOT authorized** |
| **Conditional later** — future multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / -I) | docs-only | **NOT authorized** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Diagnostics / ML / strategy / backtest work on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-Q** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-Q** |
