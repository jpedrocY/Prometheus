# Phase 4bl-F — Phase Risk-Tiering and Controlled Remediation Standard

## 1. Phase identity

- **Phase:** Phase 4bl-F — Phase Risk-Tiering and Controlled
  Remediation Standard
- **Type:** docs-only process refinement / governance calibration
  phase
- **Tier:** Tier 1 (Full Phase) under the new
  `docs/00-meta/process/phase-risk-tiering-standard.md` —
  introducing a new process standard is itself an irreversible
  governance change and must use full ceremony, even though the
  content of the new standard authorizes lighter ceremony for
  future bounded work.
- **Branch:**
  `phase-4bl-f/phase-risk-tiering-controlled-remediation-standard`
- **Base commit (`main` / `origin/main` at branch creation):**
  `b765fd48d9d70ef5ad1a930a869b1a33c82d9f87` — the Phase 4bl-E
  merge-closeout commit (`docs(phase-4bl-e): add merge closeout`)
  on `main`. `git rev-parse main == git rev-parse origin/main`
  at branch creation.
- **Predecessor project-complete phase:** Phase 4bl-E — Multi-Day
  Raw Manifest Successor-State Recording (project-complete on
  `main` per
  `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-e_merge-closeout.md`).
- **Status statement:** This memo is **docs-only**. It does **not**
  modify source code, tests, scripts, `pyproject.toml`,
  `README.md`, `.gitignore`, `.gitattributes`, MCP files, data,
  manifests, sidecars, gate reports, successor-state artefacts,
  local artefacts, or runtime artefacts. It performs **no** sidecar
  rewrite, **no** sidecar normalization, **no** Phase 4bb-F
  canonical path policy amendment, **no** Phase 4bl-D gate
  amendment, **no** gate rerun, **no** manifest mutation, **no**
  successor-state creation, and **no** authorization of any
  successor phase.

## 2. Pre-state verified before any write

Before creating the branch and writing files, the following
state was verified:

```text
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
        .claude/scheduled_tasks.lock
        data/research/

nothing added to commit but untracked files present

$ git rev-parse main
b765fd48d9d70ef5ad1a930a869b1a33c82d9f87

$ git rev-parse origin/main
b765fd48d9d70ef5ad1a930a869b1a33c82d9f87

$ git log --oneline -12 --decorate
b765fd4 (HEAD -> main, origin/main, origin/HEAD) docs(phase-4bl-e): add merge closeout
e0d92f9 feat(phase-4bl-e): merge multi-day raw manifest successor-state recording
e2c527a (phase-4bl-e/...) feat(phase-4bl-e): multi-day raw manifest successor-state recording
4d91616 docs(phase-4bl-d-r): add merge closeout
8c5309b feat(phase-4bl-d-r): merge multi-day raw manifest eligibility gate rerun
4d5a1c1 (phase-4bl-d-r/...) feat(phase-4bl-d-r): multi-day raw manifest eligibility gate rerun
69e4528 docs(phase-4bl-d-s2): add merge closeout
d8c43b5 feat(phase-4bl-d-s2): merge controlled sidecar canonicalization execution
3a8864b (phase-4bl-d-s2/...) feat(phase-4bl-d-s2): controlled sidecar canonicalization execution
0d51bd7 docs(phase-4bl-d-s1): add merge closeout
ffe50d3 docs(phase-4bl-d-s1): merge sidecar canonicalization governance memo
d4e2315 (phase-4bl-d-s1/...) docs(phase-4bl-d-s1): sidecar canonicalization governance memo
```

`main` and `origin/main` are in sync at `b765fd4`. Phase 4bl-E is
project-complete (merge-closeout committed at `b765fd4`). The
Phase 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E chain is
fully recorded on `main`. The branch
`phase-4bl-f/phase-risk-tiering-controlled-remediation-standard`
was created from `b765fd4`.

## 3. Goal of Phase 4bl-F

Author a prospective process standard that calibrates phase
ceremony to phase risk:

- preserve full ceremony for irreversible scientific or
  admissibility decisions;
- introduce controlled lightweight ceremony for bounded metadata
  remediations that satisfy a standing policy;
- introduce batch ceremony for repeated proven operations;
- introduce minimal ceremony for purely administrative
  documentation corrections;
- introduce a standing decision tree for one specific recurring
  remediation pattern (CRLF → LF sidecar canonicalization) so
  that future equivalents can use Tier 2 controlled remediation
  without re-authoring a governance memo;
- define reusable non-authorization blocks that future prompts
  may reference rather than restate in full;
- define short-form report and batch-phase guidance;
- preserve every retained verdict, project lock, and prior phase
  result verbatim.

The driver was the Phase 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R /
Phase 4bl-E chain. That chain demonstrated that the existing
governance worked correctly — the failed gate was recorded
honestly, the cause was interpreted in a separate memo, the fix
was executed in a separate controlled phase, the gate was rerun
in a separate phase, and the result was recorded as a sibling
artefact in yet another phase. Five phases were used to
canonicalize one sidecar's line ending. That outcome was correct
because no standing policy existed yet. It is also a clear
signal that future bounded, well-understood remediations need a
lighter but still auditable path.

## 4. Tracked files added (3)

| File | Purpose |
| --- | --- |
| `docs/00-meta/process/phase-risk-tiering-standard.md` | The new process standard. Defines purpose, authority, core principle, four phase risk tiers (Tier 1 Full Phase, Tier 2 Controlled Remediation, Tier 3 Batch, Tier 4 Administrative / Docs Correction), escalation rules, the standing R-SIDECAR-CRLF remediation decision tree, standing remediation exclusions, nine reusable non-authorization blocks, short-form report guidance, batch-phase guidance, the relationship to prior phases, future application examples, the Phase 4bl-F non-authorizations, and the change-control process for the standard itself. |
| `docs/00-meta/implementation-reports/2026-05-14_phase-4bl-f_phase-risk-tiering-controlled-remediation-standard.md` | This implementation report. |
| `docs/00-meta/implementation-reports/2026-05-14_phase-4bl-f_closeout.md` | Phase 4bl-F closeout. |

## 5. Tracked files modified narrowly (5)

| File | Nature of change |
| --- | --- |
| `docs/00-meta/process/phase-workflow-standard.md` | Two narrow additions: (a) the "Phase lifecycle overview" section now mentions that step ceremony is calibrated by tier per the new standard; (b) the "Required references for future chats" section now lists the new standard. No lifecycle step, role, gate, or governance rule was changed. |
| `docs/00-meta/process/phase-prompt-template.md` | One new bullet at the top of "Prompt design principles" stating that every authorization prompt should declare the phase risk tier per the new standard. No prompt-section structure was changed. |
| `docs/00-meta/process/operator-report-standard.md` | One new "Risk-tier acknowledgement" subsection inserted before "Evidence and citation standard", instructing ChatGPT to identify the phase's tier in recommendations and reviews. No report shape was changed. |
| `docs/00-meta/process/merge-closeout-standard.md` | One new "Short-form merge-closeout (Tier 4 only)" subsection inserted between "When merge-closeout is required" and "Required merge-closeout sections", explicitly restricting the short-form merge-closeout to Tier 4 phases and reaffirming that Tier 1 / Tier 2 / Tier 3 phases must use the full 16-section structure. No required section was changed. |
| `docs/00-meta/current-project-state.md` | Narrow Phase 4bl-F paragraph addition at the top of the current-phase block, plus a new "Current phase:" block describing Phase 4bl-F branch-complete state. The prior Phase 4bl-E "Current phase:" block is preserved as historical context per the project's standing convention. No retained verdict, project lock, or prior narrative was changed. |

## 6. Files NOT modified

The following surfaces were not touched:

- any source file under `src/prometheus/`;
- any test file under `tests/`;
- any script under `scripts/`;
- `pyproject.toml`;
- `README.md`;
- `.gitignore`;
- `.gitattributes`;
- any MCP file;
- any prior governance memo beyond the narrow current-
  project-state.md paragraph addition and the four narrow
  process-doc cross-references;
- any `data/microstructure/` artefact (raw zip, raw manifest,
  raw zip sidecar, acquisition log, derived manifest, normalized
  parquet, feature manifest, feature parquet, label manifest,
  label parquet, gate reports, successor-state artefacts,
  canonicalization reports, every paired `.sha256` sidecar — all
  byte-identical pre/post Phase 4bl-F);
- any prior phase report or merge-closeout under
  `docs/00-meta/implementation-reports/`.

## 7. Content summary of the new standard

The new `docs/00-meta/process/phase-risk-tiering-standard.md`
contains 14 sections plus a final note. The structure is:

1. **Purpose** — explains that Prometheus retains strict phase
   governance, that governance should be proportional to risk,
   that the standard exists to prevent process overhead from
   becoming the product, and that the standard is prospective
   only and does not rewrite prior phase history.
2. **Authority** — the standard is process-only; it does not
   authorize any successor phase, does not modify any technical
   state, and does not enable ML / strategy / backtests /
   acquisition / paper / shadow / live / deployment /
   exchange-write / production keys / authenticated APIs /
   private endpoints / user stream / MCP / Graphify /
   `.mcp.json` / credentials.
3. **Core principle** — full ceremony for irreversible
   scientific or admissibility decisions; controlled lightweight
   ceremony for bounded metadata remediations; batch ceremony
   for repeated proven operations; minimal ceremony for purely
   administrative documentation corrections.
4. **Phase risk tiers** — defines Tier 1 (Full Phase), Tier 2
   (Controlled Remediation), Tier 3 (Batch), and Tier 4
   (Administrative / Docs Correction), with use cases, criteria,
   and required ceremony for each.
5. **Standing remediation decision tree** — establishes
   R-SIDECAR-CRLF as the first standing rule. A future Tier 2
   Controlled Remediation Phase may canonicalize a single
   Phase 4bb-F sidecar from CRLF to canonical LF without a
   separately authorized governance memo if and only if five
   criteria hold (correct embedded SHA, correct basename,
   byte-identical target file, only-line-ending difference,
   otherwise-canonical Phase 4bb-F format). Required evidence is
   enumerated explicitly.
6. **Standing remediation exclusions** — twelve cases where the
   R-SIDECAR-CRLF rule does not apply and the phase escalates
   to Tier 1 or a dedicated governance memo.
7. **Reusable non-authorization blocks** — defines nine
   canonical blocks (N-ACQUISITION, N-ENDPOINT, N-CREDENTIALS,
   N-MANIFEST, N-GATE-RERUN, N-SUCCESSOR-STATE, N-DERIVATION,
   N-DIAGNOSTICS-ML-STRATEGY, N-PHASE-5, N-VERDICT-LOCK) plus
   a use-with-care clause that the blocks are a convenience for
   clarity, not a way to hide scope.
8. **Short-form report guidance** — defines when a short-form
   implementation report is acceptable (Tier 2 with one target,
   or Tier 4) and what it must still include (phase identity,
   target, pre/post evidence, validation, boundaries,
   recommended state, no successor authorization).
9. **Batch-phase guidance** — defines when many operations may
   be handled in one phase, the per-item PASS / FAIL /
   NOT_APPLICABLE / ERROR inventory requirement, the
   "no silent skipping" rule, the "batch success cannot hide
   partial failure" rule, and the rule that batch phases may not
   authorize downstream phases by themselves unless explicitly
   in scope.
10. **Relationship to prior phases** — three binding statements:
    (a) Phase 4bl-D through Phase 4bl-E remain valid; (b) the
    CRLF sidecar chain established the precedent for
    R-SIDECAR-CRLF; (c) prior retained verdicts and project
    locks remain unchanged.
11. **Future application examples** — a table of plausible
    future phases and their tier assignments under the standard.
12. **Non-authorizations for Phase 4bl-F itself** — explicit
    list of activities Phase 4bl-F does not authorize, including
    Phase 4bm-A, multi-day normalization, features, labels,
    diagnostics, ML, strategy, backtests, acquisition,
    exchange-write, paper / shadow, live, MCP, Graphify,
    `.mcp.json`, credentials, additional acquisition, and any
    successor phase.
13. **Change-control process for this standard** — defines that
    the standard may be updated only by a separately authorized
    docs-only Tier 1 process phase that names the file in its
    allowed tracked files, with full ceremony.
14. **Required references for future chats** — lists the other
    process docs and current-project-state.md.

A final note closes the standard with the rationale: the
project's evidentiary discipline is its competitive advantage;
the standard does not relax that discipline; it re-allocates
ceremony so that bounded, well-understood, low-risk work does
not consume the same operator and reviewer attention as
admissibility, manifest, gate, label, ML, strategy, backtest, or
successor-state decisions.

## 8. Validation

This phase is docs-only. The validation gates run were:

```text
$ git status
On branch phase-4bl-f/phase-risk-tiering-controlled-remediation-standard
Untracked files:
        .claude/scheduled_tasks.lock
        data/research/
nothing added to commit but untracked files present
(before staging tracked changes)

$ git diff --check
(clean)
```

`ruff`, `mypy`, and `pytest` were **not** run because no source,
test, script, or configuration file was modified. Per the
operator-report standard, validation results must distinguish
fact from claim; this report does not claim ruff / mypy / pytest
were run.

## 9. Boundary confirmations

- **No data/microstructure/ write.** No file under
  `data/microstructure/` was created, modified, or deleted by
  Phase 4bl-F. Every prior local artefact under
  `data/microstructure/` (raw zips, raw manifest, raw zip
  sidecars, acquisition log, acquisition log sidecar, normalized
  parquet, derived manifest, derived manifest sidecar, feature
  parquet, feature manifest, feature manifest sidecar, label
  parquet, label manifest, label manifest sidecar, Phase 4bb-D
  raw `__v001` gate report, Phase 4bf derived gate report,
  Phase 4bi-B feature-family gate report, Phase 4bj-E label-
  family gate report, Phase 4bg-B / 4bi-D / 4bj-G / 4bb-G / 4bl-E
  successor-state artefacts, Phase 4bl-D-S2 canonicalisation
  report, Phase 4bl-D / 4bl-D-R gate reports, every paired
  `.sha256` sidecar) is byte-identical pre/post Phase 4bl-F.
- **No manifest mutation.** No actual manifest was modified.
  No `research_eligible` flag was flipped. No
  `eligibility_gate_status` was transitioned on any actual
  manifest. No `chronological_split_policy` was changed on any
  actual manifest. The Phase 4aw
  `MicrostructureManifest.flip_research_eligible(...)` always-
  raises invariant is preserved (never invoked).
- **No gate rerun.** No raw / derived / feature / label /
  metrics gate was rerun. No gate report was generated.
- **No successor-state.** No successor-state artefact was
  created. No prior successor-state artefact was modified.
- **No acquisition.** No data was acquired, downloaded, or
  fetched. No Binance / public / private endpoint was
  contacted. No WebSocket was opened. No credential was used.
  No `.env` or `.mcp.json` was read or created. MCP and
  Graphify were not enabled.
- **No normalization, derivation, features, labels.** No
  normalization, derivation, feature computation, or label
  computation was performed. No diagnostics, ML, strategy,
  signals, or backtests were produced. No PnL, MFE, MAE,
  R-multiple, equity, position, alpha, edge, prediction,
  model-score, decision-score, entry-exit, or strategy output
  was computed.
- **No retained verdict or project lock change.** All retained
  verdicts (H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD;
  R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m
  thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT —
  terminal for V2 first-spec; G1 HARD REJECT — terminal for G1
  first-spec; C1 HARD REJECT — terminal for C1 first-spec) are
  preserved verbatim. All project locks (§11.6 = 8 bps per
  side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position
  / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
  Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p;
  Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause
  gate + post-null cooldown + cooled-down families list + memo
  template; Phase 4al refined no-rescue rule + §13 boundary +
  §14 hierarchy; Phase 4aw `flip_research_eligible(...)`
  always-raises invariant; Phase 4bb-F canonical path policy;
  Phase 4bb-G raw `__v001` successor-state precedent; Phase
  4bg-B / Phase 4bi-D / Phase 4bj-G / Phase 4bl-E successor-
  state precedents) are preserved verbatim.
- **No successor authorization.** Phase 4bl-F does not
  authorize Phase 4bl-F merge phase, Phase 4bm-A, Phase 4bm-*,
  Phase 4bn-*, Phase 4bo-*, Phase 4bp-*, Phase 4bq-*, Phase 5,
  Phase 4 canonical, paper / shadow, live-readiness,
  deployment, exchange-write, production-key creation,
  authenticated APIs, private endpoints, user stream, live
  WebSocket implementation, MCP, Graphify, `.mcp.json`,
  credentials, or any additional acquisition.

## 10. Retained verdict ledger preserved verbatim

| Verdict | State |
| --- | --- |
| H0 | FRAMEWORK ANCHOR |
| R3 | BASELINE-OF-RECORD |
| R1a | RETAINED — NON-LEADING |
| R1b-narrow | RETAINED — NON-LEADING |
| R2 | FAILED — §11.6 |
| F1 | HARD REJECT |
| D1-A | MECHANISM PASS / FRAMEWORK FAIL |
| 5m thread | OPERATIONALLY CLOSED per Phase 3t |
| V2 | HARD REJECT — terminal for V2 first-spec |
| G1 | HARD REJECT — terminal for G1 first-spec |
| C1 | HARD REJECT — terminal for C1 first-spec |

## 11. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7 (strict integrity gate)
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14
  hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant (never invoked by Phase 4bl-F)
- Phase 4bb-F canonical path policy (Phase 4bl-F follows it
  verbatim — the new standard's R-SIDECAR-CRLF rule preserves
  Phase 4bb-F format and only canonicalizes line endings; the
  new standard does not amend Phase 4bb-F)

## 12. No-rescue and Phase 4al boundary

This standard preserves the Phase 4al refined no-rescue rule,
§13 boundary, and §14 hierarchy verbatim. The standard does not
introduce any new admissibility path, does not relax any
mechanism check, does not amend any opportunity-rate or
edge-rate viability requirement, and does not introduce any
new admissibility gate. The standard exclusively addresses
process ceremony for already-admissible work.

## 13. Recommended state

**Remain paused.**

The operator has signalled an intent to pause for a broader
project discussion (complexity, phase usefulness, possible
energy-market sibling project) before any technical successor
is authorized. Phase 4bm-A (Multi-Day Normalization Design
Memo) remains a conditional natural successor by precedent of
Phase 4bc for the Phase 4az `__v001` raw family, but is **not
authorized** by Phase 4bl-F. No other phase is authorized.

## 14. Lifecycle status

Phase 4bl-F is **branch-complete only** by this work. Per the
Phase 4bk-A workflow standard:

> A phase is not project-complete until it is merged into main
> and its merge-closeout is recorded.

Phase 4bl-F is not project-complete until a separately
authorized merge phase records its merge-closeout on `main`.
The Phase 4bl-F merge phase, if separately authorized, would be
a Tier 1 phase under the new standard (introducing a new process
standard is itself an irreversible governance change).

## 15. Conditional next, not authorized

- Future operator-authorized merge phase that merges this
  Phase 4bl-F branch into `main` and records a Phase 4bl-F
  merge-closeout per `merge-closeout-standard.md`. Tier 1.
- Followed by a future operator-driven discussion about
  project complexity, phase usefulness, and possible energy-
  market sibling project.
- Followed by a separately authorized future Phase 4bm-A —
  Multi-Day Normalization Design Memo (docs-only) only if the
  operator chooses to continue the multi-day data arc. Tier 1
  (new design; new semantics).

None of the above is authorized by Phase 4bl-F.

## 16. Final notes

Phase 4bl-F is the second pure process / standardization
phase in the project's history (after Phase 4bk-A, which
introduced the original phase-workflow / phase-prompt /
operator-report / merge-closeout / chat-branching-handoff
standards). Phase 4bl-F does not amend the Phase 4bk-A
standards in their substance; it adds a fifth process standard
and records four narrow cross-references in the existing four.

Phase 4 canonical remains unauthorized. Phase 4bl-F merge
phase / Phase 4bm-A / Phase 4bm-* / Phase 4bn-* / Phase 4bo-* /
Phase 4bp-* / Phase 4bq-* / Phase 5 / any successor phase
remains unauthorized. Paper / shadow, live-readiness,
deployment, production keys, authenticated APIs, private
endpoints, public-endpoint calls in code, user stream,
WebSocket implementation, MCP, Graphify, `.mcp.json`,
credentials, exchange-write, and any additional acquisition
beyond the 90 locked BTCUSDT UTC dates remain unauthorized.

M0 mechanism-admissibility gate and post-null cooldown rule
remain binding prospective governance for any future research
lane.

Recommended state: **remain paused.**

No next phase authorized.
