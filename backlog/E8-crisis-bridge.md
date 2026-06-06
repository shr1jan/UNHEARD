# Epic E8 — Crisis Detection + Interim Safety Bridge

**Phase:** 2 · **Goal:** detect crisis signals and gently offer help — and, until the full hotline (E9) exists, route to vetted external national lines so detection never points at a dead end.
**Exit:** crisis signal always reaches a staffed external line + resource cards; offer is gentle, never forced or punitive.

> 🔒 **Non-negotiable:** crisis detection ships **with** this interim bridge, never alone. A detected crisis must never reach silence (`CRIS-FALLBACK`).

---

### [ ] E8-1 — Gentle in-app crisis offer `client` `safety-critical` 🔒
**Requirements:** `FR-HOT-02`, `FR-HOT-07`, `FR-MOD-01` (crisis branch)
**Acceptance:**
- On a crisis signal from E7-1, the app gently offers help ("Would it help to talk to a real person right now? Someone's here.").
- Never forced, never punitive; the author quietly receives support + resources, never flagged as a violation.
**Blocked by:** E7-1.

### [ ] E8-2 — Interim routing to vetted national lines + resource cards `client` `backend` `safety-critical` 🔒
**Requirements:** `CRIS-FALLBACK` (interim), `FR-HOT-09`
**Acceptance:**
- Tapping the offer (or "Talk to a human") routes to vetted, region-appropriate national crisis lines and resource cards.
- No dead end: every path resolves to a staffed external resource until E9 ships.
**Blocked by:** E0-3.

### [ ] E8-3 — Persistent "Talk to a human" entry point `client`
**Requirements:** `FR-HOT-01`
**Acceptance:** a calm, always-reachable, never-buried "Talk to a human" presence — warm, not alarming — present even when not in crisis.
