# Phase 4bc — Merge Closeout

**Phase identity:** Phase 4bc — AggTrades Normalization Design Memo.
**Type:** docs-only normalization-design memo.
**Date:** 2026-05-07.
**Action:** merge into `main`.

---

## 1. Merge purpose

To merge the Phase 4bc AggTrades Normalization Design Memo from the Phase 4bc feature branch into `main`. Phase 4bc is text-only. It defines a future normalized derived aggTrades dataset family (proposed name: `microstructure_normalized_aggtrades_v001`) — its schema, manifest contract, transformation rules, validation checks, eligibility model, and governance — that may be produced from the Phase 4az raw aggTrades archive **only after** a separately authorized normalization-implementation phase.

The merge brings forward only the three Phase 4bc tracked-doc changes. It does **not** modify source code, tests, scripts, configs, `pyproject.toml`, `README.md`, `.gitignore`, M0 governance, strategy specs, validation checklists, phase-gates, runtime docs, or MCP files; it does **not** implement a normalizer, run a normalizer, generate a normalized derived dataset, create a successor manifest, or modify any file under `data/microstructure/`; it does **not** rerun the gate, generate a new gate report, or modify the existing Phase 4bb-D gate report or its sidecar; it does **not** acquire data, call any Binance / public / private endpoint, open any WebSocket, use any credential, read or create `.env`, create or read `.mcp.json`, or enable MCP / Graphify; it does **not** flip `research_eligible` or transition the actual manifest's `eligibility_gate_status`; it does **not** authorize any successor phase. The actual on-disk Phase 4az manifest still has `research_eligible=false` and `eligibility_gate_status=pending`; the dataset remains **infrastructure evidence only**.

---

## 2. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4bc/aggtrades-normalization-design` |

---

## 3. SHAs

| Item | SHA |
| ---- | --- |
| `main` before merge | `f231a09baae7872eab2fff62e7cebb11e60c3582` |
| Phase 4bc commit | `fdacbfc3abbdf3a082cfbdacce0081e639f747e2` (`docs(phase-4bc): design aggtrades normalization`) |
| Source branch HEAD | `fdacbfc3abbdf3a082cfbdacce0081e639f747e2` |
| Source / origin in sync at start | yes (`main == origin/main == f231a09b`) |
| Phase 4bb-E merge commit ancestry | `2962a72b481858cab0264657cb0de3b2ee0648d7` confirmed ancestor of `main` (`git merge-base --is-ancestor` returns 0) |
| Phase 4bb-E merge-closeout file present on `main` before merge | yes — `docs/00-meta/implementation-reports/2026-05-07_phase-4bb-e_merge-closeout.md` |
| Merge method | `git merge --no-ff` (ort strategy) |
| Merge commit SHA | `07729df9f378452c6d1049172747dcd3e3e34a9d` (`docs(phase-4bc): merge aggtrades normalization design`, `Merge: f231a09 fdacbfc`) |
| Final `main` SHA after push | `07729df9f378452c6d1049172747dcd3e3e34a9d` |
| Final `origin/main` SHA after push | `07729df9f378452c6d1049172747dcd3e3e34a9d` |
| Local / origin sync after push | in sync |

The Phase 4bc merge-closeout commit (this file) is added on top of the merge commit on `main`. Its SHA appears in the operator report after this file is committed.

---

## 4. Files brought forward by the merge

The merge brought forward exactly three tracked file changes from the Phase 4bc source branch:

| File | Change | Lines |
| ---- | ------ | -----:|
| `docs/00-meta/implementation-reports/2026-05-07_phase-4bc_aggtrades-normalization-design.md` | added | +661 |
| `docs/00-meta/implementation-reports/2026-05-07_phase-4bc_closeout.md` | added | +196 |
| `docs/00-meta/current-project-state.md` | modified | +350 |

Total diff summary: **3 files changed, 1207 insertions(+)**.

No code under `src/prometheus/` modified. No test under `tests/` modified. No file under `scripts/` modified. No `pyproject.toml` change. No `README.md` change. No `.gitignore` change. No file under `data/`, `data/manifests/`, `data/research/`, `data/derived/`, `data/raw/`, `data/normalized/`, `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, or `data/microstructure/gate-reports/` modified. No M0 governance amendment. No phase-gate, strategy-spec, validation-checklist, runtime-doc, or MCP file modified.

---

## 5. Design conclusions (recorded by Phase 4bc)

- **Proposed normalized family:** `microstructure_normalized_aggtrades_v001`.
- **Family relationship:** derived; separate from the raw family `microstructure_raw_aggtrades_v001`. Never overwrites the raw family.
- **Raw-family permanence:** `microstructure_raw_aggtrades_v001` remains `research_eligible=false` **permanently**, regardless of any future gate or normalization outcome.
- **Schema scope:** trade-record-level only. The proposed v001 schema has 19 columns (`dataset_family`, `dataset_version`, `source_dataset_family`, `source_dataset_version`, `symbol`, `utc_date`, `agg_trade_id`, `price`, `quantity`, `first_trade_id`, `last_trade_id`, `transact_time_ms`, `is_buyer_maker`, `source_file_sha256`, `source_manifest_sha256`, `source_gate_report_id`, `source_gate_report_sha256`, `row_index`, `normalization_schema_version`).
- **Forbidden columns at v001:** any feature, label, signal, return, alpha, edge, opportunity-rate, taker-imbalance, sweep-detection, aggressive-flow-score, spread, depth, liquidity, slippage, order-flow, execution-quality, regime, trend, momentum, volatility, MFE / MAE, R-multiple, PnL, equity, position, or strategy column.
- **Transformation discipline:** lossless one-to-one row mapping; no row dropped, reordered, or duplicated; no float precision loss; raw artefacts byte-immutable across the run.
- **Numeric precision:** `price` and `quantity` are stored as Decimal-parsable **strings**; float storage is **forbidden**.
- **Timestamps:** UTC milliseconds `int64`; half-open day bounds enforced; no float; no local time.
- **Partitioning:** deterministic and symbol/date-based at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet` (under the gitignored `data/microstructure/` namespace).
- **Manifest contract:** the future normalized manifest must reference the source manifest path + SHA, the raw zip SHA, the Phase 4bb-D gate `report_id`, the gate report SHA `96f09159...`, and the gate `code_commit_sha = aa612ba2...`, all under `governance_labels`. Defaults: `research_eligible=false`, `eligibility_gate_status=pending`.
- **Invalid-window propagation:** source-derived invalid windows propagated verbatim (Phase 4az currently has zero); normalization-time invalid windows abort the run; no per-row exclusion mode at v001; no silent forward-fill / interpolation / imputation / replacement.
- **Eligibility staircase (Phase 4ba ladder applied to derived family):** Stage-0 acquired (after a future Phase 4bd run); Stage-1 inspected; Stage-2 gate-passed (sibling successor-state manifest only; never overwrites); Stage-3 research-eligible — **first stage in the entire microstructure data lineage at which `research_eligible=true` is permitted**; Stage-4 feature-cleared.
- **Stage-transition policy:** each transition (Stage-0 → 1, 1 → 2, 2 → 3, 3 → 4) requires its own separately authorized phase. Phase 4bc authorizes none of them.
- **`research_eligible=true` is not allowed** until a future separately authorized Stage-3 transition phase records the transition with cited Stage-2 gate-passed evidence + Phase 4ak M0 admissibility + operator authorization.
- **27-check normalization-time validation set** is predeclared for any future Phase 4bd implementation (raw manifest exists; cited PASS gate report ID and SHA recorded; raw / zip / sidecar SHAs match; one CSV member; clean decompression; row-count parity; one-to-one mapping; no duplicate `agg_trade_id`; no row dropped except per propagated invalid windows; deterministic ordering; first/last `transact_time_ms` parity; half-open day bounds; numeric precision preserved; no feature columns; manifest references all source evidence; output path under gitignored normalized namespace; raw artefacts byte-immutable across the run; derived manifest defaults; static no-network / no-credentials / no-MCP scan).
- **18-criterion future Phase 4bd acceptance criteria** are predeclared.
- **12 fail-closed rules** are predeclared.
- **Doubled `gate-reports/gate-reports/` path:** does NOT block normalization design; harmless for the existing Phase 4bb-D report; should be fixed in a separately authorized future Phase 4bb-F before any future repeated gate execution.
- **Phase 4bc explicitly does NOT authorize:** Phase 4bd (normalizer implementation), Phase 4bd-A (intermediate planning memo), Phase 4bb-F (output-path hygiene), Phase 4bb-G (sibling successor-state manifest), Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, live WebSocket, MCP, Graphify, `.mcp.json`, credentials, additional acquisition, normalization implementation, features, ML, strategy, or backtest.

---

## 6. Local gitignored gate report reference

| Item | Value |
| ---- | ----- |
| Report path | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` |
| Sidecar path | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json.sha256` |
| Report SHA256 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Recomputed SHA256 at merge time | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| SHA match | yes — bit-for-bit identical to sidecar |
| Local presence at merge time | present in this workspace (17,053 bytes report; 140 bytes sidecar) |
| Committed to repository? | no — gitignored under `.gitignore:85: data/microstructure/` |

The Phase 4bb-D gate report is not committed and was not modified by Phase 4bc or by this merge. Phase 4bc's design references the report by SHA + path + `report_id` + `code_commit_sha` + status + counts in tracked Markdown only. The doubled `gate-reports/gate-reports/` segment in the report path is observed Phase 4bb-C orchestrator behavior and was not changed by Phase 4bc.

---

## 7. Validation results

| Gate | Result |
| ---- | ------ |
| `git diff --stat main...HEAD` (on branch, pre-merge) | exactly the three Phase 4bc tracked-doc changes (+1207 lines) |
| `git diff --name-only main...HEAD` | three Phase 4bc tracked-doc paths only |
| `ruff check .` | PASS (`All checks passed!`) |
| `pytest tests/research/microstructure/` | PASS (258 passed in ~3 s) |
| `pytest` (whole repo) | 1041 passed, 2 failed |
| The 2 failures | `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`; both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`; both pre-existing on `main` before Phase 4bc (zero new regressions) |
| `mypy` (whole repo, strict) | `Success: no issues found in 93 source files` |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/` |
| `git status` post-merge | clean working tree on `main`; only the always-untracked `.claude/scheduled_tasks.lock` and gitignored `data/research/` listed |

Phase 4bc introduced zero new regressions.

---

## 8. Boundary confirmations

| Boundary | Preserved? |
| -------- | :--------: |
| No source code change | yes |
| No test change | yes |
| No script change | yes |
| No config change | yes |
| No `.gitignore` change | yes |
| No M0 governance change | yes |
| No data acquisition | yes |
| No public-endpoint calls | yes |
| No Binance API calls | yes |
| No WebSocket | yes |
| No credential / `.env` / `.mcp.json` / MCP / Graphify | yes |
| No data normalization occurred | yes |
| No derived dataset created | yes |
| No feature computation | yes |
| No ML / strategy / backtest | yes |
| No mutation of `data/microstructure/` | yes |
| Original Phase 4az manifest unchanged | yes |
| Phase 4bb-D gate report unchanged (present this workspace; SHA recomputed identical) | yes |
| `research_eligible` for raw family stays `false` | yes |
| `eligibility_gate_status` stays `pending` | yes |
| No retained verdict revised | yes |
| No project lock loosened | yes |
| No M0 amendment | yes |
| No successor authorized | yes |

---

## 9. Retained verdict ledger (preserved verbatim)

| Family | Status |
| ------ | ------ |
| H0 | FRAMEWORK ANCHOR |
| R3 | BASELINE-OF-RECORD |
| R1a | RETAINED — NON-LEADING |
| R1b-narrow | RETAINED — NON-LEADING |
| R2 | FAILED — §11.6 |
| F1 | HARD REJECT |
| D1-A | MECHANISM PASS / FRAMEWORK FAIL |
| 5m thread | OPERATIONALLY CLOSED (Phase 3t) |
| V2 | HARD REJECT — terminal for V2 first-spec |
| G1 | HARD REJECT — terminal for G1 first-spec |
| C1 | HARD REJECT — terminal for C1 first-spec |

No retained verdicts were revised by Phase 4bc or by this merge.

---

## 10. Project locks (preserved verbatim)

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7 strict integrity gate; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.

No project locks were changed by Phase 4bc or by this merge. M0 was not amended.

---

## 11. No-rescue constraints (preserved verbatim)

Phase 4bc did not authorize and explicitly forbids:

- R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / H0-prime;
- F1-prime / D1-A-prime / D1-B;
- V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- G1-prime / G1-narrow / G1-extension / G1 hybrid;
- C1-prime / C1-narrow / C1-extension / C1 hybrid;
- V1-D1 / F1-D1 / any cross-strategy hybrid;
- M0 amendment derived from Phase 4bc reasoning;
- reopening the 5m research thread;
- flipping `research_eligible` to `true` on any raw aggTrades family;
- flipping `research_eligible` to `true` on any derived normalized family without the full Stage-0 → Stage-3 evidence chain;
- transitioning the raw manifest's `eligibility_gate_status` from `pending` to `pass` without a separately authorized successor-state phase that preserves the original raw manifest byte-identically;
- normalization implementation, feature computation, ML training, strategy implementation, or backtest based on the Phase 4bc design alone;
- additional data acquisition justified by the Phase 4bc design;
- paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

---

## 12. Successor authorization

**No successor phase is authorized by the Phase 4bc merge.**

Specifically:

- no Phase 4bd (AggTrades Normalization Implementation);
- no Phase 4bd-A (intermediate Normalization Implementation Plan Memo);
- no Phase 4bb-F (Gate Report Output Path Hygiene);
- no Phase 4bb-G (Raw Manifest Successor-State Recording);
- no Phase 5;
- no Phase 4 canonical;
- no additional acquisition;
- no normalization implementation;
- no features;
- no ML;
- no strategy;
- no backtest;
- no paper / shadow;
- no live-readiness;
- no deployment;
- no exchange-write;
- no production keys;
- no authenticated APIs;
- no private endpoints;
- no user stream;
- no MCP / Graphify / `.mcp.json` / credentials.

A future docs-and-code Phase 4bd (or docs-only Phase 4bd-A planning intermediate) is the conditional next option only if the operator wants to begin moving toward implementation; it must implement the design defined in the Phase 4bc memo and produce Stage-0 derived artefacts only. A future code-and-docs Phase 4bb-F (gate-report output-path hygiene) is the conditional cleanup option only before any future repeated gate execution. A future docs-and-local-gitignored-output (or docs-and-code) Phase 4bb-G (raw-manifest successor-state recording) is the conditional policy-marker option only if the operator wants a machine-readable Stage-2 marker on the raw manifest. None of these are authorized by Phase 4bc or by this merge.

---

## 13. Recommended state

**Recommended state: remain paused. No next phase authorized.**

The Phase 4az dataset's eligibility flags are unchanged: `research_eligible = false`; `eligibility_gate_status = pending`. The Phase 4bb-D PASS gate report exists locally under the gitignored `data/microstructure/gate-reports/` namespace; it is not committed; its SHA256 (`96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`) is the pinning hash recorded in tracked Markdown. Phase 4bc does not authorize any further work.

Phase 4 (canonical) remains unauthorized. Phase 4bd / Phase 4bd-A / Phase 4bb-F / Phase 4bb-G / Phase 5 / any successor phase remains unauthorized. Paper / shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, exchange-write, and additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition all remain unauthorized.
