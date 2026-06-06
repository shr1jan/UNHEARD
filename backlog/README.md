# Unheard — Development Backlog

Execution-ready breakdown of the [Development Requirements & Roadmap](../Unheard%20-%20Development%20Requirements%20and%20Roadmap.md) into epics and issues.

Each **epic** = one roadmap milestone. Each **issue** is independently assignable, has acceptance criteria, and links back to requirement IDs (`FR-*`, `NFR-*`, etc.) for traceability.

## How to use this

- Work top-to-bottom; the file order is the recommended build order.
- Each issue has a checkbox in its epic file — check it when **Done** (all acceptance criteria met).
- Issues marked 🔒 **Safety-critical** or 🛡️ **Privacy-critical** require elevated review and cannot be descoped to hit a date.
- "Blocked by" lists hard dependencies — do not start an issue until its blockers are Done.

## Importing into a tracker

These map 1:1 to GitHub Issues / Linear:
- Epic file → a GitHub **Milestone** (or Linear **Project**).
- Each `### [ID]` issue → one **Issue**, with the title, body, labels, and "Blocked by" as a dependency link.
- A CSV/script can be generated from these on request once a repo/remote exists.

## Labels

| Label | Meaning |
|---|---|
| `privacy-critical` | Defect can de-anonymize a user. Elevated review + CI gates. |
| `safety-critical` | Defect can harm someone in crisis. Clinical-advisor review. |
| `core` | On the critical path for the MVP. |
| `ml` | Masking / STT / moderation model work. |
| `infra` | Platform, CI, storage, queues. |
| `client` | Mobile/web app. |
| `backend` | API gateway / services. |
| `legal` | Gated on or producing legal/clinical sign-off. |
| `risk` | High-uncertainty; benchmark/spike before committing. |

## Epics (build order)

| # | Epic | Phase | File |
|---|---|---|---|
| E0 | Foundations & safety design | 0 | [E0-foundations.md](E0-foundations.md) |
| E1 | MVP — Masking service | 1 | [E1-masking-service.md](E1-masking-service.md) |
| E2 | MVP — Accounts, auth & Covenant | 1 | [E2-accounts-auth.md](E2-accounts-auth.md) |
| E3 | MVP — Post, feed & topics | 1 | [E3-post-feed.md](E3-post-feed.md) |
| E4 | MVP — Reactions, Echo, originals & delete | 1 | [E4-engagement-originals.md](E4-engagement-originals.md) |
| E5 | MVP — Privacy & security hardening | 1 | [E5-hardening.md](E5-hardening.md) |
| E6 | Comments & poster controls | 2 | [E6-comments.md](E6-comments.md) |
| E7 | Moderation AI & abuse controls | 2 | [E7-moderation.md](E7-moderation.md) |
| E8 | Crisis detection + interim safety bridge | 2 | [E8-crisis-bridge.md](E8-crisis-bridge.md) |
| E9 | Human crisis hotline | 3 | [E9-hotline.md](E9-hotline.md) |
| E10 | Sustainability, ads & nonprofit structure | 4 | [E10-sustainability.md](E10-sustainability.md) |
| E11 | Deepen support & quality | 5 | [E11-deepen.md](E11-deepen.md) |

## Critical dependency gates

- **E9 (hotline) is blocked by** legal counsel sign-off in E0 (`LEGAL-01`).
- **E8 must ship the interim national-line bridge** with crisis detection — never detection alone.
- **E1 masking benchmark** gates the MVP quality exit and informs E9 real-time latency budget.
- **E10 ads** are blocked until the "zero ads in vulnerable surfaces" guard exists.
