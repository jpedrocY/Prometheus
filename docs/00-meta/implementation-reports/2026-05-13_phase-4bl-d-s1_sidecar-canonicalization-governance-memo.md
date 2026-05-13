# Phase 4bl-D-S1 — Sidecar Canonicalization Governance Memo

## 1. Phase identity

- **Phase:** Phase 4bl-D-S1 — Sidecar Canonicalization Governance
  Memo
- **Type:** docs-only governance / remediation-decision memo
- **Branch:** `phase-4bl-d-s1/sidecar-canonicalization-governance-memo`
- **Base commit (`main` / `origin/main` at branch creation):**
  `01ca1d07c601655e3c66b6349038ea4385d4e281`
  (the Phase 4bl-D merge-closeout commit
  `docs(phase-4bl-d): add merge closeout`; in sync with `origin/main`
  at branch creation).
- **Project-complete anchor for Phase 4bl-D:** Per the Phase 4bk-A
  workflow standard, Phase 4bl-D is project-complete on `main` as of
  commit `01ca1d07c601655e3c66b6349038ea4385d4e281`. The Phase
  4bl-D merge-closeout's §2 "Merge-closeout commit SHA" placeholder
  reads "to be filled at commit time of this merge-closeout file";
  this Phase 4bl-D-S1 memo records that the canonical Phase 4bl-D
  project-complete anchor is `01ca1d07c601655e3c66b6349038ea4385d4e281`
  and acknowledges that no separately authorized SHA-chain-fixup
  commit has updated §2 yet. The lifecycle semantics are unchanged:
  Phase 4bl-D is project-complete; any future one-commit SHA-chain
  fixup would only record the final-`main` SHA value into the §2
  placeholder.
- **Status statement:** This memo is **docs-only**. It does **not**
  modify source code, tests, scripts, `pyproject.toml`, `README.md`,
  `.gitignore`, `.gitattributes`, MCP files, data, manifests,
  sidecars, gate reports, successor-state artefacts, local artefacts,
  or runtime artefacts. It performs **no** sidecar rewrite, **no**
  sidecar normalization, **no** Phase 4bb-F canonical path policy
  amendment, **no** Phase 4bl-D gate amendment, **no** gate rerun,
  and **no** authorization of any successor phase.

## 2. Pre-state

### Phase 4bl-C acquisition

Phase 4bl-C (merged at `691e68c`; merge-closeout `2ec0a9a`;
SHA-chain-fixup `2576a00`) successfully acquired the locked 90
contiguous UTC dates 2024-12-01 through 2025-02-28 for BTCUSDT
from public unauthenticated `data.binance.vision` daily aggTrades
archives. All 90 dates were SHA256-verified against their paired
`.CHECKSUM` companions with zero mismatches. Aggregate result:

- `acquired_file_count`: 90 / 90
- `missing_file_count`: 0
- `checksum_mismatch_count`: 0
- `total_size_bytes`: 1,943,823,208 (~1.81 GiB)
- `total_row_count`: 155,153,449
- v002 raw manifest:
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`
  - SHA256:
    `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
- v002 acquisition log:
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json`
  - SHA256:
    `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
- v002 manifest state: `research_eligible: false`,
  `eligibility_gate_status: "pending"` (locked invariants for raw
  families per Phase 4bb-E).

The Phase 4az 2025-01-15 fixture (`BTCUSDT-aggTrades-2025-01-15.zip`;
SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`;
21,271,119 bytes) was detected at the canonical path, three-way
cross-verified (recorded SHA ↔ fresh local SHA ↔ fresh `.CHECKSUM`
companion SHA — all three match bit-for-bit), and reused in place;
its **zip** is byte-identical to the Phase 4az fixture.

### Phase 4bl-D gate FAIL

Phase 4bl-D (merged at `093c42c`; merge-closeout `01ca1d0`)
implemented and ran a comprehensive multi-day raw eligibility gate
against the Phase 4bl-C v002 manifest and per-file inventory, with
full per-row Phase 4ax `validate_aggtrade_payload` validation.
Exact gate result:

- `overall_status`: **fail** (`RAW_MULTIDAY_GATE_FAIL`)
- `checks_total / passed / failed / error / not_applicable`:
  33 / 29 / 4 / 0 / 0
- `recomputed_total_row_count`: 153,472,351
  (manifest expected 155,153,449; shortfall exactly 1,681,098 — the
  recorded Phase 4az 2025-01-15 row count)
- `recomputed_total_size_bytes`: 1,943,823,208 (matches manifest
  exactly)
- `all_rows_validated_count`: 153,472,351
- `all_schema_validation_errors_count`: 0
- `all_timestamp_boundary_errors_count`: 0
- `all_duplicate_agg_trade_id_errors_count`: 0
- `all_monotonicity_errors_count`: 0
- `adjacent_date_overlap_errors_count`: 0
- `acquired_file_count`: 89 / 90 reached full per-row validation
- `existing_fixture_preservation_zip_sha`: pass (2025-01-15 zip
  SHA matches the Phase 4az recorded value exactly)
- `manifest_mutated`: false
- `manifest_transition_performed`: false
- `research_eligible_after`: false
- `eligibility_gate_status_after`: `fail_report_level_only`
  (report-level only; the on-disk v002 manifest's
  `eligibility_gate_status` remains `"pending"`)
- `no_successor_authorization`: true
- `strict_fail_closed`: true
- Phase 4bl-D gate report:
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json`
  - SHA256:
    `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`
  - Size: 169,637 bytes
  - Local gitignored under `.gitignore:85: data/microstructure/`;
    not committed.

### Single root cause

The pre-existing Phase 4az 2025-01-15 fixture **sidecar** at

```
data/microstructure/raw/microstructure_raw_aggtrades_v001/
BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256
```

uses Windows CRLF (`\r\n`) line terminator (100 bytes) instead of
the canonical Phase 4bb-F LF (`\n`) terminator (99 bytes for the
same basename). All 89 Phase 4bl-C newly-acquired sidecars, the
v002 manifest sidecar, and the v002 acquisition-log sidecar use
canonical LF. Under fail-closed discipline, the Phase 4bl-D gate's
`parse_canonical_sidecar(...)` rejected the CRLF form, marked the
2025-01-15 per-file `status = fail`, and skipped per-row iteration
for that file only. The other 89 dates' full per-row validation
passed cleanly with zero schema, timestamp, duplicate, monotonicity,
or adjacent-date overlap errors.

### Phase 4az fixture preservation

- 2025-01-15 raw zip:
  - SHA256:
    `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  - Size: 21,271,119 bytes
  - **Byte-identical** to the Phase 4az fixture (verified by
    three-way cross-check at Phase 4bl-C acquisition time and
    again at Phase 4bl-D gate run).
- 2025-01-15 sidecar:
  - Size: 100 bytes (CRLF terminator)
  - Embedded SHA value: matches the raw zip SHA exactly
    (`f560c2e5…`)
  - The **embedded SHA value is correct**; only the line terminator
    is non-canonical under the later Phase 4bb-F sidecar policy.

### Manifest state and successor authorization

- The on-disk v002 raw manifest's `research_eligible` remains
  `false` (locked invariant for raw families per Phase 4bb-E).
- The on-disk v002 raw manifest's `eligibility_gate_status` remains
  `"pending"`. The gate-report-level
  `eligibility_gate_status_after = "fail_report_level_only"` is a
  report-level recommendation only; it does not transition the
  on-disk manifest field.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant remains intact (never invoked by
  Phase 4bl-D or Phase 4bl-D-S1).
- **No successor phase is authorized.**

### Why Phase 4bl-E is not appropriate now

Phase 4bl-E (Multi-Day Raw Manifest Successor-State Recording) is
the natural conditional successor to a PASS raw eligibility gate.
The project's established lifecycle for raw-family successor-state
recording is:

```
raw acquisition (PASS) → raw integrity gate (PASS) →
successor-state recording (Phase 4bb-G precedent)
```

Phase 4bl-D produced a **FAIL** gate verdict. Proceeding directly
to Phase 4bl-E would record a successor-state for a manifest whose
companion gate verdict is FAIL, which would:

- contradict the Phase 4bb-G precedent
  (`stage2_raw_admissible` was recorded only after Phase 4bb-D
  produced a PASS report with 45 / 45 PASS);
- imply that the Phase 4bl-D gate verdict can be ignored or
  overridden by successor-state recording;
- weaken the fail-closed discipline that produced the FAIL in the
  first place;
- record an admissibility marker for a manifest whose evidence
  base contains a non-canonical sidecar that the strict gate
  rejected.

Phase 4bl-E therefore **remains unauthorized** until either (i) the
sidecar is canonicalized and a future gate rerun produces PASS, or
(ii) the operator separately authorizes a governance amendment
that explicitly allows successor-state recording without a
preceding PASS gate (no such amendment is recommended by Phase
4bl-D-S1).

## 3. Failure interpretation

It is important to distinguish four distinct statuses that the
Phase 4bl-D FAIL might be conflated with:

- **Data-integrity status: VALID.** The 2025-01-15 raw zip is
  byte-identical to the Phase 4az fixture; the embedded sidecar
  SHA value matches the raw zip SHA exactly; the other 89 dates'
  per-row validation produced zero schema, timestamp, duplicate,
  monotonicity, or adjacent-date overlap errors; aggregate
  recomputed size matches the v002 manifest's recorded value
  exactly. The acquired market data is uncorrupted and intact.
- **Sidecar-format status: NON-CANONICAL.** The 2025-01-15
  sidecar's line terminator is Windows CRLF (100 bytes) instead of
  canonical Phase 4bb-F LF (99 bytes). This is a metadata-format
  deviation from the canonical sidecar contract, not a data-
  corruption signal.
- **Gate status: FAIL.** Under strict canonical parsing, the Phase
  4bl-D gate correctly rejected the CRLF sidecar and emitted FAIL.
  This is the **correct** behaviour of a fail-closed gate: it
  surfaced the deviation rather than silently accepting it.
- **Research / strategy status: NO CHANGE.** The FAIL is **not**
  evidence of a strategy edge, a research conclusion, or a market
  finding. It is a metadata-format finding only. The retained
  verdict ledger and project locks remain preserved verbatim.
- **Remediation status: NOT YET AUTHORIZED.** The Phase 4bl-D
  closeout's §"Recommended state" enumerates three remediation
  options (B1 / B2 / B3) but explicitly **did not recommend any of
  the three** — the operator decision was deferred to a separately
  authorized governance memo. This memo (Phase 4bl-D-S1) is that
  memo.

The most important distinction is between **data integrity** and
**metadata format**. A fail-closed gate that rejects a non-canonical
sidecar is doing its job. The remedy depends on whether the project
treats the sidecar contract as immutable or amendable, and whether
the fixture artefact is treated as immutable or as eligible for
metadata-format canonicalization.

## 4. Governance question

**Question:** What is the correct governance response to a
pre-existing fixture sidecar whose embedded SHA value is correct
but whose line terminator is non-canonical under the later
Phase 4bb-F sidecar policy?

This phrasing is deliberate. It separates the two things that
could be "wrong":

- the **embedded SHA value** (it is **correct**; the sidecar
  correctly identifies the raw zip's contents);
- the **line terminator** (it is **non-canonical** under the
  later Phase 4bb-F policy that the project adopted after the
  Phase 4az fixture was created).

The Phase 4az fixture predates the Phase 4bb-F canonical sidecar
format. The Phase 4bb-F policy was adopted prospectively, not
retroactively, but the Phase 4bl-D gate enforces it across all
files referenced by the v002 manifest, including the pre-existing
Phase 4az fixture. The question is therefore: how should the
project resolve the tension between (i) the immutability of a
pre-existing fixture artefact and (ii) the strict enforcement of a
later-adopted canonical-format contract?

Sub-questions:

- Should the fixture sidecar be **canonicalized in place**, on the
  grounds that line-terminator normalization is a metadata-format
  change and does not affect the embedded SHA value?
- Should the **Phase 4bb-F policy** be amended to grandfather the
  Phase 4az sidecar, on the grounds that the policy was adopted
  after the fixture existed?
- Should the **gate** be amended to accept CRLF as
  canonical-equivalent, on the grounds that a strict line-
  terminator check is overly brittle for a metadata-format
  contract?
- Should the project **remain paused** indefinitely, on the
  grounds that the FAIL is descriptive evidence only and does not
  prevent any other work the operator might want to authorize?

## 5. Option table

Seven options are evaluated below. The evaluation columns are
chosen to expose the trade-offs the operator decision must
balance:

- **Data immutability** — does the option preserve the raw zip
  byte-identically? (The raw zip is the market-data artefact;
  preserving it is the highest priority.)
- **Metadata mutation** — does the option mutate the sidecar
  file's bytes? (Mutating a pre-existing fixture artefact's bytes
  is non-trivial and must be transparent.)
- **Governance amendment** — does the option mutate the Phase
  4bb-F canonical sidecar contract? (Governance amendments must
  be explicit and separately authorized.)
- **Gate strictness** — does the option weaken the strict
  fail-closed gate? (Weakening the gate has long-term reliability
  consequences.)
- **Auditability** — does the option preserve a clear,
  recoverable audit trail?
- **Likely future PASS** — would a future gate rerun be likely to
  produce PASS under this option, given the rest of the v002
  artefacts are clean?
- **Risk of hiding evidence** — does the option silently
  suppress, normalize away, or hide evidence the gate surfaced?
- **Risk of overfitting** — does the option overfit the project's
  governance posture to one incident?
- **Phase 4bb-F compatibility** — does the option preserve the
  Phase 4bb-F canonical path policy verbatim?
- **Fail-closed compatibility** — does the option preserve the
  strict fail-closed discipline?

### Option A — remain paused

Do nothing. Leave the Phase 4az 2025-01-15 sidecar unchanged at
100 bytes (CRLF). Leave the Phase 4bb-F canonical sidecar contract
unchanged. Leave the Phase 4bl-D gate unchanged. Do not authorize
any successor phase. Treat the Phase 4bl-D FAIL as a permanent
descriptive finding.

| Dimension | A — remain paused |
| --- | --- |
| Data immutability | preserved (no mutation) |
| Metadata mutation | none |
| Governance amendment | none |
| Gate strictness | preserved |
| Auditability | preserved (FAIL recorded verbatim in
  Phase 4bl-D gate report; remediation gap recorded in this
  memo) |
| Likely future PASS | **no** — the FAIL persists indefinitely; no
  PASS is possible without remediation |
| Risk of hiding evidence | none |
| Risk of overfitting | none |
| Phase 4bb-F compatibility | preserved |
| Fail-closed compatibility | preserved |

A is the maximally conservative posture. It is acceptable as a
default. It does not unlock Phase 4bl-E or any forward arc, and it
leaves the gate FAIL as a permanent finding rather than as a
resolved issue.

### Option B1 — normalize the Phase 4az 2025-01-15 sidecar to canonical LF

Mutate exactly one sidecar file's line terminator from CRLF to LF,
preserving the embedded SHA value bit-for-bit and the raw zip
byte-identically. The change is from 100 bytes to 99 bytes
(removal of one `\r`). The mutation must be performed in a
separately authorized execution phase (Phase 4bl-D-S2) that
verifies pre-state, performs the rewrite atomically, verifies
post-state, and records the mutation transparently. A future
gate rerun (Phase 4bl-D-R) is then required to confirm PASS.

| Dimension | B1 — normalize sidecar |
| --- | --- |
| Data immutability | preserved (raw zip byte-identical;
  embedded SHA value byte-identical) |
| Metadata mutation | yes (one sidecar file's line terminator
  changed; one byte removed) |
| Governance amendment | none |
| Gate strictness | preserved |
| Auditability | preserved if the execution phase records
  pre/post SHA and byte sizes with full evidence |
| Likely future PASS | **yes** — under strict canonical parsing,
  a canonicalized sidecar should produce PASS; all other 32
  checks already pass; the four failed checks all cascade from
  this single root cause |
| Risk of hiding evidence | low — the original CRLF state is
  recorded in Phase 4bl-D gate report and in Phase 4bl-D-S1; the
  canonicalization is transparent and reversible if needed |
| Risk of overfitting | low — line-terminator canonicalization
  is a one-line transformation; the project does not generalize
  the precedent |
| Phase 4bb-F compatibility | preserved |
| Fail-closed compatibility | preserved |

B1 is the cleanest practical path. It treats the sidecar's line
terminator as a metadata format that must conform to the
canonical contract; it preserves the embedded SHA value and the
raw zip byte-identically; it preserves the canonical sidecar
contract and the strict gate; and it produces a future PASS
without amending governance.

### Option B2 — amend Phase 4bb-F to grandfather CRLF sidecars

Amend the Phase 4bb-F canonical path policy to recognize CRLF as
an acceptable line terminator for pre-existing fixture sidecars
created before the policy was adopted, while keeping LF as the
default for new sidecars.

| Dimension | B2 — amend Phase 4bb-F |
| --- | --- |
| Data immutability | preserved (no mutation) |
| Metadata mutation | none |
| Governance amendment | **yes** — Phase 4bb-F is amended |
| Gate strictness | weakened (the canonical contract now has two
  acceptable terminators, with a grandfathering rule that
  introduces case-by-case complexity) |
| Auditability | preserved if the amendment is documented |
| Likely future PASS | yes — the gate, if also amended (or
  retrofitted to consult Phase 4bb-F's revised contract), would
  PASS |
| Risk of hiding evidence | medium — the FAIL becomes
  retroactively reclassified as "acceptable under grandfathering"
  rather than resolved |
| Risk of overfitting | **high** — the project would amend a
  general governance contract to accommodate a single fixture |
| Phase 4bb-F compatibility | not preserved (the policy is
  amended) |
| Fail-closed compatibility | weakened (grandfathering carves an
  exception into the fail-closed contract) |

B2 is weaker than B1. It preserves the sidecar bytes but at the
cost of amending a general governance contract for a single
fixture. The amendment would also need to be propagated to the
gate, the canonical-path helpers, and any future raw / derived /
feature / label gate's sidecar parser — all to preserve one
non-canonical sidecar.

### Option B3 — amend the gate to accept CRLF as canonical-equivalent

Amend the Phase 4bl-D gate script (and any future raw / derived /
feature / label gate's sidecar parser) to accept CRLF as
canonical-equivalent to LF. Leave the Phase 4bb-F policy
unchanged or update it to clarify that the gate accepts both.

| Dimension | B3 — amend the gate |
| --- | --- |
| Data immutability | preserved (no mutation) |
| Metadata mutation | none |
| Governance amendment | partial — the gate's strictness is
  loosened; the Phase 4bb-F policy may or may not be updated to
  match |
| Gate strictness | weakened (the strict parser now accepts two
  terminators) |
| Auditability | preserved if the amendment is documented |
| Likely future PASS | yes — the gate would PASS |
| Risk of hiding evidence | medium — the FAIL becomes
  retroactively reclassified as "acceptable under relaxed
  parser" rather than resolved |
| Risk of overfitting | **high** — the gate is weakened to
  accommodate a single fixture; the precedent generalizes to all
  future gates |
| Phase 4bb-F compatibility | partial — Phase 4bb-F may still
  declare LF canonical even though the gate accepts CRLF,
  introducing a gap between the policy and the gate |
| Fail-closed compatibility | weakened (the gate is no longer
  strictly fail-closed on line terminator) |

B3 is weaker than B2. It introduces a divergence between the
canonical policy (which the project documents as authoritative)
and the actual gate (which tolerates a deviation from the
canonical policy). Future raw / derived / feature / label gates
would inherit the weakened parser and the weaker fail-closed
posture.

### Option C — proceed to Phase 4bl-E despite the FAIL

Record a Phase 4bl-E successor-state JSON for the v002 raw
manifest with `successor_admissibility_status =
"admissible_in_principle_policy_level_only"` (mirroring the
Phase 4bb-G precedent for the Phase 4az raw family) but cite the
Phase 4bl-D FAIL as the gate-report evidence.

| Dimension | C — proceed to Phase 4bl-E despite FAIL |
| --- | --- |
| Data immutability | preserved |
| Metadata mutation | yes — a new successor-state JSON is
  written |
| Governance amendment | **yes** — the gate-pass-first precedent
  is implicitly amended |
| Gate strictness | weakened (a successor-state is recorded
  despite the gate emitting FAIL) |
| Auditability | preserved at artefact level, but the
  governance precedent is muddled |
| Likely future PASS | not applicable — C bypasses the gate
  question |
| Risk of hiding evidence | **high** — the FAIL is recorded but
  the successor-state implies admissibility |
| Risk of overfitting | high — the project's gate-pass-first
  precedent is broken to accommodate one incident |
| Phase 4bb-F compatibility | preserved |
| Fail-closed compatibility | weakened (the successor-state
  contract is decoupled from gate-PASS) |

C is unacceptable. It directly contradicts the Phase 4bb-G
precedent, which recorded a `stage2_raw_admissible` successor-state
**only after** Phase 4bb-D produced a PASS gate report with
45 / 45 PASS. The Phase 4bl-D gate produced FAIL; the parallel
precedent does not apply.

### Option D — rerun the gate without remediation

Rerun the Phase 4bl-D gate against the unchanged v002 artefacts
without canonicalizing the sidecar.

| Dimension | D — rerun without remediation |
| --- | --- |
| Data immutability | preserved |
| Metadata mutation | none |
| Governance amendment | none |
| Gate strictness | preserved |
| Auditability | preserved (the rerun produces a new gate
  report) |
| Likely future PASS | **no** — the rerun will produce the same
  FAIL (the gate is deterministic; the root cause is unchanged) |
| Risk of hiding evidence | none |
| Risk of overfitting | none |
| Phase 4bb-F compatibility | preserved |
| Fail-closed compatibility | preserved |

D is acceptable as a sanity check (a determinism test) but does
not resolve the FAIL. It is not a remediation option; it is a
verification option. It is not authorized by Phase 4bl-D-S1.

### Option E — manually override / ignore the gate failure

Annotate the Phase 4bl-D gate report or the v002 manifest with a
manual override that classifies the FAIL as "ignored" or
"superseded by operator decision" without remediating the
sidecar.

| Dimension | E — manual override |
| --- | --- |
| Data immutability | preserved |
| Metadata mutation | yes — manifest or gate report is
  annotated |
| Governance amendment | **yes** — the fail-closed contract is
  amended to allow override |
| Gate strictness | **destroyed** |
| Auditability | weakened (overrides create governance fog) |
| Likely future PASS | not applicable |
| Risk of hiding evidence | **critical** — manual overrides
  silently suppress fail-closed evidence |
| Risk of overfitting | critical |
| Phase 4bb-F compatibility | weakened or destroyed |
| Fail-closed compatibility | **destroyed** |

E is unacceptable. It violates fail-closed discipline at the
strongest possible level. It is not authorized by Phase 4bl-D-S1.

## 6. Recommended policy

**Recommendation: Option B1 — normalize the Phase 4az 2025-01-15
sidecar to canonical LF.**

This recommendation is binding on this memo only as a policy
recommendation; it does **not** authorize execution. Execution
requires a separately authorized Phase 4bl-D-S2 controlled
sidecar canonicalization execution phase.

### Why B1

- **B1 is a metadata canonicalization, not market-data
  mutation.** The only mutation is the removal of one carriage-
  return byte (`\r`) from one sidecar file. The raw zip is
  preserved byte-identically. The embedded SHA value in the
  sidecar is preserved byte-identically. The aggregate manifest
  state is unchanged (`research_eligible: false`,
  `eligibility_gate_status: "pending"`).
- **B1 preserves the Phase 4bb-F canonical sidecar contract
  unchanged.** Other options (B2, B3) would amend the contract.
- **B1 preserves the strict fail-closed gate unchanged.** Other
  options (B3) would weaken it.
- **B1 produces a likely future PASS** if a future gate rerun is
  separately authorized. The four failed checks all cascade from
  one root cause; canonicalizing the sidecar removes the cascade.
- **B1 is transparent and reversible.** The Phase 4bl-D gate
  report records the pre-canonicalization CRLF state verbatim;
  the future Phase 4bl-D-S2 execution would record the
  pre/post sidecar SHA, byte size, and line-ending state with
  full evidence; the original sidecar could be re-derived if
  needed (it is a one-line file with a known SHA value and a
  known canonical-format target).
- **B1 does not overfit governance to one incident.** It treats
  the sidecar as a metadata-format file that must conform to the
  canonical contract, exactly as 89 / 90 Phase 4bl-C sidecars
  already do.
- **B1 is the only option that resolves the FAIL without
  amending governance or weakening the gate.**

### Strict scope of B1

B1 is **scoped to one sidecar file**:

- target path:
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
- target mutation: line-terminator canonicalization (CRLF → LF)
- expected pre-state size: 100 bytes
- expected post-state size: 99 bytes
- expected byte delta: -1 (removal of one `\r`)
- embedded SHA value before:
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
- embedded SHA value after: **identical**
- associated raw zip:
  `BTCUSDT-aggTrades-2025-01-15.zip`
- associated raw zip SHA256:
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
- raw zip mutation: **none** (raw zip is preserved byte-
  identically)

No other sidecar file is mutated by B1. No raw zip is mutated by
B1. No manifest is mutated by B1. No gate report is mutated by
B1. No successor-state is created by B1. No Phase 4bb-F amendment
is made by B1. No gate amendment is made by B1.

### B1 is a remediation, not an authorization

B1 is a remediation that, if executed, resolves the Phase 4bl-D
FAIL root cause. It does **not** authorize:

- recording a successor-state for the v002 manifest;
- transitioning the v002 manifest's `eligibility_gate_status` from
  `"pending"` to `"pass"`;
- flipping the v002 manifest's `research_eligible` from `false`
  to `true`;
- normalization, derivation, feature computation, label
  computation, diagnostics, ML, strategy, signals, backtests,
  or any successor phase.

A separately authorized Phase 4bl-D-R rerun gate is required to
confirm that the canonicalization resolves the FAIL (likely PASS;
not guaranteed). A separately authorized Phase 4bl-E successor-
state recording phase remains the natural conditional next step
**only after** Phase 4bl-D-R produces a PASS.

## 7. Controlled execution requirements for future Phase 4bl-D-S2

If the operator separately authorizes a future Phase 4bl-D-S2
controlled sidecar canonicalization execution phase, that phase
must satisfy the following binding requirements. These
requirements are recorded here as governance for the future
phase; **Phase 4bl-D-S1 does not authorize Phase 4bl-D-S2**.

### Pre-execution verification

Before any mutation, Phase 4bl-D-S2 must verify:

- `git rev-parse main` and `git rev-parse origin/main` are in
  sync;
- the Phase 4bl-D merge-closeout commit is present on `main`;
- the Phase 4bl-D-S1 merge-closeout commit is present on `main`
  (Phase 4bl-D-S1 must be project-complete before Phase 4bl-D-S2
  begins);
- the target sidecar exists at the canonical path:
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256`
- the target sidecar's current size is exactly **100 bytes**;
- the target sidecar's current byte content ends with the
  two-byte CRLF sequence `\r\n` (not just `\n`);
- the target sidecar's embedded SHA value (the first 64
  characters) equals exactly:
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
- the target sidecar's basename in the body equals exactly:
  `BTCUSDT-aggTrades-2025-01-15.zip`
- the associated raw zip exists at:
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`
- the associated raw zip's recomputed SHA256 equals:
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
- the associated raw zip's current size is exactly **21,271,119
  bytes**;
- the v002 raw manifest's SHA256 equals:
  `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`
- the v002 acquisition log's SHA256 equals:
  `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`
- the Phase 4bl-D gate report's SHA256 equals:
  `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`

If any precondition fails, Phase 4bl-D-S2 must **fail closed**
with a clear status report and must not mutate any artefact.

### Mutation specification

Phase 4bl-D-S2 must rewrite exactly one sidecar file to the
following canonical content:

```
<sha>  BTCUSDT-aggTrades-2025-01-15.zip\n
```

where `<sha>` is the 64-character lowercase hex SHA256 value
`f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`,
followed by exactly two ASCII space characters (`0x20 0x20`),
followed by the basename `BTCUSDT-aggTrades-2025-01-15.zip`,
followed by exactly one LF byte (`\n`, `0x0A`). The total file
size must be exactly **99 bytes**.

The mutation must be performed atomically: write to a temporary
file, then `os.replace` onto the target path. No other file
under `data/microstructure/` may be opened for write.

### Post-execution verification

After the mutation, Phase 4bl-D-S2 must verify:

- the target sidecar's post-mutation size is exactly **99 bytes**;
- the target sidecar's post-mutation byte content ends with a
  single LF (`\n`), not CRLF;
- the target sidecar's post-mutation embedded SHA value equals
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  (identical to pre-mutation);
- the target sidecar's post-mutation basename in the body equals
  `BTCUSDT-aggTrades-2025-01-15.zip` (identical to pre-mutation);
- the associated raw zip's recomputed SHA256 equals
  `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  (unchanged);
- the associated raw zip's size is exactly **21,271,119 bytes**
  (unchanged);
- the v002 raw manifest's SHA256 is unchanged
  (`016967865c…d87485`);
- the v002 acquisition log's SHA256 is unchanged
  (`52f6d7fb3c…c6b314`);
- the Phase 4bl-D gate report's SHA256 is unchanged
  (`d97948ed4d…6629e7`);
- no other file under `data/microstructure/` has been modified;
- the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant is preserved (never invoked by
  Phase 4bl-D-S2);
- the v002 raw manifest's `research_eligible` remains `false`;
- the v002 raw manifest's `eligibility_gate_status` remains
  `"pending"`;
- no successor-state artefact is created.

### Output artefact

Phase 4bl-D-S2 must write a local gitignored **canonicalization
report** plus paired SHA256 sidecar under

```
data/microstructure/canonicalization-reports/raw/
microstructure_raw_aggtrades_v001__v002__phase-4bl-d-s2__
<unix_ms>__<short_commit>.json
```

(or an equivalent path that conforms to Phase 4bb-F canonical
path policy and that the operator approves at authorization time).
The report's schema is defined in §8 of this memo. The paired
sidecar must use canonical Phase 4bb-F format
(`<sha>  <basename>\n`; 99 bytes equivalent for the basename).

### Tracked commits

Phase 4bl-D-S2 must commit only:

- the Phase 4bl-D-S2 implementation report under
  `docs/00-meta/implementation-reports/`;
- the Phase 4bl-D-S2 closeout under
  `docs/00-meta/implementation-reports/`;
- a narrow `docs/00-meta/current-project-state.md` update
  (new Phase 4bl-D-S2 narrative paragraph + new "Current phase:"
  block; prior block preserved as historical context);
- optionally, a tiny standalone script and/or offline test under
  `scripts/` and `tests/research/microstructure/` if Phase
  4bl-D-S2's authorization prompt approves them; the scope must
  be no broader than a one-file rewrite and its test fixture.

Phase 4bl-D-S2 must **not** commit anything under
`data/microstructure/`. The canonicalization report and its
paired sidecar live under the gitignored
`data/microstructure/canonicalization-reports/` namespace and are
**not** committed.

### Gate-rerun boundary

Phase 4bl-D-S2 must **not** rerun the Phase 4bl-D gate. A
separately authorized Phase 4bl-D-R rerun phase is required for
that (see §9 of this memo).

### Non-authorizations carried forward

Phase 4bl-D-S2 must not authorize Phase 4bl-D-R, Phase 4bl-E, or
any other successor phase. It must not modify the v002 manifest.
It must not flip `research_eligible`. It must not transition
`eligibility_gate_status`. It must not change
`chronological_split_policy`. It must not acquire data. It must
not call any Binance endpoint. It must not use credentials, MCP,
Graphify, `.mcp.json`, or `.env`.

## 8. Future report schema for Phase 4bl-D-S2

If Phase 4bl-D-S2 is separately authorized and executed, its
canonicalization report should include the following fields. The
exact JSON field names and types are recorded here as governance;
small field-name adjustments may be made at authorization time
provided the spirit of each field is preserved.

```json
{
  "schema_version": "v001",
  "phase": "Phase 4bl-D-S2",
  "phase_id": "4bl-D-S2",
  "artefact_type": "sidecar_canonicalization_report",

  "target_sidecar_path":
    "data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip.sha256",
  "target_zip_path":
    "data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip",

  "pre_sidecar_sha256":  "<recomputed sidecar SHA256 before mutation>",
  "post_sidecar_sha256": "<recomputed sidecar SHA256 after mutation>",
  "pre_sidecar_size_bytes":  100,
  "post_sidecar_size_bytes": 99,

  "embedded_zip_sha256_before":
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e",
  "embedded_zip_sha256_after":
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e",

  "target_zip_sha256_before":
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e",
  "target_zip_sha256_after":
    "f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e",

  "line_ending_before": "CRLF",
  "line_ending_after":  "LF",
  "byte_delta": -1,

  "mutation_type": "metadata_sidecar_line_ending_canonicalization",
  "market_data_mutated": false,
  "raw_zip_mutated": false,
  "manifest_mutated": false,
  "gate_rerun_performed": false,
  "successor_authorized": false,

  "v002_manifest_sha256_before":
    "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485",
  "v002_manifest_sha256_after":
    "016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485",
  "v002_acquisition_log_sha256_before":
    "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314",
  "v002_acquisition_log_sha256_after":
    "52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314",
  "phase_4bl_d_gate_report_sha256_before":
    "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7",
  "phase_4bl_d_gate_report_sha256_after":
    "d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7",

  "created_at_utc":      "<RFC3339 timestamp>",
  "created_at_unix_ms":  "<unix milliseconds>",
  "base_commit_sha":     "<main SHA at branch creation>",
  "code_commit_sha":     "<branch tip SHA at execution time>",

  "non_authorizations": {
    "phase_4bl_d_r_authorized":       false,
    "phase_4bl_e_authorized":         false,
    "phase_4bm_authorized":           false,
    "phase_4bn_authorized":           false,
    "phase_4bo_authorized":           false,
    "phase_4bp_authorized":           false,
    "phase_4bq_authorized":           false,
    "phase_5_authorized":             false,
    "phase_4_canonical_authorized":   false,
    "successor_state_recording_authorized": false,
    "manifest_research_eligible_flip_authorized": false,
    "manifest_eligibility_gate_status_transition_authorized": false,
    "chronological_split_policy_change_authorized": false,
    "normalization_authorized":       false,
    "feature_computation_authorized": false,
    "label_computation_authorized":   false,
    "diagnostics_authorized":         false,
    "ml_training_authorized":         false,
    "strategy_implementation_authorized": false,
    "signal_computation_authorized":  false,
    "backtest_execution_authorized":  false,
    "acquisition_authorized":         false,
    "public_endpoint_call_in_code_authorized": false,
    "binance_api_authorized":         false,
    "authenticated_api_authorized":   false,
    "private_endpoint_authorized":    false,
    "websocket_authorized":           false,
    "user_stream_authorized":         false,
    "credentials_authorized":         false,
    "env_file_authorized":            false,
    "mcp_json_authorized":            false,
    "mcp_authorized":                 false,
    "graphify_authorized":            false,
    "paper_shadow_authorized":        false,
    "live_readiness_authorized":      false,
    "deployment_authorized":          false,
    "exchange_write_authorized":      false,
    "phase_4bb_f_amendment_authorized": false,
    "phase_4bl_d_gate_amendment_authorized": false
  }
}
```

The report must be written atomically (write-then-rename via
`os.replace`) and accompanied by a paired SHA256 sidecar in
canonical Phase 4bb-F format. Both files are gitignored under
`.gitignore:85: data/microstructure/`.

## 9. Future gate rerun requirements

If Phase 4bl-D-S2 is separately authorized and executes
successfully, a future separately authorized **Phase 4bl-D-R
multi-day raw gate rerun phase** would be the natural conditional
follow-on. Phase 4bl-D-R must satisfy:

- **Verification of predecessor lifecycle.** Phase 4bl-D-R must
  verify that Phase 4bl-D-S2 is project-complete on `main`
  (merge-closeout recorded; SHA-chain integrity preserved).
- **Verification of artefact state.** Phase 4bl-D-R must verify:
  - the 2025-01-15 sidecar is exactly 99 bytes;
  - the 2025-01-15 sidecar ends with LF;
  - the 2025-01-15 sidecar's embedded SHA equals the raw zip SHA
    bit-for-bit;
  - the 2025-01-15 raw zip's SHA256 is unchanged
    (`f560c2e5…`);
  - the v002 manifest's SHA256 is unchanged;
  - the v002 acquisition log's SHA256 is unchanged;
  - the Phase 4bl-D gate report's SHA256 is unchanged (it
    remains as descriptive evidence of the pre-canonicalization
    state).
- **Gate execution.** Phase 4bl-D-R must run the Phase 4bl-D
  gate script (or an equivalent that follows the same 33-check
  protocol) against the unchanged v002 manifest and the
  canonicalized sidecar set. The gate must produce a new gate
  report under the canonical
  `data/microstructure/gate-reports/raw/` namespace with a
  distinct filename (different `unix_ms` and / or `phase_id`).
- **Expected outcome.** A future Phase 4bl-D-R is **likely to
  PASS** (32 of 33 checks already passed in Phase 4bl-D; the
  four failed checks all cascade from one root cause that B1
  removes). However, **PASS must not be assumed**. Phase 4bl-D-R
  must record the gate result exactly as produced, including any
  newly discovered issue.
- **No manifest mutation.** Phase 4bl-D-R must not mutate the
  v002 manifest. The gate-report-level
  `eligibility_gate_status_after` recommendation remains
  report-level only.
- **No successor authorization.** Phase 4bl-D-R must not
  authorize Phase 4bl-E. A separately authorized Phase 4bl-E
  successor-state recording phase is required for that, and is
  appropriate only after Phase 4bl-D-R produces PASS.
- **Boundary preservation.** Phase 4bl-D-R must preserve every
  retained verdict, every project lock, the M0 twelve-clause
  gate, the post-null cooldown rule, the cooled-down families
  list, the Phase 4al refined no-rescue rule, the Phase 4aw
  `flip_research_eligible(...)` always-raises invariant, and the
  Phase 4bb-F canonical path policy verbatim.

The full conditional chain is therefore:

```
Phase 4bl-D-S1 (this memo; B1 recommended)
  → Phase 4bl-D-S1 merge phase (operator-authorized)
  → Phase 4bl-D-S2 (operator-authorized; sidecar canonicalization)
  → Phase 4bl-D-S2 merge phase (operator-authorized)
  → Phase 4bl-D-R (operator-authorized; gate rerun; likely PASS)
  → Phase 4bl-D-R merge phase (operator-authorized)
  → Phase 4bl-E (operator-authorized; raw successor-state recording)
```

Each step in the chain requires a separate operator
authorization. No step authorizes the next.

## 10. Why B2 is weaker than B1

B2 amends the Phase 4bb-F canonical sidecar contract to
grandfather the Phase 4az CRLF sidecar. The reasons B2 is weaker
than B1:

- **B2 preserves the old sidecar bytes** (no metadata mutation),
  but at the cost of **amending a general governance contract**
  to accommodate one fixture. The Phase 4bb-F policy is otherwise
  cleanly enforced across all 89 Phase 4bl-C sidecars, the v002
  manifest sidecar, the v002 acquisition-log sidecar, the Phase
  4bb-D gate-report sidecar, the Phase 4bd derived-manifest
  sidecar, every feature / label / gate / successor-state sidecar
  in the project, and every prior Phase 4az / 4bb / 4bd / 4be /
  4bf / 4bg / 4bh / 4bi / 4bj / 4bl artefact sidecar.
- **B2 introduces dual canonical formats.** After the amendment,
  the canonical sidecar contract becomes "either CRLF or LF, with
  a grandfathering rule that may or may not apply to a given
  sidecar." This is harder to audit, harder to enforce, and harder
  to explain in future governance memos.
- **B2 risks inconsistent sidecar expectations.** Future raw /
  derived / feature / label gates would inherit either the
  grandfathering rule (in which case CRLF sidecars created
  anywhere could pass) or a refinement of it (in which case each
  gate would need to consult the policy's grandfathering carve-
  out), introducing case-by-case complexity.
- **B2 may create future ambiguity** if other pre-existing
  fixtures are discovered with similar metadata-format
  deviations. The grandfathering rule would then need to be
  generalized, narrowed, or revisited.
- **B2 weakens the strict fail-closed contract.** A
  grandfathering carve-out is fundamentally a fail-open exception
  to a fail-closed rule. Each carve-out makes the rule less
  strict in aggregate.
- **B2 does not produce a stronger audit trail than B1.** Both
  options can be documented transparently; B1's documentation is
  bounded to one execution phase, while B2's documentation
  amends the project's general governance.

## 11. Why B3 is weaker than B1

B3 amends the Phase 4bl-D gate (and any future raw / derived /
feature / label gate's sidecar parser) to accept CRLF as
canonical-equivalent to LF. The reasons B3 is weaker than B1:

- **B3 preserves the old sidecar bytes** (no metadata mutation),
  but at the cost of **weakening the strict gate**. A gate that
  accepts two terminators is not strict on line terminator.
- **B3 causes future gate ambiguity.** Future raw / derived /
  feature / label gates would inherit the relaxed parser. New
  pre-existing fixtures with CRLF sidecars (or other metadata-
  format deviations) would pass silently rather than being
  surfaced.
- **B3 makes the gate less aligned with Phase 4bb-F canonical
  path policy.** Phase 4bb-F documents the canonical sidecar
  format as `<sha>  <basename>\n` (two spaces, trailing LF).
  Under B3, the gate would accept `<sha>  <basename>\r\n` as
  equivalent, creating a gap between the documented policy and
  the actual gate behaviour. Operators or implementers
  consulting Phase 4bb-F would not learn from the policy alone
  that CRLF is accepted by the gate.
- **B3 sets a generalizing precedent.** Once the gate accepts
  CRLF, it becomes harder to reject any future relaxation
  request ("accept BOM-prefixed sidecars", "accept trailing
  whitespace", "accept multi-line sidecars", etc.). Each
  relaxation chips away at the strict fail-closed contract.
- **B3 does not resolve the underlying metadata-format
  deviation.** The sidecar remains non-canonical; the gate just
  stops emitting FAIL on it.

## 12. Why Phase 4bl-E is blocked

Phase 4bl-E is the **Multi-Day Raw Manifest Successor-State
Recording** phase. It would record a sibling successor-state
JSON for the v002 raw manifest with
`successor_admissibility_status =
"admissible_in_principle_policy_level_only"`, mirroring the
Phase 4bb-G precedent for the Phase 4az raw family.

Phase 4bl-E is **blocked** for the following reasons:

- **Phase 4bb-G precedent requires a PASS gate.** Phase 4bb-G
  was preceded by Phase 4bb-D, which produced a PASS gate report
  with 45 / 45 PASS. The successor-state recorded by Phase 4bb-G
  cites the Phase 4bb-D PASS report as its gate-evidence
  reference. The parallel for the v002 raw family is: Phase
  4bl-D would produce a PASS gate report, then Phase 4bl-E would
  record a successor-state citing that PASS report. **Phase
  4bl-D produced FAIL**, so the Phase 4bb-G precedent does not
  apply.
- **Gate-pass-first discipline is binding.** The project's
  established raw / derived / feature / label successor-state
  recording lifecycle requires a PASS gate at the corresponding
  layer before a successor-state can be recorded. This pattern
  is preserved in every prior successor-state phase:
  - Phase 4bg-B (derived-family successor-state) cites Phase
    4bf 55 / 55 PASS.
  - Phase 4bi-D (feature-family successor-state) cites Phase
    4bi-B 70 / 70 PASS.
  - Phase 4bj-G (label-family successor-state) cites Phase
    4bj-E 72 / 72 PASS.
  - Phase 4bb-G (raw-family successor-state for the Phase 4az
    `__v001` family) cites Phase 4bb-D 45 / 45 PASS.

  Recording a Phase 4bl-E successor-state without a preceding
  PASS gate at the v002 multi-day raw layer would break this
  precedent.
- **Operator-discipline integrity.** The Phase 4bl-D gate
  surfaced one specific issue; the appropriate operator response
  is to address the issue (B1) and rerun the gate (Phase 4bl-D-R),
  not to override the gate verdict by recording a successor-state
  anyway. Overriding would establish a precedent that
  successor-state recording can bypass gate verdicts, which
  weakens fail-closed discipline.

Phase 4bl-E therefore **remains unauthorized** until Phase 4bl-D-R
produces a PASS gate. Phase 4bl-D-S1 does not authorize Phase
4bl-D-R or Phase 4bl-E; both require separate operator
authorization at the appropriate lifecycle moment.

## 13. Non-authorizations

Phase 4bl-D-S1 explicitly does **NOT** authorize:

- Phase 4bl-D-S2 (sidecar canonicalization execution);
- sidecar rewrite;
- sidecar normalization (CRLF → LF mutation);
- Phase 4bb-F canonical path policy amendment;
- Phase 4bl-D gate amendment;
- Phase 4bl-D gate rerun (Phase 4bl-D-R);
- Phase 4bl-E (multi-day raw successor-state recording);
- successor-state recording for any other family;
- normalization (derived-family generation);
- derived parquet creation or mutation;
- feature generation (feature parquet creation or mutation);
- label generation (label parquet creation or mutation);
- diagnostics (label or other);
- label statistics computation;
- ML training, model selection, feature ranking, meta-labeling;
- strategy implementation;
- signal computation;
- backtest execution;
- additional data acquisition;
- additional downloads (aggTrades / 5m / 1m / tick / mark-price
  30m / 4h / order-book / spot / cross-venue / funding /
  open-interest);
- public endpoint calls in code;
- Binance API usage (authenticated or unauthenticated);
- authenticated APIs;
- private endpoints;
- WebSockets;
- user streams;
- credential read or creation;
- `.env` read or creation;
- `.mcp.json` read or creation;
- MCP usage;
- Graphify usage;
- paper / shadow operation;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- manifest mutation (any field, any manifest);
- `research_eligible` flip (any manifest);
- `eligibility_gate_status` transition (any manifest);
- `chronological_split_policy` mutation (any manifest);
- `data/microstructure/` artefact mutation;
- `data/microstructure/` artefact migration / rename / copy /
  delete;
- creation of any local artefact under `data/microstructure/`;
- creation of any new gate report;
- creation of any new successor-state artefact;
- creation of any canonicalization report;
- modification of any prior source code, test, script, config,
  governance memo, manifest, sidecar, gate report, or
  successor-state artefact (beyond the narrow
  `current-project-state.md` paragraph addition required by the
  process standard);
- Phase 5;
- Phase 4 canonical.

This memo is **docs-only** and changes nothing under
`data/microstructure/`, `src/`, `tests/`, or `scripts/`. Its only
tracked changes are the three new / modified files listed in §1.

## 14. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m thread** — OPERATIONALLY CLOSED (Phase 3t).
- **V2** — HARD REJECT — terminal for V2 first-spec
  (Phase 4l).
- **G1** — HARD REJECT — terminal for G1 first-spec
  (Phase 4r).
- **C1** — HARD REJECT — terminal for C1 first-spec
  (Phase 4x).

All preserved verbatim. No retained verdict is revised by
Phase 4bl-D-S1.

## 15. Preserved locks

- **§11.6** — HIGH cost = 8 bps slippage per side; round-trip
  = 16 bps.
- **§1.7.3** — 0.25% risk per trade; 2× leverage cap;
  one-position max; mark-price stops.
- **M0** — Phase 4ak twelve-clause mechanism-admissibility gate
  remains binding.
- **Phase 4ak post-null cooldown rule** — remains binding.
- **Phase 4ak cooled-down families list** — remains binding.
- **Phase 4ak future M0 memo template** — remains binding.
- **Phase 4al refined no-rescue rule** — remains binding (with
  §13 boundary specification and §14 hierarchy).
- **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant** — remains binding (not invoked by
  Phase 4bl-D-S1).
- **Phase 3v §8 stop-trigger-domain governance** — remains
  binding.
- **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance** — remains binding.
- **Phase 3p §4.7 strict integrity gate** — remains binding
  (multi-day extension applied verbatim by Phase 4bl-D).
- **Phase 3r §8 mark-price gap governance** — remains binding.
- **Phase 4j §11 metrics OI-subset partial-eligibility rule** —
  remains binding.
- **Phase 4k V2 backtest-plan methodology** — remains binding.
- **Phase 4p G1 strategy-spec memo** — remains binding.
- **Phase 4q G1 backtest-plan methodology** — remains binding.
- **Phase 4v C1 strategy-spec memo** — remains binding.
- **Phase 4w C1 backtest-plan methodology** — remains binding.
- **Phase 4bb-F canonical path policy** — remains binding.
  Phase 4bl-D-S1 does **not** amend Phase 4bb-F. The Phase 4az
  2025-01-15 sidecar CRLF deviation is recorded by Phase 4bl-D
  as a finding under the existing Phase 4bb-F policy and is
  recommended for remediation by Option B1 (sidecar
  canonicalization) rather than by Phase 4bb-F amendment.

All prior phase results are preserved verbatim. Phase 4bl-D-S1
does not amend, soften, narrow, or expand any prior governance
contract.

## 16. Current-project-state update

A narrow update to `docs/00-meta/current-project-state.md` is the
only governance-document modification required by Phase 4bl-D-S1
under the process standard. The update inserts:

- a new Phase 4bl-D-S1 narrative paragraph immediately before the
  existing Phase 4bl-D narrative paragraph;
- a new "Current phase:" Phase 4bl-D-S1 block replacing the prior
  top "Current phase:" Phase 4bl-D block;
- the prior Phase 4bl-D "Current phase:" block preserved as
  historical context immediately below the new block, per the
  documented standard.

The update preserves:

- Phase 4bl-D-S1 is **docs-only**;
- it records the recommended governance response to the Phase
  4bl-D `RAW_MULTIDAY_GATE_FAIL`;
- it recommends **Option B1** only as a future separately
  authorized execution path;
- it performs **no** sidecar rewrite;
- it performs **no** gate rerun;
- it authorizes **no** Phase 4bl-D-S2;
- it authorizes **no** Phase 4bl-D-R;
- it authorizes **no** Phase 4bl-E;
- recommended state remains **paused** unless the operator
  separately authorizes Phase 4bl-D-S2 controlled sidecar
  canonicalization execution.

The update does not modify any other governance document, any
specialist memo, the M0 mechanism-admissibility durable
governance file, the phase-workflow standard, the merge-closeout
standard, the operator-report standard, the chat-branching
handoff standard, the phase-prompt template, the phase-gates
roadmap, the technical-debt register, or any prior phase
implementation report / closeout / merge-closeout.

## 17. Validation

This is a docs-only phase. Required validation:

- `git diff --check` — clean.
- `git status` — only the three tracked Phase 4bl-D-S1 docs are
  staged for commit; pre-existing untracked entries
  (`.claude/scheduled_tasks.lock`, `data/research/`) remain
  untouched; no `data/microstructure/` artefact is staged or
  modified.

Whole-repo `ruff` / `mypy` / `pytest` were **not** rerun by Phase
4bl-D-S1. Phase 4bl-D-S1 modifies no source code, no test, and
no script. The latest authoritative whole-repo validation
remains the Phase 4bb-F-implementation merge baseline (`ruff
check .` PASS, `mypy` strict 120 source files PASS, `pytest
tests/research/microstructure/` 915 passed + 1 pre-existing
labelled skip, whole-repo `pytest` 1698 passed + 1 skipped + 2
pre-existing simulation failures).

## 18. Summary

Phase 4bl-D-S1 records the recommended governance response to the
Phase 4bl-D `RAW_MULTIDAY_GATE_FAIL` caused by one pre-existing
Phase 4az sidecar using Windows CRLF instead of canonical Phase
4bb-F LF. Seven options were evaluated (A remain paused; B1
normalize the sidecar; B2 amend Phase 4bb-F; B3 amend the gate;
C proceed to Phase 4bl-E despite the FAIL; D rerun without
remediation; E manual override). **Option B1 is recommended** as
the cleanest practical path: it is a metadata canonicalization
that preserves the raw zip byte-identically, preserves the
embedded SHA value byte-identically, preserves the Phase 4bb-F
canonical sidecar contract verbatim, preserves the strict
fail-closed gate verbatim, and produces a likely future PASS
without amending governance. B1 must be executed only in a
separately authorized Phase 4bl-D-S2 controlled sidecar
canonicalization execution phase that satisfies the pre/post
verification, mutation specification, output-artefact, and
non-authorization requirements recorded in §§7-8 of this memo.
A separately authorized Phase 4bl-D-R gate rerun is then
required to confirm PASS (likely but not guaranteed) before any
Phase 4bl-E successor-state recording can be authorized.

Phase 4bl-D-S1 is docs-only. It changes no source code, tests,
scripts, data, manifests, sidecars, gate reports, successor-state
artefacts, or runtime artefacts. It authorizes no successor
phase. All retained verdicts and project locks are preserved
verbatim. Recommended state remains **paused**.

---

**End of Phase 4bl-D-S1 — Sidecar Canonicalization Governance
Memo.**
