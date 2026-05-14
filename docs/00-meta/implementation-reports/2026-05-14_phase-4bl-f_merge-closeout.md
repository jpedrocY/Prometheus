# Phase 4bl-F — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-F — Phase Risk-Tiering and Controlled
  Remediation Standard
- **Type:** docs-only process refinement / governance calibration
  phase (Tier 1 — Full Phase under the new
  `docs/00-meta/process/phase-risk-tiering-standard.md`, because
  Phase 4bl-F authors a new prospective process standard).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bl-F branch onto `main` and
  record the project-complete merge-closeout. Phase 4bl-F authored
  the new prospective `phase-risk-tiering-standard.md`, narrowly
  cross-referenced it from the four existing process standards,
  added the Phase 4bl-F implementation report and closeout, and
  updated `current-project-state.md`. Without this merge plus this
  merge-closeout, Phase 4bl-F is branch-complete only and is not
  project-complete.
- **Target branch:** `main`.
- **Source branch:** `phase-4bl-f/phase-risk-tiering-controlled-remediation-standard`.

## 2. SHAs

- **`main` SHA before merge:** `b765fd48d9d70ef5ad1a930a869b1a33c82d9f87`
  (Phase 4bl-E merge-closeout commit on `main`).
- **Branch commit SHAs:**
  - `aaee4ab` — `docs(phase-4bl-f): phase risk-tiering and
    controlled remediation standard` (the single Phase 4bl-F
    branch commit; contained the new standard, four narrow
    process-doc cross-references, the Phase 4bl-F implementation
    report, the Phase 4bl-F closeout, and the
    `current-project-state.md` Phase 4bl-F paragraph + new
    "Current phase:" block).
- **Merge commit SHA:** `27973095b4d7477c1ebfd5ce43ab372c18d1e687`
  (`docs(phase-4bl-f): merge phase risk-tiering and controlled
  remediation standard`).
- **Merge-closeout commit SHA:** to be filled at commit time of
  this merge-closeout file.
- **Final `main` / `origin/main` SHA after push:** to be filled at
  push time of the merge-closeout commit.

## 3. Merge method

- `git merge --no-ff phase-4bl-f/phase-risk-tiering-controlled-remediation-standard`
- Strategy: `ort` (the default).
- Merge commit message: `docs(phase-4bl-f): merge phase
  risk-tiering and controlled remediation standard`.
- Pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing.

## 4. Files brought forward by the merge

Docs added (3):

- `docs/00-meta/process/phase-risk-tiering-standard.md` — the new
  prospective process standard.
- `docs/00-meta/implementation-reports/2026-05-14_phase-4bl-f_phase-risk-tiering-controlled-remediation-standard.md`
  — Phase 4bl-F implementation report.
- `docs/00-meta/implementation-reports/2026-05-14_phase-4bl-f_closeout.md`
  — Phase 4bl-F closeout.

Docs modified narrowly (5):

- `docs/00-meta/process/phase-workflow-standard.md` — lifecycle
  overview note about tiered ceremony; added the new standard to
  "Required references for future chats".
- `docs/00-meta/process/phase-prompt-template.md` — one new
  "Prompt design principles" bullet requiring tier declaration in
  every authorization prompt.
- `docs/00-meta/process/operator-report-standard.md` — one new
  "Risk-tier acknowledgement" subsection inserted before the
  "Evidence and citation standard" subsection.
- `docs/00-meta/process/merge-closeout-standard.md` — one new
  "Short-form merge-closeout (Tier 4 only)" subsection inserted
  between "When merge-closeout is required" and "Required
  merge-closeout sections".
- `docs/00-meta/current-project-state.md` — Phase 4bl-F narrative
  paragraph + new "Current phase:" block; prior Phase 4bl-E
  "Current phase:" block preserved as historical context.

Source: not modified.
Tests: not modified.
Scripts: not modified.
Configs (`pyproject.toml`, `README.md`, `.gitignore`,
`.gitattributes`, MCP files): not modified.
`data/microstructure/`: not modified — every existing artefact
(raw zips, raw manifests, sidecars, acquisition logs, normalized
parquets, derived manifests, feature parquet, feature manifest,
label parquet, label manifest, every gate report, every
successor-state artefact, every canonicalization report) is
byte-identical pre/post.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 319 ++++++++
 .../2026-05-14_phase-4bl-f_closeout.md             | 251 +++++++
 ...risk-tiering-controlled-remediation-standard.md | 451 +++++++++++
 docs/00-meta/process/merge-closeout-standard.md    |  13 +
 docs/00-meta/process/operator-report-standard.md   |  12 +
 docs/00-meta/process/phase-prompt-template.md      |  10 +
 .../00-meta/process/phase-risk-tiering-standard.md | 823 +++++++++++++++++++++
 docs/00-meta/process/phase-workflow-standard.md    |  16 +-
 8 files changed, 1894 insertions(+), 1 deletion(-)
```

The diff matches the expected change set from the Phase 4bl-F
authorization prompt verbatim: 3 new docs, 5 narrowly modified
docs, no source / test / script / config / data files modified.

## 6. Verdict

**PROCESS STANDARDIZATION COMPLETE.**

Phase 4bl-F is now project-complete, having been merged into `main`
and closed out by this merge-closeout. The merge added the new
prospective process standard
`docs/00-meta/process/phase-risk-tiering-standard.md`, narrowly
cross-referenced it from the four existing process standards, and
recorded the Phase 4bl-F implementation report and closeout. The
new standard calibrates Prometheus phase ceremony to phase risk
across four tiers (Tier 1 Full Phase, Tier 2 Controlled
Remediation, Tier 3 Batch, Tier 4 Administrative), establishes the
project's first standing remediation rule R-SIDECAR-CRLF (which
permits a future Tier 2 controlled phase to canonicalize a single
Phase 4bb-F sidecar from CRLF to canonical LF without a separately
authorized governance memo, subject to five precise criteria and
twelve exclusions that escalate to Tier 1), defines nine reusable
non-authorization blocks, and adds short-form report and
batch-phase guidance. R-SIDECAR-CRLF does not pre-authorize
execution; it pre-selects the policy path for any future
separately authorized controlled remediation phase. Phase 4bl-D
through Phase 4bl-E history is preserved verbatim. No retained
verdict was revised. No project lock was changed. No `data/microstructure/`
artefact was created or modified. No `research_eligible` flag was
flipped on any actual manifest. No `eligibility_gate_status` was
transitioned on any actual manifest. No `chronological_split_policy`
was changed on any actual manifest. No gate was rerun. No new gate
report was created. No successor-state artefact was created. No
data was acquired. No successor phase is authorized.
**Recommended state: remain paused.**

## 7. Local gitignored outputs (if any)

**None.** Phase 4bl-F was a docs-only phase. No local artefacts
were produced under `data/microstructure/` or anywhere else outside
the tracked docs.

## 8. Validation results

- `git diff --check` — clean (no whitespace errors).
- `git status` — clean (only pre-existing untracked entries
  `.claude/scheduled_tasks.lock` and `data/research/`).
- `git log --oneline -3 --decorate` — confirms the merge commit at
  HEAD on top of the Phase 4bl-F branch commit on top of the
  Phase 4bl-E merge-closeout commit.
- `ruff` / `mypy` / `pytest` — **not run**. Per the
  `operator-report-standard.md` and the Phase 4bl-F brief, no
  source / test / script / configuration file was modified by
  Phase 4bl-F or by this merge, so no whole-repo code-quality gate
  was rerun. The latest authoritative whole-repo validation
  remains the Phase 4bb-F-implementation merge baseline (`ruff`
  PASS, `mypy` strict 120 source files PASS, microstructure
  `pytest` 915 passed + 1 pre-existing labelled skip, whole-repo
  `pytest` 1698 passed + 1 skipped + 2 pre-existing simulation
  failures).

## 9. Upstream immutability evidence (if applicable)

**n/a** — Phase 4bl-F was a docs-only process-standardization
phase. It did not access, read, write, or modify any artefact
under `data/microstructure/`. Every prior local artefact (raw
zips, raw manifests, sidecars, acquisition logs, normalized
parquets, derived manifest, feature parquet, feature manifest,
label parquet, label manifest, every gate report, every
successor-state artefact, every canonicalization report) is
byte-identical pre/post by virtue of not having been touched.

## 10. Manifest state preservation (if applicable)

**n/a — phase did not touch any manifest.** No manifest field was
read for write purposes, no manifest was modified, no manifest
was created, no manifest was deleted. Every actual on-disk
manifest retains the state recorded by its last authoring phase:

- raw `__v001` manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"` (Phase 4az / 4bb-G).
- raw `__v002` multi-day manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"` (Phase 4bl-C / 4bl-E
  successor-state JSON sibling).
- derived manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"` (Phase 4bd / 4bg-B
  successor-state JSON sibling).
- feature manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"` (Phase 4bh / 4bi-D
  successor-state JSON sibling).
- label manifest: `research_eligible = false`,
  `eligibility_gate_status = "pending"`,
  `chronological_split_policy = "not_yet_defined"` (Phase 4bj-C /
  4bj-G successor-state JSON sibling / 4bj-J no-split
  determination JSON sibling).

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked by Phase 4bl-F or
by this merge).

## 11. Boundary confirmations

- no source code modified
- no test modified
- no script modified
- no `.gitignore`, `.gitattributes`, `pyproject.toml`, or
  `README.md` modified
- no MCP file modified
- no `data/microstructure/` write of any kind
- no `data/microstructure/` artefact committed
- no manifest mutation
- no `research_eligible` flipped on any actual manifest
- no `eligibility_gate_status` transitioned on any actual manifest
- no `chronological_split_policy` changed on any actual manifest
- no gate rerun (raw / derived / feature / label)
- no new gate report created
- no successor-state artefact created
- no canonicalization report created
- no normalization, derivation, features, labels, diagnostics,
  ML, strategy, signals, or backtests run
- no PnL / MFE / MAE / R-multiple / equity / position / alpha /
  edge / prediction / model-score / decision-score / entry-exit /
  strategy output computed
- no data acquired
- no Binance / public / private endpoint contacted
- no WebSocket opened
- no credential used
- no `.env` read or created
- no `.mcp.json` read or created
- MCP and Graphify not enabled
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no Phase 4al refined no-rescue rule, §13 boundary, or §14
  hierarchy amendment
- no Phase 4aw `flip_research_eligible(...)` always-raises
  invariant amended (preserved; never invoked)
- no Phase 4bb-F canonical path policy amended (the new
  R-SIDECAR-CRLF rule preserves Phase 4bb-F format byte-for-byte
  except for the line ending; no policy text changed)
- no prior governance memo modified beyond the four narrow
  process-doc cross-references and the narrow
  `current-project-state.md` paragraph addition
- no prior phase result rewritten
- Phase 4bl-D through Phase 4bl-E history preserved verbatim
- no successor authorized

## 12. Retained verdict ledger

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7 (strict integrity gate)
- Phase 3r §8 (mark-price gap governance)
- Phase 3v §8 (stop-trigger-domain governance)
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation
  governance)
- Phase 4j §11 (metrics OI-subset partial-eligibility rule)
- Phase 4k (V2 backtest-plan methodology)
- Phase 4p (G1 strategy-spec)
- Phase 4q (G1 backtest-plan methodology)
- Phase 4v (C1 strategy-spec)
- Phase 4w (C1 backtest-plan methodology)
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant
- Phase 4bb-F canonical path policy

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bl-F merge does not, and cannot, be construed as
authorising:

- ML model training, model selection, strategy hypothesis
  generation, or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- normalization, derivation, feature computation, label
  computation, or diagnostics;
- paper / shadow / live-readiness / deployment / exchange-write
  work;
- production-key creation, authenticated APIs, private endpoints,
  public-endpoint calls in code, user stream, or live WebSocket
  implementation;
- MCP, Graphify, `.mcp.json`, or credentials work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL
  labels;
- mark-price / spot / cross-venue / order-book / additional
  aggTrades acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible` or
  `eligibility_gate_status` from this evidence alone;
- changing any manifest's `chronological_split_policy` from this
  evidence alone;
- rescuing R2, F1, D1-A, V2, G1, C1, or any cooled-down family;
- amending the Phase 4bb-F canonical path policy (the new
  R-SIDECAR-CRLF rule preserves Phase 4bb-F format byte-for-byte
  except for the line ending);
- amending Phase 4ak M0, the post-null cooldown rule, the
  cooled-down families list, or the memo template;
- amending Phase 4al refined no-rescue rule, §13 boundary, or §14
  hierarchy;
- amending Phase 4aw `flip_research_eligible(...)` always-raises
  invariant;
- pre-authorising execution under R-SIDECAR-CRLF (R-SIDECAR-CRLF
  pre-selects the policy path; it does not pre-authorise
  execution).

## 15. Successor authorization

**None.**

The following candidate successors are explicitly **not**
authorized by this merge:

- Phase 4bm-A — Multi-Day Normalization Design Memo (the natural
  conditional successor by precedent of Phase 4bc for the
  Phase 4az `__v001` raw family)
- Phase 4bm-* (any further multi-day normalization arc)
- Phase 4bn-* (any multi-day feature arc)
- Phase 4bo-* (any multi-day label arc)
- Phase 4bp-* (any multi-day diagnostic arc)
- Phase 4bq-* (any multi-day chronological-split arc)
- Phase 5
- Phase 4 canonical
- normalization
- derivation
- feature computation
- label computation
- label diagnostics
- ML training / model selection / meta-labeling
- strategy implementation / strategy spec / strategy hypothesis
- signal construction
- backtest design / backtest execution
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production-key creation
- authenticated APIs
- private endpoints
- public-endpoint calls in code
- user stream
- live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h /
  order-book / spot / cross-venue / funding / open-interest data
  acquisition
- any execution under R-SIDECAR-CRLF (R-SIDECAR-CRLF requires a
  separately authorized Tier 2 controlled remediation phase)

## 16. Recommended state

**Remain paused.**

The operator has signalled an intent to pause for a broader
project discussion (project complexity, phase usefulness, possible
energy-market sibling project) before any technical successor is
authorized.

**Conditional next, NOT authorized:**

Phase 4bm-A — Multi-Day Normalization Design Memo (docs-only) is
the cleanest non-paused option. It would translate the Phase 4bc
design pattern (originally written for the Phase 4az `__v001` raw
aggTrades family) onto the Phase 4bl-C `__v002` multi-day raw
aggTrades family — proposing a future normalized derived family
sibling to `microstructure_normalized_aggtrades_v001` (e.g.
`microstructure_normalized_aggtrades_v002`) without implementing,
without acquiring further data, and without authorizing any
downstream feature / label / diagnostic / ML / strategy work.
Phase 4bm-A is **not** authorised by this merge.
