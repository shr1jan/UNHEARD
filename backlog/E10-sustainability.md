# Epic E10 — Sustainability, Ads & Nonprofit Structure

**Phase:** 4 · **Goal:** keep the lights on without betraying the mission.
**Exit:** no tracking SDKs (audit); zero ads in vulnerable surfaces (test); hotline funded separately; legal entity established.

> Ads work is **blocked until the "zero ads in vulnerable surfaces" guard exists** (E10-3).

---

### [ ] E10-1 — Visual-only, contextual (non-tracking) ads `client` `backend` `privacy-critical` 🛡️
**Requirements:** `FR-SUS-01`, `FR-SUS-02`, `NFR-PRIV-08`
**Acceptance:** ads are visual only (never audio); targeted by topic being browsed (contextual), never behavioral; **no third-party tracking SDKs** (verified by dependency audit).

### [ ] E10-2 — Advertiser vetting + calm styling `backend` `client`
**Requirements:** `FR-SUS-03`
**Acceptance:** vetted advertisers only (no gambling, predatory loans, alcohol near recovery content, sketchy cures); calm/discreet, muted, bottom-anchored styling.

### [ ] E10-3 — Zero-ads guard for vulnerable surfaces `backend` `client` `safety-critical` 🔒
**Requirements:** `FR-SUS-04`
**Acceptance:** automated test asserts no ad renders in: the hotline, "talk to a human," crisis-detection moments, resource cards, and the moment right after posting a heavy note.
**Blocks:** E10-1, E10-2.

### [ ] E10-4 — Separate hotline funding (donations / Supporter) `backend` `client`
**Requirements:** `FR-SUS-05`
**Acceptance:** donations + optional "Supporter" contribution flow exists so the hotline never depends on ad pressure.

### [ ] E10-5 — Radical money transparency `backend`
**Requirements:** `FR-SUS-06`
**Acceptance:** a published, plain-language monthly statement of run cost vs. income vs. gap.

### [ ] E10-6 — Establish nonprofit / steward-ownership structure `legal`
**Requirements:** `FR-SUS-07`, `LEGAL-05`
**Acceptance:** legal entity established (nonprofit and/or steward-ownership/charter) that enforces "survive, don't profit" and prevents acquisition-and-repurposing.
