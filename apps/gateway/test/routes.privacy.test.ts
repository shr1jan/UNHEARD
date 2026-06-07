/**
 * E5-3 — no public-profile or cross-account history endpoints exist.
 * Requirements: FR-ACCT-03, NFR-PRIV-05
 *
 * This is a structural guarantee: if someone adds `/users/:id` or `/v1/accounts/:id/posts`
 * to the registry, this test fails before it can ship.
 */
import { describe, it, expect } from 'vitest';
import { ROUTES, FORBIDDEN_ROUTE_PATTERNS } from '../src/routes.js';
import { scrub } from '../src/lib/logScrub.js';

describe('route registry forbids identity-exposing surfaces (NFR-PRIV-05)', () => {
  for (const route of ROUTES) {
    it(`${route.method} ${route.path} matches no forbidden pattern`, () => {
      for (const pattern of FORBIDDEN_ROUTE_PATTERNS) {
        expect(route.path, `${route.path} matched ${pattern}`).not.toMatch(pattern);
      }
    });
  }

  it('the only self-scoped collection is /v1/me/posts', () => {
    const selfScoped = ROUTES.filter((r) => /\/me\//.test(r.path));
    expect(selfScoped.map((r) => r.path)).toEqual(['/v1/me/posts']);
  });
});

describe('log scrubbing removes sensitive payloads (NFR-PRIV-03)', () => {
  it('redacts sensitive keys and binary payloads', () => {
    const body = {
      transcript: 'I am not okay',
      audio: new Uint8Array([1, 2, 3, 4]), // sensitive key -> redacted by name
      payload: new Uint8Array([9, 9, 9]), // neutral key but binary -> redacted by type
      phone_number: '+15551234567',
      topic: 'loneliness',
    };
    const out = scrub(body) as Record<string, unknown>;
    expect(out.transcript).toBe('[redacted]');
    expect(out.phone_number).toBe('[redacted]');
    expect(out.audio).toBe('[redacted]');
    expect(String(out.payload)).toMatch(/redacted .* bytes/);
    expect(out.topic).toBe('loneliness'); // non-sensitive passes through
  });
});
