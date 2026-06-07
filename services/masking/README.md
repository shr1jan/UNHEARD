# unheard-masking

Python + GPU voice-masking service. **Neural voice conversion** for posts and
audio comments: keeps pitch contour, timing, pauses, breaths; swaps only timbre;
maps everyone into a small shared set of neutral voices. (Architecture §8, epic **E1**.)

## The one rule

Raw audio is held **in memory only**, for the duration of conversion, then
destroyed. It is **never** written to disk, logs, or storage. This is enforced,
not trusted:

- [`masking/guards.py`](masking/guards.py) — `no_disk_writes()` makes any file
  write or tempfile use on the masking path raise `DiskWriteForbidden`.
- [`tests/test_no_disk_writes.py`](tests/test_no_disk_writes.py) — the E5-1 gate.

## Status

Skeleton. `convert()` is an identity transform placeholder so the pipeline, API,
and privacy tests are exercisable before a model is chosen. The real neural VC
model is selected and benchmarked in **`E1-1`** (RVC / so-vits-svc family etc. —
quality, latency, GPU cost, **and license terms**).

## Develop

```bash
cd services/masking
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest                       # runs the no-disk-writes gate
uvicorn masking.app:app --reload --port 8081
```

## Next issues

`E1-1` model benchmark · `E1-2` neutral target voices · `E1-3` in-memory pipeline ·
`E1-4` GPU worker pool + queue · `E1-6` quality acceptance harness.
