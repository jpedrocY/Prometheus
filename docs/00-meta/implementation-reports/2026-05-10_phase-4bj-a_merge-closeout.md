# Phase 4bj-A Merge Closeout — Label Boundary / Target Definition Memo

Date: 2026-05-10
Phase: 4bj-A
Phase type: docs-only label-boundary / target-definition memo
Action: merge into main
Status: COMPLETED

## Merge purpose

Bring the Phase 4bj-A docs-only label-boundary / target-definition
memo into `main`. Phase 4bj-A selects **Outcome 1 — Label boundary
admissible in principle, implementation deferred** for the Stage-5-
admissible feature family `microstructure_features_aggtrades_v001`.

The merge brings forward only docs files. No source code, tests,
scripts, configs, manifests, gate reports, successor-state artefacts,
or data artefacts are introduced. No labels, targets, ML, strategy,
backtests, acquisition, or successor phases are authorized.

## Branches

- **Target branch:** `main`
- **Source branch:** `phase-4bj-a/label-boundary-target-definition`

## Recorded SHAs

- **Phase 4bi-D merge commit (verified ancestor of main):**
  `b69052e75f18fff0fbebc7983cfe77986638fd3b`
- **Phase 4bj-A branch base / post-Phase-4bi-D closeout main SHA
  (verified at start of Phase 4bj-A and again at merge time):**
  `bddc84dd8219295f9f0b809e248c13af66fb0d66`
- **Main SHA before this merge:**
  `bddc84dd8219295f9f0b809e248c13af66fb0d66`
- **Phase 4bj-A source commit SHA:**
  `80e387bdeef07505265b9b44a58e30ba1bb07628`
- **Phase 4bj-A merge commit SHA:**
  `8a99a74930b5c8b33c63e9eceb0116e5e97b11b8`
- **Final main SHA after push:**
  `8a99a74930b5c8b33c63e9eceb0116e5e97b11b8`
- **Final origin/main SHA after push:**
  `8a99a74930b5c8b33c63e9eceb0116e5e97b11b8`

## Merge method

- `git merge --no-ff phase-4bj-a/label-boundary-target-definition`
- Merge strategy: `ort` (automatic; no conflicts)
- Merge commit message:
  `docs(phase-4bj-a): merge label boundary target policy`

## Files brought forward by the merge (tracked)

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-a_label-boundary-target-definition.md`
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-a_closeout.md`
- `docs/00-meta/current-project-state.md`

## Total diff summary from the Phase 4bj-A merge

```
 docs/00-meta/current-project-state.md              |  382 +++++++
 .../2026-05-10_phase-4bj-a_closeout.md             |  190 ++++
 ...phase-4bj-a_label-boundary-target-definition.md | 1083 ++++++++++++++++++++
 3 files changed, 1655 insertions(+)
```

No code, tests, scripts, configs, README, `pyproject.toml`,
`.gitignore`, MCP files, governance source files, strategy specs,
validation checklists, phase-gates, runtime docs, manifests, gate
reports, successor-state artefacts, feature artefacts, label
artefacts, ML artefacts, strategies, or backtest artefacts were
changed.

## Decision result

- **Selected outcome:** Outcome 1 — Label boundary admissible in
  principle, implementation deferred.
- Label boundary admissible in principle at policy level.
- Implementation deferred.
- **No labels created.**
- **No targets created.**
- **No label schema implemented.**
- **No label namespace created.**
- **No label manifest created.**
- **No label gate report created.**
- **No label successor-state created.**
- **No ML authorized.**
- **No strategy authorized.**
- **No backtest authorized.**
- **No acquisition authorized.**
- **No successor authorized.**

## Preferred future label boundary (proposed only; not authorized)

- **Family name (proposed):** `microstructure_labels_aggtrades_v001`
- **Initial label list (proposed):**
  - `forward_log_return_1s`
  - `forward_log_return_5s`
  - `forward_log_return_15s`
  - `forward_log_return_60s`
  - `forward_direction_1s`
  - `forward_direction_5s`
  - `forward_direction_15s`
  - `forward_direction_60s`

## Explicitly deferred label classes

- barrier labels;
- target-before-stop labels;
- MFE / MAE labels;
- R-multiple labels;
- PnL labels;
- strategy-action labels;
- position-state labels;
- execution-quality labels;
- multi-symbol labels;
- cross-sectional labels;
- 30s horizon;
- 5m horizon;
- longer horizons.

## Label boundary principles (recorded as policy)

- labels must be a sibling artefact family, never a mutation of any
  upstream family;
- labels may use future information only inside label computation;
- labels must never feed back into features;
- labels must never normalize, rank, bucket, filter, or mask feature
  rows before split definition;
- labels must be event-aligned to feature rows by default;
- labels must preserve lineage to the feature parquet, feature
  manifest, Phase 4bi-D successor-state, and Phase 4bi-B gate report;
- label manifests default to `research_eligible: false` and
  `eligibility_gate_status: pending`;
- label design does not prove edge;
- direction accuracy is not profitability;
- RR / WR / expectancy are strategy-evaluation concepts, not label-
  schema proof;
- M0 remains binding;
- Phase 4al refined no-rescue rule remains binding.

## Future namespace proposal (not created)

- `data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet`
- `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`
- `data/microstructure/gate-reports/labels/`
- `data/microstructure/successor-state/` (sibling label successor-
  states only; feature-family successor-states must not be modified)

None of the above paths were created by Phase 4bj-A. The entire
`data/microstructure/` tree remains gitignored under `.gitignore:85`.

## Future sequence (proposed only; none authorized)

- Phase 4bj-B — Label Schema Finalization Memo
- Phase 4bj-C — Label Implementation + Local Label Artefact Generation
- Phase 4bj-D — Label Artefact Structural QA Memo
- Phase 4bj-E — Label-Family Eligibility Gate Design + Implementation
  + Execution
- Phase 4bj-F — Label-Family Research / ML-Use Decision Memo
- Phase 4bj-G — Label-Family Successor-State Recording

None of these is authorized by Phase 4bj-A or by this merge-closeout.

## Validation results (recorded at merge time)

- `ruff check .` (whole repo): **All checks passed!**
- `pytest tests/research/microstructure/`: **666 passed** in 8.10s
- `pytest` (whole repo): **1449 passed, 2 failed** — the two failures
  are the same pre-existing simulation failures that have been on
  `main` since before Phase 4bj-A:
  - `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
  - `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_ethusdt`
  - both `KeyError: 'trade_count'` in
    `src/prometheus/research/data/storage.py:232`
  - **zero new regressions from Phase 4bj-A.**
- `mypy src/prometheus` strict: **Success: no issues found in 110
  source files.**
- `git diff --check`: clean.
- `git check-ignore -v data/microstructure/`: covered by
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/`: covered
  by `.gitignore:85`.
- `git check-ignore -v data/microstructure/features/`: covered by
  `.gitignore:85`.
- `git check-ignore -v data/microstructure/manifests/`: covered by
  `.gitignore:85`.
- `git check-ignore -v data/microstructure/gate-reports/features/`:
  covered by `.gitignore:85`.

## Upstream immutability evidence (SHA256 byte-identical pre/post)

| # | artefact | SHA256 |
|---|----------|--------|
| 1 | feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| 2 | feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| 3 | normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| 4 | original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| 5 | raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| 6 | raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| 7 | Phase 4bb-D raw gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| 8 | Phase 4bf derived gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| 9 | Phase 4bg-B successor-state | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| 10 | Phase 4bi-B feature-family gate report | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| 11 | Phase 4bi-D feature-family successor-state | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant was preserved end-to-end and never invoked
across the Phase 4bj-A merge.

## Manifest state preservation

- raw manifest `research_eligible: false`;
- raw manifest `eligibility_gate_status: pending`;
- original derived manifest `research_eligible: false`;
- original derived manifest `eligibility_gate_status: pending`;
- feature manifest `research_eligible: false`;
- feature manifest `eligibility_gate_status: pending`;
- feature manifest `governance_labels.labels: forbidden`;
- feature manifest `governance_labels.ml: forbidden`;
- feature manifest `governance_labels.strategy: forbidden`;
- feature manifest `governance_labels.backtest: forbidden`;
- feature manifest `governance_labels.acquisition: unauthorized`.

No label namespace exists. No label manifest exists. No label gate
report exists. No label successor-state exists.

## Boundary confirmations

- no source code modified;
- no tests modified;
- no scripts modified;
- no configs changed;
- no README changed;
- no `pyproject.toml` changed;
- no `.gitignore` changed;
- no MCP files changed;
- no data acquisition;
- no public endpoint calls;
- no Binance API calls;
- no WebSocket;
- no credential / `.env` / `.mcp.json` / MCP / Graphify;
- no normalizer rerun;
- no raw gate rerun;
- no derived gate rerun;
- no feature kernel rerun;
- no feature-family gate rerun;
- no label code;
- no target code;
- no label namespace created;
- no label manifest created;
- no label parquet created;
- no label gate report created;
- no label successor-state created;
- no replacement feature parquet;
- no replacement feature manifest;
- no replacement gate report;
- no replacement upstream artefact;
- no labels;
- no targets;
- no signals;
- no ML;
- no strategy;
- no backtest;
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge /
  prediction / model-score / decision-score / entry-exit / strategy
  output;
- no tracked `data/microstructure/` output;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant
  preserved (never invoked);
- no retained verdict revised;
- no project lock loosened;
- no M0 amendment;
- no successor authorized.

## Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

## Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25 % / 2× / one-position / mark-price stops
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k V2 backtest-plan methodology
- Phase 4p G1 strategy-spec memo
- Phase 4q G1 backtest-plan methodology
- Phase 4v C1 strategy-spec memo
- Phase 4w C1 backtest-plan methodology
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-
  down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw / Phase 4ax / Phase 4ay / Phase 4az / Phase 4ba /
  Phase 4bb-A / Phase 4bb-B / Phase 4bb-C / Phase 4bb-D / Phase 4bb-E /
  Phase 4bc / Phase 4bd-A / Phase 4bd / Phase 4be / Phase 4bf-A /
  Phase 4bf / Phase 4bg-A / Phase 4bg-B / Phase 4bh-A / Phase 4bh-B /
  Phase 4bh / Phase 4bi-A / Phase 4bi-B / Phase 4bi-C / Phase 4bi-D
  results all preserved verbatim.

## No-rescue constraints

Phase 4al refined no-rescue rule applies verbatim, including to any
future label or target family. Specifically forbidden as future
labels / targets:

- any rescue-shaped reconstruction of R2 / F1 / D1-A / V2 / G1 / C1 /
  5m-thread rules under a different name;
- any label that directly encodes strategy entry / exit / position
  decision / model prediction / alpha score / edge score / PnL /
  realized profit / realized loss / equity curve / live order outcome
  / production execution quality / manual intervention result /
  exchange-write result / post-hoc optimized threshold result;
- any external data not already governed at the same eligibility
  level;
- any future-feature-normalization leakage;
- any centered-window construction;
- any mark-price stop-domain assumption without separate Phase 3v §8
  reconciliation.

The Phase 4ak twelve-clause M0 gate applies prospectively to any
future label, target, hypothesis, strategy, or backtest. Stage-5
admissibility is upstream of M0, not a bypass of M0.

## Successor authorization

- no Phase 4bj-B
- no Phase 4bj-C
- no Phase 4bj-D
- no Phase 4bj-E
- no Phase 4bj-F
- no Phase 4bj-G
- no Phase 4bj
- no Phase 4bb-F
- no Phase 4bb-G
- no Phase 5
- no Phase 4 canonical
- no additional acquisition
- no labels
- no targets
- no signals
- no ML implementation
- no strategy
- no backtest
- no paper / shadow
- no live-readiness
- no deployment
- no exchange-write
- no production keys
- no authenticated APIs
- no private endpoints
- no user stream
- no MCP / Graphify / `.mcp.json` / credentials

## Recommended state

- **Primary:** remain paused.
- **Conditional next (NOT authorized):** Phase 4bj-B — Label Schema
  Finalization Memo, docs-only.
- **Conditional cleanup (NOT authorized):** Phase 4bb-F — Gate Report
  Output Path Hygiene.
- **Conditional raw policy marker (NOT authorized):** Phase 4bb-G —
  Raw Manifest Successor-State Recording.

**No next phase authorized.**
