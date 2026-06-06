# Unheard — Development Requirements & Roadmap

**Status:** Draft v1.0 — engineering planning artifact
**Audience:** Engineering, product, design, security/privacy, clinical-safety, and legal leads
**Source documents:** Concept & Technical Document; Engineering Build Plan (Phase 1 MVP); One-Page Brief; Terms & Community Guidelines
**Last updated:** 2026-06-07

> This document turns the Unheard concept into a buildable, traceable specification. It defines **what** must be built (functional + non-functional requirements with stable IDs), **how** it should be architected, and **in what order** it should ship (a phased roadmap with milestones, exit criteria, dependencies, and risks).
>
> Two principles override every decision below and are treated as acceptance gates, not aspirations:
> 1. **Identity-less by design** — no real voice stored, no profiles, no aggregatable history.
> 2. **Survive, don't profit** — funding and structure are a ceiling, not a growth target.
>
> Anything that conflicts with these is a defect, regardless of how well it works.

---

## 0. How to read this document

- Requirements carry **stable IDs** (`FR-*`, `NFR-*`, `SEC-*`, `DATA-*`, `API-*`, `CRIS-*`, `LEGAL-*`). IDs never change once assigned; deprecated requirements are struck through, not deleted, to preserve traceability.
- **Priority** uses MoSCoW: **M** (Must), **S** (Should), **C** (Could), **W** (Won't, this release).
- **Phase** maps each requirement to the roadmap section (§10).
- "**Privacy-critical**" and "**Safety-critical**" tags mark requirements where a defect can cause de-anonymization or harm to a person in crisis. These get elevated review, extra tests, and cannot be waived to hit a date.

---

## 1. Product summary (engineering framing)

Unheard is an anonymous, voice-only social feed plus a human crisis hotline.

- A user records a voicenote → it is **masked server-side** (identity/timbre removed, words + emotion preserved) → the user **previews** the mask → it is **posted** to a feed.
- The **original recording is destroyed** the instant the mask exists. The masked clip is the only audio artifact the platform keeps.
- There are **no profiles, no followers, no visible posting history**. The unit of the network is the *voicenote*, not the *person*.
- Users react ("Heard you / Felt this / Sending strength"), comment (text or masked audio, poster-controlled), and follow **topics** (never people).
- A **human is always reachable** via three channels (PSTN relay, in-app VoIP, encrypted text), with the user's voice masked even to the responder, 24/7, with no dead ends.
- **Moderation** performs a three-way sort: **Pain** (protect), **Harm** (block), **Crisis** (offer help, never punish).
- The **Covenant** — never identify, never carry outside, never speak badly of what you heard — is accepted before listening or posting, and is the gravest violation if broken.

---

## 2. Scope & phase boundaries

| Capability | Phase | In MVP (P1)? |
|---|---|---|
| Anonymous account creation | 0–1 | ✅ |
| Record → server masking → preview → post | 1 | ✅ |
| Feed (Newest / Most heard / Needs love), topics, topic-follow | 1 | ✅ |
| Reactions (public counts) | 1 | ✅ |
| "My posts" private view + instant hard delete | 1 | ✅ |
| Optional save-original-to-Files (with warning) | 1 | ✅ |
| Comments (text + masked audio) + poster comment controls | 2 | ⛔ (P2) |
| AI moderation (pain/harm/crisis), reporting, rate-limit/ban | 2 | ⛔ (P2) |
| Human crisis hotline (PSTN / VoIP / E2E text) | 3 | ⛔ (P3) |
| Real-time DSP masking gateway (live calls) | 3 | ⛔ (P3) |
| Crisis detection → gentle in-app offer + national-line fallback | 2–3 | ⛔ |
| Ads (contextual, non-tracking), donations/Supporter, money transparency | 4 | ⛔ (P4) |
| Nonprofit / steward-ownership structure | 4 | ⛔ (P4) |
| Own peer + clinical responder tiers; stronger real-time neural masking | 5 | ⛔ (P5) |
| On-device masking | — | ❌ Explicitly never |
| Ephemeral posts, "whisper rooms", reply-to-reply threading | — | ❌ Rejected decisions |

> **Note on safety sequencing.** Crisis detection (a moderation-AI function) is specified in Phase 2 so the *signal* exists, but the *human response infrastructure* is Phase 3. Until Phase 3 ships, any crisis detection MUST route to vetted external national lines and resource cards (`CRIS-FALLBACK`), never to a dead end. See §6 and §10.

---

## 3. Functional requirements

### 3.1 Accounts & identity (`FR-ACCT-*`)

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| FR-ACCT-01 | M | 1 | The system MUST allow account creation with **no personal identity** (no name, email, or phone required to post/listen). Anonymous auth issues a credential bound only to a hidden internal ID. |
| FR-ACCT-02 | M | 1 | Each account MUST have a **hidden, stable internal ID** used solely for rate-limiting, shadow-mute, and bans. **Privacy-critical:** this ID MUST NEVER appear in any user-facing response, log, or export. |
| FR-ACCT-03 | M | 1 | The system MUST NOT create or expose any **public profile**, follower graph, or cross-post history for any account. |
| FR-ACCT-04 | M | 1 | A user MUST be able to view **only their own** posts in a private "My posts" view; this view is visible to no one else, including staff UIs except where ban enforcement strictly requires (audited). |
| FR-ACCT-05 | M | 2 | Banned accounts MUST be prevented from posting/commenting; **ban evasion** (new account to bypass a ban) is a violation and SHOULD be mitigated with device/abuse signals that do not store PII. |
| FR-ACCT-06 | S | 1 | The system MUST support account deletion that hard-deletes all of the account's posts/comments and the account record. |
| FR-ACCT-07 | M | 1 | Before a user can **listen or post**, they MUST accept the **Covenant** (`LEGAL-COV-01`). Acceptance is recorded against the internal ID with timestamp + version, with no other identifying data. |

### 3.2 Recording, masking & posting (`FR-POST-*`) — **the core flow**

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| FR-POST-01 | M | 1 | The flow MUST be **Open → Record → (mask) → Preview the mask → Post**, optimized for minimum friction (a person posting may be at their lowest). |
| FR-POST-02 | M | 1 | A topic tag MUST be **optional** and offered only as a final, skippable step. Posting MUST NOT require categorization. |
| FR-POST-03 | M | 1 | **Privacy-critical / Preview gate:** the masked clip MUST be played back to the poster and explicitly confirmed ("yes, that's not me") **before** anything is published. No post becomes public without passing this gate. |
| FR-POST-04 | M | 1 | The poster MUST choose a comment setting at post time: `off` / `text` / `audio` / `both` (enforcement is P2; the field is set in P1). |
| FR-POST-05 | M | 1 | **Privacy-critical:** by default the **original recording is destroyed** the instant the mask is produced. Default = destroy. |
| FR-POST-06 | S | 1 | The poster MAY opt in to **save the original to the device's Files app** (OS filesystem, outside the app sandbox). The platform MUST NOT retain it. |
| FR-POST-07 | M | 1 | On the first save-to-Files, the app MUST show a **safety warning** (a raw emotional recording can be found by a partner/parent/anyone with phone access) and suggest a **neutral default filename** (never "my breakdown about Dad.m4a"). |
| FR-POST-08 | M | 1 | A post record MUST store only: masked-audio reference, optional topic, duration, comment_mode, timestamps, reaction counts, owner internal ID. **No** original audio, transcript, or voiceprint. |
| FR-POST-09 | M | 1 | The poster MUST be able to **delete any of their own posts instantly and completely** (hard delete of row + masked audio object). |
| FR-POST-10 | C | 1 | The app SHOULD detect and gently warn when a poster says obviously **identifying details** (names, places, employers) — a guidance layer, explicitly **not** a guarantee. |

### 3.3 Feed, topics & reactions (`FR-FEED-*`)

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| FR-FEED-01 | M | 1 | The feed MUST be a scrollable timeline of masked voicenotes; each item shows a play button, **waveform**, duration, optional topic tag, relative time, and reaction counts. |
| FR-FEED-02 | M | 1 | Default feed = **everything** (tagged and untagged posts). |
| FR-FEED-03 | M | 1 | Sort options MUST include **Newest**, **Most heard**, and **Needs love** (surfaces low-listen posts so no one pours their heart out to silence). |
| FR-FEED-04 | M | 1 | A user MUST be able to **follow topics** (not people); following shapes the feed. |
| FR-FEED-05 | M | 1 | A user MUST be able to **browse a single topic** to find others going through the same thing. |
| FR-FEED-06 | M | 1 | **Reactions** MUST be empathy-first only: `Heard you` / `Felt this` / `Sending strength`. No approval/clout/like semantics. |
| FR-FEED-07 | M | 1 | Reaction **counts are public** (visible to everyone). The system MUST NOT implement karma, reputation, leaderboards, or any cross-post user score. |
| FR-FEED-08 | S | 1 | The UI MUST embody **anti-doomscroll** design: reactions framed as support not scores; an optional "that's enough for today" stopping point. |
| FR-FEED-09 | M | 1 | The initial topic set MUST include at least: Work life, Family, Relationships, Friendships, Mental health, Loneliness, Grief, Identity, Money, Health, "Just need to vent." |
| FR-FEED-10 | S | 1 | A user MUST be able to **Echo** (share/repost) a masked voicenote **within the app**. Sharing spreads the post, never a profile. (External sharing is forbidden by the Covenant.) |

### 3.4 Comments & poster control (`FR-CMT-*`) — Phase 2

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| FR-CMT-01 | M | 2 | The system MUST enforce the poster's `comment_mode` (`off` / `text` / `audio` / `both`) on every comment attempt. |
| FR-CMT-02 | M | 2 | Audio comments MUST run through the **same masking pipeline**; the commenter is unrecognizable and their original is destroyed too. |
| FR-CMT-03 | M | 2 | Comment threading MUST be **flat** — everyone replies to the original post; **no reply-to-reply** (parent_id does not exist). |
| FR-CMT-04 | M | 2 | Reactions MUST remain available **regardless** of the comment setting (even when comments are off). |
| FR-CMT-05 | M | 2 | All comments MUST pass moderation **pre-check** before reaching the poster (`FR-MOD-*`). |

### 3.5 Moderation (`FR-MOD-*`) — Phase 2

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| FR-MOD-01 | M | 2 | Moderation MUST perform a **three-way sort**: **Pain** (allow & protect), **Harm** (block), **Crisis** (offer help, never a violation). |
| FR-MOD-02 | M | 2 | **Safety-critical:** self-directed pain ("I want to die", "I feel worthless") MUST NEVER be blocked as a policy violation. The classifier's #1 job is distinguishing self-directed pain from other-directed harm. |
| FR-MOD-03 | M | 2 | Moderation MUST be a **pre-check** (before content reaches a vulnerable poster), targeted sub-second, backed by user reporting for anything that slips through. |
| FR-MOD-04 | M | 2 | For audio comments, moderation MUST transcribe **in-memory only**, weigh **tone of voice** (delivery, not just words), then **destroy raw audio + transcript**; only a passing mask survives. |
| FR-MOD-05 | M | 2 | Enforcement escalation MUST be: **rate-limit → shadow-mute → ban**, keyed on the hidden internal ID, never exposing identity. |
| FR-MOD-06 | M | 2 | Blocked content handling: **silent drop** for clear abuse (don't coach trolls); **soft "rephrase?" nudge** for borderline cases. |
| FR-MOD-07 | S | 2 | False-positive recovery: a light "this was hidden — doesn't feel right? tap to ask a human" path, with no heavy appeals bureaucracy. |
| FR-MOD-08 | M | 2 | Users MUST be able to **report** any post or comment; reports are **anonymous to the reported party** and the reporter is not linked to them in any exposed way. |
| FR-MOD-09 | M | 2 | Zero-tolerance categories (CSAM, etc.) MUST be detected, removed, and reported to authorities per `LEGAL-*`. |

### 3.6 Crisis hotline (`FR-HOT-*` / `CRIS-*`) — Phase 3 — **Safety-critical throughout**

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| FR-HOT-01 | M | 3 | A persistent, calm **"Talk to a human"** entry point MUST be always reachable and never buried — warm, not alarming. |
| FR-HOT-02 | M | 2→3 | Two ways in: (1) user-initiated tap; (2) moderation AI gently **offers** it on crisis signals ("Would it help to talk to a real person right now?"). Never forced, never punitive. |
| FR-HOT-03 | M | 3 | Three channels MUST exist: **PSTN via relay/proxy** (caller number not logged), **in-app VoIP/VoWiFi** (no number exposed, E2E), **E2E encrypted text**. |
| FR-HOT-04 | M | 3 | **Privacy-critical:** the user's voice MUST be **masked on every audio channel, including the live call** — even the responder never hears the real voice. Real-time masking uses **DSP** (near-zero latency). |
| CRIS-FALLBACK | M | 2→3 | **Safety-critical / no dead ends:** if no responder is available or the line is "closed," the system MUST automatically and instantly hand off to a **staffed national line**. A person in crisis MUST NEVER reach silence. |
| FR-HOT-05 | M | 3 | **Break glass:** the user — and only the user — MAY trigger revealing location/contact in imminent danger. The responder and platform MUST NEVER reveal it for them. Gated on legal counsel. |
| FR-HOT-06 | M | 3 | Coverage MUST be **24/7 from day one**, anchored by 24/7 partner crisis orgs. |
| FR-HOT-07 | M | 3 | Crisis content MUST NEVER be treated as a moderation violation; the author quietly receives support + resources. |
| FR-HOT-08 | M | 3 | Hotline conversation content MUST be **minimized** — retain only what safety law requires, encrypted, with explicit user disclosure of what (if anything) is kept. |
| FR-HOT-09 | S | 3 | The app SHOULD surface **region-appropriate** crisis hotline information and resources. |

### 3.7 Sustainability, ads & transparency (`FR-SUS-*`) — Phase 4

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| FR-SUS-01 | M | 4 | Ads MUST be **visual only — never audio**. The stream of human voices is sacred; no jingles, ever. |
| FR-SUS-02 | M | 4 | **Privacy-critical:** ad targeting MUST be **contextual (by topic being browsed), never behavioral**. No third-party tracking SDKs. |
| FR-SUS-03 | M | 4 | Ads MUST be **calm/discreet** (muted, bottom-anchored) and from **vetted advertisers only** (no gambling, predatory loans, alcohol near recovery content, sketchy "cures"). |
| FR-SUS-04 | M | 4 | **Zero ads** in any crisis/vulnerable surface: the hotline, "talk to a human," crisis-detection moments, resource cards, and the moment right after posting a heavy note. |
| FR-SUS-05 | M | 4 | The hotline MUST be **funded separately** (donations, grants, optional "Supporter" contribution) so it never depends on ad pressure. |
| FR-SUS-06 | S | 4 | The org SHOULD publish **radical money transparency** ("this month it costs $X to run; here's what came in; here's the gap"). |
| FR-SUS-07 | M | 4 | The org structure MUST enforce "survive, don't profit" (nonprofit and/or steward-ownership/charter) so it can't be acquired and turned against its users. |

---

## 4. Non-functional requirements

### 4.1 Privacy & data handling (`NFR-PRIV-*`) — **Privacy-critical, all M**

| ID | Phase | Requirement |
|---|---|---|
| NFR-PRIV-01 | 1 | **Original recordings, transcripts, and voiceprints MUST NEVER be persisted** to disk, logs, or storage. They exist in memory only, for the duration of conversion/classification, then are destroyed. |
| NFR-PRIV-02 | 1 | The masking/STT code paths MUST be asserted (by test + runtime guard) to write **no temp files**. CI MUST fail if a temp-file write is detected in these paths. |
| NFR-PRIV-03 | 1 | Logs MUST NEVER contain raw audio, transcripts, or (later) phone numbers. Request bodies MUST be scrubbed before logging. |
| NFR-PRIV-04 | 1 | The hidden internal ID MUST NEVER be serialized into any user-facing response. (Contract test enforced.) |
| NFR-PRIV-05 | 1 | There MUST be **no API endpoint** that returns a public profile or any cross-post history of an account. Enforced at the API layer (not just the UI). |
| NFR-PRIV-06 | 1 | Deletes MUST be **hard deletes** (row + object), not soft flags. |
| NFR-PRIV-07 | 1 | Data minimization: only the fields in §5 may be stored. Adding a new stored field requires privacy review sign-off. |
| NFR-PRIV-08 | 4 | No behavioral tracking, no third-party analytics/ad SDKs that profile users. Any analytics MUST be aggregate and non-identifying. |

### 4.2 Security (`SEC-*`)

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| SEC-01 | M | 1 | All transport MUST be encrypted (TLS 1.2+). |
| SEC-02 | M | 1 | Masked audio at rest MUST be encrypted; the database MUST be encrypted at rest. |
| SEC-03 | M | 3 | Hotline text MUST be **end-to-end encrypted**; hotline voice E2E is the goal where the architecture allows. |
| SEC-04 | M | 1 | Object-store access to masked audio MUST be authorized per request (signed, short-lived URLs); objects MUST NOT be publicly enumerable. |
| SEC-05 | M | 1 | Abuse controls (rate limits, report handling, shadow-mute/ban) MUST exist from day one of public exposure. |
| SEC-06 | M | 1 | Secrets MUST be managed via a secrets manager, never in source or images. |
| SEC-07 | S | 1 | A security review MUST precede each public-facing phase release; a third-party pen test SHOULD precede GA. |
| SEC-08 | M | 3 | PSTN inbound MUST route through a relay/proxy number; caller ID MUST NOT be logged. |

### 4.3 Performance & reliability (`NFR-PERF-*`)

| ID | Priority | Phase | Target |
|---|---|---|---|
| NFR-PERF-01 | M | 1 | Neural masking latency (post): target **< ~10 s** for a typical clip (benchmark-driven; see §11). Must not feel like an upload that hangs — show progress. |
| NFR-PERF-02 | M | 3 | Real-time DSP masking (live call): **near-zero added latency** (target end-to-end mouth-to-ear added delay < 150 ms) so a call doesn't feel like satellite delay. |
| NFR-PERF-03 | M | 2 | Moderation pre-check: targeted **sub-second** for text; audio bounded by STT + classify, with a fast pre-filter. |
| NFR-PERF-04 | M | 1 | Feed read latency p95 **< 300 ms** server-side at expected MVP load. |
| NFR-PERF-05 | M | 3 | Hotline availability MUST be **24/7 with no dead ends** (`CRIS-FALLBACK`); design for graceful degradation to national lines, not outage. |
| NFR-PERF-06 | S | 1 | The masking service MUST be horizontally scalable (GPU worker pool behind a queue) and back-pressure safely under load. |

### 4.4 Accessibility & UX quality (`NFR-UX-*`)

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| NFR-UX-01 | M | 1 | The app MUST meet **WCAG 2.2 AA** where applicable (contrast, focus, touch targets), and support OS dynamic type / screen readers. |
| NFR-UX-02 | M | 1 | The recording and "Talk to a human" flows MUST be operable one-handed and reachable within minimal taps. |
| NFR-UX-03 | S | 1 | Provide visible captions/transcripts? **No** — transcripts are not stored. Provide waveform + duration as the visual affordance. (Open question: optional client-side captions — see §12.) |
| NFR-UX-04 | M | 1 | The tone of all copy MUST be calm, warm, non-clinical, non-gamified (per the brand voice in the concept doc). |

### 4.5 Compliance & legal (`LEGAL-*`)

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| LEGAL-COV-01 | M | 1 | The **Covenant** MUST be presented and explicitly accepted before listening/posting, version-tracked. |
| LEGAL-01 | M | 0 | Legal counsel MUST advise on **crisis duty-of-care**, anonymity-vs-rescue, and **multi-jurisdiction** rules before the hotline launches. This **gates Phase 3**. |
| LEGAL-02 | M | 0 | **Minimum age** and parental-consent rules MUST be finalized per region with counsel; enforced at signup. |
| LEGAL-03 | M | 1 | A binding **Terms of Service + Privacy Policy** MUST be prepared with counsel per region before GA. The current Terms are an explicit DRAFT. |
| LEGAL-04 | M | 2 | **Mandatory-reporting** obligations (CSAM, imminent-harm where law requires) MUST be implemented per jurisdiction. |
| LEGAL-05 | M | 4 | The **nonprofit / steward-ownership** structure MUST be legally established to enforce "survive, don't profit." |
| LEGAL-06 | S | 1 | GDPR/CCPA-style data-subject rights are largely satisfied by design (no PII, hard delete), but counsel MUST confirm per region. |

---

## 5. Data model requirements (`DATA-*`)

Postgres-style relational core. **What is deliberately absent is as important as what is present.**

**Stored tables (P1–P2):**

| Table | Key columns | Notes |
|---|---|---|
| `accounts` | `internal_id` (PK), `created_at`, `ban_state`, `rate_state`, `covenant_version`, `covenant_accepted_at` | Hidden internal ID only; never exposed. |
| `posts` | `id`, `owner_id → accounts`, `masked_audio_key`, `topic` (nullable), `duration`, `comment_mode`, `created_at` | `comment_mode ∈ {off,text,audio,both}`. `masked_audio_key` → object store. |
| `reactions` | `post_id`, `account_id`, `type`, `created_at` | `type ∈ {heard,felt,strength}`. One row per (account,post,type). Counts public. |
| `comments` (P2) | `id`, `post_id`, `account_id`, `kind`, `body_text` (nullable), `masked_audio_key` (nullable), `created_at` | `kind ∈ {text,audio}`. **No `parent_id`** — flat by design. |
| `reports` (P2) | `id`, `target_type`, `target_id`, `reason`, `created_at` | Reporter NOT linked to reported user in any exposed way. |
| `topic_follows` | `account_id`, `topic` | Drives topic-filtered feed. |
| `echoes` | `post_id`, `account_id`, `created_at` | In-app reshare only. |

**Storage tiers:**
- **Object store:** masked audio only, **encrypted at rest** (`DATA-OBJ-01`).
- **Postgres:** the tables above.
- **Redis:** masking/moderation **job queue** + sliding-window **rate-limit** state (ephemeral).

**Never stored (`DATA-NEVER-01`, privacy-critical):** original recordings, transcripts, voiceprints/biometrics, public profiles, posting histories, hotline caller phone numbers, behavioral tracking profiles.

| ID | Requirement |
|---|---|
| DATA-01 | Schema migrations MUST be reviewed for privacy impact; any new column storing user-derived content requires privacy sign-off. |
| DATA-02 | Reaction counts SHOULD be maintained as denormalized counters (updated transactionally or via the queue) for feed performance. |
| DATA-03 | Hard delete of a post MUST cascade: masked audio object + reactions + comments + echoes referencing it. |
| DATA-04 | `reports` MUST be structurally unable to join reporter→reported in any user-facing query path. |

---

## 6. Crisis-safety design requirements (cross-cutting) — **Safety-critical**

Because lives are at stake, the hotline and crisis path get more rigor than the social side. These requirements are **non-negotiable** and cannot be descoped to hit a date.

1. **No dead ends (`CRIS-FALLBACK`).** Every crisis path resolves to a staffed human or staffed national line — never silence, never a "try again later."
2. **Crisis ≠ violation.** Crisis content is met with help and resources; the author is never punished, blocked, or flagged as a rule-breaker (`FR-HOT-07`, `FR-MOD-02`).
3. **Anonymity follows to the human.** Voice masked on every audio channel including live calls (`FR-HOT-04`).
4. **Break glass is user-only.** Only the person in crisis can reveal location/contact; never the responder or platform (`FR-HOT-05`).
5. **Trained humans + clinical oversight.** Launch via vetted partner orgs (988/Lifeline, Samaritans, Crisis Text Line, local equivalents); own peer + clinical tiers later (Phase 5).
6. **Legal gate.** Multi-jurisdiction duty-of-care counsel MUST be complete before Phase 3 (`LEGAL-01`).
7. **Minimal retention.** Crisis conversations retain only what law requires, encrypted, with explicit user disclosure (`FR-HOT-08`).
8. **Interim safety bridge.** Until the hotline (P3) exists, any P2 crisis detection routes to vetted external national lines + resource cards. This bridge ships **with** crisis detection, never after.

---

## 7. Architecture requirements

### 7.1 Component decomposition (target)

```
CLIENT (React Native + TypeScript; iOS + Android; web later via TanStack Start)
  - Record / preview-mask / post / feed / react / (comment) / delete
  - Hotline launcher (P3): PSTN / VoIP / E2E text
  - "My posts" private view; optional save-original-to-Files
        |  HTTPS / TLS
API GATEWAY (Node.js + TypeScript)
  - Auth, feed, posts, reactions, comments, reports, topic-follow
  - Enqueues masking + moderation jobs; serves signed audio URLs
        |                                   |
MASKING SERVICE (Python, GPU)        MODERATION (STT in-memory + LLM classifier)
  - neural voice conversion             - pain / harm / crisis sort
  - raw audio in-memory only            - tone weighting on audio
  - delete raw after convert            - destroy transcript after read
        |
REAL-TIME MASKING GATEWAY (P3, DSP, low-latency)  — live hotline audio
HOTLINE ORCHESTRATION (P3) — routing, queueing, national-line fallback
        |
STORAGE
  - Object store: masked audio only (encrypted at rest)
  - Postgres: accounts, posts, reactions, comments, reports, topic_follows
  - Redis: job queue + rate-limit state
  - NEVER: originals, transcripts, voiceprints, profiles, histories
```

### 7.2 Architecture requirements (`ARCH-*`)

| ID | Priority | Requirement |
|---|---|---|
| ARCH-01 | M | Masking MUST be a **separate service** from the gateway, communicating via a queue, so GPU workers scale independently and raw audio never lands in the general API tier's storage. |
| ARCH-02 | M | The gateway MUST **stream** uploaded bytes to the masking service **without writing to disk** (`NFR-PRIV-02`). |
| ARCH-03 | M | Masked audio is written to the object store **only after** successful conversion; the raw buffer is discarded immediately after (`FR-POST-05`). |
| ARCH-04 | M | The two masking engines MUST be cleanly separated: **batch neural VC** (posts/comments) and **real-time DSP gateway** (live calls, P3). Shared contract: words clear, emotion preserved, user previews/has-mask before anyone else hears. |
| ARCH-05 | S | Masking is **always server-side; no on-device path** (explicit decision — works on any phone, simpler build; accepted trade-off that raw audio briefly touches a server in-memory). |
| ARCH-06 | M | Job processing MUST be idempotent and crash-safe such that a failed masking job leaves **no** persisted raw audio. |
| ARCH-07 | S | Provider choices SHOULD remain swappable: Supabase (anon auth, Postgres, object storage, edge functions) for fastest path; Neon (serverless Postgres, MCP already connected) + S3-compatible storage as documented alternative. |

### 7.3 Masking pipeline (canonical order — `ARCH-PIPE-01`)

1. Client records; uploads over TLS to gateway.
2. Gateway streams bytes to Masking Service (no disk write).
3. Masking Service converts in-memory → masked audio buffer.
4. Masked audio written to object store (encrypted at rest).
5. Raw audio buffer discarded immediately (never persisted).
6. Post row created; masked clip returned to client for **preview/publish** (the publish step requires user confirmation per `FR-POST-03`).

### 7.4 Moderation pipeline (`ARCH-PIPE-02`, P2)

```
Text comment  → LLM classifier (pain/harm/crisis) → allow | block | offer-help
Audio comment → STT (in-memory) → LLM classifier (+tone) → mask → allow | block | offer-help
              → destroy raw audio + transcript (only a passing mask survives)
Post          → same crisis check; crisis ⇒ gently surface help (never blocked)
```

---

## 8. Voice masking requirements (the heart) (`MASK-*`)

| ID | Priority | Phase | Requirement |
|---|---|---|---|
| MASK-01 | M | 1 | The masking engine MUST be **neural voice conversion (audio-to-audio)** for posts/comments: keep pitch contour, timing, pauses, breaths; swap only timbre. **Transcript→TTS resynthesis is rejected** (it kills the emotion that is the message). |
| MASK-02 | M | 1 | All users MUST be mapped into a **small shared set of neutral target voices** (not a unique voice per person) — maximizes anonymity and gives the app a sonic identity. |
| MASK-03 | M | 1 | Words MUST remain **perfectly clear** in the output; emotion preserved as much as the engine allows. |
| MASK-04 | M | 1 | Candidate models (RVC / so-vits-svc family and similar) MUST be **evaluated for quality, latency, GPU cost, and license terms** before adoption; licensing/ethics for this use MUST be confirmed (`RISK-LIC`). |
| MASK-05 | M | 3 | The **real-time path** MUST use **DSP pitch + formant shifting** through a low-latency gateway for live calls (neural too slow live). |
| MASK-06 | M | 1 | The masked output MUST be the **only audio artifact** the platform keeps. |
| MASK-07 | S | 5 | Stronger neural real-time masking SHOULD be pursued as latency budgets allow (Phase 5). |
| MASK-08 | M | 1 | **Quality acceptance:** a masked clip MUST pass (a) intelligibility check (human raters: words clear), (b) anonymity check (raters cannot match masked→speaker above chance), and (c) emotion-preservation check (pauses/breaks/tone judged intact). Define rater protocol in §11. |

---

## 9. API requirements (`API-*`, illustrative contract)

| ID | Method/Path | Notes |
|---|---|---|
| API-01 | `POST /v1/posts` | Create post (multipart audio) → returns masked post for preview/publish. Enforces preview gate semantics. |
| API-02 | `GET /v1/feed?sort=&topic=` | Paginated feed; `sort ∈ {newest,most_heard,needs_love}`. |
| API-03 | `DELETE /v1/posts/:id` | Hard delete own post (cascade per `DATA-03`). |
| API-04 | `POST /v1/posts/:id/reactions` | Add/remove a reaction. |
| API-05 | `POST /v1/posts/:id/comments` | Add text or audio comment; respects `comment_mode` (P2). |
| API-06 | `GET /v1/posts/:id/comments` | List comments (flat). |
| API-07 | `POST /v1/topics/:topic/follow` | Follow/unfollow a topic. |
| API-08 | `POST /v1/reports` | Report a post or comment. |
| API-09 | `GET /v1/me/posts` | Private "my posts" view (self only). |
| API-10 | `POST /v1/echoes` | In-app reshare. |

**API-wide rules:** every response MUST omit internal IDs (`NFR-PRIV-04`); no endpoint may return another account's history/profile (`NFR-PRIV-05`); audio is served via signed short-lived URLs (`SEC-04`); all endpoints rate-limited (`SEC-05`).

---

## 10. Roadmap (phased) — milestones, deliverables, exit criteria

> Estimates are **planning ranges** for a small senior team (assume ~2 mobile, ~2 backend, 1 ML, 1 design, fractional security/legal/clinical). They are *t-shirt* sizes, not commitments; the masking benchmark (P1-M2) is the biggest source of variance.

### Phase 0 — Foundations & safety design (gating)
**Goal:** make the dangerous parts safe before building the easy parts.
**Workstreams**
- Engage legal counsel: crisis duty-of-care, anonymity-vs-rescue, multi-jurisdiction, minimum age (`LEGAL-01`, `LEGAL-02`).
- Select crisis partner org(s) for launch; design national-line **fallback routing** on paper (`CRIS-FALLBACK`).
- Lock the **privacy/data-handling spec** (§5, §4.1) as the binding contract.
- Stand up repo, CI, environments, secrets management, threat model.
**Exit criteria:** signed privacy spec; counsel engaged with a written scope; ≥1 partner org in discussion; threat model reviewed; CI green skeleton.
**Estimate:** ~2–4 weeks (legal runs in parallel and continues into later phases).

### Phase 1 — Core social MVP
**Goal:** record → mask → preview → post → feed, identity-less, with originals destroyed.
**Milestones**
- **P1-M1 Foundations:** anonymous auth, `accounts` table, object store + DB + Redis wiring, Covenant acceptance gate (`FR-ACCT-01/02/07`, `SEC-01/02/06`).
- **P1-M2 Masking service (highest risk):** pick + **benchmark** a VC model (`MASK-04`); in-memory pipeline with no disk writes (`NFR-PRIV-01/02`); preview gate (`FR-POST-03`); quality acceptance (`MASK-08`).
- **P1-M3 Post + feed:** create/post, feed with three sorts, optional topics + follow, hard delete, "my posts" (`FR-FEED-*`, `FR-POST-08/09`, `FR-ACCT-04`).
- **P1-M4 Engagement-lite:** reactions with public counts (`FR-FEED-06/07`); Echo (`FR-FEED-10`).
- **P1-M5 Originals & save:** default destroy; opt-in save-to-Files with warning + neutral filename (`FR-POST-05/06/07`).
- **P1-M6 Hardening:** privacy assertions in CI (temp-file guard, internal-ID leak contract tests), security review, load-test the masking path (`NFR-PRIV-02/04`, `SEC-07`, `NFR-PERF-01/06`).
**Exit criteria (Definition of Done for MVP):**
- A user can post and the **original is provably destroyed** (test asserts no persistence).
- Preview gate cannot be bypassed.
- No endpoint exposes profiles/history/internal IDs (contract tests pass).
- Masking passes intelligibility + anonymity + emotion acceptance with human raters.
- Hard delete verified to remove row + object + dependents.
- Security review completed with no criticals open.
**Estimate:** ~8–14 weeks (driven by P1-M2 masking benchmark).

### Phase 2 — Interaction & moderation
**Goal:** safe two-way interaction; the three-way moderation sort; abuse controls; crisis **detection** with an interim safety bridge.
**Milestones**
- **P2-M1 Comments:** text + masked audio comments through the same pipeline; flat threading; poster control panel enforcement (`FR-CMT-*`).
- **P2-M2 Moderation AI:** pain/harm/crisis classifier + fast pre-filter; in-memory STT + transcript destruction; tone weighting (`FR-MOD-01..06`, `ARCH-PIPE-02`).
- **P2-M3 Abuse controls:** rate-limit → shadow-mute → ban on internal ID; reporting (reporter-unlinked) (`FR-MOD-05/08`, `SEC-05`).
- **P2-M4 Crisis detection + bridge:** gentle in-app offer on crisis signal (`FR-HOT-02`); **interim routing to vetted national lines + resource cards** until P3 (`CRIS-FALLBACK` interim).
- **P2-M5 Recovery & legal:** false-positive "ask a human" path (`FR-MOD-07`); mandatory-reporting hooks (`LEGAL-04`).
**Exit criteria:** pain is never blocked (red-team test set); abuse pre-check lands before the poster sees it; crisis signal always reaches a staffed external line; classifier accuracy meets an agreed bar on a labeled eval set with human review of edge cases.
**Estimate:** ~8–12 weeks. **Safety-critical** items get clinical-advisor review.

### Phase 3 — The human hotline
**Goal:** real humans inside the app, anonymity preserved, 24/7, no dead ends. **Gated by `LEGAL-01`.**
**Milestones**
- **P3-M1 Real-time masking gateway:** DSP pitch+formant, low latency (`MASK-05`, `NFR-PERF-02`).
- **P3-M2 Three channels:** PSTN relay (caller ID not logged), in-app VoIP/VoWiFi (E2E, no number), E2E text (`FR-HOT-03`, `SEC-03/08`).
- **P3-M3 Orchestration:** routing, queueing, **automatic national-line fallback** (`CRIS-FALLBACK`); 24/7 coverage anchored by partners (`FR-HOT-06`).
- **P3-M4 Break glass:** user-only location/contact reveal, counsel-approved (`FR-HOT-05`).
- **P3-M5 Retention & disclosure:** minimal encrypted retention with explicit user disclosure (`FR-HOT-08`).
**Exit criteria:** every channel masks live voice; fallback proven under "no responder" and "line closed" drills; break glass works and is user-triggered only; legal sign-off complete; load/failover drills pass.
**Estimate:** ~10–16 weeks (telephony + 24/7 ops + legal dominate).

### Phase 4 — Sustainability & trust
**Goal:** keep the lights on without betraying the mission.
**Milestones:** contextual, vetted, **crisis-free, audio-free** banner ads (`FR-SUS-01..04`); separate hotline funding (donations/Supporter) (`FR-SUS-05`); public money transparency (`FR-SUS-06`); establish nonprofit/steward-ownership (`FR-SUS-07`, `LEGAL-05`).
**Exit criteria:** no tracking SDKs present (audit); zero ads in vulnerable surfaces (test); legal entity established.
**Estimate:** ~6–10 weeks engineering + parallel legal/finance.

### Phase 5 — Deepen support & quality
**Goal:** own peer + clinical responder tiers alongside partners; stronger neural real-time masking as latency allows (`MASK-07`); continuous moderation tuning + ongoing safety review.
**Estimate:** ongoing.

### Roadmap dependency map
- `LEGAL-01` (P0) **gates** all of Phase 3.
- P1-M2 masking benchmark **gates** P1 quality exit and informs P3 real-time budget.
- P2 crisis detection **must ship with** the interim national-line bridge (never detection alone).
- Phase 4 ads **must not** start before the "zero ads in vulnerable surfaces" guard exists.

---

## 11. Testing, evaluation & verification strategy

- **Privacy invariants (CI gates, privacy-critical):** temp-file write detector on masking/STT paths; static + contract tests that internal IDs never serialize; endpoint tests that no profile/history route exists; delete-cascade tests; "no original after post" integration test.
- **Masking quality evals (`MASK-08`):** maintain a held-out clip set; human-rater protocol scoring (a) intelligibility, (b) speaker-match-above-chance (anonymity), (c) emotion preservation. Track per model candidate; set release thresholds before P1 exit.
- **Moderation evals:** labeled corpus across pain/harm/crisis with deliberate hard cases ("I want to die" must classify as crisis-not-violation). Track precision/recall per class; **pain-blocked = critical defect**. Include tone-of-voice audio cases.
- **Crisis/safety drills (safety-critical):** scripted "no responder," "line closed," and "break glass" exercises with the partner org; verify no dead ends; measure time-to-human.
- **Performance:** load-test masking GPU pool (throughput, queue depth, back-pressure); feed p95; live-call mouth-to-ear latency.
- **Security:** per-phase security review; pre-GA third-party pen test; secrets scanning in CI.
- **Accessibility:** automated + manual WCAG 2.2 AA passes on record and "talk to a human" flows.

---

## 12. Open questions / decisions needed

1. **Optional client-side captions** for accessibility without storing transcripts — feasible on-device? (`NFR-UX-03`)
2. **VC model choice** — RVC vs so-vits-svc vs other; license terms for commercial/nonprofit use; self-host vs managed GPU (`MASK-04`, `RISK-LIC`).
3. **STT** — self-hosted Whisper vs API for in-memory moderation; latency/cost trade (`FR-MOD-04`).
4. **Auth/DB stack** — Supabase (fastest) vs Neon + S3 (MCP already connected); pick before P1-M1.
5. **Telephony provider** for PSTN relay + real-time audio injection masking (P3).
6. **Minimum age + parental consent** per launch region (counsel) (`LEGAL-02`).
7. **Break-glass legal model** per jurisdiction (`FR-HOT-05`, `LEGAL-01`).
8. **Launch regions** — drives legal scope, partner orgs, and resource cards.
9. **Identifying-details detector** (`FR-POST-10`) — on-device vs server (server reintroduces a transcript-touch concern).

---

## 13. Risk register

| ID | Risk | Impact | Mitigation |
|---|---|---|---|
| RISK-MASK | Neural VC can't keep emotion intact while being unrecognizable, or GPU cost/throughput is prohibitive | Core product fails | Early benchmark (P1-M2); rater acceptance gate; cost modeling; DSP fallback understood |
| RISK-LIC | Chosen VC/STT models not licensed for this use | Legal/ship blocker | License review in P0/P1 before adoption (`MASK-04`) |
| RISK-MOD | Pain-vs-harm line mis-drawn; pain silenced | Harms the exact users we protect; reputational | Labeled evals, pain-block = critical, human review of edges, soft nudges over hard blocks |
| RISK-LEGAL | Crisis duty-of-care / multi-jurisdiction unresolved | Cannot launch hotline; liability | P0 counsel engagement gating Phase 3 |
| RISK-ABUSE | Anonymous comments are the top abuse vector | Drives away vulnerable users | Pre-check moderation + internal-ID bans from day one |
| RISK-DEADEND | A crisis path reaches silence | Life-safety | `CRIS-FALLBACK` everywhere; drills; interim bridge ships with detection |
| RISK-PRIV-LEAK | Raw audio/transcript/internal ID persisted or logged | Breaks the founding promise | CI privacy gates; in-memory-only asserts; scrubbed logs; privacy review on schema changes |
| RISK-FUND | Contextual no-tracking ads can't fund 24/7 humans | Hotline unsustainable | Separate hotline funding (grants/donations/Supporter); nonprofit structure; transparent books |
| RISK-MISSION | Org acquired and turned against users | Existential to the mission | Nonprofit/steward-ownership charter baked in (Phase 4) |

---

## 14. Appendix — rejected & resolved decisions (do not relitigate without cause)

- **Rejected:** transcript→TTS resynthesis (kills emotion); on-device masking (excludes weak phones, complicates build); ephemeral posts (posts are permanent until user deletes); reply-to-reply threading (flat only); live "whisper rooms" (stay focused on feed + 1:1 hotline); behavioral/audio ads; karma/leaderboards/profiles.
- **Resolved:** name = **Unheard**; reaction counts **public** (+ "Needs love" counterweight); **one small shared set** of neutral mask voices; masking **always server-side**; **break glass = user-triggered only**; **24/7 from day one** via partners; **partner orgs first**, own tiers later; comment threading **flat**.

---

*This is a living engineering artifact. The vision and the two overriding principles (identity-less; survive-don't-profit) are fixed. Requirement IDs are stable for traceability; open questions in §12 are where the next decisions happen.*
