# Phase 4bn-BC — Merge Closeout

## 1. Phase identity

Phase 4bn-BC — CF-1 Valid-Pass Filter-Admissibility and Consequence Assessment. A
**docs-only decision and governance assessment** phase. **Tier 1 / Full Phase**
per `docs/00-meta/process/phase-risk-tiering-standard.md` — it decides the
downstream consequence of the project's only positive scientific result.

**This merge is a recordkeeping action only.** It records a decision, an audit,
and a closeout on `main`. It changes no data, no manifest, no eligibility state,
no reserve, and no lock, and it authorizes no successor phase.

`Merging Phase 4bn-BC records the rejection of the CF-1 filter continuation and its governance basis; it authorizes no successor phase.`

## 2. SHAs

| Item | SHA |
|---|---|
| Pre-merge `main` == `origin/main` (Phase 4bn-BB merge-closeout SHA-finalization tip) | `7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49` |
| Phase 4bn-BC decision commit (three documents added) | `bcf3685722187757eaceab2d609a8df01e34b8fa` |
| Phase 4bn-BC M0 mapping correction commit | `6816cf5e8dcf88a05f44be60b15e4a4f961ff7f6` |
| Phase 4bn-BC merge-closeout branch commit (this file) | `<MERGE_CLOSEOUT_COMMIT_SHA>` |
| Phase 4bn-BC no-fast-forward merge commit | `<MERGE_COMMIT_SHA>` |

**SHA-finalization convention.** This merge-closeout is created on the BC source
branch with the last two SHAs as placeholders. After the `--no-ff` merge into
`main`, one narrow SHA-finalization commit on `main`
(`docs(phase-4bn-bc): finalize merge closeout shas`) replaces them with the
actual values. A commit cannot embed its own SHA; the finalization commit's own
SHA equals the resulting final `main` / `origin/main` tip and is recorded in the
final operator report and the Git log after commit.

**Recording the correction commit here is deliberate.** Phase 4bn-BC's closeout
§19 deferred `6816cf5e…` to "the final operator report", which is a chat
artefact rather than a repository record — and this project has already lost one
authorizing prompt to a deleted chat. Lineage SHAs belong in Git.

## 3. Merge method

`git merge --no-ff` from
`phase-4bn-bc/cf1-valid-pass-filter-admissibility-consequence-assessment` into
`main`. Not squashed, not rebased, not amended. Source-branch history preserved
exactly: three commits (decision, correction, this merge-closeout).

## 4. Files brought forward by the merge

Four added files, all under `docs/00-meta/implementation-reports/`:

- `2026-07-31_phase-4bn-bc_cf1-valid-pass-filter-admissibility-and-consequence-assessment.md`
- `2026-07-31_phase-4bn-bc_cf1-m0-evidence-budget-and-anti-rescue-audit.md`
- `2026-07-31_phase-4bn-bc_closeout.md`
- `2026-07-31_phase-4bn-bc_merge-closeout.md` (this file)

## 5. Diff summary

Relative to pre-merge `main` `7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49`, the
change set is **additions only**. Verified before merge:

```text
git diff --name-status 7bb6819a..6816cf5e   ->  3 entries, all A
git diff --stat        7bb6819a..6816cf5e   ->  3 files changed, 1508 insertions(+)
git diff --check       7bb6819a..6816cf5e   ->  clean
```

No `M`, `D`, or `R` on any pre-existing path. No whitespace error. No
`data/microstructure/` or `data/research/` file modified or committed. No source,
test, script, config, manifest, ledger, process standard, phase gate, or
technical-debt entry created or changed. `docs/00-meta/current-project-state.md`
left unchanged, matching the docs-only precedent from Phase 4bn-AH onward.

The M0 correction commit `6816cf5e…` modified exactly two files (the audit and
the closeout); the main decision memo is **byte-identical** to `bcf3685…`.

## 6. Verdict

Scientific outcome of the predecessor is unchanged and preserved:

```text
CF1_VALID_PASS
```

Phase 4bn-BC decisions:

```text
Decision A:  REJECT_CF1_FILTER_CONTINUATION__REMAIN_PAUSED
Decision B:  R3 — NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED
```

Exact merged result state:

```text
CF1_VALID_PASS_PRESERVED__FILTER_CONTINUATION_REJECTED__NO_SUCCESSOR_AUTHORIZED__RESERVES_UNTOUCHED__REMAIN_PAUSED
```

The rejection rests on **decision consequence and anti-duplication**. It does
**not** rest on an M0 clause failure — see §17.

## 7. Local gitignored outputs

None produced by this phase. Phase 4bn-BC opened nothing under
`data/microstructure/` or `data/research/`, inspected neither the Phase 4bn-BB
v002 nor the Phase 4bn-AZ v001 artefact root, and generated no artefact. The
Phase 4bn-BB artefact root remains local and gitignored, untouched by this merge.

## 8. Validation results

Phase 4bn-BC was docs-only; `pytest`, Ruff, and mypy were correctly **not run**
and were outside its authorized scope. Their absence is not a regression.

Pre-existing failures elsewhere in the repository, unchanged and unrelated to
this arc: two in `tests/simulation/test_backtest_real_2026_03.py`
(`KeyError: 'trade_count'` at `src/prometheus/research/data/storage.py:232`,
reading kline Parquet) and twelve `mypy --strict` errors. Neither touches CF-1,
microstructure, or aggTrades code.

Structural validation performed for this merge: base-to-tip diff shape, whitespace
check, branch/upstream equality, and main-memo byte-identity after the correction
commit. All pass (§5).

## 9. Upstream immutability evidence

`main` and `origin/main` were confirmed equal at
`7bb6819ad5f1d5aded1746bf3332ad6f4aa5dc49` before any mutation, and were not
advanced by any other actor during the phase. The BC branch was confirmed equal
between local and `origin` at `6816cf5e…`. No published history was rewritten,
rebased, amended, or force-pushed.

## 10. Manifest state preservation

Unchanged and not touched by this merge:

```text
research_eligible          = false
eligibility_gate_status    = pending
all authorization flags    = false
test_rows_loaded           = 0
```

The Phase 4aw always-raising `flip_research_eligible(...)` behaviour is preserved
and was not invoked. No manifest, gate, sidecar, or split policy was mutated.

## 11. Boundary confirmations

- No data opened, listed for content, sampled, hashed, or scored.
- No evidence reserve opened or spent; the evidence-budget ledger is unchanged,
  with no row added, edited, or deleted and no transition-history entry.
- No metric recomputed. Every scientific value in the phase is transcribed from
  the committed Phase 4bn-BB reports, verified verbatim during review.
- No model fitted, no target or feature generated, no runner invoked in any mode.
- No row-level prediction inspected.
- No network, API, endpoint, credential, `.env`, WebSocket, MCP, Graphify, or
  `.mcp.json` use.
- No external reviewer used **during** the phase. An independent compliance
  review was performed **at merge time** — see §17.

## 12. Retained verdict ledger

Preserved verbatim:

```text
H0          — FRAMEWORK ANCHOR
R3          — BASELINE-OF-RECORD
R1a         — RETAINED — NON-LEADING
R1b-narrow  — RETAINED — NON-LEADING
R2          — FAILED — §11.6
F1          — HARD REJECT
D1-A        — MECHANISM PASS / FRAMEWORK FAIL — other
5m thread   — OPERATIONALLY CLOSED (per Phase 3t)
V2          — HARD REJECT — terminal for V2 first-spec
G1          — HARD REJECT — terminal for G1 first-spec
C1          — HARD REJECT — terminal for C1 first-spec
```

Research-arc verdicts, unchanged:

```text
CF1_INVALID_RUN   (Phase 4bn-AZ)  — consumed, no rerun
CF1_VALID_PASS    (Phase 4bn-BB)  — consumed, no rerun
```

Note on identifier collision: **strategy `R3`** (baseline-of-record) and
**reserve posture `R3`** (`NO_CF1_RESERVE_PATH_JUSTIFIED__REMAIN_RESERVED`) are
unrelated. Never cross-reference them.

## 13. Preserved project locks

Preserved exactly and unchanged: `STOP_LONGHORIZON_ML_ARC`;
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`;
`REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
`STRUCTURALLY_NON_IDENTIFIABLE__PROHIBITED_FOR_FUTURE_EXECUTION`;
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`;
`V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
`V002_SEALED_TEST = UNTOUCHED_RESERVED`;
`HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`; `test_rows_loaded = 0`;
`research_eligible = false`; `eligibility_gate_status = pending`; all
authorization flags false; the Phase 4aw always-raising
`flip_research_eligible(...)`; Phase 4bn-AE §19; the Phase 4ak twelve-clause M0
gate with its §6 post-null cooldown rule and §7 cooled-down-family list; M0 §7.D
at `NOT_RECOMMENDED_NOW`; the locked 8 bps/side · 16 bps round trip; the Phase
4bn-BB no-rerun boundary; every prior verdict; every dataset identity and hash;
all split, holdout, sidecar, and storage policies; the evidence-ledger statuses;
and the spending-authority rules.

Also preserved, though not named in the phase's own lock inventories (inherited
omission from Phase 4bn-BB closeout §12, covered there under "all
split/holdout/sidecar/storage policies"): `UNUSED_NON_RESERVE_BUFFER`
(2024-11-01 .. 2024-11-15, Phase 4bn-AY §20). Nothing in this arc weakens it.

**No stopped arc is softened, merged, reinterpreted, reopened, or rescued.**

## 14. No-rescue constraints

Phase 4bn-BC closes the CF-1 filter continuation and, per Phase 4bn-AY §30, does
**not** authorize neighbouring variants. No alternative filter family, feature
set, horizon, loss, model, or state object is proposed as a substitute. The
rejection forfeits a possible favourable outcome and authorizes nothing in its
place — the opposite shape from the rescue behaviour M0.10 and the scarce-reserve
standard §19 exist to prevent.

`CF1_VALID_PASS` is preserved in full and is not narrowed, downgraded, or
reinterpreted by the rejection.

## 15. Successor authorization

**No successor phase is authorized by this merge.**

`Phase 4bn-BD — CF-1 Bounded Non-Directional Volatility-Regime Filter Preregistration` is **not proposed and not authorized**; it exists in the record only as the title of the continuation Phase 4bn-BC declines.

No reserve-spend proposal and no sealed-test proposal is created or authorized.
Any future CF-1-adjacent object would require a new mechanism justification, a
new docs-only phase, an explicit anti-duplication audit, separate operator
authorization, and its own M0 clearance.

## 16. Recommended state

**Remain paused.**

The CF-1 lane is closed, both prior arcs are stopped, and no genuinely new
mechanism source has been identified. `Remaining paused is a valid operator choice.`

---

## 17. Independent compliance review at merge time

The phase's own authorizing prompt was lost with a deleted chat, so the review
could not compare the phase against the prompt as issued. This is recorded as a
known weakening of the review, not glossed.

The review was performed by an **instance independent of the phase's execution
agent**, per `OPERATING_CONVENTIONS` practice that an agent does not review its
own phase. Its non-circular anchors were the add-only three-file diff (which
bounds physical scope absolutely) and Phases 4bn-AX §14/§17/§27/§28 and 4bn-AY
§29/§30/§31 (which bound the predeclared consequence independently of anything
Phase 4bn-BC wrote). Both cleared.

**Verdict:** `COMPLIANT_WITH_NOTES__RECOMMEND_MERGE`.

Six findings are recorded here as required merge content. **None touches a lock,
a reserve, a metric, or a claim.**

### F1 — the M0 correction narrowed an over-determined rejection (principal)

Before commit `6816cf5e…`, the continuation faced four independent adverse
grounds: M0.2, M0.12, anti-duplication, and decision consequence. After it, two
remain, and both are judgment-based rather than clause-based.

The corrected clause readings are textually right (§17 F3 below), and the
decisions did not move. But the **prospective** effect is a real reduction in the
standing barrier, and the phase does not name it.

**Binding consequence:** a future author must **not** cite "M0.2: PASS,
M0.8: PASS, M0.12: PASS" as partial pre-clearance of a CF-1 state object. Those
results describe individual clause mappings of an object that was **rejected**.
The assessed continuation does **not** clear the twelve-clause M0 gate either —
M0.5 is undischarged and M0.3/M0.7 are hollow in substance.

### F2 — the audit does not state that the assessed object also fails to clear M0

The audit correctly hedges "M0-permissible in form", but with three bolded
`PASS` labels a skim-reader may infer near-clearance. §17 F1 above supplies the
missing sentence explicitly.

### F3 — memo §25 is inaccurate as written

§25 states "No admissible filter envelope, mapping, threshold, regime count,
comparator, or consequence rule is defined here." True of mapping, threshold,
regime count, comparator, and consequence rule. **Not true of "envelope"** — §10
defines the object and §11 supplies nine admissibility criteria, seven of which
are declared satisfiable. The record therefore closes the lane while retaining a
partially specified scaffold. Read §25 as scoped to the parameters, not the
envelope.

### F4 — memo §13's decisive appeal is untraceable

§13 concludes "Per the governing standard that a failure to answer these cleanly
weighs against continuation, this is decisive." No owner is cited, and the rule
does not appear anywhere in committed governance (verified by search).

**Origin, recorded here because it is otherwise unrecoverable:** the instruction
came from the operator's authorizing prompt, which stated that a failure to
answer the decision-consequence questions cleanly "must weigh against Option A."
It was therefore legitimate when written — but the prompt is lost, so the
sentence is now unverifiable from the repository. The substance is independently
recoverable from Phase 4bn-AX §28, which makes decision consequence the decisive
criterion.

### F5 — source/test inspection claimed but not inventoried

Memo §3/§4 authorize reading committed source and tests; §5 and closeout §6 list
none. The audit nonetheless relies on a source-level fact (the feature schema
forbidding the `liquidation` token — confirmed at
`src/prometheus/research/microstructure/features_schema.py`). Phase 4bn-AX §7 set
the better precedent by inventorying source files explicitly. Traceability
defect only; the underlying fact is true.

### F6 — the correction commit SHA was recorded nowhere in the repository

Closeout §19 deferred `6816cf5e…` to the final operator report, a chat artefact.
Given this phase's own prompt was lost that way, deferring a lineage SHA to a
non-repository record is the precise failure mode the project's SHA discipline
exists to prevent. **Resolved by §2 of this merge-closeout.**

### Verified accurate during review

Every transcribed scientific value was checked line-by-line against Phase 4bn-BB:
all seven `D_i`, both equal-weighted QLIKE values, `Δ_equal`, `ρ`, `LB_95`, seed
`20260715`, 10,000 replicates, `PCG64`, origin counts 5,854 / 5,516 / 338
(`har_unavailable` 336, `har_coverage_failure` 2), ranks 4/4 and 6/6, condition
numbers `3.983e2`–`6.494e2`, and the `> 1e10` guard. **All verbatim.** No
unsupported claim is softened; no materiality threshold is adopted; the claim
table correctly separates `NOT_SUPPORTED` from `NOT_ESTABLISHED` from
`NOT_CLEARED` from `PROHIBITED_CONSUMED`.

### Corrective phase

None required. F2–F5 are presentation and traceability defects in a completed
record; correcting them in place would amend a phase after its review. They are
recorded here instead, which is what a merge-closeout is for. A future docs-only
corrective phase could address them if the operator wishes; **it is not
authorized by this merge.**
