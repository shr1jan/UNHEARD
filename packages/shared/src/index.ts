/**
 * @unheard/shared — domain types shared between the client and the gateway.
 *
 * This file is the typed expression of the data model in
 * `Unheard - Development Requirements and Roadmap.md` §5 (DATA-*).
 *
 * TWO LOAD-BEARING RULES are encoded here:
 *   1. The hidden internal account id (`AccountInternalId`) is a SERVER-ONLY
 *      brand. It MUST NEVER appear in a wire/public type. (NFR-PRIV-04, FR-ACCT-02)
 *   2. There is NO profile / posting-history type, by design. (FR-ACCT-03, NFR-PRIV-05)
 *
 * What is NEVER modeled because it is NEVER stored (DATA-NEVER-01):
 *   original recordings, transcripts, voiceprints/biometrics, public profiles,
 *   posting histories, hotline phone numbers, behavioral tracking profiles.
 */

// ---------------------------------------------------------------------------
// Enums / unions (match the data model exactly)
// ---------------------------------------------------------------------------

/** Empathy-first reactions only — no approval/clout semantics. (FR-FEED-06) */
export type ReactionType = 'heard' | 'felt' | 'strength';

/** Poster-controlled comment policy, set at post time. (FR-POST-04) */
export type CommentMode = 'off' | 'text' | 'audio' | 'both';

/** Comment payload kind. Threading is flat — there is no parent_id. (FR-CMT-03) */
export type CommentKind = 'text' | 'audio';

/** Feed sort options. "needs_love" surfaces low-listen posts. (FR-FEED-03) */
export type FeedSort = 'newest' | 'most_heard' | 'needs_love';

/** Moderation three-way sort. Pain is protected, never blocked. (FR-MOD-01/02) */
export type ModerationVerdict = 'pain' | 'harm' | 'crisis' | 'allow';

/** The fixed, curated starter topic set. Topics are a lens, never a gate. (FR-FEED-09) */
export const TOPICS = [
  'work-life',
  'family',
  'relationships',
  'friendships',
  'mental-health',
  'loneliness',
  'grief',
  'identity',
  'money',
  'health',
  'just-need-to-vent',
] as const;
export type Topic = (typeof TOPICS)[number];

// ---------------------------------------------------------------------------
// Branded server-only identity (must never be serialized to clients)
// ---------------------------------------------------------------------------

declare const SERVER_ONLY: unique symbol;
/**
 * The hidden, stable internal account id. Used ONLY for rate-limit / shadow-mute
 * / ban. The brand makes it a compile-time error to place this on any *Public
 * type below. Enforced at runtime by the gateway serializer + tests. (FR-ACCT-02)
 */
export type AccountInternalId = string & { readonly [SERVER_ONLY]: 'AccountInternalId' };

// ---------------------------------------------------------------------------
// Public wire types (what clients are allowed to receive)
// ---------------------------------------------------------------------------

/** A post as seen in the feed. Note: NO author identity of any kind. */
export interface PublicPost {
  id: string;
  /** Signed, short-lived URL to the MASKED audio (the only audio artifact). (SEC-04) */
  maskedAudioUrl: string;
  topic: Topic | null;
  /** Clip length in seconds. */
  durationSec: number;
  commentMode: CommentMode;
  reactions: Record<ReactionType, number>;
  createdAt: string; // ISO-8601
  /** True only when the *requesting* account owns this post (drives delete UI). */
  isOwn?: boolean;
}

/** A flat comment under a post — no author identity, no parent reference. */
export interface PublicComment {
  id: string;
  postId: string;
  kind: CommentKind;
  /** Present when kind === 'text'. */
  text?: string;
  /** Present when kind === 'audio': signed URL to the MASKED comment audio. */
  maskedAudioUrl?: string;
  createdAt: string;
}

export interface FeedPage {
  items: PublicPost[];
  /** Opaque cursor for the next page, or null at the end. */
  nextCursor: string | null;
}

// ---------------------------------------------------------------------------
// Request payloads
// ---------------------------------------------------------------------------

export interface CreatePostInput {
  /** Set at post time; cannot be added by anyone else later. */
  commentMode: CommentMode;
  topic?: Topic;
}

export interface AddReactionInput {
  type: ReactionType;
}

export interface ReportInput {
  targetType: 'post' | 'comment';
  targetId: string;
  reason: string;
}
