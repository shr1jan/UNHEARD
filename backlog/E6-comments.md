# Epic E6 — Comments & Poster Controls

**Phase:** 2 · **Goal:** safe two-way interaction, fully poster-controlled, flat by design.
**Exit:** comment modes enforced server-side; audio comments masked + originals destroyed; flat threading; reactions always available.

---

### [ ] E6-1 — Comment data model (flat, no parent_id) `backend`
**Requirements:** `FR-CMT-03`, `DATA-*` (`comments`), `API-06`
**Acceptance:** `comments` table has `kind ∈ {text,audio}`, nullable `body_text`/`masked_audio_key`, and **no `parent_id`**; `GET /v1/posts/:id/comments` returns a flat list.

### [ ] E6-2 — Enforce poster comment_mode `backend` `core`
**Requirements:** `FR-CMT-01`, `API-05`
**Acceptance:** `POST /v1/posts/:id/comments` rejects comments not allowed by the post's `comment_mode` (off/text/audio/both); enforced server-side.

### [ ] E6-3 — Masked audio comments through the same pipeline `backend` `ml` `privacy-critical` 🛡️
**Requirements:** `FR-CMT-02`, `ARCH-PIPE-01`
**Acceptance:** audio comments run the same masking pipeline; commenter unrecognizable; their original destroyed (verified by the same no-original test as posts).

### [ ] E6-4 — Reactions available regardless of comment setting `backend` `client`
**Requirements:** `FR-CMT-04`
**Acceptance:** reactions work even when comments are off.

### [ ] E6-5 — Comments pass moderation pre-check before reaching poster `backend` `safety-critical`
**Requirements:** `FR-CMT-05`, `FR-MOD-03`
**Acceptance:** every comment is moderated (E7) before it becomes visible to the poster.
**Blocked by:** E7-1.
