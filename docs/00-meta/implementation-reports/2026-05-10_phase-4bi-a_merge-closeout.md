# Phase 4bi-A Merge Closeout — Feature Artefact Structural QA

## Status

**MERGED** to `main`.

## Branches and SHAs

| Item | Value |
| --- | --- |
| Source branch | `phase-4bi-a/feature-artefact-structural-qa` |
| Source HEAD | `c878186c2ed45362231debaf9eeea6a1c0581b7d` |
| `main` before merge | `c42f6187f7a3ce3257603a863dbd0dd7770fa36d` |
| Merge commit (`--no-ff`) | `97f9d760698d89900fb4c43d57c7bbc559c8a52e` |
| Phase 4bh merge ancestor | `03100d4267e0984342c622c88cb204218f953367` |
| Merge message | `docs(phase-4bi-a): merge feature artefact structural qa` |
| Merge timestamp (UTC) | `2026-05-10T17:26:49Z` |

## Files brought forward at merge

Three tracked docs files (+828 insertions; 0 deletions):

- `docs/00-meta/current-project-state.md` (+345 lines; Phase 4bi-A narrative paragraph + new "Current phase:" block; prior Phase 4bh block preserved as historical context)
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-a_feature-artefact-structural-qa.md` (+344 lines; main 33-section memo)
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-a_closeout.md` (+139 lines; standard closeout)

No source code, tests, scripts, configs, README, pyproject, .gitignore, or MCP files modified by the merge.

No tracked file under `data/`, `data/microstructure/`, or `data/manifests/` modified by the merge.

## Phase 4bi-A scope (recap)

Read-only structural QA of the Phase 4bh on-disk feature parquet and feature manifest against:

- the Phase 4bh-B finalised feature schema contract,
- the Phase 4bh implementation result, and
- the Phase 4bh merge-closeout evidence.

## QA result

- **Phase 4bi-A explicit structural QA:** 67 / 67 PASS
- **Independent causal spot-checks:** 18 / 18 PASS (rows 0, 5, 100, 1000, 50000, 100000, 500000, 1000000, 1681097 × windows 1s, 60s)
- **Same-timestamp tie-break inspection:** PASS (verified at first same-T pair `(14, 15)`: `count_1s[15] == count_1s[14] + 1`)
- **`validate_feature_dataset` (read-only re-run):** `overall_status = pass`; 135 / 135 checks PASS

## Local gitignored artefacts (NOT committed; preserved unchanged)

Phase 4bh feature outputs at the gitignored paths:

| Artefact | SHA256 | Size |
| --- | --- | --- |
| Feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | 224,382,279 B |
| Feature parquet sidecar | matches recomputed bytes | 112 B |
| Feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` | 3,851 B |
| Feature manifest sidecar | matches recomputed bytes | 116 B |

## Upstream artefact immutability evidence

All 7 upstream artefacts byte-for-byte unchanged across the entire Phase 4bi-A run:

| Artefact | SHA256 |
| --- | --- |
| Original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |

## Manifest state preservation

- Raw manifest `research_eligible = false` / `eligibility_gate_status = pending` (unchanged).
- Original derived manifest `research_eligible = false` / `eligibility_gate_status = pending` (unchanged).
- Feature manifest `research_eligible = false` / `eligibility_gate_status = pending` (unchanged).
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved end-to-end (never invoked).

## Validation evidence (pre-merge and post-merge)

- `git diff --check` — clean.
- `ruff check .` (whole repo) — `All checks passed!`
- `pytest tests/research/microstructure/` — 589 passed.
- `pytest` (whole repo) — 1372 passed, 2 failed; the two failures are the same pre-existing simulation failures (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`). Zero new test regressions from Phase 4bi-A.
- `mypy src/prometheus` (strict) — `Success: no issues found in 106 source files`.
- `git check-ignore -v data/microstructure/` — `.gitignore:85:data/microstructure/	data/microstructure/`.
- `git check-ignore -v data/microstructure/features/` — gitignored under `.gitignore:85`.
- `git check-ignore -v data/microstructure/manifests/` — gitignored under `.gitignore:85`.

## Boundary confirmations

- no source code modified
- no tests modified
- no scripts modified
- no configs / README / pyproject / .gitignore / MCP files modified
- no data acquisition
- no public-endpoint calls
- no Binance API calls
- no WebSocket
- no credentials / `.env` / `.mcp.json` / MCP / Graphify
- no normalizer rerun
- no raw eligibility-gate rerun
- no derived-family eligibility-gate rerun
- no new gate report
- no replacement feature parquet
- no replacement feature manifest
- no replacement upstream artefact
- no successor-state artefact created
- no labels / targets / signals / ML / strategy / backtest artefacts
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output
- no tracked `data/microstructure/` output
- raw-family `research_eligible` remains `false`
- raw-family `eligibility_gate_status` remains `pending`
- original derived manifest `research_eligible` remains `false`
- original derived manifest `eligibility_gate_status` remains `pending`
- feature manifest `research_eligible = false`
- feature manifest `eligibility_gate_status = pending`
- Stage-3 reached at memo level only (structural QA on local one-day artefact)
- Stage-4 NOT reached
- Stage-5 NOT reached
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

## Retained verdict ledger (preserved verbatim)

- H0 FRAMEWORK ANCHOR
- R3 BASELINE-OF-RECORD
- R1a / R1b-narrow RETAINED — NON-LEADING
- R2 FAILED — §11.6
- F1 HARD REJECT
- D1-A MECHANISM PASS / FRAMEWORK FAIL
- 5m thread OPERATIONALLY CLOSED per Phase 3t
- V2 HARD REJECT — terminal for V2 first-spec
- G1 HARD REJECT — terminal for G1 first-spec
- C1 HARD REJECT — terminal for C1 first-spec

## Project locks (preserved verbatim)

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
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D, 4bb-E, 4bc, 4bd-A, 4bd, 4be, 4bf-A, 4bf, 4bg-A, 4bg-B, 4bh-A, 4bh-B, 4bh

## No-rescue constraints

Phase 4bi-A did NOT compute features, labels, targets, signals, ML, strategy, or backtests; did NOT modify any source code, tests, scripts, or feature artefact; did NOT mutate any upstream artefact; did NOT flip any `research_eligible` flag; did NOT transition any `eligibility_gate_status`; did NOT amend M0 governance.

## Successor authorization

**None.** This merge does not authorize:

- Phase 4bi-B (Feature-Family Eligibility-Gate Design + Implementation + Execution)
- Phase 4bi-C, Phase 4bi-D, Phase 4bj, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical
- additional acquisition
- Stage-4 feature-cleared status
- Stage-5 research-use / ML-use decision
- labels / targets / signals / ML / strategy / backtest
- paper / shadow / live-readiness / deployment / exchange-write
- production keys / authenticated APIs / private endpoints / user stream
- MCP / Graphify / `.mcp.json` / credentials

Each successor requires a separate, explicit operator authorization.

## Recommended state

**Remain paused.**

The next conditional step (NOT authorised by this merge) is Phase 4bi-B — Feature-Family Eligibility-Gate Design + Implementation + Execution.
