# Phase 4bd-A — Closeout

**Phase identity:** Phase 4bd-A — AggTrades Normalization Implementation Plan Memo.
**Type:** docs-only implementation-plan memo.
**Date:** 2026-05-07.
**Branch:** `phase-4bd-a/aggtrades-normalization-implementation-plan`.
**Status:** drafted; pending operator review.

---

## 1. Purpose

Phase 4bd-A is a docs-only planning memo for a future Phase 4bd AggTrades Normalization Implementation. It translates the Phase 4bc design into a precise file-by-file, function-by-function implementation plan. It changed no source code, no tests, no scripts, no Phase 4az artefacts, no Phase 4bb-D gate report, no project locks, no retained verdicts, and authorizes no successor.

---

## 2. Branch and base

| Item | Value |
| ---- | ----- |
| Branch | `phase-4bd-a/aggtrades-normalization-implementation-plan` |
| Base SHA (`main`) | `53914b88dfaf3459a9fc56c4c7fd31a40e6d5b3e` |
| Base parent commit | `docs(phase-4bc): add merge closeout` |

(The Phase 4bd-A documentation commit SHA appears in the operator report after this file is committed. No merge is requested by Phase 4bd-A.)

---

## 3. Files added / modified

### Added (2 docs files)

- `docs/00-meta/implementation-reports/2026-05-07_phase-4bd-a_aggtrades-normalization-implementation-plan.md` (Phase 4bd-A main memo).
- `docs/00-meta/implementation-reports/2026-05-07_phase-4bd-a_closeout.md` (this file).

### Modified (1 docs file)

- `docs/00-meta/current-project-state.md` (Phase 4bd-A narrative paragraph + new "Current phase:" block; prior Phase 4bc block preserved as historical context).

### Created (gitignored, NOT committed)

- (none) — Phase 4bd-A is text-only; no local outputs were generated.

`.gitignore` is unchanged. `pyproject.toml` is unchanged. `README.md` is unchanged. No `scripts/...` entrypoint added or modified. No file under `src/prometheus/` modified. No test under `tests/` modified. No file under `data/`, `data/manifests/`, `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, `data/microstructure/gate-reports/`, `data/research/`, `data/derived/`, `data/raw/`, or `data/normalized/` modified. The Phase 4bb-D gate report and paired sidecar are unchanged at their local gitignored paths.

---

## 4. Headline plan conclusions

| Question | Answer |
| -------- | ------ |
| Proposed source modules under `src/prometheus/research/microstructure/`? | `normalize_io.py`, `normalize_aggtrades.py`, `normalize_manifest.py`, `normalize_validation.py`, plus narrow `__init__.py` re-export update |
| Proposed test files under `tests/research/microstructure/`? | `test_normalize_io.py`, `test_normalize_aggtrades.py`, `test_normalize_manifest.py`, `test_normalize_validation.py`, `test_normalize_no_network.py` (plus optional `_normalize_fixtures.py` shared fixture builder) |
| Proposed public API symbols? | `NormalizeAggTradesInput`, `NormalizeAggTradesResult`, `NormalizedAggTradeRow`, `NormalizationManifestDraft`, `NormalizationValidationResult`, `NormalizationCheckResult`, `NormalizationCheckStatus`, `NormalizationIOError`, `NormalizationValidationError`, `run_normalize_aggtrades` |
| Future Phase 4bd execution flow? | 16-step ordered flow: path discipline → source manifest read + hash → sidecar + zip hash → acquisition log hash → gate report citation verification → in-memory zip iteration → per-row Phase 4ax validation → one-to-one mapping with `row_index` counter → schema-equality assertion → atomic Parquet write → file SHA256 → derived manifest builder + atomic write → 27-check validation suite → pre/post raw-artefact hash equality → result construction → Stage-0-only documentation |
| 27-check validation set mapped to functions and tests? | yes — every Phase 4bc check ID `4bc.24.1` .. `4bc.24.27` mapped to a `check_*` function in `normalize_validation.py` and to a positive-test + negative-test pair in `test_normalize_validation.py` (54+ tests minimum) |
| 18-criterion future Phase 4bd acceptance criteria? | enumerated in §22 of the memo |
| Fail-closed conditions? | 16 categories in §23 of the memo |
| Static no-network / no-credentials / no-feature guards? | three-layer: import-boundary scan; credential-pattern scan against dynamically-built `DENYLIST_TOKENS`; module-level `NORMALIZED_SCHEMA_V001` constant + row construction-time field-set assertion |
| Total minimum new test count for future Phase 4bd? | ~90 tests (54 from check-mapping table + ~36 from API / orchestrator / boundary / I/O / manifest / static-scan tests) |
| Does Phase 4bd-A authorize Phase 4bd? | no — explicitly not |

---

## 5. Recommended posture

| Layer | Recommendation |
| ----- | -------------- |
| Default current state | remain paused — no Phase 4bd, no Stage-0 derived artefacts, no derived manifest |
| Conditional next | Phase 4bd — AggTrades Normalization Implementation (docs-and-code; produces Stage-0 derived artefacts only); only if separately authorized; must implement the Phase 4bc design exactly per the Phase 4bd-A plan |
| Conditional cleanup | Phase 4bb-F — Gate Report Output Path Hygiene; only before any repeated production-style gate execution; independent of Phase 4bd |
| Conditional policy marker | Phase 4bb-G — Raw Manifest Successor-State Recording; only if a machine-readable Stage-2 marker is wanted on the raw manifest; independent of Phase 4bd |

Phase 4bd-A does **not** authorize any of these as a binding policy execution. They remain recommendations to a future separately-authorized phase.

---

## 6. Validation

| Gate | Result |
| ---- | ------ |
| `git diff --stat` (pre-docs commit) | empty (no diff) |
| `git diff --name-only` (pre-docs commit) | empty |
| `ruff check .` | PASS (`All checks passed!`) |
| `pytest tests/research/microstructure/` | PASS (258 passed) |
| `pytest` (whole repo) | 1041 passed, 2 failed |
| The 2 failures | `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`; both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`; both pre-existing on `main` before Phase 4bd-A (zero new regressions) |
| `mypy` (whole repo, strict) | `Success: no issues found in 93 source files` |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/` |
| `git status` post-run, pre-docs commit | working tree clean; only the always-untracked `.claude/scheduled_tasks.lock` and gitignored `data/research/` are listed |

Phase 4bd-A introduced zero new regressions.

---

## 7. Boundary confirmations

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
| No data normalization (Phase 4bd-A is plan only) | yes |
| No feature computation | yes |
| No ML / strategy / backtest | yes |
| No mutation of `data/microstructure/` | yes |
| Original Phase 4az manifest unchanged | yes |
| Phase 4bb-D gate report unchanged | yes |
| `research_eligible` for raw family stays `false` | yes |
| `eligibility_gate_status` stays `pending` | yes |
| No retained verdict revised | yes |
| No project lock loosened | yes |
| No successor authorized | yes |

---

## 8. Retained verdict ledger (preserved verbatim)

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

No retained verdicts were revised by Phase 4bd-A.

---

## 9. Project locks (preserved verbatim)

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7 strict integrity gate; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc results.

No project locks were changed by Phase 4bd-A. M0 was not amended.

---

## 10. No-rescue constraints (preserved verbatim)

Phase 4bd-A did not authorize and explicitly forbids:

- R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / H0-prime;
- F1-prime / D1-A-prime / D1-B;
- V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- G1-prime / G1-narrow / G1-extension / G1 hybrid;
- C1-prime / C1-narrow / C1-extension / C1 hybrid;
- V1-D1 / F1-D1 / any cross-strategy hybrid;
- M0 amendment derived from Phase 4bd-A reasoning;
- reopening the 5m research thread;
- flipping `research_eligible` to `true` on any raw aggTrades family;
- transitioning the raw manifest's `eligibility_gate_status` from `pending` to `pass` without a separately authorized successor-state phase that preserves the original raw manifest byte-identically;
- flipping `research_eligible` to `true` on any derived normalized family without the full Stage-0 → Stage-3 evidence chain;
- normalization implementation, feature computation, ML training, strategy implementation, or backtest based on the Phase 4bd-A plan alone;
- additional data acquisition justified by the Phase 4bd-A plan;
- paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

---

## 11. Successor authorization

**No successor phase is authorized by Phase 4bd-A.**

Recommended next operator options (each NOT authorized; each requires separate operator authorization):

- Option A — remain paused (primary; no further work).
- Option B — future docs-and-code **Phase 4bd — AggTrades Normalization Implementation** (implements the Phase 4bc design per the Phase 4bd-A plan; produces Stage-0 derived artefacts only).
- Option C — future code-and-docs **Phase 4bb-F — Gate Report Output Path Hygiene** (only before any future repeated gate execution).
- Option D — future docs-and-local-gitignored-output (or docs-and-code) **Phase 4bb-G — Raw Manifest Successor-State Recording** (only if the operator wants a machine-readable Stage-2 marker on the raw manifest).

---

## 12. Recommended state

**Recommended state: remain paused. No next phase authorized.**

Phase 4 (canonical) remains unauthorized. Phase 4bd / Phase 4be / Phase 4bf / Phase 4bb-F / Phase 4bb-G / Phase 5 / any successor phase remains unauthorized. Paper / shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, exchange-write, and additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition all remain unauthorized.

The Phase 4az dataset's eligibility flags are unchanged: `research_eligible = false`; `eligibility_gate_status = pending`. The Phase 4bb-D PASS gate report exists locally under the gitignored `data/microstructure/gate-reports/` namespace; it is not committed; its SHA256 (`96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`) is the pinning hash recorded in tracked Markdown.
