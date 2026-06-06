# Epic E4 — MVP: Reactions, Echo, Originals & Save

**Phase:** 1 · **Goal:** empathy-first engagement and a safe, warned path for keeping originals.
**Exit:** public reaction counts with no clout mechanics; default-destroy originals; warned opt-in save-to-Files.

---

### [ ] E4-1 — Empathy-first reactions with public counts `backend` `client` `core`
**Requirements:** `FR-FEED-06`, `FR-FEED-07`, `API-04`, `DATA-*` (`reactions`), `DATA-02`
**Acceptance:**
- Reaction types: `Heard you` / `Felt this` / `Sending strength` only.
- `POST /v1/posts/:id/reactions` add/remove; one row per (account,post,type).
- Counts public; **no** karma/reputation/leaderboards/cross-post scores.
- Counts maintained as denormalized counters for feed performance.

### [ ] E4-2 — Echo (in-app reshare) `backend` `client`
**Requirements:** `FR-FEED-10`, `API-10`, `DATA-*` (`echoes`)
**Acceptance:** `POST /v1/echoes` reshares a masked voicenote **within the app only**; spreads the post, never a profile.

### [ ] E4-3 — Default-destroy originals (verified) `backend` `privacy-critical` `core` 🛡️
**Requirements:** `FR-POST-05`, `MASK-06`, `NFR-PRIV-01`
**Acceptance:** by default the original is destroyed the instant the mask exists; the masked clip is the only audio artifact kept. (Covered jointly with E1-3's "no original after post" test.)

### [ ] E4-4 — Opt-in save-original-to-Files with safety warning `client`
**Requirements:** `FR-POST-06`, `FR-POST-07`
**Acceptance:**
- User may opt in to save the original to the device Files app (OS filesystem, outside app sandbox). Platform never retains it.
- First save shows the safety warning (a raw emotional recording can be found by a partner/parent/anyone with phone access) and suggests a neutral default filename.

### [ ] E4-5 — (Could) Identifying-details gentle warning `client` `ml`
**Requirements:** `FR-POST-10`
**Acceptance:** the app gently warns when a poster says obviously identifying details (names/places/employers), clearly framed as guidance, not a guarantee.
**Note:** open question §12.9 — on-device vs server (server reintroduces a transcript-touch concern). Decide before building.
