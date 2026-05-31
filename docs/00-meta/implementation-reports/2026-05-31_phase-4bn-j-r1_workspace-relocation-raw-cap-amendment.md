# Phase 4bn-J-R1 — Workspace Relocation + Raw-Only Acquisition Cap Amendment

**Phase 4bn-J-R1 is branch-complete only by this work; not merged into
main; not project-complete.** It is a docs-only / governance-only /
amendment-only phase. It is **Tier 1 — Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3, because it
amends the acquisition execution contract adjacent to public historical
data acquisition, local disk / runtime caps, data / microstructure
artefact generation, future eligibility gates, and future ML-baseline
admissibility — while explicitly authorizing no acquisition and no
downstream use.

This amendment **acquires no data, calls no endpoint, writes no
acquisition code, runs no acquisition, creates no manifest, creates no
sidecar except normal tracked Git docs files, creates no
data/microstructure or data/research artefact, runs no ML, runs no
diagnostics, runs no backtests, migrates no storage, creates no
database, compacts no Parquet, creates no v003, and authorizes no
successor.** It records a workspace relocation, intakes a stop report as
tracked documentation, and amends one numeric disk cap as raw-only —
nothing more.

---

## 1. Purpose

Phase 4bn-J (the acquisition-only BTCUSDT aggTrades 12-month phase) was
authorized after Phase 4bn-I but **stopped before acquisition** at the
disk-footprint preflight, on operator request, and produced an untracked
stop report rather than either acquiring under an amended cap or writing
the full Tier-1 fail-closed doc set. Separately, the operator has
relocated the active local repository and the lightweight Claude Code
workspace from the `C:` drive to the `D:` drive.

This phase exists to record those two facts cleanly and to make exactly
one narrow, evidence-based amendment to the merged Phase 4bn-I
acquisition execution contract. Specifically, this memo:

1. records the local workspace relocation from `C:\Prometheus` to
   `D:\Prometheus`;
2. records the Claude Code lightweight-workspace relocation from
   `C:\ClaudeRuns\prometheus-light` to `D:\ClaudeRuns\prometheus-light`;
3. records that future prompts and command conventions must use
   `D:\Prometheus`;
4. records that Phase 4bn-J stopped before acquisition;
5. preserves the Phase 4bn-J stop report as a **tracked stop report, not
   a closeout**;
6. amends the Phase 4bn-I 5 GiB hard / 3 GiB warning disk cap **for the
   acquisition retry only**;
7. re-scopes the amended cap as **raw-only**, set from the stop-report
   evidence;
8. confirms that **all other** Phase 4bn-I boundaries remain intact;
9. records that a revised acquisition-only retry **may be recommended
   but is not authorized by this amendment**.

This memo does not solve the ML problem, does not claim more data will
produce edge, does not move any artefact toward eligibility, and does
not authorize any executable successor. It is a governance amendment
plus a workspace-of-record update.

---

## 2. Authority and repository state

**Authority.** This memo is authorized as a docs-only Tier 1 amendment
phase. It is an **amendment**, not an in-place correction to prior
finalized reports. It does not modify, rewrite, or re-finalize any prior
Phase 4bn-I file, any Phase 4bn-I merge-closeout, or any earlier merged
report. The Phase 4bn-I contract remains on `main` as recorded; this
memo records a forward-looking amendment to one of its numeric caps,
scoped to the acquisition retry only.

**Repository state verified at branch creation:**

- Active machine: Desktop.
- Active local repository path: **`D:\Prometheus`** (relocated; see §3).
- Pre-branch `main == origin/main == HEAD` verified equal at:
  `27dbc5723f3f068c34663ec57cd85a0e6b42f501`
  — `docs(phase-4bn-i): finalize merge closeout shas`.
- Predecessor chain confirmed present on `main`: `5aed510`
  (4bn-I merge-closeout), `4733d90` (4bn-I merge), `a513c4f` (4bn-I
  branch), `654befd` (4bn-H finalize).
- Branch created: **`phase-4bn-j-r1/workspace-relocation-raw-cap-amendment`**
  from `main` at the SHA above.
- Expected untracked transient present and not committed:
  `.claude/scheduled_tasks.lock`.
- The Phase 4bn-J stop report
  (`docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j_acquisition-stop-report.md`)
  was present untracked at branch creation and is preserved and tracked
  by this phase (see §4).
- GitHub remote `origin` verified intact:
  `https://github.com/jpedrocY/Prometheus.git` (fetch and push). The
  remote did **not** require re-pointing; the remote configuration is
  repository-local (`.git/config`) and was carried with the copied repo.

**README caveat.** `README.md` may be stale and is **not** treated as
current-state authority. The authoritative current state is
`docs/00-meta/current-project-state.md` plus the merged
implementation-report chain.

---

## 3. Workspace relocation record

The operator has moved the working roots from the `C:` drive to the `D:`
drive. This memo records the new active convention.

**Active local repository path.**

- Active local repo path is now **`D:\Prometheus`**.
- Previous local repo path **`C:\Prometheus`** is **no longer the active
  repo path**.

**Active Claude Code lightweight workspace path.**

- Active Claude Code lightweight workspace is now
  **`D:\ClaudeRuns\prometheus-light`**.
- Previous Claude Code workspace **`C:\ClaudeRuns\prometheus-light`** is
  **no longer the active workspace path**.

**New Claude Code launch convention.**

```powershell
cd D:\ClaudeRuns\prometheus-light

$env:CLAUDE_CODE_DISABLE_CLAUDE_MDS="1"
$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY="1"

claude --add-dir D:\Prometheus
```

**New command convention.**

For every shell command, use:

```text
cd D:\Prometheus <command>
```

On Windows PowerShell 5.1 (where `&&` may not be available), the
equivalent manual forms are `cd D:\Prometheus <command>` or
`cd D:\Prometheus; <command>`.

**Remote.** The GitHub remote does **not** need to be "re-pointed". The
remote configuration is repository-local and was preserved by the copy;
`origin` still points to `https://github.com/jpedrocY/Prometheus.git`.

**Forward rule.** Future prompts must use `D:\Prometheus` unless
explicitly amended later. The old `C:` folders, if retained, are
**backups only** and are **not active project roots**.

**Relationship to the lightweight-workspace process standard.** The
process document
`docs/00-meta/process/claude-code-lightweight-workspace-standard.md`
(Phase 4bm-D-P1) still records the **principle** of launching heavy
sessions from a lightweight workspace and reaching the real repo
explicitly, but it still uses the **old `C:` example paths** in §4, §5,
§6, §10, and §16. That standard's own §15 change-control requires that
it be updated only by a phase that **names that file in its allowed
tracked files**. This amendment phase does **not** name that file in its
allowed tracked files, so — fail-closed — this phase does **not** edit
that standard. Instead, the active path convention is recorded here and
in `current-project-state.md`, and §16 of this memo **recommends a
separate, §15-compliant docs-only process-doc update phase** to refresh
the path strings in the lightweight-workspace standard. Until that
separate phase runs, the path strings in that standard are superseded by
this memo and by `current-project-state.md` for the active convention;
the standard's *principle* (launch light, reach the repo explicitly,
suppress heavy auto-context) is unchanged and remains binding.

---

## 4. Phase 4bn-J stop-report intake

The Phase 4bn-J stop report
(`docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j_acquisition-stop-report.md`)
is intaken and **preserved as tracked documentation** by this amendment
phase. It is a **stop report, not a closeout**. It is **not** treated as
a Phase 4bn-J closeout, **not** treated as branch-complete for Phase
4bn-J, and **not** treated as project-complete for Phase 4bn-J.

The stop report records, and this memo carries forward verbatim, that
in the stopped Phase 4bn-J attempt:

- Phase 4bn-J **stopped before acquisition**.
- Phase 4bn-J is **not branch-complete**.
- Phase 4bn-J is **not merged**.
- Phase 4bn-J is **not committed** (the stopped attempt created no
  commit on its branch).
- Phase 4bn-J is **not project-complete**.
- **No archive was downloaded.**
- **No data was acquired.**
- **No data/microstructure artefact was created.**
- **No data/research artefact was created.**
- **No manifest was created.**
- **No sidecar was created.**
- **No acquisition code was written.**
- **No existing script was modified.**
- **No `current-project-state.md` update was made** by the stopped
  Phase 4bn-J attempt.
- **No commit was made** by the stopped Phase 4bn-J attempt.
- The stop report is **now preserved as tracked documentation by this
  amendment phase** (Phase 4bn-J-R1), which is the first phase to commit
  it.

The only read-only / metadata-only work the stopped attempt performed
was: verifying repo state and SHAs; reading committed reports, the
committed acquisition tooling, and committed footprint evidence; and a
**HEAD-only Content-Length metadata probe** of 7 pre-v002 dates (no
archive bodies downloaded, nothing written to disk, no v002 / sealed
data touched). That probe is the evidence base for §6–§7.

---

## 5. Phase 4bn-I contract carried forward

Phase 4bn-I (merged at `27dbc57`) is the **Docs-Only Acquisition
Execution Plan**. It pre-declared the exact acquisition envelope, the
exact source-endpoint policy confirmation requirement, the exact
canonical path layout, the exact disk-footprint cap (5 GiB hard / 3 GiB
warning), the exact derivation-time / runtime cap (4 hours hard / 2
hours warning), the exact manifest and sidecar policy, the exact
sealed-test preservation language, the exact new-holdout policy, the
exact 25 fail-closed stop conditions, the exact acquisition-phase
non-authorization envelope, and the exact post-acquisition successor
chain. It authorized nothing executable.

**This amendment changes exactly one element of that contract** — the
disk-footprint cap, re-scoped as raw-only with new thresholds, **for the
acquisition retry only** (§7). **Every other element of the Phase 4bn-I
contract is carried forward intact**: the acquisition envelope (§9), the
source-policy result (§10), the sealed-test boundary (§11), the storage
posture (§12), the runtime cap (§8), and the non-authorizations (§13).
Phase 4bn-I's own files are not modified; this memo is the amending
artefact.

---

## 6. Disk-cap defect and root-cause finding

The Phase 4bn-I disk-footprint cap is **too strict, and scope-confused**,
for the acquisition retry. The stop-report evidence establishes this:

- Phase 4bn-I recorded a **5 GiB hard / 3 GiB warning** disk cap, and its
  §15 justified the 5 GiB figure as "≈ 4× the 90-day v002 raw +
  normalized + feature + label footprint."
- The acquisition retry is, by repo convention, a **raw-only** phase
  (Phase 4bl-C-style acquisition-only; normalization, features, and
  labels are separate, separately gated phases). The relevant footprint
  is therefore **raw zips only**.
- The stop-report preflight estimated the **275 new pre-v002 raw days**
  (2024-03-01 .. 2024-11-30) at approximately **5.5–7.5 GiB raw-only**
  (central estimate ≈ 5.53 GiB at the v002 contiguous-quarter average of
  ≈ 20.6 MiB/day; conservative / event-aware estimate ≈ 7.45 GiB from a
  deliberately event-weighted HEAD sample).
- **Therefore the 5 GiB hard cap is too strict even for raw-only
  acquisition**: both ends of the raw-only estimate exceed it, and the
  cap is breached before the 275-day range completes even on the
  optimistic average.
- The 5 GiB cap also **mixed raw-only acquisition footprint with
  derived-stack footprint.** Committed evidence shows v002 **raw** alone
  (90 d) ≈ 1.81 GiB, but v002 **normalized** alone (90 d) ≈ 20.6 GiB and
  v002 **label** parquet ≈ 14–21 GiB for 60–90 days — so the true 90-day
  raw + normalized + feature + label stack is already tens of GiB, and
  "4× of it" would be ~80–120+ GiB, not 5 GiB. The 5 GiB figure is only
  even near-plausible for a **raw-only** scope, and even raw-only for 12
  months exceeds it.
- The **derived stack should have a separate future cap**, because
  normalized / feature / label outputs may be tens or hundreds of GiB
  and must not silently inherit a raw-only number.
- The operator has moved the repo to **`D:\Prometheus`** with
  approximately **1.25 TB free on `D:`**, so **`C:` disk pressure is no
  longer the binding local storage constraint**.

**Finding.** Disk remains governed, but the cap must be (a) **scope-
correct** — naming raw-only as the thing it bounds — and (b) **realistic**
— set from the real per-day evidence with headroom. The 5 GiB hard /
3 GiB warning cap, as written and as scoped, is the only binding issue
the stopped attempt found; source policy passed (§10).

---

## 7. Amended raw-only disk cap

For the **Phase 4bn-J acquisition-only retry only**, the raw-only
acquisition disk cap is amended to:

- **Warning threshold: 10 GiB** additional local raw acquisition
  footprint.
- **Hard cap: 25 GiB** additional local raw acquisition footprint.

This amendment applies **only** to raw-only acquisition artefacts for:

- **BTCUSDT**;
- **Binance USDⓈ-M futures**;
- **aggTrades**;
- the **2024-03-01 through 2024-11-30 new pre-v002 segment** (275 days,
  inclusive, UTC);
- under the existing **12-month envelope 2024-03-01 through 2025-02-28**.

The amended cap is **raw-only** and is set from the stop-report evidence
(§6): comfortably above the ~5.5–7.5 GiB raw-only estimate, with
headroom for the 2024 event days, and trivial against the ~1.25 TB free
on `D:`.

**This amendment does NOT authorize, and CANNOT be construed as
authorizing:**

- derived normalized / feature / label cap expansion;
- normalization;
- feature derivation;
- label derivation;
- ML;
- diagnostics;
- strategy;
- storage migration;
- database creation;
- Parquet compaction;
- v003;
- **acquisition itself** (the cap amendment is not an acquisition
  authorization; a separate operator authorization is still required —
  see §15–§16).

**Derived-stack planning note (warning only, not a decision).** Future
normalized / feature / label phases need a **separate derived-stack disk
budget** set **before** execution. As a planning range recorded as a
**warning only**, not a decision: a full ML-ready 12-month stack may
plausibly require **~150–250 GiB**; comfortable working headroom should
be higher, e.g. **~300 GiB**. The exact derived-stack cap **must be set
in the future derivation / gate phase, not here.** This memo sets no
derived-stack cap.

---

## 8. Preserved runtime cap

The Phase 4bn-I **runtime cap is unchanged**:

- **Warning threshold: 2 hours** total wall-clock.
- **Hard cap: 4 hours** total wall-clock.

The stop report indicates the runtime cap remains plausible for a 275-day
raw-only acquisition (275 days × 2 HTTP round-trips with conservative
pacing, ~5.5–7.5 GiB total transfer plus per-day decompress / inventory;
the 90-day v002 normalization orchestrator alone ran ~24 minutes, and
raw acquisition is lighter per day). Runtime must still be measured
per-day and cap-enforced during any future run. With disk de-fanged,
runtime and integrity become the binding execution gates.

---

## 9. Preserved acquisition envelope

The future retry, **if separately authorized**, must preserve the Phase
4bn-I envelope exactly:

- **Symbol:** BTCUSDT only.
- **Market:** Binance USDⓈ-M futures.
- **Data family:** aggTrades only.
- **New acquisition segment:** 2024-03-01 through 2024-11-30 inclusive
  UTC only (275 days).
- **Existing v002 terminal window:** 2024-12-01 through 2025-02-28 — not
  re-downloaded and not overwritten.
- **Existing v002 sealed test split:** 2025-02-14 through 2025-02-28 —
  untouched (see §11).
- **No** post-v002 dates.
- **No** ETHUSDT.
- **No** extra horizons.
- **No** mark-price.
- **No** spot.
- **No** cross-venue.
- **No** order book.
- **No** tick data.
- **No** v003.

---

## 10. Preserved source-policy result

The source-policy result from the stopped Phase 4bn-J attempt is carried
forward:

- The **source-policy preflight PASSED** in the stopped attempt.
- The committed `docs/04-data/historical-data-spec.md` **gap is real**:
  it documents the official Binance USDⓈ-M REST endpoints (klines,
  mark-price, funding, exchange-info, leverage, commission) but does
  **not** fully document aggTrades bulk historical archives,
  `data.binance.vision`, archive naming, or archive checksum policy.
- **Existing committed tooling resolves the source policy clearly enough
  for acquisition** (the same tooling that produced the existing v002
  raw window), establishing:
  - public unauthenticated Binance data archive;
  - host `data.binance.vision`;
  - BTCUSDT USDⓈ-M futures daily aggTrades zip archive pattern
    (`.../data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-{YYYY-MM-DD}.zip`);
  - `.CHECKSUM` companion (two-space `<sha256hex>  <filename>` format);
  - checksum-first download discipline (CHECKSUM → zip → SHA256 match →
    `testzip()` → bounded row-sample validation);
  - **no** credentials;
  - **no** private endpoint;
  - **no** authenticated API;
  - **no** WebSocket;
  - **no** user stream;
  - **no** `.env`;
  - **no** `.mcp.json`;
  - **no** MCP;
  - **no** Graphify.
- A future **source-policy documentation memo** to backfill
  `historical-data-spec.md` with the aggTrades-archive convention **may
  be useful hygiene** but is **not required** before retrying
  acquisition, unless new evidence contradicts the stop report.

---

## 11. Preserved sealed-test boundary

The existing v002 sealed test split **2025-02-14 through 2025-02-28
remains sealed**. For any future retry and for this memo:

- **Do not** read it.
- **Do not** count it.
- **Do not** sample it.
- **Do not** hash it.
- **Do not** summarize it.
- **Do not** inspect it.
- **Do not** use it for continuity checks.
- **Do not** use it for acquisition QA.
- **Do not** use it for normalization QA.
- **Do not** use it for feature QA.
- **Do not** use it for label QA.
- **Do not** use it for split policy.
- **Do not** use it for any reason.

Preserve Phase 4bn-B `test_rows_loaded: 0` and the
`iter_partitions(split="test", ...)` always-raise pattern. The 275-day
backward extension never touches the sealed split.

---

## 12. Preserved storage posture

The Phase 4bn-I storage posture is carried forward unchanged:

- **Parquet remains canonical.**
- **No DuckDB database cache.**
- **No `.duckdb` files.**
- **No SQLite research matrices.**
- **No `.sqlite` files.**
- DuckDB querying Parquet **in place** remains permitted **only** as a
  non-invasive query layer if separately needed.
- **No Parquet compaction.**
- **No storage migration.**
- **No dataset layout modification.**

---

## 13. Preserved non-authorizations

This amendment honors the reusable non-authorization blocks
`N-ACQUISITION`, `N-ENDPOINT`, `N-CREDENTIALS`, `N-MANIFEST`,
`N-GATE-RERUN`, `N-SUCCESSOR-STATE`, `N-DERIVATION`,
`N-DIAGNOSTICS-ML-STRATEGY`, `N-PHASE-5`, and `N-VERDICT-LOCK` from
`docs/00-meta/process/phase-risk-tiering-standard.md` §7, expanded here
for clarity. Phase 4bn-J-R1 does **not** and **cannot** be construed as
authorizing:

- any acquisition; any archive download; any endpoint call (public,
  Binance, authenticated, or private); any WebSocket or user stream;
- any credentials; any `.env`; any `.mcp.json`; any MCP; any Graphify;
- any acquisition code; any script modification (none was required to
  preserve the stop report as docs);
- any v003; any extra symbol; any extra horizon; any mark-price; any
  spot; any cross-venue; any order book; any tick data;
- any local parquet read; any local data/research read; any local
  data/microstructure read;
- any diagnostics; any ML training; any model scoring; any predictions;
  any feature ranking / selection / pruning / engineering; any
  hyperparameter tuning; any threshold tuning; any calibration fitting;
- any strategy research; any signal generation; any PnL simulation; any
  backtests; any test-holdout access;
- any manifest mutation; any successor-state mutation; any gate-report
  mutation;
- any data/research or data/microstructure artefact creation or commit;
- any storage migration; any database creation; any Parquet compaction;
- any paper / shadow; any live-readiness; any deployment; any
  exchange-write; any production keys;
- any Phase 4bn-J-R2 authorization; any Phase 5 authorization; any
  successor phase whatsoever.

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked). No retained
verdict is revised; no project lock is loosened; no M0 amendment is
made. All new manifests in any future retry must start
`research_eligible: false`, `eligibility_gate_status: "pending"`; this
memo creates no manifest and makes no eligibility transition.

---

## 14. Revised acquisition-retry requirements

A revised acquisition-only retry, **if separately authorized after this
branch is merged**, should:

- use **`D:\Prometheus`** as the active repo path;
- use a **new bounded 275-day raw-only acquisition script** if needed
  (the existing `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`
  is hardcoded to the 90-day v002 range and is a locked prior-phase
  artefact that must not be repointed);
- **reuse proven Phase 4bl-C patterns** verbatim (same host allowlist,
  same URL / path pattern, same CHECKSUM-first ordering, same SHA256 +
  `testzip()` + row-sample validation, same Phase 4bb-F sidecars, same
  refuse-overwrite, same non-eligible manifest seed, same per-day cap
  enforcement);
- **reject any date `>= 2024-12-01`**;
- **reject any date outside 2024-03-01 through 2024-11-30**;
- preserve **BTCUSDT-only** and **aggTrades-only** scope;
- enforce the **10 GiB warning / 25 GiB hard raw-only** disk cap (§7);
- enforce the **2 h warning / 4 h hard** runtime cap (§8);
- create **only raw acquisition artefacts** if repo convention keeps
  normalization / features / labels separate;
- produce **canonical Phase 4bb-F sidecars**
  (`<sha256>  <basename>\n`; two-space separator; LF; no BOM;
  refuse-overwrite);
- **refuse overwrite** of any existing artefact;
- keep manifests **non-eligible** (`research_eligible: false`,
  `eligibility_gate_status: "pending"`);
- **not create research outputs**;
- **not commit** data/microstructure or data/research;
- **recommend a raw archive eligibility gate only if acquisition
  succeeds**;
- **recommend remain paused or another corrective docs-only memo if
  acquisition fails closed again.**

This section is a requirements specification for a possible future
phase. It is **not** an authorization to run that phase.

---

## 15. Decision

**Decision:**
`RECOMMEND_AUTHORIZE_REVISED_ACQUISITION_ONLY_RETRY__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

**Reason.** The stopped Phase 4bn-J attempt found that **source policy
passed** and that the **only binding issue was an unrealistically low,
scope-confused disk cap**. The repository has now been moved to
`D:\Prometheus` with much larger free space (~1.25 TB on `D:`). The cap
can be amended as **raw-only** without changing any other acquisition
boundary. A revised acquisition-only retry, bounded exactly by §7–§14,
is therefore the cleanest non-paused option to recommend — **but it is
not authorized by this amendment.**

The candidate decision options for this phase were:

1. `RECORD_WORKSPACE_RELOCATION_AND_CAP_AMENDMENT__REMAIN_PAUSED`
2. `RECOMMEND_AUTHORIZE_REVISED_ACQUISITION_ONLY_RETRY__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
   ← **chosen**
3. `RECOMMEND_AUTHORIZE_SOURCE_POLICY_DOCUMENTATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
4. `RECOMMEND_AUTHORIZE_DOCS_ONLY_DERIVED_STACK_STORAGE_BUDGET_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
5. `RECOMMEND_CLOSE_ML_BASELINE_ARC__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`

**No successor is authorized from inside Phase 4bn-J-R1.** The
recommendation is a recommendation only; any executable follow-up
requires a separate operator authorization after this branch is merged.

---

## 16. Recommended state and successor options

**Recommended state: remain paused.** Phase 4bn-J-R1 is branch-complete
only by this work; not merged into main; not project-complete. Per
`phase-workflow-standard.md`, it is NOT project-complete until a
separately authorized merge phase records its merge-closeout on `main`
per `merge-closeout-standard.md` (Tier 1).

The operator may, as separate decisions after this branch is merged:

- **remain paused** (default);
- **request a merge prompt** for Phase 4bn-J-R1;
- separately authorize the **revised acquisition-only retry**
  (the chosen recommendation; bounded exactly by §7–§14);
- separately authorize a docs-only **source-policy documentation memo**
  (backfill `historical-data-spec.md` with the aggTrades-archive
  convention; hygiene, not required for acquisition);
- separately authorize a docs-only **derived-stack storage-budget memo**
  (set the separate normalized / feature / label disk budget before any
  derivation phase; §7 derived-stack planning note);
- separately authorize a docs-only **process-doc update phase** that
  names `docs/00-meta/process/claude-code-lightweight-workspace-standard.md`
  in its allowed tracked files and refreshes its `C:` path strings to
  the `D:` convention (per that standard's §15 change-control; see §3);
- **reject further ML-baseline successors and close the ML arc.**

**No acquisition / ML / diagnostics / strategy / PnL / backtest /
storage-migration / database-creation / Parquet-compaction / v003 /
paper / shadow / live / exchange-write option is valid from this state
unless separately authorized after this branch is merged.**

---

## 17. Current-project-state update summary

`docs/00-meta/current-project-state.md` is updated narrowly by this
phase: a new Phase 4bn-J-R1 prose paragraph is appended at the end of
the Current-Phase prose stack, and a new `Current phase:` block for
Phase 4bn-J-R1 is added at the top of the stacked `Current phase:`
code-block list. Prior Phase 4bn-A … 4bn-I paragraphs and prior
`Current phase:` blocks are preserved verbatim as labelled historical
context. The update records: the workspace relocation to `D:\Prometheus`
and `D:\ClaudeRuns\prometheus-light`; the new launch and command
conventions; the Phase 4bn-J stopped-before-acquisition state and the
preserved tracked stop report; the amended raw-only disk cap (10 GiB
warning / 25 GiB hard) for the acquisition retry only; the preserved
4 h / 2 h runtime cap; the preserved envelope, source-policy result,
sealed-test boundary, storage posture, and non-authorizations; the
decision
`RECOMMEND_AUTHORIZE_REVISED_ACQUISITION_ONLY_RETRY__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
and the recommended state **remain paused** with no successor
authorized.

No prior finalized Phase 4bn-I file is modified, no Phase 4bn-I history
is rewritten, and no Phase 4bn-I merge-closeout is edited. This phase is
an amendment, not an in-place correction to prior finalized reports.
