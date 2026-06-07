# unheard-moderation

The three-way sort, not "filter toxicity":

| Verdict | Action |
|---|---|
| **Pain** (your own distress) | **Allow & protect** — never blocked (`FR-MOD-02`) |
| **Harm** (cruelty aimed at someone) | **Block** |
| **Crisis** (self-harm signals) | **Offer help**, never punish (`FR-HOT-07`) |

Architecture §7.4, epic **E7**.

## Status

Skeleton with a conservative heuristic stub so the safety invariant is testable
now. The real classifier (`E7-1`) is an LLM + fast pre-filter that judges nuance
and, for audio, tone of voice — with transcription **in-memory only** and the
transcript destroyed after reading (`FR-MOD-04`, `NFR-PRIV-01`).

The single most dangerous failure is blocking pain. That invariant is locked by
[`tests/test_pain_never_blocked.py`](tests/test_pain_never_blocked.py) and runs in CI.

## Develop

```bash
cd services/moderation
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Next issues

`E7-1` classifier + pre-filter · `E7-2` in-memory STT + tone weighting ·
`E7-3` labeled eval harness · `E7-8` zero-tolerance + mandatory reporting.
