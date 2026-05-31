# Phase 4bn-I — Docs-Only Acquisition Execution Plan

**Phase 4bn-I is branch-complete only by this work; not merged into main;
not project-complete.** Phase 4bn-I is the docs-only / design-only /
scoping-only acquisition **execution plan** authorised by the operator
following the Phase 4bn-H recommendation
`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
Phase 4bn-I takes the Phase 4bn-H acquisition-readiness recommendation
one level lower of abstraction by pre-declaring the **exact** future
acquisition envelope (Option C — 12-month continuous BTCUSDT Binance
USDⓈ-M futures aggTrades history), the **exact** UTC calendar range, the
**exact** canonical path layout, the **exact** source-endpoint policy
confirmation requirement, the **exact** disk-footprint cap, the **exact**
derivation-time cap, the **exact** manifest and sidecar policy, the
**exact** sealed-test preservation language, the **exact** new-holdout
policy, the **exact** fail-closed stop conditions, the **exact**
non-authorization envelope for the future acquisition phase, and the
**exact** post-acquisition successor chain. The phase authorises nothing
executable.

## 0. Required exact phrases

- **Phase 4bn-I is a docs-only / design-only / scoping-only acquisition
  execution plan.**
- **Phase 4bn-I does not acquire data.**
- **Phase 4bn-I does not call public, Binance, authenticated, or private
  endpoints.**
- **Phase 4bn-I does not migrate storage.**
- **Phase 4bn-I does not create any database.**
- **Phase 4bn-I does not compact Parquet.**
- **Phase 4bn-I does not create v003.**
- **Phase 4bn-I does not authorize acquisition.**
- **Phase 4bn-I does not authorize any successor.**
- **Phase 4bn-I does not read local parquets.**
- **Phase 4bn-I does not inspect local data.**
- **Phase 4bn-I does not open any local gitignored `data/research/` or
  `data/microstructure/` artefact.**
- **Phase 4bn-I does not create or modify any manifest.**
- **Phase 4bn-I does not run diagnostics.**
- **Phase 4bn-I does not run ML.**
- **Phase 4bn-I does not train models.**
- **Phase 4bn-I does not score models.**
- **Phase 4bn-I does not generate predictions.**
- **Phase 4bn-I does not inspect the test holdout.**
- **Phase 4bn-I does not use the sealed test split.**
- **Phase 4bn-I does not rank features.**
- **Phase 4bn-I does not select features.**
- **Phase 4bn-I does not prune features.**
- **Phase 4bn-I does not engineer features.**
- **Phase 4bn-I does not tune hyperparameters.**
- **Phase 4bn-I does not tune thresholds.**
- **Phase 4bn-I does not fit calibrators.**
- **Phase 4bn-I does not run strategy research.**
- **Phase 4bn-I does not define a strategy.**
- **Phase 4bn-I does not generate trade signals.**
- **Phase 4bn-I does not simulate PnL.**
- **Phase 4bn-I does not run backtests.**
- **Phase 4bn-I does not modify dataset layout.**
- **Phase 4bn-I does not open any WebSocket or user stream.**
- **Phase 4bn-I does not use credentials, `.env`, `.mcp.json`, MCP, or
  Graphify.**
- **Phase 4bn-I does not mutate any manifest.**
- **Phase 4bn-I does not mutate any successor-state artefact.**
- **Phase 4bn-I does not commit `data/microstructure`.**
- **Phase 4bn-I does not commit `data/research`.**
- **Phase 4bn-I does not authorize Phase 4bn-J, Phase 5, paper / shadow,
  live-readiness, deployment, exchange-write, production keys, or any
  successor phase.**
- **The current v002 microstructure ML-baseline window is 90 calendar
  days.**
- **The split structure is 45 train days, 30 validation days, and 15
  sealed test days.**
- **The sealed test split remains sealed and is not inspected.**
- **Phase 4bn-B produced descriptive ML-baseline evidence only.**
- **Phase 4bn-C interpreted that evidence as small descriptive lift, not
  edge.**
- **Phase 4bn-D scoped bounded expansion options but authorized nothing.**
- **Phase 4bn-E partially ruled out gross train-vs-validation
  feature-distribution drift at the measurement-frame level only.**
- **Phase 4bn-F concluded the 90-day window is useful but not enough to
  prove broad sufficiency, insufficiency, representativeness, or outlier
  status.**
- **Phase 4bn-G defined a concrete data-expansion requirements framework
  and storage-scaling comparison.**
- **Phase 4bn-H recommended a docs-only acquisition execution plan for a
  12-month continuous BTCUSDT expansion at design level only.**
- **None of Phase 4bn-A through Phase 4bn-I establishes edge,
  profitability, tradability, strategy-readiness, signal-readiness,
  paper / shadow readiness, or live-readiness.**
- **Any actual acquisition requires a separate future operator
  authorization after this phase is merged.**
- **Any future acquisition phase must remain constrained to acquisition
  only and must not run ML, diagnostics, strategy, PnL, backtests,
  storage migration, database creation, or manifest eligibility
  transitions.**
- **Recommended state remains paused.**

---

## 1. Purpose

Phase 4bn-I answers a single governance / scoping question — the
**acquisition execution question**:

> Can the project safely execute a future acquisition-only phase for a
> 12-month continuous BTCUSDT Binance USDⓈ-M futures aggTrades history,
> preserving v002 feature/label semantics and the existing sealed v002
> test split, while keeping Parquet canonical and enforcing fail-closed
> disk, runtime, sidecar, manifest, holdout, and endpoint boundaries?

Phase 4bn-I is **docs-only / design-only / scoping-only**. It reads only
committed repository Markdown reports and committed architecture
documents as its evidence base. It opens no local gitignored
`data/research/` outputs. It opens no local gitignored
`data/microstructure/` datasets. It reads no local parquet, CSV, or JSON
output. It calls no endpoint. It uses no credentials. It mutates no
manifest, sidecar, gate report, or successor-state artefact. It trains
nothing, scores nothing, predicts nothing, evaluates nothing on test
data, selects nothing, ranks nothing, tunes nothing, runs nothing,
materialises no artefact, acquires no data, migrates no storage, creates
no database, compacts no Parquet, modifies no dataset layout, creates no
v003 dataset, and authorizes no successor implementation. **Phase 4bn-I
is the governance-level acquisition execution plan, not data
acquisition, not storage migration, and not v003 creation.**

This memo writes the **exact future acquisition execution plan** that
would be used if the operator later **separately** authorizes a real
acquisition-only phase. It is specific enough that a later acquisition
phase could be authorized safely, but it does not perform or authorize
that later acquisition. The plan deliberately pre-declares every value a
future acquisition phase would otherwise have to invent ad hoc — the
exact range, the exact paths, the exact caps, the exact stop
conditions — so that the future acquisition phase, if authorized,
inherits a fixed, fail-closed contract rather than discretionary scope.

## 2. Authority and repository state

- **Authorising instruction.** Operator authorization of Phase 4bn-I as
  a Tier 1 Full Phase docs-only acquisition execution plan, following
  and honouring the Phase 4bn-H recommendation
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Branch.** `phase-4bn-i/docs-only-acquisition-execution-plan`.
- **Base `main` SHA.** `654befd236884c8c47cc062722ac74c794272d12`
  (Phase 4bn-H SHA-finalization commit `docs(phase-4bn-h): finalize
  merge closeout shas`; pre-branch `main == origin/main` verified in
  sync).
- **Predecessor chain present on `main` at branch time.**
  - `654befd` — `docs(phase-4bn-h): finalize merge closeout shas`
    (Phase 4bn-H merge-closeout SHA finalization);
  - `55b011d` — `docs(phase-4bn-h): add merge closeout`;
  - `1aad93a` — `docs(phase-4bn-h): merge acquisition readiness scoping`
    (Phase 4bn-H merge commit);
  - `c1038f9` — `docs(phase-4bn-h): scope acquisition readiness`
    (Phase 4bn-H branch commit);
  - `1ab9ebe` — `docs(phase-4bn-g): finalize merge closeout shas`.
- **Risk tier.** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3, because this
  phase is adjacent to possible future data acquisition, longer-history
  microstructure planning, future local disk / runtime commitments,
  manifest / sidecar policy, possible future ML-baseline downstream
  admissibility, possible future holdout design, and possible future
  storage workload definition, while explicitly authorizing none of
  them.
- **Working-tree expectation.** Only the pre-existing untracked
  transient `.claude/scheduled_tasks.lock`, plus pre-existing gitignored
  `data/research/` and `data/microstructure/` namespaces that may exist
  locally and must remain uncommitted.

## 3. Phase type and strict scope

Phase 4bn-I is a **docs-only / design-only / scoping-only acquisition
execution plan**. It produces exactly three tracked artefacts (this
implementation report, a closeout, and a narrow
`current-project-state.md` update) and **no** executable change.

**This phase must not, and does not:**

- acquire data; call Binance or any public endpoint; call any
  authenticated or private endpoint; open any WebSocket or user stream;
- read local parquets; inspect local data; open any local gitignored
  `data/research/` or `data/microstructure/` artefact; hash or inspect
  any local data artefact;
- create a database; compact Parquet; create or modify any manifest or
  sidecar; migrate storage; modify dataset layout;
- authorize acquisition; authorize storage migration; authorize v003;
  authorize ML, models, tuning, diagnostics, strategy, signals, PnL, or
  backtests; authorize any successor phase;
- use credentials, `.env`, `.mcp.json`, MCP, or Graphify.

Phase 4bn-I is an **execution plan only**. It is specific enough that a
later acquisition phase could be authorized safely, but it must not
perform or authorize that later acquisition.

## 4. Evidence base and input boundary

**Inputs read (committed repository Markdown / architecture docs only):**

- `docs/00-meta/current-project-state.md`;
- `docs/00-meta/process/merge-closeout-standard.md`;
- `docs/00-meta/process/phase-risk-tiering-standard.md`;
- `docs/00-meta/process/phase-workflow-standard.md`;
- `docs/00-meta/process/phase-prompt-template.md`;
- `docs/00-meta/process/operator-report-standard.md`;
- the three Phase 4bn-H reports (merge-closeout, acquisition-readiness
  memo, closeout);
- the three Phase 4bn-G reports (merge-closeout,
  combined-data-expansion-storage-scaling-scoping, closeout);
- the three Phase 4bn-F reports (merge-closeout,
  v002-data-sufficiency-representativeness-scoping, closeout);
- the three Phase 4bn-E reports (merge-closeout,
  train-validation-feature-drift-diagnostics, closeout);
- the three Phase 4bn-D reports (merge-closeout,
  bounded-ml-baseline-expansion-scoping, closeout);
- the three Phase 4bn-C reports (merge-closeout,
  ml-baseline-evidence-interpretation-memo, closeout);
- the three Phase 4bn-B reports (merge-closeout,
  multi-day-v002-ml-baseline-implementation, closeout);
- the three Phase 4bn-A reports (merge-closeout,
  ml-baseline-implementation-scoping-design, closeout);
- `docs/04-data/data-requirements.md`;
- `docs/04-data/historical-data-spec.md`;
- `docs/04-data/timestamp-policy.md`;
- `docs/04-data/dataset-versioning.md`;
- `docs/08-architecture/database-design.md`.

**Inputs explicitly NOT used:** local gitignored
`data/research/microstructure/ml-baselines/phase-4bn-b/` outputs; local
gitignored `data/research/microstructure/ml-baselines/phase-4bn-e/`
outputs; local gitignored Phase 4bm-* artefacts; local
`data/microstructure/` raw / normalized / feature / label parquets; the
sealed v002 test split (`test_rows_loaded: 0`;
`iter_partitions(split="test", ...)` raises). README is treated as
**potentially stale** and is **not** used as current-state authority.

## 5. Phase 4bn-H decision carried forward

**Phase 4bn-H decision (verbatim):**
`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Phase 4bn-H was the docs-only acquisition-readiness memo. It selected
**Option B — longer single continuous BTCUSDT aggTrades history** as the
candidate expansion shape, compared calendar-coverage options A / B / C
/ D / E at design level only, and recommended **Option C (12-month
continuous BTCUSDT)** as the cleanest first-expansion calendar coverage
subject to separate operator authorization of a docs-only acquisition
execution plan. It preserved the Phase 4bn-G `A + F + C` storage posture
verbatim (Parquet canonical; defer migration; DuckDB querying Parquet in
place as the preferred non-invasive query layer; defer Storage B
compaction and Storage D DuckDB database cache; preserve SQLite for the
runtime role only). It defined 14 pre-acquisition gates extending Phase
4bn-G §13 and 13 stop conditions extending Phase 4bn-G §8.24. It
authorised nothing executable.

Phase 4bn-I **is** the docs-only acquisition execution plan that Phase
4bn-H recommended. It inherits the Phase 4bn-H recommendation boundary
verbatim, narrows the Option C envelope to **exact** values, and
likewise authorises nothing executable.

## 6. Phase 4bn-G / 4bn-F / 4bn-E / 4bn-D / 4bn-C / 4bn-B interpretation carried forward

- **Phase 4bn-G (verbatim):**
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  — defined the combined data-expansion requirements + storage-scaling
  scoping framework (24-requirement framework; seven candidate expansion
  shapes; six candidate storage architectures; 7 × 6 coupled decision
  matrix; 14 pre-acquisition gates; 10 pre-storage-migration gates; 13
  non-authorization constraints; recommended `A + F + C` storage path).
- **Phase 4bn-F (verbatim):**
  `RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  — concluded the 90-day window is useful but not enough to prove broad
  sufficiency, insufficiency, representativeness, or outlier status;
  treated "outlier" as an unresolved risk, not a conclusion.
- **Phase 4bn-E (verbatim):**
  `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED` — partially ruled
  out gross train-vs-validation feature-distribution drift at the
  measurement-frame level only (31 low / 13 moderate / 0 high / 1
  undefined drift classification; highest absolute standardized mean
  delta 0.330; highest missing-rate delta ≈ 6e-06; 13 moderate-drift
  features cluster on count and mean-quantity dimensions, signed
  consistently count-up / mean-quantity-down between train and
  validation).
- **Phase 4bn-D (verbatim):**
  `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  — scoped bounded expansion options but authorized nothing.
- **Phase 4bn-C (verbatim):**
  `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` —
  interpreted Phase 4bn-B evidence as small descriptive lift, not edge,
  with a severe high-confidence calibration tail and §11.6
  cost-commensurability fractions consistent with 80 – 95 % of
  validation rows being below the round-trip cost.
- **Phase 4bn-B (verbatim):** `RECORD_EVIDENCE_ONLY` — descriptive
  ML-baseline evidence on train / validation only; test holdout sealed
  (`test_rows_loaded: 0`); no model selected as best; no feature ranked
  or selected; no hyperparameter or threshold tuned; no strategy /
  signal / PnL / backtest.

Phase 4bn-I inherits all six decisions verbatim and softens none of
them.

## 7. Exact future acquisition question

The acquisition execution question is defined exactly as:

> **Can the project safely execute a future acquisition-only phase for a
> 12-month continuous BTCUSDT Binance USDⓈ-M futures aggTrades history,
> preserving v002 feature/label semantics and the existing sealed v002
> test split, while keeping Parquet canonical and enforcing fail-closed
> disk, runtime, sidecar, manifest, holdout, and endpoint boundaries?**

This is an **execution-safety** question, not an edge-search question.
It is **not** phrased as, and must never be read as, any of:

- "Will more data make ML work?";
- "Can we find edge with more data?";
- "Can we rescue the model?";
- "Can we tune until performance improves?";
- "Can we get a tradable signal?";
- "Can we go to paper / shadow / live after acquisition?".

The question asks only whether a bounded, fail-closed acquisition-only
phase can be **executed safely** against a fixed contract. It does not
ask, assume, or imply that the acquired data would establish edge,
sufficiency, or tradability.

## 8. Exact proposed acquisition envelope

The recommended future acquisition envelope (Phase 4bn-H Option C),
pre-declared at exact values:

- **Symbol:** BTCUSDT only.
- **Market:** Binance USDⓈ-M futures.
- **Data family:** aggTrades only.
- **Shape:** 12-month continuous history.
- **Date range:** 2024-03-01 through 2025-02-28 inclusive UTC (see §9).
- **Existing v002 envelope included as terminal 90-day portion:**
  2024-12-01 through 2025-02-28.
- **Existing v002 sealed test split preserved untouched:** 2025-02-14
  through 2025-02-28.
- **New acquisition adds only pre-v002 historical context before
  2024-12-01** (i.e., 2024-03-01 through 2024-11-30).
- **No ETHUSDT.**
- **No extra horizons** (15s and 60s preserved; no new horizon).
- **No mark-price.**
- **No spot.**
- **No cross-venue.**
- **No order book.**
- **No tick data.**
- **No v003.**
- **No storage migration.**
- **No database creation.**
- **No Parquet compaction.**
- **No ML, diagnostics, strategy, signals, PnL, or backtests.**

The envelope preserves the v002 feature family (the 45 computed feature
columns) and the v002 label family (3-class strict-sign direction at 15s
and 60s, flat class preserved explicitly) unchanged. The acquisition
would extend the existing 90-day window **backward** in calendar time
only.

## 9. Exact UTC calendar range

**Recommended exact range: 2024-03-01 through 2025-02-28 inclusive UTC.**

Reasoning at design level (repository-evidence-grounded; preferred over
the illustrative `2024-04-01 .. 2025-03-31` example in Phase 4bn-H §13.2
precisely because that example would add post-v002 March-2025 dates):

- **Exactly 365 calendar days.** 2024 is a leap year; March 2024
  through February 2025 spans 366 − 1 = 365 days (2024-03-01 .. 2025-02-28
  inclusive). The window is one continuous single-symbol BTCUSDT history.
- **Ends at the existing v002 envelope end date.** The window terminates
  at 2025-02-28, identical to the existing v002 90-day envelope end.
- **Contains the existing v002 90-day envelope as the terminal portion.**
  2024-12-01 through 2025-02-28 sits at the tail of the range; the new
  acquisition adds only the 275-day pre-v002 segment 2024-03-01 ..
  2024-11-30 in front of it.
- **Preserves the existing v002 sealed test split untouched.** The
  15-day sealed test split 2025-02-14 .. 2025-02-28 remains the terminal
  segment of the range. No backward extension touches it.
- **Extends backward rather than forward.** The existing v002 sealed
  test split therefore remains **terminal historical evidence** within
  the proposed range; no later-dated data is introduced ahead of it.
- **Avoids introducing post-v002 dates before a new holdout policy is
  predeclared.** Because no date after 2025-02-28 is acquired, the first
  expansion cannot accidentally create a newer terminal window that
  would demand a holdout-policy decision the acquisition phase is not
  authorized to make.
- **Materially broader regime exposure.** A 365-day window samples
  materially broader calendar, volatility, activity, funding, intraday,
  weekday, and event-regime exposure than the 90-day window, per Phase
  4bn-H §10 Option C.
- **Bounded compared with 24 months.** It remains bounded versus Option
  D (24 months), so the first expansion measures real per-day disk and
  runtime cost before any larger envelope is considered.
- **Comparable to the Phase 4bn-B / 4bn-C evidence.** The terminal
  90-day portion of the range is byte-comparable to the existing v002
  window, so any future descriptive ML-baseline rerun on the expanded
  envelope (separately authorized) remains comparable to the existing
  Phase 4bn-B / 4bn-C descriptive picture.

If a future acquisition execution-phase preflight, or newer repository
evidence, shows that a *different* exact 12-month window is safer, that
phase may recommend a different range **only** under a separately
authorized amendment, and **only** if it preserves the existing v002
sealed test split (2025-02-14 .. 2025-02-28) untouched and does not
introduce post-v002 dates ahead of it without a separately predeclared
holdout policy.

## 10. Source endpoint policy confirmation requirement

Phase 4bn-I calls no endpoint. It **requires** that the future
acquisition phase, if separately authorized, confirms source policy from
the committed `docs/04-data/historical-data-spec.md` and any existing
acquisition tooling **before fetching anything**.

The execution plan declares:

- **public Binance USDⓈ-M futures bulk historical archives only;**
- **no credentials;**
- **no private endpoint;**
- **no authenticated API;**
- **no WebSocket;**
- **no user stream;**
- **no `.env`;**
- **no `.mcp.json`;**
- **no MCP;**
- **no Graphify;**
- **fail closed if source URL, archive naming, schema, or availability
  differs from committed source policy;**
- **if source policy is insufficient or ambiguous, stop and require a
  separate source-policy memo before acquisition.**

**Explicit source-policy gap flagged for the future phase.** The
committed `historical-data-spec.md` canonical source policy is written
around official Binance USDⓈ-M *kline / mark-price / funding / metadata*
endpoints; it does **not** explicitly enumerate the **aggTrades bulk
historical archive** source (URL pattern, per-day archive naming,
checksum policy, schema) at the same level of detail. Phase 4bn-I does
not resolve this gap (resolving it would require inspecting source
tooling and/or endpoints, which is out of scope). The execution plan
therefore **requires** that the future acquisition phase treat the
aggTrades bulk-archive source policy as **ambiguous until confirmed**:
it must confirm the exact archive source from committed docs and/or
existing acquisition tooling, and if that confirmation is insufficient
or ambiguous, it must **fail closed** and require a separately
authorized source-policy memo before any fetch. Phase 4bn-I neither
calls the source nor authorises the source-policy memo; it only records
that one may be required.

## 11. Canonical path layout, design-level only

Phase 4bn-I pre-declares the future local **gitignored** namespaces
without creating them, following the repository's actual canonical path
pattern established by the Phase 4bb-F canonical path policy and the
existing `data/microstructure/` family layout (the pattern carried
verbatim from Phase 4bn-H §11). The chosen pattern is the existing
per-family `data/microstructure/<family>/` convention:

- **Raw aggTrades archives** under the existing `data/microstructure/raw/`
  family path convention;
- **Normalized aggTrades** under the existing
  `data/microstructure/normalized/` family path convention;
- **v002-compatible feature outputs** under the existing
  `data/microstructure/features/` family path convention;
- **v002-compatible label outputs** under the existing
  `data/microstructure/labels/` family path convention;
- **Manifests** under the existing `data/microstructure/manifests/`
  path convention;
- **Any future descriptive ML-baseline outputs** only under
  `data/research/` (e.g., `data/research/microstructure/ml-baselines/phase-4bn-{X}/`)
  and only if **separately authorized later**;
- **Any future diagnostics outputs** only under `data/research/` and
  only if **separately authorized later**.

All of the above are gitignored (`.gitignore` rules for
`data/microstructure/` and `data/research/`) and are **never committed**.

Phase 4bn-I states explicitly:

- **Phase 4bn-I does not create these paths.**
- **Phase 4bn-I does not write these files.**
- The future acquisition phase, if separately authorized, may create
  **only** acquisition-related local gitignored raw / normalized /
  feature / label / manifest artefacts under the
  `data/microstructure/<family>/` conventions above.
- **The future acquisition phase must not create ML or diagnostic
  outputs** (those remain `data/research/` artefacts gated behind
  separate later authorization).

If a future acquisition execution phase finds that the **exact** existing
on-disk path patterns differ from the `data/microstructure/<family>/`
convention named here (Phase 4bn-I does not inspect on-disk paths, so it
cannot confirm them byte-for-byte), it must follow the repository's
actual canonical path pattern as established by the Phase 4bb-F policy
and document the precise pattern chosen, without path drift relative to
the existing v002 layout.

## 12. Expected future artefact families, design-level only

Any future acquisition phase, if separately authorized, would produce
the following artefact families. Phase 4bn-I **defines** which families
would be needed; it **does not create** them.

- **Raw aggTrades archives** — public Binance USDⓈ-M aggTrades archives
  for 2024-03-01 .. 2025-02-28; under `data/microstructure/raw/`;
  canonical Phase 4bb-F sidecars; gitignored; never committed. Governed
  by a separately authorized raw eligibility-gate execution.
- **Normalized aggTrades** — normalized aggTrade tables under the
  existing v002 normalization logic (Phase 4bd implementation; Phase 4be
  structural-QA result preserved verbatim); under
  `data/microstructure/normalized/`; canonical sidecars; gitignored;
  never committed. Governed by a separately authorized derived
  eligibility-gate execution.
- **v002-compatible feature outputs** — feature parquets under the
  existing v002 feature kernel (45 `computed_feature_column_names`
  preserved); under `data/microstructure/features/`; canonical sidecars;
  gitignored; never committed. Governed by a separately authorized
  feature-family eligibility-gate execution.
- **v002-compatible label outputs** — label parquets under the existing
  v002 label kernel (strict-sign direction at 15s and 60s; flat class
  preserved explicitly); under `data/microstructure/labels/`; canonical
  sidecars; gitignored; never committed. Governed by a separately
  authorized label-family eligibility-gate execution.
- **Per-family manifests** — raw / normalized / feature / label
  manifests recording phase identity, base SHA, source manifest SHAs,
  split-policy snapshot, source endpoint set, fetch timestamps,
  transform / pipeline version, schema version, partitioning rules,
  primary-key definition, generation timestamp, quality checks, known
  issues, and predecessor versions; under
  `data/microstructure/manifests/`; canonical sidecars; gitignored;
  never committed.
- **Future descriptive ML-baseline outputs** — analogous to the Phase
  4bn-B local artefacts; **only if separately authorized later**; under
  `data/research/`; never committed. **Not produced by the acquisition
  phase.**
- **Future diagnostics outputs** — analogous to the Phase 4bn-E local
  artefacts; **only if separately authorized later**; under
  `data/research/`; never committed. **Not produced by the acquisition
  phase.**

## 13. Manifest and sidecar policy

The execution plan preserves the following manifest / sidecar policy
verbatim for any future acquisition phase:

- **Phase 4bb-F canonical sidecar policy** — every future artefact
  carries a canonical sidecar of the form `<sha256>  <basename>\n`
  (two-space separator; LF only; no CRLF; no BOM; no extra fields).
- **Refuse-overwrite behavior** — an existing artefact or sidecar must
  never be silently overwritten; a duplicate write fails closed.
- **SHA256 sidecars for every future artefact** — raw, normalized,
  feature, label, and manifest artefacts each carry a SHA256 sidecar.
- **Manifest immutability** — published dataset-version manifests are
  immutable per `docs/04-data/dataset-versioning.md`; corrections create
  a new version with a recorded predecessor, never an in-place rewrite.
- **Dataset-versioning `__vNNN` naming policy** — manifests follow the
  `<dataset_name>__vNNN` pattern with monotonic version numbers;
  identifiers are never reused or overwritten.
- **All new manifests start `research_eligible: false`.**
- **All new manifests start `eligibility_gate_status: "pending"`.**
- **Label manifest starts `chronological_split_policy: "not_yet_defined"`.**
- **No `research_eligible` flip from acquisition.**
- **No `eligibility_gate_status` transition from acquisition.**
- **No `chronological_split_policy` transition from acquisition.**
- **No `diagnostics_authorized` or `ml_authorized` transition from
  acquisition.**
- **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved** (never invoked by acquisition;
  manifest eligibility transitions require a separately authorized gate
  phase, not the acquisition phase).

Under the recommended v002-semantics-preserved envelope, the expectation
is that the v002 feature / label schema is preserved exactly (no
schema-driven `__vNNN` bump for the feature / label families); any new
raw manifest produced by per-day acquisition conforms to the existing
raw schema. Any breaking schema change would trigger a new dataset
version with explicit predecessor reference per `dataset-versioning.md`.

## 14. Existing v002 sealed-test preservation and new holdout policy

**Existing v002 sealed-test preservation (preserved verbatim):**

- the existing v002 test split **2025-02-14 through 2025-02-28 remains
  sealed**;
- **no test-holdout read, count, sample, hash, summary, metric, or
  inspection** of any kind;
- any future acquisition phase **must not open the existing v002 test
  split**;
- because the recommended acquisition range ends at 2025-02-28 and adds
  only backward history, the existing v002 test split **remains terminal
  within the proposed range**;
- the `iter_partitions(split="test", ...)` raise pattern in the existing
  Phase 4bn-B implementation is the canonical enforcement and remains
  unchanged (`test_rows_loaded: 0`).

**New holdout policy:**

- any future **new** holdout policy for the 12-month expanded envelope
  must be **separately predeclared** before ML or diagnostics are run;
- **acquisition alone must not define a model-evaluation holdout** beyond
  recording that no ML is authorized;
- if a future acquisition execution phase chooses to introduce a new
  sealed terminal window inside the expanded envelope, that window must
  be **sealed by construction**; opening it would require a separately
  authorized terminal-holdout phase that does not exist and is not
  authorized by Phase 4bn-I;
- the recommended range (§9) deliberately ends at the existing v002 end
  date so that **no new holdout decision is forced by the first
  expansion** — the existing sealed test split simply remains terminal.

## 15. Disk-footprint cap and derivation-time cap

Phase 4bn-I must not inspect local data, so it does **not** compute exact
disk usage or derivation time from local files. It defines **caps** at
design level and **requires** a future execution-phase preflight estimate
before acquisition.

**Disk-footprint cap:**

- **Hard local disk-footprint cap for the first acquisition phase: 5 GiB
  additional** local data footprint across raw + normalized + feature +
  label + manifest artefacts;
- **Warning threshold: 3 GiB additional** local data footprint;
- **Fail-closed if the future preflight estimate exceeds 5 GiB before
  acquisition;**
- **Fail-closed if actual footprint crosses 5 GiB during acquisition**
  (checked at each per-day boundary; no further per-day acquisition
  proceeds without a separately authorized cap update);
- if repository evidence or existing docs indicate a **safer (lower)
  cap**, the future phase must use the safer cap and explain why. Phase
  4bn-I sets 5 GiB as a conservative design-level ceiling for an
  approximately 4× scaling of the 90-day v002 raw + normalized + feature
  + label footprint (Phase 4bn-H §10 Option C ≈ 4×); the true ceiling is
  governed by the future preflight estimate, which must not exceed 5 GiB.

**Derivation-time cap:**

- **Hard derivation-time cap: 4 hours total wall-clock** for raw
  verification + normalization + v002-compatible feature derivation +
  v002-compatible label derivation on the 12-month BTCUSDT envelope;
- **Warning threshold: 2 hours;**
- **Fail-closed if the future preflight estimate exceeds 4 hours before
  acquisition;**
- **Fail-closed if actual derivation runtime crosses 4 hours during
  acquisition;**
- if repository evidence or existing docs indicate a **safer (lower)
  cap**, the future phase must use the safer cap and explain why. The
  4-hour ceiling is a conservative design-level bound: at roughly 4× the
  Phase 4bn-E two-pass diagnostic scaling unit (~2 200 s ≈ 37 minutes for
  an equivalent 12-month two-pass diagnostic per Phase 4bn-H §10 Option
  C), a full normalize + feature + label derivation pass over 12 months
  is expected to be comfortably under 4 hours, leaving headroom; the true
  ceiling is governed by the future preflight estimate, which must not
  exceed 4 hours.

Both caps must be **measured** during the future acquisition phase (disk
footprint at each per-day boundary; derivation runtime cumulatively);
neither is measured by Phase 4bn-I.

## 16. Fail-closed stop conditions

The future acquisition phase must declare and enforce at minimum the
following 25 fail-closed stop conditions. Phase 4bn-I **defines** them;
it **executes** none.

1. **Source endpoint or archive naming mismatch** — fail closed until a
   separately authorized source-policy memo governs the divergence.
2. **Public source unavailable** — fail closed; no silent retry against
   any non-public or authenticated alternative.
3. **Archive missing for any expected day** — fail closed for that day;
   the gap is recorded in the manifest `known_issues`; no silent gap
   repair.
4. **Duplicate archive or overwrite attempt** — fail closed (Phase 4bb-F
   refuse-overwrite); the duplicate fetch is logged.
5. **Unexpected schema** — fail closed; the archive is preserved on disk
   with its sidecar; no downstream derivation proceeds on that day.
6. **Timestamp monotonicity violation** — fail closed; archive preserved
   for diagnostic review; no downstream derivation.
7. **Unexpected timestamp gap** — fail closed; gap recorded; no silent
   repair.
8. **Unexpected duplicate aggTrade primary key** — fail closed; logged;
   no deterministic auto-merge without a documented rule.
9. **Sidecar format mismatch** — fail closed until canonicalised per the
   Phase 4bl-F R-SIDECAR-CRLF standing rule or a separately authorized
   memo.
10. **SHA256 hash mismatch** — fail closed; the archive is treated as
    suspect; no downstream derivation.
11. **Manifest validation failure** — fail closed; no downstream
    derivation.
12. **Disk-footprint warning threshold crossed (3 GiB)** — warn; the
    phase records the warning and continues only within the hard cap.
13. **Disk-footprint hard cap exceeded (5 GiB)** — fail closed at the
    next per-day boundary; no further acquisition without a separately
    authorized cap update.
14. **Derivation-time warning threshold crossed (2 hours)** — warn; the
    phase records the warning and continues only within the hard cap.
15. **Derivation-time hard cap exceeded (4 hours)** — fail closed; no
    further derivation without a separately authorized cap update.
16. **Any attempt to read the existing v002 test holdout** — fail closed;
    the `iter_partitions(split="test", ...)` raise pattern is the
    canonical enforcement.
17. **Any attempt to create a new ML split without separate
    authorization** — fail closed.
18. **Any attempt to run ML, diagnostics, strategy, PnL, or backtests**
    — fail closed; the acquisition phase produces only raw / normalized
    / feature / label artefacts.
19. **Any attempt to create DuckDB / SQLite / database files** — fail
    closed; no `.duckdb` or `.sqlite` artefact is created.
20. **Any attempt to compact Parquet** — fail closed; per-day
    partitioned Parquet is preserved as-is.
21. **Any attempt to commit `data/microstructure` or `data/research`** —
    fail closed; the `.gitignore` rules plus a per-phase
    `git check-ignore -v` verification gate make accidental commits
    detectable.
22. **Any credential / private-endpoint / WebSocket / user-stream /
    `.env` / `.mcp.json` / MCP / Graphify usage** — fail closed; the
    Phase 4bl-F §7 N-CREDENTIALS and N-ENDPOINT blocks apply verbatim.
23. **Any manifest eligibility transition** — fail closed; no
    `research_eligible` / `eligibility_gate_status` /
    `chronological_split_policy` / `diagnostics_authorized` /
    `ml_authorized` change from acquisition alone.
24. **Any deviation from the exact UTC date range (2024-03-01 ..
    2025-02-28)** — fail closed; a range change requires a separately
    authorized execution-plan amendment.
25. **Any requirement to add ETHUSDT, v003, mark-price, spot,
    cross-venue, order-book, or extra-horizon data** — fail closed; the
    first expansion is BTCUSDT aggTrades only.

## 17. Future acquisition phase non-authorization envelope

The future acquisition phase, if later separately authorized, would be
**acquisition-only** and would still **not** authorize:

- ML training; model scoring; predictions; diagnostics;
- feature ranking / selection / pruning / engineering;
- hyperparameter tuning; threshold tuning; calibration fitting;
- strategy research; signal generation; PnL; backtests;
- paper / shadow / live; exchange-write; production keys;
- storage migration; database creation; Parquet compaction;
- v003; ETHUSDT; mark-price; spot; cross-venue; order book;
- manifest eligibility transitions.

The acquisition phase produces raw / normalized / feature / label
artefacts and their manifests / sidecars only, each starting at
non-eligible manifest state, and authorises no downstream use.

## 18. Post-acquisition gates and required successor chain

If a future acquisition phase is separately authorized and completed,
the project **still** requires the following separate successor phases
before any research use. Phase 4bn-I **predeclares** this chain; it
authorizes none of it.

1. **Acquisition merge-closeout on `main`** — per
   `merge-closeout-standard.md` (Tier 1).
2. **Raw archive eligibility validation / gate** — separately authorized
   raw eligibility-gate execution.
3. **Normalized artefact eligibility validation / gate** — separately
   authorized derived eligibility-gate execution.
4. **Feature-family derivation and eligibility gate** — separately
   authorized feature-family eligibility-gate execution.
5. **Label-family derivation and eligibility gate** — separately
   authorized label-family eligibility-gate execution.
6. **Successor-state recording if required by repo convention** — per
   the existing per-family successor-state recording protocol.
7. **New chronological split / holdout policy memo before any ML or
   diagnostics** — separately authorized; required before any
   `chronological_split_policy` transition.
8. **Separate descriptive ML-baseline implementation plan before any ML
   rerun** — separately authorized; satisfies the Phase 4bn-A design
   boundary.
9. **Separate diagnostics plan before any diagnostics rerun** —
   separately authorized; satisfies the Phase 4bn-E measurement-frame
   boundary.
10. **No test-holdout use until a future explicitly authorized
    terminal-holdout phase, if ever** — the existing v002 sealed test
    split and any new sealed window remain sealed until and unless such a
    phase is separately authorized.

## 19. Decision

**`RECOMMEND_AUTHORIZE_ACQUISITION_ONLY_PHASE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Rationale (anchored to §5 – §18 and to the repository evidence, not to a
preference):

1. **The question has been progressively narrowed by the repository
   evidence chain.** Phase 4bn-F reduced a data-sufficiency *concern* to
   an unresolved question; Phase 4bn-G converted it to a combined
   data-expansion + storage-scaling *scoping framework*; Phase 4bn-H
   converted that to an *acquisition-readiness* recommendation focused on
   Option C; Phase 4bn-I now records the *exact execution plan* for that
   Option C envelope. Each step has been a separately authorized Tier 1
   phase that authorised nothing executable.
2. **Phase 4bn-I successfully records every value an acquisition phase
   would otherwise have to invent.** Exact range (§9), exact caps (§15),
   exact paths (§11), exact sidecar / manifest policy (§13), exact
   holdout preservation (§14), and exact fail-closed stop conditions
   (§16) are all now fixed. The future acquisition phase would inherit a
   fixed, fail-closed contract rather than discretionary scope.
3. **The next logical non-paused step is therefore an acquisition-only
   phase**, separately authorized, bounded by this plan. That phase must
   remain acquisition-only and must still not run ML, diagnostics,
   storage migration, v003, strategy, PnL, or backtests (§17).
4. **This recommendation is not edge-search.** It recommends only that a
   bounded, fail-closed acquisition-only phase *could be executed safely*
   — it does **not** claim that more data will establish edge,
   sufficiency, or tradability, and it does **not** recommend tuning,
   strategy, signal, storage-migration, or deployment work.
5. **The operator is not pressured.** Phase 4bn-I does not foreclose
   remaining paused, closing the ML-baseline arc, or authorizing instead
   a docs-only storage-architecture decision memo or a docs-only holdout
   / split-policy memo (§20). The acquisition-only recommendation is the
   cleanest non-paused, non-arc-closing option, **subject to separate
   operator authorization**.
6. **Phase 4bn-I authorizes nothing.** The successor acquisition-only
   phase is recommended only. A separate operator authorization is
   required after this branch is merged. No acquisition, storage
   migration, database creation, Parquet compaction, v003 creation, ML,
   diagnostics, strategy, signal, PnL, or backtest is authorized by Phase
   4bn-I.

## 20. Recommended state and successor options

**Recommended state: remain paused.**

Phase 4bn-I is **recommendation-only** and does not authorize any
successor. The operator may equivalently choose any of the following:

- **remain paused** (default; no successor authorized; the
  recommendation does not pressure the operator to authorize a
  successor);
- **request a merge prompt for Phase 4bn-I** so the acquisition execution
  plan becomes project-complete on `main`;
- **reject further ML-baseline successors and close the ML arc**
  (operationally close the v002 ML-baseline family for further bounded
  expansion under current evidence; preserve all Phase 4bn-A .. 4bn-I
  artefacts as research evidence; preserve every retained verdict and
  project lock; no further v002 ML-baseline follow-up under this arc
  unless reopened by a separately authorized future phase; does not
  delete evidence; does not close Prometheus);
- **separately authorize the recommended acquisition-only phase**
  (recommended) bounded exactly by this plan (BTCUSDT aggTrades;
  2024-03-01 .. 2025-02-28; 5 GiB / 4 h caps; v002 semantics preserved;
  Parquet canonical; DuckDB-in-place; no ETHUSDT / v003 / compaction /
  database; manifests start non-eligible; sealed v002 test split
  untouched; 25 fail-closed stop conditions); must remain
  acquisition-only;
- **separately authorize a docs-only storage-architecture decision
  memo** (a weaker variant; must remain docs-only and must not authorize
  any storage migration);
- **separately authorize a docs-only holdout and split-policy memo** (a
  weaker variant focused on the new-holdout question raised in §14; must
  remain docs-only and must not transition `chronological_split_policy`).

**No acquisition / storage migration / paper / shadow / live /
exchange-write option is valid unless separately authorized after this
branch is merged.**

## 21. Explicit non-authorizations

Phase 4bn-I is docs-only / design-only / scoping-only and authorizes
**nothing executable**. It does not, and cannot, authorize:

- any data acquisition (no aggTrades acquisition; no additional days /
  symbols / families / horizons; no ETHUSDT; no v003; no mark-price /
  spot / cross-venue / order-book / tick data; no longer-history
  acquisition; no new feature or label engineering);
- any public / Binance / authenticated / private endpoint call; any
  WebSocket / user stream; any credential / `.env` / `.mcp.json` / MCP /
  Graphify use;
- any storage migration (no Parquet → DuckDB / SQLite / other database
  migration; no Parquet compaction; no partition restructuring; no
  `.duckdb` / `.sqlite` / other database file creation);
- any ML training, model scoring, prediction generation, feature ranking,
  feature selection, feature pruning, feature engineering, model
  selection through results, hyperparameter tuning, threshold tuning,
  calibrator fitting, meta-labeling, ensemble construction, or any other
  ML execution;
- any diagnostics rerun, diagnostic artefact creation, ML artefact
  creation, reusable split-mask materialization, row-level prediction
  persistence, or model-binary persistence;
- any strategy research, strategy design, signal generation, trade-signal
  generation, PnL simulation, equity-curve construction, backtests, or
  walk-forward optimization;
- any use of the test holdout for training, fitting, calibration,
  evaluation, tuning, design, model selection, threshold selection,
  reporting, or inspection;
- any manifest mutation, successor-state mutation, gate-report mutation,
  or change to `research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`, `diagnostics_authorized`, or
  `ml_authorized` on any on-disk manifest;
- any source / test / committed-script / config / `.gitignore` /
  `pyproject.toml` / `README.md` / MCP-file modification;
- any commit under `data/microstructure/` or `data/research/`;
- the acquisition-only phase itself (recommended but not authorized), any
  docs-only storage-architecture decision memo, any docs-only holdout /
  split-policy memo, any storage-migration phase, any database-creation
  phase, any Parquet-compaction phase, any v003-creation phase, any ML
  implementation, any diagnostics implementation, Phase 4bn-J, any
  further Phase 4bn-* / 4bo-* / 4bp-* successor, Phase 5, or Phase 4
  canonical;
- paper / shadow; live-readiness; deployment; exchange-write;
  production-key creation; authenticated APIs; private endpoints; user
  stream; WebSocket implementation;
- any revision of a retained verdict, any loosening of a project lock, or
  any amendment of M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F
  / Phase 4bm-A-P1 / Phase 4bm-D-P1.

**Phase 4bn-I is a docs-only / design-only / scoping-only acquisition
execution plan.** **Phase 4bn-I does not acquire data.** **Phase 4bn-I
does not call public, Binance, authenticated, or private endpoints.**
**Phase 4bn-I does not migrate storage.** **Phase 4bn-I does not create
any database.** **Phase 4bn-I does not compact Parquet.** **Phase 4bn-I
does not create v003.** **Phase 4bn-I does not authorize acquisition.**
**Phase 4bn-I does not authorize any successor.** **Phase 4bn-I does not
mutate any manifest.** **Phase 4bn-I does not mutate any successor-state
artefact.** **Phase 4bn-I does not commit `data/microstructure`.**
**Phase 4bn-I does not commit `data/research`.** **Phase 4bn-I does not
authorize Phase 4bn-J, Phase 5, paper / shadow, live-readiness,
deployment, exchange-write, production keys, or any successor phase.**

## 22. Current-project-state update summary

The narrow `docs/00-meta/current-project-state.md` update made by Phase
4bn-I consists of:

- a new Phase 4bn-I paragraph appended immediately after the Phase 4bn-H
  paragraph;
- a new "Current phase:" block for Phase 4bn-I inserted immediately
  before the existing Phase 4bn-H "Current phase:" block;
- preservation of every earlier paragraph (Phase 4a .. Phase 4bn-H) and
  every earlier "Current phase:" block (Phase 4bn-H, Phase 4bn-G, Phase
  4bn-F, Phase 4bn-E, Phase 4bn-D, Phase 4bn-C, Phase 4bn-B, and older
  blocks) as labelled historical context;
- recording of Phase 4bn-I as **branch-complete only, not merged, not
  project-complete**;
- recording of the Phase 4bn-I decision
  `RECOMMEND_AUTHORIZE_ACQUISITION_ONLY_PHASE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
- recording of the exact non-authorizations (per §0 / §3 / §21);
- recording of the recommended state (**remain paused**);
- explicit statement that an acquisition-only successor phase (Phase
  4bn-J or any equivalent under any name) is recommended but **not
  authorized** by Phase 4bn-I.

No other section of `docs/00-meta/current-project-state.md` is modified.
No retained verdict, project lock, manifest field, successor-state
field, gate-report field, or governance label is changed. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant is preserved (never invoked by Phase 4bn-I).

---

## Appendix A — Retained verdicts preserved

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All prior phase results (Phase 4am .. Phase 4bn-H) preserved verbatim.

## Appendix B — Project locks preserved

All preserved verbatim: §11.6 = 8 bps per side / round-trip 16 bps;
§1.7.3 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7;
Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k;
Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 + post-null
cooldown + cooled-down families list + memo template; Phase 4al refined
no-rescue + §13 boundary + §14 hierarchy; Phase 4aw
`flip_research_eligible(...)` always-raises invariant (never invoked);
Phase 4bb-F canonical path policy + sidecar policy; Phase 4bl-F
four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization
blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase
4bm-D-P1 lightweight Claude Code workspace standard.

## Appendix C — Recommended next state

**Remain paused.** Phase 4bn-I is branch-complete only by this work; not
merged into main; not project-complete. Per `phase-workflow-standard.md`,
Phase 4bn-I is NOT project-complete until a separately authorized merge
phase records its merge-closeout on `main` per
`merge-closeout-standard.md` (Tier 1). The recommended successor — a
separately authorized acquisition-only phase bounded exactly by this
plan — is **recommended only and not authorized**. No next phase is
authorized.
