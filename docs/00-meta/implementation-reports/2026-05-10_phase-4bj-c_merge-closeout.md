# Phase 4bj-C — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bj-C — Label Implementation + Local Label Artefact
  Generation
- **Type:** code + docs + local gitignored label artefact generation
- **Action:** merge into `main`
- **Merge purpose:** bring the Phase 4bj-C label implementation
  (5 source modules + narrow `__init__.py` re-export update + 7 test
  files + 73 new tests + Phase 4bj-C main memo and closeout + the
  narrow `current-project-state.md` Phase 4bj-C update) into `main` so
  the project record reflects the materialised Phase 4bj-B v001 label
  schema as runnable code, with the validated local-only Stage-0
  label artefacts for BTCUSDT 2025-01-15 produced under the gitignored
  `data/microstructure/` namespace.
- **Target branch:** `main`
- **Source branch:** `phase-4bj-c/label-implementation-local-artefacts`

## 2. SHAs

- **`main` SHA before merge:** `f73a3db591bb0aa376b21ce0294f24de4acdfee4`
- **Phase 4bj-C source commit SHA:**
  `f797ca1b88d2de13ce54b3a78f8b57aba30db30c`
- **Phase 4bj-C merge commit SHA:**
  `deb90bf2346c3b133e2e6ec079f0670694654870`
- **Final `main` / `origin/main` SHA after push:**
  `deb90bf2346c3b133e2e6ec079f0670694654870`
- **Code commit SHA recorded inside label manifest:**
  `f73a3db591bb0aa376b21ce0294f24de4acdfee4`

## 3. Merge method

- `git merge --no-ff` with `ort` strategy
- Merge commit message: `feat(phase-4bj-c): merge local label artefact generation`
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Source modules (5 added, 1 narrowly updated):

- `src/prometheus/research/microstructure/labels_schema.py`
- `src/prometheus/research/microstructure/labels_io.py`
- `src/prometheus/research/microstructure/labels_compute.py`
- `src/prometheus/research/microstructure/labels_manifest.py`
- `src/prometheus/research/microstructure/labels_validation.py`
- `src/prometheus/research/microstructure/__init__.py` (Phase 4bj-C
  re-exports + extended package docstring; no prior export removed)

Tests (7 added):

- `tests/research/microstructure/_labels_fixtures.py`
- `tests/research/microstructure/test_labels_schema.py` (14 tests)
- `tests/research/microstructure/test_labels_io.py` (13 tests)
- `tests/research/microstructure/test_labels_compute.py` (12 tests)
- `tests/research/microstructure/test_labels_manifest.py` (14 tests)
- `tests/research/microstructure/test_labels_validation.py` (8 tests)
- `tests/research/microstructure/test_labels_no_network.py` (12 parametrised tests)

Docs (2 added, 1 narrowly updated):

- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-c_label-implementation-local-artefacts.md`
- `docs/00-meta/implementation-reports/2026-05-10_phase-4bj-c_closeout.md`
- `docs/00-meta/current-project-state.md` (Phase 4bj-C narrative
  paragraph + Current phase block; prior Phase 4bj-B block demoted to
  historical context)

Total diff summary from the Phase 4bj-C merge:

```text
16 files changed, 5231 insertions(+), 0 deletions
```

`.gitignore`, `pyproject.toml`, `README.md`, all prior source modules
outside `__init__.py`, all prior tests, all scripts, all prior
governance memos, and all prior `data/microstructure/` artefacts were
not modified by the merge.

## 5. Implementation result

- **5 new source modules** under
  `src/prometheus/research/microstructure/`:
  - `labels_schema.py` — 39-column canonical schema + 8 label names
    + 14 support column names + 17 lineage column names + horizon
    constants + `FORBIDDEN_LABEL_COLUMN_SUBSTRINGS` + 5 policy
    descriptor strings + `build_label_config_hash` (deterministic
    SHA256 over canonical-JSON of locked schema fields + 4 upstream
    lineage SHAs) + `LabelSchemaError`.
  - `labels_io.py` — path discipline helpers
    (`assert_label_path_under_data_microstructure`,
    `assert_output_path_under_labels`,
    `assert_label_manifest_path_under_manifests`,
    `derive_label_output_path`,
    `derive_label_manifest_output_path`) + atomic writers
    (`atomic_write_label_parquet`, `atomic_write_label_manifest`,
    `write_label_sha256_sidecar`) + `LabelIOError`.
  - `labels_compute.py` — `LabelLineage`, `LabelComputationSummary`,
    `LabelComputationError`, `compute_aggtrade_labels_v001`,
    `write_label_dataset_v001`.
  - `labels_manifest.py` — `REQUIRED_LABEL_GOVERNANCE_KEYS`,
    `FORBIDDEN_LABEL_GOVERNANCE_VALUES`,
    `REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS`,
    `build_label_manifest_v001`, `LabelManifestError`.
  - `labels_validation.py` — `LabelCheckStatus`, `LabelCheckResult`,
    `LabelValidationResult`, `LabelValidationError`,
    `validate_label_dataset_v001`, `iter_failures`,
    `to_summary_dict`.
- **Narrow `__init__.py` re-export update** exposing the Phase 4bj-C
  public API and extending the package docstring with a Phase 4bj-C
  section. No prior export was removed.
- **7 new test files** under `tests/research/microstructure/`:
  shared `_labels_fixtures.py` mini-fixture builder, `test_labels_*`
  (5 unit modules + 1 static no-network scan), totalling
  **73 new tests; all pass** at the targeted level.
- **label schema constants implemented** exactly per Phase 4bj-B:
  `LABEL_SCHEMA_V001` is a 39-column tuple in canonical order
  (17 lineage + 8 labels + 14 support); `LABEL_NAMES_V001`,
  `LABEL_SUPPORT_COLUMN_NAMES_V001`, `LABEL_LINEAGE_COLUMNS_V001`,
  `LABEL_HORIZONS_V001`, `LABEL_HORIZON_MS_V001` all locked.
- **`label_config_hash` implemented** as SHA256 over canonical-JSON
  (sorted keys, ASCII, no whitespace) of dataset / version / schema
  identity, label / support / horizon / horizon-ms lists, five
  policy descriptors (anchor / future-reference /
  direction-threshold / null-censoring / dtype), and the four
  upstream lineage SHAs (feature manifest, feature parquet,
  Phase 4bi-D successor-state, Phase 4bi-B gate report).
- **label computation kernel implemented** with:
  - per-row alignment validation versus the feature parquet
    (`row_index`, `agg_trade_id`, `feature_timestamp_ms`,
    `feature_timestamp_ms == source_transact_time_ms`),
  - normalized parquet sort invariant verification,
  - per-horizon `searchsorted(side="right")`-based reference index,
  - right-edge censoring when
    `target_timestamp_ms > final_source_T`,
  - same-timestamp tie-break to the largest `row_index` (implicit
    from Phase 4bd `row_index == np.arange(n)` invariant),
  - Decimal parsing of anchor and reference prices,
  - Decimal ratio with `float64` cast only at the `math.log()` step,
  - strict-sign direction derivation (`+1` / `0` / `-1` / `null`),
  - defensive invalid-price branch counted in
    `invalid_price_row_count` and flagged via
    `label_invalid_price_flag`,
  - `label_any_censored_flag = OR(horizon_censored_flag_*)`,
  - no NaN / inf in any output column.
- **label manifest builder implemented** with locked 10-key
  governance label block, 13-key all-true boundary confirmation
  block, schema descriptors, policy descriptors, locked
  `chronological_split_policy = "not_yet_defined"`,
  `research_eligible = false` and `eligibility_gate_status =
  "pending"` defaults preserved.
- **atomic writers + refuse-overwrite implemented** for label
  parquet, label parquet sidecar, label manifest, and label
  manifest sidecar, each constrained to its specific gitignored
  subdirectory under `data/microstructure/`.
- **label validator implemented** running 100 checks at the full
  row scale (sidecar SHA parity, manifest content, schema order,
  forbidden-substring scan, row-count parity vs feature parquet
  and label manifest, per-row alignment, lineage constancy, per-
  horizon label finiteness + direction-domain + sign-match,
  support-column censoring + reference-index + reference-timestamp,
  OR-invariant for `label_any_censored_flag`, strict bool for
  boolean flags, observed vs declared censored / invalid counts,
  lineage null-count, and upstream-immutability SHA matches).
- **no-network / no-credential static scan implemented** over all
  five new label source modules (extends the Phase 4aw / Phase 4ax
  / Phase 4bb-C / Phase 4bd / Phase 4bf / Phase 4bh pattern).
- **no scripts added.**
- **no new dependencies** beyond the existing environment (the new
  modules import only `dataclasses`, `decimal`, `enum`, `hashlib`,
  `json`, `math`, `os`, `pathlib`, `re`, `tempfile`, `typing`,
  plus `pyarrow`, `numpy`, and the existing
  `prometheus.research.microstructure.normalize_io` helpers).

## 6. Local gitignored label outputs

| Output | Path | SHA256 | Size (bytes) |
|---|---|---|---|
| Label parquet | `data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet` | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | 66,073,234 |
| Label parquet sidecar | same path with `.sha256` | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | 154 |
| Label manifest | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json` | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | 6,786 |
| Label manifest sidecar | same path with `.sha256` | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | 138 |

- **Label parquet row count:** 1,681,098
- **Label parquet column count:** 39
- **Sidecar parity:** label parquet sidecar matches recomputed
  parquet bytes; label manifest sidecar matches recomputed manifest
  bytes (verified again post-merge).
- **All four files gitignored** under `.gitignore:85: data/microstructure/`
  and **NOT** committed to the repository.

## 7. Label dataset summary

- `dataset_family = microstructure_labels_aggtrades_v001`
- `dataset_version = v001`
- `label_schema_version = v001`
- `symbol = BTCUSDT`
- `utc_date = 2025-01-15`
- `row_count = 1,681,098`
- `column_count = 39`
- `label_config_hash = fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`
- `invalid_price_row_count = 0`
- `censored_per_horizon = {"1s": 9, "5s": 42, "15s": 118, "60s": 507}`
- `chronological_split_policy = "not_yet_defined"`
- `research_eligible = false`
- `eligibility_gate_status = "pending"`

## 8. Label generation sample summary

| Row | row_index | agg_trade_id | feature_ts_ms | forward_log_return_1s | forward_direction_60s | horizon_censored_flag_1s | horizon_censored_flag_60s |
|---|---|---|---|---|---|---|---|
| first | 0 | 2,516,301,323 | 1,736,899,205,109 | 0.0001502245860383073 | 1 | false | false |
| last | 1,681,097 | 2,517,982,420 | 1,736,985,599,991 | null (right-edge censoring) | n/a | true | true |

## 9. Validation results

- `validate_label_dataset_v001`: `overall_status=pass`, **100 / 100 PASS**
- targeted Phase 4bj-C label tests
  (`test_labels_schema.py` + `test_labels_io.py` +
  `test_labels_compute.py` + `test_labels_manifest.py` +
  `test_labels_validation.py` + `test_labels_no_network.py`):
  **73 / 73 PASS**
- `pytest tests/research/microstructure/`: **744 passed**
- `ruff check src/prometheus/research/microstructure
  tests/research/microstructure`: All checks passed
- `ruff check .` (whole repo): All checks passed
- `mypy src/prometheus/research/microstructure`: Success on 33 source
  files (with the harmless pre-existing
  `pyproject.toml: note: unused section(s): module = ['duckdb',
  'duckdb.*']` advisory)
- `mypy` (whole repo, strict): Success on 115 source files
- `pytest` (whole repo): 1527 passed, 2 failed — only the pre-existing
  simulation `KeyError: 'trade_count'` failures in
  `tests/simulation/test_backtest_real_2026_03.py`
  (`test_real_2026_03_btcusdt` and `test_real_2026_03_ethusdt`);
  **zero new regressions from Phase 4bj-C**.
- `git diff --check`: clean
- `git check-ignore -v data/microstructure/`: `.gitignore:85`
- `git check-ignore -v data/microstructure/labels/`: `.gitignore:85`
- `git check-ignore -v data/microstructure/manifests/`: `.gitignore:85`
- `git check-ignore -v data/microstructure/successor-state/`:
  `.gitignore:85`
- `git check-ignore -v data/microstructure/gate-reports/features/`:
  `.gitignore:85`
- `git check-ignore -v data/microstructure/gate-reports/labels/`:
  `.gitignore:85`

## 10. Upstream immutability evidence

| Artefact | Recorded SHA256 | Status |
|---|---|---|
| Feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` | unchanged |
| Feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` | unchanged |
| Normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` | unchanged |
| Original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` | unchanged |
| Raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | unchanged |
| Raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | unchanged |
| Phase 4bb-D raw gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | unchanged |
| Phase 4bf derived gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` | unchanged |
| Phase 4bg-B successor-state | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` | unchanged |
| Phase 4bi-B feature-family gate report | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` | unchanged |
| Phase 4bi-D feature-family successor-state | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` | unchanged |

All 11 upstream artefacts remain byte-for-byte identical to the SHAs
recorded at the start of Phase 4bj-C.

## 11. Manifest state preservation

- raw manifest `research_eligible = false`
- raw manifest `eligibility_gate_status = "pending"`
- original derived manifest `research_eligible = false`
- original derived manifest `eligibility_gate_status = "pending"`
- feature manifest `research_eligible = false`
- feature manifest `eligibility_gate_status = "pending"`
- label manifest `research_eligible = false`
- label manifest `eligibility_gate_status = "pending"`
- label manifest `governance_labels.labels = "allowed_by_phase_4bj_c"`
- label manifest `governance_labels.targets = "allowed_by_phase_4bj_c"`
- label manifest `governance_labels.ml = "forbidden"`
- label manifest `governance_labels.strategy = "forbidden"`
- label manifest `governance_labels.backtest = "forbidden"`
- label manifest `governance_labels.acquisition = "unauthorized"`
- label manifest `governance_labels.paper_shadow_live = "forbidden"`
- label manifest `governance_labels.deployment = "forbidden"`
- label manifest `governance_labels.exchange_write = "forbidden"`

## 12. Boundary confirmations

- no scripts added
- no configs changed
- no `README.md` changed
- no `pyproject.toml` changed
- no `.gitignore` changed
- no MCP files changed
- no data acquisition
- no public endpoint calls
- no Binance API calls
- no WebSocket
- no credential / `.env` / `.mcp.json` / MCP / Graphify
- no normalizer rerun
- no raw eligibility gate rerun
- no derived-family gate rerun
- no feature kernel rerun
- no feature-family gate rerun
- no label-family gate created
- no label gate report file created
- no label successor-state artefact created
- no replacement feature parquet
- no replacement feature manifest
- no replacement normalized parquet
- no replacement upstream artefact
- no replacement Phase 4bi-B gate report
- no replacement Phase 4bi-D successor-state
- no ML
- no strategy
- no backtest
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge
  / prediction / model-score / decision-score / entry-exit / strategy
  output
- no tracked `data/microstructure/` output
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

## 13. Retained verdict ledger

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 14. Preserved project locks

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
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule
  + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D /
  4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B /
  4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B
  results all preserved verbatim

## 15. No-rescue constraints

The Phase 4bj-C merge does not, and cannot, be construed as
authorising:

- ML model training, model selection, strategy hypothesis generation,
  or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state, entry
  / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved).

## 16. Successor authorization

**None.**

The Phase 4bj-C merge closes the local label artefact generation
phase. Specifically not authorised by this merge:

- Phase 4bj-D — Label Artefact Structural QA Memo
- Phase 4bj-E — Label-Family Eligibility Gate
- Phase 4bj-F — Label-Family Research / ML-Use Decision
- Phase 4bj-G — Label-Family Successor-State Recording
- Phase 4bj (catch-all)
- Phase 4bb-F — Gate Report Output Path Hygiene
- Phase 4bb-G — Raw Manifest Successor-State Recording
- Phase 5
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book data
  acquisition
- ML implementation
- strategy implementation
- backtest implementation
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- user stream
- MCP / Graphify / `.mcp.json` / credentials

## 17. Recommended state

**Remain paused.**

Conditional next, if separately authorised by the operator in a future
phase: **Phase 4bj-D — Label Artefact Structural QA Memo**
(analysis-and-docs read-only) is the cleanest non-paused option. It
would inspect the locally generated Phase 4bj-C label artefacts
read-only against the Phase 4bj-B schema contract without producing a
label-family eligibility gate or label successor-state artefact, and
without transitioning any manifest state.

Phase 4bj-D is **not** authorised by this merge.
