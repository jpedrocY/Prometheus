# Phase 4bj-B Merge Closeout — Label Schema Finalization Memo

Date: 2026-05-10
Phase: 4bj-B
Phase type: docs-only label-schema finalization memo
Action: merge into main
Status: COMPLETED

## Merge purpose

Bring the Phase 4bj-B docs-only label-schema finalization memo into
`main`. Phase 4bj-B selects **Outcome 1 — Label schema finalized,
implementation deferred** for the future label family
`microstructure_labels_aggtrades_v001` (BTCUSDT / 2025-01-15;
event-aligned to the existing feature parquet with `row_count =
1681098`).

The merge brings forward only docs files. No source code, tests,
scripts, configs, manifests, gate reports, successor-state
artefacts, or data artefacts are introduced. No labels, targets,
ML, strategy, backtests, acquisition, or successor phases are
authorized.

A tiny docs-only column-count clarification was applied to the
Phase 4bj-B memo on the source branch before merge: the confusing
"33 columns" / "41 columns" explanatory parenthetical in Section 10
was replaced with the clear statement that the future label parquet
must contain exactly 39 columns in canonical order, with the
enumerated column list below as authoritative. The Section 10
enumerated list, the "Total finalized columns: 39" conclusion, the
closeout, and the `current-project-state.md` summary already
recorded canonical column count = 39; the clarification is purely
cosmetic.

## Branches

- **Target branch:** `main`
- **Source branch:** `phase-4bj-b/label-schema-finalization`

## Recorded SHAs

- **Phase 4bj-A merge commit (verified ancestor of main):**
  `8a99a74930b5c8b33c63e9eceb0116e5e97b11b8`
- **Phase 4bj-B branch base / post-Phase-4bj-A closeout main SHA
  (verified at start of Phase 4bj-B and again at merge time):**
  `777edbf8460e50067cdd6301a240276eaed1ffbf`
- **Main SHA before this merge:**
  `777edbf8460e50067cdd6301a240276eaed1ffbf`
- **Phase 4bj-B source commit SHA (initial):**
  `8c0a6f2708f22bb88b5e442c08fbf006659d2827`
- **Phase 4bj-B source commit SHA (clarification, column count):**
  `f92cd8e642959aadaec5f85c7b527c9813e65b98`
- **Phase 4bj-B merge commit SHA:**
  `decc6624079ef786d5f360226303ae10a644a237`
- **Final main SHA after push:**
  `decc6624079ef786d5f360226303ae10a644a237`
- **Final origin/main SHA after push:**
  `decc6624079ef786d5f360226303ae10a644a237`

## Merge method

- `git merge --no-ff phase-4bj-b/label-schema-finalization`
- Merge strategy: `ort` (automatic; no conflicts)
- Merge commit message:
  `docs(phase-4bj-b): merge label schema finalization`

## Files brought forward by the merge (tracked)

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-b_label-schema-finalization.md`
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-b_closeout.md`
- `docs/00-meta/current-project-state.md`

## Total diff summary from the Phase 4bj-B merge

```
 docs/00-meta/current-project-state.md              |  485 +++++++++
 .../2026-05-10_phase-4bj-b_closeout.md             |  242 +++++
 ...-05-10_phase-4bj-b_label-schema-finalization.md | 1141 ++++++++++++++++++++
 3 files changed, 1868 insertions(+)
```

No code, tests, scripts, configs, README, `pyproject.toml`,
`.gitignore`, MCP files, governance source files, strategy specs,
validation checklists, phase-gates, runtime docs, manifests, gate
reports, successor-state artefacts, feature artefacts, label
artefacts, ML artefacts, strategies, or backtest artefacts were
changed.

## Tiny clarification applied (column count)

- The confusing "33 columns" / "41 columns" explanatory
  parenthetical in Section 10 of the Phase 4bj-B memo was replaced
  with the clean statement:
  "The future label parquet must contain exactly the following 39
  columns in canonical order. The enumerated column list below is
  authoritative."
- The Section 10 enumerated column list (1..39) was unchanged.
- The "Total finalized columns: 39" conclusion line was unchanged.
- The Phase 4bj-B closeout already recorded canonical finalized
  column count = 39.
- The `current-project-state.md` Phase 4bj-B narrative paragraph
  and "Current phase:" block already recorded canonical finalized
  column count = 39.
- The clarification commit SHA is
  `f92cd8e642959aadaec5f85c7b527c9813e65b98`.

## Decision result

- **Selected outcome:** Outcome 1 — Label schema finalized,
  implementation deferred.
- Label schema finalized at docs / policy level.
- Implementation deferred.
- **No labels created.**
- **No targets created.**
- **No code written.**
- **No label parquet created.**
- **No label manifest created.**
- **No label gate report created.**
- **No label successor-state created.**
- **No ML authorized.**
- **No strategy authorized.**
- **No backtest authorized.**
- **No acquisition authorized.**
- **No successor authorized.**

## Finalized label family identity

- `dataset_family` = `microstructure_labels_aggtrades_v001`
- `dataset_version` = `v001`
- `label_schema_version` = `v001`
- `symbol` = `BTCUSDT`
- `utc_date` = `2025-01-15`
- `row_count` = `1681098`

## Finalized horizons

- `horizon_list` = `["1s", "5s", "15s", "60s"]`
- `horizon_ms_list` = `[1000, 5000, 15000, 60000]`
- Deferred: `30s`, `5m`, `15m`, `30m`, `1h`, `4h`, day-end,
  multi-day.

## Finalized canonical label columns (eight)

- `forward_log_return_1s`
- `forward_log_return_5s`
- `forward_log_return_15s`
- `forward_log_return_60s`
- `forward_direction_1s`
- `forward_direction_5s`
- `forward_direction_15s`
- `forward_direction_60s`

## Finalized canonical column count

- **39 total columns.**
- The enumerated column list in the Phase 4bj-B memo (Section 10)
  is **authoritative**.
- The tiny clarification commit (`f92cd8e6...`) replaced the
  confusing "33 columns" / "41 columns" explanatory parenthetical
  with the clear "39 columns" statement.

## Finalized row model

- One label row per feature row.
- Same `row_count` as feature parquet (`1681098`).
- Same `row_index` `0..1681097` as feature parquet.
- No row dropping.
- No resampling.
- No synthetic timestamps.
- No upsampling.
- No downsampling.
- No cross-day stitching.
- Right-edge horizon values are **nullable / censored**, not
  removed.

## Finalized reference policy

- `target_timestamp_ms` = `feature_timestamp_ms` + horizon ms.
- Reference row = latest normalized aggTrades row with
  `transact_time_ms <= target_timestamp_ms`.
- Same-timestamp tie-break = largest `row_index`.
- Price domain = normalized aggTrades **trade price only**.
- **No mark price.**
- **No index price.**
- **No book / bid / ask / midpoint.**
- **No external data.**
- **No first trade after target timestamp.**
- **No future feature values.**
- **No cross-midnight stitching.**

## Finalized formulas

- `forward_log_return_H` = `ln(reference_trade_price_H /
  anchor_trade_price)`.
- `forward_direction_H` = `+1` if `forward_log_return_H > 0`;
  `0` if `forward_log_return_H == 0`;
  `-1` if `forward_log_return_H < 0`;
  `null` if `forward_log_return_H` is null.
- **Strict sign threshold at `0.0`.**
- No deadband.
- No bp threshold.
- No threshold optimization.
- No cost-based threshold at label-schema level.

## Finalized support / QA columns

- `reference_row_index_H` (one per horizon).
- `reference_timestamp_ms_H` (one per horizon).
- `horizon_censored_flag_H` (one per horizon).
- `label_invalid_price_flag` (global).
- `label_any_censored_flag` (global).

## Finalized dtype policy

- `int64` for ids and timestamps (including UTC ms timestamps and
  reference timestamps).
- Lineage strings / hashes / dataset IDs / versions / symbol /
  utc_date as `string`.
- `forward_log_return_*` as nullable `float64`.
- `forward_direction_*` as nullable `int8` in `{-1, 0, 1}`.
- `reference_row_index_*` as nullable `int64`.
- `reference_timestamp_ms_*` as nullable `int64`.
- `horizon_censored_flag_*` as non-nullable `bool`.
- `label_invalid_price_flag` as non-nullable `bool`.
- `label_any_censored_flag` as non-nullable `bool`.
- `label_config_hash` as `string`.
- **No NaN / inf** in any column.
- Nulls allowed only under defined censoring / invalid-price
  conditions.

## Finalized future label manifest defaults

- `research_eligible` = `false`.
- `eligibility_gate_status` = `pending`.
- `chronological_split_policy` = `not_yet_defined`.
- `governance_labels.labels` = `allowed_by_future_phase_only`.
- `governance_labels.targets` = `allowed_by_future_phase_only`.
- `governance_labels.ml` = `forbidden`.
- `governance_labels.strategy` = `forbidden`.
- `governance_labels.backtest` = `forbidden`.
- `governance_labels.acquisition` = `unauthorized`.
- `governance_labels.paper_shadow_live` = `forbidden`.
- `governance_labels.deployment` = `forbidden`.
- `governance_labels.exchange_write` = `forbidden`.

## Finalized future output paths (not created)

- `data/microstructure/labels/microstructure_labels_aggtrades_v001/`
  `BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet`
- `data/microstructure/manifests/`
  `microstructure_labels_aggtrades_v001__v001.json`
- `data/microstructure/gate-reports/labels/`
- `data/microstructure/successor-state/` (sibling label successor-
  state files only; feature successor-state files must not be
  modified)

None of the above paths were created by Phase 4bj-B. The entire
`data/microstructure/` tree remains gitignored under
`.gitignore:85`.

## Validation results (recorded at merge time)

- `ruff check .` (whole repo): **All checks passed!**
- `pytest tests/research/microstructure/`: **666 passed**
- `pytest` (whole repo): **1449 passed, 2 failed** — the two
  failures are the same pre-existing simulation failures that have
  been on `main` since before Phase 4bj-B:
  - `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
  - `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_ethusdt`
  - both `KeyError: 'trade_count'` in
    `src/prometheus/research/data/storage.py:232`
  - **zero new regressions from Phase 4bj-B.**
- `mypy src/prometheus` strict: **Success: no issues found in 110
  source files.**
- `git diff --check`: clean.
- `git check-ignore -v data/microstructure/`: covered by
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/`:
  covered by `.gitignore:85`.
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
across the Phase 4bj-B merge.

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
- no PnL / MFE / MAE / R-multiple / equity / position / alpha /
  edge / prediction / model-score / decision-score / entry-exit /
  strategy output;
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
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k V2 backtest-plan methodology
- Phase 4p G1 strategy-spec memo
- Phase 4q G1 backtest-plan methodology
- Phase 4v C1 strategy-spec memo
- Phase 4w C1 backtest-plan methodology
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw / Phase 4ax / Phase 4ay / Phase 4az / Phase 4ba /
  Phase 4bb-A / Phase 4bb-B / Phase 4bb-C / Phase 4bb-D /
  Phase 4bb-E / Phase 4bc / Phase 4bd-A / Phase 4bd / Phase 4be /
  Phase 4bf-A / Phase 4bf / Phase 4bg-A / Phase 4bg-B /
  Phase 4bh-A / Phase 4bh-B / Phase 4bh / Phase 4bi-A /
  Phase 4bi-B / Phase 4bi-C / Phase 4bi-D / Phase 4bj-A results
  all preserved verbatim.

## No-rescue constraints

Phase 4al refined no-rescue rule applies verbatim, including to any
future label or target family. Specifically forbidden as future
labels / targets:

- any rescue-shaped reconstruction of R2 / F1 / D1-A / V2 / G1 /
  C1 / 5m-thread rules under a different name;
- any label that directly encodes strategy entry / exit / position
  decision / model prediction / alpha score / edge score / PnL /
  realized profit / realized loss / equity curve / live order
  outcome / production execution quality / manual intervention
  result / exchange-write result / post-hoc optimized threshold
  result;
- any external data not already governed at the same eligibility
  level;
- any future-feature-normalization leakage;
- any centered-window construction;
- any mark-price stop-domain assumption without separate Phase 3v
  §8 reconciliation.

The Phase 4ak twelve-clause M0 gate applies prospectively to any
future label, target, hypothesis, strategy, or backtest. Stage-5
admissibility is upstream of M0, not a bypass of M0.

## Successor authorization

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
- **Conditional next (NOT authorized):** Phase 4bj-C — Label
  Implementation + Local Label Artefact Generation (code + docs +
  local gitignored output), separately authorized.
- **Conditional cleanup (NOT authorized):** Phase 4bb-F — Gate
  Report Output Path Hygiene.
- **Conditional raw policy marker (NOT authorized):** Phase 4bb-G —
  Raw Manifest Successor-State Recording.

**No next phase authorized.**
