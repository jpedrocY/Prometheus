# Evidence-Budget Ledger

**Standing status index for the project's scarce predictive-evidence reserves.**

Owner phase: Phase 4bn-AV — Evidence-Budget Ledger, Scarce-Reserve Spending
Authority, and Late-Inadmissibility Consequence Protocol (docs-only).
Created 2026-07-14. Base SHA `90c7765ba68a9b14416b79bba6f78376d94da225`.

---

## 1. Purpose and authority

This ledger is the single standing inventory of the project's scarce, irreplaceable
predictive-evidence reserves and their current status. It exists so that any future
phase can answer, **without opening any underlying evidence**, three questions:

1. Which evidence reserves still exist, and what is each reserve's status?
2. Which evidence has already been consumed, and therefore cannot be re-used as
   independent confirmation?
3. Which candidate source is currently inadmissible or unavailable for a specific
   historical question?

This ledger is a **status index only**. It does not replace, restate, or override:

- the split / holdout / sealed-test structure owned by Phase 4bn-Y and the committed
  split-policy source (`pre_v002_split_policy.py`, `diagnostics_split_policy_v002.py`);
- the source-admissibility criteria owned by Phase 4bn-AB and the Phase 4bn-AT
  top-of-book decision;
- the manifest / eligibility locks enforced in committed source
  (`manifest.py`: `research_eligible = False`, `flip_research_eligible(...)`
  always-raises).

Where this ledger and a specialist document appear to conflict, the specialist
document wins in its own domain and the ledger entry is treated as **ambiguous and
fail-closed** until a docs-only reconciliation phase resolves it (§4).

The binding rules for *who may authorize spending a reserve*, *how*, and *what happens
if a source is later found inadmissible* live in the companion standard,
[`scarce-reserve-spending-and-late-inadmissibility-standard.md`](scarce-reserve-spending-and-late-inadmissibility-standard.md).
This ledger records status; that standard governs change of status. **Neither document
authorizes any evidence spend.**

## 2. Status vocabulary

A ledger entry's `status` field is exactly one of the following finite values. No other
value is admissible. Ambiguity is not a fifth silent state — it is `UNKNOWN_OR_AMBIGUOUS`
and it fails closed.

| Status | Meaning |
|---|---|
| `UNTOUCHED_RESERVED` | A scarce reserve whose content has never been read, loaded, inspected, enumerated for content, scored, sampled, or consumed. May become spendable only after the companion standard's pre-spend sequence is fully satisfied. |
| `CONSUMED` | Evidence that has been scored / evaluated / relied upon. May be described with correct provenance, but **may never be represented as independent confirmation** and **may never return to `UNTOUCHED_RESERVED`**. |
| `INADMISSIBLE_OR_UNAVAILABLE` | A candidate source that cannot currently answer the named question because it is inadmissible, unavailable, or not regime-comparable. This is **not a reserve that can be "spent"**; it is a recorded negative source status for a specific question. |
| `RETIRED` | A reserve or source that is permanently withdrawn from all future decision use by an explicit committed decision (for example, disproved provenance, or a decision to never use it). Distinct from `CONSUMED` (which was used) and from `INADMISSIBLE_OR_UNAVAILABLE` (which may become admissible for a different question via a new admissibility decision). |
| `UNKNOWN_OR_AMBIGUOUS` | Status cannot be established from committed evidence, or two committed sources disagree. **Fails closed** (§2.1). |

### 2.1 `UNKNOWN_OR_AMBIGUOUS` fails closed

When an entry is `UNKNOWN_OR_AMBIGUOUS`:

- it **cannot** support a claim of independence or independent confirmation;
- it **cannot** be spent;
- it **cannot** support any promotion, eligibility change, or verdict;
- it requires operator review and a docs-only reconciliation before its status may
  change to any other value.

No phase may treat an `UNKNOWN_OR_AMBIGUOUS` reserve as if it were
`UNTOUCHED_RESERVED`.

The five statuses above are the complete vocabulary. Additional statuses may be added
only by a future docs-only phase that proves from committed evidence that a genuinely
distinct status is necessary; the default is to reuse these five.

## 3. Update rules

1. **Same-branch update.** Every phase that proposes to spend a reserve, or that
   completes a spend, must update this ledger in the same branch as the spend proposal
   or the spend, or in the immediate closeout of that phase. There is no separate
   "ledger maintenance" phase for a spend that already happened.
2. **No silent transition.** No status may change without an explicit, committed
   citation to the phase / report / commit that authorizes the change. A status change
   with no citation is invalid and fails closed.
3. **Consumed is terminal.** No entry may transition from `CONSUMED` back to
   `UNTOUCHED_RESERVED` (or to any status implying renewed independence). Consumption
   is irreversible.
4. **No independence claim under ambiguity.** No evidence may be described as
   independent, unseen, sealed, or independent confirmation while its ledger status is
   `UNKNOWN_OR_AMBIGUOUS`, or while it is `CONSUMED`.
5. **Citations required.** Every status change must cite committed evidence (a phase
   report, closeout, merge-closeout, or committed source constant). Chat history,
   handoffs, and advisory reviews are not sufficient citations for a status change.
6. **Derived from committed evidence only.** Every value in this ledger is derived from
   committed repository reports and committed source constants. No underlying evidence
   reserve was opened to create or update this ledger (§9, §10).

## 4. Conflict / fail-closed rule

If two committed sources disagree about a reserve's status, or if a status cannot be
established from committed evidence, the entry is set to `UNKNOWN_OR_AMBIGUOUS` and:

- the conflict is recorded in the transition-history section (§7);
- the reserve is treated as unspendable and non-independent until resolved;
- resolution requires a **docs-only reconciliation phase** with explicit operator
  authorization; it may not be resolved inside a spend-execution phase.

Ledger conflicts always fail closed. When in doubt, a reserve is treated as more
protected, not less.

## 5. Current reserve table

All values below are carried forward verbatim from committed reports and committed
source constants (Phase 4bn-Y split/holdout policy; Phase 4bn-AR baseline verdict;
Phase 4bn-AS stop decision; Phase 4bn-AU direction memo; committed split-policy
source). **No underlying evidence was opened to populate this table.**

### 5.1 Pre-v002 predictive holdout (internal dry-run holdout)

| Field | Value |
|---|---|
| `evidence_id` | `PRE_V002_INTERNAL_HOLDOUT` |
| Name | Pre-v002 internal dry-run holdout |
| Family / split / category | `microstructure_labels_aggtrades_v001 @ v002`, pre-v002 backward segment; BTCUSDT / Binance USDⓈ-M futures / aggTrades; internal-holdout split |
| Scope (from committed metadata) | 2024-11-17 .. 2024-11-30 inclusive UTC; 14 dates; the last split of the 275-date `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` pre-v002 partition (Phase 4bn-Y §11) |
| Status | **`CONSUMED`** |
| Independence | Not independent. Scored under the Phase 4bn-AR fixed long-horizon baseline run; the arc was stopped at Phase 4bn-AS (`STOP_LONGHORIZON_ML_ARC`) |
| Permitted use | Descriptive decomposition only, with correct "consumed" provenance, and only if a future admissible decomposition is separately authorized |
| Prohibited use | Any use as independent confirmation, unseen evidence, sealed evidence, or reusable confirmation; any use to rescue or reopen the stopped long-horizon ML arc |
| Authority to change status | Not applicable — `CONSUMED` is terminal; cannot return to `UNTOUCHED_RESERVED` |
| Last authoritative phase/report | Phase 4bn-AR verdict; Phase 4bn-AS stop decision; restated in Phase 4bn-AU §5 |
| Last status-change date | 2026-07-12 (consumed at Phase 4bn-AR) |
| Notes / caveats | Explicitly **not** a substitute for the sealed test (Phase 4bn-Y §15). Must never be described as untouched or sealed. |

### 5.2 v002 terminal window

| Field | Value |
|---|---|
| `evidence_id` | `V002_TERMINAL_WINDOW` |
| Name | v002 terminal window |
| Family / split / category | Published v002 terminal envelope; BTCUSDT / Binance USDⓈ-M futures; raw / normalized / feature / label |
| Scope (from committed metadata) | 2024-12-01 .. 2025-02-28 inclusive UTC; 90 dates; 155,153,449 rows (Phase 4bn-Y §7). Governed by the recorded `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy. Carried forward **by reference only** |
| Status | **`UNTOUCHED_RESERVED`** |
| Independence | Genuinely unseen; independence intact |
| Permitted use | None now. Consideration is permitted only after the companion standard's full pre-spend sequence for a terminal reserve is satisfied (§10.B of the standard) |
| Prohibited use | Any read, load, inspection, enumeration for content, scoring, sampling, or consumption in the absence of an authorized spend; any tuning after viewing |
| Authority to change status | Human operator only, via the companion standard's pre-spend sequence and quorum |
| Last authoritative phase/report | Phase 4bn-Y §7/§14; restated in Phase 4bn-AU §5 |
| Last status-change date | Never changed (reserved since defined) |
| Notes / caveats | The non-sealed sub-window (2024-12-01 .. 2025-02-13) and the sealed sub-window (2025-02-14 .. 2025-02-28) are governed distinctly; the sealed sub-window is the separate `V002_SEALED_TEST` entry below |

### 5.3 v002 sealed test

| Field | Value |
|---|---|
| `evidence_id` | `V002_SEALED_TEST` |
| Name | v002 sealed test (final single-use holdout) |
| Family / split / category | Published v002 terminal envelope, TEST split; BTCUSDT / Binance USDⓈ-M futures |
| Scope (from committed metadata) | 2025-02-14 .. 2025-02-28 inclusive UTC; 15 dates; `test_rows_loaded = 0` (Phase 4bn-Y §7/§15; committed split-policy source) |
| Status | **`UNTOUCHED_RESERVED`** (highest protection level) |
| Independence | Genuinely unseen; highest-value independence; single-use |
| Permitted use | None now. Consideration is permitted only after terminal evidence supports promotion under existing gates, and only under the **strictest** form of the companion standard's pre-spend sequence (§10.C of the standard). Proposal and authorization must occur in **separate phases** |
| Prohibited use | The seven prohibited uses recorded in the v002 policy — `feature_selection`, `model_selection`, `hyperparameter_selection`, `threshold_tuning`, `strategy_design`, `diagnostic_iteration`, `eligibility_rescue` (Phase 4bn-Y §7); plus any exploration, debugging, calibration, or rescue; plus any second sealed test (spending it creates no replacement) |
| Authority to change status | Human operator only, under the strictest pre-spend sequence and quorum |
| Last authoritative phase/report | Phase 4bn-Y §7/§15; restated in Phase 4bn-AU §5 |
| Last status-change date | Never changed (sealed since defined) |
| Notes / caveats | `test_rows_loaded = 0` posture is code-enforced and must be preserved. This is the project's only remaining single-use final holdout |

## 6. Inadmissible / unavailable-source registry

This section records candidate **sources** (not reserves) whose current status for a
specific historical question is `INADMISSIBLE_OR_UNAVAILABLE`. These are not reserves
that can be "spent"; they are recorded negative source statuses. A source may become
admissible for a **different** question only via a new, separately authorized docs-only
admissibility decision — never by silent substitution.

### 6.1 Historical retrospective top-of-book (bookTicker) source

| Field | Value |
|---|---|
| `evidence_id` | `HIST_TOB_BOOKTICKER_SOURCE` |
| Name | Historical retrospective top-of-book / bookTicker source for the 2024 aggTrades mechanism question |
| Question it was required to answer | Whether the clean 15s last-trade result was genuine midpoint movement or bid–ask bounce (a model-free measurement-validity question), over the 2024-10-02 .. 2024-11-30 window |
| Status | **`INADMISSIBLE_OR_UNAVAILABLE`** for that historical mechanism question |
| Basis (from committed metadata) | Phase 4bn-AT: no currently-admissible retrospective source can answer it (the futures um daily bookTicker archive is Tier-1-undocumented, carries an unremediated out-of-order defect, reportedly ceased updating in 2024, and its coverage of the required window is unconfirmed from Tier-1 index metadata); prospective capture is regime-non-comparable to the 2024 aggTrades and cannot answer the specific historical question |
| Consequence | Phase 4bn-AT decision `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`. Not reopened |
| Important non-implication | **Prospective top-of-book collection does not retroactively answer the historical question.** Acquiring prospective data would not change this entry's status for the 2024 question |
| Last authoritative phase/report | Phase 4bn-AT; restated in Phase 4bn-AU §3 |
| Notes / caveats | This is a source status, not a reserve. It is not "spendable". It must not be silently replaced by a substitute source; a new source requires a new docs-only admissibility decision |

## 7. Transition history

This section is the append-only record of status changes. Every future status change
must add a dated, cited row here. No row may be edited or deleted; corrections are made
by appending a new row that supersedes the prior one, with a citation.

| Date | Entry | From → To | Authorizing committed evidence |
|---|---|---|---|
| 2026-07-12 | `PRE_V002_INTERNAL_HOLDOUT` | `UNTOUCHED_RESERVED` → `CONSUMED` | Phase 4bn-AR fixed long-horizon baseline run verdict (scored the internal holdout); Phase 4bn-AS `STOP_LONGHORIZON_ML_ARC` |
| 2026-07-14 | `HIST_TOB_BOOKTICKER_SOURCE` | (new) → `INADMISSIBLE_OR_UNAVAILABLE` | Phase 4bn-AT `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` |
| 2026-07-14 | Ledger established | — | Phase 4bn-AV (this ledger); reserves recorded from committed metadata without opening any evidence |

`V002_TERMINAL_WINDOW` and `V002_SEALED_TEST` have **no** transition rows because their
status has never changed: both have been `UNTOUCHED_RESERVED` since defined.

## 8. Required fields for future entries

Every future ledger entry (reserve or source) must record at least:

- `evidence_id` (stable, uppercase, unique);
- human-readable name;
- evidence family / split / source category;
- exact scope expressed from committed metadata (never from opening data);
- current status (from the §2 vocabulary);
- independence status;
- permitted use;
- prohibited use;
- authority required to change status;
- last authoritative phase / report;
- last status-change date;
- notes / caveats.

A new entry with any of these fields missing or unciteable from committed evidence is
recorded as `UNKNOWN_OR_AMBIGUOUS` until completed.

## 9. Evidence-source statement

Every status and scope value in this ledger is **derived from committed repository
evidence only** — committed implementation reports, closeouts, merge-closeouts, and
committed source constants. No value is inferred, estimated, or reconstructed from
opening any evidence reserve, and no row count, date, hash, or content was invented.

## 10. No-open statement

**No underlying evidence reserve was opened to create this ledger.** The pre-v002
internal holdout, the v002 terminal window, and the v002 sealed test were not read,
loaded, inspected, enumerated for content, scored, sampled, or consumed by Phase 4bn-AV.
Nothing under `data/microstructure/` or `data/research/` was opened. The
`test_rows_loaded = 0` posture is preserved.

---

**This ledger authorizes no evidence spend.** It records status only. Change of status,
and the authority to spend any reserve, are governed by
[`scarce-reserve-spending-and-late-inadmissibility-standard.md`](scarce-reserve-spending-and-late-inadmissibility-standard.md),
which itself authorizes no spend.
