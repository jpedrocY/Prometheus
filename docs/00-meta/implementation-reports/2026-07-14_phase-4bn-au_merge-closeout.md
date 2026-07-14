# Phase 4bn-AU — Merge-Closeout

## 1. Phase name and branch

Phase 4bn-AU — Post-AT Project-Direction Review and Progress-Successor Selection.
Source branch: `phase-4bn-au/post-at-project-direction-progress-successor-selection`.
Target branch: `main`.

## 2. Phase type and merge action

Docs-only project-direction review, independent-review assessment, provisional successor recommendation, and bounded successor scoping. Merge-only review and closeout: no source, test, script, config, data, manifest, gate, sidecar, split, or model change; no data acquisition/read; no model, diagnostic, builder, backtest, replay, or runtime process. The merge brings four documentation files onto `main` via a `--no-ff` merge commit; documentation only.

## 3. Risk tier

Tier 1 (Full Phase) per `docs/00-meta/process/phase-risk-tiering-standard.md` — highest ceremony because it concerns scientific direction, evidence-reserve reasoning, and successor selection, though it mutates no eligibility, manifest, verdict, or lock and records a recommendation only.

## 4. Source and target branches

- Source: `phase-4bn-au/post-at-project-direction-progress-successor-selection`.
- Target: `main`.

## 5. Pre-merge main / base SHA

`6ba589bc704e06f28ba30039aff8ead6523c5031` (main == origin/main at merge start; tip after the Phase 4bn-AT merge-closeout SHA-finalization commit).

## 6. Original AU phase commit SHA

`68783b86ec07d66fbdd6745e8a2c0f31b0e065b2` (the single Phase 4bn-AU phase commit that added the three AU documents).

## 7. Merge-closeout branch commit SHA

`TO_BE_FILLED_AFTER_MERGE` (this merge-closeout's own commit on the AU branch, `docs(phase-4bn-au): add merge closeout`).

## 8. Merge commit SHA

`TO_BE_FILLED_AFTER_MERGE` (the `--no-ff` merge of the AU branch into `main`).

## 9. SHA-finalization commit statement

The placeholders in §7 and §8 are replaced on `main` by a narrow SHA-finalization update to this file, committed as `docs(phase-4bn-au): finalize merge closeout shas`. Its exact SHA equals the resulting final `main` / `origin/main` tip and is recorded in the final operator report and Git log. The finalization commit's own SHA is not embedded inside the commit that creates it.

## 10. Final main / origin/main statement

After the SHA-finalization commit is pushed, `main == origin/main` equals that SHA-finalization commit. Both SHAs are recorded and confirmed equal in the Phase 4bn-AU operator report after `git push origin main`.

## 11. Merge method

`git merge --no-ff` of the AU branch into `main`, message `docs(phase-4bn-au): merge post-AT project-direction review`. No squash, no rebase, no amend, no fast-forward, no hook-skipping, no signing-disable, no force push. `.claude/scheduled_tasks.lock` and any local generated artefact excluded.

## 12. Files brought forward

Four documentation files, all under `docs/00-meta/implementation-reports/`:
1. `2026-07-14_phase-4bn-au_post-at-project-direction-progress-successor-selection.md` (main decision memo, 32 sections).
2. `2026-07-14_phase-4bn-au_fable-independent-review-assessment.md` (independent-review assessment).
3. `2026-07-14_phase-4bn-au_closeout.md` (phase closeout).
4. `2026-07-14_phase-4bn-au_merge-closeout.md` (this merge-closeout).

## 13. Additions-only confirmation

`git diff --name-status main..<AU branch>` shows exactly three additions (the memo, the Fable assessment, and the closeout) with no modifications, deletions, or renames; this merge-closeout is a fourth addition committed on the AU branch before merge. No existing file was modified, renamed, or deleted. No `data/microstructure/` or `data/research/` path is tracked or committed. `.claude/scheduled_tasks.lock` is not staged.

## 14. Diff summary

- Pre-merge (`main..<AU branch>`): 3 files changed, 507 insertions(+); `git diff --check` clean.
- Post-merge (`<base>..HEAD`, after this merge-closeout is included): four added documents; no modification/deletion/rename beyond the single later SHA-finalization edit of this merge-closeout.

## 15. AU decision and provisional successor recommendation

Phase 4bn-AU selected provisional recommendation state `RECOMMEND_FORWARD_LOOKING_EPISTEMIC_PROTOCOL_AND_EVIDENCE_BUDGET_SUCCESSOR` (Candidate E). Proposed successor: **Phase 4bn-AV — Evidence-Budget Ledger, Scarce-Reserve Spending Authority, and Late-Inadmissibility Consequence Protocol** (docs-only). This is a recommended next direction and a proposed future phase only — not authorized work.

## 16. Candidate A versus Candidate E conclusion

Both premises held.
- **Candidate A had real missing runtime components:** reconciliation engine (absent; specified in the Phase 4e memo), fake-exchange divergence injection (partial; `FakeOrderOutcome.REJECTED` defined but never emitted), restart re-hydration (the documented restart-safety invariant is enforced only in test code, not in any production function — the cleanest standalone fake/local-testable slice), and audit-export/redaction (absent).
- **Candidate E had three genuine governance gaps:** (1) no standing evidence-budget / scarce-reserve **ledger**; (2) no named reserve-spending **authority** or binding pre-spend review/quorum; (3) no **late-inadmissibility-discovery consequence** rule.
- **E was selected** because the evidence-governance gaps affect the **next possible research step** (what may be spent, who authorizes spending the sealed test / v002 terminal, is it rescue, what if a source proves inadmissible after reliance) and guard the project's scarcest irreplaceable asset, whereas the runtime defects remain **dormant and off the current critical path** (nothing is authorized to run the runtime, so A's defect is latent while paused) and A carries deployment-shaped sunk-cost drift.
- **A remains the strong runner-up.**

## 17. Fable independent-review standing

`POST_AT_INDEPENDENT_REVIEW_PROVIDED__FABLE_RANKING_A_GT_B_GT_D_GT_C__CANDIDATE_E_RAISED`. The Fable review is operator-supplied, bounded, non-binding, and subordinate to committed repository evidence; it authorizes no phase or capability. Phase 4bn-AU revised Fable's ranking to E > A > B > C > D — promoting E to first and A to Fable's first-place position (second) — consistent with Fable's own stated view that "E could contend with A for first place."

## 18. Strongest counterargument

E's surrounding epistemic substance already exists (M0, Phase 4bn-AE preregistration, Phase 4bn-AS anti-rescue, Phase 4bn-Y split/holdout/sealed-reserve structure) and worked twice in practice (AS refused a scarce-reserve spend; AT caught inadmissibility before acquisition), so the three remaining holes are preventive rather than acute — whereas A's restart re-hydration slice is a concrete, falsifiable, provably-missing safety defect with a perfect fake/local acceptance test, and a paused project writing governance risks substituting motion for progress. This keeps A a close second rather than dismissed; it does not prevail because the runtime defect is latent and off the current critical path while the evidence-governance gap is live at the next research step, E's three holes are genuinely-absent binding mechanisms rather than restatements, E carries no deployment-shaped drift, and protecting irreplaceable evidence outranks hardening a dormant subsystem under the decisive question.

## 19. AV kill criteria

If Phase 4bn-AV is ever separately authorized, kill it if: authoring it requires re-legislating existing M0 / Phase 4bn-AE / Phase 4bn-AS / Phase 4bn-Y machinery (i.e., the only content would be duplication → the gap was not real → STOP); the ledger/authority/late-rule cannot be defined without designing a new strategy, hypothesis, or data source; it degenerates into an open-ended governance-writing loop with no bounded completion; or it would require touching data, code, the manifest, or any existing governance file. (For an A-shaped alternative instead: kill if the acceptance test requires market data, network access, credentials, exchange-write semantics, or assumptions about a particular strategy's behavior — Fable's clean-kill criterion, adopted in substance.)

## 20. Confirmation that AV remains unauthorized

Confirmed. Phase 4bn-AU does not authorize Phase 4bn-AV, and this merge does not authorize it. AV is proposed only. `No successor execution is authorized by the Phase 4bn-AU merge.`

## 21. Confirmation that no data or evidence reserve was touched

Confirmed. No market data, archive, sample, Parquet, CSV, or JSON snapshot was read or acquired; no local generated research output was inspected; the v002 terminal window and sealed test were not opened, read, inspected, enumerated for content, scored, loaded, or consumed; nothing under `data/microstructure/` or `data/research/` was opened. `test_rows_loaded = 0` posture preserved. The pre-v002 predictive holdout remains consumed; the v002 terminal window and sealed test remain scarce untouched reserves.

## 22. Confirmation that no executable surface changed

Confirmed. No source, test, script, config, manifest, gate, sidecar, split, dataset, or model configuration was modified. Only documentation files were added under `docs/00-meta/implementation-reports/`.

## 23. Validation results

- `git status --short` → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check main..<AU branch>` → clean.
- `git diff --name-status main..<AU branch>` → three additions only; no modification/deletion/rename.
- `git diff --stat main..<AU branch>` → 3 files changed, 507 insertions(+).
- `git show --stat --oneline 68783b86ec07d66fbdd6745e8a2c0f31b0e065b2` → the three AU documents, 507 insertions.
- Post-merge: `git diff --name-status 6ba589bc704e06f28ba30039aff8ead6523c5031..HEAD` → four added documents; `git diff --check` → clean.
- `pytest`, Ruff, mypy, project scripts, data workflows, models, diagnostics, backtests, and runtime processes were **not run** because no executable surface changed and execution is outside merge scope.

## 24. Manifest, eligibility, M0, split, sidecar, storage, and evidence-lock preservation

Preserved unchanged: manifest immutability (`flip_research_eligible(...)` always-raises, never invoked; `research_eligible = False`; `eligibility_gate_status = PENDING`); all published authorization flags `false`; the Phase 4bn-AE §19 M0 boundary (absolute); locked cost assumptions (8 bps/side · 16 bps round-trip); dataset identities and hashes; split and holdout policies; Phase 4bb-F sidecar policy and Phase 4bn-L storage/budget policy; `STOP_LONGHORIZON_ML_ARC` and `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct, not rewritten); all prior strategy verdicts (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A; 5m / V2 / G1 / C1) and retained-evidence classifications; all previous implementation reports.

## 25. Exact post-merge result state

`POST_AT_PROJECT_DIRECTION_REVIEW_MERGED_TO_MAIN__RECOMMEND_FORWARD_LOOKING_EPISTEMIC_PROTOCOL_AND_EVIDENCE_BUDGET_SUCCESSOR_RECORDED__FABLE_INDEPENDENT_REVIEW_ASSESSED__NO_SUCCESSOR_EXECUTION_AUTHORIZED`

## 26. Required post-merge operator posture

Remain paused with respect to execution. Return this merge-closeout and the final operator report to ChatGPT for review before deciding whether to authorize Phase 4bn-AV.

`No successor execution is authorized by the Phase 4bn-AU merge.`

`Phase 4bn-AV requires separate ChatGPT review, explicit operator authorization, and a new Claude Code prompt.`
