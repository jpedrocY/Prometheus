# Phase 4bb-F — Gate Report Output Path Hygiene

**Phase identity:** Phase 4bb-F — Gate Report Output Path Hygiene (docs-only path-governance memo).
**Date:** 2026-05-11.
**Branch:** `phase-4bb-f/gate-report-output-path-hygiene`.
**Base:** `main` at `bb9e1322aef54dce80dd2afb49a51674d1994dbf` (post-Phase-4bj-G SHA-chain-fixup state). Phase 4bj-G merge commit `92d9e5b76fd5d34a26ed01ec4f1d2f6e87edf4b2` and merge-closeout commit `73970aff3ec51cba7f320a7d0ec6a38b69dc9e11` confirmed as ancestors of `main`. The one-commit fixup on top of `73970af` (commit `bb9e132`) only records the final-SHA value into the Phase 4bj-G merge-closeout's §2 placeholder; it does not change Phase 4bj-G lifecycle semantics.
**Status:** drafted; pending operator review.
**Phase type:** docs-only path-governance memo.

---

## 1. Phase identity

Phase 4bb-F is a docs-only path-governance memo. It is the deferred cleanup originally proposed by Phase 4bb-E §15 (the "doubled `gate-reports/gate-reports/` path issue") and recommended again as conditional cleanup by Phase 4bb-D / Phase 4bf / Phase 4be / Phase 4bi-A / Phase 4bi-D / Phase 4bj-E / Phase 4bj-G — none of which authorised Phase 4bb-F.

**Phase 4bb-F is path-governance only.** It produces:

- exactly one new memo file under `docs/00-meta/implementation-reports/`;
- exactly one narrow paragraph + new "Current phase:" block in `docs/00-meta/current-project-state.md`;
- a future-facing canonical path policy that any future gate-report or successor-state phase should consult.

Phase 4bb-F does **not**:

- modify any source code, test, script, configuration, `.gitignore`, `pyproject.toml`, `README.md`, MCP file, or runtime configuration;
- modify any existing gate report;
- modify any existing successor-state artefact;
- modify any sidecar;
- modify any manifest (raw, derived, feature, or label);
- modify any label parquet, feature parquet, or normalized parquet;
- run, rerun, or invoke any gate (raw, derived, feature, or label);
- run kernels or normalizers;
- migrate, copy, rename, or delete any existing local artefact;
- create or read credentials, `.env`, `.mcp.json`, MCP, or Graphify;
- contact any Binance endpoint, public endpoint, authenticated endpoint, private endpoint, user stream, or WebSocket;
- compute features, labels, signals, ML output, strategy output, or backtest output;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output;
- acquire data;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any manifest;
- revise any retained verdict;
- change any project lock;
- amend M0;
- authorize any successor phase (Phase 4bb-G, Phase 5, label evaluation, ML, strategy, backtests, acquisition, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, or user stream).

---

## 2. Problem statement

The Prometheus microstructure data lineage has produced four distinct gate-report families and three distinct successor-state families:

- raw-family gate report (Phase 4bb-D, written by the Phase 4bb-C `run_eligibility_gate` orchestrator);
- derived-family gate report (Phase 4bf, written by the Phase 4bf `run_derived_aggtrades_gate` orchestrator);
- feature-family gate report (Phase 4bi-B, written by the Phase 4bi-B `run_feature_family_gate` orchestrator);
- label-family gate report (Phase 4bj-E, written by the Phase 4bj-E `run_label_family_gate` orchestrator);
- derived-family successor-state (Phase 4bg-B);
- feature-family successor-state (Phase 4bi-D);
- label-family successor-state (Phase 4bj-G).

Each was added independently and at a different phase boundary. As a consequence the on-disk path conventions are not perfectly uniform:

- some writers compose a doubled subdirectory segment (Phase 4bb-C raw gate);
- some writers use per-family subdirectories (Phase 4bf normalized, Phase 4bi-B features, Phase 4bj-E labels);
- successor-state artefacts live flat in a single shared directory (no per-family subdirectory);
- the gate-report filename conventions diverged: older writers omit a `phase-<id>` tag (Phase 4bb-D, Phase 4bf), while newer writers include one (Phase 4bi-B, Phase 4bj-E);
- successor-state filename conventions are uniform across families and use a stable `<family>__<version>__<stage_marker>__<phase-id>.json` pattern.

Path hygiene matters because:

- a future repeated raw-gate execution would write to a doubled path (`data/microstructure/gate-reports/gate-reports/`) per the Phase 4bb-E §15-documented Phase 4bb-C orchestrator behaviour;
- without a canonical policy, future gate-report or successor-state phases may invent yet another convention, increasing path drift and operator cognitive load;
- ambiguity between report-level PASS evidence (a gate report) and policy-level admissibility (a successor-state artefact) can confuse future tooling if both kinds of artefact share too similar a naming surface;
- sidecar mismatch ambiguity (whether the sidecar is the SHA of the JSON or the SHA of the sidecar itself, and where the basename in the sidecar should resolve relative to) needs to be locked before future repeated runs;
- the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant must be preserved by every future writer.

The goal of Phase 4bb-F is therefore not to migrate any existing artefact, but to lock the **prospective** path policy so that any future repeated gate execution or new successor-state recording follows a single canonical convention.

---

## 3. Existing path inventory

The following inventory is derived from `find data/microstructure/gate-reports/` and `find data/microstructure/successor-state/` on the Phase 4bb-F base commit (`bb9e132`). Each artefact is present locally, gitignored under `.gitignore:85: data/microstructure/`, and NOT committed.

### 3.1 Raw-family gate report (Phase 4bb-D)

| Item | Value |
| ---- | ----- |
| Path | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` |
| Paired sidecar | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json.sha256` |
| Report SHA256 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Sidecar SHA256 (self) | (sidecar file content is `<json-sha256>  <basename>\n`) |
| Filename pattern | `<family>__<version>__<unix_ms>__<short_commit>.json` (NO `phase-<id>` tag) |
| Writer | Phase 4bb-C `run_eligibility_gate` orchestrator |
| Observed anomaly | doubled `gate-reports/gate-reports/` path segment |
| Anomaly history | documented verbatim in Phase 4bb-E §15 and §5.D; called out as the canonical reason a future Phase 4bb-F should exist |
| Anomaly origin | Phase 4bb-C orchestrator composes `output_root / "gate-reports" / filename` while Phase 4bb-D supplied `output_root = data/microstructure/gate-reports`; result is `data/microstructure/gate-reports/gate-reports/<filename>` |
| Validity | the report and sidecar are bit-for-bit valid evidence; the SHA matches the sidecar; the file is well-formed JSON; the only issue is the path |

### 3.2 Derived-family gate report (Phase 4bf)

| Item | Value |
| ---- | ----- |
| Path | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json` |
| Paired sidecar | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json.sha256` |
| Report SHA256 | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Filename pattern | `<family>__<version>__<unix_ms>__<short_commit>.json` (NO `phase-<id>` tag) |
| Writer | Phase 4bf `run_derived_aggtrades_gate` orchestrator |
| Observed anomaly | none — single `normalized/` subdirectory under `gate-reports/`; not doubled |
| Subdirectory choice | `normalized/` (derived family is named `microstructure_normalized_aggtrades_v001`) |

### 3.3 Feature-family gate report (Phase 4bi-B)

| Item | Value |
| ---- | ----- |
| Path | `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v001__phase-4bi-b__1778436978312__2bc026b4e0d9.json` |
| Paired sidecar | `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v001__phase-4bi-b__1778436978312__2bc026b4e0d9.json.sha256` |
| Report SHA256 | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| Filename pattern | `<family>__<version>__phase-<id>__<unix_ms>__<short_commit>.json` (INCLUDES `phase-<id>` tag) |
| Writer | Phase 4bi-B `run_feature_family_gate` orchestrator |
| Observed anomaly | none — single `features/` subdirectory under `gate-reports/`; not doubled |
| Subdirectory choice | `features/` (feature family is named `microstructure_features_aggtrades_v001`) |

### 3.4 Label-family gate report (Phase 4bj-E)

| Item | Value |
| ---- | ----- |
| Path | `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5.json` |
| Paired sidecar | `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5.json.sha256` |
| Report SHA256 | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` |
| Filename pattern | `<family>__<version>__phase-<id>__<unix_ms>__<short_commit>.json` (INCLUDES `phase-<id>` tag) |
| Writer | Phase 4bj-E `run_label_family_gate` orchestrator |
| Observed anomaly | none — single `labels/` subdirectory under `gate-reports/`; not doubled |
| Subdirectory choice | `labels/` (label family is named `microstructure_labels_aggtrades_v001`) |

### 3.5 Derived-family successor-state (Phase 4bg-B)

| Item | Value |
| ---- | ----- |
| Path | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json` |
| Paired sidecar | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json.sha256` |
| JSON SHA256 | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Filename pattern | `<family>__<version>__<stage_marker>__<phase-id>.json` (NO `unix_ms`, NO `short_commit` in filename) |
| Namespace | flat — directly under `successor-state/`, no per-family subdirectory |

### 3.6 Feature-family successor-state (Phase 4bi-D)

| Item | Value |
| ---- | ----- |
| Path | `data/microstructure/successor-state/microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json` |
| Paired sidecar | `data/microstructure/successor-state/microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json.sha256` |
| JSON SHA256 | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |
| Filename pattern | `<family>__<version>__<stage_marker>__<phase-id>.json` |
| Namespace | flat — same convention as Phase 4bg-B |

### 3.7 Label-family successor-state (Phase 4bj-G)

| Item | Value |
| ---- | ----- |
| Path | `data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bj-g.json` |
| Paired sidecar | `data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bj-g.json.sha256` |
| JSON SHA256 | `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5` |
| Filename pattern | `<family>__<version>__<stage_marker>__<phase-id>.json` |
| Namespace | flat — same convention as Phase 4bg-B and Phase 4bi-D |

### 3.8 Gitignore coverage

`.gitignore:85: data/microstructure/` covers the entire microstructure tree. Every artefact above is verified gitignored via `git check-ignore -v`. No artefact is tracked in git; all artefacts remain on the local filesystem only and are reproducible by re-invoking the appropriate writer at the recorded `code_commit_sha`.

---

## 4. Path-hygiene risks

The following risks are identified at the current evidence boundary. None of them is acutely dangerous (every artefact is gitignored, byte-validated, and bit-for-bit reproducible), but each represents a future trap that Phase 4bb-F's prospective policy should prevent.

### 4.1 Doubled `gate-reports/gate-reports/` repeat-write risk

If the Phase 4bb-C `run_eligibility_gate` orchestrator is invoked again with `output_root = data/microstructure/gate-reports`, it will write a second report to `data/microstructure/gate-reports/gate-reports/...`. This is harmless once (gitignored, byte-valid) but is undesirable as a project-record artefact path. Phase 4bb-E §15 documented this behaviour and recommended either D.2 (orchestrator code fix) or D.3 (calling-convention fix). Phase 4bb-F itself does **not** fix the code; it only locks the prospective policy.

### 4.2 Flat-vs-family-scoped namespace inconsistency

Gate reports live in family-scoped subdirectories (`gate-reports/normalized/`, `gate-reports/features/`, `gate-reports/labels/`, plus the doubled `gate-reports/gate-reports/` for raw). Successor-state artefacts live flat in `successor-state/`. A future operator skimming the repository may wonder which convention to apply to a new artefact class.

### 4.3 Filename-tag inconsistency between older and newer gate writers

Phase 4bb-D and Phase 4bf reports do **not** include a `phase-<id>` tag in the filename. Phase 4bi-B and Phase 4bj-E reports **do** include the tag. The tag is useful because it associates the report with a specific phase identity in addition to the `unix_ms` + `short_commit` combination. Without the tag, two consecutive runs of the same gate primitive (same `code_commit_sha`, different `unix_ms`) would produce two reports whose filenames differ only by the `unix_ms` value, with no obvious "this one was Phase 4bb-D, this one was the Phase 4bb-D re-run".

### 4.4 Sidecar format ambiguity

All current sidecars use the format `<json-sha256>  <basename>\n` (two spaces; trailing newline). This is the conventional `sha256sum` line format and is sufficient. The risk is that a future writer might emit a different format (e.g., a JSON wrapper containing the SHA) and break tooling that parses by whitespace. Phase 4bb-F should lock the format.

### 4.5 Repeat-run ambiguity for the same gate

If any of the four gates is run a second time at the same `code_commit_sha`, the existing writers' refuse-overwrite semantics will reject the second write because the report-id is derived from `unix_ms`, not `code_commit_sha`. (Two consecutive writes will have different `unix_ms`, so the filenames will differ.) This is acceptable, but the policy should document it explicitly so a future operator does not expect idempotent-by-content writes.

### 4.6 Branch-local artefact not reproducible from docs alone

Every gate report and successor-state artefact is reproducible from a `code_commit_sha` + input artefact set, but only if the tracked memo records that `code_commit_sha`. All current memos do; the prospective policy should require this verbatim.

### 4.7 Accidental commit risk

Because all artefacts live under `data/microstructure/` and `.gitignore:85` covers that root, no artefact can be accidentally committed via `git add data/microstructure/...`. Phase 4bb-F should reaffirm this and require that any future writer must validate gitignore coverage before writing.

### 4.8 Confusion between report-level PASS and successor-state admissibility

A gate report records an overall PASS / FAIL / ERROR over a list of checks. A successor-state artefact records a policy-level admissibility-in-principle decision. These are distinct kinds of evidence. The prospective policy should require that successor-state artefacts include explicit fields that distinguish the two kinds (which they currently do — every successor-state JSON records `successor_admissibility_status` and per-flag `*_authorized = false` markers, and never claims that the gate-level PASS itself authorises ML / strategy / backtest / acquisition / paper-shadow / live / exchange-write).

### 4.9 Confusion between manifest fields and sibling successor-state markers

The most important interpretation hazard. A label manifest's `research_eligible` field is **not** equivalent to a sibling successor-state's `successor_research_use_admissible` field. Any tool that consumes either artefact must read the correct one. The prospective policy should require that successor-state artefacts explicitly record both the original manifest's `research_eligible` (always false for raw / derived / feature / label families absent a separately authorized transition phase) and the successor-state's own admissibility marker — which the three existing successor-state JSONs already do.

### 4.10 Path drift across families

The four gate-report subdirectories (`gate-reports/gate-reports/`, `gate-reports/normalized/`, `gate-reports/features/`, `gate-reports/labels/`) reflect path drift across phase boundaries. A future fifth gate (e.g., a hypothetical `gate-reports/metrics/`) might add yet another convention.

---

## 5. Recommended canonical path policy (prospective only)

Phase 4bb-F recommends the following canonical path policy for all **future** repeated gate executions, new gate-report writers, new successor-state writers, and new artefact classes. The policy is **prospective only**; it does not require migration of any existing artefact.

### 5.1 Canonical gate-report root

```text
data/microstructure/gate-reports/<family-subdirectory>/<report-filename>
```

where `<family-subdirectory>` is one of:

- `raw/` — for any future re-run of the raw aggTrades eligibility gate;
- `normalized/` — for any future re-run of the derived-family eligibility gate;
- `features/` — for any future re-run of the feature-family eligibility gate;
- `labels/` — for any future re-run of the label-family eligibility gate;
- `<future-family>/` — for any future new gate class (lowercase, plural, underscore-free where possible).

The doubled `gate-reports/gate-reports/` path is **explicitly retired** for future raw-gate runs. A future Phase 4bb-F-implementation phase (if separately authorized) would fix the Phase 4bb-C orchestrator so that re-running the raw gate writes to `data/microstructure/gate-reports/raw/<report-filename>` instead of `data/microstructure/gate-reports/gate-reports/<report-filename>`.

### 5.2 Canonical successor-state root

```text
data/microstructure/successor-state/<artefact-filename>
```

A flat namespace, mirroring the existing Phase 4bg-B / Phase 4bi-D / Phase 4bj-G convention. No per-family subdirectory.

Rationale for keeping successor-state flat (and not introducing `successor-state/derived/`, `successor-state/features/`, `successor-state/labels/`): there are typically zero-to-one successor-state artefacts per family per stage marker, the filename's family + stage-marker + phase-id segments are already unambiguous, and a flat layout is consistent with the three existing artefacts.

### 5.3 Flat-vs-family-scoped policy

| Artefact class | Layout |
| -------------- | ------ |
| Gate reports | family-scoped (subdirectory per family) |
| Successor-state | flat (no subdirectory; filename carries the family + stage marker) |

This is the existing convention for three of the four gate-report classes (Phase 4bf, 4bi-B, 4bj-E) and all three successor-state classes. Phase 4bb-F simply formalises it and identifies the Phase 4bb-D raw-gate doubled-path case as the one exception that future repeats should fix.

### 5.4 Naming conventions

**Gate-report filename (forward canonical):**

```text
<dataset_family>__<dataset_version>__phase-<phase-id>__<unix_ms>__<short_commit>.json
```

- `<dataset_family>` — full family name, e.g. `microstructure_raw_aggtrades_v001`, `microstructure_normalized_aggtrades_v001`, `microstructure_features_aggtrades_v001`, `microstructure_labels_aggtrades_v001`.
- `<dataset_version>` — typically `v001`.
- `phase-<phase-id>` — explicit phase tag, e.g. `phase-4bb-d`, `phase-4bf`, `phase-4bi-b`, `phase-4bj-e`. Required.
- `<unix_ms>` — UTC unix millisecond timestamp at which the report was written.
- `<short_commit>` — first 12 characters of the writer's `code_commit_sha`.
- `.json` — file extension.

Phase 4bb-D and Phase 4bf were written before the `phase-<id>` segment became canonical. Their filenames omit the tag. They are valid evidence by their recorded paths and SHAs; they are NOT renamed by this policy. Any future re-run of the raw or derived gate at a new phase identity (if ever authorized) should follow the forward canonical with the phase tag.

**Successor-state filename (forward canonical, already in use):**

```text
<dataset_family>__<dataset_version>__<stage_marker>__phase-<phase-id>.json
```

- `<stage_marker>` — semantic marker, e.g. `stage3_research_eligible`, `stage5_research_ml_admissible`.
- `phase-<phase-id>` — explicit phase tag, e.g. `phase-4bg-b`, `phase-4bi-d`, `phase-4bj-g`. Required.

No `unix_ms` or `short_commit` segment in successor-state filenames because the artefact records its own `created_at_unix_ms` and `code_commit_sha` (and `base_main_commit_sha`) as JSON fields, and successor-state artefacts are intended to be one-per-(family, stage marker, phase) — not re-runnable in the same way a gate is.

### 5.5 Timestamp and commit-SHA conventions

- All `unix_ms` values are UTC milliseconds since the Unix epoch, taken at the moment of writing (after the gate has run and just before the file is finalised). Use the writer's wall clock; do not derive from the input artefact's `transact_time_ms`.
- All `short_commit` values are the first 12 hexadecimal characters of the writer's `code_commit_sha` (the `git rev-parse HEAD` of the branch the writer was invoked from).
- Successor-state JSON bodies must include `created_at_unix_ms`, `created_at_utc` (ISO 8601 with microseconds and trailing `Z`), `code_commit_sha` (full 40-char), and `base_main_commit_sha` (full 40-char) as top-level fields. The Phase 4bg-B / Phase 4bi-D / Phase 4bj-G artefacts already follow this pattern.

### 5.6 Sidecar conventions

For every new gate report or successor-state artefact:

- Sidecar path is the JSON path with the literal `.sha256` suffix appended (no other transformation of the JSON filename).
- Sidecar content is `<json-sha256>  <basename>\n` where `<json-sha256>` is the lowercase 64-character SHA256 hex of the JSON file bytes and `<basename>` is the JSON filename without directory components. Two spaces between the SHA and the basename (`sha256sum` standard). One trailing newline.
- Sidecar size is therefore `64 + 2 + len(basename) + 1` bytes.
- Sidecar must parse cleanly with a simple whitespace split on the first line.
- Sidecar must be written atomically via the same `tmp + os.replace` pattern as the JSON, in the same write transaction (write JSON, fsync, replace; then write sidecar, fsync, replace).

### 5.7 Refuse-overwrite expectations

Every writer must:

- check whether the target JSON path already exists; if so, raise an exception (e.g. `RawWriterAlreadyExistsError` / equivalent) and abort the write;
- check whether the target sidecar path already exists; if so, raise and abort;
- check whether a stale `.tmp` companion exists at the target path; if so, raise and abort;
- never overwrite a finalised report or sidecar.

### 5.8 Immutability expectations

Once a gate report or successor-state artefact is written and its sidecar is finalised, the JSON file is immutable. No rewrite, no in-place edit, no field "patch" is permitted. If a JSON later turns out to be wrong (e.g., a misrecorded `code_commit_sha`), the canonical remedy is **not** to rewrite — it is to write a new artefact at a new path (new `unix_ms`, new phase tag) and to record the correction in a tracked memo.

The Phase 4bj-G successor-state JSON's `code_commit_sha = 0a069e2...` field — which records the `main` HEAD that the Phase 4bj-G branch was created from rather than the branch commit (`d84d398`) that committed the surrounding docs — is the canonical example. The Phase 4bj-G merge-closeout §7 documents this as intended behaviour; the JSON is not rewritten.

### 5.9 Gitignore expectations

- `data/microstructure/` (and therefore every subpath, including `gate-reports/`, `successor-state/`, `labels/`, `features/`, `manifests/`, `raw/`, `normalized/`) must remain gitignored.
- Every writer must verify gitignore coverage of the target path before writing (e.g. via a static path-prefix assertion or via a `git check-ignore`-equivalent), and must abort the write if coverage is missing.
- No artefact under `data/microstructure/` is ever to be committed. This includes:
  - gate reports;
  - successor-state JSONs;
  - sidecars;
  - manifests;
  - manifest sidecars;
  - parquet files;
  - parquet sidecars;
  - raw `.zip` files;
  - any future artefact class.

### 5.10 Report-id conventions

For gate reports, the canonical report-id is the basename of the JSON file without the `.json` extension. That is:

```text
<dataset_family>__<dataset_version>__phase-<phase-id>__<unix_ms>__<short_commit>
```

This report-id is the value that tracked memos cite (e.g. Phase 4bj-E gate report id `microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5`). The report-id is also recorded inside the JSON body as a `report_id` field. The on-disk filename and the in-body `report_id` must match.

For successor-state artefacts, the canonical successor-id is the basename of the JSON file without the `.json` extension, e.g. `microstructure_labels_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bj-g`.

### 5.11 How to cite previous local gitignored artefacts in tracked docs

Tracked memos that cite a gate report or successor-state artefact must include:

- the full repository-relative path of the JSON;
- the full repository-relative path of the sidecar;
- the JSON SHA256 (full 64-char hex);
- the sidecar self-SHA256 if relevant for cross-verification, OR a statement that the sidecar parses to the JSON SHA bit-for-bit;
- the JSON size in bytes;
- the writer's `code_commit_sha`;
- the `created_at_unix_ms` if recorded inside the JSON;
- an explicit "(gitignored; NOT committed)" annotation.

This is the convention every existing tracked memo already follows (Phase 4bb-D, Phase 4bf, Phase 4bi-B, Phase 4bj-E for gate reports; Phase 4bg-B, Phase 4bi-D, Phase 4bj-G for successor-state).

### 5.12 How to handle existing artefacts that do not perfectly match the future policy

**The three existing gate reports without a `phase-<id>` tag in the filename** (Phase 4bb-D raw gate and Phase 4bf derived gate) **remain valid by their recorded paths and SHAs**. They are NOT renamed, copied, or moved by this policy. Their recorded paths and SHAs are the authoritative project record. If either of these gates is ever re-run under a new phase identity, the new run should follow the forward canonical (with `phase-<id>`).

**The Phase 4bb-D doubled-path artefact** remains valid at `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json`. It is NOT moved. If the raw gate is ever re-run, the Phase 4bb-C orchestrator should be fixed in a separately authorized implementation phase (Phase 4bb-F-implementation or equivalent) so the next run lands at `data/microstructure/gate-reports/raw/<canonical-filename>.json` instead. Until that fix happens, do **not** re-run the raw gate; if the operator wants to re-run, the orchestrator fix is the prerequisite.

**The three existing successor-state artefacts** (Phase 4bg-B, Phase 4bi-D, Phase 4bj-G) already match the forward canonical exactly. No action.

---

## 6. Backward compatibility policy

This section is binding on every future phase that touches gate-report or successor-state artefacts.

- **Existing Phase 4bb-D gate report** (`microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json`, SHA `96f09159…`, at the doubled `gate-reports/gate-reports/` path) is **NOT moved, copied, renamed, or deleted** by this memo or by any future phase that does not explicitly name "migrate the Phase 4bb-D doubled-path artefact" in its authorization prompt.
- **Existing Phase 4bf gate report** (`microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json`, SHA `dd4e0c1c…`, at `gate-reports/normalized/`) is **NOT moved, copied, renamed, or deleted**.
- **Existing Phase 4bi-B gate report** (`...phase-4bi-b__1778436978312__2bc026b4e0d9.json`, SHA `aa5d29c2…`, at `gate-reports/features/`) is **NOT moved, copied, renamed, or deleted**.
- **Existing Phase 4bj-E gate report** (`...phase-4bj-e__1778531608796__89cde8ad14b5.json`, SHA `b0b5405b…`, at `gate-reports/labels/`) is **NOT moved, copied, renamed, or deleted**.
- **Existing Phase 4bg-B successor-state** (`microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json`, SHA `8bcc7d01…`) is **NOT moved, copied, renamed, or deleted**.
- **Existing Phase 4bi-D successor-state** (`microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json`, SHA `8176aa3f…`) is **NOT moved, copied, renamed, or deleted**.
- **Existing Phase 4bj-G successor-state** (`microstructure_labels_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bj-g.json`, SHA `ce7d3917…`) is **NOT moved, copied, renamed, or deleted**.
- All existing artefacts remain valid project record at their recorded paths and SHAs. Every tracked memo that cites them remains valid.
- Future phases may follow the new canonical policy **prospectively**.
- Any migration / copy / rename / delete of any existing local artefact would require a **separate explicit operator authorization** that names the artefact and explains why migration is needed. Phase 4bb-F does NOT authorize migration.

---

## 7. Prospective implementation implications

This section identifies, for reference only, where any future implementation work would likely live. **Phase 4bb-F does not authorize any source-code change.** The locations below are descriptive, not prescriptive.

### 7.1 Gate-report writers

Future source-code work to align gate-report writers with the canonical policy would likely touch:

- `src/prometheus/research/microstructure/eligibility_gate.py` (Phase 4bb-C raw-gate orchestrator) — for the doubled-path fix. The function `run_eligibility_gate` currently composes `output_root / "gate-reports" / filename`; future fix would either (a) compose `output_root / filename` (caller supplies the family subdirectory explicitly) or (b) infer the family subdirectory from the dataset family and compose `output_root / "<family-subdir>" / filename`.
- `src/prometheus/research/microstructure/eligibility_report.py` — for the report-filename construction (the `report_id` builder). Future fix would add a `phase-<id>` segment to the report-id for forward canonical reports.
- The equivalent files for Phase 4bf (`derived_gate.py` / `derived_gate_report.py`), Phase 4bi-B (`feature_gate.py` / `feature_gate_report.py`), and Phase 4bj-E (`label_gate.py` / `label_gate_report.py`). These three already use family-scoped subdirectories and include `phase-<id>` in the filename (Phase 4bi-B and Phase 4bj-E only); only the Phase 4bf writer would need the `phase-<id>` segment added.

### 7.2 Successor-state writers

The three existing successor-state artefacts were written by per-phase ad-hoc scripts (Phase 4bg-B, Phase 4bi-D, Phase 4bj-G each used a one-shot deterministic helper that was deleted post-write). There is no shared successor-state writer module in `src/prometheus/`. Future code-level work could:

- introduce a `src/prometheus/research/microstructure/successor_state_writer.py` module with a `write_successor_state(input: SuccessorStateInput) -> SuccessorStateResult` function;
- enforce the forward canonical filename, sidecar format, refuse-overwrite, and immutability guarantees;
- accept a `family`, `version`, `stage_marker`, and `phase_id` and compose the path under `data/microstructure/successor-state/`.

This work is **not** authorized by Phase 4bb-F. It would belong in a future code phase whose authorization prompt explicitly names it.

### 7.3 Report-id constructors

A shared `report_id` constructor under `src/prometheus/research/microstructure/` would centralise the forward canonical filename pattern across the four gate-report writers and the future successor-state writer. Not authorized now.

### 7.4 Sidecar helpers

The four existing gate-report writers and the three existing successor-state ad-hoc writers each implement their own sidecar write. A shared `write_sha256_sidecar(json_path: Path) -> Path` helper would reduce duplication and ensure format uniformity. Not authorized now.

### 7.5 Path validation helpers

A shared `assert_under_data_microstructure(path: Path) -> None` helper that confirms a target path is under `data/microstructure/` (and therefore gitignored by `.gitignore:85`) would centralise the gitignore-coverage assertion. Phase 4aw `raw_writer.py` already has `assert_path_under_data_microstructure(...)` for the raw-archive writer; the same pattern could extend to the gate writers and the future successor-state writer. Not authorized now.

### 7.6 Tests

Future tests for the writers would assert:

- target path resolves under `data/microstructure/`;
- target path is gitignored;
- refuse-overwrite semantics for both JSON and sidecar;
- sidecar bytes match the canonical `<sha>  <basename>\n` format;
- the on-disk JSON SHA matches the in-body `report_id`'s `<short_commit>` segment when applicable;
- writing fails closed on disk-full, permission-denied, or path-not-resolvable errors.

Not authorized now.

---

## 8. Decision options

Phase 4bb-F evaluated five options for the path-hygiene problem.

### Option A — remain paused, no path policy

Do nothing. Leave path conventions as they are. Risk: a future operator who re-runs the raw gate will write a second doubled-path artefact, and the project record continues to carry the Phase 4bb-E §15-documented anomaly indefinitely. Acceptable as a default but does not extract the cleanup-memo value the operator authorized this phase to produce.

### Option B — docs-only canonical path policy, prospective only

Author a memo (this memo) that records the canonical path policy for all future gate-report and successor-state writers, leaves every existing local artefact untouched, and does not authorize any source-code change. The next operator-authorized phase (whether a code-fix phase, a label-evaluation phase, or any successor) consults this memo for the canonical convention. **Recommended.**

### Option C — code + docs helper update in a later phase

A separately authorized future phase implements the source-code fixes identified in §7 (orchestrator path composition, shared sidecar helper, shared path-validation helper, shared report-id constructor, tests). This phase would build on Phase 4bb-F's locked policy. Acceptable as a future option but **not authorized by Phase 4bb-F**. Phase 4bb-F is the docs prerequisite for Option C; the operator may authorize Option C at any time after Phase 4bb-F is merged.

### Option D — migrate existing local artefacts

Move, copy, or rename one or more existing local gitignored artefacts to match the canonical policy. Specifically, move the Phase 4bb-D doubled-path report from `data/microstructure/gate-reports/gate-reports/...` to `data/microstructure/gate-reports/raw/...`. **NOT recommended; NOT authorized by Phase 4bb-F.** Every existing tracked memo cites the existing path and SHA; moving the artefact would invalidate the path citations (the SHA would survive but the recorded path would no longer resolve). The cost of migration is higher than the cost of leaving the existing artefact at its existing path.

### Option E — proceed to label evaluation / ML / strategy

**Forbidden / not recommended.** Phase 4bb-F is not the right phase to make a label-evaluation, ML, strategy, backtest, acquisition, paper / shadow, live-readiness, deployment, or exchange-write decision. Those are M0 admissibility decisions per Phase 4ak and require independent operator authorization following separate authorization prompts.

---

## 9. Recommendation

**Option B — docs-only canonical path policy, prospective only.**

This memo (Phase 4bb-F) is the path-policy lock. It records the canonical conventions in §5, the backward compatibility constraints in §6, and the prospective implementation implications in §7 for future reference. No existing artefact is touched. No source code is changed. No data is acquired. No gate is re-run.

The operator may, at any time after Phase 4bb-F is merged, authorize a separate Option C code-fix phase that applies the canonical conventions to the four existing writers (and introduces a shared successor-state writer if desired). Option C is **not** authorized by Phase 4bb-F.

Recommended state after Phase 4bb-F: **remain paused.**

---

## 10. Strict non-authorizations

Phase 4bb-F does **NOT** authorize:

- rerunning any gate (raw, derived, feature, or label);
- creating any new gate report;
- creating any new successor-state artefact;
- moving, copying, renaming, or deleting any existing local artefact;
- modifying any manifest (raw, derived, feature, or label);
- flipping `research_eligible` on any manifest;
- transitioning `eligibility_gate_status` on any manifest;
- changing `chronological_split_policy` on any manifest;
- modifying any sidecar;
- modifying any parquet file (label parquet, feature parquet, normalized parquet, raw `.zip`);
- modifying any prior gate report;
- modifying any prior successor-state artefact;
- modifying source code, tests, scripts, configurations, `.gitignore`, `pyproject.toml`, `README.md`, or MCP files;
- ML implementation;
- ML training;
- ML architecture design;
- feature ranking;
- meta-labeling;
- strategy creation;
- signal computation;
- backtesting;
- backtest execution;
- data acquisition (additional aggTrades / 5m / 1m / tick / mark-price / order-book);
- paper / shadow;
- live-readiness;
- deployment;
- production keys;
- authenticated APIs;
- private endpoints;
- user stream;
- live WebSocket implementation;
- MCP;
- Graphify;
- `.mcp.json`;
- credentials;
- exchange-write;
- Phase 4bb-G — Raw Manifest Successor-State Recording;
- Phase 4bj-H or any label-evaluation phase;
- Phase 5;
- Phase 4 canonical;
- any other successor phase.

Any future phase requires a separately authorized authorization prompt that satisfies the Phase 4bk-A `phase-prompt-template.md`.

---

## 11. Retained verdict ledger (preserved verbatim)

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED per Phase 3t
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

No verdict is revised by Phase 4bb-F.

---

## 12. Preserved project locks

- §11.6 = 8 bps per side
- Round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8 — stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 — break-even / EMA slope / stagnation governance
- Phase 4j §11 — metrics OI-subset partial-eligibility rule
- Phase 4k V2 backtest-plan methodology
- Phase 4p G1 strategy-spec methodology
- Phase 4q G1 backtest-plan methodology
- Phase 4v C1 strategy-spec methodology
- Phase 4w C1 backtest-plan methodology
- Phase 4ak M0 twelve-clause gate
- Phase 4ak post-null cooldown rule
- Phase 4ak cooled-down families list
- Phase 4ak memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant

Every prior phase's recorded outcomes (Phase 4am through Phase 4bj-G) preserved verbatim.

No project lock is loosened, modified, or amended by Phase 4bb-F.

---

## 13. Current-project-state update

Phase 4bb-F adds:

- one narrow Phase 4bb-F narrative paragraph in `docs/00-meta/current-project-state.md` (inserted above the Phase 4bj-G narrative paragraph);
- one new "Current phase:" block summarising Phase 4bb-F; the prior Phase 4bj-G "Current phase:" block is demoted to historical context verbatim with an appropriate bridge label.

The current-project-state update is narrow and consistent with the process standards. It preserves:

- Phase 4bb-F is path-governance only;
- no local artefact moved, copied, renamed, deleted, or created;
- no gate re-run;
- no manifest mutation;
- no ML / strategy / backtest / acquisition / paper-shadow / live / exchange-write authorized;
- recommended state remains paused unless the operator separately authorizes a future phase.

---

## 14. Validation

| Check | Result |
| ----- | ------ |
| `git diff --check` | clean |
| `git status --short` | only pre-existing untracked entries (`.claude/scheduled_tasks.lock`, `data/research/`) plus the new Phase 4bb-F memo + narrow `current-project-state.md` update |
| `find data/microstructure/gate-reports/ -type f` | inventory matches §3 verbatim; no new file created |
| `find data/microstructure/successor-state/ -type f` | inventory matches §3 verbatim; no new file created |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `ruff` / `mypy` / `pytest` | not rerun — Phase 4bb-F modifies zero source code and zero tests |

Phase 4bb-F introduces zero new test regressions and modifies no production code.

---

## 15. Closeout and recommended state

Phase 4bb-F is a docs-only path-governance memo. It locks the prospective canonical path policy for all future gate-report and successor-state writers. It does not migrate any existing artefact, does not authorize any source-code change, and does not authorize any successor phase.

**Recommended state: remain paused.**

**No successor phase is authorized by Phase 4bb-F.**

The next sensible step is operator-driven. Conditional next options (none authorized by Phase 4bb-F):

- a future operator-authorized merge of this Phase 4bb-F branch into `main` with a Phase 4bb-F merge-closeout;
- future code + docs **Option C / Phase 4bb-F-implementation** (orchestrator path-composition fix, shared sidecar helper, shared path-validation helper, shared report-id constructor, tests);
- future docs-only or docs-and-local-gitignored-output **Phase 4bb-G** — Raw Manifest Successor-State Recording (would extend the successor-state pattern to the raw aggTrades family; entirely independent of Phase 4bb-F);
- future label-evaluation phases (would require independent M0 admissibility per Phase 4ak; not authorized here).
