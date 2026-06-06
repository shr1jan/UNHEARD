# Epic E1 — MVP: Masking Service (the core, highest risk)

**Phase:** 1 · **Goal:** record → server-side neural mask → preview, with the original provably destroyed.
**Exit:** masking passes intelligibility + anonymity + emotion acceptance with human raters; no disk writes on the raw-audio path; preview gate unbypassable.

> This is the make-or-break epic. Front-load the model benchmark (E1-1) — it drives MVP viability and the Phase 3 real-time latency budget.

---

### [ ] E1-1 — Benchmark & select a neural voice-conversion model `ml` `risk` `core`
Evaluate the RVC / so-vits-svc family and similar audio-to-audio VC models for quality, latency, GPU cost, and **license terms** for nonprofit use.
**Requirements:** `MASK-01`, `MASK-04`, `RISK-MASK`, `RISK-LIC`
**Acceptance:**
- ≥2 candidate models benchmarked on a held-out clip set.
- A written decision: chosen model, latency profile, $/clip GPU cost, license confirmed for this use.
**Blocked by:** E0-6.

### [ ] E1-2 — Map all users into a small shared set of neutral target voices `ml` `privacy-critical` 🛡️
**Requirements:** `MASK-02`
**Acceptance:** a fixed small set of neutral target voices defined; every conversion maps to one of them (no per-user unique voice); rationale documented (max anonymity + sonic identity).

### [ ] E1-3 — In-memory masking pipeline (no disk writes) `backend` `ml` `privacy-critical` 🛡️
Gateway streams uploaded bytes → masking service converts in-memory → masked buffer → object store; raw buffer discarded immediately.
**Requirements:** `ARCH-PIPE-01`, `ARCH-02`, `ARCH-03`, `ARCH-06`, `NFR-PRIV-01`, `FR-POST-05`
**Acceptance:**
- Canonical 6-step pipeline implemented.
- Integration test proves: after a post, **no original audio exists** anywhere (memory, disk, store, logs).
- A crashed/failed job leaves **zero** persisted raw audio.

### [ ] E1-4 — GPU worker pool behind a queue (scalable, back-pressured) `infra` `ml`
**Requirements:** `ARCH-01`, `NFR-PERF-06`, `NFR-PERF-01`
**Acceptance:** masking runs as a separate service consuming a Redis job queue; horizontally scalable; back-pressures safely under load; p-latency target (~<10s typical clip) met in load test.

### [ ] E1-5 — Preview gate (mask confirmed before publish) `client` `backend` `privacy-critical` `core` 🛡️
**Requirements:** `FR-POST-03`, `ARCH-PIPE-01` step 6
**Acceptance:**
- The masked clip is played back to the poster; explicit "yes, that's not me" confirmation required.
- Nothing becomes public without passing this gate (server enforces, not just UI).

### [ ] E1-6 — Masking quality acceptance harness (raters) `ml`
**Requirements:** `MASK-03`, `MASK-08`, §11
**Acceptance:** a repeatable human-rater protocol scoring (a) intelligibility — words clear, (b) anonymity — raters can't match masked→speaker above chance, (c) emotion preserved — pauses/breaks/tone intact. Release thresholds defined and met.
