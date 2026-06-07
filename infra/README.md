# infra

Local development infrastructure (stack-neutral).

```bash
cd infra
cp .env.example .env
docker compose up -d        # Postgres :5432, Redis :6379, MinIO :9000 (console :9001)
```

- **Postgres** — the relational core (apply `../db/migrations/0001_init.sql`).
- **Redis** — masking/moderation job queue + sliding-window rate-limit state. Run
  ephemeral (no persistence) — it holds no durable user data.
- **MinIO** — S3-compatible object store for **masked** audio (encrypted at rest
  in production). The only audio artifact the platform keeps.

The managed-provider decision (Supabase vs Neon + S3) is `E0-6`. This compose
file exists so feature work isn't blocked on that decision and so local dev never
touches a real backend.

Production environments, secrets management, and CI environments are `E0-5`.
