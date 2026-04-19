"""Shared exception hierarchy for Prometheus domain errors."""

from __future__ import annotations


class PrometheusError(Exception):
    """Base class for Prometheus domain errors."""


class DataIntegrityError(PrometheusError):
    """Raised when historical or derived data fails an integrity invariant.

    Examples: duplicate bars for the same (symbol, interval, open_time),
    missing bars in an expected range, non-monotonic timestamps, or
    unaligned open_times.
    """


class ManifestError(PrometheusError):
    """Raised when a dataset manifest is invalid or would be overwritten.

    Dataset manifests are immutable once written; attempts to clobber
    an existing manifest must fail closed rather than silently replace it.
    """
