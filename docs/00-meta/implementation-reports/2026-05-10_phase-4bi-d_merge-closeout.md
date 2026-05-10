# Phase 4bi-D Merge Closeout — Feature-Family Successor-State Recording

## Status

**MERGED** to `main`.

## Phase identity

- **Phase:** 4bi-D — Feature-Family Successor-State Recording
- **Type:** docs + local gitignored successor-state artefact recording
- **Action:** merge into `main`
- **Merge purpose:** record on `main` the documentation evidence of the Phase 4bi-D successor-state recording (one local gitignored sibling JSON + paired SHA256 sidecar) that translates the Phase 4bi-C Stage-5 policy decision into a machine-readable marker for `microstructure_features_aggtrades_v001`, while preserving all source artefacts, manifest state, retained verdicts, and project locks unchanged

## Branches and SHAs

| Item | Value |
| --- | --- |
| Source branch | `phase-4bi-d/feature-family-successor-state-recording` |
| Target branch | `main` |
| Source HEAD | `1c3a061d75e6f55e6f88a2bc3128f5f8da57f5d6` (Phase 4bi-D source commit) |
| `main` before merge | `b3bb6dbe7dceb097af0346cf0e7318ff48669b28` |
| Merge commit (`--no-ff`) | `b69052e75f18fff0fbebc7983cfe77986638fd3b` |
| `main` / `origin/main` after push | `b69052e75f18fff0fbebc7983cfe77986638fd3b` |
| Phase 4bi-C merge ancestor (verified) | `62bba715a08a5b29e31bca125041f51a2a6f9ddc` |
| Code commit SHA recorded inside Phase 4bi-D successor-state JSON | `b3bb6dbe7dceb097af0346cf0e7318ff48669b28` |
| Merge method | `--no-ff`, `ort` strategy |
| Merge message | `docs(phase-4bi-d): merge feature-family successor-state recording` |
| Merge timestamp (UTC+1) | `2026-05-10T22:04:11+01:00` |

## Files brought forward at merge

Total diff summary: **3 files changed, 885 insertions(+), 0 deletions(-)**.

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-d_feature-family-successor-state-recording.md` (+380 lines; the 18-section main memo)
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-d_closeout.md` (+166 lines; standard closeout)
- `docs/00-meta/current-project-state.md` (+339 lines; new Phase 4bi-D narrative paragraph + new "Current phase:" code block; prior Phase 4bi-C paragraph and code block preserved as historical context)

No source code, tests, scripts, configs, README, pyproject, `.gitignore`, M0 governance source files, MCP files, manifests, gate reports, prior successor-state artefacts, feature artefacts, or any tracked file under `data/` or `data/microstructure/` was modified by Phase 4bi-D or by this merge.

## Local gitignored successor-state output

| Item | Value |
| --- | --- |
| JSON path | `data/microstructure/successor-state/microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json` |
| JSON SHA256 | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |
| JSON size | 4 428 bytes |
| Sidecar path | `data/microstructure/successor-state/microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json.sha256` |
| Sidecar size | 160 bytes |
| Sidecar match | matches recomputed bytes |
| `created_at_unix_ms` (recorded inside JSON) | `1778445390206` |
| `created_at_utc` (recorded inside JSON) | `2026-05-10T20:36:30.206830Z` |
| Gitignore | both files gitignored under `.gitignore:85: data/microstructure/` |
| Tracked in git | NO — both files are gitignored and are NOT committed |

## Successor-state interpretation

- A machine-readable Stage-5 successor-state marker now exists for the feature family `microstructure_features_aggtrades_v001`.
- The marker exists **only** as a sibling gitignored successor-state JSON; it is **not** on the feature manifest and **not** in any committed git tree.
- `successor_state_type = "feature_family_stage5_research_ml_admissibility"`
- `successor_stage = "Feature Stage-5"`
- `successor_research_ml_admissible = true`
- `successor_research_eligible = true`
- `successor_eligibility_gate_status = "pass"`
- `successor_policy_decision_phase = "4bi-C"`
- `successor_policy_decision_outcome = "Outcome 1 / Decision form 1"`
- `original_feature_manifest_research_eligible = false` (unchanged)
- `original_feature_manifest_eligibility_gate_status = "pending"` (unchanged)
- `original_feature_manifest_must_remain_byte_identical = true`
- `manifest_mutation_permitted = false`
- The actual feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` continues to carry `research_eligible=false` and `eligibility_gate_status=pending`.
- Labels remain forbidden.
- Targets remain forbidden.
- ML remains forbidden.
- Strategy remains forbidden.
- Backtests remain forbidden.
- Acquisition remains unauthorized.
- Phase 4bj-A is **not** authorized by Phase 4bi-D.
- No successor phase is authorized.

## Validation evidence

- `git diff --check` — clean.
- `ruff check .` (whole repo) — `All checks passed!`.
- `pytest tests/research/microstructure/` — **666 passed**.
- `pytest` (whole repo) — **1 449 passed, 2 failed**. The two failures are the unchanged pre-existing simulation failures (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`). **Zero new test regressions** from Phase 4bi-D.
- `mypy` (whole repo, strict) — `Success: no issues found in 110 source files`.
- `git check-ignore -v data/microstructure/` — `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/` — gitignored under `.gitignore:85`.
- `git check-ignore -v data/microstructure/features/` — gitignored under `.gitignore:85`.
- `git check-ignore -v data/microstructure/manifests/` — gitignored under `.gitignore:85`.
- `git check-ignore -v data/microstructure/gate-reports/features/` — gitignored under `.gitignore:85`.

## Upstream immutability evidence

All 10 upstream artefacts remained byte-for-byte unchanged across the entire Phase 4bi-D run, verified pre- and post-run:

| Artefact | SHA256 |
| --- | --- |
| Feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| Normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Phase 4bi-B feature-family gate report | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |

The only new artefact under `data/microstructure/` is the single Phase 4bi-D successor-state JSON plus its paired `.sha256` sidecar; both are gitignored and not committed.

## Boundary confirmations

- no source code modified
- no tests modified
- no scripts modified
- no configs changed
- no README changed
- no `pyproject` changed
- no `.gitignore` changed
- no MCP files changed
- no data acquisition
- no public-endpoint calls
- no Binance API calls
- no WebSocket
- no credential / `.env` / `.mcp.json` / MCP / Graphify
- no normalizer rerun
- no raw eligibility-gate rerun
- no derived-family eligibility-gate rerun
- no feature kernel rerun
- no feature-family eligibility-gate rerun
- no replacement feature parquet
- no replacement feature manifest
- no replacement gate report
- no replacement upstream artefact
- no labels
- no targets
- no signals
- no ML
- no strategy
- no backtest
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output
- no tracked `data/microstructure/` output
- raw-family `research_eligible` remains `false`
- raw-family `eligibility_gate_status` remains `pending`
- original derived manifest `research_eligible` remains `false`
- original derived manifest `eligibility_gate_status` remains `pending`
- feature manifest `research_eligible = false` (unchanged)
- feature manifest `eligibility_gate_status = pending` (unchanged)
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked)
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
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C — all preserved verbatim

## No-rescue constraints

Phase 4bi-D did NOT acquire data; did NOT run the normalizer, raw eligibility gate, derived-family gate, feature kernel, or feature-family eligibility gate; did NOT mutate any source artefact, manifest, sidecar, or gate report; did NOT create labels, targets, signals, ML, strategy, or backtest artefacts; did NOT flip any `research_eligible` flag on any actual manifest; did NOT transition any `eligibility_gate_status` on any actual manifest; did NOT amend M0 governance; did NOT call any endpoint, open any WebSocket, use any credential, read or create `.env`, create or read `.mcp.json`, or enable MCP or Graphify; did NOT authorize any rescue of any cooled-down family.

The single new sibling successor-state JSON records Stage-5 admissibility solely as a policy marker; it does not flip the feature manifest's `research_eligible` field, does not authorize labels / targets / ML / strategy / backtests / acquisition, and explicitly records `manifest_mutation_permitted = false` and `original_feature_manifest_must_remain_byte_identical = true`.

## Successor authorization

**None.** This merge does not authorize:

- Phase 4bj-A (Label Boundary / Target Definition Memo)
- Phase 4bj
- Phase 4bb-F (Gate Report Output Path Hygiene)
- Phase 4bb-G (Raw Manifest Successor-State Recording)
- Phase 5
- Phase 4 canonical
- additional acquisition
- labels
- targets
- signals
- ML implementation
- strategy
- backtest
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- user stream
- MCP / Graphify / `.mcp.json` / credentials

Each successor requires a separate, explicit operator authorization.

## Recommended state

**Remain paused.**

The conditional next step (NOT authorised by this merge) is Phase 4bj-A — Label Boundary / Target Definition Memo (allowed in principle now that a machine-readable Stage-5 admissibility marker exists; authorization is a separate operator decision).
