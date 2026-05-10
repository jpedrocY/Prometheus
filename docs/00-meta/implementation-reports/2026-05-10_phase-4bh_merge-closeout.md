# Phase 4bh Merge Closeout — AggTrades Feature Schema / Feature Computation Implementation

## Phase identity

- **Phase id:** Phase 4bh
- **Phase title:** AggTrades Feature Schema / Feature Computation Implementation
- **Type:** code + docs + local gitignored feature artefact implementation and execution
- **Action:** merge into main
- **Merge purpose:** bring the Phase 4bh implementation (5 new source modules + 7 new test files + narrow `__init__.py` re-export update + 2 new docs files + narrow `current-project-state.md` update; 16 tracked files; +5,133 insertions) onto `main`. The phase implements exactly the Phase 4bh-B finalised feature schema, runs the kernel exactly once against the real Phase 4bd normalized aggTrades parquet for BTCUSDT 2025-01-15 (1,681,098 rows), and validates the result against the Phase 4bh-B contract. Local gitignored feature artefacts (parquet + paired `.sha256` sidecar; manifest + paired `.sha256` sidecar) are NOT committed.

## Branches

- **Target branch:** `main`
- **Source branch:** `phase-4bh/aggtrades-feature-computation`

## SHAs

- **`main` SHA before merge:** `e99d2f3e5dcea2ceb8daa3428bbe72fd81d77293`
- **Phase 4bh source commit SHA (final):** `fc47a2eb1940156eb6aa9675d5e565e8276be6f0` (`feat(phase-4bh): implement aggtrades feature computation`)
- **Phase 4bh merge commit SHA:** `03100d4267e0984342c622c88cb204218f953367` (`feat(phase-4bh): merge aggtrades feature computation`)
- **Final `main` / `origin/main` SHA after push:** `03100d4267e0984342c622c88cb204218f953367` (this closeout commit will advance `main` further)
- **Code commit SHA recorded inside feature outputs:** `e99d2f3e5dcea2ceb8daa3428bbe72fd81d77293`

The code commit SHA recorded inside the feature parquet's `feature_config_hash` input set and inside the feature manifest's `code_commit_sha` field is `e99d2f3e5dcea2ceb8daa3428bbe72fd81d77293`. It is recorded separately from the post-merge `main` SHA because the kernel was executed before the source commit existed; it pins the lineage to the `main` baseline at the time of the run.

## Merge method

- `git merge --no-ff phase-4bh/aggtrades-feature-computation`
- ort strategy
- merge commit message: `feat(phase-4bh): merge aggtrades feature computation`
- pushed to `origin/main` (`e99d2f3..03100d4 main -> main`)

## Files brought forward by the merge

### Source

- `src/prometheus/research/microstructure/features_schema.py`
- `src/prometheus/research/microstructure/features_io.py`
- `src/prometheus/research/microstructure/features_compute.py`
- `src/prometheus/research/microstructure/features_manifest.py`
- `src/prometheus/research/microstructure/features_validation.py`
- `src/prometheus/research/microstructure/__init__.py` (narrow re-export update + extended package docstring)

### Tests

- `tests/research/microstructure/_features_fixtures.py`
- `tests/research/microstructure/test_features_schema.py`
- `tests/research/microstructure/test_features_io.py`
- `tests/research/microstructure/test_features_compute.py`
- `tests/research/microstructure/test_features_manifest.py`
- `tests/research/microstructure/test_features_validation.py`
- `tests/research/microstructure/test_features_no_network.py`

### Docs

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bh_aggtrades-feature-computation.md`
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bh_closeout.md`
- `docs/00-meta/current-project-state.md` (narrow Phase 4bh narrative paragraph + new "Current phase:" block; prior Phase 4bh-B block preserved as historical context)

### Total diff summary

`16 files changed, 5133 insertions(+)`

`.gitignore`, `pyproject.toml`, `README.md`, `scripts/...`, all M0 governance source files, strategy specs, validation checklists, phase-gates, runtime docs, MCP files, prior memos, prior gate reports, prior manifests, prior successor-state artefacts, and any tracked file under `data/` or `data/microstructure/` are unchanged.

## Implementation result

- 5 new source modules (`features_schema.py`, `features_io.py`, `features_compute.py`, `features_manifest.py`, `features_validation.py`)
- narrow `__init__.py` re-export update (new public symbols added; no prior export removed)
- 7 new test files (1 fixture builder + 6 test files)
- exact Phase 4bh-B schema implemented: 61-column event-aligned schema in canonical column order
- 45 feature / quality columns implemented (40 windowed = 4 windows × 10 + 3 time-context + 2 quality)
- 16 lineage / identity / metadata columns implemented
- windows implemented: `1s = 1000 ms`, `5s = 5000 ms`, `15s = 15000 ms`, `60s = 60000 ms`
- deferred windows not implemented: `30s`, `5m`
- same-timestamp tie-break `row_index <= R` implemented
- aggressive-side convention implemented: `is_buyer_maker = false → aggressive buy`
- Decimal-as-string quantity semantics implemented (raw price / quantity Decimal-as-string only; quantity sums / aggressive quantities / imbalances Decimal-as-string; quantity means Decimal-as-string nullable; ratios `float64` nullable; log returns `float64` nullable)
- no-network / no-credential static scan implemented
- no scripts added
- no new dependencies beyond existing environment

## Real-run result

- **Source rows:** 1,681,098
- **Feature rows:** 1,681,098
- **Schema columns:** 61
- **Feature / quality columns:** 45
- **Lineage / identity / metadata columns:** 16
- **Compute time:** 48.8 s wall-clock
- **Write time:** 3.8 s wall-clock
- **Validation overall:** `pass`
- **Validation checks:** 135 / 135 PASS
- **`feature_config_hash`:** `49b4ec1fd63688cc11d72ea7286af6efe2bad8ac5c29da0438c0f65d571f0c77`

## Local gitignored feature outputs

All under `data/microstructure/` and covered by `.gitignore:85: data/microstructure/`. **None committed.**

| Artefact | Path | SHA256 | Size |
| --- | --- | --- | --- |
| feature parquet | `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet` | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | 224,382,279 B |
| feature parquet sidecar | same path with `.sha256` suffix | sidecar matches | 112 B |
| feature manifest | `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` | 3,851 B |
| feature manifest sidecar | same path with `.sha256` suffix | sidecar matches | 116 B |

`git check-ignore -v data/microstructure/`, `git check-ignore -v data/microstructure/features/`, and `git check-ignore -v data/microstructure/manifests/` all return `.gitignore:85:data/microstructure/` — the four local feature artefacts are NOT tracked or staged.

## Feature manifest state

- `dataset_family = microstructure_features_aggtrades_v001`
- `dataset_version = v001`
- `feature_schema_version = v001`
- `symbol = BTCUSDT`
- `utc_date = 2025-01-15`
- `row_count = 1681098`
- `invalid_windows = []`
- `research_eligible = false`
- `eligibility_gate_status = pending`
- `governance_labels.phase_id = 4bh`
- `governance_labels.feature_computation = allowed_by_phase_4bh`
- `governance_labels.labels = forbidden`
- `governance_labels.ml = forbidden`
- `governance_labels.strategy = forbidden`
- `governance_labels.backtest = forbidden`
- `governance_labels.acquisition = unauthorized`
- `governance_labels.stop_trigger_domain = trade_price_backtest_candidate`
- all 11 boundary confirmations true: `no_labels`, `no_targets`, `no_signals`, `no_ml`, `no_strategy`, `no_backtest`, `no_acquisition`, `no_network`, `no_credentials`, `no_manifest_mutation`, `no_source_artefact_mutation`

## Feature-stage interpretation

Per Phase 4bh-A's feature-stage model:

- **Feature Stage-1 implementation merged** — REACHED by Phase 4bh.
- **Feature Stage-2 local feature artefacts exist with manifest** — REACHED by Phase 4bh.
- **Feature Stage-3 structurally QA-passed** — NOT REACHED.
- **Feature Stage-4 feature-family eligibility-gate-passed** — NOT REACHED.
- **Feature Stage-5 research-use / ML-use decision** — NOT REACHED.

## Validation results

| Command | Result |
| --- | --- |
| Targeted Phase 4bh tests (6 files) | 92 passed |
| `pytest tests/research/microstructure/` | 589 passed (492 prior + 97 new) |
| `ruff check src/prometheus/research/microstructure tests/research/microstructure` | All checks passed! |
| `ruff check .` (whole repo) | All checks passed! |
| `mypy src/prometheus/research/microstructure` | Success: no issues found in 24 source files |
| `mypy src/prometheus` strict (whole repo) | Success: no issues found in 106 source files |
| Whole-repo `pytest` | 1372 passed, 2 failed; the 2 failures are the unchanged pre-existing simulation `KeyError: 'trade_count'` failures (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`); zero new test regressions |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/	data/microstructure/` |
| `git check-ignore -v data/microstructure/features/` | `.gitignore:85:data/microstructure/	data/microstructure/features/` |
| `git check-ignore -v data/microstructure/manifests/` | `.gitignore:85:data/microstructure/	data/microstructure/manifests/` |

## Upstream immutability evidence

All 7 upstream artefact SHAs are byte-for-byte identical pre- and post-Phase-4bh:

| Artefact | SHA256 |
| --- | --- |
| original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B successor-state JSON | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant was preserved end-to-end (never invoked).

## Boundary confirmations

- no scripts added
- no configs changed
- no `README.md` changed
- no `pyproject.toml` changed
- no `.gitignore` changed
- no M0 governance changed
- no data acquisition
- no public endpoint calls
- no Binance API calls
- no WebSocket
- no credential / `.env` / `.mcp.json` / MCP / Graphify
- no normalizer rerun
- no raw gate rerun
- no derived gate rerun
- no new raw or derived gate report
- no replacement derived manifest
- no replacement raw manifest
- no replacement normalized parquet
- no replacement successor-state artefact
- no labels
- no targets
- no signals
- no ML
- no strategy
- no backtest
- no PnL / MFE / MAE / R-multiple / equity / position-state / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output
- no tracked `data/microstructure/` output
- no mutation of upstream artefacts
- raw-family `research_eligible` remains `false`
- raw-family `eligibility_gate_status` remains `pending`
- original derived manifest `research_eligible` remains `false`
- original derived manifest `eligibility_gate_status` remains `pending`
- feature manifest `research_eligible = false`
- feature manifest `eligibility_gate_status = pending`
- Stage-3 not reached
- Stage-4 not reached
- Stage-5 not reached
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

## Retained verdict ledger (preserved verbatim)

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED per Phase 3t
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

## Preserved project locks

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B results preserved

## No-rescue constraints

Phase 4bh did NOT:

- create labels, targets, or signals
- compute future returns, alpha, edge, prediction, or model score
- compute PnL, MFE, MAE, R-multiple, equity, or position state
- create a strategy
- run any backtest
- train ML
- acquire data
- modify any source artefact, prior gate report, or successor-state artefact
- flip `research_eligible` to `True` on any actual manifest
- transition `eligibility_gate_status` out of `pending` on any actual manifest
- imply paper / shadow / live-readiness / exchange-write
- amend M0 governance
- broaden Phase 4bh-A / 4bh-B recommendations beyond their prior scopes

## Successor authorization

**None.** Phase 4bh does NOT authorize:

- Phase 4bi-A
- Phase 4bi-B
- Phase 4bi-C
- Phase 4bi-D
- Phase 4bj
- Phase 4bb-F
- Phase 4bb-G
- Phase 5
- Phase 4 canonical
- additional acquisition
- Stage-3 structural QA
- Stage-4 feature-cleared status
- Stage-5 research-use / ML-use decision
- labels / targets / signals
- ML / strategy / backtest
- paper / shadow
- live-readiness / deployment
- exchange-write
- production keys
- authenticated APIs / private endpoints / user stream
- MCP / Graphify / `.mcp.json` / credentials

## Recommended state

**Remain paused.**

The conditional next steps (NOT authorized by Phase 4bh):

- Phase 4bi-A — Feature Artefact Structural QA Memo (analysis-and-docs; verifies the on-disk feature parquet against the Phase 4bh-B contract at descriptive QA scope; does not authorize Stage-3 feature transition)
- Phase 4bh-C — Feature Schema Finalization Review / Red-Team Memo (docs-only, only if schema ambiguity worth red-teaming surfaces)
- Phase 4bb-F — Gate Report Output Path Hygiene (docs-and-code cleanup of the doubled `gate-reports/gate-reports/` segment)
- Phase 4bb-G — Raw Manifest Successor-State Recording (sibling successor-state manifest only)

Each requires a separate, explicit operator authorization.
