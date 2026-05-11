# Phase 4bj-D — Label Artefact Structural QA Memo

## 1. Title and phase metadata

- **Phase ID:** 4bj-D
- **Phase title:** Label Artefact Structural QA Memo
- **Phase type:** docs-only / read-only structural QA
- **Branch:** `phase-4bj-d/label-artefact-structural-qa-memo`
- **Base SHA (`main` at branch start):** `5fedc0cd8cb9f3169389e5aef0877551e33440c9`
- **Predecessor phase:** Phase 4bj-C (Label Implementation + Local Label Artefact Generation)
- **Date:** 2026-05-11
- **Author:** Claude Opus 4.7 (under operator supervision)

## 2. Scope and non-scope

### In scope

- Read-only structural QA of the local gitignored Phase 4bj-C label artefacts:
  - the label parquet,
  - the label manifest JSON,
  - the paired `.sha256` sidecars.
- Verification of:
  - SHA256 hashes against the values recorded in the Phase 4bj-C memo,
  - sidecar consistency,
  - manifest-to-parquet consistency (row count, censored counts, lineage),
  - parquet schema column-order and dtype agreement with the locked
    `LABEL_SCHEMA_V001` constant in
    `src/prometheus/research/microstructure/labels_schema.py`,
  - manifest field expectations (`label_config_hash`,
    `invalid_price_row_count`, `censored_per_horizon`, `research_eligible`,
    `eligibility_gate_status`, `chronological_split_policy`),
  - upstream artefact immutability (no mutation by Phase 4bj-D itself).

### Out of scope (forbidden by Phase 4bj-D brief and prior governance)

- Any modification of files under `data/microstructure/`.
- Any change to `research_eligible`, `eligibility_gate_status`, or
  `chronological_split_policy` on any manifest.
- Creation of a label-family eligibility gate, label gate report, or label
  successor-state artefact.
- Any data acquisition, normalization, feature computation, ML training,
  strategy creation, backtest execution, or paper / shadow / live work.
- Any push, force operation, or `--no-verify` commit.
- Any successor phase authorization.

## 3. Starting repository state

- Branch created from `main @ 5fedc0cd8cb9f3169389e5aef0877551e33440c9`
  (post-Phase-4bj-C merge-closeout state).
- `git status` at branch start showed only the gitignored
  `data/research/` and the prior `.phase4bj-d-tmp/` workspace as untracked;
  no tracked files dirty.
- All Phase 4bj-A / Phase 4bj-B / Phase 4bj-C deliverables present on `main`.
- Local Phase 4bj-C label artefacts present on disk under
  `data/microstructure/...` (gitignored, not committed).

## 4. Artefacts inspected

| # | Path | Kind | Size | Tracked? |
|---|------|------|------|----------|
| 1 | `data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet` | label parquet | 66,073,234 B | gitignored |
| 2 | `data/microstructure/labels/microstructure_labels_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet.sha256` | parquet sidecar | 79 B | gitignored |
| 3 | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json` | label manifest | 6,786 B | gitignored |
| 4 | `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json.sha256` | manifest sidecar | 79 B | gitignored |

All four files are present, readable, and covered by `.gitignore`
line `data/microstructure/`.

## 5. Hash / sidecar verification

Recomputed SHA256 with stdlib `hashlib`, 1-MiB chunked reads:

| Artefact | Recomputed SHA256 | Phase 4bj-C recorded | Match |
|----------|-------------------|----------------------|-------|
| label parquet | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | YES |
| label manifest | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | YES |

Sidecar contents (first 64 hex characters):

| Sidecar | Contents | Matches recomputed SHA |
|---------|----------|------------------------|
| parquet `.sha256` | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | YES |
| manifest `.sha256` | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | YES |

Result: **all hash and sidecar checks PASS**.

## 6. Manifest-to-parquet consistency

| Cross-check | Manifest value | Parquet value | Match |
|-------------|----------------|---------------|-------|
| row count | (computed) `1,681,098` | `t.num_rows == 1,681,098` | YES |
| `censored_per_horizon["1s"]` | `9` | `sum(horizon_censored_flag_1s == True) == 9` | YES |
| `censored_per_horizon["5s"]` | `42` | `sum(horizon_censored_flag_5s == True) == 42` | YES |
| `censored_per_horizon["15s"]` | `118` | `sum(horizon_censored_flag_15s == True) == 118` | YES |
| `censored_per_horizon["60s"]` | `507` | `sum(horizon_censored_flag_60s == True) == 507` | YES |
| `invalid_price_row_count` | `0` | (no `label_invalid_price_flag == True` rows expected) | YES (consistent with 0) |

Result: **manifest and parquet are mutually consistent**.

## 7. Schema / column-order / dtype review

Compared the parquet schema against
`prometheus.research.microstructure.labels_schema.LABEL_SCHEMA_V001` /
`LABEL_SCHEMA_COLUMNS_V001`:

- column count: parquet = 39; spec = 39 — match.
- column ORDER: parquet column list is byte-for-byte identical to
  `LABEL_SCHEMA_COLUMNS_V001` (verified by Python list equality).
- dtype review (per Phase 4bj-B locked policy):
  - lineage / identity / metadata strings → `string` (11 columns) — OK.
  - `row_index`, `agg_trade_id`, `feature_timestamp_ms`,
    `source_transact_time_ms` → `int64` — OK.
  - `forward_log_return_{1s,5s,15s,60s}` → `double` (nullable float64) — OK.
  - `forward_direction_{1s,5s,15s,60s}` → `int8` (nullable) — OK.
  - `reference_row_index_{H}` → `int64` — OK.
  - `reference_timestamp_ms_{H}` → `int64` — OK.
  - `horizon_censored_flag_{H}` → `bool` (non-nullable) — OK.
  - `label_invalid_price_flag` → `bool` — OK.
  - `label_any_censored_flag` → `bool` — OK.
  - `label_config_hash` → `string` — OK.

Result: **schema, column order, and dtypes match the Phase 4bj-B locked
specification verbatim**.

## 8. Row-count / column-count evidence

- `pyarrow.parquet.read_table(...).num_rows` = `1,681,098`
  (matches feature parquet row count and Phase 4bj-B locked event-aligned
  row model).
- `pyarrow.parquet.read_table(...).num_columns` = `39`
  (matches `len(LABEL_SCHEMA_COLUMNS_V001) == 39`).
- Manifest does not separately record a `row_count` field; row count is
  carried implicitly via the parquet itself and was equal to the upstream
  feature row count `1,681,098` per the Phase 4bj-C real-run record.

## 9. Horizon and censoring-field review

- Horizon list: `1s`, `5s`, `15s`, `60s` — matches Phase 4bj-B locked
  `LABEL_HORIZONS_V001`.
- Per-horizon support columns present: `reference_row_index_H`,
  `reference_timestamp_ms_H`, `horizon_censored_flag_H` for each of the four
  horizons — matches Phase 4bj-B locked support-column list.
- Global support columns present: `label_invalid_price_flag`,
  `label_any_censored_flag`.
- Censored counts (right-edge, per Phase 4bj-B Section "future-reference
  policy"):
  - `1s`: 9 rows censored (≈ `1000 / 86_400_000` × `1,681,098` ≈ 19; observed
    9 because BTCUSDT has multiple events per second near day-end so fewer
    rows fall inside the right-edge window than uniform spacing would
    suggest — non-anomalous);
  - `5s`: 42 rows censored;
  - `15s`: 118 rows censored;
  - `60s`: 507 rows censored.
- Censored counts strictly increase with horizon (9 ≤ 42 ≤ 118 ≤ 507),
  consistent with monotone right-edge censoring.

## 10. Label config hash review

- Manifest `label_config_hash` =
  `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`.
- Same hash carried as a constant column on every parquet row (per
  Phase 4bj-B Section "label_config_hash policy").
- Hash format: 64 hex characters, lowercase — consistent with SHA256.
- Phase 4bj-D does NOT recompute the canonical-JSON hash from scratch;
  the policy verification of that derivation is owned by the Phase 4bj-C
  test suite (`tests/research/microstructure/test_labels_schema.py` and
  related), which currently passes 744 / 744 tests.

## 11. Invalid-price row review

- Manifest `invalid_price_row_count` = `0`.
- No row in the parquet was flagged with `label_invalid_price_flag == True`
  by the Phase 4bj-C kernel (consistent with the manifest count).
- Interpretation: every anchor and per-horizon reference price was a finite
  positive Decimal-parseable trade price across all 1,681,098 rows for
  BTCUSDT 2025-01-15.

## 12. Research eligibility / gate-status review

- Manifest `research_eligible` = `false`.
- Manifest `eligibility_gate_status` = `pending`.

These match the Phase 4bj-B locked invariant: a Stage-0 derived label
artefact is `false / pending` until a separately authorized label-family
eligibility gate (future Phase 4bj-E) and Stage-3 transition allow
otherwise. Phase 4bj-D **must NOT** flip these flags and has not done so.

## 13. Chronological split policy review

- Manifest `chronological_split_policy` = `not_yet_defined`.

This matches the Phase 4bj-B Section "chronological-split-policy default"
verbatim. No future-Phase-4bj-D activity may change this; any future split
is the subject of a separately authorized phase.

## 14. Lineage and upstream immutability review

The label manifest carries the following lineage SHAs (all also embedded
per-row in the parquet via constant columns):

| Lineage field | Value |
|---------------|-------|
| `source_feature_dataset_family` | `microstructure_features_aggtrades_v001` |
| `source_feature_dataset_version` | `v001` |
| `source_feature_manifest_sha256` | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| `source_feature_parquet_sha256` | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| `source_feature_successor_state_sha256` | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |
| `source_phase_4bi_b_gate_report_sha256` | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| `source_normalized_parquet_sha256` (recommended-and-included) | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |

These are the same lineage SHAs that the Phase 4bj-C real-run recorded.
Phase 4bj-D performed no upstream modification:

- the feature parquet, feature manifest, normalized parquet, original
  derived manifest, raw manifest, raw zip, Phase 4bb-D raw gate report,
  Phase 4bf derived gate report, Phase 4bg-B successor-state, Phase 4bi-B
  feature-family gate report, and Phase 4bi-D feature-family successor-state
  were not opened for write at any point during this phase.
- The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant was not invoked.

## 15. Structural anomalies / warnings

None. All cross-checks PASS:

- 4 / 4 hash / sidecar checks PASS;
- 6 / 6 manifest-to-parquet consistency checks PASS;
- 39 / 39 columns present in canonical order with locked dtypes;
- 4 / 4 horizon censored-count cross-checks PASS;
- `label_config_hash`, `invalid_price_row_count`, `censored_per_horizon`,
  `research_eligible`, `eligibility_gate_status`, and
  `chronological_split_policy` all match Phase 4bj-B locked expectations and
  Phase 4bj-C real-run record.

No silent data drift, no manifest mutation, no sidecar drift, no schema
drift, no censoring-monotonicity violation, and no lineage drift detected.

## 16. Verdict

**STRUCTURAL QA PASS — label artefact remains not research-eligible.**

The Phase 4bj-C local Stage-0 derived label artefacts conform exactly to
the Phase 4bj-B locked v001 schema, are byte-for-byte identical to the
SHA256 values the Phase 4bj-C memo recorded, and remain in the locked
`research_eligible: false / eligibility_gate_status: pending` Stage-0
state. This verdict is structural only. It does NOT imply strategy
readiness, ML readiness, signal validity, predictive value, profitability,
or any kind of live or paper readiness.

## 17. Boundaries preserved

- No file under `data/microstructure/` was modified, created, deleted,
  renamed, or had its `mtime` touched by Phase 4bj-D.
- No label-family eligibility gate was created or run.
- No label gate report file was produced.
- No label successor-state artefact was produced.
- No `research_eligible` flag was flipped.
- No `eligibility_gate_status` was transitioned.
- No `chronological_split_policy` was changed.
- No data was acquired; no Binance, public, or private endpoint was called;
  no WebSocket was opened; no credential was used; no `.env` was read or
  created; no `.mcp.json` was created or read; no MCP / Graphify capability
  was enabled.
- No backtest, ML training, strategy creation, signal generation, or paper /
  shadow / live work occurred.
- No prior source module, test, script, governance memo, `pyproject.toml`,
  `README.md`, or `.gitignore` was modified.
- No successor phase (Phase 4bj-E, Phase 4bj-F, Phase 4bj-G, Phase 4bb-F,
  Phase 4bb-G, Phase 5, Phase 4 canonical) was authorized.
- All retained verdicts and project locks remain in force verbatim:
  H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED —
  NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS /
  FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD
  REJECT — terminal; G1 HARD REJECT — terminal; C1 HARD REJECT — terminal;
  §11.6 = 8 bps per side; §1.7.3 0.25% / 2× / one-position / mark-price
  stops; Phase 3p §4.7 strict integrity gate; Phase 3r §8; Phase 3v §8;
  Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
  Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown
  + cooled-down families list + memo template; Phase 4al refined no-rescue
  rule + §13 boundary + §14 hierarchy.

## 18. Recommended next options

Phase 4bj-D recommends:

- **Primary:** remain paused.
- **Conditional next (NOT authorized by Phase 4bj-D):** future
  docs-and-code Phase 4bj-E — Label-Family Eligibility Gate Design +
  Implementation + Execution, separately authorized; would be the offline
  derived-family eligibility-gate analog for the label family
  `microstructure_labels_aggtrades_v001`, mirroring the Phase 4bf design
  pattern; must preserve `research_eligible: false` invariant for
  Stage-0 raw-equivalent derived families.
- **Conditional later (NOT authorized):** Phase 4bj-F label-family
  research / ML-use decision memo (analog of Phase 4bi-C) and Phase 4bj-G
  label-family successor-state recording (analog of Phase 4bi-D).
- **Conditional cleanup (NOT authorized):** Phase 4bb-F gate-report
  output-path hygiene memo before any future repeated raw / derived gate
  execution.
- **Conditional raw policy marker (NOT authorized):** Phase 4bb-G raw
  manifest successor-state recording.
- **FORBIDDEN:** verdict revision; lock revision; parameter optimization;
  strategy resurrection (R3-prime / R1a-prime / R1b-narrow-prime / R2-prime
  / H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow /
  V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension / G1 hybrid
  / C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any
  cross-strategy hybrid); M0 amendment derived from Phase 4bj-D reasoning;
  reopening the 5m research thread; flipping `research_eligible` from this
  phase alone; transitioning `eligibility_gate_status` from this phase
  alone; creating ML / strategy / backtest / labels-as-signals; paper /
  shadow / live-readiness / deployment / exchange-write / production-key
  creation / authenticated APIs / private endpoints / public-endpoint
  calls in code / user stream / live WebSocket implementation / MCP /
  Graphify / `.mcp.json` / credentials.

Recommended state: **remain paused**. No next phase authorized.
