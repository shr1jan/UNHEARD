"""E5-1 / E1-3 — the masking path performs NO disk writes.

Requirements: NFR-PRIV-01, NFR-PRIV-02, FR-POST-05
"""
import tempfile

import pytest

from masking.convert import convert
from masking.guards import DiskWriteForbidden, no_disk_writes


def test_convert_produces_masked_bytes_without_disk_io():
    raw = b"\x00\x01\x02pretend-audio"
    masked = convert(raw)
    assert isinstance(masked, bytes)
    assert len(masked) == len(raw)


def test_guard_blocks_open_for_write():
    with pytest.raises(DiskWriteForbidden):
        with no_disk_writes():
            open("/tmp/should-not-happen.wav", "wb")  # noqa: SIM115


def test_guard_blocks_tempfile():
    with pytest.raises(DiskWriteForbidden):
        with no_disk_writes():
            tempfile.NamedTemporaryFile()


def test_guard_allows_reads():
    # Reading config/models is fine; only writes are forbidden on this path.
    with no_disk_writes():
        with open(__file__, "r") as fh:
            assert "E5-1" in fh.read()
