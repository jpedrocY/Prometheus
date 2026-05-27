"""Phase 4bm-W — Multi-Day v002 descriptive diagnostics runner.

Standalone offline orchestrator authorised by the Phase 4bm-W authorization
prompt. Runs the strictly descriptive / structural read-only diagnostics over
the existing 90-day v002 BTCUSDT label/feature family, applies the Phase 4bm-U
recorded chronological split policy, and writes local gitignored diagnostic
outputs (summary JSON + paired canonical Phase 4bb-F sidecar, per-split /
per-day CSV tables, and a diagnostics manifest + sidecar) under the approved
research-output namespace
``data/research/microstructure/diagnostics/phase-4bm-w/``.

This script:

- Python standard library + numpy + pyarrow + the Phase 4bm-W
  ``prometheus.research.microstructure`` diagnostics modules only;
- NO network access; NO credentials; NO ``.env``; NO ``.mcp.json``;
  NO MCP / Graphify;
- NO modification of any label / feature parquet / sidecar / manifest /
  gate report / successor-state JSON; reads ``data/microstructure/``
  read-only and writes only under the research-output namespace;
- Phase 4bm-W runs descriptive diagnostics only. It does not run ML, does not
  define or run strategy, does not run backtests, does not authorize
  acquisition, performs no feature / model / threshold selection, and does not
  use the test holdout for tuning or design.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure.descriptive_diagnostics_v002 import (  # noqa: E402
    DiagnosticsInput,
    run_descriptive_diagnostics,
)
from prometheus.research.microstructure.diagnostics_report_v002 import (  # noqa: E402
    VERDICT_ERROR,
    VERDICT_PASS,
    build_payload,
    write_outputs,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 4bm-W multi-day v002 descriptive diagnostics runner"
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
        "--output-root", type=Path, default=None,
        help="research-output namespace root (defaults to the approved path)",
    )
    args = parser.parse_args(argv)
    repo_root: Path = args.repo_root.resolve()
    if not (repo_root / "src" / "prometheus").exists():
        raise SystemExit(
            f"repo_root does not look like the Prometheus repo: {repo_root}"
        )

    manifests = repo_root / "data" / "microstructure" / "manifests"
    inp = DiagnosticsInput(
        repo_root=repo_root,
        label_manifest_path=manifests
        / "microstructure_labels_aggtrades_v001__v002.json",
        feature_manifest_path=manifests
        / "microstructure_features_aggtrades_v001__v002.json",
    )
    output_root: Path = (
        args.output_root
        if args.output_root is not None
        else repo_root
        / "data"
        / "research"
        / "microstructure"
        / "diagnostics"
        / "phase-4bm-w"
    )

    print(f"[phase-4bm-w] repo_root       : {repo_root}", flush=True)
    print(f"[phase-4bm-w] code_commit_sha : {args.code_commit_sha}", flush=True)
    print(f"[phase-4bm-w] output_root     : {output_root}", flush=True)
    print("[phase-4bm-w] running descriptive diagnostics over 90 partitions...",
          flush=True)

    created_at = int(time.time() * 1000)
    try:
        run = run_descriptive_diagnostics(inp)
        payload = build_payload(
            run,
            created_at_unix_ms=created_at,
            code_commit_sha=args.code_commit_sha,
        )
        written = write_outputs(
            output_root,
            payload,
            created_at_unix_ms=created_at,
            code_commit_sha=args.code_commit_sha,
        )
    except Exception as exc:  # noqa: BLE001 - report-level error capture
        print(f"[phase-4bm-w] verdict         : {VERDICT_ERROR}", flush=True)
        print(f"[phase-4bm-w] error           : {exc!r}", flush=True)
        return 3

    verdict = payload["diagnostics_verdict"]
    print(f"[phase-4bm-w] verdict         : {verdict}", flush=True)
    for f in payload["verdict_blocking_failures"]:
        print(f"[phase-4bm-w]   BLOCKING: {f}", flush=True)
    for c in payload["verdict_caveats"]:
        print(f"[phase-4bm-w]   caveat  : {c}", flush=True)
    print(
        f"[phase-4bm-w] summary json    : {written.summary_json_path}",
        flush=True,
    )
    print(
        f"[phase-4bm-w] summary sha256  : {written.summary_json_sha256}",
        flush=True,
    )
    print(
        f"[phase-4bm-w] summary sidecar : {written.summary_sidecar_path}",
        flush=True,
    )
    print(
        f"[phase-4bm-w] sidecar sha256  : {written.summary_sidecar_sha256}",
        flush=True,
    )
    print(
        f"[phase-4bm-w] manifest json   : {written.manifest_json_path}",
        flush=True,
    )
    print(
        f"[phase-4bm-w] manifest sha256 : {written.manifest_json_sha256}",
        flush=True,
    )
    print(
        f"[phase-4bm-w] manifest sidecar: {written.manifest_sidecar_path}",
        flush=True,
    )
    print(
        f"[phase-4bm-w] msidecar sha256 : {written.manifest_sidecar_sha256}",
        flush=True,
    )
    for tp in written.table_paths:
        print(f"[phase-4bm-w] table           : {tp}", flush=True)

    # Verdict is descriptive-only; PASS and PASS_WITH_CAVEATS are both
    # successful completions. Only FAIL / ERROR return non-zero.
    if verdict in (VERDICT_PASS, "DESCRIPTIVE_DIAGNOSTICS_PASS_WITH_CAVEATS"):
        return 0
    return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
