# Phase 4bc — Closeout

**Phase identity:** Phase 4bc — AggTrades Normalization Design Memo.
**Type:** docs-only normalization-design memo.
**Date:** 2026-05-07.
**Branch:** `phase-4bc/aggtrades-normalization-design`.
**Status:** drafted; pending operator review.

---

## 1. Purpose

Phase 4bc is a docs-only design memo for a future normalized derived aggTrades dataset family (proposed name: `microstructure_normalized_aggtrades_v001`). It defines the schema, manifest contract, transformation rules, validation checks, eligibility model, and governance for a normalized derived family that **may** in the future be produced from the Phase 4az raw aggTrades archive — only after a separately authorized normalization-implementation phase. It changed no source code, no tests, no scripts, no Phase 4az artefacts, no Phase 4bb-D gate report, no project locks, no retained verdicts, and authorizes no successor.

---

## 2. Branch and base

| Item | Value |
| ---- | ----- |
| Branch | `phase-4bc/aggtrades-normalization-design` |
| Base SHA (`main`) | `f231a09baae7872eab2fff62e7cebb11e60c3582` |
| Base parent commit | `docs(phase-4bb-e): add merge closeout` |

(The Phase 4bc documentation commit SHA appears in the operator report after this file is committed. No merge is requested by Phase 4bc.)

---

## 3. Files added / modified

### Added (2 docs files)

- `docs/00-meta/implementation-reports/2026-05-07_phase-4bc_aggtrades-normalization-design.md` (Phase 4bc main memo).
- `docs/00-meta/implementation-reports/2026-05-07_phase-4bc_closeout.md` (this file).

### Modified (1 docs file)

- `docs/00-meta/current-project-state.md` (Phase 4bc narrative paragraph + new "Current phase:" block; prior Phase 4bb-E block preserved as historical context).

### Created (gitignored, NOT committed)

- (none) — Phase 4bc is text-only; no local outputs were generated.

`.gitignore` is unchanged. `pyproject.toml` is unchanged. `README.md` is unchanged. No `scripts/...` entrypoint added or modified. No file under `src/prometheus/` modified. No test under `tests/` modified. No file under `data/`, `data/manifests/`, `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, `data/microstructure/gate-reports/`, `data/research/`, `data/derived/`, `data/raw/`, or `data/normalized/` modified. The Phase 4bb-D gate report and paired sidecar are unchanged at their local gitignored paths.

---

## 4. Headline design conclusions

| Question | Answer |
| -------- | ------ |
| Proposed normalized dataset family name? | `microstructure_normalized_aggtrades_v001` |
| Is the normalized family derived (separate from raw)? | yes — derived; never overwrites the raw family |
| Must the raw family `microstructure_raw_aggtrades_v001` remain `research_eligible=false`? | yes — permanently |
| When may the normalized family become `research_eligible=true`? | only at a separately authorized Stage-3 transition phase, after Stage-0 (Phase 4bd produces it) → Stage-1 (inspected) → Stage-2 (gate-passed via sibling successor-state manifest) → Stage-3 |
| Is the normalized schema trade-record-level? | yes — strictly. Zero feature / label / signal / proxy columns at v001 |
| Is the normalization lossless? | yes — one-to-one mapping; no row dropped, reordered, or duplicated; no float precision loss |
| Are timestamps UTC ms integers? | yes — `transact_time_ms` `int64`; half-open day bounds enforced; no float, no local time |
| Are `price` / `quantity` stored as strings (Decimal-parsable)? | yes — float storage forbidden |
| Is partitioning deterministic and symbol/date-based? | yes — `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet` |
| Does the normalized manifest reference all source evidence? | yes — source manifest path + SHA, raw zip SHA, Phase 4bb-D gate `report_id` + SHA + `code_commit_sha` recorded under `governance_labels` |
| Is invalid-window propagation defined even at v001 with zero current candidates? | yes — source-derived propagated verbatim; normalization-time invalid windows abort the run; no per-row exclusion mode at v001 |
| Does the doubled `gate-reports/gate-reports/` path block normalization design? | no — harmless for the existing Phase 4bb-D report; should be fixed in a separately authorized future Phase 4bb-F before any future repeated gate execution; not a prerequisite for Phase 4bd |
| Does Phase 4bc authorize normalization implementation? | no — explicitly not. A separately authorized Phase 4bd is required |

---

## 5. Recommended posture

| Layer | Recommendation |
| ----- | -------------- |
| Default current state | remain paused — no derived dataset, no Phase 4bd, no Stage-1/2/3/4 transition |
| Conditional next | Phase 4bd — AggTrades Normalization Implementation (docs-and-code; or docs-only intermediate Phase 4bd-A plan memo first); only if separately authorized |
| Conditional cleanup | Phase 4bb-F — Gate Report Output Path Hygiene; only before any repeated production-style gate execution |
| Conditional policy marker | Phase 4bb-G — Raw Manifest Successor-State Recording; only if a machine-readable Stage-2 marker is wanted on the raw manifest |

Phase 4bc does **not** authorize any of these as a binding policy execution. They remain recommendations to a future separately-authorized phase.

---

## 6. Validation

| Gate | Result |
| ---- | ------ |
| `git diff --stat` (pre-docs commit) | empty (no diff) |
| `git diff --name-only` (pre-docs commit) | empty |
| `ruff check .` | PASS (`All checks passed!`) |
| `pytest tests/research/microstructure/` | PASS (258 passed) |
| `pytest` (whole repo) | 1041 passed, 2 failed |
| The 2 failures | `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`; both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`; both pre-existing on `main` before Phase 4bc (zero new regressions) |
| `mypy` (whole repo, strict) | `Success: no issues found in 93 source files` |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/` |
| `git status` post-run, pre-docs commit | working tree clean; only the always-untracked `.claude/scheduled_tasks.lock` and gitignored `data/research/` are listed |

Phase 4bc introduced zero new regressions.

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
| No data normalization (Phase 4bc is design only) | yes |
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

No retained verdicts were revised by Phase 4bc.

---

## 9. Project locks (preserved verbatim)

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7 strict integrity gate; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E results.

No project locks were changed by Phase 4bc. M0 was not amended.

---

## 10. No-rescue constraints (preserved verbatim)

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
- transitioning the raw manifest's `eligibility_gate_status` from `pending` to `pass` without a separately authorized successor-state phase that preserves the original raw manifest byte-identically;
- flipping `research_eligible` to `true` on any derived normalized family without the full Stage-0 → Stage-3 evidence chain;
- normalization implementation, feature computation, ML training, strategy implementation, or backtest based on the Phase 4bc design alone;
- additional data acquisition justified by the Phase 4bc design;
- paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

---

## 11. Successor authorization

**No successor phase is authorized by Phase 4bc.**

Recommended next operator options (each NOT authorized; each requires separate operator authorization):

- Option A — remain paused (primary; no further work).
- Option B — future docs-and-code **Phase 4bd — AggTrades Normalization Implementation** (implements the design defined in the Phase 4bc memo; produces Stage-0 derived artefacts only). Optionally preceded by a docs-only **Phase 4bd-A — AggTrades Normalization Implementation Plan Memo** if the operator wants an extra planning step.
- Option C — future code-and-docs **Phase 4bb-F — Gate Report Output Path Hygiene** (only before any future repeated gate execution).
- Option D — future docs-and-local-gitignored-output (or docs-and-code) **Phase 4bb-G — Raw Manifest Successor-State Recording** (only if the operator wants a machine-readable Stage-2 marker on the raw manifest).

---

## 12. Recommended state

**Recommended state: remain paused. No next phase authorized.**

Phase 4 (canonical) remains unauthorized. Phase 4bd / Phase 4bd-A / Phase 4bb-F / Phase 4bb-G / Phase 5 / any successor phase remains unauthorized. Paper / shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, exchange-write, and additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition all remain unauthorized.

The Phase 4az dataset's eligibility flags are unchanged: `research_eligible = false`; `eligibility_gate_status = pending`. The Phase 4bb-D PASS gate report exists locally under the gitignored `data/microstructure/gate-reports/` namespace; it is not committed; its SHA256 (`96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`) is the pinning hash recorded in tracked Markdown.
