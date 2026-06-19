# Phase 4bn-X — Label-Layer Eligibility Gate

## 1. Purpose

Phase 4bn-X implements and runs a bounded, **read-only** label-layer
eligibility gate over the Phase 4bn-W local, non-eligible, gitignored
**pre-v002 BTCUSDT aggTrades label segment** (Binance USDⓈ-M futures;
2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates; 400,001,695 label rows).

The gate proves the local label segment is structurally complete, internally
consistent, manifest-consistent, schema-consistent, hash-consistent,
lineage-consistent, censoring-consistent, predecessor-consistent, and
governance-consistent, and records the result in exactly one local gitignored
label-layer gate report + canonical sidecar. It prepares the label layer for a
later, separately-authorized chronological-split / holdout-policy memo and a
future ML-baseline admissibility review.

A passing gate **authorizes nothing**: it does not flip `research_eligible`,
does not transition `eligibility_gate_status`, runs no ML / diagnostics /
strategy / PnL / backtests, defines no chronological split policy, and
authorizes no successor.

## 2. Authority and repository state

Phase 4bn-X was separately authorized by the operator following the Phase
4bn-W decision `RECOMMEND_AUTHORIZE_LABEL_LAYER_ELIGIBILITY_GATE`.

- **Branch:** `phase-4bn-x/label-layer-eligibility-gate`.
- **Base:** `main` at `5bcae53ee843759a6c81c14d71a66dc241023e31`
  (`docs(phase-4bn-w): finalize merge closeout shas`).
- Pre-branch `main == origin/main == HEAD == 5bcae53…` verified in sync.
- Predecessor chain confirmed present on main: Phase 4bn-W SHA-finalization
  `5bcae53`, merge-closeout `1f2323f`, merge `1353525`, branch `098b274`, and
  Phase 4bn-V finalization `e53652a`.
- GitHub remote: `https://github.com/jpedrocY/Prometheus.git`.
- Only expected untracked transient at start: `.claude/scheduled_tasks.lock`.
- `data/microstructure/` and `data/research/` confirmed gitignored
  (`.gitignore:85` / `.gitignore:88`).

## 3. Phase type and strict scope

**Phase type:** code + tests + docs + local gitignored read-only gate-report
generation phase. **Tier:** Tier 1 — Full Phase per
`phase-risk-tiering-standard` §3 (reads local label artefacts and predecessor
manifests/gate reports; validates a newly generated label segment; adjacent to
future chronological-split / ML-baseline admissibility work).

This phase **must not** and **did not**: mutate labels / features / normalized
/ raw data / manifests / predecessor gate reports / published `__v002`
artefacts / eligibility state; commit any `data/microstructure` or
`data/research` artefact; create `data/research` outputs; run ML / diagnostics
/ strategy / signals / PnL / backtests; flip eligibility; transition
`eligibility_gate_status` or `chronological_split_policy`; authorize any
successor.

## 4. Evidence base and input boundary

Committed process docs and predecessor reports read read-only:
`current-project-state.md`; the `merge-closeout-standard`,
`phase-risk-tiering-standard`, `phase-workflow-standard`,
`phase-prompt-template`, and `operator-report-standard` process docs; the
Phase 4bn-W / 4bn-V / 4bn-U / 4bn-T / 4bn-S / 4bn-R / 4bn-P / 4bn-O / 4bn-L
implementation reports, memos, and closeouts; and the `04-data` /
`08-architecture` data/architecture docs.

Committed tooling read read-only: `labels_schema_v002.py`,
`labels_manifest_v002.py`, `labels_compute_v002.py`, `labels_io.py`,
`labels_io_v002.py`, `labels_validation.py`, `label_gate.py`,
`multiday_label_gate.py`, `multiday_label_gate_v002.py`, `normalize_io.py`, and
the Phase 4bn-W / 4bn-T / 4bn-P gate/compute scripts and tests.

Allowed local data reads (only): the Phase 4bn-W label segment manifest +
sidecar; the 275 label Parquets + 275 sidecars; the Phase 4bn-S feature segment
manifest + sidecar; the Phase 4bn-T feature-layer gate report; the Phase 4bn-O
normalized segment manifest + sidecar; the Phase 4bn-P normalized-layer gate
report; the Phase 4bn raw segment manifest. **No** published `__v002` Parquet
content, **no** v002 terminal raw/normalized/feature/label window, **no**
sealed-test dates, and **no** `data/research` artefact were read.

## 5. Phase 4bn-W label segment carried forward

The gate validates the Phase 4bn-W segment exactly as recorded:

- output directory
  `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w/BTCUSDT/<YYYY>/<MM>/`;
- manifest
  `…/manifests/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w.json`
  (SHA256 `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`)
  + canonical sidecar
  (SHA256 `636a4c1a0159364e7d67f502dda48664f18fc16545c993935e6429ccdf868239`);
- 275 label Parquet + 275 sidecars; total rows **400,001,695**; footprint
  **15,654,082,679 B** (parquet + sidecar bytes);
- `label_config_hash =
  b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`;
- `envelope_terminal_unix_ms = 1733011199331`, `envelope_terminal_utc_date =
  2024-11-30`;
- per-horizon censored counts 1s=3 / 5s=20 / 15s=42 / 60s=216; invalid-price
  rows 0;
- posture `research_eligible=false`, `eligibility_gate_status=pending`,
  `no_successor_authorization=true`, `ml_use/diagnostics_use/strategy_use/
  backtest_use=forbidden`, `chronological_split_policy=not_yet_defined`,
  `v002_terminal_window_mode=by_reference`, `sealed_test_split_touched=false`,
  `test_rows_loaded=0`.

## 6. Phase 4bn-V selected conventions carried forward

The gate enforces the Phase 4bn-V label manifest/versioning conventions:
segment-scoped manifest naming distinct from published `__v002`;
`dataset_version=v002` / `label_schema_version=v001` /
`segment_label=pre_v002_segment`; the **segment-scoped `label_config_hash`**
builder (re-specified future-reference envelope clause + Phase 4bn-T / 4bn-P
gate witnesses + `feature_config_hash=0726b41d…`, never the published
`819cfa7a…`); and the **lineage re-mapping** of the two terminal-specific
lineage columns. The gate re-implements the segment-scoped hash builder inline
(reading the locked policy constants from `labels_schema_v002`) and reproduces
`b3bd5d2b…` from the manifest's recorded source SHAs.

## 7. Phase 4bn-S / 4bn-T feature predecessor carried forward

- Feature segment manifest SHA256
  `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52` + sidecar
  `f2ca2f48a5ac8ccfb892d0460cdfbbbb891451b9d94135adb3bff0936c8592e5`; feature
  rows 400,001,695; `feature_config_hash=0726b41d…`; posture
  `research_eligible=false` / `eligibility_gate_status=pending`.
- Feature-layer gate report
  `…/gate-reports/features/…__phase-4bn-t__1780674917156__e647435c81d7.json`
  SHA256 `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08`,
  verdict
  `FEATURE_LAYER_GATE_PASSED__LOCAL_FEATURE_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`,
  27/27 PASS.

## 8. Phase 4bn-O / 4bn-P normalized predecessor carried forward

- Normalized segment manifest SHA256
  `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa` + sidecar
  `5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402`;
  normalized rows 400,001,695; posture `research_eligible=false` /
  `eligibility_gate_status=pending`.
- Normalized-layer gate report SHA256
  `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134`, verdict
  `NORMALIZED_LAYER_GATE_PASSED__LOCAL_NORMALIZED_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`,
  25/25 PASS.
- Raw segment manifest SHA256
  `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`.

## 9. Gate contract

The gate is network-free (imports no networking library; uses no credentials,
`.env`, `.mcp.json`, MCP, or Graphify), refuses to overwrite a finalised gate
report or sidecar, uses atomic write-then-rename, writes a canonical two-space
`.sha256` sidecar, writes only under `data/microstructure/gate-reports/labels/`
(validated by `_assert_under_gate_reports_labels`, failing closed on any path
outside that subtree), and fails closed on missing/mismatched sidecars, missing
predecessor PASS, non-eligible-posture violations, governance violations, any
schema/hash/lineage/censoring mismatch, and any attempted read of v002-terminal
or sealed-test dates (the date guard rejects `≥ 2024-12-01` and the sealed-test
window). Temporary files are cleaned on success and failure.

## 10. Gate wrapper implementation

`scripts/phase4bn_x_validate_label_pre_v002_gate.py` follows the Phase 4bn-T /
4bn-P gate structure: locked identity/expectation constants; a `CheckResult` /
`GateResult` model; a `_check_manifest_contract` contract validator; a
**full per-file scan** (`_deep_scan_label_file`); a `_check_predecessors`
integrity validator; and an atomic, path-guarded, refuse-overwrite report
writer. Unlike the feature/normalized gates, **no check is sampled** — every
one of the 275 Parquets is fully scanned. The wrapper reuses only the locked
generic SHA/sidecar/path primitives from `normalize_io` and the locked
`LABEL_SCHEMA_V002` / label-policy constants from `labels_schema_v002`; it adds
no `src/prometheus` change.

## 11. Manifest and sidecar validation

The gate verifies the manifest SHA256 == `69746c88…b161`, the sidecar exists,
is canonical two-space form (`<sha>  <basename>\n`, no BOM/CR/extra lines), its
recorded SHA equals the manifest SHA, and the sidecar file's own SHA256 ==
`636a4c1a…8239`. It then validates the required-field set, identity/scope
fields, the 40/8/14/17 column-count fields and `schema_column_list ==
LABEL_SCHEMA_V002`, the window/footprint/row totals, the hash/envelope/censoring
manifest fields, the predecessor lineage SHAs + posture, the
`lineage_column_reinterpretation` binding, the non-eligible / governance /
non-authorization / v002-terminal / sealed / published-`__v002`-by-reference /
storage postures, the forbidden field-name scan (declaration subtrees skipped),
and the segment-scoped `label_config_hash` recomputation.

## 12. Label Parquet and sidecar validation

For every date in the manifest inventory the gate: resolves the Parquet +
sidecar paths under the segment family directory; validates the path layout +
`BTCUSDT-labels-aggtrades-<YYYY-MM-DD>.parquet` basename and rejects any path
containing the published `__v002` directory part or `v003`; streams the Parquet
SHA256 and compares to the sidecar and the manifest `per_day_outputs` entry;
accumulates the on-disk size; validates the sidecar canonical body and SHA; and
performs the full per-row scan. The recomputed totals (275 Parquet + 275
sidecars; 400,001,695 rows; 15,654,082,679 B) must match the manifest and the
locked expectations exactly.

## 13. Schema and forbidden-column validation

Every Parquet's column names must equal `LABEL_SCHEMA_V002` (40 columns, exact
canonical order) — this rejects any missing or extra column. Every column name
is checked against the locked 21-token forbidden-substring guard
(`FORBIDDEN_LABEL_COLUMN_SUBSTRINGS_V002`: pnl/profit/loss/mfe/mae/r_multiple/
equity/position/alpha/edge/prediction/model/score/decision/strategy/entry/exit/
signal/target/barrier/liquidation). A schema or forbidden-column violation in
any file fails the gate.

## 14. label_config_hash recomputation

The gate re-implements the segment-scoped builder inline (mirroring Phase
4bn-W's `build_label_config_hash_v002_pre_v002_segment`): it preserves the
locked anchor / direction / null-censoring / dtype / schema / horizon / lineage
policy fields, re-specifies the future-reference envelope clause to the pre-v002
segment terminal, binds the Phase 4bn-T feature-layer gate and Phase 4bn-P
normalized-layer gate witnesses, binds `feature_config_hash=0726b41d…` (and
rejects the published `819cfa7a…`), and adds the `pre_v002_segment`
discriminator. Recomputing from the manifest's recorded source SHAs reproduces
`b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970` exactly, and
that constant is verified on **every row of every file** (exhaustive constant
check: zero nulls, every value equal).

## 15. Lineage re-mapping validation

The constant lineage/identity columns are verified exhaustively across all 275
files: `dataset_family`, `dataset_version`, `label_schema_version`, `symbol`,
`source_feature_manifest_sha256` (`4881eb87…`),
`source_phase_4bm_j_gate_report_sha256` re-mapped to the Phase 4bn-T gate
(`db731d1b…`), `source_feature_successor_state_sha256` re-mapped to the Phase
4bn-P gate (`3452fd9d…`), `source_normalized_manifest_sha256` (`0e96ae37…`),
`source_raw_manifest_sha256` (`1659e6da…`), and `utc_date` equal to each
partition date. The manifest `lineage_column_reinterpretation` block is checked
to bind the same two gate SHAs.

## 16. Envelope-terminal and censoring validation

For every row of every file the gate recomputes, per horizon H ∈ {1s,5s,15s,60s}
with offset H_ms: `target = feature_timestamp_ms + H_ms`; `expected_censored =
target > 1733011199331`. It asserts `horizon_censored_flag_H ==
expected_censored`; that `reference_timestamp_ms_H` is null iff censored and,
when present, `≤ target` and `≤ envelope_terminal`; that `forward_log_return_H`
and `forward_direction_H` are null iff (censored or invalid-price) and, when
present, `forward_direction_H ∈ {-1,0,1}`; that `label_any_censored_flag` equals
the row-wise OR of the four horizon flags; that `row_index == arange(n)` and
`feature_timestamp_ms == source_transact_time_ms` with no anchor past the
terminal. Recomputed per-horizon censored counts (1s=3 / 5s=20 / 15s=42 /
60s=216), per-day counts vs the inventory, the invalid-price count (0), and the
recomputed terminal (`1733011199331`, UTC date 2024-11-30) all match exactly.
No reference timestamp exceeds the envelope terminal.

## 17. Predecessor integrity validation

The gate re-hashes the Phase 4bn-S feature manifest + sidecar (and checks
non-eligible/pending + `feature_config_hash`), verifies the Phase 4bn-T
feature-layer gate report SHA + verdict + 27/27 PASS, re-hashes the Phase 4bn-O
normalized manifest + sidecar (non-eligible/pending), verifies the Phase 4bn-P
normalized-layer gate report SHA + verdict + 25/25 PASS, and re-hashes the raw
segment manifest. All predecessor files are read read-only; none was mutated.

## 18. Non-eligible posture validation

The manifest's posture is validated and the gate report records it verbatim:
`research_eligible=false`, `eligibility_gate_status=pending`,
`no_successor_authorization=true`, `ml_use/diagnostics_use/strategy_use/
backtest_use=forbidden`, governance labels forbidden, all
`non_authorization_flags` false, `v002_terminal_window_mode=by_reference`,
`existing_v002_terminal_window.read=false` and
`feature_normalized_raw_dates_read=false`, `sealed_test_split_touched=false`,
`test_holdout_touched=false`, `test_rows_loaded=0`, the published label
`__v002` reference unread / unmutated / path-disjoint, and
`chronological_split_policy=not_yet_defined`.

## 19. Boundary confirmations

No acquisition, endpoint call, archive download, or HEAD preflight; no raw /
normalized / feature / label execution or gate rerun; no ML / diagnostics /
strategy / signals / PnL / backtests; no eligibility flip or
`eligibility_gate_status` / `chronological_split_policy` transition; no
published `__v002` mutation; no v002-terminal or sealed-test read
(`test_rows_loaded=0`); no database, no Parquet compaction, no v003; no
`data/research` output; no `data/microstructure` or `data/research` commit; no
paper / shadow / live / exchange-write / credentials / MCP / Graphify work. The
Phase 4aw `flip_research_eligible(...)` always-raises invariant was never
invoked.

## 20. Test coverage

`tests/research/microstructure/test_phase4bn_x_label_layer_gate.py` — 48
offline tests using only temp dirs and small synthetic 40-column
`LABEL_SCHEMA_V002` Parquets with correctly computed censoring. Covered:
network-free / no-forbidden-imports / no-credential-token static scans; gate
report path construction + rejection of unsafe paths + canonical sidecar +
refuse-overwrite; manifest required-field / forbidden-field / non-eligible /
governance / non-authorization / published-`__v002`-read / v002-terminal-read /
sealed / test_rows_loaded / chronological-split-policy posture rejections;
lineage-remap rejection; `label_config_hash` recompute determinism + mismatch +
published-`819cfa7a…` rejection; date-window guard; full-scan failures (schema
drop, forbidden column, censor-flag flip, reference-past-terminal, direction
domain, any-censored OR, invalid-price flag); per-file hash / missing-sidecar
failures; predecessor manifest-SHA / gate-not-PASS / eligible-source failures;
output-confined-to-gate-reports/labels + no-`data/research` assertion; and the
end-to-end PASS path. All 48 pass.

## 21. Real gate execution

The gate was run once over the real local Phase 4bn-W segment:

```text
[Phase 4bn-X] LABEL_LAYER_GATE_PASSED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED
  overall=pass; parquets=275; sidecars=275; rows=400001695;
  footprint=15654082679 B; censored={'1s':3,'5s':20,'15s':42,'60s':216};
  invalid_price=0; runtime=205.6s
```

40/40 checks PASS. Runtime 205.6 s. The run read the manifest + sidecar, all
275 Parquets + 275 sidecars (full per-row scan), and the predecessor manifests
/ gate reports for integrity; it recomputed file hashes, row counts, footprint,
per-horizon censored counts, invalid-price count, the envelope terminal, and the
segment `label_config_hash`; it wrote one gate report + sidecar; it mutated no
input artefact; it read no v002-terminal or sealed-test data; it ran no ML /
diagnostics / strategy / backtests.

## 22. Local gitignored gate report

- Report:
  `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w__phase-4bn-x__1781897304431__5bcae53ee843.json`
- Report SHA256:
  `ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984`
- Sidecar SHA256:
  `68dd5b5709bb523003ed183ac776e95ad1c82a40deb65e3cda51b2e10e51997c`

The report records `phase_id=phase-4bn-x`; the input manifest path + SHA +
sidecar SHA; the input directory + Parquet/sidecar counts; recomputed total
rows / footprint / per-horizon censored counts / invalid-price count /
`label_config_hash` / envelope terminal; the 40 checks with PASS/FAIL status;
predecessor manifests/gate SHAs + verdicts; runtime; `segment_non_eligible:
true`; `research_eligible_after: false`; `eligibility_gate_status_after:
pending`; `no_successor_authorization: true`; the explicit non-authorizations
list; `v002_terminal_window_read: false`; `sealed_test_split_touched: false`;
`published_v002_label_mutated: false` / `_read: false`. Both files are gitignored
(`.gitignore:85`) and uncommitted.

## 23. Validation

- `ruff check` on the runner + test → all checks passed.
- `pytest tests/research/microstructure/test_phase4bn_x_label_layer_gate.py` →
  48 passed.
- `pytest` predecessor suites (`test_phase4bn_w_label_pre_v002.py`,
  `test_phase4bn_t_feature_layer_gate.py`, `test_phase4bn_s_feature_pre_v002.py`,
  `test_phase4bn_p_normalized_layer_gate.py`,
  `test_phase4bn_o_normalization_pre_v002.py`) → 155 passed (203 total with the
  new module).
- `mypy src/prometheus` → 96 pre-existing errors in 12 unrelated modules; Phase
  4bn-X added no `src/prometheus` change (the wrapper lives under `scripts/`).
- `git diff --check` clean.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` shows only the five tracked Phase 4bn-X files plus the
  expected untracked `.claude/scheduled_tasks.lock`; no `data/microstructure/`
  or `data/research/` artefact staged.

## 24. Result state

`LABEL_LAYER_GATE_PASSED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`
(40/40 checks PASS).

## 25. Decision

`RECOMMEND_AUTHORIZE_CHRONOLOGICAL_SPLIT_AND_HOLDOUT_POLICY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

## 26. Recommended state and successor options

**Recommended state: remain paused.** Acceptable operator options: remain
paused; request a merge prompt for Phase 4bn-X; separately authorize a docs-only
chronological split / holdout policy memo (preferred next step before any ML);
separately authorize an ML-baseline readiness memo (only after a split policy
exists); separately authorize a docs-only holdout-boundary memo (only if a
future scope touches the v002 terminal or sealed-test dates); separately
authorize a source-policy documentation memo; separately authorize a process-doc
`D:` path-string update; or reject further ML-baseline successors and close the
ML arc. No successor is authorized from inside Phase 4bn-X.

## 27. Explicit non-authorizations

A passing label-layer gate does not make the dataset research-eligible and
authorizes no chronological split policy, labels-for-ML use, ML, model training,
scoring, predictions, diagnostics, strategy, signals, PnL, backtests, research
matrices, storage migration, database, Parquet compaction, v003, paper / shadow
/ live, exchange-write, credentials, MCP, Graphify, or any successor. The
published `__v002` label family remains by-reference only and unmutated; the
v002 terminal raw/normalized/feature/label window and the sealed-test split
remain untouched.

## 28. Current-project-state update summary

A narrow Phase 4bn-X paragraph was appended after the Phase 4bn-W paragraph and
a new active `Current phase:` block was inserted (prior Phase 4bn-A … 4bn-W
paragraphs and blocks preserved verbatim as labelled historical context). The
update records the branch, base SHA, result state, decision, the 40/40-PASS
gate over the 275-file label segment, the gate report path + SHAs, the
read-only/non-eligible posture, the explicit non-authorizations, and the
remain-paused recommendation. No retained verdict or project lock was modified.
