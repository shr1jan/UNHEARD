# Contributing to Unheard

Unheard is built on two principles that override everything else. Treat them as
acceptance gates, not aspirations:

1. **Identity-less by design** — no real voice stored, no profiles, no aggregatable history.
2. **Survive, don't profit** — funding and structure are a ceiling, not a growth target.

If a change conflicts with either, it is a defect — regardless of how well it works.

## Repo layout

```
apps/client          React Native + TS mobile client          (E0-5 scaffolds the RN app)
apps/gateway         Node + TS API gateway (Fastify)           (E2/E3)
packages/shared      Shared TS domain types                    (DATA-*)
services/masking     Python neural voice conversion (GPU)      (E1)
services/moderation  Python three-way moderation               (E7)
db/migrations        Postgres schema                           (DATA-*)
infra                Local Postgres + Redis + MinIO            (E0-5/E0-6)
scripts              Issue generator + privacy scan
backlog              The 12 epics / 72 issues (source of truth)
```

## Workflow

1. Pick an issue from a phase **Milestone**. Work phases in order; within a phase,
   respect each issue's **Blocked by**.
2. Branch from `main`. Keep changes scoped to one issue where possible.
3. Make the acceptance criteria in the issue pass — that's the Definition of Done.
4. Open a PR. CI must be green (see below). Fill in the PR checklist.

## The CI gates (do not weaken to hit a date)

| Gate | What it proves | Requirement |
|---|---|---|
| `scripts/privacy_scan.sh` | no disk-write primitives on raw-audio paths | NFR-PRIV-02 |
| `services/masking` pytest | masking path performs no disk writes | NFR-PRIV-01, E5-1 |
| `services/moderation` pytest | **pain is never blocked**; crisis offers help | FR-MOD-02, FR-HOT-07 |
| gateway `serialize.test.ts` | internal IDs never serialized | NFR-PRIV-04 |
| gateway `routes.privacy.test.ts` | no profile/history endpoints; logs scrubbed | NFR-PRIV-03/05 |

🔒 **safety-critical** and 🛡️ **privacy-critical** issues require elevated review
(clinical advisor / privacy reviewer respectively) and cannot be descoped.

## PR checklist (paste into the PR body)

```
- [ ] Linked issue and its acceptance criteria are met
- [ ] CI green (privacy-scan, node, python)
- [ ] No new stored field holding user-derived content WITHOUT privacy sign-off (DATA-01)
- [ ] No raw audio / transcript / phone number can reach disk or logs
- [ ] No new endpoint exposes a profile, another account's history, or an internal id
- [ ] For safety-critical changes: clinical-advisor review requested
```

## Local setup

```bash
npm install                      # workspaces: gateway + shared + client
npm run typecheck && npm test    # node side
(cd infra && cp .env.example .env && docker compose up -d)   # Postgres/Redis/MinIO
(cd services/masking    && python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]" && pytest)
(cd services/moderation && python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]" && pytest)
```
