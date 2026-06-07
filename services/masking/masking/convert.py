"""Conversion entry point (stub).

The real implementation (E1-1/E1-3) loads a neural VC model and converts
`raw_audio` -> masked audio buffer entirely in memory, then the caller discards
`raw_audio`. This stub keeps the *contract* and the in-memory guarantee so the
pipeline, API, and privacy tests can be built before the model is chosen.
"""
from __future__ import annotations

from .guards import no_disk_writes

# The small shared set of neutral target voices. (MASK-02)
NEUTRAL_VOICES = ("neutral-a", "neutral-b", "neutral-c")


def convert(raw_audio: bytes, target_voice: str = "neutral-a") -> bytes:
    """Return masked audio bytes. Raw audio never leaves memory.

    Replace the body with neural voice conversion in E1-1. The `no_disk_writes`
    guard MUST remain wrapped around any code that touches `raw_audio`.
    """
    if target_voice not in NEUTRAL_VOICES:
        raise ValueError(f"unknown target voice: {target_voice}")
    with no_disk_writes():
        # TODO(E1-1): real neural voice conversion here.
        # Placeholder: identity transform so the pipeline is exercisable.
        masked = bytes(raw_audio)
    return masked
