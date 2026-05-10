# Phase 4bj-A Closeout — Label Boundary / Target Definition Memo

Date: 2026-05-10
Phase: 4bj-A
Phase type: docs-only label-boundary / target-definition memo
Branch: phase-4bj-a/label-boundary-target-definition
Base: main at the post-Phase-4bi-D merge-closeout state
Status: drafted (docs-only; text-only)

## Outcome

**Selected outcome:** Outcome 1 — Label boundary admissible in
principle, implementation deferred.

Phase 4bj-A defines, at policy level only, the future label / target
boundary for the Stage-5-admissible feature family
`microstructure_features_aggtrades_v001`. No labels were created. No
targets were created. No label namespace was created. No label
manifest was created. No label gate report was created. No label
successor-state was created. No code, tests, scripts, data, manifests,
or sidecars were modified outside the two new docs files and the
narrow `current-project-state.md` update.

## Files added (tracked)

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-a_label-boundary-target-definition.md`
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-a_closeout.md`

## Files modified narrowly (tracked)

- `docs/00-meta/current-project-state.md`
  - added a Phase 4bj-A narrative paragraph;
  - replaced the "Current phase:" block with a Phase 4bj-A summary;
  - preserved the prior Phase 4bi-D "Current phase:" block as historical
    context.

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

## Pre / post artefact SHA256 verification

All ten upstream artefacts inspected pre-phase remained byte-identical
after Phase 4bj-A (Phase 4bj-A read them only):

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
| — | Phase 4bi-D feature-family successor-state | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |

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

The Phase 4bi-D successor-state artefact's
`successor_research_ml_admissible: true` field applies to the sibling
successor-state artefact only and does **not** flip
`research_eligible` on any actual manifest. The feature manifest, the
derived manifest, and the raw manifest all continue to carry
`research_eligible: false / eligibility_gate_status: pending`. Stage-5
admissibility is **upstream of M0**, not a bypass of M0.

Phase 4bj-A consumes this Stage-5 admissibility marker only to define,
at policy level, what labels and targets may eventually mean. It does
not extend admissibility, does not authorize ML / strategy / backtest
/ acquisition, and does not propose Stage-6 (research-eligible) for
the feature family.

## Validation

- `git status`: clean before docs commit;
- `ruff check .` (whole repo): PASS (recorded at validation time);
- `pytest tests/research/microstructure/`: PASS (recorded at validation
  time);
- `pytest` (whole repo): PASS except the two known pre-existing
  simulation failures in
  `tests/simulation/test_backtest_real_2026_03.py` (`KeyError:
  'trade_count'` in `src/prometheus/research/data/storage.py:232`); zero
  new regressions introduced by Phase 4bj-A;
- `mypy` strict: PASS (recorded at validation time);
- `git diff --check`: PASS (no whitespace or merge conflict markers);
- `git check-ignore -v data/microstructure/`: covered by
  `.gitignore:85: data/microstructure/`;
- `git check-ignore -v data/microstructure/successor-state/`: covered;
- `git check-ignore -v data/microstructure/features/`: covered;
- `git check-ignore -v data/microstructure/manifests/`: covered;
- `git check-ignore -v data/microstructure/gate-reports/features/`:
  covered.

## What Phase 4bj-A did NOT do

Phase 4bj-A did NOT:

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
  edge, prediction, model score, decision score, entry/exit, or
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
- authorize Phase 4bj-B, Phase 4bj-C, Phase 4bj-D, Phase 4bj-E,
  Phase 4bj-F, Phase 4bj-G, Phase 4bb-F, Phase 4bb-G, Phase 5,
  Phase 4 canonical, paper / shadow / live-readiness, deployment,
  exchange-write, production keys, authenticated APIs, private
  endpoints, user stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

## Recommendation

- **Primary:** remain paused.
- **Conditional next (NOT authorized):** Phase 4bj-B — Label Schema
  Finalization Memo, docs-only.
- **Conditional cleanup (NOT authorized):** Phase 4bb-F — Gate Report
  Output Path Hygiene.
- **Conditional raw policy marker (NOT authorized):** Phase 4bb-G —
  Raw Manifest Successor-State Recording.

**No next phase authorized.**
