# Phase 4av Merge Closeout — Public-Only Microstructure Capture Implementation Plan

## Merge identity

- **Phase:** 4av.
- **Phase title:** Public-Only Microstructure Capture
  Implementation Plan.
- **Phase type:** docs-only implementation-planning memo.
- **Target branch:** `main`.
- **Source branch:**
  `phase-4av/public-only-microstructure-capture-implementation-plan`.
- **Merge method:** `--no-ff` (preserves the Phase 4av branch
  history as a discrete merge node on `main`).
- **Main before merge SHA:** `6e9521bbba5f2af8ca19f4789de4c9034c7a301a`.
- **Phase 4av memo commit SHA:**
  `bf11d4b52d7485fcc2bdab5a7972c81fa590ac17`
  (`docs(phase-4av): plan public-only microstructure capture implementation`).
- **Phase 4av closeout commit SHA:**
  `b67a679eb3b81299c4892cb426d8f8b53690db2f`
  (`docs(phase-4av): add closeout`).
- **Merge commit SHA:** recorded in this merge closeout's final
  operator report (and in the live `git log` on `main`) once
  the merge commit lands. Self-referential SHA-in-content is
  avoided per prior-phase convention.

## Merge purpose

This merge brings the Phase 4av docs-only public-only
microstructure capture implementation plan onto `main`,
together with the Phase 4av closeout and a narrow Phase 4av
update to `docs/00-meta/current-project-state.md`. Phase 4av
translates the Phase 4au Binance Microstructure Capture Design
Specification into a precise, file-by-file future
implementation plan — without implementing anything.

The merge is **docs-only**. It brings forward the Phase 4av
memo, the Phase 4av closeout, and the narrow current-project-
state update. It does **not** authorise any successor phase,
data acquisition, endpoint call, public-archive download,
WebSocket connection, capture / replay / order-book-
reconstruction code, feature implementation, ML model,
strategy candidate, paper / shadow, live-readiness,
deployment, exchange-write, production-key creation,
authenticated APIs, private endpoints, user stream, WebSocket
implementation, MCP, Graphify, `.mcp.json`, credentials, or
any 5m / 1m / aggTrades / tick / mark-price 30m / 4h /
order-book data acquisition.

## Files brought forward

- `docs/00-meta/implementation-reports/2026-05-07_phase-4av_public-only-microstructure-capture-implementation-plan.md`
  — Phase 4av main memo (33 sections; +2,058 lines).
- `docs/00-meta/implementation-reports/2026-05-07_phase-4av_closeout.md`
  — Phase 4av closeout (+729 lines).
- `docs/00-meta/current-project-state.md`
  — narrow update: Phase 4av narrative paragraph + Phase 4av
  "Current phase:" block + transition lines preserving the
  prior Phase 4au block as historical context (matching
  prior-phase convention).

This merge closeout adds:

- `docs/00-meta/implementation-reports/2026-05-07_phase-4av_merge-closeout.md`
  — this file.

No other file is changed by this merge.

## Confirmation Phase 4av was docs-only

Phase 4av is a docs-only implementation-planning memo. The
merge brings forward only:

- the Phase 4av memo,
- the Phase 4av closeout,
- the narrow `current-project-state.md` update,
- this merge closeout.

No script was added or executed. No backtest was run. No data
was acquired. No Binance endpoint was called. No WebSocket
was opened. No archive file was downloaded. No code under
`src/prometheus/` was modified. No test was modified. No
existing script was modified. No `.gitignore` change was
made. No `data/research/` content was committed. **No
directory under `data/microstructure/...` was created.** **No
actual manifest file was created.** No schema-as-code, config
file, module stub, or capture-code artefact was created.

`ruff check`, `pytest`, and `mypy` were **not** run because
the phase is docs-only (no `src/prometheus/`, test, script,
or `scripts/` change of any kind). This matches the docs-only
convention used by prior docs-only phases.

## Phase 4av implementation-plan result

Phase 4av translates the Phase 4au design specification into a
precise file-by-file future implementation plan. **None of
the plan is implemented.**

### Proposed future file / module layout summary

A hypothetical
`src/prometheus/research/microstructure/` namespace plus a
`scripts/microstructure_*` CLI surface and a paired
`tests/research/microstructure/` test tree, with per-module
purpose / allowed imports / forbidden imports / public API /
inputs / outputs / failure modes / tests / governance notes:

- `__init__.py` (package marker; no executable logic).
- `config.py` (config loader; no `.env`; no secrets).
- `allowlist.py` (Phase 4au allowlist + denylist as the only
  source of truth).
- `public_rest.py` (public-only REST wrapper; no signed
  helpers).
- `public_ws.py` (public-only WS wrapper; no user stream;
  no `listenKey`).
- `raw_writer.py` (append-only JSONL.zst writer; atomic
  write-then-rename; SHA256 pairing).
- `manifest.py` (append-only manifest; only path that may
  flip `research_eligible`).
- `schema.py` (per-family validators).
- `invalid_window.py` (closed enum of seventeen reasons +
  `InvalidWindow` dataclass).
- `collectors/aggtrade.py`, `collectors/bookticker.py`,
  `collectors/depthdiff.py`, `collectors/depth_snapshot.py`,
  `collectors/forceorder_proxy.py`,
  `collectors/oi_funding.py`.
- `normalizer.py` (deterministic batch normalizer).
- `replay/lob.py`, `replay/deterministic.py` (deterministic
  replay; LOB reconstruction).
- `eligibility_gate.py` (Phase 4au §22 ten checks; only path
  that may flip `research_eligible: true`).
- `healthcheck.py` (local-only structured signals).
- `dashboard_hook.py` (read-only consumer of healthcheck;
  no order panel; no kill-switch surface).
- `scripts/microstructure_capture.py`,
  `scripts/microstructure_replay.py`,
  `scripts/microstructure_eligibility_gate.py` (CLIs).
- `tests/research/microstructure/` (per-module tests + global
  import-boundary test).

**None created.**

### Future CLI surface summary

Eleven planned subcommands: `capture aggtrades`;
`capture bookticker`; `capture depthdiff`;
`capture forceorder`; `poll oi-funding`; `snapshot depth`;
`normalize`; `replay lob`; `validate-schema`;
`eligibility-gate`; `health-report`. Per subcommand:
required / optional / forbidden flags, dry-run behaviour,
output paths, stop conditions, and logging expectations.
**None implemented.**

### Future config plan summary

Twelve config sections: endpoint allowlist; endpoint
denylist; symbol allowlist; dataset family config; storage
root; capture cadence; WebSocket reconnect; REST rate-limit
budgets; invalid-window thresholds; eligibility-gate
thresholds; replay settings; health-check settings. Forbidden
config fields: no API keys; no `.env` reads; no MCP /
Graphify / `.mcp.json` / credential-shaped fields. **No
config file is created.**

### Future storage / `.gitignore` plan summary

Recommends a `data/microstructure/` `.gitignore` line for any
future implementation phase, **before** any directory is
created. **Phase 4av does not modify `.gitignore` and does
not create any directory under `data/microstructure/...`.**

### Future manifest implementation plan summary

Translates Phase 4au §13 into ten implementation steps:
manifest schema; append-only updates; SHA256 pairing;
per-file event counts; invalid windows;
`research_eligible: false` default;
`eligibility_gate_status: pending` default;
`code_commit_sha`; `capture_config_hash`;
`endpoint_docs_reference`. **No manifest is created.**

### Future schema implementation order summary

aggTrades first; bookTicker second; depthDiff + depthSnapshot
third; forceOrder proxy fourth; OI / funding metrics fifth;
markPrice only if separately authorised; replay LOB derived
schema after depthDiff. **No schema file is created.**

### Future invalid-window plan summary (seventeen triggers)

`missing_sequence`, `out_of_order_event`, `duplicate_event`,
`gap_after_reconnect`, `snapshot_mismatch`, `clock_skew`,
`symbol_mismatch`, `stale_stream`, `stale_book`,
`impossible_spread`, `negative_size`, `zero_or_invalid_price`,
`archive_checksum_mismatch`, `rest_retention_gap`,
`force_order_proxy_incompleteness`, `failed_atomic_write`,
`partial_file_recovery_event`. Per-trigger detection point /
severity / downstream eligibility action / required evidence
/ tests recorded. **No enum or class created.** **No silent
forward-fill / interpolation / imputation / replacement** at
any layer.

### Future eligibility-gate plan summary

Translates the ten Phase 4au §22 checks (raw files present;
checksum pass; schema validation pass; timestamp sanity
pass; sequence continuity pass; invalid-window threshold;
retention completeness label; proxy limitation label;
governance labels; final `research_eligible` decision) into
implementation steps. **The eligibility gate is not
implemented and no `research_eligible` flag is flipped by
Phase 4av.** The gate is the only path that may flip
`research_eligible: true`.

### Future deterministic replay plan summary

Raw → normalized; normalized → derived; LOB replay;
`replay_config_hash`; byte-identical output requirement;
replay logs; replay failure handling; **no ad-hoc raw reads
by research code.** **Not implemented.**

### Future LOB reconstruction plan summary

Snapshot fetcher; diff buffer; first-event bracketing
(`U <= lastUpdateId AND u >= lastUpdateId`); `U` / `u` / `pu`
continuity validation; apply-diff engine; top-N extractor;
stale-book detector; impossible-spread detector; resync
handler; invalid-window writer. **Not implemented.**

### Future collector implementation order summary, including aggTrades-first rationale

Conservative twelve-step order: 1 config + allowlist /
denylist; 2 manifest + raw writer + checksum; 3 aggTrades
historical / archive planning only or public REST/WS
collector if separately authorised; 4 schema validation;
5 eligibility gate skeleton; 6 bookTicker collector;
7 depthDiff + REST depth snapshot; 8 deterministic LOB
replay; 9 forceOrder proxy collector; 10 OI / funding REST
polling; 11 health-check reporter; 12 local dashboard hook.

**aggTrades-first rationale:** historically available at
`data.binance.vision`, so a future scaffold phase can validate
end-to-end correctness from archive alone before any WS / REST
forward capture is wired up; smaller than depth (per-event
records aggregated at 100 ms with one record per (price,
taker side); no full book to reconstruct); directly relevant
to Lane B (M-5 aggressive volume / taker imbalance; M-6 trade
burst); avoids immediate LOB replay complexity (reconstructing
the order book is the highest implementation risk; doing it
after aggTrades is mature reduces blast radius).

### Future test matrix summary

Twenty test families: config validation; allowlist /
denylist; no-secret / no-`.env`; raw writer atomic;
checksum; manifest append; schema validation; invalid-window
enum; aggTrade sequence; bookTicker spread sanity; depthDiff
`U/u/pu` gap; REST snapshot bracketing; LOB replay golden;
forceOrder proxy label; OI / funding retention label;
eligibility gate; CLI dry-run; import boundaries; no endpoint
call; no network by default. **No test is created.**

### Future failure-mode matrix summary

Twenty failure modes: network timeout; HTTP 429; HTTP 418;
WebSocket disconnect; stale stream; queue backpressure;
partial file write; corrupt checksum; schema mismatch;
sequence gap; snapshot mismatch; impossible spread; clock
skew; disk full; permission error; malformed JSON; unexpected
field; missing field; symbol mismatch; proxy incompleteness.
Each with future behaviour, fail-open / fail-closed
classification, invalid-window action, manifest action, and
test requirement.

### Future implementation stop-conditions summary

Twelve stop conditions any future implementation phase must
respect: any private endpoint in allowlist; any credential
path; any user-stream / `listenKey` path; any order endpoint
path; any source imports `prometheus.runtime` / `execution`
/ `persistence`; any actual endpoint call in non-mocked
tests; any data directory created before `.gitignore` and
authorisation; any manifest flips `research_eligible` outside
the gate; any silently filled invalid window; any markPrice
stop-domain bypass of Phase 3r §8 / 3v §8; any old-strategy
rescue interpretation; any strategy or ML logic.

### Future branch strategy summary

Phase 4aw scaffold-only; Phase 4ax aggTrades-only;
Phase 4ay manifest / eligibility; Phase 4az depth / LOB
replay; Phase 4ba forceOrder / OI context. **None
authorised** by this merge.

### Security / credential boundary summary

No `.env` reads; no API-key arguments; no secret config
fields; no signed-request helpers; no private-endpoint
strings; no user stream; no listenKey; no order endpoints;
no leverage / margin endpoints; no MCP / Graphify /
`.mcp.json`. Required future tests: import-boundary;
repo-wide grep for known private-endpoint substrings;
`os.environ` access bounded to a documented allowlist.

### Runtime separation summary

No imports from `prometheus.runtime` / `execution` /
`persistence`; no runtime database writes; no safety-state
mutation; no order-router contact; capture is research
infrastructure only.

### Symbol / scope plan summary

BTCUSDT primary; ETHUSDT comparison; no alt-symbol mining;
Phase 4ac core symbols only if separately authorised; no
old-strategy alt-symbol rerun; symbol-specific future study
must be mechanism-first.

### M0 / no-rescue implications

Implementation planning is infrastructure planning only; no
edge claim; no cooled-down family is reopened; no R3 / R2 /
V1-arc rescue; no D1-A funding-trigger reuse; no G1 / V2 / C1
hidden wrapper; no strategy until data quality and mechanism
feasibility are established.

## Recommendation

- **Primary recommendation:** remain paused.
- **Conditional secondary (NOT authorized by this merge):**
  Phase 4aw — Public-Only Microstructure Capture Scaffold
  Implementation (docs-and-code; **limited scope only** —
  scaffold (`__init__.py`, `config.py`, `allowlist.py`,
  `invalid_window.py`, `manifest.py` with no live writes,
  `raw_writer.py` with no live writes), test scaffolding,
  import-boundary tests, and a `.gitignore` line for
  `data/microstructure/`; **no live endpoint calls; no
  archive downloads; no WebSockets; no data acquisition; no
  actual manifest creation; no actual raw file writes**).
  No acquisition. No successor authorisation. **Phase 4aw is
  NOT authorized by this merge.**
- **Alternative acceptable recommendation:** remain paused
  if more design / plan review is needed before any
  scaffold implementation.
- **NOT recommended:** immediate implementation; immediate
  endpoint calls; immediate WebSocket connections; immediate
  archive downloads; immediate capture; immediate
  order-book reconstruction; immediate replay; immediate
  feature implementation; immediate ML or strategy work;
  old-strategy alt-symbol rerun; R3 / R2 / V1-arc rescue;
  reopening the 5m research thread; paper / live work.
- **FORBIDDEN:** verdict revision; lock revision; parameter
  optimization; strategy resurrection; M0 amendment;
  reopening the 5m research thread; data acquisition without
  separately authorised data-requirements memo; paper /
  shadow / live-readiness / deployment / exchange-write /
  production-key creation / authenticated APIs / private
  endpoints / public-endpoint calls in code / user stream /
  WebSocket implementation / MCP / Graphify / `.mcp.json` /
  credentials.

## Implementation / governance review

### What changed

- New file: `docs/00-meta/implementation-reports/2026-05-07_phase-4av_public-only-microstructure-capture-implementation-plan.md`
  (Phase 4av main memo).
- New file: `docs/00-meta/implementation-reports/2026-05-07_phase-4av_closeout.md`
  (Phase 4av closeout).
- Narrow update: `docs/00-meta/current-project-state.md`
  (Phase 4av narrative paragraph + Phase 4av "Current phase:"
  block; prior Phase 4au block preserved as historical
  context).
- New file (this merge): `docs/00-meta/implementation-reports/2026-05-07_phase-4av_merge-closeout.md`.

### What did not change

- No `src/prometheus/` modification.
- No test modification.
- No existing-script modification.
- No data / manifest / `research_eligible` / v003 change.
- **No directory under `data/microstructure/...` created.**
- **No actual manifest file created.**
- No schema-as-code, config file, or module-stub artefact
  created.
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
- No archive file downloaded.
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
Phase 4as mechanism map, the Phase 4at availability map, and
the Phase 4au design specification are all preserved.

### Is the merge docs-only?

Yes. The merge brings forward two new memos under
`docs/00-meta/implementation-reports/` plus a narrow update
to `docs/00-meta/current-project-state.md`, plus this merge
closeout. No code, test, script, data, manifest, governance,
or lock change occurs.

## Research interpretation review (plain English)

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
steps, LOB reconstruction implementation steps, collector
implementation order with rationale for aggTrades-first,
test matrix (twenty test families), failure-mode matrix
(twenty failure modes), validation-command list, twelve stop
conditions, branch strategy, security / credential plan,
runtime-separation plan, and symbol / scope plan — without
implementing any of it.

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
implementation follow?" — is answered across §6–§28 of the
Phase 4av memo (future implementation scope; future
implementation non-scope; proposed future file / module
plan; future CLI design; future configuration design;
storage and `.gitignore` plan; future manifest implementation
plan; future schema implementation plan; future invalid-
window implementation plan; future research eligibility gate
implementation plan; future deterministic replay
implementation plan; future LOB reconstruction
implementation plan; future collector implementation order;
future test matrix; future failure-mode matrix; future
validation-command list; future implementation stop-
conditions; future implementation branch strategy; security
/ credential implementation plan; runtime-separation
implementation plan; symbol / scope implementation plan;
M0 / no-rescue implications; recommended next phase
Phase 4aw).

### Which original questions remain open?

- Whether any of the M-1 → M-14 mechanisms contains edge
  under the project's locked cost realism. **This is not
  answered by this merge.**
- Whether Phase 4aw is the cleanest next move. The memo
  recommends Phase 4aw but does **not** authorise it.
- Whether storage and operational overhead for live capture
  is acceptable for the project's host in numeric terms. The
  Phase 4av memo defers this to a future implementation-
  sizing memo if needed before any forward-capture phase.

### What does it mean for strategy research?

This merge confirms that Lane A — Binance microstructure data
availability / capture feasibility — now has an exhaustive
public-availability map (Phase 4at), an implementation-ready
capture design specification (Phase 4au), and an
implementation-ready implementation plan (Phase 4av) at the
docs layer. Together they form a complete docs-only
foundation that any future scaffold implementation phase can
build against. The cooled-down families list, the
six-candidate rejection topology, the cost lock, the position
lock, the leverage lock, and the mark-price stop lock are
all preserved. M0 remains the binding admissibility
framework.

### What does it mean for governance?

This merge reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3,
Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8,
Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v,
Phase 4w, Phase 4ak adoption, Phase 4al refined no-rescue +
§13 / §14, Phase 4am §11.A audit findings, Phase 4an
inventory, Phase 4ao harmonization, Phase 4ap forensic plan,
Phase 4aq computation result preserved as descriptive
evidence only, Phase 4ar interpretation result preserved as
descriptive interpretation only, Phase 4as mechanism-map
result preserved as docs-only reset evidence only,
Phase 4at availability map preserved as docs-only feasibility
evidence only, and Phase 4au design specification preserved
as docs-only design evidence only. **None is amended.**

### What is the clean next step?

Operator review of Phase 4av on `main` after this merge
lands. **No successor phase is authorised by this merge.**
The clean next step is operator-driven only. Acceptable
separately-authorised future options include remain paused
(recommended), Phase 4aw as a docs-and-code scaffold-only
implementation phase (with strict allowed-scope list), or
further docs-only governance memos on precise governance
questions. None is started or authorised by this merge.

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
- **Phase 4av** — implementation-plan result preserved as
  docs-only planning evidence only.

## No-rescue constraints (preserved)

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

## Successor authorisation status

**No successor phase is authorised by this merge.** The
following remain unauthorised:

- Phase 4aw;
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

Phase 4av is being merged into `main` via `--no-ff` to
preserve the Phase 4av branch history as a discrete merge
node. Phase 4av is docs-only. **Recommended state remains
paused unless the operator separately authorizes a future
phase.** No next phase is authorized.

## End of Phase 4av merge closeout
