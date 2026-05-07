# Phase 4av — Public-Only Microstructure Capture Implementation Plan

## Phase identity

- Phase ID: **4av**.
- Phase title: **Public-Only Microstructure Capture
  Implementation Plan**.
- Type: docs-only implementation-planning memo.
- Authority: separately operator-authorised as a docs-only
  implementation-planning phase only.
- Branch: `phase-4av/public-only-microstructure-capture-implementation-plan`.
- Base SHA (main at branch creation):
  `6e9521bbba5f2af8ca19f4789de4c9034c7a301a`.
- Phase 4av memo commit SHA: recorded in this phase's closeout
  once this memo is committed.

---

## 1. Executive summary

Phase 4au specified a complete docs-only public-only Binance
microstructure capture design covering nine cooperating
components, a thirteen-endpoint allowlist, an explicit denylist,
seven proposed dataset family designs, a four-layer storage
model, per-family schemas, manifest fields, a seventeen-trigger
invalid-window taxonomy, a ten-check eligibility gate,
deterministic replay, a local-only dashboard, and a
security / runtime-separation boundary. Phase 4au
**did not implement any of it.**

Phase 4av is the separately-authorised next docs-only phase
recommended (but not authorised) by Phase 4au. Its purpose is
to translate the Phase 4au design specification into a
**precise, file-by-file implementation plan** covering future
file / module layout, CLI surface, config sections, manifest
implementation steps, schema implementation order, invalid-
window error-class enumeration, eligibility-gate
implementation steps, deterministic-replay implementation
steps, local-order-book reconstruction implementation steps,
collector implementation order, test matrix, failure-mode
matrix, validation commands, stop conditions, branch strategy,
security / credential plan, runtime-separation plan, and
symbol / scope plan — **without implementing any of it**.

Phase 4av does **not** acquire data, call any Binance
endpoint, open any WebSocket, download any archive, modify
endpoint code, implement capture / replay / order-book
reconstruction / features, run scripts, modify manifests,
modify governance, modify retained verdicts or project locks,
create any source / test / data / manifest / dataset directory
artefact, modify `.gitignore`, or authorise any successor
phase.

The recommendation is to **remain paused** unless the operator
separately authorises a future phase. The cleanest possible
separately-authorised next docs-and-code phase, *if and only
if* the operator chooses one, would be **Phase 4aw — Public-
Only Microstructure Capture Scaffold Implementation** (limited
scope: scaffold + config validation + allowlist / denylist +
raw writer + manifest skeleton + invalid-window enum + tests;
no endpoint calls, no archive downloads, no WebSockets, no
data acquisition). **Phase 4aw is not authorised by Phase 4av.**

All retained verdicts and project locks are preserved verbatim.
M0 governance, the post-null cooldown rule, the cooled-down
families list, the Phase 4al refined no-rescue rule, the
Phase 4t 10-dimension scoring matrix, the Phase 4m 18-
requirement validity gate, the Phase 3t 5m closure, §11.6, and
§1.7.3 are all binding and unchanged.

---

## 2. Scope and explicit non-scope

### In scope

- A docs-only **implementation plan** that translates Phase 4au
  §6–§35 into a precise file-by-file plan a future
  implementation phase could safely follow.
- A **proposed future file / module plan** (§8) under a
  hypothetical `src/prometheus/research/microstructure/...` /
  `scripts/microstructure_*` / `tests/research/microstructure/`
  namespace, with per-module purpose / allowed imports /
  forbidden imports / public API / inputs / outputs / failure
  modes / tests / governance notes. **No file is created.**
- A **future CLI design** (§9) of subcommands, flags, dry-run
  behaviour, output paths, stop conditions, and logging.
- A **future configuration design** (§10) covering allowlist /
  denylist / symbol / family / cadence / rate-limit / threshold
  sections, with explicit no-secret / no-`.env` / no-API-key
  rule.
- A **future storage and `.gitignore` plan** (§11) describing
  the `data/microstructure/...` namespace as a future addition
  only; **no `.gitignore` modification, no directory
  creation**.
- A **future manifest implementation plan** (§12).
- A **future schema implementation plan** (§13) with explicit
  implementation order.
- A **future invalid-window implementation plan** (§14)
  enumerating all seventeen Phase 4au triggers as future
  error-class / enum entries with detection point, severity,
  downstream eligibility action, evidence fields, and tests.
- A **future research eligibility gate implementation plan**
  (§15) translating Phase 4au's ten checks into implementation
  steps; no flag flipped by Phase 4av.
- A **future deterministic replay implementation plan** (§16).
- A **future local-order-book reconstruction implementation
  plan** (§17).
- A **future collector implementation order** (§18) with
  rationale for aggTrades-first.
- A **future test matrix** (§19).
- A **future failure-mode matrix** (§20).
- A **future validation-command list** (§21).
- A **future implementation stop-conditions list** (§22).
- A **future implementation branch strategy** (§23).
- A **future security / credential implementation plan** (§24).
- A **future runtime-separation implementation plan** (§25).
- A **future symbol / scope implementation plan** (§26).
- **M0 and no-rescue implications** (§27).
- A **recommended next phase** (§28) and explicit
  **non-recommendations** (§29).
- The **implementation / governance review** (§30), the
  **research interpretation review** (§31), and explicit
  **preservation of verdicts, locks, and no-rescue
  constraints** (§32).

### Out of scope (forbidden in Phase 4av)

- No data acquisition.
- No Binance endpoint calls.
- No WebSocket connections.
- No public-archive downloads.
- No endpoint code creation or modification.
- No capture / replay / feature / ML / strategy
  implementation.
- No order-book reconstruction implementation.
- No backtest or historical strategy script execution.
- No Phase 4aq script re-execution.
- No simulation; no predictive statistics computation.
- No source / test / script / data / manifest / governance /
  spec / threshold / lock change.
- No `.gitignore` change.
- No commit of any `data/research/` output.
- No actual dataset directory creation under
  `data/microstructure/...`.
- No actual manifest creation.
- No schema-as-code, config file, or module-stub creation.
- No new strategy candidate.
- No exit / entry design.
- No optimisation of R3 or any prior population.
- No R3-prime / R2-prime / R1a-prime / R1b-narrow-prime / H0-prime
  / V2-prime / G1-prime / C1-prime / D1-A-prime / D1-B / V1-D1 /
  F1-D1 / cross-strategy hybrid.
- No verdict revision.
- No lock revision.
- No M0 amendment.
- No reopening of the 5m research thread.
- No authorisation of Phase 4aw, Phase 5, Phase 4 canonical,
  paper / shadow, live-readiness, deployment, exchange-write,
  production keys, authenticated APIs, private endpoints, user
  stream, WebSocket implementation, MCP, Graphify,
  `.mcp.json`, credentials, 5m / 1m / aggTrades / tick-data /
  mark-price 30m / 4h, or order-book capture.

---

## 3. Repository verification summary

Repository state at branch creation:

```text
git status                 — clean working tree on main; only
                              gitignored transients
                              (.claude/scheduled_tasks.lock,
                              data/research/) untracked.
git branch --show-current  — main (before branch creation) /
                              phase-4av/... (after).
git log --oneline -16      — Phase 4au merged at 6e9521b.
git rev-parse main         — 6e9521bbba5f2af8ca19f4789de4c9034c7a301a.
git rev-parse origin/main  — 6e9521bbba5f2af8ca19f4789de4c9034c7a301a.
```

Phase 4au files confirmed present on `main`:

- `docs/00-meta/implementation-reports/2026-05-07_phase-4au_binance-microstructure-capture-design-specification.md`.
- `docs/00-meta/implementation-reports/2026-05-07_phase-4au_closeout.md`.
- `docs/00-meta/implementation-reports/2026-05-07_phase-4au_merge-closeout.md`.

`main` and `origin/main` are in sync. The working tree contains
no unexpected uncommitted change.

Branch created:

```text
git checkout -b phase-4av/public-only-microstructure-capture-implementation-plan
```

---

## 4. Methodology

Phase 4av is a docs-only implementation-planning memo. It is
built from:

- **static repository inspection** of committed docs (Phase 4au
  memo + closeout + merge-closeout; Phase 4at; Phase 4as;
  Phase 4ar; Phase 4ak M0 governance file; Phase 3t / 3r §8 /
  3v §8 / 3w / 4j §11 governance; current-project-state;
  phase-gates);
- **public / official documentation references** carried
  forward from Phase 4au — Phase 4au is treated as the
  citation source of record for endpoint behaviour. Phase 4av
  itself makes **no new external research calls**.

The memo does **not**:

- call any Binance endpoint;
- modify any endpoint code;
- acquire any data;
- open any WebSocket;
- download any archive;
- inspect or modify local `data/research/` outputs;
- run any script;
- create any source file, test file, schema-as-code artefact,
  config file, manifest skeleton, or dataset directory;
- modify `.gitignore`;
- touch credentials, MCP, `.mcp.json`, or any exchange-write
  surface.

The memo follows the prior-phase docs-only convention used by
Phase 4d, 4e, 4f, 4g, 4h, 4j, 4k, 4m, 4n, 4o, 4p, 4q, 4s, 4t,
4u, 4v, 4w, 4y, 4z, 4aa, 4ab, 4ad, 4ag, 4ah, 4aj, 4ak, 4al,
4an, 4ao, 4ap, 4ar, 4as, 4at, and 4au (no `ruff` / `pytest` /
`mypy` execution because no code, test, or script is changed).

---

## 5. Phase 4au baseline (preserved)

Phase 4au is the binding context for Phase 4av. It is preserved
verbatim:

- **Capture-design goals (Phase 4au §6):** public-only;
  read-only; no credentials; no exchange-write; deterministic
  replay; immutable raw logs; manifest-first lineage; explicit
  invalid-window governance; layer separation; runtime
  separation; future-research-only.
- **Nine-component architecture (Phase 4au §7):** capture
  supervisor; per-symbol stream workers; REST polling workers;
  raw event writer; normalizer; replay builder; manifest
  writer; health-check reporter; local operator dashboard
  hook.
- **Public endpoint allowlist (Phase 4au §8):** aggTrade
  family (WS + REST + bulk archive); bookTicker stream;
  partial book depth stream; diff book depth stream; REST
  depth snapshot; forceOrder proxy stream; markPrice family
  (governance-blocked under Phase 3r §8 / Phase 3v §8);
  indexPrice family; fundingRate REST; openInterest REST
  snapshot (forward REST polling for time-series; not
  WebSocket); openInterestHist REST (~30 days rolling);
  top/global long-short REST (~30 days rolling);
  takerlongshortRatio REST (~30 days rolling).
- **Endpoint denylist (Phase 4au §9):** all private /
  authenticated endpoints; user stream; listenKey lifecycle;
  REST `/fapi/v1/forceOrders`; order placement; account;
  position; leverage / margin endpoints; any endpoint
  requiring API keys; MCP / Graphify / `.mcp.json` /
  credential-based integrations.
- **Seven dataset-family names (Phase 4au §10):**
  `microstructure_raw_aggtrades_v001`,
  `microstructure_raw_depthdiff_v001`,
  `microstructure_raw_bookticker_v001`,
  `microstructure_raw_forceorder_proxy_v001`,
  `microstructure_raw_markprice_v001`,
  `microstructure_metrics_oi_funding_v001`,
  `microstructure_replay_lob_v001`.
- **Storage layout (Phase 4au §11):** separate
  `data/microstructure/{raw,normalized,derived,manifests}`
  namespace; no writes to existing project data namespaces.
- **Manifest design (Phase 4au §13):** required fields
  including paired SHA256 list, `schema_version`,
  `capture_config_hash`, `code_commit_sha`, `invalid_windows`,
  `retention_warning`, `proxy_warning`, `governance_labels`,
  `research_eligible: false` default,
  `eligibility_gate_status: pending` default.
- **Schema design (Phase 4au §14):** per-family raw schemas
  with `event_time_ms` / `transaction_time_ms` /
  `ingestion_time_ms` / `local_monotonic_ns` separation.
- **Timestamp discipline (Phase 4au §15):** UTC ms
  canonicalisation; clock-skew detection; no mixing of
  event-time and ingestion-time in labels; future latency
  realism.
- **Rate-limit / retry design (Phase 4au §16):** documented
  endpoint budgets respected; backoff on 429 / 418; retry
  limits; no API keys; no IP rotation.
- **WebSocket design (Phase 4au §17):** one worker per
  (symbol, stream) pair; jittered exponential reconnect
  backoff; staleness detection; bounded queue with FIFO
  backpressure; persistence-before-processing; sequence-gap
  marking; no order placement surface.
- **LOB reconstruction (Phase 4au §18):** REST snapshot +
  diff-depth WS stream per the official Binance procedure
  (`U` / `u` / `pu` validation; first-event bracketing;
  resync on gap; stale-book / impossible-spread checks;
  deterministic replay).
- **Liquidation proxy (Phase 4au §19):** forceOrder largest-
  per-1000ms limitation; proxy-only label; no complete-tape
  claim; no authenticated `forceOrders` REST use; M-9
  admissible only as context / regime overlay.
- **OI / funding capture (Phase 4au §20):** funding history
  via REST; current OI via forward REST polling; OI historical
  statistics recent-only; long-short ratios recent-only;
  takerlongshortRatio recent-only; **Phase 4j §11 OI subset
  governance** binding; **D1-A precedent — funding context
  only**.
- **Invalid-window taxonomy (Phase 4au §21):** seventeen
  triggers; no silent forward-fill / interpolation /
  imputation / replacement.
- **Research eligibility gate (Phase 4au §22):** ten checks;
  the gate is the only path that may flip
  `research_eligible: true`.
- **Deterministic replay (Phase 4au §23):** raw → normalized →
  derived; LOB replay; replay config hash; reproducibility;
  no ad-hoc reads; replay logs; failure handling.
- **Health-check / dashboard (Phase 4au §24):** local-only
  per-stream and per-family signals; **no order panel; no
  kill-switch surface; no remote alerting at this layer**.
- **Security and credential boundary (Phase 4au §25):** no API
  keys; no `.env` reads; no authenticated / private endpoints;
  no order endpoints; no leverage / margin endpoints; no user
  stream; no listenKey; no MCP / Graphify / `.mcp.json`; no
  secrets in logs.
- **Runtime separation (Phase 4au §26):** no imports from
  `prometheus.runtime` / `execution` / `persistence`; no
  runtime database writes; no safety-state mutation; no
  order-router contact.

Phase 4av inherits all of those constraints verbatim and
translates them into a per-module implementation plan.

---

## 6. Future implementation scope (allowed if separately authorised)

If a future implementation phase is separately authorised, it
may implement (subject to that phase's own scope and stop
conditions):

1. **Public-only capture scaffold** — config loading,
   allowlist / denylist enforcement, dry-run CLI.
2. **Public-only endpoint allowlist enforcement** — runtime
   refusal of any URL or stream name not on the Phase 4au
   allowlist.
3. **Raw event writer** — append-only JSONL.zst writer with
   atomic write-then-rename and SHA256 pairing.
4. **Read-only archive / downloader helper** — only if
   separately authorised; downloads paired
   `<file>` + `<file>.CHECKSUM` from `data.binance.vision`,
   verifies SHA256, never mutates existing manifests.
5. **aggTrade collector** — bulk archive + REST forward
   catch-up + WS forward stream variants.
6. **bookTicker collector** — WS forward stream.
7. **diff depth collector** — WS forward stream.
8. **REST depth snapshot collector** — paired snapshot
   fetcher.
9. **forceOrder proxy collector** — WS forward stream with
   proxy-only labelling.
10. **OI / funding REST polling** — at documented `period`
    cadence with rate-limit-aware backoff.
11. **Manifest writer** — append-only manifest updater with
    SHA256 pairing.
12. **Schema validation** — per-family validators consuming
    raw files.
13. **Invalid-window writer** — appends `invalid_window`
    entries to manifests.
14. **Eligibility gate** — runs Phase 4au §22 ten checks and
    writes the structured eligibility-gate report.
15. **Deterministic replay builder** — raw → normalized →
    derived; LOB replay; byte-identical output requirement.
16. **Local health-check reporter** — emits structured local
    signals.
17. **Local-only dashboard hook** — read-only display of the
    health-check reporter.

**Phase 4av implements none of these.** Each item above is
recorded as a future allowed scope only.

---

## 7. Future implementation non-scope (always forbidden)

The following items are forbidden at every future
implementation phase derived from this plan and may not be
added without separate operator authorisation that itself
satisfies M0 admissibility:

- Authenticated endpoints.
- Order placement.
- User stream.
- listenKey lifecycle.
- Account / position / leverage endpoints.
- Private liquidation REST endpoint
  (`/fapi/v1/forceOrders`).
- Paper / shadow / live-readiness.
- Strategy logic.
- Feature research (any feature beyond those that satisfy a
  separately-authorised feasibility memo).
- ML model.
- Old-strategy reruns (R3 / R2 / R1a / R1b-narrow / H0 /
  F1 / D1-A / V2 / G1 / C1).
- 5m research thread reopening.
- Mark-price stop-domain forensics (Phase 3v §8 governance
  blocks this without separate authorisation).
- Any runtime / execution / persistence coupling.

---

## 8. Proposed future file / module plan

The following is a **design-only file tree**. **No file is
created in Phase 4av.** Each entry records purpose, allowed
imports, forbidden imports, public API / CLI role, expected
inputs, expected outputs, failure modes, tests required, and
governance notes.

```text
src/prometheus/research/microstructure/
├── __init__.py
├── config.py
├── allowlist.py
├── public_rest.py
├── public_ws.py
├── raw_writer.py
├── manifest.py
├── schema.py
├── invalid_window.py
├── collectors/
│   ├── __init__.py
│   ├── aggtrade.py
│   ├── bookticker.py
│   ├── depthdiff.py
│   ├── depth_snapshot.py
│   ├── forceorder_proxy.py
│   └── oi_funding.py
├── normalizer.py
├── replay/
│   ├── __init__.py
│   ├── lob.py
│   └── deterministic.py
├── eligibility_gate.py
├── healthcheck.py
└── dashboard_hook.py

scripts/
├── microstructure_capture.py
├── microstructure_replay.py
└── microstructure_eligibility_gate.py

tests/research/microstructure/
├── __init__.py
├── test_config.py
├── test_allowlist.py
├── test_no_secrets.py
├── test_raw_writer_atomic.py
├── test_manifest.py
├── test_schema.py
├── test_invalid_window.py
├── collectors/
│   ├── test_aggtrade.py
│   ├── test_bookticker.py
│   ├── test_depthdiff.py
│   ├── test_depth_snapshot.py
│   ├── test_forceorder_proxy.py
│   └── test_oi_funding.py
├── replay/
│   ├── test_lob_golden.py
│   └── test_deterministic.py
├── test_eligibility_gate.py
├── test_healthcheck.py
├── test_dashboard_hook.py
├── test_cli_dry_run.py
└── test_import_boundaries.py
```

### 8.1 `src/prometheus/research/microstructure/__init__.py`

- **Purpose:** package marker; **no executable logic**.
- **Allowed imports:** none beyond the standard library at this
  layer (the package init must not pre-import collectors or
  pull side effects).
- **Forbidden imports:** any of `prometheus.runtime`,
  `prometheus.execution`, `prometheus.persistence`,
  `requests`, `httpx`, `aiohttp`, `websockets`, `urllib`,
  `binance`, `python-binance`.
- **Public API:** none.
- **Inputs / outputs:** none.
- **Failure modes:** import error if forbidden import is added
  by mistake (caught by the import-boundary test).
- **Tests required:** import-boundary test
  (`test_import_boundaries.py`) verifying no forbidden
  imports.
- **Governance notes:** establishes the namespace boundary;
  must not be reused for paper / shadow / live work.

### 8.2 `config.py`

- **Purpose:** load and validate the capture configuration
  (allowlist, symbols, family settings, storage root, cadence,
  WS reconnect, REST budget, invalid-window thresholds,
  eligibility-gate thresholds, replay settings, health-check
  settings).
- **Allowed imports:** `pydantic` (or `dataclasses` + manual
  validation), `pathlib`, standard library only. **Reads
  config from a non-secret YAML / TOML file**, not from
  `.env`.
- **Forbidden imports:** any HTTP / WS / Binance client; any
  `prometheus.runtime / execution / persistence`; any
  `os.environ` access pattern that would suggest secret
  loading; any `.env` reader.
- **Public API:** `load_config(path) -> CaptureConfig`,
  `CaptureConfig` model with frozen invariants.
- **Inputs:** path to a non-secret config file.
- **Outputs:** validated `CaptureConfig`.
- **Failure modes:** missing path; malformed file; unknown
  field; unknown endpoint; unknown symbol; out-of-range
  threshold.
- **Tests required:** valid-config golden;
  invalid-config-rejected; unknown-endpoint-rejected;
  unknown-symbol-rejected; threshold-bounds tests; **no-env
  test** asserting the loader never calls `os.environ` for any
  key beyond a documented allowlist (e.g. `LOG_LEVEL`).
- **Governance notes:** central point that enforces "no
  secrets, no API keys" by construction.

### 8.3 `allowlist.py`

- **Purpose:** define the public-only endpoint allowlist and
  the explicit denylist as immutable data structures, and
  provide a single helper that refuses any URL / stream not on
  the allowlist.
- **Allowed imports:** `re`, `enum`, standard library only.
- **Forbidden imports:** any HTTP / WS client; any
  `prometheus.runtime / execution / persistence`.
- **Public API:** `ALLOWLIST_REST`, `ALLOWLIST_WS`,
  `DENYLIST_PATTERNS`, `is_endpoint_allowed(url) -> bool`,
  `assert_endpoint_allowed(url) -> None`.
- **Inputs:** URL strings, stream names.
- **Outputs:** boolean / raises `EndpointNotAllowedError`.
- **Failure modes:** denylisted URL passed; allowlisted URL
  malformed; pattern match ambiguity.
- **Tests required:** every Phase 4au allowlist entry passes;
  every Phase 4au denylist entry is rejected; private endpoints
  rejected; user-stream paths rejected; order-placement paths
  rejected; `forceOrders` REST rejected; `forceOrder` stream
  allowed; allowlist enumeration matches the Phase 4au memo.
- **Governance notes:** **the only place** where endpoint
  policy is encoded. Any new endpoint requires a separately
  authorised governance memo + an update here.

### 8.4 `public_rest.py`

- **Purpose:** thin wrapper around a public-only REST client.
  Wraps `httpx` (or equivalent) calls but exposes only
  allowlist-vetted callers.
- **Allowed imports:** `httpx` (or chosen sync/async client),
  `time`, `random`, `enum`, `allowlist` (own module),
  standard library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`; any signature / HMAC helper; any `binance`
  package; any user-stream / listenKey helper.
- **Public API:** `get_aggtrades(...)`, `get_klines(...)`,
  `get_funding_rate(...)`, `get_open_interest(...)`,
  `get_open_interest_hist(...)`,
  `get_top_long_short_account_ratio(...)`,
  `get_top_long_short_position_ratio(...)`,
  `get_global_long_short_account_ratio(...)`,
  `get_taker_long_short_ratio(...)`, `get_depth_snapshot(...)`,
  `get_premium_index_klines(...)`, `get_index_price_klines(...)`,
  `get_mark_price_klines(...)`. Each helper passes its target
  URL through `assert_endpoint_allowed` before any I/O.
- **Inputs:** allowlist-vetted parameters.
- **Outputs:** parsed JSON dicts / typed records.
- **Failure modes:** non-2xx response; HTTP 429; HTTP 418;
  network timeout; unexpected schema; rate-limit budget
  exceeded.
- **Tests required:** allowlist-vetted test (every helper
  rejects denylisted URLs); rate-limit-aware backoff test (with
  injected fake clock); 429 / 418 backoff behaviour;
  unexpected-schema rejection; **no real network call in
  tests** — all I/O mocked.
- **Governance notes:** never accepts an API key; never
  produces a signed request; never reads `.env`.

### 8.5 `public_ws.py`

- **Purpose:** thin wrapper around a public-only WebSocket
  client.
- **Allowed imports:** `websockets`, `asyncio`, `time`,
  `random`, `enum`, `allowlist`, standard library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`; any user-stream helper; any `listenKey`
  helper; any `binance` package.
- **Public API:** `subscribe(stream_name) -> AsyncIterator[Event]`
  with built-in reconnect, jittered exponential backoff, and
  staleness detection per Phase 4au §17.
- **Inputs:** allowlist-vetted stream names.
- **Outputs:** async iterator of parsed events with attached
  `ingestion_time_ms` and `local_monotonic_ns` fields.
- **Failure modes:** disconnect; stale stream; malformed
  payload; backpressure overflow; symbol mismatch.
- **Tests required:** disconnect → reconnect golden;
  staleness threshold exceeded → invalid window;
  backpressure FIFO behaviour; symbol-mismatch detection;
  **no real network call** in tests.
- **Governance notes:** never opens a user stream; never
  uses `listenKey`; never accepts authentication.

### 8.6 `raw_writer.py`

- **Purpose:** append-only raw-event writer. Writes JSONL.zst
  with the atomic write-then-rename pattern and pairs each
  file with a `.sha256` companion.
- **Allowed imports:** `zstandard`, `hashlib`, `pathlib`,
  `os`, `tempfile`, standard library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`; any HTTP / WS client.
- **Public API:** `RawWriter(family, symbol, root_dir,
  partition_key)` with `append(event)`, `rotate()`, `close()`.
- **Inputs:** events as dicts.
- **Outputs:** raw JSONL.zst files + paired `.sha256` files
  under `data/microstructure/raw/<family>/<symbol>/<yyyy>/<mm>/<dd>/`.
- **Failure modes:** disk full; permission error; partial
  write (`.tmp` left behind); checksum mismatch on read-back.
- **Tests required:** atomic write-then-rename; `.tmp`
  cleanup; SHA256 pairing; checksum mismatch detection;
  rotation by symbol + UTC date; recovery on startup with
  partial file present (writes `failed_atomic_write` invalid
  window).
- **Governance notes:** **never overwrites** existing files;
  never modifies existing project data namespaces.

### 8.7 `manifest.py`

- **Purpose:** append-only manifest writer per the Phase 4au
  §13 schema.
- **Allowed imports:** `json`, `pathlib`, `hashlib`, standard
  library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`; any HTTP / WS client.
- **Public API:**
  `Manifest.load(family, version, root_dir)`,
  `Manifest.append_file(file_entry)`,
  `Manifest.append_invalid_window(window_entry)`,
  `Manifest.set_governance_label(...)`, `Manifest.save()`.
- **Inputs:** file entries; invalid-window entries; governance
  labels.
- **Outputs:**
  `data/microstructure/manifests/<family>__v001.json`.
- **Failure modes:** concurrent write (must be single-writer
  per family); malformed entry; SHA256 mismatch; schema
  violation.
- **Tests required:** append-only invariant; immutable
  fields; idempotent writes; SHA256 pairing for every file
  entry; default `research_eligible: false`; default
  `eligibility_gate_status: pending`; cannot flip
  `research_eligible: true` without going through the
  eligibility-gate code path.
- **Governance notes:** **the only writer** allowed to set
  `research_eligible` (and only when called by the
  eligibility-gate module).

### 8.8 `schema.py`

- **Purpose:** per-family schema validators per Phase 4au §14.
- **Allowed imports:** `pydantic` or `dataclasses` + manual
  validation, standard library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`; any HTTP / WS client.
- **Public API:** one validator per family
  (`validate_aggtrade`, `validate_bookticker`,
  `validate_depthdiff`, `validate_depth_snapshot`,
  `validate_forceorder_proxy`, `validate_markprice`,
  `validate_oi_funding`, `validate_replay_lob`).
- **Inputs:** raw event dicts (or Parquet rows in the
  normalized layer).
- **Outputs:** validated typed records or `SchemaError`.
- **Failure modes:** missing required field; type mismatch;
  unexpected field; out-of-range value.
- **Tests required:** golden valid records pass; common
  malformed records rejected with deterministic error
  messages; required-field absence rejected; unknown-field
  rejected; cross-family validators do not bleed into each
  other.
- **Governance notes:** the schemas pin types under
  `schema_version = "v001"`; a schema change forces a fresh
  `__vNNN` family bump per Phase 4au §10.

### 8.9 `invalid_window.py`

- **Purpose:** enumerate the seventeen Phase 4au triggers as a
  closed enum and provide constructors for `InvalidWindow`
  records.
- **Allowed imports:** `enum`, `dataclasses`, standard library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`.
- **Public API:** `InvalidWindowReason` enum with seventeen
  members; `InvalidWindow` dataclass with required fields
  (`start_time_ms`, `end_time_ms`, `family`, `symbol`,
  `reason`, `evidence`, `severity`,
  `downstream_eligibility_action`).
- **Inputs:** detection-point arguments.
- **Outputs:** structured `InvalidWindow` records appended
  to the manifest via `manifest.append_invalid_window`.
- **Failure modes:** missing required field; unknown reason
  string.
- **Tests required:** every enum value round-trips through
  serialization; required-field absence rejected; severity /
  downstream-action enums match Phase 4au §21.3.
- **Governance notes:** **no silent forward-fill /
  interpolation / imputation / replacement** is permitted at
  any layer.

### 8.10–8.15 Collectors (`collectors/<family>.py`)

- **Purpose:** per-family capture orchestration. Each collector
  pulls from the public REST / WS surface (via §8.4 / §8.5),
  dispatches events to the raw writer (§8.6), and reports
  invalid windows (§8.9) and manifest updates (§8.7).
- **Allowed imports:** the package's own `config`,
  `allowlist`, `public_rest`, `public_ws`, `raw_writer`,
  `manifest`, `schema`, `invalid_window`; `asyncio`,
  standard library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`.
- **Public API:** `CollectorAggTrade.run(...)`,
  `CollectorBookTicker.run(...)`,
  `CollectorDepthDiff.run(...)`,
  `CollectorDepthSnapshot.run(...)`,
  `CollectorForceOrderProxy.run(...)`,
  `CollectorOIFunding.run(...)` (one collector per family;
  `oi_funding.py` aggregates the multiple REST endpoints
  under one collector with shared rate-limit budget).
- **Inputs:** configuration, symbol allowlist, time bounds.
- **Outputs:** raw files + manifest entries + invalid-window
  entries.
- **Failure modes:** see §20.
- **Tests required:** see §19.
- **Governance notes:** each collector is constrained to
  exactly one Phase 4au allowlist entry.

### 8.16 `normalizer.py`

- **Purpose:** deterministic batch normalizer that consumes
  raw files and produces normalized Parquet under
  `data/microstructure/normalized/<family>/...`.
- **Allowed imports:** `pyarrow`, `zstandard`, `hashlib`,
  `pathlib`, `schema`, `invalid_window`, `manifest`, standard
  library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`.
- **Public API:** `Normalizer.run(family, symbol, partition)`.
- **Inputs:** completed raw partitions only (never partial).
- **Outputs:** normalized Parquet files + manifest entries +
  invalid-window propagation.
- **Failure modes:** schema mismatch; partial partition;
  byte-non-deterministic output.
- **Tests required:** byte-identical normalization under
  fixed `capture_config_hash`; schema-validation pass; partial
  partition refusal; SHA256 pairing.
- **Governance notes:** never modifies raw layer; never
  modifies existing project data.

### 8.17 `replay/lob.py` and `replay/deterministic.py`

- **Purpose:** deterministic replay builder; `lob.py`
  reconstructs the local order book per Phase 4au §18;
  `deterministic.py` provides the replay-config-hash and
  byte-identical-output discipline shared with the normalizer.
- **Allowed imports:** `pyarrow`, `hashlib`, `pathlib`,
  `schema`, `invalid_window`, `manifest`, standard library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`; any HTTP / WS client (replay does not
  re-fetch).
- **Public API:** `ReplayLOB.run(...)`,
  `ReplayConfig.hash()`.
- **Inputs:** completed normalized partitions only; replay
  config.
- **Outputs:**
  `data/microstructure/derived/microstructure_replay_lob_v001/...`;
  manifest entries with `replay_config_hash` and
  `code_commit_sha`.
- **Failure modes:** snapshot mismatch; sequence gap;
  impossible spread; stale book; non-deterministic output.
- **Tests required:** golden-replay test (byte-identical
  output); `U` / `u` / `pu` validation; first-event bracketing;
  resync-on-gap; impossible-spread detection; stale-book
  detection; deterministic `replay_config_hash`.
- **Governance notes:** replay does not re-fetch from the
  network; only the raw layer + REST snapshot files are
  consumed.

### 8.18 `eligibility_gate.py`

- **Purpose:** run the Phase 4au §22 ten checks and write the
  structured eligibility-gate report.
- **Allowed imports:** `manifest`, `schema`, `invalid_window`,
  standard library.
- **Forbidden imports:** any HTTP / WS client; `prometheus.runtime
  / execution / persistence`; any random number generator that
  could affect determinism.
- **Public API:**
  `run_eligibility_gate(family, version, root_dir) -> GateReport`.
  Internal: `Manifest.set_research_eligible(True)` may **only**
  be called from this module.
- **Inputs:** a manifest + the underlying raw / normalized /
  derived files.
- **Outputs:** structured `GateReport` JSON file under
  `data/microstructure/manifests/<family>__v001.gate_report.json`;
  on full pass, manifest's `research_eligible` is set to
  `true` and `eligibility_gate_status` is set to
  `passed_full` or `passed_partial`.
- **Failure modes:** any check fails → `eligibility_gate_status
  = failed`; manifest `research_eligible` remains `false`.
- **Tests required:** every check pass / fail individually
  golden; no-flip path tested; `passed_partial` for
  governance-bounded families like OI subset under Phase 4j
  §11; proxy-warning families always tagged.
- **Governance notes:** the **only path** allowed to flip
  `research_eligible: true`.

### 8.19 `healthcheck.py`

- **Purpose:** emit structured local health signals per
  Phase 4au §24.
- **Allowed imports:** `json`, `pathlib`, `time`, standard
  library.
- **Forbidden imports:** any HTTP / WS client (the health-check
  reporter is local-only); `prometheus.runtime / execution /
  persistence`; any remote alerting (Telegram, n8n, MCP,
  Graphify).
- **Public API:** `HealthCheckReporter.update(per_stream,
  per_family, ...)`, file-based (writes to
  `data/microstructure/healthcheck/<runid>.json`).
- **Inputs:** in-memory metrics from the supervisor / workers.
- **Outputs:** local JSON file consumed by the dashboard hook.
- **Failure modes:** disk full; concurrent write (single-writer
  enforced).
- **Tests required:** atomic write; structured-fields golden;
  per-stream / per-family aggregation correctness.
- **Governance notes:** **no remote alerting** at this layer.

### 8.20 `dashboard_hook.py`

- **Purpose:** read-only consumer of the health-check
  reporter's local file; exposes a small read API for the
  operator dashboard.
- **Allowed imports:** `json`, `pathlib`, standard library.
- **Forbidden imports:** any HTTP / WS client; any
  order-placement helper; any kill-switch surface; any
  `prometheus.runtime / execution / persistence`.
- **Public API:** `read_health(runid) -> HealthSnapshot`.
- **Inputs:** path to the health-check file.
- **Outputs:** typed health snapshot.
- **Failure modes:** missing / corrupt file.
- **Tests required:** read happy-path; missing file → graceful
  empty snapshot.
- **Governance notes:** **read-only**; no order panel; no
  kill-switch surface.

### 8.21 `scripts/microstructure_capture.py`

- **Purpose:** CLI entry-point that wires the supervisor to
  collectors. Subcommands per §9.
- **Allowed imports:** package modules above + `argparse` /
  `click` / `typer`, `asyncio`, `logging`, standard library.
- **Forbidden imports:** `prometheus.runtime / execution /
  persistence`.
- **Public API / CLI role:** see §9.
- **Inputs:** config path; subcommand-specific flags.
- **Outputs:** raw files; manifest updates; health-check
  signals.
- **Failure modes:** see §20.
- **Tests required:** dry-run for every subcommand; allowlist
  enforcement; help text golden.
- **Governance notes:** dry-run is the default for unknown /
  unauthorised subcommand combinations.

### 8.22 `scripts/microstructure_replay.py`

- **Purpose:** CLI entry-point for the replay builder.
- **Allowed imports:** package modules above + CLI parser.
- **Forbidden imports:** any HTTP / WS client;
  `prometheus.runtime / execution / persistence`.
- **Public API / CLI role:** `replay lob`.
- **Inputs:** config path; family; symbol; partition.
- **Outputs:** derived Parquet under
  `data/microstructure/derived/...`; manifest entries.
- **Failure modes:** see §17 / §20.
- **Tests required:** replay determinism; CLI dry-run.
- **Governance notes:** never re-fetches data.

### 8.23 `scripts/microstructure_eligibility_gate.py`

- **Purpose:** CLI entry-point for the eligibility gate.
- **Allowed imports:** package modules above.
- **Forbidden imports:** any HTTP / WS client;
  `prometheus.runtime / execution / persistence`.
- **Public API / CLI role:** `eligibility-gate`.
- **Inputs:** config path; family.
- **Outputs:** gate report JSON; manifest update on pass.
- **Failure modes:** any check fails → gate status set to
  `failed`; no flag flip.
- **Tests required:** every check pass / fail; partial-pass
  for governance-bounded families.
- **Governance notes:** the **only** code path that may flip
  `research_eligible: true`.

### 8.24 `tests/research/microstructure/`

- See §19 for the full test matrix. Every module above has a
  paired test file. The package includes a global
  `test_import_boundaries.py` that grep-asserts no module
  imports `prometheus.runtime / execution / persistence`,
  `binance`, `python-binance`, signature helpers, or
  authentication helpers.

---

## 9. Future CLI design

### 9.1 Subcommands (planned only)

- `capture aggtrades`
- `capture bookticker`
- `capture depthdiff`
- `capture forceorder`
- `poll oi-funding`
- `snapshot depth`
- `normalize`
- `replay lob`
- `validate-schema`
- `eligibility-gate`
- `health-report`

### 9.2 Per-subcommand specification

Each entry below is a planned design only.

#### `capture aggtrades`

- **Purpose:** collect aggTrade events for a symbol via WS or
  REST catch-up; optionally backfill from
  `data.binance.vision`.
- **Required flags:** `--symbol`, `--mode {ws|rest|archive}`,
  `--config`.
- **Optional flags:** `--start-ts-ms`, `--end-ts-ms`,
  `--rotation {hour|day}`.
- **Forbidden flags:** `--api-key`, `--secret`,
  `--listen-key`, `--user-stream`, `--order`, `--leverage`,
  `--margin`, `--mcp-config`, `--graphify`.
- **Output paths:**
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/...`.
- **Dry-run behaviour:** prints the planned actions, including
  the resolved allowlist URL / stream name and the planned
  output paths; **does not open any connection**.
- **Stop conditions:** allowlist refusal; rate-limit budget
  exceeded; archive checksum mismatch; disk full.
- **Logging:** structured JSON lines; never include
  credentials; never include raw event bodies above a
  documented size bound.

#### `capture bookticker`

- **Purpose:** collect bookTicker events via WS.
- **Required flags:** `--symbol`, `--config`.
- **Optional flags:** `--rotation {hour|day}`.
- **Forbidden flags:** as above.
- **Output paths:**
  `data/microstructure/raw/microstructure_raw_bookticker_v001/...`.
- **Dry-run / stop / logging:** as above.

#### `capture depthdiff`

- **Purpose:** collect diff-depth events via WS.
- **Required flags:** `--symbol`, `--config`,
  `--cadence {100ms|250ms|500ms}`.
- **Optional flags:** `--rotation {hour|day}`,
  `--snapshot-on-start {bool}`,
  `--periodic-snapshot {hours}`.
- **Forbidden flags:** as above.
- **Output paths:**
  `data/microstructure/raw/microstructure_raw_depthdiff_v001/...`.
- **Dry-run / stop / logging:** as above.

#### `capture forceorder`

- **Purpose:** collect forceOrder snapshots via WS.
- **Required flags:** `--symbol-or-all`, `--config`.
- **Optional flags:** `--rotation {hour|day}`.
- **Forbidden flags:** as above; **plus** `--rest-forceorders`
  (the user-scope REST endpoint is denylisted by Phase 4au
  §9).
- **Output paths:**
  `data/microstructure/raw/microstructure_raw_forceorder_proxy_v001/...`.
- **Dry-run / stop / logging:** as above; manifest carries
  `proxy_warning = "largest_per_1000ms_snapshot_only"`.

#### `poll oi-funding`

- **Purpose:** poll the REST family
  (`fundingRate`, `openInterest`, `openInterestHist`,
  `topLongShortAccountRatio`, `topLongShortPositionRatio`,
  `globalLongShortAccountRatio`, `takerlongshortRatio`).
- **Required flags:** `--config`,
  `--families <comma-list>`, `--symbols <comma-list>`,
  `--period <bucket>`.
- **Optional flags:** `--start-ts-ms`, `--end-ts-ms`.
- **Forbidden flags:** as above.
- **Output paths:**
  `data/microstructure/raw/microstructure_metrics_oi_funding_v001/...`.
- **Dry-run / stop / logging:** as above; manifest carries
  `retention_warning = "rest_recent_only_30d"` for the
  recent-only families.

#### `snapshot depth`

- **Purpose:** fetch a paired REST depth snapshot for a symbol
  (used as the bracketing snapshot for a depthdiff capture).
- **Required flags:** `--symbol`, `--limit 1000`, `--config`.
- **Optional flags:** none.
- **Forbidden flags:** as above.
- **Output paths:** subordinate to
  `microstructure_raw_depthdiff_v001` partition.

#### `normalize`

- **Purpose:** deterministic batch normalization of completed
  raw partitions.
- **Required flags:** `--family`, `--symbol`, `--partition`,
  `--config`.
- **Optional flags:** `--force` (no — must be rejected; the
  normalized layer is rebuilt deterministically only on a
  family `__vNNN` bump).
- **Forbidden flags:** anything that would mutate the raw
  layer.
- **Output paths:** `data/microstructure/normalized/...`.
- **Dry-run / stop / logging:** as above; partial partitions
  are refused.

#### `replay lob`

- **Purpose:** deterministic LOB replay from depthDiff +
  snapshot.
- **Required flags:** `--symbol`, `--partition`, `--config`,
  `--top-n`.
- **Optional flags:** `--snapshot-interval-hours`.
- **Forbidden flags:** anything that would re-fetch.
- **Output paths:**
  `data/microstructure/derived/microstructure_replay_lob_v001/...`.
- **Dry-run / stop / logging:** as above; replay must produce
  byte-identical output across runs.

#### `validate-schema`

- **Purpose:** validate raw / normalized files against pinned
  schemas.
- **Required flags:** `--family`, `--symbol`, `--partition`.
- **Optional flags:** `--strict` (default on).
- **Forbidden flags:** anything that would mutate manifests
  outside the eligibility-gate path.
- **Output paths:** none beyond log output.

#### `eligibility-gate`

- **Purpose:** run the Phase 4au §22 ten checks; on full pass,
  flip `research_eligible: true`.
- **Required flags:** `--family`, `--config`.
- **Optional flags:** `--report-path`.
- **Forbidden flags:** anything that would force-flip the
  flag.
- **Output paths:**
  `data/microstructure/manifests/<family>__v001.gate_report.json`
  + manifest update on pass.

#### `health-report`

- **Purpose:** local-only health dump.
- **Required flags:** `--runid`.
- **Optional flags:** `--out`.
- **Forbidden flags:** anything remote-alerting.
- **Output paths:** stdout / local file.

---

## 10. Future configuration design

### 10.1 Sections (planned only)

- `endpoint_allowlist` — populated from Phase 4au §8;
  read-only at runtime.
- `endpoint_denylist` — populated from Phase 4au §9;
  read-only at runtime.
- `symbol_allowlist` — `["BTCUSDT", "ETHUSDT"]` by default;
  Phase 4ac core symbols only if separately authorised.
- `dataset_family_config` — per-family settings (cadence,
  rotation, snapshot interval, schema version).
- `storage_root` — default `data/microstructure/`; never
  the project's existing `data/raw/` / `data/normalized/`
  / `data/manifests/` namespaces.
- `capture_cadence` — per-family / per-stream cadence in
  milliseconds.
- `websocket_reconnect` — base / max backoff,
  staleness threshold, queue depth.
- `rest_rate_limit_budgets` — per-endpoint pool budgets
  (e.g. 500 req/5min/IP for funding; 1000 req/5min/IP for
  takerlongshortRatio / globalLongShortAccountRatio; per-
  endpoint request weight; IP-level
  `REQUEST_WEIGHT` budget).
- `invalid_window_thresholds` — per-family per-month
  threshold for non-info severity (e.g. ≤ 5%).
- `eligibility_gate_thresholds` — per-check thresholds.
- `replay_settings` — top-N, snapshot interval, replay
  config-hash inputs.
- `healthcheck_settings` — output path, write cadence,
  per-stream / per-family signals.

### 10.2 Forbidden config fields

The following must be **structurally absent** from any future
configuration and rejected by the loader:

- `api_key`, `api_secret`, `secret_key`, `signature`,
  `listen_key`, `user_stream`, `auth_token`,
  `private_endpoint`, any field that holds a credential.
- `.env` references (the loader does not read `.env`).
- `mcp_config`, `graphify_config`, `mcp_json`,
  any MCP / Graphify integration field.
- `order_url`, `account_url`, `position_url`, `leverage_url`,
  `margin_url`, any path that would target a denylisted
  endpoint family.

**No config file is created by Phase 4av.**

---

## 11. Future storage and `.gitignore` plan

### 11.1 `data/microstructure/...` namespace

Phase 4au recommended a separate
`data/microstructure/raw/` /
`data/microstructure/normalized/` /
`data/microstructure/derived/` /
`data/microstructure/manifests/` namespace, isolated from the
existing `data/raw/` / `data/normalized/` / `data/derived/` /
`data/manifests/` paths used by Phase 2 / 3q / 4i / 4ac.

**Phase 4av does not create any directory under
`data/microstructure/...`.**

### 11.2 `.gitignore` plan

A future implementation phase would need an explicit
`.gitignore` addition for `data/microstructure/` **before**
creating any local capture data. The line should follow the
existing pattern at `.gitignore:88` (`data/research/`):

```text
data/microstructure/
```

**Phase 4av does not modify `.gitignore`.** A future scaffold
implementation phase would add the line as part of its first
commit, before any directory is created and before any
collector is wired up.

### 11.3 Boundary

**Phase 4av does not create any directory under
`data/microstructure/...` and does not modify `.gitignore`.**

---

## 12. Future dataset manifest implementation plan

Translate Phase 4au §13 into implementation steps. **None
implemented in Phase 4av.**

1. **Manifest schema.** Implemented in `manifest.py` (§8.7);
   fields exactly per Phase 4au §13.
2. **Append-only updates.** `Manifest.append_file` and
   `Manifest.append_invalid_window` are append-only;
   immutable fields cannot change after first write.
3. **SHA256 pairing.** Every `files[]` entry is written only
   after the corresponding `.sha256` companion file exists
   on disk and matches the file's content.
4. **Per-file event counts.** Every `files[]` entry carries
   `event_count`; the family-level `event_count` is the sum.
5. **Invalid windows.** Append-only via
   `append_invalid_window`; never silently filled.
6. **`research_eligible` default false.** Set by
   `Manifest.load` for fresh manifests; only the eligibility-
   gate module may flip it (§8.18).
7. **`eligibility_gate_status` default pending.** Set by
   `Manifest.load` for fresh manifests; only the eligibility-
   gate module may transition it.
8. **`code_commit_sha`.** Recorded at every manifest write;
   sourced from `git rev-parse HEAD`.
9. **`capture_config_hash`.** Recorded at every manifest
   write; sourced from a stable hash of the validated
   config.
10. **`endpoint_docs_reference`.** Recorded once per family;
    points to the relevant Binance Open Platform doc URL or
    Phase 4at citation.

**No manifest is created by Phase 4av.**

---

## 13. Future schema implementation plan

Translate Phase 4au §14 into an implementation order. **None
implemented in Phase 4av.**

1. **aggTrades first.** Smallest, fully archived, simplest
   sequence model (`agg_id`).
2. **bookTicker second.** Single sequence field (`u`); spread
   sanity check is straightforward.
3. **depthDiff + depthSnapshot third.** `U` / `u` / `pu`
   bracketing rule; paired snapshot files.
4. **forceOrder proxy fourth.** Bounded; proxy-only label.
5. **OI / funding metrics fifth.** Polled REST records
   (multiple endpoints aggregated under one family).
6. **markPrice only if separately authorised.** Phase 3r §8 /
   Phase 3v §8 governance applies; not implemented by default.
7. **Replay LOB derived schema after depthDiff.** Top-N rows;
   produced from §17.

**No schema file is created by Phase 4av.**

---

## 14. Future invalid-window implementation plan

Translate every Phase 4au §21.1 trigger into a future
`InvalidWindowReason` enum entry (§8.9). **No enum or class is
created in Phase 4av.**

| Trigger | Detection point | Severity | Downstream eligibility action | Required evidence | Tests required |
|---|---|---|---|---|---|
| `missing_sequence` | aggTrade `a` / bookTicker `u` / depthDiff `u` jump | error | exclude | seq numbers before / after | unit test golden |
| `out_of_order_event` | event-time decreases beyond tolerance | warn | flag | `event_time_ms` pair | unit |
| `duplicate_event` | repeat `agg_id` or `(U, u, pu)` | warn | flag | duplicate id | unit |
| `gap_after_reconnect` | WS reconnect crosses unconfirmed seq | error | exclude | reconnect window | unit |
| `snapshot_mismatch` | depthDiff `U > lastUpdateId` | error | exclude | snapshot file ref | unit |
| `clock_skew` | `ingestion - event` > drift bound | warn | flag | mean / max drift | unit |
| `symbol_mismatch` | WS payload symbol mismatch | error | exclude | payload symbol | unit |
| `stale_stream` | no event within staleness bound | warn | flag | last-event timestamp | unit |
| `stale_book` | no diff applied within staleness bound | warn | flag | last-diff timestamp | unit |
| `impossible_spread` | `best_ask < best_bid` | error | exclude | offending row | unit |
| `negative_size` | quantity < 0 | error | exclude | level entry | unit |
| `zero_or_invalid_price` | price ≤ 0 / non-finite | error | exclude | row | unit |
| `archive_checksum_mismatch` | `.CHECKSUM` SHA256 fails | error | exclude | archive path | unit |
| `rest_retention_gap` | REST returns less than requested window | warn | flag with `retention_warning` | requested vs returned | unit |
| `force_order_proxy_incompleteness` | indication of multiple liquidations in same 1000 ms | warn | proxy_only | timestamps | unit |
| `failed_atomic_write` | `.tmp` present at startup | error | exclude | tmp path | unit |
| `partial_file_recovery_event` | partial file deleted on startup | error | exclude | deleted path | unit |

**Phase 4av does not implement any enum, class, or detection
logic.** The table is design-only.

---

## 15. Future research eligibility gate implementation plan

Translate Phase 4au §22 ten checks into implementation steps.
**None implemented in Phase 4av.**

1. **Raw files present.** Iterate `manifest.files[]`; assert
   each path exists.
2. **Checksum pass.** Recompute SHA256 per file; compare to
   manifest entry.
3. **Schema validation pass.** Run the family's schema
   validator (§8.8) against every file.
4. **Timestamp sanity pass.** Per-family monotonicity /
   tolerance checks.
5. **Sequence continuity pass.** Per-family sequence-number
   continuity (`agg_id` / `u` / `pu`) — every gap must already
   be in `manifest.invalid_windows[]`.
6. **Invalid-window threshold.** Sum non-info-severity
   coverage; assert ≤ per-family threshold per month.
7. **Retention completeness label.** Assert
   `retention_warning` is set correctly for the recent-only
   REST families.
8. **Proxy limitation label.** Assert `proxy_warning` is set
   for `microstructure_raw_forceorder_proxy_v001`.
9. **Governance labels.** Assert per-family
   `governance_labels` are present and consistent
   (Phase 3r §8 / Phase 3v §8 / Phase 4j §11).
10. **Final `research_eligible` decision.** Only on full pass:
    flip to `true`; set `eligibility_gate_status` to
    `passed_full` (or `passed_partial` for governance-bounded
    families like OI subset under Phase 4j §11).

### 15.1 Phase 4av boundary

- The eligibility gate is **not** implemented by Phase 4av.
- **No `research_eligible` flag is flipped by Phase 4av.**
- No flag-flipping helper or skeleton is created.

---

## 16. Future deterministic replay implementation plan

Translate Phase 4au §23 into implementation steps. **None
implemented in Phase 4av.**

1. **Raw → normalized replay.** `normalizer.py` (§8.16)
   reads completed raw partitions and writes normalized
   Parquet under
   `data/microstructure/normalized/...`.
   Byte-identical output under fixed `capture_config_hash`.
2. **Normalized → derived replay.** `replay/deterministic.py`
   reads completed normalized partitions and writes derived
   Parquet under `data/microstructure/derived/...`.
3. **LOB replay.** `replay/lob.py` reconstructs the local
   order book from a paired snapshot + diff stream; emits
   top-N rows per event-time row.
4. **`replay_config_hash`.** Stable hash of all replay-config
   inputs (top-N, snapshot interval, staleness bounds, schema
   version, etc.). Recorded in the derived manifest.
5. **Byte-identical output requirement.** A failed determinism
   test halts the build before any partial output is written.
6. **Replay logs.** Every replay emits a structured log
   (start / end time, source files, output files, config
   hash, code commit SHA, exit status).
7. **Replay failure behaviour.** Partial output is deleted;
   `failed_atomic_write` invalid window recorded if applicable.
8. **No ad-hoc raw reads by research code.** Research consumes
   derived layers only; ad-hoc reads of raw logs are
   forbidden by code-review rule.

**Phase 4av does not implement any replay logic.**

---

## 17. Future local order-book reconstruction implementation plan

Translate Phase 4au §18 into planned module boundaries and
tests. **None implemented in Phase 4av.**

| Sub-component | Module | Tests |
|---|---|---|
| Snapshot fetcher | `collectors/depth_snapshot.py` | REST `limit=1000` parses; mocked client |
| Diff buffer | `replay/lob.py` | bounded buffer; FIFO discipline |
| First-event bracketing | `replay/lob.py` | `U <= lastUpdateId AND u >= lastUpdateId` |
| `U` / `u` / `pu` continuity | `replay/lob.py` | gap → resync → invalid window |
| Apply-diff engine | `replay/lob.py` | golden replay; price-level upsert; quantity-zero removal |
| Top-N extractor | `replay/lob.py` | top-N invariant per row |
| Stale-book detector | `replay/lob.py` | staleness bound exceeded → invalid window |
| Impossible-spread detector | `replay/lob.py` | `best_ask < best_bid` → invalid window |
| Resync handler | `replay/lob.py` | fresh snapshot fetched; partition resumed cleanly |
| Invalid-window writer | via `manifest.py` | every detection produces a manifest entry |

**Phase 4av does not implement reconstruction.**

---

## 18. Future collector implementation order

A conservative implementation order for any future
implementation phase:

1. **config + allowlist / denylist.** No I/O; no network;
   pure logic.
2. **manifest + raw writer + checksum.** Local-only; atomic
   write.
3. **aggTrades** (historical / archive planning only or public
   REST/WS collector if separately authorised). Lane B
   strongest candidate; smallest dataset.
4. **schema validation.** Per-family validators; consume raw
   files only.
5. **eligibility gate skeleton.** Single-family path first;
   no flag-flipping until all checks pass.
6. **bookTicker collector.** WS-only; small payloads.
7. **depthDiff + REST depth snapshot.** Paired; sequence
   bookkeeping mandatory.
8. **deterministic LOB replay.** Consumes the previous step's
   raw layer; no re-fetch.
9. **forceOrder proxy collector.** WS-only; bounded.
10. **OI / funding REST polling.** Multiple endpoints under
    one collector with shared rate-limit budget.
11. **health-check reporter.**
12. **local dashboard hook.**

### 18.1 Why aggTrades is the safest first implementation target

- **Historically available** at `data.binance.vision`
  (per Phase 4at §6.1 / §8 / §9.1), so a future scaffold
  phase can validate end-to-end correctness from archive
  alone before any WS / REST forward capture is wired up.
- **Smaller than depth.** Per-event records aggregated at
  100 ms with one record per (price, taker side); no full
  book to reconstruct.
- **Directly relevant to Lane B** (M-5 aggressive volume /
  taker imbalance; M-6 trade burst). Phase 4at recorded
  Lane B as the strongest follow-on mechanism feasibility
  lane.
- **Avoids immediate LOB replay complexity.** Reconstructing
  the order book is the highest implementation risk; doing
  it after aggTrades is mature reduces blast radius.

**Phase 4av implements no step in this order.**

---

## 19. Future test matrix

A future implementation phase must produce the following
tests. **No test is created in Phase 4av.**

| Test family | Module under test | Type | Notes |
|---|---|---|---|
| Config validation | `config.py` | unit | golden / malformed / unknown-field |
| Allowlist / denylist | `allowlist.py` | unit | every Phase 4au allowlist + denylist entry |
| No-secret / no-`.env` | `config.py` + import-boundary | unit | no `os.environ` access beyond a documented allowlist |
| Raw writer atomic | `raw_writer.py` | unit | atomic write; `.tmp` cleanup; SHA256 pairing |
| Checksum | `raw_writer.py` + `manifest.py` | unit | SHA256 mismatch detection |
| Manifest append | `manifest.py` | unit | append-only invariant; immutable fields |
| Schema validation | `schema.py` | unit | per-family golden / malformed |
| Invalid-window enum | `invalid_window.py` | unit | every reason round-trips |
| aggTrade sequence | `collectors/aggtrade.py` | unit | sequence-gap detection |
| bookTicker spread sanity | `collectors/bookticker.py` | unit | impossible-spread detection |
| depthDiff `U/u/pu` gap | `collectors/depthdiff.py` | unit | gap → resync → invalid window |
| REST snapshot bracketing | `collectors/depth_snapshot.py` | unit | first-event bracketing rule |
| LOB replay golden | `replay/lob.py` | golden | byte-identical output under fixed config |
| forceOrder proxy label | `collectors/forceorder_proxy.py` | unit | manifest carries `proxy_warning` |
| OI / funding retention label | `collectors/oi_funding.py` | unit | manifest carries `retention_warning` for recent-only families |
| Eligibility gate | `eligibility_gate.py` | unit | every check pass / fail; partial-pass for OI subset |
| CLI dry-run | every CLI subcommand | unit | dry-run prints planned actions; no I/O |
| Import boundaries | `test_import_boundaries.py` | unit | grep / AST-walk asserts no forbidden imports |
| No endpoint call | every collector test | unit | I/O mocked; no real network |
| No network by default | global pytest config | unit | a fixture flag forbids network calls |

---

## 20. Future failure-mode matrix

| Failure mode | Future behaviour | Fail-open / closed | Invalid-window action | Manifest action | Test requirement |
|---|---|---|---|---|---|
| Network timeout (REST) | jittered exponential backoff up to N retries | fail closed after N | none unless retention gap caused | log only | unit |
| HTTP 429 | exponential backoff (5s → 5min); resume in plan order | fail closed | none unless coverage gap | log only | unit |
| HTTP 418 | permanent halt of REST worker; alert via dashboard | fail closed | record retention gap | append `rest_retention_gap` | unit |
| WebSocket disconnect | jittered exponential reconnect; gap recorded | fail closed | record `gap_after_reconnect` | append | unit |
| Stale stream | reconnect; gap recorded | fail closed | record `stale_stream` | append | unit |
| Queue backpressure | FIFO discipline; refuse new events; persistent saturation triggers managed reconnect | fail closed | record `gap_after_reconnect` if reconnect needed | append | unit |
| Partial file write | delete `.tmp`; record `failed_atomic_write` | fail closed | record `failed_atomic_write` / `partial_file_recovery_event` | append | unit |
| Corrupt checksum | quarantine file; refuse to consume | fail closed | record `archive_checksum_mismatch` | append | unit |
| Schema mismatch | reject row; quarantine file | fail closed | record under family-specific reason | append | unit |
| Sequence gap | resync; record gap | fail closed | record `missing_sequence` / `gap_after_reconnect` | append | unit |
| Snapshot mismatch | refetch snapshot; restart partition | fail closed | record `snapshot_mismatch` | append | unit |
| Impossible spread | quarantine row; force resync | fail closed | record `impossible_spread` | append | unit |
| Clock skew | flag and continue | fail open (warn) | record `clock_skew` | append (severity=warn) | unit |
| Disk full | halt all writers; alert via dashboard | fail closed | record `failed_atomic_write` if applicable | append on resume | unit |
| Permission error | halt affected writer; alert | fail closed | record `failed_atomic_write` if applicable | append on resume | unit |
| Malformed JSON | quarantine event; record | fail closed | record under family-specific reason | append | unit |
| Unexpected field | log warning; preserve row | fail open (warn) | optional `flag` action | optional | unit |
| Missing field | reject row | fail closed | record `schema_mismatch`-equivalent reason | append | unit |
| Symbol mismatch | reject row | fail closed | record `symbol_mismatch` | append | unit |
| Proxy incompleteness (forceOrder) | flag and continue (proxy semantics) | fail open (warn) | record `force_order_proxy_incompleteness` | append (severity=warn; action=proxy_only) | unit |

---

## 21. Future validation commands

A future implementation phase would need to run, at minimum:

- `ruff check src/prometheus/research/microstructure tests/research/microstructure scripts/microstructure_*.py`
- `mypy src/prometheus/research/microstructure scripts/microstructure_*.py` (strict, if the repo applies it to new modules; the v1 project precedent is strict mypy on `src/prometheus/`).
- `pytest tests/research/microstructure -k "not network"` (network tests are gated and run separately if ever authorised).
- `python -m compileall src/prometheus/research/microstructure scripts/microstructure_*.py`.
- An import-boundary check (grep or AST-walk) verifying that
  no module under
  `src/prometheus/research/microstructure/` imports
  `prometheus.runtime`, `prometheus.execution`,
  `prometheus.persistence`, `binance`, `python-binance`,
  signature helpers, or authentication helpers.
- A no-network test mode (pytest fixture) that fails any test
  that opens a real socket.
- `git diff --check` (whitespace).

**Phase 4av runs none of these.** Phase 4av is docs-only;
`git diff --check` and `git status` are the only project-
convention validations needed for this docs-only phase.

---

## 22. Future implementation stop conditions

Any future implementation phase derived from this plan must
**halt before commit** if any of the following appears:

- Any private endpoint appears in the allowlist.
- Any credential path appears (file path, environment
  variable, config field).
- Any user-stream / `listenKey` path appears.
- Any order-placement endpoint path appears.
- Any source imports
  `prometheus.runtime`, `prometheus.execution`, or
  `prometheus.persistence`.
- Any actual endpoint call occurs in non-mocked tests.
- Any data directory under `data/microstructure/...` is
  created **before** `.gitignore` is updated and authorisation
  is confirmed in the implementation phase's brief.
- Any manifest flips `research_eligible: true` outside the
  eligibility-gate code path.
- Any invalid window is silently filled (forward-fill,
  interpolation, imputation, replacement).
- Any markPrice stop-domain use bypasses Phase 3r §8 /
  Phase 3v §8 governance.
- Any old-strategy rescue interpretation appears (R3-prime /
  R2-prime / R1a-prime / R1b-narrow-prime / H0-prime /
  F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow /
  V2-relaxed / V2 hybrid / G1-prime / G1-narrow /
  G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid / V1-D1 / F1-D1 / cross-strategy
  hybrid).
- Any strategy logic or ML logic appears.

---

## 23. Future implementation branch strategy

A future implementation effort may be split into narrowly-
scoped phases, each separately operator-authorised:

1. **Phase 4aw — Public-Only Microstructure Capture Scaffold
   Implementation** (allowed scope only):
   `src/prometheus/research/microstructure/__init__.py`,
   `config.py`, `allowlist.py`, `invalid_window.py`,
   `manifest.py` (no live writes), `raw_writer.py` (no live
   writes), test scaffolding, import-boundary tests, a
   `.gitignore` line for `data/microstructure/`. **No
   collectors, no endpoint calls, no archive downloads, no
   WebSockets.**
2. **Phase 4ax — aggTrades-only capture phase.** Adds
   `collectors/aggtrade.py`, `public_rest.py`, `public_ws.py`
   (aggTrade only), the `capture aggtrades` CLI subcommand,
   schema validation for aggTrades, and family
   `microstructure_raw_aggtrades_v001`. May download from
   `data.binance.vision` if the phase brief explicitly
   authorises it.
3. **Phase 4ay — manifest / eligibility phase.** Activates
   the eligibility gate for `microstructure_raw_aggtrades_v001`
   only.
4. **Phase 4az — depth / LOB replay phase.** Adds
   bookTicker, depthDiff, depth snapshot, LOB replay.
5. **Phase 4ba — forceOrder / OI context phase.** Adds
   forceOrder proxy and OI / funding REST polling.

**Phase 4av does not authorise Phase 4aw, 4ax, 4ay, 4az, or
4ba.** Each requires its own operator-authorised brief that
itself must satisfy M0 admissibility.

---

## 24. Security / credential implementation plan

Required future tests / checks:

- **No `.env` reads.** Both an import-boundary test and a
  runtime invariant: `config.py` does not call
  `dotenv.load_dotenv` and does not read any `.env` file;
  `os.environ` access is bounded to a documented allowlist
  (e.g. `LOG_LEVEL` only).
- **No API-key arguments.** CLI parsers must reject
  `--api-key` / `--secret` / `--listen-key` / `--user-stream`
  / `--order` / `--leverage` / `--margin` / `--mcp-config` /
  `--graphify` flags by construction.
- **No secret config fields.** `config.py` Pydantic / dataclass
  models must not include credential-shaped fields; an
  unknown field is a hard error.
- **No signed-request helpers.** No HMAC helper, no signature
  helper, no timestamp-and-sign helper anywhere in the
  package.
- **No private endpoint strings.** A repo-wide grep for known
  private endpoint substrings (`/fapi/v1/order`, `/fapi/v2/account`,
  `/fapi/v2/positionRisk`, `/fapi/v1/leverage`,
  `/fapi/v1/marginType`, `/fapi/v1/forceOrders`,
  `userDataStream`, `listenKey`) must return zero matches in
  the microstructure namespace.
- **No user stream / `listenKey`.** Same grep.
- **No order endpoints.** Same grep.
- **No leverage / margin endpoints.** Same grep.
- **No MCP / Graphify / `.mcp.json`.** Same grep; plus a test
  that the package does not import any MCP / Graphify
  client.

**Phase 4av implements none of these tests.** They are
specified as required for any future implementation phase.

---

## 25. Runtime separation implementation plan

Required future import-boundary rules:

- **No imports from `prometheus.runtime`.** Enforced by
  `test_import_boundaries.py`.
- **No imports from `prometheus.execution`.** Enforced by
  `test_import_boundaries.py`.
- **No imports from `prometheus.persistence`.** Enforced by
  `test_import_boundaries.py`.
- **No runtime database writes.** The microstructure package
  must not open the runtime SQLite database, either directly
  or through any helper.
- **No safety-state mutation.** The runtime safety state
  (kill-switch, runtime mode, exposure gates) is invisible to
  the microstructure package.
- **No order-router contact.** No code path that could enqueue
  an order; even via a fake adapter.
- **Capture is research infrastructure only.**

**Phase 4av implements none of these.**

---

## 26. Symbol / scope implementation plan

- **BTCUSDT primary.** Default capture set is BTCUSDT
  (project-locked first-live symbol).
- **ETHUSDT comparison.** ETHUSDT is captured as comparison
  context only.
- **No alt-symbol mining.**
- **Phase 4ac core symbols only if separately authorised.**
  SOLUSDT / XRPUSDT / ADAUSDT may be added later only if a
  separately-authorised symbol-extension memo is approved.
- **No old-strategy alt-symbol rerun.**
- **Symbol-specific future study must be mechanism-first.**
  Per Phase 4as §13 and Phase 4at symbol policy.

---

## 27. M0 and no-rescue implications

- **Implementation planning is infrastructure planning only.**
  Phase 4av is a research-infrastructure planning memo. It
  does not propose a strategy candidate, a feature, or a
  mechanism-feasibility claim.
- **No edge claim.** A future implementation pipeline says
  nothing about whether any microstructure mechanism contains
  edge under §11.6.
- **No cooled-down family is reopened.** Cooled-down lanes
  (per Phase 4ak post-null cooldown rule) remain cooled down.
- **No R3 / R2 / V1-arc rescue.** The future implementation
  must not be used as a backdoor to re-run R3 / R2 / R1a /
  R1b-narrow / H0 / F1 / D1-A / V2 / G1 / C1 with new
  microstructure features added.
- **No D1-A funding-trigger reuse.** Funding is **context
  only**.
- **No G1 / V2 / C1 hidden wrapper.** Phase 4al refined no-
  rescue rule applies.
- **No strategy until data quality and mechanism feasibility
  are established.** Capture is infrastructure; strategy work
  is gated independently.

---

## 28. Recommended next phase

The cleanest possible separately-authorised next move, **if
the operator chooses one after reviewing Phase 4av**, is:

**Phase 4aw — Public-Only Microstructure Capture Scaffold
Implementation**

- **Type:** code-and-docs implementation phase, but **limited
  scope only**: scaffold (`__init__.py`, `config.py`,
  `allowlist.py`, `invalid_window.py`, `manifest.py` with no
  live writes, `raw_writer.py` with no live writes), test
  scaffolding, import-boundary tests, and a `.gitignore` line
  for `data/microstructure/`.
- **Forbidden in Phase 4aw if ever authorised:** no live
  endpoint calls, no archive downloads, no WebSockets, no
  data acquisition, no actual manifest creation, no actual
  raw file writes (manifest and writer modules have unit-test
  coverage only with mocked filesystem at this phase).
- **Authorisation status:** **NOT authorised by Phase 4av.**
  The operator may later authorise Phase 4aw as a separate
  decision.

### 28.1 Acceptable alternative recommendation

Remain paused, or run a narrower docs-only implementation-
risk review before any code, if the operator concludes that
more design review is needed before any scaffold
implementation.

### 28.2 What Phase 4av does NOT recommend

- No immediate implementation.
- No immediate endpoint calls.
- No immediate WebSocket connections.
- No immediate archive downloads.
- No immediate capture.
- No immediate ML or strategy work.

---

## 29. Explicit non-recommendations

The following are **not** recommended by Phase 4av. Several
are explicitly forbidden by prior governance:

- No immediate data acquisition.
- No endpoint calls.
- No WebSockets.
- No archive downloads.
- No capture implementation by Phase 4av.
- No strategy.
- No ML.
- No old-strategy alt-symbol rerun.
- No 5m research thread reopening.
- No verdict / lock revision.
- No M0 amendment.
- No D1-A funding-trigger reuse.
- No G1 / V2 / C1 rescue under a microstructure label.
- No authorisation of paper / shadow / live-readiness /
  deployment / exchange-write / production-key creation /
  authenticated APIs / private endpoints / public-endpoint
  calls in code / user stream / WebSocket implementation /
  MCP / Graphify / `.mcp.json` / credentials.

---

## 30. Implementation / governance review

### What changed?

- New file: this memo at
  `docs/00-meta/implementation-reports/2026-05-07_phase-4av_public-only-microstructure-capture-implementation-plan.md`.
- Narrow update to `docs/00-meta/current-project-state.md` —
  Phase 4av narrative paragraph and "Current phase:" block
  update, with the prior Phase 4au block preserved as
  historical context (matching prior-phase convention).

### What did not change?

- No `src/prometheus/` modification.
- No test under `tests/` modified.
- No existing script under `scripts/` modified.
- No data file under `data/raw/`, `data/normalized/`,
  `data/derived/` modified.
- No manifest under `data/manifests/` modified or created.
- No actual dataset directory created under
  `data/microstructure/...`.
- No actual manifest created.
- No schema-as-code, config file, or module-stub created.
- No `research_eligible` flag flipped.
- No v003 created.
- No `.gitignore` modified.
- No specialist governance file modified beyond the narrow
  current-project-state update (no Phase 3r §8 / Phase 3v §8 /
  Phase 3w / Phase 4j §11 / Phase 4k / Phase 4p / Phase 4q /
  Phase 4v / Phase 4w / Phase 4ak / Phase 4al / Phase 4am /
  Phase 4an / Phase 4ao / Phase 4ap / Phase 4aq / Phase 4ar /
  Phase 4as / Phase 4at / Phase 4au modification).
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No reopening of the 5m research thread.
- No data acquisition.
- No backtest run.
- No historical strategy script executed.
- No Phase 4aq script re-execution.
- No `data/research/` content committed.
- No Binance endpoint called.
- No WebSocket opened.
- No archive downloaded.
- No capture, replay, or feature implementation.

### Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are
preserved verbatim. M0 governance is unchanged. The 5m
closure (Phase 3t) is preserved. The cost lock (§11.6) and
project locks (§1.7.3) are preserved. The stop-trigger-domain
governance (Phase 3v §8), break-even / EMA slope / stagnation
governance (Phase 3w §6 / §7 / §8), mark-price gap governance
(Phase 3r §8), and OI subset governance (Phase 4j §11) are all
preserved. The Phase 4ak M0 gate, post-null cooldown rule,
cooled-down families list, and memo template are all
preserved. The Phase 4al refined no-rescue rule, the Phase 4am
audit findings, the Phase 4an inventory, the Phase 4ao
harmonization, the Phase 4ap forensic plan, the Phase 4aq
computation, the Phase 4ar interpretation, the Phase 4as
mechanism map, the Phase 4at availability map, and the
Phase 4au design specification are all preserved.

### Were any historical scripts, source files, existing data, manifests, or tests modified?

No. Phase 4av is a docs-only implementation-planning memo.

### Is the phase mergeable as docs-only?

Yes. Phase 4av adds two markdown files under
`docs/00-meta/implementation-reports/` plus a narrow update
to `docs/00-meta/current-project-state.md`. Per the operator's
instruction in this prompt, **Phase 4av is not merged in this
prompt**.

---

## 31. Research interpretation review (plain English)

### What did this phase prove?

Phase 4av did not prove anything in the predictive-statistics
sense. As a docs-only implementation-planning memo it
documents, in implementation-ready detail, a future public-
only Binance microstructure capture pipeline implementation
plan covering proposed file / module layout, CLI surface,
config sections, manifest implementation steps, schema
implementation order, invalid-window error-class enumeration
covering all seventeen Phase 4au triggers, eligibility-gate
implementation steps, deterministic-replay implementation
steps, local-order-book reconstruction implementation steps,
collector implementation order with rationale for aggTrades-
first, test matrix, failure-mode matrix, validation-command
list, stop-conditions list, branch strategy, security /
credential plan, runtime-separation plan, and symbol / scope
plan — without implementing any of it.

### What did this phase not prove?

Phase 4av did not prove that any specific microstructure
mechanism contains edge. It did not run any computation. It
did not acquire any data. It did not call any Binance
endpoint or open any WebSocket. It did not authorise any
successor phase. It did not implement any capture, replay,
feature, or strategy. It did not amend M0. It did not modify
any verdict or lock. It did not create a strategy candidate.
It did not create any source / test / data / manifest /
dataset directory artefact.

### Which original questions did it answer?

The Phase 4av question — "If the operator later authorizes a
public-only Binance microstructure capture implementation,
exactly what files, modules, CLI commands, configs, schemas,
manifests, tests, validation gates, failure modes,
implementation order, and stop conditions should that future
implementation follow?" — is answered across §6 (future
implementation scope), §7 (future implementation non-scope),
§8 (proposed future file / module plan), §9 (future CLI
design), §10 (future configuration design), §11 (storage and
`.gitignore` plan), §12 (future manifest implementation
plan), §13 (future schema implementation plan), §14 (future
invalid-window implementation plan), §15 (future eligibility-
gate implementation plan), §16 (future deterministic-replay
implementation plan), §17 (future LOB reconstruction
implementation plan), §18 (future collector implementation
order), §19 (future test matrix), §20 (future failure-mode
matrix), §21 (future validation-command list), §22 (future
implementation stop-conditions), §23 (future implementation
branch strategy), §24 (security / credential implementation
plan), §25 (runtime-separation implementation plan), §26
(symbol / scope implementation plan), §27 (M0 / no-rescue
implications), §28 (recommended next phase Phase 4aw).

### Which original questions remain open?

- Whether any of the M-1 → M-14 mechanisms contains edge
  under the project's locked cost realism. **This is not
  answered by Phase 4av and should not be answered by
  Phase 4av.**
- Whether Phase 4aw (a future scaffold-only implementation
  phase) is the cleanest next move. The memo recommends
  Phase 4aw but does **not** authorise it.
- Whether storage and operational overhead for live capture
  is acceptable for the project's host in numeric terms. The
  Phase 4av memo defers this to a future implementation-
  sizing memo if needed before any forward-capture phase.

### What does it mean for strategy research?

Phase 4av confirms that Lane A — Binance microstructure data
availability / capture feasibility — now has an exhaustive
public-availability map (Phase 4at), an implementation-ready
capture design specification (Phase 4au), and an
implementation-ready implementation plan (Phase 4av) at the
docs layer. Together they form a complete docs-only
foundation that any future scaffold implementation phase can
build against. The cooled-down families list, the
six-candidate rejection topology, the cost lock, the position
lock, the leverage lock, and the mark-price stop lock are all
preserved. M0 remains the binding admissibility framework.

### What does it mean for governance?

Phase 4av reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3,
Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11,
Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak
adoption, Phase 4al refined no-rescue + §13 / §14, Phase 4am
§11.A audit findings, Phase 4an inventory, Phase 4ao
harmonization, Phase 4ap forensic plan, Phase 4aq computation
result preserved as descriptive evidence only, Phase 4ar
interpretation result preserved as descriptive interpretation
only, Phase 4as mechanism-map result preserved as docs-only
reset evidence only, Phase 4at availability map preserved as
docs-only feasibility evidence only, and Phase 4au design
specification preserved as docs-only design evidence only.
**None is amended.**

### What is the clean next step?

Operator review of Phase 4av. **No successor phase is
authorised by Phase 4av.** Acceptable separately-authorised
future options include remain paused (recommended), Phase 4aw
as a docs-and-code scaffold-only implementation phase (with a
strict allowed-scope list), or further docs-only governance
memos on precise governance questions. None is started or
authorised by Phase 4av.

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
  implementation / MCP / Graphify / `.mcp.json` /
  credentials.

---

## 32. Preserved verdicts, locks, and no-rescue constraints

### Retained verdict ledger (preserved verbatim)

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

### Project locks (preserved verbatim)

- **§11.6** = 8 bps slippage per side; round-trip = 16 bps.
- **§1.7.3** = 0.25 % risk; 2× leverage cap; one position
  max; mark-price stops where applicable.
- **Phase 3r §8** mark-price gap governance.
- **Phase 3v §8** stop-trigger-domain governance.
- **Phase 3w §6 / §7 / §8** break-even / EMA slope /
  stagnation governance.
- **Phase 4j §11** metrics OI-subset partial-eligibility rule.
- **Phase 4k** V2 backtest-plan methodology.
- **Phase 4p** G1 strategy-spec memo.
- **Phase 4q** G1 backtest-plan methodology.
- **Phase 4v** C1 strategy-spec memo.
- **Phase 4w** C1 backtest-plan methodology.
- **Phase 4ak** M0 mechanism-admissibility gate adoption
  (twelve clauses + post-null cooldown + cooled-down families
  list + memo template).
- **Phase 4al** refined no-rescue rule + §13 future-phase
  boundary + §14 data-resolution hierarchy.
- **Phase 4am** §11.A audit findings.
- **Phase 4an** historical-trade-population exit-path
  inventory.
- **Phase 4ao** exit-path methodology / artefact harmonization.
- **Phase 4ap** V1-Arc Exit-Path Forensic Plan.
- **Phase 4aq** computation result preserved as descriptive
  evidence only.
- **Phase 4ar** interpretation result preserved as descriptive
  interpretation only.
- **Phase 4as** mechanism-map result preserved as docs-only
  reset evidence only.
- **Phase 4at** availability / capture-feasibility result
  preserved as docs-only feasibility evidence only.
- **Phase 4au** capture-design result preserved as docs-only
  design evidence only.

### No-rescue constraints (preserved)

- No R3-prime / R2-prime / R1a-prime / R1b-narrow-prime /
  H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime /
  V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow /
  G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-
  strategy hybrid.
- No window / threshold / parameter mining from Phase 4l /
  Phase 4r / Phase 4x forensic numbers.
- No reopening of the 5m research thread.
- No silent reduction of microstructure to a rank-then-trade
  variant of any cooled-down candidate.
- No microstructure use of optional metrics ratio columns
  outside Phase 4j §11.
- No D1-A reuse as a directional trigger; funding remains a
  context lens only if ever used.

### Boundaries not altered

- No M0 amendment.
- No Phase 4m 18-requirement validity-gate amendment.
- No Phase 4t 10-dimension scoring-matrix amendment.
- No Phase 4u opportunity-rate-vs-edge-rate amendment.
- No Phase 4w negative-baseline / PBO / DSR / CSCV amendment.
- No Phase 4z framework adoption.
- No Phase 4al / Phase 4am audit-finding amendment.
- No Phase 4an / Phase 4ao / Phase 4ap / Phase 4aq /
  Phase 4ar / Phase 4as / Phase 4at / Phase 4au amendment.

---

## 33. Final status

Phase 4av is complete on branch
`phase-4av/public-only-microstructure-capture-implementation-plan`.

- **Memo:** this file.
- **Closeout:** to be added at
  `docs/00-meta/implementation-reports/2026-05-07_phase-4av_closeout.md`
  in the next commit on this branch.
- **Successor authorisation:** none. **Phase 4aw / Phase 5 /
  Phase 4 canonical / paper / shadow / live-readiness /
  deployment / exchange-write / production-key /
  authenticated APIs / private endpoints / user stream /
  WebSocket implementation / MCP / Graphify / `.mcp.json` /
  credentials all remain unauthorised.** Acquisition of
  5m / 1m / aggTrades / tick / mark-price 30m / 4h / order-
  book data also remains unauthorised.
- **Recommended state:** **paused** unless the operator
  separately authorises a future phase. The merge of
  Phase 4av into `main` is itself a separate operator
  decision and is **not** performed by this prompt.

## End of Phase 4av memo
