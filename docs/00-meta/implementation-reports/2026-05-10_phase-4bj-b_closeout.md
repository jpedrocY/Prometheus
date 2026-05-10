# Phase 4bj-B Closeout — Label Schema Finalization Memo

Date: 2026-05-10
Phase: 4bj-B
Phase type: docs-only label-schema finalization memo
Branch: phase-4bj-b/label-schema-finalization
Base: main at the post-Phase-4bj-A merge-closeout state
  (`777edbf8460e50067cdd6301a240276eaed1ffbf`)
Phase 4bj-A merge commit (verified ancestor of main):
  `8a99a74930b5c8b33c63e9eceb0116e5e97b11b8`
Status: drafted (docs-only; text-only)

## Outcome

**Selected outcome:** Outcome 1 — Label schema finalized,
implementation deferred.

Phase 4bj-B locks the exact v001 label schema for the future label
family `microstructure_labels_aggtrades_v001` at policy level only.
No labels were created. No targets were created. No code was written.
No label artefact was created. No label manifest was created. No
label gate report was created. No label successor-state was created.
No ML / strategy / backtest / acquisition / successor was authorized.

## Files added (tracked)

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-b_label-schema-finalization.md`
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-b_closeout.md`

## Files modified narrowly (tracked)

- `docs/00-meta/current-project-state.md`
  - added a Phase 4bj-B narrative paragraph;
  - replaced the "Current phase:" block with a Phase 4bj-B summary;
  - preserved the prior Phase 4bj-A "Current phase:" block as
    historical context.

## Untouched

- all source code under `src/prometheus/`;
- all tests;
- all scripts;
- `.gitignore`;
- `pyproject.toml`;
- `README.md`;
- all prior governance memos;
- all prior `data/microstructure/` artefacts (raw, derived, feature,
  gate-reports, successor-state).

## Locked v001 schema summary

- **Label family:** `microstructure_labels_aggtrades_v001`
- **Dataset version:** `v001`
- **Label schema version:** `v001`
- **Symbol / date:** `BTCUSDT` / `2025-01-15`
- **Row count:** `1681098` (event-aligned to feature parquet)
- **Horizons:** `["1s", "5s", "15s", "60s"]` with `[1000, 5000,
  15000, 60000]` ms
- **Labels (eight):**
  - `forward_log_return_1s`, `forward_log_return_5s`,
    `forward_log_return_15s`, `forward_log_return_60s`
  - `forward_direction_1s`, `forward_direction_5s`,
    `forward_direction_15s`, `forward_direction_60s`
- **Support columns (14):** 4 × (`reference_row_index_H`,
  `reference_timestamp_ms_H`, `horizon_censored_flag_H`) +
  `label_invalid_price_flag` + `label_any_censored_flag`
- **Lineage / identity / metadata (16):** dataset family, dataset
  version, label schema version, source feature family / version /
  manifest SHA / parquet SHA / successor-state SHA / Phase 4bi-B
  gate report SHA, optional source normalized parquet SHA, symbol,
  utc_date, row_index, agg_trade_id, feature_timestamp_ms,
  source_transact_time_ms
- **Hash column (1):** `label_config_hash`
- **Anchor price domain:** trade price from normalized aggTrades
  source row (no mark price, no book, no index)
- **Future-reference policy:** latest normalized aggTrades row with
  `transact_time_ms <= T + H_ms`; same-timestamp tie-break by
  largest `row_index`; cross-midnight forbidden
- **Formula:** `forward_log_return_H = ln(reference_trade_price_H /
  anchor_trade_price)` (natural log; Decimal arithmetic into
  ratio; float64 cast at the log step)
- **Direction policy:** strict-sign threshold at `0.0` log-return;
  no deadband; no bp threshold; no optimization
- **Null / censoring:** keep all feature rows; per-horizon
  independent right-edge censoring; no forward-fill; no
  cross-midnight stitching
- **Dtype policy:** int64 for ids and timestamps; nullable float64
  for log returns; nullable int8 in `{-1, 0, 1}` for direction;
  bool for flags; no NaN / inf
- **Chronological split policy:** `not_yet_defined`
- **Governance labels:** labels = `allowed_by_future_phase_only`;
  targets = `allowed_by_future_phase_only`; ml = `forbidden`;
  strategy = `forbidden`; backtest = `forbidden`; acquisition =
  `unauthorized`; paper_shadow_live / deployment / exchange_write =
  `forbidden`
- **Manifest defaults:** `research_eligible = false`;
  `eligibility_gate_status = pending`

## Pre / post artefact SHA256 verification

All 11 upstream artefacts inspected pre-phase remain byte-identical
after Phase 4bj-B (Phase 4bj-B read them only):

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
always-raises invariant was preserved end-to-end and never invoked.

## Manifest state preservation

- raw manifest: `research_eligible: false /
  eligibility_gate_status: pending` (unchanged)
- original derived manifest: `research_eligible: false /
  eligibility_gate_status: pending` (unchanged)
- feature manifest: `research_eligible: false /
  eligibility_gate_status: pending` (unchanged)
- feature manifest governance labels (unchanged):
  - `acquisition: unauthorized`
  - `backtest: forbidden`
  - `labels: forbidden`
  - `ml: forbidden`
  - `strategy: forbidden`
  - `feature_computation: allowed_by_phase_4bh`
  - `stop_trigger_domain: trade_price_backtest_candidate`
  - `phase_id: 4bh`

No label namespace exists. No label manifest exists. No label gate
report exists. No label successor-state exists.

## Critical interpretation

Phase 4bj-B locks the v001 schema **at docs / policy level only**. It
neither implements the schema, nor flips any `research_eligible`
flag, nor transitions any `eligibility_gate_status`, nor extends the
Phase 4bi-D Stage-5 admissibility marker beyond its sibling-artefact
scope.

Any future Phase 4bj-C implementation must obey the schema verbatim;
schema drift at implementation time is forbidden. The future label
artefact, if ever produced, will continue to carry
`research_eligible: false / eligibility_gate_status: pending` until
a separately authorized successor phase changes that under M0 and
no-rescue.

## Validation

- `git status`: clean before docs commit (only `.claude/scheduled_tasks.lock`
  and `data/research/` untracked, both pre-existing).
- `ruff check .` (whole repo): PASS (recorded at validation time).
- `pytest tests/research/microstructure/`: PASS (recorded at
  validation time).
- `pytest` (whole repo): PASS except the two known pre-existing
  simulation failures in
  `tests/simulation/test_backtest_real_2026_03.py` (`KeyError:
  'trade_count'` in `src/prometheus/research/data/storage.py:232`);
  zero new regressions introduced by Phase 4bj-B.
- `mypy` strict: PASS (recorded at validation time).
- `git diff --check`: PASS (no whitespace or merge conflict markers).
- `git check-ignore -v data/microstructure/`: covered by
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/`:
  covered.
- `git check-ignore -v data/microstructure/features/`: covered.
- `git check-ignore -v data/microstructure/manifests/`: covered.
- `git check-ignore -v data/microstructure/gate-reports/features/`:
  covered.

## What Phase 4bj-B did NOT do

Phase 4bj-B did NOT:

- modify source code;
- modify tests;
- modify scripts;
- modify any sidecar;
- modify the feature parquet;
- modify the feature manifest;
- modify the Phase 4bi-B gate report;
- modify the Phase 4bi-D successor-state artefact;
- modify the Phase 4bg-B successor-state artefact;
- modify the Phase 4bf gate report;
- modify the Phase 4bb-D gate report;
- modify the original derived manifest;
- modify the raw manifest;
- modify the raw zip;
- rerun the normalizer, raw eligibility gate, derived-family gate,
  feature kernel, or feature-family eligibility gate;
- generate any new gate report (raw, derived, feature, label, or
  other);
- create labels;
- create targets;
- create signals;
- create ML artefacts;
- train ML;
- create strategy logic;
- run backtests or simulations;
- compute PnL, MFE, MAE, R-multiple, equity, position state, alpha,
  edge, prediction, model score, decision score, entry / exit, or
  strategy output;
- acquire data;
- call any Binance, public, or private endpoint;
- open any WebSocket;
- use any credential;
- read or create `.env`;
- create or read `.mcp.json`;
- enable MCP or Graphify;
- flip `research_eligible` on any actual manifest;
- transition `eligibility_gate_status` on any actual manifest;
- revise any retained verdict;
- change any project lock;
- amend M0 governance;
- authorize Phase 4bj-C, Phase 4bj-D, Phase 4bj-E, Phase 4bj-F,
  Phase 4bj-G, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical,
  paper / shadow / live-readiness, deployment, exchange-write,
  production keys, authenticated APIs, private endpoints, user
  stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

## Recommendation

- **Primary:** remain paused.
- **Conditional next (NOT authorized):** Phase 4bj-C — Label
  Implementation + Local Label Artefact Generation (code + docs +
  local gitignored output), separately authorized.
- **Conditional cleanup (NOT authorized):** Phase 4bb-F — Gate
  Report Output Path Hygiene.
- **Conditional raw policy marker (NOT authorized):** Phase 4bb-G —
  Raw Manifest Successor-State Recording.

**No next phase authorized.**
