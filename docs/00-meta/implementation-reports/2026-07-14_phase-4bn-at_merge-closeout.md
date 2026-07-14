# Phase 4bn-AT — Merge-Closeout

## 1. Phase name and branch

Phase 4bn-AT — Top-of-Book Mechanism Admissibility and Bounce-Decomposition Preregistration.
Branch: `phase-4bn-at/top-of-book-mechanism-admissibility-bounce-preregistration`.

## 2. Phase type

Docs-only source-admissibility and scientific-preregistration decision; merge-only review and closeout. No market-data acquisition, capture, read, parse, normalization, alignment, label/feature construction, model, diagnostic, builder, or workflow.

## 3. Base SHA

`40377e231cc72318c884a11d258775912fe71b4c` (main == origin/main at phase start).

## 4. Pre-merge AT branch HEAD

`d3b216daca1809e9173c6e1a27e9ad50b14c39f1` (Phase 4bn-AT decision-memo commit).

## 5. Main / origin main before merge

Both `40377e231cc72318c884a11d258775912fe71b4c`.

## 6. Files added by AT

- `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-at_top-of-book-mechanism-admissibility-bounce-preregistration.md` (main memo, 61 sections, 524 insertions).
- `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-at_closeout.md` (closeout, 126 insertions).
- `docs/00-meta/implementation-reports/2026-07-14_phase-4bn-at_merge-closeout.md` (this merge-closeout).

## 7. Confirmation additions-only

`git diff --name-status main..<AT branch>` shows exactly two additions (the memo and closeout) with no modifications, deletions, or renames; this merge-closeout is a third addition committed on the AT branch before merge. No other path changes.

## 8. Confirmation no source/test/script/config/data/prior-report modification

Confirmed. No source, test, script, config, manifest, gate, sidecar, split, dataset, model configuration, or prior report was modified, renamed, or deleted. Nothing under `data/microstructure/` or `data/research/` is tracked or committed. `.claude/scheduled_tasks.lock` is not staged.

## 9. Project documents inspected by AT

`current-project-state.md` (stale past Phase 3k); `m0-mechanism-admissibility-gate.md`; process standards; Phase 4bn-AB/Y/AA/AC/AE/AH–AS lineage; the prior microstructure arc 4as/4at/4au/4av/4az/4ba/4bb-C/4bb-F; Phase 4bn-L storage/budget; `docs/04-data` timestamp/data-requirements/live-data/historical-data/dataset-versioning specs; `docs/06-execution-exchange` order-model/adapter docs; and committed source constants (`manifest.py`, `pre_v002_ml_dataset_contract.py`, `pre_v002_split_policy.py`, `canonical_paths.py`) — read, not modified.

## 10. External documentation sources inspected by AT

Accessed 2026-07-14 UTC, documentation / index / issue metadata only: `github.com/binance/binance-public-data` (README; MIT; aggTrades/klines/trades documented; `.CHECKSUM` SHA256); `data.binance.vision/?prefix=…/bookTicker/BTCUSDT/` (index — undocumented bookTicker tree exists); the S3 index-metadata endpoint (file-name/LastModified only; required-window coverage unconfirmed; earliest visible ~2023-05-16); `github.com/binance/binance-public-data/issues/305` (out-of-sequence futures bookTicker BTC/ETH; opened 2024-01-16, Closed, no maintainer fix); `dev.binance.vision/t/…/36122/1` (2025-08-16; archive ceased updating in 2024; no staff reply); the official WS book-ticker doc (SPA, not retrievable as static content — field contract taken from committed Phase 4au spec); Tier-3 (Tardis.dev, cryptodatadownload) as candidate-identification only, not admitted.

## 11. Confirmation merge review did not revisit external sources

Confirmed. This merge review performed **no** external browsing, no re-investigation of archive availability, no S3 object-content inspection, no file download to verify coverage, and no archive-index re-fetch. Only local `git` and local document reads were used.

## 12. Confirmation no data, archive, sample, endpoint, WebSocket, or local output was accessed

Confirmed. No bookTicker/aggTrades archive, sample, Parquet, CSV, or JSON market snapshot was downloaded, opened, or parsed; no Binance market-data endpoint was called; no WebSocket was opened; no local generated AQ/AR/model artefact was read; nothing under `data/` was opened. `test_rows_loaded = 0`.

## 13. Exact market-mechanism question

Did the clean 15-second last-trade directional-information result (Phase 4bn-AJ) represent genuine movement of the bid/ask midpoint, or was it substantially caused by predictable bid–ask trade-price bounce?

## 14. Why it was distinct from ML rescue

It is **model-free** (decomposes a price *label* into quote-referenced components; fits/scores/tunes/selects nothing), its object is a **measurement-validity** property of the 15s last-trade label rather than the AR predictive verdict, and it requires a **new data family** (top-of-book quotes) the aggTrades-only substrate cannot express — the deferred Phase 4bn-AK §16(b) `bookticker_midprice_data_admissibility_memo`. It cannot upgrade AR, revise AJ/AK/AR/AS metrics, reopen the stopped arc, or reuse the consumed holdout as confirmation.

## 15. Exact required historical date window

BTCUSDT / Binance USDⓈ-M / bookTicker. Validation 2024-10-02 … 2024-11-15 (45 UTC dates); embargo 2024-11-16 (excluded); holdout 2024-11-17 … 2024-11-30 (14 UTC dates). **Total required = 59 BTCUSDT UTC dates.** Train dates optional for a model-free descriptive decomposition.

## 16. Official archive-presence finding

A futures um daily bookTicker archive tree for BTCUSDT **exists** on the official host `data.binance.vision`, with `.CHECKSUM` companions present. This corrects the project's earlier Phase 4at "Hist: FALSE" position to "undocumented-but-present."

## 17. Tier-1-undocumented classification

The bookTicker family is **present in Tier-1 infrastructure** (the archive host) but **undocumented in Tier-1 specification**: absent from the public-data README and not retrievable from the API-docs single-page app. Its schema and its ordering defect are documented only at Tier-2 (issue #305) and Tier-3; its coverage/cessation are Tier-2 assertion, unconfirmed by Tier-1 metadata.

## 18. Known out-of-order defect

Official issue `binance/binance-public-data` #305 (opened 2024-01-16, **Closed with no documented maintainer repair**) confirms archived USDⓈ-M futures bookTicker records for BTC/ETH are **interleaved out of order by event_time and update_id**, and confirms the 7-column layout `update_id, best_bid_price, best_bid_qty, best_ask_price, best_ask_qty, transaction_time, event_time` (timestamps BIGINT Unix ms).

## 19. Coverage uncertainty and cessation report

Complete coverage of the required 2024-10-02 … 2024-11-30 window **could not be confirmed** from permitted Tier-1 index metadata (index probe truncated; earliest visible daily key ~2023-05-16). A Tier-2 Developer Community thread (2025-08-16) reports the bookTicker archive **ceased updating during 2024**, with no staff confirmation of the last available date. Under the default conservative rule, unestablished validation/holdout coverage does not qualify for retrospective admission.

## 20. Retrospective feasibility assessment

**Fails.** Coverage of all 59 dates unestablished; archived-file timestamp/sequencing semantics undocumented and documented-defective (#305); provenance/immutability/terms inadequate; the project's own prior admissibility finding recorded the family as unavailable; resolving the uncertainty would require prohibited data acquisition or content inspection (counts against admission). Checksums present but insufficient alone.

## 21. Prospective-only feasibility assessment

**Fails for this question.** Live `<symbol>@bookTicker` capture is technically/legally feasible and officially documented, but a 2026 capture is regime-non-comparable and — decisively — cannot be aligned to the 2024 aggTrades under examination, so it cannot answer the specific mechanism question; the operational/storage burden is disproportionate; fresh spread evidence risks relitigating completed cost/materiality decisions; and no currently-authorized action would change.

## 22. Provenance / terms / immutability assessment

MIT-licensed tooling; `.CHECKSUM` SHA256 companions enable bit-for-bit verification (checksum-first); but the archived bookTicker schema is undocumented in Tier-1, no immutability guarantee exists (families "may be added or removed by Binance over time"; the reported cessation illustrates this), no Tier-1 terms page governs the archived files specifically, and a single checksum match does not guarantee future re-fetch byte-identity. **Provenance inadequate for a causal-alignment-grade study.**

## 23. Frozen coverage requirements

BTCUSDT only; all 59 evaluation dates required; 0 missing dates; 0 partial UTC days; full UTC-day coverage per date with no intraday data gap > 60 s; 59/59 files present, each with a `.CHECKSUM` companion; no partial-coverage admission.

## 24. Frozen file-integrity requirements

0 checksum failures; 0 unreadable files; exact frozen 7-column schema (any deviation → dataset fail); exact-duplicate rate ≤ 0.5 % per day (else reject day); rows sharing `update_id` with differing quotes → quarantine; residual out-of-order rate ≤ 0.5 % after an evidence-preserving stable sort by (`transaction_time` asc, `update_id` asc); mandatory reorder-evidence bundle (original SHA256, original record count, pre-sort monotonicity diagnostics, exact sort keys, post-sort SHA256, post-sort monotonicity proof, duplicate policy applied); raw layer preserves source bytes; reorder without complete evidence → dataset fail.

## 25. Frozen quote-validity requirements

Bid and ask finite and positive; bid ≤ ask; crossed, locked, zero-quantity, and non-finite quotes excluded and **never repaired**; invalid share > 1.0 % on a day → reject the day; invalid share > 0.5 % across the segment → dataset partition failure.

## 26. Frozen timestamp / freshness requirements

Authoritative causal timestamp = `transaction_time` (T); secondary = `event_time` (E); equal `transaction_time` resolved by ascending `update_id` then original stable order; ms precision; UTC; date assignment by `transaction_time` UTC date; E/T disagreement > 1.0 %/day flags, > 5.0 %/day rejects the day; residual backward-time > 0.5 % after sort rejects the day; quote age ≤ 2000 ms for label construction; stale share > 5.0 % on a day → reject the day; > 2.0 % across the segment → dataset failure; no interpolation; no future backfill.

## 27. Frozen causal-alignment rule

For an observation timestamp t (trade `transaction_time`, or the 15s target = trade `transaction_time` + 15000 ms), select the latest valid quote with `transaction_time` ≤ t; never use a future quote; no nearest-neighbor that could select a future quote; no interpolation; no backfill; the selected quote must satisfy the 2000 ms freshness ceiling; both 15s endpoints must have valid support; alignment support ≥ 95 % for the segment; support < 90 % on a day → reject the day; support < 95 % for the segment → dataset failure; no target crosses a split or UTC-date boundary contrary to the pre-v002 split policy.

## 28. Frozen partition / dataset rejection rules

Reject a UTC day on any of: missing file, checksum failure, unreadable, schema deviation, invalid > 1.0 %, residual out-of-order > 0.5 %, E/T disagreement > 5.0 %, stale > 5.0 %, support < 90 %, duplicate > 0.5 %. Reject the dataset if any required date is rejected (all-59 requirement), or segment invalid > 0.5 %, or segment stale > 2.0 %, or segment support < 95 %, or any reorder lacks complete evidence. Minimum retained = 59/59. Fail-closed; **no threshold relaxation after data inspection**.

## 29. Frozen model-free descriptive registry

Model-free only (no fit/score/predict/calibrate/threshold-tune): quoted midpoint; quoted spread; spread in bps; half-spread bps; quote age; quote lifetime; trade-to-midpoint location (price/bps/half-spread); frozen historical trade-price 15s direction (descriptive reproduction, not a rerun/score); midpoint 15s direction; label-agreement matrix; exact and non-zero directional agreement; disagreement and opposite-direction rates; trade-only-movement rate; midpoint-only-movement rate; Cohen's κ (alongside raw rates); trade movement while midpoint unchanged; reversals inside a stable midpoint; movement relative to one spread and one half-spread; aggressor-side-conditioned disagreement; spread/freshness distributions by segment, UTC date, UTC month, hour, spread bucket, and quote-age bucket; quoted-spread and observable-friction-component audit.

## 30. Frozen bounce-decomposition metrics

Trade-only-movement share (trade dir ≠ 0 while midpoint dir = 0); opposite-direction share (both non-zero, opposite sign); sub-spread share (|15s trade move| ≤ one quoted spread) and sub-half-spread share; bid↔ask crossing without same-direction midpoint move; non-zero midpoint-support share; all additionally conditioned on aggressor side and on spread / quote-age buckets. These feed the outcome thresholds (§34).

## 31. Frozen quoted-spread audit scope

Top-of-book may describe: visible best bid/ask; midpoint; quoted spread and half-spread; spread variation; quote age and lifetime; visible top quantities; whether trades appear at/inside/outside the visible spread; a theoretical immediate-crossing spread component.

## 32. Explicit total-cost limitations

Top-of-book does **not** establish: true total trading cost; total slippage; queue position; partial-fill probability; market impact; hidden or excluded liquidity; depth beyond best bid/ask; order-size-dependent execution; decision-to-execution latency; account fee tier; complete realized round-trip cost. The terms "true trading cost" and "true-cost audit" must not be used as allowed claims (only when explaining why they are forbidden).

## 33. Frozen outcome categories

`BOUNCE_DOMINATED`; `MIDPOINT_CONFIRMED`; `MIXED_MECHANISM`; `DATA_INTEGRITY_FAILURE` (fail-closed, precedence). Exactly one is to be recorded by a later descriptive phase; `DATA_INTEGRITY_FAILURE` is evaluated first and overrides.

## 34. Frozen outcome thresholds

Definitions: A = non-zero directional agreement; TOM = trade-only-movement share; OPP = opposite-direction share; SUB = sub-spread trade-move share; MNZ = non-zero midpoint-support share. "Consistent" = holds on ≥ 80 % of admitted dates and both validation months (2024-10, 2024-11).

- **BOUNCE_DOMINATED:** A < 0.60 ∧ TOM ≥ 0.50 ∧ SUB ≥ 0.60 ∧ OPP ≥ 0.10, consistent.
- **MIDPOINT_CONFIRMED:** A ≥ 0.80 ∧ TOM ≤ 0.25 ∧ MNZ ≥ 0.60 ∧ OPP ≤ 0.05 ∧ SUB ≤ 0.40, consistent.
- **MIXED_MECHANISM:** integrity passes but neither pure region is satisfied consistently.
- **DATA_INTEGRITY_FAILURE:** any coverage/file/quote-validity/timestamp/freshness/alignment/dataset gate fails; fail-closed precedence.

No category relies on a single statistic; no category is a "success" that authorizes modeling.

## 35. Outcome-consequence table

| Future result | Consequence (frozen) |
|---|---|
| BOUNCE_DOMINATED | 15s last-trade result reinterpreted as substantially measurement-level bounce; no completed verdict rewritten; stopped ML arc stays stopped; no quote-feature model; no strategy/PnL/backtest; question closes unless a separate unrelated hypothesis is later proposed. |
| MIDPOINT_CONFIRMED | Genuine 15s midpoint-direction information descriptively supported; no old arc reopens; no model auto-authorized; no strategy/PnL/backtest; at most a later docs-only decision memo may consider a genuinely new hypothesis. |
| MIXED_MECHANISM | Both mechanisms material; no predictive claim upgraded; no threshold adjusted to force a cleaner category; at most a later docs-only interpretation memo; no model/strategy. |
| DATA_INTEGRITY_FAILURE | Stop the arc; quarantine/reject the dataset; no post-hoc threshold repair; no unapproved-source substitution; remain paused. |

No outcome may revise previous metrics, revise the locked 8/16 bps reference retrospectively, change `STOP_LONGHORIZON_ML_ARC`, or authorize a model/strategy/backtest/live work.

## 36. Confirmation no outcome automatically authorizes modeling or strategy work

Confirmed. None of the four outcomes authorizes a model, a quote-feature study, a strategy, PnL, backtesting, paper/shadow, or live work; none reopens a stopped arc or upgrades a predictive claim.

## 37. Negative-results codification summary

The AT appendix classifies: the clean 15s directional-information result (completed positive information finding); its economic thinness (2.47 %/1.20 % of 15s moves clear 16 bps round-trip); the spent single long-horizon follow-up; the stopped long-horizon ML arc (`STOP_LONGHORIZON_ML_ARC`); the consumed pre-v002 holdout (descriptive-only reuse); rejected strategy families (H0/R3/R1a/R1b-narrow/R2/F1/D1-A; 5m/V2/G1/C1); the v002-terminal and sealed-test reserves (untouched; `test_rows_loaded = 0`); the stopped top-of-book mechanism question (mechanism- and data-limited); unresolved spread/slippage/mid/depth/impact limitations; and the absolute Phase 4bn-AE §19 M0 boundary — each with status, unknowns, reconsideration evidence, insufficient evidence, same-data-reuse rule, future-phase type, and authorization state.

## 38. Expected-information-gain assessment

**Low.** The bounce hypothesis is already an acknowledged limitation (AJ/AK/AR/AS); refining "may embed" into "does/does not" is a general methodological lesson that does not require decomposing this specific spent result, changes no currently-authorized action, and can only be obtained from data that is inadmissible (retrospective) or non-comparable (prospective).

## 39. Cost / resource assessment

Both paths cost real engineering and storage — retrospective needs a checksum-verified acquirer, a mandatory evidence-preserving reorderer (#305), a strict causal aligner, and a descriptive computer (low-tens of GiB within Phase 4bn-L caps with the ≥500 GiB free-space preflight); prospective needs a sustained weeks-to-months capture/monitoring service. Payoff is low (§38); cost/benefit favors remaining paused.

## 40. Strongest argument for stopping

The "expensive autopsy" objection: neither `BOUNCE_DOMINATED` nor `MIDPOINT_CONFIRMED` changes any currently-authorized action; the only data that could decompose this specific result is inadmissible (retrospective) or cannot align to the 2024 trades (prospective); and prospective spread evidence risks relitigating completed cost verdicts. Low decision-relevant information gain plus inadmissible/non-comparable data ⇒ remain paused.

## 41. Exact decision

**STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE.**

## 42. Exact decision-precedence mapping

1. Retrospective first — evaluated, **fails** (coverage unestablished; sequencing defective/undocumented; provenance inadequate; resolving requires prohibited acquisition → counts against).
2. Prospective-only next — evaluated, **fails** (cannot answer the retrospective question; non-comparable; disproportionate; rescue/relitigation risk).
3. Neither credible and proportionate → **STOP**.
4. Not chosen because Candidate A was previously recommended — the independent review is non-binding and was weighed against the committed record.
5. Remaining paused is preferred over weak/incomplete/unverifiable data.
6. No fourth decision invented.
7. No genuine official-source contradiction blocks the decision (archive-exists vs README-silence resolved as "undocumented-but-present"), so the BLOCKED state is not used.
8. Documentation uncertainty unresolvable without prohibited acquisition counted against admission.

## 43. Allowed claims

The 15s label may embed bounce and cannot be determined on current admissible data; the futures um bookTicker archive exists but is Tier-1-undocumented, out-of-order-defective (#305), reportedly ceased in 2024, and of unconfirmed required-window coverage; the retrospective source is inadmissible and the prospective analogue cannot answer the specific question; a falsifiable admissibility/alignment/metric/outcome contract is preregistered for future genuinely-admissible data only.

## 44. Forbidden claims

No claim that the 15s result is/is not bounce; no "true trading cost" / "true-cost audit"; no revision of Phase 4bn-AJ/AK/AR/AS metrics, completed strategy rejections, materiality decisions, or the locked 8/16 bps reference by any future/prospective spread evidence (prospective-only); no describing the consumed pre-v002 holdout as unseen/untouched/independent confirmation or a sealed reserve; no reopening the stopped arc; no authorizing any model/quote-feature model/classifier/directional study/strategy/backtest/live work.

## 45. Confirmation locked 8/16 bps interpretation remains unchanged

Confirmed. The locked 8 bps per side / 16 bps round-trip reference remains binding and descriptive for all completed phases and verdicts; no new spread observation may retrospectively change it; future quoted-spread evidence, if ever obtained, applies prospectively only.

## 46. Confirmation STOP_LONGHORIZON_ML_ARC remains unchanged

Confirmed. `STOP_LONGHORIZON_ML_ARC` (Phase 4bn-AS) remains final; Phase 4bn-AR verdict and Phase 4bn-AS decision are unchanged.

## 47. Confirmation no successor execution

Confirmed. No successor execution phase of any kind is authorized by AT or this merge.

## 48. Confirmation no strategy/signals/PnL/backtest/replay/paper/shadow/live/exchange-write

Confirmed. None was performed, planned, or authorized.

## 49. Confirmation all authorization flags remain false

Confirmed. All published authorization flags remain `false`.

## 50. Confirmation research_eligible unchanged

Confirmed. `research_eligible` remains `False`; `eligibility_gate_status` remains `PENDING`.

## 51. Confirmation flip_research_eligible(...) was not invoked

Confirmed. The Phase 4aw `flip_research_eligible(...)` always-raising invariant was preserved and never invoked.

## 52. Validation commands and results

- `git diff --check` → clean.
- `git diff --name-status main..<AT branch>` → two additions only (memo, closeout); no modifications/deletions/renames.
- `git diff --stat main..<AT branch>` → 2 files changed, 650 insertions(+).
- `git ls-tree -r --name-only <AT branch> -- data/microstructure/` → empty.
- `git ls-tree -r --name-only <AT branch> -- data/research/` → empty.
- `git ls-files data/microstructure/` → empty; `git ls-files data/research/` → empty.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`; `git check-ignore -v data/research/` → `.gitignore:88`.
- Exact-string checks: decision `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` present in both docs; result-state `TOP_OF_BOOK_MECHANISM_ADMISSIBILITY_MEMO_COMPLETE__STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE__NO_SUCCESSOR_AUTHORIZED__REMAIN_PAUSED` present in both docs.
- `.claude/scheduled_tasks.lock` not staged; working tree clean except that transient lock.

## 53. Git status before merge

`?? .claude/scheduled_tasks.lock` only (plus the untracked, about-to-be-committed merge-closeout on the AT branch). main == origin/main == `40377e231cc72318c884a11d258775912fe71b4c`.

## 54. Merge method

`git merge --no-ff` of the AT branch into `main`. No squash. No rebase. `.claude/scheduled_tasks.lock` and any local data/generated artefact excluded.

## 55. Merge-closeout branch commit SHA

`c20eca6fab055792b521c395720b0db1026e9596` (merge-closeout committed on the AT branch before merge).

## 56. Merge commit SHA

`3094c07d0cb74c5ec971655c21dab68bba81fcd3` (`git merge --no-ff` of the AT branch into main).

## 57. SHA-finalization commit

This document's finalization commit on main (the commit that fills §55–§58); its SHA becomes the final main SHA in §58 and is confirmed against origin after push in the operator report.

## 58. Final main / origin SHA

Final main = the SHA-finalization commit (§57), pushed to origin so that `main == origin/main`. Both SHAs are recorded and confirmed equal in the Phase 4bn-AT operator report after `git push origin main`.

## 59. Final result state

`TOP_OF_BOOK_MECHANISM_ADMISSIBILITY_MEMO_MERGED_TO_MAIN__STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE_RECORDED__NO_SUCCESSOR_EXECUTION_AUTHORIZED__REMAIN_PAUSED`

## 60. Recommended state

**Remain paused.**

## 61. Remaining blockers before any future top-of-book work

- a genuinely admissible source;
- complete required-date coverage (59/59 BTCUSDT UTC dates);
- documented schema, timestamp, sequence, provenance, terms, and immutability;
- separate operator authorization;
- **no current source qualifies.**

## 62. Remaining blockers before any future ML work

- the current long-horizon ML arc is stopped (`STOP_LONGHORIZON_ML_ARC`);
- a fresh, unrelated hypothesis;
- a new preregistration;
- independent evidence;
- proof it is not rescue.

## 63. Remaining blockers before strategy / PnL / backtest / live

- the absolute Phase 4bn-AE §19 M0 gate (twelve M0 clauses, incl. M0.5 cost realism at 8/16 bps, M0.8 data feasibility, §7.D microstructure lane `NOT_RECOMMENDED_NOW`);
- spread / slippage / executable-mid / depth / impact unresolved;
- separate authorization for every capability.

## 64. Preserved project locks

`STOP_LONGHORIZON_ML_ARC` final; `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` final for this phase; Phase 4aw `flip_research_eligible(...)` always-raises and never invoked; `research_eligible` false/unchanged; all authorization flags false; Phase 4bb-F canonical sidecar policy unchanged; Phase 4bn-L storage/budget policy unchanged; Phase 4bn-AE claim scope unchanged; Phase 4bn-AE §19 M0 boundary absolute; Phase 4bn-AP contract unchanged; Phase 4bn-AQ dataset identity unchanged; Phase 4bn-AR metrics/verdict unchanged; Phase 4bn-AS stop decision unchanged; all completed strategy verdicts unchanged.

## 65. Explicit no-successor execution statement

**No successor execution is authorized.** This merge phase commits documentation only, records the STOP decision on main, and leaves the project paused. No data acquisition, capture, download, parsing, normalization, alignment, label/feature construction, model, strategy, signal, PnL, backtest, replay, simulated fill, paper/shadow/live/exchange-write, or successor phase of any kind is authorized.

## 66. Explicit note on ChatGPT handoff

ChatGPT chat branching and handoff preparation should happen only **after** this merge is complete and the final main SHA is known. No ChatGPT branching handoff file is created during this merge phase.
