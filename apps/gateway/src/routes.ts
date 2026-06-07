/**
 * Central route registry. (API-*)
 *
 * Every endpoint the gateway exposes is declared here as data, so a test can
 * statically assert that NO route exposes a public profile or another account's
 * posting history. (FR-ACCT-03, NFR-PRIV-05)
 *
 * Patterns that must never exist (enforced by test/routes.privacy.test.ts):
 *   - /users/:id, /profiles, /accounts/:id (public account surfaces)
 *   - any route returning another account's history/timeline
 */

export interface RouteDef {
  method: 'GET' | 'POST' | 'DELETE';
  path: string;
  /** Maps to a requirement id for traceability. */
  req: string;
  summary: string;
}

export const ROUTES: readonly RouteDef[] = [
  { method: 'GET', path: '/healthz', req: 'NFR-PERF-05', summary: 'liveness probe' },
  { method: 'POST', path: '/v1/posts', req: 'API-01', summary: 'create post (multipart) -> masked post for preview' },
  { method: 'GET', path: '/v1/feed', req: 'API-02', summary: 'paginated feed: sort + topic' },
  { method: 'DELETE', path: '/v1/posts/:id', req: 'API-03', summary: 'hard delete own post' },
  { method: 'POST', path: '/v1/posts/:id/reactions', req: 'API-04', summary: 'add/remove reaction' },
  { method: 'POST', path: '/v1/posts/:id/comments', req: 'API-05', summary: 'add comment (respects comment_mode)' },
  { method: 'GET', path: '/v1/posts/:id/comments', req: 'API-06', summary: 'list comments (flat)' },
  { method: 'POST', path: '/v1/topics/:topic/follow', req: 'API-07', summary: 'follow/unfollow topic' },
  { method: 'POST', path: '/v1/reports', req: 'API-08', summary: 'report a post or comment' },
  { method: 'GET', path: '/v1/me/posts', req: 'API-09', summary: 'private my-posts (self only)' },
  { method: 'POST', path: '/v1/echoes', req: 'API-10', summary: 'in-app reshare' },
] as const;

/** Route shapes that would betray the identity-less guarantee. */
export const FORBIDDEN_ROUTE_PATTERNS: readonly RegExp[] = [
  /\/users?\//i,
  /\/profiles?\b/i,
  /\/accounts?\/:?\w*id/i,
  /\/authors?\//i,
  /\/timeline/i,
  /\/history/i,
] as const;
