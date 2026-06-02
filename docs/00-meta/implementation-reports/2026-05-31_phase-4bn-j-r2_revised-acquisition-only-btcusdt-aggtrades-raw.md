# Phase 4bn-J-R2 — Revised Acquisition-Only BTCUSDT aggTrades Raw Retry

**Phase 4bn-J-R2 is branch-complete only by this work; not merged into
main; not project-complete.** It is an acquisition-only / raw-only /
local gitignored data-artefact generation / integrity-bound execution
phase (Tier 1 Full Phase per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3), executed under
the revised acquisition-only retry recommended by Phase 4bn-J-R1.

- **Branch:** `phase-4bn-j-r2/revised-acquisition-only-btcusdt-aggtrades-raw`.
- **Base `main` SHA:** `03dc876cab9ecd3db982beb0ba51712858cbdf9c`
  (`docs(phase-4bn-j-r1): finalize merge closeout shas`; pre-branch
  `main == origin/main == HEAD` verified in sync; Phase 4bn-J-R1
  merge-closeout `bbe8b46`, merge `f63ded8`, and branch `3f792a6` all
  present on `main`).
- **Active local repo path:** `D:\Prometheus`.

---

## 1. Purpose

Execute the revised acquisition-only retry authorized by the Phase
4bn-J-R1 *Workspace Relocation + Raw-Only Acquisition Cap Amendment*.
This phase acquires **only** the 275 new pre-v002 raw BTCUSDT Binance
USDⓈ-M futures aggTrades daily archives covering UTC dates **2024-03-01
through 2024-11-30 inclusive**, preserving the existing v002 terminal
window (2024-12-01 .. 2025-02-28) and the sealed v002 test split
(2025-02-14 .. 2025-02-28) untouched. It is raw-only: it does not
normalize, derive features, derive labels, run ML, run diagnostics, run
strategy / signals / PnL / backtests, migrate storage, create a
database, compact Parquet, create v003, or authorize any successor.

## 2. Authority and repository state

- Authorized by the operator as the Phase 4bn-J-R1 recommendation
  `RECOMMEND_AUTHORIZE_REVISED_ACQUISITION_ONLY_RETRY__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- Repository state verified before branching:
  - `HEAD == main == origin/main == 03dc876cab9ecd3db982beb0ba51712858cbdf9c`;
  - latest commit `docs(phase-4bn-j-r1): finalize merge closeout shas`;
  - Phase 4bn-J-R1 merge-closeout `bbe8b46`, merge `f63ded8`, branch
    `3f792a6` all present on `main`;
  - only untracked transient: `.claude/scheduled_tasks.lock`;
  - gitignored `data/microstructure/` and `data/research/` namespaces
    present locally and uncommitted;
  - GitHub remote `origin` → `https://github.com/jpedrocY/Prometheus.git`.
- The stopped Phase 4bn-J branch
  `phase-4bn-j/acquisition-only-btcusdt-aggtrades-12m` was **not** merged,
  resumed, deleted, or treated as branch-complete. This retry started
  fresh from current `main`.

## 3. Phase type and strict scope

Acquisition-only / raw-only / integrity-bound. **Raw zip archives are
canonical for this phase.** This phase MUST NOT and DID NOT: normalize
data; derive features; derive labels; run ML; run diagnostics; run
strategy, signals, PnL, or backtests; migrate storage; create a
database; compact Parquet; create v003; authorize any successor. No
ETHUSDT, mark-price, spot, cross-venue, order-book, tick, or extra
horizons. No post-v002 dates.

## 4. Evidence base and input boundary

Read read-only before execution: the Phase 4bn-J-R1 amendment memo and
closeout, the Phase 4bn-J stop report, the Phase 4bn-I execution plan,
the Phase 4bn-H readiness memo, the relevant `docs/04-data/*` and
`docs/08-architecture/database-design.md` docs, and the committed
acquisition tooling
(`scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`,
`scripts/phase4az_acquire_btcusdt_aggtrades_archive.py`,
`src/prometheus/research/microstructure/aggtrades.py`,
`src/prometheus/research/data/binance_bulk.py`) plus their tests. The
existing v002 terminal window and the sealed v002 test split were **not**
opened, inspected, summarized, hashed, counted, sampled, or read.

## 5. Phase 4bn-J-R1 decision carried forward

Phase 4bn-J-R1 recorded that the source-policy preflight PASSED in the
stopped Phase 4bn-J attempt (committed tooling resolves the source
contract unambiguously) and that the only binding issue was an
unrealistically low, scope-confused 5 GiB disk cap. It amended the
**raw-only** acquisition disk cap to **10 GiB warning / 25 GiB hard**
additional local raw footprint for this retry only, kept the runtime cap
(2 h warning / 4 h hard), and preserved every other Phase 4bn-I boundary
(envelope, sealed-test preservation, storage posture, manifest / sidecar
policy, 25 fail-closed stop conditions). This phase executes exactly
within that amended contract.

## 6. Exact revised acquisition contract

- Symbol: BTCUSDT only. Market: Binance USDⓈ-M futures. Family:
  aggTrades only.
- New acquisition segment: **2024-03-01 .. 2024-11-30 inclusive UTC =
  275 days**.
- Full intended envelope: 2024-03-01 .. 2025-02-28 inclusive UTC (only
  the 275 pre-v002 days fetched here).
- Existing v002 terminal window 2024-12-01 .. 2025-02-28: not
  re-downloaded, not overwritten, not read.
- Existing v002 sealed test split 2025-02-14 .. 2025-02-28: untouched.
- The new script rejects any date `>= 2024-12-01`, `< 2024-03-01`, or
  `> 2024-11-30`; rejects any symbol other than BTCUSDT; rejects any
  family other than aggTrades; rejects ETHUSDT / mark-price / spot /
  order-book / tick / cross-venue / extra-horizon / v003 scope tokens.

## 7. Source-policy confirmation

Confirmed before fetching any archive, from committed tooling and a
HEAD-only / CHECKSUM-only probe (no archive bodies downloaded during the
source check):

| Field | Value |
|---|---|
| Source class | `public_unauthenticated_daily_archive` |
| Base host (allowlisted, HTTPS only) | `data.binance.vision` |
| Archive URL pattern | `https://data.binance.vision/data/futures/um/daily/aggTrades/BTCUSDT/BTCUSDT-aggTrades-{YYYY-MM-DD}.zip` |
| Checksum URL | same + `.CHECKSUM` |
| Checksum format | `<sha256hex>  <filename>` (exactly two spaces) |
| Integrity order | CHECKSUM → zip → SHA256 match → `testzip()` → bounded row-sample validation (Phase 4ax validator) |
| Sidecar | Phase 4bb-F canonical `<sha>␠␠<basename>\n` (LF, no BOM) |
| Manifest seed | `research_eligible=false`, `eligibility_gate_status="pending"` |

The empirical probe for `2024-03-01` returned HTTP 200 with
`Content-Length = 18,575,092` for the zip and a 200 CHECKSUM companion
with body `8851c90b6e8dc6d3c1af0226fd3cf91d537fb5d028ef8c04c95d486335bfdded  BTCUSDT-aggTrades-2024-03-01.zip`,
confirming the host, URL pattern, checksum companion, and two-space
checksum format. **No credentials, no private endpoint, no authenticated
API, no WebSocket, no user stream, no `.env`, no `.mcp.json`, no MCP, no
Graphify** are required or used. Source-policy preflight: **PASS**.

## 8. Acquisition implementation path

A new bounded raw-only acquisition script was written —
`scripts/phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py` — because
the locked `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py` is
hardcoded to the 90-day v002 range and must not be repointed. The new
script reuses the proven Phase 4bl-C patterns verbatim: host allowlist;
URL/path pattern; CHECKSUM-first ordering; SHA256 verification;
`zipfile.testzip()`; bounded row-sample validation via the Phase 4ax
`validate_aggtrade_payload`; Phase 4bb-F canonical sidecars;
refuse-overwrite; non-eligible raw manifest seed. It adds: a hard
segment date guard (rejects any date `>= 2024-12-01` and any date
outside 2024-03-01 .. 2024-11-30); BTCUSDT-only and aggTrades-only
guards; a forbidden-scope-token denylist; the amended raw-only disk cap
(10 GiB warning / 25 GiB hard) and runtime cap (2 h / 4 h) enforced at
per-day boundaries; and a HEAD-only `--preflight` footprint estimate
that downloads no archive bodies. It writes a **distinct, phase-scoped
segment manifest** (`microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`)
and never mutates the published `microstructure_raw_aggtrades_v001__v002.json`
manifest. The script is Python stdlib only (`urllib`, `zipfile`, `csv`,
`hashlib`, `json`, …) plus the Phase 4ax validator import; no
`requests` / `httpx` / `aiohttp` / `websockets`.

## 9. Disk-footprint and runtime preflight

- **Disk preflight (HEAD only, no bodies):** the script's `--preflight`
  issued 275 allow-listed HTTP HEAD requests and summed `Content-Length`
  = **5,140,686,147 bytes ≈ 4.79 GiB**, average ≈ 18.69 MB/day. This is
  **below** the 10 GiB warning threshold and **well below** the 25 GiB
  hard cap. (The Phase 4bn-J stop report's 5.5–7.5 GiB range was an
  event-weighted 7-day sample; the full 275-day HEAD sum is the accurate
  figure.) Because the estimate was below the hard cap, acquisition
  proceeded with per-day cap enforcement.
- **Runtime preflight:** transfer of ~4.79 GiB across 275 days × 2 HTTP
  round-trips was expected within the 4 h hard cap; per-day runtime was
  cap-enforced during the run.

## 10. Raw artefacts created

- Acquired-verified daily zip archives: **275 / 275** (every day
  `acquired_verified`; 0 missing, 0 checksum mismatch, 0 decompression
  failure, 0 row-sample failure, 0 retry-exhausted, 0 cap-skip).
- Total raw footprint measured: **5,140,686,147 bytes (4.788 GiB)** —
  matching the HEAD-only preflight estimate exactly.
- Total aggTrade rows inventoried (bounded inventory pass):
  **400,001,695**.
- Local gitignored layout (canonical Phase 4bb-F):
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/{YYYY}/{MM}/BTCUSDT-aggTrades-{date}.zip`
  with a paired `.sha256` sidecar per archive, for each day in
  2024-03-01 .. 2024-11-30. All outputs are gitignored and uncommitted.

## 11. Sidecars and manifests

- Every generated raw archive has a canonical Phase 4bb-F SHA256
  sidecar: `<sha256>␠␠<basename>\n` (two-space separator, LF only, no
  BOM, no extra fields). Refuse-overwrite is enforced; existing
  artefacts are never silently overwritten.
- A phase-scoped **segment** manifest + acquisition log (each with a
  `.sha256` sidecar) were written under
  `data/microstructure/manifests/`:
  - manifest: `microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`
    (sha256 `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`);
  - acquisition log:
    `microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2_acquisition_log.json`
    (sha256 `0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`).
- The manifest records: `phase=4bn-J-R2`; base SHA
  `03dc876cab9ecd3db982beb0ba51712858cbdf9c`; symbol BTCUSDT; market
  `binance_usdm_futures`; family aggTrades; acquired segment
  2024-03-01 .. 2024-11-30; full intended envelope 2024-03-01 ..
  2025-02-28; existing v002 terminal window 2024-12-01 .. 2025-02-28
  (`read=false`, `overwritten=false`, `redownloaded=false`); existing
  v002 sealed test split 2025-02-14 .. 2025-02-28 (`touched=false`);
  `test_holdout_touched=false`; `test_rows_loaded=0`;
  `research_eligible=false`; `eligibility_gate_status="pending"`; source
  policy / URL pattern / archive naming convention; per-file inventory
  with each output file name and SHA256; raw disk footprint measured;
  runtime measured; warnings crossed; `hard_caps_crossed=false`;
  fail-closed stop conditions triggered (none); and the explicit
  non-authorization envelope. The published
  `microstructure_raw_aggtrades_v001__v002.json` manifest was **not**
  read or mutated.

## 12. Integrity checks

For every acquired day, in order: download the `.CHECKSUM` companion;
download the zip; verify the local SHA256 equals the companion value
bit-for-bit; run `zipfile.testzip()`; run bounded row-sample validation
(head 100 + tail 100 + up to 100 deterministic middle rows) through the
Phase 4ax `validate_aggtrade_payload`. Any mismatch fails that date
closed without overwriting existing files. Result: all 275 acquired days
passed checksum, decompression, and row-sample validation (400,001,695
aggTrade rows inventoried across the segment).

## 13. Sealed-test preservation

The existing v002 sealed test split 2025-02-14 .. 2025-02-28 was never
read, counted, sampled, hashed, summarized, inspected, or used for any
reason. The script's segment date guard makes any date `>= 2024-12-01`
unreachable, so the sealed split and the entire v002 terminal window are
structurally untouchable by this tooling. Phase 4bn-B
`test_rows_loaded: 0` and the `iter_partitions(split="test", ...)`
always-raise pattern are preserved. No new model-evaluation holdout and
no ML split were defined; `chronological_split_policy` was not
transitioned. Any future holdout/split policy for the expanded envelope
requires a separate docs-only memo before any ML or diagnostics.

## 14. Fail-closed stop conditions

The 25 fail-closed stop conditions from the Phase 4bn-I contract (as
amended raw-only by Phase 4bn-J-R1) were preserved and enforced in code:
source/URL/host mismatch, public-source unavailability, missing archive,
duplicate/overwrite attempt, unexpected schema, intra-archive timestamp
monotonicity / gap / duplicate-key anomalies surfaced by the validator,
sidecar format mismatch, SHA256 mismatch, manifest validation failure,
10 GiB raw warning, 25 GiB raw hard cap, 2 h runtime warning, 4 h runtime
hard cap, any attempt to read the v002 holdout, any ML-split creation,
any ML/diagnostics/strategy/PnL/backtest, any DuckDB/SQLite/database
creation, any Parquet compaction, any `data/microstructure` or
`data/research` commit, any credential/private-endpoint/WebSocket/user-
stream/`.env`/`.mcp.json`/MCP/Graphify usage, any manifest eligibility
transition, any deviation from the exact 2024-03-01 .. 2024-11-30 range,
and any ETHUSDT/v003/mark-price/spot/cross-venue/order-book/tick/extra-
horizon requirement. **Fail-closed stop conditions triggered: none. Hard
caps crossed: false. Warning thresholds crossed: none** — runtime was
2,051 s (≈34 min, under the 2 h warning) and raw footprint 4.788 GiB
(under the 10 GiB warning).

## 15. Validation

- `ruff check` on the new script and the new test module: **pass** (after
  fixing SIM108/SIM300/UP037).
- `pytest tests/research/microstructure/test_phase4bn_j_r2_acquisition_script.py`:
  **117 passed** (all offline; no network; no local data read; no
  sealed-test read).
- Existing `test_phase4bl_c_acquisition_script.py`: still passing (no
  regression; the locked script was not modified).
- `mypy` gate is scoped to `src/prometheus` only (`pyproject.toml`
  `[tool.mypy] files = ["src/prometheus"]`); the new acquisition script
  lives under `scripts/` like the locked Phase 4bl-C script and is
  outside the type-gate (the locked Phase 4bl-C script produces the same
  `scripts/`-only mypy notes when run directly).
- `git diff --check`: clean.
- `git check-ignore -v` confirms `data/microstructure/` and
  `data/research/` are gitignored; no data artefact staged.

## 16. Boundary confirmations

- no source code (`src/prometheus`) modified;
- no locked prior-phase script modified (the new script is additive);
- no existing test modified;
- no config / `.gitignore` / `pyproject.toml` / `README.md` / MCP file
  modified;
- no `data/microstructure/` or `data/research/` artefact committed;
- existing v002 terminal window and sealed test split not read / counted
  / sampled / hashed / summarized / inspected / mutated;
- no published v002 manifest mutated; no `research_eligible` flipped; no
  `eligibility_gate_status` transitioned; no `chronological_split_policy`
  changed;
- no successor-state / gate-report artefact mutated;
- no `.duckdb` / `.sqlite` / database created; no Parquet compaction; no
  normalized / feature / label artefact created; no v003 created;
- no ML / diagnostics / strategy / signals / PnL / backtest run;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used; no
  authenticated / private endpoint / WebSocket / user stream contacted;
  only `data.binance.vision` public archive URLs were fetched;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).

## 17. Result

**Result state: `ACQUISITION_SUCCEEDED__RAW_ARTEFACTS_LOCAL_GITIGNORED__REMAIN_PAUSED`.**
All 275 pre-v002 days were acquired and integrity-verified; raw artefacts
+ sidecars + the segment manifest/log live locally under the gitignored
`data/microstructure/` tree; no hard cap and no warning threshold was
crossed; the project remains paused.

## 18. Decision

**`RECOMMEND_AUTHORIZE_RAW_ARCHIVE_ELIGIBILITY_GATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`** —
acquisition succeeded and raw artefacts / manifest / sidecars were
created, so the recommended (but not authorized) next option is a future
raw archive eligibility gate, subject to separate operator authorization.
No ML / diagnostics / normalization / feature / label / strategy / PnL /
backtest / storage-migration / database / Parquet-compaction / v003 is
recommended or authorized. No successor is authorized from inside Phase
4bn-J-R2.

## 19. Recommended state and successor options

**Remain paused.** Phase 4bn-J-R2 is branch-complete only by this work;
not merged into main; not project-complete. Per the
`phase-workflow-standard.md` rule it is not project-complete until a
separately authorized merge phase records its merge-closeout on `main`
per `merge-closeout-standard.md` (Tier 1). The operator may equivalently:
remain paused; request a merge prompt for Phase 4bn-J-R2; separately
authorize a raw archive eligibility gate (the recommendation, if
acquisition succeeded); separately authorize a docs-only source-policy
documentation memo; separately authorize a docs-only derived-stack
storage-budget memo before any normalization / features / labels; or
reject further ML-baseline successors and close the ML arc. **No ML /
diagnostics / normalization / feature / label / strategy / PnL / backtest
/ storage-migration / database-creation / Parquet-compaction / v003 /
paper / shadow / live / exchange-write option is valid from this state
unless separately authorized after this branch is merged.** No successor
is authorized from inside Phase 4bn-J-R2.

## 20. Explicit non-authorizations

No ML was trained; no model scoring was performed; no predictions were
generated; no diagnostics were run; no normalization was run; no features
were derived; no labels were derived; no strategy / signal / PnL /
backtest work was performed; no storage migration occurred; no database
was created; no Parquet was compacted; no v003 dataset was created; no
test holdout was touched; no manifest eligibility transition occurred; no
`data/research` artefacts were created or committed; no
`data/microstructure` artefacts were committed; and no paper / shadow /
live / exchange-write / credentials / MCP / Graphify work was authorized.
Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock is preserved verbatim.

## 21. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: a new Phase
4bn-J-R2 prose paragraph and a new `Current phase:` block were added;
prior Phase 4bn-A … 4bn-J-R1 paragraphs and `Current phase:` blocks are
preserved as labelled historical context. Phase 4bn-J-R2 is recorded as
branch-complete only, not merged, not project-complete, with the
acquisition result, exact raw outputs, all non-authorizations,
recommended state (remain paused), and the note that a raw archive
eligibility gate is recommended but **not authorized**.
