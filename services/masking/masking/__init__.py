"""Unheard masking service.

Neural voice conversion for posts/comments: keep pitch contour, timing, pauses,
breaths; swap only timbre; map into a small shared set of neutral voices.

INVIOLABLE: raw audio is held in-memory only, for the duration of conversion,
then destroyed. It is NEVER written to disk, logs, or storage. (NFR-PRIV-01,
FR-POST-05, MASK-01/02). Enforced by `guards.no_disk_writes` + tests.
"""
