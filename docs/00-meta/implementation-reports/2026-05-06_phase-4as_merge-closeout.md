# Phase 4as Merge Closeout — Crypto Microstructure Research Reset and Mechanism Map

## Merge identity

- **Phase:** 4as.
- **Phase title:** Crypto Microstructure Research Reset and Mechanism Map.
- **Phase type:** docs-only research-program reset / mechanism-map memo.
- **Target branch:** `main`.
- **Source branch:** `phase-4as/crypto-microstructure-research-reset-mechanism-map`.
- **Merge method:** `--no-ff` (preserves the Phase 4as branch
  history as a discrete merge node on `main`).
- **Main before merge SHA:** `12f2b5558b0812a11526da331fa70feb45fcae9d`.
- **Phase 4as memo commit SHA:** `67fa2a55d73d41b89b5695605eabf38dd1906fdd`
  (`docs(phase-4as): map crypto microstructure research reset`).
- **Phase 4as closeout commit SHA:** `2002cab84eac08c98f1106fb2e2356a63a341f50`
  (`docs(phase-4as): add closeout`).
- **Merge commit SHA:** recorded in this merge closeout's final
  operator report (and in the live `git log` on `main`) once the
  merge commit lands. Self-referential SHA-in-content is avoided
  per prior-phase convention.

## Merge purpose

This merge brings the Phase 4as docs-only research-program reset
and mechanism map onto `main`. Phase 4as resets the Prometheus
research program toward Binance-native crypto microstructure and
derivatives-flow mechanisms after Phase 4ar closed the V1 /
exit-rescue arc as descriptive evidence only and after the
cumulative six-candidate rejection topology (R2 / F1 / D1-A / V2 /
G1 / C1) has not produced deployable edge under §11.6 cost realism.

The merge is **docs-only**. It brings forward two new memos and a
narrow update to `docs/00-meta/current-project-state.md`. It does
**not** authorise any successor phase, data acquisition, endpoint
call, capture code, feature implementation, ML model, strategy
candidate, paper / shadow, live-readiness, deployment,
exchange-write, production-key creation, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, or any 5m / 1m / aggTrades / tick /
mark-price 30m / 4h / order-book data acquisition.

## Files brought forward

- `docs/00-meta/implementation-reports/2026-05-06_phase-4as_crypto-microstructure-research-reset-mechanism-map.md`
  — Phase 4as main memo (21 sections; +1,671 lines).
- `docs/00-meta/implementation-reports/2026-05-06_phase-4as_closeout.md`
  — Phase 4as closeout (+526 lines).
- `docs/00-meta/current-project-state.md`
  — narrow update: Phase 4as narrative paragraph + Phase 4as
  "Current phase:" block + transition lines preserving the
  prior Phase 4ar block as historical context (matching
  prior-phase convention).

This merge closeout adds:

- `docs/00-meta/implementation-reports/2026-05-06_phase-4as_merge-closeout.md`
  — this file.

No other file is changed by this merge.

## Confirmation Phase 4as was docs-only

Phase 4as is a docs-only research-program reset memo. The merge
brings forward only:

- two new markdown memos under `docs/00-meta/implementation-reports/`,
- a narrow update to `docs/00-meta/current-project-state.md`,
- this merge closeout.

No script was added or executed. No backtest was run. No data was
acquired. No Binance endpoint was called. No code under
`src/prometheus/` was modified. No test was modified. No existing
script was modified. No `.gitignore` change was made. No
`data/research/` content was committed.

`ruff check`, `pytest`, and `mypy` were **not** run because the
phase is docs-only (no `src/prometheus/`, test, script, or
`scripts/` change of any kind). This matches the docs-only
convention used by Phase 4d, 4e, 4f, 4g, 4h, 4j, 4k, 4m, 4n, 4o,
4p, 4q, 4s, 4t, 4u, 4v, 4w, 4y, 4z, 4aa, 4ab, 4ad, 4ag, 4ah, 4aj,
4ak, 4al, 4am (audit-only), 4an, 4ao, 4ap, and 4ar.

## Phase 4as mechanism-map result

Phase 4as resets the Prometheus research program toward
Binance-native crypto microstructure and derivatives-flow
mechanisms. The reset is a **change of information set**, not a
guarantee of edge. The cooled-down families list, the six-candidate
rejection topology, M0 admissibility, the post-null cooldown rule,
the Phase 4al refined no-rescue rule, the Phase 4t 10-dimension
scoring matrix, the Phase 4m 18-requirement validity gate, the
Phase 3t 5m closure, §11.6, and §1.7.3 remain binding.

### Mechanism map (M-1 through M-14, conceptual; not strategies)

- **M-1** spread / spread-widening.
- **M-2** top-of-book depth.
- **M-3** order-book imbalance (top-N).
- **M-4** depth imbalance across deeper levels.
- **M-5** aggressive volume / taker buy-sell imbalance.
- **M-6** trade burst / volume impulse.
- **M-7** liquidity sweep / book consumption.
- **M-8** book recovery / replenishment after sweep.
- **M-9** liquidation cascade proxies (bounded visibility).
- **M-10** funding-rate context (context only, not directional
  trigger; D1-A precedent — funding is not a directional trigger).
- **M-11** open-interest context (under Phase 4j §11 OI subset
  governance).
- **M-12** funding + OI interaction.
- **M-13** funding + OI + aggressive-flow interaction.
- **M-14** spread / depth / flow regime interaction.

Each mechanism entry in the Phase 4as memo records plain-English
hypothesis, why-might-contain-edge, why-might-fail, required
data, granularity, historical-vs-live feasibility, likely Binance
data source (per official Binance docs; no calls made),
leakage risks, cost / slippage sensitivity, validation challenges,
M0 admissibility concerns, and suitability for future feasibility
study. **No mechanism is authorized for implementation, data
capture, or strategy work.**

### Candidate lane ranking (governance-safe, not strategy ranking)

```text
A → B → C → D → E
```

- **Lane A** — Binance microstructure data availability / capture
  feasibility (cleanest next move; docs-only).
- **Lane B** — aggressive-volume / order-flow imbalance feasibility
  (M-5 / M-6).
- **Lane C** — order-book imbalance / depth feasibility (M-3 /
  M-4).
- **Lane D** — liquidation proxy + flow / OI interaction (M-9 /
  M-12 / M-13).
- **Lane E** — ML / meta-labeling admissibility (later only;
  admissible only after a base mechanism is independently
  validated).

Each lane is gated by separate operator authorisation, M0
admissibility, the Phase 4ak post-null cooldown rule, the
Phase 4al refined no-rescue rule, the Phase 4m 18-requirement
validity gate, the Phase 4t 10-dimension scoring matrix, and
§11.6 cost realism.

### Phase 4at status

Phase 4as **recommends** Phase 4at — Binance Microstructure Data
Availability / Capture Feasibility Memo (docs-only) as the
cleanest separately-authorised next move *if the operator chooses
to continue research after reviewing Phase 4as*.

**Phase 4at is NOT authorized by this merge.**

Phase 4at, if ever authorised, would translate §9 of the Phase 4as
memo into a precise Binance data availability map, identify
historical-vs-live boundaries, and predeclare a capture design
under M0-style admissibility — without acquiring any data,
calling any endpoint, or implementing any capture.

## Confirmation no data acquisition occurred

This merge does not acquire any data. No file under `data/raw/`,
`data/normalized/`, `data/derived/`, or `data/manifests/` is
created or modified. No `data.binance.vision` archive is
downloaded. No Binance REST endpoint is called. No Binance WS
stream is opened.

## Confirmation no Binance endpoint call occurred

This merge does not call any Binance endpoint. No `requests`,
`httpx`, `aiohttp`, `websockets`, `urllib`, or equivalent network
client is invoked. No authenticated API call is made. No private
endpoint, public endpoint in code, user stream, WebSocket,
listenKey, MCP, Graphify, `.mcp.json`, or credentials are
touched.

## Confirmation no out-of-scope changes occurred

Beyond the narrow `docs/00-meta/current-project-state.md` update
and the new memo / closeout / merge-closeout files under
`docs/00-meta/implementation-reports/`, this merge does **not**
modify:

- endpoint code,
- capture code,
- feature implementation,
- `src/prometheus/` source code,
- any test under `tests/`,
- any existing script under `scripts/` (including
  `scripts/phase4aq_v1_arc_exit_path_forensics.py` and every
  prior research script),
- any data file under `data/raw/`, `data/normalized/`,
  `data/derived/`, or `data/manifests/`,
- any `research_eligible` flag (no flip),
- any v003 dataset (none created),
- `.gitignore`,
- any specialist governance file (no Phase 3r §8 / Phase 3v §8 /
  Phase 3w §6 / §7 / §8 / Phase 4j §11 / Phase 4k / Phase 4p /
  Phase 4q / Phase 4v / Phase 4w / Phase 4ak / Phase 4al / 4am /
  4an / 4ao / 4ap / 4aq / 4ar governance modification),
- any retained verdict (no verdict revision),
- any project lock (no §11.6 / §1.7.3 / Phase 3r §8 / Phase 3v §8
  / Phase 3w §6 / §7 / §8 / Phase 4j §11 modification).

## Confirmation no local data/research/ outputs were committed

`data/research/` remains git-ignored at `.gitignore:88`. No
content under `data/research/` is committed by Phase 4as or by
this merge. Local Phase 4aq output bundle under
`data/research/phase4aq/` (from the merged Phase 4aq research
phase) remains uncommitted and unchanged.

## Implementation / governance review

### What changed

- New file: `docs/00-meta/implementation-reports/2026-05-06_phase-4as_crypto-microstructure-research-reset-mechanism-map.md`
  (Phase 4as main memo, 21 sections).
- New file: `docs/00-meta/implementation-reports/2026-05-06_phase-4as_closeout.md`
  (Phase 4as closeout).
- Narrow update: `docs/00-meta/current-project-state.md` (Phase
  4as narrative paragraph + Phase 4as "Current phase:" block;
  prior Phase 4ar block preserved as historical context).
- New file (this merge): `docs/00-meta/implementation-reports/2026-05-06_phase-4as_merge-closeout.md`.

### What did not change

- No `src/prometheus/` modification.
- No test modification.
- No existing-script modification.
- No data / manifest / `research_eligible` / v003 change.
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
- No capture implementation.
- No feature implementation.

### Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are preserved
verbatim. M0 governance is unchanged. The 5m closure (Phase 3t)
is preserved. The cost lock (§11.6) and project locks (§1.7.3)
are preserved. The stop-trigger-domain governance (Phase 3v §8),
break-even / EMA slope / stagnation governance (Phase 3w §6 /
§7 / §8), mark-price gap governance (Phase 3r §8), and OI subset
governance (Phase 4j §11) are all preserved. The Phase 4ak M0
gate, post-null cooldown rule, cooled-down families list, and
memo template are all preserved. The Phase 4al refined no-rescue
rule + §13 / §14 hierarchy is preserved. The Phase 4am §11.A
audit findings, Phase 4an inventory, Phase 4ao harmonization,
Phase 4ap forensic plan, Phase 4aq computation, and Phase 4ar
interpretation are all preserved.

### Is the merge docs-only?

Yes. The merge brings forward two new memos under
`docs/00-meta/implementation-reports/` plus a narrow update to
`docs/00-meta/current-project-state.md`, plus this merge
closeout. No code, test, script, data, manifest, governance, or
lock change occurs.

## Research interpretation review (plain English)

### What did this phase prove?

Phase 4as did not prove anything in the predictive-statistics
sense. As a docs-only reset memo it consolidates the existing
project record (Phase 4ar interpretation; Phase 4aq descriptive
forensic snapshot; six-candidate rejection topology; M0
governance; cost / position / leverage locks; 5m closure) and
documents that the project's research program should now widen
its information set toward Binance-native microstructure and
derivatives-flow mechanisms, while preserving every prior
verdict and lock and without authorising any data acquisition,
capture, model, or strategy.

### What did this phase not prove?

Phase 4as did not prove that any specific microstructure mechanism
contains edge. It did not run any computation. It did not acquire
any data. It did not call any Binance endpoint. It did not
authorise any successor phase. It did not authorise any data
capture or endpoint call. It did not produce a new strategy
candidate. It did not amend M0. It did not modify any verdict or
lock.

### Which original questions did it answer?

The Phase 4as question — "What new mechanism classes are
plausibly worth studying after the V1 / exits arc closed, and how
should Prometheus evaluate them before any data acquisition,
feature implementation, or strategy design is authorized?" — is
answered across §5–§17 of the Phase 4as memo (justification of the
reset, why crypto / Binance, why move beyond lagging OHLCV, the
M-1..M-14 mechanism map, the Binance data availability map, data
complexity / feasibility, research validity / anti-overfitting,
ML / AI placement, symbol discussion, window / regime discussion,
candidate lane ranking, recommended next phase Phase 4at,
explicit non-recommendations).

### Which original questions remain open?

- Whether any of the M-1 → M-14 mechanisms contains edge under
  the project's locked cost realism. **This is not answered by
  Phase 4as.**
- Whether Phase 4at would be the cleanest next move. The memo
  recommends Phase 4at but does not authorise it.
- Whether any future microstructure research will eventually
  satisfy M0 admissibility, the Phase 4m validity gate, the
  Phase 4t scoring matrix, the Phase 4ak post-null cooldown
  rule, and the Phase 4al refined no-rescue rule. This is
  operator-driven.

### What does it mean for strategy research?

The reset re-orients the *next* admissibility question from "can
we improve previous geometry?" to "are there mechanisms the
previous geometry never measured?" without authorising any new
mechanism, model, or strategy. The cooled-down families list is
preserved. The six-candidate rejection topology is preserved.
The cost lock, position lock, leverage lock, and mark-price stop
lock are preserved. M0 remains the binding admissibility
framework.

### What does it mean for governance?

This merge reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k,
Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption,
Phase 4al refined no-rescue + §13 / §14, Phase 4am §11.A audit
findings, Phase 4an inventory, Phase 4ao harmonization,
Phase 4ap forensic plan, Phase 4aq computation result preserved
as descriptive evidence only, and Phase 4ar interpretation result
preserved as descriptive interpretation only. **None is amended.**

### What is the clean next step?

Operator review of Phase 4as on `main` after this merge lands.
**No successor phase is authorised by this merge.** The clean
next step is operator-driven only. Acceptable separately-
authorised future options include remain paused (recommended),
Phase 4at as a docs-only Binance microstructure data
availability / capture feasibility memo, or further docs-only
governance memos on precise governance questions. None is
started or authorised by this merge.

### What should we not do yet?

- No data acquisition.
- No Binance endpoint calls.
- No data-capture implementation.
- No feature implementation.
- No ML model.
- No new strategy candidate.
- No exit / entry design.
- No verdict / lock revision.
- No M0 amendment.
- No reopening of the 5m research thread.
- No 5m / 1m / aggTrades / tick / mark-price / order-book
  acquisition.
- No paper / shadow / live-readiness / deployment /
  exchange-write / production-key creation / authenticated APIs
  / private endpoints / user stream / WebSocket / MCP /
  Graphify / `.mcp.json` / credentials.

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
- **Phase 4j §11** — metrics OI-subset partial-eligibility rule.
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
- **Phase 4an** — historical-trade-population exit-path inventory.
- **Phase 4ao** — exit-path methodology / artefact harmonization.
- **Phase 4ap** — V1-Arc Exit-Path Forensic Plan.
- **Phase 4aq** — computation result preserved as descriptive
  evidence only.
- **Phase 4ar** — interpretation result preserved as descriptive
  interpretation only.
- **Phase 4as** — mechanism-map result preserved as docs-only
  reset evidence only.

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

- Phase 4at;
- Phase 5;
- Phase 4 canonical;
- data acquisition;
- Binance endpoint calls;
- endpoint implementation;
- data-capture implementation;
- feature implementation;
- ML model;
- strategy candidate;
- entry / exit design;
- old-strategy alt-symbol reruns;
- R3 / R2 / V1-arc rescue;
- 5m research thread reopening;
- 5m / 1m / aggTrades / tick / mark-price 30m / 4h / order-book
  data acquisition;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production keys;
- authenticated APIs;
- private endpoints;
- user stream;
- WebSocket;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials.

## Final status

Phase 4as is being merged into `main` via `--no-ff` to preserve
the Phase 4as branch history as a discrete merge node. Phase 4as
is docs-only. **Recommended state remains paused unless the
operator separately authorizes a future phase.** No next phase
is authorized.

## End of Phase 4as merge closeout
