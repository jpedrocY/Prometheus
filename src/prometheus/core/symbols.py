"""Canonical symbol identifiers for Prometheus v1."""

from __future__ import annotations

from enum import StrEnum


class Symbol(StrEnum):
    """Supported symbols for Prometheus v1.

    BTCUSDT is the only live-capable symbol. ETHUSDT is research/comparison
    only. New symbols require phase-gate approval per
    docs/12-roadmap/phase-gates.md.
    """

    BTCUSDT = "BTCUSDT"
    ETHUSDT = "ETHUSDT"
