# Epic E5 — MVP: Privacy & Security Hardening

**Phase:** 1 · **Goal:** make the founding privacy promises enforceable in CI, not just intentions.
**Exit:** all privacy invariants pass as automated gates; security review clean of criticals; masking path load-tested.

> This epic turns §4.1 / §4.2 of the requirements doc into running checks. Treat every item as a release blocker for the MVP.

---

### [ ] E5-1 — CI gate: no temp-file writes on masking/STT paths `infra` `privacy-critical` 🛡️
**Requirements:** `NFR-PRIV-02`
**Acceptance:** a runtime guard + test detects any temp-file write in the masking (and later STT) code paths; CI fails if triggered.

### [ ] E5-2 — CI gate: internal IDs never serialized `infra` `backend` `privacy-critical` 🛡️
**Requirements:** `NFR-PRIV-04`, `FR-ACCT-02`
**Acceptance:** contract tests over all endpoints assert no internal ID appears in any response body/header.

### [ ] E5-3 — CI gate: no profile/history endpoints `infra` `backend` `privacy-critical` 🛡️
**Requirements:** `NFR-PRIV-05`, `FR-ACCT-03`
**Acceptance:** negative tests assert no route returns a public profile or another account's history.

### [ ] E5-4 — Log scrubbing (no raw audio/transcripts/PII) `backend` `privacy-critical` 🛡️
**Requirements:** `NFR-PRIV-03`
**Acceptance:** request bodies scrubbed before logging; tests assert raw audio, transcripts, and (later) phone numbers never reach logs.

### [ ] E5-5 — Encryption in transit & at rest `infra` `backend`
**Requirements:** `SEC-01`, `SEC-02`, `DATA-OBJ-01`
**Acceptance:** TLS 1.2+ everywhere; masked audio encrypted at rest; DB encrypted at rest.

### [ ] E5-6 — Signed, short-lived, non-enumerable audio URLs `backend`
**Requirements:** `SEC-04`
**Acceptance:** masked audio served only via per-request signed short-lived URLs; objects not publicly enumerable.

### [ ] E5-7 — Baseline abuse controls (rate limits) `backend`
**Requirements:** `SEC-05`, `NFR-PRIV-07`
**Acceptance:** sliding-window rate limits on all write endpoints from day one of public exposure (full shadow-mute/ban lands in E7).

### [ ] E5-8 — Privacy-review checklist for schema migrations `infra` `privacy-critical` 🛡️
**Requirements:** `DATA-01`, `NFR-PRIV-07`
**Acceptance:** every migration adding a user-derived column requires documented privacy sign-off; checklist enforced in PR template.

### [ ] E5-9 — Security review + masking-path load test `infra` `risk`
**Requirements:** `SEC-07`, `NFR-PERF-01`, `NFR-PERF-06`
**Acceptance:** pre-release security review with no open criticals; masking GPU pool load-tested for throughput, queue depth, back-pressure.
