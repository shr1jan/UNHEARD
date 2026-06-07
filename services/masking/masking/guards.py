"""Runtime guard proving the masking path performs NO disk writes.

The privacy promise ("we never store your real voice") is only as strong as the
code path that handles raw audio. This guard makes a violation *fail loudly*:
within `no_disk_writes()`, any attempt to open a file for writing — or to use
tempfile — raises. (E5-1 / NFR-PRIV-02)

Usage:
    with no_disk_writes():
        masked = convert(raw_audio_bytes)   # raw_audio_bytes lives only here
"""
from __future__ import annotations

import builtins
import tempfile
from contextlib import contextmanager

_WRITE_MODES = ("w", "a", "x", "+")


class DiskWriteForbidden(RuntimeError):
    """Raised when code under no_disk_writes() attempts to persist to disk."""


@contextmanager
def no_disk_writes():
    real_open = builtins.open
    real_mkstemp = tempfile.mkstemp
    real_namedtemp = tempfile.NamedTemporaryFile

    def guarded_open(file, mode="r", *args, **kwargs):
        if any(m in mode for m in _WRITE_MODES):
            raise DiskWriteForbidden(
                f"disk write attempted on masking path: open({file!r}, {mode!r}) "
                f"— raw audio must stay in-memory (NFR-PRIV-01)"
            )
        return real_open(file, mode, *args, **kwargs)

    def guarded_tmp(*args, **kwargs):
        raise DiskWriteForbidden(
            "tempfile use attempted on masking path — raw audio must stay in-memory (NFR-PRIV-01)"
        )

    builtins.open = guarded_open  # type: ignore[assignment]
    tempfile.mkstemp = guarded_tmp  # type: ignore[assignment]
    tempfile.NamedTemporaryFile = guarded_tmp  # type: ignore[assignment]
    try:
        yield
    finally:
        builtins.open = real_open  # type: ignore[assignment]
        tempfile.mkstemp = real_mkstemp  # type: ignore[assignment]
        tempfile.NamedTemporaryFile = real_namedtemp  # type: ignore[assignment]
