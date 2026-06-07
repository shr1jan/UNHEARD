-- Unheard initial schema. (Requirements §5, DATA-*)
--
-- WHAT IS DELIBERATELY ABSENT IS AS IMPORTANT AS WHAT IS PRESENT.
-- There are NO tables for: original recordings, transcripts, voiceprints,
-- public profiles, posting histories, or hotline phone numbers. (DATA-NEVER-01)
--
-- The masked voicenote (in object storage) is the only audio artifact.
-- Deletes are HARD deletes (no soft-delete columns). (NFR-PRIV-06)

BEGIN;

-- Accounts: hidden internal id only; never exposed to other users. (FR-ACCT-02)
CREATE TABLE accounts (
    internal_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    ban_state          TEXT NOT NULL DEFAULT 'none'
                         CHECK (ban_state IN ('none', 'rate_limited', 'shadow_muted', 'banned')),
    rate_state         JSONB NOT NULL DEFAULT '{}'::jsonb,
    covenant_version   TEXT,            -- which Covenant version was accepted (FR-ACCT-07)
    covenant_accepted_at TIMESTAMPTZ
);

-- Posts: masked audio reference + metadata only. No author identity beyond the
-- hidden owner fk. (FR-POST-08)
CREATE TABLE posts (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id         UUID NOT NULL REFERENCES accounts(internal_id) ON DELETE CASCADE,
    masked_audio_key TEXT NOT NULL,     -- object-store key for the MASKED clip
    topic            TEXT,              -- nullable; topics are optional (FR-POST-02)
    duration_sec     INTEGER NOT NULL CHECK (duration_sec > 0),
    comment_mode     TEXT NOT NULL DEFAULT 'both'
                       CHECK (comment_mode IN ('off', 'text', 'audio', 'both')),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX posts_created_at_idx ON posts (created_at DESC);
CREATE INDEX posts_topic_idx ON posts (topic) WHERE topic IS NOT NULL;
CREATE INDEX posts_owner_idx ON posts (owner_id);   -- powers /v1/me/posts only

-- Reactions: empathy-first; counts are public. One row per (account, post, type).
CREATE TABLE reactions (
    post_id    UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES accounts(internal_id) ON DELETE CASCADE,
    type       TEXT NOT NULL CHECK (type IN ('heard', 'felt', 'strength')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (post_id, account_id, type)
);
CREATE INDEX reactions_post_idx ON reactions (post_id);

-- Comments: FLAT. There is intentionally NO parent_id. (FR-CMT-03)
CREATE TABLE comments (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id          UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    account_id       UUID NOT NULL REFERENCES accounts(internal_id) ON DELETE CASCADE,
    kind             TEXT NOT NULL CHECK (kind IN ('text', 'audio')),
    body_text        TEXT,             -- present when kind = 'text'
    masked_audio_key TEXT,             -- present when kind = 'audio' (MASKED only)
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK ( (kind = 'text'  AND body_text IS NOT NULL AND masked_audio_key IS NULL)
         OR (kind = 'audio' AND masked_audio_key IS NOT NULL AND body_text IS NULL) )
);
CREATE INDEX comments_post_idx ON comments (post_id, created_at);

-- Reports: the reporter is NOT linked to the reported party in any exposed way.
-- (FR-MOD-08, DATA-04) We store who reported only to rate-limit abusive reporting;
-- it must never be joined into a user-facing query.
CREATE TABLE reports (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_type TEXT NOT NULL CHECK (target_type IN ('post', 'comment')),
    target_id   UUID NOT NULL,
    reason      TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Topic follows: drives the topic-filtered feed. Users follow topics, not people.
CREATE TABLE topic_follows (
    account_id UUID NOT NULL REFERENCES accounts(internal_id) ON DELETE CASCADE,
    topic      TEXT NOT NULL,
    PRIMARY KEY (account_id, topic)
);

-- Echoes: in-app reshare only. (FR-FEED-10)
CREATE TABLE echoes (
    post_id    UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES accounts(internal_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (post_id, account_id)
);

COMMIT;
