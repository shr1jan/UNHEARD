# Epic E2 — MVP: Accounts, Auth & Covenant

**Phase:** 1 · **Goal:** identity-less accounts with a hidden internal ID, gated behind Covenant acceptance.
**Exit:** account creation needs no PII; internal IDs never leave the server; Covenant acceptance recorded; no profile/history endpoints exist.

---

### [ ] E2-1 — Anonymous account creation (no PII) `backend` `privacy-critical` `core` 🛡️
**Requirements:** `FR-ACCT-01`, `SEC-01`
**Acceptance:** an account can be created and used to post/listen with no name/email/phone; credential bound only to a hidden internal ID.
**Blocked by:** E0-6.

### [ ] E2-2 — Hidden stable internal ID (never exposed) `backend` `privacy-critical` 🛡️
**Requirements:** `FR-ACCT-02`, `NFR-PRIV-04`
**Acceptance:**
- Each account has a stable internal ID used only for rate-limit/shadow-mute/ban.
- Contract test: the internal ID never appears in any API response, log, or export.

### [ ] E2-3 — Enforce no public profile / no cross-post history `backend` `privacy-critical` `core` 🛡️
**Requirements:** `FR-ACCT-03`, `NFR-PRIV-05`
**Acceptance:** there is **no** endpoint returning a public profile, follower graph, or another account's post history. Enforced at the API layer; covered by a negative contract test.

### [ ] E2-4 — Covenant acceptance gate `client` `backend` `legal`
**Requirements:** `FR-ACCT-07`, `LEGAL-COV-01`
**Acceptance:**
- Before a user can listen or post, the Covenant is shown and explicitly accepted.
- Acceptance recorded against internal ID with timestamp + version; no other identifying data.

### [ ] E2-5 — Minimum-age enforcement at signup `client` `backend` `legal`
**Requirements:** `LEGAL-02`, `FR-ACCT-05`
**Acceptance:** signup enforces the region-appropriate minimum age / consent rules from E0-2.
**Blocked by:** E0-2.

### [ ] E2-6 — Account deletion (hard delete) `backend` `privacy-critical` 🛡️
**Requirements:** `FR-ACCT-06`, `NFR-PRIV-06`, `DATA-03`
**Acceptance:** deleting an account hard-deletes all its posts/comments/reactions/echoes + masked audio objects + the account record. Verified by test.
