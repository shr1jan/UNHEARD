# Epic E3 — MVP: Post, Feed & Topics

**Phase:** 1 · **Goal:** the frictionless post flow and a calm, anti-doomscroll feed.
**Exit:** post in minimal taps; feed with three sorts + topics; "my posts" private view; hard delete.

---

### [ ] E3-1 — Post flow: Open → Record → mask → Preview → Post `client` `core`
**Requirements:** `FR-POST-01`, `FR-POST-02`, `FR-POST-04`
**Acceptance:**
- Minimal-friction record→post flow, operable one-handed.
- Topic is optional and offered only as a final skippable step.
- Poster sets comment mode (`off`/`text`/`audio`/`both`) at post time (field stored; enforcement is E6).
**Blocked by:** E1-5.

### [ ] E3-2 — Post creation API & data model `backend` `core`
**Requirements:** `API-01`, `FR-POST-08`, `DATA-*` (`posts`)
**Acceptance:** `POST /v1/posts` (multipart audio) creates a post storing only masked-audio ref, optional topic, duration, comment_mode, timestamps, owner internal ID. No original/transcript/voiceprint fields exist.

### [ ] E3-3 — Feed with three sorts `backend` `client` `core`
**Requirements:** `FR-FEED-01`, `FR-FEED-02`, `FR-FEED-03`, `API-02`, `NFR-PERF-04`
**Acceptance:**
- `GET /v1/feed?sort=&topic=` paginated; default = everything.
- Sorts: **Newest**, **Most heard**, **Needs love** (surfaces low-listen posts).
- Each item shows play button, waveform, duration, optional topic, relative time, reaction counts.
- Feed read p95 < 300ms at MVP load.

### [ ] E3-4 — Topics: set, browse, follow `backend` `client`
**Requirements:** `FR-FEED-04`, `FR-FEED-05`, `FR-FEED-09`, `API-07`, `DATA-*` (`topic_follows`)
**Acceptance:**
- Initial topic set present (Work life, Family, Relationships, Friendships, Mental health, Loneliness, Grief, Identity, Money, Health, Just need to vent).
- Follow/unfollow topics shapes the feed; browse a single topic works.

### [ ] E3-5 — "My posts" private view (self only) `backend` `client` `privacy-critical` 🛡️
**Requirements:** `FR-ACCT-04`, `API-09`
**Acceptance:** `GET /v1/me/posts` returns only the caller's posts; no path lets anyone view another account's collection.

### [ ] E3-6 — Instant hard delete of own post `backend` `client` `privacy-critical` `core` 🛡️
**Requirements:** `FR-POST-09`, `API-03`, `DATA-03`, `NFR-PRIV-06`
**Acceptance:** `DELETE /v1/posts/:id` hard-deletes row + masked audio object + dependent reactions/comments/echoes. No soft-delete flag.

### [ ] E3-7 — Anti-doomscroll UX `client`
**Requirements:** `FR-FEED-08`, `NFR-UX-04`
**Acceptance:** reactions framed as support not scores; optional "that's enough for today" stopping point; calm/warm/non-gamified copy throughout.
