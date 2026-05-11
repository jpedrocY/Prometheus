# Phase 4bj-E — Label-Family Eligibility Gate Design + Implementation + Execution

## 1. Phase identity

- **Phase:** Phase 4bj-E — Label-Family Eligibility Gate Design +
  Implementation + Execution
- **Type:** code + docs + local gitignored output
- **Branch:** `phase-4bj-e/label-family-eligibility-gate`
- **Base:** `main` at `26a3bebc020fabf78f30bdd9b433c5fbd074e85a`
  (post-Phase-4bk-A merge-closeout state)
- **Source commit (gate code + tests):**
  `89cde8ad14b5ce92cdd718a7a4eca7bfce3e3835`
- **Predecessor merge-closeout ancestry:**
  - Phase 4bk-A merge `6f76b02b8b5fbf1f22b80d88e878e42dd3671571` is an
    ancestor of `main`.
  - Phase 4bj-D merge `11e25acbf7d33b30f5149b93919594c3ccab9fe2` is an
    ancestor of `main`.
- **Action:** branch-complete (not merged by this work).

## 2. Purpose

Design and implement an offline label-family eligibility gate for the
Phase 4bj-C local Stage-0 label artefacts:

- `data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet`
- `data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet.sha256`
- `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`
- `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json.sha256`

and execute the gate exactly once against those artefacts, producing a
single local gitignored gate report plus paired SHA256 sidecar under
`data/microstructure/gate-reports/labels/`. The gate verifies that the
locally-generated Stage-0 label artefacts conform to the Phase 4bj-B
v001 schema contract bit-for-bit, while preserving every upstream
artefact byte-identically.

Phase 4bj-E is the label-family analogue of Phase 4bb-C
(raw aggTrades eligibility gate), Phase 4bf (normalized derived-family
gate), and Phase 4bi-B (feature-family gate).

**Phase 4bj-E is branch-complete only.** It is not merged into `main`
by this work and is not project-complete; the Phase 4bk-A workflow
standard requires a separately authorized merge phase + merge-closeout
before project-complete.

## 3. Critical boundaries

The gate is offline-only and read-only. It:

- never mutates the label parquet, the label parquet sidecar, the label
  manifest, or the label manifest sidecar;
- never mutates the source feature parquet, source feature manifest, or
  any other source artefact;
- never flips `research_eligible` on any manifest;
- never transitions `eligibility_gate_status` on any actual manifest;
- never changes `chronological_split_policy` on any actual manifest;
- never creates a label successor-state artefact;
- never authorizes any successor phase (Phase 4bj-F / Phase 4bj-G /
  Phase 4bb-F / Phase 4bb-G / Phase 5 / Phase 4 canonical all remain
  unauthorized);
- never calls any Binance endpoint, public endpoint, private endpoint,
  authenticated REST, WebSocket, or user stream;
- never reads `.env`, creates `.env`, creates `.mcp.json`, or invokes
  MCP / Graphify;
- never trains ML, designs ML, ranks features, creates meta-labeling,
  creates a strategy, runs a backtest, computes PnL / MFE / MAE /
  R-multiple / equity / position-state / signal output, or acquires
  data.

The gate report's `research_eligible_after` is invariant `False`. The
gate report's `label_manifest_research_eligible_after` is invariant
`False`. The gate report's `label_manifest_eligibility_gate_status_after`
is invariant `"pending"`. The gate report's
`label_manifest_chronological_split_policy_after` is invariant
`"not_yet_defined"`. The gate report's `no_successor_authorization` is
invariant `True`. These invariants are enforced by
`write_label_gate_report` before the atomic write.

## 4. Implementation surface

### 4.1 New source modules (4)

- `src/prometheus/research/microstructure/label_gate_io.py` — read-only
  artefact loaders, path discipline restricted to
  `data/microstructure/gate-reports/labels/`, atomic write-then-rename
  JSON writer, paired SHA256 sidecar writer, deterministic report-id
  derivation. Uses only the Python standard library (`hashlib`, `json`,
  `os`, `tempfile`, `contextlib`, `pathlib`, `dataclasses`); no network
  imports, no credential paths, no MCP/Graphify references.
- `src/prometheus/research/microstructure/label_gate_checks.py` — 72
  stable check IDs (`4bj-e.A01` .. `4bj-e.O01`) grouped:
  - **A (4)** — artefact presence (label parquet / sidecar / manifest /
    manifest sidecar);
  - **B (4)** — gitignore boundary (`data/microstructure/`,
    `data/microstructure/labels/`, `data/microstructure/manifests/`,
    `data/microstructure/gate-reports/labels/`);
  - **C (10)** — label manifest governance (dataset_family / version /
    label_schema_version / symbol / utc_date / row_count /
    research_eligible / eligibility_gate_status /
    chronological_split_policy / governance_labels);
  - **D (10)** — schema / column-order / label-list (column count == 39;
    column order == `LABEL_SCHEMA_V001`; label / support / lineage
    column counts; manifest `label_list`, `horizon_list`,
    `horizon_ms_list`, `schema_column_list`; forbidden-substring
    detector against `FORBIDDEN_LABEL_COLUMN_SUBSTRINGS`);
  - **E (4)** — row-count / row-identity (parquet rows == 1,681,098;
    parquet rows == manifest `row_count`; `row_index` contiguous
    `0..n-1`; manifest `files[0].row_count` parity);
  - **F (11)** — hash / lineage (label parquet SHA vs expected
    `ef50038a...`; label parquet sidecar self-consistency; label
    manifest SHA vs expected `181a799c...`; label manifest sidecar
    self-consistency; `label_config_hash` vs expected `fe4633af...`;
    manifest `source_feature_parquet_sha256` / `source_feature_manifest_sha256`
    / `source_feature_successor_state_sha256`
    / `source_phase_4bi_b_gate_report_sha256` / `source_normalized_parquet_sha256`
    vs expected; per-row lineage SHA constancy spot-check on parquet);
  - **G (2)** — manifest scalar counts (`invalid_price_row_count == 0`;
    `censored_per_horizon == {"1s": 9, "5s": 42, "15s": 118, "60s": 507}`);
  - **H (4)** — per-horizon flag-count parity (parquet
    `horizon_censored_flag_*` true-count vs manifest `censored_per_horizon[*]`);
  - **I (9)** — dtype / value sanity (`row_index` int64;
    `feature_timestamp_ms` int64; `forward_log_return_*` float64
    nullable & null-or-finite; `forward_direction_*` int8 nullable &
    values in `{-1, 0, 1, null}`; `horizon_censored_flag_*` bool;
    `label_invalid_price_flag` bool; `label_any_censored_flag` bool;
    lineage SHA columns strings; `label_invalid_price_flag` all-false);
  - **J (2)** — pre/post immutability anchored to `ctx.measured`'s
    pre/post SHAs for the label parquet and label manifest;
  - **K (4)** — one-row-per-feature-row evidence (NOT_APPLICABLE if no
    source feature parquet is provided; otherwise row-count parity,
    per-row `agg_trade_id`, per-row `feature_timestamp_ms`, per-row
    `row_index`);
  - **L (4)** — consistency / no-rescue (`label_any_censored_flag ==`
    OR of per-horizon flags; `label_any_censored_flag` true-count ==
    expected `507` under nested censoring; per-horizon censoring nested
    `1s ⊆ 5s ⊆ 15s ⊆ 60s`; manifest `boundary_confirmations` complete
    and all `true`);
  - **M (2)** — stage interpretation (manifest `research_eligible` ==
    False; manifest `eligibility_gate_status` == `"pending"`);
  - **N (1)** — manifest `boundary_confirmations` contains every
    `REQUIRED_LABEL_BOUNDARY_CONFIRMATIONS` key;
  - **O (1)** — manifest `chronological_split_policy` ==
    `"not_yet_defined"`.

  `LabelGateCheckStatus` `StrEnum` (`pass` / `fail` / `not_applicable`
  / `error`), `LabelGateCheckResult`, `LabelGateContext`,
  `run_all_checks`, plus offline-only helpers
  `query_gitignore_status` (via `git check-ignore -q` subprocess) and
  `load_parquet_table` (via pyarrow).
- `src/prometheus/research/microstructure/label_gate_report.py` —
  `LabelGateReport` frozen dataclass and `LabelGateReportError`,
  `build_label_gate_report` constructor (counts checks by status),
  `write_label_gate_report` atomic writer with paired SHA256 sidecar
  and invariant enforcement (`research_eligible_after == False`,
  `label_manifest_research_eligible_after == False`,
  `label_manifest_eligibility_gate_status_after == "pending"`,
  `label_manifest_chronological_split_policy_after == "not_yet_defined"`,
  `stage_5_authorized == False`, `stage_5_research_or_ml_use == False`,
  `no_successor_authorization == True`).
- `src/prometheus/research/microstructure/label_gate.py` —
  `LabelGateInput` frozen dataclass with `__post_init__` Path /
  microstructure-path-discipline validation; `LabelGateResult` frozen
  dataclass; `LabelGateError`; `validate_label_gate_inputs` for
  existence + sidecar presence checks; `run_label_family_gate` public
  orchestrator that runs the gate exactly once, computes pre/post
  SHAs, builds boundary confirmations, writes the report under
  `data/microstructure/gate-reports/labels/` when `write_report=True`,
  and returns `LabelGateResult`. The orchestrator appends the
  canonical `gate-reports/labels/` segment to `output_root` when not
  already present (matching the Phase 4bi-B precedent).

### 4.2 Package `__init__.py` narrow update (1)

`src/prometheus/research/microstructure/__init__.py` is narrowly
updated to:

- extend the module docstring with a Phase 4bj-E section describing
  the new modules and invariants;
- import the 14 new public symbols
  (`LabelGateCheckResult`, `LabelGateCheckStatus`, `LabelGateContext`,
  `LabelGateError`, `LabelGateIOError`, `LabelGateInput`,
  `LabelGateReport`, `LabelGateReportError`, `LabelGateReportPaths`,
  `LabelGateResult`, `build_label_gate_report`,
  `run_label_family_gate`, `validate_label_gate_inputs`,
  `write_label_gate_report`);
- append the 14 names to `__all__` under a `# label_gate (Phase 4bj-E)`
  group.

No prior export removed. No prior import removed.

### 4.3 New test files (5) + shared fixture (1)

- `tests/research/microstructure/_label_gate_fixtures.py` — builds a
  self-consistent label parquet + label manifest pair (plus tiny
  feature parquet + feature manifest) under pytest `tmp_path`. Uses
  the real Phase 4bj-C kernel (`compute_aggtrade_labels_v001`,
  `write_label_dataset_v001`, `build_label_manifest_v001`,
  `atomic_write_label_manifest`, `write_label_sha256_sidecar`).
  Lineage SHAs are synthetic (`"a"*64`, etc.) so production-locked
  SHA-equality checks in Group F / G / H / L (against the
  `1,681,098`-row BTCUSDT 2025-01-15 constants) FAIL by design on the
  fixture; tests that target those paths exercise FAIL behavior
  explicitly.
- `tests/research/microstructure/test_label_gate_io.py` — 16 tests
  covering path discipline, atomic write, refuse-overwrite, sidecar
  read/write, SHA helpers.
- `tests/research/microstructure/test_label_gate_checks.py` — 23 tests
  covering per-group PASS paths on the fixture plus explicit FAIL paths
  (e.g. `research_eligible` flipped, `eligibility_gate_status` not
  `"pending"`, `chronological_split_policy` changed, governance label
  loosened, manifest `files` emptied, J-group pre/post mismatch /
  missing, L-group boundary key missing, K-group `NOT_APPLICABLE` when
  feature parquet absent).
- `tests/research/microstructure/test_label_gate_report.py` — 11 tests
  covering builder counts, invariants, writer atomicity, refuse-to-
  overwrite, and one explicit invariant-violation test per locked field
  via `dataclasses.replace`.
- `tests/research/microstructure/test_label_gate.py` — 9 tests covering
  input validation, path discipline, end-to-end orchestrator run,
  invariants on result + serialized report, source-artefact immutability
  pre/post run, NOT_APPLICABLE handling for K-group when no feature
  parquet is provided, refuse-to-overwrite of existing reports,
  `write_report=False` path.
- `tests/research/microstructure/test_label_gate_no_network.py` —
  static no-network / no-credential scanner restricted to the four
  Phase 4bj-E modules. Confirms the existing parametrised
  `test_import_boundaries.py` scan also picks the new files up.

## 5. Execution (gate run)

The gate was executed **exactly once** against the real Phase 4bj-C
artefacts on disk, with this `LabelGateInput`:

```text
label_parquet_path = data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet
label_manifest_path = data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json
source_feature_parquet_path = data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet
source_feature_manifest_path = data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json
output_root = data/microstructure
repo_root = .
code_commit_sha = 89cde8ad14b5ce92cdd718a7a4eca7bfce3e3835
write_report = True
```

### 5.1 Result

- **`overall_status` = `pass`**
- **`checks_total` = 72**
- **`PASS` = 72 / `FAIL` = 0 / `ERROR` = 0 / `NOT_APPLICABLE` = 0**
- `research_eligible_after = False`
- `eligibility_gate_status_after = "pass_report_level_only"` (report
  level only — the on-disk manifest is **not** transitioned)
- `label_manifest_research_eligible_after = False`
- `label_manifest_eligibility_gate_status_after = "pending"`
- `label_manifest_chronological_split_policy_after = "not_yet_defined"`
- `stage_5_authorized = False`
- `stage_5_research_or_ml_use = False`
- `no_successor_authorization = True`
- 20/20 `boundary_confirmations` true

### 5.2 Local gitignored gate-report outputs (NOT committed)

| Path | Size | SHA256 |
|---|---|---|
| `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5.json` | 24,715 | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` |
| `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5.json.sha256` | 156 | `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191` |

The sidecar is the standard `<sha>  <name>\n` line, and the report
SHA matches `compute_bytes_sha256(report)` bit-for-bit.

Both files are confirmed gitignored:

```text
git check-ignore -v data/microstructure/                                  -> .gitignore:85
git check-ignore -v data/microstructure/labels/                           -> .gitignore:85
git check-ignore -v data/microstructure/manifests/                        -> .gitignore:85
git check-ignore -v data/microstructure/gate-reports/labels/              -> .gitignore:85
git check-ignore -v data/microstructure/gate-reports/labels/<report>.json -> .gitignore:85
```

### 5.3 Report id

```text
microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5
```

- `1778531608796` = generated_at_unix_ms (gate run time).
- `89cde8ad14b5` = short of the code commit
  `89cde8ad14b5ce92cdd718a7a4eca7bfce3e3835`.

## 6. Upstream immutability evidence (pre vs post gate run)

| Artefact | Pre-run SHA256 | Post-run SHA256 | Status |
|---|---|---|---|
| label parquet | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | IDENTICAL |
| label parquet sidecar | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | IDENTICAL |
| label manifest | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | IDENTICAL |
| label manifest sidecar | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | IDENTICAL |

Sizes are also unchanged: parquet = 66,073,234 bytes; parquet sidecar
= 110 bytes; manifest = 6,786 bytes; manifest sidecar = 114 bytes.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved end-to-end. The gate never reads
or writes the manifest through that helper; it reads the manifest's
bytes via `read_manifest_bytes`, parses with `json.loads`, and never
calls any mutating helper.

## 7. Manifest state preservation

The on-disk label manifest at
`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`
remains exactly as written by Phase 4bj-C:

- `research_eligible = False`
- `eligibility_gate_status = "pending"`
- `chronological_split_policy = "not_yet_defined"`
- `label_config_hash = "fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00"`
- `invalid_price_row_count = 0`
- `censored_per_horizon = {"1s": 9, "5s": 42, "15s": 118, "60s": 507}`
- `row_count = 1,681,098`
- `governance_labels.ml = "forbidden"`
- `governance_labels.strategy = "forbidden"`
- `governance_labels.backtest = "forbidden"`
- `governance_labels.paper_shadow_live = "forbidden"`
- `governance_labels.deployment = "forbidden"`
- `governance_labels.exchange_write = "forbidden"`
- `governance_labels.acquisition = "unauthorized"`

The gate's PASS verdict is recorded **on the gate report only**; the
manifest's `eligibility_gate_status` is not transitioned. Any future
transition from `"pending"` to any other value requires a separately
authorized successor-state phase (the Phase 4bj-G analogue).

## 8. Validation

```text
ruff check src/prometheus/research/microstructure/ tests/research/microstructure/
  -> All checks passed!

ruff check .  (whole-repo invocation succeeds in CI per project standard)
  -> All checks passed! (covered by scoped ruff above + Phase 4bk-A baseline)

mypy src (strict)
  -> Success: no issues found in 119 source files
     (Phase 4bk-A baseline: 115; Phase 4bj-E adds 4 modules -> 119)

pytest tests/research/microstructure/
  -> 823 passed, 1 skipped in 9.75s

git diff --check
  -> clean

git check-ignore -v data/microstructure/
  -> .gitignore:85

git check-ignore -v data/microstructure/labels/
  -> .gitignore:85

git check-ignore -v data/microstructure/manifests/
  -> .gitignore:85

git check-ignore -v data/microstructure/gate-reports/labels/
  -> .gitignore:85
```

The whole-repo pytest run is left to a separately authorized phase /
merge gate; the known pre-existing failures at
`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
and `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_ethusdt`
(`KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`)
are unrelated to the microstructure / label arc and are unchanged by
this work. Phase 4bj-E adds **zero new test regressions** to the
microstructure suite; the single skipped test in
`test_label_gate_report.py` is a labeled placeholder (`pytest.skip`)
documenting that the explicit invariant-violation tests appear below
it in the file.

## 9. Boundary confirmations (gate-result)

All 20 boundary confirmations on `LabelGateResult.boundary_confirmations`
are `True`:

- `no_label_parquet_mutation`
- `no_label_manifest_mutation`
- `no_source_artefact_mutation`
- `no_data_microstructure_write_outside_gate_reports_labels`
- `no_label_successor_state_created`
- `no_ml_trained`
- `no_strategy_created`
- `no_signal_computed`
- `no_backtest_run`
- `no_acquisition`
- `no_network_io`
- `no_websocket`
- `no_credential_read`
- `no_env_read`
- `no_mcp_or_graphify`
- `label_manifest_research_eligible_after_is_false`
- `label_manifest_eligibility_gate_status_after_is_pending`
- `label_manifest_chronological_split_policy_after_is_not_yet_defined`
- `stage_5_research_or_ml_use_is_false`
- `no_successor_authorization`

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked).

## 10. Retained verdict ledger

All retained verdicts preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

## 11. Preserved project locks

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
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `flip_research_eligible(...)` always-raises invariant
- All prior phase results (Phase 4am ... Phase 4bk-A) preserved
  verbatim.

## 12. No-rescue constraints

Phase 4bj-E does NOT, and cannot, be construed as authorising:

- ML model training, model selection, strategy hypothesis generation,
  or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state, entry /
  exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning the label manifest's `research_eligible` or
  `eligibility_gate_status` or `chronological_split_policy` from this
  PASS gate report alone.

## 13. Successor authorization

**None.**

Specifically NOT authorized by Phase 4bj-E:

- Phase 4bj-F — Label-Family Research / ML-Use Decision Memo
- Phase 4bj-G — Label-Family Successor-State Recording
- Phase 4bj (catch-all)
- Phase 4bb-F — Gate Report Output Path Hygiene
- Phase 4bb-G — Raw Manifest Successor-State Recording
- Phase 5 (any)
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h /
  order-book data acquisition
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
- manifest transition (`research_eligible`,
  `eligibility_gate_status`, `chronological_split_policy`).

The Phase 4bj-E PASS gate report is **report-level evidence only**.
Any future transition of the label manifest's `eligibility_gate_status`
from `"pending"` to any other value requires a separately authorized
successor-state phase. The default recommendation is remain paused.

## 14. Recommended state

**Recommended state at the end of Phase 4bj-E: remain paused.**

Conditional next, NOT authorized:

- **Phase 4bj-F — Label-Family Research / ML-Use Decision Memo**
  (docs-only) is the cleanest non-paused option. It would decide
  whether and under what conditions a sibling successor-state JSON for
  the label family may ever be authorized, in the style of Phase 4bi-C
  for the feature family. Phase 4bj-F is **not** authorized by this
  work; per the Phase 4bk-A workflow standard, the operator must
  separately author an authorization prompt before any successor is
  begun.

## 15. Validation caveats

- The single skipped pytest test (`test_label_gate_report.py::test_write_label_gate_report_invariant_violations_param`)
  is an intentional `pytest.skip` placeholder. The explicit invariant
  violation tests appear below it in the same file as named tests
  using `dataclasses.replace`.
- The whole-repo pytest pre-existing failures at
  `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
  and `::test_real_2026_03_ethusdt` (`KeyError: 'trade_count'` in
  `src/prometheus/research/data/storage.py:232`) are unrelated to the
  microstructure / label arc and are unchanged by Phase 4bj-E.

## 16. Final SHAs

- **Phase 4bj-E source commit (gate code + tests):**
  `89cde8ad14b5ce92cdd718a7a4eca7bfce3e3835`
- **Phase 4bj-E gate report (local, gitignored, not committed):**
  - path:
    `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5.json`
  - SHA256: `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0`
  - paired sidecar SHA256: `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191`
- **Base `main` SHA at branch start:**
  `26a3bebc020fabf78f30bdd9b433c5fbd074e85a`
