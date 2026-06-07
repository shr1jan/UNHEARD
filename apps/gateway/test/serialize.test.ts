/**
 * E5-2 — internal IDs (and other server-only fields) never serialized.
 * Requirements: NFR-PRIV-04, FR-ACCT-02
 */
import { describe, it, expect } from 'vitest';
import { toPublic, assertNoForbiddenFields } from '../src/lib/serialize.js';

describe('toPublic() strips server-only fields (NFR-PRIV-04)', () => {
  it('removes internal_id / owner_id at the top level', () => {
    const record = {
      id: 'post_1',
      internal_id: 'acct_secret',
      owner_id: 'acct_secret',
      topic: 'grief',
    };
    const pub = toPublic(record) as Record<string, unknown>;
    expect(pub).toEqual({ id: 'post_1', topic: 'grief' });
  });

  it('removes forbidden fields when nested in arrays/objects', () => {
    const feed = {
      items: [
        { id: 'p1', ownerId: 'a1', reactions: { heard: 2 } },
        { id: 'p2', ownerId: 'a2', author: { internalId: 'a2', banState: 'ok' } },
      ],
    };
    const pub = toPublic(feed);
    expect(() => assertNoForbiddenFields(pub)).not.toThrow();
    expect(JSON.stringify(pub)).not.toMatch(/ownerId|internalId|banState/);
  });

  it('assertNoForbiddenFields throws on a leak (fail closed)', () => {
    expect(() => assertNoForbiddenFields({ id: 'x', internal_id: 'leak' })).toThrow(
      /forbidden field/,
    );
  });
});
