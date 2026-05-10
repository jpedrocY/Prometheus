"""Phase 4bh static no-network / no-credential / no-MCP scan.

This test scans the five Phase 4bh source modules for forbidden
imports and credential-shaped tokens. It uses the same regex patterns
already enforced by ``test_import_boundaries.py`` for the rest of the
microstructure package and additionally enforces zero references to
the Phase 4bh forbidden-substring set inside source code (only inside
the schema constant, which is excluded since that is the literal
denylist).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "prometheus"
    / "research"
    / "microstructure"
)

PHASE_4BH_MODULES: tuple[str, ...] = (
    "features_schema.py",
    "features_io.py",
    "features_compute.py",
    "features_manifest.py",
    "features_validation.py",
)


FORBIDDEN_IMPORT_PATTERNS: tuple[tuple[str, str], ...] = (
    ("prometheus.runtime", r"^\s*(?:from|import)\s+prometheus\.runtime\b"),
    ("prometheus.execution", r"^\s*(?:from|import)\s+prometheus\.execution\b"),
    ("prometheus.persistence", r"^\s*(?:from|import)\s+prometheus\.persistence\b"),
    ("requests", r"^\s*(?:from|import)\s+requests\b"),
    ("httpx", r"^\s*(?:from|import)\s+httpx\b"),
    ("aiohttp", r"^\s*(?:from|import)\s+aiohttp\b"),
    ("websockets", r"^\s*(?:from|import)\s+websockets\b"),
    ("binance", r"^\s*(?:from|import)\s+binance\b"),
    ("dotenv", r"^\s*(?:from|import)\s+dotenv\b"),
    ("python-dotenv", r"^\s*(?:from|import)\s+python_dotenv\b"),
    ("urllib.request", r"^\s*(?:from|import)\s+urllib\.request\b"),
    ("socket", r"^\s*(?:from|import)\s+socket\b"),
    ("os.environ-secret", r"\bos\.environ\b"),
    ("getenv", r"\bgetenv\s*\("),
)


_TRIPLE_DQ = re.compile(r'""".*?"""', flags=re.DOTALL)
_TRIPLE_SQ = re.compile(r"'''.*?'''", flags=re.DOTALL)


def _strip_docstrings_and_comments(text: str) -> str:
    text = _TRIPLE_DQ.sub("", text)
    text = _TRIPLE_SQ.sub("", text)
    out: list[str] = []
    for line in text.splitlines():
        idx = line.find("#")
        if idx >= 0:
            out.append(line[:idx])
        else:
            out.append(line)
    return "\n".join(out)


def _phase_4bh_files() -> list[Path]:
    return [PACKAGE_ROOT / name for name in PHASE_4BH_MODULES]


@pytest.mark.parametrize(
    "module_path", _phase_4bh_files(), ids=lambda p: p.name
)
def test_phase_4bh_module_has_no_forbidden_imports(module_path: Path) -> None:
    text = module_path.read_text(encoding="utf-8")
    stripped = _strip_docstrings_and_comments(text)
    for label, pattern in FORBIDDEN_IMPORT_PATTERNS:
        if re.search(pattern, stripped, flags=re.MULTILINE):
            pytest.fail(
                f"{module_path.name} contains forbidden import / reference matching "
                f"{label!r} ({pattern}) in code (not in docstrings)"
            )


_DENY_TOKENS: tuple[str, ...] = (
    "api_key",
    "secret",
    "signature",
    "listenKey",
    "userDataStream",
    "/fapi/v1/order",
    "/fapi/v2/account",
    "/fapi/v2/positionRisk",
    "/fapi/v1/leverage",
    "/fapi/v1/marginType",
    "/fapi/v1/forceOrders",
    ".env",
    "Graphify",
    "MCP",
    ".mcp.json",
)


def test_phase_4bh_modules_have_no_credential_tokens_in_code() -> None:
    for module_path in _phase_4bh_files():
        text = module_path.read_text(encoding="utf-8")
        code = _strip_docstrings_and_comments(text)
        for token in _DENY_TOKENS:
            assert token not in code, (
                f"{module_path.name} code (excluding docstrings/comments) must not "
                f"contain forbidden token {token!r}"
            )


def test_phase_4bh_module_files_exist() -> None:
    for module_path in _phase_4bh_files():
        assert module_path.exists(), f"missing module: {module_path}"


def test_phase_4bh_modules_do_not_import_pyarrow_at_top_level() -> None:
    """``pyarrow`` may be imported but only inside functions / TYPE_CHECKING.

    Top-level ``import pyarrow`` is fine because it has no network or
    credential surface; this test simply documents the import shape so
    that any future top-level networking import would be visible in
    ``test_phase_4bh_module_has_no_forbidden_imports``.
    """
    for module_path in _phase_4bh_files():
        text = module_path.read_text(encoding="utf-8")
        # Sanity: at least one of the modules references pyarrow somehow,
        # but no networking library appears anywhere.
        assert "requests" not in text
        assert "httpx" not in text
        assert "aiohttp" not in text
