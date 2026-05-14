# Phase Risk-Tiering and Controlled Remediation Standard

## Title

Prometheus Phase Risk-Tiering and Controlled Remediation Standard —
prospective process standard that calibrates phase ceremony to phase
risk.

## Purpose

Prometheus retains strict phase governance. Every irreversible
scientific or admissibility decision must continue to flow through a
full phase: authorization prompt, branch execution, implementation
report, closeout, separate merge phase, merge-closeout on `main`, and a
narrow `current-project-state.md` update. That discipline is how the
project earns trust in its own evidence.

This standard exists for a different problem: the project has begun to
accumulate phases whose ceremony is heavier than their risk. The
Phase 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E chain demonstrated
that the existing governance worked correctly — the failed gate was
recorded honestly, the cause was interpreted in a separate memo, the
fix was executed in a separate controlled phase, the gate was rerun in
a separate phase, and the result was recorded as a sibling artefact in
yet another phase. Five phases were used to canonicalize one sidecar's
line ending. That outcome was *correct*, because no standing policy
existed yet. It is also a clear signal that future bounded, well-
understood remediations need a lighter but still auditable path.

The goal of this standard is **not** to weaken governance. The goal is
to prevent process overhead from becoming the product. Future low-risk,
bounded, already-understood work should not receive the same ceremony
as new acquisition designs, new gate protocols, manifest semantic
transitions, label / feature / ML / strategy / backtest decisions, or
successor-state recordings. High-risk work continues to receive full
ceremony. Low-risk work receives proportional ceremony.

This standard is **prospective only**. It does not rewrite prior phase
history. Every phase merged into `main` before this standard remains
valid as recorded. The Phase 4bl-D through Phase 4bl-E chain stands
unchanged and is treated as the precedent that established the standing
sidecar-canonicalization remediation tier defined below.

## Authority

This document is **process-only**. It does not revise any retained
verdict, project lock, M0 governance, manifest state, label artefact,
gate protocol, canonical path policy, or strategy decision. Where this
standard conflicts with a specialist domain document on technical
content, the specialist document wins. Where another process file
conflicts on lifecycle, prompt design, report shape, merge-closeout
structure, or chat handoff content, the domain-specific process file
wins for its own surface (`phase-prompt-template.md`,
`operator-report-standard.md`, `merge-closeout-standard.md`,
`chat-branching-handoff-standard.md`,
`phase-workflow-standard.md`).

This standard does not authorize any successor phase. It does not
authorize Phase 4bm-A. It does not authorize multi-day normalization.
It does not authorize features, labels, diagnostics, ML, strategy,
backtests, acquisition, paper / shadow, live-readiness, deployment,
exchange-write, production keys, authenticated APIs, private endpoints,
user stream, MCP, Graphify, `.mcp.json`, or credentials.

## Core principle

**Ceremony must be proportional to risk.**

- **Full ceremony** for irreversible scientific or admissibility
  decisions.
- **Controlled lightweight ceremony** for bounded metadata
  remediations that satisfy a standing policy.
- **Batch ceremony** for repeated proven operations that follow an
  established protocol.
- **Minimal ceremony** for purely administrative documentation
  corrections that change no semantics.

Every tier is still auditable. Every tier still produces an
implementation report and (with the exception of Tier 4 admin) a
merge-closeout. Every tier still preserves retained verdicts, project
locks, governance, and the `data/microstructure/` non-commit rule.
What changes between tiers is the depth of the prompt, the length of
the report, the number of separately authorized phases needed, and the
breadth of the non-authorization block.

## Phase risk tiers

This standard defines four tiers. Every Prometheus phase must be
assignable to exactly one tier at authorization time.

---

### Tier 1 — Full Phase

**Use for** any phase whose effect could change scientific meaning,
admissibility, or downstream authorization, or whose error could
silently corrupt the project record.

Tier 1 includes (non-exhaustive):

- new acquisition designs;
- new acquisition executions;
- new raw / derived / feature / label / metrics dataset families;
- new dataset versions whose semantics differ from prior versions;
- first implementation of a gate;
- first execution of a gate over a new family / version;
- successor-state recording (Stage transitions);
- chronological split policy design and recording;
- diagnostics design and execution;
- ML feasibility memos;
- ML training;
- strategy specification;
- strategy implementation;
- backtest specification, plan, or execution;
- any change to manifest state semantics
  (`research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`, governance labels);
- any change to retained verdicts;
- any change to project locks (§11.6, §1.7.3, Phase 3p §4.7,
  Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11,
  Phase 4ak M0 + post-null cooldown, Phase 4al refined no-rescue +
  §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)`
  always-raises invariant, Phase 4bb-F canonical path policy);
- any phase that could affect research eligibility or downstream
  admissibility;
- any phase that introduces network access, credentials,
  exchange-write, paper / shadow, live-readiness, deployment,
  production-key creation, authenticated APIs, private endpoints,
  user stream, MCP, Graphify, or `.mcp.json`.

**Required ceremony.** Tier 1 must include all of:

- a full authorization prompt that satisfies
  `phase-prompt-template.md` (single phase named, allowed tracked
  files enumerated, allowed local gitignored outputs enumerated,
  strict non-scope enumerated, validation commands specified,
  fail-closed conditions specified);
- a dedicated branch named per the project's branch convention;
- a full implementation report under
  `docs/00-meta/implementation-reports/`;
- a full closeout under the same directory;
- a separate, separately authorized merge phase;
- a merge-closeout on `main` per `merge-closeout-standard.md` (all 16
  required sections);
- a narrow `current-project-state.md` paragraph and `Current phase`
  block update;
- the full relevant non-authorization block, written out explicitly
  rather than referenced.

**Recommended report length.** Long-form. There is no maximum length.
Brevity is not a virtue when scientific meaning, admissibility, or
governance are at stake.

---

### Tier 2 — Controlled Remediation Phase

**Use for** exactly one bounded, well-understood, low-risk fix where a
standing remediation policy exists and the prompt names exactly one
target.

Tier 2 includes (non-exhaustive):

- one known metadata fix to a single sidecar, gate report, or
  successor-state artefact;
- one sidecar canonicalization (CRLF → canonical LF) that satisfies
  the standing decision tree below;
- one deterministic artefact wrapper correction whose semantics are
  preserved byte-for-byte;
- one known local report regeneration that produces a byte-identical
  payload (idempotent);
- one bounded path pointer correction in a tracked doc that does not
  change governance meaning;
- one known local artefact metadata repair where the semantics are
  preserved.

**Criteria.** All of the following must hold for a Tier 2 phase to be
authorized:

- exactly one defined target named in the prompt;
- no policy ambiguity (a standing policy answers the question);
- the standing policy that authorizes the fix exists in the repo
  (this standard, the relevant specialist memo, or both);
- no scientific interpretation change (the fix does not change what
  the artefact means);
- no market-data mutation (raw zip / source CSV / underlying market
  data is byte-identical pre/post; if market data must change, the
  phase escalates to Tier 1);
- exact pre/post SHA proof for every touched artefact;
- proof that no other tracked or local artefact changed;
- no downstream successor authorization;
- no manifest semantic transition
  (`research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy` are unchanged on every actual
  manifest);
- no hidden broad rewrite (the phase does not also clean up
  unrelated paths, files, or wording).

**Required ceremony.** Tier 2 must include:

- an authorization prompt naming exactly one phase, exactly one
  target, the standing policy that authorizes the fix, allowed
  tracked files, allowed local gitignored outputs, and a strict
  non-scope referencing the standing exclusions;
- a dedicated branch;
- a **short-form** implementation report under
  `docs/00-meta/implementation-reports/` (see §8);
- a closeout;
- a separate merge phase (unless explicitly classified as Tier 4
  admin in the prompt, which it normally cannot be because Tier 2
  involves a controlled mutation);
- pre/post SHA evidence for every touched artefact;
- a "no-other-files-changed" proof (typically `git diff --check` and
  `git status` plus any relevant `find` over the affected namespace);
- a `current-project-state.md` update only if the project state
  actually changes (in many Tier 2 cases the project state does not
  change at all — for instance, a sidecar canonicalization does not
  alter retained verdicts, project locks, or the latest project-
  complete phase identity);
- a non-authorization block that may reference the canonical
  reusable blocks listed in §7 rather than restating every
  prohibition in full.

---

### Tier 3 — Batch Phase

**Use for** repeated known operations across many equivalent targets
where an operation template already exists and there is no per-item
policy ambiguity.

Tier 3 includes (non-exhaustive):

- repeated canonical sidecar checks across many files when no
  rewrite is required;
- repeated per-day artefact validation when the protocol is already
  established by a prior Tier 1 phase;
- repeated deterministic report production using a proven template;
- repeated SHA-pinning operations across a known artefact set;
- repeated `git check-ignore -v` audits across a known path set.

**Criteria.** All of the following must hold:

- the operation template already exists in the repo (a prior Tier 1
  phase introduced and validated it);
- no new semantics (the batch does not introduce a new check, new
  field, new validator, or new policy interpretation);
- no new policy decision (the batch executes existing policy);
- per-item result inventory is recorded (every target gets an
  explicit PASS / FAIL / NOT_APPLICABLE / ERROR row);
- failures are explicit and fail-closed (no silent skipping);
- no per-item ambiguity (each target is fully resolvable under the
  existing policy without operator intervention).

**Required ceremony.** Tier 3 must include:

- an authorization prompt naming the batch, the operation, the
  artefact family, the validation protocol, the per-item result
  format, and the strict non-scope;
- a dedicated branch;
- one implementation report that records per-item outcomes;
- a closeout;
- a separate merge phase;
- a merge-closeout on `main` per `merge-closeout-standard.md`;
- a `current-project-state.md` update if project state changes
  (often a batch validation phase does not change project state).

**Important.** A batch phase may not authorize downstream phases by
itself. A batch phase produces evidence. Acting on that evidence is a
separate operator decision and, depending on the action, a separate
Tier 1 / Tier 2 / Tier 3 phase. A batch PASS over 90 daily artefacts
does not authorize the next family, the next stage, or the next
admissibility decision.

A batch phase must itemize partial failure. If 89 of 90 targets PASS
and 1 FAILs, the phase reports `BATCH_PARTIAL_FAIL` (or similar) with
the failing item identified, and the phase does not silently round to
"success."

---

### Tier 4 — Administrative / Docs Correction

**Use for** purely administrative documentation corrections that
change no semantics, no data, no source behavior, and no governance
meaning.

Tier 4 includes (non-exhaustive):

- typo fixes;
- stale SHA placeholder fixups (for example, recording the actual
  final-`main` SHA into a `to be filled at commit time` placeholder
  inside an already-merged closeout);
- narrow wording corrections;
- navigation pointer corrections (broken internal link, wrong
  filename reference);
- non-semantic documentation cleanup;
- `current-project-state.md` formatting corrections;
- repository-internal cross-reference updates that do not change
  governance meaning.

**Criteria.** All of the following must hold:

- no data artefact touched;
- no source / test / script behavior changed;
- no governance meaning changed;
- no project state transition;
- no successor authorization;
- no change to retained verdicts or project locks;
- no change to manifest semantics or invariants.

**Required ceremony.** Tier 4 may include:

- a minimal authorization prompt naming the file(s) and the exact
  textual correction, the strict non-scope, and the validation
  command set (typically only `git diff --check` and `git status`);
- a dedicated branch (still required — direct commits to `main` are
  not the Prometheus convention);
- a minimal implementation report or, where the change is truly
  trivial, a short closeout note that records what was fixed and
  why;
- a merge phase (may use a short-form merge-closeout per
  `merge-closeout-standard.md` §10 short-form rules);
- validation limited to `git diff --check` and `git status`;
- no `current-project-state.md` update unless the correction is in
  `current-project-state.md` itself.

**Important.** Tier 4 is the only tier that may use a short-form
merge-closeout. All other tiers must use the full 16-section merge-
closeout structure.

---

## Escalation rules

Any phase must escalate to **Tier 1** if it does any of the
following, regardless of how small the change appears:

- changes data semantics (the meaning of a field, a column, a
  timestamp policy, a per-bar exclusion rule);
- changes a manifest (any field, any value, any tracked manifest
  file under `data/microstructure/manifests/` or
  `data/manifests/`);
- changes a successor-state meaning (adds, removes, or reinterprets
  a Stage marker);
- changes a gate protocol (adds, removes, or reinterprets a check;
  changes a fail-closed condition; changes a check ordering with
  semantic effect);
- relaxes a validator (loosens any input check, schema check,
  invariant check, or boundary check);
- amends a canonical policy (Phase 4bb-F path policy, Phase 3p
  §4.7 strict integrity gate, Phase 3v §8 stop-trigger-domain,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4ak M0, Phase 4al
  no-rescue, Phase 4aw `flip_research_eligible(...)` invariant);
- affects eligibility / admissibility (any change that could move
  any artefact toward `research_eligible: true` or
  `eligibility_gate_status != "pending"` on any actual manifest);
- creates features / labels / diagnostics;
- touches ML / strategy / backtest;
- changes retained verdicts (H0, R3, R1a, R1b-narrow, R2, F1,
  D1-A, V2, G1, C1, 5m thread closure);
- changes project locks (§11.6, §1.7.3, round-trip = 16 bps,
  taker fee = 4 bps per side, position sizing constants);
- introduces network access (any new endpoint, any new download,
  any new live data path);
- introduces credentials (any new secret, any `.env` field, any
  authenticated API path, any private endpoint);
- touches exchange-write / live paths (paper / shadow, live-
  readiness, deployment, production-key creation, real-money
  exposure).

If any of the above apply, the phase is Tier 1, period. The standing
remediation decision tree (§5) does not apply. The Tier 2 short-form
report does not apply. The reusable non-authorization blocks (§7) may
still be referenced inside a Tier 1 prompt for brevity, but the full
ceremony is required.

## Standing remediation decision tree

This standard establishes one prospective standing remediation rule.
Future standing rules may be added by separately authorized Tier 1
process phases that name this file in their allowed tracked files.

### Standing rule R-SIDECAR-CRLF — Sidecar line-ending canonicalization

A future Tier 2 Controlled Remediation Phase may canonicalize a
single Phase 4bb-F sidecar from CRLF to canonical LF without a
separately authorized governance memo, **if and only if** all of the
following hold:

1. the sidecar contains the correct embedded SHA256 (the embedded
   SHA matches the recomputed SHA256 of the byte-identical target
   file);
2. the sidecar contains the correct basename (the basename
   referenced in the sidecar matches the basename of the target
   file);
3. the sidecar points to a byte-identical target file (the target
   file's recomputed SHA256 matches the value recorded by the
   originating phase's implementation report or merge-closeout);
4. the sidecar differs from canonical Phase 4bb-F format only by
   line ending (CRLF vs LF);
5. the Phase 4bb-F canonical sidecar format is otherwise satisfied
   (two-space separator between SHA and basename, no extra tokens,
   no extra fields, no BOM, no other formatting drift).

**Required evidence.** A Tier 2 phase invoking R-SIDECAR-CRLF must
record:

- pre sidecar SHA256;
- post sidecar SHA256;
- pre sidecar size in bytes;
- post sidecar size in bytes;
- embedded SHA before;
- embedded SHA after (must equal embedded SHA before);
- target artefact SHA before;
- target artefact SHA after (must equal target artefact SHA
  before — the target file is byte-identical);
- line ending before (CRLF);
- line ending after (LF);
- byte delta (typically `-1` for a single-line CRLF → LF
  conversion);
- proof that no other tracked or local file changed (`git status`,
  `git diff --check`, plus any relevant `find` over the affected
  namespace);
- a local canonicalization report under
  `data/microstructure/canonicalization-reports/<family-subdir>/`
  if a `data/microstructure/` artefact is touched (gitignored,
  not committed, paired with its own SHA256 sidecar in canonical
  Phase 4bb-F format).

**Important.** R-SIDECAR-CRLF does **not** pre-authorize execution.
It only pre-selects the governance policy path. An operator
authorization prompt is still required. A branch is still required.
A short-form implementation report is still required. A separate
merge phase is still required. A merge-closeout is still required.
The standing rule changes only one thing: the operator does not
need to author a separate governance memo before the controlled
execution phase. The governance memo's reasoning is now part of
this standard.

### Why this rule is safe

The Phase 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E chain
established that:

- the failed gate did not corrupt data (the underlying raw zip was
  byte-identical to the Phase 4az fixture);
- the sidecar's embedded SHA was correct;
- the sidecar's basename was correct;
- the only deviation from canonical Phase 4bb-F format was the
  line ending;
- the controlled rewrite preserved every other byte of the sidecar
  and every byte of the target zip;
- the rerun of the Phase 4bl-D gate produced
  `RAW_MULTIDAY_GATE_PASS` against the unchanged manifest, log,
  zips, and other sidecars.

Future equivalent CRLF-only sidecar issues that satisfy criteria
1–5 reproduce a problem the project has already fully analyzed,
fixed, validated, and recorded. Re-authoring a governance memo for
each future occurrence adds ceremony without adding safety.

## Standing remediation exclusions

The R-SIDECAR-CRLF standing rule does **NOT** apply (and the phase
must escalate to Tier 1, or to a separately authorized governance
memo) if any of the following hold:

- the embedded SHA in the sidecar differs from the recomputed SHA
  of the target file;
- the basename in the sidecar differs from the actual target
  basename;
- the target file's SHA256 differs from the value recorded by the
  originating phase;
- the target file is missing;
- the sidecar contains extra tokens (extra fields, extra lines,
  comments, signatures);
- the sidecar points to a different file than expected;
- the sidecar repair would require changing market data (raw zip,
  CSV, underlying source);
- multiple unexplained artefacts are affected (the issue is not
  scoped to one sidecar line ending);
- governance policy is ambiguous (any criterion in §5 is
  uncertain);
- a manifest would need mutation;
- the fix could change scientific meaning;
- the fix would also touch derived / feature / label / metrics
  artefacts.

These cases require a Tier 1 phase or a dedicated governance memo
(or both) before any controlled execution phase is authorized.

## Reusable non-authorization blocks

Future authorization prompts and implementation reports may
reference canonical reusable non-authorization blocks instead of
restating every prohibition in full. Each block is named below and
is canonical when referenced verbatim. A prompt or report may
include a block by writing, for example: "Non-authorization block
N-ACQUISITION applies." or "This phase honors blocks N-ACQUISITION,
N-ENDPOINT, N-CREDENTIALS, N-MANIFEST." A Tier 1 phase should still
expand the relevant blocks in its full ceremony for clarity, but is
not required to do so when every block applies.

### N-ACQUISITION — No acquisition

The phase does not acquire data, does not download files, does not
fetch any new artefact from any remote source, does not extend any
existing dataset, and does not create or modify raw data files
under `data/microstructure/raw/` or `data/raw/`.

### N-ENDPOINT — No endpoint calls

The phase does not call any Binance endpoint (public, authenticated,
or private), does not call any other exchange or data-vendor
endpoint, does not call `data.binance.vision`, does not open any
WebSocket, and does not contact `fapi.binance.com`,
`api.binance.com`, or any equivalent.

### N-CREDENTIALS — No credentials, no exchange-write

The phase does not use, read, create, or reference any credential.
The phase does not read or create `.env`. The phase does not read
or create `.mcp.json`. The phase does not enable MCP or Graphify.
The phase does not place any order, modify any position, or
interact with any exchange-write surface.

### N-MANIFEST — No manifest mutation

The phase does not modify any actual manifest file. The phase does
not flip `research_eligible` on any actual manifest. The phase does
not transition `eligibility_gate_status` on any actual manifest.
The phase does not change `chronological_split_policy` on any
actual manifest. The phase preserves the Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never
invoked).

### N-GATE-RERUN — No gate rerun

The phase does not rerun any raw / derived / feature / label /
metrics gate. The phase does not generate any new gate report.

### N-SUCCESSOR-STATE — No successor-state

The phase does not create any new successor-state artefact. The
phase does not modify any existing successor-state artefact.

### N-DERIVATION — No normalization, derivation, features, or labels

The phase does not normalize, derive, compute features, or compute
labels. The phase does not run feature kernels. The phase does not
run label kernels. The phase does not produce derived / feature /
label parquet files.

### N-DIAGNOSTICS-ML-STRATEGY — No diagnostics, ML, strategy, or backtest

The phase does not run diagnostics. The phase does not train ML.
The phase does not design ML architecture. The phase does not rank
features. The phase does not create meta-labeling. The phase does
not create a strategy. The phase does not compute signals. The
phase does not run backtests. The phase does not compute PnL,
MFE, MAE, R-multiple, equity, position, alpha, edge, prediction,
model-score, decision-score, entry-exit, or strategy output.

### N-PHASE-5 — No Phase 5, paper / shadow, or live

The phase does not authorize Phase 5. The phase does not authorize
Phase 4 canonical. The phase does not authorize paper / shadow,
live-readiness, deployment, exchange-write, production-key
creation, authenticated APIs, private endpoints, user stream, or
live WebSocket implementation.

### N-VERDICT-LOCK — No retained verdict or project lock change

The phase does not revise any retained verdict (H0, R3, R1a,
R1b-narrow, R2, F1, D1-A, V2, G1, C1, 5m thread closure). The
phase does not change any project lock (§11.6, §1.7.3, round-trip
= 16 bps, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 /
§7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v,
Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families
list + memo template, Phase 4al refined no-rescue rule + §13
boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)`
always-raises invariant, Phase 4bb-F canonical path policy).

### Use-with-care

The reusable blocks are a convenience for clarity, not a way to
hide scope. A prompt or report that references a block must still
satisfy the underlying prohibition. If any part of a block is in
doubt, the prompt must restate it explicitly. The blocks are
defined here so that future Tier 2 / Tier 3 / Tier 4 phases can be
written compactly without losing audit value.

## Short-form report guidance

A **short-form** implementation report is acceptable when:

- the phase is Tier 2 (Controlled Remediation) with exactly one
  target;
- or the phase is Tier 4 (Administrative / Docs Correction);
- and the phase introduces no new data semantics;
- and the phase introduces no new scientific claim;
- and the phase introduces no new governance meaning.

A short-form report must still include:

1. **Phase identity.** Phase identifier, phase name, phase type,
   tier, branch name, base `main` SHA at branch creation.
2. **Target.** The exact artefact or text being changed; the
   exact path; the standing policy that authorizes the change
   (for Tier 2: the relevant standing rule from §5 of this
   standard); the reason this is a Tier 2 / Tier 4 fix and not a
   Tier 1 phase.
3. **Pre/post evidence.** For Tier 2: pre/post SHA256 for every
   touched artefact, pre/post size, line-ending state, byte
   delta, embedded-SHA preservation, target-file preservation
   proof, no-other-files-changed proof. For Tier 4: the diff or
   the textual change description, plus `git status` and
   `git diff --check`.
4. **Validation.** The exact validation commands run and their
   exact output (or the relevant snippet). For Tier 4 this is
   typically just `git diff --check` and `git status`.
5. **Boundaries.** A non-authorization block (referencing the
   reusable blocks in §7 by name where appropriate).
6. **Recommended state.** Typically `remain paused` for Tier 2;
   `remain paused` or `n/a` for Tier 4 (Tier 4 corrections
   normally do not change recommended state).
7. **No successor authorization.** Explicit statement that no
   successor phase is authorized.

A short-form report is shorter than a full Tier 1 implementation
report, but it is not less rigorous. Every fact required for audit
must still appear.

## Batch-phase guidance

A **batch phase** may handle many operations in one phase when:

- the same operation is performed on every target;
- the same artefact family is involved (or a tightly-scoped set of
  families with identical handling);
- the same validation protocol applies;
- the per-item result inventory is deterministic;
- there is no per-item policy ambiguity (no operator decision is
  needed mid-batch).

A batch phase must:

- record per-item PASS / FAIL / NOT_APPLICABLE / ERROR for every
  target;
- itemize failures explicitly (the failing item must be named, its
  SHA recorded, and its failure category recorded);
- never silently skip a target (a target that cannot be processed
  must be recorded as ERROR with the reason);
- never let batch success hide partial failure (if 89 of 90 targets
  PASS and 1 FAILs, the phase verdict is `BATCH_PARTIAL_FAIL` or
  equivalent, and the phase report does not advertise "success");
- not authorize downstream phases by itself unless explicitly in
  scope and the prompt explicitly grants that authorization (which
  is rare and should normally be a separate Tier 1 phase).

A batch phase that produces only PASS results is still a batch
phase. It does not become a single-target Tier 2 phase, and its
PASS does not authorize any successor by itself.

## Relationship to prior phases

The following statements about prior phase history are binding:

1. **Phase 4bl-D through Phase 4bl-E remain valid.** None of those
   phases are retroactively criticized or rewritten by this
   standard. Each was correct under the governance that existed at
   the time. Each implementation report and merge-closeout stands
   unchanged.
2. **The CRLF sidecar chain established the precedent for
   R-SIDECAR-CRLF.** Phase 4bl-D (the failed gate), Phase 4bl-D-S1
   (the governance memo), Phase 4bl-D-S2 (the controlled
   canonicalization), Phase 4bl-D-R (the gate rerun), and Phase
   4bl-E (the successor-state recording) together built the
   evidence base that makes the standing rule safe. Future
   equivalent CRLF-only sidecar issues may use Tier 2 controlled
   remediation directly under R-SIDECAR-CRLF, subject to the
   criteria in §5 and the exclusions in §6.
3. **Prior retained verdicts and project locks remain unchanged.**
   This standard does not touch H0 / R3 / R1a / R1b-narrow / R2 /
   F1 / D1-A / V2 / G1 / C1 / 5m thread closure. It does not touch
   §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8,
   Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p,
   Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null
   cooldown + cooled-down families list + memo template, Phase 4al
   refined no-rescue rule + §13 boundary + §14 hierarchy, Phase
   4aw `flip_research_eligible(...)` always-raises invariant, or
   Phase 4bb-F canonical path policy.

## Future application examples

The following examples illustrate how this standard applies to
plausible future phases. None of these examples authorize the
phases described.

| Scenario | Tier | Notes |
| --- | --- | --- |
| One CRLF-only sidecar with correct embedded SHA, correct basename, byte-identical target file | **Tier 2** | R-SIDECAR-CRLF applies; short-form report; pre/post SHA evidence required; merge-closeout required. |
| Sidecar with wrong embedded SHA | **Tier 1** | R-SIDECAR-CRLF does not apply; dedicated governance / remediation memo required before any execution phase. |
| Sidecar that points to a different file than expected | **Tier 1** | Underlying scientific question; dedicated governance memo required. |
| First multi-day normalization design memo (Phase 4bm-A or equivalent) | **Tier 1** | New design; new semantics; full ceremony. |
| First execution of multi-day normalization producing 90 daily partitions, where the design and protocol were locked by a prior Tier 1 phase and there is no per-item policy ambiguity | **Tier 3** | Batch phase; per-item PASS / FAIL inventory required; partial failure must be explicit; no downstream authorization by itself. |
| First execution of multi-day normalization where the per-item handling introduces new semantics (for example, a new invalid-window rule per-day) | **Tier 1** | New semantics; first execution semantics matter; full ceremony. |
| `current-project-state.md` typo or formatting fix | **Tier 4** | Minimal report; short-form merge-closeout permitted; no other-state changes. |
| README wording refresh that does not change governance meaning | **Tier 4** | Minimal report; short-form merge-closeout permitted. |
| README wording refresh that *does* change state semantics (for example, redefining a project lock or relabeling a retained verdict) | **Tier 1** | Escalation rule applies; full ceremony. |
| Label-generation kernel implementation | **Tier 1** | New family; new semantics; full ceremony. |
| ML baseline training | **Tier 1** | Touches ML; full ceremony. |
| Strategy backtest implementation or execution | **Tier 1** | Touches strategy / backtest; full ceremony. |
| Adding a new endpoint to a script | **Tier 1** | Introduces network access; escalation rule applies. |
| Adding a new credential to any config | **Tier 1** | Introduces credentials; escalation rule applies. |
| SHA-chain placeholder fixup recording the actual final-`main` SHA into a `to be filled at commit time` placeholder inside an already-merged closeout | **Tier 4** | Administrative correction; no governance meaning changes; short-form merge-closeout permitted. |
| Repeated SHA-pinning audit across a known artefact set, using a proven validation template, where every artefact is expected to PASS | **Tier 3** | Batch phase; per-item evidence; partial failure must be itemized. |

These examples are illustrative. Future ambiguous cases should
default to the higher tier when in doubt.

## Non-authorizations for Phase 4bl-F itself

Phase 4bl-F (this standard) explicitly does **not** authorize:

- changing any prior phase result;
- weakening the Phase 4bb-F canonical path policy;
- weakening the Phase 4bl-D raw multi-day eligibility gate or any
  of its 33 checks;
- weakening any other gate (Phase 4bb-D raw `__v001`, Phase 4bf
  derived, Phase 4bi-B feature, Phase 4bj-E label);
- weakening Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w
  §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
  Phase 4v, Phase 4w, or Phase 4ak M0 governance;
- weakening the Phase 4al refined no-rescue rule, §13 boundary,
  or §14 hierarchy;
- weakening the Phase 4aw `flip_research_eligible(...)` always-
  raises invariant;
- changing any actual manifest;
- flipping `research_eligible` on any actual manifest;
- transitioning `eligibility_gate_status` on any actual manifest;
- changing `chronological_split_policy` on any actual manifest;
- starting Phase 4bm-A or any successor;
- multi-day normalization design;
- multi-day normalization execution;
- features;
- labels;
- diagnostics;
- ML;
- strategy;
- backtests;
- acquisition;
- exchange-write;
- paper / shadow;
- live;
- production-key creation;
- authenticated APIs;
- private endpoints;
- user stream;
- live WebSocket implementation;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials;
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h /
  order-book data acquisition;
- any successor phase whatsoever.

The recommended state after Phase 4bl-F is **remain paused**.
Phase 4bm-A remains conditional and **not authorized**. The
operator has signalled an intent to pause for a broader project
discussion (complexity, phase usefulness, possible energy-market
sibling project) before any technical successor is authorized.

## Change-control process for this standard

This standard may be updated only by:

- a separately authorized docs-only Tier 1 process phase that
  names this file in its allowed tracked files;
- with a corresponding implementation report and closeout;
- merged into `main` with a merge-closeout that records the
  change;
- and a narrow `current-project-state.md` paragraph addition.

Updating this standard does not transition any technical state.
Updating it does not authorize any successor phase, does not
modify any manifest, does not enable ML / strategy / backtests,
and does not imply readiness for paper / shadow / live /
deployment / exchange-write.

## Required references for future chats

A future chat that uses this standard must also reference:

- `docs/00-meta/process/phase-workflow-standard.md` — master phase
  lifecycle manual;
- `docs/00-meta/process/phase-prompt-template.md` — authorization
  prompt structure;
- `docs/00-meta/process/operator-report-standard.md` — Claude Code
  compact report and ChatGPT operator-facing response shape;
- `docs/00-meta/process/merge-closeout-standard.md` — merge-
  closeout structure;
- `docs/00-meta/process/chat-branching-handoff-standard.md` —
  chat branching handoff structure;
- `docs/00-meta/current-project-state.md` — current project
  state;
- the most recent merge-closeout under
  `docs/00-meta/implementation-reports/`;
- the most recent phase implementation report.

## Final note

The Prometheus project's evidentiary discipline is its competitive
advantage. This standard does not relax that discipline. It
re-allocates ceremony so that bounded, well-understood, low-risk
work does not consume the same operator and reviewer attention as
admissibility, manifest, gate, label, ML, strategy, backtest, or
successor-state decisions. Full ceremony remains the default for
anything that could change scientific meaning. Lighter, still-
auditable ceremony is reserved for fixes whose meaning is already
fully analyzed and recorded.
