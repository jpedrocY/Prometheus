# Phase 4au Merge Closeout — Binance Microstructure Capture Design Specification Memo

## Merge identity

- **Phase:** 4au.
- **Phase title:** Binance Microstructure Capture Design
  Specification Memo.
- **Phase type:** docs-only Binance microstructure capture-
  design specification memo.
- **Target branch:** `main`.
- **Source branch:**
  `phase-4au/binance-microstructure-capture-design-specification`.
- **Merge method:** `--no-ff` (preserves the Phase 4au branch
  history as a discrete merge node on `main`).
- **Main before merge SHA:** `4bce0042fcccd32a4b1aeeda3bb19d7d73fb4121`.
- **Phase 4au memo commit SHA:**
  `41b7f29fc455ffd80a097dfbc2a58eb0ff99d195`
  (`docs(phase-4au): specify binance microstructure capture design`).
- **Phase 4au closeout commit SHA:**
  `e20e8d0c0158e85516da7cc53a124ca25ab74761`
  (`docs(phase-4au): add closeout`).
- **Phase 4au correction commit SHA:**
  `91b2983e3dc5350986a735eb8c571a4718bd4a09`
  (`docs(phase-4au): correct invalid-window trigger count`).
- **Merge commit SHA:** recorded in this merge closeout's final
  operator report (and in the live `git log` on `main`) once
  the merge commit lands. Self-referential SHA-in-content is
  avoided per prior-phase convention.

## Merge purpose

This merge brings the Phase 4au docs-only Binance microstructure
capture design specification onto `main`, together with the
Phase 4au closeout and a narrow Phase 4au update to
`docs/00-meta/current-project-state.md`. Phase 4au translates
the Phase 4at availability map and §15 capture-design
requirements into a precise, implementation-ready design
specification for a future public-only Binance microstructure
capture pipeline — without implementing anything.

The merge is **docs-only**. It brings forward the Phase 4au
memo, the Phase 4au closeout, and the narrow current-project-
state update. It does **not** authorise any successor phase,
data acquisition, endpoint call, public-archive download,
WebSocket connection, capture code, replay code, feature
implementation, ML model, strategy candidate, paper / shadow,
live-readiness, deployment, exchange-write, production-key
creation, authenticated APIs, private endpoints, user stream,
WebSocket implementation, MCP, Graphify, `.mcp.json`,
credentials, or any 5m / 1m / aggTrades / tick / mark-price 30m
/ 4h / order-book data acquisition.

## Pre-merge wording correction summary

One narrow wording correction was applied to the Phase 4au memo,
the Phase 4au closeout, and the narrow Phase 4au update in
`docs/00-meta/current-project-state.md` on the Phase 4au branch
in commit `91b2983e3dc5350986a735eb8c571a4718bd4a09`
(`docs(phase-4au): correct invalid-window trigger count`)
**before** this merge:

- **Correction — invalid-window trigger count:** the memo,
  the closeout, and the narrow current-project-state update
  previously said "sixteen trigger reasons" for the Phase 4au
  invalid-window taxonomy, but the listed taxonomy contains
  **17** triggers (`missing_sequence`, `out_of_order_event`,
  `duplicate_event`, `gap_after_reconnect`, `snapshot_mismatch`,
  `clock_skew`, `symbol_mismatch`, `stale_stream`, `stale_book`,
  `impossible_spread`, `negative_size`, `zero_or_invalid_price`,
  `archive_checksum_mismatch`, `rest_retention_gap`,
  `force_order_proxy_incompleteness`, `failed_atomic_write`,
  `partial_file_recovery_event`). The wording was updated to
  "seventeen trigger reasons" in all four locations (memo §23
  research-interpretation summary; closeout §"Capture design
  result" Invalid-window taxonomy heading; closeout §"Research
  interpretation review" summary; and the two
  current-project-state references — the long Phase 4au
  narrative paragraph and the Phase 4au "Current phase:"
  block).

The taxonomy itself was **not** changed; the 17 triggers remain
listed verbatim in §21.1 of the Phase 4au memo. No substantive
design conclusion changed. No data was acquired. No Binance
endpoint was called. No code, script, source, test, data,
manifest, governance, verdict, lock, or `.gitignore` was
modified. No successor authorisation changed.

## Files brought forward

- `docs/00-meta/implementation-reports/2026-05-07_phase-4au_binance-microstructure-capture-design-specification.md`
  — Phase 4au main memo (36 sections; +2,243 lines initially;
  with the wording correction applied in the Phase 4au
  correction commit).
- `docs/00-meta/implementation-reports/2026-05-07_phase-4au_closeout.md`
  — Phase 4au closeout (+745 lines initially; with the wording
  correction applied in the Phase 4au correction commit).
- `docs/00-meta/current-project-state.md`
  — narrow update: Phase 4au narrative paragraph + Phase 4au
  "Current phase:" block + transition lines preserving the
  prior Phase 4at block as historical context (matching
  prior-phase convention; with the wording correction applied
  in the Phase 4au correction commit).

This merge closeout adds:

- `docs/00-meta/implementation-reports/2026-05-07_phase-4au_merge-closeout.md`
  — this file.

No other file is changed by this merge.

## Confirmation Phase 4au was docs-only

Phase 4au is a docs-only design specification memo. The merge
brings forward only:

- the Phase 4au memo,
- the Phase 4au closeout,
- the narrow `current-project-state.md` update,
- this merge closeout.

No script was added or executed. No backtest was run. No data
was acquired. No Binance endpoint was called. No WebSocket was
opened. No archive file was downloaded. No code under
`src/prometheus/` was modified. No test was modified. No
existing script was modified. No `.gitignore` change was made.
No `data/research/` content was committed. **No directory
under `data/microstructure/...` was created.** **No actual
manifest file was created.** No schema file or capture-code
artefact was created.

`ruff check`, `pytest`, and `mypy` were **not** run because the
phase is docs-only (no `src/prometheus/`, test, script, or
`scripts/` change of any kind). This matches the docs-only
convention used by prior docs-only phases.

## Phase 4au capture-design result

Phase 4au translates the Phase 4at availability map and §15
capture-design requirements into a precise, implementation-
ready design specification for a future public-only Binance
microstructure capture pipeline. **None of the design is
implemented.**

### Nine-component architecture summary

1. Capture supervisor.
2. Per-symbol stream workers.
3. REST polling workers.
4. Raw event writer.
5. Normalizer.
6. Replay builder.
7. Manifest writer.
8. Health-check reporter.
9. Local operator dashboard hook.

All components are specified at the design layer only and run
**outside** `prometheus.runtime`, `prometheus.execution`, and
`prometheus.persistence`.

### Public-only endpoint allowlist summary

Thirteen families:

- aggTrade family (WS + REST + bulk archive);
- bookTicker stream;
- partial book depth stream;
- diff book depth stream;
- REST depth snapshot;
- forceOrder proxy stream;
- markPrice family (WS + REST + bulk archive; **governance-
  blocked under Phase 3r §8 / Phase 3v §8**);
- indexPrice family;
- fundingRate REST;
- openInterest REST snapshot (forward REST polling for time-
  series; not WebSocket);
- openInterestHist REST (~30 days rolling);
- top/global long-short REST (~30 days rolling);
- takerlongshortRatio REST (~30 days rolling).

### Explicit endpoint denylist summary

All private / authenticated endpoints; user stream; listenKey
lifecycle; REST `/fapi/v1/forceOrders` (user-scope); order
placement; account; position; leverage / margin endpoints; any
endpoint requiring API keys; MCP / Graphify / `.mcp.json` /
credential-based integrations.

### Seven dataset-family design names recorded but not created

- `microstructure_raw_aggtrades_v001`
- `microstructure_raw_depthdiff_v001`
- `microstructure_raw_bookticker_v001`
- `microstructure_raw_forceorder_proxy_v001`
- `microstructure_raw_markprice_v001`
- `microstructure_metrics_oi_funding_v001`
- `microstructure_replay_lob_v001`

Per-family design fields recorded: purpose, source endpoint
family, raw / normalized / derived layer, partition keys, file
format, timestamp / sequence fields, schema-version field,
manifest requirement, default `research_eligible: false`,
invalid-window behaviour, and governance constraints. **None
created.**

### Separate `data/microstructure/...` namespace recommended; no directories created

```text
data/microstructure/raw/<family>/<symbol>/<yyyy>/<mm>/<dd>/<file>.jsonl.zst
data/microstructure/normalized/<family>/<symbol>/<yyyy>/<mm>/<file>.parquet
data/microstructure/derived/<family>/<symbol>/<yyyy>/<mm>/<file>.parquet
data/microstructure/manifests/<family>__v001.json
```

A separate namespace is recommended (rather than reusing
`data/raw/` / `data/normalized/` / `data/manifests/` paths)
to keep the new high-volume capture pipeline cleanly isolated
from the existing project data families. **No directory is
created by Phase 4au.**

### Manifest design recorded but no manifest created

Required fields: `dataset_family`, `version`, `symbol`,
`source`, `endpoint`, `capture_mode`, `start_time_ms`,
`end_time_ms`, `event_count`, `file_count`, paired SHA256 list
per file with per-file time range and event count,
`schema_version`, `endpoint_docs_reference`,
`capture_config_hash`, `code_commit_sha`, `invalid_windows[]`,
`retention_warning`, `proxy_warning`, `governance_labels`,
`research_eligible: false` default, `eligibility_gate_status:
pending` default. **No actual manifest file is created.**

### Schema design recorded but no schema/code created

Per-family schemas: aggTrades, bookTicker, depthDiff,
depthSnapshot, forceOrder proxy, markPrice, OI / funding
metrics, reconstructed LOB state. Every raw-layer schema
records `event_time_ms` / `transaction_time_ms` /
`ingestion_time_ms` / `local_monotonic_ns` separately. **No
schema-as-code artefact, no Pydantic / dataclass / IDL
declaration is created.**

### Seventeen-trigger invalid-window taxonomy recorded

`missing_sequence`, `out_of_order_event`, `duplicate_event`,
`gap_after_reconnect`, `snapshot_mismatch`, `clock_skew`,
`symbol_mismatch`, `stale_stream`, `stale_book`,
`impossible_spread`, `negative_size`, `zero_or_invalid_price`,
`archive_checksum_mismatch`, `rest_retention_gap`,
`force_order_proxy_incompleteness`, `failed_atomic_write`,
`partial_file_recovery_event`. Every entry carries
`start_time_ms`, `end_time_ms`, `family`, `symbol`, `reason`,
`evidence`, `severity`, `downstream_eligibility_action`.
**No silent forward-fill / interpolation / imputation /
replacement** (Phase 3p §4.7 / Phase 3r §8 / Phase 4j §11
precedent).

### Ten-check research eligibility gate recorded but not implemented

Raw files present; checksum pass; schema validation pass;
timestamp sanity pass; sequence continuity pass; invalid-
window threshold (≤ 5 % per family per month for non-info
severity); retention completeness label; proxy limitation
label; governance labels; final `research_eligible` decision.
The gate is the **only** path that may flip
`research_eligible: true` and set
`eligibility_gate_status = "passed_full"` (or
`"passed_partial"` for governance-bounded families like OI
subset under Phase 4j §11). **Not implemented.**

### Deterministic replay design recorded but not implemented

Raw → normalized; normalized → derived; LOB replay; replay
config hash; reproducibility requirements (byte-identical
output under same inputs); no ad-hoc reads of raw logs;
replay logs for every run; replay failure handling (no partial
output; partial files deleted; `invalid_window` recorded if
applicable). **Not implemented.**

### Health-check / dashboard design recorded but not implemented

Per-stream `last_event_time` / `ingestion_lag` / `reconnect_count`
/ `gap_count`; per-family `invalid_window_count`; `disk_usage`
per layer; `file_write_lag`; `rate_limit_status` per endpoint;
`per_symbol_stream_status`. **Local-only display**; no order
panel; no kill-switch surface; no remote alerting at this
layer. **Not implemented.**

### Security and credential boundary recorded

No API keys; no `.env` reads; no authenticated endpoints; no
private endpoints; no order endpoints; no leverage / margin
endpoints; no user stream; no listenKey; no MCP / Graphify /
`.mcp.json`; no secrets in logs (trivially safe — no signature
ever computed because the public-only boundary makes signing
unnecessary).

### Runtime separation recorded

No imports from `prometheus.runtime` / `execution` /
`persistence`; no runtime database writes; no safety-state
mutation; no order-router contact. The capture pipeline is
research infrastructure only.

## Recommendation

- **Primary recommendation:** remain paused.
- **Conditional secondary (NOT authorized by this merge):**
  Phase 4av — Public-Only Microstructure Capture Implementation
  Plan (docs-only). Translates the Phase 4au design
  specification into a precise, file-by-file docs-only
  implementation plan covering file list, module boundaries,
  CLI surface, test matrix, failure modes, validation gates,
  and implementation order — **without implementing capture**.
  No acquisition. No successor authorisation. **Phase 4av is
  NOT authorized by this merge.**
- **Alternative acceptable recommendation:** remain paused if
  more design review is needed before any implementation
  planning.
- **NOT recommended:** immediate implementation; immediate
  endpoint calls; immediate WebSocket connections; immediate
  archive downloads; immediate capture; immediate order-book
  reconstruction; immediate replay; immediate feature
  implementation; immediate ML or strategy work; old-strategy
  alt-symbol rerun; R3 / R2 / V1-arc rescue; reopening the 5m
  research thread; paper / live work.
- **FORBIDDEN:** verdict revision; lock revision; parameter
  optimization; strategy resurrection; M0 amendment; reopening
  the 5m research thread; data acquisition without separately
  authorised data-requirements memo; paper / shadow / live-
  readiness / deployment / exchange-write / production-key
  creation / authenticated APIs / private endpoints / public-
  endpoint calls in code / user stream / WebSocket
  implementation / MCP / Graphify / `.mcp.json` / credentials.

## Implementation / governance review

### What changed

- New file: `docs/00-meta/implementation-reports/2026-05-07_phase-4au_binance-microstructure-capture-design-specification.md`
  (Phase 4au main memo, with the pre-merge wording correction
  applied).
- New file: `docs/00-meta/implementation-reports/2026-05-07_phase-4au_closeout.md`
  (Phase 4au closeout, with the pre-merge wording correction
  applied).
- Narrow update: `docs/00-meta/current-project-state.md`
  (Phase 4au narrative paragraph + Phase 4au "Current phase:"
  block + transition lines preserving the prior Phase 4at
  block as historical context; with the pre-merge wording
  correction applied).
- New file (this merge): `docs/00-meta/implementation-reports/2026-05-07_phase-4au_merge-closeout.md`.

### What did not change

- No `src/prometheus/` modification.
- No test modification.
- No existing-script modification.
- No data / manifest / `research_eligible` / v003 change.
- **No directory under `data/microstructure/...` created.**
- **No actual manifest file created.**
- No `.gitignore` modification.
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No 5m / 1m / aggTrades / tick / mark-price 30m / 4h /
  order-book acquisition.
- No reopening of the 5m research thread.
- No backtest run.
- No historical strategy script executed.
- No endpoint code modification.
- No endpoint call.
- No WebSocket opened.
- No public-archive download.
- No capture, replay, order-book-reconstruction, or feature
  implementation.

### Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are
preserved verbatim. M0 governance is unchanged. The 5m
closure (Phase 3t) is preserved. The cost lock (§11.6) and
project locks (§1.7.3) are preserved. The stop-trigger-domain
governance (Phase 3v §8), break-even / EMA slope /
stagnation governance (Phase 3w §6 / §7 / §8), mark-price gap
governance (Phase 3r §8), and OI subset governance
(Phase 4j §11) are all preserved. The Phase 4ak M0 gate,
post-null cooldown rule, cooled-down families list, and memo
template are all preserved. The Phase 4al refined no-rescue
rule, the Phase 4am audit findings, the Phase 4an inventory,
the Phase 4ao harmonization, the Phase 4ap forensic plan, the
Phase 4aq computation, the Phase 4ar interpretation, the
Phase 4as mechanism map, and the Phase 4at availability map
are all preserved.

### Is the merge docs-only?

Yes. The merge brings forward two new memos under
`docs/00-meta/implementation-reports/` plus a narrow update to
`docs/00-meta/current-project-state.md`, plus this merge
closeout. No code, test, script, data, manifest, governance,
or lock change occurs.

## Research interpretation review (plain English)

### What did this phase prove?

Phase 4au did not prove anything in the predictive-statistics
sense. As a docs-only design specification memo it documents,
in implementation-ready detail, a future public-only Binance
microstructure capture pipeline covering nine cooperating
components, a thirteen-endpoint allowlist, an explicit
denylist, seven proposed dataset family designs, a four-layer
storage model with a recommended separate
`data/microstructure/...` namespace, a per-family schema
design, a manifest design with all required fields, an
invalid-window taxonomy with **seventeen** trigger reasons,
an eligibility-gate design with ten checks, deterministic-
replay rules, a health-check / operator-dashboard design,
security / credential boundaries, runtime-separation rules,
and a symbol / scope policy.

### What did this phase not prove?

Phase 4au did not prove that any specific microstructure
mechanism contains edge. It did not run any computation. It
did not acquire any data. It did not call any Binance
endpoint or open any WebSocket. It did not authorise any
successor phase. It did not implement any capture, replay,
feature, or strategy. It did not amend M0. It did not modify
any verdict or lock. It did not create a strategy candidate.

### Which original questions did it answer?

The Phase 4au question — "Exactly what public-only Binance
microstructure capture architecture, endpoint allowlist,
storage layout, schema design, manifest discipline, invalid-
window governance, replay discipline, health-check model, and
safety boundary would need to exist before any future capture
implementation could be safely authorized?" — is answered
across §6 (capture design goals), §7 (architecture overview),
§8 (public-only endpoint allowlist), §9 (denylist), §10
(dataset family design), §11 (storage layout), §12 (file
format / compression), §13 (manifest design), §14 (schema
design), §15 (timestamp discipline), §16 (rate-limit / retry),
§17 (WebSocket connection), §18 (LOB reconstruction), §19
(liquidation proxy), §20 (OI / funding capture), §21
(invalid-window governance), §22 (eligibility gate), §23
(replay), §24 (health-check / dashboard), §25 (security
boundary), §26 (runtime separation), §27 (symbol / scope),
§28 (storage / hardware feasibility), §29 (validation /
anti-overfitting), §30 (M0 implications), §31 (recommended
next phase Phase 4av).

### Which original questions remain open?

- Whether any of the M-1 → M-14 mechanisms contains edge
  under the project's locked cost realism. **This is not
  answered by this merge.**
- Whether Phase 4av is the cleanest next move. The memo
  recommends Phase 4av but does **not** authorise it.
- Whether storage and operational overhead for live capture
  is acceptable for the project's host in numeric terms. The
  Phase 4au memo makes only qualitative estimates.

### What does it mean for strategy research?

This merge confirms that Lane A — Binance microstructure data
availability / capture feasibility — now has both an
exhaustive public-availability map (Phase 4at) and an
implementation-ready capture design specification (Phase 4au)
at the docs layer. Together they form a complete docs-only
foundation that any future implementation phase can build
against. The cooled-down families list, the six-candidate
rejection topology, the cost lock, the position lock, the
leverage lock, and the mark-price stop lock are all
preserved. M0 remains the binding admissibility framework.

### What does it mean for governance?

This merge reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k,
Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption,
Phase 4al refined no-rescue + §13 / §14, Phase 4am §11.A audit
findings, Phase 4an inventory, Phase 4ao harmonization,
Phase 4ap forensic plan, Phase 4aq computation result
preserved as descriptive evidence only, Phase 4ar
interpretation result preserved as descriptive interpretation
only, Phase 4as mechanism-map result preserved as docs-only
reset evidence only, and Phase 4at availability map preserved
as docs-only feasibility evidence only. **None is amended.**

### What is the clean next step?

Operator review of Phase 4au on `main` after this merge lands.
**No successor phase is authorised by this merge.** The clean
next step is operator-driven only. Acceptable separately-
authorised future options include remain paused (recommended),
Phase 4av as a docs-only public-only microstructure capture
implementation plan, or further docs-only governance memos on
precise governance questions. None is started or authorised
by this merge.

### What should we not do yet?

- No data acquisition.
- No Binance endpoint calls.
- No public-archive downloads.
- No WebSocket connections.
- No capture implementation.
- No order-book reconstruction implementation.
- No replay implementation.
- No feature implementation.
- No ML model.
- No new strategy candidate.
- No exit / entry design.
- No verdict / lock revision.
- No M0 amendment.
- No reopening of the 5m research thread.
- No 5m / 1m / aggTrades / tick / mark-price 30m / 4h /
  order-book acquisition.
- No paper / shadow / live-readiness / deployment /
  exchange-write / production-key creation / authenticated
  APIs / private endpoints / user stream / WebSocket
  implementation / MCP / Graphify / `.mcp.json` / credentials.

## Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m research thread** — operationally CLOSED (Phase 3t).
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

## Preserved project locks

- **M0 governance** — binding prospectively only.
- **§11.6** — 8 bps slippage per side; round-trip = 16 bps.
- **§1.7.3** — 0.25 % risk per trade; 2× leverage cap; one
  position max; mark-price stops where applicable.
- **Phase 3r §8** — mark-price gap governance.
- **Phase 3v §8** — stop-trigger-domain governance.
- **Phase 3w §6 / §7 / §8** — break-even / EMA slope /
  stagnation governance.
- **Phase 4j §11** — metrics OI-subset partial-eligibility
  rule.
- **Phase 4k** — V2 backtest-plan methodology.
- **Phase 4p** — G1 strategy-spec memo.
- **Phase 4q** — G1 backtest-plan methodology.
- **Phase 4v** — C1 strategy-spec memo.
- **Phase 4w** — C1 backtest-plan methodology.
- **Phase 4ak** — M0 mechanism-admissibility gate adoption
  (twelve clauses + post-null cooldown + cooled-down families
  list + memo template).
- **Phase 4al** — refined no-rescue rule + §13 future-phase
  boundary + §14 data-resolution hierarchy.
- **Phase 4am** — §11.A audit findings.
- **Phase 4an** — historical-trade-population exit-path
  inventory.
- **Phase 4ao** — exit-path methodology / artefact
  harmonization.
- **Phase 4ap** — V1-Arc Exit-Path Forensic Plan.
- **Phase 4aq** — computation result preserved as descriptive
  evidence only.
- **Phase 4ar** — interpretation result preserved as
  descriptive interpretation only.
- **Phase 4as** — mechanism-map result preserved as docs-only
  reset evidence only.
- **Phase 4at** — availability / capture-feasibility result
  preserved as docs-only feasibility evidence only.
- **Phase 4au** — capture-design result preserved as docs-only
  design evidence only.

## No-rescue constraints (preserved)

- No R3-prime / R2-prime / R1a-prime / R1b-narrow-prime /
  H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime /
  V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow /
  G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy
  hybrid.
- No window / threshold / parameter mining from Phase 4l /
  Phase 4r / Phase 4x forensic numbers.
- No reopening of the 5m research thread.
- No silent reduction of microstructure to a rank-then-trade
  variant of any cooled-down candidate.
- No microstructure use of optional metrics ratio columns
  outside Phase 4j §11.
- No D1-A reuse as a directional trigger; funding remains a
  context lens only if ever used.

## Successor authorisation status

**No successor phase is authorised by this merge.** The
following remain unauthorised:

- Phase 4av;
- Phase 5;
- Phase 4 canonical;
- data acquisition;
- Binance endpoint calls;
- public-archive downloads;
- WebSocket connections;
- endpoint implementation;
- data-capture implementation;
- order-book reconstruction implementation;
- replay implementation;
- feature implementation;
- ML model;
- strategy candidate;
- entry / exit design;
- old-strategy alt-symbol reruns;
- R3 / R2 / V1-arc rescue;
- 5m research thread reopening;
- 5m / 1m / aggTrades / tick / mark-price 30m / 4h /
  order-book data acquisition;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production keys;
- authenticated APIs;
- private endpoints;
- user stream;
- WebSocket implementation;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

## Final status

Phase 4au is being merged into `main` via `--no-ff` to preserve
the Phase 4au branch history as a discrete merge node.
Phase 4au is docs-only. **Recommended state remains paused
unless the operator separately authorizes a future phase.** No
next phase is authorized.

## End of Phase 4au merge closeout
