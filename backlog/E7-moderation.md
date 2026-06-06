# Epic E7 — Moderation AI & Abuse Controls

**Phase:** 2 · **Goal:** the three-way sort (Pain protect / Harm block / Crisis help), pre-check before harm lands, abuse controls without exposing identity.
**Exit:** pain is never blocked (red-team set passes); abuse pre-checked before the poster sees it; rate-limit→shadow-mute→ban works on internal ID.

> 🔒 The #1 job is distinguishing **self-directed pain (protect)** from **other-directed harm (remove)**. A defect that blocks pain is **critical** and a release blocker.

---

### [ ] E7-1 — Pain/harm/crisis classifier + fast pre-filter `ml` `safety-critical` `core` 🔒
**Requirements:** `FR-MOD-01`, `FR-MOD-02`, `FR-MOD-03`, `ARCH-PIPE-02`, `NFR-PERF-03`
**Acceptance:**
- Classifier sorts content into Pain (allow & protect) / Harm (block) / Crisis (offer help, never violation).
- "I want to die" / "I feel worthless" classify as **crisis/pain, never violation**.
- Fast pre-filter keeps text pre-check targeting sub-second.

### [ ] E7-2 — In-memory STT + tone weighting for audio comments `ml` `privacy-critical` 🛡️
**Requirements:** `FR-MOD-04`, `NFR-PRIV-01`
**Acceptance:**
- Audio comment transcribed **in-memory only**; tone of voice weighed (delivery, not just words).
- Raw audio + transcript destroyed after the AI reads them; only a passing mask survives.
**Note:** open question §12.3 — self-hosted Whisper vs API.

### [ ] E7-3 — Moderation eval harness (labeled corpus) `ml`
**Requirements:** §11, `RISK-MOD`
**Acceptance:** labeled corpus across all three classes incl. deliberate hard cases (self-harm vs harassment, "good luck with that" sneer vs sincere); track precision/recall per class; **pain-blocked = critical**; human review of edges; audio tone cases included.

### [ ] E7-4 — Blocked-content handling (silent drop / soft nudge) `backend` `client`
**Requirements:** `FR-MOD-06`
**Acceptance:** clear abuse silently dropped (don't coach trolls); borderline gets a soft "this might hurt someone — rephrase?" nudge.

### [ ] E7-5 — Abuse escalation: rate-limit → shadow-mute → ban `backend` `privacy-critical` 🛡️
**Requirements:** `FR-MOD-05`, `SEC-05`, `FR-ACCT-05`
**Acceptance:** escalation keyed on the hidden internal ID; identity never exposed; ban prevents posting/commenting; basic ban-evasion mitigation that stores no PII.

### [ ] E7-6 — User reporting (reporter unlinked from reported) `backend` `client` `privacy-critical` 🛡️
**Requirements:** `FR-MOD-08`, `API-08`, `DATA-*` (`reports`), `DATA-04`
**Acceptance:** `POST /v1/reports` flags a post/comment; reports anonymous to the reported party; schema structurally cannot join reporter→reported in any user-facing path.

### [ ] E7-7 — False-positive recovery path `client` `backend`
**Requirements:** `FR-MOD-07`
**Acceptance:** a light "this was hidden — doesn't feel right? tap to ask a human" path; no heavy appeals bureaucracy.

### [ ] E7-8 — Zero-tolerance detection + mandatory reporting `ml` `backend` `legal` `safety-critical` 🔒
**Requirements:** `FR-MOD-09`, `LEGAL-04`
**Acceptance:** CSAM and equivalent categories detected, removed, and reported to authorities per jurisdiction.
**Blocked by:** E0-1.
