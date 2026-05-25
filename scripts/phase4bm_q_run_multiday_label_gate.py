"""Phase 4bm-Q — Multi-Day v002 Label-Family Eligibility Gate runner.

Standalone offline orchestrator authorised by the Phase 4bm-Q
authorization prompt. Runs the read-only Phase 4bm-Q check suite over
the existing Phase 4bm-O v002 label artefacts and (when
``--write-report`` is set, default) emits a deterministic local
gitignored gate report + paired canonical Phase 4bb-F sidecar under
``data/microstructure/gate-reports/labels/``.

This script:

- Python standard library + pyarrow + the new
  ``prometheus.research.microstructure`` Phase 4bm-Q modules only;
- NO network access; NO credentials; NO ``.env``; NO ``.mcp.json``;
  NO MCP / Graphify;
- NO modification of any label parquet / label sidecar / label
  manifest / feature manifest / derived manifest / raw manifest /
  gate report / successor-state JSON; the only file the script writes
  is the new gate report JSON + paired sidecar under
  ``data/microstructure/gate-reports/labels/``;
- atomic write-then-rename via ``tempfile.mkstemp`` + ``os.replace``;
  refuse-to-overwrite at the writer level;
- strict fail-closed: any precondition / check / immutability failure
  is recorded explicitly in the gate report.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure import (  # noqa: E402
    MULTIDAY_LABEL_GATE_VERDICT_PASS,
    MultidayLabelGateInput,
    run_multiday_label_family_gate,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 4bm-Q multi-day v002 label-family eligibility gate runner"
    )
    parser.add_argument(
        "--repo-root", type=Path, default=_REPO_ROOT,
        help="repository root (defaults to script's parent)",
    )
    parser.add_argument(
        "--code-commit-sha", type=str, default="unknown",
        help="40-char lowercase hex code commit SHA (or 'unknown')",
    )
    parser.add_argument(
        "--write-report", action="store_true", default=True,
        help="write the gate report (default True)",
    )
    parser.add_argument(
        "--no-write-report", dest="write_report", action="store_false",
        help="run the check suite but do not write any output file",
    )
    args = parser.parse_args(argv)
    repo_root: Path = args.repo_root.resolve()
    if not (repo_root / "src" / "prometheus").exists():
        raise SystemExit(
            f"repo_root does not look like the Prometheus repo: {repo_root}"
        )

    print(f"[phase-4bm-q] repo_root         : {repo_root}", flush=True)
    print(f"[phase-4bm-q] code_commit_sha   : {args.code_commit_sha}", flush=True)
    print(f"[phase-4bm-q] write_report      : {args.write_report}", flush=True)

    ms = repo_root / "data" / "microstructure"
    manifests = ms / "manifests"
    gate_raw = ms / "gate-reports" / "raw"
    gate_norm = ms / "gate-reports" / "normalized"
    gate_feat = ms / "gate-reports" / "features"
    succ = ms / "successor-state"
    bm_d_basename = (
        "microstructure_normalized_aggtrades_v001__v002__"
        "phase-4bm-d__1779056065059__57e1c97e6e93.json"
    )
    bm_f_basename = (
        "microstructure_normalized_aggtrades_v001__v002__"
        "stage3_research_eligible__phase-4bm-f.json"
    )
    bl_d_r_basename = (
        "microstructure_raw_aggtrades_v001__v002__"
        "phase-4bl-d-r__1778717359124__69e45280f080.json"
    )
    bl_e_basename = (
        "microstructure_raw_aggtrades_v001__v002__"
        "stage2_raw_admissible__phase-4bl-e.json"
    )
    bm_j_basename = (
        "microstructure_features_aggtrades_v001__v002__"
        "phase-4bm-j__1779475950843__3212722a7ffd.json"
    )
    bm_l_basename = (
        "microstructure_features_aggtrades_v001__v002__"
        "stage5_research_use_approved__phase-4bm-l.json"
    )

    # The Phase 4bm-J gate report and Phase 4bm-L successor-state filenames
    # follow the canonical Phase 4bb-F naming with phase-specific timestamps.
    # If the operator wishes to override either basename, they can edit this
    # script; otherwise the resolver below picks the only matching file under
    # the corresponding canonical directory.
    def _resolve_unique(directory: Path, *, prefix: str, suffix: str) -> Path:
        candidates = sorted(
            p for p in directory.glob(f"{prefix}*{suffix}") if not p.name.endswith(".sha256.sha256")
        )
        if not candidates:
            raise SystemExit(
                f"no matching file under {directory} (prefix={prefix!r}, suffix={suffix!r})"
            )
        # Prefer the most recent one if multiple exist.
        return candidates[-1]

    # Resolve Phase 4bm-J gate report (the actual basename may differ from
    # the constant above; try the constant first and fall back to glob).
    bm_j_path = gate_feat / bm_j_basename
    if not bm_j_path.exists():
        bm_j_path = _resolve_unique(
            gate_feat,
            prefix="microstructure_features_aggtrades_v001__v002__phase-4bm-j",
            suffix=".json",
        )
    bm_l_path = succ / bm_l_basename
    if not bm_l_path.exists():
        bm_l_path = _resolve_unique(
            succ,
            prefix=(
                "microstructure_features_aggtrades_v001__v002__"
                "stage5_research_use_approved__phase-4bm-l"
            ),
            suffix=".json",
        )

    inp = MultidayLabelGateInput(
        repo_root=repo_root,
        label_manifest_path=manifests
        / "microstructure_labels_aggtrades_v001__v002.json",
        label_manifest_sidecar_path=manifests
        / "microstructure_labels_aggtrades_v001__v002.json.sha256",
        labels_root=ms / "labels" / "microstructure_labels_aggtrades_v001__v002",
        feature_manifest_path=manifests
        / "microstructure_features_aggtrades_v001__v002.json",
        feature_manifest_sidecar_path=manifests
        / "microstructure_features_aggtrades_v001__v002.json.sha256",
        phase_4bm_j_gate_report_path=bm_j_path,
        phase_4bm_j_gate_sidecar_path=Path(str(bm_j_path) + ".sha256"),
        phase_4bm_l_successor_state_path=bm_l_path,
        phase_4bm_l_successor_state_sidecar_path=Path(str(bm_l_path) + ".sha256"),
        derived_manifest_path=manifests
        / "microstructure_normalized_aggtrades_v001__v002.json",
        derived_manifest_sidecar_path=manifests
        / "microstructure_normalized_aggtrades_v001__v002.json.sha256",
        raw_manifest_path=manifests
        / "microstructure_raw_aggtrades_v001__v002.json",
        acquisition_log_path=manifests
        / "microstructure_raw_aggtrades_v001__v002_acquisition_log.json",
        phase_4bm_d_gate_report_path=gate_norm / bm_d_basename,
        phase_4bm_d_sidecar_path=gate_norm / (bm_d_basename + ".sha256"),
        phase_4bm_f_successor_state_path=succ / bm_f_basename,
        phase_4bm_f_successor_state_sidecar_path=succ / (bm_f_basename + ".sha256"),
        phase_4bl_d_r_gate_report_path=gate_raw / bl_d_r_basename,
        phase_4bl_e_successor_state_path=succ / bl_e_basename,
        output_root=ms / "gate-reports" / "labels",
        code_commit_sha=args.code_commit_sha,
        write_report=args.write_report,
    )

    from prometheus.research.microstructure import (  # noqa: E402
        MULTIDAY_LABEL_GATE_CHECK_ORDER,
    )
    print(
        f"[phase-4bm-q] running check suite "
        f"({len(MULTIDAY_LABEL_GATE_CHECK_ORDER)} checks)...",
        flush=True,
    )
    result = run_multiday_label_family_gate(inp)

    n = len(result.results)
    p = sum(1 for r in result.results if r.status.value == "PASS")
    f = sum(1 for r in result.results if r.status.value == "FAIL")
    e = sum(1 for r in result.results if r.status.value == "ERROR")
    na = sum(1 for r in result.results if r.status.value == "NOT_APPLICABLE")
    print(
        f"[phase-4bm-q] check results: total={n} PASS={p} FAIL={f} ERROR={e} "
        f"NOT_APPLICABLE={na}",
        flush=True,
    )
    if f or e:
        for r in result.results:
            if r.status.value in {"FAIL", "ERROR"}:
                print(
                    f"[phase-4bm-q] {r.status.value:>5} {r.check_id} ({r.group}): "
                    f"expected={r.expected} observed={r.observed}",
                    flush=True,
                )
    print(f"[phase-4bm-q] gate_verdict     : {result.report.gate_verdict}", flush=True)
    print(f"[phase-4bm-q] overall_status   : {result.report.overall_status}", flush=True)

    if args.write_report:
        print(f"[phase-4bm-q] report path      : {result.report_path}", flush=True)
        print(f"[phase-4bm-q] report sha256    : {result.report_sha256}", flush=True)
        print(f"[phase-4bm-q] report size      : {result.report_size_bytes} bytes", flush=True)
        print(f"[phase-4bm-q] sidecar path     : {result.sidecar_path}", flush=True)
        print(f"[phase-4bm-q] sidecar sha256   : {result.sidecar_sha256}", flush=True)
        print(f"[phase-4bm-q] sidecar size     : {result.sidecar_size_bytes} bytes", flush=True)

    if result.report.gate_verdict != MULTIDAY_LABEL_GATE_VERDICT_PASS:
        return 2
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
