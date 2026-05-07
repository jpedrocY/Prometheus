# Phase 4ay — Merge Closeout

**Phase identity:** Phase 4ay — AggTrades Public Archive Acquisition Authorization Memo.
**Type:** docs-only data-acquisition authorization / boundary memo.
**Date:** 2026-05-07.
**Action:** merge into `main`.

---

## 1. Merge purpose

To merge the Phase 4ay docs-only authorization-boundary memo from the Phase 4ay feature branch into `main`. The memo defines the exact constraints under which a future, separately authorized phase could safely acquire a first, tightly scoped public Binance USDⓈ-M Futures aggTrades archive sample on top of the Phase 4aw scaffold and the Phase 4ax aggTrades-only collector skeleton.

The merge does **not** acquire data, contact endpoints, open WebSockets, download archives, implement REST clients, implement WebSocket clients, implement collectors, modify the Phase 4ax aggTrades skeleton, implement order-book reconstruction, implement deterministic replay, implement normalizers, implement eligibility-gate execution, implement feature computation, run backtests, run historical strategy scripts, run simulations, or modify source / tests / scripts / data / manifests / governance / verdicts / locks / `.gitignore`. It does **not** create the `data/microstructure/` directory, write under any project data path, or create real project manifests. It does **not** authorize any successor phase.

---

## 2. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4ay/aggtrades-public-archive-acquisition-authorization` |

---

## 3. SHAs

| Item | SHA |
| ---- | --- |
| `main` before merge | `436660e4e9578b6086f6a73367e2e68cd83ead1b` |
| Phase 4ay memo commit | `efae11002290a2090b0fd554886a041dee01df52` |
| Phase 4ay closeout commit | `14ab6b979d1abf0f5642e93ccf4b0563633b63a8` |
| Source branch HEAD | `14ab6b979d1abf0f5642e93ccf4b0563633b63a8` |
| Source / origin in sync at start | yes |
| Merge method | `git merge --no-ff --no-commit` |

The merge commit SHA appears in the operator report after `git commit` and `git push`.

---

## 4. Files brought forward by the merge

3 file changes, 1,018 insertions, 0 deletions.

**Added (2 new files):**

```
docs/00-meta/implementation-reports/2026-05-07_phase-4ay_aggtrades-public-archive-acquisition-authorization.md
docs/00-meta/implementation-reports/2026-05-07_phase-4ay_closeout.md
```

**Modified (1 narrow update):**

```
docs/00-meta/current-project-state.md   (Phase 4ay narrative paragraph + new "Current phase:" block; prior Phase 4ax block preserved as historical context)
```

**Files NOT modified by the merge:**

- No file under `src/prometheus/`.
- No file under `tests/`.
- No file under `scripts/`.
- No existing dataset manifest under `data/manifests/`.
- No existing trade log under `data/derived/backtests/`.
- No existing strategy spec, validation checklist, runtime doc, or governance memo (M0 governance, §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak, Phase 4al, Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax memos all unchanged).
- No `pyproject.toml`, `README.md`, or `.gitignore` change.

---

## 5. Phase 4ay was docs-only

**Confirmed.** Phase 4ay is a docs-only data-acquisition authorization / boundary memo. Its scope was strictly limited to:

- one new 21-section authorization memo;
- one new closeout file;
- one narrow `current-project-state.md` update.

No code, tests, scripts, data, manifests, governance docs, retained verdicts, project locks, or `.gitignore` were modified.

---

## 6. Phase 4ay authorization-boundary result

The 21-section memo records, before any acquisition:

- the executive summary, scope, repository verification, and docs-only methodology;
- the Phase 4ax baseline preserved verbatim;
- why a separate authorization memo was necessary (real external data crossing; project data paths created; manifests required; checksum / retention completeness; future-feature implications; explicit non-strategy framing);
- the proposed conservative future acquisition target;
- the candidate symbol / date policy;
- the public archive source plan;
- the strict integrity gate (19 explicit checks; aggTrades equivalent of Phase 3p §4.7);
- the future staging-and-storage plan;
- the manifest authorization plan;
- 14 explicit fail-closed rules;
- a side-by-side mapping of Phase 3p §4.7 kline checks onto aggTrades equivalents;
- §11.6 cost-realism preservation;
- M0 + post-null-cooldown preservation;
- three future implementation options (A docs-and-code Phase 4az; B remain paused; C narrower docs-only acquisition-risk review);
- explicit non-recommendations;
- implementation / governance review;
- 8-question research interpretation review in plain English;
- explicit preservation of verdicts, locks, and no-rescue constraints.

The memo's primary recommendation is **remain paused (Option B)**; conditional secondary is a narrower docs-only acquisition-risk review (Option C); Option A (Phase 4az public archive acquisition) is *allowable* but **not authorized** by Phase 4ay.

### Future acquisition target

If a future phase is separately authorized, the recommended target is:

- **Dataset family:** `microstructure_raw_aggtrades_v001`.
- **Market:** Binance USDⓈ-M Futures.
- **Source:** public Binance archive only — preferably `data.binance.vision`.
- **Symbol:** **BTCUSDT only** for first acquisition.
- **Timeframe:** one complete UTC daily archive file, recommended at least 30 days before acquisition date so retention-window limitations are unlikely to bite.
- **Acquisition mode:** **archive only** — explicitly **not** REST polling and **not** WebSocket capture.
- **`research_eligible` default:** `false`.
- **`eligibility_gate_status` default:** `pending`.

Phase 4ay does **not** acquire this data. Phase 4ay does **not** authorize Phase 4az. The exact date, the exact archive URL, the exact file size, the exact checksum, the exact event count, and the exact final landing path are all to be selected and recorded at acquisition time in a future Phase 4az memo (if ever authorized).

### Candidate symbol / date policy

- **BTCUSDT first.** ETHUSDT and any alt symbol are excluded from the first acquisition unless separately authorized in a successor memo.
- **No alt-symbol mining.** Symbol choice anchored in §1.7.3 project-level scope and prior alt-symbol governance.
- **No old-strategy alt-symbol rerun.** Acquired aggTrades data must not be retroactively used to revisit R3 / R2 / F1 / D1-A / V2 / G1 / C1 verdicts.
- **No date-window mining.** Exactly one complete UTC day; no multi-day backfill; no "scan a range and pick the best day".
- **Date selected before download.** The chosen UTC date must be recorded in the future Phase 4az memo *before* any HTTP request is attempted.
- **Date choice must not be based on expected market behaviour.** A simple, defensible heuristic (e.g. "first complete UTC day of the most recent fully-archived month, at least 30 days old") is the recommended posture.
- **One file per day.** The Binance public archive serves one daily aggTrades file per (symbol, date).

### Public archive source plan

- **Expected family.** `data.binance.vision/data/futures/um/daily/aggTrades/<SYMBOL>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.zip`. Monthly archives at `monthly/aggTrades/...` exist; daily preferred for first acquisition.
- **File format expected.** Zipped CSV per UTC day. Column conventions to be confirmed against official documentation at acquisition time and recorded in the manifest's `endpoint_docs_reference`.
- **Checksum file.** Sibling `<file>.zip.CHECKSUM` containing the SHA256 hex digest, where published. If a checksum file is not published for a given archive variant, the future acquisition memo must record the absence explicitly and either (a) declare `research_eligible: false` until a separately authorized "checksum-relaxed" governance memo is on the record, or (b) decline the acquisition.
- **URL / path pattern.** May be documented from official sources in the future Phase 4az memo. Phase 4ay does **not** record a literal URL because no fetch was intended and to avoid implying that any URL has been verified.
- **Archive retention.** Public archive retention extends back to listing for daily aggTrades. The future acquisition phase must select a date within the documented retention window.
- **Why archive over REST.** Reproducibility (the file at a given (symbol, date) is fixed and checksummable); no sequence-number bookkeeping; lowest credential surface (purely public); no rate-limit / pagination concern.

### Strict integrity gate (19 checks)

Per memo §10:

1. Source provenance recorded in `endpoint_docs_reference`.
2. File downloaded exactly once into staging path.
3. Checksum verified bit-for-bit when a `.CHECKSUM` companion is available.
4. File size nonzero with predeclared upper bound.
5. Decompression succeeds cleanly.
6. Every row passes the Phase 4ax `validate_aggtrade_payload` validator.
7. Row count strictly > 0.
8. Timestamp range matches the requested UTC day exactly.
9. Symbol consistency (every row has the requested symbol).
10. No duplicate aggregate trade IDs unless explicitly documented and handled.
11. Aggregate trade-id monotonicity; exceptions recorded as `OUT_OF_ORDER_EVENT` invalid windows.
12. Price > 0 (Phase 4ax validator).
13. Quantity > 0 (Phase 4ax validator).
14. `m` strict bool present (Phase 4ax validator).
15. No project data overwrite.
16. Invalid windows recorded as Phase 4aw `InvalidWindow` entries.
17. Manifest written with `research_eligible=false` and `eligibility_gate_status=pending`.
18. Eligibility gate fails closed until a separately authorized phase runs.
19. No feature computation.

### Future staging and storage plan

```
data/microstructure/
├── staging/
│   └── microstructure_raw_aggtrades_v001/BTCUSDT/<yyyy>/<mm>/
├── raw/
│   └── microstructure_raw_aggtrades_v001/BTCUSDT/<yyyy>/<mm>/
└── manifests/
    └── microstructure_raw_aggtrades_v001__v001.json
```

Rules: no writes outside `data/microstructure/`; atomic staging-to-final movement; no overwrite; SHA256 pairing; raw `.zip` preserved (no decompression into final tree); no normalized JSONL / Parquet created; project data path remains gitignored.

### Manifest authorization plan

Every Phase 4aw `MicrostructureManifest` field is enumerated in the memo with required values: `dataset_family=microstructure_raw_aggtrades_v001`; `version=v001`; `symbol=BTCUSDT`; `source=binance_data_archive`; `endpoint=data.binance.vision/data/futures/um/daily/aggTrades` archive label; `capture_mode=historical_archive`; `start_time_ms` = min observed `T`; `end_time_ms` = max observed `T`; `event_count` = total row count; `file_count=1`; `files` with one `FileEntry` (path; 64-char `sha256` hex; `event_count`; `start_time_ms`; `end_time_ms`); `schema_version=v001`; `endpoint_docs_reference` recorded verbatim; `capture_config_hash` = SHA256 of future Phase 4az config; `code_commit_sha` = merge commit SHA at acquisition time; `invalid_windows` empty if integrity gate passes else list of `InvalidWindow` entries; `retention_warning` string label if file in trailing-30-day risk band else `None`; `proxy_warning=None`; `governance_labels` includes `stop_trigger_domain=trade_price_backtest_candidate` and `phase_4ax_validator=v001`; `research_eligible=false`; `eligibility_gate_status=pending`.

### Fail-closed rules (14)

Per memo §13: official URL not verifiable; checksum missing or mismatch; empty file; decompression failure; **schema validation failure on any row** (no tiny tolerance); symbol mismatch; timestamp range outside requested UTC day; project data overwrite; manifest cannot be written atomically; any non-archive endpoint call attempted; any WebSocket opened; any feature computation attempted; any strategy interpretation appears; any cooled-down family rescue implied. On fail-closed: staging artefact preserved for operator inspection; no final file moved; no manifest written; operator decides whether to retry, abandon, or escalate.

### Phase 3p §4.7 mapping to aggTrades

Per memo §14, Phase 3p §4.7 (kline strict integrity gate) maps onto aggTrades as follows:

| Phase 3p §4.7 (kline) | Phase 4ay aggTrades equivalent |
| --------------------- | ------------------------------ |
| No gaps in bar stream | Aggregate trade IDs monotonically non-decreasing; duplicates treated as integrity events |
| Monotone timestamps | `T` is non-decreasing within the file |
| Boundary alignment | Trade-time range matches requested UTC day exactly |
| Close-time consistency | Not applicable (aggTrades have no close-time) |
| OHLC sanity | `price > 0` and `quantity > 0` (Phase 4ax validator) |
| Volume sanity | `quantity > 0` and `m` strict bool (Phase 4ax validator) |
| Symbol consistency | All rows have requested symbol |
| Interval consistency | Replaced by archive-day consistency |
| Date-range coverage | Source URL records requested UTC day; row range matches it |
| No forward-fill / interpolation / silent omission | No row patching; any anomaly recorded verbatim as an `InvalidWindow` |

Phase 3p §4.7 itself is unchanged. Phase 4ay records the aggTrades equivalent for use by any future Phase 4az.

### §11.6 cost-realism preservation

Per memo §15: `§11.6 = 8 bps slippage per side; round-trip = 16 bps` is unchanged. AggTrades acquisition is **market-data infrastructure**, not a trading result. No fee assumption is changed; no slippage assumption is changed; no funding assumption is changed; no acquired data may be used to weaken cost assumptions without a separately authorized methodology phase. Any future feature, regime study, or strategy hypothesis that treats acquired aggTrades data as evidence for relaxing §11.6 (or any other locked cost constant) is forbidden until a separate cost-methodology memo is on the record. Phase 4ay does **not** propose such a memo.

### M0 and no-rescue preservation

Per memo §16: data acquisition is infrastructure only; no cooled-down family is reopened (R2 / F1 / D1-A / V2 / G1 / C1 all remain in their current cooled-down posture); no R3 / R2 / V1 rescue; no old-strategy alt-symbol rerun; no 5m thread reopening (Phase 3t closure preserved); future feature work must separately clear the Phase 4ak twelve-clause M0 gate, the Phase 4l 18-requirement validity gate, and the Phase 4t 10-dimension scoring matrix in a separately authorized hypothesis-spec memo *before* any feature is computed.

---

## 7. Implementation / governance review

### What changed?

- Two new docs files (memo + closeout) under `docs/00-meta/implementation-reports/`.
- One narrow `current-project-state.md` update.

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md` unchanged).
- No Phase 4ak / 4al / 4j / 3p §4.7 / 3r / 3v / 3w governance.
- No Phase 4aw scaffold module.
- No Phase 4ax aggTrades skeleton module.
- No data manifest under `data/manifests/`.
- No data file under `data/raw/`, `data/normalized/`, `data/derived/`, or `data/research/`.
- No strategy spec, backtest plan, validation checklist, runtime doc, or live-readiness doc.
- No existing test or script.
- No `pyproject.toml`, `README.md`, or `.gitignore`.

### Were any locks, verdicts, or safety boundaries affected?

No. Phase 4ay is a docs-only authorization-boundary memo. All locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) and all verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, source files, existing data, manifests, or tests modified?

No. None of the existing scripts under `scripts/` was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4ay paragraph addition.

### Mergeability

The phase introduces only two new docs files and a narrow `current-project-state.md` update. It does not touch source, tests, scripts, data, manifests, or any other governance file. The merge is a clean automatic merge (no conflicts) with `--no-ff` to preserve the Phase 4ay commit history.

---

## 8. Research interpretation review

### What did this phase prove?

That the project can author a precise authorization-boundary memo for a possible future first aggTrades archive acquisition without acquiring any data, contacting any endpoint, opening any WebSocket, downloading any archive, writing under any project data path, creating any manifest, modifying any source / test / script / governance file, or authorizing any successor phase. It proved that the Phase 4aw scaffold and the Phase 4ax aggTrades-only collector skeleton compose cleanly with a documented Phase 3p §4.7-style strict integrity gate, a documented atomic staging-then-final move, a documented manifest contract, and a documented fail-closed rule set — with every constraint expressed in writing before the work begins.

### What did this phase NOT prove?

Anything about Binance public-archive availability at acquisition time, archive bit-fidelity in practice, or aggTrades data quality. No archive URL was verified live. No file was downloaded or hashed. No row was inspected. No edge claim is supported by any aggTrades data, since none exists in the project. No historical strategy verdict changed. No project lock changed.

### What does this mean for strategy research?

Plumbing only. No strategy candidate is created. No cooled-down family (R2 / F1 / D1-A / V2 / G1 / C1) is reopened. No 5m thread reopening. No old-strategy alt-symbol rerun. The Phase 4m 18-requirement validity gate, the Phase 4t 10-dimension scoring matrix, and the Phase 4ak twelve-clause M0 gate remain binding for any future hypothesis derived from microstructure data.

### What does this mean for governance?

Nothing changes. M0 (Phase 4ak), the Phase 4al refined no-rescue rule, the Phase 4j §11 OI subset governance, the Phase 3p §4.7 strict integrity gate, the Phase 3r §8 mark-price gap governance, the Phase 3v §8 stop-trigger-domain governance, the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance, and §11.6 / §1.7.3 project-level locks all remain verbatim. The Phase 4ay memo is itself non-governing: it records a *framework* for a possible future acquisition phase, not a binding rule that takes effect by being merged.

### Clean next step

After the merge, **remain paused** is the primary recommendation. If the operator decides that the boundary should be crossed, the cleanest path is a separately authorized future Phase 4az that implements memo §10–§13 verbatim. A narrower docs-only acquisition-risk review (Option C) is also acceptable as a final pre-flight check before authorizing Phase 4az.

---

## 9. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other.
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

No verdict is revised by this merge.

---

## 10. Preserved project locks

- M0 governance remains binding prospectively only.
- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops where applicable.
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent recorded by Phase 4ay).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy spec.
- Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy spec.
- Phase 4w C1 backtest-plan methodology.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4am §11.A audit findings.
- Phase 4an inventory result.
- Phase 4ao harmonization result.
- Phase 4ap forensic plan.
- Phase 4aq computation result preserved as descriptive evidence only.
- Phase 4ar interpretation result preserved as descriptive interpretation only.
- Phase 4as mechanism-map result preserved as docs-only reset evidence only.
- Phase 4at availability / capture-feasibility result preserved as docs-only feasibility evidence only.
- Phase 4au capture-design result preserved as docs-only design evidence only.
- Phase 4av implementation-plan result preserved as docs-only planning evidence only.
- Phase 4aw scaffold result preserved as scaffold-only infrastructure evidence only.
- Phase 4ax aggTrades skeleton result preserved as collector-skeleton infrastructure evidence only.
- Phase 4ay authorization-boundary result preserved as docs-only acquisition-boundary evidence only.

No new lock is introduced. No existing lock is loosened.

---

## 11. No-rescue constraints (preserved)

- No R3-prime / R3 next-spec / R3 rescue / baseline-of-record revision.
- No R1a-prime / R1a promotion to leading.
- No R1b-narrow-prime / R1b-narrow promotion to leading.
- No R2-prime / R2 rescue / R2 cheaper-cost rerun.
- No H0-prime / framework-anchor revision.
- No F1-prime / F1 rescue / F1 profitable-subset rescue.
- No D1-A-prime / D1-A extra-filter / D1-B / V1-D1 hybrid / F1-D1 hybrid.
- No V2-prime / V2-narrow / V2-relaxed / V2 hybrid.
- No G1-prime / G1-narrow / G1-extension / G1 hybrid / G1 classifier relaxation.
- No C1-prime / C1-narrow / C1-extension / C1 hybrid.
- No cross-strategy hybrid of any kind.
- No 5m thread reopening.
- No 5m strategy / hybrid / retained-evidence successor.
- No conversion of Phase 4aq forensic numbers, Phase 4l V2 forensic numbers, Phase 4r G1 active-fraction numbers, or Phase 4x C1 forensic numbers into parameter-selection inputs.
- No M0 amendment derived from Phase 4ay reasoning.

---

## 12. Successor authorisation

**No successor phase is authorized by this merge.**

In particular, the merge does NOT authorize:

- Phase 4az,
- Phase 5,
- Phase 4 canonical,
- data acquisition (real aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book),
- Binance endpoint calls,
- public-archive downloads,
- WebSocket connections,
- live REST implementation,
- live WebSocket implementation,
- data-capture implementation,
- order-book reconstruction implementation,
- replay implementation,
- eligibility-gate execution,
- feature implementation,
- ML model creation,
- strategy candidate creation,
- entry / exit design,
- old-strategy alt-symbol reruns,
- R3 / R2 / V1-arc rescue,
- 5m research thread reopening,
- paper / shadow,
- live-readiness,
- deployment,
- exchange-write,
- production keys,
- authenticated APIs,
- private endpoints,
- user stream,
- MCP, Graphify, `.mcp.json`,
- credentials.

Any successor phase requires a separate operator authorization brief. Phase 4az (whether docs-only narrower acquisition-risk review per Option C, or docs-and-code public archive acquisition per Option A) is documented as a possible future path but is **not** activated by this merge.

---

## 13. Recommended state

**Recommended state remains paused.** The Phase 4ay authorization-boundary memo is now available on `main` for any future separately-authorized phase to consult. No further work should occur until the operator separately authorizes a future phase.

---

## 14. Final note

This merge-closeout is preserved alongside the Phase 4ay memo and the Phase 4ay closeout under `docs/00-meta/implementation-reports/`. The merge is intentionally `--no-ff` so the Phase 4ay commit history is preserved and the boundary between Phase 4ax (aggTrades skeleton) and Phase 4ay (authorization memo) remains visible in `git log`.

**Phase 4ay is now merged into `main`. No next phase is authorized.**
