"""Shared mini-fixture helpers for the Phase 4bd normalization tests.

Builds on the Phase 4bb-C ``_eligibility_fixtures.py`` and adds a
small ``NormalizeFixtureBundle`` that exposes the additional
``output_root``, ``manifests_root``, and Phase 4bb-D-style cited gate
report fields used by the normalizer's input contract.

All fixtures live entirely within pytest ``tmp_path`` directories
that are arranged to look like ``data/microstructure/...``. They
never touch the real project ``data/microstructure/`` tree.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ._eligibility_fixtures import (
    FixtureBundle,
    build_happy_fixture,
)

CITED_GATE_REPORT_ID = "microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c"
CITED_GATE_REPORT_SHA = "96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423"
CITED_GATE_CODE_COMMIT_SHA = "aa612ba2778c97a5150b80064244b90d024bfa54"


@dataclass(frozen=True)
class NormalizeFixtureBundle:
    """Paths used by Phase 4bd tests."""

    eligibility_bundle: FixtureBundle
    output_root: Path
    manifests_root: Path
    cited_gate_report_id: str
    cited_gate_report_sha256: str
    cited_gate_code_commit_sha: str
    cited_gate_report_path: Path | None
    code_commit_sha: str


def build_normalize_fixture(
    tmp_path: Path,
    *,
    write_local_gate_report: bool = True,
    rows: list | None = None,
) -> NormalizeFixtureBundle:
    """Build a complete normalization mini-fixture under *tmp_path*."""
    bundle = build_happy_fixture(tmp_path, rows=rows)
    # output_root must resolve under data/microstructure/normalized/ per the
    # Phase 4bd path discipline. The orchestrator further appends the family
    # subdirectory inside derive_normalized_output_path.
    output_root = bundle.microstructure_root / "normalized"
    output_root.mkdir(parents=True, exist_ok=True)
    manifests_root = bundle.manifest_path.parent

    gate_report_path: Path | None = None
    if write_local_gate_report:
        gate_dir = bundle.microstructure_root / "gate-reports" / "gate-reports"
        gate_dir.mkdir(parents=True, exist_ok=True)
        gate_report_path = gate_dir / "phase4bb-d-gate-report.json"
        # We only need the file's SHA to match the cited SHA. We synthesise
        # bytes whose SHA happens to equal CITED_GATE_REPORT_SHA by storing
        # the cited SHA itself as the placeholder (the recomputed SHA will
        # NOT match the cited SHA). For tests that need a SHA-match, we
        # use a synthetic cited SHA recomputed from these bytes.
        # In practice, tests that exercise the local-report verify path
        # should pass write_local_gate_report=False and rely on tracked
        # citation only, OR override cited_gate_report_sha256 with the
        # recomputed SHA of this synthetic file.
        gate_report_path.write_text(
            "{\"phase4bb-d-test\": \"placeholder\"}\n", encoding="utf-8"
        )

    return NormalizeFixtureBundle(
        eligibility_bundle=bundle,
        output_root=output_root,
        manifests_root=manifests_root,
        cited_gate_report_id=CITED_GATE_REPORT_ID,
        cited_gate_report_sha256=CITED_GATE_REPORT_SHA,
        cited_gate_code_commit_sha=CITED_GATE_CODE_COMMIT_SHA,
        cited_gate_report_path=gate_report_path,
        code_commit_sha=bundle.code_commit_sha,
    )


def synthetic_gate_report_with_sha(tmp_path: Path) -> tuple[Path, str]:
    """Write a synthetic gate-report file and return ``(path, recomputed_sha)``."""
    bundle = build_happy_fixture(tmp_path)
    gate_dir = bundle.microstructure_root / "gate-reports" / "gate-reports"
    gate_dir.mkdir(parents=True, exist_ok=True)
    gate_report_path = gate_dir / "synthetic-gate-report.json"
    payload = b"{\"synthetic\": true}\n"
    gate_report_path.write_bytes(payload)
    recomputed = hashlib.sha256(payload).hexdigest()
    return gate_report_path, recomputed
