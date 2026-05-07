# Phase 4ba — Merge Closeout

**Phase identity:** Phase 4ba — AggTrades Dataset Eligibility-Gate Review Memo.
**Type:** docs-only governance / eligibility-gate review memo.
**Date:** 2026-05-07.
**Action:** merge into `main`.

---

## 1. Merge purpose

To merge the Phase 4ba aggTrades dataset eligibility-gate review memo from the Phase 4ba feature branch into `main`. Phase 4ba is a docs-only governance memo. It defines exactly what must be true before any aggTrades raw dataset family can become `research_eligible=true` or otherwise usable for downstream research. It is the natural docs-only successor to Phase 4ay (authorization-boundary memo) and Phase 4az (first authorized acquisition).

The merge does **not** acquire data, contact any Binance API endpoint, open any WebSocket, normalise the Phase 4az dataset, compute features, create a strategy candidate, train an ML model, flip `research_eligible` to `true`, transition any dataset out of `eligibility_gate_status=pending`, modify any data or manifest under `data/microstructure/`, modify any source file / test / script under the project, or authorize any successor phase. The Phase 4az dataset's manifest still has `research_eligible=false` and `eligibility_gate_status=pending`; the dataset remains **infrastructure evidence only**.

---

## 2. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4ba/aggtrades-dataset-eligibility-gate-review` |

---

## 3. SHAs

| Item | SHA |
| ---- | --- |
| `main` before merge | `203d9ae6ef71ca95ff77be70542474983f3292b2` |
| Phase 4ba commit | `bc9f645390e7838dc427cd32b1c7f61eb700430d` (`docs(phase-4ba): define aggtrades dataset eligibility gate`) |
| Source branch HEAD | `bc9f645390e7838dc427cd32b1c7f61eb700430d` |
| Source / origin in sync at start | yes |
| Merge method | `git merge --no-ff` (ort strategy) |
| Merge commit SHA | `4f8317a725d36df3ec36d0b6901576d6fb2dc462` (`docs(phase-4ba): merge aggtrades dataset eligibility gate`, `Merge: 203d9ae bc9f645`) |
| Final `main` SHA | `4f8317a725d36df3ec36d0b6901576d6fb2dc462` |
| Final `origin/main` SHA | `4f8317a725d36df3ec36d0b6901576d6fb2dc462` |
| Local / origin sync after push | in sync |

The merge-closeout commit SHA appears in the operator report after `git commit` and `git push`.

---

## 4. Files brought forward by the merge

3 file changes, 1,104 insertions, 0 deletions.

**Added (2 new tracked files):**

```
docs/00-meta/implementation-reports/2026-05-07_phase-4ba_aggtrades-dataset-eligibility-gate-review.md
docs/00-meta/implementation-reports/2026-05-07_phase-4ba_closeout.md
```

**Modified (1 narrow update):**

```
docs/00-meta/current-project-state.md   (Phase 4ba narrative paragraph + new "Current phase:" block; prior Phase 4az block preserved as historical context)
```

**Files NOT modified by the merge:**

- No file under `src/prometheus/`.
- No file under `tests/`.
- No file under `scripts/`.
- No file under `data/microstructure/` (gitignored; Phase 4az artefacts are read-only context).
- No file under `data/manifests/`.
- No file under `data/derived/`, `data/raw/`, `data/normalized/`, or `data/research/`.
- No strategy spec, validation checklist, runtime doc, or governance memo beyond Phase 4ba's own memo + closeout + the narrow `current-project-state.md` update.
- No `pyproject.toml`, `README.md`, or `.gitignore`.
- No M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md` unchanged).

**Local data outputs:** no new local data outputs were created by Phase 4ba. The Phase 4az artefacts under `data/microstructure/` (raw `.zip`, paired `.sha256`, manifest, acquisition log) are byte-identical to their post-Phase-4az state and were not touched by this phase.

---

## 5. Phase 4ba is docs-only

**Confirmed.** Phase 4ba is a docs-only governance / eligibility-gate review memo. Its scope was strictly limited to:

- two new docs files under `docs/00-meta/implementation-reports/` (the 18-section memo and the closeout);
- one narrow update to `docs/00-meta/current-project-state.md` (Phase 4ba narrative paragraph + new "Current phase:" block; prior Phase 4az block preserved verbatim as historical context);
- this merge-closeout.

The memo defines:

- a staged five-stage eligibility ladder (`acquired` Stage 0 → `inspected` Stage 1 → `gate-passed` Stage 2 → `normalized` Stage 3 → `feature-cleared` Stage 4) with `research_eligible=true` flipping only at Stage 3 on a normalized derived family — never on a raw family;
- 45 minimum eligibility-time gate checks across twelve categories (source, checksum, manifest, schema, timestamps, monotonicity, duplicates, row count, symbol / date, archive integrity, invalid windows, cross-cutting);
- a manifest-field contract restated against the Phase 4aw `MicrostructureManifest` shape;
- the seventeen-reason invalid-window taxonomy with severity (`INFO` / `WARN` / `ERROR`) and downstream-action (`FLAG` / `EXCLUDE` / `PROXY_ONLY`) semantics, plus a fail-closed cooldown-and-demotion primitive;
- the dataset-versioning policy (same-version reacquisition vs new-version triggers vs permanent-ineligibility triggers);
- downstream-use permissions in three tiers (before normalization, before feature computation, before ML / strategy / backtest), each requiring a separately authorized successor memo;
- six-category fail-closed rules (unknown / mixed / stale / partial / ambiguous / cross-cutting);
- seven recommended future phase options, with **remain paused** as the primary recommendation and Options B / C / D as allowable but not authorized.

---

## 6. Validation summary

Validation was performed on the Phase 4ba branch immediately before merge.

| Item | Result |
| ---- | ------ |
| `ruff check .` (whole repo) | `All checks passed!` |
| `mypy` (whole repo, strict) | `Success: no issues found in 89 source files` |
| `pytest` (whole repo) | `2 failed, 979 passed in 6.36s` |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/	data/microstructure/` |
| `git diff --check` | clean |
| `git status` (final, on `main`) | clean apart from the persistent transient untracked `.claude/scheduled_tasks.lock` and `data/research/` |

**Whole-repo pytest has 2 failures, both pre-existing on `main` since before Phase 4az and unrelated to the eligibility-gate review; Phase 4ba introduced zero new test regressions.**

The two failures are in `tests/simulation/test_backtest_real_2026_03.py`:

- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_ethusdt`

Both fail with `KeyError: 'trade_count'` raised in the unrelated `src/prometheus/research/data/storage.py:232`. The failures were verified as pre-existing on `main` before Phase 4ba (and indeed before Phase 4az). Phase 4ba is docs-only and does not touch `src/prometheus/research/data/storage.py`, the simulation tests, or any related path.

---

## 7. Boundary confirmations

The Phase 4ba merge confirms verbatim:

- **No data was modified.** The `data/microstructure/` tree is byte-identical to its post-Phase-4az state. The Phase 4az manifest mtime is the original `May 7 21:55`.
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
- **No source / test / script change.** Phase 4ba touched only `docs/00-meta/...` paths.
- **No retained verdict revised.**
- **No project lock loosened.**
- **No M0 governance amended.** `docs/00-meta/m0-mechanism-admissibility-gate.md` is unchanged.
- **No successor phase authorized.**

---

## 8. Retained verdict ledger (preserved verbatim)

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

## 9. Preserved project locks

- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops where applicable.
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent applied verbatim by Phase 4az and reaffirmed by Phase 4ba).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance).
- Phase 4j §11 (OI subset governance).
- Phase 4ak — M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al — refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax, Phase 4ay, Phase 4az results — all preserved verbatim.

No new lock is introduced. No existing lock is loosened.

---

## 10. No-rescue constraints (preserved)

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
- No conversion of Phase 4aq forensic numbers, Phase 4l V2 forensic numbers, Phase 4r G1 active-fraction numbers, Phase 4x C1 forensic numbers, Phase 4az aggTrades counts, or Phase 4ba eligibility-gate enumerations into parameter-selection inputs.
- No M0 amendment derived from Phase 4ba reasoning.
- No flipping of `research_eligible` to `true` for the Phase 4az dataset (or any other raw aggTrades dataset family) without a separately authorized eligibility-gate phase.

---

## 11. Successor authorisation

**No successor phase is authorized by this merge.**

In particular, the merge does NOT authorize:

- Phase 4bb,
- Phase 5,
- Phase 4 canonical,
- a code-level eligibility-gate primitive implementation,
- transitioning any aggTrades dataset out of `eligibility_gate_status=pending`,
- flipping `research_eligible` to `true`,
- normalization of the Phase 4az dataset into Parquet / JSONL / DuckDB,
- feature computation,
- additional aggTrades data acquisition (additional UTC days; ETHUSDT; alt symbols; monthly archives),
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

Any successor phase requires a separate operator authorization brief. Phase 4bb (whether docs-only data-quality interpretation memo, docs-only eligibility-gate execution-plan memo, docs-and-code eligibility-gate primitive implementation, or docs-only extension to additional dataset families) is documented in Phase 4ba memo §16 as a possible future path but is **not** activated by this merge.

---

## 12. Recommended state

**Recommended state remains paused.** The Phase 4ba memo, closeout, and current-project-state update are now on `main`. The Phase 4az dataset's eligibility flags are unchanged. No further work should occur until the operator separately authorizes a future phase.

---

## 13. Final note

This merge-closeout is preserved alongside the Phase 4ba memo and the Phase 4ba closeout under `docs/00-meta/implementation-reports/`. The merge is intentionally `--no-ff` so the Phase 4ba commit history is preserved and the boundary between Phase 4az (real-data acquisition) and Phase 4ba (docs-only eligibility-gate review) remains visible in `git log`.

**Phase 4ba is now merged into `main`. No next phase is authorized.**
