# Phase 4bj-B — Label Schema Finalization Memo

Date: 2026-05-10
Phase: 4bj-B
Phase type: docs-only label-schema finalization memo
Branch: phase-4bj-b/label-schema-finalization
Base: main at the post-Phase-4bj-A merge-closeout state
  (`777edbf8460e50067cdd6301a240276eaed1ffbf`)
Phase 4bj-A merge commit (verified ancestor of main):
  `8a99a74930b5c8b33c63e9eceb0116e5e97b11b8`
Status: drafted (docs-only; text-only)

---

## 1. Current state

Phase 4bj-A is merged to main and selected
**Outcome 1 — Label boundary admissible in principle, implementation
deferred** for the Stage-5-admissible feature family
`microstructure_features_aggtrades_v001`. Phase 4bj-A defined the
label-boundary policy at policy level only and proposed a
conservative initial future label family
`microstructure_labels_aggtrades_v001` containing four forward-log-
return columns and four forward-direction columns at horizons
{1s, 5s, 15s, 60s} — without authorizing implementation.

No labels exist. No targets exist. No label namespace exists. No
label manifest exists. No label gate report exists. No label
successor-state exists. The feature manifest continues to carry
`research_eligible: false / eligibility_gate_status: pending`.

Phase 4bj-B is the schema-finalization phase within the Phase 4bj
family. It locks the **exact v001 label schema** at policy level so
that a future Phase 4bj-C implementation phase, if separately
authorized, cannot drift on column names, horizons, anchor policy,
future-reference policy, formulas, dtypes, lineage, manifest fields,
or QA expectations.

## 2. Inputs reviewed

The following artefacts were inspected read-only:

- Phase 4bj-A main memo and closeout:
  - `docs/00-meta/implementation-reports/`
    `2026-05-10_phase-4bj-a_label-boundary-target-definition.md`
  - `docs/00-meta/implementation-reports/`
    `2026-05-10_phase-4bj-a_closeout.md`
  - `docs/00-meta/implementation-reports/`
    `2026-05-10_phase-4bj-a_merge-closeout.md`
- Phase 4bi-D successor-state JSON:
  - path:
    `data/microstructure/successor-state/`
    `microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json`
  - SHA256:
    `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`
  - paired `.sha256` sidecar: matches
  - successor_stage = `Feature Stage-5`;
  - successor_research_ml_admissible = `true`;
  - successor_research_eligible = `true`;
  - successor_eligibility_gate_status = `pass`;
  - manifest_mutation_permitted = `false`;
  - original_feature_manifest_research_eligible = `false`;
  - original_feature_manifest_eligibility_gate_status = `pending`;
  - governance_labels.labels = `forbidden`;
  - governance_labels.targets = `forbidden`;
  - governance_labels.ml = `forbidden`;
  - governance_labels.strategy = `forbidden`;
  - governance_labels.backtest = `forbidden`;
  - governance_labels.acquisition = `unauthorized`;
  - boundary_confirmations.no_successor_authorization = `true`.
- Phase 4bi-B feature-family gate report:
  - path:
    `data/microstructure/gate-reports/features/`
    `microstructure_features_aggtrades_v001__v001__phase-4bi-b__1778436978312__2bc026b4e0d9.json`
  - SHA256:
    `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988`
  - overall_status: `pass`; 70 / 70 PASS.
- Feature parquet:
  - path:
    `data/microstructure/features/microstructure_features_aggtrades_v001/`
    `BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet`
  - SHA256:
    `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`
  - rows: 1 681 098.
- Feature manifest:
  - path:
    `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json`
  - SHA256:
    `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718`
  - `research_eligible`: `false`;
  - `eligibility_gate_status`: `pending`.
- Original derived manifest:
  - SHA256:
    `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`
  - `research_eligible`: `false`; `eligibility_gate_status`: `pending`.
- Original raw manifest:
  - SHA256:
    `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`
  - `research_eligible`: `false`; `eligibility_gate_status`: `pending`.
- Normalized parquet:
  - SHA256:
    `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`.
- Raw zip:
  - SHA256:
    `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`.
- Phase 4bb-D raw gate report:
  - SHA256:
    `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`.
- Phase 4bf derived gate report:
  - SHA256:
    `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`.
- Phase 4bg-B successor-state JSON:
  - SHA256:
    `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`.

No label namespace exists. No label manifest exists. No label gate
report exists. No label successor-state exists.

## 3. Scope

Phase 4bj-B finalizes, at policy level only:

- the exact label family identity and naming;
- the exact label schema version;
- the exact label column list (eight columns);
- the exact horizon list (four horizons);
- the exact anchor-row and anchor-price policy;
- the exact future-reference-row and future-reference-price policy;
- the exact `forward_log_return` formula;
- the exact `forward_direction` derivation policy;
- the exact support / quality column set;
- the exact lineage / identity column set;
- the exact dtype policy;
- the exact null / censoring policy;
- the exact future label manifest schema;
- the exact `label_config_hash` policy;
- the exact future label output paths;
- the exact future implementation acceptance criteria;
- the exact future QA / gate expectations;
- the exact chronological-split-policy default;
- the exact no-rescue / M0 boundary.

Phase 4bj-B applies prospectively. It does not authorize
implementation work and does not authorize Phase 4bj-C.

## 4. Non-scope

Phase 4bj-B does **not**:

- modify source code;
- modify tests;
- modify scripts;
- create label-computation code;
- create target-computation code;
- create ML code;
- create strategy code;
- create backtest code;
- create analysis scripts;
- create notebooks;
- rerun the feature-family eligibility gate;
- rerun feature computation;
- regenerate the feature parquet;
- regenerate the feature manifest;
- modify the feature parquet;
- modify the feature manifest;
- modify the Phase 4bi-B gate report;
- modify the Phase 4bi-D successor-state artefact;
- modify any sidecar;
- run the normalizer;
- rerun the raw eligibility gate;
- rerun the derived-family gate;
- generate any new gate report (raw, derived, feature, label, or
  other);
- create a label manifest;
- create a target manifest;
- create a label successor-state artefact;
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
- call public or private endpoints;
- call Binance APIs;
- open WebSockets;
- request or use credentials;
- read or create `.env`;
- create or read `.mcp.json`;
- enable MCP or Graphify;
- authorize labels or targets beyond schema finalization;
- authorize ML implementation;
- authorize strategy;
- authorize backtests;
- authorize acquisition;
- authorize paper / shadow / live or deployment;
- authorize Phase 4bj-C implementation;
- revise retained verdicts;
- change project locks;
- amend M0;
- authorize Phase 5, Phase 4 canonical, exchange-write, production
  keys, authenticated APIs, private endpoints, user stream, or live
  WebSocket implementation;
- commit anything under `data/microstructure/`.

## 5. Phase 4bj-A dependency

Phase 4bj-B finalizes a schema only because Phase 4bj-A established
the label-boundary policy at policy level. The Phase 4bj-A boundary
binds Phase 4bj-B without exception:

- labels must be a sibling artefact family;
- labels must never feed back into features;
- labels must use only `transact_time_ms <= T` and feature row index
  `<= R` inside feature columns; labels may use future information
  only inside the label routine itself;
- labels must preserve lineage to the feature parquet, feature
  manifest, Phase 4bi-D successor-state, and Phase 4bi-B gate report;
- label manifests default to `research_eligible: false /
  eligibility_gate_status: pending`;
- label design does not prove edge;
- direction accuracy is not profitability;
- RR / WR / expectancy are strategy-evaluation concepts, not label-
  schema proof;
- M0 (Phase 4ak twelve-clause gate + post-null cooldown rule + memo
  template + cooled-down families list) remains binding;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
  remain binding.

The Phase 4bi-D successor-state's `successor_research_ml_admissible:
true` field is sibling-artefact only and does not flip
`research_eligible` on any actual manifest. Phase 4bj-B reads it as
policy-level admissibility and finalizes a v001 schema consistent
with that admissibility, not as authorization to implement.

## 6. Schema-finalization objective

Phase 4bj-B answers a single question:

> Given Phase 4bj-A Outcome 1, what is the **exact** v001 label
> schema — column-by-column, horizon-by-horizon, formula-by-formula,
> dtype-by-dtype, lineage-by-lineage — that any future Phase 4bj-C
> implementation must follow without amendment?

Phase 4bj-B locks that schema so that future implementation cannot
silently widen scope, silently change formulas, silently re-anchor
labels, silently drop or add columns, silently change horizons,
silently shuffle dtypes, silently change null policy, silently
add ML / strategy / signal semantics, or silently leak future
information into features.

## 7. Selected outcome

**Selected outcome: Outcome 1 — Label schema finalized,
implementation deferred.**

Justification:

- Phase 4bj-A is merged and selected Outcome 1.
- Phase 4bi-D successor-state JSON exists at the recorded path and
  its SHA256 matches
  `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`.
- Phase 4bi-D successor-state records Stage-5 admissibility only at
  sibling-artefact level (`manifest_mutation_permitted = false`;
  governance labels all `forbidden` / `unauthorized`;
  `boundary_confirmations.no_successor_authorization = true`).
- Feature manifest remains `research_eligible: false /
  eligibility_gate_status: pending`.
- No labels or targets currently exist.
- All 10 upstream artefact SHAs preserve byte-identical pre-phase
  values.
- The memo finalizes an exact leakage-safe schema without
  weakening M0 or no-rescue rules.

Outcome 1 does **not** authorize Phase 4bj-C. Phase 4bj-C remains a
separately authorized future option.

## 8. Finalized label family identity

Locked by Phase 4bj-B:

| field | value |
|---|---|
| `dataset_family` | `microstructure_labels_aggtrades_v001` |
| `dataset_version` | `v001` |
| `label_schema_version` | `v001` |
| `source_feature_dataset_family` | `microstructure_features_aggtrades_v001` |
| `source_feature_dataset_version` | `v001` |
| `source_feature_manifest_sha256` | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| `source_feature_parquet_sha256` | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| `source_feature_successor_state_sha256` | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |
| `source_phase_4bi_b_gate_report_sha256` | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| `source_normalized_parquet_sha256` (optional but recommended) | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| `symbol` | `BTCUSDT` (one symbol per artefact; future expansion separately authorized) |
| `utc_date` | `2025-01-15` |

## 9. Finalized row model

Event-aligned to feature rows:

- **One label row per feature row.**
- `row_count` = `1681098` (matches feature parquet exactly).
- `row_index` = `0..1681097` (matches feature parquet exactly).
- No row dropping.
- No resampling.
- No synthetic timestamps.
- No upsampling.
- No downsampling.
- No cross-day stitching.
- Right-edge horizon values are **nullable / censored**, not removed.
- Row ordering uses `(transact_time_ms ASC, row_index ASC)`, matching
  Phase 4bh row contract verbatim.

## 10. Finalized column schema

The future label parquet must contain **exactly** the following 33
columns in this canonical order. (8 feature labels + 8 reference row
support + 8 reference timestamp support + 4 horizon censoring flags
+ 2 row-level flags + 3 family identity + 1 schema version + 4
source lineage + 1 phase-4bi-B lineage + 1 normalized lineage + 2
identity + 2 anchor identity + 1 label-config hash = some 8 + 8 + 8
+ 4 + 2 + 11 = 41 columns; the canonical list is enumerated below
and overrides any informal count above.)

Lineage / identity / metadata columns (15):

1. `dataset_family` — string
2. `dataset_version` — string
3. `label_schema_version` — string
4. `source_feature_dataset_family` — string
5. `source_feature_dataset_version` — string
6. `source_feature_manifest_sha256` — string
7. `source_feature_parquet_sha256` — string
8. `source_feature_successor_state_sha256` — string
9. `source_phase_4bi_b_gate_report_sha256` — string
10. `symbol` — string
11. `utc_date` — string
12. `row_index` — int64
13. `agg_trade_id` — int64
14. `feature_timestamp_ms` — int64 (UTC ms)
15. `source_transact_time_ms` — int64 (UTC ms)

Optional but recommended lineage column (1):

16. `source_normalized_parquet_sha256` — string

Label config hash column (1):

17. `label_config_hash` — string

Regression label columns (4):

18. `forward_log_return_1s` — nullable float64
19. `forward_log_return_5s` — nullable float64
20. `forward_log_return_15s` — nullable float64
21. `forward_log_return_60s` — nullable float64

Classification label columns (4):

22. `forward_direction_1s` — nullable int8 in `{-1, 0, 1}`
23. `forward_direction_5s` — nullable int8 in `{-1, 0, 1}`
24. `forward_direction_15s` — nullable int8 in `{-1, 0, 1}`
25. `forward_direction_60s` — nullable int8 in `{-1, 0, 1}`

Per-horizon support columns (12 = 4 × 3):

26. `reference_row_index_1s` — nullable int64
27. `reference_timestamp_ms_1s` — nullable int64
28. `horizon_censored_flag_1s` — bool
29. `reference_row_index_5s` — nullable int64
30. `reference_timestamp_ms_5s` — nullable int64
31. `horizon_censored_flag_5s` — bool
32. `reference_row_index_15s` — nullable int64
33. `reference_timestamp_ms_15s` — nullable int64
34. `horizon_censored_flag_15s` — bool
35. `reference_row_index_60s` — nullable int64
36. `reference_timestamp_ms_60s` — nullable int64
37. `horizon_censored_flag_60s` — bool

Global support / QA columns (2):

38. `label_invalid_price_flag` — bool
39. `label_any_censored_flag` — bool

**Total finalized columns: 39**, with column #16
(`source_normalized_parquet_sha256`) recommended-but-optional and
defaulting to **included** unless the future implementation memo
explicitly justifies excluding it. If column #16 is included, the
column count remains 39 inclusive; if excluded, the column count is
38 and the future label manifest must record `column_count = 38`.
For the canonical v001 schema, Phase 4bj-B records column #16 as
**included** by default.

## 11. Finalized label list

The future label parquet must include **exactly** these eight label
columns and no others:

- `forward_log_return_1s`
- `forward_log_return_5s`
- `forward_log_return_15s`
- `forward_log_return_60s`
- `forward_direction_1s`
- `forward_direction_5s`
- `forward_direction_15s`
- `forward_direction_60s`

The following label classes are **forbidden** at v001:

- barrier labels;
- target-before-stop labels;
- MFE labels;
- MAE labels;
- R-multiple labels;
- PnL labels;
- strategy-action labels;
- position-state labels;
- execution-quality labels;
- cross-symbol labels;
- cross-sectional labels;
- model-score labels;
- alpha / edge labels;
- prediction labels;
- decision-score labels;
- entry / exit labels;
- equity / drawdown labels;
- exchange-write outcome labels.

## 12. Finalized horizon list

Locked exactly:

- `1s` = `1000` ms
- `5s` = `5000` ms
- `15s` = `15000` ms
- `60s` = `60000` ms

`horizon_list = ["1s", "5s", "15s", "60s"]`
`horizon_ms_list = [1000, 5000, 15000, 60000]`

Explicitly deferred at v001:

- `30s`
- `5m`
- `15m`
- `30m`
- `1h`
- `4h`
- day-end
- multi-day horizons

A future amendment memo would be required to widen the horizon list;
silent widening at implementation time is forbidden.

## 13. Finalized forward-reference price policy

For every feature row `R` with anchor timestamp `T = feature_timestamp_ms`
and per horizon `H` in `{1s, 5s, 15s, 60s}` with `H_ms` in
`{1000, 5000, 15000, 60000}`:

- **target_timestamp_ms** = `T + H_ms`.
- If `target_timestamp_ms > final_source_normalized_transact_time_ms`
  for the artefact's `utc_date` (i.e., the maximum
  `transact_time_ms` across the normalized aggTrades source within
  the day), then:
  - `horizon_censored_flag_H = true`,
  - `forward_log_return_H = null`,
  - `forward_direction_H = null`,
  - `reference_row_index_H = null`,
  - `reference_timestamp_ms_H = null`.
- Otherwise:
  - `reference_row_index_H` = the **largest** `row_index` in the
    normalized aggTrades source such that
    `transact_time_ms <= target_timestamp_ms`.
  - When multiple rows share the same maximum
    `transact_time_ms <= target_timestamp_ms`, choose the largest
    `row_index` at that timestamp (this is the Phase 4bh same-
    timestamp tie-break, applied inside the label routine only).
  - `reference_timestamp_ms_H` = the `transact_time_ms` of that
    chosen normalized aggTrades row.
  - `reference_trade_price_H` = the trade price of that chosen
    normalized aggTrades row, parsed from the Decimal-as-string
    column.

Forbidden:

- using mark price for any anchor or reference;
- using index price;
- using bid / ask / book midpoint;
- using order-book data;
- using external data;
- using the first trade **after** `target_timestamp_ms`;
- looking past `target_timestamp_ms` for any horizon;
- using future feature columns;
- using any future label column to compute another label;
- cross-midnight stitching (treat each `utc_date` independently in
  v001).

**Anchor price** for row `R`:

- `anchor_trade_price` = the trade price of the normalized aggTrades
  row identified by `(agg_trade_id, row_index)` for feature row `R`.
- The anchor price domain is the same trade-price domain as the
  feature parquet's price-related Decimal columns (Phase 4bh
  contract verbatim).

Rationale (recorded):

> This policy measures the last observed trade price at or before
> the future horizon timestamp without peeking past the horizon. It
> avoids forward-trade bias, mark-price domain mixing, and book-data
> dependence. It treats each UTC day independently to match the
> Phase 4bh row-by-row, day-by-day artefact scope.

## 14. Finalized `forward_log_return` formula

For every (row R, horizon H) where the horizon is **not** censored
and both anchor and reference prices are valid:

```
forward_log_return_H = ln(reference_trade_price_H / anchor_trade_price)
```

Rules:

- Use natural logarithm (`math.log` or `numpy.log`).
- Parse `anchor_trade_price` and `reference_trade_price_H` from the
  Decimal-as-string source column to `Decimal` exactly, then cast
  the ratio to deterministic `float64` only at the log step.
- If `anchor_trade_price <= 0`:
  - `forward_log_return_H = null` for all H,
  - `forward_direction_H = null` for all H,
  - `label_invalid_price_flag = true`.
- If `reference_trade_price_H <= 0`:
  - that horizon's `forward_log_return_H = null`,
  - that horizon's `forward_direction_H = null`,
  - `label_invalid_price_flag = true`.
- If the horizon is censored:
  - that horizon's `forward_log_return_H = null` (regardless of
    `label_invalid_price_flag`).
- `forward_log_return_H` columns must never contain `NaN` or `inf`.
  Any case that would produce `NaN` or `inf` must instead be
  represented as a null with the appropriate flag set.
- Null is allowed only under explicit censoring or invalid-price
  conditions defined above.

Implementation contract (binding on Phase 4bj-C):

- the Decimal → float64 cast must occur **after** the ratio is
  formed in `Decimal`, not before;
- the natural-log step is allowed to lose precision below
  `float64` epsilon; this is acceptable for v001 because labels are
  descriptive, not strategy-grade;
- the future implementation must not switch to `log10`, `log2`, or
  a base-10 percentage formula without a separately authorized
  schema-amendment memo.

## 15. Finalized `forward_direction` policy

For every (row R, horizon H):

- `forward_direction_H` is derived **only** from
  `forward_log_return_H`.
- Values:
  - `+1` if `forward_log_return_H > 0`
  - `0` if `forward_log_return_H == 0`
  - `-1` if `forward_log_return_H < 0`
  - `null` if `forward_log_return_H` is null
- Threshold policy at v001: **strict sign threshold**, threshold =
  `0.0` log-return.
- **No deadband** at v001.
- **No bp threshold** at v001.
- **No threshold optimization** at v001 or in any future Phase 4bj-C
  implementation.
- **No evaluation-window fitting** at v001.
- **No cost-based threshold** at the label-schema level.

Rationale (recorded):

> The v001 direction labels are descriptive sign labels, not
> profitability labels and not strategy labels. They are not safe to
> read as "predicted direction"; they are the realized sign of the
> measured forward log return at the labeled horizon. A future
> deadband, bp-threshold, or cost-based threshold variant requires a
> separately authorized schema-amendment memo.

## 16. Finalized null / censoring policy

- **Keep all feature rows** in the label artefact (`row_count =
  1681098`).
- **Do not drop** right-edge rows.
- For each horizon `H` independently:
  - if `target_timestamp_ms > final_source_normalized_transact_time_ms`
    for the artefact's `utc_date`, set
    `horizon_censored_flag_H = true` and all that horizon's
    label columns (regression + classification + reference row +
    reference timestamp) to `null`.
- `label_any_censored_flag` = `true` if **any** horizon is censored
  for that row.
- If invalid price is encountered:
  - set affected label columns to `null`,
  - set `label_invalid_price_flag = true`.
- Invalid price must be unexpected for this artefact (the Phase 4bb-D
  raw gate confirmed all rows passed `validate_aggtrade_payload`
  with positive price and quantity; the Phase 4bd normalization
  preserves rows 1-for-1 in Decimal-as-string form). The future
  Phase 4bj-C / Phase 4bj-D phases must still record invalid-price
  counts in the label manifest and the structural QA report.
- **No forward-fill of censored labels** beyond the final source
  timestamp.
- **No cross-midnight / UTC-date boundary** for v001. The artefact
  represents BTCUSDT 2025-01-15 only; right-edge censoring inside
  this UTC day is expected for rows whose `feature_timestamp_ms +
  H_ms` exceeds the day's final normalized `transact_time_ms`.

## 17. Finalized dtype policy

- `row_index`: `int64`.
- `agg_trade_id`: `int64`.
- All timestamp columns (`feature_timestamp_ms`,
  `source_transact_time_ms`, `reference_timestamp_ms_*`): `int64`
  representing UTC milliseconds.
- Hashes, dataset IDs, dataset / schema versions, symbol,
  utc_date: `string`.
- `forward_log_return_*`: nullable `float64`.
- `forward_direction_*`: nullable `int8` with values `{-1, 0, 1}`.
- `reference_row_index_*`: nullable `int64`.
- `horizon_censored_flag_*`: non-nullable `bool`.
- `label_invalid_price_flag`: non-nullable `bool`.
- `label_any_censored_flag`: non-nullable `bool`.
- `label_config_hash`: `string`.
- **No NaN values** in any column (including float columns).
- **No inf values** in any column.
- **Null is allowed only** in the columns explicitly typed as
  nullable above and only under the censoring / invalid-price
  conditions defined in section 16.

## 18. Finalized lineage / identity policy

The lineage / identity columns must be present in **every** label
row (constant for the artefact's `(symbol, utc_date)` scope):

- `dataset_family` = `microstructure_labels_aggtrades_v001`
- `dataset_version` = `v001`
- `label_schema_version` = `v001`
- `source_feature_dataset_family` =
  `microstructure_features_aggtrades_v001`
- `source_feature_dataset_version` = `v001`
- `source_feature_manifest_sha256` =
  `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718`
- `source_feature_parquet_sha256` =
  `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`
- `source_feature_successor_state_sha256` =
  `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`
- `source_phase_4bi_b_gate_report_sha256` =
  `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988`
- `source_normalized_parquet_sha256` (recommended; included by
  default) =
  `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`
- `symbol` = `BTCUSDT`
- `utc_date` = `2025-01-15`

Per-row identity columns:

- `row_index`: matches feature parquet row by row.
- `agg_trade_id`: matches feature parquet row by row.
- `feature_timestamp_ms`: matches feature parquet
  `feature_timestamp_ms` row by row.
- `source_transact_time_ms`: matches feature parquet
  `source_transact_time_ms` row by row.

## 19. Finalized label manifest schema

The future label manifest, if later implemented by a separately
authorized Phase 4bj-C, must include at minimum:

| field | value |
|---|---|
| `dataset_family` | `microstructure_labels_aggtrades_v001` |
| `dataset_version` | `v001` |
| `label_schema_version` | `v001` |
| `source_feature_dataset_family` | `microstructure_features_aggtrades_v001` |
| `source_feature_dataset_version` | `v001` |
| `source_feature_manifest_sha256` | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| `source_feature_parquet_sha256` | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| `source_feature_successor_state_sha256` | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |
| `source_phase_4bi_b_gate_report_sha256` | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| `source_normalized_parquet_sha256` (recommended) | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| `symbol` | `BTCUSDT` |
| `utc_date` | `2025-01-15` |
| `row_count` | `1681098` |
| `label_list` | the eight finalized labels in canonical order |
| `support_column_list` | the 12 per-horizon support columns + 2 global support columns in canonical order |
| `horizon_list` | `["1s", "5s", "15s", "60s"]` |
| `horizon_ms_list` | `[1000, 5000, 15000, 60000]` |
| `nullable_tail_policy` | text description of section 16 |
| `reference_price_policy` | text description of section 13 |
| `direction_threshold_policy` | text description of section 15 |
| `label_config_hash` | deterministic SHA256 over canonical JSON of all schema-locking fields (see section 20) |
| `chronological_split_policy` | `not_yet_defined` |
| `governance_labels.labels` | `allowed_by_future_phase_only` |
| `governance_labels.targets` | `allowed_by_future_phase_only` |
| `governance_labels.ml` | `forbidden` |
| `governance_labels.strategy` | `forbidden` |
| `governance_labels.backtest` | `forbidden` |
| `governance_labels.acquisition` | `unauthorized` |
| `governance_labels.paper_shadow_live` | `forbidden` |
| `governance_labels.deployment` | `forbidden` |
| `governance_labels.exchange_write` | `forbidden` |
| `governance_labels.phase_id` | `4bj-C` (future) |
| `research_eligible` | `false` |
| `eligibility_gate_status` | `pending` |
| `code_commit_sha` | recorded by future Phase 4bj-C at implementation time |
| `created_at_unix_ms` | recorded by future Phase 4bj-C at implementation time |
| `invalid_price_row_count` | int (0 expected for the v001 artefact) |
| `censored_per_horizon` | object mapping horizon → row count |
| `files[]` | list of label-parquet file entries with sha256, byte size, row count |

The future label manifest must:

- be governed by the same Phase 4aw `MicrostructureManifest` model,
  unless a separately authorized memo amends that model;
- preserve the Phase 4aw `flip_research_eligible(...)` always-raises
  invariant — the manifest's `research_eligible` flag may only be
  flipped to `true` by a separately authorized successor phase, and
  this v001 schema does not authorize it.

## 20. Finalized `label_config_hash` policy

The future Phase 4bj-C implementation must compute a deterministic
`label_config_hash` as follows:

- Build a canonical-JSON object with **sorted keys** containing the
  following fields **and only these fields**:

  - `dataset_family`
  - `dataset_version`
  - `label_schema_version`
  - `label_list` (canonical order from section 11)
  - `support_column_list` (canonical order from section 10)
  - `horizon_list` (canonical order from section 12)
  - `horizon_ms_list` (canonical order from section 12)
  - `anchor_policy` (sectioned text from section 13)
  - `future_reference_policy` (sectioned text from section 13)
  - `direction_threshold_policy` (sectioned text from section 15)
  - `null_censoring_policy` (sectioned text from section 16)
  - `dtype_policy` (sectioned text from section 17)
  - `source_feature_manifest_sha256` (section 18)
  - `source_feature_parquet_sha256` (section 18)
  - `source_feature_successor_state_sha256` (section 18)
  - `source_phase_4bi_b_gate_report_sha256` (section 18)

- Compute `sha256(canonical_json(config_object))`.
- Record the result as:
  - the value of the `label_config_hash` column in every label-
    parquet row (constant across the artefact), and
  - the value of `label_config_hash` in the label manifest.
- The hash must be deterministic across reruns. Reordering keys,
  re-spacing JSON, or altering any of the above fields must change
  the hash. Any future schema-amendment memo must record the new
  hash explicitly.

## 21. Finalized future label output paths

Proposed and finalized for future implementation only, **not created
now**:

- label parquet:
  `data/microstructure/labels/microstructure_labels_aggtrades_v001/`
  `BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet`
- label parquet paired sidecar:
  same path with `.sha256` suffix
- label manifest:
  `data/microstructure/manifests/`
  `microstructure_labels_aggtrades_v001__v001.json`
- label manifest paired sidecar:
  same path with `.sha256` suffix
- future label gate-report directory:
  `data/microstructure/gate-reports/labels/`
- future label successor-state directory:
  `data/microstructure/successor-state/` (sibling label successor-
  state files only; feature successor-state files must not be
  modified)

The entire `data/microstructure/` tree remains gitignored under
`.gitignore:85`, so any future Phase 4bj-C-style implementation must
write only inside that gitignored namespace and must not produce
tracked files under `data/microstructure/`.

Phase 4bj-B does not create any of the above paths.

## 22. Finalized validation and QA requirements

A future Phase 4bj-D structural QA memo must verify the label
artefact against this section verbatim:

1. label parquet exists at the canonical path;
2. label parquet sidecar exists and matches recomputed SHA256;
3. label manifest exists at the canonical path;
4. label manifest sidecar exists and matches recomputed SHA256;
5. label-parquet `row_count` equals feature-parquet `row_count`
   (1 681 098);
6. label-parquet `row_index` parity with feature parquet row by row;
7. label-parquet `agg_trade_id` parity with feature parquet row by
   row;
8. label-parquet `feature_timestamp_ms` parity with feature parquet
   row by row;
9. label-parquet `source_transact_time_ms` parity with feature
   parquet row by row;
10. lineage hashes (`source_feature_manifest_sha256`,
    `source_feature_parquet_sha256`,
    `source_feature_successor_state_sha256`,
    `source_phase_4bi_b_gate_report_sha256`) match expected values;
11. `label_config_hash` is constant across all label rows;
12. `label_config_hash` matches the label-manifest
    `label_config_hash`;
13. `forward_log_return_H` values reproduce the section-14 formula
    on a predeclared sample of rows;
14. `reference_row_index_H` and `reference_timestamp_ms_H` reproduce
    the section-13 future-reference policy on the same sample;
15. no `NaN` or `inf` in any float column;
16. all `forward_direction_H` values are in `{-1, 0, 1, null}`;
17. horizon-censored flags match the predicate
    `target_timestamp_ms > final_source_normalized_transact_time_ms`
    for the artefact's `utc_date`;
18. support columns (`reference_row_index_H`,
    `reference_timestamp_ms_H`, `horizon_censored_flag_H`,
    `label_invalid_price_flag`, `label_any_censored_flag`) are not
    interpreted as signals;
19. upstream artefact SHAs remain byte-identical pre/post run;
20. no `data/microstructure/` file outside the gitignored label
    namespace was modified.

A future Phase 4bj-E label-family eligibility gate must:

- be offline;
- be deterministic;
- write exactly one local gitignored label gate report and paired
  sidecar under `data/microstructure/gate-reports/labels/`;
- **never** flip the label manifest's `research_eligible` flag to
  `true`;
- **never** transition the label manifest's
  `eligibility_gate_status` to `pass` on the actual manifest
  (gate-report-level recommendation only, mirroring the Phase 4bf /
  4bi-B precedent);
- not authorize ML, strategy, backtest, or acquisition;
- preserve the Phase 4al refined no-rescue rule and the Phase 4ak
  M0 twelve-clause gate.

## 23. Finalized forbidden outputs

A future Phase 4bj-C implementation must **not** create:

- any column named anything that contains the substring `pnl`,
  `profit`, `loss`, `mfe`, `mae`, `r_multiple`, `equity`,
  `position`, `alpha`, `edge`, `prediction`, `model`, `score`,
  `decision`, `strategy`, `entry`, `exit`, `signal`, `target`,
  `barrier`, or `liquidation` (forbidden-substring detector applied
  per Phase 4bh-A / Phase 4bh-B precedent);
- any column derived from mark price, index price, bid / ask, book
  data, order-book imbalance, or external data;
- any column that uses future feature values to alter feature
  semantics;
- any centered-window derivation;
- any ML model artefact;
- any backtest artefact;
- any strategy logic;
- any paper / shadow / live runtime artefact;
- any modification to the feature parquet, feature manifest,
  Phase 4bi-D successor-state, Phase 4bi-B gate report, normalized
  parquet, derived manifest, raw manifest, raw zip, Phase 4bb-D gate
  report, Phase 4bf gate report, or Phase 4bg-B successor-state;
- any flip of `research_eligible` on the raw manifest, derived
  manifest, or feature manifest;
- any transition of `eligibility_gate_status` on the raw manifest,
  derived manifest, or feature manifest.

## 24. Finalized chronological split policy

`chronological_split_policy = not_yet_defined` at v001.

- No train / validation / test split is finalized by Phase 4bj-B.
- A future split memo must be separate and must occur before any
  ML training or strategy evaluation.
- Any future split policy must be **chronological only**, predeclared
  before evaluation, locked in the label manifest, and lineage-bound
  to the feature parquet and the Phase 4bi-D successor-state.

## 25. Finalized no-rescue / M0 policy

The Phase 4al refined no-rescue rule applies verbatim:

> No future memo, no future label, no future evaluation, and no
> future ML training may, in effect, restate or rescue R2 / F1 /
> D1-A / V2 / G1 / C1 / 5m-thread rules under a different name.

The Phase 4ak M0 twelve-clause gate applies prospectively:

> Stage-5 admissibility is upstream of M0. M0 still applies to any
> future hypothesis, label, target, strategy, or backtest. Stage-5
> admissibility does not bypass M0.

Operational consequences for v001:

- labels are **not** signals;
- labels are **not** strategies;
- forward returns are **not** strategy returns;
- direction accuracy is **not** profitability;
- MFE / MAE / R-multiple labels remain forbidden at v001;
- cost-adjusted expectancy requires a later separately authorized
  strategy / backtest phase that applies §11.6 = 8 bps HIGH per
  side verbatim;
- a future Phase 4bj-C / Phase 4bj-D / Phase 4bj-E / Phase 4bj-F /
  Phase 4bj-G memo or implementation must clear M0 for any
  interpretation, decision, or admissibility transition it proposes;
- no Phase 4bj-* phase may interpret Phase 4bi-D Stage-5
  admissibility as Stage-6 research-eligibility or as strategy
  authorization;
- the actual raw manifest, derived manifest, and feature manifest
  must remain `research_eligible: false / eligibility_gate_status:
  pending` for the lifetime of v001 unless a separately authorized
  phase changes that explicitly under M0 and no-rescue.

## 26. Future implementation acceptance criteria (Phase 4bj-C)

A future Phase 4bj-C label-implementation phase may be acceptable
only if **all** of the following are satisfied:

1. it is **separately authorized** by an explicit operator decision;
2. it implements **exactly** this Phase 4bj-B schema (column names,
   horizons, formulas, dtypes, lineage, support columns, manifest
   fields, paths) without amendment;
3. it writes only **gitignored** label artefacts under
   `data/microstructure/labels/`,
   `data/microstructure/manifests/microstructure_labels_aggtrades_v001*`,
   `data/microstructure/gate-reports/labels/`, and
   `data/microstructure/successor-state/` (the latter only for
   sibling label successor-states; feature successor-states must
   not be touched);
4. it refuses to overwrite any existing local artefact under the
   same names;
5. it preserves the feature parquet SHA byte-identically;
6. it preserves the feature manifest byte-identically (no field
   flip; no reordering; no whitespace change);
7. it preserves the Phase 4bi-D successor-state artefact byte-
   identically;
8. it preserves the Phase 4bi-B gate report byte-identically;
9. it preserves the Phase 4bf gate report byte-identically;
10. it preserves the Phase 4bb-D raw gate report byte-identically;
11. it preserves the original derived manifest byte-identically;
12. it preserves the raw manifest byte-identically;
13. it creates **no** ML models;
14. it creates **no** strategy signals;
15. it creates **no** backtests;
16. it creates **no** column whose name matches any forbidden-
    substring listed in section 23;
17. it keeps the label manifest `research_eligible: false /
    eligibility_gate_status: pending`;
18. it records `label_config_hash` per section 20;
19. it records horizon-censoring counts in the label manifest;
20. it records invalid-price row count in the label manifest
    (expected `0` for this artefact);
21. it passes label-specific tests, microstructure tests, ruff,
    mypy, and whole-repo pytest with only the two known pre-
    existing simulation failures
    (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
    and `::test_real_2026_03_ethusdt`,
    both `KeyError: 'trade_count'` in
    `src/prometheus/research/data/storage.py:232`);
22. it produces a Phase 4bj-C main memo + closeout report under
    `docs/00-meta/implementation-reports/` recording the same
    discipline as Phase 4bh / Phase 4bi-B / Phase 4bi-D / Phase
    4bj-A;
23. it does not authorize Phase 4bj-D, Phase 4bj-E, Phase 4bj-F,
    Phase 4bj-G, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4
    canonical, paper / shadow / live, exchange-write, production
    keys, authenticated APIs, private endpoints, user stream, live
    WebSocket implementation, MCP, Graphify, `.mcp.json`, or
    credentials.

## 27. Future QA / gate sequence

Phase 4bj-B recommends the following future Phase 4bj-* sequence
(none of which is authorized here):

- **Phase 4bj-C** — Label Implementation + Local Label Artefact
  Generation. Implements exactly this Phase 4bj-B schema; produces
  label parquet, label manifest, paired sidecars locally under the
  gitignored namespace.
- **Phase 4bj-D** — Label Artefact Structural QA Memo (analysis-and-
  docs only; read-only). Verifies the label artefact against
  section 22.
- **Phase 4bj-E** — Label-Family Eligibility Gate Design +
  Implementation + Execution. Mirrors Phase 4bi-B for the label
  family; emits a label gate report; never flips the label
  manifest's `research_eligible` to `true`.
- **Phase 4bj-F** — Label-Family Research / ML-Use Decision Memo
  (docs-only). Decides whether the label family is admissible in
  principle for research / ML use at policy level.
- **Phase 4bj-G** — Label-Family Successor-State Recording (docs +
  local gitignored output). Mirrors Phase 4bi-D; records the policy
  decision in a sibling successor-state artefact while preserving
  the label manifest byte-identically.

No phase in the above sequence is authorized by Phase 4bj-B.

## 28. What this phase proves

Phase 4bj-B proves only the following:

- a fully specified, leakage-safe, deterministic v001 label schema
  exists at docs / policy level for the future label family
  `microstructure_labels_aggtrades_v001`;
- the schema preserves all upstream artefact SHAs and the byte-
  immutability discipline of Phase 4bh / Phase 4bi-B / Phase 4bi-D /
  Phase 4bj-A;
- the schema is compatible with the Phase 4aw `MicrostructureManifest`
  model and with the Phase 4aw `flip_research_eligible(...)` always-
  raises invariant;
- a future Phase 4bj-C implementation is **possible** if separately
  authorized, and **bounded** by sections 8–26 of this memo;
- the no-rescue, no-leakage, no-shuffling, cost-aware, M0-bound, and
  Phase 4al-bound interpretation of labels is locked at v001.

## 29. What this phase does not prove

Phase 4bj-B does **not** prove:

- that any v001 label has predictive value;
- that forward log returns at any v001 horizon are forecastable;
- that direction classification at any v001 horizon is forecastable;
- that any label-based ML model would generalize;
- that any label-based strategy would be edge-positive;
- that the v001 label family is the right one;
- that mark-price stop-domain forensics is admissible;
- that aggTrades-domain barrier labels are admissible at v001;
- that ETHUSDT or any other symbol is admissible at v001;
- that multi-date label coverage is admissible at v001;
- that ML training is authorized;
- that strategy work is authorized;
- that backtest work is authorized;
- that paper / shadow / live work is authorized;
- that Phase 4bj-C or any successor phase is authorized.

## 30. Preserved boundaries

Phase 4bj-B preserves every retained verdict and project lock
verbatim:

- H0 → FRAMEWORK ANCHOR;
- R3 → BASELINE-OF-RECORD;
- R1a / R1b-narrow → RETAINED — NON-LEADING;
- R2 → FAILED — §11.6;
- F1 → HARD REJECT;
- D1-A → MECHANISM PASS / FRAMEWORK FAIL — other;
- 5m thread → OPERATIONALLY CLOSED per Phase 3t;
- V2 → HARD REJECT — terminal for V2 first-spec;
- G1 → HARD REJECT — terminal for G1 first-spec;
- C1 → HARD REJECT — terminal for C1 first-spec;
- §11.6 = 8 bps per side; round-trip = 16 bps;
- §1.7.3 = 0.25 % / 2× / one-position / mark-price stops;
- Phase 3p §4.7 strict integrity gate;
- Phase 3r §8 mark-price gap governance;
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance;
- Phase 4j §11 metrics OI-subset partial-eligibility rule;
- Phase 4k V2 backtest-plan methodology;
- Phase 4p G1 strategy-spec memo;
- Phase 4q G1 backtest-plan methodology;
- Phase 4v C1 strategy-spec memo;
- Phase 4w C1 backtest-plan methodology;
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-
  down families list + memo template;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy;
- Phase 4am §11.A audit findings;
- Phase 4an V1-arc inventory result;
- Phase 4ao harmonization result;
- Phase 4ap V1-arc forensic plan;
- Phase 4aq V1-arc forensic computation;
- Phase 4ar V1-arc forensic interpretation;
- Phase 4as mechanism-map memo;
- Phase 4at availability / capture-feasibility memo;
- Phase 4au capture-design memo;
- Phase 4av implementation-plan memo;
- Phase 4aw scaffold result;
- Phase 4ax aggTrades-only collector skeleton;
- Phase 4ay aggTrades archive acquisition authorization memo;
- Phase 4az aggTrades archive acquisition (BTCUSDT 2025-01-15);
- Phase 4ba aggTrades dataset eligibility-gate review;
- Phase 4bb-A structural QA;
- Phase 4bb-B execution-plan;
- Phase 4bb-C primitive implementation;
- Phase 4bb-D gate-execution PASS;
- Phase 4bb-E successor-state policy memo;
- Phase 4bc normalization design;
- Phase 4bd-A normalization implementation plan;
- Phase 4bd Stage-0 normalization implementation;
- Phase 4be structural QA;
- Phase 4bf-A derived-family gate design;
- Phase 4bf derived-family gate execution PASS;
- Phase 4bg-A derived-family research-eligibility decision;
- Phase 4bg-B derived-family research-eligibility successor-state
  recording;
- Phase 4bh-A feature-boundary design;
- Phase 4bh-B feature schema finalization;
- Phase 4bh feature-computation implementation;
- Phase 4bi-A feature artefact structural QA;
- Phase 4bi-B feature-family eligibility gate PASS;
- Phase 4bi-C feature-family research-use / ML-use admissibility
  decision (Outcome 1 / Decision form 1);
- Phase 4bi-D feature-family successor-state recording (Outcome 1);
- Phase 4bj-A label boundary / target definition memo (Outcome 1) —
  all preserved verbatim.

## 31. Recommended future options

- **Primary:** remain paused.
- **Conditional next (NOT authorized):** Phase 4bj-C — Label
  Implementation + Local Label Artefact Generation (code + docs +
  local gitignored output), separately authorized.
- **Conditional cleanup (NOT authorized):** Phase 4bb-F — Gate
  Report Output Path Hygiene.
- **Conditional raw policy marker (NOT authorized):** Phase 4bb-G —
  Raw Manifest Successor-State Recording.

No successor phase is authorized.

## 32. Closeout / lock preservation

Phase 4bj-B is docs-only and text-only. No code, tests, scripts,
configs, manifests, gate reports, successor-state artefacts, feature
parquet, normalized parquet, raw zip, or data files were created or
modified outside the two new docs files and the narrow
`current-project-state.md` update. Whole-repo quality gates remain
clean. No retained verdicts were revised. No project locks changed.
M0 governance and the post-null cooldown rule remain binding
prospective governance for any future research lane.

**Recommended state:** remain paused.

**No next phase authorized.**
