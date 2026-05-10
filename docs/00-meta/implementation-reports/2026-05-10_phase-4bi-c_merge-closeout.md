# Phase 4bi-C Merge Closeout — Feature-Family Research-Use / ML-Use Decision

## Status

**MERGED** to `main`.

## Phase identity

- **Phase:** 4bi-C — Feature-Family Research-Use / ML-Use Decision Memo
- **Type:** docs-only research-use / ML-use decision memo
- **Action:** merge into `main`
- **Merge purpose:** record the Stage-5 research-use / ML-use admissibility policy decision (Outcome 1 / Decision form 1) for `microstructure_features_aggtrades_v001` on `main` while preserving all source artefacts, manifest state, retained verdicts, and project locks unchanged

## Branches and SHAs

| Item | Value |
| --- | --- |
| Source branch | `phase-4bi-c/feature-family-research-ml-use-decision` |
| Target branch | `main` |
| Source HEAD | `a762c67e9a8edaa15d9e1018e85f76ee0c1e8a86` (Phase 4bi-C source commit) |
| `main` before merge | `ab33cd06724ef0e1e151e5554bb20b13673435aa` |
| Merge commit (`--no-ff`) | `62bba715a08a5b29e31bca125041f51a2a6f9ddc` |
| `main` / `origin/main` after push | `62bba715a08a5b29e31bca125041f51a2a6f9ddc` |
| Phase 4bi-B merge ancestor (verified) | `046ec90ddfefb3c59164740eaf572ce104fb060f` |
| Merge method | `--no-ff`, `ort` strategy |
| Merge message | `docs(phase-4bi-c): merge feature-family research ml-use decision` |
| Merge timestamp (UTC+1) | `2026-05-10T20:41:05+01:00` |

## Files brought forward at merge

Total diff summary: **3 files changed, 1 036 insertions(+), 0 deletions(-)**.

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-c_feature-family-research-ml-use-decision.md` (+529 lines; the 26-section main memo)
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-c_closeout.md` (+159 lines; standard closeout)
- `docs/00-meta/current-project-state.md` (+348 lines; new Phase 4bi-C narrative paragraph + new "Current phase:" code block; prior Phase 4bi-B paragraph and code block preserved as historical context)

No source code, tests, scripts, configs, README, pyproject, `.gitignore`, M0 governance source files, MCP files, manifests, gate reports, successor-state artefacts, feature artefacts, or any tracked file under `data/` or `data/microstructure/` was modified by Phase 4bi-C or by this merge.

## Decision result

**Outcome 1 / Decision form 1 selected:**

> **Stage-5 research-use / ML-use admissibility is admissible in principle at policy level for the feature family `microstructure_features_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bi-D successor-state recording phase is required before any machine-readable Stage-5 marker exists.**

Specifically:

- no manifest mutation occurred during Phase 4bi-C;
- no machine-readable Stage-5 marker has been created;
- a future Phase 4bi-D successor-state recording phase is required before any machine-readable Stage-5 marker exists;
- the original feature manifest remains `research_eligible=false`;
- the original feature manifest remains `eligibility_gate_status=pending`;
- the raw family `microstructure_raw_aggtrades_v001` remains `research_eligible=false` and `eligibility_gate_status=pending`;
- the original derived manifest remains `research_eligible=false` and `eligibility_gate_status=pending`;
- labels remain forbidden;
- targets remain forbidden;
- ML remains forbidden;
- strategy remains forbidden;
- backtests remain forbidden;
- acquisition remains unauthorized;
- no successor phase is authorized.

## Evidence summary

| Evidence | Value |
| --- | --- |
| Phase 4bi-B feature-family gate report SHA256 | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| Phase 4bi-B report `overall_status` | `pass` |
| Phase 4bi-B report checks | 70 / 70 PASS (0 FAIL / 0 ERROR / 0 NOT_APPLICABLE) |
| Phase 4bh validation | 135 / 135 PASS |
| Phase 4bi-A explicit structural QA | 67 / 67 PASS |
| Phase 4bi-A causal spot-checks | 18 / 18 PASS |
| Phase 4bi-A same-timestamp tie-break | PASS |
| Feature parquet SHA256 | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Feature manifest SHA256 | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| Feature config hash | `49b4ec1fd63688cc11d72ea7286af6efe2bad8ac5c29da0438c0f65d571f0c77` |
| Feature row count | `1 681 098` |
| Schema columns | 61 |
| Feature / quality columns | 45 |
| Lineage / identity / metadata columns | 16 |

## Machine-readable state after Phase 4bi-C

| Object | Field | Value |
| --- | --- | --- |
| Feature manifest | `research_eligible` | `false` |
| Feature manifest | `eligibility_gate_status` | `pending` |
| Feature manifest | `governance_labels.labels` | `forbidden` |
| Feature manifest | `governance_labels.ml` | `forbidden` |
| Feature manifest | `governance_labels.strategy` | `forbidden` |
| Feature manifest | `governance_labels.backtest` | `forbidden` |
| Feature manifest | `governance_labels.acquisition` | `unauthorized` |
| Phase 4bi-B gate report | `research_eligible_after` | `false` |
| Phase 4bi-B gate report | `feature_manifest_research_eligible_after` | `false` |
| Phase 4bi-B gate report | `feature_manifest_eligibility_gate_status_after` | `pending` |
| Phase 4bi-B gate report | `stage_5_authorized` | `false` |
| Phase 4bi-B gate report | `stage_5_research_or_ml_use` | `false` |
| Phase 4bi-B gate report | `no_successor_authorization` | `true` |

The Phase 4bi-C policy decision is text-only. No flag has been flipped. No status has been transitioned. No successor-state artefact has been created.

## Required successor-state policy

Any future Phase 4bi-D, if separately authorized, must:

- be docs-and-local-gitignored-output only;
- create exactly one sibling successor-state JSON artefact and exactly one paired `.sha256` sidecar under a gitignored namespace;
- preserve the feature manifest byte-identically (SHA `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718`);
- preserve `research_eligible=false` and `eligibility_gate_status=pending` on the original feature manifest;
- cite this Phase 4bi-C memo as the policy-decision evidence;
- cite the Phase 4bi-B feature-family gate report id and SHA verbatim;
- cite all upstream artefact SHAs verbatim;
- record Stage-5 admissibility (`successor_research_eligible=true`, `successor_eligibility_gate_status=pass`) **only at the sibling successor-state artefact level**, never on the feature manifest;
- record `labels=forbidden`, `targets=forbidden`, `ml=forbidden`, `strategy=forbidden`, `backtest=forbidden`, `acquisition=unauthorized` until a separately authorized further phase changes those;
- not authorize labels, targets, signals, ML, strategy, backtests, or acquisition;
- not authorize Phase 4bj-A (Label Boundary / Target Definition Memo) by itself;
- preserve every retained verdict and project lock verbatim;
- not amend M0;
- not bypass the Phase 4al refined no-rescue rule.

## Validation evidence

- `git diff --check` — clean.
- `ruff check .` (whole repo) — `All checks passed!`.
- `pytest tests/research/microstructure/` — **666 passed**.
- `pytest` (whole repo) — **1 449 passed, 2 failed**. The two failures are the unchanged pre-existing simulation failures (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`). **Zero new test regressions** from Phase 4bi-C.
- `mypy` (whole repo, strict) — `Success: no issues found in 110 source files`.
- `git check-ignore -v data/microstructure/` — `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/features/` — gitignored under `.gitignore:85`.
- `git check-ignore -v data/microstructure/manifests/` — gitignored under `.gitignore:85`.
- `git check-ignore -v data/microstructure/gate-reports/features/` — gitignored under `.gitignore:85`.

## Upstream immutability evidence

All 10 upstream artefacts remained byte-for-byte unchanged across the entire Phase 4bi-C run, verified pre- and post-run:

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

## Boundary confirmations

- no source code modified
- no tests modified
- no scripts modified
- no configs changed
- no README changed
- no `pyproject` changed
- no `.gitignore` changed
- no M0 governance source files changed
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
- no successor-state artefact created
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
- feature manifest `research_eligible = false`
- feature manifest `eligibility_gate_status = pending`
- no machine-readable Stage-5 marker exists yet
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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B — all preserved verbatim

## No-rescue constraints

Phase 4bi-C did NOT acquire data; did NOT run the normalizer, raw eligibility gate, derived-family gate, feature kernel, or feature-family eligibility gate; did NOT mutate any source artefact or manifest; did NOT create labels, targets, signals, ML, strategy, or backtest artefacts; did NOT flip any `research_eligible` flag; did NOT transition any `eligibility_gate_status`; did NOT amend M0 governance; did NOT call any endpoint, open any WebSocket, use any credential, read or create `.env`, create or read `.mcp.json`, or enable MCP or Graphify; did NOT create a successor-state artefact; did NOT authorize any rescue of any cooled-down family.

## Successor authorization

**None.** This merge does not authorize:

- Phase 4bi-D (Feature-Family Successor-State Recording)
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

The conditional next step (NOT authorised by this merge) is Phase 4bi-D — Feature-Family Successor-State Recording.
