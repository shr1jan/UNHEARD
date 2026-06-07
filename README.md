# UNHEARD

> **Be heard, anonymously. A human if you need one. We keep none of your voice, and we keep none of the profit.**

Unheard is an **anonymous, voice-only social space** where people share what they're going through — out loud, in their own emotional voice, with their identity made unrecognizable — and a **real human is reachable** the moment they need one.

This repository holds the **product concept, requirements, roadmap, and engineering backlog**. It is a planning repo at the pre-build stage; application code does not exist yet.

---

## Table of contents

- [What it is](#what-it-is)
- [Why it exists](#why-it-exists)
- [The two principles that override everything](#the-two-principles-that-override-everything)
- [How it works (end to end)](#how-it-works-end-to-end)
- [The Covenant](#the-covenant)
- [Repository structure](#repository-structure)
- [Documents index](#documents-index)
- [The roadmap at a glance](#the-roadmap-at-a-glance)
- [The backlog](#the-backlog)
- [Architecture overview](#architecture-overview)
- [What is never stored](#what-is-never-stored)
- [Contributing & workflow](#contributing--workflow)
- [Status & disclaimers](#status--disclaimers)

---

## What it is

You open the app and record a voicenote about whatever you're going through. Before anyone hears it, your **voice is transformed so it's unrecognizable** — but every word stays perfectly clear, and the emotion (pauses, breaks, tone) is preserved. Your post drops into a **feed of human voices**. Others can react, comment (by text or their own masked voice), and browse by topic to find people going through the same thing. At any moment you can reach a **real, trained human** for support — by phone, in-app call, or encrypted text — and you stay unrecognizable even to them.

The app stores nothing of your real voice, you have no profile and no visible history, and it runs on only enough money to survive — not for profit.

## Why it exists

The heaviest things people carry are the ones they hide from those closest to them. Text strips the humanity out of those moments — a typed "I'm not okay" is flat. A voice carries everything: the crack on a word, the three-second pause before a confession, the shaky breath. The barrier has always been **identity** — people won't share their rawest moments if their voice could give them away. Unheard removes that barrier: **keep the full emotion of the human voice, remove the identity entirely.**

## The two principles that override everything

These are acceptance gates, not aspirations. Anything that conflicts with them is a defect, regardless of how well it works.

1. **Identity-less by design** — no real voice stored, no profiles, no aggregatable history. The unit of the network is the *voicenote*, not the *person*.
2. **Survive, don't profit** — funding and structure are a ceiling, not a growth target. Built as a nonprofit / steward-owned org so it can never be acquired and turned against the people it protects.

## How it works (end to end)

```
Open app → Record → (voice masked, server-side) → Preview the mask → Post
                                                       │
                            "yes, that's not me" confirmation required
                                                       │
                                          drops into a feed of human voices
                                                       │
            react ("Heard you" / "Felt this" / "Sending strength") · comment · Echo · follow topics
                                                       │
                          ── at any moment ──►  Talk to a human (phone · in-app call · encrypted text)
                                                       │
                                          voice masked even to the responder · 24/7 · no dead ends
```

- **The original recording is destroyed** the instant the mask exists. The masked clip is the only audio artifact the platform keeps.
- **Preview is sacred** — you always hear your masked clip and confirm before anything goes public.
- **No profiles, no followers, no visible history.** Each voicenote stands alone.
- **Moderation is a three-way sort:** Pain (protect — never blocked), Harm (block), Crisis (offer help, never punish).

## The Covenant

Technology hides the voice. The Covenant binds the listener. Every user accepts it before they can listen or post:

> **What you hear here is someone's wound, shared in trust. You will never use it to identify them, never carry it outside these walls, and never speak badly of it — anywhere, to anyone.**

Breaking it is the gravest violation on the platform.

---

## Repository structure

```
.
├── README.md                                          ← you are here
├── Unheard - One-Page Brief.docx                      ← for partners & supporters
├── Unheard - Concept and Technical Document.docx      ← the full vision + technical concept
├── Unheard - Engineering Build Plan (Phase 1 MVP).docx← MVP engineering plan
├── Unheard - Terms and Community Guidelines.docx      ← plain-language draft terms (pending counsel)
├── Unheard - Development Requirements and Roadmap.md  ← THE SPEC: traceable requirements + phased roadmap
├── backlog/                                            ← execution-ready epics & issues
│   ├── README.md                                       ← backlog index, labels, build order, dependency gates
│   └── E0-foundations.md … E11-deepen.md               ← 12 epics, 72 issues, each w/ acceptance criteria
└── scripts/
    └── create_github_issues.py                         ← idempotent generator: labels + milestones + issues
```

## Documents index

| Document | Audience | What it covers |
|---|---|---|
| [One-Page Brief](Unheard%20-%20One-Page%20Brief.docx) | Partners, crisis orgs, supporters | The pitch, the ask |
| [Concept & Technical Document](Unheard%20-%20Concept%20and%20Technical%20Document.docx) | Everyone | Full vision, UX, masking, hotline, moderation, sustainability, resolved decisions, glossary |
| [Engineering Build Plan (Phase 1 MVP)](Unheard%20-%20Engineering%20Build%20Plan%20(Phase%201%20MVP).docx) | Engineers | MVP scope, stack, data model, pipelines, milestones, risks |
| [Terms & Community Guidelines](Unheard%20-%20Terms%20and%20Community%20Guidelines.docx) | Users / legal | Plain-language draft terms (DRAFT — pending counsel) |
| **[Development Requirements & Roadmap](Unheard%20-%20Development%20Requirements%20and%20Roadmap.md)** | Eng / product / security / legal | **The spec** — traceable `FR/NFR/SEC/DATA/MASK/CRIS/LEGAL` requirements + the full phased roadmap |

> **Reading order:** Brief → Concept doc → Requirements & Roadmap → `backlog/README.md`.

## The roadmap at a glance

| Phase | Theme | Key outcomes |
|---|---|---|
| **0** | Foundations & safety design | Legal counsel engaged; crisis partner(s); privacy spec locked; CI + threat model |
| **1** | Core social MVP | Record → server mask → preview → post; feed (Newest/Most heard/Needs love); topics; reactions; "my posts"; instant hard delete; originals destroyed by default |
| **2** | Interaction & moderation | Comments (text + masked audio) + poster controls; AI moderation (pain/harm/crisis); reporting; rate-limit→shadow-mute→ban; crisis detection + interim national-line bridge |
| **3** | Human crisis hotline | Three channels (PSTN relay / in-app VoIP / E2E text); real-time DSP masking; 24/7 no-dead-ends; user-only "break glass" |
| **4** | Sustainability & trust | Contextual non-tracking ads (visual only); separate hotline funding; money transparency; nonprofit/steward-ownership |
| **5** | Deepen support & quality | Own peer + clinical responder tiers; stronger real-time neural masking; ongoing moderation tuning |

**Hard gates:**
- Legal counsel sign-off **gates all of Phase 3** (the hotline).
- Crisis detection (Phase 2) ships **with** the interim national-line bridge — never detection alone (no dead ends).
- The Phase 1 masking benchmark gates the MVP quality exit and feeds the Phase 3 real-time latency budget.

Full detail, with exit criteria per phase: **[Development Requirements & Roadmap → §10](Unheard%20-%20Development%20Requirements%20and%20Roadmap.md)**.

## The backlog

The roadmap is decomposed into **12 epics / 72 issues** under [`backlog/`](backlog/README.md). Each issue carries:

- a scope line and **acceptance criteria** (Definition of Done),
- **requirement-ID traceability** back to the spec,
- **labels** (`privacy-critical` 🛡️, `safety-critical` 🔒, `core`, `ml`, `infra`, `client`, `backend`, `legal`, `risk`),
- explicit **Blocked by / Blocks** dependency links.

These are mirrored into **GitHub Issues** (grouped by phase **Milestones**) — regenerate or sync them with:

```bash
python3 scripts/create_github_issues.py            # create/sync labels, milestones, and issues (idempotent)
python3 scripts/create_github_issues.py --dry-run  # preview without writing anything
```

## Architecture overview

```
CLIENT (React Native + TS; iOS + Android; web later via TanStack Start)
        │  HTTPS / TLS
API GATEWAY (Node.js + TypeScript)  — auth, feed, posts, reactions, comments, reports, topic-follow
        │                                   │
MASKING SERVICE (Python, GPU)        MODERATION (in-memory STT + LLM classifier)
  neural voice conversion              pain / harm / crisis sort; tone weighting
  raw audio in-memory only             transcript destroyed after read
  delete raw after convert
        │
REAL-TIME MASKING GATEWAY (Phase 3, DSP, low-latency)  — live hotline audio
HOTLINE ORCHESTRATION (Phase 3) — routing, queueing, national-line fallback
        │
STORAGE
  Object store: masked audio only (encrypted at rest)
  Postgres: accounts, posts, reactions, comments, reports, topic_follows
  Redis: job queue + rate-limit state
```

**Recommended stack:** React Native + TypeScript (client), Node.js + TypeScript (gateway), Python + GPU (masking), Supabase *or* Neon + S3-compatible storage (auth/DB/object store), Whisper (in-memory STT for moderation only), an LLM classifier (e.g. Claude API) for the nuanced pain-vs-harm-vs-crisis judgement, Redis (queue + rate-limit).

## What is never stored

This list is as load-bearing as any feature:

- ❌ Original recordings (destroyed after conversion; optionally exported by the user to their own Files app)
- ❌ Transcripts (in-memory only, for moderation, then destroyed)
- ❌ Voiceprints / biometrics (never extracted)
- ❌ Public profiles / posting histories (do not exist by design)
- ❌ Hotline caller phone numbers (routed via relay, not logged)
- ❌ Behavioral tracking profiles (no third-party tracking SDKs)

✅ The **only** audio artifact kept is the **masked voicenote**, encrypted at rest, hard-deletable by the poster instantly.

## Contributing & workflow

1. Pick an issue from a **Milestone** (work phases in order; within a phase, respect "Blocked by").
2. Branch from `main`; keep changes scoped to one issue where possible.
3. **`privacy-critical` 🛡️ and `safety-critical` 🔒 issues require elevated review** and cannot be descoped to hit a date. Privacy invariants are enforced as CI gates (no temp-file writes on audio paths; internal IDs never serialized; no profile/history endpoints; log scrubbing).
4. An issue is **Done** only when all its acceptance criteria are met.

## Status & disclaimers

- **Status:** Concept / pre-build planning. No application code yet.
- **Not a medical or emergency service.** Unheard is a peer space and a doorway to a human — **not** therapy, counseling, medical care, or an emergency service. If you or someone else is in immediate danger, call your local emergency number now (e.g. 911 in the US, 112 in much of Europe, 999 in the UK).
- **Terms are a DRAFT** pending qualified legal counsel per region. The binding Terms of Service and Privacy Policy will be prepared with counsel before launch.

---

*This is a living planning repository. The vision and the two overriding principles are fixed; open questions are tracked in the [Requirements & Roadmap (§12)](Unheard%20-%20Development%20Requirements%20and%20Roadmap.md) and in the issue tracker.*
