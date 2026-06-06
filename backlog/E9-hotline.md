# Epic E9 — Human Crisis Hotline

**Phase:** 3 · **Goal:** real humans inside the app, anonymity preserved on every channel, 24/7, no dead ends.
**Exit:** every channel masks live voice; fallback proven under drills; break glass user-only; legal sign-off complete.

> 🔒 **Entire epic blocked by E0-1 (legal counsel sign-off, `LEGAL-01`).** This is safety-critical infrastructure, not a feature. Lives are on the line.

---

### [ ] E9-1 — Real-time DSP masking gateway (live audio) `ml` `backend` `safety-critical` 🔒
**Requirements:** `MASK-05`, `FR-HOT-04`, `NFR-PERF-02`, `ARCH-04`
**Acceptance:** DSP pitch+formant masking on live audio; added mouth-to-ear latency < ~150ms; words clear, emotion preserved; responder never hears the real voice.

### [ ] E9-2 — PSTN channel via relay (caller ID not logged) `backend` `privacy-critical` `safety-critical` 🛡️🔒
**Requirements:** `FR-HOT-03`, `SEC-08`, `NFR-PRIV-03`
**Acceptance:** inbound routed through a relay/proxy number; caller number never logged; audio passed through the real-time masking gateway before reaching the responder.
**Note:** open question §12.5 — telephony provider selection.

### [ ] E9-3 — In-app VoIP/VoWiFi channel (E2E, no number exposed) `client` `backend` `safety-critical` 🔒
**Requirements:** `FR-HOT-03`, `SEC-03`, `FR-HOT-04`
**Acceptance:** app-controlled audio pipeline; masking + encryption end-to-end; no phone number exposed.

### [ ] E9-4 — End-to-end encrypted text channel `client` `backend` `safety-critical` 🔒
**Requirements:** `FR-HOT-03`, `SEC-03`
**Acceptance:** E2E-encrypted messaging to the responder; reachable by people who can't speak out loud.

### [ ] E9-5 — Orchestration: routing, queueing, national-line fallback `backend` `safety-critical` 🔒
**Requirements:** `CRIS-FALLBACK`, `FR-HOT-06`, `NFR-PERF-05`
**Acceptance:**
- Routes to available humans; queues; **automatically hands off to a staffed national line** whenever no responder is free or the line is closed.
- 24/7 coverage anchored by partner orgs; drills under "no responder" and "line closed" prove no dead ends.

### [ ] E9-6 — Break glass (user-triggered only) `client` `backend` `legal` `safety-critical` 🔒
**Requirements:** `FR-HOT-05`
**Acceptance:** only the user can trigger revealing location/contact in imminent danger; responder and platform can never reveal it for them; counsel-approved per jurisdiction.
**Blocked by:** E0-1.

### [ ] E9-7 — Minimal encrypted retention + user disclosure `backend` `legal` `privacy-critical` 🛡️
**Requirements:** `FR-HOT-08`, `SEC-03`
**Acceptance:** hotline conversation content retained only as safety law requires, encrypted, with explicit user disclosure of what (if anything) is kept.
