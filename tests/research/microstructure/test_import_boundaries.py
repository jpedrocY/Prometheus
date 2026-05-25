"""Static import-boundary and content scanner for the microstructure scaffold.

Scans the source files of ``src/prometheus/research/microstructure/`` to
verify the scaffold (Phase 4aw) and the aggTrades collector skeleton
(Phase 4ax) remain inert: no imports from runtime/execution/
persistence; no Binance SDK imports; no signed-request helpers; no
network clients used in this phase; no `.env` reads; no MCP / Graphify
references; and no credential-shaped strings or private endpoint paths
appear in source code.

This test runs entirely against repository source files. It does not
invoke the modules under test, does not import them, and does not
perform any network or filesystem mutation.
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


def _scaffold_files() -> list[Path]:
    assert PACKAGE_ROOT.is_dir(), f"package root missing: {PACKAGE_ROOT}"
    return sorted(p for p in PACKAGE_ROOT.glob("*.py"))


# ----------------------------------------------------------------------
# Import-boundary scanner
# ----------------------------------------------------------------------

# Each regex matches a forbidden import. The regex is intentionally
# tolerant of relative-to-absolute conversion: it matches ``import X`` or
# ``from X import ...`` but not occurrences of the same string inside
# string literals or comments — those are checked separately by the
# content scanner below.
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


@pytest.mark.parametrize("module_path", _scaffold_files(), ids=lambda p: p.name)
def test_no_forbidden_imports(module_path: Path) -> None:
    text = module_path.read_text(encoding="utf-8")
    # Strip docstrings and comments before scanning imports.
    stripped = _strip_docstrings_and_comments(text)
    for label, pattern in FORBIDDEN_IMPORT_PATTERNS:
        if re.search(pattern, stripped, flags=re.MULTILINE):
            pytest.fail(
                f"{module_path.name} contains forbidden import / reference matching "
                f"{label!r} ({pattern}) in code (not in docstrings)"
            )


# ----------------------------------------------------------------------
# Content scanner: forbidden tokens / strings
# ----------------------------------------------------------------------

# These tokens must NOT appear in scaffold source code. They may appear
# in test code (e.g. denylist tests intentionally constructing denied
# strings), so this scan only inspects ``src/prometheus/research/
# microstructure/`` files.
#
# Two categories:
#   STRICT_DENY — must not appear anywhere in scaffold source.
#   ALLOWLIST_DENY — may appear ONLY inside the ``allowlist.py`` module,
#       which legitimately encodes denylist tokens used by the runtime
#       allowlist machinery.

# All denylist tokens may legitimately appear in ``allowlist.py`` code,
# which is the module that encodes the denylist itself. They must NOT
# appear in the code of any other scaffold module (docstrings and
# comments are excluded from the scan).
STRICT_DENY_TOKENS: tuple[str, ...] = ()

ALLOWLIST_DENY_TOKENS: tuple[str, ...] = (
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
    "Graphify",
    "MCP",
    ".mcp.json",
)

# ``.env`` is checked separately with a word boundary so it does not collide
# with legitimate identifiers like ``envelope_terminal_unix_ms`` (Phase
# 4bm-N v002 label schema field) accessed via ``self.envelope_terminal_unix_ms``
# inside dataclass methods. The boundary requires that ``.env`` is followed
# by a non-word character so ``.env``, ``.env.local``, ``.env "`` trip the
# check but ``.envelope_*`` attribute access does not.
_DOT_ENV_RE = re.compile(r"\.env(?![A-Za-z0-9_])")


def test_strict_deny_tokens_absent_from_all_scaffold_code() -> None:
    """STRICT_DENY tokens must not appear in scaffold code.

    Module docstrings and comments may reference the tokens for
    documentation purposes, but they must never appear in actual code.
    """
    for module_path in _scaffold_files():
        text = module_path.read_text(encoding="utf-8")
        code = _strip_docstrings_and_comments(text)
        for token in STRICT_DENY_TOKENS:
            assert token not in code, (
                f"{module_path.name} code (excluding docstrings/comments) must not "
                f"contain forbidden token {token!r}"
            )


def test_allowlist_deny_tokens_only_in_allowlist_code() -> None:
    """ALLOWLIST_DENY tokens may only appear in ``allowlist.py`` code.

    Module docstrings and comments may reference the tokens for
    documentation purposes, but only ``allowlist.py`` may encode them
    in source code.
    """
    for module_path in _scaffold_files():
        text = module_path.read_text(encoding="utf-8")
        code = _strip_docstrings_and_comments(text)
        if module_path.name == "allowlist.py":
            # allowlist.py legitimately encodes denylist tokens
            continue
        for token in ALLOWLIST_DENY_TOKENS:
            assert token not in code, (
                f"{module_path.name} code (excluding docstrings/comments) must not "
                f"contain denylist token {token!r}; only allowlist.py may encode such tokens"
            )
        assert not _DOT_ENV_RE.search(code), (
            f"{module_path.name} code (excluding docstrings/comments) must not "
            f"reference any '.env' file (word-boundary match)"
        )


# ----------------------------------------------------------------------
# Helper: strip docstrings and comments from Python source
# ----------------------------------------------------------------------

_TRIPLE_DQ = re.compile(r'""".*?"""', flags=re.DOTALL)
_TRIPLE_SQ = re.compile(r"'''.*?'''", flags=re.DOTALL)


def _strip_docstrings_and_comments(text: str) -> str:
    text = _TRIPLE_DQ.sub("", text)
    text = _TRIPLE_SQ.sub("", text)
    out: list[str] = []
    for line in text.splitlines():
        idx = line.find("#")
        if idx >= 0:
            # naive but adequate for scaffold scanning: comments out
            # everything after the first '#' on the line.
            out.append(line[:idx])
        else:
            out.append(line)
    return "\n".join(out)
