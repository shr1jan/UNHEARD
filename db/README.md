# db

Postgres schema for Unheard. (Requirements §5, `DATA-*`.)

`migrations/0001_init.sql` creates: `accounts`, `posts`, `reactions`, `comments`
(flat — no `parent_id`), `reports`, `topic_follows`, `echoes`.

## What is NOT here, on purpose

No tables for original recordings, transcripts, voiceprints, public profiles,
posting histories, or hotline phone numbers (`DATA-NEVER-01`). The masked
voicenote in object storage is the only audio artifact. All deletes are hard
deletes (`NFR-PRIV-06`) — note the `ON DELETE CASCADE` chains from `accounts`
and `posts`.

## Apply locally

```bash
# with infra/docker-compose.yml running:
psql "postgres://unheard:unheard@localhost:5432/unheard" -f migrations/0001_init.sql
```

A migration tool (e.g. `node-pg-migrate`, `sqlx`, or the chosen provider's
tooling) is wired in `E0-5`/`E0-6`. Until then these are plain SQL files applied
in order.

## Rule for new migrations

Any migration that adds a column storing user-derived content requires a privacy
review sign-off (`DATA-01`, `NFR-PRIV-07`). See the PR checklist in
`../CONTRIBUTING.md`.
