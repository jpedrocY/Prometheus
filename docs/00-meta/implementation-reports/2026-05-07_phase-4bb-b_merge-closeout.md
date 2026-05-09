# Phase 4bb-B — Merge Closeout

**Phase identity:** Phase 4bb-B — AggTrades Eligibility-Gate Execution-Plan Memo.
**Type:** docs-only eligibility-gate execution-plan memo.
**Date:** 2026-05-07.
**Action:** merge into `main`.

---

## 1. Merge purpose

To merge the Phase 4bb-B aggTrades eligibility-gate execution-plan memo from the Phase 4bb-B feature branch into `main`. Phase 4bb-B is a docs-only planning memo for a future offline aggTrades eligibility-gate primitive (Phase 4bb-C, **not authorized** by this merge). It translates the Phase 4ba 45-check enumeration, fail-closed rules, and staged eligibility ladder, plus the Phase 4bb-A 13 implementation-planning observations, plus the existing Phase 4aw scaffold and Phase 4ax aggTrades skeleton, into a precise file-by-file, function-by-function execution plan.

The merge does **not** implement code, run any gate as a tool, acquire data, contact any Binance API endpoint, open any WebSocket, normalise any dataset, compute features, create a strategy candidate, train an ML model, flip `research_eligible` to `true`, transition any dataset out of `eligibility_gate_status=pending`, modify any data or manifest under `data/microstructure/`, modify any source / test / script / config / `.gitignore` / `pyproject.toml` / `README.md`, or authorize any successor phase. The Phase 4az dataset's manifest still has `research_eligible=false` and `eligibility_gate_status=pending`; the dataset remains **infrastructure evidence only**.

---

## 2. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4bb-b/aggtrades-eligibility-gate-execution-plan` |

---

## 3. SHAs

| Item | SHA |
| ---- | --- |
| `main` before merge | `32a41ddc39b7f0fae33de0f6d59d27eed65d2f11` |
| Phase 4bb-B commit | `160de912a38bb9bc57cf75de7e82443ef819b65f` (`docs(phase-4bb-b): plan aggtrades eligibility gate implementation`) |
| Source branch HEAD | `160de912a38bb9bc57cf75de7e82443ef819b65f` |
| Source / origin in sync at start | yes |
| Merge method | `git merge --no-ff` (ort strategy) |
| Merge commit SHA | `4f5337e886d7c26f010821597fe9cffced24d5d5` (`docs(phase-4bb-b): merge aggtrades eligibility-gate execution plan`, `Merge: 32a41dd 160de91`) |
| Final `main` SHA after push | `4f5337e886d7c26f010821597fe9cffced24d5d5` |
| Final `origin/main` SHA after push | `4f5337e886d7c26f010821597fe9cffced24d5d5` |
| Local / origin sync after push | in sync |

The merge-closeout commit SHA appears in the operator report after `git commit` and `git push`.

---

## 4. Files brought forward by the merge

3 file changes, 1,114 insertions, 0 deletions.

**Added (2 new tracked files):**

```
docs/00-meta/implementation-reports/2026-05-07_phase-4bb-b_aggtrades-eligibility-gate-execution-plan.md
docs/00-meta/implementation-reports/2026-05-07_phase-4bb-b_closeout.md
```

**Modified (1 narrow update):**

```
docs/00-meta/current-project-state.md   (Phase 4bb-B narrative paragraph + new "Current phase:" block; prior Phase 4bb-A block preserved as historical context)
```

**Files NOT modified by the merge:**

- No file under `src/prometheus/`.
- No file under `tests/`.
- No file under `scripts/`.
- No file under `data/microstructure/` (gitignored; Phase 4az artefacts are read-only context).
- No file under `data/manifests/`, `data/derived/`, `data/raw/`, `data/normalized/`, or `data/research/`.
- No strategy spec, validation checklist, runtime doc, or governance memo beyond Phase 4bb-B's own memo + closeout + the narrow `current-project-state.md` update.
- No `pyproject.toml`, `README.md`, or `.gitignore`.
- No M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md` unchanged).

**Local data outputs:** no new local data outputs were created by Phase 4bb-B. The Phase 4az artefacts under `data/microstructure/` (raw `.zip`, paired `.sha256`, manifest, acquisition log) are byte-identical to their post-Phase-4az state and were not touched. The Phase 4az manifest mtime is the original `May 7 21:55`.

---

## 5. Phase 4bb-B is docs-only

**Confirmed.** Phase 4bb-B is a docs-only eligibility-gate execution-plan memo. Its scope was strictly limited to:

- two new docs files under `docs/00-meta/implementation-reports/` (the 23-section memo and the closeout);
- one narrow update to `docs/00-meta/current-project-state.md` (Phase 4bb-B narrative paragraph + new "Current phase:" block; prior Phase 4bb-A block preserved verbatim as historical context);
- this merge-closeout.

---

## 6. Execution-plan result

The Phase 4bb-B memo records the following plan content for any future Phase 4bb-C, **none of which is activated by this merge**:

- **Future Phase 4bb-C implementation goal defined.** Offline-only primitive that reads raw `.zip`, `.sha256` sidecar, manifest, and acquisition log read-only; runs all 45 Phase 4ba §10 checks; records PASS / FAIL / NOT_APPLICABLE / ERROR; surfaces invalid-window candidates without mutating the original manifest; writes a JSON gate report under `data/microstructure/gate-reports/`; never flips `research_eligible=true` for raw families.
- **Proposed source module layout defined.** Four new modules under `src/prometheus/research/microstructure/` — `eligibility_gate.py`, `eligibility_checks.py`, `eligibility_report.py`, `eligibility_io.py` — plus a narrow `__init__.py` re-export update. No other source files modified.
- **Proposed test layout defined.** New test files under `tests/research/microstructure/` — `test_eligibility_gate.py`, `test_eligibility_checks.py`, `test_eligibility_report.py`, `test_eligibility_io.py`, `test_eligibility_no_network.py`. All offline (`pytest tmp_path` only).
- **No CLI / no script decision recorded.** No new `scripts/...` entrypoint. The gate is library-style and is invoked by direct import only. No `--output-root` / `--allow-network` / `--force` flag surface.
- **Proposed value objects and enums defined.** `AggTradesEligibilityGateInput`, `AggTradesEligibilityCheckResult`, `AggTradesEligibilityCheckStatus` `StrEnum` (`PASS` / `FAIL` / `NOT_APPLICABLE` / `ERROR`), `InvalidWindowCandidate`, `AggTradesEligibilityGateResult`, `AggTradesGateReport`.
- **Proposed gate execution flow defined.** A 17-step orchestrator: load read-only context; run 45 checks in a fixed order grouped 10.1 source / 10.2 checksum / 10.3 manifest / 10.4 schema / 10.5 timestamps / 10.6 monotonicity / 10.7 duplicates / 10.8 row count / 10.9 symbol-date / 10.10 archive integrity / 10.11 invalid windows / 10.12 cross-cutting; checks 10.4–10.10 share a single-pass row iterator so the file is decompressed and SHA-hashed exactly once; aggregate; recommend successor status (`research_eligible_after = false` always for raw families); write report; return result.
- **All 45 Phase 4ba checks mapped to future functions.** §12 of the memo gives a check-id-to-function mapping for every one of the 45 checks (e.g. `check_recomputed_sha_matches_manifest_and_sidecar` for §10.2.7; `check_a_non_decreasing_across_file` for §10.6.21; `check_feature_computation_forbidden_on_raw_family` for §10.12.41).
- **Gate-report schema defined.** Frozen dataclass + JSON serialisation: `report_id`, `dataset_family`, `version`, `symbol`, `source_manifest_path`, `raw_zip_path`, `sidecar_path`, `acquisition_log_path`, `created_at_utc_ms`, `code_commit_sha`, `overall_status`, `research_eligible_after` (always `false` for raw families), `eligibility_gate_status_after`, `checks` (always exactly 45 entries), `invalid_window_candidates`, `measured_summary`, `boundary_confirmations` (every key `true` for overall PASS), `no_successor_authorization` (always `true`).
- **Invalid-window handling plan defined.** Per-row anomalies surfaced as `InvalidWindowCandidate` records inside the gate report only; the original manifest's `invalid_windows` is never mutated.
- **Manifest immutability and successor-state policy defined.** Default mode never writes any successor manifest. Reserved `write_successor_manifest=True` mode is locked behind explicit Phase 4bb-C authorization-brief enablement and even when enabled may at most transition `eligibility_gate_status` from `pending` to `pass` or `fail` for raw families with `research_eligible_after = false` always.
- **Fail-closed conditions defined.** Eleven binding conditions including path discipline, read-only discipline, network discipline (no `requests` / `httpx` / `aiohttp` / `urllib.request` / `urllib3` / `socket` / `websockets` / `binance` / `dotenv` / `os.environ` reachable in import boundary), credential discipline (Phase 4aw `DENYLIST_TOKENS` scan), manifest-immutability hash equality before/after, raw-family `research_eligible=true` internal-error FAIL, eligibility-status discipline, 45-check completeness, forbidden-derived-data scan of output tree, `no_successor_authorization` invariant, static governance shape (`feature_computation: forbidden`, `strategy_use: forbidden`).
- **Future Phase 4bb-C test plan defined.** Happy path on a Phase 4az-shaped tmp_path mini-fixture; one failure-path test per failure pattern; coverage minimum of 45/45 check functions plus ≥ 90 total new tests; all offline.
- **Future Phase 4bb-C acceptance criteria defined.** Only the four new source modules + narrow re-export update; only the new test files; no new script; no new dependency; no `.gitignore` change; no data/manifest mutation under default invocation; gate report only under gitignored `data/microstructure/gate-reports/`; all planned failure tests fail at the predicted check id; `ruff` / `mypy` strict / `pytest` pass with the same pre-existing 2-failure baseline; `research_eligible_after = false` always; `no_successor_authorization = true` always.

---

## 7. Validation summary

Validation was performed on the Phase 4bb-B branch immediately before merge, and again on `main` after merge.

| Item | Result |
| ---- | ------ |
| `ruff check .` (whole repo) | `All checks passed!` |
| `mypy` (whole repo, strict) | `Success: no issues found in 89 source files` |
| `pytest` (whole repo) | `2 failed, 979 passed in 8.06s` (pre-merge); same pattern post-merge |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/	data/microstructure/` |
| `git diff --check` | clean |
| `git status` (final, on `main`) | clean apart from the persistent transient untracked `.claude/scheduled_tasks.lock` and `data/research/` |

**Whole-repo pytest has 2 failures, both pre-existing on `main` since before Phase 4az and unrelated to the eligibility-gate execution plan; Phase 4bb-B introduced zero new test regressions.**

The two failures are in `tests/simulation/test_backtest_real_2026_03.py`:

- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_ethusdt`

Both fail with `KeyError: 'trade_count'` raised in the unrelated `src/prometheus/research/data/storage.py:232`. The failures were verified as pre-existing on `main` before Phase 4bb-B. Phase 4bb-B is docs-only and does not touch `src/prometheus/research/data/storage.py`, the simulation tests, or any related path.

---

## 8. Boundary confirmations

The Phase 4bb-B merge confirms verbatim:

- **No code implemented.** No file under `src/prometheus/` or `tests/` or `scripts/` was added, modified, or deleted.
- **No gate run as a new tool.**
- **No data was modified.** The `data/microstructure/` tree is byte-identical to its post-Phase-4az state. The Phase 4az manifest mtime is the original `May 7 21:55`.
- **No manifest was modified.** Recomputed against the on-disk file before and after the merge confirms no mutation.
- **`data/microstructure/` remains gitignored.** `git check-ignore -v` returns `.gitignore:85:data/microstructure/	data/microstructure/`. Nothing under that subtree is staged or tracked.
- **`research_eligible` remains `false`** on the Phase 4az manifest (verified post-merge by direct inspection of `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json`).
- **`eligibility_gate_status` remains `pending`** on the Phase 4az manifest (same verification). The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` method (`ManifestImmutableError`) was not bypassed.
- **No acquisition occurred.** No HTTP request, no `data.binance.vision` fetch, no archive download.
- **No Binance API call.** No `fapi.binance.com`. No `/fapi/v1/aggTrades`. No `/fapi/v1/order`. No `/fapi/v2/account`. No `/fapi/v2/positionRisk`. No `/fapi/v1/leverage`. No `/fapi/v1/marginType`. No `/fapi/v1/forceOrders`. No `/fapi/v1/listenKey`.
- **No WebSocket opened.** No subscription, no stream.
- **No credential used.** No API key, no signed request, no `X-MBX-APIKEY` header.
- **No `.env` reads.**
- **No `.mcp.json` created.**
- **No MCP enabled.**
- **No Graphify enabled.**
- **No normalization.** No JSONL, no Parquet, no DuckDB, no derived dataset.
- **No features computed.** No metric, no ratio, no transform, no aggregation, no descriptive trading statistic.
- **No ML.** No label, no model, no embedding, no calibration, no fit.
- **No strategy.** No candidate, no entry rule, no exit rule, no threshold, no signal.
- **No backtest.**
- **No source / test / script change.** Phase 4bb-B touched only `docs/00-meta/...` paths.
- **No retained verdict revised.**
- **No project lock loosened.**
- **No M0 governance amended.** `docs/00-meta/m0-mechanism-admissibility-gate.md` is unchanged.
- **No successor phase authorized.**

---

## 9. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

No verdict is revised by this merge.

---

## 10. Preserved project locks

- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops where applicable.
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent applied verbatim by Phase 4az and reaffirmed by Phase 4ba; structural QA confirmed by Phase 4bb-A; execution plan mapped by Phase 4bb-B).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance).
- Phase 4j §11 (OI subset governance).
- Phase 4ak — M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al — refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax, Phase 4ay, Phase 4az, Phase 4ba, Phase 4bb-A results — all preserved verbatim.

No new lock is introduced. No existing lock is loosened.

---

## 11. No-rescue constraints (preserved)

- No R3-prime / R3 next-spec / R3 rescue / baseline-of-record revision.
- No R1a-prime / R1a promotion to leading.
- No R1b-narrow-prime / R1b-narrow promotion to leading.
- No R2-prime / R2 rescue / R2 cheaper-cost rerun.
- No H0-prime / framework-anchor revision.
- No F1-prime / F1 rescue / F1 profitable-subset rescue.
- No D1-A-prime / D1-A extra-filter / D1-B / V1-D1 hybrid / F1-D1 hybrid.
- No V2-prime / V2-narrow / V2-relaxed / V2 hybrid.
- No G1-prime / G1-narrow / G1-extension / G1 hybrid / G1 classifier relaxation.
- No C1-prime / C1-narrow / C1-extension / C1 hybrid.
- No cross-strategy hybrid of any kind.
- No 5m thread reopening.
- No 5m strategy / hybrid / retained-evidence successor.
- No conversion of Phase 4aq forensic numbers, Phase 4l V2 forensic numbers, Phase 4r G1 active-fraction numbers, Phase 4x C1 forensic numbers, Phase 4az aggTrades counts, Phase 4ba eligibility-gate enumerations, Phase 4bb-A structural QA observations, or Phase 4bb-B execution-plan content into parameter-selection inputs or feature recipes.
- No M0 amendment derived from Phase 4bb-B reasoning.
- No flipping of `research_eligible` to `true` for the Phase 4az dataset (or any other raw aggTrades dataset family) without a separately authorized eligibility-gate phase.

---

## 12. Successor authorisation

**No successor phase is authorized by this merge.**

In particular, the merge does NOT authorize:

- Phase 4bb-C (docs-and-code eligibility-gate primitive implementation),
- Phase 4bb-D (docs-only eligibility-gate extension to additional dataset families),
- Phase 5,
- Phase 4 canonical,
- additional acquisition (additional UTC days, ETHUSDT, alt symbols, monthly archives),
- eligibility-gate primitive implementation,
- gate execution as a new tool,
- gate report generation,
- transitioning any aggTrades dataset out of `eligibility_gate_status=pending`,
- flipping `research_eligible` to `true`,
- normalization of the Phase 4az dataset into Parquet / JSONL / DuckDB,
- feature computation,
- ML model creation,
- strategy candidate creation,
- entry / exit design,
- backtest plan or backtest execution,
- old-strategy alt-symbol reruns,
- R3 / R2 / V1-arc rescue,
- 5m research thread reopening,
- 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition,
- Binance API endpoint calls,
- REST polling,
- WebSocket connections,
- live REST implementation,
- live WebSocket implementation,
- order-book reconstruction,
- replay implementation,
- paper / shadow,
- live-readiness,
- deployment,
- exchange-write,
- production keys,
- authenticated APIs,
- private endpoints,
- user stream,
- listenKey lifecycle,
- MCP, Graphify, `.mcp.json`,
- credentials.

Any successor phase requires a separate operator authorization brief. Phase 4bb-C (docs-and-code eligibility-gate primitive implementation) and Phase 4bb-D (docs-only extension to additional dataset families) are documented as possible future paths but are **not** activated by this merge.

---

## 13. Recommended state

**Recommended state remains paused.** The Phase 4bb-B memo, closeout, and `current-project-state.md` update are now on `main`. The Phase 4az dataset's eligibility flags are unchanged. The execution plan is recorded for any future Phase 4bb-C / Phase 4bb-D planner. No further work should occur until the operator separately authorizes a future phase.

---

## 14. Final note

This merge-closeout is preserved alongside the Phase 4bb-B memo and the Phase 4bb-B closeout under `docs/00-meta/implementation-reports/`. The merge is intentionally `--no-ff` so the Phase 4bb-B commit history is preserved and the boundary between Phase 4bb-A (docs-only structural QA interpretation) and Phase 4bb-B (docs-only execution-plan memo) remains visible in `git log`.

**Phase 4bb-B is now merged into `main`. No next phase is authorized.**
