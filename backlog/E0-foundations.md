# Epic E0 — Foundations & Safety Design

**Phase:** 0 (gating) · **Goal:** make the dangerous parts safe before building the easy parts.
**Exit:** signed privacy spec; counsel engaged with written scope; ≥1 partner org in discussion; threat model reviewed; CI green skeleton.

---

### [ ] E0-1 — Engage legal counsel on crisis duty-of-care & multi-jurisdiction `legal` 🔒
Engage qualified counsel covering crisis duty-of-care, anonymity-vs-rescue, mandatory reporting, and multi-jurisdiction rules.
**Requirements:** `LEGAL-01`, `LEGAL-04`, `FR-HOT-05`
**Acceptance:**
- Counsel retained with a written scope covering launch regions.
- A memo identifying duty-of-care obligations and break-glass legal constraints per region.
**Blocked by:** none · **Blocks:** all of E9.

### [ ] E0-2 — Finalize minimum age & parental-consent rules `legal`
**Requirements:** `LEGAL-02`
**Acceptance:** documented minimum age + consent rules per launch region, ready to enforce at signup (E2-2).

### [ ] E0-3 — Select crisis partner org(s) & design fallback routing on paper `legal` `safety-critical` 🔒
**Requirements:** `CRIS-FALLBACK`, `FR-HOT-06`
**Acceptance:**
- ≥1 partner crisis org in active discussion (988/Lifeline, Samaritans, Crisis Text Line, or local equivalent).
- A documented fallback-routing design: what happens when no responder is free / line closed → staffed national line. No dead ends.

### [ ] E0-4 — Lock the privacy / data-handling spec as a binding contract `privacy-critical` 🛡️
**Requirements:** §5, §4.1 of the requirements doc (`NFR-PRIV-*`, `DATA-NEVER-01`)
**Acceptance:**
- The "never stored" list and the stored-fields list are signed off as binding.
- A privacy-review checklist exists that all schema changes must pass.

### [ ] E0-5 — Repo, CI, environments, secrets, threat model `infra`
**Requirements:** `SEC-06`, foundation for `NFR-PRIV-02`/`NFR-PRIV-04` CI gates
**Acceptance:**
- Monorepo (or polyrepo) skeleton with CI running on every PR.
- Secrets manager wired; no secrets in source/images.
- Dev/staging environments provisioned.
- A written threat model reviewed by the team (top threats: raw-audio leak, internal-ID leak, crisis dead-end, abuse under anonymity).

### [ ] E0-6 — Decide auth/DB/storage stack `infra` `risk`
Choose between Supabase (anon auth + Postgres + object storage + edge functions, fastest) vs Neon (serverless Postgres, MCP already connected) + S3-compatible storage.
**Requirements:** `ARCH-07`
**Acceptance:** a written decision with rationale; provider provisioned; spike proving anonymous auth + encrypted object storage works end-to-end.
**Note:** open question §12.4 — resolve before E2-1.
