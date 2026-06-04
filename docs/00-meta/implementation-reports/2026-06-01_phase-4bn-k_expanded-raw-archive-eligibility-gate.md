# Phase 4bn-K — Expanded Raw Archive Eligibility Gate

**Phase 4bn-K is branch-complete only by this work; not merged into
main; not project-complete.** Phase 4bn-K is a raw archive eligibility
gate / local gitignored data-validation / docs + gate-report phase
(**Tier 1 Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3). It evaluates
the local Phase 4bn-J-R2 pre-v002 raw segment
(2024-03-01 .. 2024-11-30 inclusive UTC) for **structural** eligibility
to proceed to a future, separately authorized normalization-readiness /
normalization gate. It authorizes none of those downstream uses.

> **A passing raw archive gate does not flip `research_eligible`. It does
> not authorize normalization, feature derivation, label derivation, ML,
> diagnostics, or strategy. It does not authorize any successor phase.**

---

## 1. Purpose

The purpose of Phase 4bn-K is to record whether the newly acquired
pre-v002 raw envelope segment created by Phase 4bn-J-R2 is structurally
eligible to proceed to a future separately authorized normalization gate.
The gate reads, hashes, counts, decompresses, and validates the local
Phase 4bn-J-R2 raw artefacts under `data/microstructure/` for the
acquired pre-v002 segment **only**, and records a fail-closed gate result
state plus an explicitly non-authorizing decision.

The gate is **structural**, not empirical: it makes no claim about edge,
predictiveness, signal quality, profitability, or readiness. A PASS means
only that the local raw pre-v002 segment is structurally suitable to be
considered, under separate operator authorization, for a future
normalization-readiness / normalization planning phase.

---

## 2. Authority and repository state

- **Branch:** `phase-4bn-k/expanded-raw-archive-eligibility-gate`.
- **Base `main` SHA:** `cf7dc4f7e663d6f17610e775a9e5061de0b523ce`
  (`docs(phase-4bn-j-r2): finalize merge closeout shas`).
- Pre-branch verification: `HEAD == main == origin/main ==
  cf7dc4f7e663d6f17610e775a9e5061de0b523ce`; Phase 4bn-J-R2
  merge-closeout `26afba7`, merge `c80ab68`, and branch `e714150` present
  on `main`; GitHub remote `origin` →
  `https://github.com/jpedrocY/Prometheus.git`.
- Working tree before branch: only the expected untracked transient
  `.claude/scheduled_tasks.lock`; `data/microstructure/` and
  `data/research/` gitignored under `.gitignore:85` / `.gitignore:88`.
- Active local repo path: `D:\Prometheus`.
- Phase 4bn-K creates a branch only; it does **not** merge into `main`
  and does **not** record a merge-closeout.

---

## 3. Phase type and strict scope

Phase 4bn-K is a raw archive eligibility gate / local gitignored data
validation / docs + gate-report phase, classified **Tier 1 — Full
Phase** because it evaluates local raw acquisition artefacts created by
Phase 4bn-J-R2 and is adjacent to future normalization, feature
derivation, label derivation, future holdout policy, future ML-baseline
admissibility, and future data eligibility state — while explicitly
authorizing none of those downstream uses.

**Allowed:** read committed docs; inspect committed acquisition script,
tests, and source modules; read the Phase 4bn-J-R2 local segment
manifest and acquisition log; read / hash / decompress / validate the
local Phase 4bn-J-R2 raw zip archives and `.sha256` sidecars for
2024-03-01 .. 2024-11-30 only; run `zipfile.testzip()`; run bounded
Phase 4ax aggTrades row-sample validation; compare aggregate footprint
and row count to the manifest/log; create local gitignored gate
artefacts under the established `data/microstructure/gate-reports/raw/`
convention with a canonical `.sha256` sidecar; create tracked
documentation reports; add focused offline gate tests; update
`current-project-state.md` narrowly.

**Forbidden (and not done):** no data acquisition; no endpoint / public
endpoint / Binance / `data.binance.vision` contact; no archive or
CHECKSUM download; no HEAD preflight; no credentials / `.env` /
`.mcp.json` / MCP / Graphify; no authenticated / private endpoint;
no WebSocket / user stream; no v002 terminal-window read; no sealed
test-split read / count / sample / hash / summary / inspection / QA /
continuity use; no manifest mutation; no normalization; no feature /
label derivation; no feature ranking / selection / pruning /
engineering; no ML training / scoring / prediction; no diagnostics; no
strategy / signal / PnL / backtest; no storage migration; no database;
no `.duckdb` / `.sqlite`; no Parquet compaction; no v003; no ETHUSDT;
no extra horizons; no mark-price / spot / cross-venue / order-book /
tick data; no `data/research` output; no `data/microstructure` commit;
no manifest eligibility transition; no `research_eligible` flip; no
`eligibility_gate_status` transition; no successor authorization.

---

## 4. Evidence base and input boundary

**Committed evidence read:** `current-project-state.md`; the process
standards (`merge-closeout-standard.md`, `phase-risk-tiering-standard.md`,
`phase-workflow-standard.md`, `phase-prompt-template.md`,
`operator-report-standard.md`); the Phase 4bn-J / 4bn-J-R1 / 4bn-J-R2 and
Phase 4bn-I implementation reports and closeouts; the data specs
(`data-requirements.md`, `historical-data-spec.md`, `timestamp-policy.md`,
`dataset-versioning.md`) and `database-design.md`; the committed
acquisition script `scripts/phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py`
and its tests; the prior raw-gate precedents
`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`,
`scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`,
`scripts/phase4az_acquire_btcusdt_aggtrades_archive.py`; the source
modules `src/prometheus/research/microstructure/aggtrades.py` (Phase 4ax
validator) and `canonical_paths.py` (Phase 4bb-F path policy). README is
treated as potentially stale and not used as current-state authority.

**Local gitignored input read (pre-v002 segment only):** the Phase
4bn-J-R2 segment manifest
`data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`
(+ `.sha256`), the acquisition log
`…_pre_v002_segment_4bn_j_r2_acquisition_log.json` (+ `.sha256`), and the
275 raw zip archives + 275 `.sha256` sidecars referenced by that
manifest's `per_file_inventory` for 2024-03-01 .. 2024-11-30.

**Input boundary (hard, fail-closed):** the gate reads only files
recorded in the *segment* manifest and guards every inventory date.
Any date `>= 2024-12-01` is rejected and its file is **never opened**
(`is_within_segment(...)` returns before any filesystem access). The
existing v002 terminal window and the sealed v002 test split therefore
remain structurally unreachable, even though those files exist locally
under the same raw tree (`…/BTCUSDT/2024/12/`, `…/2025/`).

---

## 5. Phase 4bn-J-R2 result carried forward

Phase 4bn-J-R2 result:
`ACQUISITION_SUCCEEDED__RAW_ARTEFACTS_LOCAL_GITIGNORED__REMAIN_PAUSED`.
It acquired and integrity-verified the 275 new pre-v002 raw BTCUSDT
Binance USDⓈ-M futures aggTrades daily archives for
2024-03-01 .. 2024-11-30 inclusive UTC (0 missing / 0 checksum-mismatch /
0 decompression-failure / 0 row-sample-failure / 0 retry-exhausted / 0
cap-skip), totalling **5,140,686,147 bytes ≈ 4.788 GiB** and
**400,001,695** aggTrade rows in **2,051 s (≈34 min)**; no warning
threshold and no hard cap crossed. Segment manifest SHA256
`1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`;
acquisition log SHA256
`0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`.
All artefacts non-eligible (`research_eligible=false`,
`eligibility_gate_status="pending"`, `test_holdout_touched=false`).
Phase 4bn-K carries these recorded values forward as gate targets.

---

## 6. Raw segment under gate

- **Symbol:** BTCUSDT only.
- **Market:** Binance USDⓈ-M futures (`binance_usdm_futures`).
- **Data family:** aggTrades only.
- **New raw segment:** 2024-03-01 .. 2024-11-30 inclusive UTC.
- **Expected date count:** 275.
- **Expected raw archives:** 275 zip files.
- **Expected raw sidecars:** 275 `.sha256` sidecars.
- **Segment manifest:**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`
  (SHA256 `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`).
- **Acquisition log:**
  `…_pre_v002_segment_4bn_j_r2_acquisition_log.json`
  (SHA256 `0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`).
- **Expected footprint:** 5,140,686,147 bytes / 4.788 GiB.
- **Expected rows:** 400,001,695.
- **Path layout:**
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/{YYYY}/{MM}/BTCUSDT-aggTrades-{YYYY-MM-DD}.zip`.

---

## 7. Existing v002 terminal window by-reference treatment

The existing v002 terminal raw window (2024-12-01 .. 2025-02-28) and the
sealed v002 test split (2025-02-14 .. 2025-02-28) are handled **by
reference only** from committed docs and the segment manifest's
`existing_v002_terminal_window` / `existing_v002_sealed_test_split`
blocks. Phase 4bn-K did **not** read, hash, count, sample, summarize, or
inspect any v002 terminal-window file or any sealed-test file. No prior
v002 gate report (e.g. `phase-4bl-d`) and no published v002 raw manifest
was opened or mutated. The gate's hard date guard makes those files
structurally unreachable.

---

## 8. Gate implementation path

A new bounded standalone script
`scripts/phase4bn_k_validate_pre_v002_raw_archive_gate.py` was added,
modelled closely on the locked Phase 4bl-D multi-day raw gate
(`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`) but scoped
strictly to the pre-v002 *segment* manifest. The locked Phase 4bl-D
script (which targets the v002 manifest and reads the v002 window) was
**not** modified or invoked, so that no v002 / sealed-test artefact could
be touched. The new script imports only the Phase 4ax validator
(`validate_aggtrade_payload`) and the Phase 4bb-F canonical-path helpers;
it uses the standard library otherwise. No source module was modified.

Differences from the Phase 4bl-D template, all narrowing scope:

1. Targets the segment manifest + segment acquisition log and their
   Phase 4bn-J-R2 recorded SHA256 values.
2. Locked window 2024-03-01 .. 2024-11-30, 275 dates / files.
3. A hard `is_within_segment(...)` boundary guard rejects any date
   `>= 2024-12-01` and never opens its file (boundary fail-closed).
4. Adds segment-scope checks: `segment_label`, `data_family`, `market`,
   a scope-token denylist across all manifest paths, the
   `existing_v002_terminal_window` and `existing_v002_sealed_test_split`
   by-reference blocks, and the eligibility-state block
   (`research_eligible=false` / `eligibility_gate_status="pending"` /
   `test_holdout_touched=false`).
5. Row-validation depth (see §13) uses a **full** streaming structural
   scan over every row (independent row count + UTC boundary + strict
   agg-id monotonicity + min/max + first/last) plus a **bounded** Phase
   4ax full-schema `validate_aggtrade_payload` head+tail sample per
   archive, rather than full per-row Decimal payload validation across
   all 400,001,695 rows.
6. No Phase 4az single-day fixture-preservation check (that fixture is
   2025-01-15, inside the v002 window, and must not be touched).

53 focused offline tests were added in
`tests/research/microstructure/test_phase4bn_k_raw_archive_gate.py`
(no network, no local-data read, no sealed-test read). The gate report is
written to `data/microstructure/gate-reports/raw/` per the Phase 4bb-F
canonical path policy, with a paired `.sha256` sidecar; it is gitignored
and not committed.

**Tooling note (denylist fix + re-run).** The first gate execution
fail-closed on a defect in the gate's own scope-token denylist: the token
`"trades-"` is a substring of the in-scope `aggTrades-` family token
(lowercased `aggtrades-`), so it false-positively flagged every
legitimate aggTrades path. This was a tool defect, not a data defect — all
other 32 checks passed, including the full recomputed 400,001,695-row /
5,140,686,147-byte aggregates. The denylist token was corrected to the
hyphen-delimited `"-trades-"` (plus `"/trades/"` and `"/spot/"`), which
catches non-agg `BTCUSDT-trades-` / spot archives without matching
`aggTrades-`; a regression test was added; the false-failure local gate
report (and its sidecar) from the defective run was deleted; and the gate
was re-run from a clean state, producing the authoritative 33 / 33 PASS
report cited in §10.

---

## 9. Gate checks performed

The gate ran the following critical, fail-closed checks (overall verdict
is PASS only if every check passes):

1. `manifest_file_integrity` — segment manifest present, SHA256 ==
   `1659e6da…`.
2. `acquisition_log_integrity` — log present, SHA256 == `0266210f…`.
3. `sidecar_format_integrity` — manifest + log `.sha256` sidecars are
   canonical `<sha>␠␠<basename>\n` and match the target SHAs.
4. `gitignore_boundary` — `data/microstructure/`, `gate-reports/`, and
   `gate-reports/raw/` gitignored.
5. `manifest_schema_integrity` — all required manifest + inventory keys
   present.
6. `scope_lock` — family / version / schema / segment label / data
   family / market / window / counts match the locked scope.
7. `symbol_family_scope` — BTCUSDT / aggTrades / binance_usdm_futures
   only.
8. `scope_token_denylist` — no out-of-scope token (ethusdt, markprice,
   spot, orderbook, depth, klines, …) in any manifest path.
9. `segment_boundary_date_guard` — every inventory date within
   `[2024-03-01, 2024-12-01)`; no date reaches the v002 terminal window.
10. `date_list_integrity` — `date_list` and inventory dates equal the
    contiguous 275-day list; no missing, no duplicate.
11. `per_file_path_layout` — every path follows
    `…/BTCUSDT/{YYYY}/{MM}/BTCUSDT-aggTrades-{date}.zip`.
12. `no_unexpected_statuses` — every inventory entry status ==
    `acquired_verified`.
13. `raw_zip_existence`, `raw_zip_sha256_integrity` (vs manifest
    `sha256` and `sha256_from_companion`), `raw_zip_sidecar_integrity`
    (canonical sidecar matches the recomputed hash).
14. `zip_decompression_integrity` + `single_csv_member_integrity` —
    `zipfile.testzip()` reports no corruption; exactly one CSV member.
15. `bounded_row_sample_schema_validation` — Phase 4ax
    `validate_aggtrade_payload` on the per-archive head+tail sample.
16. `per_file_row_count_consistency`, `per_file_time_bounds_consistency`,
    `utc_day_boundary_integrity`,
    `agg_trade_id_monotonicity_within_file`,
    `agg_trade_id_overlap_absence_across_adjacent_dates`.
17. `total_row_count_consistency` (== 400,001,695),
    `total_size_bytes_consistency` (== 5,140,686,147),
    `archive_count_consistency` (== 275), `sidecar_count_consistency`
    (== 275).
18. `manifest_eligibility_state`,
    `v002_terminal_window_by_reference_preservation`,
    `sealed_test_split_untouched`.
19. `non_authorizations_preserved`, `retained_verdicts_preserved`,
    `project_locks_preserved`.

---

## 10. Local gate outputs, if any

The gate wrote one local gitignored gate report plus its canonical
`.sha256` sidecar under `data/microstructure/gate-reports/raw/`
(Phase 4bb-F canonical path policy). Both files are gitignored under
`.gitignore:85` and **uncommitted**.

- **Gate report:**
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bn-k__1780436389489__cf7dc4f7e663.json`
- **Gate report SHA256:**
  `051bed7b3a146278e389bd8e265243d30fd541b5f36061d0573f3522920f9c24`
- **Gate report sidecar:**
  `…__phase-4bn-k__1780436389489__cf7dc4f7e663.json.sha256` (153 bytes;
  canonical `<sha256>␠␠<basename>\n`; sidecar token matches the recomputed
  report SHA256 bit-for-bit).
- **Gate run:** `overall_status=pass`; **33 / 33** checks PASS / 0 FAIL /
  0 ERROR; wall-clock **496.2 s** (full SHA256 + `testzip()` + full
  streaming structural scan over all 400,001,695 rows + bounded Phase 4ax
  head+tail sample totalling **281,600** sampled rows validated across the
  275 archives).

The report records `phase-4bn-k`, base main SHA
`cf7dc4f7e663d6f17610e775a9e5061de0b523ce`, the input segment manifest
SHA256, the gate result state, `segment_non_eligible: true`,
`research_eligible_after: false`, `no_successor_authorization: true`,
`v002_terminal_window_read: false`, and `sealed_test_split_touched:
false`.

---

## 11. Date coverage result

**PASS.** Exactly 275 inventory dates; starts
2024-03-01; ends 2024-11-30; contiguous; no missing date; no duplicate
date; no date `>= 2024-12-01`; no date outside the pre-v002 segment.
(Pre-run static confirmation already established: inventory dates
`>= 2024-12-01` = none; duplicates = none; `sum` of per-file counts
matched the recorded aggregates.)

---

## 12. Sidecar and hash integrity result

**PASS.** Manifest + log SHA256 matched the Phase
4bn-J-R2 recorded values; manifest + log sidecars canonical; every raw
zip SHA256 matched both the manifest `sha256` and `sha256_from_companion`
and its paired canonical `.sha256` sidecar; all 275 sidecars present and
canonical (`<sha256>␠␠<basename>\n`, two spaces, LF, no BOM).

---

## 13. Zip and row-sample validation result

**PASS.** `zipfile.testzip()` reported no corruption on any
of the 275 archives; each archive contained exactly one CSV member with
the expected header
`agg_trade_id,price,quantity,first_trade_id,last_trade_id,transact_time,is_buyer_maker`.

**Row-validation decision.** Full per-row Decimal payload validation
across all 400,001,695 rows would impose excessive runtime (two full
decompression passes plus a `Decimal`-parsing object construction per
row). Per the gate brief's item-9 provision, the gate instead performs
(a) a **full** streaming structural scan over every row of every archive
— independently recomputing the per-file and aggregate row count, UTC
day boundary, strictly-increasing aggregate-trade-id, min/max
aggregate-trade-id, and first/last trade time — and (b) a **bounded**
Phase 4ax `validate_aggtrade_payload` full-schema check on a per-archive
head+tail sample (default 512 + 512 rows). This independently reproduces
the headline 400,001,695-row figure and the per-file bounds while keeping
the per-row full-schema check bounded, consistent with how Phase 4bn-J-R2
itself acquired and validated the segment (bounded Phase 4ax sample).
Headerless field order `a,p,q,f,l,T,m`, types, and timestamp behaviour
were confirmed on the samples.

---

## 14. Manifest / acquisition-log verification result

**PASS.** Segment manifest present, recomputed SHA256
`1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`;
acquisition log present, SHA256
`0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`;
`research_eligible=false`; `eligibility_gate_status="pending"`;
`test_holdout_touched=false`; `test_rows_loaded` absent (the segment
manifest does not carry that field; the no-test-rows invariant is
satisfied by `test_holdout_touched=false` and the segment never touching
the v002 window); `existing_v002_terminal_window`
`{read:false, redownloaded:false, overwritten:false}`;
`existing_v002_sealed_test_split` `{touched:false}`. The manifest was
read only; it was **not** mutated.

---

## 15. Aggregate count and footprint result

**PASS.** Recomputed archive count 275; recomputed sidecar
count 275; recomputed total footprint **5,140,686,147 bytes** (== manifest
== Phase 4bn-J-R2 recorded); recomputed total row count **400,001,695**
(== manifest == Phase 4bn-J-R2 recorded).

---

## 16. Gitignore and non-commit verification

`git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. No
`data/microstructure/` or `data/research/` artefact was staged. The gate
report and sidecar live under `data/microstructure/gate-reports/raw/`
(gitignored, uncommitted). No `data/research/` artefact was created. The
expected untracked transient `.claude/scheduled_tasks.lock` was present
and not committed.

---

## 17. Sealed-test preservation

The sealed v002 test split (2025-02-14 .. 2025-02-28) was not read,
counted, sampled, hashed, summarized, inspected, or used for any
continuity / QA check. It is structurally unreachable from the gate: the
segment manifest contains no date `>= 2024-12-01`, and the
`is_within_segment(...)` guard returns before any filesystem access for
any such date. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant was preserved (never invoked).

---

## 18. Boundary confirmations

No endpoint call was made; no acquisition was rerun; no archive or
CHECKSUM was downloaded; no HEAD preflight ran; no existing v002 terminal
data was read; no sealed test split was touched; no published v002
manifest was opened or mutated; no normalization / feature / label / ML /
diagnostics / strategy / signal / PnL / backtest work occurred; no
storage migration; no database; no `.duckdb` / `.sqlite`; no Parquet
compaction; no v003; no credentials / `.env` / `.mcp.json` / MCP /
Graphify; no WebSocket / user stream / private / authenticated endpoint.

---

## 19. Result state

**`RAW_ARCHIVE_GATE_PASSED__LOCAL_RAW_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`**

The local Phase 4bn-J-R2 pre-v002 raw segment is structurally eligible to
proceed, under separate operator authorization, to a future
normalization-readiness / normalization gate. It remains **non-eligible**
in the research sense (`research_eligible` stays `false`).

---

## 20. Decision

**`RECOMMEND_AUTHORIZE_DOCS_ONLY_DERIVED_STACK_STORAGE_BUDGET_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`**

Rationale (repository-evidence-grounded): the gate passed and the local
raw artefacts / manifest / sidecars are structurally sound. Before any
normalization / feature / label derivation, the project has already
identified (Phase 4bn-G combined data-expansion + storage-scaling
architecture scoping memo) that the full ML-ready 12-month derived stack
may plausibly require ~150–250 GiB with ~300 GiB comfortable working
headroom, and classified every derived-stack-expanding storage option as
"compatible but deferred" pending explicit storage governance. Phase
4bn-J-R2's own decision likewise listed a derived-stack storage-budget
memo as a next option *before* any normalization / features / labels. A
separate docs-only derived-stack storage-budget memo should therefore set
explicit caps and stage boundaries before any normalized / feature / label
phase runs. The acceptable alternative if repository convention is read to
expect normalization-readiness next is
`RECOMMEND_AUTHORIZE_NORMALIZATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
Phase 4bn-K authorizes neither; both are subject to separate operator
authorization.

---

## 21. Recommended state and successor options

**Recommended state: remain paused.** No next phase is authorized by
Phase 4bn-K. The operator may, subject to separate operator
authorization: remain paused (default); request a merge prompt for Phase
4bn-K; separately authorize a docs-only derived-stack storage-budget memo
(the preferred recommendation — see §20); separately authorize a
normalization-readiness or normalization execution plan only;
separately authorize a source-policy documentation memo; or reject
further ML-baseline successors and close the ML arc. No ML / diagnostics
/ normalization / feature / label / strategy / PnL / backtest / storage
migration / paper / shadow / live / exchange-write option is valid from
this state unless separately authorized after this branch is merged.

---

## 22. Explicit non-authorizations

Even on PASS, Phase 4bn-K does **not** flip `research_eligible` (raw
remains `false`), does not transition `eligibility_gate_status` out of
`pending`, does not transition `chronological_split_policy`, does not set
`diagnostics_authorized` or `ml_authorized`, does not authorize
normalization, feature derivation, label derivation, feature ranking /
selection / pruning / engineering, ML training / scoring / prediction,
diagnostics, strategy, signals, PnL, backtests, storage migration,
database creation, Parquet compaction, v003 creation, ETHUSDT, extra
horizons, mark-price / spot / cross-venue / order-book / tick data,
`data/research` outputs, paper / shadow, live-readiness, deployment,
exchange-write, production keys, MCP, Graphify, or any Phase 5 / any
successor phase. A passing raw archive gate means only that the local raw
pre-v002 segment is structurally suitable to proceed, under separate
authorization, to a future normalization planning / gate phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side;
round-trip = 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown
+ cooled-down families list + memo template; Phase 4al refined no-rescue
rule + §13 boundary + §14 hierarchy; Phase 4aw
`flip_research_eligible(...)` always-raises invariant; Phase 4bb-F
canonical path + sidecar policy; the Phase 4bn-J-R1 raw-only cap
amendment) is preserved verbatim. Phase 4 canonical remains unauthorized.

---

## 23. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: one new
Phase 4bn-K narrative paragraph and one new `Current phase:` block were
added; all prior paragraphs and `Current phase:` blocks (Phase 4bn-A …
Phase 4bn-J-R2 and earlier) are preserved verbatim as labelled historical
context. No other section of that document was changed.
