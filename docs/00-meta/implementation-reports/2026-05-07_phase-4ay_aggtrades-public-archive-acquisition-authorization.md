# Phase 4ay — AggTrades Public Archive Acquisition Authorization Memo

**Type:** docs-only data-acquisition authorization / boundary memo.
**Status:** drafted on branch `phase-4ay/aggtrades-public-archive-acquisition-authorization`; pending operator review and merge approval.
**Date:** 2026-05-07.

---

## 1. Executive summary

Phase 4ay is a docs-only authorization-boundary memo. It defines the exact constraints under which a future, separately-authorized phase could safely acquire a first, tightly scoped public Binance USDⓈ-M Futures aggTrades archive sample on top of the Phase 4aw scaffold and the Phase 4ax aggTrades-only collector skeleton — without acquiring data here, contacting endpoints, opening WebSockets, downloading archives, creating `data/microstructure/`, writing under any project data path, creating real manifests, modifying source / tests / scripts / strategy specs / governance, creating strategies / features / ML, or authorizing any successor phase.

Phase 4ay does **not** acquire data. Phase 4ay does **not** authorize Phase 4az or any other successor. Phase 4ay produces a written authorization framework only; activation is a separate operator decision.

The memo defines: a conservative future acquisition target (BTCUSDT, one complete UTC day, public archive only); a candidate symbol/date policy; a public archive source plan; a strict integrity gate (mapping Phase 3p §4.7 strict-integrity discipline onto aggTrades); a future staging and storage plan rooted under `data/microstructure/`; a manifest authorization plan whose `research_eligible` defaults to `false`; explicit fail-closed rules; the relationship to §11.6 cost realism (unchanged); the relationship to M0 admissibility and the post-null cooldown rule (preserved); future implementation options A / B / C with conservative recommendation; explicit non-recommendations; an implementation / governance review; and an 8-question research interpretation review in plain English.

---

## 2. Scope and explicit non-scope

### Allowed (and performed) in Phase 4ay

- Static repository inspection of committed docs (Phase 3p, 3r, 3v, 3w, 4j, 4k, 4l, 4m, 4n, 4o, 4p, 4q, 4r, 4s, 4t, 4u, 4v, 4w, 4x, 4y, 4z, 4aa, 4ab, 4ac, 4ad, 4ae, 4af, 4ag, 4ah, 4ai, 4aj, 4ak, 4al, 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax).
- Reasoning derived from the Phase 4aw scaffold and the Phase 4ax aggTrades-only collector skeleton.
- Reasoning derived from official / public Binance documentation references where useful (no live calls, no fetches; references only).
- Adding the Phase 4ay memo and closeout under `docs/00-meta/implementation-reports/`.
- A narrow `docs/00-meta/current-project-state.md` update.

### Forbidden (and not performed) in Phase 4ay

- Acquire data of any kind.
- Call Binance endpoints.
- Open WebSockets.
- Download public archive files.
- Create the `data/microstructure/` directory.
- Write raw files under any project data path.
- Create real project manifests.
- Implement REST clients.
- Implement WebSocket clients.
- Implement collectors.
- Modify the Phase 4ax aggTrades skeleton.
- Implement order-book reconstruction.
- Implement deterministic replay.
- Implement normalizers.
- Implement eligibility-gate execution.
- Implement feature computation.
- Compute predictive statistics.
- Run backtests, historical strategy scripts, Phase 4aq / Phase 4l / Phase 4r / Phase 4x or any prior research script, or simulations.
- Modify existing data, manifests, trade logs, source code, tests, scripts, strategy specs, thresholds, governance docs, retained verdicts, project locks, or prior research reports beyond the new Phase 4ay docs and the narrow `current-project-state.md` update.
- Create a strategy candidate, design entries or exits, or create an ML model.
- Authorize any successor phase by Phase 4ay itself.

---

## 3. Repository verification summary

Before branching:

- Branch: `main`.
- Working tree: clean (only gitignored `.claude/scheduled_tasks.lock` and `data/research/` untracked).
- `git rev-parse main` and `git rev-parse origin/main` both `436660e4e9578b6086f6a73367e2e68cd83ead1b`.
- All Phase 4ax artefacts present on main:
  - `src/prometheus/research/microstructure/aggtrades.py`,
  - `tests/research/microstructure/test_aggtrades.py`,
  - `docs/00-meta/implementation-reports/2026-05-07_phase-4ax_aggtrades-only-public-microstructure-collector-skeleton.md`,
  - `docs/00-meta/implementation-reports/2026-05-07_phase-4ax_closeout.md`,
  - `docs/00-meta/implementation-reports/2026-05-07_phase-4ax_merge-closeout.md`.
- All Phase 4aw scaffold modules present on main: `__init__.py`, `config.py`, `allowlist.py`, `invalid_window.py`, `manifest.py`, `raw_writer.py`.
- `.gitignore` line `data/microstructure/` present (added by Phase 4aw).
- `data/microstructure/` directory does not exist.
- Phase 3p §4.7 integrity-gate spec is committed at `docs/00-meta/implementation-reports/2026-04-30_phase-3p_5m-diagnostics-data-requirements-and-execution-plan.md` (referenced verbatim in §14 below).

Phase 4ay branch `phase-4ay/aggtrades-public-archive-acquisition-authorization` was created from this clean base.

---

## 4. Methodology

Phase 4ay is a docs-only authorization memo. It was constructed under the following methodology:

- **Static repo inspection only.** Committed docs and prior phase reports were read. No code or test was executed.
- **Official / public documentation references.** Where useful, the memo references conventions known from the official Binance public market-data archive (`data.binance.vision`) and the `binance/binance-public-data` repository. No live fetch, no endpoint call, no archive download was performed.
- **No endpoint calls.** No HTTP request was issued.
- **No WebSockets.** No streaming connection was opened.
- **No archive downloads.** No file under the public archive was retrieved.
- **No data acquisition.** Nothing was written under any project data path.
- **No code / source / test / data / manifest change.** The Phase 4aw scaffold and the Phase 4ax aggTrades skeleton remain byte-identical.
- **No strategy candidate.** No strategy is proposed.
- **No feature implementation.** No metric, transform, or feature was computed.
- **No ML model.** No model was trained, fit, or evaluated.
- **No successor authorization.** Phase 4ay records a *framework* for a possible future Phase 4az; it does not activate Phase 4az.

---

## 5. Phase 4ax baseline (preserved)

Phase 4ay is layered on top of Phase 4ax. The Phase 4ax aggTrades-only collector skeleton, merged at `436660e4e9578b6086f6a73367e2e68cd83ead1b`, provides:

- **Mocked / offline payload validation.** `validate_aggtrade_payload` accepts REST-shaped or stream-shaped payloads, enforces field-shape and value constraints (price > 0, quantity > 0, `l` ≥ `f`, `T` > 0, `m` strictly bool, optional `E` > 0 if present), preserves unknown extra fields, and accepts int-shaped strings for integer-typed fields.
- **Taker-side derivation.** `m=False → BUY`; `m=True → SELL`.
- **Dry-run planning.** `build_aggtrades_plan(...)` returns a frozen `AggTradePlan` for archive / REST / WS modes without creating directories or contacting endpoints.
- **Temp-path writer composition.** `write_validated_aggtrades_to_path(payloads, target_path)` composes the Phase 4aw `RawWriter` for pytest temp-path JSONL + paired SHA256 finalisation; refuses paths under `data/microstructure/` regardless of OS separator; fails closed on validation errors mid-stream without leaving a finalised file behind.
- **No endpoint contact.** No HTTP, WebSocket, urllib, socket, or Binance SDK import.
- **No real data.** Tests use pytest `tmp_path` only.
- **No manifest creation.** The `AggTradeWriteResult` is the explicit handoff contract; manifest translation is not implemented.
- **No `data/microstructure/` directory.** The Phase 4aw `.gitignore` line continues to protect the path.

Phase 4ay does not modify any of these properties.

---

## 6. Why a separate authorization memo is needed

Acquiring real public market data is a deliberate boundary crossing. Until now, the project has been limited to:

- historical klines / funding / metrics already acquired by Phase 2 / Phase 3q / Phase 4i / Phase 4ac under prior, separately authorized acquisition phases;
- inert microstructure infrastructure (Phase 4aw scaffold + Phase 4ax aggTrades-only skeleton).

A future aggTrades archive acquisition is qualitatively different from the inert path because:

1. **Real external data enters the project.** External bytes — even from a public archive — become part of the local repository's data tree.
2. **Project data paths may be created.** `data/microstructure/staging/`, `data/microstructure/raw/`, `data/microstructure/manifests/` may be populated for the first time.
3. **Manifests may be required.** The data must be self-describing for replay, audit, and eligibility-gate decisions.
4. **Checksums and retention completeness matter.** Bit-flips, mid-stream truncation, mid-day archive splits, or upstream gaps must be detected, recorded, and not silently masked.
5. **Acquired data can later support features.** Therefore the governance boundary must be established *before* acquisition, not after — to make later feature work cleanly subordinate to the acquisition gate rather than retrospectively justified.
6. **Acquisition is not strategy research and must not imply edge.** Real data does not by itself license any edge claim. M0 admissibility (Phase 4ak), the Phase 4al refined no-rescue rule, the Phase 4m 18-requirement validity gate, and the Phase 4t 10-dimension scoring matrix all remain binding for any future strategy hypothesis derived from microstructure data.

A separate authorization memo therefore serves two purposes: (a) the operator approves crossing the boundary explicitly and on the record; and (b) the boundary's exact shape is fixed in writing before the work begins.

---

## 7. Proposed future acquisition target

### 7.1 Recommended scope

A future, separately authorized acquisition phase should adopt the most conservative non-trivial scope:

- **Data family:** `microstructure_raw_aggtrades_v001`.
- **Market:** Binance USDⓈ-M Futures.
- **Source:** public Binance archive only; preferred host `data.binance.vision`.
- **Symbol:** `BTCUSDT` only for first acquisition.
- **Timeframe:** one complete UTC daily archive file. The exact date should be selected in the future acquisition memo according to archive availability and operator confirmation; the recommended posture is to choose a stable historical day at least 30 days before the acquisition date so retention-window limitations are unlikely to bite.
- **Mode:** public archive download only — explicitly **not** REST polling and **not** WebSocket capture.
- **Project paths (descriptive only; not created by Phase 4ay):**
  - raw landing: `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/<yyyy>/<mm>/`;
  - manifest: `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json`;
  - staging: `data/microstructure/staging/microstructure_raw_aggtrades_v001/BTCUSDT/<yyyy>/<mm>/`.
- **`research_eligible` default:** `false` until the eligibility gate runs and explicitly flips it. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always raises; only a future, separately authorized eligibility-gate phase may legitimately bypass that with its own primitive.

### 7.2 Phase 4ay does not acquire this data

Phase 4ay records the proposed target only. The exact date, the exact archive URL, the exact file size, the exact checksum, the exact event count, and the exact final landing path are all to be selected and recorded at acquisition time in the future Phase 4az memo (if ever authorized). Phase 4ay does **not** activate Phase 4az.

---

## 8. Candidate symbol / date policy

The future acquisition phase, if ever authorized, must respect the following symbol / date policy:

- **BTCUSDT first.** ETHUSDT and any alt symbol are excluded from the first acquisition unless separately authorized in a successor memo.
- **No alt-symbol mining.** The choice of BTCUSDT is anchored in §1.7.3 project-level scope (BTCUSDT primary; ETHUSDT comparison only) and Phase 4aa / Phase 4ab alt-symbol governance, not in any expectation of microstructure edge.
- **No old-strategy alt-symbol rerun.** Acquired aggTrades data must not be retroactively used to revisit R3 / R2 / F1 / D1-A / V2 / G1 / C1 verdicts on alt symbols.
- **No date-window mining.** Exactly **one** complete UTC day for first acquisition. No multi-day backfill. No "scan a range and pick the best day".
- **Date selected before download.** The chosen UTC date must be recorded in the future Phase 4az memo *before* any HTTP request is attempted, so the choice cannot be silently adjusted to favour an outcome.
- **Date choice must not be based on expected market behaviour.** No "pick a high-volume day" or "pick a quiet day". A simple, defensible heuristic (e.g. "the first complete UTC day of the most recent fully-archived month, at least 30 days old") is the recommended posture.
- **One file per day.** The Binance public archive serves one daily aggTrades file per (symbol, date). The acquisition phase must commit to one file per day and record exactly that.

---

## 9. Public archive source plan

The future acquisition phase must consume only the public Binance archive. The following describes what is *expected* from official documentation (no live request was issued by Phase 4ay):

- **Expected family.** `data.binance.vision/data/futures/um/daily/aggTrades/<SYMBOL>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.zip`. Monthly archives also exist at `monthly/aggTrades/...`; daily is preferred for first acquisition because it bounds the size and event-count.
- **File format expected.** A zipped CSV per UTC day. Header conventions and column names must be confirmed against official documentation at acquisition time and recorded in the future manifest's `endpoint_docs_reference`.
- **Checksum file.** Where available, a sibling `<file>.zip.CHECKSUM` containing the SHA256 hex digest. If a checksum file is not published for a given archive variant, the future acquisition memo must record the absence explicitly and either (a) declare the acquisition `research_eligible: false` until a separately authorized "checksum-relaxed" governance memo is on the record, or (b) decline the acquisition.
- **URL / path pattern.** May be documented from official sources in the future Phase 4az memo. Phase 4ay does **not** record a literal URL because no fetch is intended here, and to avoid creating the impression that any URL has been verified by this phase.
- **Archive retention limitations.** Public archive retention extends back to listing for daily aggTrades. The future acquisition phase must select a date within the documented retention window and must not assume availability beyond it.
- **Why public archive is preferred over REST for first acquisition.** (1) The archive is reproducible: the file at a given (symbol, date) is fixed and checksummable, whereas REST results vary across sliding windows. (2) The archive does not require sequence-number bookkeeping, retry policy, or backoff design. (3) The archive is the lowest-credential surface (purely public), entirely consistent with the Phase 4aw allowlist and the Phase 4ax aggTrades-shape guard. (4) The archive avoids the rate-limit and pagination concerns inherent to REST polling.

---

## 10. Integrity gate for future acquisition

The future acquisition phase must satisfy a strict integrity gate before it writes the final raw file or any manifest. The gate is the aggTrades analogue of the Phase 3p §4.7 strict integrity gate (see §14). Required checks:

1. **Source provenance.** Official archive URL is recorded in the manifest's `endpoint_docs_reference`.
2. **File downloaded exactly once.** A single HTTP GET produces a single file in the staging path. Any retry must be deterministic and recorded.
3. **Checksum.** If a `.CHECKSUM` companion is available, it is downloaded into the staging path and verified bit-for-bit against the archive file.
4. **File size.** Nonzero. A predeclared upper bound (e.g. 5 GiB) protects against runaway downloads.
5. **Decompression.** The archive can be decompressed / opened cleanly. No silent corruption, no partial extraction.
6. **Schema validation.** Every row passes the Phase 4ax `validate_aggtrade_payload` validator (REST-shaped, since archive rows are REST-equivalent).
7. **Row count.** Strictly greater than zero.
8. **Timestamp range.** All `T` (trade time) values fall within the requested UTC day, inclusive of `00:00:00.000` and exclusive of the next day's `00:00:00.000`. Boundary entries are recorded as evidence.
9. **Symbol consistency.** Every row has the requested symbol (`BTCUSDT` for first acquisition).
10. **Aggregate trade-id duplicates.** No duplicate `a` (aggregate trade id) within the file unless explicitly documented and handled (the Binance archive is not expected to contain duplicates within a single daily file; any duplicate is treated as an integrity event).
11. **Aggregate trade-id monotonicity.** `a` is monotonically non-decreasing across the file. Any monotonicity exception is recorded as an `OUT_OF_ORDER_EVENT` invalid window (Phase 4aw `InvalidWindowReason.OUT_OF_ORDER_EVENT`) with explicit evidence and sequence numbers.
12. **Price > 0.** Already enforced by `validate_aggtrade_payload`.
13. **Quantity > 0.** Already enforced by `validate_aggtrade_payload`.
14. **`m` boolean present.** Already enforced by `validate_aggtrade_payload` (strict `bool`).
15. **No project data overwrite.** The final `data/microstructure/raw/...` path must not exist before the atomic move from staging.
16. **Invalid windows recorded.** Any integrity event surfaces as a Phase 4aw `InvalidWindow` entry attached to the manifest.
17. **Manifest created.** A `MicrostructureManifest` is written at the final manifest path with `research_eligible=false` and `eligibility_gate_status=pending`.
18. **Eligibility gate fails closed.** Until a separately authorized eligibility-gate phase runs and flips `research_eligible` via its own primitive, any feature / strategy / ML / paper / shadow / live use of the dataset is forbidden.
19. **No feature computation.** The acquisition phase must end before any derived value is computed.

---

## 11. Future staging and storage plan

The future acquisition phase's storage layout (descriptive only; nothing is created by Phase 4ay):

```
data/microstructure/
├── staging/
│   └── microstructure_raw_aggtrades_v001/BTCUSDT/<yyyy>/<mm>/
│       ├── BTCUSDT-aggTrades-<yyyy-mm-dd>.zip.tmp
│       └── BTCUSDT-aggTrades-<yyyy-mm-dd>.zip.CHECKSUM.tmp (if available)
├── raw/
│   └── microstructure_raw_aggtrades_v001/BTCUSDT/<yyyy>/<mm>/
│       ├── BTCUSDT-aggTrades-<yyyy-mm-dd>.zip
│       └── BTCUSDT-aggTrades-<yyyy-mm-dd>.zip.sha256
└── manifests/
    └── microstructure_raw_aggtrades_v001__v001.json
```

Rules (binding for any future Phase 4az):

- **No writes outside `data/microstructure/`.** The Phase 4aw `RawWriter` already enforces this for caller-provided paths; the acquisition phase must apply the same discipline at the archive download layer.
- **Atomic staging-to-final movement.** The download lands in `staging/...` first; the final `raw/...` placement happens only after every integrity check passes. Failure leaves the staging artefact in place for operator inspection and does not create the final file.
- **No overwrite.** A pre-existing final file aborts the run. The future Phase 4az memo must explicitly disclose any need for a re-acquisition pathway.
- **SHA256 pairing.** The final file is paired with a `.sha256` file containing the digest hex.
- **Raw archive preserved.** The acquisition phase does **not** decompress the archive into the final tree. The `.zip` is the raw artefact; per-row schema validation runs against an in-memory or staging-time decompression for gate purposes only.
- **Normalized JSONL / Parquet not created.** The acquisition phase does **not** produce normalized rows under `data/microstructure/normalized/`. Normalization is reserved for a separately authorized future phase.
- **Project data path remains gitignored.** The Phase 4aw `.gitignore` line `data/microstructure/` continues to protect the entire subtree from accidental commits.

---

## 12. Manifest authorization plan

The future Phase 4az manifest must be a Phase 4aw `MicrostructureManifest` with the following required fields:

| Field | Value / source |
| ----- | -------------- |
| `dataset_family` | `microstructure_raw_aggtrades_v001` |
| `version` | `v001` |
| `symbol` | `BTCUSDT` |
| `source` | `binance_data_archive` (literal label; documented in `endpoint_docs_reference`) |
| `endpoint` | logical archive label, e.g. `data.binance.vision/data/futures/um/daily/aggTrades` (descriptive; aggTrades-shaped) |
| `capture_mode` | `historical_archive` |
| `start_time_ms` | minimum `T` observed in the file |
| `end_time_ms` | maximum `T` observed in the file |
| `event_count` | total row count |
| `file_count` | `1` for first acquisition (one daily archive) |
| `files` | one `FileEntry` with `path`, 64-char `sha256` hex, `event_count`, `start_time_ms`, `end_time_ms` |
| `schema_version` | `v001` |
| `endpoint_docs_reference` | URL or repo-relative reference to the official archive documentation, recorded verbatim |
| `capture_config_hash` | SHA256 of the future Phase 4az config (not "secret-hash"; just deterministic config-hash) |
| `code_commit_sha` | the merge commit SHA at acquisition time |
| `invalid_windows` | empty if integrity gate passes; otherwise a list of Phase 4aw `InvalidWindow` entries |
| `retention_warning` | string label if the file falls in the trailing-30-day risk band, otherwise `None` |
| `proxy_warning` | always `None` for archive aggTrades (the archive is the canonical source, not a proxy) |
| `governance_labels` | mapping that includes `stop_trigger_domain: "trade_price_backtest_candidate"` and a `phase_4ax_validator: "v001"` entry for traceability |
| `research_eligible` | **`false`** (default; not flipped by acquisition) |
| `eligibility_gate_status` | **`pending`** (default; eligibility gate not implemented) |

The Phase 4aw `MicrostructureManifest` already enforces all of these defaults. The future Phase 4az memo must additionally specify exactly how the manifest is written atomically and how it is paired with the raw `.zip` file.

---

## 13. Failure and fail-closed rules

The future acquisition phase must fail closed if any of the following occurs:

1. The official archive URL or path cannot be verified against committed documentation references.
2. A checksum companion is expected but missing, or a checksum mismatch occurs.
3. The downloaded file is empty.
4. Decompression fails.
5. Schema validation fails on **any** row (Phase 4ay does **not** authorize a "tiny tolerance" — the aggTrades archive is the canonical source and any malformed row is an integrity event).
6. Symbol mismatch occurs on any row.
7. Timestamp range does not match the selected UTC day (any row with `T` outside the requested 24-hour UTC window is an integrity event).
8. Project data overwrite would occur (a final file at the target path already exists).
9. The manifest cannot be written atomically.
10. Any endpoint call other than the explicit archive GET (e.g. private endpoint, user stream, listenKey, order, account, position, leverage, margin, `forceOrders` REST) is attempted at any point in the run.
11. Any WebSocket is opened.
12. Any feature computation is attempted.
13. Any strategy interpretation appears.
14. Any cooled-down family rescue is implied.

Fail-closed semantics: the staging artefact is preserved for operator inspection; no final file is moved into `data/microstructure/raw/...`; no manifest is written; the run records the failure in its log; the operator decides whether to retry, abandon, or escalate.

---

## 14. Relationship to Phase 3p §4.7 strict integrity gate

Phase 3p §4.7 (committed at `docs/00-meta/implementation-reports/2026-04-30_phase-3p_5m-diagnostics-data-requirements-and-execution-plan.md`, lines 193–205) defines a strict integrity gate for kline datasets. It requires: no gaps; monotone timestamps; boundary alignment; close-time consistency; OHLC sanity; volume sanity; symbol consistency; interval consistency; and date-range coverage. Forward-fill, interpolation, and silent omission are explicitly forbidden, per `docs/04-data/data-requirements.md` forbidden patterns. Phase 3q, Phase 4ac, and Phase 4i applied this gate verbatim.

Phase 3p §4.7 is a *kline* gate. AggTrades are not klines. The aggTrades equivalent of the §4.7 discipline is the gate specified in §10 above:

| Phase 3p §4.7 (kline) | Phase 4ay aggTrades equivalent (this memo §10) |
| --------------------- | ----------------------------------------------- |
| No gaps in the bar stream | Aggregate trade IDs monotonically non-decreasing; duplicates treated as integrity events |
| Monotone timestamps | `T` is non-decreasing within the file |
| Boundary alignment (`open_time mod 300000 = 0`) | Trade-time range matches the requested UTC day exactly |
| Close-time consistency | Not applicable (aggTrades have no close-time) |
| OHLC sanity (`low ≤ open ≤ high`, all > 0) | `price > 0` and `quantity > 0` (Phase 4ax validator) |
| Volume sanity | `quantity > 0` and `m` strict bool (Phase 4ax validator) |
| Symbol consistency | All rows have requested symbol (Phase 4ax validator + acquisition gate) |
| Interval consistency | Not applicable (aggTrades have no interval); replaced by archive-day consistency |
| Date-range coverage | Source URL records the requested UTC day; row range matches it; absent or partial coverage is an integrity event |
| No forward-fill / interpolation / silent omission | No row patching; any anomaly recorded verbatim as an `InvalidWindow` |

The Phase 4aw `MicrostructureManifest` and `InvalidWindow` taxonomy were designed for exactly this purpose. The Phase 4ax aggTrades validator was designed to enforce the row-shape constraints. The gate composes Phase 4ax + Phase 4aw without modifying either.

The future Phase 4az memo must enumerate every check from §10 of this memo and attach pass / fail evidence to the manifest. Any unenumerated relaxation requires a separately authorized governance memo.

---

## 15. Relationship to §11.6 cost realism

`§11.6 = 8 bps slippage per side; round-trip = 16 bps` is a **trading cost** lock derived from Phase 2w R2 cost-fragility evidence and reaffirmed in every subsequent retained-evidence phase. AggTrades acquisition is **market-data infrastructure**, not a trading result.

Therefore:

- **No fee assumption is changed.** The acquisition phase does not compute realised P&L.
- **No slippage assumption is changed.** The acquisition phase does not simulate fills.
- **No funding assumption is changed.** The acquisition phase does not compute funding.
- **§11.6 remains 8 bps per side.** This lock is unaffected by Phase 4ay or by any future Phase 4az.
- **No acquired data may be used to weaken cost assumptions** without a separately authorized methodology phase that explicitly amends §11.6 with its own evidence.

This is a binding constraint: any future feature, regime study, or strategy hypothesis that treats acquired aggTrades data as evidence for relaxing §11.6 (or any other locked cost constant) is forbidden until a separate cost-methodology memo is on the record. Phase 4ay does not propose such a memo.

---

## 16. Relationship to M0 and no-rescue

Phase 4ak adopted the twelve-clause M0 mechanism-admissibility gate and the post-null cooldown rule as binding prospective governance for any future research lane. Phase 4al refined the no-rescue rule and the data-resolution hierarchy. The retained-verdict ledger (H0 anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remains binding.

Phase 4ay restates these constraints for clarity:

- **Data acquisition is infrastructure only.** Acquiring real aggTrades does not by itself license any edge claim, any feature implementation, any strategy candidate, or any verdict revision.
- **No cooled-down family is reopened.** R2 / F1 / D1-A / V2 / G1 / C1 all remain in their current cooled-down posture.
- **No R3 / R2 / V1 rescue.** No old strategy is rerun or revisited on aggTrades data.
- **No old-strategy alt-symbol rerun.** Even if alt-symbol aggTrades data is acquired in a future memo, it must not be used to revisit any old verdict.
- **No 5m thread reopening.** Phase 3t remains the operational closure of the 5m research thread. AggTrades acquisition is finer-resolution than 5m and must not be silently used to bypass the 5m closure.
- **Future feature work must separately clear M0.** Any hypothesis that proposes to derive a strategy signal from aggTrades data must satisfy the Phase 4ak twelve-clause M0 gate, the Phase 4l 18-requirement validity gate, and the Phase 4t 10-dimension scoring matrix in a separately authorized hypothesis-spec memo *before* any feature is computed.

---

## 17. Future acquisition implementation options

Three options are available for what the operator could do after Phase 4ay merges. Phase 4ay does **not** activate any of them.

### Option A — Future docs-and-code Phase 4az: public archive acquisition, BTCUSDT, one UTC day

**Status:** allowable but **not activated** by Phase 4ay.

A future Phase 4az would: implement an archive-fetch helper (HTTP GET against `data.binance.vision`); apply the §10 integrity gate; create the staging-then-final tree under `data/microstructure/`; write one `MicrostructureManifest` with `research_eligible=false` and `eligibility_gate_status=pending`; preserve the raw `.zip` and `.zip.sha256` paired files; and stop. No normalization. No features. No strategies.

### Option B — Remain paused

**Status:** procedurally acceptable.

The operator may decide that even a single-day archive acquisition is premature and that the project should remain paused. This option preserves every retained verdict and every project lock without further infrastructure expansion.

### Option C — Narrower docs-only acquisition-risk review

**Status:** allowable but **not activated** by Phase 4ay.

A future docs-only memo could enumerate acquisition-time risks more deeply (e.g. retention edge cases; checksum availability gaps; storage / disk / bandwidth budget; reproducibility of the daily file across re-downloads; parity with the public-data repo's documented schema) without committing to acquisition. This is a "double-check before crossing the boundary" option.

### Recommendation

The conservative recommendation is **Option B (remain paused)** as primary and **Option C (narrower docs-only acquisition-risk review)** as conditional secondary if the operator wants more pre-flight safety. **Option A (Phase 4az public archive acquisition)** is *allowable* but should be treated as a deliberate operator decision — not a default next step — and is **not authorized by Phase 4ay**.

---

## 18. Explicit non-recommendations

The following are explicitly **not** recommended and **not** authorized by Phase 4ay:

- No immediate live REST polling of `/fapi/v1/aggTrades`.
- No WebSocket capture of `<symbol>@aggTrade`.
- No order-book data acquisition.
- No OI / funding acquisition (existing Phase 2 / Phase 4i / Phase 4ac coverage stands).
- No `forceOrder` proxy acquisition.
- No ETHUSDT first acquisition unless separately authorized in a successor memo.
- No multi-day backfill.
- No full historical backfill.
- No feature computation derived from any acquired data.
- No ML model training on any acquired data.
- No strategy candidate derived from acquired data.
- No paper / shadow / live-readiness / deployment / exchange-write work.
- No production-key creation, authenticated APIs, private endpoints, user stream, listenKey lifecycle, MCP, Graphify, `.mcp.json`, or credentials work.
- No reopening of the 5m research thread.
- No revival of cooled-down R2 / F1 / D1-A / V2 / G1 / C1 first-spec families.

---

## 19. Implementation / governance review

### What changed?

Phase 4ay added two new docs files under `docs/00-meta/implementation-reports/` (this memo and the closeout) and narrowly updated `docs/00-meta/current-project-state.md` (Phase 4ay narrative paragraph + new "Current phase:" block; prior Phase 4ax block preserved as historical context).

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md` unchanged).
- No Phase 4ak / 4al / 4j / 3r / 3v / 3w / 3p §4.7 governance.
- No Phase 4aw scaffold module.
- No Phase 4ax aggTrades skeleton module.
- No `data/manifests/` content.
- No `data/raw/`, `data/normalized/`, `data/derived/`, or `data/research/` content.
- No strategy spec, backtest plan, validation checklist, runtime doc, or live-readiness doc.
- No existing test or script.
- No `pyproject.toml`, `README.md`, or `.gitignore`.
- The `data/microstructure/` directory does not exist after Phase 4ay.

### Were any locks, verdicts, or safety boundaries affected?

No. Phase 4ay is a docs-only authorization-boundary memo. All locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) and all verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, source files, existing data, manifests, or tests modified?

No. None of the existing scripts under `scripts/` was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4ay paragraph addition.

### Mergeability

The phase introduces only two new docs files and a narrow `current-project-state.md` update. It does not touch source, tests, scripts, data, manifests, or any other governance file. It is mergeable as docs-only.

---

## 20. Research interpretation review

### 1. What did this phase prove?

That the project can author a precise authorization-boundary memo for a possible future first aggTrades archive acquisition without acquiring any data, contacting any endpoint, opening any WebSocket, downloading any archive, writing under any project data path, creating any manifest, modifying any source / test / script / governance file, or authorizing any successor phase. It proved that the Phase 4aw scaffold and the Phase 4ax aggTrades-only collector skeleton compose cleanly with a documented Phase 3p §4.7-style strict integrity gate, a documented staging-then-final atomic move, a documented manifest contract, and a documented fail-closed rule set — with every constraint expressed in writing before the work begins.

### 2. What did this phase not prove?

Anything about Binance public-archive availability at acquisition time, archive bit-fidelity in practice, or aggTrades data quality. No archive URL was verified live. No file was downloaded or hashed. No row was inspected. No edge claim is supported by any aggTrades data, since none exists in the project. No historical strategy verdict changed. No project lock changed.

### 3. Which original questions did it answer?

- "Under what exact constraints, integrity gates, storage rules, manifest rules, symbol/date limits, validation checks, and governance boundaries could a future phase safely acquire the first public Binance aggTrades archive sample — without creating strategy work, feature work, ML, paper/live capability, or old-strategy rescue?" → **Recorded in writing** by §7–§16 of this memo.
- "Is the Phase 4ax aggTrades skeleton sufficient to validate archive rows once acquired?" → **Yes** for the row-shape gate; the acquisition-time gate (§10) layers ordering / range / file-level checks on top.
- "Does Phase 3p §4.7 still apply to aggTrades?" → **Yes in spirit**, with the per-row equivalents recorded in §14.
- "Does §11.6 cost realism survive aggTrades acquisition?" → **Yes**, §15. Acquired data does not by itself license any cost-assumption change.
- "Does M0 still gate any future feature derived from acquired aggTrades?" → **Yes**, §16. No exception is created.

### 4. Which original questions remain open?

- The exact archive URL and file format will need to be verified against official Binance documentation at acquisition time, not by Phase 4ay.
- Whether `.CHECKSUM` companions are uniformly available for daily aggTrades archives is documented as an *acquisition-time check*, not as an answered question.
- Whether the project's storage budget can accommodate first-acquisition aggTrades plus future expansion is recorded as a future Phase 4az consideration.
- Whether the eligibility-gate primitive should ever be implemented is deferred to a separately authorized future phase.
- Whether any aggTrades-derived feature carries edge under §11.6 cost realism is not addressed by Phase 4ay; a future feature memo must satisfy M0 and the Phase 4m 18-requirement validity gate first.

### 5. What does it mean for strategy research?

Plumbing only. No strategy candidate is created. No cooled-down family (R2 / F1 / D1-A / V2 / G1 / C1) is reopened. No 5m thread reopening. No old-strategy alt-symbol rerun. The Phase 4m 18-requirement validity gate, the Phase 4t 10-dimension scoring matrix, and the Phase 4ak twelve-clause M0 gate remain binding for any future hypothesis.

### 6. What does it mean for governance?

Nothing changes. M0 (Phase 4ak), the Phase 4al refined no-rescue rule, the Phase 4j §11 OI subset governance, the Phase 3r §8 mark-price gap governance, the Phase 3v §8 stop-trigger-domain governance, the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance, and §11.6 / §1.7.3 project-level locks all remain verbatim. The Phase 4ay memo is itself non-governing: it records a *framework* for a possible future acquisition phase, not a binding rule that takes effect by being merged.

### 7. What is the clean next step?

After operator review and merge, **remain paused** is the primary recommendation. If the operator decides that the boundary should be crossed, the cleanest path is a separately authorized future Phase 4az that implements §10–§13 of this memo verbatim. A narrower docs-only acquisition-risk review (Option C) is also acceptable as a final pre-flight check before authorizing Phase 4az.

### 8. What should we not do yet?

- Do not download any archive.
- Do not contact any Binance endpoint.
- Do not open any WebSocket.
- Do not create the `data/microstructure/` directory.
- Do not create any manifest.
- Do not implement any REST or WebSocket client.
- Do not implement any collector beyond the Phase 4ax skeleton.
- Do not implement any normalizer, replay, eligibility-gate execution, healthcheck, dashboard hook, feature, ML model, or strategy candidate.
- Do not approach paper / shadow, live-readiness, deployment, exchange-write, or production keys.
- Do not authorize a successor phase.

---

## 21. Explicit preservation of verdicts, locks, and no-rescue constraints

Phase 4ay preserves verbatim:

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m thread** — OPERATIONALLY CLOSED.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

Project locks preserved verbatim:

- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade, 2× leverage cap, one position max, mark-price stops where applicable.
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent recorded in §14 of this memo).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w.
- Phase 4ak (M0 twelve-clause gate, post-null cooldown rule, cooled-down families list, memo template).
- Phase 4al (refined no-rescue rule + §13 boundary + §14 hierarchy).
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax results.

No new lock is introduced. No existing lock is loosened. M0 admissibility and the post-null cooldown rule remain binding prospectively for any future research lane.

**Recommended state remains paused. No successor phase is authorized.**
