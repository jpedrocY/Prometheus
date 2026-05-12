# Phase 4bl-A — Multi-Day aggTrades Expansion Requirements Memo

**Phase identity:** Phase 4bl-A — Multi-Day aggTrades Expansion Requirements Memo (docs-only).
**Date:** 2026-05-12.
**Phase type:** docs-only requirements / scope / governance memo.
**Branch:** `phase-4bl-a/multi-day-aggtrades-expansion-requirements-memo`.
**Base:** `main` at `c120450b87918d104474e6d1bb88b6fa30132f34` (Phase 4bj-K SHA-chain-fixup commit on top of the Phase 4bj-K merge-closeout `0074f696d5f4e9bd7fccf665d6742c77af2edaa2`).
**Status:** drafted; pending operator review.

A note on the SHA-chain pattern: the Phase 4bj-K merge-closeout itself anchored its §2 final-`main` value at the merge-closeout commit `0074f69`. The one-commit fixup on top of that anchor (commit `c120450`) only records the final-`main` SHA back into §2 of the Phase 4bj-K merge-closeout; it does not change Phase 4bj-K lifecycle semantics. Phase 4bl-A branches from `c120450` because that is the post-fixup `main` state; the canonical "Phase 4bj-K project-complete" anchor remains the merge-closeout commit (`0074f69`).

---

## 1. Phase identity

- **Phase name:** Phase 4bl-A — Multi-Day aggTrades Expansion Requirements Memo.
- **Phase type:** docs-only requirements / scope / governance memo.
- **Branch:** `phase-4bl-a/multi-day-aggtrades-expansion-requirements-memo`.
- **Base SHA:** `main` at `c120450b87918d104474e6d1bb88b6fa30132f34`.
- **Predecessor anchor:** Phase 4bj-K merge-closeout `0074f696d5f4e9bd7fccf665d6742c77af2edaa2` (project-complete).
- **Authorization:** explicit operator authorization for Phase 4bl-A only.

Phase 4bl-A is **strictly docs-only**. It does **not**:

- acquire data of any kind;
- download files;
- call public endpoints;
- call Binance APIs;
- call authenticated APIs;
- call private endpoints;
- open user streams or WebSockets;
- create or read credentials, `.env`, or `.mcp.json`;
- enable MCP or Graphify;
- create raw, normalized, derived, feature, label, gate-report, successor-state, split, segmentation, or diagnostic artefacts;
- create, modify, move, copy, rename, or delete any file under `data/microstructure/`;
- rerun any eligibility gate;
- run kernels, normalizers, or processing scripts;
- read or process the label parquet beyond documentation-level reference already recorded in repo docs;
- compute label statistics;
- execute diagnostics;
- train ML, design ML architecture, rank features, or create meta-labeling;
- create a strategy, compute signals, or run backtests;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output;
- modify any source code, test, script, `pyproject.toml`, `README.md`, `.gitignore`, or MCP file;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any actual manifest;
- modify project locks, retained verdicts, or M0 governance;
- authorize Phase 4bl-B, Phase 5, or any successor phase.

Tracked changes by Phase 4bl-A are exactly three new docs (this memo + the Phase 4bl-A closeout + narrow paragraph + "Current phase:" block update in `docs/00-meta/current-project-state.md`). No `data/microstructure/` artefact, no local gitignored file, no source / test / script / config / pyproject / README / `.gitignore` / MCP file is created or modified.

---

## 2. Pre-state and motivation

### 2.1 Current research cell

The current microstructure aggTrades research arc has exactly one governed research cell:

| Property | Value |
| --- | --- |
| Source | Binance USDⓈ-M Futures public aggTrades daily archive (`data.binance.vision`) |
| Symbol | `BTCUSDT` |
| Date | `2025-01-15` (one UTC day) |
| Raw row count | 1,681,098 |
| Pipeline | raw → normalized / derived → feature → label, all four layers completed and gated |
| Label family | `microstructure_labels_aggtrades_v001` |
| Label row count | 1,681,098 |
| Label column count | 39 |
| Label horizons | 1s, 5s, 15s, 60s |
| Label parquet SHA256 | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label manifest SHA256 | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| `label_config_hash` | `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00` |
| `invalid_price_row_count` | 0 |
| `censored_per_horizon` | `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` |
| Label manifest `research_eligible` | `false` (unchanged) |
| Label manifest `eligibility_gate_status` | `"pending"` (unchanged) |
| Label manifest `chronological_split_policy` | `"not_yet_defined"` (unchanged) |

The Phase 4bj-E label-family eligibility gate produced a PASS report (72 / 72) at SHA256 `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0`. The Phase 4bj-G label-family successor-state JSON (`ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5`) records Stage-5 research / ML admissibility at policy level. The Phase 4bj-J no-split determination JSON (`7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6`) records the Option D no-formal-split policy for the locked single-day cell.

### 2.2 Phase 4bj-H — label-evaluation / chronological split boundary

Phase 4bj-H (project-complete) recorded the **label-evaluation / chronological split boundary** at policy level. Label evaluation is a future controlled diagnostic activity, never a strategy or signal. No empirical label evaluation may run before a chronological split policy is recorded as a sibling artefact.

### 2.3 Phase 4bj-I — Option D no-formal-split policy

Phase 4bj-I (project-complete) recorded the **Option D recommended policy**: the single-day BTCUSDT 2025-01-15 label cell is **insufficient** for formal train / validation / test partitioning and must remain unsplit until multi-day data exists. Train / validation / test vocabulary is forbidden for the single-day cell.

### 2.4 Phase 4bj-J — no-split determination artefact

Phase 4bj-J (project-complete) operationalized the Phase 4bj-I Option D decision into exactly one machine-readable sibling no-split determination JSON, gitignored / not committed. The original label manifest remains byte-identical and the `chronological_split_policy` field on the manifest remains `"not_yet_defined"`.

### 2.5 Phase 4bj-K — label diagnostic study plan

Phase 4bj-K (project-complete) recorded a docs-only predeclared diagnostic study plan for any future Phase 4bj-L-equivalent label diagnostic execution phase. The plan does not execute diagnostics. It identifies two conditional next options:

1. Phase 4bj-L-equivalent — descriptive full-cell label diagnostic execution on the locked single-day cell (low-stakes sanity check).
2. **Multi-day aggTrades expansion requirements memo** (the present Phase 4bl-A), recognised as the more meaningful research path.

### 2.6 Why one-day diagnostics are low-stakes sanity checks only

The locked one-day cell can only support **descriptive characterization of itself**. It cannot characterize BTCUSDT generally, cannot characterize other days or symbols, cannot characterize crypto microstructure broadly, and cannot support out-of-sample claims. Empirical evidence from this cell is structurally bounded to confirming that the artefact pipeline produced an internally consistent label parquet. That is valuable as pipeline-proving evidence; it is not enough for ML, strategy, backtest, or live-readiness discussions.

### 2.7 Why multi-day data is required before meaningful empirical research

Meaningful empirical research in the Prometheus arc requires, at minimum:

- a **chronological out-of-sample period** for any model fit / score / select decision;
- a **non-trivial number of distinct UTC days** so that intraday regime variation does not dominate the entire sample;
- coverage of **multiple weekdays and at least one weekend** so that within-week effects are not silently treated as universal;
- coverage of **at least one high-volatility day and at least one quiet day** so that regime mix is not cherry-picked;
- enough rows per horizon × regime cell to support a **PBO / DSR / CSCV** sample-size floor (Phase 4k / 4q / 4w precedent);
- enough rows to support an **opportunity-rate viability floor** (Phase 4u / 4v / 4w / 4y precedent) without being structurally sparse;
- a **predeclared chronological split policy** with strict purge / embargo at the maximum label horizon (Phase 4bj-I §5 60s policy preserved).

A one-day cell satisfies none of these in any meaningful sense. Phase 4bj-I correctly recorded the cell as insufficient for formal split. Phase 4bj-K correctly recorded the cell as insufficient for anything beyond descriptive sanity checks.

The next coherent research step is to define what multi-day expansion would look like, before any acquisition is performed. Phase 4bl-A is that step.

---

## 3. Requirements question

Phase 4bl-A answers four distinct requirements questions at memo level only.

### 3.1 What minimum data expansion is needed before formal chronological split policy can be meaningful?

A meaningful chronological split policy requires at least:

- enough distinct UTC days to support a **train block + a validation block + an out-of-sample test block**, each non-trivial in size;
- enough days inside each block to absorb day-of-week and intra-week effects (at least one full week per block in a contiguous design, or a sampled equivalent that covers both weekday and weekend behaviour);
- enough days **after** the train block to leave at least one purge / embargo gap and a meaningful out-of-sample block;
- enough days so that any single high-volatility day cannot bias an entire block's statistics;
- a contiguous date list (preferred) or a deterministically predeclared sampled date list (acceptable);
- a recorded date list **predeclared before any download** so that date selection cannot be biased by post-hoc inspection of labels.

A reasonable floor is **30 distinct UTC days**. This is the minimum the memo is willing to call sufficient for a "meaningful" chronological split policy; even 30 days is thin by classical machine-learning standards, and Phase 4bl-A recommends 60–90 days as a more robust default if storage / runtime permit (see §5).

### 3.2 What minimum data expansion is needed before label diagnostics can become more than one-day sanity checks?

Per-day descriptive label diagnostics aggregated across many days can support:

- per-day censoring nest distributions;
- per-day class balance distributions;
- per-day forward-return distribution shape comparisons;
- per-weekday vs per-weekend descriptive comparisons;
- per-volatility-regime descriptive comparisons (using a predeclared volatility definition);
- alignment robustness across days.

For any of those aggregations to be meaningful, the number of days must be large enough that day-to-day variation is not the dominant source of noise. A floor of **30 distinct UTC days** is the smallest scope the memo is willing to call useful for cross-day descriptive comparisons; **60–90 days** is more robust.

### 3.3 What minimum data expansion is needed before ML feasibility can even be discussed?

ML feasibility (per Phase 4ak M0 §1 / §6 / §7 / §11) requires, before any model fit:

- a chronological train block;
- a chronological out-of-sample block;
- a predeclared edge-rate plausibility argument grounded in theory, not on observed numbers (Phase 4ak M0 §7; Phase 4y central lesson);
- an opportunity-rate viability floor predeclared from theory (Phase 4u §16; Phase 4v / 4w);
- cost realism with §11.6 = 8 bps per side preserved verbatim;
- a falsification criterion (Phase 4ak M0 §11);
- a forbidden-rescue check (Phase 4ak M0 §10; Phase 4al refined no-rescue rule);
- a post-null-cooldown check (Phase 4ak M0 §12);
- a design-family-distance check (Phase 4ak M0 §4).

ML feasibility memo authorship can only be *conceivable* after multi-day raw / normalized / feature / label artefacts exist with passing gates and recorded successor-state markers on a multi-day arc. Phase 4bl-A does **not** authorize ML feasibility memo authorship; it merely defines that the required precondition is multi-day data, not better one-day diagnostics.

### 3.4 What minimum data expansion is needed before strategy / backtest discussions remain blocked but at least become conceivable later under M0?

Strategy hypothesis admission under M0 (Phase 4ak twelve-clause gate) requires the full M0 evidence stack: mechanism source, non-price-only / structurally-distinct source, predicted Δ_R baseline-superiority theory, rejection-topology distance vs the six retained rejected families (R2, F1, D1-A, V2, G1, C1), cost realism, opportunity-rate plausibility, edge-rate plausibility, data feasibility, governance compatibility, forbidden-rescue check, pre-backtest falsification criteria, post-null cooldown. Even with multi-day data, a strategy candidate must additionally clear the Phase 4m 18-requirement fresh-hypothesis validity gate and the Phase 4t 10-dimension candidate scoring matrix.

Multi-day data is **necessary but not sufficient**. Strategy / backtest discussions remain blocked even after multi-day data exists; they become *conceivable* only after multi-day data + multi-day split policy + multi-day label diagnostics + ML feasibility memo + a candidate hypothesis that survives M0 admission.

---

## 4. Scope candidates

The memo evaluates seven candidate scopes. Each is evaluated against:

- evidentiary value;
- acquisition burden;
- governance burden;
- storage / processing burden;
- suitability for split policy;
- suitability for label diagnostics;
- suitability for later ML feasibility discussion;
- risk of scope creep.

### Option A — Remain paused, no expansion requirements

| Dimension | Assessment |
| --- | --- |
| Evidentiary value | Zero new evidence. |
| Acquisition burden | Zero. |
| Governance burden | Zero. |
| Storage / processing burden | Zero. |
| Suitability for split policy | None. |
| Suitability for label diagnostics | Cell remains structurally insufficient; only one-day sanity check possible. |
| Suitability for later ML feasibility discussion | Not conceivable. |
| Risk of scope creep | None. |

Option A is the conservative anchor. It is procedurally always available and does not authorize anything.

### Option B — BTCUSDT-only, 30 UTC days of aggTrades

| Dimension | Assessment |
| --- | --- |
| Evidentiary value | First scope that admits a coherent chronological train / OOS split. Useful descriptive cross-day baseline. Still thin by classical ML standards. |
| Acquisition burden | ~30× current Phase 4az daily archive size; manageable under public archive. |
| Governance burden | One symbol, one source class, one timestamp policy; matches Phase 4az precedent exactly. |
| Storage / processing burden | Approximately 30× the current local 21 MiB raw archive footprint; raw + normalized + feature + label growth proportional. |
| Suitability for split policy | First scope that admits a non-trivial chronological split. 30 days is a floor, not a guarantee. |
| Suitability for label diagnostics | Admits per-day cross-day descriptive comparisons. |
| Suitability for later ML feasibility discussion | Conceivable for an M0-cleared ML feasibility memo. |
| Risk of scope creep | Low, single symbol, one source class. |

Option B is the **minimum viable** multi-day expansion. It is the recommended floor.

### Option C — BTCUSDT-only, 60–90 UTC days of aggTrades

| Dimension | Assessment |
| --- | --- |
| Evidentiary value | More robust per-block sample sizes; better day-of-week and regime mix coverage; better PBO / DSR / CSCV sample-size floor support. |
| Acquisition burden | 2–3× Option B. |
| Governance burden | Same as Option B. |
| Storage / processing burden | 2–3× Option B; still manageable locally if storage permits. |
| Suitability for split policy | Strong; admits multi-week train / validation / OOS partitioning with proper purge / embargo. |
| Suitability for label diagnostics | Strong; admits per-week and per-weekday descriptive comparisons. |
| Suitability for later ML feasibility discussion | More robust precondition. |
| Risk of scope creep | Low, single symbol, one source class. |

Option C is the **preferred upper bound** for the first multi-day expansion if storage / runtime permit.

### Option D — BTCUSDT + ETHUSDT, same 30 UTC days

| Dimension | Assessment |
| --- | --- |
| Evidentiary value | Admits cross-symbol descriptive comparison on a small symbol set. Cross-symbol generalisation claims still cannot be made from two symbols. |
| Acquisition burden | 2× Option B. |
| Governance burden | Requires per-symbol manifest layer; per-symbol gate; per-symbol successor-state; per-symbol diagnostics; cross-symbol governance language. Higher than Option B. |
| Storage / processing burden | 2× Option B. |
| Suitability for split policy | Same as Option B per-symbol; cross-symbol split adds policy complexity without clearly improving evidence. |
| Suitability for label diagnostics | Adds cross-symbol comparison capability. |
| Suitability for later ML feasibility discussion | Comparable to Option B per-symbol; multi-symbol ML feasibility adds complexity. |
| Risk of scope creep | Moderate; introduces symbol-portfolio temptation that the v1 BTCUSDT-only live scope explicitly forbids. |

Option D is **not recommended for the first expansion**. The marginal cross-symbol evidence is small and the governance burden is non-trivial.

### Option E — BTCUSDT + ETHUSDT + selected high-liquidity alts, same 30 UTC days

| Dimension | Assessment |
| --- | --- |
| Evidentiary value | Admits broader cross-symbol descriptive baseline. Lower-liquidity symbols add microstructure regime variation that may or may not be informative. |
| Acquisition burden | 4–6× Option B. |
| Governance burden | Adds per-symbol microstructure regime risk; alt symbols differ materially in tick size, lot size, funding behaviour, and liquidity depth. |
| Storage / processing burden | 4–6× Option B. |
| Suitability for split policy | Marginal improvement; cross-symbol symbol leakage risk increases. |
| Suitability for label diagnostics | Adds cross-symbol descriptive context but with higher governance burden. |
| Suitability for later ML feasibility discussion | Marginal; cross-symbol portfolio ML is out of v1 scope. |
| Risk of scope creep | High; alt-symbol rescue temptation for old failed strategies (R2 / F1 / D1-A / V2 / G1 / C1) is explicitly forbidden. |

Option E is **not recommended for the first expansion**.

### Option F — order-book / mark-price / spot / cross-venue / funding / open-interest expansion now

| Dimension | Assessment |
| --- | --- |
| Evidentiary value | Adds entirely new data families. Each new family requires its own data-requirements memo, acquisition memo, integrity-gate, normalization, feature, label, gate, successor-state arc. |
| Acquisition burden | Order-of-magnitude larger than Option B. |
| Governance burden | Each family requires Phase 4az / 4bb / 4bd / 4bh / 4bj-style governance. |
| Storage / processing burden | Order-of-magnitude larger than Option B. |
| Suitability for split policy | Same as Option B for split policy; new families do not change split. |
| Suitability for label diagnostics | Same as Option B for label diagnostics; new families do not change one-day-vs-multi-day. |
| Suitability for later ML feasibility discussion | Marginal; the bottleneck is multi-day generalisation, not richer data per row. |
| Risk of scope creep | High; multiple new families increase governance complexity dramatically. |

Option F is **not recommended for the first expansion**.

### Option G — ML / strategy / backtest now

| Dimension | Assessment |
| --- | --- |
| Evidentiary value | None; structurally bypasses M0. |
| Acquisition burden | Bypasses acquisition gates. |
| Governance burden | Bypasses governance entirely. |
| Suitability for split policy | None; uses the unsplit single-day cell. |
| Suitability for label diagnostics | None. |
| Suitability for later ML feasibility discussion | None. |
| Risk of scope creep | Maximum. |

Option G is **FORBIDDEN**. It would bypass the Phase 4ak twelve-clause M0 gate, the post-null cooldown rule, the Phase 4al refined no-rescue rule, the Phase 4bj-J non-authorizations, and every retained verdict. Option G is not recommended under any circumstance.

---

## 5. Recommended initial expansion scope

**Primary recommendation: Option B — BTCUSDT-only, at least 30 distinct UTC days of public USDⓈ-M futures aggTrades.**

**Preferred upper bound: Option C — BTCUSDT-only, 60–90 UTC days**, only if storage / runtime constraints permit. Option C is preferable to Option B if storage permits because it is more robust against day-to-day noise and gives meaningful train / validation / OOS block sizes.

The recommendation justifies each design choice:

### 5.1 Why BTCUSDT-only first is simpler and safer than immediate multi-symbol

- The v1 live scope is locked to BTCUSDT-only per §1.7.3. Live-readiness for a different symbol would require separate authorization. Research on BTCUSDT-only matches live scope and avoids implicit multi-symbol portfolio framing.
- The Phase 4az / 4bb / 4bd / 4bh / 4bj-C / 4bj-E / 4bj-G arc is BTCUSDT-only; the precedent matches.
- The per-symbol governance burden compounds: per-symbol manifest layer, per-symbol gate, per-symbol successor-state, per-symbol label generation, per-symbol diagnostics. Beginning with one symbol keeps governance simple.
- Cross-symbol generalisation cannot be claimed from two symbols anyway. ETHUSDT comparison can be added later under a separately governed multi-symbol arc, after BTCUSDT-only multi-day has been validated.

### 5.2 Why 30 days is a minimum floor, not a guarantee

- 30 days is the smallest scope that admits a coherent chronological train / validation / OOS split with non-trivial block sizes (e.g. 15 / 7 / 8 days, or 20 / 5 / 5 days).
- 30 days covers four week-of-week cycles plus a few days, so day-of-week effects are visible but not exhaustively absorbed.
- 30 days is **not** enough to absorb regime variation (e.g. macro-event days, funding-stress days, exchange outages). It is a floor for a *meaningful* split policy, not a guarantee of *robust* ML feasibility.
- A future Phase 4bl-B-equivalent acquisition design memo may revise this floor upward based on per-symbol intraday row counts and storage budget.

### 5.3 Why 60–90 days may be preferable if storage / runtime permit

- 60 days admits two-month coverage with a 30 / 15 / 15-day chronological partition, which is robust enough for descriptive cross-day comparisons.
- 90 days admits three-month coverage with a 60 / 15 / 15-day partition or a rolling walk-forward design with multiple OOS windows.
- 60–90 days at 1.6M rows/day ≈ 100–150M rows total raw aggTrades for BTCUSDT; per-row label parquet at ~140 bytes ≈ 14–21 GiB label parquet total. This is locally manageable for most operator hardware, though it should be verified at acquisition-authorization time.
- 60–90 days substantially reduces the risk that any single day's regime biases an entire block's statistics.

### 5.4 Why ETHUSDT / alts should be a later expansion

- A single-symbol multi-day arc is sufficient to satisfy the *necessary* condition for split / diagnostics / ML feasibility.
- Adding a second or third symbol changes the data-governance surface (per-symbol manifest layer, per-symbol gate, per-symbol successor-state, per-symbol label generation, per-symbol diagnostics) without obviously improving the bottleneck (single-symbol multi-day generalisation).
- ETHUSDT comparison may be authorized as a parallel arc after the BTCUSDT-only multi-day arc has completed governance.
- Lower-liquidity alts introduce per-symbol microstructure regime risk (different tick size, lot size, funding behaviour, liquidity depth) that complicates per-symbol calibration. Alts should never be added on the same merge.

### 5.5 Why order-book / mark-price / funding / OI should not be added in the same first expansion

- The bottleneck is multi-day data along the *time* axis, not richer features per row.
- Each new family requires its own data-requirements memo, acquisition memo, integrity-gate, normalization, feature, label, gate, successor-state arc.
- Combining multi-day aggTrades expansion with multi-family expansion would multiply governance burden, not reduce it.
- Order-book / mark-price / funding / OI may be authorized as later separately governed arcs after BTCUSDT-only multi-day aggTrades is in place.

### 5.6 Why this requirements phase does not authorize acquisition

- Phase 4bl-A is **requirements-only**. It records what a future Phase 4bl-B-equivalent acquisition design memo would have to consider before requesting authorization.
- Acquisition would touch external endpoints (public archive downloads), would create local artefacts, would require integrity governance, and would require a separately approved acquisition design.
- Acquisition is not a phase that can be combined with a requirements memo.

---

## 6. Date-range / regime coverage requirements

A future Phase 4bl-B-equivalent acquisition design memo (not authorized by Phase 4bl-A) must consider the following date-range requirements when defining the future acquisition target.

### 6.1 Contiguous vs sampled UTC days

- **Contiguous (preferred for first expansion).** A contiguous date range (e.g. 2025-01-01 through 2025-01-30 UTC) is simpler to acquire, simpler to validate, simpler to split, and simpler to diagnose. Day-to-day variation is captured naturally. A purge / embargo at the maximum label horizon is straightforward.
- **Sampled (acceptable only if specifically justified).** A predeclared sampled date list (e.g. every 3rd day across a longer period) may be acceptable if the rationale is documented in the acquisition design memo and approved separately. Sampling introduces governance complexity (sampling rule predeclared, no post-hoc inclusion / exclusion of days, sample diversity check).

For the first multi-day expansion, the memo recommends a **contiguous** date range.

### 6.2 Minimum number of distinct UTC days

- **Floor:** 30 distinct UTC days.
- **Preferred:** 60–90 distinct UTC days.

### 6.3 Inclusion of multiple weekdays

The date range must include at least one full Mon–Fri week. With 30 contiguous days this is automatic; with 30 sampled days it must be enforced by the sampling rule.

### 6.4 Inclusion of weekends

Crypto markets trade 24/7, so weekends are present in any contiguous range. A future memo may consider whether weekend behaviour is meaningfully different and whether to explicitly diagnose it.

### 6.5 Inclusion of high-volatility days

Any contiguous range likely includes at least one elevated-volatility day. No specific volatility threshold is required at this requirements level; the acquisition design memo may revisit this.

### 6.6 Inclusion of quiet days

Any contiguous range likely includes at least one quiet day. No specific volatility threshold is required at this requirements level.

### 6.7 Avoidance of cherry-picked dates

- The date list must be **deterministically predeclared** before any download.
- No date may be added / removed / replaced based on observed label outcomes.
- The acquisition design memo must lock the date list at memo-authorship time.
- The acquisition execution phase must download the dates exactly as locked.

### 6.8 Recording missing or unavailable archive files explicitly

- The public archive (`data.binance.vision`) may occasionally have missing or unavailable files (e.g. exchange downtime, archive gaps).
- The future acquisition execution phase must record any missing file explicitly in an `invalid_windows` field of the multi-day raw manifest.
- Missing files must not be silently skipped, forward-filled, interpolated, imputed, or replaced.
- The Phase 4ay §10 strict integrity gate precedent applies: failure on missing checksum / missing file is fail-closed.

### 6.9 First acquisition contiguous window recommendation

The memo recommends that the first acquisition uses a **contiguous window**. A natural choice is the 30 / 60 / 90 contiguous UTC days immediately following or including the existing Phase 4az single-day cell (2025-01-15), e.g. 2025-01-01..2025-01-30 or 2024-12-01..2025-01-30. The exact date list must be locked by the acquisition design memo, not by this requirements memo.

---

## 7. Symbol-scope requirements

A future Phase 4bl-B-equivalent acquisition design memo must consider the following symbol-scope requirements.

### 7.1 BTCUSDT as first mandatory symbol

BTCUSDT is the first and mandatory symbol for the first multi-day expansion. Rationale:

- v1 live scope is BTCUSDT-only (§1.7.3);
- the existing single-day arc is BTCUSDT-only, so multi-day expansion preserves the symbol-scope precedent;
- single-symbol governance is simpler than multi-symbol governance;
- single-symbol diagnostics are simpler than cross-symbol diagnostics.

### 7.2 ETHUSDT as likely second symbol later

ETHUSDT is the most natural second symbol if cross-symbol comparison becomes desirable. ETHUSDT is:

- a high-liquidity Binance USDⓈ-M perpetual;
- supported by the same public archive class (`data.binance.vision`);
- the natural research comparison symbol per project precedent.

ETHUSDT addition must be a **separately authorized** future phase, not part of the first multi-day expansion.

### 7.3 Criteria for adding SOLUSDT / XRPUSDT / ADAUSDT or other high-liquidity symbols later

If a future multi-symbol arc is ever authorized, criteria for adding additional symbols must include:

- daily aggTrades row count comparable to BTCUSDT / ETHUSDT (within an order of magnitude);
- stable tick size and lot size over the acquisition date range;
- stable funding behaviour over the acquisition date range;
- minimal exchange downtime / archive gaps;
- liquidity depth sufficient to make microstructure features meaningful;
- per-symbol manifest layer / gate / successor-state / label generation must be repeated for each new symbol;
- separately authorized acquisition design memo per symbol.

### 7.4 Why lower-liquidity symbols increase microstructure regime risk

Lower-liquidity symbols differ from BTCUSDT in:

- tick size relative to typical spread (larger relative ticks → coarser price quanta);
- lot size relative to typical trade size (larger relative lots → more discrete fills);
- funding behaviour (more frequent funding sign flips, larger funding magnitudes);
- exchange order-book depth (fewer levels populated, larger relative gaps);
- regime stability (more frequent flash moves, lower mean reversion).

These differences change microstructure feature distributions and label distributions in ways that complicate per-symbol calibration. Lower-liquidity symbols should not be added to the first multi-day expansion.

### 7.5 Why cross-symbol generalisation cannot be claimed until a separately governed multi-symbol arc exists

- Generalisation claims require statistically meaningful symbol diversity, which two or three symbols do not provide.
- Per-symbol manifest layer / gate / successor-state must be separately governed.
- Cross-symbol split policy must address symbol-portfolio leakage (e.g. correlated returns, common funding regimes).
- Cross-symbol ML feasibility is a separate question from single-symbol ML feasibility.

### 7.6 No alt-symbol rescue of old failed strategies

No old failed strategy family (R2, F1, D1-A, V2, G1, C1) may be revived by attempting alt-symbol fitting. The Phase 4ak post-null cooldown rule and Phase 4al refined no-rescue rule remain binding. Alt-symbol expansion (if ever authorized) must be a new mechanism arc, not a rescue arc.

---

## 8. Data-source requirements

A future Phase 4bl-B-equivalent acquisition design memo must consider the following data-source requirements at requirements level only.

### 8.1 Expected source class

**Public daily aggTrades archive for Binance USDⓈ-M Futures**, consistent with the existing Phase 4az source lineage:

```text
https://data.binance.vision/data/futures/um/daily/aggTrades/<SYMBOL>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.zip
```

with paired `.CHECKSUM` companion file for SHA256 verification.

### 8.2 No authenticated APIs

No future acquisition phase may use authenticated Binance APIs (`fapi.binance.com` signed endpoints, `vapi.binance.com`, etc.) for multi-day data acquisition. The public archive is the canonical source.

### 8.3 No private endpoints

No future acquisition phase may use private endpoints (`/fapi/v1/order`, `/fapi/v2/account`, `/fapi/v2/positionRisk`, `/fapi/v1/leverage`, `/fapi/v1/marginType`, `/fapi/v1/forceOrders`, user data streams, listenKey lifecycle).

### 8.4 No user streams or WebSockets

No future acquisition phase may open user streams or WebSocket connections. The public archive is the canonical source and does not require streaming connectivity.

### 8.5 No production keys

No future acquisition phase may create or use production trade-capable Binance API keys. Public archive access does not require keys.

### 8.6 No credentials, .env, .mcp.json

No future acquisition phase may create or read credentials, `.env`, or `.mcp.json`.

### 8.7 No public endpoint calls during Phase 4bl-A

Phase 4bl-A itself must not call any public endpoint. The requirements memo records what the source class should be, not what the source contents are. No URL is opened, no archive is downloaded, no checksum is fetched.

### 8.8 Future acquisition requires separate authorization

A future Phase 4bl-B-equivalent acquisition design memo (and a subsequent Phase 4bl-C-equivalent acquisition execution phase) is required before any download. Phase 4bl-A does **not** authorize acquisition.

---

## 9. Storage and namespace requirements

A future Phase 4bl-B-equivalent acquisition design memo must define the storage layout requirements for multi-day aggTrades artefacts. The memo must preserve the Phase 4bb-F canonical path policy and must not mutate historical one-day artefacts.

### 9.1 Raw zip files

Future raw zip files should follow the existing Phase 4az precedent:

```text
data/microstructure/raw/microstructure_raw_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.zip
```

Each zip must be paired with a `.sha256` sidecar (canonical Phase 4bb-F format `<json_sha256_hex>  <basename>\n`).

### 9.2 Raw manifests

Future raw manifests must either:

- extend the existing `microstructure_raw_aggtrades_v001__v001.json` manifest as a multi-day manifest (preferred if version semantics permit), or
- create a new dataset family / version (e.g. `microstructure_raw_aggtrades_multiday_v001__v001.json` or a versioning bump).

The acquisition design memo must decide between these two paths and justify the choice. The existing single-day Phase 4az manifest must remain byte-identical regardless.

### 9.3 Acquisition logs

A future multi-day acquisition log must record:

- date list locked at memo time;
- per-date download status (`success`, `missing`, `checksum_mismatch`, `decompression_failure`, etc.);
- per-file SHA256;
- per-file size;
- acquisition source URL;
- acquisition start / end timestamps;
- acquisition code commit SHA;
- acquisition `base_main_commit_sha`.

The log must follow the Phase 4az precedent.

### 9.4 Normalized / derived parquets

Future normalized / derived parquets must follow the Phase 4bd canonical path policy:

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet
```

with paired `.sha256` sidecars.

### 9.5 Derived manifests

Future derived manifests must either extend the existing manifest as a multi-day manifest or create a new dataset family / version, parallel to §9.2.

### 9.6 Feature parquets

Future feature parquets must follow the Phase 4bh canonical path policy:

```text
data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-features-aggtrades-<YYYY-MM-DD>.parquet
```

with paired `.sha256` sidecars.

### 9.7 Feature manifests

Future feature manifests must either extend the existing manifest as a multi-day manifest or create a new dataset family / version, parallel to §9.2.

### 9.8 Label parquets

Future label parquets must follow the Phase 4bj-C canonical path policy:

```text
data/microstructure/labels/microstructure_labels_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-labels-aggtrades-<YYYY-MM-DD>.parquet
```

with paired `.sha256` sidecars.

### 9.9 Label manifests

Future label manifests must either extend the existing manifest as a multi-day manifest or create a new dataset family / version, parallel to §9.2. The existing single-day Phase 4bj-C label manifest must remain byte-identical regardless.

### 9.10 Gate reports

Future gate reports must follow the Phase 4bb-F canonical path policy:

```text
data/microstructure/gate-reports/<raw|normalized|features|labels>/<dataset_family>__<dataset_version>__phase-<phase_id>__<unix_ms>__<short_commit>.json
```

with paired `.sha256` sidecars. The doubled `gate-reports/gate-reports/` path observed in the Phase 4bb-D legacy report must not be reused.

### 9.11 Successor-state records

Future successor-state records must follow the Phase 4bb-F canonical path policy:

```text
data/microstructure/successor-state/<dataset_family>__<dataset_version>__<stage_marker>__phase-<phase_id>.json
```

with paired `.sha256` sidecars.

### 9.12 Diagnostics outputs

Future diagnostics outputs must follow the Phase 4bj-K §10 canonical convention:

```text
data/microstructure/diagnostics/labels/<dataset_family>__<dataset_version>__<diagnostic_marker>__phase-<phase_id>.json
```

with paired `.sha256` sidecars.

### 9.13 Split artefacts for multi-day data

Future multi-day split artefacts must follow the Phase 4bj-J sibling-artefact precedent under the canonical successor-state namespace:

```text
data/microstructure/successor-state/<dataset_family>__<dataset_version>__split_policy__phase-<phase_id>.json
```

with paired `.sha256` sidecars. The split artefact must record the predeclared chronological partition (train / validation / OOS UTC date blocks), the purge / embargo policy (uniform 60s; locked by Phase 4bj-I §5), and the label-horizon set.

### 9.14 Preserve Phase 4bb-F canonical path policy

All future paths must conform to the Phase 4bb-F canonical path policy:

- gate reports under `data/microstructure/gate-reports/<family-subdir>/`;
- successor-state flat under `data/microstructure/successor-state/`;
- canonical filename pattern `<dataset_family>__<dataset_version>__<stage_marker>__phase-<phase_id>.json` or `<dataset_family>__<dataset_version>__phase-<phase_id>__<unix_ms>__<short_commit>.json`;
- canonical sidecar body `<json_sha256_hex>  <basename>\n` (two spaces, trailing newline).

### 9.15 No mutation of historical one-day artefacts

The existing Phase 4az / 4bb-D / 4bd / 4be / 4bf / 4bg-A / 4bg-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K artefacts must remain byte-identical. The one-day BTCUSDT 2025-01-15 cell may either be included as one of the days in the multi-day expansion (preferred for continuity) or treated as a separate historical fixture; this choice must be made by the future Phase 4bl-B acquisition design memo, not by Phase 4bl-A.

### 9.16 All data/microstructure outputs gitignored

All future `data/microstructure/` outputs must remain gitignored under the existing `.gitignore:85: data/microstructure/` rule. No data file may be committed to the repository.

### 9.17 Paired SHA256 sidecars where required

Every parquet, gate report, successor-state JSON, split artefact, and diagnostic JSON must carry a paired `.sha256` sidecar in canonical Phase 4bb-F format. Atomic write-then-rename and refuse-overwrite semantics must be preserved.

---

## 10. Raw acquisition requirements

A future Phase 4bl-B-equivalent acquisition design memo, and its successor Phase 4bl-C-equivalent acquisition execution phase, must predeclare the following before any download begins.

### 10.1 Exact symbols

The acquisition design memo must lock the exact symbol list. Per §5 / §7, the recommended initial scope is `["BTCUSDT"]`. Additional symbols may be added later under separately authorized phases.

### 10.2 Exact UTC date list

The acquisition design memo must lock the exact UTC date list as a deterministic ordered list before any download. Per §6, the recommended initial scope is a 30–90 day contiguous range. The date list must be recorded in the acquisition log alongside per-date outcomes.

### 10.3 Expected archive URL pattern

The acquisition design memo must record the expected source URL pattern. Per §8, the pattern is:

```text
https://data.binance.vision/data/futures/um/daily/aggTrades/<SYMBOL>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.zip
```

with paired `.CHECKSUM` companion at the same path + `.CHECKSUM` suffix. Phase 4bl-A is not authorized to open this URL; the requirements memo records the pattern only.

### 10.4 Expected local path layout

The acquisition design memo must record the exact future local path layout per §9. The path layout must conform to the Phase 4bb-F canonical path policy.

### 10.5 Hash computation rules

The acquisition design memo must lock:

- SHA256 hashing algorithm;
- chunked-read implementation;
- decimal-vs-hex encoding (hex lowercase 64-character standard);
- equality check against the `.CHECKSUM` companion;
- failure handling (fail-closed on mismatch).

### 10.6 Sidecar format

The acquisition design memo must lock the canonical Phase 4bb-F sidecar format:

```text
<json_sha256_hex>  <basename>\n
```

with two spaces between hash and basename, and exactly one trailing newline (`sha256sum`-compatible).

### 10.7 Acquisition log schema

The acquisition design memo must lock the acquisition log JSON schema. Required fields include:

- `dataset_family`, `dataset_version`, `symbol_list`, `date_list`;
- per-date status (`success`, `missing`, `checksum_mismatch`, `decompression_failure`, `invalid_window_detected`, etc.);
- per-file `path`, `size_bytes`, `sha256`, `companion_checksum_hex`, `companion_match` boolean;
- acquisition `start_unix_ms`, `end_unix_ms`;
- acquisition `code_commit_sha`, `base_main_commit_sha`;
- governance labels mirroring the Phase 4bj-J / 4bj-G precedent.

### 10.8 Failure / retry / missing-file policy

The acquisition design memo must lock:

- maximum retry count for transient HTTP errors;
- backoff policy;
- explicit fail-closed for `404 Not Found` after retries (record as missing-file);
- explicit fail-closed for checksum mismatch;
- explicit fail-closed for decompression failure;
- no silent skipping of failed dates.

### 10.9 No partial silent success

If any per-date download fails after retries, the acquisition phase must record the failure explicitly in the acquisition log and mark the overall result as `partial`. No date may be silently dropped from the date list.

### 10.10 No API keys

The acquisition phase must not use API keys.

### 10.11 No authenticated endpoints

The acquisition phase must not use authenticated Binance endpoints.

### 10.12 No WebSockets

The acquisition phase must not open WebSocket connections.

### 10.13 No data post-processing inside acquisition phase

The acquisition phase must not normalize, derive, feature-engineer, label, gate, or diagnose. Post-processing must occur in separately authorized successor phases (raw gate, normalization, feature, label, gate, successor-state, diagnostics arcs).

---

## 11. Repeat pipeline requirements

Multi-day expansion is not just "download more data." It requires repeating or extending, under separately authorized successor phases, the entire data-governance arc that already produced the single-day cell.

### 11.1 Required repeat / extension phases

Each of the following phases is **not authorized by Phase 4bl-A** and is named here only to define the required scope:

- **Phase 4bl-C-equivalent — Multi-Day Public Archive Acquisition Execution.** Downloads the predeclared date list under §10 governance.
- **Phase 4bl-D-equivalent — Multi-Day Raw Artefact QA / Raw Gate.** Re-applies the Phase 4ay §10 strict integrity gate (19+ checks per file) to the multi-day raw set; produces a multi-day raw gate report under `data/microstructure/gate-reports/raw/`.
- **Phase 4bl-E-equivalent — Multi-Day Raw Successor-State Recording.** Sibling JSON under `data/microstructure/successor-state/` recording the multi-day raw admissibility status, parallel to Phase 4bb-G.
- **Phase 4bm-*-equivalent — Multi-Day Normalization / Derived Artefact Arc.** Per-date normalized parquet generation under Phase 4bd canonical layout; multi-day derived manifest; multi-day derived gate; multi-day derived successor-state.
- **Phase 4bn-*-equivalent — Multi-Day Feature Generation / Gate Arc.** Per-date feature parquet generation; multi-day feature manifest; multi-day feature gate; multi-day feature successor-state.
- **Phase 4bo-*-equivalent — Multi-Day Label Generation / Gate Arc.** Per-date label parquet generation; multi-day label manifest; multi-day label gate; multi-day label successor-state.
- **Phase 4bp-*-equivalent — Multi-Day Split Policy Design / Artefact Recording.** Predeclared chronological train / validation / OOS partition; sibling artefact under successor-state namespace.
- **Phase 4bq-*-equivalent — Multi-Day Label Diagnostic Plan / Execution.** Predeclared diagnostic plan (analogous to Phase 4bj-K); diagnostic execution (analogous to Phase 4bj-L); output under `data/microstructure/diagnostics/labels/`.

### 11.2 Later phases (not authorized)

- ML feasibility memo (after multi-day diagnostics);
- Baseline ML diagnostic (after ML feasibility);
- Failure interpretation / fallback selection memo;
- Strategy hypothesis under M0 (Phase 4ak twelve-clause gate);
- Strategy spec;
- Backtest plan;
- Backtest execution;
- Paper / shadow / live only much later, under separate authorization.

### 11.3 Each phase is separately authorized

None of the phases in §11.1 / §11.2 is authorized by Phase 4bl-A. Each requires:

- a separately authorized authorization prompt per the Phase 4bk-A workflow standard;
- a branch dedicated to the phase;
- a branch-complete implementation report and closeout;
- operator review;
- a merge prompt;
- a merge into `main`;
- a merge-closeout per the Phase 4bk-A workflow standard.

### 11.4 Phase ladder enforces M0 admissibility

The phase ladder is deliberately long. It enforces that no shortcut bypasses the Phase 4ak M0 twelve-clause gate, the post-null cooldown rule, the Phase 4al refined no-rescue rule, or any retained verdict.

---

## 12. Multi-day manifest / indexing requirements

A future multi-day manifest must record, at minimum, the following fields. Field naming should follow the existing Phase 4az / 4bd / 4bh / 4bj-C precedent unless the acquisition design memo justifies a deviation.

### 12.1 Identity

- `dataset_family`: same family if extending (e.g. `microstructure_raw_aggtrades_v001`), or new family if a versioning bump is justified;
- `dataset_version`: same version if extending in place, or new version (e.g. `v002`) if a bump is needed;
- `source`: `"binance_data_archive"`;
- `endpoint`: `"data.binance.vision/data/futures/um/daily/aggTrades"`;
- `capture_mode`: `"historical_archive"`.

### 12.2 Multi-symbol / multi-date inventory

- `symbol_list`: list of symbols included (e.g. `["BTCUSDT"]`);
- `date_list`: locked ordered list of UTC dates included;
- per-`(symbol, date)` file inventory: path, size, SHA256, `.CHECKSUM` companion match status;
- per-`(symbol, date)` row count;
- total row count across all `(symbol, date)` pairs;
- per-file SHA256;
- paired sidecar SHA256;
- missing-file list (per-`(symbol, date)` failure outcomes).

### 12.3 Source provenance

- per-file source URL;
- per-file `companion_checksum_hex`;
- per-file `companion_match` boolean;
- acquisition `code_commit_sha`;
- acquisition `base_main_commit_sha`;
- acquisition `start_unix_ms`, `end_unix_ms`.

### 12.4 Governance labels

Multi-day manifests must carry governance labels mirroring the Phase 4az / 4bd / 4bh / 4bj-C precedent:

- `phase`, `phase_id`, `source_phase_boundary`;
- `validator` (e.g. `phase_4ax_aggtrades_v001` for raw aggTrades validation);
- `stop_trigger_domain`: `trade_price_backtest_candidate` (preserved per Phase 3v §8);
- `feature_computation`: `forbidden` (raw / normalized / derived only);
- `strategy_use`: `forbidden`;
- `acquisition`: `unauthorized` (until the acquisition phase explicitly authorizes itself);
- `ml`: `forbidden`;
- `backtest`: `forbidden`;
- `paper_shadow`: `forbidden`;
- `live`: `forbidden`;
- `deployment`: `forbidden`;
- `exchange_write`: `forbidden`.

### 12.5 Default flag values

- `research_eligible`: `false` (default; not flipped except via a separately authorized successor-state / eligibility-gate phase per the Phase 4aw `flip_research_eligible(...)` always-raises invariant);
- `eligibility_gate_status`: `"pending"` (default; not transitioned except via a separately authorized phase);
- `chronological_split_policy`: not mutated on raw / derived / feature manifests; mutated on label manifests only via a separately authorized split policy phase.

### 12.6 Sibling artefacts for admissibility / split states

Multi-day manifest admissibility and split states must be recorded as **sibling JSON artefacts** under `data/microstructure/successor-state/`, never as in-place mutations of the original manifest. This preserves the Phase 4bb-G / 4bg-B / 4bi-D / 4bj-G / 4bj-J precedent.

### 12.7 Immutable input references

The multi-day manifest must reference the predecessor single-day manifests (Phase 4az, 4bd, 4bh, 4bj-C) by SHA256 if the multi-day arc claims continuity. The single-day artefacts must remain byte-identical regardless of whether they are claimed as continuity inputs.

### 12.8 Processing code commit SHAs

Every processing layer must record:

- `code_commit_sha`: full 40-char SHA of the commit at which the processing kernel was run;
- `base_main_commit_sha`: full 40-char SHA of `main` at the time the phase branched.

This enables reproducibility.

---

## 13. Multi-day split policy implications

A future Phase 4bp-*-equivalent multi-day split policy phase must define the following at policy / artefact level. Phase 4bl-A does not authorize Phase 4bp-* and does not pre-decide the split.

### 13.1 train / validation / test vocabulary admissibility

Train / validation / test vocabulary only becomes admissible **after** multi-day data exists. The Phase 4bj-I §4 / Phase 4bj-J §6 forbidden-vocabulary rule applies to single-day cells only. Once multi-day data exists, train / validation / test partitioning of the multi-day cell is the correct vocabulary.

### 13.2 Strictly chronological split

Any future split must be strictly chronological:

- earliest UTC dates → train block;
- middle UTC dates → validation block (if a validation block is used);
- latest UTC dates → out-of-sample / test block.

No random shuffling. No row-level random split. No leave-one-day-out cross-validation that randomly reshuffles dates.

### 13.3 No random split

Random splits are forbidden under the Phase 4bj-I §5 / Phase 4bj-J §6 precedent, generalized to the multi-day cell. Random splits leak future information into past blocks and produce biased estimators.

### 13.4 Purge / embargo based on maximum label horizon

The maximum forward label horizon in the locked label schema is 60s. Phase 4bj-I §5 locked a uniform 60s purge / embargo policy for the single-day cell; the same policy applies to multi-day splits:

- rows in `[block_end - 60s, block_end)` are purged from the earlier block;
- rows in `[block_start, block_start + 60s)` are embargoed from the later block;
- both blocks lose 60 seconds of rows at the boundary;
- this is a strict, uniform policy; no per-horizon variation.

If a future label-schema phase adds longer horizons (which is currently forbidden by Phase 4bj-J §10), the purge / embargo must be revisited to use the new maximum horizon.

### 13.5 Split by UTC day or contiguous date block, not by random row

The natural split granularity is whole UTC days or whole contiguous date blocks. Splitting by row would mix dates within a single block.

### 13.6 Out-of-sample period must be later in time

The out-of-sample / test block must always be later in time than the train and validation blocks. No reversed-time evaluation. No look-ahead.

### 13.7 No repeated peeking at test period

Once the out-of-sample period is locked, it may not be inspected during model selection or threshold tuning. The Phase 4ay §10 strict integrity gate and the Phase 4bj-J §6 no-cherry-picking discipline apply to the test period.

### 13.8 Potential rolling-window or walk-forward design

A rolling-window or walk-forward design (multiple OOS windows, each later in time than its corresponding train window) may be designed in a future split-policy memo. Walk-forward is preferable to a single split because it reduces sample-time-dependence of the OOS evaluation. The split-policy memo must lock the walk-forward parameters predeclared.

### 13.9 Multi-symbol split must avoid symbol leakage claims

If a future multi-symbol arc is ever authorized, the split must avoid claiming cross-symbol generalisation from a single symbol's train and another symbol's test. Multi-symbol generalisation requires symbol-level diversity and a separately governed multi-symbol split policy.

---

## 14. Minimum future diagnostic eligibility

A future Phase 4bq-*-equivalent multi-day label diagnostic phase requires the following predecessors to exist in `main`. Phase 4bl-A does not authorize Phase 4bq-* and merely defines the precondition.

### 14.1 Multi-day raw artefacts

Multi-day raw zip files + paired `.sha256` sidecars + raw manifest + raw acquisition log under `data/microstructure/raw/...` and `data/microstructure/manifests/...`.

### 14.2 Multi-day raw gate report

A multi-day raw gate report under `data/microstructure/gate-reports/raw/` confirming integrity for every `(symbol, date)` pair in the multi-day inventory.

### 14.3 Multi-day raw successor-state

A multi-day raw successor-state JSON under `data/microstructure/successor-state/` confirming raw-stage admissibility.

### 14.4 Multi-day normalized / feature / label artefacts

Per-date normalized, feature, and label parquets for every `(symbol, date)` pair, with paired `.sha256` sidecars and multi-day manifests at each layer.

### 14.5 Multi-day gates passed

A multi-day derived-family gate report, a multi-day feature-family gate report, and a multi-day label-family gate report, each PASS, each under `data/microstructure/gate-reports/<family>/`.

### 14.6 Multi-day successor-state records

Multi-day derived / feature / label successor-state JSONs under `data/microstructure/successor-state/`.

### 14.7 Multi-day no-split or split policy artefact

Either a multi-day no-split determination (analogous to Phase 4bj-J but applied to the multi-day cell, recording why a formal split is not yet possible if applicable) **or** a multi-day split policy artefact under `data/microstructure/successor-state/` recording the predeclared chronological partition.

If the multi-day data is sufficient to support a chronological split, the split artefact path is preferred. If the multi-day data is unexpectedly insufficient, the no-split path is preferred.

### 14.8 Predeclared diagnostics plan

A predeclared multi-day diagnostics plan analogous to Phase 4bj-K, listing allowed diagnostic categories, forbidden diagnostics, per-horizon exclusion rules, leakage checks, output namespace, stop conditions, and interpretation limits.

### 14.9 Output namespace

```text
data/microstructure/diagnostics/labels/
```

with canonical Phase 4bb-F filename pattern and paired `.sha256` sidecars.

### 14.10 Stop conditions

The future multi-day diagnostic phase must record stop conditions analogous to Phase 4bj-K §12 (source SHA mismatch, row-count mismatch, manifest summary mismatch, label schema mismatch, feature-label alignment failure, timestamp monotonicity failure, unexpected null / invalid counts, unexpected censoring mismatch, unapproved segmentation detected, strategy / ML / signal / PnL metric attempted, external endpoint call attempted, `data/microstructure/` mutation outside the approved diagnostics namespace, original artefact mutation).

### 14.11 Non-authorizations

The future multi-day diagnostic JSON must enumerate the same non-authorization booleans as Phase 4bj-K §10.10 (`ml_training_authorized=false`, `strategy_authorized=false`, `backtest_authorized=false`, etc.).

---

## 15. Relationship to current one-day cell

### 15.1 Existing BTCUSDT 2025-01-15 artefacts remain valid historical evidence

The Phase 4az / 4bb-D / 4bd / 4be / 4bf / 4bg-A / 4bg-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K artefacts remain valid historical evidence. They are byte-identical and must not be moved, migrated, rewritten, or replaced.

### 15.2 No mutation under Phase 4bl-A

Phase 4bl-A modifies no `data/microstructure/` artefact. All 23 prior artefacts (raw / derived / feature / label parquets, manifests, sidecars, gate reports, successor-state JSONs including the Phase 4bj-J no-split determination) remain byte-identical pre/post the Phase 4bl-A branch.

### 15.3 One-day cell as pipeline-proving fixture

The one-day cell can remain a **pipeline-proving fixture**:

- it demonstrates that the raw → normalized / derived → feature → label arc works end-to-end;
- it demonstrates that each gate (raw, derived, feature, label) can pass;
- it demonstrates that each successor-state record can be written;
- it demonstrates that the canonical path policy works;
- it demonstrates that the Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved across many phases;
- it provides reference SHAs for reproducibility checks.

### 15.4 One-day cell not research-grade for ML or strategy

The one-day cell **must not** be treated as research-grade for ML, strategy, signal, or backtest purposes. It is a fixture for pipeline testing, not a sample for evidence generation. Phase 4bj-I, Phase 4bj-J, and Phase 4bj-K all record this boundary.

### 15.5 Decision: include or exclude 2025-01-15 from the multi-day expansion

Whether the multi-day expansion includes 2025-01-15 as one of the days or treats it as a separate historical fixture is a decision for the future Phase 4bl-B-equivalent acquisition design memo. Phase 4bl-A does not lock this decision.

- **Include path.** The multi-day acquisition includes 2025-01-15 as one of the dates. The existing single-day artefacts may be referenced as continuity inputs (with SHA references) but must not be modified. The multi-day arc must regenerate normalized / feature / label parquets for 2025-01-15 as part of the multi-day arc; the original single-day parquets remain on disk as historical fixtures.
- **Exclude path.** The multi-day acquisition uses a date range that does not include 2025-01-15. The existing single-day artefacts remain as separate historical fixtures with no continuity claim.

The acquisition design memo must justify either path explicitly.

---

## 16. Decision options and recommendation

### 16.1 Decision option table

| Option | Description | Authorized by Phase 4bl-A? |
| --- | --- | --- |
| **A** | Remain paused, no expansion requirements | The default if Phase 4bl-A is not merged. |
| **B** | Author Phase 4bl-A memo (docs-only requirements) | **YES — this is the recommended option for the Phase 4bl-A operator decision; the memo is what Phase 4bl-A produces.** |
| **C** | Author Phase 4bl-B — Multi-Day aggTrades Acquisition Design Memo (docs-only design) | Not authorized by Phase 4bl-A. |
| **D** | Author Phase 4bl-B — Multi-Day aggTrades Acquisition Authorization Memo (docs-only authorization gate) | Not authorized by Phase 4bl-A. |
| **E** | Phase 4bl-C-equivalent — Multi-Day Public Archive Acquisition Execution | Not authorized by Phase 4bl-A. |
| **F** | Multi-symbol expansion, mark-price / OI / funding / order-book expansion, or alt-symbol arc | Not authorized by Phase 4bl-A. |
| **G** | ML / strategy / backtest now | FORBIDDEN. |

### 16.2 Primary recommendation

**Primary recommendation:** record this Phase 4bl-A docs-only requirements memo (Option B).

This option:

- captures the requirements for a future multi-day expansion;
- preserves the boundary between requirements and acquisition;
- preserves all retained verdicts and project locks;
- authorizes nothing further;
- leaves the operator with a clean choice for the next phase (Phase 4bl-B-equivalent design or authorization memo, or remain paused).

### 16.3 Conditional next step (NOT authorized by Phase 4bl-A)

If the operator wants to continue toward multi-day data, the cleanest next phase is:

**Phase 4bl-B — Multi-Day aggTrades Acquisition Authorization / Design Memo** (docs-only).

This future phase would:

- lock the exact date list;
- lock the exact symbol list;
- lock the exact source URL pattern;
- lock the future local path layout;
- lock the manifest schema;
- lock the integrity-gate plan;
- lock the failure / retry / missing-file policy;
- lock the acquisition log schema;
- predeclare the future Phase 4bl-C-equivalent acquisition execution;
- authorize neither acquisition itself nor any downstream phase.

**Phase 4bl-B is NOT authorized by Phase 4bl-A.** It requires a separately authorized authorization prompt per the Phase 4bk-A workflow standard.

### 16.4 Alternative recommendation: remain paused

The operator may instead choose to **remain paused** after merging Phase 4bl-A. Remain-paused is always a procedurally valid choice. It does not preclude future phase authorization.

---

## 17. Future phase ladder

The following safe future sequence is named here only for completeness. **All phases below are NOT authorized by Phase 4bl-A.**

- **Phase 4bl-B — Multi-Day aggTrades Acquisition Authorization / Design Memo** (docs-only)
- **Phase 4bl-C — Multi-Day Public Archive Acquisition Execution** (docs + local gitignored output: raw zips, manifest, acquisition log)
- **Phase 4bl-D — Multi-Day Raw Artefact QA / Raw Gate** (docs + local gitignored output: raw gate report)
- **Phase 4bl-E — Multi-Day Raw Successor-State Recording** (docs + local gitignored sibling successor-state JSON)
- **Phase 4bm-* — Multi-Day Normalization / Derived Artefact Arc**
- **Phase 4bn-* — Multi-Day Feature Generation / Gate Arc**
- **Phase 4bo-* — Multi-Day Label Generation / Gate Arc**
- **Phase 4bp-* — Multi-Day Split Policy Design / Artefact Recording**
- **Phase 4bq-* — Multi-Day Label Diagnostic Plan / Execution**
- **Later — ML feasibility memo**
- **Later — Baseline ML diagnostic**
- **Later — Failure interpretation / fallback selection memo**
- **Later — Strategy hypothesis under M0**
- **Later — Strategy spec**
- **Later — Backtest plan**
- **Later — Backtest execution**
- **Paper / shadow / live — much later, only after separate authorization**

Each phase requires its own authorization prompt, branch, implementation report, closeout, merge prompt, merge, and merge-closeout per the Phase 4bk-A workflow standard.

---

## 18. M0 and no-rescue integration

### 18.1 Data expansion is upstream of label diagnostics

Multi-day acquisition → multi-day gates → multi-day successor-state → multi-day split policy → multi-day label diagnostics. Phase 4bl-A is upstream of the diagnostic layer.

### 18.2 Label diagnostics are upstream of ML feasibility

Multi-day label diagnostics → ML feasibility memo → baseline ML diagnostic. Label diagnostics do not authorize ML feasibility; they are merely a prerequisite.

### 18.3 ML diagnostics are upstream of M0 strategy admission

Baseline ML diagnostic + multi-day evidence → ML feasibility memo → strategy hypothesis under M0. ML diagnostics do not bypass M0; they are merely a prerequisite to even drafting an M0-admissible hypothesis.

### 18.4 Data expansion does not bypass M0

Multi-day data does not bypass the Phase 4ak M0 twelve-clause gate. More data does not change M0 requirements; it merely makes M0 admissibility *conceivable*. M0 still requires mechanism source, non-price-only / structurally-distinct source, predicted Δ_R baseline-superiority theory, rejection-topology distance, cost realism (§11.6 = 8 bps per side preserved verbatim), opportunity-rate plausibility, edge-rate plausibility, data feasibility, governance compatibility, forbidden-rescue check, falsification criteria, and post-null cooldown.

### 18.5 More data does not rescue failed strategy families

R2 / F1 / D1-A / V2 / G1 / C1 first-spec hard rejects remain terminal. No multi-day dataset rescues them. The Phase 4ak post-null cooldown rule and the Phase 4al refined no-rescue rule remain binding. Alt-symbol expansion (if ever authorized) must be a new mechanism arc, not a rescue arc. The 5m research thread remains operationally closed per Phase 3t.

### 18.6 Labels are not signals

Labels remain not signals. Multi-day labels are still descriptive, not predictive by themselves.

### 18.7 Features are not signals

Features remain not signals. Multi-day features are still descriptive, not predictive by themselves.

### 18.8 Old failed strategy families remain closed

H0 FRAMEWORK ANCHOR, R3 BASELINE-OF-RECORD, R1a / R1b-narrow RETAINED — NON-LEADING, R2 FAILED — §11.6, F1 HARD REJECT, D1-A MECHANISM PASS / FRAMEWORK FAIL, V2 HARD REJECT — terminal, G1 HARD REJECT — terminal, C1 HARD REJECT — terminal. All preserved verbatim. Multi-day data does not change any verdict.

### 18.9 5m thread remains operationally closed

Phase 3t closure preserved. Multi-day aggTrades expansion does not reopen the 5m thread. The 5m thread closure is not about data scarcity; it is about strategy / signal admissibility on 5m bars, which remains closed regardless of data scope.

---

## 19. Explicit non-authorizations

Phase 4bl-A does **not** authorize any of the following:

- **Phase 4bl-B or any successor.** A future acquisition design / authorization memo is not authorized by Phase 4bl-A.
- **Any data acquisition.** Multi-day or single-day. Raw, normalized, derived, feature, label, or any other data family.
- **Any download.** No archive file may be downloaded. No checksum file may be downloaded. No request may be issued.
- **Any public endpoint call.** No call to `data.binance.vision`. No call to `fapi.binance.com`. No call to any other endpoint.
- **Any Binance API call.** No authenticated REST. No public REST. No WebSocket. No user stream.
- **Authenticated APIs.** No signed-request endpoint.
- **Private endpoints.** No `/fapi/v1/order`, `/fapi/v2/account`, `/fapi/v2/positionRisk`, `/fapi/v1/leverage`, `/fapi/v1/marginType`, `/fapi/v1/forceOrders`, listenKey lifecycle.
- **User streams.** No user data stream.
- **WebSockets.** No WebSocket connections.
- **Credentials.** No API keys, secrets, or other credentials may be created, read, written, or used.
- **`.env`.** No `.env` file may be created, read, written, or modified.
- **`.mcp.json`.** No `.mcp.json` file may be created, read, written, or modified.
- **MCP.** No MCP server may be enabled.
- **Graphify.** No Graphify access.
- **Raw artefact creation.** No raw zip, raw manifest, raw acquisition log, or raw sidecar may be created.
- **Manifest creation.** No new manifest may be created.
- **Gate execution.** No gate may be rerun or executed.
- **Successor-state artefact creation.** No new sibling successor-state JSON may be written.
- **Normalized / derived generation.** No normalization or derivation processing.
- **Feature generation.** No feature computation.
- **Label generation.** No label generation.
- **Split artefact creation.** No split or no-split-determination artefact.
- **Diagnostic artefact creation.** No diagnostic JSON.
- **Label diagnostic execution.** No diagnostics run.
- **Label statistics.** No statistics computed.
- **ML implementation.** No ML code path enabled.
- **ML training.** No model fit.
- **Model selection.** No model selected.
- **Feature ranking.** No ranking.
- **Meta-labeling.** No meta-labels.
- **Strategy implementation.** No strategy.
- **Signal computation.** No signal.
- **Backtesting.** No backtest.
- **Paper / shadow.** No paper / shadow operation.
- **Live-readiness.** No live-readiness work.
- **Deployment.** No deployment work.
- **Exchange-write.** No exchange-write.
- **Manifest transition.** No `research_eligible` flip, no `eligibility_gate_status` transition, no `chronological_split_policy` mutation on any actual manifest.

---

## 20. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

---

## 21. Preserved project locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max / mark-price stops
- M0 (Phase 4ak twelve-clause gate) remains binding
- Phase 4ak post-null cooldown rule remains binding
- Phase 4ak cooled-down families list remains binding (price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane)
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy remain binding
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains binding (never invoked)
- Phase 3p §4.7 strict integrity gate remains binding
- Phase 3r §8 mark-price gap governance remains binding
- Phase 3v §8 stop-trigger-domain governance remains binding
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance remain binding
- Phase 4j §11 metrics OI-subset partial-eligibility rule remains binding
- Phase 4k V2 backtest-plan methodology remains binding
- Phase 4p G1 strategy-spec remains binding
- Phase 4q G1 backtest-plan methodology remains binding
- Phase 4v C1 strategy-spec remains binding
- Phase 4w C1 backtest-plan methodology remains binding
- Phase 4bb-F canonical path policy remains binding

All prior phase results preserved verbatim.

---

## 22. Current-project-state update

`docs/00-meta/current-project-state.md` is updated narrowly with:

- a new Phase 4bl-A narrative paragraph prepended above the Phase 4bj-K paragraph;
- a new "Current phase:" Phase 4bl-A block;
- the prior Phase 4bj-K "Current phase:" block preserved as historical context per the documented standard.

The update must preserve:

- Phase 4bl-A is docs-only.
- Phase 4bl-A authorizes no acquisition.
- Phase 4bl-A authorizes no download.
- Phase 4bl-A authorizes no new local artefact.
- Phase 4bl-A authorizes no gate.
- Phase 4bl-A authorizes no diagnostics.
- Phase 4bl-A authorizes no ML / strategy / backtest / acquisition / paper-shadow / live / exchange-write.
- Recommended state remains paused unless the operator separately authorizes a future Phase 4bl-B acquisition authorization / design memo.

---

## 23. Final summary

Phase 4bl-A records the requirements for a future multi-day aggTrades expansion at memo level only. It evaluates seven candidate scopes (A–G), recommends Option B (BTCUSDT-only, at least 30 distinct UTC days) as the minimum viable expansion with Option C (BTCUSDT-only, 60–90 distinct UTC days) as the preferred upper bound, defines date-range / regime coverage requirements, defines symbol-scope requirements, defines data-source requirements (public archive only, no authenticated endpoints, no credentials), defines storage and namespace requirements (preserving the Phase 4bb-F canonical path policy), defines raw acquisition requirements (predeclared symbols, predeclared date list, predeclared source URL pattern, predeclared hash rules, predeclared sidecar format, predeclared acquisition log schema, predeclared failure / retry / missing-file policy), defines repeat pipeline requirements (raw acquisition, raw manifest, raw gate, raw successor-state, normalization, derived gate, derived successor-state, feature generation, feature gate, feature successor-state, label generation, label gate, label successor-state, multi-day split policy, split artefact, diagnostics plan / execution — each separately authorized), defines multi-day manifest / indexing requirements, defines multi-day split policy implications (train / validation / test vocabulary becomes admissible after multi-day data exists; strictly chronological; no random split; uniform 60s purge / embargo at the maximum label horizon; split by UTC day or contiguous date block; out-of-sample must be later in time; no repeated peeking; walk-forward acceptable; no symbol-leakage claims), defines minimum future diagnostic eligibility (multi-day raw + normalized + feature + label artefacts; multi-day gates passed; multi-day successor-state records; multi-day no-split or split artefact; predeclared diagnostics plan; output namespace; stop conditions; non-authorizations), records the relationship to the current one-day cell (preserved as pipeline-proving fixture; not research-grade for ML or strategy; inclusion / exclusion decision deferred to future Phase 4bl-B), records decision options and recommendation (primary: record this memo; conditional next not authorized: Phase 4bl-B; alternative: remain paused), defines the future phase ladder (Phase 4bl-B, 4bl-C, 4bl-D, 4bl-E, 4bm-*, 4bn-*, 4bo-*, 4bp-*, 4bq-*, ML feasibility memo, baseline ML diagnostic, failure interpretation memo, strategy hypothesis under M0, strategy spec, backtest plan, backtest execution, paper / shadow / live — all NOT authorized), records M0 and no-rescue integration (data expansion does not bypass M0; more data does not rescue failed strategy families; labels and features remain not signals; old failed strategy families remain closed; 5m thread remains operationally closed), and enumerates explicit non-authorizations (Phase 4bl-B and all successors, all acquisition, all downloads, all endpoint calls, all Binance APIs, all credentials, all `.env` / `.mcp.json`, all MCP / Graphify, all raw / manifest / gate / successor-state / normalized / derived / feature / label / split / diagnostic artefact creation, all label diagnostic execution, all label statistics, all ML / strategy / backtest / paper-shadow / live-readiness / deployment / exchange-write, all manifest transitions).

All 11 retained verdicts and 18+ project locks preserved verbatim. Phase 4bl-A is branch-complete only by this work; per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main`.

**Recommended state: remain paused** unless the operator separately authorizes a future Phase 4bl-B acquisition authorization / design memo. **No next phase authorized.**
